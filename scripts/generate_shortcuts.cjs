const fs = require('fs');

// Comprehensive, witty, phonetic & visual memory shortcuts for all cards 800-1000
// Pure visual/phonetic punchlines relating to Indian/Tamil/English contexts
const shortcuts = {
  800: { // STOVE
    es: "<strong>Es-tufa</strong> → <em>Tough-ah</em> flame on the stove, or <em>Stuff</em> the cooking pot onto the burner!",
    hi: "<strong>Choolha</strong> → Village desi <em>Chulha</em> cooking hot rotis over crackling clay fire!"
  },
  801: { // OVEN
    es: "<strong>Horn-o</strong> → Sounds like a blazing hot <em>horn</em> blowing superheated air inside!",
    hi: "<strong>Tandoor Oven</strong> → Desi <em>Tandoor</em> baking hot butter naan and roasted tandoori paneer!"
  },
  802: { // SINK
    es: "<strong>Free-ga-there-o (Fregadero)</strong> → Sink-la cold water vandhu kai <em>freeze</em> aagudhu (or <em>Free</em>-ya dishes podra edam)!",
    hi: "<strong>Sink</strong> → Indian kitchen-la direct-ah <em>'Sink'</em> nu dhaan solluvanga, zero effort!"
  },
  803: { // TAP
    es: "<strong>Giraffe-o (Grifo)</strong> → The tall curved neck of the tap looks exactly like a <em>giraffe</em> bending down to spit water!",
    hi: "<strong>Null (Nal)</strong> → Turn the tap knob off till water flow drops to zero (<em>null</em>)!"
  },
  804: { // SPONGE
    es: "<strong>Es-ponja</strong> → English word <em>Sponge</em> with an 'Es-' prefix added: Es-ponge-a!",
    hi: "<strong>Sponge</strong> → Desi spoken word: direct <em>Sponge</em> to wipe kitchen counters!"
  },
  805: { // APRON
    es: "<strong>Delantal</strong> → In Spanish 'delante' means front. Worn in the <em>front</em> so curry never stains your shirt!",
    hi: "<strong>Apron</strong> → MasterChef style cooking <em>Apron</em> tied around the neck!"
  },
  806: { // TABLECLOTH
    es: "<strong>Mantel</strong> → Drapes like a royal protective <em>mantle</em> over the dining table to keep it spotless!",
    hi: "<strong>Mez-posh</strong> → <em>Mez</em> (Table) + <em>Posh</em> (Outfit/Dress) = Designer dress for the dining table!"
  },
  807: { // MENU
    es: "<strong>Menú</strong> → Exact match with English <em>Menu</em>, with a stylish accent on the 'ú'!",
    hi: "<strong>Menu</strong> → Hotel-la first command: 'Bhaiya, pehle <em>Menu</em> card lao'!"
  },
  808: { // HOUSE
    es: "<strong>Casa</strong> → Iconic phrase <em>'Mi Casa es su Casa'</em> (My house is your house)!",
    hi: "<strong>Makaan</strong> → Legendary Bollywood line: 'Roti, Kapda aur <em>Makaan</em>'!"
  },
  809: { // HOME
    es: "<strong>Hogar</strong> → Sounds like <em>Hug-ar</em>. Home is the warm place where family gives you a tight hug!",
    hi: "<strong>Ghar</strong> → 'Apna <em>Ghar</em>' / 'Home sweet home' where your heart truly rests!"
  },
  810: { // ROOM
    es: "<strong>Habitación</strong> → Sounds like <em>Habitat</em> / where humans reside and live!",
    hi: "<strong>Kamra</strong> → 'Kamre ka darwaza band karo' / Classic Indian room!"
  },
  811: { // BEDROOM
    es: "<strong>Dormitorio</strong> → English <em>Dormitory</em> / Dorm where tired students sleep!",
    hi: "<strong>Bedroom</strong> → Direct modern Indian usage: directly <em>Bedroom</em>!"
  },
  812: { // BATHROOM
    es: "<strong>Baño</strong> → Sounds like <em>Bath</em>-o / Where you take a warm bath!",
    hi: "<strong>Bathroom</strong> → Direct everyday Indian usage: <em>Bathroom</em>!"
  },
  813: { // LIVING ROOM
    es: "<strong>Sala</strong> → Grand <em>Salon</em> or front sitting hall for guests!",
    hi: "<strong>Living Room</strong> → Front guest hall / family TV <em>Living Room</em>!"
  },
  814: { // DINING ROOM
    es: "<strong>Comedor</strong> → 'Comer' means eat. <em>Come-and-eat-dor</em> / Where the family gathers to eat!",
    hi: "<strong>Dining Room</strong> → Daily spoken term: <em>Dining Room</em> / khane ka kamra!"
  },
  815: { // KITCHEN
    es: "<strong>Cocina</strong> → <em>Cook-sina / Cuisine</em> / Where aromatic food is cooked!",
    hi: "<strong>Rasoi</strong> → Traditional mother's <em>Rasoi-ghar</em> with fresh garam chai and aromas!"
  },
  816: { // HALLWAY
    es: "<strong>Pasillo</strong> → <em>Pass</em>-illo / The long narrow walkway you <em>pass</em> through!",
    hi: "<strong>Galiyara</strong> → Long house passage / house ki <em>gali (galiyara)</em>!"
  },
  817: { // CORRIDOR
    es: "<strong>Corredor</strong> → Direct English sound match with <em>Corridor</em>!",
    hi: "<strong>Corridor</strong> → School/office <em>Corridor</em> where everyone walks!"
  },
  818: { // CEILING
    es: "<strong>Techo</strong> → <em>Tech</em> overhead / ceiling holding high-tech lamps and fan!",
    hi: "<strong>Chhat</strong> → Fan rotating smoothly under the <em>Chhat</em> (ceiling)!"
  },
  819: { // ROOF
    es: "<strong>Tejado</strong> → <em>Tile</em>-ado / Pitched roof covered with red Spanish terracotta tiles!",
    hi: "<strong>Chhat</strong> → Evening stroll on the open <em>Chhat</em> under starry skies!"
  },
  820: { // WALL
    es: "<strong>Pared</strong> → <em>Barred / Parade</em> stops immediately when hitting a solid concrete wall!",
    hi: "<strong>Deewaar</strong> → Amitabh Bachchan's evergreen movie dialogue: <em>'Deewaar'</em>!"
  },
  821: { // FLOOR
    es: "<strong>Suelo / Piso</strong> → <em>Soil</em>-o / The ground level right above Mother Earth's soil!",
    hi: "<strong>Farsh</strong> → Sparkling clean marble <em>Farsh</em> polished till it shines!"
  },
  822: { // DOOR
    es: "<strong>Puerta</strong> → <em>Portal</em> / The main entry portal into the room or house!",
    hi: "<strong>Darwaaza</strong> → 'Darwaaza khadkhadao' / Classic entrance doorway!"
  },
  823: { // WINDOW
    es: "<strong>Ventana</strong> → <em>Vent</em>-ana / Cool breezy natural <em>ventilation</em> enters through the window!",
    hi: "<strong>Khidki</strong> → 'Khidki se bahar dekho' / Peeking into the street from the window!"
  },
  824: { // STAIRS
    es: "<strong>Escaleras</strong> → <em>Escalator</em>-as / Step-by-step staircase leading to upper floors!",
    hi: "<strong>Seedhiyan</strong> → Walk <em>Seedha</em> (straight) up the stairs without tripping!"
  },
  825: { // BASEMENT
    es: "<strong>Sótano</strong> → <em>Sub-terrain</em> / Deep subterranean room below the ground floor!",
    hi: "<strong>Tehkhana</strong> → Mysterious historical underground <em>Tehkhana</em>!"
  },
  826: { // ATTIC
    es: "<strong>Ático</strong> → Direct sound match with English <em>Attic</em> (just say with Spanish rhythm)!",
    hi: "<strong>Attari</strong> → High loft under the roof for vintage trunks: <em>Attari</em>!"
  },
  827: { // GARAGE
    es: "<strong>Garaje</strong> → Exact phonetic match with <em>Garage</em>!",
    hi: "<strong>Garage</strong> → Park the car and bike inside the <em>Garage</em>!"
  },
  828: { // BALCONY
    es: "<strong>Balcón</strong> → Direct sound match with <em>Balcony</em>!",
    hi: "<strong>Balcony</strong> → Morning cup of tea standing in the breezy <em>Balcony</em>!"
  },
  829: { // TERRACE
    es: "<strong>Terraza</strong> → Direct sound match with <em>Terrace</em> (Terra = earth/platform)!",
    hi: "<strong>Terrace / Chhat</strong> → Sunset kite flying and walking on the <em>Terrace</em>!"
  },
  830: { // GARDEN
    es: "<strong>Jardín</strong> → English <em>Garden</em> spoken with a soft Spanish 'J' (Har-deen)!",
    hi: "<strong>Bageecha</strong> → Blooming flowers and green grass in the <em>Bageecha</em>!"
  },
  831: { // YARD
    es: "<strong>Patio</strong> → Classic open-air Spanish courtyard / <em>Patio</em>!",
    hi: "<strong>Aangan</strong> → Traditional Indian house courtyard <em>Aangan</em> with a Tulsi plant!"
  },
  832: { // FENCE
    es: "<strong>Cerca</strong> → <em>Circle</em>-ca / Wooden boundary fencing that circles around the garden!",
    hi: "<strong>Baadh</strong> → Protective wooden or wire boundary <em>Baadh</em> around farm!"
  },
  833: { // GATE
    es: "<strong>Puerta</strong> → <em>Portal</em> / Iron entrance gate opening wide for visitors!",
    hi: "<strong>Phaatak</strong> → Grand iron railway or bungalow <em>Phaatak</em>!",
  },
  834: { // PORCH
    es: "<strong>Porche</strong> → Direct sound match with <em>Porch</em>!",
    hi: "<strong>Baramda</strong> → Front shaded sit-out <em>Baramda</em> where grandfather reads newspapers!"
  },
  835: { // CHIMNEY
    es: "<strong>Chimenea</strong> → Direct sound match with <em>Chimney</em>!",
    hi: "<strong>Chimney</strong> → Rooftop brick smoke pipe: <em>Chimney</em>!"
  },
  836: { // TABLE
    es: "<strong>Mesa</strong> → Clean the <em>Mess</em> off the study/dining table!",
    hi: "<strong>Mez</strong> → 'Kitab <em>Mez</em> par rakho' / Sturdy wooden study table!"
  },
  837: { // CHAIR
    es: "<strong>Silla</strong> → Sit and <em>Chill-a</em> on the chair!",
    hi: "<strong>Kursi</strong> → 'Kursi par baithiye' / Classic four-legged wooden chair!"
  },
  838: { // ARMCHAIR
    es: "<strong>Sillón</strong> → Big <em>Silla</em> / Luxurious plush armchair with armrests!",
    hi: "<strong>Aaraam Kursi</strong> → <em>Aaraam</em> (Rest) dene wali ultra-comfy rocking armchair!"
  },
  839: { // SOFA
    es: "<strong>Sofá</strong> → Direct match with <em>Sofa</em>!",
    hi: "<strong>Sofa</strong> → Living room plush three-seater <em>Sofa</em>!"
  },
  840: { // COUCH
    es: "<strong>Sofá</strong> → Direct match with <em>Sofa / Couch</em>!",
    hi: "<strong>Sofa</strong> → Couch potato relaxing on the <em>Sofa</em>!"
  },
  841: { // BED
    es: "<strong>Cama</strong> → <em>Calm-a</em> down and sleep soundly in bed!",
    hi: "<strong>Bistar</strong> → 'Bistar lagao' / Cozy bedtime mattress and blanket setup!"
  },
  842: { // MATTRESS
    es: "<strong>Colchón</strong> → Giant <em>Cushion</em> that cushions your entire body while sleeping!",
    hi: "<strong>Gadda</strong> → Super soft fluffy cotton <em>Gadda</em> spread on the cot!"
  },
  843: { // PILLOW
    es: "<strong>Almohada</strong> → Soft as sweet <em>Almond</em> cream under your head!",
    hi: "<strong>Takiya</strong> → Rest your tired neck on a plush fluffy <em>Takiya</em>!"
  },
  844: { // BLANKET
    es: "<strong>Manta</strong> → Wrap yourself in a warm woolen <em>Mantle</em> on chilly nights!",
    hi: "<strong>Kambal</strong> → Snuggle inside a heavy warm woolen <em>Kambal</em> during winter!"
  },
  845: { // SHEET
    es: "<strong>Sábana</strong> → Smooth cool white cotton bedsheet covering the bed!",
    hi: "<strong>Chaadar</strong> → Spread a clean fresh floral <em>Chaadar</em> over the mattress!"
  },
  846: { // CURTAIN
    es: "<strong>Cortina</strong> → Sounds just like English <em>Curtain</em>: Cor-teena!",
    hi: "<strong>Parda</strong> → 'Parda gira do' / Draw the window curtain to block direct sunlight!"
  },
  847: { // CARPET
    es: "<strong>Alfombra</strong> → <em>Al-foam-bra</em> / Soft spongy foam cushioning under your feet!",
    hi: "<strong>Kaaleen</strong> → Luxurious Kashmiri floral woven <em>Kaaleen</em> on the floor!"
  },
  848: { // RUG
    es: "<strong>Alfombra</strong> → Woven decorative floor rug / soft runner!",
    hi: "<strong>Rug / Kaaleen</strong> → Small bedside ornamental woven <em>Rug</em>!"
  },
  849: { // MIRROR
    es: "<strong>Espejo</strong> → Wear your <em>Specs-ejo</em> and check your face in the mirror!",
    hi: "<strong>Aaina</strong> → 'Aaina jhoot nahi bolta' / Gaze into the crystal mirror!"
  },
  850: { // CLOSET
    es: "<strong>Armario</strong> → Sounds like <em>Armory</em> / Wardrobe closet where all shirts and outfits are stored!",
    hi: "<strong>Almaari</strong> → Traditional heavy Godrej steel <em>Almaari</em> full of neatly folded clothes!"
  },
  851: { // WARDROBE
    es: "<strong>Armario</strong> → Grand wooden wardrobe with full-length mirror doors!",
    hi: "<strong>Wardrobe / Almaari</strong> → Bedroom sliding door <em>Wardrobe</em>!"
  },
  852: { // CUPBOARD
    es: "<strong>Alacena</strong> → Kitchen wall cupboard holding spices and dinner plates!",
    hi: "<strong>Cupboard / Almaari</strong> → Crockery storage cupboard in kitchen!"
  },
  853: { // CABINET
    es: "<strong>Gabinete</strong> → Direct sound match with <em>Cabinet</em>!",
    hi: "<strong>Cabinet</strong> → Wooden storage cabinet with shelves!"
  },
  854: { // DRAWER
    es: "<strong>Cajón</strong> → Big sliding <em>Caja</em> (box) that slides smoothly out of the desk!",
    hi: "<strong>Daraaz</strong> → Pull open the desk <em>Daraaz</em> to grab your pens and documents!"
  },
  855: { // SHELF
    es: "<strong>Estante</strong> → <em>Stand</em>-te / Sturdy wooden plank where items <em>stand</em> safely!",
    hi: "<strong>Shelf</strong> → Wall <em>Shelf</em> holding trophies and potted succulents!"
  },
  856: { // BOOKCASE
    es: "<strong>Librería</strong> → Mini home <em>Library</em> cabinet packed with your favorite novels!",
    hi: "<strong>Kitabon ki Almaari</strong> → Multi-tier glass-door bookcase packed with books!"
  },
  857: { // DESK
    es: "<strong>Escritorio</strong> → Place where you write <em>Scripts</em> and work on your laptop!",
    hi: "<strong>Desk</strong> → Study table and computer working <em>Desk</em>!"
  },
  858: { // LAMP
    es: "<strong>Lámpara</strong> → Direct sound match with English <em>Lamp</em>!",
    hi: "<strong>Lamp</strong> → Nightstand reading <em>Lamp</em> casting a cozy warm glow!"
  },
  859: { // BULB
    es: "<strong>Bombilla</strong> → Tiny pear-shaped glass <em>Bomb</em>-illa glowing with bright filament light!",
    hi: "<strong>Bulb</strong> → Classic yellow incandescent or LED <em>Bulb</em>!"
  },
  860: { // SWITCH
    es: "<strong>Interruptor</strong> → <em>Interrupts</em> electric flow to turn lights ON and OFF!",
    hi: "<strong>Switch</strong> → Click the wall <em>Switch</em> to turn on the room ceiling fan!"
  },
  861: { // PLUG
    es: "<strong>Enchufe</strong> → <em>En-chew-fe</em> / Metal pins bite firmly into wall socket like teeth!",
    hi: "<strong>Plug</strong> → Insert laptop charger <em>Plug</em> into power point!"
  },
  862: { // SOCKET
    es: "<strong>Enchufe</strong> → Wall outlet that accepts electric power plug pins!",
    hi: "<strong>Socket</strong> → Three-pin wall electrical <em>Socket</em>!"
  },
  863: { // WIRE
    es: "<strong>Cable</strong> → Direct sound match with electrical <em>Cable</em>!",
    hi: "<strong>Taar</strong> → Insulated copper electrical <em>Taar</em> carrying current!"
  },
  864: { // CLOCK
    es: "<strong>Reloj</strong> → Time to <em>Relax-o</em> when clock hands strike 5 PM! Ticks 're-loj'!",
    hi: "<strong>Ghadi</strong> → 'Ghadi me kitne baje hain?' / Ticking wall clock!"
  },
  865: { // BELL
    es: "<strong>Campana</strong> → Giant ringing bell in cathedral tower / rings like <em>Campanile</em>!",
    hi: "<strong>Ghanti</strong> → Ding-dong entrance doorbell / temple brass <em>Ghanti</em>!"
  },
  866: { // KEY
    es: "<strong>Llave (Yave)</strong> → Lock the front door before you <em>Leave</em> home!",
    hi: "<strong>Chaabi</strong> → 'Ghar ki <em>Chaabi</em> jeb me rakho' / Key to safety!"
  },
  867: { // PADLOCK
    es: "<strong>Candado</strong> → <em>Candid</em> heavy brass lock guarding your main gate!",
    hi: "<strong>Taala</strong> → Heavy brass <em>Taala</em> locked tight with key!"
  },
  868: { // BROOM
    es: "<strong>Escoba</strong> → <em>Scoop-a</em> / Sweeps and scoops up all dust off the floor!",
    hi: "<strong>Jhaadoo</strong> → Morning house cleaning ritual: <em>Jhaadoo</em>-pocha!"
  },
  869: { // MOP
    es: "<strong>Fregona</strong> → Wets and scrubs the floor spotless clean!",
    hi: "<strong>Pocha</strong> → Wet floor cleaning <em>Pocha</em> with lemon phenyl!"
  },
  870: { // BUCKET
    es: "<strong>Cubo</strong> → <em>Cube</em>-o / Large cylindrical container filled with water!",
    hi: "<strong>Baalti</strong> → Bright plastic bathroom <em>Baalti</em> full of fresh water!"
  },
  871: { // DUSTPAN
    es: "<strong>Recogedor</strong> → <em>Recover</em>-dor / Collects and recovers all swept dirt!",
    hi: "<strong>Dustpan</strong> → Plastic tray to pick up swept dust: <em>Dustpan</em>!"
  },
  872: { // TRASH
    es: "<strong>Basura</strong> → <em>Bass-ura</em> / Smelly waste food scraps you discard!",
    hi: "<strong>Kachra</strong> → 'Kachra mat phailao' / Throw waste into dustbin!"
  },
  873: { // BIN
    es: "<strong>Cubo de basura</strong> → Waste bucket / dustbin!",
    hi: "<strong>Koodedaan</strong> → Segregated green/blue waste <em>Koodedaan</em>!"
  },
  874: { // CANDLE
    es: "<strong>Vela</strong> → White wax candle giving bright <em>Velicham</em> (Tamil: bright light)!",
    hi: "<strong>Mombatti</strong> → <em>Mom</em> (Wax) + <em>Batti</em> (Wick/Light) = Wax candle!"
  },
  875: { // MATCH
    es: "<strong>Fósforo</strong> → Red <em>Phosphorus</em> chemical tip strikes instant flame on matchbox!",
    hi: "<strong>Maachis</strong> → Strike a single wooden <em>Maachis</em> stick to light diya!"
  },
  876: { // LIGHTER
    es: "<strong>Encendedor</strong> → <em>Incendiary</em> pocket tool that sparks instant flame!",
    hi: "<strong>Lighter</strong> → Kitchen gas stove clicker <em>Lighter</em>!"
  },
  877: { // SOAP
    es: "<strong>Jabón (Habón)</strong> → Sounds remarkably like Indian <em>Sabun</em>!",
    hi: "<strong>Sabun</strong> → 'Haath achhe se <em>Sabun</em> se dho lo' / Lathering bath soap!"
  },
  878: { // TOWEL
    es: "<strong>Toalla</strong> → Sounds just like English <em>Towel</em>-la!",
    hi: "<strong>Tauliya</strong> → Soft dry cotton bath <em>Tauliya</em> after a shower!"
  },
  879: { // SHAMPOO
    es: "<strong>Champú</strong> → Direct match with English <em>Shampoo</em> (which originally came from Hindi champi)!",
    hi: "<strong>Shampoo</strong> → Foaming hair wash <em>Shampoo</em>!"
  },
  880: { // TOOTHBRUSH
    es: "<strong>Cepillo de dientes</strong> → Dental brush to clean teeth!",
    hi: "<strong>Toothbrush</strong> → Morning toothpaste and <em>Toothbrush</em> routine!"
  },
  881: { // TOOTHPASTE
    es: "<strong>Pasta de dientes</strong> → Minty paste for white teeth!",
    hi: "<strong>Toothpaste</strong> → Mint fresh gel <em>Toothpaste</em>!"
  },
  882: { // RAZOR
    es: "<strong>Maquinilla de afeitar</strong> → Mini machine that gives a close clean shave!",
    hi: "<strong>Razor</strong> → Stainless steel safety <em>Razor</em> for smooth shave!"
  },
  883: { // SCISSORS
    es: "<strong>Tijeras</strong> → Sharp blades snip and <em>tear-as</em> cloth smoothly into pieces!",
    hi: "<strong>Kainchi</strong> → Sharp tailor's snip-snip <em>Kainchi</em> cutting fabric!"
  },
  884: { // HAMMER
    es: "<strong>Martillo</strong> → Strikes down with fierce <em>Martial</em> force like a blacksmith!",
    hi: "<strong>Hathoda</strong> → Heavy iron <em>Haath</em> (hand) tool that drives nails deep!"
  },
  885: { // NAIL
    es: "<strong>Clavo</strong> → Digs like a sharp steel <em>Claw</em> into wooden planks!",
    hi: "<strong>Keel</strong> → Iron <em>Keel</em> hammered firmly into the wall to hang pictures!"
  },
  886: { // SCREW
    es: "<strong>Tornillo</strong> → Spirals round and round like a mini <em>Tornado</em> into wood!",
    hi: "<strong>Pench</strong> → Threaded metal <em>Pench</em> fastened tightly into place!"
  },
  887: { // SCREWDRIVER
    es: "<strong>Destornillador</strong> → Tool that turns the spiral tornado screw in and out!",
    hi: "<strong>Pechkas</strong> → Magnetic tip screwdriver: <em>Pechkas</em>!"
  },
  888: { // ROPE
    es: "<strong>Cuerda</strong> → Strong heavy braided <em>Cord</em> that ties cargo securely!",
    hi: "<strong>Rassi</strong> → Strong jute or nylon braided <em>Rassi</em>!"
  },
  889: { // STRING
    es: "<strong>Hilo</strong> → <em>He-low</em> / Thin kite thread hanging low!",
    hi: "<strong>Dhaaga</strong> → Cotton needle thread / kite <em>Dhaaga</em>!"
  },
  890: { // GLUE
    es: "<strong>Pegamento</strong> → <em>Pegs</em> and sticks two paper sheets permanently together!",
    hi: "<strong>Gond / Fevicol</strong> → Strong adhesive glue: <em>Gond</em>!"
  },
  891: { // CLOTHES
    es: "<strong>Ropa</strong> → Wardrobe filled with royal <em>Robes</em> and dresses!",
    hi: "<strong>Kapde</strong> → Freshly ironed cotton <em>Kapde</em> hanging in wardrobe!"
  },
  892: { // CLOTHING
    es: "<strong>Ropa</strong> → Apparel and clothing collection!",
    hi: "<strong>Kapde</strong> → Everyday comfortable casual <em>Kapde</em>!"
  },
  893: { // SHIRT
    es: "<strong>Camisa</strong> → Exact match with traditional Indian <em>Qameez</em> (Kurta-Qameez)!",
    hi: "<strong>Qameez / Shirt</strong> → Crisp formal collared button-up <em>Qameez / Shirt</em>!"
  },
  894: { // PANTS
    es: "<strong>Pantalón</strong> → Direct phonetic match with English <em>Pants</em>: Pant-alon!",
    hi: "<strong>Pant</strong> → Tailored formal trousers / everyday <em>Pant</em>!"
  },
  895: { // JEANS
    es: "<strong>Vaqueros / Jeans</strong> → Rugged denim jeans worn by cowboys ('vaqueros')!",
    hi: "<strong>Jeans</strong> → Classic rugged blue denim <em>Jeans</em>!"
  },
  896: { // SHORTS
    es: "<strong>Pantalones cortos</strong> → Literally 'short pants'!",
    hi: "<strong>Shorts</strong> → Casual summer sports <em>Shorts</em>!"
  },
  897: { // BLOUSE
    es: "<strong>Blusa</strong> → Direct sound match with English <em>Blouse</em>-a!",
    hi: "<strong>Blouse</strong> → Traditional embroidered saree <em>Blouse</em>!"
  },
  898: { // SKIRT
    es: "<strong>Falda</strong> → Pretty pleated skirt with gentle swinging <em>Folds</em>!",
    hi: "<strong>Skirt</strong> → School uniform or festive flared <em>Skirt</em>!"
  },
  899: { // SUIT
    es: "<strong>Traje</strong> → Formal gentleman's 3-piece <em>Attire</em> for weddings!",
    hi: "<strong>Suit</strong> → Elegant formal coat and pant <em>Suit</em>!"
  },
  900: { // JACKET
    es: "<strong>Chaqueta</strong> → Direct sound match with <em>Jacket</em>-a!",
    hi: "<strong>Jacket</strong> → Warm zip-up winter <em>Jacket</em>!"
  },
  901: { // COAT
    es: "<strong>Abrigo</strong> → Wraps you up cozy to block <em>biting cold</em> winds!",
    hi: "<strong>Coat</strong> → Heavy winter overcoat / blazer <em>Coat</em>!"
  },
  902: { // SWEATER
    es: "<strong>Suéter</strong> → Direct phonetic match with English <em>Sweater</em>!",
    hi: "<strong>Sweater</strong> → Knitted warm woolen <em>Sweater</em>!"
  },
  903: { // VEST
    es: "<strong>Chaleco</strong> → Sleeveless Nehru vest worn over a kurta!",
    hi: "<strong>Baniyan / Vest</strong> → Inner cotton <em>Baniyan</em> or formal waist vest!"
  },
  904: { // UNIFORM
    es: "<strong>Uniforme</strong> → Direct match with English <em>Uniform</em>!",
    hi: "<strong>Vardi / Uniform</strong> → Smart school and police <em>Vardi / Uniform</em>!"
  },
  905: { // UNDERWEAR
    es: "<strong>Ropa interior</strong> → Literally 'interior clothes' worn inside!",
    hi: "<strong>Underwear</strong> → Breathable cotton <em>Underwear</em>!"
  },
  906: { // SOCK
    es: "<strong>Calcetín</strong> → Keeps your ankle and heel bones warm inside shoes!",
    hi: "<strong>Moza</strong> → Pair of warm cotton <em>Moze</em> worn with school shoes!"
  },
  907: { // SHOE
    es: "<strong>Zapato</strong> → <em>Zap</em> your feet into leather shoes and run out!",
    hi: "<strong>Joota</strong> → 'Joota pehan ke bahar jao' / Polished leather footwear!"
  },
  908: { // BOOT
    es: "<strong>Bota</strong> → Direct sound match with English <em>Boot</em>-a!",
    hi: "<strong>Boot</strong> → Rugged high-ankle leather trekking <em>Boot</em>!"
  },
  909: { // SANDAL
    es: "<strong>Sandalia</strong> → Direct sound match with <em>Sandal</em>!",
    hi: "<strong>Chappal / Sandal</strong> → Comfortable breezy summer <em>Sandal</em>!"
  },
  910: { // SLIPPER
    es: "<strong>Pantufla</strong> → Soft fluffy indoor foam slippers!",
    hi: "<strong>Chappal</strong> → Daily indoor rubber Hawaii <em>Chappal</em>!"
  },
  911: { // HAT
    es: "<strong>Sombrero</strong> → <em>Sombra</em> means shade in Spanish. Hat brim provides cool shade from sun!",
    hi: "<strong>Topi</strong> → Wide-brim sun protection <em>Topi</em>!"
  },
  912: { // CAP
    es: "<strong>Gorra</strong> → Snug baseball cap with curved sun visor!",
    hi: "<strong>Cap / Topi</strong> → Sporty cricket batting <em>Cap</em>!"
  },
  913: { // BELT
    es: "<strong>Cinturón</strong> → <em>Cinches</em> firmly around your waist to hold pants up!",
    hi: "<strong>Belt</strong> → Leather buckle <em>Belt</em> fastened around waist!"
  },
  914: { // RIBBON
    es: "<strong>Cinta</strong> → Decorative colorful silk gift tape / hair ribbon!",
    hi: "<strong>Ribbon</strong> → Satin gift packaging and hair braid <em>Ribbon</em>!"
  },
  915: { // SCARF
    es: "<strong>Bufanda</strong> → Wraps round neck to <em>buff</em> away freezing winter gusts!",
    hi: "<strong>Scarf / Mafflar</strong> → Woolen neck <em>Scarf</em> during winter chill!"
  },
  916: { // GLOVE
    es: "<strong>Guante</strong> → Armor <em>Gauntlet</em> guarding your fingers against snow or heat!",
    hi: "<strong>Dastaana</strong> → Woolen hand warmers: <em>Dastaane</em>!"
  },
  917: { // POCKET
    es: "<strong>Bolsillo</strong> → <em>Bolsa</em> (mini bag) stitched right inside your jeans!",
    hi: "<strong>Jeb</strong> → 'Jeb me hath daalo' / Pants wallet pocket!"
  },
  918: { // BUTTON
    es: "<strong>Botón</strong> → Direct sound match with English <em>Button</em>!",
    hi: "<strong>Button</strong> → Fasten the front shirt <em>Button</em>!"
  },
  919: { // ZIPPER
    es: "<strong>Cremallera</strong> → Smooth gliding teeth fastener zipping up your jacket!",
    hi: "<strong>Chain / Zip</strong> → Pull up the jacket metal <em>Chain / Zip</em>!"
  },
  920: { // SLEEVE
    es: "<strong>Manga</strong> → Arm covering cloth sleeve (roll up your sleeves)!",
    hi: "<strong>Aasteen</strong> → Roll up the shirt <em>Aasteen</em> to get to work!"
  },
  921: { // COLLAR
    es: "<strong>Cuello</strong> → Stiff neck collar framing your dress shirt!",
    hi: "<strong>Collar</strong> → Crisp ironed shirt <em>Collar</em>!"
  },
  922: { // BAG
    es: "<strong>Bolsa</strong> → Large reusable shopping / tote carry bag!",
    hi: "<strong>Thaila / Bag</strong> → Cotton grocery shopping <em>Thaila / Bag</em>!"
  },
  923: { // PURSE
    es: "<strong>Bolso</strong> → Elegant leather shoulder hand purse!",
    hi: "<strong>Purse</strong> → Lady's elegant zipper hand <em>Purse</em>!"
  },
  924: { // WALLET
    es: "<strong>Cartera</strong> → Filled with credit <em>Cards</em> and currency notes!",
    hi: "<strong>Wallet</strong> → Leather back-pocket money <em>Wallet</em>!"
  },
  925: { // BACKPACK
    es: "<strong>Mochila</strong> → Carries <em>much load</em> comfortably on your back!",
    hi: "<strong>Backpack / Basta</strong> → Heavy school and college laptop <em>Backpack</em>!"
  },
  926: { // SUITCASE
    es: "<strong>Maleta</strong> → Roller luggage packed for international vacation!",
    hi: "<strong>Suitcase / Peti</strong> → Four-wheel roller airport travel <em>Suitcase</em>!"
  },
  927: { // UMBRELLA
    es: "<strong>Paraguas</strong> → <em>Para</em> (Stop) + <em>Aguas</em> (Water)! Blocks rain showers!",
    hi: "<strong>Chhaata</strong> → <em>Chhat</em> (roof) over your head during heavy monsoon rain!"
  },
  928: { // JEWELRY
    es: "<strong>Joyas</strong> → Precious gold jewels that bring sparkling <em>Joy</em>!",
    hi: "<strong>Gehne / Zewar</strong> → Traditional Indian wedding gold <em>Gehne</em>!"
  },
  929: { // GLASSES
    es: "<strong>Gafas</strong> → Spectacles to <em>gawk</em> and read crisp text clearly!",
    hi: "<strong>Chashma</strong> → Reading <em>Chashma</em> for crystal clear 20/20 vision!"
  },
  930: { // SUNGLASSES
    es: "<strong>Gafas de sol</strong> → UV protection sunglasses for bright sunny days!",
    hi: "<strong>Dhoop ka Chashma</strong> → Cool black aviator sunglasses for hot summer days!"
  },
  931: { // RING
    es: "<strong>Anillo</strong> → Circular <em>Annulus</em> ring slipped onto wedding finger!",
    hi: "<strong>Angoothi</strong> → Diamond and gold engagement <em>Angoothi</em>!"
  },
  932: { // NECKLACE
    es: "<strong>Collar</strong> → Precious gem necklace draped around the neck!",
    hi: "<strong>Haar</strong> → Royal bridal gold and pearl <em>Haar</em>!"
  },
  933: { // EARRING
    es: "<strong>Pendiente</strong> → Sparkling jewel <em>pendant</em> dangling from the earlobe!",
    hi: "<strong>Jhumka</strong> → Traditional dancing <em>Jhumka</em> shining bright!"
  },
  934: { // BRACELET
    es: "<strong>Pulsera</strong> → Worn on the wrist right where your <em>Pulse</em> beats!",
    hi: "<strong>Kangan</strong> → Golden wedding bangle / wrist <em>Kangan</em>!"
  },
  935: { // TRANSPORT
    es: "<strong>Transporte</strong> → Direct match with English <em>Transport</em>!",
    hi: "<strong>Parivahan</strong> → Public bus and metro transit network: <em>Parivahan</em>!"
  },
  936: { // VEHICLE
    es: "<strong>Vehículo</strong> → Direct match with English <em>Vehicle</em>!",
    hi: "<strong>Gaadi</strong> → Any wheeled automobile / motor <em>Gaadi</em>!"
  },
  937: { // CAR
    es: "<strong>Coche / Auto</strong> → Sounds like four-wheel horse <em>Coach / Auto</em>!",
    hi: "<strong>Car / Gaadi</strong> → 'Car start karo' / Four-wheel family motor car!"
  },
  938: { // BICYCLE
    es: "<strong>Bicicleta</strong> → Direct match with English <em>Bicycle</em>!",
    hi: "<strong>Cycle</strong> → Two-wheeler pedal <em>Cycle</em> for evening rides!"
  },
  939: { // SCOOTER
    es: "<strong>Patinete / Scooter</strong> → Two-wheel twist-and-go motor scooter!",
    hi: "<strong>Scooter</strong> → Classic Bajaj or Activa family <em>Scooter</em>!"
  },
  940: { // MOTORCYCLE
    es: "<strong>Motocicleta</strong> → Direct match with English <em>Motorcycle</em>!",
    hi: "<strong>Motorcycle / Bike</strong> → Geared road-cruiser <em>Bike</em>!"
  },
  941: { // BUS
    es: "<strong>Autobús</strong> → Direct match with English <em>Bus</em>!",
    hi: "<strong>Bus</strong> → City public transit red double-decker <em>Bus</em>!"
  },
  942: { // TRAIN
    es: "<strong>Tren</strong> → Exact match with English <em>Train</em>: Tren!",
    hi: "<strong>Railgaadi</strong> → Legendary 'Railgaadi chuk chuk chuk chuk'!"
  },
  943: { // TRUCK
    es: "<strong>Camión</strong> → Heavy 18-wheel cargo transport lorry!",
    hi: "<strong>Truck / Lorry</strong> → National highway cargo hauler <em>Truck</em>!"
  },
  944: { // VAN
    es: "<strong>Furgoneta</strong> → Boxy passenger and goods delivery van!",
    hi: "<strong>Van / Omni</strong> → School children transport <em>Van</em>!"
  },
  945: { // TAXI
    es: "<strong>Taxi</strong> → Worldwide universal word: <em>Taxi</em>!",
    hi: "<strong>Taxi / Cab</strong> → Yellow-and-black city meter <em>Taxi</em>!"
  },
  946: { // SUBWAY
    es: "<strong>Metro</strong> → Underground rapid transit railway: <em>Metro</em>!",
    hi: "<strong>Metro</strong> → Air-conditioned fast underground <em>Metro</em> train!"
  },
  947: { // AIRPLANE
    es: "<strong>Avión</strong> → <em>Aviation</em> / High-speed metal bird soaring in the clouds!",
    hi: "<strong>Hawai Jahaaz</strong> → Giant silver bird cruising through the <em>Hawa</em> (air)!"
  },
  948: { // HELICOPTER
    es: "<strong>Helicóptero</strong> → Direct match with English <em>Helicopter</em>!",
    hi: "<strong>Helicopter</strong> → Whirring overhead rotor blade <em>Helicopter</em>!"
  },
  949: { // BOAT
    es: "<strong>Barco</strong> → Floats like buoyant wooden <em>Bark</em> across river ripples!",
    hi: "<strong>Naav</strong> → Wooden rowboat gliding smoothly across the lake: <em>Naav</em>!"
  },
  950: { // SHIP
    es: "<strong>Barco</strong> → Massive ocean liner crossing rough sea waves!",
    hi: "<strong>Jahaaz</strong> → Huge multi-deck ocean cargo <em>Samundari Jahaaz</em>!"
  },
  951: { // FERRY
    es: "<strong>Ferry</strong> → Passenger ferry shuttling vehicles across the river bay!",
    hi: "<strong>Ferry</strong> → Island hopping boat transport: <em>Ferry</em>!"
  },
  954: { // WHEEL
    es: "<strong>Rueda</strong> → <em>Roll</em>-da / Round circular disc that rolls smoothly!",
    hi: "<strong>Pahiya</strong> → Rotating rubber and alloy car <em>Pahiya</em>!"
  },
  955: { // TIRE
    es: "<strong>Neumático</strong> → <em>Pneumatic</em> heavy rubber tire pressurized with air!",
    hi: "<strong>Tyre</strong> → Puncture-resistant tubeless road <em>Tyre</em>!"
  },
  956: { // BRAKE
    es: "<strong>Freno</strong> → Stops crazy highway <em>frenzy</em> dead in its tracks!",
    hi: "<strong>Brake</strong> → Press the foot <em>Brake</em> pedal to bring car to immediate stop!"
  },
  957: { // SEAT
    es: "<strong>Asiento</strong> → Place to <em>Sit</em> comfortably in the car!",
    hi: "<strong>Seat</strong> → Cushioned ergonomic passenger <em>Seat</em>!"
  },
  958: { // SEATBELT
    es: "<strong>Cinturón de seguridad</strong> → Security belt clicked across your chest!",
    hi: "<strong>Seatbelt</strong> → 'Seatbelt pehno' for highway road safety!"
  },
  959: { // FUEL
    es: "<strong>Combustible</strong> → High-octane <em>Combustion</em> liquid that powers engines!",
    hi: "<strong>Eendhan / Fuel</strong> → Car engine fuel: <em>Eendhan</em>!"
  },
  960: { // PETROL
    es: "<strong>Gasolina</strong> → Direct match with <em>Gasoline</em> / Petrol!",
    hi: "<strong>Petrol</strong> → 'Tanki full karo' at the local <em>Petrol</em> pump!"
  },
  961: { // TRAFFIC
    es: "<strong>Tráfico</strong> → Direct match with English <em>Traffic</em>!",
    hi: "<strong>Traffic</strong> → Red signal junction bumper-to-bumper <em>Traffic</em> jam!"
  },
  962: { // STREET
    es: "<strong>Calle (Kaye)</strong> → City street lined with shops and colorful sidewalks!",
    hi: "<strong>Gali / Sadak</strong> → Busy neighborhood market <em>Gali / Sadak</em>!"
  },
  963: { // ROAD
    es: "<strong>Carretera</strong> → Wide asphalt highway paved for speeding cars!",
    hi: "<strong>Sadak</strong> → Smooth tarred motor vehicle <em>Sadak</em>!"
  },
  964: { // HIGHWAY
    es: "<strong>Autopista</strong> → Multi-lane high speed expressway / <em>Autobahn</em>!",
    hi: "<strong>Highway</strong> → Six-lane toll express <em>Highway</em>!"
  },
  965: { // PATH
    es: "<strong>Camino</strong> → Peaceful walking trail through green trees!",
    hi: "<strong>Raasta</strong> → 'Sahi <em>Raasta</em> chuno' / Footpath through forest!"
  },
  966: { // PAVEMENT
    es: "<strong>Acera</strong> → Elevated pedestrian sidewalk safe from road traffic!",
    hi: "<strong>Footpath</strong> → Pedestrian walking path: <em>Footpath</em>!"
  },
  967: { // BRIDGE
    es: "<strong>Puente</strong> → Connects <em>Point A</em> to <em>Point B</em> over deep river waters!",
    hi: "<strong>Pul</strong> → Cross over the roaring river via the suspension <em>Pul</em>!"
  },
  968: { // TUNNEL
    es: "<strong>Túnel</strong> → Direct match with English <em>Tunnel</em>!",
    hi: "<strong>Surang / Tunnel</strong> → Mountain passage railway <em>Surang / Tunnel</em>!"
  },
  969: { // CORNER
    es: "<strong>Esquina</strong> → Sharp 90-degree square corner of intersecting streets!",
    hi: "<strong>Kona</strong> → 'Sadak ke <em>Kone</em> par milte hain' / Street corner!"
  },
  970: { // INTERSECTION
    es: "<strong>Intersección</strong> → Direct match with <em>Intersection</em>!",
    hi: "<strong>Chauraaha</strong> → <em>Chau</em> (four) roads meeting in the middle: <em>Chauraaha</em>!"
  },
  971: { // STATION
    es: "<strong>Estación</strong> → Direct match with <em>Station</em>!",
    hi: "<strong>Station</strong> → Railway passenger transit hub: <em>Station</em>!"
  },
  972: { // AIRPORT
    es: "<strong>Aeropuerto</strong> → Direct match with <em>Aero-Port / Airport</em>!",
    hi: "<strong>Hawai Adda / Airport</strong> → International flights departure terminal!"
  },
  973: { // PORT
    es: "<strong>Puerto</strong> → Sea harbor where massive container ships dock!",
    hi: "<strong>Bandargaah</strong> → Ocean container cargo terminal: <em>Bandargaah</em>!"
  },
  974: { // HARBOR
    es: "<strong>Puerto</strong> → Natural sheltered bay protecting docked ships from storm waves!",
    hi: "<strong>Bandargaah</strong> → Sheltered sea vessel docking bay!"
  },
  975: { // PARKING
    es: "<strong>Estacionamiento</strong> → Designated area for stationing parked vehicles!",
    hi: "<strong>Parking</strong> → Basement vehicle <em>Parking</em> lot!"
  },
  976: { // JUNCTION
    es: "<strong>Cruce</strong> → Road crossway where two highway routes cross!",
    hi: "<strong>Junction</strong> → Busy railway or road crossing <em>Junction</em>!"
  },
  977: { // TRACK
    es: "<strong>Vía</strong> → Steel railway tracks stretching to the horizon!",
    hi: "<strong>Patri</strong> → Steel train rail: 'Rail ki <em>Patri</em>'!"
  },
  978: { // SIGN
    es: "<strong>Señal</strong> → High-visibility road directional <em>Signal</em> signboard!",
    hi: "<strong>Signboard</strong> → Highway speed limit & distance <em>Signboard</em>!"
  },
  979: { // TICKET
    es: "<strong>Billete</strong> → Train and movie travel admission <em>Bill / Ticket</em>!",
    hi: "<strong>Ticket</strong> → Train and cinema entrance pass: <em>Ticket</em>!"
  },
  980: { // PASSPORT
    es: "<strong>Pasaporte</strong> → Direct match with international <em>Passport</em>!",
    hi: "<strong>Passport</strong> → Official blue international travel booklet: <em>Passport</em>!"
  },
  981: { // CITY
    es: "<strong>Ciudad</strong> → Skyscraper-filled metropolitan <em>City</em>!",
    hi: "<strong>Shahar</strong> → Bustling bright lights metropolitan <em>Shahar</em>!"
  },
  982: { // TOWN
    es: "<strong>Pueblo</strong> → Charming historic settlement with tight-knit community!",
    hi: "<strong>Kasba</strong> → Cozy semi-urban market settlement: <em>Kasba</em>!"
  },
  983: { // VILLAGE
    es: "<strong>Aldea</strong> → Peaceful rural village surrounded by green paddy fields!",
    hi: "<strong>Gaaon</strong> → Quiet fresh-air countryside village: <em>Gaaon</em>!"
  },
  984: { // COUNTRY
    es: "<strong>País</strong> → Sovereign nation with its own flag and constitution!",
    hi: "<strong>Desh</strong> → 'Mera pyara <em>Desh</em>' / Nation and homeland!"
  },
  985: { // CENTER
    es: "<strong>Centro</strong> → Central hub / downtown <em>Center</em>!",
    hi: "<strong>Kendra</strong> → City downtown or community gathering <em>Kendra</em>!"
  },
  986: { // BUILDING
    es: "<strong>Edificio</strong> → Impressive multi-story architectural <em>Edifice</em>!",
    hi: "<strong>Imaarat</strong> → Tall towering concrete <em>Imaarat / Building</em>!"
  },
  987: { // SCHOOL
    es: "<strong>Escuela</strong> → Direct sound match with English <em>School</em>!",
    hi: "<strong>School</strong> → Morning bell and classroom learning at <em>School</em>!"
  },
  988: { // COLLEGE
    es: "<strong>Colegio</strong> → Higher education university campus / <em>College</em>!",
    hi: "<strong>College</strong> → Graduation degree campus: <em>College</em>!"
  },
  989: { // UNIVERSITY
    es: "<strong>Universidad</strong> → Direct match with <em>University</em>!",
    hi: "<strong>Vishwavidyalaya</strong> → Prestigious academic <em>University</em> campus!"
  },
  990: { // LIBRARY
    es: "<strong>Biblioteca</strong> → Home of thousands of bound books and quiet study tables!",
    hi: "<strong>Pustakaalaya / Library</strong> → Silent reading room full of books: <em>Library</em>!"
  },
  991: { // MUSEUM
    es: "<strong>Museo</strong> → Direct match with English <em>Museum</em>!",
    hi: "<strong>Ajoobaghar / Museum</strong> → Historic artifacts and dinosaur fossil <em>Museum</em>!"
  },
  992: { // THEATER
    es: "<strong>Teatro</strong> → Live stage performance and dramatic <em>Theater</em>!",
    hi: "<strong>Natak Ghar / Theater</strong> → Live Broadway and drama stage <em>Theater</em>!"
  },
  993: { // CINEMA
    es: "<strong>Cine</strong> → Direct match with <em>Cinema / Movie Theater</em>!",
    hi: "<strong>Cinema Hall</strong> → Giant 70mm movie screen with tub of popcorn: <em>Cinema</em>!"
  },
  994: { // STORE
    es: "<strong>Tienda</strong> → Market shopping boutique / retail store!",
    hi: "<strong>Dukaan</strong> → Neighborhood grocery and general store: <em>Dukaan</em>!"
  },
  995: { // BAKERY
    es: "<strong>Panadería</strong> → 'Pan' means bread in Spanish (like Mumbai Pav!). Fresh bread shop!",
    hi: "<strong>Bakery</strong> → Freshly baked sourdough loaves, cakes and cookies: <em>Bakery</em>!"
  },
  996: { // MARKET
    es: "<strong>Mercado</strong> → Direct match with English <em>Market</em>!",
    hi: "<strong>Bazaar</strong> → Colorful bustling fruit and vegetable <em>Bazaar</em>!"
  },
  997: { // SUPERMARKET
    es: "<strong>Supermercado</strong> → Giant grocery market with shopping carts!",
    hi: "<strong>Supermarket</strong> → Multi-aisle grocery department store: <em>Supermarket</em>!"
  },
  998: { // RESTAURANT
    es: "<strong>Restaurante</strong> → Direct match with <em>Restaurant</em>!",
    hi: "<strong>Restaurant</strong> → Fine dining family dinner at favorite <em>Restaurant</em>!"
  },
  999: { // CAFE
    es: "<strong>Cafetería</strong> → Direct match with <em>Cafe / Coffee shop</em>!",
    hi: "<strong>Cafe</strong> → Cozy coffee shop with hot espresso and croissants: <em>Cafe</em>!"
  },
  1000: { // BANK
    es: "<strong>Banco</strong> → Direct match with English <em>Bank</em>!",
    hi: "<strong>Bank</strong> → Financial institution with cash vault and ATMs: <em>Bank</em>!"
  }
};

console.log('Shortcuts count:', Object.keys(shortcuts).length);
fs.writeFileSync('scripts/shortcuts_data.json', JSON.stringify(shortcuts, null, 2));
