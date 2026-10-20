/* =========================================================================
   CONFIGURACIÓN — lo único que tocas tú
   ========================================================================= */

/* Idioma de la página: lo marca el <html lang>. Cada texto va en los dos
   idiomas, uno al lado del otro, para que al cambiar uno no se olvide el otro. */
const EN = document.documentElement.lang === "en";
const L = (es, en) => EN ? en : es;

const CONFIG = {
  /* Con quién hay acuerdo de afiliación. Vive en hosts.js → partner, que es el
     ÚNICO sitio que se toca al cambiar de partner. Con activo=false (el estado
     desde el 11-sep-2026) no sale ningún botón de contratar ni ningún hosting
     destacado: la web es un comparador y punto. */
  partner: window.DATOS.partner || { activo: false },

  // Etiqueta de canal para el enlace del partner (?cid=). Se sobreescribe si
  // la visita entra con ?cid=YT, ?cid=TIKTOK…
  canal: (window.DATOS.partner && window.DATOS.partner.canal) || "WEB",

  pricesChecked: EN ? (window.DATOS.comprobado_en || window.DATOS.comprobado) : window.DATOS.comprobado,
};

/* =========================================================================
   LOS HOSTINGS Y SUS PRECIOS
   Viven en hosts.js, que se carga ANTES que este archivo. Está así para que
   Python (build.py) pueda leer los mismos números y generar las tablas de
   las comparativas: un solo sitio que actualizar, sin riesgo de que la
   calculadora y las páginas digan precios distintos.
   ========================================================================= */

const CAMBIO_USD_EUR = window.DATOS.cambioUsdEur;

/* Todos los hostings van en hosts.js y se tratan igual. Hasta el 11-sep-2026
   DatHost iba aparte, con su precio anual en la tabla mientras al resto se le
   ponía el mensual; eso le hacía parecer más barato de lo que era mes a mes. */
const HOSTS = window.DATOS.hosts;

/* ---- Partner ----------------------------------------------------------- */
function partnerActivo(){
  const p = CONFIG.partner;
  return !!(p && p.activo && p.hostId && p.enlace);
}
function esPartner(id){ return partnerActivo() && id === CONFIG.partner.hostId; }
function partnerHost(){
  return partnerActivo() ? HOSTS.find(h => h.id === CONFIG.partner.hostId) : null;
}
// Enlace de afiliado para este juego, o null. Nunca enlaza a un juego que el
// partner no vende: sería mandar a alguien a contratar algo que no existe.
function partnerLink(g){
  const h = partnerHost();
  if (!h || !(h.precios || {})[g.id]) return null;
  const p = CONFIG.partner;
  let url = p.enlace;
  if (url.includes("{juego}"))
    url = url.replace("{juego}", (p.slugs || {})[g.id] || g.slug || g.id);
  return url + (url.includes("?") ? "&" : "?") + "cid=" + CONFIG.canal;
}
// La promo del partner para este juego, si está viva y trae su letra pequeña.
function promoPartner(g){
  if (!partnerActivo()) return null;
  const pr = CONFIG.partner.promo;
  if (!pr || !pr.letra || !(pr.juegos || []).includes(g.id)) return null;
  return new Date().toISOString().slice(0, 10) <= pr.hasta ? pr : null;
}

/* =========================================================================
   MINECRAFT — tabla de RAM
   Base: consumo real observado en servidores de Minecraft (Paper, Fabric,
   Forge). Son RECOMENDACIONES con margen, no mínimos absolutos.
   Hasta el 17-sep-2026 aquí había 11 juegos; la web es ahora solo de
   Minecraft. Se deja como lista para no reescribir el motor entero.
   ========================================================================= */

const GAMES = [
  {
    id: "minecraft", url: "minecraft", slug: "minecraft", name: "Minecraft", icon: "🟩",
    maxPlayers: 200, defPlayers: 10,
    // [hasta X jugadores, GB base]
    tiers: [[4,2],[10,3],[20,4],[40,6],[70,8],[120,12],[200,16]],
    modLabel: L("¿Mods o plugins?", "Mods or plugins?"),
    mods: [
      { id:"vanilla", label:"Vanilla",                             desc:L("Sin nada instalado","Nothing installed"),        mult:1,   floor:0 },
      { id:"plugins", label:"Plugins",                             desc:L("Paper/Spigot, hasta ~25","Paper/Spigot, up to ~25"), mult:1.25,floor:3 },
      { id:"light",   label:L("Modpack ligero","Light modpack"),   desc:L("Hasta ~100 mods","Up to ~100 mods"),             mult:2,   floor:6 },
      { id:"heavy",   label:L("Modpack grande","Big modpack"),     desc:"100-250 mods, RLCraft…",                           mult:2.5, floor:8 },
      { id:"insane",  label:L("Modpack bestia","Huge modpack"),    desc:"250+ mods, GTNH, ATM",                             mult:3,   floor:12 },
    ],
    extraLabel: L("Distancia de renderizado del servidor", "Server view distance"),
    extra: [
      { id:"6",  label:L("Corta (6)","Short (6)"),  desc:L("Menos RAM, mundo más 'pequeño'","Less RAM, a 'smaller' world"), mult:0.85 },
      { id:"10", label:"Normal (10)",               desc:L("El valor por defecto","The default"),                           mult:1 },
      { id:"16", label:L("Larga (16)","Long (16)"), desc:L("Se ve lejísimos, come RAM","See for miles, eats RAM"),          mult:1.35 },
    ],
    cpu: L("Minecraft va casi todo por <strong>un solo núcleo</strong>. Un procesador con muchos núcleos flojos rinde peor que uno con pocos núcleos rápidos: mira qué CPU te ponen, no solo los gigas.",
           "Minecraft runs almost entirely on <strong>a single core</strong>. A CPU with lots of slow cores does worse than one with a few fast ones: check which CPU you get, not just the gigabytes."),
  },
];

