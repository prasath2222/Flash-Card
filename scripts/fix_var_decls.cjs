const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

html = html.replace(
`      var isSwiping = false;
      isDragging = false;
      touchStartX = 0;
      touchStartY = 0;
      var touchStartTime = 0;
      var velocitySamples = [];
      var lastTapTime = 0;
      var lastTapX = 0;
      var lastTapY = 0;
      var suppressSyntheticClickUntil = 0;
      var isCardAnimating = false;`,
`      isSwiping = false;
      isDragging = false;
      touchStartX = 0;
      touchStartY = 0;
      touchStartTime = 0;
      velocitySamples = [];
      lastTapTime = 0;
      lastTapX = 0;
      lastTapY = 0;
      suppressSyntheticClickUntil = 0;
      isCardAnimating = false;`
);

fs.writeFileSync('index.html', html, 'utf8');
console.log('Cleaned variable declarations.');
