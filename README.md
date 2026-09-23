# MontaTuServer

Comparador independiente de hosting de Minecraft y calculadora de RAM:
**[montatuserver.com](https://montatuserver.com)**

Web estática, sin framework y sin dependencias de JavaScript: se genera con
Python y se publica en Cloudflare Workers. Hecha por
[Doublelag](https://www.youtube.com/@Doublelag).

    python subir.py          # genera, prepara dist/ y publica (o doble clic en SUBIR.bat)
    python subir.py --local  # lo mismo pero sin publicar, para mirarlo antes

## Qué hace

- **Calculadora de RAM.** Dice los GB que necesita un servidor según jugadores,
  mods y cuánto tiempo va a estar encendido, y lo que costaría en cada hosting.
- **Comparador de 23 hostings** con precios comprobados a mano, precio por
  gigabyte y la letra pequeña de cada uno.
- **Versus**, cara a cara entre dos hostings con marcador y veredicto.
- **Plantillas de servidor**: un .zip ya configurado que el navegador monta
  descargando los plugins de su web oficial, y fichas de los modpacks más
  jugados con la RAM que piden de verdad.
- Todo en **español e inglés**, con tema oscuro y claro.

## Cómo está montado

| Archivo | Para qué |
|---|---|
| `hosts.js` | La única fuente de verdad: precios, modelos de cobro y el partner |
| `build.py` | Genera las ~96 páginas, el sitemap y el índice del buscador |
| `marco.py` | Cabecera, pie y cambio de idioma, iguales en todas las páginas |
| `hostings.py`, `duelos.py`, `plantillas.py`, `modpacks.py`… | Cada sección |
| `publicar.py` | Deja en `dist/` solo lo publicable y minifica |
| `subir.py` | Publica en Cloudflare y comprueba la web ya publicada |
| `app.js` | La calculadora, sin librerías |
| `zip_ui.js` | Un .zip hecho en el navegador, sin dependencias |

Detalles de decisiones y trampas conocidas: cada archivo lleva su explicación
arriba del todo.

## Principios

- **Los precios se comprueban a mano**, con la fecha puesta. Si un dato no está
  publicado, se dice; no se rellena a ojo.
- **El precio que manda es el recurrente.** Los descuentos de entrada van
  aparte y con su nombre.
- **Las tablas se ordenan por precio.** El partner de afiliación sale donde le
  toca, no más arriba, y se avisa en el pie de cada página.

## Licencia

Código abierto para mirar y aprender. Los textos, los análisis y la marca son
de Doublelag.
