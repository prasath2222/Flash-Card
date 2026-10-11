const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

// 1. Add CSS for Shortcut Section
const shortcutCss = `
      /* ==========================================================
         Dedicated Memory Shortcut / Trick Section Styles
         ========================================================== */
      .shortcut-section {
        display: flex;
        flex-direction: column;
        gap: 8px;
        background: rgba(15, 23, 42, 0.78);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border: 1px solid rgba(56, 189, 248, 0.22);
        border-radius: 18px;
        padding: 12px 14px;
        box-shadow: 0 8px 20px -6px rgba(0, 0, 0, 0.4);
      }

      .shortcut-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 8px;
        padding-bottom: 6px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
      }

      .shortcut-title-group {
        display: flex;
        align-items: center;
        gap: 6px;
      }

      .shortcut-icon-sparkle {
        font-size: 0.95rem;
        filter: drop-shadow(0 0 6px rgba(250, 204, 21, 0.6));
      }

      .shortcut-title {
        font-size: 0.78rem;
        font-weight: 750;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        color: #f8fafc;
      }

      .shortcut-badge {
        font-size: 0.64rem;
        font-weight: 700;
        padding: 2px 7px;
        border-radius: 9999px;
        background: rgba(56, 189, 248, 0.16);
        border: 1px solid rgba(56, 189, 248, 0.35);
        color: var(--accent-cyan);
        letter-spacing: 0.05em;
        text-transform: uppercase;
      }

      .shortcut-sub {
        font-size: 0.68rem;
        color: #94a3b8;
        font-weight: 500;
      }

      .shortcut-grid {
        display: flex;
        flex-direction: column;
        gap: 7px;
      }

      .shortcut-box {
        display: flex;
        flex-direction: column;
        gap: 4px;
        padding: 8px 11px;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        transition: all 0.2s ease;
      }

      .shortcut-box-es {
        border-left: 3px solid #f43f5e;
        background: rgba(244, 63, 94, 0.06);
      }

      .shortcut-box-hi {
        border-left: 3px solid #f59e0b;
        background: rgba(245, 158, 11, 0.06);
      }

      .shortcut-box-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 6px;
      }

      .shortcut-lang-tag {
        font-size: 0.66rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
      }

      .shortcut-lang-tag.tag-es {
        color: #fda4af;
      }

      .shortcut-lang-tag.tag-hi {
        color: #fde68a;
      }

      .shortcut-target-word {
        font-size: 0.76rem;
        font-weight: 700;
        color: #e2e8f0;
        font-family: monospace;
        background: rgba(0, 0, 0, 0.28);
        padding: 1px 6px;
        border-radius: 6px;
      }

      .shortcut-punchline {
        font-size: 0.81rem;
        line-height: 1.38;
        color: #cbd5e1;
      }

      .shortcut-punchline strong {
        color: #ffffff;
        font-weight: 750;
      }

      .shortcut-punchline em {
        color: #38bdf8;
        font-style: normal;
        font-weight: 600;
      }

      /* Front Face Shortcut Glance Button */
      .front-shortcut-glance {
        margin-top: 4px;
        display: flex;
        justify-content: center;
      }

      .front-shortcut-btn {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 14px;
        border-radius: 9999px;
        background: rgba(56, 189, 248, 0.08);
        border: 1px solid rgba(56, 189, 248, 0.25);
        color: #7dd3fc;
        font-size: 0.75rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
      }

      .front-shortcut-btn:hover,
      .front-shortcut-btn:active {
        background: rgba(56, 189, 248, 0.2);
        border-color: rgba(56, 189, 248, 0.5);
        transform: scale(0.97);
        color: #38bdf8;
      }

      .front-shortcut-btn .shortcut-bolt {
        font-size: 0.85rem;
        animation: subtlePulse 1.8s infinite;
      }

      @keyframes subtlePulse {
        0%, 100% { transform: scale(1); opacity: 0.9; }
        50% { transform: scale(1.25); opacity: 1; }
      }
`;

if (!html.includes('.shortcut-section {')) {
  html = html.replace('/* Floating Toast Notification */', shortcutCss + '\n      /* Floating Toast Notification */');
  console.log('Added shortcut CSS styles');
}

// 2. Adjust .back-content and .tamil-hero-card sizing for sleek layout
html = html.replace(
  `.back-content {
        display: flex;
        flex-direction: column;
        justify-content: center;
        flex: 1;
        min-height: 0;
        gap: 16px;
        padding: 4px 0;
      }`,
  `.back-content {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        flex: 1;
        min-height: 0;
        gap: 10px;
        padding: 2px 0 6px;
        overflow-y: auto;
        scrollbar-width: thin;
        scrollbar-color: rgba(56, 189, 248, 0.3) transparent;
      }`
);

