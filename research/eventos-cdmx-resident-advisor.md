# CDMX 2026 en Resident Advisor — eventos, DJs y géneros

**Investigación para CLSTR · Año cubierto: 2026 · Corte de datos: 29 de agosto de 2026**

Qué pasó y qué falta por pasar en la escena electrónica de la Ciudad de México durante 2026:
fechas documentadas, quién tocó, en qué venue y bajo qué género.

---

## Nota de método: por qué esto no es un volcado directo de RA

**No pude conectarme a `ra.co` desde la sesión donde se hizo esta investigación.** La política de
red del entorno bloquea el egress HTTPS: todo intento de conexión —a RA y a cualquier otro host—
devuelve `403` en el CONNECT del proxy. No es rate limiting ni un problema de RA, y no intenté
rodearlo.

Eso parte el trabajo en dos entregables:

1. **Este documento.** Calendario 2026 construido con búsqueda web sobre fuentes secundarias: la
   guía de clubes y las fichas de venue/promotor de RA accesibles vía buscador, más coberturas de
   DJ Mag, Mixmag, Beatportal, Time Out México, Milenio, Infobae y La Jornada.
2. **`research/ra_cdmx_scraper.py`**, que consulta la API GraphQL pública de RA y saca el censo
   **completo y autoritativo** de 2026 —todos los eventos, line-up por evento y la etiqueta de
   género oficial de RA— desde cualquier máquina con salida a internet.

Dicho de frente: **los conteos exactos de 2026 sólo salen del script.** Lo que sigue son fechas y
nombres verificados en fuentes públicas, no una extracción censal. Toda fecha citada aquí tiene
fuente; donde sólo hay perfil histórico de un venue sin año confirmado, está marcado como tal.

---

## 1. Cómo obtener el listado completo de 2026

```bash
# El año 2026 completo, con line-up y género por evento
python3 research/ra_cdmx_scraper.py --year 2026 -o research/out

# Sólo lo transcurrido del año
python3 research/ra_cdmx_scraper.py --start 2026-01-01 --end 2026-08-29

# Sin barrido de géneros (mucho más rápido)
python3 research/ra_cdmx_scraper.py --year 2026 --no-genres
```

Genera tres archivos:

| Archivo | Contenido |
|---|---|
| `eventos-cdmx.json` | Dataset crudo: evento, fecha, venue, promotores, line-up, géneros, asistentes |
| `eventos-cdmx.csv` | El mismo dataset plano, para Excel / Sheets |
| `resumen-cdmx.md` | Ranking de DJs por número de fechas, distribución de géneros, top de venues |

Sin API key ni dependencias externas (sólo librería estándar de Python 3). Resuelve el ID de área
de CDMX leyéndolo en vivo de RA en vez de hardcodearlo, pide los datos mes por mes para no romper
la paginación, y obtiene el género de cada evento consultando el filtro de género de RA —es decir,
**la etiqueta oficial de RA, no una inferencia sobre el nombre del evento**.

---

## 2. Calendario 2026 — fechas documentadas

### Enero

| Fecha | Evento | Venue | Género |
|---|---|---|---|
| 23 ene | **Deep Dish** (Dubfire + Sharam) | LooLoo Studio | Progressive house, deep house |

### Febrero — el mes más denso del año

| Fecha | Evento | Venue | Género |
|---|---|---|---|
| 12 feb (jue) | **Ricardo Villalobos & Friends** · ACTO live · Lostnights | Frontón Bucareli | Minimal, microhouse |
| 13 feb (vie) | **Claptone** | LooLoo Studio | House |
| 13–15 feb | **Festival Bahidorá** *(Las Estacas, Morelos — fuera de CDMX)* | — | Afrobeat, jazz, electrónica global |
| 20–22 feb | **EDC México**, 12ª edición | Autódromo Hermanos Rodríguez | Techno, house, hardstyle, psytrance, bass, EDM |

