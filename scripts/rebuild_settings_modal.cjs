const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');
console.log('Original index.html length:', html.length);

// =========================================================================
// 1. NEW CSS FOR WORLD-CLASS SETTINGS DIALOG
// =========================================================================
const settingsModalCss = `
      /* ==========================================================
         WORLD-CLASS CENTERED SETTINGS MODAL & DIALOG
         ========================================================== */
      .menu-drawer-backdrop {
        position: fixed !important;
        inset: 0 !important;
        background: rgba(7, 11, 22, 0.8) !important;
        backdrop-filter: blur(14px) !important;
        -webkit-backdrop-filter: blur(14px) !important;
        z-index: 1998 !important;
        opacity: 0 !important;
        pointer-events: none !important;
        transition: opacity 0.25s ease !important;
      }
      .menu-drawer-backdrop.open {
        opacity: 1 !important;
        pointer-events: auto !important;
      }

      .app-menu-drawer {
        position: fixed !important;
        inset: 0 !important;
        margin: auto !important;
        width: calc(100% - 32px) !important;
        max-width: 560px !important;
        height: fit-content !important;
        max-height: 86vh !important;
        background: linear-gradient(180deg, #172236 0%, #0c1424 100%) !important;
        border: 1.5px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 26px !important;
        box-shadow: 0 32px 75px -12px rgba(0, 0, 0, 0.9), 0 0 1px 1px rgba(255, 255, 255, 0.12) !important;
        z-index: 2000 !important;
        display: flex !important;
        flex-direction: column !important;
        overflow: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
        transform: scale(0.95) translateY(14px) !important;
        transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.22s ease !important;
      }

      .app-menu-drawer.open {
        opacity: 1 !important;
        pointer-events: auto !important;
        transform: scale(1) translateY(0) !important;
      }

      @media (max-width: 640px) {
        .app-menu-drawer {
          inset: auto 0 0 0 !important;
          width: 100% !important;
          max-width: 100% !important;
          max-height: 90vh !important;
          border-radius: 28px 28px 0 0 !important;
          border-bottom: none !important;
          border-left: none !important;
          border-right: none !important;
          transform: translateY(100%) !important;
        }
        .app-menu-drawer.open {
          transform: translateY(0) !important;
        }
      }

      /* Modal Header */
      .settings-modal-header {
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        padding: 20px 24px 16px !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
        background: rgba(255, 255, 255, 0.02) !important;
      }
      .settings-header-title-group {
        display: flex !important;
        align-items: center !important;
        gap: 14px !important;
      }
      .settings-icon-badge {
        width: 44px !important;
        height: 44px !important;
        border-radius: 14px !important;
        background: rgba(56, 189, 248, 0.14) !important;
        border: 1px solid rgba(56, 189, 248, 0.35) !important;
        box-shadow: 0 4px 14px rgba(56, 189, 248, 0.25) !important;
        color: #38bdf8 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
      }
      .settings-modal-title {
        font-size: 1.25rem !important;
        font-weight: 800 !important;
        color: #ffffff !important;
        margin: 0 !important;
        line-height: 1.2 !important;
        letter-spacing: -0.01em !important;
      }
      .settings-modal-sub {
        font-size: 0.78rem !important;
        color: #94a3b8 !important;
        margin: 3px 0 0 !important;
        font-weight: 500 !important;
      }
      .settings-modal-close-btn {
        width: 38px !important;
        height: 38px !important;
        border-radius: 12px !important;
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        box-shadow: 0 3px 0 rgba(0, 0, 0, 0.4) !important;
        color: #cbd5e1 !important;
        font-size: 1.2rem !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
        transition: all 0.15s ease !important;
      }
      .settings-modal-close-btn:hover {
        background: rgba(255, 255, 255, 0.16) !important;
        color: #ffffff !important;
      }

      /* Tabs Bar */
      .settings-tabs-bar {
        display: flex !important;
        gap: 8px !important;
        padding: 12px 24px !important;
        background: rgba(0, 0, 0, 0.22) !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06) !important;
      }
      .settings-tab-btn {
        flex: 1 !important;
        padding: 9px 12px !important;
        border-radius: 12px !important;
        background: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        color: #94a3b8 !important;
        font-size: 0.82rem !important;
        font-weight: 750 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 6px !important;
        cursor: pointer !important;
        transition: all 0.18s ease !important;
      }
      .settings-tab-btn:hover {
        background: rgba(255, 255, 255, 0.08) !important;
        color: #f1f5f9 !important;
      }
      .settings-tab-btn.active {
        background: rgba(56, 189, 248, 0.16) !important;
        border-color: rgba(56, 189, 248, 0.5) !important;
        color: #38bdf8 !important;
        box-shadow: 0 2px 8px rgba(56, 189, 248, 0.25) !important;
      }

      /* Modal Body & Tab Panels */
      .settings-modal-body {
        flex: 1 !important;
        overflow-y: auto !important;
        padding: 20px 24px 28px !important;
        display: flex !important;
        flex-direction: column !important;
        gap: 16px !important;
      }
      .settings-tab-panel {
        display: none !important;
        flex-direction: column !important;
        gap: 16px !important;
      }
      .settings-tab-panel.active {
        display: flex !important;
      }

      /* Settings Card */
      .settings-card {
        background: rgba(255, 255, 255, 0.035) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 20px !important;
        padding: 16px 18px !important;
        display: flex !important;
        flex-direction: column !important;
        gap: 14px !important;
        transition: border-color 0.2s ease !important;
      }
      .settings-card:hover {
        border-color: rgba(255, 255, 255, 0.14) !important;
      }
      .settings-card-header {
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        gap: 12px !important;
      }
      .settings-card-left {
        display: flex !important;
        align-items: center !important;
        gap: 12px !important;
      }
      .settings-card-icon {
        width: 38px !important;
        height: 38px !important;
        border-radius: 12px !important;
        background: rgba(255, 255, 255, 0.06) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 1.15rem !important;
      }
      .settings-card-title {
        font-size: 0.96rem !important;
        font-weight: 750 !important;
        color: #f1f5f9 !important;
        margin: 0 !important;
      }
      .settings-card-sub {
        font-size: 0.76rem !important;
        color: #94a3b8 !important;
        margin: 2px 0 0 !important;
      }

      /* Chips and Preset Buttons */
      .settings-choice-group {
        display: flex !important;
        gap: 8px !important;
        width: 100% !important;
      }
      .settings-choice-btn {
        flex: 1 !important;
        padding: 9px 12px !important;
        border-radius: 12px !important;
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        box-shadow: 0 3px 0 rgba(0, 0, 0, 0.3) !important;
        color: #cbd5e1 !important;
        font-size: 0.82rem !important;
        font-weight: 700 !important;
        cursor: pointer !important;
        transition: all 0.15s ease !important;
        text-align: center !important;
      }
      .settings-choice-btn:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        color: #ffffff !important;
      }
      .settings-choice-btn.active {
        background: rgba(56, 189, 248, 0.22) !important;
        border-color: rgba(56, 189, 248, 0.6) !important;
        box-shadow: 0 3px 0 rgba(14, 116, 144, 0.5) !important;
        color: #38bdf8 !important;
      }

      /* Sliders */
      .settings-slider-row {
        display: flex !important;
        flex-direction: column !important;
        gap: 6px !important;
      }
      .settings-slider-label-row {
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        font-size: 0.82rem !important;
        color: #cbd5e1 !important;
        font-weight: 650 !important;
      }
      .settings-val-badge {
        font-size: 0.75rem !important;
        font-weight: 800 !important;
        padding: 2px 8px !important;
        border-radius: 6px !important;
        background: rgba(56, 189, 248, 0.15) !important;
        color: #38bdf8 !important;
        border: 1px solid rgba(56, 189, 248, 0.25) !important;
      }
      .custom-settings-slider {
        -webkit-appearance: none !important;
        width: 100% !important;
        height: 6px !important;
        border-radius: 9999px !important;
        background: rgba(255, 255, 255, 0.1) !important;
        outline: none !important;
        cursor: pointer !important;
      }
      .custom-settings-slider::-webkit-slider-thumb {
        -webkit-appearance: none !important;
        width: 18px !important;
        height: 18px !important;
        border-radius: 50% !important;
        background: #38bdf8 !important;
        box-shadow: 0 0 10px rgba(56, 189, 248, 0.6) !important;
        cursor: pointer !important;
        transition: transform 0.1s ease !important;
      }
      .custom-settings-slider::-webkit-slider-thumb:hover {
        transform: scale(1.15) !important;
      }

      /* Tactile Action Buttons in Settings */
      .settings-action-btn {
        width: 100% !important;
        padding: 12px 18px !important;
        border-radius: 14px !important;
        font-size: 0.88rem !important;
        font-weight: 750 !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 8px !important;
        cursor: pointer !important;
        transition: all 0.18s ease !important;
      }
      .settings-action-btn-danger {
        background: rgba(239, 68, 68, 0.12) !important;
        border: 1.5px solid rgba(239, 68, 68, 0.35) !important;
        box-shadow: 0 3px 0 rgba(185, 28, 28, 0.45) !important;
        color: #f87171 !important;
      }
      .settings-action-btn-danger:hover {
        background: rgba(239, 68, 68, 0.24) !important;
        border-color: rgba(239, 68, 68, 0.65) !important;
        transform: translateY(-1px) !important;
      }
      .settings-action-btn-danger:active {
        transform: translateY(2px) !important;
        box-shadow: 0 1px 0 rgba(185, 28, 28, 0.45) !important;
      }
      .settings-action-btn-primary {
        background: rgba(56, 189, 248, 0.14) !important;
        border: 1.5px solid rgba(56, 189, 248, 0.35) !important;
        box-shadow: 0 3px 0 rgba(14, 116, 144, 0.5) !important;
        color: #38bdf8 !important;
      }
      .settings-action-btn-primary:hover {
        background: rgba(56, 189, 248, 0.24) !important;
        border-color: rgba(56, 189, 248, 0.65) !important;
        transform: translateY(-1px) !important;
      }
      .settings-action-btn-primary:active {
        transform: translateY(2px) !important;
        box-shadow: 0 1px 0 rgba(14, 116, 144, 0.5) !important;
      }
      .settings-action-btn-success {
        background: rgba(16, 185, 129, 0.14) !important;
        border: 1.5px solid rgba(16, 185, 129, 0.35) !important;
        box-shadow: 0 3px 0 rgba(5, 150, 105, 0.5) !important;
        color: #34d399 !important;
      }
      .settings-action-btn-success:hover {
        background: rgba(16, 185, 129, 0.24) !important;
        border-color: rgba(16, 185, 129, 0.65) !important;
        transform: translateY(-1px) !important;
      }
      .settings-action-btn-success:active {
        transform: translateY(2px) !important;
        box-shadow: 0 1px 0 rgba(5, 150, 105, 0.5) !important;
      }
`;

