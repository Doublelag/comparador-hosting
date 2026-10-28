# -*- coding: utf-8 -*-
"""
Comprobaciones rápidas del sitio, sin red y sin dependencias (solo la
biblioteca estándar de Python; si hay Node, también revisa la sintaxis JS).

Uso:  python comprobar.py

Mira estas cosas sobre lo que ya está generado en el repositorio:

  1. Enlaces internos: cada href/src/url(...) que empieza por "/" en las
     páginas y en styles.css apunta a un archivo o página que existe (o a una
     redirección de _redirects, o a la API del Worker).
  2. Publicación: esos destinos están entre lo que publicar.py copia a dist/,
     para que no funcione en local y dé 404 en la web de verdad. Y que cada
     .css/.js publicado tenga su entrada de caché en _headers.
  3. Datos: hosts.js se puede leer como JSON y cada hosting tiene id, nombre,
     moneda y un precio de Minecraft con RAM y precios positivos.
  4. JavaScript: cada .js de la raíz pasa `node --check` (si Node está).

Sale con código 1 si algo falla, así sirve también para GitHub Actions.
"""

import io
import json
import os
import re
import shutil
import subprocess
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
SALTAR = {".git", ".claude", ".github", "dist", "node_modules", "__pycache__",
          "plantillas_src", "_fuentes_ttf"}
ATRIBUTOS = re.compile(r'\b(?:href|src|data-indice)="(/[^"]*)"')
SRCSET = re.compile(r'\bsrcset="([^"]*)"')
CSS_URL = re.compile(r"url\(\s*['\"]?(/[^)'\"]+)['\"]?\s*\)")

fallos = []


def fallo(msg):
    fallos.append(msg)


def paginas():
    for base, dirs, ficheros in os.walk(RAIZ):
        dirs[:] = sorted(d for d in dirs if d not in SALTAR and not d.startswith("."))
        for f in sorted(ficheros):
            if f.endswith(".html"):
                yield os.path.join(base, f)


def redirecciones():
    """Orígenes de _redirects: exactos y con comodín (/algo/*)."""
    exactas, prefijos = set(), []
    ruta = os.path.join(RAIZ, "_redirects")
    if os.path.exists(ruta):
        for linea in io.open(ruta, encoding="utf-8"):
            linea = linea.strip()
            if not linea or linea.startswith("#"):
                continue
            origen = linea.split()[0]
            if origen.endswith("*"):
                prefijos.append(origen[:-1])
            else:
                exactas.add(origen)
    return exactas, prefijos


def destino_local(url):
    """Archivo del repo que sirve esa URL, o None si no existe."""
    partes = [p for p in url.split("/") if p]
    ruta = os.path.join(RAIZ, *partes)
    if os.path.isfile(ruta):
        return ruta
    indice = os.path.join(ruta, "index.html")
    if os.path.isfile(indice):
        return indice
    return None


def se_publica(ruta, archivos, carpetas):
    rel = os.path.relpath(ruta, RAIZ).replace("\\", "/")
    primera = rel.split("/")[0]
    return rel in archivos or (primera in carpetas and "/" in rel)


def comprobar_enlaces():
    sys.path.insert(0, RAIZ)
    import publicar  # solo listas; no ejecuta nada al importarse
    archivos, carpetas = set(publicar.ARCHIVOS), set(publicar.CARPETAS)
    exactas, prefijos = redirecciones()

    vistos = 0
    fuentes = list(paginas()) + [os.path.join(RAIZ, "styles.css")]
    for fichero in fuentes:
        texto = io.open(fichero, encoding="utf-8").read()
        urls = ATRIBUTOS.findall(texto) + CSS_URL.findall(texto)
        for s in SRCSET.findall(texto):
            urls += [t.split()[0] for t in s.split(",") if t.strip().startswith("/")]
        origen = os.path.relpath(fichero, RAIZ).replace("\\", "/")
        for url in urls:
            if url.startswith("//"):
                continue  # enlace externo sin protocolo
            limpia = re.split(r"[?#]", url, 1)[0] or "/"
            if limpia.startswith("/api/"):
                continue  # la sirve worker.js
            vistos += 1
            ruta = destino_local(limpia)
            if ruta is None:
                if limpia in exactas or limpia.rstrip("/") in exactas \
                        or any(limpia.startswith(p) for p in prefijos):
                    continue
                fallo("%s: enlace roto %s" % (origen, url))
            elif not se_publica(ruta, archivos, carpetas):
                fallo("%s: %s existe pero publicar.py no lo copia a dist/" % (origen, url))
    print("  enlaces internos revisados: %d" % vistos)

    # _headers: cada .css/.js publicado lleva su caché larga (van uno a uno)
    cabeceras = io.open(os.path.join(RAIZ, "_headers"), encoding="utf-8").read()
    for f in sorted(archivos):
        if f.endswith((".css", ".js")) and not re.search(r"^/%s$" % re.escape(f), cabeceras, re.M):
            fallo("_headers: falta la entrada de /%s" % f)


