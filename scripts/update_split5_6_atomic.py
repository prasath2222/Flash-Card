#!/usr/bin/env python3
"""
Atomic quality upgrade for Split 5 & Split 6 (#822-#1262, 441 cards in var split5DeckCards + var split6DeckCards):
  1. Aligns all 133 multi-sense Tamil strings to exact 1-to-1 numbered "1. ... / 2. ..." (and 3-sense on #1255) matching parseCardSenses(), fixes swapped #837/#1025 and garbled/leaked single-sense Tamil strings (#952, #1037, #1152, #1156, #1164, #1165, #1178, #1185, #1187, #1195, #1197, #1222, #1238, #1242, #1258).
  2. Eliminates all template slop ("Direct sibling", "Direct match", "Direct English", "Everyday spoken loanword", "Core Spanish/Hindi", "Meaning ...") and fixes wrong homonym leaks (#956 Aam, #1202 Bail, #1217 Patrol, #1222 Koshika, #1260 Haar) in shortcutEs & shortcutHi across all flagged cards in #822-#1262.
  3. Upgrades 54 off-topic/NSFW/EFTA/unclear images (#1237 NSFW, #1190 Alicia Keys, #1195 Boomerang, #1232 Swedish beach house, #1261 bird, #1093 coin mint statue, #931 buzzard, #960 dog, #961 fingernail diagram, etc.) with Wikimedia Commons curated photos.
  4. Syncs split5DeckCards, split6DeckCards, cardShortcuts, and data/backup_original_cards.json 100%.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(ROOT, "index.html")
BACKUP_PATH = os.path.join(ROOT, "data", "backup_original_cards.json")

IMAGE_UPGRADES = {
    898: "https://upload.wikimedia.org/wikipedia/commons/2/2a/Boxing_Tournament_in_Aid_of_King_George%27s_Fund_For_Sailors_at_the_Royal_Naval_Air_Station%2C_Henstridge%2C_Somerset%2C_July_1945_A29806.jpg",
    910: "https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Schleifpapier_verschiedene_Sorten.jpg/960px-Schleifpapier_verschiedene_Sorten.jpg",
    911: "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Cucina_012.jpg/960px-Cucina_012.jpg",
    916: "https://upload.wikimedia.org/wikipedia/commons/7/71/Holey_Tree_%28772111164%29.jpg",
    921: "https://upload.wikimedia.org/wikipedia/commons/c/c2/Wire-and-Wooden-CoatHangers.JPG",
    931: "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Runny_hunny.jpg/960px-Runny_hunny.jpg",
    942: "https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/Australian_Made_CMI_H2D_Home_Safe.JPG/960px-Australian_Made_CMI_H2D_Home_Safe.JPG",
    947: "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Homeless_man_in_Toronto_across_from_old_City_Hall.jpg/960px-Homeless_man_in_Toronto_across_from_old_City_Hall.jpg",
    952: "https://upload.wikimedia.org/wikipedia/commons/a/a6/Matura2005_ILOSzczecin.jpg",
    953: "https://upload.wikimedia.org/wikipedia/commons/b/bd/Codebeispiel_-_Syntax_error.png",
    960: "https://upload.wikimedia.org/wikipedia/commons/f/fe/Angry-2766265_960_720.jpg",
    961: "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Edvard_Munch%2C_1893%2C_The_Scream%2C_oil%2C_tempera_and_pastel_on_cardboard%2C_91_x_73_cm%2C_National_Gallery_of_Norway.jpg/960px-Edvard_Munch%2C_1893%2C_The_Scream%2C_oil%2C_tempera_and_pastel_on_cardboard%2C_91_x_73_cm%2C_National_Gallery_of_Norway.jpg",
    968: "https://upload.wikimedia.org/wikipedia/commons/f/fc/%C4%90%C3%A1nh_ghen.JPG",
    971: "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Prayers-collage.png/960px-Prayers-collage.png",
    978: "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/Crying-girl.jpg/960px-Crying-girl.jpg",
    984: "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Mold_on_a_strawberry.jpg/960px-Mold_on_a_strawberry.jpg",
    985: "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/At_Eternity%27s_Gate_-_Vincent_Van_Gogh.jpg/960px-At_Eternity%27s_Gate_-_Vincent_Van_Gogh.jpg",
    989: "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Charles_Bell%2C_Essays_on_the_anatomy_of_Wellcome_L0031951.jpg/960px-Charles_Bell%2C_Essays_on_the_anatomy_of_Wellcome_L0031951.jpg",
    992: "https://upload.wikimedia.org/wikipedia/commons/c/c0/Heinrich_Vogtherr_d._J._Schalksnarr.JPG",
    1000: "https://upload.wikimedia.org/wikipedia/commons/0/04/Oil_painting_palette.jpg",
    1001: "https://upload.wikimedia.org/wikipedia/commons/b/bc/Banana_%28partially_peeled%29.jpg",
    1002: "https://upload.wikimedia.org/wikipedia/commons/f/f2/Russian_finished_watch_movement.jpg",
    1003: "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Baby_Sofia.jpg/960px-Baby_Sofia.jpg",
    1017: "https://upload.wikimedia.org/wikipedia/commons/thumb/1/19/Crack_climbing_in_Indian_Creek%2C_Utah.jpg/960px-Crack_climbing_in_Indian_Creek%2C_Utah.jpg",
    1024: "https://upload.wikimedia.org/wikipedia/commons/4/42/Shrug.jpg",
    1029: "https://upload.wikimedia.org/wikipedia/commons/0/06/Cfs_woman_sketch.jpg",
    1030: "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Luna_Park_Melbourne_scenic_railway.jpg/960px-Luna_Park_Melbourne_scenic_railway.jpg",
    1031: "https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/Symptoms-headache.jpg/960px-Symptoms-headache.jpg",
    1039: "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Chaplin%2C_Charlie_%28His_New_Job%29_03.jpg/960px-Chaplin%2C_Charlie_%28His_New_Job%29_03.jpg",
    1041: "https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Types_de_plumes._-_Larousse_pour_tous%2C_-1907-1910-.jpg/960px-Types_de_plumes._-_Larousse_pour_tous%2C_-1907-1910-.jpg",
    1055: "https://upload.wikimedia.org/wikipedia/commons/7/76/Pieter_Brueghel_the_Younger_-_Proverbs_%28detail%29_-_WGA03627.jpg",
    1062: "https://upload.wikimedia.org/wikipedia/commons/7/79/Marco_aurelio_e_barbaros_-_museus_capitolinos.jpg",
    1064: "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/Giotto_-_Scrovegni_-_-31-_-_Kiss_of_Judas.jpg/960px-Giotto_-_Scrovegni_-_-31-_-_Kiss_of_Judas.jpg",
    1065: "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Poker_cheating_20170611.jpg/960px-Poker_cheating_20170611.jpg",
    1068: "https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Candy_corn_in_a_jar.png/960px-Candy_corn_in_a_jar.png",
    1078: "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f9/STOP_sign.jpg/960px-STOP_sign.jpg",
    1093: "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Mentha_spicata-IMG_6186.jpg/960px-Mentha_spicata-IMG_6186.jpg",
    1096: "https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/LBJOathOfOffice1963.jpg/960px-LBJOathOfOffice1963.jpg",
    1097: "https://upload.wikimedia.org/wikipedia/commons/6/6c/Mughal43.jpg",
    1142: "https://upload.wikimedia.org/wikipedia/en/thumb/6/62/John_Lewis_Payslip.png/960px-John_Lewis_Payslip.png",
    1145: "https://upload.wikimedia.org/wikipedia/commons/thumb/e/eb/Box.agr.jpg/960px-Box.agr.jpg",
    1152: "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Change_of_work_shift_at_Ford_Motor_Company.jpg/960px-Change_of_work_shift_at_Ford_Motor_Company.jpg",
    1155: "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Coworking_space_S2M_Utrecht%2C_the_Netherlands.jpg/960px-Coworking_space_S2M_Utrecht%2C_the_Netherlands.jpg",
    1156: "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/West_side_of_Manhattan_from_Hudson_Commons_%2895103p%29.jpg/960px-West_side_of_Manhattan_from_Hudson_Commons_%2895103p%29.jpg",
    1181: "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e2/Sparschwein_Haspa02.jpg/960px-Sparschwein_Haspa02.jpg",
    1190: "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f7/30_year_mortgage_calculator.webp/960px-30_year_mortgage_calculator.webp",
    1195: "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/European_Court_of_Human_Rights%2C_courtroom%2C_2014_%28cropped%29.JPG/960px-European_Court_of_Human_Rights%2C_courtroom%2C_2014_%28cropped%29.JPG",
    1207: "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Counterfeit_100_dollar_bill%2C_dated_1974_but_probably_made_later%2C_over-stamped_with_%22Contrefa%C3%A7on%22_on_both_sides._On_display_at_the_British_Museum%2C_London.jpg/960px-Counterfeit_100_dollar_bill%2C_dated_1974_but_probably_made_later%2C_over-stamped_with_%22Contrefa%C3%A7on%22_on_both_sides._On_display_at_the_British_Museum%2C_London.jpg",
    1215: "https://upload.wikimedia.org/wikipedia/commons/2/21/A_detonation_erupts_as_U.S._Marines_with_the_1st_Explosive_Ordnance_Disposal_Company%2C_Combat_Logistics_Regiment_2_conduct_a_demolition_operation_in_Helmand_province%2C_Afghanistan%2C_March_17%2C_2013_130317-M-KS710-206.jpg",
    1218: "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Burglar.jpg/960px-Burglar.jpg",
    1232: "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/White_House_north_and_south_sides.jpg/960px-White_House_north_and_south_sides.jpg",
    1237: "https://upload.wikimedia.org/wikipedia/commons/a/a6/Papeletareferendum2006.jpg",
    1245: "https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/La_Libert%C3%A9_guidant_le_peuple_-_Eug%C3%A8ne_Delacroix_-_Mus%C3%A9e_du_Louvre_Peintures_RF_129_-_apr%C3%A8s_restauration_2024.jpg/960px-La_Libert%C3%A9_guidant_le_peuple_-_Eug%C3%A8ne_Delacroix_-_Mus%C3%A9e_du_Louvre_Peintures_RF_129_-_apr%C3%A8s_restauration_2024.jpg",
    1261: "https://upload.wikimedia.org/wikipedia/en/thumb/4/42/Illustrated_London_News_-_Christmas_Truce_1914.jpg/960px-Illustrated_London_News_-_Christmas_Truce_1914.jpg",
}

TAMIL_UPDATES = {
    825: "1. விண்மீன் / நட்சத்திரம் (Celestial body) / 2. பிரபலம் (Celebrity)",
    827: "1. மழை (Noun) / 2. மழை பெய்தல் (Verb)",
    828: "1. பனி / வெண்பனி (Noun) / 2. பனி பொழிதல் (Verb)",
    830: "1. காற்று / தென்றல் (Breeze/Wind) / 2. புயல் / சூறாவளி (Storm/Tempest)",
    832: "1. இடி (Sound rumble) / 2. மின்னல் (Light flash)",
    835: "1. நிழல் (Silhouette of object) / 2. குளுமை நிழல் (Cool shade)",
    837: "1. விண்வெளி (Outer cosmos) / 2. இடம் / இடைவெளி (Empty room/gap)",
    839: "1. பூமி / புவி (Planet ground) / 2. உலகம் (Global sphere)",
    846: "1. மலை (High peak) / 2. குன்று (Lower elevation)",
    849: "1. வயல் / மைதானம் (Farmland/Meadow) / 2. துறை / களம் (Domain/Profession)",
    850: "1. பாலைவனம் (Arid wasteland) / 2. கைவிட்டுச் செல் (Abandon)",
    852: "1. ஆறு / நதி (Large river) / 2. நீரோடை / சிற்றாறு (Small brook)",
    853: "1. ஏரி (Large lake) / 2. குளம் / குட்டை (Small pool)",
    855: "1. கடற்கரை (Sandy shore) / 2. கரையோரம் (Coastline)",
    860: "1. நாய் (Adult dog) / 2. நாய்க்குட்டி (Young pup)",
    861: "1. பூனை (Adult cat) / 2. பூனைக்குட்டி (Young kitten)",
    862: "1. பசு (Female cow) / 2. காளை / எருது (Male bull)",
    863: "1. செம்மறி ஆடு (Wool sheep) / 2. வெள்ளாடு (Horned goat)",
    864: "1. குதிரை (Horse) / 2. கழுதை (Donkey)",
    868: "1. சிங்கம் (Lion) / 2. புலி (Striped tiger)",
    869: "1. கரடி (Animal) / 2. தாங்கு / சகித்துக்கொள் (Endure)",
    870: "1. ஓநாய் (Wolf) / 2. நரி (Fox)",
    880: "1. புறா (Dove/Pigeon) / 2. காகம் (Black crow)",
    901: "1. திருமண வாழ்க்கை (Marital state) / 2. திருமண விழா (Ceremony event)",
    902: "1. மணமகள் (Bride) / 2. மணமகன் (Groom)",
    903: "1. தம்பதி / ஜோடி (Romantic pair) / 2. இரண்டு மூன்று / சில (A few items)",
    905: "1. அலாரம் / எச்சரிக்கை மணி (Clock buzzer) / 2. நினைவூட்டல் (Prompt note)",
    910: "1. சொரசொரப்பான (Coarse surface) / 2. கடுமையான / தோராயமான (Harsh/Approximate)",
    911: "1. கூர்மையான (Edged blade) / 2. புத்திசாலியான (Intellectually keen)",
    913: "1. தட்டையான / சமதளமான (Level surface) / 2. அடுக்குமாடி வீடு (Apartment)",
    914: "1. நேரான (Direct unbent line) / 2. வெளிப்படையான (Frank/Candid)",
    916: "1. திடமான / உறுதியான (Dense/Firm) / 2. உள்ளீடற்ற / பொந்தான (Empty cavity)",
    918: "1. தளர்வான (Not tight) / 2. கட்டவிழ்த்த / சுதந்திரமான (Unfastened/Free)",
    920: "1. சிறு தலையணை / குஷன் (Sofa pad) / 2. தலையணை உறை (Slipcover)",
    923: "1. சீப்பு (Hair groomer) / 2. தலை வாரு / சீவு (Verb)",
    925: "1. பச்சையான / சமைக்காத (Uncooked food) / 2. கச்சாப் பொருள் (Unprocessed material)",
    934: "1. மிருதுவான / மென்மையான (Soft to chew) / 2. கடினமான / சவடலான (Hard/Rubbery)",
    942: "1. பாதுகாப்பான (Secure) / 2. பாதுகாப்புப் பெட்டகம் (Lockbox)",
    946: "1. பணக்கார / செல்வந்தர் (Wealthy) / 2. சுவையான / செழுமையான (Rich flavor)",
    947: "1. ஏழை (Impoverished) / 2. பாவம் / பரிதாபமான (Pitiable)",
    952: "சரியான",
    957: "1. விசித்திரமான (Odd/Bizarre) / 2. அரிதான (Scarce occurrence)",
    966: "1. வெட்கப்படுகிற (Feeling shame) / 2. குற்றவாளியான / குற்ற உணர்வுள்ள (Culpable)",
    976: "1. உணர்ச்சி (Deep feeling) / 2. மனநிலை (Temporary mood)",
    982: "1. பெருமை / தன்மானம் (Self-respect) / 2. ஆணவம் / கர்வம் (Arrogance)",
    983: "1. பாசம் / அன்பு (Warm fondness) / 2. தீவிர ஆர்வம் / வெறி (Intense fervor)",
    989: "1. மன அதிர்ச்சி (Emotional jolt) / 2. மின்சார அதிர்ச்சி (Electrical shock)",
    998: "1. பேராசை கொண்ட (Avaricious) / 2. சுயநலமான (Self-centered)",
    1003: "1. பக்குவமான (Grown-up mindset) / 2. பக்குவமற்ற (Childish)",
    1007: "1. காட்டுத்தனமான / வன (Undomesticated) / 2. கட்டுப்பாடற்ற (Uncontrolled)",
    1018: "1. நிரபராதியான (Free from guilt) / 2. அப்பாவியான (Naive/Pure)",
    1025: "1. கையசை (Hand gesture) / 2. அலை (Water swell)",
    1028: "1. கண் சிமிட்டு (Involuntary blink) / 2. கண்ணடி (One-eye wink)",
    1037: "தலைவணங்கு / குனிந்து வணங்கு",
    1038: "1. சாய்ந்து கொள் (Rest against) / 2. சரிவாக வளை (Slant/Incline)",
    1040: "1. குத்து (Fist strike) / 2. துளையிடு (Hole maker)",
    1051: "1. இணை (Join/Append) / 2. பிரித்தெடு (Separate/Unfasten)",
    1056: "1. ஆறுதல் கூறு (Console person) / 2. வசதி / சௌகரியம் (Physical ease)",
    1069: "1. கவனி / உணர் (Perceive) / 2. அறிவிப்புப் பலகை (Written warning)",
    1073: "1. மதிப்பீடு செய் / ஆராய் (Evaluate merits) / 2. நீதிபதி (Court magistrate)",
    1074: "1. வழிநடத்து / வழிகாட்டு (Guide path) / 2. நேரடியான (Straightforward)",
    1077: "1. தவிர் / ஒதுங்கு (Steer clear) / 2. தடு (Stop from happening)",
    1078: "1. அனுமதி அளி (Allow) / 2. தடை செய் (Prohibit)",
    1082: "1. ஊறுகாய் (Preserved pickle) / 2. சட்னி / தொடுகறி (Piquant dip)",
    1083: "1. குழம்பு / கறி (Gravy stew) / 2. பருப்பு (Pulse grain)",
    1096: "1. ஒப்புக்கொள் (Acknowledge truth) / 2. மறுத்துவிடு (Refuse truth)",
    1101: "1. தகவல் தெரிவி (Notify facts) / 2. குறிப்பிடு (Briefly refer to)",
    1104: "1. மேற்கோள் காட்டு (Repeat exact words) / 2. விலை மதிப்பீடு (Estimated price)",
    1105: "1. முரண்படு / எதிர்த்துப் பேசு (Oppose words) / 2. சவால் விடு (Dare/Confront)",
    1110: "1. எழுத்தர் / கிளார்க் (General clerk) / 2. கணக்காளர் / ஆடிட்டர் (Financial books)",
    1112: "1. படை/காவல் அதிகாரி (Military/Police) / 2. அரசு/நிறுவன அதிகாரி (Corporate/State)",
    1114: "1. கட்டிடக் கலைஞர் (Building designer) / 2. ஒப்பந்ததாரர் (Contractor)",
    1119: "1. விமானி / பைலட் (Flight aviator) / 2. கேப்டன் / தலைவர் (Ship/Team leader)",
    1129: "1. நூலாசிரியர் / எழுத்தாளர் (Book writer) / 2. கவிஞர் (Verse maker)",
    1140: "1. வேலை நேர்காணல் (Job evaluation) / 2. ஊடகப் பேட்டி (Media Q&A)",
    1144: "1. பதவி உயர்வு (Rank elevation) / 2. பதவி இறக்கம் (Rank degradation)",
    1145: "1. ராஜினாமா (Voluntary quit) / 2. பணி நீக்கம் (Fired from work)",
    1146: "1. ஓய்வு / ரிட்டயர்மென்ட் (Work exit age) / 2. ஓய்வூதியம் / பென்ஷன் (Allowance)",
    1149: "1. திட்டப்பணி / புராஜெக்ட் (Endeavor) / 2. திரையில் காட்டு / கணி (Cast/Predict)",
    1151: "1. கால அட்டவணை (Timetable) / 2. முன்பதிவு நேரம் (Appointment)",
    1152: "1. பணி நேரம் / ஷிப்ட் (Work shift) / 2. கூடுதல் நேரம் / ஓவர்டைம் (Extra hours)",
    1154: "1. வேலைப்பளு (Workload) / 2. பணியாளர்கள் / ஸ்டாஃப் (Staff)",
    1156: "வியாபாரம் / நிறுவனம் / கம்பெனி",
    1157: "1. தொழிற்துறை (Economic sector) / 2. தொழிற்சாலை (Physical mill)",
    1161: "1. தயாரிப்புப் பொருள் (Manufactured good) / 2. சேவை / சர்வீஸ் (Work supplied)",
    1164: "கட்டணம் (ஃபீஸ்)",
    1165: "கட்டணப் பட்டியல் / விலைப்பட்டியல் (இன்வாய்ஸ்)",
    1167: "1. தள்ளுபடி (Discount) / 2. பணம் திரும்பப் பெறுதல் (Refund)",
    1168: "1. தள்ளுபடி விற்பனை (Sale window) / 2. லாபகரமான ஒப்பந்தம் / பேரம் (Deal/Bargain)",
    1170: "1. நாணயம் (Metal coin) / 2. ரூபாய் நோட்டு (Banknote)",
    1172: "1. செல்வம் (Wealth) / 2. வறுமை (Poverty)",
    1176: "1. வைப்புத்தொகை / பணம் செலுத்துதல் (Deposit) / 2. பணம் எடுத்தல் (Withdrawal)",
    1178: "1. வங்கிக் கணக்கு (Account) / 2. இருப்புத் தொகை (Balance)",
    1179: "1. கடன் பாக்கி (Debt) / 2. வங்கிக் கடன் / லோன் (Loan)",
    1180: "1. லாபம் (Profit) / 2. நஷ்டம் / இழப்பு (Loss)",
    1183: "1. தணிக்கை / ஆடிட் (Audit) / 2. பணப் பரிவர்த்தனை (Transaction)",
    1185: "அபராதம் / அபராதத் தொகை",
    1186: "1. பொருளாதாரம் (Economy) / 2. நிதி சார்ந்த (Financial)",
    1187: "வட்டி / வட்டி விகிதம்",
    1188: "1. முதலீடு (Investment) / 2. ஆபத்து / ரிஸ்க் (Risk)",
    1191: "1. பணவீக்கம் / விலைவாசி உயர்வு (Inflation) / 2. பொருளாதார மந்தநிலை (Recession)",
    1194: "1. நீதி (Justice) / 2. அநீதி (Injustice)",
    1195: "நீதிமன்றம் / நீதிமன்ற அறை",
    1197: "1. தீர்ப்பு (Verdict) / 2. தண்டனைத் தீர்ப்பு (Sentence)",
    1199: "1. சாட்சி (Witness) / 2. சாட்சியம் / வாக்குமூலம் (Testimony)",
    1201: "1. ஒப்புதல் வாக்குமூலம் (Confession) / 2. உறுதிமொழி / சத்தியம் (Oath)",
    1202: "1. ஜாமீன் (Bail) / 2. காவல் (Custody)",
    1205: "1. குற்றம் (Crime) / 2. குற்றவாளி (Criminal)",
    1210: "1. கடத்தல் (Kidnapping) / 2. பிணைக் கைதி (Hostage)",
    1213: "1. ஆயுதம் (Weapon) / 2. துப்பாக்கி (Gun)",
    1215: "1. வெடிகுண்டு (Bomb) / 2. வெடிப்பு (Explosion)",
    1217: "1. சைரன் ஒலி (Siren) / 2. ரோந்துப் பணி (Patrol)",
    1219: "1. துப்பு / தடயம் (Clue) / 2. கைரேகை (Fingerprint)",
    1220: "1. கண்காணிப்பு (Surveillance) / 2. விசாரணை (Interrogation)",
    1222: "1. சிறைச்சாலை / ஜெயில் (Prison/Jail) / 2. சிறை அறை / தனிச் சிறை (Lockup cell)",
    1227: "1. நாடு / தேசம் (Nation) / 2. குடியரசு (Republic)",
    1228: "1. ஜனநாயகம் / மக்களாட்சி (Democracy) / 2. அரசியலமைப்புச் சட்டம் (Constitution)",
    1230: "1. கொள்கை / பாலிசி (Policy) / 2. சட்டம் / சட்டமியற்றல் (Legislation)",
    1232: "1. குடியரசுத் தலைவர் (President) / 2. பிரதமர் (Prime minister)",
    1233: "1. அமைச்சர் / மந்திரி (Minister) / 2. அமைச்சகம் (Ministry)",
    1234: "1. மேயர் / நகரத் தலைவர் (Mayor) / 2. ஆளுநர் / கவர்னர் (Governor)",
    1235: "1. குடிமகன் (Citizen) / 2. குடியுரிமை / தேசிய இனம் (Nationality)",
    1236: "1. எதிர்க்கட்சி (Opposition) / 2. கூட்டணி (Coalition)",
    1237: "1. பெரும்பான்மை (Majority) / 2. சிறுபான்மை (Minority)",
    1238: "1. அதிகாரம் (Authority) / 2. ஆட்சி / வலிமை (Power/Rule)",
    1239: "1. தேர்தல் (Election) / 2. வாக்கு / வாக்களி (Vote)",
    1240: "1. பிரச்சாரம் (Campaign) / 2. வேட்பாளர் (Candidate)",
    1242: "1. உரிமை (Legal right) / 2. சுதந்திரம் / விடுதலை (Freedom/Liberty)",
    1244: "1. வேலை நிறுத்தம் (Strike) / 2. புறக்கணிப்பு (Boycott)",
    1245: "1. புரட்சி (Revolution) / 2. இயக்கம் (Movement)",
    1246: "1. சமூக ஆர்வலர் (Activist) / 2. தன்னார்வலர் (Volunteer)",
    1249: "1. சமூகம் (Society) / 2. சமுதாயம் / உள்ளூர் குழு (Community)",
    1251: "1. அகதி (Refugee) / 2. குடியேறியவர் (Immigrant)",
    1252: "1. சர்வதேச (International) / 2. வெளிநாட்டு (Foreign)",
    1253: "1. ராஜதந்திரம் / தூதரக உறவு (Diplomacy) / 2. தூதரகம் (Embassy)",
    1255: "1. தகராறு / சர்ச்சை (Dispute) / 2. மோதல் (Conflict) / 3. நெருக்கடி (Crisis)",
    1257: "1. ராணுவம் / தரைப்படை (Military/Army) / 2. கடற்படை (Navy)",
    1258: "படைத்தளபதி / ராணுவத் தளபதி",
    1260: "1. வெற்றி (Victory) / 2. தோல்வி (Defeat)",
    1261: "1. சரணடைதல் (Surrender) / 2. போர் நிறுத்தம் (Ceasefire)",
}

# Tuple format: (new_es_or_None, new_hi_or_None)
SHORTCUT_UPDATES = {
    825: (
        None,
        '1. Celestial body: <strong>Taara</strong> ≈ <strong>Tamil தாரகை (Thaaragai)</strong> / <strong>Sitaara</strong> (Shining cinema or sky star!) = <em>Star</em>!<br>2. Celebrity: <strong>Sitaara</strong> (Movie legend) / <strong>Star</strong> (Superstar celebrity!) = <em>Celebrity</em>!'
    ),
    830: (
        '1. Breeze: <strong>Viento</strong> (Air rushing out of a <strong>"Vent"</strong>) | <strong>Aire</strong> (Crisp flowing <strong>"Air"</strong>) = <em>Wind</em>!<br>2. Storm: <strong>Tormenta</strong> (<strong>"Tormenting"</strong> gale) | <strong>Temporal</strong> (Raging <strong>"Tempest"</strong>) = <em>Storm</em>!',
        None
    ),
    832: (
        '1. Sound: <strong>Trueno</strong> ≈ Booming <strong>"True-Noise"</strong> clapping across clouds = <em>Thunder</em>!<br>2. Flash: <strong>Relámpago</strong> (Sudden sky <strong>"Lamp"</strong> flash!) | <strong>Rayo</strong> (Sky <strong>"Ray"</strong> bolt) = <em>Lightning</em>!',
        '1. Sound: <strong>Garjan / Baadal ki garaj</strong> ≈ <strong>Tamil கர்ஜனை (Garjanai = Thunderous roar!)</strong> = <em>Thunder</em>!<br>2. Flash: <strong>Bijli (chamakne wali)</strong> ≈ Sparkling <strong>"Chamak"</strong> electric flash (<strong>Bijli</strong>) zigzagging across clouds = <em>Lightning</em>!'
    ),
    833: (
        '<strong>Tiempo</strong> (Same root as <strong>"Tempo"</strong> — daily sky tempo) | <strong>Clima</strong> (Origin of <strong>"Climate"</strong>!) = <em>Weather / Climate</em>!',
        None
    ),
    834: (
        '<strong>Temperatura</strong> ≈ Latin thermometer degree scale ("Temper" of hot &amp; cold!) = <em>Temperature</em>!',
        None
    ),
    836: (
        '<strong>Aire</strong> ≈ Invisible oxygen breath we inhale (<em>Aire</em> fresh as mountain breeze!) = <em>Air</em>!',
        None
    ),
    837: (
        '1. Cosmos: <strong>Espacio (exterior)</strong> ≈ Vast outer expanse beyond Earth (root of <em>Spatial</em>!) = <em>Outer Space</em>!<br>2. Gap: <strong>Espacio</strong> (Open room) | <strong>Lugar</strong> (Spot/Place) = <em>Room / Gap</em>!',
        '1. Cosmos: <strong>Space</strong> (Orbiting rockets beyond Earth) / <strong>Aasmaan ke baahar</strong> (Outside the sky!) = <em>Outer Space</em>!<br>2. Gap: <strong>Jagah</strong> (Open spot) / <strong>Faasla</strong> (Measured gap between objects) = <em>Space / Gap</em>!'
    ),
    838: (
        '<strong>Naturaleza</strong> ≈ Living forest, rivers, and earth created naturally (origin of <em>Natural</em>!) = <em>Nature</em>!',
        '<strong>Qudrat</strong> (Divine creation of trees, sky &amp; rivers!) / <strong>Nature</strong> (Green outdoors!) = <em>Nature</em>!'
    ),
    840: (
        '<strong>Tierra</strong> (<strong>"Terrain"</strong> planet surface) | <strong>Suelo</strong> (<strong>"Soil"</strong> under shoe sole) | <strong>Terreno</strong> (Plot of terrain) = <em>Land / Ground</em>!',
        None
    ),
    841: (
        '<strong>Tierra</strong> (Earthy garden dirt) | <strong>Suelo</strong> (<strong>"Soil"</strong>) | <strong>Polvo</strong> (Dry fine earth powder) = <em>Dirt / Soil</em>!',
        None
    ),
    845: (
        '<strong>Piedra</strong> (Stone — root of <strong>"Petrified / Peter"</strong>) | <strong>Roca</strong> (Massive quarry boulder!) = <em>Rock / Stone</em>!',
        None
    ),
    846: (
        '1. Peak: <strong>Montaña</strong> ≈ Towering snowy ridge (origin of <strong>"Montane / Montana"</strong>!) = <em>Mountain</em>!<br>2. Lower: <strong>Colina</strong> (Rolling green curve) | <strong>Cerro</strong> (Steep ridge) = <em>Hill</em>!',
        None
    ),
    847: (
        '<strong>Valle</strong> ≈ Deep green basin carved between mountains (think Napa <em>Valle</em>!) = <em>Valley</em>!',
        '<strong>Ghaati</strong> ≈ Winding pass sunken between ridges (think Western <strong>Ghats</strong> mountain gorges!) = <em>Valley</em>!'
    ),
    848: (
        '<strong>Cueva</strong> (Hollow hillside grotto) | <strong>Caverna</strong> (Deep rocky <strong>"Cavern"</strong>) = <em>Cave</em>!',
        None
    ),
    849: (
        '1. Farmland: <strong>Campo</strong> (Open pasture — root of <strong>"Camp"</strong>) | <strong>Prado</strong> (Lush green meadow!) = <em>Field</em>!<br>2. Domain: <strong>Área</strong> (Zone/Scope) | <strong>Campo</strong> (Line of expertise) = <em>Career Field</em>!',
        '1. Farmland: <strong>Khet</strong> (Crop farmland) / <strong>Maidaan</strong> (<strong>Tamil மைதானம் = Open ground!</strong>) = <em>Field</em>!<br>2. Domain: <strong>Ilaqa</strong> (Zone/Region) / <strong>Field</strong> (Career specialty!) = <em>Domain / Field</em>!'
    ),
    850: (
        '1. Wasteland: <strong>Desierto</strong> ≈ Sun-baked arid Sahara wasteland! = <em>Desert</em>!<br>2. Abandon: <strong>Abandonar</strong> (Leave behind) | <strong>Dejar tirado</strong> (Leave stranded!) = <em>To Desert</em>!',
        None
    ),
    853: (
        '1. Large: <strong>Lago</strong> ≈ Glacial lake (think Italian <em>Lago</em> di Como!) = <em>Lake</em>!<br>2. Small: <strong>Estanque</strong> (Stagnant backyard pool!) | <strong>Charca</strong> (Rainwater puddle pond) = <em>Pond</em>!',
        None
    ),
    854: (
        '<strong>Mar</strong> (Root of <strong>"Marine / Maritime"</strong>) | <strong>Océano</strong> (Deep vast <strong>Atlantic Ocean</strong>!) = <em>Sea / Ocean</em>!',
        None
    ),
    855: (
        '1. Sandy shore: <strong>Playa</strong> ≈ Golden sand where kids <strong>"Play-Yah!"</strong> by the surf = <em>Beach</em>!<br>2. Coastline: <strong>Costa</strong> (Sea <strong>Coastline</strong>) | <strong>Orilla</strong> (River/sea rim edge!) = <em>Shore / Coast</em>!',
        '1. Sandy shore: <strong>Samandar ka kinaara</strong> (Edge of the sea!) / <strong>Beach</strong> (Golden seaside surf!) = <em>Beach</em>!<br>2. Coastline: <strong>Kinaara</strong> ≈ <strong>Tamil கரை (Karai = Shore/Edge!)</strong> = <em>Shore / Coast</em>!'
    ),
    856: (
        '<strong>Isla</strong> ≈ Lone sandy dot encircled by blue ocean (think tropical <strong>"Isle"</strong>!) = <em>Island</em>!',
        None
    ),
    858: (
        '<strong>Animal</strong> (Breathing creature with soul — Latin <em>Anima</em>!) | <strong>Bicho</strong> (Tiny backyard <strong>"Bug/Critter"</strong>) = <em>Animal</em>!',
        None
    ),
    862: (
        '1. Cow: <strong>Vaca</strong> ≈ Dairy pasture cow (origin of Jenner\'s <strong>"Vaccine"</strong>!) = <em>Cow</em>!<br>2. Bull: <strong>Toro</strong> ≈ Charging horned bull (zodiac <strong>"Taurus"</strong>!) = <em>Bull</em>!',
        None
    ),
    866: (
        '<strong>Camello</strong> ≈ Hump-backed desert caravan traveler (think trekking in Morocco!) = <em>Camel</em>!',
        None
    ),
    867: (
        '<strong>Elefante</strong> ≈ Long-trunked savanna giant with ivory tusks! = <em>Elephant</em>!',
        None
    ),
    868: (
        '1. Lion: <strong>León</strong> ≈ Golden-maned king of the pride (think constellation <strong>Leo</strong>!) = <em>Lion</em>!<br>2. Tiger: <strong>Tigre</strong> ≈ Black-striped orange Bengal hunter (think river <strong>Tigris</strong>!) = <em>Tiger</em>!',
        None
    ),
    869: (
        '1. Animal: <strong>Oso</strong> ≈ Shaggy grizzly (Latin <em>Ursa</em> — think <strong>"Oh-So-Big!"</strong>) = <em>Bear</em>!<br>2. Endure: <strong>Aguantar</strong> (Hold strong under heavy load) | <strong>Soportar</strong> (<strong>"Support"</strong> the weight!) = <em>To Bear</em>!',
        None
    ),
    875: (
        '<strong>Serpiente</strong> (Coiled serpent) | <strong>Víbora</strong> (Venomous <strong>"Viper"</strong>) | <strong>Culebra</strong> (Slithering garden snake) = <em>Snake</em>!',
        None
    ),
    877: (
        '<strong>Tortuga</strong> ≈ Slow domed reptile with protective shell (remember pirate island <em>Tortuga</em> — shaped like a turtle shell!) = <em>Turtle</em>!',
        None
    ),
    878: (
        '<strong>Cocodrilo</strong> (Nile reptile!) | <strong>Caimán</strong> (Swamp alligator <strong>"Caiman"</strong>!) = <em>Crocodile</em>!',
        None
    ),
    881: (
        '1. Animal: <strong>Murciélago</strong> ≈ Blind-mouse night flyer (<em>Mur = Mouse, Ciego = Blind!</em>) = <em>Bat</em>!<br>2. Sports stick: <strong>Bate</strong> ≈ Wooden baseball slugger club (swinging <em>Bat!</em>) = <em>Sports Bat</em>!',
        None
    ),
    882: (
        None,
        '<strong>Shark</strong> ≈ Sharp-finned ocean predator cruising reefs (<strong>"Shark"</strong> with razor dorsal fin!) = <em>Shark</em>!'
    ),
    883: (
        '<strong>Insecto</strong> (Six-legged bug — <em>Segmented</em> body!) | <strong>Bicho</strong> (Tiny crawling garden critter!) = <em>Insect / Bug</em>!',
        None
    ),
    884: (
        '<strong>Mosquito</strong> (Literally <em>"Little fly"</em> — Mosca + -ito!) | <strong>Zancudo</strong> (Long-legged biting flyer!) = <em>Mosquito</em>!',
        None
    ),
    889: (
        '<strong>Humano</strong> (Born of the earth — Latin <em>Humus</em>!) | <strong>Ser humano</strong> (<em>Ser</em> Being + <em>Humano</em> = Human being) = <em>Human</em>!',
        None
    ),
    890: (
        '<strong>Adolescente</strong> (Growing teen) | <strong>Joven</strong> (Full of youth — root of <strong>"Juvenile"</strong>!) = <em>Teenager / Youth</em>!',
        None
    ),
    891: (
        '<strong>Anciano</strong> (Wise ancient!) | <strong>Mayor</strong> (Senior elder — like <strong>"Major"</strong> age) | <strong>Persona de edad</strong> (Person of years) = <em>Elder / Senior</em>!',
        None
    ),
    894: (
        '<strong>Pareja</strong> (Matched life pair!) | <strong>Cónyuge</strong> (Joined in <strong>"Conjugal"</strong> wedlock) | <strong>Esposo(a)</strong> (Husband/Wife — <em>Spouse!</em>) = <em>Spouse / Partner</em>!',
        '<strong>Pati-patni</strong> (<strong>Tamil பதி-பத்தினி = Husband &amp; Wife!</strong>) / <strong>Partner</strong> (Teammate standing beside you through life!) = <em>Spouse / Partner</em>!'
    ),
    895: (
        '<strong>Miembro</strong> (Club roster limb/member!) | <strong>Socio</strong> (Business/social ally — think <strong>"Associate"</strong>!) = <em>Member</em>!',
        '<strong>Hissa</strong> (<strong>Spoken Tamil ஹிஸ்ஸா = Share/Part!</strong>) / <strong>Member</strong> (Signed-up club roster holder!) = <em>Member</em>!'
    ),
    896: (
        '<strong>Multitud</strong> (<strong>"Multitude"</strong> throng!) | <strong>Muchedumbre</strong> (Dense packed mob!) | <strong>Gente</strong> (Folk/People — think <strong>"Gentry"</strong>) = <em>Crowd</em>!',
        None
    ),
    898: (
        '<strong>Enemigo</strong> (<em>In-</em> Not + <em>Amigo</em> Friend = Enemy!) | <strong>Rival</strong> (Competitor across the river!) | <strong>Adversario</strong> (Opposing <strong>"Adversary"</strong>!) = <em>Enemy / Rival</em>!',
        None
    ),
    899: (
        '<strong>Relación</strong> (Two lives linked together!) | <strong>Vínculo</strong> (Invisible tie/bond linking family!) = <em>Relationship</em>!',
        None
    ),
    901: (
        '1. State: <strong>Matrimonio</strong> (Lifelong <strong>"Matrimony"</strong>) / <strong>Casamiento</strong> (Joining one <em>Casa</em>/home!) = <em>Marriage</em>!<br>2. Ceremony: <strong>Boda</strong> (<strong>"Both-Day"</strong> vow celebration!) / <strong>Casamiento</strong> (Wedding ceremony!) = <em>Wedding</em>!',
        None
    ),
    903: (
        '1. Romantic pair: <strong>Pareja</strong> (Matched life <strong>"Pair"</strong> holding hands!) = <em>Couple</em>!<br>2. A few: <strong>Un par</strong> (Just one pair) / <strong>Unos pocos</strong> (Two or three!) = <em>A Few</em>!',
        None
    ),
    904: (
        '<strong>Barrio</strong> (Local block — famous Spanish ward!) | <strong>Vecindario</strong> (Home <strong>"Vicinity"</strong>) | <strong>Colonia</strong> (Residential <strong>"Colony"</strong>!) = <em>Neighborhood</em>!',
        None
    ),
    905: (
        '1. Buzzer: <strong>Alarma</strong> ≈ Loud bedside ringing warning (Origin: <em>All\'arme</em> — "To arms!" wake-up!) = <em>Alarm</em>!<br>2. Note: <strong>Recordatorio</strong> ≈ Sticky note to <strong>"Record"</strong> in memory = <em>Reminder</em>!',
        '1. Buzzer: <strong>Alarm</strong> (Morning clock siren!) / <strong>Ghanti</strong> (<strong>Tamil கண்டை = Bell!</strong>) = <em>Alarm</em>!<br>2. Note: <strong>Yaad dilaane wala</strong> (That which brings back memory!) / <strong>Reminder</strong> (Phone pop-up ping!) = <em>Reminder</em>!'
    ),
    906: (
        '<strong>Linterna</strong> ≈ Hand-held glowing beam lantern (think <strong>"Lantern"</strong> in the dark!) = <em>Flashlight / Torch</em>!',
        '<strong>Torch</strong> ≈ Hand-held electric beam tube lighting dark paths (think bright camp beam!) = <em>Flashlight / Torch</em>!'
    ),
    907: (
        None,
        '<strong>Earphones</strong> (Tiny buds tucked inside ears!) / <strong>Headphones</strong> (Cushioned band over your head for music!) = <em>Earphones / Headphones</em>!'
    ),
    908: (
        '<strong>Cargador</strong> (Refills battery <strong>"Cargo"</strong>!) | <strong>Adaptador</strong> (Wall plug power <strong>"Adapter"</strong>!) = <em>Charger / Adapter</em>!',
        '<strong>Charger</strong> (Cable pumping juice into a phone battery!) / <strong>Adapter</strong> (Square wall socket block!) = <em>Charger / Adapter</em>!'
    ),
    913: (
        '1. Level: <strong>Plano</strong> (Flat <strong>"Plane"</strong>) | <strong>Llano</strong> (Wide prairie) | <strong>Chato</strong> (Squashed snub/flat!) = <em>Flat</em>!<br>2. Home: <strong>Piso</strong> (Walked floor) | <strong>Departamento</strong> (Building <strong>"Apartment"</strong> unit!) = <em>Apartment</em>!',
        '1. Level: <strong>Seedha</strong> (Smooth level plane) / <strong>Chipta</strong> (Pressed flat like a coin!) = <em>Flat Surface</em>!<br>2. Home: <strong>Flat</strong> (Single-floor apartment living room on one level!) = <em>Apartment</em>!'
    ),
    914: (
        '1. Line: <strong>Recto</strong> (<strong>"Rectangle"</strong> straight line) | <strong>Derecho</strong> (Unbending right way!) = <em>Straight</em>!<br>2. Candid: <strong>Directo</strong> (Right to the point!) | <strong>Sincero</strong> (Honest &amp; <strong>"Sincere"</strong>!) = <em>Frank</em>!',
        None
    ),
    915: (
        '<strong>Curvo / curvado</strong> ≈ Bending smoothly like a crescent road arc (from <em>Curva</em> = Arc bend!) = <em>Curved</em>!',
        None
    ),
    916: (
        '1. Dense: <strong>Sólido</strong> (Rock-hard core) | <strong>Firme</strong> (Unshakeably <strong>"Firm"</strong>!) = <em>Solid</em>!<br>2. Cavity: <strong>Hueco</strong> (Rings with an <strong>"Echo"</strong> inside!) | <strong>Vacío</strong> (Totally <strong>"Vacant"</strong> tube!) = <em>Hollow</em>!',
        None
    ),
    917: (
        '<strong>Apretado</strong> (Squeezed/Pressed tight!) | <strong>Ajustado</strong> (Snugly <strong>"Adjusted"</strong> belt notch!) = <em>Tight</em>!',
        None
    ),
    920: (
        None,
        '1. Pad: <strong>Gaddi</strong> ≈ Soft stuffed couch pad (sink right into cozy <em>Gaddi!</em>) = <em>Cushion</em>!<br>2. Cover: <strong>Takiye ka cover</strong> (Zip-up sleeve for <em>Takiya</em> pillow) / <strong>Khol</strong> (Outer shell!) = <em>Pillowcase</em>!'
    ),
    921: (
        None,
        '<strong>Hanger</strong> (Triangle hook hanging shirts neatly in a closet!) / <strong>Khunti</strong> (Wall peg sticking out to hang coats!) = <em>Hanger</em>!'
    ),
    924: (
        None,
        '<strong>Tissue paper</strong> ≈ Ultra-thin disposable wipe sheet pulled from a pocket pack! = <em>Tissue</em>!'
    ),
    925: (
        '1. Food: <strong>Crudo / cruda</strong> (Uncooked sushi/steak — root of <strong>"Crude"</strong>!) = <em>Raw Food</em>!<br>2. Material: <strong>En bruto</strong> (Rough ore!) | <strong>Virgen</strong> (Untouched pure wood/oil!) = <em>Raw Material</em>!',
        None
    ),
    926: (
        '<strong>Maduro / madura</strong> ≈ Fruit sweetened to full maturity (think <strong>"Mature"</strong> golden mango!) = <em>Ripe</em>!',
        None
    ),
    928: (
        '<strong>Rancio / rancia</strong> (Sour butter — root of <strong>"Rancid"</strong>!) | <strong>Duro</strong> (Rock-hard day-old baguette!) = <em>Stale</em>!',
        None
    ),
    930: (
        '<strong>Húmedo</strong> (Misty <strong>"Humid"</strong> morning towel!) | <strong>Mojado</strong> (Soaked wet like spilled <strong>"Mojito"</strong>!) = <em>Damp / Moist</em>!',
        None
    ),
    934: (
        '1. Soft: <strong>Tierno</strong> (Melt-in-mouth <strong>"Tender"</strong>) | <strong>Suave</strong> (Silky <strong>"Suave"</strong>!) = <em>Tender</em>!<br>2. Hard: <strong>Duro</strong> (Tough rock) | <strong>Correoso</strong> (Chewy like leather <em>Correa</em> belt!) = <em>Tough</em>!',
        None
    ),
    936: (
        None,
        '<strong>Cashier</strong> ≈ Store clerk counting bills and handing back change at the checkout till! = <em>Cashier</em>!'
    ),
    937: (
        '<strong>Precio</strong> (Store shelf cost!) | <strong>Etiqueta de precio</strong> (<em>Etiqueta</em> <strong>"Ticket"</strong> tag + <em>de Precio</em> = Price sticker!) = <em>Pricetag / Price</em>!',
        None
    ),
    940: (
        '<strong>Garantía</strong> ≈ Signed paper promising free repair if it breaks! = <em>Warranty / Guarantee</em>!',
        '<strong>Guarantee</strong> (100% promise!) / <strong>Warranty</strong> (Official repair coverage slip inside the box!) = <em>Warranty / Guarantee</em>!'
    ),
    941: (
        None,
        '<strong>Delivery</strong> (Doorstep parcel drop!) / <strong>Courier</strong> (Speedy rider rushing boxes from city to city!) = <em>Delivery / Courier</em>!'
    ),
    942: (
        '1. Secure: <strong>Seguro</strong> (Protected vault — root of <strong>"Secure"</strong>!) | <strong>A salvo</strong> (Out of harm!) = <em>Safe</em>!<br>2. Box: <strong>Caja fuerte</strong> (<em>Caja</em> Box + <em>Fuerte</em> Strong = Steel vault!) = <em>Bank Safe</em>!',
        None
    ),
    946: (
        '1. Wealthy: <strong>Rico</strong> (Loaded with gold!) | <strong>Adinerado</strong> (Full of <em>Dinero</em> cash!) = <em>Rich</em>!<br>2. Flavor: <strong>Rico</strong> (Delicious!) | <strong>Sustancioso</strong> (Hearty <strong>"Substantial"</strong> feast!) = <em>Rich Food</em>!',
        None
    ),
    947: (
        '1. Broke: <strong>Pobre</strong> (Living in <strong>"Poverty"</strong> without coins!) = <em>Poor</em>!<br>2. Pitiable: <strong>Pobre / pobrecito</strong> (Adding <em>-cito</em> makes it "Oh, poor little thing!") = <em>Unfortunate</em>!',
        None
    ),
    948: (
        '<strong>Paquete</strong> (Taped box) | <strong>Bulto</strong> (Bulky bundle!) | <strong>Encomienda</strong> (<strong>"Entrusted"</strong> mailed parcel!) = <em>Parcel / Package</em>!',
        '<strong>Parcel</strong> (Wrapped brown shipping box!) / <strong>Packet</strong> (Neat sealed pouch handed to your door!) = <em>Parcel / Package</em>!'
    ),
    949: (
        '<strong>Puro / pura</strong> (Unmixed spring water!) | <strong>Auténtico</strong> (<strong>"Authentic"</strong> real gold!) = <em>Pure</em>!',
        None
    ),
    950: (
        '<strong>Verdadero</strong> (Truth — root of <strong>"Verdict"</strong>!) | <strong>Real</strong> (Genuine!) | <strong>De verdad</strong> ("For real!") = <em>True / Real</em>!',
        None
    ),
    951: (
        '<strong>Falso / falsa</strong> (Untrue lie!) | <strong>Imitación</strong> (Plastic knockoff <strong>"Imitation"</strong>!) = <em>False / Fake</em>!',
        None
    ),
    952: (
        '<strong>Correcto</strong> (Marked right!) | <strong>Acertado</strong> (<strong>"Asserted"</strong> bullseye hit!) | <strong>Bien</strong> (Well done!) = <em>Correct / Right</em>!',
        None
    ),
    953: (
        '<strong>Incorrecto</strong> (<em>In-</em> Not + <em>Correcto</em>!) | <strong>Equivocado</strong> (Mistaken!) | <strong>Mal</strong> (Bad/Wrong!) = <em>Wrong</em>!',
        None
    ),
    954: (
        '<strong>Exacto / exacta</strong> (Spot-on to the millimeter!) | <strong>Preciso</strong> (<strong>"Precise"</strong> laser accuracy!) = <em>Exact</em>!',
        None
    ),
    955: (
        None,
        '<strong>Tracking</strong> (Live GPS dot moving on your delivery map!) / <strong>Pata lagana</strong> (<strong>Pata</strong> Address/Clue + <strong>Lagana</strong> Find = Trace!) = <em>Tracking</em>!'
    ),
    956: (
        '<strong>Normal</strong> (Everyday standard) | <strong>Común</strong> (Shared by all — <em>"Common"</em>!) | <strong>Corriente</strong> (Ordinary flow — <em>"Current"</em>!) = <em>Normal / Common</em>!',
        '<strong>Aam</strong> ≈ Common everyday person/thing (famous phrase <strong>"Aam Aadmi" = Common Man</strong> — distinct from <em>Aam</em> fruit!) = <em>Normal / Common</em>!'
    ),
    957: (
        '1. Odd: <strong>Raro</strong> (Bizarre) | <strong>Extraño</strong> (Unfamiliar <strong>"Stranger"</strong>!) = <em>Strange</em>!<br>2. Scarce: <strong>Raro</strong> (Hardly seen) | <strong>Poco común</strong> (<em>Poco</em> Little + <em>Común</em> Common!) = <em>Rare</em>!',
        None
    ),
    958: (
        '<strong>Perfecto / perfecta</strong> (Zero errors!) | <strong>Impecable</strong> (<strong>"Impeccable"</strong> — literally spotless!) = <em>Perfect</em>!',
        '<strong>Bilkul sahi</strong> (<strong>Tamil முழுதும்</strong> Totally + <strong>Sahi</strong> True = Spot-on!) / <strong>Perfect</strong> (10/10 flawless score!) = <em>Perfect</em>!'
    ),
    960: (
        '1. Angry: <strong>Enojado</strong> (Fuming!) | <strong>Furioso</strong> (Red-hot <strong>"Furious"</strong>!) = <em>Angry</em>!<br>2. Crazy: <strong>Loco / loca</strong> (Wildly shouting <em>"Loco!"</em>) = <em>Mad / Crazy</em>!',
        None
    ),
    961: (
        '<strong>Nervioso / nerviosa</strong> ≈ Sweaty palms and racing heartbeat before an exam! = <em>Nervous</em>!',
        None
    ),
    962: (
        None,
        '<strong>Bore hona</strong> ≈ Yawning at the clock when nothing exciting happens (<em>Bore</em> + <em>Hona</em> Become!) = <em>Bored</em>!'
    ),
    963: (
        '<strong>Preocupado / preocupada</strong> ≈ Mind <strong>"Preoccupied"</strong> with nonstop anxious thoughts! = <em>Worried</em>!',
        None
    ),
    964: (
        '<strong>Sorprendido / sorprendida</strong> ≈ Wide-eyed jaw drop at an unexpected gift! = <em>Surprised</em>!',
        None
    ),
    967: (
        '<strong>Solitario / sola</strong> ≈ Walking alone down a quiet street (like Latin <em>Solus</em> = alone!) = <em>Lonely</em>!',
        None
    ),
    968: (
        '<strong>Celoso</strong> (Protective <strong>"Zealous"</strong> jealousy!) | <strong>Envidioso</strong> (Green with <strong>"Envy"</strong>!) = <em>Jealous / Envious</em>!',
        None
    ),
    970: (
        '<strong>Esperanzado</strong> (Full of <em>Esperanza</em> — sunny <strong>Hope</strong>!) | <strong>Optimista</strong> (Sees bright silver linings!) = <em>Hopeful / Optimistic</em>!',
        None
    ),
    971: (
        '<strong>Desesperado / desesperada</strong> ≈ <em>Des-</em> (Without) + <em>Esperar</em> (Hope) → Running out of hope = <em>Desperate</em>!',
        None
    ),
    972: (
        '<strong>Confundido / confundida</strong> ≈ Thoughts scrambled together in a fog ("Confused"!) = <em>Confused</em>!',
        None
    ),
    973: (
        '<strong>Frustrado / frustrada</strong> ≈ Screaming into a pillow when plans keep jamming! = <em>Frustrated</em>!',
        None
    ),
    974: (
        '<strong>Decepcionado</strong> (Let down by <em>Deception</em>!) | <strong>Desilusionado</strong> (Shattered <strong>"Illusion"</strong>!) = <em>Disappointed</em>!',
        None
    ),
    975: (
        '<strong>Satisfecho</strong> (Full &amp; happy after a feast!) | <strong>Contenta</strong> (Calmly <strong>"Content"</strong>!) = <em>Satisfied</em>!',
        None
    ),
    976: (
        '1. Feeling: <strong>Emoción</strong> (Heart rush) | <strong>Sentimiento</strong> (Deep <strong>"Sentiment"</strong>!) = <em>Emotion</em>!<br>2. Mood: <strong>Estado de ánimo</strong> (State of spirit) | <strong>Humor</strong> (Current temperament!) = <em>Mood</em>!',
        None
    ),
    979: (
        '<strong>Furia</strong> (Explosive <strong>"Fury"</strong>!) | <strong>Rabia</strong> (Foaming <strong>"Rabies"</strong> anger!) | <strong>Cólera</strong> (Hot temper!) = <em>Rage</em>!',
        None
    ),
    980: (
        '<strong>Pánico</strong> (Sudden wild stampede!) | <strong>Terror</strong> (Heart-stopping icy dread!) = <em>Terror / Panic</em>!',
        None
    ),
    981: (
        '<strong>Ansiedad</strong> (Tight chest worry!) | <strong>Estrés</strong> (Pressure overload snapping nerves!) = <em>Anxiety / Stress</em>!',
        None
    ),
    983: (
        '1. Fondness: <strong>Cariño</strong> (Tender hug!) | <strong>Afecto</strong> (Warm <strong>"Affection"</strong>!) = <em>Affection</em>!<br>2. Fervor: <strong>Pasión</strong> (Blazing fire in the heart!) = <em>Passion</em>!',
        None
    ),
    985: (
        '<strong>Depresión</strong> (Heavy dark cloud sinking the mind!) | <strong>Bajón</strong> (Sudden emotional drop — from <em>Bajar</em> Down!) = <em>Depression</em>!',
        '<strong>Gehri udaasi</strong> (<em>Gehri</em> Deep + <em>Udaasi</em> Sorrow!) / <strong>Depression</strong> (Long heavy gloom pulling energy down!) = <em>Depression</em>!'
    ),
    986: (
        '<strong>Entusiasmo</strong> (Electric stadium cheers!) | <strong>Ganas</strong> (Eager hunger/desire to do something!) = <em>Enthusiasm</em>!',
        None
    ),
    987: (
        '<strong>Paciencia</strong> ≈ Quiet calm breath while waiting in a slow queue! = <em>Patience</em>!',
        None
    ),
    988: (
        '<strong>Coraje</strong> (Lion-hearted bravery!) | <strong>Valentía</strong> (Knightly <strong>"Valor"</strong>!) = <em>Courage</em>!',
        None
    ),
    989: (
        '1. Emotional: <strong>Conmoción</strong> (Mind <strong>"Commotion"</strong>) | <strong>Susto</strong> (Sudden jump fright!) = <em>Shock</em>!<br>2. Electric: <strong>Descarga eléctrica</strong> (Static jolt) | <strong>Choque</strong> (Zap impact!) = <em>Electric Shock</em>!',
        '1. Emotional: <strong>Sadma</strong> (Heavy blow — "SAD-Ma") / <strong>Jhatka</strong> (Sudden jolt!) = <em>Shock</em>!<br>2. Electric: <strong>Current</strong> (Live wire surge!) / <strong>Bijli ka jhatka</strong> (Lightning zap jolt!) = <em>Electric Shock</em>!'
    ),
    990: (
        '<strong>Simpático</strong> (Warm vibe!) | <strong>Amable</strong> (Kind &amp; <strong>"Amiable"</strong>!) | <strong>Agradable</strong> (Pleasant!) = <em>Nice / Friendly</em>!',
        None
    ),
    992: (
        '<strong>Tonto</strong> (Silly goof) | <strong>Estúpido</strong> (Foolish error) | <strong>Bobo</strong> (Simpleton clown — think "Bozo"!) = <em>Stupid / Foolish</em>!',
        None
    ),
    994: (
        '<strong>Deshonesto</strong> (<em>Des-</em> Un + Honest) | <strong>Tramposo</strong> (Sneaky card-trick cheater — from <em>Trampa</em> Trap!) = <em>Dishonest</em>!',
        None
    ),
    995: (
        '<strong>Humilde</strong> (Grounded close to earth — <em>Humus</em>!) | <strong>Modesto</strong> (Quietly down-to-earth, never brags!) = <em>Humble / Modest</em>!',
        None
    ),
    996: (
        '<strong>Cobarde</strong> ≈ Ducking and hiding behind the sofa at any noise! = <em>Cowardly</em>!',
        None
    ),
    997: (
        '<strong>Generoso / generosa</strong> ≈ Open hands freely sharing bread and coins! = <em>Generous</em>!',
        None
    ),
    998: (
        '1. Greedy: <strong>Codicioso</strong> (<strong>"Coin-Dizzy"</strong>!) | <strong>Avaro</strong> (Tight-fisted <strong>"Avarice"</strong> miser!) = <em>Greedy</em>!<br>2. Selfish: <strong>Egoísta</strong> (Me-first <strong>"Egoist"</strong>!) = <em>Selfish</em>!',
        None
    ),
    1000: (
        '<strong>Creativo / creativa</strong> ≈ Artist\'s colorful palette sparking fresh inventions! = <em>Creative</em>!',
        None
    ),
    1002: (
        '<strong>Confiable</strong> (You can <strong>"Confide"</strong> secrets!) | <strong>Responsable</strong> (Keeps every promise like clockwork!) = <em>Reliable / Responsible</em>!',
        None
    ),
    1003: (
        '1. Mature: <strong>Maduro / madura</strong> (Seasoned wisdom — ripe mind!) = <em>Mature</em>!<br>2. Immature: <strong>Inmaduro / inmadura</strong> (<em>In-</em> Not + <em>Maduro</em> = Childish tantrum!) = <em>Immature</em>!',
        None
    ),
    1004: (
        '<strong>Estricto</strong> (By-the-book!) | <strong>Severo</strong> (Stern-faced <strong>"Severe"</strong> drillmaster!) = <em>Strict</em>!',
        None
    ),
    1005: (
        '<strong>Sensible</strong> ≈ False-friend alert: touches easily like a <em>Touch-me-not</em> leaf = <em>Sensitive</em>!',
        None
    ),
    1006: (
        '<strong>Suave</strong> (Velvet-soft!) | <strong>Tierno</strong> (Gentle lamb!) | <strong>Delicado</strong> (Fragile <strong>"Delicate"</strong> touch!) = <em>Gentle</em>!',
        None
    ),
    1007: (
        '1. Untamed: <strong>Salvaje</strong> (<strong>"Savage"</strong>) | <strong>Silvestre</strong> (Forest-born <strong>"Sylvan"</strong>!) = <em>Wild</em>!<br>2. Crazy: <strong>Loco</strong> (Frenzied) | <strong>Descontrolado</strong> (<em>Des-</em> Out of + Control!) = <em>Uncontrolled</em>!',
        None
    ),
    1008: (
        '<strong>Seguro (de sí mismo)</strong> (<em>Sure</em> of yourself!) | <strong>Confiado</strong> (Walking tall with self-belief!) = <em>Confident</em>!',
        '<strong>Confident</strong> (Steady eye contact &amp; firm voice on stage!) / <strong>Pakka</strong> (<strong>Tamil பக்கா = 100% solid sure!</strong>) = <em>Confident</em>!'
    ),
    1009: (
        '<strong>Leal</strong> (True ally!) | <strong>Fiel</strong> (Faithful — root of <strong>"Fidelity"</strong>!) | <strong>Sincero</strong> (Honest heart!) = <em>Loyal / Sincere</em>!',
        None
    ),
    1010: (
        '<strong>Cruel</strong> (Cold &amp; harsh) | <strong>Despiadado</strong> (<em>Des-</em> Without + <em>Piedad</em> Pity = Ruthless!) = <em>Cruel</em>!',
        None
    ),
    1011: (
        '<strong>Arrogante</strong> (Nose in the air!) | <strong>Creído</strong> (Full of himself!) | <strong>Prepotente</strong> (Overbearing!) = <em>Arrogant</em>!',
        None
    ),
    1012: (
        '<strong>Pacífico</strong> (Calm like the <strong>Pacific Ocean</strong>!) | <strong>Tranquilo</strong> (Quietly serene — <strong>"Tranquil"</strong>!) = <em>Peaceful</em>!',
        None
    ),
    1014: (
        '<strong>Sombrío</strong> (Wrapped in dark <strong>"Sombra"</strong> shadow!) | <strong>Apagado</strong> (Dimmed out) | <strong>Decaído</strong> (Drooping low!) = <em>Gloomy</em>!',
        None
    ),
    1015: (
        '<strong>Enérgico</strong> (Charged dynamo!) | <strong>Activo</strong> (On the move!) | <strong>Lleno de energía</strong> ("Full of energy!") = <em>Energetic</em>!',
        None
    ),
    1016: (
        '<strong>Precavido</strong> (Checks <em>Pre-</em> ahead!) | <strong>Cauteloso</strong> (Stepping carefully on thin ice!) = <em>Cautious</em>!',
        None
    ),
    1017: (
        '<strong>Audaz</strong> (<strong>"Audacious"</strong>!) | <strong>Atrevido</strong> (Daring risk-taker!) | <strong>Valiente</strong> (<strong>"Valiant"</strong> cliff climber!) = <em>Bold</em>!',
        None
    ),
    1018: (
        '1. Not guilty: <strong>Inocente</strong> (Cleared of all charges!) = <em>Innocent</em>!<br>2. Naive/pure: <strong>Ingenuo</strong> (<strong>"Ingenuous"</strong> childlike trust!) | <strong>Inocente</strong> (Pure-hearted!) = <em>Naive / Pure</em>!',
        None
    ),
    1033: (
        '<strong>Temblar</strong> (Teeth-chattering tremor!) | <strong>Tiritar</strong> (Onomatopoeia <em>"Ti-ti-ti"</em> teeth clicking in snow!) = <em>Shiver / Tremble</em>!',
        None
    ),
    1037: (
        '<strong>Inclinarse</strong> (Lean forward respectfully!) | <strong>Hacer una reverencia</strong> (Make a stage curtain bow — <strong>"Reverence"</strong>!) = <em>Bow</em>!',
        None
    ),
    1038: (
        '1. Rest: <strong>Apoyarse</strong> (Prop shoulder against wall!) | <strong>Recargarse</strong> (Rest weight back!) = <em>Lean Against</em>!<br>2. Slant: <strong>Inclinarse</strong> (Tilt like the Leaning Tower!) = <em>Incline</em>!',
        None
    ),
    1040: (
        '1. Fist: <strong>Dar un puñetazo</strong> (Swing fist <em>Puño!</em>) | <strong>Trompada</strong> (Knockout boxer blow!) = <em>Fist Punch</em>!<br>2. Hole: <strong>Perforar</strong> (<strong>"Perforate"</strong>!) | <strong>Ponchar</strong> (Ticket punch!) = <em>Punch Hole</em>!',
        None
    ),
    1043: (
        '<strong>Abrazar</strong> (Wrap both <em>Brazos</em> arms around!) | <strong>Abrazo</strong> (Warm chest-to-chest squeeze!) = <em>Hug</em>!',
        None
    ),
    1045: (
        '<strong>Presentar (a alguien)</strong> ≈ Politely bringing two strangers face to face (<em>"Present"</em> a friend!) = <em>Introduce</em>!',
        None
    ),
    1046: (
        '<strong>Saludar</strong> (Wave <strong>"Salute"</strong> hello!) | <strong>Dar la bienvenida</strong> (Wish a warm <em>Well-come!</em>) = <em>Greet</em>!',
        None
    ),
    1048: (
        '<strong>Divorciarse de / divorcio</strong> ≈ Legally splitting one household into two ("Di-" = Two parts!) = <em>Divorce</em>!',
        None
    ),
    1051: (
        '1. Join: <strong>Adjuntar</strong> (Email clip!) | <strong>Unir</strong> (<strong>"Unite"</strong>) | <strong>Pegar</strong> (Glue-stick!) = <em>Attach</em>!<br>2. Separate: <strong>Separar</strong> (Pull apart) | <strong>Despegar</strong> (Un-stick!) | <strong>Soltar</strong> (Unfasten!) = <em>Detach</em>!',
        None
    ),
    1052: (
        '<strong>Insultar</strong> (Hurl harsh words!) | <strong>Ofensa</strong> (Wounding verbal <strong>"Offense"</strong>!) = <em>Insult</em>!',
        None
    ),
    1056: (
        '1. Console: <strong>Consolar</strong> (<strong>"Console"</strong> a crying friend!) | <strong>Reconfortar</strong> (Re-strengthen hearts!) = <em>Comfort</em>!<br>2. Ease: <strong>Comodidad</strong> (Plush armchair!) | <strong>Confort</strong> (Cozy warmth!) = <em>Physical Comfort</em>!',
        None
    ),
    1057: (
        '<strong>Aplaudir</strong> (Thunderous clapping <strong>"Applause"</strong>!) | <strong>Animar</strong> (Inject spirited <em>Anima</em> cheer!) = <em>Cheer / Applaud</em>!',
        None
    ),
    1059: (
        '<strong>Criticar</strong> ≈ Pointing out every tiny flaw like a harsh film critic! = <em>Criticize</em>!',
        None
    ),
    1063: (
        '<strong>Cooperar</strong> (Work together in harmony!) | <strong>Colaborar</strong> (<em>Co-</em> Together + <em>Labor</em> = Team up!) = <em>Cooperate</em>!',
        None
    ),
    1064: (
        '<strong>Traicionar</strong> ≈ Stabbing an ally in the back (same root as <strong>"Treason"</strong>!) = <em>Betray</em>!',
        None
    ),
    1066: (
        '<strong>Batalla</strong> (War clash!) | <strong>Combate</strong> (Close <strong>"Combat"</strong>!) | <strong>Lucha</strong> (Fierce struggle!) = <em>Battle</em>!',
        None
    ),
    1067: (
        '<strong>Imaginar / imaginarse</strong> ≈ Painting vivid daydream worlds inside your mind! = <em>Imagine</em>!',
        None
    ),
    1068: (
        '<strong>Adivinar</strong> (<strong>"Divine"</strong> an answer!) | <strong>Suponer</strong> (<strong>"Suppose"</strong>) | <strong>Asumir</strong> (<strong>"Assume"</strong>!) = <em>Guess / Suppose / Assume</em>!',
        None
    ),
    1069: (
        '1. Perceive: <strong>Notar</strong> (Spot a <strong>"Note"</strong>!) | <strong>Darse cuenta de</strong> (Realize!) = <em>Notice</em>!<br>2. Warning: <strong>Aviso</strong> (<strong>"Advisory"</strong>) | <strong>Cartel</strong> (Wall poster sign!) = <em>Written Notice</em>!',
        '1. Perceive: <strong>Dhyan jaana</strong> (<strong>Tamil தியானம் = Attention</strong> goes straight to something!) = <em>Notice</em>!<br>2. Warning: <strong>Notice</strong> (Pinned office wall circular!) / <strong>Khabar</strong> (Heads-up alert!) = <em>Notice</em>!'
    ),
    1070: (
        '<strong>Observar</strong> (Watch keenly with a magnifying glass!) | <strong>Mirar con atención</strong> (Look with full attention!) = <em>Observe</em>!',
        None
    ),
    1071: (
        '<strong>Reconocer</strong> ≈ <em>Re-</em> (Again) + <em>Conocer</em> (Know) → Know a familiar face again = <em>Recognize</em>!',
        None
    ),
    1072: (
        '<strong>Identificar</strong> ≈ Matching a fingerprint to its exact owner\'s ID card! = <em>Identify</em>!',
        None
    ),
    1073: (
        '1. Evaluate: <strong>Evaluar</strong> (Grade value!) | <strong>Juzgar</strong> (Weigh pros &amp; cons!) = <em>Evaluate</em>!<br>2. Magistrate: <strong>Juez</strong> (Black-robed courtroom gavel holder!) = <em>Judge</em>!',
        '1. Evaluate: <strong>Parakhna</strong> (Test gold purity — <strong>Tamil பரீட்சை = Examine!</strong>) = <em>Evaluate</em>!<br>2. Magistrate: <strong>Judge</strong> (Robed magistrate banging the courtroom gavel!) = <em>Judge</em>!'
    ),
    1074: (
        '1. Guide: <strong>Dirigir</strong> (Steer film/team!) | <strong>Guiar</strong> (Trail <strong>"Guide"</strong>!) = <em>Direct / Guide</em>!<br>2. Straight: <strong>Directo</strong> (No detours!) | <strong>Recto</strong> (Straight-line <strong>"Rect-angle"</strong>!) = <em>Straightforward</em>!',
        None
    ),
    1075: (
        '<strong>Manejar</strong> (Steer &amp; <strong>"Manage"</strong>!) | <strong>Lidiar con</strong> (Grapple with) | <strong>Sobrellevar</strong> (<em>Sobre-</em> Over + Carry!) = <em>Handle / Cope</em>!',
        None
    ),
    1077: (
        '1. Steer clear: <strong>Evitar</strong> (<strong>"Inevitable"</strong>!) | <strong>Esquivar</strong> (Dodge aside!) = <em>Avoid</em>!<br>2. Stop: <strong>Prevenir</strong> (Catch <em>Pre-</em> before!) | <strong>Impedir</strong> (Block/<strong>"Impede"</strong>!) = <em>Prevent</em>!',
        None
    ),
    1078: (
        '1. Allow: <strong>Permitir</strong> (Grant green pass!) | <strong>Autorizar</strong> (Sign official <strong>"Authorize"</strong> stamp!) = <em>Permit</em>!<br>2. Prohibit: <strong>Prohibir</strong> (Strict red-sign ban!) = <em>Forbid</em>!',
        '1. Allow: <strong>Ijaazat dena</strong> ≈ Sounds like <strong>"Easy-Exit"</strong> green pass granted! = <em>Permit</em>!<br>2. Prohibit: <strong>Mana karna</strong> (Firmly say "No!") / <strong>Rok lagana</strong> (Put a roadblock stop!) = <em>Forbid</em>!'
    ),
    1079: (
        '<strong>Insistir</strong> (Knock again &amp; again!) | <strong>Empeñarse</strong> (Dig your heels in stubbornly!) = <em>Insist</em>!',
        None
    ),
    1080: (
        '<strong>Depender de</strong> (Hang from — like a <em>Pendulum</em>!) | <strong>Confiar en</strong> (Trust <strong>"Confide"</strong> in!) = <em>Depend / Rely</em>!',
        None
    ),
    1082: (
        None,
        '1. Pickle: <strong>Achaar</strong> ≈ <strong>Spoken Tamil ஆச்சார் = Spicy oil-cured mango pickle!</strong> = <em>Pickle</em>!<br>2. Dip: <strong>Chutney</strong> ≈ Fresh ground mint-coconut spicy side dip! = <em>Chutney</em>!'
    ),
    1083: (
        '1. Stew: <strong>Curry</strong> (<strong>Tamil கறி = Spiced gravy!</strong>) | <strong>Estofado con especias</strong> (Spiced slow stew!) = <em>Curry</em>!<br>2. Grain: <strong>Lenteja</strong> ≈ Tiny lens-shaped bean (root of eye <strong>"Lens"</strong>!) = <em>Lentil</em>!',
        None
    ),
    1085: (
        '<strong>Almendra</strong> ≈ Crunchy tear-shaped pale nut wrapped inside a hard shell! = <em>Almond</em>!',
        None
    ),
    1090: (
        '<strong>Canela</strong> ≈ Fragrant brown bark rolled into hollow spice sticks (same shape as <em>Cannelloni</em> tubes!) = <em>Cinnamon</em>!',
        None
    ),
    1092: (
        '<strong>Cilantro / coriandro</strong> ≈ Bright leafy green salsa herb (seeds = <em>Coriandro</em>, fresh leaves = <em>Cilantro!</em>) = <em>Coriander</em>!',
        None
    ),
    1093: (
        '<strong>Menta</strong> (Cool menthol leaf!) | <strong>Hierbabuena</strong> (Literally <em>"Good herb"</em> for tea &amp; mojitos!) = <em>Mint</em>!',
        None
    ),
    1094: (
        '<strong>Culpar</strong> (Pin the <strong>"Culprit"</strong>!) | <strong>Acusar</strong> (Point fingers across court!) = <em>Blame / Accuse</em>!',
        None
    ),
    1096: (
        '1. Admit: <strong>Admitir</strong> (Confess!) | <strong>Confesar</strong> (Spill truth!) = <em>Admit</em>!<br>2. Deny: <strong>Negar</strong> (<strong>"Negate"</strong>!) | <strong>Desmentir</strong> (<em>Des-</em> Call it a <em>Mentira</em> lie!) = <em>Deny</em>!',
        '1. Admit: <strong>Manna</strong> (Accept truth!) / <strong>Qubool karna</strong> (<strong>Tamil கபூல் = Agree/Admit!</strong>) = <em>Admit</em>!<br>2. Deny: <strong>Inkaar karna</strong> (Flatly refuse!) / <strong>Mukarna</strong> (Back out denying!) = <em>Deny</em>!'
    ),
    1097: (
        '<strong>Convencer</strong> (Win over with solid logic!) | <strong>Persuadir</strong> (Talk someone sweetly into agreeing!) = <em>Convince / Persuade</em>!',
        None
    ),
    1098: (
        '<strong>Interrumpir</strong> ≈ <em>Inter-</em> (Between) + <em>Rupt</em> (Break) → Break right into someone\'s sentence = <em>Interrupt</em>!',
        None
    ),
    1100: (
        '<strong>Declarar</strong> (Proclaim loudly!) | <strong>Anunciar</strong> (Broadcast public news on stage!) = <em>Declare / Announce</em>!',
        None
    ),
    1101: (
        '1. Notify: <strong>Informar</strong> (Share facts!) | <strong>Avisar</strong> (Send <strong>"Advisory"</strong> heads-up!) = <em>Inform</em>!<br>2. Refer: <strong>Mencionar</strong> (Drop a name!) | <strong>Nombrar</strong> (<strong>"Name"</strong> briefly!) = <em>Mention</em>!',
        '1. Notify: <strong>Batana</strong> (Tell facts clearly!) / <strong>Khabar dena</strong> (Pass news!) = <em>Inform</em>!<br>2. Refer: <strong>Zikr karna</strong> (Drop a passing reference/name in chat!) = <em>Mention</em>!'
    ),
    1102: (
        '<strong>Aclarar / clarificar</strong> ≈ Turn murky fog <em>Claro</em> (clear!) so everyone sees the point = <em>Clarify</em>!',
        None
    ),
    1103: (
        None,
        '<strong>Nichod nikalna</strong> (Squeeze out the juicy core essence!) / <strong>Short mein batana</strong> (Sum up the long story into 2 quick lines!) = <em>Summarize</em>!'
    ),
    1104: (
        '1. Repeat: <strong>Citar</strong> (<strong>"Cite"</strong> exact speech!) = <em>Quote Words</em>!<br>2. Price: <strong>Cotización</strong> (Price estimate) | <strong>Presupuesto</strong> (<em>Pre-</em> Before + Cost!) = <em>Price Quote</em>!',
        None
    ),
    1105: (
        '1. Oppose: <strong>Contradecir</strong> (<em>Contra-</em> Against + <em>Decir</em> Say = Say the opposite!) = <em>Contradict</em>!<br>2. Dare: <strong>Desafiar</strong> (Boldly defy!) | <strong>Retar</strong> (Throw down a duel challenge!) = <em>Challenge</em>!',
        None
    ),
    1106: (
        '<strong>Trabajo</strong> (Daily toil) | <strong>Empleo</strong> (Paid <strong>"Employment"</strong>) | <strong>Carrera</strong> (Lifelong <strong>"Career"</strong> race!) = <em>Job / Career / Profession</em>!',
        None
    ),
    1107: (
        '<strong>Empleado</strong> (Salaried staff) | <strong>Trabajadora</strong> (Hardworking staff) | <strong>Obrero</strong> (Factory <em>Obra</em> laborer!) = <em>Employee / Worker</em>!',
        None
    ),
    1108: (
        '<strong>Jefe</strong> (Top <strong>"Chief"</strong>!) | <strong>Patrón</strong> (Company <strong>"Patron"</strong> owner!) | <strong>Gerente</strong> (Office floor manager!) = <em>Employer / Boss / Manager</em>!',
        '<strong>Maalik</strong> (<strong>Spoken Tamil மாலிக் = Master/Owner!</strong>) / <strong>Boss</strong> (Corner-office manager calling all shots!) = <em>Employer / Boss / Manager</em>!'
    ),
    1109: (
        '<strong>Asistente</strong> (Right-hand helper!) | <strong>Secretario / secretaria</strong> (Keeps confidential office files — <em>Secrets!</em>) = <em>Assistant / Secretary</em>!',
        '<strong>Madadgaar</strong> (<strong>Spoken Tamil மதத் = Help!</strong>) / <strong>Assistant</strong> (Right-hand desk helper scheduling meetings!) = <em>Assistant / Secretary</em>!'
    ),
    1110: (
        None,
        '1. Clerk: <strong>Clerk</strong> (Front-desk register &amp; stamp handler!) = <em>Clerk</em>!<br>2. Books: <strong>Accountant</strong> (Ledger auditor balancing columns) / <strong>Hisaab rakhne wala</strong> (<strong>Tamil இசாப் = Accounts keeper!</strong>) = <em>Accountant</em>!'
    ),
    1111: (
        '<strong>Abogado / abogada</strong> ≈ Same root as <strong>"Advocate"</strong> — courtroom defender speaking on your behalf = <em>Lawyer / Attorney</em>!',
        None
    ),
    1112: (
        '1. Rank: <strong>Oficial</strong> (Uniformed police/army stripe!) = <em>Officer</em>!<br>2. State: <strong>Funcionario</strong> (Government bureaucrat) | <strong>Directivo</strong> (Executive!) = <em>Official / Officer</em>!',
        None
    ),
    1113: (
        '<strong>Ingeniero / ingeniera</strong> ≈ Root of <strong>"Ingenious"</strong> — blueprint mind building bridges and engines = <em>Engineer</em>!',
        '<strong>Engineer</strong> ≈ Hard-hat bridge, software, and machine builder turning blueprints into reality! = <em>Engineer</em>!'
    ),
    1114: (
        '1. Designer: <strong>Arquitecto</strong> (Sketches skyscraper blueprints!) = <em>Architect</em>!<br>2. Builder: <strong>Contratista</strong> (Hires crew on signed contract!) = <em>Contractor</em>!',
        '1. Designer: <strong>Architect</strong> (Blueprint draftsman) / <strong>Naksha banane wala</strong> (Draws the house map!) = <em>Architect</em>!<br>2. Builder: <strong>Thekedaar</strong> (Holds the construction <em>Theka</em> contract!) = <em>Contractor</em>!'
    ),
    1115: (
        '<strong>Carpintero</strong> ≈ Woodshop craftsman sawing oak timber and hammering joints (root of <em>Carriage-maker</em>!) = <em>Carpenter</em>!',
        None
    ),
    1116: (
        None,
        '<strong>Plumber</strong> (Wrench-turning pipe fitter!) / <strong>Nal theek karne wala</strong> (Fixes leaking <em>Nal</em> water taps!) = <em>Plumber</em>!'
    ),
    1117: (
        '<strong>Electricista</strong> ≈ Tests live circuits, breakers, and sparks to wire up buildings = <em>Electrician</em>!',
        '<strong>Electrician</strong> (Tester-screwdriver pro wiring switches!) / <strong>Bijli wala</strong> (<em>Bijli</em> Lightning/Power expert!) = <em>Electrician</em>!'
    ),
    1118: (
        '<strong>Mecánico / mecánica</strong> ≈ Grease-stained garage wizard tuning car engines = <em>Mechanic</em>!',
        '<strong>Mistri</strong> (Master workshop repair craftsman!) / <strong>Mechanic</strong> (Hood-up car engine fixer!) = <em>Mechanic</em>!'
    ),
    1119: (
        '1. Flight: <strong>Piloto</strong> (Steers jet cockpit!) = <em>Pilot</em>!<br>2. Leader: <strong>Capitán</strong> (Commands ship deck or team!) = <em>Captain</em>!',
        '1. Flight: <strong>Pilot</strong> (Striped uniform flyer in the cockpit!) = <em>Pilot</em>!<br>2. Leader: <strong>Kaptaan</strong> (Ship bridge or cricket skipper!) = <em>Captain</em>!'
    ),
    1120: (
        None,
        '<strong>Jahaazi</strong> (From <em>Jahaaz</em> Ship!) / <strong>Sailor</strong> (Uniformed ocean deckhand tying ropes at sea!) = <em>Sailor</em>!'
    ),
    1121: (
        '<strong>Soldado</strong> (Originally paid with solid gold coin <em>Sueldo</em>!) | <strong>Militar</strong> (Uniformed defense troop!) = <em>Soldier / Military</em>!',
        None
    ),
    1122: (
        '<strong>Agricultor</strong> (Soil cultivator) | <strong>Campesino</strong> (Lives in the green <em>Campo</em> countryside sowing wheat!) = <em>Farmer</em>!',
        None
    ),
    1123: (
        '<strong>Jardinero / jardinera</strong> ≈ Trims hedges and waters roses inside the sunlit <em>Jardín</em> = <em>Gardener</em>!',
        None
    ),
    1124: (
        '<strong>Limpiador</strong> (Makes rooms <em>Limpio</em> sparkling clean!) | <strong>Conserje</strong> (Building caretaker / <strong>"Concierge"</strong>!) = <em>Cleaner / Janitor</em>!',
        None
    ),
    1125: (
        None,
        '<strong>Waiter</strong> ≈ Balancing trays of steaming curry plates to restaurant tables with a crisp napkin! = <em>Waiter / Waitress</em>!'
    ),
    1126: (
        '<strong>Cocinero</strong> (Stirs sizzling pots in the <em>Cocina</em> kitchen!) | <strong>Chef</strong> (Tall-hatted head cook!) = <em>Chef / Cook</em>!',
        '<strong>Rasoiya</strong> (Master of the <em>Rasoi</em> kitchen!) / <strong>Chef</strong> (White-toque culinary artist!) = <em>Chef / Cook</em>!'
    ),
    1127: (
        None,
        '<strong>Qasaai</strong> ≈ <strong>Spoken Tamil கசாப்பு (Kasaappu = Meat butcher!)</strong> slicing fresh cuts at the market = <em>Butcher</em>!'
    ),
    1128: (
        '<strong>Sastre</strong> ≈ Same root as English <strong>"Sartorial"</strong> — measures cloth and stitches crisp custom suits = <em>Tailor</em>!',
        None
    ),
    1129: (
        '1. Author: <strong>Autor</strong> (Originator) | <strong>Escritor</strong> (<strong>"Script"</strong> writer!) = <em>Author</em>!<br>2. Poet: <strong>Poeta / poetisa</strong> (Rhyming verse composer!) = <em>Poet</em>!',
        None
    ),
    1130: (
        '<strong>Artista</strong> (Painter on canvas) | <strong>Escultor</strong> (Chisels marble statues into life!) = <em>Artist / Sculptor</em>!',
        None
    ),
    1131: (
        '<strong>Actor / actriz</strong> ≈ Performs dramatic roles under bright theater spotlights = <em>Actor / Actress</em>!',
        '<strong>Actor</strong> (Star on movie sets!) / <strong>Kalakaar</strong> (<strong>Tamil கலை = Art</strong> performer) / <strong>Hero-heroine</strong> (Cinema lead!) = <em>Actor / Actress</em>!'
    ),
    1132: (
        '<strong>Músico</strong> (Plays violin/drums!) | <strong>Cantante</strong> (Sings melodies — think <strong>"Cantata / Chant"</strong>!) = <em>Musician / Vocalist</em>!',
        '<strong>Musician</strong> (Band instrumentalist!) / <strong>Singer</strong> (Microphone vocalist!) / <strong>Gaane wala</strong> (From <em>Gaana</em> Song!) = <em>Musician / Vocalist</em>!'
    ),
    1133: (
        '<strong>Fotógrafo</strong> (Captures light <em>Photo-</em> frames!) | <strong>Cineasta</strong> (Directs motion pictures at the <em>Cine</em>!) = <em>Photographer / Filmmaker</em>!',
        '<strong>Photographer</strong> (Clicking DSLR shutter lens!) / <strong>Filmmaker</strong> (Calling "Lights, Camera, Action!" on set!) = <em>Photographer / Filmmaker</em>!'
    ),
    1134: (
        '<strong>Periodista</strong> (Writes for the <em>Periódico</em> newspaper!) | <strong>Reportero</strong> (Brings live street news!) = <em>Journalist / Reporter</em>!',
        '<strong>Patrakaar</strong> (<strong>Tamil பத்திரிகை = Newspaper</strong> + <em>Kaar</em>!) / <strong>Reporter</strong> (Holding mic live on breaking news!) = <em>Journalist / Reporter</em>!'
    ),
    1135: (
        '<strong>Detective</strong> (Magnifying-glass sleuth!) | <strong>Investigador</strong> (Follows hidden crime clues!) = <em>Detective / Investigator</em>!',
        None
    ),
    1136: (
        '<strong>Policía</strong> ≈ Keeps peace in the city (Greek <em>Polis</em> = City!) = <em>Police</em>!',
        '<strong>Police</strong> ≈ Khaki/blue uniformed patrol officers keeping neighborhood streets safe! = <em>Police</em>!'
    ),
    1138: (
        '<strong>Paramédico / paramédica</strong> ≈ Racing inside sirens to treat patients beside the ambulance! = <em>Paramedic</em>!',
        '<strong>Paramedic</strong> ≈ Ambulance emergency medic rushing stretchers and oxygen straight to the hospital! = <em>Paramedic</em>!'
    ),
    1139: (
        None,
        '<strong>Resume</strong> (One-page job skills sheet!) / <strong>Bio-data</strong> (Personal qualifications profile!) = <em>Resume / CV</em>!'
    ),
    1140: (
        None,
        '1. Job Q&amp;A: <strong>Interview</strong> (Sitting across the hiring desk answering questions!) = <em>Job Interview</em>!<br>2. Media Q&amp;A: <strong>Interview</strong> (Microphone press sit-down!) = <em>Media Interview</em>!'
    ),
    1141: (
        '<strong>Vacante</strong> (Empty chair waiting!) | <strong>Contratación</strong> (Signing fresh job <em>Contratos!</em>) = <em>Vacancy / Hiring</em>!',
        None
    ),
    1142: (
        '<strong>Salario</strong> (Roman salt pay!) | <strong>Sueldo</strong> (Monthly wage!) | <strong>Ingresos</strong> (Money flowing <em>In!</em>) = <em>Salary / Wage / Income</em>!',
        None
    ),
    1143: (
        '<strong>Bono</strong> (Extra cash reward — <em>Good</em>!) | <strong>Prima</strong> (<strong>"Prime"</strong> top-up payout!) = <em>Bonus</em>!',
        '<strong>Bonus</strong> (Extra festive salary gift!) / <strong>Inaam</strong> (Prize reward for hitting targets!) = <em>Bonus</em>!'
    ),
    1144: (
        '1. Elevation: <strong>Ascenso</strong> (Climbing up!) | <strong>Promoción</strong> (Moving higher!) = <em>Promotion</em>!<br>2. Drop: <strong>Descenso</strong> (Sliding down!) | <strong>Degradación</strong> (Step down!) = <em>Demotion</em>!',
        '1. Elevation: <strong>Tarakki</strong> (Climbing higher!) / <strong>Promotion</strong> (New title &amp; corner desk!) = <em>Promotion</em>!<br>2. Drop: <strong>Demotion</strong> (Rank cut) / <strong>Pad girna</strong> (<em>Pad</em> Rank + <em>Girna</em> Drop!) = <em>Demotion</em>!'
    ),
    1145: (
        '1. Voluntary: <strong>Renuncia</strong> (<strong>"Renounce"</strong> job!) | <strong>Dimisión</strong> (Resigning!) = <em>Resignation</em>!<br>2. Fired: <strong>Despido</strong> (<em>Des-</em> + Show the exit door!) = <em>Dismissal</em>!',
        None
    ),
    1146: (
        '1. Exit: <strong>Jubilación</strong> (<strong>"Jubilee"</strong> celebration!) | <strong>Retiro</strong> (Stepping back!) = <em>Retirement</em>!<br>2. Pay: <strong>Pensión</strong> (Monthly golden-years payout!) = <em>Pension</em>!',
        '1. Exit: <strong>Retirement</strong> (Hanging up the work badge at 60 with a farewell party!) = <em>Retirement</em>!<br>2. Pay: <strong>Pension</strong> (Steady monthly paycheck after retiring!) = <em>Pension</em>!'
    ),
    1147: (
        '<strong>Contrato</strong> ≈ Signed paper binding two parties together ("Drawn together"!) = <em>Contract</em>!',
        '<strong>Contract</strong> (Signed binding agreement!) / <strong>Samjhauta</strong> (Mutual <em>Samajh</em> understanding!) = <em>Contract</em>!'
    ),
    1149: (
        '1. Endeavor: <strong>Proyecto</strong> (Blueprint plan thrown forward!) = <em>Project</em>!<br>2. Cast: <strong>Proyectar</strong> (Beam movie light or forecast!) = <em>To Project</em>!',
        '1. Plan: <strong>Project</strong> (Team blueprint) / <strong>Yojna</strong> (<strong>Tamil யோசனை = Plan!</strong>) = <em>Project</em>!<br>2. Cast: <strong>Parde par dikhana</strong> (Beam onto cinema screen) / <strong>Aage ka sochna</strong> (Look ahead!) = <em>To Project</em>!'
    ),
    1150: (
        None,
        '<strong>Aakhri taareekh</strong> (Final calendar date!) / <strong>Deadline</strong> (Red clock line you cannot cross!) = <em>Deadline</em>!'
    ),
    1151: (
        None,
        '1. Timetable: <strong>Schedule</strong> (Hour-by-hour time grid!) = <em>Schedule</em>!<br>2. Meeting: <strong>Mulaqat ka waqt</strong> (Meet-up time!) / <strong>Appointment</strong> (Booked clinic/office slot!) = <em>Appointment</em>!'
    ),
    1152: (
        '1. Shift: <strong>Turno (de trabajo)</strong> ≈ Taking your assigned clock <strong>"Turn"</strong>! = <em>Work Shift</em>!<br>2. Extra: <strong>Horas extra</strong> ≈ Extra hours stayed past closing = <em>Overtime</em>!',
        '1. Shift: <strong>Shift</strong> ≈ Rotating morning, evening, or night duty block at the factory/office! = <em>Work Shift</em>!<br>2. Extra: <strong>Overtime</strong> ≈ Extra clocked hours past 5 PM earning bonus pay! = <em>Overtime</em>!'
    ),
    1153: (
        '<strong>Vacaciones</strong> (Suitcase getaway!) | <strong>Día feriado</strong> (Official festival red-letter day off!) = <em>Vacation / Holiday</em>!',
        None
    ),
    1154: (
        '1. Burden: <strong>Carga de trabajo</strong> (<strong>"Cargo"</strong> stack of work!) = <em>Workload</em>!<br>2. Crew: <strong>Personal</strong> (Workers) | <strong>Plantilla</strong> (Roster sheet!) = <em>Staff</em>!',
        '1. Burden: <strong>Kaam ka bojh</strong> (Stack of heavy work files!) = <em>Workload</em>!<br>2. Crew: <strong>Staff</strong> (Full team!) / <strong>Karmchari</strong> (<strong>Tamil கர்மம் = Work</strong> doers!) = <em>Staff</em>!'
    ),
    1155: (
        '<strong>Colega</strong> (Office peer!) | <strong>Compañero de trabajo</strong> (Shares bread — <em>Com-panis</em> — at work!) = <em>Colleague / Coworker</em>!',
        None
    ),
    1156: (
        '<strong>Negocio</strong> (Trade deal!) | <strong>Empresa</strong> (<strong>"Enterprise"</strong>) | <strong>Compañía</strong> (Corporate firm!) = <em>Business / Company / Firm</em>!',
        '<strong>Business</strong> (Commerce!) / <strong>Company</strong> (Office firm!) / <strong>Dhandha</strong> (Everyday shop &amp; trade hustle!) = <em>Business / Company / Firm</em>!'
    ),
    1157: (
        '1. Sector: <strong>Industria</strong> (Manufacturing branch!) = <em>Industry</em>!<br>2. Mill: <strong>Fábrica</strong> (Where items are <strong>"Fabricated"</strong>!) | <strong>Planta</strong> (Industrial plant!) = <em>Factory</em>!',
        '1. Sector: <strong>Industry</strong> (Heavy economy!) / <strong>Karobaar</strong> (Trade sector!) = <em>Industry</em>!<br>2. Mill: <strong>Karkhana</strong> (Machine hall!) / <strong>Factory</strong> (Smokestack assembly line!) = <em>Factory</em>!'
    ),
    1159: (
        '<strong>Cliente</strong> (Regular patron!) | <strong>Comprador</strong> (Buyer who <em>Compras</em> shops!) = <em>Customer / Client</em>!',
        None
    ),
    1160: (
        '<strong>Proveedor</strong> (<strong>"Provides"</strong> inventory!) | <strong>Vendedor</strong> (Merchant <strong>"Vendor"</strong>!) = <em>Supplier / Vendor</em>!',
        '<strong>Saamaan bechne wala</strong> (Seller supplying goods!) / <strong>Supplier</strong> (Stock truck delivering crates!) = <em>Supplier / Vendor</em>!'
    ),
    1161: (
        '1. Good: <strong>Producto</strong> (Boxed shelf item!) | <strong>Artículo</strong> (Store <strong>"Article"</strong>!) = <em>Product</em>!<br>2. Help: <strong>Servicio</strong> (Helpful maintenance work!) = <em>Service</em>!',
        '1. Good: <strong>Maal / Saamaan</strong> (<strong>Tamil சாமான் = Goods on shelf!</strong>) = <em>Product</em>!<br>2. Help: <strong>Seva</strong> (<strong>Tamil சேவை!</strong>) / <strong>Service</strong> (Repair &amp; care work!) = <em>Service</em>!'
    ),
    1162: (
        '<strong>Marca</strong> ≈ Stamped cattle/trademark symbol ("Mark") identifying a famous label = <em>Brand</em>!',
        '<strong>Brand</strong> ≈ Iconic logo stamp making sneakers or phones instantly recognizable! = <em>Brand</em>!'
    ),
    1163: (
        '<strong>Precio</strong> (Sticker <strong>"Price"</strong>!) | <strong>Costo</strong> (Total <strong>"Cost"</strong>!) = <em>Price / Cost</em>!',
        None
    ),
    1164: (
        '<strong>Tarifa</strong> (Rate <strong>"Tariff"</strong>) | <strong>Cuota</strong> (Fixed <strong>"Quota"</strong>) | <strong>Cargo</strong> (Bill <strong>"Charge"</strong>!) = <em>Fee / Charge</em>!',
        None
    ),
    1165: (
        '<strong>Cuenta</strong> (Restaurant check!) | <strong>Factura</strong> (Itemized tax <strong>"Invoice"</strong>!) = <em>Bill / Invoice</em>!',
        '<strong>Bill</strong> (Paper check arriving at your table!) / <strong>Hisaab</strong> (<strong>Spoken Tamil ஹிசாப் = Tally account!</strong>) = <em>Bill / Invoice</em>!'
    ),
    1166: (
        '<strong>Recibo</strong> (Proof you <em>Received</em> pay!) | <strong>Comprobante</strong> (Paper proof!) = <em>Receipt</em>!',
        '<strong>Raseed</strong> (<strong>Tamil ரசீது!</strong>) / <strong>Receipt</strong> (Printed supermarket slip proving payment!) = <em>Receipt</em>!'
    ),
    1167: (
        '1. Price cut: <strong>Descuento</strong> (Subtract!) | <strong>Rebaja</strong> (Slash price!) = <em>Discount</em>!<br>2. Payback: <strong>Reembolso</strong> (Back in pocket!) | <strong>Devolución</strong> (Money returned!) = <em>Refund</em>!',
        '1. Price cut: <strong>Discount</strong> (Red "% OFF" tag!) / <strong>Chhoot</strong> (Amount let off!) = <em>Discount</em>!<br>2. Payback: <strong>Paise wapas milna</strong> (Cash returning!) / <strong>Refund</strong> (Returned purchase payout!) = <em>Refund</em>!'
    ),
    1168: (
        '1. Sale: <strong>Rebajas</strong> (Slashed prices!) | <strong>Liquidación</strong> (Clearance!) = <em>Sale</em>!<br>2. Deal: <strong>Ganga</strong> ("Gang-grab"!) | <strong>Buen trato</strong> (Good deal!) = <em>Bargain</em>!',
        '1. Sale: <strong>Sale</strong> (Clearance rack banners!) = <em>Sale</em>!<br>2. Deal: <strong>Sasta sauda</strong> (Cheap lucky deal!) / <strong>Badhiya deal</strong> (Sweet handshake bargain!) = <em>Deal / Bargain</em>!'
    ),
    1169: (
        None,
        '<strong>Cash</strong> (Crisp green/purple bills in hand!) / <strong>Nagad paise</strong> (Instant spot notes, no credit wait!) = <em>Cash / Money</em>!'
    ),
    1170: (
        '1. Metal: <strong>Moneda</strong> (Clinking minted coin — root of <strong>"Money"</strong>!) = <em>Coin</em>!<br>2. Paper: <strong>Billete</strong> (Crisp folded paper bill!) = <em>Banknote</em>!',
        None
    ),
    1171: (
        '<strong>Moneda</strong> (National coin!) | <strong>Divisa</strong> (Foreign exchange note — Dollar, Euro, Rupee!) = <em>Currency</em>!',
        '<strong>Currency</strong> ≈ Official country notes &amp; coins exchanged at airports (USD, EUR, INR)! = <em>Currency</em>!'
    ),
    1172: (
        '1. Wealth: <strong>Riqueza</strong> (From <em>Rico</em> Rich!) | <strong>Fortuna</strong> (Golden <strong>"Fortune"</strong>!) = <em>Wealth</em>!<br>2. Poverty: <strong>Pobreza</strong> (Being <em>Pobre</em> without coins!) = <em>Poverty</em>!',
        None
    ),
    1173: (
        None,
        '<strong>Budget</strong> ≈ Monthly spending envelope dividing income into rent, food, and savings! = <em>Budget</em>!'
    ),
    1174: (
        '<strong>Impuesto</strong> ≈ Government fee <strong>"Imposed"</strong> on salaries and receipts! = <em>Tax</em>!',
        '<strong>Tax</strong> ≈ Mandatory percentage deducted from payslips and store bills for public roads &amp; schools! = <em>Tax</em>!'
    ),
    1176: (
        '1. Put in: <strong>Depositar</strong> (Slide cash in) | <strong>Ingreso</strong> (Money entering!) = <em>Deposit</em>!<br>2. Take out: <strong>Retirar / retiro</strong> (Pull ATM cash out!) = <em>Withdrawal</em>!',
        '1. Put in: <strong>Paise jama karna</strong> (<strong>Tamil ஜமா!</strong>) / <strong>Deposit karna</strong> (Put cash into account!) = <em>Deposit</em>!<br>2. Take out: <strong>Paise nikalna</strong> (Pull crisp bills out of the ATM!) = <em>Withdrawal</em>!'
    ),
    1177: (
        '<strong>Transferir / transferencia</strong> ≈ Wire money moving smoothly across bank accounts! = <em>Transfer</em>!',
        '<strong>Transfer</strong> (Digital wire!) / <strong>Paise bhejna</strong> (Send money to another account!) = <em>Transfer</em>!'
    ),
    1178: (
        '1. Ledger: <strong>Cuenta bancaria</strong> (Bank count book!) = <em>Bank Account</em>!<br>2. Funds: <strong>Saldo</strong> (Net total left!) | <strong>Balance</strong> (Remaining bank balance!) = <em>Balance</em>!',
        '1. Ledger: <strong>Account</strong> (Online passbook) / <strong>Khata</strong> (Traditional ledger book!) = <em>Account</em>!<br>2. Funds: <strong>Balance</strong> (Leftover net sum) / <strong>Bacha hua paisa</strong> (Remaining cash!) = <em>Balance</em>!'
    ),
    1179: (
        '1. Liability: <strong>Deuda</strong> (Money owed — root of <strong>"Debt"</strong>!) = <em>Debt</em>!<br>2. Advance: <strong>Préstamo</strong> (Lent cash!) | <strong>Crédito</strong> (Bank <strong>"Credit"</strong>!) = <em>Loan</em>!',
        '1. Liability: <strong>Karza / Udhaar</strong> (Borrowed money you owe back!) = <em>Debt</em>!<br>2. Advance: <strong>Loan</strong> (Bank credit advance!) / <strong>Karz</strong> (Borrowed sum!) = <em>Loan</em>!'
    ),
    1180: (
        '1. Gain: <strong>Ganancia</strong> (Money gained!) | <strong>Beneficio</strong> (Positive <strong>"Benefit"</strong>!) = <em>Profit</em>!<br>2. Loss: <strong>Pérdida</strong> (Money lost from <em>Perder</em>!) = <em>Loss</em>!',
        None
    ),
    1183: (
        '1. Inspect: <strong>Auditoría</strong> (Tax examiner checking ledgers!) = <em>Audit</em>!<br>2. Trade: <strong>Transacción</strong> (Money swap!) | <strong>Operación</strong> (Bank deal!) = <em>Transaction</em>!',
        '1. Audit: <strong>Hisaab ki jaanch</strong> (<strong>Tamil இசாப்</strong> accounts + careful check!) = <em>Audit</em>!<br>2. Trade: <strong>Len-den</strong> (Give &amp; take!) / <strong>Transaction</strong> (Swiped bank transfer!) = <em>Transaction</em>!'
    ),
    1184: (
        '<strong>Donación</strong> (Generous <strong>"Gift/Donation"</strong>!) | <strong>Caridad</strong> (Warm-hearted <strong>"Charity"</strong>!) = <em>Donation / Charity</em>!',
        None
    ),
    1185: (
        None,
        '<strong>Challan</strong> (Traffic slip) / <strong>Fine</strong> (Cash penalty ticket!) / <strong>Jurmana</strong> (<strong>Tamil ஜுர்மானா = Legal penalty!</strong>) = <em>Fine / Penalty</em>!'
    ),
    1186: (
        '1. System: <strong>Economía</strong> (National money engine!) = <em>Economy</em>!<br>2. Adj: <strong>Financiero / financiera</strong> (Related to banks &amp; budgets!) = <em>Financial</em>!',
        '1. System: <strong>Economy</strong> (National markets) / <strong>Arthavyavastha</strong> (<strong>Tamil அர்த்தம் = Wealth</strong> system!) = <em>Economy</em>!<br>2. Adj: <strong>Aarthik</strong> (Wealth-related) / <strong>Paiso ka</strong> (Of money!) = <em>Financial</em>!'
    ),
    1187: (
        '<strong>Tasa de interés / interés</strong> ≈ Extra percentage fee charged on a loan ("Inter-est" money between lender &amp; borrower)! = <em>Interest / Rate</em>!',
        '<strong>Byaaj</strong> (Extra loan charge — "Buy-charge"!) / <strong>Byaaj rate</strong> (Percentage interest charged per year!) = <em>Interest / Rate</em>!'
    ),
    1188: (
        '1. Capital: <strong>Inversión</strong> (Putting cash into stocks/gold!) = <em>Investment</em>!<br>2. Peril: <strong>Riesgo</strong> (Gambling hazard!) | <strong>Peligro</strong> (Danger!) = <em>Risk</em>!',
        '1. Capital: <strong>Investment</strong> (Planting money to grow) / <strong>Paisa lagana</strong> (Putting capital in!) = <em>Investment</em>!<br>2. Peril: <strong>Khatra</strong> (Danger) / <strong>Risk</strong> (Chance of loss!) = <em>Risk</em>!'
    ),
    1189: (
        '<strong>Seguro</strong> ≈ Policy shield protecting your car, health, and home against accidents (root of <strong>"Ensure"</strong>!) = <em>Insurance</em>!',
        '<strong>Insurance</strong> (Safety net paying medical/car bills!) / <strong>Bima</strong> (Famous <strong>LIC Bima</strong> coverage shield!) = <em>Insurance</em>!'
    ),
    1190: (
        None,
        '<strong>Home loan</strong> (Monthly bank EMIs buying a house!) / <strong>Girvi</strong> (House deed pledged to lender!) = <em>Mortgage</em>!'
    ),
    1191: (
        '1. Surge: <strong>Inflación</strong> (Prices <strong>"Inflating"</strong> like a balloon!) = <em>Inflation</em>!<br>2. Slump: <strong>Recesión</strong> (Economy sliding backwards!) = <em>Recession</em>!',
        None
    ),
    1193: (
        '<strong>Ilegal</strong> (Against law!) | <strong>Ilícito</strong> (Forbidden — origin of <strong>"Illicit"</strong>!) = <em>Illegal / Unlawful</em>!',
        '<strong>Gair-kanooni</strong> (<em>Gair</em> Non + <em>Kanoon</em> Law!) / <strong>Illegal</strong> (Strictly banned under penal code!) = <em>Illegal / Unlawful</em>!'
    ),
    1194: (
        '1. Equity: <strong>Justicia</strong> (Balanced court scales!) = <em>Justice</em>!<br>2. Unfair: <strong>Injusticia</strong> (<em>In-</em> Not + <em>Justicia</em> = Tilted scales!) = <em>Injustice</em>!',
        None
    ),
    1195: (
        '<strong>Tribunal</strong> (Three-judge bench) | <strong>Corte</strong> (Royal/Law hall) | <strong>Juzgado</strong> (Magistrate hall!) = <em>Court / Courtroom</em>!',
        '<strong>Court</strong> (Wood-paneled judge\'s hall!) / <strong>Adalat</strong> (Famous Hindi courtroom — <em>Aap Ki Adalat!</em>) = <em>Court / Courtroom</em>!'
    ),
    1196: (
        '<strong>Juicio</strong> (Courtroom judgment process — <strong>"Judicial"</strong>!) | <strong>Audiencia</strong> (Judge listening to both sides!) = <em>Trial / Hearing</em>!',
        '<strong>Sunwai</strong> (From <em>Sun-na</em> = Official court listening!) / <strong>Court case</strong> (Formal trial inside courtroom!) = <em>Trial / Hearing</em>!'
    ),
    1197: (
        '1. Verdict: <strong>Veredicto</strong> (Truth spoken!) | <strong>Fallo</strong> (Judge\'s ruling!) = <em>Verdict</em>!<br>2. Order: <strong>Condena</strong> (Conviction!) | <strong>Sentencia</strong> (Prison term!) = <em>Sentence</em>!',
        None
    ),
    1198: (
        '<strong>Demanda</strong> (Filing formal court claim!) | <strong>Pleito</strong> (Bitter legal <strong>"Plea"</strong> battle!) = <em>Lawsuit</em>!',
        '<strong>Court case</strong> (Filing papers before a judge!) / <strong>Muqadma</strong> (<strong>Spoken Tamil முகத்மா = Formal court suit!</strong>) = <em>Lawsuit</em>!'
    ),
    1199: (
        '1. Person: <strong>Testigo</strong> (Sworn observer!) = <em>Witness</em>!<br>2. Statement: <strong>Testimonio</strong> (Spoken account!) | <strong>Declaración</strong> (Official record!) = <em>Testimony</em>!',
        None
    ),
    1200: (
        '<strong>Prueba</strong> (Lab proof — think <strong>"Probe"</strong>!) | <strong>Evidencia</strong> (Clear visible clue!) = <em>Evidence / Proof</em>!',
        None
    ),
    1201: (
        '1. Admit: <strong>Confesión</strong> (Admitting guilt!) = <em>Confession</em>!<br>2. Pledge: <strong>Juramento</strong> (Hand raised before <strong>"Jury"</strong>!) = <em>Oath</em>!',
        None
    ),
    1202: (
        '1. Money: <strong>Fianza</strong> (Court <strong>"Finance"</strong> guarantee for release!) = <em>Bail</em>!<br>2. Hold: <strong>Custodia</strong> (Police watch!) | <strong>Detención</strong> (Lockup arrest!) = <em>Custody</em>!',
        '1. Money: <strong>Zamanat</strong> (Pledged release bond!) / <strong>Bail</strong> (Cash deposit letting an accused go home — distinct from Hindi <em>Bail</em> bull!) = <em>Bail</em>!<br>2. Hold: <strong>Police custody</strong> (Cell detention) / <strong>Hirasat</strong> (Police grip!) = <em>Custody</em>!'
    ),
    1203: (
        '<strong>Arrestar</strong> (Seize suspect!) | <strong>Detener</strong> (<strong>"Detain"</strong>/Stop!) | <strong>Arresto</strong> (Handcuff booking!) = <em>Arrest</em>!',
        None
    ),
    1204: (
        '<strong>Víctima</strong> ≈ Innocent person harmed by a crime or disaster! = <em>Victim</em>!',
        '<strong>Shikaar</strong> (Targeted prey!) / <strong>Victim</strong> (Harmed person testifying in court!) = <em>Victim</em>!'
    ),
    1205: (
        '1. Act: <strong>Delito</strong> (Legal offense!) | <strong>Crimen</strong> (Major felony!) = <em>Crime</em>!<br>2. Felon: <strong>Delincuente</strong> (Offender!) | <strong>Criminal</strong> (Lawbreaker!) = <em>Criminal</em>!',
        '1. Act: <strong>Jurm</strong> (Broken law!) / <strong>Crime</strong> (Police-blotter felony!) = <em>Crime</em>!<br>2. Felon: <strong>Mujrim</strong> (Convicted <em>Jurm</em> doer!) / <strong>Criminal</strong> (Wanted suspect!) = <em>Criminal</em>!'
    ),
    1207: (
        '<strong>Fraude</strong> (Scam!) | <strong>Estafa</strong> (Swindle!) | <strong>Falsificación</strong> (<strong>"Falsifying"</strong> fake banknotes!) = <em>Fraud / Forgery</em>!',
        '<strong>Fraud</strong> (Deceptive scam!) / <strong>Dhokhadhadi</strong> (Cheating!) / <strong>Jaal-saazi</strong> (Weaving a fake web <em>Jaal</em>!) = <em>Fraud / Forgery</em>!'
    ),
    1208: (
        '<strong>Soborno</strong> (Under-table cash!) | <strong>Corrupción</strong> (Rotten <strong>"Corrupt"</strong> abuse of power!) = <em>Bribery / Corruption</em>!',
        None
    ),
    1209: (
        None,
        '<strong>Blackmail karna</strong> (Threatening to expose secrets unless paid!) / <strong>Dhamki dena</strong> (Intimidating threat!) = <em>Blackmail</em>!'
    ),
    1210: (
        '1. Abduct: <strong>Secuestro</strong> (Forcefully <strong>"Sequestering"</strong> a person!) = <em>Kidnapping</em>!<br>2. Captive: <strong>Rehén</strong> (Prisoner held for ransom!) = <em>Hostage</em>!',
        '1. Abduct: <strong>Kidnapping</strong> (Forcible snatch!) / <strong>Agwa karna</strong> (Abduct!) = <em>Kidnapping</em>!<br>2. Captive: <strong>Bandhak</strong> (<strong>Tamil பந்தம் = Tied!</strong>) / <strong>Hostage</strong> (Ransom captive!) = <em>Hostage</em>!'
    ),
    1211: (
        '<strong>Asesinato</strong> (<strong>"Assassination"</strong>!) | <strong>Homicidio</strong> (<em>Homo</em> Human + <em>-cide</em> Kill = <strong>"Homicide"</strong>!) = <em>Murder</em>!',
        '<strong>Qatl</strong> (Fatal strike!) / <strong>Khoon</strong> (Spilled blood!) / <strong>Murder</strong> (Intentional killing!) = <em>Murder</em>!'
    ),
    1212: (
        '<strong>Violencia</strong> (Brutal force!) | <strong>Agresión</strong> (Physical <strong>"Aggression"</strong> strike!) = <em>Violence / Assault</em>!',
        None
    ),
    1213: (
        '1. General: <strong>Arma</strong> (Combat <strong>"Arm"</strong>!) = <em>Weapon</em>!<br>2. Firearm: <strong>Pistola</strong> (Handgun!) | <strong>Rifle</strong> (Long barrel rifle!) = <em>Gun</em>!',
        '1. General: <strong>Hathiyaar</strong> (From <em>Haath</em> Hand tool!) = <em>Weapon</em>!<br>2. Firearm: <strong>Bandook</strong> (<strong>Spoken Tamil பந்தூக்!</strong>) / <strong>Gun</strong> (Trigger firearm!) = <em>Gun</em>!'
    ),
    1214: (
        '<strong>Bala</strong> ≈ High-speed lead projectile (same root as <strong>"Ballistic"</strong> missile!) = <em>Bullet</em>!',
        None
    ),
    1215: (
        '1. Device: <strong>Bomba</strong> (Ticking TNT charge!) = <em>Bomb</em>!<br>2. Blast: <strong>Explosión</strong> (Fiery boom &amp; shockwave!) = <em>Explosion</em>!',
        '1. Device: <strong>Bomb</strong> (Live explosive device!) = <em>Bomb</em>!<br>2. Blast: <strong>Dhamaka</strong> (Earth-shaking festive or fiery <strong>Bang!</strong>) = <em>Explosion</em>!'
    ),
    1217: (
        '1. Hooter: <strong>Sirena</strong> (Flashing police <strong>"Siren"</strong>!) = <em>Siren</em>!<br>2. Round: <strong>Patrulla / patrullaje</strong> (Night beat rounds!) = <em>Patrol</em>!',
        '1. Hooter: <strong>Siren</strong> (Wailing red-blue cruiser alarm!) = <em>Siren</em>!<br>2. Round: <strong>Patrol</strong> (Police cruising neighborhood beats — distinct from <em>Petrol</em> fuel!) / <strong>Chakkar lagana</strong> (Making rounds!) = <em>Patrol</em>!'
    ),
    1219: (
        None,
        '1. Lead: <strong>Suraag</strong> (Hidden trace!) / <strong>Clue</strong> (Detective puzzle hint!) = <em>Clue</em>!<br>2. Dactyl: <strong>Fingerprint</strong> (Inked ridge swirl!) / <strong>Ungliyon ke nishaan</strong> (Finger marks!) = <em>Fingerprint</em>!'
    ),
    1220: (
        '1. Watch: <strong>Vigilancia</strong> (Stay <strong>"Vigilant"</strong> on CCTV!) = <em>Surveillance</em>!<br>2. Q&amp;A: <strong>Interrogatorio</strong> (Bright-lamp questioning!) = <em>Interrogation</em>!',
        None
    ),
    1221: (
        None,
        '<strong>Raid</strong> (Surprise dawn sweep!) / <strong>Chhapemaari</strong> (Sudden stamped surprise search!) = <em>Raid</em>!'
    ),
    1222: (
        '1. Prison: <strong>Prisión</strong> (Penitentiary) | <strong>Cárcel</strong> (Root of <strong>"Incarcerate"</strong>!) = <em>Prison / Jail</em>!<br>2. Cell: <strong>Celda</strong> (Iron-barred lockup room!) = <em>Cell</em>!',
        '1. Building: <strong>Jail</strong> (Barred penitentiary!) = <em>Prison / Jail</em>!<br>2. Lockup: <strong>Kothri</strong> (Tight stone lockup room!) / <strong>Cell</strong> (Single iron-barred compartment — distinct from biology cell!) = <em>Cell</em>!'
    ),
    1223: (
        '<strong>Preso</strong> (Captured!) | <strong>Prisionero</strong> (Jailed captive!) | <strong>Convicto</strong> (Found guilty <strong>"Convict"</strong>!) = <em>Prisoner / Convict</em>!',
        None
    ),
    1225: (
        None,
        '<strong>Warrant</strong> ≈ Judge-signed court slip authorizing police search or arrest! = <em>Warrant</em>!'
    ),
    1226: (
        '<strong>Gobierno</strong> ≈ State cabinet steering the ship (same Greek origin as <em>"Governor"</em>!) = <em>Government</em>!',
        None
    ),
    1227: (
        '1. Nation: <strong>Nación</strong> (Sovereign people) | <strong>País</strong> (Country land!) = <em>Nation</em>!<br>2. Republic: <strong>República</strong> (Elected non-royal state!) = <em>Republic</em>!',
        '1. Nation: <strong>Desh</strong> (<strong>Tamil தேசம்!</strong>) = <em>Nation</em>!<br>2. Republic: <strong>Loktantra</strong> (<strong>Tamil லோகம்</strong> People rule!) / <strong>Republic</strong> (Citizen-elected head of state!) = <em>Republic</em>!'
    ),
    1228: (
        '1. Rule: <strong>Democracia</strong> (<em>Demos</em> People + <em>Kratos</em> Power = People\'s vote!) = <em>Democracy</em>!<br>2. Charter: <strong>Constitución</strong> (Supreme law book!) = <em>Constitution</em>!',
        '1. Rule: <strong>Loktantra</strong> (<strong>Tamil லோகம்</strong> People\'s system!) / <strong>Democracy</strong> (Ballot-box rule!) = <em>Democracy</em>!<br>2. Charter: <strong>Samvidhan</strong> (<strong>Tamil சமம் + விதி!</strong>) = <em>Constitution</em>!'
    ),
    1229: (
        '<strong>Parlamento</strong> (From <em>Parlar</em> = Speak/Debate hall!) | <strong>Congreso</strong> (Lawmakers gathering together!) = <em>Parliament / Congress</em>!',
        '<strong>Sansad</strong> (Grand lawmakers chamber where MPs sit!) / <strong>Parliament</strong> (Bicameral legislative house!) = <em>Parliament / Congress</em>!'
    ),
    1230: (
        '1. Policy: <strong>Política</strong> (Action plan!) | <strong>Directriz</strong> (Guideline!) = <em>Policy</em>!<br>2. Statute: <strong>Legislación</strong> (Bills passed!) | <strong>Ley</strong> (Law!) = <em>Legislation</em>!',
        '1. Policy: <strong>Policy</strong> (Guiding plan!) / <strong>Niyam</strong> (<strong>Tamil நியமம் = Rule!</strong>) = <em>Policy</em>!<br>2. Law: <strong>Kanoon</strong> (<strong>Spoken Tamil கானூன் = Enacted law!</strong>) = <em>Legislation</em>!'
    ),
    1231: (
        '<strong>Político / política</strong> ≈ Elected campaigner debating bills inside city halls (Greek <em>Polis</em> = City!) = <em>Politician</em>!',
        None
    ),
    1232: (
        '1. President: <strong>Presidente / presidenta</strong> (Sits at head — <em>Pre-siding</em>!) = <em>President</em>!<br>2. PM: <strong>Primer ministro</strong> (First/Chief cabinet minister!) = <em>Prime Minister</em>!',
        '1. President: <strong>Rashtrapati</strong> (<strong>Tamil ராஷ்ட்ரபதி!</strong>) / <strong>President</strong> (Head of state!) = <em>President</em>!<br>2. PM: <strong>Pradhan mantri</strong> (<strong>Tamil பிரதான மந்திரி = Chief Minister!</strong>) = <em>Prime Minister</em>!'
    ),
    1233: (
        '1. Leader: <strong>Ministro / ministra</strong> (Cabinet official serving state!) = <em>Minister</em>!<br>2. Dept: <strong>Ministerio</strong> (Government headquarters building!) = <em>Ministry</em>!',
        '1. Leader: <strong>Mantri</strong> (<strong>Tamil மந்திரி = Cabinet minister!</strong>) = <em>Minister</em>!<br>2. Dept: <strong>Ministry</strong> (Executive department!) / <strong>Mantralaya</strong> (<em>Mantri + Alaya</em> House = Ministry!) = <em>Ministry</em>!'
    ),
    1234: (
        '1. City: <strong>Alcalde / alcaldesa</strong> (Chief city mayor — Arabic <em>Al-Qadi</em>!) = <em>Mayor</em>!<br>2. State: <strong>Gobernador</strong> (Chief executive steering a state!) = <em>Governor</em>!',
        '1. City: <strong>Mayor</strong> (Elected municipal head holding city keys!) = <em>Mayor</em>!<br>2. State: <strong>Governor</strong> (State head!) / <strong>Rajyapaal</strong> (<strong>Tamil ராஜ்ஜியம்</strong> State protector!) = <em>Governor</em>!'
    ),
    1235: (
        '1. Person: <strong>Ciudadano</strong> (Legal city/country member — <em>Ciudad!</em>) = <em>Citizen</em>!<br>2. Status: <strong>Nacionalidad</strong> (Passport country bond!) = <em>Nationality</em>!',
        None
    ),
    1236: (
        '1. Rivals: <strong>Oposición</strong> (Minority bench across the aisle!) = <em>Opposition</em>!<br>2. Alliance: <strong>Coalición</strong> (Parties uniting together!) = <em>Coalition</em>!',
        '1. Rivals: <strong>Opposition</strong> (Across-aisle critics!) / <strong>Vipaksh</strong> (<strong>Tamil பட்சம் = Opposite side!</strong>) = <em>Opposition</em>!<br>2. Alliance: <strong>Gathbandhan</strong> (<strong>Tamil பந்தம்!</strong>) / <strong>Alliance</strong> (United front!) = <em>Coalition</em>!'
    ),
    1237: (
        '1. Greater: <strong>Mayoría</strong> (Over 50% larger block!) = <em>Majority</em>!<br>2. Lesser: <strong>Minoría</strong> (Smaller group of seats!) = <em>Minority</em>!',
        '1. Greater: <strong>Bahumat</strong> (<strong>Tamil வெகு + மதம்</strong> Most votes!) / <strong>Zyada log</strong> (More people!) = <em>Majority</em>!<br>2. Lesser: <strong>Kam log</strong> (Fewer people!) / <strong>Minority</strong> (Smaller share!) = <em>Minority</em>!'
    ),
    1238: (
        '1. Right: <strong>Autoridad</strong> (Official badge to issue orders!) = <em>Authority</em>!<br>2. Rule: <strong>Poder</strong> (<strong>"Potent"</strong> strength!) | <strong>Mando</strong> (Command!) = <em>Power / Rule</em>!',
        '1. Right: <strong>Power</strong> (Command badge!) / <strong>Adhikaar</strong> (<strong>Tamil அதிகாரம்!</strong>) = <em>Authority</em>!<br>2. Rule: <strong>Taakat</strong> (Mighty strength!) / <strong>Raaj</strong> (<strong>Tamil ராஜ்ஜியம் = Reign!</strong>) = <em>Power / Rule</em>!'
    ),
    1239: (
        '1. Process: <strong>Elecciones</strong> (Choosing leaders on polling day!) = <em>Election</em>!<br>2. Ballot: <strong>Voto / votar</strong> (Dropping ballot paper!) = <em>Vote</em>!',
        '1. Process: <strong>Chunaav</strong> (Choosing!) / <strong>Election</strong> (Ballot polling day!) = <em>Election</em>!<br>2. Ballot: <strong>Vote / Vote dena</strong> (Inked finger casting a ballot choice!) = <em>Vote</em>!'
    ),
    1240: (
        '1. Drive: <strong>Campaña</strong> (Touring cities for rallies!) = <em>Campaign</em>!<br>2. Nominee: <strong>Candidato / candidata</strong> (Roman white-toga hopeful!) = <em>Candidate</em>!',
        '1. Drive: <strong>Campaign</strong> (Election posters!) / <strong>Prachaar</strong> (<strong>Tamil பிரச்சாரம்!</strong>) = <em>Campaign</em>!<br>2. Nominee: <strong>Candidate</strong> (Ballot name!) / <strong>Umeedwaar</strong> (Hopeful contender!) = <em>Candidate</em>!'
    ),
    1241: (
        '<strong>Reforma</strong> ≈ <em>Re-</em> (Again) + <em>Forma</em> (Shape) → Reshaping laws for the better = <em>Reform</em>!',
        None
    ),
    1242: (
        '1. Legal: <strong>Derecho</strong> (Human entitlement!) = <em>Right</em>!<br>2. Free: <strong>Libertad</strong> (Broken chains — Statue of <strong>"Liberty"</strong>!) = <em>Freedom / Liberty</em>!',
        None
    ),
    1243: (
        '<strong>Protesta</strong> (Loud street objection!) | <strong>Manifestación</strong> (Marching banner display — <strong>"Manifest"</strong>!) = <em>Protest / Rally</em>!',
        '<strong>Dharna</strong> (Peaceful sit-in protest!) / <strong>Virodh</strong> (Opposition!) / <strong>Rally</strong> (Chanting street march!) = <em>Protest / Rally</em>!'
    ),
    1244: (
        None,
        '1. Walkout: <strong>Hartal</strong> (Shop-shutter strike!) / <strong>Strike</strong> (Workers holding picket signs!) = <em>Strike</em>!<br>2. Shun: <strong>Boycott</strong> (Refusing goods!) / <strong>Mana karna</strong> (Say firm NO!) = <em>Boycott</em>!'
    ),
    1245: (
        '1. Overthrow: <strong>Revolución</strong> (Turning the entire wheel — <em>Re-volve</em> — toppling rulers!) = <em>Revolution</em>!<br>2. Campaign: <strong>Movimiento</strong> (Organized mass march!) = <em>Movement</em>!',
        None
    ),
    1246: (
        '1. Campaigner: <strong>Activista</strong> (Takes active steps for justice!) = <em>Activist</em>!<br>2. Helper: <strong>Voluntario / voluntaria</strong> (Serves by free will!) = <em>Volunteer</em>!',
        '1. Campaigner: <strong>Activist</strong> (Banner organizer!) / <strong>Karyakarta</strong> (Dedicated worker!) = <em>Activist</em>!<br>2. Helper: <strong>Volunteer</strong> (Unpaid helper!) / <strong>Madadgaar</strong> (<strong>Spoken Tamil மதத் = Help!</strong>) = <em>Volunteer</em>!'
    ),
    1247: (
        '<strong>Igualdad</strong> (From <em>Igual</em> Equal!) | <strong>Equidad</strong> (Fair balance — <strong>"Equity"</strong>!) = <em>Equality / Fairness</em>!',
        None
    ),
    1248: (
        '<strong>Discriminación</strong> (Unfair divide!) | <strong>Prejuicio</strong> (<em>Pre-</em> Before + <em>Juicio</em> Judge = Judging before knowing!) = <em>Discrimination / Prejudice</em>!',
        None
    ),
    1249: (
        '1. Public: <strong>Sociedad</strong> (All citizens together!) = <em>Society</em>!<br>2. Local: <strong>Comunidad</strong> (Tight neighborhood sharing life!) = <em>Community</em>!',
        '1. Public: <strong>Society</strong> (Modern network!) / <strong>Samaaj</strong> (<strong>Tamil சமாஜம்!</strong>) = <em>Society</em>!<br>2. Local: <strong>Community</strong> (Neighborhood circle!) / <strong>Basti</strong> (Close local settlement!) = <em>Community</em>!'
    ),
    1250: (
        '<strong>Público</strong> (Open to every taxpayer!) | <strong>Cívico</strong> (Town citizen duties — <strong>"Civic"</strong>!) = <em>Public / Civic</em>!',
        None
    ),
    1251: (
        '1. Asylum: <strong>Refugiado / refugiada</strong> (Fleeing war seeking safe shelter/refuge!) = <em>Refugee</em>!<br>2. Migrant: <strong>Inmigrante</strong> (Moving <em>In-</em> to settle permanently!) = <em>Immigrant</em>!',
        '1. Asylum: <strong>Refugee</strong> (Border tent-camp survivor) / <strong>Bahar se aaye log</strong> (Folks who arrived from outside!) = <em>Refugee</em>!<br>2. Migrant: <strong>Bahar se aaya hua</strong> (Came from abroad) / <strong>Immigrant</strong> (New permanent resident!) = <em>Immigrant</em>!'
    ),
    1252: (
        '1. Global: <strong>Internacional</strong> (Cross-border!) | <strong>Global</strong> (Worldwide!) = <em>International</em>!<br>2. Abroad: <strong>Extranjero / extranjera</strong> (From a strange/distant land!) = <em>Foreign</em>!',
        '1. Global: <strong>International</strong> (Flags of every continent flying outside the UN!) = <em>International</em>!<br>2. Abroad: <strong>Videshi</strong> (<strong>Tamil தேசம்</strong> Country → <em>Vi-deshi</em> = From an outside land!) = <em>Foreign</em>!'
    ),
    1253: (
        '1. Statecraft: <strong>Diplomacia</strong> (Envoys negotiating treaties calmly!) = <em>Diplomacy</em>!<br>2. Office: <strong>Embajada</strong> (Official foreign mission building!) = <em>Embassy</em>!',
        '1. Statecraft: <strong>Diplomacy</strong> (Tactful peace talks between ambassadors!) = <em>Diplomacy</em>!<br>2. Office: <strong>Embassy</strong> (Guarded passport compound flying another nation\'s flag!) = <em>Embassy</em>!'
    ),
    1254: (
        '<strong>Frontera</strong> (Guarded <strong>"Frontier"</strong> checkpoint!) | <strong>Límite</strong> (Drawn boundary <strong>"Limit"</strong>!) = <em>Border / Boundary</em>!',
        '<strong>Border</strong> (Guarded checkpoint fence!) / <strong>Sarhad</strong> (<strong>Sar</strong> Head + <strong>Had</strong> Limit = Nation boundary!) = <em>Border / Boundary</em>!'
    ),
    1255: (
        '1. Row: <strong>Disputa</strong> (Heated debate!) | <strong>Riña</strong> (Brawl!) = <em>Dispute</em>!<br>2. Clash: <strong>Conflicto</strong> (Armed clash!) = <em>Conflict</em>!<br>3. Tipping point: <strong>Crisis</strong> (Emergency moment!) = <em>Crisis</em>!',
        '1. Row: <strong>Jhagda</strong> (Loud quarrel!) = <em>Dispute</em>!<br>2. Clash: <strong>Takraav / Ladai</strong> (Head-on collision fight!) = <em>Conflict</em>!<br>3. Crisis: <strong>Sankat</strong> (<strong>Tamil சங்கடம்!</strong>) / <strong>Crisis</strong> (Red-alert emergency!) = <em>Crisis</em>!'
    ),
    1256: (
        '<strong>Guerra</strong> (All-out war — root of <strong>"Guerrilla"</strong>!) | <strong>Combate</strong> (Frontline <strong>"Combat"</strong>!) = <em>War / Combat</em>!',
        None
    ),
    1257: (
        None,
        '1. Army: <strong>Fauj</strong> (Marching armed ranks!) / <strong>Army</strong> (Olive-camo land force!) = <em>Military / Army</em>!<br>2. Fleet: <strong>Navy</strong> (Warship fleet!) / <strong>Samundari fauj</strong> (Sea army!) = <em>Navy</em>!'
    ),
    1258: (
        '<strong>Comandante</strong> (Gives tactical orders!) | <strong>General</strong> (Highest 4-star army rank!) = <em>Commander / General</em>!',
        '<strong>Commander</strong> (Top tactical unit officer!) / <strong>General</strong> (Four-star army chief!) = <em>Commander / General</em>!'
    ),
    1259: (
        '<strong>Invasión</strong> (Troops marching over borders!) | <strong>Ataque</strong> (Sudden frontline strike!) = <em>Invasion / Attack</em>!',
        None
    ),
    1260: (
        '1. Triumph: <strong>Victoria</strong> (Champion cup!) | <strong>Triunfo</strong> (Sweet <strong>"Triumph"</strong>!) = <em>Victory</em>!<br>2. Loss: <strong>Derrota</strong> (Army put to <strong>"Rout"</strong>!) = <em>Defeat</em>!',
        '1. Triumph: <strong>Jeet</strong> ≈ <strong>Tamil ஜெயம் (Jeyam = Victory!)</strong> → Lifting the gold trophy! = <em>Victory</em>!<br>2. Loss: <strong>Haar</strong> ≈ Losing a battle or match (<strong>"Haar maanna"</strong> = admit defeat — distinct from garland <em>Haar</em>!) = <em>Defeat</em>!'
    ),
    1261: (
        '1. Capitulate: <strong>Rendirse / rendición</strong> (Surrendering arms!) = <em>Surrender</em>!<br>2. Halt: <strong>Alto el fuego</strong> ("Halt the fire!") | <strong>Tregua</strong> (<strong>"Truce"</strong>!) = <em>Ceasefire</em>!',
        '1. Capitulate: <strong>Hathiyaar daalna</strong> (Drop weapons!) / <strong>Surrender karna</strong> (Raise white flag!) = <em>Surrender</em>!<br>2. Halt: <strong>Ceasefire</strong> (Silence guns!) / <strong>Jung rokna</strong> (Stop war!) = <em>Ceasefire</em>!'
    ),
}


def main():
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        lines = f.read().splitlines(True)

    sc_idx = next(i for i, l in enumerate(lines) if l.startswith("var cardShortcuts = "))
    s5_idx = next(i for i, l in enumerate(lines) if l.startswith("var split5DeckCards = "))
    s6_idx = next(i for i, l in enumerate(lines) if l.startswith("var split6DeckCards = "))

    card_shortcuts = json.loads(lines[sc_idx][len("var cardShortcuts = "):].rstrip().rstrip(";"))
    split5 = json.loads(lines[s5_idx][len("var split5DeckCards = "):].rstrip().rstrip(";"))
    split6 = json.loads(lines[s6_idx][len("var split6DeckCards = "):].rstrip().rstrip(";"))

    assert len(split5) == 272 and split5[0]["num"] == 822 and split5[-1]["num"] == 1093, f"Unexpected split5: {len(split5)}"
    assert len(split6) == 169 and split6[0]["num"] == 1094 and split6[-1]["num"] == 1262, f"Unexpected split6: {len(split6)}"

    updated_by_num = {}
    for c in split5 + split6:
        n = c["num"]
        if n in TAMIL_UPDATES:
            c["tamil"] = TAMIL_UPDATES[n]
        if n in SHORTCUT_UPDATES:
            ses, shi = SHORTCUT_UPDATES[n]
            if ses is not None:
                c["shortcutEs"] = ses
            if shi is not None:
                c["shortcutHi"] = shi
        if n in IMAGE_UPGRADES:
            c["imageUrl"] = IMAGE_UPGRADES[n]
            c["gifUrl"] = IMAGE_UPGRADES[n]

        # Ensure 100% sync with cardShortcuts
        card_shortcuts[str(n)] = {
            "es": c["shortcutEs"],
            "hi": c["shortcutHi"],
        }
        updated_by_num[n] = c

    lines[sc_idx] = "var cardShortcuts = " + json.dumps(card_shortcuts, ensure_ascii=False) + ";\n"
    lines[s5_idx] = "var split5DeckCards = " + json.dumps(split5, ensure_ascii=False) + ";\n"
    lines[s6_idx] = "var split6DeckCards = " + json.dumps(split6, ensure_ascii=False) + ";\n"

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.writelines(lines)

    # Sync data/backup_original_cards.json
    if os.path.exists(BACKUP_PATH):
        with open(BACKUP_PATH, "r", encoding="utf-8") as f:
            bkp = json.load(f)
        items = bkp.values() if isinstance(bkp, dict) else bkp
        for val in items:
            if isinstance(val, dict):
                n = val.get("originalNum") or val.get("num")
                if n in updated_by_num:
                    src = updated_by_num[n]
                    val["trans"] = dict(src["trans"])
                    val["hiDevanagari"] = src["hiDevanagari"]
                    val["tamil"] = src["tamil"]
                    val["shortcutEs"] = src["shortcutEs"]
                    val["shortcutHi"] = src["shortcutHi"]
                    val["imageUrl"] = src["imageUrl"]
                    val["gifUrl"] = src["gifUrl"]
        with open(BACKUP_PATH, "w", encoding="utf-8") as f:
            json.dump(bkp, f, indent=2, ensure_ascii=False)

    print(
        f"Updated Split 5 & 6 (#822-#1262): {len(split5) + len(split6)} cards synced | "
        f"Tamil fixes: {len(TAMIL_UPDATES)} | Shortcuts upgraded: {len(SHORTCUT_UPDATES)} | "
        f"Images upgraded: {len(IMAGE_UPGRADES)}"
    )


if __name__ == "__main__":
    main()
