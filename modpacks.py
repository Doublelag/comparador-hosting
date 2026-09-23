# -*- coding: utf-8 -*-
"""
Plantillas de modpacks: /plantillas/modpacks/ y /en/templates/modpacks/.

Qué resuelve: la gente elige el modpack por el vídeo que ha visto y luego
contrata 2 GB porque era el plan barato. Aquí, para cada modpack famoso, están
los datos que de verdad deciden — versión, cargador, cuántos mods lleva — y la
RAM que hace falta según cuántos seáis, con el mismo cálculo que la calculadora
de la portada.

Los packs NO se alojan aquí: cada uno se instala desde el panel del hosting o
desde su página oficial. Lo que se descarga es el paquete de ajustes
(server.properties, argumentos de arranque y las instrucciones), que es lo que
nadie te da y lo que hace que un modpack vaya fino o a tirones.

Los números (mods, versión, descargas) salen de la API de Modrinth y están
comprobados en la fecha de COMPROBADO. Si se actualiza un pack, se vuelven a
mirar: aquí no se inventa nada.

Lo importa build.py.
"""

import io
import json
import os

import paginas

RAIZ = os.path.dirname(os.path.abspath(__file__))
COMPROBADO = "23 de septiembre de 2026"
COMPROBADO_EN = "23 September 2026"

# ---------------------------------------------------------------------------
# LOS PACKS. mods/mc/cargador/descargas: datos reales de Modrinth.
# "peso" es cómo lo trata la calculadora: ligero (<100 mods), grande (100-250)
# o bestia (250+). Pixelmon es la excepción a mano: son pocos archivos pero un
# mod gigante, así que pesa como uno grande.
# ---------------------------------------------------------------------------
# Iconos por género, con el mismo trazo que los de la portada.
ICONOS = {
 "pokemon": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h6M15 12h6"/><circle cx="12" cy="12" r="3"/></svg>',
 "mundo": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 20h18M5 20V9l7-5 7 5v11"/><path d="M10 20v-6h4v6"/></svg>',
 "magia": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m5 19 9-9M14 4l1.5 3L19 8.5 15.5 10 14 13l-1.5-3L9 8.5 12.5 7z"/><path d="m18 16 .8 1.7 1.7.8-1.7.8-.8 1.7-.8-1.7-1.7-.8 1.7-.8z"/></svg>',
 "zombi": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="4" y="4" width="16" height="16" rx="3"/><path d="M9 10h.01M15 10h.01M8 16h8"/></svg>',
 "slime": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 18a7 7 0 0 1 14 0z"/><path d="M9 13h.01M15 13h.01"/><path d="M4 21h16"/></svg>',
 "terror": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 21V10a7 7 0 0 1 14 0v11l-3-2-2 2-2-2-2 2-2-2z"/><path d="M9 11h.01M15 11h.01"/></svg>',
 "maquinas": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M19.1 4.9 17 7M7 17l-2.1 2.1"/></svg>',
}

