# -*- coding: utf-8 -*-
"""
Páginas sueltas que no salen de la tabla de precios: las legales (privacidad,
cookies, aviso legal) y la de ChorizoSMP, el servidor de Doublelag.

Cada una en español y en inglés. La cabecera y el pie los pone marco.py
después, así que aquí solo va lo de dentro.

Lo importa build.py.
"""

import html as _html

import partner
import sitio

DOMINIO = "https://montatuserver.com"
FUENTES = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
           '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
           '<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700'
           '&family=Inter:wght@400..800&display=swap" rel="stylesheet">')


def pagina(lang, ruta, titulo, desc, cuerpo, extra_js="", og_type="article"):
    return """<!doctype html>
<html lang="%(lang)s">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(titulo)s</title>
<meta name="description" content="%(desc)s">
<link rel="canonical" href="%(dom)s%(ruta)s">
<meta property="og:type" content="%(og_type)s">
<meta property="og:site_name" content="MontaTuServer">
<meta property="og:url" content="%(dom)s%(ruta)s">
<meta property="og:title" content="%(titulo)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:image" content="%(dom)s/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
%(fuentes)s
<link rel="stylesheet" href="/styles.css">
</head>
<body>

<header class="site-head"></header>

<main>
%(cuerpo)s
</main>

<footer></footer>

<script src="/buscador_ui.js" defer></script>
%(extra_js)s
</body>
</html>
""" % dict(lang=lang, titulo=_html.escape(titulo), desc=_html.escape(desc), dom=DOMINIO,
           ruta=ruta, og_type=og_type, fuentes=FUENTES, cuerpo=cuerpo, extra_js=extra_js)


def _fila(etiqueta, valor, lang, correo=False):
    """Una fila de los datos del titular. Si el dato no está, no se inventa ni
    se enseña un hueco: la fila no sale."""
    if not valor:
        return ""
    v = _html.escape(valor)
    if correo:
        v = '<a href="mailto:%s">%s</a>' % (v, v)
    return "      <li><strong>%s:</strong> %s</li>\n" % (etiqueta, v)


def _dato(valor, lang):
    if valor:
        return _html.escape(valor)
    return ('<span class="pendiente">pendiente de completar</span>' if lang == "es"
            else '<span class="pendiente">to be completed</span>')


