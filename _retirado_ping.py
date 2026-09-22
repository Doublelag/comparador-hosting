# -*- coding: utf-8 -*-
"""
Página /ping-desde-espana/

La idea salió de la web de DatHost: tienen un medidor que te dice a cuántos
milisegundos tienes cada centro de datos. Ningún comparador del sector hace eso,
y para un público español el ping decide la compra tanto como el precio.

La diferencia con ellos: sus números solo hablan de sus servidores. Aquí se mide
lo mismo para varios hostings y se dice **cómo** se ha obtenido cada dato. Lo que
no se ha podido medir se deja fuera en vez de rellenarlo a ojo.

Lo importa build.py. No se ejecuta solo.
"""

import io, json, os

import hostings
import partner

DOMINIO = "https://montatuserver.com"
RAIZ = os.path.dirname(os.path.abspath(__file__))

METODOS = {
    "tcp":       ("Medido", "Conexión TCP al puerto 25565 de su servidor público de "
                            "prueba, el mejor de cuatro intentos."),
    "widget":    ("Medido", "Con el medidor de su propia web, ejecutado desde esta "
                            "misma conexión."),
    "ubicacion": ("Solo ubicación", "Sé dónde tienen centro de datos, pero no publican "
                               "servidor de prueba y no he podido medirlo yo."),
}

MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


def datos():
    s = io.open(os.path.join(RAIZ, "hosts.js"), encoding="utf-8").read()
    crudo = s[s.index("window.DATOS =") + len("window.DATOS ="):].strip().rstrip(";").strip()
    return json.loads(crudo)


def _nombre(d, host_id):
    if host_id == "dathost":
        return "DatHost"
    for h in d["hosts"]:
        if h["id"] == host_id:
            return h["nombre"]
    return host_id


def _slug(host_id):
    """Carpeta del perfil. No siempre coincide con el id del hosting
    (pebble-budget vive en /hosting/pebblehost/), asi que se lee de
    hostings.FICHAS, que es donde vive ese dato."""
    f = hostings.FICHAS.get(host_id)
    return f["url"] if f else host_id


def _clase(ms):
    return "ok" if ms <= 45 else ("warn" if ms <= 80 else "bad")


