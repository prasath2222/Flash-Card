import json
import re
from scripts.apply_part1_and_part2_splits import parse_split_file, sync_card_shortcuts


def main():
    print("Reading index.html...")
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    pos = html.find("var split8DeckCards = [")
    if pos == -1:
        raise RuntimeError("split8DeckCards not found in index.html")
    end = html.find("];", pos)
    s8 = json.loads(html[pos + len("var split8DeckCards = ") : end + 1])

    p8_map = parse_split_file(
        "public/assets/aistudio/Paste_November_08__2026_-_7_40PM_a38c61dd"
    )
    print(f"Parsed {len(p8_map)} entries from Split 8 specification.")

    new_s8 = []
    for c in s8:
        w = c["word"].strip().upper()
        if w not in p8_map:
            continue
        spec = p8_map[w]
        c["trans"]["hi"] = spec["hi"]
        c["trans"]["es"] = spec["es"]
        sync_card_shortcuts(c)
        new_s8.append(c)

    print(f"Split 8 updated: {len(new_s8)} cards (expected 478)")
    assert len(new_s8) == 478, f"Expected 478, got {len(new_s8)}"

    new_s8_line = f"var split8DeckCards = {json.dumps(new_s8, ensure_ascii=False)};"
    html = html[:pos] + new_s8_line + html[end + 2 :]

    # Update tier-2501 word count badge & stat line
    html = re.sub(
        r'(<strong id="tier-2501-total-words">)\d+(</strong>)',
        rf"\g<1>{len(new_s8)}\g<2>",
        html,
    )
    html = re.sub(
        r'(<span id="tier-2501-stat-line"[^>]*>0 / )\d+( Learned</span>)',
        rf"\g<1>{len(new_s8)}\g<2>",
        html,
    )

    html = html.replace(
        'var STORAGE_KEY_EDITS = "sequential_vocab_user_custom_edits_v15";',
        'var STORAGE_KEY_EDITS = "sequential_vocab_user_custom_edits_v16";',
    )

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    # Sync backup_original_cards.json
    try:
        with open("data/backup_original_cards.json", "r", encoding="utf-8") as f:
            bkp = json.load(f)
        by_num = {c.get("originalNum") or c.get("num"): c for c in new_s8}
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

    print("Successfully updated Split 8 in index.html and backup_original_cards.json!")


if __name__ == "__main__":
    main()
