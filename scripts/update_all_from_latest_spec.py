import json
import re
from collections import defaultdict
from scripts.hooks_2001_2500_complete import MULTI_TAMIL_2001_2500
HOOKS_2001_2500 = {}

# 1. Update HOOKS_2001_2500 and MULTI_TAMIL_2001_2500 for the cards in 2001-2200 whose sense count/order changed
UPDATED_TAMIL = {
    2004: "1. பள்ளித் தலைமை ஆசிரியர் (School Head) / 2. முக்கியமான (Main / Primary)",
    2033: "1. ஆட்டப் புள்ளிகள் (Sports Match Points) / 2. தேர்வு மதிப்பெண் (Test Marks Total)",
    2060: "தரவரிசை / நிலை (Position on a Leaderboard)",
    2063: "1. வேதியியல் (Science of Chemicals) / 2. மனப் பொருத்தம் (Interpersonal Spark)",
    2068: "1. தத்துவவியல் (Academic Study of Thought) / 2. வாழ்க்கைக் கொள்கை (Personal Outlook on Life)",
    2102: "1. விஷயம் / பிரச்சனை (Problem / Situation / Issue) / 2. பருப்பொருள் நிலை (Physical State in Science)",
    2113: "1. உடல் உற்சாகம் (Human Stamina / Vibe) / 2. மின்சார ஆற்றல் (Utility Power / Fuel)",
    2116: "இயக்கம் / அசைவு (Physical Movement / Gesture)",
    2117: "1. வாகன வேகம் (Moving Fast on the Road) / 2. இணைய வேகம் (Internet / Download Speed)",
    2119: "வாகன வேக அதிகரிப்பு (Vehicle Pickup / Surge)",
    2120: "1. பெருங்கூட்டம் (General Public / Crowd) / 2. தேவாலயத் திருப்பலி (Catholic Church Service)",
    2128: "1. மின்சாரத்தில் இயங்கும் (Powered by Battery / Cord) / 2. விறுவிறுப்பான சூழல் (Exciting Atmosphere)",
    2133: "1. கவர்ச்சியான ஆளுமை (Charismatic Personality) / 2. காந்த ஈர்ப்பு (Physical Magnetic Snap)",
    2143: "1. அலைபேசி / டிவி திரை (Phone / TV Display) / 2. திரையரங்கத் திரை (Movie Cinema Screen)",
    2144: "1. கணினித் திரை (Desktop Computer Screen) / 2. கண்காணி (Track / Supervise Actively)",
    2171: "1. தாதுச் சத்து (Dietary Nutrient) / 2. கனிமப் பாறை (Mined Ore / Crystal)",
    2186: "1. எலும்பு மாவுக்கட்டு (Broken Bone Cast) / 2. சுவர் பூச்சு (Wall Surface Coating)",
    2193: "1. இரப்பர் பொருள் (Flexible Elastic Material) / 2. இரப்பர் வளையம் (Elastic Band)",
}
MULTI_TAMIL_2001_2500.update(UPDATED_TAMIL)

