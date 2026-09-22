# -*- coding: utf-8 -*-
"""
El marco común de todas las páginas: cabecera, pie y lo que va en el <head>
para el tema y los idiomas.

Antes cada generador (portada, fichas, duelos, ofertas…) escribía su propia
cabecera y su propio pie, siete copias que se desincronizaban: una tenía el
enlace a la calculadora, otra no, el pie de una decía una cosa y el de otra
otra. Ahora build.py pasa por todas las páginas ya generadas y les pone el
mismo marco, sacado de aquí. Un solo pie para toda la web.

También lleva el mapa de URLs entre español e inglés, que es lo que usa el
selector de idioma para saltar a la misma página en el otro idioma.
"""

import datetime, re

import partner
import sitio

DOMINIO = "https://montatuserver.com"

# ---------------------------------------------------------------------------
# URLs español ↔ inglés. Los prefijos se prueban de más largo a más corto:
# /hosting/godlike/ en inglés es /en/hosting/godlike/.
# ---------------------------------------------------------------------------
PREFIJOS = [
    ("/minecraft/como-montar-un-servidor/", "/en/minecraft/how-to-set-up-a-server/"),
    ("/minecraft/mejor-hosting/", "/en/minecraft/best-hosting/"),
    ("/aviso-legal/", "/en/legal-notice/"),
    ("/privacidad/", "/en/privacy/"),
    ("/mi-server/", "/en/my-server/"),
    ("/plantillas/smp-amigos/", "/en/templates/friends-smp/"),
    ("/plantillas/", "/en/templates/"),
    ("/versus/", "/en/versus/"),
    ("/ofertas/", "/en/deals/"),
    ("/cookies/", "/en/cookies/"),
    ("/hosting/", "/en/hosting/"),
    ("/", "/en/"),
]


def a_ingles(url):
    for es, en in PREFIJOS:
        if url.startswith(es):
            return en + url[len(es):]
    return "/en/"


def a_espanol(url):
    for es, en in PREFIJOS:
        if url.startswith(en):
            return es + url[len(en):]
    return "/"


def idioma_de(url):
    return "en" if url == "/en/" or url.startswith("/en/") else "es"


# ---------------------------------------------------------------------------
# Textos del marco
# ---------------------------------------------------------------------------
T = {
    "es": dict(
        menu="Menú", abrir="Abrir el menú", cerrar="Cerrar el menú",
        hostings="Hostings", duelos="Versus", ofertas="Ofertas", plantillas="Plantillas", server="Mi server",
        buscar="Buscar hosting o guía…", buscar_aria="Buscar en la web",
        tema_claro="Cambiar a modo claro", tema_noche="Cambiar a modo noche",
        otro_idioma="English", otro_idioma_corto="EN", otro_idioma_aria="Read this page in English",
        pie_minecraft="Minecraft", pie_comparar="Comparar", pie_doublelag="Doublelag",
        pie_legal="Legal",
        calculadora="Calculadora de RAM", mejor="Mejor hosting de Minecraft",
        guia="Cómo montar un servidor", ping="Ping desde España",
        todos="Todos los hostings", cara="Versus", cupones="Ofertas y cupones",
        canal="Canal de YouTube", chorizo="Jugar en ChorizoSMP",
        privacidad="Privacidad", cookies="Cookies", aviso="Aviso legal",
        contacto="Escríbeme",
        revision="Precios comprobados a mano. Última revisión: %s.",
        firma="MontaTuServer · Hecho por",
    ),
    "en": dict(
        menu="Menu", abrir="Open the menu", cerrar="Close the menu",
        hostings="Hosts", duelos="Versus", ofertas="Deals", plantillas="Templates", server="My server",
        buscar="Search a host or guide…", buscar_aria="Search the site",
        tema_claro="Switch to light mode", tema_noche="Switch to night mode",
        otro_idioma="Español", otro_idioma_corto="ES", otro_idioma_aria="Leer esta página en español",
        pie_minecraft="Minecraft", pie_comparar="Compare", pie_doublelag="Doublelag",
        pie_legal="Legal",
        calculadora="RAM calculator", mejor="Best Minecraft hosting",
        guia="How to set up a server", ping="Ping from Spain",
        todos="All hosts", cara="Versus", cupones="Deals and coupons",
        canal="YouTube channel", chorizo="Play on ChorizoSMP",
        privacidad="Privacy", cookies="Cookies", aviso="Legal notice",
        contacto="Email me",
        revision="Prices checked by hand. Last review: %s.",
        firma="MontaTuServer · Made by",
    ),
}


def _u(url, lang):
    """URL de una página en el idioma pedido (las rutas se escriben en español)."""
    return url if lang == "es" else a_ingles(url)


