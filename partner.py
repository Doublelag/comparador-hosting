# -*- coding: utf-8 -*-
"""
El partner de afiliación — todo lo que depende de con quién hay acuerdo.

Hasta el 11-sep-2026 la web estaba cableada a DatHost en catorce ficheros: sus
precios aparte, su enlace, su promo, «gano comisión si contratas DatHost» en
cada pie de página. Cambiar de partner habría sido tocar los catorce.

Ahora hay una sola fuente: el bloque `partner` de hosts.js. Este módulo es lo
único que lo lee en Python, y todo lo que diga «afiliado», «comisión» o lleve
un botón de contratar sale de aquí. Si mañana cambias de partner, cambias ese
bloque y ejecutas build.py. Ningún texto más.

Con `activo: false` (el estado actual) la web es un comparador sin ningún
enlace de afiliado, ningún hosting destacado, y los avisos dicen la verdad:
que no hay acuerdo con nadie.

Lo importan todos los generadores de páginas.
"""

import io, json, os

RAIZ = os.path.dirname(os.path.abspath(__file__))


def _datos():
    s = io.open(os.path.join(RAIZ, "hosts.js"), encoding="utf-8").read()
    crudo = s[s.index("window.DATOS =") + len("window.DATOS ="):].strip().rstrip(";").strip()
    return json.loads(crudo)


def config():
    return _datos().get("partner") or {"activo": False}


def activo():
    p = config()
    return bool(p.get("activo") and p.get("hostId") and p.get("enlace"))


def host_id():
    return config().get("hostId") if activo() else None


def nombre():
    """Nombre del hosting partner, tal como está en hosts[]."""
    if not activo():
        return None
    hid = host_id()
    for h in _datos()["hosts"]:
        if h["id"] == hid:
            return h["nombre"]
    return hid


def es_partner(hid):
    return activo() and hid == host_id()


def ofrece(juego):
    """¿El partner tiene precio comprobado para este juego?"""
    if not activo():
        return False
    for h in _datos()["hosts"]:
        if h["id"] == host_id():
            return juego in (h.get("precios") or {})
    return False


def enlace(juego=None, cid=None):
    """URL de afiliado para ese juego, o None si no hay partner o no lo ofrece.

    Nunca devuelve un enlace a un juego que el partner no vende: mandar a alguien
    a contratar algo que no existe sería engañarle.
    """
    if not activo():
        return None
    if juego is not None and not ofrece(juego):
        return None
    p = config()
    url = p["enlace"]
    if "{juego}" in url:
        slug = (p.get("slugs") or {}).get(juego, juego or "")
        url = url.replace("{juego}", slug)
    canal = cid or p.get("canal") or "WEB"
    return url + ("&" if "?" in url else "?") + "cid=" + canal


def boton(juego, cid, texto=None, clase="cta"):
    """Botón de contratar, o cadena vacía si no toca enseñarlo."""
    url = enlace(juego, cid)
    if not url:
        return ""
    texto = texto or "Ir a %s" % nombre()
    return ('<a class="%s" href="%s" rel="sponsored nofollow noopener" '
            'target="_blank">%s</a>' % (clase, url, texto))


def razones():
    """Las tres líneas de «por qué este hosting» que van junto al botón."""
    if not activo():
        return ""
    lista = config().get("razones") or []
    if not lista:
        return ""
    return '<ul class="pf-razones">%s</ul>' % "".join("<li>%s</li>" % r for r in lista)


def divulgacion():
    """El aviso del pie de página. Sin partner no hay nada que avisar, y repetir
    en cada página que no gano comisión suena a estar justificándose: eso se dice
    una vez, en «Qué gano yo» de la portada. La caja vacía la esconde el CSS."""
    if not activo():
        return ""
    return ("<strong>Aviso de afiliación:</strong> gano comisión si contratas %s por "
            "los enlaces de esta web, sin coste extra para ti. Con el resto de "
            "hostings no tengo ningún acuerdo. Eso no cambia sus precios ni su "
            "posición en las tablas: el más barato sale primero, sea quien sea."
            % nombre())


def divulgacion_en():
    """El aviso del pie en inglés. Sin partner, nada."""
    if not activo():
        return ""
    return ("<strong>Affiliate disclosure:</strong> I earn a commission if you buy %s "
            "through the links on this site, at no extra cost to you. I have no deal with "
            "any other host. That doesn't change their prices or their place in the "
            "tables: the cheapest comes first, whoever it is." % nombre())


def aviso_boton():
    """La línea pequeña que va debajo de un botón de afiliado."""
    if not activo():
        return ""
    return ("Enlace de afiliado: si contratas, me llevo una comisión y a ti no te "
            "cuesta ni un céntimo más.")


def aviso_boton_en():
    if not activo():
        return ""
    return ("Affiliate link: if you buy, I earn a commission and it costs you "
            "nothing extra.")


def que_gano_yo_en():
    if not activo():
        return ("Right now, nothing: I have no affiliate deal with any host on this site. "
                "If I ever do, I'll say so here and in every page footer, and that host "
                "will sit in the tables where its <strong>price puts it, not higher</strong>.")
    return ("A commission if you buy %s through my links, at no extra cost to you. "
            "That's why the calculator <strong>tells you the cheapest first even when it "
            "isn't them</strong>, and in the tables they sit where their price puts them."
            % nombre())


def caja_independencia():
    """La caja de arriba del índice de hostings."""
    if not activo():
        return ("<strong>No tengo acuerdo de afiliación con ninguno de estos.</strong> "
                "Están aquí con sus precios reales y con sus pegas, y ninguno ha pagado "
                "por salir. Los precios se comprueban a mano en la web de cada uno, con "
                "la fecha puesta.")
    return ("<strong>Solo tengo acuerdo de afiliado con uno de estos: %s.</strong> Del "
            "resto no gano nada, y aun así están aquí con sus precios reales y sus "
            "cosas buenas. En la tabla sale en el puesto que le toca por precio."
            % nombre())


