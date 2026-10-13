const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');
console.log('Original index.html length:', html.length);

// =========================================================================
// 1. RESPONSIVE CSS & HEADER FIX (PC vs Mobile Navigation, Menu on Left)
// =========================================================================

// Let's replace the broken top nav in #screen-flashcard (lines 3598-3615 approx)
const badFlashcardNav = /<header class="flashcard-top-nav">[\s\S]*?<\/header>/;

const newFlashcardNav = `<header class="flashcard-top-nav">
          <div class="top-nav-main">
            <!-- Mobile Menu Toggle on FAR LEFT (Mobile only) -->
            <button class="mobile-hamburger-btn" id="btn-flashcard-menu" aria-label="Open Navigation Menu" title="Menu">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="3" y1="6" x2="21" y2="6"/>
                <line x1="3" y1="12" x2="21" y2="12"/>
                <line x1="3" y1="18" x2="21" y2="18"/>
              </svg>
            </button>

            <!-- Back to Subsections / Home -->
            <button class="breadcrumb-back-btn" id="btn-breadcrumb-back" title="Back to Subsections" aria-label="Back to Subsections">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="15 18 9 12 15 6"/>
              </svg>
              <span>Tiers</span>
            </button>

            <!-- Active Deck & Category Badge -->
            <div class="top-nav-center-group">
              <span class="top-tier-pill" id="breadcrumb-deck-label">Cards 800 – 1000</span>
              <span class="top-category-pill" id="current-category">Kitchen & Cooking</span>
            </div>

            <!-- Right Controls: Learned Checkbox, Status 1 to 3k, Shuffle, Settings -->
            <div class="top-nav-actions">
              <!-- Flashcard Learned Toggle -->
              <button type="button" class="btn-top-learned-toggle" id="btn-top-learned-toggle" title="Toggle Learned Status" aria-label="Mark Card as Learned">
                <span class="learned-check-indicator">✓</span>
                <span class="learned-status-text">Learned</span>
              </button>

              <!-- Global Status 1 to 3K Counter -->
              <div class="global-status-3k-pill" id="flashcard-3k-status-pill" title="Status across 3,000 vocabulary words">
                <span class="status-dot-pulse"></span>
                <span id="flashcard-3k-status-text">0 / 3,000</span>
              </div>

              <button class="shuffle-btn" id="btn-shuffle" title="Shuffle cards" aria-label="Shuffle cards">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M2 18h1.4c1.3 0 2.5-.6 3.3-1.7l6.6-8.6c.8-1.1 2-1.7 3.3-1.7H22" />
                  <path d="m18 2 4 4-4 4" />
                  <path d="M2 6h1.4c1.3 0 2.5.6 3.3 1.7l2 2.6" />
                  <path d="M14.6 13.7l2.1 2.6c.8 1.1 2 1.7 3.3 1.7H22" />
                  <path d="m18 20 4-4-4-4" />
                </svg>
              </button>

              <!-- Desktop Settings Button -->
              <button class="desktop-settings-btn" id="btn-desktop-settings" title="Open Settings" aria-label="Open Settings">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="3"></circle>
                  <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
                </svg>
              </button>

              <div class="counter-display">
                <span class="current-num" id="card-counter-current">800</span>
                <span class="counter-divider">/</span>
                <span class="total-num" id="card-counter-total">1000</span>
              </div>
            </div>
          </div>
          <!-- Single Slim Progress Line -->
          <div class="progress-track">
            <div class="progress-fill" id="progress-fill"></div>
          </div>
        </header>`;

if (badFlashcardNav.test(html)) {
  html = html.replace(badFlashcardNav, newFlashcardNav);
  console.log('Replaced bad flashcard top nav successfully!');
} else {
  console.warn('Could not match badFlashcardNav regex');
}

// =========================================================================
// 2. REDESIGN SCREEN-HOME TOP APP BAR (PC Nav vs Mobile Left Hamburger)
// =========================================================================

const oldHomeAppBar = /<header class="home-app-bar">[\s\S]*?<\/header>/;

