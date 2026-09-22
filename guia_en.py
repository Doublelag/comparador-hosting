# -*- coding: utf-8 -*-
"""
English setup guide: /en/minecraft/how-to-set-up-a-server/.

The English twin of guias.GUIAS[0]. Same sections in the same order (the
homepage links to #s6, the backups section), so keep them aligned.

Imported by build.py.
"""

import guias
import migas

DOMINIO = "https://montatuserver.com"
RUTA = "/en/minecraft/how-to-set-up-a-server/"
FUENTES = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
           '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
           '<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700'
           '&family=Inter:wght@400..800&display=swap" rel="stylesheet">')

GUIA = dict(
    title="How to set up a Minecraft server in 2026 (step-by-step guide)",
    desc="A real guide to setting up a Minecraft server: how much RAM you need, which software "
         "to pick, how to get console players in with crossplay and the mistakes that ruin a server.",
    h1="How to set up a Minecraft server",
    sub="No beating around the bush and no hype. This is what I do when I set one up.",
    minutos=9,
    secciones=[
      ("First things first: your PC or rented?", """
        <p>
          You can run it on your own computer and pay nothing. It works, and for a one-off
          evening with two friends it's fine. But it has three catches nobody tells you about
          until you run into them:
        </p>
        <ul>
          <li><strong>Your PC has to stay on all the time.</strong> Turn it off to sleep and
              your friends can't play. And if you play on the same machine, the server and
              the game fight over the CPU.</li>
          <li><strong>You have to open ports on your router.</strong> With luck it takes a
              while; with your ISP's CG-NAT, you simply can't.</li>
          <li><strong>Your upload speed is what it is.</strong> You download at 600 Mbps but
              upload at 40, and upload is what matters for a server. That's why your friends
              lag even though it runs perfectly for you.</li>
        </ul>
        <p>
          Honest summary: to try things out, your PC. For a world that lasts months with
          people who don't live with you, rented. And if anyone in your group plays on
          console, renting is <em>the only</em> option.
        </p>
      """),
      ("Step 1 — Find out how much RAM you need", """
        <p>
          It's the step almost everyone skips, and then they overpay or fall short. The rule
          you'll hear everywhere — "1 GB for every 10 players" — <strong>is wrong as soon as
          you install anything</strong>.
        </p>
        <p>
          What really decides it: a 200-mod pack with 5 friends needs more RAM than a vanilla
          server with 40 people. Mods load into memory whether two people are playing or twenty.
        </p>
        <p class="cta-inline">
          <a href="/en/#calculadora">Work out your exact GB here</a> — it takes 20 seconds and
          also tells you what it costs on each host.
        </p>
      """),
      ("Step 2 — Pick the software (and no, not vanilla)", """
        <p>When you create the server you'll be asked to pick a type. In plain words:</p>
        <ul>
          <li><strong>Paper</strong> — what you want 90% of the time. It's normal Minecraft
              but <em>much</em> better optimised, supports plugins and fixes bugs the
              official server still has. Players don't need to install anything.</li>
          <li><strong>Vanilla</strong> — Mojang's official server. It runs worse on the same
              RAM and doesn't support plugins. There's no reason to pick it.</li>
          <li><strong>Fabric or NeoForge</strong> — only if you're going to play with real
              <em>mods</em>. Careful: here <strong>everyone</strong> has to install exactly
              the same mods to be able to join.</li>
        </ul>
        <p>
          The key difference: <strong>plugins</strong> (Paper) only you install on the
          server and nobody else touches anything. <strong>Mods</strong> (Fabric/Forge)
          everyone has to install. If your group complains about installing things, Paper
          and off you go.
        </p>
      """),
      ("Step 3 — Let console and mobile players in (crossplay)", """
        <p>
          This is the mess that generates the most questions. Minecraft is really two games:
          <strong>Java</strong> (PC) and <strong>Bedrock</strong> (consoles, mobile and
          Windows 10/11 from the Store). By default they can't see each other.
        </p>
        <p>The fix is two plugins, and it really works:</p>
        <ul>
          <li><strong>Geyser</strong> — makes a Java server accept Bedrock players by
              translating the connection on the fly.</li>
          <li><strong>Floodgate</strong> — so they don't also need a Java account to join.
              Without it, your cousin on Switch would have to buy the game again.</li>
        </ul>
        <p>
          You drop them in the <code>plugins</code> folder, restart, and console players join
          on <strong>port 19132</strong> (Bedrock's), not the same one as PC players. That
          detail is what makes people give up thinking it doesn't work.
        </p>
        <p>
          A realistic warning: crossplay works well but isn't perfect. Some interface bits and
          very visual plugins look odd on Bedrock. For playing together, it's more than enough.
        </p>
      """),
      ("Step 4 — The settings you do need to change", """
        <p>
          The <code>server.properties</code> file has fifty lines and only four matter:
        </p>
        <ul>
          <li><strong>view-distance</strong> — the biggest RAM eater. It defaults to 10.
              Drop it to <strong>8</strong> and you gain performance that almost nobody
              notices. Raising it to 16 can push usage up 35%.</li>
          <li><strong>simulation-distance</strong> — how far away things keep happening
              (mobs, crops, farms). 6 is fine.</li>
          <li><strong>online-mode</strong> — leave it on <code>true</code>. On
              <code>false</code> anyone can join with any name they like, including your
              admin one.</li>
          <li><strong>difficulty</strong> — set it to <code>normal</code> or
              <code>hard</code> before you start. Changing it once the world is underway
              throws everyone off.</li>
        </ul>
      """),
      ("Step 5 — Plugins: the four worth having", """
        <p>
          The temptation is to install thirty on day one. Don't: every plugin is one more
          thing that can break the server when you update. These four cover 90%:
        </p>
        <ul>
          <li><strong>EssentialsX</strong> — basic commands that should come as standard:
              <code>/home</code>, <code>/tpa</code>, <code>/spawn</code>, <code>/msg</code>.</li>
          <li><strong>LuckPerms</strong> — permissions and ranks. As soon as you want someone
              to be a moderator without giving them access to everything, you need it.</li>
          <li><strong>CoreProtect</strong> — your life insurance. It logs who placed and broke
              every block, and rolls back damage with one command. The day someone burns the
              base down, this saves the world.</li>
          <li><strong>Chunky</strong> — pre-generates the map. Without it, the server stalls
              every time someone explores new ground.</li>
        </ul>
        <p>
          And one to <em>avoid</em>: any plugin that promises "magic optimisation" and isn't
          maintained. They usually do more harm than good.
        </p>
      """),
      ("Step 6 — Backups and restarts", """
        <p>
          This is what separates a server that lasts a year from one that dies in three weeks.
          Two things, both automatic:
        </p>
        <ul>
          <li><strong>A daily backup.</strong> Any decent host does it in two clicks. A
              corrupted world with no backup means the whole world in the bin, and it happens
              more than you think.</li>
          <li><strong>An automatic restart overnight.</strong> It clears memory that builds up
              and stops the server getting a little worse every day. At 5 a.m. it bothers
              nobody.</li>
        </ul>
      """),
      ("The mistakes I see most", """
        <ul>
          <li><strong>Sizing RAM by players and forgetting the mods.</strong> Mistake number
              one, by far.</li>
          <li><strong>Leaving view distance at 16 "so it looks good".</strong> The server
              crawls and nobody knows why.</li>
          <li><strong>Not installing CoreProtect until something happens.</strong> By then
              it's useless: it only logs from the moment you install it.</li>
          <li><strong>Starting with twenty plugins.</strong> When something breaks you have no
              idea which one it is.</li>
          <li><strong>Paying for a yearly plan without trying it.</strong> Take one month
              first, bring your people in and see how it goes. Then decide.</li>
        </ul>
      """),
    ],
    faq=[
      ("How much RAM does a Minecraft server need for 10 friends?",
       "In vanilla or with a few plugins, 3 GB is plenty. With a big modpack of 100 to 250 "
       "mods, the same group of 10 goes up to 8 or 12 GB. Mods weigh more than people."),
      ("Can I play from PS5 or Switch on my own server?",
       "Yes, if the server runs Geyser and Floodgate. What you can't do is host the server "
       "from the console: it has to be on an always-on PC or at a host."),
      ("Is it legal to run a Minecraft server?",
       "Yes, as long as you don't charge for access to the game. Mojang allows servers and even "
       "selling ranks and cosmetics, but there are rules: you can't sell gameplay advantages "
       "or loot boxes for real money."),
      ("How much does a Minecraft server cost per month?",
       "It depends on the GB. A small server for friends costs €3-6 a month. One with a big "
       "modpack or a community, €7-15. Above that you're being overcharged unless it's "
       "something really big."),
    ],
)


