# -*- coding: utf-8 -*-
"""
English best-hosting page: /en/minecraft/best-hosting/.

Same tables and numbers as the Spanish comparison (comparativas.py); the text
is here. If the Spanish text changes, update this one too.

Imported by build.py.
"""

import json

from comparativas import precio_para, coste_primer_ano, cuantos, COMPARATIVAS
import migas
import partner

DOMINIO = "https://montatuserver.com"
RUTA = "/en/minecraft/best-hosting/"
FUENTES = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
           '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
           '<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700'
           '&family=Inter:wght@400..800&display=swap" rel="stylesheet">')

GB_REF = [2, 4, 8, 16]


def eur(n):
    return "€%.2f" % n


def tabla_grande(d):
    cambio = d["cambioUsdEur"]
    filas = []
    for h in d["hosts"]:
        pr = h["precios"].get("minecraft")
        if not pr:
            continue
        celdas = []
        for gb in GB_REF:
            precio, da = precio_para(h, "minecraft", gb, cambio)
            if precio is None:
                celdas.append('<td class="nd">not available</td>')
            else:
                extra = ("<small>gives you %s</small>" % da) if da != "%d GB" % gb else ""
                celdas.append('<td class="price">%s%s</td>' % (eur(precio), extra))
        clave = next((precio_para(h, "minecraft", gb, cambio)[0] for gb in GB_REF
                      if precio_para(h, "minecraft", gb, cambio)[0] is not None), 9e9)
        marca = ' class="hl"' if partner.es_partner(h["id"]) else ""
        filas.append((clave, '<tr%s><td>%s<small>%s</small></td>%s</tr>'
                      % (marca, h["nombre"], pr.get("nota_en", pr["nota"]), "".join(celdas))))
    filas = [f for _, f in sorted(filas, key=lambda x: x[0])]
    return ('<div class="table-wrap">\n  <table class="tabla-maestra ordenable">\n'
            '    <thead><tr><th>Host</th>%s</tr></thead>\n    <tbody>\n%s\n    </tbody>\n'
            '  </table>\n</div>\n'
            '<p class="tbl-note">Recurring monthly price, in euros. Hosts that charge in dollars '
            'are converted at $1&nbsp;=&nbsp;€%s. Prices checked by hand on %s.</p>'
            % ("".join("<th>%d GB</th>" % gb for gb in GB_REF),
               "\n".join("      " + f for f in filas), cambio,
               d.get("comprobado_en", d["comprobado"])))


def tabla_primer_ano(d, gb=8):
    cambio = d["cambioUsdEur"]
    filas = []
    for h in d["hosts"]:
        pr = h["precios"]["minecraft"]
        if pr["modelo"] == "slots":
            continue
        mes, entrada, ano = coste_primer_ano(h, gb, cambio)
        if mes is None:
            continue
        e = pr.get("entrada")
        gancho = ("%s <small>%s</small>" % (eur(entrada), e.get("que_en", e["que"]))
                  if entrada is not None else '<span class="nd">none</span>')
        marca = ' class="hl"' if partner.es_partner(h["id"]) else ""
        filas.append((ano, '<tr%s><td>%s</td><td class="price">%s</td><td>%s</td>'
                           '<td class="price">%s</td></tr>'
                      % (marca, h["nombre"], eur(mes), gancho, eur(ano))))
    filas = [f for _, f in sorted(filas, key=lambda x: x[0])]
    return ('<div class="table-wrap">\n<table class="tabla-maestra ordenable">\n'
            '<thead><tr><th>Host</th><th>Monthly</th><th>Entry price</th>'
            '<th>First 12 months</th></tr></thead>\n<tbody>\n%s\n</tbody>\n</table>\n</div>\n'
            '<p class="tbl-note">For a %d GB server. “First 12 months” is the entry discount '
            'where there is one plus the normal rate for the rest of the year. Hosts that '
            'sell by slots without publishing RAM are left out, because there\'s no way to '
            'know whether they give you those gigabytes.</p>' % ("\n".join(filas), gb))


