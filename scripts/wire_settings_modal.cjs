const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

const targetPos = html.indexOf('const btnDownloadHtmlMenu = document.getElementById("btn-download-html-menu");');

if (targetPos === -1) {
  console.error('Target marker not found!');
  process.exit(1);
}

const jsToAdd = `// ==========================================================
      // SETTINGS MODAL INTERACTIVE TABS & ACTION HANDLERS
      // ==========================================================
      const settingsTabBtns = document.querySelectorAll("[data-tab-target]");
      settingsTabBtns.forEach(btn => {
        btn.addEventListener("click", () => {
          settingsTabBtns.forEach(b => b.classList.remove("active"));
          btn.classList.add("active");
          const targetId = btn.getAttribute("data-tab-target");
          document.querySelectorAll(".settings-tab-panel").forEach(p => p.classList.remove("active"));
          const panel = document.getElementById(targetId);
          if (panel) panel.classList.add("active");
          if (typeof playHapticTick === "function") playHapticTick(520, "sine", 0.03);
        });
      });

      // Quick Speech Speed Preset Buttons
      const btnRateSlow = document.getElementById("btn-rate-slow");
      const btnRateNormal = document.getElementById("btn-rate-normal");
      const btnRateFast = document.getElementById("btn-rate-fast");
      const sliderVoiceRateEl = document.getElementById("slider-voice-rate");

      function setSpeechRatePreset(rateVal, activeBtn) {
        if (!sliderVoiceRateEl) return;
        sliderVoiceRateEl.value = rateVal;
        sliderVoiceRateEl.dispatchEvent(new Event("input"));
        [btnRateSlow, btnRateNormal, btnRateFast].forEach(b => {
          if (b) b.classList.remove("active");
        });
        if (activeBtn) activeBtn.classList.add("active");
        if (typeof playHapticTick === "function") playHapticTick(480, "sine", 0.03);
      }

      if (btnRateSlow) {
        btnRateSlow.addEventListener("click", () => setSpeechRatePreset(75, btnRateSlow));
      }
      if (btnRateNormal) {
        btnRateNormal.addEventListener("click", () => setSpeechRatePreset(100, btnRateNormal));
      }
      if (btnRateFast) {
        btnRateFast.addEventListener("click", () => setSpeechRatePreset(125, btnRateFast));
      }

      // Settings Modal: Reset Deck & Restore All 200 Cards
      const btnSettingsResetDeck = document.getElementById("btn-settings-reset-deck");
      if (btnSettingsResetDeck) {
        btnSettingsResetDeck.addEventListener("click", () => {
          resetFlashcardDeck();
          closeMenuDrawer();
        });
      }

      // Settings Modal: Reset Learned Cards Progress
      const btnSettingsResetLearned = document.getElementById("btn-settings-reset-learned");
      if (btnSettingsResetLearned) {
        btnSettingsResetLearned.addEventListener("click", () => {
          if (learnedCardsSet && typeof learnedCardsSet.clear === "function") {
            learnedCardsSet.clear();
          } else {
            learnedCardsSet = new Set();
          }
          saveLearnedCards();
          updateSectionLearnedCounter();
          renderCurrentCard();
          if (typeof playHapticTick === "function") playHapticTick(350, "sine", 0.06);
          if (typeof showToast === "function") showToast("Learned cards progress reset to 0 / 200");
          closeMenuDrawer();
        });
      }

      `;

html = html.slice(0, targetPos) + jsToAdd + html.slice(targetPos);

fs.writeFileSync('index.html', html, 'utf8');
console.log('Wired settings modal interactive handlers successfully.');
