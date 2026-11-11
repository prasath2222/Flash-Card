def main():
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Desktop status badge
    old_desktop = """            <div class="stat-badge-duo stat-badge-mastery" id="desktop-3k-status-badge" title="Status across 3,000 words">
              <span>⚡</span>
              <span>Status: <strong id="desktop-status-count">0</strong> / 3,000</span>
            </div>"""

    new_desktop = """            <div class="stat-badge-duo stat-badge-mastery" id="desktop-3k-status-badge" title="Status across all words">
              <span>⚡</span>
              <span>Status: <strong id="desktop-status-count">0</strong> / <span id="desktop-total-words-count">2,906</span></span>
            </div>"""

    if old_desktop in html:
        html = html.replace(old_desktop, new_desktop, 1)
        print("Updated desktop status badge.")

    # 2. Mobile status badge
    old_mobile = """            <div class="stat-badge-duo stat-badge-mastery" id="mobile-3k-status-badge">
              <span>⚡ <strong id="mobile-status-count">0</strong>/3k</span>
            </div>"""

    new_mobile = """            <div class="stat-badge-duo stat-badge-mastery" id="mobile-3k-status-badge">
              <span>⚡ <strong id="mobile-status-count">0</strong>/<span id="mobile-total-words-count">2,906</span></span>
            </div>"""

    if old_mobile in html:
        html = html.replace(old_mobile, new_mobile, 1)
        print("Updated mobile status badge.")

    # 3. Overall Mastery line
    old_mastery = '<span>Overall Mastery: <strong id="card-3k-learned-count">0</strong> / 3,000 Learned</span>'
    new_mastery = '<span>Overall Mastery: <strong id="card-3k-learned-count">0</strong> / <span id="card-3k-total-words-count">2,906</span> Learned</span>'
    if old_mastery in html:
        html = html.replace(old_mastery, new_mastery, 1)
        print("Updated Overall Mastery line.")

    # 4. updateGlobalLearnedDisplays
    old_ugld = """      function updateGlobalLearnedDisplays() {
        const totalLearned = learnedCardsSet ? learnedCardsSet.size : 0;
        const totalWords = 3000;
        const totalPct = Math.min(100, ((totalLearned / totalWords) * 100)).toFixed(1);
        const desktopStatusEl = document.getElementById("desktop-status-count");
        if (desktopStatusEl) desktopStatusEl.textContent = totalLearned.toLocaleString();
        const mobileStatusEl = document.getElementById("mobile-status-count");
        if (mobileStatusEl) mobileStatusEl.textContent = totalLearned.toLocaleString();"""

    new_ugld = """      function updateGlobalLearnedDisplays() {
        const uniqueMetas = (typeof BUILT_IN_DECKS_META === "object" && BUILT_IN_DECKS_META)
          ? Array.from(new Set(Object.values(BUILT_IN_DECKS_META)))
          : [];
        const totalWords = uniqueMetas.reduce((sum, meta) => {
          const rem = getRemainingDeckCards((meta && meta.cards) || []);
          return sum + rem.length;
        }, 0) || 2906;
        const totalLearned = learnedCardsSet ? learnedCardsSet.size : 0;
        const totalPct = Math.min(100, ((totalLearned / totalWords) * 100)).toFixed(1);
        const desktopStatusEl = document.getElementById("desktop-status-count");
        if (desktopStatusEl) desktopStatusEl.textContent = totalLearned.toLocaleString();
        const desktopTotalEl = document.getElementById("desktop-total-words-count");
        if (desktopTotalEl) desktopTotalEl.textContent = totalWords.toLocaleString();
        const mobileStatusEl = document.getElementById("mobile-status-count");
        if (mobileStatusEl) mobileStatusEl.textContent = totalLearned.toLocaleString();
        const mobileTotalEl = document.getElementById("mobile-total-words-count");
        if (mobileTotalEl) mobileTotalEl.textContent = totalWords.toLocaleString();
        const card3kTotalEl = document.getElementById("card-3k-total-words-count");
        if (card3kTotalEl) card3kTotalEl.textContent = totalWords.toLocaleString();"""

    if old_ugld in html:
        html = html.replace(old_ugld, new_ugld, 1)
        print("Updated updateGlobalLearnedDisplays.")

    # 5. Update flashcard3kStatusText and deduplicate BUILT_IN_DECKS_META iteration
    old_fc_text = 'if (flashcard3kStatusText) flashcard3kStatusText.textContent = `${totalLearned} / 3,000`;'
    new_fc_text = 'if (flashcard3kStatusText) flashcard3kStatusText.textContent = `${totalLearned.toLocaleString()} / ${totalWords.toLocaleString()}`;'
    if old_fc_text in html:
        html = html.replace(old_fc_text, new_fc_text, 1)
        print("Updated flashcard3kStatusText.")

    html = html.replace(
        "Object.values(BUILT_IN_DECKS_META).forEach(meta => {",
        "Array.from(new Set(Object.values(BUILT_IN_DECKS_META))).forEach(meta => {",
    )

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Done!")


if __name__ == "__main__":
    main()
