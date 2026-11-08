import json
import re
import unicodedata
from scripts.es_hooks_data import ES_SOUND_ALIKES as ES1
from scripts.hi_hooks_data import HI_SOUND_ALIKES as HI1
from scripts.hooks_2001_2500_complete import (
    EXTRA_ES_HOOKS,
    EXTRA_HI_HOOKS,
)

with open("scripts/final_master_fix_3000.py", "r", encoding="utf-8") as f:
    fmf = f.read()

fmf_defs = fmf.split("def main(")[0]
ns = {"__file__": "scripts/final_master_fix_3000.py"}
exec(fmf_defs, ns)
ES2 = ns.get("ES_SOUND_ALIKES", {})
HI2 = ns.get("HI_SOUND_ALIKES", {})


def strip_acc(s):
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    ).lower()


def find_cognate(en_str, es_str):
    for ew in re.findall(r"[A-Za-z]+", en_str.lower()):
        if len(ew) < 3:
            continue
        for sw in re.findall(r"[A-Za-záéíóúüñ]+", es_str.lower()):
            sw_c = strip_acc(sw)
            if len(sw_c) < 3:
                continue
            if ew == sw_c:
                return ew.title()
            if len(ew) >= 4 and len(sw_c) >= 4 and (ew[:4] == sw_c[:4] or ew[:4] in sw_c or sw_c[:4] in ew):
                return ew.title()
            if sw_c.startswith("es") and len(ew) >= 3 and sw_c[1:4] == ew[:3]:
                return ew.title()
    return None


def build_es_sense_shortcut(word, label, es_val):
    es_clean = es_val.strip()
    es_low = es_clean.lower()
    en_ctx = f"{word} {label or ''}".strip()

    if es_low in EXTRA_ES_HOOKS:
        return EXTRA_ES_HOOKS[es_low]

    parts = [p.strip() for p in re.split(r"[/()]", es_clean) if p.strip()]
    for p in parts:
        pl = p.lower()
        if pl in EXTRA_ES_HOOKS:
            return EXTRA_ES_HOOKS[pl]
        if pl in ES2:
            return ES2[pl]
        if pl.endswith("se") and pl[:-2] in ES2:
            return ES2[pl[:-2]]
        if pl in ES1:
            bridge, link = ES1[pl]
            return f"<strong>{es_clean}</strong> ≈ {bridge} → {link}!"
        if pl.endswith("se") and pl[:-2] in ES1:
            bridge, link = ES1[pl[:-2]]
            return f"<strong>{es_clean}</strong> ≈ {bridge} → {link}!"

    cog = find_cognate(en_ctx, es_clean)
    if cog:
        return f'<strong>{es_clean}</strong> ≈ Direct match with English <strong>"{cog}"</strong> (same Latin root &amp; sound) → <em>{word.title()} ({es_clean})</em>!'

    return f'<strong>{es_clean}</strong> ≈ Key Spanish expression for <em>{word.title()} ({es_clean})</em>!'


def build_hi_sense_shortcut(word, label, hi_val, tamil_str=""):
    hi_clean = hi_val.strip()
    hi_low = hi_clean.lower()
    en_ctx = f"{word} {label or ''}".strip()
    ta_short = tamil_str.split("(")[0].split("/")[0].strip()
    ta_short = re.sub(r"^\d+\.\s*", "", ta_short).strip()

    if hi_low in EXTRA_HI_HOOKS:
        return EXTRA_HI_HOOKS[hi_low]

    parts = [p.strip() for p in re.split(r"[/()]", hi_clean) if p.strip()]
    en_words = set(re.findall(r"[a-z]+", en_ctx.lower()))

    native_parts = [p for p in parts if p.lower() not in en_words]
    search_order = native_parts + parts

    for p in search_order:
        pl = p.lower()
        st = re.sub(
            r"\s+(karna|hona|dena|lena|jaana|aana|padna|lagna|rehna|rakhna)$", "", pl
        ).strip()
        for cand in [pl, st]:
            if not cand:
                continue
            if cand in EXTRA_HI_HOOKS:
                return EXTRA_HI_HOOKS[cand]
            if cand in HI2:
                res = HI2[cand]
                if "/" in hi_clean:
                    res = re.sub(
                        r"^<strong>[^<]+</strong>",
                        f"<strong>{hi_clean}</strong>",
                        res,
                        count=1,
                    )
                return res
            if cand in HI1:
                bridge, link = HI1[cand]
                return f"<strong>{hi_clean}</strong> ≈ {bridge} → {link}!"

    ta_part = f" &amp; spoken Tamil <strong>{ta_short}</strong>" if ta_short else ""
    return f'<strong>{hi_clean}</strong> ≈ Everyday spoken Hindi for <strong>"{word.title()}"</strong>{ta_part}!'


