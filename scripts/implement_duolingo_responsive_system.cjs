const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

// =========================================================================
// 1. CLEAN UP ASIDE (app-desktop-sidebar) TO EXACT PRODUCTION GRADE MARKUP
// =========================================================================
const asideStart = html.indexOf('<aside class="app-desktop-sidebar"');
const asideEnd = html.indexOf('</aside>', asideStart) + '</aside>'.length;

const cleanAsideHtml = `<aside class="app-desktop-sidebar" id="app-desktop-sidebar" aria-label="Main Navigation">
        <div class="sidebar-main-group">
          <!-- Brand Wordmark with Lexi Mascot -->
          <div class="sidebar-brand-lockup" id="sidebar-brand-home" title="Stellar Home">
            <svg width="40" height="40" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg" class="brand-mascot-svg">
              <defs>
                <linearGradient id="owlBodyGrad" x1="32" y1="12" x2="32" y2="58" gradientUnits="userSpaceOnUse">
                  <stop stop-color="#10b981"/>
                  <stop offset="1" stop-color="#059669"/>
                </linearGradient>
                <linearGradient id="owlBellyGrad" x1="32" y1="30" x2="32" y2="52" gradientUnits="userSpaceOnUse">
                  <stop stop-color="#f0fdf4"/>
                  <stop offset="1" stop-color="#d1fae5"/>
                </linearGradient>
                <linearGradient id="capGrad" x1="32" y1="4" x2="32" y2="18" gradientUnits="userSpaceOnUse">
                  <stop stop-color="#1e293b"/>
                  <stop offset="1" stop-color="#0f172a"/>
                </linearGradient>
              </defs>
              <!-- Ear Feathers -->
              <path d="M16 18L22 24L14 26L16 18Z" fill="#047857"/>
              <path d="M48 18L42 24L50 26L48 18Z" fill="#047857"/>
              <!-- Body -->
              <rect x="14" y="16" width="36" height="40" rx="18" fill="url(#owlBodyGrad)"/>
              <!-- Belly -->
              <ellipse cx="32" cy="42" rx="12" ry="11" fill="url(#owlBellyGrad)"/>
              <path d="M28 38C29.5 40 34.5 40 36 38" stroke="#10b981" stroke-width="1.8" stroke-linecap="round" fill="none"/>
              <path d="M26 43C28.5 45 35.5 45 38 43" stroke="#10b981" stroke-width="1.8" stroke-linecap="round" fill="none"/>
              <!-- Big Friendly Eyes -->
              <circle cx="24" cy="28" r="8" fill="#ffffff"/>
              <circle cx="40" cy="28" r="8" fill="#ffffff"/>
              <circle cx="25" cy="28" r="4.5" fill="#0f172a"/>
              <circle cx="39" cy="28" r="4.5" fill="#0f172a"/>
              <circle cx="23.5" cy="26.5" r="1.8" fill="#ffffff"/>
              <circle cx="37.5" cy="26.5" r="1.8" fill="#ffffff"/>
              <!-- Beak -->
              <polygon points="32,32 29,36 35,36" fill="#f59e0b"/>
              <!-- Spectacles -->
              <circle cx="24" cy="28" r="8.2" stroke="#f59e0b" stroke-width="1.8" fill="none"/>
              <circle cx="40" cy="28" r="8.2" stroke="#f59e0b" stroke-width="1.8" fill="none"/>
              <line x1="32.2" y1="28" x2="31.8" y2="28" stroke="#f59e0b" stroke-width="2" stroke-linecap="round"/>
              <!-- Academic Cap -->
              <polygon points="32,6 50,12 32,18 14,12" fill="url(#capGrad)"/>
              <rect x="24" y="15" width="16" height="4" rx="1" fill="#0f172a"/>
              <line x1="32" y1="12" x2="44" y2="16" stroke="#fbbf24" stroke-width="1.5" stroke-linecap="round"/>
              <circle cx="44" cy="18" r="1.5" fill="#fbbf24"/>
              <!-- Feet -->
              <rect x="22" y="54" width="6" height="3" rx="1.5" fill="#f59e0b"/>
              <rect x="36" y="54" width="6" height="3" rx="1.5" fill="#f59e0b"/>
            </svg>
            <div class="sidebar-brand-text">
              <span class="sidebar-brand-title">Stellar</span>
              <span class="sidebar-brand-sub">Vocabulary Mastery</span>
            </div>
          </div>

          <!-- Tactile Navigation Tabs -->
          <nav class="sidebar-nav-list">
            <button type="button" class="sidebar-nav-btn active" id="nav-btn-home" title="Learn Home">
              <span class="sidebar-nav-icon">🏠</span>
              <span class="sidebar-nav-label">Learn Home</span>
            </button>
            <button type="button" class="sidebar-nav-btn" id="nav-btn-3k" title="3k Vocabulary (800 – 1000)">
              <span class="sidebar-nav-icon">⚡</span>
              <span class="sidebar-nav-label">3k Vocabulary</span>
            </button>
            <button type="button" class="sidebar-nav-btn" id="nav-btn-sections" title="My Sections">
              <span class="sidebar-nav-icon">📚</span>
              <span class="sidebar-nav-label">My Sections</span>
            </button>
            <button type="button" class="sidebar-nav-btn" id="nav-btn-settings" title="Audio & Settings">
              <span class="sidebar-nav-icon">⚙️</span>
              <span class="sidebar-nav-label">Settings</span>
            </button>
          </nav>
        </div>

        <!-- Sidebar Footer Status & Quick Sound -->
        <div class="sidebar-footer-card">
          <div class="sidebar-streak-badge">
            <span>⚡</span>
            <span class="sidebar-footer-label">Target: 3,000 Words</span>
          </div>
          <div class="sidebar-sound-quick-toggle" id="sidebar-quick-sound" title="Toggle audio sound FX">
            <span class="sidebar-footer-label">Sound FX</span>
            <span id="sidebar-sound-indicator" style="color: #34d399; font-weight: 700;">ON 🔊</span>
          </div>
        </div>
      </aside>`;

