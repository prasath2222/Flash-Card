const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

// 1. Upgrade CSS for 3D card physics, z-index, and tactile modern look
const oldCardPhysicsCss = `      .flashcard-wrapper {
        width: 100%;
        height: 100%;
        max-height: 600px;
        position: relative;
        transform-style: preserve-3d;
        cursor: pointer;
        transition: transform 0.55s cubic-bezier(0.34, 1.25, 0.64, 1);
        will-change: transform;
      }

      .flashcard-wrapper.flipped {
        transform: rotateY(180deg);
      }

      /* Card Faces */
      .card-face {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        border-radius: 28px;
        background: linear-gradient(180deg, #131c31 0%, #0d1527 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 20px 48px -12px rgba(0, 0, 0, 0.75),
          0 0 0 1px rgba(255, 255, 255, 0.04);
        backface-visibility: hidden;
        -webkit-backface-visibility: hidden;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 22px 20px 18px;
        overflow: hidden;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
      }

      .flashcard-wrapper:active .card-face {
        border-color: var(--card-border-glow);
      }

      .card-face-front {
        transform: rotateY(0deg);
      }

      .card-face-back {
        transform: rotateY(180deg);
        background: linear-gradient(180deg, #131c31 0%, #0d1527 100%);
      }`;

const newCardPhysicsCss = `      .flashcard-wrapper {
        width: 100%;
        height: 100%;
        max-height: 600px;
        position: relative;
        transform-style: preserve-3d;
        -webkit-transform-style: preserve-3d;
        cursor: pointer;
        transition: transform 0.58s cubic-bezier(0.34, 1.28, 0.64, 1);
        will-change: transform;
        user-select: none;
        -webkit-user-select: none;
      }

      .flashcard-wrapper.flipped {
        transform: rotateY(180deg);
        -webkit-transform: rotateY(180deg);
      }

      /* Production-grade card face physics & glassmorphism */
      .card-face {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        border-radius: 28px;
        background: linear-gradient(180deg, #131d34 0%, #0b1324 100%);
        border: 1px solid rgba(255, 255, 255, 0.09);
        box-shadow: 0 24px 60px -12px rgba(0, 0, 0, 0.82),
          0 0 0 1px rgba(255, 255, 255, 0.06),
          inset 0 1px 0 rgba(255, 255, 255, 0.12);
        backface-visibility: hidden;
        -webkit-backface-visibility: hidden;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 22px 20px 18px;
        overflow: hidden;
        transition: border-color 0.25s ease, box-shadow 0.25s ease;
      }

      .flashcard-wrapper:active .card-face {
        border-color: rgba(56, 189, 248, 0.5);
        box-shadow: 0 24px 60px -12px rgba(0, 0, 0, 0.82),
          0 0 20px rgba(56, 189, 248, 0.2);
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
        background: linear-gradient(180deg, #131d34 0%, #0a1120 100%);
      }

      .flashcard-wrapper.flipped .card-face-front {
        z-index: 1;
        pointer-events: none;
      }

      .flashcard-wrapper.flipped .card-face-back {
        z-index: 2;
        pointer-events: auto;
      }

      /* Subtle Tap Cue Indicator */
      .card-tap-cue {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        font-size: 0.68rem;
        font-weight: 600;
        color: #94a3b8;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 9999px;
        padding: 3px 9px;
        pointer-events: none;
        transition: all 0.2s ease;
      }

      .flashcard-wrapper:hover .card-tap-cue {
        color: var(--accent-cyan);
        background: rgba(56, 189, 248, 0.1);
        border-color: rgba(56, 189, 248, 0.25);
      }`;

html = html.replace(oldCardPhysicsCss, newCardPhysicsCss);

// 2. Add Tap Cue to card header bars in HTML
html = html.replace(
  `<span class="card-category-tag" id="front-card-cat">Kitchen & Cooking</span>`,
  `<span class="card-category-tag" id="front-card-cat">Kitchen & Cooking</span>
              <span class="card-tap-cue">Tap to flip ↺</span>`
);

html = html.replace(
  `<span
                class="card-category-tag"
                id="back-card-word-preview"
                style="color: var(--accent-cyan); background: rgba(56, 189, 248, 0.12); border-color: rgba(56, 189, 248, 0.28);"
                >STOVE</span
              >`,
  `<span
                class="card-category-tag"
                id="back-card-word-preview"
                style="color: var(--accent-cyan); background: rgba(56, 189, 248, 0.12); border-color: rgba(56, 189, 248, 0.28);"
                >STOVE</span
              >
              <span class="card-tap-cue">Tap to flip ↩</span>`
);