def sync_card_shortcuts(card):
    w = card.get("word", "").strip()
    hi_str = card.get("trans", {}).get("hi", "").strip()
    es_str = card.get("trans", {}).get("es", "").strip()
    ta_str = card.get("tamil", "").strip()

    if "|" in hi_str and re.match(r"^1\.\s+", hi_str):
        hi_senses = [s.strip() for s in hi_str.split("|")]
        es_senses = [s.strip() for s in es_str.split("|")]
        ta_senses = [t.strip() for t in ta_str.split("/")]
        ses_parts = []
        shi_parts = []
        for idx, hs in enumerate(hi_senses):
            es_s = es_senses[idx] if idx < len(es_senses) else es_str
            hm = re.match(r"^(\d+)\.\s*([^:]+):\s*(.+)$", hs)
            em = re.match(r"^(\d+)\.\s*([^:]+):\s*(.+)$", es_s)
            s_i = hm.group(1) if hm else str(idx + 1)
            lbl = hm.group(2).strip() if hm else (em.group(2).strip() if em else f"Sense {s_i}")
            h_val = hm.group(3).strip() if hm else hs
            e_val = em.group(3).strip() if em else es_s
            ta_s = ta_senses[idx] if idx < len(ta_senses) else ta_str

            ses = build_es_sense_shortcut(w, lbl, e_val)
            shi = build_hi_sense_shortcut(w, lbl, h_val, ta_s)
            ses = re.sub(r"^<strong>", f"<strong>{s_i}. ({lbl}) ", ses, count=1)
            shi = re.sub(r"^<strong>", f"<strong>{s_i}. ({lbl}) ", shi, count=1)
            ses_parts.append(ses)
            shi_parts.append(shi)

        card["shortcutEs"] = "<br>".join(ses_parts)
        card["shortcutHi"] = "<br>".join(shi_parts)
    else:
        card["shortcutEs"] = build_es_sense_shortcut(w, None, es_str)
        card["shortcutHi"] = build_hi_sense_shortcut(w, None, hi_str, ta_str)

    card["hiDevanagari"] = hi_str


def parse_split_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    lines = text.splitlines()
    joined_entries = []
    cur = ""
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if s.startswith(
            (
                "Part ",
                "Filtered ",
                "Scowl/",
                "spoken ",
                "twins,",
                "original ",
                "Split ",
                "Whenever ",
            )
        ):
            continue
        if re.match(r"^\d+\.\s+[A-Z]", s):
            if cur:
                joined_entries.append(cur)
            cur = s
        else:
            if cur:
                cur += " " + s
    if cur:
        joined_entries.append(cur)

    parsed = {}
    for item in joined_entries:
        m = re.match(r"^(\d+)\.\s+([A-Z0-9\s\(\)\-\'\"]+?)\s+[—\-]\s+(.*)$", item)
        if not m:
            raise RuntimeError(f"Failed to match line: {item}")
        num = int(m.group(1))
        word = m.group(2).strip().upper()
        content = m.group(3).strip()
        if re.match(r"^1\.\s+", content):
            senses = re.split(r"\s*\|\s*(?=\d+\.\s+)", content)
            hi_parts, es_parts = [], []
            for s in senses:
                sm = re.match(
                    r"^(\d+\.\s*[^:]*?):\s*Hindi:\s*([^|]+)\s*\|\s*Spanish:\s*(.+)$",
                    s.strip(),
                )
                if not sm:
                    raise RuntimeError(f"Failed sense match: {s}")
                label = sm.group(1).strip()
                h = sm.group(2).strip()
                e = sm.group(3).strip()
                hi_parts.append(f"{label}: {h}")
                es_parts.append(f"{label}: {e}")
            hi_val = " | ".join(hi_parts)
            es_val = " | ".join(es_parts)
        else:
            hi_m = re.search(r"Hindi:\s*([^|]+)", content)
            es_m = re.search(r"Spanish:\s*(.+)$", content)
            hi_val = hi_m.group(1).strip() if hi_m else ""
            es_val = es_m.group(1).strip() if es_m else ""

        parsed[word] = {"list_num": num, "word": word, "hi": hi_val, "es": es_val}
    return parsed


