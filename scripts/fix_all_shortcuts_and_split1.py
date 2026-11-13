import json, re, sys, unicodedata

DRY_RUN = "--dry-run" in sys.argv
UNMATCHED_ES = []
UNMATCHED_HI = []

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

from scripts.hooks_1_1446_complete import COMPLETE_ES_BRIDGES, COMPLETE_HI_BRIDGES
from scripts.hooks_gap_closure import GAP_ES_BRIDGES, GAP_HI_BRIDGES
from scripts.es_hooks_data import ES_SOUND_ALIKES as ES1
from scripts.hi_hooks_data import HI_SOUND_ALIKES as HI1
from scripts.hooks_2001_2500_complete import EXTRA_ES_HOOKS, EXTRA_HI_HOOKS

with open("scripts/final_master_fix_3000.py", "r", encoding="utf-8") as f:
    fmf = f.read()
fmf_head = fmf.split("# Load backup_original_cards.json")[0]
fmf_head = fmf_head.replace("from es_hooks_data import", "from scripts.es_hooks_data import")
fmf_head = fmf_head.replace("from hi_hooks_data import", "from scripts.hi_hooks_data import")
ns_fmf = {"__file__": "scripts/final_master_fix_3000.py"}
exec(fmf_head, ns_fmf)
ES2 = ns_fmf.get("ES_SOUND_ALIKES", {})
HI2 = ns_fmf.get("HI_SOUND_ALIKES", {})

with open("scripts/upgrade_all_to_800_1000_standard.py", "r", encoding="utf-8") as f:
    upg_code = f.read()
ns_upg = {}
exec(upg_code.split("def build_shortcut_es")[0], ns_upg)
ATOMIC_ES_PARTS = ns_upg.get("ATOMIC_ES_PARTS", {})
ATOMIC_HI_PARTS = ns_upg.get("ATOMIC_HI_PARTS", {})
HINDI_WORD_GLOSS = ns_upg.get("HINDI_WORD_GLOSS", {})

# Load user's manual gold-standard overrides from data/user_profiles.json if present
user_custom_overrides = {}
try:
    with open("data/user_profiles.json", "r", encoding="utf-8") as f:
        up = json.load(f)
    edits = up.get("profiles", {}).get("GLOBAL-1", {}).get("edits", {})
    for k, v in edits.items():
        user_custom_overrides[int(k)] = v
except Exception as e:
    print("Note: Could not read user_profiles.json:", e)

def strip_devanagari(s):
    if not s:
        return s
    s = s.replace("ஆश्रिதம்", "ஆசிரிதம்")
    s = re.sub(r'\s*\([\u0900-\u097F\s/,\.\-\'\"]+\)', '', s)
    s = re.sub(r'[\u0900-\u097F]+', '', s)
    s = re.sub(r'\s{2,}', ' ', s).strip()
    return s

def normalize_key(s):
    s = strip_devanagari(s)
    s = re.sub(r'<[^>]+>', '', s)
    s = s.lower().strip()
    s = re.sub(r'\s+', ' ', s)
    return s

def cap_first(s):
    if not s:
        return s
    return s[0].upper() + s[1:]

def strip_acc(s):
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    ).lower()

def find_cognate(en_str, es_str):
    stop = {"to", "the", "and", "for", "with", "from", "into", "over", "under", "verb", "noun", "adj", "person", "object", "action", "state", "place"}
    for ew in re.findall(r"[A-Za-z]+", en_str.lower()):
        if len(ew) < 3 or ew in stop:
            continue
        for sw in re.findall(r"[A-Za-záéíóúüñ]+", es_str.lower()):
            sw_c = strip_acc(sw)
            if len(sw_c) < 3 or sw_c in stop:
                continue
            if ew == sw_c:
                return ew.title()
            if len(ew) >= 4 and len(sw_c) >= 4 and (ew[:4] == sw_c[:4] or ew[:4] in sw_c or sw_c[:4] in ew):
                return ew.title()
            if sw_c.startswith("es") and len(ew) >= 3 and sw_c[1:4] == ew[:3]:
                return ew.title()
    return None

def get_Target_Display(card_word, sense_label):
    target_meaning = card_word.title()
    if sense_label:
        clean_lbl = re.sub(r'^\d+\.\s*', '', sense_label).strip()
        clean_lbl = re.sub(r'^(Verb|Noun|Adj|Adv|Prep|Conj)\s*-\s*', '', clean_lbl, flags=re.I).strip()
        if clean_lbl and clean_lbl.lower() not in ("verb", "noun", "adj", "adjective", "adverb"):
            target_meaning = f"{card_word.title()} ({clean_lbl})"
    return target_meaning

def clean_trailing_punct(s):
    s = s.strip()
    # Collapse doubled punctuation like "!!", ")!!", "!)!", "!."
    s = re.sub(r'!+', '!', s)
    s = re.sub(r'([)!])\s*!$', r'\1', s)
    if s.endswith("!)"):
        pass
    elif not s.endswith("!") and not s.endswith("?"):
        s += "!"
    # Normalize ")!" -> ")" if preceded by "!" inside parens, or keep clean ending
    s = re.sub(r'!+\s*\)!', '!)', s)
    s = re.sub(r'!+\s*→', ' →', s)
    s = re.sub(r'!+$', '!', s)
    return s

