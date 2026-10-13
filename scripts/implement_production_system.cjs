const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');
console.log('Read index.html, total size:', html.length);

// =========================================================================
// 1. BRAND MASCOT SVG (Charming, memorable, Duolingo-grade mascot "Lexi")
// =========================================================================
const brandMascotSvg = `<svg width="40" height="40" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg" class="brand-mascot-svg">
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
</svg>`;

// =========================================================================
// 2. COMPLETE DESKTOP & MOBILE RESPONSIVE CSS
// =========================================================================
const modernLayoutCss = `
      /* ==========================================================
         PRODUCTION-GRADE DUOLINGO-INSPIRED LAYOUT & ARCHITECTURE
         ========================================================== */
      
      :root {
        --sidebar-width: 256px;
        --accent-emerald: #10b981;
        --accent-emerald-dark: #059669;
        --accent-blue: #0284c7;
        --accent-amber: #f59e0b;
        --surface-dark: #070a13;
        --surface-card: #0d1424;
        --surface-border: rgba(255, 255, 255, 0.08);
      }

      /* Global App Reset */
      html, body {
        width: 100%;
        height: 100%;
        margin: 0;
        padding: 0;
        background: #070a13;
        color: #f8fafc;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        overflow-x: hidden;
      }

      /* Outer Application Shell */
      #app-container {
        width: 100% !important;
        max-width: 100% !important;
        min-height: 100vh !important;
        height: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        display: flex !important;
        flex-direction: row !important;
        background: #070a13 !important;
        position: relative !important;
        overflow: hidden !important;
      }

      /* ==========================================================
         DESKTOP PERSISTENT LEFT SIDEBAR (Duolingo-grade)
         ========================================================== */
      .app-desktop-sidebar {
        width: var(--sidebar-width);
        min-width: var(--sidebar-width);
        height: 100vh;
        background: #0b1120;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 24px 18px;
        position: fixed;
        left: 0;
        top: 0;
        bottom: 0;
        z-index: 50;
        overflow-y: auto;
      }

      .sidebar-brand-lockup {
        display: flex;
        align-items: center;
        gap: 12px;
        padding-bottom: 24px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.07);
        text-decoration: none;
        cursor: pointer;
      }

      .sidebar-brand-text {
        display: flex;
        flex-direction: column;
      }

      .sidebar-brand-title {
        font-size: 1.25rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #ffffff;
        line-height: 1.1;
      }

      .sidebar-brand-sub {
        font-size: 0.72rem;
        font-weight: 600;
        color: #10b981;
        letter-spacing: 0.05em;
        text-transform: uppercase;
      }

      /* Nav Items with Chunky Tactile 3D Depth */
      .sidebar-nav-list {
        display: flex;
        flex-direction: column;
        gap: 10px;
        margin-top: 20px;
        flex: 1;
      }

      .sidebar-nav-btn {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 12px 16px;
        border-radius: 16px;
        background: transparent;
        border: 2px solid transparent;
        color: #94a3b8;
        font-size: 0.95rem;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.16s ease;
        text-align: left;
        width: 100%;
      }

      .sidebar-nav-btn:hover {
        background: rgba(255, 255, 255, 0.05);
        color: #ffffff;
      }

      .sidebar-nav-btn.active {
        background: rgba(16, 185, 129, 0.12);
        border-color: rgba(16, 185, 129, 0.35);
        color: #34d399;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.15);
      }

      .sidebar-nav-icon {
        font-size: 1.25rem;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 28px;
        height: 28px;
        flex-shrink: 0;
      }

      /* Sidebar Footer Widget */
      .sidebar-footer-card {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 18px;
        padding: 16px;
        display: flex;
        flex-direction: column;
        gap: 12px;
      }

      .sidebar-streak-badge {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.85rem;
        font-weight: 700;
        color: #f59e0b;
      }

      .sidebar-sound-quick-toggle {
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-size: 0.8rem;
        color: #94a3b8;
        background: rgba(0, 0, 0, 0.25);
        padding: 6px 10px;
        border-radius: 10px;
        cursor: pointer;
      }

      /* ==========================================================
         MAIN CONTENT AREA (Expands beside Sidebar on Desktop)
         ========================================================== */
      .app-main-viewport {
        flex: 1;
        margin-left: var(--sidebar-width);
        min-height: 100vh;
        width: calc(100% - var(--sidebar-width));
        display: flex;
        flex-direction: column;
        position: relative;
        overflow-y: auto;
      }

      /* Desktop Top Stats Bar */
      .desktop-top-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 16px 36px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        background: rgba(11, 17, 32, 0.7);
        backdrop-filter: blur(12px);
        position: sticky;
        top: 0;
        z-index: 40;
      }

      .desktop-header-left {
        display: flex;
        align-items: center;
        gap: 12px;
      }

      .desktop-page-breadcrumb {
        font-size: 0.95rem;
        font-weight: 700;
        color: #cbd5e1;
      }

      .desktop-header-stats {
        display: flex;
        align-items: center;
        gap: 14px;
      }

      .stat-badge-duo {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        padding: 6px 14px;
        border-radius: 14px;
        font-size: 0.82rem;
        font-weight: 700;
        border: 1px solid transparent;
        white-space: nowrap;
        flex-shrink: 0;
      }

      .stat-badge-streak {
        background: rgba(245, 158, 11, 0.12);
        border-color: rgba(245, 158, 11, 0.3);
        color: #fbbf24;
      }

      .stat-badge-mastery {
        background: rgba(16, 185, 129, 0.12);
        border-color: rgba(16, 185, 129, 0.3);
        color: #34d399;
      }

      /* ==========================================================
         MOBILE TOP APP BAR (HAMBURGER STRICTLY FAR LEFT)
         ========================================================== */
      .mobile-top-bar {
        display: none;
        align-items: center;
        justify-content: space-between;
        padding: 12px 16px;
        background: #0b1120;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        position: sticky;
        top: 0;
        z-index: 40;
        width: 100%;
      }

      .mobile-left-cluster {
        display: flex;
        align-items: center;
        gap: 12px;
      }

      /* Mobile Hamburger Menu Button: Pin strictly to top-left! */
      .mobile-hamburger-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 44px;
        height: 44px;
        min-width: 44px;
        min-height: 44px;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #f8fafc;
        cursor: pointer;
        flex-shrink: 0;
        transition: transform 0.15s ease, background 0.15s ease;
      }

      .mobile-hamburger-btn:active {
        transform: scale(0.94);
        background: rgba(16, 185, 129, 0.2);
        color: #34d399;
      }

      .mobile-brand-title {
        font-size: 1.1rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.02em;
      }

      /* Mobile Bottom Navigation Bar */
      .mobile-bottom-nav {
        display: none;
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        height: 64px;
        background: #0b1120;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        z-index: 45;
        grid-template-columns: repeat(4, 1fr);
        align-items: center;
      }

      .mobile-tab-btn {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 3px;
        background: transparent;
        border: none;
        color: #94a3b8;
        font-size: 0.68rem;
        font-weight: 700;
        cursor: pointer;
        height: 100%;
      }

      .mobile-tab-btn.active {
        color: #34d399;
      }

      .mobile-tab-icon {
        font-size: 1.25rem;
      }

      /* ==========================================================
         APP SCREENS ARCHITECTURE (Smooth Switching)
         ========================================================== */
      .app-screen {
        width: 100%;
        max-width: 1080px;
        margin: 0 auto;
        padding: 24px 32px 48px;
        display: none;
        flex-direction: column;
        gap: 28px;
        flex: 1;
      }

      .app-screen.active-screen {
        display: flex;
      }

      /* ==========================================================
         FEATURED 3K VOCABULARY SECTION (Modern 3D Tactile Card)
         ========================================================== */
      .featured-3k-wrapper {
        width: 100%;
        perspective: 1200px;
      }

      .card-3k-featured {
        position: relative;
        border-radius: 28px;
        background: linear-gradient(145deg, #131d33 0%, #0e172a 60%, #090e1c 100%);
        border: 2px solid rgba(56, 189, 248, 0.35);
        box-shadow: 0 16px 40px -10px rgba(0, 0, 0, 0.8),
                    0 6px 0 #075985,
                    0 0 28px rgba(56, 189, 248, 0.15);
        padding: 32px 36px;
        overflow: hidden;
        cursor: pointer;
        transform-style: preserve-3d;
        transition: transform 0.22s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.22s ease, border-color 0.22s ease;
      }

      .card-3k-featured:hover {
        border-color: #38bdf8;
        transform: translateY(-3px);
        box-shadow: 0 22px 50px -10px rgba(0, 0, 0, 0.9),
                    0 8px 0 #0284c7,
                    0 0 36px rgba(56, 189, 248, 0.25);
      }

      .card-3k-featured:active {
        transform: translateY(2px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.7),
                    0 2px 0 #0284c7;
      }

      .card-3k-layout {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 36px;
        position: relative;
        z-index: 2;
      }

      .card-3k-info-col {
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: 14px;
      }

      /* Clean unboxed label: 3k Vocabulary */
      .card-3k-title {
        font-size: 2.35rem;
        font-weight: 900;
        letter-spacing: -0.03em;
        color: #ffffff;
        margin: 0;
        line-height: 1.1;
      }

      .card-3k-desc {
        font-size: 0.98rem;
        line-height: 1.55;
        color: #94a3b8;
        max-width: 580px;
        margin: 0;
      }

      /* Status Progress Box */
      .card-3k-progress-box {
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 14px 18px;
        display: flex;
        flex-direction: column;
        gap: 8px;
        max-width: 540px;
      }

      .progress-meta-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.88rem;
        font-weight: 700;
        color: #cbd5e1;
      }

      .progress-track-3k {
        width: 100%;
        height: 12px;
        border-radius: 9999px;
        background: rgba(255, 255, 255, 0.08);
        overflow: hidden;
        position: relative;
      }

      .progress-fill-3k {
        height: 100%;
        border-radius: 9999px;
        background: linear-gradient(90deg, #0284c7 0%, #10b981 100%);
        transition: width 0.35s ease;
      }

      /* Actions: Resume & Open Subsections */
      .card-3k-actions {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-top: 6px;
        flex-wrap: wrap;
      }

      .btn-launch-3k {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        padding: 13px 28px;
        border-radius: 16px;
        background: #0284c7;
        color: #ffffff;
        font-size: 1rem;
        font-weight: 800;
        border: none;
        cursor: pointer;
        box-shadow: 0 4px 0 #0369a1, 0 8px 20px rgba(2, 132, 199, 0.4);
        transition: all 0.16s ease;
      }

      .btn-launch-3k:hover {
        background: #0ea5e9;
        transform: translateY(-2px);
        box-shadow: 0 6px 0 #0369a1, 0 12px 24px rgba(2, 132, 199, 0.5);
      }

      .btn-launch-3k:active {
        transform: translateY(2px);
        box-shadow: 0 1px 0 #0369a1;
      }

      .btn-subsections-3k {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 13px 22px;
        border-radius: 16px;
        background: rgba(255, 255, 255, 0.07);
        border: 2px solid rgba(255, 255, 255, 0.14);
        color: #f1f5f9;
        font-size: 0.92rem;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.18s ease;
      }

      .btn-subsections-3k:hover {
        background: rgba(255, 255, 255, 0.14);
        border-color: rgba(255, 255, 255, 0.28);
      }

      /* ==========================================================
         SECTIONS & CUSTOM DECKS GRID
         ========================================================== */
      .sections-container-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-top: 8px;
      }

      .sections-main-heading {
        font-size: 1.4rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.02em;
        margin: 0;
      }

      .btn-create-section-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 10px 18px;
        border-radius: 14px;
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.35);
        color: #34d399;
        font-size: 0.88rem;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.18s ease;
      }

      .btn-create-section-pill:hover {
        background: #10b981;
        color: #064e3b;
        transform: translateY(-1px);
      }

      .sections-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
        gap: 16px;
      }

      .custom-section-card {
        background: #0f172a;
        border: 1.5px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 20px;
        display: flex;
        flex-direction: column;
        gap: 14px;
        cursor: pointer;
        transition: transform 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease;
        position: relative;
      }

      .custom-section-card:hover {
        border-color: rgba(56, 189, 248, 0.4);
        transform: translateY(-2px);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.5);
      }

      .section-card-top-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
      }

      .section-icon-badge {
        width: 44px;
        height: 44px;
        min-width: 44px;
        min-height: 44px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.3rem;
        flex-shrink: 0;
      }

      .section-title-text {
        font-size: 1.1rem;
        font-weight: 800;
        color: #ffffff;
      }

      .section-subtitle-text {
        font-size: 0.82rem;
        color: #94a3b8;
        line-height: 1.4;
      }

      .reorder-btns-group {
        display: flex;
        align-items: center;
        gap: 4px;
      }

      .btn-reorder-arrow {
        width: 28px;
        height: 28px;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #cbd5e1;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.72rem;
      }

      .btn-reorder-arrow:hover {
        background: rgba(56, 189, 248, 0.2);
        color: #38bdf8;
      }

      /* ==========================================================
         SUBSECTIONS SCREEN (Tiers 800 - 1000 & all)
         ========================================================== */
      .subsections-top-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-bottom: 8px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      }

      .breadcrumb-back-btn {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 16px;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.12);
        color: #e2e8f0;
        font-size: 0.88rem;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.16s ease;
      }

      .breadcrumb-back-btn:hover {
        background: rgba(255, 255, 255, 0.12);
        color: #ffffff;
      }

      .tier-active-pill {
        background: #0284c7 !important;
        border-color: #38bdf8 !important;
        color: #ffffff !important;
        box-shadow: 0 0 24px rgba(2, 132, 199, 0.35) !important;
      }

      /* ==========================================================
         FLASHCARD SCREEN & STRICT DOUBLE TAP
         ========================================================== */
      .flashcard-top-nav {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 8px 0 16px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      }

      .btn-card-face-learned {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 14px;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.06);
        border: 1.5px solid rgba(255, 255, 255, 0.15);
        color: #cbd5e1;
        font-size: 0.82rem;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.18s ease;
      }

      .btn-card-face-learned.is-learned {
        background: rgba(16, 185, 129, 0.18);
        border-color: #10b981;
        color: #34d399;
        box-shadow: 0 0 14px rgba(16, 185, 129, 0.25);
      }

      .btn-card-face-learned.is-learned .learned-face-check {
        background: #10b981;
        color: #064e3b;
      }

      .learned-face-check {
        width: 18px;
        height: 18px;
        border-radius: 5px;
        background: rgba(255, 255, 255, 0.1);
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 0.72rem;
        font-weight: 900;
      }

      /* Flashcard Stage Sizing */
      .card-stage {
        max-width: 660px;
        width: 100%;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        align-items: center;
      }

      .bottom-nav-bar {
        max-width: 660px;
        width: 100%;
        margin: 16px auto 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
      }

      /* Clean Red / Status / Indicator Geometry Fixes: NEVER COMPRESSED! */
      .round-indicator,
      .status-dot-pulse,
      .badge-dot,
      .vector-icon,
      .brand-mascot-svg {
        flex-shrink: 0 !important;
        aspect-ratio: 1 / 1 !important;
        overflow: visible !important;
      }

      /* ==========================================================
         RESPONSIVE BREAKPOINTS (Desktop vs Mobile)
         ========================================================== */
      @media (min-width: 768px) {
        .app-desktop-sidebar {
          display: flex !important;
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

        .mobile-hamburger-btn {
          display: none !important;
        }
      }

      @media (max-width: 767px) {
        .app-desktop-sidebar {
          display: none !important;
        }

        .app-main-viewport {
          margin-left: 0 !important;
          width: 100% !important;
          padding-bottom: 74px !important;
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

        .app-screen {
          padding: 16px 16px 32px !important;
          gap: 20px !important;
        }

        .card-3k-featured {
          padding: 22px 20px !important;
        }

        .card-3k-layout {
          flex-direction: column !important;
          gap: 20px !important;
        }

        .card-3k-visual-col {
          display: none !important;
        }

        .card-3k-title {
          font-size: 1.75rem !important;
        }
      }
`;

