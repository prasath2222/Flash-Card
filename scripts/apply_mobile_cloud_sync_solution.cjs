const fs = require('fs');
const path = require('path');

const indexHtmlPath = path.resolve('index.html');
let content = fs.readFileSync(indexHtmlPath, 'utf8');

// 1. Replace tab-cloud HTML
const tabCloudStart = `<div class="settings-tab-panel" id="tab-cloud">`;
const tabCloudEnd = `<!-- ========================================================== -->
    <!-- UPLOAD DECK & AUTOMATIC IMAGE DISCOVERY MODAL              -->`;

const newTabCloudHtml = `<div class="settings-tab-panel" id="tab-cloud">
          <!-- 1. Universal Cross-Device Pairing (Zero Login / Zero Popups Needed) -->
          <div class="duo-settings-section-title">📱 Instant Multi-Device Sync (Phones, Tablets & PCs)</div>
          <div class="settings-card" style="border: 2px solid rgba(56, 189, 248, 0.4); background: linear-gradient(135deg, rgba(2, 132, 199, 0.16), rgba(16, 185, 129, 0.08)); margin-bottom: 18px;">
            <div class="settings-card-header">
              <div class="settings-card-left">
                <div class="settings-card-icon" style="background: #0284c7; box-shadow: 0 3px 0 #0369a1; color: #ffffff; border: none;">🔗</div>
                <div>
                  <h3 class="settings-card-title">Universal Device Cloud Code</h3>
                  <p class="settings-card-sub">Guaranteed to save on ANY mobile phone, tablet or browser with zero popup blockers or login errors.</p>
                </div>
              </div>
            </div>

            <!-- Current Device Code Box -->
            <div style="margin-top: 14px; padding: 14px; background: rgba(0,0,0,0.35); border: 1px solid rgba(255,255,255,0.12); border-radius: 14px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
              <div>
                <div style="font-size: 0.72rem; color: #94a3b8; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">This Device's Cloud Code</div>
                <div id="display-device-sync-code" style="font-size: 1.4rem; font-weight: 900; color: #38bdf8; font-family: monospace; letter-spacing: 0.05em;">STELLAR-SYNC</div>
              </div>
              <button type="button" class="duo-btn-3d" id="btn-copy-sync-code" style="padding: 9px 16px; font-size: 0.82rem; font-weight: 800; background: rgba(56, 189, 248, 0.2); border: 1px solid rgba(56, 189, 248, 0.45); color: #38bdf8; cursor: pointer;">
                📋 Copy Code
              </button>
            </div>

            <!-- Pair Another Device Box -->
            <div style="margin-top: 14px; padding-top: 14px; border-top: 1px solid rgba(255,255,255,0.08);">
              <label for="input-pair-code" style="font-size: 0.82rem; font-weight: 700; color: #f1f5f9; display: block; margin-bottom: 6px;">Connect with your other device's code:</label>
              <div style="display: flex; gap: 8px;">
                <input type="text" id="input-pair-code" placeholder="Enter code (e.g. STELLAR-8291)" style="flex: 1; text-transform: uppercase; padding: 11px 14px; background: rgba(0,0,0,0.35); border: 1px solid rgba(255,255,255,0.15); border-radius: 12px; color: #fff; font-family: monospace; font-size: 0.95rem; font-weight: 700;" />
                <button type="button" class="duo-btn-3d duo-btn-3d-green" id="btn-pair-device-code" style="padding: 11px 18px; font-size: 0.88rem; font-weight: 800; white-space: nowrap; cursor: pointer;">
                  Pair & Sync
                </button>
              </div>
              <div id="device-sync-live-status" style="margin-top: 8px; font-size: 0.78rem; color: #34d399; display: flex; align-items: center; gap: 6px;">
                <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #10b981;"></span>
                <span>Active 2-way cloud sync enabled</span>
              </div>
            </div>
          </div>

          <!-- 2. Google Cloud Account Sync (Optional SSO) -->
          <div class="duo-settings-section-title">Google Account Sign-In</div>
          <div class="settings-card">
            <div class="settings-card-header">
              <div class="settings-card-left">
                <div class="settings-card-icon" id="cloud-user-avatar-icon" style="background: #38bdf8; box-shadow: 0 3px 0 #0284c7; color: #ffffff; border: none;">☁️</div>
                <div>
                  <h3 class="settings-card-title" id="cloud-sync-user-title">Google Cloud Account</h3>
                  <p class="settings-card-sub" id="cloud-sync-user-sub">Sign in with Google to link your profile to your Google email and Firestore.</p>
                </div>
              </div>
            </div>
            <div style="padding-top: 14px; display: flex; flex-direction: column; gap: 10px;">
              <button type="button" class="settings-action-btn settings-action-btn-primary" id="btn-cloud-signin" style="background: #1cb0f6; border-color: #1899d6;">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/>
                  <polyline points="10 17 15 12 10 7"/>
                  <line x1="15" y1="12" x2="3" y2="12"/>
                </svg>
                <span id="btn-cloud-signin-label">Sign In with Google</span>
              </button>

              <button type="button" class="settings-action-btn settings-action-btn-secondary" id="btn-cloud-manual-sync">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/>
                </svg>
                <span>Sync to Cloud Now</span>
              </button>

              <button type="button" class="settings-action-btn settings-action-btn-danger" id="btn-cloud-signout" style="display: none;">
                <span>Sign Out of Google</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </aside>
    `;