const newHomeAppBar = `<header class="home-app-bar">
          <!-- Mobile Hamburger Button (FAR LEFT CORNER - Mobile Only) -->
          <button class="mobile-hamburger-btn" id="btn-home-menu" aria-label="Open Navigation Menu" title="Menu">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="3" y1="6" x2="21" y2="6"/>
              <line x1="3" y1="12" x2="21" y2="12"/>
              <line x1="3" y1="18" x2="21" y2="18"/>
            </svg>
          </button>

          <!-- Brand Logo & Identity -->
          <div class="brand-group">
            <div class="brand-icon-box">
              <span>✦</span>
            </div>
            <div class="brand-text-col">
              <span class="brand-title">3K Vocabulary</span>
              <span class="brand-subtitle">Sequential Trilingual Mastery</span>
            </div>
          </div>

          <!-- Desktop Navigation Bar (PC / Tablet Only - NEVER hamburger on PC) -->
          <nav class="desktop-nav-bar" aria-label="Main Navigation">
            <button type="button" class="desktop-nav-link active" id="desktop-nav-home">
              <span>🏠 Home</span>
            </button>
            <button type="button" class="desktop-nav-link" id="desktop-nav-3k">
              <span>⚡ 3k Vocabulary</span>
            </button>
            <button type="button" class="desktop-nav-link" id="desktop-nav-subsections">
              <span>📑 Tiers (800 – 1000)</span>
            </button>
            <button type="button" class="desktop-nav-link" id="desktop-nav-sections">
              <span>📚 My Sections</span>
            </button>
          </nav>

          <!-- Top Actions: Status 1 to 3k & Settings Modal Toggle -->
          <div class="home-top-actions">
            <!-- Global Learned Metric Pill -->
            <div class="global-status-3k-pill" id="home-3k-status-pill" title="Status across 3,000 words">
              <span class="status-dot-pulse"></span>
              <span>Status: <strong id="home-3k-status-count">0</strong> / 3,000</span>
            </div>

            <!-- Settings Button -->
            <button class="btn-settings-header" id="btn-home-settings" aria-label="Open Settings" title="Settings">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="3"></circle>
                <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
              </svg>
              <span class="desktop-only-text">Settings</span>
            </button>
          </div>
        </header>`;

if (oldHomeAppBar.test(html)) {
  html = html.replace(oldHomeAppBar, newHomeAppBar);
  console.log('Replaced home app bar successfully!');
} else {
  console.warn('Could not match oldHomeAppBar regex');
}

// =========================================================================
// 3. REDESIGN FEATURED "3K VOCABULARY" CARD ON HOME PAGE
// =========================================================================

// Requirements:
// - Labeled simply "3k Vocabulary"
// - Tapping label or card body opens subsections (800 - 1000)
// - Has dedicated "Resume" button that directly redirects to specific subsection and card left off on!
// - Shows Status 1 to 3k learned status with progress bar

const oldFeatured3k = /<div class="featured-3k-wrapper" id="featured-3k-wrapper">[\s\S]*?<!-- ====================================================\s*-->\s*<!-- DYNAMIC CUSTOM SECTIONS/;