html = html.slice(0, asideStart) + cleanAsideHtml + html.slice(asideEnd);
console.log('Cleaned sidebar HTML!');

// =========================================================================
// 2. REMOVE ARTIFICIAL SIDEBAR BACKDROP IF PRESENT
// =========================================================================
html = html.replace(/<!--\s*Sidebar Backdrop for overlay mode\s*-->\s*<div class="sidebar-backdrop"[^>]*><\/div>/g, '');
html = html.replace(/<div class="sidebar-backdrop"[^>]*><\/div>/g, '');
console.log('Removed artificial sidebar-backdrop!');

// =========================================================================
// 3. CLEAN UP DESKTOP-TOP-HEADER (PINNED FAR LEFT AND FAR RIGHT CORNERS)
// =========================================================================
const oldHeaderPattern = /<header class="desktop-top-header">[\s\S]*?<\/header>/;
const cleanHeaderHtml = `<header class="desktop-top-header">
          <div class="desktop-header-left">
            <span class="desktop-page-breadcrumb" id="desktop-breadcrumb-text">Dashboard · Choose Your Learning Path</span>
          </div>
          <div class="desktop-header-stats">
            <!-- Global Status 1 to 3K Learned Pinned to FAR RIGHT CORNER -->
            <div class="stat-badge-duo stat-badge-mastery" id="desktop-3k-status-badge" title="Status across 3,000 words">
              <span>⚡</span>
              <span>Status: <strong id="desktop-status-count">0</strong> / 3,000</span>
            </div>
          </div>
        </header>`;

html = html.replace(oldHeaderPattern, cleanHeaderHtml);
console.log('Cleaned desktop-top-header HTML!');