# =============================================================================
# AVISO LEGAL
# =============================================================================
def aviso_legal(lang):
    t, n, e, d = (_dato(sitio.TITULAR, lang), _dato(sitio.NIF, lang),
                  _dato(sitio.EMAIL, lang), _dato(sitio.DOMICILIO, lang))
    if lang == "es":
        afil = ("<p>Algunos enlaces de esta web son <strong>enlaces de afiliado</strong>: "
                "si contratas a través de ellos, el titular cobra una comisión sin coste "
                "extra para ti. Eso no cambia el orden de las tablas, que va por precio.</p>"
                if partner.activo() else
                "<p>Ahora mismo esta web no tiene acuerdos de afiliación con ningún hosting.</p>")
        cuerpo = """  <article class="wrap articulo legal">
    <h1>Aviso legal</h1>
    <p class="art-meta">Última actualización: septiembre de 2026</p>

    <h2>Quién está detrás</h2>
    <p>En cumplimiento del artículo 10 de la Ley 34/2002, de Servicios de la Sociedad
    de la Información (LSSI), estos son los datos del titular de montatuserver.com:</p>
    <ul class="datos-legales">
%(filas)s    </ul>

    <h2>Qué es esta web</h2>
    <p>MontaTuServer es una calculadora de RAM para servidores de Minecraft y un
    comparador de precios de hosting. No vende servidores ni cobra por usarla.</p>
    %(afil)s

    <h2>Los precios</h2>
    <p>Los precios se comprueban a mano en la web de cada hosting y se indica la
    fecha. Los hostings los cambian sin avisar, así que lo que manda siempre es lo
    que diga su web en el momento de contratar. Si ves un precio que no cuadra,
    escríbeme y lo corrijo.</p>

    <h2>Propiedad intelectual</h2>
    <p>Los textos, el diseño y el código de esta web son del titular. Los nombres y
    logotipos de los hostings pertenecen a sus dueños y se citan solo para
    compararlos. Minecraft es una marca de Mojang Studios; esta web no está
    afiliada a Mojang ni a Microsoft.</p>

    <h2>Enlaces a otras webs</h2>
    <p>Esta web enlaza a las páginas de los hostings y a otras webs. No respondo de
    su contenido ni de sus condiciones: cuando sales de aquí, se aplican las suyas.</p>

    <h2>Ley aplicable</h2>
    <p>Este aviso se rige por la ley española.</p>
  </article>""" % dict(filas=(_fila("Titular", sitio.TITULAR, lang)
                             + _fila("NIF", sitio.NIF, lang)
                             + _fila("Correo de contacto", sitio.EMAIL, lang, correo=True)
                             + _fila("Domicilio", sitio.DOMICILIO, lang)), afil=afil)
        return pagina("es", "/aviso-legal/", "Aviso legal · MontaTuServer",
                      "Quién está detrás de MontaTuServer y en qué condiciones se usa la web.", cuerpo)

    afil = ("<p>Some links on this site are <strong>affiliate links</strong>: if you buy "
            "through them, the owner earns a commission at no extra cost to you. That "
            "doesn't change the order of the tables, which is by price.</p>"
            if partner.activo() else
            "<p>This site currently has no affiliate agreement with any host.</p>")
    cuerpo = """  <article class="wrap articulo legal">
    <h1>Legal notice</h1>
    <p class="art-meta">Last updated: September 2026</p>

    <h2>Who runs this site</h2>
    <p>As required by article 10 of Spanish Law 34/2002 on Information Society
    Services (LSSI), these are the details of the owner of montatuserver.com:</p>
    <ul class="datos-legales">
%(filas)s    </ul>

    <h2>What this site is</h2>
    <p>MontaTuServer is a RAM calculator for Minecraft servers and a hosting price
    comparison. It doesn't sell servers and it's free to use.</p>
    %(afil)s

    <h2>Prices</h2>
    <p>Prices are checked by hand on each host's website, with the date shown. Hosts
    change them without notice, so what counts is always what their site says when
    you buy. If you spot a price that doesn't match, write to me and I'll fix it.</p>

    <h2>Intellectual property</h2>
    <p>The text, design and code of this site belong to its owner. Host names and
    logos belong to their owners and are only mentioned to compare them. Minecraft
    is a trademark of Mojang Studios; this site is not affiliated with Mojang or
    Microsoft.</p>

    <h2>Links to other sites</h2>
    <p>This site links to hosting providers and other websites. I'm not responsible
    for their content or terms: once you leave, theirs apply.</p>

    <h2>Governing law</h2>
    <p>This notice is governed by Spanish law.</p>
  </article>""" % dict(filas=(_fila("Owner", sitio.TITULAR, lang)
                           + _fila("Tax ID", sitio.NIF, lang)
                           + _fila("Contact email", sitio.EMAIL, lang, correo=True)
                           + _fila("Address", sitio.DOMICILIO, lang)), afil=afil)
    return pagina("en", "/en/legal-notice/", "Legal notice · MontaTuServer",
                  "Who runs MontaTuServer and the terms for using the site.", cuerpo)


