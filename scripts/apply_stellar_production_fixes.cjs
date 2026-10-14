const fs = require('fs');
const path = require('path');

const indexPath = path.join(__dirname, '..', 'index.html');
let html = fs.readFileSync(indexPath, 'utf8');

console.log('Original index.html length:', html.length);

// 1. Ensure #app-toast exists in the HTML
if (!html.includes('id="app-toast"')) {
  // Insert before </body>
  const toastHtml = `
    <!-- Global Tactile Toast Notification -->
    <div class="toast-notification" id="app-toast">
      <span class="toast-icon" id="toast-icon">⚡</span>
      <span id="toast-text"></span>
    </div>
  `;
  html = html.replace('</body>', toastHtml + '\n</body>');
  console.log('Added #app-toast to HTML');
}

// 2. Fix the Flashcard Screen Top Header
// Replace the top category learned pill with clean Deck / Tier indicator, and add Settings button to top-nav-actions
const topNavOld = `<div class="top-nav-center-group" style="display: flex; align-items: center; gap: 10px;">
              <span class="top-category-pill learned-tier-badge" id="current-category" style="padding: 6px 14px; font-weight: 750; font-size: 0.84rem; border-radius: 9999px; background: rgba(16, 185, 129, 0.16); border: 1.5px solid rgba(16, 185, 129, 0.35); color: #34d399; display: inline-flex; align-items: center; gap: 4px;">
                <span>Learned:</span> <strong id="section-learned-count">0</strong> / <span id="section-total-count">200</span>
              </span>
              <div class="counter-display" style="font-weight: 800; font-size: 0.95rem; color: #f1f5f9; display: flex; align-items: center; gap: 4px;">
                <span class="current-num" id="card-counter-current">800</span>
                <span class="counter-divider" style="color: #64748b;">/</span>
                <span class="total-num" id="card-counter-total" style="color: #94a3b8;">1000</span>
              </div>
            </div>`;

const topNavNew = `<div class="top-nav-center-group" style="display: flex; align-items: center; gap: 10px;">
              <span class="top-category-pill" id="current-category" style="padding: 5px 12px; font-weight: 700; font-size: 0.82rem; border-radius: 9999px; background: rgba(56, 189, 248, 0.12); border: 1px solid rgba(56, 189, 248, 0.3); color: #38bdf8; display: inline-flex; align-items: center; gap: 6px;">
                <span style="display: inline-block; width: 6px; height: 6px; border-radius: 50%; background: #38bdf8;"></span>
                <span>Tier 1: 800–1000</span>
              </span>
              <div class="counter-display" style="font-weight: 800; font-size: 0.95rem; color: #f1f5f9; display: flex; align-items: center; gap: 4px;">
                <span class="current-num" id="card-counter-current">800</span>
                <span class="counter-divider" style="color: #64748b;">/</span>
                <span class="total-num" id="card-counter-total" style="color: #94a3b8;">1000</span>
              </div>
            </div>`;

if (html.includes(topNavOld)) {
  html = html.replace(topNavOld, topNavNew);
  console.log('Replaced topNav center group (removed Learned label from top)');
}

// In top-nav-actions, ensure btn-flashcard-settings exists
const topActionsOld = `<div class="top-nav-actions" style="display: flex; align-items: center; gap: 8px;">
              <button type="button" class="reset-deck-btn duo-btn-3d" id="btn-reset-deck" title="Reset deck & restore all deleted cards" aria-label="Reset deck">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>
                  <path d="M3 3v5h5"/>
                </svg>
              </button>
              <button class="shuffle-btn duo-btn-3d" id="btn-shuffle" title="Shuffle cards" aria-label="Shuffle cards" style="width: 38px; height: 38px; border-radius: 12px; display: flex; align-items: center; justify-content: center; background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.16); box-shadow: 0 3px 0 rgba(0,0,0,0.4); color: #f1f5f9;">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M2 18h1.4c1.3 0 2.5-.6 3.3-1.7l6.6-8.6c.8-1.1 2-1.7 3.3-1.7H22"/>
                  <path d="m18 2 4 4-4 4"/>
                  <path d="M2 6h1.4c1.3 0 2.5.6 3.3 1.7l2 2.6"/>
                  <path d="M14.6 13.7l2.1 2.6c.8 1.1 2 1.7 3.3 1.7H22"/>
                  <path d="m18 20 4-4-4-4"/>
                </svg>
              </button>
            </div>`;

