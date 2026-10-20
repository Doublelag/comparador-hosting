// Worker de montatuserver.com. Sirve los estáticos de dist/ y una sola API:
//
//   GET /api/server  →  {online, jugadores, maximo, version}
//
// Es el estado de ChorizoSMP para la portada y /mi-server/. Se consulta
// desde aquí y no desde el navegador del visitante para no mandar su IP a
// un servicio de terceros (mcsrvstat): el Worker pregunta una vez por
// minuto y todos los visitantes leen esa misma respuesta cacheada.

const SERVER = "chorizosmp.datho.st";
const CACHE_SEG = 60;

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    if (url.pathname === "/api/server") {
      return estadoServer(request, ctx);
    }
    return env.ASSETS.fetch(request);
  },
};

async function estadoServer(request, ctx) {
  const cache = caches.default;
  const clave = new Request("https://montatuserver.com/api/server", { method: "GET" });
  const guardada = await cache.match(clave);
  if (guardada) return guardada;

  let datos = { online: false, jugadores: 0, maximo: 0, version: "" };
  try {
    const r = await fetch("https://api.mcsrvstat.us/3/" + SERVER, {
      headers: { "User-Agent": "montatuserver.com (estado de ChorizoSMP)" },
      cf: { cacheTtl: CACHE_SEG },
    });
    if (r.ok) {
      const j = await r.json();
      datos = {
        online: !!j.online,
        jugadores: (j.players && j.players.online) || 0,
        maximo: (j.players && j.players.max) || 0,
        version: (j.version || "").toString().slice(0, 24),
      };
    }
  } catch (e) {
    // si mcsrvstat no responde, se devuelve "desconocido" y la web no rompe
    datos.desconocido = true;
  }

  const resp = new Response(JSON.stringify(datos), {
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "public, max-age=" + CACHE_SEG,
      "access-control-allow-origin": "https://montatuserver.com",
    },
  });
  ctx.waitUntil(cache.put(clave, resp.clone()));
  return resp;
}
