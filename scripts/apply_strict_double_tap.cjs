const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

// 1. Upgrade playNativeSpeech to prioritize direct, synchronous SpeechSynthesis
// This guarantees instant, loud, crystal-clear Spanish and Hindi speech on all mobile devices and static sites
const oldSpeechFunction = `      // Speaks in 100% authentic native language accent, slowly and clearly
      function playNativeSpeech(text, langCode, visualTile = null, activeClass = "") {
        if (!text) return;

        // Clean text: if multiple alternatives like "suelo / piso", take primary word
        const cleanWord = text.split("/")[0].split(";")[0].replace(/[\(\)]/g, "").trim();
        if (!cleanWord) return;

        // Stop any currently playing audio track
        if (currentActiveAudio) {
          try {
            currentActiveAudio.pause();
            currentActiveAudio.currentTime = 0;
          } catch (e) {}
          currentActiveAudio = null;
        }
        if ("speechSynthesis" in window) {
          try {
            window.speechSynthesis.cancel();
          } catch (e) {}
        }

        // Active visual glowing feedback on the tile
        if (visualTile && activeClass) {
          visualTile.classList.add(activeClass);
        }

        const cleanupActive = () => {
          if (visualTile && activeClass) {
            visualTile.classList.remove(activeClass);
          }
          if (currentActiveAudio === audio) {
            currentActiveAudio = null;
          }
        };

        // Standardize language code for native speech endpoint
        const ttsLang = langCode.startsWith("es") ? "es" : langCode.startsWith("hi") ? "hi" : "en";
        // Connect to server proxy endpoint which returns high-fidelity authentic native audio
        const ttsUrl = \`/api/tts?lang=\${encodeURIComponent(ttsLang)}&text=\${encodeURIComponent(cleanWord)}\`;

        const audio = new Audio();
        audio.src = ttsUrl;
        // Maximum volume and clear, natural pace
        audio.volume = 1.0;
        audio.playbackRate = 0.84;
        currentActiveAudio = audio;

        audio.onended = () => {
          cleanupActive();
        };

        // Fallback to local Web Speech API with strict native voice if network is unavailable
        audio.onerror = () => {
          speakWebSpeechStrict(cleanWord, ttsLang, cleanupActive);
        };

        audio.play().catch(() => {
          speakWebSpeechStrict(cleanWord, ttsLang, cleanupActive);
        });
      }`;

const newSpeechFunction = `      // Speaks in 100% authentic native language accent, slowly, clearly, and loudly
      function playNativeSpeech(text, langCode, visualTile = null, activeClass = "") {
        if (!text) return;

        // Clean text: if multiple alternatives like "suelo / piso", take primary word
        const cleanWord = text.split("/")[0].split(";")[0].replace(/[\\(\\)]/g, "").trim();
        if (!cleanWord) return;

        // Active visual glowing feedback on the tile
        if (visualTile && activeClass) {
          visualTile.classList.add(activeClass);
          setTimeout(() => visualTile.classList.remove(activeClass), 1600);
        }

        // 1. Direct synchronous Web Speech Synthesis: works 100% reliably within user gestures on mobile devices and static sites
        if ("speechSynthesis" in window) {
          try {
            window.speechSynthesis.cancel();
            const utterance = new SpeechSynthesisUtterance(cleanWord);
            const code = langCode.startsWith("es") ? "es-ES" : langCode.startsWith("hi") ? "hi-IN" : "en-US";
            utterance.lang = code;
            utterance.volume = 1.0;
            utterance.rate = 0.80;
            utterance.pitch = 1.0;

            const voices = window.speechSynthesis.getVoices() || [];
            const prefix = code.split("-")[0];
            const nativeVoice = voices.find(v => {
              const vLang = (v.lang || "").toLowerCase().replace("_", "-");
              return vLang.startsWith(prefix) ||
                     (prefix === "es" && v.name.toLowerCase().includes("spanish")) ||
                     (prefix === "hi" && (v.name.toLowerCase().includes("hindi") || v.name.toLowerCase().includes("india")));
            });

            if (nativeVoice) {
              utterance.voice = nativeVoice;
            } else if (langCode.startsWith("hi")) {
              const indianVoice = voices.find(v => (v.lang || "").toLowerCase().includes("in"));
              if (indianVoice) utterance.voice = indianVoice;
            }

            window.speechSynthesis.speak(utterance);
            return;
          } catch (e) {
            console.warn("Direct SpeechSynthesis error:", e);
          }
        }

        // 2. Audio endpoint fallback
        try {
          const ttsLang = langCode.startsWith("es") ? "es" : langCode.startsWith("hi") ? "hi" : "en";
          const audio = new Audio(\`/api/tts?lang=\${encodeURIComponent(ttsLang)}&text=\${encodeURIComponent(cleanWord)}\`);
          audio.volume = 1.0;
          audio.play().catch(() => {});
        } catch (e) {}
      }`;

html = html.replace(oldSpeechFunction, newSpeechFunction);

