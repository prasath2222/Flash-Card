const fs = require('fs');

const html = fs.readFileSync('index.html', 'utf8');

// ==========================================================
// 1. EXTRACT & REPOSITION MODALS AND DRAWERS BEFORE <script>
// ==========================================================
const scriptStartTag = '<script>';
const scriptStartIdx = html.indexOf(scriptStartTag);
const scriptEndTag = '</script>';
const scriptEndIdx = html.lastIndexOf(scriptEndTag);

if (scriptStartIdx === -1 || scriptEndIdx === -1) {
  console.error('Script tags missing');
  process.exit(1);
}

// Check if any modals or drawers are still trapped after </script>
const htmlAfterScript = html.slice(scriptEndIdx + scriptEndTag.length);
let modalsTrailing = '';
const backdropMarker = '<div class="menu-drawer-backdrop" id="menu-drawer-backdrop">';
if (htmlAfterScript.includes(backdropMarker)) {
  const bIdx = htmlAfterScript.indexOf(backdropMarker);
  const endBodyIdx = htmlAfterScript.indexOf('</body>');
  if (bIdx !== -1 && endBodyIdx !== -1) {
    modalsTrailing = htmlAfterScript.slice(bIdx, endBodyIdx).trim();
  }
}

// Also check if drawer and modals exist in html before <script>
let updatedHtml = html;
if (modalsTrailing) {
  // Remove from after script
  updatedHtml = updatedHtml.slice(0, scriptEndIdx + scriptEndTag.length) + '\n  </body>\n</html>\n';
  // Insert before script
  const curScriptStart = updatedHtml.indexOf('<script>');
  updatedHtml = updatedHtml.slice(0, curScriptStart) +
    '\n    <!-- APP MODALS & DRAWER -->\n    ' + modalsTrailing + '\n\n    ' +
    updatedHtml.slice(curScriptStart);
}

// Ensure modals like modal-add-section and app-menu-drawer exist in the HTML before <script>
console.log('Modals repositioned. Testing existence:');
console.log('app-menu-drawer exists:', updatedHtml.includes('id="app-menu-drawer"'));
console.log('modal-add-section exists:', updatedHtml.includes('id="modal-add-section"'));

// ==========================================================
// 2. RESTRUCTURE SCREEN-HOME & SCREEN-SUBSECTIONS IN HTML
// ==========================================================
const sHomeStart = updatedHtml.indexOf('<div class="app-screen');
const sFlashcardStart = updatedHtml.indexOf('<div class="app-screen', updatedHtml.indexOf('id="screen-subsections"'));

if (sHomeStart === -1 || sFlashcardStart === -1) {
  console.error('Could not find screen start positions', sHomeStart, sFlashcardStart);
  process.exit(1);
}

