# -*- coding: utf-8 -*-
"""
Pasada automática de revisar_precios.py (la programa la tarea de Windows
"montatuserver precios", los lunes a las 10:00).

Guarda el informe completo en _revisiones/<fecha>.txt y, SOLO si hay precios
sospechosos, deja un aviso en el escritorio (montatuserver PRECIOS.txt) para
que no pase desapercibido. Si todo está bien, no molesta.
"""
import datetime, io, os, re, subprocess, sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
CARPETA = os.path.join(RAIZ, "_revisiones")
ESCRITORIO = os.path.join(os.environ.get("USERPROFILE", ""), "Desktop")


def main():
    os.makedirs(CARPETA, exist_ok=True)
    hoy = datetime.date.today().isoformat()
    r = subprocess.run([sys.executable, os.path.join(RAIZ, "revisar_precios.py")],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    salida = re.sub(r"\x1b\[[0-9;]*m", "", r.stdout + ("\n" + r.stderr if r.stderr else ""))
    io.open(os.path.join(CARPETA, hoy + ".txt"), "w", encoding="utf-8").write(salida)

    m = re.search(r"(\d+) parecen correctos · (\d+) sospechosos · (\d+) sin poder comprobar", salida)
    sospechosos = int(m.group(2)) if m else -1
    aviso = os.path.join(ESCRITORIO, "montatuserver PRECIOS.txt")
    if sospechosos != 0:
        cabecera = ("REVISIÓN DE PRECIOS DE montatuserver.com (%s)\n"
                    "%s\n\nHay que mirar estos y, si han cambiado, editarlos en hosts.js, poner la fecha en\n"
                    "\"comprobado\" y publicar (python subir.py).\n\n" % (hoy, m.group(0) if m else "el revisor no terminó bien"))
        trozo = salida[salida.find("HAY QUE MIRAR ESTOS"):] if "HAY QUE MIRAR ESTOS" in salida else salida[-3000:]
        io.open(aviso, "w", encoding="utf-8").write(cabecera + trozo)
    elif os.path.exists(aviso):
        os.remove(aviso)
    print(salida[-400:])


if __name__ == "__main__":
    main()
