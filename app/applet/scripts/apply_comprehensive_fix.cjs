const fs = require('fs');
const path = require('path');

const indexPath = path.join(__dirname, '..', 'index.html');
let html = fs.readFileSync(indexPath, 'utf8');

console.log('Original index.html length:', html.length);

// =========================================================================
// 1. CLEAN UP CSS: Remove all duplicated style blocks between 251767 and </style>
// =========================================================================
const dupCssMarker = "/* ========================================================================= */\n    /* ZERO-SCROLL GUARANTEE: FIXED VIEWPORT SCREEN ARCHITECTURE";
const styleEndMarker = "</style>";

const dupCssPos = html.indexOf("/* ZERO-SCROLL GUARANTEE: FIXED VIEWPORT SCREEN ARCHITECTURE");
const styleEndPos = html.indexOf(styleEndMarker);

if (dupCssPos === -1 || styleEndPos === -1) {
  console.error("Could not find style cut locations!");
  process.exit(1);
}

console.log(`Replacing duplicate styles from ${dupCssPos} to ${styleEndPos} (${styleEndPos - dupCssPos} chars)...`);

const cleanResponsiveCss = `    /* ========================================================================= */
    /* PRODUCTION-GRADE ZERO-SCROLL ALL-DEVICE FLASHCARD VIEWPORT SYSTEM         */
    /* ========================================================================= */
    body.in-flashcard-mode,
    html.in-flashcard-mode {
      overflow: hidden !important;
      position: fixed !important;
      inset: 0 !important;
      width: 100% !important;
      height: 100% !important;
      height: 100dvh !important;
      max-height: 100dvh !important;
      margin: 0 !important;
      padding: 0 !important;
    }
    body.in-flashcard-mode #app-container,
    body.in-flashcard-mode .app-main-viewport {
      overflow: hidden !important;
      position: fixed !important;
      inset: 0 !important;
      width: 100% !important;
      height: 100% !important;
      height: 100dvh !important;
      max-height: 100dvh !important;
      min-height: 0 !important;
      padding: 0 !important;
      margin: 0 !important;
    }
    body.in-flashcard-mode .mobile-bottom-nav,
    body.in-flashcard-mode .mobile-top-bar,
    body.in-flashcard-mode .desktop-top-header,
    body.in-flashcard-mode .app-desktop-sidebar {
      display: none !important;
      visibility: hidden !important;
    }

    #screen-flashcard.active-screen {
      position: fixed !important;
      top: 0 !important;
      left: 0 !important;
      right: 0 !important;
      bottom: 0 !important;
      width: 100% !important;
      height: 100% !important;
      height: 100dvh !important;
      max-height: 100dvh !important;
      min-height: 0 !important;
      background: #060b13 !important;
      z-index: 99999 !important;
      display: flex !important;
      flex-direction: column !important;
      justify-content: space-between !important;
      align-items: center !important;
      padding: env(safe-area-inset-top, 6px) 12px env(safe-area-inset-bottom, 8px) !important;
      box-sizing: border-box !important;
      overflow: hidden !important;
    }

    /* Fixed 44px Top Nav */
    #screen-flashcard .flashcard-top-nav {
      flex: 0 0 44px !important;
      width: 100% !important;
      max-width: 480px !important;
      height: 44px !important;
      min-height: 44px !important;
      max-height: 44px !important;
      display: flex !important;
      flex-direction: column !important;
      justify-content: center !important;
      margin: 0 auto !important;
      padding: 0 !important;
      box-sizing: border-box !important;
      overflow: hidden !important;
    }
    #screen-flashcard .top-nav-main {
      display: flex !important;
      align-items: center !important;
      justify-content: space-between !important;
      width: 100% !important;
      padding: 0 !important;
      margin: 0 !important;
    }

    /* Pinned 52px Bottom Navigation Controls (ALWAYS 100% Visible & Accessible) */
    #screen-flashcard .nav-controls {
      flex: 0 0 52px !important;
      width: 100% !important;
      max-width: 480px !important;
      height: 52px !important;
      min-height: 52px !important;
      max-height: 52px !important;
      margin: 0 auto !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      gap: 16px !important;
      padding: 0 !important;
      box-sizing: border-box !important;
    }
    #screen-flashcard .nav-btn-flip-cobalt {
      height: 46px !important;
      padding: 0 34px !important;
      font-size: 0.98rem !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      gap: 8px !important;
      font-family: inherit !important;
      font-weight: 800 !important;
      border-radius: 14px !important;
      cursor: pointer !important;
    }
    #screen-flashcard .nav-chevron-btn {
      width: 46px !important;
      height: 46px !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      border-radius: 14px !important;
      cursor: pointer !important;
    }

    /* Middle Stage: Takes EXACT remaining height between top nav and bottom controls */
    #screen-flashcard .card-stage {
      flex: 1 1 0 !important;
      min-height: 0 !important;
      height: auto !important;
      width: 100% !important;
      max-width: 480px !important;
      margin: 0 auto !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      overflow: hidden !important;
      padding: 4px 0 !important;
      box-sizing: border-box !important;
      position: relative !important;
    }

    /* Card Wrapper: Auto-fitted dynamically, strictly bounded by stage */
    #screen-flashcard .flashcard-wrapper {
      max-width: 100% !important;
      max-height: 100% !important;
      position: relative !important;
      margin: auto !important;
      display: block !important;
      cursor: pointer !important;
      user-select: none !important;
      -webkit-user-select: none !important;
      border-radius: 20px !important;
      box-sizing: border-box !important;
      transform-style: preserve-3d !important;
    }

    #screen-flashcard .card-face {
      position: absolute !important;
      inset: 0 !important;
      width: 100% !important;
      height: 100% !important;
      display: flex !important;
      flex-direction: column !important;
      justify-content: space-between !important;
      padding: 10px 14px 12px !important;
      box-sizing: border-box !important;
      border-radius: 20px !important;
      background: #111726 !important;
      border: 1.5px solid rgba(255, 255, 255, 0.12) !important;
      box-shadow: 0 14px 36px -6px rgba(0, 0, 0, 0.75) !important;
      overflow: hidden !important;
      backface-visibility: hidden !important;
      -webkit-backface-visibility: hidden !important;
    }

    #screen-flashcard .card-header-bar {
      flex: 0 0 32px !important;
      height: 32px !important;
      display: flex !important;
      align-items: center !important;
      justify-content: space-between !important;
      margin-bottom: 4px !important;
      width: 100% !important;
    }

    /* Front Face Layout: High-definition visual + bold target word */
    #screen-flashcard .front-content {
      flex: 1 1 0 !important;
      min-height: 0 !important;
      display: flex !important;
      flex-direction: column !important;
      align-items: center !important;
      justify-content: space-between !important;
      width: 100% !important;
      gap: 6px !important;
      overflow: hidden !important;
    }

    #screen-flashcard .visual-box {
      flex: 1 1 0 !important;
      min-height: 0 !important;
      width: 100% !important;
      border-radius: 14px !important;
      overflow: hidden !important;
      background: #080c14 !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      position: relative !important;
    }

    #screen-flashcard .visual-img {
      width: 100% !important;
      height: 100% !important;
      object-fit: contain !important;
      background: #080c14 !important;
    }

    #screen-flashcard .target-word-container {
      flex: 0 0 auto !important;
      padding: 2px 0 0 !important;
      text-align: center !important;
    }

    #screen-flashcard .target-word-title {
      font-size: clamp(1.4rem, 4.5vw, 2.1rem) !important;
      font-weight: 850 !important;
      letter-spacing: -0.01em !important;
      margin: 0 !important;
      color: #ffffff !important;
      line-height: 1.15 !important;
    }

    /* Back Face Layout */
    #screen-flashcard .card-face-back {
      transform: rotateY(180deg) !important;
    }
    #screen-flashcard .back-content {
      flex: 1 1 0 !important;
      min-height: 0 !important;
      display: flex !important;
      flex-direction: column !important;
      justify-content: space-between !important;
      gap: 6px !important;
      width: 100% !important;
      overflow-y: auto !important;
      scrollbar-width: thin !important;
      scrollbar-color: rgba(255,255,255,0.2) transparent !important;
    }
    #screen-flashcard .tamil-hero-card {
      flex: 0 0 auto !important;
      margin: 0 !important;
      padding: 8px 12px !important;
    }
    #screen-flashcard .translations-grid {
      flex: 0 0 auto !important;
      gap: 6px !important;
      margin: 0 !important;
    }
    #screen-flashcard .shortcut-section {
      flex: 0 0 auto !important;
      margin: 0 !important;
    }
    #screen-flashcard .shortcut-grid {
      gap: 6px !important;
    }`;