const newScreensHtml = `<!-- ========================================== -->
        <!-- SCREEN 1: MODERN HOME SECTIONS VIEW        -->
        <!-- ========================================== -->
        <div class="app-screen active-screen" id="screen-home">
          <!-- Featured 3K Vocabulary Section -->
          <div class="home-main-section-group" style="display: flex; flex-direction: column; gap: 14px;">
            <div class="main-section-header" style="display: flex; flex-direction: column; gap: 4px;">
              <h1 class="main-section-headline" style="font-size: 1.6rem; font-weight: 800; color: #ffffff; letter-spacing: -0.02em; margin: 0;">3k Vocabulary</h1>
              <p class="main-section-subline" style="font-size: 0.9rem; color: #94a3b8; margin: 0;">Master the 3,000 core vocabulary spectrum with native Tamil, Spanish, and Hindi.</p>
            </div>

            <div class="featured-3k-wrapper" id="featured-3k-wrapper">
              <div class="card-3k-featured" id="card-3k-featured" role="button" tabindex="0" aria-label="3k Vocabulary - Open Subsections">
                <!-- Dynamic Specular Reflection Light Sheen -->
                <div class="card-3d-shine" id="card-3k-shine"></div>
                <div class="card-3k-layout">
                  <!-- Left Info Column -->
                  <div class="card-3k-info-col">
                    <h2 class="card-3k-title" id="label-3k-vocabulary">3k Vocabulary</h2>
                    
                    <p class="card-3k-desc">
                      Comprehensive 3,000-word trilingual spectrum. Master everyday English, authentic native Tamil script, Spanish, and Hindi with verified HD imagery and audio pronunciation.
                    </p>

                    <!-- Real-time Status 1 to 3K Metric -->
                    <div class="card-3k-progress-box">
                      <div class="progress-meta-row">
                        <span>Overall Mastery: <strong id="card-3k-learned-count">0</strong> / 3,000 Learned</span>
                        <span id="card-3k-learned-pct" style="color: #38bdf8; font-weight: 800;">0%</span>
                      </div>
                      <div class="progress-track-3k">
                        <div class="progress-fill-3k" id="progress-fill-3k-total" style="width: 0%;"></div>
                      </div>
                      <div class="progress-tier-hint" style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #94a3b8; margin-top: 4px;">
                        <span>Active Focus: <strong>Cards 800 – 1000</strong></span>
                        <span id="tier-800-learned-stat">0 / 200 in active tier</span>
                      </div>
                    </div>

                    <!-- Open Subsections Resume Button (Duolingo 3D Tactile) -->
                    <div class="card-3k-actions" style="margin-top: 16px;">
                      <button type="button" class="duo-btn-3d duo-btn-3d-green" id="btn-open-subsections" title="Resume 3k Vocabulary Subsections" style="width: 100%; padding: 14px 24px; font-size: 1rem;">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                          <polygon points="5 3 19 12 5 21 5 3"></polygon>
                        </svg>
                        <span>Resume</span>
                      </button>
                    </div>
                  </div>

                  <!-- Right 3D Layered Mini-Cards Stack -->
                  <div class="card-3k-visual-col" aria-hidden="true">
                    <div class="floating-card-stack" id="floating-card-stack">
                      <div class="mini-deck-card mini-card-3">
                        <div class="mini-card-header">
                          <span>#802</span>
                          <span>SINK</span>
                        </div>
                        <div class="mini-card-word">SINK</div>
                        <div class="mini-card-trans">fregadero · தொட்டி</div>
                      </div>
                      <div class="mini-deck-card mini-card-2">
                        <div class="mini-card-header">
                          <span>#801</span>
                          <span>OVEN</span>
                        </div>
                        <div class="mini-card-word">OVEN</div>
                        <div class="mini-card-trans">horno · அடுமனை</div>
                      </div>
                      <div class="mini-deck-card mini-card-1">
                        <div class="mini-card-header">
                          <span>#800</span>
                          <span>STOVE</span>
                        </div>
                        <div class="mini-card-word">STOVE</div>
                        <div class="mini-card-trans">estufa · அடுப்பு</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- User Created Sections Grid (Clean: populated ONLY when user adds custom sections, NO 'Custom Sections' label) -->
          <div class="sections-grid" id="sections-grid" style="margin-top: 14px;"></div>

          <!-- Centered Duolingo-style 3D Add Section Button -->
          <div class="duo-add-section-wrapper">
            <button type="button" class="duo-btn-add-section" id="btn-open-add-section" title="Add a custom section">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">
                <line x1="12" y1="5" x2="12" y2="19"/>
                <line x1="5" y1="12" x2="19" y2="12"/>
              </svg>
              <span>Add Section</span>
            </button>
          </div>
        </div>

        <!-- ========================================== -->
        <!-- SCREEN 2: DECK SUB-SECTIONS VIEW            -->
        <!-- ========================================== -->
        <div class="app-screen" id="screen-subsections">
          <!-- Top Bar with Back to Home -->
          <div class="subsections-top-bar" style="display: flex; align-items: center; justify-content: space-between; padding: 12px 0 16px; border-bottom: 1px solid rgba(255, 255, 255, 0.08); margin-bottom: 18px; flex-wrap: wrap; gap: 12px;">
            <button type="button" class="breadcrumb-back-btn duo-btn-3d" id="btn-back-to-home" title="Back to Home" style="padding: 9px 18px; background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.18); box-shadow: 0 4px 0 rgba(0,0,0,0.45); color: #f1f5f9; font-size: 0.9rem;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="15 18 9 12 15 6"/>
              </svg>
              <span>Back to Home</span>
            </button>
            <span style="font-size: 1.15rem; font-weight: 800; color: #ffffff;">3k Vocabulary Subsections</span>
            <div class="stat-badge-duo stat-badge-mastery" style="padding: 6px 14px; background: rgba(56, 189, 248, 0.12); border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 12px; color: #38bdf8; font-weight: 700; font-size: 0.85rem;">
              <span>Status: <strong id="subsections-3k-total" style="color: #ffffff;">0</strong> / 3,000</span>
            </div>
          </div>

          <!-- ONLY ONE TIER: Cards 800 – 1000 Featured Card (No other down shits!) -->
          <div class="tier-800-featured-card" id="sub-tier-800-1000" role="button" tabindex="0" style="background: linear-gradient(135deg, rgba(2, 132, 199, 0.24), rgba(16, 185, 129, 0.15)); border: 2px solid rgba(56, 189, 248, 0.45); box-shadow: 0 10px 30px rgba(2, 132, 199, 0.18), 0 5px 0 #0369a1; border-radius: 24px; padding: 26px 28px; cursor: pointer; transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px;">
              <div style="display: flex; align-items: center; gap: 16px;">
                <span style="display: flex; align-items: center; justify-content: center; width: 56px; height: 56px; border-radius: 18px; background: rgba(255, 255, 255, 0.12); font-size: 1.8rem; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.25);">🔥</span>
                <div>
                  <div style="font-size: 0.76rem; font-weight: 800; letter-spacing: 0.08em; color: #38bdf8; text-transform: uppercase;">Active Recommended Tier</div>
                  <h3 style="font-size: 1.4rem; font-weight: 800; color: #ffffff; margin: 3px 0 5px;">Cards 800 – 1000 (Active)</h3>
                  <div style="font-size: 0.88rem; color: #cbd5e1;">Kitchen, Dining, Appliances & Daily Life · 200 Words</div>
                </div>
              </div>
              <button type="button" class="duo-btn-3d duo-btn-3d-green" id="btn-resume-from-subsections" style="padding: 13px 26px; font-size: 0.95rem;">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                  <polygon points="5 3 19 12 5 21 5 3"></polygon>
                </svg>
                <span>Study Deck Now</span>
              </button>
            </div>
            <div style="margin-top: 18px; padding-top: 16px; border-top: 1px solid rgba(255, 255, 255, 0.1); display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
              <div style="font-size: 0.84rem; color: #94a3b8;">
                STOVE, OVEN, SINK, REFRIGERATOR, KETTLE... With trilingual translations & HD photos.
              </div>
              <div style="display: flex; align-items: center; gap: 10px;">
                <span id="tier-800-stat-line" style="font-size: 0.85rem; font-weight: 700; color: #38bdf8;">0 / 200 Learned</span>
                <div style="width: 120px; height: 8px; background: rgba(255, 255, 255, 0.1); border-radius: 9999px; overflow: hidden;">
                  <div id="tier-800-progress-bar" style="width: 0%; height: 100%; background: #38bdf8; border-radius: 9999px;"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- Centered Duolingo-style 3D Add Section Button (Both Main & Subsection have it centered!) -->
          <div class="duo-add-section-wrapper" style="margin-top: 36px;">
            <button type="button" class="duo-btn-add-section" id="btn-subsections-add-section" title="Add a custom section">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">
                <line x1="12" y1="5" x2="12" y2="19"/>
                <line x1="5" y1="12" x2="19" y2="12"/>
              </svg>
              <span>Add Section</span>
            </button>
          </div>
        </div>

        `;