# =============================================================================
# PRIVACIDAD
# =============================================================================
def privacidad(lang):
    e = _dato(sitio.EMAIL, lang)
    t = _dato(sitio.TITULAR, lang)
    if lang == "es":
        cuerpo = """  <article class="wrap articulo legal">
    <h1>Política de privacidad</h1>
    <p class="art-meta">Última actualización: septiembre de 2026</p>

    <p class="legal-resumen"><strong>En corto:</strong> esta web no te pide ningún dato,
    no tiene cuentas ni formularios, no usa analítica y no instala cookies.</p>

    <h2>Responsable</h2>
    <p>%(t)s. Contacto: %(e)s.</p>

    <h2>Qué datos se tratan</h2>
    <ul>
      <li><strong>Ninguno que tú escribas.</strong> No hay registro, ni formularios, ni
      comentarios.</li>
      <li><strong>Datos técnicos del alojamiento.</strong> La web está alojada en Netlify
      (Netlify, Inc., Estados Unidos), que como cualquier servidor registra datos
      técnicos de las visitas, como la dirección IP y el navegador, para servir la
      página y protegerla de ataques. Netlify se acoge al Marco de Privacidad de Datos
      UE-EE. UU.</li>
      <li><strong>Tipografías.</strong> Las letras de la web se cargan desde Google Fonts
      (Google), así que tu navegador le pide esos archivos a Google y Google recibe tu
      dirección IP. Google Fonts no instala cookies.</li>
      <li><strong>Estado del servidor.</strong> En la página de ChorizoSMP, tu navegador
      consulta si el servidor está abierto a api.mcsrvstat.us, que recibe tu IP para
      responder. Solo en esa página.</li>
      <li><strong>Plantillas de servidor.</strong> Al darle a descargar una plantilla, tu
      navegador baja los plugins de su web oficial (api.modrinth.com, cdn.modrinth.com y
      download.geysermc.org), que reciben tu IP para enviártelos. Solo en ese momento.</li>
    </ul>

    <h2>Lo que se guarda en tu navegador</h2>
    <p>Algunas preferencias se guardan en tu propio navegador y no salen de él: el
    tema noche o claro que eliges, y si ya has cerrado un aviso. Está explicado en la
    <a href="/cookies/">política de cookies</a>.</p>

    <h2>Enlaces a hostings</h2>
    <p>Cuando pinchas en un hosting sales de esta web y se aplica su política de
    privacidad. %(afil)s</p>

    <h2>Tus derechos</h2>
    <p>Puedes pedir acceso, rectificación, supresión, oposición, limitación y
    portabilidad escribiendo a %(e)s. Si crees que algo no se hace bien, puedes
    reclamar ante la Agencia Española de Protección de Datos (aepd.es).</p>
  </article>""" % dict(t=t, e=e, afil=(
            "Algunos enlaces llevan una etiqueta que dice desde qué parte de la web "
            "vienes, sin ningún dato personal." if partner.activo() else ""))
        return pagina("es", "/privacidad/", "Política de privacidad · MontaTuServer",
                      "Qué datos trata MontaTuServer: ninguno que escribas, sin cuentas, sin analítica y sin cookies.",
                      cuerpo)

    cuerpo = """  <article class="wrap articulo legal">
    <h1>Privacy policy</h1>
    <p class="art-meta">Last updated: September 2026</p>

    <p class="legal-resumen"><strong>In short:</strong> this site doesn't ask you for
    any data, has no accounts or forms, uses no analytics and sets no cookies.</p>

    <h2>Controller</h2>
    <p>%(t)s. Contact: %(e)s.</p>

    <h2>What data is processed</h2>
    <ul>
      <li><strong>Nothing you type.</strong> There's no sign-up, no forms and no
      comments.</li>
      <li><strong>Hosting technical data.</strong> The site is hosted on Netlify
      (Netlify, Inc., United States), which like any server logs technical data such
      as your IP address and browser to serve the page and protect it from attacks.
      Netlify is certified under the EU-US Data Privacy Framework.</li>
      <li><strong>Fonts.</strong> The site's fonts load from Google Fonts, so your
      browser requests those files from Google and Google receives your IP address.
      Google Fonts sets no cookies.</li>
      <li><strong>Server status.</strong> On the ChorizoSMP page, your browser asks
      api.mcsrvstat.us whether the server is online, which receives your IP to answer.
      Only on that page.</li>
      <li><strong>Server templates.</strong> When you download a template, your browser
      fetches the plugins from their official site (api.modrinth.com, cdn.modrinth.com and
      download.geysermc.org), which receive your IP to send them. Only at that moment.</li>
    </ul>

    <h2>What's stored in your browser</h2>
    <p>A couple of preferences are stored in your own browser and never leave it: the
    night or light theme you pick, and whether you've closed a notice. See the
    <a href="/en/cookies/">cookie policy</a>.</p>

    <h2>Links to hosts</h2>
    <p>When you click through to a host you leave this site and their privacy policy
    applies. %(afil)s</p>

    <h2>Your rights</h2>
    <p>You can request access, rectification, erasure, objection, restriction and
    portability by writing to %(e)s. If you think something isn't right, you can
    complain to the Spanish Data Protection Agency (aepd.es).</p>
  </article>""" % dict(t=t, e=e, afil=(
        "Some links carry a tag saying which part of the site you came from, with no "
        "personal data." if partner.activo() else ""))
    return pagina("en", "/en/privacy/", "Privacy policy · MontaTuServer",
                  "What data MontaTuServer processes: nothing you type, no accounts, no analytics and no cookies.",
                  cuerpo)


