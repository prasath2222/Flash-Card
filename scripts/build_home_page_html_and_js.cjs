const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

// 1. REPLACE screen-home and screen-subsections with our modern production-grade structure
const homeAndSubsectionsPattern = /<!-- ========================================== -->\s*<!-- SCREEN 1: HOME SCREEN[\s\S]*?<!-- ========================================== -->\s*<!-- SCREEN 3: MODERN FLASHCARD VIEW/;

const modernHomeAndSubsectionsHtml = `<!-- ========================================== -->
      <!-- SCREEN 1: MODERN RESPONSIVE HOME SCREEN     -->
      <!-- ========================================== -->
      <div class="app-screen active-screen" id="screen-home">
        <!-- Top App Bar -->
        <header class="home-app-bar">
          <div class="brand-group">
            <div class="brand-icon-box">
              <span>✦</span>
            </div>
            <div class="brand-text-col">
              <span class="brand-title">Polyglot Studio</span>
              <span class="brand-subtitle">Sequential Trilingual Learning</span>
            </div>
          </div>
          <div class="home-top-actions">
            <button class="btn-menu-drawer-toggle" id="btn-home-menu" aria-label="Open Settings and Menu" title="Open Settings and Menu">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="3" y1="6" x2="21" y2="6"/>
                <line x1="3" y1="12" x2="21" y2="12"/>
                <line x1="3" y1="18" x2="21" y2="18"/>
              </svg>
              <span>Menu</span>
            </button>
          </div>
        </header>

        <!-- Main Scrollable Canvas -->
        <div class="home-scroll-canvas">
          <!-- ==================================================== -->
          <!-- FEATURED 3K VOCABULARY SECTION (Interactive 3D Card) -->
          <!-- ==================================================== -->
          <div class="featured-3k-wrapper" id="featured-3k-wrapper">
            <div class="card-3k-featured" id="card-3k-featured" role="button" tabindex="0" aria-label="3K Vocabulary collection - Click to study">
              <!-- Dynamic Specular Reflection Light Sheen -->
              <div class="card-3d-shine" id="card-3k-shine"></div>

              <div class="card-3k-layout">
                <!-- Left Info Column -->
                <div class="card-3k-info-col">
                  <div class="card-3k-badge-row">
                    <span class="badge-live-pulse">
                      <span class="pulse-indicator-dot"></span>
                      <span>Featured Collection</span>
                    </span>
                    <span class="badge-trilingual">3,000 Words</span>
                    <span class="badge-trilingual">ES · HI · TA</span>
                  </div>

                  <h2 class="card-3k-title">3K Vocabulary</h2>
                  <p class="card-3k-desc">
                    Comprehensive sequential mastery deck featuring verified HD photographs, pure native Tamil script, slow audio, and instant recall mnemonics.
                  </p>

                  <!-- Real-time Progress Metric -->
                  <div class="card-3k-progress-box">
                    <div class="progress-meta-row">
                      <span>Active Tier: <strong>Cards 800 – 1000</strong></span>
                      <span>800 / 1000 (80%)</span>
                    </div>
                    <div class="progress-track-3k">
                      <div class="progress-fill-3k" style="width: 80%;"></div>
                    </div>
                  </div>

                  <!-- Quick Action Controls -->
                  <div class="card-3k-actions">
                    <button type="button" class="btn-launch-3k" id="btn-launch-3k-deck">
                      <span>Resume Study</span>
                      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
                        <polygon points="5 3 19 12 5 21 5 3"></polygon>
                      </svg>
                    </button>
                    <button type="button" class="btn-subsections-3k" id="btn-open-subsections">
                      <span>View Sub-sections</span>
                      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="9 18 15 12 9 6"/>
                      </svg>
                    </button>
                  </div>
                </div>

                <!-- Right 3D Layered Isometric Mini-Cards Stack -->
                <div class="card-3k-visual-col" aria-hidden="true">
                  <div class="floating-card-stack" id="floating-card-stack">
                    <!-- Layer 3 (Deepest) -->
                    <div class="mini-deck-card mini-card-3">
                      <div class="mini-card-header">
                        <span>#802</span>
                        <span>SINK</span>
                      </div>
                      <div class="mini-card-word">SINK</div>
                      <div class="mini-card-trans">
                        <span>fregadero</span> · தொட்டி
                      </div>
                    </div>
                    <!-- Layer 2 (Middle) -->
                    <div class="mini-deck-card mini-card-2">
                      <div class="mini-card-header">
                        <span>#801</span>
                        <span>OVEN</span>
                      </div>
                      <div class="mini-card-word">OVEN</div>
                      <div class="mini-card-trans">
                        <span>horno</span> · அடுமனை
                      </div>
                    </div>
                    <!-- Layer 1 (Top Hero) -->
                    <div class="mini-deck-card mini-card-1">
                      <div class="mini-card-header">
                        <span>#800</span>
                        <span>STOVE</span>
                      </div>
                      <div class="mini-card-word">STOVE</div>
                      <div class="mini-card-trans">
                        <span>estufa</span> · அடுப்பு
                      </div>
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
              <span class="sections-count-pill" id="sections-count-pill">4 Decks</span>
            </div>
            <button type="button" class="btn-create-section-pill" id="btn-open-add-section">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
                <line x1="12" y1="5" x2="12" y2="19"/>
                <line x1="5" y1="12" x2="19" y2="12"/>
              </svg>
              <span>+ Add Section</span>
            </button>
          </div>

          <!-- Draggable Sections Grid -->
          <div class="sections-grid" id="sections-grid">
            <!-- Dynamically populated by JavaScript from localStorage -->
          </div>
        </div>
      </div>

      <!-- ========================================== -->
      <!-- SCREEN 2: DECK SUB-SECTIONS VIEW            -->
      <!-- ========================================== -->
      <div class="app-screen" id="screen-subsections">
        <header class="home-app-bar" style="padding-bottom: 12px;">
          <div class="brand-group">
            <button class="breadcrumb-back-btn" id="btn-back-to-home">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="15 18 9 12 15 6"/>
              </svg>
              <span>Back to Home</span>
            </button>
          </div>
          <span class="brand-title" style="font-size: 0.95rem;">3K Vocabulary Tiers</span>
        </header>

        <div class="home-scroll-canvas">
          <div class="sections-grid" style="grid-template-columns: 1fr;">
            <!-- Active Tier: 800-1000 -->
            <div class="custom-section-card" id="sub-tier-800-1000" style="border-color: rgba(56, 189, 248, 0.45); background: #131c2e;">
              <div class="section-card-top-bar">
                <div style="display: flex; align-items: center; gap: 10px;">
                  <span class="section-icon-badge" style="background: rgba(56, 189, 248, 0.15); border-color: rgba(56, 189, 248, 0.3);">🔥</span>
                  <div class="section-main-meta">
                    <div class="section-title-text" style="color: #38bdf8;">Cards 800 – 1000 (Active)</div>
                    <div class="section-subtitle-text">Kitchen, Tools, Dining, Travel & Daily Life</div>
                  </div>
                </div>
                <span class="badge-live-pulse" style="font-size: 0.65rem;">Active</span>
              </div>
              <div class="section-card-bottom">
                <div class="section-bottom-stats">
                  <span>Progress</span>
                  <span style="color: #38bdf8;">800 / 1000</span>
                </div>
                <div class="section-card-progress">
                  <div class="section-card-progress-fill" style="width: 80%; background: #38bdf8;"></div>
                </div>
              </div>
            </div>

            <!-- Tier 600-800 -->
            <div class="custom-section-card" id="sub-tier-600-800">
              <div class="section-card-top-bar">
                <div style="display: flex; align-items: center; gap: 10px;">
                  <span class="section-icon-badge">🌿</span>
                  <div class="section-main-meta">
                    <div class="section-title-text">Cards 600 – 800</div>
                    <div class="section-subtitle-text">Nature, Weather, Science & Environment</div>
                  </div>
                </div>
              </div>
              <div class="section-card-bottom">
                <div class="section-bottom-stats">
                  <span>Progress</span>
                  <span>600 / 800</span>
                </div>
                <div class="section-card-progress">
                  <div class="section-card-progress-fill" style="width: 75%; background: #10b981;"></div>
                </div>
              </div>
            </div>

            <!-- Tier 400-600 -->
            <div class="custom-section-card" id="sub-tier-400-600">
              <div class="section-card-top-bar">
                <div style="display: flex; align-items: center; gap: 10px;">
                  <span class="section-icon-badge">🏛️</span>
                  <div class="section-main-meta">
                    <div class="section-title-text">Cards 400 – 600</div>
                    <div class="section-subtitle-text">Society, Careers, City & Architecture</div>
                  </div>
                </div>
              </div>
              <div class="section-card-bottom">
                <div class="section-bottom-stats">
                  <span>Progress</span>
                  <span>400 / 600</span>
                </div>
                <div class="section-card-progress">
                  <div class="section-card-progress-fill" style="width: 66%; background: #818cf8;"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ========================================== -->
      <!-- SCREEN 3: MODERN FLASHCARD VIEW`;

