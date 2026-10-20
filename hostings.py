# -*- coding: utf-8 -*-
"""
Fichas de hosting: /hosting/shockbyte/, /hosting/dathost/…

Por qué existen: quien ya tiene un nombre en la cabeza ("¿qué tal Shockbyte?")
no entra por la calculadora, entra por el hosting. Cada ficha le da lo que
cobra en Minecraft por tamaño, lo bueno, los peros y un veredicto.

Desde el 17-sep-2026 la web es solo de Minecraft: antes aquí había una tabla
de lo que cobraba cada hosting en 11 juegos.

Lo importa build.py.
"""

import io, json, os

# Reutilizamos el cálculo de precios en vez de duplicarlo:
# si un día cambia la lógica, cambia en los dos sitios a la vez.
from comparativas import precio_para, coste_primer_ano

import fichas_extra
import historico
import migas
import partner

DOMINIO = "https://montatuserver.com"
RAIZ = os.path.dirname(os.path.abspath(__file__))

# Tamaños que se enseñan en las tablas de precio
GB_TABLA = [2, 4, 8, 16, 32]

# ---------------------------------------------------------------------------
# FICHAS EDITORIALES
# Los precios salen de hosts.js. Aquí solo va el juicio: qué son, cuándo
# compensan y cuándo no. Sin esto la página sería una tabla sin criterio.
# ---------------------------------------------------------------------------