UPDATED_HOOKS = {
    2004: (
        "<strong>1. Director / Directora</strong> ≈ Direct match with English <strong>\"Director\"</strong> → School head!<br>"
        "<strong>2. Principal</strong> ≈ 100% identical to English <strong>\"Principal\"</strong> → Main / Primary!",
        "<strong>1. Principal</strong> ≈ 100% identical to English &amp; spoken Tamil <strong>\"Principal\"</strong>!<br>"
        "<strong>2. Mukhya / Khas</strong> ≈ <strong>Tamil முக்கிய (Mukkiya)</strong> → <em>Mukhya</em> = Main / Primary!"
    ),
    2033: (
        "<strong>1. Marcador / Puntuación</strong> ≈ <em>Marcador</em> (Scoreboard marker) + <em>Puntuación</em> (Points) → Sports match points!<br>"
        "<strong>2. Calificación / Puntuación</strong> ≈ From <em>Qualify + Points</em> → Test marks total!",
        "<strong>1. Score / Run / Goal</strong> ≈ Direct English <strong>\"Score / Run / Goal\"</strong>!<br>"
        "<strong>2. Marks / Score</strong> ≈ Direct English &amp; spoken Tamil <strong>\"Marks / Score\"</strong>!"
    ),
    2060: (
        "<strong>Puesto / Posición / Rango</strong> ≈ <em>Posición</em> = English <strong>\"Position\"</strong>, <em>Rango</em> = English <strong>\"Rank\"</strong> → Position on a leaderboard!",
        "<strong>Rank / Position</strong> ≈ Direct English <strong>\"Rank / Position\"</strong> → Same exact words used in Hindi &amp; Tamil!"
    ),
    2063: (
        "<strong>1. Química (Science)</strong> ≈ Sounds like <strong>\"Chem-ica\" (Chemical)</strong> → Science of chemicals!<br>"
        "<strong>2. Química (Spark)</strong> ≈ Same word <em>Química</em> for romantic/interpersonal spark!",
        "<strong>1. Chemistry (Science)</strong> ≈ Direct English <strong>\"Chemistry\"</strong>!<br>"
        "<strong>2. Chemistry / Connection</strong> ≈ Direct English <strong>\"Chemistry / Connection\"</strong> between two people!"
    ),
    2068: (
        "<strong>1. Filosofía</strong> ≈ Direct sibling of English <strong>\"Philosophy\"</strong>!<br>"
        "<strong>2. Filosofía de vida</strong> ≈ <em>Filosofía</em> (Philosophy) + <em>de vida</em> (of life) → Personal outlook on life!",
        "<strong>1. Philosophy / Darshan-shastra</strong> ≈ Direct English <strong>\"Philosophy\"</strong> + <strong>Tamil தரிசனம் (Darshanam)</strong>!<br>"
        "<strong>2. Soch / Nazariya / Philosophy</strong> ≈ <em>Soch</em> (Thought) + <em>Nazariya</em> (Viewpoint) → Personal mindset!"
    ),
    2113: (
        "<strong>1. Energía / Ganas</strong> ≈ Direct sibling of English <strong>\"Energy\"</strong>!<br>"
        "<strong>2. Energía / Luz</strong> ≈ <em>Energía</em> (Power) + <em>Luz</em> (Light/Electricity) → Utility power!",
        "<strong>1. Energy / Josh</strong> ≈ Direct English <strong>\"Energy\"</strong> + <strong>Tamil ஜோஷ் (Josh - enthusiasm)</strong>!<br>"
        "<strong>2. Power / Bijli</strong> ≈ Direct English <strong>\"Power\"</strong> + <em>Bijli</em> (Electricity)!"
    ),
    2116: (
        "<strong>Movimiento (Moh-vee-myen-toh)</strong> ≈ Direct sibling of English <strong>\"Movement / Motion\"</strong> → Physical movement or gesture!",
        "<strong>Movement / Harkat</strong> ≈ Direct English <strong>\"Movement\"</strong> + <em>Harkat</em> (Motion/Gesture)!"
    ),
    2117: (
        "<strong>1. Velocidad / Rapidez</strong> ≈ Direct sibling of English <strong>\"Velocity / Rapid\"</strong> → Moving fast on the road!<br>"
        "<strong>2. Velocidad</strong> ≈ Same word <em>Velocidad</em> (Velocity) for internet download speed!",
        "<strong>1. Speed / Raftaar</strong> ≈ Direct English <strong>\"Speed\"</strong> + <em>Raftaar</em> (Fast pace)!<br>"
        "<strong>2. Speed</strong> ≈ 100% identical to English <strong>\"Internet Speed\"</strong>!"
    ),
    2119: (
        "<strong>Aceleración</strong> ≈ Direct sibling of English <strong>\"Acceleration\"</strong> → Vehicle pickup / surge!",
        "<strong>Pickup / Speed badhana</strong> ≈ Direct English <strong>\"Pickup / Speed\"</strong> + <em>Badhana</em> (Increase)!"
    ),
    2120: (
        "<strong>1. Las masas / La multitud</strong> ≈ Direct match with English <strong>\"The masses / Multitude\"</strong> → Massive crowd!<br>"
        "<strong>2. Misa</strong> ≈ Sounds like English <strong>\"Mass\" (Misa)</strong> → Catholic church service!",
        "<strong>1. Public / Bheed</strong> ≈ Direct English <strong>\"Public\"</strong> + <em>Bheed</em> (Crowd)!<br>"
        "<strong>2. Mass / Church service</strong> ≈ Direct English <strong>\"Mass / Church service\"</strong>!"
    ),
    2128: (
        "<strong>1. Eléctrico (Battery/Cord)</strong> ≈ Direct sibling of English <strong>\"Electric\"</strong>!<br>"
        "<strong>2. Eléctrico / Vibrante</strong> ≈ <em>Eléctrico</em> + English <strong>\"Vibrant\"</strong> → Exciting stadium atmosphere!",
        "<strong>1. Electric</strong> ≈ 100% identical to English <strong>\"Electric\"</strong>!<br>"
        "<strong>2. Zabardast mahaul</strong> ≈ <em>Zabardast</em> (Awesome/High-voltage) + <em>Mahaul</em> (Atmosphere)!"
    ),
    2133: (
        "<strong>1. Magnético (Personality)</strong> ≈ Direct sibling of English <strong>\"Magnetic\"</strong> → Charismatic personality!<br>"
        "<strong>2. Magnético (Snap)</strong> ≈ Same word <em>Magnético</em> for physical magnetic snap!",
        "<strong>1. Aakarshak / Zabardast personality</strong> ≈ <strong>Tamil ஆகர்ஷணம் (Aakarshanam - attraction)</strong> → Charismatic personality!<br>"
        "<strong>2. Magnetic</strong> ≈ 100% identical to English <strong>\"Magnetic\"</strong>!"
    ),
    2143: (
        "<strong>1. Pantalla</strong> ≈ Sounds like <strong>\"Paint-All-Ya\"</strong> → Phone or TV display screen!<br>"
        "<strong>2. Pantalla grande</strong> ≈ <em>Pantalla</em> (Screen) + <em>Grande</em> (Grand/Big) → Movie cinema big screen!",
        "<strong>1. Screen</strong> ≈ 100% identical to English <strong>\"Screen\"</strong>!<br>"
        "<strong>2. Screen / Parda</strong> ≈ Direct English <strong>\"Screen\"</strong> + <strong>Tamil பர்தா (Parda - curtain/screen)</strong>!"
    ),
    2144: (
        "<strong>1. Monitor / Pantalla</strong> ≈ 100% identical to English <strong>\"Monitor\"</strong>!<br>"
        "<strong>2. Monitorear / Vigilar</strong> ≈ Direct verb of <strong>\"Monitor / Vigilant\"</strong> → Track and supervise!",
        "<strong>1. Monitor / Screen</strong> ≈ 100% identical to English <strong>\"Monitor / Screen\"</strong>!<br>"
        "<strong>2. Najar rakhna / Check karte rehna</strong> ≈ <em>Najar</em> (Eye/Watch) + English <strong>\"Check\"</strong> → Supervise actively!"
    ),
    2171: (
        "<strong>1. Mineral (Nutrient)</strong> ≈ 100% identical to English <strong>\"Mineral\"</strong>!<br>"
        "<strong>2. Mineral (Geological Crystal)</strong> ≈ 100% identical to English <strong>\"Mineral\"</strong>!",
        "<strong>1. Mineral / Vitamin-mineral</strong> ≈ Direct English <strong>\"Vitamin-Mineral\"</strong>!<br>"
        "<strong>2. Khanij / Mineral</strong> ≈ From <em>Khan</em> (Mine) → Mined ore = <em>Khanij / Mineral</em>!"
    ),
    2186: (
        "<strong>1. Yeso / Escayola (Bone Cast)</strong> ≈ Sounds like <strong>\"Yes-Oh!\"</strong> → Hard white plaster cast on a wrist!<br>"
        "<strong>2. Yeso / Enlucido (Wall Coating)</strong> ≈ Same word <em>Yeso</em> for smooth wall plaster!",
        "<strong>1. Plaster (Bone Cast)</strong> ≈ 100% identical to English <strong>\"Plaster\"</strong>!<br>"
        "<strong>2. Plaster / Lep (Wall Coating)</strong> ≈ Direct English <strong>\"Plaster\"</strong> + <strong>Tamil லேபனம் (Lepanam = Lep)</strong>!"
    ),
    2193: (
        "<strong>1. Caucho / Goma</strong> ≈ <em>Goma</em> = English <strong>\"Gum / Rubber\"</strong>!<br>"
        "<strong>2. Gomita / Banda elástica</strong> ≈ Little <em>Goma</em> + <em>Elastic band</em> → Rubber band!",
        "<strong>1. Rubber</strong> ≈ 100% identical to English &amp; Tamil <strong>\"Rubber (ரப்பர்)\"</strong>!<br>"
        "<strong>2. Rubber band</strong> ≈ 100% identical to English <strong>\"Rubber band\"</strong>!"
    ),
}
HOOKS_2001_2500.update(UPDATED_HOOKS)