def html():
    g = GUIA
    indice = "\n".join('        <li><a href="#s%d">%s</a></li>' % (i, t)
                       for i, (t, _) in enumerate(g["secciones"]))
    cuerpo = "\n".join('      <h2 id="s%d">%s</h2>\n%s' % (i, t, c.rstrip())
                       for i, (t, c) in enumerate(g["secciones"]))
    faq = "\n".join('      <details>\n        <summary>%s</summary>\n        <p>%s</p>\n      </details>'
                    % q for q in g["faq"])
    # guias._articulo_schema busca "Paso" en el título: en inglés es "Step"
    import json
    howto = json.dumps({
        "@context": "https://schema.org", "@type": "HowTo", "name": g["title"],
        "description": g["desc"], "totalTime": "PT%dM" % g["minutos"],
        "step": [{"@type": "HowToStep", "name": t.split("—")[-1].strip()}
                 for t, _ in g["secciones"] if t.startswith("Step")],
    }, ensure_ascii=False, indent=2)

    return """<!doctype html>
<html lang="en">
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

    <nav class="miga" aria-label="You are here"><a href="/en/">Home</a> › Guide</nav>

    <h1>%(h1)s</h1>
    <p class="sub art-sub">%(sub)s</p>
    <p class="art-meta">%(minutos)d-minute read · Updated September 2026</p>

    <nav class="indice" aria-label="Contents">
      <div class="indice-tit">What you'll read</div>
      <ol>
%(indice)s
      </ol>
    </nav>

%(cuerpo)s

    <div class="art-cierre">
      <h2 id="faq">Frequently asked questions</h2>
%(faq)s
    </div>

    <div class="art-cta">
      <h3>And how many GB do you need?</h3>
      <p>
        It's the first thing to decide and what sets the price. The calculator tells you in
        20 seconds, no sign-up, and shows you what it costs at each host.
      </p>
      <a class="cta" href="/en/#calculadora">Size my server</a>
    </div>

  </article>
</main>

<footer></footer>

<script type="application/ld+json">
%(faq_schema)s
</script>
<script type="application/ld+json">
%(howto)s
</script>
<script type="application/ld+json">
%(migas)s
</script>

<script src="/buscador_ui.js" defer></script>

</body>
</html>
""" % dict(title=g["title"], desc=g["desc"], h1=g["h1"], sub=g["sub"], minutos=g["minutos"],
           dom=DOMINIO, ruta=RUTA, fuentes=FUENTES, indice=indice, cuerpo=cuerpo, faq=faq,
           faq_schema=guias._faq_schema(g), howto=howto,
           migas=migas.schema([("Home", "/en/"), (g["h1"], None)]))
