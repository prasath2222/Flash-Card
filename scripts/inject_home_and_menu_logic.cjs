const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

const homeLogicCode = `
      /* ==========================================================
         SCREEN NAVIGATION & RESPONSIVE LAYOUT CONTROLLER
         ========================================================== */
      function switchScreen(screenId) {
        document.querySelectorAll(".app-screen").forEach((s) => s.classList.remove("active-screen"));
        const target = document.getElementById(screenId);
        if (target) {
          target.classList.add("active-screen");
          if (screenId === "screen-home") {
            document.body.classList.add("home-view-active");
          } else {
            document.body.classList.remove("home-view-active");
          }
        }
        closeMenuDrawer();
      }

      // Breadcrumb / Screen Back Buttons
      const btnBreadcrumbBack = document.getElementById("btn-breadcrumb-back");
      if (btnBreadcrumbBack) {
        btnBreadcrumbBack.addEventListener("click", () => switchScreen("screen-home"));
      }

      const btnBackToHome = document.getElementById("btn-back-to-home");
      if (btnBackToHome) {
        btnBackToHome.addEventListener("click", () => switchScreen("screen-home"));
      }

      const btnLaunch3kDeck = document.getElementById("btn-launch-3k-deck");
      if (btnLaunch3kDeck) {
        btnLaunch3kDeck.addEventListener("click", (e) => {
          e.stopPropagation();
          switchScreen("screen-flashcard");
        });
      }

      const btnOpenSubsections = document.getElementById("btn-open-subsections");
      if (btnOpenSubsections) {
        btnOpenSubsections.addEventListener("click", (e) => {
          e.stopPropagation();
          switchScreen("screen-subsections");
        });
      }

      const subTier800_1000 = document.getElementById("sub-tier-800-1000");
      if (subTier800_1000) {
        subTier800_1000.addEventListener("click", () => switchScreen("screen-flashcard"));
      }

      /* ==========================================================
         3D INTERACTIVE TILT PHYSICS FOR 3K VOCABULARY CARD
         ========================================================== */
      const card3kFeatured = document.getElementById("card-3k-featured");
      const card3kShine = document.getElementById("card-3k-shine");

      if (card3kFeatured) {
        // Direct click on 3K card (outside buttons) opens flashcards
        card3kFeatured.addEventListener("click", (e) => {
          if (e.target.closest("button")) return;
          switchScreen("screen-flashcard");
        });

        // 3D Parallax Tilt calculation
        card3kFeatured.addEventListener("mousemove", (e) => {
          const rect = card3kFeatured.getBoundingClientRect();
          const x = e.clientX - rect.left;
          const y = e.clientY - rect.top;
          const centerX = rect.width / 2;
          const centerY = rect.height / 2;

          const rotateX = ((y - centerY) / centerY) * -6.5;
          const rotateY = ((x - centerX) / centerX) * 6.5;

          card3kFeatured.style.transform = \`perspective(1000px) rotateX(\${rotateX.toFixed(2)}deg) rotateY(\${rotateY.toFixed(2)}deg) scale3d(1.015, 1.015, 1.015)\`;
          if (card3kShine) {
            card3kShine.style.background = \`radial-gradient(circle at \${x}px \${y}px, rgba(255, 255, 255, 0.16), transparent 60%)\`;
            card3kShine.style.opacity = "1";
          }
        });

        card3kFeatured.addEventListener("mouseleave", () => {
          card3kFeatured.style.transform = "perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)";
          if (card3kShine) {
            card3kShine.style.opacity = "0.5";
            card3kShine.style.background = "radial-gradient(circle at 50% 30%, rgba(255, 255, 255, 0.12), transparent 70%)";
          }
        });

        // Subtle Touch Tilt for Mobile
        card3kFeatured.addEventListener("touchmove", (e) => {
          if (!e.touches[0]) return;
          const rect = card3kFeatured.getBoundingClientRect();
          const x = e.touches[0].clientX - rect.left;
          const y = e.touches[0].clientY - rect.top;
          const centerX = rect.width / 2;
          const centerY = rect.height / 2;

          const rotateX = ((y - centerY) / centerY) * -4;
          const rotateY = ((x - centerX) / centerX) * 4;
          card3kFeatured.style.transform = \`perspective(1000px) rotateX(\${rotateX.toFixed(2)}deg) rotateY(\${rotateY.toFixed(2)}deg)\`;
        }, { passive: true });

        card3kFeatured.addEventListener("touchend", () => {
          card3kFeatured.style.transform = "perspective(1000px) rotateX(0deg) rotateY(0deg)";
        });
      }

      /* ==========================================================
         DYNAMIC SECTIONS MANAGER (Add, Edit, Drag and Move)
         ========================================================== */
      const SECTIONS_STORAGE_KEY = "vocab_custom_sections_data_v1";

      const defaultSections = [
        {
          id: "sec_daily",
          title: "Daily Essentials",
          sub: "Conversational & Everyday Idioms",
          count: 350,
          progress: 100,
          color: "#10b981",
          icon: "🗣️"
        },
        {
          id: "sec_travel",
          title: "Travel & Airport",
          sub: "Transit, Flights, Hotel & City Signs",
          count: 180,
          progress: 45,
          color: "#38bdf8",
          icon: "✈️"
        },
        {
          id: "sec_food",
          title: "Food & Dining",
          sub: "Restaurants, Kitchenware & Recipes",
          count: 240,
          progress: 60,
          color: "#f59e0b",
          icon: "🍳"
        },
        {
          id: "sec_career",
          title: "Workplace & Career",
          sub: "Office, Meetings & Technology",
          count: 190,
          progress: 25,
          color: "#818cf8",
          icon: "💼"
        }
      ];

      function loadCustomSections() {
        try {
          const raw = localStorage.getItem(SECTIONS_STORAGE_KEY);
          if (raw) return JSON.parse(raw);
        } catch (e) {
          console.error("Could not load custom sections:", e);
        }
        return defaultSections;
      }

      let currentSections = loadCustomSections();

      function saveCustomSections(sections) {
        currentSections = sections;
        try {
          localStorage.setItem(SECTIONS_STORAGE_KEY, JSON.stringify(sections));
        } catch (e) {
          console.error("Could not save sections:", e);
        }
        renderCustomSections();
      }

      const sectionsGridEl = document.getElementById("sections-grid");
      const sectionsCountPillEl = document.getElementById("sections-count-pill");

      // Drag and Drop State
      let draggedSectionId = null;

      function renderCustomSections() {
        if (!sectionsGridEl) return;
        sectionsGridEl.innerHTML = "";

        if (sectionsCountPillEl) {
          sectionsCountPillEl.textContent = \`\${currentSections.length} Decks\`;
        }

        currentSections.forEach((sec, index) => {
          const card = document.createElement("div");
          card.className = "custom-section-card";
          card.id = \`sec-card-\${sec.id}\`;
          card.setAttribute("draggable", "true");
          card.dataset.id = sec.id;
          card.dataset.index = index;

          card.innerHTML = \`
            <div class="section-card-top-bar">
              <div style="display: flex; align-items: center; gap: 8px;">
                <div class="section-drag-handle" title="Drag to reorder" aria-label="Drag to reorder">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="9" cy="5" r="1.5"/><circle cx="15" cy="5" r="1.5"/>
                    <circle cx="9" cy="12" r="1.5"/><circle cx="15" cy="12" r="1.5"/>
                    <circle cx="9" cy="19" r="1.5"/><circle cx="15" cy="19" r="1.5"/>
                  </svg>
                </div>
                <div class="section-icon-badge" style="background: \${sec.color}18; border-color: \${sec.color}35;">
                  \${sec.icon || "📚"}
                </div>
              </div>
              <div class="section-card-actions">
                <div class="reorder-btns-group">
                  <button type="button" class="btn-reorder-arrow btn-move-up" title="Move Up" \${index === 0 ? "disabled style='opacity:0.25;'" : ""}>
                    ▲
                  </button>
                  <button type="button" class="btn-reorder-arrow btn-move-down" title="Move Down" \${index === currentSections.length - 1 ? "disabled style='opacity:0.25;'" : ""}>
                    ▼
                  </button>
                </div>
                <button type="button" class="section-tool-btn btn-edit-section" title="Edit Section" aria-label="Edit Section">
                  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 20h9"/>
                    <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/>
                  </svg>
                </button>
              </div>
            </div>

            <div class="section-main-meta">
              <div class="section-title-text">\${sec.title}</div>
              <div class="section-subtitle-text">\${sec.sub || "Custom vocabulary deck"}</div>
            </div>

            <div class="section-card-bottom">
              <div class="section-bottom-stats">
                <span>Progress: \${sec.progress}%</span>
                <span style="color: \${sec.color}; font-weight:700;">\${sec.count} Words</span>
              </div>
              <div class="section-card-progress">
                <div class="section-card-progress-fill" style="width: \${sec.progress}%; background: \${sec.color};"></div>
              </div>
            </div>
          \`;

          // Card Click: Launches Flashcard deck with Toast
          card.addEventListener("click", (e) => {
            if (e.target.closest("button") || e.target.closest(".section-drag-handle")) return;
            switchScreen("screen-flashcard");
            showToast(\`Studying: \${sec.title}\`);
          });

          // Move Up / Move Down buttons
          const btnMoveUp = card.querySelector(".btn-move-up");
          if (btnMoveUp) {
            btnMoveUp.addEventListener("click", (e) => {
              e.stopPropagation();
              if (index > 0) {
                const updated = [...currentSections];
                [updated[index - 1], updated[index]] = [updated[index], updated[index - 1]];
                saveCustomSections(updated);
                showToast(\`Moved "\${sec.title}" up\`);
              }
            });
          }

          const btnMoveDown = card.querySelector(".btn-move-down");
          if (btnMoveDown) {
            btnMoveDown.addEventListener("click", (e) => {
              e.stopPropagation();
              if (index < currentSections.length - 1) {
                const updated = [...currentSections];
                [updated[index], updated[index + 1]] = [updated[index + 1], updated[index]];
                saveCustomSections(updated);
                showToast(\`Moved "\${sec.title}" down\`);
              }
            });
          }

          // Edit Section Button
          const btnEditSec = card.querySelector(".btn-edit-section");
          if (btnEditSec) {
            btnEditSec.addEventListener("click", (e) => {
              e.stopPropagation();
              openEditSectionModal(sec);
            });
          }

          // HTML5 Drag and Drop Handlers
          card.addEventListener("dragstart", (e) => {
            draggedSectionId = sec.id;
            card.classList.add("dragging");
            e.dataTransfer.effectAllowed = "move";
            e.dataTransfer.setData("text/plain", sec.id);
          });

          card.addEventListener("dragover", (e) => {
            e.preventDefault();
            e.dataTransfer.dropEffect = "move";
            card.classList.add("drag-over");
          });

          card.addEventListener("dragleave", () => {
            card.classList.remove("drag-over");
          });

          card.addEventListener("drop", (e) => {
            e.preventDefault();
            card.classList.remove("drag-over");
            const srcId = e.dataTransfer.getData("text/plain") || draggedSectionId;
            const targetId = sec.id;
            if (srcId && targetId && srcId !== targetId) {
              const fromIdx = currentSections.findIndex((s) => s.id === srcId);
              const toIdx = currentSections.findIndex((s) => s.id === targetId);
              if (fromIdx !== -1 && toIdx !== -1) {
                const reordered = [...currentSections];
                const [movedItem] = reordered.splice(fromIdx, 1);
                reordered.splice(toIdx, 0, movedItem);
                saveCustomSections(reordered);
                showToast("Section order updated");
                playHapticTick(540, "sine", 0.04);
              }
            }
          });

          card.addEventListener("dragend", () => {
            card.classList.remove("dragging", "drag-over");
            draggedSectionId = null;
          });

          sectionsGridEl.appendChild(card);
        });
      }

      // Initial Render
      renderCustomSections();

      /* ==========================================================
         ADD & EDIT SECTION MODALS
         ========================================================== */
      const modalAddSection = document.getElementById("modal-add-section");
      const btnOpenAddSection = document.getElementById("btn-open-add-section");
      const btnCloseAddSection = document.getElementById("btn-close-add-section");
      const btnCancelAddSection = document.getElementById("btn-cancel-add-section");
      const btnSaveNewSection = document.getElementById("btn-save-new-section");

      const inputNewSecTitle = document.getElementById("input-new-section-title");
      const inputNewSecSub = document.getElementById("input-new-section-sub");
      const inputNewSecCount = document.getElementById("input-new-section-count");
      const inputNewSecIcon = document.getElementById("input-new-section-icon");

      function openAddSectionModal() {
        if (!modalAddSection) return;
        modalAddSection.classList.add("open");
        if (inputNewSecTitle) {
          inputNewSecTitle.value = "";
          inputNewSecTitle.focus();
        }
        if (inputNewSecSub) inputNewSecSub.value = "";
      }

      function closeAddSectionModal() {
        if (modalAddSection) modalAddSection.classList.remove("open");
      }

      if (btnOpenAddSection) btnOpenAddSection.addEventListener("click", openAddSectionModal);
      if (btnCloseAddSection) btnCloseAddSection.addEventListener("click", closeAddSectionModal);
      if (btnCancelAddSection) btnCancelAddSection.addEventListener("click", closeAddSectionModal);

      if (btnSaveNewSection) {
        btnSaveNewSection.addEventListener("click", () => {
          const title = (inputNewSecTitle?.value || "").trim();
          if (!title) {
            showToast("Please enter a section name");
            return;
          }
          const sub = (inputNewSecSub?.value || "").trim() || "Custom vocabulary set";
          const count = parseInt(inputNewSecCount?.value || "100", 10) || 100;
          const icon = (inputNewSecIcon?.value || "📚").trim() || "📚";
          const colors = ["#38bdf8", "#10b981", "#f59e0b", "#818cf8", "#f43f5e", "#ec4899"];
          const randomColor = colors[currentSections.length % colors.length];

          const newSec = {
            id: \`sec_\${Date.now()}\`,
            title,
            sub,
            count,
            progress: 0,
            color: randomColor,
            icon
          };

          saveCustomSections([...currentSections, newSec]);
          closeAddSectionModal();
          showToast(\`Created "\${title}" section!\`);
          playHapticTick(650, "triangle", 0.06);
        });
      }

      // Edit Section Modal Handlers
      const modalEditSection = document.getElementById("modal-edit-section");
      const btnCloseEditSection = document.getElementById("btn-close-edit-section");
      const btnSaveEditSection = document.getElementById("btn-save-edit-section");
      const btnDeleteSection = document.getElementById("btn-delete-section");

      const editSecId = document.getElementById("edit-section-id");
      const inputEditSecTitle = document.getElementById("input-edit-section-title");
      const inputEditSecSub = document.getElementById("input-edit-section-sub");
      const inputEditSecCount = document.getElementById("input-edit-section-count");
      const inputEditSecIcon = document.getElementById("input-edit-section-icon");

      function openEditSectionModal(sec) {
        if (!modalEditSection) return;
        editSecId.value = sec.id;
        inputEditSecTitle.value = sec.title;
        inputEditSecSub.value = sec.sub || "";
        inputEditSecCount.value = sec.count || 100;
        inputEditSecIcon.value = sec.icon || "📚";
        modalEditSection.classList.add("open");
        inputEditSecTitle.focus();
      }

      function closeEditSectionModal() {
        if (modalEditSection) modalEditSection.classList.remove("open");
      }

      if (btnCloseEditSection) btnCloseEditSection.addEventListener("click", closeEditSectionModal);

      if (btnSaveEditSection) {
        btnSaveEditSection.addEventListener("click", () => {
          const id = editSecId.value;
          const updatedTitle = inputEditSecTitle.value.trim();
          if (!updatedTitle) return;

          const updated = currentSections.map((s) => {
            if (s.id === id) {
              return {
                ...s,
                title: updatedTitle,
                sub: inputEditSecSub.value.trim(),
                count: parseInt(inputEditSecCount.value, 10) || s.count,
                icon: inputEditSecIcon.value.trim() || s.icon
              };
            }
            return s;
          });

          saveCustomSections(updated);
          closeEditSectionModal();
          showToast("Section updated!");
        });
      }

      if (btnDeleteSection) {
        btnDeleteSection.addEventListener("click", () => {
          const id = editSecId.value;
          const filtered = currentSections.filter((s) => s.id !== id);
          saveCustomSections(filtered);
          closeEditSectionModal();
          showToast("Section deleted");
        });
      }

      /* ==========================================================
         SLIDE-OVER MENU DRAWER CONTROLLER (Settings in Menu)
         ========================================================== */
      const appMenuDrawer = document.getElementById("app-menu-drawer");
      const menuDrawerBackdrop = document.getElementById("menu-drawer-backdrop");
      const drawerCloseBtn = document.getElementById("drawer-close-btn");
      const btnHomeMenu = document.getElementById("btn-home-menu");
      const btnFlashcardMenu = document.getElementById("btn-flashcard-menu");

      function openMenuDrawer() {
        if (appMenuDrawer) appMenuDrawer.classList.add("open");
        if (menuDrawerBackdrop) menuDrawerBackdrop.classList.add("open");
        playHapticTick(480, "sine", 0.04);
      }

      function closeMenuDrawer() {
        if (appMenuDrawer) appMenuDrawer.classList.remove("open");
        if (menuDrawerBackdrop) menuDrawerBackdrop.classList.remove("open");
      }

      if (btnHomeMenu) btnHomeMenu.addEventListener("click", openMenuDrawer);
      if (btnFlashcardMenu) btnFlashcardMenu.addEventListener("click", openMenuDrawer);
      if (drawerCloseBtn) drawerCloseBtn.addEventListener("click", closeMenuDrawer);
      if (menuDrawerBackdrop) menuDrawerBackdrop.addEventListener("click", closeMenuDrawer);

      // Drawer Navigation Links
      const menuNavHome = document.getElementById("menu-nav-home");
      if (menuNavHome) {
        menuNavHome.addEventListener("click", () => switchScreen("screen-home"));
      }

      const menuNav3k = document.getElementById("menu-nav-3k");
      if (menuNav3k) {
        menuNav3k.addEventListener("click", () => switchScreen("screen-flashcard"));
      }

      const menuNavSubsections = document.getElementById("menu-nav-subsections");
      if (menuNavSubsections) {
        menuNavSubsections.addEventListener("click", () => switchScreen("screen-subsections"));
      }

      // Offline HTML Download Button inside Menu
      const btnDownloadHtmlMenu = document.getElementById("btn-download-html-menu");
      if (btnDownloadHtmlMenu) {
        btnDownloadHtmlMenu.addEventListener("click", downloadOfflineHtml);
      }
`;

// Insert home logic before the initialize app section
html = html.replace('// Initialize App', `${homeLogicCode}\n\n      // Initialize App`);

// Set default screen on load: Ensure screen-home is active
html = html.replace('document.body.classList.add("home-view-active");', 'document.body.classList.add("home-view-active");');

fs.writeFileSync('index.html', html, 'utf8');
console.log('Successfully injected home and menu logic into index.html!');
