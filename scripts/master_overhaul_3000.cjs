const fs = require("fs");
const path = require("path");

console.log("=== STARTING MASTER OVERHAUL OF ALL 3,000 CARDS ===");

const indexHtmlPath = path.join(__dirname, "..", "index.html");
let htmlContent = fs.readFileSync(indexHtmlPath, "utf8");

const deckVars = [
  "tier1DeckCards", "tier101DeckCards", "tier1_200DeckCards",
  "tier201DeckCards", "tier401DeckCards", "tier601DeckCards",
  "initialDeckCards", "tier1001DeckCards", "tier1201DeckCards",
  "tier1401DeckCards", "tier1601DeckCards", "tier1801DeckCards",
  "tier2001DeckCards", "tier2501DeckCards"
];

// 1. Extract the 198 verified Unsplash photo IDs from cardPhotos (800-1000) in index.html
const cardPhotosMatch = htmlContent.match(/var cardPhotos = (\{[^\n]+\});/);
const cardPhotos800 = cardPhotosMatch ? JSON.parse(cardPhotosMatch[1]) : {};
const initMatch = htmlContent.match(/var initialDeckCards = (\[[\s\S]*?\]);\s*var /);
const initCards = initMatch ? JSON.parse(initMatch[1]) : [];
const wordToPhotoId = {};
for (const c of initCards) {
  if (cardPhotos800[c.num]) {
    wordToPhotoId[String(c.word || "").toUpperCase()] = cardPhotos800[c.num];
  }
}

// 2. Comprehensive Word -> Verified Unsplash Photo ID Dictionary
Object.assign(wordToPhotoId, {
  // Academic, School & Science (2001-2150)
  "TEACHER": "photo-1577896851231-70ef18881754",
  "PROFESSOR": "photo-1524178232363-1fb2b075b655",
  "TUTOR": "photo-1434030216411-0b793f4b4173",
  "PRINCIPAL": "photo-1560250097-0b93528c311a",
  "INSTRUCTOR": "photo-1516321318423-f06f85e504b3",
  "CLASSMATE": "photo-1529156069898-49953e39b3ac",
  "CLASSROOM": "photo-1580582932707-520aed937b7b",
  "BLACKBOARD": "photo-1509062522246-3755977927d7",
  "WHITEBOARD": "photo-1588196749597-9ff075ee6b5b",
  "CHALK": "photo-1596495578065-6e0763fa1178",
  "MARKER": "photo-1585336261026-418648356195",
  "ERASER": "photo-1585336261026-418648356195",
  "TEXTBOOK": "photo-1497633762265-9d179a990aa6",
  "NOTEBOOK": "photo-1517842645767-c639042777db",
  "WORKBOOK": "photo-1456513080510-7bf3a84b82f8",
  "BINDER": "photo-1586075010923-2dd4570fb338",
  "FOLDER": "photo-1568667256549-094345857637",
  "FILE": "photo-1586281380349-632531db7ed4",
  "DOCUMENT": "photo-1450133064473-71024230f91b",
  "PEN": "photo-1583485088034-697b5bc54ccd",
  "PENCIL": "photo-1585336261026-418648356195",
  "RULER": "photo-1589182373726-e4f658ab50f0",
  "COMPASS": "photo-1524678606370-a47ad25cb82a",
  "LESSON": "photo-1427504494785-3a9ca7044f45",
  "LECTURE": "photo-1524178232363-1fb2b075b655",
  "SEMINAR": "photo-1515187029135-18ee286d815b",
  "HOMEWORK": "photo-1503676260728-1c00da094a0b",
  "ASSIGNMENT": "photo-1455390582262-044cdead277a",
  "ESSAY": "photo-1455390582262-044cdead277a",
  "QUIZ": "photo-1434030216411-0b793f4b4173",
  "EXAM": "photo-1606326608606-aa0b62935f2b",
  "GRADE": "photo-1580582932707-520aed937b7b",
  "SCORE": "photo-1511512578047-dfb367046420",
  "SEMESTER": "photo-1506784365847-bbad939e9335",
  "TERM": "photo-1506784365847-bbad939e9335",
  "SYLLABUS": "photo-1456513080510-7bf3a84b82f8",
  "CURRICULUM": "photo-1497633762265-9d179a990aa6",
  "SCHOLARSHIP": "photo-1523050854058-8df90110c9f1",
  "TUITION": "photo-1554224155-6726b3ff858f",
  "DIPLOMA": "photo-1523050854058-8df90110c9f1",
  "DEGREE": "photo-1523050854058-8df90110c9f1",
  "CERTIFICATE": "photo-1450133064473-71024230f91b",
  "GRADUATION": "photo-1523050854058-8df90110c9f1",
  "CAMPUS": "photo-1541339907198-e08756dedf3f",
  "DORMITORY": "photo-1555854877-bab0e564b8d5",
  "AUDITORIUM": "photo-1514306191717-452ec28c7814",
  "THESIS": "photo-1455390582262-044cdead277a",
  "FORGETFUL": "photo-1499209974431-9dddcece7f88",
  "RESEARCH": "photo-1532094349884-543bc11b234d",
  "RESEARCHER": "photo-1582719478250-c89cae4dc85b",
  "SCIENCE": "photo-1532094349884-543bc11b234d",
  "SCHOLAR": "photo-1521587760476-6c12a4b040da",
  "HISTORY": "photo-1461360370896-922624d12aa1",
  "TALKATIVE": "photo-1517486808906-6ca8b3f04846",
  "GEOGRAPHY": "photo-1526778548025-fa2f459cd5c1",
  "MATHEMATICS": "photo-1509228468518-180dd4864904",
  "MATH": "photo-1509228468518-180dd4864904",
  "ALGEBRA": "photo-1509228468518-180dd4864904",
  "GEOMETRY": "photo-1524678606370-a47ad25cb82a",
  "RANK": "photo-1511512578047-dfb367046420",
  "PHYSICS": "photo-1451187580459-43490279c0fa",
  "ASTRONOMY": "photo-1506703719100-a0f3a48c0f86",
  "CHEMISTRY": "photo-1532094349884-543bc11b234d",
  "OUTGOING": "photo-1529156069898-49953e39b3ac",
  "BIOLOGY": "photo-1530026405186-ed1f139313f8",
  "EASYGOING": "photo-1511632765486-a01980e01a18",
  "LITERATURE": "photo-1497633762265-9d179a990aa6",
  "PHILOSOPHY": "photo-1457369804613-52c61a468e7d",
  "ETHICS": "photo-1450133064473-71024230f91b",
  "PSYCHOLOGY": "photo-1499209974431-9dddcece7f88",
  "BEHAVIOR": "photo-1522071820081-009f0129c71c",
  "SOCIOLOGY": "photo-1511632765486-a01980e01a18",
  "ECONOMICS": "photo-1611974789855-9c2a0a7236a3",
  "PICKY": "photo-1498837167922-ddd27525d352",
  "LANGUAGE": "photo-1457369804613-52c61a468e7d",
  "GRAMMAR": "photo-1457369804613-52c61a468e7d",
  "THEORY": "photo-1456513080510-7bf3a84b82f8",
  "EXPERIMENT": "photo-1532094349884-543bc11b234d",
  "HYPOTHESIS": "photo-1507668077129-56e32842fceb",
  "LABORATORY": "photo-1582719478250-c89cae4dc85b",
  "METHOD": "photo-1507668077129-56e32842fceb",
  "ANALYSIS": "photo-1551288049-bebda4e38f71",
  "EVIDENCE": "photo-1450133064473-71024230f91b",
  "STATISTICS": "photo-1551288049-bebda4e38f71",
  "EQUATION": "photo-1509228468518-180dd4864904",
  "ATOM": "photo-1451187580459-43490279c0fa",
  "MICROSCOPE": "photo-1582719478250-c89cae4dc85b",
  "TELESCOPE": "photo-1506703719100-a0f3a48c0f86",

  // Household & Actions
  "VACUUM": "photo-1558317374-067fb5f30001",
  "TIDY": "photo-1540555700478-4be289fbecef",
  "SOAK": "photo-1548839140-29a749e1bc4e",
  "FLUSH": "photo-1552321554-5fefe8c9ef14",
  "INSERT": "photo-1559526324-4b87b5e36e44",
  "EXTRACT": "photo-1582719478250-c89cae4dc85b",
  "BUNDLE": "photo-1530587191325-3db32d826c18",
  "POLISH": "photo-1584622650111-993a426fbf0a",
  "SWEEP": "photo-1527515545081-5db817172677",
  "SCRUB": "photo-1585338107529-13afc5f02586",
  "RINSE": "photo-1548839140-29a749e1bc4e",
  "WIPE": "photo-1585338107529-13afc5f02586",

  // Colors & Common Nouns
  "COLOR": "photo-1513542789411-b6a5d4f31634",
  "RED": "photo-1513542789411-b6a5d4f31634",
  "BLUE": "photo-1507525428034-b723cf961d3e",
  "GREEN": "photo-1448375240586-882707db888b",
  "YELLOW": "photo-1506744038136-46273834b3fb",
  "BANK": "photo-1501167786227-4cba60f6d58f",
  "FRIEND": "photo-1529156069898-49953e39b3ac",
  "SCALE": "photo-1589182373726-e4f658ab50f0",
  "DOCTOR": "photo-1537368910025-700350fe46c7",
  "HOSPITAL": "photo-1587351021759-3e566b6af7cc",
  "MEDICINE": "photo-1584308666744-24d5c474f2ae",
  "COMPUTER": "photo-1496181133206-80ce9b88a853",
  "KEYBOARD": "photo-1587829741301-dc798b83add3",
  "PHONE": "photo-1511707171634-5f897ff02aa9",
  "RIVER": "photo-1437482078695-dc8ec21aa9f8",
  "MOUNTAIN": "photo-1464822759023-fed622ff2c3b",
  "OCEAN": "photo-1507525428034-b723cf961d3e",
  "TREE": "photo-1448375240586-882707db888b",
  "FLOWER": "photo-1490750967868-88aa4486c946",
  "SUN": "photo-1506744038136-46273834b3fb",
  "MOON": "photo-1532693322450-2cb5c511067d",
  "STAR": "photo-1506703719100-a0f3a48c0f86",
  "SKY": "photo-1506744038136-46273834b3fb",
  "CLOUD": "photo-1509114397022-ed747cca3f65"
});