def seccion_de(url):
    es = a_espanol(url) if idioma_de(url) == "en" else url
    for pref in ("/hosting/", "/versus/", "/ofertas/", "/plantillas/", "/mi-server/"):
        if es.startswith(pref):
            return pref
    return None


# ---------------------------------------------------------------------------
# Cabecera
# ---------------------------------------------------------------------------
ICONO_SOL = ('<svg class="i-sol" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4.2"/>'
             '<path d="M12 2.5v2.2M12 19.3v2.2M4.6 4.6l1.6 1.6M17.8 17.8l1.6 1.6M2.5 12h2.2M19.3 12h2.2'
             'M4.6 19.4l1.6-1.6M17.8 6.2l1.6-1.6"/></svg>')
ICONO_LUNA = ('<svg class="i-luna" viewBox="0 0 24 24" aria-hidden="true">'
              '<path d="M20 14.2A8 8 0 0 1 9.8 4 8.2 8.2 0 1 0 20 14.2z"/></svg>')


def cabecera(url):
    lang = idioma_de(url)
    t = T[lang]
    actual = seccion_de(url)
    otra = a_ingles(url) if lang == "es" else a_espanol(url)

    def enlace(ruta_es, texto):
        cur = ' aria-current="page"' if actual == ruta_es else ""
        return '<a href="%s"%s>%s</a>' % (_u(ruta_es, lang), cur, texto)

    nav = "\n        ".join([
        enlace("/hosting/", t["hostings"]),
        enlace("/versus/", t["duelos"]),
        enlace("/ofertas/", t["ofertas"]),
        enlace("/plantillas/smp-amigos/", t["plantillas"]),
        enlace("/mi-server/", t["server"]),
    ])
    return '''<header class="site-head">
  <div class="wrap">
    <a class="brand" href="%(home)s"><svg class="logo-mark" viewBox="0 0 32 32" aria-hidden="true"><defs><linearGradient id="lm" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6FFFE9"/><stop offset="1" stop-color="#5BC0BE"/></linearGradient></defs><path d="M16 2.5 28.5 9.3v13.4L16 29.5 3.5 22.7V9.3z" fill="url(#lm)"/><path d="M16 2.5 28.5 9.3 16 16.1 3.5 9.3z" fill="#fff" fill-opacity=".38"/><path d="M16 16.1v13.4L3.5 22.7V9.3z" fill="#0B132B" fill-opacity=".22"/><path d="M9.8 12.7 16 16.1l6.2-3.4" fill="none" stroke="#0B132B" stroke-opacity=".35" stroke-width="1.1"/></svg><span>Monta<b>TuServer</b></span></a>
    <div class="menu" id="menu">
      <nav class="nav" aria-label="%(menu)s">
        %(nav)s
      </nav>
      <div class="buscador" id="buscador"><input type="search" placeholder="%(buscar)s" aria-label="%(buscar_aria)s" autocomplete="off"><kbd>/</kbd><div class="bs-panel" role="listbox" hidden></div></div>
    </div>
    <div class="head-tools">
      <a class="lang-btn" href="%(otra)s" hreflang="%(otro_code)s" lang="%(otro_code)s" aria-label="%(otro_aria)s">%(otro_corto)s</a>
      <button class="tema-btn" type="button" data-claro="%(tema_claro)s" data-noche="%(tema_noche)s" aria-label="%(tema_claro)s">%(sol)s%(luna)s</button>
      <button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu" data-abrir="%(abrir)s" data-cerrar="%(cerrar)s" aria-label="%(abrir)s"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>''' % dict(home=_u("/", lang), menu=t["menu"], nav=nav, buscar=t["buscar"],
                    buscar_aria=t["buscar_aria"], otra=otra,
                    otro_code="en" if lang == "es" else "es",
                    otro_aria=t["otro_idioma_aria"], otro_corto=t["otro_idioma_corto"],
                    tema_claro=t["tema_claro"], tema_noche=t["tema_noche"],
                    sol=ICONO_SOL, luna=ICONO_LUNA, abrir=t["abrir"], cerrar=t["cerrar"])


