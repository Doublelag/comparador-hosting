# MontaTuServer — calculadora de RAM y hostings de Minecraft

Calculadora de RAM para servidores de **Minecraft** y comparativa de precios de
hosting. Web estática: sin dependencias, sin framework. **Sin partner de
afiliación** desde el 11-sep-2026 (ver la sección del partner al final).

    python build.py     # regenera todas las páginas + sitemap + buscador
    python make_og.py   # regenera la imagen de compartir (og-image.jpg)
    python publicar.py  # prepara dist/ para arrastrarlo a Netlify

---

## Solo Minecraft (desde el 17-sep-2026)

La web era de 11 juegos y ahora es **solo de Minecraft**, más sencilla y
centrada. Qué cambió:

- **La portada ES la calculadora de Minecraft.** Ya no hay selector de juego ni
  páginas por juego (`/valheim/`, `/rust/`…). `build.py` ya no copia `index.html`.
- **`_redirects`** (Netlify) manda con un 301 a la portada todas las URLs viejas
  de juegos, `/minecraft/` incluida, y `/hosting/gportal/` a `/hosting/`. Los
  enlaces compartidos antiguos (`?j=valheim&p=…`) abren la calculadora de Minecraft.
- Se quedan: `/minecraft/mejor-hosting/`, `/minecraft/como-montar-un-servidor/`,
  las 15 fichas de `/hosting/`, los 9 cara a cara, `/ofertas/` y el ping.
- **Fuera:** GPORTAL (no vendía Minecraft), la guía y comparativas de otros
  juegos (`comparativas_extra.py` borrado), las ofertas de Valheim.
- `hosts.js` sigue guardando los precios en `precios.minecraft` a propósito: si
  algún día vuelve un juego, se añade su entrada al lado.
- Las fichas de hosting enseñan ahora lo que cobra cada uno por 2/4/8/16/32 GB
  de Minecraft, y el índice de hostings compara 4, 8 y 16 GB.

Copia de todo lo anterior: `antes-minecraft.tgz` en el scratchpad de la sesión
del 17-sep-2026.

---

## Godlike.host y el coste del primer año (19-sep-2026)

**Godlike ya está en la web como un hosting más**, con sus precios comprobados
a mano en su web ese día:

| GB | Al mes (tarifa) | Primera compra (−75 %) |
|---|---|---|
| 2 | 6,29 € | 1,57 € |
| 4 | 12,99 € | 3,25 € |
| 6 | 18,99 € | 4,75 € |
| 8 | 25,99 € | 6,50 € |
| 12 | 37,99 € | 9,50 € |
| 16 | 50,99 € | 12,75 € |
| 20 | 63,99 € | 16,00 € |

Lo importante, y lo que hay que tener claro antes de vender nada:

- **El −75 % es de la PRIMERA COMPRA**, no recurrente. Lo pone su propia web al
  lado del precio ("first purchase discount"), con cuenta atrás que se reinicia.
- **De tarifa son 3,19 €/GB**, de los más caros de la tabla: solo Apex cobra más
  por 16 GB. Nada que ver con el "1 $/GB" del plan de ventas.
- Pagando por adelantado baja: −10 % a 90 días, −15 % a 180, **−20 % a 360**
  (16 GB = 486,99 € el año, 40,58 €/mes → 2,54 €/GB). Sigue siendo caro.
- **Su configurador es lo mejor que tienen**: eliges gigas (2-33), plazas
  (5-200) y **días** (30/90/180/360). Casi nadie deja elegir duración.
- Servidor gratis de 2 GB durante 1 día, sin tarjeta.
- Empresa rumana: Godlike Digital Solutions SRL.
- Su programa de afiliados: Starter 30 % de la primera compra o 15 % recurrente;
  Bronze 50/20; Gold 70/25; Partner 90/30. Piden 7.500 subs en YouTube (Double
  tiene 217k, entra de sobra).

`hosts.js → partner.hostId` ya apunta a `"godlike"`. **Falta enlace y código**
para poner `activo: true`.

---

## Lo que pagas el primer año (19-sep-2026)

La mejora más grande de la web, copiada de los comparadores de seguros y de
telefonía, donde llevan años separando "primer año" de "a partir del segundo".
En hosting no lo hace nadie, y es justo donde está la trampa del sector.

- En `hosts.js`, la tarifa de `tiers`/`porGB` es **siempre la recurrente**. El
  descuento de entrada va aparte, en `precios.minecraft.entrada`:
  `{"pct": 75, "meses": 1, "que": "la primera compra"}`.
