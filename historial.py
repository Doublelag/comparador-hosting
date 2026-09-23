# -*- coding: utf-8 -*-
"""
Historial de precios: /precios/ y /en/price-history/.

Por qué existe: en idealo o en los comparadores de vuelos, el gráfico de "cómo
ha ido el precio" es de lo más consultado, porque responde a la pregunta de
verdad: ¿esto está caro ahora o es lo normal? En hosting no lo enseña nadie,
entre otras cosas porque casi todos los comparadores del sector son de una
empresa de hosting.

La honestidad de esta página está en el encabezado: dice desde cuándo se sigue
y cuántos cambios se han visto. Si se ha visto uno, pone uno. Una página de
histórico que finge tener años de datos se cae sola en cuanto alguien mira.

Lo importa build.py.
"""

import io
import json
import os

import historico
import paginas

RAIZ = os.path.dirname(os.path.abspath(__file__))
MESES_EN = ["January", "February", "March", "April", "May", "June", "July",
            "August", "September", "October", "November", "December"]


def _fecha(iso, lang):
    a, m, d = iso.split("-")
    if lang == "es":
        return "%d de %s de %s" % (int(d), historico.MESES[int(m) - 1], a)
    return "%d %s %s" % (int(d), MESES_EN[int(m) - 1], a)


def cambios(d):
    """Los cambios de precio de verdad, del más nuevo al más viejo.

    Solo cuentan los hostings que YA estaban en la foto anterior: cuando añado
    uno nuevo, eso no es una subida, es que antes no lo miraba.
    """
    archivo = os.path.join(RAIZ, "historico.json")
    if not os.path.exists(archivo):
        return []
    historia = json.loads(io.open(archivo, encoding="utf-8").read())
    cambio_usd = d["cambioUsdEur"]
    hosts = {h["id"]: h for h in d["hosts"]}
    fuera = []
    for i in range(1, len(historia)):
        antes, ahora = historia[i - 1]["precios"], historia[i]["precios"]
        for hid, v in ahora.items():
            if hid not in antes or antes[hid] == v or hid not in hosts:
                continue
            a = historico._precio8(antes[hid], cambio_usd)
            b = historico._precio8(v, cambio_usd)
            if a is None or b is None or abs(a - b) < 0.01:
                continue
            moneda = hosts[hid].get("moneda")
            if moneda == "USD":
                a, b = a * cambio_usd, b * cambio_usd
            fuera.append(dict(fecha=historia[i]["fecha"], id=hid,
                              nombre=hosts[hid]["nombre"], ficha=hosts[hid].get("ficha"),
                              antes=a, ahora=b, pct=(b - a) / a * 100))
    fuera.reverse()
    return fuera


def _filas(lista, lang):
    from hostings import eur
    out = []
    for c in lista:
        sube = c["ahora"] > c["antes"]
        flecha = "&#9650;" if sube else "&#9660;"
        clase = "sube" if sube else "baja"
        out.append(
            '        <tr>\n'
            '          <td>%s</td>\n'
            '          <td><a href="%s%s">%s</a></td>\n'
            '          <td class="price">%s</td>\n'
            '          <td class="price">%s</td>\n'
            '          <td class="hist-%s">%s %+.1f %%</td>\n'
            '        </tr>'
            % (_fecha(c["fecha"], lang),
               ("/en" if lang == "en" else ""), c["ficha"] or "/hosting/", c["nombre"],
               eur(c["antes"]), eur(c["ahora"]), clase, flecha, c["pct"]))
    return "\n".join(out)


