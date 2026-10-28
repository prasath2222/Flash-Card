import glob
import json
import re
import unicodedata
from scripts.es_hooks_data import ES_SOUND_ALIKES
from scripts.hi_hooks_data import HI_SOUND_ALIKES

def strip_acc(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()

# Accurate Spanish Phonetic Pronunciation Generator (matches 800-1000 style e.g. Pizarra -> Pee-sah-rah)
def pronounce_es_word(word):
    w = word.strip().lower()
    w = re.sub(r"[^a-záéíóúüñ]", "", w)
    if not w:
        return ""
    # Common exact overrides for ultra-clean pronunciation
    exact_pron = {
        "pizarra": "Pee-sah-rah",
        "tiza": "Tee-sah",
        "lápiz": "Lah-pees",
        "borrador": "Boh-rah-dor",
        "cuaderno": "Kwah-der-noh",
        "olvidadizo": "Ohl-vee-dah-dee-soh",
        "profesor": "Proh-feh-sor",
        "aula": "Ow-lah",
        "cielo": "Syeh-loh",
        "sol": "Sol",
        "luna": "Loo-nah",
        "estrella": "Es-treh-yah",
        "nube": "Noo-beh",
        "lluvia": "Yoo-vyah",
        "nieve": "Nyeh-veh",
        "hielo": "Yeh-loh",
        "viento": "Vyen-toh",
        "llorar": "Yoh-rar",
        "quejarse": "Keh-har-seh",
        "hipo": "Ee-poh",
        "eructar": "Eh-rook-tar",
        "jadear": "Hah-deh-ar",
        "hormiguear": "Or-mee-geh-ar",
        "guion": "Gee-on",
        "ajedrez": "Ah-heh-dres",
        "reloj": "Reh-loh",
        "llave": "Yah-vay",
        "ojo": "Oh-hoh",
        "aguja": "Ah-goo-hah",
        "jeringa": "Heh-reen-gah",
        "cirugía": "See-roo-hee-ah",
        "psiquiatra": "See-kyah-trah",
        "psiquiatría": "See-kyah-tree-ah",
        "psicología": "See-koh-loh-hee-ah",
        "química": "Kee-mee-kah",
        "física": "Fee-see-kah",
        "éxito": "Ek-see-toh",
        "examen": "Ek-sah-men",
        "búho": "Boo-oh",
        "pingüino": "Peen-gwee-noh",
        "ungüento": "Oon-gwen-toh",
        "vergüenza": "Ver-gwen-sah",
        "cónyuge": "Kon-yoo-heh",
    }
    if w in exact_pron:
        return exact_pron[w]

    # Phonetic transformation rules for Spanish
    s = w
    s = s.replace("qu", "k").replace("güe", "gweh").replace("güi", "gwee")
    s = s.replace("gue", "geh").replace("gui", "gee")
    s = s.replace("ge", "heh").replace("gi", "hee")
    s = s.replace("j", "h")
    s = s.replace("ll", "y")
    s = s.replace("ñ", "ny")
    s = s.replace("ch", "ch")
    s = s.replace("ce", "seh").replace("ci", "see").replace("z", "s")
    s = s.replace("h", "")  # silent h (after ch is handled; wait: protect ch first!)

    # Re-do carefully protecting 'ch' and 'sh'
    s = w
    s = s.replace("ch", "§")
    s = s.replace("qu", "k").replace("güe", "gwe").replace("güi", "gwi")
    s = s.replace("gue", "ge").replace("gui", "gi")
    s = s.replace("ge", "he").replace("gi", "hi").replace("j", "h")
    s = s.replace("ll", "y").replace("ñ", "ny")
    s = s.replace("ce", "se").replace("ci", "si").replace("z", "s")
    s = s.replace("h", "")
    s = s.replace("§", "ch")
    s = s.replace("ción", "syon").replace("sión", "syon").replace("tión", "tyon")
    s = s.replace("ia", "yah").replace("ie", "yeh").replace("io", "yoh").replace("ua", "wah").replace("ue", "weh")
    s = strip_acc(s)
    return s.capitalize()

def pronounce_es(es_phrase):
    main = es_phrase.split("/")[0].split("(")[0].strip()
    words = [w for w in re.split(r"\s+", main) if w]
    prons = [pronounce_es_word(w) for w in words[:4]]
    return " ".join(p for p in prons if p)

# Map of atomic Spanish building blocks for multi-word phrases
ATOMIC_ES_PARTS = {
    "profesor": 'Profesor ("Professor")',
    "universitario": 'Universitario ("University")',
    "director": 'Director ("Director")',
    "escolar": 'Escolar ("School")',
    "compañero": 'Compañero ("Companion")',
    "clase": 'Clase ("Class")',
    "pizarra": 'Pizarra ("Pizza-Board")',
    "blanca": 'Blanca ("Blank White")',
    "libro": 'Libro ("Library Book")',
    "texto": 'Texto ("Text")',
    "cuaderno": 'Cuaderno ("Quarter-Note" Notebook)',
    "ejercicios": 'Ejercicios ("Exercises")',
    "nota": 'Nota ("Note")',
    "adhesiva": 'Adhesiva ("Adhesive" sticky)',
    "pinzas": 'Pinzas ("Pinchers")',
    "cocina": 'Cocina ("Kitchen")',
    "rodillo": 'Rodillo ("Roller")',
    "amasar": 'Amasar ("Mash/Knead" dough)',
    "tabla": 'Tabla ("Table/Board")',
    "cortar": 'Cortar ("Cut")',
    "recipiente": 'Recipiente ("Recipient" container)',
    "hermético": 'Hermético ("Hermetic" airtight)',
    "papel": 'Papel ("Paper")',
    "aluminio": 'Aluminio ("Aluminum")',
    "individual": 'Individual ("Single mat")',
    "mesa": 'Mesa ("Table/மேசை")',
    "funda": 'Funda ("Found-Cover")',
    "almohada": 'Almohada ("All-My-Head" Pillow)',
    "ropa": 'Ropa ("Robes/Clothes")',
    "sucia": 'Sucia ("Soot-Dirty")',
    "pinza": 'Pinza ("Pincher clip")',
    "enjuague": 'Enjuague ("In-Wash" rinse)',
    "bucal": 'Bucal ("Vocal/Mouth")',
    "hilo": 'Hilo ("Thread")',
    "dental": 'Dental ("Dental/Teeth")',
    "protector": 'Protector ("Protector")',
    "solar": 'Solar ("Sun")',
    "secador": 'Secador ("Desiccate/Dryer")',
    "pelo": 'Pelo ("Pelt/Hair")',
    "pañuelo": 'Pañuelo ("Handkerchief")',
    "carrito": 'Carrito ("Little Cart")',
    "compras": 'Compras ("Shopping")',
    "código": 'Código ("Code")',
    "barras": 'Barras ("Bars")',
    "etiqueta": 'Etiqueta ("Etiquette/Tag")',
    "precio": 'Precio ("Price")',
    "entrega": 'Entrega ("Entry/Delivery")',
    "domicilio": 'Domicilio ("Domicile/Home")',
    "tortilla": 'Tortilla ("Omelet")',
    "huevos": 'Huevos ("Eggs")',
    "palomitas": 'Palomitas ("Little White Doves" = Popcorn)',
    "maíz": 'Maíz ("Maize/Corn")',
    "batido": 'Batido ("Beaten/Blended shake")',
    "frutas": 'Frutas ("Fruits")',
    "estado": 'Estado ("State")',
    "ánimo": 'Ánimo ("Animated Spirit/Mood")',
    "nombre": 'Nombre ("Name")',
    "usuario": 'Usuario ("User")',
    "inicio": 'Inicio ("Initiate/Start")',
    "sesión": 'Sesión ("Session")',
    "cerrar": 'Cerrar ("Close")',
    "captura": 'Captura ("Capture")',
    "pantalla": 'Pantalla ("Screen")',
    "fondo": 'Fondo ("Background/Fund")',
    "tono": 'Tono ("Tone")',
    "llamada": 'Llamada ("Call")',
    "auriculares": 'Auriculares ("Earphones")',
    "inalámbricos": 'Inalámbricos ("Wireless")',
    "batería": 'Batería ("Battery")',
    "portátil": 'Portátil ("Portable")',
    "punto": 'Punto ("Point")',
    "acceso": 'Acceso ("Access")',
    "cámara": 'Cámara ("Camera")',
    "computadora": 'Computadora ("Computer")',
    "teclado": 'Teclado ("Keyboard")',
    "numérico": 'Numérico ("Numeric")',
    "táctil": 'Táctil ("Tactile/Touch")',
    "transmisión": 'Transmisión ("Transmission")',
    "directo": 'Directo ("Direct/Live")',
    "bandeja": 'Bandeja ("Tray")',
    "entrada": 'Entrada ("Entry/In")',
    "correo": 'Correo ("Courier/Mail")',
    "basura": 'Basura ("Trash")',
    "archivo": 'Archivo ("Archive/File")',
    "adjunto": 'Adjunto ("Adjoined/Attached")',
    "ramo": 'Ramo ("Branch/Bunch")',
    "flores": 'Flores ("Flowers")',
    "asesor": 'Asesor ("Advisor")',
    "legal": 'Legal ("Legal")',
    "piel": 'Piel ("Peel/Skin")',
    "gallina": 'Gallina ("Hen")',
    "reír": 'Reír ("Laugh")',
    "dientes": 'Dientes ("Dentist/Teeth")',
    "fruncir": 'Fruncir ("Furrow/Wrinkle")',
    "ceño": 'Ceño ("Brow")',
    "poner": 'Poner ("Put")',
    "mala": 'Mala ("Bad")',
    "cara": 'Cara ("Face")',
    "palpitar": 'Palpitar ("Palpitate/Beat")',
    "dolor": 'Dolor ("Dolorous Pain")',
    "sentir": 'Sentir ("Sense/Feel")',
    "vergüenza": 'Vergüenza ("Shame/Cringe")',
}

# Parse user's original .txt files (1001-3000) to restore clean daily spoken Hindi
RAW_TXT_HI = {}
for path in sorted(glob.glob("public/assets/aistudio/Untitled_document_*.txt")):
    with open(path, "r", encoding="utf-8-sig") as f:
        text = f.read()
    for m in re.finditer(r"(\d+)\.\s*([^\n=]+)=\s*([^\n]+)", text):
        num = int(m.group(1))
        word_part = m.group(2).strip()
        word_clean = re.sub(r"^[^\w]+", "", word_part).strip().upper()
        trans_part = m.group(3).strip()
        if "/" in trans_part:
            es, hi = [x.strip() for x in trans_part.split("/", 1)]
        else:
            es, hi = trans_part, ""
        RAW_TXT_HI[word_clean] = hi

# Everyday spoken Hindi pairs where showing both spoken Hindi & loanword is best for learners
SPOKEN_HI_PAIRS = {
    "TEACHER": "teacher",
    "PROFESSOR": "professor",
    "TUTOR": "tutor",
    "PRINCIPAL": "principal",
    "INSTRUCTOR": "instructor",
    "CLASSMATE": "classmate",
    "CLASSROOM": "classroom",
    "BLACKBOARD": "blackboard",
    "WHITEBOARD": "whiteboard",
    "CHALK": "chalk",
    "MARKER": "marker",
    "ERASER": "rabad / eraser",
    "TEXTBOOK": "kitaab / textbook",
    "NOTEBOOK": "copy / notebook",
    "WORKBOOK": "workbook",
    "PENCIL": "pencil",
    "SALARY": "salary / tankhwah",
    "BONUS": "bonus",
    "COMMISSION": "commission / dalali",
    "PROMOTION": "promotion / tarakki",
    "DEMOTION": "demotion",
    "RETIREMENT": "retirement",
    "PENSION": "pension",
    "CONTRACT": "contract",
    "PROJECT": "project",
    "DEADLINE": "deadline",
    "PARTNER": "partner / saathi",
    "VISITOR": "visitor / mehmaan",
    "FOLLOWER": "follower",
    "ANNIVERSARY": "anniversary / saalgirah",
    "TIGHT": "tight / kasa hua",
    "MOOD": "mood / mijaaz",
    "DEPRESSION": "depression / tanaav",
    "CREATIVE": "creative",
    "AMBITIOUS": "ambitious",
    "CAREER": "career",
    "BOSS": "boss / maalik",
    "MANAGER": "manager",
    "SUPERVISOR": "supervisor",
    "EXECUTIVE": "executive",
    "SECRETARY": "secretary",
    "CLERK": "clerk",
    "ACCOUNTANT": "accountant / munshi",
    "ENGINEER": "engineer",
    "ARCHITECT": "architect",
    "PLUMBER": "plumber",
    "ELECTRICIAN": "electrician",
    "MECHANIC": "mechanic",
    "OPERATOR": "operator",
    "PILOT": "pilot",
    "CAPTAIN": "captain",
    "TECHNICIAN": "technician",
    "WAITER": "waiter",
    "WAITRESS": "waitress",
    "CHEF": "chef / rasoiya",
    "ARTIST": "artist / kalakaar",
    "ACTOR": "actor",
    "ACTRESS": "actress",
    "MUSICIAN": "musician / sangeetkaar",
    "PHOTOGRAPHER": "photographer",
    "FILMMAKER": "filmmaker",
    "CORRESPONDENT": "correspondent / reporter",
    "EDITOR": "editor",
    "COLUMNIST": "columnist / lekhak",
    "ANCHOR": "news anchor",
    "PRESENTER": "presenter / anchor",
    "MAGISTRATE": "magistrate / judge",
    "DETECTIVE": "detective / jaasoos",
    "POLICE": "police",
    "FIREFIGHTER": "firefighter",
    "WARDEN": "warden",
    "PARAMEDIC": "paramedic",
    "RESUME": "resume / bio-data",
    "INTERVIEW": "interview",
    "HIRING": "hiring / bharti",
    "RECRUITMENT": "recruitment / bharti",
    "APPEAL": "appeal",
    "CONVICTION": "saza / jurm saabit",
    "ORCHESTRA": "orchestra",
    "SYMPHONY": "symphony",
    "CHOIR": "choir",
    "CHORUS": "chorus",
    "SURGERY": "surgery / operation",
    "SYRINGE": "syringe / injection",
    "THERMOMETER": "thermometer",
    "ULTRASOUND": "ultrasound / sonography",
    "THERAPY": "therapy / ilaaj",
    "THERAPIST": "therapist",
    "PAINKILLER": "painkiller / dard ki goli",
    "STRETCHER": "stretcher",
    "CRUTCH": "baisakhi / crutch",
    "SLING": "arm sling / patti",
    "PSYCHIATRIST": "psychiatrist",
    "COUNSELING": "counseling / salaah",
    "COUNSELOR": "counselor / salaahkaar",
    "PHOBIA": "phobia / dar",
    "ADDICTION": "lat / addiction",
    "BURNOUT": "burnout / thakaan",
    "HYSTERIA": "hysteria",
    "ILLUSION": "bhram / illusion",
    "HALLUCINATION": "bhram / hallucination",
    "MINDSET": "soch / mindset",
    "ESTEEM": "aatma-sammaan / self-esteem",
    "DEMENTIA": "bhoolne ki beemaari / dementia",
    "JET LAG": "jet lag / safar ki thakaan",
    "MONEY CHANGER": "money changer",
    "AISLE SEAT": "aisle seat / galiyare wali seat",
    "WINDOW SEAT": "window seat / khidki wali seat",
    "BOARDING PASS": "boarding pass",
    "CUSTOMS": "customs",
    "TERMINAL": "terminal",
    "RUNWAY": "runway / hawai patti",
    "COCKPIT": "cockpit",
    "FLIGHT ATTENDANT": "air hostess / flight attendant",
    "BAGGAGE": "saamaan / luggage",
    "RESERVATION": "booking / reservation",
    "BOOKING": "booking",
    "TOURIST": "tourist / sailaani",
    "TOURISM": "tourism / paryatan",
    "SIGHTSEEING": "sightseeing / ghoomna",
    "SOUVENIR": "yaadgaar / souvenir",
    "RECEPTION": "reception",
    "FRONT DESK": "front desk / reception",
    "KEYCARD": "keycard",
    "ROOM SERVICE": "room service",
    "HOUSEKEEPING": "housekeeping / safaai",
    "VISA": "visa",
    "IMMIGRATION": "immigration",
    "PASSPORT CONTROL": "passport check",
    "EXCESS BAGGAGE": "extra saamaan / excess baggage",
    "LAYOVER": "layover / rukawat",
    "STOPOVER": "stopover / halt",
    "USERNAME": "username",
    "SCREENSHOT": "screenshot",
    "SUBTITLE": "subtitles",
    "ATTACHMENT": "attachment / file jodna",
    "CHOPPING BOARD": "chopping board",
    "DISHWASHER": "dishwasher",
    "MOUTHWASH": "mouthwash",
    "SUNSCREEN": "sunscreen",
    "HAIRDRYER": "hair dryer",
    "DIRECTOR": "director",
    "OFFICER": "officer / afsar",
    "CONTRACTOR": "contractor / thekedaar",
    "JOURNALIST": "journalist / patrakaar",
    "CONSUMER": "customer / upbhokta",
    "SUPPLIER": "supplier",
    "ASSOCIATE": "associate / sahyogi",
    "COUPON": "coupon / voucher",
    "INSTALLMENT": "EMI / kisht",
    "AUDIT": "audit",
    "INVESTMENT": "investment / nivesh",
    "RISK": "risk / jokhim",
    "DIVIDEND": "dividend / laabhaansh",
    "MONOPOLY": "monopoly / ekadhikar",
    "WARRANT": "arrest warrant",
    "PARLIAMENT": "parliament / sansad",
    "CONGRESS": "congress",
    "COUNCIL": "council / parishad",
    "MINISTRY": "ministry / mantraalaya",
    "SENATOR": "senator / MP",
    "GOVERNOR": "governor / rajyapaal",
    "CANDIDATE": "candidate / umeedwaar",
    "NOMINEE": "nominee / umeedwaar",
    "EMBASSY": "embassy / dootavaas",
    "AMBASSADOR": "ambassador / raajdoot",
    "ARMY": "army / fauj",
    "NAVY": "navy / nausena",
    "CEASEFIRE": "ceasefire / yuddhaviraam",
    "MEDIA": "media",
    "EDITORIAL": "editorial / sampadakiya",
    "DISPATCH": "dispatch / bhejna",
    "COVERAGE": "news coverage",
    "JOURNAL": "journal / patrika",
    "PUBLICATION": "publication / prakashan",
    "BULLETIN": "news bulletin",
    "STUDENT": "student / chhaatra",
    "SYLLABUS": "syllabus",
    "CURRICULUM": "curriculum",
    "SCHOLARSHIP": "scholarship / chhatravritti",
    "CERTIFICATE": "certificate",
    "GEOGRAPHY": "geography / bhoogol",
    "MATH": "maths / ganit",
    "ALGEBRA": "algebra",
    "CHEMISTRY": "chemistry",
    "BIOLOGY": "biology",
    "PSYCHOLOGY": "psychology",
    "ECONOMICS": "economics",
    "GRAMMAR": "grammar / vyakaran",
    "HYPOTHESIS": "hypothesis / anumaan",
    "DATABASE": "database",
    "STATISTICS": "statistics / aakde",
    "EQUATION": "equation / samikaran",
    "ATOM": "atom / parmanu",
    "MICROSCOPE": "microscope",
    "ENERGY": "energy / oorja",
    "GRAVITY": "gravity / gurutvakarshan",
    "CIRCUIT": "circuit",
    "GALLERY": "art gallery",
    "EXHIBITION": "exhibition / pradarshani",
    "SOUNDTRACK": "soundtrack / film music",
    "RECORDING": "recording",
    "CONCERT": "concert",
    "ECOSYSTEM": "ecosystem",
    "FOSSIL": "fossil / jeevaashm",
    "FREELANCER": "freelancer",
    "FERTILIZER": "fertilizer / khaad",
    "PESTICIDE": "pesticide / keetnaashak",
    "INGREDIENT": "ingredients / saamaan",
    "CULINARY": "cooking / rasoi",
    "COURSE": "course",
    "DIAGNOSIS": "diagnosis / jaanch",
    "PRESCRIPTION": "doctor ki parchi / prescription",
    "DISINFECTANT": "disinfectant / phenyl",
    "VACCINE": "vaccine / teeka",
    "WHEELCHAIR": "wheelchair",
    "PSYCHIATRY": "psychiatry",
    "EGO": "ego / ghamand",
    "EXTROVERT": "extrovert / milansaar",
    "FLATMATE": "flatmate",
    "ROOMMATE": "roommate",
    "INSPECTION": "inspection / jaanch",
    "TURNSTILE": "turnstile gate",
    "CAPACITY": "capacity / kshamta",
    "LIMIT": "limit / seema",
    "MINIMUM": "minimum / kam se kam",
    "TEMPORARY": "temporary / asthaayi",
}

def find_cognate_match(eng_word, es_main):
    w_c = re.sub(r"[^a-z]", "", strip_acc(eng_word))
    es_c = re.sub(r"[^a-z]", "", strip_acc(es_main))
    if not w_c or not es_c:
        return None
    if w_c == es_c:
        return eng_word.title()
    if len(w_c) >= 4 and (w_c[:4] in es_c or es_c[:4] in w_c):
        return eng_word.title()
    if len(w_c) >= 3 and w_c[:3] == es_c[:3]:
        return eng_word.title()
    if es_c.startswith("es") and len(w_c) >= 3 and es_c[1:4] == w_c[:3]:
        return eng_word.title()
    # Check common suffix transformations: -ción <-> -tion, -dad <-> -ty, -mente <-> -ly, -oso <-> -ous
    for es_suf, en_suf in [("cion", "tion"), ("sion", "sion"), ("dad", "ty"), ("tad", "ty"), ("mente", "ly"), ("oso", "ous"), ("ico", "ic"), ("ista", "ist"), ("ismo", "ism")]:
        if es_c.endswith(es_suf) and len(es_c) > len(es_suf) + 2:
            stem = es_c[:-len(es_suf)]
            if stem[:3] == w_c[:3]:
                return eng_word.title()
    return None

# Syllable sound-alike generator for any Spanish word not in ES_SOUND_ALIKES or cognates
SYL_MAP = {
    "ab": "Up", "ac": "Act", "ad": "Add", "af": "Af-", "ag": "Ag-", "al": "All", "am": "Am",
    "an": "On", "ap": "Up", "ar": "Art", "as": "Ace", "at": "At", "au": "Auto", "av": "Av-",
    "ba": "Bar", "be": "Best", "bi": "Bi", "bl": "Blue", "bo": "Box", "br": "Bright", "bu": "Bus",
    "ca": "Car", "ce": "Set", "ch": "Check", "ci": "See", "cl": "Clear", "co": "Co", "cr": "Cross", "cu": "Cup",
    "da": "Day", "de": "De", "di": "Direct", "do": "Door", "dr": "Drive", "du": "Due",
    "ef": "Ef-", "ej": "Ex-", "el": "El", "em": "In", "en": "In", "eq": "Equal", "er": "Air", "es": "Step", "ev": "Ever", "ex": "Ex",
    "fa": "Fast", "fe": "Fair", "fi": "Fine", "fl": "Flow", "fo": "Focus", "fr": "Fresh", "fu": "Full",
    "ga": "Gain", "ge": "Gem", "gi": "Giant", "gl": "Glow", "go": "Go", "gr": "Grand", "gu": "Guard",
    "ha": "High", "he": "Hey", "hi": "High", "ho": "Home", "hu": "Huge",
    "id": "Idea", "ig": "Equal", "il": "Ill-", "im": "In", "in": "In", "ir": "Go",
    "ja": "Jar", "je": "Jet", "ji": "Jig", "jo": "Joy", "ju": "Just",
    "la": "Lap", "le": "Lead", "li": "Line", "ll": "Yeah", "lo": "Low", "lu": "Light",
    "ma": "Main", "me": "Meet", "mi": "Mini", "mo": "Move", "mu": "Much",
    "na": "Now", "ne": "Net", "ni": "Near", "no": "Note", "nu": "New",
    "ob": "Ob-", "oc": "Oc-", "of": "Of-", "oj": "Eye", "ol": "All", "op": "Open", "or": "Order", "os": "Os-",
    "pa": "Pack", "pe": "Pen", "pi": "Peak", "pl": "Plan", "po": "Power", "pr": "Pro", "pu": "Pure",
    "qu": "Key", "ra": "Run", "re": "Re-Do", "ri": "Rich", "ro": "Roll", "ru": "Rule",
    "sa": "Safe", "se": "See", "si": "Sit", "so": "So", "su": "Super",
    "ta": "Tap", "te": "Tech", "ti": "Time", "to": "Top", "tr": "Track", "tu": "Turn",
    "ub": "Up", "ul": "Ultra", "un": "One", "ur": "Urgent", "us": "Use", "ut": "Use",
    "va": "Val-", "ve": "View", "vi": "Vital", "vo": "Voice", "vu": "Turn",
    "ya": "Yah", "ye": "Yes", "za": "Zap", "zo": "Zone", "zu": "Zoom",
}

ATOMIC_HI_PARTS = {
    "aap": "Aap (You)", "aapka": "Aapka (Your)", "aapki": "Aapki (Your)", "aapse": "Aapse (With you)",
    "main": "Main (I)", "mera": "Mera (My)", "meri": "Meri (My)", "mujhe": "Mujhe (To me)",
    "tum": "Tum (You)", "kya": "Kya (What)", "kaise": "Kaise (How)", "kaisa": "Kaisa (How)",
    "kahan": "Kahan (Where)", "kab": "Kab (When)", "kaun": "Kaun (Who)",
    "hain": "Hain (Are)", "hai": "Hai (Is)", "hoon": "Hoon (Am)", "ho": "Ho (Are/Be)",
    "chal": "Chal (Going/Walk)", "raha": "Raha (-ing)", "rahe": "Rahe (-ing)", "rahi": "Rahi (-ing)",
    "milkar": "Milkar (Meeting)", "milte": "Milte (Meet)", "milna": "Milna (Meet)",
    "khushi": "Khushi (Tamil குஷி / Joy)", "achha": "Achha (Good)", "badhiya": "Badhiya (Great)",
    "naam": "Naam (Tamil நாமம் / Name)", "din": "Din (Tamil தினம் / Day)",
    "shubh": "Shubh (Tamil சுபம் / Good)", "prabhat": "Prabhat (Morning)",
    "sandhya": "Sandhya (Tamil சந்தியா / Evening)", "raatri": "Raatri (Tamil ராத்திரி / Night)",
    "jaldi": "Jaldi (Spoken Tamil ஜல்தி / Quickly)", "kal": "Kal (Tomorrow/Yesterday)",
    "fir": "Fir (Again)", "bohot": "Bohot (Very/Many)", "dino": "Dino (Days)", "baad": "Baad (After)",
    "aur": "Aur (And/More)", "naya": "Naya (Tamil நவ / New)", "sab": "Sab (All)",
    "parivaar": "Parivaar (Family)", "kar": "Kar (Do)", "karo": "Karo (Do)", "karna": "Karna (Do)",
    "yatra": "Yatra (Tamil யாத்திரை / Trip)", "khaane": "Khaane (Food)", "anand": "Anand (Tamil ஆனந்தம் / Joy)",
    "swaagat": "Swaagat (Tamil ஸ்வாகதம் / Welcome)", "aisa": "Aisa (Like this)",
    "lagta": "Lagta (Seems/Feels)", "nahi": "Nahi (No/Not)", "sahmat": "Sahmat ( Tamil சம்மதம் / Agree)",
    "yeh": "Yeh (This)", "sach": "Sach (Tamil சத்தியம் / True)", "sahi": "Sahi (Right)",
    "baat": "Baat (Matter/Talk)", "samajh": "Samajh (Understand)", "aata": "Aata (Comes)",
    "mazaak": "Mazaak (Joke/Kidding)", "ummeed": "Ummeed (Hope)", "shaq": "Shaq (Spoken Tamil சக் / Doubt)",
    "pakka": "Pakka ( Tamil பக்கா / Sure)", "pata": "Pata (Know)", "keh": "Keh (Say)",
    "nirbhar": "Nirbhar (Depend)", "theek": "Theek (Fine/Right)", "bhi": "Bhi (Also/Too)",
    "haal": "Haal (Condition)", "kismat": "Kismat (Spoken Tamil கிஸ்மத் / Luck)",
    "aitraaz": "Aitraaz (Objection)", "chahein": "Chahein (Wish)", "dekhne": "Dekhne (See/Look)",
    "sochne": "Sochne (Think)", "raay": "Raay (Opinion)", "matlab": "Matlab (Meaning)",
    "maano": "Maano (Believe)", "batao": "Batao (Tell)", "chhod": "Chhod (Leave)",
    "bhool": "Bhool (Forget)", "fark": "Fark (Difference)", "parwaah": "Parwaah (Care)",
    "apna": "Apna (Own)", "ghar": "Ghar (Home)", "aaraam": "Aaraam (Spoken Tamil ஆராம் / Rest)",
    "chinta": "Chinta (Tamil சிந்தனை / Worry)", "mat": "Mat (Don't)",
    "thoda": "Thoda (A little)", "zor": "Zor (Loud/Force)", "bolo": "Bolo (Speak)",
    "agar": "Agar (If)", "galat": "Galat (Wrong)", "mukhya": "Mukhya (Tamil முக்கியம் / Main)",
    "dheere": "Dheere (Slowly)", "chalo": "Chalo (Walk/Go)", "dhyaan": "Dhyaan (Tamil தியானம் / Care)",
    "madad": "Madad (Spoken Tamil மதத் / Help)", "kitne": "Kitne (How much)",
    "khulle": "Khulle (Loose change)", "rakh": "Rakh (Keep)", "bhatak": "Bhatak (Lost)",
    "taiyaar": "Taiyaar (Tamil தயார் / Ready)", "raaste": "Raaste (Spoken Tamil ராஸ்தா / Way)",
    "der": "Der (Late)", "jaana": "Jaana (Go)", "shaant": "Shaant (Tamil சாந்தம் / Calm)",
    "bhagwan": "Bhagwan (Tamil பகவான் / God)", "bhala": "Bhala (Good)",
    "janamdin": "Janamdin (Birthday)", "mubarak": "Mubarak (Congrats)",
    "sun": "Sun (Hear)", "dohra": "Dohra (Repeat)", "kripya": "Kripya (Tamil கிருபை / Please)",
    "kehte": "Kehte (Say)", "gaye": "Gaye (Went/Got)", "gaya": "Gaya (Got/Went)",
    "doosri": "Doosri (Other)", "taraf": "Taraf (Side)", "sthiti": "Sthiti (Case/State)",
    "kam": "Kam (Tamil கம்மி / Less)", "mool": "Mool (Tamil மூலம் / Root)",
    "imaandaari": "Imaandaari (Tamil நேர்மை / Honesty)", "peeche": "Peeche (Back)",
    "paidal": "Paidal (On foot)", "aage": "Aage (Ahead)", "hadd": "Hadd (Limit)",
    "zaroorat": "Zaroorat (Spoken Tamil ஜரூர் / Need)", "zyada": "Zyada (Spoken Tamil ஜாஸ்தி / More)",
    "bina": "Bina (Without)", "dhaar": "Dhaar (Sharp edge)", "takiye": "Takiye (Pillow)",
    "kapde": "Kapde (Tamil கப்படம் / Clothes)", "paka": "Paka (Tamil பக்குவம் / Ripe)",
    "sada": "Sada (Rotten)", "dara": "Dara (Scared)", "ghabraya": "Ghabraya (Nervous)",
    "uljhan": "Uljhan (Confusion)", "nimbu": "Nimbu (Lemon)", "paani": "Paani (Tamil பானம் / Water)",
    "hansna": "Hansna (Laugh)", "aanso": "Aanso (Tears)", "tevar": "Tevar (Frown)",
    "gusse": "Gusse (Anger)", "sar": "Sar (Tamil சிரம் / Head)", "kandhe": "Kandhe (Shoulders)",
    "nazar": "Nazar (Glance/Eye)", "palkein": "Palkein (Eyelids)", "aankhein": "Aankhein (Eyes)",
    "aah": "Aah (Sigh)", "gala": "Gala (Throat)", "ghutne": "Ghutne (Knees)",
    "jung": "Jung (Battle)", "hosla": "Hosla (Courage/Cheer)", "taaliyan": "Taaliyan (Claps)",
    "dhing": "Dhing (Boast)", "zinda": "Zinda (Alive)", "yakeen": "Yakeen (Belief/Convince)",
    "beech": "Beech (Middle)", "tokna": "Tokna (Interrupt)", "saaransh": "Saaransh (Tamil சாராம்சம் / Summary)",
    "safaai": "Safaai (Spoken Tamil சாஃப் / Cleaning)", "khaali": "Khaali (Spoken Tamil காலி / Empty)",
    "jagah": "Jagah (Place/Spot)", "chashma": "Chashma (Glasses)", "tyohaar": "Tyohaar (Festival)",
    "chhutti": "Chhutti (Spoken Tamil சுட்டி / Holiday)", "haath": "Haath (Hand)",
    "ghadi": "Ghadi (Tamil கடிகாரம் / Watch)", "giraawat": "Giraawat (Fall/Downturn)",
    "naai": "Naai (Barber)", "dukaan": "Dukaan (Shop)", "adaalat": "Adaalat (Court)",
    "davaai": "Davaai (Medicine)", "sarkari": "Sarkari (Tamil சர்க்கார் / Govt)",
    "vakeel": "Vakeel (Tamil வக்கீல் / Lawyer)", "ulti": "Ulti (Vomit/Nausea)",
    "vastu": "Vastu (Tamil வஸ்து / Object)", "dukhant": "Dukhant (Tamil துக்கம் / Tragedy)",
    "yantra": "Yantra (Tamil எந்திரம் / Instrument)", "naav": "Naav (Tamil நாவாய் / Boat)",
    "khilaadi": "Khilaadi (Player)", "dhuen": "Dhuen (Smoke)", "tapmaan": "Tapmaan (Tamil தாபம் / Temp)",
    "ganda": "Ganda (Dirty)", "pedon": "Pedon (Trees)", "kataai": "Kataai (Cutting)",
    "veeraan": "Veeraan (Wild)", "makke": "Makke (Corn)", "khet": "Khet (Field)",
    "phalon": "Phalon (Tamil பழம் / Fruits)", "bageecha": "Bageecha (Garden/Orchard)",
    "angooron": "Angooron (Grapes)", "paaltu": "Paaltu (Pet/Livestock)", "sookhi": "Sookhi (Dry)",
    "ghaas": "Ghaas (Grass/Hay)", "janga": "Janga (Rust)", "bheegha": "Bheegha (Soaked)",
    "dhoop": "Dhoop (Sun heat)", "thand": "Thand (Tamil தண்மை / Cold)",
    "tootne": "Tootne (Breaking)", "chabaane": "Chabaane (Chewing)", "fafundi": "Fafundi (Mold)",
    "dhuendaar": "Dhuendaar (Smoky)", "teekha": "Teekha (Spicy)", "teekhi": "Teekhi (Pungent)",
    "meetha": "Meetha (Sweet)", "ragad": "Ragad (Scrub)", "saans": "Saans (Breath)",
    "soojha": "Soojha (Swollen)", "seene": "Seene (Chest)", "jalan": "Jalan (Burning)",
    "ghaav": "Ghaav (Wound)", "behoshi": "Behoshi (Anesthesia)", "dimaagi": "Dimaagi (Brain/Intellect)",
    "avachetan": "Avachetan (Subconscious)", "hosh": "Hosh (Conscious)", "sadma": "Sadma (Trauma/Shock)",
    "pravritti": "Pravritti (Instinct)", "achanak": "Achanak (Sudden)", "vichaar": "Vichaar (Tamil விசாரம் / Thought)",
    "bolne": "Bolne (Speaking)", "yaadasht": "Yaadasht (Memory)", "ghar": "Ghar (House)",
    "maalikana": "Maalikana (Spoken Tamil மாலிக் / Ownership)", "rehne": "Rehne (Living)",
    "theherne": "Theherne (Staying)", "jootey": "Jootey (Shoes)", "hal": "Hal (Solution)",
    "oopar": "Oopar (Up)", "neeche": "Neeche (Down)", "udhaar": "Udhaar (Loan)",
    "door": "Door (Tamil தூரம் / Far)", "paas": "Paas (Near)", "alvida": "Alvida (Goodbye)",
}

def build_shortcut_es(card):
    word = card.get("word", "").strip()
    es_raw = card["trans"].get("es", "").strip()
    tamil = card.get("tamil", "").strip()
    ta_short = tamil.split("(")[0].strip() if tamil else ""
    es_main = es_raw.split("/")[0].split("(")[0].strip()
    es_lower = es_main.lower()
    es_cap = es_main[0].upper() + es_main[1:] if es_main else es_raw
    pron = pronounce_es(es_main)
    header = f"<strong>{es_cap} ({pron})</strong>" if pron and pron.lower() != es_lower else f"<strong>{es_cap}</strong>"

    # 1. Check handcrafted ES_SOUND_ALIKES
    if es_lower in ES_SOUND_ALIKES:
        bridge, link = ES_SOUND_ALIKES[es_lower]
        if "Tamil" not in bridge and ta_short:
            bridge = f"{bridge} + <strong>Tamil {ta_short}</strong>"
        return f"{header} ≈ {bridge} → {link}!"

    # Also check without reflexive -se
    if es_lower.endswith("se") and es_lower[:-2] in ES_SOUND_ALIKES:
        bridge, link = ES_SOUND_ALIKES[es_lower[:-2]]
        if "Tamil" not in bridge and ta_short:
            bridge = f"{bridge} + <strong>Tamil {ta_short}</strong>"
        return f"{header} ≈ {bridge} → {link}!"

    # 2. Check if Cognate with English word
    cog = find_cognate_match(word, es_main)
    if cog:
        ta_part = f" + <strong>Tamil {ta_short}</strong>" if ta_short else ""
        return f'{header} ≈ Direct match with English <strong>"{cog}"</strong>{ta_part} → Same root & sound: <em>{es_cap} = {word.title()}</em>!'

    # 3. Multi-word phrase breakdown
    if " " in es_main:
        tokens = [t for t in re.split(r"\s+", es_lower) if t not in ("de", "del", "la", "el", "los", "las", "en", "a", "con", "por", "para", "un", "una", "y", "o", "que", "se")]
        parts = []
        for t in tokens[:3]:
            t_clean = re.sub(r"[^a-záéíóúüñ]", "", t)
            if t_clean in ATOMIC_ES_PARTS:
                parts.append(ATOMIC_ES_PARTS[t_clean])
            elif t_clean in ES_SOUND_ALIKES:
                b_str = re.sub(r"<[^>]+>", "", ES_SOUND_ALIKES[t_clean][0]).replace("Sounds like ", "").replace("Direct match with English ", "")
                parts.append(f"{t_clean.capitalize()} ({b_str})")
            else:
                p_t = pronounce_es_word(t_clean)
                parts.append(f"{t_clean.capitalize()} ({p_t})")
        joined_parts = " + ".join(parts) if parts else f'"{pron}"'
        ta_part = f" + <strong>Tamil {ta_short}</strong>" if ta_short else ""
        return f"{header} ≈ <strong>{joined_parts}</strong>{ta_part} → Combine the parts for <em>{word.title()} ({es_cap})</em>!"

    # 4. Single non-cognate word: Build phonetic syllable sound-alike + Tamil bridge
    clean_w = re.sub(r"[^a-z]", "", strip_acc(es_lower))
    prefix2 = clean_w[:2]
    syl_cue = SYL_MAP.get(prefix2, pron.split("-")[0] if "-" in pron else pron)
    ta_part = f" + <strong>Tamil {ta_short}</strong>" if ta_short else ""
    return f'{header} ≈ Sounds like <strong>"{syl_cue}-{pron}"</strong>{ta_part} → Link the sound <em>"{pron}"</em> to <em>{word.title()} ({es_cap})</em>!'


def build_shortcut_hi(card):
    word = card.get("word", "").strip()
    hi_raw = card["trans"].get("hi", "").strip()
    hi_dev = card.get("hiDevanagari", "").strip()
    tamil = card.get("tamil", "").strip()
    ta_short = tamil.split("(")[0].strip() if tamil else ""

    hi_main = hi_raw.split("/")[0].split("(")[0].strip()
    hi_lower = hi_main.lower()
    hi_cap = hi_main[0].upper() + hi_main[1:] if hi_main else hi_raw

    if hi_dev and hi_dev != hi_raw and not re.search(r"[a-zA-Z]", hi_dev):
        header = f"<strong>{hi_cap} ({hi_dev})</strong>"
    else:
        header = f"<strong>{hi_cap}</strong>"

    # 1. Check handcrafted HI_SOUND_ALIKES (try full hi_lower, second slash-part, and first word)
    slash_parts = [p.strip().lower() for p in hi_raw.split("/") if p.strip()]
    for candidate in [hi_lower, hi_raw.lower()] + slash_parts + ([hi_lower.split()[0]] if hi_lower else []):
        if candidate in HI_SOUND_ALIKES:
            bridge, link = HI_SOUND_ALIKES[candidate]
            if "Tamil" not in bridge and ta_short:
                bridge = f"{bridge} + <strong>Tamil {ta_short}</strong>"
            return f"{header} ≈ {bridge} → {link}!"

    # 2. Check if hi_main is an everyday English loanword or compound loanword phrase
    w_clean = re.sub(r"[^a-z]", "", word.lower())
    hi_clean = re.sub(r"[^a-z]", "", hi_lower)
    ta_disp = tamil if tamil else word.title()
    if hi_clean == w_clean or any(re.sub(r"[^a-z]", "", p.lower()) == w_clean for p in slash_parts):
        return f'{header} ≈ 100% identical to spoken Tamil <strong>{ta_disp}</strong> & English <strong>"{word.title()}"</strong> → Same everyday word in Tamil, Hindi & English!'

    # Check if any word token of `word` (3+ letters) or common English loanword is in `hi_lower`
    w_tokens = [re.sub(r"[^a-z]", "", t) for t in word.lower().split() if len(re.sub(r"[^a-z]", "", t)) >= 3]
    extra_loans = ["jail", "survey", "football", "mic", "bore", "omelette", "registry", "shifting", "cancel", "entry", "bill", "gate", "red", "light", "backup", "table", "mat", "cover", "clip", "home", "loan", "hair", "salon", "medical", "store", "musical", "group", "dumping", "ground", "salary", "slip", "main", "course", "secret", "pin", "natural", "furniture", "plug", "form", "phone", "workout", "view", "puncture", "tyre", "travel", "plan"]
    matched_loan = None
    for tok in w_tokens + extra_loans:
        if tok and (tok in hi_lower or tok[:4] in hi_lower if len(tok) >= 5 else tok in hi_lower.split()):
            matched_loan = tok.capitalize()
            break
    if matched_loan:
        if any(v in hi_lower for v in ["karna", "lena", "dena", "hona", "lagana"]):
            return f'{header} ≈ Direct English word <strong>"{matched_loan}"</strong> + Hindi action <strong>{hi_lower.split()[-1].capitalize()}</strong> + <strong>Tamil {ta_short}</strong> → Everyday spoken Hinglish for <em>{word.title()} ({hi_cap})</em>!'
        return f'{header} ≈ Contains direct English word <strong>"{matched_loan}"</strong> + <strong>Tamil {ta_disp}</strong> → Same modern spoken word in Tamil, Hindi & English!'

    # 3. Multi-word Hindi phrase breakdown (word-by-word atomic breakdown with +)
    if " " in hi_main or "-" in hi_main:
        tokens = [re.sub(r"[^a-z]", "", t) for t in re.split(r"[\s\-]+", hi_lower) if t and t not in ("ka", "ki", "ke", "ko", "se", "mein", "par", "toh", "hi", "ya", "na", "ise", "iski", "iska", "us", "uske", "ek", "wala", "wali", "wale")]
        parts = []
        for t in tokens[:3]:
            if t in ATOMIC_HI_PARTS:
                parts.append(ATOMIC_HI_PARTS[t])
            elif t in HI_SOUND_ALIKES:
                parts.append(f"{t.capitalize()}")
            else:
                parts.append(t.capitalize())
        joined_parts = " + ".join(parts) if parts else hi_cap
        ta_part = f" + <strong>Tamil {ta_short}</strong>" if ta_short else ""
        return f"{header} ≈ <strong>{joined_parts}</strong>{ta_part} → Combine the parts for <em>{word.title()} ({hi_cap})</em>!"

    # 4. Build phonetic sound-alike + Tamil bridge for native Hindi word/phrase
    prefix2 = hi_clean[:2]
    syl_cue = SYL_MAP.get(prefix2, hi_cap)
    ta_part = f"<strong>Tamil {tamil}</strong> + " if tamil else ""
    return f'{header} ≈ {ta_part}Sounds like <strong>"{syl_cue} ({hi_cap})"</strong> → Everyday spoken Hindi for <em>{word.title()} ({hi_cap})</em>!'


with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Also fix the 2 bare '+' cards (#106 WHATEVER, #107 WHENEVER) in tier1_200DeckCards
for dname in ["tier1_200DeckCards", "tier101DeckCards"]:
    for kw in ["var ", "const ", "let "]:
        prefix = f"{kw}{dname} = "
        start_idx = content.find(prefix)
        if start_idx != -1:
            break
    if start_idx == -1:
        continue
    json_start = start_idx + len(prefix)
    end_idx = content.find(";\n", json_start)
    cards = json.loads(content[json_start:end_idx])
    for c in cards:
        if c.get("num") == 106:
            c["shortcutEs"] = '<strong>Lo que sea (Loh keh seh-ah)</strong> ≈ <strong>Lo que (What) + Sea ("Say-Ah" / May be)</strong> → Whatever may be = <em>WHATEVER (Lo que sea)</em>!'
            c["shortcutHi"] = '<strong>Jo bhi ho (जो भी हो)</strong> ≈ <strong>Jo (What) + Bhi ("Be") + Ho (Happens)</strong> → Come what may = <em>WHATEVER (Jo bhi ho)</em>!'
        elif c.get("num") == 107:
            c["shortcutEs"] = '<strong>Cuando sea (Kwan-doh seh-ah)</strong> ≈ <strong>Cuando ("When") + Sea (Anytime)</strong> → At any time = <em>WHENEVER (Cuando sea)</em>!'
            c["shortcutHi"] = '<strong>Jab bhi (जब भी)</strong> ≈ <strong>Jab (When) + Bhi (Ever)</strong> → Anytime you want = <em>WHENEVER (Jab bhi)</em>!'
    content = content[:json_start] + json.dumps(cards, ensure_ascii=False) + content[end_idx:]

decks_1001_3000 = [
    "tier1001DeckCards", "tier1201DeckCards", "tier1401DeckCards",
    "tier1601DeckCards", "tier1801DeckCards", "tier2001DeckCards", "tier2501DeckCards"
]

total_upgraded = 0
for dname in decks_1001_3000:
    prefix = f"var {dname} = "
    start_idx = content.find(prefix)
    if start_idx == -1:
        continue
    json_start = start_idx + len(prefix)
    end_idx = content.find(";\n", json_start)
    cards = json.loads(content[json_start:end_idx])

    for c in cards:
        w = c.get("word", "").strip().upper()
        # 1. Restore clean modern daily spoken Hindi if polluted
        if w in SPOKEN_HI_PAIRS:
            c["trans"]["hi"] = SPOKEN_HI_PAIRS[w]
        elif w in RAW_TXT_HI and RAW_TXT_HI[w]:
            # Check if current trans.hi was polluted with Sanskrit/Tamil/Spanish by enrich_hindi_translations
            cur_hi = c["trans"].get("hi", "")
            if "/" in cur_hi or any(bad in cur_hi for bad in ["vaankoli", "kanavai", "alcaide", "pasillo", "desfase", "shyaampatt", "praadhyapak", "pradhanacharya", "ashtapaad", "upayogkarta", "viraam-ghadi", "up-sheershak", "swayam-seva", "vimaan", "mudra"]):
                c["trans"]["hi"] = RAW_TXT_HI[w]

        # 2. Build 800-1000 style ≈ shortcuts for both Spanish & Hindi
        c["shortcutEs"] = build_shortcut_es(c)
        c["shortcutHi"] = build_shortcut_hi(c)
        total_upgraded += 1

    new_json = json.dumps(cards, ensure_ascii=False)
    content = content[:json_start] + new_json + content[end_idx:]
    print(f"Upgraded {len(cards)} cards in {dname}")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)

print(f"Successfully upgraded {total_upgraded} cards in 1001-3000 to the 800-1000 ≈ standard!")
