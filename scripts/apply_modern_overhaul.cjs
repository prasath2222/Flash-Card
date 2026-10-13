const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

console.log('Original html length:', html.length);

// 1. UPDATE CSS STYLES FOR MODERN DESIGN
// Remove ambient glowing blob
html = html.replace(/\/\* Ambient glowing background aura \*\/[\s\S]*?body::before\s*\{[\s\S]*?\}\s*/, `/* Modern Clean Slate Background */
      body {
        background: radial-gradient(circle at 50% 0%, #111726 0%, #090d15 70%);
      }
`);

// Clean top nav and header in Screen 3
const modernTopNavCss = `
      /* ==========================================================
         Unified Modern Top Navigation (Single Header, No Duplication)
         ========================================================== */
      .flashcard-top-nav {
        display: flex;
        flex-direction: column;
        gap: 8px;
        padding: 4px 6px 10px;
        flex-shrink: 0;
      }

      .top-nav-main {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
      }

      .breadcrumb-back-btn {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        color: #94a3b8;
        font-size: 0.8rem;
        font-weight: 600;
        cursor: pointer;
        padding: 6px 12px;
        transition: all 0.18s ease;
      }

      .breadcrumb-back-btn:hover,
      .breadcrumb-back-btn:active {
        background: rgba(255, 255, 255, 0.09);
        color: #ffffff;
        border-color: rgba(255, 255, 255, 0.16);
      }

      .top-category-pill {
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.02em;
        color: #cbd5e1;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 5px 12px;
        border-radius: 9999px;
        max-width: 200px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }

      .top-nav-actions {
        display: flex;
        align-items: center;
        gap: 8px;
      }

      .counter-display {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 5px 11px;
        border-radius: 12px;
        font-variant-numeric: tabular-nums;
        font-size: 0.82rem;
        font-weight: 650;
        color: #e2e8f0;
      }

      .counter-display .current-num {
        color: #38bdf8;
        font-weight: 750;
      }

      .counter-display .counter-divider {
        color: #475569;
        font-weight: 400;
      }

      .counter-display .total-num {
        color: #94a3b8;
      }

      /* Slim, refined 2.5px progress line */
      .progress-track {
        position: relative;
        width: 100%;
        height: 3px;
        background: rgba(255, 255, 255, 0.08);
        border-radius: 9999px;
        overflow: hidden;
      }

      .progress-fill {
        height: 100%;
        width: 0%;
        background: linear-gradient(90deg, #2563eb 0%, #38bdf8 60%, #10b981 100%);
        border-radius: 9999px;
        transition: width 0.35s cubic-bezier(0.25, 1, 0.5, 1);
      }
`;

// Replace or augment top nav CSS
if (!html.includes('.flashcard-top-nav')) {
  html = html.replace('/* Header */', `${modernTopNavCss}\n\n      /* Legacy Header fallback */`);
}

