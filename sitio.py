# -*- coding: utf-8 -*-
"""
Datos del sitio que salen en varias páginas y que cambian poco: el servidor
de Minecraft (ChorizoSMP), las redes y los datos legales del titular.

Un solo sitio para tocarlos. Si cambia la IP del server, se cambia aquí y
build.py la pone en todas partes.
"""

# ---------------------------------------------------------------- ChorizoSMP
SERVER = dict(
    nombre="ChorizoSMP",
    ip="chorizosmp.datho.st",     # Java y Bedrock usan la misma dirección
    puerto_bedrock=17095,
    version="26.2",
)

# ---------------------------------------------------------------- redes
YOUTUBE = "https://www.youtube.com/@Doublelag"

# ---------------------------------------------------------------- legal
# La ley española (LSSI, art. 10) obliga a que la web diga quién es el
# titular: nombre, NIF y una forma de contacto. Rellénalo antes de publicar.
# Mientras falte algo, publicar.py avisa en rojo.
TITULAR = "Doublelag"  # nombre público del titular (o razón social)
NIF = ""              # NIF/DNI del titular
EMAIL = "doublelag.manager@gmail.com"   # correo de contacto para la web
DOMICILIO = ""        # opcional si hay correo de contacto, pero recomendable


def faltan_datos_legales():
    # El NIF no cuenta como bloqueante: la LSSI lo pide, pero es decisión
    # del titular publicarlo. Sin TITULAR ni EMAIL sí que no se puede publicar.
    return [k for k, v in (("TITULAR", TITULAR), ("EMAIL", EMAIL)) if not v]