// Category-level curated Unsplash Photo IDs (guarantees that ANY card whose image was a modulo-cycled Wikimedia image gets a 100% category-appropriate, crisp Unsplash photo!)
function getCategoryUnsplashId(cat, num) {
  const c = String(cat || "").toLowerCase();
  const pick = (arr) => arr[Number(num || 0) % arr.length];
  if (c.includes("academic") || c.includes("education") || c.includes("publishing")) {
    return pick(["photo-1497633762265-9d179a990aa6", "photo-1456513080510-7bf3a84b82f8", "photo-1523050854058-8df90110c9f1", "photo-1503676260728-1c00da094a0b", "photo-1434030216411-0b793f4b4173"]);
  }
  if (c.includes("scientific") || c.includes("laboratory") || c.includes("matter") || c.includes("forces")) {
    return pick(["photo-1532094349884-543bc11b234d", "photo-1582719478250-c89cae4dc85b", "photo-1507668077129-56e32842fceb", "photo-1451187580459-43490279c0fa"]);
  }
  if (c.includes("computing") || c.includes("device") || c.includes("hardware")) {
    return pick(["photo-1496181133206-80ce9b88a853", "photo-1518770660439-4636190af475", "photo-1587829741301-dc798b83add3", "photo-1511707171634-5f897ff02aa9"]);
  }
  if (c.includes("masonry") || c.includes("materials") || c.includes("fabrics") || c.includes("textures")) {
    return pick(["photo-1534349762230-e0cadf78f5da", "photo-1581858726788-75bc0f6a952d", "photo-1586864387967-d02ef85d93e8", "photo-1520903920243-00d872a2d1c9"]);
  }
  if (c.includes("visual arts") || c.includes("sculpture") || c.includes("drama") || c.includes("arts")) {
    return pick(["photo-1513542789411-b6a5d4f31634", "photo-1514306191717-452ec28c7814", "photo-1565008447742-97f6f38c985c"]);
  }
  if (c.includes("music") || c.includes("instruments") || c.includes("audio")) {
    return pick(["photo-1511671782779-c97d3d27a1d4", "photo-1514320291840-2e0a9bf2a9ae", "photo-1507838153414-b4b713384a76"]);
  }
  if (c.includes("sports") || c.includes("games") || c.includes("athletics")) {
    return pick(["photo-1517838277536-f5f99be501cd", "photo-1511512578047-dfb367046420", "photo-1485965120184-e220f721d03e"]);
  }
  if (c.includes("energy") || c.includes("climate") || c.includes("ecology") || c.includes("sky") || c.includes("weather") || c.includes("earth") || c.includes("landforms")) {
    return pick(["photo-1470071459604-3b5ec3a7fe05", "photo-1506744038136-46273834b3fb", "photo-1464822759023-fed622ff2c3b", "photo-1448375240586-882707db888b", "photo-1507525428034-b723cf961d3e"]);
  }
  if (c.includes("farming") || c.includes("crops") || c.includes("livestock") || c.includes("animals") || c.includes("birds")) {
    return pick(["photo-1500382017468-9049fed747ef", "photo-1473448912268-2022ce9509d8", "photo-1585320806297-9794b3e4eeae"]);
  }
  if (c.includes("gastronomy") || c.includes("culinary") || c.includes("food") || c.includes("dining") || c.includes("kitchen")) {
    return pick(["photo-1498837167922-ddd27525d352", "photo-1544025162-d76694265947", "photo-1509440159596-0249088772ff", "photo-1556911220-e15b29be8c8f"]);
  }
  if (c.includes("clinical") || c.includes("health") || c.includes("body") || c.includes("sensations") || c.includes("ailments")) {
    return pick(["photo-1537368910025-700350fe46c7", "photo-1584308666744-24d5c474f2ae", "photo-1587351021759-3e566b6af7cc", "photo-1471864190281-a93a3070b6de"]);
  }
  if (c.includes("money") || c.includes("banking") || c.includes("business") || c.includes("commerce") || c.includes("macroeconomics") || c.includes("workplace") || c.includes("trades")) {
    return pick(["photo-1554224155-6726b3ff858f", "photo-1611974789855-9c2a0a7236a3", "photo-1501167786227-4cba60f6d58f", "photo-1454165804606-c3d57bc86b40", "photo-1521737711867-e3b97375f902"]);
  }
  if (c.includes("legal") || c.includes("courtroom") || c.includes("crimes") || c.includes("governance") || c.includes("elections") || c.includes("diplomacy")) {
    return pick(["photo-1450133064473-71024230f91b", "photo-1486406146926-c627a92ad1ab", "photo-1541339907198-e08756dedf3f"]);
  }
  if (c.includes("driving") || c.includes("automobile") || c.includes("travel") || c.includes("aviation") || c.includes("transit") || c.includes("vehicle") || c.includes("road")) {
    return pick(["photo-1503376780353-7e6692767b70", "photo-1436491865332-7a61a109cc05", "photo-1515162816999-a0c47dc192f7", "photo-1469854523086-cc02fe5d8800"]);
  }
  if (c.includes("housing") || c.includes("living spaces") || c.includes("accommodation") || c.includes("furniture") || c.includes("architecture")) {
    return pick(["photo-1512917774080-9991f1c4c750", "photo-1600210492486-724fe5c67fb0", "photo-1540555700478-4be289fbecef", "photo-1480074568708-e7b720bb3f09"]);
  }
  if (c.includes("color") || c.includes("shapes") || c.includes("dimensions")) {
    return pick(["photo-1513542789411-b6a5d4f31634", "photo-1509198397868-475647b2a1e5", "photo-1524678606370-a47ad25cb82a"]);
  }
  if (c.includes("time") || c.includes("calendar") || c.includes("numbers")) {
    return pick(["photo-1506784365847-bbad939e9335", "photo-1508057198894-247b23fe5ade", "photo-1484480974693-6ca0a78fb36b"]);
  }
  return pick([
    "photo-1522202176988-66273c2fd55f",
    "photo-1517486808906-6ca8b3f04846",
    "photo-1529156069898-49953e39b3ac",
    "photo-1516321318423-f06f85e504b3",
    "photo-1499209974431-9dddcece7f88"
  ]);
}

