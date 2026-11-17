# Deep atomic word-by-word upgrades for Split 2 (#440 - #821)

DATA_S2 = {
    441: (
        '<strong>Malo / mala / mal</strong> (Latin <em>Malus</em> Evil/Defective — prefix in <em>Malfunction / Malpractice / Malice</em>!) = <em>Bad</em>!',
        '<strong>Bura / buri / bure</strong> (Sanskrit <em>Vira / Vikrita</em> Spoiled/Crooked — root in <em>Buraai</em> Evil, inflecting <em>-a / -i / -e</em>!) = <em>Bad</em>!'
    ),
    442: (
        '1. Excellent: <strong>Genial</strong> (Latin <em>Genius</em> Inspired brilliance!) | '
        '<strong>Estupendo</strong> (Latin <em>Stupere</em> Stunning [<em>Stupendous</em>]!) = <em>Great / Excellent</em>!<br>'
        '2. Prominent/large: <strong>Gran / grande</strong> (Latin <em>Grandis</em> Tall/Mighty [<em>Grand</em>]!) = <em>Great / Large</em>!',
        '1. Excellent: <strong>Bohot badhiya</strong> (<strong>Bohot</strong> Much [Sanskrit <em>Bahut</em>] + <strong>Badhiya</strong> Fine/Elevated!) / '
        '<strong>Zabardast</strong> (Persian <strong>Zabar</strong> Over/Top + <strong>Dast</strong> Hand = Dominant/Awesome!) = <em>Great / Excellent</em>!<br>'
        '2. Prominent/large: <strong>Mahan</strong> (Sanskrit <strong>Maha [Tamil மகான் Mahaan = Great Sage!]</strong>) / '
        '<strong>Bada</strong> (Sanskrit <strong>Vardh</strong> Grown huge!) = <em>Great / Prominent</em>!'
    ),
    445: (
        '<strong>Grande / grandes</strong> (Latin <em>Grandis</em> Full-grown/Mighty [root of <em>Grand / Grandiose</em>]!) = <em>Big / Large</em>!',
        '<strong>Bada / badi / bade</strong> (Sanskrit <strong>Vriddha / Vardh</strong> Grown vast — inflects by gender/number <em>-a / -i / -e</em>!) = <em>Big / Large</em>!'
    ),
    450: (
        '<strong>Largo / larga</strong> (Latin <em>Largus</em> Abundant/Extended — false friend: in Spanish <em>Largo</em> = <em>Lengthy / Long</em>, not Wide!) = <em>Long</em>!',
        '<strong>Lamba / lambi</strong> (Sanskrit <strong>Lamba = Hanging down/Long [Tamil இலம்பம்!]</strong> — inflects <em>-a / -i</em>!) = <em>Long</em>!'
    ),
    451: (
        '<strong>Ancho / ancha</strong> (Latin <em>Amplus</em> Broad across!) | '
        '<strong>Amplio</strong> (Latin <em>Amplus</em> Roomy [<em>Ample / Amplify</em>]!) = <em>Wide</em>!',
        '<strong>Chauda / chaudi</strong> (Sanskrit <strong>Chatur</strong> Four-fold breadth across — inflects <em>-a / -i</em>!) = <em>Wide</em>!'
    ),
    453: (
        '<strong>Alto / alta</strong> (Latin <em>Altus</em> High/Nourished tall [root of <em>Altitude</em>]!) | '
        '<strong>Elevado</strong> (<strong>E-</strong> Out + <strong>Levare</strong> Lift [<em>Elevate</em>]!) = <em>High</em>!',
        '<strong>Uncha / unchi</strong> (Sanskrit <strong>Uchcha = Lofty/Peak [Tamil உச்சம் Uchcham = Summit!]</strong> — inflects <em>-a / -i</em>!) = <em>High</em>!'
    ),
    455: (
        '<strong>Profundo / profunda</strong> (<strong>Pro-</strong> Forward/Down + <strong>Fundus</strong> Bottom [<em>Profound</em>]!) | '
        '<strong>Hondo</strong> (Latin <em>Fundus</em> Deep hollow bottom!) = <em>Deep</em>!',
        '<strong>Gehra / gehri</strong> (Sanskrit <strong>Gabhira = Deep Abyss [Tamil கம்பீரம்]</strong> — inflects <em>-a / -i</em>!) = <em>Deep</em>!'
    ),
    458: (
        '1. Person/slender: <strong>Flaco / flaca</strong> (Latin <em>Flaccus</em> Lean/Drooping — lean frame!) | '
        '<strong>Delgado</strong> (Latin <em>Delicatus</em> Slender/Trim!) = <em>Thin</em>!<br>'
        '2. Object/fine: <strong>Fino / fina</strong> (Latin <em>Finis</em> Finished to a razor-fine edge [<em>Fine</em>]!) | '
        '<strong>Delgado</strong> (Slender sheet!) = <em>Thin</em>!',
        '1. Person/slender: <strong>Patla / patli</strong> (Sanskrit <strong>Patra</strong> Thin leaf/blade [<strong>Tamil பத்திரம் Leaf!</strong>]!) = <em>Thin</em>!<br>'
        '2. Object/fine: <strong>Bareek</strong> (Arabic/Persian <strong>Barik</strong> Thread-fine/Minute!) / '
        '<strong>Patla</strong> (Leaf-thin sheet!) = <em>Thin / Fine</em>!'
    ),
    463: (
        '1. Solid/firm: <strong>Duro / dura</strong> (Latin <em>Durus</em> Hard/Enduring [<em>Durable / Endure</em>]!) = <em>Hard</em>!<br>'
        '2. Difficult: <strong>Difícil</strong> (<strong>Dis-</strong> Not + <strong>Facilis</strong> Easy [<em>Difficult</em>]!) | '
        '<strong>Complicado</strong> (<strong>Com-</strong> Together + <strong>Plicare</strong> Fold/Tangle [<em>Complicate</em>]!) = <em>Difficult</em>!',
        '1. Solid/firm: <strong>Sakht</strong> (Persian <strong>Sakht</strong> Rock-hard/Strict!) / '
        '<strong>Kadak</strong> (Sanskrit <strong>Katina [Tamil கடினம் Kadinam = Hard/Stiff!]</strong> = Crisp/Stiff!) = <em>Hard</em>!<br>'
        '2. Difficult: <strong>Mushkil</strong> (Arabic <strong>Mushkil</strong> Tangled/Puzzling difficulty [<strong>Tamil முஷ்கில்</strong>]!) = <em>Difficult</em>!'
    ),
    464: (
        '<strong>Suave</strong> (Latin <em>Suavis</em> Sweet/Smooth [<em>Suave</em>]!) | '
        '<strong>Blando / blanda</strong> (Latin <em>Blandus</em> Yielding/Tender [<em>Bland</em>]!) = <em>Soft</em>!',
        '<strong>Naram</strong> (Persian <strong>Narm</strong> Pliant/Gentle to touch!) / '
        '<strong>Mulayam</strong> (Arabic <strong>Mula\'im</strong> Smooth, tender & yielding!) = <em>Soft</em>!'
    ),
    482: (
        '<strong>Cerrado / cerrada</strong> (Latin <em>Serare</em> Bar/Bolt shut [root of <em>Serrated</em> latch-teeth]!) = <em>Closed</em>!',
        '<strong>Band</strong> (Persian/Sanskrit <strong>Bandh [Tamil பந்த் Bandh = Tied/Closed Shut!]</strong>!) = <em>Closed</em>!'
    ),
    493: (
        '<strong>Amargo / amarga</strong> (Latin <em>Amarus</em> Sharp/Pungent taste!) = <em>Bitter</em>!',
        '<strong>Kadva / kadvi</strong> (Sanskrit <strong>Katu = Sharp/Bitter [Tamil கடு / கடுகு Pungent!]</strong> — inflects <em>-a / -i</em>!) = <em>Bitter</em>!'
    ),
    499: (
        '<strong>Feo / fea</strong> (Latin <em>Foedus</em> Foul/Unsightly — unpleasant to look at!) = <em>Ugly</em>!',
        '<strong>Badsoorat</strong> (Persian <strong>Bad</strong> Ill + Arabic <strong>Soorat</strong> Face [<strong>Tamil சூரத் Form!</strong>] = Ill-faced!) / '
        '<strong>Ganda dikhne wala</strong> (<strong>Ganda</strong> Dirty/Foul + <strong>Dikhne wala</strong> Looking!) = <em>Ugly</em>!'
    ),
    502: (
        '<strong>Triste</strong> (Latin <em>Tristis</em> Heavy-hearted/Grief-stricken!) = <em>Sad</em>!',
        '<strong>Udaas</strong> (Sanskrit <strong>Ud-</strong> Away + <strong>Aas</strong> Sitting alone — spiritless gloom!) / '
        '<strong>Dukhi</strong> (Sanskrit <strong>Duhkha [Tamil துக்கம் Dukkam = Sorrow!]</strong>!) = <em>Sad</em>!'
    ),
    503: (
        '<strong>Enojado</strong> (<strong>En-</strong> In + <strong>Ojo / Odium</strong> Hatred/Vexed annoyance!) | '
        '<strong>Enfadado</strong> (From Latin <em>Infatuare / Fatuus</em> Frustrated mad!) = <em>Angry</em>!',
        '<strong>Gussa</strong> (Arabic <strong>Ghussah</strong> Choking rage!) / '
        '<strong>Naraaz</strong> (Persian <strong>Na-</strong> Not + <strong>Raazi [Tamil ராஜி Pleased!]</strong> = Displeased!) = <em>Angry</em>!'
    ),
    507: (
        '<strong>Somnoliento</strong> (Latin <em>Somnus</em> Sleep [<em>Somnolent / Insomnia</em>]!) | '
        '<strong>Con sueño</strong> (<strong>Con</strong> With + <strong>Sueño</strong> Sleep!) = <em>Sleepy</em>!',
        '<strong>Neend mein / neend aana</strong> (<strong>Neend</strong> [Sanskrit <em>Nidra</em>, <strong>Tamil நித்திரை!</strong>] + <strong>Mein</strong> In / <strong>Aana</strong> Coming!) = <em>Sleepy</em>!'
    ),
    511: (
        '<strong>Sano / sana</strong> (Latin <em>Sanus</em> Sound [<em>Sanitary / Sanity</em>]!) | '
        '<strong>Saludable</strong> (<strong>Salud</strong> Health [<em>Salute</em>] + <strong>-able</strong>!) = <em>Healthy</em>!',
        '<strong>Tandurust</strong> (Persian <strong>Tan</strong> Body + <strong>Durust</strong> Sound/Right = Whole body fit!) / '
        '<strong>Sehatmand</strong> (Arabic <strong>Sehat</strong> Health + <strong>-mand</strong> Possessing!) = <em>Healthy</em>!'
    ),
    513: (
        '<strong>Asustado</strong> (<strong>A-</strong> + <strong>Susto</strong> Sudden startle/shock!) | '
        '<strong>Tener miedo</strong> (<strong>Tener</strong> Hold + <strong>Miedo</strong> Fear [Latin <em>Metus</em>]!) = <em>Afraid / Scared</em>!',
        '<strong>Dara hua / darr lagna</strong> (Sanskrit <strong>Dara</strong> Split/Trembling fright [<strong>Tamil திகில்</strong>] + <strong>Hua / Lagna</strong> Feel!) = <em>Afraid / Scared</em>!'
    ),
    521: (
        '<strong>Cuidadoso / cuidadosa</strong> (Latin <em>Cogitare</em> Think/Take thought [<strong>Cuidado</strong> Care + <strong>-oso / -osa</strong> Full of!]) = <em>Careful</em>!',
        '<strong>Dhyaan se</strong> (<strong>Dhyaan [Tamil தியானம் = Focus!]</strong> + <strong>Se</strong> With!) / '
        '<strong>Khayaal rakhne wala</strong> (Arabic <strong>Khayaal</strong> Thought/Care + <strong>Rakhna</strong> Keep!) = <em>Careful</em>!'
    ),
    526: (
        '<strong>Rojo / roja</strong> (Latin <em>Russus</em> Deep crimson/red [<em>Russet</em>]!) = <em>Red</em>!',
        '<strong>Laal</strong> (Persian <strong>La\'l</strong> Bright red ruby gemstone!) = <em>Red</em>!'
    ),
    528: (
        '<strong>Verde</strong> (Latin <em>Viridis</em> Fresh green plant shoot [root of <em>Verdant</em>]!) = <em>Green</em>!',
        '<strong>Hara / hari</strong> (Sanskrit <strong>Harita [Tamil பச்சை / ஹரித் Green!]</strong> — inflects <em>-a / -i</em>!) = <em>Green</em>!'
    ),
    534: (
        '<strong>Marrón</strong> (Roasted chestnut color [<em>Maroon</em>]!) | '
        '<strong>Café</strong> (Roasted dark coffee bean brown!) = <em>Brown</em>!',
        '<strong>Bhoora / bhoori</strong> (Sanskrit <strong>Babhru</strong> Tawny earth-ochre color — inflects <em>-a / -i</em>!) = <em>Brown</em>!'
    ),
    537: (
        '<strong>Plata</strong> (Latin <em>Platta</em> Hammered flat metal sheet [<em>Plate</em>] -> Silver!) | '
        '<strong>Plateado</strong> (<strong>Plata</strong> Silver + <strong>-ado</strong> Silver-plated!) = <em>Silver</em>!',
        '<strong>Chaandi</strong> (Sanskrit <strong>Chandra [Tamil சந்திரன் = Shining Moon!]</strong> -> Moon-white silver!) / '
        '<strong>Chaandi jaisa</strong> (<strong>Chaandi</strong> Silver + <strong>Jaisa</strong> Like!) = <em>Silver</em>!'
    ),
    546: (
        '<strong>Mujer</strong> (Latin <em>Mulier</em> Gentle/Soft grown female -> Woman!) = <em>Woman</em>!',
        '<strong>Aurat</strong> (Arabic <em>\'Awrah</em> / Dignity — adult woman!) / '
        '<strong>Mahila</strong> (Sanskrit <strong>Mahila [Tamil மகிளா Mahilaa = Noble Woman!]</strong>!) = <em>Woman</em>!'
    ),
    549: (
        '<strong>Niño / niña</strong> (Affectionate nursery syllable <em>Nin-</em> Little child!) | '
        '<strong>Hijo</strong> (Latin <em>Filius</em> Offspring/Son [<em>Filial</em>]!) = <em>Child</em>!',
        '<strong>Bachha / bachhi</strong> (Sanskrit <strong>Vatsa</strong> Calf/Young darling — boy <em>-a</em> / girl <em>-i</em>!) = <em>Child</em>!'
    ),
    553: (
        '<strong>Padre</strong> (Father [<em>Paternal</em>]!) | '
        '<strong>Madre</strong> (Mother [<em>Maternal</em>]!) | '
        '<strong>Progenitores</strong> (<strong>Pro-</strong> Forth + <strong>Gen-</strong> Beget [<em>Progenitor</em>] = Both parents!) = <em>Parent(s)</em>!',
        '<strong>Maa-baap</strong> (<strong>Maa</strong> Mother [Sanskrit <em>Mata</em>] + <strong>Baap</strong> Father [Sanskrit <em>Vapra</em>] = Mother & Father!) = <em>Parents</em>!'
    ),
    556: (
        '<strong>Hijo</strong> (Latin <em>Filius</em> Male child [root of <em>Filial</em>]!) = <em>Son</em>!',
        '<strong>Beta</strong> (Sanskrit <strong>Bata / Vatsa</strong> Dear lad/offspring — boy child!) = <em>Son</em>!'
    ),
    564: (
        '<strong>Tío</strong> (Greek <em>Theios</em> Divine elder kinsman — respected uncle!) = <em>Uncle</em>!',
        '<strong>Chacha</strong> (Father’s younger brother) / '
        '<strong>Mama</strong> (Mother’s brother — <strong>Tamil மாமா Maamaa!</strong>) / '
        '<strong>Fufa</strong> (Father’s sister’s husband) / '
        '<strong>Mausa</strong> (Mother’s sister’s husband!) = <em>Uncle</em>!'
    ),
    570: (
        '<strong>Amigo / amiga</strong> (Latin <em>Amicus</em> Loved companion [from <em>Amare</em> Love, root of <em>Amicable</em>]!) = <em>Friend</em>!',
        '<strong>Dost</strong> (Persian <strong>Dost</strong> Dear companion/Lover!) / '
        '<strong>Yaar</strong> (Persian <strong>Yar</strong> Trusted bosom pal!) = <em>Friend</em>!'
    ),
    583: (
        '<strong>Oreja</strong> (Latin <em>Auricula</em> Outer ear flap [<em>Auricle</em>]!) | '
        '<strong>Oído</strong> (From <strong>Oír</strong> Hear [<em>Audire</em>] = Inner hearing organ!) = <em>Ear</em>!',
        '<strong>Kaan</strong> (Sanskrit <strong>Karna = Ear [Tamil கர்ணம் Karnam = Ear/Angle!]</strong>!) = <em>Ear</em>!'
    ),
    593: (
        '<strong>Hombro</strong> (Latin <em>Umerus</em> Upper arm bone [medical English <em>Humerus</em>]!) = <em>Shoulder</em>!',
        '<strong>Kandha</strong> (Sanskrit <strong>Skandha = Trunk/Shoulder [Tamil கந்தம் / ஸ்கந்தம்!]</strong>!) = <em>Shoulder</em>!'
    ),
    599: (
        '<strong>Codo</strong> (Latin <em>Cubitum</em> Bent forearm bone [ancient measurement <em>Cubit</em>]!) = <em>Elbow</em>!',
        '<strong>Kohni</strong> (Sanskrit <strong>Kaphoni / Kona [Tamil கோணம் Konam = Angle/Bend!]</strong>!) = <em>Elbow</em>!'
    ),
    600: (
        '<strong>Muñeca</strong> (Swivel joint linking hand & arm — also means doll jointed at wrist!) = <em>Wrist</em>!',
        '<strong>Kalai</strong> (Sanskrit <strong>Kalaya</strong> Slender turning joint where <em>Kangan / Kalai</em> bangles sit!) = <em>Wrist</em>!'
    ),
    603: (
        '<strong>Pulgar</strong> (Latin <em>Pollex</em> Mighty thumb finger [<em>Pollicis</em>]!) | '
        '<strong>Dedo gordo</strong> (<strong>Dedo</strong> Digit/Finger + <strong>Gordo</strong> Fat/Thick!) = <em>Thumb</em>!',
        '<strong>Angootha</strong> (Sanskrit <strong>Angushtha = Big Digit [Tamil அங்குஷ்டம் Angushtam = Thumb!]</strong>!) = <em>Thumb</em>!'
    ),
    611: (
        '<strong>Piel</strong> (Latin <em>Pellis</em> Outer hide/coat [twin of <em>Pelt / Peel</em>]!) = <em>Skin</em>!',
        '<strong>Chamdi</strong> (Sanskrit <strong>Charma [Tamil சருமம் Charmam = Hide/Skin!]</strong>!) / '
        '<strong>Skin</strong> (Old Norse <em>Skinn</em> Stripped outer layer!) = <em>Skin</em>!'
    ),
    619: (
        '<strong>Voz</strong> (Latin <em>Vox / Vocis</em> Spoken sound [root of <em>Vocal / Voice</em>]!) = <em>Voice</em>!',
        '<strong>Awaaz</strong> (Persian <strong>Awaz</strong> Sound/Cry vibrating through the air!) = <em>Voice</em>!'
    ),
    627: (
        '1. Noun: <strong>Tos</strong> (Latin <em>Tussis</em> Harsh chest bark [cough medicine word <em>Anti-tussive</em>]!) = <em>Cough</em>!<br>'
        '2. Verb: <strong>Toser</strong> (From <strong>Tos</strong> — expel air from lungs!) = <em>To Cough</em>!',
        '1. Noun: <strong>Khaansi</strong> (Sanskrit <strong>Kasa</strong> Sharp throat rattle!) = <em>Cough</em>!<br>'
        '2. Verb: <strong>Khaansna</strong> (<strong>Khaans-</strong> Bark + <strong>-na</strong> Verb ending = Clearing the chest!) = <em>To Cough</em>!'
    ),
    649: (
        '<strong>Sopa</strong> (Germanic <em>Suppa</em> Bread soaked in broth!) | '
        '<strong>Caldo</strong> (Latin <em>Calidus</em> Hot simmered stock [<em>Cauldron</em>]!) = <em>Soup</em>!',
        '<strong>Shorba</strong> (Persian <strong>Shor</strong> Salty + <strong>Ab</strong> Water = Spiced broth!) / '
        '<strong>Soup</strong> (<em>Suppa</em> Sipping liquid!) = <em>Soup</em>!'
    ),
    660: (
        '1. Cooking: <strong>Aceite</strong> (Arabic <strong>Al-Zayt</strong> Pressed olive juice -> Oil!) = <em>Cooking Oil</em>!<br>'
        '2. Petroleum: <strong>Petróleo</strong> (<strong>Petra</strong> Rock + <strong>Óleo</strong> Oil!) | '
        '<strong>Crudo</strong> (Latin <em>Crudus</em> Raw/Unrefined!) = <em>Petroleum / Crude</em>!',
        '1. Cooking: <strong>Tel</strong> (Sanskrit <strong>Taila = Sesame oil [Tamil தைலம் Thailam = Pressed Oil!]</strong>!) = <em>Cooking Oil</em>!<br>'
        '2. Petroleum: <strong>Kachha tel</strong> (<strong>Kachha</strong> Raw/Unripe + <strong>Tel</strong> Oil!) = <em>Crude Oil</em>!'
    ),
    669: (
        '<strong>Manzana</strong> (Latin <em>Mala Matiana</em> Orchard apples named after Roman botanist Matius!) = <em>Apple</em>!',
        '<strong>Seb</strong> (Persian <strong>Seb</strong> Crisp mountain orchard apple!) = <em>Apple</em>!'
    ),
    688: (
        '1. Seed/food: <strong>Fruto seco</strong> (<strong>Fruto</strong> Fruit + <strong>Seco</strong> Dry!) | '
        '<strong>Nuez</strong> (Latin <em>Nux</em> Hard-shelled kernel [<em>Nut</em>]!) = <em>Nut</em>!<br>'
        '2. Hardware: <strong>Tuerca</strong> (From <em>Torcer</em> Twist [<em>Torque</em>] — twisted onto a bolt!) = <em>Hardware Nut</em>!',
        '1. Seed/food: <strong>Mewa</strong> (Persian <strong>Mewah</strong> Rich fruit/nut!) / '
        '<strong>Akhrot</strong> (Sanskrit <strong>Akshota [Tamil அக்ரூட் = Walnut!]</strong>!) = <em>Nut</em>!<br>'
        '2. Hardware: <strong>Dhibri</strong> (Threaded metal cap screwed tightly onto a bolt!) = <em>Hardware Nut</em>!'
    ),
    690: (
        '<strong>Tazón</strong> (<strong>Taza</strong> Cup + <strong>-ón</strong> Large deep cup!) | '
        '<strong>Cuenco</strong> (Latin <em>Concha</em> Hollow conch shell dish!) = <em>Bowl</em>!',
        '<strong>Katori</strong> (Sanskrit <em>Katotra</em> Small hollow dish — diminutive of <em>Katora</em>!) / '
        '<strong>Bowl</strong> (Old English <em>Bolla</em> Rounded hollow vessel!) = <em>Bowl</em>!'
    ),
    699: (
        '<strong>Sartén</strong> (Latin <em>Sartago</em> Sizzling metal skillet!) = <em>Pan</em>!',
        '<strong>Tawa</strong> (Persian/Indian flat iron griddle [<strong>Tamil தவா = Griddle!</strong>]!) / '
        '<strong>Kadhai</strong> (Sanskrit <strong>Kataha [Tamil கடாய் Kadaai = Deep Wok!]</strong>!) = <em>Pan</em>!'
    ),
    703: (
        '<strong>Casa</strong> (Latin <em>Casa</em> Dwelling roof!) | '
        '<strong>Hogar</strong> (Latin <em>Focus</em> Warm hearth fireplace -> Family <em>Home</em>!) = <em>House / Home</em>!',
        '<strong>Ghar</strong> (Sanskrit <strong>Griha [Tamil கிரஹம் Griham = House!]</strong>!) / '
        '<strong>Makaan</strong> (Arabic <strong>Makan</strong> Built dwelling place!) = <em>House / Home</em>!'
    ),
    719: (
        '<strong>Silla</strong> (Latin <em>Sella</em> Seat/Saddle [from <em>Sedere</em> Sit]!) = <em>Chair</em>!',
        '<strong>Kursi</strong> (Arabic <strong>Kursi</strong> Raised throne/four-legged seat [<strong>Tamil குர்சி</strong>]!) = <em>Chair</em>!'
    ),
    721: (
        '<strong>Cama</strong> (Late Latin <em>Cama</em> Low woven sleep cot on the floor!) = <em>Bed</em>!',
        '<strong>Bistar</strong> (Persian <strong>Bistar</strong> Spread-out bedding!) / '
        '<strong>Palang</strong> (Sanskrit <strong>Paryanka</strong> Carved four-post bedframe!) = <em>Bed</em>!'
    ),
    740: (
        '1. Sweeping brush: <strong>Escoba</strong> (Latin <em>Scopae</em> Tied twigs [origin of <em>Sweep / Broom</em>]!) = <em>Broom</em>!<br>'
        '2. Wet wipe tool: <strong>Trapeador</strong> (<strong>Trapo</strong> Rag!) | '
        '<strong>Fregona</strong> (<strong>Fregar</strong> Rub [<em>Friction</em>]!) = <em>Mop</em>!',
        '1. Sweeping brush: <strong>Jhaadu</strong> (From <strong>Jhaadna</strong> Shake/Brush off twigs & dust!) = <em>Broom</em>!<br>'
        '2. Wet wipe tool: <strong>Pocha</strong> (From <strong>Ponchhna</strong> Wipe dry/clean with damp cloth!) = <em>Mop</em>!'
    ),
    741: (
        '<strong>Cubo</strong> (Greek <em>Kybos</em> Hollow cube/vessel!) | '
        '<strong>Balde</strong> (Portuguese <em>Balde</em> Deck-washing tub -> Hindi <em>Balti</em> twin!) = <em>Bucket</em>!',
        '<strong>Balti</strong> (Portuguese <em>Balde</em> Pail [<strong>Tamil வாளி / பால்டி Baalti = Bucket!</strong>]!) = <em>Bucket</em>!'
    ),
    742: (
        '1. Waste matter: <strong>Basura</strong> (Latin <em>Versura</em> Broom floor sweepings!) = <em>Trash</em>!<br>'
        '2. Receptacle: <strong>Basurero</strong> (<strong>Basura</strong> + <strong>-ero</strong> Holder) | '
        '<strong>Cubo</strong> (Hollow tub!) = <em>Trash Bin</em>!',
        '1. Waste matter: <strong>Kachra</strong> (<strong>Spoken Tamil கச்சடா Kachada = Sweepings!</strong>) / '
        '<strong>Kooda</strong> (<strong>Tamil கூடை Koodai = Basket/Dustbin!</strong>!) = <em>Trash</em>!<br>'
        '2. Receptacle: <strong>Koodadan</strong> (<strong>Kooda</strong> Trash + Persian <strong>-dan</strong> Container!) = <em>Trash Bin</em>!'
    ),
    773: (
        '1. Wallet for cash/cards: <strong>Billetera</strong> (Holds paper <strong>Billetes</strong> bills!) | '
        '<strong>Cartera</strong> (<strong>Carta</strong> Card + <strong>-era</strong> Case!) = <em>Wallet</em>!<br>'
        '2. Handbag: <strong>Bolso</strong> (Pouch [<em>Bourse</em>]!) | '
        '<strong>Cartera de mano</strong> (Hand-held case!) = <em>Purse / Handbag</em>!',
        '1. Wallet for cash/cards: <strong>Batua</strong> (Puckered cloth drawstring money pouch!) / '
        '<strong>Wallet</strong> (Pocket knapsack/fold!) = <em>Wallet</em>!<br>'
        '2. Handbag: <strong>Purse</strong> (Greek <em>Byrsa</em> Leather pouch!) / '
        '<strong>Theli</strong> (<strong>Thaila</strong> Sack + small <strong>-i</strong> bag!) = <em>Purse / Handbag</em>!'
    ),
    798: (
        '<strong>Calle</strong> (Latin <em>Callis</em> Narrow beaten path/lane!) | '
        '<strong>Camino</strong> (Celtic/Latin <em>Camminus</em> Step-by-step travel track!) = <em>Street / Road</em>!',
        '<strong>Sadak</strong> (Paved roadbed [<strong>Spoken Tamil சடக் / சாலை!</strong>]!) / '
        '<strong>Raasta</strong> (Persian <strong>Rah</strong> Way/Path [<strong>Tamil ராஸ்தா!</strong>]!) = <em>Street / Road</em>!'
    ),
}
