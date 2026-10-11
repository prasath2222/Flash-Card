const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

// 1. Updated Device Modal HTML with clear explanations and foolproof methods
const newModalHtml = `
    <!-- Use on Any Device / Offline HTML Modal -->
    <div class="modal-backdrop" id="device-modal">
      <div class="modal-sheet">
        <div class="modal-handle"></div>
        <div class="modal-header">
          <div class="edit-modal-title-group">
            <span class="modal-title">Use on Any Device & Phone</span>
            <span class="edit-badge">Multi-Device</span>
          </div>
          <button class="modal-close-btn" id="device-modal-close-btn" aria-label="Close">&times;</button>
        </div>

        <div class="device-modal-content">
          <!-- Notice explaining the 404 error on dev preview links -->
          <div style="background: rgba(239, 68, 68, 0.08); border: 1px solid rgba(239, 68, 68, 0.25); border-radius: 12px; padding: 10px 12px; display: flex; gap: 8px; align-items: flex-start;">
            <span style="font-size: 1.1rem; line-height: 1;">⚠️</span>
            <div style="font-size: 0.72rem; color: #fca5a5; line-height: 1.4;">
              <strong>Why did Method 1 show "404 Page Not Found"?</strong><br />
              The internal AI Studio dev preview URL (<code>ais-dev-...</code>) is a temporary private developer sandbox locked to your current builder session. External devices cannot access it. Use the guaranteed methods below!
            </div>
          </div>

          <!-- Method 1 (Guaranteed): Download Standalone HTML App -->
          <div class="device-option-card" style="border-color: rgba(56, 189, 248, 0.4); background: rgba(56, 189, 248, 0.04);">
            <div class="device-card-header">
              <span class="device-icon">💾</span>
              <div class="device-card-info">
                <span class="device-card-title" style="color: #38bdf8;">Method 1 (Recommended): Download Standalone App</span>
                <span class="device-card-desc">Single-file deck with all 199 cards, accurate real photos, phonetic shortcuts, and full in-app editing!</span>
              </div>
            </div>
            
            <button type="button" class="btn-download-html" id="btn-download-html" style="margin-top: 6px;">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                <polyline points="7 10 12 15 17 10" />
                <line x1="12" y1="15" x2="12" y2="3" />
              </svg>
              <span>Download HTML App (.html)</span>
            </button>

            <div class="device-steps-list" style="margin-top: 6px;">
              <div class="device-step-item">
                <strong>1. Send to Phone:</strong> Send the downloaded <code>.html</code> file to your phone via <em>WhatsApp</em> (message yourself), <em>Telegram</em>, <em>Google Drive</em>, or <em>Email</em>.
              </div>
              <div class="device-step-item">
                <strong>2. Open on Phone:</strong> Tap the file and open in <em>Chrome</em> or <em>Safari</em>. Works 100% offline!
              </div>
              <div class="device-step-item">
                <strong>3. Edit on Phone:</strong> You can edit any card's word, Tamil, Spanish, Hindi, or shortcuts directly on your phone — saves automatically!
              </div>
            </div>
          </div>

          <!-- Method 2: Install as Native Phone App Icon -->
          <div class="device-option-card">
            <div class="device-card-header">
              <span class="device-icon">📱</span>
              <div class="device-card-info">
                <span class="device-card-title">Method 2: Add to Phone Home Screen (PWA)</span>
                <span class="device-card-desc">Makes it look and feel like an installed App Store / Play Store app with an icon!</span>
              </div>
            </div>
            <div class="device-steps-list">
              <div class="device-step-item">
                <strong>iPhone / iPad (Safari):</strong> Tap the <em>Share button</em> (square with arrow) → scroll down and tap <em>"Add to Home Screen"</em>.
              </div>
              <div class="device-step-item">
                <strong>Android (Chrome):</strong> Tap the <em>Menu (⋮)</em> in the top-right → select <em>"Add to Home screen"</em> or <em>"Install app"</em>.
              </div>
            </div>
          </div>

          <!-- Method 3: 1-Click Free Public Website Link -->
          <div class="device-option-card">
            <div class="device-card-header">
              <span class="device-icon">🌐</span>
              <div class="device-card-info">
                <span class="device-card-title">Method 3: Create a Free Public Link (Netlify Drop)</span>
                <span class="device-card-desc">Want an <code>https://...</code> website link to open on any device without sending files?</span>
              </div>
            </div>
            <div class="device-steps-list">
              <div class="device-step-item">
                <strong>1. Download:</strong> Click the "Download HTML App" button above.
              </div>
              <div class="device-step-item">
                <strong>2. Drag & Drop:</strong> Open <em><a href="https://app.netlify.com/drop" target="_blank" style="color: #38bdf8; text-decoration: underline;">app.netlify.com/drop</a></em> in your browser (free, no coding needed).
              </div>
              <div class="device-step-item">
                <strong>3. Get Link:</strong> Drag and drop the downloaded file. Netlify gives you a permanent public URL (e.g., <code>https://my-deck.netlify.app</code>) that works anywhere!
              </div>
            </div>
          </div>

          <!-- Method 4: Transfer / Backup Custom Edits -->
          <div class="device-option-card">
            <div class="device-card-header">
              <span class="device-icon">🔄</span>
              <div class="device-card-info">
                <span class="device-card-title">Transfer / Sync Edits Between Devices</span>
                <span class="device-card-desc">Backup your edited words, translations, and memory shortcuts to JSON</span>
              </div>
            </div>
            <div style="display: flex; gap: 8px; margin-top: 4px;">
              <button type="button" class="btn-edit-reset" id="btn-export-edits" style="padding: 8px 12px; font-size: 0.76rem; border-color: rgba(56, 189, 248, 0.4); color: #38bdf8;">📥 Export My Edits (.json)</button>
              <button type="button" class="btn-copy-url" id="btn-import-edits" style="padding: 8px 12px; font-size: 0.76rem;">📤 Import Edits (.json)</button>
            </div>
          </div>

        </div>
      </div>
    </div>`;

