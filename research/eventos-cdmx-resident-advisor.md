# Escena de Ciudad de México en Resident Advisor — venues, DJs y géneros

**Investigación para CLSTR · Corte de datos: 29 de agosto de 2026**

Mapa de la escena electrónica de CDMX tal como la organiza Resident Advisor: qué venues
programan, qué colectivos están detrás, qué DJs han tocado y en qué géneros se mueve
cada circuito.

---

## Nota de método: por qué esto no es un volcado directo de RA

**No pude conectarme a `ra.co` desde la sesión donde se hizo esta investigación.** La política
de red del entorno bloquea el egress HTTPS: todo intento de conexión —a RA y a cualquier otro
host— devuelve `403` en el CONNECT del proxy. No es un problema de RA ni de rate limiting, y no
intenté rodearlo.

Eso parte el trabajo en dos entregables:

1. **Este documento**, construido con búsqueda web sobre fuentes secundarias: la propia guía de
   clubes de RA, perfiles de venue y promotor de RA (accesibles vía buscador), y coberturas de
   DJ Mag, Mixmag, Beatportal, Remezcla y prensa mexicana. Sirve como mapa cualitativo de la
   escena: quién programa qué y con qué sonido.
2. **`research/ra_cdmx_scraper.py`**, un script que consulta la API GraphQL pública de RA y saca
   el dataset **completo y autoritativo** —todos los eventos del rango, line-up por evento y la
   etiqueta de género que RA les asigna— desde cualquier máquina con salida a internet.

Dicho de frente: los conteos exactos ("cuántos eventos de techno hubo en julio") sólo salen del
script. Lo que sigue son nombres y adscripciones verificadas en fuentes públicas, no una
extracción censal.

**Fechas y line-ups:** los line-ups citados corresponden a fechas documentadas en las fuentes.
Un artista listado bajo un venue tocó ahí, pero la lista por venue no es exhaustiva.

---

## 1. Cómo obtener el listado completo

```bash
# Últimos 6 meses de eventos en CDMX, con line-up y género por evento
python3 research/ra_cdmx_scraper.py

# Rango explícito
python3 research/ra_cdmx_scraper.py --start 2026-01-01 --end 2026-08-29 -o research/out

# Sólo eventos y line-ups, sin barrido de géneros (mucho más rápido)
python3 research/ra_cdmx_scraper.py --no-genres
```

Genera tres archivos en el directorio de salida:

| Archivo | Contenido |
|---|---|
| `eventos-cdmx.json` | Dataset crudo: evento, fecha, venue, promotores, line-up, géneros, asistentes |
| `eventos-cdmx.csv` | El mismo dataset plano, para Excel / Sheets |
| `resumen-cdmx.md` | Ranking de DJs por número de fechas, distribución de géneros, top de venues |

El script no requiere API key ni dependencias externas (sólo la librería estándar de Python 3).
Resuelve el ID de área de CDMX leyéndolo en vivo de RA en vez de hardcodearlo, pide los datos mes
por mes para no romper la paginación, y obtiene el género de cada evento consultando el filtro de
género de RA —es decir, **la etiqueta oficial de RA, no una inferencia mía** sobre el nombre del
evento.

---

## 2. Los venues y su enfoque de género

IDs de club en RA para ir directo a la ficha (`ra.co/clubs/<id>`):

