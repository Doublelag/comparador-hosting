# -*- coding: utf-8 -*-
"""
English deals page: /en/deals/.

TEXTOS goes in the SAME ORDER as ofertas.OFERTAS (checked by host name when
building). If you add or reorder a Spanish deal, do the same here.

Imported by build.py.
"""

import datetime

import hostings
import ofertas
import partner

DOMINIO = "https://montatuserver.com"
FUENTES = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
           '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
           '<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700'
           '&family=Inter:wght@400..800&display=swap" rel="stylesheet">')

VEREDICTOS = {"buena": "A real deal", "truco": "Has a catch", "evitar": "I'd avoid it"}

TEXTOS = [
  ("Godlike.host", dict(
    titulo="−25% every month: the only discount here that never expires",
    resumen="The other nine discounts on this site are first-invoice only. This one "
            "is not: the −25% is still there in month twelve. 16 GB comes to €38.24 "
            "and 8 GB to €19.49, always.",
    letra="It still is not cheap per GB: €2.44 with the code against €1.00 at the "
          "cheapest host in the table. You are paying for convenience, not gigabytes.",
    consejo="It shines brightest on a first server: try it free for a day with no card, "
            "mods go in from the panel, and their launcher gets the game ready for each "
            "friend. If you just want to spend the least, look at Kinetic.",
  )),
  ("HolyHosting", dict(
    titulo="25% off with a countdown",
    resumen="They advertise $0.95 per GB on the homepage, with a clock ticking down.",
    letra="The small print says it: <strong>25% OFF on your first month</strong>. The real "
          "rate is $1.25/GB, so their 16 GB is $19.99 a month from the second month. That "
          "$0.95 you only pay once.",
    consejo="The countdown is there so you don't do the maths. Do it: multiply by 1.25 and "
            "compare with that.",
  )),
  ("The Minecraft Hosting", dict(
    titulo="60% off with the BLACKFRIDAY code",
    resumen="A 60% Black Friday code they say is “lifetime”.",
    letra="They call it Black Friday and it's running <strong>in September</strong>. A "
          "discount that never goes away isn't a discount: it's the price. Their 16 GB is "
          "listed at $35 so the 60% looks huge. And “lifetime” on a website isn't a contract.",
    consejo="If you're still interested, ask them <strong>in writing</strong> what it renews "
            "at before paying. There's too big a gap between $35 and $14 to trust one word on "
            "a banner.",
  )),
  ("WiseHosting", dict(
    titulo="50% off paying yearly",
    resumen="Brings the GB down to $1.50 instead of $3.00 if you sign up for twelve months.",
    letra="It's a good old commitment discount. You pay the year upfront and that's it. No "
          "hidden trap. But it's twelve months in one go for something you haven't tried yet.",
    consejo="They have a seven-day refund. Sign up, really test it for those seven days, and "
            "if it convinces you, stay.",
  )),
  ("Shockbyte", dict(
    titulo="30% off Minecraft, permanently",
    resumen="Their Minecraft discount is recurring, not first-month only. The price on their "
            "site already includes it.",
    letra="Careful when comparing: since it's already applied, the headline price IS the real "
          "price. Don't knock another 30% off in your head.",
    consejo="For Minecraft they charge per gigabyte. It helps if your plan is small; it doesn't "
            "save the big ones. 16 GB is still around $47.",
  )),
  ("Shockbyte", dict(
    titulo="25% off paying yearly",
    resumen="A discount for signing up for 12 months. They also do 10% off paying quarterly.",
    letra="You pay the 12 months upfront. If the server doesn't win you over after a month "
          "and a half, the money's already gone.",
    consejo="Reasonable if you've already tried the service. Never as a first purchase.",
  )),
  ("Apex Hosting", dict(
    titulo="25% off with the APEX25 code",
    resumen="25% off your first order.",
    letra="<strong>It's for the first month only.</strong> Their 16 GB goes from $53.99 the "
          "first month to <strong>$71.99 every month after</strong>. The discount hides that "
          "they're by far the most expensive in the comparison.",
    consejo="Don't let the 25% distract you: look at month two. For that $71.99 you get the "
            "same RAM for around €13.75 elsewhere.",
  )),
  ("Hostinger", dict(
    titulo="Up to 67% off",
    resumen="They advertise 16 GB at $13.99/month instead of $42.99.",
    letra="For that price you have to <strong>pay 24 months upfront</strong> ($335.76 in one "
          "go) and then it <strong>renews at $28.99/month</strong>, more than double the "
          "advertised price. The 67% is worked out from a list price almost nobody pays.",
    consejo="The most misleading deal I've found in this business. If you're still interested, "
            "do the maths at $28.99, which is what you'll actually pay.",
  )),
  ("Nodecraft", dict(
    titulo="30% off the first month and 24 hours free",
    resumen="They rebuilt their site in September: a 24-hour trial and the first month 30% cheaper.",
    letra="The −30% is <strong>for the first month only</strong>: 8 GB starts at $27.99 and "
          "renews at $39.98. And for the free trial <strong>they ask you to verify your "
          "phone</strong>, which they only tell you at the end.",
    consejo="The 24 free hours are good for seeing the panel. But at $4.99 per GB they're among "
            "the most expensive in the comparison: do the maths with month two's price.",
  )),
]


