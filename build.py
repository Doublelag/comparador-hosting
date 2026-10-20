# -*- coding: utf-8 -*-
"""
Genera todas las páginas estáticas de la web a partir de hosts.js y de los
módulos de contenido (guías, comparativa, fichas, versus, ofertas).

Desde el 17-sep-2026 la web es solo de Minecraft. Antes esto sacaba además una
copia de index.html por cada uno de 11 juegos (/valheim/, /rust/…); ahora la
portada ES la calculadora de Minecraft y esas URLs redirigen a ella
(ver _redirects).

Uso:  python build.py
Vuelve a ejecutarlo cada vez que toques index.html, hosts.js o los textos.
"""

import io, os, re, json, datetime, hashlib
import guias
import comparativas
import hostings
import ofertas
import partner
import duelos
import historico
import marco
import paginas
import plantillas
import modpacks
import historial
import hostings_en
import duelos_en
import ofertas_en
import comparativa_en
import guia_en
import videos
import seo

DOMINIO = "https://montatuserver.com"
RAIZ = os.path.dirname(os.path.abspath(__file__))
HOY = datetime.date.today().isoformat()

def rellenar_partner():
    """Rellena en la portada (index.html y su versión inglesa index.en.html) los
    textos que dependen del partner y la IP del server.

    Las portadas son ficheros escritos a mano, así que no pueden llevar
    %(variables)s. En su lugar llevan marcadores <!--partner:x-->…<!--/partner:x-->
    y aquí se reescribe lo de dentro. Es idempotente. La inglesa se copia
    después a /en/index.html.
    """
    import sitio
    cfg = partner.config()
    promo = ('<script src="/promo_ui.js" defer></script>'
             if partner.activo() and cfg.get("promo") else "")
    for fichero, textos in (
        ("index.html", {"quegano": partner.que_gano_yo(), "boton": partner.aviso_boton(),
                        "quien": partner.linea_bienvenida(), "promoscript": promo}),
        ("index.en.html", {"quegano": partner.que_gano_yo_en(), "boton": partner.aviso_boton_en(),
                           "quien": partner.linea_bienvenida_en(), "promoscript": promo}),
    ):
        ruta = os.path.join(RAIZ, fichero)
        html = io.open(ruta, encoding="utf-8").read()
        html = re.sub(r"(<!--server:ip-->).*?(<!--/server:ip-->)",
                      lambda m: m.group(1) + sitio.SERVER["ip"] + m.group(2), html, flags=re.S)
        for clave, texto in textos.items():
            patron = re.compile(r"(<!--partner:%s-->).*?(<!--/partner:%s-->)" % (clave, clave), re.S)
            assert patron.search(html), "falta el marcador partner:%s en %s" % (clave, fichero)
            html = patron.sub(lambda m, t=texto: m.group(1) + t + m.group(2), html)
        io.open(ruta, "w", encoding="utf-8").write(html)
    # la portada en inglés vive en /en/
    os.makedirs(os.path.join(RAIZ, "en"), exist_ok=True)
    io.open(os.path.join(RAIZ, "en", "index.html"), "w", encoding="utf-8").write(
        io.open(os.path.join(RAIZ, "index.en.html"), encoding="utf-8").read())
    print("  partner: %s" % (partner.nombre() or "ninguno (comparador sin afiliación)"))


ESTATICOS = ["styles.css", "app.js", "hosts.js", "buscador_ui.js", "tabla_ui.js",
             "filtros_ui.js", "promo_ui.js", "indice.js", "plantilla_ui.js",
             "zip_ui.js", "modpack_ui.js", "estado_ui.js"]