// Replace style block cleanly in HTML
const styleRegex = /<style>[\s\S]*?<\/style>/;
if (styleRegex.test(html)) {
  // We keep font imports & core keyframes, appending our production CSS
  html = html.replace(/<\/style>/, modernLayoutCss + '\n</style>');
  console.log('Appended modern production-grade CSS rules!');
}

// =========================================================================
// 3. BUILD THE DUOLINGO-GRADE APPLICATION SHELL (Sidebar + Main Viewport)
// =========================================================================

// Let's create the desktop sidebar markup
const desktopSidebarHtml = `
      <!-- ========================================================== -->
      <!-- DESKTOP PERSISTENT LEFT SIDEBAR (Duolingo Grade)           -->
      <!-- ========================================================== -->
      <aside class="app-desktop-sidebar" id="app-desktop-sidebar" aria-label="Main Navigation">
        <div>
          <!-- Brand Wordmark with Lexi Mascot -->
          <div class="sidebar-brand-lockup" id="sidebar-brand-home" title="VOCAB 3K Home">
            ${brandMascotSvg}
            <div class="sidebar-brand-text">
              <span class="sidebar-brand-title">VOCAB 3K</span>
              <span class="sidebar-brand-sub">Mastery Studio</span>
            </div>
          </div>

          <!-- Tactile Navigation Tabs -->
          <nav class="sidebar-nav-list">
            <button type="button" class="sidebar-nav-btn active" id="nav-btn-home">
              <span class="sidebar-nav-icon">🏠</span>
              <span>Learn Home</span>
            </button>
            <button type="button" class="sidebar-nav-btn" id="nav-btn-3k">
              <span class="sidebar-nav-icon">⚡</span>
              <span>3k Vocabulary</span>
            </button>
            <button type="button" class="sidebar-nav-btn" id="nav-btn-subsections">
              <span class="sidebar-nav-icon">📑</span>
              <span>Tiers (800–1000)</span>
            </button>
            <button type="button" class="sidebar-nav-btn" id="nav-btn-sections">
              <span class="sidebar-nav-icon">📚</span>
              <span>My Sections</span>
            </button>
            <button type="button" class="sidebar-nav-btn" id="nav-btn-settings">
              <span class="sidebar-nav-icon">⚙️</span>
              <span>Settings</span>
            </button>
          </nav>
        </div>

        <!-- Sidebar Footer Status & Quick Sound -->
        <div class="sidebar-footer-card">
          <div class="sidebar-streak-badge">
            <span>🔥</span>
            <span>7-Day Streak Active!</span>
          </div>
          <div class="sidebar-sound-quick-toggle" id="sidebar-quick-sound" title="Toggle audio sound FX">
            <span>Sound FX</span>
            <span id="sidebar-sound-indicator" style="color: #34d399; font-weight: 700;">ON 🔊</span>
          </div>
        </div>
      </aside>
`;