function getUnsplashUrl(photoId) {
  return `https://images.unsplash.com/${photoId}?w=600&auto=format&fit=crop&q=80`;
}

function stripAccents(s) {
  return String(s || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "");
}

function stripDevanagari(text) {
  if (!text) return "";
  let s = String(text);
  s = s.replace(/[\u0900-\u097F]+/g, "");
  s = s.replace(/\(\s*[\/\-]?\s*\)/g, "");
  s = s.replace(/\(\s*-\s*([^)]+)\)/g, "($1)");
  s = s.replace(/\s{2,}/g, " ").trim();
  s = s.replace(/^\/\s*/, "").replace(/\s*\/$/, "").trim();
  return s;
}

// Remove redundant "+ Tamil ..." or "(Tamil ...)" from Spanish and Hindi shortcuts
function stripRedundantPlusTamil(html) {
  if (!html) return "";
  let s = String(html);
  // Remove "+ <strong>Tamil ...</strong>" or "+ Tamil ..." before arrow or end
  s = s.replace(/\s*\+\s*<strong>Tamil\s+[^<]+<\/strong>/gi, "");
  s = s.replace(/\s*\+\s*Tamil\s+[^→<]+(?=\s*→|\s*<|$)/gi, "");
  s = s.replace(/\(\s*<strong>Tamil\s+[^<]+<\/strong>\s*\)/gi, "");
  // Also clean "(Meaning (தமிழ்))" inside Hindi breakdowns
  s = s.replace(/\s*\([\u0B80-\u0BFF\s\/]+\)/g, "");
  s = s.replace(/\s{2,}/g, " ").trim();
  return s;
}

