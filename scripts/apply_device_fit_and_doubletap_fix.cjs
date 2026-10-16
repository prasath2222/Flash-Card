const fs = require('fs');
const path = require('path');

const indexPath = path.join(__dirname, '..', 'index.html');
let html = fs.readFileSync(indexPath, 'utf8');

console.log('Original index.html length:', html.length);

// 1. Remove conflicting rules earlier in <style>
// Search for old #screen-flashcard .flashcard-wrapper rules that have width: 100% !important
html = html.replace(
  /#screen-flashcard \.flashcard-wrapper\s*\{[\s\S]*?width:\s*100%\s*!important;[\s\S]*?\}/g,
  `#screen-flashcard .flashcard-wrapper {
        position: relative !important;
        transform-style: preserve-3d !important;
        -webkit-transform-style: preserve-3d !important;
        cursor: pointer !important;
        border-radius: 22px !important;
        user-select: none !important;
        -webkit-user-select: none !important;
        touch-action: none !important;
        box-sizing: border-box !important;
        margin: auto !important;
      }`
);

// Search for any other .flashcard-wrapper rules with max-height: min(480px, 62vh)
html = html.replace(
  /\.flashcard-wrapper\s*\{[\s\S]*?max-height:\s*min\(480px,\s*62vh\)[\s\S]*?\}/g,
  `.flashcard-wrapper {
        position: relative !important;
        cursor: pointer !important;
        user-select: none !important;
        -webkit-user-select: none !important;
        touch-action: none !important;
        box-sizing: border-box !important;
        margin: auto !important;
      }`
);

// 2. Locate the tail of <style> starting from cut1
let cut1 = html.indexOf("/* 100% VIEWPORT FIT ARCHITECTURE FOR FLASHCARD MODE (ZERO SCROLLING)");
if (cut1 === -1) {
  cut1 = html.indexOf("/* ========================================================================= */\n    /* PRODUCTION-GRADE ZERO-SCROLL ALL-DEVICE FLASHCARD VIEWPORT SYSTEM");
}
if (cut1 === -1) {
  cut1 = html.indexOf("/* PRODUCTION-GRADE ZERO-SCROLL ALL-DEVICE FLASHCARD VIEWPORT SYSTEM");
}

const styleEnd = html.indexOf("</style>");

if (cut1 === -1 || styleEnd === -1 || cut1 >= styleEnd) {
  console.error("Could not find style cut position! cut1:", cut1, "styleEnd:", styleEnd);
  process.exit(1);
}

console.log(`Replacing tail of <style> from ${cut1} to ${styleEnd} (${styleEnd - cut1} chars)...`);