/* =========================================================================
   MOTOR DE CÁLCULO
   ========================================================================= */

// Escalones reales de RAM que se venden en el mercado
const STEPS = [2,3,4,5,6,8,10,12,14,16,20,24,32,48,64];

function snapUp(gb){
  for (const s of STEPS) if (gb <= s) return s;
  return STEPS[STEPS.length - 1];
}

function baseRam(game, players){
  for (const [max, gb] of game.tiers) if (players <= max) return gb;
  return game.tiers[game.tiers.length - 1][1];
}

function calcRam(game, players, modId, extraId){
  let gb = baseRam(game, players);

  const mod = game.mods.find(m => m.id === modId) || game.mods[0];
  if (mod.mult) gb *= mod.mult;
  if (mod.add)  gb += mod.add;
  if (mod.floor) gb = Math.max(gb, mod.floor);

  if (game.extra){
    const ex = game.extra.find(e => e.id === extraId) || game.extra[0];
    if (ex.mult) gb *= ex.mult;
  }

  return snapUp(Math.ceil(gb));
}


/* Si alguien llega con ?cid=TIKTOK (o ?utm_source=tiktok), ese canal viaja hasta
   el partner. Así en su panel ves qué red te trae las ventas, no solo las visitas.
   Pon en cada bio: montatuserver.com/?cid=TIKTOK , /?cid=IG , /?cid=YT … */
(function detectarCanal(){
  const p = new URLSearchParams(location.search);
  let cid = p.get("cid") || p.get("utm_source");
  if (cid && /^[A-Za-z0-9_-]{1,20}$/.test(cid)){
    // Se guarda para el resto de la visita: si entra por ?cid=YT y luego navega
    // a la comparativa, la venta se seguia apuntando al sitio del boton y no al
    // canal, que es justo lo que queriamos medir.
    try { sessionStorage.setItem("cid", cid.toUpperCase()); } catch {}
  } else {
    try { cid = sessionStorage.getItem("cid"); } catch {}
  }
  if (cid && /^[A-Za-z0-9_-]{1,20}$/.test(cid)){
    CONFIG.canal = cid.toUpperCase();
  }
})();

/* ---- Precios y promos --------------------------------------------------- */

function eur(n){ return EN ? "€" + n.toFixed(2) : n.toFixed(2).replace(".", ",") + " €"; }

/* =========================================================================
   ESTADO + RENDER
   ========================================================================= */


/* Presupuesto. No cambia los GB que necesitas — cambia cuáles de las opciones
   te sirven, que es lo que de verdad quiere saber quien entra. */
/* Cuánto tiempo va a estar encendido. Es la pregunta que más cambia la
   respuesta y no la hace nadie: con un mes gana quien tenga mejor descuento de
   entrada; con un año, quien tenga la tarifa más baja. Sin esto, recomendar es
   medio adivinar. */
const TIEMPOS = [
  { id:"mes",       label:L("Un mes","A month"),        desc:L("Probar, un evento","Trying it out, an event"),       meses:1 },
  { id:"temporada", label:L("Unos meses","A few months"), desc:L("Una temporada con amigos","A season with friends"), meses:4 },
  { id:"ano",       label:L("Todo el año","All year"),   desc:L("Un server serio","A serious server"),                meses:12 },
];

const PRESUPUESTOS = [
  { id:"todo", label:L("Sin límite","No limit"),   desc:L("Enséñamelo todo","Show me everything"),          max:null },
  { id:"5",    label:L("Hasta 5 €","Up to €5"),    desc:L("Lo más barato posible","As cheap as it gets"),   max:5 },
  { id:"10",   label:L("Hasta 10 €","Up to €10"),  desc:L("Un café al mes","A coffee a month"),             max:10 },
  { id:"15",   label:L("Hasta 15 €","Up to €15"),  desc:L("Lo normal para un grupo","Typical for a group"), max:15 },
  { id:"25",   label:L("Hasta 25 €","Up to €25"),  desc:L("Sin agobios","No stress"),                       max:25 },
];

const state = {
  gameId: "minecraft",
  tiempoId: "temporada",
  players: 6,
  modId: null,
  extraId: null,
  presuId: "todo",
  verTodo: false,
};

/* ---- Resultado compartible ----------------------------------------------
   El caso de uso real: alguien calcula "30 jugadores con modpack" y lo pega
   en el Discord de su grupo. Sin esto, al de enfrente le salía la calculadora
   en blanco y se perdía la conversión. Ahora el estado va en la URL. */

function leerURL(){
  const p = new URLSearchParams(location.search);
  return {
    players: parseInt(p.get("p"), 10) || null,
    modId:   p.get("m"),
    extraId: p.get("e"),
    presuId: p.get("b"),
    tiempoId: p.get("t"),
  };
}

function escribirURL(){
  const p = new URLSearchParams(location.search);
  p.delete("j");            // enlaces viejos de cuando había varios juegos
  p.set("p", state.players);
  p.set("m", state.modId);
  if (state.extraId) p.set("e", state.extraId); else p.delete("e");
  p.set("t", state.tiempoId);
  if (state.presuId && state.presuId !== "todo") p.set("b", state.presuId); else p.delete("b");
  history.replaceState(null, "", location.pathname + "?" + p.toString());
}

function enlaceResultado(){
  const p = new URLSearchParams();
  p.set("p", state.players);
  p.set("m", state.modId);
  if (state.extraId) p.set("e", state.extraId);
  if (state.presuId && state.presuId !== "todo") p.set("b", state.presuId);
  return `${location.origin}${EN ? "/en/" : "/"}?${p.toString()}`;
}

