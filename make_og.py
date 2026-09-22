# -*- coding: utf-8 -*-
"""
Genera las tarjetas que se ven al pegar el enlace en WhatsApp, Discord,
Twitter o Telegram: og-image.jpg, la misma para toda la web.

Es más importante de lo que parece: esta herramienta se comparte por chat
("mira, calcula la RAM que necesitas"), y un enlace sin imagen se ignora.

Uso:  python make_og.py
"""

import os
from PIL import Image, ImageDraw, ImageFont

RAIZ = os.path.dirname(os.path.abspath(__file__))
W, H = 1200, 630

# Cuantos hostings hay en la tabla, leido de hosts.js: escrito a mano se queda
# viejo en cuanto se anade uno, y es de las primeras cosas que se ven.
import io as _io, json as _json
# Se cuentan empresas, no gamas: PebbleHost Budget y Premium son un hosting.
CUANTOS = len({h.get("ficha") or h["id"] for h in _json.loads(
    _io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "hosts.js"),
             encoding="utf-8").read().split("window.DATOS =")[1].strip().rstrip(";"))["hosts"]})

# Mismos colores que la web
FONDO      = (11, 15, 20)
FONDO_CARD = (20, 29, 42)
LINEA      = (35, 48, 66)
TXT        = (232, 238, 246)
DIM        = (147, 164, 184)
ACC        = (62, 224, 138)

F  = "C:/Windows/Fonts/segoeuib.ttf"   # Segoe UI Bold
FR = "C:/Windows/Fonts/segoeui.ttf"    # Segoe UI Regular

# (carpeta destino, sufijo del titular, chips). carpeta None = portada.
JUEGOS = [
    (None, None, ["Vanilla", "Plugins", "Modpacks", "Java y Bedrock"]),
]


def fuente(path, size):
    return ImageFont.truetype(path, size)


def ancho(d, txt, f):
    return d.textbbox((0, 0), txt, font=f)[2]


def ajustar(d, txt, f_path, maximo, inicial):
    """Baja el tamaño de fuente hasta que el texto quepa a lo ancho."""
    size = inicial
    while size > 34:
        f = fuente(f_path, size)
        if ancho(d, txt, f) <= maximo:
            return f
        size -= 3
    return fuente(f_path, 34)


def crear(carpeta, sufijo, chips):
    img = Image.new("RGB", (W, H), FONDO)
    d = ImageDraw.Draw(img)

    # Resplandor verde suave arriba a la derecha
    brillo = Image.new("RGB", (W, H), FONDO)
    bd = ImageDraw.Draw(brillo)
    for i in range(28, 0, -1):
        r = i * 26
        c = tuple(int(FONDO[k] + (ACC[k] - FONDO[k]) * (0.055 * (1 - i / 28.0)))
                  for k in range(3))
        bd.ellipse([W - 180 - r, -240 - r, W - 180 + r, -240 + r], fill=c)
    img = Image.blend(img, brillo, 0.85)
    d = ImageDraw.Draw(img)

    # Marca
    f_marca = fuente(F, 30)
    d.text((70, 62), "MontaTuServer", font=f_marca, fill=TXT)
    d.text((70 + ancho(d, "MontaTuServer", f_marca) + 14, 62), ".com",
           font=fuente(FR, 30), fill=ACC)

    # Titular
    linea1 = "¿Cuánta RAM necesita tu"
    linea2_pre, linea2_acc = ("servidor de ", "Minecraft") if not sufijo else ("un servidor ", sufijo[3:])
    f_h1 = fuente(F, 76)
    # el nombre del juego puede ser largo: ajusta para que quepa
    f_h1 = ajustar(d, linea2_pre + linea2_acc + "?", F, W - 140, 76)

    d.text((70, 150), linea1, font=fuente(F, 76), fill=TXT)
    y = 150 + 88
    d.text((70, y), linea2_pre, font=f_h1, fill=TXT)
    x = 70 + ancho(d, linea2_pre, f_h1)
    d.text((x, y), linea2_acc, font=f_h1, fill=ACC)
    d.text((x + ancho(d, linea2_acc, f_h1), y), "?", font=f_h1, fill=TXT)

    # Subtítulo
    f_sub = fuente(FR, 30)
    d.text((70, 348), "Calcula tus GB y mira lo que cuestan en cada hosting.",
           font=f_sub, fill=DIM)
    d.text((70, 389), "%d hostings comparados, con precios comprobados a mano." % CUANTOS,
           font=f_sub, fill=DIM)

    # Chips
    f_chip = fuente(FR, 24)
    x = 70
    for txt in chips:
        w = ancho(d, txt, f_chip)
        if x + w + 40 > W - 70:
            break
        d.rounded_rectangle([x, 470, x + w + 40, 522], radius=26,
                            fill=FONDO_CARD, outline=LINEA, width=2)
        d.text((x + 20, 483), txt, font=f_chip, fill=DIM)
        x += w + 54

    # Franja inferior de acento
    d.rectangle([0, H - 9, W, H], fill=ACC)

    destino = os.path.join(RAIZ, carpeta, "og-image.jpg") if carpeta \
        else os.path.join(RAIZ, "og-image.jpg")
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    # 82 basta de sobra para una tarjeta de 1200x630 con texto plano, y pesa
    # casi la mitad que 92. La ve mucha gente al pegar el enlace en un chat.
    img.save(destino, "JPEG", quality=82, optimize=True, progressive=True)
    return destino


if __name__ == "__main__":
    for carpeta, sufijo, chips in JUEGOS:
        ruta = crear(carpeta, sufijo, chips)
        print("  " + os.path.relpath(ruta, RAIZ).replace("\\", "/"))
    print("\n%d imágenes de 1200x630." % len(JUEGOS))
