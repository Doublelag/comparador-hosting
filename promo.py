# -*- coding: utf-8 -*-
"""
La tira de promo que va dentro de los artículos (comparativas y guías).

Hasta el 11-sep-2026 esto era "DatHost deja Valheim a 1 €", escrito para un
solo hosting. Ahora lee la promo del PARTNER configurado en hosts.js
(`partner.promo`). Sin partner activo, o sin promo, o con la promo caducada,
no pinta nada — que es lo que tiene que pasar.

Formato de la promo en hosts.js:

    "promo": {
      "juegos": ["minecraft"],          # la web es solo de Minecraft
      "titulo": "Primer mes a 1 €",
      "texto":  "Por el lanzamiento de la 1.0 …",
      "letra":  "Solo el primer mes; después son X €/mes.",   # obligatoria
      "hasta":  "2026-09-17"
    }

`letra` es obligatoria a propósito: una promo sin su letra pequeña al lado es
justo lo que esta web le critica al resto del sector.

Se genera en HTML estático (Google la ve) con un guardián de caducidad en
JavaScript: si nadie regenera el sitio después de la fecha, se borra sola.

Lo importan comparativas.py y guias.py.
"""

import datetime

import partner

MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


def banner(juego_id, cid="BANNER"):
    """HTML de la tira, o "" si no toca."""
    if not partner.activo():
        return ""
    promo = partner.config().get("promo")
    if not promo or juego_id not in promo.get("juegos", []):
        return ""
    if not promo.get("letra"):
        return ""                                   # sin letra pequeña, no sale
    if datetime.date.today().isoformat() > promo["hasta"]:
        return ""                                   # caducada: ni se genera
    enlace = partner.enlace(juego_id, cid)
    if not enlace:
        return ""                                   # el partner no ofrece el juego

    _, m, dia = promo["hasta"].split("-")
    fecha = "%d de %s" % (int(dia), MESES[int(m) - 1])

    return """
    <aside class="promo-tira" data-hasta="%s">
      <span class="pt-tag">⏳ Solo hasta el %s</span>
      <p class="pt-txt"><strong>%s.</strong> %s</p>
      <a class="cta" href="%s" rel="sponsored nofollow noopener" target="_blank">Ver la oferta en %s</a>
      <small class="pt-pie">%s %s</small>
    </aside>
    <script>
    /* Si el sitio no se regenera despues de la fecha, la tira se quita sola. */
    (function(){var t=document.currentScript.previousElementSibling;
     if(t&&new Date().toISOString().slice(0,10)>t.dataset.hasta)t.remove();})();
    </script>
""" % (promo["hasta"], fecha, promo["titulo"], promo.get("texto", ""),
       enlace, partner.nombre(), promo["letra"], partner.aviso_boton())
