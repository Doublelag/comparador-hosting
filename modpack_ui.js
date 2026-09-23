/* Paquete de ajustes de cada modpack (/plantillas/modpacks/).

   No descarga el modpack: eso se instala desde el panel del hosting. Lo que
   genera es lo que nadie te da y decide que vaya fino o a tirones:
     · server.properties afinado para ese pack
     · arranque.txt con los argumentos de Java (los de Aikar, los de siempre)
     · LEEME.txt con los pasos concretos de ese pack y su versión

   El zip lo monta zip_ui.js. */
(function () {
  const PACKS = window.MODPACKS;
  if (!PACKS || !document.querySelector("[data-ajustes]")) return;
  const EN = document.documentElement.lang === "en";
  const L = (es, en) => (EN ? en : es);

  // Los mismos escalones que la calculadora de la portada (app.js). Si cambian
  // allí, cambian aquí: es el mismo número el que se enseña y el que se escribe.
  const TIERS = [[4, 2], [10, 3], [20, 4], [40, 6], [70, 8], [120, 12], [200, 16]];
  const PESOS = { ligero: [2, 6], grande: [2.5, 8], bestia: [3, 12] };
  const ESCALONES = [2, 3, 4, 5, 6, 8, 10, 12, 14, 16, 20, 24, 32, 48, 64];

  function ram(jugadores, peso) {
    const base = (TIERS.find(([t]) => jugadores <= t) || TIERS[TIERS.length - 1])[1];
    const [mult, suelo] = PESOS[peso] || PESOS.grande;
    const gb = Math.ceil(Math.max(base * mult, suelo));
    return ESCALONES.find(e => gb <= e) || ESCALONES[ESCALONES.length - 1];
  }

  // Distancia de renderizado: en un modpack es de lo que más TPS come, así que
  // se baja a conciencia y se dice por qué en el LEEME.
  function vista(peso) {
    return peso === "bestia" ? [6, 4] : peso === "grande" ? [7, 5] : [8, 6];
  }

  function propiedades(p, jugadores) {
    const [vd, sd] = vista(p.peso);
    return [
      "# Ajustes para " + p.nombre + " - montatuserver.com",
      "# Pensados para " + jugadores + " jugadores en Minecraft " + p.mc + " (" + p.cargador + ").",
      "# Solo van los ajustes que cambian: el servidor completa el resto al arrancar.",
      "motd=" + p.nombre,
      "max-players=" + jugadores,
      "view-distance=" + vd,
      "simulation-distance=" + sd,
      "difficulty=normal",
      "spawn-protection=0",
      "enforce-secure-profile=false",
      "# Un modpack tarda en arrancar: si el servidor se mata solo al iniciar, sube esto.",
      "max-tick-time=180000",
      "sync-chunk-writes=false",
      "",
    ].join("\n");
  }

  function arranque(gb) {
    return [
      "# Argumentos de Java para " + gb + " GB (los de Aikar, los que usa medio sector).",
      "# En la mayoria de paneles esto se pega en 'JVM arguments' o 'Flags'.",
      "",
      "-Xms" + gb + "G -Xmx" + gb + "G -XX:+UseG1GC -XX:+ParallelRefProcEnabled",
      "-XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC",
      "-XX:+AlwaysPreTouch -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40",
      "-XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5",
      "-XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15",
      "-XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5",
      "-XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1",
      "",
      "# Ojo: Xms y Xmx iguales, y NUNCA mas de la RAM que tengas contratada.",
      "",
    ].join("\n");
  }

  function leeme(p, jugadores, gb) {
    const [vd] = vista(p.peso);
    return L(
`AJUSTES PARA ${p.nombre} - montatuserver.com
=====================================================

EL PACK
  Minecraft ${p.mc} con ${p.cargador}. ${p.mods} mods.
  Pagina oficial: https://modrinth.com/modpack/${p.slug}

LO QUE NECESITAS
  ${gb} GB de RAM para ${jugadores} jugadores.
  Mas RAM de la cuenta no lo hace ir mas rapido: lo que manda es la
  velocidad del procesador por nucleo. En montatuserver.com/hosting/
  esta el procesador de cada hosting.

COMO MONTARLO
  1. En el panel de tu hosting, busca el instalador de modpacks y elige
     "${p.nombre}". Casi todos lo tienen de un clic.
     Si el tuyo no lo tiene, sube el server pack del pack a mano.
  2. Arrancalo una vez y apagalo, para que cree sus carpetas.
  3. Sube este server.properties a la carpeta principal (reemplaza el que hay).
  4. Copia los argumentos de arranque.txt en el apartado de Java del panel.
  5. Arranca. El primer arranque de un modpack tarda varios minutos: es normal.

POR QUE ESTOS AJUSTES
  view-distance=${vd}: en un modpack, la distancia de renderizado es lo que mas
  TPS come. Bajarla dos puntos se nota mas que subir 2 GB de RAM.
  max-tick-time=180000: evita que el servidor se mate solo mientras carga.

SI VA A TIRONES
  - Baja view-distance de uno en uno antes de pagar mas RAM.
  - Mira si el hosting te da nucleos dedicados o compartidos.
  - Con 20 personas o mas, plantearos pre-generar el mundo (mod Chunky).

Datos del pack comprobados en Modrinth. Calculo de RAM: el mismo que la
calculadora de montatuserver.com
`,
`SETTINGS FOR ${p.nombre} - montatuserver.com
=====================================================

THE PACK
  Minecraft ${p.mc} on ${p.cargador}. ${p.mods} mods.
  Official page: https://modrinth.com/modpack/${p.slug}

WHAT YOU NEED
  ${gb} GB of RAM for ${jugadores} players.
  More RAM than that won't make it faster: what matters is single-core CPU
  speed. montatuserver.com/en/hosting/ lists each host's CPU.

HOW TO SET IT UP
  1. In your host's panel, find the modpack installer and pick
     "${p.nombre}". Nearly all of them have it in one click.
     If yours doesn't, upload the pack's server pack by hand.
  2. Start it once and stop it, so it creates its folders.
  3. Upload this server.properties to the main folder (replace the existing one).
  4. Copy the arguments from arranque.txt into the panel's Java section.
  5. Start it. A modpack's first start takes several minutes: that's normal.

WHY THESE SETTINGS
  view-distance=${vd}: on a modpack, view distance is what eats the most TPS.
  Dropping it two points does more than adding 2 GB of RAM.
  max-tick-time=180000: stops the server killing itself while loading.

IF IT STUTTERS
  - Lower view-distance one step at a time before paying for more RAM.
  - Check whether the host gives you dedicated or shared cores.
  - With 20+ people, consider pre-generating the world (Chunky mod).

Pack data checked on Modrinth. RAM maths: the same as the calculator on
montatuserver.com
`);
  }

  document.addEventListener("click", (ev) => {
    const btn = ev.target.closest("[data-ajustes]");
    if (!btn) return;
    const p = PACKS.find(x => x.slug === btn.dataset.ajustes);
    if (!p || !window.MTSzip) return;

    const jugadores = 10;                 // el caso normal; la calculadora afina
    const gb = ram(jugadores, p.peso);
    const enc = new TextEncoder();
    const blob = window.MTSzip([
      [L("LEEME.txt", "README.txt"), enc.encode(leeme(p, jugadores, gb).replace(/\n/g, "\r\n"))],
      ["server.properties", enc.encode(propiedades(p, jugadores))],
      ["arranque.txt", enc.encode(arranque(gb).replace(/\n/g, "\r\n"))],
    ]);
    window.MTSdescargar(blob, "ajustes-" + p.slug + ".zip");

    const antes = btn.textContent;
    btn.textContent = L("Descargado ✓", "Downloaded ✓");
    setTimeout(() => { btn.textContent = antes; }, 2500);
  });
})();
