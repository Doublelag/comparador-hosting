# MontaTuServer

**¿Cuánta RAM necesita tu servidor de Minecraft y cuánto te va a costar en cada hosting?**
MontaTuServer responde a eso en segundos: una calculadora de RAM y un comparador
independiente de hosting con los precios comprobados a mano.

🌐 **[montatuserver.com](https://montatuserver.com)** · Hecho por
[Doublelag](https://www.youtube.com/@Doublelag)

> 📸 CAPTURA AQUÍ — portada con la calculadora de RAM y el gráfico de precios

![Comprobar el sitio](https://github.com/doublelag/comparador-hosting/actions/workflows/comprobar.yml/badge.svg)

---

## Qué hace

- **Calculadora de RAM.** Dice los GB que necesita un servidor según jugadores,
  mods y cuánto tiempo va a estar encendido, y lo que costaría en cada hosting.
- **Comparador de 25 hostings** con precios comprobados a mano, precio por
  gigabyte y la letra pequeña de cada uno (descuentos de entrada aparte, con su
  nombre).
- **Ficha de cada hosting** con sus datos técnicos, para qué tipo de servidor
  es ideal y su historial de precios.
- **Versus**: cara a cara entre dos hostings con marcador y veredicto.
- **Plantillas de servidor**: un `.zip` ya configurado que el propio navegador
  monta descargando los plugins de su web oficial, y fichas de los modpacks más
  jugados con la RAM que piden de verdad.
- **Ofertas y cupones**, guías paso a paso y un buscador interno.
- **Estado en directo de ChorizoSMP** (el servidor del canal) a través de un
  Worker de Cloudflare.
- Todo en **español e inglés**, con tema oscuro y claro.

> 📸 CAPTURA AQUÍ — tabla del comparador / página de Versus

## Tecnología

- **Web estática sin framework** y sin dependencias de JavaScript: HTML, CSS y
  JS escritos a mano.
- **Python** para generar las ~100 páginas (`build.py` y los módulos de cada
  sección), el sitemap, el índice del buscador y las imágenes para redes
  (Pillow).
- **Cloudflare Workers** con archivos estáticos para servir la web, más una
  pequeña API (`/api/server`) en `worker.js`.
- Fuentes autoalojadas, CSS/JS versionados con huella (`?v=…`) para poder
  cachearlos un año, y minificado al publicar.

## Probarlo en local

Hace falta Python 3 (y Pillow para generar las páginas).

```bash
pip install -r requirements.txt

# 1. Generar todas las páginas a partir de hosts.js y los textos
python build.py

# 2. Servir la carpeta y abrir http://localhost:4173
python -m http.server 4173
```

Para ver exactamente lo que se publicaría (minificado, sin los `.py` ni los
documentos internos):

```bash
python subir.py --local          # build.py + publicar.py → deja dist/ listo
python -m http.server 4174 --directory dist
```

La API del Worker (`/api/server`) no existe con `http.server`, así que en
local el estado del servidor sale como «no se ha podido comprobar» (y verás un
404 en la consola por esa petición; es lo esperado).

> Nota: el historial de precios se guarda en `historico.json`, que es local y
> no está en el repositorio. Si generas la web en un clon nuevo, la página
> `/precios/` sale sin cambios apuntados.

### Comprobaciones

```bash
python comprobar.py
```

Revisa, sin red y solo con la biblioteca estándar, que:

- todos los enlaces internos (`href`, `src`, `url(...)`) apuntan a algo que
  existe o a una redirección de `_redirects`, y que ese destino se publica;
- cada `.css`/`.js` publicado tiene su entrada de caché en `_headers`;
- `hosts.js` se lee como JSON y cada hosting tiene precios y RAM positivos;
- todos los `.js` pasan `node --check` (si hay Node instalado).

Lo mismo se ejecuta en **GitHub Actions** (`.github/workflows/comprobar.yml`)
en cada push y pull request: primero sobre lo que hay en el repositorio y luego
tras generar la web desde cero con `build.py` (sin publicar nada).

## Despliegue en Cloudflare

La web vive en **Cloudflare Workers con archivos estáticos**
(`wrangler.jsonc`):

- Solo se sube la carpeta **`dist/`**, nunca la raíz del proyecto, para que no
  se publiquen los `.py` ni las notas internas.
- `worker.js` atiende `/api/server` (estado de ChorizoSMP, consultado desde el
  Worker y cacheado 60 s para no mandar la IP del visitante a terceros) y deja
  todo lo demás a los estáticos.
- `_redirects` mantiene vivas las URLs antiguas con 301 y `_headers` fija la
  caché de cada archivo.
- El dominio `montatuserver.com` (y `www`) va como *custom domain* del Worker.

Publicar es un solo comando (o doble clic en `SUBIR.bat` en Windows):

```bash
python subir.py
```

Que hace, en orden: `build.py` → `publicar.py` (prepara y minifica `dist/`) →
`wrangler deploy` → y una ronda de comprobaciones contra el dominio real (las
páginas clave dan 200, las redirecciones 301 y los archivos internos 404). Si
algo falla por el camino, para y no sube nada. Necesita
[wrangler](https://developers.cloudflare.com/workers/wrangler/) instalado y con
sesión iniciada (`npm i -g wrangler` y `wrangler login`); no hay claves ni
tokens en el repositorio.

## Estructura del proyecto

| Archivo / carpeta | Para qué |
|---|---|
| `hosts.js` | La única fuente de verdad: precios, modelos de cobro y el partner |
| `build.py` | Genera todas las páginas, el sitemap y el índice del buscador |
| `marco.py` | Cabecera, pie y cambio de idioma, iguales en todas las páginas |
| `hostings.py`, `duelos.py`, `comparativas.py`, `ofertas.py`, `plantillas.py`, `modpacks.py`, `guias.py`, `seo.py`, `paginas.py` | Cada sección (y sus `*_en.py` en inglés) |
| `sitio.py`, `partner.py`, `videos.py` | Datos compartidos: servidor, redes, datos legales, afiliación y vídeos del canal |
| `og.py`, `make_og.py`, `favicon.py` | Imágenes para redes sociales e iconos |
| `publicar.py`, `minificar.py` | Dejan en `dist/` solo lo publicable, minificado |
| `subir.py`, `SUBIR.bat` | Publican en Cloudflare y comprueban la web ya publicada |
| `revisar_precios.py`, `revisar_auto.py` | Avisan de precios que ya no aparecen en la web de cada hosting (no los cambian solos) |
| `comprobar.py` | Comprobaciones del sitio (también en CI) |
| `app.js` | La calculadora, sin librerías |
| `*_ui.js` | Buscador, tablas ordenables, filtros, plantillas, `.zip` en el navegador, animaciones… |
| `worker.js`, `wrangler.jsonc`, `_headers`, `_redirects` | Despliegue en Cloudflare |
| `hosting/`, `versus/`, `ofertas/`, `plantillas/`, `minecraft/`, `en/`… | Páginas ya generadas (se versionan tal cual se publican) |
| `_retirado_*.py` | Código de secciones retiradas (la página de ping), guardado como referencia; no lo usa el build |

Cada archivo lleva arriba del todo la explicación de sus decisiones y de las
trampas conocidas.

## Principios

- **Los precios se comprueban a mano**, con la fecha puesta. Si un dato no está
  publicado, se dice; no se rellena a ojo.
- **El precio que manda es el recurrente.** Los descuentos de entrada van
  aparte y con su nombre.
- **Las tablas se ordenan por precio.** Si hay partner de afiliación, sale
  donde le toca, no más arriba, y se avisa en el pie de cada página.

## Cómo se hizo

MontaTuServer lo he construido con ayuda de IA, en lo que se suele llamar
*vibe coding*: yo pongo la idea, el criterio, los textos y la comprobación de
cada precio, y el código se ha escrito en conversación con
[Claude Code](https://claude.com/claude-code), el asistente de programación de
Anthropic. Eso explica también el estilo del proyecto: cada archivo documenta
el porqué de sus decisiones, para que tanto una persona como la IA puedan
retomarlo sin perderse.

## Licencia

Código abierto para mirar y aprender. Los textos, los análisis y la marca son
de Doublelag.
