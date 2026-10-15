# -*- coding: utf-8 -*-
"""
Cara a cara entre hostings: /versus/godlike-vs-apex-hosting/ …

Por qué: "X vs Y" es de las búsquedas con más intención de compra que existe —
quien la teclea ya ha decidido gastar y solo está eligiendo. CompareGameHosting
tiene una sección entera de esto.

La tabla se genera sola desde hosts.js. Aquí solo va el juicio editorial:
cuándo gana cada uno. Sin eso sería una tabla sin criterio, que es justo lo
que ya hay de sobra en internet.

Lo importa build.py.
"""

import io, json, os

from comparativas import precio_para, coste_primer_ano
from hostings import FICHAS, datos, eur
import migas
import partner

DOMINIO = "https://montatuserver.com"
GB_REF = [2, 4, 8, 16]


# ---------------------------------------------------------------------------
# LOS DUELOS
# a / b son ids de FICHAS. El orden importa: `a` es el que sale primero.
# ---------------------------------------------------------------------------

DUELOS = [
  dict(
    a="godlike", b="apex",
    gana_a="Casi siempre: tu primer pago sale a un cuarto, y en servidores pequeños "
           "o grandes también gana a tarifa.",
    gana_b="Buscas su catálogo de modpacks de un clic o sus vCores dedicados, y te da "
           "igual pagar más.",
    veredicto="Apex es la marca más conocida de Minecraft, y también de las más caras. "
              "Godlike le gana en casi todo lo que se puede medir. Para empezar, el "
              "<strong>−75 % de su primer mes</strong> deja los 16 GB en 12,75 €, "
              "cuando Apex pide 46,43 € con su −25 % del primer mes. Y a tarifa normal "
              "tampoco se queda atrás: 6,29 € los 2 GB frente a 12,89 €, y 50,99 € los "
              "16 GB frente a 61,91 €. Solo en 8 GB se da la vuelta, y por menos de dos "
              "euros. Súmale que en Godlike eliges los días, tienes hasta tres copias "
              "diarias y Ryzen de última generación. Apex solo compensa si su catálogo "
              "de modpacks te ahorra una tarde de configuración.",
  ),
  dict(
    a="godlike", b="nodecraft",
    gana_a="En precio, en tamaño máximo y en el descuento de entrada.",
    gana_b="Quieres que te elijan el plan a base de preguntas y no te importa pagar más.",
    veredicto="Aquí no hay mucha discusión. Nodecraft rehízo su web en septiembre de "
              "2026 y se fue a 4,99 $ el giga: sus 8 GB son 34,38 € al mes. Godlike "
              "pide 25,99 € por esos mismos 8 GB, y el primer pago se queda en 6,50 €. "
              "Nodecraft además se para en 12 GB, mientras Godlike llega a 33. Los dos "
              "tienen prueba gratis, pero la de Nodecraft pide verificar el teléfono. "
              "Si dudas entre los dos, Godlike.",
  ),
  dict(
    a="godlike", b="realms",
    gana_a="Queréis un solo plugin, un solo mod, o que entren más de diez personas.",
    gana_b="Sois cuatro amigos en vanilla y no queréis tocar nada de configuración.",
    veredicto="Realms es el oficial de Mojang: cuesta 7,99 $ (6,87 €), se contrata "
              "desde el propio juego y no se rompe al actualizar. Pero tiene dos techos "
              "que no se quitan pagando: <strong>ni mods ni plugins</strong>, y "
              "<strong>diez jugadores</strong> como mucho. Godlike te da un servidor de "
              "2 GB por 6,29 € al mes, menos que Realms, con Paper, Forge, Fabric y "
              "todos los plugins que quieras. Y con el código DOUBLELAG se queda en "
              "4,72 € <strong>todos los meses</strong>, no solo el primero. Si algún "
              "día queréis meter un modpack o sois más de diez, con "
              "Realms tocará mudarse; con Godlike, subir de plan en dos clics.",
  ),
  dict(
    a="godlike", b="gportal",
    gana_a="Necesitas más de 6 GB, o un procesador de última generación.",
    gana_b="Tu servidor cabe en 2-4 GB y lo vas a tener todo el año.",
    veredicto="Los dos te montan un modpack en pocos clics y tienen buena red en "
              "Europa. La diferencia está en el techo y en la entrada. GPORTAL "
              "<strong>se queda en 6 GB</strong>: para un modpack grande o una "
              "comunidad no llega. Godlike sube hasta 33. En precio manda GPORTAL en los "
              "planes pequeños: 11,80 € los 4 GB frente a los 9,74 € de Godlike con el "
              "código, que ahí se quedan cerca, pero el −25 % de GPORTAL es solo del "
              "primer periodo y el de Godlike no caduca. Así que: servidor pequeño y "
              "sabes apañártelas, GPORTAL; más de 6 GB o quieres que te lo pongan fácil, "
              "Godlike.",
  ),
  dict(
    a="godlike", b="bisect",
    gana_a="El servidor es de unos meses, o quieres copias diarias y elegir los días.",
    gana_b="Lo vas a tener más de cuatro meses y quieres una tarifa lineal en euros.",
    veredicto="BisectHosting cobra una línea recta: 2,69 € el giga, todos los meses. "
              "Godlike cobra más a tarifa (25,99 € los 8 GB frente a 21,52 €), pero su "
              "primer mes sale a un cuarto. Echando la cuenta con 8 GB, <strong>Godlike "
              "sale más barato durante los cuatro primeros meses</strong>: 6,50 € frente "
              "a 21,52 € el primero, y 84,47 € frente a 86,08 € a los cuatro. A partir "
              "del quinto, Bisect. Por eso para un modpack de temporada, un evento o "
              "algo que no sabes cuánto va a durar, Godlike; y además eliges los días "
              "exactos y tienes hasta tres copias al día.",
  ),
  dict(
    a="godlike", b="shockbyte",
    gana_a="El servidor es de uno o dos meses, o quieres elegir los días y tener "
           "copias diarias.",
    gana_b="Lo vas a tener mucho tiempo y buscas la tarifa mensual más baja de los dos.",
    veredicto="Shockbyte es de los más conocidos y cobra por escalones de RAM: 19,26 € "
              "los 8 GB con su descuento ya aplicado. Godlike está más caro a tarifa, "
              "25,99 €, pero el primer pago sale a 6,50 € gracias al <strong>mayor descuento "
              "de la comparativa</strong>. Con 8 GB, los dos primeros meses "
              "te salen por 32,49 € en Godlike y 38,52 € en Shockbyte; al tercero ya "
              "empatan. Para un servidor corto, Godlike, con la ventaja de pagar solo los "
              "días que vais a jugar. Para uno de años, Shockbyte.",
  ),
  dict(
    a="godlike", b="hostinger",
    gana_a="No quieres atarte dos años, o el servidor es para unos meses.",
    gana_b="Vas a pagar 24 meses por adelantado y quieres un VPS que administrar tú.",
    veredicto="Hostinger anuncia precios que parecen imbatibles, pero para tenerlos hay "
              "que <strong>pagar 24 meses por adelantado</strong>, y después renueva "
              "casi al doble. Además es un VPS: te toca administrar más cosas tú. "
              "Godlike va al revés: <strong>eliges cuántos días pagas</strong>, de 30 "
              "a 360, sin ataduras, y con el código te quitas un 25 % todos los meses. "
              "Para probar, para una "
              "temporada o para no atarte dos años a algo que aún no conoces, Godlike. "
              "Si tienes claro que vas a estar dos años y sabes manejar un servidor, "
              "Hostinger sale más barato a la larga.",
  ),
  dict(
    a="godlike", b="pebble-budget",
    gana_a="Vais a jugar unas semanas o unos meses concretos, queréis copias de "
           "seguridad, o el modpack pide un procesador rápido.",
    gana_b="El servidor va a durar y quieres pagar lo menos posible cada mes.",
    veredicto="Son los dos extremos de la tabla. PebbleHost Budget es lo más barato "
              "que existe: 13,76 € los 16 GB, todos los meses. Pero ese precio tiene "
              "truco: su gama Budget <strong>no trae copias de seguridad</strong> y "
              "monta un Ryzen 7 5700X con DDR4 a 2133 MHz. Godlike está en el otro "
              "lado: Ryzen de última generación hasta el 9950X3D, NVMe, hasta tres "
              "copias al día y la posibilidad de <strong>elegir los días</strong> que "
              "pagas. Lo que cuesta: 38,24 € los 16 GB con el código, casi el triple que "
              "Pebble, eso sí todos los meses y no solo el primero. Para un servidor de "
              "todo el año y gastar lo mínimo, Pebble. Para "
              "un modpack pesado de unos meses, donde un corte o un procesador lento "
              "te arruinan la partida, Godlike.",
  ),
  dict(
    a="godlike", b="dathost",
    gana_a="Es un servidor de temporada, quieres el mejor procesador, o necesitas "
           "menos de 16 GB.",
    gana_b="Vas a tener 16 GB encendidos todo el año y quieres pagar lo mínimo.",
    veredicto="Los dos van a por la gente que quiere que el servidor vaya fino, pero "
              "lo cobran de forma opuesta. DatHost tiene un solo plan: 16 GB con "
              "Ryzen 9 7950X y plazas ilimitadas por 14,90 € al mes, pase lo que pase. "
              "Godlike te deja montarte el plan — gigas, plazas y días —, monta Ryzen "
              "de una generación posterior, hasta el 9950X3D, y te da hasta tres copias "
              "al día. La diferencia está en la factura: sus 16 GB son 50,99 € al mes "
              "de tarifa (40,58 € pagando el año), más del triple que DatHost. Así que "
              "para 16 GB todo el año, DatHost. Para un modpack de unos meses, para "
              "servidores más pequeños o si quieres el procesador más rápido, Godlike.",
  ),
  dict(
    a="shockbyte", b="bisect",
    gana_a="Casi en todo: es más barato por gigabyte en todos los tamaños.",
    gana_b="Prefieres facturación en euros y soporte en español.",
    veredicto="Duelo entre dos que cobran por gigabyte. Shockbyte sale más barato "
              "en todos los tramos; Bisect gana en "
              "comodidad para el mercado español. Quédate con el que más te encaje.",
  ),
]


