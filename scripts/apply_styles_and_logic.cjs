const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');
console.log('Original html length for styles and logic:', html.length);

// =========================================================================
// 1. INJECT MODERN RESPONSIVE CSS STYLES
// =========================================================================

const modernResponsiveCSS = `
      /* ==========================================================
         MODERN RESPONSIVE LAYOUT (DESKTOP / TABLET / MOBILE)
         ========================================================== */

      /* App Container & Screen Responsive Sizing */
      #app-container {
        width: 100%;
        height: 100%;
        max-width: 100%;
        background: #070a13;
        display: flex;
        flex-direction: column;
        position: relative;
        overflow: hidden;
      }

      .app-screen {
        width: 100%;
        height: 100%;
        max-width: 1120px;
        margin: 0 auto;
        padding: 0 16px;
        flex: 1;
        display: none;
        flex-direction: column;
        overflow: hidden;
      }

      .app-screen.active-screen {
        display: flex;
      }

      /* Desktop Navigation Bar (PC / Large Screen) */
      .desktop-nav-bar {
        display: none;
        align-items: center;
        gap: 6px;
        background: rgba(255, 255, 255, 0.04);
        padding: 4px 6px;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.07);
      }

      .desktop-nav-link {
        background: transparent;
        border: none;
        color: #94a3b8;
        padding: 6px 14px;
        border-radius: 10px;
        font-size: 0.85rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.16s ease;
        display: inline-flex;
        align-items: center;
        gap: 6px;
      }

      .desktop-nav-link:hover {
        color: #ffffff;
        background: rgba(255, 255, 255, 0.07);
      }

      .desktop-nav-link.active {
        color: #38bdf8;
        background: rgba(56, 189, 248, 0.12);
        border: 1px solid rgba(56, 189, 248, 0.25);
      }

      /* Mobile Hamburger Menu Button (FAR LEFT CORNER ON MOBILE) */
      .mobile-hamburger-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 42px;
        height: 42px;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #e2e8f0;
        cursor: pointer;
        transition: all 0.18s ease;
        flex-shrink: 0;
        margin-right: 8px;
      }

      .mobile-hamburger-btn:hover,
      .mobile-hamburger-btn:active {
        background: rgba(56, 189, 248, 0.15);
        color: #38bdf8;
        border-color: rgba(56, 189, 248, 0.35);
        transform: scale(0.96);
      }

      /* Top App Bar Modern Styling */
      .home-app-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.07);
        flex-shrink: 0;
        width: 100%;
        gap: 12px;
      }

      .brand-group {
        display: flex;
        align-items: center;
        gap: 10px;
        flex-shrink: 0;
      }

      /* Global Status 1 to 3K Pill */
      .global-status-3k-pill {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        padding: 6px 12px;
        border-radius: 20px;
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.28);
        color: #34d399;
        font-size: 0.8rem;
        font-weight: 600;
        white-space: nowrap;
      }

      .status-dot-pulse {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #10b981;
        box-shadow: 0 0 10px #10b981;
        animation: pulseLiveDot 2s infinite ease-in-out;
      }

      @keyframes pulseLiveDot {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.45; transform: scale(0.85); }
      }

      /* Settings Button in Header */
      .btn-settings-header,
      .desktop-settings-btn {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 8px 14px;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #cbd5e1;
        font-size: 0.82rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.18s ease;
      }

      .btn-settings-header:hover,
      .desktop-settings-btn:hover {
        background: rgba(255, 255, 255, 0.1);
        color: #ffffff;
        border-color: rgba(255, 255, 255, 0.22);
      }

      /* Learned Checkbox Buttons (Tactile Feedback) */
      .btn-card-face-learned,
      .btn-top-learned-toggle {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 12px;
        border-radius: 20px;
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.12);
        color: #94a3b8;
        font-size: 0.78rem;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      }

      .btn-card-face-learned .learned-face-check,
      .btn-top-learned-toggle .learned-check-indicator {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 16px;
        height: 16px;
        border-radius: 4px;
        background: rgba(255, 255, 255, 0.1);
        font-size: 0.7rem;
        font-weight: 900;
        color: transparent;
        transition: all 0.2s ease;
      }

      .btn-card-face-learned.is-learned,
      .btn-top-learned-toggle.is-learned {
        background: rgba(16, 185, 129, 0.15);
        border-color: rgba(16, 185, 129, 0.5);
        color: #34d399;
        box-shadow: 0 0 16px rgba(16, 185, 129, 0.2);
      }

      .btn-card-face-learned.is-learned .learned-face-check,
      .btn-top-learned-toggle.is-learned .learned-check-indicator {
        background: #10b981;
        color: #064e3b;
      }

      /* Featured 3k Vocabulary Card Enhancements */
      .featured-3k-wrapper {
        width: 100%;
        perspective: 1200px;
      }

      .card-3k-featured {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(20, 30, 52, 0.88));
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 24px;
        padding: 28px 32px;
        position: relative;
        overflow: hidden;
        cursor: pointer;
        box-shadow: 0 20px 48px -12px rgba(0, 0, 0, 0.7), 0 0 32px rgba(56, 189, 248, 0.08);
        transition: transform 0.22s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.22s ease, border-color 0.22s ease;
      }

      .card-3k-featured:hover {
        border-color: rgba(56, 189, 248, 0.45);
        box-shadow: 0 24px 56px -10px rgba(0, 0, 0, 0.8), 0 0 40px rgba(56, 189, 248, 0.15);
      }

      .card-3k-layout {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 32px;
      }

      .card-3k-info-col {
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: 12px;
      }

      .card-3k-title {
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        color: #ffffff;
        line-height: 1.1;
      }

      .card-3k-desc {
        font-size: 0.92rem;
        line-height: 1.5;
        color: #94a3b8;
        max-width: 540px;
      }

      .progress-tier-hint {
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-size: 0.78rem;
        color: #94a3b8;
        margin-top: 6px;
      }

      /* Direct Launch Buttons on 3k Card */
      .card-3k-actions {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-top: 8px;
        flex-wrap: wrap;
      }

      .btn-launch-3k {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 12px 24px;
        border-radius: 14px;
        background: linear-gradient(135deg, #0284c7, #0ea5e9);
        color: #ffffff;
        font-size: 0.95rem;
        font-weight: 700;
        border: none;
        cursor: pointer;
        box-shadow: 0 8px 24px rgba(14, 165, 233, 0.38);
        transition: all 0.2s ease;
      }

      .btn-launch-3k:hover {
        background: linear-gradient(135deg, #0369a1, #0284c7);
        transform: translateY(-2px);
        box-shadow: 0 12px 28px rgba(14, 165, 233, 0.48);
      }

      .btn-subsections-3k {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 12px 20px;
        border-radius: 14px;
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.14);
        color: #e2e8f0;
        font-size: 0.9rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s ease;
      }

      .btn-subsections-3k:hover {
        background: rgba(255, 255, 255, 0.12);
        color: #ffffff;
        border-color: rgba(255, 255, 255, 0.25);
      }

      /* Subsections Screen Styling */
      .subsections-overview-banner {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.85));
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 18px 22px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
        margin-bottom: 8px;
        flex-wrap: wrap;
      }

      .banner-kicker {
        font-size: 0.7rem;
        font-weight: 800;
        letter-spacing: 0.1em;
        color: #38bdf8;
        margin-bottom: 4px;
      }

      .banner-heading {
        font-size: 1.2rem;
        font-weight: 700;
        color: #ffffff;
      }

      .banner-sub {
        font-size: 0.82rem;
        color: #94a3b8;
        margin-top: 2px;
      }

      .btn-direct-resume-tier {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 10px 18px;
        border-radius: 12px;
        background: rgba(56, 189, 248, 0.14);
        border: 1px solid rgba(56, 189, 248, 0.3);
        color: #38bdf8;
        font-size: 0.85rem;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.18s ease;
      }

      .btn-direct-resume-tier:hover {
        background: rgba(56, 189, 248, 0.24);
        border-color: #38bdf8;
        color: #ffffff;
      }

      .active-tier-highlight {
        background: #101c30 !important;
        border-color: #38bdf8 !important;
        box-shadow: 0 0 28px rgba(56, 189, 248, 0.18) !important;
      }

      /* MEDIA QUERIES FOR SCREEN BREAKPOINTS */
      @media (min-width: 768px) {
        /* On PC/Tablet: HIDE mobile hamburger menu completely! */
        .mobile-hamburger-btn {
          display: none !important;
        }

        /* On PC: SHOW full desktop navigation bar */
        .desktop-nav-bar {
          display: flex !important;
        }

        .desktop-only-text {
          display: inline !important;
        }

        /* Flashcard screen desktop optimization */
        .flashcard-top-nav {
          max-width: 900px;
          margin: 0 auto;
        }

        .card-stage {
          max-width: 700px;
          margin: 0 auto;
        }

        .bottom-nav-bar {
          max-width: 700px;
          margin: 0 auto;
        }
      }

      @media (max-width: 767px) {
        .desktop-nav-bar {
          display: none !important;
        }

        .mobile-hamburger-btn {
          display: flex !important;
        }

        .desktop-only-text {
          display: none !important;
        }

        .card-3k-featured {
          padding: 20px 18px;
        }

        .card-3k-layout {
          flex-direction: column;
        }

        .card-3k-visual-col {
          display: none;
        }

        .card-3k-title {
          font-size: 1.6rem;
        }
      }
`;

