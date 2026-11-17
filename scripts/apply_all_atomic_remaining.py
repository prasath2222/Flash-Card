import json, re, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from atomic_data_s1a import DATA_S1A
from atomic_data_s1b import DATA_S1B
from atomic_data_s2 import DATA_S2
from atomic_data_s7 import DATA_S7
from atomic_data_s8 import DATA_S8
from atomic_data_s5b import DATA_S5B
from atomic_data_polish_s156 import DATA_POLISH

ALL_UPDATES = {}
for d in (DATA_S1A, DATA_S1B, DATA_S2, DATA_S5B, DATA_S7, DATA_S8, DATA_POLISH):
    ALL_UPDATES.update(d)

print(f"Loaded {len(ALL_UPDATES)} atomic card updates.")

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

slices = []
counts = {}
for var_name in ("split1DeckCards", "split2DeckCards", "split5DeckCards", "split6DeckCards", "split7DeckCards", "split8DeckCards"):
    a, b, arr = extract_json_var(src, var_name)
    updated = 0
    for c in arr:
        n = c["num"]
        if n in ALL_UPDATES:
            c["shortcutEs"], c["shortcutHi"] = ALL_UPDATES[n]
            updated += 1
    counts[var_name] = updated
    slices.append((a, b, json.dumps(arr, ensure_ascii=False)))

cs_a, cs_b, cs = extract_json_var(src, "cardShortcuts")
cs_updated = 0
for n, (es_sc, hi_sc) in ALL_UPDATES.items():
    k = str(n)
    if k in cs:
        cs[k]["es"] = es_sc
        cs[k]["hi"] = hi_sc
        cs_updated += 1
slices.append((cs_a, cs_b, json.dumps(cs, ensure_ascii=False)))

slices.sort(key=lambda x: x[0], reverse=True)
new_src = src
for a, b, rep in slices:
    new_src = new_src[:a] + rep + new_src[b:]

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(new_src)

print("Updated index.html:", counts, "cardShortcuts:", cs_updated)

if os.path.exists(BACKUP_PATH):
    with open(BACKUP_PATH, "r", encoding="utf-8") as f:
        backup = json.load(f)
    bk_updated = 0
    items = backup.values() if isinstance(backup, dict) else backup
    for c in items:
        n = c.get("num") or c.get("originalNum")
        if n in ALL_UPDATES:
            c["shortcutEs"], c["shortcutHi"] = ALL_UPDATES[n]
            bk_updated += 1
    with open(BACKUP_PATH, "w", encoding="utf-8") as f:
        json.dump(backup, f, ensure_ascii=False, indent=2)
    print(f"Updated {BACKUP_PATH}: {bk_updated} cards")