html = html.replace(
  `padding: 20px 16px;
        border-radius: 22px;`,
  `padding: 13px 16px;
        border-radius: 18px;`
);

// 3. Add front face shortcut button
const frontShortcutBtnHtml = `              <!-- Quick Front Shortcut Glance Button -->
              <div class="front-shortcut-glance">
                <button
                  type="button"
                  class="front-shortcut-btn"
                  id="front-shortcut-btn"
                  title="Reveal memory shortcut trick"
                  aria-label="Reveal memory shortcut trick"
                >
                  <span class="shortcut-bolt">⚡</span>
                  <span class="shortcut-btn-label">Memory Trick: Tap to Reveal</span>
                </button>
              </div>`;

if (!html.includes('id="front-shortcut-btn"')) {
  html = html.replace(
    '</div>\n\n            <div class="card-hint-footer">\n              <span class="hint-icon">↻</span>',
    '</div>\n\n' + frontShortcutBtnHtml + '\n\n            <div class="card-hint-footer">\n              <span class="hint-icon">↻</span>'
  );
  console.log('Added front shortcut button');
}

// 4. Add back face shortcut section
const backShortcutSectionHtml = `              <!-- Dedicated Memory Shortcut Section -->
              <div class="shortcut-section" id="card-shortcut-section">
                <div class="shortcut-header">
                  <div class="shortcut-title-group">
                    <span class="shortcut-icon-sparkle">⚡</span>
                    <span class="shortcut-title">Memory Shortcuts</span>
                    <span class="shortcut-badge">Instant Recall</span>
                  </div>
                  <span class="shortcut-sub">Phonetic & Visual Tricks</span>
                </div>
                
                <div class="shortcut-grid">
                  <!-- Spanish Shortcut Box -->
                  <div class="shortcut-box shortcut-box-es">
                    <div class="shortcut-box-top">
                      <span class="shortcut-lang-tag tag-es">🇪🇸 Spanish Trick</span>
                      <span class="shortcut-target-word" id="shortcut-es-word">estufa</span>
                    </div>
                    <div class="shortcut-punchline" id="shortcut-es-text">
                      <strong>Es-tufa</strong> → <em>Tough-ah</em> flame on the stove, or <em>Stuff</em> the cooking pot onto the burner!
                    </div>
                  </div>

                  <!-- Hindi / Desi Shortcut Box -->
                  <div class="shortcut-box shortcut-box-hi">
                    <div class="shortcut-box-top">
                      <span class="shortcut-lang-tag tag-hi">🇮🇳 Hindi / Desi Trick</span>
                      <span class="shortcut-target-word" id="shortcut-hi-word">choolha</span>
                    </div>
                    <div class="shortcut-punchline" id="shortcut-hi-text">
                      <strong>Choolha</strong> → Village desi <em>Chulha</em> cooking hot rotis over crackling clay fire!
                    </div>
                  </div>
                </div>
              </div>`;

if (!html.includes('id="card-shortcut-section"')) {
  html = html.replace(
    '</div>\n\n              <!-- Edit Translations Action Pill -->',
    '</div>\n\n' + backShortcutSectionHtml + '\n\n              <!-- Edit Translations Action Pill -->'
  );
  console.log('Added back shortcut section HTML');
}

// 5. Add fields in Edit Modal Form
const editModalFields = `          <div class="edit-form-field">
            <label class="edit-label" for="edit-input-shortcut-es">
              <span>⚡ 🇪🇸 Spanish Shortcut Trick</span>
            </label>
            <input type="text" id="edit-input-shortcut-es" class="edit-input" autocomplete="off" />
          </div>

          <div class="edit-form-field">
            <label class="edit-label" for="edit-input-shortcut-hi">
              <span>⚡ 🇮🇳 Hindi / Desi Shortcut Trick</span>
            </label>
            <input type="text" id="edit-input-shortcut-hi" class="edit-input" autocomplete="off" />
          </div>`;

if (!html.includes('id="edit-input-shortcut-es"')) {
  html = html.replace(
    '<div class="edit-helper-note">',
    editModalFields + '\n\n          <div class="edit-helper-note">'
  );
  console.log('Added shortcut fields in Edit Modal');
}

