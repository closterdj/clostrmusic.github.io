#!/usr/bin/env python3
"""
ra_cdmx_scraper.py — Eventos de Resident Advisor en la Ciudad de México.

Extrae, para un rango de fechas:
  1. Todos los eventos listados en RA para el área de CDMX.
  2. El line-up completo (los DJs que tocaron en cada evento).
  3. El género con el que RA clasifica cada evento (techno, house, minimal, ...).

Y produce tres salidas: JSON crudo, CSV plano y un resumen en Markdown con
ranking de DJs, distribución de géneros y desglose por venue.

Uso básico (últimos 6 meses, resuelve el área automáticamente):

    python3 research/ra_cdmx_scraper.py

Rango explícito y directorio de salida:

    python3 research/ra_cdmx_scraper.py --start 2026-01-01 --end 2026-08-29 -o research/out

Eventos futuros en lugar de pasados:

    python3 research/ra_cdmx_scraper.py --start 2026-08-29 --end 2026-12-31

Notas:
  - No requiere API key. RA expone un endpoint GraphQL público en /graphql, que es
    el mismo que consume su propio front-end.
  - Sólo usa la librería estándar de Python 3 (urllib). Sin dependencias.
  - RA está detrás de Cloudflare. Si empiezan a llegar 403, baja el ritmo con
    --sleep 2 o corre el script desde una red doméstica.
"""

import argparse
import csv
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta

GRAPHQL_URL = "https://ra.co/graphql"
AREA_PAGE = "https://ra.co/events/mx/mexicocity"

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

# Slugs de género tal como RA los usa en sus filtros y en las URLs
# del tipo /events/mx/mexicocity/<genero>.
GENRE_SLUGS = [
    "techno", "house", "techhouse", "minimal", "deephouse", "disco",
    "electro", "dubtechno", "ambient", "drumandbass", "dubstep", "trance",
    "hardtechno", "breakbeat", "indiedance", "progressivehouse", "psytrance",
    "bassmusic", "experimental", "leftfield", "funk", "hiphop", "uktgarage",
]

EVENT_FIELDS = """
fragment eventFields on Event {
  id
  date
  startTime
  endTime
  title
  contentUrl
  flyerFront
  isTicketed
  attending { id }
  pick { id blurb }
  venue {
    id
    name
    contentUrl
    live
    area { id name urlName country { id name urlCode } }
  }
  artists { id name }
  promoters { id name }
}
"""

LISTINGS_QUERY = """
query GET_EVENT_LISTINGS(
  $filters: FilterInputDtoInput
  $filterOptions: FilterOptionsInputDtoInput
  $page: Int
  $pageSize: Int
) {
  eventListings(
    filters: $filters
    filterOptions: $filterOptions
    pageSize: $pageSize
    page: $page
  ) {
    data {
      id
      listingDate
      event { ...eventFields }
    }
    totalResults
  }
}
""" + EVENT_FIELDS


# --------------------------------------------------------------------------- #
# Transporte HTTP
# --------------------------------------------------------------------------- #

def _request(url, data=None, headers=None, timeout=45):
    req = urllib.request.Request(url, data=data, headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def http_get(url, retries=3, sleep=1.0):
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "es-MX,es;q=0.9,en;q=0.8",
    }
    last = None
    for attempt in range(retries):
        try:
            return _request(url, headers=headers)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
            last = exc
            time.sleep(sleep * (2 ** attempt))
    raise RuntimeError("GET falló en %s: %s" % (url, last))


def graphql(query, variables, operation, retries=4, sleep=1.0):
    payload = json.dumps(
        {"query": query, "variables": variables, "operationName": operation}
    ).encode("utf-8")
    headers = {
        "User-Agent": USER_AGENT,
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Accept-Language": "es-MX,es;q=0.9,en;q=0.8",
        "Origin": "https://ra.co",
        "Referer": AREA_PAGE,
        "ra-content-language": "es",
    }
    last = None
    for attempt in range(retries):
        try:
            raw = _request(GRAPHQL_URL, data=payload, headers=headers)
            body = json.loads(raw)
            if body.get("errors"):
                raise RuntimeError("GraphQL devolvió errores: %s" % body["errors"])
            return body["data"]
        except (urllib.error.URLError, urllib.error.HTTPError,
                TimeoutError, json.JSONDecodeError) as exc:
            last = exc
            time.sleep(sleep * (2 ** attempt))
    raise RuntimeError("Consulta GraphQL '%s' falló: %s" % (operation, last))


# --------------------------------------------------------------------------- #
# Resolución del área
# --------------------------------------------------------------------------- #

def resolve_area_id(url_name="mexicocity"):
    """Lee el ID numérico de área desde el __NEXT_DATA__ de la página de RA.

    RA cambia estos IDs muy rara vez, pero prefiero leerlo en vivo antes que
    hardcodear un número que puede quedar obsoleto sin aviso.
    """
    html = http_get(AREA_PAGE)
    patterns = [
        r'"areaId"\s*:\s*(\d+)',
        r'"area"\s*:\s*\{[^{}]*?"id"\s*:\s*"?(\d+)"?[^{}]*?"urlName"\s*:\s*"%s"' % url_name,
        r'"urlName"\s*:\s*"%s"[^{}]*?"id"\s*:\s*"?(\d+)"?' % url_name,
    ]
    for pattern in patterns:
        match = re.search(pattern, html)
        if match:
            return int(match.group(1))
    raise RuntimeError(
        "No pude resolver el areaId de CDMX automáticamente. "
        "Abre %s, busca 'areaId' en el HTML y pásalo con --area-id." % AREA_PAGE
    )