updatedHtml = updatedHtml.slice(0, sHomeStart) + newScreensHtml + updatedHtml.slice(sFlashcardStart);
console.log('Updated HTML screens. Length:', updatedHtml.length);

// ==========================================================
// 3. REVISE SCREEN-FLASHCARD (Top bar cleanly aligned, no "Tap to flip back" labels, shortcuts stacked vertically)
// ==========================================================
// Check and update top-nav and card-wrapper in screen-flashcard
// Update breadcrumb back button text and alignment
const flashcardNavOld = updatedHtml.slice(updatedHtml.indexOf('<header class="flashcard-top-nav">'), updatedHtml.indexOf('</header>', updatedHtml.indexOf('<header class="flashcard-top-nav">')) + 9);
const flashcardNavNew = `<header class="flashcard-top-nav">
          <div class="top-nav-main" style="display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 12px 16px;">
            <!-- Back to Subsections -->
            <button class="breadcrumb-back-btn duo-btn-3d" id="btn-breadcrumb-back" title="Back to Subsections" aria-label="Back to Subsections" style="padding: 8px 16px; background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.16); box-shadow: 0 3px 0 rgba(0,0,0,0.4); color: #f1f5f9; font-size: 0.88rem;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="15 18 9 12 15 6"/>
              </svg>
              <span>Back</span>
            </button>
            <!-- Active Deck & Counter -->
            <div class="top-nav-center-group" style="display: flex; align-items: center; gap: 10px;">
              <span class="top-category-pill" id="current-category" style="padding: 6px 14px; font-weight: 700; font-size: 0.84rem; border-radius: 9999px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12);">Kitchen & Cooking</span>
              <div class="counter-display" style="font-weight: 800; font-size: 0.95rem; color: #f1f5f9; display: flex; align-items: center; gap: 4px;">
                <span class="current-num" id="card-counter-current">800</span>
                <span class="counter-divider" style="color: #64748b;">/</span>
                <span class="total-num" id="card-counter-total" style="color: #94a3b8;">1000</span>
              </div>
            </div>
            <!-- Learned Toggle & Shuffle -->
            <div class="top-nav-actions" style="display: flex; align-items: center; gap: 8px;">
              <button type="button" class="btn-top-learned-toggle duo-btn-3d" id="btn-top-learned-toggle" title="Mark as Learned" aria-label="Mark Card as Learned" style="padding: 7px 14px; border-radius: 12px; font-size: 0.82rem; font-weight: 700;">
                <span class="learned-check-indicator">✓</span>
                <span class="learned-status-text">Learned</span>
              </button>
              <button class="shuffle-btn duo-btn-3d" id="btn-shuffle" title="Shuffle cards" aria-label="Shuffle cards" style="width: 38px; height: 38px; border-radius: 12px; display: flex; align-items: center; justify-content: center; background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.16); box-shadow: 0 3px 0 rgba(0,0,0,0.4); color: #f1f5f9;">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M2 18h1.4c1.3 0 2.5-.6 3.3-1.7l6.6-8.6c.8-1.1 2-1.7 3.3-1.7H22" />
                  <path d="m18 2 4 4-4 4" />
                  <path d="M2 6h1.4c1.3 0 2.5.6 3.3 1.7l2 2.6" />
                  <path d="M14.6 13.7l2.1 2.6c.8 1.1 2 1.7 3.3 1.7H22" />
                  <path d="m18 20 4-4-4-4" />
                </svg>
              </button>
            </div>
          </div>
          <!-- Single Slim Progress Line -->
          <div class="progress-track" style="height: 3px; background: rgba(255, 255, 255, 0.08); width: 100%; overflow: hidden;">
            <div class="progress-fill" id="progress-fill" style="height: 100%; background: #38bdf8; transition: width 0.3s ease;"></div>
          </div>
        </header>`;

