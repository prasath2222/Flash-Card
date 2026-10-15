const fs = require('fs');
const path = require('path');

const indexPath = path.join(__dirname, '..', 'index.html');
let html = fs.readFileSync(indexPath, 'utf8');

console.log('Original index.html length:', html.length);

// =========================================================================
// 1. CLEAN UP THE OUT-OF-PLACE "+ Add Section" AT BOTTOM OF SUBSECTIONS
// =========================================================================
const subsectionAddMarker = `          <!-- Centered Duolingo-style 3D Add Section Button (Both Main & Subsection have it centered!) -->
          <div class="duo-add-section-wrapper" style="margin-top: 36px;">
            <button type="button" class="duo-btn-add-section" id="btn-subsections-add-section" title="Add a custom section">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">
                <line x1="12" y1="5" x2="12" y2="19"/>
                <line x1="5" y1="12" x2="19" y2="12"/>
              </svg>
              <span>Add Section</span>
            </button>
          </div>`;

if (html.includes(subsectionAddMarker)) {
  html = html.replace(subsectionAddMarker, '');
  console.log('Removed redundant Add Section button from 3k Subsections view');
} else {
  // Try alternative regex removal
  html = html.replace(/<div class="duo-add-section-wrapper"[^>]*>\s*<button[^>]*id="btn-subsections-add-section"[\s\S]*?<\/div>/g, '');
  console.log('Removed redundant Add Section via regex');
}

// Remove any JS listener for btn-subsections-add-section
html = html.replace(/const btnAddSub = document\.getElementById\("btn-subsections-add-section"\);[\s\S]*?btnAddSub\.addEventListener\("click"[\s\S]*?\};\s*\}/g, '// btn-subsections-add-section removed');