- Con eso, `coste_primer_ano()` (comparativas.py) y `preciosDe()` (app.js)
  calculan lo que llevas gastado a los 12 meses.
- Dónde se ve: columna **«12 meses»** en la tabla de la calculadora, aviso
  naranja bajo las barras cuando el precio de entrada es el más barato pero
  renueva caro, tabla **«Lo que pagas el primer año»** en la comparativa, y
  aviso en la ficha del que lo tenga.
- Lo tienen: Godlike (−75 % primera compra), HolyHosting y Apex (−25 % primer mes).

## Otras mejoras del 19-sep-2026

- **Columna «Por GB»** en /hosting/, y la tabla se ordena por ella. Es el precio
  por kilo del súper: lo único que compara planes cerrados con tarifas por giga.
  Se divide entre los gigas que te DAN (DatHost sale a 0,93 €, no a 1,86 €).
- **Filtros** en /hosting/ (`filtros_ui.js`): menos de 1,50 €/GB, sin descuento
  de entrada, por gigabyte, plan cerrado, por uso. Solo dato duro, nada de
  "recomendado". Se apoyan en los `data-*` que escribe hostings.py.
- **El nombre del hosting lleva a su ficha** desde el gráfico y la tabla de la
  calculadora (campo `ficha` en cada host de hosts.js).
- **Primera columna fija** en las tablas en móvil.
- Quien vende por plazas (Realms) **no entra** en la tabla del primer año ni
  tiene euro/GB: sin RAM publicada, ese número no se puede saber.

---

## Revisión de precios del 19-sep-2026 (comprobada a mano)

`revisar_precios.py` dio 12 correctos, 4 sospechosos y 4 ilegibles. Los ocho que
no pudo leer los comprobé a mano en el navegador. Resultado:

- **BisectHosting: ha subido** de 2,66 € a **2,69 €/GB**, y además **cambió de
  URL** (`/games/minecraft` da 404; ahora es `/minecraft-servers`).
- **Nodecraft ha rehecho su web entera.** Ya no hay Budget/Premium en euros:
  ahora te hacen tres preguntas y te asignan plan de la gama **Pro** (24/7, IP
  propia): 2 GB 9,98 $ · 4 GB 19,98 $ · 8 GB 39,98 $ · 12 GB 59,98 $ = **4,99 $/GB**,
  con **−30 % el primer mes** y prueba de 24 h que **pide verificar el teléfono**.
  Su gama **Lite** (se enciende bajo demanda) sigue existiendo pero **ya no
  publica precio**. En la web quedan fusionados en un solo `nodecraft`.
- **Vultam tiene una tercera gama**: Performance, **3,50 $/GB**, Ryzen 9 5950X y
  copias cada 12 horas. Añadida como `vultam-performance`.
- **Sparked Host**: confirmados 2,59 $ (Enterprise) y 4,00 $ (Extreme). Tienen
  **prueba gratis de 1 día**, y las copias vienen justas (3 incluidas, ampliar cuesta).
- Confirmados sin cambios: PebbleHost (1 $ y 2,25 $/GB), Vultam Standard y
  Advanced, Godlike,
  Realms, WiseHosting, NexoHost, The Minecraft Hosting, DatHost, Shockbyte,
  Apex, Hostinger, HolyHosting.

**Los dos «sospechosos» que siempre saltan** son PebbleHost Premium y Vultam
Advanced: comparten `fuente` con su gama hermana y la página solo enseña una sin
pulsar pestaña. No es un fallo de datos.

## Historial de precios (`historico.py`)

Cada `build.py` guarda una foto de los precios en `historico.json` **solo si algo
ha cambiado**. Cuando un hosting se mueve, su ficha lo dice sola:
«📉 Su plan de 8 GB ha subido: el 9 de septiembre costaba 21,28 € y ahora son
21,52 €». Es el historial de precios de idealo, que en hosting no tiene nadie.

`historico.json` **no se publica** (no está en `publicar.py`): es material de
trabajo. La primera foto está fechada el 9-sep porque esos eran los precios
comprobados ese día.

---

## Optimización de consumo (19-sep-2026)

Netlify cobra por **despliegues** (15 créditos) y por **ancho de banda y
peticiones** (20 créditos por GB, 2 por cada 10.000 peticiones), con 300
créditos gratis al mes. Así que cuanto menos pese y menos pida cada visita,
más lejos llegan esos 300. Lo que se ha hecho:

| | Antes | Ahora |
|---|---|---|
| Peticiones de la portada | 9 | **6** |
| Peso comprimido (1.ª visita) | ~66 KB | **~29 KB** |
| Visita repetida | volvía a bajar todo | **solo el HTML (~5 KB)** |
| dist/ entero | 0,5 MB | **0,42 MB** |

Qué se tocó, por orden de lo que más ahorró:

1. **`favicon.ico` de 26 KB → 4 KB** (lo pedía cada visita) y
   `apple-touch-icon.png` de 13 KB → 3 KB, cuantizado a 64 colores.
2. **`hosts.js` publicado sin lo que solo usa Python**: las notas de
   mantenimiento, el campo `fuente` (de revisar_precios.py) y los datos de ping
   (de ping.py). 17,5 KB → 5,8 KB. Lo hace `publicar.py`, el archivo del
   proyecto no se toca.
3. **Minificado al publicar** (`minificar.py`): quita comentarios y sangría de
   css, js y html. Un 23 % menos ya comprimido. Es conservador a propósito: no
   renombra nada ni toca líneas que puedan estar dentro de un texto.
4. **El índice del buscador ya no se carga con la página.** Son 10 KB que casi
   nadie usa; ahora se piden al tocar el buscador (`buscador_ui.js` lo trae
   solo, ya versionado).
5. **Cada página carga solo sus scripts.** `podar_scripts()` en build.py quita
   `tabla_ui.js` de las páginas sin tablas ordenables y `filtros_ui.js` de las
   que no tienen filtros. El pop-up de promo (`promo_ui.js`) solo se incluye si
   hay partner con promo activa.
6. **Caché de un año con `?v=<huella>`.** `versionar()` pone la huella del
   archivo en cada referencia y `_headers` (nuevo, se publica) dice
   `immutable`. Resultado: quien vuelve no se descarga ni el css ni el js. El
   **HTML no se cachea** a propósito: ahí viven los precios.
7. **og-image.jpg** a calidad 82 y progresivo: 81 KB → 57 KB. Y el número de
   hostings que sale en la imagen se lee de hosts.js, para que no envejezca.
8. Space Grotesk se pide con **un solo peso** (700) en vez de tres.

**Cómo comprobar que el dist minificado no está roto** (por si se toca el
minificador): se sirve `dist/` y se mira que la calculadora pinte las barras y
la tabla. Hay una configuración `dist` en `.claude/launch.json` para eso.

---

## Más hostings y fuera los modelos raros (20-sep-2026)

Él lo dijo claro: **"quiero solo los normales, los típicos hostings, no cosas
raras"**. Así que:

**Fuera:**
- **exaroton** (cobraba por hora encendida) y con él el **paso de «cuántas horas
  al día»** de la calculadora, que existía solo por ellos. Menos código y un
  paso menos que responder.
- **Aternos y Minehut**, que llegué a meter por ser gratis: no son hostings
  normales y se fueron con el modelo `gratis` entero.

**Dentro, con precios comprobados a mano el 20-sep:**

| Hosting | Precio | Detalle |
|---|---|---|
| **Kinetic Hosting** | 0,99 $/GB | 8 GB por 7,99 $. Copias incluidas, devolución 7 días. **Empieza en 4 GB** |
| **GPORTAL** | 5,40 / 11,80 / 15 € | 2, 4 y 6 GB. Plazas ilimitadas, 250 modpacks. **Su tope son 6 GB**. −25 % solo el primer periodo |
| **ScalaCube** | ~3 $/GB | De 768 MB a **64 GB**. −50 % solo el primer mes |
| **GGServers** | 3 $/GB | Standard (DDR4 2133, SSD). Cupón TAKE20 de la primera factura |
| **GGServers Premium** | 6 $/GB | CPU 4,4-5 GHz y NVMe. El doble de precio |

GPORTAL volvió: se había quedado fuera al pasar la web a solo Minecraft porque
solo teníamos sus precios de Palworld, Rust y Valheim. **Sí vende Minecraft.**

**Comprobados y descartados:**
- **MCProHosting** ya es Apex Hosting (se fusionaron): sería la misma ficha dos veces.
- **Bloom.Host** no publica su escala de precios, solo el precio de un plan por
  gama (Essentials 12 $/4 GB, Performance 22 $/8 GB). Sin la tabla no se puede
  comparar por tamaño.
- **Nitrado** tenía la web caída ese día (error en todas sus URLs de Minecraft).

