const fs = require('fs');
const path = require('path');

const indexPath = path.join(__dirname, '..', 'index.html');
let html = fs.readFileSync(indexPath, 'utf8');

console.log('Starting comprehensive overhaul on index.html, length:', html.length);

// 1. Ensure flashcard top nav actions includes the settings button
if (!html.includes('id="btn-flashcard-settings"')) {
  html = html.replace(
    'id="btn-shuffle"',
    'id="btn-shuffle"'
  );
  html = html.replace(
    '</button>\n            </div>\n          </div>\n          <!-- Single Slim Progress Line -->',
    `</button>
              <button type="button" class="duo-btn-3d" id="btn-flashcard-settings" title="Settings & Audio Studio" aria-label="Settings" style="width: 38px; height: 38px; border-radius: 12px; display: flex; align-items: center; justify-content: center; background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.16); box-shadow: 0 3px 0 rgba(0,0,0,0.4); color: #f1f5f9; cursor: pointer;">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="3"/>
                  <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
                </svg>
              </button>
            </div>
          </div>
          <!-- Single Slim Progress Line -->`
  );
  console.log('Ensured btn-flashcard-settings exists in top-nav-actions');
}

// 2. Wire btn-flashcard-settings in JavaScript
const wireSettingsJs = `
      // Wire Flashcard Screen Settings Button
      const btnFlashcardSettings = document.getElementById("btn-flashcard-settings");
      if (btnFlashcardSettings) {
        btnFlashcardSettings.addEventListener("click", (e) => {
          e.stopPropagation();
          openMenuDrawer();
        });
      }
`;

if (!html.includes('btnFlashcardSettings')) {
  html = html.replace('function openMenuDrawer() {', wireSettingsJs + '\n      function openMenuDrawer() {');
  console.log('Wired btnFlashcardSettings to openMenuDrawer');
}

// 3. Improve the drag interaction and double tap in the script
// Replace the touchstart, touchmove, touchend block with an ultra-responsive, rock-solid physical touch implementation
const oldTouchBlockStart = '// --- TOUCH EVENTS ---';
const oldTouchBlockEnd = '// --- DESKTOP MOUSE DRAG & DOUBLE CLICK ---';

const startIdx = html.indexOf(oldTouchBlockStart);
const endIdx = html.indexOf(oldTouchBlockEnd);

if (startIdx !== -1 && endIdx !== -1) {
  const newTouchBlock = `// --- ULTRA-RESPONSIVE PHYSICAL TOUCH & DOUBLE TAP PHYSICS ---
      let touchPressStartTime = 0;
      let lastTapTimestamp = 0;
      let lastTapCoords = { x: 0, y: 0 };

      cardWrapper.addEventListener("touchstart", (e) => {
        if (isCardInteractiveBtn(e.target) || isCardAnimating) return;
        if (typeof cardAudio !== "undefined" && cardAudio.unlock) cardAudio.unlock();
        const touch = e.touches[0];
        touchStartX = touch.clientX;
        touchStartY = touch.clientY;
        touchStartTime = performance.now();
        touchPressStartTime = Date.now();
        isSwiping = false;
        isDragging = true;
        velocitySamples = [{ x: touch.clientX, y: touch.clientY, time: performance.now() }];
        cardWrapper.style.transition = "none";
      }, { passive: true });

      cardWrapper.addEventListener("touchmove", (e) => {
        if (!isDragging || isCardInteractiveBtn(e.target) || isCardAnimating) return;
        const touch = e.touches[0];
        const diffX = touch.clientX - touchStartX;
        const diffY = touch.clientY - touchStartY;
        const absX = Math.abs(diffX);
        const absY = Math.abs(diffY);

        // Detect horizontal swipe intent (responsive threshold of 10px)
        if (absX > absY * 1.15 && absX > 10) {
          isSwiping = true;
          velocitySamples.push({ x: touch.clientX, y: touch.clientY, time: performance.now() });
          if (velocitySamples.length > 6) velocitySamples.shift();

          const isAtStart = currentIndex <= 0;
          const isAtEnd = currentIndex >= cards.length - 1;
          let effectiveX = diffX;
          if ((isAtStart && diffX > 0) || (isAtEnd && diffX < 0)) {
            // Elastic boundary resistance
            effectiveX = diffX * 0.28;
          }

          // Subtle physical card tilt during swipe
          const rotateAngle = (effectiveX * 0.045).toFixed(2);
          const flipTransform = isFlipped ? "rotateY(180deg)" : "";

          // Put translateX and rotateZ FIRST so screen direction is always preserved!
          cardWrapper.style.transform = \`translateX(\${effectiveX}px) rotateZ(\${rotateAngle}deg) \${flipTransform}\`;
        }
      }, { passive: true });

      cardWrapper.addEventListener("touchend", (e) => {
        if (!isDragging) return;
        isDragging = false;
        const touch = e.changedTouches[0];
        const diffX = touch.clientX - touchStartX;
        const diffY = touch.clientY - touchStartY;
        const dist = Math.hypot(diffX, diffY);
        const touchDuration = Date.now() - touchPressStartTime;

        if (isSwiping && Math.abs(diffX) > 28) {
          // Calculate true physical touch swipe velocity (px/ms)
          let vX = 0;
          if (velocitySamples.length >= 2) {
            const first = velocitySamples[0];
            const last = velocitySamples[velocitySamples.length - 1];
            const dt = Math.max(1, last.time - first.time);
            vX = (last.x - first.x) / dt;
          } else {
            const dt = Math.max(1, performance.now() - touchStartTime);
            vX = diffX / dt;
          }
          executeKineticSwipe(diffX, vX);
        } else if (dist < 45 && touchDuration < 320) {
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
        } else {
          // Smooth spring return to center if not enough kinetic swipe
          cardWrapper.style.transition = "transform 0.22s cubic-bezier(0.175, 0.885, 0.32, 1.275)";
          cardWrapper.style.transform = isFlipped ? "rotateY(180deg)" : "rotateY(0deg)";
        }
        isSwiping = false;
      });

      `;

  html = html.slice(0, startIdx) + newTouchBlock + html.slice(endIdx);
  console.log('Replaced touch gesture block with ultra-responsive physics & double tap');
}