FICHAS = {
  "dathost": dict(
    desde_ano="2015", ubicaciones="9", rasgos=['Ryzen 9 7950X', 'Slots ilimitados', '14 días de devolución'],
    url="dathost", nombre="DatHost", pais="Suecia",
    resumen="Un solo plan de 16 GB, con Ryzen 9 7950X y slots ilimitados.",
    bueno=[
      "Un único producto: 16 GB, sin escalones ni tramos que descifrar.",
      "Slots ilimitados, así que el número de jugadores nunca te sube el precio.",
      "Pagando el año por adelantado baja a 6,90 € al mes por los mismos 16 GB.",
    ],
    malo=[
      "Si solo necesitas 2 o 3 GB, pagas de más: no hay plan pequeño.",
      "El plan trae 30 GB de disco. A partir de ahí cobran 0,30 € por GB y mes, "
      "y un modpack grande con copias de seguridad se los come.",
      "Nueve localizaciones en seis países: menos red que algunos rivales. "
      "Desde España lo más cerca es Fráncfort o Ámsterdam.",
    ],
    veredicto="Con 16 GB por 14,90 € al mes compite con los más baratos por giga, "
              "y con mejor procesador que casi todos; pagando el año baja a 6,90 €. "
              "Si solo necesitas 2 o 3 GB, estás pagando RAM que no vas a usar y "
              "casi cualquier otro te sale más barato.",
  ),
  "shockbyte": dict(
    desde_ano="2013", ubicaciones="9", rasgos=['De los más conocidos', 'Reembolso 72 h'],
    url="shockbyte", nombre="Shockbyte", pais="Australia",
    resumen="De los más conocidos del sector. En Minecraft cobra por gigabyte, desde 2,79 $.",
    bueno=[
      "Muchos años en el sector y mucha gente usándolo: hay opiniones de sobra.",
      "El plan de entrada es barato: 1 GB por 2,79 $.",
    ],
    malo=[
      "En Minecraft cobra por gigabyte, así que crecer sale caro: 16 GB se van a 47 $.",
      "Su 30 % de descuento está ya aplicado en el precio que anuncian, ojo al comparar.",
    ],
    veredicto="Buena opción para empezar con un servidor pequeño. Se vuelve caro "
              "en cuanto necesitas RAM, porque cobra cada giga.",
  ),
  "bisect": dict(
    desde_ano="2012", ubicaciones="10", rasgos=['Web en español', 'Precios en euros', 'Modpacks CurseForge'],
    url="bisecthosting", nombre="BisectHosting", pais="Estados Unidos",
    resumen="Precio por gigabyte, lineal y clarísimo: 2,69 € el GB, sin sorpresas.",
    bueno=[
      "El precio es una línea recta: sabes exactamente lo que vas a pagar.",
      "Web en español y precios en euros, cosa rara en el sector.",
      "Muy integrado con modpacks de CurseForge.",
    ],
    malo=[
      "Es de los más caros por gigabyte de los que he mirado.",
      "16 GB se van a 43,04 € al mes, más del triple que PebbleHost Budget.",
      "En septiembre de 2026 subió de 2,66 € a 2,69 € el giga. Poco, pero subió.",
    ],
    veredicto="Su transparencia de precios es de las mejores. El problema es que "
              "cuando haces la multiplicación, sale caro.",
  ),
  "apex": dict(
    desde_ano="2013", ubicaciones="20+", rasgos=['Soporte 24/7', 'Fusionado con MCProHosting', 'vCores dedicados en su gama EX'],
    url="apex-hosting", nombre="Apex Hosting", pais="Estados Unidos",
    resumen="Marca grande con mucho marketing. También la más cara de la comparativa.",
    bueno=[
      "Soporte 24/7 con buena reputación y muchísimos modpacks de un clic.",
      "MCProHosting se ha fusionado con ellos, así que ahora son aún más grandes.",
      "Su gama EX de 16 GB lleva vCores dedicados, no compartidos.",
    ],
    malo=[
      "Es el más caro de todos: 71,99 $ al mes por 16 GB.",
      "El 25 % de descuento que anuncian es solo del primer mes.",
    ],
    veredicto="Pagas marca y soporte. Si eso te importa más que el precio, adelante; "
              "si miras el euro, hay opciones cuatro veces y media más baratas por la misma RAM.",
  ),
  "hostinger": dict(
    desde_ano="2004", ubicaciones="8", rasgos=['Soporte en español', 'Facturación europea', 'VPS con acceso root'],
    url="hostinger", nombre="Hostinger", pais="Lituania",
    resumen="Gigante del hosting web que también vende servidores de juego, en formato VPS.",
    bueno=[
      "Marca enorme, con soporte en español y facturación europea.",
      "Los planes traen más CPU y disco que la media, porque son VPS de verdad.",
    ],
    malo=[
      "El precio de escaparate exige pagar 24 MESES por adelantado.",
      "Después renueva casi al doble: los 16 GB pasan de 13,99 $ a 28,99 $.",
      "Al ser VPS, tienes que administrar más cosas tú que en un panel de juego.",
    ],
    veredicto="Su oferta parece la mejor de la tabla hasta que lees la letra pequeña. "
              "Con el precio de renovación en la mano, está en la media.",
  ),
  "pebble-budget": dict(
    desde_ano="2017", ubicaciones="3", rasgos=['Lo más barato por GB', 'Slots ilimitados', 'Sin permanencia', 'Budget sin backups'],
    url="pebblehost", nombre="PebbleHost", pais="Reino Unido",
    resumen="Dos gamas: Budget a 1 $ el GB, y Premium con Ryzen 9 a 2,25 $.",
    bueno=[
      "Su gama Budget es lo más barato que he encontrado: 1 $ por gigabyte.",
      "Slots ilimitados incluso en los planes pequeños.",
      "Pago mensual sin permanencia.",
    ],
    malo=[
      "La gama Budget <strong>no incluye copias de seguridad automáticas</strong>: "
      "eso es del plan Premium. Es lo que estás pagando de menos.",
      "Su hardware es más modesto — Ryzen 7 5700X y memoria DDR4 a 2133 MHz — y en "
      "modpacks grandes se nota.",
      "Subir a Premium te dobla el precio por gigabyte: de 1 $ a 2,25 $.",
    ],
    veredicto="Para servidores pequeños y sin mods es probablemente la mejor relación "
              "precio-prestaciones que hay. "
              "Pero acuérdate de las copias: si el mundo os importa, o subís a Premium "
              "o os hacéis las copias a mano. Y en cuanto pides muchos gigas la cuenta "
              "se da la vuelta, porque cobra por GB y no tiene tope.",
  ),
  "sparked": dict(
    desde_ano="2019", ubicaciones="6",
    rasgos=['Ryzen 9 7900 con DDR5', 'Prueba gratis de 1 día', 'Tres gamas'],
    url="sparked-host", nombre="Sparked Host", pais="Estados Unidos",
    resumen="Precio por gigabyte con hardware moderno: Ryzen 9 7900 y DDR5.",
    bueno=[
      "Hardware actual de verdad: Ryzen 9 7900 con memoria DDR5.",
      "Precio por GB lineal y sin trucos: 2,59 $.",
      "Tiene una gama Extreme con Ryzen 9 9900X para quien la necesite.",
      "Prueba gratis de un día, sin compromiso.",
    ],
    malo=[
      "Como todos los que cobran por GB, escalar sale caro.",
      "Menos conocido, así que hay menos opiniones de gente de fuera.",
      "Las copias de seguridad vienen justas: tres incluidas, y ampliar cuesta más "
      "dinero. Lo mismo con el almacenamiento.",
    ],
    veredicto="Buena opción intermedia si quieres hardware moderno sin pagar precio "
              "de marca grande.",
  ),
  "nodecraft": dict(
    desde_ano="2013", ubicaciones="10+",
    rasgos=['Prueba gratis de 24 h', 'Socio oficial de Hypixel', 'Piden verificar el teléfono'],
    url="nodecraft", nombre="Nodecraft", pais="Estados Unidos",
    resumen="Rehicieron su web en septiembre de 2026: ahora te preguntan tres cosas y te asignan plan.",
    bueno=[
      "Prueba gratis de 24 horas sin pagar nada.",
      "Su web ya no te hace elegir entre veinte planes: preguntan cuántos sois y "
      "qué jugáis, y te dicen el plan. Se agradece si no tienes ni idea de gigas.",
      "Son socios oficiales de Hypixel y llevan desde 2013 en esto.",
      "Siete días de devolución.",
    ],
    malo=[
      "<strong>Han subido mucho</strong>: 4,99 $ el GB, de los más caros que he mirado. "
      "Sus 8 GB son 39,98 $ al mes.",
      "El −30 % que enseñan es <strong>solo del primer mes</strong>.",
      "<strong>Piden verificar el teléfono</strong> hasta para la prueba gratis.",
      "Su gama Lite, la que se enciende sola cuando alguien entra, sigue existiendo "
      "pero <strong>ya no publican su precio</strong>: hay que preguntarlo.",
    ],
    veredicto="La idea de que te dimensionen el servidor a base de preguntas está bien "
              "para quien empieza, y la prueba de 24 horas ayuda a decidir. Pero el "
              "precio se ha ido a 4,99 $ el giga, y por ese dinero hay bastantes "
              "opciones mejores en esta misma tabla. Si te interesan, que sea por la "
              "gama Lite — y entonces pídeles el precio por escrito.",
  ),
}

