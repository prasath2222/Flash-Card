const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

// 1. Add CSS for device modal
const deviceModalCss = `
      /* Header Device Access Button & Modal Styles */
      .header-tool-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 32px;
        height: 32px;
        padding: 0;
        border-radius: 10px;
        background: rgba(56, 189, 248, 0.12);
        border: 1px solid rgba(56, 189, 248, 0.32);
        color: var(--accent-cyan);
        cursor: pointer;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25);
        flex-shrink: 0;
      }

      .header-tool-btn:active {
        transform: scale(0.92);
        background: rgba(56, 189, 248, 0.25);
      }

      .device-modal-content {
        display: flex;
        flex-direction: column;
        gap: 12px;
        overflow-y: auto;
        padding-bottom: 4px;
      }

      .device-option-card {
        background: rgba(255, 255, 255, 0.035);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 12px 14px;
        display: flex;
        flex-direction: column;
        gap: 8px;
      }

      .device-card-header {
        display: flex;
        align-items: flex-start;
        gap: 10px;
      }

      .device-icon {
        font-size: 1.25rem;
        flex-shrink: 0;
      }

      .device-card-info {
        display: flex;
        flex-direction: column;
        gap: 2px;
      }

      .device-card-title {
        font-size: 0.88rem;
        font-weight: 700;
        color: #f8fafc;
      }

      .device-card-desc {
        font-size: 0.74rem;
        color: #94a3b8;
        line-height: 1.35;
      }

      .device-action-row {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-top: 4px;
      }

      .device-url-input {
        flex: 1;
        background: #090f1d;
        border: 1px solid #1e293b;
        border-radius: 10px;
        padding: 8px 10px;
        color: #94a3b8;
        font-size: 0.74rem;
        font-family: monospace;
        outline: none;
      }

      .btn-copy-url {
        background: rgba(56, 189, 248, 0.16);
        border: 1px solid rgba(56, 189, 248, 0.35);
        color: var(--accent-cyan);
        border-radius: 10px;
        padding: 8px 14px;
        font-size: 0.76rem;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.15s ease;
        flex-shrink: 0;
      }

      .btn-copy-url:active {
        background: rgba(56, 189, 248, 0.35);
        transform: scale(0.96);
      }

      .btn-download-html {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.2), rgba(99, 102, 241, 0.2));
        border: 1px solid rgba(56, 189, 248, 0.4);
        color: #ffffff;
        border-radius: 12px;
        padding: 10px 14px;
        font-size: 0.82rem;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.18s ease;
        margin-top: 2px;
      }

      .btn-download-html:active {
        transform: scale(0.97);
        filter: brightness(1.15);
      }

      .device-steps-list {
        display: flex;
        flex-direction: column;
        gap: 6px;
        font-size: 0.75rem;
        color: #cbd5e1;
        line-height: 1.4;
        background: rgba(0, 0, 0, 0.2);
        padding: 8px 10px;
        border-radius: 10px;
      }

      .device-step-item strong {
        color: var(--accent-cyan);
      }

      .device-step-item em {
        color: #fde68a;
        font-style: normal;
      }
`;

if (!html.includes('.header-tool-btn {')) {
  html = html.replace('/* Floating Toast Notification */', deviceModalCss + '\n      /* Floating Toast Notification */');
  console.log('Added device modal CSS');
}

// 2. Add button in header
const deviceHeaderBtnHtml = `            <button
              class="header-tool-btn"
              id="btn-device-modal"
              title="Use on any device, phone, or download HTML"
              aria-label="Use on any device"
            >
              <svg
                width="15"
                height="15"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2.3"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <rect width="14" height="20" x="5" y="2" rx="2" ry="2" />
                <path d="M12 18h.01" />
              </svg>
            </button>`;

if (!html.includes('id="btn-device-modal"')) {
  html = html.replace(
    'aria-label="Shuffle cards"\n            >',
    'aria-label="Shuffle cards"\n            >'
  );
  html = html.replace(
    '</button>\n            <div class="counter-badge"',
    '</button>\n' + deviceHeaderBtnHtml + '\n            <div class="counter-badge"'
  );
  console.log('Added device modal trigger button to header');
}