VEREDICTOS = [
    ("If there are few of you and no mods", "PebbleHost Budget",
     "2-4 GB is plenty, and they charge $1 per GB: €3.44 for 4 GB. It's the cheapest there "
     "is. Two things before you sign up: the hardware is modest, which you won't notice with "
     "four friends in vanilla, and that range has no backups."),
    ("If the server will run all year", "Kinetic Hosting or PebbleHost",
     "Month to month, both are around €0.86 per GB: 16 GB for about €13.75. Kinetic includes "
     "five backups and starts at 4 GB; PebbleHost Budget has no backups."),
    ("If it's a seasonal server", "Godlike.host",
     "A modpack with friends, an event, a project of a few months. Godlike has <strong>the "
     "only discount in the comparison that never expires, −25% every month</strong>, and "
     "it's the only one that lets you <strong>pick the days</strong> (30, 90, 180 or 360). You can try "
     "it free for a day, and it runs latest-gen Ryzen with up to three backups a day. You pay "
     "for as long as the server lasts, not a month more. For a full year it costs more than "
     "the ones above."),
    ("If you need more than 16 GB", "Kinetic, ScalaCube or the per-GB hosts",
     "Single plans stop at 16 GB. Kinetic goes up to 124 GB (32 GB for about €27.50), "
     "ScalaCube to 64 and PebbleHost charges every gigabyte with no ceiling. Beyond that "
     "you're in dedicated-server territory."),
]

FAQ = [
    ("What's the cheapest Minecraft host?",
     "Kinetic Hosting and PebbleHost Budget, at around €0.86 per GB every month; "
     "PebbleHost's Budget range has no backups. Godlike, even with its permanent −25%, "
     "sits at €2.44 per GB: there you are not paying for gigabytes, you are paying to "
     "have it made easy."),
    ("Is paying a year upfront worth it?",
     "Only if you've already tried the server and know you'll stay. Take one month first, "
     "bring your people in and see how it goes. And be wary of anyone who only gives you the "
     "good price if you pay 24 months in one go."),
    ("What's the difference between paying per GB and a single plan?",
     "Per GB you pay exactly for what you ask for, so it's cheaper if you need little and much "
     "more expensive if you need to grow. A single plan gives you plenty of RAM for a fixed "
     "price: you lose if you need 2 GB and win big from 8 up."),
    ("Are the prices on this page up to date?",
     "I check them by hand on each host's website, and the date is under the table. Hosts "
     "change them without notice, so if you see something different, tell me and I'll fix it."),
]


def html(d):
    n = cuantos(COMPARATIVAS[0], d)
    titulo = "The best Minecraft hosting in 2026: %d compared with real prices" % n
    desc = ("A real comparison of %d Minecraft hosts with prices checked by hand: Godlike.host, "
            "PebbleHost, Kinetic, Shockbyte, BisectHosting, Apex and more. With the fine print "
            "they don't tell you." % n)
    veredictos = "\n".join(
        '        <div class="card">\n          <h3>%s</h3>\n          <p class="ver-gana">%s</p>\n'
        '          <p>%s</p>\n        </div>' % v for v in VEREDICTOS)
    faq = "\n".join('      <details>\n        <summary>%s</summary>\n        <p>%s</p>\n      </details>'
                    % q for q in FAQ)
    faq_schema = json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
                             "mainEntity": [{"@type": "Question", "name": p,
                                             "acceptedAnswer": {"@type": "Answer", "text": r}}
                                            for p, r in FAQ]}, ensure_ascii=False, indent=2)

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

    <nav class="miga" aria-label="You are here"><a href="/en/">Home</a> › Best hosting</nav>

    <h1>The best <em>Minecraft</em> hosting</h1>
    <p class="sub art-sub">%(n)d hosts, prices checked by hand and the fine print that isn't on their homepage.</p>
    <p class="art-meta">Prices checked on %(comprobado)s · Reviewed every 2-3 months</p>

      <p>
        I went through all %(n)d websites, <strong>wrote the prices down by hand and read
        the fine print</strong>. There are surprises.
      </p>
      <p>
        And a warning: the winner changes depending on how much RAM you need. Below you'll
        find when each one wins. If I steer you wrong once, you won't come back.
      </p>

    <h2 id="tabla">The table, no frills</h2>
    <p>
      What each host charges per month depending on the gigabytes you need. Look at
      <strong>your column</strong>, not the cheapest row: the winner changes completely
      depending on how much RAM you need.
    </p>