**Siguientes candidatos** para cuando toque otra tanda: Nitrado, ZAP-Hosting,
MelonCube, Fluctis, Skynode, Server.pro.

---

## Godlike.host como partner (21-sep-2026) — va a firmar con ellos

Leída entera su web (portada de Minecraft, FAQ, página del panel y «Sobre
nosotros»). **Puntos fuertes comprobados:**

- **El plan te lo montas tú**: gigas (2-33), plazas (5-200) y **días** (30, 90,
  180, 360; −10/−15/−20 % por adelantado). Nadie más deja elegir la duración.
- **Hardware**: AMD Ryzen de última generación, **hasta el 9950X3D**, y EPYC, con
  NVMe. Hardware propio en regiones clave.
- **Hasta 3 copias de seguridad al día gratis**, restaurables desde el panel.
- **Prueba gratis de un día** (2 GB). Su plan gratis permanente es de una plaza y
  hay que renovarlo cada 3 h: sirve para trastear, no para jugar.
- **Panel renovado en 2025**: consola con filtro de errores, reinicios y copias
  programadas, editor con resaltado, config de Minecraft en una pantalla sin SFTP,
  permisos por roles, asistente de configuración e instalador de mods/plugins que
  comprueba versiones. Va bien en móvil y se maneja también por **bot de Discord**.
- Para comunidades: **tienda in-game** en un clic, sistema de valoraciones para
  atraer jugadores y varios servidores enlazados.
- Subir o bajar de plan al momento con prorrateo.
- DDoS por capas con **Path.net**, **10 centros de datos** (Europa incluida), pago
  con casi cualquier método (cripto incluida).
- Reseñas: 4,9/5 en su web (78) y 4,5/5 en más de 300.

**Pegas que la web sigue diciendo** (si no, pierde credibilidad y deja de vender):
tarifa de 3,19 €/GB; el −75 % y el «1 $/GB» de su cartel son solo la primera
compra; empresa de 2021 con una queja de reembolso en 2024 que ellos mismos
explican en su web.

**Qué se ha hecho en la web:**
- **Ficha reescrita** con 8 puntos fuertes y 4 pegas. Corregidos dos errores
  míos: fundaron en **2021** (no 2019) y **sí publican procesador**. También lo
  del panel: es un Pterodactyl personalizado, no uno propio.
- **La comparativa tiene un caso donde Godlike gana**: «Si es un servidor de
  temporada» → Godlike (elige días, prueba gratis, copias, CPU). Los demás casos
  se rehicieron con los hostings nuevos (Kinetic, ScalaCube).
- **Los dos cara a cara** reescritos: el de DatHost decía que DatHost tenía mejor
  procesador, y con el 9950X3D ya no es verdad.
- **`partner.razones` en hosts.js**: tres líneas de «por qué Godlike» que salen
  junto al botón en la calculadora y en su ficha **solo cuando el partner está
  activo**.
- La oferta del −75 % sigue marcada «con truco», con un consejo que dice dónde
  sí vale la pena: el servidor de temporada.

**Lo que NO se ha tocado, a propósito:** el orden de las tablas. Godlike sigue en
su puesto por precio (17 de 19 en /hosting/). Subirlo sería justo lo que la web
critica, y el día que alguien lo pille se acaba la credibilidad que es lo que
vende. Si se quiere cambiar, es decisión suya.

**Para activarlo:** `hosts.js → partner`: `enlace` (su URL de afiliado),
`codigo` y `descuento`, `activo: true`, y `python build.py` + `publicar.py`.

---

## Publicarla

Dominio comprado en Nominalia el 8-sep-2026: **montatuserver.com** (1 € el primer
año; ojo a la renovación, y se puede transferir a Cloudflare Registrar pasados
60 días, que es el bloqueo de ICANN).

### 1. Prepara los archivos

    python build.py
    python make_og.py
    python publicar.py

Eso deja **`dist/`** con los 31 archivos que se publican y nada más.
Nunca arrastres la carpeta del proyecto entera: `LEEME.md` lleva tus enlaces de
afiliado y tu estrategia, y quedaría colgado en internet.

### 2. Cloudflare (gratis)

1. Cuenta en `dash.cloudflare.com`
2. **Add a site** → `montatuserver.com` → plan **Free** → te da dos nameservers
3. En el panel de Nominalia, cambia los DNS por esos dos
4. **Workers & Pages → Create → Pages → Upload assets** → arrastra el
   **contenido** de `dist/`, no la carpeta
