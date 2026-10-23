/* Aparición al bajar (23-oct-2026).

   Las cosas entran según llegan a la pantalla: suben un poco, se enfocan y
   se escalonan dentro de su grupo. El titular entra palabra a palabra. Copia
   la técnica de excellentiaclub.com (la web de Óscar): una sola curva para
   todo, cubic-bezier(.16,1,.3,1), que arranca rápido y frena largo.

   No hay que marcar nada en el HTML: este script recorre <main> y decide él
   qué es un bloque y qué es una rejilla. Así vale para las 96 páginas sin
   tocar ni un generador. Si una página nueva se ve rara, se mira aquí.

   Solo corre si <head> puso la clase "anim" (sin movimiento reducido y con
   IntersectionObserver). Sin ella la web se ve entera y quieta. */
(function () {
  var raiz = document.documentElement;
  if (!raiz.classList.contains("anim")) return;
  var main = document.querySelector("main");
  if (!main) { raiz.classList.add("anim-listo"); return; }

  var DURA = 700;                 // ms, igual que en styles.css
  var PASO = 0.07, TOPE = 0.42;   // escalón entre lo que entra a la vez y retraso máximo (s)
  var NO_TOCAR = "script,style,template,link,noscript,br,hr";

  function visible(el) {
    return el.offsetParent !== null || getComputedStyle(el).position === "fixed";
  }

  // Una rejilla es un contenedor flex/grid con 3+ hijos del mismo tipo:
  // tarjetas, pasos, vídeos, cifras... Sus hijos entran uno detrás de otro.
  function esRejilla(el) {
    var h = el.children;
    if (h.length < 3) return false;
    var d = getComputedStyle(el).display;
    if (!/grid|flex/.test(d) && !/^(UL|OL)$/.test(el.tagName)) return false;
    var firma = h[0].tagName + "." + h[0].className;
    for (var i = 1; i < h.length; i++)
      if (h[i].tagName + "." + h[i].className !== firma) return false;
    return true;
  }

  // Envoltorio de maquetación: no tiene texto propio, solo coloca a sus
  // hijos (dos columnas, cabecera de sección...). Se entra dentro.
  function esEnvoltorio(el) {
    if (/^(SECTION|ARTICLE|HEADER)$/.test(el.tagName) || el.classList.contains("wrap")) return true;
    if (el.tagName !== "DIV" || el.children.length < 2 || el.children.length > 5) return false;
    for (var n = el.firstChild; n; n = n.nextSibling)
      if (n.nodeType === 3 && n.textContent.trim()) return false;
    // el bloque de título de una sección (etiqueta + h2 + entradilla)
    if (el.querySelector(":scope>h2,:scope>h3") && !el.className) return true;
    return /grid|flex/.test(getComputedStyle(el).display);
  }

  // El retraso solo se fija a mano en el hero. Lo demás se escalona al entrar,
  // entre lo que asoma a la vez (ver el observador): así en móvil, con todo en
  // una columna, la sexta tarjeta no espera medio segundo estando ya a la vista.
  var marcados = [];
  function marcar(el, retraso, tipo) {
    if (el.matches(NO_TOCAR) || el.classList.contains("rv") || !visible(el)) return;
    el.classList.add("rv");
    if (tipo) el.classList.add(tipo);
    if (retraso) el.style.setProperty("--rv-d", retraso.toFixed(2) + "s");
    marcados.push(el);
  }

  function recorrer(cont, prof) {
    [].slice.call(cont.children).forEach(function (c) {
      if (c.matches(NO_TOCAR) || c.tagName === "H1") return;
      if (esRejilla(c)) {
        [].forEach.call(c.children, function (h) { marcar(h); });
      } else if (prof < 4 && esEnvoltorio(c)) {
        // dos columnas: la de la izquierda entra desde la izquierda y la otra
        // desde la derecha; queda menos «todo sube igual»
        if (c.children.length === 2 && /grid|flex/.test(getComputedStyle(c).display) &&
            !/SECTION|ARTICLE/.test(c.tagName) && !c.classList.contains("wrap") &&
            c.children[0].offsetWidth < c.offsetWidth * .8) {
          var a = c.children[0], b = c.children[1];
          if (esEnvoltorio(a)) recorrer(a, prof + 1); else marcar(a, 0, "rv-izq");
          if (esEnvoltorio(b)) recorrer(b, prof + 1); else marcar(b, 0, "rv-der");
        } else recorrer(c, prof + 1);
      } else {
        var tipo = /^H[2-3]$/.test(c.tagName) ? "rv-foco"
                 : c.classList.contains("sec-eyebrow") ? "rv-barrido" : "";
        marcar(c, 0, tipo);
      }
    });
  }

  // ---- Titular: palabra a palabra -------------------------------------------
  // Se parten solo los nodos de texto; un <em> o <span> dentro (la palabra en
  // degradado) entra entero, para no romperle el background-clip.
  function partir(h1) {
    var n = 0;
    [].slice.call(h1.childNodes).forEach(function (nodo) {
      if (nodo.nodeType === 3) {
        var trozos = nodo.textContent.split(/(\s+)/), frag = document.createDocumentFragment();
        trozos.forEach(function (t) {
          if (!t) return;
          if (/^\s+$/.test(t)) { frag.appendChild(document.createTextNode(t)); return; }
          var s = document.createElement("span");
          s.className = "pal"; s.textContent = t;
          s.style.setProperty("--pd", (n++ * .06).toFixed(2) + "s");
          frag.appendChild(s);
        });
        nodo.parentNode.replaceChild(frag, nodo);
      } else if (nodo.nodeType === 1 && nodo.tagName !== "BR") {
        nodo.classList.add("pal");
        nodo.style.setProperty("--pd", (n++ * .06).toFixed(2) + "s");
      }
    });
    h1.setAttribute("aria-label", h1.textContent.replace(/\s+/g, " ").trim());
    return n * .06;
  }

  var h1 = main.querySelector("h1"), finH1 = 0;
  if (h1 && visible(h1)) finH1 = partir(h1);

  // El hero de las portadas va aparte: tiene su propio orden.
  var hero = main.querySelector(".hero");
  if (hero) {
    var txt = hero.querySelector(".hero-txt");
    if (txt) [].forEach.call(txt.children, function (c, i) {
      if (c !== h1) marcar(c, Math.min(finH1, .5) + i * .08);
    });
    var demo = hero.querySelector(".hero-demo");
    if (demo) {
      marcar(demo, .25, "rv-der");
      [].forEach.call(demo.querySelectorAll(".hd-lista>li"), function (li, j) {
        marcar(li, .55 + j * .08);
      });
    }
  }
  [].forEach.call(main.children, function (c) {
    if (hero && c.contains(hero)) return;
    if (c.matches(NO_TOCAR)) return;
    if (esEnvoltorio(c)) recorrer(c, 0); else marcar(c);
  });

  // ---- Cifras que cuentan ----------------------------------------------------
  // "25", "100 %", "1,99 €"... cuentan desde 0 cuando entran. El texto de
  // después del número se respeta tal cual.
  function contar(el) {
    var m = el.textContent.match(/^(\D*)(\d+(?:[.,]\d+)?)([\s\S]*)$/);
    if (!m) return;
    var fin = parseFloat(m[2].replace(",", ".")), dec = (m[2].split(/[.,]/)[1] || "").length;
    if (!fin) return;
    var sep = m[2].indexOf(",") > -1 ? "," : ".", t0 = null;
    function paso(t) {
      if (t0 === null) t0 = t;
      var p = Math.min((t - t0) / 1100, 1), e = 1 - Math.pow(1 - p, 4);
      el.textContent = m[1] + (fin * e).toFixed(dec).replace(".", sep) + m[3];
      if (p < 1) requestAnimationFrame(paso);
    }
    el.textContent = m[1] + (0).toFixed(dec).replace(".", sep) + m[3];
    requestAnimationFrame(paso);
  }
  var cifras = [].slice.call(main.querySelectorAll(".datos-bar b"));

  // ---- Observador -------------------------------------------------------------
  function mostrar(el, k) {
    if (!el.style.getPropertyValue("--rv-d") && k)
      el.style.setProperty("--rv-d", Math.min(k * PASO, TOPE).toFixed(2) + "s");
    el.classList.add("visto");
    if (el.querySelectorAll) cifras.forEach(function (c) { if (el.contains(c) || el === c) contar(c); });
    // Al acabar se quitan las clases: así vuelven las transiciones propias del
    // elemento (el :hover de las tarjetas, por ejemplo) sin pelearse con estas.
    var d = parseFloat(el.style.getPropertyValue("--rv-d")) || 0;
    setTimeout(function () {
      el.classList.remove("rv", "visto", "rv-izq", "rv-der", "rv-foco", "rv-barrido");
      el.style.removeProperty("--rv-d");
    }, DURA + d * 1000 + 80);
  }
  var io = new IntersectionObserver(function (entradas) {
    // las entradas llegan en orden de documento: el lote se escalona así
    var k = 0;
    entradas.forEach(function (e) {
      if (!e.isIntersecting) return;
      var alto = e.boundingClientRect.height > innerHeight * .5;
      if (alto || e.intersectionRatio >= .15 || e.target.classList.contains("rv-barrido")) {
        mostrar(e.target, k++); io.unobserve(e.target);
      }
    });
  }, { threshold: [0, .15], rootMargin: "0px 0px -40px 0px" });

  // Se marcan sin transición (styles.css: .anim:not(.anim-listo) .rv) y se
  // fuerza un cálculo de estilos: si no, lo que ya estaba pintado se iría
  // fundiendo de visible a oculto antes de entrar.
  void main.offsetHeight;
  raiz.classList.add("anim-listo");

  marcados.forEach(function (el) {
    // lo que ya quedó por encima (recarga a media página, enlace con #ancla)
    // se enseña sin animar: nadie lo está mirando entrar
    if (el.getBoundingClientRect().bottom < 0) { el.classList.remove("rv"); return; }
    io.observe(el);
  });

  // ---- Cabecera y cielo del hero ----------------------------------------------
  var cab = document.querySelector(".site-head"), pendiente = false;
  function alBajar() {
    pendiente = false;
    var y = scrollY;
    if (cab) cab.classList.toggle("bajado", y > 8);
    if (y < innerHeight * 1.2) raiz.style.setProperty("--cielo", (y * .3).toFixed(1) + "px");
  }
  addEventListener("scroll", function () {
    if (!pendiente) { pendiente = true; requestAnimationFrame(alBajar); }
  }, { passive: true });
  alBajar();
})();