def html():
    d = datos()
    ping = d["ping"]

    a, m, dia = ping["medido"].split("-")
    fecha = "%d de %s de %s" % (int(dia), MESES[int(m) - 1], a)

    # Ordenados por el mejor ping conocido; los que no se han medido, al final.
    filas = []
    for host_id, p in ping["hosts"].items():
        medidos = [ms for _, ms in p["detalle"]]
        mejor = min(medidos) if medidos else None
        filas.append((mejor is None, mejor if mejor is not None else 9999,
                      host_id, p, mejor))
    filas.sort()

    tabla = []
    for _, _, host_id, p, mejor in filas:
        etiqueta = METODOS[p["metodo"]][0]
        cerca = ", ".join(p["europa"]) if p["europa"] else "&mdash;"
        if mejor is None:
            celda = '<td class="nd">Sin medir</td>'
        else:
            celda = '<td><b class="ms %s">%d ms</b></td>' % (_clase(mejor), mejor)
        tabla.append(
            '        <tr>\n'
            '          <td><a href="/hosting/%s/">%s</a></td>\n'
            '          <td>%s</td>\n'
            '          %s\n'
            '          <td><span class="met met-%s">%s</span></td>\n'
            '        </tr>'
            % (_slug(host_id), _nombre(d, host_id), cerca, celda, p["metodo"], etiqueta))

    # Detalle por hosting: todos los destinos, no solo el mejor. Así se ve lo que
    # te juegas si eliges mal la ubicación al contratar.
    detalles = []
    for _, _, host_id, p, _mejor in filas:
        if not p["detalle"]:
            continue
        items = "".join(
            '<li><span>%s</span><b class="ms %s">%d ms</b></li>'
            % (ciudad, _clase(ms), ms) for ciudad, ms in p["detalle"])
        detalles.append(
            '      <div class="card ping-card">\n'
            '        <h3>%s</h3>\n'
            '        <ul class="ping-lista">%s</ul>\n'
            '        <p class="ping-como">%s</p>\n'
            '      </div>'
            % (_nombre(d, host_id), items, METODOS[p["metodo"]][1]))

    faq = [
        ("¿Qué ping es aceptable en Minecraft?",
         "Por debajo de 50 ms no vas a notar nada. Entre 50 y 100 se nota al pegar y "
         "al picar bloques, pero se juega. Por encima de 150 empieza a molestar de "
         "verdad: los bloques &laquo;vuelven&raquo; y los mobs se teletransportan."),
        ("¿Hay algún hosting con servidores en España?",
         "De los que he podido comprobar, ninguno. Lo más cerca que vas a estar es "
         "Ámsterdam, Fráncfort o Londres, que desde España salen sobre 35 ms. Eso es "
         "perfectamente jugable."),
        ("¿Entonces da igual qué hosting elija por el ping?",
         "Dentro de Europa, casi. La diferencia entre 35 y 37 ms no la nota nadie. Lo "
         "que sí importa es no acabar en un centro de datos de Estados Unidos por "
         "descuido: ahí te vas a 130 ms o más."),
        ("¿Por qué vuestro ping no coincide con el mío?",
         "Porque depende de tu operador, de tu ciudad y de si vas por fibra o por "
         "móvil. Estos números son de una conexión doméstica de fibra en España, "
         "medidos el " + fecha + ". Tómalos como referencia para comparar hostings "
         "entre sí, no como una promesa de lo que vas a tener tú."),
        ("¿El ping depende del plan que contrate?",
         "No. Depende de dónde esté la máquina, no de cuánta RAM le pongas. Un plan "
         "caro en Nueva York te dará peor ping que uno barato en Ámsterdam."),
    ]
    faq_html = "\n".join(
        '      <details>\n        <summary>%s</summary>\n        <p>%s</p>\n      </details>'
        % (q, r) for q, r in faq)
    faq_schema = json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": r}}
                       for q, r in faq],
    }, ensure_ascii=False, indent=2)

    return """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">

<title>Ping desde España a cada hosting de servidores (medido a mano)</title>
<meta name="description" content="Cuántos milisegundos tienes desde España hasta los servidores de cada hosting de Minecraft. Medido con una conexión real, no estimado, y diciendo cómo se ha obtenido cada dato.">
<link rel="canonical" href="%(dom)s/ping-desde-espana/">

<meta property="og:type" content="article">
<meta property="og:site_name" content="MontaTuServer">
<meta property="og:url" content="%(dom)s/ping-desde-espana/">
<meta property="og:title" content="¿Qué ping vas a tener desde España?">
<meta property="og:description" content="Ningún hosting de servidores tiene máquinas en España. Esto es lo que vas a tener de verdad, medido.">
<meta property="og:image" content="%(dom)s/og-image.jpg">
<meta property="og:locale" content="es_ES">
<meta name="twitter:card" content="summary_large_image">

<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400..800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/styles.css">
<script type="application/ld+json">%(faq_schema)s</script>
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
  <div class="wrap articulo" style="max-width:860px">
    <nav class="miga"><a href="/">Inicio</a> &rsaquo; Ping desde España</nav>

    <h1>¿Qué <em>ping</em> vas a tener desde España?</h1>
    <p class="sub art-sub">
      Todos dicen &laquo;servidores de baja latencia&raquo; y ninguno te dice cuántos
      milisegundos son. Aquí los tienes medidos, y al lado te digo cómo.
    </p>
    <p class="art-meta">Medido el %(fecha)s desde %(desde)s</p>

    <div class="indep" style="margin:24px 0 30px">
      <span class="indep-ico" aria-hidden="true">⚡</span>
      <p>
        <strong>Empiezo por la mala noticia.</strong> De los que he podido comprobar,
        ninguno tiene máquinas en España. Lo más cerca que vas a estar es
        Ámsterdam, Fráncfort o Londres. <strong>La buena:</strong> desde aquí eso son
        unos 35 ms, y en Minecraft no se nota.
      </p>
    </div>


    <h2 id="detalle">Todos los destinos medidos</h2>
    <p>
      No solo el mejor. Así ves lo que te juegas si eliges mal la ubicación al
      contratar, que es el error más caro y el más fácil de cometer.
    </p>
    <div class="cards">
%(detalles)s
    </div>

    <h2 id="que-significa">Qué significa cada número</h2>
    <ul>
      <li><strong>Menos de 50 ms</strong> — no lo vas a notar. Es lo que tienes con
        cualquier centro de datos del centro de Europa.</li>
      <li><strong>De 50 a 100 ms</strong> — se nota al pegar y al picar bloques, pero
        se juega perfectamente.</li>
      <li><strong>Más de 150 ms</strong> — molesta de verdad: los bloques
        &laquo;vuelven&raquo; y los mobs se teletransportan. Aquí es donde acabas si
        dejas la ubicación por defecto y te toca Estados Unidos.</li>
    </ul>

    <div class="indep" style="margin:26px 0">
      <span class="indep-ico" aria-hidden="true">⚖️</span>
      <p>
        <strong>Por qué esta página está incompleta a propósito:</strong> solo aparecen
        los hostings a los que he podido medirles el ping. Los demás no publican servidor
        de prueba, y rellenarla a ojo con estimaciones sería exactamente lo que
        le critico al resto del sector. Los iré añadiendo según pueda medirlos.
      </p>
    </div>

    <div class="art-cierre">
      <h2 id="faq">Preguntas frecuentes</h2>
%(faq)s
    </div>

    <div class="art-cta" style="margin-top:34px">
      <h3>El ping ya lo sabes: ahora los gigas</h3>
      <p>
        Dentro de Europa la diferencia de latencia entre unos y otros es de un par de
        milisegundos, así que lo que de verdad decide es cuánta RAM necesitas y quién
        te la da más barata.
      </p>
      <a class="cta" href="/">Calcular mi servidor</a>
    </div>
  </div>
</main>

<footer>
  <div class="wrap">
    <div class="disclosure">
      %(divulgacion)s Las mediciones las hice igual para todos, y al lado de cada
      dato pongo cómo, para que puedas repetirlas tú.
    </div>
    <p>MontaTuServer · Hecho por <a href="https://www.youtube.com/@Doublelag">Doublelag</a></p>
  </div>
</footer>

<script src="/buscador_ui.js" defer></script>
<script src="/tabla_ui.js" defer></script>

</body>
</html>
""" % dict(dom=DOMINIO, fecha=fecha, desde=ping["desde"],
           divulgacion=partner.divulgacion(),
           tabla="\n".join(tabla), detalles="\n".join(detalles),
           faq=faq_html, faq_schema=faq_schema)
