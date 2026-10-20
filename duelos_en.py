# -*- coding: utf-8 -*-
"""
English versus pages: /en/versus/ and /en/versus/<a>-vs-<b>/.

Same duels and same numbers as duelos.py; only the text is here. If a Spanish
verdict changes, change its English twin (same (a, b) key).

Imported by build.py.
"""

import json

from comparativas import precio_para, coste_primer_ano
from fichas_en import FICHAS_EN
from hostings import FICHAS
import duelos
import migas
import partner

DOMINIO = "https://montatuserver.com"
FUENTES = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
           '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
           '<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700'
           '&family=Inter:wght@400..800&display=swap" rel="stylesheet">')

TEXTOS = {
  ("godlike", "apex"): dict(
    gana_a="Almost always: your first payment is a quarter of the price, and on small "
           "or big servers it wins at the normal rate too.",
    gana_b="You want their one-click modpack catalogue or their dedicated vCores, and "
           "don't mind paying more.",
    veredicto="Apex is the best-known name in Minecraft hosting, and also one of the most "
              "expensive. Godlike beats it on almost everything you can measure. To start "
              "with, the code brings 16 GB down to €38.24 <strong>every month</strong>, while "
              "Apex asks €46.43 with a −25% deal that only covers the first one. And at the "
              "normal rate it holds its own too: €6.29 for 2 GB against €12.89, and €50.99 "
              "for 16 GB against €61.91. Only at 8 GB does it flip, and by less than two "
              "euros. Add that on Godlike you pick the days, get up to three backups a day "
              "and latest-gen Ryzen. Apex is only worth it if their modpack catalogue saves "
              "you an afternoon of setup.",
  ),
  ("godlike", "nodecraft"): dict(
    gana_a="On price, maximum size and the entry discount.",
    gana_b="You want the plan picked for you through a few questions and don't mind paying more.",
    veredicto="Not much of a contest here. Nodecraft rebuilt its site in September 2026 and "
              "went to $4.99 per GB: their 8 GB is €34.38 a month. Godlike asks €25.99 for "
              "the same 8 GB, and the first payment is €6.50. Nodecraft also stops at 12 GB, "
              "while Godlike goes up to 33. Both have a free trial, but Nodecraft's asks you "
              "to verify your phone. If you're torn between the two, Godlike.",
  ),
  ("godlike", "realms"): dict(
    gana_a="You want a single plugin, a single mod, or more than ten people.",
    gana_b="You're four friends playing vanilla and don't want to touch any settings.",
    veredicto="Realms is Mojang's official option: it costs $7.99 (€6.87), you subscribe "
              "from inside the game and it never breaks on updates. But it has two ceilings "
              "you can't pay your way past: <strong>no mods or plugins</strong>, and "
              "<strong>ten players</strong> at most. Godlike gives you a 2 GB server for "
              "€6.29 a month, less than Realms, with Paper, Forge, Fabric and all the plugins "
              "you want. If you ever want "
              "a modpack or there are more than ten of you, with Realms you'll have to move; "
              "with Godlike, you upgrade in two clicks.",
  ),
  ("godlike", "gportal"): dict(
    gana_a="You need more than 6 GB, or a latest-gen CPU.",
    gana_b="Your server fits in 2-4 GB and you'll run it all year.",
    veredicto="Both set up a modpack in a few clicks and have a good network in Europe. The "
              "difference is the ceiling and the entry price. GPORTAL <strong>stops at "
              "6 GB</strong>: not enough for a big modpack or a community. Godlike goes up to "
              "33. On price GPORTAL wins the small plans: €11.80 for 4 GB against €9.74 at "
              "Godlike with the code, which lands close, except GPORTAL's −25% is first "
              "period only and Godlike's never expires. So: a small server and you can "
              "find your way around, GPORTAL; more than 6 GB or you want it made easy, "
              "Godlike.",
  ),
  ("godlike", "bisect"): dict(
    gana_a="The server will run for a few months, or you want daily backups and to pick the days.",
    gana_b="You'll run it for more than four months and want a flat rate in euros.",
    veredicto="BisectHosting charges a straight line: €2.69 per GB, every month. Godlike "
              "costs more at the normal rate (€25.99 for 8 GB against €21.52), but its first "
              "purchase is a quarter of the price. Doing the maths with 8 GB, <strong>Godlike "
              "is cheaper for the first four months</strong>: €6.50 against €21.52 the first, "
              "and €84.47 against €86.08 after four. From the fifth, Bisect. So for a seasonal "
              "modpack, an event or something you don't know how long will last, Godlike; and "
              "you also pick the exact days and get up to three backups a day.",
  ),
  ("godlike", "shockbyte"): dict(
    gana_a="The server is for one or two months, or you want to pick the days and have daily backups.",
    gana_b="You'll run it for a long time and want the lower monthly rate of the two.",
    veredicto="Shockbyte is one of the best known and charges by RAM tiers: €19.26 for 8 GB "
              "with its discount already applied. Godlike is pricier at the normal rate, "
              "€25.99, but the first payment is €6.50 thanks to the <strong>biggest discount "
              "in the comparison</strong>. With 8 GB, the first two months cost €32.49 on "
              "Godlike and €38.52 on Shockbyte; by the third they're even. For a short-lived "
              "server, Godlike, with the bonus of paying only for the days you'll play. For "
              "one that runs for years, Shockbyte.",
  ),
  ("godlike", "hostinger"): dict(
    gana_a="You don't want to be tied in for two years, or the server is for a few months.",
    gana_b="You'll pay 24 months upfront and want a VPS to manage yourself.",
    veredicto="Hostinger advertises prices that look unbeatable, but to get them you "
              "<strong>pay 24 months upfront</strong>, and then it renews at almost double. "
              "It's also a VPS: you manage more things yourself. Godlike works the other way "
              "round: <strong>you choose how many days you pay for</strong>, from 30 to 360, "
              "with no lock-in, and the code takes 25% off every month. To try it out, "
              "for a season, or to "
              "avoid tying yourself for two years to something you don't know yet, Godlike. If "
              "you're sure you'll stay two years and can manage a server, Hostinger is cheaper "
              "in the long run.",
  ),
  ("godlike", "pebble-budget"): dict(
    gana_a="You'll play for a few weeks or months, you want backups, or the modpack needs a fast CPU.",
    gana_b="The server will last and you want to pay as little as possible each month.",
    veredicto="They're the two ends of the table. PebbleHost Budget is the cheapest there is: "
              "€13.76 for 16 GB, every month. But that price has a catch: their Budget range "
              "<strong>has no backups</strong> and runs a Ryzen 7 5700X with DDR4 at 2133 MHz. "
              "Godlike is at the other end: latest-gen Ryzen up to the 9950X3D, NVMe, up to "
              "three backups a day and the option to <strong>pick the days</strong> you pay "
              "for. What it costs: €38.24 for 16 GB with the code, nearly three times Pebble, "
              "though every month and not just the first. For a year-round server on the "
              "smallest budget, Pebble. For a heavy modpack "
              "over a few months, where an outage or a slow CPU ruins the run, Godlike.",
  ),
  ("godlike", "dathost"): dict(
    gana_a="It's a seasonal server, you want the best CPU, or you need less than 16 GB.",
    gana_b="You'll run 16 GB all year and want to pay the least.",
    veredicto="Both go after people who want the server to run smoothly, but they charge in "
              "opposite ways. DatHost has a single plan: 16 GB with a Ryzen 9 7950X and "
              "unlimited slots for €14.90 a month, no matter what. Godlike lets you build the "
              "plan — GB, slots and days —, runs a Ryzen one generation newer, up to the "
              "9950X3D, and gives you up to three backups a day. The difference is the bill: "
              "their 16 GB is €50.99 a month at the normal rate (€40.58 paying the year), more "
              "than triple DatHost. So for 16 GB all year, DatHost. For a modpack of a few "
              "months, for smaller servers or if you want the fastest CPU, Godlike.",
  ),
  ("shockbyte", "bisect"): dict(
    gana_a="Almost everything: it's cheaper per gigabyte at every size.",
    gana_b="You prefer billing in euros and Spanish-language support.",
    veredicto="A duel between two per-gigabyte hosts. Shockbyte is cheaper at every tier; "
              "Bisect wins on convenience for the Spanish market. Pick whichever suits you.",
  ),
}


