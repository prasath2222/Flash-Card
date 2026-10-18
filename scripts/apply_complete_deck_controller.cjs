const fs = require('fs');
const path = require('path');

const indexHtmlPath = path.resolve('index.html');
let content = fs.readFileSync(indexHtmlPath, 'utf8');

const tier1CardsJson = fs.readFileSync(path.resolve('scripts/tier_1_100_cards.json'), 'utf8');

const targetPoint = `      /* ==========================================================
         AUTOMATIC SEQUENTIAL REINDEXING & PERSISTENT DELETION SYSTEM
         ========================================================== */`;

const replacementCode = `      /* ==========================================================
         TIER 1 (CARDS 1 – 100) EMBEDDED CURRICULUM
         ========================================================== */
      const tier1DeckCards = ${tier1CardsJson.trim()};
      const tier800DeckCards = initialDeckCards;

      /* ==========================================================
         CUSTOM DECKS CATALOG & MULTI-TIER MANAGEMENT SYSTEM
         ========================================================== */
      let customDecksCatalog = {};
      try {
        customDecksCatalog = JSON.parse(localStorage.getItem("custom_decks_catalog_v1") || "{}");
        if (typeof customDecksCatalog !== "object" || customDecksCatalog === null) customDecksCatalog = {};
      } catch(e) { customDecksCatalog = {}; }

      let currentDeckId = localStorage.getItem("active_deck_id_v1") || "deck-800-1000";

      function getActiveDeckInfo() {
        if (currentDeckId === "deck-1-100") {
          return {
            id: "deck-1-100",
            title: "Cards 1 – 100",
            startNum: 1,
            cards: tier1DeckCards
          };
        }
        if (customDecksCatalog[currentDeckId]) {
          const cd = customDecksCatalog[currentDeckId];
          return {
            id: cd.deckId,
            title: cd.title || "Custom Deck",
            startNum: (cd.cards && cd.cards[0] && cd.cards[0].num) || 1,
            cards: cd.cards || []
          };
        }
        return {
          id: "deck-800-1000",
          title: "Cards 800 – 1000",
          startNum: 800,
          cards: tier800DeckCards
        };
      }

      /* ==========================================================
         AUTOMATIC SEQUENTIAL REINDEXING & PERSISTENT DELETION SYSTEM
         ========================================================== */
      const DELETED_CARDS_STORAGE_KEY = "vocab_deleted_cards_v3";
      let deletedCardNums = [];
      try {
        deletedCardNums = JSON.parse(localStorage.getItem(DELETED_CARDS_STORAGE_KEY) || "[]");
        if (!Array.isArray(deletedCardNums)) deletedCardNums = [];
      } catch(e) {
        deletedCardNums = [];
      }

      let cards = [];
      function reindexAndBuildCards() {
        const deckInfo = getActiveDeckInfo();
        const baseCards = deckInfo.cards || [];
        const startNum = deckInfo.startNum || 1;

        cards = baseCards
          .filter(c => !deletedCardNums.includes(c.num) && !deletedCardNums.includes(c.originalNum))
          .map((c, idx) => ({
            ...c,
            originalNum: c.originalNum || c.num,
            num: startNum + idx,
            displayNum: startNum + idx
          }));

        // Sync Nav Button Badge
        const navDeckLabel = document.getElementById("nav-active-deck-label");
        if (navDeckLabel) {
          navDeckLabel.textContent = \`Deck: \${deckInfo.title}\`;
        }

        // Update Subsections UI Active States
        if (typeof updateSubsectionsUI === "function") {
          updateSubsectionsUI();
        }
      }
      reindexAndBuildCards();

      function switchDeck(deckId, customCards = null, customTitle = "") {
        if (customCards && deckId) {
          customDecksCatalog[deckId] = {
            deckId: deckId,
            title: customTitle || "Custom Deck",
            cardCount: customCards.length,
            cards: customCards,
            updatedAt: new Date().toISOString()
          };
          try {
            localStorage.setItem("custom_decks_catalog_v1", JSON.stringify(customDecksCatalog));
          } catch(e){}

          // Cloud Sync Custom Deck to Firestore
          if (window.firebaseSync && window.firebaseSync.pushCustomDeckToCloud) {
            window.firebaseSync.pushCustomDeckToCloud(customDecksCatalog[deckId]);
          }
        }

        currentDeckId = deckId;
        try {
          localStorage.setItem("active_deck_id_v1", deckId);
        } catch(e){}

        reindexAndBuildCards();
        currentIndex = 0;
        isFlipped = false;
        const cardStageWrapper = document.getElementById("card-stage-wrapper");
        if (cardStageWrapper) cardStageWrapper.classList.remove("flipped");

        if (cards.length > 0) {
          if (counterCurrentEl) counterCurrentEl.textContent = cards[0].displayNum || cards[0].num;
          if (counterTotalEl) counterTotalEl.textContent = cards[cards.length - 1].displayNum || cards[cards.length - 1].num;
        }

        renderCurrentCard(false);
        updateSectionLearnedCounter();
        if (typeof updateSubsectionsUI === "function") updateSubsectionsUI();
        if (typeof renderCustomDecksList === "function") renderCustomDecksList();

        // Push Active Deck preference to Firestore
        if (window.firebaseSync && window.firebaseSync.pushStudyStateToCloud) {
          window.firebaseSync.pushStudyStateToCloud({
            activeDeckId: deckId,
            lastActiveCardNum: cards[0] ? (cards[0].originalNum || cards[0].num) : 1
          });
        }

        const info = getActiveDeckInfo();
        showToast(\`Active Deck: \${info.title} (\${cards.length} cards)\`);
        switchScreen("screen-flashcard");
      }`;

