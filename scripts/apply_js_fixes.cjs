const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');
console.log('Original index.html length:', html.length);

// 1. Locate the block in script:
// From: function isCardInteractiveBtn(target) {
// To: frontSpeakBtn.addEventListener("click",

const startMarker = 'function isCardInteractiveBtn(target) {';
const endMarker = 'frontSpeakBtn.addEventListener("click",';

const startPos = html.indexOf(startMarker);
const endPos = html.indexOf(endMarker);

if (startPos === -1 || endPos === -1) {
  console.error('Markers not found! startPos:', startPos, 'endPos:', endPos);
  process.exit(1);
}

const replacementJs = `function isCardInteractiveBtn(target) {
        if (!target) return false;
        return Boolean(
          target.closest("button, .speak-btn, #front-speak-btn, #front-learned-btn, #front-delete-btn, .front-learned-btn, .front-delete-btn, .btn-audio-test, input, textarea, a, .duo-btn-3d, .reset-deck-btn, #btn-reset-deck")
        );
      }

      // Visual Speed Feedback Badge for Swipes
      let speedBadgeTimer = null;
      function showSpeedIndicator(text) {
        const badge = document.getElementById("swipe-speed-badge");
        if (!badge) return;
        badge.innerHTML = \`⚡ <span>\${text}</span>\`;
        badge.classList.add("show");
        clearTimeout(speedBadgeTimer);
        speedBadgeTimer = setTimeout(() => {
          badge.classList.remove("show");
        }, 750);
      }

      // Visual Ripple Cue for Double Tap
      function showDoubleTapCue(clientX, clientY) {
        const stage = document.querySelector(".card-stage");
        if (!stage) return;
        const ripple = document.createElement("div");
        ripple.className = "double-tap-ripple";
        const rect = stage.getBoundingClientRect();
        const posX = clientX ? (clientX - rect.left) : (rect.width / 2);
        const posY = clientY ? (clientY - rect.top) : (rect.height / 2);
        ripple.style.left = posX + "px";
        ripple.style.top = posY + "px";
        stage.appendChild(ripple);
        setTimeout(() => ripple.remove(), 450);
      }

      // =========================================================================
      // DYNAMIC SWIPE & PHYSICAL TOUCH FORCE KINETICS
      // =========================================================================
      let isSwiping = false;
      let isDragging = false;
      let touchStartX = 0;
      let touchStartY = 0;
      let touchStartTime = 0;
      let velocitySamples = [];
      let lastTapTime = 0;
      let lastTapX = 0;
      let lastTapY = 0;
      let suppressSyntheticClickUntil = 0;
      let isCardAnimating = false;

      function executeKineticSwipe(diffX, velocityX) {
        if (isCardAnimating) return;
        const distance = Math.abs(diffX);
        const speed = Math.abs(velocityX) || 0;
        // Physical touch kinetic force = displacement + speed momentum factor
        const kineticForce = distance + (speed * 280);

        const goingNext = diffX < 0;
        const atBoundary = (goingNext && currentIndex >= cards.length - 1) || (!goingNext && currentIndex <= 0);

        if (atBoundary) {
          // Elastic rubber-band spring snapback
          cardWrapper.style.transition = "transform 0.22s cubic-bezier(0.175, 0.885, 0.32, 1.275)";
          cardWrapper.style.transform = isFlipped ? "rotateY(180deg)" : "rotateY(0deg)";
          if (typeof playHapticTick === "function") playHapticTick(280, "sine", 0.03);
          return;
        }

        // Dynamic multi-card progression based on swipe force & speed
        // Reflects user intent dynamically instead of just moving one card!
        let steps = 1;
        if (kineticForce >= 580 || speed >= 2.0) {
          steps = 4; // High power flick: advances 4 cards!
        } else if (kineticForce >= 380 || speed >= 1.25) {
          steps = 3; // Fast swipe: advances 3 cards!
        } else if (kineticForce >= 180 || speed >= 0.6) {
          steps = 2; // Medium flick: advances 2 cards!
        } else {
          steps = 1; // Gentle swipe: advances 1 card!
        }

        // Clamp steps to remaining deck size
        if (goingNext) {
          steps = Math.min(steps, (cards.length - 1) - currentIndex);
        } else {
          steps = Math.min(steps, currentIndex);
        }
        steps = Math.max(1, steps);

        // Proportional animation speed:
        // Higher touch speed = faster, snappier throw!
        const durationMs = Math.max(85, Math.min(230, Math.round(200 / Math.max(0.65, speed))));
        isCardAnimating = true;

        // 1. Kinetic throw off-screen in swipe direction
        const throwX = (goingNext ? -1 : 1) * (window.innerWidth + 120);
        const throwRot = (goingNext ? -1 : 1) * 16;
        cardWrapper.style.transition = \`transform \${durationMs}ms cubic-bezier(0.2, 0.9, 0.3, 1)\`;
        cardWrapper.style.transform = \`\${isFlipped ? "rotateY(180deg) " : ""}translateX(\${throwX}px) rotateZ(\${throwRot}deg)\`;

        // 2. Advance index and slide in target card smoothly from opposite side
        setTimeout(() => {
          if (goingNext) {
            currentIndex += steps;
          } else {
            currentIndex -= steps;
          }
          isFlipped = false;
          cardWrapper.classList.remove("flipped");
          renderCurrentCard();

          // Position incoming card on opposite side
          const enterX = (goingNext ? 1 : -1) * 65;
          const enterRot = (goingNext ? 1 : -1) * 3.5;
          cardWrapper.style.transition = "none";
          cardWrapper.style.transform = \`translateX(\${enterX}px) rotateZ(\${enterRot}deg)\`;

          // Force browser reflow
          void cardWrapper.offsetHeight;

          // Animate smoothly to center
          const inDuration = Math.max(105, Math.round(durationMs * 0.88));
          cardWrapper.style.transition = \`transform \${inDuration}ms cubic-bezier(0.16, 1, 0.3, 1)\`;
          cardWrapper.style.transform = "rotateY(0deg) translateX(0) rotateZ(0)";

          setTimeout(() => {
            isCardAnimating = false;
          }, inDuration + 10);

          if (typeof playHapticTick === "function") {
            playHapticTick(460 + Math.min(200, steps * 40), "sine", 0.04);
          }

          if (steps > 1) {
            showSpeedIndicator(goingNext ? \`Fast Swipe: +\${steps} Cards\` : \`Fast Swipe: -\${steps} Cards\`);
          }
        }, Math.round(durationMs * 0.65));
      }

      // --- TOUCH EVENTS ---
      cardWrapper.addEventListener("touchstart", (e) => {
        if (isCardInteractiveBtn(e.target) || isCardAnimating) return;
        cardAudio.unlock();
        const touch = e.touches[0];
        touchStartX = touch.clientX;
        touchStartY = touch.clientY;
        touchStartTime = performance.now();
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

        if (Math.abs(diffX) > Math.abs(diffY) * 1.15 && Math.abs(diffX) > 8) {
          isSwiping = true;
          velocitySamples.push({ x: touch.clientX, y: touch.clientY, time: performance.now() });
          if (velocitySamples.length > 5) velocitySamples.shift();

          const isAtStart = currentIndex <= 0;
          const isAtEnd = currentIndex >= cards.length - 1;
          let effectiveX = diffX;
          if ((isAtStart && diffX > 0) || (isAtEnd && diffX < 0)) {
            effectiveX = diffX * 0.32;
          }
          const rotateAngle = (effectiveX * 0.045).toFixed(2);
          const flipBase = isFlipped ? "rotateY(180deg)" : "rotateY(0deg)";
          cardWrapper.style.transform = \`\${flipBase} translateX(\${effectiveX}px) rotateZ(\${rotateAngle}deg)\`;
        }
      }, { passive: true });

      cardWrapper.addEventListener("touchend", (e) => {
        if (!isDragging) return;
        isDragging = false;
        const touch = e.changedTouches[0];
        const diffX = touch.clientX - touchStartX;
        const diffY = touch.clientY - touchStartY;
        const dist = Math.hypot(diffX, diffY);

        if (isSwiping && Math.abs(diffX) > 28) {
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
        } else if (dist < 18) {
          // Stationary tap: ROCK-SOLID DOUBLE TAP DETECTION
          if (!isCardInteractiveBtn(e.target)) {
            const now = Date.now();
            const tapDist = Math.hypot(touch.clientX - lastTapX, touch.clientY - lastTapY);
            if (now - lastTapTime < 450 && tapDist < 55) {
              lastTapTime = 0;
              suppressSyntheticClickUntil = Date.now() + 650;
              flipCard();
              showDoubleTapCue(touch.clientX, touch.clientY);
            } else {
              lastTapTime = now;
              lastTapX = touch.clientX;
              lastTapY = touch.clientY;
            }
          }
        } else {
          // Snap back to center
          cardWrapper.style.transition = "transform 0.18s cubic-bezier(0.175, 0.885, 0.32, 1.275)";
          cardWrapper.style.transform = isFlipped ? "rotateY(180deg)" : "rotateY(0deg)";
        }
        isSwiping = false;
      });

      // --- DESKTOP MOUSE DRAG & DOUBLE CLICK ---
      let isMouseDown = false;
      let mouseStartX = 0;
      let mouseStartY = 0;
      let mouseStartTime = 0;
      let mouseSamples = [];

      cardWrapper.addEventListener("mousedown", (e) => {
        if (isCardInteractiveBtn(e.target) || isCardAnimating || e.button !== 0) return;
        isMouseDown = true;
        mouseStartX = e.clientX;
        mouseStartY = e.clientY;
        mouseStartTime = performance.now();
        mouseSamples = [{ x: e.clientX, y: e.clientY, time: performance.now() }];
        cardWrapper.style.transition = "none";
      });

      window.addEventListener("mousemove", (e) => {
        if (!isMouseDown || isCardAnimating) return;
        const diffX = e.clientX - mouseStartX;
        const diffY = e.clientY - mouseStartY;
        if (Math.abs(diffX) > 8) {
          mouseSamples.push({ x: e.clientX, y: e.clientY, time: performance.now() });
          if (mouseSamples.length > 5) mouseSamples.shift();

          const isAtStart = currentIndex <= 0;
          const isAtEnd = currentIndex >= cards.length - 1;
          let effectiveX = diffX;
          if ((isAtStart && diffX > 0) || (isAtEnd && diffX < 0)) {
            effectiveX = diffX * 0.32;
          }
          const rotateAngle = (effectiveX * 0.045).toFixed(2);
          const flipBase = isFlipped ? "rotateY(180deg)" : "rotateY(0deg)";
          cardWrapper.style.transform = \`\${flipBase} translateX(\${effectiveX}px) rotateZ(\${rotateAngle}deg)\`;
        }
      });

      window.addEventListener("mouseup", (e) => {
        if (!isMouseDown) return;
        isMouseDown = false;
        const diffX = e.clientX - mouseStartX;
        const diffY = e.clientY - mouseStartY;
        const dist = Math.hypot(diffX, diffY);

        if (Math.abs(diffX) > 28) {
          let vX = 0;
          if (mouseSamples.length >= 2) {
            const first = mouseSamples[0];
            const last = mouseSamples[mouseSamples.length - 1];
            const dt = Math.max(1, last.time - first.time);
            vX = (last.x - first.x) / dt;
          } else {
            const dt = Math.max(1, performance.now() - mouseStartTime);
            vX = diffX / dt;
          }
          executeKineticSwipe(diffX, vX);
        } else if (dist < 10) {
          // Stationary click: let dblclick handle flipping
        } else {
          cardWrapper.style.transition = "transform 0.18s cubic-bezier(0.175, 0.885, 0.32, 1.275)";
          cardWrapper.style.transform = isFlipped ? "rotateY(180deg)" : "rotateY(0deg)";
        }
      });

      // Desktop native double-click
      cardWrapper.addEventListener("dblclick", (e) => {
        if (isCardInteractiveBtn(e.target)) return;
        flipCard();
        showDoubleTapCue(e.clientX, e.clientY);
      });

      // Suppress synthetic click interference from mobile touch
      cardWrapper.addEventListener("click", (e) => {
        if (Date.now() < suppressSyntheticClickUntil) {
          e.preventDefault();
          e.stopPropagation();
          return;
        }
        // Single click does NOT flip card! Only double-tap or Flip button flips!
      });

      // =========================================================================
      // DELETE FLASHCARD WITH AUTOMATIC CONTINUOUS RENUMBERING
      // =========================================================================
      function deleteCurrentCard() {
        if (!cards || cards.length <= 1) {
          if (typeof showToast === "function") showToast("Cannot delete the last remaining card!");
          return;
        }
        const targetCard = cards[currentIndex];
        if (!targetCard) return;

        const rawNum = targetCard.originalNum || targetCard.num;
        if (!deletedCardNums.includes(rawNum)) {
          deletedCardNums.push(rawNum);
        }
        try {
          localStorage.setItem(DELETED_CARDS_STORAGE_KEY, JSON.stringify(deletedCardNums));
        } catch(e) {}

        // Automatically renumbers all remaining cards sequentially starting from 800!
        reindexAndBuildCards();

        if (currentIndex >= cards.length) {
          currentIndex = cards.length - 1;
        }

        isFlipped = false;
        if (cardWrapper) {
          cardWrapper.classList.remove("flipped");
          cardWrapper.style.transform = "rotateY(0deg) translateX(0) rotateZ(0)";
        }

        renderCurrentCard();
        updateSectionLearnedCounter();

        if (typeof playHapticTick === "function") playHapticTick(320, "sine", 0.05);

        // Show toast with auto-renumber details and quick UNDO
        const toast = document.getElementById("app-toast");
        if (toast) {
          toast.innerHTML = \`
            <div style="display: flex; align-items: center; justify-content: space-between; gap: 14px; width: 100%;">
              <span>Deleted card #\${targetCard.displayNum || targetCard.num} (\${targetCard.word}) · Order updated (800–\${800 + cards.length - 1})</span>
              <button type="button" id="btn-undo-delete-card" class="duo-btn-3d" style="padding: 4px 12px; background: rgba(56, 189, 248, 0.25); border: 1px solid rgba(56, 189, 248, 0.5); color: #38bdf8; border-radius: 8px; font-weight: 800; font-size: 0.8rem; cursor: pointer;">
                UNDO
              </button>
            </div>
          \`;
          toast.classList.add("show");
          const undoBtn = document.getElementById("btn-undo-delete-card");
          if (undoBtn) {
            undoBtn.onclick = () => {
              deletedCardNums = deletedCardNums.filter(n => n !== rawNum);
              try {
                localStorage.setItem(DELETED_CARDS_STORAGE_KEY, JSON.stringify(deletedCardNums));
              } catch(e) {}
              reindexAndBuildCards();
              const restoredIdx = cards.findIndex(c => (c.originalNum || c.num) === rawNum);
              if (restoredIdx !== -1) currentIndex = restoredIdx;
              renderCurrentCard();
              updateSectionLearnedCounter();
              toast.classList.remove("show");
              if (typeof playHapticTick === "function") playHapticTick(580, "sine", 0.05);
            };
          }
          clearTimeout(toast._timer);
          toast._timer = setTimeout(() => {
            toast.classList.remove("show");
          }, 4500);
        }
      }

      // =========================================================================
      // RESET FLASHCARD DECK & RESTORE DELETED CARDS
      // =========================================================================
      function resetFlashcardDeck() {
        deletedCardNums = [];
        try {
          localStorage.removeItem(DELETED_CARDS_STORAGE_KEY);
        } catch (e) {}
        reindexAndBuildCards();
        currentIndex = 0;
        isFlipped = false;
        if (cardWrapper) {
          cardWrapper.classList.remove("flipped");
          cardWrapper.style.transform = "rotateY(0deg) translateX(0) rotateZ(0)";
        }
        renderCurrentCard();
        updateSectionLearnedCounter();
        if (typeof playHapticTick === "function") playHapticTick(620, "triangle", 0.08);
        if (typeof showToast === "function") showToast("Flashcard deck reset! All 200 cards restored (800–1000).");
      }

      // =========================================================================
      // LEARNED TOGGLE FUNCTIONALITY
      // =========================================================================
      function toggleLearnedCard(targetNum) {
        const currentCard = cards[currentIndex];
        if (!currentCard) return;
        const num = targetNum || currentCard.originalNum || currentCard.num;

        if (learnedCardsSet.has(num) || learnedCardsSet.has(String(num))) {
          learnedCardsSet.delete(num);
          learnedCardsSet.delete(String(num));
          if (typeof playHapticTick === "function") playHapticTick(400, "sine", 0.03);
          if (typeof showToast === "function") showToast("Card marked as unlearned");
        } else {
          learnedCardsSet.add(num);
          if (typeof playHapticTick === "function") playHapticTick(750, "triangle", 0.06);
          if (typeof showToast === "function") showToast("Card marked as learned! 🌟");
        }
        saveLearnedCards();
        updateCardLearnedUI(num);
        updateSectionLearnedCounter();
        if (currentCategoryEl) {
          const sectionLearned = getSectionLearnedCount();
          currentCategoryEl.innerHTML = \`<span>Learned:</span> <strong id="section-learned-count" style="color: #34d399;">\${sectionLearned}</strong> / <span id="section-total-count">\${cards.length}</span>\`;
        }
      }

      // Wire Front Learned Button (Icon Only, No text)
      const frontLearnedBtn = document.getElementById("front-learned-btn");
      if (frontLearnedBtn) {
        frontLearnedBtn.addEventListener("click", (e) => {
          e.stopPropagation();
          e.preventDefault();
          toggleLearnedCard();
        });
        frontLearnedBtn.addEventListener("touchstart", (e) => e.stopPropagation(), { passive: false });
      }

      // Wire Front Delete Button (Icon Only, No text)
      const frontDeleteBtn = document.getElementById("front-delete-btn");
      if (frontDeleteBtn) {
        frontDeleteBtn.addEventListener("click", (e) => {
          e.stopPropagation();
          e.preventDefault();
          deleteCurrentCard();
        });
        frontDeleteBtn.addEventListener("touchstart", (e) => e.stopPropagation(), { passive: false });
      }

      // Wire Reset Deck Button (Top Header Action)
      const btnResetDeck = document.getElementById("btn-reset-deck");
      if (btnResetDeck) {
        btnResetDeck.addEventListener("click", (e) => {
          e.stopPropagation();
          e.preventDefault();
          resetFlashcardDeck();
        });
      }

      // Also support legacy IDs safely if present
      const btnDeleteCard = document.getElementById("btn-delete-card");
      if (btnDeleteCard) {
        btnDeleteCard.addEventListener("click", (e) => {
          e.stopPropagation();
          deleteCurrentCard();
        });
      }

      `;

