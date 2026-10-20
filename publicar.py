# -*- coding: utf-8 -*-
"""
Deja en dist/ exactamente lo que hay que subir a Cloudflare Pages.

Por qué existe: en la carpeta del proyecto hay cosas que NO deben acabar
publicadas — sobre todo LEEME.md, que lleva tus enlaces de afiliado, tus
márgenes y tu estrategia. Si arrastras la carpeta entera, eso queda colgado
en internet para quien sepa mirar.

Uso:
    python build.py      # genera las paginas
    python make_og.py    # genera las imagenes
    python publicar.py   # deja dist/ listo para arrastrar
"""

import io, json, os, shutil

import minificar

RAIZ = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(RAIZ, "dist")

# Lo que SÍ se publica
ARCHIVOS = ["index.html", "404.html", "styles.css", "hosts.js", "app.js",
            "indice.js", "buscador_ui.js", "tabla_ui.js", "promo_ui.js", "filtros_ui.js", "plantilla_ui.js", "zip_ui.js", "modpack_ui.js",
            "favicon.ico", "apple-touch-icon.png", "chorizosmp.webp",
            "godlike-banner.webp", "hero-cielo.webp",
            "robots.txt", "sitemap.xml", "og-image.jpg", "_redirects", "_headers"]

# Carpetas con páginas (minecraft/ guarda la comparativa y la guía)
CARPETAS = ["hosting", "ofertas", "versus", "minecraft",
            "mi-server", "plantillas", "privacidad", "cookies", "aviso-legal",
            "como-lo-compruebo", "precios", "en", "logos"]

# Lo que NUNCA se publica (aunque esté dentro de una carpeta de juego)
PROHIBIDO = {".py", ".md", ".pyc"}


def limpio(nombre):
    return os.path.splitext(nombre)[1].lower() not in PROHIBIDO


def hosts_para_web(texto):
    """hosts.js sin lo que solo usan los scripts de Python.

    El archivo del proyecto lleva las notas de mantenimiento, la página de la
    que sale cada precio (`fuente`, que usa revisar_precios.py) y los datos de
    ping (que usa ping.py al generar). Nada de eso lo lee el navegador, así que
    se queda fuera de lo publicado: son kilobytes que descarga cada visita para
    nada.
    """
    i = texto.index("window.DATOS =")
    d = json.loads(texto[i + len("window.DATOS ="):].strip().rstrip(";"))
    d = {k: v for k, v in d.items() if not k.startswith("_") and k != "ping"}
    d["hosts"] = [{k: v for k, v in h.items() if k != "fuente"} for h in d["hosts"]]
    return ("window.DATOS = "
            + json.dumps(d, ensure_ascii=False, separators=(",", ":")) + ";\n")


def copiar(origen, destino):
    """Copia al dist, minificando lo que se pueda por el camino.

    El proyecto se queda con sus comentarios (son medio valor del código) y lo
    que se publica va sin ellos. Si algo falla al minificar, se copia el
    original tal cual: publicar es más importante que ahorrar cuatro kilobytes.
    """
    nombre = os.path.basename(origen)
    if nombre.endswith((".css", ".js", ".html")):
        try:
            texto = io.open(origen, encoding="utf-8").read()
            salida = (hosts_para_web(texto) if nombre == "hosts.js"
                      else minificar.para(nombre, texto))
            io.open(destino, "w", encoding="utf-8", newline="\n").write(salida)
            return
        except Exception as e:
            print("  no he podido minificar %s (%s): va entero" % (nombre, e))
    shutil.copy2(origen, destino)


def vaciar(carpeta):
    """Vacía dist/ sin borrar la carpeta en sí.

    Si borras la carpeta entera y tienes esa ventana abierta en el Explorador
    de Windows, Windows la bloquea y el script peta con 'Acceso denegado'.
    Vaciando el contenido no pasa.
    """
    for nombre in os.listdir(carpeta):
        ruta = os.path.join(carpeta, nombre)
        try:
            shutil.rmtree(ruta) if os.path.isdir(ruta) else os.remove(ruta)
        except PermissionError:
            print("  No se pudo borrar %s (¿lo tienes abierto?). Se sobreescribe." % nombre)


