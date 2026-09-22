/* =========================================================================
   FILTROS DE LA TABLA DE HOSTINGS
   =========================================================================
   Idea prestada de los comparadores de otros sectores — idealo, Rastreator,
   los de luz: ahí nadie te enseña 16 filas y te desea suerte, te dejan
   quitarte de encima lo que no te sirve en un clic.

   Aquí los filtros son solo DATOS DUROS que ya están en hosts.js (cómo cobra,
   cuánto cuesta el giga, si tiene descuento de entrada). Nada de "el mejor" o
   "recomendado", que es donde los comparadores se vuelven publicidad.

   Se apoya en los data-* que escribe hostings.py en cada fila. Si no hay tabla
   con filtros en la página, no hace nada.
   ========================================================================= */

const EN_F = document.documentElement.lang === "en";
const LF = (es, en) => EN_F ? en : es;

/* ---- 1. La tabla de /hosting/ ---- */
(function(){
  const tabla = document.querySelector("table[data-filtrable]");
  const caja  = document.getElementById("filtros");
  if (!tabla || !caja) return;

  const filas = [...tabla.tBodies[0].rows];

  const FILTROS = [
    { id: "barato",  texto: LF("Menos de 1,50 € el GB", "Under €1.50 per GB"),
      pasa: f => +f.dataset.porgb > 0 && +f.dataset.porgb < 1.5 },
    { id: "limpio",  texto: LF("Sin descuento de entrada", "No entry discount"),
      pasa: f => f.dataset.entrada !== "si" },
    { id: "porgb",   texto: LF("Pagas por gigabyte", "Pay per gigabyte"),
      pasa: f => f.dataset.modelo === "porGB" },
    { id: "cerrado", texto: LF("Plan cerrado", "Fixed plans"),
      pasa: f => f.dataset.modelo === "plano" || f.dataset.modelo === "tabla" },
  ];

  const activos = new Set();

  caja.innerHTML = FILTROS.map(f =>
    `<button type="button" class="filtro" data-f="${f.id}" aria-pressed="false">${f.texto}</button>`
  ).join("") + `<span class="filtro-cuenta" id="filtroCuenta"></span>`;

  function aplicar(){
    let visibles = 0;
    for (const fila of filas){
      const pasa = [...activos].every(id => FILTROS.find(x => x.id === id).pasa(fila));
      fila.hidden = !pasa;
      if (pasa) visibles++;
    }
    const cuenta = document.getElementById("filtroCuenta");
    cuenta.textContent = activos.size
      ? LF(`${visibles} de ${filas.length} hostings`, `${visibles} of ${filas.length} hosts`)
      : LF(`${filas.length} hostings`, `${filas.length} hosts`);

    // Si un filtro deja la tabla vacía hay que decirlo, no dejar un hueco raro
    let vacio = document.getElementById("filtroVacio");
    if (!visibles){
      if (!vacio){
        vacio = document.createElement("p");
        vacio.id = "filtroVacio";
        vacio.className = "tbl-note";
        vacio.textContent = LF("Con esos filtros no queda ninguno. Quita alguno y vuelve a mirar.",
                               "No host matches those filters. Remove one and look again.");
        tabla.closest(".table-wrap").after(vacio);
      }
    } else if (vacio){
      vacio.remove();
    }
  }

  caja.addEventListener("click", e => {
    const b = e.target.closest("[data-f]");
    if (!b) return;
    const id = b.dataset.f;
    if (activos.has(id)) activos.delete(id); else activos.add(id);
    b.setAttribute("aria-pressed", activos.has(id));
    aplicar();
  });

  aplicar();
})();

/* ---- 2. Las tarjetas de /ofertas/ ----
   Aquí el filtro que de verdad quiere la gente es "enséñame solo las que
   valen la pena". Las otras no se borran: se pueden volver a ver, porque una
   oferta marcada como trampa también es información útil. */
(function(){
  const caja = document.getElementById("filtros-ofertas");
  if (!caja) return;
  const tarjetas = [...document.querySelectorAll(".oferta")];
  if (!tarjetas.length) return;

  const FILTROS = [
    { id: "buena",  texto: LF("Solo las que valen la pena", "Only the good ones"),
      pasa: t => t.dataset.veredicto === "buena" },
    { id: "codigo", texto: LF("Con código de descuento", "With a discount code"),
      pasa: t => t.dataset.codigo === "si" },
  ];
  const activos = new Set();

  caja.innerHTML = FILTROS.map(f =>
    `<button type="button" class="filtro" data-f="${f.id}" aria-pressed="false">${f.texto}</button>`
  ).join("") + `<span class="filtro-cuenta" id="ofertasCuenta"></span>`;

  function aplicar(){
    let visibles = 0;
    for (const t of tarjetas){
      const pasa = [...activos].every(id => FILTROS.find(x => x.id === id).pasa(t));
      t.hidden = !pasa;
      if (pasa) visibles++;
    }
    document.getElementById("ofertasCuenta").textContent =
      activos.size ? LF(`${visibles} de ${tarjetas.length} ofertas`, `${visibles} of ${tarjetas.length} deals`)
                   : LF(`${tarjetas.length} ofertas`, `${tarjetas.length} deals`);
  }

  caja.addEventListener("click", e => {
    const b = e.target.closest("[data-f]");
    if (!b) return;
    const id = b.dataset.f;
    if (activos.has(id)) activos.delete(id); else activos.add(id);
    b.setAttribute("aria-pressed", activos.has(id));
    aplicar();
  });

  aplicar();
})();