# Multi-sense overrides and cleanups for Splits 2, 3, 4 (from user's Part 1 spec)
SPLIT2_PRUNED = {"MOMENT", "START", "REMAIN", "PICK", "WIPE", "WISH", "COMPLETE"}
SPLIT2_MULTI = {
    "SECOND": (
        "1. Time Unit: Second | 2. Ordinal Number: Doosra / Doosri",
        "1. Time Unit: Segundo | 2. Ordinal Number: Segundo / Segunda",
    ),
    "SPRING": (
        "1. Season: Vasant | 2. Water / Coil: Jharna / Spring",
        "1. Season: Primavera | 2. Water / Coil: Manantial / Resorte",
    ),
    "KNOW": (
        "1. Facts/Information: Pata hona / Jaanna | 2. People/Places: Jaan-pehchan hona",
        "1. Facts/Information: Saber | 2. People/Places: Conocer",
    ),
    "WORK": (
        "1. Job/Labor: Kaam karna | 2. Function/Machine: Chalna / Kaam karna",
        "1. Job/Labor: Trabajar | 2. Function/Machine: Funcionar",
    ),
    "CALL": (
        "1. Phone: Call karna | 2. Shout/Name: Bulaana / Pukaarna",
        "1. Phone: Llamar | 2. Shout/Name: Llamar",
    ),
    "LEAVE": (
        "1. Depart: Nikalna / Jaana | 2. Leave behind: Chhodna",
        "1. Depart: Salir / Irse | 2. Leave behind: Dejar",
    ),
    "TURN": (
        "1. Rotate/Direction: Mudna | 2. Switch State: Chalu karna / Band karna",
        "1. Rotate/Direction: Girar / Doblar | 2. Switch State: Encender / Apagar",
    ),
    "RUN": (
        "1. Sprint on foot: Daudna | 2. Manage business: Chalana",
        "1. Sprint on foot: Correr | 2. Manage business: Dirigir / Manejar",
    ),
    "WATCH": (
        "1. Wristwatch: Ghadi | 2. Observe/Look at: Dekhna",
        "1. Wristwatch: Reloj | 2. Observe/Look at: Mirar / Ver",
    ),
    "PASS": (
        "1. Ticket/Permit: Pass | 2. Move past/Hand over: Aage badhana / Guzarna",
        "1. Ticket/Permit: Pase | 2. Move past/Hand over: Pasar",
    ),
    "CLEAN": (
        "1. Adjective: Saaf | 2. Verb: Saaf karna",
        "1. Adjective: Limpio | 2. Verb: Limpiar",
    ),
}

