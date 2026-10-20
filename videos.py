# -*- coding: utf-8 -*-
"""
Los últimos vídeos del canal en la portada, leídos del RSS público de YouTube
al construir. Sin API ni clave: el feed es público y no pide nada.

Se eligen primero los que hablan de servers/hosting (los que tienen que ver
con esta web); si no hay bastantes, se completa con los últimos. Si YouTube
no responde al construir, se dejan los de la pasada anterior: la portada
nunca se queda sin bloque.
"""
import io, os, re, html, urllib.request

CANAL = "UC-Iu4z_V6hhMDtZexbq6crg"        # @Doublelag (el principal; UCmaY1... es el canal en ingles)
CUANTOS = 4
CLAVES = re.compile(r"server|servidor|hosting|smp|chorizo|host", re.I)
# Largos del canal que hablan de servers. El feed solo trae los 15 ultimos y
# casi todo son shorts o directos, asi que estos van fijos y el feed solo
# aporta algun largo nuevo de servers si lo hay.
# Los tres de hosting estan en OCULTO en el canal: no salen en el feed ni en
# busquedas, pero se reproducen por enlace. Por eso van a mano.
FIJOS = [
    dict(id="lx9pmNpSu0M", titulo="El mejor hosting para Minecraft 2026", fecha="2026-03-06"),
    dict(id="olfBXRwdrUs", titulo="Por qué dejé Aternos después de 2 años (y qué uso ahora)", fecha="2025-12-24"),
    dict(id="E9wr6wsF7hQ", titulo="He creado un servidor de Minecraft donde eres un MAGO", fecha="2026-10-10"),
    dict(id="CxCG7rQO0FE", titulo="NUEVO SERVIDOR DE MODS GRATIS NO PREMIUM 24/7", fecha="2025-12-18"),
]


def _clave(t):
    return re.sub(r"[^a-z0-9]", "", t.lower())


def leer():
    url = "https://www.youtube.com/feeds/videos.xml?channel_id=" + CANAL
    try:
        xml = urllib.request.urlopen(url, timeout=15).read().decode("utf-8")
    except Exception:
        return None
    vids = []
    for e in re.findall(r"<entry>(.*?)</entry>", xml, re.S):
        vid = re.search(r"<yt:videoId>([^<]+)", e)
        tit = re.search(r"<title>([^<]+)", e)
        fecha = re.search(r"<published>([^<]+)", e)
        if not (vid and tit and fecha):
            continue
        vids.append(dict(id=vid.group(1), titulo=html.unescape(tit.group(1)).strip(),
                         fecha=fecha.group(1)[:10]))
    # Del feed solo los largos de servers que no sean directos ni repetidos.
    # Los directos y sus VOD empiezan por emoji; los largos, por letra.
    con = [v for v in vids if CLAVES.search(v["titulo"]) and v["titulo"][:1].isalnum()]
    out, vistos = [], set()
    for v in FIJOS[:2] + con + FIJOS[2:]:
        k = _clave(v["titulo"])[:30]
        if v["id"] in vistos or k in vistos:
            continue
        vistos.add(v["id"]); vistos.add(k)
        out.append(v)
    return out[:CUANTOS]


def _fecha(iso, lang):
    a, m, d = iso.split("-")
    meses = (["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
             if lang == "es" else
             ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    return "%d %s %s" % (int(d), meses[int(m) - 1], a)


def tarjetas(vids, lang):
    out = []
    for v in vids:
        out.append(
            '<a class="video" href="https://www.youtube.com/watch?v=%(id)s" rel="noopener">'
            '<span class="video-mini"><img src="https://i.ytimg.com/vi/%(id)s/hqdefault.jpg" '
            'alt="" width="480" height="360" loading="lazy"></span>'
            '<span class="video-tit">%(tit)s</span><span class="video-fecha">%(fecha)s</span></a>'
            % dict(id=v["id"], tit=html.escape(v["titulo"]), fecha=_fecha(v["fecha"], lang)))
    return "\n".join(out)


def rellenar(raiz):
    vids = leer()
    if not vids:
        print("  videos: YouTube no responde, se dejan los de la pasada anterior")
        return
    for fichero, lang in (("index.html", "es"), ("index.en.html", "en")):
        ruta = os.path.join(raiz, fichero)
        s = io.open(ruta, encoding="utf-8").read()
        assert "<!--videos-->" in s, "falta el marcador videos en " + fichero
        s = re.sub(r"(<!--videos-->).*?(<!--/videos-->)",
                   lambda m: m.group(1) + "\n" + tarjetas(vids, lang) + "\n" + m.group(2), s, flags=re.S)
        io.open(ruta, "w", encoding="utf-8", newline="\n").write(s)
    print("  videos: %d del canal en la portada" % len(vids))
