# -*- coding: utf-8 -*-
"""
Guías paso a paso: /minecraft/como-montar-un-servidor/ y compañía.

Van colgando de la página del juego a propósito. Google entiende que
/minecraft/ y /minecraft/como-montar-un-servidor/ hablan de lo mismo y le da
autoridad al conjunto; sueltas en /guias/ se quedarían huérfanas.

Este módulo lo importa build.py. No se ejecuta solo.
"""

import migas
import promo
import partner

DOMINIO = "https://montatuserver.com"

# ---------------------------------------------------------------------------
# CONTENIDO
# Cada sección es (titulo, html). Escribe como hablas: esto lo lee gente
# agobiada que quiere jugar con sus amigos, no un tribunal.
# ---------------------------------------------------------------------------

GUIAS = [
  dict(
    juego="minecraft", juego_nombre="Minecraft",
    url="como-montar-un-servidor",
    title="Cómo montar un servidor de Minecraft en 2026 (guía paso a paso)",
    desc="Guía real para montar un servidor de Minecraft: cuánta RAM necesitas, qué software elegir, cómo meter a los de consola con crossplay y los errores que arruinan un servidor.",
    h1="Cómo montar un servidor de Minecraft",
    resumen="qué software elegir, crossplay con consolas, los plugins que valen la pena y los errores que arruinan un servidor",
    sub="Sin rodeos y sin vender humo. Esto es lo que hago yo cuando monto uno.",
    minutos=9,
    secciones=[
      ("Primero lo importante: ¿tu PC o alquilado?", """
        <p>
          Puedes montarlo en tu propio ordenador y no pagar nada. Funciona, y para
          jugar una tarde suelta con dos amigos está bien. Pero tiene tres pegas que
          nadie te cuenta hasta que las sufres:
        </p>
        <ul>
          <li><strong>Tu PC tiene que estar encendido siempre.</strong> Si lo apagas
              para dormir, tus amigos no juegan. Y si juegas tú en el mismo equipo,
              el servidor y el juego se pelean por el procesador.</li>
          <li><strong>Hay que abrir puertos en el router.</strong> Con suerte es un
              rato; con CG-NAT de tu operadora, directamente no puedes.</li>
          <li><strong>Tu subida de internet es la que es.</strong> Bajas 600 megas
              pero subes 40, y lo que importa para un servidor es la subida. Por eso
              tus amigos van a tirones aunque a ti te vaya perfecto.</li>
        </ul>
        <p>
          Resumen honesto: para probar, tu PC. Para una partida que dure meses y con
          gente que no vive en tu casa, alquilado. Y si alguien de tu grupo va en
          consola, alquilar es <em>la única</em> opción.
        </p>
      """),
      ("Paso 1 — Averigua cuánta RAM necesitas", """
        <p>
          Es el paso que casi todo el mundo se salta, y luego paga de más o se queda
          corto. La regla que te van a repetir por ahí —"1 GB por cada 10 jugadores"—
          <strong>es falsa en cuanto instalas algo</strong>.
        </p>
        <p>
          Lo que de verdad manda: un modpack de 200 mods con 5 amigos pide más RAM
          que un servidor vanilla con 40 personas. Los mods se cargan en memoria estén
          jugando dos o veinte.
        </p>
        <p class="cta-inline">
          <a href="/#calculadora">Calcula tus GB exactos aquí</a> — tarda 20 segundos y
          te dice también lo que cuesta en cada hosting.
        </p>
      """),
      ("Paso 2 — Elige el software (y no, no es vanilla)", """
        <p>Cuando crees el servidor te van a pedir elegir tipo. Traducido:</p>
        <ul>
          <li><strong>Paper</strong> — es lo que quieres el 90 % de las veces. Es
              Minecraft normal pero <em>mucho</em> más optimizado, admite plugins y
              arregla fallos que el servidor oficial arrastra. Los jugadores no
              necesitan instalar nada.</li>
          <li><strong>Vanilla</strong> — el oficial de Mojang. Va peor con la misma
              RAM y no admite plugins. No hay razón para elegirlo.</li>
          <li><strong>Fabric o NeoForge</strong> — solo si vas a jugar con
              <em>mods</em> de verdad. Ojo: aquí <strong>todos</strong> tenéis que
              instalar exactamente los mismos mods para poder entrar.</li>
        </ul>
        <p>
          La diferencia clave: <strong>plugins</strong> (Paper) los instalas solo tú
          en el servidor y nadie más toca nada. <strong>Mods</strong> (Fabric/Forge)
          los tenéis que instalar todos. Si tu grupo es de los que se quejan de
          instalar cosas, Paper y a correr.
        </p>
      """),
      ("Paso 3 — Que entren los de consola y móvil (crossplay)", """
        <p>
          Aquí está el lío que más preguntas genera. Minecraft son en realidad dos
          juegos: <strong>Java</strong> (PC) y <strong>Bedrock</strong> (consolas,
          móvil y Windows 10/11 de la Store). Por defecto no se ven entre ellos.
        </p>
        <p>La solución son dos plugins, y funciona de verdad:</p>
        <ul>
          <li><strong>Geyser</strong> — hace que un servidor de Java acepte a los de
              Bedrock traduciendo la conexión al vuelo.</li>
          <li><strong>Floodgate</strong> — para que además no necesiten cuenta de Java
              para entrar. Sin esto, tu primo con la Switch tendría que comprarse el
              juego otra vez.</li>
        </ul>
        <p>
          Los pones en la carpeta <code>plugins</code>, reinicias, y los de consola
          entran por el <strong>puerto 19132</strong> (el de Bedrock), no por el
          mismo que los de PC. Ese detalle es el que hace que la gente se rinda
          pensando que no funciona.
        </p>
        <p>
          Aviso realista: el crossplay va bien pero no es perfecto. Algunas cosas
          de interfaz y algún plugin muy visual se ven raros en Bedrock. Para jugar
          juntos, sobra.
        </p>
      """),
      ("Paso 4 — Los ajustes que sí hay que tocar", """
        <p>
          El archivo <code>server.properties</code> tiene cincuenta líneas y solo
          importan cuatro:
        </p>
        <ul>
          <li><strong>view-distance</strong> — la que más RAM come. Viene en 10.
              Bájala a <strong>8</strong> y ganas rendimiento sin que casi nadie lo
              note. Subirla a 16 puede dispararte el consumo un 35 %.</li>
          <li><strong>simulation-distance</strong> — a qué distancia siguen pasando
              cosas (bichos, cultivos, granjas). Con 6 vas bien.</li>
          <li><strong>online-mode</strong> — déjalo en <code>true</code>. En
              <code>false</code> cualquiera puede entrar con el nombre que quiera,
              incluido el tuyo de administrador.</li>
          <li><strong>difficulty</strong> — ponlo en <code>normal</code> o
              <code>hard</code> antes de empezar. Cambiarlo con el mundo ya avanzado
              descoloca a todo el mundo.</li>
        </ul>
      """),
      ("Paso 5 — Plugins: los cuatro que valen la pena", """
        <p>
          La tentación es instalar treinta el primer día. No lo hagas: cada plugin es
          una cosa más que puede romper el servidor cuando actualices la versión.
          Con estos cuatro tienes cubierto el 90 %:
        </p>
        <ul>
          <li><strong>EssentialsX</strong> — comandos básicos que deberían venir de
              serie: <code>/home</code>, <code>/tpa</code>, <code>/spawn</code>,
              <code>/msg</code>.</li>
          <li><strong>LuckPerms</strong> — permisos y rangos. En cuanto quieras que
              alguien sea moderador sin darle acceso a todo, lo necesitas.</li>
          <li><strong>CoreProtect</strong> — el seguro de vida. Registra quién puso y
              quitó cada bloque, y deshace destrozos con un comando. El día que
              alguien queme la base, esto te salva la partida.</li>
          <li><strong>Chunky</strong> — genera el mapa por adelantado. Sin él, el
              servidor se atasca cada vez que alguien explora zona nueva.</li>
        </ul>
        <p>
          Y uno que <em>no</em>: cualquier plugin que prometa "optimización mágica" y
          no esté mantenido. Suelen hacer más daño que bien.
        </p>
      """),
      ("Paso 6 — Copias de seguridad y reinicios", """
        <p>
          Esto es lo que separa un servidor que dura un año de uno que muere en tres
          semanas. Dos cosas, las dos automáticas:
        </p>
        <ul>
          <li><strong>Copia de seguridad diaria.</strong> Cualquier hosting decente lo
              hace en dos clics. Un mundo corrupto sin copia es la partida entera a la
              basura, y pasa más de lo que crees.</li>
          <li><strong>Reinicio automático de madrugada.</strong> Limpia la memoria que
              se va acumulando y evita que el servidor vaya cada día un poco peor.
              A las 5 de la mañana no molesta a nadie.</li>
        </ul>
      """),
      ("Los errores que más veo", """
        <ul>
          <li><strong>Calcular la RAM por jugadores y olvidar los mods.</strong> El
              error número uno, con diferencia.</li>
          <li><strong>Dejar la distancia de renderizado en 16 "para que se vea
              bien".</strong> El servidor se arrastra y nadie sabe por qué.</li>
          <li><strong>No poner CoreProtect hasta que pasa algo.</strong> Para entonces
              ya no sirve: solo registra desde que lo instalas.</li>
          <li><strong>Empezar con veinte plugins.</strong> Cuando algo falla no tienes
              ni idea de cuál es.</li>
          <li><strong>Pagar un plan anual sin haberlo probado.</strong> Coge un mes
              primero, mete a tu gente y mira cómo va. Luego ya decides.</li>
        </ul>
      """),
    ],
    faq=[
      ("¿Cuánta RAM necesita un servidor de Minecraft para 10 amigos?",
       "En vanilla o con unos pocos plugins, 3 GB van sobrados. Con un modpack "
       "grande de 100 a 250 mods, el mismo grupo de 10 se te va a 8 o 12 GB. "
       "Los mods pesan más que las personas."),
      ("¿Puedo jugar desde PS5 o Switch en un servidor propio?",
       "Sí, si el servidor lleva Geyser y Floodgate. Lo que no puedes es montar el "
       "servidor desde la consola: eso tiene que estar en un PC encendido siempre o "
       "en un hosting."),
      ("¿Es legal montar un servidor de Minecraft?",
       "Sí, siempre que no cobres por el acceso al juego. Mojang permite servidores "
       "y hasta vender rangos y cosméticos, pero tiene reglas: no puedes vender "
       "ventajas de juego ni cajas de botín con dinero real."),
      ("¿Cuánto cuesta tener un servidor de Minecraft al mes?",
       "Depende de los GB. Un servidor pequeño para amigos sale por 3-6 € al mes. "
       "Uno con modpack grande o comunidad, entre 7 y 15 €. Por encima de eso te "
       "están cobrando de más salvo que sea algo muy gordo."),
    ],
  ),
]


