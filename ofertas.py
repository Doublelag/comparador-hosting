# -*- coding: utf-8 -*-
"""
Página de ofertas: /ofertas/

Los dos comparadores serios del sector tienen sección de cupones, y funciona:
es la búsqueda con más intención de compra que existe. Pero ellos se limitan a
listarlos.

Aquí se hace lo que ninguno hace: **juzgar la oferta**. Cada una lleva un
veredicto — buena, con truco o evítala — porque la mitad de los descuentos del
sector son de primer mes disfrazados de permanentes, y eso hay que decirlo.

Lo importa build.py.
"""

import io, json, os

import partner

DOMINIO = "https://montatuserver.com"
RAIZ = os.path.dirname(os.path.abspath(__file__))

REVISADO = "19 de septiembre de 2026"


def datos():
    s = io.open(os.path.join(RAIZ, "hosts.js"), encoding="utf-8").read()
    crudo = s[s.index("window.DATOS =") + len("window.DATOS ="):].strip().rstrip(";").strip()
    return json.loads(crudo)


def eur(n):
    return ("%.2f" % n).replace(".", ",") + " €"


# ---------------------------------------------------------------------------
# LAS OFERTAS
#
# veredicto: "buena" | "truco" | "evitar"
# Sé duro. Una página de cupones que dice que todos son buenos no vale nada,
# y además es exactamente lo que hace la competencia.
# ---------------------------------------------------------------------------

OFERTAS = [
  dict(
    host="HolyHosting", ficha="/hosting/holyhosting/",
    titulo="25 % de descuento con cuenta atrás",
    codigo=None,
    veredicto="truco",
    resumen="Anuncian 0,95 $ el GB en portada, con un reloj que va bajando.",
    letra="El cartel pequeño lo dice: <strong>25 % OFF on your first month</strong>. "
          "La tarifa de verdad es 1,25 $/GB, así que sus 16 GB son 19,99 $ al mes a "
          "partir del segundo. Ese 0,95 $ solo lo pagas una vez.",
    consejo="La cuenta atrás es para que no eches la cuenta. Échala: multiplica "
            "por 1,25 y compara con eso.",
  ),
  dict(
    host="The Minecraft Hosting", ficha="/hosting/theminecrafthosting/",
    titulo="60 % con el código BLACKFRIDAY",
    codigo="BLACKFRIDAY",
    veredicto="evitar",
    resumen="Un código de Black Friday del 60 %, que dicen que es «lifetime».",
    letra="Lo llaman Black Friday y está puesto <strong>en septiembre</strong>. Un "
          "descuento que no se quita nunca no es un descuento: es el precio. Sus "
          "16 GB figuran a 35 $ para que el 60 % parezca enorme. Y «lifetime», en "
          "una web, no es un contrato.",
    consejo="Si aun así te interesan, pídeles <strong>por escrito</strong> a cuánto "
            "renueva antes de pagar. Entre 35 $ y 14 $ hay demasiada diferencia como "
            "para fiarse de una palabra en un banner.",
  ),
  dict(
    host="WiseHosting", ficha="/hosting/wisehosting/",
    titulo="50 % pagando el año",
    codigo=None,
    veredicto="buena",
    resumen="Deja el GB en 1,50 $ en vez de 3,00 $ si contratas doce meses.",
    letra="Es un descuento por permanencia de los de toda la vida. Pagas el año por "
          "adelantado y ya está. No hay trampa escondida. Pero son doce meses de "
          "golpe en algo que todavía no has probado.",
    consejo="Tienen siete días de devolución. Contrata, prueba de verdad esos siete "
            "días, y si convence te quedas.",
  ),
  dict(
    host="Shockbyte", ficha="/hosting/shockbyte/",
    titulo="30 % en Minecraft, permanente",
    codigo=None,
    veredicto="buena",
    resumen="Su descuento de Minecraft es recurrente, no de primer mes. El precio "
            "que ves en su web ya lo lleva aplicado.",
    letra="Ojo al comparar: como ya está aplicado, el precio de escaparate ES el "
          "precio real. No le restes otro 30 % mentalmente.",
    consejo="En Minecraft cobran por gigabyte. Ayuda si tu plan es pequeño; a los "
            "grandes no los salva. 16 GB siguen siendo unos 47 $.",
  ),
  dict(
    host="Shockbyte", ficha="/hosting/shockbyte/",
    titulo="25 % pagando el año",
    codigo=None,
    veredicto="buena",
    resumen="Descuento por contratar 12 meses. También tienen un 10 % pagando "
            "trimestral.",
    letra="Pagas los 12 meses por adelantado. Si el servidor no os convence al mes "
          "y medio, ya lo has soltado.",
    consejo="Razonable si ya has probado el servicio. Nunca como primera compra.",
  ),
  dict(
    host="Apex Hosting", ficha="/hosting/apex-hosting/",
    titulo="25 % con el código APEX25",
    codigo="APEX25",
    veredicto="truco",
    resumen="25 % de descuento en el primer pedido.",
    letra="<strong>Es solo del primer mes.</strong> Sus 16 GB pasan de 53,99 $ el "
          "primero a <strong>71,99 $ todos los demás</strong>. El descuento tapa "
          "que son, con diferencia, los más caros de la comparativa.",
    consejo="No dejes que el 25 % te distraiga: mira el precio del mes 2. Por esos "
            "71,99 $ tienes la misma RAM por unos 13,75 € en otro sitio.",
  ),
  dict(
    host="Hostinger", ficha="/hosting/hostinger/",
    titulo="Hasta 67 % de descuento",
    codigo=None,
    veredicto="evitar",
    resumen="Anuncian los 16 GB a 13,99 $/mes en vez de 42,99 $.",
    letra="Para ese precio hay que <strong>pagar 24 meses por adelantado</strong> "
          "(335,76 $ de golpe) y después <strong>renueva a 28,99 $/mes</strong>, "
          "más del doble de lo anunciado. El 67 % se calcula sobre un precio de "
          "tarifa que casi nadie paga.",
    consejo="Es la oferta más engañosa que he encontrado en el sector. Si aun así "
            "te interesan, haz la cuenta con 28,99 $, que es lo que vas a pagar.",
  ),
  dict(
    host="Nodecraft", ficha="/hosting/nodecraft/",
    titulo="30 % el primer mes y 24 horas gratis",
    codigo=None,
    veredicto="truco",
    resumen="Rehicieron la web en septiembre: prueba de 24 h y el primer mes un 30 % más barato.",
    letra="El −30 % es <strong>solo del primer mes</strong>: los 8 GB entran por "
          "27,99 $ y renuevan a 39,98 $. Y para la prueba gratis <strong>piden "
          "verificar el teléfono</strong>, cosa que no avisan hasta el final.",
    consejo="Las 24 horas gratis valen para ver el panel. Pero a 4,99 $ el giga están "
            "de los más caros de la comparativa: haz la cuenta con el precio del mes dos.",
  ),
]