// Insert the modern responsive CSS right before </style>
html = html.replace('</style>', `${modernResponsiveCSS}\n</style>`);
console.log('Injected modern responsive CSS.');

// =========================================================================
// 2. INJECT ENHANCED JAVASCRIPT LOGIC
// =========================================================================

const modernLogicJS = `
      /* ==========================================================
         COMPREHENSIVE LEARNED TRACKER & STATUS 1 TO 3K SYSTEM
         ========================================================== */
      const LEARNED_STORAGE_KEY = "vocab_learned_cards_v3";
      const LAST_CARD_STORAGE_KEY = "vocab_last_card_v3";

      function loadLearnedCards() {
        try {
          const raw = localStorage.getItem(LEARNED_STORAGE_KEY);
          if (raw) {
            const arr = JSON.parse(raw);
            return new Set(arr);
          }
        } catch (e) {
          console.error("Could not load learned cards:", e);
        }
        return new Set();
      }

      let learnedCardsSet = loadLearnedCards();

      function saveLearnedCards() {
        try {
          localStorage.setItem(LEARNED_STORAGE_KEY, JSON.stringify([...learnedCardsSet]));
        } catch (e) {
          console.error("Could not save learned cards:", e);
        }
        updateGlobalLearnedDisplays();
      }

      function updateGlobalLearnedDisplays() {
        const totalLearned = learnedCardsSet.size;
        const totalWords = 3000;
        const totalPct = Math.min(100, ((totalLearned / totalWords) * 100)).toFixed(1);

        // Calculate count within active tier (800 - 1000)
        let tier800Learned = 0;
        if (typeof cards !== "undefined") {
          cards.forEach(c => {
            if (learnedCardsSet.has(c.num)) tier800Learned++;
          });
        }
        const tierPct = Math.min(100, ((tier800Learned / 200) * 100)).toFixed(0);

        // Update Home Screen displays
        const home3kCountEl = document.getElementById("home-3k-status-count");
        if (home3kCountEl) home3kCountEl.textContent = totalLearned.toLocaleString();

        const card3kLearnedCountEl = document.getElementById("card-3k-learned-count");
        if (card3kLearnedCountEl) card3kLearnedCountEl.textContent = totalLearned.toLocaleString();

        const card3kLearnedPctEl = document.getElementById("card-3k-learned-pct");
        if (card3kLearnedPctEl) card3kLearnedPctEl.textContent = \`\${totalPct}%\`;

        const progressFill3kTotal = document.getElementById("progress-fill-3k-total");
        if (progressFill3kTotal) progressFill3kTotal.style.width = \`\${Math.max(1, totalPct)}%\`;

        const tier800LearnedStat = document.getElementById("tier-800-learned-stat");
        if (tier800LearnedStat) tier800LearnedStat.textContent = \`\${tier800Learned} / 200 learned in tier\`;

        // Update Subsections displays
        const subsections3kTotal = document.getElementById("subsections-3k-total");
        if (subsections3kTotal) subsections3kTotal.textContent = totalLearned.toLocaleString();

        const tier800StatLine = document.getElementById("tier-800-stat-line");
        if (tier800StatLine) tier800StatLine.textContent = \`\${tier800Learned} / 200 Learned\`;

        const tier800ProgressBar = document.getElementById("tier-800-progress-bar");
        if (tier800ProgressBar) tier800ProgressBar.style.width = \`\${tierPct}%\`;

        // Update Flashcard top status
        const flashcard3kStatusText = document.getElementById("flashcard-3k-status-text");
        if (flashcard3kStatusText) flashcard3kStatusText.textContent = \`\${totalLearned} / 3,000\`;
      }

      function toggleCardLearned(cardNum) {
        if (!cardNum) return;
        const isNowLearned = !learnedCardsSet.has(cardNum);
        if (isNowLearned) {
          learnedCardsSet.add(cardNum);
          playHapticTick(680, "triangle", 0.05);
          showToast(\`Card #\${cardNum} marked learned! (Status: \${learnedCardsSet.size} / 3,000)\`);
        } else {
          learnedCardsSet.delete(cardNum);
          playHapticTick(380, "sine", 0.04);
          showToast(\`Card #\${cardNum} unmarked\`);
        }
        saveLearnedCards();
        updateCardLearnedUI(cardNum);
      }

      function updateCardLearnedUI(cardNum) {
        const isLearned = learnedCardsSet.has(cardNum);

        // Flashcard front face button
        const btnCardLearnedAction = document.getElementById("btn-card-learned-action");
        const frontLearnedText = document.getElementById("front-learned-text");
        if (btnCardLearnedAction) {
          if (isLearned) {
            btnCardLearnedAction.classList.add("is-learned");
            if (frontLearnedText) frontLearnedText.textContent = "Learned ✓";
          } else {
            btnCardLearnedAction.classList.remove("is-learned");
            if (frontLearnedText) frontLearnedText.textContent = "Mark Learned";
          }
        }

        // Top bar button
        const btnTopLearnedToggle = document.getElementById("btn-top-learned-toggle");
        if (btnTopLearnedToggle) {
          if (isLearned) {
            btnTopLearnedToggle.classList.add("is-learned");
          } else {
            btnTopLearnedToggle.classList.remove("is-learned");
          }
        }
      }

      /* ==========================================================
         RESUME POSITION SYSTEM (Redirects directly to left-off card)
         ========================================================== */
      function getLastCardNumber() {
        try {
          const val = localStorage.getItem(LAST_CARD_STORAGE_KEY);
          if (val) return parseInt(val, 10);
        } catch (e) {}
        return 800;
      }

      function setLastCardNumber(num) {
        try {
          localStorage.setItem(LAST_CARD_STORAGE_KEY, num);
        } catch (e) {}
        const resumeLabel = document.getElementById("btn-resume-label");
        if (resumeLabel) resumeLabel.textContent = \`Resume (#\${num})\`;
      }

      function resumeStudyDeck() {
        const targetNum = getLastCardNumber();
        const foundIdx = cards.findIndex(c => c.num === targetNum);
        if (foundIdx !== -1) {
          currentIndex = foundIdx;
        } else {
          currentIndex = 0;
        }
        isFlipped = false;
        switchScreen("screen-flashcard");
        renderCurrentCard();
        showToast(\`Resumed at Card #\${cards[currentIndex].num}: \${cards[currentIndex].word}\`);
      }

      /* ==========================================================
         WIRE UP BUTTONS, RESUME, AND SUBSECTIONS
         ========================================================== */
      window.addEventListener("DOMContentLoaded", () => {
        // Resume Button on 3K Featured Card -> DIRECT REDIRECT to left-off card
        const btnResume3k = document.getElementById("btn-resume-3k-deck");
        if (btnResume3k) {
          btnResume3k.addEventListener("click", (e) => {
            e.stopPropagation();
            resumeStudyDeck();
          });
        }

        // Resume Button on Subsections Screen -> DIRECT REDIRECT
        const btnResumeSubsections = document.getElementById("btn-resume-from-subsections");
        if (btnResumeSubsections) {
          btnResumeSubsections.addEventListener("click", (e) => {
            e.stopPropagation();
            resumeStudyDeck();
          });
        }

        // Tapping '3k Vocabulary' card body or label -> OPENS SUBSECTIONS (800 - 1000)
        const card3kFeatured = document.getElementById("card-3k-featured");
        if (card3kFeatured) {
          card3kFeatured.addEventListener("click", (e) => {
            if (e.target.closest("button")) return;
            switchScreen("screen-subsections");
          });
        }

        // Open Subsections Button
        const btnOpenSubsections = document.getElementById("btn-open-subsections");
        if (btnOpenSubsections) {
          btnOpenSubsections.addEventListener("click", (e) => {
            e.stopPropagation();
            switchScreen("screen-subsections");
          });
        }

        // Tapping Active Tier 800-1000 in Subsections -> OPENS FLASHCARD
        const subTier800_1000 = document.getElementById("sub-tier-800-1000");
        if (subTier800_1000) {
          subTier800_1000.addEventListener("click", () => {
            switchScreen("screen-flashcard");
            renderCurrentCard();
          });
        }

        // Tapping other tiers in Subsections
        const allOtherTiers = document.querySelectorAll(".custom-section-card[id^='sub-tier-']:not(#sub-tier-800-1000)");
        allOtherTiers.forEach(tierCard => {
          tierCard.addEventListener("click", () => {
            showToast("Tier in preparation. Switching to Active Study Deck: Cards 800 – 1000");
            setTimeout(() => {
              switchScreen("screen-flashcard");
              renderCurrentCard();
            }, 500);
          });
        });

        // Learned Action Buttons on Flashcard
        const btnCardLearnedAction = document.getElementById("btn-card-learned-action");
        if (btnCardLearnedAction) {
          btnCardLearnedAction.addEventListener("click", (e) => {
            e.stopPropagation();
            const currCard = cards[currentIndex];
            if (currCard) toggleCardLearned(currCard.num);
          });
        }

        const btnTopLearnedToggle = document.getElementById("btn-top-learned-toggle");
        if (btnTopLearnedToggle) {
          btnTopLearnedToggle.addEventListener("click", (e) => {
            e.stopPropagation();
            const currCard = cards[currentIndex];
            if (currCard) toggleCardLearned(currCard.num);
          });
        }

        // Desktop Navigation Links
        const desktopNavHome = document.getElementById("desktop-nav-home");
        if (desktopNavHome) desktopNavHome.addEventListener("click", () => switchScreen("screen-home"));

        const desktopNav3k = document.getElementById("desktop-nav-3k");
        if (desktopNav3k) desktopNav3k.addEventListener("click", () => switchScreen("screen-subsections"));

        const desktopNavSubsections = document.getElementById("desktop-nav-subsections");
        if (desktopNavSubsections) desktopNavSubsections.addEventListener("click", () => switchScreen("screen-subsections"));

        const desktopNavSections = document.getElementById("desktop-nav-sections");
        if (desktopNavSections) {
          desktopNavSections.addEventListener("click", () => {
            switchScreen("screen-home");
            const secGrid = document.getElementById("sections-grid");
            if (secGrid) secGrid.scrollIntoView({ behavior: "smooth" });
          });
        }

        // Settings Buttons -> Open Menu Drawer / Settings Modal
        const btnHomeSettings = document.getElementById("btn-home-settings");
        if (btnHomeSettings) btnHomeSettings.addEventListener("click", openMenuDrawer);

        const btnDesktopSettings = document.getElementById("btn-desktop-settings");
        if (btnDesktopSettings) btnDesktopSettings.addEventListener("click", openMenuDrawer);

        // Mobile Hamburger Buttons (On FAR LEFT CORNER of each screen)
        const btnSubsectionsMenu = document.getElementById("btn-subsections-menu");
        if (btnSubsectionsMenu) btnSubsectionsMenu.addEventListener("click", openMenuDrawer);

        // Initial setup
        updateGlobalLearnedDisplays();
        const initLastCard = getLastCardNumber();
        setLastCardNumber(initLastCard);
      });
`;

// Hook into renderCurrentCard to update card learned state and last visited card
const oldRenderCall = 'function renderCurrentCard() {';
const newRenderCall = `function renderCurrentCard() {
        const currentCardObj = cards[currentIndex];
        if (currentCardObj) {
          setLastCardNumber(currentCardObj.num);
          updateCardLearnedUI(currentCardObj.num);
        }`;

html = html.replace(oldRenderCall, newRenderCall);

// Insert modernLogicJS right before </script>
html = html.replace('</script>', `${modernLogicJS}\n</script>`);
console.log('Injected modern logic JS.');

fs.writeFileSync('index.html', html, 'utf8');
console.log('Successfully written index.html with styles and logic!');
