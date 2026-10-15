const fs = require('fs');
const path = require('path');

const indexPath = path.join(__dirname, '..', 'index.html');
let html = fs.readFileSync(indexPath, 'utf8');

console.log('Starting layout perfection. Original length:', html.length);

// 1. Clean up .mobile-top-bar in HTML: Remove the hamburger button and make Stellar on left, status on right in ONE row
const oldMobileTopBarRegex = /<header class="mobile-top-bar">[\s\S]*?<\/header>/;
const newMobileTopBar = `<header class="mobile-top-bar">
          <div class="mobile-top-bar-left">
            <span class="mobile-brand-title">Stellar</span>
          </div>
          <div class="mobile-top-bar-right">
            <div class="stat-badge-duo stat-badge-mastery" id="mobile-3k-status-badge">
              <span>⚡ <strong id="mobile-status-count">0</strong> / 3,000</span>
            </div>
          </div>
        </header>`;

if (oldMobileTopBarRegex.test(html)) {
  html = html.replace(oldMobileTopBarRegex, newMobileTopBar);
  console.log('Replaced mobile-top-bar: removed hamburger, separated Stellar on left and status on right');
} else {
  console.log('Warning: oldMobileTopBarRegex did not match directly');
}

// 2. Remove mobile-nav-drawer and mobile-nav-backdrop since user noted bottom nav already handles navigation
const drawerRegex = /<!-- ========================================================== -->\s*<!-- MOBILE NAVIGATION DRAWER[\s\S]*?<\/aside>/;
if (drawerRegex.test(html)) {
  html = html.replace(drawerRegex, '');
  console.log('Removed mobile-nav-drawer markup (bottom nav handles mobile navigation cleanly)');
}

