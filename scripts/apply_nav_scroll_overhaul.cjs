const fs = require('fs');

const html = fs.readFileSync('index.html', 'utf8');

// 1. Find the elements after </script>
const scriptEndTag = '</script>';
const scriptEndIdx = html.indexOf(scriptEndTag);
if (scriptEndIdx === -1) {
  console.error('</script> tag not found!');
  process.exit(1);
}

const htmlAfterScript = html.slice(scriptEndIdx + scriptEndTag.length);
console.log('Length of HTML after </script>:', htmlAfterScript.length);

// Extract the modals and drawers that were mistakenly placed after </script>
// Everything from the start of menu-drawer-backdrop until before </body>
const backdropMarker = '<div class="menu-drawer-backdrop" id="menu-drawer-backdrop"></div>';
const backdropIdx = htmlAfterScript.indexOf(backdropMarker);
const bodyCloseIdx = htmlAfterScript.indexOf('</body>');

if (backdropIdx === -1 || bodyCloseIdx === -1) {
  console.error('Could not find backdropMarker or </body> in htmlAfterScript:', backdropIdx, bodyCloseIdx);
  process.exit(1);
}

const modalsAndDrawersHtml = htmlAfterScript.slice(backdropIdx, bodyCloseIdx).trim();
console.log('Extracted modalsAndDrawersHtml length:', modalsAndDrawersHtml.length);

// Clean htmlAfterScript to just be \n  </body>\n</html>
const cleanHtmlAfterScript = '\n  </body>\n</html>\n';

// 2. Remove the trailing modals from after </script>
let updatedHtml = html.slice(0, scriptEndIdx + scriptEndTag.length) + cleanHtmlAfterScript;

// 3. Insert modalsAndDrawersHtml BEFORE <script>
const scriptStartTag = '<script>';
const scriptStartIdx = updatedHtml.indexOf(scriptStartTag);
if (scriptStartIdx === -1) {
  console.error('<script> tag not found!');
  process.exit(1);
}

// Place before <script>
updatedHtml = updatedHtml.slice(0, scriptStartIdx) +
  '\n    <!-- ========================================================== -->\n' +
  '    <!-- APP MODALS & SLIDE-OVER SETTINGS DRAWER                    -->\n' +
  '    <!-- ========================================================== -->\n' +
  '    ' + modalsAndDrawersHtml + '\n\n    ' +
  updatedHtml.slice(scriptStartIdx);

console.log('Inserted modals and drawers before <script>. New length:', updatedHtml.length);

// 4. Update the Home Screen HTML
// Find screen-home block
const homeStartMarker = '<div class="app-screen active-screen" id="screen-home">';
const subsectionsStartMarker = '<!-- SCREEN 2: DECK SUB-SECTIONS VIEW';
const homeStartPos = updatedHtml.indexOf(homeStartMarker);
const subStartPos = updatedHtml.indexOf(subsectionsStartMarker);

if (homeStartPos === -1 || subStartPos === -1) {
  console.error('Could not find homeStartMarker or subsectionsStartMarker!', homeStartPos, subStartPos);
  process.exit(1);
}

const newScreenHomeHtml = `<div class="app-screen active-screen" id="screen-home">
          <!-- ==================================================== -->
          <!-- FEATURED 3K VOCABULARY SECTION (Interactive 3D Card) -->
          <!-- ==================================================== -->
          <div class="home-main-section-group" style="display: flex; flex-direction: column; gap: 14px;">
            <div class="main-section-header" style="display: flex; flex-direction: column; gap: 4px;">
              <h1 class="main-section-headline" style="font-size: 1.6rem; font-weight: 800; color: #ffffff; letter-spacing: -0.02em; margin: 0;">Learning Sections</h1>
              <p class="main-section-subline" style="font-size: 0.9rem; color: #94a3b8; margin: 0;">Master the 3,000 core vocabulary spectrum or build custom study tracks below.</p>
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

                    <!-- Open Subsections Primary Button -->
                    <div class="card-3k-actions" style="margin-top: 14px;">
                      <button type="button" class="btn-subsections-3k" id="btn-open-subsections" title="View 3,000 vocabulary subsections (800 – 1000)" style="width: 100%; justify-content: center; padding: 12px 20px; font-size: 0.95rem; font-weight: 700;">
                        <span>Explore Subsections (800 – 1000)</span>
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
                          <polyline points="9 18 15 12 9 6"/>
                        </svg>
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

          <!-- ==================================================== -->
          <!-- CUSTOM SECTIONS AREA (Right below 3k Vocab)          -->
          <!-- ==================================================== -->
          <div class="home-add-section-area" style="margin-top: 10px;">
            <div class="sections-container-header" style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
              <div class="sections-heading-group">
                <h3 class="sections-main-heading" style="font-size: 1.15rem; font-weight: 800; color: #ffffff; margin: 0;">Custom Sections</h3>
                <span style="font-size: 0.85rem; color: #94a3b8;" id="sections-count-pill">0 Decks</span>
              </div>
              <button type="button" class="btn-create-section-pill" id="btn-open-add-section" title="Create a custom study section">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="12" y1="5" x2="12" y2="19"/>
                  <line x1="5" y1="12" x2="19" y2="12"/>
                </svg>
                <span>Add Section</span>
              </button>
            </div>

            <!-- Draggable & Movable Sections Grid (Clean: populated only when user adds sections!) -->
            <div class="sections-grid" id="sections-grid">
              <!-- Dynamically populated from localStorage -->
            </div>

            <!-- Empty State / Add Section Prompt below 3k Vocab -->
            <div class="empty-custom-sections" id="empty-custom-sections" style="display: none; margin-top: 6px;">
              <button type="button" class="btn-empty-add-section-card" id="btn-empty-add-section" title="Add a custom section">
                <div class="empty-add-icon">
                  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="12" y1="5" x2="12" y2="19"/>
                    <line x1="5" y1="12" x2="19" y2="12"/>
                  </svg>
                </div>
                <div class="empty-add-text">
                  <div class="empty-add-title">Add Section</div>
                  <div class="empty-add-sub">Create your own custom vocabulary topic or word list</div>
                </div>
              </button>
            </div>
          </div>
        </div>

        `;