**El regreso de Villalobos es el hecho del año.** El chileno-alemán volvió a tocar en México el
jueves 12 de febrero en el Frontón Bucareli ([evento RA 2342429](https://ra.co/events/2342429)),
en formato "& Friends" con ACTO en vivo bajo el sello Lostnights, vinculado al circuito de Fünk.
*Las fuentes discrepan sobre cuánto llevaba sin pisar el país: unas dicen más de doce años, otras
dieciocho.* Días después tocó en Bahidorá.

**EDC México 2026** — más de 100 artistas y más de 300,000 asistentes esperados, con un cartel
deliberadamente cruzado entre mainstream y underground:

- *Cabezas de cartel:* Alesso, Hardwell, Anyma (cierre de cada día)
- *EDM / trance:* Above & Beyond, Zedd
- *Techno:* Charlotte de Witte, Adam Beyer, Indira Paganotto
- *Underground de house y techno:* Four Tet, The Blessed Madonna, Daphni, Helena Hauff,
  DJ Seinfeld, VTSS, HVOB, Roza Terenzi
- *Local:* 3Ball MTY

### Mayo

| Fecha | Evento | Venue | Género |
|---|---|---|---|
| 9 may (sáb) | **PARTIBOI69** | LooLoo Studio | Techno, ghetto house, electro |
| 23 may (sáb) | **[sic] x Por Detroit** | Versalles 64, Col. Juárez | Techno queer |

El cartel de Por Detroit del 23 de mayo —**Por Detroit, Valeriana, Alby Esc, Enya Botello,
Luigi Bridges**— es un buen retrato del circuito: casi todo local, de 23:00 a 06:00, $350 MXN,
18+ ([evento RA 2447263](https://es-mx.ra.co/events/2447263)).

### Junio–julio — Campo Marte 26 y el Pride

| Fecha | Evento | Venue | Género |
|---|---|---|---|
| 11 jun – 19 jul | **Campo Marte 26** (Music Pavilion / Santander) | [Campo Marte](https://es-mx.ra.co/clubs/178567) | House, indie dance, nu-disco |
| 25 jun (jue) | **Adriatique** | Campo Marte | Melodic house & techno |
| 26 jun (vie) | **Titan** DJ set | Bar Oriente | Electrónica de club |
| 26–28 jun | **Pervert MX** · edición Pride, tres noches | Ubicación revelada el día previo | Disco house, techno |
| 4 jul | **Diplo** | Music Pavilion, Campo Marte | Crossover / dance |
| 19 jul | **Max Cooper** (MUTEK MX) | — | Electrónica experimental, A/V |

**Campo Marte 26** es la novedad estructural del año: un festival de cinco semanas amarrado al
Mundial, con al menos 17 conciertos en el escenario Music Pavilion. Cartel: The Avalanches,
Claptone, Hugel, L'Impératrice, Mathame, Modeselektor, Parcels, Polo & Pan, Purple Disco Machine,
Adriatique y Diplo.

**Pervert MX** hizo su edición más grande hasta la fecha en el Pride, del viernes 26 al domingo 28
de junio. El formato es parte de la propuesta: la ubicación se revela el día anterior. Boletos
desde $335 MXN.

### Agosto

| Fecha | Evento | Venue | Género |
|---|---|---|---|
| Agosto | **Dance Your Name · 13 años** — Fina b2b Young Drums (all night long) | Fünk | Techno, house |

La Jornada perfiló al colectivo el 18 de agosto con motivo del aniversario
([evento RA 2501275](https://ra.co/events/2501275)).

### Septiembre y lo que resta del año

| Fecha | Evento | Nota |
|---|---|---|
| 5 sep | **Reapertura de yuyu Club** en un antiguo casino, con dos eventos por fin de semana durante septiembre | Cambio de sede |
| 15 sep | **Pervert** | Boletos en efectivo en puerta |
| 23–24 oct | Festival Hipnosis | Psicodelia y rock, no electrónica de club — contexto, no escena |
| Marzo–noviembre | **MUTEK MX**, reformateado a dos ciclos (primavera y otoño) | Ver abajo |

**MUTEK MX 2026** abandonó el formato de edición única. Programación: Andy Stott, Caterina
Barbieri, Kaitlyn Aurelia Smith, Sinjin Hawke & Zora Jones, Max Cooper (19 de julio), y debuts de
Loraine James y Koreless. Estrenos: *Entanglement* de France Jobin & Marcus Heckmann, e instalación
y live A/V de SKY H1 & Mika Oki. Bloque local y colaborativo: Kia, Reptant, Andy Martin, Koscoy,
Octoptic, Andreas y Daniel Alanís.

---

## 3. Los venues y su enfoque de género

IDs de club en RA para ir directo a la ficha (`ra.co/clubs/<id>`):

| Venue | RA | Zona | Enfoque de género |
|---|---|---|---|
| **Fünk** | [176300](https://ra.co/clubs/176300) | Insurgentes Sur 377, Hipódromo / Condesa | Techno, house, deep y tech house, disco-house, afro-house, experimental |
| **Loo Loo (LooLoo Studio)** | [148331](https://ra.co/clubs/148331) | Juárez | Deep house y techno |
| **Bar Oriente** | [165188](https://ra.co/clubs/165188) | Durango 181, Roma Norte | Techno, indie dance, house, nu-disco, melodic techno, dark disco |
| **yuyu** | [144659](https://ra.co/clubs/144659) | Nueva sede desde sep 2026 | Curaduría estricta, estilos electrónicos de vanguardia |
| **Departamento** | [113383](https://ra.co/clubs/113383) | Juárez | Espacio íntimo, música y artes innovadoras |
| **Campo Marte** | [178567](https://es-mx.ra.co/clubs/178567) | Chapultepec | Sede de festival; house, indie dance, nu-disco |
| **Pervertmx** | [236089](https://es-mx.ra.co/clubs/236089) | Itinerante | Techno y disco house queer |
| **Brutal MX** | — | Cuauhtémoc | Warehouse industrial; techno duro |
| **Club Amok** | — | — | Techno de vanguardia, instalaciones de arte |
| **[sic] Community Club** | [198169](https://ra.co/clubs/198169) | — | Club comunitario |
| **Radio Escondido** | [233085](https://ra.co/clubs/233085) | — | Apertura reciente |

**Fünk** es el eje del circuito underground desde 2017: Funktion-One, aforo aproximado de 500,
jueves de takeover de colectivos y fines de semana con cabezas de cartel internacionales.
Anunciados para 2026: **Jane Fitz, Seth Troxler, DJ Fucci, JEWELSSEA**, además de Dave Seaman,
Damian Lazarus y Gome.

**Loo Loo** es la sala grande del deep house y el techno, con más de 125 artistas internacionales
declarados en su historial.

**Bar Oriente** es el más ecléctico, en un edificio histórico de tres pisos con sistema VOID: ahí
cabe desde techno hasta nu-disco y dark disco en la misma semana.

> **Perfil histórico de booking, sin fecha 2026 verificada.** Estos nombres definen el gusto de
> cada casa pero **no** están confirmados como fechas de 2026 y por eso quedan fuera del calendario
> de arriba. En Fünk: Chez Damier, Lil' Louis, DJ Harvey, Craig Richards, Francesco Del Garda,
> Rhadoo, Fumiya Tanaka, Magda, Daphni, PARAMIDA. En Loo Loo: Solomun, Maceo Plex, Jamie Jones,
> Four Tet, Acid Pauli, Worakls, Infected Mushroom. En Bar Oriente: Aleksandir, Julia Toporek,
> Jamira Estrada.

---

## 4. Colectivos y promotores — dónde vive la curaduría

En CDMX el género lo define más el colectivo que el venue.

| Colectivo | RA | Perfil y sonido |
|---|---|---|
| **Por Detroit** | [89503](https://ra.co/promoters/89503) | Fiesta queer de techno. Política estricta de no discriminación: personas trans y drag queens exentas de cover, y quien no puede pagar puede escribir antes y entrar gratis |
| **Pervert MX** | [80633](https://es.ra.co/promoters/80633) | Fundada en 2017 por Robin Garcia y Alberto Herbel. Fiesta itinerante de disco house y techno; convierte estructuras en desuso en paraísos queer. Mismo equipo detrás de Brutal MX. Atrae público de EE. UU. y el resto de Latinoamérica |
| **EXT** | — | Rave fundado por Ramón Jaramillo, Gabo Barranco (**AAAA**) y Francisco Ventura (**Lumber Jack**). Lo multigénero es la tesis: representar las escenas superpuestas de la ciudad, no una sola |
| **Dance Your Name** | — | Desde 2013, nacido de DJs sin sede que hacían fiestas en casas. House, techno y artnoise. Dirige Gerardo Figueroa (**Fig**), residente de Fünk. Cumplió 13 años en 2026 |
| **Disco Fetish** | — | Fiesta queer, residencia de jueves en Fünk |
| **MORFEMA** | — | Colectivo enteramente femenino, takeover de jueves en Fünk |
| **Capricho** | — | Takeover de jueves en Fünk |
| **MUTEK MX** | [46321](https://ra.co/promoters/46321) | Electrónica experimental, ambient y audiovisual |
| **Yu Yu Club** | [77639](https://ra.co/promoters/77639) | Brazo de programación del club |
| **Algo Bien**, **Disco Dust**, **Lapi**, **Desculonización** | — | Incubadoras de talento local y emergente |

Un rasgo estructural, y que conviene entender antes de programar en esta ciudad: **la presencia
queer no es un nicho lateral, es columna vertebral.** Por Detroit, Pervert y Disco Fetish están
entre las fiestas más consolidadas, y su política de puerta es parte explícita de la propuesta.

---

## 5. Artistas mexicanos y residentes activos en 2026

| Artista | Adscripción |
|---|---|
| **Rebolledo** | House, techno y psicodelia; más de 20 años de carrera internacional. Figura mayor de la escena mexicana |
| **Zombies In Miami** | Dúo; indie dance, dark disco, nu-disco |
| **DJ Fucci** | Underground CDMX; programado en Fünk en 2026 |
| **AAAA** (Gabo Barranco) | Productor; cofundador de EXT |
| **Lumber Jack** (Francisco Ventura) | Cofundador de EXT |
| **Fig** (Gerardo Figueroa) | Director de Dance Your Name, residente de Fünk |
| **Fina**, **Young Drums** | Residentes de Dance Your Name; b2b del 13º aniversario |
| **Enya Botello**, **Valeriana**, **Alby Esc**, **Luigi Bridges** | Cartel de Por Detroit, mayo 2026 |
| **Concepción Huerta** | Electrónica experimental, ambient, drone |
| **Nortec Collective** | Pioneros; fusión de electrónica con música norteña |
| **Coco Maria** | Selectora; tropical, latin, digging de catálogo |
| **Itzvan**, **Cami** (fka Phaedra), **Deejay Energy** | Circuito underground CDMX |
| **1OO1O**, **Celice**, **Sadgal** | Generación emergente perfilada por Beatport Landed |
| **JEWELSSEA** | Programada en Fünk en 2026 |
| **Andy Martin**, **Koscoy**, **Octoptic**, **Daniel Alanís** | Circuito MUTEK MX 2026 |

---

## 6. Los géneros de 2026, por circuito

Al cruzar el calendario con los venues y colectivos, **CDMX no es una ciudad de un solo género**:
son al menos siete circuitos con públicos que apenas se tocan.

| Circuito | Géneros | Evidencia en 2026 |
|---|---|---|
| **Minimal / microhouse** | Minimal, microhouse, deep tech | Villalobos en Frontón Bucareli (12 feb) — el evento más significativo del año |
| **Techno duro / industrial** | Techno peak time, industrial, hard techno | Brutal MX, Club Amok, Pervert, Dance Your Name; De Witte, Beyer y Paganotto en EDC |
| **Techno queer** | Techno y disco house con política de puerta | Por Detroit (23 may), Pervert Pride (26–28 jun) y 15 sep |
| **House / disco / nu-disco** | Deep house, house clásico, disco, nu-disco | Deep Dish (23 ene), Claptone (13 feb), Campo Marte completo |
| **Indie dance / melódico** | Indie dance, dark disco, melodic techno | Bar Oriente; Adriatique y Mathame en Campo Marte |
| **Electro / ghetto house** | Electro, ghetto house | PARTIBOI69 (9 may) |
| **Experimental / A-V** | Ambient, experimental, live audiovisual | MUTEK MX (marzo–noviembre); Max Cooper, Andy Stott, Caterina Barbieri |
| **EDM / mainstream** | Big room, hardstyle, psytrance, bass | EDC México (20–22 feb) |

El centro de gravedad del underground sigue en el eje **techno ↔ minimal ↔ house**. El dato que
más define a 2026: la ciudad confirmó su afinidad con la escuela minimal europea trayendo a
Villalobos tras más de una década de ausencia, y a la vez abrió un frente nuevo de festival diurno
de house y nu-disco con Campo Marte 26.

---

## 7. Limitaciones

- **No hay conteos.** Este documento no dice cuántos eventos hubo en 2026 ni cuántas fechas tocó
  cada DJ, porque no tuve acceso al listado. Para eso está el script.
- **Sesgo hacia lo anunciado.** Las fuentes secundarias cubren bien el evento grande con boletaje y
  prensa, y mal la fecha de club de un martes cualquiera. El calendario de arriba está sesgado
  hacia lo que se promocionó.
- **Circuito clandestino ausente.** Las raves ilegales y fiestas en espacios clandestinos son,
  según Beatport, parte central de esta escena — y por definición no se listan en RA ni en prensa.
- **Los géneros por artista son adscripción, no etiqueta de RA.** En las secciones 2 y 5 el género
  es mi lectura del perfil del artista. La etiqueta oficial por evento la produce el script.
- **Un dato en disputa:** cuánto llevaba Villalobos sin tocar en México. Las fuentes dan entre doce
  y dieciocho años; no elegí una al azar.

---

## Fuentes

[RA — Best Clubs in Mexico City](https://ra.co/guides/clubs-in-mexicocity)
· [RA Guide to Mexico City](https://ra.co/guide/mx/mexicocity)
· [RA — Ricardo Villalobos & Friends, Frontón Bucareli](https://ra.co/events/2342429)
· [RA — \[sic\] x Por Detroit, Versalles 64](https://es-mx.ra.co/events/2447263)
· [RA — Dance Your Name 13 años](https://ra.co/events/2501275)
· [DJ Mag, *Inside Mexico City's vibrant electronic underground*](https://djmag.com/features/inside-mexico-citys-vibrant-electronic-underground)
· [Mixmag sobre EXT](https://mixmag.net/feature/mexico-citys-ext-party-is-inclusive-innovative-and-inexpensive)
· [Mixmag sobre Pervert](https://mixmag.net/feature/pervert-interview-mexico-city-queer-party-functions)
· [Beatportal, *Landed: Mexico City*](https://www.beatportal.com/articles/1206244-beatport-landed-mexico-citys-underground-dance-music-scene)
· [MUTEK MX 2026](https://mexico.mutek.org/en/news/first-wave-of-confirmed-artists-by-program)
· [EDC México 2026](https://mexico.edc.com/en/)
· [Campo Marte 26 — Infobae](https://www.infobae.com/mexico/2026/04/09/campo-marte-26-todos-los-artistas-confirmados-fechas-y-precios-de-boletos-para-el-festival-del-mundial-2026/)
· [Bahidorá 2026 — Milenio](https://www.milenio.com/espectaculos/musica/festival-bahidora-2026-revela-cartel-fechas-costo-boletos)
· [Villalobos regresa a México — Beat Digital](https://beatdigital.mx/news/ricardo-villalobos-regresa-a-mexico/)
· [Pervert MX Pride — Time Out México](https://www.timeoutmexico.mx/ciudad-de-mexico/gay-y-lesbico/pervert-una-fiesta-libre-de-prejuicios)
· [Reapertura de YuYu — Time Out México](https://www.timeoutmexico.mx/ciudad-de-mexico/musica/yuyu-club-reapertura-cdmx-cuauhtemoc)
· [La Jornada sobre Dance Your Name](https://www.jornada.com.mx/2026/08/18/espectaculos/a08n1esp)
· [Fünk Club](https://www.funkclub.mx/) · [LooLoo Studio](https://wearelooloo.com/)

---

*Documento de investigación interno. Año cubierto: 2026. Corte: 29/08/2026.*
