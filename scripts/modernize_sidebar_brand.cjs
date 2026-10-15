const fs = require('fs');
const path = require('path');

const indexPath = path.join(__dirname, '..', 'index.html');
let html = fs.readFileSync(indexPath, 'utf8');

console.log('Original length:', html.length);

// 1. Add Google Fonts for Fredoka and Nunito if not present
if (!html.includes('fonts.googleapis.com/css2?family=Fredoka')) {
  const fontLinks = `    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@600;700&family=Nunito:wght@700;800;900&display=swap" rel="stylesheet">\n`;
  html = html.replace('<meta name="viewport"', fontLinks + '    <meta name="viewport"');
  console.log('Added Fredoka and Nunito fonts to head');
}

// 2. Replace the desktop sidebar brand lockup (remove owl mascot, remove "Vocabulary Mastery" subtext, keep simple "Stellar" label with Duolingo-style font)
const oldBrandLockupRegex = /<div class="sidebar-brand-lockup"[^>]*>[\s\S]*?<\/div>\s*<\/div>/;
const newBrandLockup = `<div class="sidebar-brand-lockup" id="sidebar-brand-home" title="Stellar Home">
            <span class="sidebar-brand-title">Stellar</span>
          </div>`;

if (oldBrandLockupRegex.test(html)) {
  html = html.replace(oldBrandLockupRegex, newBrandLockup);
  console.log('Replaced desktop sidebar brand lockup with simple "Stellar" label');
} else {
  console.log('Warning: oldBrandLockupRegex did not match directly');
}

// 3. Remove the unnecessary widget with the red 'X' mark (sidebar-footer-card)
const oldFooterCardRegex = /<!-- Sidebar Footer Status & Quick Sound -->\s*<div class="sidebar-footer-card">[\s\S]*?<\/div>\s*<\/div>/;
if (oldFooterCardRegex.test(html)) {
  html = html.replace(oldFooterCardRegex, '');
  console.log('Removed unnecessary sidebar-footer-card (Target 3,000 words & Sound FX)');
} else {
  // Try alternative match
  const altFooter = /<div class="sidebar-footer-card">[\s\S]*?<\/div>\s*<\/aside>/;
  if (altFooter.test(html)) {
    html = html.replace(altFooter, '</aside>');
    console.log('Removed sidebar-footer-card via altFooter');
  } else {
    console.log('Warning: sidebar-footer-card regex did not match');
  }
}

// 4. Replace mobile top bar logo with simple clean "Stellar" label
const oldMobileLogoRegex = /<div style="display: flex; align-items: center; gap: 8px;">\s*<svg width="30" height="30"[\s\S]*?<\/svg>\s*<span[^>]*>Stellar<\/span>\s*<\/div>/;
const newMobileLogo = `<div style="display: flex; align-items: center; gap: 8px;">
              <span class="mobile-brand-title">Stellar</span>
            </div>`;

if (oldMobileLogoRegex.test(html)) {
  html = html.replace(oldMobileLogoRegex, newMobileLogo);
  console.log('Replaced mobile top bar logo with clean "Stellar" text');
} else {
  console.log('Warning: oldMobileLogoRegex did not match directly');
}

