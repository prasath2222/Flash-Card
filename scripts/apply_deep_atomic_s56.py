import json, re, html, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from atomic_data_s5a import DATA_S5A
from atomic_data_s5b import DATA_S5B
from atomic_data_s6 import DATA_S6

ALL_UPDATES = {}
ALL_UPDATES.update(DATA_S5A)
ALL_UPDATES.update(DATA_S5B)
ALL_UPDATES.update(DATA_S6)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(ROOT, "index.html")
BACKUP_PATH = os.path.join(ROOT, "data", "backup_original_cards.json")

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    src = f.read()

def extract_json_var(text, var_name):
    m = re.search(rf'(const|var|let)\s+{re.escape(var_name)}\s*=\s*', text)
    if not m:
        raise RuntimeError(f"Could not find {var_name}")
    start = m.end()
    ch = text[start]
    assert ch in "[{", f"Unexpected start {ch} for {var_name}"
    depth = 0
    in_str = False
    esc = False
    end_idx = None
    for i in range(start, len(text)):
        c = text[i]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
        else:
            if c == '"':
                in_str = True
            elif c in "[{":
                depth += 1
            elif c in "]}":
                depth -= 1
                if depth == 0:
                    end_idx = i + 1
                    break
    assert end_idx is not None
    return start, end_idx, json.loads(text[start:end_idx])

# 1. Update split5DeckCards
s5_s, s5_e, s5 = extract_json_var(src, "split5DeckCards")
s5_updated = 0
for c in s5:
    n = c["num"]
    if n in ALL_UPDATES:
        c["shortcutEs"], c["shortcutHi"] = ALL_UPDATES[n]
        s5_updated += 1

# 2. Update split6DeckCards
s6_s, s6_e, s6 = extract_json_var(src, "split6DeckCards")
s6_updated = 0
for c in s6:
    n = c["num"]
    if n in ALL_UPDATES:
        c["shortcutEs"], c["shortcutHi"] = ALL_UPDATES[n]
        s6_updated += 1

# 3. Update cardShortcuts
cs_s, cs_e, cs = extract_json_var(src, "cardShortcuts")
cs_updated = 0
for n, (es_sc, hi_sc) in ALL_UPDATES.items():
    k = str(n)
    if k in cs:
        cs[k]["es"] = es_sc
        cs[k]["hi"] = hi_sc
        cs_updated += 1

# Splice right-to-left by offset so indices never shift
slices = [
    (s5_s, s5_e, json.dumps(s5, ensure_ascii=False)),
    (s6_s, s6_e, json.dumps(s6, ensure_ascii=False)),
    (cs_s, cs_e, json.dumps(cs, ensure_ascii=False)),
]
slices.sort(key=lambda x: x[0], reverse=True)
new_src = src
for a, b, rep in slices:
    new_src = new_src[:a] + rep + new_src[b:]

# 4. Strengthen isStaleTemplateShortcut so stale Turn 11 glosses/cached versions auto-heal
stale_marker = 'str.includes("Tamil Dosham (தோஷம்) = Hindi Dosh dena") ||'
new_stale_checks = '''str.includes("Tamil Dosham (தோஷம்) = Hindi Dosh dena") ||
          str.includes("Kay-Harsh-Say") ||
          str.includes("(Grumble!)") ||
          str.includes("(Confess!)") ||
          str.includes("(Spill truth!)") ||
          str.includes("(Stick a charge onto!)") ||
          str.includes("(Accept truth!)") ||
          str.includes("(Flatly refuse!)") ||
          str.includes("(Back out denying!)") ||'''
if "Kay-Harsh-Say" not in new_src:
    assert stale_marker in new_src, "stale marker not found"
    new_src = new_src.replace(stale_marker, new_stale_checks, 1)

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(new_src)

# 5. Update backup_original_cards.json
with open(BACKUP_PATH, "r", encoding="utf-8") as f:
    bk = json.load(f)

bk_updated = 0
for k, v in bk.items():
    n = v.get("num") or v.get("originalNum")
    if n in ALL_UPDATES:
        v["shortcutEs"], v["shortcutHi"] = ALL_UPDATES[n]
        bk_updated += 1

with open(BACKUP_PATH, "w", encoding="utf-8") as f:
    json.dump(bk, f, ensure_ascii=False, indent=2)

print(f"Updated counts -> split5: {s5_updated}, split6: {s6_updated}, cardShortcuts: {cs_updated}, backup: {bk_updated}")