def strip_tautology_prefix(word_disp, val):
    """If val starts with '<word_disp> ("Gloss")' or '<word_disp> (Gloss)', extract clean gloss."""
    w_low = normalize_key(word_disp)
    m = re.match(r'^([A-Za-záéíóúüñ\-]+)\s*\(\s*["\']?([^"\')]+)["\']?\s*\)\s*(.*)$', val.strip())
    if m and normalize_key(m.group(1)) == w_low:
        gloss = m.group(2).strip()
        rest = m.group(3).strip()
        val_new = f'Meaning <strong>"{gloss}"</strong>'
        if rest:
            val_new += f" {rest}"
        return val_new
    return val

def format_bridge_entry(word_disp, val, target_disp):
    """Convert tuple or bridge string into full '<strong>Word</strong> ≈ ... → <em>Target</em>!' hook."""
    if isinstance(val, tuple):
        b, link = val
        b = strip_devanagari(b).rstrip("!.")
        link = strip_devanagari(link).rstrip("!.")
        return clean_trailing_punct(f"<strong>{cap_first(word_disp)}</strong> ≈ {b} → {link}")
    val = strip_devanagari(val).strip()
    if val.startswith("<strong>") or val.startswith("<b>"):
        if "≈" in val:
            if "<em>" not in val:
                val = val.rstrip("!.") + f" → <em>{target_disp}</em>!"
            return clean_trailing_punct(val)
    val = strip_tautology_prefix(word_disp, val)
    if "<em>" in val or "→" in val or "=" in val:
        return clean_trailing_punct(f"<strong>{cap_first(word_disp)}</strong> ≈ {val}")
    return clean_trailing_punct(f"<strong>{cap_first(word_disp)}</strong> ≈ {val.rstrip('!.')} → <em>{target_disp}</em>")

PRIMARY_ES = {normalize_key(k): v for k, v in COMPLETE_ES_BRIDGES.items()}
PRIMARY_ES.update({normalize_key(k): v for k, v in GAP_ES_BRIDGES.items()})
PRIMARY_HI = {normalize_key(k): v for k, v in COMPLETE_HI_BRIDGES.items()}
PRIMARY_HI.update({normalize_key(k): v for k, v in GAP_HI_BRIDGES.items()})

SECONDARY_ES = {}
for d in (ES1, ES2, EXTRA_ES_HOOKS, ATOMIC_ES_PARTS):
    for k, v in d.items():
        nk = normalize_key(k)
        if nk not in SECONDARY_ES:
            SECONDARY_ES[nk] = v

SECONDARY_HI = {}
for d in (HI1, HI2, EXTRA_HI_HOOKS, ATOMIC_HI_PARTS, HINDI_WORD_GLOSS):
    for k, v in d.items():
        nk = normalize_key(k)
        if nk not in SECONDARY_HI:
            SECONDARY_HI[nk] = v

def check_target_compatible(hook_text, card_word, sense_label):
    em_matches = re.findall(r'<em>([^<]+)</em>', hook_text)
    if not em_matches:
        return True
    context = f"{card_word} {sense_label or ''}".lower()
    context_words = set(re.findall(r'[a-z]+', context))
    stop = {"to", "a", "an", "the", "of", "in", "on", "for", "or", "and", "be", "make", "do", "get", "adj", "noun", "verb", "person", "object", "action", "state", "place"}
    sig_context = context_words - stop
    if not sig_context:
        sig_context = context_words

    # Check both <em> tags AND the trailing conclusion after the last '=' or '→'
    plain_text = re.sub(r'<[^>]+>', '', hook_text).lower()
    tail = plain_text.rsplit('=', 1)[-1] if '=' in plain_text else plain_text.rsplit('→', 1)[-1]
    all_target_text = (" ".join(em_matches) + " " + tail).lower()
    target_words = set(re.findall(r'[a-z]+', all_target_text))
    for cw in sig_context:
        if cw in target_words:
            return True
        if len(cw) >= 4:
            for ew in target_words:
                if len(ew) >= 4 and (cw[:4] == ew[:4] or cw in ew or ew in cw):
                    return True
    return False

def align_hook_target(hook_text, card_word, sense_label, word_disp):
    if check_target_compatible(hook_text, card_word, sense_label):
        return hook_text
    target_disp = f"{get_Target_Display(card_word, sense_label)} ({cap_first(word_disp)})"
    if "→" in hook_text:
        prefix = hook_text.rsplit("→", 1)[0].strip().rstrip("!.")
        return clean_trailing_punct(f"{prefix} → <em>{target_disp}</em>")
    # If the last <em> is inside parentheses or near the start (etymology/example), append → <em>Target</em> instead of overwriting it
    last_em = list(re.finditer(r'<em>[^<]+</em>', hook_text))[-1]
    if last_em.end() < len(hook_text) - 5:
        return clean_trailing_punct(f"{hook_text.rstrip('!.')} → <em>{target_disp}</em>")
    return clean_trailing_punct(re.sub(r'<em>[^<]+</em>(?!.*<em>)', f'<em>{target_disp}</em>', hook_text))

