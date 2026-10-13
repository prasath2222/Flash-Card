const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');
console.log('Original index.html length:', html.length);

// 1. Inject CSS for perfect full-visibility Flashcard layout and distraction-free mode
const flashcardCss = `
      /* ==========================================================
         PRODUCTION-GRADE FLASHCARD VIEWPORT & RESPONSIVE GEOMETRY
         ========================================================== */
      #screen-flashcard {
        display: none;
        flex-direction: column !important;
        justify-content: space-between !important;
        width: 100% !important;
        max-width: 600px !important;
        margin: 0 auto !important;
        padding: 12px 16px 16px !important;
        gap: 10px !important;
        height: 100vh !important;
        max-height: 100vh !important;
        min-height: 100vh !important;
        box-sizing: border-box !important;
        overflow: hidden !important;
      }

      #screen-flashcard.active-screen {
        display: flex !important;
      }

      body.in-flashcard-mode {
        overflow: hidden !important;
      }

      body.in-flashcard-mode .app-desktop-sidebar {
        display: none !important;
      }

      body.in-flashcard-mode .desktop-top-header,
      body.in-flashcard-mode .mobile-top-bar,
      body.in-flashcard-mode .mobile-bottom-nav {
        display: none !important;
      }

      body.in-flashcard-mode .app-main-viewport {
        margin-left: 0 !important;
        width: 100% !important;
        padding-bottom: 0 !important;
        min-height: 100vh !important;
        height: 100vh !important;
        overflow: hidden !important;
      }

      .flashcard-top-nav {
        flex-shrink: 0 !important;
        width: 100% !important;
        padding: 4px 0 8px !important;
      }

      .flashcard-top-nav .top-nav-main {
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        gap: 12px !important;
      }

      .flashcard-top-nav .breadcrumb-back-btn {
        display: inline-flex !important;
        align-items: center !important;
        gap: 6px !important;
        padding: 8px 14px !important;
        border-radius: 9999px !important;
        background: rgba(255, 255, 255, 0.06) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        color: #f1f5f9 !important;
        font-size: 0.82rem !important;
        font-weight: 700 !important;
        cursor: pointer !important;
        transition: all 0.18s ease !important;
      }

      .flashcard-top-nav .breadcrumb-back-btn:hover {
        background: rgba(255, 255, 255, 0.12) !important;
        transform: translateX(-2px) !important;
      }

      #screen-flashcard .card-stage {
        flex: 1 1 auto !important;
        width: 100% !important;
        max-width: 500px !important;
        margin: 0 auto !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        perspective: 1200px !important;
        min-height: 0 !important;
        position: relative !important;
      }

      #screen-flashcard .flashcard-wrapper {
        width: 100% !important;
        height: 100% !important;
        max-height: 520px !important;
        min-height: 380px !important;
        position: relative !important;
        transform-style: preserve-3d !important;
        -webkit-transform-style: preserve-3d !important;
        cursor: pointer !important;
        transition: transform 0.48s cubic-bezier(0.34, 1.28, 0.64, 1) !important;
        user-select: none !important;
        -webkit-user-select: none !important;
      }

      #screen-flashcard .card-face {
        position: absolute !important;
        inset: 0 !important;
        width: 100% !important;
        height: 100% !important;
        border-radius: 24px !important;
        background: #111726 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: 0 16px 40px -8px rgba(0, 0, 0, 0.75), 0 0 0 1px rgba(255, 255, 255, 0.05) !important;
        backface-visibility: hidden !important;
        -webkit-backface-visibility: hidden !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
        padding: 18px 20px 14px !important;
        box-sizing: border-box !important;
        overflow-y: auto !important;
        scrollbar-width: thin;
      }

      #screen-flashcard .card-face-front {
        transform: rotateY(0deg) !important;
        -webkit-transform: rotateY(0deg) !important;
        z-index: 2 !important;
      }

      #screen-flashcard .card-face-back {
        transform: rotateY(180deg) !important;
        -webkit-transform: rotateY(180deg) !important;
        z-index: 1 !important;
        background: #0d1422 !important;
      }

      #screen-flashcard .flashcard-wrapper.flipped {
        transform: rotateY(180deg) !important;
        -webkit-transform: rotateY(180deg) !important;
      }

      #screen-flashcard .flashcard-wrapper.flipped .card-face-front {
        z-index: 1 !important;
        pointer-events: none !important;
      }

      #screen-flashcard .flashcard-wrapper.flipped .card-face-back {
        z-index: 2 !important;
        pointer-events: auto !important;
      }

      .card-face .card-header-bar {
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        width: 100% !important;
        padding-bottom: 8px !important;
      }

      .card-face .front-content {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        flex: 1 1 auto !important;
        min-height: 0 !important;
        gap: 12px !important;
        text-align: center !important;
        padding: 6px 0 !important;
      }

      .card-face .visual-box {
        position: relative !important;
        width: 100% !important;
        max-width: 320px !important;
        height: min(180px, 26vh) !important;
        border-radius: 18px !important;
        background: #080c14 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        overflow: hidden !important;
        box-shadow: 0 10px 24px -6px rgba(0, 0, 0, 0.6) !important;
      }

      .card-face .target-word-container {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
      }

      .card-face .target-word {
        font-size: clamp(2rem, 6.5vw, 2.75rem) !important;
        font-weight: 800 !important;
        letter-spacing: -0.01em !important;
        color: #ffffff !important;
        margin: 0 !important;
        line-height: 1.1 !important;
      }

      .card-hint-footer {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 6px !important;
        font-size: 0.74rem !important;
        font-weight: 600 !important;
        color: #64748b !important;
        padding-top: 8px !important;
      }

      /* Back Content styling */
      .card-face .back-content {
        display: flex !important;
        flex-direction: column !important;
        gap: 12px !important;
        flex: 1 1 auto !important;
        min-height: 0 !important;
        overflow-y: auto !important;
        padding: 4px 0 6px !important;
      }

      .tamil-hero-card {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 12px 16px !important;
        border-radius: 16px !important;
        background: rgba(16, 185, 129, 0.08) !important;
        border: 1px solid rgba(16, 185, 129, 0.28) !important;
        cursor: pointer !important;
        transition: all 0.18s ease !important;
      }

      .tamil-hero-card:hover {
        background: rgba(16, 185, 129, 0.15) !important;
        border-color: rgba(16, 185, 129, 0.45) !important;
      }

      .tamil-hero-header {
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        width: 100% !important;
        margin-bottom: 4px !important;
      }

      .lang-tag.tag-ta {
        color: #34d399 !important;
        font-size: 0.68rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.06em !important;
      }

      .tamil-script-display {
        font-size: clamp(2rem, 6.5vw, 2.6rem) !important;
        font-weight: 800 !important;
        color: #ffffff !important;
        line-height: 1.2 !important;
      }

      .translations-grid {
        display: grid !important;
        grid-template-columns: 1fr 1fr !important;
        gap: 10px !important;
      }

      .trans-tile {
        padding: 10px 14px !important;
        border-radius: 14px !important;
        background: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        cursor: pointer !important;
        transition: all 0.18s ease !important;
      }

      .trans-tile:hover {
        background: rgba(255, 255, 255, 0.08) !important;
        border-color: rgba(255, 255, 255, 0.18) !important;
      }

      .trans-tile-word {
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        margin-top: 4px !important;
      }

      .shortcut-section {
        background: rgba(15, 23, 42, 0.5) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 14px !important;
        padding: 10px 12px !important;
      }

      .shortcut-grid {
        display: grid !important;
        grid-template-columns: 1fr 1fr !important;
        gap: 8px !important;
      }

      .shortcut-box {
        padding: 8px 10px !important;
        border-radius: 10px !important;
        background: rgba(0, 0, 0, 0.25) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
      }

      .shortcut-punchline {
        font-size: 0.74rem !important;
        color: #cbd5e1 !important;
        line-height: 1.35 !important;
        margin-top: 4px !important;
      }

      /* Clean Tactile Bottom Controls */
      #screen-flashcard .nav-controls {
        flex-shrink: 0 !important;
        width: 100% !important;
        max-width: 500px !important;
        margin: 0 auto !important;
        padding: 6px 12px 10px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 16px !important;
      }

      .nav-btn-flip-cobalt {
        flex: 1 !important;
        max-width: 220px !important;
        height: 52px !important;
        border-radius: 9999px !important;
        background: #2563eb !important;
        color: #ffffff !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 8px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        cursor: pointer !important;
        box-shadow: 0 4px 16px rgba(37, 99, 235, 0.45) !important;
        transition: all 0.18s ease !important;
      }

      .nav-btn-flip-cobalt:hover, .nav-btn-flip-cobalt:active {
        background: #1d4ed8 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 22px rgba(37, 99, 235, 0.6) !important;
      }

      .nav-chevron-btn {
        width: 52px !important;
        height: 52px !important;
        border-radius: 9999px !important;
        background: #18181f !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #e2e8f0 !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
        transition: all 0.18s ease !important;
      }

      .nav-chevron-btn:hover, .nav-chevron-btn:active {
        background: #23232d !important;
        color: #ffffff !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
      }
`;