// =========================================================================
// 2. INJECT BULLETPROOF FLASHCARD VIEWPORT-CONTAINMENT CSS
// =========================================================================
const productionViewportCSS = `
    /* ========================================================================= */
    /* MASTERCLASS ZERO-SCROLL FLASHCARD VIEWPORT SYSTEM ACROSS ALL DEVICES     */
    /* ========================================================================= */
    body.in-flashcard-mode,
    html:has(body.in-flashcard-mode) {
      overflow: hidden !important;
      height: 100% !important;
      height: 100dvh !important;
      max-height: 100dvh !important;
      width: 100% !important;
      position: fixed !important;
      inset: 0 !important;
      touch-action: none !important;
    }

    body.in-flashcard-mode #app-container {
      height: 100% !important;
      height: 100dvh !important;
      max-height: 100dvh !important;
      min-height: 0 !important;
      overflow: hidden !important;
      padding: 0 !important;
      margin: 0 !important;
      width: 100% !important;
      position: fixed !important;
      inset: 0 !important;
    }

    body.in-flashcard-mode .app-main-viewport {
      margin: 0 !important;
      padding: 0 !important;
      padding-bottom: 0 !important;
      width: 100% !important;
      height: 100% !important;
      height: 100dvh !important;
      min-height: 0 !important;
      max-height: 100dvh !important;
      overflow: hidden !important;
      position: fixed !important;
      inset: 0 !important;
    }

    body.in-flashcard-mode .app-desktop-sidebar,
    body.in-flashcard-mode .desktop-top-header,
    body.in-flashcard-mode .mobile-top-bar,
    body.in-flashcard-mode .mobile-bottom-nav,
    body.in-flashcard-mode .mobile-nav-drawer,
    body.in-flashcard-mode .mobile-nav-backdrop {
      display: none !important;
    }

    #screen-flashcard {
      display: none;
      flex-direction: column !important;
      justify-content: space-between !important;
      width: 100% !important;
      max-width: 500px !important;
      margin: 0 auto !important;
      height: 100% !important;
      height: 100dvh !important;
      max-height: 100dvh !important;
      min-height: 0 !important;
      padding: 6px 12px 10px !important;
      box-sizing: border-box !important;
      overflow: hidden !important;
      position: relative !important;
    }

    #screen-flashcard.active-screen {
      display: flex !important;
    }

    /* Flashcard Top Navigation Bar */
    #screen-flashcard .flashcard-top-nav {
      flex: 0 0 auto !important;
      width: 100% !important;
      padding: 0 !important;
      margin-bottom: 4px !important;
    }

    #screen-flashcard .top-nav-main {
      display: flex !important;
      align-items: center !important;
      justify-content: space-between !important;
      padding: 2px 0 !important;
      width: 100% !important;
      box-sizing: border-box !important;
      gap: 8px !important;
    }

    /* Back Button */
    #screen-flashcard .breadcrumb-back-btn {
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      width: 38px !important;
      height: 38px !important;
      min-width: 38px !important;
      border-radius: 12px !important;
      padding: 0 !important;
      flex-shrink: 0 !important;
      background: rgba(255, 255, 255, 0.08) !important;
      border: 1px solid rgba(255, 255, 255, 0.16) !important;
      color: #f1f5f9 !important;
    }

    @media (max-width: 640px) {
      #screen-flashcard .breadcrumb-back-btn span {
        display: none !important;
      }
      #current-category {
        display: none !important;
      }
      #btn-reset-deck {
        display: none !important;
      }
    }

    /* Center Group: Streak badge + Counter display */
    #screen-flashcard .top-nav-center-group {
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      gap: 8px !important;
      flex: 1 1 auto !important;
    }

    #screen-flashcard .counter-display {
      font-weight: 800 !important;
      font-size: 0.92rem !important;
      color: #f1f5f9 !important;
      display: inline-flex !important;
      align-items: center !important;
      gap: 4px !important;
      white-space: nowrap !important;
      flex-shrink: 0 !important;
    }

    #screen-flashcard .top-nav-actions {
      display: flex !important;
      align-items: center !important;
      gap: 6px !important;
      flex-shrink: 0 !important;
    }

    /* Flashcard Stage: Flexes to fill EXACT vertical space */
    #screen-flashcard .card-stage {
      flex: 1 1 0% !important;
      width: 100% !important;
      min-height: 0 !important;
      max-height: none !important;
      margin: 0 !important;
      padding: 0 !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      perspective: 1200px !important;
      position: relative !important;
      overflow: hidden !important;
      box-sizing: border-box !important;
    }

    #screen-flashcard .flashcard-wrapper {
      width: 100% !important;
      height: 100% !important;
      max-height: 100% !important;
      min-height: 0 !important;
      position: relative !important;
      display: flex !important;
      border-radius: 20px !important;
      transform-style: preserve-3d !important;
      -webkit-transform-style: preserve-3d !important;
      cursor: pointer !important;
      user-select: none !important;
      -webkit-user-select: none !important;
      touch-action: pan-y !important;
    }

    #screen-flashcard .card-face {
      position: absolute !important;
      inset: 0 !important;
      width: 100% !important;
      height: 100% !important;
      display: flex !important;
      flex-direction: column !important;
      justify-content: space-between !important;
      padding: 10px 14px !important;
      border-radius: 20px !important;
      box-sizing: border-box !important;
      overflow: hidden !important;
      background: #111726 !important;
      border: 1px solid rgba(255, 255, 255, 0.1) !important;
      box-shadow: 0 16px 40px -8px rgba(0, 0, 0, 0.75), 0 0 0 1px rgba(255, 255, 255, 0.05) !important;
      backface-visibility: hidden !important;
      -webkit-backface-visibility: hidden !important;
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

    /* Card Header Bar */
    #screen-flashcard .card-header-bar {
      display: flex !important;
      align-items: center !important;
      justify-content: space-between !important;
      width: 100% !important;
      padding: 2px 2px 4px !important;
      flex: 0 0 auto !important;
    }

    /* Front Face Layout: Guaranteed inside viewport */
    #screen-flashcard .front-content {
      flex: 1 1 0% !important;
      display: flex !important;
      flex-direction: column !important;
      min-height: 0 !important;
      overflow: hidden !important;
      justify-content: space-between !important;
      gap: 6px !important;
      width: 100% !important;
      align-items: center !important;
    }

    #screen-flashcard .visual-box {
      flex: 1 1 0% !important;
      width: 100% !important;
      min-height: 70px !important;
      max-height: none !important;
      border-radius: 14px !important;
      overflow: hidden !important;
      position: relative !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      background: #080c14 !important;
      border: 1px solid rgba(255, 255, 255, 0.08) !important;
    }

    #screen-flashcard .visual-img {
      width: 100% !important;
      height: 100% !important;
      object-fit: contain !important;
      border-radius: 12px !important;
    }

    #screen-flashcard .target-word-container {
      flex: 0 0 auto !important;
      padding: 4px 0 2px !important;
      text-align: center !important;
    }

    #screen-flashcard .target-word {
      font-size: clamp(1.4rem, 5vw, 1.95rem) !important;
      line-height: 1.15 !important;
      margin: 0 !important;
      font-weight: 800 !important;
      letter-spacing: -0.01em !important;
      color: #ffffff !important;
    }

    /* Back Face Content: Internal scroll if needed, page never scrolls */
    #screen-flashcard .card-face-back .back-content {
      flex: 1 1 0% !important;
      min-height: 0 !important;
      display: flex !important;
      flex-direction: column !important;
      gap: 8px !important;
      overflow-y: auto !important;
      -webkit-overflow-scrolling: touch !important;
      padding: 2px 2px 4px !important;
    }

    #screen-flashcard .tamil-hero-card {
      padding: 10px 14px !important;
      border-radius: 14px !important;
      flex-shrink: 0 !important;
    }

    #screen-flashcard .tamil-script-display {
      font-size: clamp(1.5rem, 5vw, 2rem) !important;
      line-height: 1.2 !important;
    }

    #screen-flashcard .translations-grid {
      display: grid !important;
      grid-template-columns: 1fr 1fr !important;
      gap: 8px !important;
      flex-shrink: 0 !important;
    }

    #screen-flashcard .trans-tile {
      padding: 8px 12px !important;
      border-radius: 12px !important;
    }

    #screen-flashcard .shortcut-section {
      flex-shrink: 0 !important;
      padding: 8px 10px !important;
      border-radius: 12px !important;
    }

    /* Bottom Navigation Controls: GUARANTEED VISIBLE, NEVER PUSHED OFF-SCREEN */
    #screen-flashcard .nav-controls {
      flex: 0 0 52px !important;
      height: 52px !important;
      min-height: 52px !important;
      max-height: 52px !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      gap: 14px !important;
      padding: 0 !important;
      margin-top: 6px !important;
      margin-bottom: 0 !important;
      width: 100% !important;
      z-index: 20 !important;
    }

    .nav-btn-flip-cobalt {
      flex: 1 !important;
      max-width: 200px !important;
      height: 46px !important;
      border-radius: 9999px !important;
      background: #2563eb !important;
      color: #ffffff !important;
      font-size: 0.95rem !important;
      font-weight: 750 !important;
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
    }

    .nav-chevron-btn {
      width: 46px !important;
      height: 46px !important;
      min-width: 46px !important;
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
    }

    /* Tablet Responsive Fix: Never show half-cut mini-card visual column */
    @media (max-width: 1099px) {
      .card-3k-visual-col {
        display: none !important;
      }
    }
`;