if (updatedHtml.includes('<header class="flashcard-top-nav">')) {
  updatedHtml = updatedHtml.replace(flashcardNavOld, flashcardNavNew);
}

// Remove any unwanted labels like "Tap card to flip back" or "aria-label=\"Flashcard - Tap to flip\""
updatedHtml = updatedHtml.replace(/aria-label="Flashcard - Tap to flip"/g, 'aria-label="Vocabulary Flashcard"');

// ==========================================================
// 4. DUOLINGO 3D CSS & UNIVERSAL SCROLLING OVERHAUL
// ==========================================================
const styleEndTag = '</style>';
const styleEndIdx = updatedHtml.lastIndexOf(styleEndTag);
if (styleEndIdx === -1) {
  console.error('</style> tag missing');
  process.exit(1);
}

const comprehensiveDuolingoAndScrollCss = `
      /* ==========================================================
         CRITICAL SCROLLING & DUOLINGO 3D STYLING CONSTITUTION
         ========================================================== */
      html, body {
        width: 100% !important;
        min-height: 100% !important;
        height: auto !important;
        margin: 0 !important;
        padding: 0 !important;
        background: #070a13 !important;
        color: #f8fafc !important;
        overflow-x: hidden !important;
        overflow-y: auto !important;
        -webkit-overflow-scrolling: touch !important;
        touch-action: pan-y !important;
      }

      body.home-view-active,
      body.in-flashcard-mode {
        overflow-y: auto !important;
        height: auto !important;
      }

      #app-container {
        width: 100% !important;
        max-width: 100% !important;
        min-height: 100vh !important;
        height: auto !important;
        margin: 0 !important;
        padding: 0 !important;
        display: flex !important;
        flex-direction: row !important;
        background: #070a13 !important;
        position: relative !important;
        overflow: visible !important;
      }

      .app-main-viewport {
        flex: 1 1 auto !important;
        margin-left: var(--sidebar-width) !important;
        min-height: 100vh !important;
        height: auto !important;
        width: calc(100% - var(--sidebar-width)) !important;
        display: flex !important;
        flex-direction: column !important;
        position: relative !important;
        overflow-y: auto !important;
        overflow-x: hidden !important;
        -webkit-overflow-scrolling: touch !important;
        touch-action: pan-y !important;
      }

      @media (max-width: 900px) {
        .app-main-viewport {
          margin-left: 0 !important;
          width: 100% !important;
          padding-bottom: 78px !important;
          overflow-y: auto !important;
          height: auto !important;
          min-height: 100vh !important;
        }
      }

      .app-screen {
        width: 100% !important;
        max-width: 1080px !important;
        margin: 0 auto !important;
        padding: 24px 28px 60px !important;
        display: none;
        flex-direction: column !important;
        gap: 24px !important;
        flex: 1 0 auto !important;
        min-height: 100% !important;
        height: auto !important;
        overflow-y: visible !important;
        overflow-x: hidden !important;
        box-sizing: border-box !important;
      }

      .app-screen.active-screen {
        display: flex !important;
      }

      @media (max-width: 900px) {
        .app-screen {
          padding: 16px 16px 90px !important;
          gap: 18px !important;
        }
      }

      #screen-flashcard {
        width: 100% !important;
        max-width: 600px !important;
        margin: 0 auto !important;
        min-height: calc(100vh - 20px) !important;
        height: auto !important;
        display: none;
        flex-direction: column !important;
        justify-content: space-between !important;
        overflow-y: auto !important;
        overflow-x: hidden !important;
        padding: 10px 14px 24px !important;
      }

      #screen-flashcard.active-screen {
        display: flex !important;
      }

      /* DUOLINGO 3D TACTILE BUTTONS & CARDS */
      .duo-btn-3d {
        position: relative !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 10px !important;
        border-radius: 16px !important;
        font-weight: 800 !important;
        letter-spacing: 0.04em !important;
        text-transform: uppercase !important;
        cursor: pointer !important;
        user-select: none !important;
        transition: transform 0.12s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.12s cubic-bezier(0.34, 1.56, 0.64, 1), background-color 0.15s ease !important;
        will-change: transform, box-shadow !important;
        border: none !important;
        outline: none !important;
      }

      .duo-btn-3d-green {
        background: #22c55e !important;
        color: #ffffff !important;
        box-shadow: 0 5px 0 #15803d, 0 8px 18px rgba(34, 197, 94, 0.35) !important;
      }

      .duo-btn-3d-green:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 7px 0 #15803d, 0 12px 22px rgba(34, 197, 94, 0.45) !important;
      }

      .duo-btn-3d-green:active {
        transform: translateY(4px) !important;
        box-shadow: 0 1px 0 #15803d, 0 3px 8px rgba(34, 197, 94, 0.25) !important;
      }

      .duo-btn-3d-blue {
        background: #0284c7 !important;
        color: #ffffff !important;
        box-shadow: 0 5px 0 #0369a1, 0 8px 18px rgba(2, 132, 199, 0.35) !important;
      }

      .duo-btn-3d-blue:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 7px 0 #0369a1, 0 12px 22px rgba(2, 132, 199, 0.45) !important;
      }

      .duo-btn-3d-blue:active {
        transform: translateY(4px) !important;
        box-shadow: 0 1px 0 #0369a1, 0 3px 8px rgba(2, 132, 199, 0.25) !important;
      }

      /* Centered Duolingo Add Section Button */
      .duo-add-section-wrapper {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
        margin: 28px 0 20px !important;
      }

      .duo-btn-add-section {
        width: 100% !important;
        max-width: 440px !important;
        padding: 16px 28px !important;
        font-size: 1.05rem !important;
        border-radius: 20px !important;
        background: linear-gradient(180deg, #1e293b, #0f172a) !important;
        color: #38bdf8 !important;
        border: 2px solid rgba(56, 189, 248, 0.35) !important;
        box-shadow: 0 6px 0 #090e1a, 0 10px 24px rgba(0, 0, 0, 0.5) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 12px !important;
        font-weight: 800 !important;
        letter-spacing: 0.03em !important;
        cursor: pointer !important;
        transition: transform 0.12s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.12s cubic-bezier(0.34, 1.56, 0.64, 1), border-color 0.2s ease !important;
      }

      .duo-btn-add-section:hover {
        transform: translateY(-2px) !important;
        border-color: #38bdf8 !important;
        color: #ffffff !important;
        box-shadow: 0 8px 0 #090e1a, 0 14px 28px rgba(56, 189, 248, 0.25) !important;
      }

      .duo-btn-add-section:active {
        transform: translateY(4px) !important;
        box-shadow: 0 1px 0 #090e1a, 0 4px 10px rgba(0, 0, 0, 0.3) !important;
      }

      /* Stacked Shortcut Memory Section (Spanish top, Hindi bottom, generously padded) */
      .shortcut-section {
        margin-top: 14px !important;
        width: 100% !important;
      }

      .shortcut-grid {
        display: flex !important;
        flex-direction: column !important;
        gap: 10px !important;
        width: 100% !important;
      }

      .shortcut-box {
        display: flex !important;
        flex-direction: column !important;
        gap: 5px !important;
        padding: 10px 14px !important;
        border-radius: 12px !important;
        background: rgba(255, 255, 255, 0.035) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        width: 100% !important;
        box-sizing: border-box !important;
      }

      /* Modal & Drawer strict pointer-events and display discipline */
      .modal-backdrop:not(.open) {
        display: none !important;
        opacity: 0 !important;
        pointer-events: none !important;
      }
      .modal-backdrop.open {
        display: flex !important;
        opacity: 1 !important;
        pointer-events: auto !important;
        z-index: 1000 !important;
      }

      .menu-drawer-backdrop:not(.open) {
        display: none !important;
        opacity: 0 !important;
        pointer-events: none !important;
      }
      .menu-drawer-backdrop.open {
        display: block !important;
        opacity: 1 !important;
        pointer-events: auto !important;
        z-index: 998 !important;
      }

      .app-menu-drawer:not(.open) {
        transform: translateX(-100%) !important;
        pointer-events: none !important;
      }
      .app-menu-drawer.open {
        transform: translateX(0) !important;
        pointer-events: auto !important;
        z-index: 999 !important;
      }
    `;