// Replace old device modal HTML
const modalRegex = /<!-- Use on Any Device \/ Offline HTML Modal -->[\s\S]*?<!-- Floating Toast Notification -->/;
if (modalRegex.test(html)) {
  html = html.replace(modalRegex, newModalHtml + '\n\n    <!-- Floating Toast Notification -->');
  console.log('Replaced modal HTML successfully!');
} else {
  console.error('Could not find old modal HTML to replace');
}

// 2. Enhance btnDownloadHtml in JS to automatically bake current custom edits into the exported HTML
const oldDownloadCode = `      if (btnDownloadHtml) {
        btnDownloadHtml.addEventListener("click", () => {
          try {
            const htmlContent = "<!doctype html>\\n" + document.documentElement.outerHTML;
            const blob = new Blob([htmlContent], { type: "text/html;charset=utf-8" });
            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "vocabulary_flashcards_800_1000.html";
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            showToast("HTML file downloaded! Open in any browser.");
            playHapticTick(640, "triangle", 0.06);
          } catch (err) {
            showToast("Download error: " + err.message);
          }
        });
      }`;

const newDownloadCode = `      if (btnDownloadHtml) {
        btnDownloadHtml.addEventListener("click", () => {
          try {
            // Get any saved user edits from localStorage
            const savedEdits = localStorage.getItem(STORAGE_KEY_EDITS) || "{}";
            let htmlDoc = "<!doctype html>\\n" + document.documentElement.outerHTML;

            // Bake custom user edits directly into the exported HTML so they are loaded on the phone immediately
            if (savedEdits && savedEdits !== "{}") {
              const injectScript = \`\\n    <script>\\n      // Auto-bake custom user edits into new device storage\\n      try {\\n        const current = localStorage.getItem("\${STORAGE_KEY_EDITS}");\\n        if (!current || current === "{}") {\\n          localStorage.setItem("\${STORAGE_KEY_EDITS}", \${JSON.stringify(savedEdits)});\\n        }\\n      } catch(e) {}\\n    <\\/script>\\n\`;
              htmlDoc = htmlDoc.replace("</body>", injectScript + "</body>");
            }

            const blob = new Blob([htmlDoc], { type: "text/html;charset=utf-8" });
            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "vocabulary_flashcards_800_1000.html";
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            showToast("HTML app downloaded! Open on your phone in any browser.");
            playHapticTick(640, "triangle", 0.06);
          } catch (err) {
            showToast("Download error: " + err.message);
          }
        });
      }`;

if (html.includes('a.download = "vocabulary_flashcards_800_1000.html";')) {
  // Replace download handler
  html = html.replace(oldDownloadCode, newDownloadCode);
  console.log('Updated btnDownloadHtml handler to bake in user edits!');
}

fs.writeFileSync('index.html', html);
console.log('Successfully updated index.html with universal device support!');