def linea_bienvenida():
    """La línea de la bienvenida de la portada. Decirlo arriba y no escondido
    en el pie es la diferencia entre avisar y cumplir el expediente."""
    if not activo():
        return ("Ahora mismo no tengo acuerdo de afiliación con ningún hosting de "
                "esta web.")
    p = config()
    cupon = (" con el código <strong>%s</strong>" % p["codigo"]) if p.get("codigo") else ""
    return ("Con <strong>%s</strong> sí tengo acuerdo, y es por esto: he usado el alcance "
            "de mis redes para conseguiros un trato de verdad bueno: "
            "un <strong>−25 %% todos los meses</strong>%s, el único que no caduca: los otros nueve descuentos de esta web valen solo para la primera factura. Sí, me llevo una comisión si contratas por mi enlace, y a ti "
            "no te cuesta ni un céntimo más. Aun así sale en las tablas en el puesto que "
            "le toca por precio, y la calculadora te dice el más barato aunque no sea él."
            % (nombre(), cupon))


def linea_bienvenida_en():
    if not activo():
        return "I currently have no affiliate deal with any host on this site."
    p = config()
    cupon = (" with the code <strong>%s</strong>" % p["codigo"]) if p.get("codigo") else ""
    return ("With <strong>%s</strong> I do have a deal, and this is why: I used the reach "
            "of my channels to get you a genuinely good one: "
            "<strong>−25%% off every month</strong>%s, the only one that never expires: the other nine discounts on this site are first-invoice only. Yes, I earn a commission if you buy through my link, and it "
            "costs you nothing extra. It still sits in the tables where its price puts it, "
            "and the calculator tells you the cheapest even when that isn't them."
            % (nombre(), cupon))


def caja_independencia_en():
    """La misma caja del indice de hostings, en ingles."""
    if not activo():
        return ("<strong>I have no affiliate deal with any of these.</strong> They're here "
                "with their real prices and their downsides, and none of them paid to be "
                "listed. Prices are checked by hand on each host's site, with the date shown.")
    return ("<strong>I only have an affiliate deal with one of these: %s.</strong> I earn "
            "nothing from the rest, and they're still here with their real prices and their "
            "good points. In the table it sits where its price puts it." % nombre())


def que_gano_yo():
    """El párrafo de la tarjeta «Qué gano yo» de la portada."""
    if not activo():
        return ("Ahora mismo, nada: no tengo acuerdo de afiliación con ningún hosting "
                "de esta web. Si algún día lo tengo, lo diré aquí y en el pie de cada "
                "página, y ese hosting saldrá en las tablas en el puesto que le toque "
                "<strong>por precio, no más arriba</strong>.")
    return ("Comisión si contratas %s por mis enlaces, sin coste extra para ti. Por eso "
            "la calculadora <strong>te dice primero el más barato aunque no sea él</strong>, "
            "y en las tablas sale en el puesto que le toca por precio." % nombre())


# El banner oficial que manda el partner. Va DEBAJO de la tabla y etiquetado
# como publicidad a proposito: un comparador que esconde sus anuncios deja de
# ser un comparador. El descuento se explica al lado ("el primer mes") porque
# la imagen la disena el partner y ahi solo pone "Save 75%".
BANNER = {
    "archivo": "/godlike-banner.webp",
    "ancho": 1674,
    "alto": 160,
    "alt": u"Godlike.host, hosting para modpacks de Minecraft",
}


def _banner(rotulo, pie, alt, cta):
    """El bloque del banner, o cadena vacia si no hay partner.

    El cid=BANNER es para poder separar en el panel de afiliado las ventas que
    vienen de aqui de las que vienen de los botones de las fichas.
    """
    if not activo():
        return ""
    url = enlace(cid="BANNER")
    if not url:
        return ""
    return (
        '<figure class="pub">\n'
        '  <figcaption class="pub-et">%s</figcaption>\n'
        '  <a href="%s" rel="sponsored nofollow noopener" target="_blank">\n'
        '    <img src="%s" alt="%s" width="%d" height="%d"\n'
        '         loading="lazy" decoding="async">\n'
        '    <span class="pub-cta">%s</span>\n'
        '  </a>\n'
        '  <p class="pub-pie">%s</p>\n'
        '</figure>\n'
        % (rotulo, url, BANNER["archivo"], alt,
           BANNER["ancho"], BANNER["alto"], cta, pie))


def banner():
    p = config()
    cupon = (u" con el c\u00f3digo <strong>%s</strong>" % p["codigo"]) if p.get("codigo") else ""
    return _banner(
        u"Publicidad \u00b7 enlace de afiliado",
        u"<strong>\u221225 %% todos los meses</strong>%s, no solo el primero. El \u221275 %% que "
        u"anuncia el cartel era su oferta de entrada antigua y ya no est\u00e1. En la tabla de "
        u"arriba sale en el puesto que le toca por su tarifa normal."
        % cupon,
        BANNER["alt"],
        u"Ver Godlike.host")


def banner_en():
    p = config()
    cupon = (u" with the code <strong>%s</strong>" % p["codigo"]) if p.get("codigo") else ""
    return _banner(
        u"Advertisement \u00b7 affiliate link",
        u"<strong>\u221225%% every month</strong>%s, not just the first. The \u221275%% on the "
        u"banner was their old entry offer and it is gone. In the table above it sits where "
        u"its list price puts it."
        % cupon,
        u"Godlike.host, Minecraft modpack hosting",
        u"Go to Godlike.host")
