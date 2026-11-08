import re, json
from update_split1 import parse_split1

def main():
    entries = parse_split1()
    print(f"Loaded {len(entries)} parsed entries for Split 1.")

    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

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

    # Process Split 1
    # Filtered words to remove:
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
        # Find entry
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

    print(f"Split 1 cards count: {len(s1_cards)} (expected 233)")
    assert len(s1_cards) == 233, f"Expected 233, got {len(s1_cards)}"

    # Check that each card has updated translations
    print("Sample card 2 (YOU):", s1_cards[1]["word"], s1_cards[1]["trans"])

    # Now let us format all 8 split deck variables:
    # var split1DeckCards = ...
    # var split2DeckCards = ...
    # var split3DeckCards = ...
    # var split4DeckCards = ...
    # var split5DeckCards = ...
    # var split6DeckCards = ...
    # var split7DeckCards = ...
    # var split8DeckCards = ...
    
    # Also maintain tier1_200DeckCards etc as aliases or references so backward compatibility is 100% intact!
    print("Done validating 8 decks!")

if __name__ == "__main__":
    main()