5. Cuando propague el DNS: **Custom domains** → añade `montatuserver.com`

El paso 4 ya te deja la web viva en una URL `.pages.dev` aunque el DNS no haya
propagado. Sirve para enseñarla mientras tanto.

### 3. Actualizarla después

Repites los tres comandos y vuelves a subir `dist/`. Nada más.

---

## Verla en local

```bash
python -m http.server 4173 --directory "E:/PROYECTOS/comparador-hosting"
```

Y abres `http://localhost:4173`.

---

## De dónde salen los números

**RAM:** requisitos oficiales de cada juego cruzados con consumo real observado.
Son recomendaciones con margen, no mínimos absolutos. Las tablas están en `app.js`,
en el array `GAMES`, con el formato `[hasta X jugadores, GB base]`. Si un dato te
parece mal por experiencia propia, cámbialo: tú has montado más servidores que la
mayoría de webs que salen en Google.

**Precios:** comprobados a mano el 7-sep-2026.

Todos están en `HOSTS`, en `app.js`. **Añadir un hosting nuevo es meter un objeto ahí**
y aparece solo en el gráfico y en la tabla.

### Minecraft (11) — todos recurrentes, sin ganchos de primer mes

| Hosting | Modelo | Precio |
|---|---|---|
| DatHost | plano | 16 GB por 14,90 €/mes · **6,90 €/mes en anual** |
| PebbleHost Budget | por GB | 1,00 $/GB — hardware modesto |
| Sparked Host | por GB | 2,59 $/GB — Ryzen 9 7900 DDR5 |
| PebbleHost Premium | por GB | 2,25 $/GB — Ryzen 9 9900X |
| BisectHosting | por GB | 2,66 €/GB, lineal clavado |
| Shockbyte | tabla | 2,79 $/GB … 47,48 $ los 17 GB+ |
| Sparked Host Extreme | por GB | 4,00 $/GB — su gama alta |
| Apex Hosting | tabla | 4/6/8/16 GB → 14,99 / 22,49 / 27,99 / **71,99 $** |
| Hostinger | tabla | Renovación: 4/8/16/32 GB → 11,99 / 14,99 / 28,99 / 49,99 $ |
| Nodecraft Budget | tabla | 2/4/8 GB → 5,98 / 11,98 / 23,48 € — **se apaga si no juega nadie** |
| Nodecraft Premium | tabla | 2/4/8 GB → 9,98 / 19,98 / 39,98 € — 24/7 e IP fija |

### Trampas encontradas (material para vídeos)

- **Hostinger**: anuncia 13,99 $ los 16 GB pero exige **24 meses por adelantado**
  (335 $ de golpe) y luego renueva a 28,99 $. El doble de lo que enseña.
- **Apex**: su 25 % de descuento es **solo del primer mes**.
- **Nodecraft Budget**: es más barato porque **se apaga cuando no juega nadie**.
  No es un servidor 24/7 y no lo dicen en grande.
- **MCProHosting se ha fusionado con Apex Hosting** (visto el 8-sep-2026).
- **GPORTAL y Nitrado** venden slots sin publicar la RAM.
- Caídos al consultarlos: ScalaCube (error 522) y Nitrado.

Cambio usado: **1 $ = 0,860 €** (7-sep-2026, contrastado en frankfurter y er-api).
Está en `CAMBIO_USD_EUR`.

### Por qué el gráfico dice "te da X GB"
Sin ese dato la comparación **engañaba en contra tuya**: enseñaba 2,58 € (3 GB de
PebbleHost) al lado de 14,90 € (16 GB de DatHost) como si fuera lo mismo. Ahora cada
barra dice lo que recibes, y cuando pides 16 GB el plan anual de DatHost gana por
6 veces al siguiente. No lo quites.

### El 30 % es solo del primer mes (confirmado 8-sep-2026)
Por eso la web **nunca** anuncia 10,43 € como precio permanente. El 30 % se
presenta como lo que es —una entrada más barata— y el precio que se destaca es
**6,90 €/mes contratando el año**, que es el único número bueno y además cierto.

Ojo con esto al escribir guiones y descripciones: decir "16 GB por 10 €" en un
vídeo es mentira a los 30 días, y esos comentarios no se borran. Lo correcto es
"el primer mes te sale un 30 % más barato" o directamente ir con el anual.

⚠️ **Revísalos cada 2-3 meses.** Una tabla de precios desfasada se nota y te hunde
la credibilidad, que es justo lo único que tienes que vender aquí.

