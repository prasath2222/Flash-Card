const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

// 1. Update CSS: Add cue-bounce animation and enhance trans-tile voice presentation
const cueBounceCss = `
      @keyframes cueBounce {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.16); background: rgba(56, 189, 248, 0.28); color: #38bdf8; border-color: rgba(56, 189, 248, 0.5); }
      }
      .card-tap-cue.cue-bounce {
        animation: cueBounce 0.45s cubic-bezier(0.34, 1.3, 0.64, 1);
      }
`;

if (!html.includes('cueBounce')) {
  html = html.replace('.card-tap-cue {', cueBounceCss + '\n      .card-tap-cue {');
}

// 2. Update Tap Cue labels to explicitly say "Double-tap to flip"
html = html.replace(
  `<span class="card-tap-cue">Tap to flip ↺</span>`,
  `<span class="card-tap-cue" id="card-cue-front">Double-tap to flip ↺</span>`
);
html = html.replace(
  `<span class="card-tap-cue">Tap to flip ↩</span>`,
  `<span class="card-tap-cue" id="card-cue-back">Double-tap to flip ↩</span>`
);

// If already named without id, ensure id is set
html = html.replace(/<span class="card-tap-cue"[^>]*>Double-tap to flip ↺<\/span>/g, `<span class="card-tap-cue" id="card-cue-front">Double-tap to flip ↺</span>`);
html = html.replace(/<span class="card-tap-cue"[^>]*>Double-tap to flip ↩<\/span>/g, `<span class="card-tap-cue" id="card-cue-back">Double-tap to flip ↩</span>`);

// 3. Update CardAudioEngine for much higher volume (punchy, clear, tactile)
const oldAudioEnginePart = `            // Layer 1: Air Displacement / Card Whoosh
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
            gain.gain.exponentialRampToValueAtTime(0.0001, t + 0.04);`;

const newAudioEnginePart = `            // Layer 1: Air Displacement / Card Whoosh (High-Volume Rich Sound)
            const whooshOsc = this.ctx.createOscillator();
            const whooshGain = this.ctx.createGain();
            whooshOsc.type = "sine";
            const startFreq = isFlippingBack ? 460 : 640;
            const endFreq = isFlippingBack ? 190 : 280;
            whooshOsc.frequency.setValueAtTime(startFreq, t);
            whooshOsc.frequency.exponentialRampToValueAtTime(endFreq, t + 0.16);

            whooshGain.gain.setValueAtTime(0.50, t);
            whooshGain.gain.exponentialRampToValueAtTime(0.001, t + 0.17);

            whooshOsc.connect(whooshGain);
            whooshGain.connect(this.ctx.destination);
            whooshOsc.start(t);
            whooshOsc.stop(t + 0.18);

            // Layer 2: Tactile Card Snap / Surface Release Transient (Crisp High-Gain Snap)
            const snapOsc = this.ctx.createOscillator();
            const snapGain = this.ctx.createGain();
            snapOsc.type = "triangle";
            snapOsc.frequency.setValueAtTime(isFlippingBack ? 820 : 1100, t + 0.01);
            snapOsc.frequency.exponentialRampToValueAtTime(260, t + 0.08);

            snapGain.gain.setValueAtTime(0.58, t + 0.01);
            snapGain.gain.exponentialRampToValueAtTime(0.001, t + 0.085);

            snapOsc.connect(snapGain);
            snapGain.connect(this.ctx.destination);
            snapOsc.start(t + 0.01);
            snapOsc.stop(t + 0.09);

            // Layer 3: Physical Haptic Motor Impulse on Mobile
            if (typeof navigator !== "undefined" && navigator.vibrate) {
              navigator.vibrate(22);
            }
          } catch (e) {}
        }

        // UI Tap Micro-Click (Loud and clear tactile click)
        playTapClick() {
          if (!this.enabled) return;
          this.unlock();
          if (!this.ctx) return;

          try {
            const t = this.ctx.currentTime;
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();
            osc.type = "sine";
            osc.frequency.setValueAtTime(680, t);
            osc.frequency.exponentialRampToValueAtTime(340, t + 0.04);

            gain.gain.setValueAtTime(0.38, t);
            gain.gain.exponentialRampToValueAtTime(0.001, t + 0.045);`;

