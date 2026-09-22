# -*- coding: utf-8 -*-
"""
Revisor de precios — te dice QUÉ ha cambiado, no te lo cambia.

El problema que resuelve: la web tiene 24 entradas de precio sacadas a mano.
Revisarlos uno a uno cada dos meses es una tarde entera, y si no se hace la web
empieza a mentir sin querer — que es lo único que no se puede permitir.

Lo que hace:
  1. Entra en la página de precios de cada hosting (el campo `fuente` de hosts.js).
  2. Saca todos los números con pinta de precio.
  3. Comprueba si los precios que tenemos guardados siguen apareciendo ahí.
  4. Te lista SOLO los sospechosos, con el enlace para mirarlo tú.

Lo que NO hace, a propósito:
  · No toca hosts.js. Los precios se cambian a mano después de mirarlos, porque
    un número mal leído se publica en 46 páginas.
  · No se fía de sí mismo. Muchas de estas webs pintan el precio con JavaScript
    y en el HTML crudo no está (a Shockbyte ya nos pasó). Cuando no encuentra
    nada, lo dice y te manda a mirarlo, en vez de callarse y dar el precio por
    bueno. Un revisor que da falsos "todo correcto" es peor que no tenerlo.

Uso:
    python revisar_precios.py                 # todos
    python revisar_precios.py valheim         # solo un juego
"""

import io, json, os, re, sys, urllib.request, urllib.error

RAIZ = os.path.dirname(os.path.abspath(__file__))
TIEMPO_LIMITE = 20

CABECERAS = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"),
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
}

VERDE, AMBAR, ROJO, GRIS, FIN = "\033[92m", "\033[93m", "\033[91m", "\033[90m", "\033[0m"


def datos():
    s = io.open(os.path.join(RAIZ, "hosts.js"), encoding="utf-8").read()
    crudo = s[s.index("window.DATOS =") + len("window.DATOS ="):].strip().rstrip(";").strip()
    return json.loads(crudo)


def bajar(url):
    """Devuelve el texto de la página, o None si no se puede."""
    try:
        req = urllib.request.Request(url, headers=CABECERAS)
        with urllib.request.urlopen(req, timeout=TIEMPO_LIMITE) as r:
            crudo = r.read(3_000_000)
        return crudo.decode("utf-8", "ignore")
    except Exception:
        return None


def precios_de_la_pagina(html):
    """Todos los números con pinta de precio que aparecen en la página.

    Se queda con el número, sin moneda: comparamos cifras, no divisas. Un
    hosting puede enseñarte 14.99 o 14,99 según de dónde entres.
    """
    texto = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    texto = re.sub(r"<[^>]+>", " ", texto)
    fuera = set()
    for m in re.finditer(r"(?<![\d.,])(\d{1,4})[.,](\d{2})(?![\d])", texto):
        fuera.add(round(float("%s.%s" % (m.group(1), m.group(2))), 2))
    for m in re.finditer(r"[$€]\s?(\d{1,4})(?![\d.,])", texto):
        fuera.add(float(m.group(1)))
    for m in re.finditer(r"(\d{1,4})\s?[$€]", texto):
        fuera.add(float(m.group(1)))
    return fuera


def precios_guardados(pr):
    """Los números que ESTA web publica de ese hosting."""
    m = pr["modelo"]
    if m == "porGB":
        # el precio por giga rara vez sale tal cual; se comprueban planes tipicos
        return [round(pr["porGB"] * n, 2) for n in (1, 2, 4, 8, 16)]
    if m in ("tabla", "slots"):
        return [round(p, 2) for _, p in pr["tiers"]]
    if m == "plano":
        return [round(pr["precio"], 2)]
    if m == "slots":
        return [round(p, 2) for _, p in pr["tiers"]]
    return []


def main():
    juego = sys.argv[1] if len(sys.argv) > 1 else None
    d = datos()

    print()
    print("Revisando precios%s. Comprobado por última vez: %s"
          % (" de " + juego if juego else "", d["comprobado"]))
    print("=" * 78)

    cambiados, sin_leer, correctos = [], [], 0

    for h in d["hosts"]:
        fuente = h.get("fuente")
        precios = h.get("precios") or {}
        juegos = [juego] if juego else list(precios)

        for j in juegos:
            pr = precios.get(j)
            if not pr:
                continue
            etiqueta = "%s · %s" % (h["nombre"], j)

            if not fuente:
                sin_leer.append((etiqueta, "no tiene 'fuente' en hosts.js", ""))
                continue

            html = bajar(fuente)
            if html is None:
                sin_leer.append((etiqueta, "no he podido abrir la página", fuente))
                continue

            en_web = precios_de_la_pagina(html)
            if not en_web:
                sin_leer.append((etiqueta, "la página no da precios en el HTML "
                                           "(los pinta con JavaScript)", fuente))
                continue

            esperados = precios_guardados(pr)
            if not esperados:
                sin_leer.append((etiqueta, "modelo '%s': hay que mirarlo a mano"
                                 % pr["modelo"], fuente))
                continue

            # Con margen de dos centimos: quien cobra "por giga" casi siempre
            # remata en ,99 (16 GB a 19,99 y no a 20,00). Sin esta tolerancia
            # el revisor grita en cada hosting por GB y acabas ignorandolo,
            # que es la peor forma de que falle una alarma.
            encontrados = [p for p in esperados
                           if any(abs(p - w) <= 0.02 for w in en_web)]
            if encontrados:
                correctos += 1
                print("%s  OK    %s%s  (sigo viendo %s)"
                      % (VERDE, etiqueta.ljust(34), FIN,
                         ", ".join("%.2f" % p for p in encontrados[:3])))
            else:
                cambiados.append((etiqueta, esperados, sorted(en_web)[:8], fuente))
                print("%s  OJO   %s%s  ninguno de nuestros precios aparece ya"
                      % (ROJO, etiqueta.ljust(34), FIN))

    print("=" * 78)
    print("%d parecen correctos · %d sospechosos · %d sin poder comprobar"
          % (correctos, len(cambiados), len(sin_leer)))

    if cambiados:
        print()
        print("%sHAY QUE MIRAR ESTOS%s" % (ROJO, FIN))
        for etiqueta, esperados, vistos, url in cambiados:
            print()
            print("  %s" % etiqueta)
            print("    tenemos:  %s" % ", ".join("%.2f" % p for p in esperados[:6]))
            print("    en su web: %s" % ", ".join("%.2f" % p for p in vistos))
            print("    %s" % url)

    if sin_leer:
        print()
        print("%sESTOS NO LOS PUEDO LEER — míralos tú%s" % (AMBAR, FIN))
        for etiqueta, motivo, url in sin_leer:
            print("  %-34s %s" % (etiqueta, motivo))
            if url:
                print("  %s%s%s" % (GRIS, url, FIN))

    print()
    print("Si cambia algo: edítalo en hosts.js, actualiza \"comprobado\" con la")
    print("fecha de hoy y ejecuta build.py. No lo toques a mano en el HTML.")
    print()


if __name__ == "__main__":
    main()