html = html.slice(0, dupCssPos) + cleanResponsiveCss + '\n  ';

// =========================================================================
// 2. REQUIREMENT 1: Remove "tier 800-100" text, add Learn / Tick symbol count
// =========================================================================

// (A) In Home Screen: Replace "Active Focus: Cards 800 – 1000" and "0 / 200 in active tier"
const oldHomeHintRegex = /<div class="progress-tier-hint"[\s\S]*?<span>Active Focus: <strong>Cards 800 – 1000<\/strong><\/span>[\s\S]*?<span id="tier-800-learned-stat">[\s\S]*?<\/div>/;
const newHomeHint = `<div class="progress-tier-hint" style="display: flex; justify-content: space-between; align-items: center; font-size: 0.85rem; color: #94a3b8; margin-top: 6px;">
                        <span style="display: flex; align-items: center; gap: 6px; font-weight: 700; color: #f1f5f9;"><span style="color: #10b981; font-size: 1.15rem; font-weight: 900; line-height: 1;">✓</span> <span>Learned Progress</span></span>
                        <span id="tier-800-learned-stat" style="font-weight: 800; color: #34d399; background: rgba(16, 185, 129, 0.16); border: 1px solid rgba(16, 185, 129, 0.4); padding: 3px 12px; border-radius: 9999px;">0 / 200 Learned</span>
                      </div>`;

