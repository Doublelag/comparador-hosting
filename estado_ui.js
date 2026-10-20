// ¿Está abierto ChorizoSMP ahora? Lee /api/server, que responde el Worker
// (es él quien pregunta a mcsrvstat una vez por minuto): el navegador del
// visitante no sale de montatuserver.com. Si no se puede saber, se dice que
// no se ha podido comprobar: nunca se inventa.
//
// Marcado: <span class="estado" data-abierto="Abierto · {n} jugando"
//                data-cerrado="…" data-nose="…">Comprobando…</span>
(function () {
  var cajas = document.querySelectorAll(".estado[data-abierto]");
  if (!cajas.length) return;
  fetch("/api/server", { cache: "no-store" })
    .then(function (r) { return r.ok ? r.json() : null; })
    .then(function (d) {
      cajas.forEach(function (caja) {
        var T = caja.dataset;
        if (!d || d.desconocido) {
          caja.className = "estado"; caja.textContent = T.nose; return;
        }
        if (d.online) {
          caja.className = "estado on";
          caja.textContent = T.abierto.replace("{n}", d.jugadores || 0);
        } else {
          caja.className = "estado off";
          caja.textContent = T.cerrado;
        }
      });
    })
    .catch(function () {
      cajas.forEach(function (caja) { caja.className = "estado"; caja.textContent = caja.dataset.nose; });
    });
})();
