# -*- coding: utf-8 -*-
"""
Páginas de comparativa: /minecraft/mejor-hosting/ y compañía.

Atacan las búsquedas con intención de compra ("mejor hosting minecraft",
"comparador hosting minecraft", "hosting minecraft barato"), que son las que
más convierten de toda la web.

La tabla se genera en HTML ESTÁTICO leyendo hosts.js, no con JavaScript:
el valor de esta página es la tabla, así que tiene que estar en el código
fuente para que Google la vea seguro.

Lo importa build.py. No se ejecuta solo.
"""

import io, json, os
import migas
import promo
import partner

DOMINIO = "https://montatuserver.com"
RAIZ = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------------------
# Leer la fuente única de precios
# ---------------------------------------------------------------------------

def datos():
    s = io.open(os.path.join(RAIZ, "hosts.js"), encoding="utf-8").read()
    crudo = s[s.index("window.DATOS =") + len("window.DATOS ="):].strip().rstrip(";").strip()
    return json.loads(crudo)


def carpeta(c):
    """Carpeta de la URL. Puede no coincidir con el id interno del juego:
    el id es "zomboid" pero la URL es /project-zomboid/."""
    return c.get("carpeta", c["juego"])


def eur(n):
    return ("%.2f" % n).replace(".", ",") + " €"


def precio_para(h, juego, gb, cambio):
    """Lo que cobra este hosting al mes por `gb` en ESE juego, en euros.

    Devuelve (precio, lo_que_da). None si no lo ofrece o se queda corto.
    Los precios cuelgan de precios[juego] en hosts.js; hoy solo hay Minecraft.
    """
    pr = h.get("precios", {}).get(juego)
    if not pr:
        return None, None          # None = ni siquiera lo tenemos comprobado

    a_eur = (lambda v: v * cambio) if h["moneda"] == "USD" else (lambda v: v)

    if pr["modelo"] == "porGB":
        return a_eur(pr["porGB"] * gb), "%d GB" % gb
    if pr["modelo"] == "tabla":
        for tgb, precio in pr["tiers"]:
            if gb <= tgb:
                return a_eur(precio), "%d GB" % tgb
        return None, "—"
    if pr["modelo"] == "plano":
        da = "%d slots" % pr["slots"] if pr.get("slots") else "%d GB" % pr["ram"]
        if pr.get("ram") and gb > pr["ram"]:
            return None, da
        return a_eur(pr["precio"]), da
    if pr["modelo"] == "slots":
        # se vende por plazas: en las tablas por GB mostramos su plan de entrada
        return a_eur(pr["tiers"][0][1]), "%d slots" % pr["tiers"][0][0]
    return None, "—"


# ---------------------------------------------------------------------------
# CONTENIDO
# ---------------------------------------------------------------------------

