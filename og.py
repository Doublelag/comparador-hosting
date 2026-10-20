# -*- coding: utf-8 -*-
"""
Una tarjeta por página para cuando se pega el enlace en Discord, WhatsApp,
Twitter o Telegram: og/<slug>.jpg. La pone marco.aplicar al enmarcar.

Antes toda la web compartía og-image.jpg. Un enlace a la ficha de Kinetic con
la imagen genérica de la calculadora no dice nada; con su logo y sus precios
se abre. Es la parte de la web que más se comparte por chat.

Tres tipos de tarjeta:
  · ficha de hosting: logo, nombre, lo que cobra por 4, 8 y 16 GB y el €/GB.
  · versus: los dos logos enfrentados.
  · cualquier otra página: el h1 y la descripción.

No se regenera si el texto no ha cambiado (sidecar .txt junto al jpg): asi el
build no tarda y git no ve 100 jpg nuevos en cada pasada.
"""
import hashlib, html as _html, io, os, re

from PIL import Image, ImageDraw, ImageFont

RAIZ = os.path.dirname(os.path.abspath(__file__))
CARPETA = os.path.join(RAIZ, "og")
DOMINIO = "https://montatuserver.com"
W, H = 1200, 630

# Mismos colores que styles.css (tema noche)
BG, BG2, CARD, LINEA = (11, 19, 43), (19, 28, 56), (28, 37, 65), (46, 58, 92)
TXT, DIM, FAINT = (238, 246, 247), (169, 188, 203), (120, 144, 166)
ACC, ACC2, INK = (91, 192, 190), (111, 255, 233), (11, 19, 43)

_TTF = os.path.join(RAIZ, "_fuentes_ttf")


def _fuente(nombre, size, peso):
    f = ImageFont.truetype(os.path.join(_TTF, nombre), size)
    ejes = [a["name"] for a in f.get_variation_axes()]
    vals = []
    for a in f.get_variation_axes():
        if a["name"] == b"Weight":
            vals.append(peso)
        else:
            vals.append(a["default"])
    f.set_variation_by_axes(vals)
    return f


def display(size, peso=800):
    return _fuente("Bricolage.ttf", size, peso)


def texto(size, peso=500):
    return _fuente("Instrument.ttf", size, peso)


def mono(size, peso=700):
    return _fuente("JetBrainsMono.ttf", size, peso)


def _ancho(d, t, f):
    return d.textbbox((0, 0), t, font=f)[2]


def _lineas(d, t, f, maximo, max_lineas):
    """Parte el texto en líneas que quepan; la última lleva puntos si sobra."""
    palabras, lineas, actual = t.split(), [], ""
    for p in palabras:
        prueba = (actual + " " + p).strip()
        if _ancho(d, prueba, f) <= maximo:
            actual = prueba
        else:
            lineas.append(actual)
            actual = p
            if len(lineas) == max_lineas:
                break
    if len(lineas) < max_lineas and actual:
        lineas.append(actual)
    if len(palabras) and " ".join(lineas) != " ".join(palabras):
        ultima = lineas[-1]
        while _ancho(d, ultima + "…", f) > maximo and " " in ultima:
            ultima = ultima.rsplit(" ", 1)[0]
        lineas[-1] = ultima + "…"
    return lineas