if (oldHomeHintRegex.test(html)) {
  html = html.replace(oldHomeHintRegex, newHomeHint);
  console.log('Successfully replaced Home hint with green tick learned counter!');
} else {
  console.log('Notice: Home hint regex did not match directly, trying substring replacement');
  html = html.replace('<span>Active Focus: <strong>Cards 800 – 1000</strong></span>', '<span style="display: flex; align-items: center; gap: 6px; font-weight: 700; color: #f1f5f9;"><span style="color: #10b981; font-size: 1.15rem; font-weight: 900;">✓</span> <span>Learned Progress</span></span>');
  html = html.replace('<span id="tier-800-learned-stat">0 / 200 in active tier</span>', '<span id="tier-800-learned-stat" style="font-weight: 800; color: #34d399; background: rgba(16, 185, 129, 0.16); border: 1px solid rgba(16, 185, 129, 0.4); padding: 3px 12px; border-radius: 9999px;">0 / 200 Learned</span>');
}

// (B) In Subsections Screen: Remove "Active Recommended Tier" and "Cards 800 – 1000 (Active)"
html = html.replace(
  '<div style="font-size: 0.76rem; font-weight: 800; letter-spacing: 0.08em; color: #38bdf8; text-transform: uppercase;">Active Recommended Tier</div>',
  '<div style="display: inline-flex; align-items: center; gap: 6px; font-size: 0.78rem; font-weight: 800; letter-spacing: 0.06em; color: #34d399; text-transform: uppercase; margin-bottom: 2px;"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg><span>Active Vocabulary Deck</span></div>'
);

html = html.replace(
  '<h3 style="font-size: 1.4rem; font-weight: 800; color: #ffffff; margin: 3px 0 5px;">Cards 800 – 1000 (Active)</h3>',
  '<h3 style="font-size: 1.45rem; font-weight: 800; color: #ffffff; margin: 2px 0 5px;">3K Vocabulary · Core Deck</h3>'
);

