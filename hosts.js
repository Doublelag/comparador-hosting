/* =========================================================================
   DATOS DE PRECIOS — LA ÚNICA FUENTE DE VERDAD
   =========================================================================

   Este archivo lo leen DOS cosas:
     · app.js         → la calculadora y el gráfico de barras
     · build.py       → las tablas estáticas de las comparativas

   Por eso está escrito como JSON puro después del "=": así Python puede
   leerlo sin ejecutar JavaScript. NO metas comentarios ni comas de más
   DENTRO del objeto o Python dejará de poder leerlo. Fuera, como aquí, sí.

   ─────────────────────────────────────────────────────────────────────────
   SOLO MINECRAFT (desde el 17-sep-2026)
   ─────────────────────────────────────────────────────────────────────────
   La web era de 11 juegos y ahora es solo de Minecraft. Los precios siguen
   colgando de `precios.minecraft` y no de `precios` a secas a propósito: los
   hostings cobran distinto cada juego (Shockbyte cobraba Minecraft por GB y
   Valheim con plan único), y si algún día vuelve otro juego se añade su
   entrada al lado sin tocar el código. Lo que NO se hace nunca es copiar
   el precio de un juego a otro.

   Modelos:
     "porGB"   → precio = porGB × los GB que necesitas
     "tabla"   → escalones que publican ellos: [GB, precio]
     "plano"   → un solo plan: precio + ram (+ "slots" si venden plazas)
     "slots"   → se vende por jugadores, sin RAM publicada: [plazas, precio]

   ACTUALIZAR: cambia números, cambia "comprobado", y `python build.py`.
   ========================================================================= */

