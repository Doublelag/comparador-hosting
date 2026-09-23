# -*- coding: utf-8 -*-
"""
Plantillas de servidor: la página donde se genera el .zip listo para subir.

La página no lleva los plugins: el navegador del usuario los baja de su web
oficial (plantilla_ui.js). Aquí solo van los textos y las configuraciones,
que se leen de plantillas_src/<plantilla>/ y se meten dentro de la página.

Cada plantilla se prueba de verdad en un Paper antes de publicarla: si se
cambia `mc`, hay que volver a probarla y actualizar `probada`.

Lo importa build.py.
"""

import io
import json
import os

import paginas

RAIZ = os.path.dirname(os.path.abspath(__file__))

SMP = dict(
    id="smp-amigos",
    nombre="SMP de amigos",
    nombre_en="Friends SMP",
    zip="smp-amigos",
    # EssentialsX estable llega hasta 26.1.2. Con ViaVersion entran también
    # los que tengan el juego más nuevo, así que no hace falta ir por delante.
    mc="26.1.2",
    probada="21 de septiembre de 2026, Paper build 74",
    probada_en="21 September 2026, Paper build 74",
    plugins=[
        dict(titulo="Geyser", geyser="geyser", archivo="Geyser-Spigot.jar", bedrock=True),
        dict(titulo="Floodgate", geyser="floodgate", archivo="floodgate-spigot.jar", bedrock=True),
        dict(titulo="ViaVersion", modrinth="viaversion"),
        dict(titulo="LuckPerms", modrinth="luckperms"),
        dict(titulo="EssentialsX", modrinth="essentialsx"),
        dict(titulo="CoreProtect", modrinth="coreprotect"),
    ],
)


def _archivos(pid):
    base = os.path.join(RAIZ, "plantillas_src", pid)
    out = {}
    for d, _, fs in os.walk(base):
        for f in sorted(fs):
            ruta = os.path.join(d, f)
            out[os.path.relpath(ruta, base).replace(os.sep, "/")] = io.open(ruta, encoding="utf-8").read()
    return out


def _datos_js(p):
    d = {k: v for k, v in p.items() if k != "id"}
    d["archivos"] = _archivos(p["id"])
    return ("<script>window.PLANTILLA = %s;</script>\n"
            '<script src="/zip_ui.js" defer></script>\n'
            '<script src="/plantilla_ui.js" defer></script>'
            % json.dumps(d, ensure_ascii=False).replace("</", "<\\/"))


PLUGINS_ES = [
    ("Geyser + Floodgate", "Los de móvil, consola y Windows (Bedrock) juegan en el mismo mundo que los de PC, sin cuenta de Java."),
    ("ViaVersion", "Si a alguien se le actualiza el Minecraft, puede seguir entrando."),
    ("EssentialsX", "Casas, /tpa entre amigos, /back al morir y mensajes privados. Todo en español."),
    ("LuckPerms", "Los permisos ya vienen puestos: cada jugador puede usar lo suyo desde el primer minuto."),
    ("CoreProtect", "Si alguien rompe o roba algo, ves quién ha sido y lo deshaces con un comando."),
]
PLUGINS_EN = [
    ("Geyser + Floodgate", "Mobile, console and Windows (Bedrock) players share the same world as PC players, no Java account needed."),
    ("ViaVersion", "If someone's Minecraft updates, they can still join."),
    ("EssentialsX", "Homes, /tpa between friends, /back when you die and private messages."),
    ("LuckPerms", "Permissions are already set: every player can use their commands from minute one."),
    ("CoreProtect", "If someone breaks or steals something, you see who did it and undo it with one command."),
]


def _plugins_html(lista):
    return "\n".join('        <li><strong>%s</strong><span>%s</span></li>' % x for x in lista)


def _faq(lista):
    return "\n".join('      <details>\n        <summary>%s</summary>\n        <p>%s</p>\n      </details>'
                     % q for q in lista)


