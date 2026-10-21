# -*- coding: utf-8 -*-
"""
Lo técnico de cada hosting que la gente de mods pregunta antes de pagar:
procesador, disco y copias de seguridad. Sale en la ficha, debajo de los
datos básicos.

Leído de la web de cada uno el 21-oct-2026. "No publican" quiere decir
exactamente eso: que en su web no lo dicen, no que no lo tengan. "Sin
comprobar" es que su web no me dejó entrar ese día (bloqueo 403). No se
rellena a ojo: un dato inventado aquí vale menos que una casilla vacía.

Clave = id de la ficha en hostings.FICHAS.
"""

TECNICO = {
    "dathost":             dict(cpu="Ryzen 9 7950X o EPYC", disco="60 GB NVMe (0,30 €/GB extra)", copias="Diarias, incluidas"),
    "pebble-budget":       dict(cpu="Ryzen 7 5700X (Budget) / 9900X (Premium)", disco="NVMe sin límite (uso justo)", copias="Solo en Premium (diarias + por hora)"),
    "bisect":              dict(cpu="No publican", disco="NVMe sin límite", copias="Diarias, 3-7 días; más huecos de pago"),
    "shockbyte":           dict(cpu="Sin comprobar", disco="NVMe", copias="Sin comprobar"),
    "apex":                dict(cpu="Sin comprobar", disco="NVMe RAID 1", copias="Sin comprobar"),
    "hostinger":           dict(cpu="AMD EPYC, 1 a 8 vCPU", disco="50 a 400 GB NVMe", copias="Automáticas + instantánea manual"),
    "sparked":             dict(cpu="Ryzen 9 7900 / 9900X, 2 a 3,5 vCPU", disco="100 GB NVMe RAID 1", copias="De pago: 3 huecos por 1 $ al mes"),
    "nodecraft":           dict(cpu="Ryzen 9 o EPYC (sin modelo)", disco="SSD, sin GB publicados", copias="Incluidas"),
    "chunkly":             dict(cpu="No publican", disco="NVMe en la UE, sin GB publicados", copias="Incluidas"),
    "holyhosting":         dict(cpu="No publican («última generación»)", disco="NVMe sin límite", copias="No publican"),
    "vultam-standard":     dict(cpu="Sin comprobar", disco="Sin comprobar", copias="Sin comprobar"),
    "wisehosting":         dict(cpu="Ryzen 9 7950X o EPYC 4564P, 3,5 a 5 vCores", disco="25 a 50 GB NVMe", copias="1 o 2 huecos incluidos"),
    "nexohost":            dict(cpu="Ryzen 7 3700X", disco="100 GB SSD NVMe por GB de RAM", copias="No publican"),
    "theminecrafthosting": dict(cpu="No publican", disco="SSD sin límite", copias="No publican"),
    "godlike":             dict(cpu="Ryzen, hasta 9950X3D", disco="SSD, sin GB publicados", copias="Hasta 3 al día, gratis"),
    "gportal":             dict(cpu="No publican", disco="NVMe", copias="Manuales desde el panel"),
    "scalacube":           dict(cpu="No publican", disco="No publican", copias="Automáticas, sin detalle"),
    "ggservers":           dict(cpu="3,2-4 GHz; Ryzen o i7 en Premium", disco="SSD RAID 1; NVMe en Premium", copias="No publican"),
    "kinetic":             dict(cpu="Hasta Ryzen 9 9950X, 6 a 8 hilos", disco="60 GB NVMe, ampliable gratis", copias="5 huecos incluidos"),
    "realms":              dict(cpu="—", disco="—", copias="Las guarda Mojang"),
    "akliz":               dict(cpu="No publican", disco="NVMe sin límite", copias="2 al día, incluidas"),
    "hosthavoc":           dict(cpu="Hilos dedicados, sin modelo", disco="NVMe, sin GB publicados", copias="Diarias, incluidas"),
    "serverminer":         dict(cpu="No publican", disco="No publican", copias="No publican"),
    "bloom":               dict(cpu="Hasta Ryzen 9 5950X (2 núcleos compartidos); 9950X en Performance+", disco="60 a 600 GB NVMe", copias="Externas, incluidas"),
    "ouiheberg":           dict(cpu="2 a 4 vCPU a 3,7 GHz (Ryzen)", disco="20 a 100 GB NVMe", copias="2 a 5 huecos incluidos"),
}