---

## Por qué la web dice cosas que no me convienen

Está hecho aposta y es la parte importante:

- Si necesitas **menos de 4 GB**, te dice que un plan pequeño de otro sitio sale
  más barato a la larga.
- Si necesitas **más de 16 GB**, te dice que DatHost no te vale y que busques
  un dedicado, y el botón cambia de "móntalo por 1 €" a "ver qué me ofrece".
- El aviso de afiliación está en el resultado y en el pie.

Eso es lo que separa un comparador que la gente enlaza y comparte de una landing
de afiliado más. Si lo quitas conviertes más hoy y pierdes el negocio a los 6 meses.

---

## Resultados compartibles

El estado va en la URL: `montatuserver.com/minecraft/?p=30&m=heavy&e=16` abre la
calculadora con 30 jugadores, modpack grande y render 16 ya puestos. Hay un botón
**"Copiar este resultado para mandarlo al grupo"** debajo del resultado.

Es el motor de difusión de la web: alguien calcula, lo pega en su Discord, y los
otros cinco del grupo entran con el resultado ya hecho. Un enlace a la portada
pelada no habría convertido a ninguno.

## Analítica (pendiente de tu token)

En `index.html`, al final, está el snippet de **Cloudflare Web Analytics** comentado.
Es gratis, sin cookies y por tanto **sin banner de cookies** (Google Analytics te
obligaría a ponerlo). Sacas el token en el mismo panel donde despliegas:
`Analytics & Logs → Web Analytics → Add a site`. Lo pegas, quitas los comentarios
y ejecutas `python build.py` para que entre en las 11 páginas.

Lo necesitas para saber **qué juego busca la gente**: eso te dice qué vídeo grabar
y qué guía escribir, que es medio negocio.

## Guías paso a paso

Hay dos, las dos con schema `HowTo` + `FAQPage` para optar a resultados
enriquecidos en Google:

- **`/minecraft/como-montar-un-servidor/`** — 1.214 palabras
- **`/valheim/como-montar-un-servidor/`** — 1.251 palabras, centrada en el
  crossplay con consolas y en no perder el mundo al migrarlo

Cuelgan de la página del juego a propósito: Google entiende que `/minecraft/` y
`/minecraft/como-montar-un-servidor/` hablan de lo mismo y le da autoridad al
conjunto. Sueltas en `/guias/` se quedarían huérfanas.

**Para añadir otra**, abre `guias.py` y copia un bloque entero cambiando
`juego`, `url`, `title`, `desc`, `h1`, `resumen`, `sub`, `secciones` y `faq`.
El campo `resumen` es el texto de la tarjeta que aparece en la calculadora de ese
juego. Ejecuta `python build.py` y solo:
se genera la página, se enlaza desde la calculadora de ese juego y entra en el
sitemap. No hay que tocar nada más.

Por dónde seguir, por volumen de búsqueda: **Palworld**, **ARK** y
**Project Zomboid**.

Escríbelas como la de Minecraft: contando lo que sabes por haber montado
servidores, no repitiendo lo que pone en la wiki. Eso es literalmente lo único
que no te puede copiar una web generada con IA.

## Páginas de comparativa

**`/minecraft/mejor-hosting/`** — 8 hostings con tabla estática (no la pinta
JavaScript: el valor de la página es la tabla, así que tiene que estar en el
código fuente para que Google la vea seguro). Ataca las búsquedas con intención
de compra, que son las que más convierten.

Para añadir otra (Valheim, Palworld…), copia el bloque en `comparativas.py`.

## ⚠️ Los precios viven en UN SOLO SITIO: `hosts.js`

Antes estaban solo en `app.js` y la comparativa los necesitaba desde Python.
Escribirlos dos veces era garantía de que un día uno se quedara viejo.

Ahora `hosts.js` es la fuente única: lo lee la calculadora (JavaScript) **y**
lo lee `build.py` (Python) para generar las tablas.

**Para actualizar precios:** cambias los números en `hosts.js`, cambias la fecha
de `"comprobado"`, y ejecutas `python build.py`. Ya está en toda la web.

Está escrito como JSON puro después del `=` para que Python pueda leerlo. **No
metas comentarios ni comas de más dentro del objeto** o Python dejará de leerlo.

## El diseño y de dónde sale

