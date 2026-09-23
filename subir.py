# -*- coding: utf-8 -*-
"""
Publicar la web entera con un solo comando:  python subir.py

Hace, en este orden:
  1. build.py      → genera todas las páginas
  2. publicar.py   → deja en dist/ solo lo que se puede publicar
  3. wrangler      → lo sube a Cloudflare (montatuserver.com)
  4. una ronda de comprobaciones en el dominio de verdad

Si algo falla por el camino, PARA y no sube nada: más vale no publicar que
publicar algo roto. Con --local hace todo menos subir, para mirar antes.

Antes existía el baile de Netlify (arrastrar dist a mano, 15 créditos por
subida). Esto es su sustituto: gratis, sin límite y sin arrastrar nada.
"""

import io
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request

RAIZ = os.path.dirname(os.path.abspath(__file__))
DOMINIO = "https://montatuserver.com"
WRANGLER = os.path.join(os.environ.get("APPDATA", ""), "npm", "wrangler.cmd")

# Lo que se comprueba después de subir. Si una de estas falla, algo gordo se ha
# roto: son las puertas de entrada y las trampas que ya hemos pisado antes.
COMPROBAR = [
    ("/", 200),
    ("/hosting/", 200),
    ("/versus/", 200),
    ("/ofertas/", 200),
    ("/plantillas/smp-amigos/", 200),
    ("/en/", 200),
    ("/en/hosting/", 200),
    ("/aviso-legal/", 200),
    ("/comparar/", 301),          # el nombre viejo de Versus
    ("/LEEME.md", 404),           # nunca debe publicarse
    ("/build.py", 404),
]

VERDE, ROJO, GRIS, FIN = "\033[92m", "\033[91m", "\033[90m", "\033[0m"


def paso(titulo):
    print("\n%s== %s%s" % (GRIS, titulo, FIN))


def correr(orden, cwd=RAIZ):
    r = subprocess.run(orden, cwd=cwd, shell=isinstance(orden, str))
    if r.returncode != 0:
        print("%sFALLO en: %s%s" % (ROJO, orden, FIN))
        sys.exit(1)


def codigo(url):
    req = urllib.request.Request(url, headers={"User-Agent": "subir.py"})
    try:
        class SinSeguir(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, *a, **k):
                return None
        op = urllib.request.build_opener(SinSeguir)
        return op.open(req, timeout=20).getcode()
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:
        return str(e)


def main():
    solo_local = "--local" in sys.argv
    py = sys.executable

    paso("1/4  Generando las páginas")
    correr([py, "build.py"])

    paso("2/4  Preparando dist/")
    correr([py, "publicar.py"])

    if solo_local:
        print("\n%sHecho (modo local): dist/ está listo, no se ha subido nada.%s" % (VERDE, FIN))
        return

    paso("3/4  Subiendo a Cloudflare")
    if not os.path.exists(WRANGLER):
        print("%sNo encuentro wrangler en %s%s" % (ROJO, WRANGLER, FIN))
        print("Instálalo con:  npm i -g wrangler   (y luego:  wrangler login)")
        sys.exit(1)
    correr([WRANGLER, "deploy"])

    paso("4/4  Comprobando la web publicada")
    time.sleep(5)
    fallos = 0
    for ruta, esperado in COMPROBAR:
        c = codigo(DOMINIO + ruta)
        bien = c == esperado
        fallos += 0 if bien else 1
        print("  %s%s  %-28s %s (esperado %s)%s"
              % (VERDE if bien else ROJO, "OK  " if bien else "MAL ", ruta, c, esperado, FIN))

    if fallos:
        print("\n%s%d comprobaciones han fallado. Míralo antes de anunciar nada.%s"
              % (ROJO, fallos, FIN))
        sys.exit(1)
    print("\n%sPublicado y comprobado: %s%s" % (VERDE, DOMINIO, FIN))


if __name__ == "__main__":
    main()
