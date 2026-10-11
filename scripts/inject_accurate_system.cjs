const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

// 1. Read accurate images data
const accurateImagesData = JSON.parse(fs.readFileSync('scripts/accurate_images.json', 'utf8'));

// 2. Insert cardAccurateImages dictionary right before cardPhotos
const accurateImagesCode = `
      // 100% Verified, Authentic Real-World Concept Images (Strict Non-Random, Highly Accurate)
      const cardAccurateImages = ${JSON.stringify(accurateImagesData, null, 8)};
`;

if (!html.includes('const cardAccurateImages =')) {
  html = html.replace('const cardPhotos = {', accurateImagesCode + '\n      const cardPhotos = {');
  console.log('Inserted cardAccurateImages into index.html');
}

// 3. Update primaryImgUrl in renderCurrentCard() to strictly use accurate real images
html = html.replace(
  `const photoId = cardPhotos[card.num] || "photo-1556911220-e15b29be8c8f";
        const primaryImgUrl = \`https://images.unsplash.com/\${photoId}?w=600&auto=format&fit=crop&q=80\`;`,
  `// Strictly use exact, verified, authentic concept image
        const primaryImgUrl = (typeof cardAccurateImages !== "undefined" && cardAccurateImages[card.num]) 
          ? cardAccurateImages[card.num] 
          : \`/api/image?num=\${card.num}\`;`
);

// 4. Update image error fallback to try /api/image before emoji fallback
html = html.replace(
  `tempImg.onerror = () => {
          if (visualSkeletonEl) visualSkeletonEl.style.display = "none";
          frontVisualImgEl.style.display = "none";
          frontVisualFallbackEl.style.display = "flex";
        };`,
  `tempImg.onerror = () => {
          if (!tempImg.dataset.retried) {
            tempImg.dataset.retried = "true";
            tempImg.src = \`/api/image?num=\${card.num}\`;
            return;
          }
          if (visualSkeletonEl) visualSkeletonEl.style.display = "none";
          frontVisualImgEl.style.display = "none";
          frontVisualFallbackEl.style.display = "flex";
        };`
);

// 5. Clean up Shortcut Section labels and add Quick Edit button in header
const oldShortcutSectionHeader = `<div class="shortcut-header">
                  <div class="shortcut-title-group">
                    <span class="shortcut-icon-sparkle">⚡</span>
                    <span class="shortcut-title">Memory Shortcuts</span>
                    <span class="shortcut-badge">Instant Recall</span>
                  </div>
                  <span class="shortcut-sub">Phonetic & Visual Tricks</span>
                </div>`;

const newShortcutSectionHeader = `<div class="shortcut-header">
                  <div class="shortcut-title-group">
                    <span class="shortcut-icon-sparkle">⚡</span>
                    <span class="shortcut-title">Memory Shortcuts</span>
                  </div>
                  <button type="button" class="shortcut-quick-edit-btn" id="btn-quick-edit-shortcut" title="Edit shortcuts for this card" aria-label="Edit shortcuts">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M12 20h9" />
                      <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z" />
                    </svg>
                    <span>Edit Shortcut</span>
                  </button>
                </div>`;

html = html.replace(oldShortcutSectionHeader, newShortcutSectionHeader);

// Clean tags (remove 'Desi' and clumsy words)
html = html.replace(
  '<span class="shortcut-lang-tag tag-es">🇪🇸 Spanish Trick</span>',
  '<span class="shortcut-lang-tag tag-es">🇪🇸 Spanish Shortcut</span>'
);
html = html.replace(
  '<span class="shortcut-lang-tag tag-hi">🇮🇳 Hindi / Desi Trick</span>',
  '<span class="shortcut-lang-tag tag-hi">🇮🇳 Hindi Shortcut</span>'
);

// Update front shortcut label
html = html.replace(
  '<span class="shortcut-btn-label">Memory Trick: Tap to Reveal</span>',
  '<span class="shortcut-btn-label">Memory Shortcuts</span>'
);