# Las de fichas_extra.py se juntan aqui para que el resto del modulo solo
# tenga que mirar un diccionario.
FICHAS.update(fichas_extra.FICHAS_EXTRA)


def datos():
    s = io.open(os.path.join(RAIZ, "hosts.js"), encoding="utf-8").read()
    crudo = s[s.index("window.DATOS =") + len("window.DATOS ="):].strip().rstrip(";").strip()
    return json.loads(crudo)


def eur(n):
    return ("%.2f" % n).replace(".", ",") + " €"


def _modelo_texto(pr, h, cambio):
    """Cómo cobra, en una línea y en euros."""
    aEur = (lambda v: v * cambio) if h["moneda"] == "USD" else (lambda v: v)
    if pr["modelo"] == "porGB":
        return "%s por GB" % eur(aEur(pr["porGB"]))
    if pr["modelo"] == "tabla":
        return "Por escalones de RAM"
    if pr["modelo"] == "slots":
        return "Por plazas, sin RAM publicada"
    if pr["modelo"] == "plano":
        que = "%d slots" % pr["slots"] if pr.get("slots") else "%d GB" % pr["ram"]
        return "Plan único de %s" % que
    return "—"


def tabla_precios(host_id, d):
    """Lo que cobra ESTE hosting por cada tamaño de servidor de Minecraft."""
    cambio = d["cambioUsdEur"]
    h = next(x for x in d["hosts"] if x["id"] == host_id)
    celdas = []
    for gb in GB_TABLA:
        precio, da = precio_para(h, "minecraft", gb, cambio)
        if precio is None:
            celdas.append('<td class="nd">no llega</td>')
        else:
            extra = ("<small>te da %s</small>" % da) if da != "%d GB" % gb else ""
            celdas.append('<td class="price">%s%s</td>' % (eur(precio), extra))
    pr = h["precios"]["minecraft"]

    # ¿Ha movido precios desde la última vez que se miró? Es la pregunta que
    # contesta el historial de idealo y que aquí no contestaba nadie.
    historia = historico.cambio(host_id, h["moneda"], cambio)
    aviso = ('<p class="tbl-note">📉 %s</p>' % historia) if historia else ""

    # Lo que cuesta de verdad el primer año, si es de los que hacen oferta de entrada
    if pr.get("entrada"):
        # se busca el tamaño mayor que ese hosting pueda servir, hasta 8 GB:
        # GPORTAL no llega a 8 y sin esto la ficha reventaba
        mes = entrada = ano = None
        for gb_ref in (8, 6, 4, 2):
            mes, entrada, ano = coste_primer_ano(h, gb_ref, cambio)
            if mes is not None:
                break
    if pr.get("entrada") and mes is not None:
        if pr["entrada"].get("permanente"):
            # No hay trampa que avisar: lo que toca decir es que no caduca.
            aviso = ('<p class="tbl-note"><strong>Su descuento no caduca.</strong> '
                     'Un servidor de %d GB sale por %s al mes con el c\u00f3digo, en vez de %s, '
                     'y sigue as\u00ed el mes doce: <strong>%s el primer a\u00f1o</strong>.</p>'
                     % (gb_ref, eur(entrada), eur(mes), eur(ano)))
        else:
            aviso = ('<p class="tbl-note"><strong>Ojo con su descuento de entrada.</strong> '
                     'Un servidor de %d GB te entra por %s %s, pero despu\u00e9s son %s al mes: '
                     '<strong>%s el primer a\u00f1o</strong>.</p>'
                     % (gb_ref, eur(entrada), pr["entrada"]["que"], eur(mes), eur(ano)))

    return (aviso + '<div class="table-wrap">\n<table class="tabla-maestra">\n'
            '<thead><tr><th>Plan</th>%s</tr></thead>\n'
            '<tbody>\n<tr><td>%s<small>%s</small></td>%s</tr>\n</tbody>\n</table>\n</div>\n'
            '<p class="tbl-note">Precio mensual en euros. Los que cobran en dólares están '
            'convertidos a 1&nbsp;$&nbsp;=&nbsp;%s&nbsp;€.</p>'
            % ("".join("<th>%d GB</th>" % gb for gb in GB_TABLA),
               _modelo_texto(pr, h, cambio), pr["nota"], "".join(celdas),
               str(cambio).replace(".", ",")))