// 4. Ensure executeKineticSwipe uses screen-first transform
html = html.replace(
  'cardWrapper.style.transform = `${isFlipped ? "rotateY(180deg) " : ""}translateX(${throwX}px) rotateZ(${throwRot}deg)`;',
  'cardWrapper.style.transform = `translateX(${throwX}px) rotateZ(${throwRot}deg) ${isFlipped ? "rotateY(180deg)" : ""}`;'
);

// 5. Update Desktop Mouse events to preserve screen space transform
html = html.replace(
  'cardWrapper.style.transform = `${flipBase} translateX(${effectiveX}px) rotateZ(${rotateAngle}deg)`;',
  'cardWrapper.style.transform = `translateX(${effectiveX}px) rotateZ(${rotateAngle}deg) ${flipBase}`;'
);

// 6. Make sure all modal close and backdrop events are wired
if (!html.includes('menuDrawerBackdrop.addEventListener("click", closeMenuDrawer)')) {
  const backdropWiring = `
      const menuDrawerBackdrop = document.getElementById("menu-drawer-backdrop");
      if (menuDrawerBackdrop) {
        menuDrawerBackdrop.addEventListener("click", closeMenuDrawer);
      }
      const drawerCloseBtn = document.getElementById("drawer-close-btn");
      if (drawerCloseBtn) {
        drawerCloseBtn.addEventListener("click", closeMenuDrawer);
      }
  `;
  html = html.replace('function closeMenuDrawer() {', backdropWiring + '\n      function closeMenuDrawer() {');
  console.log('Wired menuDrawerBackdrop and drawerCloseBtn');
}

// 7. Make sure reset deck button in settings is fully wired
const resetDeckSettingsWiring = `
      // Reset Deck in Settings
      const btnSettingsResetDeck = document.getElementById("btn-settings-reset-deck");
      if (btnSettingsResetDeck) {
        btnSettingsResetDeck.addEventListener("click", () => {
          resetFlashcardDeck();
          closeMenuDrawer();
        });
      }
`;
if (!html.includes('btnSettingsResetDeck.addEventListener')) {
  html = html.replace('function resetFlashcardDeck() {', resetDeckSettingsWiring + '\n      function resetFlashcardDeck() {');
  console.log('Wired btnSettingsResetDeck');
}

fs.writeFileSync(indexPath, html, 'utf8');
console.log('Finished applying comprehensive fix! Total length:', html.length);