const pristineFlashcardCss = `    /* ========================================================================= */
    /* MASTER ZERO-SCROLL ALL-DEVICE FLASHCARD SYSTEM                           */
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

    /* Fixed full-screen flashcard container: strictly fits on 1 screen */
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
      background: #080d1a !important;
      z-index: 99999 !important;
      display: flex !important;
      flex-direction: column !important;
      justify-content: space-between !important;
      align-items: center !important;
      padding: env(safe-area-inset-top, 6px) 12px env(safe-area-inset-bottom, 8px) !important;
      box-sizing: border-box !important;
      overflow: hidden !important;
    }

    /* Pinned 46px Top Navigation Bar */
    #screen-flashcard .flashcard-top-nav {
      flex: 0 0 46px !important;
      width: 100% !important;
      max-width: 480px !important;
      height: 46px !important;
      min-height: 46px !important;
      max-height: 46px !important;
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

    /* Pinned 54px Bottom Navigation Controls (Prev, Flip Pill, Next) */
    #screen-flashcard .nav-controls {
      flex: 0 0 54px !important;
      width: 100% !important;
      max-width: 480px !important;
      height: 54px !important;
      min-height: 54px !important;
      max-height: 54px !important;
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
      padding: 0 36px !important;
      font-size: 0.98rem !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      gap: 8px !important;
      font-family: inherit !important;
      font-weight: 800 !important;
      border-radius: 14px !important;
      cursor: pointer !important;
      background: #2563eb !important;
      border: 1px solid rgba(255, 255, 255, 0.25) !important;
      color: #ffffff !important;
      box-shadow: 0 4px 14px rgba(37, 99, 235, 0.45) !important;
      transition: all 0.15s ease !important;
    }
    #screen-flashcard .nav-btn-flip-cobalt:hover,
    #screen-flashcard .nav-btn-flip-cobalt:active {
      background: #1d4ed8 !important;
      transform: translateY(-1px) scale(0.98) !important;
    }
    #screen-flashcard .nav-chevron-btn {
      width: 46px !important;
      height: 46px !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      border-radius: 14px !important;
      cursor: pointer !important;
      background: #18181f !important;
      border: 1px solid rgba(255, 255, 255, 0.12) !important;
      color: #e2e8f0 !important;
      transition: all 0.15s ease !important;
    }
    #screen-flashcard .nav-chevron-btn:hover,
    #screen-flashcard .nav-chevron-btn:active {
      background: #23232d !important;
      border-color: rgba(255, 255, 255, 0.25) !important;
      transform: scale(0.96) !important;
    }

    /* Middle Card Stage: Takes EXACT remaining viewport height */
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
      perspective: 1200px !important;
    }

    /* Dynamic Flashcard: Auto-sized by JS Engine to strictly fit any screen */
    #screen-flashcard .flashcard-wrapper {
      max-width: 100% !important;
      max-height: 100% !important;
      position: relative !important;
      margin: auto !important;
      display: block !important;
      cursor: pointer !important;
      user-select: none !important;
      -webkit-user-select: none !important;
      border-radius: 22px !important;
      box-sizing: border-box !important;
      transform-style: preserve-3d !important;
      -webkit-transform-style: preserve-3d !important;
      touch-action: none !important;
      transition: transform 0.38s cubic-bezier(0.34, 1.25, 0.64, 1);
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

    #screen-flashcard .card-face {
      position: absolute !important;
      inset: 0 !important;
      width: 100% !important;
      height: 100% !important;
      display: flex !important;
      flex-direction: column !important;
      justify-content: space-between !important;
      padding: 10px 14px 10px !important;
      box-sizing: border-box !important;
      border-radius: 22px !important;
      background: #101726 !important;
      border: 1.5px solid rgba(255, 255, 255, 0.12) !important;
      box-shadow: 0 16px 38px -8px rgba(0, 0, 0, 0.75) !important;
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
      margin-bottom: 2px !important;
      width: 100% !important;
    }

    /* Front Face Layout: High-definition visual + bold target word (Image 1 replica) */
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
      border-radius: 16px !important;
      overflow: hidden !important;
      background: #060b13 !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      position: relative !important;
    }

    #screen-flashcard .visual-img {
      width: 100% !important;
      height: 100% !important;
      object-fit: contain !important;
      background: #060b13 !important;
      border-radius: 14px !important;
    }

    #screen-flashcard .target-word-container {
      flex: 0 0 auto !important;
      padding: 4px 0 2px !important;
      text-align: center !important;
      width: 100% !important;
    }

    #screen-flashcard .target-word,
    #screen-flashcard #front-word,
    #screen-flashcard .target-word-title {
      font-size: clamp(1.6rem, 5.2vw, 2.3rem) !important;
      font-weight: 850 !important;
      letter-spacing: -0.015em !important;
      margin: 0 !important;
      color: #ffffff !important;
      line-height: 1.15 !important;
      text-transform: uppercase !important;
    }

    /* Back Face Layout */
    #screen-flashcard .card-face-back {
      transform: rotateY(180deg) !important;
      -webkit-transform: rotateY(180deg) !important;
      background: #0d1422 !important;
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

html = html.slice(0, cut1) + pristineFlashcardCss + '\n  ' + html.slice(styleEnd);

// 3. Clean up gesture handling in JavaScript to guarantee STRICT DOUBLE-TAP TO FLIP
// Remove any duplicate tail scripts
const autoFitScriptMarker = "// DYNAMIC ALL-DEVICE FLASHCARD AUTO-FIT ENGINE";
const scriptCut = html.indexOf(autoFitScriptMarker);
const lastScriptEnd = html.lastIndexOf("</script>");

if (scriptCut !== -1 && lastScriptEnd !== -1) {
  html = html.slice(0, scriptCut) + html.slice(lastScriptEnd);
}

// Ensure the main flipCard function handles animation locks and styles cleanly
html = html.replace(
  /function flipCard\(\) \{[\s\S]*?cardWrapper\.classList\.add\("flipped"\);[\s\S]*?cardWrapper\.classList\.remove\("flipped"\);[\s\S]*?\}/,
  `function flipCard() {
        if (isAnimating) return;
        isAnimating = true;
        setTimeout(() => { isAnimating = false; }, 380);
        isFlipped = !isFlipped;
        if (typeof cardAudio !== "undefined" && cardAudio.playCardFlip) {
          cardAudio.playCardFlip(!isFlipped);
        }
        if (cardWrapper) {
          cardWrapper.classList.toggle("flipped", isFlipped);
          cardWrapper.style.setProperty("transform", isFlipped ? "rotateY(180deg)" : "rotateY(0deg)", "important");
        }
      }`
);

// Unified Robust Double-Tap Gesture Engine appended before </script>
const masterGestureAndAutoFitScript = `
      // =========================================================================
      // DYNAMIC ALL-DEVICE FLASHCARD AUTO-FIT & STRICT DOUBLE-TAP FLIP SYSTEM
      // =========================================================================
      (function() {
        // --- 1. Dynamic Auto-Fit Engine: Fits 100% on ANY Device Viewport ---
        function autoFitFlashcard() {
          const screen = document.getElementById("screen-flashcard");
          if (!screen || !screen.classList.contains("active-screen")) return;
          const stage = screen.querySelector(".card-stage");
          const wrapper = screen.querySelector(".flashcard-wrapper");
          if (!stage || !wrapper) return;

          const availW = stage.clientWidth;
          const availH = stage.clientHeight;
          if (availW <= 0 || availH <= 0) return;

          // Ideal card ratio: 0.72 (standard 3.6 : 5 portrait flashcard)
          const ratio = 0.72;
          const maxW = 420;
          const maxH = 580;
          const minW = 250;
          const minH = 340;

          // Deduct 10px breathing room
          const targetAvailH = Math.min(availH - 10, maxH);
          const targetAvailW = Math.min(availW - 10, maxW);

          // Calculate height-constrained size
          let h = targetAvailH;
          let w = h * ratio;

          // If width overflows stage, switch to width-constrained size
          if (w > targetAvailW) {
            w = targetAvailW;
            h = w / ratio;
          }

          // Strict boundary clamp
          if (h > availH - 10) {
            h = availH - 10;
            w = h * ratio;
          }

          w = Math.max(minW, Math.min(maxW, Math.round(w)));
          h = Math.max(minH, Math.min(maxH, Math.round(h)));

          wrapper.style.setProperty("width", w + "px", "important");
          wrapper.style.setProperty("height", h + "px", "important");
          wrapper.style.setProperty("margin", "auto", "important");
        }

        window.addEventListener("resize", autoFitFlashcard);
        window.addEventListener("orientationchange", () => {
          setTimeout(autoFitFlashcard, 60);
          setTimeout(autoFitFlashcard, 250);
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

        const prevSwitch = window.switchScreen;
        window.switchScreen = function(id) {
          if (typeof prevSwitch === "function") prevSwitch(id);
          if (id === "screen-flashcard") {
            setTimeout(autoFitFlashcard, 20);
            setTimeout(autoFitFlashcard, 150);
            setTimeout(autoFitFlashcard, 400);
          }
        };

        const prevRender = window.renderCurrentCard;
        window.renderCurrentCard = function() {
          if (typeof prevRender === "function") prevRender();
          autoFitFlashcard();
        };

        // --- 2. Strict Double-Tap to Flip Engine ---
        // Single tap DOES NOT flip! Only double-tap or Flip button flips!
        const cardWrapper = document.getElementById("flashcard-wrapper");
        if (cardWrapper) {
          let lastCardTapTime = 0;
          let lastCardTapX = 0;
          let lastCardTapY = 0;

          function isInteractiveElement(target) {
            if (!target) return false;
            return Boolean(
              target.closest("button, .speak-btn, #front-speak-btn, #front-learned-btn, #front-delete-btn, .front-learned-btn, .front-delete-btn, input, textarea, a, .duo-btn-3d, .reset-deck-btn, #btn-reset-deck, #card-tamil-tile, #card-es-tile, #card-hi-tile")
            );
          }

          function triggerDoubleTapFlip(clientX, clientY) {
            if (typeof flipCard === "function") {
              flipCard();
            }
            if (typeof showDoubleTapCue === "function") {
              showDoubleTapCue(clientX, clientY);
            }
            if (typeof playHapticTick === "function") {
              playHapticTick(600, "sine", 0.04);
            }
          }

          // Handle Touch Double Tap
          let touchDownX = 0;
          let touchDownY = 0;
          let touchDownTime = 0;

          cardWrapper.addEventListener("touchstart", function(e) {
            if (isInteractiveElement(e.target)) return;
            const t = e.touches[0];
            touchDownX = t.clientX;
            touchDownY = t.clientY;
            touchDownTime = Date.now();
          }, { passive: true });

          cardWrapper.addEventListener("touchend", function(e) {
            if (isInteractiveElement(e.target)) return;
            const t = e.changedTouches[0];
            const dist = Math.hypot(t.clientX - touchDownX, t.clientY - touchDownY);
            const duration = Date.now() - touchDownTime;

            // Only consider clean stationary taps (not swipes)
            if (dist < 30 && duration < 380) {
              const now = Date.now();
              const gap = now - lastCardTapTime;
              const tapDist = Math.hypot(t.clientX - lastCardTapX, t.clientY - lastCardTapY);

              if (gap > 60 && gap < 480 && tapDist < 75) {
                // CONFIRMED DOUBLE TAP!
                lastCardTapTime = 0;
                e.preventDefault();
                triggerDoubleTapFlip(t.clientX, t.clientY);
              } else {
                lastCardTapTime = now;
                lastCardTapX = t.clientX;
                lastCardTapY = t.clientY;
                // Single tap does NOTHING!
              }
            }
          });

          // Handle Mouse Double Click / Double Tap
          cardWrapper.addEventListener("click", function(e) {
            if (isInteractiveElement(e.target)) return;
            const now = Date.now();
            const gap = now - lastCardTapTime;
            const clickDist = Math.hypot(e.clientX - lastCardTapX, e.clientY - lastCardTapY);

            if (gap > 60 && gap < 450 && clickDist < 50) {
              lastCardTapTime = 0;
              e.preventDefault();
              triggerDoubleTapFlip(e.clientX, e.clientY);
            } else {
              lastCardTapTime = now;
              lastCardTapX = e.clientX;
              lastCardTapY = e.clientY;
              // Single click does NOTHING!
            }
          });

          // Native desktop dblclick fallback
          cardWrapper.addEventListener("dblclick", function(e) {
            if (isInteractiveElement(e.target)) return;
            e.preventDefault();
            triggerDoubleTapFlip(e.clientX, e.clientY);
          });
        }

        // --- 3. Synchronize Learned Counters ---
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

        const prevRender2 = window.renderCurrentCard;
        window.renderCurrentCard = function() {
          if (typeof prevRender2 === "function") prevRender2();
          syncAllLearnedCounters();
          autoFitFlashcard();
        };

        syncAllLearnedCounters();
        if (document.readyState === "complete") {
          autoFitFlashcard();
        } else {
          window.addEventListener("load", autoFitFlashcard);
        }
      })();
`;

const finalScriptEnd = html.lastIndexOf('</script>');
html = html.slice(0, finalScriptEnd) + masterGestureAndAutoFitScript + '\n    ' + html.slice(finalScriptEnd);

fs.writeFileSync(indexPath, html, 'utf8');
console.log('Successfully written index.html! New length:', html.length);
