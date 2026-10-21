# -*- coding: utf-8 -*-
"""
English version of every host review (hostings.FICHAS). Same keys, same
structure. Prices, host names and URLs are shared with the Spanish version;
only the text lives here.

Keep in step with hostings.py and fichas_extra.py: if a Spanish review
changes, change its English twin too.
"""

FICHAS_EN = {

  "ouiheberg": dict(
    pais="France",
    rasgos=['€1.99 for 4 GB incl. VAT', 'No contract', 'Free 4-player server', 'Marseille: closest to Spain'],
    resumen=("French host with three fixed plans: 4 GB for €1.99, 8 for €4.99 and 16 for €10, VAT included and no contract. "
             "Per gigabyte, the cheapest in the whole table. Marseille is the closest datacenter to Spain of any host compared here."),
    bueno=[
      "<strong>Cheapest per GB in the comparison</strong>: €0.50 per GB on the 4 GB plan (€1.99) and €0.62 on the 16 GB one (€10). Half of Chunkly and PebbleHost, the cheap ones until now.",
      "<strong>Recurring price, VAT included, in euros</strong>: not a first-month promo and no dollar conversion. Month to month, no contract.",
      "<strong>Marseille</strong> as a datacenter: of all the hosts compared, the closest to Spain. Frankfurt as a second European option.",
      "Backups included (2 on Start, 5 on Pro), 2-4 vCPU at 3.7 GHz, NVMe, unlimited players and one-click modpacks from CurseForge and Modrinth.",
      "They offer a <strong>free server</strong> for up to 4 players (Paper/Spigot, no mods) to try the panel with no card.",
    ],
    malo=[
      "Only three sizes: 4, 8 and 16 GB. No 2 GB for four friends and no 12 GB for a mid modpack; above 16 you move to their OuiBox, which is a different product.",
      "The 4 GB plan ships with <strong>20 GB</strong> of disk: a big modpack plus its backups fills it. The 8 GB plan has 50 GB.",
      "They don't publish the exact CPU model (“Ryzen infrastructure”, 3.7 GHz). Fine for vanilla and plugins; for a heavy modpack you want to know.",
      "Ticket support in French and English. Spanish website, French team.",
      "Their own “best Minecraft hosting” page ranks themselves first. It's not a comparison: it's their site.",
    ],
    veredicto=("Today it's the cheapest per GB in the whole table and, on top, in euros, VAT included, with no first-month trick. If one of its three sizes "
               "(4, 8 or 16 GB) fits you and you're not a 30 GB-disk modpack, it's the first option I'd look at. If you need 2 GB or more than 16, it's not your place."),
  ),

  "chunkly": dict(
    pais="Europe (GateX Ltd)",
    rasgos=['€0.85 per GB incl. VAT', 'Free 2 GB plan', 'Monthly billing in euros', 'Modpacks only on Kingdom'],
    resumen=("€0.85 per GB incl. VAT, monthly billing in euros and a free plan to try the panel. "
             "Modpacks go on their Kingdom range, at €1.90 per GB."),
    bueno=[
      "<strong>Among the cheapest in the table</strong>: €0.85 per GB on the Village range, 2 to 12 GB. 4 GB is €3.40 a month.",
      "Price <strong>with VAT and in euros</strong>: what you see is what you pay, no surprise at checkout and no dollar conversion.",
      "Free <strong>Campfire plan</strong> (2 GB, vanilla, about 3 players) to try the panel with no card.",
      "Month to month, cancel any time. NVMe, DDoS protection, Java and Bedrock.",
    ],
    malo=[
      "New brand: little track record and few reviews so far. The company behind it says 25 years in hosting, but Chunkly itself has only just started.",
      "The cheap range (Village) only runs Paper, Purpur and Vanilla. For Forge, Fabric or a modpack you need Kingdom, which costs more than double: €1.90 per GB.",
      "Capped at 12 GB on Village and 16 on Kingdom. They don't say which CPU they use.",
      "Support in English only.",
    ],
    veredicto=("On price it's one of the two or three cheapest in the table and, billing in euros with VAT, "
               "the price you see is the price you pay. It's new with little track record: try the free plan "
               "before moving your community over. For modpacks, Kingdom costs more than double and there you have real rivals."),
  ),

  "dathost": dict(
    pais="Sweden",
    rasgos=['Ryzen 9 7950X', 'Unlimited slots', '14-day refund'],
    resumen="A single 16 GB plan, with a Ryzen 9 7950X and unlimited slots.",
    bueno=[
      "One product: 16 GB, no tiers or brackets to decode.",
      "Unlimited slots, so the number of players never pushes the price up.",
      "Paying the year upfront brings it down to €6.90 a month for the same 16 GB.",
    ],
    malo=[
      "If you only need 2 or 3 GB, you overpay: there's no small plan.",
      "The plan includes 30 GB of disk. Beyond that they charge €0.30 per GB per "
      "month, and a big modpack with backups eats through it.",
      "Nine locations in six countries: a smaller network than some rivals. From Spain, "
      "the closest are Frankfurt and Amsterdam.",
    ],
    veredicto="At €14.90 a month for 16 GB it competes with the cheapest per gigabyte, "
              "with a better CPU than most; paying the year it drops to €6.90. If you "
              "only need 2 or 3 GB, you're paying for RAM you won't use and almost any "
              "other host is cheaper.",
  ),

  "shockbyte": dict(
    pais="Australia",
    rasgos=['One of the best known', '72-hour refund'],
    resumen="One of the best-known names in the business. For Minecraft it charges per gigabyte, from $2.79.",
    bueno=[
      "Years in the business and lots of people using it: plenty of reviews out there.",
      "The entry plan is cheap: 1 GB for $2.79.",
    ],
    malo=[
      "For Minecraft it charges per gigabyte, so growing gets expensive: 16 GB comes to $47.",
      "Their 30% discount is already baked into the advertised price, so watch out when comparing.",
    ],
    veredicto="A good option to start with a small server. It gets expensive as soon as "
              "you need RAM, because every gigabyte is charged.",
  ),

  "bisect": dict(
    pais="United States",
    rasgos=['Spanish-language site', 'Prices in euros', 'CurseForge modpacks'],
    resumen="Flat, crystal-clear per-gigabyte pricing: €2.69 per GB, no surprises.",
    bueno=[
      "The price is a straight line: you know exactly what you'll pay.",
      "A Spanish-language site and prices in euros, which is rare in this business.",
      "Tightly integrated with CurseForge modpacks.",
    ],
    malo=[
      "One of the most expensive per gigabyte of those I've looked at.",
      "16 GB comes to €43.04 a month, more than three times PebbleHost Budget.",
      "In September 2026 it went up from €2.66 to €2.69 per GB. Not much, but up.",
    ],
    veredicto="Their pricing transparency is among the best. The problem is that once "
              "you do the maths, it's expensive.",
  ),

  "apex": dict(
    pais="United States",
    rasgos=['24/7 support', 'Merged with MCProHosting', 'Dedicated vCores on the EX range'],
    resumen="A big brand with lots of marketing. Also one of the most expensive in the comparison.",
    bueno=[
      "24/7 support with a good reputation and loads of one-click modpacks.",
      "MCProHosting has merged into them, so they're even bigger now.",
      "Their 16 GB EX range comes with dedicated vCores, not shared ones.",
    ],
    malo=[
      "The most expensive of all: $71.99 a month for 16 GB.",
      "The 25% discount they advertise only applies to the first month.",
    ],
    veredicto="You pay for brand and support. If that matters more to you than price, go "
              "ahead; if you're watching the euro, there are options four and a half times "
              "cheaper for the same RAM.",
  ),

  "hostinger": dict(
    pais="Lithuania",
    rasgos=['Spanish-language support', 'European billing', 'VPS with root access'],
    resumen="A web hosting giant that also sells game servers, as VPSs.",
    bueno=[
      "A huge brand, with Spanish-language support and European billing.",
      "Plans come with more CPU and disk than average, because they're real VPSs.",
    ],
    malo=[
      "The headline price requires paying 24 MONTHS upfront.",
      "After that it renews at almost double: 16 GB goes from $13.99 to $28.99.",
      "Being a VPS, you have to manage more things yourself than on a game panel.",
    ],
    veredicto="Their offer looks like the best in the table until you read the fine print. "
              "With the renewal price in hand, it's middle of the pack.",
  ),

  "pebble-budget": dict(
    pais="United Kingdom",
    rasgos=['Cheapest per GB', 'Unlimited slots', 'No lock-in', 'Budget without backups'],
    resumen="Two ranges: Budget at $1 per GB, and Premium with a Ryzen 9 at $2.25.",
    bueno=[
      "Their Budget range is the cheapest I've found: $1 per gigabyte.",
      "Unlimited slots even on small plans.",
      "Monthly billing with no lock-in.",
    ],
    malo=[
      "The Budget range <strong>doesn't include automatic backups</strong>: those come "
      "with the Premium plan. That's what you're paying less for.",
      "The hardware is more modest — a Ryzen 7 5700X and DDR4 at 2133 MHz — and it "
      "shows with big modpacks.",
      "Moving up to Premium doubles the per-gigabyte price: from $1 to $2.25.",
    ],
    veredicto="For small servers without mods it's probably the best value there is. But "
              "remember the backups: if your world matters, either go Premium or back it up "
              "by hand. And once you need lots of gigabytes the maths flips, because it "
              "charges per GB with no cap.",
  ),

  "sparked": dict(
    pais="United States",
    rasgos=['Ryzen 9 7900 with DDR5', '1-day free trial', 'Three ranges'],
    resumen="Per-gigabyte pricing with modern hardware: Ryzen 9 7900 and DDR5.",
    bueno=[
      "Genuinely current hardware: a Ryzen 9 7900 with DDR5 memory.",
      "Flat, no-tricks per-GB price: $2.59.",
      "There's an Extreme range with a Ryzen 9 9900X for those who need it.",
      "A one-day free trial, no strings attached.",
    ],
    malo=[
      "Like everyone who charges per GB, scaling up gets expensive.",
      "Less well known, so there are fewer outside reviews.",
      "Backups are tight: three included, and more costs extra. Same with storage.",
    ],
    veredicto="A good middle-ground option if you want modern hardware without paying "
              "big-brand prices.",
  ),

  "nodecraft": dict(
    pais="United States",
    rasgos=['24-hour free trial', 'Official Hypixel partner', 'Phone verification required'],
    resumen="They rebuilt their site in September 2026: now they ask you three questions and assign you a plan.",
    bueno=[
      "A 24-hour free trial without paying anything.",
      "Their site no longer makes you choose between twenty plans: they ask how many of "
      "you there are and what you play, and tell you the plan. Handy if you have no idea "
      "about gigabytes.",
      "They're an official Hypixel partner and have been at this since 2013.",
      "Seven-day refund.",
    ],
    malo=[
      "<strong>They've gone up a lot</strong>: $4.99 per GB, among the most expensive "
      "I've looked at. Their 8 GB is $39.98 a month.",
      "The −30% they show is <strong>for the first month only</strong>.",
      "<strong>They ask you to verify your phone</strong> even for the free trial.",
      "Their Lite range, the one that starts when someone joins, still exists but "
      "<strong>they no longer publish its price</strong>: you have to ask.",
    ],
    veredicto="Having your server sized through questions is nice for beginners, and the "
              "24-hour trial helps you decide. But the price has gone to $4.99 per GB, and "
              "for that money there are plenty of better options in this table. If you're "
              "interested, make it the Lite range — and get the price in writing.",
  ),

  "holyhosting": dict(
    pais="Spain",
    rasgos=['Popular with creators', 'The −25% is first month only'],
    resumen="The one many Spanish creators use. $1.25 per GB at the real rate.",
    bueno=[
      "Over 200 creators use it, several of them very big Spanish ones. That means their "
      "servers handle events with lots of people joining at once.",
      "You get a portless .holy.gg subdomain, which is much easier to share with your "
      "community than an IP full of numbers.",
      "Site, panel and support in Spanish, which isn't the norm in this business.",
    ],
    malo=[
      "They advertise <strong>$0.95/GB</strong> on the homepage, but that's the "
      "<strong>first month</strong> price with their −25%. The real rate is $1.25/GB.",
      "The discount comes with an on-screen countdown, which is a way of rushing you so "
      "you don't do the maths for month two.",
    ],
    veredicto="If you run events or a community, their track record with creators is a "
              "strong argument and I'll give them that. But do the numbers at $1.25/GB, "
              "which is what you'll pay from the second month.",
  ),

  "vultam-standard": dict(
    pais="Estonia",
    rasgos=['Free trial', 'Daily backups', 'Three ranges', 'Standard is from 2015'],
    resumen="Three ranges: Standard at $1.75/GB, Advanced at $2.40 and Performance at $3.50.",
    bueno=[
      "They offer a <strong>free trial with no card required</strong>, and very few do "
      "that. You test it and you decide, without taking anyone's word for it.",
      "Daily backups included on both lower ranges, not just the expensive one.",
      "Nodes in France and Germany, which is what you want from Spain.",
    ],
    malo=[
      "The Standard range runs an <strong>Intel i7-6700K, a 2015 processor</strong>. Fine "
      "for vanilla with four friends; you'll feel it with a modpack.",
      "The Advanced range goes up to $2.40/GB, and at that price there's competition with "
      "newer hardware.",
      "The Performance range, with a Ryzen 9 5950X and backups every 12 hours, costs "
      "$3.50/GB: at that point it barely competes with anyone.",
    ],
    veredicto="The free trial is the reason to look at them: they let you check it yourself "
              "before spending a euro. Don't expect miracles with mods on Standard; that "
              "processor has some years on it.",
  ),

  "wisehosting": dict(
    pais="Estonia",
    rasgos=['Minecraft only', '50% off paying yearly', '7-day refund'],
    resumen="They only do Minecraft. $3/GB a month, or $1.50 paying the whole year.",
    bueno=[
      "They do <strong>Minecraft only</strong>, and you notice when you contact support: "
      "whoever answers knows what a modpack is.",
      "Seven days to ask for a refund.",
      "Paying the year it comes to $1.50/GB, which is competitive.",
    ],
    malo=[
      "At the monthly price it's <strong>$3/GB</strong>: <strong>triple</strong> the "
      "cheapest in this table. 8 GB comes to about $24 a month.",
      "To make it worthwhile you have to pay twelve months upfront, which is a bet before "
      "you know if you like the service.",
      "The plans are tight: the 4 GB one comes with <strong>a single backup</strong> and "
      "25 GB of disk.",
    ],
    veredicto="Paying month to month it's among the most expensive in the comparison, and "
              "nothing in the plan justifies it. It only makes sense if you pay the whole "
              "year, and even then I'd try another one on this list first.",
  ),

  "nexohost": dict(
    pais="Spain",
    rasgos=['Spanish', 'From €1/month', 'Tops out at 9 GB'],
    resumen="A Spanish host with plans from 1 to 9 GB, starting at €1 a month.",
    bueno=[
      "A Spanish company, with its own panel and Spanish-language support.",
      "Starts at <strong>€1 a month</strong>. To set something up and try it, it's next to nothing.",
      "Ryzen 7 3700X and NVMe: solid hardware for what they charge.",
    ],
    malo=[
      "Their biggest plan is <strong>9 GB</strong>. For a heavy modpack or a big "
      "community it falls short and you'll have to move.",
      "They don't publish where their data centres are, so I can't tell you what ping "
      "you'll get from Spain. I looked, and it isn't there.",
    ],
    veredicto="For a small, cheap server for friends, in Spanish, it's a very reasonable "
              "option. The day you need more than 9 GB, that's the end of the road.",
  ),

  "theminecrafthosting": dict(
    pais="United States",
    rasgos=['Paris node', 'A −60% coupon all year'],
    resumen="Prices vary by location. The Paris node is the one that matters here.",
    bueno=[
      "You can pick a node in <strong>Paris</strong>, about as close to Spain as you'll find.",
      "Unlimited storage and player slots.",
    ],
    malo=[
      "They run a <strong>−60% BLACKFRIDAY code all year round</strong> and call it "
      "“lifetime”. If a discount never goes away, the list price is decorative — and you "
      "don't know what you'll renew at.",
      "At full price their 16 GB is $35, among the most expensive in the comparison.",
    ],
    veredicto="A Black Friday running in September doesn't sit right with me. If you're "
              "interested, ask them <strong>in writing</strong> what it renews at before "
              "paying: the gap between $35 and $14 is no detail.",
  ),

  "godlike": dict(
    pais="Romania",
    rasgos=['Launcher that sets up the client',
            'Built-in mod installer', 'One-day free trial, no card',
            'You pick GB, slots and days'],
    resumen=("The one that asks least of you: a launcher that sets your friends' "
             "Minecraft up for them, mods in two clicks and a free day to try it with "
             "no card. Not cheap per GB: you pay for convenience."),
    bueno=[
      "<strong>Their launcher saves you the worst afternoon of the year.</strong> You sign "
      "in with your Godlike account and manage the server from there, but the real win is "
      "the set-up-client button: it installs the version and the mods the server runs. That "
      "kills the “everyone install the same thing, same version” problem that finishes off "
      "half the modded servers out there. Nobody else in this table has it.",
      "<strong>You build the plan yourself</strong>: gigabytes (2 to 33), slots (5 to 200) "
      "and <strong>days</strong> — 30, 90, 180 or 360. Hardly anyone lets you pick the "
      "duration: if the modpack will last you three months, you pay for three months and "
      "close it.",
      "<strong>Some of the best hardware around</strong>: latest-gen AMD Ryzen, up to the "
      "9950X3D, and NVMe drives. Minecraft leans on a single core, and that's where it shows.",
      "<strong>Up to three backups a day, free</strong>, restorable from the panel. "
      "Exactly what other budget hosts lack.",
      "They give you <strong>a free 2 GB server for a day</strong> to try the panel before "
      "paying anything.",
      "The panel was rebuilt in 2025: a console that filters errors, scheduled restarts and "
      "backups, a file editor, all the Minecraft settings on one screen with no SFTP, "
      "role-based permissions and a mod and plugin installer that checks versions. It "
      "works well on mobile and through a Discord bot too.",
      "For community owners: an in-game store in one click, a rating system to attract "
      "players, and several linked servers.",
      "Upgrade or downgrade instantly and pay only the difference. Paying upfront brings "
      "it down: −10% for 90 days, −15% for 180 and −20% for 360.",
      "Layered DDoS protection with Path.net, ten data centres (Europe included) and "
      "payment with almost any method, crypto included.",
    ],
    malo=[
      "<strong>It is not cheap per GB and I won't dress it up</strong>: €3.25 at the normal "
      "rate and €2.44 with the code, when the cheapest in this table is €1.00. You're "
      "paying for convenience, not for gigabytes. If you know your way around a panel and "
      "you want to spend little, there are options at less than half.",
      "<strong>Support doesn't speak Spanish.</strong> They answer in English, and they say "
      "themselves they lean on translation tools for other languages. It works, but know it "
      "going in.",
      "A young company, from 2021. In 2024 they had a refund complaint that ended up on "
      "Reddit; they explain it on their own site, which says something.",
      "The free server is for tinkering: one slot, and you have to renew it every three hours.",
    ],
    veredicto=("It is not the cheapest and I am not going to tell you it is. It is the "
               "easiest. You pay more per GB, yes. In exchange you get the launcher that "
               "sets the game up for your friends, mods in two clicks, daily backups, "
               "picking the days you pay for and a free day to try it. Of the 23 in this "
               "table, no one else gives you all of that together. If your time is worth "
               "anything, the maths changes. And if you just want to spend as little as "
               "possible and a bare panel does not scare you, look at Kinetic or NexoHost, "
               "at less than half per GB."),
  ),

  "gportal": dict(
    pais="Germany",
    rasgos=['Unlimited slots', '250 one-click modpacks', 'Tops out at 6 GB'],
    resumen="One of Europe's big names. For Minecraft it goes from 2 to 6 GB, with unlimited slots.",
    bueno=[
      "Unlimited player slots on every plan: more people joining never raises the price.",
      "Over 250 preinstalled one-click modpacks, which is great for setting up RLCraft or "
      "All the Mods without wrestling with files.",
      "Around since 2003 with data centres across Europe, so ping from Spain is among the best.",
      "Site, panel and support in Spanish.",
    ],
    malo=[
      "<strong>It tops out at 6 GB.</strong> For a big modpack or community you'll run "
      "out of room and have to move.",
      "The <strong>−25% is for the first period only</strong>. 6 GB starts at €11.25 "
      "and renews at €15.",
      "Per gigabyte it doesn't compare well: their 4 GB is €11.80, almost triple "
      "PebbleHost for the same RAM.",
    ],
    veredicto="If you want a modpack set up in two clicks, unlimited slots and good ping "
              "from Spain, it delivers and it's convenient. But you pay for that "
              "convenience: per gigabyte it's among the pricey ones, and with a 6 GB "
              "ceiling it's no place for a growing community.",
  ),

  "scalacube": dict(
    pais="Estonia",
    rasgos=['Unlimited slots', 'Free domain and MySQL', 'The −50% is first month only'],
    resumen="Tiers from 768 MB to 64 GB, at about $3 per GB, with unlimited slots.",
    bueno=[
      "Goes up to <strong>64 GB</strong>, more than almost anyone: if you run a big "
      "community, you won't run out of room.",
      "Unlimited player slots on every plan.",
      "A domain and a MySQL database are included at no extra cost, which many charge for.",
      "Supports modpacks, plugins, BungeeCord and custom JARs.",
    ],
    malo=[
      "At $3 per GB they're <strong>above average</strong> for this table.",
      "The <strong>−50% is for the first month only</strong>, and the headline price comes from it.",
      "Their tiers are odd (768 MB, 1.5 GB, 4.5 GB): check carefully which one really "
      "covers what you need.",
    ],
    veredicto="If you need a lot of RAM or unlimited slots, they're among the highest in "
              "the comparison and that isn't easy to find. For a small server, there are "
              "cheaper options right here for that money.",
  ),

  "ggservers": dict(
    pais="Canada",
    rasgos=['Java and Bedrock', 'Two ranges', 'Standard runs DDR4 2133'],
    resumen="Two ranges pegged at $3 and $6 per GB, with one-click modpacks.",
    bueno=[
      "The price is simple arithmetic, no surprises: $3 per GB on Standard and $6 on Premium.",
      "Java and Bedrock, one-click modpacks and plugins, and full FTP and MySQL access.",
      "Around since 2013, with 24-hour chat support.",
    ],
    malo=[
      "The Standard range runs <strong>DDR4 at 2133 MHz and a regular SSD</strong>: "
      "you'll feel it with a big modpack.",
      "Premium, which does have NVMe and a fast CPU, <strong>costs double</strong>: $6 "
      "per GB, among the most expensive here.",
      "Their welcome coupon is <strong>for the first invoice only</strong>.",
    ],
    veredicto="Standard is fine for vanilla or a few plugins, and for that price you can "
              "do better. Premium has good hardware, but at $6 per GB you'd have to really "
              "like them.",
  ),

  "kinetic": dict(
    pais="United Kingdom",
    rasgos=['Under $1 per GB', '7-day refund', 'Starts at 4 GB'],
    resumen="Among the cheapest per gigabyte: 8 GB for $7.99, with backups and game switching.",
    bueno=[
      "<strong>About $0.99 per GB</strong>: going toe to toe with PebbleHost Budget for "
      "cheapest, and here backups are included.",
      "Five backups included and crash detection that alerts you.",
      "You can <strong>switch games whenever you like</strong> without paying again.",
      "A seven-day, no-questions refund.",
      "Goes up to 124 GB, so there's room to grow.",
    ],
    malo=[
      "<strong>Their smallest plan is 4 GB.</strong> If you want 1 or 2 GB for four "
      "friends, it isn't here.",
      "They don't list the exact CPU model on the pricing page: you have to check their "
      "specs section.",
      "A less-known brand than the big ones, so fewer outside reviews.",
    ],
    veredicto="On price it's among the best in the whole table, and unlike PebbleHost "
              "Budget the backups are included. If you need 4 GB or more, it's one of the "
              "first I'd look at; below that, it doesn't exist.",
  ),

  "realms": dict(
    pais="Sweden",
    rasgos=["Mojang's official one", 'No mods or plugins', '10-player cap'],
    resumen="Mojang's official option. Dead simple, but no mods and a player cap.",
    bueno=[
      "It's Mojang's: you subscribe from inside the game and there's nothing to set up.",
      "It never breaks when Minecraft updates, because the update is theirs.",
      "It keeps three worlds and your friends can join even when you're offline.",
    ],
    malo=[
      "<strong>No plugins or mods.</strong> No Paper, no Forge, no Fabric.",
      "A cap of <strong>10 players at once</strong>, and paying more doesn't raise it.",
      "It isn't sold by RAM, so if it falls short there's no way to give it more.",
    ],
    veredicto="If all you want is to play with four friends without any hassle, it's the "
              "simplest option there is and I have no complaints. The moment you want a "
              "plugin, a mod or fifteen people, you'll have to move.",
  ),

  "akliz": dict(
    pais="United States",
    rasgos=['Hands-on support', 'Backups twice a day', '7-day refund'],
    resumen="Managed hosting at $5 per GB: you pay more to get help setting it up.",
    bueno=[
      "Their strength is support: they focus on helping you set the server up, not just "
      "handing you a panel.",
      "Automatic backups <strong>twice a day</strong> and automatic restarts on every plan.",
      "Unlimited players and several servers per plan (from 4 GB you can run two at once).",
      "Over 600 one-click modpacks and a full refund in the first 7 days.",
      "They've been at it since 2006.",
    ],
    malo=[
      "<strong>$5 per GB</strong>: among the most expensive in the comparison. 8 GB is $40 a month.",
      "They sometimes show 20% off without explaining on what terms.",
      "They don't list the CPU model on their pricing page.",
      "Their biggest standard plan is 24 GB; beyond that you have to ask for a quote.",
    ],
    veredicto="It makes sense if you've never set up a server and want someone to hold "
              "your hand. If you know what you're doing, you get the same GB for half the "
              "money elsewhere on this list.",
  ),

  "hosthavoc": dict(
    pais="Canada",
    rasgos=['Data centres in London, Amsterdam and Frankfurt', '72-hour guarantee', 'NVMe on every plan'],
    resumen="$5 per GB with NVMe disks and 13 data centres, three of them in Europe.",
    bueno=[
      "They have data centres in <strong>London, Amsterdam and Frankfurt</strong>: from "
      "Spain the ping will be good.",
      "NVMe disks on every plan and their own hardware (not rented).",
      "Free dedicated IP from 6 GB.",
      "A 72-hour guarantee on every new order.",
    ],
    malo=[
      "<strong>$5 per GB</strong> at the regular price: expensive for what's in the table.",
      "The 25% they advertise is a <strong>seasonal promotion</strong> (code SUMMER), "
      "not the usual price.",
      "Below 6 GB, a dedicated IP costs $4 more a month.",
      "They don't list the CPU model on the Minecraft page.",
    ],
    veredicto="A serious host with a good presence in Europe, but at the regular price "
              "you pay double per GB compared with the cheapest in the table. If you "
              "catch the promotion, it gets close to average.",
  ),

  "serverminer": dict(
    pais="United Kingdom",
    rasgos=['Prices in euros', 'Player cap per plan', 'Discount for 3 or 6 months'],
    resumen="Fixed plans priced in euros, each with a player cap.",
    bueno=[
      "They charge <strong>in euros</strong>: what you see is what you pay, no currency conversion.",
      "10% off paying for 3 months and 15% for 6.",
      "They have data centres in Germany and Finland.",
      "No contract: cancel whenever you like.",
      "A British company registered since 2012.",
    ],
    malo=[
      "<strong>Every plan has a player cap</strong>: 15 on the smallest, 100 on the "
      "biggest. Almost everywhere else in the table it's unlimited.",
      "About €4.30 per GB: on the expensive side.",
      "Their biggest plan is 10 GB: not enough for very heavy modpacks.",
      "A dedicated IP and help with plugins or modpacks are paid extras.",
    ],
    veredicto="Paying in euros is handy, but for that money there are hosts with more RAM "
              "and no player cap. I'd only look at it if you already know them.",
  ),

  "bloom": dict(
    pais="United States",
    rasgos=['Data centre in Germany', 'Up to Ryzen 9 9950X', 'Backups you can mount from the panel'],
    resumen="Three ranges: a cheap Essentials, and Performance and Performance+ with dedicated cores.",
    bueno=[
      "They have a data centre in <strong>Falkenstein (Germany)</strong>: good ping from Spain.",
      "On Performance and Performance+ the <strong>cores are dedicated</strong>, not "
      "shared with other customers.",
      "Performance+ runs a <strong>Ryzen 9 9950X</strong> (7950X3D in Germany), among "
      "the fastest there is for Minecraft.",
      "Their backup system lets you open a backup as a folder and restore a single file "
      "from the panel.",
      "Every plan lets you create extra servers at no extra cost (Discord bots, websites, "
      "other games).",
    ],
    malo=[
      "Essentials starts at 4 GB and uses <strong>shared cores</strong> with older CPUs "
      "(Ryzen 9 3900X outside Germany).",
      "About $2.75 per GB on Performance and $3.50 on Performance+: mid-to-high pricing.",
      "Their Performance+ coupon is <strong>for the first invoice only</strong>.",
      "I couldn't find their refund policy or founding year on their site.",
    ],
    veredicto="Very good hardware and a data centre in Germany. Performance+ is among the "
              "best for a demanding server if you can afford it; for a small server with "
              "friends, there are cheaper options.",
  ),
}