def smp(lang):
    p = SMP
    if lang == "es":
        cuerpo = """  <div class="wrap articulo plt" style="max-width:900px">
    <nav class="miga"><a href="/">Inicio</a> &rsaquo; Plantillas &rsaquo; SMP de amigos</nav>

    <span class="sec-eyebrow">Plantilla gratis</span>
    <h1>Tu server de Minecraft con amigos, <em>montado en 5 minutos</em></h1>
    <p class="sub art-sub">
      Configurar un servidor desde cero son horas de plugins, permisos y archivos.
      Aquí eliges cuatro cosas, descargas un .zip y lo subes a tu hosting. Ya está.
    </p>

    <ul class="plt-plugins">
%(plugins)s
    </ul>

    <form id="plt-form" class="card plt-form" autocomplete="off">
      <h2>Personalízala</h2>
      <label class="plt-campo">
        <span>Nombre del server <small>(lo que sale en la lista de servidores)</small></span>
        <input id="plt-nombre" type="text" maxlength="59" placeholder="Server de amigos">
      </label>
      <label class="plt-campo">
        <span>¿Cuántos vais a jugar? <b id="plt-jug-val">8</b></span>
        <input id="plt-jugadores" type="range" min="2" max="20" value="8">
        <small>Necesitarás unos <b id="plt-ram">4 GB</b> de RAM.
        <a id="plt-calc" href="/">Calcúlalo exacto</a></small>
      </label>
      <label class="plt-campo">
        <span>Dificultad</span>
        <select id="plt-dificultad">
          <option value="peaceful">Pacífico (sin monstruos)</option>
          <option value="easy">Fácil</option>
          <option value="normal" selected>Normal</option>
          <option value="hard">Difícil</option>
        </select>
      </label>
      <label class="plt-check"><input id="plt-pvp" type="checkbox" checked>
        <span>PvP activado <small>(os podéis atacar entre vosotros)</small></span></label>
      <label class="plt-check"><input id="plt-bedrock" type="checkbox" checked>
        <span>Hay gente en móvil o consola <small>(añade el crossplay; si todos jugáis en PC, quítalo y el zip pesa 55 MB menos)</small></span></label>

      <button id="plt-generar" class="cta" type="submit">Descargar mi plantilla</button>
      <progress id="plt-barra" max="100" value="0" hidden></progress>
      <p id="plt-estado" class="plt-estado" aria-live="polite">
        Los plugins se descargan de su web oficial en ese momento: siempre te llevas la última versión.
      </p>
    </form>

    <h2 id="pasos-subir">Cómo subirla a tu hosting</h2>
    <ol class="plt-pasos">
      <li><strong>Elige Paper %(mc)s</strong> en el panel de tu hosting como tipo de servidor.</li>
      <li><strong>Arráncalo una vez y apágalo.</strong> Así crea sus carpetas y acepta la EULA.</li>
      <li><strong>Sube el .zip</strong> a la carpeta principal y descomprímelo ahí. Si pregunta
        si reemplazar archivos, di que sí.</li>
      <li><strong>Arráncalo.</strong> Los de PC entran con la IP; los de Bedrock, con la misma IP
        y el mismo puerto.</li>
      <li><strong>Hazte admin:</strong> en la consola del panel escribe <code>op TuNombre</code>.</li>
    </ol>
    <p>Dentro del zip va un <code>LEEME.txt</code> con los comandos, cómo deshacer destrozos y cómo
      dejar el server solo para tus amigos.</p>

    <div class="plt-host">
      <div>
        <h3>¿Aún no tienes hosting?</h3>
        <p>Para empezar, <strong>Godlike.host</strong> tiene el mayor descuento de la comparativa:
          <strong>−75 %% el primer mes</strong> con el código <strong>DOUBLELAG</strong>. Y antes de pagar nada, te dejan
          <strong>un servidor gratis durante un día</strong> para probarlo.</p>
      </div>
      <div class="plt-host-botones">
        <a class="cta" href="/hosting/godlike/">Ver Godlike.host</a>
        <a class="cta-ghost" href="/hosting/">Comparar todos</a>
      </div>
    </div>

    <div class="art-cierre">
      <h2 id="faq">Preguntas frecuentes</h2>
%(faq)s
    </div>

    <p class="art-meta">Probada en un servidor real el %(probada)s.</p>
  </div>"""
        faq = [
            ("¿Es gratis?", "Sí, entera. No hay que registrarse ni dejar el correo."),
            ("¿De dónde salen los plugins?",
             "De su web oficial (Modrinth y GeyserMC). Tu navegador los descarga en el momento "
             "de darle al botón y monta el zip en tu ordenador: esta web no aloja ni modifica "
             "ningún plugin."),
            ("¿Por qué Paper %s y no la última versión?" % p["mc"],
             "Porque es la más nueva en la que todos los plugins están probados y funcionan. "
             "Con ViaVersion, los que tengan el juego actualizado entran igual, así que no "
             "notaréis nada."),
            ("¿Funciona en cualquier hosting?",
             "En cualquiera que te deje usar Paper y subir archivos, que son casi todos. Si tu "
             "hosting te da un puerto aparte para Bedrock, el LEEME explica qué línea cambiar."),
            ("He subido el zip y nadie puede entrar",
             "El zip trae su propio <code>server.properties</code>. Casi todos los paneles "
             "vuelven a poner tu puerto solos al arrancar; si el tuyo no, abre ese archivo y "
             "añade <code>server-port=</code> con el puerto que te da tu hosting."),
            ("¿Y si lo quiero montar en mi PC?",
             "También vale: descarga Paper %s de papermc.io, ponlo en una carpeta, descomprime el "
             "zip al lado y arráncalo. Eso sí, tu PC tiene que estar encendido para que jueguen "
             "los demás." % p["mc"]),
        ]
        return paginas.pagina(
            "es", "/plantillas/smp-amigos/",
            "Plantilla gratis: servidor de Minecraft con amigos listo en 5 minutos",
            "Descarga un servidor de Minecraft ya configurado: crossplay Java y Bedrock, casas, "
            "/tpa, anti-destrozos y permisos hechos. Eliges cuatro cosas y lo subes a tu hosting.",
            cuerpo % dict(plugins=_plugins_html(PLUGINS_ES), mc=p["mc"], probada=p["probada"],
                          faq=_faq(faq)),
            _datos_js(p), og_type="website")

    cuerpo = """  <div class="wrap articulo plt" style="max-width:900px">
    <nav class="miga"><a href="/en/">Home</a> &rsaquo; Templates &rsaquo; Friends SMP</nav>

    <span class="sec-eyebrow">Free template</span>
    <h1>Your Minecraft server with friends, <em>set up in 5 minutes</em></h1>
    <p class="sub art-sub">
      Setting up a server from scratch takes hours of plugins, permissions and config files.
      Here you pick four things, download a .zip and upload it to your host. Done.
    </p>

    <ul class="plt-plugins">
%(plugins)s
    </ul>

    <form id="plt-form" class="card plt-form" autocomplete="off">
      <h2>Customise it</h2>
      <label class="plt-campo">
        <span>Server name <small>(what shows in the server list)</small></span>
        <input id="plt-nombre" type="text" maxlength="59" placeholder="Friends server">
      </label>
      <label class="plt-campo">
        <span>How many of you will play? <b id="plt-jug-val">8</b></span>
        <input id="plt-jugadores" type="range" min="2" max="20" value="8">
        <small>You'll need around <b id="plt-ram">4 GB</b> of RAM.
        <a id="plt-calc" href="/en/">Work it out exactly</a></small>
      </label>
      <label class="plt-campo">
        <span>Difficulty</span>
        <select id="plt-dificultad">
          <option value="peaceful">Peaceful (no monsters)</option>
          <option value="easy">Easy</option>
          <option value="normal" selected>Normal</option>
          <option value="hard">Hard</option>
        </select>
      </label>
      <label class="plt-check"><input id="plt-pvp" type="checkbox" checked>
        <span>PvP on <small>(you can attack each other)</small></span></label>
      <label class="plt-check"><input id="plt-bedrock" type="checkbox" checked>
        <span>Some people play on mobile or console <small>(adds crossplay; if you're all on PC, untick it and the zip is 55 MB smaller)</small></span></label>

      <button id="plt-generar" class="cta" type="submit">Download my template</button>
      <progress id="plt-barra" max="100" value="0" hidden></progress>
      <p id="plt-estado" class="plt-estado" aria-live="polite">
        Plugins are downloaded from their official site right then: you always get the latest version.
      </p>
    </form>

    <h2 id="pasos-subir">How to upload it to your host</h2>
    <ol class="plt-pasos">
      <li><strong>Pick Paper %(mc)s</strong> as the server type in your host's panel.</li>
      <li><strong>Start it once and stop it.</strong> That creates its folders and accepts the EULA.</li>
      <li><strong>Upload the .zip</strong> to the main folder and extract it there. If it asks
        whether to replace files, say yes.</li>
      <li><strong>Start it.</strong> PC players join with the IP; Bedrock players with the same IP
        and the same port.</li>
      <li><strong>Make yourself admin:</strong> in the panel's console type <code>op YourName</code>.</li>
    </ol>
    <p>Inside the zip there's a <code>README.txt</code> with the commands, how to undo griefing and
      how to make the server friends-only.</p>

    <div class="plt-host">
      <div>
        <h3>No host yet?</h3>
        <p>To start with, <strong>Godlike.host</strong> has the biggest discount in the comparison:
          <strong>−75%% off the first month</strong> with the code <strong>DOUBLELAG</strong>. And before paying anything, they
          give you <strong>a free server for a day</strong> to try it out.</p>
      </div>
      <div class="plt-host-botones">
        <a class="cta" href="/en/hosting/godlike/">See Godlike.host</a>
        <a class="cta-ghost" href="/en/hosting/">Compare them all</a>
      </div>
    </div>

    <div class="art-cierre">
      <h2 id="faq">Frequently asked questions</h2>
%(faq)s
    </div>

    <p class="art-meta">Tested on a real server on %(probada)s.</p>
  </div>"""
    faq = [
        ("Is it free?", "Yes, all of it. No sign-up, no email."),
        ("Where do the plugins come from?",
         "From their official site (Modrinth and GeyserMC). Your browser downloads them when "
         "you press the button and builds the zip on your computer: this site doesn't host or "
         "modify any plugin."),
        ("Why Paper %s and not the latest version?" % p["mc"],
         "Because it's the newest one where every plugin is tested and works. With ViaVersion, "
         "people on an updated game can still join, so you won't notice a thing."),
        ("Does it work on any host?",
         "On any host that lets you run Paper and upload files, which is nearly all of them. If "
         "your host gives you a separate Bedrock port, the README explains which line to change."),
        ("I uploaded the zip and nobody can join",
         "The zip has its own <code>server.properties</code>. Almost every panel puts your "
         "port back automatically on start; if yours doesn't, open that file and add "
         "<code>server-port=</code> with the port your host gives you."),
        ("What if I want to run it on my PC?",
         "That works too: download Paper %s from papermc.io, put it in a folder, extract the zip "
         "next to it and start it. Your PC has to stay on for the others to play, though." % p["mc"]),
    ]
    return paginas.pagina(
        "en", "/en/templates/friends-smp/",
        "Free template: a Minecraft server for friends ready in 5 minutes",
        "Download a ready-made Minecraft server: Java and Bedrock crossplay, homes, /tpa, "
        "anti-griefing and permissions done. Pick four things and upload it to your host.",
        cuerpo % dict(plugins=_plugins_html(PLUGINS_EN), mc=p["mc"], probada=p["probada_en"],
                      faq=_faq(faq)),
        _datos_js(p), og_type="website")