// =========================================================================
// 4. CLEAN UP CSS: REMOVE PREVIOUS EXPERIMENTAL ADDITION & INSERT DUOLINGO 3-TIER ENGINE
// =========================================================================
const cssOldMarker = '/* ========================================================== */\n      /* CRITICAL MASTER RESPONSIVE LAYOUT & SIDEBAR CONTROLS';
const cssIdx = html.indexOf(cssOldMarker);
if (cssIdx !== -1) {
  const cssEnd = html.indexOf('</style>', cssIdx);
  html = html.slice(0, cssIdx) + html.slice(cssEnd);
  console.log('Removed old experimental responsive CSS block');
}

const styleClose = html.indexOf('</style>');
const duolingoCss = `
      /* ========================================================== */
      /* DUOLINGO 3-TIER PRODUCTION RESPONSIVE ENGINE               */
      /* ========================================================== */
      #app-container {
        display: flex !important;
        flex-direction: row !important;
        width: 100% !important;
        min-height: 100vh !important;
        position: relative !important;
        background: #090e1a !important;
        overflow-x: hidden !important;
      }

      /* Core Sidebar */
      .app-desktop-sidebar {
        height: 100vh !important;
        background: #0b1120 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
        box-sizing: border-box !important;
        position: fixed !important;
        left: 0 !important;
        top: 0 !important;
        bottom: 0 !important;
        z-index: 50 !important;
        overflow-y: auto !important;
        overflow-x: hidden !important;
        transition: width 0.22s cubic-bezier(0.16, 1, 0.3, 1), padding 0.22s ease !important;
      }

      .sidebar-main-group {
        display: flex !important;
        flex-direction: column !important;
        width: 100% !important;
      }

      .sidebar-brand-lockup {
        display: flex !important;
        align-items: center !important;
        gap: 12px !important;
        padding-bottom: 20px !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.07) !important;
        cursor: pointer !important;
        text-decoration: none !important;
      }
      .sidebar-brand-text {
        display: flex !important;
        flex-direction: column !important;
      }
      .sidebar-brand-title {
        font-size: 1.25rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em !important;
        color: #ffffff !important;
        line-height: 1.1 !important;
      }
      .sidebar-brand-sub {
        font-size: 0.72rem !important;
        font-weight: 600 !important;
        color: #10b981 !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
      }

      .sidebar-nav-list {
        display: flex !important;
        flex-direction: column !important;
        gap: 8px !important;
        margin-top: 18px !important;
        width: 100% !important;
      }

      /* Duolingo 3D Tactile Sidebar Buttons */
      .sidebar-nav-btn {
        display: flex !important;
        align-items: center !important;
        gap: 14px !important;
        border-radius: 16px !important;
        background: transparent !important;
        border: 2px solid transparent !important;
        color: #94a3b8 !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        cursor: pointer !important;
        transition: all 0.16s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        text-align: left !important;
        width: 100% !important;
        box-sizing: border-box !important;
      }
      .sidebar-nav-btn:hover {
        background: rgba(255, 255, 255, 0.05) !important;
        color: #ffffff !important;
      }
      .sidebar-nav-btn.active {
        background: rgba(16, 185, 129, 0.12) !important;
        border-color: rgba(16, 185, 129, 0.4) !important;
        color: #34d399 !important;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.15), 0 3px 0 #059669 !important;
        transform: translateY(-1px) !important;
      }
      .sidebar-nav-btn:active {
        transform: translateY(1px) !important;
        box-shadow: 0 1px 0 #059669 !important;
      }

      .sidebar-nav-icon {
        font-size: 1.25rem !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 28px !important;
        height: 28px !important;
        flex-shrink: 0 !important;
      }

      /* Sidebar Footer Card */
      .sidebar-footer-card {
        padding: 14px !important;
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 16px !important;
        display: flex !important;
        flex-direction: column !important;
        gap: 10px !important;
        width: 100% !important;
        box-sizing: border-box !important;
      }
      .sidebar-streak-badge {
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
        font-size: 0.82rem !important;
        font-weight: 700 !important;
        color: #fbbf24 !important;
      }
      .sidebar-sound-quick-toggle {
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        font-size: 0.8rem !important;
        color: #94a3b8 !important;
        cursor: pointer !important;
        padding: 6px 10px !important;
        border-radius: 10px !important;
        background: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
      }

      /* Common Main Viewport */
      .app-main-viewport {
        flex: 1 1 auto !important;
        min-height: 100vh !important;
        height: auto !important;
        display: flex !important;
        flex-direction: column !important;
        position: relative !important;
        overflow-y: auto !important;
        overflow-x: hidden !important;
        background: #090e1a !important;
        box-sizing: border-box !important;
        transition: margin-left 0.22s cubic-bezier(0.16, 1, 0.3, 1), width 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
      }

      /* ========================================================== */
      /* TIER 1: DESKTOP (>= 1024px) - FULL EXPANDED DUOLINGO SIDEBAR */
      /* ========================================================== */
      @media (min-width: 1024px) {
        .app-desktop-sidebar {
          width: 256px !important;
          min-width: 256px !important;
          max-width: 256px !important;
          padding: 24px 16px !important;
          display: flex !important;
        }
        .sidebar-brand-text {
          display: flex !important;
        }
        .sidebar-nav-label, .sidebar-footer-label {
          display: inline !important;
        }
        .sidebar-nav-btn {
          justify-content: flex-start !important;
          padding: 12px 16px !important;
        }
        .app-main-viewport {
          margin-left: 256px !important;
          width: calc(100% - 256px) !important;
        }
        .desktop-top-header {
          display: flex !important;
        }
        .mobile-top-bar {
          display: none !important;
        }
        .mobile-bottom-nav {
          display: none !important;
        }
      }

      /* ========================================================== */
      /* TIER 2: TABLET / NARROW DESKTOP (768px - 1023px)           */
      /* DUOLINGO ICON RAIL (Image 2 in user upload!)               */
      /* ========================================================== */
      @media (min-width: 768px) and (max-width: 1023px) {
        .app-desktop-sidebar {
          width: 76px !important;
          min-width: 76px !important;
          max-width: 76px !important;
          padding: 20px 8px !important;
          display: flex !important;
          align-items: center !important;
        }
        .sidebar-brand-lockup {
          justify-content: center !important;
          padding-bottom: 14px !important;
          width: 100% !important;
        }
        .sidebar-brand-text {
          display: none !important; /* Hide text, keep only mascot! */
        }
        .sidebar-nav-list {
          align-items: center !important;
          width: 100% !important;
          gap: 12px !important;
        }
        .sidebar-nav-label {
          display: none !important; /* Hide labels, keep only tactile icons! */
        }
        .sidebar-nav-btn {
          width: 52px !important;
          height: 52px !important;
          min-width: 52px !important;
          padding: 0 !important;
          justify-content: center !important;
          border-radius: 16px !important;
        }
        .sidebar-footer-card {
          padding: 8px 4px !important;
          align-items: center !important;
          background: transparent !important;
          border: none !important;
        }
        .sidebar-footer-label {
          display: none !important;
        }
        .sidebar-sound-quick-toggle {
          padding: 8px !important;
          justify-content: center !important;
          border-radius: 12px !important;
        }
        .app-main-viewport {
          margin-left: 76px !important;
          width: calc(100% - 76px) !important;
        }
        .desktop-top-header {
          display: flex !important;
          padding: 14px 20px !important;
        }
        .mobile-top-bar {
          display: none !important;
        }
        .mobile-bottom-nav {
          display: none !important;
        }
      }

      /* ========================================================== */
      /* TIER 3: MOBILE PHONES (< 768px)                            */
      /* DUOLINGO MOBILE: TOP BAR + CONTENT + THUMB ZONE BOTTOM BAR */
      /* ========================================================== */
      @media (max-width: 767px) {
        .app-desktop-sidebar {
          display: none !important; /* Hidden on mobile! */
        }
        .app-main-viewport {
          margin-left: 0 !important;
          width: 100% !important;
          padding-bottom: 78px !important;
        }
        .desktop-top-header {
          display: none !important;
        }
        .mobile-top-bar {
          display: flex !important;
        }
        .mobile-bottom-nav {
          display: grid !important;
        }
      }

      /* Flashcard Full Immersion Mode (Distraction-Free) */
      body.in-flashcard-mode .app-desktop-sidebar,
      body.in-flashcard-mode .desktop-top-header,
      body.in-flashcard-mode .mobile-top-bar,
      body.in-flashcard-mode .mobile-bottom-nav {
        display: none !important;
      }
      body.in-flashcard-mode .app-main-viewport {
        margin-left: 0 !important;
        width: 100% !important;
        padding-bottom: 0 !important;
        min-height: 100vh !important;
        height: 100vh !important;
        overflow: hidden !important;
      }

      /* Desktop Top Header Corner Separation */
      .desktop-top-header {
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: space-between !important;
        padding: 16px 32px !important;
        background: rgba(11, 17, 32, 0.85) !important;
        backdrop-filter: blur(14px) !important;
        -webkit-backdrop-filter: blur(14px) !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
        position: sticky !important;
        top: 0 !important;
        z-index: 40 !important;
        flex-shrink: 0 !important;
      }
      .desktop-header-left {
        display: flex !important;
        align-items: center !important;
        gap: 12px !important;
        min-width: 0 !important;
        flex: 1 1 auto !important;
      }
      .desktop-page-breadcrumb {
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        color: #f1f5f9 !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        min-width: 0 !important;
      }
      .desktop-header-stats {
        display: flex !important;
        align-items: center !important;
        gap: 12px !important;
        flex: 0 0 auto !important;
        margin-left: auto !important;
      }
`;