SPLIT2_EXACT = {
    "ZERO": ("Zero / Shoonya", "Cero"),
    "ONE": ("Ek", "Uno / Una"),
    "TWO": ("Do", "Dos"),
    "THREE": ("Teen", "Tres"),
    "FOUR": ("Chaar", "Cuatro"),
    "FIVE": ("Paanch", "Cinco"),
    "SIX": ("Chheh", "Seis"),
    "SEVEN": ("Saat", "Siete"),
    "EIGHT": ("Aath", "Ocho"),
    "NINE": ("Nau", "Nueve"),
    "TEN": ("Das", "Diez"),
    "ELEVEN": ("Gyaarah", "Once"),
    "TWELVE": ("Baarah", "Doce"),
    "THIRTEEN": ("Terah", "Trece"),
    "FOURTEEN": ("Chaudah", "Catorce"),
    "FIFTEEN": ("Pandrah", "Quince"),
    "SIXTEEN": ("Solah", "Dieciséis"),
    "SEVENTEEN": ("Satrah", "Diecisiete"),
    "EIGHTEEN": ("Athaarah", "Dieciocho"),
    "NINETEEN": ("Unnees", "Diecinueve"),
    "TWENTY": ("Bees", "Veinte"),
    "THIRTY": ("Tees", "Treinta"),
    "FORTY": ("Chaalees", "Cuarenta"),
    "FIFTY": ("Pachaas", "Cincuenta"),
    "SIXTY": ("Saath", "Sesenta"),
    "SEVENTY": ("Sattar", "Setenta"),
    "EIGHTY": ("Assi", "Ochenta"),
    "NINETY": ("Nabbe", "Noventa"),
    "HUNDRED": ("Sau", "Cien / Ciento"),
    "THOUSAND": ("Hazaar", "Mil"),
    "MILLION": ("Das laakh / Million", "Millón"),
    "BILLION": ("Ek arab / Billion", "Mil millones / Billón"),
    "FIRST": ("Pehla / Pehli", "Primero / Primera"),
    "THIRD": ("Teesra / Teesri", "Tercero / Tercera"),
    "HALF": ("Aadha / Aadhi", "Mitad / Medio"),
}

SPLIT3_PRUNED = {"LARGE", "TINY", "HUGE", "QUICK", "VACANT", "SILENT", "PRETTY", "ILLNESS"}
SPLIT3_MULTI = {
    "SHORT": (
        "1. Height: Chhota / Kam kad ka | 2. Length/Duration: Chhota / Kam samay ka",
        "1. Height: Bajo / Baja | 2. Length/Duration: Corto / Corta",
    ),
    "HARD": (
        "1. Firm/Solid: Sakht / Thos | 2. Difficult: Mushkil / Kathin",
        "1. Firm/Solid: Duro / Dura | 2. Difficult: Difícil",
    ),
    "COOL": (
        "1. Weather: Thanda / Suhaavana | 2. Slang/Calm: Shaant / Cool / Badhiya",
        "1. Weather: Fresco | 2. Slang/Calm: Tranquilo / Genial / Guay",
    ),
    "KIND": (
        "1. Caring: Dayalu / Achhe dil ka | 2. Type: Kism / Tarah",
        "1. Caring: Amable / Bondadoso | 2. Type: Tipo / Clase",
    ),
    "FACE": (
        "1. Anatomy: Chehra / Munh | 2. Confront: Saamna karna",
        "1. Anatomy: Cara / Rostro | 2. Confront: Enfrentar",
    ),
    "ARM": (
        "1. Anatomy: Baanh / Haath | 2. Weapon: Hathiyaar",
        "1. Anatomy: Brazo | 2. Weapon: Arma",
    ),
    "TEAR": (
        "1. Eye Drop: Aansoo | 2. Rip/Rend: Faadna",
        "1. Eye Drop: Lágrima | 2. Rip/Rend: Rasgar / Romper",
    ),
}

