const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

// 1. Replace #app-container and card sizing in CSS for uncompressed modern layout
html = html.replace(
  `#app-container {
        position: relative;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        width: 100%;
        max-width: 480px;
        height: 100%;
        height: 100dvh;
        margin: 0 auto;
        padding: env(safe-area-inset-top, 14px) 16px
          env(safe-area-inset-bottom, 16px) 16px;
        z-index: 1;
      }`,
  `#app-container {
        position: relative;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        width: 100%;
        max-width: 520px;
        height: 100%;
        height: 100dvh;
        margin: 0 auto;
        padding: env(safe-area-inset-top, 16px) 18px
          env(safe-area-inset-bottom, 18px) 18px;
        z-index: 1;
        transition: max-width 0.3s ease;
      }

      @media (min-width: 768px) {
        #app-container {
          max-width: 620px;
          padding: 24px 20px;
        }
      }`
);

// 2. Adjust flashcard-wrapper and visual-box sizing
html = html.replace(
  `.flashcard-wrapper {
        width: 100%;
        height: 100%;
        max-height: 570px;`,
  `.flashcard-wrapper {
        width: 100%;
        height: 100%;
        max-height: 600px;`
);

// Update visual box height for uncompressed, modern presentation
html = html.replace(
  `.visual-box {
        position: relative;
        width: 100%;
        max-width: 320px;
        height: 175px;`,
  `.visual-box {
        position: relative;
        width: 100%;
        max-width: 380px;
        height: 190px;`
);

// 3. Remove the redundant edit pill button wrapper from card back
html = html.replace(
  `<!-- Edit Translations Action Pill -->
              <div class="edit-pill-wrapper">
                <button
                  class="edit-card-pill-btn"
                  id="back-edit-pill-btn"
                  title="Edit translations for this card"
                  aria-label="Edit translations"
                >
                  <svg
                    width="13"
                    height="13"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2.2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <path d="M12 20h9" />
                    <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z" />
                  </svg>
                  <span>Edit Translations</span>
                </button>
              </div>`,
  ''
);

// 4. Update the bottom footer button: replace jump button with Settings Symbol (⚙️)
const oldFooterBtn = `<button
          class="jump-trigger-btn"
          id="btn-jump-modal"
          title="Jump to card"
          aria-label="Jump to card index"
        >
          <svg
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <line x1="8" y1="6" x2="21" y2="6"></line>
            <line x1="8" y1="12" x2="21" y2="12"></line>
            <line x1="8" y1="18" x2="21" y2="18"></line>
            <line x1="3" y1="6" x2="3.01" y2="6"></line>
            <line x1="3" y1="12" x2="3.01" y2="12"></line>
            <line x1="3" y1="18" x2="3.01" y2="18"></line>
          </svg>
        </button>`;

const newFooterBtn = `<button
          class="jump-trigger-btn settings-trigger-btn"
          id="btn-settings-modal"
          title="Settings & Offline HTML"
          aria-label="Settings and Offline HTML"
        >
          <svg
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2.2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/>
            <circle cx="12" cy="12" r="3"/>
          </svg>
        </button>`;

html = html.replace(oldFooterBtn, newFooterBtn);

// 5. Replace Quick Jump Drawer Modal with Modern Settings & Offline Modal
const oldJumpModal = `<!-- Quick Jump Drawer Modal -->
    <div class="modal-backdrop" id="jump-modal">
      <div class="modal-sheet">
        <div class="modal-handle"></div>
        <div class="modal-header">
          <span class="modal-title">Jump to Card</span>
          <button class="modal-close-btn" id="modal-close-btn">&times;</button>
        </div>

        <div class="range-slider-wrapper">
          <div class="slider-bubble" id="slider-val-indicator">#800</div>
          <input
            type="range"
            class="jump-slider"
            id="jump-slider"
            min="800"
            max="1000"
            value="800"
          />
        </div>

        <div style="font-size: 0.8rem; color: #94a3b8; font-weight: 600;">
          Sections:
        </div>
        <div class="category-chips-list" id="category-chips"></div>
      </div>
    </div>`;