// Insert productionViewportCSS before </head>
html = html.replace('</head>', `<style>${productionViewportCSS}</style>\n</head>`);
console.log('Injected masterclass zero-scroll flashcard viewport CSS');

// =========================================================================
// 3. UNIFY & STRENGTHEN STRICT DOUBLE-TAP ENGINE
// =========================================================================

// First remove the second duplicate double-tap listener at the end of index.html
const dupMarker = '// STRICT DOUBLE-TAP TO FLIP ONLY ENGINE (Single-tap NEVER flips!)';
if (html.includes(dupMarker)) {
  const dupIdx = html.indexOf(dupMarker);
  const endScriptIdx = html.lastIndexOf('</script>');
  html = html.slice(0, dupIdx) + html.slice(endScriptIdx);
  console.log('Removed duplicate double-tap block from end of file');
}

// Now replace the touch event handler in lines ~518000
const oldTouchBlockMarker = `} else if (dist < 45 && touchDuration < 320) {
          // Stationary clean tap: 100% RELIABLE DOUBLE TAP FLIP
          if (!isCardInteractiveBtn(e.target)) {
            const now = Date.now();
            const tapDist = Math.hypot(touch.clientX - lastTapCoords.x, touch.clientY - lastTapCoords.y);
            if (now - lastTapTimestamp < 420 && tapDist < 80) {
              // Confirmed Double Tap!
              lastTapTimestamp = 0;
              suppressSyntheticClickUntil = Date.now() + 650;
              flipCard();
              showDoubleTapCue(touch.clientX, touch.clientY);
              if (typeof playHapticTick === "function") playHapticTick(650, "triangle", 0.05);
            } else {
              lastTapTimestamp = now;
              lastTapCoords = { x: touch.clientX, y: touch.clientY };
            }
          }
        }`;