COMPARATIVAS = [
  dict(
    juego="minecraft", juego_nombre="Minecraft", url="mejor-hosting",
    title="El mejor hosting de Minecraft en 2026: {n} comparados con precios reales",
    desc="Comparativa real de {n} hostings de Minecraft con precios comprobados a mano: Godlike.host, PebbleHost, Kinetic, Shockbyte, BisectHosting, Apex y más. Con la letra pequeña que no te cuentan.",
    h1="El mejor hosting de <em>Minecraft</em>",
    sub="{n} hostings, precios comprobados a mano y la letra pequeña que no sale en su portada.",
    # los GB de referencia para la tabla grande
    gb_ref=[2, 4, 8, 16],
    gb_destacado=8,
    intro="""
      <p>
        He entrado en las {n} webs, <strong>he apuntado los precios a mano y me he
        leído la letra pequeña</strong>. Y hay sorpresas.
      </p>
      <p>
        Y un aviso: el ganador cambia según cuánta RAM necesites. Abajo tienes en qué
        caso gana cada uno. Si te recomiendo mal una vez, no vuelves.
      </p>
    """,
    secciones=[
      ("Las tres trampas que me he encontrado", """
        <p>
          Comparar precios de hosting es difícil aposta. Estos son los tres trucos
          que he visto repetidos, y cómo detectarlos:
        </p>
        <ul>
          <li>
            <strong>El precio que exige pagar dos años por adelantado.</strong>
            Hostinger anuncia sus 16 GB a 13,99 $ al mes. La letra pequeña dice que
            hay que pagar <strong>24 meses de golpe</strong> (335 $) y que después
            <strong>renueva a 28,99 $</strong>. El precio real es el doble del que
            ves en grande.
          </li>
          <li>
            <strong>El descuento que solo vale el primer mes.</strong> Apex anuncia
            un 25 % de descuento. Es del primer mes. Sus 16 GB son 53,99 $ el primero
            y <strong>71,99 $ todos los demás</strong>.
          </li>
          <li>
            <strong>Vender "slots" y no decir la RAM.</strong> Si un hosting te
            promete 20 o 50 jugadores pero no publica los gigas, no puedes saber si
            tu modpack va a ir. Y normalmente es porque no interesa que lo sepas.
          </li>
        </ul>
        <p>
          Por eso en la tabla de abajo uso siempre <strong>el precio recurrente</strong>:
          lo que vas a pagar el mes 3, el 6 y el 12. No el gancho del primer mes.
        </p>
      """),
      ("El modelo de precio importa más que la marca", """
        <p>Hay tres formas de cobrarte, y cambian por completo a quién le conviene qué:</p>
        <ul>
          <li>
            <strong>Por gigabyte</strong> (Shockbyte, BisectHosting, PebbleHost, Apex).
            Pagas según lo que pides, y entre ellos hay un abismo: los mismos 16 GB
            van de 13,76 € en PebbleHost Budget a 61,91 € en Apex.
          </li>
          <li>
            <strong>Plan único</strong> (DatHost). Un solo producto: 16 GB, Ryzen 9 7950X
            y slots ilimitados. Si necesitas 2 GB pagas de más; a partir de 12-16 GB
            compite con los más baratos por giga, y con mejor procesador.
          </li>
          <li>
            <strong>Por slots</strong> (Minecraft Realms). Cobran por jugadores y no
            publican la RAM. Cómodo de entender, imposible de comparar.
          </li>
        </ul>
        <p>
          <strong>La conclusión práctica:</strong> el "mejor hosting" depende de cuánta
          RAM necesites, y por eso esta pregunta no tiene una respuesta única. Mira
          la tabla en tu columna, no en general.
        </p>
      """),
    ],
    veredictos=[
      ("Si sois pocos y sin mods", "PebbleHost Budget",
       "Con 2-4 GB te sobra, y cobran 1 $ el giga: 3,44 € los 4 GB. Es lo más barato "
       "que hay. Dos cosas antes de contratar: el hardware es modesto, que para cuatro "
       "amigos en vanilla no se nota, y esa gama no trae copias de seguridad."),
      ("Si el servidor va a durar todo el año", "Kinetic Hosting o PebbleHost",
       "Mes a mes, los dos rondan los 0,86 € el giga: 16 GB por unos 13,75 €. Kinetic "
       "trae cinco copias de seguridad y empieza en 4 GB; PebbleHost Budget no trae "
       "copias."),
      ("Si es un servidor de temporada", "Godlike.host",
       "Un modpack con amigos, un evento, un proyecto de unos meses. Godlike tiene "
       "<strong>el mayor descuento de la comparativa, −75 % el primer mes</strong>, "
       "y es el único que te deja <strong>elegir los días</strong> (30, 90, 180 o 360), lo "
       "pruebas gratis un día y monta Ryzen de última generación con hasta tres copias "
       "diarias. Pagas lo que dura el servidor, ni un mes más. Para todo el año sale "
       "más caro que los de arriba."),
      ("Si necesitas más de 16 GB", "Kinetic, ScalaCube o los que cobran por giga",
       "Los planes únicos se quedan en 16 GB. Kinetic llega a 124 GB (32 GB por unos "
       "27,50 €), ScalaCube a 64 y PebbleHost te cobra cada giga sin techo. Por "
       "encima de eso ya estás en terreno de servidor dedicado."),
    ],
    faq=[
      ("¿Cuál es el hosting de Minecraft más barato?",
       "Depende de cuánto tiempo lo vayas a tener. Para empezar, Godlike.host: su −75 % "
       "el primer mes es el mayor descuento de la comparativa y deja los 16 GB en "
       "12,75 €. Para todo el año, Kinetic Hosting y PebbleHost Budget, que rondan los "
       "0,86 € el giga todos los meses; el Budget de PebbleHost no trae copias de seguridad."),
      ("¿Merece la pena pagar el año por adelantado?",
       "Solo si ya has probado el servidor y sabes que os vais a quedar. Coge un mes "
       "primero, mete a tu gente y mira cómo va. Y desconfía de quien solo te da el "
       "precio bueno pagando 24 meses de golpe."),
      ("¿Qué diferencia hay entre pagar por GB y un plan único?",
       "Por GB pagas exactamente lo que pides, así que es más barato si necesitas poco "
       "y mucho más caro si necesitas crecer. El plan único te da RAM de sobra por un "
       "precio fijo: pierdes si necesitas 2 GB y ganas mucho a partir de 8."),
      ("¿Los precios de esta página están actualizados?",
       "Los compruebo a mano entrando en la web de cada hosting, y la fecha está debajo "
       "de la tabla. Los hostings los cambian sin avisar, así que si ves algo distinto "
       "al entrar, avísame y lo corrijo."),
    ],
  ),
]


