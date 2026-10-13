const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

// 1. Remove front card-hint-footer ("Tap card to flip")
const frontCueRegex = /\s*<!-- Clear Tap Hint -->\s*<div class="card-hint-footer" id="card-cue-front">[\s\S]*?<\/div>/;
if (frontCueRegex.test(html)) {
  html = html.replace(frontCueRegex, '');
  console.log('Removed front card-cue-front successfully');
} else {
  console.log('Warning: frontCueRegex did not match');
}

// 2. Remove back card-hint-footer ("Tap card to flip back")
const backCueRegex = /\s*<!-- Cue: Tap to flip back -->\s*<div class="card-hint-footer" id="card-cue-back">[\s\S]*?<\/div>/;
if (backCueRegex.test(html)) {
  html = html.replace(backCueRegex, '');
  console.log('Removed back card-cue-back successfully');
} else {
  console.log('Warning: backCueRegex did not match');
}

// 3. Remove unwanted hardcoded "KITCHEN" label on front card header
const catLabelRegex = /<span class="card-unboxed-cat" id="front-card-cat-label">KITCHEN<\/span>\s*/;
if (catLabelRegex.test(html)) {
  html = html.replace(catLabelRegex, '');
  console.log('Removed unwanted front-card-cat-label successfully');
} else {
  console.log('Warning: catLabelRegex did not match');
}

// 4. Update CSS for shortcut-grid: stack vertically (up side and down side), no horizontal compression!
// Replace the earlier CSS rule
html = html.replace(
  /\.shortcut-grid\s*\{\s*display:\s*grid\s*!important;\s*grid-template-columns:\s*1fr\s*1fr\s*!important;\s*gap:\s*8px\s*!important;\s*\}/g,
  `.shortcut-grid {
        display: flex !important;
        flex-direction: column !important;
        gap: 8px !important;
        width: 100% !important;
      }`
);

// Also replace standard .shortcut-grid definition if needed
html = html.replace(
  /\.shortcut-grid\s*\{\s*display:\s*flex;\s*flex-direction:\s*column;\s*gap:\s*6px;\s*\}/g,
  `.shortcut-grid {
        display: flex !important;
        flex-direction: column !important;
        gap: 8px !important;
        width: 100% !important;
      }`
);

// Add top nav and shortcut enhancements in CSS
const styleEnhancement = `
      /* Double Tap & Clean Flashcard Layout Overrides */
      .card-hint-footer {
        display: none !important;
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
        gap: 8px !important;
        width: 100% !important;
      }
      .flashcard-top-nav .breadcrumb-back-btn {
        flex-shrink: 0 !important;
        display: inline-flex !important;
        align-items: center !important;
        gap: 6px !important;
        padding: 7px 12px !important;
        border-radius: 9999px !important;
        background: rgba(255, 255, 255, 0.06) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        color: #f1f5f9 !important;
        font-size: 0.8rem !important;
        font-weight: 700 !important;
        cursor: pointer !important;
        transition: all 0.18s ease !important;
        white-space: nowrap !important;
      }
      .flashcard-top-nav .top-nav-center-group {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 6px !important;
        flex: 1 1 auto !important;
        min-width: 0 !important;
      }
      .flashcard-top-nav .top-category-pill {
        font-size: 0.78rem !important;
        font-weight: 600 !important;
        color: #cbd5e1 !important;
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        padding: 5px 11px !important;
        border-radius: 9999px !important;
        max-width: 170px !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        text-align: center !important;
      }
      .flashcard-top-nav .counter-display {
        flex-shrink: 0 !important;
        display: inline-flex !important;
        align-items: center !important;
        gap: 3px !important;
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        padding: 5px 10px !important;
        border-radius: 9999px !important;
        font-variant-numeric: tabular-nums !important;
        font-size: 0.8rem !important;
        font-weight: 700 !important;
        color: #e2e8f0 !important;
        white-space: nowrap !important;
      }
      .flashcard-top-nav .top-nav-actions {
        flex-shrink: 0 !important;
        display: flex !important;
        align-items: center !important;
        gap: 6px !important;
      }
      .flashcard-top-nav .btn-top-learned-toggle {
        display: inline-flex !important;
        align-items: center !important;
        gap: 5px !important;
        padding: 6px 11px !important;
        border-radius: 9999px !important;
        background: rgba(255, 255, 255, 0.06) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        color: #cbd5e1 !important;
        font-size: 0.76rem !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        white-space: nowrap !important;
      }
      .flashcard-top-nav .shuffle-btn {
        width: 32px !important;
        height: 32px !important;
        border-radius: 9px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.09) !important;
        color: #94a3b8 !important;
        cursor: pointer !important;
      }
      .shortcut-section {
        background: rgba(15, 23, 42, 0.5) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 14px !important;
        padding: 10px 12px !important;
        width: 100% !important;
        box-sizing: border-box !important;
      }
      .shortcut-grid {
        display: flex !important;
        flex-direction: column !important;
        gap: 8px !important;
        width: 100% !important;
      }
      .shortcut-box {
        width: 100% !important;
        box-sizing: border-box !important;
        padding: 8px 12px !important;
        border-radius: 12px !important;
        background: rgba(0, 0, 0, 0.28) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
      }
      .shortcut-box-es {
        border-left: 3px solid #f43f5e !important;
        background: rgba(244, 63, 94, 0.06) !important;
      }
      .shortcut-box-hi {
        border-left: 3px solid #f59e0b !important;
        background: rgba(245, 158, 11, 0.06) !important;
      }
      .shortcut-box-top {
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        margin-bottom: 3px !important;
      }
      .shortcut-lang-label {
        font-size: 0.72rem !important;
        font-weight: 750 !important;
        letter-spacing: 0.04em !important;
        text-transform: uppercase !important;
      }
      .shortcut-target-word {
        font-size: 0.82rem !important;
        font-weight: 700 !important;
        color: #ffffff !important;
      }
      .shortcut-punchline {
        font-size: 0.8rem !important;
        color: #cbd5e1 !important;
        line-height: 1.4 !important;
        margin-top: 2px !important;
      }
`;

