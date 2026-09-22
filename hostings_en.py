# -*- coding: utf-8 -*-
"""
English host pages: /en/hosting/ and /en/hosting/<host>/.

Same numbers as the Spanish pages — the prices come from the same functions
(precio_para, coste_primer_ano) and the same hosts.js. Only the text changes,
and it lives in fichas_en.py.

Imported by build.py.
"""

import json

from comparativas import precio_para, coste_primer_ano
import hostings
import historico
import migas
import partner
from fichas_en import FICHAS_EN

DOMINIO = "https://montatuserver.com"
FUENTES = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
           '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
           '<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700'
           '&family=Inter:wght@400..800&display=swap" rel="stylesheet">')


def eur(n):
    return "€%.2f" % n


def modelo_texto(pr, h, cambio):
    aEur = (lambda v: v * cambio) if h["moneda"] == "USD" else (lambda v: v)
    if pr["modelo"] == "porGB":
        return "%s per GB" % eur(aEur(pr["porGB"]))
    if pr["modelo"] == "tabla":
        return "RAM tiers"
    if pr["modelo"] == "slots":
        return "By slots, no RAM published"
    if pr["modelo"] == "plano":
        que = "%d slots" % pr["slots"] if pr.get("slots") else "%d GB" % pr["ram"]
        return "Single %s plan" % que
    return "—"


def _cambio_en(frase):
    """historico.cambio() speaks Spanish; translate its one sentence."""
    if not frase:
        return ""
    import re
    m = re.match(r"Su plan de 8 GB (ha subido|ha bajado): el (\d+) de (\w+) costaba ([\d,]+) € y ahora son ([\d,]+) €\.", frase)
    if not m:
        return ""
    meses = dict(zip(historico.MESES, ["January", "February", "March", "April", "May", "June",
                                       "July", "August", "September", "October", "November", "December"]))
    verbo = "went up" if m.group(1) == "ha subido" else "went down"
    a = m.group(4).replace(",", "."); b = m.group(5).replace(",", ".")
    return "Their 8 GB plan %s: on %s %s it cost €%s and now it's €%s." % (
        verbo, m.group(2), meses.get(m.group(3), m.group(3)), a, b)


def tabla_precios(host_id, d):
    cambio = d["cambioUsdEur"]
    h = next(x for x in d["hosts"] if x["id"] == host_id)
    celdas = []
    for gb in hostings.GB_TABLA:
        precio, da = precio_para(h, "minecraft", gb, cambio)
        if precio is None:
            celdas.append('<td class="nd">not available</td>')
        else:
            extra = ("<small>gives you %s</small>" % da) if da != "%d GB" % gb else ""
            celdas.append('<td class="price">%s%s</td>' % (eur(precio), extra))
    pr = h["precios"]["minecraft"]

    frase = _cambio_en(historico.cambio(host_id, h["moneda"], cambio))
    aviso = ('<p class="tbl-note">📉 %s</p>' % frase) if frase else ""

    if pr.get("entrada"):
        mes = entrada = ano = None
        for gb_ref in (8, 6, 4, 2):
            mes, entrada, ano = coste_primer_ano(h, gb_ref, cambio)
            if mes is not None:
                break
        if mes is not None:
            aviso = ('<p class="tbl-note"><strong>Mind the entry discount.</strong> A %d GB '
                     'server starts at %s for %s, then it\'s %s a month: '
                     '<strong>%s for the first year</strong>.</p>'
                     % (gb_ref, eur(entrada), pr["entrada"].get("que_en", pr["entrada"]["que"]),
                        eur(mes), eur(ano)))

    return (aviso + '<div class="table-wrap">\n<table class="tabla-maestra">\n'
            '<thead><tr><th>Plan</th>%s</tr></thead>\n'
            '<tbody>\n<tr><td>%s<small>%s</small></td>%s</tr>\n</tbody>\n</table>\n</div>\n'
            '<p class="tbl-note">Monthly price in euros. Hosts that charge in dollars are '
            'converted at $1&nbsp;=&nbsp;€%s.</p>'
            % ("".join("<th>%d GB</th>" % gb for gb in hostings.GB_TABLA),
               modelo_texto(pr, h, cambio), pr.get("nota_en", pr["nota"]), "".join(celdas),
               cambio))


