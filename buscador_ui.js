/* =========================================================================
   BUSCADOR DE LA CABECERA
   =========================================================================
   El índice (window.INDICE) lo genera build.py leyendo los <title> de todas
   las páginas y se escribe en indice.js. Así no hay que mantener una lista a
   mano: cada página nueva aparece sola en el buscador.

   El índice NO se carga con la página: son 10 KB que casi nadie llega a usar.
   Se pide la primera vez que alguien toca el buscador, y para entonces ya está
   antes de que termine de escribir la primera palabra.
   ========================================================================= */

(function(){
  const caja = document.getElementById("buscador");
  if (!caja) return;

  const EN = document.documentElement.lang === "en";
  const suyo = e => e.u.startsWith("/en/") === EN;       // cada idioma, sus páginas
  let indice = (window.INDICE || []).filter(suyo);
  let pidiendo = null;

  function cargarIndice(){
    if (indice.length) return Promise.resolve(indice);
    if (pidiendo) return pidiendo;
    pidiendo = new Promise(listo => {
      const s = document.createElement("script");
      s.src = (document.currentScript && document.currentScript.dataset.indice) || "/indice.js";
      s.onload = () => { indice = (window.INDICE || []).filter(suyo); listo(indice); };
      s.onerror = () => listo([]);
      document.head.appendChild(s);
    });
    return pidiendo;
  }

  const input = caja.querySelector("input");
  const panel = caja.querySelector(".bs-panel");
  let activo = -1, resultados = [];

  // Quita acentos: buscar "pebble" debe encontrar "PebbleHost", y "cuanta"
  // debe encontrar "cuánta". En español esto no es opcional.
  const limpiar = s => s.toLowerCase()
    .normalize("NFD").replace(/[̀-ͯ]/g, "");

  function buscar(q){
    const t = limpiar(q.trim());
    if (!t) return [];
    const palabras = t.split(/\s+/);
    return indice
      .map(e => {
        const heno = limpiar(e.t + " " + e.k);
        // todas las palabras tienen que aparecer
        if (!palabras.every(p => heno.includes(p))) return null;
        // puntúa: mejor si empieza por lo buscado, y los hostings primero
        let pts = 0;
        if (limpiar(e.t).startsWith(t)) pts += 10;
        if (heno.indexOf(t) === 0) pts += 5;
        if (e.c === "hosting") pts += 3;
        return { e, pts };
      })
      .filter(Boolean)
      .sort((a, b) => b.pts - a.pts)
      .slice(0, 8)
      .map(x => x.e);
  }

  function pintar(){
    if (!resultados.length){
      panel.innerHTML = input.value.trim()
        ? '<div class="bs-vacio">Nada por aquí. Prueba con el nombre de un hosting.</div>'
        : "";
      panel.hidden = !input.value.trim();
      return;
    }
    panel.innerHTML = resultados.map((e, i) => `
      <a class="bs-item${i === activo ? " on" : ""}" href="${e.u}" role="option">
        <span class="bs-cat">${e.c}</span>
        <span class="bs-tit">${e.t}</span>
      </a>`).join("");
    panel.hidden = false;
  }

  function cerrar(){ panel.hidden = true; activo = -1; }

  function refrescar(){
    resultados = buscar(input.value);
    activo = resultados.length ? 0 : -1;
    pintar();
  }

  input.addEventListener("input", () => {
    if (!indice.length) cargarIndice().then(refrescar);
    refrescar();
  });

  // Al enfocar ya se va pidiendo: cuando termine de escribir, está.
  input.addEventListener("focus", cargarIndice, { once: true });

  input.addEventListener("keydown", e => {
    if (e.key === "Escape") return (input.blur(), cerrar());
    if (!resultados.length) return;
    if (e.key === "ArrowDown" || e.key === "ArrowUp"){
      e.preventDefault();
      activo = (activo + (e.key === "ArrowDown" ? 1 : -1) + resultados.length) % resultados.length;
      pintar();
    } else if (e.key === "Enter" && resultados[activo]){
      location.href = resultados[activo].u;
    }
  });

  input.addEventListener("focus", () => { if (resultados.length) pintar(); });
  document.addEventListener("click", e => { if (!caja.contains(e.target)) cerrar(); });

  // "/" enfoca el buscador, como en GitHub. Cuesta nada y se agradece.
  document.addEventListener("keydown", e => {
    if (e.key === "/" && !/^(INPUT|TEXTAREA)$/.test(document.activeElement.tagName)){
      e.preventDefault(); input.focus();
    }
  });
})();

/* En movil el menu es una fila de pastillas que se desliza, y la de la seccion
   en la que estas puede quedar fuera de vista. Se acerca sin animacion: es el
   estado inicial de la pagina, no un movimiento que el usuario haya pedido. */