def _tabla(dueloA, dueloB, d):
    """Precio de cada uno en Minecraft, en varios tamaños de RAM."""
    cambio = d["cambioUsdEur"]

    def celdas(hid):
        out = []
        for gb in GB_REF:
            h = next(x for x in d["hosts"] if x["id"] == hid)
            precio, etiqueta = precio_para(h, "minecraft", gb, cambio)
            # La etiqueta se enseña cuando NO son gigas normales: Realms no se
            # vende por RAM, sino por plazas.
            # Sin decirlo, la tabla parece que miente.
            extra = ("<small>%s</small>" % etiqueta
                     if etiqueta and etiqueta != "%d GB" % gb else "")
            out.append(('<td class="price">%s%s</td>' % (eur(precio), extra))
                       if precio else '<td class="nd">no llega</td>')
        return "".join(out)

    # Si alguno de los dos vive de un descuento de entrada, se dice aqui mismo:
    # es media tabla de diferencia y aparece en letra pequena en su web.
    avisos = []
    for hid in (dueloA, dueloB):
        h = next(x for x in d["hosts"] if x["id"] == hid)
        e = h["precios"]["minecraft"].get("entrada")
        if e:
            # con 8 GB si llega; si no (GPORTAL se queda en 6), con su mayor plan
            for gb_ref in (8, 6, 4, 2):
                mes, entrada, ano = coste_primer_ano(h, gb_ref, cambio)
                if mes is not None:
                    break
            if mes is None:
                continue
            avisos.append("<strong>%s</strong> deja %s en %s para un servidor de %d GB, "
                          "y después son %s al mes: %s el primer año."
                          % (h["nombre"], e["que"], eur(entrada), gb_ref, eur(mes), eur(ano)))
    aviso = ('<p class="tbl-note">%s</p>' % " ".join(avisos)) if avisos else ""

    cab = "".join("<th>%d GB</th>" % g for g in GB_REF)
    return ('<div class="table-wrap"><table class="tabla-maestra ordenable">\n'
            '<thead><tr><th>Hosting</th>%s</tr></thead>\n<tbody>\n'
            '<tr%s><td>%s<small>%s</small></td>%s</tr>\n'
            '<tr%s><td>%s<small>%s</small></td>%s</tr>\n'
            '</tbody></table></div>\n'
            '<p class="tbl-note">Precio mensual recurrente en Minecraft, en euros. '
            'Comprobado a mano el %s.</p>'
            % (cab,
               ' class="hl"' if partner.es_partner(dueloA) else "",
               FICHAS[dueloA]["nombre"], FICHAS[dueloA]["pais"], celdas(dueloA),
               ' class="hl"' if partner.es_partner(dueloB) else "",
               FICHAS[dueloB]["nombre"], FICHAS[dueloB]["pais"], celdas(dueloB),
               d["comprobado"])) + aviso


