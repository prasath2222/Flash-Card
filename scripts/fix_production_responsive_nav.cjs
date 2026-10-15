const fs = require('fs');
const path = require('path');

const indexPath = path.join(__dirname, '..', 'index.html');
let html = fs.readFileSync(indexPath, 'utf8');

console.log('Original index.html length:', html.length);

// 1. Change all brand "Stellar" references to Violet instead of Green
// Replace in CSS:
html = html.replace(/color:\s*#58cc02\s*!important/g, 'color: #a855f7 !important');
html = html.replace(/text-shadow:\s*0\s*2px\s*14px\s*rgba\(88,\s*204,\s*2,\s*0\.32\)\s*!important/g, 'text-shadow: 0 0 18px rgba(168, 85, 247, 0.45) !important');
html = html.replace(/text-shadow:\s*0\s*2px\s*10px\s*rgba\(88,\s*204,\s*2,\s*0\.28\)\s*!important/g, 'text-shadow: 0 0 16px rgba(168, 85, 247, 0.4) !important');
html = html.replace(/color:\s*#58cc02/g, 'color: #a855f7');
console.log('Updated brand color to Violet (#a855f7)');

// 2. Add Mobile Navigation Drawer markup if not present
if (!html.includes('id="mobile-nav-drawer"')) {
  const mobileNavDrawerHtml = `
    <!-- ========================================================== -->
    <!-- MOBILE NAVIGATION DRAWER (Slide-out menu for mobile/tablet)-->
    <!-- ========================================================== -->
    <div class="mobile-nav-backdrop" id="mobile-nav-backdrop"></div>
    <aside class="mobile-nav-drawer" id="mobile-nav-drawer" aria-label="Mobile Navigation Drawer">
      <div class="mobile-nav-drawer-header">
        <span class="drawer-brand-title">Stellar</span>
        <button type="button" class="mobile-nav-close-btn duo-btn-3d" id="mobile-nav-close-btn" aria-label="Close Navigation">✕</button>
      </div>
      <nav class="mobile-nav-drawer-list">
        <button type="button" class="mobile-drawer-btn active" id="mob-drawer-home">
          <span class="mobile-drawer-icon">🏠</span>
          <span class="mobile-drawer-label">Learn Home</span>
        </button>
        <button type="button" class="mobile-drawer-btn" id="mob-drawer-3k">
          <span class="mobile-drawer-icon">⚡</span>
          <span class="mobile-drawer-label">3k Vocabulary</span>
        </button>
        <button type="button" class="mobile-drawer-btn" id="mob-drawer-sections">
          <span class="mobile-drawer-icon">📚</span>
          <span class="mobile-drawer-label">My Sections</span>
        </button>
        <button type="button" class="mobile-drawer-btn" id="mob-drawer-settings">
          <span class="mobile-drawer-icon">⚙️</span>
          <span class="mobile-drawer-label">Settings & Audio</span>
        </button>
      </nav>
      <div class="mobile-nav-drawer-footer">
        <div style="font-size: 0.8rem; font-weight: 750; color: #f1f5f9;">Mastery Track</div>
        <div style="font-size: 0.74rem; color: #a855f7; font-weight: 700;">3,000 Words · 800–1000 Active</div>
      </div>
    </aside>
  `;
  // Insert before </aside> of app-menu-drawer or right before <main class="app-main-viewport">
  html = html.replace('<main class="app-main-viewport"', mobileNavDrawerHtml + '\n<main class="app-main-viewport"');
  console.log('Added Mobile Navigation Drawer markup');
}

// 3. Inject Master Responsive CSS that rigorously enforces layout across Mobile, Tablet, and Desktop
const masterResponsiveCss = `
    /* ========================================================================= */
    /* MASTER PRODUCTION-GRADE RESPONSIVE & MOBILE DRAWER STYLES                 */
    /* ========================================================================= */
    :root {
      --sidebar-width: 216px !important;
      --brand-violet: #a855f7 !important;
    }

    /* Stellar Brand Title: Radiant Violet */
    .sidebar-brand-title,
    .mobile-brand-title,
    .drawer-brand-title {
      font-family: 'Fredoka', 'Nunito', -apple-system, sans-serif !important;
      font-weight: 700 !important;
      color: #a855f7 !important;
      text-shadow: 0 0 18px rgba(168, 85, 247, 0.42) !important;
      letter-spacing: -0.025em !important;
      line-height: 1 !important;
    }
    .sidebar-brand-title {
      font-size: 2.1rem !important;
    }
    .mobile-brand-title {
      font-size: 1.55rem !important;
    }
    .drawer-brand-title {
      font-size: 1.85rem !important;
    }

    /* ------------------------------------------------------------- */
    /* 1. DESKTOP VIEWPORTS (>= 1024px)                              */
    /* ------------------------------------------------------------- */
    @media (min-width: 1024px) {
      .app-desktop-sidebar {
        display: flex !important;
        width: 216px !important;
        min-width: 216px !important;
        max-width: 216px !important;
        padding: 24px 14px 20px !important;
        position: fixed !important;
        left: 0 !important;
        top: 0 !important;
        bottom: 0 !important;
        z-index: 50 !important;
        box-sizing: border-box !important;
        background: #0b1120 !important;
        border-right: 1.5px solid rgba(255, 255, 255, 0.09) !important;
      }
      .app-main-viewport {
        margin-left: 216px !important;
        width: calc(100% - 216px) !important;
        padding-bottom: 0 !important;
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
      .mobile-nav-backdrop,
      .mobile-nav-drawer {
        display: none !important;
      }
    }

    /* ------------------------------------------------------------- */
    /* 2. TABLET & MOBILE VIEWPORTS (< 1024px)                       */
    /* NEVER DISPLAY DESKTOP HEADER OR DESKTOP SIDEBAR!              */
    /* ------------------------------------------------------------- */
    @media (max-width: 1023px) {
      .app-desktop-sidebar {
        display: none !important; /* Never show desktop sidebar on tablet/mobile! */
      }
      .desktop-top-header {
        display: none !important; /* NEVER stack duplicate desktop header! */
      }
      .mobile-top-bar {
        display: flex !important;
        position: sticky !important;
        top: 0 !important;
        z-index: 45 !important;
        background: rgba(11, 17, 32, 0.92) !important;
        backdrop-filter: blur(14px) !important;
        -webkit-backdrop-filter: blur(14px) !important;
        border-bottom: 1.5px solid rgba(255, 255, 255, 0.08) !important;
      }
      .mobile-bottom-nav {
        display: grid !important;
      }
      .app-main-viewport {
        margin-left: 0 !important;
        width: 100% !important;
        padding-bottom: 78px !important;
      }
    }

    /* ------------------------------------------------------------- */
    /* 3. MOBILE NAVIGATION DRAWER                                   */
    /* ------------------------------------------------------------- */
    .mobile-nav-backdrop {
      position: fixed !important;
      inset: 0 !important;
      background: rgba(3, 7, 18, 0.75) !important;
      backdrop-filter: blur(10px) !important;
      -webkit-backdrop-filter: blur(10px) !important;
      z-index: 9990 !important;
      opacity: 0 !important;
      pointer-events: none !important;
      transition: opacity 0.25s ease !important;
    }
    .mobile-nav-backdrop.open {
      opacity: 1 !important;
      pointer-events: auto !important;
    }

    .mobile-nav-drawer {
      position: fixed !important;
      top: 0 !important;
      left: 0 !important;
      bottom: 0 !important;
      width: 280px !important;
      max-width: 82% !important;
      background: linear-gradient(180deg, #10182b 0%, #090e1a 100%) !important;
      border-right: 1.5px solid rgba(255, 255, 255, 0.12) !important;
      box-shadow: 10px 0 40px rgba(0, 0, 0, 0.8) !important;
      z-index: 9995 !important;
      display: flex !important;
      flex-direction: column !important;
      justify-content: space-between !important;
      padding: 22px 18px !important;
      box-sizing: border-box !important;
      transform: translateX(-100%) !important;
      transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    .mobile-nav-drawer.open {
      transform: translateX(0) !important;
    }

    .mobile-nav-drawer-header {
      display: flex !important;
      align-items: center !important;
      justify-content: space-between !important;
      padding-bottom: 18px !important;
      border-bottom: 1.5px solid rgba(255, 255, 255, 0.08) !important;
      margin-bottom: 16px !important;
    }
    .mobile-nav-close-btn {
      width: 36px !important;
      height: 36px !important;
      border-radius: 10px !important;
      background: rgba(255, 255, 255, 0.08) !important;
      border: 1px solid rgba(255, 255, 255, 0.16) !important;
      color: #cbd5e1 !important;
      font-size: 1.1rem !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      cursor: pointer !important;
    }

    .mobile-nav-drawer-list {
      display: flex !important;
      flex-direction: column !important;
      gap: 10px !important;
      flex: 1 !important;
    }

    .mobile-drawer-btn {
      display: flex !important;
      align-items: center !important;
      gap: 14px !important;
      padding: 12px 16px !important;
      border-radius: 14px !important;
      background: transparent !important;
      border: 2px solid transparent !important;
      color: #ffffff !important;
      font-family: 'Nunito', sans-serif !important;
      font-weight: 800 !important;
      font-size: 0.94rem !important;
      letter-spacing: 0.04em !important;
      text-transform: uppercase !important;
      cursor: pointer !important;
      transition: all 0.18s ease !important;
      text-align: left !important;
      width: 100% !important;
      box-sizing: border-box !important;
    }
    .mobile-drawer-btn:hover,
    .mobile-drawer-btn:active {
      background: rgba(255, 255, 255, 0.08) !important;
      transform: translateX(4px) !important;
    }
    .mobile-drawer-btn.active {
      background: rgba(168, 85, 247, 0.16) !important;
      border-color: #a855f7 !important;
      color: #ffffff !important;
      box-shadow: 0 0 16px rgba(168, 85, 247, 0.28), 0 3px 0 #7e22ce !important;
    }
    .mobile-drawer-icon {
      font-size: 1.35rem !important;
      width: 28px !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
    }

    .mobile-nav-drawer-footer {
      padding-top: 16px !important;
      border-top: 1px solid rgba(255, 255, 255, 0.08) !important;
      display: flex !important;
      flex-direction: column !important;
      gap: 4px !important;
    }

    /* ------------------------------------------------------------- */
    /* 4. SETTINGS MODAL 4-TABS BAR FIX (NO TEXT OVERLAP!)           */
    /* ------------------------------------------------------------- */
    .settings-tabs-bar {
      display: flex !important;
      gap: 8px !important;
      padding: 12px 20px !important;
      background: rgba(0, 0, 0, 0.3) !important;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
    }

    @media (max-width: 640px) {
      .settings-tabs-bar {
        display: grid !important;
        grid-template-columns: 1fr 1fr !important;
        gap: 8px !important;
        padding: 12px 14px !important;
      }
      .settings-tab-btn {
        flex: 1 1 100% !important;
        padding: 10px 8px !important;
        font-size: 0.78rem !important;
        text-align: center !important;
        justify-content: center !important;
        white-space: nowrap !important;
      }
    }

    /* Flashcard Immersion (Clean screen) */
    body.in-flashcard-mode .app-desktop-sidebar,
    body.in-flashcard-mode .desktop-top-header,
    body.in-flashcard-mode .mobile-top-bar,
    body.in-flashcard-mode .mobile-bottom-nav,
    body.in-flashcard-mode .mobile-nav-drawer,
    body.in-flashcard-mode .mobile-nav-backdrop {
      display: none !important;
    }
`;

html = html.replace('</style>', masterResponsiveCss + '\n</style>');
console.log('Injected masterResponsiveCss before </style>');

// 4. Update JavaScript to wire hamburger menu to the Mobile Navigation Drawer!
const mobileNavDrawerScript = `
      // =========================================================================
      // MOBILE NAVIGATION DRAWER (Slide-out menu showing left sidebar items)
      // =========================================================================
      const mobileNavDrawer = document.getElementById("mobile-nav-drawer");
      const mobileNavBackdrop = document.getElementById("mobile-nav-backdrop");
      const mobileNavCloseBtn = document.getElementById("mobile-nav-close-btn");
      const mobileHamburgerBtn = document.getElementById("mobile-hamburger-btn");

      function openMobileNavDrawer() {
        if (mobileNavDrawer) mobileNavDrawer.classList.add("open");
        if (mobileNavBackdrop) mobileNavBackdrop.classList.add("open");
        if (typeof playHapticTick === "function") playHapticTick(480, "sine", 0.04);
      }

      function closeMobileNavDrawer() {
        if (mobileNavDrawer) mobileNavDrawer.classList.remove("open");
        if (mobileNavBackdrop) mobileNavBackdrop.classList.remove("open");
      }

      if (mobileHamburgerBtn) {
        // Remove old listener and attach openMobileNavDrawer
        mobileHamburgerBtn.onclick = (e) => {
          e.preventDefault();
          e.stopPropagation();
          openMobileNavDrawer();
        };
      }

      if (mobileNavCloseBtn) {
        mobileNavCloseBtn.addEventListener("click", closeMobileNavDrawer);
      }
      if (mobileNavBackdrop) {
        mobileNavBackdrop.addEventListener("click", closeMobileNavDrawer);
      }

      // Drawer navigation buttons
      const mobDrawerHome = document.getElementById("mob-drawer-home");
      if (mobDrawerHome) {
        mobDrawerHome.addEventListener("click", () => {
          closeMobileNavDrawer();
          switchToScreen("screen-home");
          syncNavigationState("home");
        });
      }

      const mobDrawer3k = document.getElementById("mob-drawer-3k");
      if (mobDrawer3k) {
        mobDrawer3k.addEventListener("click", () => {
          closeMobileNavDrawer();
          switchToScreen("screen-subsections");
          syncNavigationState("3k");
        });
      }

      const mobDrawerSections = document.getElementById("mob-drawer-sections");
      if (mobDrawerSections) {
        mobDrawerSections.addEventListener("click", () => {
          closeMobileNavDrawer();
          switchToScreen("screen-subsections");
          syncNavigationState("sections");
        });
      }

      const mobDrawerSettings = document.getElementById("mob-drawer-settings");
      if (mobDrawerSettings) {
        mobDrawerSettings.addEventListener("click", () => {
          closeMobileNavDrawer();
          setTimeout(() => {
            if (typeof openMenuDrawer === "function") openMenuDrawer();
          }, 150);
        });
      }

      function syncNavigationState(activeTarget) {
        document.querySelectorAll(".sidebar-nav-btn, .mobile-tab-btn, .mobile-drawer-btn").forEach(btn => btn.classList.remove("active"));
        if (activeTarget === "home") {
          const h1 = document.getElementById("nav-btn-home"); if (h1) h1.classList.add("active");
          const h2 = document.getElementById("mob-tab-home"); if (h2) h2.classList.add("active");
          const h3 = document.getElementById("mob-drawer-home"); if (h3) h3.classList.add("active");
        } else if (activeTarget === "3k") {
          const k1 = document.getElementById("nav-btn-3k"); if (k1) k1.classList.add("active");
          const k2 = document.getElementById("mob-tab-3k"); if (k2) k2.classList.add("active");
          const k3 = document.getElementById("mob-drawer-3k"); if (k3) k3.classList.add("active");
        } else if (activeTarget === "sections") {
          const s1 = document.getElementById("nav-btn-sections"); if (s1) s1.classList.add("active");
          const s2 = document.getElementById("mob-tab-sections"); if (s2) s2.classList.add("active");
          const s3 = document.getElementById("mob-drawer-sections"); if (s3) s3.classList.add("active");
        }
      }
`;

// Insert mobileNavDrawerScript before </script>
const lastScriptEnd = html.lastIndexOf('</script>');
html = html.slice(0, lastScriptEnd) + mobileNavDrawerScript + '\n' + html.slice(lastScriptEnd);
console.log('Appended mobileNavDrawerScript');

fs.writeFileSync(indexPath, html, 'utf8');
console.log('Finished writing index.html! New length:', html.length);
