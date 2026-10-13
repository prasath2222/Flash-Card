const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');
console.log('Read index.html for event wiring, length:', html.length);

// 1. Update updateGlobalLearnedDisplays to also update desktop and mobile headers
const oldUpdateDisplays = `function updateGlobalLearnedDisplays() {`;
const newUpdateDisplays = `function updateGlobalLearnedDisplays() {
        const totalLearned = learnedCardsSet.size;
        const totalWords = 3000;
        const totalPct = Math.min(100, ((totalLearned / totalWords) * 100)).toFixed(1);

        // Update Desktop and Mobile top headers
        const desktopStatusEl = document.getElementById("desktop-status-count");
        if (desktopStatusEl) desktopStatusEl.textContent = totalLearned.toLocaleString();

        const mobileStatusEl = document.getElementById("mobile-status-count");
        if (mobileStatusEl) mobileStatusEl.textContent = totalLearned.toLocaleString();`;

if (html.includes(oldUpdateDisplays)) {
  html = html.replace(oldUpdateDisplays, newUpdateDisplays);
  console.log('Updated updateGlobalLearnedDisplays with desktop and mobile headers!');
}

// 2. Enhance switchScreen to update sidebar and mobile tabs active state
const oldSwitchScreen = `function switchScreen(screenId) {
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
      }`;

const newSwitchScreen = `function switchScreen(screenId) {
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

        // Update Sidebar active tabs
        document.querySelectorAll(".sidebar-nav-btn").forEach(btn => btn.classList.remove("active"));
        document.querySelectorAll(".mobile-tab-btn").forEach(btn => btn.classList.remove("active"));

        const breadcrumbEl = document.getElementById("desktop-breadcrumb-text");

        if (screenId === "screen-home") {
          const btn = document.getElementById("nav-btn-home");
          if (btn) btn.classList.add("active");
          const mob = document.getElementById("mob-tab-home");
          if (mob) mob.classList.add("active");
          if (breadcrumbEl) breadcrumbEl.textContent = "Dashboard · Choose Your Learning Path";
        } else if (screenId === "screen-subsections") {
          const btn = document.getElementById("nav-btn-subsections");
          if (btn) btn.classList.add("active");
          const mob = document.getElementById("mob-tab-3k");
          if (mob) mob.classList.add("active");
          if (breadcrumbEl) breadcrumbEl.textContent = "3k Vocabulary · Select Subsection Tier";
        } else if (screenId === "screen-flashcard") {
          const btn = document.getElementById("nav-btn-3k");
          if (btn) btn.classList.add("active");
          const mob = document.getElementById("mob-tab-3k");
          if (mob) mob.classList.add("active");
          if (breadcrumbEl) breadcrumbEl.textContent = "Flashcard Session · Cards 800 – 1000";
        }

        window.scrollTo({ top: 0, behavior: "smooth" });
        closeMenuDrawer();
      }`;

if (html.includes(oldSwitchScreen)) {
  html = html.replace(oldSwitchScreen, newSwitchScreen);
  console.log('Enhanced switchScreen with sidebar & mobile tab active states!');
}

// 3. Add sidebar, mobile nav, and sound toggle handlers inside DOMContentLoaded
const sidebarEventWiring = `
        // DESKTOP SIDEBAR NAVIGATION
        const navBtnHome = document.getElementById("nav-btn-home");
        if (navBtnHome) navBtnHome.addEventListener("click", () => switchScreen("screen-home"));

        const navBtn3k = document.getElementById("nav-btn-3k");
        if (navBtn3k) navBtn3k.addEventListener("click", () => switchScreen("screen-subsections"));

        const navBtnSubsections = document.getElementById("nav-btn-subsections");
        if (navBtnSubsections) navBtnSubsections.addEventListener("click", () => switchScreen("screen-subsections"));

        const navBtnSections = document.getElementById("nav-btn-sections");
        if (navBtnSections) {
          navBtnSections.addEventListener("click", () => {
            switchScreen("screen-home");
            setTimeout(() => {
              const secGrid = document.getElementById("sections-grid");
              if (secGrid) secGrid.scrollIntoView({ behavior: "smooth" });
            }, 100);
          });
        }

        const navBtnSettings = document.getElementById("nav-btn-settings");
        if (navBtnSettings) navBtnSettings.addEventListener("click", openMenuDrawer);

        const sidebarBrandHome = document.getElementById("sidebar-brand-home");
        if (sidebarBrandHome) sidebarBrandHome.addEventListener("click", () => switchScreen("screen-home"));

        const btnDesktopOpenSettings = document.getElementById("btn-desktop-open-settings");
        if (btnDesktopOpenSettings) btnDesktopOpenSettings.addEventListener("click", openMenuDrawer);

        // MOBILE TOP & BOTTOM NAVIGATION
        const mobileHamburgerBtn = document.getElementById("mobile-hamburger-btn");
        if (mobileHamburgerBtn) mobileHamburgerBtn.addEventListener("click", openMenuDrawer);

        const mobTabHome = document.getElementById("mob-tab-home");
        if (mobTabHome) mobTabHome.addEventListener("click", () => switchScreen("screen-home"));

        const mobTab3k = document.getElementById("mob-tab-3k");
        if (mobTab3k) mobTab3k.addEventListener("click", () => switchScreen("screen-subsections"));

        const mobTabSections = document.getElementById("mob-tab-sections");
        if (mobTabSections) {
          mobTabSections.addEventListener("click", () => {
            switchScreen("screen-home");
            setTimeout(() => {
              const secGrid = document.getElementById("sections-grid");
              if (secGrid) secGrid.scrollIntoView({ behavior: "smooth" });
            }, 100);
          });
        }

        const mobTabSettings = document.getElementById("mob-tab-settings");
        if (mobTabSettings) mobTabSettings.addEventListener("click", openMenuDrawer);

        // SIDEBAR SOUND QUICK TOGGLE
        const sidebarQuickSound = document.getElementById("sidebar-quick-sound");
        if (sidebarQuickSound) {
          let soundEnabled = true;
          sidebarQuickSound.addEventListener("click", () => {
            soundEnabled = !soundEnabled;
            const ind = document.getElementById("sidebar-sound-indicator");
            if (ind) {
              ind.textContent = soundEnabled ? "ON 🔊" : "MUTED 🔇";
              ind.style.color = soundEnabled ? "#34d399" : "#f87171";
            }
            showToast(soundEnabled ? "Audio Sound FX Enabled" : "Audio Sound FX Muted");
          });
        }
`;

const insertMarker = `updateGlobalLearnedDisplays();\n        const initLastCard = getLastCardNumber();`;
if (html.includes(insertMarker)) {
  html = html.replace(insertMarker, `${sidebarEventWiring}\n        updateGlobalLearnedDisplays();\n        const initLastCard = getLastCardNumber();`);
  console.log('Injected sidebar & mobile navigation event listeners!');
} else {
  console.warn('Could not find insertMarker');
}

fs.writeFileSync('index.html', html, 'utf8');
console.log('Successfully wired all production events into index.html!');
