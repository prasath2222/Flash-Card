import json

# Exact 800-1000 phonetic sound-alike + Tamil bridge restorations for the 108 cards in 201-1000
RESTORE_MAP = {
    # tier201DeckCards
    225: (
        "swipe karna", "स्वाइप करना",
        '<strong>Deslizar (Des-lee-sar)</strong> ≈ Sounds like <strong>"Desk-Slide-Far"</strong> → Slide your finger across the screen to <em>Swipe (Deslizar)</em>!',
        '<strong>Swipe karna (स्वाइप करना)</strong> ≈ 100% identical to spoken Tamil <strong>ஸ்வைப் (Swipe)</strong> & English <strong>"Swipe"</strong>!'
    ),
    292: (
        "minute", "मिनट",
        None,
        '<strong>Minute (मिनट)</strong> ≈ 100% identical to spoken Tamil <strong>மினிட் (Minute)</strong> & English <strong>"Minute"</strong>!'
    ),
    302: (
        "weekend", "वीकेंड",
        None,
        '<strong>Weekend (वीकेंड)</strong> ≈ 100% identical to spoken Tamil <strong>வீக்கெண்ட் (Weekend)</strong> & English <strong>"Weekend"</strong>!'
    ),
    319: (
        "calendar", "कैलेंडर",
        None,
        '<strong>Calendar (कैलेंडर)</strong> ≈ 100% identical to Tamil <strong>காலண்டர் (Calendar)</strong> & English <strong>"Calendar"</strong>!'
    ),
    # tier601DeckCards
    655: (
        "neta / leader", "नेता / लीडर",
        '<strong>Líder (Lee-der)</strong> ≈ Sounds 100% identical to English <strong>"Leader"</strong> & spoken Tamil <strong>லீடர் (Leader)</strong>!',
        None
    ),
    716: (
        "doctor", "डॉक्टर",
        '<strong>Médico / Doctor (Meh-dee-koh)</strong> ≈ Direct match with English <strong>"Medical / Doctor"</strong> & Tamil <strong>டாக்டர் (Doctor)</strong>!',
        '<strong>Doctor (डॉक्टर)</strong> ≈ 100% identical to spoken Tamil <strong>டாக்டர் (Doctor)</strong> & English <strong>"Doctor"</strong>!'
    ),
    717: (
        "nurse", "नर्स",
        '<strong>Enfermero / Enfermera (En-fer-meh-roh)</strong> ≈ Sounds like <strong>"In-Firmary" (Infirmary care)</strong> → Hospital <em>Nurse (Enfermera)</em>!',
        '<strong>Nurse (नर्स)</strong> ≈ 100% identical to spoken Tamil <strong>நர்ஸ் (Nurse)</strong> & English <strong>"Nurse"</strong>!'
    ),
    730: (
        "coffee", "कॉफ़ी",
        None,
        '<strong>Coffee (कॉफ़ी)</strong> ≈ 100% identical to Tamil <strong>காபி (Kaapi / Coffee)</strong> & English <strong>"Coffee"</strong>!'
    ),
    738: (
        "pasta", "पास्ता",
        None,
        '<strong>Pasta (पास्ता)</strong> ≈ 100% identical to Tamil <strong>பாஸ்தா (Pasta)</strong> & English <strong>"Pasta"</strong>!'
    ),
    754: (
        "sandwich", "सैंडविच",
        None,
        '<strong>Sandwich (सैंडविच)</strong> ≈ 100% identical to Tamil <strong>சாண்ட்விச் (Sandwich)</strong> & English <strong>"Sandwich"</strong>!'
    ),
    755: (
        "cake", "केक",
        None,
        '<strong>Cake (केक)</strong> ≈ 100% identical to Tamil <strong>கேக் (Cake)</strong> & English <strong>"Cake"</strong>!'
    ),
    757: (
        "chocolate", "चॉकलेट",
        None,
        '<strong>Chocolate (चॉकलेट)</strong> ≈ 100% identical to Tamil <strong>சாக்லேட் (Chocolate)</strong> & English <strong>"Chocolate"</strong>!'
    ),
    767: (
        "strawberry", "स्ट्रॉबेरी",
        None,
        '<strong>Strawberry (स्ट्रॉबेरी)</strong> ≈ 100% identical to Tamil <strong>ஸ்ட்ராபெர்ரி (Strawberry)</strong> & English <strong>"Strawberry"</strong>!'
    ),
    788: (
        "mug / bada cup", "मग / बड़ा कप",
        None,
        '<strong>Mug / Bada Cup (मग)</strong> ≈ 100% identical to spoken Tamil <strong>மக் / கப் (Mug / Cup)</strong> & English <strong>"Mug"</strong>!'
    ),
    # initialDeckCards (800-1000)
    802: (
        "sink", "सिंक",
        '<strong>Fregadero (Freh-gah-deh-roh)</strong> ≈ Sounds like <strong>"Free-Gutter-o"</strong> → Wash dishes in the <em>Sink</em> so water drains down the <em>gutter (Fregadero)</em>!',
        '<strong>Sink (सिंक)</strong> ≈ 100% identical to spoken Tamil <strong>சிங்க் (Sink)</strong> & English <strong>"Sink"</strong>!'
    ),
    804: (
        "sponge / foam", "स्पंज / फ़ोम",
        '<strong>Esponja (Es-pon-hah)</strong> ≈ English <strong>"Sponge"</strong> + <strong>Tamil பஞ்சு (Panju)</strong> → Contains both English <em>Sponge</em> & Tamil <em>Panju (பஞ்சு)</em>!',
        '<strong>Sponge (स्पंज)</strong> ≈ <strong>Tamil பஞ்சு (Panju)</strong> + English <strong>"Sponge"</strong> → Drop the <em>"S"</em> from <em>Sponge</em> and you hear Tamil <em>Panju (பஞ்சு)</em>!'
    ),
    805: (
        "apron", "एप्रन",
        '<strong>Delantal (Deh-lan-tal)</strong> ≈ From <em>Delante</em> (In front) + <strong>Tamil தாளி (Thaali)</strong> → Tied in front while <em>thaalichifying</em> curry = <em>Delantal (Apron)</em>!',
        '<strong>Apron (एप्रन)</strong> ≈ 100% identical to spoken Tamil <strong>ஏப்ரன் (Apron)</strong> & English <strong>"Apron"</strong>!'
    ),
    807: (
        "menu", "मेनू",
        '<strong>Menú (Meh-noo)</strong> ≈ Direct match with English & spoken Tamil <strong>"Menu (மெனு)"</strong> → 100% identical!',
        '<strong>Menu (मेनू)</strong> ≈ Direct match with spoken Tamil <strong>மெனு (Menu)</strong> & English <strong>"Menu"</strong>!'
    ),
    811: (
        "bedroom / sone ka kamra", "बेडरूम / सोने का कमरा",
        '<strong>Dormitorio (Dor-mee-toh-ryoh)</strong> ≈ English <strong>"Dormitory"</strong> → A college <em>Dormitory</em> is a sleeping <em>Bedroom (Dormitorio)</em>!',
        '<strong>Bedroom / Sone ka kamra</strong> ≈ <strong>Spoken Tamil பெட்ரூம் (Bedroom)</strong> or <strong>Sona (Sleep) + Kamra (Room)</strong>!'
    ),
    812: (
        "bathroom", "बाथरूम",
        '<strong>Baño (Bah-nyoh)</strong> ≈ Sounds like <strong>"Bath-Now"</strong> + <strong>Tamil பானை (Paanai - water pot)</strong> → Pour water and bathe in the <em>Baño (Bathroom)</em>!',
        '<strong>Bathroom (बाथरूम)</strong> ≈ 100% identical to spoken Tamil <strong>பாத்ரூம் (Bathroom)</strong> & English <strong>"Bathroom"</strong>!'
    ),
    813: (
        "living room / baithak", "बैठक / हॉल",
        '<strong>Sala de estar (Sah-lah deh es-tar)</strong> ≈ <strong>Tamil சாலை / ஹால் (Saalai - hall) + "Stay"</strong> → The front hall where you <em>stay & relax</em> is the <em>Living Room (Sala de estar)</em>!',
        '<strong>Baithak / Hall (बैठक)</strong> ≈ From <strong>Baithna (Sit)</strong> + <strong>Tamil ஹால் (Hall)</strong> → Front room where guests sit = <em>Baithak (Living Room)</em>!'
    ),
    814: (
        "dining room", "डाइनिंग रूम",
        '<strong>Comedor (Koh-meh-dor)</strong> ≈ Sounds like <strong>"Come-Eat-Door"</strong> → Walk through the door and <em>come eat</em> in the <em>Comedor (Dining Room)</em>!',
        '<strong>Dining Room (डाइनिंग रूम)</strong> ≈ 100% identical to spoken Tamil <strong>டைனிங் ரூம் (Dining Room)</strong> & English!'
    ),
    817: (
        "galiyara / corridor", "गलियारा / कॉरिडोर",
        '<strong>Corredor (Koh-reh-dor)</strong> ≈ Sounds 100% like English <strong>"Corridor"</strong> → Walk straight down the <em>Corredor (Corridor)</em>!',
        '<strong>Galiyara / Corridor (गलियारा)</strong> ≈ <strong>Gali (Lane) + Yaara</strong> + spoken Tamil <strong>காரிடார் (Corridor)</strong>!'
    ),
    827: (
        "garage", "गैराज",
        '<strong>Garaje (Gah-rah-heh)</strong> ≈ Direct match with English <strong>"Garage"</strong> & spoken Tamil <strong>கேரேஜ் (Garage)</strong>!',
        '<strong>Garage (गैराज)</strong> ≈ 100% identical to spoken Tamil <strong>கேரேஜ் (Garage)</strong> & English <strong>"Garage"</strong>!'
    ),
    828: (
        "balcony / chhajja", "बालकनी / छज्जा",
        '<strong>Balcón (Bal-kon)</strong> ≈ Direct match with English <strong>"Balcony"</strong> & Tamil <strong>பால்கனி (Balcony)</strong>!',
        '<strong>Balcony / Chhajja (छज्जा)</strong> ≈ <strong>Tamil பால்கனி (Balcony)</strong> + <strong>Chhat (Roofledge = Chhajja)</strong>!'
    ),
    835: (
        "chimney", "चिमनी",
        '<strong>Chimenea (Chee-meh-neh-ah)</strong> ≈ Direct match with English <strong>"Chimney"</strong> & spoken Tamil <strong>சிம்னி (Chimney)</strong>!',
        '<strong>Chimney (चिमनी)</strong> ≈ 100% identical to spoken Tamil <strong>சிம்னி (Chimney)</strong> & English <strong>"Chimney"</strong>!'
    ),
    839: (
        "sofa", "सोफ़ा",
        '<strong>Sofá (Soh-fah)</strong> ≈ 100% identical to Tamil <strong>சோபா (Sofa)</strong> & English <strong>"Sofa"</strong>!',
        '<strong>Sofa (सोफ़ा)</strong> ≈ 100% identical to Tamil <strong>சோபா (Sofa)</strong> & English <strong>"Sofa"</strong>!'
    ),
    848: (
        "paydan / kaleen", "पायदान / क़ालीन",
        '<strong>Alfombra pequeña (Al-fom-brah peh-keh-nyah)</strong> ≈ <strong>Alfombra ("Foam" carpet) + Pequeña (Small)</strong> → Small foam-soft floor <em>Rug</em>!',
        '<strong>Paydan / Kaleen (पायदान)</strong> ≈ <strong>Paay (Foot/கால்) + Daan (Stand)</strong> → Soft mat under your feet = <em>Paydan (Rug)</em>!'
    ),
    851: (
        "almari / wardrobe", "अलमारी",
        '<strong>Ropero (Roh-peh-roh)</strong> ≈ <strong>Ropa ("Robe" / clothes) + -ero</strong> → Closet where your <em>robes & clothes</em> hang = <em>Ropero (Wardrobe)</em>!',
        '<strong>Almari (अलमारी)</strong> ≈ <strong>Tamil அலமாரி (Alamaari)</strong> → 100% identical word! Tamil <em>Alamaari (அலமாரி)</em> = Hindi <em>Almari (Wardrobe)</em>!'
    ),
    853: (
        "almari / cabinet", "अलमारी / कैबिनेट",
        '<strong>Gabinete (Gah-bee-neh-teh)</strong> ≈ Direct sibling of English <strong>"Cabinet"</strong> (<em>G-abinete ≈ C-abinet</em>)!',
        '<strong>Almari / Cabinet (अलमारी)</strong> ≈ <strong>Tamil அலமாரி (Alamaari)</strong> & English <strong>"Cabinet"</strong>!'
    ),
    855: (
        "rack / taaq", "रैक / ताक़",
        '<strong>Estante (Es-tan-teh)</strong> ≈ Sounds like English <strong>"Stand"</strong> → Books <em>stand</em> on the wall <em>Estante (Shelf)</em>!',
        '<strong>Rack / Taaq (रैक / ताक़)</strong> ≈ <strong>Spoken Tamil ரேக் (Rack)</strong> + <strong>Taaq ("Tuck" items on the shelf)</strong>!'
    ),
    857: (
        "desk / mez", "डेस्क / मेज़",
        '<strong>Escritorio (Es-kree-toh-ryoh)</strong> ≈ English <strong>"Scribe / Script"</strong> → The table where you write a <em>script</em> is an <em>Escritorio (Desk)</em>!',
        '<strong>Desk / Mez (डेस्क / मेज़)</strong> ≈ <strong>Tamil மேசை (Mesai = Mez)</strong> & spoken Tamil <strong>டெஸ்க் (Desk)</strong>!'
    ),
    858: (
        "lamp / batti", "लैंप / बत्ती",
        '<strong>Lámpara (Lam-pah-rah)</strong> ≈ Direct match with English <strong>"Lamp"</strong> (<em>Lámpara ≈ Lamp</em>)!',
        '<strong>Lamp / Batti (लैंप / बत्ती)</strong> ≈ <strong>Tamil வத்தி / விளக்கு (Vatti = Batti)</strong> & English <strong>"Lamp"</strong>!'
    ),
    859: (
        "bulb", "बल्ब",
        '<strong>Bombilla (Bom-bee-yah)</strong> ≈ Sounds like a tiny glowing <strong>"Little Bomb (Bomb-illa)"</strong> of glass light = <em>Bulb (Bombilla)</em>!',
        '<strong>Bulb (बल्ब)</strong> ≈ 100% identical to spoken Tamil <strong>பல்பு (Bulb)</strong> & English <strong>"Bulb"</strong>!'
    ),
    860: (
        "switch / button", "स्विच / बटन",
        '<strong>Interruptor (Een-teh-roop-tor)</strong> ≈ English <strong>"Interrupt"</strong> → Flip the <em>Switch (Interruptor)</em> to <em>interrupt</em> the power flow!',
        '<strong>Switch (स्विच)</strong> ≈ 100% identical to spoken Tamil <strong>சுவிட்ச் (Switch)</strong> & English <strong>"Switch"</strong>!'
    ),
    861: (
        "plug / pin", "प्लग / पिन",
        '<strong>Enchufe (En-choo-feh)</strong> ≈ Sounds like <strong>"In-Shove-It"</strong> → Shove the <em>Plug (Enchufe)</em> into the wall!',
        '<strong>Plug (प्लग)</strong> ≈ 100% identical to spoken Tamil <strong>பிளக் (Plug)</strong> & English <strong>"Plug"</strong>!'
    ),
    862: (
        "socket", "सॉकेट",
        '<strong>Toma de corriente (Toh-mah deh koh-ryen-teh)</strong> ≈ <strong>Toma (Take) + Corriente ("Current")</strong> → Wall point where you take electric <em>current = Socket</em>!',
        '<strong>Socket (सॉकेट)</strong> ≈ 100% identical to spoken Tamil <strong>சாக்கெட் (Socket)</strong> & English <strong>"Socket"</strong>!'
    ),
    871: (
        "soopda / dustpan", "सूपड़ा",
        '<strong>Recogedor (Reh-koh-heh-dor)</strong> ≈ Sounds like <strong>"Re-Collect-Dirt"</strong> → Scoop and collect floor dirt into the <em>Recogedor (Dustpan)</em>!',
        '<strong>Soopda (सूपड़ा)</strong> ≈ <strong>Tamil முறம் / சுளகு + English "Scoop-da"</strong> → <em>Scoop-da</em> trash into the <em>Soopda (Dustpan)</em>!'
    ),
    876: (
        "lighter", "लाइटर",
        '<strong>Encendedor (En-sen-deh-dor)</strong> ≈ English <strong>"Incendiary / Ignite"</strong> → Sparks a flame to ignite = <em>Encendedor (Lighter)</em>!',
        '<strong>Lighter (लाइटर)</strong> ≈ 100% identical to spoken Tamil <strong>லைட்டர் (Lighter)</strong> & English <strong>"Lighter"</strong>!'
    ),
    879: (
        "shampoo", "शैम्पू",
        '<strong>Champú (Cham-poo)</strong> ≈ Sounds 100% identical to English <strong>"Shampoo"</strong> & Tamil <strong>ஷாம்பு (Shampoo)</strong>!',
        '<strong>Shampoo (शैम्पू)</strong> ≈ Comes from Hindi <strong>Champi (Head massage!)</strong> & 100% identical to Tamil <strong>ஷாம்பு</strong>!'
    ),
    880: (
        "toothbrush / daant ka brush", "टूथब्रश",
        '<strong>Cepillo de dientes (Seh-pee-yoh deh dyen-tes)</strong> ≈ <strong>Cepillo ("Sweep-illo" brush) + Dientes ("Dentist" teeth)</strong> → Brush for your teeth = <em>Toothbrush</em>!',
        '<strong>Toothbrush / Daant ka brush</strong> ≈ <strong>Tamil தந்தம் (Dant = Daant) + பிரஷ் (Brush)</strong>!'
    ),
    881: (
        "toothpaste / paste", "टूथपेस्ट / पेस्ट",
        '<strong>Pasta de dientes (Pas-tah deh dyen-tes)</strong> ≈ <strong>Pasta ("Paste") + Dientes ("Dentist" teeth)</strong> → Literally <em>"Paste of teeth" = Toothpaste</em>!',
        '<strong>Paste / Toothpaste (पेस्ट)</strong> ≈ 100% identical to spoken Tamil <strong>பேஸ்ட் (Paste)</strong> & English!'
    ),
    882: (
        "razor / ustura", "रेज़र / उस्तरा",
        '<strong>Maquinilla (Mah-kee-nee-yah)</strong> ≈ Mini <strong>"Machine (Máquina)"</strong> blade for shaving = <em>Maquinilla (Razor)</em>!',
        '<strong>Razor / Ustura (रेज़र / उस्तरा)</strong> ≈ Spoken Tamil <strong>ரேசர் (Razor)</strong> + <strong>"Ultra-Sharp" (Ustura)</strong>!'
    ),
    886: (
        "pech / screw", "पेच / स्क्रू",
        '<strong>Tornillo (Tor-nee-yoh)</strong> ≈ English <strong>"Turn-illo"</strong> → You <em>turn</em> and twist a metal <em>Screw (Tornillo)</em>!',
        '<strong>Pech / Screw (पेच)</strong> ≈ <strong>"Pinch & Twist" (Pech)</strong> + spoken Tamil <strong>ஸ்க்ரூ (Screw)</strong>!'
    ),
    887: (
        "pechkash / screwdriver", "पेचकस",
        '<strong>Destornillador (Des-tor-nee-yah-dor)</strong> ≈ <strong>Des + Tornillo ("Turn-Screw") + -dor</strong> → Tool that turns the <em>Tornillo = Screwdriver</em>!',
        '<strong>Pechkash (पेचकस)</strong> ≈ <strong>Pech (Screw) + Kasna (Tighten)</strong> & spoken Tamil <strong>ஸ்க்ரூடிரைவர்</strong>!'
    ),
    895: (
        "jeans", "जींस",
        None,
        '<strong>Jeans (जींस)</strong> ≈ 100% identical to Tamil <strong>ஜீன்ஸ் (Jeans)</strong> & English <strong>"Jeans"</strong>!'
    ),
    896: (
        "shorts / nikkar", "निक्कर / शॉर्ट्स",
        None,
        '<strong>Shorts / Nikkar (निक्कर)</strong> ≈ 100% identical to spoken Tamil <strong>நிக்கர் / ஷார்ட்ஸ் (Nikkar / Shorts)</strong>!'
    ),
    897: (
        "blouse", "ब्लाउज़",
        None,
        '<strong>Blouse (ब्लाउज़)</strong> ≈ 100% identical to spoken Tamil <strong>பிளவுஸ் (Blouse)</strong> & English <strong>"Blouse"</strong>!'
    ),
    898: (
        "skirt", "स्कर्ट",
        None,
        '<strong>Skirt (स्कर्ट)</strong> ≈ 100% identical to spoken Tamil <strong>ஸ்கர்ட் (Skirt)</strong> & English <strong>"Skirt"</strong>!'
    ),
    899: (
        "suit", "सूट",
        None,
        '<strong>Suit (सूट)</strong> ≈ 100% identical to spoken Tamil <strong>சூட் (Suit)</strong> & English <strong>"Suit"</strong>!'
    ),
    900: (
        "jacket", "जैकेट",
        None,
        '<strong>Jacket (जैकेट)</strong> ≈ 100% identical to spoken Tamil <strong>ஜாக்கெட் (Jacket)</strong> & English <strong>"Jacket"</strong>!'
    ),
    901: (
        "coat", "कोट",
        None,
        '<strong>Coat (कोट)</strong> ≈ 100% identical to spoken Tamil <strong>கோட் (Coat)</strong> & English <strong>"Coat"</strong>!'
    ),
    902: (
        "sweater", "स्वेटर",
        None,
        '<strong>Sweater (स्वेटर)</strong> ≈ 100% identical to spoken Tamil <strong>ஸ்வெட்டர் (Sweater)</strong> & English <strong>"Sweater"</strong>!'
    ),
    903: (
        "baniyaan / vest", "बनियान",
        None,
        '<strong>Baniyaan (बनियान)</strong> ≈ <strong>Spoken Tamil பனியன் (Baniyan - inner vest!)</strong> → 100% same word in Tamil & Hindi!'
    ),
    904: (
        "uniform / vardi", "यूनिफ़ॉर्म / वर्दी",
        None,
        '<strong>Uniform / Vardi (वर्दी)</strong> ≈ <strong>Spoken Tamil யூனிஃபார்ம் (Uniform)</strong> + <strong>Vardi ("Worthy" dress)</strong>!'
    ),
    905: (
        "underwear / chaddi", "अंडरवियर / चड्डी",
        '<strong>Ropa interior (Roh-pah een-teh-ryor)</strong> ≈ <strong>Ropa (Clothes) + Interior (Inside)</strong> → Inside clothes = <em>Underwear</em>!',
        '<strong>Underwear / Chaddi (चड्डी)</strong> ≈ <strong>Spoken Tamil ஜட்டி (Jatti ≈ Chaddi!)</strong> → 100% same everyday word!'
    ),
    908: (
        "boot", "बूट",
        '<strong>Bota (Boh-tah)</strong> ≈ Direct match with English <strong>"Boot"</strong> & spoken Tamil <strong>பூட்ஸ் (Boots)</strong>!',
        '<strong>Boot (बूट)</strong> ≈ 100% identical to spoken Tamil <strong>பூட்ஸ் (Boot)</strong> & English <strong>"Boot"</strong>!'
    ),
    913: (
        "belt", "बेल्ट",
        '<strong>Cinturón (Seen-too-ron)</strong> ≈ English <strong>"Cinch-Around"</strong> → <em>Cinch</em> the leather <em>Belt (Cinturón)</em> around your waist!',
        '<strong>Belt (बेल्ट)</strong> ≈ 100% identical to spoken Tamil <strong>பெல்ட் (Belt)</strong> & English <strong>"Belt"</strong>!'
    ),
    914: (
        "ribbon / feeta", "रिबन / फ़ीता",
        '<strong>Cinta (Seen-tah)</strong> ≈ Sounds like <strong>"Cinch-Tie"</strong> → Tie a silk <em>Ribbon (Cinta)</em> in a bow!',
        '<strong>Ribbon / Feeta (रिबन / फ़ीता)</strong> ≈ <strong>Spoken Tamil ரிப்பன் (Ribbon)</strong> & <strong>"Feet-Tie" (Feeta = lace/ribbon)</strong>!'
    ),
    915: (
        "muffler / scarf", "मफ़लर / स्कार्फ़",
        '<strong>Bufanda (Boo-fan-dah)</strong> ≈ Sounds like <strong>"Puff-And-Warm"</strong> → Wrap a puffy warm <em>Scarf (Bufanda)</em> around your neck!',
        '<strong>Scarf / Muffler (मफ़लर)</strong> ≈ 100% identical to spoken Tamil <strong>மஃப்ளர் / ஸ்கார்ஃப் (Muffler / Scarf)</strong>!'
    ),
    918: (
        "button", "बटन",
        '<strong>Botón (Boh-ton)</strong> ≈ Direct match with English <strong>"Button"</strong> & Tamil <strong>பொத்தான் (Pothaan = Botón!)</strong> → 100% same word!',
        '<strong>Button (बटन)</strong> ≈ <strong>Tamil பொத்தான் (Pothaan) / பட்டன் (Button)</strong> → 100% identical in Tamil, Hindi & English!'
    ),
    921: (
        "collar", "कॉलर",
        '<strong>Cuello (Kweh-yoh)</strong> ≈ English <strong>"Collar"</strong> (neck/collar) → Fold down your shirt <em>Collar (Cuello)</em>!',
        '<strong>Collar (कॉलर)</strong> ≈ 100% identical to spoken Tamil <strong>காலர் (Collar)</strong> & English <strong>"Collar"</strong>!'
    ),
    922: (
        "bag / thaila", "बैग / थैला",
        '<strong>Bolsa (Bol-sah)</strong> ≈ Sounds like <strong>"Ball-Sack / Pouch"</strong> → Carry groceries in a <em>Bolsa (Bag)</em>!',
        '<strong>Thaila / Bag (थैला / बैग)</strong> ≈ <strong>Tamil தைத்த பை (Thaitha pai ≈ Thaila)</strong> & spoken Tamil <strong>பேக் (Bag)</strong>!'
    ),
    923: (
        "purse / batua", "पर्स / बटुआ",
        '<strong>Cartera (Kar-teh-rah)</strong> ≈ Holds your <strong>"Cards (Carta)"</strong> & cash = <em>Cartera (Purse)</em>!',
        '<strong>Purse / Batua (पर्स / बटुआ)</strong> ≈ 100% identical to spoken Tamil <strong>பர்ஸ் (Purse)</strong>!'
    ),
    924: (
        "batua / wallet", "बटुआ / वॉलेट",
        '<strong>Billetera (Bee-yeh-teh-rah)</strong> ≈ Holds paper <strong>"Bills (Billetes)"</strong> → Money <em>Wallet (Billetera)</em>!',
        '<strong>Batua / Wallet (बटुआ)</strong> ≈ <strong>Spoken Tamil மணிபர்ஸ் / வாலெட் (Wallet)</strong> + <strong>"Put-Away" cash (Batua)</strong>!'
    ),
    925: (
        "backpack / basta", "बैग / बस्ता",
        '<strong>Mochila (Moh-chee-lah)</strong> ≈ Sounds like <strong>"More-Chiller"</strong> + <strong>Tamil மூட்டை (Moottai - bundle/pack)</strong> → Sling your <em>Mochila (Backpack)</em> on your back!',
        '<strong>Basta / Bag (बस्ता)</strong> ≈ <strong>"Bus-Bag" (Basta)</strong> carried by school kids + spoken Tamil <strong>பேக் (Bag)</strong>!'
    ),
    926: (
        "suitcase / peti", "सूटकेस / पेटी",
        '<strong>Maleta (Mah-leh-tah)</strong> ≈ Sounds like <strong>"My-Luggage-a"</strong> → Pack your travel <em>Suitcase (Maleta)</em>!',
        '<strong>Suitcase / Peti (सूटकेस / पेटी)</strong> ≈ <strong>Tamil பெட்டி (Petti = Peti!)</strong> & <strong>சூட்கேஸ் (Suitcase)</strong> → 100% same word!'
    ),
    934: (
        "kangan / bracelet", "कंगन / ब्रेसलेट",
        '<strong>Pulsera (Pool-seh-rah)</strong> ≈ Worn right on your wrist <strong>"Pulse (Pulso)"</strong> = <em>Pulsera (Bracelet)</em>!',
        '<strong>Kangan / Bracelet (कंगन)</strong> ≈ <strong>Tamil கங்கணம் (Kanganam - wrist bangle!)</strong> → 100% same word: Tamil <em>Kanganam</em> = Hindi <em>Kangan</em>!'
    ),
    935: (
        "transport / yaatayaat", "ट्रांसपोर्ट / यातायात",
        None,
        '<strong>Transport / Yaatayaat (यातायात)</strong> ≈ <strong>Tamil யாத்திரை (Yaathirai - travel/journey)</strong> & English <strong>"Transport"</strong>!'
    ),
    937: (
        "car / gaadi", "कार / गाड़ी",
        '<strong>Auto / Coche (Ow-toh / Koh-cheh)</strong> ≈ Direct match with English <strong>"Auto / Coach"</strong> & Tamil <strong>ஆட்டோ / கார்</strong>!',
        '<strong>Car / Gaadi (कार / गाड़ी)</strong> ≈ <strong>Spoken Tamil கார் / காடி (Car / Gaadi)</strong> → 100% same everyday words!'
    ),
    939: (
        "scooter", "स्कूटर",
        '<strong>Motoneta (Moh-toh-neh-tah)</strong> ≈ Mini <strong>"Motor-Net"</strong> two-wheeler = <em>Scooter (Motoneta)</em>!',
        '<strong>Scooter (स्कूटर)</strong> ≈ 100% identical to spoken Tamil <strong>ஸ்கூட்டர் (Scooter)</strong> & English <strong>"Scooter"</strong>!'
    ),
    940: (
        "bike / motorcycle", "बाइक / मोटरसाइकिल",
        '<strong>Motocicleta (Moh-toh-see-kleh-tah)</strong> ≈ Direct match with English <strong>"Motorcycle"</strong>!',
        '<strong>Bike / Motorcycle (बाइक)</strong> ≈ 100% identical to spoken Tamil <strong>பைக் / மோட்டார் சைக்கிள்</strong>!'
    ),
    941: (
        "bus", "बस",
        '<strong>Autobús (Ow-toh-boos)</strong> ≈ Direct match with English <strong>"Auto + Bus"</strong> & Tamil <strong>பஸ் (Bus)</strong>!',
        '<strong>Bus (बस)</strong> ≈ 100% identical to spoken Tamil <strong>பஸ் (Bus)</strong> & English <strong>"Bus"</strong>!'
    ),
    942: (
        "train / railgaadi", "ट्रेन / रेलगाड़ी",
        '<strong>Tren (Tren)</strong> ≈ Sounds 100% identical to English <strong>"Train"</strong> & spoken Tamil <strong>டிரெயின் (Train)</strong>!',
        '<strong>Train / Railgaadi (ट्रेन / रेलगाड़ी)</strong> ≈ <strong>Spoken Tamil டிரெயின் / ரயில் (Train / Rail)</strong>!'
    ),
    943: (
        "truck", "ट्रक",
        '<strong>Camión (Kah-myon)</strong> ≈ Sounds like <strong>"Carry-On"</strong> heavy cargo → Heavy cargo <em>Truck (Camión)</em>!',
        '<strong>Truck / Lorry (ट्रक)</strong> ≈ 100% identical to spoken Tamil <strong>டிரக் / லாரி (Truck / Lorry)</strong>!'
    ),
    944: (
        "van", "वैन",
        '<strong>Furgoneta (Foor-goh-neh-tah)</strong> ≈ Sounds like <strong>"Four-Go-In-A-Van"</strong> → Family cargo <em>Van (Furgoneta)</em>!',
        '<strong>Van (वैन)</strong> ≈ 100% identical to spoken Tamil <strong>வேன் (Van)</strong> & English <strong>"Van"</strong>!'
    ),
    945: (
        "taxi", "टैक्सी",
        '<strong>Taxi (Tak-see)</strong> ≈ 100% identical in Spanish, English & Tamil <strong>டாக்ஸி (Taxi)</strong>!',
        '<strong>Taxi (टैक्सी)</strong> ≈ 100% identical to spoken Tamil <strong>டாக்ஸி (Taxi)</strong> & English <strong>"Taxi"</strong>!'
    ),
    948: (
        "helicopter", "हेलीकॉप्टर",
        '<strong>Helicóptero (Eh-lee-kop-teh-roh)</strong> ≈ Direct match with English <strong>"Helicopter"</strong> & Tamil <strong>ஹெலிகாப்டர்</strong>!',
        '<strong>Helicopter (हेलीकॉप्टर)</strong> ≈ 100% identical to spoken Tamil <strong>ஹெலிகாப்டர் (Helicopter)</strong> & English!'
    ),
    951: (
        "ferry / naav", "फ़ेरी / नाव",
        '<strong>Transbordador (Trans-bor-dah-dor)</strong> ≈ <strong>Trans (Across) + Bordo ("Board" a ship)</strong> → Passenger boat that boards people across water = <em>Ferry</em>!',
        '<strong>Ferry / Naav (फ़ेरी / नाव)</strong> ≈ <strong>Tamil நாவாய் (Naavaay = Naav, boat!)</strong> & English <strong>"Ferry"</strong>!'
    ),
    955: (
        "brake", "ब्रेक",
        '<strong>Freno (Freh-noh)</strong> ≈ Sounds like <strong>"Freeze-Now!"</strong> → Slam the <em>Brake (Freno)</em> to freeze the car now!',
        '<strong>Brake (ब्रेक)</strong> ≈ 100% identical to spoken Tamil <strong>பிரேக் (Brake)</strong> & English <strong>"Brake"</strong>!'
    ),
    956: (
        "seat", "सीट",
        '<strong>Asiento (Ah-syen-toh)</strong> ≈ Contains English <strong>"A-Seat" (A-siento)</strong> → Take a <em>Seat (Asiento)</em>!',
        '<strong>Seat (सीट)</strong> ≈ 100% identical to spoken Tamil <strong>சீட் (Seat)</strong> & English <strong>"Seat"</strong>!'
    ),
    957: (
        "seatbelt", "सीटबेल्ट",
        '<strong>Cinturón de seguridad (Seen-too-ron deh seh-goo-ree-dad)</strong> ≈ <strong>Cinturón (Belt) + Seguridad ("Security")</strong> → Security belt = <em>Seatbelt</em>!',
        '<strong>Seatbelt (सीटबेल्ट)</strong> ≈ 100% identical to spoken Tamil <strong>சீட்பெல்ட் (Seatbelt)</strong> & English!'
    ),
    958: (
        "fuel / eedhan", "ईंधन / फ़्यूल",
        '<strong>Combustible (Kom-boos-tee-bleh)</strong> ≈ Spelled 100% identically to English <strong>"Combustible"</strong> (burns as engine <em>Fuel</em>)!',
        '<strong>Eedhan / Fuel (ईंधन)</strong> ≈ <strong>Tamil எரிபொருள் + English "Engine-Fuel" (Eedhan)</strong>!'
    ),
    959: (
        "petrol", "पेट्रोल",
        '<strong>Gasolina (Gah-soh-lee-nah)</strong> ≈ Direct match with English <strong>"Gasoline"</strong> (<em>Gasolina = Petrol</em>)!',
        '<strong>Petrol (पेट्रोल)</strong> ≈ 100% identical to Tamil <strong>பெட்ரோல் (Petrol)</strong> & English <strong>"Petrol"</strong>!'
    ),
    960: (
        "traffic / jam", "ट्रैफ़िक / जाम",
        '<strong>Tráfico (Trah-fee-koh)</strong> ≈ Direct match with English <strong>"Traffic"</strong> & spoken Tamil <strong>டிராஃபிக்</strong>!',
        '<strong>Traffic / Jam (ट्रैफ़िक)</strong> ≈ 100% identical to spoken Tamil <strong>டிராஃபிக் ஜாம் (Traffic Jam)</strong>!'
    ),
    963: (
        "highway", "हाईवे",
        '<strong>Autopista (Ow-toh-pees-tah)</strong> ≈ <strong>Auto (Car) + Pista (Fast track)</strong> → Fast car expressway = <em>Highway (Autopista)</em>!',
        '<strong>Highway (हाईवे)</strong> ≈ 100% identical to spoken Tamil <strong>ஹைவே (Highway)</strong> & English <strong>"Highway"</strong>!'
    ),
    967: (
        "tunnel / surang", "सुरंग / टनल",
        '<strong>Túnel (Too-nel)</strong> ≈ Sounds 100% identical to English <strong>"Tunnel"</strong> & spoken Tamil <strong>டனல்</strong>!',
        '<strong>Surang / Tunnel (सुरंग)</strong> ≈ <strong>Tamil சுரங்கம் (Surangam - underground tunnel!)</strong> → 100% same word: Tamil <em>Surangam (சுரங்கம்)</em> = Hindi <em>Surang (Tunnel)</em>!'
    ),
    970: (
        "station", "स्टेशन",
        '<strong>Estación (Es-tah-syon)</strong> ≈ Direct match with English <strong>"Station"</strong> & spoken Tamil <strong>ஸ்டேஷன்</strong>!',
        '<strong>Station (स्टेशन)</strong> ≈ 100% identical to spoken Tamil <strong>ஸ்டேஷன் (Station)</strong> & English <strong>"Station"</strong>!'
    ),
    971: (
        "airport / hawai adda", "एयरपोर्ट / हवाई अड्डा",
        '<strong>Aeropuerto (Ah-eh-roh-pwer-toh)</strong> ≈ Direct match with English <strong>"Aero + Port" (Airport)</strong>!',
        '<strong>Airport / Hawai Adda (हवाई अड्डा)</strong> ≈ <strong>Hawa (Air) + Adda (Station)</strong> & spoken Tamil <strong>ஏர்போர்ட் (Airport)</strong>!'
    ),
    972: (
        "port / bandargaah", "पोर्ट / बंदरगाह",
        '<strong>Puerto (Pwer-toh)</strong> ≈ Direct match with English <strong>"Port"</strong> (<em>Puerto ≈ Port</em>)!',
        '<strong>Port / Bandargaah (बंदरगाह)</strong> ≈ <strong>Spoken Tamil போர்ட் (Port)</strong> + <strong>"Bandar" (Ships docked at harbor)</strong>!'
    ),
    973: (
        "harbor / bandargaah", "बंदरगाह",
        '<strong>Puerto (Pwer-toh)</strong> ≈ Direct match with English <strong>"Port"</strong> (safe ship <em>Harbor = Puerto</em>)!',
        '<strong>Bandargaah (बंदरगाह)</strong> ≈ <strong>Bandar + Gaah (Place)</strong> → Coastal harbor where cargo ships dock!'
    ),
    974: (
        "parking", "पार्किंग",
        '<strong>Estacionamiento (Es-tah-syoh-nah-myen-toh)</strong> ≈ From <strong>"Station-ing"</strong> your car in a spot = <em>Parking (Estacionamiento)</em>!',
        '<strong>Parking (पार्किंग)</strong> ≈ 100% identical to spoken Tamil <strong>பார்க்கிங் (Parking)</strong> & English <strong>"Parking"</strong>!'
    ),
    975: (
        "junction / chauraaha", "चौराहा / जंक्शन",
        '<strong>Cruce (Kroo-seh)</strong> ≈ Direct sibling of English <strong>"Cross / Crossing"</strong> → Where roads cross = <em>Junction (Cruce)</em>!',
        '<strong>Chauraaha / Junction (चौराहा)</strong> ≈ <strong>Chaur (Four/நான்கு) + Raah (Roads)</strong> & spoken Tamil <strong>ஜங்ஷன் (Junction)</strong>!'
    ),
    976: (
        "patri / track", "पटरी / ट्रैक",
        '<strong>Vía (Vee-ah)</strong> ≈ English <strong>"Via"</strong> (by way of the rail line) → Train <em>Track (Vía)</em>!',
        '<strong>Patri / Track (पटरी)</strong> ≈ <strong>Tamil பாதை / பட்டறை (Paathai / Pattarai)</strong> & spoken Tamil <strong>டிராக் (Track)</strong>!'
    ),
    978: (
        "ticket", "टिकट",
        '<strong>Billete / Boleto (Bee-yeh-teh)</strong> ≈ English <strong>"Bill / Billet"</strong> (printed pass) → Travel <em>Ticket (Billete)</em>!',
        '<strong>Ticket (टिकट)</strong> ≈ 100% identical to Tamil <strong>டிக்கெட் (Ticket)</strong> & English <strong>"Ticket"</strong>!'
    ),
    979: (
        "passport", "पासपोर्ट",
        '<strong>Pasaporte (Pah-sah-por-teh)</strong> ≈ Direct match with English <strong>"Passport"</strong> (<em>Pasa + Porte</em>)!',
        '<strong>Passport (पासपोर्ट)</strong> ≈ 100% identical to Tamil <strong>பாஸ்போர்ட் (Passport)</strong> & English <strong>"Passport"</strong>!'
    ),
    986: (
        "school", "स्कूल",
        None,
        '<strong>School (स्कूल)</strong> ≈ 100% identical to spoken Tamil <strong>ஸ்கூல் (School)</strong> & English <strong>"School"</strong>!'
    ),
    987: (
        "college", "कॉलेज",
        None,
        '<strong>College (कॉलेज)</strong> ≈ 100% identical to spoken Tamil <strong>காலேஜ் (College)</strong> & English <strong>"College"</strong>!'
    ),
    988: (
        "university", "यूनिवर्सिटी",
        None,
        '<strong>University (यूनिवर्सिटी)</strong> ≈ 100% identical to spoken Tamil <strong>யூனிவர்சிட்டி (University)</strong> & English!'
    ),
    989: (
        "library", "लाइब्रेरी",
        None,
        '<strong>Library (लाइब्रेरी)</strong> ≈ 100% identical to spoken Tamil <strong>லைப்ரரி (Library)</strong> & English <strong>"Library"</strong>!'
    ),
    990: (
        "museum", "म्यूज़ियम",
        None,
        '<strong>Museum (म्यूज़ियम)</strong> ≈ 100% identical to spoken Tamil <strong>மியூசியம் (Museum)</strong> & English <strong>"Museum"</strong>!'
    ),
    991: (
        "theater", "थिएटर",
        None,
        '<strong>Theater (थिएटर)</strong> ≈ 100% identical to spoken Tamil <strong>தியேட்டர் (Theater)</strong> & English <strong>"Theater"</strong>!'
    ),
    992: (
        "cinema / talkies", "सिनेमा",
        None,
        '<strong>Cinema (सिनेमा)</strong> ≈ 100% identical to Tamil <strong>சினிமா (Cinema)</strong> & English <strong>"Cinema"</strong>!'
    ),
    994: (
        "bakery", "बेकरी",
        None,
        '<strong>Bakery (बेकरी)</strong> ≈ 100% identical to spoken Tamil <strong>பேக்கரி (Bakery)</strong> & English <strong>"Bakery"</strong>!'
    ),
    996: (
        "supermarket", "सुपरमार्केट",
        None,
        '<strong>Supermarket (सुपरमार्केट)</strong> ≈ 100% identical to spoken Tamil <strong>சூப்பர்மார்க்கெட் (Supermarket)</strong> & English!'
    ),
    997: (
        "restaurant / hotel", "रेस्तरां / होटल",
        None,
        '<strong>Restaurant (रेस्तरां)</strong> ≈ 100% identical to spoken Tamil <strong>ரெஸ்டாரன்ட் (Restaurant)</strong> & English!'
    ),
    998: (
        "cafe", "कैफ़े",
        None,
        '<strong>Cafe (कैफ़े)</strong> ≈ 100% identical to spoken Tamil <strong>கபே (Cafe)</strong> & English <strong>"Cafe"</strong>!'
    ),
    999: (
        "bank", "बैंक",
        None,
        '<strong>Bank (बैंक)</strong> ≈ 100% identical to spoken Tamil <strong>பேங்க் (Bank)</strong> & English <strong>"Bank"</strong>!'
    ),
}

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

