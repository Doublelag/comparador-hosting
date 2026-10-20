# -*- coding: utf-8 -*-
"""
Las páginas que responden a lo que la gente escribe en Google antes de
alquilar un servidor:

  /minecraft/hosting-barato/             "hosting minecraft barato"
  /minecraft/hosting-gratis/             "servidor minecraft gratis"
  /minecraft/cuanto-cuesta-un-servidor/  "cuánto cuesta un servidor de minecraft"

Los números salen de hosts.js al construir, igual que en el comparador: una
página de "los más baratos" con precios escritos a mano miente a los tres
meses. Lo importa build.py (seo.TODAS).
"""
import html as _html

import hostings
from paginas import pagina, DOMINIO

eur = hostings.eur


def _precios():
    d = hostings.datos()
    c = d["cambioUsdEur"]
    filas = []
    for hid, f in hostings.FICHAS.items():
        h = next(x for x in d["hosts"] if x["id"] == hid)
        pr = h["precios"]["minecraft"]
        p = {gb: hostings.precio_para(h, "minecraft", gb, c)[0] for gb in (2, 4, 8, 16)}
        ent = pr.get("entrada") or {}
        filas.append(dict(id=hid, nombre=f["nombre"], url=f["url"], p=p, pais=f["pais"],
                          entrada=ent.get("pct") if not ent.get("permanente") else None,
                          modelo=pr["modelo"]))
    return filas, d["comprobado"]


def _fila_tabla(r, cols):
    celdas = "".join(
        ('<td class="price">%s</td>' % eur(r["p"][gb])) if r["p"][gb] is not None else '<td class="nd">no llega</td>'
        for gb in cols)
    return ('<tr><td><a href="/hosting/%s/"><img class="h-logo" src="/logos/%s.png" alt="" width="18" height="18" loading="lazy">%s</a>'
            '<small>%s</small></td>%s<td><a class="cta-mini" href="/hosting/%s/">Ver ficha</a></td></tr>'
            % (r["url"], r["url"], r["nombre"], r["pais"], celdas, r["url"]))


def _tabla(filas, cols):
    cab = "".join("<th>%d GB</th>" % gb for gb in cols)
    return ('<div class="table-wrap"><table class="tabla-maestra"><thead><tr><th>Hosting</th>%s<th></th></tr></thead>'
            '<tbody>\n%s\n</tbody></table></div>' % (cab, "\n".join(_fila_tabla(r, cols) for r in filas)))