%(tabla)s

    <h2 id="primer-ano">What you pay in the first year, not the first month</h2>
    <p>
      This is the sum almost nobody does. Half the industry advertises an entry price —
      “−75%% on your first purchase”, “−25%% the first month” — and renews at the full rate
      without warning. So here are both: what you pay to get started and <strong>what
      you'll have spent after twelve months</strong>, which is when you really know if it
      was cheap.
    </p>

%(tabla_ano)s

    <div class="art-cta" style="margin-top:26px">
      <h3>And how many GB do you need?</h3>
      <p>
        It's the question that decides everything else. Tell me how many of you there are
        and what you've installed and I'll work it out in 20 seconds. No sign-up.
      </p>
      <a class="cta" href="/en/#calculadora">Work out my GB</a>
    </div>

      <h2 id="s0">The three traps I found</h2>
        <p>
          Comparing hosting prices is hard on purpose. These are the three tricks I've seen
          over and over, and how to spot them:
        </p>
        <ul>
          <li>
            <strong>The price that requires paying two years upfront.</strong> Hostinger
            advertises its 16 GB at $13.99 a month. The fine print says you have to pay
            <strong>24 months in one go</strong> ($335) and that it then <strong>renews at
            $28.99</strong>. The real price is double the one in big letters.
          </li>
          <li>
            <strong>The discount that only lasts the first month.</strong> Apex advertises
            25%% off. It's for the first month. Their 16 GB is $53.99 the first month and
            <strong>$71.99 every month after</strong>.
          </li>
          <li>
            <strong>Selling “slots” without saying the RAM.</strong> If a host promises 20
            or 50 players but doesn't publish the gigabytes, you can't know if your modpack
            will run. And usually it's because they'd rather you didn't know.
          </li>
        </ul>
        <p>
          That's why the table above always uses <strong>the recurring price</strong>: what
          you'll pay in month 3, 6 and 12. Not the first-month hook.
        </p>
      <h2 id="s1">The pricing model matters more than the brand</h2>
        <p>There are three ways they charge you, and they completely change who suits what:</p>
        <ul>
          <li>
            <strong>Per gigabyte</strong> (Shockbyte, BisectHosting, PebbleHost, Apex). You
            pay for what you ask for, and there's a chasm between them: the same 16 GB goes
            from €13.76 at PebbleHost Budget to €61.91 at Apex.
          </li>
          <li>
            <strong>Single plan</strong> (DatHost). One product: 16 GB, a Ryzen 9 7950X and
            unlimited slots. If you need 2 GB you overpay; from 12-16 GB it competes with the
            cheapest per gigabyte, with a better CPU.
          </li>
          <li>
            <strong>By slots</strong> (Minecraft Realms). They charge by players and don't
            publish the RAM. Easy to understand, impossible to compare.
          </li>
        </ul>
        <p>
          <strong>The practical takeaway:</strong> the “best host” depends on how much RAM
          you need, which is why this question has no single answer. Look at the table in
          your column, not overall.
        </p>

    <h2 id="veredicto">Which one suits you</h2>
    <p>
      There's no “best host” full stop. There's a best host <em>for your case</em>, and it
      changes with how many of you there are and what you've installed:
    </p>
    <div class="cards" style="margin-top:18px">
%(veredictos)s
    </div>

    <div class="art-cierre">
      <h2 id="faq">Frequently asked questions</h2>
%(faq)s
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
""" % dict(titulo=titulo, desc=desc, dom=DOMINIO, ruta=RUTA, fuentes=FUENTES, n=n,
           comprobado=d.get("comprobado_en", d["comprobado"]), tabla=tabla_grande(d),
           tabla_ano=tabla_primer_ano(d), veredictos=veredictos, faq=faq,
           faq_schema=faq_schema,
           migas=migas.schema([("Home", "/en/"), ("Best Minecraft hosting", None)]))
