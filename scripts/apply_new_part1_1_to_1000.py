import json
import re
from scripts.apply_part1_and_part2_splits import sync_card_shortcuts

FILE_1 = "public/assets/aistudio/Paste_November_10__2026_-_9_56PM_a3e39257"
FILE_2 = "public/assets/aistudio/Paste_November_10__2026_-_9_57PM_b5aa3988"


def parse_new_paste_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    joined = []
    cur = ""
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if re.match(r"^\d+\.\s+", s):
            if cur:
                joined.append(cur)
            cur = s
        else:
            if cur:
                cur += " " + s
    if cur:
        joined.append(cur)

    items = []
    for entry in joined:
        m = re.match(r"^(\d+)\.\s+(.+?)\s+—\s+(.+)$", entry)
        if not m:
            raise RuntimeError(f"Cannot parse entry: {entry}")
        num = int(m.group(1))
        raw_word = m.group(2).strip()
        clean_word = re.sub(r"\s*\[[^\]]*\]", "", raw_word).strip().upper()
        body = m.group(3).strip()
        body = re.sub(r"\s*\[[^\]]*\]", "", body).strip()

        if re.match(r"^1\.\s+", body):
            sense_chunks = [c.strip() for c in re.split(r";\s*(?=\d+\.\s+)", body) if c.strip()]
            es_parts = []
            hi_parts = []
            for sc in sense_chunks:
                sm = re.match(
                    r"^(\d+)\.\s*\(([^)]+)\):\s*Sp:\s*([^|]+)\|\s*Hn:\s*(.+)$",
                    sc,
                )
                if not sm:
                    sm = re.match(
                        r"^(\d+)\.\s*([^:]+):\s*Sp:\s*([^|]+)\|\s*Hn:\s*(.+)$",
                        sc,
                    )
                if not sm:
                    raise RuntimeError(f"Cannot parse sense '{sc}' in entry {num} ({clean_word})")
                s_idx = sm.group(1).strip()
                s_lbl = sm.group(2).strip()
                sp_val = sm.group(3).strip()
                hn_val = sm.group(4).strip()
                if sp_val:
                    sp_val = sp_val[0].upper() + sp_val[1:]
                if hn_val:
                    hn_val = hn_val[0].upper() + hn_val[1:]
                es_parts.append(f"{s_idx}. {s_lbl}: {sp_val}")
                hi_parts.append(f"{s_idx}. {s_lbl}: {hn_val}")
            es_str = " | ".join(es_parts)
            hi_str = " | ".join(hi_parts)
        else:
            sm = re.match(r"^Sp:\s*([^|]+)\|\s*Hn:\s*(.+)$", body)
            if not sm:
                raise RuntimeError(f"Cannot parse single-sense '{body}' in entry {num} ({clean_word})")
            sp_val = sm.group(1).strip()
            hn_val = sm.group(2).strip()
            if sp_val:
                sp_val = sp_val[0].upper() + sp_val[1:]
            if hn_val:
                hn_val = hn_val[0].upper() + hn_val[1:]
            es_str = sp_val
            hi_str = hn_val

        items.append(
            {
                "num": num,
                "word": clean_word,
                "raw_word": raw_word,
                "es": es_str,
                "hi": hi_str,
            }
        )
    return items


def resolve_base_card(clean_word, pool_by_word):
    if clean_word in pool_by_word:
        return pool_by_word[clean_word]
    no_paren = re.sub(r"\s*\([^)]*\)", "", clean_word).strip()
    if no_paren in pool_by_word:
        return pool_by_word[no_paren]
    parts = [p.strip() for p in no_paren.split("/") if p.strip()]
    for p in parts:
        if p in pool_by_word:
            return pool_by_word[p]
    if clean_word == "DAYS OF THE WEEK" and "MONDAY" in pool_by_word:
        return pool_by_word["MONDAY"]
    return None