def versionar():
    """Pone ?v=<huella> a los css y js de todas las páginas.

    Sirve para poder cachearlos un año entero en el navegador (lo dice
    `_headers`): mientras el archivo no cambie, la visita repetida no se
    descarga nada, y en cuanto cambie, cambia la huella y se pide solo. Sin
    esto hay que elegir entre caché corta (se pagan peticiones de más) o caché
    larga (la gente ve precios viejos), y ninguna de las dos vale.
    """
    huellas = {}
    for nombre in ESTATICOS:
        ruta = os.path.join(RAIZ, nombre)
        if os.path.exists(ruta):
            huellas[nombre] = hashlib.sha1(
                io.open(ruta, "rb").read()).hexdigest()[:8]

    tocadas = 0
    for base, dirs, ficheros in os.walk(RAIZ):
        dirs[:] = [d for d in dirs
                   if d not in (".claude", "dist", "__pycache__") and not d.startswith(".")]
        for fichero in ficheros:
            if fichero not in ("index.html", "404.html"):
                continue
            ruta = os.path.join(base, fichero)
            html = io.open(ruta, encoding="utf-8").read()
            original = html
            for nombre, huella in huellas.items():
                html = re.sub(r'(["\'])/%s(\?v=[0-9a-f]+)?\1' % re.escape(nombre),
                              lambda m: '%s/%s?v=%s%s' % (m.group(1), nombre, huella, m.group(1)),
                              html)
            # el buscador pide el índice él solo: se lo pasamos ya versionado
            # (se quita antes el de la pasada anterior, o se van acumulando)
            html = re.sub(r' data-indice="[^"]*"', "", html)
            if "indice.js" in huellas:
                html = re.sub(r'<script src="/buscador_ui\.js([^"]*)"',
                              '<script src="/buscador_ui.js\\1" data-indice="/indice.js?v=%s"'
                              % huellas["indice.js"], html)
            if html != original:
                io.open(ruta, "w", encoding="utf-8").write(html)
                tocadas += 1
    print("  version puesta a los estaticos en %d paginas" % tocadas)


def contar_en_portadas():
    """Pone el número de hostings en las portadas (meta y cifra de la barra).

    Van escritos en el HTML para Google y para quien no tenga JavaScript; así
    no se quedan viejos cuando se añade un hosting."""
    d = comparativas.datos()
    n = len({h.get("ficha") or h["id"] for h in d["hosts"]})
    for nombre in ("index.html", "index.en.html"):
        ruta = os.path.join(RAIZ, nombre)
        s = io.open(ruta, encoding="utf-8").read()
        s = re.sub(r"\b\d+ (hostings|hosts)\b", lambda m: "%d %s" % (n, m.group(1)), s)
        s = re.sub(r"(data-n-hosts>)\d+<", lambda m: "%s%d<" % (m.group(1), n), s)
        io.open(ruta, "w", encoding="utf-8", newline="\n").write(s)
    return n


def podar_scripts():
    """Quita de cada página los <script> que ahí no hacen nada.

    tabla_ui.js solo ordena tablas con class="ordenable" y filtros_ui.js solo
    trabaja si hay filtros. Cargarlos donde no hay ni una cosa ni la otra es
    pedirle al visitante bytes que no va a usar — y a Netlify, peticiones que
    se pagan. Se hace sobre lo ya generado, así que ninguna plantilla tiene que
    acordarse de nada.
    """
    def sin(script, html):
        # el ?v=… lo pone versionar() después, pero puede quedar de la pasada anterior
        return re.sub(r'[ \t]*<script src="/%s(\?v=[0-9a-f]+)?"[^>]*></script>\n'
                      % re.escape(script), "", html)

    quitadas = 0
    for base, dirs, ficheros in os.walk(RAIZ):
        dirs[:] = [d for d in dirs
                   if d not in (".claude", "dist", "__pycache__") and not d.startswith(".")]
        for pagina in ("index.html", "404.html"):
            if pagina not in ficheros:
                continue
            ruta = os.path.join(base, pagina)
            html = io.open(ruta, encoding="utf-8").read()
            original = html
            if "ordenable" not in html:
                html = sin("tabla_ui.js", html)
            if "data-filtrable" not in html and 'id="filtros-ofertas"' not in html:
                html = sin("filtros_ui.js", html)
            if html != original:
                io.open(ruta, "w", encoding="utf-8").write(html)
                quitadas += 1
    print("  scripts podados en %d paginas" % quitadas)