const newFeatured3k = `<div class="featured-3k-wrapper" id="featured-3k-wrapper">
            <div class="card-3k-featured" id="card-3k-featured" role="button" tabindex="0" aria-label="3k Vocabulary - Tap to open subsections">
              <!-- Specular Reflection Sheen -->
              <div class="card-3d-shine" id="card-3k-shine"></div>

              <div class="card-3k-layout">
                <!-- Left Info Column -->
                <div class="card-3k-info-col">
                  <div class="card-3k-badge-row">
                    <span class="badge-live-pulse">
                      <span class="pulse-indicator-dot"></span>
                      <span>Mastery Series</span>
                    </span>
                    <span class="badge-trilingual">3,000 Words</span>
                    <span class="badge-trilingual">ES · HI · TA</span>
                  </div>

                  <!-- SIMPLY LABELED '3k Vocabulary' -->
                  <h2 class="card-3k-title" id="label-3k-vocabulary">3k Vocabulary</h2>
                  
                  <p class="card-3k-desc">
                    Tap to explore subsections (Cards 800 – 1000 & all tiers). English, pure native Tamil script, verified photos, and native speech audio.
                  </p>

                  <!-- Real-time Status 1 to 3K Metric -->
                  <div class="card-3k-progress-box">
                    <div class="progress-meta-row">
                      <span>Status: <strong id="card-3k-learned-count">0</strong> / 3,000 Learned</span>
                      <span id="card-3k-learned-pct" style="color: #38bdf8; font-weight: 700;">0%</span>
                    </div>
                    <div class="progress-track-3k">
                      <div class="progress-fill-3k" id="progress-fill-3k-total" style="width: 0%;"></div>
                    </div>
                    <div class="progress-tier-hint">
                      <span>Active Tier: <strong>Cards 800 – 1000</strong></span>
                      <span id="tier-800-learned-stat">0 / 200 learned in tier</span>
                    </div>
                  </div>

                  <!-- Quick Action Controls -->
                  <div class="card-3k-actions">
                    <!-- RESUME BUTTON: Redirects directly to last visited card in active subsection -->
                    <button type="button" class="btn-launch-3k" id="btn-resume-3k-deck" title="Directly resume where you left off">
                      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">
                        <polygon points="5 3 19 12 5 21 5 3"></polygon>
                      </svg>
                      <span id="btn-resume-label">Resume (#800)</span>
                    </button>

                    <!-- OPEN SUBSECTIONS BUTTON -->
                    <button type="button" class="btn-subsections-3k" id="btn-open-subsections" title="View all 3,000 vocabulary subsections">
                      <span>Open Subsections (800 – 1000)</span>
                      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="9 18 15 12 9 6"/>
                      </svg>
                    </button>
                  </div>
                </div>

                <!-- Right 3D Layered Isometric Mini-Cards Stack -->
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
          <!-- DYNAMIC CUSTOM SECTIONS`;

if (oldFeatured3k.test(html)) {
  html = html.replace(oldFeatured3k, newFeatured3k);
  console.log('Replaced featured 3k card successfully!');
} else {
  console.warn('Could not match oldFeatured3k regex');
}

// =========================================================================
// 4. SUBSECTIONS SCREEN: FULL RANGE 1 TO 3K TIERS WITH 800-1000 ACTIVE
// =========================================================================

const oldSubsections = /<div class="app-screen" id="screen-subsections">[\s\S]*?<!-- ==========================================\s*-->\s*<!-- SCREEN 3: MODERN FLASHCARD VIEW/;

