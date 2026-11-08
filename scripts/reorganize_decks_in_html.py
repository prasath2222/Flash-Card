import re, json
from update_split1 import parse_split1

def main():
    print("Reading index.html...")
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    entries = parse_split1()
    print(f"Loaded {len(entries)} parsed entries for Split 1.")

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

    # Format JSON strings
    s1_json = json.dumps(s1_cards, ensure_ascii=False)
    s2_json = json.dumps(raw_s2, ensure_ascii=False)
    s3_json = json.dumps(raw_s3, ensure_ascii=False)
    s4_json = json.dumps(raw_s4, ensure_ascii=False)
    s5_json = json.dumps(raw_s5, ensure_ascii=False)
    s6_json = json.dumps(raw_s6, ensure_ascii=False)
    s7_json = json.dumps(raw_s7, ensure_ascii=False)
    s8_json = json.dumps(raw_s8, ensure_ascii=False)

    # Replace the existing deck declarations in index.html
    # Find the start of var initialDeckCards
    deck_start_match = re.search(r"var initialDeckCards\s*=\s*\[", html)
    if not deck_start_match:
        raise Exception("Cannot find start of deck declarations!")
    deck_start_idx = deck_start_match.start()

    # Find where tier2501DeckCards ends
    deck_end_match = re.search(r"var tier2501DeckCards\s*=\s*\[.*?\];", html, re.S)
    if not deck_end_match:
        raise Exception("Cannot find end of tier2501DeckCards!")
    deck_end_idx = deck_end_match.end()

    new_deck_decls = f"""var split1DeckCards = {s1_json};
var split2DeckCards = {s2_json};
var split3DeckCards = {s3_json};
var split4DeckCards = {s4_json};
var split5DeckCards = {s5_json};
var split6DeckCards = {s6_json};
var split7DeckCards = {s7_json};
var split8DeckCards = {s8_json};

// Legacy deck aliases for full backward compatibility
var initialDeckCards = split4DeckCards;
var tier800DeckCards = split4DeckCards;
var tier1DeckCards = split1DeckCards.slice(0, 100);
var tier101DeckCards = split1DeckCards.slice(100, 200);
var tier1_200DeckCards = split1DeckCards;
var tier201DeckCards = split2DeckCards;
var tier401DeckCards = split3DeckCards;
var tier601DeckCards = split3DeckCards;
var tier1001DeckCards = split5DeckCards;
var tier1201DeckCards = split5DeckCards;
var tier1401DeckCards = split5DeckCards;
var tier1601DeckCards = split6DeckCards;
var tier1801DeckCards = split6DeckCards;
var tier2001DeckCards = split7DeckCards;
var tier2501DeckCards = split8DeckCards;"""

    html = html[:deck_start_idx] + new_deck_decls + html[deck_end_idx:]

    # Update hydrateDeckArraysAndMaps allDecks
    hydrate_match = re.search(r"function hydrateDeckArraysAndMaps\(\)\s*\{.*?var allDecks\s*=\s*\[(.*?)\];", html, re.S)
    if hydrate_match:
        old_all_decks = hydrate_match.group(1)
        new_all_decks = """
          split1DeckCards,
          split2DeckCards,
          split3DeckCards,
          split4DeckCards,
          split5DeckCards,
          split6DeckCards,
          split7DeckCards,
          split8DeckCards
        """
        html = html[:hydrate_match.start(1)] + new_all_decks + html[hydrate_match.end(1):]

    # Update BUILT_IN_DECKS_META
    meta_match = re.search(r"const BUILT_IN_DECKS_META\s*=\s*\{.*?\n\s*\};", html, re.S)
    if not meta_match:
        raise Exception("Cannot find BUILT_IN_DECKS_META!")

    new_built_in_meta = """const BUILT_IN_DECKS_META = {
        "deck-1-250": { id: "deck-1-250", rangeGroup: "1-1000", title: "Split 1: Cards 1 – 250", startNum: 1, cards: split1DeckCards, prefix: "tier-1", subId: "sub-tier-1-250", pillId: "pill-tier-1", accent: "#10b981", borderIdle: "rgba(16, 185, 129, 0.42)", shadowActive: "0 12px 32px rgba(16, 185, 129, 0.28), 0 0 0 2px #10b981", shadowIdle: "0 8px 24px rgba(16, 185, 129, 0.14)" },
        "deck-251-500": { id: "deck-251-500", rangeGroup: "1-1000", title: "Split 2: Cards 251 – 500", startNum: 251, cards: split2DeckCards, prefix: "tier-251", subId: "sub-tier-251-500", pillId: "pill-tier-251", accent: "#f59e0b", borderIdle: "rgba(245, 158, 11, 0.42)", shadowActive: "0 12px 32px rgba(245, 158, 11, 0.28), 0 0 0 2px #f59e0b", shadowIdle: "0 8px 24px rgba(245, 158, 11, 0.14)" },
        "deck-501-750": { id: "deck-501-750", rangeGroup: "1-1000", title: "Split 3: Cards 501 – 750", startNum: 501, cards: split3DeckCards, prefix: "tier-501", subId: "sub-tier-501-750", pillId: "pill-tier-501", accent: "#ec4899", borderIdle: "rgba(236, 72, 153, 0.42)", shadowActive: "0 12px 32px rgba(236, 72, 153, 0.28), 0 0 0 2px #ec4899", shadowIdle: "0 8px 24px rgba(236, 72, 153, 0.14)" },
        "deck-751-1000": { id: "deck-751-1000", rangeGroup: "1-1000", title: "Split 4: Cards 751 – 1000", startNum: 751, cards: split4DeckCards, prefix: "tier-751", subId: "sub-tier-751-1000", pillId: "pill-tier-751", accent: "#38bdf8", borderIdle: "rgba(56, 189, 248, 0.45)", shadowActive: "0 12px 32px rgba(2, 132, 199, 0.28), 0 0 0 2px #38bdf8", shadowIdle: "0 8px 24px rgba(2, 132, 199, 0.16)" },
        "deck-1001-1500": { id: "deck-1001-1500", rangeGroup: "1001-2000", title: "Split 5: Cards 1001 – 1500", startNum: 1001, cards: split5DeckCards, prefix: "tier-1001", subId: "sub-tier-1001-1500", pillId: "pill-tier-1001", accent: "#6366f1", borderIdle: "rgba(99, 102, 241, 0.42)", shadowActive: "0 12px 32px rgba(99, 102, 241, 0.28), 0 0 0 2px #6366f1", shadowIdle: "0 8px 24px rgba(99, 102, 241, 0.14)" },
        "deck-1501-2000": { id: "deck-1501-2000", rangeGroup: "1001-2000", title: "Split 6: Cards 1501 – 2000", startNum: 1501, cards: split6DeckCards, prefix: "tier-1501", subId: "sub-tier-1501-2000", pillId: "pill-tier-1501", accent: "#0ea5e9", borderIdle: "rgba(14, 165, 233, 0.42)", shadowActive: "0 12px 32px rgba(14, 165, 233, 0.28), 0 0 0 2px #0ea5e9", shadowIdle: "0 8px 24px rgba(14, 165, 233, 0.14)" },
        "deck-2001-2500": { id: "deck-2001-2500", rangeGroup: "2001-3000", title: "Split 7: Cards 2001 – 2500", startNum: 2001, cards: split7DeckCards, prefix: "tier-2001", subId: "sub-tier-2001-2500", pillId: "pill-tier-2001", accent: "#10b981", borderIdle: "rgba(16, 185, 129, 0.45)", shadowActive: "0 12px 32px rgba(16, 185, 129, 0.28), 0 0 0 2px #10b981", shadowIdle: "0 8px 26px rgba(16, 185, 129, 0.15)" },
        "deck-2501-3000": { id: "deck-2501-3000", rangeGroup: "2001-3000", title: "Split 8: Cards 2501 – 3000", startNum: 2501, cards: split8DeckCards, prefix: "tier-2501", subId: "sub-tier-2501-3000", pillId: "pill-tier-2501", accent: "#3b82f6", borderIdle: "rgba(59, 130, 246, 0.45)", shadowActive: "0 12px 32px rgba(59, 130, 246, 0.28), 0 0 0 2px #3b82f6", shadowIdle: "0 8px 26px rgba(59, 130, 246, 0.15)" }
      };

      // Legacy aliases
      BUILT_IN_DECKS_META["deck-1-200"] = BUILT_IN_DECKS_META["deck-1-250"];
      BUILT_IN_DECKS_META["deck-201-400"] = BUILT_IN_DECKS_META["deck-251-500"];
      BUILT_IN_DECKS_META["deck-401-600"] = BUILT_IN_DECKS_META["deck-501-750"];
      BUILT_IN_DECKS_META["deck-601-800"] = BUILT_IN_DECKS_META["deck-501-750"];
      BUILT_IN_DECKS_META["deck-800-1000"] = BUILT_IN_DECKS_META["deck-751-1000"];
      BUILT_IN_DECKS_META["deck-1001-1200"] = BUILT_IN_DECKS_META["deck-1001-1500"];
      BUILT_IN_DECKS_META["deck-1201-1400"] = BUILT_IN_DECKS_META["deck-1001-1500"];
      BUILT_IN_DECKS_META["deck-1401-1600"] = BUILT_IN_DECKS_META["deck-1001-1500"];
      BUILT_IN_DECKS_META["deck-1601-1800"] = BUILT_IN_DECKS_META["deck-1501-2000"];
      BUILT_IN_DECKS_META["deck-1801-2000"] = BUILT_IN_DECKS_META["deck-1501-2000"];"""

    html = html[:meta_match.start()] + new_built_in_meta + html[meta_match.end():]

    # Update active_deck_id default
    html = re.sub(
        r'let currentDeckId = localStorage\.getItem\("active_deck_id_v1"\) \|\| "deck-800-1000";',
        'let currentDeckId = localStorage.getItem("active_deck_id_v1") || "deck-1-250"; if (BUILT_IN_DECKS_META[currentDeckId]) currentDeckId = BUILT_IN_DECKS_META[currentDeckId].id;',
        html
    )

    # Update subsection cards HTML in #subsections-tiers-container
    subsections_container_match = re.search(
        r'<div id="subsections-tiers-container">(.*?)<!-- Custom Uploaded Decks Dynamic Section -->',
        html,
        re.S
    )
    if not subsections_container_match:
        raise Exception("Cannot find subsections-tiers-container in HTML!")

    new_subsections_html = """<!-- Sortable & Movable Tiers Container -->
          <div id="subsections-tiers-container">
          <!-- SPLIT 1: Cards 1 – 250 (Core Foundations & Pronouns) -->
          <div class="tier-card-option tier-card-Sortable-item subsection-tier-card" id="sub-tier-1-250" data-deck-id="deck-1-250" data-range-group="1-1000" data-default-order="1" draggable="true" role="button" tabindex="0" style="margin-bottom: 16px; background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(15, 23, 42, 0.9)); border: 1.5px solid rgba(16, 185, 129, 0.42); box-shadow: 0 8px 24px rgba(16, 185, 129, 0.14); border-radius: 20px; padding: 22px 24px; cursor: pointer; transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px;">
              <div style="display: flex; align-items: center; gap: 16px;">
                <span style="display: flex; align-items: center; justify-content: center; width: 52px; height: 52px; border-radius: 14px; background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.1); font-size: 1.65rem;">👤</span>
                <div>
                  <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                    <span style="font-size: 0.72rem; font-weight: 800; letter-spacing: 0.08em; color: #34d399; text-transform: uppercase;">Section 1 (1–1000) · Split 1</span>
                    <span class="active-tier-pill" id="pill-tier-1" style="display: none; font-size: 0.66rem; font-weight: 800; background: #10b981; color: #ffffff; padding: 2px 8px; border-radius: 999px;">ACTIVE DECK</span>
                  </div>
                  <h3 style="font-size: 1.25rem; font-weight: 800; color: #ffffff; margin: 3px 0 4px;">Cards 1 – 250 (Core Foundations & Pronouns)</h3>
                  <div id="tier-1-words-sub" style="font-size: 0.84rem; color: #cbd5e1;">I, YOU, WE, THEY, WILL, MUST, MAY, BETWEEN, ALTHOUGH, TRULY · <strong id="tier-1-total-words">233</strong> Words</div>
                </div>
              </div>
              <div style="display: flex; align-items: center; gap: 10px;">
                <div class="sub-move-controls" title="Reorder deck">
                  <span class="sub-drag-handle" aria-label="Drag to reorder">⋮⋮</span>
                  <button type="button" class="sub-move-btn btn-sub-move-up" data-deck-id="deck-1-250" title="Move Up" aria-label="Move Deck Up">↑</button>
                  <button type="button" class="sub-move-btn btn-sub-move-down" data-deck-id="deck-1-250" title="Move Down" aria-label="Move Deck Down">↓</button>
                </div>
                <button type="button" class="duo-btn-3d duo-btn-3d-green" id="btn-study-tier-1" style="padding: 12px 22px; font-size: 0.9rem;">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <polygon points="5 3 19 12 5 21 5 3"></polygon>
                  </svg>
                  <span>Study 1–250</span>
                </button>
              </div>
            </div>
            <div style="margin-top: 14px; padding-top: 12px; border-top: 1px solid rgba(255, 255, 255, 0.08); display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
              <div style="font-size: 0.8rem; color: #94a3b8;">
                Filtered core foundations: pronouns, auxiliary/modal verbs, spatial/time prepositions & logical connectors.
              </div>
              <div style="display: flex; align-items: center; gap: 10px;">
                <span id="tier-1-stat-line" style="font-size: 0.82rem; font-weight: 700; color: #34d399; font-variant-numeric: tabular-nums;">0 / 233 Learned</span>
                <div style="width: 110px; height: 7px; background: rgba(255, 255, 255, 0.1); border-radius: 9999px; overflow: hidden;">
                  <div id="tier-1-progress-bar" style="width: 0%; height: 100%; background: #34d399; border-radius: 9999px;"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- SPLIT 2: Cards 251 – 500 (Numbers, Time & Core Actions) -->
          <div class="tier-card-option tier-card-Sortable-item subsection-tier-card" id="sub-tier-251-500" data-deck-id="deck-251-500" data-range-group="1-1000" data-default-order="2" draggable="true" role="button" tabindex="0" style="margin-bottom: 16px; background: linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(15, 23, 42, 0.9)); border: 1.5px solid rgba(245, 158, 11, 0.42); box-shadow: 0 8px 24px rgba(245, 158, 11, 0.14); border-radius: 20px; padding: 22px 24px; cursor: pointer; transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px;">
              <div style="display: flex; align-items: center; gap: 16px;">
                <span style="display: flex; align-items: center; justify-content: center; width: 52px; height: 52px; border-radius: 14px; background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.1); font-size: 1.65rem;">⚡</span>
                <div>
                  <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                    <span style="font-size: 0.72rem; font-weight: 800; letter-spacing: 0.08em; color: #fbbf24; text-transform: uppercase;">Section 1 (1–1000) · Split 2</span>
                    <span class="active-tier-pill" id="pill-tier-251" style="display: none; font-size: 0.66rem; font-weight: 800; background: #f59e0b; color: #0f172a; padding: 2px 8px; border-radius: 999px;">ACTIVE DECK</span>
                  </div>
                  <h3 style="font-size: 1.25rem; font-weight: 800; color: #ffffff; margin: 3px 0 4px;">Cards 251 – 500 (Numbers, Time & Core Actions)</h3>
                  <div id="tier-251-words-sub" style="font-size: 0.84rem; color: #cbd5e1;">ZERO, HUNDRED, TODAY, GO, COME, MAKE, THINK, BREAK, SLEEP, COMPARE · <strong id="tier-251-total-words">250</strong> Words</div>
                </div>
              </div>
              <div style="display: flex; align-items: center; gap: 10px;">
                <div class="sub-move-controls" title="Reorder deck">
                  <span class="sub-drag-handle" aria-label="Drag to reorder">⋮⋮</span>
                  <button type="button" class="sub-move-btn btn-sub-move-up" data-deck-id="deck-251-500" title="Move Up" aria-label="Move Deck Up">↑</button>
                  <button type="button" class="sub-move-btn btn-sub-move-down" data-deck-id="deck-251-500" title="Move Down" aria-label="Move Deck Down">↓</button>
                </div>
                <button type="button" class="duo-btn-3d duo-btn-3d-green" id="btn-study-tier-251" style="padding: 12px 22px; font-size: 0.9rem;">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <polygon points="5 3 19 12 5 21 5 3"></polygon>
                  </svg>
                  <span>Study 251–500</span>
                </button>
              </div>
            </div>
            <div style="margin-top: 14px; padding-top: 12px; border-top: 1px solid rgba(255, 255, 255, 0.08); display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
              <div style="font-size: 0.8rem; color: #94a3b8;">
                Cardinal numbers, time & calendar, essential high-frequency action verbs & daily routines.
              </div>
              <div style="display: flex; align-items: center; gap: 10px;">
                <span id="tier-251-stat-line" style="font-size: 0.82rem; font-weight: 700; color: #fbbf24; font-variant-numeric: tabular-nums;">0 / 250 Learned</span>
                <div style="width: 110px; height: 7px; background: rgba(255, 255, 255, 0.1); border-radius: 9999px; overflow: hidden;">
                  <div id="tier-251-progress-bar" style="width: 0%; height: 100%; background: #fbbf24; border-radius: 9999px;"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- SPLIT 3: Cards 501 – 750 (Adjectives, Colors, Body & Health) -->
          <div class="tier-card-option tier-card-Sortable-item subsection-tier-card" id="sub-tier-501-750" data-deck-id="deck-501-750" data-range-group="1-1000" data-default-order="3" draggable="true" role="button" tabindex="0" style="margin-bottom: 16px; background: linear-gradient(135deg, rgba(236, 72, 153, 0.2), rgba(15, 23, 42, 0.9)); border: 1.5px solid rgba(236, 72, 153, 0.42); box-shadow: 0 8px 24px rgba(236, 72, 153, 0.14); border-radius: 20px; padding: 22px 24px; cursor: pointer; transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px;">
              <div style="display: flex; align-items: center; gap: 16px;">
                <span style="display: flex; align-items: center; justify-content: center; width: 52px; height: 52px; border-radius: 14px; background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.1); font-size: 1.65rem;">🏃</span>
                <div>
                  <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                    <span style="font-size: 0.72rem; font-weight: 800; letter-spacing: 0.08em; color: #f472b6; text-transform: uppercase;">Section 1 (1–1000) · Split 3</span>
                    <span class="active-tier-pill" id="pill-tier-501" style="display: none; font-size: 0.66rem; font-weight: 800; background: #ec4899; color: #ffffff; padding: 2px 8px; border-radius: 999px;">ACTIVE DECK</span>
                  </div>
                  <h3 style="font-size: 1.25rem; font-weight: 800; color: #ffffff; margin: 3px 0 4px;">Cards 501 – 750 (Adjectives, Colors, Body & Health)</h3>
                  <div id="tier-501-words-sub" style="font-size: 0.84rem; color: #cbd5e1;">GOOD, BIG, FAST, COLOR, FAMILY, HEART, DOCTOR, FOOD, RICE, SPICE · <strong id="tier-501-total-words">250</strong> Words</div>
                </div>
              </div>
              <div style="display: flex; align-items: center; gap: 10px;">
                <div class="sub-move-controls" title="Reorder deck">
                  <span class="sub-drag-handle" aria-label="Drag to reorder">⋮⋮</span>
                  <button type="button" class="sub-move-btn btn-sub-move-up" data-deck-id="deck-501-750" title="Move Up" aria-label="Move Deck Up">↑</button>
                  <button type="button" class="sub-move-btn btn-sub-move-down" data-deck-id="deck-501-750" title="Move Down" aria-label="Move Deck Down">↓</button>
                </div>
                <button type="button" class="duo-btn-3d duo-btn-3d-green" id="btn-study-tier-501" style="padding: 12px 22px; font-size: 0.9rem;">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <polygon points="5 3 19 12 5 21 5 3"></polygon>
                  </svg>
                  <span>Study 501–750</span>
                </button>
              </div>
            </div>
            <div style="margin-top: 14px; padding-top: 12px; border-top: 1px solid rgba(255, 255, 255, 0.08); display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
              <div style="font-size: 0.8rem; color: #94a3b8;">
                Core descriptive adjectives, colors, shapes, human relationships, body anatomy & food nutrition.
              </div>
              <div style="display: flex; align-items: center; gap: 10px;">
                <span id="tier-501-stat-line" style="font-size: 0.82rem; font-weight: 700; color: #f472b6; font-variant-numeric: tabular-nums;">0 / 250 Learned</span>
                <div style="width: 110px; height: 7px; background: rgba(255, 255, 255, 0.1); border-radius: 9999px; overflow: hidden;">
                  <div id="tier-501-progress-bar" style="width: 0%; height: 100%; background: #f472b6; border-radius: 9999px;"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- SPLIT 4: Cards 751 – 1000 (Home, Kitchen, City & Transit) -->
          <div class="tier-card-option tier-card-Sortable-item subsection-tier-card" id="sub-tier-751-1000" data-deck-id="deck-751-1000" data-range-group="1-1000" data-default-order="4" draggable="true" role="button" tabindex="0" style="margin-bottom: 16px; background: linear-gradient(135deg, rgba(2, 132, 199, 0.22), rgba(15, 23, 42, 0.9)); border: 1.5px solid rgba(56, 189, 248, 0.45); box-shadow: 0 8px 24px rgba(2, 132, 199, 0.16); border-radius: 20px; padding: 22px 24px; cursor: pointer; transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px;">
              <div style="display: flex; align-items: center; gap: 16px;">
                <span style="display: flex; align-items: center; justify-content: center; width: 52px; height: 52px; border-radius: 14px; background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.1); font-size: 1.65rem;">🏠</span>
                <div>
                  <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                    <span style="font-size: 0.72rem; font-weight: 800; letter-spacing: 0.08em; color: #38bdf8; text-transform: uppercase;">Section 1 (1–1000) · Split 4</span>
                    <span class="active-tier-pill" id="pill-tier-751" style="display: none; font-size: 0.66rem; font-weight: 800; background: #38bdf8; color: #0f172a; padding: 2px 8px; border-radius: 999px;">ACTIVE DECK</span>
                  </div>
                  <h3 style="font-size: 1.25rem; font-weight: 800; color: #ffffff; margin: 3px 0 4px;">Cards 751 – 1000 (Home, Kitchen, City & Transit)</h3>
                  <div id="tier-751-words-sub" style="font-size: 0.84rem; color: #cbd5e1;">HONEY, STOVE, SINK, SOFA, BED, SHIRT, TRAIN, AIRPORT, BANK · <strong id="tier-751-total-words">250</strong> Words</div>
                </div>
              </div>
              <div style="display: flex; align-items: center; gap: 10px;">
                <div class="sub-move-controls" title="Reorder deck">
                  <span class="sub-drag-handle" aria-label="Drag to reorder">⋮⋮</span>
                  <button type="button" class="sub-move-btn btn-sub-move-up" data-deck-id="deck-751-1000" title="Move Up" aria-label="Move Deck Up">↑</button>
                  <button type="button" class="sub-move-btn btn-sub-move-down" data-deck-id="deck-751-1000" title="Move Down" aria-label="Move Deck Down">↓</button>
                </div>
                <button type="button" class="duo-btn-3d duo-btn-3d-green" id="btn-study-tier-751" style="padding: 12px 22px; font-size: 0.9rem;">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <polygon points="5 3 19 12 5 21 5 3"></polygon>
                  </svg>
                  <span>Study 751–1000</span>
                </button>
              </div>
            </div>
            <div style="margin-top: 14px; padding-top: 12px; border-top: 1px solid rgba(255, 255, 255, 0.08); display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
              <div style="font-size: 0.8rem; color: #94a3b8;">
                Kitchenware, appliances, furniture, wardrobe, city locations & transport infrastructure.
              </div>
              <div style="display: flex; align-items: center; gap: 10px;">
                <span id="tier-751-stat-line" style="font-size: 0.82rem; font-weight: 700; color: #38bdf8; font-variant-numeric: tabular-nums;">0 / 250 Learned</span>
                <div style="width: 110px; height: 7px; background: rgba(255, 255, 255, 0.1); border-radius: 9999px; overflow: hidden;">
                  <div id="tier-751-progress-bar" style="width: 0%; height: 100%; background: #38bdf8; border-radius: 9999px;"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- SPLIT 5: Cards 1001 – 1500 (Nature, Tech, Social & Professions) -->
          <div class="tier-card-option tier-card-Sortable-item subsection-tier-card" id="sub-tier-1001-1500" data-deck-id="deck-1001-1500" data-range-group="1001-2000" data-default-order="5" draggable="true" role="button" tabindex="0" style="margin-bottom: 16px; background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(15, 23, 42, 0.9)); border: 1.5px solid rgba(99, 102, 241, 0.42); box-shadow: 0 8px 24px rgba(99, 102, 241, 0.14); border-radius: 20px; padding: 22px 24px; cursor: pointer; transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px;">
              <div style="display: flex; align-items: center; gap: 16px;">
                <span style="display: flex; align-items: center; justify-content: center; width: 52px; height: 52px; border-radius: 14px; background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.1); font-size: 1.65rem;">🌤️</span>
                <div>
                  <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                    <span style="font-size: 0.72rem; font-weight: 800; letter-spacing: 0.08em; color: #818cf8; text-transform: uppercase;">Section 2 (1001–2000) · Split 5</span>
                    <span class="active-tier-pill" id="pill-tier-1001" style="display: none; font-size: 0.66rem; font-weight: 800; background: #6366f1; color: #ffffff; padding: 2px 8px; border-radius: 999px;">ACTIVE DECK</span>
                  </div>
                  <h3 style="font-size: 1.25rem; font-weight: 800; color: #ffffff; margin: 3px 0 4px;">Cards 1001 – 1500 (Nature, Tech, Social & Professions)</h3>
                  <div id="tier-1001-words-sub" style="font-size: 0.84rem; color: #cbd5e1;">SKY, SUN, ANIMAL, WIFI, LAPTOP, TEXTURES, EMOTIONS, PROFESSIONS, BOTHER · <strong id="tier-1001-total-words">500</strong> Words</div>
                </div>
              </div>
              <div style="display: flex; align-items: center; gap: 10px;">
                <div class="sub-move-controls" title="Reorder deck">
                  <span class="sub-drag-handle" aria-label="Drag to reorder">⋮⋮</span>
                  <button type="button" class="sub-move-btn btn-sub-move-up" data-deck-id="deck-1001-1500" title="Move Up" aria-label="Move Deck Up">↑</button>
                  <button type="button" class="sub-move-btn btn-sub-move-down" data-deck-id="deck-1001-1500" title="Move Down" aria-label="Move Deck Down">↓</button>
                </div>
                <button type="button" class="duo-btn-3d duo-btn-3d-green" id="btn-study-tier-1001" style="padding: 12px 22px; font-size: 0.9rem;">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <polygon points="5 3 19 12 5 21 5 3"></polygon>
                  </svg>
                  <span>Study 1001–1500</span>
                </button>
              </div>
            </div>
            <div style="margin-top: 14px; padding-top: 12px; border-top: 1px solid rgba(255, 255, 255, 0.08); display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
              <div style="font-size: 0.8rem; color: #94a3b8;">
                Sky & atmospheric nature, wildlife, modern digital tech, kitchen tools, sensory textures & professions.
              </div>
              <div style="display: flex; align-items: center; gap: 10px;">
                <span id="tier-1001-stat-line" style="font-size: 0.82rem; font-weight: 700; color: #818cf8; font-variant-numeric: tabular-nums;">0 / 500 Learned</span>
                <div style="width: 110px; height: 7px; background: rgba(255, 255, 255, 0.1); border-radius: 9999px; overflow: hidden;">
                  <div id="tier-1001-progress-bar" style="width: 0%; height: 100%; background: #6366f1; border-radius: 9999px;"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- SPLIT 6: Cards 1501 – 2000 (Commerce, Law, Society & Media) -->
          <div class="tier-card-option tier-card-Sortable-item subsection-tier-card" id="sub-tier-1501-2000" data-deck-id="deck-1501-2000" data-range-group="1001-2000" data-default-order="6" draggable="true" role="button" tabindex="0" style="margin-bottom: 16px; background: linear-gradient(135deg, rgba(14, 165, 233, 0.2), rgba(15, 23, 42, 0.9)); border: 1.5px solid rgba(14, 165, 233, 0.42); box-shadow: 0 8px 24px rgba(14, 165, 233, 0.14); border-radius: 20px; padding: 22px 24px; cursor: pointer; transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px;">
              <div style="display: flex; align-items: center; gap: 16px;">
                <span style="display: flex; align-items: center; justify-content: center; width: 52px; height: 52px; border-radius: 14px; background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.1); font-size: 1.65rem;">⚖️</span>
                <div>
                  <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                    <span style="font-size: 0.72rem; font-weight: 800; letter-spacing: 0.08em; color: #38bdf8; text-transform: uppercase;">Section 2 (1001–2000) · Split 6</span>
                    <span class="active-tier-pill" id="pill-tier-1501" style="display: none; font-size: 0.66rem; font-weight: 800; background: #0ea5e9; color: #ffffff; padding: 2px 8px; border-radius: 999px;">ACTIVE DECK</span>
                  </div>
                  <h3 style="font-size: 1.25rem; font-weight: 800; color: #ffffff; margin: 3px 0 4px;">Cards 1501 – 2000 (Commerce, Law, Society & Media)</h3>
                  <div id="tier-1501-words-sub" style="font-size: 0.84rem; color: #cbd5e1;">DISTURB, CAREER, SALARY, BUSINESS, MONEY, LAW, CRIME, GOVERNMENT, NEWS, PUPIL · <strong id="tier-1501-total-words">500</strong> Words</div>
                </div>
              </div>
              <div style="display: flex; align-items: center; gap: 10px;">
                <div class="sub-move-controls" title="Reorder deck">
                  <span class="sub-drag-handle" aria-label="Drag to reorder">⋮⋮</span>
                  <button type="button" class="sub-move-btn btn-sub-move-up" data-deck-id="deck-1501-2000" title="Move Up" aria-label="Move Deck Up">↑</button>
                  <button type="button" class="sub-move-btn btn-sub-move-down" data-deck-id="deck-1501-2000" title="Move Down" aria-label="Move Deck Down">↓</button>
                </div>
                <button type="button" class="duo-btn-3d duo-btn-3d-green" id="btn-study-tier-1501" style="padding: 12px 22px; font-size: 0.9rem;">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <polygon points="5 3 19 12 5 21 5 3"></polygon>
                  </svg>
                  <span>Study 1501–2000</span>
                </button>
              </div>
            </div>
            <div style="margin-top: 14px; padding-top: 12px; border-top: 1px solid rgba(255, 255, 255, 0.08); display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
              <div style="font-size: 0.8rem; color: #94a3b8;">
                Workplace dynamics, finance & commerce, judicial law, civic government, international affairs & public media.
              </div>
              <div style="display: flex; align-items: center; gap: 10px;">
                <span id="tier-1501-stat-line" style="font-size: 0.82rem; font-weight: 700; color: #38bdf8; font-variant-numeric: tabular-nums;">0 / 500 Learned</span>
                <div style="width: 110px; height: 7px; background: rgba(255, 255, 255, 0.1); border-radius: 9999px; overflow: hidden;">
                  <div id="tier-1501-progress-bar" style="width: 0%; height: 100%; background: #0ea5e9; border-radius: 9999px;"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- SPLIT 7: Cards 2001 – 2500 (Education, Science, Arts & Sports) -->
          <div class="tier-card-option tier-card-Sortable-item subsection-tier-card" id="sub-tier-2001-2500" data-deck-id="deck-2001-2500" data-range-group="2001-3000" data-default-order="7" draggable="true" role="button" tabindex="0" style="margin-bottom: 16px; background: linear-gradient(135deg, rgba(16, 185, 129, 0.22), rgba(6, 182, 212, 0.16)); border: 1.5px solid rgba(16, 185, 129, 0.45); box-shadow: 0 8px 26px rgba(16, 185, 129, 0.15); border-radius: 20px; padding: 22px 24px; cursor: pointer; transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px;">
              <div style="display: flex; align-items: center; gap: 16px;">
                <span style="display: flex; align-items: center; justify-content: center; width: 52px; height: 52px; border-radius: 14px; background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.1); font-size: 1.65rem;">🎓</span>
                <div>
                  <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                    <span style="font-size: 0.72rem; font-weight: 800; letter-spacing: 0.08em; color: #34d399; text-transform: uppercase;">Section 3 (2001–3000) · Split 7</span>
                    <span class="active-tier-pill" id="pill-tier-2001" style="display: none; font-size: 0.66rem; font-weight: 800; background: #10b981; color: #ffffff; padding: 2px 8px; border-radius: 999px;">ACTIVE DECK</span>
                  </div>
                  <h3 style="font-size: 1.25rem; font-weight: 800; color: #ffffff; margin: 3px 0 4px;">Cards 2001 – 2500 (Education, Science, Arts & Sports)</h3>
                  <div id="tier-2001-words-sub" style="font-size: 0.84rem; color: #cbd5e1;">TEACHER, SCIENCE, PHYSICS, MATERIALS, ART, MUSIC, SPORTS, ECOLOGY, CUISINE, BUNDLE · <strong id="tier-2001-total-words">500</strong> Words</div>
                </div>
              </div>
              <div style="display: flex; align-items: center; gap: 10px;">
                <div class="sub-move-controls" title="Reorder deck">
                  <span class="sub-drag-handle" aria-label="Drag to reorder">⋮⋮</span>
                  <button type="button" class="sub-move-btn btn-sub-move-up" data-deck-id="deck-2001-2500" title="Move Up" aria-label="Move Deck Up">↑</button>
                  <button type="button" class="sub-move-btn btn-sub-move-down" data-deck-id="deck-2001-2500" title="Move Down" aria-label="Move Deck Down">↓</button>
                </div>
                <button type="button" class="duo-btn-3d duo-btn-3d-green" id="btn-study-tier-2001" style="padding: 12px 22px; font-size: 0.9rem;">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <polygon points="5 3 19 12 5 21 5 3"></polygon>
                  </svg>
                  <span>Study 2001–2500</span>
                </button>
              </div>
            </div>
            <div style="margin-top: 14px; padding-top: 12px; border-top: 1px solid rgba(255, 255, 255, 0.08); display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
              <div style="font-size: 0.8rem; color: #94a3b8;">
                Academic education, sciences, digital devices, physical materials, fine arts, music, athletics & culinary arts.
              </div>
              <div style="display: flex; align-items: center; gap: 10px;">
                <span id="tier-2001-stat-line" style="font-size: 0.82rem; font-weight: 700; color: #34d399; font-variant-numeric: tabular-nums;">0 / 500 Learned</span>
                <div style="width: 110px; height: 7px; background: rgba(255, 255, 255, 0.1); border-radius: 9999px; overflow: hidden;">
                  <div id="tier-2001-progress-bar" style="width: 0%; height: 100%; background: #10b981; border-radius: 9999px;"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- SPLIT 8: Cards 2501 – 3000 (Health, Housing, Phrasal Verbs & Dialogues) -->
          <div class="tier-card-option tier-card-Sortable-item subsection-tier-card" id="sub-tier-2501-3000" data-deck-id="deck-2501-3000" data-range-group="2001-3000" data-default-order="8" draggable="true" role="button" tabindex="0" style="margin-bottom: 16px; background: linear-gradient(135deg, rgba(59, 130, 246, 0.22), rgba(139, 92, 246, 0.16)); border: 1.5px solid rgba(59, 130, 246, 0.45); box-shadow: 0 8px 26px rgba(59, 130, 246, 0.15); border-radius: 20px; padding: 22px 24px; cursor: pointer; transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px;">
              <div style="display: flex; align-items: center; gap: 16px;">
                <span style="display: flex; align-items: center; justify-content: center; width: 52px; height: 52px; border-radius: 14px; background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.1); font-size: 1.65rem;">🗣️</span>
                <div>
                  <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                    <span style="font-size: 0.72rem; font-weight: 800; letter-spacing: 0.08em; color: #60a5fa; text-transform: uppercase;">Section 3 (2001–3000) · Split 8</span>
                    <span class="active-tier-pill" id="pill-tier-2501" style="display: none; font-size: 0.66rem; font-weight: 800; background: #3b82f6; color: #ffffff; padding: 2px 8px; border-radius: 999px;">ACTIVE DECK</span>
                  </div>
                  <h3 style="font-size: 1.25rem; font-weight: 800; color: #ffffff; margin: 3px 0 4px;">Cards 2501 – 3000 (Health, Housing, Phrasal Verbs & Dialogues)</h3>
                  <div id="tier-2501-words-sub" style="font-size: 0.84rem; color: #cbd5e1;">HICCUP, SURGERY, MINDSET, PROPERTY, LEASE, FIND OUT, TURN ON, HOW ARE YOU, AUTHENTIC · <strong id="tier-2501-total-words">500</strong> Words</div>
                </div>
              </div>
              <div style="display: flex; align-items: center; gap: 10px;">
                <div class="sub-move-controls" title="Reorder deck">
                  <span class="sub-drag-handle" aria-label="Drag to reorder">⋮⋮</span>
                  <button type="button" class="sub-move-btn btn-sub-move-up" data-deck-id="deck-2501-3000" title="Move Up" aria-label="Move Deck Up">↑</button>
                  <button type="button" class="sub-move-btn btn-sub-move-down" data-deck-id="deck-2501-3000" title="Move Down" aria-label="Move Deck Down">↓</button>
                </div>
                <button type="button" class="duo-btn-3d duo-btn-3d-green" id="btn-study-tier-2501" style="padding: 12px 22px; font-size: 0.9rem;">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <polygon points="5 3 19 12 5 21 5 3"></polygon>
                  </svg>
                  <span>Study 2501–3000</span>
                </button>
              </div>
            </div>
            <div style="margin-top: 14px; padding-top: 12px; border-top: 1px solid rgba(255, 255, 255, 0.08); display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
              <div style="font-size: 0.8rem; color: #94a3b8;">
                Clinical medicine, mindset, real estate & tenancy, everyday phrasal verbs, spoken idioms & travel dialogues.
              </div>
              <div style="display: flex; align-items: center; gap: 10px;">
                <span id="tier-2501-stat-line" style="font-size: 0.82rem; font-weight: 700; color: #60a5fa; font-variant-numeric: tabular-nums;">0 / 500 Learned</span>
                <div style="width: 110px; height: 7px; background: rgba(255, 255, 255, 0.1); border-radius: 9999px; overflow: hidden;">
                  <div id="tier-2501-progress-bar" style="width: 0%; height: 100%; background: #3b82f6; border-radius: 9999px;"></div>
                </div>
              </div>
            </div>
          </div>
          </div>
          </div>
          </div><!-- /#vocab-3k-drilldown-view -->
          <!-- Custom Uploaded Decks Dynamic Section -->"""

    html = html[:subsections_container_match.start()] + new_subsections_html + html[subsections_container_match.end():]

    # Update tierWireMap
    wire_map_match = re.search(r"const tierWireMap\s*=\s*\[(.*?)\];", html, re.S)
    if wire_map_match:
        new_wire_map = """const tierWireMap = [
          { deckId: "deck-1-250", subId: "sub-tier-1-250", btnId: "btn-study-tier-1", presetId: "btn-preset-tier-1" },
          { deckId: "deck-251-500", subId: "sub-tier-251-500", btnId: "btn-study-tier-251", presetId: "btn-preset-tier-251" },
          { deckId: "deck-501-750", subId: "sub-tier-501-750", btnId: "btn-study-tier-501", presetId: "btn-preset-tier-501" },
          { deckId: "deck-751-1000", subId: "sub-tier-751-1000", btnId: "btn-study-tier-751", presetId: "btn-preset-tier-751" },
          { deckId: "deck-1001-1500", subId: "sub-tier-1001-1500", btnId: "btn-study-tier-1001", presetId: "btn-preset-tier-1001" },
          { deckId: "deck-1501-2000", subId: "sub-tier-1501-2000", btnId: "btn-study-tier-1501", presetId: "btn-preset-tier-1501" },
          { deckId: "deck-2001-2500", subId: "sub-tier-2001-2500", btnId: "btn-study-tier-2001", presetId: "btn-preset-tier-2001" },
          { deckId: "deck-2501-3000", subId: "sub-tier-2501-3000", btnId: "btn-study-tier-2501", presetId: "btn-preset-tier-2501" }
        ];"""
        html = html[:wire_map_match.start()] + new_wire_map + html[wire_map_match.end():]

    # Update settings-section-reset-select builtInOptions
    reset_opts_match = re.search(r"const builtInOptions\s*=\s*\[(.*?)\];", html, re.S)
    if reset_opts_match:
        new_reset_opts = """const builtInOptions = [
            { id: "deck-1-250", label: "Split 1: Cards 1 – 250 (Core Foundations & Pronouns)" },
            { id: "deck-251-500", label: "Split 2: Cards 251 – 500 (Numbers, Time & Core Actions)" },
            { id: "deck-501-750", label: "Split 3: Cards 501 – 750 (Adjectives, Colors, Body & Health)" },
            { id: "deck-751-1000", label: "Split 4: Cards 751 – 1000 (Home, Kitchen, City & Transit)" },
            { id: "deck-1001-1500", label: "Split 5: Cards 1001 – 1500 (Nature, Tech, Social & Professions)" },
            { id: "deck-1501-2000", label: "Split 6: Cards 1501 – 2000 (Commerce, Law, Society & Media)" },
            { id: "deck-2001-2500", label: "Split 7: Cards 2001 – 2500 (Education, Science, Arts & Sports)" },
            { id: "deck-2501-3000", label: "Split 8: Cards 2501 – 3000 (Health, Housing, Phrasal Verbs & Dialogues)" }
          ];"""
        html = html[:reset_opts_match.start()] + new_reset_opts + html[reset_opts_match.end():]

    # Update buildMasterIndex deckOrder
    deck_order_match = re.search(r"const deckOrder\s*=\s*\[(.*?)\];", html, re.S)
    if deck_order_match:
        new_deck_order = """const deckOrder = [
            "deck-1-250",
            "deck-251-500",
            "deck-501-750",
            "deck-751-1000",
            "deck-1001-1500",
            "deck-1501-2000",
            "deck-2001-2500",
            "deck-2501-3000"
          ];"""
        html = html[:deck_order_match.start()] + new_deck_order + html[deck_order_match.end():]

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Successfully updated index.html with 8 splits and Split 1 translations!")

if __name__ == "__main__":
    main()
