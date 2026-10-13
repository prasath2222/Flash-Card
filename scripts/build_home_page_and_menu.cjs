const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

console.log('Original length:', html.length);

// 1. CSS STYLES FOR RESPONSIVE MULTI-DEVICE HOME PAGE, 3D CARD, DRAG & DROP, AND SLIDE-OVER MENU
const modernHomeAndMenuCss = `
      /* ==========================================================
         Multi-Device Responsive Architecture (Mobile, Tablet, Desktop)
         ========================================================== */
      :root {
        --home-max-width: 1080px;
        --deck-max-width: 520px;
      }

      #app-container {
        position: relative;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        width: 100%;
        max-width: var(--deck-max-width);
        height: 100%;
        height: 100dvh;
        margin: 0 auto;
        padding: env(safe-area-inset-top, 16px) 16px env(safe-area-inset-bottom, 16px) 16px;
        z-index: 1;
        transition: max-width 0.35s cubic-bezier(0.16, 1, 0.3, 1);
      }

      /* Home Screen Active: Expands for Tablet & Desktop Screens */
      body.home-view-active #app-container {
        max-width: var(--home-max-width);
        padding: env(safe-area-inset-top, 18px) 24px env(safe-area-inset-bottom, 20px) 24px;
      }

      @media (min-width: 768px) {
        body:not(.home-view-active) #app-container {
          max-width: 600px;
          padding: 24px 20px;
        }
        body.home-view-active #app-container {
          padding: 28px 32px;
        }
      }

      /* Multi-Screen Display */
      .app-screen {
        display: none;
        flex-direction: column;
        width: 100%;
        height: 100%;
        flex: 1;
        overflow: hidden;
      }

      .app-screen.active-screen {
        display: flex;
      }

      /* ==========================================================
         Home Page Header & Top Bar
         ========================================================== */
      .home-app-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 4px 0 16px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.07);
        flex-shrink: 0;
      }

      .brand-group {
        display: flex;
        align-items: center;
        gap: 12px;
      }

      .brand-icon-box {
        width: 40px;
        height: 40px;
        border-radius: 12px;
        background: linear-gradient(135deg, #2563eb, #10b981);
        display: flex;
        align-items: center;
        justify-content: center;
        color: #ffffff;
        font-size: 1.25rem;
        box-shadow: 0 4px 16px rgba(37, 99, 235, 0.35);
      }

      .brand-text-col {
        display: flex;
        flex-direction: column;
      }

      .brand-title {
        font-size: 1.12rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #ffffff;
        line-height: 1.2;
      }

      .brand-subtitle {
        font-size: 0.72rem;
        color: #94a3b8;
        font-weight: 500;
      }

      .home-top-actions {
        display: flex;
        align-items: center;
        gap: 10px;
      }

      .btn-menu-drawer-toggle {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 14px;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.09);
        color: #cbd5e1;
        font-size: 0.82rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.18s ease;
      }

      .btn-menu-drawer-toggle:hover,
      .btn-menu-drawer-toggle:active {
        background: rgba(255, 255, 255, 0.1);
        color: #ffffff;
        border-color: rgba(255, 255, 255, 0.2);
      }

      .home-scroll-canvas {
        flex: 1;
        overflow-y: auto;
        padding: 18px 0 24px;
        display: flex;
        flex-direction: column;
        gap: 24px;
        scrollbar-width: thin;
        scrollbar-color: rgba(255, 255, 255, 0.15) transparent;
      }

      /* ==========================================================
         FEATURED 3K VOCABULARY SECTION (Interactive 3D Card)
         ========================================================== */
      .featured-3k-wrapper {
        position: relative;
        perspective: 1200px;
        width: 100%;
      }

      .card-3k-featured {
        position: relative;
        border-radius: 26px;
        background: linear-gradient(145deg, #131b2e 0%, #0d1322 65%, #080c16 100%);
        border: 1px solid rgba(56, 189, 248, 0.28);
        box-shadow: 0 24px 60px -15px rgba(0, 0, 0, 0.85),
                    0 0 0 1px rgba(255, 255, 255, 0.06),
                    inset 0 1px 0 rgba(255, 255, 255, 0.15);
        padding: 26px 24px;
        overflow: hidden;
        cursor: pointer;
        transform-style: preserve-3d;
        transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.25s ease, border-color 0.25s ease;
      }

      .card-3k-featured:hover {
        border-color: rgba(56, 189, 248, 0.55);
        box-shadow: 0 30px 70px -12px rgba(37, 99, 235, 0.3),
                    0 0 24px rgba(56, 189, 248, 0.2);
      }

      /* Dynamic Specular Reflection Sheen */
      .card-3d-shine {
        position: absolute;
        inset: 0;
        pointer-events: none;
        background: radial-gradient(circle at 50% 30%, rgba(255, 255, 255, 0.12), transparent 70%);
        opacity: 0.6;
        transition: opacity 0.3s ease;
        z-index: 1;
      }

      .card-3k-layout {
        position: relative;
        z-index: 2;
        display: grid;
        grid-template-columns: 1fr;
        gap: 20px;
      }

      @media (min-width: 860px) {
        .card-3k-layout {
          grid-template-columns: 1.25fr 1fr;
          align-items: center;
          gap: 32px;
        }
      }

      .card-3k-info-col {
        display: flex;
        flex-direction: column;
        gap: 14px;
      }

      .card-3k-badge-row {
        display: flex;
        align-items: center;
        gap: 8px;
        flex-wrap: wrap;
      }

      .badge-live-pulse {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 10px;
        border-radius: 9999px;
        background: rgba(16, 185, 129, 0.16);
        border: 1px solid rgba(16, 185, 129, 0.35);
        color: #34d399;
        font-size: 0.68rem;
        font-weight: 750;
        letter-spacing: 0.06em;
        text-transform: uppercase;
      }

      .pulse-indicator-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #10b981;
        box-shadow: 0 0 8px #10b981;
        animation: livePulse 2s infinite;
      }

      @keyframes livePulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.4; transform: scale(0.8); }
      }

      .badge-trilingual {
        font-size: 0.7rem;
        font-weight: 650;
        color: #7dd3fc;
        background: rgba(56, 189, 248, 0.1);
        border: 1px solid rgba(56, 189, 248, 0.25);
        padding: 3px 9px;
        border-radius: 9999px;
        letter-spacing: 0.04em;
        text-transform: uppercase;
      }

      .card-3k-title {
        font-size: clamp(1.8rem, 5vw, 2.35rem);
        font-weight: 850;
        letter-spacing: -0.025em;
        line-height: 1.1;
        color: #ffffff;
        margin: 0;
      }

      .card-3k-desc {
        font-size: 0.88rem;
        line-height: 1.45;
        color: #94a3b8;
      }

      .card-3k-progress-box {
        display: flex;
        flex-direction: column;
        gap: 6px;
        background: rgba(0, 0, 0, 0.25);
        padding: 12px 14px;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.06);
      }

      .progress-meta-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-size: 0.78rem;
        font-weight: 600;
        color: #cbd5e1;
      }

      .progress-meta-row strong {
        color: #38bdf8;
      }

      .progress-track-3k {
        width: 100%;
        height: 6px;
        border-radius: 9999px;
        background: rgba(255, 255, 255, 0.09);
        overflow: hidden;
      }

      .progress-fill-3k {
        width: 80%;
        height: 100%;
        border-radius: 9999px;
        background: linear-gradient(90deg, #2563eb, #38bdf8 60%, #10b981);
        box-shadow: 0 0 12px rgba(56, 189, 248, 0.5);
      }

      .card-3k-actions {
        display: flex;
        align-items: center;
        gap: 12px;
        flex-wrap: wrap;
        padding-top: 4px;
      }

      .btn-launch-3k {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        padding: 12px 24px;
        border-radius: 14px;
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        border: 1px solid rgba(255, 255, 255, 0.18);
        color: #ffffff;
        font-size: 0.9rem;
        font-weight: 750;
        cursor: pointer;
        box-shadow: 0 8px 24px -4px rgba(37, 99, 235, 0.6);
        transition: all 0.2s ease;
      }

      .btn-launch-3k:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 28px -4px rgba(37, 99, 235, 0.75);
      }

      .btn-subsections-3k {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 12px 18px;
        border-radius: 14px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #cbd5e1;
        font-size: 0.85rem;
        font-weight: 650;
        cursor: pointer;
        transition: all 0.18s ease;
      }

      .btn-subsections-3k:hover {
        background: rgba(255, 255, 255, 0.1);
        color: #ffffff;
      }

      /* 3D Isometric Mini Flashcards Stack Animation */
      .card-3k-visual-col {
        position: relative;
        height: 190px;
        display: flex;
        align-items: center;
        justify-content: center;
        perspective: 1000px;
      }

      .floating-card-stack {
        position: relative;
        width: 220px;
        height: 140px;
        transform-style: preserve-3d;
      }

      .mini-deck-card {
        position: absolute;
        width: 100%;
        height: 100%;
        border-radius: 18px;
        border: 1px solid rgba(255, 255, 255, 0.12);
        padding: 14px 16px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 16px 36px -8px rgba(0, 0, 0, 0.7);
        transition: all 0.3s ease;
      }

      .mini-card-3 {
        background: #090e1a;
        transform: translate3d(24px, -18px, -40px) rotate(8deg);
        opacity: 0.55;
        border-color: rgba(255, 255, 255, 0.06);
      }

      .mini-card-2 {
        background: #0e1628;
        transform: translate3d(12px, -9px, -20px) rotate(-4deg);
        opacity: 0.8;
        border-color: rgba(56, 189, 248, 0.2);
      }

      .mini-card-1 {
        background: linear-gradient(135deg, #152238 0%, #0d1526 100%);
        transform: translate3d(0, 0, 10px) rotate(1deg);
        border-color: rgba(56, 189, 248, 0.45);
        box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.8), 0 0 20px rgba(56, 189, 248, 0.2);
      }

      .mini-card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-size: 0.72rem;
        font-weight: 700;
        color: #38bdf8;
      }

      .mini-card-word {
        font-size: 1.3rem;
        font-weight: 850;
        color: #ffffff;
        letter-spacing: -0.01em;
      }

      .mini-card-trans {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.72rem;
        color: #94a3b8;
      }

      .mini-card-trans span {
        color: #34d399;
        font-weight: 700;
      }

      /* Hover animation for 3D stack */
      .card-3k-featured:hover .mini-card-1 {
        transform: translate3d(-4px, -6px, 25px) rotate(0deg);
      }
      .card-3k-featured:hover .mini-card-2 {
        transform: translate3d(18px, -16px, -10px) rotate(-6deg);
      }
      .card-3k-featured:hover .mini-card-3 {
        transform: translate3d(36px, -26px, -30px) rotate(12deg);
      }

      /* ==========================================================
         DYNAMIC SECTIONS LIST (Add, Edit, Drag and Move)
         ========================================================== */
      .sections-container-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        padding-top: 6px;
      }

      .sections-heading-group {
        display: flex;
        align-items: center;
        gap: 10px;
      }

      .sections-main-heading {
        font-size: 1.18rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #ffffff;
      }

      .sections-count-pill {
        font-size: 0.72rem;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 9999px;
        background: rgba(255, 255, 255, 0.08);
        color: #94a3b8;
      }

      .btn-create-section-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 8px 16px;
        border-radius: 12px;
        background: rgba(56, 189, 248, 0.12);
        border: 1px solid rgba(56, 189, 248, 0.35);
        color: #38bdf8;
        font-size: 0.82rem;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.18s ease;
      }

      .btn-create-section-pill:hover,
      .btn-create-section-pill:active {
        background: rgba(56, 189, 248, 0.25);
        color: #ffffff;
        transform: scale(0.98);
      }

      .sections-grid {
        display: grid;
        grid-template-columns: 1fr;
        gap: 14px;
      }

      @media (min-width: 720px) {
        .sections-grid {
          grid-template-columns: repeat(2, 1fr);
        }
      }

      @media (min-width: 1020px) {
        .sections-grid {
          grid-template-columns: repeat(3, 1fr);
        }
      }

      /* Custom Section Card (Draggable, Editable) */
      .custom-section-card {
        position: relative;
        background: #111724;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 16px 18px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        gap: 12px;
        cursor: pointer;
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        user-select: none;
      }

      .custom-section-card:hover {
        background: #151d2e;
        border-color: rgba(255, 255, 255, 0.16);
        transform: translateY(-2px);
        box-shadow: 0 14px 30px -8px rgba(0, 0, 0, 0.6);
      }

      .custom-section-card.dragging {
        opacity: 0.45;
        border: 1px dashed #38bdf8;
        transform: scale(0.97);
      }

      .custom-section-card.drag-over {
        border-color: #38bdf8;
        box-shadow: 0 0 16px rgba(56, 189, 248, 0.4);
      }

      .section-card-top-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 8px;
      }

      .section-drag-handle {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 30px;
        height: 30px;
        border-radius: 8px;
        color: #64748b;
        cursor: grab;
        transition: color 0.15s ease, background 0.15s ease;
      }

      .section-drag-handle:hover,
      .section-drag-handle:active {
        color: #e2e8f0;
        background: rgba(255, 255, 255, 0.06);
      }

      .section-icon-badge {
        font-size: 1.35rem;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 38px;
        height: 38px;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
      }

      .section-card-actions {
        display: flex;
        align-items: center;
        gap: 6px;
      }

      .section-tool-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 30px;
        height: 30px;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        color: #94a3b8;
        cursor: pointer;
        transition: all 0.15s ease;
      }

      .section-tool-btn:hover {
        background: rgba(255, 255, 255, 0.1);
        color: #ffffff;
      }

      .section-main-meta {
        display: flex;
        flex-direction: column;
        gap: 3px;
      }

      .section-title-text {
        font-size: 1.05rem;
        font-weight: 750;
        color: #ffffff;
        letter-spacing: -0.015em;
      }

      .section-subtitle-text {
        font-size: 0.78rem;
        color: #94a3b8;
        line-height: 1.35;
      }

      .section-card-bottom {
        display: flex;
        flex-direction: column;
        gap: 6px;
        padding-top: 4px;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
      }

      .section-bottom-stats {
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-size: 0.74rem;
        color: #cbd5e1;
        font-weight: 600;
      }

      .section-card-progress {
        width: 100%;
        height: 4px;
        border-radius: 9999px;
        background: rgba(255, 255, 255, 0.07);
        overflow: hidden;
      }

      .section-card-progress-fill {
        height: 100%;
        border-radius: 9999px;
        transition: width 0.3s ease;
      }

      /* Quick reorder buttons for touch / accessibility */
      .reorder-btns-group {
        display: inline-flex;
        align-items: center;
        gap: 2px;
      }

      .btn-reorder-arrow {
        width: 24px;
        height: 24px;
        border-radius: 6px;
        background: transparent;
        border: none;
        color: #64748b;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0;
      }

      .btn-reorder-arrow:hover {
        color: #ffffff;
        background: rgba(255, 255, 255, 0.08);
      }

      /* ==========================================================
         SLIDE-OVER MENU DRAWER (Moving Settings to Menu)
         ========================================================== */
      .menu-drawer-backdrop {
        position: fixed;
        inset: 0;
        background: rgba(0, 0, 0, 0.75);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        z-index: 999;
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.28s cubic-bezier(0.16, 1, 0.3, 1);
      }

      .menu-drawer-backdrop.open {
        opacity: 1;
        pointer-events: auto;
      }

      .app-menu-drawer {
        position: fixed;
        top: 0;
        left: 0;
        bottom: 0;
        width: 88%;
        max-width: 440px;
        background: #0d1322;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 24px 0 60px rgba(0, 0, 0, 0.85);
        z-index: 1000;
        display: flex;
        flex-direction: column;
        transform: translateX(-100%);
        transition: transform 0.32s cubic-bezier(0.16, 1, 0.3, 1);
        overflow: hidden;
      }

      .app-menu-drawer.open {
        transform: translateX(0);
      }

      .drawer-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 20px 22px 16px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        flex-shrink: 0;
      }

      .drawer-brand {
        display: flex;
        align-items: center;
        gap: 12px;
      }

      .drawer-close-btn {
        width: 36px;
        height: 36px;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.08);
        color: #94a3b8;
        font-size: 1.25rem;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.15s ease;
      }

      .drawer-close-btn:hover {
        background: rgba(255, 255, 255, 0.1);
        color: #ffffff;
      }

      .drawer-scroll-body {
        flex: 1;
        overflow-y: auto;
        padding: 18px 22px 28px;
        display: flex;
        flex-direction: column;
        gap: 20px;
      }

      .drawer-section-heading {
        font-size: 0.72rem;
        font-weight: 750;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #64748b;
        margin-bottom: 8px;
      }

      .drawer-nav-list {
        display: flex;
        flex-direction: column;
        gap: 6px;
      }

      .drawer-nav-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px 14px;
        border-radius: 14px;
        background: rgba(255, 255, 255, 0.035);
        border: 1px solid rgba(255, 255, 255, 0.06);
        color: #e2e8f0;
        font-size: 0.88rem;
        font-weight: 650;
        cursor: pointer;
        transition: all 0.18s ease;
      }

      .drawer-nav-item:hover,
      .drawer-nav-item:active {
        background: rgba(56, 189, 248, 0.12);
        border-color: rgba(56, 189, 248, 0.3);
        color: #ffffff;
      }

      .drawer-nav-item-left {
        display: flex;
        align-items: center;
        gap: 10px;
      }
`;

// Insert the modern CSS before </style>
html = html.replace('</style>', `${modernHomeAndMenuCss}\n    </style>`);

console.log('Appended home and menu CSS.');

fs.writeFileSync('index.html', html, 'utf8');