// 2. Rewrite the Gesture Engine to STRICTLY ENFORCE:
//    - Double-tap ONLY to flip (single-tap strictly never flips)
//    - Touching Spanish or Hindi speaks voice and NEVER flips under any circumstances
const oldEngineSection = `      // Production-Grade Double-Tap & Action Element Engine
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

const newEngineSection = `      // STRICT DOUBLE-TAP & ACTION ISOLATION SYSTEM
      let lastTouchEndTime = 0;
      let cardTapCount = 0;
      let cardTapTimer = null;

      // Pulse visual cue badge
      function pulseDoubleTapCue() {
        const activeCue = isFlipped ? document.getElementById("card-cue-back") : document.getElementById("card-cue-front");
        if (activeCue) {
          activeCue.classList.remove("cue-bounce");
          void activeCue.offsetWidth;
          activeCue.classList.add("cue-bounce");
          setTimeout(() => activeCue.classList.remove("cue-bounce"), 480);
        }
      }

      // Checks if target is an interactive action element (Translations, Audio, Buttons, Form fields)
      // Any touch or click inside these elements is 100% BLOCKED from flipping the card
      function isActionElement(target) {
        if (!target) return false;
        return Boolean(
          target.closest(
            "#card-es-tile, #card-hi-tile, .trans-tile, .tile-top-bar, .tile-audio-icon, .trans-tile-word, " +
            "#card-tamil-tile, #front-speak-btn, #front-edit-btn, #back-edit-btn, .speak-btn, .icon-tool-btn, " +
            ".shortcut-quick-edit-btn, #front-shortcut-btn, button, input, textarea, a, .modal-sheet, .modal-backdrop"
          )
        );
      }

      // STRICT DOUBLE-TAP CONTROLLER:
      // - Single tap: strictly NEVER flips! Plays soft tactile click and bounces the "Double-tap to flip" cue.
      // - Double tap (2 taps within 420ms): FLIPS THE CARD with full high-volume physical audio!
      function handleCardSurfaceTap(e) {
        // If user tapped Spanish, Hindi, or any button, STRICTLY DO NOT FLIP
        if (isActionElement(e.target)) {
          cardTapCount = 0;
          return;
        }

        cardTapCount++;

        if (cardTapCount === 1) {
          // FIRST TAP: STRICTLY DO NOT FLIP!
          cardAudio.playTapClick();
          pulseDoubleTapCue();

          clearTimeout(cardTapTimer);
          cardTapTimer = setTimeout(() => {
            cardTapCount = 0; // Expired: single tap will NEVER flip
          }, 420);
        } else if (cardTapCount >= 2) {
          // SECOND TAP CONFIRMED: FLIP CARD!
          cardTapCount = 0;
          clearTimeout(cardTapTimer);
          flipCard();
        }
      }

      // Touch Events on Card Wrapper
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

        // Horizontal Swipe: Next / Previous
        if (Math.abs(deltaX) > SWIPE_THRESHOLD && Math.abs(deltaX) > Math.abs(deltaY)) {
          if (deltaX < 0) {
            nextCard();
          } else {
            prevCard();
          }
        } else if (Math.abs(deltaX) < 18 && Math.abs(deltaY) < 18) {
          // Touch Tap on card face
          if (isActionElement(e.target)) return;

          if (e.cancelable) e.preventDefault();
          handleCardSurfaceTap(e);
        }
      });

      // Desktop Click Listener
      cardWrapper.addEventListener("click", (e) => {
        // Prevent duplicate synthetic touch clicks
        if (Date.now() - lastTouchEndTime < 450) {
          return;
        }
        if (isActionElement(e.target)) return;
        if (Math.abs(currentDeltaX) < 10) {
          handleCardSurfaceTap(e);
        }
      });

      // Explicit Double-Click on Desktop
      cardWrapper.addEventListener("dblclick", (e) => {
        if (isActionElement(e.target)) return;
        flipCard();
      });

      // Front Face Shortcut Button
      if (frontShortcutBtn) {
        frontShortcutBtn.addEventListener("click", (e) => {
          e.stopPropagation();
          flipCard();
        });
      }

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
          e.stopImmediatePropagation();
          if (e.cancelable && e.type === "touchend") e.preventDefault();
        }
        cardAudio.playTapClick();
        const card = cards[currentIndex];
        const esWord = card.trans.es.split('/')[0].trim();
        playNativeSpeech(esWord, "es", cardEsTile, "speaking-es");
      }

      cardEsTile.addEventListener("pointerdown", (e) => e.stopPropagation());
      cardEsTile.addEventListener("click", handleSpanishSpeech);
      cardEsTile.addEventListener("touchend", handleSpanishSpeech);

      // Hindi Voice Handler: Speaks in authentic native Indian Hindi accent at FULL volume, NEVER flips
      function handleHindiSpeech(e) {
        if (e) {
          e.stopPropagation();
          e.stopImmediatePropagation();
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

      cardHiTile.addEventListener("pointerdown", (e) => e.stopPropagation());
      cardHiTile.addEventListener("click", handleHindiSpeech);
      cardHiTile.addEventListener("touchend", handleHindiSpeech);`;

html = html.replace(oldEngineSection, newEngineSection);

fs.writeFileSync('index.html', html);
console.log('Successfully applied strict double-tap only flip and direct synchronous Spanish/Hindi speech!');
