const fs = require('fs');

// Read the current index.html
const html = fs.readFileSync('index.html', 'utf8');

// Restore to clean state if duplicated
const head1 = html.indexOf('<head>');
const head2 = html.indexOf('<head>', 100);

let cleanHtml = html;
if (head2 !== -1) {
  cleanHtml = html.slice(0, head1) + html.slice(head2);
  console.log('Restored cleanHtml from duplicated state. Length:', cleanHtml.length);
}

// Locate the Learned Cards & Resume system block
const trackerMarker = `      /* ==========================================================
         COMPREHENSIVE LEARNED TRACKER & STATUS 1 TO 3K SYSTEM
         ========================================================== */`;

const resumeMarkerEnd = `      function resumeStudyDeck() {
        const targetNum = getLastCardNumber();
        const foundIdx = cards.findIndex(c => c.num === targetNum);
        if (foundIdx !== -1) {
          currentIndex = foundIdx;
        } else {
          currentIndex = 0;
        }
        isFlipped = false;
        switchScreen("screen-flashcard");
        renderCurrentCard();
        showToast(\`Resumed at Card #\${cards[currentIndex].num}: \${cards[currentIndex].word}\`);
      }`;

const trackerIdx = cleanHtml.indexOf(trackerMarker);
const resumeEndIdx = cleanHtml.indexOf(resumeMarkerEnd);

if (trackerIdx === -1 || resumeEndIdx === -1) {
  console.error('Could not find markers:', trackerIdx, resumeEndIdx);
  process.exit(1);
}

const blockToMove = cleanHtml.slice(trackerIdx, resumeEndIdx + resumeMarkerEnd.length);
console.log('Found blockToMove, length:', blockToMove.length);

// Remove block from current position
const htmlWithoutBlock = cleanHtml.slice(0, trackerIdx) + cleanHtml.slice(resumeEndIdx + resumeMarkerEnd.length);

// Find insertion point: Right after `let isShuffled = false;` in Application State
const insertTarget = '      let isShuffled = false;\n';
const insertPos = htmlWithoutBlock.indexOf(insertTarget);

if (insertPos === -1) {
  console.error('Could not find insertTarget!');
  process.exit(1);
}

const finalHtml = htmlWithoutBlock.slice(0, insertPos + insertTarget.length) +
  '\n' + blockToMove + '\n' +
  htmlWithoutBlock.slice(insertPos + insertTarget.length);

console.log('finalHtml length:', finalHtml.length);

// Validate script syntax
const scriptMatch = finalHtml.match(/<script[\s\S]*?<\/script>/g);
if (!scriptMatch || scriptMatch.length !== 1) {
  console.error('Unexpected script tags count:', scriptMatch ? scriptMatch.length : 0);
  process.exit(1);
}

const scriptCode = scriptMatch[0].replace(/^<script[^>]*>/, '').replace(/<\/script>$/, '');
try {
  new Function(scriptCode);
  console.log('Syntax check: PASSED');
} catch (e) {
  console.error('Syntax check failed:', e.message);
  process.exit(1);
}

// Validate runtime in mock DOM environment
function makeEl() {
  return {
    textContent: '',
    innerHTML: '',
    style: {},
    dataset: {},
    classList: { add: () => {}, remove: () => {}, contains: () => false },
    addEventListener: () => {},
    setAttribute: () => {},
    appendChild: () => {},
    querySelector: () => null,
    querySelectorAll: () => [],
    focus: () => {}
  };
}

const window = {
  addEventListener: () => {},
  Image: class Image {
    constructor() {
      this.onload = null;
      this.onerror = null;
      this.src = '';
    }
  },
  speechSynthesis: { getVoices: () => [], speak: () => {}, cancel: () => {} },
  AudioContext: class {
    constructor() { this.currentTime = 0; }
    createOscillator() { return { type: '', frequency: { setValueAtTime: () => {} }, connect: () => {}, start: () => {}, stop: () => {} }; }
    createGain() { return { gain: { setValueAtTime: () => {}, linearRampToValueAtTime: () => {}, exponentialRampToValueAtTime: () => {} }, connect: () => {} }; }
  }
};
global.Image = window.Image;
const document = {
  getElementById: (id) => makeEl(),
  querySelectorAll: () => [],
  createElement: () => makeEl(),
  addEventListener: () => {}
};
const localStorage = {
  getItem: () => null,
  setItem: () => {}
};

try {
  const fn = new Function('window', 'document', 'localStorage', scriptCode);
  fn(window, document, localStorage);
  console.log('Runtime mock DOM execution: PASSED (No ReferenceErrors or TDZ issues!)');
} catch (e) {
  console.error('Runtime execution FAILED:', e.name, e.message);
  console.error(e.stack);
  process.exit(1);
}

// Write the fixed index.html
fs.writeFileSync('index.html', finalHtml, 'utf8');
console.log('Successfully wrote pristine and fixed index.html!');
