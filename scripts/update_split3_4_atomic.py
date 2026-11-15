#!/usr/bin/env python3
"""
Atomic quality upgrade for Split 3 & 4 (#440-#821, 382 cards in var split2DeckCards):
  1. Fixes all 65 multi-sense Tamil strings to exact 1-to-1 numbered "1. ... / 2. ..." alignment + fixes #445 Devanagari, #474/#570 markers, #621 Sweat copy-paste, #717 Gate/Fence swap, #730 Shelf/Cabinet, #755 Dress/Skirt, #756 Suit, #773 Purse/Wallet.
  2. Eliminates all template slop ("Direct sibling", "Direct match", "Direct English", "Everyday spoken loanword", etc.), circular tautologies, wrong homonyms (#760, #763), and missing synonyms in shortcutEs & shortcutHi across all 382 cards.
  3. Upgrades 29 off-topic/NSFW/unclear images (#578 NSFW penis -> headshot, #763/#768 swapped boots/gloves, etc.) with Wikimedia Commons imageinfo-verified URLs.
  4. Syncs split2DeckCards, cardShortcuts, and data/backup_original_cards.json 100%.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(ROOT, "index.html")
BACKUP_PATH = os.path.join(ROOT, "data", "backup_original_cards.json")

TAMIL_UPDATES = {
    442: "1. சிறந்த / அருமையான (Excellent) / 2. மாபெரும் / பெரிய (Prominent)",
    445: "பெரிய (பிரம்மாண்டமான)",
    449: "1. குள்ளமான (Height) / 2. குறுகிய / சுருக்கமான (Length/Duration)",
    458: "1. ஒல்லியான / மெலிந்த (Person) / 2. மெல்லிய / நுண்ணிய (Object/Fine)",
    463: "1. திடமான / கடினமான (Solid) / 2. கஷ்டமான / சிக்கலான (Difficult)",
    467: "1. சூடான (Temperature) / 2. காரமான (Spicy)",
    468: "1. குளிர்ந்த (Temperature) / 2. சளி ஜலதோஷம் (Sickness)",
    470: "1. குளிர்ச்சியான / இதமான (Slightly Cold) / 2. அருமையான / அசத்தலான (Awesome)",
    474: "சுத்தமான",
    475: "1. நேர்த்தியான / ஒழுங்கான (Tidy) / 2. கலைந்த / ஒழுங்கற்ற (Messy)",
    477: "1. பழைய / புராதன (Objects) / 2. வயதான / முதிய (People)",
    486: "1. தெளிவான / புரியக்கூடிய (Understandable) / 2. தெளிந்த / மேகமற்ற (Transparent/Sunny)",
    491: "1. இனிப்பான (Taste) / 2. இனிமையான / அன்பான (Kind)",
    519: "1. வேடிக்கையான / நகைச்சுவையான (Humorous) / 2. விசித்திரமான (Strange)",
    540: "1. சதுரம் (Shape) / 2. நகர சதுக்கம் (Town Plaza)",
    542: "1. கோடு (Drawn Stripe) / 2. வரிசை (Queue)",
    543: "1. புள்ளி / மதிப்பெண் (Dot/Score) / 2. சுட்டிக்காட்டு (Gesture)",
    544: "1. நபர் / மனிதர் (Singular) / 2. மக்கள் (Plural)",
    570: "நண்பன் / தோழன்",
    575: "1. அரசன் / ராஜா (King) / 2. அரசி / ராணி (Queen)",
    578: "1. தலை (Anatomy) / 2. தலைவர் / மேலாளர் (Chief/Leader)",
    589: "1. நாக்கு (Anatomy) / 2. மொழி (Language)",
    594: "1. மார்பு (Anatomy) / 2. மரப்பெட்டி (Box/Trunk)",
    604: "1. நகம் (Fingernail) / 2. ஆணி (Metal Hardware)",
    609: "1. பாதம் (Anatomy) / 2. அடி (Measurement)",
    616: "1. இதயம் (Organ) / 2. மையம் / நடுப்பகுதி (Core/Center)",
    620: "1. கண்ணீர் (From Eye) / 2. கிழி (Rip/Shred)",
    621: "1. வியர்வை (Noun) / 2. வியர்த்தல் (Verb)",
    627: "1. இருமல் (Noun) / 2. இருமுதல் (Verb)",
    630: "1. காயம் / புண் (Noun) / 2. காயப்படுத்து (Verb)",
    636: "1. நோயாளி (Medical Person) / 2. பொறுமையான (Calm/Enduring)",
    652: "1. கோதுமை (Grain) / 2. மாவு (Ground Powder)",
    655: "1. கோழி இறைச்சி (Meat) / 2. கோழி (Bird)",
    656: "1. மீன் உணவு (Food) / 2. மீன் (Live Animal)",
    660: "1. சமையல் எண்ணெய் (Cooking) / 2. கச்சா எண்ணெய் (Petroleum)",
    663: "1. மிளகு (Black Spice) / 2. குடைமிளகாய் (Bell Pepper)",
    671: "1. ஆரஞ்சு பழம் (Fruit) / 2. ஆரஞ்சு நிறம் (Color)",
    684: "1. பீன்ஸ் / பயறு (Beans) / 2. பட்டாணி (Peas)",
    687: "1. பசலைக் கீரை (Spinach) / 2. முட்டைக்கோஸ் (Cabbage)",
    688: "1. கொட்டை / பருப்பு (Food) / 2. திருகுநட் (Hardware)",
    692: "1. டம்ளர் / குவளை (Drinking Tumbler) / 2. கண்ணாடி (Material)",
    701: "1. அடுப்பு (Cooktop/Burner) / 2. அடுமனை / அவன் (Baking Chamber)",
    702: "1. கழுவும் தொட்டி (Basin) / 2. தண்ணீர் குழாய் (Faucet)",
    709: "1. கூரை (Exterior Top) / 2. உட்கூரை (Interior Ceiling)",
    711: "1. தரை (Ground Surface) / 2. தளம் / மாடி (Building Storey)",
    717: "1. வேலி / சுற்றுச்சுவர் (Barrier Fence) / 2. வாயில் / கேட் (Access Gate)",
    725: "1. படுக்கை விரிப்பு (Bed Cover) / 2. காகிதத் தாள் (Paper Piece)",
    730: "1. அடுக்கு பலகை / ஷெல்ஃப் (Ledge) / 2. அலமாரி (Storage Box)",
    732: "1. விளக்கு (Fixture) / 2. மின் குமிழ் (Glass Bulb)",
    733: "1. மின் விசை / சுவிட்ச் (Electrical Device) / 2. மாற்று (Change/Swap)",
    734: "1. மின் செருகி / பிளக் (Male Prong) / 2. செருகுதுளை / சாக்கெட் (Wall Outlet)",
    738: "1. சாவி (Door Lock Tool) / 2. முக்கியமான (Crucial Factor)",
    740: "1. விளக்குமாறு / துடைப்பம் (Sweeping Brush) / 2. மாப் / தரை துடைப்பான் (Wet Wipe Tool)",
    742: "1. குப்பை (Waste Matter) / 2. குப்பைத் தொட்டி (Receptacle)",
    745: "1. பல் துலக்கி (Brush) / 2. பல் பசை (Paste)",
    748: "1. திருகாணி (Threaded Spike) / 2. திருப்புளி (Driver Tool)",
    755: "1. முழு ஆடை / கவுன் (One-Piece Garment) / 2. பாவாடை (Lower Garment)",
    756: "1. கோட்டு சூட் (Formal Outfit) / 2. பொருந்துதல் (Fit/Match)",
    770: "1. சட்டைப் பொத்தான் (Clothing Fastener) / 2. அழுத்து பொத்தான் (Push Device)",
    773: "1. பணப்பை / வாலட் (Wallet) / 2. கைப்பை (Handbag)",
    778: "1. மோதிரம் (Finger Jewelry) / 2. மணி அடி (Sound Chime/Call)",
    779: "1. கழுத்து மாலை / சங்கிலி (Neck Chain) / 2. நகைகள் (General Ornaments)",
    785: "1. தொடருந்து / ரயில் (Rail Vehicle) / 2. பயிற்சி அளி (Coach/Practice)",
    792: "1. டயர் / சக்கர உறை (Rubber Wheel Cover) / 2. சோர்வடைதல் (Fatigue)",
    800: "1. ஒற்றையடிப் பாதை (Footpath) / 2. நடைபாதை (Paved Walkway)",
    809: "1. பெருநகரம் (Large Metropolis) / 2. நகரம் / பேரூராட்சி (Smaller Town)",
    811: "1. நாடு (Nation) / 2. கிராமப்புறம் (Rural Countryside)",
    821: "1. வங்கி (Financial Institution) / 2. ஆற்றங்கரை (River Edge)",
}

IMAGE_UPGRADES = {
    441: "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Rotten_apple_under_the_tree.jpg/960px-Rotten_apple_under_the_tree.jpg",
    443: "https://upload.wikimedia.org/wikipedia/commons/4/48/Hong_Kong_Gold_Cup_%28trophy%29_20260301.jpg",
    457: "https://upload.wikimedia.org/wikipedia/commons/7/7e/Stack_volumes_wrong.jpg",
    462: "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Wilted_flowers_on_Friedhof_Obermenzing_01.jpg/960px-Wilted_flowers_on_Friedhof_Obermenzing_01.jpg",
    480: "https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/A_Glass_Full_of_Water.jpg/960px-A_Glass_Full_of_Water.jpg",
    492: "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Lime_-_whole_and_halved.jpg/960px-Lime_-_whole_and_halved.jpg",
    516: "https://upload.wikimedia.org/wikipedia/commons/thumb/d/db/Random_acts_of_kindness_%284986298%29.jpg/960px-Random_acts_of_kindness_%284986298%29.jpg",
    517: "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Business_agreement_handshake_at_coffee_shop.jpg/960px-Business_agreement_handshake_at_coffee_shop.jpg",
    530: "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Black-Cat-Sitia-Crete-Greece.jpg/960px-Black-Cat-Sitia-Crete-Greece.jpg",
    564: "https://upload.wikimedia.org/wikipedia/commons/7/7c/Ezra_Meeker_and_child%2C_Olympia%2C_1914_%28PORTRAITS_227%29.jpg",
    576: "https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Captainarmbandfifa.jpg/960px-Captainarmbandfifa.jpg",
    578: "https://upload.wikimedia.org/wikipedia/commons/thumb/0/01/Pranab_Mukherjee_Portrait_%28headshot%29.jpg/960px-Pranab_Mukherjee_Portrait_%28headshot%29.jpg",
    591: "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/Lateral_head_anatomy_detail.jpg/960px-Lateral_head_anatomy_detail.jpg",
    592: "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/US_Navy_040113-N-4614W-005_Capt._Wan_Mun_Chin_examines_a_patient_suffering_from_a_sore_throat_and_high_fever.jpg/960px-US_Navy_040113-N-4614W-005_Capt._Wan_Mun_Chin_examines_a_patient_suffering_from_a_sore_throat_and_high_fever.jpg",
    596: "https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/FLUX_-_A_Indian_tailor_measuring_his_customer_waist_sizes_using_yellow_tailor%27s_tape.png/960px-FLUX_-_A_Indian_tailor_measuring_his_customer_waist_sizes_using_yellow_tailor%27s_tape.png",
    620: "https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/Crying_baby_%282%29.jpg/960px-Crying_baby_%282%29.jpg",
    627: "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Man_Coughing_%28NIH_BioArt_332%29.png/960px-Man_Coughing_%28NIH_BioArt_332%29.png",
    629: "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Migraine.jpg/960px-Migraine.jpg",
    644: "https://upload.wikimedia.org/wikipedia/commons/0/02/Water_pouring_from_a_faucet_into_a_clear_glass_cup._%2815054813052%29.jpg",
    724: "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Blanket_%28AM_2007.16.1-2%29.jpg/960px-Blanket_%28AM_2007.16.1-2%29.jpg",
    728: "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/EFTA00000140_-_Elegant_bathroom_features_ornate_wooden_mirror_marble_countertop_vintage_wall_sconces_and_decorative_bronze_figurine.jpg/960px-EFTA00000140_-_Elegant_bathroom_features_ornate_wooden_mirror_marble_countertop_vintage_wall_sconces_and_decorative_bronze_figurine.jpg",
    730: "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/Armoire_avec_linge_de_maison2.jpg/960px-Armoire_avec_linge_de_maison2.jpg",
    737: "https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Bell_%28AM_2004.105.13-1%29.jpg/960px-Bell_%28AM_2004.105.13-1%29.jpg",
    741: "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Buckets_Made_of_Leather%3F_%28d8bd5c34-1dd8-b71b-0b0e-90d26e10a4a4%29.JPG/960px-Buckets_Made_of_Leather%3F_%28d8bd5c34-1dd8-b71b-0b0e-90d26e10a4a4%29.JPG",
    763: "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Boots_of_a_man.jpg/960px-Boots_of_a_man.jpg",
    768: "https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Leather_gloves_out_hiking_P1000952.jpg/960px-Leather_gloves_out_hiking_P1000952.jpg",
    773: "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/WalletMpegMan.jpg/960px-WalletMpegMan.jpg",
    776: "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fd/Colorful_Rainy_Day_%28238641099%29.jpeg/960px-Colorful_Rainy_Day_%28238641099%29.jpeg",
    813: "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/New_York_City_%28New_York%2C_USA%29%2C_Empire_State_Building_--_2012_--_6440.jpg/960px-New_York_City_%28New_York%2C_USA%29%2C_Empire_State_Building_--_2012_--_6440.jpg",
}

SHORTCUT_UPDATES = {
    440: (
        '<strong>Bueno / buena / buen</strong> ≈ Root of English <strong>"Bonus / Bonanza / Bon Appétit"</strong> → Always positive and <em>Good</em>!',
        '<strong>Achha / achhi / achhe</strong> ≈ Famous Indian exclamation <strong>"Achha!"</strong> (Good / Okay!) → Same word flips <em>-a / -i / -e</em> for gender!'
    ),
    441: (
        '<strong>Malo / mala / mal</strong> ≈ Prefix in English <strong>"Malfunction / Malpractice / Malice"</strong> → Something gone wrong or <em>Bad</em>!',
        '<strong>Bura / buri / bure</strong> ≈ Sounds like <strong>"Boo-Rah!"</strong> when booing a <em>Bad / Nasty</em> movie villain!'
    ),
    442: (
        '1. Excellent: <strong>Genial</strong> ≈ Sounds like <strong>"Genius!"</strong> + <strong>Estupendo</strong> ≈ English <strong>"Stupendous!"</strong> = Awesome / <em>Great</em>!<br>2. Prominent/large: <strong>Gran / grande</strong> ≈ Coffee size <strong>"Grande"</strong> & <strong>"Grand"</strong> (<em>Prominent / Large</em>)!',
        '1. Excellent: <strong>Bohot badhiya</strong> ≈ <strong>Bohot</strong> (Very) + <strong>Badhiya</strong> (Super!) | <strong>Zabardast</strong> ≈ Powerful hit / Awesome = <em>Great</em>!<br>2. Prominent/large: <strong>Mahan</strong> ≈ <strong>Tamil மகான் (Mahaan = Great sage!)</strong> | <strong>Bada</strong> ≈ Big & <em>Prominent</em>!'
    ),
    443: (
        '<strong>El mejor / la mejor</strong> ≈ Root of English <strong>"Ameliorate"</strong> (improve to the <em>Best</em>!) & <strong>"Major"</strong> = Topmost!',
        '<strong>Sabse achha / sabse badhiya</strong> ≈ <strong>Sabse</strong> (Compared to all) + <strong>Achha / Badhiya</strong> (Good/Fine) = Literally <em>Best of all</em>!'
    ),
    444: (
        '<strong>El peor / la peor</strong> ≈ Root of English <strong>"Pejorative / Pessimist"</strong> → Seeing the darkest side = <em>The Worst</em>!',
        '<strong>Sabse bura / sabse bekar</strong> ≈ <strong>Sabse</strong> (Of all) + <strong>Bura</strong> (Bad) / <strong>Bekar</strong> (<strong>Spoken Tamil பேக்கார் = Useless!</strong>) = <em>Worst</em>!'
    ),
    445: (
        '<strong>Grande / grandes</strong> ≈ Giant coffee cup <strong>"Grande"</strong> & English <strong>"Grand Canyon"</strong> = <em>Big / Large</em>!',
        '<strong>Bada / badi / bade</strong> ≈ Sounds like <strong>"Big-Daddy" (Ba-da)</strong> → Big elephant or older sibling = <em>Big / Large</em>!'
    ),
    446: (
        '<strong>Pequeño / pequeña</strong> ≈ Tiny bird <strong>"Peck-a-bit"</strong> | <strong>Diminuto</strong> ≈ English <strong>"Diminutive"</strong> (shrunk tiny) = <em>Small / Tiny</em>!',
        '<strong>Chhota / chhoti / chhote</strong> ≈ Think <strong>"Short-a"</strong> → Cut short and tiny in size = <em>Small / Little</em>!'
    ),
    447: (
        '<strong>Enorme</strong> ≈ Twin of English <strong>"Enormous"</strong> (mountain-sized!) | <strong>Gigante</strong> ≈ Twin of <strong>"Gigantic / Giant"</strong> = <em>Huge</em>!',
        '<strong>Bohot bada</strong> ≈ <strong>Bohot</strong> ("A boatload / very") + <strong>Bada</strong> (Big) → Giant-sized = <em>Huge</em>!'
    ),
    448: (
        '<strong>Alto / alta</strong> ≈ Root of English <strong>"Altitude / Alto"</strong> (high mountain or high voice) → Stretching upward = <em>Tall</em>!',
        '<strong>Lamba / lambi (unchai mein)</strong> ≈ Stretching out <strong>"Long"</strong> vertically (<strong>Unchai mein</strong> = in height) = <em>Tall</em>!'
    ),
    449: (
        '1. Height: <strong>Bajo / baja</strong> ≈ Root of <strong>"Bass / Basement"</strong> (low down) = <em>Short in height</em>!<br>2. Length/duration: <strong>Corto / corta</strong> ≈ Root of <strong>"Curt / Curtail"</strong> (cut brief) = <em>Short in length/time</em>!',
        '1. Height: <strong>Chhota</strong> (Small) / <strong>Kam lambai ka</strong> (<strong>Tamil கம்மி = Less</strong> height) = <em>Short</em>!<br>2. Length/duration: <strong>Chhota / chhoti</strong> / <strong>Kam samay</strong> (<strong>Tamil சமயம் = Time</strong> → Less time) = <em>Short</em>!'
    ),
    450: (
        '<strong>Largo / larga</strong> ≈ False-friend alert: sounds like <em>Large</em>, actually means <strong>"Lengthy"</strong> (a long road or long speech) = <em>Long</em>!',
        '<strong>Lamba / lambi</strong> ≈ Think of stretching a rubber band <strong>"Long-ba!"</strong> from end to end = <em>Long</em>!'
    ),
    451: (
        '<strong>Ancho / ancha</strong> ≈ Broad across (think <em>Wide Open Ranch</em>) | <strong>Amplio</strong> ≈ English <strong>"Ample"</strong> room to spread = <em>Wide</em>!',
        '<strong>Chauda / chaudi</strong> ≈ Sounds like a <strong>"Broad-Wide-Road (Chaud-road)"</strong> with plenty of lanes = <em>Wide</em>!'
    ),
    452: (
        '<strong>Estrecho / estrecha</strong> ≈ English <strong>"Strait"</strong> (narrow sea channel) | <strong>Angosto</strong> ≈ Squeezing in agony = <em>Narrow</em>!',
        '<strong>Patla</strong> ≈ Thin/slim lane | <strong>Tang</strong> ≈ Tight squeeze (think <strong>"Tangled tight"</strong> alley) = <em>Narrow</em>!'
    ),
    453: (
        '<strong>Alto / alta</strong> ≈ Root of <strong>"Altitude"</strong> | <strong>Elevado</strong> ≈ English <strong>"Elevated"</strong> high above ground = <em>High</em>!',
        '<strong>Uncha / unchi</strong> ≈ Sounds like soaring <strong>"Up-High on a Crane" (Unch-a)</strong> → Opposite of <em>Neecha</em> (low) = <em>High</em>!'
    ),
    454: (
        '<strong>Bajo / baja</strong> ≈ Root of <strong>"Base / Basement"</strong> (down at the bottom floor) = <em>Low</em>!',
        '<strong>Neecha / neechi</strong> ≈ Near the ground (below your <strong>"Knees"</strong>) | <strong>Kam</strong> ≈ <strong>Spoken Tamil கம்மி (Kammi = Less/Low!)</strong>!'
    ),
    455: (
        '<strong>Profundo / profunda</strong> ≈ Twin of <strong>"Profound"</strong> (deep thought/ocean) | <strong>Hondo</strong> ≈ Plunging down into a deep hollow = <em>Deep</em>!',
        '<strong>Gehra / gehri</strong> ≈ Sounds like sinking into a <strong>"Great-Hollow" (Geh-ra)</strong> pit or deep ocean = <em>Deep</em>!'
    ),
    456: (
        '<strong>Poco profundo</strong> ≈ Literally <strong>"Little deep"</strong> | <strong>Superficial</strong> ≈ Twin of English <strong>"Superficial"</strong> (just on the surface) = <em>Shallow</em>!',
        '<strong>Kam gehra</strong> ≈ <strong>Kam</strong> (<strong>Spoken Tamil கம்மி = Less</strong>) + <strong>Gehra</strong> (Deep) = <em>Shallow</em>!'
    ),
    457: (
        '<strong>Grueso / gruesa</strong> ≈ Twin of English <strong>"Gross"</strong> bulk | <strong>Gordo</strong> ≈ Plump/stout like a thick log = <em>Thick</em>!',
        '<strong>Mota / moti</strong> ≈ Heavy & chunky (think <strong>"Motor-tire thick"</strong>) | <strong>Gaadha</strong> ≈ Rich & dense (like thick gravy) = <em>Thick</em>!'
    ),
    458: (
        '1. Person/slender: <strong>Flaco</strong> ≈ <strong>"Flat & Slim"</strong> | <strong>Delgado</strong> ≈ Slender & <strong>"Delicate"</strong> = <em>Thin</em>!<br>2. Object/fine: <strong>Fino</strong> ≈ Twin of <strong>"Fine"</strong> thread | <strong>Delgado</strong> ≈ Wafer-slim = <em>Thin</em>!',
        '1. Person/slender: <strong>Patla / patli</strong> ≈ Slim as a thin petal leaf = <em>Thin</em>!<br>2. Object/fine: <strong>Bareek</strong> ≈ <strong>"Barley-grain"</strong> fine/tiny | <strong>Patla</strong> ≈ Paper-thin = <em>Thin</em>!'
    ),
    460: (
        '<strong>Ligero / ligera</strong> ≈ Root of <strong>"Light / Featherlight"</strong> | <strong>Liviano</strong> ≈ Floating like a feather in the air = <em>Light (weight)</em>!',
        '<strong>Halka / halki</strong> ≈ Whisper-soft breeze (<strong>"Hal-ka"</strong> = gentle tap, barely any weight) = <em>Light</em>!'
    ),
    462: (
        '<strong>Débil</strong> ≈ Root of English <strong>"Debilitate"</strong> (drain strength) | <strong>Flojo</strong> ≈ Loose, limp & floppy = <em>Weak</em>!',
        '<strong>Kamzor</strong> ≈ <strong>Kam</strong> (<strong>Tamil கம்மி = Less</strong>) + <strong>Zor</strong> (Force/Power) → Running low on strength = <em>Weak</em>!'
    ),
    463: (
        '1. Solid/firm: <strong>Duro</strong> ≈ Root of <strong>"Durable"</strong> (rock-solid) | <strong>Firme</strong> ≈ Twin of <strong>"Firm"</strong> = <em>Hard</em>!<br>2. Difficult: <strong>Difícil</strong> ≈ <strong>"Difficult"</strong> | <strong>Complicado</strong> ≈ <strong>"Complicated"</strong> = <em>Hard</em>!',
        '1. Solid/firm: <strong>Sakht</strong> ≈ Unyielding as stone (sounds like <em>Shock-hard</em>) | <strong>Kadak</strong> ≈ Crisp/stiff (like <em>Kadak chai</em>!) = <em>Hard</em>!<br>2. Difficult: <strong>Mushkil</strong> ≈ Tangled puzzle (like Tamil <strong>கடினம்</strong>) = <em>Hard / Difficult</em>!'
    ),
    465: (
        '<strong>Rápido / rápida</strong> ≈ Twin of <strong>"Rapid"</strong> | <strong>Veloz</strong> ≈ Root of <strong>"Velocity"</strong> (high speed) = <em>Fast / Quick</em>!',
        '<strong>Tez</strong> ≈ Arrow-sharp speed | <strong>Jaldi</strong> ≈ <strong>Spoken Tamil ஜல்தி (Jaldi = Quickly!)</strong> = <em>Fast / Quick</em>!'
    ),
    466: (
        '<strong>Lento / lenta</strong> ≈ Musical tempo <strong>"Lento"</strong> (slowly) | <strong>Despacio</strong> ≈ Take it easy, step by step (<em>Slowly</em>)!',
        '<strong>Dheema / dheemi</strong> ≈ Gentle & unhurried (think <strong>"Dim-down the speed"</strong>) = <em>Slow</em>!'
    ),
    467: (
        '1. Temperature: <strong>Caliente</strong> ≈ Root of <strong>"Calorie / Cauldron"</strong> (boiling heat) = <em>Hot</em>!<br>2. Spicy: <strong>Picante</strong> ≈ Twin of <strong>"Piquant"</strong> (poking your tongue with spice) = <em>Spicy Hot</em>!',
        '1. Temperature: <strong>Garam</strong> ≈ Pipping-hot warmth (as in <strong>Garam Masala / Garam Chai</strong>) = <em>Hot</em>!<br>2. Spicy: <strong>Teekha / teekhi</strong> ≈ Sharp tongue-tingling chili heat = <em>Spicy</em>!'
    ),
    468: (
        '1. Temperature: <strong>Frío / fría</strong> ≈ Root of <strong>"Frigid / Refrigerator"</strong> (icy chill) = <em>Cold</em>!<br>2. Sickness: <strong>Resfriado</strong> ≈ Re-chilled weather | <strong>Catarro</strong> ≈ Phlegm/<strong>"Catarrh"</strong> chest chill = <em>Head Cold</em>!',
        '1. Temperature: <strong>Thanda / thandi</strong> ≈ <strong>Tamil தண்மை (Thanmai = Cool/Cold!)</strong> → Ice-chilled = <em>Cold</em>!<br>2. Sickness: <strong>Sardi</strong> (Winter chill) + <strong>Zukaam</strong> (Runny nose sniffling) = <em>Catching a Cold</em>!'
    ),
    469: (
        '<strong>Tibio / tibia</strong> ≈ Twin of <strong>"Tepid"</strong> (lukewarm) | <strong>Cálido</strong> ≈ Cozy sun-warmed glow (like <em>Calorie</em>) = <em>Warm</em>!',
        '<strong>Gunguna</strong> ≈ Comforting lukewarm sip (not boiling!) | <strong>Halka garam</strong> ≈ Lightly <em>Warm</em>!'
    ),
    470: (
        '1. Slightly cold: <strong>Fresco / fresca</strong> ≈ Crisp morning breeze (<strong>"Fresh"</strong> chill) = <em>Cool</em>!<br>2. Awesome: <strong>Genial</strong> (Brilliant) | <strong>Guay</strong> ≈ Trendy Spanish slang ("Whoa-Way cool!") = <em>Awesome</em>!',
        '1. Slightly cold: <strong>Thanda / halka thanda</strong> ≈ Lightly chilled (<strong>Tamil தண்மை = Cool!</strong>) = <em>Cool</em>!<br>2. Awesome: <strong>Badhiya</strong> (Super!) | <strong>Mast</strong> ≈ <strong>Spoken Tamil மஸ்த் (Masth = Amazing!)</strong> = <em>Cool / Awesome</em>!'
    ),
    471: (
        '<strong>Mojado / mojada</strong> ≈ Splashed by a spilled <strong>"Mojito"</strong> | <strong>Húmedo</strong> ≈ Twin of <strong>"Humid"</strong> damp air = <em>Wet</em>!',
        '<strong>Geela / geeli</strong> ≈ Soaked in water (think <strong>"Glistening puddles"</strong> after rain) = <em>Wet</em>!'
    ),
    472: (
        '<strong>Seco / seca</strong> ≈ Root of <strong>"Desiccated / Sec"</strong> (zero moisture left) = <em>Dry</em>!',
        '<strong>Sookha / sookhi</strong> ≈ Same root as <strong>Tamil சுக்கு (Sukku = Dried ginger!)</strong> → Parched and baked dry = <em>Dry</em>!'
    ),
    473: (
        '<strong>Sucio / sucia</strong> ≈ Covered in chimney <strong>"Soot"</strong> and mud smudges = <em>Dirty</em>!',
        '<strong>Ganda / gandi</strong> ≈ Muddy mess | <strong>Maila</strong> ≈ <strong>Tamil மாசு / அழுக்கு</strong> (think <em>Muddy-stained</em> cloth) = <em>Dirty</em>!'
    ),
    474: (
        '<strong>Limpio / limpia</strong> ≈ Sparkling <strong>"Gleam-Pure"</strong> after washing = <em>Clean</em>!',
        '<strong>Saaf</strong> ≈ Identical to <strong>Spoken Tamil சாஃப் (Saaf = Spotless & Clean!)</strong>!'
    ),
    475: (
        '1. Tidy/neat: <strong>Ordenado / ordenada</strong> ≈ Everything put in neat <strong>"Order"</strong> = <em>Tidy / Neat</em>!<br>2. Disordered/messy: <strong>Desordenado / desordenada</strong> ≈ Prefix <strong>Des-</strong> (Out of) + Order = <em>Messy</em>!',
        '1. Tidy/neat: <strong>Saaf-suthra</strong> ≈ <strong>Saaf</strong> (Clean) + <strong>Suthra</strong> (Neat/<strong>Tamil சுத்தம்</strong>) = <em>Neat</em>!<br>2. Disordered/messy: <strong>Bikhra hua</strong> (Scattered everywhere) / <strong>Ganda</strong> (Filthy mess) = <em>Messy</em>!'
    ),
    476: (
        '<strong>Nuevo / nueva</strong> ≈ Root of English <strong>"Novelty / Nova / Novice"</strong> (brand fresh start) = <em>New</em>!',
        '<strong>Naya / nayi / naye</strong> ≈ Same Sanskrit root as <strong>Tamil நவ (Nava = New!)</strong> → Brand <em>New</em>!'
    ),
    477: (
        '1. Objects: <strong>Viejo</strong> (Worn vintage) | <strong>Antiguo</strong> ≈ Twin of <strong>"Antique"</strong> = <em>Old</em>!<br>2. People: <strong>Viejo</strong> | <strong>Anciano</strong> (<strong>"Ancient"</strong> elder) | <strong>Mayor</strong> (<strong>"Major"</strong> senior in age) = <em>Old</em>!',
        '1. Objects: <strong>Purana / purani</strong> ≈ Identical to <strong>Tamil புராணம் (Puraanam = Ancient!)</strong> = <em>Old</em>!<br>2. People: <strong>Boodha</strong> (White-haired elder) | <strong>Buzurg</strong> (Respected senior) = <em>Old</em>!'
    ),
    478: (
        '<strong>Joven</strong> ≈ Root of English <strong>"Juvenile / Rejuvenate"</strong> → Bursting with youth = <em>Young</em>!',
        '<strong>Jawan</strong> (Full of youth/vitality) | <strong>Chhota</strong> (Little/junior in age) = <em>Young</em>!'
    ),
    479: (
        '<strong>Fresco / fresca</strong> ≈ Straight off the farm vine (<strong>"Fresh"</strong> produce) = <em>Fresh</em>!',
        '<strong>Taaza / taazi</strong> ≈ Identical to <strong>Spoken Tamil தாஜா (Taaza = Garden-fresh!)</strong>!'
    ),
    480: (
        '<strong>Lleno / llena</strong> ≈ Think <strong>"Yeah-No more can fit!"</strong> → Filled right up to the brim = <em>Full</em>!',
        '<strong>Bhara hua / bhari hui</strong> ≈ Same root as <strong>Tamil பூரணம் (Pooranam/Bharam = Filled completely!)</strong> = <em>Full</em>!'
    ),
    481: (
        '<strong>Vacío / vacía</strong> ≈ Root of English <strong>"Vacant / Vacuum"</strong> (hollow inside) = <em>Empty</em>!',
        '<strong>Khaali</strong> ≈ Identical to <strong>Spoken Tamil காலி (Kaali = Empty / Vacant!)</strong>!'
    ),
    482: (
        '<strong>Cerrado / cerrada</strong> ≈ Sounds like <strong>"Sealed-Shut"</strong> behind bolted doors = <em>Closed</em>!',
        '<strong>Band</strong> ≈ Shut tight (think <strong>"City Bandh / Shut down"</strong>) = <em>Closed</em>!'
    ),
    483: (
        '<strong>Fácil</strong> ≈ Root of <strong>"Facilitate"</strong> (make smooth) | <strong>Sencillo</strong> ≈ Plain and <em>Simple/Easy</em>!',
        '<strong>Aasaan</strong> ≈ Smooth sailing without struggle (paired with Tamil <strong>சரளம் = Fluent/Easy</strong>) = <em>Easy</em>!'
    ),
    484: (
        '<strong>Difícil</strong> ≈ Twin of <strong>"Difficult"</strong> | <strong>Complicado</strong> ≈ Twin of <strong>"Complicated"</strong> puzzle = <em>Difficult</em>!',
        '<strong>Mushkil</strong> ≈ Tough climb (think <em>"Must-use-skill"</em> to solve it) = <em>Difficult</em>!'
    ),
    485: (
        '<strong>Simple</strong> ≈ Twin of <strong>"Simple"</strong> | <strong>Sencillo</strong> ≈ Uncomplicated & <strong>"Single-step"</strong> plain = <em>Simple</em>!',
        '<strong>Seedha</strong> (Straightforward, no twists) | <strong>Aasaan</strong> (Effortless) = <em>Simple</em>!'
    ),
    486: (
        '1. Understandable: <strong>Claro</strong> (Crystal <strong>"Clarity"</strong>) | <strong>Evidente</strong> (<strong>"Evident"</strong> obvious) = <em>Clear</em>!<br>2. Transparent/sunny: <strong>Despejado</strong> (Clouds pushed away) | <strong>Claro</strong> (See-through) = <em>Clear</em>!',
        '1. Understandable: <strong>Saaf</strong> ≈ <strong>Spoken Tamil சாஃப் (Saaf = Crystal-clear!)</strong><br>2. Transparent/sunny: <strong>Saaf</strong> ≈ Cloudless & spotless = <em>Clear</em>!'
    ),
    487: (
        '<strong>Oscuro / oscura</strong> ≈ Root of English <strong>"Obscure"</strong> (hidden in shadows) = <em>Dark</em>!',
        '<strong>Andhera</strong> (Pitch-black night shadow) | <strong>Kaala</strong> (<strong>Tamil காளம் = Black/Dark!</strong>) = <em>Dark</em>!'
    ),
    488: (
        '<strong>Brillante</strong> ≈ Twin of <strong>"Brilliant"</strong> | <strong>Luminoso</strong> ≈ Root of <strong>"Luminous"</strong> glowing light = <em>Bright / Shiny</em>!',
        '<strong>Chamkila / chamkili</strong> (Sparkling from <em>Chamak</em>) | <strong>Roshan</strong> (Lit up brightly) = <em>Bright / Shiny</em>!'
    ),
    490: (
        '<strong>Silencioso</strong> (<strong>"Silent"</strong>) | <strong>Callado</strong> (Hushed voice) | <strong>Tranquilo</strong> (<strong>"Tranquil"</strong> peace) = <em>Quiet / Silent</em>!',
        '<strong>Shaant</strong> ≈ <strong>Tamil சாந்தம் (Shaantham = Peaceful!)</strong> | <strong>Chupchap</strong> ≈ Whispering <em>"Shh-Chup!"</em> silently = <em>Quiet</em>!'
    ),
    491: (
        '1. Taste: <strong>Dulce</strong> ≈ Root of <strong>"Dulcet"</strong> sugary sweetness = <em>Sweet</em>!<br>2. Kind personality: <strong>Tierno</strong> (Warm & <strong>"Tender"</strong>) | <strong>Dulce</strong> (Gentle) = <em>Sweet</em>!',
        '1. Taste: <strong>Meetha / meethi</strong> ≈ Sweet like a <strong>Mithai</strong> dessert box = <em>Sweet</em>!<br>2. Kind personality: <strong>Pyaara / pyaari</strong> ≈ From <strong>Pyaar</strong> (Love) → Warm-hearted = <em>Sweet</em>!'
    ),
    492: (
        '<strong>Agrio / agria</strong> ≈ Twin of <strong>"Acrid"</strong> tang | <strong>Ácido</strong> ≈ Twin of <strong>"Acid"</strong> citrus bite = <em>Sour</em>!',
        '<strong>Khatta / khatti</strong> ≈ Mouth-puckering tang of raw mango or lime (think <em>Cut-tart</em>!) = <em>Sour</em>!'
    ),
    493: (
        '<strong>Amargo / amarga</strong> ≈ Sounds like biting an <strong>"Almond-bark"</strong> sharp taste = <em>Bitter</em>!',
        '<strong>Kadva / kadvi</strong> ≈ Same root as <strong>Tamil கடு / கசப்பு (Kadu = Harsh/Bitter!)</strong> = <em>Bitter</em>!'
    ),
    494: (
        '<strong>Salado / salada</strong> ≈ Sprinkled with ocean <strong>"Sal / Salt"</strong> = <em>Salty</em>!',
        '<strong>Namkeen</strong> ≈ Made from <strong>Namak</strong> (Salt) → Classic Indian crispy <em>Salty</em> snack!'
    ),
    495: (
        '<strong>Picante</strong> ≈ Piquant chili prick | <strong>Picoso</strong> ≈ Poking your tongue with fiery spice = <em>Spicy</em>!',
        '<strong>Teekha</strong> (Fiery chili bite) | <strong>Masaaledaar</strong> (Loaded with <strong>Tamil மசாலா</strong> spices!) = <em>Spicy</em>!'
    ),
    496: (
        '<strong>Delicioso</strong> (<strong>"Delicious"</strong>) | <strong>Rico</strong> (<strong>"Rich"</strong> flavor!) | <strong>Sabroso</strong> (From <strong>Sabor</strong> = Savor!) = <em>Delicious</em>!',
        '<strong>Swadisht</strong> (<strong>Tamil சுவை / ஸ்வாது = Tasty!</strong>) | <strong>Mazedaar</strong> (<strong>Spoken Tamil மஜா = Fun/Yummy!</strong>) = <em>Delicious</em>!'
    ),
    497: (
        '<strong>Hermoso</strong> (Glorious) | <strong>Bonito</strong> (<strong>"Bonny"</strong>) | <strong>Linda</strong> (<strong>"Lovely"</strong>) = <em>Beautiful / Pretty</em>!',
        '<strong>Sundar</strong> ≈ <strong>Tamil சுந்தரம் (Sundaram = Beauty!)</strong> | <strong>Khoobsurat</strong> ≈ <strong>Khoob</strong> (Great) + <strong>Surat</strong> (Face) = <em>Beautiful</em>!'
    ),
    498: (
        '<strong>Guapo</strong> (Dashing gentleman) | <strong>Atractivo</strong> (Twin of English <strong>"Attractive"</strong>) = <em>Handsome</em>!',
        '<strong>Khoobsurat</strong> (Fine features: <strong>Khoob + Surat</strong>) | <strong>Smart</strong> (Sharp dapper look) = <em>Handsome</em>!'
    ),
    499: (
        '<strong>Feo / fea</strong> ≈ Sounds like wrinkling your nose saying <strong>"Feh!"</strong> at something grim = <em>Ugly</em>!',
        '<strong>Badsoorat</strong> ≈ <strong>Bad</strong> (Ill) + <strong>Surat</strong> (Face) | <strong>Ganda dikhne wala</strong> (Looking awful) = <em>Ugly</em>!'
    ),
    500: (
        '<strong>Tierno / tierna</strong> (Warm & <strong>"Tender"</strong>) | <strong>Lindo / linda</strong> (Sweet little darling) = <em>Cute</em>!',
        '<strong>Pyaara / pyaari</strong> ≈ From <strong>Pyaar</strong> (Love) → Makes everyone smile with affection = <em>Cute</em>!'
    ),
    502: (
        '<strong>Triste</strong> ≈ Sounds like <strong>"Tear-Stained"</strong> downcast eyes (think <em>Tragic</em>) = <em>Sad</em>!',
        '<strong>Udaas</strong> (Heavy-hearted blues) | <strong>Dukhi</strong> ≈ <strong>Tamil துக்கம் (Dukkam = Sorrow!)</strong> = <em>Sad</em>!'
    ),
    503: (
        '<strong>Enojado</strong> (Fed up & cross) | <strong>Enfadado</strong> (Fuming mad — sounds like <em>Offended</em>) = <em>Angry</em>!',
        '<strong>Gussa</strong> (Boiling temper — <em>"Gussa mat karo!"</em>) | <strong>Naraaz</strong> (Sulkily upset & mad) = <em>Angry</em>!'
    ),
    504: (
        '<strong>Tranquilo</strong> (Root of <strong>"Tranquil"</strong> stillness) | <strong>Calmado</strong> (Cool & <strong>"Calm"</strong>) = <em>Calm</em>!',
        '<strong>Shaant</strong> ≈ <strong>Tamil சாந்தம் (Shaantham = Serene!)</strong> | <strong>Sukoon se</strong> ≈ Deep peaceful relief = <em>Calm</em>!'
    ),
    505: (
        '<strong>Emocionado / emocionada</strong> ≈ Thrilled with high <strong>"Emotion"</strong> and cheers = <em>Excited</em>!',
        '<strong>Khush</strong> (<strong>Spoken Tamil குஷி = Joyful!</strong>) | <strong>Excited</strong> (Pumped with thrill) = <em>Excited</em>!'
    ),
    506: (
        '<strong>Cansado</strong> (Knees sagging from heavy labor) | <strong>Agotado</strong> (<strong>"All-Got-Out"</strong> of fuel!) = <em>Tired</em>!',
        '<strong>Thaka hua / thaki hui</strong> ≈ Drained by <strong>Thakaan</strong> (Exhaustion after a long trek) = <em>Tired</em>!'
    ),
    507: (
        '<strong>Somnoliento</strong> (Root of <strong>"Somnolent / Insomnia"</strong>) | <strong>Con sueño</strong> (Literally "With dreams/sleep") = <em>Sleepy</em>!',
        '<strong>Neend mein / neend aana</strong> ≈ <strong>Neend</strong> (Drowsy slumber — sounds like <em>"Nodding off"</em>) + <strong>Aana</strong> (Coming on) = <em>Sleepy</em>!'
    ),
    508: (
        '<strong>Hambriento / tener hambre</strong> ≈ Stomach growling for a juicy <strong>"Hamburger"</strong> (<em>Hambre</em>) = <em>Hungry</em>!',
        '<strong>Bhookha / bhookh lagna</strong> ≈ Empty belly roaring <strong>"Bhoo-Khaa (Eat!)"</strong> = <em>Hungry</em>!'
    ),
    509: (
        '<strong>Sediento / tener sed</strong> ≈ Throat parched dry like dry <strong>"Sand"</strong> (<em>Sed</em> = Thirst) = <em>Thirsty</em>!',
        '<strong>Pyaasa / pyaas lagna</strong> ≈ Longing for cool <em>Paani</em> (think <strong>"Pining-for-water"</strong>) = <em>Thirsty</em>!'
    ),
    510: (
        '<strong>Enfermo / enferma</strong> (In the <strong>"Infirmary"</strong>) | <strong>Malo</strong> (Feeling awful/ill) = <em>Sick</em>!',
        '<strong>Beemar</strong> ≈ Unwell and resting in bed with fever/illness (think <em>"Bed-rest needed"</em>) = <em>Sick</em>!'
    ),
    512: (
        '<strong>Valiente</strong> ≈ Twin of English <strong>"Valiant"</strong> hero charging forward without fear = <em>Brave</em>!',
        '<strong>Bahadur</strong> (Fearless warrior spirit) | <strong>Himmati</strong> (From <strong>Himmat</strong> = Courage/Guts!) = <em>Brave</em>!'
    ),
    514: (
        '<strong>Orgulloso / orgullosa</strong> ≈ Standing tall with chest out (think <strong>"Our-Gold-Medal"</strong> moment) = <em>Proud</em>!',
        '<strong>Garv hona</strong> ≈ <strong>Tamil கர்வம் (Garvam = Pride!)</strong> | <strong>Fakr hona</strong> ≈ Honored glory = <em>Proud</em>!'
    ),
    515: (
        '<strong>Tímido / tímida</strong> (<strong>"Timid"</strong>) | <strong>Vergonzoso</strong> (Bashfully blushing with shyness) = <em>Shy</em>!',
        '<strong>Sharmeela</strong> (From <strong>Sharam</strong> = Bashfulness) | <strong>Jhijhakne wala</strong> (Hesitating nervously) = <em>Shy</em>!'
    ),
    516: (
        '<strong>Amable</strong> (<strong>"Amiable"</strong>) | <strong>Educado</strong> (Well-mannered) | <strong>Cortés</strong> (<strong>"Courteous"</strong>) = <em>Kind / Polite</em>!',
        '<strong>Achha</strong> (Warm-hearted) | <strong>Shareef</strong> (Gentlemanly) | <strong>Tameezdaar</strong> (Respectful manners) = <em>Kind / Polite</em>!'
    ),
    517: (
        '<strong>Honesto</strong> (True to word) | <strong>Sincero</strong> (<strong>"Sincere"</strong>) | <strong>Honrado</strong> (<strong>"Honor"</strong>-bound) = <em>Honest</em>!',
        '<strong>Imaandaar</strong> (Full of <em>Imaan</em> / Integrity) | <strong>Sachha</strong> ≈ <strong>Tamil சத்தியம் (Sathiyam = Truth!)</strong> = <em>Honest</em>!'
    ),
    519: (
        '1. Humorous: <strong>Gracioso</strong> (<strong>"Graceful"</strong> wit) | <strong>Chistoso</strong> (Joke-cracking) | <strong>Cómico</strong> (<strong>"Comic"</strong>) = <em>Funny</em>!<br>2. Strange: <strong>Raro</strong> (<strong>"Rare"</strong> oddity) | <strong>Extraño</strong> (<strong>"Strange"</strong>) = <em>Odd / Funny</em>!',
        '1. Humorous: <strong>Mazedaar</strong> (<strong>Spoken Tamil மஜா = Fun!</strong>) | <strong>Hasi aane wala</strong> (Makes you laugh <em>Hasi</em>) = <em>Funny</em>!<br>2. Strange: <strong>Ajeeb</strong> ≈ Bizarre or uncanny = <em>Strange / Funny</em>!'
    ),
    520: (
        '<strong>Serio / seria</strong> (Sober-faced & earnest) | <strong>Grave</strong> (<strong>"Grave"</strong> weighty matter) = <em>Serious</em>!',
        '<strong>Serious</strong> (No-nonsense focus) | <strong>Sanjeeda</strong> (Thoughtful & calm composure) = <em>Serious</em>!'
    ),
    524: (
        '<strong>Ocupado / ocupada</strong> ≈ Hands completely <strong>"Occupied"</strong> with non-stop tasks = <em>Busy</em>!',
        '<strong>Kaam mein laga</strong> (Absorbed in work <em>Kaam</em>) | <strong>Busy</strong> (Booked solid) = <em>Busy</em>!'
    ),
    525: (
        '<strong>Color</strong> ≈ Paint-box palette of bright hues (same Latin root as <em>Coloratura</em>) = <em>Color</em>!',
        '<strong>Rang</strong> ≈ <strong>Tamil ரங்கம் / ரங்கோலி (Rangam = Festival of bright hues!)</strong> = <em>Color</em>!'
    ),
    526: (
        '<strong>Rojo / roja</strong> ≈ Fiery ruby glow (sounds like <em>"Royal-Rose"</em> crimson) = <em>Red</em>!',
        '<strong>Laal</strong> ≈ Famous in <strong>Laal Qila (Red Fort)</strong> & ruby jewels = <em>Red</em>!'
    ),
    527: (
        '<strong>Azul</strong> ≈ Same Arabic-Spanish origin as English <strong>"Azure"</strong> deep-sky tint = <em>Blue</em>!',
        '<strong>Neela / neeli</strong> ≈ <strong>Tamil நீலம் (Neelam = Deep ocean & sapphire blue!)</strong> = <em>Blue</em>!'
    ),
    529: (
        '<strong>Amarillo / amarilla</strong> ≈ Golden sunshine glow (picture an <strong>"Armadillo"</strong> basking in bright yellow sunlight) = <em>Yellow</em>!',
        '<strong>Peela / peeli</strong> ≈ Golden turmeric hue (same root as <strong>Tamil பீத / மஞ்சள்</strong> gold-pale) = <em>Yellow</em>!'
    ),
    530: (
        '<strong>Negro / negra</strong> ≈ Deep midnight darkness (Latin root <em>Niger</em> = jet dark) = <em>Black</em>!',
        '<strong>Kaala / kaali</strong> ≈ <strong>Tamil காளம் (Kaalam = Pitch-black ink/cloud!)</strong> = <em>Black</em>!'
    ),
    531: (
        '<strong>Blanco / blanca</strong> ≈ Fresh <strong>"Blank"</strong> snow-bright canvas before painting = <em>White</em>!',
        '<strong>Safed</strong> ≈ Crisp snow or milk brightness (think <strong>"Soft-Fade"</strong> into pure light, like <em>Safed Mahal</em>!) = <em>White</em>!'
    ),
    532: (
        '<strong>Morado</strong> (Mulberry-berry shade) | <strong>Púrpura</strong> (Royal Tyrian purple dye) = <em>Purple</em>!',
        '<strong>Baingani</strong> ≈ Color of glossy purple <strong>Baingan (Eggplant / Brinjal)</strong> = <em>Purple</em>!'
    ),
    533: (
        '<strong>Rosa / rosado / rosada</strong> ≈ Soft pastel petals of a blooming garden <strong>"Rose"</strong> = <em>Pink</em>!',
        '<strong>Gulaabi</strong> ≈ From <strong>Gulaab</strong> (Rose flower — think <em>Gulab Jamun / Pink City</em>) = <em>Pink</em>!'
    ),
    534: (
        '<strong>Marrón</strong> (Roasted chestnut <strong>"Maroon"</strong>) | <strong>Café</strong> (Dark roasted coffee bean) = <em>Brown</em>!',
        '<strong>Bhoora / bhoori</strong> ≈ Rich roasted mud & tree-bark shade (sounds like <em>"Burnt-earth"</em>) = <em>Brown</em>!'
    ),
    535: (
        '<strong>Gris</strong> ≈ Overcast storm cloud / <strong>"Grizzled"</strong> silver-ash hair = <em>Gray</em>!',
        '<strong>Grey</strong> ≈ Foggy slate-ash shade between charcoal black and chalk white = <em>Gray</em>!'
    ),
    538: (
        '<strong>Forma</strong> (Outer <strong>"Form"</strong> outline) | <strong>Figura</strong> (Geometric <strong>"Figure"</strong> silhouette) = <em>Shape</em>!',
        '<strong>Shape</strong> (Outline silhouette) | <strong>Roop</strong> ≈ <strong>Tamil ரூபம் (Roopam = Form / Visage!)</strong> = <em>Shape</em>!'
    ),
    539: (
        '<strong>Círculo</strong> (Spinning round wheel) | <strong>Redondel</strong> (Round <strong>"Rotunda"</strong> ring) = <em>Circle</em>!',
        '<strong>Gola</strong> ≈ <strong>Tamil கோளம் (Golam = Round sphere / Orb!)</strong> = <em>Circle</em>!'
    ),
    540: (
        '1. Shape: <strong>Cuadrado</strong> ≈ Root of <strong>"Quad"</strong> (4 equal corners) = <em>Square</em>!<br>2. Town plaza: <strong>Plaza</strong> ≈ Open stone civic market courtyard = <em>Town Square</em>!',
        '1. Shape: <strong>Chaukona</strong> ≈ <strong>Chau</strong> (Four) + <strong>Kona</strong> (<strong>Tamil கோணம் = Corner!</strong>) = <em>Square</em>!<br>2. Town plaza: <strong>Chowk</strong> ≈ 4-way town crossroads hub = <em>Town Square</em>!'
    ),
    541: (
        '<strong>Triángulo</strong> ≈ Prefix <strong>Tri-</strong> (Three) + <strong>Ángulo</strong> (Angle/Corner) = <em>Triangle</em>!',
        '<strong>Tikona</strong> ≈ <strong>Ti</strong> (<strong>Tamil திரி = Three</strong>) + <strong>Kona</strong> (<strong>Tamil கோணம் = Corner!</strong>) = <em>Triangle</em>!'
    ),
    542: (
        '1. Drawn stripe: <strong>Línea</strong> (Pencil stroke) | <strong>Raya</strong> (Laser <strong>"Ray"</strong> streak) = <em>Line</em>!<br>2. Queue: <strong>Fila</strong> (Single <strong>"File"</strong>) | <strong>Cola</strong> (Waiting "Tail") = <em>Line</em>!',
        '1. Drawn stripe: <strong>Lakeer</strong> ≈ Chalk streak across the page (think <strong>"Long-Line"</strong>)!<br>2. Queue: <strong>Kataar</strong> ≈ People standing shoulder-to-shoulder in a ticket queue = <em>Line</em>!'
    ),
    543: (
        '1. Dot/score: <strong>Punto</strong> ≈ Pinpoint <strong>"Punctuation"</strong> dot or game score = <em>Point</em>!<br>2. Gesture/indicate: <strong>Señalar</strong> (<strong>"Signal"</strong>) | <strong>Apuntar</strong> (Aim finger) = <em>Point</em>!',
        '1. Dot/score: <strong>Point</strong> (Score mark) | <strong>Nishaan</strong> (Spot/Mark) = <em>Point</em>!<br>2. Gesture/indicate: <strong>Ishara karna</strong> (Hand signal) | <strong>Dikhana</strong> (Show) = <em>Point</em>!'
    ),
    544: (
        '1. Singular: <strong>Persona</strong> ≈ One individual human being = <em>Person</em>!<br>2. Plural: <strong>Personas</strong> (Individuals) | <strong>Gente</strong> ≈ Root of <strong>"Gentry"</strong> (Crowd) = <em>People</em>!',
        '1. Singular: <strong>Aadmi</strong> (Human) | <strong>Insaan</strong> (Mortal soul) = <em>Person</em>!<br>2. Plural: <strong>Log</strong> ≈ Crowd of folks (paired with Tamil <strong>ஜனதா / லோகம்</strong>) = <em>People</em>!'
    ),
    547: (
        '<strong>Chico</strong> (Young lad) | <strong>Niño</strong> (Like <strong>"El Niño"</strong>) | <strong>Muchacho</strong> (Energetic youth) = <em>Boy</em>!',
        '<strong>Ladka</strong> ≈ Young male youth (masculine <em>-a</em> ending, vs <em>Ladki</em> = girl) = <em>Boy</em>!'
    ),
    548: (
        '<strong>Chica</strong> (Young lass) | <strong>Niña</strong> (Feminine of <em>Niño</em>) | <strong>Muchacha</strong> (Young maiden) = <em>Girl</em>!',
        '<strong>Ladki</strong> ≈ Young female youth (feminine <em>-i</em> ending, vs <em>Ladka</em> = boy) = <em>Girl</em>!'
    ),
    549: (
        '<strong>Niño / niña</strong> (Little kid) | <strong>Hijo</strong> (Son / Offspring — sounds like <strong>"He-Junior"</strong>) = <em>Child</em>!',
        '<strong>Bachha / bachhi</strong> ≈ Playful toddler/kid (think <strong>"Bouncing little bundle"</strong>) = <em>Child</em>!'
    ),
    550: (
        '<strong>Bebé</strong> (Crying infant in cradle) | <strong>Nene</strong> (Sweet little toddler) = <em>Baby</em>!',
        '<strong>Chhota bachha</strong> ≈ <strong>Chhota</strong> (Tiny/Little) + <strong>Bachha</strong> (Child) = <em>Baby</em>!'
    ),
    551: (
        '<strong>Adulto / adulta</strong> ≈ Fully grown-up citizen taking responsibility = <em>Adult</em>!',
        '<strong>Bada</strong> (Grown-up senior) | <strong>Jawaan</strong> (Vigorous youth/soldier) = <em>Adult</em>!'
    ),
    552: (
        '<strong>Familia</strong> ≈ Parents, kids & kin sharing one roof and dinner table = <em>Family</em>!',
        '<strong>Parivaar</strong> ≈ Identical to <strong>Tamil பரிவாரம் (Parivaaram = Kin & Household!)</strong> = <em>Family</em>!'
    ),
    554: (
        '<strong>Padre</strong> (Root of <strong>"Paternal"</strong>) | <strong>Papá</strong> (Warm childhood call <strong>"Papa"</strong>) = <em>Father</em>!',
        '<strong>Pita</strong> (<strong>Tamil பிதா = Father!</strong>) | <strong>Papa</strong> (Dad) | <strong>Abba</strong> (Respectful household father) = <em>Father</em>!'
    ),
    555: (
        '<strong>Madre</strong> (Root of <strong>"Maternal / Alma Mater"</strong>) | <strong>Mamá</strong> (Loving call <strong>"Mama"</strong>) = <em>Mother</em>!',
        '<strong>Maa</strong> (<strong>Tamil அம்மா = Mom!</strong>) | <strong>Mummy</strong> (Household mom) | <strong>Ammi</strong> (Tender mom call) = <em>Mother</em>!'
    ),
    556: (
        '<strong>Hijo</strong> ≈ Sounds like <strong>"He-Junior"</strong> carrying the family name forward = <em>Son</em>!',
        '<strong>Beta</strong> ≈ Affectionate Indian term for a boy/offspring (<em>"Mera Beta"</em> = My son) = <em>Son</em>!'
    ),
    557: (
        '<strong>Hija</strong> ≈ Feminine pair of <em>Hijo</em> ("She-Junior" in the family) = <em>Daughter</em>!',
        '<strong>Beti</strong> ≈ Feminine pair of <em>Beta</em> (<em>"Beti Bachao"</em> = Save the daughter) = <em>Daughter</em>!'
    ),
    559: (
        '<strong>Hermana</strong> ≈ Female pair of <em>Hermano</em> (Think <strong>"Her-Mana"</strong> = Sisterly guardian) = <em>Sister</em>!',
        '<strong>Behen</strong> ≈ Loving female sibling (famous in <strong>Raksha Bandhan</strong> sibling festival) = <em>Sister</em>!'
    ),
    560: (
        '<strong>Esposo</strong> (Root of <strong>"Spouse"</strong>) | <strong>Marido</strong> (Root of <strong>"Married"</strong> partner) = <em>Husband</em>!',
        '<strong>Pati</strong> (<strong>Tamil பதி = Husband!</strong>) | <strong>Shohar</strong> (Wedding groom & married partner) = <em>Husband</em>!'
    ),
    561: (
        '<strong>Esposa</strong> (Female <strong>"Spouse"</strong>) | <strong>Mujer</strong> (Woman / Partner at home) = <em>Wife</em>!',
        '<strong>Patni</strong> (<strong>Tamil பத்தினி = Wife!</strong>) | <strong>Biwi</strong> (Everyday warm word for married partner) = <em>Wife</em>!'
    ),
    562: (
        '<strong>Abuelo</strong> ≈ Wise elder <strong>"Ah-Well-Old"</strong> telling family stories by the fire = <em>Grandfather</em>!',
        '<strong>Dada</strong> (Father\'s father — older <em>Dad</em>!) | <strong>Nana</strong> (Mother\'s father) = <em>Grandfather</em>!'
    ),
    563: (
        '<strong>Abuela</strong> ≈ Feminine pair of <em>Abuelo</em> (loving silver-haired matriarch) = <em>Grandmother</em>!',
        '<strong>Dadi</strong> (Father\'s mother — feminine of <em>Dada</em>) | <strong>Nani</strong> (Mother\'s mother) = <em>Grandmother</em>!'
    ),
    564: (
        '<strong>Tío</strong> ≈ Sounds like sharing evening <strong>"Tea-Oh"</strong> with your fun <em>Uncle</em>!',
        '<strong>Chacha</strong> (Father\'s brother) | <strong>Mama</strong> (<strong>Tamil மாமா!</strong>) | <strong>Fufa</strong> (Aunt\'s husband) | <strong>Mausa</strong> (Mother\'s sister\'s husband) = <em>Uncle</em>!'
    ),
    565: (
        '<strong>Tía</strong> ≈ Feminine pair of <em>Tío</em> (warm family <em>Aunt</em>)!',
        '<strong>Chachi</strong> (Uncle\'s wife) | <strong>Mami</strong> (<strong>Tamil மாமி!</strong>) | <strong>Bua</strong> (Father\'s sister) | <strong>Mausi</strong> (Mother\'s sister) = <em>Aunt</em>!'
    ),
    567: (
        '<strong>Sobrino</strong> ≈ Think <strong>"So-Bright-Nephew"</strong> cheering at family reunions = <em>Nephew</em>!',
        '<strong>Bhatija</strong> (Brother\'s son — <em>Bhai</em> + son) | <strong>Bhanja</strong> (Sister\'s son) = <em>Nephew</em>!'
    ),
    568: (
        '<strong>Sobrina</strong> ≈ Feminine pair of <em>Sobrino</em> (smiling little family <em>Niece</em>)!',
        '<strong>Bhatiji</strong> (Brother\'s daughter) | <strong>Bhanji</strong> (Sister\'s daughter) = <em>Niece</em>!'
    ),
    571: (
        '<strong>Vecino / vecina</strong> ≈ Root of English <strong>"Vicinity"</strong> (folks living right next door) = <em>Neighbor</em>!',
        '<strong>Padosi</strong> ≈ Living right across the wall (from <strong>Pados</strong> = neighborhood next door) = <em>Neighbor</em>!'
    ),
    572: (
        '<strong>Invitado / invitada</strong> (Literally "The <strong>Invited</strong> one") | <strong>Huésped</strong> (Root of <strong>"Hospitality"</strong>) = <em>Guest</em>!',
        '<strong>Mehmaan</strong> ≈ Welcomed visitor treated like royalty (<em>"Mehmaan Bhagwan hota hai"</em>) = <em>Guest</em>!'
    ),
    575: (
        '1. King: <strong>Rey</strong> ≈ Root of <strong>"Royal / Regal / Rex"</strong> = <em>King</em>!<br>2. Queen: <strong>Reina</strong> ≈ Root of <strong>"Reign"</strong> over the palace = <em>Queen</em>!',
        '1. King: <strong>Raja</strong> (<strong>Tamil ராஜா!</strong>) | <strong>Badshah</strong> (Imperial Emperor) = <em>King</em>!<br>2. Queen: <strong>Rani</strong> ≈ Identical to <strong>Tamil ராணி (Raani!)</strong> = <em>Queen</em>!'
    ),
    576: (
        '<strong>Líder</strong> (Captain) | <strong>Dirigente</strong> (<strong>"Directing"</strong> manager) | <strong>Jefe</strong> (<strong>"Chief"</strong> boss) = <em>Leader</em>!',
        '<strong>Neta</strong> ≈ <strong>Spoken Tamil நேதா (like Netaji!)</strong> | <strong>Leader</strong> (Guiding captain) = <em>Leader</em>!'
    ),
    578: (
        '1. Anatomy: <strong>Cabeza</strong> ≈ Root of <strong>"Captain / Capitol"</strong> (top of the body) = <em>Head</em>!<br>2. Chief/leader: <strong>Jefe</strong> (<strong>"Chief"</strong>) | <strong>Líder</strong> (Team captain) = <em>Head / Leader</em>!',
        '1. Anatomy: <strong>Sir</strong> ≈ Same root as <strong>Tamil சிரம் (Siram = Head!)</strong> = <em>Head</em>!<br>2. Chief/leader: <strong>Mukhiya</strong> (<strong>Tamil முக்கியம் = Main!</strong>) | <strong>Boss</strong> (Commander) = <em>Head / Chief</em>!'
    ),
    579: (
        '<strong>Pelo</strong> (Root of <strong>"Pelt"</strong> coat) | <strong>Cabello</strong> (Silky strands on top of the scalp) = <em>Hair</em>!',
        '<strong>Baal</strong> ≈ Same root as <strong>Tamil வாலம் / மயிர்</strong> (Strands growing down your head) = <em>Hair</em>!'
    ),
    580: (
        '<strong>Cara</strong> (Front expression) | <strong>Rostro</strong> (Root of <strong>"Rostrum"</strong> — front stage look) = <em>Face</em>!',
        '<strong>Chehra</strong> (Facial features) | <strong>Moonh</strong> ≈ <strong>Tamil முகம் (Mugam = Face/Mouth!)</strong> = <em>Face</em>!'
    ),
    581: (
        '<strong>Frente</strong> ≈ Top <strong>"Front"</strong> wall right above your eyebrows = <em>Forehead</em>!',
        '<strong>Maatha</strong> ≈ Smooth brow where you place a sacred tilak/bindi mark (Think <em>"Master-mind brow"</em>) = <em>Forehead</em>!'
    ),
    583: (
        '<strong>Oreja</strong> (Outer curved shell — sounds like <strong>"O-Hear-a"</strong>) | <strong>Oído</strong> (Root of <strong>"Audio"</strong> inner hearing) = <em>Ear</em>!',
        '<strong>Kaan</strong> ≈ Same root as <strong>Tamil கர்ணம் (Karnam ≈ Kaan = Listening organ!)</strong> = <em>Ear</em>!'
    ),
    584: (
        '<strong>Nariz</strong> ≈ Root of English <strong>"Nasal / Nostril"</strong> breathing passage = <em>Nose</em>!',
        '<strong>Naak</strong> ≈ Same root as <strong>Tamil நாசி (Naasi ≈ Naak = Sniffing organ!)</strong> = <em>Nose</em>!'
    ),
    585: (
        '<strong>Mejilla</strong> (Soft rosy side of the face) | <strong>Cachete</strong> (Pinchable plump rosy cheek) = <em>Cheek</em>!',
        '<strong>Gaal</strong> ≈ Plump side of your face (Think <strong>"Chubby Glow"</strong> when smiling) = <em>Cheek</em>!'
    ),
    586: (
        '<strong>Boca</strong> ≈ Root of <strong>"Vocal"</strong> & sunny city <em>Boca Raton</em> (speaking & eating opening) = <em>Mouth</em>!',
        '<strong>Moonh</strong> ≈ Same root as <strong>Tamil முகம் (Mugam = Face / Mouth opening!)</strong> = <em>Mouth</em>!'
    ),
    587: (
        '<strong>Labio</strong> ≈ Root of English <strong>"Labial"</strong> (soft outer edge used to pronounce B/P/M) = <em>Lip</em>!',
        '<strong>Honth</strong> ≈ Soft rim framing your smile (Think <strong>"Humming-edge"</strong> around the mouth) = <em>Lip</em>!'
    ),
    589: (
        '1. Anatomy: <strong>Lengua</strong> ≈ Muscular taste organ inside the mouth (root of <strong>"Lingual"</strong>) = <em>Tongue</em>!<br>2. Language: <strong>Lengua</strong> | <strong>Idioma</strong> (Root of <strong>"Idiom"</strong>) = <em>Language / Tongue</em>!',
        '1. Anatomy: <strong>Jeebh</strong> ≈ <strong>Tamil ஜிஹ்வை (Jihva ≈ Jeebh = Taste organ!)</strong> = <em>Tongue</em>!<br>2. Language: <strong>Bhasha</strong> (<strong>Tamil பாஷை!</strong>) | <strong>Zabaan</strong> (Spoken speech) = <em>Language / Tongue</em>!'
    ),
    590: (
        '<strong>Barbilla</strong> (From <strong>Barba</strong> = Beard tip) | <strong>Mentón</strong> (Root of <strong>"Mental / Thinker pose"</strong> resting on chin!) = <em>Chin</em>!',
        '<strong>Thodi</strong> ≈ Bottom tip below your lower lip (Think <strong>"A Thoughtful rest"</strong> on your palm) = <em>Chin</em>!'
    ),
    591: (
        '<strong>Cuello</strong> ≈ Root of English <strong>"Collar"</strong> hugging the throat and spine = <em>Neck</em>!',
        '<strong>Gardan</strong> ≈ Stem supporting your head (think <strong>"Guard-head pillar"</strong> turning left & right) = <em>Neck</em>!'
    ),
    594: (
        '1. Anatomy: <strong>Pecho</strong> ≈ Root of <strong>"Pectoral"</strong> ribcage muscles = <em>Chest</em>!<br>2. Box/trunk: <strong>Baúl</strong> (Steamer trunk) | <strong>Caja</strong> (<strong>"Cash-box"</strong> container) = <em>Chest / Box</em>!',
        '1. Anatomy: <strong>Chhati</strong> (Front ribcage) | <strong>Seena</strong> (Proud broad front) = <em>Chest</em>!<br>2. Box/trunk: <strong>Sandook</strong> (Heavy lockbox) | <strong>Baksa</strong> (English <strong>"Box"</strong>) = <em>Chest / Trunk</em>!'
    ),
    595: (
        '<strong>Espalda</strong> ≈ Along your rear <strong>"Spinal"</strong> column between shoulder blades = <em>Back (Body)</em>!',
        '<strong>Peeth</strong> ≈ Broad rear side opposite the chest (Think <strong>"Carry a pack on your rear pillar"</strong>) = <em>Back (Body)</em>!'
    ),
    596: (
        '<strong>Cintura</strong> ≈ Narrow midsection where you buckle your <strong>Cinturón</strong> (belt) = <em>Waist</em>!',
        '<strong>Kamar</strong> ≈ Middle bend around the hips (Think <strong>"Cummerbund sash"</strong> tied around it!) = <em>Waist</em>!'
    ),
    597: (
        '<strong>Estómago</strong> (Digestive organ) | <strong>Barriga</strong> (Rounded <strong>"Barrel"</strong> belly after dinner) = <em>Stomach</em>!',
        '<strong>Pet</strong> ≈ Identical to <strong>Spoken Tamil பேட் / தொப்பை</strong> (Soft belly where food digests) = <em>Stomach</em>!'
    ),
    598: (
        '<strong>Brazo</strong> ≈ Root of English <strong>"Brace / Embrace"</strong> hugging tightly = <em>Arm</em>!',
        '<strong>Baanh</strong> (Upper limb) | <strong>Baazu</strong> (Sleeve/side limb — think <em>"Side-by-side wingman"</em>) = <em>Arm</em>!'
    ),
    604: (
        '1. Fingernail: <strong>Uña</strong> ≈ Root of <strong>"Ungulate"</strong> (hard claw/tip) = <em>Fingernail</em>!<br>2. Metal hardware: <strong>Clavo</strong> ≈ Sharp <strong>"Clove"</strong>-shaped iron spike = <em>Nail</em>!',
        '1. Fingernail: <strong>Nakhun</strong> ≈ <strong>Tamil நகம் (Nagam ≈ Nakhun!)</strong> = <em>Fingernail</em>!<br>2. Metal hardware: <strong>Keel</strong> ≈ Sharp iron spike hammered into a wall (Think <em>"Steel keel spike"</em>) = <em>Nail</em>!'
    ),
    605: (
        '<strong>Pierna</strong> ≈ Sturdy bridge <strong>"Pier-Pillar"</strong> carrying your stride = <em>Leg</em>!',
        '<strong>Taang</strong> ≈ Long walking limb below the hip (think <strong>"Tall-stride pillar"</strong>) = <em>Leg</em>!'
    ),
    606: (
        '<strong>Muslo</strong> ≈ Built from the largest <strong>"Muscle"</strong> above the knee = <em>Thigh</em>!',
        '<strong>Jaangh</strong> ≈ Strong upper leg segment above the knee (think <strong>"Jump-spring"</strong> power!) = <em>Thigh</em>!'
    ),
    607: (
        '<strong>Rodilla</strong> ≈ Sound-cue <strong>"Roll-de-ya"</strong> → Rolling hinge joint halfway down the leg = <em>Knee</em>!',
        '<strong>Ghutna</strong> ≈ Middle leg hinge that bends when kneeling down (Think <strong>"Get-down-on-joint"</strong>) = <em>Knee</em>!'
    ),
    608: (
        '<strong>Tobillo</strong> ≈ Sound-cue <strong>"Toe-Bend-Low"</strong> → Joint right above your heel & foot = <em>Ankle</em>!',
        '<strong>Takhna</strong> ≈ Rounded bony knot connecting lower shin to the foot (Think <strong>"Twist-turn joint"</strong>) = <em>Ankle</em>!'
    ),
    609: (
        '1. Anatomy: <strong>Pie</strong> ≈ Root of <strong>"Pedal / Pedestrian"</strong> stepping on ground = <em>Foot</em>!<br>2. Measurement: <strong>Pie</strong> ≈ 12-inch ruler unit = <em>Foot</em>!',
        '1. Anatomy: <strong>Pair / paanv</strong> ≈ From Sanskrit <em>Pada</em> = <strong>Tamil பாதம்!</strong> = <em>Foot</em>!<br>2. Measurement: <strong>Fit</strong> ≈ 12-inch ruler length (spelled phonetically as <em>"Fit"</em>) = <em>Foot</em>!'
    ),
    610: (
        '<strong>Dedo del pie</strong> ≈ <strong>Dedo</strong> (Digit/Finger) + <strong>del Pie</strong> (of the Foot) = <em>Toe</em>!',
        '<strong>Pair ki ungli</strong> (Digit of the foot) | <strong>Pair ka angootha</strong> (Big thumb-digit of foot) = <em>Toe</em>!'
    ),
    611: (
        '<strong>Piel</strong> ≈ Sounds like orange <strong>"Peel"</strong> wrapping and protecting the flesh inside = <em>Skin</em>!',
        '<strong>Chamdi</strong> (<strong>Tamil சர்மம் = Hide/Coat!</strong>) | <strong>Skin</strong> (Outer covering layer) = <em>Skin</em>!'
    ),
    613: (
        '<strong>Músculo</strong> ≈ Latin origin <em>Musculus</em> ("Little flexing mouse" curling under the arm) = <em>Muscle</em>!',
        '<strong>Muscle</strong> (Flexing fiber) | <strong>Patthe</strong> (Strong sinewy arm/leg bands built at the gym) = <em>Muscle</em>!'
    ),
    614: (
        '<strong>Sangre</strong> ≈ Root of crimson <strong>"Sangria / Sanguine"</strong> pulsing through veins = <em>Blood</em>!',
        '<strong>Khoon</strong> ≈ Crimson life fluid flowing in veins (paired with Sanskrit/Tamil <strong>ரத்தம்</strong>) = <em>Blood</em>!'
    ),
    616: (
        '1. Organ: <strong>Corazón</strong> ≈ Root of <strong>"Core / Cordial"</strong> beating in your chest = <em>Heart</em>!<br>2. Core/center: <strong>Centro</strong> (Bullseye center) | <strong>Corazón</strong> (Innermost soul) = <em>Core / Heart</em>!',
        '1. Organ: <strong>Dil</strong> ≈ Famous beating organ (<em>"Dil se"</em>) = <em>Heart</em>!<br>2. Core/center: <strong>Beech</strong> (Right in the middle — sitting on the <em>"Beach"</em> between land & sea) | <strong>Dil</strong> (Hub) = <em>Center</em>!'
    ),
    617: (
        '<strong>Pulmón</strong> ≈ Root of English <strong>"Pulmonary"</strong> airway inflating with every inhale = <em>Lung</em>!',
        '<strong>Fefda</strong> ≈ Spongy twin air-bags inside the ribs inflating with oxygen (Think <em>"Puff-air bag"</em>) = <em>Lung</em>!'
    ),
    618: (
        '<strong>Cerebro</strong> (Root of <strong>"Cerebral"</strong>) | <strong>Sesos</strong> (Grey thinking matter inside skull) = <em>Brain</em>!',
        '<strong>Dimaag</strong> ≈ Command center of intelligence inside your skull (<em>"Dimaag lagao!"</em> = Use your head!) = <em>Brain</em>!'
    ),
    619: (
        '<strong>Voz</strong> ≈ Root of <strong>"Vocal / Voice"</strong> resonating from your vocal cords = <em>Voice</em>!',
        '<strong>Awaaz</strong> ≈ Sounds like <strong>"A-Voice!"</strong> ringing out clearly when speaking or singing = <em>Voice</em>!'
    ),
    620: (
        '1. From eye: <strong>Lágrima</strong> ≈ Root of <strong>"Lachrymose"</strong> (weeping droplets) = <em>Tear</em>!<br>2. Rip/shred: <strong>Romper</strong> (Burst apart) | <strong>Rasgar</strong> (Slash/shred fabric) = <em>Tear / Rip</em>!',
        '1. From eye: <strong>Aansu</strong> ≈ Same root as <strong>Tamil அஸ்ரு (Asru = Drop from eye!)</strong> = <em>Tear</em>!<br>2. Rip/shred: <strong>Faadna</strong> ≈ Sharp sound <strong>"Faad!"</strong> ripping paper cleanly in two = <em>Tear Up</em>!'
    ),
    621: (
        '1. Noun: <strong>Sudor</strong> ≈ Heat droplets (Think <strong>"Soaked-Door"</strong> in summer heat) = <em>Sweat</em>!<br>2. Verb: <strong>Sudar</strong> ≈ Action form of <em>Sudor</em> dripping after running = <em>To Sweat</em>!',
        '1. Noun: <strong>Paseena</strong> ≈ Cooling salty droplets beading on skin after hard work = <em>Sweat</em>!<br>2. Verb: <strong>Paseena aana / bahana</strong> ≈ Sweat coming out / flowing down = <em>To Sweat</em>!'
    ),
    623: (
        '<strong>Salud</strong> ≈ Origin of raising a glass <strong>"Salute / Salud!"</strong> wishing total fitness = <em>Health</em>!',
        '<strong>Sehat</strong> ≈ Body vigor and wellness (paired with Tamil <strong>ஸ்வஸ்தம் / ஆரோக்கியம்</strong>) = <em>Health</em>!'
    ),
    625: (
        '<strong>Dolor</strong> ≈ Root of English <strong>"Dolorous"</strong> aching agony = <em>Pain</em>!',
        '<strong>Dard</strong> (Sharp physical ache) | <strong>Takleef</strong> (Troubling discomfort) = <em>Pain</em>!'
    ),
    626: (
        '<strong>Fiebre</strong> (Spiking temperature) | <strong>Calentura</strong> (From <strong>Caliente</strong> = burning hot!) = <em>Fever</em>!',
        '<strong>Bukhaar</strong> ≈ Burning high temperature (Think <strong>"Bake-Hot"</strong> forehead under a thermometer!) = <em>Fever</em>!'
    ),
    627: (
        '1. Noun: <strong>Tos</strong> ≈ Sharp chest bark sounding like <strong>"Toss!"</strong> = <em>Cough</em>!<br>2. Verb: <strong>Toser</strong> ≈ Action of clearing the airway = <em>To Cough</em>!',
        '1. Noun: <strong>Khaansi</strong> ≈ Dry/wet bark from the chest (Think <strong>"Hack-Khaansi"</strong>) = <em>Cough</em>!<br>2. Verb: <strong>Khaansna</strong> ≈ Action verb of hacking out a cough = <em>To Cough</em>!'
    ),
    628: (
        '<strong>Gripe</strong> (Old term <strong>"La Grippe"</strong>) | <strong>Influenza</strong> (Viral seasonal bug) = <em>Flu</em>!',
        '<strong>Sardi-zukaam</strong> ≈ <strong>Sardi</strong> (Cold shivers) + <strong>Zukaam</strong> (Blocked sneezing nose) = <em>Flu</em>!'
    ),
    631: (
        '<strong>Medicina</strong> (Healing science) | <strong>Medicamento</strong> (Tablet dose) | <strong>Remedio</strong> (<strong>"Remedy"</strong>) = <em>Medicine</em>!',
        '<strong>Dawai</strong> ≈ Prescribed healing syrup or tablet (Think <strong>"Dose-Away"</strong> the illness!) = <em>Medicine</em>!'
    ),
    632: (
        '<strong>Pastilla</strong> (Lozenge <strong>"Pastille"</strong>) | <strong>Píldora</strong> (Small round capsule) | <strong>Tableta</strong> (Pressed <strong>"Tablet"</strong>) = <em>Pill</em>!',
        '<strong>Goli</strong> ≈ Small smooth marble-shaped capsule you swallow with water (Think <em>"Goal-round bead"</em>) = <em>Pill</em>!'
    ),
    633: (
        '<strong>Venda</strong> (Cloth <strong>"Band"</strong> wrap — B & V sound alike!) | <strong>Curita</strong> (Little "Cure" strip) = <em>Bandage</em>!',
        '<strong>Patti</strong> ≈ Identical to <strong>Tamil பட்டி (Patti = Wrapped gauze strip!)</strong> = <em>Bandage</em>!'
    ),
    634: (
        '<strong>Médico</strong> (Root of <strong>"Medical"</strong>) | <strong>Doctor</strong> (Hospital physician) = <em>Doctor</em>!',
        '<strong>Doctor</strong> ≈ Stethoscope-wearing healer at the clinic (paired with Tamil <strong>டாக்டர்</strong>) = <em>Doctor</em>!'
    ),
    635: (
        '<strong>Enfermero / enfermera</strong> ≈ Caretaker tending patients in the <strong>"Infirmary"</strong> (<em>Enfermo</em>) = <em>Nurse</em>!',
        '<strong>Nurse</strong> ≈ Caring ward attendant checking vitals & medicine rounds = <em>Nurse</em>!'
    ),
    636: (
        '1. Medical person: <strong>Paciente</strong> (Clinic visitor) | <strong>Enfermo</strong> (<strong>"Infirm"</strong> sick person) = <em>Patient</em>!<br>2. Calm/enduring: <strong>Paciente</strong> ≈ Waiting calmly without rushing = <em>Patient</em>!',
        '1. Medical person: <strong>Mareez</strong> ≈ Person under clinic care (Think <em>"Med-receives"</em> treatment) = <em>Patient</em>!<br>2. Calm/enduring: <strong>Sabr wala</strong> ≈ Filled with <strong>Sabr</strong> (Calm endurance) = <em>Patient</em>!'
    ),
    637: (
        '<strong>Hospital</strong> (Full emergency medical ward) | <strong>Clínica</strong> (Neighborhood outpatient center) = <em>Hospital / Clinic</em>!',
        '<strong>Aspatal</strong> (Pronounced from <em>Hospital</em>!) | <strong>Clinic</strong> (Local doctor office) = <em>Hospital / Clinic</em>!'
    ),
    638: (
        '<strong>Comida</strong> (From <strong>Comer</strong> = Eat) | <strong>Alimento</strong> (Root of <strong>"Aliment / Nourish"</strong>) = <em>Food</em>!',
        '<strong>Khaana</strong> ≈ Both noun ("Meal") and verb ("To eat") — cooked nourishment on your plate = <em>Food</em>!'
    ),
    639: (
        '<strong>Comida</strong> (Daily sitting to eat) | <strong>Plato</strong> (Prepared dinner course / <strong>"Plate"</strong>) = <em>Meal</em>!',
        '<strong>Waqt ka khaana</strong> ≈ <strong>Waqt</strong> (Meal-time hour) + <strong>ka Khaana</strong> (Food) = <em>Meal</em>!'
    ),
    645: (
        '<strong>Leche</strong> ≈ Root of English <strong>"Lactose"</strong> & famous drink <strong>"Café con Leche"</strong> = <em>Milk</em>!',
        '<strong>Doodh</strong> ≈ White dairy drink poured fresh every morning (from Sanskrit <em>Dugdha</em>) = <em>Milk</em>!'
    ),
    646: (
        '<strong>Té</strong> ≈ Steeping fragrant dried leaves in boiling water (same root as Amoy <em>Tê</em>!) = <em>Tea</em>!',
        '<strong>Chai</strong> ≈ Famous spiced milk-and-leaf brew poured at every street stall (from <em>Cha</em>) = <em>Tea</em>!'
    ),
    647: (
        '<strong>Café</strong> ≈ Dark roasted bean brew served in morning <strong>"Cafés"</strong> = <em>Coffee</em>!',
        '<strong>Coffee</strong> ≈ Aromatic roasted-bean morning pick-me-up = <em>Coffee</em>!'
    ),
    648: (
        '<strong>Jugo</strong> (Freshly pressed liquid) | <strong>Zumo</strong> (Citrus squeezed nectar) = <em>Juice</em>!',
        '<strong>Ras</strong> (<strong>Tamil ரசம் = Fruit essence!</strong>) | <strong>Juice</strong> (Pressed drink) = <em>Juice</em>!'
    ),
    649: (
        '<strong>Sopa</strong> (Warm bowl) | <strong>Caldo</strong> (Simmering <strong>"Cauldron"</strong> broth) = <em>Soup</em>!',
        '<strong>Shorba</strong> (Steaming spiced broth — sounds like <strong>"Slurp-Ah!"</strong>) | <strong>Soup</strong> (Hot liquid bowl) = <em>Soup</em>!'
    ),
    650: (
        '<strong>Pan</strong> ≈ Root of <strong>"Pantry / Panini / Companion"</strong> (one you break bread with) = <em>Bread</em>!',
        '<strong>Roti</strong> (Flat wheat tawa loaf) | <strong>Pav</strong> (Soft Portuguese-derived bun) | <strong>Bread</strong> (Baked loaf) = <em>Bread</em>!'
    ),
    651: (
        '<strong>Arroz</strong> ≈ Famous Spanish staple dish <strong>"Arroz con Pollo"</strong> (chicken & grain!) = <em>Rice</em>!',
        '<strong>Chawal</strong> ≈ Fluffy white grains steamed daily beside dal (Think <strong>"Chow-all"</strong> staple!) = <em>Rice</em>!'
    ),
    652: (
        '1. Grain: <strong>Trigo</strong> ≈ Tall golden stalks of <strong>"Tree-Gold"</strong> harvest = <em>Wheat</em>!<br>2. Ground powder: <strong>Harina</strong> ≈ Fine dusty <strong>"Arena-powder"</strong> for baking dough = <em>Flour</em>!',
        '1. Grain: <strong>Gehoon</strong> ≈ Golden bearded stalks harvested in spring = <em>Wheat</em>!<br>2. Ground powder: <strong>Aata</strong> (Whole-wheat dough powder) | <strong>Maida</strong> (Refined white powder) = <em>Flour</em>!'
    ),
    654: (
        '<strong>Carne</strong> ≈ Root of English <strong>"Carnivore / Chili con Carne"</strong> = <em>Meat</em>!',
        '<strong>Gosht</strong> (Tender braised butcher cut) | <strong>Meat</strong> (Protein cut from market) = <em>Meat</em>!'
    ),
    655: (
        '1. Meat: <strong>Pollo</strong> (In <em>Arroz con Pollo</em> & <strong>"Poultry"</strong>) = <em>Chicken Meat</em>!<br>2. Bird: <strong>Gallina</strong> (Laying hen) | <strong>Pollo</strong> (Young barnyard fowl) = <em>Chicken Bird</em>!',
        '1. Meat: <strong>Chicken</strong> (Cooked cut) | <strong>Murga</strong> (Rooster meat) = <em>Chicken</em>!<br>2. Bird: <strong>Murga</strong> (Rooster) | <strong>Murgi</strong> (Clucking hen) = <em>Chicken</em>!'
    ),
    657: (
        '<strong>Queso</strong> ≈ Melted golden dip <strong>"Chili con Queso / Quesadilla"</strong> = <em>Cheese</em>!',
        '<strong>Paneer</strong> (Fresh pressed Indian cottage curd) | <strong>Cheese</strong> (Aged dairy block) = <em>Cheese</em>!'
    ),
    658: (
        '<strong>Mantequilla</strong> (Smooth table spread) | <strong>Manteca</strong> (Rich cooking fat/lard) = <em>Butter</em>!',
        '<strong>Makkhan</strong> ≈ White whipped dairy spread churned fresh from cream (think Krishna stealing <em>Makkhan</em>!) = <em>Butter</em>!'
    ),
    659: (
        '<strong>Yogur</strong> ≈ Tangy fermented milk cup eaten with fruit or honey = <em>Yogurt</em>!',
        '<strong>Dahi</strong> ≈ Identical origin to <strong>Tamil தயிர் (Thayir ↔ Dahi = Cultured curd!)</strong> = <em>Yogurt</em>!'
    ),
    660: (
        '1. Cooking: <strong>Aceite</strong> ≈ Sounds like <strong>"A-Sauté"</strong> sizzling pan oil = <em>Cooking Oil</em>!<br>2. Petroleum: <strong>Petróleo</strong> (Rock-oil fuel) | <strong>Crudo</strong> (Unrefined <strong>"Crude"</strong>) = <em>Petroleum</em>!',
        '1. Cooking: <strong>Tel</strong> ≈ Same root as <strong>Tamil தைலம் (Thailam = Pressed oil!)</strong> = <em>Oil</em>!<br>2. Petroleum: <strong>Kachha tel</strong> ≈ <strong>Kachha</strong> (Raw/Unrefined) + <strong>Tel</strong> (Oil) = <em>Crude Oil</em>!'
    ),
    661: (
        '<strong>Sal</strong> ≈ Origin of <strong>"Saline / Salad / Salary"</strong> (Roman soldiers paid in salt!) = <em>Salt</em>!',
        '<strong>Namak</strong> ≈ White seasoning crystals from sea pans (famous <strong>Dandi Namak March</strong>!) = <em>Salt</em>!'
    ),
    662: (
        '<strong>Azúcar</strong> ≈ Same Arabic-Sanskrit chain (<em>Sarkara</em> → <em>As-sukkar</em> → <em>Sugar</em>) = <em>Sugar</em>!',
        '<strong>Cheeni</strong> (White crystals) | <strong>Shakkar</strong> ≈ <strong>Tamil சர்க்கரை (Sarkkarai = Cane sweet!)</strong> = <em>Sugar</em>!'
    ),
    663: (
        '1. Black spice: <strong>Pimienta</strong> ≈ Crushed <strong>"Pimento"</strong> berries crackling over pasta = <em>Black Pepper</em>!<br>2. Bell pepper: <strong>Pimiento / morrón</strong> ≈ Crisp sweet salad pepper = <em>Bell Pepper</em>!',
        '1. Black spice: <strong>Kaali mirch</strong> ≈ <strong>Kaali</strong> (Black) + <strong>Mirch</strong> (Peppercorn) = <em>Black Pepper</em>!<br>2. Bell pepper: <strong>Shimla mirch</strong> ≈ Crunchy green/red capsicum grown in cool <strong>Shimla</strong> = <em>Bell Pepper</em>!'
    ),
    664: (
        '<strong>Especia</strong> (Aromatic dried bark/seed) | <strong>Condimento</strong> (Flavoring <strong>"Condiment"</strong>) = <em>Spice</em>!',
        '<strong>Masala</strong> ≈ Identical to <strong>Tamil மசாலா (Masaalaa = Blended aromatic spices!)</strong> = <em>Spice</em>!'
    ),
    665: (
        '<strong>Miel</strong> ≈ Root of <strong>"Mellifluous"</strong> (flowing smoothly like golden honey) = <em>Honey</em>!',
        '<strong>Shehad</strong> ≈ Thick amber nectar gathered by honeybees in hives (Think <em>"Sweet-hive drip"</em>) = <em>Honey</em>!'
    ),
    666: (
        '<strong>Salsa</strong> ≈ Literally salted/seasoned <strong>"Salsa"</strong> dip poured over chips or pasta = <em>Sauce</em>!',
        '<strong>Chutney</strong> (Fresh ground herb/fruit dip) | <strong>Sauce</strong> (Bottled tomato/chili pour) = <em>Sauce</em>!'
    ),
    667: (
        '<strong>Ensalada</strong> ≈ Salted bowl of crisp greens tossed in olive oil (origin of <em>Salad</em>) = <em>Salad</em>!',
        '<strong>Kachumber</strong> (Finely diced onion-tomato-cucumber mix) | <strong>Salaad</strong> (Fresh crisp bowl) = <em>Salad</em>!'
    ),
    668: (
        '<strong>Fruta</strong> ≈ Sweet orchard harvest picked ripe from branches (root of <em>Fructose</em>) = <em>Fruit</em>!',
        '<strong>Phal</strong> ≈ Same root as <strong>Tamil பழம் (Pazham = Ripe orchard produce!)</strong> = <em>Fruit</em>!'
    ),
    669: (
        '<strong>Manzana</strong> ≈ Crisp red orchard crunch (Think of biting a sweet <em>"Man\'s-Apple"</em> in autumn!) = <em>Apple</em>!',
        '<strong>Seb</strong> ≈ Crisp red/green fruit from Kashmir orchards (Sounds like <em>"Save an apple a day!"</em>) = <em>Apple</em>!'
    ),
    670: (
        '<strong>Plátano</strong> (Plantain / tropical bunch) | <strong>Banana</strong> (Curved yellow fruit) = <em>Banana</em>!',
        '<strong>Kela</strong> ≈ Same root as <strong>Tamil கதலி (Kadhali ≈ Kela = Sweet yellow fruit!)</strong> = <em>Banana</em>!'
    ),
    671: (
        '1. Fruit: <strong>Naranja</strong> ≈ From Arabic <em>Naranj</em> (the original word before English dropped the N!) = <em>Orange</em>!<br>2. Color: <strong>Naranja / anaranjado</strong> ≈ Glowing sunset citrus tint = <em>Orange</em>!',
        '1. Fruit: <strong>Santra</strong> ≈ Juicy Nagpur citrus peel segments = <em>Orange</em>!<br>2. Color: <strong>Naarangi</strong> ≈ Origin of English word <strong>"Naranj / Orange"</strong> = <em>Orange Color</em>!'
    ),
    672: (
        '<strong>Mango</strong> ≈ Borrowed directly via Portuguese traders from <strong>Tamil மாங்காய் (Maangaay!)</strong> = <em>Mango</em>!',
        '<strong>Aam</strong> ≈ Same Sanskrit root as <strong>Tamil ஆம்ரம் (Aamram = King of summer fruits!)</strong> = <em>Mango</em>!'
    ),
    673: (
        '<strong>Uva</strong> ≈ Root of anatomy\'s <strong>"Uvula"</strong> (hanging in back of throat like a tiny grape!) = <em>Grape</em>!',
        '<strong>Angoor</strong> ≈ Tight green/purple cluster hanging on a vineyard vine = <em>Grape</em>!'
    ),
    674: (
        '<strong>Limón</strong> ≈ Tart citrus squeezed over tacos and tea (same Persian-Arabic origin as <em>Lime/Lemon</em>!) = <em>Lemon</em>!',
        '<strong>Neembu</strong> ≈ Same root as <strong>Spoken Tamil நிம்பு / எலுமிச்சை (Nimbu = Zesty citrus!)</strong> = <em>Lemon</em>!'
    ),
    675: (
        '<strong>Sandía</strong> ≈ Refreshing red picnic melon eaten on a hot <strong>"Sun-Day"</strong>! = <em>Watermelon</em>!',
        '<strong>Tarbooz</strong> ≈ Striped green summer melon bursting with sweet pink juice = <em>Watermelon</em>!'
    ),
    676: (
        '<strong>Verdura</strong> (From <strong>Verde</strong> = Fresh garden greens!) | <strong>Vegetal</strong> (Plant produce) = <em>Vegetable</em>!',
        '<strong>Sabzi</strong> ≈ Fresh market greens (from Persian <em>Sabz</em> = Green!) and cooked curries = <em>Vegetable</em>!'
    ),
    677: (
        '<strong>Papa</strong> (In Latin America) | <strong>Patata</strong> (In Spain — blended with sweet potato <em>Batata</em>!) = <em>Potato</em>!',
        '<strong>Aalu</strong> ≈ Famous golden kitchen tuber in <strong>Aloo Gobi & Aloo Paratha</strong> = <em>Potato</em>!'
    ),
    678: (
        '<strong>Tomate</strong> (Spain) | <strong>Jitomate</strong> (Mexico) — from Nahuatl <strong>Xictomatl</strong> ("Plump red fruit"!) = <em>Tomato</em>!',
        '<strong>Tamatar</strong> ≈ Juicy red curry base borrowed from Portuguese <em>Tomate</em> = <em>Tomato</em>!'
    ),
    679: (
        '<strong>Cebolla</strong> ≈ Think <strong>"See-Boil-Ya"</strong> sizzling in a pan while making your eyes water = <em>Onion</em>!',
        '<strong>Pyaaz</strong> ≈ Papery purple rings sliced into every savory curry base = <em>Onion</em>!'
    ),
    681: (
        '<strong>Jengibre</strong> ≈ Same ancient <strong>Tamil இஞ்சிவேர் (Inji-ver)</strong> root traded along spice routes! = <em>Ginger</em>!',
        '<strong>Adrak</strong> ≈ Same root as <strong>Tamil ஆர்த்ரகம் (Aardhrakam = Spicy root!)</strong> = <em>Ginger</em>!'
    ),
    682: (
        '<strong>Zanahoria</strong> ≈ Crunchy bright-orange taproot from Arabic <em>Safunnariya</em> = <em>Carrot</em>!',
        '<strong>Gajar</strong> ≈ Sweet winter orange root famous in rich <strong>Gajar ka Halwa</strong> dessert = <em>Carrot</em>!'
    ),
    683: (
        '<strong>Chile</strong> (From Aztec Nahuatl <em>Chilli</em>) | <strong>Ají</strong> (South American spicy pod) = <em>Chili</em>!',
        '<strong>Mirch / hari mirch</strong> ≈ <strong>Hari</strong> (Green) fiery pod crackling in hot oil = <em>Chili</em>!'
    ),
    684: (
        '1. Beans: <strong>Frijoles</strong> (Refried pinto pods) | <strong>Alubias</strong> (White kidney pods) = <em>Beans</em>!<br>2. Peas: <strong>Guisantes</strong> (Sweet green) | <strong>Arvejas</strong> (Podded round seeds) = <em>Peas</em>!',
        '1. Beans: <strong>Rajma</strong> (Red kidney curry) | <strong>Faliyan</strong> (Green bean pods) = <em>Beans</em>!<br>2. Peas: <strong>Matar</strong> ≈ Sweet green pods famous in <strong>Matar Paneer</strong> = <em>Peas</em>!'
    ),
    685: (
        '<strong>Maíz</strong> (Carib word giving English <strong>"Maize"</strong>) | <strong>Choclo</strong> (Tender cob in Andes) = <em>Corn</em>!',
        '<strong>Makka</strong> (<strong>Tamil மக்காச்சோளம் = Makkaa-cholam!</strong>) | <strong>Bhutta</strong> (Charcoal-roasted street cob!) = <em>Corn</em>!'
    ),
    686: (
        '<strong>Pepino</strong> ≈ Crisp cool green salad stick full of refreshing <strong>"Pep"</strong> = <em>Cucumber</em>!',
        '<strong>Kheera</strong> ≈ Cool watery green slice eaten chilled with chaat masala in summer = <em>Cucumber</em>!'
    ),
    687: (
        '1. Spinach: <strong>Espinaca</strong> ≈ Iron-rich dark green leaf (Popeye\'s favorite) = <em>Spinach</em>!<br>2. Cabbage: <strong>Repollo</strong> (Tight round sprout) | <strong>Col</strong> (Root of <em>Cole-slaw</em>!) = <em>Cabbage</em>!',
        '1. Spinach: <strong>Paalak</strong> ≈ Identical to <strong>Tamil பாலக் கீரை (Paalak = Leafy green!)</strong> = <em>Spinach</em>!<br>2. Cabbage: <strong>Patta gobhi</strong> ≈ <strong>Patta</strong> (Leaf) + <strong>Gobhi</strong> (Round head) = <em>Cabbage</em>!'
    ),
    688: (
        '1. Seed/food: <strong>Fruto seco</strong> (Dry kernel) | <strong>Nuez</strong> (Hard-shell walnut) = <em>Nut</em>!<br>2. Hardware: <strong>Tuerca</strong> ≈ Sounds like <strong>"Torque-Nut"</strong> spinning onto a steel bolt = <em>Hardware Nut</em>!',
        '1. Seed/food: <strong>Mewa</strong> (Rich dried kernel) | <strong>Akhrot</strong> (<strong>Tamil அக்ரூட் = Walnut!</strong>) = <em>Nut</em>!<br>2. Hardware: <strong>Dhibri</strong> ≈ Threaded hexagonal metal fastener twisted onto a bolt = <em>Hardware Nut</em>!'
    ),
    689: (
        '<strong>Plato</strong> ≈ Flat ceramic dinnerware holding your food (origin of <strong>"Platter / Plate"</strong>) = <em>Plate</em>!',
        '<strong>Thali</strong> (Traditional round metal dining tray) | <strong>Plate</strong> (Ceramic dish) = <em>Plate</em>!'
    ),
    690: (
        '<strong>Tazón</strong> ≈ Oversized <strong>Taza</strong> (cup) deep enough to cradle steaming soup = <em>Bowl</em>!',
        '<strong>Katori</strong> (Small stainless curry dish) | <strong>Bowl</strong> (Deep serving dish) = <em>Bowl</em>!'
    ),
    691: (
        '<strong>Taza</strong> (Morning coffee mug) | <strong>Pocillo</strong> (Small espresso demi-cup) = <em>Cup / Mug</em>!',
        '<strong>Cup</strong> (Hand-held mug) | <strong>Pyala</strong> (Traditional clay or tea vessel) = <em>Cup / Mug</em>!'
    ),
    692: (
        '1. Drinking tumbler: <strong>Vaso</strong> ≈ Root of <strong>"Vessel / Vase"</strong> holding water = <em>Drinking Glass</em>!<br>2. Material: <strong>Vidrio</strong> (Root of <strong>"Vitreous"</strong>) | <strong>Cristal</strong> (Sparkling crystal) = <em>Glass Material</em>!',
        '1. Drinking tumbler: <strong>Gilaas</strong> ≈ Tall stainless or clear tumbler for lassi/water = <em>Glass</em>!<br>2. Material: <strong>Kaanch</strong> ≈ Transparent pane (same root as <strong>Tamil காசம்!</strong>) = <em>Glass Material</em>!'
    ),
    693: (
        '<strong>Botella</strong> ≈ Narrow-necked flask sealed with a cap (from Late Latin <em>Butticula</em>) = <em>Bottle</em>!',
        '<strong>Botal</strong> ≈ Borrowed into Hindi/Tamil (பாட்டில்) as a cylindrical water or soda container = <em>Bottle</em>!'
    ),
    694: (
        '<strong>Cuchara</strong> ≈ Rounded scoop built to lift hot soup and cereal to your mouth = <em>Spoon</em>!',
        '<strong>Chammach</strong> ≈ Metal eating scoop beside your fork and knife (Think <em>"Chomp-much with a scoop"</em>) = <em>Spoon</em>!'
    ),
    695: (
        '<strong>Tenedor</strong> ≈ From <strong>Tener</strong> (To hold) → Sharp prongs pinning food steady while you cut = <em>Fork</em>!',
        '<strong>Kaanta</strong> ≈ Literally "Thorn / Prong" — sharp tines stabbing fruit or noodles = <em>Fork</em>!'
    ),
    696: (
        '<strong>Cuchillo</strong> ≈ Sharp steel kitchen blade (think <strong>"Cut-Chill-Blade"</strong> slicing veggies) = <em>Knife</em>!',
        '<strong>Chaaku</strong> ≈ Sharp folding or kitchen blade (Think <strong>"Chop-Cut"</strong> cleanly!) = <em>Knife</em>!'
    ),
    698: (
        '<strong>Olla</strong> (Deep stew vessel, as in <em>Olla podrida</em>) | <strong>Cacerola</strong> (<strong>"Casserole"</strong> saucepan) = <em>Pot</em>!',
        '<strong>Patila</strong> (Deep round boiling vessel) | <strong>Bartan</strong> (Kitchen cooking container) = <em>Pot</em>!'
    ),
    699: (
        '<strong>Sartén</strong> ≈ Shallow frying skillet sizzling with olive oil (sounds like <strong>"Sauté-in"</strong>!) = <em>Pan</em>!',
        '<strong>Tawa</strong> (<strong>Tamil தவா = Flat iron griddle!</strong>) | <strong>Kadhai</strong> (Deep curved wok!) = <em>Pan</em>!'
    ),
    700: (
        '<strong>Refrigerador</strong> (Chilling appliance) | <strong>Nevera</strong> (From <strong>Nieve</strong> = Snow cold box!) = <em>Refrigerator</em>!',
        '<strong>Fridge</strong> ≈ Cold kitchen cabinet keeping milk, fruit & leftovers icy fresh = <em>Refrigerator</em>!'
    ),
    701: (
        '1. Cooktop/burner: <strong>Estufa</strong> (Heating burner) | <strong>Cocina</strong> (Cooking range) = <em>Stove</em>!<br>2. Baking chamber: <strong>Horno</strong> ≈ Root of <strong>"Furnace"</strong> baking hot bread = <em>Oven</em>!',
        '1. Cooktop/burner: <strong>Chulha</strong> ≈ Traditional clay or gas flame hearth = <em>Stove</em>!<br>2. Baking chamber: <strong>Tandoor</strong> (Clay pit baker) | <strong>Oven</strong> (Heated chamber) = <em>Oven</em>!'
    ),
    702: (
        '1. Basin: <strong>Fregadero</strong> (From <em>Fregar</em> = scrub) | <strong>Lavabo</strong> (<strong>"Lavatory"</strong> bowl) = <em>Sink</em>!<br>2. Faucet: <strong>Grifo</strong> (Griffin spout) | <strong>Llave</strong> (Turn-valve) = <em>Tap</em>!',
        '1. Basin: <strong>Sink</strong> | <strong>Haath dhone ki jagah</strong> (Spot to wash hands) = <em>Sink</em>!<br>2. Faucet: <strong>Nal</strong> (Pipe spout) | <strong>Toti</strong> (Curved tap nozzle) = <em>Tap</em>!'
    ),
    704: (
        '<strong>Cuarto</strong> (Living <strong>"Quarter"</strong>) | <strong>Habitación</strong> (<strong>"Habitation"</strong> space inside walls) = <em>Room</em>!',
        '<strong>Kamra</strong> ≈ Identical origin to Latin <strong>"Camera / Chamber"</strong> (enclosed living space!) = <em>Room</em>!'
    ),
    705: (
        '<strong>Dormitorio</strong> (Sleeping <strong>"Dormitory"</strong>) | <strong>Recámara</strong> (Private inner chamber) = <em>Bedroom</em>!',
        '<strong>Sone ka kamra</strong> (<strong>Sone ka</strong> = For sleeping + <strong>Kamra</strong> = Room) | <strong>Bedroom</strong> = <em>Bedroom</em>!'
    ),
    706: (
        '<strong>Baño</strong> ≈ Tiled shower & tub washroom (same root as English <strong>"Bath"</strong>) = <em>Bathroom</em>!',
        '<strong>Bathroom</strong> | <strong>Nahaane ki jagah</strong> (<strong>Nahaane</strong> = Bathing + <strong>Jagah</strong> = Place) = <em>Bathroom</em>!'
    ),
    707: (
        '<strong>Sala / salón</strong> ≈ Grand sitting lounge (same root as <strong>"Salon"</strong>) where guests gather = <em>Living Room</em>!',
        '<strong>Baithak</strong> (From <strong>Baithna</strong> = Sit down with guests!) | <strong>Living room</strong> = <em>Living Room</em>!'
    ),
    708: (
        '<strong>Cocina</strong> ≈ Twin root of French/English <strong>"Cuisine"</strong> where meals are cooked = <em>Kitchen</em>!',
        '<strong>Rasoi</strong> ≈ Fragrant heart of the home where curries simmer (from <strong>Ras</strong> = Taste/Essence!) = <em>Kitchen</em>!'
    ),
    709: (
        '1. Exterior top: <strong>Tejado</strong> (Tiled top) | <strong>Techo</strong> (Overhanging shelter) = <em>Roof</em>!<br>2. Interior ceiling: <strong>Techo</strong> (Upper room lid) | <strong>Cielo raso</strong> ("Smooth sky" overhead) = <em>Ceiling</em>!',
        '1. Exterior top: <strong>Chhat (upar ki)</strong> ≈ Open upper terrace overhead = <em>Roof</em>!<br>2. Interior ceiling: <strong>Chhat (andar ki)</strong> ≈ Inside ceiling above the fan = <em>Ceiling</em>!'
    ),
    710: (
        '<strong>Pared</strong> (Room partition) | <strong>Muro</strong> (Root of <strong>"Mural"</strong> painted on stone) = <em>Wall</em>!',
        '<strong>Deewaar</strong> ≈ Solid brick partition separating rooms (famous <em>"Deewaar mein chhed!"</em>) = <em>Wall</em>!'
    ),
    713: (
        '<strong>Ventana</strong> ≈ Root of <strong>"Vent / Ventilate"</strong> opening wide to let fresh breeze in = <em>Window</em>!',
        '<strong>Khidki</strong> ≈ Opening set in a wall with glass & shutters (Think <em>"Kid-peeking"</em> outside!) = <em>Window</em>!'
    ),
    714: (
        '<strong>Escaleras</strong> ≈ Root of <strong>"Escalator / Scale"</strong> climbing floor by floor = <em>Stairs</em>!',
        '<strong>Seedhiyan</strong> ≈ Plural of <strong>Seedhi</strong> (Straight climbing steps rising upward) = <em>Stairs</em>!'
    ),
    715: (
        '<strong>Balcón</strong> (Projecting railing ledge) | <strong>Terraza</strong> (Open-air rooftop <strong>"Terrace"</strong>) = <em>Balcony / Terrace</em>!',
        '<strong>Balcony</strong> (Front overhanging ledge) | <strong>Chhat</strong> (Open sunny rooftop) = <em>Balcony / Terrace</em>!'
    ),
    716: (
        '<strong>Jardín</strong> (Blooming flowerbed) | <strong>Patio</strong> (Open sun-lit courtyard) = <em>Garden / Yard</em>!',
        '<strong>Bageecha</strong> (Orchard/flower patch) | <strong>Garden</strong> (Green backyard lawn) = <em>Garden / Yard</em>!'
    ),
    717: (
        '1. Barrier fence: <strong>Cerca</strong> (Surrounding rail) | <strong>Valla</strong> (Wooden/wire picket) = <em>Fence</em>!<br>2. Access gate: <strong>Portón</strong> (Giant doorway) | <strong>Reja</strong> (Iron grille) = <em>Gate</em>!',
        '1. Barrier fence: <strong>Deewaar / boundary</strong> (Outer perimeter wall enclosing a plot) = <em>Fence</em>!<br>2. Access gate: <strong>Gate</strong> (Main drive) | <strong>Phatak</strong> (Heavy clanging entry barrier) = <em>Gate</em>!'
    ),
    719: (
        '<strong>Silla</strong> ≈ Sounds like <strong>"Sit-Ya"</strong> down comfortably on a wooden seat = <em>Chair</em>!',
        '<strong>Kursi</strong> ≈ Four-legged seat around the dining table or office desk (Think <em>"Court seat"</em>) = <em>Chair</em>!'
    ),
    720: (
        '<strong>Sofá</strong> (Cushioned lounge bench) | <strong>Sillón</strong> (Big armchair) = <em>Sofa / Couch</em>!',
        '<strong>Sofa</strong> ≈ Wide plush three-seater couch in the living room = <em>Sofa / Couch</em>!'
    ),
    721: (
        '<strong>Cama</strong> ≈ Sounds like <strong>"Calm-Ah"</strong> stretching out softly at bedtime = <em>Bed</em>!',
        '<strong>Bistar</strong> (Soft bedding) | <strong>Palang</strong> (Carved wooden cot frame) = <em>Bed</em>!'
    ),
    722: (
        '<strong>Colchón</strong> ≈ Think <strong>"Cushion-on-bed"</strong> filled with soft springs & foam = <em>Mattress</em>!',
        '<strong>Gadda</strong> ≈ Thick quilted cushion pad laid across the bed frame (Think <em>"Good-soft pad"</em>) = <em>Mattress</em>!'
    ),
    724: (
        '<strong>Cobija</strong> (Cozy cover) | <strong>Manta</strong> (Root of <strong>"Mantle"</strong> shawl wrap) = <em>Blanket</em>!',
        '<strong>Kambal</strong> ≈ Identical to <strong>Tamil கம்பளி (Kambali = Warm wool wrap!)</strong> = <em>Blanket</em>!'
    ),
    725: (
        '1. Bed cover: <strong>Sábana</strong> (Crisp white <strong>"Savanna"</strong> cotton spread) = <em>Bedsheet</em>!<br>2. Paper piece: <strong>Hoja (de papel)</strong> (Leaf of paper) = <em>Paper Sheet</em>!',
        '1. Bed cover: <strong>Chaadar</strong> ≈ Smooth woven cloth spread over the mattress = <em>Bedsheet</em>!<br>2. Paper piece: <strong>Panna</strong> ≈ Single book leaf (same root as <strong>"Panel / Page"</strong>) = <em>Sheet</em>!'
    ),
    726: (
        '<strong>Cortina</strong> ≈ Draped window cloth pulled shut at sunset (same root as <strong>"Curtain"</strong>) = <em>Curtain</em>!',
        '<strong>Parda</strong> ≈ Identical to <strong>Tamil பர்தா (Pardha = Hanging privacy drape!)</strong> = <em>Curtain</em>!'
    ),
    727: (
        '<strong>Alfombra</strong> (Woven floor rug) | <strong>Tapete</strong> (Root of <strong>"Tapestry"</strong> mat) = <em>Carpet / Rug</em>!',
        '<strong>Kaaleen</strong> ≈ Hand-knotted wool floor mat (famous Persian/Kashmiri <em>Kaleen</em>) = <em>Carpet / Rug</em>!'
    ),
    728: (
        '<strong>Espejo</strong> ≈ Root of <strong>"Speculum / Speculate"</strong> reflecting your face clearly = <em>Mirror</em>!',
        '<strong>Aayina</strong> (Looking-glass frame) | <strong>Sheesha</strong> (Silvered reflecting pane) = <em>Mirror</em>!'
    ),
    729: (
        '<strong>Armario</strong> (French/English <strong>"Armoire"</strong>) | <strong>Ropero</strong> (Cabinet for <em>Ropa</em> clothes) = <em>Closet / Wardrobe</em>!',
        '<strong>Almaari</strong> ≈ Identical to <strong>Tamil அலமாரி (Alamaari = Storage cupboard!)</strong> = <em>Closet / Wardrobe</em>!'
    ),
    730: (
        '1. Ledge: <strong>Estante</strong> (Where books <strong>"Stand"</strong>) | <strong>Repisa</strong> (Wall ledge) = <em>Shelf</em>!<br>2. Storage box: <strong>Gabinete</strong> (Locker) | <strong>Alacena</strong> (Pantry cupboard) = <em>Cabinet</em>!',
        '1. Ledge: <strong>Shelf</strong> (Horizontal display plank) | <strong>Almaari</strong> (Open rack) = <em>Shelf</em>!<br>2. Storage box: <strong>Almaari</strong> ≈ <strong>Tamil அலமாரி (Alamaari = Enclosed cupboard!)</strong> = <em>Cabinet</em>!'
    ),
    731: (
        '<strong>Escritorio</strong> ≈ From <strong>Escribir</strong> (Write) → Study table for books and laptop = <em>Desk</em>!',
        '<strong>Table / desk</strong> ≈ Flat study or office workstation with drawers underneath = <em>Desk</em>!'
    ),
    732: (
        '1. Fixture: <strong>Lámpara</strong> (Bedside light stand) = <em>Lamp</em>!<br>2. Glass bulb: <strong>Bombilla</strong> (Little glowing glass drop) | <strong>Foco</strong> (<strong>"Focus"</strong> spotlight) = <em>Bulb</em>!',
        '1. Fixture: <strong>Batti</strong> (Glowing fixture) | <strong>Diya</strong> (Traditional earthen oil lamp!) = <em>Lamp</em>!<br>2. Glass bulb: <strong>Bulb</strong> (Screwed-in glowing glass) = <em>Bulb</em>!'
    ),
    733: (
        '1. Electrical device: <strong>Interruptor</strong> (Breaks circuit) | <strong>Apagador</strong> (Turns off) = <em>Switch</em>!<br>2. Verb - change/swap: <strong>Cambiar</strong> | <strong>Intercambiar</strong> (Swap places) = <em>Switch</em>!',
        '1. Electrical device: <strong>Switch / button</strong> (Wall toggle flicking lights on/off) = <em>Switch</em>!<br>2. Verb - change/swap: <strong>Badalna</strong> ≈ Trade or shift from one thing to another = <em>Switch</em>!'
    ),
    734: (
        '1. Male prong: <strong>Enchufe</strong> (Two-pin connector) | <strong>Clavija</strong> (Key-peg prong) = <em>Plug</em>!<br>2. Wall outlet: <strong>Tomacorriente</strong> (<strong>Toma</strong> Take + <strong>Corriente</strong> Current) = <em>Socket</em>!',
        '1. Male prong: <strong>Plug</strong> (Pronged cord tip) = <em>Plug</em>!<br>2. Wall outlet: <strong>Socket / board</strong> (Multi-hole power strip in the wall) = <em>Socket</em>!'
    ),
    735: (
        '<strong>Cable</strong> (Insulated cord) | <strong>Alambre</strong> (Thin copper/steel strand) = <em>Wire</em>!',
        '<strong>Taar</strong> (Stretched metal line — also means "Telegram"!) | <strong>Wire</strong> = <em>Wire</em>!'
    ),
    736: (
        '<strong>Reloj (de pared)</strong> ≈ Tick-tock timepiece hanging on the living room wall (origin of <em>Horology</em>) = <em>Clock</em>!',
        '<strong>Deewaar ghadi</strong> ≈ <strong>Deewaar</strong> (Wall) + <strong>Ghadi</strong> (<strong>Tamil கடிகாரம் = Timepiece!</strong>) = <em>Clock</em>!'
    ),
    737: (
        '<strong>Campana</strong> (Church bell — root of <strong>"Campanile"</strong>) | <strong>Timbre</strong> (Door buzzer) = <em>Bell</em>!',
        '<strong>Ghanti</strong> ≈ Same root as <strong>Tamil கண்டை (Ghanta = Ringing temple bell!)</strong> = <em>Bell</em>!'
    ),
    738: (
        '1. Door lock tool: <strong>Llave</strong> (Pronounced <em>Yah-veh</em> → Metal turn-key!) = <em>Key</em>!<br>2. Crucial factor: <strong>Clave</strong> (Root of <strong>"Clef"</strong>) | <strong>Fundamental</strong> (Essential) = <em>Key</em>!',
        '1. Door lock tool: <strong>Chaabi</strong> ≈ Identical to <strong>Spoken Tamil சாவி (Chaavi = Key!)</strong> = <em>Key</em>!<br>2. Crucial factor: <strong>Mukhya</strong> ≈ <strong>Tamil முக்கியம் (Mukkiyam = Essential!)</strong> = <em>Key</em>!'
    ),
    739: (
        '<strong>Candado</strong> (Hanging metal padlock) | <strong>Cerradura</strong> (Built-in door bolt from <em>Cerrar</em>) = <em>Lock / Padlock</em>!',
        '<strong>Taala</strong> (<strong>Spoken Tamil தாளம் = Padlock!</strong>) | <strong>Lock</strong> (Key-fastened latch) = <em>Lock / Padlock</em>!'
    ),
    740: (
        '1. Sweeping brush: <strong>Escoba</strong> ≈ Sounds like <strong>"Scoop-up"</strong> dust bunnies off the floor = <em>Broom</em>!<br>2. Wet wipe tool: <strong>Trapeador</strong> (Rag-swab) | <strong>Fregona</strong> (Scrubbing handle) = <em>Mop</em>!',
        '1. Sweeping brush: <strong>Jhaadu</strong> ≈ Bundled palm-bristle sweeper clearing dust every morning = <em>Broom</em>!<br>2. Wet wipe tool: <strong>Pocha</strong> ≈ Wet floor-wiping rag (Think <em>"Polish-clean"</em> tiles!) = <em>Mop</em>!'
    ),
    741: (
        '<strong>Cubo</strong> (Round or square haul pail) | <strong>Balde</strong> (Plastic carry tub — sounds like <em>Balti</em>!) = <em>Bucket</em>!',
        '<strong>Balti</strong> ≈ Identical to <strong>Spoken Tamil வாளி / பால்டி (Baalti = Bathwater pail!)</strong> = <em>Bucket</em>!'
    ),
    742: (
        '1. Waste matter: <strong>Basura</strong> ≈ Discarded scraps tossed away (sounds like <em>"Mess-ura"</em>) = <em>Trash</em>!<br>2. Receptacle: <strong>Basurero</strong> (Trash holder) | <strong>Cubo</strong> (Bin pail) = <em>Trash Bin</em>!',
        '1. Waste matter: <strong>Kachra</strong> (<strong>Spoken Tamil கச்சடா = Rubbish!</strong>) | <strong>Kooda</strong> (Sweepings) = <em>Trash</em>!<br>2. Receptacle: <strong>Koodadan</strong> ≈ <strong>Kooda</strong> (Waste) + <strong>-dan</strong> (Container) = <em>Trash Bin</em>!'
    ),
    743: (
        '<strong>Jabón</strong> ≈ Foamy cleansing bar from Latin <em>Sapo</em> (Think <strong>"Have-On-Hands"</strong> bubbles!) = <em>Soap</em>!',
        '<strong>Saabun</strong> ≈ Identical to <strong>Spoken Tamil சாபூன் (Saabun = Foamy wash bar!)</strong> = <em>Soap</em>!'
    ),
    744: (
        '<strong>Toalla</strong> ≈ Fluffy drying cloth hung beside the shower (same Germanic origin as <em>Towel</em>) = <em>Towel</em>!',
        '<strong>Tauliya</strong> ≈ Phonetic twin of <strong>"Towel"</strong> wrapped after a bath = <em>Towel</em>!'
    ),
    745: (
        '1. Brush: <strong>Cepillo de dientes</strong> ≈ Bristled scrub for teeth (<em>Dientes = Dental</em>) = <em>Toothbrush</em>!<br>2. Paste: <strong>Pasta de dientes</strong> ≈ Minty paste squeezed onto bristles = <em>Toothpaste</em>!',
        '1. Brush: <strong>Toothbrush</strong> ≈ Morning bristle stick for scrubbing teeth = <em>Toothbrush</em>!<br>2. Paste: <strong>Toothpaste</strong> ≈ Minty tube squeezed before brushing = <em>Toothpaste</em>!'
    ),
    746: (
        '<strong>Tijeras</strong> ≈ Twin crossed blades that <strong>"Tear & Shear"</strong> paper or cloth cleanly = <em>Scissors</em>!',
        '<strong>Kainchi</strong> ≈ Identical to <strong>Spoken Tamil கத்திரி / கைஞ்சி (Kainchi = Snipping blades!)</strong> = <em>Scissors</em>!'
    ),
    747: (
        '<strong>Martillo</strong> ≈ Heavy iron pounding head (nickname of warrior Charles <strong>"Martel — The Hammer"</strong>) = <em>Hammer</em>!',
        '<strong>Hathoda</strong> ≈ From <strong>Haath</strong> (Hand) → Heavy-headed hand tool slamming nails straight in = <em>Hammer</em>!'
    ),
    748: (
        '1. Threaded spike: <strong>Tornillo</strong> (From <em>Tornar</em> = Turn/Twist) = <em>Screw</em>!<br>2. Driver tool: <strong>Destornillador</strong> (Tool that twists screws in & out) = <em>Screwdriver</em>!',
        '1. Threaded spike: <strong>Pech / screw</strong> (Spiral-grooved metal pin) = <em>Screw</em>!<br>2. Driver tool: <strong>Pechkas</strong> ≈ <strong>Pech</strong> (Screw) + <strong>Kas</strong> (Tightener) = <em>Screwdriver</em>!'
    ),
    749: (
        '<strong>Cuerda</strong> (<strong>"Cord"</strong>) | <strong>Soga</strong> (Thick hemp knot) | <strong>Hilo</strong> (Thin sewing <strong>"Filament"</strong>) = <em>Rope / String</em>!',
        '<strong>Rassi</strong> (Thick braided tug-of-war line) | <strong>Dhaaga</strong> (Fine cotton sewing thread) = <em>Rope / String</em>!'
    ),
    750: (
        '<strong>Ropa</strong> (Garment rack — think <strong>"Robes"</strong>) | <strong>Prendas</strong> (Individual wearable items) = <em>Clothes / Clothing</em>!',
        '<strong>Kapde</strong> ≈ Same root as <strong>Tamil கப்படம் (Kappadam ≈ Kapde = Woven fabric!)</strong> = <em>Clothes / Clothing</em>!'
    ),
    751: (
        '<strong>Camisa</strong> (Button-down collar, root of <strong>"Camisole"</strong>) | <strong>Playera</strong> (Casual beach tee) = <em>Shirt</em>!',
        '<strong>Kameez</strong> (<strong>Spoken Tamil கமீஸ் = Tunic!</strong>) | <strong>Shirt</strong> (Buttoned top) = <em>Shirt</em>!'
    ),
    752: (
        '<strong>Pantalones</strong> ≈ Two-legged lower trousers (origin of English <strong>"Pantaloons / Pants"</strong>) = <em>Pants</em>!',
        '<strong>Pant</strong> (Tailored trousers) | <strong>Patloon</strong> (Classic Indian adaptation of <em>Pantaloons</em>!) = <em>Pants</em>!'
    ),
    753: (
        '<strong>Jeans</strong> (Blue denim) | <strong>Vaqueros</strong> (From <strong>Vaca = Cow</strong> → Tough <em>Cowboy</em> denim!) = <em>Jeans</em>!',
        '<strong>Jeans</strong> ≈ Tough indigo riveted denim trousers worn casually everywhere = <em>Jeans</em>!'
    ),
    754: (
        '<strong>Pantalones cortos</strong> (Literally "Short pants") | <strong>Bermudas</strong> (Knee-length island trunks) = <em>Shorts</em>!',
        '<strong>Shorts</strong> (Half-length) | <strong>Nikkar</strong> (From British <em>"Knickers / Knickerbockers"</em> school half-pants!) = <em>Shorts</em>!'
    ),
    755: (
        '1. One-piece garment: <strong>Vestido</strong> (Root of <strong>"Vestment / Invest"</strong> = Full gown) = <em>Dress</em>!<br>2. Lower garment: <strong>Falda</strong> (Draped cloth folding from waist down) = <em>Skirt</em>!',
        '1. One-piece garment: <strong>Frock</strong> (Flared gown) | <strong>Dress</strong> (Full outfit) = <em>Dress</em>!<br>2. Lower garment: <strong>Ghagra</strong> (Swirling traditional flare) | <strong>Skirt</strong> (Waist-down hem) = <em>Skirt</em>!'
    ),
    756: (
        '1. Formal outfit: <strong>Traje</strong> (Matching tailored jacket & trousers) = <em>Suit</em>!<br>2. Verb - fit/match: <strong>Quedar bien</strong> (Fits nicely) | <strong>Convenir</strong> (Works well) = <em>Suit / Match</em>!',
        '1. Formal outfit: <strong>Suit / coat-pant</strong> (Two-piece business tailoring) = <em>Suit</em>!<br>2. Verb - fit/match: <strong>Jachna</strong> (Looks flattering!) | <strong>Theek baithna</strong> (Fits just right) = <em>Suit</em>!'
    ),
    757: (
        '<strong>Chaqueta</strong> (Waist-length outer zip layer) | <strong>Abrigo</strong> (Long winter overcoat sheltering from wind) = <em>Jacket / Coat</em>!',
        '<strong>Jacket</strong> (Light zippered outer layer) | <strong>Coat</strong> (Tailored or wool winter overcoat) = <em>Jacket / Coat</em>!'
    ),
    758: (
        '<strong>Suéter</strong> (Knitted winter pullover) | <strong>Jersey</strong> (Soft wool knit named after Jersey island!) = <em>Sweater</em>!',
        '<strong>Sweater</strong> ≈ Warm knitted wool pullover layered over a shirt in winter = <em>Sweater</em>!'
    ),
    759: (
        '<strong>Uniforme</strong> ≈ Prefix <strong>Uni-</strong> (One) + <strong>Forma</strong> (Shape) → Matching team or school dress = <em>Uniform</em>!',
        '<strong>Vardi</strong> (Police/army official dress) | <strong>Uniform</strong> (Matching school outfit) = <em>Uniform</em>!'
    ),
    760: (
        '<strong>Ropa interior</strong> ≈ <strong>Ropa</strong> (Garments) + <strong>Interior</strong> (Worn underneath close to skin) = <em>Underwear</em>!',
        '<strong>Kachha</strong> (Traditional drawstring cotton brief — from <em>Kachh</em> = hip/loin!) | <strong>Underwear</strong> (Base layer) = <em>Underwear</em>!'
    ),
    761: (
        '<strong>Calcetín</strong> (Ankle knit) | <strong>Media</strong> (Knee-high stocking worn inside shoes) = <em>Sock</em>!',
        '<strong>Moja</strong> (Knitted foot warmer) | <strong>Jurab</strong> (Classic pair pulled on before shoes) = <em>Sock</em>!'
    ),
    762: (
        '<strong>Zapato</strong> ≈ Step-stomping leather footwear (think <strong>"Tap-at-toe"</strong> dancing <em>Zapateado</em>!) = <em>Shoe</em>!',
        '<strong>Joota</strong> ≈ Everyday laced or slip-on footwear (famous song <em>"Mera Joota Hai Japani"</em>!) = <em>Shoe</em>!'
    ),
    763: (
        '<strong>Bota</strong> ≈ Sturdy ankle- or knee-high leather footwear built for hiking & rain = <em>Boot</em>!',
        '<strong>Boot</strong> (Tall rugged footwear) | <strong>Bada joota</strong> (Literally "Tall big shoe" covering the ankle!) = <em>Boot</em>!'
    ),
    764: (
        '<strong>Sandalia</strong> (Strapped open shoe) | <strong>Chancla</strong> (Slap-slap rubber flip-flop) = <em>Sandal / Slipper</em>!',
        '<strong>Chappal</strong> (<strong>Spoken Tamil சப்பல் = Open flip-flop!</strong>) | <strong>Sandal</strong> (Strapped flat) = <em>Sandal / Slipper</em>!'
    ),
    765: (
        '<strong>Sombrero</strong> (From <strong>Sombra</strong> = Shade!) | <strong>Gorra</strong> (Peaked sports cap) = <em>Hat / Cap</em>!',
        '<strong>Topi</strong> ≈ Identical to <strong>Tamil தொப்பி (Thoppi = Headgear!)</strong> | <strong>Cap</strong> (Brimmed lid) = <em>Hat / Cap</em>!'
    ),
    766: (
        '<strong>Cinturón</strong> (From <strong>Cintura</strong> = Waist!) | <strong>Cinto</strong> (Buckled leather strap) = <em>Belt</em>!',
        '<strong>Belt</strong> ≈ Buckled leather strap threaded through trouser loops at the waist = <em>Belt</em>!'
    ),
    767: (
        '<strong>Bufanda</strong> (Warm winter wool neck wrap) | <strong>Pañuelo</strong> (Silky square neckerchief) = <em>Scarf</em>!',
        '<strong>Dupatta</strong> (Long flowing shoulder drape) | <strong>Scarf</strong> (Warm winter neck wrap) = <em>Scarf</em>!'
    ),
    768: (
        '<strong>Guante</strong> ≈ Origin of English <strong>"Gauntlet"</strong> (five-fingered hand armor/mitt) = <em>Glove</em>!',
        '<strong>Dastana</strong> (From Persian <em>Dast</em> = Hand!) | <strong>Gloves</strong> (Winter finger covers) = <em>Glove</em>!'
    ),
    769: (
        '<strong>Bolsillo</strong> (Little <em>Bolsa</em> pouch sewn into trousers) | <strong>Bolsa</strong> (Coat pouch) = <em>Pocket</em>!',
        '<strong>Jeb</strong> ≈ Identical to <strong>Spoken Tamil ஜேப் (Jeb = Trouser pocket!)</strong> | <strong>Pocket</strong> (Side coin pouch) = <em>Pocket</em>!'
    ),
    770: (
        '1. Clothing fastener: <strong>Botón</strong> (Round disk threaded through a shirt slit) = <em>Button</em>!<br>2. Push device: <strong>Botón</strong> | <strong>Pulsador</strong> (Press-trigger switch) = <em>Push Button</em>!',
        '1. Clothing fastener: <strong>Button (kapde ka)</strong> (Clothes button) = <em>Button</em>!<br>2. Push device: <strong>Button</strong> (Elevator/doorbell press switch) = <em>Button</em>!'
    ),
    771: (
        '<strong>Cremallera</strong> (Interlocking teeth track) | <strong>Cierre</strong> (From <em>Cerrar</em> = Close fast!) = <em>Zipper</em>!',
        '<strong>Zip</strong> (Quick sliding track) | <strong>Chain</strong> (Interlocking metallic teeth track on bags/jeans) = <em>Zipper</em>!'
    ),
    772: (
        '<strong>Bolsa</strong> (Shopping carrier, root of <strong>"Bourse"</strong>) | <strong>Saco</strong> (Burlap grain <strong>"Sack"</strong>) = <em>Bag</em>!',
        '<strong>Thela</strong> (Cloth market tote) | <strong>Bag</strong> (Carried tote or satchel) = <em>Bag</em>!'
    ),
    773: (
        '1. Wallet for cash/cards: <strong>Billetera</strong> (Holds <em>Billetes</em> bills) | <strong>Cartera</strong> (Folding ID card holder) = <em>Wallet</em>!<br>2. Handbag: <strong>Bolso / cartera de mano</strong> (Shoulder/hand bag) = <em>Purse / Handbag</em>!',
        '1. Wallet for cash/cards: <strong>Batua</strong> (Traditional coin & cash pouch) | <strong>Wallet</strong> (Slim card fold) = <em>Wallet</em>!<br>2. Handbag: <strong>Purse</strong> (Carried clutch/handbag) = <em>Purse</em>!'
    ),
    774: (
        '<strong>Mochila</strong> ≈ Twin-strapped hiking & school pack slung over both shoulders (Think <em>"Much-gear-pack"</em>) = <em>Backpack</em>!',
        '<strong>Bag / backpack</strong> ≈ Twin-strapped canvas pack carried upright behind your shoulders = <em>Backpack</em>!'
    ),
    775: (
        '<strong>Maleta</strong> (Rolling travel trunk) | <strong>Valija</strong> (Root of <strong>"Valise"</strong> luggage) = <em>Suitcase</em>!',
        '<strong>Suitcase</strong> (Wheeled trip case) | <strong>Peti / baksa</strong> (Sturdy latched travel box) = <em>Suitcase</em>!'
    ),
    776: (
        '<strong>Paraguas</strong> (<strong>Para</strong> Stops + <strong>Aguas</strong> Waters!) | <strong>Sombrilla</strong> (<strong>Sombra</strong> = Sun shade!) = <em>Umbrella</em>!',
        '<strong>Chhaata</strong> ≈ Same Sanskrit root as <strong>Tamil சத்திரம் / குடை (Chhatra = Canopy shielding rain & sun!)</strong> = <em>Umbrella</em>!'
    ),
    777: (
        '<strong>Lentes</strong> (Optical <strong>"Lenses"</strong>) | <strong>Gafas</strong> (Ear-hooked spectacle frames) = <em>Glasses / Sunglasses</em>!',
        '<strong>Chashma</strong> (Reading spectacles) | <strong>Dhoop ka chashma</strong> (<strong>Dhoop</strong> = Sunlight → Shades!) = <em>Glasses / Sunglasses</em>!'
    ),
    778: (
        '1. Finger jewelry: <strong>Anillo</strong> ≈ Root of <strong>"Annular"</strong> (Circular gold band) = <em>Ring</em>!<br>2. Sound chime/call: <strong>Timbrar</strong> (Doorbell) | <strong>Sonar</strong> (<strong>"Sonic"</strong> chime) = <em>Ring</em>!',
        '1. Finger jewelry: <strong>Angoothi</strong> (From <strong>Angootha/Ungli</strong> = Finger!) = <em>Ring</em>!<br>2. Sound chime/call: <strong>Ghanti bajna</strong> (Bell chime) | <strong>Phone aana</strong> (Phone ringing) = <em>Ring</em>!'
    ),
    779: (
        '1. Neck chain: <strong>Collar</strong> (Neckband) | <strong>Cadena</strong> (Linked gold <strong>"Chain"</strong>) = <em>Necklace</em>!<br>2. General ornaments: <strong>Joyas / joyería</strong> (Sparkling <strong>"Jewels"</strong>) = <em>Jewelry</em>!',
        '1. Neck chain: <strong>Haar</strong> (<strong>Tamil ஹாரம் = Garland!</strong>) | <strong>Chain</strong> (Gold link) = <em>Necklace</em>!<br>2. General ornaments: <strong>Gehne / zewar</strong> (Bridal gold & diamond treasures) = <em>Jewelry</em>!'
    ),
    780: (
        '<strong>Transporte</strong> (Transit network) | <strong>Vehículo</strong> (Motorized <strong>"Vehicle"</strong>) = <em>Transport / Vehicle</em>!',
        '<strong>Gaadi</strong> (<strong>Spoken Tamil காடி!</strong>) | <strong>Vaahan</strong> (<strong>Tamil வாகனம்!</strong>) | <strong>Transport</strong> = <em>Transport / Vehicle</em>!'
    ),
    781: (
        '<strong>Coche</strong> (Horse <strong>"Coach"</strong>) | <strong>Carro</strong> (Chariot/car) | <strong>Auto</strong> (<strong>"Automobile"</strong>) = <em>Car</em>!',
        '<strong>Car</strong> (Four-wheeler) | <strong>Gaadi</strong> ≈ <strong>Spoken Tamil காடி (Gaadi = Everyday vehicle!)</strong> = <em>Car</em>!'
    ),
    782: (
        '<strong>Bicicleta / bici</strong> ≈ <strong>Bi-</strong> (Two) + <strong>Ciclo</strong> (Wheels) pedaled down the lane = <em>Bicycle / Bike</em>!',
        '<strong>Cycle</strong> ≈ Two-wheeled pedal-powered commuter bike seen on every street = <em>Bicycle / Bike</em>!'
    ),
    783: (
        '<strong>Moto / motocicleta</strong> ≈ <strong>Motor</strong> + <strong>Bicicleta</strong> → Fast two-wheeled engine ride = <em>Motorcycle / Scooter</em>!',
        '<strong>Bike / scooter / motorcycle</strong> ≈ Two-wheeled motorized city commute weaving through traffic = <em>Motorcycle / Scooter</em>!'
    ),
    784: (
        '<strong>Autobús / bus</strong> ≈ Short from <em>Omnibus</em> ("For all!") carrying city commuters together = <em>Bus</em>!',
        '<strong>Bus</strong> ≈ Long multi-seat city or highway transit coach stopping at shelters = <em>Bus</em>!'
    ),
    785: (
        '1. Rail vehicle: <strong>Tren</strong> ≈ Connected steel carriages gliding along tracks = <em>Train</em>!<br>2. Verb - coach/practice: <strong>Entrenar</strong> (Athletic coach) | <strong>Capacitar</strong> (Skill building) = <em>To Train</em>!',
        '1. Rail vehicle: <strong>Railgaadi / train</strong> (<strong>Rail</strong> track + <strong>Gaadi</strong> vehicle) = <em>Train</em>!<br>2. Verb - coach/practice: <strong>Sikhana</strong> (Teach skill) | <strong>Sikhna</strong> (Practice/learn) = <em>Train</em>!'
    ),
    786: (
        '<strong>Camión</strong> ≈ Heavy cargo hauler (Think <strong>"Carry-on-a-ton"</strong> down the highway!) = <em>Truck</em>!',
        '<strong>Truck</strong> ≈ Big multi-axle cargo lorry hauling goods across state highways = <em>Truck</em>!'
    ),
    787: (
        '<strong>Taxi</strong> ≈ Metered city ride named after <em>Taxameter</em> (tariff clock!) = <em>Taxi</em>!',
        '<strong>Taxi / cab</strong> ≈ Hailed yellow-or-black metered car picking up passengers curb-side = <em>Taxi</em>!'
    ),
    788: (
        '<strong>Avión</strong> ≈ Root of <strong>"Aviation / Aviator"</strong> soaring above clouds on wings = <em>Airplane</em>!',
        '<strong>Hawai jahaaz</strong> (<strong>Hawai</strong> Air + <strong>Jahaaz</strong> Ship!) | <strong>Plane</strong> = <em>Airplane</em>!'
    ),
    789: (
        '<strong>Barco</strong> (Large seafaring vessel, like <em>Barge</em>) | <strong>Bote</strong> (Small wooden rowboat) = <em>Boat / Ship</em>!',
        '<strong>Naav</strong> (<strong>Tamil நாவாய் = Boat & Navy!</strong>) | <strong>Paani ka jahaaz</strong> ("Water-ship") = <em>Boat / Ship</em>!'
    ),
    790: (
        '<strong>Motor</strong> ≈ Roaring mechanical powerhouse under the hood turning fuel into motion = <em>Engine</em>!',
        '<strong>Engine / motor</strong> ≈ Mechanical heart under a car hood powering pistons and wheels = <em>Engine</em>!'
    ),
    791: (
        '<strong>Rueda</strong> ≈ Root of <strong>"Rotate / Roll"</strong> turning smoothly along the road = <em>Wheel</em>!',
        '<strong>Pahiya</strong> ≈ Round spoked circle spinning on an axle (Think <em>"Path-roller"</em>) = <em>Wheel</em>!'
    ),
    792: (
        '1. Rubber wheel cover: <strong>Llanta</strong> (Treaded rim ring) | <strong>Neumático</strong> (Air-filled <strong>"Pneumatic"</strong>) = <em>Tire</em>!<br>2. Verb - fatigue: <strong>Cansar</strong> (Exhaust) | <strong>Fatigarse</strong> (<strong>"Fatigue"</strong>) = <em>To Tire</em>!',
        '1. Rubber wheel cover: <strong>Tyre</strong> (Black rubber tread around the wheel rim) = <em>Tire</em>!<br>2. Verb - fatigue: <strong>Thakna</strong> (Grow exhausted) | <strong>Thakana</strong> (Wear out) = <em>To Tire</em>!'
    ),
    793: (
        '<strong>Freno</strong> ≈ Root of <strong>"Refrain"</strong> (hold back!) → Clamping wheels to halt the car = <em>Brake</em>!',
        '<strong>Brake</strong> ≈ Pedal squeezed to slow down and bring a speeding vehicle to a stop = <em>Brake</em>!'
    ),
    794: (
        '<strong>Asiento</strong> ≈ From <strong>Sentarse</strong> (To sit) → Cushioned spot for passengers = <em>Seat</em>!',
        '<strong>Seat</strong> | <strong>Baithne ki jagah</strong> (<strong>Baithne</strong> = Sitting + <strong>Jagah</strong> = Spot) = <em>Seat</em>!'
    ),
    795: (
        '<strong>Cinturón de seguridad</strong> ≈ <strong>Cinturón</strong> (Belt) + <strong>de Seguridad</strong> (of Safety) = <em>Seatbelt</em>!',
        '<strong>Seatbelt</strong> ≈ Buckled chest-and-lap strap clicked tight before driving = <em>Seatbelt</em>!'
    ),
    796: (
        '<strong>Combustible</strong> (Burnable energy) | <strong>Gasolina</strong> (Pump liquid) = <em>Fuel / Petrol</em>!',
        '<strong>Petrol / diesel</strong> ≈ Liquid pumped from gas-station nozzles into fuel tanks = <em>Fuel / Petrol</em>!'
    ),
    797: (
        '<strong>Tráfico</strong> (Bumper-to-bumper cars) | <strong>Tránsito</strong> (Moving road <strong>"Transit"</strong>) = <em>Traffic</em>!',
        '<strong>Traffic / jaam</strong> ≈ Endless honking lines of cars crawling at rush hour ("Traffic jam!") = <em>Traffic</em>!'
    ),
    798: (
        '<strong>Calle</strong> (Neighborhood paved lane — sounds like <em>"Alley"</em>) | <strong>Camino</strong> (Travel road) = <em>Street / Road</em>!',
        '<strong>Sadak</strong> (<strong>Spoken Tamil சடக் / சாலை!</strong>) | <strong>Raasta</strong> (Way/path) = <em>Street / Road</em>!'
    ),
    799: (
        '<strong>Autopista</strong> (<strong>Auto</strong> Car + <strong>Pista</strong> Track) | <strong>Carretera</strong> (Main trunk route) = <em>Highway</em>!',
        '<strong>Highway</strong> | <strong>Badi sadak</strong> (<strong>Badi</strong> Big + <strong>Sadak</strong> Road) = <em>Highway</em>!'
    ),
    800: (
        '1. Footpath: <strong>Sendero</strong> (Hiking trail) | <strong>Camino</strong> (Dirt track) = <em>Path</em>!<br>2. Paved walkway: <strong>Acera</strong> ("Edge side") | <strong>Banqueta</strong> (Raised bench curb) = <em>Sidewalk</em>!',
        '1. Footpath: <strong>Pagdandi</strong> (<strong>Pag</strong> Foot + <strong>Dandi</strong> Strip) | <strong>Raasta</strong> (Track) = <em>Path</em>!<br>2. Paved walkway: <strong>Footpath</strong> | <strong>Patri</strong> (Curb walkway strip) = <em>Sidewalk</em>!'
    ),
    801: (
        '<strong>Puente</strong> ≈ Root of English <strong>"Pontoon"</strong> archway spanning wide rivers = <em>Bridge</em>!',
        '<strong>Pul</strong> (Stone/iron span across rivers — think <strong>"Pull across the gap!"</strong>) | <strong>Bridge</strong> = <em>Bridge</em>!'
    ),
    802: (
        '<strong>Túnel</strong> ≈ Hollow underground passage bored straight through a mountain rock face = <em>Tunnel</em>!',
        '<strong>Surang</strong> ≈ Identical to <strong>Tamil சுரங்கம் (Surangam = Underground passage!)</strong> = <em>Tunnel</em>!'
    ),
    803: (
        '<strong>Esquina</strong> (Outer street intersection) | <strong>Rincón</strong> (Quiet cozy inner room nook) = <em>Corner</em>!',
        '<strong>Kona</strong> ≈ Identical to <strong>Tamil கோணம் (Konam = Sharp wall angle/junction!)</strong> = <em>Corner</em>!'
    ),
    804: (
        '<strong>Estación</strong> ≈ Busy transit hub where buses & trains pause for boarding = <em>Station</em>!',
        '<strong>Station</strong> ≈ Crowded railway platform or metro stop with departing trains = <em>Station</em>!'
    ),
    805: (
        '<strong>Aeropuerto</strong> ≈ <strong>Aero</strong> (Air) + <strong>Puerto</strong> (Harbor/Port) → Airliner terminal = <em>Airport</em>!',
        '<strong>Airport</strong> | <strong>Hawai adda</strong> (<strong>Hawai</strong> Air + <strong>Adda</strong> Hub/Terminal) = <em>Airport</em>!'
    ),
    806: (
        '<strong>Estacionamiento</strong> (Car "stationing" bay) | <strong>Parqueo</strong> (Short car-park spot) = <em>Parking</em>!',
        '<strong>Parking</strong> ≈ Marked asphalt lane where cars pull in and lock up = <em>Parking</em>!'
    ),
    807: (
        '<strong>Boleto</strong> (Theater/bus stub) | <strong>Billete</strong> (Printed fare <strong>"Bill"</strong> / pass) = <em>Ticket</em>!',
        '<strong>Ticket</strong> ≈ Printed boarding pass or movie stub scanned at the entry gate = <em>Ticket</em>!'
    ),
    808: (
        '<strong>Pasaporte</strong> ≈ Literally "Pass-through-Port" stamped booklet for crossing borders = <em>Passport</em>!',
        '<strong>Passport</strong> ≈ Official stamped travel booklet checked at international immigration desks = <em>Passport</em>!'
    ),
    809: (
        '1. Large metropolis: <strong>Ciudad</strong> (Root of <strong>"Citadel / Citizen"</strong>) = <em>City</em>!<br>2. Smaller town: <strong>Pueblo</strong> (Community) | <strong>Localidad</strong> (District) = <em>Town</em>!',
        '1. Large metropolis: <strong>Sheher</strong> ≈ Bustling skyline with skyscrapers and traffic = <em>City</em>!<br>2. Smaller town: <strong>Kasba</strong> (Compact township) | <strong>Chhota sheher</strong> (Small town) = <em>Town</em>!'
    ),
    810: (
        '<strong>Pueblo</strong> (Root of <strong>"People"</strong>) | <strong>Aldea</strong> (Tiny peaceful rural hamlet) = <em>Village</em>!',
        '<strong>Gaon</strong> (<strong>Tamil கிராமம் = Hamlet!</strong>) | <strong>Dehaat</strong> (Quiet farm countryside) = <em>Village</em>!'
    ),
    811: (
        '1. Nation: <strong>País</strong> (Homeland) | <strong>Nación</strong> (Sovereign state) = <em>Country</em>!<br>2. Rural countryside: <strong>Campo</strong> (Open green farm fields) = <em>Countryside</em>!',
        '1. Nation: <strong>Desh</strong> (<strong>Tamil தேசம் = Homeland!</strong>) | <strong>Mulk</strong> (Realm) = <em>Country</em>!<br>2. Rural countryside: <strong>Dehaat</strong> | <strong>Kheton ka ilaqa</strong> (Farm fields area) = <em>Countryside</em>!'
    ),
    812: (
        '<strong>Centro</strong> ≈ Bullseye hub right in the middle of town or the target ring = <em>Center</em>!',
        '<strong>Center</strong> (Hub) | <strong>Beech</strong> (Sitting midway — like a <em>"Beach"</em> between land & sea!) = <em>Center</em>!'
    ),
    813: (
        '<strong>Edificio</strong> (Grand <strong>"Edifice"</strong>) | <strong>Construcción</strong> (Built structure) = <em>Building</em>!',
        '<strong>Building</strong> | <strong>Imaarat</strong> (Multi-storey concrete tower — paired with Tamil <strong>பவனம்</strong>!) = <em>Building</em>!'
    ),
    814: (
        '<strong>Escuela</strong> (Neighborhood academy) | <strong>Colegio</strong> (Primary/high school) = <em>School</em>!',
        '<strong>School</strong> ≈ Morning classrooms, backpacks, chalkboards & playground bells = <em>School</em>!'
    ),
    815: (
        '<strong>Universidad</strong> (Full degree campus) | <strong>Facultad</strong> (Subject <strong>"Faculty"</strong> department) = <em>College / University</em>!',
        '<strong>College / university</strong> ≈ Higher-education degree campus with lecture halls and hostels = <em>College / University</em>!'
    ),
    816: (
        '<strong>Biblioteca</strong> ≈ From Greek <em>Biblio</em> (Book, as in <strong>"Bibliography"</strong>) + <em>Theca</em> (Case) = <em>Library</em>!',
        '<strong>Library</strong> ≈ Quiet reading hall packed wall-to-wall with bookshelves to borrow = <em>Library</em>!'
    ),
    817: (
        '<strong>Cine</strong> (Big screen movie house) | <strong>Teatro</strong> (Live stage <strong>"Theater"</strong>) = <em>Cinema / Theater</em>!',
        '<strong>Cinema</strong> (Movie hall) | <strong>Theatre</strong> (Stage & screen auditorium) = <em>Cinema / Theater</em>!'
    ),
    818: (
        '<strong>Tienda</strong> (Canvas stall / boutique shop) | <strong>Negocio</strong> (Commerce — root of <strong>"Negotiate"</strong>!) = <em>Store / Shop</em>!',
        '<strong>Dukaan</strong> (<strong>Spoken Tamil துக்கான் = Street shop!</strong>) | <strong>Store</strong> (Retail counter) = <em>Store / Shop</em>!'
    ),
    819: (
        '<strong>Mercado</strong> (Root of <strong>"Merchant / Market"</strong>) | <strong>Supermercado</strong> (Grocery hall) = <em>Market / Supermarket</em>!',
        '<strong>Bazaar</strong> (Bustling open stalls) | <strong>Market</strong> | <strong>Mandi</strong> (Wholesale produce hub!) = <em>Market / Supermarket</em>!'
    ),
    820: (
        '<strong>Restaurante</strong> (Dining room serving <em>"Restorative"</em> meals) | <strong>Cafetería</strong> (Coffee & pastry bar) = <em>Restaurant / Cafe</em>!',
        '<strong>Restaurant</strong> | <strong>Hotel</strong> (Indian diner!) | <strong>Dhaba</strong> (Highway roadside eatery!) = <em>Restaurant / Cafe</em>!'
    ),
    821: (
        '1. Financial institution: <strong>Banco</strong> ≈ Wooden money-changer\'s <strong>"Bench"</strong> (origin of Bank!) = <em>Bank</em>!<br>2. River edge: <strong>Orilla</strong> (Oar shore) | <strong>Ribera</strong> (<strong>"River-bank"</strong>) = <em>River Bank</em>!',
        '1. Financial institution: <strong>Bank</strong> ≈ Vaulted building guarding savings & loans = <em>Bank</em>!<br>2. River edge: <strong>Kinaara</strong> ≈ Same shore meaning as <strong>Tamil கரை (Karai ≈ Kinaara!)</strong> = <em>River Bank</em>!'
    ),
    489: (
        '<strong>Ruidoso</strong> (Rowdy racket) | <strong>Fuerte</strong> (Blasting force — like piano <strong>"Forte"</strong>) = <em>Loud / Noisy</em>!',
        '<strong>Shor wala</strong> (Full of rowdy clamor) | <strong>Tez awaaz</strong> (<strong>Tez</strong> Sharp + <strong>Awaaz</strong> Voice) = <em>Loud / Noisy</em>!'
    ),
    501: (
        '<strong>Feliz</strong> (Root of <strong>"Felicity"</strong>) | <strong>Alegre</strong> (<strong>"Allegro"</strong> lively!) | <strong>Contento</strong> (<strong>"Content"</strong>!) = <em>Happy</em>!',
        '<strong>Khush</strong> ≈ Identical to <strong>Spoken Tamil குஷி (Khushi = Cheerful delight!)</strong> = <em>Happy</em>!'
    ),
    518: (
        '<strong>Listo</strong> (Sharp & quick) | <strong>Inteligente</strong> (<strong>"Intelligent"</strong>) | <strong>Astuto</strong> (<strong>"Astute"</strong> fox!) = <em>Smart / Clever</em>!',
        '<strong>Hoshiyaar</strong> (Alert & bright) | <strong>Chalaak</strong> (Quick-witted mind) = <em>Smart / Clever</em>!'
    ),
    523: (
        '<strong>Perezoso</strong> (Couch-snoozer like a jungle sloth!) | <strong>Vago</strong> (Wandering idler — root of <strong>"Vagrant"</strong>!) = <em>Lazy</em>!',
        '<strong>Aalsi</strong> (<strong>Tamil ஆலசியம் = Sloth!</strong>) | <strong>Kaamchor</strong> (<strong>Kaam</strong> Work + <strong>Chor</strong> Thief = Work-shirker!) = <em>Lazy</em>!'
    ),
    536: (
        '<strong>Oro</strong> (Metallic element <em>Au</em> — root of <strong>"Ornate / Ore"</strong>) | <strong>Dorado</strong> (In <em>"El Dorado"</em>!) = <em>Gold</em>!',
        '<strong>Sona</strong> (Pure gleaming yellow treasure) | <strong>Sunehra</strong> (Sunlit golden tint!) = <em>Gold</em>!'
    ),
    545: (
        '<strong>Hombre</strong> ≈ Root of English <strong>"Human / Homage"</strong> & famous Western greeting <em>"Hombre!"</em> = <em>Man</em>!',
        '<strong>Aadmi</strong> (Son of <em>Adam</em> / adult human) | <strong>Mard</strong> (Grown adult male) = <em>Man</em>!'
    ),
    546: (
        '<strong>Mujer</strong> ≈ Warm Latin root <em>Mulier</em> (Sounds like <strong>"Mother-Care"</strong>) = <em>Woman</em>!',
        '<strong>Aurat</strong> (Common adult woman term) | <strong>Mahila</strong> ≈ <strong>Tamil மகிளா (Mahila = Respected lady!)</strong> = <em>Woman</em>!'
    ),
    558: (
        '<strong>Hermano</strong> ≈ Think <strong>"Her-Man-Bro"</strong> standing loyal beside family = <em>Brother</em>!',
        '<strong>Bhai</strong> ≈ Famous lifelong sibling & buddy bond across India (<em>"Bhai-Bhai!"</em>) = <em>Brother</em>!'
    ),
    569: (
        '<strong>Pariente</strong> (Blood-kin parent/relation) | <strong>Familiar</strong> (Member of <em>Familia</em> clan) = <em>Relative</em>!',
        '<strong>Rishtedaar</strong> ≈ From <strong>Rishta</strong> (Family bond) + <strong>-daar</strong> (Holder) = <em>Relative</em>!'
    ),
    574: (
        '<strong>Desconocido</strong> (<strong>Des-</strong> Un + <strong>Conocido</strong> Known) | <strong>Extraño</strong> (Unfamiliar outsider) = <em>Stranger</em>!',
        '<strong>Anjaan</strong> (<strong>An-</strong> Un + <strong>Jaan</strong> Know) | <strong>Ajnabi</strong> (Unfamiliar newcomer) = <em>Stranger</em>!'
    ),
    577: (
        '<strong>Cuerpo</strong> ≈ Root of English <strong>"Corporal / Corpse / Corporation"</strong> = <em>Body</em>!',
        '<strong>Shareer</strong> (<strong>Tamil சரீரம்!</strong>) | <strong>Badan</strong> (Physical frame) | <strong>Jism</strong> (Living flesh) = <em>Body</em>!'
    ),
    588: (
        '<strong>Diente</strong> (Front biting — root of <strong>"Dentist"</strong>) | <strong>Muela</strong> (Grinding back <strong>"Molar"</strong>!) = <em>Tooth</em>!',
        '<strong>Daant</strong> ≈ Same Indo-European root as <strong>"Dentist"</strong> & <strong>Tamil தந்தம் (Dhantham!)</strong> = <em>Tooth</em>!'
    ),
    592: (
        '<strong>Garganta</strong> ≈ Swallowing & voice passage (origin of <strong>"Gargle"</strong>!) = <em>Throat</em>!',
        '<strong>Gala</strong> ≈ Same root as <strong>Tamil களம் (Galam = Vocal & swallowing passage!)</strong> = <em>Throat</em>!'
    ),
    615: (
        '<strong>Sangrar</strong> ≈ Verb form of <strong>Sangre</strong> (Blood / <em>Sanguine</em>) oozing from a cut = <em>To Bleed</em>!',
        '<strong>Khoon behna / khoon nikalna</strong> ≈ <strong>Khoon</strong> (Blood) + <strong>Behna</strong> (Flow) / <strong>Nikalna</strong> (Come out) = <em>To Bleed</em>!'
    ),
    622: (
        '<strong>Respiración</strong> (Deep lung inhale/exhale) | <strong>Aliento</strong> (Fresh misted puff of air) = <em>Breath</em>!',
        '<strong>Saans</strong> ≈ Same Sanskrit root as <strong>Tamil சுவாசம் (Suvaasam = Living inhale/exhale!)</strong> = <em>Breath</em>!'
    ),
    624: (
        '<strong>Enfermedad</strong> (Being <em>Enfermo</em> = sick) | <strong>Mal</strong> (Root of <strong>"Malady"</strong>!) = <em>Illness / Disease</em>!',
        '<strong>Beemari</strong> (Sickness from <em>Beemar</em>) | <strong>Marz</strong> (Deep chronic ailment) = <em>Illness / Disease</em>!'
    ),
    630: (
        '1. Noun: <strong>Herida</strong> (Cut/gash from <em>Herir</em>) = <em>Wound</em>!<br>2. Verb: <strong>Herir</strong> ("Hurt") | <strong>Lastimar</strong> (Injure/bruise) = <em>To Wound</em>!',
        '1. Noun: <strong>Ghaav</strong> (Open cut) | <strong>Chot</strong> (Bruise/bump) = <em>Wound</em>!<br>2. Verb: <strong>Ghaayal karna</strong> (Injure) | <strong>Chot lagana</strong> (Hurt) = <em>To Wound</em>!'
    ),
    643: (
        '<strong>Merienda</strong> (Afternoon tea bite) | <strong>Botana</strong> (Crunchy spiced party nibbles) = <em>Snack</em>!',
        '<strong>Halka-fulka nashta</strong> ≈ <strong>Halka-fulka</strong> (Light & crispy) + <strong>Nashta</strong> (Morsel bite) = <em>Snack</em>!'
    ),
    711: (
        '1. Ground surface: <strong>Piso</strong> (Tiled footing) | <strong>Suelo</strong> (<strong>"Soil"</strong> ground beneath feet) = <em>Floor</em>!<br>2. Building storey: <strong>Piso</strong> | <strong>Planta</strong> (Tower level) = <em>Storey</em>!',
        '1. Ground surface: <strong>Farsh</strong> ≈ Smooth stone or marble floor beneath your feet = <em>Floor</em>!<br>2. Building storey: <strong>Manzil</strong> ≈ Stacked elevator level (1st, 2nd floor) = <em>Storey</em>!'
    ),
    718: (
        '<strong>Mesa</strong> ≈ Shared flat-top origin with <strong>Tamil மேசை (Mesai!)</strong> & plateau <em>"Mesa"</em> = <em>Table</em>!',
        '<strong>Mez</strong> (Borrowed from Portuguese <em>Mesa</em> = <strong>Tamil மேசை!</strong>) | <strong>Table</strong> (Dining/study flat) = <em>Table</em>!'
    ),
    723: (
        '<strong>Almohada</strong> ≈ Fluffy bedtime cushion (Think <strong>"All-My-Head"</strong> sinking soft at night!) = <em>Pillow</em>!',
        '<strong>Takiya</strong> ≈ Soft cotton-stuffed headrest supporting your neck while sleeping (Think <em>"Tuck-under-head"</em>) = <em>Pillow</em>!'
    ),
}


def main():
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        lines = f.read().splitlines(True)

    sc_idx = next(i for i, l in enumerate(lines) if l.startswith("var cardShortcuts = "))
    s2_idx = next(i for i, l in enumerate(lines) if l.startswith("var split2DeckCards = "))

    card_shortcuts = json.loads(lines[sc_idx][len("var cardShortcuts = "):].rstrip().rstrip(";"))
    split2 = json.loads(lines[s2_idx][len("var split2DeckCards = "):].rstrip().rstrip(";"))

    assert len(split2) == 382, f"Expected 382 cards in split2DeckCards, got {len(split2)}"
    nums = [c["num"] for c in split2]
    assert nums == list(range(440, 822)), "Unexpected card numbers in split2DeckCards"

    updated_by_num = {}
    for c in split2:
        n = c["num"]
        if n in TAMIL_UPDATES:
            c["tamil"] = TAMIL_UPDATES[n]
        if n in SHORTCUT_UPDATES:
            ses, shi = SHORTCUT_UPDATES[n]
            c["shortcutEs"] = ses
            c["shortcutHi"] = shi
        if n in IMAGE_UPGRADES:
            c["imageUrl"] = IMAGE_UPGRADES[n]
            c["gifUrl"] = IMAGE_UPGRADES[n]

        # Ensure 100% sync with cardShortcuts
        card_shortcuts[str(n)] = {
            "es": c["shortcutEs"],
            "hi": c["shortcutHi"],
        }
        updated_by_num[n] = c

    lines[sc_idx] = "var cardShortcuts = " + json.dumps(card_shortcuts, ensure_ascii=False) + ";\n"
    lines[s2_idx] = "var split2DeckCards = " + json.dumps(split2, ensure_ascii=False) + ";\n"

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.writelines(lines)

    # Sync data/backup_original_cards.json
    if os.path.exists(BACKUP_PATH):
        with open(BACKUP_PATH, "r", encoding="utf-8") as f:
            bkp = json.load(f)
        items = bkp.values() if isinstance(bkp, dict) else bkp
        for val in items:
            if isinstance(val, dict):
                n = val.get("originalNum") or val.get("num")
                if n in updated_by_num:
                    src = updated_by_num[n]
                    val["trans"] = dict(src["trans"])
                    val["hiDevanagari"] = src["hiDevanagari"]
                    val["tamil"] = src["tamil"]
                    val["shortcutEs"] = src["shortcutEs"]
                    val["shortcutHi"] = src["shortcutHi"]
                    val["imageUrl"] = src["imageUrl"]
                    val["gifUrl"] = src["gifUrl"]
        with open(BACKUP_PATH, "w", encoding="utf-8") as f:
            json.dump(bkp, f, indent=2, ensure_ascii=False)

    print(
        f"Updated Split 3 & 4 (#440-#821): {len(split2)} cards synced | "
        f"Tamil fixes: {len(TAMIL_UPDATES)} | Shortcuts upgraded: {len(SHORTCUT_UPDATES)} | "
        f"Images upgraded: {len(IMAGE_UPGRADES)}"
    )


if __name__ == "__main__":
    main()