// Modern Card Face Styling (Deep obsidian, crisp border, elegant shadow)
const cardFaceModernCss = `
      .card-face {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        border-radius: 24px;
        background: #111724;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 20px 48px -12px rgba(0, 0, 0, 0.8),
                    inset 0 1px 0 rgba(255, 255, 255, 0.08);
        backface-visibility: hidden;
        -webkit-backface-visibility: hidden;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 20px 18px 16px;
        overflow: hidden;
        transition: border-color 0.22s ease, box-shadow 0.22s ease;
      }

      .card-face-front {
        transform: rotateY(0deg);
        -webkit-transform: rotateY(0deg);
        z-index: 2;
      }

      .card-face-back {
        transform: rotateY(180deg);
        -webkit-transform: rotateY(180deg);
        z-index: 1;
        background: #0f1522;
      }
`;
html = html.replace(/\.card-face\s*\{[\s\S]*?\.card-face-back\s*\{[\s\S]*?\}/, cardFaceModernCss.trim());

// Visual Box refinement (Clean framed photo, no cartoon sketches or pill badge)
const visualBoxModernCss = `
      .visual-box {
        position: relative;
        width: 100%;
        max-width: 330px;
        height: 184px;
        max-height: 29vh;
        border-radius: 18px;
        background: #080c14;
        border: 1px solid rgba(255, 255, 255, 0.08);
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        box-shadow: 0 12px 30px -8px rgba(0, 0, 0, 0.65),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
      }

      .visual-skeleton {
        position: absolute;
        inset: 0;
        background: linear-gradient(90deg, #0e1422 0%, #1a2336 50%, #0e1422 100%);
        background-size: 200% 100%;
        animation: visualShimmer 1.8s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        z-index: 2;
        pointer-events: none;
      }

      .visual-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        display: block;
        opacity: 0;
        transform: scale(1.01);
        transition: opacity 0.35s ease, transform 0.4s ease;
      }

      .visual-img.loaded {
        opacity: 1;
        transform: scale(1);
      }

      .visual-vignette {
        position: absolute;
        inset: 0;
        pointer-events: none;
        z-index: 3;
        background: linear-gradient(180deg, rgba(8, 12, 20, 0.05) 0%, rgba(8, 12, 20, 0.65) 100%);
      }
`;
html = html.replace(/\.visual-box\s*\{[\s\S]*?\.visual-vignette\s*\{[\s\S]*?\}/, visualBoxModernCss.trim());

// Target word styling: Clean, Bold, Minimal (NO 'English' label)
const targetWordModernCss = `
      .target-word-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding-top: 4px;
      }

      .target-word {
        font-size: clamp(2.4rem, 8vw, 3.2rem);
        font-weight: 850;
        letter-spacing: -0.025em;
        line-height: 1.1;
        color: #ffffff;
        margin: 0;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.4);
      }
`;
html = html.replace(/\.target-word-container\s*\{[\s\S]*?\.target-word\s*\{[\s\S]*?\}/, targetWordModernCss.trim());

// Card footer hint & double-tap cue
const cardFooterModernCss = `
      .card-hint-footer {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
        font-size: 0.76rem;
        font-weight: 600;
        color: #64748b;
        letter-spacing: 0.04em;
        padding-top: 10px;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        flex-shrink: 0;
        transition: color 0.22s ease, transform 0.22s ease;
      }

      .card-hint-footer.cue-highlight {
        color: #38bdf8 !important;
        transform: scale(1.05);
      }

      .hint-icon {
        font-size: 0.85rem;
        color: inherit;
      }
`;
html = html.replace(/\.card-hint-footer\s*\{[\s\S]*?\.flashcard-wrapper:hover\s*\.hint-icon\s*\{[\s\S]*?\}/, cardFooterModernCss.trim());

// Mnemonic Section Styles (NO "Memory Shortcuts" banner label)
const mnemonicSectionModernCss = `
      .shortcut-section {
        display: flex;
        flex-direction: column;
        gap: 8px;
        background: rgba(255, 255, 255, 0.025);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 11px 13px;
      }

      .shortcut-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 8px;
        padding-bottom: 5px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
      }

      .mnemonic-kicker {
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: #94a3b8;
      }

      .shortcut-quick-edit-btn {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.09);
        border-radius: 9999px;
        color: #94a3b8;
        font-size: 0.68rem;
        font-weight: 650;
        padding: 2px 8px;
        cursor: pointer;
        transition: all 0.15s ease;
      }

      .shortcut-quick-edit-btn:hover,
      .shortcut-quick-edit-btn:active {
        background: rgba(56, 189, 248, 0.16);
        color: #38bdf8;
        border-color: rgba(56, 189, 248, 0.35);
      }

      .shortcut-grid {
        display: flex;
        flex-direction: column;
        gap: 6px;
      }

      .shortcut-box {
        display: flex;
        flex-direction: column;
        gap: 3px;
        padding: 7px 11px;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.025);
        border: 1px solid rgba(255, 255, 255, 0.05);
      }

      .shortcut-box-es {
        border-left: 3px solid #f43f5e;
        background: rgba(244, 63, 94, 0.05);
      }

      .shortcut-box-hi {
        border-left: 3px solid #f59e0b;
        background: rgba(245, 158, 11, 0.05);
      }

      .shortcut-box-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 6px;
      }

      .shortcut-lang-label {
        font-size: 0.65rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
      }

      .shortcut-lang-label.tag-es {
        color: #fda4af;
      }

      .shortcut-lang-label.tag-hi {
        color: #fde68a;
      }

      .shortcut-target-word {
        font-size: 0.74rem;
        font-weight: 700;
        color: #e2e8f0;
        font-family: monospace;
        background: rgba(0, 0, 0, 0.3);
        padding: 1px 6px;
        border-radius: 5px;
      }

      .shortcut-punchline {
        font-size: 0.8rem;
        line-height: 1.35;
        color: #cbd5e1;
      }

      .shortcut-punchline strong {
        color: #ffffff;
        font-weight: 750;
      }

      .shortcut-punchline em {
        color: #38bdf8;
        font-style: normal;
        font-weight: 600;
      }
`;
html = html.replace(/\.shortcut-section\s*\{[\s\S]*?\.shortcut-punchline em\s*\{[\s\S]*?\}/, mnemonicSectionModernCss.trim());

// Tamil Hero Card refinement
const tamilHeroCardModernCss = `
      .tamil-hero-card {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 12px 16px;
        border-radius: 16px;
        background: rgba(16, 185, 129, 0.08);
        border: 1px solid rgba(16, 185, 129, 0.24);
        text-align: center;
      }

      .tamil-script-display {
        font-size: clamp(2rem, 7vw, 2.7rem);
        font-weight: 800;
        color: #34d399;
        letter-spacing: 0.02em;
        line-height: 1.25;
      }

      .lang-tag {
        font-size: 0.67rem;
        font-weight: 750;
        letter-spacing: 0.06em;
        text-transform: uppercase;
      }

      .lang-tag.tag-es { color: #fda4af; }
      .lang-tag.tag-hi { color: #fde68a; }
`;
html = html.replace(/\.tamil-hero-card\s*\{[\s\S]*?\.tamil-script-display\s*\{[\s\S]*?\}/, tamilHeroCardModernCss.trim());


// 2. REPLACE SCREEN 3 HTML IN ITS ENTIRETY
// Find starting at <!-- SCREEN 3: and ending at </main>
const screen3StartPattern = /<!-- ========================================== -->\s*<!-- SCREEN 3:[\s\S]*?<main class="card-stage">[\s\S]*?<\/main>/;

const modernScreen3Html = `<!-- ========================================== -->
      <!-- SCREEN 3: MODERN FLASHCARD VIEW             -->
      <!-- ========================================== -->
      <div class="app-screen active-screen" id="screen-flashcard">
        <!-- Single Unified Modern Top Navigation (No Duplication) -->
        <header class="flashcard-top-nav">
          <div class="top-nav-main">
            <button class="breadcrumb-back-btn" id="btn-breadcrumb-back" title="Back to Decks" aria-label="Back to Decks">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="15 18 9 12 15 6"/>
              </svg>
              <span id="breadcrumb-deck-label">Cards 800 – 1000</span>
            </button>
            <div class="top-category-pill" id="current-category">Kitchen & Cooking</div>
            <div class="top-nav-actions">
              <button
                class="shuffle-btn"
                id="btn-shuffle"
                title="Shuffle cards"
                aria-label="Shuffle cards"
              >
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M2 18h1.4c1.3 0 2.5-.6 3.3-1.7l6.6-8.6c.8-1.1 2-1.7 3.3-1.7H22" />
                  <path d="m18 2 4 4-4 4" />
                  <path d="M2 6h1.4c1.3 0 2.5.6 3.3 1.7l2 2.6" />
                  <path d="M14.6 13.7l2.1 2.6c.8 1.1 2 1.7 3.3 1.7H22" />
                  <path d="m18 20 4-4-4-4" />
                </svg>
              </button>
              <div class="counter-display">
                <span class="current-num" id="card-counter-current">800</span>
                <span class="counter-divider">/</span>
                <span class="total-num" id="card-counter-total">1000</span>
              </div>
            </div>
          </div>
          <!-- Single Slim Progress Line -->
          <div class="progress-track">
            <div class="progress-fill" id="progress-fill"></div>
          </div>
        </header>

        <!-- 3D Card Stage with Swipe & Strict Double-Tap mechanics -->
        <main class="card-stage">
          <div
            class="flashcard-wrapper"
            id="flashcard-wrapper"
            role="button"
            tabindex="0"
            aria-label="Flashcard - Double tap to flip"
          >
            <!-- Front Face: Modern, Clean, No English label, No duplicate category, No memory shortcuts button -->
            <div class="card-face card-face-front" id="card-face-front">
              <div class="card-header-bar">
                <span class="card-num-tag" id="front-card-num">#800</span>
                
                <div class="card-header-actions">
                  <button
                    class="icon-tool-btn"
                    id="front-edit-btn"
                    title="Edit card"
                    aria-label="Edit card"
                  >
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M12 20h9" />
                      <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z" />
                    </svg>
                  </button>
                  <button
                    class="speak-btn"
                    id="front-speak-btn"
                    title="Pronounce word"
                    aria-label="Pronounce word"
                  >
                    <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                      <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
                      <path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path>
                    </svg>
                  </button>
                </div>
              </div>

              <!-- Front Content: High-definition photo & bold target word -->
              <div class="front-content">
                <div class="visual-box" id="visual-box">
                  <div class="visual-skeleton" id="visual-skeleton"></div>
                  <img
                    id="front-visual-img"
                    class="visual-img"
                    alt="Target vocabulary visual"
                  />
                  <div class="visual-vignette"></div>
                  <!-- Offline Fallback -->
                  <div class="visual-vector-fallback" id="visual-fallback" style="display: none;">
                    <span class="vector-icon" id="front-emoji">🔥</span>
                  </div>
                </div>

                <!-- Target Word: Bold, Clean (NO 'English' label) -->
                <div class="target-word-container">
                  <h1 class="target-word" id="front-word">STOVE</h1>
                </div>
              </div>

              <!-- Modern cue: Double-tap to flip -->
              <div class="card-hint-footer" id="card-cue-front">
                <span class="hint-icon">✦</span>
                <span>Double-tap to flip</span>
              </div>
            </div>

            <!-- Back Face: Pure Native Tamil Display, Spanish, Hindi & Clean Mnemonics -->
            <div class="card-face card-face-back" id="card-face-back">
              <div class="card-header-bar">
                <span class="card-num-tag" id="back-card-num">#800</span>
                <span class="card-category-tag" id="back-card-word-preview">STOVE</span>
                
                <div class="card-header-actions">
                  <button
                    class="icon-tool-btn"
                    id="back-edit-btn"
                    title="Edit translations"
                    aria-label="Edit translations"
                  >
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M12 20h9" />
                      <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z" />
                    </svg>
                  </button>
                </div>
              </div>

              <!-- Back Content -->
              <div class="back-content">
                <!-- Pure Native Tamil Script Display -->
                <div class="tamil-hero-card" id="card-tamil-tile">
                  <div class="tamil-script-display" id="back-tamil-script">
                    அடுப்பு
                  </div>
                </div>

                <!-- Spanish & Hindi Translations (Tap to speak) -->
                <div class="translations-grid">
                  <!-- Spanish Tile -->
                  <div
                    class="trans-tile"
                    id="card-es-tile"
                    title="Tap to listen in Spanish"
                    role="button"
                    tabindex="0"
                  >
                    <div class="tile-top-bar">
                      <span class="lang-tag tag-es">ESPAÑOL</span>
                      <span class="tile-audio-icon">
                        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                          <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
                          <path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path>
                        </svg>
                      </span>
                    </div>
                    <div class="trans-tile-word" id="back-es-word">estufa</div>
                  </div>

                  <!-- Hindi Tile -->
                  <div
                    class="trans-tile"
                    id="card-hi-tile"
                    title="Tap to listen in Hindi"
                    role="button"
                    tabindex="0"
                  >
                    <div class="tile-top-bar">
                      <span class="lang-tag tag-hi">HINDI</span>
                      <span class="tile-audio-icon">
                        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                          <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
                          <path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path>
                        </svg>
                      </span>
                    </div>
                    <div class="trans-tile-word" id="back-hi-word">choolha</div>
                  </div>
                </div>

                <!-- Mnemonics Section (WITHOUT 'Memory Shortcuts' label) -->
                <div class="shortcut-section" id="card-shortcut-section">
                  <div class="shortcut-header">
                    <span class="mnemonic-kicker">MNEMONICS & RECALL</span>
                    <button type="button" class="shortcut-quick-edit-btn" id="btn-quick-edit-shortcut" title="Edit mnemonics" aria-label="Edit mnemonics">
                      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M12 20h9" />
                        <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z" />
                      </svg>
                      <span>Edit</span>
                    </button>
                  </div>
                  
                  <div class="shortcut-grid">
                    <!-- Spanish Box -->
                    <div class="shortcut-box shortcut-box-es">
                      <div class="shortcut-box-top">
                        <span class="shortcut-lang-label tag-es">Spanish Recall</span>
                        <span class="shortcut-target-word" id="shortcut-es-word">estufa</span>
                      </div>
                      <div class="shortcut-punchline" id="shortcut-es-text">
                        <strong>Es-tufa</strong> → <em>Tough-ah</em> flame on the stove!
                      </div>
                    </div>

                    <!-- Hindi Box -->
                    <div class="shortcut-box shortcut-box-hi">
                      <div class="shortcut-box-top">
                        <span class="shortcut-lang-label tag-hi">Hindi Recall</span>
                        <span class="shortcut-target-word" id="shortcut-hi-word">choolha</span>
                      </div>
                      <div class="shortcut-punchline" id="shortcut-hi-text">
                        <strong>Choolha</strong> → Village desi <em>Chulha</em> cooking hot rotis!
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Modern cue: Double-tap to flip back -->
              <div class="card-hint-footer" id="card-cue-back">
                <span class="hint-icon">↺</span>
                <span>Double-tap to flip back</span>
              </div>
            </div>
          </div>
        </main>`;

if (screen3StartPattern.test(html)) {
  html = html.replace(screen3StartPattern, modernScreen3Html);
  console.log('Successfully replaced Screen 3 HTML!');
} else {
  console.error('Failed to match screen3StartPattern!');
}

// 3. JAVASCRIPT: STRICT DOUBLE-TAP CONTROLLER
// Replace handleCardSurfaceTap and touch/click listeners
const jsDoubleTapPattern = /\/\/ STRICT DOUBLE-TAP & ACTION ISOLATION SYSTEM[\s\S]*?cardWrapper\.addEventListener\("dblclick"[\s\S]*?\}\);/;

const modernJsDoubleTap = `// STRICT DOUBLE-TAP & ACTION ISOLATION SYSTEM
      // Single tap / single click: strictly NEVER flips the card!
      // Double tap / double click: flips the card with physical audio.
      let lastTapTime = 0;
      let lastTapX = 0;
      let lastTapY = 0;
      let ignoreSyntheticClicksUntil = 0;

      // Pulse visual cue indicator on single tap
      function pulseDoubleTapCue() {
        const activeCue = isFlipped ? document.getElementById("card-cue-back") : document.getElementById("card-cue-front");
        if (activeCue) {
          activeCue.classList.remove("cue-highlight");
          void activeCue.offsetWidth;
          activeCue.classList.add("cue-highlight");
          setTimeout(() => activeCue.classList.remove("cue-highlight"), 550);
        }
      }

      // Action element guard: Spanish/Hindi tile taps, speech buttons, edit buttons, etc.
      function isActionElement(target) {
        if (!target) return false;
        return Boolean(
          target.closest(
            "#card-es-tile, #card-hi-tile, .trans-tile, .tile-top-bar, .tile-audio-icon, .trans-tile-word, " +
            "#card-tamil-tile, #front-speak-btn, #front-edit-btn, #back-edit-btn, .speak-btn, .icon-tool-btn, " +
            ".shortcut-quick-edit-btn, #btn-quick-edit-shortcut, button, input, textarea, a, .modal-sheet, .modal-backdrop"
          )
        );
      }

      // Unified Double-Tap Gesture Handler
      function processCardTapGesture(e, clientX, clientY) {
        if (isActionElement(e.target)) {
          lastTapTime = 0;
          return;
        }

        const now = Date.now();
        const timeDelta = now - lastTapTime;
        const distDelta = Math.hypot(clientX - lastTapX, clientY - lastTapY);

        // Double tap confirmed: between 60ms and 380ms, within 35px
        if (timeDelta > 60 && timeDelta < 380 && distDelta < 35) {
          lastTapTime = 0;
          lastTapX = 0;
          lastTapY = 0;
          flipCard();
        } else {
          // SINGLE TAP: Strictly DO NOT flip!
          lastTapTime = now;
          lastTapX = clientX;
          lastTapY = clientY;
          cardAudio.playTapClick();
          pulseDoubleTapCue();
        }
      }

      // Touch Events on Card Wrapper
      cardWrapper.addEventListener("touchstart", (e) => {
        if (isAnimating) return;
        cardAudio.unlock();
        const touch = e.touches[0];
        touchStartX = touch.clientX;
        touchStartY = touch.clientY;
        currentDeltaX = 0;
        isDragging = true;
      }, { passive: true });

      cardWrapper.addEventListener("touchmove", (e) => {
        if (!isDragging || isAnimating) return;
        const touch = e.touches[0];
        currentDeltaX = touch.clientX - touchStartX;
        const currentDeltaY = touch.clientY - touchStartY;

        if (Math.abs(currentDeltaX) > Math.abs(currentDeltaY) && Math.abs(currentDeltaX) > 10) {
          const rotateAngle = (currentDeltaX / 22).toFixed(2);
          const flipBase = isFlipped ? "rotateY(180deg)" : "rotateY(0deg)";
          cardWrapper.style.transform = \`\${flipBase} translateX(\${currentDeltaX * 0.45}px) rotateZ(\${rotateAngle}deg)\`;
        }
      }, { passive: true });

      cardWrapper.addEventListener("touchend", (e) => {
        if (!isDragging || isAnimating) return;
        isDragging = false;
        cardWrapper.style.transform = "";

        const touch = e.changedTouches[0];
        const deltaX = touch.clientX - touchStartX;
        const deltaY = touch.clientY - touchStartY;

        // Horizontal Swipe: Next / Previous
        if (Math.abs(deltaX) > SWIPE_THRESHOLD && Math.abs(deltaX) > Math.abs(deltaY)) {
          if (deltaX < 0) {
            nextCard();
          } else {
            prevCard();
          }
        } else if (Math.abs(deltaX) < 18 && Math.abs(deltaY) < 18) {
          if (isActionElement(e.target)) return;
          ignoreSyntheticClicksUntil = Date.now() + 650;
          processCardTapGesture(e, touch.clientX, touch.clientY);
        }
      });

      // Desktop Click Listener (Single click never flips; double click flips)
      cardWrapper.addEventListener("click", (e) => {
        if (Date.now() < ignoreSyntheticClicksUntil) return;
        if (isActionElement(e.target)) return;
        if (Math.abs(currentDeltaX) < 10) {
          processCardTapGesture(e, e.clientX, e.clientY);
        }
      });`;

if (jsDoubleTapPattern.test(html)) {
  html = html.replace(jsDoubleTapPattern, modernJsDoubleTap);
  console.log('Successfully replaced JavaScript double-tap controller!');
} else {
  console.error('Failed to match jsDoubleTapPattern!');
}

// 4. SCREEN NAVIGATION WIRING
// Ensure breadcrumb-back button switches between screens cleanly
const navWireJs = `
      // Screen Navigation Handlers
      function showScreen(screenId) {
        document.querySelectorAll(".app-screen").forEach((s) => s.classList.remove("active-screen"));
        const target = document.getElementById(screenId);
        if (target) target.classList.add("active-screen");
      }

      const btnBreadcrumbBack = document.getElementById("btn-breadcrumb-back");
      if (btnBreadcrumbBack) {
        btnBreadcrumbBack.addEventListener("click", () => {
          showScreen("screen-subsections");
        });
      }

      const btnBackToSections = document.getElementById("btn-back-to-sections");
      if (btnBackToSections) {
        btnBackToSections.addEventListener("click", () => {
          showScreen("screen-home");
        });
      }

      const subCard800_1000 = document.getElementById("sub-card-800-1000");
      if (subCard800_1000) {
        subCard800_1000.addEventListener("click", () => {
          showScreen("screen-flashcard");
        });
      }

      const cardSection3k = document.getElementById("card-section-3k");
      if (cardSection3k) {
        cardSection3k.addEventListener("click", () => {
          showScreen("screen-subsections");
        });
      }
`;

if (!html.includes('function showScreen(screenId)')) {
  html = html.replace('// wire Audio Studio UI Elements', `${navWireJs}\n\n      // wire Audio Studio UI Elements`);
}

// 5. UPDATE renderCurrentCard logic so it doesn't duplicate category or crash on removed elements
html = html.replace(
  'currentCategoryEl.textContent = card.category;\n        if (isShuffled) {',
  `if (currentCategoryEl) currentCategoryEl.textContent = card.category;\n        if (isShuffled) {`
);
html = html.replace(
  'frontCardCatEl.textContent = card.category;',
  'if (frontCardCatEl) frontCardCatEl.textContent = card.category;'
);
html = html.replace(
  'visualTypeBadgeEl.classList.add("is-anim");',
  'if (visualTypeBadgeEl) visualTypeBadgeEl.classList.add("is-anim");'
);
html = html.replace(
  'visualTypeBadgeEl.classList.remove("is-anim");',
  'if (visualTypeBadgeEl) visualTypeBadgeEl.classList.remove("is-anim");'
);

fs.writeFileSync('index.html', html, 'utf8');
console.log('Finished updating index.html. New length:', html.length);
