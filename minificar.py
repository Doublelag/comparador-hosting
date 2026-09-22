# -*- coding: utf-8 -*-
"""
Minificador conservador para lo que se publica en `dist/`.

Por qué existe: el código de este proyecto lleva muchos comentarios a propósito
—explican por qué está hecho así, que es medio valor del repositorio— pero esos
comentarios no le sirven de nada a quien entra en la web, y se pagan dos veces:
en los datos del visitante y en el ancho de banda de Netlify.

Lo que hace es a propósito poco agresivo: NO renombra variables, NO reordena
nada y NO toca la lógica. Solo quita comentarios y espacio sobrante, que es de
donde sale casi toda la diferencia una vez que el servidor comprime.

Regla de oro: si una línea puede estar dentro de un texto (un template literal,
una cadena), se deja tal cual. Más vale minificar menos que publicar una web
rota.

Lo usa publicar.py. Los archivos del proyecto no se tocan nunca.
"""

import re


def css(texto):
    """Quita comentarios y espacio sobrante de una hoja de estilos."""
    t = re.sub(r"/\*.*?\*/", "", texto, flags=re.S)      # comentarios
    t = re.sub(r"[ \t]+", " ", t)                        # espacios repetidos
    t = re.sub(r"\s*([{};:,>])\s*", r"\1", t)            # alrededor de símbolos
    t = re.sub(r";}", "}", t)                            # punto y coma final
    t = re.sub(r"\n\s*\n+", "\n", t)
    return t.strip() + "\n"


def js(texto):
    """Quita los comentarios que ocupan una línea entera y las líneas vacías.

    Solo se borra una línea si TODA ella es comentario. Un `// algo` al final de
    una línea con código se queda: distinguirlo de un `//` dentro de una cadena
    pide un analizador de verdad, y no compensa el riesgo.
    """
    fuera = []
    en_bloque = False
    for linea in texto.split("\n"):
        pelada = linea.strip()
        if en_bloque:
            if "*/" in pelada:
                en_bloque = False
                resto = pelada.split("*/", 1)[1].strip()
                if resto:
                    fuera.append(resto)
            continue
        if pelada.startswith("/*"):
            if "*/" not in pelada:
                en_bloque = True
                continue
            resto = pelada.split("*/", 1)[1].strip()
            if resto:
                fuera.append(resto)
            continue
        if pelada.startswith("//"):
            continue
        if not pelada:
            continue
        fuera.append(linea.rstrip())
    return "\n".join(fuera) + "\n"


def html(texto):
    """Quita comentarios HTML y la sangría, respetando lo que va dentro de
    <script>, <style>, <pre> y <textarea>."""
    partes = re.split(r"(<(?:script|style|pre|textarea)\b.*?</(?:script|style|pre|textarea)>)",
                      texto, flags=re.S | re.I)
    fuera = []
    for i, parte in enumerate(partes):
        if i % 2:                       # bloque protegido: tal cual
            fuera.append(parte)
            continue
        # Los comentarios se van menos los condicionales de Internet Explorer
        parte = re.sub(r"<!--(?!\[if).*?-->", "", parte, flags=re.S)
        parte = re.sub(r"\n[ \t]+", "\n", parte)
        parte = re.sub(r"\n{2,}", "\n", parte)
        fuera.append(parte)
    return "".join(fuera)


def para(nombre, texto):
    """Elige el minificador por la extensión. Si no hay, devuelve el original."""
    if nombre.endswith(".css"):
        return css(texto)
    if nombre.endswith(".js"):
        return js(texto)
    if nombre.endswith(".html"):
        return html(texto)
    return texto