TECNICO_EN = {
    "dathost":             dict(cpu="Ryzen 9 7950X or EPYC", disco="60 GB NVMe (€0.30/GB extra)", copias="Daily, included"),
    "pebble-budget":       dict(cpu="Ryzen 7 5700X (Budget) / 9900X (Premium)", disco="Unmetered NVMe (fair use)", copias="Premium only (daily + hourly)"),
    "bisect":              dict(cpu="Not published", disco="Unlimited NVMe", copias="Daily, 3-7 days; extra slots paid"),
    "shockbyte":           dict(cpu="Not checked", disco="NVMe", copias="Not checked"),
    "apex":                dict(cpu="Not checked", disco="NVMe RAID 1", copias="Not checked"),
    "hostinger":           dict(cpu="AMD EPYC, 1 to 8 vCPU", disco="50 to 400 GB NVMe", copias="Automatic + manual snapshot"),
    "sparked":             dict(cpu="Ryzen 9 7900 / 9900X, 2 to 3.5 vCPU", disco="100 GB NVMe RAID 1", copias="Paid: 3 slots for $1/mo"),
    "nodecraft":           dict(cpu="Ryzen 9 or EPYC (no model)", disco="SSD, no GB published", copias="Included"),
    "chunkly":             dict(cpu="Not published", disco="EU NVMe, no GB published", copias="Included"),
    "holyhosting":         dict(cpu="Not published (“latest-gen”)", disco="Unlimited NVMe", copias="Not published"),
    "vultam-standard":     dict(cpu="Not checked", disco="Not checked", copias="Not checked"),
    "wisehosting":         dict(cpu="Ryzen 9 7950X or EPYC 4564P, 3.5 to 5 vCores", disco="25 to 50 GB NVMe", copias="1 or 2 slots included"),
    "nexohost":            dict(cpu="Ryzen 7 3700X", disco="100 GB NVMe SSD per GB of RAM", copias="Not published"),
    "theminecrafthosting": dict(cpu="Not published", disco="Unlimited SSD", copias="Not published"),
    "godlike":             dict(cpu="Ryzen, up to 9950X3D", disco="SSD, no GB published", copias="Up to 3 a day, free"),
    "gportal":             dict(cpu="Not published", disco="NVMe", copias="Manual from the panel"),
    "scalacube":           dict(cpu="Not published", disco="Not published", copias="Automatic, no detail"),
    "ggservers":           dict(cpu="3.2-4 GHz; Ryzen or i7 on Premium", disco="SSD RAID 1; NVMe on Premium", copias="Not published"),
    "kinetic":             dict(cpu="Up to Ryzen 9 9950X, 6 to 8 threads", disco="60 GB NVMe, free expansion", copias="5 slots included"),
    "realms":              dict(cpu="—", disco="—", copias="Kept by Mojang"),
    "akliz":               dict(cpu="Not published", disco="Unmetered NVMe", copias="Twice daily, included"),
    "hosthavoc":           dict(cpu="Dedicated threads, no model", disco="NVMe, no GB published", copias="Daily, included"),
    "serverminer":         dict(cpu="Not published", disco="Not published", copias="Not published"),
    "bloom":               dict(cpu="Up to Ryzen 9 5950X (2 shared cores); 9950X on Performance+", disco="60 to 600 GB NVMe", copias="Off-site, included"),
    "ouiheberg":           dict(cpu="2 to 4 vCPU at 3.7 GHz (Ryzen)", disco="20 to 100 GB NVMe", copias="2 to 5 slots included"),
}


def html(hid, lang="es"):
    t = (TECNICO_EN if lang == "en" else TECNICO).get(hid)
    if not t:
        return ""
    et = ("Procesador", "Disco", "Copias de seguridad") if lang == "es" else ("CPU", "Disk", "Backups")
    return ('<div class="ficha-datos ficha-tecnico">'
            '<div><span>%s</span><b>%s</b></div><div><span>%s</span><b>%s</b></div><div><span>%s</span><b>%s</b></div>'
            '</div>' % (et[0], t["cpu"], et[1], t["disco"], et[2], t["copias"]))