def filter_distinct_synonyms(tokens):
    """Keep slash-separated synonyms that represent distinct words, filtering trivial gender/plural inflections of the same stem."""
    if len(tokens) <= 1:
        return tokens
    out = [tokens[0]]
    base0 = strip_acc(re.sub(r'\s*\([^)]*\)', '', tokens[0]).strip())
    for t in tokens[1:]:
        bt = strip_acc(re.sub(r'\s*\([^)]*\)', '', t).strip())
        # Skip single-word inflections sharing >=4-char stem or differing only in final o/a/e/i/os/as/es
        if " " not in base0 and " " not in bt and len(base0) >= 3 and len(bt) >= 3:
            stem_len = max(2, min(len(base0), len(bt)) - 1)
            if base0[:stem_len] == bt[:stem_len] and abs(len(base0) - len(bt)) <= 2:
                continue
        out.append(t)
    return out

def parse_paste_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        raw_lines = f.read().splitlines()

    logical_lines = []
    in_footer = False
    for line in raw_lines:
        s = line.strip().replace("\\.", ".")
        if not s:
            continue
        if re.match(r'^Part\s+\d+.*Split\s+\d+', s):
            in_footer = False
            continue
        if s.startswith("The 2 ") or s.startswith("The 4 ") or s.startswith("Alignment on"):
            in_footer = True
            continue
        if in_footer:
            continue
        is_top = bool(re.match(r'^\d+\.\s+', line))
        is_sub = bool(re.match(r'^\s+\d+(?:\\)?\.\s+', line))
        if is_top or is_sub:
            logical_lines.append((is_top, s))
        elif logical_lines:
            prev_top, prev_text = logical_lines[-1]
            logical_lines[-1] = (prev_top, prev_text + " " + s)

    def strip_brackets(s):
        s = re.sub(r'\s*\[[^\]]*\]', '', s)
        return re.sub(r'\s{2,}', ' ', s).strip()

    parsed = {}
    cur_num = None
    for is_top, text in logical_lines:
        text = strip_brackets(text)
        if is_top:
            m = re.match(r'^(\d+)\.\s+(.+?)\s*—\s*(.*)$', text)
            assert m, f"Could not parse top line in {filepath}: {text}"
            cur_num = int(m.group(1))
            word_title = m.group(2).strip().upper()
            rest = m.group(3).strip()
            if not rest:
                parsed[cur_num] = {"word": word_title, "senses": []}
            elif re.match(r'^1\.\s+', rest):
                chunks = re.split(r'\s+(?=\d+\.\s+\()', rest)
                senses = []
                for ch in chunks:
                    sm = re.match(r'^(\d+)\.\s*\(([^)]+)\):\s*Sp:\s*(.+?)\s*\|\s*Hn:\s*(.*)$', ch.strip())
                    assert sm, f"Could not parse inline sense on #{cur_num} in {filepath}: {ch}"
                    senses.append((f"{sm.group(1)}. {sm.group(2).strip()}", sm.group(3).strip(), sm.group(4).strip()))
                parsed[cur_num] = {"word": word_title, "senses": senses}
            else:
                m_inline = re.match(r'^Sp:\s*(.+?)\s*\|\s*Hn:\s*(.*)$', rest)
                assert m_inline, f"Could not parse inline Sp/Hn on #{cur_num} in {filepath}: {rest}"
                parsed[cur_num] = {
                    "word": word_title,
                    "senses": [(None, m_inline.group(1).strip(), m_inline.group(2).strip())]
                }
        else:
            m_sub = re.match(r'^(\d+)\.\s*(?:\(([^)]+)\)|([^:]+)):\s*Sp:\s*(.+?)\s*\|\s*Hn:\s*(.*)$', text)
            assert m_sub and cur_num is not None, f"Could not parse sub line on #{cur_num} in {filepath}: {text}"
            s_idx = m_sub.group(1).strip()
            s_lbl = (m_sub.group(2) or m_sub.group(3)).strip()
            sp = m_sub.group(4).strip()
            hn = m_sub.group(5).strip()
            parsed[cur_num]["senses"].append((f"{s_idx}. {s_lbl}", sp, hn))
    return parsed

parsed_split1 = parse_paste_file("public/assets/aistudio/Paste_November_13__2026_-_8_50PM_6be1c21a")
print(f"Parsed {len(parsed_split1)} cards for Split 1 (expected 439)")
assert len(parsed_split1) == 439, f"Expected 439 cards, got {len(parsed_split1)}"

parsed_split2 = parse_paste_file("public/assets/aistudio/Paste_November_13__2026_-_9_59PM_9335d57b")
print(f"Parsed {len(parsed_split2)} cards for Split 2 (expected 382)")
assert len(parsed_split2) == 382, f"Expected 382 cards, got {len(parsed_split2)}"

parsed_part2 = parse_paste_file("public/assets/aistudio/Paste_November_13__2026_-_10_12PM_986b540b")
print(f"Parsed {len(parsed_part2)} cards for Part 2 Split 5 & 6 (expected 441)")
assert len(parsed_part2) == 441, f"Expected 441 cards, got {len(parsed_part2)}"

parsed_part3 = parse_paste_file("public/assets/aistudio/Paste_November_13__2026_-_10_14PM_39d3651f")
print(f"Parsed {len(parsed_part3)} cards for Part 3 Split 7 & 8 (expected 184)")
assert len(parsed_part3) == 184, f"Expected 184 cards, got {len(parsed_part3)}"

