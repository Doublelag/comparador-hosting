# Plan de contenido — las 50 páginas

Objetivo: llegar a ~50 páginas indexables que cubran todas las búsquedas con las
que alguien acaba alquilando un servidor. Ordenadas por lo que más convierte.

**Estado a 8-sep-2026: 26 hechas, 24 por hacer.**

Últimas altas: 7 fichas de hosting nuevas (HolyHosting, Vultam, WiseHosting,
NexoHost, The Minecraft Hosting, exaroton y Minecraft Realms) más la página
`/ping-desde-espana/`. La comparativa de Minecraft pasa de 11 a 18 hostings.

> Lo urgente ahora no es escribir páginas: la promo de Valheim a 1 € acaba
> el **17 de septiembre** y el SEO no llega a tiempo. El tráfico de esa
> ventana tiene que venir del canal.

---

## ✅ Hechas (19)

### Calculadora por juego (11) — `/`, `/minecraft/`, `/valheim/`…
Portada + 11 juegos. Cada una con su texto propio y su comparativa de precios.

### Comparativas "mejor hosting de X" (6)
- `/minecraft/mejor-hosting/` — 11 hostings
- `/valheim/mejor-hosting/` — 3
- `/palworld/mejor-hosting/` — 2
- `/rust/mejor-hosting/` — 2 *(DatHost no lo ofrece: página sin comisión)*
- `/terraria/mejor-hosting/` — 2 *(idem)*
- `/project-zomboid/mejor-hosting/` — 2

### Guías "cómo montar un servidor de X" (2)
- `/minecraft/como-montar-un-servidor/`
- `/valheim/como-montar-un-servidor/`

---

## ⬜ Por hacer (31)

### A. Comparativas que faltan (5) — `comparativas_extra.py`
Las que más convierten. **Pero cuatro están bloqueadas por falta de datos, no
por falta de tiempo.** Una comparativa con DatHost y un solo rival es un anuncio
disfrazado, justo lo que esta web le critica al resto. Antes hay que buscar y
comprobar a mano precios de un 2º y 3er hosting.

Rivales con precio comprobado hoy (además de DatHost):

| Página | Rivales | Estado |
|---|---|---|
| `/enshrouded/mejor-hosting/` | 2 (Shockbyte, Nodecraft) | ✅ **se puede escribir ya** |
| `/7-days-to-die/mejor-hosting/` | 1 (Shockbyte) | ⛔ falta un 2º |
| `/satisfactory/mejor-hosting/` | 1 (Nodecraft) | ⛔ falta un 2º |
| `/v-rising/mejor-hosting/` | 1 (Nodecraft) | ⛔ falta un 2º |
| `/ark-survival-ascended/mejor-hosting/` | 0 | ⛔ falta un 2º |

Para desbloquearlas: entrar en la web de cada hosting, **leer el DOM ya
renderizado** (el HTML crudo devuelve la plantilla y da precios idénticos para
todos los juegos — ya pasó con Shockbyte) y meter el precio en `hosts.js`
dentro de `precios[juego]`.

### B. Guías que faltan (9) — `guias.py`
Tráfico todo el año. Cada una debe contar algo que solo sepa quien lo ha montado.

6. Cómo montar un servidor de Palworld
7. Cómo montar un servidor de Rust
8. Cómo montar un servidor de ARK: Survival Ascended
9. Cómo montar un servidor de Project Zomboid
10. Cómo montar un servidor de 7 Days to Die
11. Cómo montar un servidor de Enshrouded
12. Cómo montar un servidor de Satisfactory
13. Cómo montar un servidor de V Rising
14. Cómo montar un servidor de Terraria

### C. Cara a cara entre hostings (6)
Búsquedas cortas con intención altísima. La tabla sale sola de `hosts.js`.

15. DatHost vs Shockbyte
16. DatHost vs BisectHosting
17. Shockbyte vs BisectHosting
18. Apex vs Shockbyte
19. Nodecraft vs DatHost
20. PebbleHost vs Shockbyte

### D. Preguntas de cola larga (11)
Aquí no compites contra granjas de contenido con autoridad: son búsquedas que
nadie ataca bien y que traen a gente a punto de pagar.

21. ¿Cuánto cuesta un servidor de Minecraft al mes?
22. ¿Cuánta RAM para 20 jugadores en Minecraft?
23. ¿Cuánta RAM para un modpack grande? (RLCraft, ATM, GTNH)
24. Jugar Minecraft juntos desde PC, PS5 y Switch: cómo se hace
25. ¿Es legal montar un servidor de Minecraft y cobrar rangos?
26. Servidor en mi PC vs alquilado: la comparación honesta
27. Mi servidor de Minecraft va lento: por dónde empezar
28. ¿Qué procesador necesita un servidor de Minecraft?
29. Paper vs Fabric vs Forge: cuál elegir y por qué
30. Cómo pasar tu mundo de un hosting a otro sin perderlo
31. Hosting de Minecraft barato en España: qué mirar

---

## Orden recomendado

1. **De las comparativas (A) solo Enshrouded se puede escribir hoy.** Las otras
   cuatro necesitan antes precios comprobados de un 2º hosting. Sacar esos
   precios es la tarea, no redactar.
2. **Luego el cara a cara (C)** — mismo dato, poco trabajo, intención altísima.
3. **Después la cola larga (D)** — donde de verdad puedes ganar a la competencia.
4. **Las guías (B) al final** — las más largas de escribir, aunque las más duraderas.

## Regla para no fallar

Cada página tiene que decir **algo que solo sepa alguien que ha montado ese
servidor**. Si el texto vale para cualquier juego cambiando el nombre, es
relleno y Google lo trata como tal. Ahí es exactamente donde las granjas de
contenido pierden y tú ganas.