html = html.replace(homeAndSubsectionsPattern, modernHomeAndSubsectionsHtml);

// 2. Add Home and Menu icon buttons into Screen 3 Top Nav
html = html.replace(
  '<button class="breadcrumb-back-btn" id="btn-breadcrumb-back" title="Back to Decks" aria-label="Back to Decks">',
  `<button class="breadcrumb-back-btn" id="btn-breadcrumb-back" title="Back to Home" aria-label="Back to Home">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
                <polyline points="9 22 9 12 15 12 15 22"/>
              </svg>
              <span>Home</span>
            </button>`
);

html = html.replace(
  '<div class="top-nav-actions">',
  `<div class="top-nav-actions">
              <button class="shuffle-btn" id="btn-flashcard-menu" title="Menu & Settings" aria-label="Menu & Settings">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="3" y1="6" x2="21" y2="6"/>
                  <line x1="3" y1="12" x2="21" y2="12"/>
                  <line x1="3" y1="18" x2="21" y2="18"/>
                </svg>
              </button>`
);

// 3. ADD SLIDE-OVER MENU DRAWER AND SECTION MODALS (Before </body>)
const slideOverDrawerAndModalsHtml = `
    <!-- ========================================================== -->
    <!-- SLIDE-OVER NAVIGATION & SETTINGS DRAWER                     -->
    <!-- ========================================================== -->
    <div class="menu-drawer-backdrop" id="menu-drawer-backdrop"></div>
    <aside class="app-menu-drawer" id="app-menu-drawer" aria-label="App Menu and Settings">
      <!-- Drawer Header -->
      <div class="drawer-header">
        <div class="drawer-brand">
          <div class="brand-icon-box" style="width: 36px; height: 36px; font-size: 1.1rem;">
            <span>✦</span>
          </div>
          <div class="brand-text-col">
            <span class="brand-title" style="font-size: 1rem;">Polyglot Studio</span>
            <span class="brand-subtitle">Level 4 · 14-Day Streak 🔥</span>
          </div>
        </div>
        <button type="button" class="drawer-close-btn" id="drawer-close-btn" aria-label="Close Menu">&times;</button>
      </div>

      <!-- Drawer Scroll Body -->
      <div class="drawer-scroll-body">
        <!-- Quick Screen Navigation -->
        <div>
          <div class="drawer-section-heading">Navigation</div>
          <div class="drawer-nav-list">
            <div class="drawer-nav-item" id="menu-nav-home" role="button" tabindex="0">
              <div class="drawer-nav-item-left">
                <span>🏠</span>
                <span>Home / Decks</span>
              </div>
              <span style="font-size: 0.72rem; color: #94a3b8;">Overview</span>
            </div>
            <div class="drawer-nav-item" id="menu-nav-3k" role="button" tabindex="0">
              <div class="drawer-nav-item-left">
                <span>⚡</span>
                <span>3K Vocabulary</span>
              </div>
              <span style="font-size: 0.72rem; color: #38bdf8;">800 / 1000</span>
            </div>
            <div class="drawer-nav-item" id="menu-nav-subsections" role="button" tabindex="0">
              <div class="drawer-nav-item-left">
                <span>📑</span>
                <span>Deck Tiers</span>
              </div>
              <span style="font-size: 0.72rem; color: #94a3b8;">All Tiers</span>
            </div>
          </div>
        </div>

        <!-- Integrated Audio Studio & Sound Settings -->
        <div>
          <div class="drawer-section-heading">Audio & Speech Studio</div>
          <div class="settings-audio-container">
            <!-- 1. Background Ambient Music -->
            <div class="audio-card">
              <div class="audio-card-header">
                <div class="audio-card-title-group">
                  <span class="audio-icon-badge">🎵</span>
                  <div>
                    <div class="audio-section-title">Focus Ambient Music</div>
                    <div class="audio-section-sub">Procedural binaural focus tones</div>
                  </div>
                </div>
                <label class="toggle-switch" aria-label="Toggle Background Music">
                  <input type="checkbox" id="toggle-bgm" />
                  <span class="toggle-slider"></span>
                </label>
              </div>

              <div id="bgm-panel" style="display: none; flex-direction: column; gap: 10px;">
                <div class="audio-mode-selector">
                  <button type="button" class="audio-chip-btn active" data-bgm="lofi">Lo-Fi Pad</button>
                  <button type="button" class="audio-chip-btn" data-bgm="alpha">Alpha 10Hz</button>
                  <button type="button" class="audio-chip-btn" data-bgm="zen">Zen Ambient</button>
                </div>
                <div class="audio-slider-group">
                  <div class="audio-slider-label">
                    <span>Music Volume</span>
                    <span class="val-badge" id="badge-bgm-vol">25%</span>
                  </div>
                  <input type="range" class="settings-slider" id="slider-bgm-vol" min="0" max="100" value="25" />
                </div>
              </div>
            </div>

            <!-- 2. Voice & Speech Pronunciation -->
            <div class="audio-card">
              <div class="audio-card-header">
                <div class="audio-card-title-group">
                  <span class="audio-icon-badge">🎙️</span>
                  <div>
                    <div class="audio-section-title">Native Pronunciation</div>
                    <div class="audio-section-sub">Spanish, Hindi & English voice tuning</div>
                  </div>
                </div>
                <button type="button" class="btn-audio-test" id="btn-test-voice" title="Test voice speech">
                  <span>Preview 🔊</span>
                </button>
              </div>

              <div class="audio-sliders-grid">
                <div class="audio-slider-group">
                  <div class="audio-slider-label">
                    <span>Speech Volume</span>
                    <span class="val-badge" id="badge-voice-vol">100%</span>
                  </div>
                  <input type="range" class="settings-slider" id="slider-voice-vol" min="0" max="100" value="100" />
                </div>

                <div class="audio-slider-group">
                  <div class="audio-slider-label">
                    <span>Speech Speed</span>
                    <span class="val-badge" id="badge-voice-rate">0.80×</span>
                  </div>
                  <input type="range" class="settings-slider" id="slider-voice-rate" min="50" max="130" value="80" />
                </div>

                <div class="audio-slider-group">
                  <div class="audio-slider-label">
                    <span>Speech Pitch</span>
                    <span class="val-badge" id="badge-voice-pitch">1.0×</span>
                  </div>
                  <input type="range" class="settings-slider" id="slider-voice-pitch" min="50" max="150" value="100" />
                </div>
              </div>
            </div>

            <!-- 3. Card Sound Effects -->
            <div class="audio-card">
              <div class="audio-card-header">
                <div class="audio-card-title-group">
                  <span class="audio-icon-badge">🎚️</span>
                  <div>
                    <div class="audio-section-title">Card Flip Sound</div>
                    <div class="audio-section-sub">Physical card whoosh & micro-snap</div>
                  </div>
                </div>
                <button type="button" class="btn-audio-test" id="btn-test-sfx" title="Audition sound">
                  <span>Audition ⚡</span>
                </button>
              </div>
              <div class="audio-mode-selector">
                <button type="button" class="audio-chip-btn active" data-sfx="snap">Crisp Snap</button>
                <button type="button" class="audio-chip-btn" data-sfx="whoosh">Soft Whoosh</button>
                <button type="button" class="audio-chip-btn" data-sfx="mute">Silent</button>
              </div>
            </div>
          </div>
        </div>

        <!-- Fast Card Jump -->
        <div>
          <div class="drawer-section-heading">Fast Jump</div>
          <div class="settings-card-section">
            <div class="range-slider-wrapper">
              <div class="slider-bubble" id="slider-val-indicator">#800</div>
              <input type="range" class="jump-slider" id="jump-slider" min="800" max="1000" value="800" />
            </div>
          </div>
        </div>

        <!-- Offline & Data Tools -->
        <div>
          <div class="drawer-section-heading">Offline & Tools</div>
          <button type="button" class="btn-download-html" id="btn-download-html-menu" style="width: 100%; justify-content: center;">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
              <polyline points="7 10 12 15 17 10"/>
              <line x1="12" y1="15" x2="12" y2="3"/>
            </svg>
            <span>Download Standalone Offline HTML</span>
          </button>
        </div>
      </div>
    </aside>

    <!-- ========================================================== -->
    <!-- ADD SECTION MODAL                                          -->
    <!-- ========================================================== -->
    <div class="modal-backdrop" id="modal-add-section">
      <div class="modal-sheet">
        <div class="modal-handle"></div>
        <div class="modal-header">
          <div class="edit-modal-title-group">
            <span class="modal-title">Create New Section</span>
            <span class="edit-badge">Custom</span>
          </div>
          <button class="modal-close-btn" id="btn-close-add-section" aria-label="Close">&times;</button>
        </div>

        <form id="form-add-section" class="edit-form-content" onsubmit="return false;">
          <div class="edit-form-field">
            <label class="edit-label" for="input-new-section-title">Section Name</label>
            <input type="text" class="edit-input" id="input-new-section-title" placeholder="e.g. Medical & Healthcare" required />
          </div>

          <div class="edit-form-field">
            <label class="edit-label" for="input-new-section-sub">Category / Description</label>
            <input type="text" class="edit-input" id="input-new-section-sub" placeholder="e.g. Doctors, symptoms, hospital vocabulary" />
          </div>

          <div class="edit-form-row">
            <div class="edit-form-field">
              <label class="edit-label" for="input-new-section-count">Target Cards Goal</label>
              <input type="number" class="edit-input" id="input-new-section-count" value="150" min="10" max="5000" />
            </div>
            <div class="edit-form-field">
              <label class="edit-label" for="input-new-section-icon">Icon Emoji</label>
              <input type="text" class="edit-input" id="input-new-section-icon" value="📚" maxlength="4" />
            </div>
          </div>

          <div class="edit-btn-group" style="margin-top: 10px;">
            <button type="button" class="btn-edit-reset" id="btn-cancel-add-section">Cancel</button>
            <button type="button" class="btn-edit-save" id="btn-save-new-section">Create Section</button>
          </div>
        </form>
      </div>
    </div>

    <!-- ========================================================== -->
    <!-- EDIT SECTION MODAL                                         -->
    <!-- ========================================================== -->
    <div class="modal-backdrop" id="modal-edit-section">
      <div class="modal-sheet">
        <div class="modal-handle"></div>
        <div class="modal-header">
          <div class="edit-modal-title-group">
            <span class="modal-title">Edit Section</span>
            <span class="edit-badge">Manage</span>
          </div>
          <button class="modal-close-btn" id="btn-close-edit-section" aria-label="Close">&times;</button>
        </div>

        <form id="form-edit-section" class="edit-form-content" onsubmit="return false;">
          <input type="hidden" id="edit-section-id" />
          <div class="edit-form-field">
            <label class="edit-label" for="input-edit-section-title">Section Name</label>
            <input type="text" class="edit-input" id="input-edit-section-title" required />
          </div>

          <div class="edit-form-field">
            <label class="edit-label" for="input-edit-section-sub">Description</label>
            <input type="text" class="edit-input" id="input-edit-section-sub" />
          </div>

          <div class="edit-form-row">
            <div class="edit-form-field">
              <label class="edit-label" for="input-edit-section-count">Card Count</label>
              <input type="number" class="edit-input" id="input-edit-section-count" min="10" max="5000" />
            </div>
            <div class="edit-form-field">
              <label class="edit-label" for="input-edit-section-icon">Icon</label>
              <input type="text" class="edit-input" id="input-edit-section-icon" maxlength="4" />
            </div>
          </div>

          <div class="edit-btn-group" style="margin-top: 10px;">
            <button type="button" class="btn-edit-reset" id="btn-delete-section" style="color: #f87171; border-color: rgba(248, 113, 113, 0.3);">Delete</button>
            <button type="button" class="btn-edit-save" id="btn-save-edit-section">Save Changes</button>
          </div>
        </form>
      </div>
    </div>
`;

// Insert the modals and drawer right before </body>
html = html.replace('</body>', `${slideOverDrawerAndModalsHtml}\n  </body>`);

fs.writeFileSync('index.html', html, 'utf8');
console.log('Successfully updated HTML structure for Home, Subsections, and Menu Drawer!');