def html():
    assert [o["host"] for o in ofertas.OFERTAS] == [h for h, _ in TEXTOS], \
        "ofertas_en.TEXTOS no va en el mismo orden que ofertas.OFERTAS"
    id_de_ficha = {}
    for hid, f in hostings.FICHAS.items():
        id_de_ficha.setdefault("/hosting/%s/" % f["url"], hid)
    hoy = datetime.date.today().isoformat()
    tarjetas = []
    vivas = 0
    buenas = 0
    for o, (_, t) in zip(ofertas.OFERTAS, TEXTOS):
        if o.get("caduca") and hoy > o["caduca"]:
            continue
        vivas += 1
        buenas += o["veredicto"] == "buena"
        _, cls = ofertas.VEREDICTOS[o["veredicto"]]
        codigo = ('<div class="of-codigo"><span>Code</span><code>%s</code></div>' % o["codigo"]
                  if o.get("codigo") else "")
        caduca = ('<p class="of-caduca">⏳ Ends %s/%s</p>' % (o["caduca"][8:10], o["caduca"][5:7])
                  if o.get("caduca") else "")
        ficha_en = "/en" + o["ficha"]
        hid = id_de_ficha.get(o["ficha"])
        boton = (partner.boton("minecraft", "OFERTAS-EN") if partner.es_partner(hid)
                 else '<a class="cta-ghost" href="%s">%s review</a>' % (ficha_en, o["host"]))
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
          <span class="of-letra-tit">The fine print</span>
          <p>%s</p>
        </div>
        <p class="of-consejo"><strong>My advice:</strong> %s</p>
        <div class="of-cta">%s</div>
      </article>""" % (cls, o["veredicto"], "si" if o.get("codigo") else "no",
                       ficha_en, o["host"], VEREDICTOS[o["veredicto"]], t["titulo"],
                       caduca, t["resumen"], codigo, t["letra"], t["consejo"], boton))

    rev = "20 September 2026"
    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Minecraft hosting deals and coupons (%(rev)s)</title>
<meta name="description" content="The real Minecraft hosting deals, with their fine print and an honest verdict. Which are worth it and which are first-month discounts in disguise.">
<link rel="canonical" href="%(dom)s/en/deals/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="MontaTuServer">
<meta property="og:url" content="%(dom)s/en/deals/">
<meta property="og:title" content="Server hosting deals, with the fine print">
<meta property="og:description" content="I don't just list coupons. I tell you which are worth it and which are a first-month discount dressed up as a permanent one.">
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
  <div class="wrap articulo" style="max-width:860px">
    <nav class="miga"><a href="/en/">Home</a> › Deals</nav>

    <h1>Hosting deals, <em>with the fine print</em></h1>
    <p class="sub art-sub">
      Every coupon site tells you its deals are amazing. Here, only %(buenas)d of
      %(vivas)d strike me as genuine, and every one gets its fine print printed just as big.
    </p>
    <p class="art-meta">Reviewed by hand on %(rev)s</p>

    <div class="indep" style="margin:24px 0 30px">
      <span class="indep-ico" aria-hidden="true">⚖️</span>
      <p>
        <strong>The industry's favourite trick:</strong> advertising a huge discount that
        only lasts the first month, or that requires paying two years upfront. That's why
        every deal here comes with a verdict and the price you'll <em>actually</em> pay
        from month two.
      </p>
    </div>

    <div class="filtros" id="filtros-ofertas" role="group" aria-label="Filter the deals"></div>
    <div class="ofertas">%(tarjetas)s
    </div>

    <div class="art-cta" style="margin-top:36px">
      <h3>Which one works out best for you?</h3>
      <p>
        A discount is only good if the plan fits. Tell me how many of you there are and
        what you play, set your budget, and I'll tell you which option suits you with the
        prices already compared.
      </p>
      <a class="cta" href="/en/">Size my server</a>
    </div>
  </div>
</main>

<footer></footer>

<script src="/buscador_ui.js" defer></script>
<script src="/filtros_ui.js" defer></script>

</body>
</html>
""" % dict(dom=DOMINIO, fuentes=FUENTES, rev=rev, tarjetas="".join(tarjetas),
           buenas=buenas, vivas=vivas)