def enmarcar(comprobado):
    """Pone a todas las páginas la misma cabecera, el mismo pie y el tema.

    Se hace al final, sobre lo ya generado, para que ninguna plantilla tenga
    que llevar su propia copia: antes había siete y cada una decía una cosa.
    """
    def existe(url):
        ruta = os.path.join(RAIZ, *[p for p in url.split("/") if p], "index.html")
        return os.path.exists(ruta)

    tocadas = 0
    for base, dirs, ficheros in os.walk(RAIZ):
        dirs[:] = [d for d in dirs
                   if d not in (".claude", "dist", "__pycache__") and not d.startswith(".")]
        for pagina in ("index.html", "404.html"):
            if pagina not in ficheros:
                continue
            rel = os.path.relpath(base, RAIZ).replace("\\", "/")
            url = "/" if rel == "." else "/%s/" % rel
            ruta = os.path.join(base, pagina)
            html = io.open(ruta, encoding="utf-8").read()
            nuevo = marco.aplicar(html, url, comprobado, existe, con_og=(pagina == "index.html"))
            if nuevo != html:
                io.open(ruta, "w", encoding="utf-8").write(nuevo)
                tocadas += 1
    print("  marco comun puesto en %d paginas" % tocadas)


def generar_indice():
    """Índice del buscador, leído de las páginas que existen de verdad.

    Se hace al final, cuando ya está todo generado: así una página nueva
    aparece sola en el buscador sin que haya que apuntarla en ningún sitio.
    """
    entradas = []
    for base, dirs, ficheros in os.walk(RAIZ):
        dirs[:] = [d for d in dirs
                   if d not in (".claude", "dist", "__pycache__") and not d.startswith(".")]
        if "index.html" not in ficheros:
            continue
        rel = os.path.relpath(base, RAIZ).replace("\\", "/")
        url = "/" if rel == "." else "/%s/" % rel
        html = io.open(os.path.join(base, "index.html"), encoding="utf-8").read()
        m = re.search(r"<title>(.*?)</title>", html, re.S)
        if not m:
            continue
        titulo = m.group(1).strip()

        # categoría, para que el resultado diga de qué tipo es
        if url == "/":
            cat = "calculadora"
        elif "/mejor-hosting" in url:
            cat = "comparativa"
        elif "como-montar" in url:
            cat = "guía"
        elif url.startswith("/hosting/"):
            cat = "hosting"
        else:
            cat = "página"

        # palabras clave: la descripción ayuda a encontrar por sinónimos
        d = re.search(r'<meta name="description" content="(.*?)"', html, re.S)
        claves = (d.group(1)[:160] if d else "") + " " + rel.replace("/", " ").replace("-", " ")

        entradas.append({"t": titulo, "u": url, "c": cat, "k": claves})

    entradas.sort(key=lambda e: (e["c"] != "calculadora", e["t"]))
    cabecera = "/* GENERADO POR build.py - no lo edites a mano, se sobreescribe. */\n"
    cuerpo = "window.INDICE = " + json.dumps(entradas, ensure_ascii=False, indent=1) + ";\n"
    io.open(os.path.join(RAIZ, "indice.js"), "w", encoding="utf-8").write(cabecera + cuerpo)
    print("\n  indice.js con %d paginas" % len(entradas))