// Insert before </style>
html = html.replace('</style>', `${flashcardCss}\n</style>`);

// 2. Replace the HTML of #screen-flashcard with clean, production-grade, uncluttered HTML
const oldFlashcardStart = html.indexOf('<div class="app-screen" id="screen-flashcard">');
const oldFlashcardEnd = html.indexOf('<!-- Settings & Offline HTML Modal -->', oldFlashcardStart);

if (oldFlashcardStart !== -1 && oldFlashcardEnd !== -1) {
  const newFlashcardMarkup = `<div class="app-screen" id="screen-flashcard">
        <!-- Modern Clean Flashcard Header -->
        <header class="flashcard-top-nav">
          <div class="top-nav-main">
            <!-- Back to Subsections / Home -->
            <button class="breadcrumb-back-btn" id="btn-breadcrumb-back" title="Back to Subsections" aria-label="Back">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M19 12H5M12 19l-7-7 7-7"/>
              </svg>
              <span>Back</span>
            </button>

            <!-- Active Deck & Counter -->
            <div class="top-nav-center-group">
              <span class="top-category-pill" id="current-category">Kitchen & Cooking</span>
              <div class="counter-display">
                <span class="current-num" id="card-counter-current">800</span>
                <span class="counter-divider">/</span>
                <span class="total-num" id="card-counter-total">1000</span>
              </div>
            </div>

            <!-- Learned Toggle & Shuffle -->
            <div class="top-nav-actions">
              <button type="button" class="btn-top-learned-toggle" id="btn-top-learned-toggle" title="Mark as Learned" aria-label="Mark Card as Learned">
                <span class="learned-check-indicator">✓</span>
                <span class="learned-status-text">Learned</span>
              </button>

              <button class="shuffle-btn" id="btn-shuffle" title="Shuffle cards" aria-label="Shuffle cards">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M2 18h1.4c1.3 0 2.5-.6 3.3-1.7l6.6-8.6c.8-1.1 2-1.7 3.3-1.7H22" />
                  <path d="m18 2 4 4-4 4" />
                  <path d="M2 6h1.4c1.3 0 2.5.6 3.3 1.7l2 2.6" />
                  <path d="M14.6 13.7l2.1 2.6c.8 1.1 2 1.7 3.3 1.7H22" />
                  <path d="m18 20 4-4-4-4" />
                </svg>
              </button>
            </div>
          </div>
          <!-- Single Slim Progress Line -->
          <div class="progress-track">
            <div class="progress-fill" id="progress-fill"></div>
          </div>
        </header>

        <!-- 3D Card Stage with Full Viewport Visibility -->
        <main class="card-stage">
          <div
            class="flashcard-wrapper"
            id="flashcard-wrapper"
            role="button"
            tabindex="0"
            aria-label="Flashcard - Tap to flip"
          >
            <!-- Front Face: Modern, Clean, Uncluttered, Large Image -->
            <div class="card-face card-face-front" id="card-face-front">
              <div class="card-header-bar">
                <div class="card-num-group">
                  <span class="card-num-tag" id="front-card-num">#800</span>
                  <span class="card-unboxed-cat" id="front-card-cat-label">KITCHEN</span>
                </div>
                
                <div class="card-header-actions">
                  <button
                    class="speak-btn"
                    id="front-speak-btn"
                    title="Pronounce word in English"
                    aria-label="Pronounce word"
                  >
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
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
                  <div class="visual-vector-fallback" id="visual-fallback" style="display: none;">
                    <span class="vector-icon" id="front-emoji">🔥</span>
                  </div>
                </div>

                <div class="target-word-container">
                  <h1 class="target-word" id="front-word">STOVE</h1>
                </div>
              </div>

              <!-- Clear Tap Hint -->
              <div class="card-hint-footer" id="card-cue-front">
                <span class="hint-icon">↻</span>
                <span>Tap card to flip</span>
              </div>
            </div>

            <!-- Back Face: Pure Native Tamil Display, Spanish, Hindi & Clean Mnemonics -->
            <div class="card-face card-face-back" id="card-face-back">
              <div class="card-header-bar">
                <span class="card-num-tag" id="back-card-num">#800</span>
                <span class="card-category-tag" id="back-card-word-preview">STOVE</span>
              </div>

              <!-- Back Content -->
              <div class="back-content">
                <!-- Pure Native Tamil Script Display -->
                <div class="tamil-hero-card" id="card-tamil-tile" title="Tap to listen in Tamil" role="button" tabindex="0">
                  <div class="tamil-hero-header">
                    <span class="lang-tag tag-ta">TAMIL · தமிழ்</span>
                    <span class="tile-audio-icon">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                        <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
                        <path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path>
                      </svg>
                    </span>
                  </div>
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

                <!-- Mnemonics Section -->
                <div class="shortcut-section" id="card-shortcut-section">
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

              <!-- Cue: Tap to flip back -->
              <div class="card-hint-footer" id="card-cue-back">
                <span class="hint-icon">↺</span>
                <span>Tap card to flip back</span>
              </div>
            </div>
          </div>
        </main>

        <!-- Clean Tactile Controls: Prev, Flip Pill, Next -->
        <footer class="nav-controls">
          <!-- Prev Chevron -->
          <button class="nav-chevron-btn" id="btn-prev" aria-label="Previous Card" title="Previous Card">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="15 18 9 12 15 6"/>
            </svg>
          </button>

          <!-- Modern Electric Cobalt Blue Flip Pill Button -->
          <button class="nav-btn-flip-cobalt" id="btn-flip" aria-label="Flip Card">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8" />
              <path d="M3 3v5h5" />
              <path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16" />
              <path d="M16 16h5v5" />
            </svg>
            <span>Flip</span>
          </button>

          <!-- Next Chevron -->
          <button class="nav-chevron-btn" id="btn-next" aria-label="Next Card" title="Next Card">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="9 18 15 12 9 6"/>
            </svg>
          </button>
        </footer>
      </div>
    </div>\n\n    `;
  html = html.slice(0, oldFlashcardStart) + newFlashcardMarkup + html.slice(oldFlashcardEnd);
  console.log('Replaced flashcard HTML successfully');
} else {
  console.error('Could not find flashcard start or end indices!');
}