SPLIT4_PRUNED = {
    "CORRIDOR",
    "YARD",
    "COUCH",
    "RUG",
    "WARDROBE",
    "CABINET",
    "SOCKET",
    "CLOTHING",
    "ROAD",
    "HARBOR",
}
SPLIT4_MULTI = {
    "ORANGE": (
        "1. Fruit: Santra | 2. Color: Narangi / Orange",
        "1. Fruit: Naranja | 2. Color: Naranja",
    ),
    "GLASS": (
        "1. Drinking Vessel: Glass | 2. Material: Kaanch",
        "1. Drinking Vessel: Vaso | 2. Material: Vidrio / Cristal",
    ),
    "POT": (
        "1. Cooking: Pateela / Bartan | 2. Plant: Gamla",
        "1. Cooking: Olla | 2. Plant: Maceta",
    ),
    "FLOOR": (
        "1. Surface: Farsh | 2. Story Level: Manzil",
        "1. Surface: Suelo / Piso | 2. Story Level: Piso / Planta",
    ),
    "MATCH": (
        "1. Fire: Maachis | 2. Sports: Match",
        "1. Fire: Fósforo / Cerilla | 2. Sports: Partido",
    ),
    "NAIL": (
        "1. Spike: Keel | 2. Body: Naakhoon",
        "1. Spike: Clavo | 2. Body: Uña",
    ),
    "SUIT": (
        "1. Clothing: Suit | 2. Appropriate: Suit karna / Jachna",
        "1. Clothing: Traje | 2. Appropriate: Convenir / Quedar bien",
    ),
    "BUTTON": (
        "1. Fastener: Button | 2. Electronic: Button",
        "1. Fastener: Botón | 2. Electronic: Botón",
    ),
    "COLLAR": (
        "1. Clothing: Collar | 2. Pet: Patta / Collar",
        "1. Clothing: Cuello | 2. Pet: Collar",
    ),
    "RING": (
        "1. Jewelry: Angoothi | 2. Sound/Call: Ring karna / Ghanti",
        "1. Jewelry: Anillo | 2. Sound/Call: Sonar / Llamar",
    ),
    "CORNER": (
        "1. Location: Kona / Nukkad | 2. Trap/Corner: Kone mein dabana",
        "1. Location: Esquina | 2. Trap/Corner: Arrinconar",
    ),
    "TRACK": (
        "1. Rail/Athletic: Track / Patri | 2. Monitor/Follow: Track karna",
        "1. Rail/Athletic: Vía / Pista | 2. Monitor/Follow: Rastrear / Seguir",
    ),
    "SIGN": (
        "1. Notice/Indicator: Sign board / Nishaan | 2. Signature: Sign karna",
        "1. Notice/Indicator: Señal / Letrero | 2. Signature: Firmar",
    ),
    "COUNTRY": (
        "1. Sovereign Nation: Desh | 2. Rural area: Gaaon / Dehaat",
        "1. Sovereign Nation: País | 2. Rural area: Campo",
    ),
    "CENTER": (
        "1. Middle: Center / Beech | 2. Facility Hub: Center / Kendra",
        "1. Middle: Centro | 2. Facility Hub: Centro",
    ),
    "BANK": (
        "1. Financial: Bank | 2. Riverbank: Kinaara",
        "1. Financial: Banco | 2. Riverbank: Orilla",
    ),
}


def clean_trans_format(val):
    if not val:
        return val
    if "|" in val and "1." in val:
        return val
    # Convert "(or foo)" or "(foo)" into clean " / Foo" and capitalize first letter of each slash part
    s = re.sub(r"\(\s*or\s+([^)]+)\)", r"/ \1", val)
    s = re.sub(r"\(([^)]+)\)", r"/ \1", s)
    parts = [p.strip() for p in s.split("/") if p.strip()]
    cap_parts = []
    for p in parts:
        if p:
            cap_parts.append(p[0].upper() + p[1:])
    # Deduplicate case-insensitively while preserving order
    seen = set()
    final_parts = []
    for cp in cap_parts:
        if cp.lower() not in seen:
            seen.add(cp.lower())
            final_parts.append(cp)
    return " / ".join(final_parts)


