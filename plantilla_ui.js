/* Generador de plantillas de servidor (montatuserver.com).

   Monta el .zip EN EL NAVEGADOR de quien lo pide:
   - los plugins se bajan de su web oficial (Modrinth y GeyserMC), así que
     no se redistribuye nada y a esta web no le cuesta ni un byte de tráfico;
   - las configuraciones vienen dentro de la página (window.PLANTILLA);
   - server.properties y el LEEME se escriben con lo que elija el usuario.

   El zip va sin comprimir (método «store»): los .jar ya van comprimidos por
   dentro, así que comprimirlos otra vez no ahorraría casi nada. */
(function () {
  const P = window.PLANTILLA;
  const form = document.getElementById("plt-form");
  if (!P || !form) return;
  const EN = document.documentElement.lang === "en";
  const L = (es, en) => (EN ? en : es);

  const $ = (s) => form.querySelector(s);
  const estado = document.getElementById("plt-estado");
  const barra = document.getElementById("plt-barra");
  const boton = $("#plt-generar");
  const jug = $("#plt-jugadores");
  const jugVal = $("#plt-jug-val");

  // ---------------------------------------------------------------- RAM
  // Lo mismo que da la calculadora de la portada (app.js, calcRam) para
  // Paper con plugins: si se cambia allí, se cambia aquí.
  function ram(n) { return n <= 4 ? 3 : n <= 10 ? 4 : 5; }
  function vista(n) { return n <= 6 ? [10, 8] : n <= 12 ? [8, 6] : [7, 5]; }

  function pintarJugadores() {
    const n = +jug.value;
    jugVal.textContent = n;
    const r = document.getElementById("plt-ram");
    if (r) r.textContent = ram(n) + " GB";
    const c = document.getElementById("plt-calc");
    if (c) c.href = (EN ? "/en/" : "/") + "?p=" + n + "&m=plugins#calculadora";
  }
  jug.addEventListener("input", pintarJugadores);
  pintarJugadores();

  // El zip lo monta zip_ui.js (lo comparten esta pagina y la de modpacks)
  const zip = (archivos) => window.MTSzip(archivos);

  // ---------------------------------------------------------------- descargas
  async function modrinth(slug) {
    const base = "https://api.modrinth.com/v2/project/" + slug + "/version?loaders=" +
      encodeURIComponent('["paper"]');
    const conVersion = base + "&game_versions=" + encodeURIComponent(JSON.stringify([P.mc]));
    let vs = await (await fetch(conVersion)).json();
    vs = vs.filter((v) => v.version_type === "release");
    if (!vs.length) {
      vs = (await (await fetch(base)).json()).filter((v) => v.version_type === "release");
    }
    if (!vs.length) throw new Error(slug);
    const f = vs[0].files.find((x) => x.primary) || vs[0].files[0];
    return { url: f.url, nombre: f.filename, version: vs[0].version_number };
  }
  function geyser(proyecto, nombre) {
    return {
      url: "https://download.geysermc.org/v2/projects/" + proyecto +
        "/versions/latest/builds/latest/downloads/spigot",
      nombre: nombre, version: L("la última", "latest"),
    };
  }

  // Descarga con progreso (suma de bytes de todos los plugins)
  async function bajar(url, alAvanzar) {
    const r = await fetch(url);
    if (!r.ok) throw new Error(url);
    const total = +r.headers.get("content-length") || 0;
    if (!r.body || !r.body.getReader) {
      const b = new Uint8Array(await r.arrayBuffer());
      alAvanzar(b.length, total); return b;
    }
    const lector = r.body.getReader(), trozos = [];
    let n = 0;
    for (;;) {
      const { done, value } = await lector.read();
      if (done) break;
      trozos.push(value); n += value.length; alAvanzar(value.length, total);
    }
    const out = new Uint8Array(n);
    let o = 0;
    for (const t of trozos) { out.set(t, o); o += t.length; }
    return out;
  }

  // ---------------------------------------------------------------- textos
  function propiedades(o) {
    // server.properties se lee como ISO-8859-1: lo que no sea ASCII va escapado
    const esc = (s) => s.replace(/[^\x20-\x7e]/g,
      (c) => "\\u" + c.charCodeAt(0).toString(16).padStart(4, "0"));
    const [vd, sd] = vista(o.jugadores);
    return [
      "# Plantilla " + P.nombre + " - montatuserver.com",
      "# Solo van los ajustes que cambian: el servidor completa el resto al arrancar.",
      "motd=" + esc(o.motd),
      "max-players=" + o.jugadores,
      "difficulty=" + o.dificultad,
      "pvp=" + (o.pvp ? "true" : "false"),
      "view-distance=" + vd,
      "simulation-distance=" + sd,
      "spawn-protection=0",
      // Geyser lo recomienda para que el chat de los de Bedrock funcione
      "enforce-secure-profile=false",
      "",
    ].join("\n");
  }

  function leeme(o, plugins) {
    const lista = plugins.map((p) => "  - " + p.nombre + "  (" + p.version + ")").join("\n");
    const bed = o.bedrock ? L(
      "\nJUGADORES DE BEDROCK (móvil, consola, Windows)\n" +
      "  Entran con la misma IP y el MISMO puerto que los de PC.\n" +
      "  En el juego su nombre sale con un punto delante (.Nombre): es normal.\n" +
      "  Si tu hosting te da un puerto aparte para Bedrock, ponlo en\n" +
      "  plugins/Geyser-Spigot/config.yml (bedrock > port) y cambia\n" +
      "  clone-remote-port a false.\n",
      "\nBEDROCK PLAYERS (mobile, console, Windows)\n" +
      "  They join with the same IP and the SAME port as PC players.\n" +
      "  In game their name shows with a dot in front (.Name): that's normal.\n" +
      "  If your host gives you a separate Bedrock port, set it in\n" +
      "  plugins/Geyser-Spigot/config.yml (bedrock > port) and change\n" +
      "  clone-remote-port to false.\n") : "";
    return L(
      "PLANTILLA " + P.nombre.toUpperCase() + " - montatuserver.com\n" +
      "=====================================================\n\n" +
      "CÓMO SUBIRLA (5 minutos)\n" +
      "  1. En el panel de tu hosting, elige Paper " + P.mc + " como tipo de servidor.\n" +
      "  2. Arráncalo una vez y apágalo (así crea sus carpetas y acepta la EULA).\n" +
      "  3. Sube este .zip a la carpeta principal y descomprímelo ahí.\n" +
      "     Si pregunta si reemplazar archivos: SÍ.\n" +
      "  4. Arranca el servidor.\n" +
      "  5. En la consola del panel escribe:  op TuNombre\n" +
      "     (así tú eres el admin y puedes usar todos los comandos).\n\n" +
      "RAM RECOMENDADA: " + ram(o.jugadores) + " GB para " + o.jugadores + " jugadores.\n" +
      bed +
      "\nCOMANDOS PARA TODOS\n" +
      "  /sethome [nombre]  /home  /delhome   hasta 3 casas por jugador\n" +
      "  /tpa Nombre  /tpaccept  /tpdeny      teletransporte entre amigos\n" +
      "  /back                                volver a donde moriste\n" +
      "  /msg Nombre texto  /r texto          mensajes privados\n" +
      "  /afk  /list  /seen Nombre  /mail\n\n" +
      "SI ALGUIEN LA LÍA (solo admin)\n" +
      "  /co inspect      y pica un bloque: te dice quién lo puso o lo rompió\n" +
      "  /co rollback u:Nombre t:2h r:30    deshace lo que hizo en 2 horas\n\n" +
      "SI NO ARRANCA O NADIE PUEDE ENTRAR\n" +
      "  Este zip trae su propio server.properties. Casi todos los paneles vuelven a\n" +
      "  poner tu puerto solos al arrancar, pero si el tuyo no lo hace, abre\n" +
      "  server.properties y añade la línea  server-port=  con el puerto que te\n" +
      "  da tu hosting.\n\n" +
      "SOLO PARA TUS AMIGOS (lista blanca)\n" +
      "  whitelist add Nombre    (jugador de PC)\n" +
      "  fwhitelist add Nombre   (jugador de Bedrock)\n" +
      "  whitelist on\n\n" +
      "PLUGINS (bajados de su web oficial el " + new Date().toLocaleDateString("es-ES") + ")\n" +
      lista + "\n\n" +
      "Probada en Paper " + P.mc + " (" + P.probada + ").\n" +
      "Los de PC con una versión más nueva de Minecraft también entran (ViaVersion).\n",
      "TEMPLATE " + P.nombre_en.toUpperCase() + " - montatuserver.com\n" +
      "=====================================================\n\n" +
      "HOW TO UPLOAD IT (5 minutes)\n" +
      "  1. In your host's panel, pick Paper " + P.mc + " as the server type.\n" +
      "  2. Start it once and stop it (so it creates its folders and accepts the EULA).\n" +
      "  3. Upload this .zip to the main folder and extract it there.\n" +
      "     If it asks whether to replace files: YES.\n" +
      "  4. Start the server.\n" +
      "  5. In the panel's console type:  op YourName\n" +
      "     (that makes you admin so you can use every command).\n\n" +
      "RECOMMENDED RAM: " + ram(o.jugadores) + " GB for " + o.jugadores + " players.\n" +
      bed +
      "\nCOMMANDS FOR EVERYONE\n" +
      "  /sethome [name]  /home  /delhome     up to 3 homes per player\n" +
      "  /tpa Name  /tpaccept  /tpdeny        teleport between friends\n" +
      "  /back                                go back to where you died\n" +
      "  /msg Name text  /r text              private messages\n" +
      "  /afk  /list  /seen Name  /mail\n\n" +
      "IF SOMEONE MESSES UP (admin only)\n" +
      "  /co inspect      then hit a block: shows who placed or broke it\n" +
      "  /co rollback u:Name t:2h r:30      undoes what they did in 2 hours\n\n" +
      "IF IT WON'T START OR NOBODY CAN JOIN\n" +
      "  This zip has its own server.properties. Almost every panel puts your port\n" +
      "  back automatically on start, but if yours doesn't, open server.properties\n" +
      "  and add the line  server-port=  with the port your host gives you.\n\n" +
      "FRIENDS ONLY (whitelist)\n" +
      "  whitelist add Name    (PC player)\n" +
      "  fwhitelist add Name   (Bedrock player)\n" +
      "  whitelist on\n\n" +
      "PLUGINS (downloaded from their official site on " + new Date().toLocaleDateString("en-GB") + ")\n" +
      lista + "\n\n" +
      "Tested on Paper " + P.mc + " (" + P.probada_en + ").\n" +
      "PC players on a newer Minecraft version can join too (ViaVersion).\n");
  }

  // ---------------------------------------------------------------- generar
  function mb(n) { return (n / 1048576).toFixed(1).replace(".", EN ? "." : ",") + " MB"; }

  form.addEventListener("submit", async (ev) => {
    ev.preventDefault();
    const o = {
      motd: ($("#plt-nombre").value.trim() || L("Server de amigos", "Friends server")).slice(0, 59),
      jugadores: +jug.value,
      dificultad: $("#plt-dificultad").value,
      pvp: $("#plt-pvp").checked,
      bedrock: $("#plt-bedrock").checked,
    };
    boton.disabled = true;
    barra.hidden = false; barra.value = 0;
    estado.className = "plt-estado";
    estado.textContent = L("Buscando la última versión de cada plugin…", "Finding the latest version of each plugin…");

    try {
      const fuentes = await Promise.all(P.plugins
        .filter((p) => o.bedrock || !p.bedrock)
        .map((p) => Promise.resolve(p.geyser ? geyser(p.geyser, p.archivo) : modrinth(p.modrinth))
          .then((f) => Object.assign(f, { titulo: p.titulo }))));

      let hecho = 0, total = 0;
      const vistos = new Set();
      const datos = await Promise.all(fuentes.map((f) => bajar(f.url, (n, t) => {
        if (t && !vistos.has(f.url)) { vistos.add(f.url); total += t; }
        hecho += n;
        if (total) barra.value = Math.min(99, (hecho / total) * 100);
        estado.textContent = L("Descargando plugins de su web oficial… ", "Downloading plugins from their official site… ") + mb(hecho);
      })));

      const enc = new TextEncoder();
      const archivos = [];
      archivos.push([L("LEEME.txt", "README.txt"), enc.encode(leeme(o, fuentes.map((f) => ({ nombre: f.titulo, version: f.version }))).replace(/\n/g, "\r\n"))]);
      archivos.push(["server.properties", enc.encode(propiedades(o))]);
      for (const [ruta, txt] of Object.entries(P.archivos)) {
        if (!o.bedrock && ruta.indexOf("Geyser-Spigot/") !== -1) continue;
        archivos.push([ruta, enc.encode(txt)]);
      }
      fuentes.forEach((f, i) => archivos.push(["plugins/" + f.nombre, datos[i]]));

      const blob = zip(archivos);
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = P.zip + ".zip";
      document.body.appendChild(a); a.click(); a.remove();
      setTimeout(() => URL.revokeObjectURL(a.href), 60000);

      barra.value = 100;
      estado.className = "plt-estado ok";
      estado.textContent = L("¡Listo! Se ha descargado " + P.zip + ".zip (" + mb(blob.size) + "). Sigue los pasos de abajo.",
        "Done! " + P.zip + ".zip has been downloaded (" + mb(blob.size) + "). Follow the steps below.");
      document.getElementById("pasos-subir").scrollIntoView({ behavior: "smooth", block: "start" });
    } catch (e) {
      console.error(e);
      estado.className = "plt-estado mal";
      estado.textContent = L("No se ha podido descargar algún plugin (puede que su web esté caída). Vuelve a intentarlo en un rato.",
        "Couldn't download one of the plugins (its site may be down). Try again in a while.");
    } finally {
      boton.disabled = false;
    }
  });
})();
