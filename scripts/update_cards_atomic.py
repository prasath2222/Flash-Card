import json
import os
import re

INDEX_PATH = "index.html"
BACKUP_PATH = "data/backup_original_cards.json"

# Exact atomic updates for Split 8 (Cards 1363-1446)
# Every card has crystal-clear, genuine Tamil/English/sound-alike shortcuts covering ALL words per sense.
SPLIT8_UPDATES = {
    1363: {
        "es": "Medio ambiente / entorno",
        "hi": "Mahaul / environment",
        "shortcutEs": '<strong>Medio ambiente</strong> ≈ <strong>Medio</strong> (Midst) + <strong>Ambiente ("Ambient")</strong> → The ambient world around us = <em>Environment</em>! | <strong>Entorno</strong> ≈ <strong>En-</strong> + Root of <strong>"Turn"</strong> (everything when you turn around = <em>Surroundings</em>)!',
        "shortcutHi": '<strong>Mahaul</strong> ≈ Good <strong>Mahasul (Tamil மகசூல் = harvest)</strong> needs a calm green <strong>Mahaul</strong> (Atmosphere / Surroundings)! | <strong>Environment</strong> ≈ Same everyday English word used directly in spoken Hindi (<em>Natural Environment</em>)!',
    },
    1364: {
        "es": "Contaminación / polución",
        "hi": "Pradushan / gandagi / pollution",
        "shortcutEs": '<strong>Contaminación</strong> ≈ Direct sibling of English <strong>"Contamination"</strong> → Dirtying air or water = <em>Pollution</em>! | <strong>Polución</strong> ≈ Direct sibling of English <strong>"Pollution"</strong> → Toxic factory smoke!',
        "shortcutHi": '<strong>Pradushan</strong> ≈ <strong>Pra-</strong> + <strong>Dushan (Tamil தூஷணம் = defile/taint!)</strong> → Tainting air/water = <em>Pollution</em>! | <strong>Gandagi</strong> ≈ From <strong>Ganda (Dirty)</strong> → Filth & <em>Contamination</em>! | <strong>Pollution</strong> ≈ Same everyday English word used directly in spoken Hindi!',
    },
    1365: {
        "es": "1. Trash/debris: Residuos / desechos / basura | 2. Misuse/squander: Desperdicio / malgasto",
        "hi": "1. Trash/debris: Kachra / kooda | 2. Misuse/squander: Fizool kharchi / barbaadi",
        "shortcutEs": '1. Trash/debris: <strong>Residuos</strong> ≈ <strong>"Residue"</strong> (leftover waste)! | <strong>Desechos</strong> ≈ <strong>Des-echar</strong> (thrown-out scraps/debris)! | <strong>Basura</strong> ≈ Sounds like <strong>"Bash-Bin / Mess-ura"</strong> → Kitchen bin <em>Garbage (Basura)</em>!<br>2. Misuse/squander: <strong>Desperdicio</strong> ≈ <strong>Des- + Perder ("Lose/Perish")</strong> → Throwing food or money away = <em>Waste</em>! | <strong>Malgasto</strong> ≈ <strong>Mal</strong> (Badly) + <strong>Gastar</strong> (Spend) = <em>Squandering / Misuse</em>!',
        "shortcutHi": '1. Trash/debris: <strong>Kachra</strong> ≈ <strong>Spoken Tamil கச்சடா (Kachada = trash!)</strong> → Exact same word for <em>Garbage</em>! | <strong>Kooda</strong> ≈ Household dustbin trash = <em>Kooda (Trash)</em>!<br>2. Misuse/squander: <strong>Fizool kharchi</strong> ≈ <strong>Fizool</strong> (Useless/Frivolous) + <strong>Kharchi (Tamil செலவு / Kharchu = Spending!)</strong> = <em>Wasteful Spending</em>! | <strong>Barbaadi</strong> ≈ <strong>Barbaad</strong> ("Burned-Bad" ruin) = Total <em>Waste / Ruin</em>!',
    },
    1366: {
        "es": "Reciclar",
        "hi": "Recycle karna / dobaara istemaal karna",
        "shortcutEs": '<strong>Reciclar</strong> ≈ Direct sibling of English <strong>"Recycle" (Re- + Ciclo "Cycle")</strong> → Put plastic/paper back in the loop = <em>Recycle</em>!',
        "shortcutHi": '<strong>Recycle karna</strong> ≈ English <strong>"Recycle"</strong> + <strong>Karna</strong> (To do)! | <strong>Dobaara istemaal karna</strong> ≈ <strong>Dobaara</strong> (Second time — <em>Do</em> = Two + <em>Baar</em> = Time) + <strong>Istemaal</strong> (Use) = Reuse / <em>Recycle</em>!',
    },
    1367: {
        "es": "1. Arid rain lack: Sequía | 2. Water deluge overflow: Inundación",
        "hi": "1. Arid rain lack: Sookha | 2. Water deluge overflow: Baadh",
        "shortcutEs": '1. Arid rain lack: <strong>Sequía</strong> ≈ From <strong>Seco ("Desiccated / Dry")</strong> → Cracked dry earth with zero rain = <em>Drought</em>!<br>2. Water deluge overflow: <strong>Inundación</strong> ≈ Direct sibling of English <strong>"Inundation"</strong> (water pouring everywhere) = <em>Flood</em>!',
        "shortcutHi": '1. Arid rain lack: <strong>Sookha</strong> ≈ Same root as <strong>Tamil சுக்கு (Sukku = Dried ginger → Dry!)</strong> → Dry cracked land = <em>Drought</em>!<br>2. Water deluge overflow: <strong>Baadh</strong> ≈ Sounds like <strong>"Water-Bar-Broken!"</strong> (big wave bursting a dam) = <em>Flood (Baadh)</em>!',
    },
    1368: {
        "es": "1. Wild animals: Vida silvestre / fauna | 2. Species dying out: Extinción",
        "hi": "1. Wild animals: Jangli jaanwar | 2. Species dying out: Khatam hona / gayab hona",
        "shortcutEs": '1. Wild animals: <strong>Vida silvestre</strong> ≈ <strong>Vida ("Vital" Life)</strong> + <strong>Silvestre ("Sylvan" Forest)</strong> → Forest creatures = <em>Wildlife</em>! | <strong>Fauna</strong> ≈ English scientific term <strong>"Fauna"</strong> (all animal life)!<br>2. Species dying out: <strong>Extinción</strong> ≈ Direct sibling of English <strong>"Extinction"</strong> → Vanishing forever!',
        "shortcutHi": '1. Wild animals: <strong>Jangli jaanwar</strong> ≈ <strong>Jangli ("Jungle" wild)</strong> + <strong>Jaanwar (Life/Tamil ஜீவன்)</strong> = <em>Wild Animals</em>!<br>2. Species dying out: <strong>Khatam hona</strong> ≈ <strong>Spoken Tamil கத்தம் (Khattham = Finished completely!)</strong> → Wiped out! | <strong>Gayab hona</strong> ≈ Vanishing out of sight = Going <em>Extinct</em>!',
    },
    1369: {
        "es": "Agricultura / cultivo",
        "hi": "Kheti-baadi / kheti",
        "shortcutEs": '<strong>Agricultura</strong> ≈ Direct sibling of English <strong>"Agriculture"</strong>! | <strong>Cultivo</strong> ≈ From <strong>"Cultivate"</strong> → Growing crops on a farm = <em>Farming / Cultivation</em>!',
        "shortcutHi": '<strong>Kheti-baadi / kheti</strong> ≈ From <strong>Khet (Crop field)</strong> + <strong>Baadi (Garden/Orchard)</strong> → Ploughing fields = <em>Farming / Agriculture</em>!',
    },
    1370: {
        "es": "1. Grain crop storage: Granero | 2. Horse/cattle stall: Establo / caballeriza",
        "hi": "1. Grain crop storage: Godown / anaaj ghar | 2. Horse/cattle stall: Tabela",
        "shortcutEs": '1. Grain crop storage: <strong>Granero</strong> ≈ Direct sibling of English <strong>"Granary"</strong> (<em>Grano</em> = Grain) → Crop storage <em>Barn</em>!<br>2. Horse/cattle stall: <strong>Establo</strong> ≈ Direct sibling of English <strong>"Stable"</strong>! | <strong>Caballeriza</strong> ≈ From <strong>Caballo ("Cavalry" horse)</strong> → Horse stall / <em>Stable</em>!',
        "shortcutHi": '1. Grain crop storage: <strong>Godown</strong> ≈ Shared Indian word <strong>"Godown" (Tamil குடோன்)</strong> = Warehouse / Storage <em>Barn</em>! | <strong>Anaaj ghar</strong> ≈ <strong>Anaaj</strong> (Grain) + <strong>Ghar</strong> (House) = <em>Granary</em>!<br>2. Horse/cattle stall: <strong>Tabela</strong> ≈ Rhymes with English <strong>"S-table" (Tabela ≈ Stable)</strong> → Cattle & horse shed!',
    },
    1371: {
        "es": "1. Cultivated yield: Cultivo / cosecha | 2. Cereal kernel: Grano / cereal",
        "hi": "1. Cultivated yield: Fasal | 2. Cereal kernel: Anaaj / daana",
        "shortcutEs": '1. Cultivated yield: <strong>Cultivo</strong> ≈ From <strong>"Cultivate"</strong> → Field <em>Crop</em>! | <strong>Cosecha</strong> ≈ Think of collecting crops into <strong>Co-sacks ("Cosecha")</strong> = <em>Harvest / Yield</em>!<br>2. Cereal kernel: <strong>Grano</strong> ≈ Direct sibling of English <strong>"Grain"</strong>! | <strong>Cereal</strong> ≈ 100% identical to English <strong>"Cereal"</strong>!',
        "shortcutHi": '1. Cultivated yield: <strong>Fasal</strong> ≈ <strong>Tamil பசலி (Pasali / Fasli = Harvest season!)</strong> → Ready farm <em>Crop / Harvest</em>!<br>2. Cereal kernel: <strong>Anaaj</strong> ≈ Sounds like <strong>"All-Nourish"</strong> wheat & rice = <em>Food Grain</em>! | <strong>Daana</strong> ≈ Same Tamil word <strong>தானியம் (Dhaanyam / Daana = single seed/kernel!)</strong>!',
    },
    1372: {
        "es": "1. Grassland range: Pastizal / prado | 2. Verb - eat grass: Pastar",
        "hi": "1. Grassland range: Ghaas ka maidaan | 2. Verb - eat grass: Charna / ghaas khaana",
        "shortcutEs": '1. Grassland range: <strong>Pastizal</strong> ≈ Direct sibling of English <strong>"Pasture"</strong> (wide grassy land)! | <strong>Prado</strong> ≈ Famous lush green <strong>"Prado"</strong> park / prairie = <em>Meadow / Pasture</em>!<br>2. Verb - eat grass: <strong>Pastar</strong> ≈ Action of eating in a <strong>Pasture (Pastar)</strong> = To <em>Graze</em>!',
        "shortcutHi": '1. Grassland range: <strong>Ghaas ka maidaan</strong> ≈ <strong>Ghaas ("Grass")</strong> + <strong>Maidaan (Tamil மைதானம் = Open ground!)</strong> → Grass field = <em>Pasture</em>!<br>2. Verb - eat grass: <strong>Charna</strong> ≈ Sounds like cattle <strong>"Churning / Chewing"</strong> grass = <em>Graze</em>! | <strong>Ghaas khaana</strong> ≈ Literally "to eat grass"!',
    },
    1373: {
        "es": "1. Farm beasts: Ganado / reses | 2. Group pack cluster: Rebaño / manada",
        "hi": "1. Farm beasts: Gay-bhains / jaanwar | 2. Group pack cluster: Jhund",
        "shortcutEs": '1. Farm beasts: <strong>Ganado</strong> ≈ From <strong>Ganar (Farm wealth/gains)</strong> → Farm cattle = <em>Livestock</em>! | <strong>Reses</strong> ≈ Plural of <strong>Res</strong> (head of cattle / beast)!<br>2. Group pack cluster: <strong>Rebaño</strong> ≈ Sheep gathered into a farm flock = <em>Flock / Herd</em>! | <strong>Manada</strong> ≈ Sounds like <strong>"Many-Animals"</strong> running together = <em>Herd / Pack</em>!',
        "shortcutHi": '1. Farm beasts: <strong>Gay-bhains</strong> ≈ Literally <strong>"Cow (Gaay) & Buffalo (Bhains)"</strong> → Everyday Hindi way to mean farm <em>Cattle / Livestock</em>! | <strong>Jaanwar</strong> ≈ <strong>Jaan (Tamil ஜீவன் = Life)</strong> = Animals!<br>2. Group pack cluster: <strong>Jhund</strong> ≈ Sounds like <strong>"Joined-Group"</strong> moving together = <em>Herd / Flock</em>!',
    },
    1374: {
        "es": "1. Soil compost: Fertilizante / abono | 2. Bug spray chemical: Pesticida / plaguicida",
        "hi": "1. Soil compost: Khaad | 2. Bug spray chemical: Keede maarne ki dawai / pesticide",
        "shortcutEs": '1. Soil compost: <strong>Fertilizante</strong> ≈ Direct sibling of <strong>"Fertilizer"</strong>! | <strong>Abono</strong> ≈ Gives plants a <strong>"Bonus" (Abono)</strong> of nutrients = <em>Manure / Fertilizer</em>!<br>2. Bug spray chemical: <strong>Pesticida</strong> ≈ Direct match with <strong>"Pesticide"</strong>! | <strong>Plaguicida</strong> ≈ Kills crop <strong>Plagues (Plagu-icida)</strong> = Bug killer!',
        "shortcutHi": '1. Soil compost: <strong>Khaad</strong> ≈ Plant <strong>"Food (Khaana)"</strong> mixed into soil = <em>Manure / Fertilizer</em>!<br>2. Bug spray chemical: <strong>Keede maarne ki dawai</strong> ≈ <strong>Keede</strong> (Bugs) + <strong>Maarne ki dawai</strong> (Killing medicine) = Bug spray! | <strong>Pesticide</strong> ≈ Same everyday English word used directly!',
    },
    1375: {
        "es": "Riego",
        "hi": "Khet mein paani dena",
        "shortcutEs": '<strong>Riego</strong> ≈ Sounds like <strong>"Rain-Go"</strong> through channels to crops → Watering fields = <em>Irrigation</em>!',
        "shortcutHi": '<strong>Khet mein paani dena</strong> ≈ <strong>Khet mein</strong> (In the crop field) + <strong>Paani dena</strong> (Give water) → Watering crops = <em>Irrigation</em>!',
    },
    1376: {
        "es": "Heno / paja",
        "hi": "Ghaas-phoos / sookhi ghaas / bhoosa",
        "shortcutEs": '<strong>Heno</strong> ≈ Sounds right like English <strong>"Hay-Now" (Heno ≈ Hay)</strong> → Dried grass for horses! | <strong>Paja</strong> ≈ Sounds like dry <strong>"Pack-Straw"</strong> stalks → <em>Straw</em>!',
        "shortcutHi": '<strong>Ghaas-phoos</strong> ≈ <strong>Ghaas</strong> (Grass) + <strong>Phoos</strong> (Dry twigs)! | <strong>Sookhi ghaas</strong> ≈ <strong>Sookhi (Dry — Tamil சுக்கு)</strong> + <strong>Ghaas (Grass)</strong>! | <strong>Bhoosa</strong> ≈ Dry golden chaff / fodder = <em>Hay / Straw (Bhoosa)</em>!',
    },
    1377: {
        "es": "Oxidado",
        "hi": "Zang laga hua / morcha laga",
        "shortcutEs": '<strong>Oxidado</strong> ≈ Direct sibling of English <strong>"Oxidized"</strong> (iron + oxygen = orange rust!) → <em>Rusty</em>!',
        "shortcutHi": '<strong>Zang laga hua</strong> ≈ <strong>Zang</strong> (Iron rust — "Clang of old iron!") + <strong>Laga hua</strong> (Covered with) = <em>Rusty</em>! | <strong>Morcha laga</strong> ≈ Weather-beaten rust eating iron (used across North India alongside <em>Zang</em>)!',
    },
    1378: {
        "es": "1. Grit powdered: Polvoriento | 2. Mired in sludge: Embarrado / lodoso | 3. Grit dunes: Arenoso",
        "hi": "1. Grit powdered: Dhool-bhara | 2. Mired in sludge: Keechad-bhara | 3. Grit dunes: Reetila",
        "shortcutEs": '1. Grit powdered: <strong>Polvoriento</strong> ≈ From <strong>Polvo ("Powder" / dust)</strong> → Covered in dust = <em>Dusty</em>!<br>2. Mired in sludge: <strong>Embarrado</strong> ≈ From <strong>Barro ("Wheel-Barrow" mud)</strong>! | <strong>Lodoso</strong> ≈ From <strong>Lodo</strong> (Sludge/slush) → <em>Muddy</em>!<br>3. Grit dunes: <strong>Arenoso</strong> ≈ From <strong>Arena (Gladiator "Arena" sand)</strong> → Gritty and <em>Sandy</em>!',
        "shortcutHi": '1. Grit powdered: <strong>Dhool-bhara</strong> ≈ <strong>Dhool (Tamil தூள் = Dust/Powder!)</strong> + <strong>Bhara (Filled with)</strong> = <em>Dusty</em>!<br>2. Mired in sludge: <strong>Keechad-bhara</strong> ≈ <strong>Keechad</strong> (Squishy mud) + <strong>Bhara</strong> (Full of) = <em>Muddy</em>!<br>3. Grit dunes: <strong>Reetila</strong> ≈ From <strong>Ret (Sand)</strong> → Full of sand dunes = <em>Sandy</em>!',
    },
    1379: {
        "es": "Rígido / tieso",
        "hi": "Sakht / akda hua",
        "shortcutEs": '<strong>Rígido</strong> ≈ Direct sibling of English <strong>"Rigid"</strong>! | <strong>Tieso</strong> ≈ Sounds like <strong>"Tight-So"</strong> / Taut & Tense → Frozen stiff as a board = <em>Stiff (Tieso)</em>!',
        "shortcutHi": '<strong>Sakht</strong> ≈ Hard / Strict / Unbending! | <strong>Akda hua</strong> ≈ Frozen stiff & stubborn (<em>Akad</em> = Stiffness) → Can’t bend a muscle = <em>Stiff</em>!',
    },
    1380: {
        "es": "Flexible / elástico",
        "hi": "Lacheela",
        "shortcutEs": '<strong>Flexible</strong> ≈ Direct sibling of English <strong>"Flexible"</strong>! | <strong>Elástico</strong> ≈ Direct sibling of English <strong>"Elastic"</strong>!',
        "shortcutHi": '<strong>Lacheela</strong> ≈ From <strong>Lachak (Sway/Bend easily)</strong> → Like rubber or a dancer bending effortlessly = <em>Flexible / Elastic</em>!',
    },
    1381: {
        "es": "Frágil / delicado",
        "hi": "Naazuk / jaldi tootne wala",
        "shortcutEs": '<strong>Frágil</strong> ≈ Direct sibling of English <strong>"Fragile"</strong>! | <strong>Delicado</strong> ≈ Direct sibling of English <strong>"Delicate"</strong>!',
        "shortcutHi": '<strong>Naazuk</strong> ≈ Classic Hindi/Urdu word <strong>"Naazuk"</strong> (delicate flower petal)! | <strong>Jaldi tootne wala</strong> ≈ <strong>Jaldi</strong> (Quickly) + <strong>Tootne wala</strong> (That breaks) = Easily broken / <em>Fragile</em>!',
    },
    1382: {
        "es": "Robusto / resistente / duradero",
        "hi": "Mazboot / tikau / thos",
        "shortcutEs": '<strong>Robusto</strong> ≈ <strong>"Robust"</strong>! | <strong>Resistente</strong> ≈ <strong>"Resistant"</strong> (resists breaking)! | <strong>Duradero</strong> ≈ <strong>"Durable"</strong> (endures for years)!',
        "shortcutHi": '<strong>Mazboot</strong> ≈ Strong & solid! | <strong>Tikau</strong> ≈ From <strong>Tikna (Last long!)</strong> = <em>Durable</em>! | <strong>Thos</strong> ≈ Dense, solid & unyielding = <em>Sturdy / Solid (Thos)</em>!',
    },
    1383: {
        "es": "Empapado / chorreando",
        "hi": "Tar-batar / bheega hua",
        "shortcutEs": '<strong>Empapado</strong> ≈ Sounds like <strong>"In-Puddle-Popped"</strong> → Completely <em>Soaked</em>! | <strong>Chorreando</strong> ≈ Water <strong>"Pouring/Streaming"</strong> in droplets → <em>Dripping Wet</em>!',
        "shortcutHi": '<strong>Tar-batar</strong> ≈ Sounds like <strong>"Tears-And-Water"</strong> soaking clothes head-to-toe = <em>Drenched</em>! | <strong>Bheega hua</strong> ≈ From <strong>Bheegna (Get wet in rain)</strong> = <em>Soaked</em>!',
    },
    1384: {
        "es": "1. Sun searing heat: Abrasador / sofocante | 2. Bubbling liquid temp: Hirviendo",
        "hi": "1. Sun searing heat: Tez garmi | 2. Bubbling liquid temp: Ubalta hua / khaulta hua",
        "shortcutEs": '1. Sun searing heat: <strong>Abrasador</strong> ≈ <strong>"Brazier"</strong> (burning coals) → Blistering <em>Scorching</em> heat! | <strong>Sofocante</strong> ≈ <strong>"Suffocating"</strong> summer heat!<br>2. Bubbling liquid temp: <strong>Hirviendo</strong> ≈ Sounds like <strong>"Hear-Venting"</strong> kettle steam → <em>Boiling</em>!',
        "shortcutHi": '1. Sun searing heat: <strong>Tez garmi</strong> ≈ <strong>Tez</strong> (Intense/Sharp) + <strong>Garmi</strong> ("Warm/Grilling" heat) = <em>Scorching Heat</em>!<br>2. Bubbling liquid temp: <strong>Ubalta hua</strong> ≈ From <strong>Ubalna ("Boil")</strong>! | <strong>Khaulta hua</strong> ≈ Rolling, furious <em>Boiling</em> water in a pot!',
    },
    1385: {
        "es": "Helado / congelado",
        "hi": "Baraf jaisa thanda",
        "shortcutEs": '<strong>Helado</strong> ≈ Sounds like <strong>"Hail-Iced"</strong> → Ice-cold / Ice cream = <em>Freezing</em>! | <strong>Congelado</strong> ≈ Direct sibling of English <strong>"Congealed / Frozen"</strong>!',
        "shortcutHi": '<strong>Baraf jaisa thanda</strong> ≈ <strong>Baraf</strong> (Ice — "Brrr!") + <strong>Jaisa</strong> (Like) + <strong>Thanda</strong> (Cold) → Cold like ice = <em>Freezing</em>!',
    },
    1386: {
        "es": "Tibio / templado",
        "hi": "Gunguna / halka garam",
        "shortcutEs": '<strong>Tibio</strong> ≈ Direct cousin of English <strong>"Tepid"</strong> (tepid water = <em>Lukewarm</em>)! | <strong>Templado</strong> ≈ Direct sibling of <strong>"Temperate"</strong> (mild, gentle warmth)!',
        "shortcutHi": '<strong>Gunguna</strong> ≈ Soft humming <strong>"Gun-Gun"</strong> warmth — neither burning hot nor cold = <em>Lukewarm water</em>! | <strong>Halka garam</strong> ≈ <strong>Halka</strong> (Light/Mild) + <strong>Garam</strong> (Warm)!',
    },
    1387: {
        "es": "1. Water-repelling: Impermeable | 2. Hermetic seal: Hermético",
        "hi": "1. Water-repelling: Waterproof | 2. Hermetic seal: Hawa-band / airtight",
        "shortcutEs": '1. Water-repelling: <strong>Impermeable</strong> ≈ Literally English <strong>"Impermeable"</strong> (rain jacket that water can’t soak through = <em>Waterproof</em>)!<br>2. Hermetic seal: <strong>Hermético</strong> ≈ English <strong>"Hermetic"</strong> (vacuum-sealed lid = <em>Airtight</em>)!',
        "shortcutHi": '1. Water-repelling: <strong>Waterproof</strong> ≈ Used directly in everyday Hindi (watches, jackets, bags)!<br>2. Hermetic seal: <strong>Hawa-band</strong> ≈ <strong>Hawa (Air)</strong> + <strong>Band (Tamil பந்த் = Closed/Shut!)</strong> = <em>Airtight</em>! | <strong>Airtight</strong> ≈ Used directly for kitchen containers!',
    },
    1388: {
        "es": "1. Ignites easily: Inflamable | 2. Toxic venom: Venenoso / tóxico",
        "hi": "1. Ignites easily: Aag pakadne wala | 2. Toxic venom: Zehreela / jaanleva",
        "shortcutEs": '1. Ignites easily: <strong>Inflamable</strong> ≈ Literally <strong>"Inflammable / Flammable"</strong> (catches fire fast)!<br>2. Toxic venom: <strong>Venenoso</strong> ≈ Contains <strong>"Venom"</strong>! | <strong>Tóxico</strong> ≈ Direct sibling of <strong>"Toxic"</strong> = <em>Poisonous</em>!',
        "shortcutHi": '1. Ignites easily: <strong>Aag pakadne wala</strong> ≈ <strong>Aag (Agni = Fire)</strong> + <strong>Pakadne wala (Catcher)</strong> = Easily catches fire = <em>Flammable</em>!<br>2. Toxic venom: <strong>Zehreela</strong> ≈ From <strong>Zeher (Poison)</strong>! | <strong>Jaanleva</strong> ≈ <strong>Jaan (Tamil ஜீவன் = Life) + Leva (Taker)</strong> = Fatal / Deadly <em>Toxic</em>!',
    },
    1389: {
        "es": "Tenue / débil / borroso",
        "hi": "Dheema / halka",
        "shortcutEs": '<strong>Tenue</strong> ≈ <strong>"Tenuous"</strong> (thin/faint)! | <strong>Débil</strong> ≈ <strong>"Debilitated / Feeble"</strong> (weak bulb)! | <strong>Borroso</strong> ≈ Sounds like <strong>"Blurred-Out"</strong> (faint & blurry)!',
        "shortcutHi": '<strong>Dheema</strong> ≈ Slow, soft, or turned-down light/voice = <em>Dim / Faint</em>! | <strong>Halka</strong> ≈ Light/mild (<em>Halki roshni</em> = <em>Dim light</em>)!',
    },
    1390: {
        "es": "Sabor / gusto",
        "hi": "Swaad / zaika",
        "shortcutEs": '<strong>Sabor</strong> ≈ Direct sibling of English <strong>"Savor / Savory"</strong> → Rich food <em>Flavor</em>! | <strong>Gusto</strong> ≈ English <strong>"Gusto"</strong> (relish/taste)!',
        "shortcutHi": '<strong>Swaad</strong> ≈ 100% cousin of <strong>Tamil சுவை (Suvai = Taste/Flavor!)</strong>! | <strong>Zaika</strong> ≈ Rich restaurant spice flavor & aroma = <em>Flavor / Palate (Zaika)</em>!',
    },
    1391: {
        "es": "Aroma / fragancia",
        "hi": "Khushboo / mehek",
        "shortcutEs": '<strong>Aroma</strong> ≈ Identical to English <strong>"Aroma"</strong>! | <strong>Fragancia</strong> ≈ Direct sibling of English <strong>"Fragrance"</strong>!',
        "shortcutHi": '<strong>Khushboo</strong> ≈ <strong>Khush</strong> (Happy) + <strong>Boo</strong> (Scent) = Pleasant sweet smell! | <strong>Mehek</strong> ≈ Sweet lingering perfume or flower scent wafting through a room = <em>Fragrance (Mehek)</em>!',
    },
    1392: {
        "es": "1. Wood smoke charred: Ahumado | 2. Salty umami zest: Salado / sabroso",
        "hi": "1. Wood smoke charred: Dhuein wala / smoky | 2. Salty umami zest: Chatpata / namkeen / mazedaar",
        "shortcutEs": '1. Wood smoke charred: <strong>Ahumado</strong> ≈ From <strong>Humo ("Fume" / Smoke)</strong> → Wood-fired <em>Smoky</em> taste!<br>2. Salty umami zest: <strong>Salado</strong> ≈ From <strong>Sal ("Salt")</strong> = <em>Salty</em>! | <strong>Sabroso</strong> ≈ From <strong>Sabor ("Savor")</strong> = Tasty & <em>Savory</em>!',
        "shortcutHi": '1. Wood smoke charred: <strong>Dhuein wala</strong> ≈ From <strong>Dhuan (Smoke)</strong> → Smokehouse <em>Smoky</em> flavor! | <strong>Smoky</strong> ≈ Used directly on café/tandoor menus!<br>2. Salty umami zest: <strong>Chatpata</strong> ≈ Lip-smacking chaat tang! | <strong>Namkeen</strong> ≈ From <strong>Namak (Salt)</strong>! | <strong>Mazedaar</strong> ≈ <strong>Tamil மஜா (Majaa = Tasty fun!)</strong>!',
    },
    1393: {
        "es": "Rico / sabroso / delicioso",
        "hi": "Swadisht / lazeez / mazedaar",
        "shortcutEs": '<strong>Rico</strong> ≈ <strong>"Rich"</strong> (rich in flavor = yummy)! | <strong>Sabroso</strong> ≈ Full of <strong>Sabor ("Savor")</strong>! | <strong>Delicioso</strong> ≈ Direct sibling of English <strong>"Delicious"</strong>!',
        "shortcutHi": '<strong>Swadisht</strong> ≈ From <strong>Swaad (Tamil சுவை = Taste)</strong> = Full of taste! | <strong>Lazeez</strong> ≈ Sounds like <strong>"Luscious-Cheez"</strong> → Mouthwatering <em>Delicious</em>! | <strong>Mazedaar</strong> ≈ <strong>Tamil மஜா (Majaa = Fun/Delicious!)</strong>!',
    },
    1394: {
        "es": "Soso / desabrido",
        "hi": "Pheeka / be-swaad",
        "shortcutEs": '<strong>Soso</strong> ≈ Sounds like <strong>"So-So"</strong> (meh, zero spice = <em>Bland</em>)! | <strong>Desabrido</strong> ≈ <strong>Des- (Zero) + Sabor (Flavor)</strong> = Literally <em>Tasteless</em>!',
        "shortcutHi": '<strong>Pheeka</strong> ≈ Sounds like <strong>"Weak-Flavor"</strong> (no salt or sugar) = <em>Bland</em>! | <strong>Be-swaad</strong> ≈ <strong>Be- (Without) + Swaad (Tamil சுவை = Taste)</strong> = <em>Tasteless</em>!',
    },
    1395: {
        "es": "1. Cooking formula: Receta (de cocina) | 2. Component item: Ingrediente",
        "hi": "1. Cooking formula: Recipe / banane ka tareeka | 2. Component item: Saamagri / cheez",
        "shortcutEs": '1. Cooking formula: <strong>Receta (de cocina)</strong> ≈ Cognate of English <strong>"Receipt / Recipe"</strong> → Kitchen cooking guide!<br>2. Component item: <strong>Ingrediente</strong> ≈ Direct sibling of English <strong>"Ingredient"</strong>!',
        "shortcutHi": '1. Cooking formula: <strong>Recipe</strong> ≈ Everyday English kitchen term! | <strong>Banane ka tareeka</strong> ≈ <strong>Banane</strong> (Making) + <strong>Tareeka (Way/Method)</strong> = How-to steps!<br>2. Component item: <strong>Saamagri</strong> ≈ Identical to <strong>Tamil சாமக்ரியை / சாமான் (Saamaan = Cooking items!)</strong>! | <strong>Cheez</strong> ≈ Everyday "thing / item"!',
    },
    1396: {
        "es": "Aperitivo / entrada / botana",
        "hi": "Starter / shuruat ka khana",
        "shortcutEs": '<strong>Aperitivo</strong> ≈ <strong>"Aperitif / Appetizer"</strong>! | <strong>Entrada</strong> ≈ <strong>"Entrance / Entrée"</strong> (first plate entering the table)! | <strong>Botana</strong> ≈ Mexican Spanish word for bar <em>Snacks / Starters</em>!',
        "shortcutHi": '<strong>Starter</strong> ≈ Used universally in Indian restaurants! | <strong>Shuruat ka khana</strong> ≈ <strong>Shuruat (Beginning — Tamil சுரு = Start!)</strong> + <strong>Khana (Food)</strong> = Opening course!',
    },
    1397: {
        "es": "Banquete / festín",
        "hi": "Daawat / party",
        "shortcutEs": '<strong>Banquete</strong> ≈ Direct sibling of English <strong>"Banquet"</strong>! | <strong>Festín</strong> ≈ Contains English <strong>"Feast" (Fest-ín)</strong> → Grand celebration meal!',
        "shortcutHi": '<strong>Daawat</strong> ≈ Classic <strong>"Daawat-e-Khaas"</strong> = Royal invitation feast! | <strong>Party</strong> ≈ Everyday English word used in spoken Hindi for celebratory meals!',
    },
    1398: {
        "es": "Porción / ración",
        "hi": "Hissa / plate",
        "shortcutEs": '<strong>Porción</strong> ≈ Direct sibling of English <strong>"Portion"</strong>! | <strong>Ración</strong> ≈ Direct sibling of English <strong>"Ration"</strong> → Fixed <em>Serving size</em>!',
        "shortcutHi": '<strong>Hissa</strong> ≈ Share / Cut portion (<strong>Spoken Tamil ஹிஸ்ஸா</strong>)! | <strong>Plate</strong> ≈ Everyday diner phrase ("Ek <em>plate</em> laga do" = one <em>Serving</em>)!',
    },
    1399: {
        "es": "1. Clear boiled stock: Caldo | 2. Thickened sauce stew: Salsa / jugo",
        "hi": "1. Clear boiled stock: Shorba / soup | 2. Thickened sauce stew: Gravy / tari",
        "shortcutEs": '1. Clear boiled stock: <strong>Caldo</strong> ≈ Think of a simmering <strong>"Cauldron"</strong> of clear hot <em>Broth</em>!<br>2. Thickened sauce stew: <strong>Salsa</strong> ≈ Used in English <strong>"Salsa" (Sauce)</strong>! | <strong>Jugo</strong> ≈ Sibling of English <strong>"Juice"</strong> (meat juices / <em>Gravy</em>)!',
        "shortcutHi": '1. Clear boiled stock: <strong>Shorba</strong> ≈ Sounds like <strong>"Slurp-Ah!"</strong> sipping a hot bowl of <em>Broth</em>! | <strong>Soup</strong> ≈ Direct restaurant word!<br>2. Thickened sauce stew: <strong>Gravy</strong> ≈ Universal restaurant curry term! | <strong>Tari</strong> ≈ Rich oily spiced curry sauce = <em>Tari (Gravy)</em>!',
    },
    1400: {
        "es": "Recortar / despuntar",
        "hi": "Katarna / kaatna",
        "shortcutEs": '<strong>Recortar</strong> ≈ <strong>Re- + Cortar ("Cut")</strong> → Snip edges neatly to <em>Trim</em>! | <strong>Despuntar</strong> ≈ <strong>Des- (Off) + Punta (Tips/Points)</strong> → Clip off split ends / tips!',
        "shortcutHi": '<strong>Katarna</strong> ≈ <strong>Tamil கத்தரி (Katthari = Scissors!)</strong> → Snipping hair/hedges with scissors = <em>Trim / Clip</em>! | <strong>Kaatna</strong> ≈ Sounds like English <strong>"Cut!"</strong>!',
    },
    1401: {
        "es": "1. Brush clean hard: Fregar / restregar | 2. Rub shine luster: Pulir / lustrar",
        "hi": "1. Brush clean hard: Ragad kar dhona / ghisna | 2. Rub shine luster: Chamkana / polish karna",
        "shortcutEs": '1. Brush clean hard: <strong>Fregar / restregar</strong> ≈ Sounds like <strong>"Friction-Rub"</strong> → Heavy scrubbing of pots & floors!<br>2. Rub shine luster: <strong>Pulir</strong> ≈ Sibling of English <strong>"Polish"</strong>! | <strong>Lustrar</strong> ≈ Direct sibling of English <strong>"Luster"</strong> (mirror shine)!',
        "shortcutHi": '1. Brush clean hard: <strong>Ragad kar dhona / ghisna</strong> ≈ Rubbing hard (<strong>Ragadna / Ghisna</strong> — Tamil உராய்) to wash clean (<strong>Dhona</strong>) = <em>Scrub</em>!<br>2. Rub shine luster: <strong>Chamkana</strong> ≈ From <strong>Chamak (Sparkle/Glitter)</strong> = Make it shine! | <strong>Polish karna</strong> ≈ Everyday shoe/car shine term!',
    },
    1402: {
        "es": "Remojar / empapar",
        "hi": "Bhigona / paani mein daalna",
        "shortcutEs": '<strong>Remojar</strong> ≈ Think <strong>"Remain-In-Jar"</strong> of water (soaking beans/rice overnight)! | <strong>Empapar</strong> ≈ <strong>"In-Puddle"</strong> → Saturate through and through = <em>Soak</em>!',
        "shortcutHi": '<strong>Bhigona</strong> ≈ From <strong>Bheega (Wet)</strong> → Submerge to <em>Soak</em>! | <strong>Paani mein daalna</strong> ≈ <strong>Paani (Water) + Mein daalna (Put inside)</strong>!',
    },
    1403: {
        "es": "1. Place inside: Insertar / meter | 2. Pull out: Extraer / sacar",
        "hi": "1. Place inside: Daalna / andar ghusana | 2. Pull out: Nikaalna / kheench kar nikaalna",
        "shortcutEs": '1. Place inside: <strong>Insertar</strong> ≈ English <strong>"Insert"</strong>! | <strong>Meter</strong> ≈ Think <strong>"Put into a Meter slot"</strong> → Slide coins/keys inside!<br>2. Pull out: <strong>Extraer</strong> ≈ English <strong>"Extract"</strong>! | <strong>Sacar</strong> ≈ Think <strong>"Yanked out of a Sack"</strong> → Pull/take out!',
        "shortcutHi": '1. Place inside: <strong>Daalna</strong> ≈ Sounds like <strong>"Drop-In"</strong>! | <strong>Andar ghusana</strong> ≈ <strong>Andar (Inside) + Ghusana (Push/Slip in)</strong>!<br>2. Pull out: <strong>Nikaalna</strong> ≈ Sounds like <strong>"Nick-Out"</strong> (pull/draw out)! | <strong>Kheench kar nikaalna</strong> ≈ <strong>Kheench kar (Pulling tight) + Nikaalna</strong> = Yank/<em>Extract</em> out!',
    },
    1404: {
        "es": "1. Diaphragm spasm: Hipo | 2. Stomach gas burp: Eructo / eructar",
        "hi": "1. Diaphragm spasm: Hichki | 2. Stomach gas burp: Dakaar / dakaar lena",
        "shortcutEs": '1. Diaphragm spasm: <strong>Hipo</strong> ≈ Sounds like a <strong>"Hippo"</strong> going <em>"Hic-Hipo!"</em> (Tamil இப்போ) = <em>Hiccup</em>!<br>2. Stomach gas burp: <strong>Eructo / eructar</strong> ≈ Medical <strong>"Eructation" / "Erupt-Air"</strong> = <em>Belch / Burp</em>!',
        "shortcutHi": '1. Diaphragm spasm: <strong>Hichki</strong> ≈ Sounds right like throat going <strong>"Hic-Key!"</strong> = <em>Hiccup</em>!<br>2. Stomach gas burp: <strong>Dakaar / dakaar lena</strong> ≈ Onomatopoeia <strong>"Daa-Kaar!"</strong> burp sound after a heavy meal = <em>Belch</em>!',
    },
    1405: {
        "es": "1. Tremble flutter: Temblar / estremecerse | 2. Wince back in fear: Encogerse / retroceder",
        "hi": "1. Tremble flutter: Thartharana / kaampna | 2. Wince back in fear: Jhijhakna / peeche hatna",
        "shortcutEs": '1. Tremble flutter: <strong>Temblar</strong> ≈ Sibling of English <strong>"Tremble"</strong>! | <strong>Estremecerse</strong> ≈ Contains <strong>"Tremor"</strong> → Sudden shiver/shudder!<br>2. Wince back in fear: <strong>Encogerse</strong> ≈ Shrink into a coil/shell! | <strong>Retroceder</strong> ≈ <strong>"Retro-cede"</strong> (pull/step back in shock = <em>Flinch</em>)!',
        "shortcutHi": '1. Tremble flutter: <strong>Thartharana</strong> ≈ Sound of teeth going <strong>"Thar-Thar"</strong>! | <strong>Kaampna</strong> ≈ Same root as <strong>Tamil கம்பம் / நடுக்கம் (Kampam = Shake/Quake!)</strong>!<br>2. Wince back in fear: <strong>Jhijhakna</strong> ≈ Startled <strong>"Jhi-Jhak"</strong> hesitation! | <strong>Peeche hatna</strong> ≈ <strong>Peeche (Back) + Hatna (Step away)</strong> = Recoil / <em>Flinch</em>!',
    },
    1406: {
        "es": "1. Prickle sensation: Picor / comezón | 2. Verb - scratch: Rascar / picar",
        "hi": "1. Prickle sensation: Khujli | 2. Verb - scratch: Khujana / khujli karna",
        "shortcutEs": '1. Prickle sensation: <strong>Picor</strong> ≈ Skin pricking! | <strong>Comezón</strong> ≈ Tickling rash craving a scratch = <em>Itch</em>!<br>2. Verb - scratch: <strong>Rascar</strong> ≈ Sounds like nails going <strong>"Rasp-Scratch"</strong>! | <strong>Picar</strong> ≈ Sounds like <strong>"Pick-At-Bite"</strong> → Mosquito sting itching!',
        "shortcutHi": '1. Prickle sensation: <strong>Khujli</strong> ≈ Sounds like frantic <strong>"Khuja-Khuja"</strong> skin tickle = <em>Itch</em>!<br>2. Verb - scratch: <strong>Khujana / khujli karna</strong> ≈ Verb action of scratching that itch!',
    },
    1407: {
        "es": "Entumecido / dormido",
        "hi": "Sunn",
        "shortcutEs": '<strong>Entumecido</strong> ≈ Contains <strong>"Tumid / Tingly-Numb"</strong> (deadened limb)! | <strong>Dormido</strong> ≈ Literally <strong>"Asleep / Dormant"</strong> ("mi pie está dormido" = my foot fell asleep/went <em>Numb</em>)!',
        "shortcutHi": '<strong>Sunn</strong> ≈ Same root as <strong>Tamil சூன்யம் (Soonyam = Zero feeling!)</strong> → Zero sensation = <em>Numb (Sunn)</em>!',
    },
    1408: {
        "es": "Calambre / espasmo / tirón",
        "hi": "Aithan / nas chadhna",
        "shortcutEs": '<strong>Calambre</strong> ≈ Sounds like <strong>"Clamp-Leg"</strong> (exact anagram feel of <em>Cramp</em>)! | <strong>Espasmo</strong> ≈ Sibling of English <strong>"Spasm"</strong>! | <strong>Tirón</strong> ≈ From <strong>Tirar (Pull)</strong> → Sudden muscle pull / twist!',
        "shortcutHi": '<strong>Aithan</strong> ≈ From <strong>Ainthna</strong> (Twisting/Wrenching tight like a knotted calf)! | <strong>Nas chadhna</strong> ≈ <strong>Nas (Nerve/Tendon — Tamil நரம்பு)</strong> + <strong>Chadhna (Climb/Lock up)</strong> = Muscle knot / <em>Cramp</em>!',
    },
    1409: {
        "es": "1. Fluid skin bubble: Ampolla | 2. Enlarged tissue: Hinchazón / inflamación",
        "hi": "1. Fluid skin bubble: Chhaala / phaphora | 2. Enlarged tissue: Soojan",
        "shortcutEs": '1. Fluid skin bubble: <strong>Ampolla</strong> ≈ Glass fluid <strong>"Ampoule"</strong> bubble on heel or burnt finger = <em>Blister</em>!<br>2. Enlarged tissue: <strong>Hinchazón</strong> ≈ Sounds like <strong>"Inch-High-Zone"</strong> (bump puffing out)! | <strong>Inflamación</strong> ≈ Sibling of <strong>"Inflammation"</strong>!',
        "shortcutHi": '1. Fluid skin bubble: <strong>Chhaala</strong> ≈ Sounds like <strong>"Chafed-Bubble"</strong> on foot or mouth ulcer! | <strong>Phaphora</strong> ≈ Puffed burn bubble full of fluid = <em>Blister</em>!<br>2. Enlarged tissue: <strong>Soojan</strong> ≈ Sounds like <strong>"Swollen-Zone" (Soojan ≈ Swollen)</strong> = <em>Swelling</em>!',
    },
    1410: {
        "es": "1. Gastric acid reflux: Acidez / ardor | 2. Dyspepsia upset: Indigestión / empacho",
        "hi": "1. Gastric acid reflux: Seene ki jalan / acidity | 2. Dyspepsia upset: Badhazmi / pait kharab",
        "shortcutEs": '1. Gastric acid reflux: <strong>Acidez</strong> ≈ English <strong>"Acidity"</strong>! | <strong>Ardor</strong> ≈ Direct sibling of English <strong>"Ardor / Ardent"</strong> (fiery chest burn = <em>Heartburn</em>)!<br>2. Dyspepsia upset: <strong>Indigestión</strong> ≈ English <strong>"Indigestion"</strong>! | <strong>Empacho</strong> ≈ Stuffed heavy belly ache after overeating!',
        "shortcutHi": '1. Gastric acid reflux: <strong>Seene ki jalan</strong> ≈ <strong>Seene (Chest) + ki Jalan (Burning fire)</strong> = Literally <em>Heartburn</em>! | <strong>Acidity</strong> ≈ Used daily in Indian clinics!<br>2. Dyspepsia upset: <strong>Badhazmi</strong> ≈ <strong>Bad (Bad) + Hazm (Digestion)</strong>! | <strong>Pait kharab</strong> ≈ <strong>Pait (Stomach) + Kharab (Upset/Spoiled)</strong>!',
    },
    1411: {
        "es": "1. Stuck hard bowel: Estreñimiento | 2. Loose watery runs: Diarrea / soltura",
        "hi": "1. Stuck hard bowel: Qabz | 2. Loose watery runs: Dast / loose motion",
        "shortcutEs": '1. Stuck hard bowel: <strong>Estreñimiento</strong> ≈ Contains <strong>"Strain" (Estreñi-)</strong> → Straining with a blocked bowel = <em>Constipation</em>!<br>2. Loose watery runs: <strong>Diarrea</strong> ≈ <strong>"Diarrhea"</strong>! | <strong>Soltura</strong> ≈ From <strong>Suelto ("Loose")</strong> → Loose stomach runs!',
        "shortcutHi": '1. Stuck hard bowel: <strong>Qabz</strong> ≈ Sounds like stomach <strong>"Cabs-Jammed"</strong> → Blocked digestion = <em>Constipation</em>!<br>2. Loose watery runs: <strong>Dast</strong> ≈ Sounds like <strong>"Dash-To-Toilet!"</strong>! | <strong>Loose motion</strong> ≈ Standard everyday Indian English phrase!',
    },
    1412: {
        "es": "1. Sleeplessness: Insomnio | 2. Heavy grogginess: Somnolencia / modorra",
        "hi": "1. Sleeplessness: Neend na aana | 2. Heavy grogginess: Oongh / neend ka aana",
        "shortcutEs": '1. Sleeplessness: <strong>Insomnio</strong> ≈ Direct sibling of English <strong>"Insomnia"</strong>!<br>2. Heavy grogginess: <strong>Somnolencia</strong> ≈ <strong>"Somnolence"</strong> (<em>Somno</em> = Sleep)! | <strong>Modorra</strong> ≈ Heavy post-lunch daze making eyes droop = <em>Drowsiness (Modorra)</em>!',
        "shortcutHi": '1. Sleeplessness: <strong>Neend na aana</strong> ≈ <strong>Neend (Sleep) + Na aana (Not coming)</strong> = Sleepless nights = <em>Insomnia</em>!<br>2. Heavy grogginess: <strong>Oongh</strong> ≈ Yawning <strong>"Oooo-ngh!"</strong> sound as head nods off! | <strong>Neend ka aana</strong> ≈ Sleepiness creeping over you!',
    },
    1413: {
        "es": "Cirugía / operación",
        "hi": "Operation",
        "shortcutEs": '<strong>Cirugía</strong> ≈ Direct sibling of English <strong>"Surgery" (Cirugía ≈ Surgery)</strong>! | <strong>Operación</strong> ≈ Direct sibling of English <strong>"Operation"</strong>!',
        "shortcutHi": '<strong>Operation</strong> ≈ Universal word in Indian hospitals ("Bypass <em>operation</em>" = <em>Surgery / Operation</em>)!',
    },
    1414: {
        "es": "1. Piston barrel: Jeringa | 2. Hollow steel point: Aguja",
        "hi": "1. Piston barrel: Injection / syringe | 2. Hollow steel point: Sui",
        "shortcutEs": '1. Piston barrel: <strong>Jeringa</strong> ≈ Sounds like English <strong>"Syringe" (Je-ring-a ≈ Syringe)</strong> → Nurse’s injection tube!<br>2. Hollow steel point: <strong>Aguja</strong> ≈ Cousin of English <strong>"Acute"</strong> (razor-sharp tip) = Sewing or medical <em>Needle</em>!',
        "shortcutHi": '1. Piston barrel: <strong>Injection / syringe</strong> ≈ Standard hospital words understood everywhere in India!<br>2. Hollow steel point: <strong>Sui</strong> ≈ Reverse the syllables of <strong>Tamil ஊசி (Oo-si ↔ Su-i!)</strong> = Exact match for <em>Needle</em>!',
    },
    1415: {
        "es": "Termómetro",
        "hi": "Thermometer",
        "shortcutEs": '<strong>Termómetro</strong> ≈ <strong>Termo ("Thermal" heat)</strong> + <strong>Metro ("Meter" measure)</strong> → Fever temperature gauge = <em>Thermometer</em>!',
        "shortcutHi": '<strong>Thermometer</strong> ≈ Same medical instrument name used directly in Hindi clinics & homes!',
    },
    1416: {
        "es": "Diagnóstico",
        "hi": "Jaanch / diagnosis",
        "shortcutEs": '<strong>Diagnóstico</strong> ≈ Direct sibling of English <strong>"Diagnosis / Diagnostic"</strong> → Doctor identifying the illness!',
        "shortcutHi": '<strong>Jaanch</strong> ≈ Sounds like <strong>"Judge-Check"</strong> → Lab test / medical checkup! | <strong>Diagnosis</strong> ≈ Used directly by doctors alongside <em>Jaanch</em>!',
    },
    1417: {
        "es": "1. Rehabilitation regimen: Terapia / tratamiento | 2. Clinical practitioner: Terapeuta",
        "hi": "1. Rehabilitation regimen: Therapy / ilaaj | 2. Clinical practitioner: Therapist",
        "shortcutEs": '1. Rehabilitation regimen: <strong>Terapia</strong> ≈ <strong>"Therapy"</strong>! | <strong>Tratamiento</strong> ≈ <strong>"Treatment"</strong>!<br>2. Clinical practitioner: <strong>Terapeuta</strong> ≈ Direct sibling of English <strong>"Therapist" (Tera-peuta)</strong>!',
        "shortcutHi": '1. Rehabilitation regimen: <strong>Therapy</strong> ≈ Used directly (physio-<em>therapy</em>)! | <strong>Ilaaj</strong> ≈ <strong>Spoken Tamil இலாஜ் / வைத்தியம்</strong> → Medical remedy & care!<br>2. Clinical practitioner: <strong>Therapist</strong> ≈ Everyday English title!',
    },
    1418: {
        "es": "1. Convalescence bounce back: Recuperación / restablecimiento | 2. Remedy disease: Cura / curar / sanar",
        "hi": "1. Convalescence bounce back: Theek hona / sudhaar aana | 2. Remedy disease: Theek hona / ilaaj",
        "shortcutEs": '1. Convalescence bounce back: <strong>Recuperación</strong> ≈ <strong>"Recuperation"</strong>! | <strong>Restablecimiento</strong> ≈ <strong>Re-establish</strong> your strength again!<br>2. Remedy disease: <strong>Cura / curar</strong> ≈ <strong>"Cure"</strong>! | <strong>Sanar</strong> ≈ Root of <strong>"Sanitary / Sane"</strong> = Heal & restore health!',
        "shortcutHi": '1. Convalescence bounce back: <strong>Theek hona</strong> ≈ Getting <em>Well (Theek)</em>! | <strong>Sudhaar aana</strong> ≈ Health <em>Improvement (Sudhaar)</em>!<br>2. Remedy disease: <strong>Theek hona</strong> ≈ Getting cured! | <strong>Ilaaj</strong> ≈ <strong>Spoken Tamil இலாஜ்</strong> = Treatment / Remedy!',
    },
    1419: {
        "es": "1. Doctor's drug slip: Receta médica | 2. Quantity taken: Dosis",
        "hi": "1. Doctor's drug slip: Dawai ki parchi / prescription | 2. Quantity taken: Khuraak / dose",
        "shortcutEs": '1. Doctor’s drug slip: <strong>Receta médica</strong> ≈ Medical <strong>"Recipe"</strong> (<em>Médica</em>) written by a doctor = <em>Prescription</em>!<br>2. Quantity taken: <strong>Dosis</strong> ≈ Direct sibling of English <strong>"Dose"</strong>!',
        "shortcutHi": '1. Doctor’s drug slip: <strong>Dawai ki parchi</strong> ≈ <strong>Dawai (Medicine)</strong> + <strong>Parchi (Paper slip — "Parchment"!)</strong>! | <strong>Prescription</strong> ≈ Pharmacy standard term!<br>2. Quantity taken: <strong>Khuraak</strong> ≈ Sounds like <strong>"Cure-Rack"</strong> daily ration = Medicine <em>Dose</em>! | <strong>Dose</strong> ≈ Spoken daily ("Subah ki <em>dose</em>")!',
    },
    1420: {
        "es": "1. Bacteria killer: Antibiótico | 2. Pain relief pill: Analgésico / calmante",
        "hi": "1. Bacteria killer: Antibiotic | 2. Pain relief pill: Dard ki goli / painkiller",
        "shortcutEs": '1. Bacteria killer: <strong>Antibiótico</strong> ≈ Direct sibling of English <strong>"Antibiotic"</strong>!<br>2. Pain relief pill: <strong>Analgésico</strong> ≈ Medical English <strong>"Analgesic"</strong>! | <strong>Calmante</strong> ≈ <strong>"Calming"</strong> pain-soother = <em>Painkiller</em>!',
        "shortcutHi": '1. Bacteria killer: <strong>Antibiotic</strong> ≈ Direct pharmacy word in daily Hindi!<br>2. Pain relief pill: <strong>Dard ki goli</strong> ≈ <strong>Dard (Pain) + ki Goli (Round pill/tablet)</strong>! | <strong>Painkiller</strong> ≈ Spoken everywhere in India!',
    },
    1421: {
        "es": "Vacuna",
        "hi": "Teeka / vaccine",
        "shortcutEs": '<strong>Vacuna</strong> ≈ Direct sibling of English <strong>"Vaccine"</strong> (from Latin <em>vacca</em> cowpox!) → Immunity shot = <em>Vaccine</em>!',
        "shortcutHi": '<strong>Teeka</strong> ≈ Putting a protective dot/mark (<em>Teeka</em> — Tamil திலகம் / பொட்டு!) on a baby’s arm = <em>Vaccine shot</em>! | <strong>Vaccine</strong> ≈ Everyday spoken Hindi!',
    },
    1422: {
        "es": "1. Medical van: Ambulancia | 2. Litter carrying bed: Camilla",
        "hi": "1. Medical van: Ambulance | 2. Litter carrying bed: Stretcher",
        "shortcutEs": '1. Medical van: <strong>Ambulancia</strong> ≈ Direct sibling of English <strong>"Ambulance"</strong>!<br>2. Litter carrying bed: <strong>Camilla</strong> ≈ From <strong>Cama (Bed) + -illa (Small rolling bed)</strong> → Rolling ER bed = <em>Stretcher</em>!',
        "shortcutHi": '1. Medical van: <strong>Ambulance</strong> ≈ Universal hospital van word!<br>2. Litter carrying bed: <strong>Stretcher</strong> ≈ Universal hospital emergency bed word!',
    },
    1423: {
        "es": "1. Rolling chair: Silla de ruedas | 2. Underarm support: Muleta",
        "hi": "1. Rolling chair: Wheelchair | 2. Underarm support: Baisakhi",
        "shortcutEs": '1. Rolling chair: <strong>Silla de ruedas</strong> ≈ <strong>Silla</strong> (Chair) + <strong>de Ruedas</strong> (of Wheels — "Roll-das") = Literally <em>Wheelchair</em>!<br>2. Underarm support: <strong>Muleta</strong> ≈ Sounds like <strong>"Move-Leg-a"</strong> → Support stick for an injured leg = <em>Crutch</em>!',
        "shortcutHi": '1. Rolling chair: <strong>Wheelchair</strong> ≈ Standard everyday hospital word!<br>2. Underarm support: <strong>Baisakhi</strong> ≈ Sounds like <strong>"By-Side-Key"</strong> (two sticks leaning by your two sides/arms — <em>Bai-saakhi</em> = twin limb support) = <em>Crutch</em>!',
    },
    1424: {
        "es": "1. Of the mind: Mental / psíquico | 2. Brainpower reasoning: Intelecto / entendimiento",
        "hi": "1. Of the mind: Dimaagi | 2. Brainpower reasoning: Aql / dimaag",
        "shortcutEs": '1. Of the mind: <strong>Mental</strong> ≈ Identical to English <strong>"Mental"</strong>! | <strong>Psíquico</strong> ≈ <strong>"Psychic"</strong> (psychological / of the mind)!<br>2. Brainpower reasoning: <strong>Intelecto</strong> ≈ <strong>"Intellect"</strong>! | <strong>Entendimiento</strong> ≈ Understanding & sharp reasoning!',
        "shortcutHi": '1. Of the mind: <strong>Dimaagi</strong> ≈ From <strong>Dimaag (Brain) + -i</strong> → Pertaining to the mind = <em>Mental</em>!<br>2. Brainpower reasoning: <strong>Aql</strong> ≈ Sounds like <strong>"I.Q.-Clever"</strong> (sharp street-smarts & wisdom)! | <strong>Dimaag</strong> ≈ Deep brainpower ("<em>De-mark</em> smart brainpower") = <em>Mind / Brain</em>!',
    },
    1425: {
        "es": "1. Awake aware: Consciente | 2. Mental layer under surface: Subconsciente",
        "hi": "1. Awake aware: Hosh mein | 2. Mental layer under surface: Mann ke andar",
        "shortcutEs": '1. Awake aware: <strong>Consciente</strong> ≈ Direct sibling of English <strong>"Conscious"</strong>!<br>2. Mental layer under surface: <strong>Subconsciente</strong> ≈ Direct sibling of English <strong>"Subconscious"</strong> (hidden mind layer below awareness)!',
        "shortcutHi": '1. Awake aware: <strong>Hosh mein</strong> ≈ <strong>Hosh</strong> (Awake alertness — "Whole sense") + <strong>Mein</strong> (In) = Wide awake / <em>Conscious</em>!<br>2. Mental layer under surface: <strong>Mann ke andar</strong> ≈ <strong>Mann (Tamil மனம் = Mind)</strong> + <strong>ke Andar (Deep inside)</strong> = Hidden <em>Subconscious</em>!',
    },
    1426: {
        "es": "1. Sound judgment mind: Cordura / juicio | 2. Madness disorder: Locura / demencia",
        "hi": "1. Sound judgment mind: Samajhdaari | 2. Madness disorder: Paagalpan / deewanapan",
        "shortcutEs": '1. Sound judgment mind: <strong>Cordura</strong> ≈ Balanced <strong>"Core"</strong> mind (not <em>Loco</em>) = <em>Sanity</em>! | <strong>Juicio</strong> ≈ Sound <strong>"Judgment"</strong> / clear sense!<br>2. Madness disorder: <strong>Locura</strong> ≈ From famous <strong>"Loco" (Crazy!)</strong>! | <strong>Demencia</strong> ≈ <strong>"Dementia"</strong> = Losing one’s mind!',
        "shortcutHi": '1. Sound judgment mind: <strong>Samajhdaari</strong> ≈ From <strong>Samajh (Understanding) + -daari</strong> = Sound wisdom & <em>Sanity</em>!<br>2. Madness disorder: <strong>Paagalpan</strong> ≈ <strong>Spoken Tamil பாகல் (Paagal = Mad!)</strong> + <strong>-pan (-ness)</strong> = <em>Madness</em>! | <strong>Deewanapan</strong> ≈ Wild obsession / craze = <em>Frenzy / Insanity</em>!',
    },
    1427: {
        "es": "1. Deep emotional shock: Trauma / herida emocional | 2. Irrational dread: Fobia",
        "hi": "1. Deep emotional shock: Gehra sadma / trauma | 2. Irrational dread: Behisaab darr / phobia",
        "shortcutEs": '1. Deep emotional shock: <strong>Trauma</strong> ≈ English <strong>"Trauma"</strong>! | <strong>Herida emocional</strong> ≈ Emotional <em>Wound (Herida)</em>!<br>2. Irrational dread: <strong>Fobia</strong> ≈ Direct sibling of English <strong>"Phobia" (Fobia ≈ Phobia)</strong>!',
        "shortcutHi": '1. Deep emotional shock: <strong>Gehra sadma</strong> ≈ <strong>Gehra</strong> (Deep) + <strong>Sadma</strong> ("Sad-Shock" grief) = Heavy <em>Trauma</em>! | <strong>Trauma</strong> ≈ Spoken daily!<br>2. Irrational dread: <strong>Behisaab darr</strong> ≈ <strong>Behisaab</strong> (Beyond measure/countless) + <strong>Darr</strong> (Fear) = <em>Phobia</em>! | <strong>Phobia</strong> ≈ Spoken daily!',
    },
    1428: {
        "es": "Adicción / dependencia",
        "hi": "Lat / aadat",
        "shortcutEs": '<strong>Adicción</strong> ≈ Direct sibling of English <strong>"Addiction"</strong>! | <strong>Dependencia</strong> ≈ Direct sibling of English <strong>"Dependency"</strong> (reliant on a substance/habit)!',
        "shortcutHi": '<strong>Lat</strong> ≈ "That habit <em>LATCHED</em> onto you!" → Compulsive craving = <em>Addiction (Lat)</em>! | <strong>Aadat</strong> ≈ Same root as <strong>Tamil ஆஸ்தி / வழக்கம் (Habitual routine = <em>Aadat</em>)</strong>!',
    },
    1429: {
        "es": "Agotamiento (por estrés) / estar quemado",
        "hi": "Thakaan se toot jaana / burnout",
        "shortcutEs": '<strong>Agotamiento</strong> ≈ From <strong>Agotado ("All-Got-Out" of battery)</strong> → Complete mental drain! | <strong>Estar quemado</strong> ≈ Literally "to be <em>Burned</em> out" from overwork!',
        "shortcutHi": '<strong>Thakaan se toot jaana</strong> ≈ <strong>Thakaan</strong> (Exhaustion) + <strong>Toot jaana</strong> (Snapping/breaking apart from stress)! | <strong>Burnout</strong> ≈ Used directly in modern office Hindi!',
    },
    1430: {
        "es": "1. Deceptive appearance: Ilusión / espejismo | 2. Sensory false phantom: Alucinación",
        "hi": "1. Deceptive appearance: Dhokha | 2. Sensory false phantom: Veham",
        "shortcutEs": '1. Deceptive appearance: <strong>Ilusión</strong> ≈ English <strong>"Illusion"</strong>! | <strong>Espejismo</strong> ≈ From <strong>Espejo ("Specs/Mirror")</strong> = Desert <em>Mirage</em>!<br>2. Sensory false phantom: <strong>Alucinación</strong> ≈ Direct sibling of English <strong>"Hallucination"</strong>!',
        "shortcutHi": '1. Deceptive appearance: <strong>Dhokha</strong> ≈ Optical trick deceiving your eyes ("Aankhon ka <em>dhokha</em>" = Optical <em>Illusion</em>)!<br>2. Sensory false phantom: <strong>Veham</strong> ≈ Sounds like <strong>"Whim / Phantom"</strong> → Seeing or imagining unreal ghosts in your head = <em>Hallucination / Delusion</em>!',
    },
    1431: {
        "es": "1. Primal reflex: Instinto | 2. Gut feeling flash: Intuición / corazonada",
        "hi": "1. Primal reflex: Andaaza | 2. Gut feeling flash: Dil ki aawaaz",
        "shortcutEs": '1. Primal reflex: <strong>Instinto</strong> ≈ Direct sibling of English <strong>"Instinct"</strong>!<br>2. Gut feeling flash: <strong>Intuición</strong> ≈ <strong>"Intuition"</strong>! | <strong>Corazonada</strong> ≈ From <strong>Corazón (Heart)</strong> → Heart-thumping <em>Hunch</em>!',
        "shortcutHi": '1. Primal reflex: <strong>Andaaza</strong> ≈ <strong>Spoken Tamil அந்தாஜு (Andhaaju = Rough hunch/guess!)</strong> → Quick gut feel = <em>Instinct / Hunch</em>!<br>2. Gut feeling flash: <strong>Dil ki aawaaz</strong> ≈ <strong>Dil</strong> (Heart) + <strong>ki Aawaaz</strong> (Voice) = Inner voice = <em>Intuition</em>!',
    },
    1432: {
        "es": "Mentalidad / actitud / forma de pensar",
        "hi": "Soch / rawaiya",
        "shortcutEs": '<strong>Mentalidad</strong> ≈ <strong>"Mentality"</strong>! | <strong>Actitud</strong> ≈ <strong>"Attitude"</strong>! | <strong>Forma de pensar</strong> ≈ Literally "Form/Way of thinking (<em>Pensar ≈ Pensive</em>)" = <em>Mindset</em>!',
        "shortcutHi": '<strong>Soch</strong> ≈ Thinking / Outlook ("Badi <em>soch</em>" = Growth <em>Mindset</em>)! | <strong>Rawaiya</strong> ≈ Spoken daily for how someone acts/reacts toward others = <em>Attitude (Rawaiya)</em>!',
    },
    1433: {
        "es": "Fuerza de voluntad / determinación",
        "hi": "Pakka iraada / himmat",
        "shortcutEs": '<strong>Fuerza de voluntad</strong> ≈ <strong>Fuerza (Force) + Voluntad (Volition/Will)</strong> = Literally <em>Willpower</em>! | <strong>Determinación</strong> ≈ Direct sibling of English <strong>"Determination"</strong>!',
        "shortcutHi": '<strong>Pakka iraada</strong> ≈ <strong>Pakka (Solid/Fixed — Tamil பக்கா!)</strong> + <strong>Iraada (Iron Resolve)</strong> = Unshakable resolution! | <strong>Himmat</strong> ≈ <strong>Spoken Tamil ஹிம்மத் (Guts/Courage!)</strong>!',
    },
    1434: {
        "es": "1. Reserved inward loner: Introvertido | 2. Outgoing social butterfly: Extrovertido",
        "hi": "1. Reserved inward loner: Kam-bolne wala / sharmila | 2. Outgoing social butterfly: Milansaar / khulkar bolne wala",
        "shortcutEs": '1. Reserved inward loner: <strong>Introvertido</strong> ≈ Direct sibling of English <strong>"Introverted"</strong>!<br>2. Outgoing social butterfly: <strong>Extrovertido</strong> ≈ Direct sibling of English <strong>"Extroverted"</strong>!',
        "shortcutHi": '1. Reserved inward loner: <strong>Kam-bolne wala / sharmila</strong> ≈ <strong>Kam-bolne wala</strong> (Little-talking person) + <strong>Sharmila</strong> (Shy/Bashful) = <em>Introvert</em>!<br>2. Outgoing social butterfly: <strong>Milansaar</strong> ≈ From <strong>Milna (Meet & mingle warmly)</strong>! | <strong>Khulkar bolne wala</strong> ≈ <strong>Khulkar</strong> (Openly) + <strong>Bolne wala</strong> (Speaker)!',
    },
    1435: {
        "es": "1. Owned asset holding: Propiedad / inmueble | 2. Bare ground plot: Terreno / lote / parcela",
        "hi": "1. Owned asset holding: Property / jaaydaad | 2. Bare ground plot: Plot / zameen ka tukda",
        "shortcutEs": '1. Owned asset holding: <strong>Propiedad</strong> ≈ <strong>"Property"</strong>! | <strong>Inmueble</strong> ≈ <strong>Im-mobile</strong> (unmovable land/buildings = <em>Real Estate</em>)!<br>2. Bare ground plot: <strong>Terreno</strong> ≈ <strong>"Terrain"</strong>! | <strong>Lote / parcela</strong> ≈ <strong>"Lot / Parcel"</strong> of land!',
        "shortcutHi": '1. Owned asset holding: <strong>Property</strong> ≈ Everyday real-estate term! | <strong>Jaaydaad</strong> ≈ Ancestral/family estate wealth = <em>Property / Assets</em>!<br>2. Bare ground plot: <strong>Plot</strong> ≈ Standard Indian housing word! | <strong>Zameen ka tukda</strong> ≈ <strong>Zameen (Land) + Tukda (Piece)</strong>!',
    },
    1436: {
        "es": "Propietario / casero / dueño",
        "hi": "Makaan-maalik",
        "shortcutEs": '<strong>Propietario</strong> ≈ <strong>"Proprietor"</strong> (legal owner)! | <strong>Casero</strong> ≈ From <strong>Casa (House)</strong> (house-keeper/landlord)! | <strong>Dueño</strong> ≈ From <strong>Dominus ("Owner/Master")</strong>!',
        "shortcutHi": '<strong>Makaan-maalik</strong> ≈ <strong>Makaan (House)</strong> + <strong>Maalik (Tamil மாலிக் / உரிமையாளர் = Owner!)</strong> → Owner of the house = <em>Landlord</em>!',
    },
    1437: {
        "es": "Inquilino / arrendatario",
        "hi": "Kirayedaar",
        "shortcutEs": '<strong>Inquilino</strong> ≈ Sounds like <strong>"In-Key-Living"</strong> → Person living inside with the house key = <em>Tenant</em>! | <strong>Arrendatario</strong> ≈ From <strong>Renta (Rent)</strong> → Lease-paying <em>Renter</em>!',
        "shortcutHi": '<strong>Kirayedaar</strong> ≈ <strong>Kiraya (Rent — Tamil கிரயம் = Price/Payment)</strong> + <strong>-daar (Holder/Payer)</strong> → Rent-payer living in your flat = <em>Tenant</em>!',
    },
    1438: {
        "es": "1. Monthly occupancy fee: Alquiler / renta | 2. Contract tenure term: Contrato de arrendamiento",
        "hi": "1. Monthly occupancy fee: Kiraya | 2. Contract tenure term: Lease",
        "shortcutEs": '1. Monthly occupancy fee: <strong>Alquiler</strong> ≈ Think <strong>"All-Key-Hire"</strong> (monthly apartment <em>Rent</em>)! | <strong>Renta</strong> ≈ Direct sibling of English <strong>"Rent"</strong>!<br>2. Contract tenure term: <strong>Contrato de arrendamiento</strong> ≈ <strong>"Contract"</strong> of renting/leasing = <em>Lease Agreement</em>!',
        "shortcutHi": '1. Monthly occupancy fee: <strong>Kiraya</strong> ≈ From <strong>Tamil கிரயம் (Kirayam = Fare/Fee!)</strong> → Monthly flat rent or cab fare!<br>2. Contract tenure term: <strong>Lease</strong> ≈ Standard Indian property/rental contract term!',
    },
    1439: {
        "es": "Pago inicial / anticipo / enganche",
        "hi": "Downpayment / advance",
        "shortcutEs": '<strong>Pago inicial</strong> ≈ <strong>Initial Payment</strong>! | <strong>Anticipo</strong> ≈ <strong>"Anticipate"</strong> (upfront advance)! | <strong>Enganche</strong> ≈ Hook/lock in a car or house deal with upfront cash = <em>Downpayment</em>!',
        "shortcutHi": '<strong>Downpayment / advance</strong> ≈ Both standard English banking terms are used directly in everyday Hindi when buying a home, bike, or booking a flat!',
    },
    1440: {
        "es": "1. Possession status right: Propiedad / titularidad | 2. Written title registry: Escritura / título de propiedad",
        "hi": "1. Possession status right: Haq | 2. Written title registry: Registry",
        "shortcutEs": '1. Possession status right: <strong>Propiedad</strong> ≈ <strong>"Property"</strong>! | <strong>Titularidad</strong> ≈ Holding official <strong>"Title"</strong>!<br>2. Written title registry: <strong>Escritura</strong> ≈ <strong>"Scripture / Script"</strong> (signed legal paper)! | <strong>Título de propiedad</strong> ≈ <strong>Title</strong> of property = <em>Deed</em>!',
        "shortcutHi": '1. Possession status right: <strong>Haq</strong> ≈ <strong>Spoken Tamil ஹக் (Hakku = Rightful claim!)</strong> → Legal ownership right!<br>2. Written title registry: <strong>Registry</strong> ≈ Universal Indian real-estate word ("Plot ki <em>registry</em>" = Recorded property <em>Deed</em>)!',
    },
    1441: {
        "es": "Compañero de piso / de cuarto",
        "hi": "Room-partner / flatmate",
        "shortcutEs": '<strong>Compañero de piso / de cuarto</strong> ≈ <strong>Compañero ("Companion")</strong> + <strong>de Piso (Flat/Floor)</strong> or <strong>de Cuarto (Room/"Quarter")</strong> = <em>Flatmate / Roommate</em>!',
        "shortcutHi": '<strong>Room-partner / flatmate</strong> ≈ Both crisp English compound terms are used directly across Indian hostels and shared apartments!',
    },
    1442: {
        "es": "Alojamiento / vivienda / residencia",
        "hi": "Rehne ki jagah / makaan",
        "shortcutEs": '<strong>Alojamiento</strong> ≈ Contains <strong>"Lodge" (A-loja-miento)</strong>! | <strong>Vivienda</strong> ≈ From <strong>Vivir ("Vivid"/Live)</strong> = Dwelling! | <strong>Residencia</strong> ≈ <strong>"Residence"</strong>!',
        "shortcutHi": '<strong>Rehne ki jagah</strong> ≈ <strong>Rehne (Living) + ki Jagah (Place)</strong> = Place to stay / <em>Accommodation</em>! | <strong>Makaan</strong> ≈ Built house structure / <em>Residence</em>!',
    },
    1443: {
        "es": "1. Fitted with furniture: Amueblado | 2. Empty bare walls: Sin amueblar / vacío",
        "hi": "1. Fitted with furniture: Furnished / saamaan ke saath | 2. Empty bare walls: Bina saamaan ka / khaali",
        "shortcutEs": '1. Fitted with furniture: <strong>Amueblado</strong> ≈ From <strong>Muebles ("Mobile" goods = Furniture)</strong> → Ready with sofa & bed = <em>Furnished</em>!<br>2. Empty bare walls: <strong>Sin amueblar</strong> ≈ <strong>Sin (Without)</strong> furniture! | <strong>Vacío</strong> ≈ <strong>"Vacant / Vacuum"</strong> = Bare empty!',
        "shortcutHi": '1. Fitted with furniture: <strong>Furnished / saamaan ke saath</strong> ≈ English <strong>"Furnished"</strong> or <strong>Saamaan (Stuff — Tamil சாமான்!) + ke Saath (With)</strong>!<br>2. Empty bare walls: <strong>Bina saamaan ka / khaali</strong> ≈ <strong>Bina (Without) + Saamaan (Tamil சாமான்)</strong> | <strong>Khaali (Tamil காலி = Empty!)</strong>!',
    },
    1444: {
        "es": "Servicios básicos / facturas (luz, agua, gas)",
        "hi": "Bijli-paani ke kharche / bills",
        "shortcutEs": '<strong>Servicios básicos</strong> ≈ <strong>Basic Services</strong> (power, water, gas)! | <strong>Facturas (luz, agua, gas)</strong> ≈ Monthly house <strong>"Factor/Bills"</strong> (light, water, gas)!',
        "shortcutHi": '<strong>Bijli-paani ke kharche</strong> ≈ <strong>Bijli (Electricity) + Paani (Water) + Kharche (Expenses — Tamil செலவு)</strong>! | <strong>Bills</strong> ≈ Spoken daily for utility invoices!',
    },
    1445: {
        "es": "Mantenimiento / conservación / arreglo",
        "hi": "Dekhbhaal / marammat",
        "shortcutEs": '<strong>Mantenimiento</strong> ≈ <strong>"Maintenance"</strong>! | <strong>Conservación</strong> ≈ <strong>"Conservation"</strong> (upkeep)! | <strong>Arreglo</strong> ≈ Putting back in <strong>"Regular/Order"</strong> = Fix / <em>Repair</em>!',
        "shortcutHi": '<strong>Dekhbhaal</strong> ≈ <strong>Dekh (Watch/Look) + Bhaal (Care)</strong> = Regular upkeep & <em>Maintenance</em>! | <strong>Marammat</strong> ≈ <strong>Tamil மராமத்து (Maraamatthu = Repair/Upkeep work!)</strong> → 100% shared word!',
    },
    1446: {
        "es": "Mudanza / traslado",
        "hi": "Ghar badalna / shifting",
        "shortcutEs": '<strong>Mudanza</strong> ≈ From <strong>Mudar (Change "Mode"/Home)</strong> → Packing boxes to move house = <em>Relocation</em>! | <strong>Traslado</strong> ≈ <strong>Tras- ("Trans-" Across) + Lado (Place)</strong> → Transfer across town!',
        "shortcutHi": '<strong>Ghar badalna</strong> ≈ <strong>Ghar (Home) + Badalna (Change/Swap)</strong> = Moving to a new house! | <strong>Shifting</strong> ≈ Standard everyday Indian word ("Kal hum new flat mein <em>shifting</em> kar rahe hain")!',
    },
}