window.DATOS = {
  "comprobado": "20 de septiembre de 2026",
  "cambioUsdEur": 0.86,
  "_nota_ping": "Ping MEDIDO desde una conexion domestica en Espana, no estimado. 'tcp' = conexion TCP al puerto 25565 de su servidor publico de prueba, el mejor de 4 intentos. 'widget' = el medidor de la propia web del hosting, ejecutado desde esta misma conexion. 'ubicacion' = solo sabemos donde tienen centro de datos, no hemos podido medir. Si no esta comprobado NO se inventa: se deja fuera.",
  "ping": {
    "medido": "2026-09-08",
    "desde": "una conexión doméstica de fibra en España",
    "hosts": {
      "dathost": {
        "metodo": "widget",
        "espana": false,
        "europa": [
          "Ámsterdam",
          "Fráncfort",
          "Londres",
          "Helsinki"
        ],
        "detalle": [
          [
            "Ámsterdam",
            35
          ],
          [
            "Fráncfort",
            36
          ],
          [
            "Londres",
            37
          ],
          [
            "Helsinki",
            60
          ],
          [
            "Nueva York",
            99
          ]
        ]
      },
      "shockbyte": {
        "metodo": "tcp",
        "espana": false,
        "europa": [
          "Europa (Ámsterdam / Maidenhead)"
        ],
        "detalle": [
          [
            "Europa",
            36
          ],
          [
            "Norteamérica",
            136
          ],
          [
            "Singapur",
            236
          ],
          [
            "Australia",
            267
          ]
        ]
      },
      "pebble-budget": {
        "metodo": "ubicacion",
        "espana": false,
        "europa": [
          "Coventry (Reino Unido)"
        ],
        "detalle": []
      }
    }
  },
  "hosts": [
    {
      "id": "dathost",
      "nombre": "DatHost",
      "moneda": "EUR",
      "fuente": "https://dathost.com/minecraft-server-hosting",
      "precios": {
        "minecraft": {
          "modelo": "plano",
          "ram": 16,
          "precio": 14.9,
          "nota": "Plan único de 16 GB con Ryzen 9 7950X y slots ilimitados. Precio mes a mes; pagando el año por adelantado sale a 6,90 €/mes",
          "nota_en": "A single 16 GB plan with a Ryzen 9 7950X and unlimited slots. Month-to-month price; paying a year upfront brings it to €6.90/month"
        }
      },
      "ficha": "/hosting/dathost/"
    },
    {
      "id": "pebble-budget",
      "nombre": "PebbleHost Budget",
      "moneda": "USD",
      "precios": {
        "minecraft": {
          "modelo": "porGB",
          "porGB": 1.0,
          "nota": "Ryzen 7 5700X y memoria DDR4 a 2133 MHz. Lo más barato que hay, pero SIN copias de seguridad automáticas: eso es del plan Premium. Comprobado a 16 GB: 16,00 $",
          "nota_en": "Ryzen 7 5700X and DDR4 at 2133 MHz. The cheapest there is, but WITHOUT automatic backups: those come with the Premium plan. Checked at 16 GB: $16.00"
        }
      },
      "fuente": "https://pebblehost.com/minecraft/budget",
      "ficha": "/hosting/pebblehost/",
      "aviso": "no trae copias de seguridad automáticas",
      "aviso_en": "it has no automatic backups"
    },
    {
      "id": "pebble-premium",
      "nombre": "PebbleHost Premium",
      "moneda": "USD",
      "precios": {
        "minecraft": {
          "modelo": "porGB",
          "porGB": 2.25,
          "nota": "Ryzen 9 9900X y DDR5 4800. Incluye copias diarias y por horas, instalador de modpacks y más ubicaciones. Comprobado a 16 GB: 36,00 $",
          "nota_en": "Ryzen 9 9900X and DDR5 4800. Includes daily and hourly backups, a modpack installer and more locations. Checked at 16 GB: $36.00"
        }
      },
      "fuente": "https://pebblehost.com/minecraft-server-hosting",
      "ficha": "/hosting/pebblehost/"
    },
    {
      "id": "bisect",
      "nombre": "BisectHosting",
      "moneda": "EUR",
      "precios": {
        "minecraft": {
          "modelo": "porGB",
          "porGB": 2.69,
          "nota": "Precio por GB, lineal y clavado",
          "nota_en": "Per-GB price, flat and predictable"
        }
      },
      "fuente": "https://www.bisecthosting.com/minecraft-servers",
      "ficha": "/hosting/bisecthosting/"
    },
    {
      "id": "shockbyte",
      "nombre": "Shockbyte",
      "moneda": "USD",
      "precios": {
        "minecraft": {
          "modelo": "tabla",
          "nota": "Con su descuento del 30 % ya aplicado",
          "tiers": [
            [
              1,
              2.79
            ],
            [
              2,
              5.59
            ],
            [
              3,
              8.39
            ],
            [
              4,
              11.19
            ],
            [
              5,
              13.99
            ],
            [
              6,
              16.79
            ],
            [
              7,
              19.59
            ],
            [
              8,
              22.39
            ],
            [
              9,
              25.19
            ],
            [
              10,
              27.99
            ],
            [
              12,
              33.59
            ],
            [
              17,
              47.48
            ]
          ],
          "nota_en": "Their 30% discount is already applied"
        }
      },
      "fuente": "https://shockbyte.com/games/minecraft-server-hosting",
      "ficha": "/hosting/shockbyte/"
    },
    {
      "id": "apex",
      "nombre": "Apex Hosting",
      "moneda": "USD",
      "precios": {
        "minecraft": {
          "modelo": "tabla",
          "nota": "Precio recurrente. El primer mes lleva un 25 % de descuento",
          "tiers": [
            [
              4,
              14.99
            ],
            [
              6,
              22.49
            ],
            [
              8,
              27.99
            ],
            [
              16,
              71.99
            ]
          ],
          "entrada": {
            "pct": 25,
            "meses": 1,
            "que": "el primer mes",
            "que_en": "the first month"
          },
          "nota_en": "Recurring price. The first month comes with 25% off"
        }
      },
      "fuente": "https://apexminecrafthosting.com/pricing/",
      "ficha": "/hosting/apex-hosting/"
    },
    {
      "id": "hostinger",
      "nombre": "Hostinger",
      "moneda": "USD",
      "precios": {
        "minecraft": {
          "modelo": "tabla",
          "nota": "Precio de renovación. El de escaparate exige pagar 24 meses por adelantado y luego sube",
          "tiers": [
            [
              4,
              11.99
            ],
            [
              8,
              14.99
            ],
            [
              16,
              28.99
            ],
            [
              32,
              49.99
            ]
          ],
          "nota_en": "Renewal price. The headline price requires paying 24 months upfront, then it goes up"
        }
      },
      "fuente": "https://www.hostinger.com/vps/minecraft-hosting",
      "ficha": "/hosting/hostinger/",
      "vps": true,
      "aviso": "el precio pide pagar 24 meses por adelantado",
      "aviso_en": "that price needs 24 months paid upfront"
    },
    {
      "id": "sparked",
      "nombre": "Sparked Host",
      "moneda": "USD",
      "precios": {
        "minecraft": {
          "modelo": "porGB",
          "porGB": 2.59,
          "nota": "Ryzen 9 7900 con DDR5. Precio por GB, lineal",
          "nota_en": "Ryzen 9 7900 with DDR5. Flat per-GB price"
        }
      },
      "fuente": "https://sparkedhost.com/minecraft-server-hosting",
      "ficha": "/hosting/sparked-host/"
    },
    {
      "id": "sparked-extreme",
      "nombre": "Sparked Host Extreme",
      "moneda": "USD",
      "precios": {
        "minecraft": {
          "modelo": "porGB",
          "porGB": 4.0,
          "nota": "Su gama alta, con Ryzen 9 9900X",
          "nota_en": "Their top tier, with a Ryzen 9 9900X"
        }
      },
      "fuente": "https://sparkedhost.com/minecraft-server-hosting",
      "ficha": "/hosting/sparked-host/"
    },
    {
      "id": "holyhosting",
      "nombre": "HolyHosting",
      "moneda": "USD",
      "precios": {
        "minecraft": {
          "modelo": "porGB",
          "porGB": 1.25,
          "nota": "Tarifa recurrente. Anuncian 0,95 $/GB pero ese es el precio del PRIMER MES con su -25 %",
          "entrada": {
            "pct": 25,
            "meses": 1,
            "que": "el primer mes",
            "que_en": "the first month"
          },
          "nota_en": "Recurring rate. They advertise $0.95/GB, but that's the FIRST MONTH price with their -25%"
        }
      },
      "fuente": "https://www.holy.gg/en/minecraft",
      "ficha": "/hosting/holyhosting/"
    },
    {
      "id": "vultam-standard",
      "nombre": "Vultam Standard",
      "moneda": "USD",
      "precios": {
        "minecraft": {
          "modelo": "porGB",
          "porGB": 1.75,
          "nota": "Intel i7-6700K (procesador de 2015) y DDR4 2400. Copias diarias incluidas",
          "nota_en": "Intel i7-6700K (a 2015 CPU) and DDR4 2400. Daily backups included"
        }
      },
      "fuente": "https://vultam.net/minecraft",
      "ficha": "/hosting/vultam/",
      "vps": true
    },
    {
      "id": "vultam-advanced",
      "nombre": "Vultam Advanced",
      "moneda": "USD",
      "precios": {
        "minecraft": {
          "modelo": "porGB",
          "porGB": 2.4,
          "nota": "Su gama buena: Ryzen 7 3700X, DDR4 2666 y NVMe. Nodos en Francia y Alemania",
          "nota_en": "Their better tier: Ryzen 7 3700X, DDR4 2666 and NVMe. Nodes in France and Germany"
        }
      },
      "fuente": "https://vultam.net/minecraft",
      "ficha": "/hosting/vultam/",
      "vps": true
    },
    {
      "id": "vultam-performance",
      "nombre": "Vultam Performance",
      "moneda": "USD",
      "precios": {
        "minecraft": {
          "modelo": "porGB",
          "porGB": 3.5,
          "nota": "Ryzen 9 5950X a 4,8 GHz y copias cada 12 horas. Es su gama alta",
          "nota_en": "Ryzen 9 5950X at 4.8 GHz and backups every 12 hours. Their top tier"
        }
      },
      "fuente": "https://vultam.net/minecraft",
      "ficha": "/hosting/vultam/",
      "vps": true
    },
    {
      "id": "wisehosting",
      "nombre": "WiseHosting",
      "moneda": "USD",
      "precios": {
        "minecraft": {
          "modelo": "porGB",
          "porGB": 3.0,
          "nota": "Precio mensual. Pagando el año entero lo dejan en 1,50 $/GB",
          "nota_en": "Monthly price. Paying the whole year brings it down to $1.50/GB"
        }
      },
      "fuente": "https://wisehosting.com/",
      "ficha": "/hosting/wisehosting/"
    },
    {
      "id": "nexohost",
      "nombre": "NexoHost",
      "moneda": "EUR",
      "precios": {
        "minecraft": {
          "modelo": "tabla",
          "tiers": [
            [
              1,
              1.0
            ],
            [
              2,
              2.3
            ],
            [
              3,
              3.3
            ],
            [
              4,
              4.3
            ],
            [
              5,
              5.3
            ],
            [
              6,
              6.3
            ],
            [
              7,
              7.3
            ],
            [
              8,
              8.3
            ],
            [
              9,
              9.3
            ]
          ],
          "nota": "Español, con Ryzen 7 3700X. Su plan más grande es de 9 GB. De ahí no pasa",
          "nota_en": "Spanish, with a Ryzen 7 3700X. Their biggest plan is 9 GB. That's the ceiling"
        }
      },
      "fuente": "https://nexohost.es/minecraft",
      "ficha": "/hosting/nexohost/"
    },
    {
      "id": "theminecrafthosting",
      "nombre": "The Minecraft Hosting",
      "moneda": "USD",
      "precios": {
        "minecraft": {
          "modelo": "tabla",
          "tiers": [
            [
              1,
              2.5
            ],
            [
              2,
              4.0
            ],
            [
              3,
              6.5
            ],
            [
              4,
              8.0
            ],
            [
              5,
              10.5
            ],
            [
              6,
              12.0
            ],
            [
              8,
              16.0
            ],
            [
              10,
              22.5
            ],
            [
              12,
              27.0
            ],
            [
              16,
              35.0
            ],
            [
              32,
              62.0
            ],
            [
              48,
              95.0
            ]
          ],
          "nota": "Precios de su nodo de París. Llevan un código BLACKFRIDAY del −60 % puesto todo el año",
          "nota_en": "Prices from their Paris node. They run a −60% BLACKFRIDAY code all year round"
        }
      },
      "fuente": "https://theminecrafthosting.com/france-pc-plans.php",
      "ficha": "/hosting/theminecrafthosting/"
    },
    {
      "id": "realms",
      "nombre": "Minecraft Realms",
      "moneda": "USD",
      "precios": {
        "minecraft": {
          "modelo": "slots",
          "tiers": [
            [
              11,
              7.99
            ]
          ],
          "nota": "OJO: Realms no se vende por RAM. Este precio es el mismo pongas los GB que pongas, o sea que no te dan 16 GB por 6,87 €. Es el oficial de Mojang: sin plugins, sin mods y con tope de 10 jugadores. Bedrock suelto son 3,99 $, pero ahí solo caben 3",
          "nota_en": "HEADS UP: Realms isn't sold by RAM. This price is the same whatever GB you pick, so no, you don't get 16 GB for €6.87. It's Mojang's official one: no plugins, no mods and a 10-player cap. Bedrock on its own is $3.99, but only fits 3"
        }
      },
      "fuente": "https://www.minecraft.net/es-es/realms/realms-for-java",
      "ficha": "/hosting/realms/",
      "limites": {
        "mods": false,
        "maxJugadores": 10
      }
    },
    {
      "id": "godlike",
      "nombre": "Godlike.host",
      "moneda": "EUR",
      "precios": {
        "minecraft": {
          "modelo": "tabla",
          "nota": "El único descuento de la comparativa que no caduca: −25 % todos los meses con el código DOUBLELAG. Ryzen hasta 9950X3D con NVMe y hasta 3 copias al día gratis. Eliges gigas, plazas y días. Prueba gratis de un día y buscador de mods integrado en el panel. El descuento se mantiene mientras sigas",
          "tiers": [
            [
              2,
              6.29
            ],
            [
              4,
              12.99
            ],
            [
              6,
              18.99
            ],
            [
              8,
              25.99
            ],
            [
              12,
              37.99
            ],
            [
              16,
              50.99
            ],
            [
              20,
              63.99
            ]
          ],
          "entrada": {
            "pct": 25,
            "meses": 9999,
            "permanente": true,
            "que": "siempre, no solo el primer mes",
            "que_en": "every month, not just the first"
          },
          "nota_en": "The only discount in the comparison that never expires: −25% off every month with the code DOUBLELAG. Ryzen up to 9950X3D with NVMe and up to 3 free backups a day. You pick the GB, slots and days. One-day free trial and a mod finder built into the panel. After the first purchase, the normal rate applies"
        }
      },
      "fuente": "https://godlike.host/minecraft-server-hosting/",
      "ficha": "/hosting/godlike/"
    },
    {
      "id": "nodecraft",
      "nombre": "Nodecraft",
      "moneda": "USD",
      "precios": {
        "minecraft": {
          "modelo": "tabla",
          "nota": "Gama Pro, encendida 24/7 y con IP propia. Prueba gratis de 24 h, pero piden verificar el teléfono. Devolución en 7 días",
          "tiers": [
            [
              2,
              9.98
            ],
            [
              4,
              19.98
            ],
            [
              8,
              39.98
            ],
            [
              12,
              59.98
            ]
          ],
          "entrada": {
            "pct": 30,
            "meses": 1,
            "que": "el primer mes",
            "que_en": "the first month"
          },
          "nota_en": "Pro tier, always on and with its own IP. 24-hour free trial, but they ask you to verify your phone. 7-day refund"
        }
      },
      "fuente": "https://try.nodecraft.com/minecraft-server-hosting",
      "ficha": "/hosting/nodecraft/"
    },
    {
      "id": "gportal",
      "nombre": "GPORTAL",
      "moneda": "EUR",
      "precios": {
        "minecraft": {
          "modelo": "tabla",
          "nota": "Plazas ilimitadas y 250 modpacks de un clic. Su tope son 6 GB. El −25 % del escaparate es solo del primer periodo",
          "tiers": [
            [
              2,
              5.4
            ],
            [
              4,
              11.8
            ],
            [
              6,
              15.0
            ]
          ],
          "entrada": {
            "pct": 25,
            "meses": 1,
            "que": "el primer periodo",
            "que_en": "the first period"
          },
          "nota_en": "Unlimited slots and 250 one-click modpacks. Their ceiling is 6 GB. The −25% on the shop window only applies to the first period"
        }
      },
      "fuente": "https://www.g-portal.com/en/gameserver/minecraft-server-hosting",
      "ficha": "/hosting/gportal/"
    },
    {
      "id": "scalacube",
      "nombre": "ScalaCube",
      "moneda": "USD",
      "precios": {
        "minecraft": {
          "modelo": "tabla",
          "nota": "Plazas ilimitadas, dominio y MySQL gratis. El −50 % que anuncian es solo del primer mes",
          "tiers": [
            [
              1,
              5
            ],
            [
              3,
              10
            ],
            [
              4,
              13
            ],
            [
              6,
              18
            ],
            [
              8,
              24
            ],
            [
              12,
              36
            ],
            [
              16,
              48
            ],
            [
              24,
              72
            ],
            [
              32,
              96
            ],
            [
              48,
              144
            ],
            [
              64,
              192
            ]
          ],
          "entrada": {
            "pct": 50,
            "meses": 1,
            "que": "el primer mes",
            "que_en": "the first month"
          },
          "nota_en": "Unlimited slots, free domain and MySQL. The −50% they advertise only applies to the first month"
        }
      },
      "fuente": "https://scalacube.com/hosting/server/minecraft",
      "ficha": "/hosting/scalacube/"
    },
    {
      "id": "ggservers",
      "nombre": "GGServers",
      "moneda": "USD",
      "precios": {
        "minecraft": {
          "modelo": "tabla",
          "nota": "Gama Standard: CPU de 3,2-4 GHz, DDR4 2133 y SSD. 3 $ el giga clavado. Su cupón TAKE20 es de la primera factura",
          "tiers": [
            [
              1,
              3
            ],
            [
              2,
              6
            ],
            [
              3,
              9
            ],
            [
              4,
              12
            ],
            [
              5,
              15
            ],
            [
              6,
              18
            ],
            [
              8,
              24
            ],
            [
              12,
              36
            ],
            [
              16,
              48
            ],
            [
              32,
              96
            ]
          ],
          "entrada": {
            "pct": 20,
            "meses": 1,
            "que": "la primera factura",
            "que_en": "the first invoice"
          },
          "nota_en": "Standard tier: 3.2-4 GHz CPU, DDR4 2133 and SSD. Exactly $3 per GB. Their TAKE20 coupon is for the first invoice only"
        }
      },
      "fuente": "https://ggservers.com/minecrafthosting",
      "ficha": "/hosting/ggservers/",
      "aviso": "su gama Standard monta DDR4 a 2133 MHz",
      "aviso_en": "its Standard range runs DDR4 at 2133 MHz"
    },
    {
      "id": "ggservers-premium",
      "nombre": "GGServers Premium",
      "moneda": "USD",
      "precios": {
        "minecraft": {
          "modelo": "tabla",
          "nota": "Su gama buena: CPU de 4,4-5 GHz con prioridad alta, DDR4 2400 y NVMe. Cuesta el doble que la Standard",
          "tiers": [
            [
              1,
              6
            ],
            [
              2,
              12
            ],
            [
              3,
              18
            ],
            [
              4,
              24
            ],
            [
              5,
              30
            ],
            [
              6,
              36
            ],
            [
              8,
              48
            ],
            [
              12,
              72
            ],
            [
              16,
              96
            ],
            [
              32,
              192
            ]
          ],
          "entrada": {
            "pct": 20,
            "meses": 1,
            "que": "la primera factura",
            "que_en": "the first invoice"
          },
          "nota_en": "Their better tier: 4.4-5 GHz high-priority CPU, DDR4 2400 and NVMe. Twice the price of Standard"
        }
      },
      "fuente": "https://ggservers.com/minecrafthosting",
      "ficha": "/hosting/ggservers/"
    },
    {
      "id": "kinetic",
      "nombre": "Kinetic Hosting",
      "moneda": "USD",
      "precios": {
        "minecraft": {
          "modelo": "tabla",
          "nota": "Unos 0,99 $ el giga, de lo más barato que hay. Cinco copias de seguridad, cambio de juego cuando quieras y devolución en 7 días sin preguntas. Su plan más pequeño son 4 GB",
          "tiers": [
            [
              4,
              4.99
            ],
            [
              8,
              7.99
            ],
            [
              10,
              9.99
            ],
            [
              12,
              12.99
            ],
            [
              14,
              14.0
            ],
            [
              16,
              15.99
            ],
            [
              21,
              20.99
            ],
            [
              26,
              25.99
            ],
            [
              32,
              31.99
            ],
            [
              42,
              41.99
            ],
            [
              64,
              61.99
            ],
            [
              124,
              123.99
            ]
          ],
          "nota_en": "About $0.99 per GB, among the cheapest there is. Five backups, switch games whenever you like and a 7-day no-questions refund. Their smallest plan is 4 GB"
        }
      },
      "fuente": "https://www.kinetichosting.com/game-servers/minecraft",
      "ficha": "/hosting/kinetic/"
    },
    {
      "id": "chunkly",
      "nombre": "Chunkly",
      "moneda": "EUR",
      "precios": {
        "minecraft": {
          "modelo": "tabla",
          "tiers": [
            [
              2,
              1.7
            ],
            [
              3,
              2.55
            ],
            [
              4,
              3.4
            ],
            [
              5,
              4.25
            ],
            [
              6,
              5.1
            ],
            [
              7,
              5.95
            ],
            [
              8,
              6.8
            ],
            [
              9,
              7.65
            ],
            [
              10,
              8.5
            ],
            [
              11,
              9.35
            ],
            [
              12,
              10.2
            ]
          ],
          "nota": "Gama Village: 0,85 € el giga con IVA, de 2 a 12 GB, pago mensual en euros y baja cuando quieras. Solo Paper, Purpur y Vanilla; los modpacks van en su gama Kingdom. NVMe y protección DDoS, en Europa. Tienen un plan gratis (Campfire) de 2 GB para probar sin tarjeta",
          "nota_en": "Village range: €0.85 per GB incl. VAT, 2 to 12 GB, monthly billing in euros, cancel any time. Paper, Purpur and Vanilla only; modpacks go on their Kingdom range. NVMe and DDoS protection, in Europe. Free 2 GB Campfire plan to try it without a card"
        }
      },
      "fuente": "https://chunkly.net/store/minecraft",
      "limites": {
        "mods": false
      }
    },
    {
      "id": "chunkly-kingdom",
      "nombre": "Chunkly Kingdom",
      "moneda": "EUR",
      "precios": {
        "minecraft": {
          "modelo": "tabla",
          "tiers": [
            [
              4,
              7.6
            ],
            [
              5,
              9.5
            ],
            [
              6,
              11.4
            ],
            [
              7,
              13.3
            ],
            [
              8,
              15.2
            ],
            [
              9,
              17.1
            ],
            [
              10,
              19.0
            ],
            [
              11,
              20.9
            ],
            [
              12,
              22.8
            ],
            [
              13,
              24.7
            ],
            [
              14,
              26.6
            ],
            [
              15,
              28.5
            ],
            [
              16,
              30.4
            ]
          ],
          "nota": "Su gama para modpacks (Forge, Fabric, NeoForge, Modrinth y CurseForge): 1,90 € el giga con IVA, de 4 a 16 GB, pago mensual en euros",
          "nota_en": "Their modpack range (Forge, Fabric, NeoForge, Modrinth and CurseForge): €1.90 per GB incl. VAT, 4 to 16 GB, monthly billing in euros"
        }
      },
      "fuente": "https://chunkly.net/store/minecraft"
    },
    {
      "id": "akliz",
      "nombre": "Akliz",
      "moneda": "USD",
      "precios": {
        "minecraft": {
          "modelo": "tabla",
          "nota": "Precio de lista, 5 $ el giga. A veces enseñan un 20 % de rebaja sin decir en qué condiciones, así que no lo cuento. Soporte que te ayuda a mano, copias dos veces al día y devolución en 7 días",
          "nota_en": "List price, $5 per GB. They sometimes show 20% off without saying on what terms, so I don't count it. Hands-on support, backups twice a day and a 7-day refund",
          "tiers": [
            [
              2,
              10
            ],
            [
              3,
              15
            ],
            [
              4,
              20
            ],
            [
              6,
              30
            ],
            [
              8,
              40
            ],
            [
              12,
              60
            ],
            [
              24,
              120
            ]
          ]
        }
      },
      "fuente": "https://www.akliz.net/pricing",
      "ficha": "/hosting/akliz/"
    },
    {
      "id": "hosthavoc",
      "nombre": "Host Havoc",
      "moneda": "USD",
      "precios": {
        "minecraft": {
          "modelo": "tabla",
          "nota": "Precio normal, 5 $ el giga. Ahora anuncian un 25 % menos con el código SUMMER, pero es una promoción de temporada. IP propia gratis desde 6 GB (antes, +4 $ al mes). Garantía de 72 horas",
          "nota_en": "Regular price, $5 per GB. Right now they advertise 25% off with the code SUMMER, but it's a seasonal promotion. Free dedicated IP from 6 GB (below that, +$4 a month). 72-hour guarantee",
          "tiers": [
            [
              1,
              5
            ],
            [
              2,
              10
            ],
            [
              3,
              15
            ],
            [
              4,
              20
            ],
            [
              6,
              30
            ],
            [
              8,
              40
            ],
            [
              12,
              60
            ],
            [
              16,
              80
            ],
            [
              24,
              120
            ],
            [
              32,
              160
            ]
          ]
        }
      },
      "fuente": "https://hosthavoc.com/minecraft",
      "ficha": "/hosting/hosthavoc/"
    },
    {
      "id": "serverminer",
      "nombre": "ServerMiner",
      "moneda": "EUR",
      "precios": {
        "minecraft": {
          "modelo": "tabla",
          "nota": "Cada plan tiene tope de jugadores (de 15 a 100). Un 10 % menos pagando 3 meses y un 15 % pagando 6. Tienen centros en Alemania y Finlandia",
          "nota_en": "Each plan has a player cap (15 to 100). 10% off paying for 3 months and 15% for 6. They have data centres in Germany and Finland",
          "tiers": [
            [
              1.5,
              6.77
            ],
            [
              2,
              8.83
            ],
            [
              3,
              13.08
            ],
            [
              4,
              17.29
            ],
            [
              6,
              25.78
            ],
            [
              8,
              34.2
            ],
            [
              10,
              42.61
            ]
          ]
        }
      },
      "fuente": "https://serverminer.com/buy-minecraft-server",
      "ficha": "/hosting/serverminer/"
    },
    {
      "id": "bloom",
      "nombre": "Bloom.host",
      "moneda": "USD",
      "precios": {
        "minecraft": {
          "modelo": "tabla",
          "nota": "4 y 6 GB son la gama Essentials (núcleos compartidos); desde 8 GB, la Performance, con núcleos dedicados y Ryzen 9 3950X o 5950X. Tienen centro en Falkenstein (Alemania)",
          "nota_en": "4 and 6 GB are the Essentials range (shared cores); from 8 GB it's Performance, with dedicated cores and a Ryzen 9 3950X or 5950X. They have a data centre in Falkenstein (Germany)",
          "tiers": [
            [
              4,
              12
            ],
            [
              6,
              18
            ],
            [
              8,
              22
            ],
            [
              12,
              33
            ],
            [
              16,
              44
            ],
            [
              20,
              55
            ],
            [
              24,
              66
            ],
            [
              32,
              88
            ]
          ]
        }
      },
      "fuente": "https://bloom.host/stock-mc.js",
      "ficha": "/hosting/bloom/"
    },
    {
      "id": "bloom-plus",
      "nombre": "Bloom.host Performance+",
      "moneda": "USD",
      "precios": {
        "minecraft": {
          "modelo": "tabla",
          "nota": "Núcleos dedicados con Ryzen 9 9950X (7950X3D en Alemania). Su cupón PERFPLUSME es solo de la primera factura",
          "nota_en": "Dedicated cores on a Ryzen 9 9950X (7950X3D in Germany). Their PERFPLUSME coupon is for the first invoice only",
          "tiers": [
            [
              8,
              28
            ],
            [
              12,
              42
            ],
            [
              16,
              56
            ],
            [
              20,
              70
            ],
            [
              24,
              84
            ],
            [
              32,
              112
            ]
          ],
          "entrada": {
            "pct": 20,
            "meses": 1,
            "que": "la primera factura",
            "que_en": "the first invoice"
          }
        }
      },
      "fuente": "https://bloom.host/stock-mc.js",
      "ficha": "/hosting/bloom/"
    }
  ],
  "_nota_fuente": "'fuente' es la pagina de la que sale el precio de ese hosting. La usa revisar_precios.py para avisarte cuando cambie algo. Si anades un hosting, anade tambien su fuente o quedara fuera de la revision.",
  "_nota_partner": "EL UNICO SITIO QUE SE TOCA AL CERRAR UN ACUERDO DE AFILIADO. Con activo=false la web es un comparador sin ningun enlace de afiliado ni hosting destacado, y todos los avisos dicen que no hay acuerdo con nadie. Para activar a un partner: (1) hostId = el id de ese hosting en hosts[] — su precio sale de ahi, NO se repite aqui, asi nunca hay dos precios distintos; (2) enlace = su URL de afiliado; si lleva {juego} se sustituye por slugs[juego] o por el id del juego; (3) codigo y descuento, si los hay; (4) activo=true y build.py.",
  "partner": {
    "activo": true,
    "hostId": "godlike",
    "enlace": "https://affiliate.godlike.host/doublelag",
    "slugs": {},
    "codigo": "DOUBLELAG",
    "descuento": "−25 % todos los meses con el código",
    "canal": "WEB",
    "promo": null,
    "razones": [
      "<strong>−25 % todos los meses con el código DOUBLELAG: el único descuento de esta web que no caduca.</strong>",
      "Eliges los días: si el modpack os dura tres meses, pagas tres meses.",
      "Ryzen de última generación, hasta el 9950X3D, y hasta 3 copias al día gratis.",
      "Pruebas el panel un día gratis antes de pagar."
    ],
    "razones_en": [
      "<strong>−25% off every month with the code DOUBLELAG: the only discount here that never expires.</strong>",
      "You pick the days: if the modpack lasts you three months, you pay for three months.",
      "Latest-gen Ryzen, up to the 9950X3D, and up to 3 free backups a day.",
      "Try the panel free for a day before you pay."
    ],
    "descuento_en": "−25% off every month with the code"
  },
  "_nota_entrada": "'entrada' es el descuento que SOLO vale para empezar (primer mes o primera compra). El precio de 'tiers'/'porGB' es siempre el recurrente, el que pagas el mes 2. Con los dos se calcula el coste del primer ano, que es donde se ven las trampas del sector. pct = % de descuento, meses = cuantos meses dura, que = como lo llaman ellos.",
  "_nota_ficha": "'ficha' es la pagina de analisis de ese hosting dentro de esta web. La calculadora enlaza ahi desde el grafico y desde la tabla: quien ve un precio raro quiere leer la letra pequena sin perder el resultado. Las gamas hermanas (Premium/Budget) comparten ficha.",
  "comprobado_en": "20 September 2026",
  "_nota_limites": "'limites' dice lo que un hosting NO puede hacer por mucho que pagues: mods=false (Realms no admite ni mods ni plugins) y maxJugadores. La calculadora lo saca de la lista cuando pides algo que no puede dar, en vez de enseñarlo barato y que la persona se lleve el chasco al contratar.",
  "_nota_vps": "'vps' = te dan una máquina vacía y el servidor lo instalas y lo mantienes tú. No es comparable a un panel donde le das a un botón: se avisa en la barra.",
  "_nota_aviso": "'aviso' es la pega de una línea que hay que decir si la calculadora recomienda ese hosting: no basta con que sea el más barato si tiene un pero que cambia la decisión."
};