// 6. Update JavaScript DOM element declarations & functions
const newDomElements = `      // Memory Shortcut DOM Elements
      const shortcutSectionEl = document.getElementById("card-shortcut-section");
      const shortcutEsWordEl = document.getElementById("shortcut-es-word");
      const shortcutEsTextEl = document.getElementById("shortcut-es-text");
      const shortcutHiWordEl = document.getElementById("shortcut-hi-word");
      const shortcutHiTextEl = document.getElementById("shortcut-hi-text");
      const frontShortcutBtn = document.getElementById("front-shortcut-btn");
      const editInputShortcutEs = document.getElementById("edit-input-shortcut-es");
      const editInputShortcutHi = document.getElementById("edit-input-shortcut-hi");
`;

if (!html.includes('const shortcutSectionEl =')) {
  html = html.replace('// Edit Modal Elements', newDomElements + '      // Edit Modal Elements');
  console.log('Added DOM variable bindings for shortcuts');
}

// 7. Update renderCurrentCard() to populate shortcuts
const renderShortcutsSnippet = `        // Populate Memory Shortcuts Section
        const defaultShortcut = (typeof cardShortcuts !== "undefined" && cardShortcuts[card.num]) ? cardShortcuts[card.num] : {
          es: "<strong>" + card.trans.es + "</strong> → Quick mnemonic for " + card.word,
          hi: "<strong>" + card.trans.hi + "</strong> → Daily spoken Indian recall for " + card.word
        };
        const currentEsShortcut = card.shortcutEs || defaultShortcut.es;
        const currentHiShortcut = card.shortcutHi || defaultShortcut.hi;

        if (shortcutEsTextEl) shortcutEsTextEl.innerHTML = currentEsShortcut;
        if (shortcutHiTextEl) shortcutHiTextEl.innerHTML = currentHiShortcut;
        if (shortcutEsWordEl) shortcutEsWordEl.textContent = card.trans.es;
        if (shortcutHiWordEl) shortcutHiWordEl.textContent = card.trans.hi;
`;

if (!html.includes('// Populate Memory Shortcuts Section')) {
  html = html.replace(
    'backHiWordEl.textContent = card.trans.hi;',
    'backHiWordEl.textContent = card.trans.hi;\n\n' + renderShortcutsSnippet
  );
  console.log('Updated renderCurrentCard with shortcut population');
}

// 8. Update openEditModal() and save edits
const openEditModalSnippet = `        const defaultShortcut = (typeof cardShortcuts !== "undefined" && cardShortcuts[card.num]) ? cardShortcuts[card.num] : { es: "", hi: "" };
        if (editInputShortcutEs) editInputShortcutEs.value = card.shortcutEs || defaultShortcut.es || "";
        if (editInputShortcutHi) editInputShortcutHi.value = card.shortcutHi || defaultShortcut.hi || "";
`;

if (!html.includes('editInputShortcutEs.value =')) {
  html = html.replace(
    'editInputCat.value = card.category || "";',
    'editInputCat.value = card.category || "";\n' + openEditModalSnippet
  );
  console.log('Updated openEditModal for shortcuts');
}

// 9. Update editCardForm submit handler
const saveEditsSnippet = `            shortcutEs: editInputShortcutEs ? editInputShortcutEs.value.trim() : "",
            shortcutHi: editInputShortcutHi ? editInputShortcutHi.value.trim() : "",`;

html = html.replace(
  'category: editInputCat.value.trim()',
  'category: editInputCat.value.trim(),\n            ' + saveEditsSnippet
);

// 10. Update loadSavedEdits to restore custom shortcuts
const loadSavedEditsSnippet = `              if (e.shortcutEs) card.shortcutEs = e.shortcutEs;
              if (e.shortcutHi) card.shortcutHi = e.shortcutHi;`;

if (!html.includes('card.shortcutEs = e.shortcutEs')) {
  html = html.replace(
    'if (e.category) card.category = e.category;',
    'if (e.category) card.category = e.category;\n' + loadSavedEditsSnippet
  );
  console.log('Updated loadSavedEdits for custom shortcuts');
}

// 11. Add event listener for frontShortcutBtn to flip card directly
const frontShortcutListener = `      if (frontShortcutBtn) {
        frontShortcutBtn.addEventListener("click", (e) => {
          e.stopPropagation();
          flipCard();
        });
      }
`;

if (!html.includes('frontShortcutBtn.addEventListener')) {
  html = html.replace(
    'cardWrapper.addEventListener("click", (e) => {',
    frontShortcutListener + '\n      cardWrapper.addEventListener("click", (e) => {'
  );
  console.log('Added event listener for frontShortcutBtn');
}

fs.writeFileSync('index.html', html);
console.log('Successfully integrated all shortcut features and UI!');