def html(host_id, f, d):
    h = next(x for x in d["hosts"] if x["id"] == host_id)
    cambio = d["cambioUsdEur"]

    ruta = "/hosting/%s/" % f["url"]
    lista = lambda items, cls: "\n".join(
        '        <li class="%s">%s</li>' % (cls, x) for x in items)

    # Aviso y boton SOLO si este hosting es el partner configurado en hosts.js.
    # Antes estaba cableado a DatHost: con el cambio de partner mentia en cada ficha.
    aviso = ""
    precio_final = ""
    if partner.es_partner(host_id):
        aviso = ('<div class="indep" style="margin-bottom:20px">'
                 '<span class="indep-ico">💶</span><p><strong>Aviso: con este hosting '
                 'sí gano comisión.</strong> Por eso los "peros" de abajo están escritos '
                 'con el mismo cuidado que los de los demás, y en las tablas sale en '
                 'el puesto que le toca por precio, no más arriba.</p></div>')
        juego = "minecraft"
        cfg = partner.config()
        codigo = ('<p class="pf-pie">Código de descuento: <strong>%s</strong>%s</p>'
                  % (cfg["codigo"], (" · " + cfg["descuento"]) if cfg.get("descuento") else "")
                  ) if cfg.get("codigo") else ""
        precio_final = """
    <div class="precio-final" style="border-top:0;padding-top:0">
      %s
      %s
      <div class="cta-row">
        %s
        <p class="cta-fine">%s</p>
      </div>
    </div>""" % (partner.razones(), codigo, partner.boton(juego, "FICHA", "Ir a %s" % f["nombre"]),
                 partner.aviso_boton())

    faq_schema = json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": "¿Cuánto cuesta %s?" % f["nombre"],
             "acceptedAnswer": {"@type": "Answer", "text": f["resumen"]}},
            {"@type": "Question", "name": "¿Merece la pena %s?" % f["nombre"],
             "acceptedAnswer": {"@type": "Answer", "text": f["veredicto"]}},
        ],
    }, ensure_ascii=False, indent=2)

    return """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">

<title>%(nombre)s para Minecraft: precios reales y si compensa (2026)</title>
<meta name="description" content="%(resumen)s Precios comprobados a mano, lo bueno, lo malo y en qué casos compensa.">
<link rel="canonical" href="%(dom)s%(ruta)s">

<meta property="og:type" content="article">
<meta property="og:site_name" content="MontaTuServer">
<meta property="og:url" content="%(dom)s%(ruta)s">
<meta property="og:title" content="%(nombre)s para Minecraft: precios reales y si compensa">
<meta property="og:description" content="%(resumen)s">
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
  <article class="wrap articulo">

    <nav class="miga" aria-label="Dónde estás">
      <a href="/">Inicio</a> › <a href="/hosting/">Hostings</a> › %(nombre)s
    </nav>

    <h1><img class="ficha-logo" src="/logos/%(url)s.png" alt="" width="46" height="46">%(nombre)s</h1>
    <p class="sub art-sub">%(resumen)s</p>
    <p class="veredicto-top" data-tit="Veredicto en una frase">%(veredicto)s</p>
    <div class="ficha-datos">
      <div><span>Sede</span><b>%(pais)s</b></div>
      <div><span>En el mercado desde</span><b>%(desde_ano)s</b></div>
      <div><span>Ubicaciones</span><b>%(ubicaciones)s</b></div>
      <div><span>Cómo cobra</span><b>%(modelo)s</b></div>
    </div>
    <div class="ficha-rasgos">%(rasgos)s</div>
    <p class="art-meta">Precios comprobados el %(comprobado)s</p>
    %(opiniones)s

    %(aviso)s

    <h2 id="precios">Lo que cobra en Minecraft</h2>
    <p>
      Lo que pagas al mes según los gigas que necesites. Si no sabes cuántos son,
      la calculadora te lo dice en 20 segundos.
    </p>
%(tabla)s

    <div class="pros-contras">
      <div><h2 id="bueno">Lo bueno</h2>
      <ul class="lista-si">
%(bueno)s
      </ul></div>
      <div><h2 id="malo">Los peros</h2>
      <ul class="lista-no">
%(malo)s
      </ul></div>
    </div>

    <h2 id="veredicto">Veredicto</h2>
    <p class="veredicto-final">%(veredicto)s</p>

    %(precio_final)s

    <div class="art-cta">
      <h3>¿Es el mejor para tu caso?</h3>
      <p>
        Depende de cuánta RAM necesites, y eso cambia el ganador por completo.
        Dime cuántos sois y qué lleváis instalado y te lo digo en 20 segundos, con
        %(nombre)s comparado al lado de los demás.
      </p>
      <a class="cta" href="/">Calcular y comparar</a>
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
        nombre=f["nombre"], url=f["url"], resumen=f["resumen"], pais=f["pais"],
        veredicto=f["veredicto"], dom=DOMINIO, ruta=ruta,
        precio_final=precio_final,
        desde_ano=f.get("desde_ano", "—"),
        ubicaciones=f.get("ubicaciones", "—"),
        modelo=_modelo_texto(h["precios"]["minecraft"], h, cambio),
        opiniones=opiniones(h), rasgos="".join('<span class="rasgo">%s</span>' % r for r in f.get("rasgos", [])),
        comprobado=d["comprobado"], aviso=aviso, divulgacion=partner.divulgacion(),
        tabla=tabla_precios(host_id, d),
        bueno=lista(f["bueno"], "si"), malo=lista(f["malo"], "no"),
        faq_schema=faq_schema,
        migas=migas.schema([("Inicio", "/"), ("Hostings", "/hosting/"),
                            (f["nombre"], None)]),
    )



def dominio_de(h):
    """El dominio del hosting, sacado de la URL de su web (campo `fuente`)."""
    import re
    m = re.search(r"https?://(?:www\.)?([^/]+)", h.get("fuente") or "")
    return m.group(1) if m else None


def opiniones(h, lang="es"):
    """Enlace a sus opiniones. Sin nota: esa la lee cada uno, que además cambia."""
    dom = dominio_de(h)
    if not dom:
        return ""
    if lang == "es":
        return ('<p class="opiniones">Lo que dicen sus clientes: '
                '<a href="https://www.trustpilot.com/review/%s" rel="nofollow noopener" '
                'target="_blank">opiniones de %s en Trustpilot</a>. '
                'Mira el número de reseñas, no solo la nota: un 4,9 con 200 opiniones '
                'dice menos que un 4,5 con 20.000.</p>' % (dom, h["nombre"]))
    return ('<p class="opiniones">What their customers say: '
            '<a href="https://www.trustpilot.com/review/%s" rel="nofollow noopener" '
            'target="_blank">%s reviews on Trustpilot</a>. '
            'Look at the number of reviews, not just the score: a 4.9 from 200 reviews '
            'says less than a 4.5 from 20,000.</p>' % (dom, h["nombre"]))


def indice(d):
    """La página /hosting/ que lista todos. La segunda puerta de entrada.

    Es una tabla de ranking y no una lista de tarjetas porque lo que quiere
    quien entra aquí es comparar de un vistazo, no leer nueve nombres.
    Ordenada por lo que cobran por 8 GB en Minecraft, que es el caso más común.
    """
    cambio = d["cambioUsdEur"]
    filas = []
    for hid, f in FICHAS.items():
        h = next(x for x in d["hosts"] if x["id"] == hid)
        pares = [precio_para(h, "minecraft", gb, cambio) for gb in (4, 8, 16)]
        precios = [x[0] for x in pares]
        # Precio por giga, para comparar peras con peras. Es el truco de los
        # comparadores de super y de luz: el euro por kilo y el euro por kWh.
        # Aqui el equivalente es el euro por GB, y ordena el ruido de un vistazo.
        # Euro por giga, que es el "precio por kilo" de esto. Se divide entre los
        # gigas que te DAN, no entre los que pediste: DatHost cobra 14,90 € por un
        # plan de 16 GB, y contarlo como 1,86 €/GB (14,90 entre los 8 que pedias)
        # seria castigarle por darte de mas. Quien vende plazas no entra: no
        # publica la RAM, asi que su euro por giga no se puede saber.
        # Se calcula con su plan de 8 GB; si no llega a 8 (GPORTAL se queda en 6),
        # se usa el mayor que sí pueda servir, que es mejor que dejar el hueco.
        porgb = None
        for gb_ref in (8, 6, 4, 2):
            precio_ref, da_ref = precio_para(h, "minecraft", gb_ref, cambio)
            if precio_ref is None or not (da_ref or "").endswith("GB"):
                continue
            try:
                gb_reales = int(da_ref.split()[0])
            except ValueError:
                continue
            porgb = precio_ref / gb_reales
            break
        filas.append((hid, f, h, precios, porgb, pares))

    # Por euro/GB: es lo unico que compara de verdad planes cerrados con tarifas
    # por giga. Quien no publica RAM (Realms) no tiene ese numero y va al final.
    filas.sort(key=lambda x: (x[4] is None, x[4] or 0))

    # Distintivos: se calculan una vez, de los datos, y solo uno por hosting.
    # Nada de "mejor soporte" ni notas inventadas: solo lo que se puede medir.
    _con_gb = [x for x in filas if x[4] is not None]
    _barato = _con_gb[0][0] if _con_gb else None
    _entrada = max(filas, key=lambda x: (x[2]["precios"]["minecraft"].get("entrada") or {}).get("pct", 0))
    _entrada = _entrada[0] if (_entrada[2]["precios"]["minecraft"].get("entrada") or {}).get("pct") else None

    def _techo(h):
        pr = h["precios"]["minecraft"]
        if pr["modelo"] == "tabla":
            return max(t[0] for t in pr["tiers"])
        if pr["modelo"] == "porGB":
            return 64
        return pr.get("ram") or 0
    _grande = max(filas, key=lambda x: _techo(x[2]))[0]

    DISTINTIVOS = {}
    if _barato:
        DISTINTIVOS[_barato] = "El giga más barato"
    if _entrada and _entrada not in DISTINTIVOS:
        DISTINTIVOS[_entrada] = "Lo más barato para empezar"
    if _grande not in DISTINTIVOS:
        DISTINTIVOS[_grande] = "El que más RAM da"

    # Tres ganadores encima de la tabla: los mismos distintivos, con el dato
    # medible que los hace ganar. Nada de opinion.
    _por = {hid: (f, h, porgb) for hid, f, h, precios, porgb, pares in filas}
    def _g(hid, tag, dato):
        f = _por[hid][0]
        return ('<a class="ganador" href="/hosting/%s/"><span class="ganador-tag">%s</span>'
                '<span class="ganador-nom"><img class="h-logo" src="/logos/%s.png" alt="" width="22" height="22">%s</span>'
                '<span class="ganador-dato">%s</span></a>' % (f["url"], tag, f["url"], f["nombre"], dato))
    ganadores = []
    if _barato:
        ganadores.append(_g(_barato, "El giga más barato", "<b>%s</b> por GB" % eur(_por[_barato][2])))
    if _entrada and _entrada != _barato:
        ganadores.append(_g(_entrada, "Lo más barato para empezar",
                            "<b>−%d %%</b> en la primera factura" % _por[_entrada][1]["precios"]["minecraft"]["entrada"]["pct"]))
    if _grande not in (_barato, _entrada):
        ganadores.append(_g(_grande, "El que más RAM da", "hasta <b>%d GB</b> en un plan" % _techo(_por[_grande][1])))
    ganadores_html = '<div class="ganadores">%s</div>' % "".join(ganadores)

    tabla = []
    for hid, f, h, precios, porgb, pares in filas:
        destacado = ' class="hl"' if partner.es_partner(hid) else ""
        celdas = "".join(
            ('<td class="price">%s%s</td>'
             % (eur(p), ("<small>te da %s</small>" % da) if da and not da.endswith("GB") else ""))
            if p is not None else '<td class="nd">no llega</td>'
            for p, da in pares)
        celdas += (('<td class="price">%s</td>' % eur(porgb)) if porgb is not None
                   else '<td class="nd">—</td>')
        # Los data-* son lo que leen los filtros. Solo dato duro: como cobra,
        # cuanto sale el giga y si su precio de escaparate es de entrada.
        pr = h["precios"]["minecraft"]
        tabla.append(
            '      <tr%s data-modelo="%s" data-porgb="%s" data-entrada="%s">\n'
            '        <td><a href="/hosting/%s/"><img class="h-logo" src="/logos/%s.png" alt="" width="18" height="18" loading="lazy">%s</a>%s<small>%s</small></td>\n'
            '        <td>%s</td>\n'
            '        %s\n'
            '        <td><a class="cta-mini" href="/hosting/%s/">Ver ficha</a></td>\n'
            '      </tr>'
            % (destacado, pr["modelo"], ("%.2f" % porgb) if porgb else "",
               "si" if (pr.get("entrada") and not pr["entrada"].get("permanente")) else "no",
               f["url"], f["url"], f["nombre"],
               ('<span class="badge-cat">%s</span>' % DISTINTIVOS[hid]) if hid in DISTINTIVOS else "",
               f["pais"],
               _modelo_texto(pr, h, cambio), celdas, f["url"]))

    tarjetas = [ganadores_html, '''    <div class="filtros" id="filtros" role="group"
         aria-label="Filtrar la tabla"></div>
    <div class="table-wrap">
      <table class="tabla-maestra ordenable" data-filtrable>
        <thead><tr>
          <th>Hosting</th><th>Cómo cobra</th><th>4 GB</th><th>8 GB</th><th>16 GB</th>
          <th>Por GB</th><th></th>
        </tr></thead>
        <tbody>
%s
        </tbody>
      </table>
    </div>
    <p class="tbl-note">
      Precio mensual en euros. Ordenados por la columna <strong>«Por GB»</strong>, que
      es lo que cuesta cada giga en su plan de 8: la forma de comparar a quien vende
      planes cerrados con quien te cobra los gigas sueltos, igual que el precio por
      kilo en el súper. Si su plan te da de más, el cálculo cuenta los gigas que te
      dan, no los que pediste. Pulsa en cualquier columna para ordenar por ella.
    </p>''' % "\n".join(tabla), partner.banner()]

    return """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Comparador de hosting de Minecraft: precios reales de %(cuantos)d comparados (2026)</title>