html = html.replace(
  '<div style="font-size: 0.88rem; color: #cbd5e1;">Kitchen, Dining, Appliances & Daily Life · 200 Words</div>',
  '<div style="font-size: 0.88rem; color: #cbd5e1;">Kitchen, Dining, Appliances & Daily Essentials · 200 Words</div>'
);

// In the bottom row of the subsections card:
html = html.replace(
  '<span id="tier-800-stat-line" style="font-size: 0.85rem; font-weight: 700; color: #38bdf8;">0 / 200 Learned</span>',
  '<div style="display: inline-flex; align-items: center; gap: 6px; padding: 4px 12px; background: rgba(16, 185, 129, 0.18); border: 1.5px solid rgba(16, 185, 129, 0.45); border-radius: 9999px;"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg><span id="tier-800-stat-line" style="font-size: 0.88rem; font-weight: 800; color: #34d399;">0 / 200 Learned</span></div>'
);

// Subsections progress bar color to Duolingo green
html = html.replace(
  '<div id="tier-800-progress-bar" style="width: 0%; height: 100%; background: #38bdf8; border-radius: 9999px;"></div>',
  '<div id="tier-800-progress-bar" style="width: 0%; height: 100%; background: #10b981; border-radius: 9999px;"></div>'
);

// Sidebar button & footer labels
html = html.replace('title="3k Vocabulary (800 – 1000)"', 'title="3k Vocabulary"');
html = html.replace('3,000 Words · 800–1000 Active', '3,000 Words · Core Deck');
html = html.replace('3k Vocabulary · Select Subsection Tier', '3k Vocabulary · Core Deck');
html = html.replace('Cards 800 – 1000 (Active)', '3K Vocabulary · Core Deck');
html = html.replace('(800–1000)', '');

// Update JS text update in updateGlobalLearnedDisplays
html = html.replace(
  'if (tier800LearnedStat) tier800LearnedStat.textContent = `${tier800Learned} / 200 learned in tier`;',
  'if (tier800LearnedStat) tier800LearnedStat.textContent = `${tier800Learned} / 200 Learned`;'
);

// =========================================================================
// 3. CLEAN UP SCRIPT TAIL: Remove duplicate listeners & inject AutoFit Engine
// =========================================================================
const doubleTapTailMarker = "// =========================================================================\n      // STRICT DOUBLE-TAP TO FLIP ONLY";
let dtPos = html.indexOf("// STRICT DOUBLE-TAP TO FLIP ONLY (Single tap ignored; debounce locked)");
if (dtPos === -1) {
  dtPos = html.indexOf("// STRICT DOUBLE-TAP TO FLIP ONLY");
}
const lastScriptTagPos = html.lastIndexOf("</script>");

if (dtPos !== -1 && lastScriptTagPos !== -1) {
  console.log(`Removing duplicate tail listeners from ${dtPos} to ${lastScriptTagPos}...`);
  html = html.slice(0, dtPos) + html.slice(lastScriptTagPos);
}

// Ensure flipCard has a debounce lock
html = html.replace(
  'function flipCard() {        if (isAnimating) return;        isFlipped = !isFlipped;',
  'function flipCard() {        if (isAnimating) return;        isAnimating = true; setTimeout(() => { isAnimating = false; }, 360);        isFlipped = !isFlipped;'
);