def parse_2001_2200(paths):
    entries = {}
    for p in paths:
        with open(p, encoding="utf-8") as f:
            lines = [l.strip() for l in f]
        i = 0
        while i < len(lines):
            line = lines[i]
            m = re.match(r"^(\d{4})\.\s+([A-ZÉ]+)\s+\((?:Only Concept|Split Concept\s+\d+):\s*(.+)\)$", line)
            if m:
                num, word, cname = int(m.group(1)), m.group(2), m.group(3).strip()
                if num not in entries:
                    entries[num] = {"word": word, "concepts": []}
                j = i + 1
                target_line, skip = "", False
                while j < len(lines) and not re.match(r"^\d{4}\.\s+[A-ZÉ]+", lines[j]):
                    if "Action:" in lines[j] and "SKIP" in lines[j]:
                        skip = True
                    if lines[j].startswith("• Target Labels:"):
                        tl = lines[j][len("• Target Labels:"):].strip()
                        if j + 1 < len(lines) and not lines[j+1].startswith("•") and lines[j+1] and not re.match(r"^\d{4}\.", lines[j+1]):
                            tl += " " + lines[j+1].strip()
                        target_line = tl
                    j += 1
                if not skip and target_line:
                    m2 = re.match(r"Hindi:\s*(.+?)\s*\|\s*Spanish:\s*(.+)$", target_line)
                    if m2:
                        entries[num]["concepts"].append((cname, m2.group(1).strip(), m2.group(2).strip()))
                i = j
            else:
                i += 1
    return entries