// 3. Inject Master Viewport & Device Fit CSS
const deviceFitMasterCss = `
    /* ========================================================================= */
    /* MASTER PRODUCTION-GRADE VIEWPORT FIT & DEVICE PERFECTION                  */
    /* ========================================================================= */
    :root {
      --sidebar-width: 180px !important; /* Reduced whole left sidebar section */
      --brand-violet: #a855f7 !important;
    }

    /* Prevent accidental text selection on card that disrupts double-tap */
    .card-stage,
    .flashcard-wrapper,
    .card-face,
    .card-face * {
      user-select: none !important;
      -webkit-user-select: none !important;
    }

    /* ------------------------------------------------------------- */
    /* DESKTOP SIDEBAR: COMPACT, CLEAN & PROPORTIONATE (180px)       */
    /* ------------------------------------------------------------- */
    @media (min-width: 1024px) {
      .app-desktop-sidebar {
        display: flex !important;
        width: 180px !important;
        min-width: 180px !important;
        max-width: 180px !important;
        padding: 20px 12px 16px !important;
        position: fixed !important;
        left: 0 !important;
        top: 0 !important;
        bottom: 0 !important;
        z-index: 50 !important;
        background: #0b1120 !important;
        border-right: 1.5px solid rgba(255, 255, 255, 0.08) !important;
        box-sizing: border-box !important;
      }
      .sidebar-brand-lockup {
        padding-bottom: 16px !important;
        margin-bottom: 8px !important;
        padding-left: 6px !important;
        border-bottom: 1.5px solid rgba(255, 255, 255, 0.07) !important;
      }
      .sidebar-brand-title {
        font-size: 1.65rem !important;
        color: #a855f7 !important;
        text-shadow: 0 0 16px rgba(168, 85, 247, 0.45) !important;
      }
      .sidebar-nav-list {
        gap: 8px !important;
        margin-top: 10px !important;
      }
      .sidebar-nav-btn {
        padding: 10px 12px !important;
        gap: 10px !important;
        border-radius: 12px !important;
      }
      .sidebar-nav-label {
        font-size: 0.82rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.04em !important;
        color: #ffffff !important;
      }
      .sidebar-nav-icon {
        font-size: 1.2rem !important;
        width: 24px !important;
        height: 24px !important;
      }
      .app-main-viewport {
        margin-left: 180px !important;
        width: calc(100% - 180px) !important;
      }
      .desktop-top-header {
        display: flex !important;
      }
      .mobile-top-bar {
        display: none !important;
      }
      .mobile-bottom-nav {
        display: none !important;
      }
    }

    /* ------------------------------------------------------------- */
    /* TABLET & MOBILE (< 1024px): CLEAN SINGLE ROW TOP BAR          */
    /* ------------------------------------------------------------- */
    @media (max-width: 1023px) {
      .app-desktop-sidebar {
        display: none !important;
      }
      .desktop-top-header {
        display: none !important; /* Absolutely NEVER show on tablet or mobile */
      }
      .app-main-viewport {
        margin-left: 0 !important;
        width: 100% !important;
        padding-bottom: 74px !important;
      }
      .mobile-top-bar {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        justify-content: space-between !important;
        padding: 12px 18px !important;
        width: 100% !important;
        box-sizing: border-box !important;
        position: sticky !important;
        top: 0 !important;
        z-index: 50 !important;
        background: rgba(11, 17, 32, 0.95) !important;
        backdrop-filter: blur(14px) !important;
        -webkit-backdrop-filter: blur(14px) !important;
        border-bottom: 1.5px solid rgba(255, 255, 255, 0.08) !important;
      }
      .mobile-top-bar-left {
        display: flex !important;
        align-items: center !important;
      }
      .mobile-brand-title {
        font-family: 'Fredoka', 'Nunito', sans-serif !important;
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        color: #a855f7 !important;
        text-shadow: 0 0 16px rgba(168, 85, 247, 0.45) !important;
        line-height: 1 !important;
      }
      .mobile-top-bar-right {
        display: flex !important;
        align-items: center !important;
      }
      .mobile-bottom-nav {
        display: grid !important;
      }
    }

    /* ------------------------------------------------------------- */
    /* HOME SCREEN: ZERO OVERFLOW FIT IN VIEWPORT                    */
    /* ------------------------------------------------------------- */
    #screen-home {
      padding: clamp(10px, 2vh, 18px) clamp(12px, 3vw, 24px) !important;
      max-width: 680px !important;
      margin: 0 auto !important;
      gap: 12px !important;
      box-sizing: border-box !important;
    }
    .home-main-section-group {
      gap: 10px !important;
    }
    .card-3k-featured {
      padding: clamp(14px, 2vh, 20px) !important;
      border-radius: 20px !important;
    }
    .card-3k-desc {
      font-size: 0.86rem !important;
      line-height: 1.4 !important;
      margin-bottom: 10px !important;
      color: #94a3b8 !important;
      display: -webkit-box !important;
      -webkit-line-clamp: 2 !important;
      -webkit-box-orient: vertical !important;
      overflow: hidden !important;
    }
    .card-3k-progress-box {
      margin-bottom: 12px !important;
      padding: 10px 14px !important;
    }
    .btn-resume-deck {
      padding: 12px 20px !important;
      font-size: 0.95rem !important;
    }

    /* ------------------------------------------------------------- */
    /* FLASHCARD SCREEN: 100% PERFECT FIT TO SCREEN (ZERO SCROLL!)   */
    /* ------------------------------------------------------------- */
    #screen-flashcard {
      height: 100vh !important;
      max-height: 100vh !important;
      width: 100% !important;
      max-width: 520px !important;
      margin: 0 auto !important;
      padding: 8px 12px 10px !important;
      box-sizing: border-box !important;
      display: none;
      flex-direction: column !important;
      justify-content: space-between !important;
      overflow: hidden !important;
    }
    #screen-flashcard.active-screen {
      display: flex !important;
    }

    /* Top Nav in Flashcard: Compact */
    .flashcard-top-nav {
      flex-shrink: 0 !important;
      width: 100% !important;
      padding: 0 0 6px !important;
    }
    .flashcard-top-nav .top-nav-main {
      padding: 4px 6px !important;
    }

    /* 3D Card Stage: Fills remaining vertical height perfectly */
    #screen-flashcard .card-stage {
      flex: 1 1 0 !important;
      min-height: 0 !important;
      width: 100% !important;
      margin: 0 auto !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      position: relative !important;
      padding: 4px 0 !important;
      overflow: hidden !important;
    }

    #screen-flashcard .flashcard-wrapper {
      width: 100% !important;
      height: 100% !important;
      max-height: 100% !important;
      min-height: 0 !important;
      position: relative !important;
      transform-style: preserve-3d !important;
      -webkit-transform-style: preserve-3d !important;
    }

    #screen-flashcard .card-face {
      position: absolute !important;
      inset: 0 !important;
      width: 100% !important;
      height: 100% !important;
      border-radius: 20px !important;
      background: #111726 !important;
      border: 1px solid rgba(255, 255, 255, 0.1) !important;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5) !important;
      display: flex !important;
      flex-direction: column !important;
      justify-content: space-between !important;
      padding: 10px 14px !important;
      box-sizing: border-box !important;
      overflow: hidden !important;
    }

    /* Front Card Header */
    .card-face .card-header-bar {
      flex-shrink: 0 !important;
      display: flex !important;
      align-items: center !important;
      justify-content: space-between !important;
      padding-bottom: 6px !important;
    }

    /* Front Image Container: Scales to fit available height */
    #screen-flashcard .visual-box {
      flex: 1 1 0 !important;
      min-height: 0 !important;
      width: 100% !important;
      max-height: 100% !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      position: relative !important;
      overflow: hidden !important;
      border-radius: 14px !important;
      background: rgba(0, 0, 0, 0.25) !important;
    }

    #screen-flashcard .visual-box img {
      max-width: 100% !important;
      max-height: 100% !important;
      width: auto !important;
      height: auto !important;
      object-fit: contain !important;
    }

    /* Front Word Section */
    .card-face-front .target-word-container {
      flex-shrink: 0 !important;
      padding-top: 8px !important;
      text-align: center !important;
    }
    .card-face-front .target-word {
      font-size: clamp(1.4rem, 3.5vh, 2rem) !important;
      font-weight: 800 !important;
      margin: 0 !important;
      color: #ffffff !important;
    }

    /* Back Card Content */
    .card-face-back .back-translations-flow {
      flex: 1 1 0 !important;
      min-height: 0 !important;
      display: flex !important;
      flex-direction: column !important;
      gap: 6px !important;
      justify-content: center !important;
      overflow-y: auto !important;
    }
    .trans-tile {
      padding: 8px 12px !important;
      border-radius: 12px !important;
    }

    /* Nav Controls at bottom of flashcard */
    #screen-flashcard .nav-controls {
      flex-shrink: 0 !important;
      width: 100% !important;
      padding: 6px 4px 2px !important;
      display: flex !important;
      align-items: center !important;
      justify-content: space-between !important;
      gap: 12px !important;
    }
    #screen-flashcard .nav-btn-flip {
      padding: 10px 24px !important;
      font-size: 0.95rem !important;
    }
`;