const newSubsections = `<div class="app-screen" id="screen-subsections">
        <header class="home-app-bar" style="padding-bottom: 12px;">
          <!-- Mobile Hamburger on FAR LEFT (Mobile Only) -->
          <button class="mobile-hamburger-btn" id="btn-subsections-menu" aria-label="Open Navigation Menu" title="Menu">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="3" y1="6" x2="21" y2="6"/>
              <line x1="3" y1="12" x2="21" y2="12"/>
              <line x1="3" y1="18" x2="21" y2="18"/>
            </svg>
          </button>

          <div class="brand-group">
            <button class="breadcrumb-back-btn" id="btn-back-to-home" title="Back to Home">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="15 18 9 12 15 6"/>
              </svg>
              <span>Back to Home</span>
            </button>
          </div>
          
          <div class="top-nav-center-group">
            <span class="brand-title" style="font-size: 1.05rem;">3k Vocabulary Subsections</span>
          </div>

          <div class="home-top-actions">
            <div class="global-status-3k-pill">
              <span class="status-dot-pulse"></span>
              <span>Total: <strong id="subsections-3k-total">0</strong> / 3,000</span>
            </div>
          </div>
        </header>

        <div class="home-scroll-canvas">
          <!-- Overview Banner -->
          <div class="subsections-overview-banner">
            <div class="banner-text-block">
              <div class="banner-kicker">3,000 WORD VOCABULARY SPECTRUM</div>
              <h3 class="banner-heading">Select a Subsection Tier</h3>
              <p class="banner-sub">Tap <strong>Cards 800 – 1000</strong> to open the full trilingual deck with HD photographs and verified Tamil audio.</p>
            </div>
            <button type="button" class="btn-direct-resume-tier" id="btn-resume-from-subsections">
              <span>Resume Card</span>
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
            </button>
          </div>

          <!-- Subsections Grid -->
          <div class="sections-grid" style="grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 14px;">
            <!-- ACTIVE TIER: 800 - 1000 -->
            <div class="custom-section-card active-tier-highlight" id="sub-tier-800-1000" role="button" tabindex="0">
              <div class="section-card-top-bar">
                <div style="display: flex; align-items: center; gap: 12px;">
                  <span class="section-icon-badge" style="background: rgba(56, 189, 248, 0.2); border-color: #38bdf8; font-size: 1.3rem;">🔥</span>
                  <div class="section-main-meta">
                    <div class="section-title-text" style="color: #38bdf8; font-size: 1.05rem;">Cards 800 – 1000 (Active)</div>
                    <div class="section-subtitle-text">Kitchen, Tools, Dining, Travel & Daily Life</div>
                  </div>
                </div>
                <span class="badge-live-pulse" style="font-size: 0.7rem; padding: 4px 10px;">STUDY NOW</span>
              </div>
              <div class="section-card-bottom">
                <div class="section-bottom-stats">
                  <span>Learned Status</span>
                  <span style="color: #38bdf8; font-weight: 700;" id="tier-800-stat-line">0 / 200 Learned</span>
                </div>
                <div class="section-card-progress">
                  <div class="section-card-progress-fill" id="tier-800-progress-bar" style="width: 0%; background: linear-gradient(90deg, #38bdf8, #10b981);"></div>
                </div>
              </div>
            </div>

            <!-- Tier 1: 1 - 200 -->
            <div class="custom-section-card" id="sub-tier-1-200" role="button" tabindex="0">
              <div class="section-card-top-bar">
                <div style="display: flex; align-items: center; gap: 12px;">
                  <span class="section-icon-badge">🌱</span>
                  <div class="section-main-meta">
                    <div class="section-title-text">Cards 1 – 200</div>
                    <div class="section-subtitle-text">Foundations, Pronouns & Everyday Basics</div>
                  </div>
                </div>
                <span class="badge-trilingual" style="font-size: 0.68rem;">200 Words</span>
              </div>
              <div class="section-card-bottom">
                <div class="section-bottom-stats"><span>Status</span><span style="color: #94a3b8;">0 / 200 Learned</span></div>
                <div class="section-card-progress"><div class="section-card-progress-fill" style="width: 0%; background: #64748b;"></div></div>
              </div>
            </div>

            <!-- Tier 2: 201 - 400 -->
            <div class="custom-section-card" id="sub-tier-201-400" role="button" tabindex="0">
              <div class="section-card-top-bar">
                <div style="display: flex; align-items: center; gap: 12px;">
                  <span class="section-icon-badge">🏠</span>
                  <div class="section-main-meta">
                    <div class="section-title-text">Cards 201 – 400</div>
                    <div class="section-subtitle-text">Family, Home, Time & Daily Routine</div>
                  </div>
                </div>
                <span class="badge-trilingual" style="font-size: 0.68rem;">200 Words</span>
              </div>
              <div class="section-card-bottom">
                <div class="section-bottom-stats"><span>Status</span><span style="color: #94a3b8;">0 / 200 Learned</span></div>
                <div class="section-card-progress"><div class="section-card-progress-fill" style="width: 0%; background: #64748b;"></div></div>
              </div>
            </div>

            <!-- Tier 3: 401 - 600 -->
            <div class="custom-section-card" id="sub-tier-401-600" role="button" tabindex="0">
              <div class="section-card-top-bar">
                <div style="display: flex; align-items: center; gap: 12px;">
                  <span class="section-icon-badge">🌳</span>
                  <div class="section-main-meta">
                    <div class="section-title-text">Cards 401 – 600</div>
                    <div class="section-subtitle-text">Nature, Weather, Colors & Surroundings</div>
                  </div>
                </div>
                <span class="badge-trilingual" style="font-size: 0.68rem;">200 Words</span>
              </div>
              <div class="section-card-bottom">
                <div class="section-bottom-stats"><span>Status</span><span style="color: #94a3b8;">0 / 200 Learned</span></div>
                <div class="section-card-progress"><div class="section-card-progress-fill" style="width: 0%; background: #64748b;"></div></div>
              </div>
            </div>

            <!-- Tier 4: 601 - 800 -->
            <div class="custom-section-card" id="sub-tier-601-800" role="button" tabindex="0">
              <div class="section-card-top-bar">
                <div style="display: flex; align-items: center; gap: 12px;">
                  <span class="section-icon-badge">✈️</span>
                  <div class="section-main-meta">
                    <div class="section-title-text">Cards 601 – 800</div>
                    <div class="section-subtitle-text">City Life, Transport, Shopping & Places</div>
                  </div>
                </div>
                <span class="badge-trilingual" style="font-size: 0.68rem;">200 Words</span>
              </div>
              <div class="section-card-bottom">
                <div class="section-bottom-stats"><span>Status</span><span style="color: #94a3b8;">0 / 200 Learned</span></div>
                <div class="section-card-progress"><div class="section-card-progress-fill" style="width: 0%; background: #64748b;"></div></div>
              </div>
            </div>

            <!-- Tier 6: 1001 - 1200 -->
            <div class="custom-section-card" id="sub-tier-1001-1200" role="button" tabindex="0">
              <div class="section-card-top-bar">
                <div style="display: flex; align-items: center; gap: 12px;">
                  <span class="section-icon-badge">💼</span>
                  <div class="section-main-meta">
                    <div class="section-title-text">Cards 1001 – 1200</div>
                    <div class="section-subtitle-text">Commerce, Work, Finance & Profession</div>
                  </div>
                </div>
                <span class="badge-trilingual" style="font-size: 0.68rem;">200 Words</span>
              </div>
              <div class="section-card-bottom">
                <div class="section-bottom-stats"><span>Status</span><span style="color: #94a3b8;">0 / 200 Learned</span></div>
                <div class="section-card-progress"><div class="section-card-progress-fill" style="width: 0%; background: #64748b;"></div></div>
              </div>
            </div>

            <!-- Tier 7: 1201 - 1400 -->
            <div class="custom-section-card" id="sub-tier-1201-1400" role="button" tabindex="0">
              <div class="section-card-top-bar">
                <div style="display: flex; align-items: center; gap: 12px;">
                  <span class="section-icon-badge">🧠</span>
                  <div class="section-main-meta">
                    <div class="section-title-text">Cards 1201 – 1400</div>
                    <div class="section-subtitle-text">Mind, Emotion, Character & Relationships</div>
                  </div>
                </div>
                <span class="badge-trilingual" style="font-size: 0.68rem;">200 Words</span>
              </div>
              <div class="section-card-bottom">
                <div class="section-bottom-stats"><span>Status</span><span style="color: #94a3b8;">0 / 200 Learned</span></div>
                <div class="section-card-progress"><div class="section-card-progress-fill" style="width: 0%; background: #64748b;"></div></div>
              </div>
            </div>

            <!-- Tier 8: 1401 - 1600 -->
            <div class="custom-section-card" id="sub-tier-1401-1600" role="button" tabindex="0">
              <div class="section-card-top-bar">
                <div style="display: flex; align-items: center; gap: 12px;">
                  <span class="section-icon-badge">🔬</span>
                  <div class="section-main-meta">
                    <div class="section-title-text">Cards 1401 – 1600</div>
                    <div class="section-subtitle-text">Science, Technology, Medicine & Body</div>
                  </div>
                </div>
                <span class="badge-trilingual" style="font-size: 0.68rem;">200 Words</span>
              </div>
              <div class="section-card-bottom">
                <div class="section-bottom-stats"><span>Status</span><span style="color: #94a3b8;">0 / 200 Learned</span></div>
                <div class="section-card-progress"><div class="section-card-progress-fill" style="width: 0%; background: #64748b;"></div></div>
              </div>
            </div>

            <!-- Tier 9: 1601 - 1800 -->
            <div class="custom-section-card" id="sub-tier-1601-1800" role="button" tabindex="0">
              <div class="section-card-top-bar">
                <div style="display: flex; align-items: center; gap: 12px;">
                  <span class="section-icon-badge">🎨</span>
                  <div class="section-main-meta">
                    <div class="section-title-text">Cards 1601 – 1800</div>
                    <div class="section-subtitle-text">Art, Literature, Music & Culture</div>
                  </div>
                </div>
                <span class="badge-trilingual" style="font-size: 0.68rem;">200 Words</span>
              </div>
              <div class="section-card-bottom">
                <div class="section-bottom-stats"><span>Status</span><span style="color: #94a3b8;">0 / 200 Learned</span></div>
                <div class="section-card-progress"><div class="section-card-progress-fill" style="width: 0%; background: #64748b;"></div></div>
              </div>
            </div>

            <!-- Tier 10: 1801 - 2000 -->
            <div class="custom-section-card" id="sub-tier-1801-2000" role="button" tabindex="0">
              <div class="section-card-top-bar">
                <div style="display: flex; align-items: center; gap: 12px;">
                  <span class="section-icon-badge">🏛️</span>
                  <div class="section-main-meta">
                    <div class="section-title-text">Cards 1801 – 2000</div>
                    <div class="section-subtitle-text">Government, Society, Law & History</div>
                  </div>
                </div>
                <span class="badge-trilingual" style="font-size: 0.68rem;">200 Words</span>
              </div>
              <div class="section-card-bottom">
                <div class="section-bottom-stats"><span>Status</span><span style="color: #94a3b8;">0 / 200 Learned</span></div>
                <div class="section-card-progress"><div class="section-card-progress-fill" style="width: 0%; background: #64748b;"></div></div>
              </div>
            </div>

            <!-- Tier 15: 2801 - 3000 -->
            <div class="custom-section-card" id="sub-tier-2801-3000" role="button" tabindex="0">
              <div class="section-card-top-bar">
                <div style="display: flex; align-items: center; gap: 12px;">
                  <span class="section-icon-badge">👑</span>
                  <div class="section-main-meta">
                    <div class="section-title-text">Cards 2801 – 3000</div>
                    <div class="section-subtitle-text">Advanced Fluency, Nuance & Mastery</div>
                  </div>
                </div>
                <span class="badge-trilingual" style="font-size: 0.68rem;">200 Words</span>
              </div>
              <div class="section-card-bottom">
                <div class="section-bottom-stats"><span>Status</span><span style="color: #94a3b8;">0 / 200 Learned</span></div>
                <div class="section-card-progress"><div class="section-card-progress-fill" style="width: 0%; background: #64748b;"></div></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ========================================== -->
      <!-- SCREEN 3: MODERN FLASHCARD VIEW`;

