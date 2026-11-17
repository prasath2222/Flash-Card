# Complete atomic polish for remaining puns / missing tokens in Split 1, Split 5, Split 6

DATA_POLISH = {
    70: (
        '1. Quantity: <strong>Poco / un poco</strong> (Latin <em>Paucus</em> Scant [<em>Paucity</em> & musical <em>Poco</em>]!) = <em>A Little</em>!<br>'
        '2. Size: <strong>Pequeño / pequeña</strong> (Expressive Latin root <em>Pikk-</em> Tiny point, cousin of <em>Piccolo</em>!) = <em>Little</em>!',
        '1. Quantity: <strong>Thoda sa</strong> (Sanskrit <strong>Stoka</strong> Drop + <strong>-sa</strong> -ish = A little bit!) = <em>A Little</em>!<br>'
        '2. Size: <strong>Chhota / chhoti</strong> (Prakrit <strong>Chhotta</strong> Short/Small, inflecting <em>-a / -i</em>!) = <em>Little</em>!'
    ),
    71: (
        '<strong>Qué</strong> (Latin <em>Quid</em> What [root of <em>Quiddity</em>] — Spain/LatAm Q-question stem!) = <em>What</em>!',
        '<strong>Kya</strong> (Sanskrit <strong>Kim</strong> What — core Hindi K-question word!) = <em>What</em>!'
    ),
    72: (
        '<strong>Dónde</strong> (Latin <strong>De</strong> From + <strong>Unde</strong> Whence = Where at!) = <em>Where</em>!',
        '<strong>Kahan</strong> (Sanskrit <strong>Kasmin Sthane</strong> -> K-stem + <strong>-han</strong> Place = Where!) = <em>Where</em>!'
    ),
    74: (
        '<strong>Por qué</strong> (<strong>Por</strong> For [Latin <em>Pro</em>] + <strong>Qué</strong> What = For what reason!) = <em>Why</em>!',
        '<strong>Kyun</strong> (Sanskrit <strong>Kim Nu</strong> What now — Hindi K-question reason word!) = <em>Why</em>!'
    ),
    229: (
        '<strong>Seis</strong> (Latin <em>Sex</em> — shared Indo-European numeral <em>Sweks</em> with English <em>Six</em>!) = <em>Six</em>!',
        '<strong>Chhe</strong> (Sanskrit <strong>Shat</strong> Six — Indo-European cousin of <em>Six</em> & <em>Seis</em>!) = <em>Six</em>!'
    ),
    371: (
        '<strong>Cantar</strong> (Latin <em>Cantare</em> Sing repeatedly [root of <em>Chant / Cantor</em>]!) = <em>Sing</em>!',
        '<strong>Gaana</strong> (Sanskrit <strong>Gana [Tamil கானம் Gaanam = Song!]</strong>!) / '
        '<strong>Geet gaana</strong> (<strong>Geet [Tamil கீதம் Geetham = Hymn!]</strong> + <strong>Gaana</strong> Sing!) = <em>Sing</em>!'
    ),
    822: (
        '<strong>Cielo</strong> (Latin <em>Caelum</em> Vault of heaven [root of <em>Celestial / Ceiling</em>]!) = <em>Sky</em>!',
        '<strong>Aasmaan</strong> (Persian <strong>Asman</strong> Vaulted stone/sky dome [<strong>Tamil ஆகாயம்</strong> poetic kin]!) = <em>Sky</em>!'
    ),
    826: (
        '<strong>Nube</strong> (Latin <em>Nubes</em> Cloud/Veil [root of <em>Nebula / Nimbus</em>]!) = <em>Cloud</em>!',
        '<strong>Baadal</strong> (Sanskrit <strong>Varida</strong> Rain-giver -> Prakrit <strong>Vaddala</strong> Moisture cloud!) = <em>Cloud</em>!'
    ),
    827: (
        '1. Noun: <strong>Lluvia</strong> (Latin <em>Pluvia</em> Rainfall [root of <em>Pluvial</em>], <em>pl-</em> -> Spanish <em>ll-</em>!) = <em>Rain</em>!<br>'
        '2. Verb: <strong>Llover</strong> (Action verb from <em>Pluere</em> Pour down water!) = <em>To Rain</em>!',
        '1. Noun: <strong>Baarish</strong> (Persian <strong>Barish</strong> From <em>Baridan</em> Pour!) / <strong>Barsaat</strong> (Sanskrit <strong>Varsha</strong> + <strong>-at</strong> Rainy season!) = <em>Rain</em>!<br>'
        '2. Verb: <strong>Baarish hona</strong> (Rain occur!) / <strong>Barasna</strong> (Sanskrit <strong>Varshana</strong> Pour down!) = <em>To Rain</em>!'
    ),
    828: (
        '1. Noun: <strong>Nieve</strong> (Latin <em>Nix / Nivem</em> [root of <em>Niveous</em> Snowy white]!) = <em>Snow</em>!<br>'
        '2. Verb: <strong>Nevar</strong> (Action verb from <em>Nivem</em> Fall as flakes!) = <em>To Snow</em>!',
        '1. Noun: <strong>Baraf (aasmaani)</strong> (Persian <strong>Barf</strong> Frozen ice + <strong>Aasmaani</strong> Sky-born = Snowflakes!) = <em>Snow</em>!<br>'
        '2. Verb: <strong>Baraf padna</strong> (<strong>Baraf</strong> Snow + <strong>Padna</strong> Fall/Drop from above!) = <em>To Snow</em>!'
    ),
    829: (
        '<strong>Hielo</strong> (Latin <em>Gelu</em> Frost [root of <em>Gel / Congeal</em>], <em>g-</em> softened to silent <em>h-</em>!) = <em>Ice</em>!',
        '<strong>Baraf</strong> (Persian <strong>Barf</strong> Frozen solid chill -> everyday word for ice block!) = <em>Ice</em>!'
    ),
    830: (
        '1. Breeze/wind: <strong>Viento</strong> (Latin <em>Ventus</em> [root of <em>Vent / Ventilate</em>]!) | <strong>Aire</strong> (Latin <em>Aer</em> Air!) = <em>Wind</em>!<br>'
        '2. Storm/tempest: <strong>Tormenta</strong> (Latin <em>Tormentum</em> Twisting whirl [<em>Torment</em>]!) | <strong>Temporal</strong> (Seasonal squall from <em>Tempus</em>!) = <em>Storm</em>!',
        '1. Breeze/wind: <strong>Hawa</strong> (Arabic <strong>Hawa</strong> Moving air/breeze!) = <em>Wind</em>!<br>'
        '2. Storm/tempest: <strong>Toofan</strong> (Greek/Arabic <em>Typhon -> Tufan</em> Violent cyclone!) / <strong>Aandhi</strong> (Sanskrit <strong>Andha</strong> Blinding dust-squall!) = <em>Storm</em>!'
    ),
    831: (
        '<strong>Niebla</strong> (Latin <em>Nebula</em> Mist/Vapor [root of <em>Nebulous</em>]!) | '
        '<strong>Neblina</strong> (<strong>Niebla</strong> + diminutive <strong>-ina</strong> Light mist!) = <em>Fog / Mist</em>!',
        '<strong>Kohra</strong> (Sanskrit <strong>Kujjhati</strong> Shroud in vapor = Thick winter fog!) / '
        '<strong>Dhund</strong> (Prakrit <strong>Dhundha</strong> Dim hazy blur!) = <em>Fog / Mist</em>!'
    ),
    832: (
        '1. Sound rumble: <strong>Trueno</strong> (Latin <em>Tonitrus</em> [root of <em>Thunder</em>]!) = <em>Thunder</em>!<br>'
        '2. Light flash: <strong>Relámpago</strong> (<strong>Re-</strong> Back + Greek <em>Lampas</em> Flash [<em>Lamp</em>]!) | <strong>Rayo</strong> (Latin <em>Radius</em> Beam/Ray!) = <em>Lightning</em>!',
        '1. Sound rumble: <strong>Garjan / baadal ki garaj</strong> (Sanskrit <strong>Garjana [Tamil கர்ஜனை Garjanai = Roar!]</strong> + <strong>Baadal ki</strong> Cloud roar!) = <em>Thunder</em>!<br>'
        '2. Light flash: <strong>Bijli (chamakne wali)</strong> (Sanskrit <strong>Vidyut</strong> Bolt + <strong>Chamakna</strong> Flash bright!) = <em>Lightning</em>!'
    ),
    836: (
        '<strong>Aire</strong> (Latin <em>Aer</em> Lower breathable atmosphere [root of <em>Aerial / Aerate</em>]!) = <em>Air</em>!',
        '<strong>Hawa</strong> (Arabic <strong>Hawa</strong> Flowing breath/wind filling lungs!) = <em>Air</em>!'
    ),
    841: (
        '<strong>Tierra</strong> (Latin <em>Terra</em> Dry land [<em>Terrain</em>]!) | '
        '<strong>Suelo</strong> (Latin <em>Solum</em> Ground floor [<em>Soil</em>]!) | '
        '<strong>Polvo</strong> (Latin <em>Pulvis</em> Fine grain [<em>Pulverize</em>]!) = <em>Dirt / Soil</em>!',
        '<strong>Mitti</strong> (Sanskrit <strong>Mrittika</strong> Clay/Earth — soft earthen soil!) = <em>Dirt / Soil</em>!'
    ),
    842: (
        '<strong>Barro</strong> (Celtic/Iberian <em>Barros</em> Wet potter’s clay!) | '
        '<strong>Lodo</strong> (Latin <em>Lutum</em> Mud mire!) | '
        '<strong>Fango</strong> (Germanic <em>Fani</em> Mire silt!) = <em>Mud</em>!',
        '<strong>Keechad</strong> (Prakrit <strong>Kichchada</strong> Wet slimy puddle mire!) = <em>Mud</em>!'
    ),
    843: (
        '<strong>Arena</strong> (Latin <em>Harena</em> Sand-strewn stadium floor — origin of English <em>Arena</em>!) = <em>Sand</em>!',
        '<strong>Ret</strong> (Prakrit <strong>Reta</strong> Fine-grained desert dust!) / '
        '<strong>Baalu</strong> (Sanskrit <strong>Baluka</strong> Riverbank sand grains!) = <em>Sand</em>!'
    ),
    844: (
        '<strong>Polvo</strong> (Latin <em>Pulvis</em> Crushed powder grains [root of <em>Pulverize / Powder</em>]!) = <em>Dust</em>!',
        '<strong>Dhool</strong> (Sanskrit <strong>Dhuli [Tamil தூள் Thool = Fine Powder/Dust!]</strong>!) / '
        '<strong>Gard</strong> (Persian <strong>Gard</strong> Floating haze/ash particle!) = <em>Dust</em>!'
    ),
    845: (
        '<strong>Piedra</strong> (Latin <em>Petra</em> Crag [<em>Petrify</em>]!) | '
        '<strong>Roca</strong> (Medieval Latin <em>Rocca</em> Massive boulder [<em>Rock</em>]!) = <em>Rock / Stone</em>!',
        '<strong>Patthar</strong> (Sanskrit <strong>Prastara</strong> Hard flat slab/stone!) / '
        '<strong>Chattaan</strong> (Hindi root <em>Chatt</em> Hard cliff boulder!) = <em>Rock / Stone</em>!'
    ),
    846: (
        '1. High peak: <strong>Montaña</strong> (Latin <em>Montanea</em> High land [<em>Mountain</em>]!) = <em>Mountain</em>!<br>'
        '2. Lower elevation: <strong>Colina</strong> (Latin <em>Collis</em> Hill crest!) | <strong>Cerro</strong> (Latin <em>Cirrus</em> Rugged ridge crest!) = <em>Hill</em>!',
        '1. High peak: <strong>Pahaad</strong> (Sanskrit <strong>Pashana / Parvata</strong> Towering stone range!) = <em>Mountain</em>!<br>'
        '2. Lower elevation: <strong>Pahadi</strong> (<strong>Pahaad</strong> + diminutive <strong>-i</strong> Little hill!) / <strong>Teela</strong> (Earthen mound!) = <em>Hill</em>!'
    ),
    848: (
        '<strong>Cueva</strong> (Latin <em>Cava</em> Hollowed vault [<em>Cave / Cavity</em>]!) | '
        '<strong>Caverna</strong> (Latin <em>Caverna</em> Deep stone chamber [<em>Cavern</em>]!) = <em>Cave</em>!',
        '<strong>Gufa</strong> (Sanskrit <strong>Guha [Tamil குகை Kugai = Mountain Cave!]</strong> Hidden hollow!) = <em>Cave</em>!'
    ),
    850: (
        '1. Arid wasteland: <strong>Desierto</strong> (<strong>De-</strong> Un- + <strong>Serere</strong> Join/Plant = Forsaken barren sand [<em>Desert</em>]!) = <em>Desert</em>!<br>'
        '2. Abandon: <strong>Abandonar</strong> (<em>Abandon</em>!) | <strong>Dejar tirado</strong> (<strong>Dejar</strong> Leave + <strong>Tirado</strong> Flung down!) = <em>Desert (Abandon)</em>!',
        '1. Arid wasteland: <strong>Registan</strong> (Persian <strong>Reg</strong> Sand + <strong>-istan</strong> Land = Land of sand!) = <em>Desert</em>!<br>'
        '2. Abandon: <strong>Chhor dena</strong> (<strong>Chhodna</strong> Leave/Drop + <strong>Dena</strong> Away!) = <em>Desert (Abandon)</em>!'
    ),
    851: (
        '<strong>Bosque</strong> (Germanic <em>Boscus</em> Woodland thicket [<em>Bosky / Bouquet</em>]!) | '
        '<strong>Selva</strong> (Latin <em>Silva</em> Wild untamed woods [<em>Sylvan</em>]!) = <em>Forest / Jungle</em>!',
        '<strong>Jangal</strong> (Sanskrit <strong>Jangala</strong> Wild uncultivated thicket — origin of English <em>Jungle</em>!) = <em>Forest / Jungle</em>!'
    ),
    852: (
        '1. Large river: <strong>Río</strong> (Latin <em>Rivus</em> Flowing current [<em>River / Rival</em>]!) = <em>River</em>!<br>'
        '2. Small brook: <strong>Arroyo</strong> (Iberian-Latin <em>Arrugia</em> Water trough!) | <strong>Riachuelo</strong> (<strong>Río</strong> + dim. <strong>-uelo</strong> Little stream!) = <em>Stream</em>!',
        '1. Large river: <strong>Nadi</strong> (Sanskrit <strong>Nadi [Tamil நதி Nadhi = River!]</strong>!) = <em>River</em>!<br>'
        '2. Small brook: <strong>Jharna</strong> (<strong>Jhar</strong> Trickle/Drop water!) / <strong>Nala</strong> (Sanskrit <strong>Nala</strong> Hollow channel brook!) = <em>Stream</em>!'
    ),
    853: (
        '1. Large lake: <strong>Lago</strong> (Latin <em>Lacus</em> Basin [<em>Lake / Lagoon</em>]!) = <em>Lake</em>!<br>'
        '2. Small pool: <strong>Estanque</strong> (Latin <em>Stagnum</em> Still standing pool [<em>Stagnant</em>]!) | <strong>Charca</strong> (Rain puddle basin!) = <em>Pond</em>!',
        '1. Large lake: <strong>Jheel</strong> (Prakrit <strong>Jhilla</strong> Broad glassy wetland!) = <em>Lake</em>!<br>'
        '2. Small pool: <strong>Talaab</strong> (Sanskrit <strong>Tadaga</strong> Tank reservoir!) / <strong>Pokhar</strong> (Sanskrit <strong>Pushkara [Tamil பொய்கை]</strong> Lotus pond!) = <em>Pond</em>!'
    ),
    855: (
        '1. Sandy shore: <strong>Playa</strong> (Late Latin <em>Plagia</em> Flat coastal sand [<em>Playa</em>]!) = <em>Beach</em>!<br>'
        '2. Coastline: <strong>Costa</strong> (Latin <em>Costa</em> Rib/Side [<em>Coast</em>]!) | <strong>Orilla</strong> (Latin <em>Ora</em> Edge/Rim!) = <em>Shore / Coast</em>!',
        '1. Sandy shore: <strong>Samandar ka kinaara</strong> (<strong>Samandar [Tamil சமுத்திரம் Sea!]</strong> + <strong>Kinaara</strong> Edge!) / <strong>Beach</strong> (English loan!) = <em>Beach</em>!<br>'
        '2. Coastline: <strong>Kinaara</strong> (Persian <strong>Kanara</strong> Border/Edge!) = <em>Shore / Coast</em>!'
    ),
    856: (
        '<strong>Isla</strong> (Latin <em>Insula</em> Land set in sea [<em>Isle / Insular / Isolate</em>]!) = <em>Island</em>!',
        '<strong>Taapu</strong> (Sanskrit <strong>Dvipu / Tapa</strong> Sandbank isle rising from water!) = <em>Island</em>!'
    ),
    857: (
        '<strong>Árbol</strong> (Latin <em>Arbor</em> Timber tree [root of <em>Arbor / Arboreal</em>]!) = <em>Tree</em>!',
        '<strong>Ped</strong> (Prakrit <strong>Pinda / Peda</strong> Rooted trunk + leafy crown!) = <em>Tree</em>!'
    ),
    858: (
        '<strong>Animal</strong> (Latin <em>Anima</em> Living breath [<em>Animate / Animal</em>]!) | '
        '<strong>Bicho</strong> (Latin <em>Bestia</em> Small critter/beast!) = <em>Animal</em>!',
        '<strong>Jaanwar</strong> (Persian <strong>Jaan</strong> Life + <strong>-war</strong> Possessing = Living creature!) = <em>Animal</em>!'
    ),
    859: (
        '<strong>Pájaro</strong> (Latin <em>Passer</em> Sparrow/Small flyer!) | '
        '<strong>Ave</strong> (Latin <em>Avis</em> Bird [root of <em>Aviation / Aviary</em>]!) = <em>Bird</em>!',
        '<strong>Chidiya</strong> (Prakrit <strong>Chitika</strong> Tiny chirping songbird!) / '
        '<strong>Parinda</strong> (Persian <strong>Par</strong> Wing + <strong>-inda</strong> Flyer = Winged bird!) = <em>Bird</em>!'
    ),
    860: (
        '1. Adult dog: <strong>Perro / perra</strong> (Hispanic root <em>Perr-</em> Growl hound — masc./fem.!) = <em>Dog</em>!<br>'
        '2. Young pup: <strong>Cachorro / cachorra</strong> (Latin <em>Catulus</em> Young cub/pup — masc./fem.!) = <em>Puppy</em>!',
        '1. Adult dog: <strong>Kutta / kutti</strong> (Sanskrit <strong>Kurkura</strong> Barking dog — masc./fem.!) = <em>Dog</em>!<br>'
        '2. Young pup: <strong>Pilla</strong> (<strong>Dravidian/Tamil பிள்ளை Pillai = Little Child/Young One!</strong>) = <em>Puppy</em>!'
    ),
    861: (
        '1. Adult cat: <strong>Gato / gata</strong> (Late Latin <em>Cattus</em> Feline [<em>Cat</em>] — masc./fem.!) = <em>Cat</em>!<br>'
        '2. Young kitten: <strong>Gatito / gatita</strong> (<strong>Gato</strong> + diminutive <strong>-ito / -ita</strong> Tiny cat!) = <em>Kitten</em>!',
        '1. Adult cat: <strong>Billi</strong> (Sanskrit <strong>Bidala</strong> Spotted house cat!) = <em>Cat</em>!<br>'
        '2. Young kitten: <strong>Billi ka bachha</strong> (<strong>Billi</strong> Cat + <strong>Bachha</strong> Baby!) = <em>Kitten</em>!'
    ),
    862: (
        '1. Female cow: <strong>Vaca</strong> (Latin <em>Vacca</em> Milk cow [origin of <em>Vaccine</em> from cowpox!]!) = <em>Cow</em>!<br>'
        '2. Male bull: <strong>Toro</strong> (Latin <em>Taurus</em> Charged arena bull [zodiac <em>Taurus</em>]!) = <em>Bull</em>!',
        '1. Female cow: <strong>Gaay</strong> (Sanskrit <strong>Gau</strong> Sacred milk cow — Indo-European cousin of English <em>Cow</em>!) = <em>Cow</em>!<br>'
        '2. Male bull: <strong>Bail</strong> (Sanskrit <strong>Balivarda</strong> Strong draft ox!) / <strong>Saand</strong> (Sanskrit <strong>Shanda</strong> Unbridled stud bull!) = <em>Bull</em>!'
    ),
    863: (
        '1. Wool sheep: <strong>Oveja</strong> (Latin <em>Ovicula</em> Little sheep [root of <em>Ovine</em>]!) = <em>Sheep</em>!<br>'
        '2. Horned goat: <strong>Cabra / chivo</strong> (Latin <em>Capra</em> Goat [<em>Capricorn</em>] / Onomatopoeic kid-call <em>Chiv-</em>!) = <em>Goat</em>!',
        '1. Wool sheep: <strong>Bhed</strong> (Sanskrit <strong>Bheda</strong> Grazing flock sheep!) = <em>Sheep</em>!<br>'
        '2. Horned goat: <strong>Bakri / bakra</strong> (Sanskrit <strong>Barkara</strong> Bleating she-goat / he-goat!) = <em>Goat</em>!'
    ),
    864: (
        '1. Horse: <strong>Caballo</strong> (Latin <em>Caballus</em> Workhorse [root of <em>Cavalry / Cavalier</em>]!) = <em>Horse</em>!<br>'
        '2. Donkey: <strong>Burro / asno</strong> (Latin <em>Burricus</em> Small shaggy pack-mule / Latin <em>Asinus</em> [<em>Asinine</em>]!) = <em>Donkey</em>!',
        '1. Horse: <strong>Ghoda</strong> (Sanskrit <strong>Ghotaka</strong> Swift galloping steed!) = <em>Horse</em>!<br>'
        '2. Donkey: <strong>Gadha</strong> (Sanskrit <strong>Gardabha</strong> Braying pack animal!) = <em>Donkey</em>!'
    ),
    865: (
        '<strong>Cerdo</strong> (Latin <em>Setiger</em> Bristle-haired hog!) | '
        '<strong>Puerco</strong> (Latin <em>Porcus</em> Swine [root of <em>Pork</em>]!) | '
        '<strong>Chancho</strong> (Latin American slang for fat hog!) = <em>Pig</em>!',
        '<strong>Suar</strong> (Sanskrit <strong>Shukara</strong> Snouting tusked boar/swine!) = <em>Pig</em>!'
    ),
    868: (
        '1. Lion: <strong>León</strong> (Latin <em>Leo / Leonem</em> [root of <em>Leo / Leonine</em>]!) = <em>Lion</em>!<br>'
        '2. Striped tiger: <strong>Tigre</strong> (Greek/Latin <em>Tigris</em> Swift river/arrow cat [<em>Tiger</em>]!) = <em>Tiger</em>!',
        '1. Lion: <strong>Sher</strong> (Persian <strong>Shir</strong> Majestic king lion!) = <em>Lion</em>!<br>'
        '2. Striped tiger: <strong>Baagh</strong> (Sanskrit <strong>Vyaghra</strong> Striped leaping Bengal predator!) = <em>Tiger</em>!'
    ),
    869: (
        '1. Animal: <strong>Oso</strong> (Latin <em>Ursus</em> Bear [root of <em>Ursa Major / Ursine</em>]!) = <em>Bear (Animal)</em>!<br>'
        '2. Endure: <strong>Aguantar</strong> (Put on gloves to bear weight!) | <strong>Soportar</strong> (<strong>Sub-</strong> Under + <strong>Portare</strong> Carry [<em>Support</em>]!) = <em>Bear (Endure)</em>!',
        '1. Animal: <strong>Bhaloo</strong> (Sanskrit <strong>Bhalluka</strong> Shaggy forest bear!) = <em>Bear (Animal)</em>!<br>'
        '2. Endure: <strong>Sehna</strong> (Sanskrit <strong>Sahana [Tamil சகிப்பு Sahi = Endure!]</strong>!) / <strong>Bardasht karna</strong> (Persian <strong>Bar-dasht</strong> Hold up!) = <em>Bear (Endure)</em>!'
    ),
    870: (
        '1. Wolf: <strong>Lobo</strong> (Latin <em>Lupus</em> Wolf [root of <em>Lupine</em>]!) = <em>Wolf</em>!<br>'
        '2. Fox: <strong>Zorro / zorra</strong> (Basque <em>Zorri</em> Clever sly tail!) = <em>Fox</em>!',
        '1. Wolf: <strong>Bhediya</strong> (From <strong>Bhed</strong> Sheep + <strong>-iya</strong> = Sheep-hunter pack predator!) = <em>Wolf</em>!<br>'
        '2. Fox: <strong>Lomdi</strong> (Sanskrit <strong>Lomasha</strong> Bushy-tailed sly creature!) = <em>Fox</em>!'
    ),
    872: (
        '<strong>Conejo</strong> (Latin <em>Cuniculus</em> Burrowing tunnel digger [root of archaic English <em>Coney</em>]!) = <em>Rabbit</em>!',
        '<strong>Khargosh</strong> (Persian <strong>Khar</strong> Donkey + <strong>Gosh</strong> Ear = Donkey-eared hopper!) = <em>Rabbit</em>!'
    ),
    873: (
        '<strong>Ratón / rata</strong> (Expressive Romance root <em>Ratt-</em> Scratching/gnawing rodent — small <em>Ratón</em> / big <em>Rata</em>!) = <em>Mouse / Rat</em>!',
        '<strong>Chuha / chuhiya</strong> (Prakrit <strong>Chuh-</strong> Squeaking burrow rodent — male/female!) = <em>Mouse / Rat</em>!'
    ),
    880: (
        '1. Dove/pigeon: <strong>Paloma</strong> (Latin <em>Palumba</em> Ring-necked wild dove!) = <em>Pigeon</em>!<br>'
        '2. Black crow: <strong>Cuervo</strong> (Latin <em>Corvus</em> Raven [root of <em>Corvid</em>]!) = <em>Crow</em>!',
        '1. Dove/pigeon: <strong>Kabootar</strong> (Persian <strong>Kabutar</strong> Bluish-grey cooing roof dove!) = <em>Pigeon</em>!<br>'
        '2. Black crow: <strong>Kauwa</strong> (Sanskrit <strong>Kaka [Tamil காக்கா Kaakka = Crow!]</strong> — "Caw!" bird!) = <em>Crow</em>!'
    ),
    881: (
        '1. Animal: <strong>Murciélago</strong> (Latin <em>Mus</em> Mouse + <em>Caecus</em> Blind = Flying blind-mouse!) = <em>Bat (Animal)</em>!<br>'
        '2. Sports stick: <strong>Bate</strong> (Borrowed directly from English <em>Bat</em>!) = <em>Bat (Sports)</em>!',
        '1. Animal: <strong>Chamgadar</strong> (<strong>Cham</strong> Skin/Membrane + <strong>Gadar</strong> Wing = Leather-winged night flyer!) = <em>Bat (Animal)</em>!<br>'
        '2. Sports stick: <strong>Balla</strong> (Prakrit <strong>Balla</strong> Carved wooden plank/club!) = <em>Bat (Sports)</em>!'
    ),
    882: (
        '<strong>Tiburón</strong> (Indigenous Taino/Caribbean sea word <em>Tiburon</em> Ocean hunter!) = <em>Shark</em>!',
        '<strong>Shark</strong> (English loanword — <em>Shark</em> used directly across Hindi!) = <em>Shark</em>!'
    ),
    883: (
        '<strong>Insecto</strong> (<strong>In-</strong> Into + <strong>Sectum</strong> Cut [<em>Section</em>] = Segmented 3-part body!) | '
        '<strong>Bicho</strong> (Latin <em>Bestia</em> Tiny creepy-crawly!) = <em>Insect / Bug</em>!',
        '<strong>Keeda</strong> (Sanskrit <strong>Kita</strong> Crawling worm/insect!) / '
        '<strong>Makoda</strong> (Large hard-shelled crawling beetle!) = <em>Insect / Bug</em>!'
    ),
    884: (
        '<strong>Mosquito</strong> (<strong>Mosca</strong> Fly [Latin <em>Musca</em>] + dim. <strong>-ito</strong> = Little biting fly!) | '
        '<strong>Zancudo</strong> (<strong>Zanca</strong> Long spindly leg + <strong>-udo</strong> = Long-legged!) = <em>Mosquito</em>!',
        '<strong>Machhar</strong> (Sanskrit <strong>Mashaka</strong> Humming blood-sucking fly!) = <em>Mosquito</em>!'
    ),
    885: (
        '<strong>Abeja</strong> (Latin <em>Apicula</em> Little bee [root of <em>Apiary</em> Bee-house]!) = <em>Bee</em>!',
        '<strong>Madhumakkhi</strong> (<strong>Madhu</strong> Honey [Sanskrit] + <strong>Makkhi</strong> Fly = Honey-making fly!) = <em>Bee</em>!'
    ),
    886: (
        '<strong>Hormiga</strong> (Latin <em>Formica</em> Ant [root of <em>Formic Acid</em> — ant venom!], <em>f-</em> -> silent <em>h-</em>!) = <em>Ant</em>!',
        '<strong>Cheenti</strong> (Prakrit <strong>Chintika</strong> Tiny marching dark speck!) = <em>Ant</em>!'
    ),
    887: (
        '<strong>Araña</strong> (Latin <em>Aranea</em> Spinner [Greek <em>Arachne</em> -> <em>Arachnid</em>]!) = <em>Spider</em>!',
        '<strong>Makdi</strong> (Sanskrit <strong>Markata / Makada</strong> Web-weaving leg-crawler!) = <em>Spider</em>!'
    ),
    888: (
        '<strong>Mariposa</strong> (<strong>María</strong> Mary + <strong>Posa</strong> Alight/Rest = Delicate <em>"Mary, rest softly!"</em> insect!) = <em>Butterfly</em>!',
        '<strong>Titli</strong> (Sanskrit <strong>Tittibha</strong> Fluttering painted-wing beauty!) = <em>Butterfly</em>!'
    ),
    891: (
        '<strong>Anciano</strong> (Latin <em>Ante</em> Before = Long-lived [<em>Ancient</em>]!) | '
        '<strong>Mayor</strong> (Latin <em>Major</em> Greater/Older!) | '
        '<strong>Persona de edad</strong> (Person of age!) = <em>Elder / Senior</em>!',
        '<strong>Buzurg</strong> (Persian <strong>Buzurg</strong> Great/Respected elder!) / '
        '<strong>Bada-boodha</strong> (<strong>Bada</strong> Big/Senior + <strong>Boodha</strong> Old [Sanskrit <em>Vriddha</em>]!) = <em>Elder / Senior</em>!'
    ),
    896: (
        '<strong>Multitud</strong> (<em>Multitude</em>!) | '
        '<strong>Muchedumbre</strong> (<strong>Mucho</strong> Many + <strong>-dumbre</strong> Mass!) | '
        '<strong>Gente</strong> (Latin <em>Gens</em> People [<em>Gentry</em>]!) = <em>Crowd</em>!',
        '<strong>Bheed</strong> (Prakrit <strong>Bhida</strong> Tightly packed thronging crush!) / '
        '<strong>Janta</strong> (Sanskrit <strong>Janata [Tamil ஜனதா]</strong> Common public!) = <em>Crowd</em>!'
    ),
    902: (
        '1. Bride: <strong>Novia</strong> (Latin <em>Nova</em> New/Young newlywed woman!) = <em>Bride</em>!<br>'
        '2. Groom: <strong>Novio</strong> (Latin <em>Novius</em> New newlywed man!) = <em>Groom</em>!',
        '1. Bride: <strong>Dulhan</strong> (Sanskrit <strong>Durlabha</strong> Prized/Cherished wedding bride!) = <em>Bride</em>!<br>'
        '2. Groom: <strong>Dulha</strong> (Sanskrit <strong>Durlabha</strong> Cherished wedding groom!) = <em>Groom</em>!'
    ),
    904: (
        '<strong>Barrio</strong> (Arabic <strong>Barri</strong> Outer city quarter!) | '
        '<strong>Vecindario</strong> (<strong>Vecino</strong> Neighbor [<em>Vicinity</em>]!) | '
        '<strong>Colonia</strong> (Planned housing block [<em>Colony</em>]!) = <em>Neighborhood</em>!',
        '<strong>Mohalla</strong> (Arabic <strong>Mahalla</strong> City quarter!) / '
        '<strong>Pados</strong> (Sanskrit <strong>Prativesha</strong> Nearby door!) / '
        '<strong>Ilaqa</strong> (Arabic <strong>Ilaqa</strong> Attached zone!) = <em>Neighborhood</em>!'
    ),
    905: (
        '1. Buzzer/siren: <strong>Alarma</strong> (Italian <em>All’arme!</em> "To arms!" warning bell [<em>Alarm</em>]!) = <em>Alarm</em>!<br>'
        '2. Prompt note: <strong>Recordatorio</strong> (<strong>Re-</strong> Again + <strong>Cor</strong> Heart = Bring back to mind!) = <em>Reminder</em>!',
        '1. Buzzer/siren: <strong>Alarm</strong> (English loan!) / <strong>Ghanti</strong> (Sanskrit <strong>Ghanta [Tamil மணி]</strong> Ringing bell!) = <em>Alarm</em>!<br>'
        '2. Prompt note: <strong>Yaad dilaane wala</strong> (Make remember!) / <strong>Reminder</strong> (English loan!) = <em>Reminder</em>!'
    ),
    909: (
        '<strong>Liso</strong> (Greek <em>Lissos</em> Glide-flat & frictionless!) | '
        '<strong>Suave</strong> (Latin <em>Suavis</em> Mild & gentle [root of <em>Suave</em>]!) = <em>Smooth</em>!',
        '<strong>Chikna</strong> (Sanskrit <strong>Chikkana</strong> Glossy & slick!) / '
        '<strong>Mulayam</strong> (Arabic <strong>Mula’im</strong> Yielding & velvet-soft!) = <em>Smooth</em>!'
    ),
    913: (
        '1. Level surface: <strong>Plano</strong> (<em>Plane</em>!) | <strong>Llano</strong> (Latin <em>Planus</em> Level plain!) | <strong>Chato</strong> (Latin <em>Plattus</em> Pressed flat!) = <em>Flat (Surface)</em>!<br>'
        '2. Apartment: <strong>Piso</strong> (Floor tier!) | <strong>Departamento</strong> (Building <em>Department/Unit</em>!) = <em>Flat (Apartment)</em>!',
        '1. Level surface: <strong>Seedha</strong> (Straight/Even!) / <strong>Chipta</strong> (Pressed flush/flat!) = <em>Flat (Surface)</em>!<br>'
        '2. Apartment: <strong>Flat</strong> (Borrowed British/Indian English urban word for apartment!) = <em>Flat (Apartment)</em>!'
    ),
    914: (
        '1. Unbent line: <strong>Recto</strong> (Latin <em>Rectus</em> [<em>Erect / Direct</em>]!) | <strong>Derecho</strong> (<strong>De-</strong> + <strong>Rectus</strong> = Uncurved right ahead!) = <em>Straight</em>!<br>'
        '2. Candid: <strong>Directo</strong> (<em>Direct</em>!) | <strong>Sincero</strong> (<em>Sincere</em>!) = <em>Straightforward</em>!',
        '1. Unbent line: <strong>Seedha</strong> (Sanskrit <strong>Siddha</strong> Unswerving upright path!) = <em>Straight</em>!<br>'
        '2. Candid: <strong>Saaf-saaf</strong> (Clear-clear!) / <strong>Khara</strong> (Pure/Unalloyed outspoken truth!) = <em>Straightforward</em>!'
    ),
    916: (
        '1. Dense/firm: <strong>Sólido</strong> (Latin <em>Solidus</em> Whole/Dense [<em>Solid</em>]!) | <strong>Firme</strong> (Latin <em>Firmus</em> [<em>Firm</em>]!) = <em>Solid</em>!<br>'
        '2. Empty cavity: <strong>Hueco</strong> (Hollow scoop!) | <strong>Vacío</strong> (Latin <em>Vacuus</em> [<em>Vacuum / Vacant</em>]!) = <em>Hollow</em>!',
        '1. Dense/firm: <strong>Thos</strong> (Prakrit <strong>Thossa</strong> Dense compact packed mass!) = <em>Solid</em>!<br>'
        '2. Empty cavity: <strong>Khokhla</strong> (<strong>Khol</strong> Shell cavity!) / <strong>Andar se khaali</strong> (Empty from inside!) = <em>Hollow</em>!'
    ),
    918: (
        '1. Not tight: <strong>Flojo</strong> (Latin <em>Fluxus</em> Slack!) | <strong>Suelto</strong> (Latin <em>Solutus</em> Untied!) | <strong>Holgado</strong> (<em>Holgar</em> Have extra breathing room!) = <em>Loose</em>!<br>'
        '2. Free: <strong>Suelto</strong> (Detached!) | <strong>Libre</strong> (Latin <em>Liber</em> [<em>Liberty</em>]!) = <em>Loose / Unfastened</em>!',
        '1. Not tight: <strong>Dheela</strong> (Sanskrit <strong>Shithila</strong> Slack & un-taut!) = <em>Loose (Fitting)</em>!<br>'
        '2. Free: <strong>Khula hua</strong> (Unbound open!) / <strong>Azaad</strong> (Persian <strong>Azad</strong> Noble & free!) = <em>Loose / Free</em>!'
    ),
    920: (
        '1. Sofa pad: <strong>Cojín</strong> (Latin <em>Culcita</em> Stuffed hip/seat pad [root of <em>Cushion</em>]!) | <strong>Almohadón</strong> (Arabic <strong>Al-Mikhadda</strong> Large pillow!) = <em>Cushion</em>!<br>'
        '2. Slipcover: <strong>Funda</strong> (Protective sleeve!) + <strong>de Almohada</strong> (Of pillow!) = <em>Pillowcase</em>!',
        '1. Sofa pad: <strong>Gaddi</strong> (Prakrit <strong>Gaddika</strong> Soft padded seat!) = <em>Cushion</em>!<br>'
        '2. Slipcover: <strong>Takiye ka cover</strong> (<strong>Takiya</strong> Pillow + <strong>Cover</strong>!) / <strong>Khol</strong> (Outer detachable cloth shell!) = <em>Pillowcase</em>!'
    ),
    923: (
        '1. Tool: <strong>Peine</strong> (Latin <em>Pecten</em> Toothed comb [root of seashell <em>Pecten</em>]!) = <em>Comb (Noun)</em>!<br>'
        '2. Action: <strong>Peinar / peinarse</strong> (Run <em>Peine</em> teeth through hair!) = <em>Comb (Verb)</em>!',
        '1. Tool: <strong>Kanghi</strong> (Sanskrit <strong>Kankatika</strong> Toothed hair tool!) = <em>Comb (Noun)</em>!<br>'
        '2. Action: <strong>Baal banana</strong> (Style hair!) / <strong>Kanghi karna</strong> (Do the comb!) = <em>Comb (Verb)</em>!'
    ),
    928: (
        '<strong>Rancio / rancia</strong> (Latin <em>Rancidus</em> Sour/spoiled oil [root of <em>Rancid</em>]!) | '
        '<strong>Duro</strong> (Latin <em>Durus</em> Hardened [<em>Durable</em>]!) = <em>Stale</em>!',
        '<strong>Baasi</strong> (Sanskrit <strong>Vasita</strong> Kept overnight — day-old food!) / '
        '<strong>Sookha</strong> (Sanskrit <strong>Shushka</strong> Dried out hard!) = <em>Stale</em>!'
    ),
    930: (
        '<strong>Húmedo</strong> (Latin <em>Humidus</em> Wet vapor [root of <em>Humid</em>]!) | '
        '<strong>Mojado</strong> (Latin <em>Molliare</em> Soaked soft!) = <em>Damp / Moist</em>!',
        '<strong>Halka geela</strong> (<strong>Halka</strong> Light + <strong>Geela</strong> Wet!) / '
        '<strong>Nami wala</strong> (Persian <strong>Nam</strong> Moisture + <strong>Wala</strong> Holding!) = <em>Damp / Moist</em>!'
    ),
    932: (
        '<strong>Resbaladizo / resbaloso</strong> (<strong>Resbalar</strong> Slide/Glaze smoothly — slimy slick surface!) = <em>Slippery</em>!',
        '<strong>Fisalnewala</strong> (From <strong>Fisalna</strong> Slide/Lose footing + <strong>-wala</strong>!) / '
        '<strong>Chikna</strong> (Slick & oiled smooth!) = <em>Slippery</em>!'
    ),
    943: (
        '<strong>Peligroso / peligrosa</strong> (<strong>Peligro</strong> Peril [Latin <em>Periculum</em>] + <strong>-oso</strong> Full of = Full of peril!) = <em>Dangerous</em>!',
        '<strong>Khatarnak</strong> (Arabic <strong>Khatar</strong> Danger + Persian suffix <strong>-nak</strong> Filled with!) = <em>Dangerous</em>!'
    ),
    944: (
        '<strong>Barato / barata</strong> (Old Spanish <em>Baratar</em> Bargain/Trade down price!) | '
        '<strong>Económico</strong> (Greek <em>Oikonomia</em> Thrifty [<em>Economical</em>]!) = <em>Cheap</em>!',
        '<strong>Sasta / sasti</strong> (Sanskrit <strong>Swastha / Sasta</strong> Easy/Low-burden — cheap in price!) = <em>Cheap</em>!'
    ),
    945: (
        '<strong>Caro / cara</strong> (Latin <em>Carus</em> Dear/Precious [root of <em>Charity / Caress</em>]!) | '
        '<strong>Costoso</strong> (<strong>Costo</strong> Cost + <strong>-oso</strong> Full of!) = <em>Expensive</em>!',
        '<strong>Mehanga / mehangi</strong> (Sanskrit <strong>Mahargha</strong> <em>Maha</em> Great + <em>Argha</em> Price = Costly!) = <em>Expensive</em>!'
    ),
    951: (
        '<strong>Falso / falsa</strong> (Latin <em>Falsus</em> Deceitful [<em>False</em>]!) | '
        '<strong>Imitación</strong> (<em>Imitation</em> copy!) = <em>False / Fake</em>!',
        '<strong>Jhootha</strong> (Prakrit <strong>Jhuttha</strong> Untrue fabricated lie!) / '
        '<strong>Nakli</strong> (Arabic <strong>Naql</strong> Copied/Counterfeit!) = <em>False / Fake</em>!'
    ),
    952: (
        '<strong>Correcto</strong> (<strong>Con-</strong> + <strong>Rectus</strong> Made straight!) | '
        '<strong>Acertado</strong> (<strong>A-</strong> + <strong>Cierto</strong> Hit target right!) | '
        '<strong>Bien</strong> (Latin <em>Bene</em> Well!) = <em>Correct / Right</em>!',
        '<strong>Sahi</strong> (Arabic <strong>Sahih</strong> Healthy/Exact/Sound!) / '
        '<strong>Theek</strong> (Sanskrit <strong>Sthita</strong> Properly settled & right!) = <em>Correct / Right</em>!'
    ),
    953: (
        '<strong>Incorrecto</strong> (<strong>In-</strong> Not + Correct!) | '
        '<strong>Equivocado</strong> (<strong>Equi-</strong> Equal + <strong>Vocare</strong> Confused mistaking two!) | '
        '<strong>Mal</strong> (Latin <em>Malus</em> Badly!) = <em>Wrong</em>!',
        '<strong>Galat</strong> (Arabic <strong>Ghalat</strong> Error/Slip/Mistake!) = <em>Wrong</em>!'
    ),
    956: (
        '<strong>Normal</strong> (Square rule [<em>Normal</em>]!) | '
        '<strong>Común</strong> (Shared by all [<em>Common</em>]!) | '
        '<strong>Corriente</strong> (Running everywhere [<em>Current</em>]!) = <em>Normal / Common</em>!',
        '<strong>Aam</strong> (Arabic <strong>Amm</strong> General/Public — like everyday <em>Aam aadmi</em>!) = <em>Normal / Common</em>!'
    ),
    962: (
        '<strong>Aburrido / aburrida</strong> (<strong>Ab-</strong> Away + <strong>Horrere</strong> Shrink/Weary = Sick & tired of monotony!) = <em>Bored</em>!',
        '<strong>Bore hona</strong> (English loan <strong>Bore</strong> + <strong>Hona</strong> Feel/Become weary!) = <em>Bored</em>!'
    ),
    963: (
        '<strong>Preocupado / preocupada</strong> (<strong>Pre-</strong> Before + <strong>Ocupar</strong> Occupy mind = Preoccupied with anxious thought!) = <em>Worried</em>!',
        '<strong>Pareshan</strong> (Persian <strong>Pareshan</strong> Scattered/Disordered in mind = Troubled & anxious!) = <em>Worried</em>!'
    ),
    973: (
        '<strong>Frustrado / frustrada</strong> (Latin <em>Frustra</em> In vain — efforts blocked [<em>Frustrated</em>]!) = <em>Frustrated</em>!',
        '<strong>Pareshan</strong> (Persian Distressed/Bothered!) / '
        '<strong>Chidchida</strong> (<strong>Chidh</strong> Annoyance -> Irritable & cranky!) = <em>Frustrated</em>!'
    ),
    978: (
        '<strong>Dolor</strong> (Latin <em>Dolor</em> Ache [<em>Dolorous</em>]!) | '
        '<strong>Pena</strong> (Latin <em>Poena</em> Suffering [<em>Pain</em>]!) | '
        '<strong>Luto</strong> (Latin <em>Luctus</em> Mourning!) = <em>Sorrow / Grief</em>!',
        '<strong>Dukh</strong> (Sanskrit <strong>Duhkha [Tamil துக்கம் Thukkam = Sorrow!]</strong>!) / '
        '<strong>Gham</strong> (Arabic <strong>Ghamm</strong> Dark cloud weighing on chest!) = <em>Sorrow / Grief</em>!'
    ),
    984: (
        '<strong>Asco</strong> (Nauseating revulsion — root related to repulsive bile that turns the stomach!) = <em>Disgust</em>!',
        '<strong>Ghin</strong> (Sanskrit <strong>Ghrina</strong> Recoiling loathing!) / '
        '<strong>Chidh</strong> (Pricking disgust/irritation!) = <em>Disgust</em>!'
    ),
    987: (
        '<strong>Paciencia</strong> (Latin <em>Patientia</em> Endurance without snapping [root of <em>Patience</em>]!) = <em>Patience</em>!',
        '<strong>Sabr</strong> (Arabic <strong>Sabr</strong> Steady restraint — root behind famous proverb <em>"Sabr ka phal meetha"</em>!) = <em>Patience</em>!'
    ),
    988: (
        '<strong>Coraje</strong> (Latin <em>Cor</em> Heart [<em>Courage</em>]!) | '
        '<strong>Valentía</strong> (Latin <em>Valere</em> Be strong [<em>Valiant</em>]!) = <em>Courage</em>!',
        '<strong>Himmat</strong> (Arabic <strong>Himmah</strong> High-spirited resolve & daring nerve!) = <em>Courage</em>!'
    ),
    991: (
        '<strong>Grosero</strong> (<strong>Grueso</strong> Thick/Coarse + <strong>-ero</strong> = Unpolished blunt manners!) | '
        '<strong>Maleducado</strong> (<strong>Mal</strong> Badly + <strong>Educado</strong> Raised!) = <em>Rude</em>!',
        '<strong>Badtameez</strong> (Persian <strong>Bad</strong> Bad + Arabic <strong>Tameez</strong> Etiquette/Sense!) / '
        '<strong>Ukhar</strong> (Abrupt/Rough & snapped!) = <em>Rude</em>!'
    ),
    992: (
        '<strong>Tonto</strong> (Uncanny dullard!) | '
        '<strong>Estúpido</strong> (Latin <em>Stupidus</em> Stunned [<em>Stupid</em>]!) | '
        '<strong>Bobo</strong> (Latin <em>Balbus</em> Stammering simpleton!) = <em>Stupid / Foolish</em>!',
        '<strong>Bewaqoof</strong> (Persian <strong>Be-</strong> Without + Arabic <strong>Wuquf</strong> Sense!) / '
        '<strong>Moorkh</strong> (Sanskrit <strong>Murkha [Tamil மூர்க்கன்]</strong> Fool!) / '
        '<strong>Pagal</strong> (Crazy-headed!) = <em>Stupid / Foolish</em>!'
    ),
    999: (
        '<strong>Terco</strong> (Unbending stiff neck!) | '
        '<strong>Testarudo</strong> (<strong>Testa</strong> Hard Head + <strong>-udo</strong> = Hard-headed!) | '
        '<strong>Tozudo</strong> (Big-head obstinate!) = <em>Stubborn</em>!',
        '<strong>Ziddi</strong> (Arabic <strong>Zidd</strong> Contrarian persistence + <strong>-i</strong>!) / '
        '<strong>Adiyal</strong> (<strong>Adna</strong> Plant feet & refuse to budge!) = <em>Stubborn</em>!'
    ),
    1001: (
        '<strong>Torpe</strong> (Latin <em>Torpere</em> Numb/Sluggish [root of <em>Torpid / Torpor</em>] — fumbling hands!) = <em>Clumsy</em>!',
        '<strong>Anadi</strong> (Sanskrit <strong>An-</strong> Un- + <strong>Nadi/Skill</strong> = Amateur novice who fumbles!) = <em>Clumsy</em>!'
    ),
    1021: (
        '<strong>Llorar</strong> (Latin <em>Plorare</em> Cry aloud [<em>Implore / Deplore</em>]!) + '
        '<strong>a lágrima viva</strong> (With streaming live tears!) = <em>Weep</em>!',
        '<strong>Phoot-phoot kar rona</strong> (<strong>Phootna</strong> Burst open like a dam + <strong>Rona</strong> Cry = Sob openly!) = <em>Weep</em>!'
    ),
    1026: (
        '<strong>Mirar fijamente</strong> (Look fixedly!) | '
        '<strong>Clavar la vista</strong> (<strong>Clavar</strong> Nail/Pin + <strong>la Vista</strong> Sight — lock eyes!) = <em>Stare / Gaze</em>!',
        '<strong>Ghoorna</strong> (Heavy wide-eyed glares!) / '
        '<strong>Taakna</strong> (Peer steadily!) / '
        '<strong>Nigaah jamana</strong> (Plant gaze firmly!) = <em>Stare / Gaze</em>!'
    ),
    1031: (
        '<strong>Gemir</strong> (Latin <em>Gemere</em> Moan/Sigh!) | '
        '<strong>Quejarse</strong> (Latin <em>Quassare</em> Break out in aching groans + <strong>-se</strong>!) = <em>Groan</em>!',
        '<strong>Karahana</strong> (Moan in deep ache!) / '
        '<strong>Dard bhari aawaaz nikalna</strong> (Let out pain-filled voice!) = <em>Groan</em>!'
    ),
    1036: (
        '<strong>Arrodillarse</strong> (<strong>A-</strong> To + <strong>Rodilla</strong> Knee [Little wheel <em>Rotella</em>] + <strong>-se</strong>!) | '
        '<strong>Hincarse</strong> (<strong>Fincar</strong> Plant knee firmly!) = <em>Kneel</em>!',
        '<strong>Ghutne tekna</strong> (<strong>Ghutna</strong> Knee + <strong>Tekna</strong> Prop/Plant down on floor!) = <em>Kneel</em>!'
    ),
    1041: (
        '<strong>Hacer cosquillas</strong> (<strong>Hacer</strong> Make + expressive <strong>Cosquillas</strong> Light rib-prickles -> laughter!) = <em>Tickle</em>!',
        '<strong>Gudgudi karna</strong> (Reduplicated belly-laugh feel <strong>Gud-Gud</strong> + <strong>Karna</strong> Do!) = <em>Tickle</em>!'
    ),
    1044: (
        '<strong>Besar / beso</strong> (Latin <em>Basiare</em> Kiss politely/tenderly [archaic poetic <em>Buss</em>]!) = <em>Kiss</em>!',
        '<strong>Choomna</strong> (Sanskrit <strong>Chumbana</strong> Touch lips fondly!) = <em>Kiss</em>!'
    ),
    1049: (
        '<strong>Asistir a</strong> (<strong>Ad-</strong> To + <strong>Sistere</strong> Stand = Stand present [<em>Assist</em>]!) | '
        '<strong>Acudir</strong> (Come promptly to aid/event!) = <em>Attend</em>!',
        '<strong>Shaamil hona</strong> (Arabic <strong>Shamil</strong> Included/Joined + <strong>Hona</strong> Become!) = <em>Attend</em>!'
    ),
    1051: (
        '1. Join/append: <strong>Adjuntar</strong> (<em>Adjunct</em>!) | <strong>Unir</strong> (<em>Unite</em>!) | <strong>Pegar</strong> (Stick like <em>Pitch</em> glue!) = <em>Attach</em>!<br>'
        '2. Separate: <strong>Separar</strong> (<em>Separate</em>!) | <strong>Despegar</strong> (<strong>Des-</strong> Un- + Stick!) | <strong>Soltar</strong> (<em>Solution</em> Unfasten!) = <em>Detach</em>!',
        '1. Join/append: <strong>Jodna</strong> (Link together — joint <em>Jod</em>!) / <strong>Lagana</strong> (Affix/Apply onto!) = <em>Attach</em>!<br>'
        '2. Separate: <strong>Alag karna</strong> (Set apart!) / <strong>Hatana</strong> (Move aside/Remove!) = <em>Detach</em>!'
    ),
    1055: (
        '<strong>Chismear / chisme</strong> (Latin <em>Schisma</em> Split/Tale-bearing rumor [<em>Schism</em>]!) | '
        '<strong>Cotillear</strong> (Busybodies chirping idle secrets!) = <em>Gossip</em>!',
        '<strong>Chugli karna</strong> (Persian <strong>Chugli</strong> Whispering behind someone’s back!) / '
        '<strong>Idhar-udhar ki baatein karna</strong> (Here-there idle chatter!) = <em>Gossip</em>!'
    ),
    1056: (
        '1. Console: <strong>Consolar</strong> (<em>Console</em>!) | <strong>Reconfortar</strong> (<strong>Re-</strong> + <strong>Con-</strong> + <strong>Fortis</strong> Make strong again!) = <em>Comfort (Verb)</em>!<br>'
        '2. Physical ease: <strong>Comodidad</strong> (<em>Commodity</em>!) | <strong>Confort</strong> (<em>Comfort</em>!) = <em>Comfort (Noun)</em>!',
        '1. Console: <strong>Tasalli dena</strong> (Arabic <strong>Tasalli</strong> Calm soothing!) / <strong>Dilasa dena</strong> (Persian <strong>Dil-asa</strong> Rest the heart!) = <em>Comfort (Verb)</em>!<br>'
        '2. Physical ease: <strong>Aaram</strong> (Persian <strong>Aram [Tamil ஆறாமம் Ease!]</strong> Calm relief!) = <em>Comfort (Noun)</em>!'
    ),
    1058: (
        '<strong>Alabar</strong> (Vulgar Latin <em>Alapare</em> Brag/Exalt openly!) | '
        '<strong>Elogiar</strong> (Greek <em>Eulogia</em> Well-spoken tribute [root of <em>Eulogy</em>]!) = <em>Praise</em>!',
        '<strong>Tareef karna</strong> (Arabic <strong>Ta’rif</strong> Making known one’s fine qualities + <strong>Karna</strong> Do!) = <em>Praise</em>!'
    ),
    1065: (
        '<strong>Engañar</strong> (Fool someone!) | '
        '<strong>Estafar</strong> (Swindle con-job!) | '
        '<strong>Hacer trampa</strong> (Set a sneaky <em>Trap</em>!) = <em>Cheat / Deceive</em>!',
        '<strong>Dhokha dena</strong> (Prakrit <strong>Dhokha</strong> Illusion/Betrayal + Give!) / '
        '<strong>Ullu banana</strong> (Literally "Turn someone into an owl/fool"!) = <em>Cheat / Deceive</em>!'
    ),
    1075: (
        '<strong>Manejar</strong> (<strong>Mano</strong> Hand = Handle/Steer!) | '
        '<strong>Lidiar con</strong> (Grapple in arena!) | '
        '<strong>Sobrellevar</strong> (Carry burdens!) = <em>Handle / Cope</em>!',
        '<strong>Sambhalna</strong> (Hold steady/Balance under load!) / '
        '<strong>Jhelna</strong> (Absorb/Endure tough impact!) = <em>Handle / Cope</em>!'
    ),
    1077: (
        '1. Steer clear: <strong>Evitar</strong> (<em>Inevitable</em>!) | <strong>Esquivar</strong> (Sidestep dodge [<em>Eschew</em>]!) = <em>Avoid</em>!<br>'
        '2. Stop happening: <strong>Prevenir</strong> (<strong>Pre-</strong> Before + <strong>Venire</strong> Come [<em>Prevent</em>]!) | <strong>Impedir</strong> (<em>Impede</em>!) = <em>Prevent</em>!',
        '1. Steer clear: <strong>Bachna</strong> (Keep oneself safe!) / <strong>Taalna</strong> (Push off/Defer aside!) = <em>Avoid</em>!<br>'
        '2. Stop happening: <strong>Rokna</strong> (Halt/Block!) / <strong>Bachav karna</strong> (Safeguard against!) = <em>Prevent</em>!'
    ),
    1087: (
        '<strong>Nuez</strong> (Latin <em>Nux / Nucis</em> Hard shell nut [root of <em>Nucleus</em> = Kernel inside nut]!) = <em>Walnut</em>!',
        '<strong>Akhrot</strong> (Sanskrit <strong>Akshota</strong> Mountain brain-shaped nut!) = <em>Walnut</em>!'
    ),
    1095: (
        '<strong>Quejarse</strong> (Latin <em>Quassare</em> Break out in groans + reflexive <strong>-se</strong>!) | '
        '<strong>Reclamar</strong> (<strong>Re-</strong> Back + <strong>Clamar</strong> Call out [<em>Clamor</em>]!) = <em>Complain</em>!',
        '<strong>Shikayat karna</strong> (Arabic <strong>Shikayat</strong> Formal grievance [<strong>Tamil சகாயம்</strong> seeking redress!] + <strong>Karna</strong> File!) = <em>Complain</em>!'
    ),
    1098: (
        '<strong>Interrumpir</strong> (<strong>Inter-</strong> Between + <strong>Rumpere</strong> Break [<em>Rupture</em>] = Break mid-talk!) = <em>Interrupt</em>!',
        '<strong>Beech mein bolna</strong> (<strong>Beech mein</strong> In the middle + <strong>Bolna</strong> Speak!) / '
        '<strong>Tokna</strong> (Sanskrit <strong>Tuda</strong> Sharp poke cutting off a speaker!) = <em>Interrupt</em>!'
    ),
    1099: (
        '<strong>Animar</strong> (Latin <em>Anima</em> Soul [<em>Animate</em>]!) | '
        '<strong>Apoyar</strong> (<strong>Ad-</strong> To + <strong>Podium</strong> Prop/Pedestal = Hold someone steady!) = <em>Encourage / Support</em>!',
        '<strong>Hausla badhana</strong> (Arabic <strong>Hausla</strong> Resolve + <strong>Badhana</strong> Boost!) / '
        '<strong>Sahara dena</strong> (Sanskrit <strong>Sahayata [Tamil சகாயம் Aid!]</strong> Prop + Give!) = <em>Encourage / Support</em>!'
    ),
    1101: (
        '1. Notify facts: <strong>Informar</strong> (<em>Inform</em>!) | <strong>Avisar</strong> (<strong>Ad-</strong> + <strong>Visum</strong> Sight [<em>Advise</em>]!) = <em>Inform</em>!<br>'
        '2. Refer briefly: <strong>Mencionar</strong> (<em>Mention</em>!) | <strong>Nombrar</strong> (Call by <em>Name</em>!) = <em>Mention</em>!',
        '1. Notify facts: <strong>Batana</strong> (Sanskrit <strong>Varta</strong> Report/Tell clearly!) / <strong>Khabar dena</strong> (<strong>Khabar [Tamil கபர்]</strong> + Give!) = <em>Inform</em>!<br>'
        '2. Refer briefly: <strong>Zikr karna</strong> (Arabic <strong>Zikr</strong> Spoken remembrance/mention!) = <em>Mention</em>!'
    ),
    1105: (
        '1. Oppose words: <strong>Contradecir</strong> (<strong>Contra-</strong> Against + <strong>Decir</strong> Speak = Twin of <em>Contradict</em>!) = <em>Contradict</em>!<br>'
        '2. Dare: <strong>Desafiar</strong> (<strong>Des-</strong> Dis- + <strong>Fiar</strong> Faith [<em>Defy</em>]!) | <strong>Retar</strong> (Hurl bold <em>Reto / Retort</em>!) = <em>Challenge</em>!',
        '1. Oppose words: <strong>Ulta bolna</strong> (<strong>Ulta</strong> Opposite + <strong>Bolna</strong> Speak!) / <strong>Baat kaatna</strong> (Cut words mid-point!) = <em>Contradict</em>!<br>'
        '2. Dare: <strong>Chunauti dena</strong> (Prakrit <strong>Chunauti</strong> Pick/Single out in duel + <strong>Dena</strong> Throw down!) = <em>Challenge</em>!'
    ),
    1115: (
        '<strong>Carpintero</strong> (Latin <em>Carpentum</em> Two-wheeled timber wagon -> Woodshop maker [<em>Carpenter</em>]!) = <em>Carpenter</em>!',
        '<strong>Badhai</strong> (Sanskrit <strong>Vardhaki</strong> From <em>Vardh</em> Cut/Shape timber!) / '
        '<strong>Carpenter</strong> (Everyday English word!) = <em>Carpenter</em>!'
    ),
    1188: (
        '1. Capital: <strong>Inversión</strong> (<strong>In-</strong> Into + <strong>Vertere</strong> Turn = Put money to work [<em>Invest</em>]!) = <em>Investment</em>!<br>'
        '2. Peril: <strong>Riesgo</strong> (<em>Risk</em>!) | <strong>Peligro</strong> (Latin <em>Periculum</em> Trial [<em>Peril</em>]!) = <em>Risk</em>!',
        '1. Capital: <strong>Investment</strong> (English loan!) / <strong>Paisa lagana</strong> (<strong>Paisa</strong> Money + <strong>Lagana</strong> Put in!) = <em>Investment</em>!<br>'
        '2. Peril: <strong>Khatra</strong> (Arabic <strong>Khatar</strong> Warning hazard!) / <strong>Risk</strong> (English loan!) = <em>Risk</em>!'
    ),
    1203: (
        '<strong>Arrestar / arresto</strong> (<strong>Ad-</strong> To + <strong>Restare</strong> Stay back [<em>Arrest</em>]!) | '
        '<strong>Detener</strong> (<strong>De-</strong> Hold back + <strong>Tener</strong> Keep [<em>Detain</em>]!) = <em>Arrest</em>!',
        '<strong>Pakadna</strong> (Prakrit <strong>Pakkad</strong> Grip fast & hold!) / '
        '<strong>Giraftaar karna</strong> (Persian <strong>Giraft</strong> Seize + <strong>-aar</strong> Captive!) = <em>Arrest</em>!'
    ),
    1213: (
        '1. Armament: <strong>Arma</strong> (Latin <em>Arma</em> Gear/Shield [<em>Arms / Armory</em>]!) = <em>Weapon</em>!<br>'
        '2. Firearm: <strong>Pistola</strong> (<em>Pistol</em>!) | <strong>Rifle</strong> (Grooved gun barrel!) = <em>Gun</em>!',
        '1. Armament: <strong>Hathiyaar</strong> (<strong>Haath</strong> Hand + <strong>-iyaar</strong> Tool = Hand-held weapon!) = <em>Weapon</em>!<br>'
        '2. Firearm: <strong>Bandook</strong> (Arabic/Persian <strong>Bunduq</strong> Musket tube firing shot!) / <strong>Gun</strong> (English loan!) = <em>Gun</em>!'
    ),
    1255: (
        '1. Argument: <strong>Disputa</strong> (<em>Dispute</em>!) | <strong>Riña</strong> (Latin <em>Ringi</em> Snarl/Brawl!) = <em>Dispute</em>!<br>'
        '2. Clash: <strong>Conflicto</strong> (<strong>Con-</strong> Together + <strong>Fligere</strong> Strike [<em>Conflict</em>]!) = <em>Conflict</em>!<br>'
        '3. Emergency: <strong>Crisis</strong> (Greek <em>Krisis</em> Decisive turning point!) = <em>Crisis</em>!',
        '1. Argument: <strong>Jhagda</strong> (Prakrit <strong>Jhaggada</strong> Loud clashing quarrel!) = <em>Dispute</em>!<br>'
        '2. Clash: <strong>Takraav</strong> (Collision!) / <strong>Ladai</strong> (Fight!) = <em>Conflict</em>!<br>'
        '3. Emergency: <strong>Sankat</strong> (<strong>Tamil சங்கடம் Sangadam = Tight distress!</strong>) / <strong>Crisis</strong> (English loan!) = <em>Crisis</em>!'
    ),
}
