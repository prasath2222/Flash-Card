const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');
console.log('Original index.html length:', html.length);

// 1. Update Title & Meta
html = html.replace(/<title>[\s\S]*?<\/title>/, '<title>Stellar – 3K Vocabulary Mastery</title>');
html = html.replace(/<meta name="description"[\s\S]*?>/, '<meta name="description" content="Stellar – Production-grade sequential multilingual vocabulary mastery app featuring English, Spanish, Hindi, and authentic native Tamil script." />');

// 2. Fix JavaScript duplicate declaration error
// Remove lines 9451-9453 where totalLearned was re-declared
const dupTarget = `        const mobileStatusEl = document.getElementById("mobile-status-count");
        if (mobileStatusEl) mobileStatusEl.textContent = totalLearned.toLocaleString();
        const totalLearned = learnedCardsSet.size;
        const totalWords = 3000;
        const totalPct = Math.min(100, ((totalLearned / totalWords) * 100)).toFixed(1);`;

const dupRepl = `        const mobileStatusEl = document.getElementById("mobile-status-count");
        if (mobileStatusEl) mobileStatusEl.textContent = totalLearned.toLocaleString();`;

if (html.includes(dupTarget)) {
  html = html.replace(dupTarget, dupRepl);
  console.log('Fixed duplicate totalLearned declaration!');
} else {
  console.log('Duplicate totalLearned target pattern not found, checking alternatives...');
  // Fallback search
  html = html.replace(
    /const mobileStatusEl = document\.getElementById\("mobile-status-count"\);\s*if \(mobileStatusEl\) mobileStatusEl\.textContent = totalLearned\.toLocaleString\(\);\s*const totalLearned = learnedCardsSet\.size;\s*const totalWords = 3000;\s*const totalPct = Math\.min\(100, \(\(totalLearned \/ totalWords\) \* 100\)\)\.toFixed\(1\);/,
    'const mobileStatusEl = document.getElementById("mobile-status-count");\n        if (mobileStatusEl) mobileStatusEl.textContent = totalLearned.toLocaleString();'
  );
}

// 3. Update Brand Name from VOCAB 3K to Stellar in Sidebar & Mobile Bar & Drawer
html = html.replace(
  /<span class="sidebar-brand-title">VOCAB 3K<\/span>/g,
  '<span class="sidebar-brand-title">Stellar</span>'
);
html = html.replace(
  /<span class="sidebar-brand-sub">Mastery Studio<\/span>/g,
  '<span class="sidebar-brand-sub">Vocabulary Mastery</span>'
);
html = html.replace(
  /<span class="mobile-brand-title">VOCAB 3K<\/span>/g,
  '<span class="mobile-brand-title">Stellar</span>'
);
html = html.replace(
  /<span class="brand-title" style="font-size: 1rem;">Polyglot Studio<\/span>[\s\S]*?<span class="brand-subtitle">Level 4 · 14-Day Streak 🔥<\/span>/,
  '<span class="brand-title" style="font-size: 1.1rem; font-weight: 800; color: #ffffff;">Stellar</span>\n            <span class="brand-subtitle" style="font-size: 0.75rem; color: #38bdf8; font-weight: 600;">Vocabulary Mastery</span>'
);

// 4. Remove 'Tiers (800–1000)' button from Sidebar Nav List
const sidebarTierRegex = /<button type="button" class="sidebar-nav-btn" id="nav-btn-subsections">[\s\S]*?<\/button>\s*/;
if (sidebarTierRegex.test(html)) {
  html = html.replace(sidebarTierRegex, '');
  console.log('Removed Tiers (800-1000) from left sidebar navigation!');
}

// 5. In desktop top header: remove 7 Days streak badge AND settings button
const desktopHeaderStatsRegex = /<div class="desktop-header-stats">[\s\S]*?<\/header>/;
const newDesktopHeaderStats = `<div class="desktop-header-stats">
            <!-- Global Status 1 to 3K Learned -->
            <div class="stat-badge-duo stat-badge-mastery" id="desktop-3k-status-badge" title="Status across 3,000 words">
              <span>⚡</span>
              <span>Status: <strong id="desktop-status-count">0</strong> / 3,000</span>
            </div>
          </div>
        </header>`;

if (desktopHeaderStatsRegex.test(html)) {
  html = html.replace(desktopHeaderStatsRegex, newDesktopHeaderStats);
  console.log('Cleaned desktop header stats (removed 7 days streak and settings button)!');
}