# Apply Split 1 micro-tweaks + card 51 (THE) clean Hindi text
parsed_split1[51]["senses"] = [
    (None, "el / la / los / las", "No direct word (dropped in Hindi)")
]
parsed_split1[236]["senses"] = [
    (None, "millón / mil millones (billón)", "das laakh (million) / ek arab (billion)")
]
parsed_split1[382]["senses"] = [
    ("1. Verb", "cocinar", "pakana / khaana banana"),
    ("2. Person", "cocinero / cocinera", "rasoiya / bawarchi"),
]
parsed_split1[401]["senses"] = [
    ("1. Strategy", "plan / proyecto", "plan / yojna"),
    ("2. Prepare ahead", "planear / planificar", "plan banana / taiyaari karna"),
]
parsed_split1[403]["senses"] = [
    (None, "organizar", "vyavasthit karna / theek se rakhna")
]

# Apply Part 2 micro-tweaks (837, 1019, 1115, 1169)
parsed_part2[837]["senses"][0] = ("1. Outer cosmos", "espacio (exterior)", "space / aasmaan ke baahar")
parsed_part2[1019]["senses"] = [(None, "encantador / seductor", "pyaara / dil jeetne wala")]
parsed_part2[1115]["senses"] = [(None, "carpintero", "badhai (carpenter)")]
parsed_part2[1169]["senses"] = [(None, "dinero en efectivo / dinero", "cash / nagad paise")]

# Apply Part 3 micro-tweak (1365 sense 2)
parsed_part3[1365]["senses"][1] = ("2. Misuse/squander", "desperdicio", "barbaadi / fizool kharchi")

def sanitize_sense_label(lbl):
    if not lbl:
        return lbl
    return lbl.replace(":", " -")

def format_trans_from_senses(senses):
    es_parts = []
    hi_parts = []
    for lbl, sp, hn in senses:
        sp_c = cap_first(strip_devanagari(sp.strip()))
        hn_c = cap_first(strip_devanagari(hn.strip()))
        if lbl is None:
            es_parts.append(sp_c)
            hi_parts.append(hn_c)
        else:
            clean_lbl = sanitize_sense_label(lbl.strip())
            es_parts.append(f"{clean_lbl}: {sp_c}")
            hi_parts.append(f"{clean_lbl}: {hn_c}")
    return " | ".join(es_parts), " | ".join(hi_parts)

def fix_existing_trans_colons(trans_str):
    if not trans_str:
        return trans_str
    trans_str = strip_devanagari(trans_str)
    parts = [p.strip() for p in trans_str.split("|")]
    fixed_parts = []
    for p in parts:
        if re.match(r'^\d+\.\s+', p) and p.count(":") >= 2:
            first_colon = p.find(":")
            second_colon = p.find(":", first_colon + 1)
            lbl_part = p[:second_colon].replace(":", " -")
            val_part = p[second_colon + 1:].strip()
            fixed_parts.append(f"{lbl_part}: {val_part}")
        else:
            fixed_parts.append(p)
    return " | ".join(fixed_parts)

def split_sense_line(part):
    part = part.strip()
    m = re.match(r'^(\d+\.\s*[^:]+):\s*(.+)$', part)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return None, part

def lookup_single_es(token_disp, card_word, sense_label):
    tk = normalize_key(token_disp)
    t_clean = re.sub(r'\s*\([^)]*\)', '', tk).strip()
    target_disp = f"{get_Target_Display(card_word, sense_label)} ({cap_first(token_disp)})"

    for key in (tk, t_clean, tk[:-2] if tk.endswith("se") else tk):
        if key in PRIMARY_ES:
            h = format_bridge_entry(token_disp, PRIMARY_ES[key], target_disp)
            return align_hook_target(h, card_word, sense_label, token_disp)
        if key in SECONDARY_ES:
            h = format_bridge_entry(token_disp, SECONDARY_ES[key], target_disp)
            return align_hook_target(h, card_word, sense_label, token_disp)

    cog = find_cognate(f"{card_word} {sense_label or ''}", token_disp)
    if cog:
        return f'<strong>{cap_first(token_disp)}</strong> ≈ Direct match with English <strong>"{cog}"</strong> (same Latin root) → <em>{target_disp}</em>!'
    return None