El hero va a **dos columnas**: mensaje a la izquierda y una tarjeta de resultado
REAL a la derecha. Está copiado de GameServerCheck, el mejor comparador del
sector: enseñan un precio antes de que toques nada, y eso es lo que busca quien
entra. La tarjeta la rellena `pintarHeroDemo()` en `app.js` con el mismo motor
que la calculadora, así que **si cambian los precios cambia sola** y nunca se
queda mintiendo en la portada.

En las páginas de juego el hero es de una columna (`.hero-solo`): quien llega ahí
ya sabe a qué viene, y la calculadora está justo debajo.

Las fichas `/hosting/<nombre>/` son la segunda puerta de entrada, que también
tienen GameServerCheck y CompareGameHosting. Lo que ellos NO tienen es la tabla
de **lo que cobra un mismo hosting en cada juego**: eso es dato propio y solo lo
tienes por haber entrado juego por juego.

## El buscador de la cabecera

Está en todas las páginas. Se escribe, salen resultados, Enter entra.
Las flechas mueven, Escape cierra y la tecla **`/`** enfoca el buscador desde
cualquier sitio (como en GitHub).

**Su índice se genera solo.** `build.py` recorre todas las carpetas al final,
lee el `<title>` y la descripción de cada `index.html` y escribe `indice.js`.
Cada página nueva aparece en el buscador sin que tengas que apuntarla en
ningún sitio — que es justo lo que hace que estas cosas no se pudran.

Busca **sin acentos**: escribir "cuanta ram" encuentra "¿Cuánta RAM…". En una
web en español eso no es opcional, la gente no escribe tildes en un buscador.

## Lo siguiente (por orden de impacto)

Ya hechos: página por juego, comparativa visual con 8 hosts, resultados
compartibles, imágenes al compartir, 404 propio, bloque de "quién hay detrás",
dos guías (Minecraft y Valheim) y la comparativa de Minecraft.

1. **Más comparativas** — Valheim, Palworld. Son las que más convierten.
2. **Más guías** — Palworld, ARK, Project Zomboid.
3. **Más hosts** — Nitrado (su web daba error), Sparked, ScalaCube.
4. **Revisar precios cada 2-3 meses** en `hosts.js`. Ponte un recordatorio.

## Promos con fecha (añadido 8-sep-2026)

La oferta vive en un solo sitio, `hosts.js`:

```js
"promo": { "juegos": ["valheim"], "precio": 1.00, "hasta": "2026-09-17" }
```

De ahí salen tres cosas, y ninguna hay que tocarla a mano:

- **`promo_ui.js`** — el pop-up de la calculadora del juego. Sale a los 1,2 s,
  se cierra con la X, Escape o pulsando fuera, y si lo cierras no vuelve.
- **`promo.py`** — la tira dentro de los artículos (`comparativas.py` y
  `guias.py`). Se genera en HTML estático, así que Google la ve. El número de
  rivales y su precio de partida se calculan desde `hosts.js`: si añades un
  hosting, el texto se corrige solo.
- **Caducidad doble.** Al generar, si la fecha pasó no se escribe. Y aunque no
  vuelvas a generar el sitio, un script diminuto la borra en el navegador.
  Anunciar una oferta muerta sería justo lo que esta web critica.

Cada sitio lleva su propio `cid=` (`POPUP`, `BANNER-COMP`, `BANNER-GUIA`), así
que en el panel de DatHost se ve cuál de los tres vende.

## Acabado visual (8-sep-2026)

Tres cosas nativas del navegador, sin librerías ni peticiones extra:

- **View Transitions** (`@view-transition { navigation: auto }`): al cambiar de
  página se funde en vez de parpadear. Con 46 páginas estáticas es lo que más
  cambia la sensación de calidad.
- **Animaciones ligadas al scroll** (`animation-timeline: view()`): las tarjetas
  asoman al entrar en pantalla. Cero JavaScript.
- **Grano** sobre el fondo, con SVG incrustado. Es lo que evita que un degradado
  oscuro parezca plástico.

Todo se apaga con `prefers-reduced-motion`.

⚠️ La lista de precios enseña **6 hostings** y el resto tras un botón. Con 20 en
pantalla nadie compara: se scrollea y se rinde.

## Revisor de precios (`revisar_precios.py`)

    python revisar_precios.py            # todas las entradas de precio
    python revisar_precios.py valheim    # solo un juego

Entra en la página de cada hosting (campo `fuente` de hosts.js), saca los
números con pinta de precio y te dice **solo lo que ya no cuadra**. Convierte
una tarde de revisar en dos minutos.