const topActionsNew = `<div class="top-nav-actions" style="display: flex; align-items: center; gap: 8px;">
              <button type="button" class="reset-deck-btn duo-btn-3d" id="btn-reset-deck" title="Reset deck & restore all deleted cards" aria-label="Reset deck">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>
                  <path d="M3 3v5h5"/>
                </svg>
              </button>
              <button class="shuffle-btn duo-btn-3d" id="btn-shuffle" title="Shuffle cards" aria-label="Shuffle cards" style="width: 38px; height: 38px; border-radius: 12px; display: flex; align-items: center; justify-content: center; background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.16); box-shadow: 0 3px 0 rgba(0,0,0,0.4); color: #f1f5f9;">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M2 18h1.4c1.3 0 2.5-.6 3.3-1.7l6.6-8.6c.8-1.1 2-1.7 3.3-1.7H22"/>
                  <path d="m18 2 4 4-4 4"/>
                  <path d="M2 6h1.4c1.3 0 2.5.6 3.3 1.7l2 2.6"/>
                  <path d="M14.6 13.7l2.1 2.6c.8 1.1 2 1.7 3.3 1.7H22"/>
                  <path d="m18 20 4-4-4-4"/>
                </svg>
              </button>
              <button type="button" class="duo-btn-3d" id="btn-flashcard-settings" title="Settings & Audio Studio" aria-label="Settings" style="width: 38px; height: 38px; border-radius: 12px; display: flex; align-items: center; justify-content: center; background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.16); box-shadow: 0 3px 0 rgba(0,0,0,0.4); color: #f1f5f9; cursor: pointer;">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="3"/>
                  <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
                </svg>
              </button>
            </div>`;

if (html.includes(topActionsOld)) {
  html = html.replace(topActionsOld, topActionsNew);
  console.log('Added btn-flashcard-settings to top-nav-actions');
}

// 3. Ensure card front actions have ONLY icons (no text labels) on the card front side
// Notice: front-learned-btn and front-delete-btn already have SVG icons only in the markup!
// Let us verify their styling and active state styling.

// 4. Clean up any unguarded jumpSlider and sliderValIndicator calls
html = html.replace(/(\bjumpSlider\.value\s*=[^;]+;)/g, 'if (typeof jumpSlider !== "undefined" && jumpSlider) { $1 }');
html = html.replace(/(\bsliderValIndicator\.textContent\s*=[^;]+;)/g, 'if (typeof sliderValIndicator !== "undefined" && sliderValIndicator) { $1 }');

// 5. Clean up any unguarded editModalCloseBtn or editCardForm
html = html.replace(/editModalCloseBtn\.addEventListener/g, 'if (editModalCloseBtn) editModalCloseBtn.addEventListener');
html = html.replace(/editCardForm\.addEventListener/g, 'if (editCardForm) editCardForm.addEventListener');