# ---------------------------------------------------------------------------
# Pie: el mismo en toda la web
# ---------------------------------------------------------------------------
def pie(url, comprobado):
    lang = idioma_de(url)
    t = T[lang]
    u = lambda r: _u(r, lang)
    aviso = partner.divulgacion() if lang == "es" else partner.divulgacion_en()
    caja = ('    <div class="disclosure">%s</div>\n' % aviso) if aviso else ""
    return '''<footer class="site-foot">
  <div class="wrap">
%(caja)s    <nav class="pie-links" aria-label="%(legal)s">
      <div>
        <span>%(pie_minecraft)s</span>
        <a href="%(home)s">%(calculadora)s</a>
        <a href="%(mejor_u)s">%(mejor)s</a>
        <a href="%(guia_u)s">%(guia)s</a>
      </div>
      <div>
        <span>%(pie_comparar)s</span>
        <a href="%(hosting_u)s">%(todos)s</a>
        <a href="%(comparar_u)s">%(cara)s</a>
        <a href="%(ofertas_u)s">%(cupones)s</a>
      </div>
      <div>
        <span>%(pie_doublelag)s</span>
        <a href="%(yt)s" rel="me noopener">%(canal)s</a>
        <a href="%(server_u)s">%(chorizo)s</a>
      </div>
      <div>
        <span>%(legal)s</span>
        <a href="%(priv_u)s">%(privacidad)s</a>
        <a href="%(cook_u)s">%(cookies)s</a>
        <a href="%(aviso_u)s">%(aviso)s</a>
        <a href="mailto:%(correo)s">%(contacto)s</a>
      </div>
    </nav>
    <div class="pie-base">
      <p>%(revision)s</p>
      <p>&copy; %(ano)d %(firma)s <a href="%(yt)s" rel="me noopener">Doublelag</a></p>
    </div>
  </div>
</footer>''' % dict(caja=caja, legal=t["pie_legal"], pie_minecraft=t["pie_minecraft"],
                    home=u("/"), calculadora=t["calculadora"],
                    mejor_u=u("/minecraft/mejor-hosting/"), mejor=t["mejor"],
                    guia_u=u("/minecraft/como-montar-un-servidor/"), guia=t["guia"],
                    pie_comparar=t["pie_comparar"], hosting_u=u("/hosting/"), todos=t["todos"],
                    comparar_u=u("/versus/"), cara=t["cara"],
                    ofertas_u=u("/ofertas/"), cupones=t["cupones"],
                    pie_doublelag=t["pie_doublelag"], yt=sitio.YOUTUBE, canal=t["canal"],
                    server_u=u("/mi-server/"), chorizo=t["chorizo"],
                    correo=sitio.EMAIL, contacto=t["contacto"],
                    priv_u=u("/privacidad/"), privacidad=t["privacidad"],
                    cook_u=u("/cookies/"), cookies=t["cookies"],
                    aviso_u=u("/aviso-legal/"), aviso=t["aviso"],
                    revision=t["revision"] % comprobado, ano=datetime.date.today().year,
                    firma=t["firma"])


# ---------------------------------------------------------------------------
# <head>: tema antes de pintar + enlaces entre idiomas
# ---------------------------------------------------------------------------
# Va en línea y lo primero: si esperase a un .js, la página se pintaría en
# noche y un instante después saltaría a claro, que es justo el parpadeo que
# da sensación de web mal hecha.
TEMA_ANTES_DE_PINTAR = ('<script>try{if(localStorage.getItem("tema")==="claro")'
                        'document.documentElement.dataset.theme="claro"}catch(e){}</script>')


def hreflang(url, existe_en):
    """<link rel=alternate> para que Google sepa cuál es la versión en cada idioma."""
    if idioma_de(url) == "es":
        es, en = url, a_ingles(url)
    else:
        es, en = a_espanol(url), url
    if not existe_en(es) or not existe_en(en):
        return ""
    return ('<link rel="alternate" hreflang="es" href="%s%s">\n'
            '<link rel="alternate" hreflang="en" href="%s%s">\n'
            '<link rel="alternate" hreflang="x-default" href="%s%s">'
            % (DOMINIO, es, DOMINIO, en, DOMINIO, es))


def aplicar(html, url, comprobado, existe):
    """Pone el marco común a una página ya generada. Es idempotente."""
    lang = idioma_de(url)
    html = re.sub(r'<html lang="[^"]*"', '<html lang="%s"' % lang, html, count=1)

    html = re.sub(r'<header class="site-head">.*?</header>', lambda m: cabecera(url),
                  html, count=1, flags=re.S)
    if re.search(r'<footer[ >].*?</footer>', html, re.S):
        html = re.sub(r'<footer[ >].*?</footer>', lambda m: pie(url, comprobado),
                      html, count=1, flags=re.S)
    else:
        html = html.replace('</main>', '</main>\n\n' + pie(url, comprobado), 1)

    # tema y hreflang, justo después del viewport (se quitan antes: idempotente)
    html = html.replace(TEMA_ANTES_DE_PINTAR + "\n", "")
    html = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n?', "", html)
    extra = TEMA_ANTES_DE_PINTAR + "\n" + hreflang(url, existe)
    html = re.sub(r'(<meta name="viewport"[^>]*>\n)', lambda m: m.group(1) + extra.rstrip("\n") + "\n",
                  html, count=1)
    return html