// 6. In mobile top bar: remove 7d streak badge, keep only mobile status
const mobileStreakRegex = /<div class="stat-badge-duo stat-badge-streak" style="padding: 4px 10px; font-size: 0\.75rem;">[\s\S]*?<\/div>\s*/;
if (mobileStreakRegex.test(html)) {
  html = html.replace(mobileStreakRegex, '');
  console.log('Removed mobile 7d streak badge!');
}

// 7. Fix '+ Add Section' button to eliminate double '+' symbol
// Previously: <svg>+</svg> <span>+ Add Section</span> -> user saw two plus signs!
html = html.replace(
  /<span>\+ Add Section<\/span>/g,
  '<span>Add Section</span>'
);
console.log('Fixed Add Section label to single clean plus icon + Add Section!');

// 8. Improve Home Screen hierarchy:
// Header: "Learning Sections" -> Primary: 3k Vocabulary -> Below: Custom Sections
const oldSectionsHeader = `<div class="sections-container-header">
            <div class="sections-heading-group">
              <h3 class="sections-main-heading">My Learning Sections</h3>
              <span style="font-size: 0.85rem; color: #94a3b8;" id="sections-count-pill">4 Decks</span>
            </div>`;

const newSectionsHeader = `<div class="sections-container-header" style="margin-top: 10px;">
            <div class="sections-heading-group">
              <h3 class="sections-main-heading">Custom Sections</h3>
              <span style="font-size: 0.85rem; color: #94a3b8;" id="sections-count-pill">4 Decks</span>
            </div>`;

if (html.includes(oldSectionsHeader)) {
  html = html.replace(oldSectionsHeader, newSectionsHeader);
  console.log('Updated Custom Sections header!');
}

// Add Main Section super-header above 3k Vocabulary
const featuredWrapperStart = `<div class="featured-3k-wrapper" id="featured-3k-wrapper">`;
const newHomeMainSectionGroup = `<div class="home-main-section-group" style="display: flex; flex-direction: column; gap: 14px;">
            <div class="main-section-header" style="display: flex; flex-direction: column; gap: 4px;">
              <h1 class="main-section-headline" style="font-size: 1.6rem; font-weight: 800; color: #ffffff; letter-spacing: -0.02em; margin: 0;">Learning Sections</h1>
              <p class="main-section-subline" style="font-size: 0.9rem; color: #94a3b8; margin: 0;">Select the primary 3,000 core vocabulary deck or organize custom study tracks below.</p>
            </div>

            <div class="featured-3k-wrapper" id="featured-3k-wrapper">`;

if (html.includes(featuredWrapperStart) && !html.includes('main-section-headline')) {
  html = html.replace(featuredWrapperStart, newHomeMainSectionGroup);
  console.log('Added top Learning Sections headline above 3k Vocabulary!');
}

// 9. Ensure hamburger menu is STRICTLY at top left on mobile, and NEVER on desktop:
// In CSS, add explicit rule ensuring .mobile-hamburger-btn is hidden on desktop and pinned left on mobile
const cssInject = `
      /* PRODUCTION-GRADE MOBILE & DESKTOP HEADER DISCIPLINE */
      @media (min-width: 768px) {
        .mobile-hamburger-btn {
          display: none !important;
          visibility: hidden !important;
          pointer-events: none !important;
        }
      }

      @media (max-width: 767px) {
        .mobile-top-bar {
          display: flex !important;
          align-items: center !important;
          justify-content: space-between !important;
          padding: 10px 16px !important;
          position: sticky !important;
          top: 0 !important;
          left: 0 !important;
          right: 0 !important;
          width: 100% !important;
          background: #0b1120 !important;
          z-index: 100 !important;
        }

        .mobile-left-cluster {
          display: flex !important;
          align-items: center !important;
          gap: 12px !important;
          margin-right: auto !important;
        }

        .mobile-hamburger-btn {
          display: flex !important;
          align-items: center !important;
          justify-content: center !important;
          flex-shrink: 0 !important;
          margin: 0 !important;
        }
      }
`;

html = html.replace('</style>', `${cssInject}\n</style>`);
console.log('Injected explicit mobile top-left and desktop hamburger display rules!');

fs.writeFileSync('index.html', html, 'utf8');
console.log('Saved index.html successfully! New length:', html.length);