def build_es_hook_for_sense(card_num, card_word, sense_label, sp_val):
    nk = normalize_key(sp_val)
    w_low = card_word.lower()
    lbl_low = (sense_label or "").lower()
    ctx = f"{w_low} {lbl_low}"

    # Context-sensitive homonym disambiguations
    if w_low == "the":
        return '<strong>El / La / Los / Las</strong> ≈ Definite articles for <strong>"The"</strong> (<em>El / La</em> singular, <em>Los / Las</em> plural — e.g., <em>Los Angeles</em>) = <em>The</em>!'
    if nk == "rico":
        if "delicious" in ctx or "tasty" in ctx:
            return '<strong>Rico</strong> ≈ <strong>Rich</strong> in flavor → Delicious, mouth-watering food = <em>Delicious / Tasty (Rico)</em>!'
        return '<strong>Rico</strong> ≈ Direct match with English <strong>"Rich"</strong> → Wealthy / affluent = <em>Rich (Rico)</em>!'
    if nk == "recoger":
        if "gather" in ctx or "collect" in ctx:
            return '<strong>Recoger</strong> ≈ <strong>Re-collect</strong> → Gather things together from around = <em>Gather / Collect (Recoger)</em>!'
        return '<strong>Recoger</strong> ≈ <strong>Re-collect</strong> → Reach down and pick something up = <em>Pick Up (Recoger)</em>!'
    if nk == "mencionar":
        if "bring up" in ctx:
            return '<strong>Mencionar</strong> ≈ Direct match with English <strong>"Mention"</strong> → Bring up a topic in conversation = <em>Bring Up / Mention (Mencionar)</em>!'
        return '<strong>Mencionar</strong> ≈ Direct match with English <strong>"Mention"</strong> → Speak briefly of something = <em>Mention (Mencionar)</em>!'
    if nk == "carrera":
        if "race" in ctx or "running" in ctx:
            return '<strong>Carrera</strong> ≈ Sibling of <strong>"Career / Chariot"</strong> → Runners or cars racing at full speed = <em>Race (Carrera)</em>!'
        return '<strong>Carrera</strong> ≈ Direct sibling of English <strong>"Career"</strong> → Your professional path or university degree = <em>Career (Carrera)</em>!'
    if nk == "impermeable":
        if "raincoat" in ctx or "coat" in ctx:
            return '<strong>Impermeable</strong> ≈ <strong>Im-permeable</strong> (water cannot pass through) → Waterproof coat worn in the rain = <em>Raincoat (Impermeable)</em>!'
        return '<strong>Impermeable</strong> ≈ <strong>Im-permeable</strong> (direct cognate) → Material that water cannot penetrate = <em>Waterproof (Impermeable)</em>!'
    if nk == "vacío":
        if "vacuum" in ctx:
            return '<strong>Vacío</strong> ≈ Direct sibling of English <strong>"Vacuum / Vacant"</strong> → Space completely devoid of matter or air = <em>Vacuum (Vacío)</em>!'
        return '<strong>Vacío</strong> ≈ Direct sibling of English <strong>"Vacant / Vacuum"</strong> → Nothing inside at all = <em>Empty (Vacío)</em>!'
    if nk == "colina":
        return '<strong>Colina</strong> ≈ Sounds like <strong>"Cool-Incline"</strong> → Walk up a gentle grassy slope = <em>Hill (Colina)</em>!'
    if nk == "guardar":
        if "put away" in ctx:
            return '<strong>Guardar</strong> ≈ <strong>Guard / Wardrobe</strong> → Put things safely away in their place = <em>Put Away (Guardar)</em>!'
        return '<strong>Guardar</strong> ≈ Direct sibling of English <strong>"Guard"</strong> → Guard and keep something safely = <em>Keep / Save (Guardar)</em>!'
    if nk == "dejar":
        if "allow" in ctx or "let" in ctx:
            return '<strong>Dejar</strong> ≈ Un-jam the door → Let someone pass or allow them to do it = <em>Let / Allow (Dejar)</em>!'
        return '<strong>Dejar</strong> ≈ Leave something behind or let it go = <em>Leave (Dejar)</em>!'
    if nk == "subir":
        if "upload" in ctx:
            return '<strong>Subir</strong> ≈ Move <strong>Up</strong> (opposite of <em>Sub-</em>) → Send a file up to the cloud = <em>Upload (Subir)</em>!'
        if "climb" in ctx:
            return '<strong>Subir</strong> ≈ Ascend / Move <strong>Up</strong> → Climb up a mountain, stairs, or ladder = <em>Climb (Subir)</em>!'
        return '<strong>Subir</strong> ≈ Move <strong>Up</strong> → Rise or go upward = <em>Go Up / Rise (Subir)</em>!'

    # Check if full phrase matches
    full_match = lookup_single_es(sp_val, card_word, sense_label)
    raw_tokens = [t.strip() for t in re.split(r'\s*/\s*', sp_val) if t.strip()]
    tokens = filter_distinct_synonyms(raw_tokens)

    # If multiple distinct slash-separated synonyms exist, combine up to 2 distinct hooks
    if len(tokens) > 1:
        sub_hooks = []
        for t in tokens:
            sh = lookup_single_es(t, card_word, sense_label)
            if sh and sh not in sub_hooks:
                sub_hooks.append(sh)
        if sub_hooks:
            return " | ".join(sub_hooks[:2])

    if len(tokens) == 1 and len(raw_tokens) > 1:
        for rt in raw_tokens:
            single_h = lookup_single_es(rt, card_word, sense_label)
            if single_h:
                return single_h

    if full_match:
        return full_match

    if DRY_RUN:
        UNMATCHED_ES.append((card_num, card_word, sense_label, sp_val))
        return f"MISSING_ES:{sp_val}"
    raise ValueError(f"Unmatched ES sense on #{card_num} {card_word}: {sp_val}")

