import json
import re
from scripts.apply_part1_and_part2_splits import sync_card_shortcuts

FILE_PART3 = "public/assets/aistudio/Paste_November_11__2026_-_8_59PM_4029e095"


def parse_part3_paste_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    joined = []
    cur = ""
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if s.startswith("Part 3 (Words"):
            if cur:
                joined.append(cur)
                cur = ""
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
        # Special case: 1355. BALL GAMES [Football / Cricket / Tennis]
        if clean_word == "BALL GAMES":
            clean_word = "BALL GAMES (FOOTBALL / CRICKET / TENNIS)"
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


def resolve_base_card(clean_word, raw_word, pool_by_word):
    if clean_word in pool_by_word:
        return pool_by_word[clean_word]
    no_paren = re.sub(r"\s*\([^)]*\)", "", clean_word).strip()
    if no_paren in pool_by_word:
        return pool_by_word[no_paren]
    parts = [p.strip() for p in no_paren.split("/") if p.strip()]
    for p in parts:
        if p in pool_by_word:
            return pool_by_word[p]
        if p.endswith("S") and p[:-1] in pool_by_word:
            return pool_by_word[p[:-1]]
    # Also check bracketed or parenthesized tokens (e.g., [Football / Cricket / Tennis])
    extra_tokens = re.findall(r"[A-Za-z]+", raw_word.upper())
    for tok in extra_tokens:
        if tok in pool_by_word:
            return pool_by_word[tok]
    return None


def main():
    all_items = parse_part3_paste_file(FILE_PART3)
    items_2001_2500 = [x for x in all_items if 1263 <= x["num"] <= 1362]
    items_2501_3000 = [x for x in all_items if 1363 <= x["num"] <= 1446]
    print(
        f"Parsed {len(items_2001_2500)} items for Split 2001-2500 (1263..1362) and "
        f"{len(items_2501_3000)} items for Split 2501-3000 (1363..1446) -> Total {len(all_items)} items."
    )
    assert len(items_2001_2500) == 100
    assert len(items_2501_3000) == 84

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
    # First populate from backup (all cards, prioritizing 2001-3000)
    for c in bkp_items:
        if not isinstance(c, dict):
            continue
        w = c.get("word", "").strip().upper()
        if w and w not in pool_by_word:
            pool_by_word[w] = dict(c)
    for c in bkp_items:
        if not isinstance(c, dict):
            continue
        try:
            n = int(c.get("originalNum") or c.get("num") or 0)
        except (ValueError, TypeError):
            n = 0
        if 2001 <= n <= 3000:
            w = c.get("word", "").strip().upper()
            if w:
                pool_by_word[w] = dict(c)

    # Also populate from existing s1..s8 (prioritizing s7, s8)
    for c in s1 + s2 + s3 + s4 + s5 + s6 + s7 + s8:
        w = c.get("word", "").strip().upper()
        if w:
            pool_by_word[w] = dict(c)
            for sub in [p.strip() for p in re.sub(r"\s*\([^)]*\)", "", w).split("/") if p.strip()]:
                if sub not in pool_by_word:
                    pool_by_word[sub] = dict(c)

    missing = []
    for item in all_items:
        base = resolve_base_card(item["word"], item["raw_word"], pool_by_word)
        if not base:
            missing.append((item["num"], item["word"]))
    if missing:
        print("Missing base cards:", missing)
        raise RuntimeError(f"Missing {len(missing)} base cards!")

    built_cards = []
    for item in all_items:
        num = item["num"]
        w = item["word"]
        base = resolve_base_card(w, item["raw_word"], pool_by_word)
        card = json.loads(json.dumps(base))
        id_prefix = "t2001" if num <= 1362 else "t2501"
        card["id"] = f"{id_prefix}_{num}"
        card["num"] = num
        card["originalNum"] = num
        card["displayNum"] = num
        card["word"] = w
        card["trans"] = {"es": item["es"], "hi": item["hi"]}

        if "/" in w:
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

    deck_2001_2500 = [c for c in built_cards if c["num"] <= 1362]
    deck_2501_3000 = [c for c in built_cards if c["num"] >= 1363]
    assert len(deck_2001_2500) == 100
    assert len(deck_2501_3000) == 84

    # Replace split1DeckCards .. split8DeckCards block in index.html
    start_s1 = html.find("var split1DeckCards = [")
    _, _, end_s8 = get_deck("split8DeckCards")

    new_decks_block = "\n".join(
        [
            f"var split1DeckCards = {json.dumps(s1, ensure_ascii=False)};",
            f"var split2DeckCards = {json.dumps(s2, ensure_ascii=False)};",
            "var split3DeckCards = [];",
            "var split4DeckCards = [];",
            f"var split5DeckCards = {json.dumps(s5, ensure_ascii=False)};",
            f"var split6DeckCards = {json.dumps(s6, ensure_ascii=False)};",
            f"var split7DeckCards = {json.dumps(deck_2001_2500, ensure_ascii=False)};",
            f"var split8DeckCards = {json.dumps(deck_2501_3000, ensure_ascii=False)};",
        ]
    )
    html = html[:start_s1] + new_decks_block + html[end_s8:]

    # Also sync cardAccurateImages in index.html and scripts/accurate_images.json
    all_active_cards = s1 + s2 + s5 + s6 + deck_2001_2500 + deck_2501_3000
    new_acc = {}
    for c in all_active_cards:
        img = c.get("img", "")
        if img:
            new_acc[str(c["num"])] = img
            new_acc[c["word"]] = img

    with open("scripts/accurate_images.json", "w", encoding="utf-8") as f:
        json.dump(new_acc, f, ensure_ascii=False, indent=2)

    acc_pos = html.find("var cardAccurateImages = {")
    if acc_pos != -1:
        acc_end = html.find("};", acc_pos)
        if acc_end != -1:
            html = (
                html[:acc_pos]
                + f"var cardAccurateImages = {json.dumps(new_acc, ensure_ascii=False)};"
                + html[acc_end + 2 :]
            )

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print(
        f"Updated split7DeckCards ({len(deck_2001_2500)} cards) and "
        f"split8DeckCards ({len(deck_2501_3000)} cards) in index.html! "
        f"Total active cards across all 6 splits: {len(all_active_cards)}"
    )


if __name__ == "__main__":
    main()
