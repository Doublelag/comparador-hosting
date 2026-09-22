# montatuserver.com en Cloudflare

Desde el 21-sep-2026 la web está en **Cloudflare Workers** (lo que antes se
llamaba Pages), en la cuenta de José Ángel, con el nombre `montatuserver`.

- Dirección de prueba: https://montatuserver.comparador-hosting.workers.dev
- Configuración: `wrangler.jsonc` (sube **solo** `dist/`).

## Publicar un cambio (sin arrastrar nada, sin créditos)
```
python build.py
python publicar.py
wrangler deploy
```
`wrangler` se instaló con Node.js (`npm i -g wrangler`) y ya tiene la sesión
de Cloudflare iniciada en este PC. Si algún día pide iniciar sesión otra vez:
`wrangler login` y pulsar **Allow** en el navegador.

**Nunca** cambies `"directory"` en `wrangler.jsonc` a `"."`: se publicaría la
carpeta entera del proyecto (LEEME.md con los márgenes, los .py, etc.).

## Volver a una versión anterior
`wrangler rollback` (elige la versión) o, en el panel: Workers y Pages →
`montatuserver` → Implementaciones.

## Pasar el dominio (lo que falta)
El dominio está en **Nominalia**, que también lleva sus DNS
(`dns1/dns2.nominalia.com`). Ahora mismo apunta a Netlify (A 75.2.60.5).

Registros que hay que conservar (Cloudflare los copia solo, pero revísalo):
- MX `montatuserver.com` → `mail.nominalia.com` (prioridad 10)
- TXT `montatuserver.com` → `v=spf1 include:spf.webapps.net ~all`

1. **Cloudflare**: panel → **Añadir un dominio** → `montatuserver.com` → plan
   **Free**. Revisa que aparezcan el MX y el TXT de arriba. Borra los registros
   A/CNAME de `montatuserver.com` y `www` que apunten a Netlify (75.2.60.5).
   Apunta los dos servidores de nombres que te dé (`xxx.ns.cloudflare.com`).
2. **Nominalia**: Mis dominios → montatuserver.com → **Servidores DNS** →
   cambia `dns1/dns2.nominalia.com` por los dos de Cloudflare.
3. Espera el correo de Cloudflare de que el dominio está **activo**.
4. Se añaden las rutas del dominio a `wrangler.jsonc` y `wrangler deploy`
   (Cloudflare crea el certificado HTTPS solo):
   ```
   "routes": [
     { "pattern": "montatuserver.com", "custom_domain": true },
     { "pattern": "www.montatuserver.com", "custom_domain": true }
   ]
   ```
5. Cuando `montatuserver.com` cargue desde Cloudflare, borra el sitio de
   Netlify.

### Ajustes recomendados del dominio en Cloudflare
- SSL/TLS → **Completo (estricto)**; **Usar siempre HTTPS: activado**.
- Scrape Shield → **Ofuscación de correo: desactivada** (mete un script).
- Rocket Loader: **desactivado**.

## Reglas que no hay que romper
- En Cloudflare una redirección de `_redirects` **manda sobre una página que
  exista**. Nunca redirijas una URL que tenga página propia.
- En `_headers` los .css y .js van **uno a uno**. Si se crea uno nuevo, se
  añade ahí.
