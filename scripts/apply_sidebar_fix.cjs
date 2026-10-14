const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');
console.log('Read index.html, size:', html.length);

// 1. Check if sidebar has close button already
if (!html.includes('id="sidebar-close-btn"')) {
  // Find <div class="sidebar-brand-lockup" id="sidebar-brand-home" title="Stellar Home">
  const brandStart = html.indexOf('<div class="sidebar-brand-lockup" id="sidebar-brand-home" title="Stellar Home">');
  if (brandStart !== -1) {
    // Find the end of this div
    const brandEnd = html.indexOf('</div>\n          </div>', brandStart);
    // Let's inspect around brandStart
    console.log('Brand lockup found at:', brandStart);
  }
}

// Let's do a safe string replacement for the sidebar header
const oldSidebarBrandSnippet = `          <div class="sidebar-brand-lockup" id="sidebar-brand-home" title="Stellar Home">`;
const newSidebarBrandSnippet = `          <!-- Sidebar Header Row with Brand & Close Button -->
          <div class="sidebar-top-bar" style="display: flex; align-items: center; justify-content: space-between; gap: 8px; margin-bottom: 20px; padding-bottom: 14px; border-bottom: 1px solid rgba(255, 255, 255, 0.08);">
            <div class="sidebar-brand-lockup" id="sidebar-brand-home" title="Stellar Home" style="display: flex; align-items: center; gap: 10px; cursor: pointer; flex: 1; min-width: 0; padding-bottom: 0; border-bottom: none;">`;

if (html.includes(oldSidebarBrandSnippet)) {
  html = html.replace(oldSidebarBrandSnippet, newSidebarBrandSnippet);
  
  // Now find the end of sidebar-brand-lockup:
  // It has:
  //             <div class="sidebar-brand-text">
  //               <span class="sidebar-brand-title">Stellar</span>
  //               <span class="sidebar-brand-sub">Vocabulary Mastery</span>
  //             </div>
  //           </div>
  //           <!-- Tactile Navigation Tabs -->
  const targetEnd = `              <div class="sidebar-brand-text">
                <span class="sidebar-brand-title">Stellar</span>
                <span class="sidebar-brand-sub">Vocabulary Mastery</span>
              </div>
            </div>
          </div>
          <!-- Tactile Navigation Tabs -->`;
  
  // Let's search flexibly:
  const textSubIdx = html.indexOf('Vocabulary Mastery</span>');
  if (textSubIdx !== -1) {
    const afterSub = html.indexOf('</div>', textSubIdx); // end of sidebar-brand-text
    const afterBrand = html.indexOf('</div>', afterSub + 6); // end of sidebar-brand-lockup
    
    const closeBtnHtml = `
            </div>
            <!-- Tactile Close Button (Duolingo 3D styling) -->
            <button type="button" class="sidebar-close-btn duo-btn-3d" id="sidebar-close-btn" aria-label="Close navigation sidebar" title="Close Sidebar">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>`;
    
    // Replace the end of sidebar-brand-lockup with closeBtnHtml
    const originalChunk = html.slice(afterSub, afterBrand + 6);
    html = html.slice(0, afterSub) + closeBtnHtml + html.slice(afterBrand + 6);
    console.log('Successfully added sidebar-close-btn to sidebar markup!');
  }
} else {
  console.log('oldSidebarBrandSnippet not matched, maybe already updated?');
}

// 2. Add sidebar backdrop after </aside> (id="app-desktop-sidebar")
const asideClose = '</aside>';
const sidebarAsideIdx = html.indexOf('id="app-desktop-sidebar"');
if (sidebarAsideIdx !== -1) {
  const asideCloseIdx = html.indexOf(asideClose, sidebarAsideIdx);
  if (asideCloseIdx !== -1 && !html.includes('id="sidebar-backdrop"')) {
    html = html.slice(0, asideCloseIdx + asideClose.length) + 
      '\n      <!-- Sidebar Backdrop for overlay mode -->\n      <div class="sidebar-backdrop" id="sidebar-backdrop" aria-hidden="true"></div>' +
      html.slice(asideCloseIdx + asideClose.length);
    console.log('Successfully added sidebar-backdrop!');
  }
}

