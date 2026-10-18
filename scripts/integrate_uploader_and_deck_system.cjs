const fs = require('fs');
const path = require('path');

const indexHtmlPath = path.resolve('index.html');
let content = fs.readFileSync(indexHtmlPath, 'utf8');

// 1. Add #btn-top-upload-deck to the top nav action buttons
const targetNavAction = `<div class="top-nav-actions">`;
const replacementNavAction = `<div class="top-nav-actions">
              <!-- Deck Switcher & Automatic Uploader Button -->
              <button type="button" class="duo-btn-3d deck-upload-nav-btn" id="btn-top-upload-deck" title="Switch Vocabulary Deck or Upload File (1–100, 800–1000)" aria-label="Deck Switcher" style="background: rgba(56, 189, 248, 0.16); border: 1px solid rgba(56, 189, 248, 0.4); color: #38bdf8; display: flex; align-items: center; gap: 5px; padding: 7px 12px; font-weight: 800; border-radius: 12px;">
                <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                  <polyline points="17 8 12 3 7 8"/>
                  <line x1="12" y1="3" x2="12" y2="15"/>
                </svg>
                <span id="nav-active-deck-label" style="font-size: 0.76rem; letter-spacing: 0.02em;">Deck: 800–1k</span>
              </button>`;

if (!content.includes('id="btn-top-upload-deck"')) {
  content = content.replace(targetNavAction, replacementNavAction);
  console.log('✓ Added btn-top-upload-deck to top nav actions');
}

// 2. Enhance screen-subsections with Tier 1 (1–100), Tier 9 (800–1000), Upload Card, and Custom Decks list
const targetSubsections = `<div class="app-screen" id="screen-subsections">`;
const replacementSubsections = `<div class="app-screen" id="screen-subsections">
          <!-- Subsections Header & Quick Switch -->
          <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px; margin-bottom: 20px;">
            <div>
              <h2 style="font-size: 1.5rem; font-weight: 800; color: #fff; margin: 0 0 4px;">Vocabulary Tiers & Decks</h2>
              <div style="font-size: 0.85rem; color: #94a3b8;">Select a curriculum tier or upload your own file with automatic authentic photo matching</div>
            </div>
            <button type="button" class="duo-btn-3d duo-btn-3d-green" id="btn-subsections-upload" style="padding: 11px 20px; font-size: 0.88rem; font-weight: 800; display: flex; align-items: center; gap: 8px;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="17 8 12 3 7 8"/>
                <line x1="12" y1="3" x2="12" y2="15"/>
              </svg>
              <span>Upload / Import Deck</span>
            </button>
          </div>

          <!-- TIER 1: Cards 1 – 100 (Foundations, Pronouns & Everyday Essentials) -->
          <div class="tier-card-option" id="sub-tier-1-100" role="button" tabindex="0" style="margin-bottom: 18px; background: linear-gradient(135deg, rgba(16, 185, 129, 0.22), rgba(2, 132, 199, 0.12)); border: 2px solid rgba(16, 185, 129, 0.45); box-shadow: 0 10px 28px rgba(16, 185, 129, 0.15), 0 5px 0 #059669; border-radius: 24px; padding: 24px 28px; cursor: pointer; transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px;">
              <div style="display: flex; align-items: center; gap: 16px;">
                <span style="display: flex; align-items: center; justify-content: center; width: 56px; height: 56px; border-radius: 18px; background: rgba(255, 255, 255, 0.12); font-size: 1.8rem; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.25);">👤</span>
                <div>
                  <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 0.74rem; font-weight: 800; letter-spacing: 0.08em; color: #34d399; text-transform: uppercase;">Tier 1 · Foundations</span>
                    <span class="active-tier-pill" id="pill-tier-1" style="display: none; font-size: 0.68rem; font-weight: 800; background: #10b981; color: #fff; padding: 2px 8px; border-radius: 999px;">ACTIVE DECK</span>
                  </div>
                  <h3 style="font-size: 1.35rem; font-weight: 800; color: #ffffff; margin: 3px 0 5px;">Cards 1 – 100 (Core Pronouns & Modals)</h3>
                  <div style="font-size: 0.86rem; color: #cbd5e1;">I, YOU, HE, SHE, WE, THEY, THIS, THAT, WILL, SHOULD, MUST · 100 Words</div>
                </div>
              </div>
              <button type="button" class="duo-btn-3d duo-btn-3d-green" id="btn-study-tier-1" style="padding: 13px 26px; font-size: 0.95rem;">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                  <polygon points="5 3 19 12 5 21 5 3"></polygon>
                </svg>
                <span>Study Tier 1</span>
              </button>
            </div>
            <div style="margin-top: 16px; padding-top: 14px; border-top: 1px solid rgba(255, 255, 255, 0.1); display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
              <div style="font-size: 0.82rem; color: #94a3b8;">
                Master core pronouns, reflexives, demonstratives and modal auxiliary verbs with real-world imagery.
              </div>
              <div style="display: flex; align-items: center; gap: 10px;">
                <span id="tier-1-stat-line" style="font-size: 0.85rem; font-weight: 700; color: #34d399;">0 / 100 Learned</span>
                <div style="width: 120px; height: 8px; background: rgba(255, 255, 255, 0.1); border-radius: 9999px; overflow: hidden;">
                  <div id="tier-1-progress-bar" style="width: 0%; height: 100%; background: #34d399; border-radius: 9999px;"></div>
                </div>
              </div>
            </div>
          </div>`;