// 3. Replace the Sound Engine with High-Fidelity Tactile Physical Sound Engine
const newSoundEngine = `
      // Production-Grade Web Audio Synthesizer (Realistic Physical Card & Haptic Sounds)
      class CardAudioEngine {
        constructor() {
          this.ctx = null;
          this.enabled = true;
          this.unlocked = false;
        }

        unlock() {
          if (!this.unlocked) {
            try {
              const AudioCtx = window.AudioContext || window.webkitAudioContext;
              if (AudioCtx) {
                this.ctx = new AudioCtx();
                if (this.ctx.state === "suspended") {
                  this.ctx.resume();
                }
              }
              this.unlocked = true;
            } catch (e) {}
          } else if (this.ctx && this.ctx.state === "suspended") {
            this.ctx.resume();
          }
        }

        // Realistic tactile playing-card flip sound (Crisp air whoosh + tactile snap transient)
        playCardFlip(isFlippingBack = false) {
          if (!this.enabled) return;
          this.unlock();
          if (!this.ctx) return;

          try {
            const t = this.ctx.currentTime;

            // Layer 1: Air Displacement / Card Whoosh
            const whooshOsc = this.ctx.createOscillator();
            const whooshGain = this.ctx.createGain();
            whooshOsc.type = "sine";
            const startFreq = isFlippingBack ? 420 : 580;
            const endFreq = isFlippingBack ? 180 : 260;
            whooshOsc.frequency.setValueAtTime(startFreq, t);
            whooshOsc.frequency.exponentialRampToValueAtTime(endFreq, t + 0.14);

            whooshGain.gain.setValueAtTime(0.09, t);
            whooshGain.gain.exponentialRampToValueAtTime(0.0001, t + 0.15);

            whooshOsc.connect(whooshGain);
            whooshGain.connect(this.ctx.destination);
            whooshOsc.start(t);
            whooshOsc.stop(t + 0.16);

            // Layer 2: Tactile Card Snap / Surface Release Transient
            const snapOsc = this.ctx.createOscillator();
            const snapGain = this.ctx.createGain();
            snapOsc.type = "triangle";
            snapOsc.frequency.setValueAtTime(isFlippingBack ? 760 : 1020, t + 0.015);
            snapOsc.frequency.exponentialRampToValueAtTime(280, t + 0.07);

            snapGain.gain.setValueAtTime(0.08, t + 0.015);
            snapGain.gain.exponentialRampToValueAtTime(0.0001, t + 0.075);

            snapOsc.connect(snapGain);
            snapGain.connect(this.ctx.destination);
            snapOsc.start(t + 0.015);
            snapOsc.stop(t + 0.08);

            // Layer 3: Physical Haptic Motor Impulse on Mobile
            if (typeof navigator !== "undefined" && navigator.vibrate) {
              navigator.vibrate(14);
            }
          } catch (e) {}
        }

        // UI Tap Micro-Click
        playTapClick() {
          if (!this.enabled) return;
          this.unlock();
          if (!this.ctx) return;

          try {
            const t = this.ctx.currentTime;
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();
            osc.type = "sine";
            osc.frequency.setValueAtTime(640, t);
            osc.frequency.exponentialRampToValueAtTime(320, t + 0.035);

            gain.gain.setValueAtTime(0.05, t);
            gain.gain.exponentialRampToValueAtTime(0.0001, t + 0.04);

            osc.connect(gain);
            gain.connect(this.ctx.destination);
            osc.start(t);
            osc.stop(t + 0.045);

            if (typeof navigator !== "undefined" && navigator.vibrate) {
              navigator.vibrate(8);
            }
          } catch (e) {}
        }
      }

      const cardAudio = new CardAudioEngine();

      // Global touch/pointer unlock
      window.addEventListener("pointerdown", () => cardAudio.unlock(), { once: true });
      window.addEventListener("touchstart", () => cardAudio.unlock(), { once: true });
      window.addEventListener("click", () => cardAudio.unlock(), { once: true });

      function playHapticTick(freq = 440, type = "sine", duration = 0.04) {
        cardAudio.playTapClick();
      }
`;

// Replace old playHapticTick
html = html.replace(
  `function playHapticTick(freq = 440, type = "sine", duration = 0.04) {
        try {
          const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
          const osc = audioCtx.createOscillator();
          const gain = audioCtx.createGain();
          osc.type = type;
          osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
          gain.gain.setValueAtTime(0.04, audioCtx.currentTime);
          gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + duration);
          osc.connect(gain);
          gain.connect(audioCtx.destination);
          osc.start();
          osc.stop(audioCtx.currentTime + duration);
        } catch (e) {
          // Fallback gracefully
        }
      }`,
  newSoundEngine
);

// 4. Update flipCard function to use cardAudio.playCardFlip
const oldFlipCard = `      function flipCard() {
        if (isAnimating) return;
        isFlipped = !isFlipped;
        if (isFlipped) {
          cardWrapper.classList.add("flipped");
          playHapticTick(560, "triangle", 0.05);
        } else {
          cardWrapper.classList.remove("flipped");
          playHapticTick(460, "triangle", 0.05);
        }
      }`;