updatedHtml = updatedHtml.slice(0, styleEndIdx) + comprehensiveDuolingoAndScrollCss + updatedHtml.slice(styleEndIdx);

// ==========================================================
// 5. JAVASCRIPT LOGIC REFINEMENT & EVENT WIRES
// ==========================================================
const sScriptStart = updatedHtml.indexOf('<script>');
const sScriptEnd = updatedHtml.lastIndexOf('</script>');
let script = updatedHtml.slice(sScriptStart + '<script>'.length, sScriptEnd);

// A. Place var learnedCardsSet definition at the top of script to avoid TDZ ReferenceError
const safeStatePreamble = `
      // TOP-LEVEL SAFE INITIALIZATION FOR LEARNED TRACKER & GLOBAL STATE
      var LEARNED_STORAGE_KEY = "vocab_learned_cards_v3";
      var LAST_CARD_STORAGE_KEY = "vocab_last_card_v3";
      function loadLearnedCards() {
        try {
          var raw = localStorage.getItem(LEARNED_STORAGE_KEY);
          if (raw) {
            var arr = JSON.parse(raw);
            return new Set(arr);
          }
        } catch (e) {
          console.error("Could not load learned cards:", e);
        }
        return new Set();
      }
      var learnedCardsSet = loadLearnedCards();
`;