# ---------------------------------------------------------------------------
# EL MARCADOR VISUAL
# Antes esto era una tabla y ya está: dos filas de números. Quien busca
# "X vs Y" quiere ver de un vistazo quién gana, así que primero va el cara a
# cara grande y un marcador fila a fila, y la tabla detallada se queda debajo.
# ---------------------------------------------------------------------------

def _precio(h, gb, cambio):
    p, etiqueta = precio_para(h, "minecraft", gb, cambio)
    return p, etiqueta


def _host(d, hid):
    return next(x for x in d["hosts"] if x["id"] == hid)


def bloque_versus(aid, bid, d, T, fichas=None):
    """Cabecera enfrentada + marcador. T trae los textos del idioma, y
    `fichas` las de ese idioma (el pais viene traducido en ellas)."""
    fichas = fichas or {}
    cambio = d["cambioUsdEur"]
    A, B = FICHAS[aid], FICHAS[bid]
    ha, hb = _host(d, aid), _host(d, bid)

    # Tamaño de referencia: el mayor que sirvan los dos (GPORTAL se queda en 6)
    ref = None
    for gb in (8, 6, 4, 2):
        if _precio(ha, gb, cambio)[0] and _precio(hb, gb, cambio)[0]:
            ref = gb
            break

    filas, puntos = [], {aid: 0, bid: 0}

    def fila(etiqueta, va, vb, na=None, nb=None, menor_gana=True):
        """Una fila del marcador. na/nb son los números con los que se compara."""
        ga = gb_ = ""
        if na is not None and nb is not None and na != nb:
            gana_a = na < nb if menor_gana else na > nb
            if gana_a:
                ga, puntos[aid] = " gana", puntos[aid] + 1
            else:
                gb_, puntos[bid] = " gana", puntos[bid] + 1
        filas.append('        <div class="vs-fila">'
                     '<b class="vs-val%s">%s</b>'
                     '<span class="vs-crit">%s</span>'
                     '<b class="vs-val%s">%s</b></div>' % (ga, va, etiqueta, gb_, vb))

    for gb in GB_REF:
        pa, ea = _precio(ha, gb, cambio)
        pb, eb = _precio(hb, gb, cambio)
        va = (eur(pa) + (("<small>%s</small>" % ea) if ea and ea != "%d GB" % gb else "")) if pa else '<i>%s</i>' % T["no"]
        vb = (eur(pb) + (("<small>%s</small>" % eb) if eb and eb != "%d GB" % gb else "")) if pb else '<i>%s</i>' % T["no"]
        fila(T["mes"] % gb, va, vb, pa if (pa and pb) else None, pb if (pa and pb) else None)

    if ref:
        pa = _precio(ha, ref, cambio)[0]
        pb = _precio(hb, ref, cambio)[0]
        fila(T["por_gb"] % ref, eur(pa / ref), eur(pb / ref), pa / ref, pb / ref)

        ma, ent_a, ano_a = coste_primer_ano(ha, ref, cambio)
        mb, ent_b, ano_b = coste_primer_ano(hb, ref, cambio)
        if ent_a is not None and ent_b is not None:
            fila(T["primer_pago"] % ref, eur(ent_a), eur(ent_b), ent_a, ent_b)
        if ano_a is not None and ano_b is not None:
            fila(T["primer_ano"] % ref, eur(ano_a), eur(ano_b), ano_a, ano_b)

    fila(T["desde"], A.get("desde_ano") or "&mdash;", B.get("desde_ano") or "&mdash;")
    fila(T["ubic"], A.get("ubicaciones") or "&mdash;", B.get("ubicaciones") or "&mdash;")

    # Tanteo: solo cuenta lo que se puede medir, y se dice cuántas son
    total = puntos[aid] + puntos[bid]
    if total and puntos[aid] != puntos[bid]:
        lider = A if puntos[aid] > puntos[bid] else B
        tanteo = '<p class="vs-tanteo">%s</p>' % (T["tanteo"] % (
            lider["nombre"], max(puntos.values()), total))
    else:
        tanteo = '<p class="vs-tanteo">%s</p>' % T["empate"] if total else ""

    def lado(F, h, clase):
        p, etiqueta = _precio(h, ref, cambio) if ref else (None, None)
        grande = ('<p class="vs-big"><b>%s</b><small>%s</small></p>'
                  % (eur(p), T["mes"] % ref)) if p else ""
        e = h["precios"]["minecraft"].get("entrada")
        entrada = ""
        if e and p:
            _, ent, _a = coste_primer_ano(h, ref, cambio)
            if ent is not None:
                entrada = ('<p class="vs-entrada">&minus;%d %%%s &rarr; <b>%s</b></p>'
                           % (e["pct"], " " + (e.get(T["que_key"]) or ""), eur(ent)))
        pais = (fichas.get(h["id"]) or {}).get("pais") or F["pais"]
        return ('    <article class="vs-lado%(cl)s">\n'
                '      <p class="vs-nom">%(n)s</p>\n'
                '      <p class="vs-pais">%(pais)s</p>\n'
                '%(grande)s%(entrada)s'
                '      <a class="cta-mini" href="%(pre)s/hosting/%(u)s/">%(ficha)s</a>\n'
                '    </article>' % dict(cl=clase, n=F["nombre"], pais=pais,
                                        grande=grande, entrada=entrada,
                                        pre=T["pre"], u=F["url"], ficha=T["ficha"]))

    hl_a = " vs-partner" if partner.es_partner(aid) else ""
    hl_b = " vs-partner" if partner.es_partner(bid) else ""
    return ('  <section class="vs-hero">\n%s\n'
            '    <div class="vs-bola" aria-hidden="true">VS</div>\n%s\n  </section>\n'
            '%s\n  <div class="vs-marcador">\n%s\n  </div>\n'
            '  <p class="tbl-note">%s</p>\n'
            % (lado(A, ha, hl_a), lado(B, hb, hl_b), tanteo, "\n".join(filas),
               T["nota"]))


