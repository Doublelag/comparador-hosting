# -*- coding: utf-8 -*-
"""
Historial de precios: qué cobraba cada hosting la última vez que se miró.

Por qué: en idealo o en los comparadores de vuelos, el gráfico de "cómo ha ido
el precio" es de lo más consultado, porque responde a la pregunta de verdad —
¿esto está caro ahora o es lo normal? En hosting no lo enseña nadie, entre
otras cosas porque casi todos los comparadores del sector son de una empresa
de hosting y no les interesa que veas la subida.

Cómo funciona: `build.py` llama a `guardar()` en cada compilación. Si algún
precio ha cambiado desde la última foto, se apunta una nueva con la fecha.
Si no ha cambiado nada, no se apunta nada — así el archivo guarda cambios, no
compilaciones.

El archivo `historico.json` NO se publica: es material de trabajo. Lo que sale
en la web es la frase de `cambio()`, del tipo "en septiembre costaba 12,99 €".

Uso suelto:
    python historico.py          # enseña lo que ha cambiado y desde cuándo
"""

import io, json, os, datetime

RAIZ = os.path.dirname(os.path.abspath(__file__))
ARCHIVO = os.path.join(RAIZ, "historico.json")

MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


def _leer():
    if not os.path.exists(ARCHIVO):
        return []
    return json.loads(io.open(ARCHIVO, encoding="utf-8").read())


def _foto(d):
    """Los precios de hoy, en un diccionario plano y comparable."""
    fuera = {}
    for h in d["hosts"]:
        pr = (h.get("precios") or {}).get("minecraft")
        if not pr:
            continue
        if pr["modelo"] == "porGB":
            fuera[h["id"]] = {"modelo": "porGB", "porGB": pr["porGB"]}
        elif pr["modelo"] in ("tabla", "slots"):
            fuera[h["id"]] = {"modelo": pr["modelo"],
                              "tiers": [[a, b] for a, b in pr["tiers"]]}
        elif pr["modelo"] == "plano":
            fuera[h["id"]] = {"modelo": "plano", "precio": pr["precio"],
                              "ram": pr.get("ram")}

    return fuera


def guardar(d):
    """Apunta una foto nueva si algo ha cambiado. Devuelve cuántos cambiaron."""
    historia = _leer()
    hoy = _foto(d)
    if historia and historia[-1]["precios"] == hoy:
        return 0
    cambiados = 0
    if historia:
        antes = historia[-1]["precios"]
        cambiados = sum(1 for k, v in hoy.items() if antes.get(k) != v)
    historia.append({"fecha": datetime.date.today().isoformat(), "precios": hoy})
    io.open(ARCHIVO, "w", encoding="utf-8", newline="\n").write(
        json.dumps(historia, ensure_ascii=False, indent=1) + "\n")
    return cambiados


def _precio8(p, cambio):
    """Lo que costaban 8 GB en aquella foto, en euros. None si no se puede saber."""
    if not p:
        return None
    if p["modelo"] == "porGB":
        return p["porGB"] * 8
    if p["modelo"] == "tabla":
        for gb, precio in p["tiers"]:
            if 8 <= gb:
                return precio
        return None
    if p["modelo"] == "plano":
        return p["precio"] if (not p.get("ram") or p["ram"] >= 8) else None
    return None            # por plazas: aquí no hay precio de 8 GB


def cambio(host_id, moneda, cambio_usd):
    """Frase del tipo «en agosto costaba 12,99 €», o "" si no hay con qué comparar.

    Compara el precio de 8 GB de hoy con la foto ANTERIOR a la última en la que
    ese hosting cambió. Si nunca ha cambiado desde que se guarda historial, no
    se dice nada: "lleva igual desde ayer" no es información.
    """
    historia = _leer()
    if len(historia) < 2:
        return ""
    aEur = (lambda v: v * cambio_usd) if moneda == "USD" else (lambda v: v)
    ahora = historia[-1]["precios"].get(host_id)
    for foto in reversed(historia[:-1]):
        antes = foto["precios"].get(host_id)
        if antes and antes != ahora:
            a, b = _precio8(antes, cambio_usd), _precio8(ahora, cambio_usd)
            if a is None or b is None or abs(a - b) < 0.01:
                return ""
            a, b = aEur(a), aEur(b)
            _, m, dia = foto["fecha"].split("-")
            cuando = "el %d de %s" % (int(dia), MESES[int(m) - 1])
            verbo = "ha subido" if b > a else "ha bajado"
            return ("Su plan de 8 GB %s: %s costaba %s y ahora son %s."
                    % (verbo, cuando,
                       ("%.2f" % a).replace(".", ",") + " €",
                       ("%.2f" % b).replace(".", ",") + " €"))
    return ""


if __name__ == "__main__":
    historia = _leer()
    if not historia:
        print("Todavía no hay historial. Ejecuta build.py y se crea solo.")
    else:
        print("%d fotos guardadas, de %s a %s"
              % (len(historia), historia[0]["fecha"], historia[-1]["fecha"]))
        for f in historia:
            print("  %s · %d hostings" % (f["fecha"], len(f["precios"])))
