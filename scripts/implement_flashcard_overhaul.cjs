const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

// =========================================================================
// 1. UPDATE FLASHCARD HEADER MARKUP:
// Replace "Kitchen & Cooking" pill with "Learned: 0 / 200" badge
// And add the Duolingo 3D "Delete Card" button next to shuffle
// =========================================================================
const oldPill = `<span class="top-category-pill" id="current-category" style="padding: 6px 14px; font-weight: 700; font-size: 0.84rem; border-radius: 9999px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12);">Kitchen & Cooking</span>`;
const newPill = `<span class="top-category-pill learned-tier-badge" id="current-category" style="padding: 6px 14px; font-weight: 750; font-size: 0.84rem; border-radius: 9999px; background: rgba(16, 185, 129, 0.16); border: 1.5px solid rgba(16, 185, 129, 0.35); color: #34d399; display: inline-flex; align-items: center; gap: 4px;"><span>Learned:</span> <strong id="section-learned-count">0</strong> / <span id="section-total-count">200</span></span>`;

if (html.includes(oldPill)) {
  html = html.replace(oldPill, newPill);
  console.log('Replaced current-category with Learned: 0 / 200 badge!');
} else {
  // Regex fallback
  html = html.replace(/<span class="top-category-pill"[^>]*id="current-category"[^>]*>[\s\S]*?<\/span>/, newPill);
  console.log('Replaced current-category with regex!');
}

// Add Delete Card button in top-nav-actions
if (!html.includes('id="btn-delete-card"')) {
  const shuffleBtnMarker = '<button class="shuffle-btn duo-btn-3d" id="btn-shuffle"';
  const deleteBtnHtml = `<button type="button" class="delete-card-btn duo-btn-3d" id="btn-delete-card" title="Delete this flashcard" aria-label="Delete Flashcard" style="width: 38px; height: 38px; border-radius: 12px; display: flex; align-items: center; justify-content: center; background: rgba(239, 68, 68, 0.14); border: 1.5px solid rgba(239, 68, 68, 0.35); box-shadow: 0 3px 0 rgba(185, 28, 28, 0.5); color: #f87171; cursor: pointer; transition: all 0.15s ease;">
                <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="3 6 5 6 21 6"/>
                  <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                  <line x1="10" y1="11" x2="10" y2="17"/>
                  <line x1="14" y1="11" x2="14" y2="17"/>
                </svg>
              </button>
              `;
  html = html.replace(shuffleBtnMarker, deleteBtnHtml + shuffleBtnMarker);
  console.log('Added btn-delete-card to top-nav-actions!');
}

// Add Delete Card styles in CSS before </style>
const deleteCardCss = `
      /* Duolingo 3D Delete Card Button */
      .delete-card-btn {
        width: 38px !important;
        height: 38px !important;
        border-radius: 12px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        background: rgba(239, 68, 68, 0.14) !important;
        border: 1.5px solid rgba(239, 68, 68, 0.35) !important;
        box-shadow: 0 3px 0 rgba(185, 28, 28, 0.5) !important;
        color: #f87171 !important;
        cursor: pointer !important;
        transition: all 0.14s ease !important;
        padding: 0 !important;
      }
      .delete-card-btn:hover {
        background: rgba(239, 68, 68, 0.25) !important;
        border-color: rgba(239, 68, 68, 0.6) !important;
        color: #fca5a5 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 0 rgba(185, 28, 28, 0.6) !important;
      }
      .delete-card-btn:active {
        transform: translateY(2px) !important;
        box-shadow: 0 1px 0 rgba(185, 28, 28, 0.5) !important;
      }
      .learned-tier-badge {
        transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
      }
`;

const styleClose = html.indexOf('</style>');
html = html.slice(0, styleClose) + deleteCardCss + html.slice(styleClose);
console.log('Added delete-card-btn CSS styles!');

fs.writeFileSync('index.html', html, 'utf8');
console.log('Updated index.html markup successfully!');