def parse_2201_2500(path):
    entries = {}
    with open(path, encoding="utf-8") as f:
        text = f.read()
    blocks = re.split(r"(?m)^(?=\d{4}\.\s+[A-ZÉ]+)", text)
    for b in blocks:
        b = b.strip()
        if not b:
            continue
        lines = [l.strip() for l in b.splitlines() if l.strip()]
        m = re.match(r"^(\d{4})\.\s+([A-ZÉ]+)$", lines[0])
        if not m:
            continue
        num, word = int(m.group(1)), m.group(2)
        rest = " ".join(lines[1:])
        if re.search(r"\b1\.\s+", rest):
            parts = re.split(r"\b(\d+)\.\s+", rest)
            concepts = []
            for k in range(1, len(parts), 2):
                s_body = parts[k+1].strip()
                m2 = re.match(r"^([^:]+):\s*Hindi:\s*(.+?)\s*\|\s*Spanish:\s*(.+)$", s_body)
                if m2:
                    concepts.append((m2.group(1).strip(), m2.group(2).strip(), m2.group(3).strip()))
            entries[num] = {"word": word, "concepts": concepts}
        else:
            m2 = re.match(r"^Hindi:\s*(.+?)\s*\|\s*Spanish:\s*(.+)$", rest)
            if m2:
                entries[num] = {"word": word, "concepts": [("Only", m2.group(1).strip(), m2.group(2).strip())]}
    return entries