const newSettingsModal = `<!-- Settings & Offline HTML Modal -->
    <div class="modal-backdrop" id="settings-modal">
      <div class="modal-sheet settings-sheet">
        <div class="modal-handle"></div>
        <div class="modal-header">
          <div class="edit-modal-title-group">
            <span class="modal-title">Settings & Tools</span>
            <span class="edit-badge">Offline Ready</span>
          </div>
          <button class="modal-close-btn" id="settings-close-btn" aria-label="Close settings">&times;</button>
        </div>

        <div class="settings-content-body">
          <!-- Download Offline HTML Card -->
          <div class="settings-action-card">
            <div class="settings-card-info">
              <div class="settings-card-icon-box">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                  <polyline points="7 10 12 15 17 10"/>
                  <line x1="12" y1="15" x2="12" y2="3"/>
                </svg>
              </div>
              <div class="settings-card-text">
                <div class="settings-card-title">Download Offline HTML</div>
                <div class="settings-card-desc">Save the entire deck as a single offline HTML file. Opens in any browser with zero internet.</div>
              </div>
            </div>
            <button type="button" class="btn-download-html" id="btn-download-html">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="7 10 12 15 17 10"/>
                <line x1="12" y1="15" x2="12" y2="3"/>
              </svg>
              <span>Download HTML File</span>
            </button>
          </div>

          <!-- Quick Jump Slider Card -->
          <div class="settings-card-section">
            <div class="settings-section-label">Fast Card Jump (800 – 1000)</div>
            <div class="range-slider-wrapper">
              <div class="slider-bubble" id="slider-val-indicator">#800</div>
              <input
                type="range"
                class="jump-slider"
                id="jump-slider"
                min="800"
                max="1000"
                value="800"
              />
            </div>
          </div>
        </div>
      </div>
    </div>`;

html = html.replace(oldJumpModal, newSettingsModal);

// 6. Add CSS styles for Settings Modal and Download Action
const settingsStyles = `
      /* Settings & Download HTML Styling */
      .settings-sheet {
        max-height: 82vh;
      }

      .settings-content-body {
        display: flex;
        flex-direction: column;
        gap: 16px;
        padding-top: 6px;
      }

      .settings-action-card {
        display: flex;
        flex-direction: column;
        gap: 12px;
        padding: 14px 16px;
        border-radius: 18px;
        background: rgba(56, 189, 248, 0.05);
        border: 1px solid rgba(56, 189, 248, 0.22);
      }

      .settings-card-info {
        display: flex;
        align-items: flex-start;
        gap: 12px;
      }

      .settings-card-icon-box {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 40px;
        height: 40px;
        border-radius: 12px;
        background: rgba(56, 189, 248, 0.12);
        border: 1px solid rgba(56, 189, 248, 0.28);
        flex-shrink: 0;
      }

      .settings-card-title {
        font-size: 0.95rem;
        font-weight: 750;
        color: #f8fafc;
        margin-bottom: 2px;
      }

      .settings-card-desc {
        font-size: 0.76rem;
        color: #94a3b8;
        line-height: 1.35;
      }

      .btn-download-html {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        width: 100%;
        padding: 11px 16px;
        border-radius: 14px;
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
        border: 1px solid rgba(56, 189, 248, 0.4);
        color: #ffffff;
        font-size: 0.88rem;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.2s ease;
        box-shadow: 0 4px 14px rgba(2, 132, 199, 0.35);
      }

      .btn-download-html:hover,
      .btn-download-html:active {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
        transform: translateY(-1px);
        box-shadow: 0 6px 18px rgba(2, 132, 199, 0.5);
      }

      .settings-card-section {
        display: flex;
        flex-direction: column;
        gap: 8px;
        padding: 14px 16px;
        border-radius: 18px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
      }

      .settings-section-label {
        font-size: 0.78rem;
        font-weight: 700;
        color: #94a3b8;
        letter-spacing: 0.03em;
        text-transform: uppercase;
      }
`;