Tres cosas que hay que entender de él:

- **No toca `hosts.js`.** Los precios se cambian a mano después de mirarlos,
  porque un número mal leído se publica en 46 páginas de golpe.
- **Avisa de lo que no puede leer.** Muchas de estas webs pintan el precio con
  JavaScript y en el HTML crudo no está. Cuando no encuentra nada lo dice y te
  manda el enlace, en vez de callarse y dar el precio por bueno. Un revisor que
  da falsos «todo correcto» es peor que no tener revisor.
- **Tolera dos céntimos.** Quien cobra por giga casi siempre remata en ,99
  (16 GB a 19,99 y no a 20,00). Sin ese margen gritaba en cada hosting por GB
  y habrías acabado ignorándolo.

**Límite conocido:** los hostings con varias gamas en la misma página
(PebbleHost Premium, Vultam Advanced) comparten `fuente` con su gama hermana, y
la página solo enseña una sin pulsar una pestaña. Salen como sospechosos
siempre. Hay que mirarlos a mano o darles una URL propia.

**Después de cambiar un precio:** actualiza también `"comprobado"` en hosts.js
con la fecha de hoy y ejecuta `build.py`.

## Partner de afiliación — cómo se enchufa (desde el 15-sep-2026)

**Contexto:** la relación con DatHost terminó el 11-sep-2026. Hasta entonces la
web estaba cableada a DatHost en catorce ficheros. Ahora DatHost es un hosting
más dentro de `hosts[]`, y todo lo que dependa de con quién hay acuerdo sale de
**un solo bloque**: `partner` en `hosts.js`.

### Estado actual: sin partner

    "partner": { "activo": false, "hostId": null, "enlace": null, … }

Con esto la web no tiene ningún enlace de afiliado, ningún botón de contratar,
ningún hosting resaltado, ningún pop-up, y todos los avisos dicen la verdad:
«ahora mismo no gano comisión con ningún hosting de esta web».

### Para activar un partner (cuando cierres el acuerdo)

1. Asegúrate de que ese hosting está en `hosts[]` con sus precios comprobados.
   **El precio no se repite en el bloque partner**: sale de su entrada en
   `hosts[]`, así nunca puede haber dos precios distintos del mismo hosting.
2. Rellena el bloque:

       "partner": {
         "activo": true,
         "hostId": "pebble-budget",
         "enlace": "https://…tu-enlace-de-afiliado…",
         "slugs": {},
         "codigo": "DOUBLELAG",
         "descuento": "−15 % el primer mes",
         "canal": "WEB",
         "promo": null
       }

   Si el enlace cambia por juego, pon `{juego}` dentro de la URL y, si el
   hosting usa otro nombre para ese juego, añádelo en `slugs`
   (`"zomboid": "projectzomboid"`).
3. `python build.py` y subir `dist/`.

Nada más. No hay que tocar ningún texto.

### Lo que pasa al activarlo (comprobado con un partner de ensayo)

- Botón «Montar mi servidor de X en {partner}» bajo el resultado, solo en los
  juegos que ese hosting vende. En los que no vende, no hay botón.
- Su barra y su fila salen resaltadas, **pero en el puesto que les toca por
  precio**. No suben ni una posición.
- **El veredicto sigue nombrando al más barato, sea quien sea.** Probado con
  WiseHosting de partner: el veredicto decía PebbleHost.
- Avisos de afiliación en el pie, en «Qué gano yo» y en su ficha, con su nombre.
- Si hay `promo` (con `letra` obligatoria), tira en comparativas y guías y
  pop-up en la calculadora de ese juego. Caducan solas.
- La etiqueta de canal (`?cid=YT`) viaja hasta su enlace igual que antes.

### Consecuencia comercial de ser neutral

Como el partner no sube en las tablas, **un partner caro queda enterrado**:
WiseHosting sale en la zona de «ver los otros 14» y solo lo promociona el botón.
Un partner que de verdad sea de los más baratos sale arriba por mérito propio y
además lleva el botón. Tenlo en cuenta al elegir.

### Precios: ahora todos mes a mes

Antes a DatHost se le enseñaba el **precio anual** (6,90 €) y al resto el
mensual, lo que le hacía parecer más barato de lo que era. Ahora todos van mes
a mes, y los precios anuales se mencionan en la nota de cada uno. Con eso, en
Minecraft **PebbleHost Budget es el más barato en todos los tamaños** y DatHost
queda segundo a 16 GB (14,90 € frente a 13,76 €).