def lookup_single_hi(token_disp, card_word, sense_label):
    tk = normalize_key(token_disp)
    t_clean = re.sub(r'\s*\([^)]*\)', '', tk).strip()
    target_disp = f"{get_Target_Display(card_word, sense_label)} ({cap_first(token_disp)})"

    for key in (tk, t_clean):
        if key in PRIMARY_HI:
            h = format_bridge_entry(token_disp, PRIMARY_HI[key], target_disp)
            return align_hook_target(h, card_word, sense_label, token_disp)
        if key in SECONDARY_HI:
            h = format_bridge_entry(token_disp, SECONDARY_HI[key], target_disp)
            return align_hook_target(h, card_word, sense_label, token_disp)

    cog = find_cognate(f"{card_word} {sense_label or ''}", token_disp)
    if cog:
        return f'<strong>{cap_first(token_disp)}</strong> ≈ Direct English loanword <strong>"{cog}"</strong> used in daily spoken Hindi → <em>{target_disp}</em>!'
    return None

def build_hi_hook_for_sense(card_num, card_word, sense_label, hn_val):
    nk = normalize_key(hn_val)
    w_low = card_word.lower()
    lbl_low = (sense_label or "").lower()
    ctx = f"{w_low} {lbl_low}"

    if nk == "no direct word (dropped in hindi)":
        return '<strong>Dropped in Hindi</strong> ≈ Hindi has no separate word for <strong>"The"</strong> → Simply say the noun directly (e.g., <em>Kitaab</em> = The book) = <em>The (Dropped in Hindi)</em>!'
    if "zamaanat" in nk and ("bail" in ctx or "custody" in ctx):
        return '<strong>Zamaanat</strong> ≈ <strong>Spoken Tamil ஜாமீன் (Jaameen / Zamaanat = Court Bail!)</strong> | <strong>Hiraasat</strong> ≈ Police custody/detention = <em>Bail (Zamaanat) / Custody (Hiraasat)</em>!'
    if "maali haalat" in nk:
        return '<strong>Arthvyavastha</strong> ≈ <strong>Arth</strong> (Wealth) + <strong>Vyavastha</strong> (System = <em>Economy</em>) | <strong>Maali haalat</strong> ≈ <strong>Maal</strong> (Money/Wealth) + <strong>Haalat</strong> (Condition = <em>Financial state</em>)!'
    if "saamaan" in nk and ("product" in ctx or "service" in ctx):
        return '<strong>Utpaad / Saamaan</strong> ≈ <strong>Utpaad</strong> (<strong>Tamil உற்பத்தி = Manufactured Product</strong>) & <strong>Saamaan</strong> (<strong>Tamil சாமான் = Goods</strong>) | <strong>Seva</strong> ≈ <strong>Tamil சேவை (Sevai = Service!)</strong> = <em>Product & Service</em>!'
    if "kothri" in nk and "cell" in ctx:
        return '<strong>Koshika</strong> ≈ Biological body cell | <strong>Kothri</strong> ≈ Small enclosed prison lockup room = <em>Cell (Koshika / Kothri)</em>!'
    if "tang karna" in nk and "harass" in ctx:
        return '<strong>Prataadit karna</strong> ≈ Torment/oppress | <strong>Tang karna</strong> ≈ Pester, trouble, and harass someone = <em>Harass / Bully (Tang karna)</em>!'
    if "kalpana karna" in nk and ("assume" in ctx or "presume" in ctx):
        return '<strong>Maan lena</strong> ≈ Accept or suppose as true without proof | <strong>Kalpana karna</strong> ≈ <strong>Tamil கற்பனை (Karpanai = Suppose in mind)</strong> = <em>Assume / Presume (Maan lena)</em>!'
    if "dhokha" in nk and ("illusion" in ctx or "hallucination" in ctx):
        return '<strong>Bhram / Aabhaas</strong> ≈ <strong>Tamil பிரமை (Bhiramai = Mental Illusion!)</strong> | <strong>Dhokha</strong> ≈ Optical trick of the eyes (<em>Aankhon ka dhokha</em>) = <em>Illusion / Hallucination (Bhram)</em>!'
    if "sinchai" in nk:
        return '<strong>Sinchai</strong> ≈ From <strong>Seench-na</strong> (to water/sprinkle crops) → Supplying water to farmland through canals = <em>Irrigation (Sinchai)</em>!'
    if "keechad" in nk and "clay" in ctx:
        return '<strong>Chikni mitti</strong> ≈ <strong>Chikni</strong> (Smooth/Slippery) + <strong>Mitti</strong> (Earth/Clay) | <strong>Keechad</strong> ≈ Wet sticky mud = <em>Clay (Chikni mitti) / Mud (Keechad)</em>!'

    full_match = lookup_single_hi(hn_val, card_word, sense_label)
    raw_tokens = [t.strip() for t in re.split(r'\s*/\s*', hn_val) if t.strip()]
    tokens = filter_distinct_synonyms(raw_tokens)

    if len(tokens) > 1:
        sub_hooks = []
        for t in tokens:
            sh = lookup_single_hi(t, card_word, sense_label)
            if sh and sh not in sub_hooks:
                sub_hooks.append(sh)
        if sub_hooks:
            return " | ".join(sub_hooks[:2])

    if len(tokens) == 1 and len(raw_tokens) > 1:
        for rt in raw_tokens:
            single_h = lookup_single_hi(rt, card_word, sense_label)
            if single_h:
                return single_h

    if full_match:
        return full_match

    if DRY_RUN:
        UNMATCHED_HI.append((card_num, card_word, sense_label, hn_val))
        return f"MISSING_HI:{hn_val}"
    raise ValueError(f"Unmatched HI sense on #{card_num} {card_word}: {hn_val}")