// Let's create the desktop top stats header
const desktopTopHeaderHtml = `
        <!-- Desktop Sticky Top Stats Bar -->
        <header class="desktop-top-header">
          <div class="desktop-header-left">
            <span class="desktop-page-breadcrumb" id="desktop-breadcrumb-text">Dashboard · Choose Your Learning Path</span>
          </div>

          <div class="desktop-header-stats">
            <!-- Streak Flame -->
            <div class="stat-badge-duo stat-badge-streak" title="Current Daily Streak">
              <span>🔥</span>
              <span>7 Days</span>
            </div>

            <!-- Global Status 1 to 3K Learned -->
            <div class="stat-badge-duo stat-badge-mastery" id="desktop-3k-status-badge" title="Status across 3,000 words">
              <span>⚡</span>
              <span>Status: <strong id="desktop-status-count">0</strong> / 3,000</span>
            </div>

            <!-- Settings Button -->
            <button class="breadcrumb-back-btn" id="btn-desktop-open-settings" style="padding: 6px 14px;" title="Settings">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="3"></circle>
                <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
              </svg>
              <span>Settings</span>
            </button>
          </div>
        </header>
`;

// Let's create the mobile top app bar (with hamburger pinned on FAR LEFT)
const mobileTopBarHtml = `
        <!-- Mobile Top App Bar (Hamburger STRICTLY on FAR LEFT) -->
        <header class="mobile-top-bar">
          <div class="mobile-left-cluster">
            <!-- Mobile Hamburger Button Pinned to LEFT CORNER -->
            <button class="mobile-hamburger-btn" id="mobile-hamburger-btn" aria-label="Open Navigation Menu" title="Menu">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
                <line x1="3" y1="6" x2="21" y2="6"/>
                <line x1="3" y1="12" x2="21" y2="12"/>
                <line x1="3" y1="18" x2="21" y2="18"/>
              </svg>
            </button>
            <div style="display: flex; align-items: center; gap: 8px;">
              ${brandMascotSvg.replace('width="40" height="40"', 'width="30" height="30"')}
              <span class="mobile-brand-title">VOCAB 3K</span>
            </div>
          </div>

          <div style="display: flex; align-items: center; gap: 8px;">
            <div class="stat-badge-duo stat-badge-streak" style="padding: 4px 10px; font-size: 0.75rem;">
              <span>🔥 7d</span>
            </div>
            <div class="stat-badge-duo stat-badge-mastery" id="mobile-3k-status-badge" style="padding: 4px 10px; font-size: 0.75rem;">
              <span>⚡ <strong id="mobile-status-count">0</strong>/3k</span>
            </div>
          </div>
        </header>
`;