html = html.replace(oldAudioEnginePart, newAudioEnginePart);

// 4. Update playNativeSpeech and speakWebSpeechStrict to enforce full volume (volume = 1.0)
html = html.replace(
  `        const audio = new Audio();
        audio.src = ttsUrl;
        // Strictly set to slow (0.84x), crystal-clear speed for effortless memorization
        audio.playbackRate = 0.84;
        currentActiveAudio = audio;`,
  `        const audio = new Audio();
        audio.src = ttsUrl;
        // Maximum volume and clear, natural pace
        audio.volume = 1.0;
        audio.playbackRate = 0.84;
        currentActiveAudio = audio;`
);

html = html.replace(
  `        const utterance = new SpeechSynthesisUtterance(text);
        const code = langCode.startsWith("es") ? "es-ES" : langCode.startsWith("hi") ? "hi-IN" : "en-US";
        utterance.lang = code;
        utterance.rate = 0.74;
        utterance.pitch = 1.0;`,
  `        const utterance = new SpeechSynthesisUtterance(text);
        const code = langCode.startsWith("es") ? "es-ES" : langCode.startsWith("hi") ? "hi-IN" : "en-US";
        utterance.lang = code;
        utterance.volume = 1.0;
        utterance.rate = 0.76;
        utterance.pitch = 1.0;`
);

// 5. Update Milestone Chime Volume
html = html.replace(
  `gain.gain.setValueAtTime(0.045, audioCtx.currentTime + i * 0.09);`,
  `gain.gain.setValueAtTime(0.38, audioCtx.currentTime + i * 0.09);`
);

// 6. Rewrite the Gesture & Touch Event Listeners so:
//    - Touching Spanish or Hindi translation speaks voice and NEVER flips
//    - Double-tap flips the card
//    - Single-tap does NOT flip the card
const oldEngineBlock = `      // Bulletproof Single Tap & Double Tap Flipping Engine
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
      });

      // Front English Pronunciation Handler (Native Audio)
      frontSpeakBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        const card = cards[currentIndex];
        playNativeSpeech(card.word, "en", frontSpeakBtn, "speaking-en");
      });

      // Tap Spanish Tile: Speaks in authentic native Spanish accent slowly and clearly
      cardEsTile.addEventListener("click", (e) => {
        e.stopPropagation();
        const card = cards[currentIndex];
        const esWord = card.trans.es.split('/')[0].trim();
        playNativeSpeech(esWord, "es", cardEsTile, "speaking-es");
      });

      // Tap Hindi Tile: Speaks in authentic native Indian Hindi accent slowly and clearly
      cardHiTile.addEventListener("click", (e) => {
        e.stopPropagation();
        const card = cards[currentIndex];
        let hiText = card.trans.hi.split('/')[0].trim();
        // If not custom edited, use rich native Devanagari dictionary text for optimal Hindi pronunciation
        if (!card.isCustomEdited && hindiDevMap && hindiDevMap[card.num]) {
          hiText = hindiDevMap[card.num];
        }
        playNativeSpeech(hiText, "hi", cardHiTile, "speaking-hi");
      });`;