if (!html.includes('.settings-action-card {')) {
  html = html.replace('/* Front Face Shortcut Glance Button */', settingsStyles + '\n      /* Front Face Shortcut Glance Button */');
  console.log('Added settings CSS styles');
}

// 7. Update JavaScript controller for Settings Modal & HTML Download
const newSettingsJs = `
      // Settings Modal & Offline HTML Download Elements
      const btnSettingsModal = document.getElementById("btn-settings-modal");
      const settingsModal = document.getElementById("settings-modal");
      const settingsCloseBtn = document.getElementById("settings-close-btn");
      const btnDownloadHtml = document.getElementById("btn-download-html");

      function openSettingsModal() {
        if (!settingsModal) return;
        settingsModal.classList.add("open");
        jumpSlider.value = cards[currentIndex].num;
        sliderValIndicator.textContent = \`#\${cards[currentIndex].num} — \${cards[currentIndex].word}\`;
        playHapticTick(500, "sine", 0.04);
      }

      function closeSettingsModal() {
        if (!settingsModal) return;
        settingsModal.classList.remove("open");
      }

      if (btnSettingsModal) {
        btnSettingsModal.addEventListener("click", openSettingsModal);
      }
      if (settingsCloseBtn) {
        settingsCloseBtn.addEventListener("click", closeSettingsModal);
      }
      if (settingsModal) {
        settingsModal.addEventListener("click", (e) => {
          if (e.target === settingsModal) closeSettingsModal();
        });
      }

      // Standalone Offline HTML Downloader
      function downloadOfflineHtml() {
        try {
          const docHtml = "<!doctype html>\\n" + document.documentElement.outerHTML;
          const blob = new Blob([docHtml], { type: "text/html;charset=utf-8" });
          const url = URL.createObjectURL(blob);
          const link = document.createElement("a");
          link.href = url;
          link.download = "Multilingual_Flashcards_800-1000.html";
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
          URL.revokeObjectURL(url);
          showToast("Offline HTML downloaded successfully!");
          playHapticTick(620, "triangle", 0.06);
        } catch (err) {
          console.error("HTML download error:", err);
          showToast("Download failed, please try again");
        }
      }

      if (btnDownloadHtml) {
        btnDownloadHtml.addEventListener("click", downloadOfflineHtml);
      }
`;

// Replace old jump modal JS bindings
html = html.replace(
  `const btnJumpModal = document.getElementById("btn-jump-modal");
      const jumpModal = document.getElementById("jump-modal");
      const modalCloseBtn = document.getElementById("modal-close-btn");
      const jumpSlider = document.getElementById("jump-slider");
      const sliderValIndicator = document.getElementById("slider-val-indicator");
      const categoryChipsEl = document.getElementById("category-chips");`,
  `const jumpSlider = document.getElementById("jump-slider");
      const sliderValIndicator = document.getElementById("slider-val-indicator");
` + newSettingsJs
);

// Remove old openJumpModal / closeJumpModal listeners
html = html.replace(
  `function openJumpModal() {
        jumpModal.classList.add("open");
        jumpSlider.value = cards[currentIndex].num;
        sliderValIndicator.textContent = \`#\${cards[currentIndex].num} — \${cards[currentIndex].word}\`;
      }

      function closeJumpModal() {
        jumpModal.classList.remove("open");
      }`,
  ''
);

html = html.replace(
  `btnJumpModal.addEventListener("click", openJumpModal);
      modalCloseBtn.addEventListener("click", closeJumpModal);
      jumpModal.addEventListener("click", (e) => {
        if (e.target === jumpModal) closeJumpModal();
      });`,
  ''
);

// Remove category chips building
html = html.replace(/buildSectionChips\(\);/g, '');
html = html.replace(/function buildSectionChips\(\) \{[\s\S]*?categoryChipsEl\.appendChild\(chip\);\s*\}\s*\}/g, '');

fs.writeFileSync('index.html', html);
console.log('Successfully updated settings, offline HTML download, and modern uncompressed layout!');