# ---------------------------------------------------------------------------
# GENERACIÓN
# ---------------------------------------------------------------------------

def coste_primer_ano(h, gb, cambio):
    """(cuota mensual, precio de entrada, lo que llevas gastado a los 12 meses).

    Media comparativa del sector enseña el precio de entrada como si fuera el
    precio. Aquí la tarifa de hosts.js es siempre la recurrente y el descuento
    de entrada va aparte, así que se puede decir las dos cosas: lo que pagas
    para empezar y lo que llevas gastado al año de estar.
    """
    mes, _ = precio_para(h, "minecraft", gb, cambio)
    if mes is None:
        return None, None, None
    e = (h.get("precios", {}).get("minecraft") or {}).get("entrada")
    if not e:
        return mes, None, mes * 12
    meses = e.get("meses", 1)
    entrada = mes * (1 - e["pct"] / 100.0)
    return mes, entrada, entrada * meses + mes * (12 - meses)


def tabla_primer_ano(c, d, gb=8):
    """Quién sale más barato el primer año, con los descuentos de entrada dentro."""
    cambio = d["cambioUsdEur"]
    filas = []
    for h in d["hosts"]:
        pr = h["precios"]["minecraft"]
        # Quien vende plazas sin publicar la RAM no puede estar en una tabla que
        # compara el coste de X GB: su plan de 11 jugadores no son 8 GB, y
        # ponerlo el primero por barato seria colarle un gol al lector.
        if pr["modelo"] == "slots":
            continue
        mes, entrada, ano = coste_primer_ano(h, gb, cambio)
        if mes is None:
            continue
        e = pr.get("entrada")
        gancho = ("%s <small>%s</small>" % (eur(entrada), e["que"])) if entrada is not None \
                 else '<span class="nd">no tiene</span>'
        marca = ' class="hl"' if partner.es_partner(h["id"]) else ""
        cuota = eur(mes)
        filas.append((ano, '<tr%s><td>%s</td><td class="price">%s</td><td>%s</td>'
                           '<td class="price">%s</td></tr>'
                      % (marca, h["nombre"], cuota, gancho, eur(ano))))
    filas = [f for _, f in sorted(filas, key=lambda x: x[0])]
    return ('<div class="table-wrap">\n<table class="tabla-maestra ordenable">\n'
            '<thead><tr><th>Hosting</th><th>Al mes</th><th>Precio de entrada</th>'
            '<th>Los 12 primeros meses</th></tr></thead>\n'
            '<tbody>\n%s\n</tbody>\n</table>\n</div>\n'
            '<p class="tbl-note">Para un servidor de %d GB. «Los 12 primeros meses» es el '
            'descuento de entrada donde lo hay más la tarifa normal el resto del año.</p>'
            % ("\n".join(filas), gb))


def tabla_grande(c, d):
    """La tabla maestra: cada hosting × varios tamaños de RAM."""
    cambio = d["cambioUsdEur"]
    filas = []

    for h in d["hosts"]:
        pr = h.get("precios", {}).get(c["juego"])
        if not pr:
            continue          # sin precio comprobado para este juego, no sale
        celdas = []
        for gb in c["gb_ref"]:
            precio, da = precio_para(h, c["juego"], gb, cambio)
            if precio is None:
                celdas.append('<td class="nd">no llega</td>')
            else:
                extra = ("<small>te da %s</small>" % da) if da != "%d GB" % gb else ""
                celdas.append('<td class="price">%s%s</td>' % (eur(precio), extra))
        # Orden neutro: por lo que cuesta el tamaño mas pequeño que pueden
        # servir. El partner, si lo hay, se marca pero NO sube ni un puesto.
        clave = next((precio_para(h, c["juego"], gb, cambio)[0]
                      for gb in c["gb_ref"]
                      if precio_para(h, c["juego"], gb, cambio)[0] is not None), 9e9)
        marca = ' class="hl"' if partner.es_partner(h["id"]) else ""
        filas.append((clave, '<tr%s><td>%s<small>%s</small></td>%s</tr>'
                      % (marca, h["nombre"], pr["nota"], "".join(celdas))))

    filas = [f for _, f in sorted(filas, key=lambda x: x[0])]
    cabecera = "".join("<th>%d GB</th>" % gb for gb in c["gb_ref"])
    return (
        '<div class="table-wrap">\n'
        '  <table class="tabla-maestra ordenable">\n'
        '    <thead><tr><th>Hosting</th>%s</tr></thead>\n'
        '    <tbody>\n%s\n    </tbody>\n'
        '  </table>\n</div>\n'
        '<p class="tbl-note">Precio mensual recurrente, en euros. Los que cobran en '
        'dólares están convertidos a 1&nbsp;$&nbsp;=&nbsp;%s&nbsp;€. Precios comprobados '
        'a mano el %s.</p>'
        % (cabecera, "\n".join("      " + f for f in filas),
           str(cambio).replace(".", ","), d["comprobado"]))


