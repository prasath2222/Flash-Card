const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

const sIdx = html.indexOf('<script>');
const script = html.slice(sIdx + '<script>'.length, html.lastIndexOf('</script>'));

const marker = '// ENHANCED KINETIC FORCE-SWIPE & BULLETPROOF DOUBLE-TAP';
const mIdx = html.indexOf(marker);

if (mIdx !== -1) {
  const slice = html.slice(mIdx, mIdx + 400);
  console.log('Context:\n', slice);

  const cleaned = slice
    .replace('let touchStartX = 0;', 'touchStartX = 0;')
    .replace('let touchStartY = 0;', 'touchStartY = 0;')
    .replace('let lastTapTime = 0;', 'lastTapTime = 0;')
    .replace('let lastTapX = 0;', 'lastTapX = 0;')
    .replace('let lastTapY = 0;', 'lastTapY = 0;')
    .replace('let isHorizontalSwipe = false;', 'isHorizontalSwipe = false;');

  html = html.slice(0, mIdx) + cleaned + html.slice(mIdx + 400);
  fs.writeFileSync('index.html', html, 'utf8');
  console.log('Cleaned up duplicate declarations successfully!');
}