def eur(n):
    return "€%.2f" % n


def _tabla(a, b, d):
    cambio = d["cambioUsdEur"]
    GB = duelos.GB_REF

    def celdas(hid):
        h = next(x for x in d["hosts"] if x["id"] == hid)
        out = []
        for gb in GB:
            precio, etiqueta = precio_para(h, "minecraft", gb, cambio)
            extra = ("<small>%s</small>" % etiqueta
                     if etiqueta and etiqueta != "%d GB" % gb else "")
            out.append(('<td class="price">%s%s</td>' % (eur(precio), extra))
                       if precio else '<td class="nd">not available</td>')
        return "".join(out)

    avisos = []
    for hid in (a, b):
        h = next(x for x in d["hosts"] if x["id"] == hid)
        e = h["precios"]["minecraft"].get("entrada")
        if not e:
            continue
        for gb_ref in (8, 6, 4, 2):
            mes, entrada, ano = coste_primer_ano(h, gb_ref, cambio)
            if mes is not None:
                break
        if mes is None:
            continue
        avisos.append("<strong>%s</strong> brings %s down to %s for a %d GB server, then "
                      "it's %s a month: %s for the first year."
                      % (h["nombre"], e.get("que_en", e["que"]), eur(entrada), gb_ref,
                         eur(mes), eur(ano)))
    aviso = ('<p class="tbl-note">%s</p>' % " ".join(avisos)) if avisos else ""

    cab = "".join("<th>%d GB</th>" % g for g in GB)
    fila = lambda hid: ('<tr%s><td>%s</td>%s</tr>'
                        % (' class="hl"' if partner.es_partner(hid) else "",
                           FICHAS[hid]["nombre"], celdas(hid)))
    return ('<div class="table-wrap"><table class="tabla-maestra ordenable">\n'
            '<thead><tr><th>Host</th>%s</tr></thead>\n<tbody>\n%s\n%s\n</tbody></table></div>\n'
            '<p class="tbl-note">Recurring monthly Minecraft price, in euros. Checked by hand '
            'on %s.</p>' % (cab, fila(a), fila(b), d.get("comprobado_en", d["comprobado"]))) + aviso