const newStrictDoubleTapTouch = `} else if (dist < 35 && touchDuration < 350) {
          // STRICT PRODUCTION-GRADE DOUBLE-TAP ENGINE
          if (!isCardInteractiveBtn(e.target)) {
            const now = Date.now();
            // Debounce lock: if card is currently flipping or just flipped, ignore rapid extra taps
            if (now >= flipAnimationLockoutUntil) {
              const timeSinceLast = now - singleTapTimestamp;
              const tapDist = Math.hypot(touch.clientX - singleTapCoords.x, touch.clientY - singleTapCoords.y);

              if (singleTapTimestamp > 0 && timeSinceLast > 60 && timeSinceLast < 380 && tapDist < 60) {
                // CONFIRMED DOUBLE TAP!
                singleTapTimestamp = 0; // Clear so 3rd tap will never flip
                if (singleTapTimer) { clearTimeout(singleTapTimer); singleTapTimer = null; }
                flipAnimationLockoutUntil = now + 500; // Lock out rapid extra taps during flip animation
                suppressSyntheticClickUntil = now + 650;
                
                flipCard();
                showDoubleTapCue(touch.clientX, touch.clientY);
                if (typeof playHapticTick === "function") playHapticTick(680, "triangle", 0.05);
              } else {
                // FIRST TAP OF POTENTIAL DOUBLE-TAP
                singleTapTimestamp = now;
                singleTapCoords = { x: touch.clientX, y: touch.clientY };
                if (singleTapTimer) clearTimeout(singleTapTimer);
                singleTapTimer = setTimeout(() => {
                  singleTapTimestamp = 0; // First tap expired without a second tap
                }, 380);
              }
            }
          }
        }`;

if (html.includes(oldTouchBlockMarker)) {
  html = html.replace(oldTouchBlockMarker, newStrictDoubleTapTouch);
  console.log('Replaced touch block with strict double-tap engine');
} else {
  console.warn('Could not find oldTouchBlockMarker, searching alternatives...');
  const altOld = html.indexOf('// Stationary clean tap: 100% RELIABLE DOUBLE TAP FLIP');
  if (altOld !== -1) {
    const endBlock = html.indexOf('} else {', altOld);
    html = html.slice(0, altOld) + newStrictDoubleTapTouch.replace('} else if (dist < 35 && touchDuration < 350) {\n          ', '') + '\n        ' + html.slice(endBlock);
    console.log('Replaced via index slice');
  }
}

// Add state variables for double tap if not declared
const varMarker = `let lastTapTimestamp = 0;
      let lastTapCoords = { x: 0, y: 0 };`;
const newVars = `let singleTapTimestamp = 0;
      let singleTapCoords = { x: 0, y: 0 };
      let singleTapTimer = null;
      let flipAnimationLockoutUntil = 0;`;

if (html.includes(varMarker)) {
  html = html.replace(varMarker, newVars);
  console.log('Replaced tap tracking variables');
} else if (!html.includes('flipAnimationLockoutUntil')) {
  // Inject right before cardWrapper.addEventListener("touchstart"
  html = html.replace('cardWrapper.addEventListener("touchstart"', `${newVars}\n      cardWrapper.addEventListener("touchstart"`);
  console.log('Injected new tap variables before touchstart');
}

// Make sure closeMobileNavDrawer and openMobileNavDrawer cleanly reset drawer styles
const drawerOpenCloseMarker = `      function openMobileNavDrawer() {
        if (mobileNavDrawer) mobileNavDrawer.classList.add("open");
        if (mobileNavBackdrop) mobileNavBackdrop.classList.add("open");
        if (typeof playHapticTick === "function") playHapticTick(480, "sine", 0.04);
      }
      function closeMobileNavDrawer() {
        if (mobileNavDrawer) mobileNavDrawer.classList.remove("open");
        if (mobileNavBackdrop) mobileNavBackdrop.classList.remove("open");
      }`;

const cleanDrawerOpenClose = `      function openMobileNavDrawer() {
        if (mobileNavDrawer) {
          mobileNavDrawer.style.transform = "";
          mobileNavDrawer.style.transition = "";
          mobileNavDrawer.classList.add("open");
        }
        if (mobileNavBackdrop) {
          mobileNavBackdrop.style.opacity = "";
          mobileNavBackdrop.style.transition = "";
          mobileNavBackdrop.classList.add("open");
        }
        if (typeof playHapticTick === "function") playHapticTick(480, "sine", 0.04);
      }
      function closeMobileNavDrawer() {
        if (mobileNavDrawer) {
          mobileNavDrawer.classList.remove("open");
          mobileNavDrawer.style.transform = "";
          mobileNavDrawer.style.transition = "";
        }
        if (mobileNavBackdrop) {
          mobileNavBackdrop.classList.remove("open");
          mobileNavBackdrop.style.opacity = "";
          mobileNavBackdrop.style.transition = "";
        }
      }`;

if (html.includes(drawerOpenCloseMarker)) {
  html = html.replace(drawerOpenCloseMarker, cleanDrawerOpenClose);
  console.log('Updated openMobileNavDrawer and closeMobileNavDrawer for clean gesture resets');
}

fs.writeFileSync(indexPath, html, 'utf8');
console.log('Finished updating index.html. New length:', html.length);