(function(){
  const activa = document.querySelector('.nav a[aria-current]');
  const nav = activa && activa.parentElement;
  if (!nav) return;
  // Hay que esperar a las fuentes: con la tipografia del sistema las pastillas
  // miden menos, parece que caben, y luego cargan Inter/Space Grotesk y ya no.
  const acercar = () => {
    if (nav.scrollWidth <= nav.clientWidth) return;
    nav.scrollLeft = activa.offsetLeft - 4;
  };
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(acercar);
  else acercar();
})();


/* =========================================================================
   DE QUE CANAL VIENE LA VENTA
   =========================================================================
   Las paginas escritas por Python (comparativas, ofertas, fichas, guias) llevan
   el enlace del partner ya puesto en el HTML, con una etiqueta que dice DONDE
   estaba el boton: cid=BANNER-COMP, cid=POPUP, cid=OFERTAS...

   Eso esta bien para saber que boton funciona, pero se comia el dato de por
   donde habia entrado la persona. Si llegaba desde un video con ?cid=YT y
   pinchaba en la comparativa, la venta figuraba como BANNER-COMP y no habia
   forma de saber que la habia traido YouTube.

   Aqui se juntan los dos: cid=YT-BANNER-COMP. Asi en el panel de DatHost se
   puede agrupar por canal (lo de antes del guion) y por boton (lo de despues).

   Este archivo se carga en todas las paginas; app.js solo en las calculadoras.
   ========================================================================= */
(function(){
  let canal = null;
  const p = new URLSearchParams(location.search);
  const dela_url = p.get("cid") || p.get("utm_source");
  if (dela_url && /^[A-Za-z0-9_-]{1,20}$/.test(dela_url)){
    canal = dela_url.toUpperCase();
    try { sessionStorage.setItem("cid", canal); } catch {}
  } else {
    try { canal = sessionStorage.getItem("cid"); } catch {}
  }
  if (!canal) return;                       // visita directa: se deja como esta

  // Cualquier enlace de afiliado de la pagina, sea del partner que sea: se
  // reconocen por rel=sponsored, que es como los marca partner.py.
  document.querySelectorAll('a[rel~="sponsored"]').forEach(a => {
    let u;
    try { u = new URL(a.href); } catch { return; }
    const sitio = u.searchParams.get("cid");
    if (sitio && sitio.startsWith(canal)) return;          // ya marcado
    u.searchParams.set("cid", sitio ? canal + "-" + sitio : canal);
    a.href = u.toString();
  });
})();


/* =========================================================================
   TEMA NOCHE / CLARO
   =========================================================================
   Noche es el de por defecto. El botón cambia a claro y lo recuerda en el
   navegador. El script en línea del <head> lo aplica antes de pintar, así que
   no hay parpadeo; esto solo gestiona el clic.
   ========================================================================= */
(function(){
  const btn = document.querySelector(".tema-btn");
  if (!btn) return;
  const raiz = document.documentElement;
  function rotular(){
    const claro = raiz.dataset.theme === "claro";
    btn.setAttribute("aria-label", claro ? btn.dataset.noche : btn.dataset.claro);
    btn.setAttribute("title", claro ? btn.dataset.noche : btn.dataset.claro);
  }
  btn.addEventListener("click", () => {
    const claro = raiz.dataset.theme !== "claro";
    if (claro) raiz.dataset.theme = "claro"; else delete raiz.dataset.theme;
    try { localStorage.setItem("tema", claro ? "claro" : "noche"); } catch {}
    rotular();
  });
  rotular();
})();

/* =========================================================================
   MENÚ DE TRES RAYAS (móvil)
   ========================================================================= */
(function(){
  const btn = document.querySelector(".menu-btn");
  const cab = document.querySelector(".site-head");
  if (!btn || !cab) return;
  function poner(abierto){
    cab.classList.toggle("abierto", abierto);
    btn.setAttribute("aria-expanded", abierto);
    btn.setAttribute("aria-label", abierto ? btn.dataset.cerrar : btn.dataset.abrir);
  }
  btn.addEventListener("click", () => poner(btn.getAttribute("aria-expanded") !== "true"));
  // se cierra al elegir un enlace, con Escape y al tocar fuera
  cab.addEventListener("click", e => { if (e.target.closest(".nav a")) poner(false); });
  document.addEventListener("keydown", e => { if (e.key === "Escape") poner(false); });
  document.addEventListener("click", e => { if (!cab.contains(e.target)) poner(false); });
  // si se agranda la ventana con el menú abierto, que no se quede colgado
  matchMedia("(min-width: 881px)").addEventListener("change", e => { if (e.matches) poner(false); });
})();


/* Botones de copiar la IP del server (portada y página de ChorizoSMP) */
document.addEventListener("click", async e => {
  const b = e.target.closest("[data-copiar],[data-copiar-ip]");
  if (!b) return;
  const texto = b.dataset.copiar ||
    (b.closest(".acciones, .ip-fila") || document).querySelector(".ip-val").textContent.trim();
  try { await navigator.clipboard.writeText(texto); } catch {}
  const antes = b.textContent; b.textContent = b.dataset.ok || "OK";
  setTimeout(() => { b.textContent = antes; }, 1600);
});
