const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

// =========================================================================
// 1. UPDATE CARDS ARRAY DECLARATION: Rename initial list & setup reindexing
// =========================================================================
const oldCardsDeclaration = 'const cards = [';
const newCardsDeclaration = 'const initialDeckCards = [';

if (html.includes(oldCardsDeclaration)) {
  html = html.replace(oldCardsDeclaration, newCardsDeclaration);
  console.log('Renamed cards to initialDeckCards!');
}

// Find the end of initialDeckCards
const endCardsMarker = 'category: "Financial Institutions", gifUrl: "", trans: { es: "banco", hi: "bank" }, tamil: "வங்கி" }\n      ];';
const reindexSetupCode = `category: "Financial Institutions", gifUrl: "", trans: { es: "banco", hi: "bank" }, tamil: "வங்கி" }
      ];

      /* ==========================================================
         AUTOMATIC SEQUENTIAL REINDEXING & PERSISTENT DELETION SYSTEM
         ========================================================== */
      const DELETED_CARDS_STORAGE_KEY = "vocab_deleted_cards_v3";
      let deletedCardNums = [];
      try {
        deletedCardNums = JSON.parse(localStorage.getItem(DELETED_CARDS_STORAGE_KEY) || "[]");
        if (!Array.isArray(deletedCardNums)) deletedCardNums = [];
      } catch(e) {
        deletedCardNums = [];
      }

      let cards = [];
      function reindexAndBuildCards() {
        cards = initialDeckCards
          .filter(c => !deletedCardNums.includes(c.num))
          .map((c, idx) => ({
            ...c,
            originalNum: c.num,
            num: 800 + idx, // Dynamically renumbered sequentially starting from 800
            displayNum: 800 + idx
          }));
      }
      reindexAndBuildCards();

      function getSectionLearnedCount() {
        if (!cards || cards.length === 0) return 0;
        let count = 0;
        cards.forEach(card => {
          const raw = card.originalNum || card.num;
          if (learnedCardsSet && (learnedCardsSet.has(raw) || learnedCardsSet.has(String(raw)) || learnedCardsSet.has(card.num) || learnedCardsSet.has(String(card.num)))) {
            count++;
          }
        });
        return count;
      }

      function updateSectionLearnedCounter() {
        const learnedCount = getSectionLearnedCount();
        const learnedEl = document.getElementById("section-learned-count");
        const totalEl = document.getElementById("section-total-count");
        if (learnedEl) learnedEl.textContent = learnedCount;
        if (totalEl) totalEl.textContent = cards.length;

        // Subsections card stat line
        const tier800Stat = document.getElementById("tier-800-stat-line");
        if (tier800Stat) tier800Stat.textContent = \`\${learnedCount} / \${cards.length} Learned\`;
        const tier800Bar = document.getElementById("tier-800-progress-bar");
        if (tier800Bar && cards.length > 0) {
          tier800Bar.style.width = \`\${Math.min(100, Math.round((learnedCount / cards.length) * 100))}%\`;
        }
        const tier800StatHint = document.getElementById("tier-800-learned-stat");
        if (tier800StatHint) tier800StatHint.textContent = \`\${learnedCount} / \${cards.length} in active tier\`;
      }
`;

if (html.includes(endCardsMarker)) {
  html = html.replace(endCardsMarker, reindexSetupCode);
  console.log('Injected reindexSetupCode!');
} else {
  console.log('Trying flexible match for end of cards array...');
  html = html.replace(/tamil:\s*"வங்கி"\s*\}\s*\];/, reindexSetupCode);
  console.log('Injected reindexSetupCode via regex!');
}

// =========================================================================
// 2. UPDATE renderCurrentCard() TO UPDATE TOP BADGE AND SEQUENTIAL COUNTERS
// =========================================================================
const renderCurrentCardOldHeader = `        // Header and Counter
        if (currentCategoryEl) currentCategoryEl.textContent = card.category;
        if (isShuffled) {
          counterCurrentEl.textContent = currentIndex + 1;
          counterTotalEl.textContent = cards.length;
        } else {
          counterCurrentEl.textContent = card.num;
          counterTotalEl.textContent = cards[cards.length - 1].num;
        }`;