| Venue | RA | Zona | Enfoque de género |
|---|---|---|---|
| **Fünk** | [176300](https://ra.co/clubs/176300) | Insurgentes Sur 377, Hipódromo / Condesa | Techno, house, deep y tech house, disco-house, subgéneros experimentales |
| **Loo Loo (LooLoo Studio)** | [148331](https://ra.co/clubs/148331) | Juárez | Deep house y techno |
| **Bar Oriente** | [165188](https://ra.co/clubs/165188) | Durango 181, Roma Norte | Techno, indie dance, house, nu-disco, melodic techno, dark disco |
| **yuyu** | [144659](https://ra.co/clubs/144659) | Sótano, centro | Curaduría estricta, estilos electrónicos de vanguardia |
| **Departamento** | [113383](https://ra.co/clubs/113383) | Juárez | Espacio íntimo, música y artes innovadoras |
| **Brutal MX** | — | Cuauhtémoc | Warehouse industrial; techno duro |
| **Club Amok** | — | — | Techno de vanguardia, instalaciones de arte |
| **Sunday Sunday** | — | — | En la guía de mejores clubes de RA |
| **[sic] Community Club** | [198169](https://ra.co/clubs/198169) | — | Club comunitario |
| **Downtown Mexico** | [118455](https://ra.co/clubs/118455) | Centro Histórico | Rooftop / eventos |
| **Radio Escondido** | [233085](https://ra.co/clubs/233085) | — | Apertura reciente |

**Fünk** es el eje del circuito underground desde 2017: Funktion-One, aforo aproximado de 500,
jueves de takeover de colectivos y fines de semana con cabezas de cartel internacionales.

**Loo Loo** es la sala grande del deep house y el techno: declara más de 125 artistas
internacionales pasados por su cabina.

**Bar Oriente** es el más ecléctico de los tres, en un edificio histórico de tres pisos con
sistema VOID; ahí cabe desde techno hasta nu-disco y dark disco en la misma semana.

---

## 3. Colectivos y promotores — dónde vive la curaduría

En CDMX el género lo define más el colectivo que el venue. RA lista promotores en
`ra.co/promoters/<id>`.

| Colectivo | RA | Perfil y sonido |
|---|---|---|
| **Por Detroit** | [89503](https://ra.co/promoters/89503) | Fiesta queer de techno. Política estricta de no discriminación: personas trans y drag queens exentas de cover, y quien no puede pagar puede escribir antes y entrar gratis |
| **Pervert (PervertMX)** | — | Fundada en 2017 por Robin Garcia y Alberto Herbel. Convierte estructuras en desuso en paraísos queer: escenografía inmersiva, dark rooms y sets de techno de día completo. Mismo equipo detrás de Brutal MX |
| **EXT** | — | Rave fundado por Ramón Jaramillo, Gabo Barranco (**AAAA**) y Francisco Ventura (**Lumber Jack**). Lo multigénero es la tesis: representar las escenas superpuestas de la ciudad, no una sola |
| **Dance Your Name** | — | Desde 2013, nacido de DJs sin sede que hacían fiestas en casas. House, techno y artnoise; hoy plataforma orientada al techno. Dirige Gerardo Figueroa (**Fig**), residente de Fünk. Cumplió 13 años en 2026 |
| **Disco Fetish** | — | Fiesta queer, residencia de jueves en Fünk |
| **MORFEMA** | — | Colectivo enteramente femenino, takeover de jueves en Fünk |
| **Capricho** | — | Takeover de jueves en Fünk |
| **MUTEK MX** | [46321](https://ra.co/promoters/46321) | Rama mexicana de MUTEK: electrónica experimental, ambient y audiovisual |
| **Algo Bien**, **Disco Dust**, **Lapi**, **Desculonización** | — | Incubadoras de talento local y emergente |
| **Yu Yu Club** | [77639](https://ra.co/promoters/77639) | Brazo de programación del club |

Un rasgo estructural de esta escena, y que conviene entender antes de programar en ella: **la
presencia queer no es un nicho lateral, es columna vertebral**. Por Detroit, Pervert y Disco
Fetish están entre las fiestas más consolidadas de la ciudad, y su política de puerta es parte
explícita de la propuesta.

---

## 4. DJs identificados

### 4.1 Internacionales documentados en cabinas de CDMX

Agrupados por el venue donde están documentados y con el género que ubica su set.

**En Fünk**

| DJ | Género / registro |
|---|---|
| **Chez Damier** | House de Detroit, deep house clásico |
| **Lil' Louis** | House de Chicago, referencia histórica |
| **DJ Harvey** | Disco, nu-disco, house eclético |
| **Craig Richards** | Minimal / house hipnótico (residente histórico de fabric) |
| **Francesco Del Garda** | Minimal / deep tech de la escuela italiana-rumana |
| **Rhadoo** | Minimal romano (\[a:rpia:r\]) |
| **Fumiya Tanaka** | Minimal techno japonés |
| **Magda** | Minimal / electro, ex-Minus |
| **Daphni** (Caribou) | House melódico, electrónica de club |
| **Seth Troxler** | Tech house, house |
| **Jane Fitz** | Deep / hipnótico, sesiones largas |
| **PARAMIDA** | House, Love On The Rocks; digging ecléctico |

**En Loo Loo**

| DJ | Género / registro |
|---|---|
| **Deep Dish** (Dubfire + Sharam) | Progressive house y deep house; fecha del 23 de enero de 2026 |
| **PARTIBOI69** | Techno, ghetto house y electro; fecha del 9 de mayo de 2026 |
| **Solomun** | Melodic house / deep house |
| **Maceo Plex** | Melodic techno, house |
| **Adriatique** | Melodic house & techno |
| **Jamie Jones** | Tech house |
| **Four Tet** | Electrónica de club, house |
| **Acid Pauli** | Downtempo, house orgánico |

**En Bar Oriente**

| DJ | Género / registro |
|---|---|
| **Aleksandir** | Deep house |
| **Titan** | DJ set, fecha del 26 de junio de 2026 |
| **Julia Toporek**, **Jamira Estrada** | Deep house / bass |
| **Mau Moctezuma**, **Roz**, **Rixxia** | Cartel local documentado en RA |

### 4.2 Artistas mexicanos y residentes de la escena

| Artista | Adscripción |
|---|---|
| **Rebolledo** | House, techno y psicodelia; más de 20 años de carrera internacional. Figura mayor de la escena mexicana |
| **Zombies In Miami** | Dúo; indie dance, dark disco, nu-disco |
| **DJ Fucci** | Underground CDMX; también programado en Fünk |
| **AAAA** (Gabo Barranco) | Productor; cofundador de EXT |
| **Lumber Jack** (Francisco Ventura) | Cofundador de EXT |
| **Fig** (Gerardo Figueroa) | Director de Dance Your Name, residente de Fünk |
| **Young Drums**, **Fina** | Residentes de Dance Your Name |
| **Concepción Huerta** | Electrónica experimental, ambient, drone |
| **Nortec Collective** | Pioneros; fusión de electrónica con música norteña |
| **Coco Maria** | Selectora; tropical, latin, digging de catálogo |
| **Itzvan**, **Cami** (fka Phaedra), **Deejay Energy** | Circuito underground CDMX |
| **1OO1O**, **Celice**, **Enya Botello**, **Sadgal** | Generación emergente perfilada por Beatport Landed |
| **JEWELSSEA** | Programada en Fünk |
| **Andy Martin**, **Koscoy**, **Octoptic**, **Daniel Alanís** | Circuito MUTEK MX |

---

## 5. Los géneros de la escena, por circuito

Lo que se ve al cruzar venues, colectivos y line-ups es que **CDMX no es una ciudad de un solo
género**: son al menos cinco circuitos con públicos que apenas se tocan.

| Circuito | Géneros | Dónde vive |
|---|---|---|
| **Techno duro / industrial** | Techno peak time, industrial, hard techno | Brutal MX, Club Amok, Pervert, Dance Your Name |
| **Minimal / deep tech** | Minimal, microhouse, deep tech de escuela rumana e italiana | Fünk (Rhadoo, Del Garda, Fumiya Tanaka, Craig Richards) |
| **House / disco** | Deep house, house clásico de Chicago y Detroit, disco, nu-disco | Loo Loo, Bar Oriente, Fünk (Chez Damier, Lil' Louis, DJ Harvey) |
| **Indie dance / dark disco / melódico** | Indie dance, dark disco, melodic techno | Bar Oriente, Zombies In Miami |
| **Experimental / A-V** | Ambient, electrónica experimental, live audiovisual | MUTEK MX, Departamento, Concepción Huerta |
| **Latino / mestizo** | Perreo, ritmos latinos, tribal / 3ball, fusión norteña | Escena emergente; DJ Mag señala el perreo como lo que mueve al público joven |
| **EDM / mainstream** | Big room, hardstyle, psytrance, bass, EDM | Circuito de festival, ajeno al underground |

El centro de gravedad del underground de CDMX está en el eje **techno ↔ minimal ↔ house**, con el
matiz de que la ciudad tiene una afinidad inusualmente fuerte con la escuela minimal europea:
Rhadoo, Francesco Del Garda, Fumiya Tanaka y Craig Richards no son bookings de excepción, son
parte del circuito habitual.

---

## 6. Eventos masivos en CDMX (2026)

Fuera del circuito de club, pero determinantes para el calendario de la ciudad:

**EDC México 2026** — 20 al 22 de febrero, Autódromo Hermanos Rodríguez. Duodécima edición, más de
100 artistas y más de 300,000 asistentes esperados. Cartel deliberadamente cruzado entre
mainstream y underground:

- *Cabezas de cartel:* Alesso, Hardwell, Anyma (cierre de cada día)
- *EDM / trance:* Above & Beyond, Zedd
- *Techno:* Charlotte de Witte, Adam Beyer, Indira Paganotto
- *Underground de house y techno:* Four Tet, **Ricardo Villalobos** (su primera presentación en
  México), The Blessed Madonna, Daphni, Helena Hauff, DJ Seinfeld, VTSS, HVOB, Roza Terenzi
- *Local:* 3Ball MTY

**MUTEK MX 2026** — reformateado a dos ciclos, primavera y otoño, con programación de marzo a
noviembre. Andy Stott, Caterina Barbieri, Kaitlyn Aurelia Smith, Sinjin Hawke & Zora Jones,
Max Cooper (19 de julio), y debuts de Loraine James y Koreless. Estrenos: *Entanglement* de
France Jobin & Marcus Heckmann, e instalación y live A/V de SKY H1 & Mika Oki.

**Fiesta electrónica de Año Nuevo** — evento masivo gratuito de la ciudad, con MGTM, Arca y
Kavinsky en la edición de cambio de año.

---

## 7. Limitaciones

- **No hay conteos.** Este documento no dice cuántos eventos hubo ni con qué frecuencia tocó cada
  DJ, porque no tuve acceso al listado. Para eso está el script.
- **Sesgo de cobertura.** Las fuentes secundarias sobre-representan lo que la prensa
  internacional cubre —Fünk, Loo Loo, Bar Oriente y las fiestas queer— y sub-representan el
  circuito de fiestas clandestinas y raves ilegales, que según Beatport es una parte central de
  la escena y por definición no se lista en RA.
- **Los géneros por artista son adscripción, no etiqueta de RA.** En la sección 4 el género es mi
  lectura del perfil del artista. La etiqueta oficial por evento la produce el script.
- **Fechas.** Sólo las fechas explícitas del documento están respaldadas por fuente. La aparición
  de un artista bajo un venue no implica que sea su única ni su más reciente presentación.

---

## Fuentes

Guía de clubes y perfiles de venue/promotor de [Resident Advisor](https://ra.co/guides/clubs-in-mexicocity)
· [RA Guide to Mexico City](https://ra.co/guide/mx/mexicocity)
· [DJ Mag, *Inside Mexico City's vibrant electronic underground*](https://djmag.com/features/inside-mexico-citys-vibrant-electronic-underground)
· [Mixmag sobre EXT](https://mixmag.net/feature/mexico-citys-ext-party-is-inclusive-innovative-and-inexpensive)
· [Mixmag sobre Pervert](https://mixmag.net/feature/pervert-interview-mexico-city-queer-party-functions)
· [Remezcla sobre Ext.](https://remezcla.com/features/music/ext-rave-profile/)
· [Beatportal, *Landed: Mexico City*](https://www.beatportal.com/articles/1206244-beatport-landed-mexico-citys-underground-dance-music-scene)
· [MUTEK MX](https://mexico.mutek.org/en/news/first-wave-of-confirmed-artists-by-program)
· [Lineup EDC México 2026](https://mexico.edc.com/en/)
· [La Jornada sobre Dance Your Name](https://www.jornada.com.mx/2026/08/18/espectaculos/a08n1esp)
· [Fünk Club](https://www.funkclub.mx/)
· [LooLoo Studio](https://wearelooloo.com/)

---

*Documento de investigación interno. Corte: 29/08/2026.*