PACKS = [
    dict(slug="cobbleverse", icono="pokemon", nombre="COBBLEVERSE", mods=168, mc="1.21.1",
         cargador="Fabric", descargas=6742460, peso="grande",
         que="Pokémon en Minecraft de verdad: gimnasios, líderes, liga y progresión, "
             "montado sobre Cobblemon. El que más se pide para jugar con amigos.",
         que_en="Proper Pokémon in Minecraft: gyms, leaders, a league and progression, "
                "built on Cobblemon. The one people ask for most to play with friends."),
    dict(slug="better-mc-fabric-bmc2", icono="mundo", nombre="Better MC [FABRIC] BMC2", mods=336, mc="1.20.1",
         cargador="Fabric", descargas=3459280, peso="bestia",
         que="Minecraft con todo puesto: estructuras, mobs, mazmorras y mejoras por todas "
             "partes, sin cambiarte el juego de sitio. También existe en Forge (BMC4).",
         que_en="Minecraft with everything on: structures, mobs, dungeons and improvements "
                "everywhere, without turning it into another game. Also on Forge (BMC4)."),
    dict(slug="prominence-2-fabric", icono="magia", nombre="Prominence II: Hasturian Era", mods=555, mc="1.20.1",
         cargador="Fabric", descargas=2015607, peso="bestia",
         que="Aventura con magia, clases y misiones. 555 mods: de los más pesados que hay, "
             "y se nota en la factura del hosting.",
         que_en="Adventure with magic, classes and quests. 555 mods: one of the heaviest "
                "there is, and it shows on the hosting bill."),
    dict(slug="the-pixelmon-modpack", icono="pokemon", nombre="The Pixelmon Modpack", mods=14, mc="1.21.1",
         cargador="NeoForge", descargas=2192923, peso="grande",
         que="El Pixelmon de siempre, con su propio sistema de Pokémon. Son pocos archivos "
             "porque el mod es uno solo, pero enorme: cuenta como modpack grande.",
         que_en="Classic Pixelmon, with its own Pokémon system. Few files because it's one "
                "single mod, but a huge one: count it as a big modpack."),
    dict(slug="zombie-invade-100-days", icono="zombi", nombre="Zombie Invade 100 Days", mods=129, mc="1.20.1",
         cargador="Forge", descargas=14560426, peso="grande",
         que="El reto de los 100 días con zombis, armas y oleadas. El más descargado de "
             "todos, y de los que mejor funcionan en grupo.",
         que_en="The 100-days challenge with zombies, guns and waves. The most downloaded "
                "of them all, and one of the best in a group."),
    dict(slug="slimes-adventure", icono="slime", nombre="Slimes Adventure", mods=105, mc="1.21.1",
         cargador="Fabric", descargas=1964867, peso="grande",
         que="Aventura con slimes, mazmorras y jefes, en la versión nueva del juego. "
             "Equilibrado: entretiene sin pedir una máquina de guerra.",
         que_en="Adventure with slimes, dungeons and bosses, on the newest version. "
                "Balanced: plenty to do without needing a monster machine."),
    dict(slug="cave-horror-project-modpack", icono="terror", nombre="Cave Horror Project", mods=136, mc="1.20.1",
         cargador="Forge", descargas=1826534, peso="grande",
         que="Terror en las cuevas: criaturas, oscuridad y sustos. Es el que mejor funciona "
             "para una noche de directo con amigos.",
         que_en="Cave horror: creatures, darkness and jump scares. The best one for a "
                "streaming night with friends."),
    dict(slug="create-live-5", icono="maquinas", nombre="Create Live 5", mods=95, mc="1.20.1",
         cargador="Forge", descargas=253036, peso="grande",
         que="El pack de Create: máquinas, trenes y fábricas enormes. Aquí la RAM importa "
             "menos que el procesador, porque las máquinas van por tick.",
         que_en="The Create pack: machines, trains and huge factories. Here RAM matters "
                "less than the CPU, because machines run every tick."),
]

# La calculadora de la portada, en tres líneas: escalón base por jugadores y
# multiplicador por lo que lleva instalado. Si cambia allí, cambia aquí.
TIERS = [(4, 2), (10, 3), (20, 4), (40, 6), (70, 8), (120, 12), (200, 16)]
PESOS = {"ligero": (2.0, 6), "grande": (2.5, 8), "bestia": (3.0, 12)}
ESCALONES = [2, 3, 4, 5, 6, 8, 10, 12, 14, 16, 20, 24, 32, 48, 64]
# id del paso 2 de la calculadora, para enlazar el caso ya relleno
MOD_ID = {"ligero": "light", "grande": "heavy", "bestia": "insane"}


def ram(jugadores, peso):
    base = next((gb for tope, gb in TIERS if jugadores <= tope), TIERS[-1][1])
    mult, suelo = PESOS[peso]
    gb = max(base * mult, suelo)
    import math
    gb = math.ceil(gb)
    return next((e for e in ESCALONES if gb <= e), ESCALONES[-1])


def _datos_js():
    d = [dict(slug=p["slug"], nombre=p["nombre"], mc=p["mc"], cargador=p["cargador"],
              peso=p["peso"], mods=p["mods"]) for p in PACKS]
    return ("<script>window.MODPACKS = %s;</script>\n"
            '<script src="/zip_ui.js" defer></script>\n'
            '<script src="/modpack_ui.js" defer></script>'
            % json.dumps(d, ensure_ascii=False))


def _miles(n, lang):
    s = "{:,}".format(n)
    return s.replace(",", "." if lang == "es" else ",")