// 6. Remove unnecessary verbose notes from Edit Modal
html = html.replace(
  `<div class="edit-helper-note">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="16" x2="12" y2="12"></line>
              <line x1="12" y1="8" x2="12.01" y2="8"></line>
            </svg>
            <span>Tapping Spanish or Hindi will immediately pronounce your custom edited words in authentic native accents!</span>
          </div>`,
  ''
);

// Remove "Desi" label from edit form as well
html = html.replace(
  '<span>⚡ 🇮🇳 Hindi / Desi Shortcut Trick</span>',
  '<span>⚡ 🇮🇳 Hindi Shortcut</span>'
);
html = html.replace(
  '<span>⚡ 🇪🇸 Spanish Shortcut Trick</span>',
  '<span>⚡ 🇪🇸 Spanish Shortcut</span>'
);

// 7. Add dedicated Quick Shortcut Edit Modal Sheet (`#shortcut-modal`)
const quickShortcutModalHtml = `
    <!-- Dedicated Quick Shortcut Edit Modal -->
    <div class="modal-backdrop" id="shortcut-modal">
      <div class="modal-sheet shortcut-sheet">
        <div class="modal-handle"></div>
        <div class="modal-header">
          <div class="edit-modal-title-group">
            <span class="modal-title" id="shortcut-modal-title">Edit Memory Shortcuts</span>
            <span class="edit-badge">Shortcuts</span>
          </div>
          <button class="modal-close-btn" id="shortcut-modal-close-btn" aria-label="Close edit">&times;</button>
        </div>

        <form id="shortcut-quick-form" class="edit-form-content" onsubmit="return false;">
          <div class="edit-form-field">
            <label class="edit-label" for="quick-shortcut-es">
              <span>🇪🇸 Spanish Shortcut</span>
            </label>
            <textarea id="quick-shortcut-es" class="edit-input edit-textarea" rows="2" placeholder="e.g. Giraffe-o → Tall neck bends like a giraffe..."></textarea>
          </div>

          <div class="edit-form-field">
            <label class="edit-label" for="quick-shortcut-hi">
              <span>🇮🇳 Hindi Shortcut</span>
            </label>
            <textarea id="quick-shortcut-hi" class="edit-input edit-textarea" rows="2" placeholder="e.g. Null → Turn tap off till flow drops to zero..."></textarea>
          </div>

          <div class="edit-btn-group">
            <button type="button" class="btn-edit-reset" id="btn-quick-shortcut-reset">Restore Default</button>
            <button type="submit" class="btn-edit-save" id="btn-quick-shortcut-save">Save Shortcut</button>
          </div>
        </form>
      </div>
    </div>
`;

if (!html.includes('id="shortcut-modal"')) {
  html = html.replace('<!-- Floating Toast Notification -->', quickShortcutModalHtml + '\n    <!-- Floating Toast Notification -->');
  console.log('Added quick shortcut modal sheet HTML');
}

// 8. Add CSS styles for Quick Shortcut Button and Textarea
const quickEditStyles = `
      /* Quick Shortcut Edit Button & Modal Styling */
      .shortcut-quick-edit-btn {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: rgba(56, 189, 248, 0.1);
        border: 1px solid rgba(56, 189, 248, 0.28);
        border-radius: 9999px;
        color: var(--accent-cyan);
        font-size: 0.68rem;
        font-weight: 700;
        padding: 3px 9px;
        cursor: pointer;
        transition: all 0.15s ease;
      }

      .shortcut-quick-edit-btn:hover,
      .shortcut-quick-edit-btn:active {
        background: rgba(56, 189, 248, 0.25);
        border-color: var(--accent-cyan);
        transform: scale(0.96);
      }

      .edit-textarea {
        resize: none;
        line-height: 1.4;
        font-family: inherit;
        font-size: 0.85rem;
      }
`;

if (!html.includes('.shortcut-quick-edit-btn {')) {
  html = html.replace('/* Front Face Shortcut Glance Button */', quickEditStyles + '\n      /* Front Face Shortcut Glance Button */');
  console.log('Added quick edit CSS styles');
}