// 5. Add custom CSS for Duolingo-grade Stellar brand and vibrant white navigation
const duolingoSidebarCss = `
    /* ========================================================================= */
    /* DUOLINGO-GRADE VIBRANT HIGH-CONTRAST SIDEBAR & BRAND                      */
    /* ========================================================================= */
    .app-desktop-sidebar {
      background: #0b1120 !important;
      border-right: 1.5px solid rgba(255, 255, 255, 0.09) !important;
      padding: 26px 16px 20px !important;
      box-shadow: 4px 0 24px rgba(0, 0, 0, 0.35) !important;
    }

    .sidebar-brand-lockup {
      display: flex !important;
      align-items: center !important;
      justify-content: flex-start !important;
      padding-bottom: 22px !important;
      padding-left: 10px !important;
      border-bottom: 1.5px solid rgba(255, 255, 255, 0.08) !important;
      margin-bottom: 14px !important;
      text-decoration: none !important;
      cursor: pointer !important;
      transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    }
    .sidebar-brand-lockup:hover {
      transform: scale(1.03) !important;
    }

    /* Brand label with Duolingo-style signature font */
    .sidebar-brand-title {
      font-family: 'Fredoka', 'Nunito', -apple-system, sans-serif !important;
      font-size: 2.25rem !important;
      font-weight: 700 !important;
      letter-spacing: -0.025em !important;
      color: #58cc02 !important; /* Iconic vibrant Duolingo green */
      text-shadow: 0 2px 14px rgba(88, 204, 2, 0.32) !important;
      display: inline-block !important;
      user-select: none !important;
      line-height: 1 !important;
    }

    .mobile-brand-title {
      font-family: 'Fredoka', 'Nunito', -apple-system, sans-serif !important;
      font-size: 1.55rem !important;
      font-weight: 700 !important;
      letter-spacing: -0.02em !important;
      color: #58cc02 !important;
      text-shadow: 0 2px 10px rgba(88, 204, 2, 0.28) !important;
      user-select: none !important;
    }

    /* Sidebar Navigation List */
    .sidebar-nav-list {
      display: flex !important;
      flex-direction: column !important;
      gap: 12px !important;
      margin-top: 14px !important;
      width: 100% !important;
    }

    /* Tactile Duolingo-Style Buttons */
    .sidebar-nav-btn {
      display: flex !important;
      align-items: center !important;
      gap: 16px !important;
      padding: 12px 16px !important;
      border-radius: 16px !important;
      background: transparent !important;
      border: 2px solid transparent !important;
      cursor: pointer !important;
      transition: all 0.22s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
      text-align: left !important;
      width: 100% !important;
      box-sizing: border-box !important;
      user-select: none !important;
      position: relative !important;
    }

    /* Bold Pure White Font for Sidebar Nav */
    .sidebar-nav-label {
      font-family: 'Nunito', 'Fredoka', -apple-system, sans-serif !important;
      font-size: 0.94rem !important;
      font-weight: 800 !important;
      letter-spacing: 0.05em !important;
      text-transform: uppercase !important;
      color: #ffffff !important; /* Pure Bright White */
      transition: color 0.16s ease !important;
      text-shadow: 0 1px 3px rgba(0, 0, 0, 0.4) !important;
    }

    /* Nav Icons */
    .sidebar-nav-icon {
      font-size: 1.4rem !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      width: 32px !important;
      height: 32px !important;
      flex-shrink: 0 !important;
      transition: transform 0.22s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
      filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.4)) !important;
    }

    /* Hover Animation: Smooth Spring Slide + Subtle Glow */
    .sidebar-nav-btn:hover {
      background: rgba(255, 255, 255, 0.08) !important;
      border-color: rgba(255, 255, 255, 0.15) !important;
      transform: translateX(6px) !important;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.35) !important;
    }
    .sidebar-nav-btn:hover .sidebar-nav-icon {
      transform: scale(1.18) rotate(4deg) !important;
    }
    .sidebar-nav-btn:hover .sidebar-nav-label {
      color: #ffffff !important;
    }

    /* Active Item (Electric Cobalt/Cyan Pill matching Duolingo Practice mode) */
    .sidebar-nav-btn.active {
      background: rgba(56, 189, 248, 0.16) !important;
      border: 2px solid #38bdf8 !important;
      box-shadow: 0 0 18px rgba(56, 189, 248, 0.28), inset 0 0 12px rgba(56, 189, 248, 0.08), 0 3px 0 #0284c7 !important;
      transform: translateY(-1px) !important;
    }
    .sidebar-nav-btn.active .sidebar-nav-label {
      color: #ffffff !important;
      text-shadow: 0 0 10px rgba(56, 189, 248, 0.5) !important;
    }
    .sidebar-nav-btn.active .sidebar-nav-icon {
      transform: scale(1.12) !important;
      filter: drop-shadow(0 0 8px rgba(56, 189, 248, 0.7)) !important;
    }

    /* Tactile Press Depth */
    .sidebar-nav-btn:active {
      transform: translateX(6px) translateY(2px) scale(0.98) !important;
      box-shadow: 0 1px 0 #0284c7 !important;
    }
`;

// Inject before </style>
html = html.replace('</style>', duolingoSidebarCss + '\n</style>');
console.log('Injected duolingoSidebarCss before </style>');

fs.writeFileSync(indexPath, html, 'utf8');
console.log('Finished writing index.html! New length:', html.length);
