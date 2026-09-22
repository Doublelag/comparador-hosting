# -*- coding: utf-8 -*-
"""
Migas de pan en datos estructurados (BreadcrumbList).

Google las usa para enseñar «montatuserver.com › Hostings › Shockbyte» en vez
de la URL pelada, y eso sube el porcentaje de clics sin tocar la posición.
Las migas visuales ya estaban en las páginas; esto es la versión que lee él.

Lo importan hostings.py, comparativas.py, guias.py y duelos.py.
"""

import json

DOMINIO = "https://montatuserver.com"


def schema(items):
    """items = [(nombre, ruta)]. La última va sin ruta: es la página actual."""
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            dict({"@type": "ListItem", "position": i + 1, "name": n},
                 **({"item": DOMINIO + u} if u else {}))
            for i, (n, u) in enumerate(items)
        ],
    }, ensure_ascii=False, indent=2)