html = html.slice(0, startPos) + replacementJs + html.slice(endPos);
console.log('Replaced JS gesture and delete block.');

// Also update updateCardLearnedUI function to update front-learned-btn
const updateUiStart = html.indexOf('function updateCardLearnedUI(');
if (updateUiStart !== -1) {
  const updateUiEnd = html.indexOf('/* ==========================================================\n         RESUME POSITION SYSTEM', updateUiStart);
  if (updateUiEnd !== -1) {
    const newUpdateUi = `function updateCardLearnedUI(cardNum) {
        if (!learnedCardsSet) return;
        const currentCard = cards[currentIndex];
        const raw = (currentCard && (currentCard.originalNum || currentCard.num)) || cardNum;
        const isLearned = learnedCardsSet.has(raw) || learnedCardsSet.has(String(raw)) || learnedCardsSet.has(cardNum) || learnedCardsSet.has(String(cardNum));

        // Front face icon-only button
        const frontLearnedBtn = document.getElementById("front-learned-btn");
        if (frontLearnedBtn) {
          if (isLearned) {
            frontLearnedBtn.classList.add("is-learned");
            frontLearnedBtn.setAttribute("title", "Card learned! (Tap to unmark)");
            frontLearnedBtn.setAttribute("aria-label", "Card learned! Tap to unmark");
          } else {
            frontLearnedBtn.classList.remove("is-learned");
            frontLearnedBtn.setAttribute("title", "Mark as learned");
            frontLearnedBtn.setAttribute("aria-label", "Mark as learned");
          }
        }
      }
      `;
    html = html.slice(0, updateUiStart) + newUpdateUi + html.slice(updateUiEnd);
    console.log('Updated updateCardLearnedUI.');
  }
}

fs.writeFileSync('index.html', html, 'utf8');
console.log('Done writing index.html! New length:', html.length);