T_ES = dict(
    mes="%d GB al mes", por_gb="Precio por GB (con %d GB)",
    primer_pago="Lo que pagas el primer mes (%d GB)",
    primer_ano="Lo que llevas gastado al año (%d GB)",
    desde="En el mercado desde", ubic="Ubicaciones", no="no llega",
    ficha="Ver ficha", pre="", que_key="que",
    tanteo="<b>%s</b> gana en %d de las %d cosas que se pueden medir.",
    nota=("El marcador solo cuenta lo que se puede poner en euros. Lo que no se "
          "mide en dinero &mdash; si admite mods, cuánta gente entra, las copias "
          "de seguridad o el procesador &mdash; está en el veredicto de abajo."),
    card_pie="%d GB: %s contra %s",
    empate="Empate técnico: ganan a lo mismo.",
)


def url_de(duelo):
    return "%s-vs-%s" % (FICHAS[duelo["a"]]["url"], FICHAS[duelo["b"]]["url"])


def html(duelo, d):
    A, B = FICHAS[duelo["a"]], FICHAS[duelo["b"]]
    ruta = "/versus/%s/" % url_de(duelo)
    titulo = "%s vs %s: cuál te conviene en 2026" % (A["nombre"], B["nombre"])
    desc = ("Comparativa cara a cara de %s y %s con precios reales comprobados a mano. "
            "Cuándo gana cada uno y por qué." % (A["nombre"], B["nombre"]))

    # Boton de contratar solo si el partner configurado juega este duelo.
    cta = ""
    for lado in (duelo["a"], duelo["b"]):
        if partner.es_partner(lado):
            cta = partner.boton("minecraft", "DUELO", "Ir a %s" % FICHAS[lado]["nombre"])
    cta = cta or '<a class="cta" href="/">Calcular mi servidor</a>'

    faq = json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": "¿Qué es mejor, %s o %s?" % (A["nombre"], B["nombre"]),
             "acceptedAnswer": {"@type": "Answer",
                                "text": duelo["veredicto"].replace("<strong>", "").replace("</strong>", "")}},
        ],
    }, ensure_ascii=False, indent=2)

    return """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(titulo)s</title>
<meta name="description" content="%(desc)s">
<link rel="canonical" href="%(dom)s%(ruta)s">
<meta property="og:type" content="article">
<meta property="og:site_name" content="MontaTuServer">
<meta property="og:url" content="%(dom)s%(ruta)s">
<meta property="og:title" content="%(titulo)s">
<meta property="og:description" content="%(desc)s">
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
    <nav class="miga"><a href="/">Inicio</a> › <a href="/hosting/">Hostings</a> › %(na)s vs %(nb)s</nav>

    <h1>%(na)s <em>vs</em> %(nb)s</h1>
    <p class="sub art-sub">Cara a cara con los precios comprobados a mano y un
      veredicto claro: quién gana, en qué, y cuándo compensa el otro.</p>
    <p class="art-meta">Actualizado el %(comprobado)s</p>

%(versus)s

    <h2 id="precios">Todos los precios, uno al lado del otro</h2>
%(tabla)s

    <h2 id="cuando">Cuándo gana cada uno</h2>
    <div class="duelo">
      <div class="duelo-lado gana-a">
        <span class="duelo-tag">Elige %(na)s si…</span>
        <p>%(gana_a)s</p>
        <a class="cta-mini" href="/hosting/%(ua)s/">Ver ficha de %(na)s</a>
      </div>
      <div class="duelo-vs" aria-hidden="true">vs</div>
      <div class="duelo-lado gana-b">
        <span class="duelo-tag">Elige %(nb)s si…</span>
        <p>%(gana_b)s</p>
        <a class="cta-mini" href="/hosting/%(ub)s/">Ver ficha de %(nb)s</a>
      </div>
    </div>

    <h2 id="veredicto">Mi veredicto</h2>
    <p class="veredicto-final">%(veredicto)s</p>

    <div class="art-cta">
      <h3>¿Y para tu caso concreto?</h3>
      <p>
        El ganador cambia por completo según cuánta RAM necesites. Dime cuántos
        sois y qué lleváis instalado y te lo digo en 20 segundos, con los dos
        comparados y con el resto.
      </p>
      <div class="hero-cta">
        <a class="cta-ghost" href="/">Calcular mis GB</a>
        %(cta)s
      </div>
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

<script src="/buscador_ui.js" defer></script>
<script src="/tabla_ui.js" defer></script>
<script type="application/ld+json">
%(faq)s
</script>
<script type="application/ld+json">
%(migas)s
</script>
</body>
</html>
""" % dict(titulo=titulo, desc=desc, dom=DOMINIO, ruta=ruta,
           divulgacion=partner.divulgacion(),
           na=A["nombre"], nb=B["nombre"], ua=A["url"], ub=B["url"],
           comprobado=d["comprobado"], tabla=_tabla(duelo["a"], duelo["b"], d),
           versus=bloque_versus(duelo["a"], duelo["b"], d, T_ES),
           gana_a=duelo["gana_a"], gana_b=duelo["gana_b"],
           veredicto=duelo["veredicto"], cta=cta, faq=faq,
           migas=migas.schema([("Inicio", "/"), ("Versus", "/versus/"),
                               ("%s vs %s" % (A["nombre"], B["nombre"]), None)]))