def html(host_id, d):
    f = hostings.FICHAS[host_id]
    t = FICHAS_EN[host_id]
    h = next(x for x in d["hosts"] if x["id"] == host_id)
    cambio = d["cambioUsdEur"]
    ruta = "/en/hosting/%s/" % f["url"]
    lista = lambda items, cls: "\n".join('        <li class="%s">%s</li>' % (cls, x) for x in items)

    aviso = precio_final = ""
    if partner.es_partner(host_id):
        aviso = ('<div class="indep" style="margin-bottom:20px">'
                 '<span class="indep-ico">💶</span><p><strong>Heads up: I do earn a '
                 'commission with this host.</strong> That\'s why the downsides below are '
                 'written as carefully as everyone else\'s, and in the tables it sits where '
                 'its price puts it, not higher.</p></div>')
        cfg = partner.config()
        razones = cfg.get("razones_en") or []
        razones_html = ('<ul class="pf-razones">%s</ul>' % "".join("<li>%s</li>" % r for r in razones)
                        if razones else "")
        codigo = ('<p class="pf-pie">Discount code: <strong>%s</strong></p>' % cfg["codigo"]
                  if cfg.get("codigo") else "")
        precio_final = """
    <div class="precio-final" style="border-top:0;padding-top:0">
      %s
      %s
      <div class="cta-row">
        %s
        <p class="cta-fine">%s</p>
      </div>
    </div>""" % (razones_html, codigo, partner.boton("minecraft", "FICHA-EN", "Go to %s" % f["nombre"]),
                 partner.aviso_boton_en())

    faq_schema = json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": "How much does %s cost?" % f["nombre"],
             "acceptedAnswer": {"@type": "Answer", "text": t["resumen"]}},
            {"@type": "Question", "name": "Is %s worth it?" % f["nombre"],
             "acceptedAnswer": {"@type": "Answer", "text": t["veredicto"]}},
        ],
    }, ensure_ascii=False, indent=2)

    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(nombre)s for Minecraft: real prices and whether it's worth it (2026)</title>
<meta name="description" content="%(resumen)s Prices checked by hand, the good, the bad and when it's worth it.">
<link rel="canonical" href="%(dom)s%(ruta)s">
<meta property="og:type" content="article">
<meta property="og:site_name" content="MontaTuServer">
<meta property="og:url" content="%(dom)s%(ruta)s">
<meta property="og:title" content="%(nombre)s for Minecraft: real prices and whether it's worth it">
<meta property="og:description" content="%(resumen)s">
<meta property="og:image" content="%(dom)s/og-image.jpg">
<meta property="og:locale" content="en_GB">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
%(fuentes)s
<link rel="stylesheet" href="/styles.css">
</head>
<body>

<header class="site-head"></header>

<main>
  <article class="wrap articulo">

    <nav class="miga" aria-label="You are here">
      <a href="/en/">Home</a> › <a href="/en/hosting/">Hosts</a> › %(nombre)s
    </nav>

    <h1>%(nombre)s</h1>
    <p class="sub art-sub">%(resumen)s</p>
    <div class="ficha-datos">
      <div><span>Based in</span><b>%(pais)s</b></div>
      <div><span>Since</span><b>%(desde_ano)s</b></div>
      <div><span>Locations</span><b>%(ubicaciones)s</b></div>
      <div><span>Pricing</span><b>%(modelo)s</b></div>
    </div>
    <div class="ficha-rasgos">%(rasgos)s</div>
    <p class="art-meta">Prices checked on %(comprobado)s</p>

    %(aviso)s

    <h2 id="precios">What it charges for Minecraft</h2>
    <p>
      What you pay each month depending on the gigabytes you need. If you don't know
      how many, the calculator tells you in 20 seconds.
    </p>
%(tabla)s

    <h2 id="bueno">The good</h2>
    <ul class="lista-si">
%(bueno)s
    </ul>

    <h2 id="malo">The catches</h2>
    <ul class="lista-no">
%(malo)s
    </ul>

    <h2 id="veredicto">Verdict</h2>
    <p class="veredicto-final">%(veredicto)s</p>

    %(precio_final)s

    <div class="art-cta">
      <h3>Is it the best for you?</h3>
      <p>
        It depends on how much RAM you need, and that changes the winner completely.
        Tell me how many of you there are and what you've installed, and I'll tell you
        in 20 seconds, with %(nombre)s compared side by side with the rest.
      </p>
      <a class="cta" href="/en/">Calculate and compare</a>
    </div>

  </article>
</main>

<footer></footer>

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
        nombre=f["nombre"], resumen=t["resumen"], pais=t["pais"], veredicto=t["veredicto"],
        dom=DOMINIO, ruta=ruta, fuentes=FUENTES, precio_final=precio_final,
        desde_ano=f.get("desde_ano", "—"), ubicaciones=f.get("ubicaciones", "—"),
        modelo=modelo_texto(h["precios"]["minecraft"], h, cambio),
        rasgos="".join('<span class="rasgo">%s</span>' % r for r in t.get("rasgos", [])),
        comprobado=d.get("comprobado_en", d["comprobado"]), aviso=aviso,
        tabla=tabla_precios(host_id, d),
        bueno=lista(t["bueno"], "si"), malo=lista(t["malo"], "no"),
        faq_schema=faq_schema,
        migas=migas.schema([("Home", "/en/"), ("Hosts", "/en/hosting/"), (f["nombre"], None)]),
    )