const renderCurrentCardNewHeader = `        // Header and Counter (Learned count out of section total replaces Kitchen & Cooking)
        if (currentCategoryEl) {
          const sectionLearned = getSectionLearnedCount();
          currentCategoryEl.innerHTML = \`<span>Learned:</span> <strong id="section-learned-count" style="color: #34d399;">\${sectionLearned}</strong> / <span id="section-total-count">\${cards.length}</span>\`;
        }
        if (isShuffled) {
          counterCurrentEl.textContent = currentIndex + 1;
          counterTotalEl.textContent = cards.length;
        } else {
          counterCurrentEl.textContent = card.displayNum || (800 + currentIndex);
          counterTotalEl.textContent = cards.length > 0 ? (cards[cards.length - 1].displayNum || (800 + cards.length - 1)) : 1000;
        }`;

if (html.includes(renderCurrentCardOldHeader)) {
  html = html.replace(renderCurrentCardOldHeader, renderCurrentCardNewHeader);
  console.log('Updated renderCurrentCard header & counters!');
} else {
  // Regex fallback
  html = html.replace(/if\s*\(currentCategoryEl\)\s*currentCategoryEl\.textContent\s*=\s*card\.category;[\s\S]*?counterTotalEl\.textContent\s*=\s*cards\[cards\.length\s*-\s*1\]\.num;\s*\}/, renderCurrentCardNewHeader);
  console.log('Updated renderCurrentCard header & counters via regex!');
}

// Also update image and anim lookup to use card.originalNum || card.num
const oldImgLookup = `const primaryImgUrl = (typeof cardAccurateImages !== "undefined" && cardAccurateImages[card.num]) 
          ? cardAccurateImages[card.num] 
          : \`/api/image?num=\${card.num}\`;
        const animInfo = cardAnims[card.num] || null;`;

const newImgLookup = `const lookupId = card.originalNum || card.num;
        const primaryImgUrl = (typeof cardAccurateImages !== "undefined" && cardAccurateImages[lookupId]) 
          ? cardAccurateImages[lookupId] 
          : \`/api/image?num=\${lookupId}\`;
        const animInfo = cardAnims[lookupId] || null;`;

if (html.includes(oldImgLookup)) {
  html = html.replace(oldImgLookup, newImgLookup);
  console.log('Updated image & animation lookup!');
} else {
  html = html.replace(/cardAccurateImages\[card\.num\]/g, 'cardAccurateImages[card.originalNum || card.num]');
  html = html.replace(/cardAnims\[card\.num\]/g, 'cardAnims[card.originalNum || card.num]');
  console.log('Replaced card image num lookups with fallback!');
}

// =========================================================================
// 3. REPLACE TOUCH AND DOUBLE-TAP HANDLERS WITH FORCE-SWIPE & BULLETPROOF DOUBLE-TAP
// =========================================================================
const touchStartMarker = 'cardWrapper.addEventListener("touchstart",';
const touchEndMarker = '// Front Face Shortcut Button';

const touchStartIdx = html.indexOf(touchStartMarker);
const touchEndIdx = html.indexOf(touchEndMarker, touchStartIdx);