# =============================================================================
# COOKIES
# =============================================================================
def cookies(lang):
    if lang == "es":
        cuerpo = """  <article class="wrap articulo legal">
    <h1>Política de cookies</h1>
    <p class="art-meta">Última actualización: septiembre de 2026</p>

    <p class="legal-resumen"><strong>Esta web no instala cookies.</strong> Ni propias ni
    de terceros, ni de análisis ni de publicidad. Por eso no te sale ningún aviso para
    aceptarlas.</p>

    <h2>Lo que sí se guarda, y por qué no hace falta pedirte permiso</h2>
    <p>Para que la web se acuerde de lo que has elegido, se guardan un par de cosas en
    el almacenamiento de tu propio navegador. No salen de tu equipo, no sirven para
    seguirte y no se comparten con nadie:</p>
    <div class="table-wrap"><table class="tabla-maestra">
      <thead><tr><th>Nombre</th><th>Para qué</th><th>Cuánto dura</th></tr></thead>
      <tbody>
        <tr><td>tema</td><td>Recordar si prefieres el modo noche o el claro</td><td>Hasta que lo borres</td></tr>
        <tr><td>promo-vista-…</td><td>No volver a enseñarte un aviso que ya has cerrado</td><td>Hasta que lo borres</td></tr>
        <tr><td>cid</td><td>Saber desde qué red llegaste (por ejemplo, un vídeo de YouTube)</td><td>Se borra al cerrar la pestaña</td></tr>
      </tbody>
    </table></div>
    <p>Son elementos técnicos y de preferencias que tú mismo pides al usar la web, así
    que la ley (artículo 22.2 de la LSSI) no obliga a pedir consentimiento para ellos.</p>

    <h2>Cómo borrarlo</h2>
    <p>Desde la configuración de tu navegador, en el apartado de datos de sitios o
    almacenamiento. Si lo borras, la web vuelve a salir en modo noche.</p>

    <h2>Si esto cambia</h2>
    <p>Si algún día se añade algo que sí necesite tu permiso, esta página lo dirá y se
    te preguntará antes.</p>
  </article>"""
        return pagina("es", "/cookies/", "Política de cookies · MontaTuServer",
                      "MontaTuServer no instala cookies. Solo guarda en tu navegador el tema que eliges.",
                      cuerpo)

    cuerpo = """  <article class="wrap articulo legal">
    <h1>Cookie policy</h1>
    <p class="art-meta">Last updated: September 2026</p>

    <p class="legal-resumen"><strong>This site sets no cookies.</strong> Not its own, not
    third-party, not analytics, not advertising. That's why you don't get a banner
    asking you to accept them.</p>

    <h2>What is stored, and why it doesn't need your consent</h2>
    <p>So the site remembers what you picked, a couple of things are kept in your own
    browser's storage. They never leave your device, can't be used to track you and
    aren't shared with anyone:</p>
    <div class="table-wrap"><table class="tabla-maestra">
      <thead><tr><th>Name</th><th>What for</th><th>How long</th></tr></thead>
      <tbody>
        <tr><td>tema</td><td>Remember whether you prefer night or light mode</td><td>Until you delete it</td></tr>
        <tr><td>promo-vista-…</td><td>Not showing you again a notice you've already closed</td><td>Until you delete it</td></tr>
        <tr><td>cid</td><td>Know which network you came from (a YouTube video, for example)</td><td>Deleted when you close the tab</td></tr>
      </tbody>
    </table></div>
    <p>These are technical and preference items you request yourself when using the
    site, so the law (article 22.2 of Spanish LSSI) doesn't require consent for them.</p>

    <h2>How to delete it</h2>
    <p>From your browser settings, under site data or storage. If you delete it, the
    site goes back to night mode.</p>

    <h2>If this changes</h2>
    <p>If something that does need your permission is ever added, this page will say
    so and you'll be asked first.</p>
  </article>"""
    return pagina("en", "/en/cookies/", "Cookie policy · MontaTuServer",
                  "MontaTuServer sets no cookies. It only stores the theme you pick in your browser.",
                  cuerpo)


