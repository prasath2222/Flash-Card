const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

// 1. Add CSS styles for the new Audio & Music Studio inside the Settings Modal
const audioSettingsCss = `
      /* Professional Audio Studio & Music Controls */
      .settings-sheet {
        max-height: 88vh;
        overflow-y: auto;
      }

      .settings-audio-container {
        display: flex;
        flex-direction: column;
        gap: 12px;
      }

      .audio-card {
        background: rgba(255, 255, 255, 0.035);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 14px 16px;
        display: flex;
        flex-direction: column;
        gap: 12px;
        transition: border-color 0.2s ease;
      }

      .audio-card:hover {
        border-color: rgba(56, 189, 248, 0.25);
      }

      .audio-card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
      }

      .audio-card-title-group {
        display: flex;
        align-items: center;
        gap: 10px;
      }

      .audio-icon-badge {
        font-size: 1.25rem;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 36px;
        height: 36px;
        border-radius: 10px;
        background: rgba(56, 189, 248, 0.1);
        border: 1px solid rgba(56, 189, 248, 0.22);
        flex-shrink: 0;
      }

      .audio-section-title {
        font-size: 0.9rem;
        font-weight: 750;
        color: #f8fafc;
        line-height: 1.2;
      }

      .audio-section-sub {
        font-size: 0.72rem;
        color: #94a3b8;
        line-height: 1.3;
        margin-top: 2px;
      }

      .audio-sliders-grid {
        display: flex;
        flex-direction: column;
        gap: 10px;
      }

      .audio-slider-group {
        display: flex;
        flex-direction: column;
        gap: 5px;
      }

      .audio-slider-label {
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-size: 0.78rem;
        font-weight: 600;
        color: #cbd5e1;
      }

      .val-badge {
        font-family: monospace;
        font-size: 0.76rem;
        font-weight: 700;
        color: var(--accent-cyan);
        background: rgba(56, 189, 248, 0.12);
        padding: 2px 7px;
        border-radius: 6px;
        border: 1px solid rgba(56, 189, 248, 0.25);
      }

      .settings-slider {
        -webkit-appearance: none;
        appearance: none;
        width: 100%;
        height: 6px;
        border-radius: 9999px;
        background: rgba(255, 255, 255, 0.1);
        outline: none;
        transition: background 0.2s ease;
      }

      .settings-slider::-webkit-slider-thumb {
        -webkit-appearance: none;
        appearance: none;
        width: 18px;
        height: 18px;
        border-radius: 50%;
        background: #38bdf8;
        box-shadow: 0 0 10px rgba(56, 189, 248, 0.6);
        cursor: pointer;
        transition: transform 0.15s ease, background-color 0.15s ease;
      }

      .settings-slider::-webkit-slider-thumb:hover,
      .settings-slider::-webkit-slider-thumb:active {
        transform: scale(1.22);
        background: #7dd3fc;
      }

      .audio-mode-selector {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
        margin-top: 2px;
      }

      .audio-chip-btn {
        padding: 5px 12px;
        border-radius: 9999px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #94a3b8;
        font-size: 0.74rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.18s ease;
      }

      .audio-chip-btn:hover {
        background: rgba(255, 255, 255, 0.1);
        color: #f1f5f9;
      }

      .audio-chip-btn.active {
        background: rgba(56, 189, 248, 0.18);
        border-color: rgba(56, 189, 248, 0.5);
        color: #38bdf8;
        box-shadow: 0 0 10px rgba(56, 189, 248, 0.25);
      }

      .btn-audio-test {
        padding: 5px 12px;
        border-radius: 9999px;
        background: rgba(56, 189, 248, 0.12);
        border: 1px solid rgba(56, 189, 248, 0.35);
        color: var(--accent-cyan);
        font-size: 0.74rem;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.18s ease;
      }

      .btn-audio-test:hover,
      .btn-audio-test:active {
        background: rgba(56, 189, 248, 0.28);
        transform: scale(0.96);
      }

      /* Clean Toggle Switch */
      .toggle-switch {
        position: relative;
        display: inline-block;
        width: 44px;
        height: 24px;
        flex-shrink: 0;
      }

      .toggle-switch input {
        opacity: 0;
        width: 0;
        height: 0;
      }

      .toggle-slider {
        position: absolute;
        cursor: pointer;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(255, 255, 255, 0.15);
        transition: .3s cubic-bezier(0.4, 0, 0.2, 1);
        border-radius: 9999px;
        border: 1px solid rgba(255, 255, 255, 0.15);
      }

      .toggle-slider:before {
        position: absolute;
        content: "";
        height: 18px;
        width: 18px;
        left: 2px;
        bottom: 2px;
        background-color: white;
        transition: .3s cubic-bezier(0.4, 0, 0.2, 1);
        border-radius: 50%;
      }

      input:checked + .toggle-slider {
        background-color: #0284c7;
        border-color: #38bdf8;
      }

      input:checked + .toggle-slider:before {
        transform: translateX(20px);
        background-color: #f0f9ff;
      }
`;