// 6. In renderCurrentCard(), remove the line that overwrites currentCategoryEl with "Learned: 0 / 200"
// Instead, keep it as category/tier title
html = html.replace(
  /currentCategoryEl\.innerHTML\s*=\s*`<span>Learned:<\/span>[^`]+`;/g,
  'currentCategoryEl.innerHTML = `<span style="display:inline-block;width:6px;height:6px;border-radius:50%;background:#38bdf8;"></span><span>Tier 1: 800–1000</span>`;'
);

// 7. Write a world-class CSS styling for .app-menu-drawer and .settings-modal-*
// Let's create an unbeatable, pristine CSS block for the Settings Modal
const modernSettingsCss = `
    /* ========================================================================= */
    /* PRODUCTION-GRADE LUXURIOUS SETTINGS MODAL & BOTTOM SHEET                  */
    /* ========================================================================= */
    .menu-drawer-backdrop {
      position: fixed !important;
      inset: 0 !important;
      background: rgba(3, 7, 18, 0.75) !important;
      backdrop-filter: blur(14px) !important;
      -webkit-backdrop-filter: blur(14px) !important;
      z-index: 9998 !important;
      opacity: 0 !important;
      pointer-events: none !important;
      transition: opacity 0.26s cubic-bezier(0.16, 1, 0.3, 1) !important;
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
      max-width: 580px !important;
      height: fit-content !important;
      max-height: 86vh !important;
      background: linear-gradient(180deg, #131d31 0%, #0a101d 100%) !important;
      border: 1px solid rgba(255, 255, 255, 0.12) !important;
      border-radius: 24px !important;
      box-shadow: 0 25px 70px -10px rgba(0, 0, 0, 0.85), 0 0 30px rgba(56, 189, 248, 0.12) !important;
      z-index: 9999 !important;
      display: flex !important;
      flex-direction: column !important;
      overflow: hidden !important;
      opacity: 0 !important;
      pointer-events: none !important;
      transform: scale(0.96) translateY(14px) !important;
      transition: opacity 0.25s cubic-bezier(0.16, 1, 0.3, 1), transform 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
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
        max-height: 88vh !important;
        border-radius: 26px 26px 0 0 !important;
        border-left: none !important;
        border-right: none !important;
        border-bottom: none !important;
        transform: translateY(100%) !important;
        box-shadow: 0 -12px 50px rgba(0, 0, 0, 0.8) !important;
      }
      .app-menu-drawer.open {
        transform: translateY(0) !important;
      }
    }

    .drawer-sheet-handle {
      display: none;
      width: 42px;
      height: 5px;
      border-radius: 9999px;
      background: rgba(255, 255, 255, 0.22);
      margin: 12px auto 4px;
    }
    @media (max-width: 640px) {
      .drawer-sheet-handle {
        display: block;
      }
    }

    /* Modal Header */
    .settings-modal-header {
      display: flex !important;
      align-items: center !important;
      justify-content: space-between !important;
      padding: 18px 24px 14px !important;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
      background: rgba(255, 255, 255, 0.02) !important;
    }
    .settings-header-title-group {
      display: flex !important;
      align-items: center !important;
      gap: 14px !important;
    }
    .settings-icon-badge {
      width: 42px !important;
      height: 42px !important;
      border-radius: 14px !important;
      background: rgba(56, 189, 248, 0.14) !important;
      border: 1px solid rgba(56, 189, 248, 0.35) !important;
      box-shadow: 0 4px 14px rgba(56, 189, 248, 0.22) !important;
      color: #38bdf8 !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      flex-shrink: 0 !important;
    }
    .settings-modal-title {
      font-size: 1.2rem !important;
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
      border: 1px solid rgba(255, 255, 255, 0.16) !important;
      box-shadow: 0 3px 0 rgba(0, 0, 0, 0.4) !important;
      color: #cbd5e1 !important;
      font-size: 1.15rem !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      cursor: pointer !important;
      transition: all 0.15s ease !important;
      flex-shrink: 0 !important;
    }
    .settings-modal-close-btn:hover {
      background: rgba(255, 255, 255, 0.16) !important;
      color: #ffffff !important;
      transform: scale(1.05) !important;
    }

    /* Tabs Bar */
    .settings-tabs-bar {
      display: flex !important;
      gap: 6px !important;
      padding: 10px 20px !important;
      background: rgba(0, 0, 0, 0.28) !important;
      border-bottom: 1px solid rgba(255, 255, 255, 0.07) !important;
      overflow-x: auto !important;
      scrollbar-width: none !important;
    }
    .settings-tabs-bar::-webkit-scrollbar {
      display: none !important;
    }
    .settings-tab-btn {
      flex: 1 1 0 !important;
      min-width: 0 !important;
      padding: 9px 8px !important;
      border-radius: 12px !important;
      background: rgba(255, 255, 255, 0.04) !important;
      border: 1px solid rgba(255, 255, 255, 0.08) !important;
      color: #94a3b8 !important;
      font-size: 0.78rem !important;
      font-weight: 700 !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      gap: 5px !important;
      cursor: pointer !important;
      transition: all 0.16s ease !important;
      white-space: nowrap !important;
    }
    .settings-tab-btn:hover {
      background: rgba(255, 255, 255, 0.09) !important;
      color: #f1f5f9 !important;
    }
    .settings-tab-btn.active {
      background: rgba(56, 189, 248, 0.18) !important;
      border-color: rgba(56, 189, 248, 0.55) !important;
      color: #38bdf8 !important;
      box-shadow: 0 2px 10px rgba(56, 189, 248, 0.3) !important;
    }

    /* Scroll Body */
    .settings-modal-body {
      flex: 1 1 auto !important;
      overflow-y: auto !important;
      padding: 20px 24px 24px !important;
      display: flex !important;
      flex-direction: column !important;
      gap: 16px !important;
      scrollbar-width: thin !important;
      scrollbar-color: rgba(255, 255, 255, 0.2) transparent !important;
    }
    .settings-modal-body::-webkit-scrollbar {
      width: 6px !important;
    }
    .settings-modal-body::-webkit-scrollbar-thumb {
      background: rgba(255, 255, 255, 0.2) !important;
      border-radius: 10px !important;
    }

    /* Panels */
    .settings-tab-panel {
      display: none !important;
      flex-direction: column !important;
      gap: 16px !important;
      animation: settingsFadeIn 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    .settings-tab-panel.active {
      display: flex !important;
    }
    @keyframes settingsFadeIn {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* Cards */
    .settings-card {
      background: rgba(255, 255, 255, 0.03) !important;
      border: 1px solid rgba(255, 255, 255, 0.08) !important;
      border-radius: 18px !important;
      padding: 16px 18px !important;
      display: flex !important;
      flex-direction: column !important;
      gap: 14px !important;
      transition: border-color 0.15s ease !important;
    }
    .settings-card:hover {
      border-color: rgba(255, 255, 255, 0.15) !important;
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
      font-size: 1.35rem !important;
      line-height: 1 !important;
    }
    .settings-card-title {
      font-size: 0.96rem !important;
      font-weight: 750 !important;
      color: #f8fafc !important;
      margin: 0 !important;
      letter-spacing: -0.01em !important;
    }
    .settings-card-sub {
      font-size: 0.77rem !important;
      color: #94a3b8 !important;
      margin: 3px 0 0 !important;
      line-height: 1.35 !important;
    }

    /* Choice Buttons Group */
    .settings-choice-group {
      display: flex !important;
      gap: 8px !important;
      width: 100% !important;
    }
    .settings-choice-btn {
      flex: 1 1 0 !important;
      padding: 10px 8px !important;
      border-radius: 12px !important;
      background: rgba(255, 255, 255, 0.04) !important;
      border: 1px solid rgba(255, 255, 255, 0.1) !important;
      color: #cbd5e1 !important;
      font-size: 0.82rem !important;
      font-weight: 700 !important;
      cursor: pointer !important;
      transition: all 0.15s ease !important;
      text-align: center !important;
      box-shadow: 0 2px 0 rgba(0, 0, 0, 0.25) !important;
    }
    .settings-choice-btn:hover {
      background: rgba(255, 255, 255, 0.08) !important;
      color: #ffffff !important;
    }
    .settings-choice-btn.active {
      background: rgba(56, 189, 248, 0.18) !important;
      border-color: #38bdf8 !important;
      color: #38bdf8 !important;
      box-shadow: 0 0 12px rgba(56, 189, 248, 0.25), 0 2px 0 rgba(0, 0, 0, 0.3) !important;
    }

    /* Slider Rows */
    .settings-slider-row {
      display: flex !important;
      flex-direction: column !important;
      gap: 7px !important;
    }
    .settings-slider-label-row {
      display: flex !important;
      align-items: center !important;
      justify-content: space-between !important;
      font-size: 0.8rem !important;
      font-weight: 600 !important;
      color: #cbd5e1 !important;
    }
    .settings-val-badge {
      font-size: 0.75rem !important;
      font-weight: 800 !important;
      padding: 3px 8px !important;
      border-radius: 8px !important;
      background: rgba(56, 189, 248, 0.14) !important;
      border: 1px solid rgba(56, 189, 248, 0.3) !important;
      color: #38bdf8 !important;
      font-variant-numeric: tabular-nums !important;
    }
    .custom-settings-slider {
      -webkit-appearance: none !important;
      appearance: none !important;
      width: 100% !important;
      height: 6px !important;
      border-radius: 9999px !important;
      background: rgba(255, 255, 255, 0.1) !important;
      outline: none !important;
      cursor: pointer !important;
    }
    .custom-settings-slider::-webkit-slider-thumb {
      -webkit-appearance: none !important;
      appearance: none !important;
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

    /* Action Buttons */
    .settings-action-btn {
      width: 100% !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      gap: 10px !important;
      padding: 12px 18px !important;
      border-radius: 14px !important;
      font-weight: 750 !important;
      font-size: 0.88rem !important;
      cursor: pointer !important;
      transition: all 0.16s ease !important;
      box-shadow: 0 3px 0 rgba(0, 0, 0, 0.35) !important;
    }
    .settings-action-btn-primary {
      background: rgba(56, 189, 248, 0.18) !important;
      border: 1.5px solid rgba(56, 189, 248, 0.45) !important;
      color: #38bdf8 !important;
    }
    .settings-action-btn-primary:hover {
      background: rgba(56, 189, 248, 0.28) !important;
      border-color: #38bdf8 !important;
      transform: translateY(-1px) !important;
    }
    .settings-action-btn-danger {
      background: rgba(239, 68, 68, 0.15) !important;
      border: 1.5px solid rgba(239, 68, 68, 0.4) !important;
      color: #f87171 !important;
    }
    .settings-action-btn-danger:hover {
      background: rgba(239, 68, 68, 0.25) !important;
      border-color: #ef4444 !important;
      transform: translateY(-1px) !important;
    }
    .settings-action-btn-success {
      background: rgba(16, 185, 129, 0.15) !important;
      border: 1.5px solid rgba(16, 185, 129, 0.4) !important;
      color: #34d399 !important;
    }
    .settings-action-btn-success:hover {
      background: rgba(16, 185, 129, 0.25) !important;
      border-color: #10b981 !important;
      transform: translateY(-1px) !important;
    }

    /* Card Front Action Buttons */
    .icon-tool-btn.front-learned-btn {
      width: 36px !important;
      height: 36px !important;
      border-radius: 10px !important;
      background: rgba(255, 255, 255, 0.08) !important;
      border: 1px solid rgba(255, 255, 255, 0.15) !important;
      color: #94a3b8 !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      cursor: pointer !important;
      transition: all 0.16s ease !important;
    }
    .icon-tool-btn.front-learned-btn:hover {
      background: rgba(16, 185, 129, 0.18) !important;
      border-color: rgba(16, 185, 129, 0.4) !important;
      color: #34d399 !important;
    }
    .icon-tool-btn.front-learned-btn.is-learned {
      background: rgba(16, 185, 129, 0.28) !important;
      border-color: #10b981 !important;
      color: #10b981 !important;
      box-shadow: 0 0 12px rgba(16, 185, 129, 0.4) !important;
    }
    .icon-tool-btn.front-delete-btn {
      width: 36px !important;
      height: 36px !important;
      border-radius: 10px !important;
      background: rgba(255, 255, 255, 0.08) !important;
      border: 1px solid rgba(255, 255, 255, 0.15) !important;
      color: #94a3b8 !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      cursor: pointer !important;
      transition: all 0.16s ease !important;
    }
    .icon-tool-btn.front-delete-btn:hover {
      background: rgba(239, 68, 68, 0.2) !important;
      border-color: #ef4444 !important;
      color: #f87171 !important;
    }

    /* Double Tap Glowing Ripple */
    .double-tap-ripple {
      position: absolute;
      width: 90px;
      height: 90px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(56, 189, 248, 0.5) 0%, rgba(56, 189, 248, 0) 70%);
      pointer-events: none;
      transform: translate(-50%, -50%) scale(0.3);
      animation: doubleTapRippleAnim 0.45s ease-out forwards;
      z-index: 100;
    }
    @keyframes doubleTapRippleAnim {
      0% { opacity: 1; transform: translate(-50%, -50%) scale(0.3); }
      100% { opacity: 0; transform: translate(-50%, -50%) scale(2.2); }
    }
`;

// Inject modernSettingsCss right before </style>
html = html.replace('</style>', modernSettingsCss + '\n</style>');
console.log('Injected modern settings CSS');

fs.writeFileSync(indexPath, html, 'utf8');
console.log('Updated index.html successfully!');