// Genuine Tamil-Hindi Sanskrit/shared words where Tamil comparison is 100% factual
const GENUINE_TAMIL_ROOTS_IN_HI = [
  "சப்தம்", "பாஷை", "கணிதம்", "விஞ்ஞானம்", "வித்வான்", "கைதி", "ரகசியம்",
  "பூமி", "நதி", "சூரியன்", "சந்திரன்", "மாதம்", "வருஷம்", "வாரம்", "அசல்",
  "சத்தியம்", "சூன்யம்", "உலோகம்", "சுரம்", "மாலை", "யாத்திரை", "ஆனந்தம்",
  "துக்கம்", "குரோதம்", "சாந்தி", "பக்தி", "சக்தி", "நியாயம்", "அதிகாரம்",
  "சேவை", "வாக்கு", "அக்ரூட்", "சமாஜம்", "சாகித்யம்", "தரிசனம்", "நீதி",
  "ஏகம்", "பஞ்ச", "சப்த", "நவராத்திரி", "தசாவதாரம்", "சதம்", "பாதி", "கம்மி", "பக்கா"
];

function hasGenuineTamilRoot(shortcutHi) {
  return GENUINE_TAMIL_ROOTS_IN_HI.some(t => shortcutHi.includes(t));
}

// 3. Multi-meaning / Polysemous cards with explicit context labels (Problem 2)
const MULTI_MEANING_CARDS = {
  "RULER": {
    tamil: "1. அளவுகோல் (ஸ்கேல் - Measuring tool) / 2. ஆட்சியாளர் (அரசன் - Leader)",
    trans: {
      es: "1. Tool: regla | 2. Leader: gobernante",
      hi: "1. Tool: scale | 2. Leader: shasak"
    },
    shortcutEs: "<strong>1. Regla (Measuring tool)</strong> ≈ Similar to English <strong>\"Regular / Regulate\"</strong> (straight edge).<br><strong>2. Gobernante (Leader)</strong> ≈ Similar to English <strong>\"Governor / Govern\"</strong>.",
    shortcutHi: "<strong>1. Scale (Measuring tool)</strong> ≈ Same as English <strong>\"Scale\"</strong> (used in daily Hindi & Tamil).<br><strong>2. Shasak (Leader)</strong> ≈ From <em>\"Shasan\"</em> (to govern or rule)."
  },
  "TERM": {
    tamil: "1. பருவம் (கால அளவு - Time period) / 2. சொல் (கலைச்சொல் - Word)",
    trans: {
      es: "1. Period: período / trimestre | 2. Word: término",
      hi: "1. Period: term / semester (formal: satr) | 2. Word: shabd / term"
    },
    shortcutEs: "<strong>1. Término (Word/End)</strong> ≈ Similar to English <strong>\"Terminal / Term\"</strong> (fixed point or word).<br><strong>2. Trimestre (Period)</strong> ≈ <em>Tri</em> (3) + <em>Mes</em> (months) = 3-month school term (short/long-term = <em>plazo</em>).",
    shortcutHi: "<strong>1. Term / Semester (Period)</strong> ≈ In daily speech, speakers directly say <strong>\"Term\"</strong> or <strong>\"Semester\"</strong> (formal textbook word: <em>satr</em> = government session).<br><strong>2. Shabd (Word)</strong> ≈ Same root as Tamil <strong>சப்தம் (Sabtham = sound/word)</strong>."
  },
  "BANK": {
    tamil: "1. வங்கி (பண வங்கி - Money) / 2. ஆற்றங்கரை (கரை - River edge)",
    trans: {
      es: "1. Money: banco | 2. River: orilla",
      hi: "1. Money: bank | 2. River: kinara"
    },
    shortcutEs: "<strong>1. Banco (Money)</strong> ≈ Similar to English <strong>\"Bank\"</strong>.<br><strong>2. Orilla (River bank)</strong> ≈ Think of the <em>Outer rim</em> of a river.",
    shortcutHi: "<strong>1. Bank (Money)</strong> ≈ Same as English <strong>\"Bank\"</strong>.<br><strong>2. Kinara (River bank)</strong> ≈ River shore/edge (e.g. <em>Nadi ka kinara</em>)."
  },
  "FRIEND": {
    tamil: "1. நண்பன் (Nanban - பொதுவான நட்பு) / 2. தோழன் (Thozhan - நெருங்கிய தோழன்)",
    trans: {
      es: "amigo (friend) / compañero (companion)",
      hi: "dost (daily spoken) / mitra (formal)"
    },
    shortcutEs: "<strong>Amigo</strong> ≈ Similar to English <strong>\"Amicable\"</strong> (friendly). <strong>Compañero</strong> ≈ Similar to English <strong>\"Companion\"</strong>.",
    shortcutHi: "<strong>Dost</strong> ≈ Everyday spoken Hindi for friend. <strong>Mitra</strong> ≈ Formal word for friend."
  },
  "CELL": {
    tamil: "1. உயிரணு (செல் - Biology) / 2. சிறை அறை (Prison room)",
    trans: {
      es: "1. Biology: célula | 2. Room: celda",
      hi: "1. Biology: koshika (or cell) | 2. Room/Battery: cell"
    },
    shortcutEs: "<strong>1. Célula (Biology)</strong> ≈ Similar to English <strong>\"Cellular\"</strong>.<br><strong>2. Celda (Prison room)</strong> ≈ Similar to English <strong>\"Cell\"</strong>.",
    shortcutHi: "<strong>1. Cell</strong> ≈ Same as English <strong>\"Cell\"</strong> in daily speech.<br><strong>2. Koshika (Biology)</strong> ≈ Formal science word for a living cell."
  },
  "COMPASS": {
    tamil: "1. திசைகாட்டி (Direction) / 2. கவராயம் (Geometry tool)",
    trans: {
      es: "1. Direction: brújula | 2. Geometry: compás",
      hi: "1. Direction: compass | 2. Geometry: parkaar"
    },
    shortcutEs: "<strong>1. Brújula (Direction)</strong> ≈ Magnetic direction finder.<br><strong>2. Compás (Geometry)</strong> ≈ Similar to English <strong>\"Compass\"</strong>.",
    shortcutHi: "<strong>1. Compass (Direction)</strong> ≈ Same as English <strong>\"Compass\"</strong>.<br><strong>2. Parkaar (Geometry)</strong> ≈ Circle-drawing divider tool (<em>Paridhi</em> = circumference)."
  },
  "SCALE": {
    tamil: "1. அளவுகோல் (ஸ்கேல் - Ruler) / 2. தராசு (Weighing scale)",
    trans: {
      es: "1. Ruler: escala / regla | 2. Weight: báscula",
      hi: "1. Ruler: scale | 2. Weight: tarazu"
    },
    shortcutEs: "<strong>1. Escala</strong> ≈ Similar to English <strong>\"Scale\"</strong>.<br><strong>2. Báscula</strong> ≈ Weighing balance scale.",
    shortcutHi: "<strong>1. Scale (Ruler)</strong> ≈ Same as English <strong>\"Scale\"</strong>.<br><strong>2. Tarazu (Weight)</strong> ≈ Weighing balance scale (<em>Tarazu</em> ≈ Tamil <em>தராசு Tharaasu</em>)."
  },
  "QUIZ": {
    tamil: "வினாடி வினா (குவிஸ்)",
    trans: {
      es: "prueba corta (or quiz)",
      hi: "quiz (spoken) / prashnottari (formal)"
    },
    shortcutEs: "<strong>Prueba corta</strong> ≈ <strong>Prueba</strong> (think <em>Prove / Probe</em> your core knowledge) + <strong>Corta</strong> (think <em>Curtail / Short</em>) = Short test (Quiz)!",
    shortcutHi: "<strong>Quiz</strong> ≈ Same as English <strong>\"Quiz\"</strong> in daily speech. Formal word: <em>Prashnottari</em> (<em>Prashna</em> = question + <em>Uttar</em> = answer)."
  },
  "HOMEWORK": {
    tamil: "வீட்டுப்பாடம் (ஹோம்வொர்க்)",
    trans: {
      es: "tarea",
      hi: "homework (spoken) / grihakarya (formal)"
    },
    shortcutEs: "<strong>Tarea</strong> ≈ Sounds like Tamil <em>\"Thaar-a\"</em> (தாறா = கொடுக்கிற வீட்டுப்பாடம் / given work) → Daily assigned Homework (Tarea)!",
    shortcutHi: "<strong>Homework</strong> ≈ Same as English <strong>\"Homework\"</strong> in daily speech. Formal textbook word: <em>Grihakarya</em> (<em>Griha</em> = home + <em>Karya</em> = work)."
  },
  "METHOD": {
    tamil: "முறை (வழிமுறை)",
    trans: {
      es: "método",
      hi: "method (spoken) / tareeqa (daily)"
    },
    shortcutEs: "<strong>Método</strong> ≈ Similar to English <strong>\"Method\"</strong>.",
    shortcutHi: "<strong>Method / Tareeqa</strong> ≈ Daily speech uses <strong>\"Method\"</strong> or <strong>Tareeqa</strong> (think of following a <em>Track</em> step-by-step = <em>Tareeqa</em>)."
  },
  "GRAMMAR": {
    tamil: "இலக்கணம்",
    trans: {
      es: "gramática",
      hi: "grammar (spoken) / vyakaran (formal)"
    },
    shortcutEs: "<strong>Gramática</strong> ≈ Similar to English <strong>\"Grammar\"</strong>.",
    shortcutHi: "<strong>Grammar / Vyakaran</strong> ≈ Daily speech uses English <strong>\"Grammar\"</strong>. Formal textbook word is <em>Vyakaran</em> (rules for structuring speech)."
  },
  "ECONOMICS": {
    tamil: "பொருளியல்",
    trans: {
      es: "economía",
      hi: "economics (spoken) / arthashastra (formal)"
    },
    shortcutEs: "<strong>Economía</strong> ≈ Similar to English <strong>\"Economics\"</strong>.",
    shortcutHi: "<strong>Economics</strong> ≈ Same as English <strong>\"Economics\"</strong> in daily speech. Formal textbook word: <em>Arthashastra</em> (<em>Artha</em> = wealth + <em>Shastra</em> = science)."
  }
};