html = html.slice(0, styleClose) + duolingoCss + html.slice(styleClose);
console.log('Injected Duolingo 3-Tier CSS engine!');

// =========================================================================
// 5. CLEAN UP JAVASCRIPT: REPLACE PREVIOUS EXPERIMENTAL BLOCK WITH MASTER WIRING
// =========================================================================
const jsOldMarker = '// ==========================================================\n      // MASTER SIDEBAR & NAVIGATION CONTROLS';
const jsIdx = html.indexOf(jsOldMarker);
if (jsIdx !== -1) {
  const jsEnd = html.lastIndexOf('</script>');
  html = html.slice(0, jsIdx) + html.slice(jsEnd);
  console.log('Removed old experimental JS block');
}

const scriptClose = html.lastIndexOf('</script>');
const masterJs = `
      // ==========================================================
      // MASTER DUOLINGO NAVIGATION WIRE-UPS (All Tiers & Devices)
      // ==========================================================
      (function initDuolingoNav() {
        // Tab click handlers (Sidebar buttons & Mobile bottom nav)
        const navHome = document.getElementById("nav-btn-home");
        if (navHome) navHome.addEventListener("click", () => switchScreen("screen-home"));

        const nav3k = document.getElementById("nav-btn-3k");
        if (nav3k) nav3k.addEventListener("click", () => switchScreen("screen-subsections"));

        const navSections = document.getElementById("nav-btn-sections");
        if (navSections) navSections.addEventListener("click", () => {
          switchScreen("screen-home");
          setTimeout(() => {
            const addBtn = document.getElementById("btn-open-add-section");
            if (addBtn) addBtn.scrollIntoView({ behavior: "smooth", block: "center" });
          }, 120);
        });

        const navSettings = document.getElementById("nav-btn-settings");
        if (navSettings) navSettings.addEventListener("click", () => {
          if (typeof openMenuDrawer === "function") openMenuDrawer();
        });

        const brandHome = document.getElementById("sidebar-brand-home");
        if (brandHome) brandHome.addEventListener("click", () => switchScreen("screen-home"));

        // Mobile Bottom Bar Tabs
        const mobHome = document.getElementById("mob-tab-home");
        if (mobHome) mobHome.addEventListener("click", () => switchScreen("screen-home"));

        const mob3k = document.getElementById("mob-tab-3k");
        if (mob3k) mob3k.addEventListener("click", () => switchScreen("screen-subsections"));

        const mobSections = document.getElementById("mob-tab-sections");
        if (mobSections) mobSections.addEventListener("click", () => {
          switchScreen("screen-home");
          setTimeout(() => {
            const addBtn = document.getElementById("btn-open-add-section");
            if (addBtn) addBtn.scrollIntoView({ behavior: "smooth", block: "center" });
          }, 120);
        });

        const mobSettings = document.getElementById("mob-tab-settings");
        if (mobSettings) mobSettings.addEventListener("click", () => {
          if (typeof openMenuDrawer === "function") openMenuDrawer();
        });

        const mobHamburger = document.getElementById("mobile-hamburger-btn");
        if (mobHamburger) mobHamburger.addEventListener("click", () => {
          if (typeof openMenuDrawer === "function") openMenuDrawer();
        });

        // Subsections Study Deck Button -> Enters Flashcard mode
        const btnResumeFromSub = document.getElementById("btn-resume-from-subsections");
        if (btnResumeFromSub) btnResumeFromSub.addEventListener("click", () => switchScreen("screen-flashcard"));

        const tier800Card = document.getElementById("sub-tier-800-1000");
        if (tier800Card) tier800Card.addEventListener("click", (e) => {
          if (e.target.closest("button")) return;
          switchScreen("screen-flashcard");
        });

        // 3K Vocab Card on Home -> Enters Subsections (Cards 800-1000)
        const btnOpenSub = document.getElementById("btn-open-subsections");
        if (btnOpenSub) btnOpenSub.addEventListener("click", () => switchScreen("screen-subsections"));

        const card3k = document.getElementById("card-3k-featured");
        if (card3k) card3k.addEventListener("click", (e) => {
          if (e.target.closest("button")) return;
          switchScreen("screen-subsections");
        });

        // Centered Add Section Buttons on Both Screens
        const btnAddHome = document.getElementById("btn-open-add-section");
        const btnAddSub = document.getElementById("btn-subsections-add-section");
        const modalAdd = document.getElementById("modal-add-section");
        const closeAdd = document.getElementById("btn-close-add-section");
        const cancelAdd = document.getElementById("btn-cancel-add-section");

        function openAddModal() {
          if (modalAdd) {
            modalAdd.classList.add("open");
            const input = document.getElementById("input-section-title");
            if (input) { input.value = ""; input.focus(); }
          }
        }
        function closeAddModal() {
          if (modalAdd) modalAdd.classList.remove("open");
        }

        if (btnAddHome) btnAddHome.addEventListener("click", openAddModal);
        if (btnAddSub) btnAddSub.addEventListener("click", openAddModal);
        if (closeAdd) closeAdd.addEventListener("click", closeAddModal);
        if (cancelAdd) cancelAdd.addEventListener("click", closeAddModal);

        if (modalAdd) {
          modalAdd.addEventListener("click", (e) => {
            if (e.target === modalAdd) closeAddModal();
          });
        }

        // Quick Sound FX Toggle in Sidebar
        const quickSound = document.getElementById("sidebar-quick-sound");
        const soundIndicator = document.getElementById("sidebar-sound-indicator");
        if (quickSound && soundIndicator) {
          quickSound.addEventListener("click", () => {
            const isMuted = soundIndicator.textContent.includes("OFF");
            if (isMuted) {
              soundIndicator.textContent = "ON 🔊";
              soundIndicator.style.color = "#34d399";
              if (typeof playHapticTick === "function") playHapticTick(520, "sine", 0.05);
            } else {
              soundIndicator.textContent = "OFF 🔇";
              soundIndicator.style.color = "#94a3b8";
            }
          });
        }
      })();
`;

html = html.slice(0, scriptClose) + masterJs + html.slice(scriptClose);
console.log('Injected master Duolingo JavaScript wiring!');

fs.writeFileSync('index.html', html, 'utf8');
console.log('Wrote clean index.html! New length:', html.length);