const newFlipCard = `      function flipCard() {
        if (isAnimating) return;
        isFlipped = !isFlipped;
        cardAudio.playCardFlip(!isFlipped);
        if (isFlipped) {
          cardWrapper.classList.add("flipped");
        } else {
          cardWrapper.classList.remove("flipped");
        }
      }`;

html = html.replace(oldFlipCard, newFlipCard);

// 5. Replace Gesture & Touch Event Listeners with Bulletproof Single/Double Tap & Flip System
const oldGestureCode = `      // Gesture & Touch Event Listeners
      cardWrapper.addEventListener("touchstart", (e) => {
        if (isAnimating) return;
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

        // Tactile tilt resistance if horizontal swipe
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

        if (Math.abs(deltaX) > SWIPE_THRESHOLD && Math.abs(deltaX) > Math.abs(deltaY)) {
          if (deltaX < 0) {
            nextCard();
          } else {
            prevCard();
          }
        } else if (Math.abs(deltaX) < 12 && Math.abs(deltaY) < 12) {
          // Do not flip if user tapped Spanish, Hindi, shortcut section, edit triggers, or modals
          if (e.target.closest("#card-es-tile, #card-hi-tile, .shortcut-section, .speak-btn, .icon-tool-btn, .edit-card-pill-btn, .modal-backdrop, .modal-sheet")) {
            return;
          }
          flipCard();
        }
      });

      // Desktop Click to Flip
      if (frontShortcutBtn) {
        frontShortcutBtn.addEventListener("click", (e) => {
          e.stopPropagation();
          flipCard();
        });
      }

      cardWrapper.addEventListener("click", (e) => {
        if (e.target.closest("#card-es-tile, #card-hi-tile, .shortcut-section, .speak-btn, .icon-tool-btn, .edit-card-pill-btn, .modal-backdrop, .modal-sheet")) return;
        if (Math.abs(currentDeltaX) < 10) {
          flipCard();
        }
      });`;

const newGestureCode = `      // Bulletproof Single Tap & Double Tap Flipping Engine
      let lastTouchEndTime = 0;
      let lastTapTime = 0;

      // Checks if target is an explicit action element that should NOT flip the card
      function isActionElement(target) {
        if (!target) return false;
        return Boolean(target.closest("button, input, textarea, .icon-tool-btn, .speak-btn, .shortcut-quick-edit-btn, .modal-backdrop, .modal-sheet"));
      }

      function handleCardTapOrDoubleTap(e) {
        const now = Date.now();
        const timeSinceLast = now - lastTapTime;
        lastTapTime = now;

        // Both single tap and double tap seamlessly trigger the flip
        flipCard();
      }

      // Gesture & Touch Event Listeners
      cardWrapper.addEventListener("touchstart", (e) => {
        if (isAnimating) return;
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

        // Tactile tilt resistance if horizontal swipe
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
        lastTouchEndTime = Date.now();

        const touch = e.changedTouches[0];
        const deltaX = touch.clientX - touchStartX;
        const deltaY = touch.clientY - touchStartY;

        // Swipe Left or Right
        if (Math.abs(deltaX) > SWIPE_THRESHOLD && Math.abs(deltaX) > Math.abs(deltaY)) {
          if (deltaX < 0) {
            nextCard();
          } else {
            prevCard();
          }
        } else if (Math.abs(deltaX) < 18 && Math.abs(deltaY) < 18) {
          // Tap on card face
          if (isActionElement(e.target)) return;

          // Prevent synthetic duplicate click on touch devices
          if (e.cancelable) e.preventDefault();
          handleCardTapOrDoubleTap(e);
        }
      });

      // Desktop Click & Double-Click to Flip
      if (frontShortcutBtn) {
        frontShortcutBtn.addEventListener("click", (e) => {
          e.stopPropagation();
          flipCard();
        });
      }

      cardWrapper.addEventListener("click", (e) => {
        // Prevent duplicate firing from mobile synthetic click
        if (Date.now() - lastTouchEndTime < 450) {
          return;
        }
        if (isActionElement(e.target)) return;
        if (Math.abs(currentDeltaX) < 10) {
          handleCardTapOrDoubleTap(e);
        }
      });

      // Explicit Double-Click / Double-Tap listener on wrapper
      cardWrapper.addEventListener("dblclick", (e) => {
        if (isActionElement(e.target)) return;
        flipCard();
      });`;

html = html.replace(oldGestureCode, newGestureCode);

fs.writeFileSync('index.html', html);
console.log('Successfully applied bulletproof tap/double-tap flipping and realistic card audio!');