// 3. Add Device Modal HTML
const deviceModalHtml = `
    <!-- Use on Any Device / Offline HTML Modal -->
    <div class="modal-backdrop" id="device-modal">
      <div class="modal-sheet">
        <div class="modal-handle"></div>
        <div class="modal-header">
          <div class="edit-modal-title-group">
            <span class="modal-title">Use on Any Device</span>
            <span class="edit-badge">Universal</span>
          </div>
          <button class="modal-close-btn" id="device-modal-close-btn" aria-label="Close">&times;</button>
        </div>

        <div class="device-modal-content">
          <!-- Option 1: Live Web App Link -->
          <div class="device-option-card">
            <div class="device-card-header">
              <span class="device-icon">🌐</span>
              <div class="device-card-info">
                <span class="device-card-title">Live Web App Link</span>
                <span class="device-card-desc">Works on any browser (Chrome, Safari, Edge, Android, iPhone, PC)</span>
              </div>
            </div>
            <div class="device-action-row">
              <input type="text" class="device-url-input" id="device-url-display" readonly value="https://ais-pre-kgrpdx7hnunkkpn4rtvjsl-444550834163.asia-east1.run.app" />
              <button type="button" class="btn-copy-url" id="btn-copy-url">Copy Link</button>
            </div>
          </div>

          <!-- Option 2: Download Standalone HTML -->
          <div class="device-option-card">
            <div class="device-card-header">
              <span class="device-icon">💾</span>
              <div class="device-card-info">
                <span class="device-card-title">Download Standalone HTML File</span>
                <span class="device-card-desc">Single-file deck with all 199 cards & shortcuts. Double-click to open anywhere!</span>
              </div>
            </div>
            <button type="button" class="btn-download-html" id="btn-download-html">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                <polyline points="7 10 12 15 17 10" />
                <line x1="12" y1="15" x2="12" y2="3" />
              </svg>
              <span>Download HTML File (.html)</span>
            </button>
          </div>

          <!-- Option 3: Install on Phone Guide -->
          <div class="device-option-card">
            <div class="device-card-header">
              <span class="device-icon">📱</span>
              <div class="device-card-info">
                <span class="device-card-title">Install as Phone App</span>
                <span class="device-card-desc">Add directly to your iPhone or Android home screen with zero app store needed</span>
              </div>
            </div>
            <div class="device-steps-list">
              <div class="device-step-item">
                <strong>iPhone (Safari):</strong> Tap Share button → select <em>"Add to Home Screen"</em>
              </div>
              <div class="device-step-item">
                <strong>Android (Chrome):</strong> Tap Menu (⋮) → select <em>"Install app"</em> or <em>"Add to Home screen"</em>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
`;

if (!html.includes('id="device-modal"')) {
  html = html.replace('<!-- Floating Toast Notification -->', deviceModalHtml + '\n    <!-- Floating Toast Notification -->');
  console.log('Added device modal HTML sheet');
}

// 4. Add JavaScript handlers for Device Modal & Standalone Download
const deviceJsSnippet = `
      // Device Access & Standalone HTML Export Controller
      const btnDeviceModal = document.getElementById("btn-device-modal");
      const deviceModal = document.getElementById("device-modal");
      const deviceModalCloseBtn = document.getElementById("device-modal-close-btn");
      const btnCopyUrl = document.getElementById("btn-copy-url");
      const deviceUrlDisplay = document.getElementById("device-url-display");
      const btnDownloadHtml = document.getElementById("btn-download-html");

      function openDeviceModal() {
        if (!deviceModal) return;
        if (deviceUrlDisplay) {
          deviceUrlDisplay.value = window.location.href.split('?')[0];
        }
        deviceModal.classList.add("open");
        playHapticTick(500, "sine", 0.04);
      }

      function closeDeviceModal() {
        if (deviceModal) deviceModal.classList.remove("open");
      }

      if (btnDeviceModal) {
        btnDeviceModal.addEventListener("click", openDeviceModal);
      }
      if (deviceModalCloseBtn) {
        deviceModalCloseBtn.addEventListener("click", closeDeviceModal);
      }
      if (deviceModal) {
        deviceModal.addEventListener("click", (e) => {
          if (e.target === deviceModal) closeDeviceModal();
        });
      }

      if (btnCopyUrl) {
        btnCopyUrl.addEventListener("click", async () => {
          const url = deviceUrlDisplay ? deviceUrlDisplay.value : window.location.href;
          try {
            if (navigator.clipboard) {
              await navigator.clipboard.writeText(url);
            } else {
              deviceUrlDisplay.select();
              document.execCommand("copy");
            }
            showToast("App URL copied to clipboard!");
            playHapticTick(600, "sine", 0.05);
          } catch (e) {
            showToast("Copied: " + url);
          }
        });
      }

      if (btnDownloadHtml) {
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
      }
`;

if (!html.includes('const btnDeviceModal =')) {
  html = html.replace('// Quick Shortcut Edit Modal Elements', deviceJsSnippet + '\n      // Quick Shortcut Edit Modal Elements');
  console.log('Added device modal JS handlers');
}

fs.writeFileSync('index.html', html);
console.log('Successfully added universal device support and HTML export!');