// Mobile bottom navigation bar
const mobileBottomNavHtml = `
        <!-- Mobile Bottom Nav Bar (Thumb Zone) -->
        <nav class="mobile-bottom-nav">
          <button type="button" class="mobile-tab-btn active" id="mob-tab-home">
            <span class="mobile-tab-icon">🏠</span>
            <span>Home</span>
          </button>
          <button type="button" class="mobile-tab-btn" id="mob-tab-3k">
            <span class="mobile-tab-icon">⚡</span>
            <span>3k Vocab</span>
          </button>
          <button type="button" class="mobile-tab-btn" id="mob-tab-sections">
            <span class="mobile-tab-icon">📚</span>
            <span>Decks</span>
          </button>
          <button type="button" class="mobile-tab-btn" id="mob-tab-settings">
            <span class="mobile-tab-icon">⚙️</span>
            <span>Settings</span>
          </button>
        </nav>
`;

// =========================================================================
// 4. SCREEN 1: MODERN HOME SCREEN MARKUP
// =========================================================================
const modernScreenHomeHtml = `
        <!-- ========================================== -->
        <!-- SCREEN 1: MODERN RESPONSIVE HOME SCREEN     -->
        <!-- ========================================== -->
        <div class="app-screen active-screen" id="screen-home">

          <!-- ==================================================== -->
          <!-- FEATURED 3K VOCABULARY SECTION (Interactive 3D Card) -->
          <!-- ==================================================== -->
          <div class="featured-3k-wrapper" id="featured-3k-wrapper">
            <div class="card-3k-featured" id="card-3k-featured" role="button" tabindex="0" aria-label="3k Vocabulary - Tap to open subsections">
              <!-- Dynamic Specular Reflection Light Sheen -->
              <div class="card-3d-shine" id="card-3k-shine"></div>

              <div class="card-3k-layout">
                <!-- Left Info Column -->
                <div class="card-3k-info-col">
                  <!-- SIMPLY LABELED '3k Vocabulary' -->
                  <h2 class="card-3k-title" id="label-3k-vocabulary">3k Vocabulary</h2>
                  
                  <p class="card-3k-desc">
                    Comprehensive 3,000-word trilingual spectrum. Master everyday English, authentic native Tamil script, Spanish, and Hindi with verified HD imagery and audio pronunciation.
                  </p>

                  <!-- Real-time Status 1 to 3K Metric -->
                  <div class="card-3k-progress-box">
                    <div class="progress-meta-row">
                      <span>Overall Mastery: <strong id="card-3k-learned-count">0</strong> / 3,000 Learned</span>
                      <span id="card-3k-learned-pct" style="color: #38bdf8; font-weight: 800;">0%</span>
                    </div>
                    <div class="progress-track-3k">
                      <div class="progress-fill-3k" id="progress-fill-3k-total" style="width: 0%;"></div>
                    </div>
                    <div class="progress-tier-hint" style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #94a3b8; margin-top: 4px;">
                      <span>Active Focus: <strong>Cards 800 – 1000</strong></span>
                      <span id="tier-800-learned-stat">0 / 200 in active tier</span>
                    </div>
                  </div>

                  <!-- Quick Action Controls -->
                  <div class="card-3k-actions">
                    <!-- RESUME BUTTON: Bypasses subsections, opens directly at exact card index! -->
                    <button type="button" class="btn-launch-3k" id="btn-resume-3k-deck" title="Directly resume where you left off">
                      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">
                        <polygon points="5 3 19 12 5 21 5 3"></polygon>
                      </svg>
                      <span id="btn-resume-label">Resume (#800)</span>
                    </button>

                    <!-- OPEN SUBSECTIONS BUTTON: Explores 800-1000 and all tiers -->
                    <button type="button" class="btn-subsections-3k" id="btn-open-subsections" title="View all 3,000 vocabulary subsections">
                      <span>Explore Subsections (800 – 1000)</span>
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="9 18 15 12 9 6"/>
                      </svg>
                    </button>
                  </div>
                </div>

                <!-- Right 3D Layered Mini-Cards Stack -->
                <div class="card-3k-visual-col" aria-hidden="true">
                  <div class="floating-card-stack" id="floating-card-stack">
                    <div class="mini-deck-card mini-card-3">
                      <div class="mini-card-header">
                        <span>#802</span>
                        <span>SINK</span>
                      </div>
                      <div class="mini-card-word">SINK</div>
                      <div class="mini-card-trans">fregadero · தொட்டி</div>
                    </div>
                    <div class="mini-deck-card mini-card-2">
                      <div class="mini-card-header">
                        <span>#801</span>
                        <span>OVEN</span>
                      </div>
                      <div class="mini-card-word">OVEN</div>
                      <div class="mini-card-trans">horno · அடுமனை</div>
                    </div>
                    <div class="mini-deck-card mini-card-1">
                      <div class="mini-card-header">
                        <span>#800</span>
                        <span>STOVE</span>
                      </div>
                      <div class="mini-card-word">STOVE</div>
                      <div class="mini-card-trans">estufa · அடுப்பு</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- ==================================================== -->
          <!-- DYNAMIC CUSTOM SECTIONS (Add, Edit, Drag and Move)   -->
          <!-- ==================================================== -->
          <div class="sections-container-header">
            <div class="sections-heading-group">
              <h3 class="sections-main-heading">My Learning Sections</h3>
              <span style="font-size: 0.85rem; color: #94a3b8;" id="sections-count-pill">4 Decks</span>
            </div>
            <button type="button" class="btn-create-section-pill" id="btn-open-add-section">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
                <line x1="12" y1="5" x2="12" y2="19"/>
                <line x1="5" y1="12" x2="19" y2="12"/>
              </svg>
              <span>+ Add Section</span>
            </button>
          </div>

          <!-- Draggable & Movable Sections Grid -->
          <div class="sections-grid" id="sections-grid">
            <!-- Dynamically populated from localStorage -->
          </div>
        </div>
`;