all_spec = {}
all_spec.update(parse_2001_2200([
    "public/assets/aistudio/Paste_November_06__2026_-_10_50PM_3fa959c9",
    "public/assets/aistudio/Paste_November_06__2026_-_10_52PM_6c2d35c4"
]))
all_spec.update(parse_2201_2500("scripts/spec_2201_2500.txt"))

assert len(all_spec) == 500, f"Expected 500 entries, got {len(all_spec)}"

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

with open("scripts/accurate_images.json", "r", encoding="utf-8") as f:
    acc_images = json.load(f)

# Update tier2001DeckCards
m2001 = re.search(r"var tier2001DeckCards = (\[.*?\]);\n", html)
arr2001 = json.loads(m2001.group(1))

for c in arr2001:
    num = int(c["num"])
    spec = all_spec[num]
    concepts = spec["concepts"]
    if len(concepts) == 1:
        hi_str = concepts[0][1]
        es_str = concepts[0][2]
    else:
        hi_str = " | ".join(f"{idx}. {sc[0]}: {sc[1]}" for idx, sc in enumerate(concepts, 1))
        es_str = " | ".join(f"{idx}. {sc[0]}: {sc[2]}" for idx, sc in enumerate(concepts, 1))
    c["word"] = spec["word"]
    c["trans"] = {"es": es_str, "hi": hi_str}
    c["hiDevanagari"] = hi_str
    if num in MULTI_TAMIL_2001_2500:
        c["tamil"] = MULTI_TAMIL_2001_2500[num]
    if num in HOOKS_2001_2500:
        c["shortcutEs"], c["shortcutHi"] = HOOKS_2001_2500[num]

html = html[:m2001.start()] + "var tier2001DeckCards = " + json.dumps(arr2001, ensure_ascii=False) + ";\n" + html[m2001.end():]