const $ = sel => document.querySelector(sel);

function game(){ return GAMES.find(g => g.id === state.gameId); }

function selectGame(id, desdeURL){
  state.gameId = id;
  const g = game();

  state.players = Math.min(g.defPlayers, g.maxPlayers);
  state.modId   = g.mods[0].id;
  // Por defecto, la opción "neutra" (la que no multiplica). Si no hay, la primera.
  state.extraId = g.extra ? (g.extra.find(e => e.mult === 1) || g.extra[0]).id : null;

  // Si venimos de un enlace compartido, respetamos lo que traiga (validado)
  if (desdeURL){
    if (desdeURL.players)
      state.players = Math.min(Math.max(1, desdeURL.players), g.maxPlayers);
    if (desdeURL.modId && g.mods.some(m => m.id === desdeURL.modId))
      state.modId = desdeURL.modId;
    if (desdeURL.extraId && g.extra && g.extra.some(e => e.id === desdeURL.extraId))
      state.extraId = desdeURL.extraId;
    if (desdeURL.presuId && PRESUPUESTOS.some(x => x.id === desdeURL.presuId))
      state.presuId = desdeURL.presuId;
  }

  renderAll();
  escribirURL();
}

// Al llegar al tope del deslizador se enseña «200+»: el tope es del
// deslizador, no de la calculadora, y así se ve que también vale para más.
function jugTxt(n){ return n >= game().maxPlayers ? n + "+" : String(n); }

function renderControls(){
  const g = game();

  // Slider de jugadores
  $("#players").max   = g.maxPlayers;
  $("#players").value = state.players;
  $("#pnum").textContent = jugTxt(state.players);

  // Mods
  $("#modLabel").textContent = g.modLabel;
  $("#mods").innerHTML = g.mods.map(m => `
    <button type="button" data-mod="${m.id}" aria-pressed="${m.id === state.modId}">
      ${m.label}<small>${m.desc}</small>
    </button>`).join("");

  // Cuánto tiempo
  $("#tiempo").innerHTML = TIEMPOS.map(x => `
    <button type="button" data-tiempo="${x.id}" aria-pressed="${x.id === state.tiempoId}">
      ${x.label}<small>${x.desc}</small>
    </button>`).join("");

  // Presupuesto
  $("#presupuesto").innerHTML = PRESUPUESTOS.map(x => `
    <button type="button" data-presu="${x.id}" aria-pressed="${x.id === state.presuId}">
      ${x.label}<small>${x.desc}</small>
    </button>`).join("");

  // Extra (opcional)
  const hasExtra = !!g.extra;
  $("#extraStep").hidden = !hasExtra;
  if (hasExtra){
    $("#extraLabel").textContent = g.extraLabel;
    $("#extra").innerHTML = g.extra.map(e => `
      <button type="button" data-extra="${e.id}" aria-pressed="${e.id === state.extraId}">
        ${e.label}<small>${e.desc}</small>
      </button>`).join("");
  }
}

/* Cuenta hasta el número en vez de saltar. Es el dato principal de la web:
   que se mueva hace que se lea, y que la calculadora parezca que calcula. */
function animarNumero(caja, destino, unidad){
  const desde = parseInt(caja.dataset.valor || "0", 10) || 0;
  caja.dataset.valor = destino;
  if (desde === destino){
    caja.innerHTML = `${destino}<span>${unidad}</span>`;
    return;
  }
  const t0 = performance.now(), dur = 380;
  const paso = ahora => {
    const t = Math.min(1, (ahora - t0) / dur);
    const suave = 1 - Math.pow(1 - t, 3);           // frena al final
    const v = Math.round(desde + (destino - desde) * suave);
    caja.innerHTML = `${v}<span>${unidad}</span>`;
    if (t < 1) requestAnimationFrame(paso);
  };
  requestAnimationFrame(paso);
}