if (!content.includes('id="sub-tier-1-100"')) {
  content = content.replace(targetSubsections, replacementSubsections);
  console.log('✓ Added Tier 1 (1–100) card to screen-subsections');
}

// 3. Add Custom Decks Section container in screen-subsections right before the Add Section button
const targetSubAddSection = `<div class="duo-add-section-wrapper" style="margin-top: 36px;">`;
const replacementCustomDecksBlock = `<!-- Custom Uploaded Decks Dynamic Section -->
          <div id="custom-decks-section" style="margin-top: 24px;">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
              <h3 style="font-size: 1.15rem; font-weight: 800; color: #fff; margin: 0;">My Custom Uploaded Decks</h3>
              <span id="custom-decks-count-badge" style="font-size: 0.78rem; font-weight: 700; color: #38bdf8; background: rgba(56, 189, 248, 0.15); padding: 3px 10px; border-radius: 999px;">0 Decks</span>
            </div>
            <div id="custom-decks-grid" style="display: flex; flex-direction: column; gap: 12px;">
              <!-- Populated dynamically via JS -->
            </div>
          </div>

          <div class="duo-add-section-wrapper" style="margin-top: 36px;">`;

if (!content.includes('id="custom-decks-section"')) {
  content = content.replace(targetSubAddSection, replacementCustomDecksBlock);
  console.log('✓ Added custom-decks-section to screen-subsections');
}