// Insert safeStatePreamble right at the beginning of <script>
script = safeStatePreamble + '\n' + script;

// Guard updateCardLearnedUI against early calls
script = script.replace(
  /function updateCardLearnedUI\(cardNum\)\s*\{/g,
  'function updateCardLearnedUI(cardNum) { if (!cardNum || !learnedCardsSet || typeof learnedCardsSet.has !== "function") return;'
);

// Empty defaultSections array so no fake dummy sections show up
script = script.replace(
  /const defaultSections\s*=\s*\[[\s\S]*?\];/g,
  'const defaultSections = [];'
);

// Ensure loadCustomSections cleans out any old dummy sections
script = script.replace(
  /function loadCustomSections\(\)\s*\{[\s\S]*?return defaultSections;[\s\S]*?\}/,
  `function loadCustomSections() {
    try {
      const raw = localStorage.getItem(SECTIONS_STORAGE_KEY);
      if (raw) {
        const parsed = JSON.parse(raw);
        // Filter out dummy sections
        const cleaned = parsed.filter(s => s && s.id && !s.id.startsWith("sec_daily") && !s.id.startsWith("sec_travel") && !s.id.startsWith("sec_food") && !s.id.startsWith("sec_career"));
        return cleaned;
      }
    } catch (e) {
      console.error("Error loading custom sections:", e);
    }
    return [];
  }`
);

// Navigation handlers update
const navHooksCode = `
      // ==========================================================
      // MASTER NAVIGATION & SCREEN ROUTING ARCHITECTURE
      // Flow: Home (3k Vocab) ---> Subsections (800 - 1000) ---> Flashcards
      // ==========================================================
      function initMasterNavigationRouting() {
        // 1. Home Screen 3k Vocab Card & Resume button -> Subsections
        const card3k = document.getElementById("card-3k-featured");
        const btnOpenSub = document.getElementById("btn-open-subsections");
        if (card3k) {
          card3k.addEventListener("click", (e) => {
            if (e.target.closest("button")) return;
            switchScreen("screen-subsections");
            playHapticTick(540, "sine", 0.04);
          });
        }
        if (btnOpenSub) {
          btnOpenSub.addEventListener("click", (e) => {
            e.stopPropagation();
            switchScreen("screen-subsections");
            playHapticTick(600, "triangle", 0.05);
          });
        }

        // 2. Subsections Screen: Back to Home
        const btnBackHome = document.getElementById("btn-back-to-home");
        if (btnBackHome) {
          btnBackHome.addEventListener("click", () => {
            switchScreen("screen-home");
            playHapticTick(440, "sine", 0.04);
          });
        }

        // 3. Subsections Screen: Cards 800 - 1000 card & Study button -> Flashcards
        const subTier800 = document.getElementById("sub-tier-800-1000");
        const btnResumeFromSub = document.getElementById("btn-resume-from-subsections");
        function launchDeck800() {
          const lastNum = getLastCardNumber() || 800;
          const targetIndex = cards.findIndex(c => c.num === lastNum);
          currentIndex = targetIndex !== -1 ? targetIndex : 0;
          switchScreen("screen-flashcard");
          renderCurrentCard();
          playHapticTick(680, "triangle", 0.05);
        }
        if (subTier800) {
          subTier800.addEventListener("click", (e) => {
            if (e.target.closest("button")) return;
            launchDeck800();
          });
        }
        if (btnResumeFromSub) {
          btnResumeFromSub.addEventListener("click", (e) => {
            e.stopPropagation();
            launchDeck800();
          });
        }

        // 4. Flashcard Screen: Breadcrumb back -> Subsections
        const btnBreadcrumbBack = document.getElementById("btn-breadcrumb-back");
        if (btnBreadcrumbBack) {
          btnBreadcrumbBack.addEventListener("click", () => {
            switchScreen("screen-subsections");
            playHapticTick(440, "sine", 0.04);
          });
        }

        // 5. Add Section Buttons (Home & Subsections) -> Modal Add Section
        const btnOpenAddHome = document.getElementById("btn-open-add-section");
        const btnOpenAddSub = document.getElementById("btn-subsections-add-section");
        function openAddSectionModal() {
          const modal = document.getElementById("modal-add-section");
          if (modal) {
            modal.classList.add("open");
            const input = document.getElementById("input-section-title");
            if (input) setTimeout(() => input.focus(), 80);
          }
          playHapticTick(500, "sine", 0.04);
        }
        if (btnOpenAddHome) btnOpenAddHome.addEventListener("click", openAddSectionModal);
        if (btnOpenAddSub) btnOpenAddSub.addEventListener("click", openAddSectionModal);

        // Close Add Section Modal
        const btnCloseAdd = document.getElementById("btn-close-add-section");
        const btnCancelAdd = document.getElementById("btn-cancel-add-section");
        const modalAdd = document.getElementById("modal-add-section");
        function closeAddSectionModal() {
          if (modalAdd) modalAdd.classList.remove("open");
        }
        if (btnCloseAdd) btnCloseAdd.addEventListener("click", closeAddSectionModal);
        if (btnCancelAdd) btnCancelAdd.addEventListener("click", closeAddSectionModal);
        if (modalAdd) {
          modalAdd.addEventListener("click", (e) => {
            if (e.target === modalAdd) closeAddSectionModal();
          });
        }

        // Save New Section Handler
        const btnSaveNew = document.getElementById("btn-save-new-section");
        if (btnSaveNew) {
          btnSaveNew.addEventListener("click", () => {
            const titleInput = document.getElementById("input-section-title");
            const subInput = document.getElementById("input-section-sub");
            const title = titleInput ? titleInput.value.trim() : "";
            const sub = subInput ? subInput.value.trim() : "";
            if (!title) {
              showToast("Please enter a section title");
              if (titleInput) titleInput.focus();
              return;
            }
            const newSec = {
              id: "sec_" + Date.now(),
              title: title,
              sub: sub || "Custom vocabulary set",
              count: 50,
              progress: 0,
              color: "#38bdf8",
              icon: "📚"
            };
            customSections.push(newSec);
            saveCustomSections();
            renderCustomSections();
            closeAddSectionModal();
            if (titleInput) titleInput.value = "";
            if (subInput) subInput.value = "";
            showToast("Created section: " + title);
          });
        }

        // 6. Settings Buttons (Desktop Sidebar & Mobile Header/Bar)
        const allSettingsTriggers = [
          document.getElementById("nav-btn-settings"),
          document.getElementById("sidebar-btn-settings"),
          document.getElementById("mob-tab-settings"),
          document.getElementById("mobile-hamburger-btn"),
          document.getElementById("btn-top-settings"),
          document.getElementById("btn-desktop-open-settings")
        ];
        allSettingsTriggers.forEach(btn => {
          if (btn) btn.addEventListener("click", openMenuDrawer);
        });

        // Sidebar and Drawer navigation links
        const navHome = document.getElementById("nav-btn-home");
        if (navHome) navHome.addEventListener("click", () => switchScreen("screen-home"));
        const nav3k = document.getElementById("nav-btn-3k");
        if (nav3k) nav3k.addEventListener("click", () => switchScreen("screen-subsections"));
        const mobHome = document.getElementById("mob-tab-home");
        if (mobHome) mobHome.addEventListener("click", () => switchScreen("screen-home"));
        const mob3k = document.getElementById("mob-tab-3k");
        if (mob3k) mob3k.addEventListener("click", () => switchScreen("screen-subsections"));
      }

      if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initMasterNavigationRouting);
      } else {
        initMasterNavigationRouting();
      }
`;

// Append navHooksCode to script
script += '\n' + navHooksCode;

updatedHtml = updatedHtml.slice(0, sScriptStart + '<script>'.length) + script + updatedHtml.slice(sScriptEnd);

fs.writeFileSync('index.html', updatedHtml, 'utf8');
console.log('Successfully wrote updated index.html! File length:', updatedHtml.length);