function renderResult(){
  const g  = game();
  const gb = calcRam(g, state.players, state.modId, state.extraId);

  animarNumero($("#resRam"), gb, L("GB de RAM", "GB of RAM"));
  $("#resFor").textContent = EN
    ? `for ${jugTxt(state.players)} ${state.players === 1 ? "player" : "players"}`
    : `para ${jugTxt(state.players)} ${state.players === 1 ? "jugador" : "jugadores"}`;

  $("#resCpu").innerHTML = g.cpu;

  const chips = [
    `<span class="chip">${jugTxt(state.players)} ${L("jugadores", "players")}</span>`,
    `<span class="chip">${(g.mods.find(m=>m.id===state.modId)||g.mods[0]).label}</span>`,
  ];
  if (g.extra){
    const ex = g.extra.find(e => e.id === state.extraId) || g.extra[0];
    chips.push(`<span class="chip">${ex.label}</span>`);
  }
  $("#resChips").innerHTML = chips.join("");

  /* Veredicto. Sale del precio real de hoy, no de un hosting elegido de
     antemano: dice cuál es el más barato para TUS gigas, sea quien sea. Antes
     giraba entero alrededor de los "16 GB fijos" de DatHost, que no era una
     verdad general sino la oferta de un solo hosting. */
  /* Solo cuenta para el veredicto quien GARANTIZA los gigas. Realms vende
     plazas y no publica la RAM: sale en las barras con su "te da 11 slots",
     pero decir "con 6 GB lo más barato es Realms" sería afirmar algo que no
     sabemos. */
  const validos = preciosDe(gb, g).filter(f => f.eurMes != null && /\bGB\b/.test(f.da || ""));
  const v = $("#verdict");
  if (!validos.length){
    v.className = "verdict over";
    v.innerHTML = L(`<strong>Aquí te quedas corto.</strong> Ninguno de los hostings que
      he comprobado llega a ${gb} GB. Para esto hace falta un servidor
      dedicado, o partir la comunidad en varios servidores.`,
      `<strong>That's beyond what's on offer.</strong> None of the hosts I've checked
      reaches ${gb} GB. For this you need a dedicated server, or to split the
      community across several servers.`);
  } else {
    const barato = validos[0];
    const otro = validos[1]
      ? L(` El siguiente es ${validos[1].nombre}, a ${eur(validos[1].eurMes)}.`,
          ` Next is ${validos[1].nombre}, at ${eur(validos[1].eurMes)}.`) : "";
    if (gb <= 4){
      v.className = "verdict small";
      v.innerHTML = L(`<strong>Necesitas muy poco.</strong> Con ${gb} GB te vale casi
        cualquier hosting, así que no pagues RAM que no vas a usar. Lo más barato ahora
        mismo es <strong>${barato.nombre}</strong>, a ${eur(barato.eurMes)} al mes.${otro}`,
        `<strong>You need very little.</strong> With ${gb} GB almost any host will do,
        so don't pay for RAM you won't use. The cheapest right now is
        <strong>${barato.nombre}</strong>, at ${eur(barato.eurMes)} a month.${otro}`);
    } else if (gb > 16){
      v.className = "verdict over";
      v.innerHTML = L(`<strong>Vas a necesitar mucha RAM.</strong> Con ${gb} GB te sales de
        lo que da un plan normal y solo llegan algunos de los que cobran por giga. Lo más
        barato que lo cubre es <strong>${barato.nombre}</strong>, a ${eur(barato.eurMes)}
        al mes. Plantéate también partir la comunidad en dos servidores.`,
        `<strong>You'll need a lot of RAM.</strong> ${gb} GB is beyond a normal plan and
        only some of the per-gigabyte hosts get there. The cheapest that covers it is
        <strong>${barato.nombre}</strong>, at ${eur(barato.eurMes)} a month. Consider
        splitting the community across two servers too.`);
    } else {
      v.className = "verdict";
      v.innerHTML = L(`<strong>Con ${gb} GB vas bien.</strong> Lo más barato que he
        comprobado es <strong>${barato.nombre}</strong>, a ${eur(barato.eurMes)} al
        mes.${otro} Echa un ojo a la letra pequeña de la tabla antes de decidir: el más
        barato no siempre es el que más te conviene.`,
        `<strong>${gb} GB will do nicely.</strong> The cheapest I've checked is
        <strong>${barato.nombre}</strong>, at ${eur(barato.eurMes)} a month.${otro}
        Look at the fine print in the table before deciding: the cheapest isn't always
        the best fit.`);
    }
  }

  renderBarras(gb, g);
  renderReco(gb, g);
  renderTable(gb, g);

  /* Partner: detalle y botón SOLO si hay acuerdo activo y vende este juego. Va
     debajo del veredicto a propósito: el veredicto dice el más barato aunque no
     sea él. */
  const link = partnerLink(g);
  const pf = $("#precioFinal");
  pf.hidden = true;
  $("#ctaWrap").hidden = !link;
  if (link){
    const h = partnerHost();
    const fila = preciosDe(gb, g).find(f => f.id === h.id);
    const cfg = CONFIG.partner;
    const pr = promoPartner(g);
    const lineas = [];
    if (fila && fila.eurMes != null)
      lineas.push(L(`${h.nombre}: <strong>${eur(fila.eurMes)} al mes</strong> para ${gb} GB.`,
                    `${h.nombre}: <strong>${eur(fila.eurMes)} a month</strong> for ${gb} GB.`));
    if (cfg.codigo)
      lineas.push(`${L("Código", "Code")} <strong>${cfg.codigo}</strong>${(EN ? cfg.descuento_en : cfg.descuento) ? " · " + (EN ? cfg.descuento_en : cfg.descuento) : ""}.`);
    if (pr) lineas.push(`<strong>${pr.titulo}.</strong> ${pr.letra}`);
    // Por qué ese hosting, en tres líneas. Salen de hosts.js → partner.razones
    const razones = ((EN ? cfg.razones_en : cfg.razones) || []).map(r => `<li>${r}</li>`).join("");
    if (lineas.length || razones){
      pf.hidden = false;
      pf.innerHTML = (razones ? `<ul class="pf-razones">${razones}</ul>` : "")
                   + (lineas.length ? `<p class="pf-pie">${lineas.join("<br>")}</p>` : "");
    }
    const cta = $("#ctaMain");
    cta.href = link;
    cta.rel = "sponsored nofollow noopener";
    cta.textContent = (fila && fila.eurMes != null)
      ? L(`Montar mi servidor en ${h.nombre}`, `Set up my server on ${h.nombre}`)
      : L(`Ver qué me ofrece ${h.nombre}`, `See what ${h.nombre} offers`);
  }
}

/* ---- Comparativa visual -------------------------------------------------
   Devuelve, para los GB que necesitas, lo que te cobra cada host al mes en
   euros. null = ese host no te sirve para este caso. */
/* `jugadores` va como argumento y no se lee de state a secas porque la tarjeta
   de ejemplo del hero calcula un caso de 30 jugadores. Leyendo el state salia
   el plan de 11 plazas de Realms como el mas barato para un caso de 30 personas
   con modpack, que Realms directamente no puede servir. */
function mesesElegidos(){
  return (TIEMPOS.find(x => x.id === state.tiempoId) || TIEMPOS[1]).meses;
}

/* Lo que te vas a gastar de verdad en el tiempo que vayas a tenerlo, contando
   el descuento de entrada donde lo haya. Es el número con el que se ordena y
   con el que se recomienda: el precio del primer mes engaña, y la tarifa sola
   también. */