html = html.replace('</style>', deviceFitMasterCss + '\n</style>');
console.log('Injected deviceFitMasterCss');

// 4. Update Double-Tap & Double-Click Handler in Script for 100% Instant Reliability
const bulletproofDoubleTapScript = `
      // =========================================================================
      // 100% BULLETPROOF ROCK-SOLID DOUBLE-TAP & DOUBLE-CLICK DETECTION
      // =========================================================================
      let cardLastTapTime = 0;
      let cardLastTapX = 0;
      let cardLastTapY = 0;

      function handleCardRapidDoubleTap(clientX, clientY, target) {
        if (isCardInteractiveBtn(target) || isCardAnimating) return;
        const now = Date.now();
        const timeDiff = now - cardLastTapTime;
        const dist = Math.hypot(clientX - cardLastTapX, clientY - cardLastTapY);

        if (timeDiff > 25 && timeDiff < 480 && dist < 75) {
          // ROCK-SOLID DOUBLE TAP!
          cardLastTapTime = 0;
          suppressSyntheticClickUntil = Date.now() + 500;
          flipCard();
          showDoubleTapCue(clientX, clientY);
          if (typeof playHapticTick === "function") playHapticTick(650, "triangle", 0.05);
        } else {
          cardLastTapTime = now;
          cardLastTapX = clientX;
          cardLastTapY = clientY;
        }
      }

      // Attach to cardWrapper click for instant desktop double-click detection without browser delay
      if (cardWrapper) {
        cardWrapper.addEventListener("click", (e) => {
          if (isCardInteractiveBtn(e.target) || isCardAnimating) return;
          handleCardRapidDoubleTap(e.clientX, e.clientY, e.target);
        });
      }
`;

const lastScriptIdx = html.lastIndexOf('</script>');
html = html.slice(0, lastScriptIdx) + bulletproofDoubleTapScript + '\n' + html.slice(lastScriptIdx);
console.log('Injected bulletproofDoubleTapScript');

fs.writeFileSync(indexPath, html, 'utf8');
console.log('Finished writing index.html! New length:', html.length);