if (touchStartIdx !== -1 && touchEndIdx !== -1) {
  const newTouchCode = `// ==========================================================
      // ENHANCED KINETIC FORCE-SWIPE & BULLETPROOF DOUBLE-TAP
      // ==========================================================
      let touchStartX = 0;
      let touchStartY = 0;
      let touchStartTime = 0;
      let lastTapTime = 0;
      let lastTapX = 0;
      let lastTapY = 0;
      let lastClickTime = 0;
      let isHorizontalSwipe = false;

      function isCardInteractiveBtn(target) {
        if (!target) return false;
        return Boolean(
          target.closest("button, .speak-btn, #front-speak-btn, .btn-audio-test, input, textarea, a, .duo-btn-3d")
        );
      }

      function stepCards(steps, direction) {
        if (direction === "next") {
          if (currentIndex >= cards.length - 1) {
            // Reached end bounce
            cardWrapper.style.transition = "transform 0.18s cubic-bezier(0.16, 1, 0.3, 1)";
            cardWrapper.style.transform = isFlipped ? "rotateY(180deg)" : "rotateY(0deg)";
            if (typeof playHapticTick === "function") playHapticTick(300, "sine", 0.03);
            return;
          }
          currentIndex = Math.min(cards.length - 1, currentIndex + steps);
        } else {
          if (currentIndex <= 0) {
            // Reached start bounce
            cardWrapper.style.transition = "transform 0.18s cubic-bezier(0.16, 1, 0.3, 1)";
            cardWrapper.style.transform = isFlipped ? "rotateY(180deg)" : "rotateY(0deg)";
            if (typeof playHapticTick === "function") playHapticTick(300, "sine", 0.03);
            return;
          }
          currentIndex = Math.max(0, currentIndex - steps);
        }

        isFlipped = false;
        cardWrapper.classList.remove("flipped");
        renderCurrentCard();

        cardWrapper.style.transition = "transform 0.16s cubic-bezier(0.16, 1, 0.3, 1)";
        cardWrapper.style.transform = "rotateY(0deg) translateX(0) rotateZ(0)";
        
        if (typeof playHapticTick === "function") {
          playHapticTick(460 + Math.min(180, steps * 40), "sine", 0.04);
        }
      }

      cardWrapper.addEventListener("touchstart", (e) => {
        cardAudio.unlock();
        const touch = e.touches[0];
        touchStartX = touch.clientX;
        touchStartY = touch.clientY;
        touchStartTime = performance.now();
        isHorizontalSwipe = false;
        cardWrapper.style.transition = "none";
      }, { passive: true });

      cardWrapper.addEventListener("touchmove", (e) => {
        const touch = e.touches[0];
        const diffX = touch.clientX - touchStartX;
        const diffY = touch.clientY - touchStartY;

        // Immediate responsive tracking when horizontal intent is established
        if (Math.abs(diffX) > Math.abs(diffY) * 1.15 && Math.abs(diffX) > 8) {
          isHorizontalSwipe = true;
          const rotateAngle = (diffX / 22).toFixed(2);
          const flipBase = isFlipped ? "rotateY(180deg)" : "rotateY(0deg)";
          // Direct 0.85x responsive tracking for smooth kinetic feel
          cardWrapper.style.transform = \`\${flipBase} translateX(\${diffX * 0.85}px) rotateZ(\${rotateAngle}deg)\`;
        }
      }, { passive: true });

      cardWrapper.addEventListener("touchend", (e) => {
        const touch = e.changedTouches[0];
        const diffX = touch.clientX - touchStartX;
        const diffY = touch.clientY - touchStartY;
        const dt = Math.max(1, performance.now() - touchStartTime);
        const velocityX = Math.abs(diffX) / dt; // px per millisecond
        const distance = Math.abs(diffX);

        cardWrapper.style.transition = "transform 0.16s cubic-bezier(0.16, 1, 0.3, 1)";

        if (isHorizontalSwipe && (distance > 24 || velocityX > 0.38)) {
          // Dynamic steps based on swipe force & speed
          let steps = 1;
          if (velocityX > 1.5 || distance > 240) {
            steps = 3; // Fast swipe / high force: moves 3 cards!
          } else if (velocityX > 0.8 || distance > 120) {
            steps = 2; // Medium force: moves 2 cards!
          } else {
            steps = 1; // Gentle drag: moves 1 card!
          }

          if (diffX < 0) {
            stepCards(steps, "next");
          } else {
            stepCards(steps, "prev");
          }
        } else if (Math.abs(diffX) < 24 && Math.abs(diffY) < 24) {
          // ROCK-SOLID DOUBLE TAP DETECTION (Touch)
          if (!isCardInteractiveBtn(e.target)) {
            const now = Date.now();
            const tapDist = Math.hypot(touch.clientX - lastTapX, touch.clientY - lastTapY);
            if (now - lastTapTime < 500 && tapDist < 65) {
              lastTapTime = 0;
              flipCard();
            } else {
              lastTapTime = now;
              lastTapX = touch.clientX;
              lastTapY = touch.clientY;
            }
          }
        } else {
          // Snap back if didn't reach threshold
          cardWrapper.style.transform = isFlipped ? "rotateY(180deg)" : "rotateY(0deg)";
        }
        isHorizontalSwipe = false;
      });

      // Desktop: Native double-click AND fast 2-click interval detection
      cardWrapper.addEventListener("dblclick", (e) => {
        if (isCardInteractiveBtn(e.target)) return;
        flipCard();
      });

      cardWrapper.addEventListener("click", (e) => {
        if (isCardInteractiveBtn(e.target)) return;
        const now = Date.now();
        if (now - lastClickTime < 450) {
          lastClickTime = 0;
          flipCard();
        } else {
          lastClickTime = now;
        }
      });

      // Delete Current Flashcard Function
      function deleteCurrentCard() {
        if (!cards || cards.length <= 1) {
          if (typeof showToast === "function") showToast("Cannot delete the last remaining card!");
          return;
        }
        const targetCard = cards[currentIndex];
        if (!targetCard) return;

        deletedCardNums.push(targetCard.originalNum);
        try {
          localStorage.setItem(DELETED_CARDS_STORAGE_KEY, JSON.stringify(deletedCardNums));
        } catch(e) {}

        reindexAndBuildCards();
        if (currentIndex >= cards.length) {
          currentIndex = cards.length - 1;
        }

        renderCurrentCard();
        updateSectionLearnedCounter();

        // Show undo toast
        const toast = document.getElementById("app-toast");
        if (toast) {
          toast.innerHTML = \`
            <div style="display: flex; align-items: center; justify-content: space-between; gap: 14px; width: 100%;">
              <span>Deleted card <strong>#\${targetCard.displayNum || targetCard.num}</strong> (\${targetCard.word}) · Order updated</span>
              <button type="button" id="btn-undo-delete-card" class="duo-btn-3d" style="padding: 4px 12px; background: rgba(56, 189, 248, 0.25); border: 1px solid rgba(56, 189, 248, 0.5); color: #38bdf8; border-radius: 8px; font-weight: 800; font-size: 0.8rem; cursor: pointer;">
                UNDO
              </button>
            </div>
          \`;
          toast.classList.add("show");

          const undoBtn = document.getElementById("btn-undo-delete-card");
          if (undoBtn) {
            undoBtn.onclick = () => {
              deletedCardNums = deletedCardNums.filter(n => n !== targetCard.originalNum);
              try {
                localStorage.setItem(DELETED_CARDS_STORAGE_KEY, JSON.stringify(deletedCardNums));
              } catch(e) {}
              reindexAndBuildCards();
              const restoredIdx = cards.findIndex(c => c.originalNum === targetCard.originalNum);
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

      // Wire up Delete Button
      const btnDeleteCard = document.getElementById("btn-delete-card");
      if (btnDeleteCard) {
        btnDeleteCard.addEventListener("click", (e) => {
          e.stopPropagation();
          deleteCurrentCard();
        });
      }

      `;

  html = html.slice(0, touchStartIdx) + newTouchCode + html.slice(touchEndIdx);
  console.log('Successfully replaced touch, swipe and double-tap handlers!');
}

fs.writeFileSync('index.html', html, 'utf8');
console.log('Wrote updated index.html! New length:', html.length);