def _tarjetas(lang):
    fuera = []
    for p in PACKS:
        t = dict(
            n=p["nombre"], slug=p["slug"], mc=p["mc"], carg=p["cargador"],
            ico=ICONOS.get(p.get("icono", ""), ""),
            mods=p["mods"], dl=_miles(p["descargas"], lang),
            que=p["que"] if lang == "es" else p["que_en"],
            r5=ram(5, p["peso"]), r10=ram(10, p["peso"]), r20=ram(20, p["peso"]),
            calc=("/" if lang == "es" else "/en/") + "?p=10&m=" + MOD_ID[p["peso"]] + "#calculadora",
            pre="" if lang == "es" else "/en",
        )
        if lang == "es":
            t.update(lbl_mods="mods", lbl_dl="descargas", lbl_ram="RAM que necesitáis",
                     j="jugadores", ver="Ver el pack", ajustes="Descargar ajustes",
                     calct="Calcular mi caso")
        else:
            t.update(lbl_mods="mods", lbl_dl="downloads", lbl_ram="RAM you'll need",
                     j="players", ver="See the pack", ajustes="Download settings",
                     calct="Work out my case")
        fuera.append("""      <article class="mp-card" data-pack="%(slug)s">
        <div class="mp-head"><span class="cat-ico mp-ico">%(ico)s</span><h3>%(n)s</h3></div>
        <p class="mp-que">%(que)s</p>
        <ul class="mp-datos">
          <li><b>%(mc)s</b><span>%(carg)s</span></li>
          <li><b>%(mods)s</b><span>%(lbl_mods)s</span></li>
          <li><b>%(dl)s</b><span>%(lbl_dl)s</span></li>
        </ul>
        <p class="mp-ram-tit">%(lbl_ram)s</p>
        <ul class="mp-ram">
          <li><b>%(r5)s GB</b><span>5 %(j)s</span></li>
          <li><b>%(r10)s GB</b><span>10 %(j)s</span></li>
          <li><b>%(r20)s GB</b><span>20 %(j)s</span></li>
        </ul>
        <div class="mp-botones">
          <button class="cta-mini" type="button" data-ajustes="%(slug)s">%(ajustes)s</button>
          <a class="cta-mini" href="%(calc)s">%(calct)s</a>
          <a class="cta-mini" href="https://modrinth.com/modpack/%(slug)s" rel="nofollow noopener" target="_blank">%(ver)s</a>
        </div>
      </article>""" % t)
    return "\n".join(fuera)