def main():
    print("Reading index.html...")
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    def get_deck(name):
        pos = html.find(f"var {name} = [")
        if pos == -1:
            raise RuntimeError(f"Deck {name} not found!")
        end = html.find("];", pos)
        return json.loads(html[pos + len(f"var {name} = ") : end + 1]), pos, end + 2

    s1, _, _ = get_deck("split1DeckCards")
    s2, _, _ = get_deck("split2DeckCards")
    s3, _, _ = get_deck("split3DeckCards")
    s4, _, _ = get_deck("split4DeckCards")
    s5, _, _ = get_deck("split5DeckCards")
    s6, _, _ = get_deck("split6DeckCards")
    s7, _, _ = get_deck("split7DeckCards")
    s8, _, _ = get_deck("split8DeckCards")

    # 1. Sync shortcuts for Split 1 (233 cards)
    for c in s1:
        sync_card_shortcuts(c)
    print(f"Split 1 synced: {len(s1)} cards")

    # 2. Filter and update Split 2 (243 cards)
    new_s2 = []
    for c in s2:
        w = c["word"].strip().upper()
        if w in SPLIT2_PRUNED:
            continue
        if w in SPLIT2_MULTI:
            c["trans"]["hi"], c["trans"]["es"] = SPLIT2_MULTI[w]
        elif w in SPLIT2_EXACT:
            c["trans"]["hi"], c["trans"]["es"] = SPLIT2_EXACT[w]
        else:
            c["trans"]["hi"] = clean_trans_format(c["trans"]["hi"])
            c["trans"]["es"] = clean_trans_format(c["trans"]["es"])
        sync_card_shortcuts(c)
        new_s2.append(c)
    print(f"Split 2 updated: {len(new_s2)} cards (expected 243)")

    # 3. Filter and update Split 3 (242 cards)
    new_s3 = []
    for c in s3:
        w = c["word"].strip().upper()
        if w in SPLIT3_PRUNED:
            continue
        if w in SPLIT3_MULTI:
            c["trans"]["hi"], c["trans"]["es"] = SPLIT3_MULTI[w]
        else:
            c["trans"]["hi"] = clean_trans_format(c["trans"]["hi"])
            c["trans"]["es"] = clean_trans_format(c["trans"]["es"])
        sync_card_shortcuts(c)
        new_s3.append(c)
    print(f"Split 3 updated: {len(new_s3)} cards (expected 242)")

    # 4. Filter and update Split 4 (240 cards)
    new_s4 = []
    for c in s4:
        w = c["word"].strip().upper()
        if w in SPLIT4_PRUNED:
            continue
        if w in SPLIT4_MULTI:
            c["trans"]["hi"], c["trans"]["es"] = SPLIT4_MULTI[w]
        else:
            c["trans"]["hi"] = clean_trans_format(c["trans"]["hi"])
            c["trans"]["es"] = clean_trans_format(c["trans"]["es"])
        sync_card_shortcuts(c)
        new_s4.append(c)
    print(f"Split 4 updated: {len(new_s4)} cards (expected 240)")

    # 5. Parse and apply Split 5 (480 cards from Paste 5:56PM)
    p5_map = parse_split_file(
        "public/assets/aistudio/Paste_November_08__2026_-_5_56PM_fc95f231"
    )
    new_s5 = []
    for c in s5:
        w = c["word"].strip().upper()
        if w not in p5_map:
            continue
        spec = p5_map[w]
        c["trans"]["hi"] = spec["hi"]
        c["trans"]["es"] = spec["es"]
        sync_card_shortcuts(c)
        new_s5.append(c)
    print(f"Split 5 updated: {len(new_s5)} cards (expected 480)")
    assert len(new_s5) == 480, f"Expected 480 for Split 5, got {len(new_s5)}"

    # 6. Parse and apply Split 6 (490 cards from Paste 6:01PM)
    p6_map = parse_split_file(
        "public/assets/aistudio/Paste_November_08__2026_-_6_01PM_fa48ab6c"
    )
    new_s6 = []
    for c in s6:
        w = c["word"].strip().upper()
        if w not in p6_map:
            continue
        spec = p6_map[w]
        c["trans"]["hi"] = spec["hi"]
        c["trans"]["es"] = spec["es"]
        sync_card_shortcuts(c)
        new_s6.append(c)
    print(f"Split 6 updated: {len(new_s6)} cards (expected 490)")
    assert len(new_s6) == 490, f"Expected 490 for Split 6, got {len(new_s6)}"

    # Replace split1DeckCards .. split8DeckCards block in index.html
    start_s1 = html.find("var split1DeckCards = [")
    _, _, end_s8 = get_deck("split8DeckCards")

    new_decks_block = "\n".join(
        [
            f"var split1DeckCards = {json.dumps(s1, ensure_ascii=False)};",
            f"var split2DeckCards = {json.dumps(new_s2, ensure_ascii=False)};",
            f"var split3DeckCards = {json.dumps(new_s3, ensure_ascii=False)};",
            f"var split4DeckCards = {json.dumps(new_s4, ensure_ascii=False)};",
            f"var split5DeckCards = {json.dumps(new_s5, ensure_ascii=False)};",
            f"var split6DeckCards = {json.dumps(new_s6, ensure_ascii=False)};",
            f"var split7DeckCards = {json.dumps(s7, ensure_ascii=False)};",
            f"var split8DeckCards = {json.dumps(s8, ensure_ascii=False)};",
        ]
    )

    html = html[:start_s1] + new_decks_block + html[end_s8:]

    # Update word count badges & learned stat lines in HTML
    count_updates = [
        ("tier-1", len(s1)),
        ("tier-251", len(new_s2)),
        ("tier-501", len(new_s3)),
        ("tier-751", len(new_s4)),
        ("tier-1001", len(new_s5)),
        ("tier-1501", len(new_s6)),
    ]
    for prefix, cnt in count_updates:
        html = re.sub(
            rf'(<strong id="{prefix}-total-words">)\d+(</strong>)',
            rf"\g<1>{cnt}\g<2>",
            html,
        )
        html = re.sub(
            rf'(<span id="{prefix}-stat-line"[^>]*>0 / )\d+( Learned</span>)',
            rf"\g<1>{cnt}\g<2>",
            html,
        )

    # Ensure registerOriginalCards registers all 8 split decks and bump STORAGE_KEY_EDITS
    html = html.replace(
        'var STORAGE_KEY_EDITS = "sequential_vocab_user_custom_edits_v12";',
        'var STORAGE_KEY_EDITS = "sequential_vocab_user_custom_edits_v15";',
    )
    reg_target = 'if (typeof tier800DeckCards !== "undefined") registerOriginalCards(tier800DeckCards);'
    reg_replacement = (
        "if (typeof split1DeckCards !== 'undefined') registerOriginalCards(split1DeckCards);\n"
        "      if (typeof split2DeckCards !== 'undefined') registerOriginalCards(split2DeckCards);\n"
        "      if (typeof split3DeckCards !== 'undefined') registerOriginalCards(split3DeckCards);\n"
        "      if (typeof split4DeckCards !== 'undefined') registerOriginalCards(split4DeckCards);\n"
        "      if (typeof split5DeckCards !== 'undefined') registerOriginalCards(split5DeckCards);\n"
        "      if (typeof split6DeckCards !== 'undefined') registerOriginalCards(split6DeckCards);\n"
        "      if (typeof split7DeckCards !== 'undefined') registerOriginalCards(split7DeckCards);\n"
        "      if (typeof split8DeckCards !== 'undefined') registerOriginalCards(split8DeckCards);\n"
        "      " + reg_target
    )
    if "registerOriginalCards(split1DeckCards)" not in html and reg_target in html:
        html = html.replace(reg_target, reg_replacement)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    # Also update data/backup_original_cards.json
    try:
        with open("data/backup_original_cards.json", "r", encoding="utf-8") as f:
            bkp = json.load(f)
        all_updated = s1 + new_s2 + new_s3 + new_s4 + new_s5 + new_s6
        by_num = {c.get("originalNum") or c.get("num"): c for c in all_updated}
        if isinstance(bkp, list):
            for item in bkp:
                n = item.get("originalNum") or item.get("num")
                if n in by_num:
                    src = by_num[n]
                    item["trans"] = dict(src["trans"])
                    item["shortcutEs"] = src.get("shortcutEs", "")
                    item["shortcutHi"] = src.get("shortcutHi", "")
                    item["hiDevanagari"] = src.get("hiDevanagari", "")
            with open("data/backup_original_cards.json", "w", encoding="utf-8") as f:
                json.dump(bkp, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("Backup sync note:", e)

    print("Successfully updated index.html and backup_original_cards.json!")


if __name__ == "__main__":
    main()