// 4. Add modal-upload-deck right before <script>
const targetScript = `<script>`;
const replacementUploadModal = `<!-- ========================================================== -->
    <!-- UPLOAD DECK & AUTOMATIC IMAGE DISCOVERY MODAL              -->
    <!-- ========================================================== -->
    <div class="modal-backdrop" id="modal-upload-deck">
      <div class="modal-sheet" style="max-width: 560px; background: linear-gradient(180deg, #172236 0%, #0c1424 100%); border: 1px solid rgba(255,255,255,0.14); border-radius: 26px; box-shadow: 0 25px 70px rgba(0,0,0,0.85); overflow: hidden; padding: 24px;">
        <div class="modal-handle"></div>
        <div class="modal-header" style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">
          <div class="edit-modal-title-group" style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 1.5rem;">⚡</span>
            <div>
              <span class="modal-title" style="font-size: 1.25rem; font-weight: 800; color: #fff;">Deck & File Uploader</span>
              <div style="font-size: 0.8rem; color: #94a3b8;">Automatic parser & latest verified photo finder</div>
            </div>
          </div>
          <button type="button" class="modal-close-btn" id="btn-close-upload-deck" aria-label="Close" style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); border-radius: 10px; width: 34px; height: 34px; color: #cbd5e1; cursor: pointer; font-size: 1.1rem; display: flex; align-items: center; justify-content: center;">&times;</button>
        </div>

        <!-- Quick Preset Tiers -->
        <div style="margin-bottom: 16px; padding: 14px; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px;">
          <div style="font-size: 0.76rem; font-weight: 800; color: #38bdf8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 10px;">Select Built-in Vocabulary Tier</div>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
            <button type="button" class="duo-btn-3d" id="btn-preset-tier-1" style="padding: 12px; font-size: 0.85rem; font-weight: 700; background: rgba(16, 185, 129, 0.16); border: 1px solid rgba(16, 185, 129, 0.45); color: #34d399; border-radius: 14px; cursor: pointer; text-align: left;">
              <span style="font-size: 1.05rem; font-weight: 800; display: block; margin-bottom: 2px;">👤 Tier 1: Cards 1 – 100</span>
              <span style="font-size: 0.74rem; color: #cbd5e1; font-weight: 500;">Foundations & Core Pronouns</span>
            </button>
            <button type="button" class="duo-btn-3d" id="btn-preset-tier-800" style="padding: 12px; font-size: 0.85rem; font-weight: 700; background: rgba(56, 189, 248, 0.16); border: 1px solid rgba(56, 189, 248, 0.45); color: #38bdf8; border-radius: 14px; cursor: pointer; text-align: left;">
              <span style="font-size: 1.05rem; font-weight: 800; display: block; margin-bottom: 2px;">🔥 Tier 9: Cards 800 – 1000</span>
              <span style="font-size: 0.74rem; color: #cbd5e1; font-weight: 500;">Kitchen, Living & Transit (200)</span>
            </button>
          </div>
        </div>

        <!-- Drag and drop zone -->
        <div id="deck-dropzone" style="border: 2px dashed rgba(56, 189, 248, 0.4); border-radius: 16px; padding: 22px 16px; text-align: center; background: rgba(2, 132, 199, 0.06); cursor: pointer; transition: all 0.2s;">
          <div style="font-size: 2rem; margin-bottom: 6px;">📂</div>
          <div style="font-size: 0.95rem; font-weight: 800; color: #ffffff;">Choose or drag & drop a file</div>
          <div style="font-size: 0.78rem; color: #94a3b8; margin-top: 3px;">Supports .txt, .json, .csv, .tsv (curriculum format)</div>
          <input type="file" id="deck-file-input" accept=".txt,.json,.csv,.tsv" style="display: none;" />
        </div>

        <!-- Optional Deck Name -->
        <div style="margin-top: 14px;">
          <label for="deck-title-input" style="font-size: 0.8rem; font-weight: 700; color: #cbd5e1; display: block; margin-bottom: 6px;">Deck Name / Title (Optional):</label>
          <input type="text" id="deck-title-input" placeholder="e.g. My Conversational Vocabulary" style="width: 100%; box-sizing: border-box; background: rgba(0,0,0,0.35); border: 1px solid rgba(255,255,255,0.12); border-radius: 12px; padding: 10px 12px; color: #fff; font-size: 0.88rem;" />
        </div>

        <!-- Paste Direct Text -->
        <div style="margin-top: 12px;">
          <label for="deck-paste-input" style="font-size: 0.8rem; font-weight: 700; color: #cbd5e1; display: block; margin-bottom: 6px;">Or Paste Raw Curriculum / Word Text Directly:</label>
          <textarea id="deck-paste-input" rows="4" style="width: 100%; box-sizing: border-box; background: rgba(0,0,0,0.35); border: 1px solid rgba(255,255,255,0.12); border-radius: 12px; padding: 10px; color: #fff; font-size: 0.82rem; font-family: monospace; resize: vertical;" placeholder="1. 👤 I = yo / main / நான்&#10;2. YOU = tú / tum / நீ&#10;3. 👨 HE = él / woh / அவன்..."></textarea>
        </div>

        <!-- Image Auto Discovery Option -->
        <div style="display: flex; align-items: center; justify-content: space-between; margin-top: 14px; padding: 12px 14px; background: rgba(255,255,255,0.04); border-radius: 14px; border: 1px solid rgba(255,255,255,0.08);">
          <div>
            <div style="font-size: 0.84rem; font-weight: 700; color: #f1f5f9;">✨ Auto-Find Latest Authentic Photos</div>
            <div style="font-size: 0.74rem; color: #94a3b8;">Automatically fetches verified Wikipedia & Wikimedia real-world photography</div>
          </div>
          <input type="checkbox" id="chk-auto-find-images" checked style="width: 20px; height: 20px; cursor: pointer; accent-color: #38bdf8;" />
        </div>

        <!-- Progress & Status Indicator -->
        <div id="upload-status-box" style="display: none; margin-top: 14px; padding: 12px; background: rgba(56, 189, 248, 0.12); border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 12px;">
          <div id="upload-status-text" style="font-size: 0.84rem; font-weight: 700; color: #38bdf8;">Parsing curriculum...</div>
          <div style="margin-top: 8px; width: 100%; height: 6px; background: rgba(255,255,255,0.1); border-radius: 999px; overflow: hidden;">
            <div id="upload-progress-fill" style="width: 0%; height: 100%; background: #38bdf8; transition: width 0.2s;"></div>
          </div>
        </div>

        <!-- Actions -->
        <div style="display: flex; gap: 10px; margin-top: 16px;">
          <button type="button" class="duo-btn-3d" id="btn-cancel-upload-deck" style="flex: 1; padding: 12px; border-radius: 12px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); color: #cbd5e1; font-weight: 700; cursor: pointer;">Cancel</button>
          <button type="button" class="duo-btn-3d duo-btn-3d-green" id="btn-parse-and-load-deck" style="flex: 2; padding: 12px; border-radius: 12px; font-weight: 800; cursor: pointer;">Load & Sync Deck</button>
        </div>
      </div>
    </div>

    <script>`;

if (!content.includes('id="modal-upload-deck"')) {
  content = content.replace(targetScript, replacementUploadModal);
  console.log('✓ Added modal-upload-deck to index.html');
}

fs.writeFileSync(indexHtmlPath, content, 'utf8');
console.log('HTML changes applied successfully.');