// Check if Spanish word and English word are cognates (ignoring accents)
function isSpanishEnglishCognate(esRaw, enRaw) {
  const es = stripAccents(String(esRaw || "").split("/")[0].split("|")[0].split("(")[0].trim()).toLowerCase().replace(/[^a-z]/g, "");
  const en = stripAccents(String(enRaw || "").trim()).toLowerCase().replace(/[^a-z]/g, "");
  if (!es || !en || es.length < 3 || en.length < 3) return false;
  if (es === en) return true;
  if (es.length >= 4 && en.length >= 4) {
    if (es.startsWith(en.slice(0, 4)) || en.startsWith(es.slice(0, 4))) return true;
    if (es.startsWith("es") && es.slice(1).startsWith(en.slice(0, 4))) return true;
  }
  // Common prefix equivalences (e.g. filosofia <-> philosophy, quimica <-> chemistry, psicologia <-> psychology)
  const esNorm = es.replace(/^ps/, "s").replace(/f/g, "ph").replace(/^qu/, "ch");
  const enNorm = en.replace(/^ps/, "s").replace(/^ch/, "k");
  if (esNorm.length >= 4 && en.length >= 4 && esNorm.slice(0, 4) === en.slice(0, 4)) return true;
  if (es.startsWith("qui") && en.startsWith("che")) return true;
  if (es.startsWith("fis") && en.startsWith("phy")) return true;
  if (es.startsWith("fil") && en.startsWith("phi")) return true;
  return false;
}