T_EN = dict(
    mes="%d GB a month", por_gb="Price per GB (at %d GB)",
    primer_pago="What you pay the first month (%d GB)",
    primer_ano="What you've spent after a year (%d GB)",
    desde="In business since", ubic="Locations", no="doesn't go that high",
    ficha="See the review", pre="/en", que_key="que_en",
    tanteo="<b>%s</b> wins on %d of the %d things you can measure.",
    nota=("The scoreboard only counts what you can put a price on. What you can't "
          "measure in money &mdash; whether it takes mods, how many people can join, "
          "backups or the CPU &mdash; is in the verdict below."),
    empate="Technical draw: they win on the same number of things.",
    card_pie="%d GB: %s against %s",
)


def html(duelo, d):
    A, B = FICHAS[duelo["a"]], FICHAS[duelo["b"]]
    t = TEXTOS[(duelo["a"], duelo["b"])]
    ruta = "/en/versus/%s/" % duelos.url_de(duelo)
    titulo = "%s vs %s: which one is right for you in 2026" % (A["nombre"], B["nombre"])
    desc = ("Head-to-head comparison of %s and %s with real prices checked by hand. "
            "When each one wins and why." % (A["nombre"], B["nombre"]))
    cta = ""
    for lado in (duelo["a"], duelo["b"]):
        if partner.es_partner(lado):
            cta = partner.boton("minecraft", "DUELO-EN", "Go to %s" % FICHAS[lado]["nombre"])
    cta = cta or '<a class="cta" href="/en/">Size my server</a>'
    faq = json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question",
                        "name": "Which is better, %s or %s?" % (A["nombre"], B["nombre"]),
                        "acceptedAnswer": {"@type": "Answer",
                                           "text": t["veredicto"].replace("<strong>", "").replace("</strong>", "")}}],
    }, ensure_ascii=False, indent=2)

    return """<!doctype html>
<html lang="en">
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
    <nav class="miga"><a href="/en/">Home</a> › <a href="/en/versus/">Versus</a> › %(na)s vs %(nb)s</nav>

    <h1>%(na)s <em>vs</em> %(nb)s</h1>
    <p class="sub art-sub">Head to head with prices checked by hand and a clear
      verdict: who wins, on what, and when the other one is worth it.</p>
    <p class="art-meta">Updated on %(comprobado)s</p>

%(versus)s

    <h2 id="precios">Every price, side by side</h2>
%(tabla)s

    <h2 id="cuando">When each one wins</h2>
    <div class="duelo">
      <div class="duelo-lado gana-a">
        <span class="duelo-tag">Pick %(na)s if…</span>
        <p>%(gana_a)s</p>
        <a class="cta-mini" href="/en/hosting/%(ua)s/">%(na)s review</a>
      </div>
      <div class="duelo-vs" aria-hidden="true">vs</div>
      <div class="duelo-lado gana-b">
        <span class="duelo-tag">Pick %(nb)s if…</span>
        <p>%(gana_b)s</p>
        <a class="cta-mini" href="/en/hosting/%(ub)s/">%(nb)s review</a>
      </div>
    </div>

    <h2 id="veredicto">My verdict</h2>
    <p class="veredicto-final">%(veredicto)s</p>

    <div class="art-cta">
      <h3>And for your case?</h3>
      <p>
        The winner changes completely depending on how much RAM you need. Tell me how
        many of you there are and what you've installed, and I'll tell you in 20 seconds,
        with both compared along with the rest.
      </p>
      <div class="hero-cta">
        <a class="cta-ghost" href="/en/">Work out my GB</a>
        %(cta)s
      </div>
    </div>
  </article>
</main>

<footer></footer>

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
""" % dict(titulo=titulo, desc=desc, dom=DOMINIO, ruta=ruta, fuentes=FUENTES,
           na=A["nombre"], nb=B["nombre"], ua=A["url"], ub=B["url"],
           comprobado=d.get("comprobado_en", d["comprobado"]),
           tabla=_tabla(duelo["a"], duelo["b"], d),
           versus=duelos.bloque_versus(duelo["a"], duelo["b"], d, T_EN, FICHAS_EN),
           gana_a=t["gana_a"], gana_b=t["gana_b"], veredicto=t["veredicto"], cta=cta, faq=faq,
           migas=migas.schema([("Home", "/en/"), ("Versus", "/en/versus/"),
                               ("%s vs %s" % (A["nombre"], B["nombre"]), None)]))