// Inject the Master Device Auto-Fit Engine and Single Clean Gesture System
const masterDeviceAutoFitEngine = `
      // =========================================================================
      // DYNAMIC ALL-DEVICE FLASHCARD AUTO-FIT ENGINE (ZERO VERTICAL SCROLL)
      // =========================================================================
      (function() {
        function autoFitFlashcard() {
          const screen = document.getElementById("screen-flashcard");
          if (!screen || !screen.classList.contains("active-screen")) return;
          const stage = screen.querySelector(".card-stage");
          const wrapper = screen.querySelector(".flashcard-wrapper");
          if (!stage || !wrapper) return;

          const availW = stage.clientWidth;
          const availH = stage.clientHeight;
          if (availW <= 0 || availH <= 0) return;

          // Ideal flashcard proportion: width / height = 0.74 (standard 3.7 : 5 card ratio)
          const ratio = 0.74;
          const maxW = 430;
          const maxH = 560;

          // Deduct 8px padding
          const targetAvailH = Math.min(availH - 8, maxH);
          const targetAvailW = Math.min(availW - 8, maxW);

          // Calculate height-constrained size
          let h = targetAvailH;
          let w = h * ratio;

          // If calculated width overflows stage, switch to width-constrained size
          if (w > targetAvailW) {
            w = targetAvailW;
            h = w / ratio;
          }

          // Ensure it strictly never exceeds stage height
          if (h > availH - 8) {
            h = availH - 8;
            w = h * ratio;
          }

          wrapper.style.width = Math.round(w) + "px";
          wrapper.style.height = Math.round(h) + "px";
        }

        // Attach resize listeners
        window.addEventListener("resize", autoFitFlashcard);
        window.addEventListener("orientationchange", () => {
          setTimeout(autoFitFlashcard, 60);
        });

        if (window.ResizeObserver) {
          const stageEl = document.querySelector("#screen-flashcard .card-stage");
          if (stageEl) {
            const ro = new ResizeObserver(() => {
              autoFitFlashcard();
            });
            ro.observe(stageEl);
          }
        }

        // Hook into screen switching and card rendering
        const prevSwitch = window.switchScreen;
        window.switchScreen = function(id) {
          if (typeof prevSwitch === "function") prevSwitch(id);
          if (id === "screen-flashcard") {
            setTimeout(autoFitFlashcard, 20);
            setTimeout(autoFitFlashcard, 150);
          }
        };

        const prevRender = window.renderCurrentCard;
        window.renderCurrentCard = function() {
          if (typeof prevRender === "function") prevRender();
          autoFitFlashcard();
        };

        // Run immediately when loaded
        if (document.readyState === "complete") {
          autoFitFlashcard();
        } else {
          window.addEventListener("load", autoFitFlashcard);
        }
      })();

      // =========================================================================
      // SYNCHRONIZE LEARNED TICK COUNTERS ACROSS ALL SCREENS
      // =========================================================================
      (function() {
        function syncAllLearnedCounters() {
          let count = 0;
          if (typeof getSectionLearnedCount === "function") {
            count = getSectionLearnedCount();
          } else if (typeof learnedCardsSet !== "undefined" && learnedCardsSet) {
            count = learnedCardsSet.size;
          }
          const total = (typeof cards !== "undefined" && cards.length) ? cards.length : 200;

          const topLearnedCount = document.getElementById("flashcard-learned-count");
          if (topLearnedCount) topLearnedCount.textContent = count;

          const topTotal = document.getElementById("flashcard-deck-total");
          if (topTotal) topTotal.textContent = total;

          const tierStatLine = document.getElementById("tier-800-stat-line");
          if (tierStatLine) tierStatLine.textContent = count + " / " + total + " Learned";

          const homeStat = document.getElementById("tier-800-learned-stat");
          if (homeStat) homeStat.textContent = count + " / " + total + " Learned";

          const tierBar = document.getElementById("tier-800-progress-bar");
          if (tierBar && total > 0) {
            tierBar.style.width = Math.min(100, Math.round((count / total) * 100)) + "%";
          }
        }

        const prevSave = window.saveLearnedCards;
        window.saveLearnedCards = function() {
          if (typeof prevSave === "function") prevSave();
          syncAllLearnedCounters();
        };

        const prevRender = window.renderCurrentCard;
        window.renderCurrentCard = function() {
          if (typeof prevRender === "function") prevRender();
          syncAllLearnedCounters();
        };

        syncAllLearnedCounters();
      })();
`;

const finalScriptEnd = html.lastIndexOf('</script>');
html = html.slice(0, finalScriptEnd) + masterDeviceAutoFitEngine + '\n    ' + html.slice(finalScriptEnd);

fs.writeFileSync(indexPath, html, 'utf8');
console.log('Successfully updated index.html! New length:', html.length);