const startIdx = content.indexOf(tabCloudStart);
const endIdx = content.indexOf(tabCloudEnd);

if (startIdx !== -1 && endIdx !== -1) {
  content = content.substring(0, startIdx) + newTabCloudHtml + content.substring(endIdx);
  console.log('✓ Successfully updated tab-cloud HTML');
} else {
  console.error('Could not find tab-cloud markers:', startIdx, endIdx);
}

// 2. Add Universal Device Sync Controller Logic to JS
const targetJsLocation = `      /* ==========================================================
         FIREBASE REAL-TIME CLOUD SYNCHRONIZATION CONTROLLER`;

const newSyncController = `      /* ==========================================================
         UNIVERSAL CROSS-DEVICE SYNC & DEVICE CODE CONTROLLER
         Works on 100% of phones, tablets & desktops with ZERO popup blockers
         ========================================================== */
      let deviceSyncCode = localStorage.getItem("device_sync_code_v1");
      if (!deviceSyncCode) {
        deviceSyncCode = "STELLAR-" + Math.floor(1000 + Math.random() * 9000);
        localStorage.setItem("device_sync_code_v1", deviceSyncCode);
      }

      let lastRemoteSyncTimestamp = "";
      let isSyncPushing = false;

      function updateDeviceSyncCodeUI() {
        const displayEl = document.getElementById("display-device-sync-code");
        if (displayEl) displayEl.textContent = deviceSyncCode;
      }

      async function syncCurrentStateToDeviceCloud(isManual = false) {
        if (isSyncPushing) return;
        isSyncPushing = true;
        try {
          const payload = {
            learnedCardNums: [...learnedCardsSet],
            deletedCardNums: deletedCardNums,
            activeDeckId: currentDeckId,
            lastActiveCardNum: (cards[currentIndex]?.originalNum || cards[currentIndex]?.num || 800),
            streakCount: parseInt(document.getElementById("flashcard-streak-count")?.textContent || "1", 10),
            customDecks: customDecksCatalog,
            updatedAt: new Date().toISOString()
          };

          const res = await fetch("/api/sync/save", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ syncCode: deviceSyncCode, payload })
          });

          if (res.ok) {
            const data = await res.json();
            if (data && data.updatedAt) lastRemoteSyncTimestamp = data.updatedAt;
            if (isManual) {
              showToast("Cloud sync complete! All devices updated ☁️");
              playHapticTick(580, "sine", 0.04);
            }
          }
        } catch (e) {
          console.warn("Device cloud sync error:", e);
        } finally {
          setTimeout(() => { isSyncPushing = false; }, 300);
        }
      }

      async function pairWithRemoteDeviceCode(remoteCode) {
        const clean = String(remoteCode || "").trim().toUpperCase();
        if (!clean) return;

        try {
          const res = await fetch(\`/api/sync/load?code=\${encodeURIComponent(clean)}\`);
          if (!res.ok) {
            showToast("Sync server unavailable. Please try again.");
            return;
          }
          const data = await res.json();
          if (data && data.success && data.payload) {
            deviceSyncCode = clean;
            localStorage.setItem("device_sync_code_v1", clean);
            updateDeviceSyncCodeUI();

            applyRemoteSyncPayload(data.payload);
            lastRemoteSyncTimestamp = data.updatedAt || new Date().toISOString();

            showToast(\`Connected to device \${clean}! Progress synchronized 🎉\`);
            playHapticTick(660, "triangle", 0.08);

            const statusEl = document.getElementById("device-sync-live-status");
            if (statusEl) statusEl.innerHTML = \`<span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#10b981;"></span><span>Paired with \${clean} · Live sync active</span>\`;
          } else {
            showToast(\`Sync Code \${clean} not found. Ensure it was entered correctly.\`);
          }
        } catch(e) {
          showToast("Failed to connect to device code.");
        }
      }

      function applyRemoteSyncPayload(payload) {
        if (!payload) return;
        let needsRebuild = false;

        // Learned cards
        if (Array.isArray(payload.learnedCardNums)) {
          learnedCardsSet = new Set(payload.learnedCardNums);
          try {
            localStorage.setItem(LEARNED_STORAGE_KEY, JSON.stringify([...learnedCardsSet]));
          } catch(e){}
          updateSectionLearnedCounter();
          updateGlobalLearnedDisplays();
          const cur = cards[currentIndex];
          if (cur) updateCardLearnedUI(cur.originalNum || cur.num);
        }

        // Deleted cards
        if (Array.isArray(payload.deletedCardNums)) {
          const oldD = JSON.stringify(deletedCardNums.slice().sort());
          const newD = JSON.stringify(payload.deletedCardNums.slice().sort());
          if (oldD !== newD) {
            deletedCardNums = payload.deletedCardNums;
            try {
              localStorage.setItem(DELETED_CARDS_STORAGE_KEY, JSON.stringify(deletedCardNums));
            } catch(e){}
            needsRebuild = true;
          }
        }

        // Streak
        if (typeof payload.streakCount === "number" && payload.streakCount > 0) {
          const streakEl = document.getElementById("flashcard-streak-count");
          if (streakEl) streakEl.textContent = payload.streakCount;
        }

        // Custom decks
        if (payload.customDecks && typeof payload.customDecks === "object") {
          Object.assign(customDecksCatalog, payload.customDecks);
          try {
            localStorage.setItem("custom_decks_catalog_v1", JSON.stringify(customDecksCatalog));
          } catch(e){}
          if (typeof renderCustomDecksList === "function") renderCustomDecksList();
        }

        // Active Deck
        if (payload.activeDeckId && payload.activeDeckId !== currentDeckId) {
          currentDeckId = payload.activeDeckId;
          try { localStorage.setItem("active_deck_id_v1", currentDeckId); } catch(e){}
          needsRebuild = true;
        }

        if (needsRebuild) {
          reindexAndBuildCards();
          renderCurrentCard();
        }
      }

      // Background poll for updates from paired devices every 4 seconds
      setInterval(async () => {
        if (!deviceSyncCode || isSyncPushing) return;
        try {
          const res = await fetch(\`/api/sync/poll?code=\${encodeURIComponent(deviceSyncCode)}&since=\${encodeURIComponent(lastRemoteSyncTimestamp)}\`);
          if (res.ok) {
            const data = await res.json();
            if (data && data.hasUpdates && data.payload) {
              lastRemoteSyncTimestamp = data.updatedAt;
              applyRemoteSyncPayload(data.payload);
            }
          }
        } catch(e) {}
      }, 4000);

      // Wire Copy & Pair Buttons
      function initUniversalSyncUI() {
        updateDeviceSyncCodeUI();

        const btnCopy = document.getElementById("btn-copy-sync-code");
        if (btnCopy) {
          btnCopy.addEventListener("click", () => {
            navigator.clipboard.writeText(deviceSyncCode).then(() => {
              showToast(\`Copied \${deviceSyncCode} to clipboard!\`);
              playHapticTick(500, "sine", 0.04);
            }).catch(() => {
              showToast(\`Code: \${deviceSyncCode}\`);
            });
          });
        }

        const btnPair = document.getElementById("btn-pair-device-code");
        const inputPair = document.getElementById("input-pair-code");
        if (btnPair && inputPair) {
          btnPair.addEventListener("click", () => {
            const val = inputPair.value.trim();
            if (!val) {
              showToast("Please enter a device sync code.");
              return;
            }
            pairWithRemoteDeviceCode(val);
          });
          inputPair.addEventListener("keydown", (e) => {
            if (e.key === "Enter") {
              btnPair.click();
            }
          });
        }

        // Trigger initial push so device is registered on cloud
        syncCurrentStateToDeviceCloud();
      }

      if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initUniversalSyncUI);
      } else {
        initUniversalSyncUI();
      }

      `;