# Eliminate the 9 token/parenthesized duplicates in 1-1000 so all 3,000 cards have 0 duplicates
DEDUP_UPDATES = {
    34: {
        "word": "THAT",
        "trans": {"es": "1. Pointing: ese (esa / eso) | 2. Connector: que", "hi": "1. Pointing: woh | 2. Connector: ki"},
        "tamil": "1. அது / அந்த (Pointing) / 2. என்று (Connector)",
        "shortcutEs": "<strong>1. Ese / Esa</strong> ≈ Point across at <em>THAT (Ese)</em>!<br><strong>2. Que (Keh)</strong> ≈ Connects clauses like \"I know <em>that (que)</em>\"!",
        "shortcutHi": "<strong>1. Woh</strong> ≈ Point across at <em>THAT (Woh)</em>!<br><strong>2. Ki</strong> ≈ Same connector sound as Tamil \"என்று\" — \"Main jaanta hoon <em>ki</em> (that)\"!"
    },
    37: {
        "word": "SOMEONE",
    },
    49: {
        "word": "NO ONE",
    },
    53: {
        "word": "A",
    },
    170: {
        "word": "WHEREAS",
        "emoji": "⚖️",
        "trans": {"es": "mientras que", "hi": "jabki"},
        "tamil": "அதேசமயம் (மாறாக)",
        "shortcutEs": "<strong>Mientras que</strong> ≈ <em>Mientras</em> (While) + <em>que</em> (that) → Contrasting two facts: <em>WHEREAS (Mientras que)</em>!",
        "shortcutHi": "<strong>Jabki (Jub-kee)</strong> ≈ <em>Jab</em> (When) + <em>Ki</em> (That) → Contrasting two sides: <em>WHEREAS (Jabki)</em>!",
        "imageUrl": "https://thumb.wikimedia.org/wikipedia/commons/thumb/c/c5/Balance_%C3%A0_tabac_1850.JPG/960px-Balance_%C3%A0_tabac_1850.JPG"
    },
    383: {
        "word": "OPEN",
        "trans": {"es": "1. Action: abrir | 2. State: abierto", "hi": "1. Action: kholna | 2. State: khula"},
        "tamil": "1. திறப்பது (Action) / 2. திறந்த (State)",
        "shortcutEs": "<strong>1. Abrir</strong> ≈ Root of <em>Aperture</em> (opening)!<br><strong>2. Abierto</strong> ≈ Sounds like <strong>\"A-Bear-Toe\"</strong> holding the door <em>open (Abierto)</em>!",
        "shortcutHi": "<strong>1. Kholna</strong> ≈ Action of opening a door!<br><strong>2. Khula</strong> ≈ State of being <em>open (Khula)</em>!"
    },
    447: {
        "word": "CLEAN",
        "trans": {"es": "1. Action: limpiar | 2. Spotless: limpio", "hi": "1. Action: saaf karna | 2. Spotless: saaf"},
        "tamil": "1. சுத்தம் செய் (Action) / 2. சுத்தமான (Spotless)",
        "shortcutEs": "<strong>1. Limpiar</strong> ≈ Wipe until it shines!<br><strong>2. Limpio</strong> ≈ Spotless and <em>Clean (Limpio)</em>!",
        "shortcutHi": "<strong>1. Saaf karna</strong> ≈ Spoken Tamil <strong>சாஃப் (Saaf)</strong> + <em>karna</em> (to make clean)!<br><strong>2. Saaf</strong> ≈ Spotless and <em>Clean (Saaf)</em>!"
    },
    532: {
        "word": "COLD",
        "trans": {"es": "1. Temperature: frío (fría) | 2. Illness: resfriado (gripe)", "hi": "1. Temperature: thanda | 2. Illness: zukaam (sardi)"},
        "tamil": "1. குளிர்ந்த (Temperature) / 2. சளி ஜலதோஷம் (Illness)",
        "shortcutEs": "<strong>1. Frío</strong> ≈ Sibling of English <strong>\"Freeze\"</strong>!<br><strong>2. Resfriado</strong> ≈ Catching a <em>Frío</em> (chilly cold) in the nose!",
        "shortcutHi": "<strong>1. Thanda</strong> ≈ Tamil <strong>தண்ணி (Thanni - cool water)</strong>!<br><strong>2. Zukaam / Sardi</strong> ≈ Winter <em>Sardi</em> nose cold!"
    },
    537: {
        "word": "HYGIENIC",
        "emoji": "🧼",
        "trans": {"es": "higiénico", "hi": "swachh / saaf-suthra"},
        "tamil": "சுகாதாரமான",
        "shortcutEs": "<strong>Higiénico (Ee-hyeh-nee-koh)</strong> ≈ Direct match with English <strong>\"Hygienic\"</strong>!",
        "shortcutHi": "<strong>Swachh / Saaf-suthra</strong> ≈ Famous <strong>\"Swachh Bharat\"</strong> (Clean &amp; Hygienic)!",
        "imageUrl": "https://thumb.wikimedia.org/wikipedia/commons/thumb/7/75/Soap_and_water_handwashing.jpg/960px-Soap_and_water_handwashing.jpg"
    },
    549: {
        "word": "VACANT",
        "emoji": "🪑",
        "trans": {"es": "vacío / libre", "hi": "khaali"},
        "tamil": "காலியான",
        "shortcutEs": "<strong>Vacío / Libre</strong> ≈ Direct sibling of English <strong>\"Vacant / Vacuum\"</strong> (<em>Vacío ≈ Vacant</em>)!",
        "shortcutHi": "<strong>Khaali</strong> ≈ Identical to Tamil <strong>காலி (Kaali - empty/vacant)</strong>!",
        "imageUrl": "https://thumb.wikimedia.org/wikipedia/commons/thumb/1/18/Ateneul_Rom%C3%A2n_-_Sala.jpg/960px-Ateneul_Rom%C3%A2n_-_Sala.jpg"
    },
    608: {
        "word": "MAROON",
        "emoji": "🟥",
        "trans": {"es": "granate / burdeos", "hi": "maroon / gehra laal"},
        "tamil": "மெரூன் நிறம் (கடும் சிவப்பு)",
        "shortcutEs": "<strong>Granate (Grah-nah-teh)</strong> ≈ Deep pomegranate (<em>Granada</em>) red = <em>Maroon (Granate)</em>!",
        "shortcutHi": "<strong>Maroon / Gehra laal</strong> ≈ Direct match with English &amp; Tamil <strong>\"Maroon (மெரூன்)\"</strong>!",
        "imageUrl": "https://thumb.wikimedia.org/wikipedia/commons/thumb/8/89/Pomegranate_fruit_-_whole_and_piece_with_arils.jpg/960px-Pomegranate_fruit_-_whole_and_piece_with_arils.jpg"
    },
    685: {
        "word": "FINGERNAIL",
        "trans": {"es": "uña", "hi": "naakhoon"},
        "tamil": "விரல் நகம்",
    },
    710: {
        "word": "FLU",
        "emoji": "🤒",
        "trans": {"es": "gripe / influenza", "hi": "flu / viral bukhar"},
        "tamil": "காய்ச்சல் சளி (ஃப்ளூ)",
        "shortcutEs": "<strong>Gripe / Influenza</strong> ≈ Direct match with English <strong>\"Grippe / Influenza (Flu)\"</strong>!",
        "shortcutHi": "<strong>Flu / Viral bukhar</strong> ≈ Direct English <strong>\"Flu / Viral\"</strong> + <em>Bukhar</em> (Fever)!",
        "imageUrl": "https://thumb.wikimedia.org/wikipedia/commons/thumb/1/1d/Clinical_thermometer_38.7.JPG/960px-Clinical_thermometer_38.7.JPG"
    },
    762: {
        "word": "ORANGE",
        "trans": {"es": "1. Fruit: naranja | 2. Color: naranja", "hi": "1. Fruit: santara | 2. Color: naarangi"},
        "tamil": "1. ஆரஞ்சு பழம் (Fruit) / 2. ஆரஞ்சு நிறம் (Color)",
        "shortcutEs": "<strong>1. Naranja (Fruit)</strong> &amp; <strong>2. Naranja (Color)</strong> ≈ Borrowed from Sanskrit/Tamil <em>Narangam (நாரங்கம்)</em>!",
        "shortcutHi": "<strong>1. Santara (Fruit)</strong> &amp; <strong>2. Naarangi (Color)</strong> ≈ <strong>Tamil நாரங்கம் (Narangam)</strong> → <em>Naarangi</em>!"
    },
}

