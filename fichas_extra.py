# -*- coding: utf-8 -*-
"""
Fichas de los hostings añadidos el 8-sep-2026.

Van aquí y no en hostings.py por el mismo motivo que comparativas_extra.py:
el diccionario original ya era largo y mezclar diez fichas más lo volvía
imposible de leer. `hostings.py` las junta con las suyas al importarlas.

Mismo formato que FICHAS: resumen, bueno, malo, veredicto. Y la misma regla —
lo bueno se dice aunque sea competencia, y lo malo se dice aunque sea nuestro.

Lo importa hostings.py.
"""

FICHAS_EXTRA = {

  "chunkly": dict(
    desde_ano="2026", ubicaciones="Europa",
    rasgos=['0,85 € el GB con IVA', 'Plan gratis de 2 GB', 'Cobro mensual en euros', 'Modpacks solo en Kingdom'],
    url="chunkly", nombre="Chunkly", pais="Europa (GateX Ltd)",
    resumen=("0,85 € el giga con IVA, cobro mensual en euros y un plan gratis para "
             "probar el panel. Los modpacks van en su gama Kingdom, a 1,90 € el giga."),
    bueno=[
      "<strong>De los más baratos de la tabla</strong>: 0,85 € por GB en la gama Village, de 2 a 12 GB. Un 4 GB son 3,40 € al mes.",
      "Precio <strong>con IVA y en euros</strong>: lo que ves es lo que pagas, sin sorpresa al pasar por caja ni cambio de dólar.",
      "Plan <strong>Campfire gratis</strong> (2 GB, vanilla, unos 3 jugadores) para probar el panel sin tarjeta.",
      "Mes a mes y baja cuando quieras. NVMe, protección DDoS, Java y Bedrock.",
    ],
    malo=[
      "Marca nueva: poca trayectoria y pocas opiniones todavía. La empresa de detrás dice llevar 25 años en hosting, pero Chunkly como tal acaba de empezar.",
      "La gama barata (Village) solo admite Paper, Purpur y Vanilla. Para Forge, Fabric o un modpack hay que ir a Kingdom, que cuesta más del doble: 1,90 € el giga.",
      "Tope de 12 GB en Village y 16 en Kingdom. No publican qué procesador llevan.",
      "Soporte en inglés.",
    ],
    veredicto=("Por precio es de los dos o tres más baratos de la tabla y, al cobrar en euros con IVA, "
               "el precio que ves es el que pagas. Es nuevo y con poca trayectoria: pruébalo con el plan "
               "gratis antes de meter a tu comunidad. Para modpacks, Kingdom cuesta más del doble y ahí ya hay rivales."),
  ),

  "holyhosting": dict(
    desde_ano="2019", ubicaciones="—",
    rasgos=['Muy usado por creadores', 'El −25 % es solo el primer mes'],
    url="holyhosting", nombre="HolyHosting", pais="España",
    resumen="El que usan muchos creadores españoles. 1,25 $ el GB de tarifa real.",
    bueno=[
      "Lo usan más de 200 creadores, varios de ellos españoles muy grandes. Eso "
      "significa que sus servidores aguantan eventos con mucha gente entrando de golpe.",
      "Te dan subdominio .holy.gg sin puerto, que para repartir la IP entre tu "
      "comunidad es bastante más cómodo que una IP con números.",
      "Web, panel y soporte en español, que en este sector no es lo normal.",
    ],
    malo=[
      "Anuncian <strong>0,95 $/GB</strong> en portada, pero ese es el precio del "
      "<strong>primer mes</strong> con su −25 %. La tarifa real es 1,25 $/GB.",
      "El descuento lleva cuenta atrás en pantalla, que es una forma de meterte prisa "
      "para que no eches la cuenta del mes dos.",
    ],
    veredicto="Si montas eventos o llevas comunidad, el rodaje que tienen con creadores "
              "es un argumento de peso y se lo reconozco. Pero haz números con "
              "1,25 $/GB, que es lo que vas a pagar a partir del segundo mes.",
  ),

  # La clave debe ser un id real de hosts.js. La ficha habla de las dos gamas,
  # igual que la de PebbleHost.
  "vultam-standard": dict(
    desde_ano="2016", ubicaciones="4",
    rasgos=['Prueba gratis', 'Copias diarias', 'Tres gamas', 'El Standard es de 2015'],
    url="vultam", nombre="Vultam", pais="Estonia",
    resumen="Tres gamas: Standard a 1,75 $/GB, Advanced a 2,40 $ y Performance a 3,50 $.",
    bueno=[
      "Ofrecen <strong>prueba gratis sin poner tarjeta</strong>, y eso lo hace muy poca "
      "gente. Pruebas tú y decides tú, sin fiarte de nadie.",
      "Copias de seguridad diarias incluidas en las dos gamas, no solo en la cara.",
      "Nodos en Francia y Alemania, que desde España es lo que te interesa.",
    ],
    malo=[
      "La gama Standard monta un <strong>Intel i7-6700K, un procesador de 2015</strong>. "
      "Para vanilla con cuatro amigos vale; para un modpack se va a notar.",
      "La gama Advanced sube a 2,40 $/GB, y a ese precio hay competencia con hardware "
      "más nuevo.",
      "La gama Performance, con Ryzen 9 5950X y copias cada 12 horas, se va a "
      "3,50 $/GB: ahí ya no compite con casi nadie.",
    ],
    veredicto="La prueba gratis es la razón para mirarlos: te dejan comprobarlo por tu "
              "cuenta antes de soltar un euro. Del Standard no esperes milagros con "
              "mods, que ese procesador ya tiene sus años.",
  ),

  "wisehosting": dict(
    desde_ano="2021", ubicaciones="—",
    rasgos=['Solo hacen Minecraft', '50 % pagando el año', 'Devolución en 7 días'],
    url="wisehosting", nombre="WiseHosting", pais="Estonia",
    resumen="Solo hacen Minecraft. 3 $/GB al mes, o 1,50 $ pagando el año entero.",
    bueno=[
      "Se dedican <strong>solo a Minecraft</strong>, y eso se nota cuando escribes al "
      "soporte: quien contesta sabe lo que es un modpack.",
      "Siete días para pedir la devolución.",
      "Pagando el año se queda en 1,50 $/GB, que ya sí es competitivo.",
    ],
    malo=[
      "A precio mensual son <strong>3 $/GB</strong>: <strong>el triple</strong> que los "
      "más baratos de esta tabla. 8 GB te salen a unos 24 $ al mes.",
      "Para que salga a cuenta hay que soltar los doce meses por adelantado, y eso es "
      "apostar antes de saber si el servicio te convence.",
      "Los planes vienen justos: el de 4 GB trae <strong>una sola copia de seguridad</strong> "
      "y 25 GB de disco.",
    ],
    veredicto="Pagando mes a mes es de lo más caro de la comparativa, y no hay nada en el "
              "plan que lo justifique. Solo tiene sentido si pagas el año entero, y aun "
              "así yo probaría antes otro de esta lista.",
  ),

  "nexohost": dict(
    desde_ano="2021", ubicaciones="—",
    rasgos=['Español', 'Desde 1 €/mes', 'Su tope son 9 GB'],
    url="nexohost", nombre="NexoHost", pais="España",
    resumen="Hosting español con planes de 1 a 9 GB, empezando en 1 € al mes.",
    bueno=[
      "Empresa española, con panel propio y soporte en español.",
      "Empieza en <strong>1 € al mes</strong>. Para montar algo y probar es casi nada.",
      "Ryzen 7 3700X y disco NVMe: hardware correcto para lo que cobran.",
    ],
    malo=[
      "Su plan más grande es de <strong>9 GB</strong>. Si vas a modpack pesado o "
      "comunidad grande, se te queda corto y hay que mudarse.",
      "No publican dónde tienen los centros de datos, así que no puedo decirte qué ping "
      "vas a tener desde España. Se lo he buscado y no está.",
    ],
    veredicto="Para un servidor pequeño de amigos, en español y barato, es una opción "
              "muy razonable. El día que necesites más de 9 GB se acabó el camino.",
  ),

  "theminecrafthosting": dict(
    desde_ano="2014", ubicaciones="4",
    rasgos=['Nodo en París', 'Cupón del −60 % todo el año'],
    url="theminecrafthosting", nombre="The Minecraft Hosting", pais="Estados Unidos",
    resumen="Cobra distinto según la ubicación. El nodo de París es el que importa aquí.",
    bueno=[
      "Puedes elegir nodo en <strong>París</strong>, de lo más cerca de España que vas "
      "a encontrar.",
      "Almacenamiento y plazas de jugador sin límite.",
    ],
    malo=[
      "Llevan un código <strong>BLACKFRIDAY del −60 % activo todo el año</strong> y lo "
      "llaman «lifetime». Si un descuento no se quita nunca, el precio de tarifa es "
      "decorativo — y tú no sabes a cuánto te van a renovar.",
      "A tarifa completa sus 16 GB son 35 $, de los más caros de la comparativa.",
    ],
    veredicto="Un Black Friday activo en septiembre me chirría. Si te interesan, "
              "pregúntales <strong>por escrito</strong> a cuánto renueva antes de "
              "pagar: la diferencia entre 35 $ y 14 $ no es un detalle.",
  ),
  "godlike": dict(
    desde_ano="2021", ubicaciones="10",
    rasgos=['Launcher que prepara el cliente',
            'Instalador de mods integrado', 'Prueba gratis de un día sin tarjeta',
            'Eliges gigas, plazas y días'],
    url="godlike", nombre="Godlike.host", pais="Rumanía",
    resumen=("El que menos cosas te obliga a saber: un launcher que le deja el "
             "Minecraft listo a tus amigos, mods en dos clics y un día gratis para "
             "probarlo sin tarjeta. No es barato por giga: pagas comodidad."),
    bueno=[
      "<strong>Su launcher te ahorra la peor tarde del año.</strong> Inicias sesión con "
      "tu cuenta de Godlike y desde ahí gestionas el servidor, pero lo gordo es el botón "
      "de preparar el cliente: te instala la versión y los mods que lleva el servidor. "
      "Eso mata el «instalaos todos lo mismo y la misma versión», que es donde se muere "
      "la mitad de los servidores con mods. No lo tiene ningún otro de esta tabla.",
      "<strong>El plan te lo montas tú</strong>: gigas (de 2 a 33), plazas (de 5 a 200) "
      "y <strong>días</strong> — 30, 90, 180 o 360. Casi nadie deja elegir la duración: "
      "si el modpack os va a durar tres meses, pagas tres meses y cierras.",
      "<strong>Hardware de lo mejor que hay</strong>: AMD Ryzen de última generación, "
      "hasta el 9950X3D, y discos NVMe. Minecraft tira de un solo núcleo, y ahí es "
      "donde se nota.",
      "<strong>Hasta tres copias de seguridad al día, gratis</strong>, y se restauran "
      "desde el panel. Justo lo que le falta a otros baratos.",
      "Te dejan <strong>un servidor de 2 GB gratis durante un día</strong> para probar el "
      "panel antes de pagar nada.",
      "El panel se rehízo en 2025: consola que filtra errores, reinicios y copias "
      "programadas, editor de archivos, toda la configuración de Minecraft en una "
      "pantalla sin SFTP, permisos por roles y un instalador de mods y plugins que "
      "comprueba versiones. Se maneja bien desde el móvil y también desde un bot de Discord.",
      "Para quien lleva comunidad: tienda para vender cosas dentro del juego en un "
      "clic, sistema de valoraciones para atraer jugadores y varios servidores enlazados.",
      "Subes o bajas de plan al momento y pagas solo la diferencia. Pagando por "
      "adelantado baja: −10 % a 90 días, −15 % a 180 y −20 % a 360.",
      "Protección DDoS por capas con Path.net, diez centros de datos (Europa "
      "incluida) y pago con casi cualquier método, cripto incluida.",
    ],
    malo=[
      "<strong>No es barato por giga y no lo disimulo</strong>: 3,25 € a tarifa y 2,44 € "
      "con el código, cuando el más barato de esta tabla está en 1,00 €. Aquí pagas la "
      "comodidad, no los gigas. Si sabes moverte por un panel y lo que quieres es "
      "gastar poco, hay opciones a menos de la mitad.",
      "<strong>El soporte no habla español.</strong> Te atienden en inglés, y ellos "
      "mismos dicen que tiran de traductor si les escribes en otro idioma. Funciona, "
      "pero contándolo: si se te cae el servidor un domingo, lo arreglas en inglés.",
      "Empresa joven, de 2021. En 2024 tuvieron una queja de reembolso que acabó en "
      "Reddit; la tienen explicada en su propia web, que ya dice algo.",
      "El servidor gratis es para trastear: una plaza y hay que renovarlo cada tres horas.",
    ],
    veredicto=("No es el más barato y no vengo a decirte que lo sea. Es el más fácil. "
               "Pagas más por giga, sí. A cambio te llevas el launcher que le prepara el "
               "juego a tus amigos, mods en dos clics, copias diarias, elegir los días que "
               "pagas y un día gratis para probarlo. De los 23 de esta tabla, no hay otro "
               "que te dé todo eso junto. Si tu tiempo vale algo, la cuenta cambia. "
               "Y si lo que quieres es gastar lo mínimo y no te asusta un panel a pelo, "
               "mira Kinetic o NexoHost, que están a menos de la mitad por giga."),
  ),

  "gportal": dict(
    desde_ano="2003", ubicaciones="11",
    rasgos=['Plazas ilimitadas', '250 modpacks de un clic', 'Su tope son 6 GB'],
    url="gportal", nombre="GPORTAL", pais="Alemania",
    resumen="Uno de los grandes de Europa. En Minecraft va de 2 a 6 GB, con plazas ilimitadas.",
    bueno=[
      "Plazas de jugador ilimitadas en todos sus planes: la gente que entre no te "
      "sube el precio.",
      "Más de 250 modpacks preinstalados de un clic, que para montar un RLCraft o un "
      "All the Mods sin pelearte con archivos se agradece.",
      "Llevan desde 2003 y tienen centros de datos por toda Europa, así que el ping "
      "desde España es de los buenos.",
      "Web, panel y soporte en español.",
    ],
    malo=[
      "<strong>Su tope son 6 GB.</strong> Si vas a modpack grande o comunidad, te "
      "quedas sin sitio y hay que mudarse.",
      "El <strong>−25 % es solo del primer periodo</strong>. Los 6 GB entran por "
      "11,25 € y renuevan a 15 €.",
      "Comparado por giga no sale bien: sus 4 GB son 11,80 €, casi el triple que "
      "PebbleHost por esa misma RAM.",
    ],
    veredicto="Si quieres un modpack montado en dos clics, plazas ilimitadas y buen "
              "ping desde España, cumple y es cómodo. Pero pagas esa comodidad: por "
              "giga está entre los caros, y con 6 GB de techo no es sitio para una "
              "comunidad que crezca.",
  ),

  "scalacube": dict(
    desde_ano="2015", ubicaciones="8",
    rasgos=['Plazas ilimitadas', 'Dominio y MySQL gratis', 'El −50 % es del primer mes'],
    url="scalacube", nombre="ScalaCube", pais="Estonia",
    resumen="Escalones de 768 MB a 64 GB, a unos 3 $ el giga, con plazas ilimitadas.",
    bueno=[
      "Llega hasta <strong>64 GB</strong>, que es más que casi todos: si montas una "
      "comunidad grande, no te quedas sin sitio.",
      "Plazas de jugador ilimitadas en todos los planes.",
      "Incluyen dominio y base de datos MySQL sin pagar aparte, cosa que muchos cobran.",
      "Soportan modpacks, plugins, BungeeCord y JAR propio.",
    ],
    malo=[
      "A 3 $ el giga están <strong>por encima de la media</strong> de esta tabla.",
      "El <strong>−50 % es solo del primer mes</strong>, y el precio de escaparate "
      "sale de ahí.",
      "Sus escalones son raros (768 MB, 1,5 GB, 4,5 GB): hay que mirar bien cuál "
      "cubre de verdad lo que necesitas.",
    ],
    veredicto="Si necesitas mucha RAM o plazas sin límite, tienen de lo más alto de la "
              "comparativa y eso no es fácil de encontrar. Para un servidor pequeño, "
              "por ese dinero hay opciones más baratas aquí mismo.",
  ),

  "ggservers": dict(
    desde_ano="2013", ubicaciones="10+",
    rasgos=['Java y Bedrock', 'Dos gamas', 'La Standard monta DDR4 2133'],
    url="ggservers", nombre="GGServers", pais="Canadá",
    resumen="Dos gamas clavadas a 3 $ y 6 $ el giga, con modpacks de un clic.",
    bueno=[
      "El precio es una regla de tres, sin sorpresas: 3 $ el giga en Standard y 6 $ "
      "en Premium.",
      "Java y Bedrock, modpacks y plugins de un clic, y acceso FTP y MySQL completo.",
      "Llevan desde 2013 y tienen soporte por chat las 24 horas.",
    ],
    malo=[
      "La gama Standard monta <strong>DDR4 a 2133 MHz y disco SSD normal</strong>: "
      "para un modpack grande se va a notar.",
      "La Premium, que sí lleva NVMe y procesador rápido, <strong>cuesta el doble</strong>: "
      "6 $ el giga, de los más caros de la tabla.",
      "Su cupón de bienvenida es <strong>solo de la primera factura</strong>.",
    ],
    veredicto="La Standard es correcta para vanilla o unos pocos plugins, y por ese "
              "precio tienes cosas mejores. La Premium está bien de hardware, pero a "
              "6 $ el giga hay que quererlos mucho.",
  ),

  "kinetic": dict(
    desde_ano="2018", ubicaciones="6",
    rasgos=['Menos de 1 $ el GB', 'Devolución en 7 días', 'Empieza en 4 GB'],
    url="kinetic", nombre="Kinetic Hosting", pais="Reino Unido",
    resumen="De los más baratos por giga: 8 GB por 7,99 $, con copias y cambio de juego.",
    bueno=[
      "<strong>Unos 0,99 $ el giga</strong>: pelea de tú a tú con PebbleHost Budget "
      "por el puesto de más barato, y aquí sí traen copias de seguridad.",
      "Cinco copias de seguridad incluidas y detección de caídas que te avisa.",
      "Puedes <strong>cambiar de juego cuando quieras</strong> sin pagar de nuevo.",
      "Siete días de devolución sin preguntas.",
      "Llegan hasta 124 GB, así que hay sitio para crecer.",
    ],
    malo=[
      "<strong>Su plan más pequeño son 4 GB.</strong> Si buscas algo de 1 o 2 GB para "
      "cuatro amigos, aquí no lo hay.",
      "No publican el modelo exacto de procesador en la página de precios: hay que "
      "mirarlo en su apartado de especificaciones.",
      "Marca menos conocida que las grandes, así que hay menos opiniones de fuera.",
    ],
    veredicto="Por precio es de lo mejor de toda la tabla, y a diferencia del Budget de "
              "PebbleHost aquí las copias vienen puestas. Si necesitas 4 GB o más, es "
              "de las primeras que miraría; por debajo de eso, ni existe.",
  ),

  "realms": dict(
    desde_ano="2013", ubicaciones="—",
    rasgos=['Oficial de Mojang', 'Sin mods ni plugins', 'Tope de 10 jugadores'],
    url="realms", nombre="Minecraft Realms", pais="Suecia",
    resumen="El oficial de Mojang. Sencillísimo, pero sin mods y con tope de jugadores.",
    bueno=[
      "Es de Mojang: se contrata desde el propio juego y no hay nada que configurar.",
      "No se rompe nunca al actualizar Minecraft, porque la actualización es suya.",
      "Guarda tres mundos y tus amigos pueden entrar aunque tú no estés conectado.",
    ],
    malo=[
      "<strong>No admite plugins ni mods.</strong> Ni Paper, ni Forge, ni Fabric.",
      "Tope de <strong>10 jugadores a la vez</strong>, y no se amplía pagando más.",
      "No se vende por RAM, así que si se te queda corto no hay forma de darle más.",
    ],
    veredicto="Si lo único que quieres es jugar con cuatro amigos sin complicarte la "
              "vida, es la opción más sencilla que hay y no le veo pega. En cuanto "
              "quieras un plugin, un mod o meter a quince personas, tienes que salir.",
  ),


  "akliz": dict(
    desde_ano="2006", ubicaciones="5 regiones",
    rasgos=['Soporte que te ayuda a mano', 'Copias dos veces al día', 'Devolución en 7 días'],
    url="akliz", nombre="Akliz", pais="Estados Unidos",
    resumen="Hosting gestionado a 5 $ el giga: pagas más para que te ayuden a montarlo.",
    bueno=[
      "Su punto fuerte es el soporte: están enfocados en ayudarte a configurar el server, "
      "no solo en darte un panel y ya.",
      "Copias de seguridad automáticas <strong>dos veces al día</strong> y reinicios "
      "automáticos en todos los planes.",
      "Jugadores ilimitados y varios servidores por plan (desde 4 GB puedes tener dos "
      "encendidos a la vez).",
      "Más de 600 modpacks de un clic y devolución completa en los primeros 7 días.",
      "Llevan en esto desde 2006.",
    ],
    malo=[
      "<strong>5 $ el giga</strong>: de lo más caro de la comparativa. 8 GB son 40 $ al mes.",
      "A veces enseñan un 20 % de rebaja sin explicar en qué condiciones.",
      "No publican el modelo de procesador en su página de precios.",
      "Su plan más grande estándar son 24 GB; más allá, hay que pedir presupuesto.",
    ],
    veredicto="Tiene sentido si nunca has montado un server y quieres que alguien te "
              "lleve de la mano. Si sabes lo que haces, por la mitad de dinero tienes el "
              "mismo giga en otros de esta lista.",
  ),

  "hosthavoc": dict(
    desde_ano="2013", ubicaciones="13",
    rasgos=['Centros en Londres, Ámsterdam y Fráncfort', 'Garantía de 72 h', 'NVMe en todos'],
    url="hosthavoc", nombre="Host Havoc", pais="Canadá",
    resumen="5 $ el giga con disco NVMe y 13 centros de datos, tres de ellos en Europa.",
    bueno=[
      "Tienen centro en <strong>Londres, Ámsterdam y Fráncfort</strong>: desde España "
      "el ping va a ser bueno.",
      "Disco NVMe en todos los planes y hardware propio (no alquilado).",
      "IP propia gratis a partir de 6 GB.",
      "Garantía de 72 horas en todos los pedidos nuevos.",
    ],
    malo=[
      "<strong>5 $ el giga</strong> a precio normal: caro para lo que hay en la tabla.",
      "El 25 % que anuncian es una <strong>promoción de temporada</strong> (código "
      "SUMMER), no el precio de siempre.",
      "Por debajo de 6 GB, la IP propia cuesta 4 $ más al mes.",
      "No publican el modelo de procesador en la página de Minecraft.",
    ],
    veredicto="Hosting serio y con buena presencia en Europa, pero a precio normal pagas "
              "el doble por giga que los más baratos de la tabla. Si pillas la "
              "promoción, se acerca a la media.",
  ),

  "serverminer": dict(
    desde_ano="2012", ubicaciones="—",
    rasgos=['Precios en euros', 'Tope de jugadores por plan', 'Descuento por pagar 3 o 6 meses'],
    url="serverminer", nombre="ServerMiner", pais="Reino Unido",
    resumen="Planes cerrados en euros, con tope de jugadores en cada uno.",
    bueno=[
      "Cobran <strong>en euros</strong>: lo que ves es lo que pagas, sin cambio de moneda.",
      "Un 10 % menos pagando 3 meses y un 15 % pagando 6.",
      "Tienen centros en Alemania y Finlandia.",
      "Sin permanencia: cancelas cuando quieras.",
      "Empresa británica registrada desde 2012.",
    ],
    malo=[
      "<strong>Cada plan tiene tope de jugadores</strong>: 15 en el pequeño, 100 en el "
      "grande. En casi toda la tabla son ilimitados.",
      "Unos 4,30 € el giga: de los caros.",
      "Su plan más grande son 10 GB: no vale para modpacks muy pesados.",
      "La IP propia y la ayuda con plugins o modpacks son extras de pago.",
    ],
    veredicto="Pagar en euros es cómodo, pero por ese dinero hay hostings con más RAM y "
              "sin tope de jugadores. Solo lo miraría si ya los conoces.",
  ),

  "bloom": dict(
    desde_ano="—", ubicaciones="6",
    rasgos=['Centro en Alemania', 'Hasta Ryzen 9 9950X', 'Copias montables desde el panel'],
    url="bloom", nombre="Bloom.host", pais="Estados Unidos",
    resumen="Tres gamas: Essentials barata y Performance y Performance+ con núcleos dedicados.",
    bueno=[
      "Tienen centro en <strong>Falkenstein (Alemania)</strong>: buen ping desde España.",
      "En Performance y Performance+ los <strong>núcleos son dedicados</strong>, no "
      "compartidos con otros clientes.",
      "La gama Performance+ monta <strong>Ryzen 9 9950X</strong> (7950X3D en Alemania), "
      "de lo más rápido que hay para Minecraft.",
      "Su sistema de copias deja abrir una copia como carpeta y recuperar un archivo "
      "suelto desde el panel.",
      "Con cada plan puedes crear más servidores sin pagar más (bots de Discord, webs, "
      "otros juegos).",
    ],
    malo=[
      "La gama Essentials empieza en 4 GB y usa <strong>núcleos compartidos</strong> con "
      "procesadores más viejos (Ryzen 9 3900X fuera de Alemania).",
      "Unos 2,75 $ el giga en Performance y 3,50 $ en Performance+: precio medio-alto.",
      "Su cupón de Performance+ es <strong>solo de la primera factura</strong>.",
      "En su web no he encontrado la política de devoluciones ni el año de fundación.",
    ],
    veredicto="Muy buen hardware y centro en Alemania. Performance+ es de lo mejor para "
              "un servidor exigente si puedes pagarlo; para un server pequeño con amigos, "
              "hay opciones más baratas.",
  ),
}