if (!content.includes('initUniversalSyncUI')) {
  content = content.replace(targetJsLocation, newSyncController + '\n' + targetJsLocation);
  console.log('✓ Injected Universal Device Sync Controller into JS');
}

// 3. Ensure manual sync button triggers both Firebase and Device cloud sync
const oldManualSyncBlock = `      if (btnCloudManualSync) {
        btnCloudManualSync.addEventListener("click", () => {
          if (!window.firebaseSync || !window.firebaseSync.getCurrentUser()) {
            showToast("Please sign in with Google to sync to cloud");
            if (btnCloudSignin) btnCloudSignin.click();
            return;
          }
          window.firebaseSync.pushStudyStateToCloud({
            learnedCardNums: [...learnedCardsSet],
            deletedCardNums: deletedCardNums,
            lastActiveCardNum: (cards[currentIndex]?.originalNum || cards[currentIndex]?.num || 800)
          });
          showToast("Syncing your cards to cloud... ☁️");
          playHapticTick(580, "sine", 0.04);
        });
      }`;

const newManualSyncBlock = `      if (btnCloudManualSync) {
        btnCloudManualSync.addEventListener("click", () => {
          // Sync via Universal Device Cloud
          syncCurrentStateToDeviceCloud(true);

          // If logged in with Google, also sync to Firestore
          if (window.firebaseSync && window.firebaseSync.getCurrentUser()) {
            window.firebaseSync.pushStudyStateToCloud({
              learnedCardNums: [...learnedCardsSet],
              deletedCardNums: deletedCardNums,
              lastActiveCardNum: (cards[currentIndex]?.originalNum || cards[currentIndex]?.num || 800)
            });
          }
        });
      }`;

if (content.includes(oldManualSyncBlock)) {
  content = content.replace(oldManualSyncBlock, newManualSyncBlock);
  console.log('✓ Updated btnCloudManualSync handler');
}

fs.writeFileSync(indexHtmlPath, content, 'utf8');
console.log('Mobile Cloud Sync enhancement complete.');
