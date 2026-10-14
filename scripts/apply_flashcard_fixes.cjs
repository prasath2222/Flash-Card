const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');
console.log('Original index.html length:', html.length);

// =========================================================================
// 1. UPDATE CSS STYLES FOR FRONT ICONS, RESET BUTTON, SPEED INDICATOR, DOUBLE-TAP CUE
// =========================================================================
const cssToAdd = `
      /* Front Face Tactile Action Buttons (Learned Icon, Delete Icon, Speak) */
      .front-learned-btn {
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.16) !important;
        box-shadow: 0 3px 0 rgba(0, 0, 0, 0.35) !important;
        color: #94a3b8 !important;
        width: 36px !important;
        height: 36px !important;
        border-radius: 12px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
        transition: all 0.18s ease !important;
        user-select: none !important;
      }
      .front-learned-btn:hover {
        background: rgba(16, 185, 129, 0.16) !important;
        border-color: rgba(16, 185, 129, 0.45) !important;
        color: #34d399 !important;
        transform: translateY(-1px) !important;
      }
      .front-learned-btn.is-learned {
        background: rgba(16, 185, 129, 0.24) !important;
        border: 1.5px solid rgba(16, 185, 129, 0.7) !important;
        color: #34d399 !important;
        box-shadow: 0 0 14px rgba(16, 185, 129, 0.45), 0 3px 0 rgba(5, 150, 105, 0.5) !important;
      }
      .front-learned-btn.is-learned svg {
        stroke-width: 3.2 !important;
      }
      .front-delete-btn {
        background: rgba(239, 68, 68, 0.12) !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
        box-shadow: 0 3px 0 rgba(185, 28, 28, 0.4) !important;
        color: #f87171 !important;
        width: 36px !important;
        height: 36px !important;
        border-radius: 12px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
        transition: all 0.18s ease !important;
        user-select: none !important;
      }
      .front-delete-btn:hover {
        background: rgba(239, 68, 68, 0.28) !important;
        border-color: rgba(239, 68, 68, 0.65) !important;
        color: #fca5a5 !important;
        transform: translateY(-1px) !important;
      }
      .front-delete-btn:active {
        transform: translateY(2px) !important;
        box-shadow: 0 1px 0 rgba(185, 28, 28, 0.5) !important;
      }
      .reset-deck-btn {
        width: 38px !important;
        height: 38px !important;
        border-radius: 12px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        background: rgba(56, 189, 248, 0.12) !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        box-shadow: 0 3px 0 rgba(14, 116, 144, 0.5) !important;
        color: #38bdf8 !important;
        cursor: pointer !important;
        transition: all 0.15s ease !important;
        user-select: none !important;
      }
      .reset-deck-btn:hover {
        background: rgba(56, 189, 248, 0.24) !important;
        border-color: rgba(56, 189, 248, 0.6) !important;
        transform: translateY(-1px) !important;
      }
      .reset-deck-btn:active {
        transform: translateY(2px) !important;
        box-shadow: 0 1px 0 rgba(14, 116, 144, 0.5) !important;
      }
      /* Kinetic Swipe Speed Indicator Badge */
      .swipe-speed-badge {
        position: absolute;
        top: 14px;
        left: 50%;
        transform: translateX(-50%) translateY(-10px) scale(0.85);
        background: rgba(15, 23, 42, 0.92);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(56, 189, 248, 0.4);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6), 0 0 16px rgba(56, 189, 248, 0.3);
        color: #38bdf8;
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 800;
        letter-spacing: 0.02em;
        pointer-events: none;
        z-index: 50;
        opacity: 0;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        display: flex;
        align-items: center;
        gap: 6px;
      }
      .swipe-speed-badge.show {
        opacity: 1;
        transform: translateX(-50%) translateY(0) scale(1);
      }
      /* Double Tap Pulse Ripple Effect */
      .double-tap-ripple {
        position: absolute;
        width: 80px;
        height: 80px;
        margin-left: -40px;
        margin-top: -40px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(56, 189, 248, 0.45) 0%, rgba(56, 189, 248, 0) 70%);
        pointer-events: none;
        z-index: 40;
        animation: doubleTapExpand 0.42s ease-out forwards;
      }
      @keyframes doubleTapExpand {
        0% { transform: scale(0.3); opacity: 1; }
        100% { transform: scale(2.4); opacity: 0; }
      }
`;

if (!html.includes('.front-learned-btn')) {
  const insertStylePos = html.indexOf('</style>');
  html = html.slice(0, insertStylePos) + '\n' + cssToAdd + '\n' + html.slice(insertStylePos);
  console.log('Appended flashcard CSS styles.');
}

// =========================================================================
// 2. UPDATE TOP NAVIGATION HEADER HTML:
//    - Show Learned count out of 200 (NO kitchen & cooking label)
//    - Remove old top learned/delete buttons
//    - Add Reset Deck button
// =========================================================================
const oldHeaderStart = html.indexOf('<header class="flashcard-top-nav">');
const oldHeaderEnd = html.indexOf('</header>', oldHeaderStart) + 9;