def polish_legacy_template_text(s: str) -> str:
    """Clean ugly automated trailing '(Card Title (Sense) (Word))' bloat in Split 1-7 without changing meaning."""
    if not s:
        return s
    # Replace: Direct English loanword "X" used in daily spoken Hindi → <em>TITLE (SENSE) (X)</em>!
    # with cleaner: Everyday spoken English/Hindi loanword <strong>"X"</strong> → <em>SENSE (X)</em>!
    s = re.sub(
        r'Direct English loanword <strong>"([^"]+)"</strong> used in daily spoken Hindi\s*→\s*<em>[^<]*?\(([^()]+)\)</em>!',
        r'Everyday spoken loanword <strong>"\1"</strong> used directly in daily Hindi → <em>\2</em>!',
        s,
    )
    # Also strip doubled trailing parens like (Title (Sense) (Word)) -> (Sense: Word) in Latin root template
    s = re.sub(
        r'Direct match with English <strong>"([^"]+)"</strong> \(same Latin root\)\s*→\s*<em>[^<]*?\(([^()]+)\)\s*\(([^()]+)\)</em>!',
        r'Direct sibling of English <strong>"\1"</strong> → <em>\2 (\3)</em>!',
        s,
    )
    s = re.sub(
        r'Direct match with English <strong>"([^"]+)"</strong> \(same Latin root\)\s*→\s*<em>[^<]*?\(([^()]+)\)</em>!',
        r'Direct sibling of English <strong>"\1"</strong> → <em>\2</em>!',
        s,
    )
    return s