// 3. Update desktop-top-header to include the sidebar toggle button on far left
if (!html.includes('id="btn-toggle-sidebar"')) {
  const headerLeftOld = `<div class="desktop-header-left">
            <span class="desktop-page-breadcrumb" id="desktop-breadcrumb-text">`;
  const headerLeftNew = `<div class="desktop-header-left">
            <button type="button" class="sidebar-toggle-btn duo-btn-3d" id="btn-toggle-sidebar" aria-label="Toggle navigation menu" title="Toggle Menu">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
                <line x1="3" y1="6" x2="21" y2="6"/>
                <line x1="3" y1="12" x2="21" y2="12"/>
                <line x1="3" y1="18" x2="21" y2="18"/>
              </svg>
            </button>
            <span class="desktop-page-breadcrumb" id="desktop-breadcrumb-text">`;
  
  if (html.includes(headerLeftOld)) {
    html = html.replace(headerLeftOld, headerLeftNew);
    console.log('Successfully added btn-toggle-sidebar to desktop-header-left!');
  } else {
    // Try regex
    html = html.replace(/<div class="desktop-header-left">\s*<span class="desktop-page-breadcrumb"/, 
      `<div class="desktop-header-left">\n            <button type="button" class="sidebar-toggle-btn duo-btn-3d" id="btn-toggle-sidebar" aria-label="Toggle navigation menu" title="Toggle Menu">\n              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">\n                <line x1="3" y1="6" x2="21" y2="6"/>\n                <line x1="3" y1="12" x2="21" y2="12"/>\n                <line x1="3" y1="18" x2="21" y2="18"/>\n              </svg>\n            </button>\n            <span class="desktop-page-breadcrumb"`);
    console.log('Replaced desktop-header-left with regex!');
  }
}