// 9. Add JavaScript DOM elements and controller logic for quick shortcut modal
const quickModalJs = `
      // Quick Shortcut Edit Modal Elements
      const btnQuickEditShortcut = document.getElementById("btn-quick-edit-shortcut");
      const shortcutModal = document.getElementById("shortcut-modal");
      const shortcutModalTitle = document.getElementById("shortcut-modal-title");
      const shortcutModalCloseBtn = document.getElementById("shortcut-modal-close-btn");
      const shortcutQuickForm = document.getElementById("shortcut-quick-form");
      const quickShortcutEs = document.getElementById("quick-shortcut-es");
      const quickShortcutHi = document.getElementById("quick-shortcut-hi");
      const btnQuickShortcutReset = document.getElementById("btn-quick-shortcut-reset");
      const btnQuickShortcutSave = document.getElementById("btn-quick-shortcut-save");

      function openQuickShortcutModal() {
        const card = cards[currentIndex];
        if (!card) return;
        shortcutModalTitle.textContent = \`Edit Shortcut: \${card.word}\`;
        
        const defaultShortcut = (typeof cardShortcuts !== "undefined" && cardShortcuts[card.num]) ? cardShortcuts[card.num] : { es: "", hi: "" };
        quickShortcutEs.value = card.shortcutEs || defaultShortcut.es || "";
        quickShortcutHi.value = card.shortcutHi || defaultShortcut.hi || "";

        shortcutModal.classList.add("open");
        quickShortcutEs.focus();
        playHapticTick(520, "sine", 0.04);
      }

      function closeQuickShortcutModal() {
        shortcutModal.classList.remove("open");
      }

      if (btnQuickEditShortcut) {
        btnQuickEditShortcut.addEventListener("click", (e) => {
          e.stopPropagation();
          openQuickShortcutModal();
        });
      }

      if (shortcutModalCloseBtn) {
        shortcutModalCloseBtn.addEventListener("click", closeQuickShortcutModal);
      }

      if (shortcutModal) {
        shortcutModal.addEventListener("click", (e) => {
          if (e.target === shortcutModal) closeQuickShortcutModal();
        });
      }

      if (shortcutQuickForm) {
        shortcutQuickForm.addEventListener("submit", (e) => {
          e.preventDefault();
          const card = cards[currentIndex];
          if (!card) return;

          const newEs = quickShortcutEs.value.trim();
          const newHi = quickShortcutHi.value.trim();
          if (newEs) card.shortcutEs = newEs;
          if (newHi) card.shortcutHi = newHi;
          card.isCustomEdited = true;

          saveEditsToStorage(card.num, {
            word: card.word,
            tamil: card.tamil,
            es: card.trans.es,
            hi: card.trans.hi,
            category: card.category,
            shortcutEs: newEs,
            shortcutHi: newHi
          });

          renderCurrentCard();
          closeQuickShortcutModal();
          showToast(\`Shortcut for \${card.word} updated!\`);
          playHapticTick(620, "triangle", 0.05);
        });
      }

      if (btnQuickShortcutReset) {
        btnQuickShortcutReset.addEventListener("click", () => {
          const card = cards[currentIndex];
          if (!card) return;
          delete card.shortcutEs;
          delete card.shortcutHi;

          const defaultShortcut = (typeof cardShortcuts !== "undefined" && cardShortcuts[card.num]) ? cardShortcuts[card.num] : { es: "", hi: "" };
          quickShortcutEs.value = defaultShortcut.es || "";
          quickShortcutHi.value = defaultShortcut.hi || "";

          renderCurrentCard();
          showToast(\`Shortcut restored to default!\`);
          playHapticTick(440, "sine", 0.05);
        });
      }
`;

if (!html.includes('function openQuickShortcutModal()')) {
  html = html.replace('function openEditModal() {', quickModalJs + '\n      function openEditModal() {');
  console.log('Added quick shortcut modal JS controller');
}

fs.writeFileSync('index.html', html);
console.log('Successfully injected accurate real images and easy shortcut editing!');