updatedHtml = updatedHtml.slice(0, homeStartPos) + newScreenHomeHtml + updatedHtml.slice(subStartPos);
console.log('Replaced screen-home HTML. New length:', updatedHtml.length);

// 5. Inject comprehensive CSS fixes for scrolling, modal displays, and empty section card
const cssMarker = '</style>';
const cssIdx = updatedHtml.indexOf(cssMarker);
if (cssIdx === -1) {
  console.error('</style> not found!');
  process.exit(1);
}

const customCssFix = `
      /* ==========================================================
         CRITICAL SCROLLING & ACCESSIBILITY SYSTEM OVERHAUL
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
        padding: 10px 14px 20px !important;
      }

      #screen-flashcard.active-screen {
        display: flex !important;
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
      }

      .app-menu-drawer:not(.open) {
        transform: translateX(-100%) !important;
        pointer-events: none !important;
      }
      .app-menu-drawer.open {
        transform: translateX(0) !important;
        pointer-events: auto !important;
      }

      /* Empty Add Section button card */
      .btn-empty-add-section-card {
        width: 100%;
        background: rgba(255, 255, 255, 0.02);
        border: 1.5px dashed rgba(255, 255, 255, 0.16);
        border-radius: 18px;
        padding: 18px 22px;
        display: flex;
        align-items: center;
        gap: 16px;
        color: #94a3b8;
        cursor: pointer;
        transition: all 0.2s ease;
        text-align: left;
      }
      .btn-empty-add-section-card:hover {
        background: rgba(56, 189, 248, 0.06);
        border-color: rgba(56, 189, 248, 0.45);
        color: #ffffff;
        transform: translateY(-2px);
      }
      .empty-add-icon {
        width: 44px;
        height: 44px;
        border-radius: 14px;
        background: rgba(56, 189, 248, 0.12);
        border: 1px solid rgba(56, 189, 248, 0.28);
        color: #38bdf8;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
      }
      .empty-add-text {
        display: flex;
        flex-direction: column;
        gap: 3px;
      }
      .empty-add-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #f1f5f9;
      }
      .empty-add-sub {
        font-size: 0.8rem;
        color: #94a3b8;
      }
    `;

updatedHtml = updatedHtml.slice(0, cssIdx) + customCssFix + updatedHtml.slice(cssIdx);
console.log('Appended custom CSS fixes. New length:', updatedHtml.length);

// 6. Update JavaScript Logic
// - Change defaultSections = []
// - Update loadCustomSections to purge old fake dummy sections
// - Wire 3k card and buttons to STRICTLY open screen-subsections
// - Wire empty add section button
// - Fix all settings & drawer click hooks
const scriptStartPos = updatedHtml.indexOf('<script>');
let scriptCode = updatedHtml.slice(scriptStartPos + '<script>'.length, updatedHtml.indexOf('</script>', scriptStartPos));

// Replace defaultSections definition
const oldDefaultSec = `const defaultSections = [
        {
          id: "sec_daily",
          title: "Daily Essentials",
          sub: "Conversational & Everyday Idioms",
          count: 350,
          progress: 100,
          color: "#10b981",
          icon: "🗣️"
        },
        {
          id: "sec_travel",
          title: "Travel & Airport",
          sub: "Transit, Flights, Hotel & City Signs",
          count: 180,
          progress: 45,
          color: "#38bdf8",
          icon: "✈️"
        },
        {
          id: "sec_food",
          title: "Food & Dining",
          sub: "Restaurants, Kitchenware & Recipes",
          count: 240,
          progress: 60,
          color: "#f59e0b",
          icon: "🍳"
        },
        {
          id: "sec_career",
          title: "Workplace & Career",
          sub: "Office, Meetings & Technology",
          count: 190,
          progress: 25,
          color: "#818cf8",
          icon: "💼"
        }
      ];`;