if (!html.includes('.settings-audio-container {')) {
  html = html.replace('.settings-sheet {', audioSettingsCss + '\n      .settings-sheet {');
}

// 2. Insert the Audio Controls into the Settings Modal HTML body
const oldSettingsModalContent = `        <div class="settings-content-body">
          <!-- Download Offline HTML Card -->
          <div class="settings-action-card">`;

const newAudioModalMarkup = `        <div class="settings-content-body">

          <!-- Professional Audio Studio & Music Controls -->
          <div class="settings-audio-container">

            <!-- 1. Background Study Music / Ambient Focus Drone -->
            <div class="audio-card">
              <div class="audio-card-header">
                <div class="audio-card-title-group">
                  <span class="audio-icon-badge">🎵</span>
                  <div>
                    <div class="audio-section-title">Background Study Music</div>
                    <div class="audio-section-sub">Ambient procedural focus tones for deep memorization</div>
                  </div>
                </div>
                <label class="toggle-switch" aria-label="Toggle Background Music">
                  <input type="checkbox" id="toggle-bgm" />
                  <span class="toggle-slider"></span>
                </label>
              </div>

              <div id="bgm-panel" style="display: none; flex-direction: column; gap: 10px;">
                <!-- Mode selector -->
                <div class="audio-mode-selector">
                  <button type="button" class="audio-chip-btn active" data-bgm="lofi">Lo-Fi Warm Pad</button>
                  <button type="button" class="audio-chip-btn" data-bgm="alpha">Alpha Wave (10Hz)</button>
                  <button type="button" class="audio-chip-btn" data-bgm="zen">Zen Ambient</button>
                </div>
                <!-- BGM Volume -->
                <div class="audio-slider-group">
                  <div class="audio-slider-label">
                    <span>Music Volume</span>
                    <span class="val-badge" id="badge-bgm-vol">25%</span>
                  </div>
                  <input type="range" class="settings-slider" id="slider-bgm-vol" min="0" max="100" value="25" />
                </div>
              </div>
            </div>

            <!-- 2. Voice & Speech Pronunciation (Volume, Pitch, Speed) -->
            <div class="audio-card">
              <div class="audio-card-header">
                <div class="audio-card-title-group">
                  <span class="audio-icon-badge">🎙️</span>
                  <div>
                    <div class="audio-section-title">Voice & Pronunciation</div>
                    <div class="audio-section-sub">Volume, pitch & speed for Spanish, Hindi & English</div>
                  </div>
                </div>
                <button type="button" class="btn-audio-test" id="btn-test-voice" title="Test voice speech">
                  <span>Preview 🔊</span>
                </button>
              </div>

              <div class="audio-sliders-grid">
                <!-- Speech Volume -->
                <div class="audio-slider-group">
                  <div class="audio-slider-label">
                    <span>Speech Volume</span>
                    <span class="val-badge" id="badge-voice-vol">100%</span>
                  </div>
                  <input type="range" class="settings-slider" id="slider-voice-vol" min="0" max="100" value="100" />
                </div>

                <!-- Speech Pitch -->
                <div class="audio-slider-group">
                  <div class="audio-slider-label">
                    <span>Speech Pitch</span>
                    <span class="val-badge" id="badge-voice-pitch">1.0×</span>
                  </div>
                  <input type="range" class="settings-slider" id="slider-voice-pitch" min="50" max="150" value="100" />
                </div>

                <!-- Speech Speed (Rate) -->
                <div class="audio-slider-group">
                  <div class="audio-slider-label">
                    <span>Speech Speed (Rate)</span>
                    <span class="val-badge" id="badge-voice-rate">0.80×</span>
                  </div>
                  <input type="range" class="settings-slider" id="slider-voice-rate" min="50" max="130" value="80" />
                </div>
              </div>
            </div>

            <!-- 3. Card Sound Effects (SFX) -->
            <div class="audio-card">
              <div class="audio-card-header">
                <div class="audio-card-title-group">
                  <span class="audio-icon-badge">🎚️</span>
                  <div>
                    <div class="audio-section-title">Card Flip Sound Effects</div>
                    <div class="audio-section-sub">Physical card whoosh & tactile micro-snap</div>
                  </div>
                </div>
                <button type="button" class="btn-audio-test" id="btn-test-sfx" title="Audition card flip sound">
                  <span>Audition ⚡</span>
                </button>
              </div>

              <div class="audio-sliders-grid">
                <div class="audio-slider-group">
                  <div class="audio-slider-label">
                    <span>SFX Volume</span>
                    <span class="val-badge" id="badge-sfx-vol">100%</span>
                  </div>
                  <input type="range" class="settings-slider" id="slider-sfx-vol" min="0" max="100" value="100" />
                </div>

                <div class="audio-mode-selector">
                  <button type="button" class="audio-chip-btn active" data-sfx="snap">Crisp Snap</button>
                  <button type="button" class="audio-chip-btn" data-sfx="whoosh">Soft Whoosh</button>
                  <button type="button" class="audio-chip-btn" data-sfx="mute">Silent</button>
                </div>
              </div>
            </div>

          </div>

          <!-- Download Offline HTML Card -->
          <div class="settings-action-card">`;