for dname in ["tier201DeckCards", "tier601DeckCards", "initialDeckCards", "tier101DeckCards"]:
    for kw in ["var ", "const ", "let "]:
        prefix = f"{kw}{dname} = "
        start_idx = content.find(prefix)
        if start_idx != -1:
            break
    if start_idx == -1:
        continue
    json_start = start_idx + len(prefix)
    depth = 0; in_str = False; esc = False; end_idx = json_start
    for i in range(json_start, len(content)):
        ch = content[i]
        if in_str:
            if esc: esc = False
            elif ch == "\\": esc = True
            elif ch == "\"": in_str = False
        else:
            if ch == "\"": in_str = True
            elif ch == "[": depth += 1
            elif ch == "]":
                depth -= 1
                if depth == 0:
                    end_idx = i + 1
                    break
    cards = json.loads(content[json_start:end_idx])
    mod = 0
    for c in cards:
        num = c.get("num")
        if num in RESTORE_MAP:
            hi_trans, hi_dev, s_es, s_hi = RESTORE_MAP[num]
            c["trans"]["hi"] = hi_trans
            c["hiDevanagari"] = hi_dev
            if s_es:
                c["shortcutEs"] = s_es
            if s_hi:
                c["shortcutHi"] = s_hi
            mod += 1
    if mod > 0:
        new_json = json.dumps(cards, ensure_ascii=False)
        content = content[:json_start] + new_json + content[end_idx:]
        print(f"Restored {mod} cards in {dname}")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)