if (!content.includes('tier1DeckCards')) {
  // Replace the original reindexAndBuildCards block
  const oldReindexPattern = /\/\* ==========================================================\s+AUTOMATIC SEQUENTIAL REINDEXING & PERSISTENT DELETION SYSTEM\s+========================================================== \*\/[\s\S]*?reindexAndBuildCards\(\);/;
  content = content.replace(oldReindexPattern, replacementCode);
  console.log('✓ Injected Multi-Tier Deck & Reindex system');
}

// Next, add the UI Controller functions for Deck Uploader, File Parsing, Auto Image Finding, and Subsections Rendering
const targetEndOfScript = `    </script>`;
const controllerLogic = `
      /* ==========================================================
         AUTOMATIC DECK UPLOADER & IMAGE RESOLUTION CONTROLLER
         ========================================================== */
      function updateSubsectionsUI() {
        const pill1 = document.getElementById("pill-tier-1");
        const cardTier1 = document.getElementById("sub-tier-1-100");
        const cardTier800 = document.getElementById("sub-tier-800-1000");

        if (cardTier1) {
          const isTier1 = currentDeckId === "deck-1-100";
          if (pill1) pill1.style.display = isTier1 ? "inline-block" : "none";
          cardTier1.style.borderColor = isTier1 ? "#10b981" : "rgba(16, 185, 129, 0.45)";
          cardTier1.style.boxShadow = isTier1 ? "0 12px 35px rgba(16, 185, 129, 0.35), 0 5px 0 #059669" : "0 10px 28px rgba(16, 185, 129, 0.15), 0 5px 0 #059669";
        }

        if (cardTier800) {
          const isTier800 = currentDeckId === "deck-800-1000";
          cardTier800.style.borderColor = isTier800 ? "#38bdf8" : "rgba(56, 189, 248, 0.45)";
          cardTier800.style.boxShadow = isTier800 ? "0 12px 35px rgba(2, 132, 199, 0.35), 0 5px 0 #0369a1" : "0 10px 30px rgba(2, 132, 199, 0.18), 0 5px 0 #0369a1";
        }

        // Update Tier 1 Learned Count
        let tier1Learned = 0;
        tier1DeckCards.forEach(c => {
          if (learnedCardsSet && (learnedCardsSet.has(c.num) || learnedCardsSet.has(String(c.num)))) tier1Learned++;
        });
        const tier1Stat = document.getElementById("tier-1-stat-line");
        if (tier1Stat) tier1Stat.textContent = \`\${tier1Learned} / \${tier1DeckCards.length} Learned\`;
        const tier1Bar = document.getElementById("tier-1-progress-bar");
        if (tier1Bar) tier1Bar.style.width = \`\${Math.round((tier1Learned / tier1DeckCards.length) * 100)}%\`;

        // Update Active Deck Header Pill
        const navDeckLabel = document.getElementById("nav-active-deck-label");
        if (navDeckLabel) navDeckLabel.textContent = \`Deck: \${getActiveDeckInfo().title}\`;
      }

      function renderCustomDecksList() {
        const grid = document.getElementById("custom-decks-grid");
        const countBadge = document.getElementById("custom-decks-count-badge");
        if (!grid) return;

        const keys = Object.keys(customDecksCatalog);
        if (countBadge) countBadge.textContent = \`\${keys.length} Deck\${keys.length === 1 ? '' : 's'}\`;

        if (keys.length === 0) {
          grid.innerHTML = \`<div style="text-align: center; padding: 20px; background: rgba(255,255,255,0.03); border: 1px dashed rgba(255,255,255,0.12); border-radius: 16px; color: #94a3b8; font-size: 0.86rem;">
            No custom decks uploaded yet. Tap <strong>Upload / Import Deck</strong> above to add your own curriculum!
          </div>\`;
          return;
        }

        grid.innerHTML = "";
        keys.forEach(k => {
          const deck = customDecksCatalog[k];
          const isCurrent = currentDeckId === deck.deckId;
          const cardDiv = document.createElement("div");
          cardDiv.className = "custom-deck-item";
          cardDiv.style.cssText = \`background: rgba(255,255,255,0.05); border: 2px solid \${isCurrent ? '#38bdf8' : 'rgba(255,255,255,0.12)'}; border-radius: 18px; padding: 16px 20px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px; transition: all 0.2s;\`;

          cardDiv.innerHTML = \`
            <div style="display: flex; align-items: center; gap: 12px;">
              <span style="font-size: 1.6rem; width: 44px; height: 44px; border-radius: 12px; background: rgba(56,189,248,0.15); display: flex; align-items: center; justify-content: center;">📑</span>
              <div>
                <div style="display: flex; align-items: center; gap: 8px;">
                  <h4 style="font-size: 1.05rem; font-weight: 800; color: #fff; margin: 0;">\${deck.title}</h4>
                  \${isCurrent ? '<span style="font-size: 0.65rem; font-weight: 800; background: #38bdf8; color: #0f172a; padding: 2px 7px; border-radius: 999px;">ACTIVE</span>' : ''}
                </div>
                <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 2px;">\${deck.cardCount || (deck.cards ? deck.cards.length : 0)} Flashcards · Synced across devices</div>
              </div>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
              <button type="button" class="duo-btn-3d duo-btn-3d-green btn-study-custom-deck" data-deck-id="\${deck.deckId}" style="padding: 9px 18px; font-size: 0.85rem; font-weight: 700;">
                \${isCurrent ? 'Study Now' : 'Switch & Study'}
              </button>
              <button type="button" class="duo-btn-3d btn-delete-custom-deck" data-deck-id="\${deck.deckId}" style="padding: 9px 12px; font-size: 0.85rem; color: #f87171; background: rgba(248,113,113,0.12); border-color: rgba(248,113,113,0.3);" title="Delete deck">
                🗑️
              </button>
            </div>
          \`;
          grid.appendChild(cardDiv);
        });

        // Wire study & delete buttons
        grid.querySelectorAll(".btn-study-custom-deck").forEach(btn => {
          btn.addEventListener("click", () => {
            const id = btn.getAttribute("data-deck-id");
            if (id) switchDeck(id);
          });
        });

        grid.querySelectorAll(".btn-delete-custom-deck").forEach(btn => {
          btn.addEventListener("click", () => {
            const id = btn.getAttribute("data-deck-id");
            if (!id) return;
            if (confirm(\`Delete this deck?\`)) {
              delete customDecksCatalog[id];
              try {
                localStorage.setItem("custom_decks_catalog_v1", JSON.stringify(customDecksCatalog));
              } catch(e){}
              if (window.firebaseSync && window.firebaseSync.deleteCustomDeckFromCloud) {
                window.firebaseSync.deleteCustomDeckFromCloud(id);
              }
              if (currentDeckId === id) {
                switchDeck("deck-800-1000");
              } else {
                renderCustomDecksList();
              }
            }
          });
        });
      }

      // Universal Intelligent Parser for Raw Curriculum, JSON, CSV & Text
      function parseCurriculumText(rawText) {
        if (!rawText || typeof rawText !== "string") return [];
        const trimmed = rawText.trim();

        // 1. JSON Array
        if (trimmed.startsWith("[") && trimmed.endsWith("]")) {
          try {
            const arr = JSON.parse(trimmed);
            if (Array.isArray(arr) && arr.length > 0) {
              return arr.map((item, idx) => ({
                num: item.num || (idx + 1),
                word: String(item.word || item.term || item.english || \`Term \${idx + 1}\`).replace(/^[\uFE0F\s]+/, '').trim(),
                emoji: item.emoji || "📌",
                category: item.category || "Uploaded Deck",
                trans: {
                  es: (item.trans && item.trans.es) || item.es || item.spanish || String(item.word || ""),
                  hi: (item.trans && item.trans.hi) || item.hi || item.hindi || String(item.word || "")
                },
                tamil: item.tamil || item.ta || String(item.word || "")
              }));
            }
          } catch(e) {}
        }

        const lines = rawText.split(/\\r?\\n/).map(l => l.trim()).filter(Boolean);

        // 2. CSV / TSV
        if (lines.length > 1 && (lines[0].includes(",") || lines[0].includes("\\t"))) {
          const delimiter = lines[0].includes("\\t") ? "\\t" : ",";
          const header = lines[0].toLowerCase().split(delimiter).map(h => h.trim().replace(/^["']|["']$/g, ""));
          const wordIdx = header.findIndex(h => h.includes("word") || h.includes("english") || h.includes("term") || h.includes("en"));
          const esIdx = header.findIndex(h => h.includes("spanish") || h.includes("es"));
          const hiIdx = header.findIndex(h => h.includes("hindi") || h.includes("hi"));
          const taIdx = header.findIndex(h => h.includes("tamil") || h.includes("ta"));

          if (wordIdx !== -1) {
            const parsed = [];
            for (let i = 1; i < lines.length; i++) {
              const row = lines[i].split(delimiter).map(c => c.trim().replace(/^["']|["']$/g, ""));
              const word = row[wordIdx];
              if (!word) continue;
              parsed.push({
                num: i,
                word: word.replace(/^[\uFE0F\s]+/, '').trim(),
                emoji: "📌",
                category: "Uploaded CSV",
                trans: {
                  es: esIdx !== -1 && row[esIdx] ? row[esIdx] : word,
                  hi: hiIdx !== -1 && row[hiIdx] ? row[hiIdx] : word
                },
                tamil: taIdx !== -1 && row[taIdx] ? row[taIdx] : word
              });
            }
            if (parsed.length > 0) return parsed;
          }
        }

        // 3. Raw Curriculum Format (e.g., raw_curriculum.txt: "1. 👤 I = yo / main / நான்")
        const parsedCards = [];
        let curCategory = "Custom Deck";
        let autoId = 1;

        for (let i = 0; i < lines.length; i++) {
          const line = lines[i];
          if (line.startsWith("Category ") || line.startsWith("# ")) {
            curCategory = line.replace(/^[#\\s]+/, "").trim();
            continue;
          }

          const numMatch = line.match(/^([0-9]+)\\.\\s*(.*)/);
          if (numMatch) {
            const num = parseInt(numMatch[1], 10);
            const rest = numMatch[2].trim();

            let emoji = "📌";
            let cleanHeader = rest;
            const emojiMatch = rest.match(/^([\uD800-\uDBFF][\uDC00-\uDFFF]|[\u2600-\u27BF]|\uD83C[\uDF00-\uDFFF]|\uD83D[\uDC00-\uDE4F]|\uD83E[\uDD00-\uDDFF]|\u23E9-\u23EC|👤|👨|👩|📦|👥|🙋|🏷️|🎯|🪞)\s*(.*)/);
            if (emojiMatch) {
              emoji = emojiMatch[1];
              cleanHeader = emojiMatch[2];
            }

            let word = cleanHeader;
            let es = "";
            let hi = "";
            let ta = "";

            if (cleanHeader.includes("=")) {
              const parts = cleanHeader.split("=");
              word = parts[0].trim();
              const transParts = parts[1].split("/");
              es = (transParts[0] || "").trim();
              hi = (transParts[1] || "").trim();
              ta = (transParts[2] || "").trim();
            }

            word = word.replace(/^[0-9]+\\.\\s*/, "").replace(/^[\\uFE0F\\s]+/, "").trim();
            if (!word) word = \`Word \${num || autoId}\`;

            parsedCards.push({
              num: num || autoId++,
              word: word,
              emoji: emoji,
              category: curCategory.replace(/\\([0-9–-]+\\)/, "").trim(),
              trans: { es: es || word, hi: hi || word },
              tamil: ta || word
            });
          } else if (line.length > 1 && !line.startsWith("EN:") && !line.startsWith("ES:") && !line.startsWith("HI:") && !line.startsWith("TA:")) {
            parsedCards.push({
              num: autoId++,
              word: line.replace(/^[\\uFE0F\\s]+/, '').trim(),
              emoji: "📌",
              category: curCategory,
              trans: { es: line.trim(), hi: line.trim() },
              tamil: line.trim()
            });
          }
        }

        return parsedCards;
      }

      // Automatic Latest Real-World Photo Discovery via Server & Wikipedia
      async function autoFindMissingImages(cardList, progressCb) {
        const batchSize = 6;
        let done = 0;
        for (let i = 0; i < cardList.length; i += batchSize) {
          const chunk = cardList.slice(i, i + batchSize);
          await Promise.all(chunk.map(async (c) => {
            const lookupId = c.originalNum || c.num;
            if (typeof cardAccurateImages !== "undefined" && cardAccurateImages[lookupId]) {
              done++;
              if (progressCb) progressCb(done, cardList.length);
              return;
            }
            try {
              const res = await fetch(\`/api/find-image?query=\${encodeURIComponent(c.word)}&num=\${lookupId}\`);
              if (res.ok) {
                const data = await res.json();
                if (data && data.imageUrl) {
                  if (typeof cardAccurateImages !== "undefined") {
                    cardAccurateImages[lookupId] = data.imageUrl;
                  }
                  c.imageUrl = data.imageUrl;
                }
              }
            } catch(e) {}
            done++;
            if (progressCb) progressCb(done, cardList.length);
          }));
        }
      }

      // Wire Up Uploader Modal & Events
      function initDeckUploaderSystem() {
        const modal = document.getElementById("modal-upload-deck");
        const btnTopUpload = document.getElementById("btn-top-upload-deck");
        const btnSubUpload = document.getElementById("btn-subsections-upload");
        const btnClose = document.getElementById("btn-close-upload-deck");
        const btnCancel = document.getElementById("btn-cancel-upload-deck");
        const btnPreset1 = document.getElementById("btn-preset-tier-1");
        const btnPreset800 = document.getElementById("btn-preset-tier-800");
        const btnStudyTier1 = document.getElementById("btn-study-tier-1");
        const cardTier1 = document.getElementById("sub-tier-1-100");
        const cardTier800 = document.getElementById("sub-tier-800-1000");

        const dropzone = document.getElementById("deck-dropzone");
        const fileInput = document.getElementById("deck-file-input");
        const pasteInput = document.getElementById("deck-paste-input");
        const titleInput = document.getElementById("deck-title-input");
        const btnLoadDeck = document.getElementById("btn-parse-and-load-deck");
        const statusBox = document.getElementById("upload-status-box");
        const statusText = document.getElementById("upload-status-text");
        const progressFill = document.getElementById("upload-progress-fill");

        function openModal() {
          if (modal) {
            modal.classList.add("open");
            if (statusBox) statusBox.style.display = "none";
          }
        }
        function closeModal() {
          if (modal) modal.classList.remove("open");
        }

        if (btnTopUpload) btnTopUpload.addEventListener("click", openModal);
        if (btnSubUpload) btnSubUpload.addEventListener("click", openModal);
        if (btnClose) btnClose.addEventListener("click", closeModal);
        if (btnCancel) btnCancel.addEventListener("click", closeModal);

        // Preset 1: Cards 1 - 100
        if (btnPreset1) {
          btnPreset1.addEventListener("click", () => {
            closeModal();
            switchDeck("deck-1-100");
          });
        }
        if (btnStudyTier1) {
          btnStudyTier1.addEventListener("click", (e) => {
            e.stopPropagation();
            switchDeck("deck-1-100");
          });
        }
        if (cardTier1) {
          cardTier1.addEventListener("click", (e) => {
            if (e.target.closest("button")) return;
            switchDeck("deck-1-100");
          });
        }

        // Preset 9: Cards 800 - 1000
        if (btnPreset800) {
          btnPreset800.addEventListener("click", () => {
            closeModal();
            switchDeck("deck-800-1000");
          });
        }
        if (cardTier800) {
          cardTier800.addEventListener("click", (e) => {
            if (e.target.closest("button")) return;
            switchDeck("deck-800-1000");
          });
        }

        // File dropzone click
        if (dropzone && fileInput) {
          dropzone.addEventListener("click", () => fileInput.click());

          dropzone.addEventListener("dragover", (e) => {
            e.preventDefault();
            dropzone.style.borderColor = "#38bdf8";
            dropzone.style.background = "rgba(56, 189, 248, 0.15)";
          });

          dropzone.addEventListener("dragleave", () => {
            dropzone.style.borderColor = "rgba(56, 189, 248, 0.4)";
            dropzone.style.background = "rgba(2, 132, 199, 0.06)";
          });

          dropzone.addEventListener("drop", (e) => {
            e.preventDefault();
            dropzone.style.borderColor = "rgba(56, 189, 248, 0.4)";
            dropzone.style.background = "rgba(2, 132, 199, 0.06)";
            if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
              handleFile(e.dataTransfer.files[0]);
            }
          });

          fileInput.addEventListener("change", () => {
            if (fileInput.files && fileInput.files.length > 0) {
              handleFile(fileInput.files[0]);
            }
          });
        }

        function handleFile(file) {
          if (!file) return;
          if (titleInput && !titleInput.value) {
            titleInput.value = file.name.replace(/\\.[^/.]+$/, "");
          }
          const reader = new FileReader();
          reader.onload = (e) => {
            if (pasteInput) pasteInput.value = e.target.result;
            showToast(\`File loaded: \${file.name}\`);
          };
          reader.readAsText(file);
        }

        // Parse and Load Deck button
        if (btnLoadDeck) {
          btnLoadDeck.addEventListener("click", async () => {
            const rawText = pasteInput ? pasteInput.value.trim() : "";
            if (!rawText) {
              showToast("Please choose a file or paste curriculum text first.");
              return;
            }

            if (statusBox) statusBox.style.display = "block";
            if (statusText) statusText.textContent = "Parsing curriculum flashcards...";
            if (progressFill) progressFill.style.width = "20%";

            const parsedCards = parseCurriculumText(rawText);
            if (!parsedCards || parsedCards.length === 0) {
              if (statusText) statusText.textContent = "Could not parse any cards. Check formatting.";
              return;
            }

            const deckTitle = (titleInput && titleInput.value.trim()) || \`Uploaded Deck (\${parsedCards.length} cards)\`;

            const autoFindChk = document.getElementById("chk-auto-find-images");
            const shouldFindImages = autoFindChk ? autoFindChk.checked : true;

            if (shouldFindImages) {
              if (statusText) statusText.textContent = \`Auto-finding verified authentic photos for \${parsedCards.length} cards...\`;
              await autoFindMissingImages(parsedCards, (done, total) => {
                const pct = Math.round((done / total) * 100);
                if (progressFill) progressFill.style.width = \`\${Math.max(20, pct)}%\`;
                if (statusText) statusText.textContent = \`Finding verified photos... \${done} / \${total} loaded (\${pct}%)\`;
              });
            }

            if (progressFill) progressFill.style.width = "100%";
            if (statusText) statusText.textContent = "Done! Activating deck...";

            setTimeout(() => {
              const deckId = \`deck-custom-\${Date.now()}\`;
              switchDeck(deckId, parsedCards, deckTitle);
              closeModal();
            }, 300);
          });
        }

        // Initialize display state
        updateSubsectionsUI();
        renderCustomDecksList();

        // Listen for Firestore remote decks
        if (window.firebaseSync && window.firebaseSync.onRemoteDecksChange) {
          window.firebaseSync.onRemoteDecksChange((remoteDecks) => {
            if (remoteDecks) {
              Object.assign(customDecksCatalog, remoteDecks);
              try {
                localStorage.setItem("custom_decks_catalog_v1", JSON.stringify(customDecksCatalog));
              } catch(e){}
              renderCustomDecksList();
            }
          });
        }
      }

      if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initDeckUploaderSystem);
      } else {
        initDeckUploaderSystem();
      }
`;

if (!content.includes('initDeckUploaderSystem')) {
  content = content.replace(targetEndOfScript, controllerLogic + '\n    </script>');
  console.log('✓ Injected Automatic Deck Uploader & Image Resolution controller');
}

fs.writeFileSync(indexHtmlPath, content, 'utf8');
console.log('All deck system controller code applied successfully.');