// 3. Update switchScreen to handle in-flashcard-mode
html = html.replace(
  'function switchScreen(screenId) {',
  `function switchScreen(screenId) {
        if (screenId === "screen-flashcard") {
          document.body.classList.add("in-flashcard-mode");
        } else {
          document.body.classList.remove("in-flashcard-mode");
        }`
);

// 4. Update gesture handling on cardWrapper so single tap FLIPS, horizontal swipe changes card, and vertical scroll is never blocked
const oldGestureCodeRegex = /\/\/ Unified Double-Tap Gesture Handler[\s\S]*?cardWrapper\.addEventListener\("click", \(e\) => \{[\s\S]*?\}\);/;

const newGestureCode = `// Production-Grade Tactile Tap & Swipe Mechanics (Single tap flips, swipe navigates, vertical scroll free)
      function isActionElement(target) {
        return Boolean(
          target.closest(
            "button, input, textarea, a, .speak-btn, #front-speak-btn, #card-es-tile, #card-hi-tile, #card-tamil-tile, #btn-top-learned-toggle, #btn-card-learned-action, .icon-tool-btn, .shortcut-quick-edit-btn"
          )
        );
      }

      let touchStartX = 0;
      let touchStartY = 0;
      let isHorizontalSwipe = false;

      // Touch handling on Card
      cardWrapper.addEventListener("touchstart", (e) => {
        if (isAnimating) return;
        cardAudio.unlock();
        const touch = e.touches[0];
        touchStartX = touch.clientX;
        touchStartY = touch.clientY;
        isHorizontalSwipe = false;
      }, { passive: true });

      cardWrapper.addEventListener("touchmove", (e) => {
        if (isAnimating) return;
        const touch = e.touches[0];
        const diffX = touch.clientX - touchStartX;
        const diffY = touch.clientY - touchStartY;

        // Only track horizontal gesture if clearly horizontal
        if (Math.abs(diffX) > Math.abs(diffY) * 1.4 && Math.abs(diffX) > 12) {
          isHorizontalSwipe = true;
          const rotateAngle = (diffX / 25).toFixed(2);
          const flipBase = isFlipped ? "rotateY(180deg)" : "rotateY(0deg)";
          cardWrapper.style.transform = \`\${flipBase} translateX(\${diffX * 0.38}px) rotateZ(\${rotateAngle}deg)\`;
        }
      }, { passive: true });

      cardWrapper.addEventListener("touchend", (e) => {
        if (isAnimating) return;
        cardWrapper.style.transform = "";

        const touch = e.changedTouches[0];
        const diffX = touch.clientX - touchStartX;
        const diffY = touch.clientY - touchStartY;

        if (isHorizontalSwipe && Math.abs(diffX) > 42) {
          // Swipe to next or prev
          if (diffX < 0) {
            nextCard();
          } else {
            prevCard();
          }
        } else if (Math.abs(diffX) < 14 && Math.abs(diffY) < 14) {
          // Clean single tap: FLIP CARD!
          if (!isActionElement(e.target)) {
            flipCard();
          }
        }
        isHorizontalSwipe = false;
      });

      // Desktop Click Listener: Single click on card flips it!
      cardWrapper.addEventListener("click", (e) => {
        if (isActionElement(e.target)) return;
        flipCard();
      });`;