const newEngineBlock = `      // Production-Grade Double-Tap & Action Element Engine
      let lastTouchEndTime = 0;
      let lastCardTapTime = 0;
      let cardTapTimeout = null;

      // Checks if target is an explicit action element (translations, audio speakers, buttons)
      // Elements that match this will NEVER flip the card
      function isActionElement(target) {
        if (!target) return false;
        return Boolean(target.closest("button, input, textarea, .icon-tool-btn, .speak-btn, #card-es-tile, #card-hi-tile, .trans-tile, .tile-top-bar, .shortcut-quick-edit-btn, .modal-backdrop, .modal-sheet"));
      }

      // Dedicated double-tap card flip handler:
      // - Single tap: plays tactile touch tick and pulses the "Double-tap to flip" cue (NO FLIP)
      // - Double tap (within 380ms): FLIPS THE CARD with full high-volume physical audio!
      function handleCardFaceDoubleTap(e) {
        const now = Date.now();
        const timeSinceLast = now - lastCardTapTime;

        if (timeSinceLast > 0 && timeSinceLast < 380) {
          // Double-tap confirmed!
          lastCardTapTime = 0;
          clearTimeout(cardTapTimeout);
          flipCard();
          return;
        }

        // Single tap: give responsive feedback without flipping
        lastCardTapTime = now;
        cardAudio.playTapClick();

        // Visual hint pulse on the cue badge
        const activeCue = isFlipped ? document.getElementById("card-cue-back") : document.getElementById("card-cue-front");
        if (activeCue) {
          activeCue.classList.add("cue-bounce");
          setTimeout(() => activeCue.classList.remove("cue-bounce"), 480);
        }

        clearTimeout(cardTapTimeout);
        cardTapTimeout = setTimeout(() => {
          lastCardTapTime = 0;
        }, 390);
      }

      // Gesture & Touch Event Listeners on Card Wrapper
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
          // If user touched Spanish, Hindi, or any action button, DO NOT FLIP!
          if (isActionElement(e.target)) return;

          // Prevent synthetic duplicate click on touch devices
          if (e.cancelable) e.preventDefault();
          handleCardFaceDoubleTap(e);
        }
      });

      // Front Face Shortcut Glance Button
      if (frontShortcutBtn) {
        frontShortcutBtn.addEventListener("click", (e) => {
          e.stopPropagation();
          flipCard();
        });
      }

      // Desktop Click Listener
      cardWrapper.addEventListener("click", (e) => {
        // Prevent duplicate firing from mobile synthetic click
        if (Date.now() - lastTouchEndTime < 450) {
          return;
        }
        if (isActionElement(e.target)) return;
        if (Math.abs(currentDeltaX) < 10) {
          handleCardFaceDoubleTap(e);
        }
      });

      // Explicit Double-Click on desktop
      cardWrapper.addEventListener("dblclick", (e) => {
        if (isActionElement(e.target)) return;
        flipCard();
      });

      // Front English Pronunciation Handler (Loud & Clear)
      frontSpeakBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        cardAudio.playTapClick();
        const card = cards[currentIndex];
        playNativeSpeech(card.word, "en", frontSpeakBtn, "speaking-en");
      });

      // Spanish Voice Handler: Speaks in authentic native Spanish accent at FULL volume, NEVER flips
      function handleSpanishSpeech(e) {
        if (e) {
          e.stopPropagation();
          if (e.cancelable && e.type === "touchend") e.preventDefault();
        }
        cardAudio.playTapClick();
        const card = cards[currentIndex];
        const esWord = card.trans.es.split('/')[0].trim();
        playNativeSpeech(esWord, "es", cardEsTile, "speaking-es");
      }

      cardEsTile.addEventListener("click", handleSpanishSpeech);
      cardEsTile.addEventListener("touchend", handleSpanishSpeech);

      // Hindi Voice Handler: Speaks in authentic native Indian Hindi accent at FULL volume, NEVER flips
      function handleHindiSpeech(e) {
        if (e) {
          e.stopPropagation();
          if (e.cancelable && e.type === "touchend") e.preventDefault();
        }
        cardAudio.playTapClick();
        const card = cards[currentIndex];
        let hiText = card.trans.hi.split('/')[0].trim();
        if (!card.isCustomEdited && hindiDevMap && hindiDevMap[card.num]) {
          hiText = hindiDevMap[card.num];
        }
        playNativeSpeech(hiText, "hi", cardHiTile, "speaking-hi");
      }

      cardHiTile.addEventListener("click", handleHindiSpeech);
      cardHiTile.addEventListener("touchend", handleHindiSpeech);`;

html = html.replace(oldEngineBlock, newEngineBlock);

fs.writeFileSync('index.html', html);
console.log('Successfully updated Spanish/Hindi voice exclusivity, double-tap flip, and high volume!');
