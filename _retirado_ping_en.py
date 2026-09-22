# -*- coding: utf-8 -*-
"""
English ping page: /en/ping-from-spain/. Same measurements as ping.py.

Imported by build.py.
"""

import json

import ping

DOMINIO = "https://montatuserver.com"
FUENTES = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
           '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
           '<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700'
           '&family=Inter:wght@400..800&display=swap" rel="stylesheet">')

METODOS = {
    "tcp": ("Measured", "TCP connection to port 25565 of their public test server, best of four tries."),
    "widget": ("Measured", "With the meter on their own website, run from this same connection."),
    "ubicacion": ("Location only", "I know where their data centre is, but they don't publish a "
                                   "test server and I couldn't measure it myself."),
}
CIUDADES = {"Ámsterdam": "Amsterdam", "Fráncfort": "Frankfurt", "Londres": "London",
            "Nueva York": "New York", "Norteamérica": "North America", "Singapur": "Singapore",
            "Europa": "Europe", "Europa (Ámsterdam / Maidenhead)": "Europe (Amsterdam / Maidenhead)",
            "Coventry (Reino Unido)": "Coventry (UK)"}
MESES = ["January", "February", "March", "April", "May", "June", "July", "August",
         "September", "October", "November", "December"]


def _c(x):
    return CIUDADES.get(x, x)


def html():
    d = ping.datos()
    p_ = d["ping"]
    a, m, dia = p_["medido"].split("-")
    fecha = "%d %s %s" % (int(dia), MESES[int(m) - 1], a)

    filas = []
    for host_id, p in p_["hosts"].items():
        medidos = [ms for _, ms in p["detalle"]]
        mejor = min(medidos) if medidos else None
        filas.append((mejor is None, mejor if mejor is not None else 9999, host_id, p, mejor))
    filas.sort()

    tabla, detalles = [], []
    for _, _, host_id, p, mejor in filas:
        cerca = ", ".join(_c(x) for x in p["europa"]) if p["europa"] else "&mdash;"
        celda = ('<td class="nd">Not measured</td>' if mejor is None
                 else '<td><b class="ms %s">%d ms</b></td>' % (ping._clase(mejor), mejor))
        tabla.append('        <tr>\n          <td><a href="/en/hosting/%s/">%s</a></td>\n'
                     '          <td>%s</td>\n          %s\n'
                     '          <td><span class="met met-%s">%s</span></td>\n        </tr>'
                     % (ping._slug(host_id), ping._nombre(d, host_id), cerca, celda,
                        p["metodo"], METODOS[p["metodo"]][0]))
        if p["detalle"]:
            items = "".join('<li><span>%s</span><b class="ms %s">%d ms</b></li>'
                            % (_c(c), ping._clase(ms), ms) for c, ms in p["detalle"])
            detalles.append('      <div class="card ping-card">\n        <h3>%s</h3>\n'
                            '        <ul class="ping-lista">%s</ul>\n'
                            '        <p class="ping-como">%s</p>\n      </div>'
                            % (ping._nombre(d, host_id), items, METODOS[p["metodo"]][1]))

    faq = [
        ("What ping is acceptable in Minecraft?",
         "Under 50 ms you won't notice anything. Between 50 and 100 you notice it when "
         "fighting and mining, but it's playable. Above 150 it really starts to get annoying: "
         "blocks &laquo;come back&raquo; and mobs teleport."),
        ("Is there any host with servers in Spain?",
         "Of the ones I've been able to check, none. The closest you'll get is Amsterdam, "
         "Frankfurt or London, which from Spain comes out at around 35 ms. That's perfectly playable."),
        ("So it doesn't matter which host I pick for ping?",
         "Within Europe, pretty much. Nobody notices the difference between 35 and 37 ms. What "
         "does matter is not ending up in a US data centre by accident: there you're at 130 ms or more."),
        ("Why doesn't your ping match mine?",
         "Because it depends on your provider, your city and whether you're on fibre or mobile. "
         "These numbers come from a home fibre connection in Spain, measured on " + fecha +
         ". Use them as a reference to compare hosts with each other, not as a promise of what "
         "you'll get."),
        ("Does ping depend on the plan I buy?",
         "No. It depends on where the machine is, not how much RAM you give it. An expensive "
         "plan in New York will give you worse ping than a cheap one in Amsterdam."),
    ]
    faq_html = "\n".join('      <details>\n        <summary>%s</summary>\n        <p>%s</p>\n      </details>'
                         % q for q in faq)
    faq_schema = json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
                             "mainEntity": [{"@type": "Question", "name": q,
                                             "acceptedAnswer": {"@type": "Answer", "text": r}}
                                            for q, r in faq]}, ensure_ascii=False, indent=2)

    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ping from Spain to each Minecraft host (measured by hand)</title>