// =========================================================================
// 5. SCREEN 2: SUBSECTIONS (800 - 1000 & all tiers)
// =========================================================================
const modernScreenSubsectionsHtml = `
        <!-- ========================================== -->
        <!-- SCREEN 2: DECK SUB-SECTIONS VIEW            -->
        <!-- ========================================== -->
        <div class="app-screen" id="screen-subsections">
          <div class="subsections-top-bar">
            <button class="breadcrumb-back-btn" id="btn-back-to-home" title="Back to Home">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="15 18 9 12 15 6"/>
              </svg>
              <span>Back to Home</span>
            </button>

            <span style="font-size: 1.1rem; font-weight: 800; color: #ffffff;">3k Vocabulary Subsections</span>

            <div class="stat-badge-duo stat-badge-mastery">
              <span>Status: <strong id="subsections-3k-total">0</strong> / 3,000</span>
            </div>
          </div>

          <!-- Active Tier 800 - 1000 Featured Banner -->
          <div style="background: linear-gradient(135deg, rgba(2, 132, 199, 0.18), rgba(16, 185, 129, 0.1)); border: 1.5px solid rgba(56, 189, 248, 0.35); border-radius: 20px; padding: 22px 26px; display: flex; align-items: center; justify-content: space-between; gap: 16px; flex-wrap: wrap;">
            <div>
              <div style="font-size: 0.72rem; font-weight: 800; letter-spacing: 0.08em; color: #38bdf8; text-transform: uppercase;">Active Recommended Tier</div>
              <h3 style="font-size: 1.35rem; font-weight: 800; color: #ffffff; margin: 4px 0;">Cards 800 – 1000 (Kitchen & Daily Life)</h3>
              <p style="font-size: 0.88rem; color: #cbd5e1; margin: 0;">200 high-frequency words with full trilingual flashcards, audio pronunciation, and HD photos.</p>
            </div>
            <button type="button" class="btn-launch-3k" id="btn-resume-from-subsections" style="padding: 10px 22px; font-size: 0.92rem;">
              <span>Study Deck Now</span>
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
            </button>
          </div>

          <!-- All Tiers Grid -->
          <div class="sections-grid">
            <!-- ACTIVE TIER: 800 - 1000 -->
            <div class="custom-section-card tier-active-pill" id="sub-tier-800-1000" role="button" tabindex="0">
              <div class="section-card-top-bar">
                <div style="display: flex; align-items: center; gap: 12px;">
                  <span class="section-icon-badge" style="background: rgba(255, 255, 255, 0.2); font-size: 1.4rem;">🔥</span>
                  <div>
                    <div class="section-title-text" style="color: #ffffff;">Cards 800 – 1000 (Active)</div>
                    <div class="section-subtitle-text" style="color: rgba(255, 255, 255, 0.8);">Kitchen, Dining, Appliances & Daily Life</div>
                  </div>
                </div>
                <span style="font-size: 0.75rem; font-weight: 800; background: #ffffff; color: #0284c7; padding: 4px 10px; border-radius: 10px;">STUDY NOW</span>
              </div>
              <div style="font-size: 0.8rem; color: rgba(255, 255, 255, 0.9); margin-top: 6px;">
                200 Words · STOVE, OVEN, SINK, REFRIGERATOR, KETTLE...
              </div>
            </div>

            <!-- Tier 1 - 200 -->
            <div class="custom-section-card" id="sub-tier-1-200" role="button" tabindex="0">
              <div class="section-card-top-bar">
                <div style="display: flex; align-items: center; gap: 12px;">
                  <span class="section-icon-badge" style="background: rgba(56, 189, 248, 0.15);">🌱</span>
                  <div>
                    <div class="section-title-text">Cards 1 – 200</div>
                    <div class="section-subtitle-text">Beginner Fundamentals & Core Nouns</div>
                  </div>
                </div>
                <span style="font-size: 0.75rem; color: #94a3b8;">200 Words</span>
              </div>
            </div>

            <!-- Tier 200 - 400 -->
            <div class="custom-section-card" id="sub-tier-200-400" role="button" tabindex="0">
              <div class="section-card-top-bar">
                <div style="display: flex; align-items: center; gap: 12px;">
                  <span class="section-icon-badge" style="background: rgba(16, 185, 129, 0.15);">🏡</span>
                  <div>
                    <div class="section-title-text">Cards 200 – 400</div>
                    <div class="section-subtitle-text">Home, Rooms & Living Objects</div>
                  </div>
                </div>
                <span style="font-size: 0.75rem; color: #94a3b8;">200 Words</span>
              </div>
            </div>

            <!-- Tier 400 - 600 -->
            <div class="custom-section-card" id="sub-tier-400-600" role="button" tabindex="0">
              <div class="section-card-top-bar">
                <div style="display: flex; align-items: center; gap: 12px;">
                  <span class="section-icon-badge" style="background: rgba(245, 158, 11, 0.15);">🚗</span>
                  <div>
                    <div class="section-title-text">Cards 400 – 600</div>
                    <div class="section-subtitle-text">Transport, Vehicles & Commute</div>
                  </div>
                </div>
                <span style="font-size: 0.75rem; color: #94a3b8;">200 Words</span>
              </div>
            </div>

            <!-- Tier 600 - 800 -->
            <div class="custom-section-card" id="sub-tier-600-800" role="button" tabindex="0">
              <div class="section-card-top-bar">
                <div style="display: flex; align-items: center; gap: 12px;">
                  <span class="section-icon-badge" style="background: rgba(168, 85, 247, 0.15);">🍎</span>
                  <div>
                    <div class="section-title-text">Cards 600 – 800</div>
                    <div class="section-subtitle-text">Groceries, Food & Markets</div>
                  </div>
                </div>
                <span style="font-size: 0.75rem; color: #94a3b8;">200 Words</span>
              </div>
            </div>

            <!-- Tier 1000 - 1200 -->
            <div class="custom-section-card" id="sub-tier-1000-1200" role="button" tabindex="0">
              <div class="section-card-top-bar">
                <div style="display: flex; align-items: center; gap: 12px;">
                  <span class="section-icon-badge" style="background: rgba(236, 72, 153, 0.15);">💼</span>
                  <div>
                    <div class="section-title-text">Cards 1000 – 1200</div>
                    <div class="section-subtitle-text">Workplace, Tech & Career</div>
                  </div>
                </div>
                <span style="font-size: 0.75rem; color: #94a3b8;">200 Words</span>
              </div>
            </div>
          </div>
        </div>
`;