html = html.replace(oldSettingsModalContent, newAudioModalMarkup);

// 3. Add Ambient Background Music Synthesizer & Audio Settings Controller in JavaScript
const audioControllerJs = `
      // ==========================================
      // PROFESSIONAL AUDIO STUDIO & MUSIC CONTROLLER
      // ==========================================
      const AUDIO_PREFS_KEY = "vocab_800_1000_audio_prefs";

      let audioPrefs = {
        bgmEnabled: false,
        bgmMode: "lofi",
        bgmVolume: 0.25,
        voiceVolume: 1.0,
        voicePitch: 1.0,
        voiceRate: 0.80,
        sfxVolume: 1.0,
        sfxStyle: "snap"
      };

      try {
        const saved = localStorage.getItem(AUDIO_PREFS_KEY);
        if (saved) {
          audioPrefs = { ...audioPrefs, ...JSON.parse(saved) };
        }
      } catch (e) {}

      function saveAudioPrefs() {
        try {
          localStorage.setItem(AUDIO_PREFS_KEY, JSON.stringify(audioPrefs));
        } catch (e) {}
      }

      // Procedural Ambient Music Synthesizer (100% Offline, Zero Network Requests)
      class AmbientStudyMusic {
        constructor() {
          this.ctx = null;
          this.isPlaying = false;
          this.nodes = [];
          this.masterGain = null;
          this.cycleTimer = null;
        }

        initContext() {
          if (!this.ctx) {
            const AudioCtx = window.AudioContext || window.webkitAudioContext;
            if (AudioCtx) this.ctx = new AudioCtx();
          }
          if (this.ctx && this.ctx.state === "suspended") {
            this.ctx.resume();
          }
        }

        start(mode = "lofi", vol = 0.25) {
          this.initContext();
          if (!this.ctx) return;
          this.stop();

          this.isPlaying = true;
          this.masterGain = this.ctx.createGain();
          this.masterGain.gain.setValueAtTime(0.001, this.ctx.currentTime);
          this.masterGain.gain.exponentialRampToValueAtTime(Math.max(0.005, vol * 0.18), this.ctx.currentTime + 1.2);
          this.masterGain.connect(this.ctx.destination);

          if (mode === "alpha") {
            // Binaural Alpha Focus Drone (10Hz difference)
            const oscL = this.ctx.createOscillator();
            const oscR = this.ctx.createOscillator();
            const filter = this.ctx.createBiquadFilter();
            filter.type = "lowpass";
            filter.frequency.value = 320;

            oscL.frequency.value = 216; // 216 Hz
            oscR.frequency.value = 226; // 226 Hz (10Hz Alpha beat for focus)
            oscL.type = "sine";
            oscR.type = "sine";

            oscL.connect(filter);
            oscR.connect(filter);
            filter.connect(this.masterGain);

            oscL.start();
            oscR.start();
            this.nodes.push(oscL, oscR, filter);
          } else if (mode === "zen") {
            // Celestial Zen Harmonics
            const freqs = [174, 261, 392, 523];
            freqs.forEach(freq => {
              const osc = this.ctx.createOscillator();
              const gain = this.ctx.createGain();
              osc.type = "sine";
              osc.frequency.value = freq;
              gain.gain.value = 0.25;
              osc.connect(gain);
              gain.connect(this.masterGain);
              osc.start();
              this.nodes.push(osc, gain);
            });
          } else {
            // Warm Lo-Fi Pad chord with slow filter breathing
            const chords = [
              [164.81, 246.94, 329.63], // E minor
              [146.83, 220.00, 293.66], // D major
              [174.61, 261.63, 349.23]  // F major
            ];
            let chordIdx = 0;

            const filter = this.ctx.createBiquadFilter();
            filter.type = "lowpass";
            filter.frequency.setValueAtTime(420, this.ctx.currentTime);
            filter.connect(this.masterGain);
            this.nodes.push(filter);

            let currentOscs = [];
            const playChord = (chord) => {
              currentOscs.forEach(o => {
                try { o.stop(this.ctx.currentTime + 0.8); } catch(e){}
              });
              currentOscs = [];

              chord.forEach(freq => {
                const osc = this.ctx.createOscillator();
                const gain = this.ctx.createGain();
                osc.type = "triangle";
                osc.frequency.setValueAtTime(freq, this.ctx.currentTime);

                gain.gain.setValueAtTime(0.001, this.ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.28, this.ctx.currentTime + 1.2);
                gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 5.8);

                osc.connect(gain);
                gain.connect(filter);
                osc.start();
                osc.stop(this.ctx.currentTime + 6.0);
                currentOscs.push(osc);
                this.nodes.push(osc, gain);
              });
            };

            playChord(chords[0]);
            this.cycleTimer = setInterval(() => {
              if (!this.isPlaying) return;
              chordIdx = (chordIdx + 1) % chords.length;
              playChord(chords[chordIdx]);
            }, 6000);
          }
        }

        setVolume(vol) {
          if (this.masterGain && this.ctx) {
            this.masterGain.gain.setValueAtTime(Math.max(0.0001, vol * 0.18), this.ctx.currentTime);
          }
        }

        stop() {
          this.isPlaying = false;
          if (this.cycleTimer) {
            clearInterval(this.cycleTimer);
            this.cycleTimer = null;
          }
          if (this.masterGain && this.ctx) {
            try {
              this.masterGain.gain.exponentialRampToValueAtTime(0.0001, this.ctx.currentTime + 0.6);
            } catch(e){}
          }
          setTimeout(() => {
            this.nodes.forEach(n => {
              try { if (n.stop) n.stop(); if (n.disconnect) n.disconnect(); } catch(e){}
            });
            this.nodes = [];
          }, 700);
        }
      }

      const ambientMusic = new AmbientStudyMusic();

      // Hook Settings DOM elements
      const toggleBgm = document.getElementById("toggle-bgm");
      const bgmPanel = document.getElementById("bgm-panel");
      const sliderBgmVol = document.getElementById("slider-bgm-vol");
      const badgeBgmVol = document.getElementById("badge-bgm-vol");
      const bgmChipBtns = document.querySelectorAll("[data-bgm]");

      const sliderVoiceVol = document.getElementById("slider-voice-vol");
      const badgeVoiceVol = document.getElementById("badge-voice-vol");
      const sliderVoicePitch = document.getElementById("slider-voice-pitch");
      const badgeVoicePitch = document.getElementById("badge-voice-pitch");
      const sliderVoiceRate = document.getElementById("slider-voice-rate");
      const badgeVoiceRate = document.getElementById("badge-voice-rate");
      const btnTestVoice = document.getElementById("btn-test-voice");

      const sliderSfxVol = document.getElementById("slider-sfx-vol");
      const badgeSfxVol = document.getElementById("badge-sfx-vol");
      const sfxChipBtns = document.querySelectorAll("[data-sfx]");
      const btnTestSfx = document.getElementById("btn-test-sfx");

      // Initialize UI from audioPrefs
      function syncAudioUI() {
        if (toggleBgm) {
          toggleBgm.checked = audioPrefs.bgmEnabled;
          if (bgmPanel) bgmPanel.style.display = audioPrefs.bgmEnabled ? "flex" : "none";
        }
        if (sliderBgmVol && badgeBgmVol) {
          sliderBgmVol.value = Math.round(audioPrefs.bgmVolume * 100);
          badgeBgmVol.textContent = \`\${Math.round(audioPrefs.bgmVolume * 100)}%\`;
        }
        bgmChipBtns.forEach(btn => {
          btn.classList.toggle("active", btn.dataset.bgm === audioPrefs.bgmMode);
        });

        if (sliderVoiceVol && badgeVoiceVol) {
          sliderVoiceVol.value = Math.round(audioPrefs.voiceVolume * 100);
          badgeVoiceVol.textContent = \`\${Math.round(audioPrefs.voiceVolume * 100)}%\`;
        }
        if (sliderVoicePitch && badgeVoicePitch) {
          sliderVoicePitch.value = Math.round(audioPrefs.voicePitch * 100);
          badgeVoicePitch.textContent = \`\${audioPrefs.voicePitch.toFixed(2)}×\`;
        }
        if (sliderVoiceRate && badgeVoiceRate) {
          sliderVoiceRate.value = Math.round(audioPrefs.voiceRate * 100);
          badgeVoiceRate.textContent = \`\${audioPrefs.voiceRate.toFixed(2)}×\`;
        }

        if (sliderSfxVol && badgeSfxVol) {
          sliderSfxVol.value = Math.round(audioPrefs.sfxVolume * 100);
          badgeSfxVol.textContent = \`\${Math.round(audioPrefs.sfxVolume * 100)}%\`;
        }
        sfxChipBtns.forEach(btn => {
          btn.classList.toggle("active", btn.dataset.sfx === audioPrefs.sfxStyle);
        });
      }

      syncAudioUI();

      // BGM Event Handlers
      if (toggleBgm) {
        toggleBgm.addEventListener("change", (e) => {
          audioPrefs.bgmEnabled = e.target.checked;
          if (bgmPanel) bgmPanel.style.display = audioPrefs.bgmEnabled ? "flex" : "none";
          saveAudioPrefs();
          if (audioPrefs.bgmEnabled) {
            ambientMusic.start(audioPrefs.bgmMode, audioPrefs.bgmVolume);
            showToast("🎵 Study ambient music started");
          } else {
            ambientMusic.stop();
          }
        });
      }

      if (sliderBgmVol) {
        sliderBgmVol.addEventListener("input", (e) => {
          audioPrefs.bgmVolume = e.target.value / 100;
          if (badgeBgmVol) badgeBgmVol.textContent = \`\${e.target.value}%\`;
          ambientMusic.setVolume(audioPrefs.bgmVolume);
          saveAudioPrefs();
        });
      }

      bgmChipBtns.forEach(btn => {
        btn.addEventListener("click", () => {
          bgmChipBtns.forEach(b => b.classList.remove("active"));
          btn.classList.add("active");
          audioPrefs.bgmMode = btn.dataset.bgm;
          saveAudioPrefs();
          if (audioPrefs.bgmEnabled) {
            ambientMusic.start(audioPrefs.bgmMode, audioPrefs.bgmVolume);
          }
        });
      });

      // Voice Slider Event Handlers
      if (sliderVoiceVol) {
        sliderVoiceVol.addEventListener("input", (e) => {
          audioPrefs.voiceVolume = e.target.value / 100;
          if (badgeVoiceVol) badgeVoiceVol.textContent = \`\${e.target.value}%\`;
          saveAudioPrefs();
        });
      }
      if (sliderVoicePitch) {
        sliderVoicePitch.addEventListener("input", (e) => {
          audioPrefs.voicePitch = e.target.value / 100;
          if (badgeVoicePitch) badgeVoicePitch.textContent = \`\${audioPrefs.voicePitch.toFixed(2)}×\`;
          saveAudioPrefs();
        });
      }
      if (sliderVoiceRate) {
        sliderVoiceRate.addEventListener("input", (e) => {
          audioPrefs.voiceRate = e.target.value / 100;
          if (badgeVoiceRate) badgeVoiceRate.textContent = \`\${audioPrefs.voiceRate.toFixed(2)}×\`;
          saveAudioPrefs();
        });
      }

      // Voice Preview Button
      if (btnTestVoice) {
        btnTestVoice.addEventListener("click", () => {
          cardAudio.playTapClick();
          const card = cards[currentIndex] || cards[0];
          playNativeSpeech(\`\${card.word}, \${card.trans.es.split('/')[0]}\`, "es", btnTestVoice, "speaking-es");
        });
      }

      // SFX Sliders and Mode Handlers
      if (sliderSfxVol) {
        sliderSfxVol.addEventListener("input", (e) => {
          audioPrefs.sfxVolume = e.target.value / 100;
          if (badgeSfxVol) badgeSfxVol.textContent = \`\${e.target.value}%\`;
          saveAudioPrefs();
        });
      }
      sfxChipBtns.forEach(btn => {
        btn.addEventListener("click", () => {
          sfxChipBtns.forEach(b => b.classList.remove("active"));
          btn.classList.add("active");
          audioPrefs.sfxStyle = btn.dataset.sfx;
          saveAudioPrefs();
        });
      });

      // SFX Preview Button
      if (btnTestSfx) {
        btnTestSfx.addEventListener("click", () => {
          cardAudio.playCardFlip(false);
        });
      }
`;