if (oldSubsections.test(html)) {
  html = html.replace(oldSubsections, newSubsections);
  console.log('Replaced subsections screen successfully!');
} else {
  console.warn('Could not match oldSubsections regex');
}

// =========================================================================
// 5. FLASHCARD FRONT FACE: ADD "LEARNED" BUTTON & VERIFY DOUBLE-TAP ONLY
// =========================================================================

// Let's ensure the card header bar on front has the "Learned" checkbox button
const oldCardHeaderFront = /<div class="card-header-bar">[\s\S]*?<div class="card-header-actions">[\s\S]*?<\/div>\s*<\/div>/;

const newCardHeaderFront = `<div class="card-header-bar">
                <div class="card-num-group">
                  <span class="card-num-tag" id="front-card-num">#800</span>
                  <span class="card-unboxed-cat" id="front-card-cat-label">KITCHEN</span>
                </div>
                
                <div class="card-header-actions">
                  <!-- DIRECT LEARNED CHECKBOX ON CARD -->
                  <button
                    class="btn-card-face-learned"
                    id="btn-card-learned-action"
                    title="Mark this card as learned (Status 1 to 3k)"
                    aria-label="Mark as learned"
                  >
                    <span class="learned-face-check">✓</span>
                    <span class="learned-face-text" id="front-learned-text">Mark Learned</span>
                  </button>

                  <button
                    class="icon-tool-btn"
                    id="front-edit-btn"
                    title="Edit card"
                    aria-label="Edit card"
                  >
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M12 20h9" />
                      <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z" />
                    </svg>
                  </button>
                  <button
                    class="speak-btn"
                    id="front-speak-btn"
                    title="Pronounce word"
                    aria-label="Pronounce word"
                  >
                    <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                      <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
                      <path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path>
                    </svg>
                  </button>
                </div>
              </div>`;

if (oldCardHeaderFront.test(html)) {
  html = html.replace(oldCardHeaderFront, newCardHeaderFront);
  console.log('Updated front card header with Learned button successfully!');
}

fs.writeFileSync('index.html', html, 'utf8');
console.log('HTML structure parts 1-5 updated.');