<meta name="description" content="Comparador de hosting de Minecraft con precios comprobados a mano: cuánto cuesta el giga en cada uno, la letra pequeña, los peros y los trucos del sector. Sin precios inventados.">
<link rel="canonical" href="%(dom)s/hosting/">
<meta property="og:type" content="website">
<meta property="og:url" content="%(dom)s/hosting/">
<meta property="og:title" content="Comparador de hosting de Minecraft">
<meta property="og:image" content="%(dom)s/og-image.jpg">
<meta property="og:locale" content="es_ES">
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
  <div class="wrap articulo">
    <nav class="miga"><a href="/">Inicio</a> › Comparador</nav>
<h1>Comparador de <em>hosting de Minecraft</em></h1>
    <p class="sub art-sub">
      Lo que cobra de verdad cada uno por 4, 8 y 16 GB, cuánto le sale el giga y la
      letra pequeña que no está en su portada. Precios comprobados a mano, uno a uno.
    </p>

%(indep)s
%(tarjetas)s


    <h2 id="trucos">Los trucos que te vas a encontrar</h2>
    <p>
      Esta web nació de cabrearme con esto. No todos los hostings hacen trampas,
      pero las que se hacen se repiten siempre, y casi ninguna es ilegal: es letra
      pequeña puesta donde no miras.
    </p>
    <ol class="trucos">
      <li>
        <strong>El precio de la portada es solo el primer mes.</strong> Es el más
        común. Ves «8 GB por 6,50 €», pagas, y al mes siguiente te cobran 25,99 €.
        Por eso en esta web el precio que manda es <strong>la tarifa normal</strong>,
        y el descuento de entrada va aparte y con su nombre.
      </li>
      <li>
        <strong>El precio bueno es pagando dos años por adelantado.</strong> Lo
        anuncian a lo grande y el «/mes» diminuto. Si cancelas antes, no recuperas
        nada, y al renovar te suben casi al doble.
      </li>
      <li>
        <strong>«Slots ilimitados» o «RAM ilimitada».</strong> Ilimitado no existe.
        Lo que hay detrás es CPU compartida con otros veinte servidores, y se nota
        justo cuando entráis todos a la vez.
      </li>
      <li>
        <strong>La gama barata viene sin copias de seguridad.</strong> Te enteras el
        día que alguien revienta el mundo. Está en la comparativa de cada uno.
      </li>
      <li>
        <strong>Los rankings de «mejor hosting» los escriben los propios hostings.</strong>
        Se ponen primeros, se dan un 4,9 y a la competencia le sacan los peros. Si
        una lista no dice quién la paga, desconfía.
      </li>
    </ol>
    <p>
      Aquí los precios se comprueban <strong>a mano en la web de cada uno</strong>, con
      la fecha puesta, la tabla se ordena por lo que cuesta el giga y cada ficha lleva
      sus peros. %(afil)s
    </p>

    <p class="art-meta">Precios comprobados el %(comprobado)s.</p>
  </div>
</main>

<footer>
  <div class="wrap">
    <p>MontaTuServer · Hecho por <a href="https://www.youtube.com/@Doublelag">Doublelag</a></p>
  </div>
</footer>

<script src="/buscador_ui.js" defer></script>
<script src="/tabla_ui.js" defer></script>
<script src="/filtros_ui.js" defer></script>

</body>
</html>
""" % dict(cuantos=len({(f.get("url") or hid) for hid, f in FICHAS.items()}),
           afil=partner.caja_afiliado_corta() if hasattr(partner, "caja_afiliado_corta") else "",
           dom=DOMINIO, tarjetas="\n".join(tarjetas), comprobado=d["comprobado"],
           # La caja solo sale si hay partner: entonces sí hay algo que avisar.
           indep=('    <div class="indep" style="margin:22px 0">\n'
                  '      <span class="indep-ico" aria-hidden="true">⚖️</span>\n'
                  '      <p>%s</p>\n    </div>\n' % partner.caja_independencia())
                 if partner.activo() else "")