const newDefaultSec = `const defaultSections = [];

      function loadCustomSections() {
        try {
          const raw = localStorage.getItem(SECTIONS_STORAGE_KEY);
          if (raw) {
            const parsed = JSON.parse(raw);
            // Clean out legacy fake dummy sections
            const cleaned = parsed.filter(s => 
              s && s.id && 
              !s.id.startsWith("sec_daily") && 
              !s.id.startsWith("sec_travel") && 
              !s.id.startsWith("sec_food") && 
              !s.id.startsWith("sec_career")
            );
            return cleaned;
          }
        } catch (e) {
          console.error("Could not load custom sections:", e);
        }
        return [];
      }`;

if (scriptCode.includes(oldDefaultSec)) {
  // Replace oldDefaultSec and old loadCustomSections
  const oldLoadFn = `function loadCustomSections() {
        try {
          const raw = localStorage.getItem(SECTIONS_STORAGE_KEY);
          if (raw) return JSON.parse(raw);
        } catch (e) {
          console.error("Could not load custom sections:", e);
        }
        return defaultSections;
      }`;
  scriptCode = scriptCode.replace(oldDefaultSec, '');
  scriptCode = scriptCode.replace(oldLoadFn, newDefaultSec);
  console.log('Replaced defaultSections and loadCustomSections');
} else {
  console.log('oldDefaultSec format differs, searching more flexibly...');
  scriptCode = scriptCode.replace(/const defaultSections = \[[\s\S]*?\];/, 'const defaultSections = [];');
  scriptCode = scriptCode.replace(/function loadCustomSections\(\) \{[\s\S]*?return defaultSections;[\s\S]*?\}/, `function loadCustomSections() {
        try {
          const raw = localStorage.getItem(SECTIONS_STORAGE_KEY);
          if (raw) {
            const parsed = JSON.parse(raw);
            const cleaned = parsed.filter(s => s && s.id && !s.id.startsWith("sec_daily") && !s.id.startsWith("sec_travel") && !s.id.startsWith("sec_food") && !s.id.startsWith("sec_career"));
            return cleaned;
          }
        } catch (e) {
          console.error("Could not load custom sections:", e);
        }
        return [];
      }`);
}

// In renderCustomSections, handle empty state
const oldRenderCustomSecStart = `function renderCustomSections() {
        if (!sectionsGridEl) return;
        sectionsGridEl.innerHTML = "";
        if (sectionsCountPillEl) {
          sectionsCountPillEl.textContent = \`\${currentSections.length} Decks\`;
        }`;

const newRenderCustomSecStart = `function renderCustomSections() {
        if (!sectionsGridEl) return;
        sectionsGridEl.innerHTML = "";
        if (sectionsCountPillEl) {
          sectionsCountPillEl.textContent = \`\${currentSections.length} \${currentSections.length === 1 ? "Section" : "Sections"}\`;
        }
        const emptyStateEl = document.getElementById("empty-custom-sections");
        if (currentSections.length === 0) {
          if (emptyStateEl) emptyStateEl.style.display = "block";
          return;
        }
        if (emptyStateEl) emptyStateEl.style.display = "none";`;

if (scriptCode.includes(oldRenderCustomSecStart)) {
  scriptCode = scriptCode.replace(oldRenderCustomSecStart, newRenderCustomSecStart);
  console.log('Updated renderCustomSections empty state');
}

// In event listeners, hook up empty add section button
const emptyAddHook = `
      const btnEmptyAddSection = document.getElementById("btn-empty-add-section");
      if (btnEmptyAddSection) {
        btnEmptyAddSection.addEventListener("click", openAddSectionModal);
      }
`;

// Insert emptyAddHook after btnOpenAddSection listener
scriptCode = scriptCode.replace('if (btnOpenAddSection) btnOpenAddSection.addEventListener("click", openAddSectionModal);',
  'if (btnOpenAddSection) btnOpenAddSection.addEventListener("click", openAddSectionModal);\n' + emptyAddHook);

// Strict routing for 3K Card: Home -> Subsections -> Flashcard
// Ensure card3kFeatured click strictly opens screen-subsections and NEVER opens screen-flashcard
// Also ensure btnOpenSubsections opens screen-subsections
// Let's verify all occurrences of card3kFeatured and btnResume3k
scriptCode = scriptCode.replace(
  /const btnResume3k = document\.getElementById\("btn-resume-3k-deck"\);[\s\S]*?if \(btnResume3k\) \{[\s\S]*?\}\s*\}/g,
  `// Primary 3k action strictly navigates to subsections
      const btnOpenSubsections = document.getElementById("btn-open-subsections");
      if (btnOpenSubsections) {
        btnOpenSubsections.addEventListener("click", (e) => {
          e.stopPropagation();
          switchScreen("screen-subsections");
        });
      }`
);

// Reassemble updatedHtml
updatedHtml = updatedHtml.slice(0, scriptStartPos + '<script>'.length) + scriptCode + updatedHtml.slice(updatedHtml.indexOf('</script>', scriptStartPos));

// Write back to index.html
fs.writeFileSync('index.html', updatedHtml, 'utf8');
console.log('Successfully updated index.html! Final length:', updatedHtml.length);