function costeEn(eurMes, entrada, mesesEntrada, meses){
  if (eurMes == null) return null;
  if (entrada == null) return eurMes * meses;
  const conDesc = Math.min(mesesEntrada || 1, meses);
  return entrada * conDesc + eurMes * (meses - conDesc);
}

function preciosDe(gb, g, jugadores, meses){
  if (jugadores == null) jugadores = state.players;
  if (meses == null) meses = mesesElegidos();
  const filas = [];

  for (const h of HOSTS){
    /* Lo que no puede hacer por mucho que pagues: Realms no admite mods ni
       plugins y se queda en diez personas. Enseñarlo barato cuando pides un
       modpack sería mandar a alguien a contratar algo que no le sirve. */
    const lim = h.limites || {};
    if (lim.mods === false && state.modId && state.modId !== "vanilla") continue;
    if (lim.maxJugadores && jugadores > lim.maxJugadores) continue;
    const aEur = v => h.moneda === "USD" ? v * CAMBIO_USD_EUR : v;

    // Solo sale quien tiene precio de Minecraft comprobado a mano

    const pr = h.precios && h.precios[g.id];
    if (!pr) continue;

    let eurMes = null, da = gb + " GB";

    if (pr.modelo === "porGB"){
      eurMes = aEur(pr.porGB * gb);
    } else if (pr.modelo === "tabla"){
      const t = pr.tiers.find(([tgb]) => gb <= tgb);
      if (t){ eurMes = aEur(t[1]); da = t[0] + " GB"; }
    } else if (pr.modelo === "plano"){
      da = pr.slots ? pr.slots + " slots" : pr.ram + " GB";
      if (pr.ram && gb > pr.ram){
        eurMes = null;
        da = pr.ram + " GB";
      } else {
        eurMes = aEur(pr.precio);
      }
    } else if (pr.modelo === "slots"){
      /* Quien vende por plazas no publica la RAM, así que su plan se elige por
         JUGADORES. Si no llega a los que sois, se dice — comparar su plan de 10
         plazas con vuestros 20 jugadores sería mentir a favor suyo. */
      const t = pr.tiers.find(([s]) => jugadores <= s);
      if (t){ eurMes = aEur(t[1]); da = t[0] + " slots"; }
      else { da = pr.tiers[pr.tiers.length - 1][0] + " slots"; }
    }

    /* Lo que pagas de verdad el primer año. Medio sector anuncia un precio de
       entrada ("-75 % en tu primera compra") y renueva al triple; sin esta
       cuenta, el comparador ayuda a la trampa en vez de destaparla. La tarifa
       de hosts.js es SIEMPRE la recurrente y el descuento de entrada va aparte,
       en `entrada`, así que aquí solo hay que juntarlos. */
    let entrada = null, anual = null;
    if (eurMes != null){
      anual = eurMes * 12;
      if (pr.entrada){
        const meses = pr.entrada.meses || 1;
        entrada = eurMes * (1 - pr.entrada.pct / 100);
        anual = entrada * meses + eurMes * (12 - meses);
      }
    }

    filas.push({
      id: h.id, nombre: h.nombre, ficha: h.ficha, eurMes, da, destacado: esPartner(h.id),
      entrada, anual, vps: !!h.vps, aviso: EN ? (h.aviso_en || h.aviso) : h.aviso,
      meses,
      coste: costeEn(eurMes, entrada, pr.entrada ? (pr.entrada.meses || 1) : 0, meses),
      entradaQue: pr.entrada ? (EN ? (pr.entrada.que_en || pr.entrada.que) : pr.entrada.que) : null,
      entradaPct: pr.entrada ? pr.entrada.pct : null,
      nota: (EN ? (pr.nota_en || pr.nota) : pr.nota) +
            (eurMes === null ? L(" · su plan se queda corto", " · their plan falls short") : ""),
    });
  }

  // Se ordena por lo que cuesta en el tiempo que ha dicho, no por la tarifa
  filas.sort((a, b) => (a.coste ?? 1e9) - (b.coste ?? 1e9) || (a.eurMes ?? 1e9) - (b.eurMes ?? 1e9));
  return filas;
}

/* ---- La recomendación ----------------------------------------------------
   Lo que más se pedía: "vale, pero ¿cuál pillo?". Se decide con el coste real
   en el tiempo que ha dicho la persona, no con la tarifa suelta ni con quien
   me pague comisión; si el partner no es el que menos cuesta, no sale aquí.
   Debajo van las dos alternativas que de verdad cambian la decisión: el más
   barato a la larga y el que menos pide para empezar. */