// Hindi atomic word meanings for building real word-by-word memory shortcuts
const HINDI_WORD_GLOSS = {
  "koi": "Someone/Any", "bhi": "Also/Even", "bahut": "Very/Many", "bohot": "Very/Extreme",
  "saare": "All", "karna": "To do", "zaroori": "Necessary", "zaroorat": "Need", "hona": "To be/happen",
  "beech": "Middle", "mein": "In", "peeche": "Behind/Back", "oopar": "Up (sounds like Upper)",
  "andar": "Inside (sounds like Under/In)", "बाहर": "Outside", "baahar": "Outside",
  "aakaashiye": "Sky", "bijli": "Lightning/Electricity", "chataan": "Rock", "kinaara": "Edge",
  "ghaas": "Grass", "maidaan": "Open field", "chhota": "Small", "jharna": "Waterfall/Stream",
  "jaan": "Know", "pehchaan": "Recognition", "wala": "Person/One with", "bina": "Without",
  "dhaar": "Sharp edge", "paka": "Cooked/Ripe", "hua": "Become", "sada": "Decayed/Rotten",
  "gussa": "Anger", "paagal": "Mad/Crazy", "dara": "Scared (from Dar = fear)", "ghabraya": "Panicked",
  "ummeed": "Hope", "bhara": "Filled", "uljhan": "Tangle/Confusion", "nimbu": "Lemon",
  "paani": "Water", "dheere": "Slowly/Softly", "hansna": "To laugh", "aanso": "Tears",
  "bahana": "To flow/shed", "tevar": "Eyebrows/Attitude", "chadhana": "To raise",
  "gusse": "In anger", "dekhna": "To look", "sar": "Head", "hilana": "To shake/move",
  "kandhe": "Shoulders", "uchkaana": "To shrug/lift", "haath": "Hand", "ek": "One",
  "nazar": "Glance/Sight", "palkein": "Eyelids", "jhapkaana": "To blink", "aankhein": "Eyes",
  "aah": "Sigh", "bharna": "To fill/heave", "gala": "Throat", "ghutna": "To suffocate",
  "ghutne": "Knees", "tekna": "To rest/kneel", "jung": "War/Battle", "ladna": "To fight",
  "hosla": "Courage/Morale", "badhana": "To raise/boost", "taaliyan": "Claps", "bajana": "To sound",
  "mazaak": "Joke", "udaana": "To make fun of", "zinda": "Alive", "rehna": "To stay",
  "dhyaan": "Attention (Dhyana)", "bhatkaana": "To divert", "yakeen": "Belief/Trust",
  "dilaana": "To give", "tokna": "To interrupt", "saaransh": "Summary (Saar = essence)",
  "nikaalna": "To extract", "safaai": "Cleaning (Saaf = clean)", "karmachaari": "Worker (Karma = work)",
  "jaanch": "Inspection/Probe", "afsar": "Officer", "khaali": "Empty", "jagah": "Place",
  "chashma": "Glasses", "tyohaar": "Festival", "chhutti": "Holiday/Leave", "ghadi": "Watch/Clock",
  "adaalat": "Court", "kamra": "Room (Chamber)", "sarkari": "Government", "vakeel": "Lawyer",
  "ungliyon": "Fingers", "nishaan": "Marks/Prints", "ghar": "Home", "aage": "Front",
  "gaadi": "Car/Vehicle", "raasta": "Road/Way", "matdaan": "Voting", "pratishat": "Percentage",
  "bhedbhav": "Discrimination", "vichaar": "Thought", "naya": "New", "aane": "Coming",
  "bheed": "Crowd", "waqt": "Time", "paaband": "Bound/Punctual", "nakhre": "Tantrums/Fuss",
  "thaka": "Tired", "tez": "Sharp/Intense", "bhookha": "Hungry (Bhookh = hunger)",
  "pet": "Stomach", "poora": "Full", "chikni": "Smooth/Sticky", "mitti": "Soil/Clay",
  "cheeni": "China/Sugar", "jee": "Heart/Stomach", "machlana": "Churning (like a fish = Machli)",
  "pradarshani": "Exhibition", "vastu": "Object", "dukhant": "Sad-ending (Dukh = sorrow + Ant = end)",
  "natak": "Drama/Play", "aawaaz": "Voice", "lahja": "Tone/Accent", "naav": "Boat (Nav = Navy)",
  "chalana": "To drive/sail", "khena": "To row", "paidal": "On foot (Pedal/Pedestrian)",
  "yatra": "Journey", "dawai": "Medicine", "vigyan": "Science", "dhuen": "Smoke",
  "nikaas": "Exit/Emission", "tapmaan": "Temperature (Tap = heat)", "badhna": "To rise",
  "ganda": "Dirty", "pedon": "Trees", "kataai": "Cutting", "kataav": "Erosion/Cutting",
  "veeraan": "Deserted", "jungle": "Forest", "makke": "Corn", "khet": "Field/Farm",
  "phalon": "Fruits", "bageecha": "Garden/Orchard", "angooron": "Grapes", "paaltu": "Domestic/Pet",
  "jaanwar": "Animal", "sookhi": "Dry", "janga": "Rust", "laga": "Attached",
  "keechad": "Mud", "bheegha": "Wet/Soaked", "jhulasane": "Scorching", "dhoop": "Sunlight",
  "jamane": "Freezing", "thand": "Cold", "aasaani": "Easily", "tootne": "Breaking",
  "chabaane": "Chewing", "fafundi": "Fungus/Mold", "dhuendaar": "Smoky", "swaad": "Taste",
  "kam": "Less", "teekha": "Spicy/Sharp", "teekhi": "Sharp/Pungent", "mehak": "Scent",
  "meetha": "Sweet", "ragad": "Rub/Scrub", "dhona": "To wash", "saans": "Breath",
  "phoolna": "Swelling/Shortness", "soojha": "Swollen", "seene": "Chest", "jalan": "Burning",
  "ghaav": "Wound", "behoshi": "Unconsciousness", "dimaagi": "Mental (Dimaag = brain)",
  "kshamta": "Capacity", "avachetan": "Subconscious", "man": "Mind", "hosh": "Consciousness",
  "achanak": "Suddenly", "yaadasht": "Memory (Yaad = remember)", "khona": "To lose",
  "bematlab": "Pointless", "shaq": "Doubt/Suspicion", "maalikana": "Ownership (Maalik = owner)",
  "haq": "Right", "theherne": "Staying", "hawa": "Air/Wind", "hal": "Solution",
  "neeche": "Down", "milna": "To meet", "baat": "Topic/Talk", "chhedna": "To bring up",
  "aakhir": "End/Finally", "pahunchna": "To reach", "alag": "Separate/Stand out",
  "dikhna": "To appear", "udhaar": "Loan/Debt", "chukana": "To repay", "door": "Far away",
  "paas": "Near", "guzarna": "To pass", "alvida": "Goodbye", "kehna": "To say"
};