<meta name="description" content="How many milliseconds you get from Spain to each Minecraft host's servers. Measured on a real connection, not estimated, and saying how each figure was obtained.">
<link rel="canonical" href="%(dom)s/en/ping-from-spain/">
<meta property="og:type" content="article">
<meta property="og:site_name" content="MontaTuServer">
<meta property="og:url" content="%(dom)s/en/ping-from-spain/">
<meta property="og:title" content="What ping will you get from Spain?">
<meta property="og:description" content="No server host has machines in Spain. This is what you'll really get, measured.">
<meta property="og:image" content="%(dom)s/og-image.jpg">
<meta property="og:locale" content="en_GB">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
%(fuentes)s
<link rel="stylesheet" href="/styles.css">
<script type="application/ld+json">%(faq_schema)s</script>
</head>
<body>

<header class="site-head"></header>

<main>
  <div class="wrap articulo" style="max-width:860px">
    <nav class="miga"><a href="/en/">Home</a> &rsaquo; Ping from Spain</nav>

    <h1>What <em>ping</em> will you get from Spain?</h1>
    <p class="sub art-sub">
      Everyone says &laquo;low-latency servers&raquo; and nobody tells you how many
      milliseconds that is. Here they are, measured, with how I got each one.
    </p>
    <p class="art-meta">Measured on %(fecha)s from a home fibre connection in Spain</p>

    <div class="indep" style="margin:24px 0 30px">
      <span class="indep-ico" aria-hidden="true">⚡</span>
      <p>
        <strong>Bad news first.</strong> Of the hosts I've been able to check, none has
        machines in Spain. The closest you'll get is Amsterdam, Frankfurt or London.
        <strong>The good news:</strong> from here that's about 35 ms, and in Minecraft you
        won't notice.
      </p>
    </div>


    <h2 id="detalle">Every location measured</h2>
    <p>
      Not just the best one. That way you see what's at stake if you pick the wrong
      location when you sign up, which is the costliest and easiest mistake to make.
    </p>
    <div class="cards">
%(detalles)s
    </div>

    <h2 id="que-significa">What each number means</h2>
    <ul>
      <li><strong>Under 50 ms</strong> — you won't notice. It's what you get with any data
        centre in central Europe.</li>
      <li><strong>50 to 100 ms</strong> — noticeable when fighting and mining, but perfectly
        playable.</li>
      <li><strong>Over 150 ms</strong> — genuinely annoying: blocks &laquo;come back&raquo;
        and mobs teleport. This is where you end up if you leave the default location and
        get the US.</li>
    </ul>

    <div class="indep" style="margin:26px 0">
      <span class="indep-ico" aria-hidden="true">⚖️</span>
      <p>
        <strong>Why this page is incomplete on purpose:</strong> only hosts I've been able
        to measure appear. The rest don't publish a test server, and filling it with
        guesses would be exactly what I criticise the rest of the industry for. I'll add
        them as I manage to measure them.
      </p>
    </div>

    <div class="art-cierre">
      <h2 id="faq">Frequently asked questions</h2>
%(faq)s
    </div>

    <div class="art-cta" style="margin-top:34px">
      <h3>Now you know the ping: on to the GB</h3>
      <p>
        Within Europe the latency gap between hosts is a couple of milliseconds, so what
        really decides it is how much RAM you need and who gives it to you cheapest.
      </p>
      <a class="cta" href="/en/">Size my server</a>
    </div>
  </div>
</main>

<footer></footer>

<script src="/buscador_ui.js" defer></script>
<script src="/tabla_ui.js" defer></script>

</body>
</html>
""" % dict(dom=DOMINIO, fuentes=FUENTES, fecha=fecha, tabla="\n".join(tabla),
           detalles="\n".join(detalles), faq=faq_html, faq_schema=faq_schema)
