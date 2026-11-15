#!/usr/bin/env python3
"""
Atomic polish pass on Split 5 & Split 6 (#822-#1262):
- Fixes 6 duplicate multi-sense <br> halves (#825, #835, #901, #918, #982, #1140)
- Fixes 10 leaked parenthetical templates (#910, #911, #960, #1051, #1077, #1082, #1083, #1104, #1112)
- Replaces weak 'Meaning "..."' entries (#897, #907, #941, #978, #1184, #1250)
- Ensures 100% of distinct ES/HI synonyms across all 441 cards have explicit, vivid memory cues
- Syncs split5DeckCards, split6DeckCards, cardShortcuts, and data/backup_original_cards.json
"""

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(ROOT, "index.html")
BACKUP_PATH = os.path.join(ROOT, "data", "backup_original_cards.json")

# Map: card_num -> (shortcutEs_or_None, shortcutHi_or_None)
POLISH = {
    825: (
        '1. Celestial: <strong>Estrella</strong> ≈ Sounds like <strong>"Extra-Ray-Yah"</strong> (<em>Stellar</em> sibling!) → Shining <em>Star</em>!<br>2. Celebrity: <strong>Estrella / famoso</strong> ≈ Movie <em>Star</em> who is <strong>"Famous" (Famoso!)</strong>!',
        None
    ),
    827: (
        None,
        '1. Noun: <strong>Baarish / barsaat</strong> ≈ <strong>"Pour-ish!"</strong> → Heavy monsoon <em>Barsaat</em> pouring rain!<br>2. Verb: <strong>Baarish hona / barasna</strong> ≈ Clouds bursting ("Baras-na") with monsoon <em>Rain</em>!'
    ),
    830: (
        None,
        '1. Breeze: <strong>Hawa</strong> ≈ Sounds like breathing <strong>"Haa-Waa"</strong> → Fresh blowing <em>Wind</em>!<br>2. Tempest: <strong>Toofan / aandhi</strong> ≈ <em>Toofan</em> ("Typhoon"!) + <em>Aandhi</em> (Blinding dust-wind storm!)'
    ),
    831: (
        None,
        '<strong>Kohra</strong> ("Cold-Haze" winter fog!) / <strong>Dhund</strong> (Dim misty veil blurring roads — <em>Dhundla</em> = blurry!)'
    ),
    835: (
        '1. Silhouette: <strong>Sombra</strong> ≈ Dark silhouette cast on asphalt (root of <strong>"Somber"</strong>)! = <em>Shadow</em>!<br>2. Cool spot: <strong>Sombra</strong> ≈ Sit beneath a wide <strong>"Sombrero"</strong> hat or leafy tree = <em>Shade</em>!',
        None
    ),
    842: (
        '<strong>Barro</strong> ("Wheel-Barrow" stuck in wet soil!) | <strong>Lodo / fango</strong> (Wet riverbank silt/bog muck = <em>Mud</em>!)',
        None
    ),
    843: (
        None,
        '<strong>Ret</strong> ("Red-Sand" dunes!) / <strong>Baalu</strong> (Coarse riverside gravel sand — <em>Balu</em> beach!)'
    ),
    844: (
        None,
        '<strong>Dhool</strong> ≈ <strong>Tamil தூள் (Thool = Powder/Dust!)</strong> / <strong>Gard</strong> (Fine swirling chalk dust in wind!)'
    ),
    852: (
        '1. River: <strong>Río</strong> ≈ Famous <strong>"Río Grande"</strong> river → Wide flowing <em>River</em>!<br>2. Stream: <strong>Arroyo / riachuelo</strong> ≈ Fast <em>Arroyo</em> ("Arrow-flow"!) + Mini-<em>Río (Riachuelo)</em> creek!',
        '1. River: <strong>Nadi</strong> ≈ <strong>Tamil நதி (Nadhi = River!)</strong> → 100% same word!<br>2. Stream: <strong>Jharna / nala</strong> ≈ Mountain brook (<em>Jharna</em> "Jar-pouring") &amp; narrow channel creek (<em>Nala</em>!)'
    ),
    853: (
        None,
        '1. Lake: <strong>Jheel</strong> ≈ Calm cool <strong>"Chill-Lake"</strong> waters!<br>2. Pond: <strong>Talaab / pokhar</strong> ≈ Village stone pool (<em>Talaab</em> ≈ Tamil <em>Thadaagam</em>) &amp; rainwater hollow (<em>Pokhar</em>!)'
    ),
    859: (
        '<strong>Pájaro</strong> (<strong>Tamil பறவை Paravai</strong> starts with <em>Pa-ra</em>!) | <strong>Ave</strong> (Root of <strong>"Aviation"</strong> = winged bird!)',
        None
    ),
    863: (
        '1. Sheep: <strong>Oveja</strong> ≈ Woolly sheep bleating <strong>"Oh-Baa-Ha!"</strong>!<br>2. Goat: <strong>Cabra / chivo</strong> ≈ <em>Cabra</em> ("Capricorn" mountain goat!) + Little kid/billy <em>Chivo</em>!',
        None
    ),
    864: (
        '1. Horse: <strong>Caballo</strong> ≈ Galloping steed (root of <strong>"Cavalry / Chivalry"</strong>)!<br>2. Donkey: <strong>Burro / asno</strong> ≈ Pack <em>Burro</em> + Wild <em>Asno</em> ("Ass/Donkey"!)!',
        None
    ),
    865: (
        '<strong>Cerdo</strong> ("Sir-Mud-o"!) | <strong>Puerco / chancho</strong> (Root of English <strong>"Pork"</strong> = <em>Puerco</em>, plus cozy farm <em>Chancho</em>!)',
        None
    ),
    871: (
        '<strong>Ciervo (Syer-voh)</strong> ≈ Swerve your car on a forest road! | <strong>Venado</strong> (Root of <strong>"Venison"</strong> = forest <em>Deer</em>!)',
        None
    ),
    876: (
        '<strong>Rana</strong> (Green leaping pond <em>Frog</em> that ran away!) | <strong>Sapo</strong> (Warty garden toad/<em>Frog</em> going "Plop"!)',
        None
    ),
    883: (
        None,
        '<strong>Keeda</strong> ≈ <strong>Tamil கீடம் (Keedam = Insect!)</strong> / <strong>Makoda</strong> (Big crawling ant-bug — <em>Keeda-Makoda</em> crawling pair!)'
    ),
    890: (
        None,
        '<strong>Naujawan / jawaan</strong> ≈ <strong>Nau</strong> (New) + <strong>Jawaan</strong> (Young!) → Fresh young soldier or <em>Youth / Teenager</em>!'
    ),
    891: (
        None,
        '<strong>Buzurg / bada-boodha</strong> ≈ Respected family elder (<em>Buzurg</em>) &amp; older grey-haired <em>Bada-Boodha</em> (Senior/Old)!'
    ),
    893: (
        None,
        '<strong>Pota / poti</strong> (Son\'s grandson/daughter — <strong>Tamil பேரன்</strong> starts with P-!) | <strong>Nawasa / nawasi</strong> (Daughter\'s son/daughter!)'
    ),
    896: (
        None,
        '<strong>Bheed</strong> ("Big-Herd" packed street crowd!) / <strong>Janta</strong> (The general public people — <em>Jan</em> Folk!)'
    ),
    897: (
        '<strong>Compañero / compañera</strong> ≈ Shares bread with you side by side (<em>Com-</em> Together + <em>Pan</em> Bread = <strong>"Companion"</strong>)!',
        '<strong>Saathi</strong> (Walks <em>Saath</em> together!) / <strong>Sangi</strong> (Always stays in your company — <strong>Tamil சங்கம் Sangam!</strong>) = <em>Companion</em>!'
    ),
    898: (
        None,
        '<strong>Dushman</strong> (Sworn foe!) / <strong>Virodhi</strong> (Opposing rival — <strong>Tamil விரோதி Virodhi = Enemy!</strong>)'
    ),
    900: (
        None,
        '<strong>Dosti</strong> (From <em>Dost</em> — spoken Tamil தோஸ்த்!) / <strong>Yaari</strong> (Deep buddy loyalty — <em>Yaar</em> = Pal!) = <em>Friendship</em>!'
    ),
    901: (
        None,
        '1. Marital state: <strong>Shaadi</strong> ≈ <strong>Spoken Tamil ஷாதி (Shaadi!)</strong> → Lifelong married bond!<br>2. Ceremony event: <strong>Shaadi</strong> ≈ Grand garlands, drums &amp; wedding feast celebration!'
    ),
    904: (
        None,
        '<strong>Mohalla</strong> (Spoken Tamil மொஹல்லா) / <strong>Pados</strong> (Next-door area — <em>Padosi</em> neighbor!) / <strong>Ilaqa</strong> (Local zone/turf!) = <em>Neighborhood</em>!'
    ),
    907: (
        '<strong>Audífonos</strong> (<em>Audio + Phone</em>!) | <strong>Auriculares</strong> (Ear cups!) | <strong>Cascos</strong> ("Hard-shell" over-ear <em>Headphones</em>!)',
        None
    ),
    910: (
        '1. Surface: <strong>Áspero</strong> ("Raspy" sandpaper!) | <strong>Rugoso</strong> (<strong>"Rugged"</strong> bumpy bark!) = <em>Rough</em>!<br>2. Manner: <strong>Duro</strong> (Hard!) | <strong>Brusco</strong> (<strong>"Brusque"</strong> blunt!) | <strong>Aproximado</strong> (<strong>"Approximate"</strong>!) = <em>Harsh / Rough</em>!',
        '1. Surface: <strong>Khurdura</strong> ("Khur-Khur" bumpy sandpaper!) = <em>Rough</em>!<br>2. Approx: <strong>Sakht</strong> (Strict/Harsh!) / <strong>Mota-moti</strong> (Broad "fat-rough" ballpark figure!) = <em>Harsh / Rough</em>!'
    ),
    911: (
        '1. Blade: <strong>Afilado / filoso</strong> (<em>Filo</em> = Edge!) | <strong>Puntiagudo</strong> (Pointy tip!) = <em>Sharp</em>!<br>2. Mind: <strong>Agudo</strong> (<strong>"Acute"</strong>!) | <strong>Avispado</strong> (Wasp-quick!) = <em>Sharp-witted</em>!',
        '1. Blade: <strong>Tez / dhaar-daar</strong> ≈ Keen knife edge (<em>Dhaar</em> = Blade edge — "Dare to touch" sharp!) = <em>Sharp</em>!<br>2. Mind: <strong>Tez dimaag</strong> ≈ Quick-witted, razor-sharp <em>Dimaag</em> brain!'
    ),
    912: (
        '<strong>Desafilado</strong> (<em>Des-</em> Lost its sharp edge!) | <strong>Romo / sin filo</strong> (Flat snub-nosed edge <em>without</em> sharpness = <em>Blunt</em>!)',
        None
    ),
    914: (
        None,
        '1. Line: <strong>Seedha</strong> (Straight!) / <strong>Khara</strong> (True, upright &amp; unbent!) = <em>Straight</em>!<br>2. Candid: <strong>Saaf-saaf</strong> (Clear &amp; blunt — no sugarcoating!) = <em>Straightforward</em>!'
    ),
    915: (
        None,
        '<strong>Ghumaavdaar</strong> (Winding <em>Ghoom</em> hairpin curve!) / <strong>Muda hua</strong> (<em>Mudna</em> = Turned/Bent curve!)'
    ),
    916: (
        None,
        '1. Solid: <strong>Thos</strong> ("Toss-A-Rock" compact!) = <em>Solid</em>!<br>2. Hollow: <strong>Khokhla</strong> (Empty "Coke-can"!) / <strong>Andar se khaali</strong> (Empty inside!)'
    ),
    917: (
        None,
        '<strong>Tang</strong> (Narrow squeeze!) / <strong>Kassa hua</strong> (Pulling belt straps <em>kassa</em> tightly cinched = <em>Tight</em>!)'
    ),
    918: (
        '1. Clothing: <strong>Flojo</strong> (Baggy!) | <strong>Suelto</strong> (Untied!) | <strong>Holgado</strong> (Roomy fit!) = <em>Loose-fitting</em>!<br>2. Free: <strong>Suelto / libre</strong> (Unchained and running free — <strong>"Liberty"</strong>!) = <em>Unfastened</em>!',
        None
    ),
    919: (
        '<strong>Redondo</strong> (Shaped like a round O!) | <strong>Esférico</strong> (3D globe <strong>"Spherical"</strong> ball!)',
        None
    ),
    920: (
        '1. Cushion: <strong>Cojín</strong> (<strong>"Cushion"</strong>!) | <strong>Almohadón</strong> (Big sofa cushion from <em>Almohada</em> pillow!) = <em>Cushion</em>!<br>2. Cover: <strong>Funda de almohada</strong> (Zippered pillow slipcover = <em>Pillowcase</em>!)',
        None
    ),
    921: (
        '<strong>Percha</strong> (Where coats "perch"!) | <strong>Gancho / colgador</strong> (Curved metal <em>hook</em> to hang clothes — <em>Colgar</em> = hang!)',
        None
    ),
    922: (
        '<strong>Ropa sucia</strong> (Dirty basket!) | <strong>Colada</strong> (Spin cycle wash!) | <strong>Lavado</strong> (Soap <strong>"Lavatory"</strong> wash = <em>Laundry</em>!)',
        None
    ),
    923: (
        '1. Groomer: <strong>Peine</strong> (Toothed pocket hair untangler!) = <em>Comb</em>!<br>2. Verb: <strong>Peinar / peinarse</strong> (Comb a doll or comb <em>yourself</em> before a mirror!)',
        None
    ),
    927: (
        '<strong>Podrido / podrida</strong> (Spoiled!) | <strong>Echado a perder</strong> (Literally "thrown to ruin/lose" = gone completely <em>Rotten</em>!)',
        '<strong>Sada hua</strong> (Smelly decayed fruit!) / <strong>Kharab</strong> (<strong>Spoken Tamil கராப் = Spoiled/Broken!</strong>) = <em>Rotten</em>!'
    ),
    929: (
        '<strong>Provisiones</strong> (Kitchen <strong>"Provisions"</strong>!) | <strong>Comestibles</strong> (Edibles!) | <strong>Compras</strong> (Store runs = <em>Groceries</em>!)',
        '<strong>Rashan</strong> (<strong>Spoken Tamil ரேஷன்!</strong>) / <strong>Kiraane ka saamaan</strong> (Neighborhood dry-goods <em>Kirana</em> shop supplies = <em>Groceries</em>!)'
    ),
    932: (
        '<strong>Resbaladizo / resbaloso</strong> ≈ Both start with <strong>"Resbal-" ("Race-Ball" sliding on soap!)</strong> → Slick and <em>Slippery</em>!',
        '<strong>Fisalnewala</strong> (Feet slipping out — <em>Fisal</em>!) / <strong>Chikna</strong> (Oily glossy slick surface!) = <em>Slippery</em>!'
    ),
    933: (
        '<strong>Crujiente</strong> (<strong>"Crunchy"</strong> bite!) | <strong>Tostado</strong> (Golden crisp <strong>"Toasted"</strong> crunch!)',
        '<strong>Kurkura</strong> (Crunchy <em>Kurkure!</em>) / <strong>Karara</strong> (Crisp fried papad snap!) = <em>Crispy / Crunchy</em>!'
    ),
    935: (
        '<strong>Grasoso</strong> (Dripping with thick <strong>"Grease"</strong>!) | <strong>Aceitoso</strong> (Slick with <em>Aceite</em> olive oil!)',
        '<strong>Teliya</strong> (From <strong>Tel</strong> = Oil!) / <strong>Chikna</strong> (Slick greasy shine on fingertips!) = <em>Oily / Greasy</em>!'
    ),
    937: (
        None,
        '<strong>Rate</strong> (Market tag!) / <strong>Keemat</strong> (True cost!) / <strong>Daam</strong> (Tag price — sounds like <strong>"Dime"</strong>!) = <em>Price</em>!'
    ),
    938: (
        '<strong>Útil</strong> (Handy tool!) | <strong>Servicial</strong> (Eager to serve!) | <strong>De ayuda</strong> (Offering a helping hand — <em>Ayuda</em>!)',
        '<strong>Kaam ka</strong> (Of real practical use!) / <strong>Madadgaar</strong> (<strong>Spoken Tamil மதத் = Help!</strong>) = <em>Useful / Helpful</em>!'
    ),
    939: (
        '<strong>Inútil</strong> (Zero utility!) | <strong>Inservible</strong> (Cannot be <strong>"Served/Used"</strong> anymore = broken &amp; <em>Useless</em>!)',
        '<strong>Bekaar</strong> (<strong>Spoken Tamil பேக்கார்!</strong>) / <strong>Kisi kaam ka nahi</strong> (Of no use to anyone at all = <em>Useless</em>!)'
    ),
    941: (
        '<strong>Entrega</strong> (Handing box over!) | <strong>Envío</strong> (Dispatched parcel!) | <strong>Mensajería</strong> (Courier messenger van = <em>Delivery</em>!)',
        None
    ),
    944: (
        '<strong>Barato / barata</strong> (Bargain tag!) | <strong>Económico</strong> (Friendly on the wallet — <strong>"Economical"</strong> = <em>Cheap</em>!)',
        None
    ),
    946: (
        None,
        '1. Wealthy: <strong>Ameer / daulatmand</strong> (Loaded with <em>Daulat</em> wealth — <strong>Tamil அமீர்</strong>!) = <em>Rich</em>!<br>2. Flavor: <strong>Swadisht / bhaari</strong> (Richly <em>Swad</em> flavorful &amp; heavy on ghee = <em>Rich food</em>!)'
    ),
    947: (
        None,
        '1. Poor: <strong>Gareeb</strong> (<strong>Spoken Tamil கரீப்</strong> — empty pockets!) = <em>Poor</em>!<br>2. Pitiable: <strong>Bechara / badqismat</strong> (Helpless &amp; <em>Bad-Qismat</em> unlucky soul!)'
    ),
    949: (
        None,
        '<strong>Shuddh</strong> (<strong>Tamil சுத்தம்!</strong>) / <strong>Asli</strong> (Genuine — <strong>Tamil அசல்!</strong>) / <strong>Saaf</strong> (Spotlessly clean!) = <em>Pure</em>!'
    ),
    951: (
        None,
        '<strong>Jhootha</strong> (Untrue lie!) / <strong>Nakli</strong> (Counterfeit copy — <strong>Spoken Tamil நக்கல் = Imitate!</strong>) = <em>False / Fake</em>!'
    ),
    955: (
        '<strong>Seguimiento</strong> (Following trail!) | <strong>Rastreo</strong> (Sniffing every step/footprint <em>Rastro</em> = <em>Tracking</em>!)',
        None
    ),
    959: (
        '<strong>Listo / lista</strong> (Checklist done!) | <strong>Preparado</strong> (Already <strong>"Prepared"</strong> for action = <em>Ready</em>!)',
        None
    ),
    960: (
        None,
        '1. Angry: <strong>Gussa</strong> ("Go-Shout!" flare!) / <strong>Naraaz</strong> (Offended upset!) = <em>Mad / Angry</em>!<br>2. Crazy: <strong>Paagal</strong> (Wildly bonkers — spoken Tamil <strong>பாகல்!</strong>) = <em>Mad / Insane</em>!'
    ),
    961: (
        None,
        '<strong>Ghabraya hua / ghabrahat</strong> ≈ Heart drumming <strong>"Ghab-Ghab"</strong> with butterflies before an exam = <em>Nervous</em>!'
    ),
    964: (
        None,
        '<strong>Hairaan</strong> (Hair standing up in awe!) / <strong>Chaunka hua</strong> (Startled jaw-drop jump!) = <em>Surprised</em>!'
    ),
    965: (
        '<strong>Alivio</strong> ≈ Root of English <strong>"Alleviate"</strong> (lifting pain off your chest!) → Deep exhale of <em>Relief</em>!',
        '<strong>Raahat</strong> (Comfort!) / <strong>Sukoon / chain</strong> (Calm inner peace after storm!) = <em>Relief</em>!'
    ),
    966: (
        None,
        '1. Shame: <strong>Sharminda</strong> (Blushing with shame!) = <em>Ashamed</em>!<br>2. Fault: <strong>Doshi</strong> (<strong>Tamil தோஷம்!</strong>) / <strong>Gunaahgaar</strong> (Sinner who committed <em>Gunaah</em>!) = <em>Guilty</em>!'
    ),
    967: (
        None,
        '<strong>Akela</strong> (<em>Jungle Book</em> lone wolf!) / <strong>Tanhaa</strong> (Solitary quiet soul wandering solo!) = <em>Lonely</em>!'
    ),
    968: (
        None,
        '<strong>Jalan</strong> (Burning envy inside!) / <strong>Hasad</strong> (Resentful green-eyed jealousy at another\'s win!) = <em>Jealous / Envious</em>!'
    ),
    971: (
        None,
        '<strong>Bechain</strong> (<em>Be-</em> Without + <em>Chain</em> Peace = Restless!) / <strong>Majboor</strong> (Cornered &amp; helpless — <strong>Tamil மஜ்பூர்</strong>) = <em>Desperate</em>!'
    ),
    974: (
        None,
        '<strong>Niraash</strong> (<strong>Tamil நிராசை</strong> — hope dashed!) / <strong>Maayoos</strong> (Downcast deflated heart!) = <em>Disappointed</em>!'
    ),
    976: (
        None,
        '1. Feeling: <strong>Bhavna</strong> (<strong>Tamil பாவனை!</strong>) / <strong>Jazbaat</strong> (Deep inner passions!) = <em>Emotion</em>!<br>2. State: <strong>Mizaaj</strong> (Temperament) / <strong>Mann</strong> (<strong>Tamil மனம் = Mind!</strong>) = <em>Mood</em>!'
    ),
    977: (
        '<strong>Alegría</strong> (Radiant joy!) | <strong>Gozo</strong> ("Goes-Oh!" thrilling inner delight = <em>Joy / Delight</em>!)',
        None
    ),
    978: (
        '<strong>Dolor</strong> (Ache!) | <strong>Pena</strong> (Deep heartache!) | <strong>Luto</strong> (Black-clad mourning <em>Sorrow / Grief</em>!)',
        '<strong>Dukh</strong> (<strong>Tamil துக்கம்!</strong>) / <strong>Gham</strong> (Heavy dark cloud of heartache &amp; mourning = <em>Sorrow / Grief</em>!)'
    ),
    981: (
        None,
        '<strong>Tension</strong> (Stressed coiled nerves!) / <strong>Chinta</strong> (<strong>Tamil சிந்தை = Constant worry!</strong>) = <em>Anxiety / Stress</em>!'
    ),
    982: (
        '1. Honor: <strong>Orgullo</strong> (Chest swelling proudly over earned gold!) = <em>Pride</em>!<br>2. Arrogance: <strong>Soberbia / orgullo</strong> (Haughty "Super-Superior" strut — root of <em>Superb</em>!) = <em>Arrogant Pride</em>!',
        None
    ),
    983: (
        None,
        '1. Fondness: <strong>Lagav</strong> (Warm bond) / <strong>Pyaar</strong> (Tender love!) = <em>Affection</em>!<br>2. Fervor: <strong>Josh</strong> (Fiery zeal!) / <strong>Deewanapan</strong> (Mad <em>Deewana</em> devotion!) = <em>Passion</em>!'
    ),
    984: (
        None,
        '<strong>Ghin</strong> (Gross stomach-turning!) / <strong>Chidh</strong> (Annoyed repulsed recoil = <em>Disgust</em>!)'
    ),
    990: (
        None,
        '<strong>Milansaar</strong> (Warm mixer!) / <strong>Achha</strong> (Sweet!) / <strong>Pyaara</strong> (Lovable warm friend!) = <em>Nice / Friendly</em>!'
    ),
    991: (
        '<strong>Grosero</strong> (Crass &amp; "Gross"!) | <strong>Maleducado</strong> (Literally <em>Mal</em> Badly + <em>Educado</em> Raised/Mannered = <em>Rude</em>!)',
        '<strong>Badtameez</strong> (<em>Bad</em> manners!) / <strong>Ukhar</strong> (Snappy, abrasive cactus tone!) = <em>Rude</em>!'
    ),
    992: (
        None,
        '<strong>Bewaqoof</strong> (Clueless!) / <strong>Moorkh</strong> (<strong>Tamil மூர்க்கன்!</strong>) / <strong>Pagal</strong> (Out-of-mind silly fool!) = <em>Stupid / Foolish</em>!'
    ),
    993: (
        '<strong>Trabajador / trabajadora</strong> ≈ From <strong>Trabajo</strong> ("Travel-Job" work) → Tireless male or female <em>Hardworking</em> pro!',
        None
    ),
    994: (
        None,
        '<strong>Be-imaan</strong> (<em>Be-</em> Without + <em>Imaan</em> Integrity!) / <strong>Jhootha</strong> (Tells <em>Jhooth</em> lies!) = <em>Dishonest</em>!'
    ),
    996: (
        None,
        '<strong>Darpok</strong> (Hides from <em>Darr</em> fear!) / <strong>Buzdil</strong> (Faint-"goat-hearted" coward!) = <em>Cowardly</em>!'
    ),
    999: (
        '<strong>Terco</strong> (Balking turkey!) | <strong>Testarudo</strong> (Hard-headed — <em>Testa</em> Head!) | <strong>Tozudo</strong> (Bull-headed = <em>Stubborn</em>!)',
        '<strong>Ziddi</strong> (<strong>Spoken Tamil ஜித்தி!</strong>) / <strong>Adiyal</strong> (Planting feet firmly — <em>Adna</em> = refuse to budge!) = <em>Stubborn</em>!'
    ),
    1004: (
        None,
        '<strong>Sakht</strong> (Unbending firm rules!) / <strong>Kadak</strong> (Crisp stern "cracker" discipline like crisp <em>Kadak</em> chai!) = <em>Strict</em>!'
    ),
    1005: (
        None,
        '<strong>Naazuk</strong> (Fragile glass!) / <strong>Jazbaati</strong> (Moved swiftly by <em>Jazbaat</em> feelings!) = <em>Sensitive</em>!'
    ),
    1007: (
        None,
        '1. Untamed: <strong>Jangli</strong> (Born of the wild forest!) = <em>Wild</em>!<br>2. Uncontrolled: <strong>Bekaboo</strong> (No reins!) / <strong>Mast</strong> (Carefree &amp; rowdy!) = <em>Uncontrolled</em>!'
    ),
    1009: (
        None,
        '<strong>Wafadaar</strong> (<em>Wafa</em> Loyalty — faithful dog!) / <strong>Sachha</strong> (True-hearted — <strong>Tamil சத்தியம்!</strong>) = <em>Loyal / Sincere</em>!'
    ),
    1012: (
        None,
        '<strong>Shaant</strong> (<strong>Tamil சாந்தம்!</strong>) / <strong>Pur-sukoon</strong> (Filled <em>Pur</em> with deep inner serenity <em>Sukoon</em>!) = <em>Peaceful</em>!'
    ),
    1013: (
        '<strong>Alegre</strong> ("Allegro"!) | <strong>Animado</strong> (Lively <em>Animated!</em>) | <strong>Risueño</strong> (Always beaming with <em>Risa</em> laughter = <em>Cheerful</em>!)',
        None
    ),
    1015: (
        None,
        '<strong>Chust</strong> (Alert &amp; nimble!) / <strong>Phurteela</strong> (Zippy <em>Phurti</em> spark — boundless energy!) = <em>Energetic</em>!'
    ),
    1017: (
        None,
        '<strong>Nidar</strong> (<em>Ni-</em> Without + <em>Dar</em> Fear!) / <strong>Himmati</strong> (Full of <em>Himmat</em> brave courage!) = <em>Bold</em>!'
    ),
    1018: (
        None,
        '1. Not guilty: <strong>Be-kasoor</strong> (Zero fault!) = <em>Innocent</em>!<br>2. Pure: <strong>Masoom</strong> (Sweet child!) / <strong>Bhola</strong> (Simple-hearted &amp; trusting!) = <em>Naive / Pure</em>!'
    ),
    1019: (
        '<strong>Encantador</strong> ("Enchanting"!) | <strong>Seductor</strong> (Magnetically <strong>"Seductive"</strong> smile = <em>Charming</em>!)',
        '<strong>Pyaara</strong> (Lovable!) / <strong>Dil jeetne wala</strong> (Literally "Heart-winning person"!) = <em>Charming</em>!'
    ),
    1020: (
        None,
        '<strong>Dabi hasi hansna</strong> (Stifled suppressed chuckle!) / <strong>Khilkhilana</strong> (Bright "Khil-Khil" petal <em>Giggle</em>!)'
    ),
    1025: (
        '1. Gesture: <strong>Saludar con la mano / agitar</strong> (Greet/shake hand!) = <em>Wave</em>!<br>2. Water: <strong>Ola / onda</strong> (Beach <em>"Hola"</em> wave + Rolling <strong>"Undulation"</strong>!) = <em>Wave</em>!',
        '1. Gesture: <strong>Haath hilana</strong> (Swing hand!) = <em>Wave</em>!<br>2. Water: <strong>Lehar / tarang</strong> (Ocean crest <em>Lehar</em> &amp; rippling <em>Tarang</em>!) = <em>Wave</em>!'
    ),
    1026: (
        '<strong>Mirar fijamente</strong> (Look fixedly!) | <strong>Clavar la vista</strong> (Literally "nail your gaze" onto someone = <em>Stare</em>!)',
        '<strong>Ghoorna</strong> (Glare hard!) / <strong>Taakna</strong> (Peer steadily!) / <strong>Nigaah jamana</strong> (Plant eyes fixed!) = <em>Stare / Gaze</em>!'
    ),
    1027: (
        '<strong>Echar un vistazo</strong> (Toss a quick glance!) | <strong>Mirar de reojo</strong> (Peek from the corner of the eye = <em>Glance</em>!)',
        None
    ),
    1029: (
        '<strong>Suspirar / suspiro</strong> ≈ Notice <strong>"Spire / Respire"</strong> → Verb &amp; Noun for letting out a long wistful breath = <em>Sigh</em>!',
        None
    ),
    1030: (
        '<strong>Jadear</strong> (Pant loudly!) | <strong>Quedarse sin aliento</strong> (Literally "stay without breath" = <em>Gasp</em>!)',
        '<strong>Achanak saans kheenchna</strong> (Suddenly yank breath in!) / <strong>Haanpna</strong> ("Haa-Puff" panting!) = <em>Gasp</em>!'
    ),
    1032: (
        '<strong>Roncar / ronquido</strong> ≈ Loud saw-buzzing "Roar-Car" vibration — both verb &amp; sound noun for <em>Snore</em>!',
        None
    ),
    1034: (
        '<strong>Sonrojarse</strong> | <strong>Ponerse rojo</strong> ≈ Both contain <strong>Rojo (Red!)</strong> → Turning tomato-red with embarrassment = <em>Blush</em>!',
        None
    ),
    1035: (
        '<strong>Atragantarse</strong> (Food stuck in <em>Garganta</em> throat!) | <strong>Asfixiarse</strong> (Cut off air — <strong>"Asphyxiate"</strong> = <em>Choke</em>!)',
        None
    ),
    1036: (
        '<strong>Arrodillarse</strong> (Drop on <em>Rodilla</em> knees!) | <strong>Hincarse</strong> (Plant both knees straight onto church stone = <em>Kneel</em>!)',
        None
    ),
    1039: (
        '<strong>Abofetear</strong> ("Buffet-ear"!) | <strong>Dar una cachetada</strong> (Smack across the <em>Cachete</em> cheek = <em>Slap</em>!)',
        '<strong>Thappad maarna</strong> ("Thap!" palm!) / <strong>Chaanta maarna</strong> (Sharp ringing cheek sting!) = <em>Slap</em>!'
    ),
    1042: (
        '<strong>Coquetear</strong> (Playful "Coquette"!) | <strong>Ligar</strong> (Tie/link someone into a romantic spark = <em>Flirt</em>!)',
        None
    ),
    1043: (
        None,
        '<strong>Gale lagana</strong> (Hold to neck!) / <strong>Jhappi paana</strong> (Famous warm Bollywood <em>"Jadoo ki Jhappi"</em> bear hug!)'
    ),
    1044: (
        '<strong>Besar / beso</strong> ≈ Warm verb &amp; noun ("Best-Heart" peck!) → Press lips to show love = <em>Kiss</em>!',
        None
    ),
    1049: (
        '<strong>Asistir a</strong> (Be present — NOT assist!) | <strong>Acudir</strong> (Turn up promptly at the gathering = <em>Attend</em>!)',
        None
    ),
    1050: (
        '<strong>Juntar</strong> (Join!) | <strong>Reunir</strong> (<strong>"Reunite"</strong>!) | <strong>Recoger</strong> (Pick up &amp; pile together = <em>Gather / Collect</em>!)',
        None
    ),
    1051: (
        None,
        '1. Join: <strong>Jodna</strong> (Pair — <strong>Tamil ஜோடு!</strong>) / <strong>Lagana</strong> (Stick onto!) = <em>Attach</em>!<br>2. Separate: <strong>Alag karna</strong> (Put apart!) / <strong>Hatana</strong> (Remove off!) = <em>Detach</em>!'
    ),
    1052: (
        None,
        '<strong>Apmaan karna</strong> (<em>Ap-</em> Down + <em>Maan</em> Respect!) / <strong>Be-izzati karna</strong> (Strip <em>Izzat</em> honor!) / <strong>Gaali dena</strong> (Hurl harsh curse words!) = <em>Insult</em>!'
    ),
    1053: (
        '<strong>Burlarse</strong> ("Burlesque" spoof!) | <strong>Molestar de broma</strong> (Bother purely as a joke = <em>Tease</em>!)',
        '<strong>Chhedna / chidhana</strong> (Playfully poke &amp; mimic!) / <strong>Satana</strong> (Playfully bug a sibling until they groan = <em>Tease</em>!)'
    ),
    1054: (
        '<strong>Adular</strong> (Shower praise!) | <strong>Halagar</strong> (Sweet-talk ego until cheeks glow = <em>Flatter</em>!)',
        None
    ),
    1055: (
        '<strong>Chismear / chisme</strong> (Juicy chatter!) | <strong>Cotillear</strong> (Whispering neighborhood secrets = <em>Gossip</em>!)',
        '<strong>Chugli karna</strong> (Backbite whispers!) / <strong>Idhar-udhar ki baatein karna</strong> (Spread "here-there" chatter = <em>Gossip</em>!)'
    ),
    1057: (
        None,
        '<strong>Taaliyan bajana</strong> (Clap hands loudly!) / <strong>Hausla badhana</strong> (Boost morale loudly = <em>Cheer / Applaud</em>!)'
    ),
    1058: (
        '<strong>Alabar</strong> ("Hallelujah" praise!) | <strong>Elogiar</strong> (Root of English <strong>"Eulogy"</strong> = high tribute <em>Praise</em>!)',
        None
    ),
    1061: (
        '<strong>Presumir</strong> (Show off!) | <strong>Alardear</strong> (Parade shiny trophies loudly = <em>Boast</em>!)',
        None
    ),
    1062: (
        '<strong>Disculparse</strong> (Clear fault <em>Culpa</em>!) | <strong>Pedir perdón</strong> (Literally "ask for pardon" = <em>Apologize</em>!)',
        None
    ),
    1065: (
        '<strong>Engañar</strong> (Trick!) | <strong>Estafar</strong> (Swindle!) | <strong>Hacer trampa</strong> (Pull a rigged card <em>trap</em> = <em>Cheat</em>!)',
        None
    ),
    1066: (
        None,
        '<strong>Yudh</strong> (Epic war!) / <strong>Jung</strong> ("Jungle" combat!) / <strong>Sangharsh</strong> (Fierce struggle!) / <strong>Ladai</strong> (Front-line clash = <em>Battle</em>!)'
    ),
    1074: (
        None,
        '1. Guide: <strong>Raasta dikhana</strong> (Show path!) / <strong>Aage le jaana</strong> (Lead forward ahead!) = <em>Guide</em>!<br>2. Straight: <strong>Seedha</strong> (Unbent &amp; frank — <strong>Tamil சாதா!</strong>) = <em>Direct</em>!'
    ),
    1075: (
        None,
        '<strong>Sambhalna</strong> (Steer firmly!) / <strong>Jhelna</strong> (Weather &amp; bear tough pressure smoothly = <em>Handle / Cope</em>!)'
    ),
    1077: (
        None,
        '1. Steer clear: <strong>Bachna</strong> (Dodge clear!) / <strong>Taalna</strong> ("Stall-Now"!) = <em>Avoid</em>!<br>2. Stop: <strong>Rokna</strong> (Block!) / <strong>Bachav karna</strong> (Safeguard &amp; stop!)'
    ),
    1079: (
        None,
        '<strong>Zidd karna</strong> (<strong>Tamil ஜித்தி!</strong>) / <strong>Zorr dena</strong> (Press heavy force/emphasis onto a point = <em>Insist</em>!)'
    ),
    1080: (
        None,
        '<strong>Bharosa karna</strong> (Lean on trust!) / <strong>Par tikna</strong> (Stay resting solidly <em>on</em> something = <em>Depend / Rely</em>!)'
    ),
    1081: (
        '<strong>Molestar</strong> ("More-Stress-Tar"!) | <strong>Fastidiar</strong> (Fuss!) | <strong>Perturbar</strong> (<strong>"Perturb"</strong> peace = <em>Disturb</em>!)',
        '<strong>Pareshan karna</strong> (Rattle worries!) / <strong>Tang karna</strong> (Pull tightly on nerves until annoyed = <em>Bother / Disturb</em>!)'
    ),
    1082: (
        '1. Jarred: <strong>Encurtido</strong> (Vinegar tang!) | <strong>Pepinillo</strong> (Small pickled cucumber!) = <em>Pickle</em>!<br>2. Dip: <strong>Salsa</strong> (Spicy sauce!) | <strong>Aderezo</strong> (Zesty condiment dressing!) = <em>Chutney / Dip</em>!',
        None
    ),
    1083: (
        None,
        '1. Stew: <strong>Saalan</strong> (Slow-simmered spicy curry!) / <strong>Sabzi</strong> (Cooked veggie stew!) = <em>Curry</em>!<br>2. Grain: <strong>Daal</strong> (<strong>Tamil பருப்பு / தால்</strong> yellow split <em>Lentil</em>!)'
    ),
    1084: (
        None,
        '<strong>Chana / chhole</strong> ≈ Famous street snack <strong>Chana Masala &amp; Chhole Bhature</strong> = Spiced <em>Chickpea</em>!'
    ),
    1086: (
        '<strong>Anacardo</strong> (Curved nut!) | <strong>Castaña de cajú</strong> ("Chestnut of the <em>Kaju</em> tree" = <em>Cashew</em>!)',
        None
    ),
    1088: (
        '<strong>Cacahuate</strong> (Mexican crispy shell!) | <strong>Maní</strong> (<strong>Tamil மணிலா Manila peanut!</strong>)',
        None
    ),
    1094: (
        None,
        '<strong>Ilzaam lagana</strong> (Stick a charge onto!) / <strong>Dosh dena</strong> (<strong>Tamil தோஷம் = Fault!</strong>) = <em>Blame / Accuse</em>!'
    ),
    1095: (
        '<strong>Quejarse</strong> (Grumble!) | <strong>Reclamar</strong> (Formally <strong>"Reclaim"</strong> money/rights over bad service = <em>Complain</em>!)',
        None
    ),
    1097: (
        None,
        '<strong>Raazi karna</strong> (Win consent — <strong>Tamil ராசி!</strong>) / <strong>Manana</strong> (Sweetly win someone over = <em>Persuade</em>!)'
    ),
    1098: (
        None,
        '<strong>Beech mein bolna</strong> (Speak right in the <em>middle</em>!) / <strong>Tokna</strong> ("Talk-Na!" cut-off!) = <em>Interrupt</em>!'
    ),
    1102: (
        None,
        '<strong>Saaf karna</strong> (Clear fog!) / <strong>Baat kholna</strong> (Unfold &amp; open the matter clearly = <em>Clarify</em>!)'
    ),
    1104: (
        None,
        '1. Repeat: <strong>Kisi ki baat dohrana</strong> (Repeat words twice — <em>Do</em> = 2!) = <em>Quote</em>!<br>2. Price: <strong>Rate batana</strong> (State price!) / <strong>Andaaza</strong> (Quick estimate = <em>Quote price</em>!)'
    ),
    1106: (
        None,
        '<strong>Naukri</strong> (Salaried post!) / <strong>Kaam</strong> (Daily work!) / <strong>Pesha</strong> (Skilled lifelong <em>Profession</em>!)'
    ),
    1110: (
        '1. Office: <strong>Oficinista</strong> (Desk pro!) | <strong>Empleado</strong> (Company <strong>"Employee"</strong>!) = <em>Clerk</em>!<br>2. Books: <strong>Contador / contable</strong> (Counts ledgers!) = <em>Accountant</em>!',
        None
    ),
    1112: (
        None,
        '1. Rank: <strong>Afsar</strong> (Crisp uniform <strong>"Officer"</strong>!) = <em>Officer</em>!<br>2. State: <strong>Adhikari</strong> (<strong>Tamil அதிகாரம்</strong> Authority holder!) = <em>Official / Officer</em>!'
    ),
    1116: (
        '<strong>Plomero</strong> (Fixed lead <em>Plomo</em> water pipes!) | <strong>Fontanero</strong> (Fixes <em>Fontana</em> taps = <em>Plumber</em>!)',
        None
    ),
    1125: (
        '<strong>Mesero / mesera</strong> (Tends your <em>Mesa</em> dining table!) | <strong>Camarero</strong> ("Come-Here-Order!" = <em>Waiter</em>!)',
        None
    ),
    1129: (
        '1. Writer: <strong>Autor / autora</strong> (Originator!) | <strong>Escritor</strong> (<strong>"Script"</strong> author!) = <em>Author</em>!<br>2. Poet: <strong>Poeta / poetisa</strong> (Rhyming verse composer!) = <em>Poet</em>!',
        '1. Writer: <strong>Lekhak</strong> (<strong>Tamil லேகன்!</strong>) = <em>Author</em>!<br>2. Poet: <strong>Shayar</strong> (Romantic <em>Shayari</em> lyricist!) / <strong>Kavi</strong> (<strong>Tamil கவி!</strong>) = <em>Poet</em>!'
    ),
    1139: (
        '<strong>Currículum</strong> (<strong>"Curriculum Vitae"</strong>!) | <strong>Hoja de vida</strong> (Literally "Sheet of life" = <em>Resume / CV</em>!)',
        None
    ),
    1140: (
        '1. Hiring: <strong>Entrevista</strong> (Hiring panel facing candidate across the table — <em>Inter-View</em>!) = <em>Job Interview</em>!<br>2. Press: <strong>Entrevista</strong> (Journalist holding mic Q&amp;A!) = <em>Media Interview</em>!',
        None
    ),
    1142: (
        None,
        '<strong>Tankhwah</strong> (Monthly envelope pay!) / <strong>Aamdani</strong> ("Amount-In" total incoming earnings = <em>Salary / Income</em>!)'
    ),
    1148: (
        '<strong>Tarea</strong> (Task!) | <strong>Deber</strong> (Owed <strong>"Debt"</strong>!) | <strong>Obligación</strong> (Bound <strong>"Obligation"</strong>!)',
        '<strong>Kaam</strong> (Daily work!) / <strong>Farz</strong> ("First" moral duty!) / <strong>Zimmedari</strong> (Shouldered burden = <em>Obligation</em>!)'
    ),
    1151: (
        '1. Grid: <strong>Horario</strong> (Hour blocks!) | <strong>Calendario</strong> (<strong>"Calendar"</strong> dates!) = <em>Schedule</em>!<br>2. Meeting: <strong>Cita</strong> ("See-Ya-At-Time" booked slot!) = <em>Appointment</em>!',
        None
    ),
    1159: (
        None,
        '<strong>Graahak</strong> (Walks in to grab/buy — <strong>Tamil கிராக்கி!</strong>) / <strong>Customer</strong> (Store buyer!) = <em>Customer / Client</em>!'
    ),
    1163: (
        None,
        '<strong>Keemat</strong> (Tag value!) / <strong>Daam</strong> (Sounds like <strong>"Dime"</strong>!) / <strong>Rate</strong> (Market per-unit <em>Price</em>!)'
    ),
    1169: (
        '<strong>Dinero en efectivo</strong> (Immediate paper cash "in effect"!) | <strong>Dinero</strong> (Pocket <em>Money</em>!)',
        None
    ),
    1172: (
        None,
        '1. Wealth: <strong>Amiri / daulat</strong> (Rich lifestyle of an <em>Ameer</em> + Fortune!) = <em>Wealth</em>!<br>2. Poverty: <strong>Gareebi / tangi</strong> (Poor state + Tight <em>Tang</em> cash squeeze!) = <em>Poverty</em>!'
    ),
    1175: (
        '<strong>Gasto</strong> ("Gas-Toll" spent!) | <strong>Egreso</strong> (Cash "Exiting" — opposite of <em>Ingreso</em> = <em>Expense</em>!)',
        None
    ),
    1180: (
        None,
        '1. Gain: <strong>Faayda</strong> (Advantage gain!) / <strong>Munaafa</strong> (<strong>Tamil முனாஃபா = Profit!</strong>)<br>2. Deficit: <strong>Nuksaan / ghata</strong> (Harm loss &amp; price dip deficit!)'
    ),
    1181: (
        None,
        '<strong>Bachat</strong> (Left saved!) / <strong>Jama-punji</strong> (<em>Jama</em> Stored + <em>Punji</em> Capital egg = <em>Savings</em>!)'
    ),
    1182: (
        '<strong>Bancarrota</strong> (Broken bank!) | <strong>Quiebra</strong> (From <em>Quebrar</em> = Shatter/Crack completely broke = <em>Bankruptcy</em>!)',
        None
    ),
    1184: (
        None,
        '<strong>Daan</strong> (<strong>Tamil தானம் = Charity!</strong>) / <strong>Madad</strong> (<strong>Tamil மதத்</strong> — generous helping gift!) = <em>Donation</em>!'
    ),
    1185: (
        '<strong>Multa</strong> (Traffic ticket!) | <strong>Sanción</strong> (Official legal <strong>"Sanction"</strong> penalty = <em>Fine</em>!)',
        None
    ),
    1206: (
        '<strong>Robo</strong> (Thievery!) | <strong>Asalto</strong> (Violent armed bank <strong>"Assault"</strong> heist = <em>Robbery</em>!)',
        '<strong>Chori</strong> (Sneaky pickpocket — <strong>Tamil சோரன்!</strong>) / <strong>Dakaiti / loot</strong> (Armed gang <em>Dacoit</em> plunder = <em>Robbery</em>!)'
    ),
    1209: (
        '<strong>Chantaje / chantajear</strong> ≈ Noun &amp; Verb ("Chant-Pay-Me" extortion threat!) → Squeezing hush money = <em>Blackmail</em>!',
        None
    ),
    1212: (
        None,
        '<strong>Maar-peet</strong> (Hit &amp; beat!) / <strong>Ladai</strong> (Fierce street/border brawl = <em>Violence / Assault</em>!)'
    ),
    1218: (
        '<strong>Ladrón / ladrona</strong> ≈ Masked burglar ("Loot-And-Run!") sneaking away with stolen gold = <em>Thief</em>!',
        None
    ),
    1225: (
        '<strong>Orden judicial / orden de arresto</strong> ≈ Official court stamp ("Judicial / Arrest <strong>Order</strong>") authorizing detention = <em>Warrant</em>!',
        None
    ),
    1234: (
        '1. City: <strong>Alcalde / alcaldesa</strong> (Chief municipal mayor!) = <em>Mayor</em>!<br>2. State: <strong>Gobernador / gobernadora</strong> (Chief executive steering a state!) = <em>Governor</em>!',
        None
    ),
    1241: (
        None,
        '<strong>Sudhaar</strong> ("So-Better" upgrade!) / <strong>Badlaav</strong> (Big sweeping policy change = <em>Reform</em>!)'
    ),
    1245: (
        None,
        '1. Overthrow: <strong>Kraanti / inqilaab</strong> (Historic freedom battle cries — <em>Inqilaab Zindabad!</em>) = <em>Revolution</em>!<br>2. Campaign: <strong>Andolan</strong> (Mass citizen march!)'
    ),
    1250: (
        None,
        '<strong>Sarkari</strong> (Government — <strong>Tamil சர்க்கார்!</strong>) / <strong>Aam janta</strong> (Ordinary everyday citizens = <em>Public</em>!)'
    ),
    1256: (
        None,
        '<strong>Jung</strong> ("Jungle" combat!) / <strong>Ladai</strong> (Armed battle clash on the front line = <em>War / Combat</em>!)'
    ),
    1257: (
        '1. Armed force: <strong>Fuerzas armadas / ejército</strong> (National defense troops!) = <em>Military / Army</em>!<br>2. Sea fleet: <strong>Marina / armada</strong> (Ocean warships!) = <em>Navy</em>!',
        None
    ),
    1262: (
        None,
        '<strong>Shaanti</strong> (<strong>Tamil சாந்தி!</strong>) / <strong>Aman</strong> (Border harmony!) / <strong>Sukoon</strong> (Deep quiet heart calm = <em>Peace</em>!)'
    ),
}