if (oldHeaderStart !== -1 && oldHeaderEnd !== -1) {
  const newHeaderHtml = `<header class="flashcard-top-nav">
          <div class="top-nav-main" style="display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 12px 16px;">
            <!-- Back to Subsections -->
            <button class="breadcrumb-back-btn duo-btn-3d" id="btn-breadcrumb-back" title="Back to Subsections" aria-label="Back to Subsections" style="padding: 8px 16px; background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.16); box-shadow: 0 3px 0 rgba(0,0,0,0.4); color: #f1f5f9; font-size: 0.88rem;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="15 18 9 12 15 6"/>
              </svg>
              <span>Back</span>
            </button>
            <!-- Active Deck & Counter: Learned count out of 200 (NO Kitchen & Cooking) -->
            <div class="top-nav-center-group" style="display: flex; align-items: center; gap: 10px;">
              <span class="top-category-pill learned-tier-badge" id="current-category" style="padding: 6px 14px; font-weight: 750; font-size: 0.84rem; border-radius: 9999px; background: rgba(16, 185, 129, 0.16); border: 1.5px solid rgba(16, 185, 129, 0.35); color: #34d399; display: inline-flex; align-items: center; gap: 4px;">
                <span>Learned:</span> <strong id="section-learned-count">0</strong> / <span id="section-total-count">200</span>
              </span>
              <div class="counter-display" style="font-weight: 800; font-size: 0.95rem; color: #f1f5f9; display: flex; align-items: center; gap: 4px;">
                <span class="current-num" id="card-counter-current">800</span>
                <span class="counter-divider" style="color: #64748b;">/</span>
                <span class="total-num" id="card-counter-total" style="color: #94a3b8;">1000</span>
              </div>
            </div>
            <!-- Top Actions: Reset Option & Shuffle (Delete and Learned moved to card front side!) -->
            <div class="top-nav-actions" style="display: flex; align-items: center; gap: 8px;">
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
            </div>
          </div>
          <!-- Single Slim Progress Line -->
          <div class="progress-track" style="height: 3px; background: rgba(255, 255, 255, 0.08); width: 100%; overflow: hidden;">
            <div class="progress-fill" id="progress-fill" style="height: 100%; background: #38bdf8; transition: width 0.3s ease;"></div>
          </div>
        </header>`;
  html = html.slice(0, oldHeaderStart) + newHeaderHtml + html.slice(oldHeaderEnd);
  console.log('Replaced flashcard-top-nav HTML.');
}

// =========================================================================
// 3. UPDATE FRONT SIDE OF CARD:
//    - Add Learned icon ONLY (no label named)
//    - Add Delete icon ONLY (no label named)
// =========================================================================
const frontCardFaceStart = html.indexOf('<div class="card-face card-face-front" id="card-face-front">');
const frontHeaderEnd = html.indexOf('<!-- Front Content:', frontCardFaceStart);

if (frontCardFaceStart !== -1 && frontHeaderEnd !== -1) {
  const newFrontHeaderBar = `<div class="card-face card-face-front" id="card-face-front">
              <div class="card-header-bar" style="display: flex; align-items: center; justify-content: space-between; width: 100%; padding: 4px 6px;">
                <div class="card-num-group">
                  <span class="card-num-tag" id="front-card-num">#800</span>
                </div>
                <div class="card-header-actions" style="display: flex; align-items: center; gap: 8px;">
                  <!-- English Speech Audio -->
                  <button
                    class="icon-tool-btn speak-btn duo-btn-3d"
                    id="front-speak-btn"
                    title="Pronounce word in English"
                    aria-label="Pronounce word"
                  >
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                      <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
                      <path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path>
                    </svg>
                  </button>
                  <!-- Learned Icon ONLY (No label named) -->
                  <button
                    type="button"
                    class="icon-tool-btn front-learned-btn duo-btn-3d"
                    id="front-learned-btn"
                    title="Toggle Learned status"
                    aria-label="Toggle Learned status"
                  >
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                      <polyline points="20 6 9 17 4 12"/>
                    </svg>
                  </button>
                  <!-- Delete Icon ONLY (No label named) -->
                  <button
                    type="button"
                    class="icon-tool-btn front-delete-btn duo-btn-3d"
                    id="front-delete-btn"
                    title="Delete this flashcard (auto-renumbers order)"
                    aria-label="Delete Flashcard"
                  >
                    <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
                      <polyline points="3 6 5 6 21 6"/>
                      <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                      <line x1="10" y1="11" x2="10" y2="17"/>
                      <line x1="14" y1="11" x2="14" y2="17"/>
                    </svg>
                  </button>
                </div>
              </div>
              `;
  html = html.slice(0, frontCardFaceStart) + newFrontHeaderBar + html.slice(frontHeaderEnd);
  console.log('Replaced front card header bar with icons only.');
}

// =========================================================================
// 4. ADD SWIPE SPEED INDICATOR BADGE ELEMENT INSIDE .card-stage IF MISSING
// =========================================================================
if (!html.includes('id="swipe-speed-badge"')) {
  const cardStagePos = html.indexOf('<main class="card-stage">');
  if (cardStagePos !== -1) {
    const badgeHtml = `<main class="card-stage" style="position: relative;">
          <div class="swipe-speed-badge" id="swipe-speed-badge">⚡ <span>Fast Swipe</span></div>`;
    html = html.slice(0, cardStagePos) + badgeHtml + html.slice(cardStagePos + '<main class="card-stage">'.length);
    console.log('Added swipe-speed-badge container.');
  }
}

fs.writeFileSync('index.html', html, 'utf8');
console.log('HTML structure updated successfully. New length:', html.length);