def html(lang):
    if lang == "es":
        cuerpo = """  <div class="wrap articulo plt" style="max-width:1000px">
    <nav class="miga"><a href="/">Inicio</a> &rsaquo; Plantillas &rsaquo; Modpacks</nav>

    <span class="sec-eyebrow">Plantillas</span>
    <h1>Los mejores <em>modpacks</em> y la RAM que piden de verdad</h1>
    <p class="sub art-sub">
      El error más caro al montar un server de modpack es contratar por el precio y no
      por lo que pide el pack. Aquí tienes los más jugados con sus datos reales
      &mdash; versión, cargador y cuántos mods llevan &mdash; y los gigas que hacen falta
      según cuántos seáis.
    </p>

    <div class="indep" style="margin:22px 0">
      <span class="indep-ico" aria-hidden="true">&#9881;</span>
      <p>
        <strong>Los modpacks no se descargan de aquí.</strong> Se instalan desde el panel de
        tu hosting (casi todos los tienen de un clic) o desde su página oficial. Lo que
        te llevas de esta web es el <strong>paquete de ajustes</strong>: el
        <code>server.properties</code> afinado para ese pack, los argumentos de arranque
        que evitan los tirones y las instrucciones paso a paso.
      </p>
    </div>

    <div class="mp-grid">
%(tarjetas)s
    </div>

    <h2 id="por-que">Por qué un modpack pide tanta RAM</h2>
    <p>
      Cada mod mete sus bloques, sus objetos y sus recetas, y todo eso vive en memoria
      mientras el server está encendido. Por eso un pack de 500 mods con cuatro amigos
      pide más gigas que un vanilla con treinta personas. Los números de arriba salen del
      mismo cálculo que la calculadora de la portada: escalón por jugadores, multiplicado
      por lo que pesa el pack.
    </p>
    <p>
      Y un aviso que te ahorra dinero: <strong>pasarte de RAM no hace que vaya más
      rápido</strong>. Lo que de verdad mueve un modpack es la velocidad del procesador
      por núcleo, porque Minecraft va casi todo en un solo hilo. Por eso en el comparador
      sale el procesador de cada hosting.
    </p>

    <div class="art-cta" style="margin-top:30px">
      <h3>¿Y cuánto cuesta eso al mes?</h3>
      <p>
        Dime cuántos sois y qué pack lleváis y te digo los gigas exactos y lo que cuesta
        en cada hosting, con el descuento de entrada y la tarifa normal por separado.
      </p>
      <div class="hero-cta">
        <a class="cta" href="/#calculadora">Calcular mi servidor</a>
        <a class="cta-ghost" href="/hosting/">Ver el comparador</a>
      </div>
    </div>

    <p class="art-meta">Datos de los packs comprobados el %(comprobado)s en Modrinth.</p>
  </div>"""
        return paginas.pagina(
            "es", "/plantillas/modpacks/",
            "Los mejores modpacks de Minecraft y cuánta RAM necesita cada uno (2026)",
            "COBBLEVERSE, Better MC, Prominence II, Pixelmon… los modpacks más jugados con su "
            "versión, su cargador, cuántos mods llevan y los GB de RAM que piden según cuántos seáis.",
            cuerpo % dict(tarjetas=_tarjetas("es"), comprobado=COMPROBADO),
            _datos_js(), og_type="website")

    cuerpo = """  <div class="wrap articulo plt" style="max-width:1000px">
    <nav class="miga"><a href="/en/">Home</a> &rsaquo; Templates &rsaquo; Modpacks</nav>

    <span class="sec-eyebrow">Templates</span>
    <h1>The best <em>modpacks</em> and the RAM they really need</h1>
    <p class="sub art-sub">
      The costliest mistake when setting up a modpack server is buying on price instead of
      what the pack actually needs. Here are the most played ones with their real data
      &mdash; version, loader and how many mods they carry &mdash; and the gigabytes you
      need depending on how many of you there are.
    </p>

    <div class="indep" style="margin:22px 0">
      <span class="indep-ico" aria-hidden="true">&#9881;</span>
      <p>
        <strong>The modpacks aren't downloaded from here.</strong> You install them from
        your host's panel (nearly all have one-click installers) or from their official
        page. What you get from this site is the <strong>settings pack</strong>: a
        <code>server.properties</code> tuned for that pack, the startup arguments that
        stop the stutter, and step-by-step instructions.
      </p>
    </div>

    <div class="mp-grid">
%(tarjetas)s
    </div>

    <h2 id="why">Why a modpack needs so much RAM</h2>
    <p>
      Every mod adds its blocks, items and recipes, and all of that sits in memory while
      the server is up. That's why a 500-mod pack with four friends needs more gigabytes
      than vanilla with thirty people. The numbers above come from the same maths as the
      calculator on the home page: a tier by player count, multiplied by how heavy the
      pack is.
    </p>
    <p>
      And one warning that saves you money: <strong>more RAM doesn't make it faster</strong>.
      What actually moves a modpack is single-core CPU speed, because Minecraft runs
      almost everything on one thread. That's why the comparison lists each host's CPU.
    </p>

    <div class="art-cta" style="margin-top:30px">
      <h3>So what does that cost a month?</h3>
      <p>
        Tell me how many of you there are and which pack you run, and I'll tell you the
        exact gigabytes and what it costs on each host, with the entry discount and the
        normal rate kept apart.
      </p>
      <div class="hero-cta">
        <a class="cta" href="/en/#calculadora">Size my server</a>
        <a class="cta-ghost" href="/en/hosting/">See the comparison</a>
      </div>
    </div>

    <p class="art-meta">Pack data checked on %(comprobado)s on Modrinth.</p>
  </div>"""
    return paginas.pagina(
        "en", "/en/templates/modpacks/",
        "The best Minecraft modpacks and how much RAM each one needs (2026)",
        "COBBLEVERSE, Better MC, Prominence II, Pixelmon… the most played modpacks with their "
        "version, loader, mod count and the GB of RAM they need depending on your group size.",
        cuerpo % dict(tarjetas=_tarjetas("en"), comprobado=COMPROBADO_EN),
        _datos_js(), og_type="website")


TODAS = [
    ("/plantillas/modpacks/", lambda: html("es")),
    ("/en/templates/modpacks/", lambda: html("en")),
]