def build_full_card_shortcuts(card):
    num = card["num"]
    word = card["word"]
    es_trans = card["trans"]["es"]
    hi_trans = card["trans"]["hi"]

    es_parts = [p.strip() for p in es_trans.split("|") if p.strip()]
    hi_parts = [p.strip() for p in hi_trans.split("|") if p.strip()]

    es_out = []
    for p in es_parts:
        lbl, val = split_sense_line(p)
        h = build_es_hook_for_sense(num, word, lbl, val)
        if lbl:
            es_out.append(f"{lbl}: {h}")
        else:
            es_out.append(h)

    hi_out = []
    for p in hi_parts:
        lbl, val = split_sense_line(p)
        h = build_hi_hook_for_sense(num, word, lbl, val)
        if lbl:
            hi_out.append(f"{lbl}: {h}")
        else:
            hi_out.append(h)

    shortcut_es = "<br>".join(es_out)
    shortcut_hi = "<br>".join(hi_out)

    # Preserve user's explicit manual gold-standard edits on 1363, 1364, 1365
    if num in user_custom_overrides:
        ov = user_custom_overrides[num]
        if ov.get("shortcutEs"):
            shortcut_es = strip_devanagari(ov["shortcutEs"])
        if ov.get("shortcutHi"):
            shortcut_hi = strip_devanagari(ov["shortcutHi"])

    return shortcut_es, shortcut_hi

deck_names = [
    "split1DeckCards",
    "split2DeckCards",
    "split5DeckCards",
    "split6DeckCards",
    "split7DeckCards",
    "split8DeckCards",
]

all_decks = {}
for dname in deck_names:
    m = re.search(r'(?:var|const|let)\s+' + dname + r'\s*=\s*(\[[^\n]*?\]);', html)
    assert m, f"Could not find {dname} in index.html"
    all_decks[dname] = json.loads(m.group(1))

# Update split1DeckCards (1..439) from parsed_split1
for card in all_decks["split1DeckCards"]:
    num = card["num"]
    assert num in parsed_split1, f"Card {num} missing from parsed_split1"
    p_entry = parsed_split1[num]
    card["word"] = p_entry["word"]
    es_str, hi_str = format_trans_from_senses(p_entry["senses"])
    card["trans"]["es"] = es_str
    card["trans"]["hi"] = hi_str
    card["hiDevanagari"] = hi_str
    if "hiDevanagari" in card.get("trans", {}):
        card["trans"]["hiDevanagari"] = ""

# Update split2DeckCards (440..821) from parsed_split2
for card in all_decks["split2DeckCards"]:
    num = card["num"]
    assert num in parsed_split2, f"Card {num} missing from parsed_split2"
    p_entry = parsed_split2[num]
    card["word"] = p_entry["word"]
    es_str, hi_str = format_trans_from_senses(p_entry["senses"])
    card["trans"]["es"] = es_str
    card["trans"]["hi"] = hi_str
    card["hiDevanagari"] = hi_str
    if "hiDevanagari" in card.get("trans", {}):
        card["trans"]["hiDevanagari"] = ""

# Update split5DeckCards (822..1093) and split6DeckCards (1094..1262) from parsed_part2
for dname_p2 in ("split5DeckCards", "split6DeckCards"):
    for card in all_decks[dname_p2]:
        num = card["num"]
        assert num in parsed_part2, f"Card {num} missing from parsed_part2"
        p_entry = parsed_part2[num]
        card["word"] = p_entry["word"]
        es_str, hi_str = format_trans_from_senses(p_entry["senses"])
        card["trans"]["es"] = es_str
        card["trans"]["hi"] = hi_str
        card["hiDevanagari"] = hi_str
        if "hiDevanagari" in card.get("trans", {}):
            card["trans"]["hiDevanagari"] = ""

# Update split7DeckCards (1263..1362) and split8DeckCards (1363..1446) from parsed_part3
for dname_p3 in ("split7DeckCards", "split8DeckCards"):
    for card in all_decks[dname_p3]:
        num = card["num"]
        assert num in parsed_part3, f"Card {num} missing from parsed_part3"
        p_entry = parsed_part3[num]
        card["word"] = p_entry["word"]
        es_str, hi_str = format_trans_from_senses(p_entry["senses"])
        card["trans"]["es"] = es_str
        card["trans"]["hi"] = hi_str
        card["hiDevanagari"] = hi_str
        if "hiDevanagari" in card.get("trans", {}):
            card["trans"]["hiDevanagari"] = ""

all_cards_flat = []
card_shortcuts_map = {}