// 4. INJECT COMPREHENSIVE RESPONSIVE CSS BEFORE </style>
const styleEndIdx = html.indexOf('</style>');
const responsiveCss = `
      /* ========================================================== */
      /* CRITICAL MASTER RESPONSIVE LAYOUT & SIDEBAR CONTROLS       */
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

      /* Sidebar Backdrop */
      .sidebar-backdrop {
        position: fixed !important;
        inset: 0 !important;
        background: rgba(3, 7, 18, 0.75) !important;
        backdrop-filter: blur(8px) !important;
        -webkit-backdrop-filter: blur(8px) !important;
        z-index: 998 !important;
        opacity: 0 !important;
        pointer-events: none !important;
        transition: opacity 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
      }
      .sidebar-backdrop.active {
        opacity: 1 !important;
        pointer-events: auto !important;
      }

      /* Sidebar Duolingo 3D Close Button */
      .sidebar-close-btn {
        width: 38px !important;
        height: 38px !important;
        min-width: 38px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.16) !important;
        border-radius: 12px !important;
        color: #cbd5e1 !important;
        cursor: pointer !important;
        box-shadow: 0 3px 0 rgba(0, 0, 0, 0.45) !important;
        transition: all 0.15s ease !important;
        padding: 0 !important;
      }
      .sidebar-close-btn:hover {
        background: rgba(239, 68, 68, 0.22) !important;
        border-color: rgba(239, 68, 68, 0.45) !important;
        color: #fca5a5 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 0 rgba(0, 0, 0, 0.5) !important;
      }
      .sidebar-close-btn:active {
        transform: translateY(2px) !important;
        box-shadow: 0 1px 0 rgba(0, 0, 0, 0.45) !important;
      }

      /* Top Header Toggle Button */
      .sidebar-toggle-btn {
        width: 40px !important;
        height: 40px !important;
        min-width: 40px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.18) !important;
        border-radius: 12px !important;
        color: #f8fafc !important;
        cursor: pointer !important;
        box-shadow: 0 3px 0 rgba(0, 0, 0, 0.4) !important;
        transition: all 0.15s ease !important;
        padding: 0 !important;
        flex-shrink: 0 !important;
      }
      .sidebar-toggle-btn:hover {
        background: rgba(56, 189, 248, 0.18) !important;
        border-color: rgba(56, 189, 248, 0.4) !important;
        color: #38bdf8 !important;
        transform: translateY(-1px) !important;
      }
      .sidebar-toggle-btn:active {
        transform: translateY(2px) !important;
        box-shadow: 0 1px 0 rgba(0, 0, 0, 0.4) !important;
      }

      /* Desktop Sidebar Base */
      .app-desktop-sidebar {
        width: 270px !important;
        min-width: 270px !important;
        max-width: 270px !important;
        height: 100vh !important;
        background: #0b1120 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
        padding: 20px 18px !important;
        box-sizing: border-box !important;
        position: fixed !important;
        left: 0 !important;
        top: 0 !important;
        bottom: 0 !important;
        z-index: 999 !important;
        overflow-y: auto !important;
        transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.28s ease !important;
      }

      /* Main Viewport Base */
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
        transition: margin-left 0.28s cubic-bezier(0.16, 1, 0.3, 1), width 0.28s cubic-bezier(0.16, 1, 0.3, 1) !important;
      }

      /* WIDE DESKTOP (> 1100px): Docked or Collapsed */
      @media (min-width: 1101px) {
        body:not(.sidebar-closed) .app-desktop-sidebar {
          transform: translateX(0) !important;
          box-shadow: none !important;
        }
        body:not(.sidebar-closed) .app-main-viewport {
          margin-left: 270px !important;
          width: calc(100% - 270px) !important;
        }
        body.sidebar-closed .app-desktop-sidebar {
          transform: translateX(-100%) !important;
        }
        body.sidebar-closed .app-main-viewport {
          margin-left: 0 !important;
          width: 100% !important;
        }
      }

      /* TABLET & MEDIUM & SPLIT PREVIEW (<= 1100px): Off-canvas overlay (CLOSED by default) */
      @media (max-width: 1100px) {
        .app-desktop-sidebar {
          transform: translateX(-100%) !important;
        }
        .app-desktop-sidebar.open {
          transform: translateX(0) !important;
          box-shadow: 16px 0 45px rgba(0, 0, 0, 0.8) !important;
        }
        .app-main-viewport {
          margin-left: 0 !important;
          width: 100% !important;
        }
      }

      /* MOBILE DEVICES (<= 767px) */
      @media (max-width: 767px) {
        .app-main-viewport {
          padding-bottom: 78px !important;
        }
        .mobile-bottom-nav {
          display: grid !important;
        }
      }

      /* FLASHCARD MODE: Absolute full screen immersion */
      body.in-flashcard-mode .app-desktop-sidebar,
      body.in-flashcard-mode .sidebar-backdrop,
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

      /* TOP HEADER: BULLETPROOF RESPONSIVE CORNER ALIGNMENT ON ALL DEVICES */
      .desktop-top-header {
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: space-between !important;
        padding: 14px 24px !important;
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
      @media (max-width: 640px) {
        .desktop-top-header {
          padding: 10px 14px !important;
          gap: 8px !important;
        }
        .desktop-page-breadcrumb {
          font-size: 0.84rem !important;
          max-width: 165px !important;
        }
        .desktop-header-stats .stat-badge-duo {
          padding: 6px 10px !important;
          font-size: 0.78rem !important;
        }
      }
`;

html = html.slice(0, styleEndIdx) + responsiveCss + html.slice(styleEndIdx);
console.log('Injected critical master responsive CSS!');

