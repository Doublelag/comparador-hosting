/* =========================================================================
   AVISO DE PROMO DEL PARTNER — solo en la página del juego que la tenga
   =========================================================================
   Hasta el 11-sep-2026 esto era el pop-up de "Valheim a 1 € en DatHost", con
   el nombre, el precio y la comparación con los rivales escritos a mano. Ahora
   lee la promo del partner de hosts.js (partner.promo) y, sin partner activo,
   no hace nada.

   Un pop-up mal hecho espanta. Este intenta no serlo:
   · Solo sale si la promo es de Minecraft (promo.juegos).
   · Se apaga solo cuando caduca (lee la fecha de hosts.js).
   · Sin letra pequeña no sale: una promo sin su "después son X €" es justo
     lo que esta web critica.
   · Aparece a los 1,2 s, no de golpe encima de la carga.
   · Si lo cierras, no vuelve (se recuerda en el navegador).
   · Se cierra con Escape, con la X y pulsando fuera.

   Necesita window.DATOS (hosts.js) y app.js cargados antes.
   ========================================================================= */

(function(){
  const D = window.DATOS;
  const cfg = D && D.partner;
  if (!cfg || !cfg.activo || !cfg.hostId || !cfg.enlace) return;
  const promo = cfg.promo;
  if (!promo || !promo.letra) return;

  const juego = "minecraft";                      // la web es solo de Minecraft
  if (!(promo.juegos || []).includes(juego)) return;

  const hoy = new Date().toISOString().slice(0, 10);
  if (hoy > promo.hasta) return;

  const host = (D.hosts || []).find(h => h.id === cfg.hostId);
  if (!host || !(host.precios || {})[juego]) return;   // no vende ese juego

  const clave = "promo-vista-" + cfg.hostId + "-" + juego + "-" + promo.hasta;
  try { if (localStorage.getItem(clave)) return; } catch {}

  // canal de entrada (?cid=YT…) + sitio del botón, igual que el resto de la web
  let canal = null;
  const enUrl = new URLSearchParams(location.search).get("cid");
  if (enUrl && /^[A-Za-z0-9_-]{1,20}$/.test(enUrl)) canal = enUrl.toUpperCase();
  else { try { canal = sessionStorage.getItem("cid"); } catch {} }
  const marca = canal ? canal + "-POPUP" : "POPUP";

  const slug = (cfg.slugs || {})[juego] || juego;
  let enlace = cfg.enlace.replace("{juego}", slug);
  enlace += (enlace.includes("?") ? "&" : "?") + "cid=" + marca;

  const [, m, d] = promo.hasta.split("-");
  const meses = ["enero","febrero","marzo","abril","mayo","junio","julio",
                 "agosto","septiembre","octubre","noviembre","diciembre"];
  const fecha = parseInt(d, 10) + " de " + meses[parseInt(m, 10) - 1];

  // Todo lo que viene de hosts.js se escapa antes de meterlo en el HTML
  const esc = t => String(t == null ? "" : t)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

  const caja = document.createElement("div");
  caja.className = "promo-fondo";
  caja.innerHTML = `
    <div class="promo" role="dialog" aria-modal="true" aria-labelledby="promo-tit">
      <button class="promo-x" aria-label="Cerrar">&times;</button>
      <span class="promo-tag">Solo hasta el ${fecha}</span>
      <h2 id="promo-tit">${esc(promo.titulo)}</h2>
      ${promo.texto ? `<p class="promo-txt">${esc(promo.texto)}</p>` : ""}
      <p class="promo-pie">${esc(promo.letra)}</p>
      <a class="cta" href="${esc(enlace)}" rel="sponsored nofollow noopener" target="_blank">
        Ver la oferta en ${esc(host.nombre)}
      </a>
      <button class="promo-no">No, gracias</button>
      <p class="promo-aviso">
        Enlace de afiliado: gano una comisión y a ti no te cuesta más.
      </p>
    </div>`;

  function cerrar(){
    caja.classList.remove("visible");
    try { localStorage.setItem(clave, "1"); } catch {}
    setTimeout(() => caja.remove(), 220);
    document.removeEventListener("keydown", porTecla);
  }
  function porTecla(e){ if (e.key === "Escape") cerrar(); }

  caja.addEventListener("click", e => {
    if (e.target === caja || e.target.closest(".promo-x, .promo-no")) cerrar();
    if (e.target.closest(".cta")) { try { localStorage.setItem(clave, "1"); } catch {} }
  });

  setTimeout(() => {
    document.body.appendChild(caja);
    void caja.offsetHeight;              // fuerza el reflow: la transicion arranca
    caja.classList.add("visible");       // (rAF no corre si la pestana esta de fondo)
    document.addEventListener("keydown", porTecla);
    caja.querySelector(".promo-x").focus();
  }, 1200);
})();