# --------------------------------------------------------------------------- #
# Descarga de listados
# --------------------------------------------------------------------------- #

def _iso(day):
    return day.strftime("%Y-%m-%dT00:00:00.000Z")


def month_chunks(start, end):
    """Parte el rango en tramos mensuales.

    La paginación profunda de RA se vuelve inestable pasados unos cientos de
    resultados; pedir mes por mes mantiene cada consulta corta y estable.
    """
    cursor = start
    while cursor <= end:
        if cursor.month == 12:
            nxt = date(cursor.year + 1, 1, 1)
        else:
            nxt = date(cursor.year, cursor.month + 1, 1)
        yield cursor, min(nxt - timedelta(days=1), end)
        cursor = nxt


def fetch_listings(area_id, start, end, genre=None, page_size=100, sleep=1.0,
                   verbose=True):
    """Devuelve los eventos del rango, opcionalmente filtrados por género."""
    events = {}
    for chunk_start, chunk_end in month_chunks(start, end):
        page = 1
        while True:
            filters = {
                "areas": {"eq": area_id},
                "listingDate": {"gte": _iso(chunk_start), "lte": _iso(chunk_end)},
            }
            if genre:
                filters["genre"] = {"eq": genre}

            data = graphql(
                LISTINGS_QUERY,
                {
                    "filters": filters,
                    "filterOptions": {"genre": True},
                    "page": page,
                    "pageSize": page_size,
                },
                "GET_EVENT_LISTINGS",
                sleep=sleep,
            )
            listings = (data or {}).get("eventListings") or {}
            rows = listings.get("data") or []
            total = listings.get("totalResults") or 0

            for row in rows:
                event = row.get("event") or {}
                if event.get("id"):
                    event["listingDate"] = row.get("listingDate")
                    events[event["id"]] = event

            if verbose and page == 1 and total:
                label = genre or "todos los géneros"
                print("  %s..%s [%s]: %d eventos"
                      % (chunk_start, chunk_end, label, total), file=sys.stderr)

            if not rows or page * page_size >= total:
                break
            page += 1
            time.sleep(sleep)
        time.sleep(sleep)
    return events


def tag_genres(area_id, start, end, sleep=1.0, genres=None, verbose=True):
    """Mapea id_evento -> [géneros], consultando un filtro por género.

    Este es el dato de género *autoritativo* de RA: son las mismas etiquetas
    que alimentan /events/mx/mexicocity/<genero>. No se infiere nada.
    """
    mapping = defaultdict(list)
    totals = {}
    for slug in (genres or GENRE_SLUGS):
        if verbose:
            print("  género: %s" % slug, file=sys.stderr)
        try:
            found = fetch_listings(area_id, start, end, genre=slug, sleep=sleep,
                                   verbose=False)
        except RuntimeError as exc:
            print("    (omitido: %s)" % exc, file=sys.stderr)
            continue
        totals[slug] = len(found)
        for event_id in found:
            mapping[event_id].append(slug)
        time.sleep(sleep)
    return mapping, totals


# --------------------------------------------------------------------------- #
# Normalización y reportes
# --------------------------------------------------------------------------- #

def flatten(event, genres_by_event):
    venue = event.get("venue") or {}
    area = venue.get("area") or {}
    artists = [a.get("name") for a in (event.get("artists") or []) if a.get("name")]
    promoters = [p.get("name") for p in (event.get("promoters") or []) if p.get("name")]
    url = event.get("contentUrl") or ""
    return {
        "id": event.get("id"),
        "fecha": (event.get("date") or "")[:10],
        "titulo": event.get("title"),
        "venue": venue.get("name"),
        "venue_id": venue.get("id"),
        "area": area.get("name"),
        "promotores": " | ".join(promoters),
        "lineup": " | ".join(artists),
        "num_djs": len(artists),
        "generos": " | ".join(sorted(genres_by_event.get(event.get("id"), []))),
        "asistentes_ra": len(event.get("attending") or []),
        "ra_pick": bool(event.get("pick")),
        "url": ("https://ra.co" + url) if url.startswith("/") else url,
    }