def main():
    import sitio
    faltan = sitio.faltan_datos_legales()
    if faltan:
        print("\n  \033[91mOJO: el aviso legal no esta completo. Falta en sitio.py: %s\033[0m\n" % ", ".join(faltan))
    if os.path.isdir(DIST):
        vaciar(DIST)
    else:
        os.makedirs(DIST)

    n = 0
    for f in ARCHIVOS:
        origen = os.path.join(RAIZ, f)
        if not os.path.exists(origen):
            print("  FALTA  %s  ← ¿has ejecutado build.py y make_og.py?" % f)
            continue
        copiar(origen, os.path.join(DIST, f))
        n += 1

    for c in CARPETAS:
        origen = os.path.join(RAIZ, c)
        if not os.path.isdir(origen):
            print("  FALTA la carpeta %s  ← ejecuta build.py" % c)
            continue
        for base, _, ficheros in os.walk(origen):
            rel = os.path.relpath(base, RAIZ)
            if os.path.basename(base) == "__pycache__":
                continue
            destino = os.path.join(DIST, rel)
            os.makedirs(destino, exist_ok=True)
            for f in ficheros:
                if limpio(f):
                    copiar(os.path.join(base, f), os.path.join(destino, f))
                    n += 1

    peso = sum(os.path.getsize(os.path.join(b, f))
               for b, _, fs in os.walk(DIST) for f in fs)

    crudo = 0
    for f in ARCHIVOS:
        r = os.path.join(RAIZ, f)
        if os.path.exists(r):
            crudo += os.path.getsize(r)
    for c in CARPETAS:
        for b, _, fs in os.walk(os.path.join(RAIZ, c)):
            crudo += sum(os.path.getsize(os.path.join(b, f)) for f in fs if limpio(f))

    print("\n  dist/ listo: %d archivos, %.1f MB (%.0f%% menos que el original)"
          % (n, peso / 1024 / 1024, 100 * (1 - peso / crudo) if crudo else 0))
    comprobar_sitemap()
    print("  dist/ listo. Para publicar: python subir.py")

    # aviso de seguridad
    colados = [f for b, _, fs in os.walk(DIST) for f in fs if not limpio(f)]
    if colados:
        print("  ¡OJO! se han colado archivos que no deberían: %s" % colados)
    else:
        print("  Comprobado: ningun .py ni .md dentro de dist/.")



def comprobar_sitemap():
    """Que no se quede ninguna pagina fuera de dist/.

    Paso esto porque ya ha pasado: se genera una pagina nueva, se olvida
    anadir su carpeta a CARPETAS y la web publica se queda sin ella, con el
    enlace del pie apuntando a un 404. El sitemap ya sabe todo lo que deberia
    existir, asi que se comprueba contra el.
    """
    import re
    mapa = os.path.join(DIST, "sitemap.xml")
    if not os.path.exists(mapa):
        return
    faltan = []
    for url in re.findall(r"<loc>([^<]+)</loc>", io.open(mapa, encoding="utf-8").read()):
        ruta = url.split("montatuserver.com")[-1]
        destino = os.path.join(DIST, *[p for p in ruta.split("/") if p], "index.html")
        if not os.path.exists(destino):
            faltan.append(ruta)
    if faltan:
        print("  " + chr(27) + "[91mOJO: estas paginas se generan pero NO se publican:" + chr(27) + "[0m")
        for r in faltan:
            print("     " + r)
        print("     anade su carpeta a CARPETAS en publicar.py")
    else:
        print("  sitemap: las %d paginas estan en dist/" %
              len(re.findall(r"<loc>", io.open(mapa, encoding="utf-8").read())))


if __name__ == "__main__":
    main()