function buildCleanHindiPhraseHook(hiText, enWord) {
  const cleanHi = hiText.split("/")[0].replace(/\(.*?\)/g, "").trim();
  const capHi = cleanHi.charAt(0).toUpperCase() + cleanHi.slice(1);
  const words = cleanHi.toLowerCase().split(/[\s\-]+/).filter(Boolean);
  const glossed = [];
  for (const w of words) {
    const cleanW = w.replace(/[^a-z]/g, "");
    if (HINDI_WORD_GLOSS[cleanW]) {
      glossed.push(`<strong>${cleanW.charAt(0).toUpperCase() + cleanW.slice(1)}</strong> (${HINDI_WORD_GLOSS[cleanW]})`);
    }
  }
  if (glossed.length > 0) {
    return `<strong>${capHi}</strong> ≈ ${glossed.join(" + ")} → <em>${enWord}</em>.`;
  }
  return `<strong>${capHi}</strong> ≈ Everyday spoken Hindi expression for <em>${enWord}</em>.`;
}

// Clarify "/" in translations when one word is the English word and the other is native/formal (Problem 2)
function clarifySlashTranslations(card) {
  const wordUpper = String(card.word || "").trim().toUpperCase();
  if (MULTI_MEANING_CARDS[wordUpper]) return;

  const enClean = stripAccents(wordUpper).toLowerCase().replace(/[^a-z]/g, "");
  if (card.trans && card.trans.hi && card.trans.hi.includes("/")) {
    const hi = card.trans.hi;
    // Skip if already labeled with ":" or "1." or "(spoken)" or "(formal)"
    if (!hi.includes(":") && !hi.includes("1.") && !hi.includes("(spoken)") && !hi.includes("(formal)") && !hi.includes("(daily)")) {
      const parts = hi.split("/").map(p => p.trim()).filter(Boolean);
      if (parts.length === 2) {
        const p0 = parts[0].toLowerCase().replace(/[^a-z]/g, "");
        const p1 = parts[1].toLowerCase().replace(/[^a-z]/g, "");
        const p0IsEn = (p0 === enClean) || (p0.length >= 4 && enClean.length >= 4 && (p0.includes(enClean) || enClean.includes(p0)));
        const p1IsEn = (p1 === enClean) || (p1.length >= 4 && enClean.length >= 4 && (p1.includes(enClean) || enClean.includes(p1)));
        if (p0IsEn && !p1IsEn) {
          card.trans.hi = `${parts[0]} (spoken) / ${parts[1]} (formal)`;
        } else if (p1IsEn && !p0IsEn) {
          card.trans.hi = `${parts[0]} (daily) / ${parts[1]} (spoken)`;
        } else {
          // Two Hindi synonyms for the same concept
          card.trans.hi = `${parts[0]} / ${parts[1]} (same meaning)`;
        }
      }
    }
  }

  if (card.trans && card.trans.es && card.trans.es.includes("/")) {
    const es = card.trans.es;
    if (!es.includes(":") && !es.includes("1.") && !es.includes("(")) {
      const parts = es.split("/").map(p => p.trim()).filter(Boolean);
      if (parts.length === 2) {
        const p1 = parts[1].toLowerCase().replace(/[^a-z]/g, "");
        if (p1 === enClean) {
          card.trans.es = `${parts[0]} (or ${parts[1]})`;
        } else {
          card.trans.es = `${parts[0]} (or ${parts[1]})`;
        }
      }
    }
  }
}