# 6. Exhaustive Audit on ALL 441 cards (#822-#1262)
all441 = s5 + s6
assert len(all441) == 441, f"Expected 441 cards, got {len(all441)}"

def clean_tok(t):
    t = re.sub(r'\([^)]*\)', '', t).strip()
    t = re.sub(r'^\d+\.\s*[^:]+:\s*', '', t).strip()
    return t.lower()

def strict_seg_ok(seg_html):
    txt = html.unescape(re.sub(r"<[^>]+>", "", seg_html)).strip()
    low = txt.lower()
    for bad_phrase in ["direct match", "direct sibling", "direct english", "core spanish recall", "everyday spoken hindi"]:
        if bad_phrase in low:
            return f"banned phrase '{bad_phrase}'"
    if "(grumble!)" in low or "(confess!)" in low or "(stick a charge" in low or "(accept truth!)" in low:
        return "bare gloss leftover"
    if any(k in low for k in [
        "≈", "tamil ", "arabic", "sanskrit", "latin", "french", "greek", "persian",
        "english", "origin", "root", "twin of", "sibling of", "phonetic", "sounds like",
        "rhymes", "from ", "literally", "echoes", "acronym", "idiom", "compound",
        "built on", "built directly", "pair with", "localized", "slang", "carib",
        "aztec", "scottish", "pushkar", "jaadu", "bagheera", "gandhian", "shayar",
        "bollywood", "urdu", "hinglish", "cid "
    ]):
        return None
    if "+" in txt or re.search(r'"[^"]{2,}"', txt) or re.search(r'\b[A-Za-z]+-[a-z]+\b', txt):
        return None
    return f"no atomic hook in: {txt}"

issues = []
for c in all441:
    n = c["num"]
    # Check <br> counts
    es_senses = len([s for s in c["trans"]["es"].split(" | ") if re.match(r'^\d+\.', s.strip())])
    hi_senses = len([s for s in c["trans"]["hi"].split(" | ") if re.match(r'^\d+\.', s.strip())])
    if es_senses > 1:
        br_es = c["shortcutEs"].count("<br>") + 1
        if br_es != es_senses:
            issues.append((n, f"ES <br> count {br_es} != senses {es_senses}"))
    if hi_senses > 1:
        br_hi = c["shortcutHi"].count("<br>") + 1
        if br_hi != hi_senses:
            issues.append((n, f"HI <br> count {br_hi} != senses {hi_senses}"))

    # Check Devanagari in Tamil
    if re.search(r'[\u0900-\u097F]', c["tamil"]):
        issues.append((n, "Devanagari in tamil"))

    # Check strict hook presence per segment
    for field in ("shortcutEs", "shortcutHi"):
        val = c[field]
        if "))" in re.sub(r"<[^>]+>", "", val):
            issues.append((n, f"double paren in {field}"))
        for line in val.split("<br>"):
            parts = [p.strip() for p in (line.split(" | ") if field == "shortcutEs" else re.split(r'\s*/\s*(?=<strong>)', line)) if p.strip()]
            for p in parts:
                err = strict_seg_ok(p)
                if err:
                    issues.append((n, f"{field}: {err}"))

    # Check synonym coverage in shortcut text
    es_sc_low = html.unescape(re.sub(r"<[^>]+>", "", c["shortcutEs"])).lower()
    hi_sc_low = html.unescape(re.sub(r"<[^>]+>", "", c["shortcutHi"])).lower()
    for sense in c["trans"]["es"].split(" | "):
        body = re.sub(r'^\d+\.\s*[^:]+:\s*', '', sense).strip()
        for syn in body.split(" / "):
            w = clean_tok(syn)
            if w and w not in es_sc_low:
                # check singular base before (a) etc.
                w2 = w.split("(")[0].strip()
                if w2 and w2 not in es_sc_low:
                    issues.append((n, f"Missing ES syn '{w}'"))
    for sense in c["trans"]["hi"].split(" | "):
        body = re.sub(r'^\d+\.\s*[^:]+:\s*', '', sense).strip()
        for syn in body.split(" / "):
            w = clean_tok(syn)
            if w and w not in hi_sc_low:
                issues.append((n, f"Missing HI syn '{w}'"))

print(f"Total audit issues: {len(issues)}")
for it in issues[:60]:
    print(" ", it)
if issues:
    sys.exit(1)
print("ALL 441 CARDS PASSED 100% STRICT ATOMIC AUDIT!")
