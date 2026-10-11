const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

// 1. Read shortcuts data
const shortcutsData = JSON.parse(fs.readFileSync('scripts/shortcuts_data.json', 'utf8'));

// 2. Verified replacements for cardPhotos
const photoUpdates = {
  803: 'photo-1590381105924-c72589b9ef3f', // TAP
  806: 'photo-1574672280600-4accfa5b6f98', // TABLECLOTH (checked tablecloth on dining table)
  816: 'photo-1600585154526-990dced4db0d', // HALLWAY
  818: 'photo-1600585154340-be6161a56a0c', // CEILING
  819: 'photo-1518780664697-55e3ad937233', // ROOF
  822: 'photo-1509644851169-2acc08aa25b5', // DOOR
  824: 'photo-1516455590571-18256e5bb9ff', // STAIRS
  828: 'photo-1582268611958-ebfd161ef9cf', // BALCONY
  829: 'photo-1534447677768-be436bb09401', // TERRACE
  833: 'photo-1549488344-1f9b8d2bd1f3', // GATE
  835: 'photo-1541123437800-1bb1317badc2', // CHIMNEY
  851: 'photo-1584905066893-7d5c142ba4e1', // WARDROBE
  868: 'photo-1527515545081-5db817172677', // BROOM
  869: 'photo-1580256081112-e49377338b7f', // MOP
  870: 'photo-1563245372-f21724e3856d', // BUCKET
  882: 'photo-1585647347483-22b66260dfff', // RAZOR
  885: 'photo-1530587191325-3db32d826c18', // NAIL
  886: 'photo-1586864387789-628af9feed72', // SCREW
  887: 'photo-1572981779307-38b8cabb2407', // SCREWDRIVER
  918: 'photo-1584441405886-bc91be61e56a', // BUTTON
  920: 'photo-1596755094514-f87e34085b2c', // SLEEVE
  921: 'photo-1598033129183-c4f50c736f10', // COLLAR
};

// Replace photo IDs in cardPhotos
for (const [num, photoId] of Object.entries(photoUpdates)) {
  const regex = new RegExp(`(${num}:\\s*")[^"]+(")`);
  html = html.replace(regex, `$1${photoId}$2`);
}

console.log('Updated photo replacements in HTML');

// 3. Insert cardShortcuts dictionary right after cardAnims
const shortcutsCode = `
      // Pure Visual & Phonetic Memory Shortcuts (800 - 1000)
      // Instant recall punchlines relating to Indian / Tamil / English contexts
      const cardShortcuts = ${JSON.stringify(shortcutsData, null, 8)};
`;

if (!html.includes('const cardShortcuts =')) {
  html = html.replace('const cardAnims = {', shortcutsCode + '\n      const cardAnims = {');
  console.log('Inserted cardShortcuts into HTML');
}

fs.writeFileSync('index.html', html);
console.log('Step 1 applied successfully');