function renderReco(gb, g){
  const caja = $("#reco");
  if (!caja) return;
  const meses = mesesElegidos();
  const tiempo = (TIEMPOS.find(x => x.id === state.tiempoId) || TIEMPOS[1]).label.toLowerCase();
  const validos = preciosDe(gb, g).filter(f => f.coste != null && /\bGB\b/.test(f.da || ""));
  if (!validos.length){ caja.hidden = true; return; }

  const mejor = validos[0];
  const total = meses > 1
    ? L(`${eur(mejor.coste)} en ${meses} meses`, `${eur(mejor.coste)} over ${meses} months`)
    : L(`${eur(mejor.coste)} el primer mes`, `${eur(mejor.coste)} for the first month`);
  const porQue = (mejor.entrada != null && meses <= 4)
    ? L(`su descuento de entrada le deja ${total}, contando ya la tarifa normal del resto`,
        `its entry discount puts it at ${total}, counting the normal rate for the rest`)
    : L(`es lo que menos te cuesta: ${total}`,
        `it's the cheapest: ${total}`);

  const alt = [];
  // Primero la pega del recomendado, y con su nombre: si va detrás de una
  // alternativa, parece que la pega es de la otra.
  if (mejor.aviso)
    alt.push(L(`Eso sí, ${mejor.nombre} ${mejor.aviso}.`, `One catch: ${mejor.nombre} ${mejor.aviso}.`));
  if (mejor.vps)
    alt.push(L(`Ojo: ${mejor.nombre} es un VPS, o sea que el servidor lo instalas y lo mantienes tú.`,
               `Heads up: ${mejor.nombre} is a VPS, so you install and maintain the server yourself.`));
  const largo = [...validos].sort((a, b) => a.eurMes - b.eurMes)[0];
  if (largo && largo.id !== mejor.id)
    alt.push(L(`Si acabáis alargándolo, el más barato mes a mes es <b>${largo.nombre}</b>, a ${eur(largo.eurMes)}.`,
               `If you end up keeping it, the cheapest month to month is <b>${largo.nombre}</b>, at ${eur(largo.eurMes)}.`));
  const entradas = validos.filter(f => f.entrada != null).sort((a, b) => a.entrada - b.entrada);
  if (entradas.length && entradas[0].id !== mejor.id)
    alt.push(L(`Si lo que quieres es empezar pagando poco, <b>${entradas[0].nombre}</b> deja el primer mes en ${eur(entradas[0].entrada)}.`,
               `If you just want to start cheap, <b>${entradas[0].nombre}</b> leaves the first month at ${eur(entradas[0].entrada)}.`));

  const socio = partnerActivo() && partnerHost()
    ? `<p class="reco-aviso">${L(`Gano comisión con ${partnerHost().nombre}. Por eso aquí sale el que menos te cuesta, sea quien sea.`,
                                 `I earn a commission with ${partnerHost().nombre}. That's why this box shows whichever costs you least.`)}</p>`
    : "";

  caja.hidden = false;
  caja.innerHTML = `
    <span class="reco-tag">${L("Mi recomendación", "What I'd pick")}</span>
    <p class="reco-txt">${L(
      `Para ${gb} GB y ${tiempo}, yo pillaría <b>${mejor.nombre}</b>: ${porQue}.`,
      `For ${gb} GB and ${tiempo}, I'd go with <b>${mejor.nombre}</b>: ${porQue}.`)}</p>
    ${alt.length ? `<p class="reco-alt">${alt.join(" ")}</p>` : ""}
    ${socio}`;
}

function renderBarras(gb, g){
  const filas = preciosDe(gb, g);
  const tope = (PRESUPUESTOS.find(x => x.id === state.presuId) || {}).max ?? null;
  const validos = filas.filter(f => f.eurMes != null);
  if (!validos.length){ $("#barras").innerHTML = ""; return; }

  const max = Math.max(...validos.map(f => f.eurMes));
  const min = Math.min(...validos.map(f => f.eurMes));

  /* Con 20 hostings en pantalla nadie compara nada: se scrollea y se rinde.
     Se enseñan los primeros y el resto queda a un clic. No se esconde a nadie
     — el botón dice cuántos hay debajo y los ordena igual. */
  const TOPE_VISIBLE = 6;
  const ocultos = Math.max(0, filas.length - TOPE_VISIBLE);

  $("#barras").innerHTML = filas.map((f, i) => {
    const tapada = !state.verTodo && i >= TOPE_VISIBLE ? " barra-oculta" : "";
    if (f.eurMes == null){
      return `<div class="barra no-sirve${tapada}">
                <div class="barra-nom">${nombreConFicha(f)}</div>
                <div class="barra-pista"><span class="barra-nd">${f.nota}</span></div>
                <div class="barra-precio">—</div>
              </div>`;
    }
    const pct = Math.max(4, (f.eurMes / max) * 100);
    const veces = f.eurMes / min;
    // Fuera de presupuesto: se marca, NO se esconde. Esconder opciones sería
    // dejar de ser un comparador.
    const fuera = tope != null && f.eurMes > tope;
    const badge = fuera
      ? `<span class="badge-fuera">${L("se te va del presupuesto", "over your budget")}</span>`
      : (f.eurMes === min
          ? `<span class="badge-mejor">${L("el más barato", "cheapest")}</span>`
          : (veces >= 1.6 ? `<span class="badge-veces">×${veces.toFixed(1)}</span>` : ""));
    // Solo tiene sentido hablar de GB que sobran si el host publica GB.
    // Realms vende "11 slots" y no dice la RAM: ahí no se compara nada.
    const enGB = f.da && /GB$/.test(f.da) ? parseInt(f.da) : null;
    const aviso = f.vps
      ? `<span class="barra-vps">${L("lo montas tú (VPS)", "you set it up (VPS)")}</span>` : "";
    const enPeriodo = (f.coste != null && f.meses > 1)
      ? `<span class="barra-total">${L(`${f.meses} meses: ${eur(f.coste)}`, `${f.meses} months: ${eur(f.coste)}`)}</span>` : "";
    const sobra = enGB && enGB > gb
      ? `<span class="barra-sobra">${L(`te sobran ${enGB - gb} GB`, `${enGB - gb} GB to spare`)}</span>` : "";
    return `<div class="barra${f.destacado ? " destacada" : ""}${fuera ? " fuera" : ""}${tapada}" title="${f.nota || ""}">
              <div class="barra-nom">${nombreConFicha(f)}<small>${L("te da", "gives you")} ${f.da} ${sobra} ${aviso} ${enPeriodo}</small></div>
              <div class="barra-pista">
                <div class="barra-fill" style="width:0" data-w="${pct}"></div>
                ${badge}
              </div>
              <div class="barra-precio">${eur(f.eurMes)}</div>
            </div>`;
  }).join("") + (ocultos && !state.verTodo
    ? `<button type="button" class="ver-todos" id="verTodos">
         ${L(`Ver los otros ${ocultos} hostings`, `See the other ${ocultos} hosts`)}
       </button>`
    : "");

  // Resumen de presupuesto: cuántas opciones te caben y cuál es la mejor
  let resumenPresu = "";
  if (tope != null){
    const caben = validos.filter(f => f.eurMes <= tope);
    resumenPresu = EN
      ? (caben.length
        ? `<div class="presu-ok"><strong>With €${tope}/month you have ${caben.length === 1
             ? "1 option" : `${caben.length} options`}.</strong>
           ${caben.length === 1 ? "It's" : "The best:"}
           ${caben[0].nombre} for ${eur(caben[0].eurMes)}.</div>`
        : `<div class="presu-ko"><strong>€${tope}/month isn't enough for any of them.</strong>
           The cheapest for ${gb} GB is ${eur(validos[0].eurMes)}
           (${validos[0].nombre}). Raise the budget, or cut players or mods.</div>`)
      : (caben.length
        ? `<div class="presu-ok"><strong>Con ${tope} €/mes te ${caben.length === 1
             ? "llega 1 opción" : `llegan ${caben.length} opciones`}.</strong>
           ${caben.length === 1 ? "Es" : "La mejor:"}
           ${caben[0].nombre} por ${eur(caben[0].eurMes)}.</div>`
        : `<div class="presu-ko"><strong>Con ${tope} €/mes no te llega ninguna.</strong>
           La más barata para ${gb} GB son ${eur(validos[0].eurMes)}
           (${validos[0].nombre}). O subes el presupuesto, o bajáis de jugadores o de mods.</div>`);
  }
  document.querySelectorAll(".presu-ok,.presu-ko").forEach(e => e.remove());
  if (resumenPresu) $("#barras").insertAdjacentHTML("afterend", resumenPresu);

  /* Quien tiene descuento de entrada aparece en las barras con su precio
     recurrente, que es el justo para compararlo con los demás. Pero si su
     primer mes es el más barato de todos, hay que decirlo — y decir también
     a cuánto renueva, que es la otra mitad del dato. */
  document.querySelectorAll(".entrada-aviso").forEach(e => e.remove());
  const conEntrada = validos.filter(f => f.entrada != null)
                            .sort((a, b) => a.entrada - b.entrada)[0];
  if (conEntrada && conEntrada.entrada < validos[0].eurMes){
    const porAno = [...validos].sort((a, b) => a.anual - b.anual)[0];
    $("#barras").insertAdjacentHTML("afterend",
      L(`<div class="entrada-aviso">
         <strong>Para empezar, nadie es más barato:</strong> ${conEntrada.nombre} deja
         ${conEntrada.entradaQue} en <strong>${eur(conEntrada.entrada)}</strong>
         (−${conEntrada.entradaPct} %). Después, tarifa normal: ${eur(conEntrada.eurMes)} al mes.
         Si el servidor va a estar todo el año, lo que menos te cuesta en doce meses es
         <strong>${porAno.nombre}</strong> (${eur(porAno.anual)}).
       </div>`,
       `<div class="entrada-aviso">
         <strong>Nobody is cheaper to start with:</strong> ${conEntrada.nombre} brings
         ${conEntrada.entradaQue} down to <strong>${eur(conEntrada.entrada)}</strong>
         (−${conEntrada.entradaPct}%). After that, the normal rate: ${eur(conEntrada.eurMes)} a month.
         If the server will run all year, the cheapest over twelve months is
         <strong>${porAno.nombre}</strong> (${eur(porAno.anual)}).
       </div>`));
  }

  // Ahora sí: se les pone el ancho en el frame siguiente y crecen a la vista
  requestAnimationFrame(() => {
    $("#barras").querySelectorAll(".barra-fill").forEach(el => {
      el.style.width = el.dataset.w + "%";
    });
  });

  $("#barrasNota").innerHTML = L(
    `Precio mensual de <strong>${gb} GB</strong> en cada hosting, en euros. ` +
    `Los que cobran en dólares están convertidos a 1 $ = ${CAMBIO_USD_EUR} €. ` +
    `Cada precio está comprobado a mano en la web de ese hosting.`,
    `Monthly price of <strong>${gb} GB</strong> on each host, in euros. ` +
    `Hosts that charge in dollars are converted at $1 = €${CAMBIO_USD_EUR}. ` +
    `Every price was checked by hand on that host's website.`);
}