def _fondo():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # Cielo del hero si existe, muy atenuado, para que la tarjeta sea "la web"
    cielo = os.path.join(RAIZ, "hero-cielo.webp")
    if os.path.exists(cielo):
        c = Image.open(cielo).convert("RGB")
        c = c.resize((W, int(c.height * W / c.width)))
        if c.height < H:
            c = c.resize((W, H))
        c = c.crop((0, 0, W, H))
        img = Image.blend(img, c, 0.35)
        d = ImageDraw.Draw(img)
    # Degradado oscuro abajo para que el texto lea
    for y in range(H // 2, H):
        a = (y - H // 2) / (H / 2)
        d.line([(0, y), (W, y)], fill=tuple(int(BG[i] * a + img.getpixel((W // 2, y))[i] * (1 - a)) for i in range(3)))
    # Brillo acento arriba a la derecha
    brillo = Image.new("RGB", (W, H), (0, 0, 0))
    bd = ImageDraw.Draw(brillo)
    for i in range(30, 0, -1):
        r = i * 24
        k = 0.09 * (1 - i / 30.0)
        bd.ellipse([W - 120 - r, -200 - r, W - 120 + r, -200 + r],
                   fill=tuple(int(ACC[j] * k) for j in range(3)))
    img = Image.fromarray(__import__("numpy").clip(
        __import__("numpy").asarray(img, dtype="int16") + __import__("numpy").asarray(brillo, dtype="int16"), 0, 255).astype("uint8")) \
        if _hay_numpy() else img
    return img


def _hay_numpy():
    try:
        import numpy  # noqa
        return True
    except ImportError:
        return False


def _pie(d, lang, comprobado):
    f = texto(26, 600)
    d.text((70, H - 78), "montatuserver", font=f, fill=TXT)
    x = 70 + _ancho(d, "montatuserver", f)
    d.text((x, H - 78), ".com", font=f, fill=ACC)
    nota = ("Precios comprobados a mano · %s" if lang == "es" else "Prices checked by hand · %s") % comprobado
    fm = mono(20, 500)
    d.text((W - 70 - _ancho(d, nota, fm), H - 74), nota, font=fm, fill=FAINT)
    d.line([(70, H - 104), (W - 70, H - 104)], fill=LINEA, width=2)


def _chip(d, x, y, etiqueta, valor, ancho=230):
    d.rounded_rectangle([x, y, x + ancho, y + 96], radius=14, fill=CARD, outline=LINEA, width=2)
    d.text((x + 20, y + 14), etiqueta, font=mono(18, 500), fill=FAINT)
    d.text((x + 20, y + 42), valor, font=mono(34, 700), fill=TXT)
    return x + ancho + 18


def _logo(img, slug, x, y, lado):
    ruta = os.path.join(RAIZ, "logos", slug + ".png")
    if not os.path.exists(ruta):
        return False
    lg = Image.open(ruta).convert("RGBA").resize((lado - 28, lado - 28), Image.LANCZOS)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x, y, x + lado, y + lado], radius=22, fill=(255, 255, 255))
    img.paste(lg, (x + 14, y + 14), lg)
    return True


# ------------------------------------------------------------------ tarjetas
def ficha(slug, nombre, chips, veredicto, lang, comprobado):
    img = _fondo()
    d = ImageDraw.Draw(img)
    hay_logo = _logo(img, slug, 70, 70, 120)
    x = 214 if hay_logo else 70
    d.text((x, 62), "HOSTING DE MINECRAFT" if lang == "es" else "MINECRAFT HOSTING",
           font=mono(20, 500), fill=ACC)
    f = display(76, 800)
    while _ancho(d, nombre, f) > W - x - 70 and f.size > 44:
        f = display(f.size - 4, 800)
    d.text((x, 92), nombre, font=f, fill=TXT)
    y = 222
    xx = 70
    for et, val in chips:
        xx = _chip(d, xx, y, et, val)
    fv = texto(28, 500)
    for i, l in enumerate(_lineas(d, veredicto, fv, W - 140, 3)):
        d.text((70, 346 + i * 38), l, font=fv, fill=DIM)
    _pie(d, lang, comprobado)
    return img


def versus(a, b, lang, comprobado, titulo):
    img = _fondo()
    d = ImageDraw.Draw(img)
    d.text((70, 62), "VERSUS", font=mono(20, 500), fill=ACC)
    lado = 150
    cy = 150
    _logo(img, a[0], 150, cy, lado)
    _logo(img, b[0], W - 150 - lado, cy, lado)
    for nombre, cx in ((a[1], 150 + lado // 2), (b[1], W - 150 - lado // 2)):
        f = display(64, 800)
        while _ancho(d, nombre, f) > W // 2 - 110 and f.size > 34:
            f = display(f.size - 3, 800)
        d.text((cx - _ancho(d, nombre, f) // 2, cy + lado + 18), nombre, font=f, fill=TXT)
    fv = display(120, 800)
    d.text((W // 2 - _ancho(d, "vs", fv) // 2, cy + 8), "vs", font=fv, fill=ACC2)
    ft = texto(30, 500)
    for i, l in enumerate(_lineas(d, titulo, ft, W - 140, 2)):
        d.text((W // 2 - _ancho(d, l, ft) // 2, 420 + i * 40), l, font=ft, fill=DIM)
    _pie(d, lang, comprobado)
    return img


def generica(etiqueta, titulo, desc, lang, comprobado):
    img = _fondo()
    d = ImageDraw.Draw(img)
    d.text((70, 62), etiqueta.upper(), font=mono(20, 500), fill=ACC)
    f = display(72, 800)
    lineas = _lineas(d, titulo, f, W - 140, 3)
    while len(lineas) > 2 and f.size > 52:
        f = display(f.size - 4, 800)
        lineas = _lineas(d, titulo, f, W - 140, 3)
    y = 100
    for l in lineas:
        d.text((70, y), l, font=f, fill=TXT)
        y += int(f.size * 1.12)
    fd = texto(30, 500)
    y += 18
    for l in _lineas(d, desc, fd, W - 140, 3 if len(lineas) < 3 else 2):
        d.text((70, y), l, font=fd, fill=DIM)
        y += 40
    _pie(d, lang, comprobado)
    return img


# ------------------------------------------------------------------ por URL
def _slug(url):
    s = url.strip("/").replace("/", "-")
    return s or "portada"


def _limpio(t):
    return _html.unescape(re.sub(r"<[^>]+>", "", t)).strip()


def _datos_ficha(url, lang):
    import hostings
    m = re.match(r"^(?:/en)?/hosting/([^/]+)/$", url)
    if not m:
        return None
    slug = m.group(1)
    hid = next((k for k, f in hostings.FICHAS.items() if f["url"] == slug), None)
    if not hid:
        return None
    d = hostings.datos()
    h = next(x for x in d["hosts"] if x["id"] == hid)
    cambio = d["cambioUsdEur"]
    chips = []
    for gb in (4, 8, 16):
        p, da = hostings.precio_para(h, "minecraft", gb, cambio)
        chips.append(("%d GB" % gb, hostings.eur(p) if p is not None else ("no llega" if lang == "es" else "n/a")))
    porgb = None
    for gb_ref in (8, 6, 4, 2):
        p, da = hostings.precio_para(h, "minecraft", gb_ref, cambio)
        if p is not None and (da or "").endswith("GB"):
            try:
                porgb = p / int(da.split()[0]); break
            except ValueError:
                pass
    chips.append(("€/GB" if lang == "es" else "€ per GB", hostings.eur(porgb) if porgb else "—"))
    f = hostings.FICHAS[hid]
    if lang == "en":
        import fichas_en
        t = fichas_en.FICHAS_EN.get(hid, {})
        ver = t.get("veredicto", f["veredicto"])
    else:
        ver = f["veredicto"]
    return slug, f["nombre"], chips, _limpio(ver)


def _datos_versus(url):
    import hostings
    m = re.match(r"^(?:/en)?/versus/([^/]+)-vs-([^/]+)/$", url)
    if not m:
        return None
    def nom(slug):
        f = next((f for f in hostings.FICHAS.values() if f["url"] == slug), None)
        return (slug, f["nombre"]) if f else (slug, slug.title())
    return nom(m.group(1)), nom(m.group(2))


def _etiqueta(url, lang):
    partes = [p for p in url.strip("/").split("/") if p and p != "en"]
    if not partes:
        return "Calculadora de RAM" if lang == "es" else "RAM calculator"
    tabla = {"hosting": ("Comparador", "Comparison"), "ofertas": ("Ofertas", "Deals"), "deals": ("Ofertas", "Deals"),
             "plantillas": ("Plantillas", "Templates"), "templates": ("Plantillas", "Templates"),
             "mi-server": ("Mi servidor", "My server"), "my-server": ("Mi servidor", "My server"),
             "minecraft": ("Minecraft", "Minecraft"), "precios": ("Precios", "Prices"),
             "como-lo-compruebo": ("Método", "Method")}
    return tabla.get(partes[0], ("MontaTuServer", "MontaTuServer"))[0 if lang == "es" else 1]


def poner(html, url, comprobado):
    """Genera la tarjeta de esta página y deja su URL en og:image."""
    lang = "en" if url.startswith("/en/") or url == "/en" else "es"
    os.makedirs(CARPETA, exist_ok=True)
    slug = _slug(url)
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S) or re.search(r"<title>(.*?)</title>", html, re.S)
    titulo = _limpio(m.group(1)) if m else "MontaTuServer"
    titulo = re.sub(r"\s*[|·]\s*MontaTuServer.*$", "", titulo)
    desc = _limpio((re.search(r'<meta name="description" content="([^"]*)"', html) or [None, ""])[1])

    f = _datos_ficha(url, lang)
    v = _datos_versus(url) if not f else None
    clave = repr((url, titulo, desc, f, v, comprobado))
    huella = hashlib.md5(clave.encode("utf-8")).hexdigest()
    jpg = os.path.join(CARPETA, slug + ".jpg")
    sidecar = os.path.join(CARPETA, slug + ".txt")
    if not (os.path.exists(jpg) and os.path.exists(sidecar) and io.open(sidecar).read() == huella):
        if f:
            img = ficha(f[0], f[1], f[2], f[3], lang, comprobado)
        elif v:
            img = versus(v[0], v[1], lang, comprobado, titulo)
        else:
            img = generica(_etiqueta(url, lang), titulo, desc, lang, comprobado)
        img.save(jpg, "JPEG", quality=84, optimize=True, progressive=True)
        io.open(sidecar, "w").write(huella)

    nuevo = '<meta property="og:image" content="%s/og/%s.jpg">' % (DOMINIO, slug)
    if re.search(r'<meta property="og:image" content="[^"]*">', html):
        html = re.sub(r'<meta property="og:image" content="[^"]*">', nuevo, html, count=1)
    else:
        html = html.replace("</title>", "</title>\n" + nuevo, 1)
    if 'name="twitter:card"' not in html:
        html = html.replace(nuevo, nuevo + '\n<meta name="twitter:card" content="summary_large_image">', 1)
    if 'property="og:image:width"' not in html:
        html = html.replace(nuevo, nuevo + '\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">', 1)
    return html