// Insert styleEnhancement right before </style>
html = html.replace('</style>', styleEnhancement + '\n    </style>');

// 5. Update Touch & Click event listeners for STRICT DOUBLE TAP TO FLIP!
const oldTouchBlock = `        if (isHorizontalSwipe && Math.abs(diffX) > 42) {
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

const newTouchBlock = `        if (isHorizontalSwipe && Math.abs(diffX) > 42) {
          // Swipe to next or prev
          if (diffX < 0) {
            nextCard();
          } else {
            prevCard();
          }
        } else if (Math.abs(diffX) < 14 && Math.abs(diffY) < 14) {
          // STRICT DOUBLE TAP DETECTION: single tap NEVER flips card!
          if (!isActionElement(e.target)) {
            const now = Date.now();
            const tapDist = Math.hypot(touch.clientX - lastTapX, touch.clientY - lastTapY);
            if (now - lastTapTime < 380 && tapDist < 50) {
              // Valid Double Tap! Flip card
              lastTapTime = 0;
              ignoreSyntheticClicksUntil = now + 500;
              flipCard();
            } else {
              // First tap: register timestamp for double-tap detection
              lastTapTime = now;
              lastTapX = touch.clientX;
              lastTapY = touch.clientY;
            }
          }
        }
        isHorizontalSwipe = false;
      });

      // Desktop: Double-click flips the card; single-click does NOT flip!
      cardWrapper.addEventListener("dblclick", (e) => {
        if (isActionElement(e.target)) return;
        flipCard();
      });
      // Single click on card does NOT flip the card
      cardWrapper.addEventListener("click", (e) => {
        if (isActionElement(e.target)) return;
        // Single click does NOT flip card! Double tap/click or footer Flip button required.
      });`;

if (html.includes(oldTouchBlock)) {
  html = html.replace(oldTouchBlock, newTouchBlock);
  console.log('Replaced touch/click handlers with double-tap logic successfully');
} else {
  console.log('Searching with looser whitespace for touch block...');
  // Let's replace specifically
  const touchSearch = html.indexOf('cardWrapper.addEventListener("touchend"');
  if (touchSearch !== -1) {
    const clickSearch = html.indexOf('// Front Face Shortcut Button', touchSearch);
    if (clickSearch !== -1) {
      console.log('Found touch block boundaries!');
      const before = html.slice(0, touchSearch);
      const after = html.slice(clickSearch);
      const replacement = `cardWrapper.addEventListener("touchend", (e) => {
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
          // STRICT DOUBLE TAP DETECTION: single tap NEVER flips card!
          if (!isActionElement(e.target)) {
            const now = Date.now();
            const tapDist = Math.hypot(touch.clientX - lastTapX, touch.clientY - lastTapY);
            if (now - lastTapTime < 380 && tapDist < 50) {
              // Valid Double Tap! Flip card
              lastTapTime = 0;
              ignoreSyntheticClicksUntil = now + 500;
              flipCard();
            } else {
              // First tap: register timestamp for double-tap detection
              lastTapTime = now;
              lastTapX = touch.clientX;
              lastTapY = touch.clientY;
            }
          }
        }
        isHorizontalSwipe = false;
      });

      // Desktop: Double-click flips the card; single-click does NOT flip!
      cardWrapper.addEventListener("dblclick", (e) => {
        if (isActionElement(e.target)) return;
        flipCard();
      });
      // Single click on card does NOT flip the card
      cardWrapper.addEventListener("click", (e) => {
        if (isActionElement(e.target)) return;
        // Single click does NOT flip card! Double tap/click or footer Flip button required.
      });

      `;
      html = before + replacement + after;
      console.log('Replaced touch and click listeners successfully via boundaries!');
    }
  }
}

fs.writeFileSync('index.html', html, 'utf8');
console.log('Updated index.html successfully!');