def indice(d):
    cambio = d["cambioUsdEur"]
    filas = []
    for hid, f in hostings.FICHAS.items():
        h = next(x for x in d["hosts"] if x["id"] == hid)
        pares = [precio_para(h, "minecraft", gb, cambio) for gb in (4, 8, 16)]
        porgb = None
        for gb_ref in (8, 6, 4, 2):
            precio_ref, da_ref = precio_para(h, "minecraft", gb_ref, cambio)
            if precio_ref is None or not (da_ref or "").endswith("GB"):
                continue
            try:
                porgb = precio_ref / int(da_ref.split()[0])
            except ValueError:
                continue
            break
        filas.append((hid, f, h, porgb, pares))
    filas.sort(key=lambda x: (x[3] is None, x[3] or 0))

    tabla = []
    for hid, f, h, porgb, pares in filas:
        pr = h["precios"]["minecraft"]
        destacado = ' class="hl"' if partner.es_partner(hid) else ""
        celdas = "".join(
            ('<td class="price">%s%s</td>'
             % (eur(p), ("<small>gives you %s</small>" % da) if da and not da.endswith("GB") else ""))
            if p is not None else '<td class="nd">not available</td>'
            for p, da in pares)
        celdas += (('<td class="price">%s</td>' % eur(porgb)) if porgb is not None
                   else '<td class="nd">—</td>')
        tabla.append(
            '      <tr%s data-modelo="%s" data-porgb="%s" data-entrada="%s">\n'
            '        <td><a href="/en/hosting/%s/">%s</a><small>%s</small></td>\n'
            '        <td>%s</td>\n        %s\n'
            '        <td><a class="cta-mini" href="/en/hosting/%s/">Review</a></td>\n'
            '      </tr>'
            % (destacado, pr["modelo"], ("%.2f" % porgb) if porgb else "",
               "si" if pr.get("entrada") else "no", f["url"], f["nombre"],
               FICHAS_EN[hid]["pais"], modelo_texto(pr, h, cambio), celdas, f["url"]))

    indep = ""
    if partner.activo():
        indep = ('    <div class="indep" style="margin:22px 0">\n'
                 '      <span class="indep-ico" aria-hidden="true">⚖️</span>\n'
                 '      <p><strong>I only have an affiliate deal with one of these: %s.</strong> '
                 "I earn nothing from the rest, and they're still here with their real prices "
                 'and their strengths. In the table it sits where its price puts it.</p>\n'
                 '    </div>\n' % partner.nombre())

    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Minecraft hosts reviewed one by one (2026)</title>
<meta name="description" content="Reviews of the main Minecraft hosts: real prices checked by hand, the good, the catches and when each one is worth it.">
<link rel="canonical" href="%(dom)s/en/hosting/">
<meta property="og:type" content="website">
<meta property="og:url" content="%(dom)s/en/hosting/">
<meta property="og:title" content="Minecraft hosts reviewed one by one">
<meta property="og:image" content="%(dom)s/og-image.jpg">
<meta property="og:locale" content="en_GB">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
%(fuentes)s
<link rel="stylesheet" href="/styles.css">
</head>
<body>

<header class="site-head"></header>

<main>
  <div class="wrap articulo">
    <nav class="miga"><a href="/en/">Home</a> › Hosts</nav>
<h1>Minecraft hosts, one by one</h1>
    <p class="sub art-sub">
      What each one charges for 4, 8 and 16 GB, and its review with the good and the catches.
    </p>

%(indep)s
    <div class="filtros" id="filtros" role="group" aria-label="Filter the table"></div>
    <div class="table-wrap">
      <table class="tabla-maestra ordenable" data-filtrable>
        <thead><tr>
          <th>Host</th><th>Pricing</th><th>4 GB</th><th>8 GB</th><th>16 GB</th>
          <th>Per GB</th><th></th>
        </tr></thead>
        <tbody>
%(tabla)s
        </tbody>
      </table>
    </div>
    <p class="tbl-note">
      Monthly price in euros. Sorted by the <strong>“Per GB”</strong> column, which is
      what each gigabyte costs on their 8 GB plan: the way to compare fixed plans with
      pay-per-gigabyte hosts, like the price per kilo at the supermarket. If a plan gives
      you more than you asked for, the maths counts the GB you get, not the ones you
      asked for. Click any column to sort by it.
    </p>

    <div class="art-cta" style="margin-top:30px">
      <h3>What about ping from Spain?</h3>
      <p>
        Price isn't the only thing that changes between them: where their machines are
        changes too. None of them are in Spain, and picking the right location or not
        is a 100-millisecond difference.
      </p>
    </div>

    <p class="art-meta">Prices checked on %(comprobado)s.</p>
  </div>
</main>

<footer></footer>

<script src="/buscador_ui.js" defer></script>
<script src="/tabla_ui.js" defer></script>
<script src="/filtros_ui.js" defer></script>

</body>
</html>
""" % dict(dom=DOMINIO, fuentes=FUENTES, indep=indep, tabla="\n".join(tabla),
           comprobado=d.get("comprobado_en", d["comprobado"]))