/* El nombre lleva a su ficha. Es lo que espera cualquiera que use un comparador:
   ves un precio que te descoloca y quieres leer por qué sin perder el resultado. */
function nombreConFicha(f){
  if (!f.ficha) return f.nombre;
  // el logo vive en /logos/<slug>.png, el mismo slug que la ficha
  const slug = f.ficha.split("/").filter(Boolean).pop();
  const logo = `<img class="h-logo" src="/logos/${slug}.png" alt="" width="16" height="16" loading="lazy">`;
  return `<a class="h-ficha" href="${EN ? "/en" + f.ficha : f.ficha}">${logo}${f.nombre}</a>`;
}

/* La tabla es el detalle del gráfico: los mismos hosts, en el mismo orden y
   con los mismos precios en euros, más la letra pequeña de cada modelo. */
function renderTable(gb, g){
  const filas = preciosDe(gb, g);

  const rows = filas.map(f => {
    if (f.eurMes == null){
      return `<tr>
        <td>${nombreConFicha(f)}</td><td>—</td>
        <td class="price">${L("No te sirve", "Won't do")}</td><td class="price">—</td>
        <td>${f.nota || ""}</td></tr>`;
    }

    let precio = `${eur(f.eurMes)}/${L("mes", "mo")}`;
    if (f.entrada != null)
      precio += `<small class="td-entrada">${eur(f.entrada)} ${f.entradaQue}</small>`;
    let letra  = f.nota || "";

    // Si es el partner y tiene código, se dice en su fila (y solo en la suya)
    if (esPartner(f.id) && CONFIG.partner.codigo)
      letra = `${letra} · ${L("Código", "Code")} <strong>${CONFIG.partner.codigo}</strong>`;

    return `<tr class="${f.destacado ? "hl" : ""}">
      <td>${nombreConFicha(f)}</td>
      <td>${f.da}</td>
      <td class="price">${precio}</td>
      <td class="price">${eur(f.anual)}</td>
      <td>${letra}</td></tr>`;
  });

  $("#cmpBody").innerHTML = rows.join("");
  $("#cmpNote").innerHTML = L(
    `La columna <strong>«12 meses»</strong> es lo que llevas gastado al año de estar, ` +
    `contando el descuento de entrada donde lo hay y la tarifa normal el resto de meses. ` +
    `Precios comprobados a mano el ${CONFIG.pricesChecked} y pasados a euros. ` +
    `Los hosts los cambian sin avisar: si ves algo distinto al entrar, manda el aviso y lo corrijo.`,
    `The <strong>“12 months”</strong> column is what you'll have spent after a year, ` +
    `counting the entry discount where there is one and the normal rate for the rest. ` +
    `Prices checked by hand on ${CONFIG.pricesChecked} and converted to euros. ` +
    `Hosts change them without notice: if you see something different, let me know and I'll fix it.`);
}