VEREDICTOS = {
    "buena":  ("Oferta real",   "ok"),
    "truco":  ("Con truco",     "warn"),
    "evitar": ("Yo la evitaría","bad"),
}


def html():
    d = datos()
    # Id de hosting a partir de la ficha, para saber si la oferta es del partner.
    import hostings
    id_de_ficha = {}
    for hid, f in hostings.FICHAS.items():
        id_de_ficha.setdefault("/hosting/%s/" % f["url"], hid)

    import datetime
    hoy = datetime.date.today().isoformat()

    tarjetas = []
    for o in OFERTAS:
        if o.get("caduca") and hoy > o["caduca"]:
            continue                       # las caducadas desaparecen solas
        etiqueta, cls = VEREDICTOS[o["veredicto"]]

        codigo = ('<div class="of-codigo"><span>Código</span><code>%s</code></div>'
                  % o["codigo"]) if o.get("codigo") else ""

        caduca = ('<p class="of-caduca">⏳ Acaba el %s/%s</p>'
                  % (o["caduca"][8:10], o["caduca"][5:7])) if o.get("caduca") else ""

        hid = id_de_ficha.get(o["ficha"])
        boton = partner.boton(o.get("juego", "minecraft"), "OFERTAS") if partner.es_partner(hid)                 else ('<a class="cta-ghost" href="%s">Ver ficha de %s</a>' % (o["ficha"], o["host"]))

        tarjetas.append("""
      <article class="oferta %s" data-veredicto="%s" data-codigo="%s">
        <div class="of-top">
          <a class="of-host" href="%s">%s</a>
          <span class="of-badge">%s</span>
        </div>
        <h3>%s</h3>
        %s
        <p class="of-resumen">%s</p>
        %s
        <div class="of-letra">
          <span class="of-letra-tit">La letra pequeña</span>
          <p>%s</p>
        </div>
        <p class="of-consejo"><strong>Mi consejo:</strong> %s</p>
        <div class="of-cta">%s</div>
      </article>""" % (cls, o["veredicto"], "si" if o.get("codigo") else "no",
                       o["ficha"], o["host"], etiqueta, o["titulo"],
                       caduca, o["resumen"], codigo, o["letra"], o["consejo"], boton))

    vivas = [o for o in OFERTAS
             if not (o.get("caduca") and hoy > o["caduca"])]
    n_buenas = sum(1 for o in vivas if o["veredicto"] == "buena")
    n_total = len(vivas)

    return """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">

<title>Ofertas y cupones de hosting de servidores (%(rev)s)</title>
<meta name="description" content="Las ofertas reales de hosting de Minecraft, con su letra pequeña y un veredicto honesto. Cuáles valen la pena y cuáles son descuentos de primer mes disfrazados.">
<link rel="canonical" href="%(dom)s/ofertas/">

<meta property="og:type" content="website">
<meta property="og:site_name" content="MontaTuServer">
<meta property="og:url" content="%(dom)s/ofertas/">
<meta property="og:title" content="Ofertas de hosting de servidores, con la letra pequeña">
<meta property="og:description" content="Aquí no me limito a listar cupones. Te digo cuáles valen la pena y cuáles son un descuento de primer mes disfrazado de permanente.">
<meta property="og:image" content="%(dom)s/og-image.jpg">
<meta property="og:locale" content="es_ES">
<meta name="twitter:card" content="summary_large_image">

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
  <div class="wrap articulo" style="max-width:860px">
    <nav class="miga"><a href="/">Inicio</a> › Ofertas</nav>

    <h1>Ofertas de hosting, <em>con la letra pequeña</em></h1>
    <p class="sub art-sub">
      Todas las webs de cupones te dicen que sus ofertas son buenísimas. Aquí de
      %(n_total)d solo %(n_buenas)d me parecen de verdad, y a todas les pongo la letra
      pequeña igual de grande.
    </p>
    <p class="art-meta">Revisadas a mano el %(rev)s</p>

    <div class="indep" style="margin:24px 0 30px">
      <span class="indep-ico" aria-hidden="true">⚖️</span>
      <p>
        <strong>El truco más repetido del sector:</strong> anunciar un descuento
        enorme que solo vale el primer mes, o que exige pagar dos años por
        adelantado. Por eso aquí cada oferta lleva su veredicto y el precio que
        vas a pagar <em>de verdad</em> a partir del mes dos.
      </p>
    </div>

    <div class="filtros" id="filtros-ofertas" role="group"
         aria-label="Filtrar las ofertas"></div>
    <div class="ofertas">%(tarjetas)s
    </div>

    <div class="art-cta" style="margin-top:36px">
      <h3>¿Cuál te sale mejor a ti?</h3>
      <p>
        Un descuento solo es bueno si el plan te encaja. Dime a qué jugáis y
        cuántos sois, pon tu presupuesto, y te digo qué opción te conviene
        con los precios ya comparados.
      </p>
      <a class="cta" href="/">Calcular mi servidor</a>
    </div>
  </div>
</main>

<footer>
  <div class="wrap">
    <div class="disclosure">
      %(divulgacion)s
    </div>
    <p>MontaTuServer · Hecho por <a href="https://www.youtube.com/@Doublelag">Doublelag</a></p>
  </div>
</footer>

<script src="/buscador_ui.js" defer></script>
<script src="/tabla_ui.js" defer></script>
<script src="/filtros_ui.js" defer></script>

</body>
</html>
""" % dict(dom=DOMINIO, rev=REVISADO, tarjetas="".join(tarjetas),
           divulgacion=partner.divulgacion(),
           n_total=n_total, n_buenas=n_buenas)