# =============================================================================
# MI SERVER: CHORIZOSMP
# =============================================================================
ESTADO_JS = """<script>
/* ¿Está abierto ahora? Se pregunta a api.mcsrvstat.us desde el navegador.
   Si no responde, se dice que no se ha podido comprobar: nunca se inventa. */
(function(){
  const caja = document.getElementById("estado-server");
  if (!caja) return;
  const T = caja.dataset;
  const api = "https://api.mcsrvstat.us/";
  // Primero Java; si no contesta, Bedrock por su puerto (el server es el mismo)
  fetch(api + "3/" + T.ip)
    .then(r => r.json())
    .then(d => d.online ? d : fetch(api + "bedrock/3/" + T.ip + ":" + T.pb).then(r => r.json()))
    .then(d => {
      if (d.online){
        caja.className = "estado on";
        caja.textContent = T.abierto.replace("{n}", (d.players && d.players.online) || 0);
      } else {
        caja.className = "estado off";
        caja.textContent = T.cerrado;
      }
    })
    .catch(() => { caja.className = "estado"; caja.textContent = T.nose; });
})();
</script>"""


def mi_server(lang):
    S = sitio.SERVER
    ip, pb, ver = S["ip"], S["puerto_bedrock"], S["version"]
    if lang == "es":
        cuerpo = """  <div class="wrap server">
    <div class="server-hero">
      <img class="server-logo" src="/chorizosmp.webp" width="128" height="128" alt="Logo de ChorizoSMP">
      <div>
        <span class="sec-eyebrow">Mi servidor de Minecraft</span>
        <h1>¿Quieres jugar en <em>ChorizoSMP</em>?</h1>
        <p class="sub">Semi-anarquía en español. Sin protección de bases: se roba, se
        raidea y se pelea, pero con economía de verdad para hacerte rico. Java y
        Bedrock en el mismo mundo.</p>
      </div>
    </div>

    <div class="ip-card">
      <div class="ip-fila">
        <div><span class="ip-lbl">Java (PC)</span><code class="ip-val">%(ip)s</code></div>
        <button class="cta" type="button" data-copiar="%(ip)s" data-ok="¡Copiada!">Copiar IP</button>
      </div>
      <div class="ip-fila">
        <div><span class="ip-lbl">Bedrock (móvil, consola, Windows)</span>
          <code class="ip-val">%(ip)s</code> <span class="ip-puerto">puerto %(pb)s</span></div>
        <button class="cta-ghost" type="button" data-copiar="%(ip)s" data-ok="¡Copiada!">Copiar</button>
      </div>
      <p class="ip-pie">Versión %(ver)s · <span id="estado-server" class="estado"
        data-ip="%(ip)s" data-pb="%(pb)s" data-abierto="Abierto ahora · {n} jugando"
        data-cerrado="Ahora mismo está cerrado" data-nose="No he podido comprobar si está abierto">Comprobando si está abierto…</span></p>
    </div>

    <h2>Cómo es el server</h2>
    <div class="cards server-cards">
      <div class="card"><h3>🌶 Semi-anarquía</h3><p>No hay claims ni protección de
        bases. Todo vale: robar, raidear y destruir. Eso sí, con reglas de economía y
        un anticheat, que esto no es 2b2t.</p></div>
      <div class="card"><h3>💰 Economía</h3><p>Vende lo que farmees con
        <code>/vender</code>, compra spawners y más en <code>/tienda</code> y puja en la
        casa de subastas con <code>/ah</code>.</p></div>
      <div class="card"><h3>💎 Chorizium (CHR)</h3><p>La segunda moneda. Se gana
        estando en las zonas AFK; en la zona PvP ganas cinco veces más, pero si te
        matan te lo roban. Se gasta en <code>/tiendachr</code>.</p></div>
      <div class="card"><h3>⚔ PvP sin escapatoria</h3><p>En combate no puedes huir
        con comandos, y si te desconectas en mitad de una pelea, mueres.</p></div>
      <div class="card"><h3>🥩 Empiezas de cero</h3><p>Apareces con 8 filetes y 4
        panes. Sin dinero, sin herramientas, sin armadura. Sal del spawn con
        <code>/rtp</code> y búscate la vida.</p></div>
      <div class="card"><h3>🎮 Crossplay y voz</h3><p>Entran los de PC, móvil y
        consola al mismo mundo, y tiene chat de voz de proximidad con el mod Simple
        Voice Chat.</p></div>
    </div>

    <h2>Cómo entrar</h2>
    <div class="pasos-server">
      <div class="card"><h3>Desde PC (Java)</h3><ol>
        <li>Abre Minecraft Java en la versión %(ver)s.</li>
        <li>Multijugador → Añadir servidor.</li>
        <li>En «Dirección del servidor» pon <code>%(ip)s</code> y dale a Listo.</li></ol></div>
      <div class="card"><h3>Desde móvil o Windows (Bedrock)</h3><ol>
        <li>Jugar → Servidores → Añadir servidor.</li>
        <li>Dirección: <code>%(ip)s</code></li>
        <li>Puerto: <code>%(pb)s</code></li></ol></div>
      <div class="card"><h3>Desde consola</h3><p>PlayStation, Xbox y Switch no dejan
        añadir servidores externos a mano. Lo más fácil es entrar desde el móvil o el
        PC de un amigo, o usar una app de las que te dejan unirte a servidores Bedrock
        desde la consola.</p></div>
    </div>

    <div class="art-cta">
      <h3>Lo vas a ver en directo</h3>
      <p>Buena parte de lo que pasa en ChorizoSMP sale en mis directos y vídeos. Si
      quieres saber cuándo hay evento, pásate por el canal.</p>
      <a class="cta" href="%(yt)s" rel="me noopener">Ir al canal de Doublelag</a>
    </div>
  </div>""" % dict(ip=ip, pb=pb, ver=ver, yt=sitio.YOUTUBE)
        return pagina("es", "/mi-server/",
                      "ChorizoSMP: juega en el servidor de Minecraft de Doublelag",
                      "Semi-anarquía en español con economía, Chorizium y crossplay Java y Bedrock. IP, cómo entrar y cómo es el server.",
                      cuerpo, ESTADO_JS, og_type="website")

    cuerpo = """  <div class="wrap server">
    <div class="server-hero">
      <img class="server-logo" src="/chorizosmp.webp" width="128" height="128" alt="ChorizoSMP logo">
      <div>
        <span class="sec-eyebrow">My Minecraft server</span>
        <h1>Want to play on <em>ChorizoSMP</em>?</h1>
        <p class="sub">A Spanish-speaking semi-anarchy server. No base protection:
        stealing, raiding and fighting are allowed, but there's a real economy to get
        rich. Java and Bedrock in the same world.</p>
      </div>
    </div>

    <div class="ip-card">
      <div class="ip-fila">
        <div><span class="ip-lbl">Java (PC)</span><code class="ip-val">%(ip)s</code></div>
        <button class="cta" type="button" data-copiar="%(ip)s" data-ok="Copied!">Copy IP</button>
      </div>
      <div class="ip-fila">
        <div><span class="ip-lbl">Bedrock (mobile, console, Windows)</span>
          <code class="ip-val">%(ip)s</code> <span class="ip-puerto">port %(pb)s</span></div>
        <button class="cta-ghost" type="button" data-copiar="%(ip)s" data-ok="Copied!">Copy</button>
      </div>
      <p class="ip-pie">Version %(ver)s · <span id="estado-server" class="estado"
        data-ip="%(ip)s" data-pb="%(pb)s" data-abierto="Online now · {n} playing"
        data-cerrado="It's closed right now" data-nose="Couldn't check whether it's online">Checking whether it's online…</span></p>
    </div>

    <h2>What the server is like</h2>
    <div class="cards server-cards">
      <div class="card"><h3>🌶 Semi-anarchy</h3><p>No claims and no base protection.
        Anything goes: steal, raid and destroy. There are still economy rules and an
        anticheat, though — this isn't 2b2t.</p></div>
      <div class="card"><h3>💰 Economy</h3><p>Sell what you farm with
        <code>/vender</code>, buy spawners and more in <code>/tienda</code>, and bid in
        the auction house with <code>/ah</code>.</p></div>
      <div class="card"><h3>💎 Chorizium (CHR)</h3><p>The second currency. You earn it
        in the AFK zones; in the PvP zone you earn five times more, but if you get
        killed, it's stolen. Spend it in <code>/tiendachr</code>.</p></div>
      <div class="card"><h3>⚔ No escaping combat</h3><p>You can't flee a fight with
        commands, and if you disconnect mid-fight, you die.</p></div>
      <div class="card"><h3>🥩 You start from zero</h3><p>You spawn with 8 steaks and
        4 loaves of bread. No money, no tools, no armour. Leave spawn with
        <code>/rtp</code> and make your own way.</p></div>
      <div class="card"><h3>🎮 Crossplay and voice</h3><p>PC, mobile and console
        players share the same world, and there's proximity voice chat with the Simple
        Voice Chat mod.</p></div>
    </div>

    <h2>How to join</h2>
    <div class="pasos-server">
      <div class="card"><h3>On PC (Java)</h3><ol>
        <li>Open Minecraft Java on version %(ver)s.</li>
        <li>Multiplayer → Add Server.</li>
        <li>Type <code>%(ip)s</code> as the server address and hit Done.</li></ol></div>
      <div class="card"><h3>On mobile or Windows (Bedrock)</h3><ol>
        <li>Play → Servers → Add Server.</li>
        <li>Address: <code>%(ip)s</code></li>
        <li>Port: <code>%(pb)s</code></li></ol></div>
      <div class="card"><h3>On console</h3><p>PlayStation, Xbox and Switch don't let
        you add external servers by hand. The easiest way is to join from a friend's
        phone or PC, or use one of the apps that let you join Bedrock servers from a
        console.</p></div>
    </div>

    <div class="art-cta">
      <h3>You'll see it live</h3>
      <p>A lot of what happens on ChorizoSMP ends up in my streams and videos. If you
      want to know when there's an event, check the channel.</p>
      <a class="cta" href="%(yt)s" rel="me noopener">Go to the Doublelag channel</a>
    </div>
  </div>""" % dict(ip=ip, pb=pb, ver=ver, yt=sitio.YOUTUBE)
    return pagina("en", "/en/my-server/",
                  "ChorizoSMP: play on Doublelag's Minecraft server",
                  "A Spanish-speaking semi-anarchy server with an economy, Chorizium and Java + Bedrock crossplay. IP, how to join and what it's like.",
                  cuerpo, ESTADO_JS, og_type="website")