# ---------------------------------------------------------------------------
# EL ÍNDICE /plantillas/  (las dos clases de plantilla)
# ---------------------------------------------------------------------------
def indice(lang):
    es = lang == "es"
    pre = "" if es else "/en"
    smp = pre + ("/plantillas/smp-amigos/" if es else "/templates/friends-smp/")
    mods = pre + ("/plantillas/modpacks/" if es else "/templates/modpacks/")
    if es:
        cuerpo = """  <div class="wrap articulo plt" style="max-width:900px">
    <nav class="miga"><a href="/">Inicio</a> &rsaquo; Plantillas</nav>

    <span class="sec-eyebrow">Plantillas</span>
    <h1>Tu servidor, <em>ya configurado</em></h1>
    <p class="sub art-sub">
      Montar un servidor desde cero son horas de plugins, permisos y archivos que nadie
      te explica. Aquí te lo doy hecho: eliges, descargas y lo subes.
    </p>

    <div class="cat-grid" style="margin:26px 0 30px">
      <a class="cat-card" href="%(smp)s">
        <span class="cat-tit">SMP de amigos</span>
        <span class="cat-txt">Un .zip con todo puesto: crossplay con móvil y consola, casas,
          /tpa, anti-destrozos y permisos hechos. Lo subes y en 5 minutos estáis dentro.</span>
      </a>
      <a class="cat-card" href="%(mods)s">
        <span class="cat-tit">Modpacks</span>
        <span class="cat-txt">Los packs más jugados con sus datos reales, la RAM que piden
          según cuántos seáis y los ajustes para que no vaya a tirones.</span>
      </a>
    </div>

    <div class="art-cta">
      <h3>¿No sabes cuánta RAM necesitas?</h3>
      <p>Dime cuántos sois y qué lleváis instalado y te lo digo en 20 segundos, con lo que
        cuesta en cada hosting.</p>
      <div class="hero-cta"><a class="cta" href="/#calculadora">Calcular mi servidor</a></div>
    </div>
  </div>""" % dict(smp=smp, mods=mods)
        return paginas.pagina("es", "/plantillas/",
                              "Plantillas de servidor de Minecraft, gratis y ya configuradas",
                              "Un servidor de Minecraft ya montado: plantilla de SMP con amigos "
                              "lista para subir y los modpacks más jugados con la RAM que piden.",
                              cuerpo, og_type="website")

    cuerpo = """  <div class="wrap articulo plt" style="max-width:900px">
    <nav class="miga"><a href="/en/">Home</a> &rsaquo; Templates</nav>

    <span class="sec-eyebrow">Templates</span>
    <h1>Your server, <em>already set up</em></h1>
    <p class="sub art-sub">
      Setting up a server from scratch is hours of plugins, permissions and config files
      nobody explains. Here it's done for you: pick one, download it, upload it.
    </p>

    <div class="cat-grid" style="margin:26px 0 30px">
      <a class="cat-card" href="%(smp)s">
        <span class="cat-tit">Friends SMP</span>
        <span class="cat-txt">A .zip with everything set: crossplay with mobile and console,
          homes, /tpa, anti-griefing and permissions done. Upload it and you're in.</span>
      </a>
      <a class="cat-card" href="%(mods)s">
        <span class="cat-tit">Modpacks</span>
        <span class="cat-txt">The most played packs with their real data, the RAM they need
          for your group size and the settings that stop the stutter.</span>
      </a>
    </div>

    <div class="art-cta">
      <h3>Not sure how much RAM you need?</h3>
      <p>Tell me how many of you there are and what you've got installed and I'll tell you
        in 20 seconds, with what it costs on each host.</p>
      <div class="hero-cta"><a class="cta" href="/en/#calculadora">Size my server</a></div>
    </div>
  </div>""" % dict(smp=smp, mods=mods)
    return paginas.pagina("en", "/en/templates/",
                          "Free Minecraft server templates, already configured",
                          "A Minecraft server already set up: a friends SMP template ready to "
                          "upload and the most played modpacks with the RAM they need.",
                          cuerpo, og_type="website")


TODAS = [
    ("/plantillas/", lambda: indice("es")),
    ("/en/templates/", lambda: indice("en")),
    ("/plantillas/smp-amigos/", lambda: smp("es")),
    ("/en/templates/friends-smp/", lambda: smp("en")),
]