def comprobar_datos():
    texto = io.open(os.path.join(RAIZ, "hosts.js"), encoding="utf-8").read()
    marca = "window.DATOS ="
    try:
        datos = json.loads(texto[texto.index(marca) + len(marca):].strip().rstrip(";"))
    except Exception as e:
        fallo("hosts.js: no se puede leer como JSON (%s)" % e)
        return

    def positivo(x):
        return isinstance(x, (int, float)) and not isinstance(x, bool) and x > 0

    hosts = datos.get("hosts") or []
    if not hosts:
        fallo("hosts.js: no hay hostings")
    ids = set()
    for h in hosts:
        hid = h.get("id", "?")
        if hid in ids:
            fallo("hosts.js: id repetido %s" % hid)
        ids.add(hid)
        for campo in ("id", "nombre", "moneda"):
            if not h.get(campo):
                fallo("hosts.js: %s sin %s" % (hid, campo))
        mc = (h.get("precios") or {}).get("minecraft")
        if not mc:
            fallo("hosts.js: %s sin precio de Minecraft" % hid)
            continue
        modelo = mc.get("modelo")
        if modelo == "porGB":
            if not positivo(mc.get("porGB")):
                fallo("hosts.js: %s porGB no positivo" % hid)
        elif modelo == "plano":
            if not (positivo(mc.get("precio")) and positivo(mc.get("ram"))):
                fallo("hosts.js: %s plan plano sin precio/ram positivos" % hid)
        elif modelo in ("tabla", "slots"):
            tiers = mc.get("tiers") or []
            if not tiers:
                fallo("hosts.js: %s sin escalones" % hid)
            for t in tiers:
                if not (isinstance(t, list) and len(t) == 2 and positivo(t[0]) and positivo(t[1])):
                    fallo("hosts.js: %s escalón raro %r" % (hid, t))
            gbs = [t[0] for t in tiers if isinstance(t, list) and t]
            if gbs != sorted(gbs):
                fallo("hosts.js: %s escalones desordenados" % hid)
        else:
            fallo("hosts.js: %s modelo desconocido %r" % (hid, modelo))
        ficha = h.get("ficha")
        if ficha and destino_local(ficha) is None:
            fallo("hosts.js: %s apunta a una ficha que no existe (%s)" % (hid, ficha))
    partner = datos.get("partner") or {}
    if partner.get("hostId") and partner["hostId"] not in ids:
        fallo("hosts.js: el partner apunta a un hosting que no existe (%s)" % partner["hostId"])
    print("  hostings revisados: %d" % len(hosts))


def comprobar_js():
    node = shutil.which("node")
    if not node:
        print("  (sin Node: no se revisa la sintaxis JS)")
        return
    js = sorted(f for f in os.listdir(RAIZ) if f.endswith(".js"))
    for f in js:
        r = subprocess.run([node, "--check", os.path.join(RAIZ, f)],
                           capture_output=True, text=True)
        if r.returncode != 0:
            fallo("%s: error de sintaxis\n%s" % (f, r.stderr.strip()))
    print("  archivos JS revisados: %d" % len(js))


def main():
    print("Comprobando el sitio…")
    comprobar_enlaces()
    comprobar_datos()
    comprobar_js()
    if fallos:
        print("\n%d problemas:" % len(fallos))
        for f in fallos:
            print("  - " + f)
        sys.exit(1)
    print("\nTodo bien.")


if __name__ == "__main__":
    main()