def html(lang, d):
    lista = cambios(d)
    desde = "9 de septiembre de 2026" if lang == "es" else "9 September 2026"
    if lang == "es":
        vacio = ("<p class=\"hist-vacio\">Desde que lo sigo no ha cambiado ningún precio. "
                 "En cuanto alguno se mueva, sale aquí con la fecha.</p>")
        tabla = vacio if not lista else """    <div class="table-wrap">
      <table class="tabla-maestra">
        <thead><tr><th>Cuándo</th><th>Hosting</th><th>Antes</th><th>Ahora</th><th>Cambio</th></tr></thead>
        <tbody>
%s
        </tbody>
      </table>
    </div>""" % _filas(lista, lang)
        cuerpo = """  <article class="wrap articulo" style="max-width:900px">
    <nav class="miga"><a href="/">Inicio</a> &rsaquo; Historial de precios</nav>

    <span class="sec-eyebrow">Historial</span>
    <h1>Cuándo <em>sube</em> cada hosting</h1>
    <p class="sub art-sub">
      Guardo los precios cada vez que los compruebo, así que cuando uno sube, queda
      apuntado con la fecha. Es lo que ningún comparador del sector enseña, porque casi
      todos son de una empresa de hosting.
    </p>
    <p class="art-meta">Siguiendo precios desde el %(desde)s &middot; %(n)d cambio%(s)s apuntado%(s)s</p>

%(tabla)s

    <h2>Cómo leer esto</h2>
    <ul>
      <li>La comparación es siempre sobre <strong>el plan de 8 GB</strong>, que es el caso
        más común, y en euros.</li>
      <li>Un hosting nuevo en la tabla del comparador <strong>no cuenta como cambio</strong>:
        que yo empiece a mirarlo no significa que haya subido.</li>
      <li>Los céntimos de diferencia en los que cobran en dólares pueden venir del cambio
        de divisa, no de una subida suya. El cambio usado está en las tablas.</li>
    </ul>

    <div class="art-cta" style="margin-top:30px">
      <h3>Lo que importa hoy</h3>
      <p>El histórico dice si algo está caro; la calculadora dice cuánto necesitas y quién
        te lo da más barato ahora mismo.</p>
      <div class="hero-cta">
        <a class="cta" href="/#calculadora">Calcular mi servidor</a>
        <a class="cta-ghost" href="/como-lo-compruebo/">Cómo compruebo los precios</a>
      </div>
    </div>
  </article>"""
        return paginas.pagina(
            "es", "/precios/", "Historial de precios de los hostings de Minecraft",
            "Cada vez que un hosting de Minecraft sube o baja sus precios, queda apuntado "
            "con la fecha. El histórico que no enseña nadie en el sector.",
            cuerpo % dict(tabla=tabla, desde=desde, n=len(lista),
                          s="" if len(lista) == 1 else "s"))

    vacio = ("<p class=\"hist-vacio\">No price has changed since I started tracking. "
             "The moment one moves, it shows up here with the date.</p>")
    tabla = vacio if not lista else """    <div class="table-wrap">
      <table class="tabla-maestra">
        <thead><tr><th>When</th><th>Host</th><th>Before</th><th>Now</th><th>Change</th></tr></thead>
        <tbody>
%s
        </tbody>
      </table>
    </div>""" % _filas(lista, lang)
    cuerpo = """  <article class="wrap articulo" style="max-width:900px">
    <nav class="miga"><a href="/en/">Home</a> &rsaquo; Price history</nav>

    <span class="sec-eyebrow">History</span>
    <h1>When each host <em>puts prices up</em></h1>
    <p class="sub art-sub">
      I save prices every time I check them, so when one goes up, it's logged with the
      date. No comparison site in this industry shows this, mostly because nearly all of
      them belong to a hosting company.
    </p>
    <p class="art-meta">Tracking prices since %(desde)s &middot; %(n)d change%(s)s logged</p>

%(tabla)s

    <h2>How to read this</h2>
    <ul>
      <li>The comparison is always on <strong>the 8 GB plan</strong>, the most common case,
        in euros.</li>
      <li>A new host appearing in the comparison <strong>doesn't count as a change</strong>:
        me starting to track it doesn't mean they put prices up.</li>
      <li>A few cents' difference on hosts that charge in dollars can come from the exchange
        rate, not from them. The rate used is printed in the tables.</li>
    </ul>

    <div class="art-cta" style="margin-top:30px">
      <h3>What matters today</h3>
      <p>The history tells you whether something is expensive; the calculator tells you how
        much you need and who gives it to you cheapest right now.</p>
      <div class="hero-cta">
        <a class="cta" href="/en/#calculadora">Size my server</a>
        <a class="cta-ghost" href="/en/how-i-check/">How I check the prices</a>
      </div>
    </div>
  </article>"""
    return paginas.pagina(
        "en", "/en/price-history/", "Minecraft hosting price history",
        "Every time a Minecraft host raises or lowers its prices, it gets logged with the "
        "date. The price history nobody in this industry shows.",
        cuerpo % dict(tabla=tabla, desde=desde, n=len(lista),
                      s="" if len(lista) == 1 else "s"))