def build_markdown(rows, genre_totals, start, end, area_id):
    dj_counter = Counter()
    dj_genres = defaultdict(Counter)
    venue_counter = Counter()
    promoter_counter = Counter()
    genre_counter = Counter()

    for row in rows:
        genres = [g for g in row["generos"].split(" | ") if g]
        for g in genres:
            genre_counter[g] += 1
        if row["venue"]:
            venue_counter[row["venue"]] += 1
        for promoter in [p for p in row["promotores"].split(" | ") if p]:
            promoter_counter[promoter] += 1
        for dj in [d for d in row["lineup"].split(" | ") if d]:
            dj_counter[dj] += 1
            for g in genres:
                dj_genres[dj][g] += 1

    out = []
    add = out.append
    add("# Eventos de Resident Advisor en CDMX — %s a %s\n" % (start, end))
    add("Generado por `research/ra_cdmx_scraper.py` el %s. Área RA: `%d`.\n"
        % (date.today().isoformat(), area_id))
    add("- **Eventos listados:** %d" % len(rows))
    add("- **DJs distintos identificados:** %d" % len(dj_counter))
    add("- **Venues distintos:** %d" % len(venue_counter))
    add("- **Promotores distintos:** %d\n" % len(promoter_counter))

    add("## Distribución por género\n")
    add("| Género | Eventos | % del total |")
    add("|---|---:|---:|")
    total = len(rows) or 1
    for slug, count in genre_counter.most_common():
        add("| %s | %d | %.1f%% |" % (slug, count, 100.0 * count / total))
    sin_genero = sum(1 for r in rows if not r["generos"])
    if sin_genero:
        add("| _(sin etiqueta de género en RA)_ | %d | %.1f%% |"
            % (sin_genero, 100.0 * sin_genero / total))
    add("")

    add("## DJs con más fechas\n")
    add("| # | DJ | Fechas | Géneros dominantes |")
    add("|---:|---|---:|---|")
    for i, (dj, count) in enumerate(dj_counter.most_common(80), 1):
        top = ", ".join(g for g, _ in dj_genres[dj].most_common(3)) or "—"
        add("| %d | %s | %d | %s |" % (i, dj, count, top))
    add("")

    add("## Venues con más eventos\n")
    add("| Venue | Eventos |")
    add("|---|---:|")
    for venue, count in venue_counter.most_common(40):
        add("| %s | %d |" % (venue, count))
    add("")

    add("## Promotores con más eventos\n")
    add("| Promotor | Eventos |")
    add("|---|---:|")
    for promoter, count in promoter_counter.most_common(40):
        add("| %s | %d |" % (promoter, count))
    add("")
    return "\n".join(out)


# --------------------------------------------------------------------------- #

def main():
    parser = argparse.ArgumentParser(
        description="Extrae eventos, line-ups y géneros de RA para CDMX.")
    today = date.today()
    parser.add_argument("--start", default=str(today - timedelta(days=180)),
                        help="Fecha inicial YYYY-MM-DD (default: hace 180 días)")
    parser.add_argument("--end", default=str(today),
                        help="Fecha final YYYY-MM-DD (default: hoy)")
    parser.add_argument("--area-id", type=int, default=None,
                        help="ID de área de RA. Si se omite, se resuelve solo.")
    parser.add_argument("-o", "--out-dir", default="research/out",
                        help="Directorio de salida (default: research/out)")
    parser.add_argument("--sleep", type=float, default=1.0,
                        help="Pausa entre peticiones en segundos (default: 1.0)")
    parser.add_argument("--no-genres", action="store_true",
                        help="Omite el barrido por género (mucho más rápido)")
    args = parser.parse_args()

    start = datetime.strptime(args.start, "%Y-%m-%d").date()
    end = datetime.strptime(args.end, "%Y-%m-%d").date()
    if start > end:
        parser.error("--start no puede ser posterior a --end")

    area_id = args.area_id
    if area_id is None:
        print("Resolviendo areaId de CDMX...", file=sys.stderr)
        area_id = resolve_area_id()
    print("Área CDMX = %d" % area_id, file=sys.stderr)

    print("Descargando eventos %s .. %s" % (start, end), file=sys.stderr)
    events = fetch_listings(area_id, start, end, sleep=args.sleep)
    print("Total de eventos: %d" % len(events), file=sys.stderr)

    genres_by_event, genre_totals = {}, {}
    if not args.no_genres:
        print("Etiquetando géneros...", file=sys.stderr)
        genres_by_event, genre_totals = tag_genres(
            area_id, start, end, sleep=args.sleep)

    rows = [flatten(e, genres_by_event) for e in events.values()]
    rows.sort(key=lambda r: (r["fecha"] or "", r["titulo"] or ""))

    os.makedirs(args.out_dir, exist_ok=True)
    json_path = os.path.join(args.out_dir, "eventos-cdmx.json")
    csv_path = os.path.join(args.out_dir, "eventos-cdmx.csv")
    md_path = os.path.join(args.out_dir, "resumen-cdmx.md")

    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump(
            {
                "area_id": area_id,
                "rango": {"inicio": str(start), "fin": str(end)},
                "generado": datetime.now().isoformat(timespec="seconds"),
                "totales_por_genero": genre_totals,
                "eventos": rows,
            },
            fh, ensure_ascii=False, indent=2,
        )

    if rows:
        with open(csv_path, "w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)

    with open(md_path, "w", encoding="utf-8") as fh:
        fh.write(build_markdown(rows, genre_totals, start, end, area_id))

    print("\nListo:\n  %s\n  %s\n  %s" % (json_path, csv_path, md_path),
          file=sys.stderr)


if __name__ == "__main__":
    main()