for dname in ["tier1_200DeckCards", "tier201DeckCards", "tier401DeckCards", "tier601DeckCards"]:
    m = re.search(rf"var {dname} = (\[.*?\]);\n", html)
    arr = json.loads(m.group(1))
    changed = False
    for c in arr:
        num = int(c["num"])
        if num in DEDUP_UPDATES:
            up = DEDUP_UPDATES[num]
            for k, v in up.items():
                c[k] = v
            if "trans" in up:
                c["hiDevanagari"] = up["trans"]["hi"]
            if "imageUrl" in up:
                c["gifUrl"] = up["imageUrl"]
                acc_images[str(num)] = up["imageUrl"]
                acc_images[c["word"]] = up["imageUrl"]
            changed = True
    if changed:
        html = html[:m.start()] + f"var {dname} = " + json.dumps(arr, ensure_ascii=False) + ";\n" + html[m.end():]

html = html.replace('var STORAGE_KEY_EDITS = "sequential_vocab_user_custom_edits_v11";', 'var STORAGE_KEY_EDITS = "sequential_vocab_user_custom_edits_v12";')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

with open("scripts/accurate_images.json", "w", encoding="utf-8") as f:
    json.dump(acc_images, f, ensure_ascii=False, indent=2)

# Sync data/backup_original_cards.json
try:
    with open("data/backup_original_cards.json", "r", encoding="utf-8") as f:
        backup = json.load(f)
    if isinstance(backup, dict):
        for dname in ["tier1_200DeckCards", "tier201DeckCards", "tier401DeckCards", "tier601DeckCards", "tier2001DeckCards"]:
            m = re.search(rf"var {dname} = (\[.*?\]);\n", html)
            if m and dname in backup:
                backup[dname] = json.loads(m.group(1))
        with open("data/backup_original_cards.json", "w", encoding="utf-8") as f:
            json.dump(backup, f, ensure_ascii=False)
except Exception as e:
    print("Backup sync note:", e)

print("All 2001-2500 updates and 3,000-card deduplication applied!")
