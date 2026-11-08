import re, json
from update_split1 import parse_split1

def run():
    print("Reading index.html...")
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    entries = parse_split1()
    print(f"Loaded {len(entries)} entries for Split 1.")

    def get_deck(name):
        m = re.search(r"(?:var|const|let)\s+" + name + r"\s*=\s*(\[.*?\]);", html, re.S)
        if not m:
            raise Exception(f"Deck {name} not found!")
        return json.loads(m.group(1))

    t1_200 = get_deck("tier1_200DeckCards")
    t201 = get_deck("tier201DeckCards")
    t401 = get_deck("tier401DeckCards")
    t601 = get_deck("tier601DeckCards")
    t800 = get_deck("initialDeckCards")
    t1001 = get_deck("tier1001DeckCards")
    t1201 = get_deck("tier1201DeckCards")
    t1401 = get_deck("tier1401DeckCards")
    t1601 = get_deck("tier1601DeckCards")
    t1801 = get_deck("tier1801DeckCards")
    t2001 = get_deck("tier2001DeckCards")
    t2501 = get_deck("tier2501DeckCards")

    all_1_1000 = t1_200 + t201 + t401 + t601 + t800
    all_1001_2000 = t1001 + t1201 + t1401 + t1601 + t1801
    all_2001_3000 = t2001 + t2501

    raw_s1 = all_1_1000[:250]
    raw_s2 = all_1_1000[250:500]
    raw_s3 = all_1_1000[500:750]
    raw_s4 = all_1_1000[750:1000]

    raw_s5 = all_1001_2000[:500]
    raw_s6 = all_1001_2000[500:1000]

    raw_s7 = all_2001_3000[:500]
    raw_s8 = all_2001_3000[500:1000]

    filtered_out_set = {
        'SOMEBODY', 'EVERYBODY', 'NOBODY', 'AN', 'NEXT TO', 'THOUGH',
        'EVEN THOUGH', 'NORMALLY', 'FREQUENTLY', 'SELDOM', 'LATELY',
        'SWIPE', 'NEARLY', 'PARTICULARLY', 'AS WELL', 'PERHAPS', 'CERTAINLY'
    }

    s1_cards = []
    for card in raw_s1:
        w = card["word"].strip()
        w_upper = w.upper()
        if w_upper in filtered_out_set:
            continue
        if w_upper in entries:
            spec = entries[w_upper]
            card["trans"]["hi"] = spec["hi"]
            card["trans"]["es"] = spec["es"]
        elif w in entries:
            spec = entries[w]
            card["trans"]["hi"] = spec["hi"]
            card["trans"]["es"] = spec["es"]
        else:
            print(f"Warning: Word {w} not in entries!")
        s1_cards.append(card)

    print(f"s1_cards: {len(s1_cards)} (expected 233)")
    print(f"s2_cards: {len(raw_s2)} (expected 250)")
    print(f"s3_cards: {len(raw_s3)} (expected 250)")
    print(f"s4_cards: {len(raw_s4)} (expected 250)")
    print(f"s5_cards: {len(raw_s5)} (expected 500)")
    print(f"s6_cards: {len(raw_s6)} (expected 500)")
    print(f"s7_cards: {len(raw_s7)} (expected 500)")
    print(f"s8_cards: {len(raw_s8)} (expected 500)")

    return {
        "s1": s1_cards,
        "s2": raw_s2,
        "s3": raw_s3,
        "s4": raw_s4,
        "s5": raw_s5,
        "s6": raw_s6,
        "s7": raw_s7,
        "s8": raw_s8
    }

if __name__ == "__main__":
    run()