// Replace screens 1 and 2 in html
const screenHomePattern = /<!-- ========================================== -->\s*<!-- SCREEN 1: MODERN RESPONSIVE HOME SCREEN[\s\S]*?<!-- ========================================== -->\s*<!-- SCREEN 3: MODERN FLASHCARD VIEW/;

const combinedScreensHtml = `${modernScreenHomeHtml}
${modernScreenSubsectionsHtml}
        <!-- ========================================== -->
        <!-- SCREEN 3: MODERN FLASHCARD VIEW`;

if (screenHomePattern.test(html)) {
  html = html.replace(screenHomePattern, combinedScreensHtml);
  console.log('Successfully updated Screen 1 and Screen 2 markup!');
} else {
  console.warn('Could not match screenHomePattern');
}

// Wrap app-container with app-desktop-sidebar and app-main-viewport
// Check if app-desktop-sidebar already exists
if (!html.includes('id="app-desktop-sidebar"')) {
  // Replace <div id="app-container"> with the full shell
  html = html.replace(
    /<div id="app-container">/,
    `<div id="app-container">\n${desktopSidebarHtml}\n<div class="app-main-viewport">\n${desktopTopHeaderHtml}\n${mobileTopBarHtml}\n${mobileBottomNavHtml}`
  );
  
  // Close app-main-viewport before closing app-container
  html = html.replace(
    /<\/div>\s*<!-- ==========================================================\s*-->\s*<!-- SLIDE-OVER NAVIGATION/,
    `</div>\n</div>\n<!-- ==========================================================\n-->\n<!-- SLIDE-OVER NAVIGATION`
  );
  console.log('Successfully wrapped application in desktop sidebar and main viewport!');
}

fs.writeFileSync('index.html', html, 'utf8');
console.log('Saved index.html successfully!');
