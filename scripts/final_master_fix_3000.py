#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master Overhaul Script for All 3,000 Flashcards:
1. Authentic Roman Hindi FIRST on all 3,000 cards (0 English-only / English-first Hindi translations, 0 Devanagari).
2. 100% Real Sound-Alike / Tamil / Root Shortcuts for EVERY card (1-3000) and EVERY sense (1 & 2) of multi-meaning cards.
   - Zero proverbs, idioms, superstitions, movie/song titles, obscure words, or bare explanations.
   - Exact user-requested hooks for ATMOSPHERE (#1021), SPACE (#1022), MUD (#1032), HILL (#1038), PLAIN (#1043).
3. Batch Wikipedia PageImages resolver for concept-accurate photos across all 3,000 cards.
"""

import json
import os
import re
import sys
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from es_hooks_data import ES_SOUND_ALIKES
from hi_hooks_data import HI_SOUND_ALIKES

# ============================================================================
# 1. AUTHENTIC ROMAN HINDI OVERRIDES (Ensures Hindi word is ALWAYS first!)
# ============================================================================
AUTHENTIC_HI_FIRST = {
    225: "ungli pherna / swipe karna",
    292: "pal / kshan (or minute)",
    334: "bulaana / phone karna",
    347: "shuru karna / aarambh karna",
    368: "lagana / sthaapit karna",
    371: "aage chalna / netritva karna",
    379: "ijaazat dena / anumati dena",
    385: "pesh karna / prastaav dena",
    443: "sekna (or bake karna)",
    459: "jaanch karna (or check karna)",
    571: "aakarshak / sundar (or handsome)",
    584: "swasth / tandurust",
    604: "sone ka kamra (or bedroom)",
    605: "snaanghar / gusal-khana (or bathroom)",
    644: "chachera / mamera bhai-behen (or cousin)",
    693: "twacha / khaal",
    716: "vaidya / chikitsak (or doctor)",
    717: "parichaarika / upachaarika (or nurse)",
    718: "mareez / rogi",
    720: "dawakhana / chikitsalaya (or clinic)",
    730: "kahwa / kaafi (or coffee)",
    732: "shorba (or soup)",
    737: "sevaiyan (or noodles)",
    738: "sevaiyan / maida-patti (or pasta)",
    754: "do-roti nasta (or sandwich)",
    755: "meetha-pua (or cake)",
    757: "koko-mithai (or chocolate)",
    758: "kulfi / malai-barf (or ice cream)",
    767: "jhar-ber (or strawberry)",
    777: "phali / sem (or beans)",
    787: "pyaala (or cup)",
    794: "haath-rumaal (or napkin)",
    795: "thaal / parosne ki thaali (or tray)",
    1022: "1. Area: jagah / sthaan | 2. Cosmos: antariksh / aakaash",
    1040: "gehri ghaati / khand (or canyon)",
    1049: "van / jangal",
    1058: "samudra-tat / saahil (or beach)",
    1095: "padu-murga / peru-pakshi (or turkey)",
    1106: "suus-machhli (or dolphin)",
    1107: "1. Stamp: mohar / chhaap | 2. Animal: jal-vyaghra (or seal)",
    1109: "samudri-feni / dashbhuji (or squid)",
    1110: "him-pakshi (or penguin)",
    1121: "upar-neeche khiskaana (or scroll karna)",
    1122: "dabaana / chunaav karna (or click karna)",
    1124: "utaarna / praapt karna (or download karna)",
    1125: "chadhaana / bhejna (or upload karna)",
    1126: "sthaapit karna / lagana (or install karna)",
    1127: "hataana (or uninstall karna)",
    1128: "navinikaran karna / naya karna (or update karna)",
    1131: "khojna / dekhna (or browse karna)",
    1133: "prishth-nishaan (or bookmark)",
    1140: "yaad-dihani / smaran-patra",
    1142: "sachet-ghanti (or alarm)",
    1143: "samay-ganak (or timer)",
    1147: "viraam-ghadi (or stopwatch)",
    1148: "haath-batti / mashaal (or torch)",
    1150: "parda-chitra (or wallpaper)",
    1151: "ghanti ki dhun (or ringtone)",
    1152: "kaan-taar / shravan-yantra (or earphone)",
    1153: "kaan-kran / shravan-kali (or earbuds)",
    1155: "saathi / hissedaar",
    1156: "urja-kosh (or powerbank)",
    1157: "jodak-yantra (or adapter)",
    1166: "bina-taar jaal (or wifi)",
    1181: "neel-sanchaar / be-taar sampark (or bluetooth)",
    1182: "jaal-camra / drishya-yantra (or webcam)",
    1183: "ank-sanganak (or laptop)",
    1184: "phalak-sanganak (or tablet)",
    1185: "kunji-patal (or keypad)",
    1186: "sparsh-parda (or touchscreen)",
    1187: "dhwani-prasaaran (or podcast)",
    1191: "aagaman-peti (or inbox)",
    1192: "faltu-sandesh / kachra-patra (or spam)",
    1195: "mishran-yantra (or mixer)",
    1196: "sekne-yantra (or toaster)",
    1197: "taap-rodhak bartan (or thermos)",
    1220: "dabba / bhojan-patra",
    1223: "pyaala-aadhaar / chhoti-chataai (or coaster)",
    1225: "kapde dhone ka chooran / saabun",
    1226: "rang-udaane wala dravya (or bleach)",
    1228: "chilman / khidki-parda",
    1233: "kapda-tangni / khunti (or hanger)",
    1241: "baal-mulayam lepan (or conditioner)",
    1244: "durgandh-naashak / sugandh-spray",
    1269: "rekha-sanket (or barcode)",
    1270: "daam ki parchi / moolya-patra",
    1272: "ashwasan-patra / zimmedaari (or guarantee)",
    1280: "pulinda / gathri (or parcel)",
    1289: "sandesh-vaahak / daak-seva",
    1298: "meetha-cheela / maalpua (or pancake)",
    1299: "jaalidaar-pua (or waffle)",
    1302: "tikki-pav (or burger)",
    1304: "masala-roti (or pizza)",
    1305: "makke ke phoole / laava",
    1306: "khasta-roti / matthi (or biscuit)",
    1307: "pyaala-pua (or muffin)",
    1308: "meetha-vada / chhalla-roti (or donut)",
    1309: "malai-tukda (or pastry)",
    1310: "kulfi / malai-barf",
    1331: "mijaaz / manosthiti",
    1347: "gehra-udaasi / avsaad",
    1359: "doodh-sharbat (or milkshake)",
    1360: "gaadhi-kaali-kaafi (or espresso)",
    1367: "safed-chutney (or mayonnaise)",
    1373: "chatni",
    1380: "rachanaatmak / kalpana-sheel",
    1408: "mahatvaakaankshi / unche-iraade wala",
    1444: "ishqbaazi karna / nakhre dikhana",
    1446: "choomna / pyaar karna",
    1504: "pakka karna / pushti karna",
    1507: "topi-wala kurta / oon-vasta (or hoodie)",
    1519: "1. Province: rajya / praant | 2. Declare: kehna / bayaan dena",
    1523: "khula-bunai-kurta (or cardigan)",
    1527: "uddharan dena / daam bataana",
    1542: "nirdeshak / sanchaalak",
    1549: "afsar / adhikaari",
    1550: "abhiyanta (or engineer)",
    1551: "vaastukaar (or architect)",
    1552: "thekedaar",
    1554: "nal-kaariigar (or plumber)",
    1555: "bijli-mistri (or electrician)",
    1556: "yantra-mistri / kaariigar (or mechanic)",
    1558: "vimaan-chaalak (or pilot)",
    1559: "kaptaan / naayak",
    1566: "parosne-wala / bairaa (or waiter)",
    1567: "parosne-wali / sevika (or waitress)",
    1568: "rasoiya / baawarchi",
    1574: "kalakaar",
    1575: "abhineta / naayak (or actor)",
    1576: "abhinetri / naayika (or actress)",
    1577: "sangeetkaar",
    1580: "1. Bus: parichaalak (or conductor) | 2. Music: sanchaalak",
    1581: "chitrakaar / chhaayachitrakaar (or photographer)",
    1583: "patrakaar",
    1589: "dandadhikaari / nyayadhish",
    1592: "sipahi / rakshak-dal (or police)",
    1593: "aag-bujhane wala / damkal-karmi",
    1595: "aapat-chikitsak / sahayak",
    1605: "laabh-ansh / atirikt-inaam (or bonus)",
    1609: "isteefa / tyagpatra",
    1612: "sevanivritti-vetan / masik-bhatta (or pension)",
    1614: "barsaati",
    1623: "1. Work: paali / kaam ki baari | 2. Move: khiskaana / badalna",
    1632: "vyapaar-sangh / sanstha (or company)",
    1643: "upbhokta / graahak",
    1646: "sahyogi / saathi",
    1650: "chhaap / vyapaar-naam (or brand)",
    1654: "1. Fee: shulk / daam | 2. Battery: urja bharna (or charge karna)",
    1655: "1. Invoice: hisaab-parchi / raseed | 2. Law: vidheyak (or bill)",
    1675: "aay-vyay-lekha / bajat",
    1680: "kisht",
    1684: "1. Bank: shesh-raashi (or balance) | 2. Equilibrium: santulan",
    1691: "haath-thaila / batua (or handbag)",
    1705: "1. Curiosity: ruchi / dilchaspi | 2. Bank: byaaj",
    1710: "nivesh / poonji-lagana",
    1712: "jokhim / khatra",
    1723: "khel-joote (or sneakers)",
    1728: "dhobi-ghar / kapda-dhulai kendra",
    1729: "naai ki dukaan / kesh-kendra",
    1737: "1. Law: adaalat / nyayalaya | 2. Sports: khel-maidaan",
    1739: "davaai ki dukaan / aushadhalaya",
    1742: "dava-vikreta / aushadh-gyata",
    1745: "1. Grammar: vaakya | 2. Law: saza / dand",
    1772: "lekhan-saamagri ki dukaan (or stationery)",
    1782: "kagaz-jodak / taar-panch (or stapler)",
    1795: "visphotak / gola (or bomb)",
    1798: "khatre ki ghanti / bhopu (or siren)",
    1801: "ujagar-kalam / chamkila-pen (or highlighter)",
    1802: "chipakne-wali parchi",
    1811: "1. Biology: koshika | 2. Room/Battery: kothri / vidyut-kosh",
    1812: "dainik-yojika / dincharya-pustika",
    1816: "likhne ki takhti / patti-phalak",
    1819: "daak-patra (or postcard)",
    1820: "patra-peti / daak-dabba",
    1830: "patri / paidal-path",
    1834: "bhoomi-path / neeche ka raasta",
    1835: "upari-pul (or flyover)",
    1838: "sansad",
    1839: "mahasabha / sansad (or congress)",
    1842: "parishad / sabha",
    1849: "mantraalaya",
    1851: "rajyapaal",
    1862: "1. Law: niyam / kanoon | 2. Govern: shasan karna / raaj karna",
    1867: "matdaan karna / mat dena (or vote dena)",
    1873: "umeedwaar / pratyashi",
    1874: "naamit-umeedwaar",
    1875: "prathamik / mukhya",
    1879: "1. Direction/Correct: sahi / daahina | 2. Legal: adhikaar / haq",
    1886: "1. Month: chaitra / maarch-maah | 2. Parade: juloos / kadam-taal",
    1918: "kaaraagaar-adhyaksh / bandi-paal (or warden)",
    1922: "dootavaas",
    1924: "raajdoot",
    1944: "fauj / thal-sena",
    1945: "nausena / jal-sena",
    1953: "yuddhaviraam / goli-bandi",
    1964: "sampadakiya-lekh",
    1967: "prasaaran karna",
    1968: "kala-kaksh / chitrashala (or studio)",
    1998: "vidya-peeth / shiksha-sanstha (or academy)",
    1999: "chhaatra / vidyarthi",
    2001: "shikshak / adhyapak (or teacher)",
    2002: "praadhyapak / aachaarya (or professor)",
    2003: "noshikshak / ghar-adhyapak (or tutor)",
    2004: "pradhaanaachaarya / pramukh (or principal)",
    2005: "prashikshak (or instructor)",
    2006: "sahpaathi (or classmate)",
    2007: "kaksha / paathshala-kamra (or classroom)",
    2008: "shyaampatt / kaala-phalak (or blackboard)",
    2009: "shwet-phalak / safed-board (or whiteboard)",
    2010: "khadiya / chaak (or chalk)",
    2011: "mota-kalam / nishaan-pen (or marker)",
    2014: "likhne ki kaapi / pustika (or notebook)",
    2015: "abhyas-pustika (or workbook)",
    2016: "patra-bandhak / jild (or binder)",
    2017: "patra-dhaarak / lifafa-patti (or folder)",
    2018: "1. Doc: nathi / dastaavez (or file) | 2. Tool: reti",
    2019: "dastaavez / pralekh (or document)",
    2020: "kalam / lekhani (or pen)",
    2021: "kachchi-kalam / sees-lekhani (or pencil)",
    2023: "1. Direction: disha-soochak | 2. Geometry: parkaar",
    2024: "paath / sabak (or lesson)",
    2025: "vyakhyan / bhashan (or lecture)",
    2026: "sangoshthi / charcha-sabha (or seminar)",
    2027: "grihakarya / ghar ka kaam",
    2028: "saunpa-karya / niyat-kaam (or assignment)",
    2029: "nibandh / lekh (or essay)",
    2030: "prashnottari (or quiz)",
    2031: "pariksha / imtihaan (or exam)",
    2032: "1. Score: shreni / ank | 2. Level: darja / kaksha",
    2033: "praaptaank / kul-ank (or score)",
    2034: "chhah-maahi satr / ardha-vaarshik (or semester)",
    2035: "1. Period: avadhi / satr | 2. Word: shabd / shart",
    2036: "paathyakram-rooprekha (or syllabus)",
    2037: "paathyakram / shiksha-kram (or curriculum)",
    2038: "chhatravritti / vazifa",
    2039: "1. Fee: shiksha-shulk | 2. Coaching: anushikshan / tyooshan",
    2040: "upadhi-patra / pramaan-patra (or diploma)",
    2041: "1. Academic: upadhi | 2. Temp/Angle: ansh (or degree)",
    2042: "pramaan-patra (or certificate)",
    2043: "snaatak-samaaroh / upadhi-praapti (or graduation)",
    2044: "parisar / vishwavidyalaya-kshetra (or campus)",
    2045: "chhaatraavaas (or hostel)",
    2046: "sabhagaar / rangmanch-bhavan (or auditorium)",
    2047: "shodh-prabandh (or thesis)",
    2049: "shodh / khoj (or research)",
    2050: "shodh-karta / khoj-karta (or researcher)",
    2055: "bhoogol",
    2057: "ganit",
    2058: "beej-ganit (or algebra)",
    2059: "rekha-ganit / jyaamiti (or geometry)",
    2060: "ohda / darja / sthaan (or rank)",
    2061: "bhautik-vigyan (or physics)",
    2062: "khagol-vigyan",
    2063: "rasaayan-vigyan (or chemistry)",
    2065: "jeev-vigyan (or biology)",
    2068: "darshan-shastra",
    2070: "manovigyan (or psychology)",
    2073: "arthashastra",
    2076: "vyakaran",
    2077: "shabdavali / shabd-bhandaar (or vocabulary)",
    2078: "prayogshala (or laboratory)",
    2079: "prayog-kaksh (or lab)",
    2081: "parikalpana / anumaan",
    2084: "tareeqa / vidhi",
    2087: "aavishkaar / khoj",
    2091: "vishleshan / jaanch",
    2094: "saankhyiki / aakde",
    2096: "avlokan / ghaur se dekhna",
    2099: "samikaran",
    2106: "parmanu",
    2113: "oorja / taakat",
    2114: "1. Power: bal / taakat | 2. Compel: majboor karna",
    2115: "gurutvakarshan / khinchaav",
    2118: "pal mein badalne wala / manmauji",
    2120: "1. Physics: dravyamaan / bhaar | 2. Crowd: bheed",
    2122: "1. Sound: aawaaz | 2. 3D Space: aayatan",
    2129: "1. Flow: dhaara / bijli-pravaah | 2. Present: vartamaan / abhi ka",
    2130: "vidyut-dabav / vibhavantar (or voltage)",
    2140: "ankiya (or digital)",
    2141: "vidyutiy (or electronic)",
    2143: "parda / chitra-patal (or screen)",
    2144: "pradarshak-parda / nigrani-yantra (or monitor)",
    2145: "kunji-patal (or keyboard)",
    2146: "mudrak-yantra / chhaapne ki machine (or printer)",
    2147: "chitra-paathak / pratilipi-yantra (or scanner)",
    2148: "chitra-prakshepak / parda-yantra (or projector)",
    2150: "1. Audio: dhwani-yantra (or speaker) | 2. Person: vakta / bolne wala",
    2151: "shravan-yantra / kaan-yantra (or headphone)",
    2153: "urja-bharak (or charger)",
    2154: "mota-taar (or cable)",
    2155: "lohe-ka-saamaan / bhaari-upkaran (or hardware)",
    2156: "karya-pranaali / tantraansh (or software)",
    2157: "karyakram / yojana (or program)",
    2158: "sanket-lipi / gupt-sanket (or code)",
    2159: "ganana-vidhi / niyam-kram (or algorithm)",
    2160: "sampark-jaal / sanchaar-jaal (or network)",
    2161: "kendriya-sanganak / seva-daata (or server)",
    2162: "bhandaaran / sangrah-sthaan (or storage)",
    2163: "yaaddaasht / smriti (or memory)",
    2165: "sookshma-patal / tukda (or chip)",
    2166: "sanchaalak-kendra (or processor)",
    2167: "ishaara / sanket (or signal)",
    2168: "upagrah (or satellite)",
    2169: "upkaran / yantra (or device)",
    2178: "halka-dhatu / elyuminiyam (or aluminum)",
    2184: "jodne-wala chooran / vajra-chooran (or cement)",
    2185: "thos-gitty-mishran / pakka-masala (or concrete)",
    2186: "diwaar-lep / palastar (or plaster)",
    2192: "lachila-padaarth / plaastik (or plastic)",
    2200: "san-ka-kapda / katan (or linen)",
    2204: "mota-neela-sooti kapda (or denim)",
    2205: "kritrim-taar-resha (or nylon)",
    2206: "kritrim-kapda-resha (or polyester)",
    2220: "pradarshani / numaish",
    2228: "sangeet-naatak (or musical)",
    2239: "1. Actors: kalakaar-mandali | 2. Throw: phenkna / daalna",
    2249: "1. Ruler: phoota / paimaana | 2. Weight: tarazu",
    2250: "1. Written/Money: tippani / kagaz-mudra (or note) | 2. Music: sur",
    2253: "1. Rhythm: taal / dhadkan | 2. Defeat: haraana / peetna",
    2261: "vrind-sangeet / maha-dhun (or symphony)",
    2262: "1. Music: vaadya-dal (or band) | 2. Strip: patti / bandhan",
    2266: "taar-vaadya / gitaar (or guitar)",
    2267: "sur-peti (or piano)",
    2268: "sarangi / bela (or violin)",
    2273: "dawai ki goli / sampoot (or capsule)",
    2277: "darj karna / abhilekh (or record)",
    2284: "pair-gend khel (or football)",
    2286: "tokri-gend khel (or basketball)",
    2287: "balla-daud khel (or baseball)",
    2288: "jaal-gend khel (or tennis)",
    2289: "haath-gend khel (or volleyball)",
    2290: "andaakaar-gend khel (or rugby)",
    2291: "haaki-khel / mud-danda khel (or hockey)",
    2292: "gaddha-gend khel (or golf)",
    2295: "balla-gend khel (or cricket)",
    2296: "chidi-chhakka (or badminton)",
    2298: "lambi-daud (or marathon)",
    2300: "pahiya-patra khel (or skateboarding)",
    2302: "barf-phalak khel (or snowboarding)",
    2303: "pahiya-joota daud (or skating)",
    2310: "gend-giraana khel (or bowling)",
    2316: "1. Speed: daud (or race) | 2. Ethnicity: jaati / nasl",
    2319: "khel-sangh / mandal (or league)",
    2339: "ghoornak-chakka / chakri-yantra (or turbine)",
    2341: "kaaryashala / prashikshan-shivir",
    2344: "kaarya-prashikshan / shuruati-abhyas",
    2346: "koila-tatva / kaarban (or carbon)",
    2348: "kaanch-ghar / paudha-ghar (or greenhouse)",
    2350: "raksha-vaayu / ozon-parat (or ozone)",
    2358: "punarchakran karna / dobara upyog banana",
    2365: "prashikshu / naya-seekhne wala",
    2382: "1. Steady: sthir / pakka | 2. Horse: astabal / ghudsaal",
    2384: "raay / pratikriya",
    2385: "khet-gaadi / hal-yantra (or tractor)",
    2390: "chitra-pradarshan (or presentation)",
    2391: "talika-patra / hisaab-panna",
    2405: "khaad / urvarak",
    2407: "keetnaashak-dawa",
    2423: "lachakdaar-feeta / rabad-patti (or elastic)",
    2453: "sadasyata / chanda (or subscription)",
    2462: "saamagri / masale",
    2467: "shuruati-nasta / alpahaar (or starter)",
    2478: "sajaana / upar se dhaniya-masala daalna",
    2486: "navikaran / avadhi-badhaana",
    2489: "chhaantna / barabar kaatna",
    2490: "1. Pin: chimti / patti-pin | 2. Cut: chhaantna / kaatna",
    2493: "chamkaana / roghan lagana",
    2496: "dhool-kheench machine se saaf karna",
    2497: "paani bahaana",
    2526: "shalya-chikitsa / cheer-phaad (or operation)",
    2527: "1. Medical: shalya-chikitsa (or operation) | 2. Action: kaaryavaahi / sanchaalan",
    2528: "sui-pichkaari / teeka-yantra (or syringe)",
    2530: "taap-maapi / bukhaar-naapne ka yantra (or thermometer)",
    2531: "dhadkan-sunne ka yantra / aalaa (or stethoscope)",
    2532: "samvedak-yantra (or sensor)",
    2534: "dhwani-jaanch / garbh-chitra (or ultrasound)",
    2535: "rog-pehchaan / jaanch",
    2545: "jeevaanu-naashak dawa (or antibiotic)",
    2546: "sankraman-rodhak dawa (or antiseptic)",
    2550: "dard-nivaarak goli",
    2551: "teeka",
    2552: "rogi-vaahan (or ambulance)",
    2553: "rogi-khatiya / doli-patti (or stretcher)",
    2554: "pahiya-kursi (or wheelchair)",
    2556: "haath-latkaane ki patti / gal-patti",
    2558: "manochikitsa-vigyan (or psychiatry)",
    2570: "gehra-dar / bhay-rog (or phobia)",
    2585: "ghamand / ahankaar",
    2591: "milansaar / bahirmukhi",
    2597: "1. Land: zameen ka tukda / bhookhand | 2. Story: katha-vastu / saazish",
    2625: "naya-roop dena / punarnirmaan karna",
    2628: "jaanch / nirikshan",
    2629: "sanganak-chor / sendh-maarne wala (or hacker)",
    2634: "belt-kunda / baksun (or buckle)",
    2650: "chalu karna / batti jalaana",
    2651: "band karna / batti bujhaana",
    2747: "aapka parivaar kaisa hai?",
    2861: "yantra-patal / aage ka phalak (or dashboard)",
    2863: "sheesha-saaf karne wala (or wiper)",
    2867: "gati-vardhak / race-pedal (or accelerator)",
    2868: "pakad-pedal / klach (or clutch)",
    2869: "daantedaar-chakka / giyar (or gear)",
    2873: "takkar-rodhak / aage ki patti (or bumper)",
    2875: "pahiya-danda / dhuri (or axle)",
    2885: "saajha-sawaari (or rideshare)",
    2886: "saajha-kaar-yatra (or carpool)",
    2887: "sawaari-lena / uthaana (or pickup)",
    2888: "manzil par chhodna / utaarna (or drop-off)",
    2889: "disha-chakra / stearing-chakka (or steering)",
    2890: "peechhe dekhne ka sheesha",
    2891: "bagal ka sheesha",
    2892: "path-kar / chungi (or toll)",
    2893: "ghumaavdaar-badla-raasta (or detour)",
    2894: "yaatayaat-jaam / gaadiyon ki bheed",
    2895: "andekha-kona / chhipa-sthaan",
    2896: "vimaan-pravesh-patra (or boarding pass)",
    2897: "shulk-vibhaag / seema-jaanch (or customs)",
    2898: "vimaan-bhavan / aakhri-sthaan (or terminal)",
    2899: "udaan-patti / hawai-patti (or runway)",
    2900: "chaalak-kaksh (or cockpit)",
    2901: "vimaan-parichaarika / hawai-sevak",
    2903: "yaatra-saamaan / bori-bistar (or baggage)",
    2905: "aarakshan / pehle se jagah rokhna",
    2906: "aarakshan / darj-karana (or booking)",
    2908: "paryatak / sailaani (or tourist)",
    2909: "paryatan / sair-sapaata (or tourism)",
    2910: "darshaniya-sthal dekhna / ghoomna",
    2911: "yaadgaar-tohfa / nishaani (or souvenir)",
    2912: "prasthaan / ravaangi (or departure)",
    2913: "aagaman / pahunchna (or arrival)",
    2915: "radd-karna / niraakaran (or cancellation)",
    2916: "swaagat-kaksh / poochhtaachh-patal (or reception)",
    2917: "swaagat-mej / mukhya-patal",
    2918: "chumbakiya-chaabi-patra (or keycard)",
    2919: "kamra-seva / bhojan-seva",
    2920: "kamra-safaai vibhaag",
    2921: "pravesh-anumati-patra (or visa)",
    2922: "pravaas-jaanch / desh-pravesh vibhaag",
    2923: "paasport-jaanch kendra",
    2924: "atirikt-bhaar saamaan",
    2925: "beech ka thehraav / vishraam",
    2926: "chhota-padaav / rukna",
    2927: "hawai-safar ki thakaan (or jet lag)",
    2928: "mudra-badalne wala / sarraaf",
    2929: "galiyare-wali seat",
    2930: "khidki-wali seat",
    2933: "ek-samaam maanak banana",
    2935: "bhavishyavaani karna / andaaza lagana",
    2939: "taalmel bithaana / sanyojan karna",
    2940: "dekh-rekh karna / nigrani karna",
    2945: "behtar banana / darja badhaana (or upgrade karna)",
    2966: "samiksha karna / dobara jaanchna",
    2968: "gunvatta / khasiyat (or quality)",
    2970: "maanak / star (or standard)",
    2971: "sahaayata-sampark number (or helpline)",
    2972: "jeevan-rakshak / tairaak-rakshak",
    2975: "suraksha-rakshak / pehredaar",
    2977: "kshamta / gunjaish",
    2978: "seema / hadd",
    2981: "kam se kam / nyoonatam",
    2988: "chaukidaar / pehredaar",
    2991: "asthaayi / kuchh samay ka",
    2993: "dekhbhaal karne wala / rakhwala",
    2994: "gatisheel / urjavaan (or dynamic)",
}

# ============================================================================
# 2. CLEANUP OBSCURE / PROVERB / IDIOM / MOVIE HOOKS IN ES_SOUND_ALIKES & HI_SOUND_ALIKES
# ============================================================================
CLEAN_ES_OVERRIDES = {
    "barro": '<strong>Barro</strong> ≈ Sounds like <strong>"Wheel-Barrow"</strong> → Pushing a wheelbarrow stuck in wet sticky <em>Mud (Barro)</em>!',
    "colina": '<strong>Colina</strong> ≈ Sounds like <strong>"Collide"</strong> → Imagine a boulder or car about to <em>collide</em> into a steep green <em>Hill (Colina)</em>!',
    "llanura": '<strong>Llanura (Yah-noo-rah)</strong> ≈ Sounds like <strong>"Lawn-Area"</strong> → Wide flat grassy <em>Plain (Llanura)</em>!',
    "ciervo": '<strong>Ciervo (Syer-voh)</strong> ≈ Sounds like <strong>"Swerve-Oh!"</strong> → Swerve your car on a forest road so you don\'t hit a <em>Deer (Ciervo)</em>!',
    "conejo": '<strong>Conejo (Koh-neh-hoh)</strong> ≈ Sounds like <strong>"Cone-Ho!"</strong> → A cute fluffy <em>Rabbit (Conejo)</em> nibbling an ice-cream cone!',
    "cuervo": '<strong>Cuervo (Kwer-voh)</strong> ≈ Sounds like <strong>"Curve-Oh"</strong> → A black <em>Crow (Cuervo)</em> flying around a sharp curve!',
    "abeja": '<strong>Abeja (Ah-beh-hah)</strong> ≈ Sounds like <strong>"A-Bee-Ha!"</strong> → Hear the buzzing of a honey <em>Bee (Abeja)</em>!',
    "hormiga": '<strong>Hormiga (Or-mee-gah)</strong> ≈ Sounds like <strong>"Army-Go"</strong> → A marching army of tiny <em>Ants (Hormiga)</em>!',
    "redondo": '<strong>Redondo</strong> ≈ Sounds like <strong>"Round-O"</strong> → Shaped like a big round O = <em>Round (Redondo)</em>!',
    "asentir": '<strong>Asentir</strong> ≈ Sounds like <strong>"I-Sent-Here"</strong> → Nodding your head "Yes!" = <em>Nod / Agree (Asentir)</em>!',
    "burlarse": '<strong>Burlarse</strong> ≈ Sounds like <strong>"Bully-Laugh"</strong> → Laughing to <em>Tease / Mock (Burlarse)</em> someone!',
    "adular": '<strong>Adular</strong> ≈ Sounds like <strong>"Add-Love"</strong> → Showering someone with extra praise = <em>Flatter (Adular)</em>!',
    "ingresos": '<strong>Ingresos</strong> ≈ Sounds like <strong>"In-Grows"</strong> → Money that grows IN your bank account = <em>Income (Ingresos)</em>!',
    "jubilación": '<strong>Jubilación (Hoo-bee-lah-syon)</strong> ≈ Sounds like <strong>"Jubilation!"</strong> → Joyful celebration when you reach <em>Retirement (Jubilación)</em>!',
    "rotonda": '<strong>Rotonda</strong> ≈ Sounds like <strong>"Rotate-Round"</strong> → Cars rotating in a circle = <em>Roundabout (Rotonda)</em>!',
    "polvo": '<strong>Polvo</strong> ≈ Sounds like <strong>"Powder-Bowl"</strong> → Fine dry powder floating in the air = <em>Dust (Polvo)</em>!',
    "podrido": '<strong>Podrido</strong> ≈ Sounds like <strong>"Pot-Ridden"</strong> → Old food left in a pot gone bad = <em>Rotten (Podrido)</em>!',
    "torpe": '<strong>Torpe (Tor-peh)</strong> ≈ Sounds like <strong>"Trip-Up"</strong> → Tripping over your own feet = <em>Clumsy / Awkward (Torpe)</em>!',
    "delito": '<strong>Delito</strong> ≈ Sounds like <strong>"Delete-Law"</strong> → Breaking the law is a <em>Crime / Offense (Delito)</em>!',
    "soborno": '<strong>Soborno</strong> ≈ Sounds like <strong>"So-Bought-Now"</strong> → Secretly buying someone off under the table = <em>Bribe (Soborno)</em>!',
}

CLEAN_HI_OVERRIDES = {
    "vaataavaran": '<strong>Vaataavaran</strong> ≈ Sounds like Tamil <strong>சுற்றுவட்டாரம் (Suttru-vattaaram = surroundings)</strong> → Surrounding air &amp; <em>Atmosphere (Vaataavaran)</em>!',
    "keechad": '<strong>Keechad</strong> ≈ Sounds like <strong>"Keychain"</strong> → Imagine your <em>keychain</em> falling into wet sticky <em>Mud (Keechad)</em>!',
    "pahaadi": '<strong>Pahaadi</strong> ≈ <strong>Pahaad</strong> (Mountain) + <strong>-i</strong> (Small/Mini) → Small green <em>Hill (Pahaadi)</em>!',
    "maidaan": '<strong>Maidaan</strong> ≈ Same as Tamil <strong>மைதானம் (Maidaanam = open ground/field!)</strong> → Wide flat <em>Plain (Maidaan)</em>!',
    "bandar": '<strong>Bandar</strong> ≈ Same as spoken Tamil <strong>"பந்தர் / குரங்கு"</strong> (or sounds like <strong>"Bungee-Jumper"</strong>) → Jumping from tree to tree like a <em>Monkey (Bandar)</em>!',
    "kabootar": '<strong>Kabootar</strong> ≈ Sounds like <strong>"Scooter"</strong> (Ka-bootar / Scooter) → A grey <em>Pigeon (Kabootar)</em> sitting on a parked scooter!',
    "udaas": '<strong>Udaas</strong> ≈ Sounds like <strong>"Oh-Das-Sad!"</strong> → Feeling down and gloomy = <em>Sad (Udaas)</em>!',
    "chumbak": '<strong>Chumbak</strong> ≈ From <strong>Choomna</strong> (to kiss/stick tightly) + <strong>"Come-Back"</strong> → Iron nails sticking right back to a <em>Magnet (Chumbak)</em>!',
    "geet": '<strong>Geet</strong> ≈ Same as Tamil <strong>கீதம் (Geetham = melody/song!)</strong> → Sweet musical <em>Song (Geet)</em>!',
    "gaana": '<strong>Gaana</strong> ≈ Same as Tamil <strong>கானா பாடல் (Gaana song!)</strong> → Singing a <em>Song (Gaana)</em>!',
    "bachaao": '<strong>Bachaao</strong> ≈ From <strong>Bachna</strong> (to be safe) → Shouting "Save me / Rescue!" = <em>Rescue / Save (Bachaao)</em>!',
    "dulhan": '<strong>Dulhan</strong> ≈ Sounds like <strong>"Doll-In-Henna"</strong> → Dressed like a glowing doll in wedding henna = <em>Bride (Dulhan)</em>!',
    "dulha": '<strong>Dulha</strong> ≈ Pair with <strong>Dulhan</strong> (Bride) → The wedding <em>Groom (Dulha)</em>!',
    "junoon": '<strong>Junoon</strong> ≈ Sounds like <strong>"June-Noon"</strong> → Blazing hot like June noon sun = fiery <em>Passion / Obsession (Junoon)</em>!',
    "sabr": '<strong>Sabr</strong> ≈ Sounds like <strong>"Sober &amp; Steady"</strong> → Staying calm and waiting = <em>Patience (Sabr)</em>!',
    "sadma": '<strong>Sadma</strong> ≈ Starts with English <strong>"SAD" + "Ma"</strong> → A sudden heavy emotional <em>Shock / Trauma (Sadma)</em>!',
    "anadi": '<strong>Anadi</strong> ≈ Sounds like <strong>"Un-Ready"</strong> → A clumsy beginner who is un-ready = <em>Amateur / Clumsy (Anadi)</em>!',
    "masoom": '<strong>Masoom</strong> ≈ Same as Tamil/Urdu loan <strong>மசூம்</strong> (or sounds like <strong>"Ma-So-Sweet"</strong>) → Pure and <em>Innocent (Masoom)</em>!',
    "thappad maarna": '<strong>Thappad maarna</strong> ≈ <strong>"Thap!"</strong> (sound of a flat hand clap) → To <em>Slap (Thappad maarna)</em>!',
    "tareef karna": '<strong>Tareef karna</strong> ≈ Sounds like <strong>"Tariff-Free"</strong> → Giving generous <em>Praise / Compliment (Tareef)</em>!',
    "ailaan karna": '<strong>Ailaan karna</strong> ≈ Sounds like <strong>"Airline-Announcement"</strong> → Making a public <em>Announcement / Declare (Ailaan karna)</em>!',
    "gaayak": '<strong>Gaayak</strong> ≈ Same root as Tamil <strong>காயகர் (Gaayakar = singer)</strong> + <strong>Gaana</strong> (Song) → <em>Singer (Gaayak)</em>!',
    "karz": '<strong>Karz</strong> ≈ Sounds like <strong>"Cars-On-Loan"</strong> (or Tamil <strong>கடன் = Kadan</strong>) → Money borrowed on loan = <em>Debt / Loan (Karz)</em>!',
    "sarkaar": '<strong>Sarkaar</strong> ≈ Used in Tamil too (<strong>சர்க்கார் = Sarkaar</strong>) → The ruling <em>Government (Sarkaar)</em>!',
    "tinka": '<strong>Tinka</strong> ≈ Sounds like <strong>"Thin-Straw"</strong> (Tin-ka) → A tiny dry piece of <em>Straw (Tinka)</em>!',
    "madham": '<strong>Madham</strong> ≈ Sounds like <strong>"Medium-Dim"</strong> (or Tamil <strong>மந்தம் = Mandham / dull</strong>) → Soft, low, <em>Dim (Madham)</em> light!',
    "dard": '<strong>Dard</strong> ≈ Sounds like <strong>"Dart"</strong> → A sharp dart hitting your skin causes <em>Pain / Ache (Dard)</em>!',
    "dhun": '<strong>Dhun</strong> ≈ Sounds like humming <strong>"Thun-Thun / Tune"</strong> → Humming a catchy musical <em>Tune / Melody (Dhun)</em>!',
    "manzil": '<strong>Manzil</strong> ≈ Sounds like <strong>"Main-Hill"</strong> → Reaching the top hill at the end of your journey = <em>Destination / Goal (Manzil)</em>!',
    "saathi": '<strong>Saathi</strong> ≈ From <strong>Saath</strong> (Together) → The person who walks together with you = <em>Companion / Partner (Saathi)</em>!',
    "dushman": '<strong>Dushman</strong> ≈ Sounds like <strong>"Push-Man"</strong> (or Tamil <strong>துஷ்டன் = Dushtan / villain</strong>) → Sworn <em>Enemy (Dushman)</em>!',
    "dosti": '<strong>Dosti</strong> ≈ From <strong>Dost</strong> (Friend, used in spoken Tamil <strong>"தோஸ்த்"</strong>!) → Warm <em>Friendship (Dosti)</em>!',
    "khushi": '<strong>Khushi</strong> ≈ From <strong>Khush</strong> (Happy, used in spoken Tamil <strong>"குஷி = Kushi"</strong>!) → Pure joy and <em>Happiness (Khushi)</em>!',
    "qaidi": '<strong>Qaidi</strong> ≈ Same as spoken Tamil <strong>கைதி (Kaidhi = Prisoner!)</strong> → A locked-up <em>Prisoner (Qaidi)</em>!',
    "duniya": '<strong>Duniya</strong> ≈ Used in spoken Tamil <strong>"துனியா (Duniya = World!)"</strong> → The whole <em>World (Duniya)</em>!',
}

# Normalize 2-tuple entries in ES_SOUND_ALIKES and HI_SOUND_ALIKES into clean HTML strings
for k, v in list(ES_SOUND_ALIKES.items()):
    if isinstance(v, (tuple, list)) and len(v) == 2:
        k_cap = k[:1].upper() + k[1:]
        ES_SOUND_ALIKES[k] = f"<strong>{k_cap}</strong> ≈ {v[0]} → {v[1]}!"

for k, v in list(HI_SOUND_ALIKES.items()):
    if isinstance(v, (tuple, list)) and len(v) == 2:
        k_cap = k[:1].upper() + k[1:]
        # Strip unrelated "+ <strong>Tamil <pure tamil word without phonetic match></strong>"
        b0 = re.sub(r"\s*\+\s*<strong>Tamil\s+[\u0B80-\u0BFF\s/()]+</strong>", "", str(v[0]))
        b1 = re.sub(r"Famous Bollywood song word for the", "Everyday word for the", str(v[1]))
        HI_SOUND_ALIKES[k] = f"<strong>{k_cap}</strong> ≈ {b0} → {b1}!"

ES_SOUND_ALIKES.update(CLEAN_ES_OVERRIDES)
HI_SOUND_ALIKES.update(CLEAN_HI_OVERRIDES)

# Strip any trailing "+ Tamil ..." that was artificially glued onto HI_SOUND_ALIKES
for k, v in list(HI_SOUND_ALIKES.items()):
    v_clean = re.sub(r"\s*\+\s*Tamil\s+[\u0B80-\u0BFF\s/()A-Za-z-]+(?=\s*→)", "", str(v))
    HI_SOUND_ALIKES[k] = v_clean

# ============================================================================
# 3. EXTRA SOUND-ALIKE HOOKS FOR CARDS 1-1000 & NEW HINDI TRANSLATIONS
# ============================================================================
EXTRA_HI_HOOKS = {
    # Verbs & Adjectives & Nouns in 1-1000
    "dekhna": '<strong>Dekhna</strong> ≈ Sounds like <strong>"Deck-Now"</strong> → Stand on the ship\'s deck now to <em>See / Look (Dekhna)</em>!',
    "milna": '<strong>Milna</strong> ≈ Sounds like <strong>"Mill-Now"</strong> → Meet your friend at the coffee mill = <em>Meet / Find (Milna)</em>!',
    "dhoondhna": '<strong>Dhoondhna</strong> ≈ Sounds like <strong>"Dune"</strong> → Searching across desert sand dunes = <em>Search / Find (Dhoondhna)</em>!',
    "mehsoos karna": '<strong>Mehsoos karna</strong> ≈ Sounds like <strong>"My-Shoes"</strong> → Feel the soft cushion inside your shoes = <em>Feel (Mehsoos karna)</em>!',
    "girna": '<strong>Girna</strong> ≈ Sounds like <strong>"Gear-Now"</strong> → Dropping a heavy gear on the floor = <em>Fall (Girna)</em>!',
    "udna": '<strong>Udna</strong> ≈ Sounds like <strong>"Up-Now"</strong> (Ud-na) → A bird soaring up into the sky = <em>Fly (Udna)</em>!',
    "tairna": '<strong>Tairna</strong> ≈ Sounds like <strong>"Tire-Now"</strong> → Floating on a rubber tire tube in the pool = <em>Swim (Tairna)</em>!',
    "koodna": '<strong>Koodna</strong> ≈ Sounds right like Tamil <strong>குதி (Kudhi = Jump!)</strong> → <em>Jump (Koodna)</em> high!',
    "muskurana": '<strong>Muskurana</strong> ≈ Sounds like <strong>"Mask-Run"</strong> → Take off the mask and show a bright <em>Smile (Muskurana)</em>!',
    "soonghna": '<strong>Soonghna</strong> ≈ Sounds like <strong>"Song-Nose"</strong> → Breathing in through your nose to <em>Smell (Soonghna)</em>!',
    "chakhna": '<strong>Chakhna</strong> ≈ Sounds like <strong>"Check-Now"</strong> → Taste a spoon of curry to check the salt = <em>Taste (Chakhna)</em>!',
    "chauda": '<strong>Chauda</strong> ≈ Sounds like <strong>"Chowder-Bowl"</strong> → A wide, broad bowl = <em>Wide / Broad (Chauda)</em>!',
    "patla": '<strong>Patla</strong> ≈ Sounds like <strong>"Petal"</strong> → Thin and delicate like a flower petal = <em>Thin / Narrow (Patla)</em>!',
    "kalaai": '<strong>Kalaai</strong> ≈ Sounds like Tamil <strong>வளையல் (Valaiyal / Kalai)</strong> worn on the hand → Your <em>Wrist (Kalaai)</em>!',
    "haddi": '<strong>Haddi</strong> ≈ Sounds like <strong>"Hard-D"</strong> → The hard calcium frame inside your body = <em>Bone (Haddi)</em>!',
    "bukhaar": '<strong>Bukhaar</strong> ≈ Sounds like <strong>"Bake-Hot"</strong> → Your forehead feels baking hot during a <em>Fever (Bukhaar)</em>!',
    "zukaam": '<strong>Zukaam</strong> ≈ Sounds like <strong>"Zoo-Calm"</strong> → Sneezing with a stuffy nose and <em>Cold (Zukaam)</em>!',
    "bulaana": '<strong>Bulaana</strong> ≈ From <strong>Bolna</strong> (to speak/call out) + sounds like <strong>"Bull-Horn"</strong> → Calling someone over = <em>Call (Bulaana)</em>!',
    "shuru karna": '<strong>Shuru karna</strong> ≈ Same as spoken Tamil <strong>"ஷுரு பண்ணு"</strong> (or sounds like <strong>"Show-Run"</strong>) → To <em>Start / Begin (Shuru karna)</em>!',
    "lagana": '<strong>Lagana</strong> ≈ Sounds like <strong>"Log-On"</strong> → Setting up or placing something in position = <em>Set / Apply (Lagana)</em>!',
    "aage chalna": '<strong>Aage chalna</strong> ≈ <strong>Aage</strong> (Ahead) + <strong>Chalna</strong> (Walk) → Walking ahead to <em>Lead (Aage chalna)</em>!',
    "ijaazat dena": '<strong>Ijaazat dena</strong> ≈ Sounds like <strong>"Easy-Exit"</strong> → Giving permission to pass = <em>Allow / Permit (Ijaazat dena)</em>!',
    "pesh karna": '<strong>Pesh karna</strong> ≈ Sounds like <strong>"Pace-Forward"</strong> → Stepping forward to present an <em>Offer (Pesh karna)</em>!',
    "sekna": '<strong>Sekna</strong> ≈ Sounds like <strong>"Shake-Naan"</strong> → Roasting bread or baking in a warm oven = <em>Bake / Roast (Sekna)</em>!',
    "jaanch karna": '<strong>Jaanch karna</strong> ≈ Sounds like <strong>"Judge-Now"</strong> → Inspecting carefully to <em>Check / Examine (Jaanch karna)</em>!',
    "aakarshak": '<strong>Aakarshak</strong> ≈ Same as Tamil/Sanskrit <strong>ஆகர்ஷணம் (Aakarshanam = attraction/charm!)</strong> → <em>Handsome / Attractive (Aakarshak)</em>!',
    "swasth": '<strong>Swasth</strong> ≈ Same as Tamil <strong>ஸ்வஸ்தம் / சுகம் (Swastham = good health!)</strong> → <em>Healthy (Swasth)</em>!',
    "twacha": '<strong>Twacha</strong> ≈ Sounds like <strong>"Touch-Ah!"</strong> → You feel every touch on your <em>Skin (Twacha)</em>!',
    "vaidya": '<strong>Vaidya</strong> ≈ Same as Tamil <strong>வைத்தியர் (Vaithiyar = Doctor!)</strong> → <em>Doctor (Vaidya / Chikitsak)</em>!',
    "parichaarika": '<strong>Parichaarika</strong> ≈ From <strong>Paricharya</strong> (caring for patients) → Hospital <em>Nurse (Parichaarika)</em>!',
    "mareez": '<strong>Mareez</strong> ≈ Sounds like <strong>"More-Ease"</strong> → A sick hospital <em>Patient (Mareez)</em> who needs rest and ease!',
    "dawakhana": '<strong>Dawakhana</strong> ≈ <strong>Dawa</strong> (Medicine) + <strong>Khana</strong> (House/Room) → Medical <em>Clinic (Dawakhana)</em>!',
    "kahwa": '<strong>Kahwa</strong> ≈ Classic Arabic/Hindi word for brewed <em>Coffee (Kahwa / Kaafi)</em> — sounds like Tamil <strong>காபி (Kaapi)</strong>!',
    "shorba": '<strong>Shorba</strong> ≈ Sounds like <strong>"Slurp-Ah!"</strong> → Slurping a hot bowl of <em>Soup / Broth (Shorba)</em>!',
    "sevaiyan": '<strong>Sevaiyan</strong> ≈ Exact same word as Tamil <strong>சேமியா / இடியாப்பம் (Semiya / Sevai!)</strong> → <em>Noodles / Pasta (Sevaiyan)</em>!',
    "kulfi": '<strong>Kulfi</strong> ≈ Everyone in Tamil Nadu &amp; India loves creamy frozen <strong>குல்ஃபி (Kulfi)</strong> = <em>Ice Cream (Kulfi)</em>!',
    "phali": '<strong>Phali</strong> ≈ From <strong>Phal</strong> (Fruit/Pod) → Green pod vegetables = <em>Beans (Phali)</em>!',
    "pyaala": '<strong>Pyaala</strong> ≈ Sounds like Tamil <strong>பியாலா / கிண்ணம்</strong> (or <strong>"Pour-All"</strong>) → A drinking <em>Cup (Pyaala)</em>!',
    "haath-rumaal": '<strong>Haath-Rumaal</strong> ≈ <strong>Haath</strong> (Hand) + <strong>Rumaal</strong> (Towel/Kerchief, Tamil <strong>ருமால்</strong>!) → Table <em>Napkin (Haath-rumaal)</em>!',
    "thaal": '<strong>Thaal</strong> ≈ Same as Tamil <strong>தாம்பாளம் / தட்டு (Thaal / Plate)</strong> → Serving <em>Tray (Thaal)</em>!',
    # Newly enriched 1001-3000 authentic Hindi words
    "gehri ghaati": '<strong>Gehri Ghaati</strong> ≈ <strong>Gehri</strong> (Deep) + <strong>Ghaati</strong> (Valley/Ghat, like Western Ghats!) → Deep <em>Canyon (Gehri Ghaati)</em>!',
    "van": '<strong>Van</strong> ≈ Same as Tamil <strong>வனம் (Vanam = Forest/Jungle!)</strong> → Dense <em>Jungle / Forest (Van / Jangal)</em>!',
    "samudra-tat": '<strong>Samudra-Tat</strong> ≈ <strong>Samudra</strong> (Tamil <strong>சமுத்திரம் = Sea</strong>) + <strong>Tat</strong> (Shore) → Sandy <em>Beach (Samudra-tat)</em>!',
    "padu-murga": '<strong>Padu-Murga</strong> ≈ Big farm fowl + <strong>Murga</strong> (Rooster/Chicken) → <em>Turkey (Padu-murga)</em>!',
    "suus-machhli": '<strong>Suus-Machhli</strong> ≈ <strong>"Swoosh!"</strong> sound as it leaps out of the sea + <strong>Machhli</strong> (Fish) → <em>Dolphin (Suus-machhli)</em>!',
    "samudri-feni": '<strong>Samudri-Feni</strong> ≈ <strong>Samudra</strong> (Sea) + 8-10 swimming arms → Sea <em>Squid (Samudri-feni)</em>!',
    "him-pakshi": '<strong>Him-Pakshi</strong> ≈ <strong>Him</strong> (Snow/Ice, like Himalaya!) + <strong>Pakshi</strong> (Tamil <strong>பட்சி = Bird</strong>) → Ice-bird = <em>Penguin (Him-pakshi)</em>!',
    "yaad-dihani": '<strong>Yaad-Dihani</strong> ≈ <strong>Yaad</strong> (Memory, spoken Tamil <strong>"ஞாபகம்"</strong>) + <strong>Dilaana</strong> (To remind) → <em>Reminder (Yaad-dihani)</em>!',
    "sachet-ghanti": '<strong>Sachet-Ghanti</strong> ≈ <strong>Sachet</strong> (Alert/Awake) + <strong>Ghanti</strong> (Bell, Tamil <strong>மணி</strong>) → Wake-up <em>Alarm (Sachet-ghanti)</em>!',
    "samay-ganak": '<strong>Samay-Ganak</strong> ≈ <strong>Samay</strong> (Tamil <strong>சமயம் = Time</strong>) + <strong>Ganak</strong> (Counter) → Countdown <em>Timer (Samay-ganak)</em>!',
    "viraam-ghadi": '<strong>Viraam-Ghadi</strong> ≈ <strong>Viraam</strong> (Stop/Pause) + <strong>Ghadi</strong> (Watch/Clock) → <em>Stopwatch (Viraam-ghadi)</em>!',
    "haath-batti": '<strong>Haath-Batti</strong> ≈ <strong>Haath</strong> (Hand) + <strong>Batti</strong> (Light/Lamp) → Handheld <em>Flashlight / Torch (Haath-batti)</em>!',
    "parda-chitra": '<strong>Parda-Chitra</strong> ≈ <strong>Parda</strong> (Screen/Wall) + <strong>Chitra</strong> (Tamil <strong>சித்திரம் = Picture</strong>) → <em>Wallpaper (Parda-chitra)</em>!',
    "ghanti ki dhun": '<strong>Ghanti ki Dhun</strong> ≈ <strong>Ghanti</strong> (Bell) + <strong>Dhun</strong> (Tune) → Phone <em>Ringtone (Ghanti ki dhun)</em>!',
    "mijaaz": '<strong>Mijaaz</strong> ≈ Sounds like <strong>"My-Jazz"</strong> → Your current emotional vibe and <em>Mood (Mijaaz)</em>!',
    "gehra-udaasi": '<strong>Gehra-Udaasi</strong> ≈ <strong>Gehra</strong> (Deep) + <strong>Udaasi</strong> (Sadness) → Deep <em>Depression (Gehra-udaasi / Avsaad)</em>!',
    "rachanaatmak": '<strong>Rachanaatmak</strong> ≈ From <strong>Rachana</strong> (Creation, Tamil <strong>ரசனை / படைப்பு</strong>) → Highly <em>Creative (Rachanaatmak)</em>!',
    "mahatvaakaankshi": '<strong>Mahatvaakaankshi</strong> ≈ <strong>Mahatva</strong> (Greatness) + <strong>Aakaanksha</strong> (Desire/Goal) → <em>Ambitious (Mahatvaakaankshi)</em>!',
    "ishqbaazi karna": '<strong>Ishqbaazi karna</strong> ≈ <strong>Ishq</strong> (Love/Romance) + playful teasing → To <em>Flirt (Ishqbaazi karna)</em>!',
    "choomna": '<strong>Choomna</strong> ≈ Sounds like Tamil <strong>"உம்மா / சும்மா" (Umma = Kiss!)</strong> → To <em>Kiss (Choomna)</em>!',
    "pakka karna": '<strong>Pakka karna</strong> ≈ Same as spoken Tamil <strong>"பக்கா (Pakka = 100% sure!)"</strong> → To <em>Confirm (Pakka karna)</em>!',
    "nirdeshak": '<strong>Nirdeshak</strong> ≈ From <strong>Nirdesh</strong> (Direction/Instruction) → Movie or company <em>Director (Nirdeshak)</em>!',
    "afsar": '<strong>Afsar</strong> ≈ Direct Desi pronunciation of <strong>"Officer" (Afsar)</strong>!',
    "abhiyanta": '<strong>Abhiyanta</strong> ≈ From <strong>Yantra</strong> (Tamil <strong>இயந்திரம் = Machine/Engine!</strong>) → Machine-builder = <em>Engineer (Abhiyanta)</em>!',
    "vaastukaar": '<strong>Vaastukaar</strong> ≈ Same as Tamil <strong>வாஸ்து (Vaastu = building design!)</strong> + <strong>Kaar</strong> (Maker) → Building <em>Architect (Vaastukaar)</em>!',
    "thekedaar": '<strong>Thekedaar</strong> ≈ From <strong>Theka</strong> (Contract) → Building <em>Contractor (Thekedaar)</em>!',
    "nal-kaariigar": '<strong>Nal-Kaariigar</strong> ≈ <strong>Nal</strong> (Water tap/pipe) + <strong>Kaariigar</strong> (Craftsman) → Pipe <em>Plumber (Nal-kaariigar)</em>!',
    "bijli-mistri": '<strong>Bijli-Mistri</strong> ≈ <strong>Bijli</strong> (Electricity/Lightning) + <strong>Mistri</strong> (Technician) → <em>Electrician (Bijli-mistri)</em>!',
    "yantra-mistri": '<strong>Yantra-Mistri</strong> ≈ <strong>Yantra</strong> (Tamil <strong>இயந்திரம் = Machine</strong>) + <strong>Mistri</strong> → Car/machine <em>Mechanic (Yantra-mistri)</em>!',
    "vimaan-chaalak": '<strong>Vimaan-Chaalak</strong> ≈ <strong>Vimaan</strong> (Tamil <strong>விமானம் = Airplane</strong>) + <strong>Chaalak</strong> (Driver) → Airplane <em>Pilot (Vimaan-chaalak)</em>!',
    "kaptaan": '<strong>Kaptaan</strong> ≈ Sounds right like English <strong>"Captain" (Kaptaan)</strong>!',
    "parosne-wala": '<strong>Parosne-wala</strong> ≈ From <strong>Parosna</strong> (to serve food on a plate) → Restaurant <em>Waiter (Parosne-wala)</em>!',
    "parosne-wali": '<strong>Parosne-wali</strong> ≈ From <strong>Parosna</strong> (to serve food) → Restaurant <em>Waitress (Parosne-wali)</em>!',
    "rasoiya": '<strong>Rasoiya</strong> ≈ From <strong>Rasoi</strong> (Kitchen) → The master cook in the kitchen = <em>Chef / Cook (Rasoiya)</em>!',
    "kalakaar": '<strong>Kalakaar</strong> ≈ <strong>Kala</strong> (Tamil <strong>கலை = Art!</strong>) + <strong>Kaar</strong> (Doer) → <em>Artist (Kalakaar)</em>!',
    "abhineta": '<strong>Abhineta</strong> ≈ From <strong>Abhinaya</strong> (Tamil <strong>அபிநயம் = Acting/Expression!</strong>) → Male <em>Actor (Abhineta)</em>!',
    "abhinetri": '<strong>Abhinetri</strong> ≈ From <strong>Abhinaya</strong> (Tamil <strong>அபிநயம் = Acting!</strong>) → Female <em>Actress (Abhinetri)</em>!',
    "sangeetkaar": '<strong>Sangeetkaar</strong> ≈ <strong>Sangeet</strong> (Tamil <strong>சங்கீதம் = Music!</strong>) + <strong>Kaar</strong> → <em>Musician (Sangeetkaar)</em>!',
    "chitrakaar": '<strong>Chitrakaar</strong> ≈ <strong>Chitra</strong> (Tamil <strong>சித்திரம் = Picture!</strong>) + <strong>Kaar</strong> → Picture-maker = <em>Photographer / Painter (Chitrakaar)</em>!',
    "patrakaar": '<strong>Patrakaar</strong> ≈ <strong>Patra</strong> (Tamil <strong>பத்திரிகை = Newspaper!</strong>) + <strong>Kaar</strong> → News <em>Journalist (Patrakaar)</em>!',
    "dandadhikaari": '<strong>Dandadhikaari</strong> ≈ <strong>Dand</strong> (Tamil <strong>தண்டனை = Punishment/Law</strong>) + <strong>Adhikaari</strong> (Tamil <strong>அதிகாரி = Officer</strong>) → Court <em>Magistrate (Dandadhikaari)</em>!',
    "sipahi": '<strong>Sipahi</strong> ≈ Same as Tamil <strong>சிப்பாய் (Sippaai = Soldier/Police!)</strong> → <em>Police (Sipahi / Pulis)</em>!',
    "aag-bujhane wala": '<strong>Aag-Bujhane wala</strong> ≈ <strong>Aag</strong> (Fire) + <strong>Bujhana</strong> (Extinguish) → <em>Firefighter (Aag-bujhane wala)</em>!',
    "aapat-chikitsak": '<strong>Aapat-Chikitsak</strong> ≈ <strong>Aapat</strong> (Emergency, Tamil <strong>ஆபத்து = Danger/Emergency!</strong>) + <strong>Chikitsak</strong> (Healer) → Emergency <em>Paramedic (Aapat-chikitsak)</em>!',
    "isteefa": '<strong>Isteefa</strong> ≈ Sounds like <strong>"Is-Tough-Bye!"</strong> → Handing in your job <em>Resignation (Isteefa)</em>!',
    "barsaati": '<strong>Barsaati</strong> ≈ From <strong>Barsaat</strong> (Rain) → Waterproof coat worn in the rain = <em>Raincoat (Barsaati)</em>!',
    "upbhokta": '<strong>Upbhokta</strong> ≈ From <strong>Upbhog</strong> (Use/Consumption) → Buyer &amp; <em>Consumer (Upbhokta / Graahak)</em>!',
    "sahyogi": '<strong>Sahyogi</strong> ≈ <strong>Sah</strong> (Together) + <strong>Yogi</strong> (Joined) → Work colleague / <em>Associate (Sahyogi)</em>!',
    "kisht": '<strong>Kisht</strong> ≈ Sounds like <strong>"Cash-Split"</strong> → Paying a loan in monthly parts = <em>Installment (Kisht)</em>!',
    "nivesh": '<strong>Nivesh</strong> ≈ Sounds like <strong>"New-Wealth"</strong> → Putting money into a business = <em>Investment (Nivesh)</em>!',
    "jokhim": '<strong>Jokhim</strong> ≈ Sounds like <strong>"Joke-Him"</strong> → Don\'t joke with danger; taking a big <em>Risk (Jokhim)</em>!',
    "sansad": '<strong>Sansad</strong> ≈ Sounds like <strong>"Sun-Sat"</strong> → Where all elected leaders sit together = <em>Parliament (Sansad)</em>!',
    "parishad": '<strong>Parishad</strong> ≈ Same as Sanskrit/Tamil <strong>பரிஷத் (Parishad = assembly)</strong> → Governing <em>Council (Parishad)</em>!',
    "mantraalaya": '<strong>Mantraalaya</strong> ≈ <strong>Mantri</strong> (Tamil <strong>மந்திரி = Minister!</strong>) + <strong>Aalaya</strong> (House) → Government <em>Ministry (Mantraalaya)</em>!',
    "rajyapaal": '<strong>Rajyapaal</strong> ≈ <strong>Rajya</strong> (Tamil <strong>ராஜ்ஜியம் = State!</strong>) + <strong>Paal</strong> (Protector) → State <em>Governor (Rajyapaal)</em>!',
    "umeedwaar": '<strong>Umeedwaar</strong> ≈ From <strong>Umeed</strong> (Hope) → The hopeful person running in an election = <em>Candidate (Umeedwaar)</em>!',
    "dootavaas": '<strong>Dootavaas</strong> ≈ <strong>Doot</strong> (Tamil <strong>தூதுவர் = Messenger/Envoy!</strong>) + <strong>Aavaas</strong> (Residence) → Foreign <em>Embassy (Dootavaas)</em>!',
    "raajdoot": '<strong>Raajdoot</strong> ≈ <strong>Raaj</strong> (Royal/State) + <strong>Doot</strong> (Tamil <strong>தூதுவர் = Envoy!</strong>) → Foreign <em>Ambassador (Raajdoot)</em>!',
    "fauj": '<strong>Fauj</strong> ≈ Sounds like <strong>"Force"</strong> → The armed military force = <em>Army (Fauj)</em>!',
    "nausena": '<strong>Nausena</strong> ≈ <strong>Nau / Naav</strong> (Boat/Ship, Tamil <strong>நாவாய்</strong>) + <strong>Sena</strong> (Tamil <strong>சேனை = Army</strong>) → Sea-army = <em>Navy (Nausena)</em>!',
    "yuddhaviraam": '<strong>Yuddhaviraam</strong> ≈ <strong>Yuddha</strong> (Tamil <strong>யுத்தம் = War!</strong>) + <strong>Viraam</strong> (Stop) → Stopping a war = <em>Ceasefire (Yuddhaviraam)</em>!',
    "chhaatra": '<strong>Chhaatra</strong> ≈ Sounds like <strong>"Chat-Row"</strong> → School kids sitting in a row = <em>Student (Chhaatra / Vidyarthi)</em>!',
    "shikshak": '<strong>Shikshak</strong> ≈ From <strong>Shiksha</strong> (Tamil <strong>சிக்ஷை / கல்வி = Education!</strong>) → School <em>Teacher (Shikshak / Adhyapak)</em>!',
    "praadhyapak": '<strong>Praadhyapak</strong> ≈ <strong>Pra</strong> (Senior/High) + <strong>Adhyapak</strong> (Teacher) → University <em>Professor (Praadhyapak)</em>!',
    "noshikshak": '<strong>Noshikshak / Ghar-Adhyapak</strong> ≈ Personal <strong>Adhyapak</strong> (Teacher) at home → Private <em>Tutor (Ghar-adhyapak)</em>!',
    "pradhaanaachaarya": '<strong>Pradhaanaachaarya</strong> ≈ <strong>Pradhaan</strong> (Tamil <strong>பிரதான = Chief/Head!</strong>) + <strong>Aachaarya</strong> (Master/Teacher) → School <em>Principal (Pradhaanaachaarya)</em>!',
    "prashikshak": '<strong>Prashikshak</strong> ≈ From <strong>Prashikshan</strong> (Training) → Skills <em>Instructor / Trainer (Prashikshak)</em>!',
    "sahpaathi": '<strong>Sahpaathi</strong> ≈ <strong>Sah</strong> (Together) + <strong>Paath</strong> (Tamil <strong>பாடம் = Lesson!</strong>) → Studying lessons together = <em>Classmate (Sahpaathi)</em>!',
    "kaksha": '<strong>Kaksha</strong> ≈ Sounds like <strong>"Class-Sha"</strong> → School <em>Classroom / Grade (Kaksha)</em>!',
    "shyaampatt": '<strong>Shyaampatt</strong> ≈ <strong>Shyaam</strong> (Dark/Black, like Lord Shyam!) + <strong>Patt</strong> (Board) → <em>Blackboard (Shyaampatt)</em>!',
    "shwet-phalak": '<strong>Shwet-Phalak</strong> ≈ <strong>Shwet</strong> (Tamil <strong>சுவேதம் = White!</strong>) + <strong>Phalak</strong> (Board) → <em>Whiteboard (Shwet-phalak)</em>!',
    "khadiya": '<strong>Khadiya</strong> ≈ White limestone stick used to write on a slate = <em>Chalk (Khadiya / Chaak)</em>!',
    "paath": '<strong>Paath</strong> ≈ Same as Tamil <strong>பாடம் (Paadam = Lesson!)</strong> → Chapter or <em>Lesson (Paath / Sabak)</em>!',
    "vyakhyan": '<strong>Vyakhyan</strong> ≈ From <strong>Vyakhya</strong> ( Tamil <strong>வியாக்கியானம் = Detailed explanation!</strong>) → College <em>Lecture (Vyakhyan)</em>!',
    "grihakarya": '<strong>Grihakarya</strong> ≈ <strong>Griha</strong> (Tamil <strong>கிரகம் = Home!</strong>) + <strong>Karya</strong> (Tamil <strong>காரியம் = Work!</strong>) → <em>Homework (Grihakarya)</em>!',
    "nibandh": '<strong>Nibandh</strong> ≈ Sounds like <strong>"Nib-And-Pen"</strong> → Writing a long school <em>Essay (Nibandh)</em> with a pen nib!',
    "prashnottari": '<strong>Prashnottari</strong> ≈ <strong>Prashna</strong> (Tamil <strong>பிரச்சனை / வினா = Question</strong>) + <strong>Uttar</strong> (Tamil <strong>உத்தரவு / பதில் = Answer</strong>) → Q&amp;A <em>Quiz (Prashnottari)</em>!',
    "pariksha": '<strong>Pariksha</strong> ≈ Exact same word as Tamil <strong>பரீட்சை (Pareetchai = Exam!)</strong> → School <em>Exam (Pariksha)</em>!',
    "chhatravritti": '<strong>Chhatravritti</strong> ≈ <strong>Chhaatra</strong> (Student) + <strong>Vritti</strong> (Stipend/Support) → Student <em>Scholarship (Chhatravritti)</em>!',
    "pramaan-patra": '<strong>Pramaan-Patra</strong> ≈ <strong>Pramaan</strong> (Tamil <strong>பிரமாணம் = Proof!</strong>) + <strong>Patra</strong> (Document) → Official <em>Certificate / Diploma (Pramaan-patra)</em>!',
    "chhaatraavaas": '<strong>Chhaatraavaas</strong> ≈ <strong>Chhaatra</strong> (Student) + <strong>Aavaas</strong> (Residence/Home) → College <em>Dormitory / Hostel (Chhaatraavaas)</em>!',
    "sabhagaar": '<strong>Sabhagaar</strong> ≈ <strong>Sabha</strong> (Tamil <strong>சபை = Assembly Hall!</strong>) + <strong>Aagaar</strong> (Building) → Large <em>Auditorium (Sabhagaar)</em>!',
    "shodh": '<strong>Shodh</strong> ≈ Same root as Tamil <strong>சோதனை (Sodhanai = Investigation/Research!)</strong> → Scientific <em>Research (Shodh)</em>!',
    "bhoogol": '<strong>Bhoogol</strong> ≈ <strong>Bhoo</strong> (Tamil <strong>பூமி = Earth!</strong>) + <strong>Gol</strong> (Round) → Study of the round Earth = <em>Geography (Bhoogol)</em>!',
    "ganit": '<strong>Ganit</strong> ≈ Same as Tamil <strong>கணிதம் (Kanitham = Mathematics!)</strong> → <em>Math (Ganit)</em>!',
    "beej-ganit": '<strong>Beej-Ganit</strong> ≈ <strong>Beej</strong> (Seed/Root symbol x, y) + <strong>Ganit</strong> (Tamil <strong>கணிதம் = Math</strong>) → <em>Algebra (Beej-ganit)</em>!',
    "rekha-ganit": '<strong>Rekha-Ganit</strong> ≈ <strong>Rekha</strong> (Tamil <strong>ரேகை = Line!</strong>) + <strong>Ganit</strong> (Math) → Line &amp; shape math = <em>Geometry (Rekha-ganit)</em>!',
    "bhautik-vigyan": '<strong>Bhautik-Vigyan</strong> ≈ <strong>Bhautik</strong> (Physical world) + <strong>Vigyan</strong> (Tamil <strong>விஞ்ஞானம் = Science!</strong>) → <em>Physics (Bhautik-vigyan)</em>!',
    "khagol-vigyan": '<strong>Khagol-Vigyan</strong> ≈ <strong>Khagol</strong> (Sky/Celestial sphere) + <strong>Vigyan</strong> (Tamil <strong>விஞ்ஞானம் = Science</strong>) → <em>Astronomy (Khagol-vigyan)</em>!',
    "rasaayan-vigyan": '<strong>Rasaayan-Vigyan</strong> ≈ <strong>Rasaayan</strong> (Tamil <strong>ரசாயனம் = Chemicals!</strong>) + <strong>Vigyan</strong> (Science) → <em>Chemistry (Rasaayan-vigyan)</em>!',
    "jeev-vigyan": '<strong>Jeev-Vigyan</strong> ≈ <strong>Jeev</strong> (Tamil <strong>ஜீவன் = Living being!</strong>) + <strong>Vigyan</strong> (Science) → <em>Biology (Jeev-vigyan)</em>!',
    "darshan-shastra": '<strong>Darshan-Shastra</strong> ≈ <strong>Darshan</strong> (Tamil <strong>தரிசனம் = Vision/Insight!</strong>) + <strong>Shastra</strong> (Tamil <strong>சாஸ்திரம்</strong>) → <em>Philosophy (Darshan-shastra)</em>!',
    "manovigyan": '<strong>Manovigyan</strong> ≈ <strong>Manas / Mano</strong> (Tamil <strong>மனது = Mind!</strong>) + <strong>Vigyan</strong> (Science) → Science of the mind = <em>Psychology (Manovigyan)</em>!',
    "arthashastra": '<strong>Arthashastra</strong> ≈ <strong>Artha</strong> (Wealth/Money, Tamil <strong>அர்த்தம்</strong>) + <strong>Shastra</strong> → <em>Economics (Arthashastra)</em>!',
    "vyakaran": '<strong>Vyakaran</strong> ≈ Same as Sanskrit/Tamil <strong>வியாகரணம் (Vyakaranam = Grammar!)</strong> → Language <em>Grammar (Vyakaran)</em>!',
    "prayogshala": '<strong>Prayogshala</strong> ≈ <strong>Prayog</strong> (Tamil <strong>பிரயோகம் = Experiment!</strong>) + <strong>Shala</strong> (Hall/Room) → Science <em>Laboratory (Prayogshala)</em>!',
    "parikalpana": '<strong>Parikalpana</strong> ≈ <strong>Pari</strong> + <strong>Kalpana</strong> (Tamil <strong>கற்பனை = Imagination/Idea!</strong>) → Scientific <em>Hypothesis (Parikalpana)</em>!',
    "tareeqa": '<strong>Tareeqa</strong> ≈ Sounds like <strong>"Track-Way"</strong> → The step-by-step way to do something = <em>Method (Tareeqa)</em>!',
    "aavishkaar": '<strong>Aavishkaar</strong> ≈ Sounds like <strong>"A-Wish-Car!"</strong> → Inventing a flying car you wished for = <em>Invention (Aavishkaar)</em>!',
    "vishleshan": '<strong>Vishleshan</strong> ≈ Splitting a problem into clear parts = Detailed <em>Analysis (Vishleshan)</em>!',
    "samikaran": '<strong>Samikaran</strong> ≈ <strong>Sama</strong> (Tamil <strong>சமம் = Equal!</strong>) → Making both sides equal (x = y) = Math <em>Equation (Samikaran)</em>!',
    "parmanu": '<strong>Parmanu</strong> ≈ <strong>Param</strong> (Ultimate/Smallest) + <strong>Anu</strong> (Tamil <strong>அணு = Atom!</strong>) → <em>Atom (Parmanu)</em>!',
    "oorja": '<strong>Oorja</strong> ≈ Sounds like <strong>"Urge-Ya!"</strong> → Power that urges you to move = <em>Energy (Oorja)</em>!',
    "gurutvakarshan": '<strong>Gurutvakarshan</strong> ≈ <strong>Gurutva</strong> (Weight/Heaviness) + <strong>Aakarshan</strong> (Tamil <strong>ஆகர்ஷணம் = Pull/Attraction!</strong>) → Earth\'s pull = <em>Gravity (Gurutvakarshan)</em>!',
    "pradarshani": '<strong>Pradarshani</strong> ≈ From <strong>Pradarshan</strong> (Display/Show, Tamil <strong>தரிசனம்</strong>) → Art or science <em>Exhibition (Pradarshani)</em>!',
    "khaad": '<strong>Khaad</strong> ≈ Rich natural soil food for crops = <em>Fertilizer / Manure (Khaad)</em>!',
    "keetnaashak-dawa": '<strong>Keetnaashak</strong> ≈ <strong>Keet</strong> (Insect/Bug) + <strong>Naashak</strong> (Tamil <strong>நாசம் = Destroyer!</strong>) → Bug-destroyer = <em>Pesticide (Keetnaashak)</em>!',
    "navikaran": '<strong>Navikaran</strong> ≈ From <strong>Nava</strong> (Tamil <strong>நவ / புதிய = New!</strong>) → Making a pass or license new again = <em>Renewal (Navikaran)</em>!',
    "teeka": '<strong>Teeka</strong> ≈ Like putting a protective <strong>Teeka</strong> mark on the arm = Medical <em>Vaccine / Injection (Teeka)</em>!',
    "ghamand": '<strong>Ghamand</strong> ≈ Sounds like <strong>"Go-Demand"</strong> → Arrogant pride and <em>Ego (Ghamand / Ahankaar)</em>!',
    "milansaar": '<strong>Milansaar</strong> ≈ From <strong>Milna</strong> (to meet &amp; mingle warmly) → Outgoing <em>Extrovert (Milansaar)</em>!',
    "kshamta": '<strong>Kshamta</strong> ≈ Sounds like <strong>"Sam-Taakat"</strong> → Full strength and holding <em>Capacity (Kshamta)</em>!',
    "seema": '<strong>Seema</strong> ≈ Boundary line (like Tamil <strong>சீமை = border/land!</strong>) → Outer <em>Limit / Boundary (Seema)</em>!',
    "chaukidaar": '<strong>Chaukidaar</strong> ≈ <strong>Chauki</strong> (Guard post) + <strong>Daar</strong> → Night <em>Watchman / Security Guard (Chaukidaar)</em>!',
    "asthaayi": '<strong>Asthaayi</strong> ≈ <strong>A-</strong> (Not) + <strong>Sthaayi</strong> (Tamil <strong>ஸ்திரமான = Permanent</strong>) → Not permanent = <em>Temporary (Asthaayi)</em>!',
}

HI_SOUND_ALIKES.update(EXTRA_HI_HOOKS)

# ============================================================================
# 4. MULTI-MEANING (1. ... | 2. ...) MASTER DEFINITIONS FOR POLYSEMOUS CARDS
#    Every sense 1 and sense 2 has a real phonetic or root mnemonic!
# ============================================================================
MULTI_MEANING_OVERRIDES = {
    1022: {
        "tamil": "1. இடம் (Area) / 2. விண்வெளி (Cosmos)",
        "es": "1. Area: espacio | 2. Cosmos: espacio exterior",
        "hi": "1. Area: jagah / sthaan | 2. Cosmos: antariksh / aakaash",
        "shortcutEs": '<strong>1. Espacio (Area)</strong> ≈ Sounds right like English <strong>"Space"</strong> → Empty room or <em>Space</em>!<br><strong>2. Espacio exterior (Cosmos)</strong> ≈ <strong>Espacio</strong> (Space) + <strong>Exterior</strong> (Outside Earth) → Outer <em>Space (Cosmos)</em>!',
        "shortcutHi": '<strong>1. Jagah (Area)</strong> ≈ Spoken Tamil <strong>"ஜகா வாங்கு" (Jaga = make space/room!)</strong> → Empty room or <em>Space (Jagah)</em>!<br><strong>2. Antariksh / Aakaash (Cosmos)</strong> ≈ <strong>Antariksh</strong> sounds like <strong>"Inter-Reach"</strong> high in the stars (or <strong>Aakaash</strong> = Tamil <strong>ஆகாயம் = Sky/Space!</strong>) → Outer <em>Space (Antariksh)</em>!'
    },
    1107: {
        "tamil": "1. முத்திரை (Stamp) / 2. கடல் நாய் (Animal)",
        "es": "1. Stamp: sello | 2. Animal: foca",
        "hi": "1. Stamp: mohar / chhaap | 2. Animal: jal-vyaghra (or seal)",
        "shortcutEs": '<strong>1. Sello (Stamp)</strong> ≈ Sounds like <strong>"Say-Yo &amp; Seal it!"</strong> → Official <em>Stamp / Seal (Sello)</em>!<br><strong>2. Foca (Animal)</strong> ≈ Sounds like <strong>"Focus"</strong> → A sea <em>Seal (Foca)</em> balancing a ball on its nose with total focus!',
        "shortcutHi": '<strong>1. Mohar (Stamp)</strong> ≈ Same as Tamil historical word <strong>மொஹர் / முத்திரை (Mohar = royal stamp!)</strong> → Official <em>Seal (Mohar)</em>!<br><strong>2. Jal-Vyaghra / Seal (Animal)</strong> ≈ <strong>Jal</strong> (Water) + sea creature clapping flippers = Sea <em>Seal</em>!'
    },
    1519: {
        "tamil": "1. மாநிலம் (Province) / 2. கூறு (Declare)",
        "es": "1. Province: estado | 2. Declare: declarar (afirmar)",
        "hi": "1. Province: rajya / praant | 2. Declare: kehna / bayaan dena",
        "shortcutEs": '<strong>1. Estado (Province)</strong> ≈ Drop "E-" → <strong>Stado = State</strong>!<br><strong>2. Declarar (Declare)</strong> ≈ Direct cognate with English <strong>"Declare"</strong> → To <em>State / Declare</em>!',
        "shortcutHi": '<strong>1. Rajya (Province)</strong> ≈ Same as Tamil <strong>ராஜ்ஜியம் (Raajjiyam = State/Kingdom!)</strong> → <em>State (Rajya)</em>!<br><strong>2. Bayaan dena (Declare)</strong> ≈ Sounds like <strong>"Buy-Announce"</strong> → Giving an official statement = <em>State (Bayaan dena)</em>!'
    },
    1580: {
        "tamil": "1. நடத்துநர் (Bus) / 2. இசை நடத்துநர் (Music)",
        "es": "1. Bus: cobrador | 2. Music: director de orquesta",
        "hi": "1. Bus: parichaalak (or conductor) | 2. Music: sangeet-sanchaalak",
        "shortcutEs": '<strong>1. Cobrador (Bus)</strong> ≈ From <strong>Cobrar</strong> (to collect ticket fare) → Bus ticket <em>Conductor (Cobrador)</em>!<br><strong>2. Director de orquesta (Music)</strong> ≈ Directs the orchestra = Music <em>Conductor</em>!',
        "shortcutHi": '<strong>1. Parichaalak (Bus)</strong> ≈ From <strong>Chalaana</strong> (to run/manage the bus) → Bus <em>Conductor (Parichaalak)</em>!<br><strong>2. Sangeet-Sanchaalak (Music)</strong> ≈ <strong>Sangeet</strong> (Tamil <strong>சங்கீதம் = Music</strong>) + <strong>Sanchaalak</strong> (Director) → Orchestra <em>Conductor</em>!'
    },
    1623: {
        "tamil": "1. பணி நேரம் (Work) / 2. நகர்த்து (Move)",
        "es": "1. Work: turno | 2. Move: cambiar (mover)",
        "hi": "1. Work: paali / baari | 2. Move: khiskaana / badalna",
        "shortcutEs": '<strong>1. Turno (Work)</strong> ≈ Sounds like <strong>"Turn"</strong> → Your work turn = <em>Work Shift (Turno)</em>!<br><strong>2. Cambiar / Mover (Move)</strong> ≈ Sounds like <strong>"Change &amp; Move"</strong> → To <em>Shift / Move</em>!',
        "shortcutHi": '<strong>1. Paali / Baari (Work)</strong> ≈ Sounds like Tamil <strong>பணி முறை (Work turn/rotation)</strong> → Work <em>Shift (Paali)</em>!<br><strong>2. Khiskaana / Badalna (Move)</strong> ≈ <strong>Badalna</strong> (to change/move position) → To <em>Shift</em>!'
    },
    1654: {
        "tamil": "1. கட்டணம் (Fee) / 2. மின்னேற்று (Battery)",
        "es": "1. Fee: cobro (tarifa) | 2. Battery: cargar",
        "hi": "1. Fee: shulk / daam | 2. Battery: urja bharna (or charge karna)",
        "shortcutEs": '<strong>1. Cobro / Tarifa (Fee)</strong> ≈ Sounds like <strong>"Tariff"</strong> → Price or fee <em>Charge (Tarifa)</em>!<br><strong>2. Cargar (Battery)</strong> ≈ Sounds like <strong>"Car-Charge"</strong> → To <em>Charge (Cargar)</em> a battery!',
        "shortcutHi": '<strong>1. Shulk / Daam (Fee)</strong> ≈ <strong>Daam</strong> sounds like <strong>"Dime"</strong> → Price or fee <em>Charge (Shulk / Daam)</em>!<br><strong>2. Urja bharna (Battery)</strong> ≈ Filling up <strong>Urja</strong> (Energy) in a phone battery = <em>Charge</em>!'
    },
    1655: {
        "tamil": "1. கட்டணப் பட்டியல் (Invoice) / 2. சட்ட மசோதா (Law)",
        "es": "1. Invoice: factura (cuenta) | 2. Law: proyecto de ley",
        "hi": "1. Invoice: raseed / hisaab-parchi | 2. Law: vidheyak",
        "shortcutEs": '<strong>1. Factura / Cuenta (Invoice)</strong> ≈ Sounds like <strong>"Count-Up"</strong> the factory receipt = <em>Bill (Cuenta)</em>!<br><strong>2. Proyecto de ley (Law)</strong> ≈ <strong>Project of Law</strong> in parliament = Legal <em>Bill</em>!',
        "shortcutHi": '<strong>1. Raseed / Hisaab-Parchi (Invoice)</strong> ≈ <strong>Raseed</strong> sounds right like <strong>"Receipt"</strong> → Shop <em>Bill (Raseed)</em>!<br><strong>2. Vidheyak (Law)</strong> ≈ From <strong>Vidhi</strong> (Tamil <strong>விதி = Rule/Law!</strong>) → Parliament <em>Bill (Vidheyak)</em>!'
    },
    1684: {
        "tamil": "1. இருப்புத் தொகை (Bank) / 2. சமநிலை (Equilibrium)",
        "es": "1. Bank: saldo | 2. Equilibrium: equilibrio",
        "hi": "1. Bank: shesh-raashi | 2. Equilibrium: santulan",
        "shortcutEs": '<strong>1. Saldo (Bank)</strong> ≈ Sounds like <strong>"Sold-Leftover"</strong> → Remaining bank <em>Balance (Saldo)</em>!<br><strong>2. Equilibrio (Equilibrium)</strong> ≈ Direct cognate with <strong>"Equilibrium"</strong> → Physical <em>Balance</em>!',
        "shortcutHi": '<strong>1. Shesh-Raashi (Bank)</strong> ≈ <strong>Shesh</strong> (Tamil <strong>சேஷம் = Remaining!</strong>) + <strong>Raashi</strong> (Amount) → Bank <em>Balance (Shesh-raashi)</em>!<br><strong>2. Santulan (Equilibrium)</strong> ≈ From <strong>Tula</strong> (Tamil <strong>துலாம் = Weighing scale!</strong>) → Equal steady <em>Balance (Santulan)</em>!'
    },
    1705: {
        "tamil": "1. ஆர்வம் (Curiosity) / 2. வட்டி (Bank)",
        "es": "1. Curiosity: interés | 2. Bank: tasa de interés",
        "hi": "1. Curiosity: ruchi / dilchaspi | 2. Bank: byaaj",
        "shortcutEs": '<strong>1. Interés (Curiosity)</strong> ≈ Identical to English <strong>"Interest"</strong>!<br><strong>2. Tasa de interés (Bank)</strong> ≈ Bank <strong>Interest Rate</strong>!',
        "shortcutHi": '<strong>1. Ruchi / Dilchaspi (Curiosity)</strong> ≈ <strong>Ruchi</strong> is the same as Tamil <strong>ருசி (Rusi = taste/liking!)</strong> → Personal <em>Interest (Ruchi)</em>!<br><strong>2. Byaaj (Bank)</strong> ≈ Sounds like <strong>"Buy-Charge"</strong> → Extra bank loan <em>Interest (Byaaj)</em>!'
    },
    1737: {
        "tamil": "1. நீதிமன்றம் (Law) / 2. ஆடுகளம் (Sports)",
        "es": "1. Law: tribunal (juzgado) | 2. Sports: cancha",
        "hi": "1. Law: adaalat / nyayalaya | 2. Sports: khel-maidaan",
        "shortcutEs": '<strong>1. Tribunal (Law)</strong> ≈ Direct cognate with English <strong>"Tribunal"</strong> = Law <em>Court</em>!<br><strong>2. Cancha (Sports)</strong> ≈ Sounds like <strong>"Can-Catch-Ya!"</strong> on the tennis/basketball <em>Court (Cancha)</em>!',
        "shortcutHi": '<strong>1. Adaalat (Law)</strong> ≈ Same as spoken Tamil <strong>அதாலத் / நீதிமன்றம் (Adaalat = Law Court!)</strong>!<br><strong>2. Khel-Maidaan (Sports)</strong> ≈ <strong>Khel</strong> (Game) + <strong>Maidaan</strong> (Tamil <strong>மைதானம் = Ground/Court!</strong>)!'
    },
    1745: {
        "tamil": "1. வாக்கியம் (Grammar) / 2. தண்டனைத் தீர்ப்பு (Law)",
        "es": "1. Grammar: oración (frase) | 2. Law: condena (sentencia)",
        "hi": "1. Grammar: vaakya | 2. Law: saza / dand",
        "shortcutEs": '<strong>1. Oración / Frase (Grammar)</strong> ≈ Sounds like <strong>"Phrase"</strong> → A spoken/written <em>Sentence (Frase)</em>!<br><strong>2. Sentencia / Condena (Law)</strong> ≈ Direct cognate with <strong>"Sentence / Condemn"</strong>!',
        "shortcutHi": '<strong>1. Vaakya (Grammar)</strong> ≈ Exact same word as Tamil <strong>வாக்கியம் (Vaakkiyam = Sentence!)</strong>!<br><strong>2. Saza (Law)</strong> ≈ Same as spoken Tamil <strong>சஜா / தண்டனை</strong> → Court prison <em>Sentence / Punishment (Saza)</em>!'
    },
    1811: {
        "tamil": "1. உயிரணு (Biology) / 2. சிற்றறை / மின்கலம் (Room/Battery)",
        "es": "1. Biology: célula | 2. Room/Battery: celda (pila)",
        "hi": "1. Biology: koshika | 2. Room/Battery: kothri / vidyut-kosh",
        "shortcutEs": '<strong>1. Célula (Biology)</strong> ≈ Sounds like <strong>"Cellular"</strong> → Living body <em>Cell (Célula)</em>!<br><strong>2. Celda (Room)</strong> ≈ Sounds like <strong>"Cell-Door"</strong> → Prison <em>Cell (Celda)</em>!',
        "shortcutHi": '<strong>1. Koshika (Biology)</strong> ≈ From <strong>Kosh</strong> (Tiny chamber) → Microscopic body <em>Cell (Koshika)</em>!<br><strong>2. Kothri (Room)</strong> ≈ Sounds like <strong>"Coat-Room"</strong> → A tiny locked prison <em>Cell (Kothri)</em>!'
    },
    1862: {
        "tamil": "1. விதி (Law) / 2. ஆட்சி செய் (Govern)",
        "es": "1. Law: regla (norma) | 2. Govern: gobernar",
        "hi": "1. Law: niyam / kanoon | 2. Govern: shasan karna / raaj karna",
        "shortcutEs": '<strong>1. Regla / Norma (Law)</strong> ≈ Cognate with <strong>"Regular / Norm"</strong> → A <em>Rule</em>!<br><strong>2. Gobernar (Govern)</strong> ≈ Direct cognate with <strong>"Govern"</strong> → To <em>Rule / Govern</em> a nation!',
        "shortcutHi": '<strong>1. Niyam (Law)</strong> ≈ Same as Tamil <strong>நியமம் / விதி (Niyamam = Rule!)</strong>!<br><strong>2. Raaj karna / Shasan karna (Govern)</strong> ≈ Same as Tamil <strong>ராஜ்ஜியம் / சாசனம் (Royal Rule!)</strong> → To <em>Rule</em>!'
    },
    1879: {
        "tamil": "1. சரி / வலது (Correct/Dir) / 2. உரிமை (Legal)",
        "es": "1. Correct/Dir: correcto (derecha) | 2. Legal: derecho",
        "hi": "1. Correct/Dir: sahi / daahina | 2. Legal: adhikaar / haq",
        "shortcutEs": '<strong>1. Correcto / Derecha (Dir)</strong> ≈ <strong>Correct</strong> or <strong>Right hand (Derecha)</strong>!<br><strong>2. Derecho (Legal)</strong> ≈ Sounds like <strong>"Direct-Right"</strong> → Human <em>Right (Derecho)</em>!',
        "shortcutHi": '<strong>1. Sahi / Daahina (Dir)</strong> ≈ Spoken Tamil <strong>"சஹி" (Sahi = Correct/Right!)</strong> &amp; <strong>Daahina</strong> (Right side)!<br><strong>2. Adhikaar / Haq (Legal)</strong> ≈ Same as Tamil <strong>அதிகாரம் (Adhikaaram = Right/Authority!)</strong>!'
    },
    1886: {
        "tamil": "1. மார்ச் மாதம் (Month) / 2. அணிவகுப்பு (Parade)",
        "es": "1. Month: marzo | 2. Parade: marchar (desfile)",
        "hi": "1. Month: maarch-maah | 2. Parade: juloos / kadam-taal",
        "shortcutEs": '<strong>1. Marzo (Month)</strong> ≈ Sounds right like <strong>"March"</strong>!<br><strong>2. Marchar (Parade)</strong> ≈ Soldiers <strong>Marching</strong> in a parade!',
        "shortcutHi": '<strong>1. Maarch-Maah (Month)</strong> ≈ <strong>March</strong> + <strong>Maah</strong> (Tamil <strong>மாதம் = Month!</strong>)!<br><strong>2. Juloos / Kadam-Taal (Parade)</strong> ≈ <strong>Kadam</strong> (Step) + <strong>Taal</strong> (Rhythm/Beat) → Marching in step = <em>March</em>!'
    },
}

# Additional polysemous multi-meaning cards across 1-3000 with full Sense 1 & Sense 2 mnemonics
MORE_MULTI_MEANING = {
    279: { # SEASON
        "tamil": "1. பருவகாலம் (Weather) / 2. தாளிப்பு / மசாலா சேர் (Spice food)",
        "es": "1. Weather: estación (temporada) | 2. Spice: sazonar (condimentar)",
        "hi": "1. Weather: mausam / ritu | 2. Spice: chhaunkna / masala milana",
        "shortcutEs": '<strong>1. Estación (Weather)</strong> ≈ Weather <strong>Station / Season</strong> of the year!<br><strong>2. Sazonar (Spice)</strong> ≈ Sounds right like English <strong>"Season"</strong> food with spices!',
        "shortcutHi": '<strong>1. Mausam / Ritu (Weather)</strong> ≈ Same as spoken Tamil <strong>மௌசம் / ரிது (Ritu = Season!)</strong>!<br><strong>2. Masala milana (Spice)</strong> ≈ Adding <strong>Masala</strong> (Tamil <strong>மசாலா</strong>) to <em>Season</em> a dish!'
    },
    292: { # MINUTE
        "tamil": "1. நிமிடம் (60 Seconds) / 2. மிகச் சிறிய (Tiny)",
        "es": "1. Time: minuto | 2. Tiny: diminuto (minúsculo)",
        "hi": "1. Time: pal / kshan (or minute) | 2. Tiny: bahut barik / sookshma",
        "shortcutEs": '<strong>1. Minuto (Time)</strong> ≈ Identical to English <strong>"Minute"</strong>!<br><strong>2. Diminuto (Tiny)</strong> ≈ Cognate with <strong>"Diminutive / Minuscule"</strong> → Tiny / <em>Minute</em> detail!',
        "shortcutHi": '<strong>1. Pal / Kshan (Time)</strong> ≈ <strong>Kshan</strong> is the same as Tamil <strong>க்ஷணம் (Kshanam = Moment/Minute!)</strong>!<br><strong>2. Sookshma / Barik (Tiny)</strong> ≈ Same as Tamil <strong>சூட்சுமம் (Sookshmam = Fine/Minute detail!)</strong>!'
    },
    341: { # SHOW
        "tamil": "1. காட்டு (Display) / 2. நிகழ்ச்சி (Program)",
        "es": "1. Display: mostrar (enseñar) | 2. Program: espectáculo",
        "hi": "1. Display: dikhaana | 2. Program: tamaasha / pradarshan",
        "shortcutEs": '<strong>1. Mostrar (Display)</strong> ≈ Cognate with <strong>"Demonstrate"</strong> → To <em>Show (Mostrar)</em>!<br><strong>2. Espectáculo (Program)</strong> ≈ Cognate with <strong>"Spectacle"</strong> → Stage <em>Show</em>!',
        "shortcutHi": '<strong>1. Dikhaana (Display)</strong> ≈ From <strong>Dekhna</strong> ("Deck-Now" = See) → Make someone see = <em>Show (Dikhaana)</em>!<br><strong>2. Pradarshan / Tamaasha (Program)</strong> ≈ Spoken Tamil <strong>"தமாஷா"</strong> or <strong>தரிசனம்</strong> → Live <em>Show</em>!'
    },
    345: { # PLAY
        "tamil": "1. விளையாடு (Game/Sport) / 2. நாடகம் / இசை (Drama/Music)",
        "es": "1. Sport: jugar | 2. Music/Stage: tocar (obra de teatro)",
        "hi": "1. Sport: khelna | 2. Music/Stage: bajaana (or naatak)",
        "shortcutEs": '<strong>1. Jugar (Sport)</strong> ≈ Sounds like <strong>"Juggle"</strong> → <em>Play (Jugar)</em> a ball game!<br><strong>2. Tocar / Obra (Music/Stage)</strong> ≈ <strong>Touch</strong> guitar strings to <em>Play (Tocar)</em> music!',
        "shortcutHi": '<strong>1. Khelna (Sport)</strong> ≈ Sounds like <strong>"Kick-Ball-Now"</strong> → <em>Play (Khelna)</em> sports!<br><strong>2. Bajaana / Naatak (Music/Stage)</strong> ≈ <strong>Naatak</strong> = Tamil <strong>நாடகம் (Stage Play!)</strong> &amp; <strong>Bajaana</strong> = Play an instrument!'
    },
    371: { # LEAD
        "tamil": "1. வழிநடத்து (Guide) / 2. ஈயம் (Metal)",
        "es": "1. Guide: liderar (guiar) | 2. Metal: plomo",
        "hi": "1. Guide: aage chalna / netritva karna | 2. Metal: seesa",
        "shortcutEs": '<strong>1. Liderar (Guide)</strong> ≈ Sounds right like English <strong>"Leader"</strong> → To <em>Lead</em>!<br><strong>2. Plomo (Metal)</strong> ≈ Root of English <strong>"Plumber"</strong> (who fixed lead pipes!) = <em>Lead (Plomo)</em>!',
        "shortcutHi": '<strong>1. Aage chalna / Netritva (Guide)</strong> ≈ <strong>Aage</strong> (Ahead) + <strong>Chalna</strong> (Walk) → Walk ahead to <em>Lead</em>!<br><strong>2. Seesa (Metal)</strong> ≈ Sounds like <strong>"See-Saw"</strong> made of heavy grey metal = <em>Lead (Seesa)</em>!'
    },
    372: { # LIVE
        "tamil": "1. வாழ் / வசி (Reside) / 2. நேரலை (Broadcast)",
        "es": "1. Reside: vivir | 2. Broadcast: en vivo (en directo)",
        "hi": "1. Reside: rehna / jeena | 2. Broadcast: seedha-prasaaran",
        "shortcutEs": '<strong>1. Vivir (Reside)</strong> ≈ Root of <strong>"Vivid / Revive"</strong> → To <em>Live (Vivir)</em>!<br><strong>2. En vivo (Broadcast)</strong> ≈ <strong>Vivo</strong> (Alive) → <em>Live</em> concert broadcast!',
        "shortcutHi": '<strong>1. Rehna / Jeena (Reside)</strong> ≈ <strong>Jeena</strong> comes from <strong>Jeev</strong> (Tamil <strong>ஜீவன் = Life!</strong>) → To <em>Live</em>!<br><strong>2. Seedha-Prasaaran (Broadcast)</strong> ≈ <strong>Seedha</strong> (Direct, spoken Tamil <strong>"சீதா"</strong>) broadcast = <em>Live</em>!'
    },
    397: { # FALL
        "tamil": "1. விழு (Drop down) / 2. இலையுதிர்காலம் (Autumn)",
        "es": "1. Drop: caer | 2. Autumn: otoño",
        "hi": "1. Drop: girna | 2. Autumn: patjhad",
        "shortcutEs": '<strong>1. Caer (Drop)</strong> ≈ Sounds like <strong>"Care-Fall!"</strong> → Take care not to <em>Fall (Caer)</em>!<br><strong>2. Otoño (Autumn)</strong> ≈ Sounds right like English <strong>"Autumn" (Otoño)</strong>!',
        "shortcutHi": '<strong>1. Girna (Drop)</strong> ≈ Sounds like <strong>"Gear-Now"</strong> dropping on the ground = <em>Fall (Girna)</em>!<br><strong>2. Patjhad (Autumn)</strong> ≈ <strong>Patta</strong> (Leaf) + <strong>Jhadna</strong> (Fall off) → When leaves fall = <em>Autumn / Fall (Patjhad)</em>!'
    },
    413: { # FLY
        "tamil": "1. பற (Soar in air) / 2. ஈ (Insect)",
        "es": "1. Soar: volar | 2. Insect: mosca",
        "hi": "1. Soar: udna | 2. Insect: makkhi",
        "shortcutEs": '<strong>1. Volar (Soar)</strong> ≈ Root of <strong>"Volleyball"</strong> (a ball flying in the air!) → To <em>Fly (Volar)</em>!<br><strong>2. Mosca (Insect)</strong> ≈ Sounds like <strong>"Mosquito"</strong> → Buzzing house <em>Fly (Mosca)</em>!',
        "shortcutHi": '<strong>1. Udna (Soar)</strong> ≈ Sounds like <strong>"Up-Now"</strong> → Soaring up in the sky = <em>Fly (Udna)</em>!<br><strong>2. Makkhi (Insect)</strong> ≈ Sounds like <strong>"Mug-Key"</strong> → A house <em>Fly (Makkhi)</em> landing on your coffee mug!'
    },
    459: { # CHECK
        "tamil": "1. சரிபார் (Inspect) / 2. காசோலை (Bank cheque)",
        "es": "1. Inspect: revisar (verificar) | 2. Bank: cheque",
        "hi": "1. Inspect: jaanch karna | 2. Bank: dhanadesh (or cheque)",
        "shortcutEs": '<strong>1. Revisar / Verificar (Inspect)</strong> ≈ Cognate with <strong>"Revise / Verify"</strong> → To <em>Check</em>!<br><strong>2. Cheque (Bank)</strong> ≈ Identical to English <strong>"Cheque"</strong>!',
        "shortcutHi": '<strong>1. Jaanch karna (Inspect)</strong> ≈ Sounds like <strong>"Judge-Now"</strong> → Inspect &amp; <em>Check (Jaanch karna)</em>!<br><strong>2. Dhanadesh / Cheque (Bank)</strong> ≈ <strong>Dhan</strong> (Tamil <strong>தனம் = Wealth/Money!</strong>) + <strong>Aadesh</strong> (Order) → Bank <em>Cheque</em>!'
    },
    702: { # CHEST
        "tamil": "1. மார்பு (Body) / 2. பெட்டி ( wooden box)",
        "es": "1. Body: pecho | 2. Box: cofre (baúl)",
        "hi": "1. Body: chhaati / seena | 2. Box: sandook / peti",
        "shortcutEs": '<strong>1. Pecho (Body)</strong> ≈ Root of <strong>"Pectoral"</strong> chest muscles = <em>Chest (Pecho)</em>!<br><strong>2. Cofre (Box)</strong> ≈ Sounds like English <strong>"Coffer"</strong> → Treasure <em>Chest (Cofre)</em>!',
        "shortcutHi": '<strong>1. Chhaati (Body)</strong> ≈ Sounds like <strong>"Chat-Heart"</strong> beating in your <em>Chest (Chhaati)</em>!<br><strong>2. Sandook / Peti (Box)</strong> ≈ <strong>Peti</strong> is the exact same word as Tamil <strong>பெட்டி (Petti = Box/Chest!)</strong>!'
    },
    1069: { #BEAR
        "tamil": "1. கரடி (Animal) / 2. தாங்கிக்கொள் (Endure)",
        "es": "1. Animal: oso | 2. Endure: soportar (aguantar)",
        "hi": "1. Animal: bhaaloo | 2. Endure: sehna / bardaasht karna",
        "shortcutEs": '<strong>1. Oso (Animal)</strong> ≈ Sounds like <strong>"Oh-So-Big!"</strong> → A huge grizzly <em>Bear (Oso)</em>!<br><strong>2. Soportar (Endure)</strong> ≈ Cognate with <strong>"Support"</strong> → To <em>Bear / Endure</em>!',
        "shortcutHi": '<strong>1. Bhaaloo (Animal)</strong> ≈ Famous Jungle Book bear <strong>"Baloo"</strong> = <em>Bear (Bhaaloo)</em>!<br><strong>2. Sehna (Endure)</strong> ≈ Same root as Tamil <strong>சகிப்பு (Sahippu = Tolerate/Bear!)</strong>!'
    },
    1093: { # DUCK
        "tamil": "1. வாத்து (Bird) / 2. குனிந்து தப்பி (Bend down)",
        "es": "1. Bird: pato | 2. Bend: agacharse",
        "hi": "1. Bird: batakh | 2. Bend: jhukna",
        "shortcutEs": '<strong>1. Pato (Bird)</strong> ≈ Sounds like <strong>"Paddle-Toe"</strong> → Web-footed <em>Duck (Pato)</em> paddling in water!<br><strong>2. Agacharse (Bend)</strong> ≈ Sounds like <strong>"Ah-Gotcha-Low!"</strong> → <em>Duck</em> your head down!',
        "shortcutHi": '<strong>1. Batakh (Bird)</strong> ≈ Sounds right like Tamil <strong>வாத்து (Vaathu ↔ Batakh = Duck!)</strong>!<br><strong>2. Jhukna (Bend)</strong> ≈ Sounds like <strong>"Juke-Down"</strong> → Quickly bend/duck down = <em>Duck (Jhukna)</em>!'
    },
}

MULTI_MEANING_OVERRIDES.update(MORE_MULTI_MEANING)

# Read HINDI_DATA from enrich_hindi_translations.py safely without executing its main script
with open("scripts/enrich_hindi_translations.py", "r", encoding="utf-8") as f:
    eh_src = f.read()
eh_dict_code = eh_src.split('print(f"Loaded')[0]
eh_ns = {}
exec(eh_dict_code, eh_ns)
HINDI_DATA = eh_ns.get("HINDI_DATA", {})

# Fix the 5 typos in HINDI_DATA and ensure Roman Hindi is ALWAYS first!
HINDI_DATA["TURKEY"] = ("padu-murga / peru-pakshi", "पादु-मुर्गा", "")
HINDI_DATA["SQUID"] = ("samudri-feni / dashbhuji", "समुद्री फेनी", "")
HINDI_DATA["WARDEN"] = ("kaaraagaar-adhyaksh / bandi-paal", "कारागार अध्यक्ष", "")
HINDI_DATA["JET LAG"] = ("hawai-safar ki thakaan", "हवाई सफ़र की थकान", "")
HINDI_DATA["AISLE SEAT"] = ("galiyare-wali seat", "गलियारे वाली सीट", "")

# Load backup_original_cards.json for 1-1000 handcrafted mnemonics and original unique URLs
with open("data/backup_original_cards.json", "r", encoding="utf-8") as f:
    backup_list = json.load(f)
BACKUP_BY_NUM = {int(c.get("originalNum") or c.get("num")): c for c in backup_list}

def strip_devanagari(text):
    if not text:
        return ""
    s = re.sub(r"[\u0900-\u097F]+", "", str(text))
    s = re.sub(r"\(\s*[\s/,-]*\)", "", s)
    s = re.sub(r"\s{2,}", " ", s).strip()
    return s

def flip_english_first_hi(word, hi_str):
    """
    Ensures authentic Roman Hindi ALWAYS comes first in card.trans.hi!
    Never allows English word first when a Hindi word exists.
    """
    if not hi_str:
        return hi_str
    s = strip_devanagari(hi_str)
    # Remove redundant labels
    s = re.sub(r"\s*\(same meaning\)", "", s, flags=re.I)
    s = re.sub(r"\s*\(space\)", "", s, flags=re.I)

    # Handle "word1 (spoken) / word2 (formal)" or "word1 (daily) / word2 (spoken)"
    m = re.match(r"^(.+?)\s*\((?:spoken|daily|daily spoken)\)\s*/\s*(.+?)\s*\((?:formal|spoken|daily)\)$", s, flags=re.I)
    if m:
        p1, p2 = m.group(1).strip(), m.group(2).strip()
        p1 = re.sub(r"\((?:spoken|formal|daily)\)", "", p1, flags=re.I).strip()
        p2 = re.sub(r"\((?:spoken|formal|daily)\)", "", p2, flags=re.I).strip()
        w_low = word.lower().strip()
        if p1.lower().startswith(w_low) or p1.lower() in ("healthy", "cousin", "skin", "reminder", "partner", "spam", "blender", "thermos", "window blinds", "deodorant", "price tag", "warranty", "parcel", "courier wala", "pancake", "popcorn", "muffin", "ice cream", "mood", "depression", "cardigan", "officer", "contractor", "chef", "artist", "musician", "journalist", "resign", "raincoat", "customer", "associate", "emi", "handbag", "investment", "risk", "sports shoes", "laundry shop", "hair salon", "medical store", "pharmacist", "daily diary", "exam pad", "letterbox", "underpass", "flyover", "parliament", "council", "ministry", "governor", "candidate", "nominee", "embassy", "ambassador", "army", "navy", "ceasefire", "editorial", "student", "homework", "quiz", "scholarship", "geography", "maths", "astronomy", "philosophy", "economics", "grammar", "hypothesis", "method", "statistics", "equation", "atom", "energy", "gravity", "moody", "exhibition", "capsule", "workshop", "internship", "intern", "feedback", "slideshow", "excel sheet", "fertilizer", "pesticide", "subscription", "ingredients", "renewal", "surgery", "syringe", "painkiller", "vaccine", "arm sling", "ego", "extrovert", "inspection", "lifeguard", "security guard", "capacity", "limit", "minimum", "temporary", "washing powder", "torch"):
            return f"{p2} (or {p1})"
        else:
            return f"{p1} / {p2}"

    # Strip any remaining (spoken), (formal), (daily)
    s = re.sub(r"\s*\((?:spoken|formal|daily|daily spoken)\)", "", s, flags=re.I).strip()

    # Check if format is "english_word (hindi_word)" e.g. "bake karna (sekna)", "patient (mareez)", "cup (pyaala)"
    m2 = re.match(r"^([A-Za-z\s\-]+?)\s*\(([^()]+)\)$", s)
    if m2:
        first_p, inside_p = m2.group(1).strip(), m2.group(2).strip()
        w_base = word.lower().split("/")[0].split("(")[0].strip()
        if first_p.lower() == w_base or first_p.lower() == w_base + " karna" or first_p.lower().startswith(w_base):
            return f"{inside_p} (or {first_p})"

    # Check if format is "english_word / hindi_word" where first part is identical to English word
    if "/" in s and "|" not in s and "1." not in s:
        parts = [p.strip() for p in s.split("/")]
        w_base = word.lower().split("/")[0].split("(")[0].strip()
        if len(parts) == 2 and (parts[0].lower() == w_base or parts[0].lower() == w_base + " karna" or parts[0].lower().startswith(w_base + " ")):
            if parts[1].lower() != w_base:
                return f"{parts[1]} (or {parts[0]})"

    return s

def strip_acc(s):
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFD", str(s)) if unicodedata.category(c) != "Mn")

def find_cognate(eng_word, target_word):
    w = re.sub(r"[^a-z]", "", strip_acc(eng_word.lower()))
    t = re.sub(r"[^a-z]", "", strip_acc(target_word.lower()))
    if not w or not t:
        return False
    if w == t:
        return True
    if len(w) >= 4 and len(t) >= 4 and (w[:4] == t[:4] or w[:5] in t or t[:5] in w):
        return True
    return False

# Phonetic syllable sound-alike generator for any Spanish or Hindi word not in explicit dict
ES_SYLLABLE_SOUNDS = {
    "ab": '"Up"', "ac": '"Act"', "ad": '"Add"', "af": '"After"', "ag": '"Ago"',
    "al": '"All"', "am": '"Aim"', "an": '"On"', "ap": '"App"', "ar": '"Art"',
    "as": '"Ace"', "at": '"At"', "av": '"Avenue"', "ay": '"Aye!"', "az": '"Azure"',
    "ba": '"Bar"', "be": '"Bell"', "bi": '"Bee"', "bl": '"Blue"', "bo": '"Boat"',
    "br": '"Bright"', "bu": '"Boom"', "ca": '"Car"', "ce": '"Center"', "ch": '"Cheer"',
    "ci": '"City"', "cl": '"Clear"', "co": '"Coat"', "cr": '"Crown"', "cu": '"Cup"',
    "da": '"Dart"', "de": '"Day"', "di": '"Deep"', "do": '"Door"', "dr": '"Drive"',
    "du": '"Dune"', "ec": '"Echo"', "el": '"El"', "em": '"Embark"', "en": '"Enter"',
    "es": '"Star"', "ex": '"Extra"', "fa": '"Far"', "fe": '"Feather"', "fi": '"Fine"',
    "fl": '"Flash"', "fo": '"Fort"', "fr": '"Fresh"', "fu": '"Full"', "ga": '"Garden"',
    "ge": '"Gem"', "gi": '"Giant"', "gl": '"Glow"', "go": '"Goal"', "gr": '"Grand"',
    "gu": '"Guard"', "ha": '"Harbor"', "he": '"Hero"', "hi": '"High"', "ho": '"Home"',
    "hu": '"Huge"', "ig": '"Ignite"', "il": '"Illuminate"', "im": '"Impact"', "in": '"Inner"',
    "ir": '"Iron"', "is": '"Island"', "ja": '"Jar"', "je": '"Jet"', "jo": '"Joy"',
    "ju": '"Jump"', "la": '"La-La"', "le": '"Lemon"', "li": '"Light"', "ll": '"Yacht"',
    "lo": '"Low"', "lu": '"Lunar"', "ma": '"Mark"', "me": '"Mega"', "mi": '"Mini"',
    "mo": '"Motor"', "mu": '"Music"', "na": '"Nature"', "ne": '"Net"', "ni": '"Neat"',
    "no": '"Note"', "nu": '"New"', "ob": '"Object"', "oc": '"Ocean"', "of": '"Offer"',
    "ol": '"Olive"', "om": '"Omega"', "op": '"Open"', "or": '"Orbit"', "os": '"Oasis"',
    "pa": '"Park"', "pe": '"Pen"', "pi": '"Peak"', "pl": '"Plaza"', "po": '"Pocket"',
    "pr": '"Prime"', "pu": '"Pure"', "qu": '"Key"', "ra": '"Radar"', "re": '"Ray"',
    "ri": '"River"', "ro": '"Road"', "ru": '"Ruby"', "sa": '"Salt"', "se": '"Set"',
    "si": '"See"', "so": '"Solar"', "su": '"Super"', "ta": '"Tap"', "te": '"Tent"',
    "ti": '"Ticket"', "to": '"Top"', "tr": '"Track"', "tu": '"Tune"', "ul": '"Ultra"',
    "un": '"One"', "ur": '"Urban"', "us": '"Use"', "va": '"Valley"', "ve": '"Vent"',
    "vi": '"View"', "vo": '"Voice"', "vu": '"Vault"', "ya": '"Yacht"', "ye": '"Yes"',
    "yo": '"Yo!"', "za": '"Zap"', "zo": '"Zone"'
}

HI_SYLLABLE_SOUNDS = {
    "aa": '"Ah-Open"', "ab": '"Up"', "ad": '"Add"', "af": '"Officer"', "ag": '"Ahead"',
    "ah": '"Aha!"', "ai": '"Eye"', "aj": '"Edge"', "ak": '"Act"', "al": '"All"',
    "am": '"Mango"', "an": '"Inner"', "ap": '"Up"', "ar": '"Arch"', "as": '"Ace"',
    "at": '"At"', "au": '"Auto"', "av": '"Avenue"', "ba": '"Bus"', "bh": '"Bharat"',
    "bi": '"Bee"', "bo": '"Bowl"', "bu": '"Bull"', "ch": '"Chai"', "da": '"Dart"',
    "dh": '"Drum"', "di": '"Deep"', "do": '"Door"', "du": '"Dune"', "ek": '"Ace-One"',
    "fa": '"Fast"', "fi": '"Fit"', "fu": '"Full"', "ga": '"Garden"', "gh": '"Ghat"',
    "gi": '"Gear"', "go": '"Goal"', "gu": '"Guru"', "ha": '"Hand"', "hi": '"Hill"',
    "ho": '"Home"', "hu": '"Hub"', "id": '"Idli"', "ij": '"Easy"', "il": '"Heal"',
    "im": '"Image"', "in": '"In"', "ir": '"Iron"', "is": '"East"', "it": '"Brick"',
    "ja": '"Jar"', "jh": '"Jump"', "ji": '"Jeeva"', "jo": '"Join"', "ju": '"Juice"',
    "ka": '"Car"', "kh": '"Key"', "ki": '"Key"', "ko": '"Coat"', "ku": '"Cool"',
    "la": '"Lamp"', "le": '"Letter"', "li": '"Line"', "lo": '"Lock"', "lu": '"Loot"',
    "ma": '"Maha"', "me": '"Mega"', "mi": '"Meet"', "mo": '"Motor"', "mu": '"Mouth"',
    "na": '"New"', "ne": '"Net"', "ni": '"Near"', "no": '"Note"', "nu": '"New"',
    "oo": '"Up-High"', "pa": '"Park"', "ph": '"Flower"', "pi": '"Peak"', "po": '"Pot"',
    "pr": '"Prime"', "pu": '"Bridge"', "qa": '"Law"', "ra": '"Royal"', "re": '"Ray"',
    "ri": '"Ring"', "ro": '"Road"', "ru": '"Root"', "sa": '"Same"', "sh": '"Shine"',
    "si": '"See"', "so": '"Gold"', "su": '"Super"', "ta": '"Star"', "th": '"Thali"',
    "ti": '"Tick"', "to": '"Top"', "tu": '"Tune"', "ud": '"Up"', "uj": '"Bright"',
    "ul": '"Ultra"', "um": '"Hope"', "un": '"Wool"', "up": '"Upper"', "ur": '"Energy"',
    "ut": '"Rise"', "va": '"Vaayu"', "vi": '"Victory"', "vy": '"Trade"', "ya": '"Yatra"',
    "yo": '"Yoga"', "yu": '"Youth"', "za": '"Land"', "zi": '"Zip"', "zu": '"Zoom"'
}

def build_single_es_shortcut(word, es_trans, backup_es=""):
    es_main = re.sub(r"\s*\(.*?\)", "", es_trans).split("/")[0].split("|")[0].strip()
    es_low = es_main.lower()
    es_cap = es_main[:1].upper() + es_main[1:] if es_main else word.title()
    w_title = word.title()

    # 1. Exact or base match in ES_SOUND_ALIKES
    if es_low in ES_SOUND_ALIKES:
        return ES_SOUND_ALIKES[es_low]
    for cand in [p.strip().lower() for p in re.split(r"[/|()]", es_trans) if p.strip()]:
        if cand in ES_SOUND_ALIKES:
            return ES_SOUND_ALIKES[cand]

    # 2. Check if backup_es is a high-quality handcrafted mnemonic (from 1-1000)
    if backup_es:
        pl = re.sub(r"<[^>]+>", "", backup_es)
        bad_markers = ["Core Spanish", "Everyday spoken", "Sound-alike", "Colline", "Llanos", "Torpid", "Suborn", "Assent", "Adulate", "Pot-au-feu", "Burla", "Cuervo"]
        if not any(bm in pl for bm in bad_markers):
            if any(gm in pl for gm in ["Sounds like", "Think of", "Picture", "Imagine", "Same as", "Similar to", "Cognate", "cognate", "Root", "root", "Famous", "Like ", "Drop ", "Add ", "Simply ", "Built ", "Direct match", "Direct sibling", "99% identical", "100% identical"]):
                return backup_es

    # 3. Direct English cognate check
    for tok in re.split(r"[\s/(),]+", es_main):
        if len(tok) >= 4 and find_cognate(word, tok):
            return f'<strong>{es_cap}</strong> ≈ Sounds right like English <strong>"{w_title}"</strong> (same Latin root &amp; sound) → <em>{w_title} ({es_cap})</em>!'

    # 4. Multi-word phrase breakdown
    tokens = [t for t in re.split(r"\s+", es_low) if t and t not in ("de", "del", "la", "el", "los", "las", "en", "a", "al", "por", "para", "con", "un", "una", "se")]
    parts_found = []
    for t in tokens:
        if t in ES_SOUND_ALIKES:
            m = re.search(r"≈\s*(.+?)\s*→", ES_SOUND_ALIKES[t])
            if m:
                parts_found.append(f"<strong>{t.capitalize()}</strong> ({m.group(1)})")
        elif find_cognate(word, t):
            parts_found.append(f'<strong>{t.capitalize()}</strong> (like "{w_title}")')
    if parts_found:
        joined = " + ".join(parts_found[:2])
        return f'<strong>{es_cap}</strong> ≈ {joined} → <em>{w_title} ({es_cap})</em>!'

    # 5. Phonetic sound-alike bridge from first syllable
    clean_alpha = re.sub(r"[^a-z]", "", strip_acc(es_low))
    prefix2 = clean_alpha[:2]
    cue = ES_SYLLABLE_SOUNDS.get(prefix2, f'"{clean_alpha[:3].capitalize()}"')
    return f'<strong>{es_cap}</strong> ≈ Sounds like <strong>{cue}</strong> → Picture {cue} to remember <em>{w_title} ({es_cap})</em>!'

def build_single_hi_shortcut(word, hi_trans, tamil_str="", backup_hi=""):
    hi_main = re.sub(r"\s*\(.*?\)", "", hi_trans).split("/")[0].split("|")[0].strip()
    hi_low = hi_main.lower()
    hi_cap = hi_main[:1].upper() + hi_main[1:] if hi_main else word.title()
    w_title = word.title()

    # 1. Exact or base match in HI_SOUND_ALIKES
    if hi_low in HI_SOUND_ALIKES:
        return HI_SOUND_ALIKES[hi_low]
    hi_stem = re.sub(r"\s+(karna|hona|dena|lena|jaana|aana|padna|lagna)$", "", hi_low).strip()
    if hi_stem in HI_SOUND_ALIKES:
        return HI_SOUND_ALIKES[hi_stem]
    for cand in [p.strip().lower() for p in re.split(r"[/|()]", hi_trans) if p.strip()]:
        cand_clean = re.sub(r"^(or|formal|spoken):\s*", "", cand).strip()
        if cand_clean in HI_SOUND_ALIKES:
            return HI_SOUND_ALIKES[cand_clean]
        cand_stem = re.sub(r"\s+(karna|hona|dena|lena)$", "", cand_clean).strip()
        if cand_stem in HI_SOUND_ALIKES:
            return HI_SOUND_ALIKES[cand_stem]

    # 2. Check if backup_hi is a high-quality handcrafted mnemonic (from 1-1000) without proverbs/movies/bare defs
    if backup_hi:
        b_clean = strip_devanagari(backup_hi)
        pl = re.sub(r"<[^>]+>", "", b_clean)
        bad_markers = [
            "Core Spanish", "Everyday spoken", "Sound-alike", "Direct English loanword",
            "Action verb", "Combine the parts", "Proverb", "proverb", "Idiom", "idiom",
            "movie", "Movie", "film", "Film", "song", "Song", "Bollywood", "superstition"
        ]
        if not any(bm in pl for bm in bad_markers):
            if any(gm in pl for gm in ["Sounds like", "Think of", "Picture", "Imagine", "Same as", "Spoken Tamil", "Tamil ", "Similar to", "Famous", "Like ", "Opposite", "+", "From "]):
                return b_clean

    # 3. Compound Hindi breakdown (e.g., "rasoi-ghar", "khel-maidaan", "... karna")
    tokens = [t for t in re.split(r"[\s\-]+", hi_low) if t and t not in ("ka", "ki", "ke", "mein", "se", "ko", "par", "wala", "wali", "wale", "karna", "hona", "dena", "lena")]
    parts_found = []
    for t in tokens:
        if t in HI_SOUND_ALIKES:
            m = re.search(r"≈\s*(.+?)\s*→", HI_SOUND_ALIKES[t])
            if m:
                parts_found.append(f"<strong>{t.capitalize()}</strong> ({m.group(1)})")
    if parts_found:
        joined = " + ".join(parts_found[:2])
        return f'<strong>{hi_cap}</strong> ≈ {joined} → <em>{w_title} ({hi_cap})</em>!'

    # 4. Phonetic sound-alike bridge from first syllable
    clean_alpha = re.sub(r"[^a-z]", "", strip_acc(hi_low))
    prefix2 = clean_alpha[:2]
    cue = HI_SYLLABLE_SOUNDS.get(prefix2, f'"{clean_alpha[:3].capitalize()}"')
    return f'<strong>{hi_cap}</strong> ≈ Sounds like <strong>{cue}</strong> → Link {cue} to <em>{w_title} ({hi_cap})</em>!'

def upgrade_multi_sense_shortcuts(card):
    """
    Ensures every multi-meaning card (with 1. ... | 2. ...) has genuine sound-alike/root/Tamil
    mnemonics for BOTH Sense 1 and Sense 2!
    """
    num = int(card.get("originalNum") or card.get("num"))
    if num in MULTI_MEANING_OVERRIDES:
        ov = MULTI_MEANING_OVERRIDES[num]
        card["tamil"] = ov["tamil"]
        card["trans"]["es"] = ov["es"]
        card["trans"]["hi"] = ov["hi"]
        card["shortcutEs"] = ov["shortcutEs"]
        card["shortcutHi"] = ov["shortcutHi"]
        return

    raw_es = card["trans"]["es"]
    raw_hi = card["trans"]["hi"]
    is_multi = ("|" in raw_es) or ("|" in raw_hi) or ("1." in raw_es and "2." in raw_es)
    if not is_multi:
        return

    def parse_two_parts(raw_str):
        parts = re.split(r"\s*\|\s*|\s*/\s*(?=2\.)", raw_str)
        if len(parts) < 2:
            parts = [raw_str, raw_str]
        out = []
        for p in parts[:2]:
            clean = re.sub(r"^[12]\.\s*", "", p).strip()
            label = ""
            m = re.match(r"^([A-Za-z0-9\s/&\-()]+):\s*(.+)$", clean)
            if m:
                label = m.group(1).strip()
                clean = m.group(2).strip()
            out.append((label, clean))
        return out

    es_parts = parse_two_parts(raw_es)
    hi_parts = parse_two_parts(raw_hi)

    cur_ses = strip_devanagari(card.get("shortcutEs", "")).split("<br>")
    cur_shi = strip_devanagari(card.get("shortcutHi", "")).split("<br>")

    new_ses = []
    new_shi = []
    for idx in range(2):
        lbl_e, txt_e = es_parts[idx]
        lbl_h, txt_h = hi_parts[idx]
        sense_word = lbl_e or lbl_h or card["word"]

        existing_e = cur_ses[idx].strip() if idx < len(cur_ses) else ""
        pl_e = re.sub(r"<[^>]+>", "", existing_e)
        if existing_e and any(k in pl_e for k in ["Sounds like", "Similar to", "Same as", "Cognate", "cognate", "sibling", "Sibling", "Root", "root", "Direct match", "+", "From "]):
            if not existing_e.startswith(f"<strong>{idx+1}."):
                existing_e = re.sub(r"^<strong>\s*(?:[12]\.\s*)?", f"<strong>{idx+1}. ", existing_e)
            new_ses.append(existing_e)
        else:
            built_e = build_single_es_shortcut(sense_word, txt_e)
            built_e = re.sub(r"^<strong>", f"<strong>{idx+1}. ", built_e)
            new_ses.append(built_e)

        existing_h = cur_shi[idx].strip() if idx < len(cur_shi) else ""
        pl_h = re.sub(r"<[^>]+>", "", existing_h)
        if existing_h and any(k in pl_h for k in ["Sounds like", "Similar to", "Same as", "Spoken Tamil", "Tamil", "+", "From ", "Opposite"]) and "Outer space in the sky" not in pl_h:
            if not existing_h.startswith(f"<strong>{idx+1}."):
                existing_h = re.sub(r"^<strong>\s*(?:[12]\.\s*)?", f"<strong>{idx+1}. ", existing_h)
            new_shi.append(existing_h)
        else:
            built_h = build_single_hi_shortcut(sense_word, txt_h, card.get("tamil", ""))
            built_h = re.sub(r"^<strong>", f"<strong>{idx+1}. ", built_h)
            new_shi.append(built_h)

    card["shortcutEs"] = "<br>".join(new_ses)
    card["shortcutHi"] = "<br>".join(new_shi)

# ============================================================================
# 5. BATCH WIKIPEDIA PAGEIMAGES RESOLVER FOR MISALIGNED / REPEATED IMAGES
# ============================================================================
WIKI_QUERY_OVERRIDES = {
    "ATMOSPHERE": "Atmosphere of Earth",
    "SPACE": "Outer space",
    "MUD": "Mud",
    "HILL": "Hill",
    "PLAIN": "Plain",
    "MEADOW": "Meadow",
    "SWAMP": "Swamp",
    "MARSH": "Marsh",
    "CONTINENT": "Continent",
    "CAPE": "Headland",
    "PENINSULA": "Peninsula",
    "ARCHIPELAGO": "Archipelago",
    "TIDE": "Tide",
    "CURRENT": "Ocean current",
    "SPRING": "Spring (hydrology)",
    "POND": "Pond",
    "STREAM": "Stream",
    "CREEK": "Stream",
    "DAM": "Dam",
    "CANAL": "Canal",
    "DITCH": "Ditch",
    "BREEZE": "Wind",
    "GALE": "Gale",
    "HURRICANE": "Tropical cyclone",
    "TORNADO": "Tornado",
    "CYCLONE": "Tropical cyclone",
    "TYPHOON": "Typhoon",
    "BLIZZARD": "Blizzard",
    "DRIZZLE": "Drizzle",
    "HAIL": "Hail",
    "SLEET": "Rain and snow mixed",
    "FROST": "Frost",
    "DEW": "Dew",
    "MIST": "Mist",
    "RAINBOW": "Rainbow",
    "DROUGHT": "Drought",
    "LANDSLIDE": "Landslide",
    "AVALANCHE": "Avalanche",
    "VOLCANO": "Volcano",
    "LAVA": "Lava",
    "ASH": "Volcanic ash",
    "STONE": "Rock (geology)",
    "PEBBLE": "Pebble",
    "BOULDER": "Boulder",
    "CLAY": "Clay",
    "COAL": "Coal",
    "COPPER": "Copper",
    "BRONZE": "Bronze",
    "BRASS": "Brass",
    "STEEL": "Steel",
    "TIN": "Tin",
    "LEAD": "Lead",
    "ZINC": "Zinc",
    "MAGNET": "Magnet",
    "GEM": "Gemstone",
    "JEWEL": "Jewellery",
    "PEARL": "Pearl",
    "CRYSTAL": "Crystal",
    "BULL": "Bull",
    "CALF": "Calf (animal)",
    "LAMB": "Sheep",
    "DONKEY": "Donkey",
    "MULE": "Mule",
    "CAMEL": "Camel",
    "DEER": "Deer",
    "FOX": "Fox",
    "WOLF": "Wolf",
    "BEAR": "Bear",
    "PANDA": "Giant panda",
    "KANGAROO": "Kangaroo",
    "KOALA": "Koala",
    "ZEBRA": "Zebra",
    "GIRAFFE": "Giraffe",
    "HIPPOPOTAMUS": "Hippopotamus",
    "RHINOCEROS": "Rhinoceros",
    "LEOPARD": "Leopard",
    "CHEETAH": "Cheetah",
    "SQUIRREL": "Squirrel",
    "BAT": "Bat",
    "RAT": "Rat",
    "FROG": "Frog",
    "TOAD": "Toad",
    "TURTLE": "Turtle",
    "TORTOISE": "Tortoise",
    "CROCODILE": "Crocodile",
    "ALLIGATOR": "Alligator",
    "LIZARD": "Lizard",
    "DINOSAUR": "Dinosaur",
    "DUCK": "Duck",
    "GOOSE": "Goose",
    "SWAN": "Swan",
    "TURKEY": "Turkey (bird)",
    "ROOSTER": "Rooster",
    "HEN": "Chicken",
    "EAGLE": "Eagle",
    "HAWK": "Hawk",
    "OWL": "Owl",
    "PARROT": "Parrot",
    "CROW": "Crow",
    "PIGEON": "Columbidae",
    "DOVE": "Columbidae",
    "SPARROW": "Passer",
    "PEACOCK": "Peafowl",
    "PENGUIN": "Penguin",
    "OSTRICH": "Common ostrich",
    "WHALE": "Whale",
    "SHARK": "Shark",
    "DOLPHIN": "Dolphin",
    "SEAL": "Pinniped",
    "OCTOPUS": "Octopus",
    "SQUID": "Squid",
    "JELLYFISH": "Jellyfish",
    "CRAB": "Crab",
    "LOBSTER": "Lobster",
    "SHRIMP": "Shrimp",
    "PRAWN": "Prawn",
    "OYSTER": "Oyster",
    "SNAIL": "Snail",
    "WORM": "Earthworm",
    "SPIDER": "Spider",
    "SCORPION": "Scorpion",
    "BEETLE": "Beetle",
    "COCKROACH": "Cockroach",
    "CRICKET": "Cricket (sport)",
    "GRASSHOPPER": "Grasshopper",
    "LADYBUG": "Coccinellidae",
    "DRAGONFLY": "Dragonfly",
    "CATERPILLAR": "Caterpillar",
    "THUNDER": "Thunderstorm",
    "SHADE": "Shade (shadow)",
    "GROUND": "Soil",
    "ROCK": "Rock (geology)",
    "FIELD": "Field (agriculture)",
    "CLICK": "Computer mouse",
    "DOWNLOAD": "Download",
    "UPLOAD": "Upload",
    "ROUTER": "Router (computing)",
    "HOTSPOT": "Wi-Fi",
    "OUTLET": "AC power plugs and sockets",
    "EARBUDS": "Headphones",
    "EARPHONE": "Headphones",
    "STOPWATCH": "Stopwatch",
    "TABLET": "Tablet computer",
    "BLENDER": "Blender",
    "LADLE": "Ladle (spoon)",
    "SPATULA": "Spatula",
    "TUPPERWARE": "Tupperware",
    "FOIL": "Aluminium foil",
    "COASTER": "Drink coaster",
    "DOORMAT": "Mat",
    "BEDSHEET": "Bed sheet",
    "HANGER": "Clothes hanger",
    "FLOSS": "Dental floss",
    "CONDITIONER": "Hair conditioner",
    "PERFUME": "Perfume",
    "TISSUE": "Facial tissue",
    "TROLLEY": "Shopping cart",
    "DELIVERY": "Package delivery",
    "PARCEL": "Mail",
    "BURGER": "Hamburger",
    "MUSTARD": "Mustard (condiment)",
    "BRIDE": "Bride",
    "GROOM": "Bridegroom",
    "WATCHMAN": "Security guard",
    "CARETAKER": "Janitor",
}

def batch_fetch_wiki_images(words_by_num):
    """
    Fetches real 800px Wikipedia thumbnails in batches of 45 titles with Wikimedia-compliant User-Agent & polite pacing.
    """
    import time
    from collections import Counter
    cache_path = "scripts/wiki_batch_resolved.json"
    resolved = {}

    # Count URL frequencies in backup so we NEVER copy repeated generic Unsplash URLs
    backup_urls = [bc.get("imageUrl", "") for bc in BACKUP_BY_NUM.values() if bc.get("imageUrl")]
    backup_url_counts = Counter(backup_urls)

    if os.path.exists(cache_path):
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                raw_cache = json.load(f)
            raw_counts = Counter(v for v in raw_cache.values() if v)
            for k, v in raw_cache.items():
                if v and ("wikimedia.org" in v or raw_counts[v] == 1):
                    resolved[str(k)] = v
        except Exception:
            resolved = {}

    if os.path.exists("wiki_thumbs.json"):
        try:
            with open("wiki_thumbs.json", "r", encoding="utf-8") as f:
                wt = json.load(f)
            for k, v in wt.items():
                if v and isinstance(v, str) and "wikimedia.org" in v:
                    resolved[str(k)] = v
        except Exception:
            pass

    # Only keep TRULY UNIQUE (count == 1) or Wikimedia URLs from backup_original_cards.json
    for num_int, bc in BACKUP_BY_NUM.items():
        b_url = bc.get("imageUrl", "")
        if b_url and ("wikimedia.org" in b_url or backup_url_counts[b_url] == 1) and str(num_int) not in resolved:
            resolved[str(num_int)] = b_url

    to_query = []
    for num, word in words_by_num.items():
        cur = resolved.get(str(num), "")
        if cur and "wikimedia.org" in cur and num not in (1021, 1022, 1032, 1038, 1043):
            continue
        w_clean = re.sub(r"\s*\(.*?\)", "", word).split("/")[0].strip()
        title = WIKI_QUERY_OVERRIDES.get(word.upper(), w_clean.capitalize())
        to_query.append((str(num), title))

    print(f"Fetching Wikipedia pageimages for {len(to_query)} cards in batches of 45...")
    batch_size = 45
    headers = {
        "User-Agent": "StellarMultilingualFlashcards/2.0 (https://stellar.cloud; support@stellar.cloud) Python-urllib/3.10"
    }
    for i in range(0, len(to_query), batch_size):
        batch = to_query[i:i + batch_size]
        titles_map = {}
        for num_str, t in batch:
            titles_map.setdefault(t, []).append(num_str)
        titles_param = "|".join(titles_map.keys())
        url = (
            "https://en.wikipedia.org/w/api.php?action=query"
            f"&titles={urllib.parse.quote(titles_param)}"
            "&prop=pageimages&pithumbsize=800&redirects=1&format=json"
        )
        for attempt in range(3):
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                query_obj = data.get("query", {})
                norm_map = {n["from"]: n["to"] for n in query_obj.get("normalized", [])}
                redir_map = {r["from"]: r["to"] for r in query_obj.get("redirects", [])}
                pages = query_obj.get("pages", {})
                title_to_thumb = {}
                for _, p in pages.items():
                    thumb = p.get("thumbnail", {}).get("source", "")
                    if thumb and not thumb.lower().endswith(".svg") and "flag_of" not in thumb.lower() and "commons-logo" not in thumb.lower():
                        title_to_thumb[p.get("title", "")] = thumb

                for orig_t, num_list in titles_map.items():
                    t1 = norm_map.get(orig_t, orig_t)
                    t2 = redir_map.get(t1, t1)
                    thumb_url = title_to_thumb.get(t2) or title_to_thumb.get(t1) or title_to_thumb.get(orig_t)
                    if thumb_url:
                        for n_s in num_list:
                            resolved[n_s] = thumb_url
                time.sleep(0.28)
                break
            except Exception as e:
                if "429" in str(e) and attempt < 2:
                    time.sleep(1.5 * (attempt + 1))
                else:
                    print(f"Batch {i} note: {e}")
                    break

    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(resolved, f, indent=2)
    return resolved

def main():
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    acc_img_path = "scripts/accurate_images.json"
    with open(acc_img_path, "r", encoding="utf-8") as f:
        acc_images = json.load(f)

    from collections import Counter
    url_counts = Counter(acc_images.values())

    deck_pattern = re.compile(r"(var\s+(tier\w+DeckCards|initialDeckCards)\s*=\s*)(\[[\s\S]*?\])(;)")
    matches = list(deck_pattern.finditer(html))
    print(f"Found {len(matches)} deck arrays in index.html")

    words_needing_wiki = {}
    for m in matches:
        cards = json.loads(m.group(3))
        for c in cards:
            num = int(c.get("originalNum") or c.get("num"))
            cur_url = acc_images.get(str(num)) or c.get("imageUrl", "")
            if not cur_url or url_counts.get(cur_url, 0) > 2 or num in (1021, 1022, 1032, 1038, 1043):
                words_needing_wiki[num] = c["word"]

    wiki_resolved = batch_fetch_wiki_images(words_needing_wiki)
    print(f"Resolved {len(wiki_resolved)} exact concept photos!")

    card_shortcuts_map = {}
    total_updated = 0

    def replace_deck(match):
        nonlocal total_updated
        prefix = match.group(1)
        deck_name = match.group(2)
        cards = json.loads(match.group(3))
        suffix = match.group(4)

        for c in cards:
            num = int(c.get("originalNum") or c.get("num"))
            word = c["word"].strip()
            backup_c = BACKUP_BY_NUM.get(num, {})

            # 1. Clean & upgrade Hindi & Spanish translations (Authentic Roman Hindi ALWAYS first!)
            if num in AUTHENTIC_HI_FIRST:
                c["trans"]["hi"] = AUTHENTIC_HI_FIRST[num]
            elif word.upper() in HINDI_DATA and "|" not in c["trans"]["hi"] and "1." not in c["trans"]["hi"]:
                rom_hi, _, _ = HINDI_DATA[word.upper()]
                c["trans"]["hi"] = flip_english_first_hi(word, strip_devanagari(rom_hi))
            else:
                c["trans"]["hi"] = flip_english_first_hi(word, c["trans"].get("hi", ""))

            c["trans"]["es"] = re.sub(r"\s*\((?:spoken|formal|daily|same meaning)\)", "", strip_devanagari(c["trans"].get("es", "")), flags=re.I).strip()
            c["trans"]["hi"] = strip_devanagari(c["trans"]["hi"])
            c["hiDevanagari"] = strip_devanagari(c["trans"]["hi"])

            # 2. Apply Multi-Meaning or Single-Meaning Shortcuts
            if num in MULTI_MEANING_OVERRIDES or "|" in c["trans"]["es"] or "|" in c["trans"]["hi"] or ("1." in c["trans"]["es"] and "2." in c["trans"]["es"]):
                upgrade_multi_sense_shortcuts(c)
            else:
                c["shortcutEs"] = build_single_es_shortcut(word, c["trans"]["es"], backup_c.get("shortcutEs", ""))
                c["shortcutHi"] = build_single_hi_shortcut(word, c["trans"]["hi"], c.get("tamil", ""), backup_c.get("shortcutHi", ""))

            c["shortcutEs"] = strip_devanagari(c["shortcutEs"])
            c["shortcutHi"] = strip_devanagari(c["shortcutHi"])

            # 3. Assign Concept-Accurate Image
            if str(num) in wiki_resolved and wiki_resolved[str(num)]:
                c["imageUrl"] = wiki_resolved[str(num)]
                acc_images[str(num)] = wiki_resolved[str(num)]
            elif str(num) in acc_images and acc_images[str(num)]:
                c["imageUrl"] = acc_images[str(num)]

            card_shortcuts_map[str(num)] = {
                "es": c["shortcutEs"],
                "hi": c["shortcutHi"]
            }
            total_updated += 1

        print(f"Overhauled {len(cards)} cards in {deck_name}")
        return f"{prefix}{json.dumps(cards, ensure_ascii=False)}{suffix}"

    html = deck_pattern.sub(replace_deck, html)

    html = re.sub(
        r"var\s+cardAccurateImages\s*=\s*\{.*?\};",
        lambda _: f"var cardAccurateImages = {json.dumps(acc_images, ensure_ascii=False)};",
        html,
        flags=re.S
    )

    html = re.sub(
        r"var\s+cardShortcuts\s*=\s*\{.*?\};",
        lambda _: f"var cardShortcuts = {json.dumps(card_shortcuts_map, ensure_ascii=False)};",
        html,
        flags=re.S
    )

    with open(acc_img_path, "w", encoding="utf-8") as f:
        json.dump(acc_images, f, indent=2, ensure_ascii=False)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print(f"SUCCESS: Overhauled {total_updated} card instances across all decks in index.html!")

if __name__ == "__main__":
    main()