def main():
    print("  portadas  %d hostings" % contar_en_portadas())
    videos.rellenar(RAIZ)
    rellenar_partner()
    cambiados = historico.guardar(hostings.datos())
    if cambiados:
        print("  historico: %d hostings han cambiado de precio" % cambiados)
    urls = ["%s/" % DOMINIO, "%s/en/" % DOMINIO]

    # ---- Guías paso a paso -------------------------------------------------
    for g in guias.GUIAS:
        carpeta = os.path.join(RAIZ, g["juego"], g["url"])
        os.makedirs(carpeta, exist_ok=True)
        io.open(os.path.join(carpeta, "index.html"), "w", encoding="utf-8").write(
            guias.html(g))
        urls.append("%s/%s/%s/" % (DOMINIO, g["juego"], g["url"]))
        print("  guía      /%s/%s/" % (g["juego"], g["url"]))

    # ---- Comparativas ------------------------------------------------------
    for c in comparativas.COMPARATIVAS:
        carpeta = os.path.join(RAIZ, comparativas.carpeta(c), c["url"])
        os.makedirs(carpeta, exist_ok=True)
        io.open(os.path.join(carpeta, "index.html"), "w", encoding="utf-8").write(
            comparativas.html(c))
        urls.append("%s/%s/%s/" % (DOMINIO, comparativas.carpeta(c), c["url"]))
        print("  compar.   /%s/%s/" % (comparativas.carpeta(c), c["url"]))

    # ---- Fichas de hosting -------------------------------------------------
    dh = hostings.datos()
    carpeta = os.path.join(RAIZ, "hosting")
    os.makedirs(carpeta, exist_ok=True)
    io.open(os.path.join(carpeta, "index.html"), "w", encoding="utf-8").write(
        hostings.indice(dh))
    urls.append("%s/hosting/" % DOMINIO)
    print("  hosting   /hosting/")
    for hid, f in hostings.FICHAS.items():
        sub = os.path.join(carpeta, f["url"])
        os.makedirs(sub, exist_ok=True)
        io.open(os.path.join(sub, "index.html"), "w", encoding="utf-8").write(
            hostings.html(hid, f, dh))
        urls.append("%s/hosting/%s/" % (DOMINIO, f["url"]))
        print("  hosting   /hosting/%s/" % f["url"])

    # ---- Fichas en inglés --------------------------------------------------
    carpeta = os.path.join(RAIZ, "en", "hosting")
    os.makedirs(carpeta, exist_ok=True)
    io.open(os.path.join(carpeta, "index.html"), "w", encoding="utf-8").write(hostings_en.indice(dh))
    urls.append("%s/en/hosting/" % DOMINIO)
    for hid, f in hostings.FICHAS.items():
        sub = os.path.join(carpeta, f["url"])
        os.makedirs(sub, exist_ok=True)
        io.open(os.path.join(sub, "index.html"), "w", encoding="utf-8").write(hostings_en.html(hid, dh))
        urls.append("%s/en/hosting/%s/" % (DOMINIO, f["url"]))
    print("  hosting   /en/hosting/ + %d fichas" % len(hostings.FICHAS))

    # ---- Ofertas -----------------------------------------------------------
    carpeta = os.path.join(RAIZ, "ofertas")
    os.makedirs(carpeta, exist_ok=True)
    io.open(os.path.join(carpeta, "index.html"), "w", encoding="utf-8").write(ofertas.html())
    urls.append("%s/ofertas/" % DOMINIO)
    print("  ofertas   /ofertas/")


    # ---- Páginas sueltas: legales y ChorizoSMP (en los dos idiomas) --------
    historiales = [("/precios/", lambda: historial.html("es", dh)),
                   ("/en/price-history/", lambda: historial.html("en", dh))]
    for ruta, hacer in paginas.TODAS + plantillas.TODAS + modpacks.TODAS + historiales + seo.TODAS:
        carpeta = os.path.join(RAIZ, *[p for p in ruta.split("/") if p])
        os.makedirs(carpeta, exist_ok=True)
        io.open(os.path.join(carpeta, "index.html"), "w", encoding="utf-8").write(hacer())
        urls.append("%s%s" % (DOMINIO, ruta))
        print("  pagina    %s" % ruta)

    # ---- 404 en inglés ------------------------------------------------------
    carpeta = os.path.join(RAIZ, "en")
    os.makedirs(carpeta, exist_ok=True)
    io.open(os.path.join(carpeta, "404.html"), "w", encoding="utf-8").write(
        paginas.NO_ENCONTRADA_EN)
    print("  pagina    /en/404.html")

    # ---- Versus -------------------------------------------------------------
    carpeta = os.path.join(RAIZ, "versus")
    os.makedirs(carpeta, exist_ok=True)
    io.open(os.path.join(carpeta, "index.html"), "w", encoding="utf-8").write(duelos.indice(dh))
    urls.append("%s/versus/" % DOMINIO)
    print("  versus    /versus/")
    for x in duelos.DUELOS:
        sub = os.path.join(carpeta, duelos.url_de(x))
        os.makedirs(sub, exist_ok=True)
        io.open(os.path.join(sub, "index.html"), "w", encoding="utf-8").write(duelos.html(x, dh))
        urls.append("%s/versus/%s/" % (DOMINIO, duelos.url_de(x)))
        print("  versus    /versus/%s/" % duelos.url_de(x))

    carpeta = os.path.join(RAIZ, "en", "minecraft", "best-hosting")
    os.makedirs(carpeta, exist_ok=True)
    io.open(os.path.join(carpeta, "index.html"), "w", encoding="utf-8").write(comparativa_en.html(dh))
    urls.append("%s/en/minecraft/best-hosting/" % DOMINIO)
    print("  compar.   /en/minecraft/best-hosting/")

    for ruta, hacer in (("/en/minecraft/how-to-set-up-a-server/", guia_en.html),
                        ):
        carpeta = os.path.join(RAIZ, *[p for p in ruta.split("/") if p])
        os.makedirs(carpeta, exist_ok=True)
        io.open(os.path.join(carpeta, "index.html"), "w", encoding="utf-8").write(hacer())
        urls.append("%s%s" % (DOMINIO, ruta))
        print("  pagina    %s" % ruta)

    carpeta = os.path.join(RAIZ, "en", "deals")
    os.makedirs(carpeta, exist_ok=True)
    io.open(os.path.join(carpeta, "index.html"), "w", encoding="utf-8").write(ofertas_en.html())
    urls.append("%s/en/deals/" % DOMINIO)
    print("  ofertas   /en/deals/")

    # ---- Versus en inglés ---------------------------------------------------
    carpeta = os.path.join(RAIZ, "en", "versus")
    os.makedirs(carpeta, exist_ok=True)
    io.open(os.path.join(carpeta, "index.html"), "w", encoding="utf-8").write(duelos_en.indice(dh))
    urls.append("%s/en/versus/" % DOMINIO)
    for x in duelos.DUELOS:
        sub = os.path.join(carpeta, duelos.url_de(x))
        os.makedirs(sub, exist_ok=True)
        io.open(os.path.join(sub, "index.html"), "w", encoding="utf-8").write(duelos_en.html(x, dh))
        urls.append("%s/en/versus/%s/" % (DOMINIO, duelos.url_de(x)))
    print("  versus    /en/versus/ + %d" % len(duelos.DUELOS))

    # sitemap con todas las páginas
    filas = "\n".join(
        "  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n"
        "    <changefreq>weekly</changefreq>\n    <priority>%s</priority>\n  </url>"
        % (u, HOY, "1.0" if i == 0 else "0.8") for i, u in enumerate(urls))
    io.open(os.path.join(RAIZ, "sitemap.xml"), "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s\n</urlset>\n' % filas)

    # El índice del buscador va el último: necesita que todas las páginas existan
    podar_scripts()
    enmarcar(dh["comprobado"])
    generar_indice()
    versionar()          # el último: necesita el indice.js ya escrito

    print("\nsitemap con %d URLs." % len(urls))


if __name__ == "__main__":
    main()