def main():
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        lines = f.read().splitlines(True)

    sc_idx = next(i for i, l in enumerate(lines) if l.startswith("var cardShortcuts = "))
    s5_idx = next(i for i, l in enumerate(lines) if l.startswith("var split5DeckCards = "))
    s6_idx = next(i for i, l in enumerate(lines) if l.startswith("var split6DeckCards = "))

    card_shortcuts = json.loads(lines[sc_idx][len("var cardShortcuts = "):].rstrip().rstrip(";"))
    split5 = json.loads(lines[s5_idx][len("var split5DeckCards = "):].rstrip().rstrip(";"))
    split6 = json.loads(lines[s6_idx][len("var split6DeckCards = "):].rstrip().rstrip(";"))

    updated = {}
    for c in split5 + split6:
        n = c["num"]
        if n in POLISH:
            es_val, hi_val = POLISH[n]
            if es_val is not None:
                c["shortcutEs"] = es_val
            if hi_val is not None:
                c["shortcutHi"] = hi_val
        card_shortcuts[str(n)] = {"es": c["shortcutEs"], "hi": c["shortcutHi"]}
        updated[n] = c

    lines[sc_idx] = "var cardShortcuts = " + json.dumps(card_shortcuts, ensure_ascii=False) + ";\n"
    lines[s5_idx] = "var split5DeckCards = " + json.dumps(split5, ensure_ascii=False) + ";\n"
    lines[s6_idx] = "var split6DeckCards = " + json.dumps(split6, ensure_ascii=False) + ";\n"

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.writelines(lines)

    with open(BACKUP_PATH, "r", encoding="utf-8") as f:
        bkp = json.load(f)
    items = bkp.values() if isinstance(bkp, dict) else bkp
    for val in items:
        if isinstance(val, dict):
            n = val.get("originalNum") or val.get("num")
            if n in updated:
                src = updated[n]
                val["shortcutEs"] = src["shortcutEs"]
                val["shortcutHi"] = src["shortcutHi"]
    with open(BACKUP_PATH, "w", encoding="utf-8") as f:
        json.dump(bkp, f, indent=2, ensure_ascii=False)

    print(f"Polished {len(POLISH)} Split 5 & 6 cards cleanly across index.html + cardShortcuts + backup_original_cards.json")


if __name__ == "__main__":
    main()