// 5. INJECT JAVASCRIPT CONTROLLERS AT THE END OF THE SCRIPT
const scriptEndIdx = html.lastIndexOf('</script>');
const sidebarJs = `
      // ==========================================================
      // MASTER SIDEBAR & NAVIGATION CONTROLS (Duolingo Grade)
      // ==========================================================
      window.openSidebar = function() {
        const sidebar = document.getElementById("app-desktop-sidebar");
        const backdrop = document.getElementById("sidebar-backdrop");
        if (window.innerWidth <= 1100) {
          if (sidebar) sidebar.classList.add("open");
          if (backdrop) backdrop.classList.add("active");
        } else {
          document.body.classList.remove("sidebar-closed");
          try { localStorage.setItem("vocab_sidebar_closed", "false"); } catch(e) {}
        }
        if (typeof playHapticTick === "function") playHapticTick(480, "sine", 0.04);
      };

      window.closeSidebar = function() {
        const sidebar = document.getElementById("app-desktop-sidebar");
        const backdrop = document.getElementById("sidebar-backdrop");
        if (sidebar) sidebar.classList.remove("open");
        if (backdrop) backdrop.classList.remove("active");
        if (window.innerWidth > 1100) {
          document.body.classList.add("sidebar-closed");
          try { localStorage.setItem("vocab_sidebar_closed", "true"); } catch(e) {}
        }
      };

      window.toggleSidebar = function() {
        const sidebar = document.getElementById("app-desktop-sidebar");
        if (window.innerWidth <= 1100) {
          if (sidebar && sidebar.classList.contains("open")) {
            closeSidebar();
          } else {
            openSidebar();
          }
        } else {
          if (document.body.classList.contains("sidebar-closed")) {
            openSidebar();
          } else {
            closeSidebar();
          }
        }
      };

      // Wire up sidebar elements once DOM is ready
      (function initSidebarEvents() {
        const closeBtn = document.getElementById("sidebar-close-btn");
        if (closeBtn) closeBtn.addEventListener("click", closeSidebar);

        const backdrop = document.getElementById("sidebar-backdrop");
        if (backdrop) backdrop.addEventListener("click", closeSidebar);

        const toggleBtn = document.getElementById("btn-toggle-sidebar");
        if (toggleBtn) toggleBtn.addEventListener("click", toggleSidebar);

        const mobHamburger = document.getElementById("mobile-hamburger-btn");
        if (mobHamburger) mobHamburger.addEventListener("click", toggleSidebar);

        // Escape key closes sidebar and any open drawer/modals
        document.addEventListener("keydown", (e) => {
          if (e.key === "Escape") {
            closeSidebar();
            if (typeof closeMenuDrawer === "function") closeMenuDrawer();
            const modalAdd = document.getElementById("modal-add-section");
            if (modalAdd) modalAdd.classList.remove("open");
          }
        });

        // Sidebar Navigation Links
        const navHome = document.getElementById("nav-btn-home");
        if (navHome) navHome.addEventListener("click", () => {
          switchScreen("screen-home");
          if (window.innerWidth <= 1100) closeSidebar();
        });

        const nav3k = document.getElementById("nav-btn-3k");
        if (nav3k) nav3k.addEventListener("click", () => {
          switchScreen("screen-subsections");
          if (window.innerWidth <= 1100) closeSidebar();
        });

        const navSections = document.getElementById("nav-btn-sections");
        if (navSections) navSections.addEventListener("click", () => {
          switchScreen("screen-home");
          if (window.innerWidth <= 1100) closeSidebar();
          setTimeout(() => {
            const addBtn = document.getElementById("btn-open-add-section");
            if (addBtn) addBtn.scrollIntoView({ behavior: "smooth", block: "center" });
          }, 120);
        });

        const navSettings = document.getElementById("nav-btn-settings");
        if (navSettings) navSettings.addEventListener("click", () => {
          if (window.innerWidth <= 1100) closeSidebar();
          if (typeof openMenuDrawer === "function") openMenuDrawer();
        });

        const sidebarBrandHome = document.getElementById("sidebar-brand-home");
        if (sidebarBrandHome) sidebarBrandHome.addEventListener("click", () => {
          switchScreen("screen-home");
          if (window.innerWidth <= 1100) closeSidebar();
        });

        // Sidebar Sound Quick Toggle
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

html = html.slice(0, scriptEndIdx) + sidebarJs + html.slice(scriptEndIdx);
console.log('Injected master sidebar JavaScript controllers!');

fs.writeFileSync('index.html', html, 'utf8');
console.log('Updated index.html successfully! New length:', html.length);