function renderAll(){
  renderControls();
  renderResult();
}

/* ===== Eventos ===== */

document.addEventListener("click", e => {
  const mBtn = e.target.closest("[data-mod]");
  if (mBtn){ state.modId = mBtn.dataset.mod; renderAll(); return escribirURL(); }

  const xBtn = e.target.closest("[data-extra]");
  if (xBtn){ state.extraId = xBtn.dataset.extra; renderAll(); return escribirURL(); }

  const tBtn = e.target.closest("[data-tiempo]");
  if (tBtn){ state.tiempoId = tBtn.dataset.tiempo; renderAll(); return escribirURL(); }

  const bBtn = e.target.closest("[data-presu]");
  if (bBtn){ state.presuId = bBtn.dataset.presu; renderAll(); return escribirURL(); }

  if (e.target.closest("#verTodos")){ state.verTodo = true; return renderAll(); }

  if (e.target.closest("#copiar")) return copiarEnlace();
});

$("#players").addEventListener("input", e => {
  state.players = +e.target.value;
  $("#pnum").textContent = jugTxt(state.players);
  renderResult();
});
// La URL se actualiza al soltar el ratón, no en cada píxel del deslizador
$("#players").addEventListener("change", escribirURL);

async function copiarEnlace(){
  const btn = $("#copiar");
  const url = enlaceResultado();
  try {
    await navigator.clipboard.writeText(url);
  } catch {
    // navegadores viejos o sin permiso de portapapeles
    const t = document.createElement("textarea");
    t.value = url; document.body.appendChild(t); t.select();
    try { document.execCommand("copy"); } catch {}
    t.remove();
  }
  const antes = btn.textContent;
  btn.textContent = L("¡Copiado!", "Copied!");
  btn.classList.add("copiado");
  setTimeout(() => { btn.textContent = antes; btn.classList.remove("copiado"); }, 1800);
}

/* ---- Tarjeta de ejemplo del hero ----------------------------------------
   Enseña un precio real antes de que el visitante toque nada. Usa el mismo
   motor que la calculadora a propósito: si algún día cambian los precios,
   esta tarjeta cambia sola y no se queda mintiendo en la portada. */
function pintarHeroDemo(){
  const caja = $("#heroDemo");
  if (!caja) return;

  const g = game();

  const JUGADORES_DEMO = 30;
  const gb = calcRam(g, JUGADORES_DEMO, "heavy", "10");
  const filas = preciosDe(gb, g, JUGADORES_DEMO).filter(f => f.eurMes != null).slice(0, 4);
  if (!filas.length) return;

  $("#hdRam").textContent = gb;
  $("#hdLista").innerHTML = filas.map((f, i) => `
    <li class="${i === 0 ? "gana" : ""}">
      <span>${f.nombre}</span><b>${eur(f.eurMes)}</b>
    </li>`).join("");

  const caro = preciosDe(gb, g, JUGADORES_DEMO).filter(f => f.eurMes != null).pop();
  const veces = caro ? (caro.eurMes / filas[0].eurMes).toFixed(1) : null;
  $("#hdPie").innerHTML = veces
    ? L(`El mismo servidor de ${gb} GB cuesta <strong>${veces} veces más</strong>
       en el hosting más caro de la comparativa. Por eso existe esta web.`,
       `The same ${gb} GB server costs <strong>${veces} times more</strong>
       at the most expensive host in the comparison. That's why this site exists.`)
    : L(`Precios comprobados a mano el ${CONFIG.pricesChecked}.`,
        `Prices checked by hand on ${CONFIG.pricesChecked}.`);
}

// Arranque
// Empresas, no gamas: PebbleHost Budget y Premium cuentan como un hosting
document.querySelectorAll("[data-n-hosts]").forEach(e => {
  e.textContent = new Set(HOSTS.map(h => h.ficha || h.id)).size;
});
const desdeURL = leerURL();
if (desdeURL.tiempoId && TIEMPOS.some(x => x.id === desdeURL.tiempoId)) {
  state.tiempoId = desdeURL.tiempoId;
}
selectGame(state.gameId, desdeURL);
pintarHeroDemo();