// Insert settingsModalCss into style
const endStylePos = html.indexOf('</style>');
html = html.slice(0, endStylePos) + '\n' + settingsModalCss + '\n' + html.slice(endStylePos);
console.log('Appended luxury settings modal CSS.');

// =========================================================================
// 2. REBUILD SETTINGS MODAL HTML (REPLACES DUPLICATE MODAL & UGLY DRAWER)
// =========================================================================
const modalStartPos = html.indexOf('<!-- Settings & Offline HTML Modal -->');
const modalEndPos = html.indexOf('<!-- ========================================================== -->\n    <!-- ADD SECTION MODAL');

if (modalStartPos === -1 || modalEndPos === -1) {
  console.error('Could not find modal markers!');
  process.exit(1);
}

const newSettingsModalHtml = `<!-- ========================================================== -->
    <!-- PRODUCTION-GRADE CENTERED SETTINGS & AUDIO DIALOG         -->
    <!-- ========================================================== -->
    <div class="menu-drawer-backdrop" id="menu-drawer-backdrop"></div>
    <aside class="app-menu-drawer" id="app-menu-drawer" aria-label="Settings and Preferences">
      <!-- Modal Header -->
      <div class="settings-modal-header">
        <div class="settings-header-title-group">
          <div class="settings-icon-badge">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/>
              <circle cx="12" cy="12" r="3"/>
            </svg>
          </div>
          <div>
            <h2 class="settings-modal-title">Settings & Preferences</h2>
            <p class="settings-modal-sub">Audio studio, speech tuning & study deck tools</p>
          </div>
        </div>
        <button type="button" class="settings-modal-close-btn duo-btn-3d" id="drawer-close-btn" aria-label="Close Settings">✕</button>
      </div>

      <!-- Tactile 3D Tabs Navigation -->
      <div class="settings-tabs-bar">
        <button type="button" class="settings-tab-btn active" data-tab-target="tab-audio">
          <span>🔊</span> <span>Sound & Music</span>
        </button>
        <button type="button" class="settings-tab-btn" data-tab-target="tab-speech">
          <span>🎙️</span> <span>Speech Tuning</span>
        </button>
        <button type="button" class="settings-tab-btn" data-tab-target="tab-deck">
          <span>⚡</span> <span>Deck & Data</span>
        </button>
      </div>

      <!-- Settings Scroll Body -->
      <div class="settings-modal-body">
        <!-- ================= TAB 1: AUDIO & SOUND EFFECTS ================= -->
        <div class="settings-tab-panel active" id="tab-audio">
          <!-- Card Flip Audio Effect -->
          <div class="settings-card">
            <div class="settings-card-header">
              <div class="settings-card-left">
                <div class="settings-card-icon">🎚️</div>
                <div>
                  <h3 class="settings-card-title">Card Flip Sound Effect</h3>
                  <p class="settings-card-sub">Tactile micro-snap and whoosh when flipping cards</p>
                </div>
              </div>
              <button type="button" class="duo-btn-3d btn-audio-test" id="btn-test-sfx" title="Audition sound" style="padding: 6px 14px; border-radius: 10px; font-size: 0.82rem; font-weight: 750; background: rgba(56, 189, 248, 0.15); border: 1px solid rgba(56, 189, 248, 0.35); color: #38bdf8;">
                <span>Audition ⚡</span>
              </button>
            </div>
            <div class="settings-choice-group">
              <button type="button" class="settings-choice-btn active" data-sfx="snap">Crisp Snap</button>
              <button type="button" class="settings-choice-btn" data-sfx="whoosh">Soft Whoosh</button>
              <button type="button" class="settings-choice-btn" data-sfx="mute">Silent</button>
            </div>
          </div>

          <!-- Background Study Music -->
          <div class="settings-card">
            <div class="settings-card-header">
              <div class="settings-card-left">
                <div class="settings-card-icon">🎵</div>
                <div>
                  <h3 class="settings-card-title">Focus Ambient Music</h3>
                  <p class="settings-card-sub">Procedural warm binaural focus tones for study</p>
                </div>
              </div>
              <label class="toggle-switch" aria-label="Toggle Background Music">
                <input type="checkbox" id="toggle-bgm" />
                <span class="toggle-slider"></span>
              </label>
            </div>

            <!-- BGM Expandable Panel -->
            <div id="bgm-panel" style="display: none; flex-direction: column; gap: 12px; margin-top: 4px; padding-top: 12px; border-top: 1px solid rgba(255, 255, 255, 0.08);">
              <div class="settings-choice-group">
                <button type="button" class="settings-choice-btn active" data-bgm="lofi">Lo-Fi Warm Pad</button>
                <button type="button" class="settings-choice-btn" data-bgm="alpha">Alpha 10Hz</button>
                <button type="button" class="settings-choice-btn" data-bgm="zen">Zen Ambient</button>
              </div>
              <div class="settings-slider-row">
                <div class="settings-slider-label-row">
                  <span>Music Volume</span>
                  <span class="settings-val-badge" id="badge-bgm-vol">25%</span>
                </div>
                <input type="range" class="custom-settings-slider" id="slider-bgm-vol" min="0" max="100" value="25" />
              </div>
            </div>
          </div>
        </div>

        <!-- ================= TAB 2: SPEECH & PRONUNCIATION ================= -->
        <div class="settings-tab-panel" id="tab-speech">
          <div class="settings-card">
            <div class="settings-card-header">
              <div class="settings-card-left">
                <div class="settings-card-icon">🎙️</div>
                <div>
                  <h3 class="settings-card-title">Native Pronunciation Tuning</h3>
                  <p class="settings-card-sub">Realistic English, Tamil, Spanish & Hindi accents</p>
                </div>
              </div>
              <button type="button" class="duo-btn-3d btn-audio-test" id="btn-test-voice" title="Test voice speech" style="padding: 6px 14px; border-radius: 10px; font-size: 0.82rem; font-weight: 750; background: rgba(56, 189, 248, 0.15); border: 1px solid rgba(56, 189, 248, 0.35); color: #38bdf8;">
                <span>Preview 🔊</span>
              </button>
            </div>

            <!-- Quick Speed Preset Chips -->
            <div style="display: flex; flex-direction: column; gap: 6px;">
              <span style="font-size: 0.78rem; color: #94a3b8; font-weight: 600;">Speech Speed Presets</span>
              <div class="settings-choice-group">
                <button type="button" class="settings-choice-btn" id="btn-rate-slow">0.75× Slower</button>
                <button type="button" class="settings-choice-btn active" id="btn-rate-normal">1.0× Normal</button>
                <button type="button" class="settings-choice-btn" id="btn-rate-fast">1.25× Faster</button>
              </div>
            </div>

            <!-- Fine-Tuning Sliders -->
            <div style="display: flex; flex-direction: column; gap: 14px; margin-top: 4px;">
              <div class="settings-slider-row">
                <div class="settings-slider-label-row">
                  <span>Speech Volume</span>
                  <span class="settings-val-badge" id="badge-voice-vol">100%</span>
                </div>
                <input type="range" class="custom-settings-slider" id="slider-voice-vol" min="0" max="100" value="100" />
              </div>

              <div class="settings-slider-row">
                <div class="settings-slider-label-row">
                  <span>Fine Speed Adjustment</span>
                  <span class="settings-val-badge" id="badge-voice-rate">0.80×</span>
                </div>
                <input type="range" class="custom-settings-slider" id="slider-voice-rate" min="50" max="130" value="80" />
              </div>

              <div class="settings-slider-row">
                <div class="settings-slider-label-row">
                  <span>Voice Pitch</span>
                  <span class="settings-val-badge" id="badge-voice-pitch">1.0×</span>
                </div>
                <input type="range" class="custom-settings-slider" id="slider-voice-pitch" min="50" max="150" value="100" />
              </div>
            </div>
          </div>
        </div>

        <!-- ================= TAB 3: DECK TOOLS & DATA MANAGEMENT ================= -->
        <div class="settings-tab-panel" id="tab-deck">
          <!-- Restore Deleted Cards -->
          <div class="settings-card">
            <div class="settings-card-header">
              <div class="settings-card-left">
                <div class="settings-card-icon" style="color: #38bdf8;">↺</div>
                <div>
                  <h3 class="settings-card-title">Restore Deleted Flashcards</h3>
                  <p class="settings-card-sub">Restore all deleted cards back to the full 200 items (800–1000)</p>
                </div>
              </div>
            </div>
            <button type="button" class="settings-action-btn settings-action-btn-primary duo-btn-3d" id="btn-settings-reset-deck">
              <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
                <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>
                <path d="M3 3v5h5"/>
              </svg>
              <span>Restore All 200 Cards (800–1000)</span>
            </button>
          </div>

          <!-- Reset Learned Progress -->
          <div class="settings-card">
            <div class="settings-card-header">
              <div class="settings-card-left">
                <div class="settings-card-icon" style="color: #f87171;">🗑️</div>
                <div>
                  <h3 class="settings-card-title">Reset Learned Progress</h3>
                  <p class="settings-card-sub">Clear your marked cards to study fresh from 0 / 200</p>
                </div>
              </div>
            </div>
            <button type="button" class="settings-action-btn settings-action-btn-danger duo-btn-3d" id="btn-settings-reset-learned">
              <span>Reset Learned Cards Progress (0 / 200)</span>
            </button>
          </div>

          <!-- Standalone Offline HTML -->
          <div class="settings-card">
            <div class="settings-card-header">
              <div class="settings-card-left">
                <div class="settings-card-icon" style="color: #34d399;">📥</div>
                <div>
                  <h3 class="settings-card-title">Standalone Offline Deck</h3>
                  <p class="settings-card-sub">Download self-contained offline study HTML file</p>
                </div>
              </div>
            </div>
            <button type="button" class="settings-action-btn settings-action-btn-success duo-btn-3d" id="btn-download-html-menu">
              <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="7 10 12 15 17 10"/>
                <line x1="12" y1="15" x2="12" y2="3"/>
              </svg>
              <span>Download Standalone Offline HTML</span>
            </button>
          </div>
        </div>
      </div>
    </aside>
    `;

html = html.slice(0, modalStartPos) + newSettingsModalHtml + html.slice(modalEndPos);
console.log('Replaced settings modal HTML markup.');

fs.writeFileSync('index.html', html, 'utf8');
console.log('Updated index.html. New size:', html.length);