def _faq_schema(preguntas):
    import json
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
                       "mainEntity": [{"@type": "Question", "name": q,
                                       "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in preguntas]},
                      ensure_ascii=False)


def _faq_html(preguntas):
    return "\n".join('<details class="faq"><summary>%s</summary><p>%s</p></details>' % (q, a) for q, a in preguntas)


# ----------------------------------------------------------------- barato
def hosting_barato():
    filas, comprobado = _precios()
    con4 = sorted([r for r in filas if r["p"][4] is not None and r["modelo"] != "plazas"],
                  key=lambda r: r["p"][4])
    top = con4[:6]
    b = top[0]
    caro = con4[-1]
    veces = caro["p"][4] / b["p"][4]
    preguntas = [
        ("¿Cuál es el hosting de Minecraft más barato?",
         "A fecha de %s, %s: %s al mes por 4 GB y %s por 8 GB, precio recurrente (no es una oferta del primer mes). "
         "Le siguen %s y %s." % (comprobado, b["nombre"], eur(b["p"][4]), eur(b["p"][8]), top[1]["nombre"], top[2]["nombre"])),
        ("¿Por cuánto se puede tener un servidor de Minecraft al mes?",
         "Para 2-5 amigos en vanilla bastan 2 GB, y eso cuesta entre %s y %s al mes en los hostings baratos. "
         "Para 10 jugadores con plugins, 4 GB: entre %s y %s." % (eur(b["p"][2]), eur(top[2]["p"][2]), eur(b["p"][4]), eur(top[2]["p"][4]))),
        ("¿El hosting barato es peor?",
         "No siempre. Lo que suele faltar en los baratos son copias de seguridad automáticas, soporte rápido y procesador bueno. "
         "Para un server de amigos da igual; para una comunidad de 30 personas, no."),
        ("¿Por qué algunos hostings anuncian precios más bajos que los de aquí?",
         "Porque anuncian el precio del primer mes con descuento. Aquí sale el precio que pagas el mes 2, que es el que vas a pagar el resto del año."),
    ]
    cuerpo = """  <article class="wrap articulo">
    <nav class="miga" aria-label="Dónde estás"><a href="/">Inicio</a> › <a href="/hosting/">Hostings</a> › Hosting barato</nav>
    <span class="sec-eyebrow">Minecraft · precios recurrentes, no de bienvenida</span>
    <h1>Hosting de Minecraft <em>barato</em>: los %(n)d que menos cobran</h1>
    <p class="sub art-sub">Ordenados por lo que cuestan 4 GB <strong>el segundo mes</strong>, que es el precio de verdad.
      Entre el más barato y el más caro de la tabla hay <strong>%(veces).0f veces</strong> de diferencia por el mismo servidor.</p>

    <p class="veredicto-top" data-tit="En una frase">Hoy el más barato es <a href="/hosting/%(burl)s/">%(bnombre)s</a>:
      <strong>%(b4)s al mes por 4 GB</strong> (%(b8)s por 8 GB). Si solo sois cuatro o cinco en vanilla, con 2 GB a %(b2)s te sobra.</p>

    <h2 id="tabla">Los %(n)d más baratos por 4 GB</h2>
%(tabla)s
    <p class="art-meta">Precios con IVA y en euros (los que cobran en dólares, al cambio del día de la comprobación: %(comprobado)s).
      "No llega" quiere decir que ese hosting no vende ese tamaño.</p>

    <h2 id="trampas">Lo barato que sale caro</h2>
    <ul class="lista-no">
      <li><strong>El descuento del primer mes.</strong> %(con_entrada)d de los %(total)d hostings de esta web anuncian un precio que solo vale la primera factura.
        Hostinger, por ejemplo, pide dos años por adelantado para dar su precio de escaparate.</li>
      <li><strong>Cobrar por plazas.</strong> Realms y alguno más no te dicen cuánta RAM te dan. Parecen baratos hasta que metes un modpack y no tira.</li>
      <li><strong>Sin copias de seguridad.</strong> Las gamas "budget" suelen quitarlas. Un rollback después de un griefeo vale más que los 2 € que ahorras.</li>
      <li><strong>Procesador viejo.</strong> Minecraft usa un solo núcleo. En un hosting con Xeon de 2015, 8 GB van peor que 4 GB en un Ryzen actual.</li>
    </ul>

    <h2 id="cuanto">¿Cuántos GB necesitas de verdad?</h2>
    <p>Pagar 16 GB para cuatro amigos es tirar el dinero, y meter 20 personas con plugins en 2 GB es un server que se cae cada tarde.
      Dime cuántos sois y qué lleváis y te lo digo en diez segundos, con el precio en cada hosting.</p>
    <p><a class="cta" href="/">Calcular mi servidor →</a> <a class="cta-ghost" href="/hosting/">Ver los %(total)d hostings</a></p>

    <div class="art-cierre">
    <h2 id="faq">Dudas frecuentes</h2>
%(faq)s
    </div>
  </article>
""" % dict(n=len(top), veces=veces, burl=b["url"], bnombre=b["nombre"], b4=eur(b["p"][4]), b8=eur(b["p"][8]), b2=eur(b["p"][2]),
           tabla=_tabla(top, (2, 4, 8)), comprobado=comprobado,
           con_entrada=sum(1 for r in filas if r["entrada"]), total=len(filas), faq=_faq_html(preguntas))
    extra = '<script type="application/ld+json">%s</script>' % _faq_schema(preguntas)
    return pagina("es", "/minecraft/hosting-barato/",
                  "Hosting de Minecraft barato: los %d que menos cobran (precio real 2026)" % len(top),
                  "Los hostings de Minecraft más baratos ordenados por lo que cuestan de verdad el segundo mes, no el precio de bienvenida. "
                  "Desde %s al mes por 4 GB. Comprobado a mano." % eur(b["p"][4]),
                  cuerpo, extra)


# ----------------------------------------------------------------- gratis
def hosting_gratis():
    filas, comprobado = _precios()
    con4 = sorted([r for r in filas if r["p"][4] is not None and r["modelo"] != "plazas"], key=lambda r: r["p"][4])
    b = con4[0]
    preguntas = [
        ("¿Se puede tener un servidor de Minecraft gratis 24/7?",
         "Gratis y 24 horas encendido, con IP fija y sin colas, no. Lo gratis se apaga cuando no hay nadie (Aternos, Minehut) o es una prueba de días. "
         "Lo más cerca que hay es el plan gratis de 2 GB de Chunkly, que está siempre encendido pero es vanilla y para unos 3 jugadores."),
        ("¿Aternos es seguro?",
         "Sí, lleva desde 2013 y no pide tarjeta. Lo que tiene es cola para arrancar y que se apaga a los pocos minutos sin jugadores. Para probar con amigos sirve; para una comunidad, no."),
        ("¿Cuánto cuesta pasar de gratis a pagar?",
         "A fecha de %s, el servidor pagado más barato de la tabla son %s al mes por 2 GB (%s) y %s por 4 GB. Menos que una pizza." % (comprobado, eur(b["p"][2]), b["nombre"], eur(b["p"][4]))),
        ("¿Puedo montarlo gratis en mi PC?",
         "Sí: el servidor de Mojang es gratis. El problema es que tu PC tiene que estar encendido mientras jueguen, tienes que abrir el puerto 25565 en el router (o usar un túnel como playit.gg) y tu conexión de casa hace de servidor."),
    ]
    cuerpo = """  <article class="wrap articulo">
    <nav class="miga" aria-label="Dónde estás"><a href="/">Inicio</a> › <a href="/hosting/">Hostings</a> › Servidor gratis</nav>
    <span class="sec-eyebrow">Minecraft · sin tarjeta</span>
    <h1>Servidor de Minecraft <em>gratis</em>: lo que hay de verdad</h1>
    <p class="sub art-sub">Hay cuatro formas de tener un server sin pagar. Todas tienen un pero, y aquí está cada uno sin adornos.
      Al final te digo a partir de cuándo compensa pagar, con el precio real.</p>

    <p class="veredicto-top" data-tit="En una frase">Para probar con tres o cuatro amigos, <strong>Aternos</strong> o el <strong>plan gratis de Chunkly</strong>.
      Para jugar en serio, el servidor pagado más barato son <strong>%(b2)s al mes</strong> (2 GB) y se acaban las colas y los apagones.</p>

    <h2 id="opciones">Las cuatro opciones gratis</h2>
    <div class="pros-contras">
      <div>
        <h3>1. Aternos (y Minehut)</h3>
        <ul class="lista-si">
          <li>Gratis de verdad, sin tarjeta, con plugins y mods.</li>
          <li>Aternos lleva desde 2013: no va a desaparecer mañana.</li>
        </ul>
        <ul class="lista-no">
          <li>Cola para arrancar cuando hay mucha gente (de minutos a mucho más).</li>
          <li>Se apaga solo a los pocos minutos sin jugadores. Las granjas no corren mientras no estáis.</li>
          <li>Poca RAM y procesador compartido: con un modpack va a tirones.</li>
        </ul>
      </div>
      <div>
        <h3>2. El plan gratis de un hosting de pago</h3>
        <ul class="lista-si">
          <li><a href="/hosting/chunkly/">Chunkly</a> tiene un plan Campfire gratis: 2 GB, vanilla, siempre encendido, sin tarjeta.</li>
          <li>Mismo panel que el de pago: si luego subes, no cambias de sitio.</li>
        </ul>
        <ul class="lista-no">
          <li>Solo vanilla (sin plugins ni mods) y para unos 3 jugadores.</li>
          <li>Es nuevo: pocas opiniones todavía.</li>
        </ul>
      </div>
      <div>
        <h3>3. Pruebas gratis de unos días</h3>
        <ul class="lista-si">
          <li><a href="/hosting/godlike/">Godlike</a> te da un día sin tarjeta; <a href="/hosting/nodecraft/">Nodecraft</a>, 24 horas (pide verificar el teléfono).</li>
          <li>Sirven para ver si el panel te gusta antes de pagar.</li>
        </ul>
        <ul class="lista-no">
          <li>Son eso, pruebas: a los días hay que pagar o se borra.</li>
        </ul>
      </div>
      <div>
        <h3>4. En tu propio PC</h3>
        <ul class="lista-si">
          <li>El servidor de Mojang es gratis y tienes toda la RAM de tu PC.</li>
          <li>Con un túnel tipo playit.gg no hace falta tocar el router.</li>
        </ul>
        <ul class="lista-no">
          <li>Tu PC tiene que estar encendido mientras jueguen, y jugar y servir a la vez en el mismo PC se nota.</li>
          <li>Tu conexión de casa es el server: a los de fuera les llega con tu subida, que suele ser la mitad que la bajada.</li>
        </ul>
      </div>
    </div>

    <h2 id="cuando">Cuándo deja de compensar lo gratis</h2>
    <p>En el momento en que queréis que el server siga vivo cuando no hay nadie (granjas, redstone, que la gente entre a su hora) o sois más de cinco.
      Ahí lo gratis os va a hacer perder más tardes de las que vale la cuota, porque la cuota es esta:</p>
%(tabla)s
    <p class="art-meta">Precio recurrente, con IVA, comprobado el %(comprobado)s. Los cuatro más baratos de los <a href="/hosting/">%(total)d que comparo</a>.</p>
    <p><a class="cta" href="/">Calcular cuántos GB necesito →</a> <a class="cta-ghost" href="/minecraft/hosting-barato/">Ver los más baratos</a></p>

    <div class="art-cierre">
    <h2 id="faq">Dudas frecuentes</h2>
%(faq)s
    </div>
  </article>
""" % dict(b2=eur(b["p"][2]), tabla=_tabla(con4[:4], (2, 4, 8)), comprobado=comprobado, total=len(filas), faq=_faq_html(preguntas))
    extra = '<script type="application/ld+json">%s</script>' % _faq_schema(preguntas)
    return pagina("es", "/minecraft/hosting-gratis/",
                  "Servidor de Minecraft gratis: las 4 opciones reales y cuándo compensa pagar",
                  "Aternos, planes gratis de hostings, pruebas de días y tu propio PC: qué da cada uno y qué pierdes. "
                  "Y el precio real desde el que compensa pagar (%s al mes)." % eur(b["p"][2]),
                  cuerpo, extra)


# ----------------------------------------------------------------- cuanto cuesta
def cuanto_cuesta():
    filas, comprobado = _precios()
    # Realms cobra lo mismo de 1 a 16 GB porque no vende RAM: fuera de las horquillas
    con_gb = [r for r in filas if r["modelo"] != "plazas" and r["id"] != "realms"]
    def rango(gb, n=4):
        xs = sorted(r["p"][gb] for r in con_gb if r["p"][gb] is not None)
        return eur(xs[0]), eur(xs[min(n, len(xs)) - 1]), eur(xs[-1])
    r2, r4, r8, r16 = rango(2), rango(4), rango(8), rango(16)
    realms = next((r for r in filas if r["id"] == "realms"), None)
    por8 = sorted([r for r in con_gb if r["p"][8] is not None], key=lambda r: r["p"][8])
    preguntas = [
        ("¿Cuánto cuesta un servidor de Minecraft al mes?",
         "Depende de los GB. A fecha de %s: 2 GB para 2-5 amigos, de %s a %s; 4 GB para unos 10, de %s a %s; 8 GB para 20 con plugins, de %s a %s; "
         "16 GB para un modpack grande, de %s a %s. El primer número es el hosting más barato de la tabla y el segundo, el cuarto más barato." %
         (comprobado, r2[0], r2[1], r4[0], r4[1], r8[0], r8[1], r16[0], r16[1])),
        ("¿Cuánto cuesta Minecraft Realms?",
         ("%s al mes (es un precio en dólares, al cambio). Hasta 10 jugadores a la vez, sin mods ni plugins." % eur(realms["p"][4])) if realms else
         "Unos 7 € al mes, hasta 10 jugadores, sin mods ni plugins."),
        ("¿Cuánto cuesta un servidor de Minecraft al año?",
         "Multiplica por 12 y súmale el descuento de bienvenida solo una vez: %s al año por 4 GB en el más barato, hasta más de %s en los caros. "
         "Si el hosting anuncia −25 %% el primer mes, al año te ahorra un 2 %%." % (eur(float(r4[0].replace(",", ".").replace(" €", "")) * 12), eur(float(r4[2].replace(",", ".").replace(" €", "")) * 12))),
        ("¿Es más barato montarlo en casa?",
         "En dinero sí (el software es gratis), pero el PC tiene que estar encendido mientras jueguen y sirves con tu subida de casa. "
         "Un server de 4 GB cuesta menos de lo que gasta en luz un PC encendido todo el día."),
    ]
    cuerpo = """  <article class="wrap articulo">
    <nav class="miga" aria-label="Dónde estás"><a href="/">Inicio</a> › <a href="/hosting/">Hostings</a> › Cuánto cuesta</nav>
    <span class="sec-eyebrow">Minecraft · precios de %(comprobado)s</span>
    <h1>¿Cuánto cuesta un <em>servidor de Minecraft</em>?</h1>
    <p class="sub art-sub">De %(min)s a %(max)s al mes por el mismo tamaño, según dónde lo alquiles. Aquí va lo que cuesta de verdad
      según cuántos seáis, con el precio del segundo mes (el que pagas el resto del año) y no el de bienvenida.</p>

    <h2 id="segun">Según cuántos seáis</h2>
    <div class="ganadores">
      <div class="ganador"><span class="ganador-tag">2-5 amigos · vanilla</span><span class="ganador-nom">2 GB</span><span class="ganador-dato">de <b>%(r2a)s</b> a %(r2b)s al mes</span></div>
      <div class="ganador"><span class="ganador-tag">Hasta 10 · plugins</span><span class="ganador-nom">4 GB</span><span class="ganador-dato">de <b>%(r4a)s</b> a %(r4b)s al mes</span></div>
      <div class="ganador"><span class="ganador-tag">15-25 · plugins o mods ligeros</span><span class="ganador-nom">8 GB</span><span class="ganador-dato">de <b>%(r8a)s</b> a %(r8b)s al mes</span></div>
      <div class="ganador"><span class="ganador-tag">Modpack grande · 10+</span><span class="ganador-nom">16 GB</span><span class="ganador-dato">de <b>%(r16a)s</b> a %(r16b)s al mes</span></div>
    </div>
    <p class="art-meta">El primer número es el hosting más barato de la tabla; el segundo, el cuarto más barato. Hay hostings que cobran el doble por lo mismo: están en la tabla de abajo.</p>

    <h2 id="porque">Por qué el mismo servidor cuesta el doble en otro sitio</h2>
    <ul class="lista-si">
      <li><strong>El procesador.</strong> Minecraft va con un solo núcleo: un Ryzen 9950X3D vale más que un Xeon de hace diez años, y se nota en los tirones, no en la RAM.</li>
      <li><strong>Las copias de seguridad.</strong> Automáticas y diarias cuestan dinero al hosting; los baratos las quitan o las cobran aparte.</li>
      <li><strong>El soporte.</strong> Que te contesten en diez minutos un sábado por la noche lo pagas en la cuota.</li>
      <li><strong>Dónde está el servidor.</strong> Un centro de datos en Europa para gente de España son 20-40 ms; uno en Estados Unidos, 120.</li>
    </ul>

    <h2 id="tabla">Lo que cobra cada uno por 8 GB</h2>
%(tabla)s
    <p class="art-meta">Con IVA, en euros, precio recurrente. Los %(total)d hostings con <a href="/hosting/">ficha en esta web</a>, comprobados a mano el %(comprobado)s.</p>

    <h2 id="tu-caso">Tu caso exacto</h2>
    <p>Las horquillas de arriba son orientativas. Dime cuántos sois, qué versión y si lleváis mods, y te digo los GB y lo que cuesta en cada hosting.</p>
    <p><a class="cta" href="/">Calcular mi servidor →</a> <a class="cta-ghost" href="/minecraft/hosting-barato/">Los más baratos</a></p>

    <div class="art-cierre">
    <h2 id="faq">Dudas frecuentes</h2>
%(faq)s
    </div>
  </article>
""" % dict(comprobado=comprobado, min=r4[0], max=r4[2], r2a=r2[0], r2b=r2[1], r4a=r4[0], r4b=r4[1], r8a=r8[0], r8b=r8[1], r16a=r16[0], r16b=r16[1],
           tabla=_tabla(por8, (4, 8, 16)), total=len(filas), faq=_faq_html(preguntas))
    extra = '<script type="application/ld+json">%s</script>' % _faq_schema(preguntas)
    return pagina("es", "/minecraft/cuanto-cuesta-un-servidor/",
                  "¿Cuánto cuesta un servidor de Minecraft? Precios reales por tamaño (2026)",
                  "Lo que cuesta un servidor de Minecraft al mes según cuántos seáis: desde %s por 2 GB hasta %s por 16 GB. "
                  "Precio recurrente de %d hostings comprobado a mano, no el de bienvenida." % (r2[0], r16[1], len(filas)),
                  cuerpo, extra)


TODAS = [
    ("/minecraft/hosting-barato/", hosting_barato),
    ("/minecraft/hosting-gratis/", hosting_gratis),
    ("/minecraft/cuanto-cuesta-un-servidor/", cuanto_cuesta),
]