def main():
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Update split8DeckCards atomically
    m8 = re.search(r"((?:var|let|const)\s+split8DeckCards\s*=\s*)(\[.*?\])(;)", html)
    if not m8:
        raise RuntimeError("Could not find split8DeckCards")
    s8_cards = json.loads(m8.group(2))
    updated_map = {}
    for c in s8_cards:
        num = c["num"]
        if num in SPLIT8_UPDATES:
            upd = SPLIT8_UPDATES[num]
            c["trans"]["es"] = upd["es"]
            c["trans"]["hi"] = upd["hi"]
            c["hiDevanagari"] = upd["hi"]
            c["shortcutEs"] = upd["shortcutEs"]
            c["shortcutHi"] = upd["shortcutHi"]
        updated_map[num] = c

    new_s8_str = m8.group(1) + json.dumps(s8_cards, ensure_ascii=False) + m8.group(3)
    html = html[:m8.start()] + new_s8_str + html[m8.end():]

    # 2. Polish robotic parenthetical bloat in split1..split7
    for dname in ["split1DeckCards", "split2DeckCards", "split5DeckCards", "split6DeckCards", "split7DeckCards"]:
        m = re.search(rf"((?:var|let|const)\s+{dname}\s*=\s*)(\[.*?\])(;)", html)
        if not m:
            raise RuntimeError(f"Could not find {dname}")
        arr = json.loads(m.group(2))
        for c in arr:
            if c.get("shortcutEs"):
                c["shortcutEs"] = polish_legacy_template_text(c["shortcutEs"])
            if c.get("shortcutHi"):
                c["shortcutHi"] = polish_legacy_template_text(c["shortcutHi"])
            updated_map[c["num"]] = c
        repl = m.group(1) + json.dumps(arr, ensure_ascii=False) + m.group(3)
        html = html[:m.start()] + repl + html[m.end():]

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(html)

    # 3. Sync data/backup_original_cards.json
    if os.path.exists(BACKUP_PATH):
        with open(BACKUP_PATH, "r", encoding="utf-8") as f:
            backup = json.load(f)
        if isinstance(backup, dict):
            for k, val in backup.items():
                if isinstance(val, dict) and val.get("num") in updated_map:
                    src = updated_map[val["num"]]
                    val["trans"] = dict(src["trans"])
                    val["hiDevanagari"] = src.get("hiDevanagari", src["trans"]["hi"])
                    val["shortcutEs"] = src.get("shortcutEs", "")
                    val["shortcutHi"] = src.get("shortcutHi", "")
        with open(BACKUP_PATH, "w", encoding="utf-8") as f:
            json.dump(backup, f, indent=2, ensure_ascii=False)

    print(f"Updated Split 8 ({len(SPLIT8_UPDATES)} cards) and polished Split 1-7 templates across {len(updated_map)} cards.")


if __name__ == "__main__":
    main()
