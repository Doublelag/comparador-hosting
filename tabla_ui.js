/* =========================================================================
   TABLAS ORDENABLES
   =========================================================================
   Cualquier tabla con class="ordenable" se puede ordenar pulsando sus
   cabeceras. Es lo que espera cualquiera que entre a un comparador, y no
   hacerlo obliga a leer nueve filas para encontrar la más barata.

   Las celdas se ordenan por el número que contengan (precios, cantidades) y,
   si no hay número, alfabéticamente. Las que no tienen dato ("No lo ofrece")
   van siempre al final: no son "cero", son "no aplica".
   ========================================================================= */

(function(){
  document.querySelectorAll("table.ordenable").forEach(tabla => {
    const cuerpo = tabla.tBodies[0];
    if (!cuerpo) return;

    const numero = celda => {
      const t = celda.innerText.replace(/\./g, "").replace(",", ".");
      const m = t.match(/-?\d+(\.\d+)?/);
      return m ? parseFloat(m[0]) : null;
    };

    tabla.querySelectorAll("thead th").forEach((th, col) => {
      if (!th.innerText.trim()) return;         // la columna del botón, no
      th.classList.add("th-orden");
      th.tabIndex = 0;
      th.setAttribute("role", "button");

      let asc = true;
      const ordenar = () => {
        const filas = [...cuerpo.rows];
        filas.sort((a, b) => {
          const ca = a.cells[col], cb = b.cells[col];
          const na = numero(ca), nb = numero(cb);
          // sin dato siempre al final, ordene como ordene
          if (na === null && nb === null) return 0;
          if (na === null) return 1;
          if (nb === null) return -1;
          return asc ? na - nb : nb - na;
        });
        filas.forEach(f => cuerpo.appendChild(f));

        tabla.querySelectorAll("thead th").forEach(x => {
          x.removeAttribute("data-orden");
          x.removeAttribute("aria-sort");
        });
        th.dataset.orden = asc ? "asc" : "desc";
        th.setAttribute("aria-sort", asc ? "ascending" : "descending");
        asc = !asc;
      };

      th.addEventListener("click", ordenar);
      th.addEventListener("keydown", e => {
        if (e.key === "Enter" || e.key === " "){ e.preventDefault(); ordenar(); }
      });
    });
  });

  /* Copiar el código de una oferta al portapapeles. Es lo que va a hacer
     todo el que llegue a esa página, así que mejor que sea un clic. */
  document.querySelectorAll(".of-codigo").forEach(caja => {
    const code = caja.querySelector("code");
    if (!code) return;
    caja.classList.add("copiable");
    caja.title = "Pulsa para copiar";
    caja.addEventListener("click", async () => {
      try { await navigator.clipboard.writeText(code.innerText.trim()); }
      catch {
        const t = document.createElement("textarea");
        t.value = code.innerText.trim();
        document.body.appendChild(t); t.select();
        try { document.execCommand("copy"); } catch {}
        t.remove();
      }
      caja.classList.add("copiado");
      setTimeout(() => caja.classList.remove("copiado"), 1600);
    });
  });
})();