// Insert the audio controller into the script
html = html.replace(
  '// Gesture & Touch Event Listeners on Card Wrapper',
  audioControllerJs + '\n\n      // Gesture & Touch Event Listeners on Card Wrapper'
);

// 4. Update CardAudioEngine and playNativeSpeech to use user-configured audioPrefs values in real time!
html = html.replace(
  `        playCardFlip(isFlippingBack = false) {
          if (!this.enabled) return;
          this.unlock();
          if (!this.ctx) return;`,
  `        playCardFlip(isFlippingBack = false) {
          if (!this.enabled) return;
          if (audioPrefs && audioPrefs.sfxStyle === "mute") return;
          this.unlock();
          if (!this.ctx) return;
          const sfxGainScale = (audioPrefs && typeof audioPrefs.sfxVolume === "number") ? audioPrefs.sfxVolume : 1.0;
          if (sfxGainScale <= 0.01) return;`
);

html = html.replace(
  `whooshGain.gain.setValueAtTime(0.50, t);`,
  `whooshGain.gain.setValueAtTime(0.50 * sfxGainScale, t);`
);

html = html.replace(
  `snapGain.gain.setValueAtTime(0.58, t + 0.01);`,
  `snapGain.gain.setValueAtTime((audioPrefs.sfxStyle === "whoosh" ? 0.05 : 0.58) * sfxGainScale, t + 0.01);`
);

html = html.replace(
  `gain.gain.setValueAtTime(0.38, t);`,
  `const tapScale = (audioPrefs && typeof audioPrefs.sfxVolume === "number") ? audioPrefs.sfxVolume : 1.0;
            gain.gain.setValueAtTime(0.38 * tapScale, t);`
);

// Update playNativeSpeech to use audioPrefs.voiceVolume, audioPrefs.voicePitch, and audioPrefs.voiceRate
html = html.replace(
  `            utterance.volume = 1.0;
            utterance.rate = 0.80;
            utterance.pitch = 1.0;`,
  `            utterance.volume = (audioPrefs && typeof audioPrefs.voiceVolume === "number") ? audioPrefs.voiceVolume : 1.0;
            utterance.rate = (audioPrefs && typeof audioPrefs.voiceRate === "number") ? audioPrefs.voiceRate : 0.80;
            utterance.pitch = (audioPrefs && typeof audioPrefs.voicePitch === "number") ? audioPrefs.voicePitch : 1.0;`
);

fs.writeFileSync('index.html', html);
console.log('Successfully integrated Professional Audio Studio & Music Controls into Settings!');