for dname in deck_names:
    for card in all_decks[dname]:
        num = card["num"]
        card["trans"]["es"] = fix_existing_trans_colons(card["trans"]["es"])
        card["trans"]["hi"] = fix_existing_trans_colons(card["trans"]["hi"])
        card["hiDevanagari"] = card["trans"]["hi"]
        if "hiDevanagari" in card.get("trans", {}):
            card["trans"]["hiDevanagari"] = ""

        if num in user_custom_overrides:
            ov = user_custom_overrides[num]
            if ov.get("es"):
                card["trans"]["es"] = strip_devanagari(ov["es"])
            if ov.get("hi"):
                card["trans"]["hi"] = strip_devanagari(ov["hi"])
                card["hiDevanagari"] = card["trans"]["hi"]
            if ov.get("ta"):
                card["trans"]["ta"] = ov["ta"]

        sc_es, sc_hi = build_full_card_shortcuts(card)
        card["shortcutEs"] = sc_es
        card["shortcutHi"] = sc_hi
        card_shortcuts_map[str(num)] = {"es": sc_es, "hi": sc_hi}
        all_cards_flat.append(card)

print(f"Processed {len(all_cards_flat)} total cards across all 6 decks.")
assert len(all_cards_flat) == 1446, f"Expected 1446 total cards, got {len(all_cards_flat)}"

if DRY_RUN:
    with open("/tmp/unmatched_list.txt", "w", encoding="utf-8") as out:
        out.write(f"UNMATCHED_ES: {len(UNMATCHED_ES)}\n")
        for x in UNMATCHED_ES:
            out.write(f"  ES: {repr(x)}\n")
        out.write(f"UNMATCHED_HI: {len(UNMATCHED_HI)}\n")
        for x in UNMATCHED_HI:
            out.write(f"  HI: {repr(x)}\n")
    print(f"DRY_RUN DONE -> ES={len(UNMATCHED_ES)}, HI={len(UNMATCHED_HI)}")
    sys.exit(0)

bad_patterns = [
    "key spanish expression",
    "everyday spoken hindi",
    "essential vocabulary",
    "direct spanish term",
    "direct hindi term",
    "sound cue",
    "first syllable",
]

for c in all_cards_flat:
    num = c["num"]
    for field in ("shortcutEs", "shortcutHi"):
        val = c[field]
        assert val and len(val.strip()) > 10, f"Empty shortcut on #{num} {field}"
        low = val.lower()
        for bp in bad_patterns:
            assert bp not in low, f"Forbidden generic pattern '{bp}' found on #{num} {c['word']} ({field}): {val}"
        assert "!!" not in val and "!)!" not in val, f"Double punctuation found on #{num} {field}: {val}"
        assert not re.search(r'[\u0900-\u0B7F\u0C00-\u0D7F]', val), f"Stray Indic/Devanagari found in #{num} {field}: {val}"
    for tfield in ("es", "hi"):
        tval = c["trans"][tfield]
        assert not re.search(r'[\u0900-\u0B7F\u0C00-\u0D7F]', tval), f"Stray Indic/Devanagari found in #{num} trans.{tfield}: {tval}"
        for part in tval.split("|"):
            part = part.strip()
            if re.match(r'^\d+\.\s+', part):
                assert part.count(":") == 1, f"Multiple colons still in #{num} trans.{tfield}: {part}"

print("STRICT AUDIT PASSED: 0 generic patterns, 0 Devanagari, 0 colon bugs across all 1,446 cards!")

for dname in deck_names:
    serialized = json.dumps(all_decks[dname], ensure_ascii=False)
    pattern = r'(?:var|const|let)\s+' + dname + r'\s*=\s*\[[^\n]*?\];'
    replacement = f"var {dname} = {serialized};"
    html, count = re.subn(pattern, lambda _: replacement, html, count=1)
    assert count == 1, f"Failed to replace {dname} in index.html"

if "cardShortcuts =" in html:
    sc_serialized = json.dumps(card_shortcuts_map, ensure_ascii=False)
    html, sc_count = re.subn(
        r'(?:var|const|let)\s+cardShortcuts\s*=\s*\{[^\n]*?\};',
        lambda _: f"var cardShortcuts = {sc_serialized};",
        html,
        count=1
    )
    print(f"Updated cardShortcuts in index.html (count={sc_count})")

old_split_trans = "const m = clean.match(/^([^:]+):\\s*(.+)$/);"
new_split_trans = "const m = clean.match(/^(.+):\\s*(.+)$/);"

if old_split_trans in html:
    html = html.replace(old_split_trans, new_split_trans)
    print("Updated splitTrans in index.html")

old_speech_re = 's = s.replace(/^[^:]+:\\s*/, "");'
new_speech_re = 's = s.replace(/^.+:\\s*/, "");'
if old_speech_re in html:
    html = html.replace(old_speech_re, new_speech_re)
    print("Updated cleanTextForSpeech colon regex in index.html")

html, k_count = re.subn(
    r'(?:var|const|let)\s+STORAGE_KEY_EDITS\s*=\s*"sequential_vocab_user_custom_edits_v\d+";',
    'var STORAGE_KEY_EDITS = "sequential_vocab_user_custom_edits_v18";',
    html
)
assert k_count >= 1, "Failed to bump STORAGE_KEY_EDITS"
print(f"Bumped STORAGE_KEY_EDITS to v18 (count={k_count})")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

backup_obj = {}
for c in all_cards_flat:
    backup_obj[str(c["num"])] = c
with open("data/backup_original_cards.json", "w", encoding="utf-8") as f:
    json.dump(backup_obj, f, ensure_ascii=False, indent=2)
print("Updated data/backup_original_cards.json")