# ---------------------------------------------------------------------------
# GENERACIÓN
# ---------------------------------------------------------------------------

def _faq_schema(g):
    import json
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": p,
             "acceptedAnswer": {"@type": "Answer", "text": r}}
            for p, r in g["faq"]
        ],
    }, ensure_ascii=False, indent=2)


def _articulo_schema(g):
    import json
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": g["title"],
        "description": g["desc"],
        "totalTime": "PT%dM" % g["minutos"],
        "step": [
            {"@type": "HowToStep", "name": t.split("—")[-1].strip()}
            for t, _ in g["secciones"] if "Paso" in t
        ],
    }, ensure_ascii=False, indent=2)


def html(g):
    ruta = "/%s/%s/" % (g["juego"], g["url"])

    indice = "\n".join(
        '        <li><a href="#s%d">%s</a></li>' % (i, t)
        for i, (t, _) in enumerate(g["secciones"]))

    cuerpo = "\n".join(
        '      <h2 id="s%d">%s</h2>\n%s' % (i, t, c.rstrip())
        for i, (t, c) in enumerate(g["secciones"]))

    faq = "\n".join(
        '      <details>\n        <summary>%s</summary>\n        <p>%s</p>\n      </details>'
        % (p, r) for p, r in g["faq"])

    return """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">

<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<link rel="canonical" href="%(dom)s%(ruta)s">

<meta property="og:type" content="article">
<meta property="og:site_name" content="MontaTuServer">
<meta property="og:url" content="%(dom)s%(ruta)s">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:image" content="%(dom)s/og-image.jpg">
<meta property="og:locale" content="es_ES">
<meta name="twitter:card" content="summary_large_image">

<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>&#129518;</text></svg>">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400..800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/styles.css">
</head>
<body>

<header class="site-head">
  <div class="wrap">
    <a class="brand" href="/">&#129518; Monta<b>TuServer</b></a>
        <nav class="nav">
      <a href="/">Calculadora</a>
      <a href="/hosting/">Hostings</a>
      <a href="/comparar/">Cara a cara</a>
      <a href="/ofertas/">Ofertas</a>
    </nav>
    <div class="buscador" id="buscador"><input type="search" placeholder="Buscar hosting o guía…" aria-label="Buscar en la web" autocomplete="off"><kbd>/</kbd><div class="bs-panel" role="listbox" hidden></div></div>
  </div>
</header>

<main>
  <article class="wrap articulo">

    <nav class="miga" aria-label="Dónde estás">
      <a href="/">Inicio</a> › Guía
    </nav>

    <h1>%(h1)s</h1>
    <p class="sub art-sub">%(sub)s</p>
    <p class="art-meta">Lectura de %(minutos)d minutos · Actualizada en septiembre de 2026</p>
%(promo)s

    <nav class="indice" aria-label="Contenido">
      <div class="indice-tit">Lo que vas a leer</div>
      <ol>
%(indice)s
      </ol>
    </nav>

%(cuerpo)s

    <div class="art-cierre">
      <h2 id="faq">Dudas frecuentes</h2>
%(faq)s
    </div>

    <div class="art-cta">
      <h3>¿Y cuántos GB necesitas tú?</h3>
      <p>
        Es lo primero que hay que decidir y lo que marca el precio. La calculadora te
        lo dice en 20 segundos, sin registro, y te enseña lo que cuesta en cada
        hosting.
      </p>
      <a class="cta" href="/#calculadora">Calcular mi servidor</a>
    </div>

  </article>
</main>

<footer>
  <div class="wrap">
    <div class="disclosure">
      %(divulgacion)s
    </div>
    <p>MontaTuServer · Hecho por <a href="https://www.youtube.com/@Doublelag">Doublelag</a></p>
  </div>
</footer>

<script type="application/ld+json">
%(faq_schema)s
</script>
<script type="application/ld+json">
%(howto_schema)s
</script>
<script type="application/ld+json">
%(migas)s
</script>

<script src="/buscador_ui.js" defer></script>
<script src="/tabla_ui.js" defer></script>

</body>
</html>
""" % dict(
        title=g["title"], desc=g["desc"], h1=g["h1"], sub=g["sub"],
        minutos=g["minutos"], juego=g["juego"], juego_nombre=g["juego_nombre"],
        dom=DOMINIO, ruta=ruta, indice=indice, cuerpo=cuerpo, faq=faq,
        faq_schema=_faq_schema(g), howto_schema=_articulo_schema(g),
        promo=promo.banner(g["juego"], "BANNER-GUIA"),
        migas=migas.schema([("Inicio", "/"), (g["h1"], None)]),
        divulgacion=partner.divulgacion(),
    )