def _pie_card(x, d, T=None):
    """Lo que va debajo de cada tarjeta: los dos precios y quién es más barato."""
    T = T or T_ES
    cambio = d["cambioUsdEur"]
    ha, hb = _host(d, x["a"]), _host(d, x["b"])
    for gb in (8, 6, 4, 2):
        pa = _precio(ha, gb, cambio)[0]
        pb = _precio(hb, gb, cambio)[0]
        if pa and pb:
            return T["card_pie"] % (gb, eur(pa), eur(pb))
    return ""


def indice(d):
    """La página /versus/ que lista todos los duelos."""
    filas = []
    for x in DUELOS:
        A, B = FICHAS[x["a"]], FICHAS[x["b"]]
        filas.append(
            '      <a class="vs-card" href="/versus/%s/">'
            '<span class="vs-card-a">%s</span>'
            '<span class="vs-card-vs" aria-hidden="true">VS</span>'
            '<span class="vs-card-b">%s</span>'
            '<span class="vs-card-pie">%s</span></a>'
            % (url_de(x), A["nombre"], B["nombre"], _pie_card(x, d)))

    return """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Versus: hostings de Minecraft cara a cara (2026)</title>
<meta name="description" content="Godlike.host vs Apex, vs Shockbyte, vs PebbleHost… Comparativas cara a cara de hostings de Minecraft con precios reales y un veredicto claro.">
<link rel="canonical" href="%(dom)s/versus/">
<meta property="og:type" content="website">
<meta property="og:url" content="%(dom)s/versus/">
<meta property="og:title" content="Versus: hostings de Minecraft cara a cara">
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
    <nav class="miga"><a href="/">Inicio</a> › Versus</nav>
    <h1><em>Versus</em>: hosting contra hosting</h1>
    <p class="sub art-sub">
      Los enfrentamientos que más se buscan, con los precios uno al lado del otro
      y un veredicto de cuándo gana cada uno.
    </p>
    <div class="vs-cards">
%(filas)s
    </div>
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
</body>
</html>
""" % dict(dom=DOMINIO, filas="\n".join(filas), comprobado=d["comprobado"])