if (oldGestureCodeRegex.test(html)) {
  html = html.replace(oldGestureCodeRegex, newGestureCode);
  console.log('Replaced gesture code successfully');
} else {
  console.error('Could not match old gesture code regex!');
}

// 5. Wire Tamil pronunciation on card-tamil-tile
if (!html.includes('cardTamilTile.addEventListener("click"')) {
  const tamilWire = `
      // Wire Tamil Voice Pronunciation on card-tamil-tile
      const cardTamilTile = document.getElementById("card-tamil-tile");
      if (cardTamilTile) {
        cardTamilTile.addEventListener("click", (e) => {
          e.stopPropagation();
          cardAudio.playTapClick();
          const card = cards[currentIndex];
          if (card && card.tamil) {
            playNativeSpeech(card.tamil, "ta", cardTamilTile, "speaking-ta");
          }
        });
      }
`;
  html = html.replace('// Spanish Voice Handler', tamilWire + '\n      // Spanish Voice Handler');
  console.log('Added Tamil speech listener');
}

// 6. Make sure btnBreadcrumbBack returns to screen-subsections
html = html.replace(
  'btnBreadcrumbBack.addEventListener("click", () => switchScreen("screen-home"));',
  'btnBreadcrumbBack.addEventListener("click", () => switchScreen("screen-subsections"));'
);

// 7. Support 'ta' in playNativeSpeech
html = html.replace(
  'const ttsLang = langCode.startsWith("es") ? "es" : langCode.startsWith("hi") ? "hi" : "en";',
  'const ttsLang = langCode.startsWith("es") ? "es" : langCode.startsWith("hi") ? "hi" : langCode.startsWith("ta") ? "ta" : "en";'
);

fs.writeFileSync('index.html', html, 'utf8');
console.log('Finished writing index.html, new length:', html.length);