# =============================================================================
# PÁGINA 404 EN INGLÉS  (/en/404.html)
# =============================================================================
# La española vive en 404.html, escrita a mano. Esta se genera para que a quien
# llega de la versión inglesa no le salga un error en español.
NO_ENCONTRADA_EN = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Page not found · MontaTuServer</title>
<meta name="robots" content="noindex">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
%(fuentes)s
<link rel="stylesheet" href="/styles.css">
</head>
<body>

<header class="site-head"></header>

<main>
  <div class="wrap">
    <div class="hero">
      <span class="eyebrow">Error 404</span>
      <h1>There's <em>nothing</em> here</h1>
      <p class="sub">
        This page doesn't exist, or I moved it. While you're here, let me tell you
        how much RAM your server needs, which is what you came for.
      </p>
    </div>
  </div>

  <section style="padding-top:0">
    <div class="wrap">
      <h2>What there is</h2>
      <p class="sec-sub">The Minecraft RAM calculator, the hosts compared and their deals.</p>
      <p style="margin-top:26px">
        <a class="cta" href="/en/">Go to the calculator</a>
        <a class="cta-ghost" href="/en/minecraft/best-hosting/">See the comparison</a>
      </p>
    </div>
  </section>
</main>

<footer></footer>

<script src="/buscador_ui.js" defer></script>

</body>
</html>
""" % dict(fuentes=FUENTES)


TODAS = [
    ("/aviso-legal/", lambda: aviso_legal("es")), ("/en/legal-notice/", lambda: aviso_legal("en")),
    ("/privacidad/", lambda: privacidad("es")), ("/en/privacy/", lambda: privacidad("en")),
    ("/cookies/", lambda: cookies("es")), ("/en/cookies/", lambda: cookies("en")),
    ("/mi-server/", lambda: mi_server("es")), ("/en/my-server/", lambda: mi_server("en")),
]
