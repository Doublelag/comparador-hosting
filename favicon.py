# -*- coding: utf-8 -*-
"""
Icono de la web con la identidad v2: cubo isométrico (un bloque de Minecraft,
un servidor) en los dos verdes de la marca sobre el azul noche.

Genera favicon.svg (el que usan los navegadores modernos), favicon.ico
(32 px, para lo viejo y para Google) y apple-touch-icon.png (180 px).

Uso: python favicon.py
"""
import io, os
from PIL import Image, ImageDraw

RAIZ = os.path.dirname(os.path.abspath(__file__))

BG, ACC, ACC2, SOMBRA = "#0B132B", "#5BC0BE", "#6FFFE9", "#2A8886"

SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
<rect width="64" height="64" rx="14" fill="%(bg)s"/>
<path d="M32 10 54 22v22L32 56 10 44V22z" fill="%(sombra)s"/>
<path d="M32 10 54 22 32 34 10 22z" fill="%(acc2)s"/>
<path d="M32 34v22L10 44V22z" fill="%(acc)s"/>
<path d="M32 34v22l22-12V22z" fill="%(sombra)s"/>
</svg>
""" % dict(bg=BG, acc=ACC, acc2=ACC2, sombra=SOMBRA)


def _hex(c):
    return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))


def png(lado):
    """El mismo dibujo con Pillow (no hay rasterizador SVG a mano)."""
    k = 8  # supermuestreo para que los bordes salgan suaves
    L = lado * k
    img = Image.new("RGBA", (L, L), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    s = L / 64.0
    d.rounded_rectangle([0, 0, L - 1, L - 1], radius=int(14 * s), fill=_hex(BG))
    P = lambda *pts: [(x * s, y * s) for x, y in pts]
    d.polygon(P((32, 10), (54, 22), (32, 34), (10, 22)), fill=_hex(ACC2))
    d.polygon(P((32, 34), (32, 56), (10, 44), (10, 22)), fill=_hex(ACC))
    d.polygon(P((32, 34), (32, 56), (54, 44), (54, 22)), fill=_hex(SOMBRA))
    return img.resize((lado, lado), Image.LANCZOS)


def main():
    io.open(os.path.join(RAIZ, "favicon.svg"), "w", encoding="utf-8").write(SVG)
    png(180).save(os.path.join(RAIZ, "apple-touch-icon.png"), "PNG", optimize=True)
    png(32).save(os.path.join(RAIZ, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
    png(512).save(os.path.join(RAIZ, "icono-512.png"), "PNG", optimize=True)
    print("favicon.svg, favicon.ico, apple-touch-icon.png, icono-512.png")


if __name__ == "__main__":
    main()