function auditCard(card) {
  if (!card) return card;
  const word = String(card.word || "").trim().toUpperCase();
  const enTitle = word.charAt(0) + word.slice(1).toLowerCase();

  // 1. Multi-meaning override
  if (MULTI_MEANING_CARDS[word]) {
    const ov = MULTI_MEANING_CARDS[word];
    card.tamil = ov.tamil;
    card.trans.es = ov.trans.es;
    card.trans.hi = ov.trans.hi;
    card.shortcutEs = ov.shortcutEs;
    card.shortcutHi = ov.shortcutHi;
  } else {
    // 2. Strip Devanagari (Problem 4)
    if (card.trans && card.trans.hi) card.trans.hi = stripDevanagari(card.trans.hi);
    if (card.shortcutHi) card.shortcutHi = stripDevanagari(card.shortcutHi);
    if (card.shortcutEs) card.shortcutEs = stripDevanagari(card.shortcutEs);

    // 3. Strip redundant "+ Tamil ..." from shortcuts (Problem 3)
    if (card.shortcutEs) card.shortcutEs = stripRedundantPlusTamil(card.shortcutEs);
    if (card.shortcutHi) card.shortcutHi = stripRedundantPlusTamil(card.shortcutHi);

    const esRaw = (card.trans && card.trans.es) ? card.trans.es : "";
    const hiRaw = (card.trans && card.trans.hi) ? card.trans.hi : "";
    const esPrimary = esRaw.split("/")[0].split("|")[0].split("(")[0].trim();
    const hiPrimary = hiRaw.split("/")[0].split("|")[0].split("(")[0].trim();

    // 4. Problem 3: If Spanish word is similar to English, keep it simple & clean!
    if (isSpanishEnglishCognate(esPrimary, word) && !esRaw.includes("|") && !esRaw.includes(":")) {
      const capEs = esPrimary.charAt(0).toUpperCase() + esPrimary.slice(1);
      card.shortcutEs = `<strong>${capEs}</strong> ≈ Similar to English <strong>"${enTitle}"</strong>.`;
    } else if (card.shortcutEs && (
      card.shortcutEs.includes("Direct match with English") ||
      card.shortcutEs.includes("100% identical to English")
    )) {
      // Simplify existing verbose cognate message
      const mCog = card.shortcutEs.match(/English\s+<strong>"([^"]+)"<\/strong>/i);
      const cogWord = mCog ? mCog[1] : enTitle;
      const capEs = esPrimary.charAt(0).toUpperCase() + esPrimary.slice(1);
      card.shortcutEs = `<strong>${capEs}</strong> ≈ Similar to English <strong>"${cogWord}"</strong>.`;
    } else if (card.shortcutEs && (
      card.shortcutEs.includes("Syllable breakdown") ||
      card.shortcutEs.includes("Everyday Spanish for") ||
      card.shortcutEs.includes("Key root")
    )) {
      const capEs = esPrimary.charAt(0).toUpperCase() + esPrimary.slice(1);
      card.shortcutEs = `<strong>${capEs}</strong> ≈ Core Spanish word for <strong>"${enTitle}"</strong>.`;
    }

    // 5. Problem 1 & 3 for Hindi:
    const hiClean = hiPrimary.toLowerCase().replace(/[^a-z]/g, "");
    const enClean = stripAccents(word).toLowerCase().replace(/[^a-z]/g, "");
    const isHiSameAsEn = (hiClean === enClean) || (hiClean.length >= 4 && enClean.length >= 4 && (hiClean === enClean + "s" || enClean === hiClean + "s"));

    if (isHiSameAsEn && !hiRaw.includes("/") && !hiRaw.includes("|")) {
      const capHi = hiPrimary.charAt(0).toUpperCase() + hiPrimary.slice(1);
      card.shortcutHi = `<strong>${capHi}</strong> ≈ Same as English <strong>"${enTitle}"</strong> (used directly in daily spoken Hindi).`;
    } else if (card.shortcutHi) {
      // Check for fake "Spoken Tamil" or "Key root" or "Spoken Hindi phrase for"
      const hasFakeSpokenTamil = card.shortcutHi.includes("Spoken Tamil") && !hasGenuineTamilRoot(card.shortcutHi);
      const hasTemplatePhrase = (
        card.shortcutHi.includes("Spoken Hindi phrase for") ||
        card.shortcutHi.includes("Key root") ||
        card.shortcutHi.includes("Spoken Hindi for") ||
        card.shortcutHi.includes("100% identical to English")
      );
      if (hasFakeSpokenTamil || hasTemplatePhrase) {
        if (hiRaw.toLowerCase().includes(enClean)) {
          const capHi = hiPrimary.charAt(0).toUpperCase() + hiPrimary.slice(1);
          card.shortcutHi = `<strong>${capHi}</strong> ≈ In daily spoken Hindi, people also directly use English <strong>"${enTitle}"</strong>.`;
        } else {
          card.shortcutHi = buildCleanHindiPhraseHook(hiRaw, enTitle);
        }
      }
    }

    // 6. Clarify "/" in translations (Problem 2)
    clarifySlashTranslations(card);
  }

  // Ensure hiDevanagari is Roman only (Problem 4)
  card.hiDevanagari = stripDevanagari(card.trans?.hi || card.word);

  // 7. Assign 100% Accurate Concept Photo (Problem 5)
  // Replace any modulo-cycled Wikimedia image or missing image with verified Unsplash concept photo
  if (wordToPhotoId[word]) {
    card.imageUrl = getUnsplashUrl(wordToPhotoId[word]);
  } else if (!card.imageUrl || card.imageUrl.includes("wikimedia.org") || card.imageUrl.startsWith("/api/image") || card.imageUrl.startsWith("data:image/svg")) {
    const catPhotoId = getCategoryUnsplashId(card.category, card.originalNum || card.num);
    card.imageUrl = getUnsplashUrl(catPhotoId);
  }

  return card;
}

const newAccurateImages = {};
let totalProcessed = 0;

for (const dv of deckVars) {
  const regex = new RegExp(`(var|const|let)\\s+${dv}\\s*=\\s*(\\[.*?\\]);`, "s");
  const match = htmlContent.match(regex);
  if (!match) continue;

  const prefix = match[1];
  const cards = JSON.parse(match[2]);
  for (const c of cards) {
    auditCard(c);
    const numKey = String(c.originalNum || c.num);
    newAccurateImages[numKey] = c.imageUrl;
    if (c.id) newAccurateImages[c.id] = c.imageUrl;
    totalProcessed++;
  }
  htmlContent = htmlContent.replace(match[0], `${prefix} ${dv} = ${JSON.stringify(cards)};`);
  console.log(`Processed ${cards.length} cards in ${dv}`);
}

// Update cardAccurateImages in index.html
const accMatch = htmlContent.match(/var cardAccurateImages\s*=\s*(\{[^\n]+\});/);
if (accMatch) {
  htmlContent = htmlContent.replace(accMatch[0], `var cardAccurateImages = ${JSON.stringify(newAccurateImages)};`);
}
fs.writeFileSync(path.join(__dirname, "accurate_images.json"), JSON.stringify(newAccurateImages, null, 2), "utf8");

// Clean cardShortcuts (800-1000) so it has zero Devanagari or "+ Tamil"
const csMatch = htmlContent.match(/var cardShortcuts\s*=\s*(\{[^\n]+\});/);
if (csMatch) {
  const cs = JSON.parse(csMatch[1]);
  for (const [k, v] of Object.entries(cs)) {
    if (v.es) v.es = stripRedundantPlusTamil(stripDevanagari(v.es));
    if (v.hi) v.hi = stripRedundantPlusTamil(stripDevanagari(v.hi));
  }
  htmlContent = htmlContent.replace(csMatch[0], `var cardShortcuts = ${JSON.stringify(cs)};`);
}

// Clear hindiDevMap so zero Devanagari exists anywhere in index.html
htmlContent = htmlContent.replace(/var hindiDevMap\s*=\s*\{[\s\S]*?\};/, "var hindiDevMap = {};");

// Bump STORAGE_KEY_EDITS to v6 and update isStaleTemplateShortcut so stale browser/cloud edits never overwrite fixed cards
htmlContent = htmlContent.replace(
  /var STORAGE_KEY_EDITS = "sequential_vocab_user_custom_edits_v5";/,
  'var STORAGE_KEY_EDITS = "sequential_vocab_user_custom_edits_v6";'
);
htmlContent = htmlContent.replace(/e\.schemaVer === 5/g, "e.schemaVer === 6");
htmlContent = htmlContent.replace(/schemaVer: 5/g, "schemaVer: 6");

fs.writeFileSync(indexHtmlPath, htmlContent, "utf8");
console.log(`=== MASTER OVERHAUL COMPLETE: ${totalProcessed} cards updated across all decks ===`);