def indice(d):
    filas = []
    for x in duelos.DUELOS:
        A, B = FICHAS[x["a"]], FICHAS[x["b"]]
        filas.append('      <a class="vs-card" href="/en/versus/%s/">'
                     '<span class="vs-card-a">%s</span>'
                     '<span class="vs-card-vs" aria-hidden="true">VS</span>'
                     '<span class="vs-card-b">%s</span>'
                     '<span class="vs-card-pie">%s</span></a>'
                     % (duelos.url_de(x), A["nombre"], B["nombre"],
                        duelos._pie_card(x, d, T_EN)))
    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Versus: Minecraft hosts head to head (2026)</title>
<meta name="description" content="Godlike.host vs Apex, vs Shockbyte, vs PebbleHost… Head-to-head Minecraft hosting comparisons with real prices and a clear verdict.">
<link rel="canonical" href="%(dom)s/en/versus/">
<meta property="og:type" content="website">
<meta property="og:url" content="%(dom)s/en/versus/">
<meta property="og:title" content="Versus: Minecraft hosts head to head">
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
    <nav class="miga"><a href="/en/">Home</a> › Versus</nav>
    <h1><em>Versus</em>: host against host</h1>
    <p class="sub art-sub">
      The most searched match-ups, with prices side by side and a verdict on when each
      one wins.
    </p>
    <div class="vs-cards">
%(filas)s
    </div>
    <p class="art-meta">Prices checked on %(comprobado)s.</p>
  </div>
</main>
<footer></footer>
<script src="/buscador_ui.js" defer></script>
</body>
</html>
""" % dict(dom=DOMINIO, fuentes=FUENTES, filas="\n".join(filas),
           comprobado=d.get("comprobado_en", d["comprobado"]))