def main():
    items1 = parse_new_paste_file(FILE_1)
    items2 = parse_new_paste_file(FILE_2)
    all_items = items1 + items2
    print(f"Parsed {len(items1)} from File 1 (1-500) and {len(items2)} from File 2 (501-1000) -> Total {len(all_items)} items.")
    assert len(items1) == 439
    assert len(items2) == 382

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

    with open("data/backup_original_cards.json", "r", encoding="utf-8") as f:
        bkp = json.load(f)

    pool_by_word = {}
    bkp_items = bkp.values() if isinstance(bkp, dict) else bkp
    for c in bkp_items:
        if not isinstance(c, dict):
            continue
        try:
            n = int(c.get("originalNum") or c.get("num") or 0)
        except (ValueError, TypeError):
            n = 0
        if 1 <= n <= 1000:
            w = c.get("word", "").strip().upper()
            if w and w not in pool_by_word:
                pool_by_word[w] = dict(c)
    for c in s1 + s2 + s3 + s4:
        w = c.get("word", "").strip().upper()
        if w:
            pool_by_word[w] = dict(c)
            for sub in [p.strip() for p in re.sub(r"\s*\([^)]*\)", "", w).split("/") if p.strip()]:
                if sub not in pool_by_word:
                    pool_by_word[sub] = dict(c)

    if "BLEED" not in pool_by_word and "BLOOD" in pool_by_word:
        bleed_card = json.loads(json.dumps(pool_by_word["BLOOD"]))
        bleed_card["word"] = "BLEED"
        bleed_card["emoji"] = "🩸"
        bleed_card["tamil"] = "இரத்தம் வடிதல்"
        bleed_card["ex"] = {
            "en": "Apply gentle pressure if the wound starts to bleed.",
            "es": "Aplica una presión suave si la herida empieza a sangrar.",
            "hi": "अगर घाव से खून बहने लगे तो हल्का दबाव डालें।",
            "ta": "காயத்திலிருந்து இரத்தம் வடியத் தொடங்கினால் மெதுவாக அழுத்தவும்.",
        }
        pool_by_word["BLEED"] = bleed_card

    built_cards = []
    for item in all_items:
        num = item["num"]
        w = item["word"]
        base = resolve_base_card(w, pool_by_word)
        if not base:
            raise RuntimeError(f"Missing base card for {num}: {w}")
        card = json.loads(json.dumps(base))
        id_prefix = "t1" if num <= 439 else "t501"
        card["id"] = f"{id_prefix}_{num}"
        card["num"] = num
        card["originalNum"] = num
        card["displayNum"] = num
        card["word"] = w
        card["trans"] = {"es": item["es"], "hi": item["hi"]}

        if w == "DAYS OF THE WEEK":
            card["tamil"] = "திங்கள், செவ்வாய், புதன், வியாழன், வெள்ளி, சனி, ஞாயிறு"
        elif "/" in w:
            parts = [p.strip() for p in re.sub(r"\s*\([^)]*\)", "", w).split("/") if p.strip()]
            ta_list = []
            for p in parts:
                if p in pool_by_word:
                    ta_p = pool_by_word[p].get("tamil", "").strip()
                    if ta_p and ta_p not in ta_list:
                        ta_list.append(ta_p)
            if len(ta_list) > 1:
                card["tamil"] = " / ".join(ta_list)

        sync_card_shortcuts(card)
        built_cards.append(card)

    # 2 splits of 500 for Section 1 (1-1000):
    # Split 1 (1-500): items 1..439 (439 cards)
    # Split 2 (501-1000): items 440..821 (382 cards)
    deck_1_500 = [c for c in built_cards if c["num"] <= 439]
    deck_501_1000 = [c for c in built_cards if c["num"] >= 440]
    assert len(deck_1_500) == 439
    assert len(deck_501_1000) == 382

    # Replace split1DeckCards .. split8DeckCards block in index.html
    start_s1 = html.find("var split1DeckCards = [")
    _, _, end_s8 = get_deck("split8DeckCards")

    new_decks_block = "\n".join(
        [
            f"var split1DeckCards = {json.dumps(deck_1_500, ensure_ascii=False)};",
            f"var split2DeckCards = {json.dumps(deck_501_1000, ensure_ascii=False)};",
            "var split3DeckCards = [];",
            "var split4DeckCards = [];",
            f"var split5DeckCards = {json.dumps(s5, ensure_ascii=False)};",
            f"var split6DeckCards = {json.dumps(s6, ensure_ascii=False)};",
            f"var split7DeckCards = {json.dumps(s7, ensure_ascii=False)};",
            f"var split8DeckCards = {json.dumps(s8, ensure_ascii=False)};",
        ]
    )
    html = html[:start_s1] + new_decks_block + html[end_s8:]

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Updated split1DeckCards (439 cards) and split2DeckCards (382 cards) in index.html!")


if __name__ == "__main__":
    main()