def cuantos(c, d):
    """Hostings (empresas, no gamas) con precio comprobado para este juego.

    PebbleHost Budget y Premium son un solo hosting: se cuentan por ficha."""
    return len({h.get("ficha") or h["id"] for h in d["hosts"] if c["juego"] in h.get("precios", {})})


def html(c):
    d = datos()
    n = cuantos(c, d)
    ruta = "/%s/%s/" % (carpeta(c), c["url"])

    secciones = "\n".join(
        '      <h2 id="s%d">%s</h2>\n%s' % (i, t, cont.rstrip())
        for i, (t, cont) in enumerate(c["secciones"]))

    veredictos = "\n".join(
        '        <div class="card">\n'
        '          <h3>%s</h3>\n'
        '          <p class="ver-gana">%s</p>\n'
        '          <p>%s</p>\n'
        '        </div>' % (caso, gana, texto)
        for caso, gana, texto in c["veredictos"])

    faq = "\n".join(
        '      <details>\n        <summary>%s</summary>\n        <p>%s</p>\n      </details>'
        % (p, r) for p, r in c["faq"])

    faq_schema = json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": p,
                        "acceptedAnswer": {"@type": "Answer", "text": r}}
                       for p, r in c["faq"]],
    }, ensure_ascii=False, indent=2)

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
      <a href="/">Inicio</a> › Mejor hosting
    </nav>

    <h1>%(h1)s</h1>
    <p class="sub art-sub">%(sub)s</p>
    <p class="art-meta">Precios comprobados el %(comprobado)s · Se revisa cada 2-3 meses</p>
%(promo)s

%(intro)s

    <h2 id="tabla">La tabla, sin adornos</h2>
    <p>
      Lo que cobra cada hosting al mes según los gigas que necesites. Fíjate en
      <strong>tu columna</strong>, no en la fila más barata: el ganador cambia
      completamente según cuánta RAM te haga falta.
    </p>

%(tabla)s

    <h2 id="primer-ano">Lo que pagas el primer año, no el primer mes</h2>
    <p>
      Esta es la cuenta que no hace casi nadie. Medio sector anuncia un precio de
      entrada — «−75 %% en tu primera compra», «−25 %% el primer mes» — y renueva a
      tarifa completa sin avisar. Así que aquí van las dos cosas: lo que pagas para
      empezar y <strong>lo que llevas gastado a los doce meses</strong>, que es
      cuando de verdad sabes si era barato.
    </p>

%(tabla_ano)s

    <div class="art-cta" style="margin-top:26px">
      <h3>¿Y cuántos GB necesitas tú?</h3>
      <p>
        Es la pregunta que decide todo lo demás. Dime cuántos sois y qué lleváis
        instalado y te lo calculo en 20 segundos. Sin registrarte ni nada.
      </p>
      <a class="cta" href="/#calculadora">Calcular mis GB</a>
    </div>

%(secciones)s

    <h2 id="veredicto">Cuál te conviene a ti</h2>
    <p>
      No hay un "mejor hosting" a secas. Hay un mejor hosting <em>para tu caso</em>,
      y cambia según cuántos seáis y qué llevéis instalado:
    </p>
    <div class="cards" style="margin-top:18px">
%(veredictos)s
    </div>

    <div class="art-cierre">
      <h2 id="faq">Dudas frecuentes</h2>
%(faq)s
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
%(migas)s
</script>

<script src="/buscador_ui.js" defer></script>
<script src="/tabla_ui.js" defer></script>

</body>
</html>
""" % dict(
        title=c["title"].replace("{n}", str(n)),
        desc=c["desc"].replace("{n}", str(n)),
        h1=c["h1"], sub=c["sub"].replace("{n}", str(n)),
        juego=carpeta(c), juego_nombre=c["juego_nombre"], dom=DOMINIO, ruta=ruta,
        comprobado=d["comprobado"], intro=c["intro"].replace("{n}", str(n)).rstrip(),
        tabla=tabla_grande(c, d), tabla_ano=tabla_primer_ano(c, d),
        secciones=secciones, veredictos=veredictos,
        faq=faq, faq_schema=faq_schema, divulgacion=partner.divulgacion(),
        migas=migas.schema([("Inicio", "/"), ("Mejor hosting de Minecraft", None)]),
        promo=promo.banner(c["juego"] if "juego" in c else carpeta(c), "BANNER-COMP"),
    )

