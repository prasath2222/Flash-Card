# Deep atomic word-by-word upgrades for Split 1 Part A (#1 - #264)

DATA_S1A = {
    1: (
        '<strong>Yo</strong> (Latin <em>Ego</em> Self/I — dropped the middle <em>g</em> and kept crisp <em>Yo</em>!) = <em>I</em>!',
        '<strong>Main</strong> (Sanskrit <strong>Maya</strong> By me — nasalized into crisp everyday <em>Main</em>!) = <em>I</em>!'
    ),
    2: (
        '1. Informal/casual: <strong>Tú</strong> (Latin <em>Tu</em> = <em>Thou / You</em>!) | '
        '<strong>Vos</strong> (Latin <em>Vos</em> Plural/Respect <em>You</em> — used informally across Argentina & Central America!) = <em>You (Informal)</em>!<br>'
        '2. Polite/formal: <strong>Usted</strong> (Contracted from <em>Vuestra Merced</em> "Your Mercy" — respectful singular!) = <em>You (Formal)</em>!<br>'
        '3. Plural/you all: <strong>Ustedes</strong> (Plural of <em>Usted</em>!) | '
        '<strong>Vosotros</strong> (<strong>Vos</strong> You + <strong>Otros</strong> Others — Spain plural!) = <em>You All</em>!',
        '1. Informal/casual: <strong>Tum</strong> (Sanskrit <strong>Tvam</strong> Thou — casual friendly <em>You</em>!) = <em>You (Informal)</em>!<br>'
        '2. Polite/formal: <strong>Aap</strong> (Sanskrit <strong>Atman</strong> Self/Honor — respectful <em>Your Honor</em>!) = <em>You (Formal)</em>!<br>'
        '3. Plural/you all: <strong>Tum log / aap log</strong> (<strong>Tum / Aap</strong> + <strong>Log [Tamil உலகம் = People!]</strong> = You folks!) = <em>You All</em>!'
    ),
    3: (
        '<strong>Él</strong> (Latin <em>Ille</em> That distant one — stressed accent <em>Él</em> = He vs <em>El</em> = The!) = <em>He</em>!',
        '<strong>Woh</strong> (Sanskrit <strong>Asau / Saha</strong> That distant person over there — points at <em>He / That</em>!) = <em>He</em>!'
    ),
    5: (
        '<strong>Eso</strong> (Latin <em>Ipsum</em> That neuter thing!) | '
        '<strong>Esto</strong> (Latin <em>Istum</em> This neuter thing!) = <em>It</em>!',
        '<strong>Yeh</strong> (Near-pointing demonstrative <em>This / It</em> right here!) / '
        '<strong>Woh</strong> (Far-pointing demonstrative <em>That / It</em> over there!) = <em>It</em>!'
    ),
    8: (
        '<strong>Me</strong> (Latin accusative/dative <em>Me</em> — same root as English <em>Me</em>!) = <em>Me</em>!',
        '<strong>Mujhe / mujhko</strong> (Oblique root <strong>Mujh</strong> [Sanskrit <em>Mahyam</em> To me] + <strong>-e / -ko</strong> Objective postposition!) = <em>Me</em>!'
    ),
    9: (
        '<strong>Lo</strong> (Latin <em>Illum</em> Direct object <em>Him</em>!) | '
        '<strong>Le</strong> (Latin <em>Illi</em> Indirect object <em>To Him</em>!) = <em>Him</em>!',
        '<strong>Use / usko</strong> (Oblique stem <strong>Us</strong> [from <em>Woh</em> That] + <strong>-e / -ko</strong> Objective marker = To/For Him!) = <em>Him</em>!'
    ),
    10: (
        '1. Object: <strong>La</strong> (Latin <em>Illam</em> Direct <em>Her</em>!) | '
        '<strong>Le</strong> (Latin <em>Illi</em> Indirect <em>To Her</em>!) = <em>Her (Object)</em>!<br>'
        '2. Possessive: <strong>Su / sus</strong> (Latin <em>Suus</em> Own — singular <em>Su</em> / plural <em>Sus</em>!) = <em>Her (Possessive)</em>!',
        '1. Object: <strong>Use / usko</strong> (Oblique stem <strong>Us</strong> + <strong>-e / -ko</strong> = Her!) = <em>Her (Object)</em>!<br>'
        '2. Possessive: <strong>Uska / uski / uske</strong> (<strong>Us</strong> + possessive genitive <strong>-ka / -ki / -ke</strong> agreeing with owned noun!) = <em>Her (Possessive)</em>!'
    ),
    12: (
        '<strong>Los / las</strong> (Latin <em>Illos / Illas</em> Direct masculine/feminine plural <em>Them</em>!) | '
        '<strong>Les</strong> (Latin <em>Illis</em> Indirect plural <em>To Them</em>!) = <em>Them</em>!',
        '<strong>Unhe / unko</strong> (Plural oblique stem <strong>Un</strong> [from <em>Woh</em>] + <strong>-he / -ko</strong> Objective marker!) = <em>Them</em>!'
    ),
    21: (
        '<strong>Mi / mis</strong> (Latin <em>Meus</em> — singular <em>Mi</em> + plural <em>Mis</em>, dropped accent vs <em>Mí</em>!) = <em>My</em>!',
        '<strong>Mera / meri / mere</strong> (From <strong>Main</strong> I + genitive suffix agreeing masc. <em>-a</em>, fem. <em>-i</em>, plural <em>-e</em>!) = <em>My</em>!'
    ),
    22: (
        '1. Informal: <strong>Tu / tus</strong> (Latin <em>Tuus</em> — singular <em>Tu</em> / plural <em>Tus</em> without accent!) = <em>Your (Informal)</em>!<br>'
        '2. Formal: <strong>Su / sus</strong> (Latin <em>Suus</em> — polite singular/plural <em>Su / Sus</em>!) = <em>Your (Formal)</em>!',
        '1. Informal: <strong>Tumhara / tumhari / tumhare</strong> (<strong>Tum</strong> You + possessive <strong>-hara / -hari / -hare</strong>!) = <em>Your (Informal)</em>!<br>'
        '2. Formal: <strong>Aapka / aapki / aapke</strong> (<strong>Aap</strong> Respectful You + <strong>-ka / -ki / -ke</strong>!) = <em>Your (Formal)</em>!'
    ),
    23: (
        '<strong>Su / sus</strong> (Latin <em>Suus</em> — singular <em>Su</em> / plural <em>Sus</em> owned by him!) = <em>His</em>!',
        '<strong>Uska / uski / uske</strong> (Oblique <strong>Us</strong> + genitive <strong>-ka / -ki / -ke</strong>!) = <em>His</em>!'
    ),
    24: (
        '<strong>Nuestro / nuestra / nuestros / nuestras</strong> (Latin <em>Noster</em> [root of <em>Nostrum</em>] inflected for 4 genders/numbers!) = <em>Our</em>!',
        '<strong>Hamara / hamari / hamare</strong> (<strong>Hum</strong> We + genitive <strong>-ara / -ari / -are</strong>!) = <em>Our</em>!'
    ),
    25: (
        '<strong>Su / sus</strong> (Latin <em>Suus</em> — singular <em>Su</em> / plural <em>Sus</em> belonging to them!) = <em>Their</em>!',
        '<strong>Unka / unki / unke</strong> (Plural oblique <strong>Un</strong> + genitive <strong>-ka / -ki / -ke</strong>!) = <em>Their</em>!'
    ),
    26: (
        '<strong>Su / sus</strong> (Latin <em>Suus</em> — belonging to an object/animal: singular <em>Su</em> / plural <em>Sus</em>!) = <em>Its</em>!',
        '<strong>Iska / iski / iske</strong> (Near oblique <strong>Is</strong> [from <em>Yeh</em>] + genitive <strong>-ka / -ki / -ke</strong>!) = <em>Its</em>!'
    ),
    27: (
        '<strong>Mío / mía / míos / mías</strong> (Stressed Latin <em>Meus</em> standalone possessive matching 4 genders/numbers!) = <em>Mine</em>!',
        '<strong>Mera / meri / mere</strong> (Same stem <em>Mer-</em> stands alone for <em>Mine</em>: masc. <em>-a</em>, fem. <em>-i</em>, plural <em>-e</em>!) = <em>Mine</em>!'
    ),
    28: (
        '1. Informal: <strong>Tuyo / tuya / tuyos / tuyas</strong> (Stressed Latin <em>Tuus</em> standalone <em>Yours</em> across 4 forms!) = <em>Yours (Informal)</em>!<br>'
        '2. Formal: <strong>Suyo / suya / suyos / suyas</strong> (Stressed Latin <em>Suus</em> standalone polite <em>Yours</em>!) = <em>Yours (Formal)</em>!',
        '1. Informal: <strong>Tumhara / tumhari / tumhare</strong> (<strong>Tum</strong> + standalone <strong>-hara / -hari / -hare</strong>!) = <em>Yours (Informal)</em>!<br>'
        '2. Formal: <strong>Aapka / aapki / aapke</strong> (<strong>Aap</strong> + standalone <strong>-ka / -ki / -ke</strong>!) = <em>Yours (Formal)</em>!'
    ),
    29: (
        '<strong>Suyo / suya / suyos / suyas</strong> (Stressed Latin <em>Suus</em> standalone <em>Hers</em> — agrees with item owned, not owner!) = <em>Hers</em>!',
        '<strong>Uska / uski / uske</strong> (Oblique <strong>Us</strong> + <strong>-ka / -ki / -ke</strong> standing alone!) = <em>Hers</em>!'
    ),
    31: (
        '<strong>El suyo / la suya / los suyos / las suyas</strong> (Article <em>El/La/Los/Las</em> + Stressed <em>Suyo/a/os/as</em> = The one of theirs!) = <em>Theirs</em>!',
        '<strong>Unka / unki / unke</strong> (Plural <strong>Un</strong> + <strong>-ka / -ki / -ke</strong>!) = <em>Theirs</em>!'
    ),
    33: (
        '<strong>Este / esta / esto</strong> (Latin <em>Iste</em> Near-speaker — masc. <em>Este</em>, fem. <em>Esta</em>, neutral <em>Esto</em>!) = <em>This</em>!',
        '<strong>Yeh / is</strong> (Direct proximal <em>Yeh</em> + oblique stem <em>Is</em> before postpositions like <em>Is mein</em>!) = <em>This</em>!'
    ),
    34: (
        '<strong>Ese / esa / eso</strong> (Medium distance <em>Ipsum</em>!) | '
        '<strong>Aquel / aquella</strong> (Latin <em>Eccum Ille</em> Far over yonder!) = <em>That</em>!',
        '<strong>Woh / us</strong> (Direct distal <em>Woh</em> + oblique stem <em>Us</em> before postpositions like <em>Us par</em>!) = <em>That</em>!'
    ),
    36: (
        '<strong>Esos / esas</strong> (Plural near-far!) | '
        '<strong>Aquellos / aquellas</strong> (Plural distant yonder!) = <em>Those</em>!',
        '<strong>Woh / un</strong> (Direct plural <em>Woh</em> + oblique plural <em>Un</em> before postpositions like <em>Un logon</em>!) = <em>Those</em>!'
    ),
    37: (
        '<strong>Alguien</strong> (Latin <em>Aliquem</em> = <em>Alius</em> Other + <em>Quem</em> Whom = Some person!) = <em>Someone / Somebody</em>!',
        '<strong>Koi</strong> (Sanskrit <strong>Ko\'pi</strong> Whosoever — indefinite single person!) = <em>Someone / Somebody</em>!'
    ),
    39: (
        '<strong>Algo</strong> (Latin <em>Aliquod</em> = <em>Alius</em> Other + <em>Quod</em> What = Some indefinite thing!) = <em>Something</em>!',
        '<strong>Kuch</strong> (Sanskrit <strong>Kinchit</strong> A small bit/Something!) / '
        '<strong>Koi cheez</strong> (<strong>Koi</strong> Some + <strong>Cheez</strong> Thing!) = <em>Something</em>!'
    ),
    40: (
        '<strong>En algún lugar</strong> (<strong>En</strong> In + <strong>Algún</strong> Some + <strong>Lugar</strong> Place [<em>Local</em>]!) | '
        '<strong>En alguna parte</strong> (<strong>Parte</strong> Part/Spot!) = <em>Somewhere</em>!',
        '<strong>Kahin</strong> (From <strong>Kahan</strong> Where + indef. <strong>-hin</strong>!) / '
        '<strong>Kisi jagah</strong> (<strong>Kisi</strong> Oblique <em>Koi</em> + <strong>Jagah</strong> Place!) = <em>Somewhere</em>!'
    ),
    41: (
        '<strong>Cualquiera</strong> (<strong>Cual</strong> Which + <strong>Quiera</strong> You want — literally "Whichever you wish"!) | '
        '<strong>Alguien</strong> (Some person!) = <em>Anyone / Anybody</em>!',
        '<strong>Koi bhi</strong> (<strong>Koi</strong> Someone + emphatic <strong>Bhi</strong> Even/At all = Any person!) = <em>Anyone / Anybody</em>!'
    ),
    44: (
        '<strong>Todos</strong> (Latin <em>Totus</em> All/Whole [<em>Total</em>]!) | '
        '<strong>Todo el mundo</strong> (Literally "The whole world"!) = <em>Everyone / Everybody</em>!',
        '<strong>Sab</strong> (Sanskrit <strong>Sarva [Tamil சர்வம் Sarvam = All!]</strong>!) / '
        '<strong>Har koi</strong> (Persian <strong>Har</strong> Every + <strong>Koi</strong> One!) = <em>Everyone / Everybody</em>!'
    ),
    47: (
        '<strong>Nadie</strong> (Latin <em>(Homines) Nati</em> "[Not a soul] Born" — not one person born!) = <em>No one / Nobody</em>!',
        '<strong>Koi nahi</strong> (<strong>Koi</strong> Anyone + <strong>Nahi</strong> Not [Sanskrit <em>Na-hi</em>]!) = <em>No one / Nobody</em>!'
    ),
    52: (
        '<strong>Todo / toda / todos / todas</strong> (Latin <em>Totus</em> Whole/Total — all 4 gender/number forms!) = <em>All</em>!',
        '<strong>Sab</strong> (Sanskrit <strong>Sarva [Tamil சர்வம் = All]</strong>!) / '
        '<strong>Saara</strong> (Whole/Entire mass from end to end!) = <em>All</em>!'
    ),
    53: (
        '<strong>Cada</strong> (Greek <em>Kata</em> Down-by-item individually!) | '
        '<strong>Todos los</strong> (Plural <em>Totus</em> + <em>Los</em> = Every single!) = <em>Every / Each</em>!',
        '<strong>Har / har ek</strong> (Persian <strong>Har</strong> Every + <strong>Ek</strong> One [Sanskrit <em>Eka</em>] = Each one!) = <em>Every / Each</em>!'
    ),
    54: (
        '<strong>Ambos / ambas</strong> (Latin <em>Ambo</em> Both [root of <em>Ambidextrous</em>]!) | '
        '<strong>Los dos / las dos</strong> (Literally "The two"!) = <em>Both</em>!',
        '<strong>Dono</strong> (Sanskrit <strong>Dvau</strong> Two + <strong>-no</strong> Collective pair = Both together!) = <em>Both</em>!'
    ),
    57: (
        '<strong>Algunos / algunas</strong> (Latin <em>Aliquis Unus</em> Some few!) | '
        '<strong>Un poco de</strong> (<strong>Un</strong> A + <strong>Poco</strong> Little [<em>Poco</em>] + <strong>de</strong>!) = <em>Some</em>!',
        '<strong>Kuch</strong> (Sanskrit <strong>Kinchit</strong> A small indefinite share!) / '
        '<strong>Thoda</strong> (Sanskrit <strong>Stoka</strong> Small bit/drop!) = <em>Some</em>!'
    ),
    58: (
        '<strong>Suficiente</strong> (<strong>Sub-</strong> Under + <strong>Facere</strong> Make = Meets the full mark [<em>Sufficient</em>]!) | '
        '<strong>Bastante</strong> (From <strong>Bastar</strong> Suffice — plenty!) = <em>Enough</em>!',
        '<strong>Kaafi</strong> (Arabic <strong>Kafi</strong> Completing need — ample!) / '
        '<strong>Bas</strong> (Persian <strong>Bas</strong> Stop here / That’s plenty!) = <em>Enough</em>!'
    ),
    61: (
        '<strong>Otro / otra / otros / otras</strong> (Latin <em>Alter</em> Other of two [<em>Alter / Alternative</em>]!) | '
        '<strong>Demás</strong> (<strong>De</strong> Of + <strong>Más</strong> More = The remaining others!) = <em>Other</em>!',
        '<strong>Doosra / doosri / doosre</strong> (<strong>Do</strong> Two + <strong>-sra</strong> Ordinal = The 2nd / Other, inflecting <em>-a / -i / -e</em>!) = <em>Other</em>!'
    ),
    62: (
        '<strong>Otro / otra (más)</strong> (Latin <em>Alter</em> + <strong>Más</strong> More = One extra other!) = <em>Another</em>!',
        '<strong>Ek aur</strong> (<strong>Ek</strong> One + <strong>Aur</strong> More/And!) / '
        '<strong>Doosra</strong> (<strong>Do</strong> Two + <strong>-sra</strong> = Another one!) = <em>Another</em>!'
    ),
    63: (
        '<strong>Tal</strong> (Latin <em>Talis</em> Of such kind [root of <em>Retaliate</em> — pay back "such" like for like]!) = <em>Such</em>!',
        '<strong>Aisa / aisi / aise</strong> (Demonstrative <strong>Is</strong> This + suffix <strong>-sa</strong> Like = Of this kind!) = <em>Such</em>!'
    ),
    64: (
        '<strong>Mismo / misma / mismos / mismas</strong> (Latin <em>Metipsimus</em> Most-self-same!) | '
        '<strong>Igual</strong> (Latin <em>Aequalis</em> Level/Even [<em>Equal</em>]!) = <em>Same</em>!',
        '<strong>Vahi</strong> (<strong>Woh</strong> That + emphatic <strong>-hi</strong> Exact very one!) / '
        '<strong>Ek jaisa</strong> (<strong>Ek</strong> One + <strong>Jaisa</strong> Like = Identical!) = <em>Same</em>!'
    ),
    65: (
        '<strong>Diferente</strong> (<strong>Dis-</strong> Apart + <strong>Ferre</strong> Carry = Carried apart!) | '
        '<strong>Distinto</strong> (<strong>Dis-</strong> Apart + <strong>Stinguere</strong> Mark/Prick [<em>Distinct</em>]!) = <em>Different</em>!',
        '<strong>Alag</strong> (Sanskrit <strong>A-lagna</strong> Un-attached/Set apart from the rest!) = <em>Different</em>!'
    ),
    66: (
        '<strong>Varios / varias</strong> (Latin <em>Varius</em> Spotted/Diverse [<em>Various</em>] = More than two!) = <em>Several</em>!',
        '<strong>Kayi / kayi saare</strong> (Sanskrit <strong>Kati</strong> How many/Multiple + <strong>Saare</strong> Whole bunch!) = <em>Several</em>!'
    ),
    67: (
        '<strong>Muchos / muchas</strong> (Latin <em>Multus</em> [<em>Multi-</em>] Plural countable = Many!) = <em>Many</em>!',
        '<strong>Bohot saare</strong> (Sanskrit <strong>Bahu</strong> Abundant + <strong>Saare</strong> Whole lot!) / '
        '<strong>Kayi</strong> (Multiple several!) = <em>Many</em>!'
    ),
    68: (
        '<strong>Mucho / mucha</strong> (Latin <em>Multus</em> [<em>Multi-</em>] Singular mass quantity!) = <em>Much</em>!',
        '<strong>Bohot</strong> (Sanskrit <strong>Bahu</strong> Plentiful!) / '
        '<strong>Zyaada</strong> (Arabic <strong>Ziyadah</strong> Increase/Surplus — excess amount!) = <em>Much</em>!'
    ),
    69: (
        '<strong>Pocos / pocas</strong> (Latin <em>Paucus</em> Small/Scant [root of <em>Paucity</em> & musical <em>Poco</em>]!) = <em>Few</em>!',
        '<strong>Kuch</strong> (Some small amount!) / '
        '<strong>Thode se</strong> (<strong>Thoda</strong> Small + <strong>-e se</strong> Just a few!) = <em>Few</em>!'
    ),
    75: (
        '<strong>Quién / a quién</strong> (Latin <em>Quem</em> Whom/Who [K-interrogative; <em>A quién</em> = To whom]!) = <em>Who / Whom</em>!',
        '<strong>Kaun / kisse / kisko</strong> (K-question base <strong>Kaun</strong> Who + oblique <strong>Kis</strong> + <strong>-se / -ko</strong> By/To whom!) = <em>Who / Whom</em>!'
    ),
    76: (
        '<strong>Cuál / cuáles</strong> (Latin <em>Qualis</em> Of which sort [root of <em>Quality</em>]!) | '
        '<strong>Qué</strong> (Latin <em>Quid</em> What/Which [root of <em>Quiddity</em>] before a noun!) = <em>Which</em>!',
        '<strong>Kaunsa / kaunsi</strong> (<strong>Kaun</strong> Which + <strong>-sa / -si</strong> Like/Select — masc. vs fem.!) = <em>Which</em>!'
    ),
    77: (
        '<strong>Cómo</strong> (Latin <em>Quomodo</em> = <em>Quo</em> In what + <em>Modo</em> Way/Mode!) = <em>How</em>!',
        '<strong>Kaise</strong> (K-question stem <strong>K-</strong> + manner suffix <strong>-aise</strong> In what way!) = <em>How</em>!'
    ),
    78: (
        '<strong>Cuánto / cuánta</strong> (Latin <em>Quantus</em> How great [root of <em>Quantity</em>]!) = <em>How much</em>!',
        '<strong>Kitna / kitni</strong> (K-question stem <strong>Kit-</strong> Amount + <strong>-na / -ni</strong> agreeing masc./fem.!) = <em>How much</em>!'
    ),
    79: (
        '<strong>Cuántos / cuántas</strong> (Plural of <em>Cuánto</em> [Latin <em>Quantus</em> = Countable quantity]!) = <em>How many</em>!',
        '<strong>Kitne / kitni</strong> (Plural K-question <strong>Kit-</strong> + plural <strong>-ne</strong> / fem. <strong>-ni</strong>!) = <em>How many</em>!'
    ),
    87: (
        '<strong>Hacer</strong> (Latin <em>Facere</em> Make/Perform [root of <em>Factory / Fact</em>] — Latin initial <em>f-</em> shifted to silent <em>h-</em>!) = <em>Do / Make</em>!',
        '<strong>Karna</strong> (Sanskrit <strong>Kri [root of Karma = Action / Tamil காரியம் Kaariyam!]</strong> + <strong>-na</strong> Verb!) = <em>Do</em>!'
    ),
    88: (
        '1. Ability/permission: <strong>Poder</strong> (Latin <em>Potere</em> Be powerful [<em>Potent / Power</em>]!) = <em>Can</em>!<br>'
        '2. Metal container: <strong>Lata</strong> (Wide flat tin-sheet metal strip -> sealed food/soda tin!) = <em>Can (Tin)</em>!',
        '1. Ability/permission: <strong>Sakna</strong> (Sanskrit <strong>Shak [Tamil சக்தி Sakthi = Power/Ability!]</strong>) / '
        '<strong>Paana</strong> (<strong>Paa-</strong> Obtain ability to manage!) = <em>Can</em>!<br>'
        '2. Metal container: <strong>Dibba</strong> (<strong>Spoken Tamil டப்பா Dabba = Box/Tin Can!</strong>) = <em>Can (Tin)</em>!'
    ),
    93: (
        '<strong>Tener que</strong> (<strong>Tener</strong> Hold + <strong>Que</strong> That = Have to!) | '
        '<strong>Deber</strong> (Latin <em>Debere</em> Owe [<em>Debt / Duty</em>] = Ought/Must!) = <em>Must</em>!',
        '<strong>Zaroor ... chahiye</strong> (<strong>Zaroor [Tamil ஜரூர் Necessary!]</strong> + <strong>Chahiye</strong> Ought) / '
        '<strong>Padna</strong> (Fall upon one as an obligation!) = <em>Must</em>!'
    ),
    94: (
        '<strong>Poder</strong> (Latin <em>Potere</em> Be possible [<em>Potential</em>]!) | '
        '<strong>Puede que</strong> (It can be that!) | '
        '<strong>Tal vez</strong> (<strong>Tal</strong> Such + <strong>Vez</strong> Time/Turn = Perhaps!) = <em>May / Might</em>!',
        '<strong>Shayad</strong> (Persian <strong>Shayad</strong> "It is fitting/possible" = Perhaps!) / '
        '<strong>Sakna</strong> (<strong>Shak [Tamil சக்தி = Capability/Possibility!]</strong>) = <em>May / Might</em>!'
    ),
    95: (
        '1. Verb - require: <strong>Necesitar</strong> (<strong>Ne-</strong> Not + <strong>Cedere</strong> Yield = Unavoidable [<em>Necessitate</em>]!) = <em>Need (Verb)</em>!<br>'
        '2. Noun - requirement: <strong>Necesidad</strong> (<strong>Neces-</strong> Unavoidable + <strong>-dad</strong> Quality [<em>Necessity</em>]!) = <em>Need (Noun)</em>!',
        '1. Verb - require: <strong>Zaroorat hona</strong> (Arabic <strong>Zaroorat [Tamil ஜரூர் = Urgent Need!]</strong> + <strong>Hona</strong> Exist!) = <em>Need (Verb)</em>!<br>'
        '2. Noun - requirement: <strong>Zaroorat</strong> (Arabic <strong>Darurah [Spoken Tamil ஜரூர் = Necessity!]</strong>!) = <em>Need (Noun)</em>!'
    ),
    96: (
        '<strong>Solía</strong> (Latin <em>Solere</em> Be accustomed — imperfect habitual past!) | '
        '<strong>Antes hacía</strong> (<strong>Antes</strong> Before + <strong>Hacía</strong> Used to do!) = <em>Used to</em>!',
        '<strong>Kiya karta tha</strong> (<strong>Kiya</strong> Done + <strong>Karta</strong> Habitual doer + <strong>Tha</strong> Was!) / '
        '<strong>Aadat thi</strong> (Arabic <strong>Aadat</strong> Habit + <strong>Thi</strong> Was!) = <em>Used to</em>!'
    ),
    98: (
        '<strong>Cuando sea</strong> (<strong>Cuando</strong> When + <strong>Sea</strong> May be!) | '
        '<strong>Cada vez que</strong> (<strong>Cada</strong> Each + <strong>Vez</strong> Time + <strong>Que</strong> That!) = <em>Whenever</em>!',
        '<strong>Jab bhi</strong> (<strong>Jab</strong> When [relative <em>J-</em>] + <strong>Bhi</strong> Ever/Also = Any time when!) = <em>Whenever</em>!'
    ),
    99: (
        '<strong>En</strong> (Latin <em>In</em> Inside/At!) | '
        '<strong>Dentro de</strong> (<strong>De-</strong> + <strong>Intro</strong> Inner/Inside + <strong>de</strong>!) = <em>In</em>!',
        '<strong>Mein</strong> (Sanskrit <strong>Madhye</strong> In the midst/middle of!) / '
        '<strong>Ke andar</strong> (Sanskrit <strong>Antar [Tamil அந்தரங்கம் = Inner!]</strong>) = <em>In</em>!'
    ),
    100: (
        '1. Surface contact: <strong>Sobre</strong> (Latin <em>Super</em> Above/On top!) | '
        '<strong>En</strong> (At/On!) | <strong>Encima de</strong> (<strong>En</strong> + <strong>Cima</strong> Top/Summit!) = <em>On</em>!<br>'
        '2. Active/working: <strong>Encendido</strong> (<strong>En-</strong> + <strong>Cender</strong> Kindle [<em>Incendiary</em>]!) | '
        '<strong>Prendido</strong> (Caught/Switched lit!) = <em>On (Active)</em>!',
        '1. Surface contact: <strong>Par</strong> (Sanskrit <strong>Upari</strong> Upon/At!) / '
        '<strong>Upar</strong> (Sanskrit <strong>Upari [Upper]</strong> = On top!) = <em>On</em>!<br>'
        '2. Active/working: <strong>Chalu</strong> (From <strong>Chalna</strong> Walk/Move -> Running/Active!) = <em>On (Active)</em>!'
    ),
    101: (
        '1. Specific place: <strong>En</strong> (Latin <em>In</em> Pinpointing location at!) = <em>At (Place)</em>!<br>'
        '2. Specific time: <strong>A la / a las</strong> (<strong>A</strong> Toward + Hour article <strong>La/Las</strong> — <em>A la 1</em> / <em>A las 3</em>!) = <em>At (Time)</em>!',
        '1. Specific place: <strong>Par / mein</strong> (<strong>Par</strong> Upon/At spot | <strong>Mein</strong> Inside/In!) = <em>At (Place)</em>!<br>'
        '2. Specific time: <strong>Baje / par</strong> (<strong>Bajna</strong> Strike clock chime -> O’clock! | <strong>Par</strong> At hour!) = <em>At (Time)</em>!'
    ),
    109: (
        '1. Regarding: <strong>Sobre</strong> (Latin <em>Super</em> Resting over a topic!) | '
        '<strong>De</strong> (Of/Concerning!) = <em>About (Topic)</em>!<br>'
        '2. Approximate: <strong>Alrededor de</strong> (<strong>Al + Rededor</strong> Circle around!) | '
        '<strong>Como</strong> (Latin <em>Quomodo</em> Like/Roughly — comparable!) = <em>About (Approx)</em>!',
        '1. Regarding: <strong>Ke baare mein</strong> (Persian <strong>Baarah</strong> Point/Subject + <strong>Mein</strong> In = Concerning!) = <em>About (Topic)</em>!<br>'
        '2. Approximate: <strong>Lagbhag</strong> (<strong>Lag-</strong> Touching + <strong>Bhag</strong> Share — almost touching!) / '
        '<strong>Kareeb</strong> (Arabic <strong>Qarib</strong> Close/Near!) = <em>About (Approx)</em>!'
    ),
    110: (
        '<strong>Dentro de</strong> (<strong>De- + Intro</strong> Within/Inside!) | '
        '<strong>Hacia adentro</strong> (<strong>Hacia</strong> Toward + <strong>Adentro</strong> Inside!) = <em>Into</em>!',
        '<strong>Ke andar</strong> (Sanskrit <strong>Antar</strong> Inside!) / '
        '<strong>Mein</strong> (Sanskrit <strong>Madhye</strong> In the middle/Into!) = <em>Into</em>!'
    ),
    112: (
        '<strong>Arriba</strong> (<strong>Ad-</strong> To + <strong>Ripa</strong> Riverbank/High shore -> Climb up!) | '
        '<strong>Hacia arriba</strong> (<strong>Hacia</strong> Toward + Up!) = <em>Up</em>!',
        '<strong>Upar</strong> (Sanskrit <strong>Upari</strong> Above — exact Indo-European cognate of English <em>Up / Over / Upper</em>!) = <em>Up</em>!'
    ),
    113: (
        '<strong>Abajo</strong> (<strong>A-</strong> To + <strong>Bajo</strong> Low [<em>Bass / Base</em>]!) | '
        '<strong>Hacia abajo</strong> (<strong>Hacia</strong> Toward + Down!) = <em>Down</em>!',
        '<strong>Neeche</strong> (Sanskrit <strong>Nicha = Low/Underneath [Tamil நீச்சம் = Low!]</strong>!) = <em>Down</em>!'
    ),
    114: (
        '1. Above/across: <strong>Encima de</strong> (<strong>En + Cima</strong> Summit!) | '
        '<strong>Por encima</strong> (Across the top!) = <em>Over</em>!<br>'
        '2. Finished: <strong>Terminado</strong> (<strong>Terminus</strong> End boundary [<em>Terminate</em>]!) | '
        '<strong>Acabado</strong> (<strong>A- + Cabo</strong> Cape/End [reached the end!]) = <em>Over (Finished)</em>!',
        '1. Above/across: <strong>Ke upar se</strong> (<strong>Upar</strong> Upper + <strong>Se</strong> Across from above!) = <em>Over</em>!<br>'
        '2. Finished: <strong>Khatam</strong> (Arabic <strong>Khatm</strong> Seal stamped on a closed letter = Ended!) = <em>Over (Finished)</em>!'
    ),
    115: (
        '<strong>Debajo de</strong> (<strong>De-</strong> Down + <strong>Bajo</strong> Low [<em>Base</em>]!) | '
        '<strong>Bajo</strong> (Low beneath!) = <em>Under / Below</em>!',
        '<strong>Ke neeche</strong> (Sanskrit <strong>Nicha</strong> Beneath/Low bottom!) = <em>Under / Below</em>!'
    ),
    116: (
        '<strong>Encima de</strong> (<strong>En</strong> On + <strong>Cima</strong> Summit/Peak [Greek <em>Kyma</em> Swell/Top]!) = <em>Above</em>!',
        '<strong>Ke upar / upar</strong> (Sanskrit <strong>Upari</strong> Higher/Upper — Indo-European twin of <em>Upper</em>!) = <em>Above</em>!'
    ),
    117: (
        '<strong>Entre (dos)</strong> (Latin <em>Inter</em> Between [root of <em>Inter-</em>] + <strong>Dos</strong> Two!) = <em>Between</em>!',
        '<strong>Ke beech mein (do ke beech)</strong> (Sanskrit <strong>Vich</strong> Separation/Middle Gap + <strong>Do</strong> Two!) = <em>Between</em>!'
    ),
    119: (
        '<strong>A través de</strong> (<strong>Trans-</strong> + <strong>Vertere</strong> Cross-turned [<em>Traverse</em>]!) | '
        '<strong>Por</strong> (Latin <em>Per / Pro</em> Through/By path!) = <em>Through</em>!',
        '<strong>Ke aar-paar</strong> (<strong>Aar</strong> Near bank + <strong>Paar</strong> Far shore = Crossing right through!) / '
        '<strong>Mein se</strong> (<strong>Mein</strong> In + <strong>Se</strong> Out through!) = <em>Through</em>!'
    ),
    120: (
        '<strong>Al otro lado de</strong> (<strong>Al otro</strong> To the other + <strong>Lado</strong> Side [<em>Lateral</em>]!) | '
        '<strong>A través de</strong> (Crossing diagonally [<em>Traverse</em>]!) = <em>Across</em>!',
        '<strong>Ke paar / us paar</strong> (Sanskrit <strong>Para</strong> Far shore [<strong>Tamil அக்கரை-இக்கரை</strong>] + <strong>Us</strong> That!) = <em>Across</em>!'
    ),
    121: (
        '<strong>A lo largo de</strong> (<strong>Largo</strong> Length — running along the whole length!) | '
        '<strong>Por</strong> (Alongside via path!) = <em>Along</em>!',
        '<strong>Ke saath-saath</strong> (<strong>Saath</strong> Company — doubled <em>Together-together</em>!) / '
        '<strong>Kinaare-kinaare</strong> (Persian <strong>Kinar</strong> Edge/Bank — along the border!) = <em>Along</em>!'
    ),
    122: (
        '<strong>Alrededor de</strong> (<strong>Al</strong> + <strong>Re-</strong> Again + <strong>Dor</strong> Back/Circle = Encircling!) | '
        '<strong>Por ahí</strong> (By thereabouts!) = <em>Around</em>!',
        '<strong>Aas-paas</strong> (Near side + close side!) / '
        '<strong>Ke chaaron or</strong> (<strong>Chaaron</strong> All four + <strong>Or</strong> Directions!) = <em>Around</em>!'
    ),
    124: (
        '<strong>Delante de</strong> (<strong>De- + In- + Ante</strong> Before/Ahead!) | '
        '<strong>Frente a</strong> (<strong>Frente</strong> Forehead [<em>Front</em>]!) = <em>In front of</em>!',
        '<strong>Ke saamne</strong> (Sanskrit <strong>Sammukha [Tamil சமுகம் = Face-to-face!]</strong>!) / '
        '<strong>Ke aage</strong> (Sanskrit <strong>Agra</strong> Tip/Ahead!) = <em>In front of</em>!'
    ),
    126: (
        '<strong>Cerca de</strong> (Latin <em>Circa</em> Inside a tight circle [<em>Circus / Circle</em>] = Close by!) = <em>Near</em>!',
        '<strong>Ke paas</strong> (Sanskrit <strong>Parshva</strong> By the flank/side!) / '
        '<strong>Nazdeek</strong> (Persian <strong>Nazdik</strong> Close/Nearby!) = <em>Near</em>!'
    ),
    127: (
        '<strong>Lejos</strong> (Latin <em>Laxus</em> Stretched out wide/loose -> Distant!) = <em>Far</em>!',
        '<strong>Door</strong> (Sanskrit <strong>Dura = Far off [Tamil தூரம் Dooram = Distance!]</strong>!) = <em>Far</em>!'
    ),
    128: (
        '<strong>Dentro / adentro</strong> (Latin <em>De-Intro</em> Within/Inward!) = <em>Inside</em>!',
        '<strong>Andar / ke andar</strong> (Sanskrit <strong>Antar [Tamil அந்தரம்]</strong> Inner space!) = <em>Inside</em>!'
    ),
    129: (
        '<strong>Fuera / afuera</strong> (Latin <em>Foris</em> Out of doors [root of <em>Foreign / Forest</em>]!) = <em>Outside</em>!',
        '<strong>Bahar</strong> (Sanskrit <strong>Bahis</strong> Outer/Excluded beyond the door!) = <em>Outside</em>!'
    ),
    130: (
        '<strong>Dentro de (límite/tiempo)</strong> (<strong>Dentro</strong> Inside + <strong>Límite</strong> Limit / <strong>Tiempo</strong> Time!) = <em>Within</em>!',
        '<strong>Ke andar-andar</strong> (<strong>Andar</strong> Inside doubled = Strictly enclosed within bounds!) = <em>Within</em>!'
    ),
    131: (
        '<strong>Más allá de</strong> (<strong>Más</strong> More + <strong>Allá</strong> Yonder there = Further past!) = <em>Beyond</em>!',
        '<strong>Ke paar</strong> (Across the far shore!) / '
        '<strong>Se aage</strong> (<strong>Se</strong> Than + <strong>Aage</strong> Ahead = Further forward than!) = <em>Beyond</em>!'
    ),
    132: (
        '<strong>Hacia</strong> (Latin <em>Faciem ad</em> "Face toward"!) | '
        '<strong>En dirección a</strong> (In direction to!) = <em>Toward</em>!',
        '<strong>Ki taraf</strong> (Arabic <strong>Taraf</strong> Side/Wing — facing the direction of!) = <em>Toward</em>!'
    ),
    133: (
        '<strong>Contra / en contra de</strong> (Latin <em>Contra</em> Facing opposite [<em>Counter / Contrast</em>]!) = <em>Against</em>!',
        '<strong>Ke khilaaf</strong> (Arabic <strong>Khilaf</strong> Behind/Opposite — standing contrary to!) = <em>Against</em>!'
    ),
    136: (
        '<strong>Durante</strong> (From <strong>Durar</strong> Endure/Last [<em>Duration</em>]!) | '
        '<strong>A lo largo de</strong> (Across the length of time!) = <em>During</em>!',
        '<strong>Ke dauran</strong> (Arabic <strong>Dauran</strong> Revolving cycle/period of time!) = <em>During</em>!'
    ),
    137: (
        '1. Time point: <strong>Desde</strong> (<strong>De- + Ex- + De</strong> Starting out from!) = <em>Since (Time)</em>!<br>'
        '2. Because/as: <strong>Ya que</strong> (Already that!) | '
        '<strong>Como</strong> (Given as!) = <em>Since (Reason)</em>!',
        '1. Time point: <strong>Tab se / se</strong> (<strong>Tab</strong> Then + <strong>Se</strong> Starting from!) = <em>Since (Time)</em>!<br>'
        '2. Because/as: <strong>Kyunki</strong> (<strong>Kyun</strong> Why + <strong>Ki</strong> That!) / '
        '<strong>Chunki</strong> (<strong>Chun</strong> Since/As + <strong>Ki</strong> That!) = <em>Since (Reason)</em>!'
    ),
    141: (
        '<strong>Excepto</strong> (<strong>Ex-</strong> Out + <strong>Capere</strong> Take [<em>Except</em>] = Left out!) | '
        '<strong>Menos</strong> (Latin <em>Minus</em> Less!) = <em>Except</em>!',
        '<strong>Ke alawa</strong> (Arabic <strong>\'Alawa</strong> Over & above/Aside from!) / '
        '<strong>Chhor kar</strong> (<strong>Chhorna</strong> Leave out!) = <em>Except</em>!'
    ),
    142: (
        '<strong>En vez de</strong> (<strong>En</strong> In + <strong>Vez</strong> Turn/Place!) | '
        '<strong>En lugar de</strong> (<strong>Lugar</strong> Spot [<em>Local</em>]!) = <em>Instead of</em>!',
        '<strong>Ki jagah</strong> (<strong>Jagah</strong> Spot/Place!) / '
        '<strong>Ke bajaye</strong> (Persian <strong>Ba-</strong> + <strong>Jaay</strong> Place = In place of!) = <em>Instead of</em>!'
    ),
    143: (
        '<strong>Según</strong> (Latin <em>Secundum</em> Following right behind!) | '
        '<strong>De acuerdo con</strong> (In <em>Accord</em>/Agreement with!) = <em>According to</em>!',
        '<strong>Ke hisaab se</strong> (<strong>Hisaab</strong> Calculation [<strong>Tamil ஹிஸாப்</strong>]!) / '
        '<strong>Ke mutabiq</strong> (Arabic <strong>Mutabiq</strong> Matching/Corresponding!) = <em>According to</em>!'
    ),
    146: (
        '<strong>O</strong> (Latin <em>Aut</em> Either/Or — becomes <em>U</em> before words starting with <em>o-/ho-</em>!) = <em>Or</em>!',
        '<strong>Ya / ya fir</strong> (Persian <strong>Ya</strong> Or + <strong>Fir</strong> Else/Again!) = <em>Or</em>!'
    ),
    147: (
        '<strong>Pero</strong> (Latin <em>Per Hoc</em> Nevertheless/Yet!) | '
        '<strong>Sino</strong> (<strong>Si</strong> If + <strong>No</strong> Not = Rather, on the contrary!) = <em>But</em>!',
        '<strong>Lekin</strong> (Arabic <strong>Lakin</strong> But!) / '
        '<strong>Par</strong> (Short contrasting twist!) / '
        '<strong>Magar</strong> (Sanskrit/Persian <strong>Magar</strong> Yet/However!) = <em>But</em>!'
    ),
    152: (
        '<strong>Aunque</strong> (<strong>Aun</strong> Still + <strong>Que</strong> That!) | '
        '<strong>A pesar de que</strong> (At weight/grief of that = In spite of!) = <em>Although / Even though</em>!',
        '<strong>Halanki</strong> (Arabic <strong>Hal</strong> State + <strong>An-ki</strong> Although!) / '
        '<strong>Bhale hi</strong> (Even good!) / '
        '<strong>Chahe</strong> (From <em>Chahna</em> Even if desired!) = <em>Although</em>!'
    ),
    153: (
        '1. Concurrent time: <strong>Mientras</strong> (Latin <em>Dum Interim</em> Meanwhile/During!) = <em>While</em>!<br>'
        '2. Contrast: <strong>Mientras que</strong> (Meanwhile + <strong>Que</strong> That = Whereas!) = <em>Whereas</em>!',
        '1. Concurrent time: <strong>Jab / ...te waqt</strong> (<strong>Jab</strong> When | <strong>-te Waqt</strong> Doing-time!) = <em>While</em>!<br>'
        '2. Contrast: <strong>Jabki</strong> (<strong>Jab</strong> When + <strong>Ki</strong> Whereas!) = <em>Whereas</em>!'
    ),
    154: (
        '<strong>Si</strong> (Latin <em>Si</em> Condition!) | '
        '<strong>Ya sea que</strong> (<strong>Ya</strong> Or + <strong>Sea</strong> Be it that!) = <em>Whether</em>!',
        '<strong>Chahe... ya / ki</strong> (<strong>Chahe</strong> Wish whether + <strong>Ya</strong> Or | <strong>Ki</strong> If/That!) = <em>Whether</em>!'
    ),
    155: (
        '1. Comparison: <strong>Como</strong> (How/Like!) | <strong>Tan</strong> (Latin <em>Tam</em> So/As!) = <em>As (Comparison)</em>!<br>'
        '2. Reason/time: <strong>Como</strong> (Since/As!) | <strong>Mientras</strong> (While!) = <em>As (Reason/Time)</em>!',
        '1. Comparison: <strong>Jaise</strong> (Relative <strong>J-</strong> Like!) / '
        '<strong>Jitna</strong> (Relative <strong>Jit-</strong> As much as!) = <em>As (Comparison)</em>!<br>'
        '2. Reason/time: <strong>Kyunki</strong> (Because!) / '
        '<strong>Jaise hi</strong> (Just the moment that!) = <em>As (Reason/Time)</em>!'
    ),
    157: (
        '<strong>Sin embargo</strong> (<strong>Sin</strong> Without + <strong>Embargo</strong> Barrier/Hold = Nonetheless!) | '
        '<strong>Pero</strong> (Yet/But!) = <em>However</em>!',
        '<strong>Halanki</strong> (Although!) / '
        '<strong>Lekin</strong> (Arabic <strong>Lakin</strong> But/However!) = <em>However</em>!'
    ),
    158: (
        '<strong>Por lo tanto</strong> (<strong>Por</strong> For + <strong>Tanto</strong> So much = For that much reason!) | '
        '<strong>Por eso</strong> (For that!) = <em>Therefore</em>!',
        '<strong>Isliye</strong> (<strong>Is</strong> This + <strong>Liye</strong> Taken for = For this reason!) / '
        '<strong>Is tarah</strong> (Arabic <strong>Tarah</strong> Way/Manner!) = <em>Therefore</em>!'
    ),
    159: (
        '<strong>Además</strong> (<strong>Ad-</strong> To + <strong>De</strong> Of + <strong>Más</strong> More = Over & above!) | '
        '<strong>Aparte de</strong> (Set apart aside from!) = <em>Moreover / Besides</em>!',
        '<strong>Iske alawa</strong> (<strong>Iske</strong> This + Arabic <strong>Alawa</strong> In addition to!) = <em>Moreover / Besides</em>!'
    ),
    161: (
        '<strong>Mientras tanto</strong> (<strong>Mientras</strong> While + <strong>Tanto</strong> So much = In that same meantime!) = <em>Meanwhile</em>!',
        '<strong>Is dauran</strong> (<strong>Is</strong> This + Arabic <strong>Dauran</strong> Cycle!) / '
        '<strong>Is beech</strong> (<strong>Is</strong> This + <strong>Beech</strong> Middle gap!) = <em>Meanwhile</em>!'
    ),
    162: (
        '<strong>En cambio</strong> (<strong>En</strong> In + <strong>Cambio</strong> Exchange [<em>Change</em>]!) | '
        '<strong>En su lugar</strong> (In its place!) = <em>Instead</em>!',
        '<strong>Ke bajaye</strong> (Persian <strong>Ba-Jaay</strong> In place of!) / '
        '<strong>Balki</strong> (Arabic/Persian <strong>Bal-ki</strong> Rather/On the contrary!) = <em>Instead</em>!'
    ),
    163: (
        '<strong>Por ejemplo</strong> (<strong>Por</strong> For + <strong>Ejemplo</strong> Taken-out sample [<em>Example</em>]!) = <em>For example</em>!',
        '<strong>Jaise ki / jaise</strong> (Relative <strong>J-</strong> Manner "Just as"!) = <em>For example</em>!'
    ),
    164: (
        '<strong>De hecho</strong> (<strong>De</strong> Of + <strong>Hecho</strong> Done Fact [Latin <em>Factum</em>]!) | '
        '<strong>En realidad</strong> (In <em>Reality</em>!) = <em>In fact</em>!',
        '<strong>Asal mein</strong> (Arabic <strong>Asl [Tamil அசல் Asal = Original/True!]</strong> + <strong>Mein</strong> In!) / '
        '<strong>Sach toh yeh hai</strong> (<strong>Sach</strong> Truth [Sanskrit <em>Satya</em>]!) = <em>In fact</em>!'
    ),
    166: (
        '<strong>Normalmente</strong> (<strong>Norma</strong> Carpenter square/Rule + <strong>-mente</strong>!) | '
        '<strong>Por lo general</strong> (In <em>General</em>!) = <em>Usually / Normally</em>!',
        '<strong>Aamtaur par</strong> (Arabic <strong>Aam</strong> Common + <strong>Taur</strong> Way + <strong>Par</strong> On!) / '
        '<strong>Aksar</strong> (Arabic <strong>Akthar</strong> Most often!) = <em>Usually / Normally</em>!'
    ),
    167: (
        '<strong>A menudo</strong> (<strong>A</strong> + <strong>Menudo</strong> Minute/Small — happening at tiny intervals = Frequently!) | '
        '<strong>Seguido</strong> (Follow-upon-follow!) = <em>Often</em>!',
        '<strong>Aksar</strong> (Arabic <strong>Akthar</strong> Majority/Frequently [related to <em>Kathrat</em> Abundance]!) = <em>Often</em>!'
    ),
    169: (
        '<strong>De vez en cuando</strong> (From turn/time to when!) | '
        '<strong>Ocasionalmente</strong> (<strong>Ocasi-</strong> Chance fall [<em>Occasion</em>] + <strong>-mente</strong>!) = <em>Occasionally</em>!',
        '<strong>Kabhi-kabhaar</strong> (<strong>Kabhi</strong> Sometime + rhyming echo <strong>-kabhaar</strong> = Now and then!) = <em>Occasionally</em>!'
    ),
    171: (
        '<strong>Nunca</strong> (Latin <em>Numquam</em> Not even once!) | '
        '<strong>Jamás</strong> (Latin <em>Jam Magis</em> Ever more -> Nevermore!) = <em>Never</em>!',
        '<strong>Kabhi nahi</strong> (<strong>Kabhi</strong> Ever/Sometime + <strong>Nahi</strong> Not!) = <em>Never</em>!'
    ),
    174: (
        '1. At that time: <strong>Entonces</strong> (Latin <em>In Tunc</em> At that very moment!) | '
        '<strong>En ese momento</strong> (At that moment!) = <em>Then</em>!<br>'
        '2. Next/after that: <strong>Luego</strong> (Latin <em>Loco</em> On the spot/Immediately after!) | '
        '<strong>Después</strong> (<strong>De- + Ex- + Post</strong> After!) = <em>Then (Next)</em>!',
        '1. At that time: <strong>Tab</strong> (Correlative <strong>T-</strong> That time!) / '
        '<strong>Us waqt</strong> (<strong>Us</strong> That + Arabic <strong>Waqt</strong> Time!) = <em>Then</em>!<br>'
        '2. Next/after that: <strong>Fir</strong> (Turning round again!) / '
        '<strong>Uske baad</strong> (<strong>Uske</strong> That + Arabic <strong>Ba\'d</strong> After!) = <em>Then (Next)</em>!'
    ),
    175: (
        '<strong>Hoy</strong> (Latin <em>Hodie</em> = <em>Hoc Die</em> "On this day" — shortened to crisp <em>Hoy</em>!) = <em>Today</em>!',
        '<strong>Aaj</strong> (Sanskrit <strong>Adya</strong> This very day!) = <em>Today</em>!'
    ),
    177: (
        '<strong>Ayer</strong> (Latin <em>Heri</em> Previous day [related to <em>Yesterday</em>]!) = <em>Yesterday</em>!',
        '<strong>Kal (beeta hua kal)</strong> (Sanskrit <strong>Kalya</strong> Next/Previous day + <strong>Beeta hua</strong> Passed away!) = <em>Yesterday</em>!'
    ),
    179: (
        '<strong>Pronto</strong> (Latin <em>Promptus</em> Brought forth/Ready [<em>Prompt</em>]!) | '
        '<strong>Dentro de poco</strong> (Within a little time!) = <em>Soon</em>!',
        '<strong>Jaldi / jald hi</strong> (Arabic <strong>Jald</strong> Swift/Brisk + <strong>-hi</strong> Right away!) = <em>Soon</em>!'
    ),
    181: (
        '1. Continuing state: <strong>Todavía</strong> (<strong>Toda</strong> All + <strong>Vía</strong> Way = All the way up to now!) | '
        '<strong>Aún</strong> (Latin <em>Adhuc</em> Yet/Still!) = <em>Still</em>!<br>'
        '2. Motionless: <strong>Quieto</strong> (Latin <em>Quietus</em> [<em>Quiet</em>]!) | '
        '<strong>Inmóvil</strong> (<strong>In-</strong> Not + <strong>Móvil</strong> Moving!) = <em>Still (Motionless)</em>!',
        '1. Continuing state: <strong>Abhi bhi</strong> (<strong>Abhi</strong> Right now + <strong>Bhi</strong> Even!) = <em>Still</em>!<br>'
        '2. Motionless: <strong>Shaant</strong> (Sanskrit <strong>Shanta [Tamil சாந்தம் = Calm!]</strong>) / '
        '<strong>Bina hile</strong> (<strong>Bina</strong> Without + <strong>Hilna</strong> Moving!) = <em>Still (Motionless)</em>!'
    ),
    182: (
        '<strong>Temprano</strong> (Latin <em>Temporanus</em> Timely/Seasonable [<em>Temporal</em>] -> Ahead of time!) = <em>Early</em>!',
        '<strong>Jaldi</strong> (Swiftly/Promptly!) / '
        '<strong>Waqt se pehle</strong> (<strong>Waqt</strong> Time + <strong>Se pehle</strong> Before!) = <em>Early</em>!'
    ),
    183: (
        '<strong>Tarde</strong> (Latin <em>Tardus</em> Slow/Lingering [root of <em>Tardy / Retard</em>]!) = <em>Late</em>!',
        '<strong>Der se</strong> (Persian <strong>Der</strong> Slow/Delayed + <strong>Se</strong> With!) = <em>Late</em>!'
    ),
    184: (
        '<strong>De repente</strong> (Latin <em>Repens</em> Creeping up all at once!) | '
        '<strong>De golpe</strong> (With one sudden blow/hit!) = <em>Suddenly</em>!',
        '<strong>Achanak</strong> (Unexpected flash without warning!) / '
        '<strong>Ekdum se</strong> (<strong>Ek</strong> One + <strong>Dum</strong> Breath = In a single breath!) = <em>Suddenly</em>!'
    ),
    185: (
        '<strong>Recientemente</strong> (<strong>Reciente</strong> Fresh/New [<em>Recent</em>]!) | '
        '<strong>Últimamente</strong> (<strong>Último</strong> Latest!) | '
        '<strong>Hace poco</strong> (Makes little time ago!) = <em>Recently</em>!',
        '<strong>Haal hi mein</strong> (Arabic <strong>Hal</strong> Present state + <strong>Hi mein</strong> Just in!) / '
        '<strong>Pichhle kuch dino mein</strong> (<strong>Pichhle</strong> Past + <strong>Kuch dino</strong> Few days!) = <em>Recently</em>!'
    ),
    186: (
        '<strong>Inmediatamente</strong> (<strong>In-</strong> No + <strong>Medio</strong> Middle gap [<em>Immediate</em>]!) | '
        '<strong>Enseguida</strong> (<strong>En</strong> In + <strong>Seguir</strong> Follow right behind!) = <em>Immediately</em>!',
        '<strong>Turant</strong> (Sanskrit <strong>Tvarant</strong> Hastening fast!) / '
        '<strong>Fauran</strong> (Arabic <strong>Fawr</strong> Instant boiling-over speed!) = <em>Immediately</em>!'
    ),
    187: (
        '<strong>Finalmente</strong> (<strong>Fin</strong> End [<em>Final</em>] + <strong>-mente</strong>!) | '
        '<strong>Por fin</strong> (By end!) = <em>Finally</em>!',
        '<strong>Aakhirkaar</strong> (Arabic <strong>Akhir</strong> Last + Persian <strong>-kaar</strong> Work/End!) / '
        '<strong>Aakhir mein</strong> (In the final end!) = <em>Finally</em>!'
    ),
    188: (
        '<strong>Con el tiempo</strong> (With the passing of time!) | '
        '<strong>Al final</strong> (At the ultimate end!) = <em>Eventually</em>!',
        '<strong>Aakhirkaar</strong> (In the final end!) / '
        '<strong>Aage chalkar</strong> (<strong>Aage</strong> Forward + <strong>Chalkar</strong> Walking ahead in time!) = <em>Eventually</em>!'
    ),
    189: (
        '<strong>Otra vez</strong> (<strong>Otra</strong> Another + <strong>Vez</strong> Turn!) | '
        '<strong>De nuevo</strong> (Of new/afresh [<em>Anew</em>]!) = <em>Again</em>!',
        '<strong>Fir se</strong> (Turning back once more!) / '
        '<strong>Dobara</strong> (<strong>Do-</strong> Two + <strong>-baara</strong> Time = A second time!) = <em>Again</em>!'
    ),
    190: (
        '<strong>A diario</strong> (From <strong>Día</strong> Day = Day by day!) | '
        '<strong>Todos los días</strong> (Every single day!) = <em>Daily</em>!',
        '<strong>Roz / rozana</strong> (Persian <strong>Roz</strong> Day/Sun + <strong>-ana</strong> Every day!) = <em>Daily</em>!'
    ),
    193: (
        '<strong>Anualmente</strong> (From <strong>Año</strong> Year [<em>Annual</em>]!) | '
        '<strong>Cada año</strong> (Each year!) = <em>Yearly</em>!',
        '<strong>Har saal</strong> (Persian <strong>Har</strong> Every + Persian <strong>Saal</strong> Year!) = <em>Yearly</em>!'
    ),
    194: (
        '<strong>Aquí</strong> (Latin <em>Eccum Hic</em> Behold right here!) | '
        '<strong>Acá</strong> (Hither/Near side!) = <em>Here</em>!',
        '<strong>Yahan</strong> (Near-locative <strong>Y-</strong> Here!) / '
        '<strong>Idhar</strong> (Directional <strong>I-</strong> This side/Hither!) = <em>Here</em>!'
    ),
    195: (
        '<strong>Ahí</strong> (Near you there!) | '
        '<strong>Allí</strong> (Further over there!) | '
        '<strong>Allá</strong> (Yonder far away!) = <em>There</em>!',
        '<strong>Wahan</strong> (Far-locative <strong>W-</strong> There!) / '
        '<strong>Udhar</strong> (Directional <strong>U-</strong> That side/Thither!) = <em>There</em>!'
    ),
    196: (
        '<strong>Adelante</strong> (<strong>Ad- + De + In + Ante</strong> Before/Front!) | '
        '<strong>Hacia adelante</strong> (Facing toward the front!) = <em>Ahead / Forward</em>!',
        '<strong>Aage / aage ki taraf</strong> (Sanskrit <strong>Agra</strong> Foremost tip + <strong>Taraf</strong> Side/Direction!) = <em>Ahead / Forward</em>!'
    ),
    197: (
        '<strong>Hacia atrás</strong> (<strong>Hacia</strong> Toward + <strong>Atrás</strong> Behind [from <em>Ad-Trans</em>]!) = <em>Backward</em>!',
        '<strong>Peeche ki taraf</strong> (<strong>Peeche</strong> Behind [Sanskrit <em>Pashchat</em>] + <strong>Taraf</strong> Direction!) / '
        '<strong>Ulta</strong> (Reversed/Upside-down!) = <em>Backward</em>!'
    ),
    198: (
        '<strong>Arriba</strong> (<strong>Ad + Ripa</strong> Up onto the upper bank/floor!) = <em>Upstairs / Up</em>!',
        '<strong>Upar</strong> (Sanskrit <strong>Upari [Upper]</strong> = Upper floor/Above!) = <em>Upstairs / Up</em>!'
    ),
    199: (
        '<strong>Abajo</strong> (<strong>A + Bajo</strong> Down on the lower floor [<em>Base</em>]!) = <em>Downstairs / Down</em>!',
        '<strong>Neeche</strong> (Sanskrit <strong>Nicha</strong> Lower level/Down below!) = <em>Downstairs / Down</em>!'
    ),
    200: (
        '<strong>Más</strong> (Latin <em>Magis</em> Greater/Additional [root of <em>Major / Maximum</em>]!) = <em>More</em>!',
        '<strong>Aur</strong> (Sanskrit <strong>Apara</strong> Other/Further!) / '
        '<strong>Zyaada</strong> (Arabic <strong>Ziyadah</strong> Increased/Excess!) = <em>More</em>!'
    ),
    202: (
        '<strong>Menos</strong> (Latin <em>Minus</em> Smaller/Fewer [twin of <em>Minus</em>]!) = <em>Less</em>!',
        '<strong>Kam</strong> (Persian <strong>Kam</strong> Deficient/Scant/Lacking [<strong>Tamil கம்மி Kammi = Less!</strong>]!) = <em>Less</em>!'
    ),
    204: (
        '<strong>Solo / solamente</strong> (Latin <em>Solus</em> Alone [<em>Solo / Solitary</em>]!) | '
        '<strong>Único</strong> (<strong>Uno</strong> One [<em>Unique</em>]!) = <em>Only</em>!',
        '<strong>Sirf</strong> (Arabic <strong>Sirf</strong> Pure/Unmixed — merely!) / '
        '<strong>Akela</strong> (<strong>Ek</strong> One + <strong>-ela</strong> Single alone!) = <em>Only</em>!'
    ),
    205: (
        '<strong>Casi</strong> (Latin <em>Quasi</em> As if/Nearly [<em>Quasi-</em>]!) | '
        '<strong>Por poco</strong> (By a tiny margin!) = <em>Almost / Nearly</em>!',
        '<strong>Lagbhag</strong> (<strong>Lag-</strong> Touching + <strong>Bhag</strong> Part = Nearly!) / '
        '<strong>Kareeb-kareeb</strong> (Arabic <strong>Qarib</strong> Near doubled = Close to!) = <em>Almost / Nearly</em>!'
    ),
    206: (
        '<strong>Bastante</strong> (From <strong>Bastar</strong> Satisfy fully!) | '
        '<strong>Totalmente</strong> (<strong>Total</strong> Whole!) = <em>Quite</em>!',
        '<strong>Kaafi</strong> (Arabic <strong>Kafi</strong> Ample/Considerable!) / '
        '<strong>Bilkul</strong> (Arabic <strong>Bi-l-Kull</strong> With the whole = Totally!) = <em>Quite</em>!'
    ),
    207: (
        '1. Somewhat: <strong>Bastante</strong> (Fairly enough!) | '
        '<strong>Un poco</strong> (A small bit!) = <em>Rather (Somewhat)</em>!<br>'
        '2. Preference/instead: <strong>Más bien</strong> (<strong>Más</strong> More + <strong>Bien</strong> Well = Better said!) = <em>Rather (Instead)</em>!',
        '1. Somewhat: <strong>Thoda sa</strong> (Small bit!) / '
        '<strong>Kaafi hadd tak</strong> (<strong>Kaafi</strong> Ample + <strong>Hadd</strong> Limit!) = <em>Rather (Somewhat)</em>!<br>'
        '2. Preference/instead: <strong>Balki</strong> (Arabic/Persian <strong>Bal-ki</strong> Nay rather!) / '
        '<strong>Bajaye</strong> (Persian <strong>Ba-Jaay</strong> Instead!) = <em>Rather (Instead)</em>!'
    ),
    210: (
        '<strong>Extremadamente</strong> (<strong>Ex- + Tremus</strong> Outermost edge [<em>Extreme</em>]!) | '
        '<strong>Súper</strong> (Latin <em>Super</em> Above all!) = <em>Extremely</em>!',
        '<strong>Behad</strong> (Persian <strong>Be-</strong> Without + Arabic <strong>Hadd</strong> Limit = Limitless!) / '
        '<strong>Bohot hi zyaada</strong> (Extremely excessive!) = <em>Extremely</em>!'
    ),
    211: (
        '1. Truly: <strong>De verdad</strong> (Of truth [<em>Verity</em>]!) | '
        '<strong>En serio</strong> (In <em>Serious</em>ness!) = <em>Really (Truly)</em>!<br>'
        '2. Very: <strong>Muy</strong> (Shortened <em>Mucho</em> = Very!) | '
        '<strong>Súper</strong> (Super-high!) = <em>Really (Very)</em>!',
        '1. Truly: <strong>Sach mein</strong> (Sanskrit <strong>Satya</strong> Truth!) / '
        '<strong>Waqai</strong> (Arabic <strong>Waqi\'i</strong> Actually occurring in reality!) = <em>Really (Truly)</em>!<br>'
        '2. Very: <strong>Bohot</strong> (Sanskrit <strong>Bahu</strong> Abundantly!) = <em>Really (Very)</em>!'
    ),
    212: (
        '<strong>Especialmente</strong> (From <em>Especie</em> Distinct kind [<em>Special</em>]!) | '
        '<strong>En particular</strong> (In <em>Particular</em>!) = <em>Especially</em>!',
        '<strong>Khaaskar</strong> (Arabic <strong>Khass</strong> Special/Private + <strong>-kar</strong> Doing = Notably!) = <em>Especially</em>!'
    ),
    213: (
        '1. Only: <strong>Solo</strong> (Alone!) | <strong>Nada más</strong> (Nothing more!) = <em>Just (Only)</em>!<br>'
        '2. Recently happened: <strong>Acabar de</strong> (To have just finished ending!) = <em>Just (Did)</em>!<br>'
        '3. Fair: <strong>Justo</strong> (Latin <em>Justus</em> Righteous/Exact [<em>Just / Justice</em>]!) = <em>Just (Fair)</em>!',
        '1. Only: <strong>Sirf</strong> (Purely!) / <strong>Bas</strong> (Enough/Only!) = <em>Just (Only)</em>!<br>'
        '2. Recently happened: <strong>Abhi-abhi</strong> (Doubled <strong>Abhi</strong> Right now = Moments ago!) = <em>Just (Did)</em>!<br>'
        '3. Fair: <strong>Sahi</strong> (Arabic <strong>Sahih</strong> True/Sound!) / '
        '<strong>Jayaz</strong> (Arabic <strong>Ja\'iz</strong> Lawful/Permitted!) = <em>Just (Fair)</em>!'
    ),
    214: (
        '<strong>Incluso</strong> (<strong>In-</strong> In + <strong>Claudere</strong> Shut/Include [<em>Inclusive</em>]!) | '
        '<strong>Hasta</strong> (Arabic <em>Hatta</em> Reaching all the way up to!) = <em>Even</em>!',
        '<strong>Bhi</strong> (Sanskrit <strong>Api</strong> Inclusive particle!) / '
        '<strong>Yahan tak ki</strong> (<strong>Yahan</strong> Here + <strong>Tak</strong> Up to + <strong>Ki</strong> That!) = <em>Even</em>!'
    ),
    215: (
        '<strong>También</strong> (<strong>Tan</strong> So + <strong>Bien</strong> Well = Equally well!) | '
        '<strong>Además</strong> (In addition!) = <em>Also / As well</em>!',
        '<strong>Bhi</strong> (Inclusive <em>Also</em>!) / '
        '<strong>Saath hi</strong> (<strong>Saath</strong> Company + <strong>Hi</strong> Together with!) = <em>Also / As well</em>!'
    ),
    217: (
        '1. Negative answer/determiner: <strong>No / ningún</strong> (Latin <em>Non</em> No | <em>Nec-Unus</em> Not even one!) = <em>No</em>!<br>'
        '2. Adverbial negation: <strong>No</strong> (Latin <em>Non</em> Verbal negation before verb!) = <em>Not</em>!',
        '1. Negative answer/determiner: <strong>Nahi / na / koi nahi</strong> (Sanskrit <strong>Na</strong> Not + <strong>Koi</strong> Any!) = <em>No</em>!<br>'
        '2. Adverbial negation: <strong>Nahi / mat</strong> (<strong>Nahi</strong> Not | Sanskrit <strong>Ma</strong> Prohibitive "Don’t!" <em>Mat</em>!) = <em>Not</em>!'
    ),
    218: (
        '<strong>Tal vez</strong> (Such a turn/time!) | '
        '<strong>Quizás</strong> (Old Spanish <em>Qui Sabe</em> "Who knows?" compressed into <em>Quizás</em>!) = <em>Maybe / Perhaps</em>!',
        '<strong>Shayad</strong> (Persian <strong>Shayad</strong> "It may be" — classic possibility word!) = <em>Maybe / Perhaps</em>!'
    ),
    219: (
        '<strong>Probablemente</strong> (<strong>Probar</strong> Prove/Test + <strong>-able</strong> Likely [<em>Probable</em>]!) | '
        '<strong>Seguro</strong> (<strong>Se-</strong> Without + <strong>Cura</strong> Care = Sure!) = <em>Probably</em>!',
        '<strong>Lagbhag pakka</strong> (<strong>Lagbhag</strong> Nearly + <strong>Pakka [Tamil பக்கா Solid!]</strong>!) / '
        '<strong>Mumkin hai</strong> (Arabic <strong>Mumkin</strong> Possible + <strong>Hai</strong> Is!) = <em>Probably</em>!'
    ),
    220: (
        '<strong>Definitivamente</strong> (<strong>De-</strong> + <strong>Finis</strong> Bound [<em>Define</em>]!) | '
        '<strong>Ciertamente</strong> (<strong>Cierto</strong> Certain!) | '
        '<strong>Sin duda</strong> (Without <em>Doubt</em>!) = <em>Definitely</em>!',
        '<strong>Pakka</strong> (Sanskrit <strong>Pakva [Tamil பக்குவம் / பக்கா Cooked solid!]</strong>!) / '
        '<strong>Bilkul</strong> (Arabic <strong>Bi-l-Kull</strong> Wholly/Completely!) = <em>Definitely</em>!'
    ),
    221: (
        '<strong>En realidad</strong> (In <em>Real</em> truth!) | '
        '<strong>De hecho</strong> (Of <em>Factum</em> / Done deed!) = <em>Actually</em>!',
        '<strong>Asal mein</strong> (Arabic <strong>Asl [Tamil அசல் Original!]</strong> + <strong>Mein</strong> In!) / '
        '<strong>Sach mein</strong> (In truth!) = <em>Actually</em>!'
    ),
    222: (
        '<strong>Verdaderamente</strong> (Latin <em>Verus</em> True [<em>Verity</em>]!) | '
        '<strong>De verdad</strong> (In truth!) = <em>Truly</em>!',
        '<strong>Sach mein</strong> (Sanskrit <strong>Satya</strong> Truth + <strong>Mein</strong> In!) / '
        '<strong>Dil se</strong> (Persian <strong>Dil</strong> Heart + <strong>Se</strong> From!) = <em>Truly</em>!'
    ),
    223: (
        '<strong>Cero</strong> (Arabic <strong>Sifr</strong> Empty cipher -> Latin <em>Zephirum</em> -> Italian <em>Zero</em>!) = <em>Zero</em>!',
        '<strong>Shunya</strong> (Sanskrit <strong>Shunya [Tamil சூன்யம் Soonyam = Void/Zero!]</strong> -> origin of math Zero!) = <em>Zero</em>!'
    ),
    229: (
        '<strong>Seis</strong> (Latin <em>Sex</em> — shared Indo-European numeral *<em>sweks</em> with English <em>Six</em>!) = <em>Six</em>!',
        '<strong>Chhe</strong> (Sanskrit <strong>Shat</strong> Six — Indo-European cousin of <em>Six</em> & <em>Seis</em>!) = <em>Six</em>!'
    ),
    234: (
        '<strong>Cien / ciento</strong> (Latin <em>Centum</em> Hundred [root of <em>Century / Cent / Percent</em>]!) = <em>Hundred</em>!',
        '<strong>Sau</strong> (Sanskrit <strong>Shata</strong> Hundred — Indo-European cousin of Latin <em>Centum</em>!) = <em>Hundred</em>!'
    ),
    236: (
        '<strong>Millón</strong> (<strong>Mil</strong> Thousand + <strong>-ón</strong> Big = Great thousand = Million!) | '
        '<strong>Mil millones (billón)</strong> (1,000 × 1,000,000 in Spanish scale!) = <em>Million / Billion</em>!',
        '<strong>Das laakh / ek arab</strong> (<strong>Das</strong> 10 × <strong>Laakh</strong> 100,000 = Million | <strong>Ek Arab</strong> 100 Crore = Billion!) = <em>Million / Billion</em>!'
    ),
    237: (
        '<strong>Primero / primera</strong> (Latin <em>Primarius</em> First in rank [root of <em>Primary / Prime</em>]!) = <em>First</em>!',
        '<strong>Pehla / pehli</strong> (Sanskrit <strong>Prathama</strong> Foremost/First — inflects <em>-a / -i</em>!) = <em>First</em>!'
    ),
    238: (
        '1. Rank/order: <strong>Segundo / segunda</strong> (Latin <em>Secundus</em> Following behind [<em>Second</em>]!) = <em>Second (Order)</em>!<br>'
        '2. Unit of time: <strong>Segundo</strong> (Second division of the hour!) = <em>Second (Time)</em>!',
        '1. Rank/order: <strong>Doosra / doosri</strong> (<strong>Do</strong> Two + <strong>-sra</strong> Ordinal = 2nd!) = <em>Second (Order)</em>!<br>'
        '2. Unit of time: <strong>Pal</strong> (Sanskrit <strong>Pala</strong> Instant eyeblink moment!) = <em>Second (Time)</em>!'
    ),
    239: (
        '<strong>Tercero / tercera</strong> (Latin <em>Tertius</em> Three [root of <em>Tertiary</em>]!) = <em>Third</em>!',
        '<strong>Teesra / teesri</strong> (<strong>Teen</strong> Three + <strong>-sra / -sri</strong> Ordinal = 3rd!) = <em>Third</em>!'
    ),
    240: (
        '<strong>Mitad</strong> (Latin <em>Medietas</em> Middle division!) | '
        '<strong>Medio / media</strong> (Latin <em>Medius</em> Middle [<em>Medium</em>]!) = <em>Half</em>!',
        '<strong>Aadha / aadhi / aadhe</strong> (Sanskrit <strong>Ardha [Tamil அர்த்தம் / அரை Half!]</strong> — inflects <em>-a / -i / -e</em>!) = <em>Half</em>!'
    ),
    241: (
        '1. One fourth: <strong>Cuarto</strong> (Latin <em>Quartus</em> 4th [<em>Quarter</em>]!) | '
        '<strong>La cuarta parte</strong> (The 4th part!) = <em>Quarter</em>!<br>'
        '2. 15 minutes: <strong>Cuarto de hora</strong> (<strong>Cuarto</strong> 1/4 + <strong>Hora</strong> Hour = 15 min!) = <em>Quarter Hour</em>!',
        '1. One fourth: <strong>Chauthai</strong> (Sanskrit <strong>Chaturtha</strong> Fourth [from <em>Chaar</em> Four]!) = <em>Quarter</em>!<br>'
        '2. 15 minutes: <strong>Pandrah minute</strong> (<strong>Pandrah</strong> 15 + <strong>Minute</strong> Small division!) = <em>15 Minutes</em>!'
    ),
    242: (
        '<strong>Doble</strong> (Latin <em>Duplus</em> = <em>Duo</em> Two + <em>Plus</em> Fold [<em>Double / Duplex</em>]!) = <em>Double</em>!',
        '<strong>Doguna</strong> (<strong>Do</strong> Two + <strong>Guna</strong> Times/Fold [Sanskrit <em>Guna = Strand/Fold</em>]!) = <em>Double</em>!'
    ),
    243: (
        '<strong>Total</strong> (Latin <em>Totus</em> Entire/All combined!) = <em>Total</em>!',
        '<strong>Kul</strong> (Arabic <strong>Kull</strong> Whole/All summed together — also used in <em>Bilkul</em>!) = <em>Total</em>!'
    ),
    244: (
        '1. Clock/hours: <strong>Tiempo</strong> (Latin <em>Tempus</em> Time [<em>Temporal</em>]!) | '
        '<strong>Hora</strong> (Latin <em>Hora</em> Hour!) = <em>Time</em>!<br>'
        '2. Instance/occasion: <strong>Vez</strong> (Latin <em>Vicis</em> Turn/Occasion [<em>Vice versa</em>]!) = <em>Time (Occasion)</em>!',
        '1. Clock/hours: <strong>Samay</strong> (Sanskrit <strong>Samaya [Tamil சமயம் Samayam = Time!]</strong>!) / '
        '<strong>Waqt</strong> (Arabic <strong>Waqt</strong> Fixed hour!) = <em>Time</em>!<br>'
        '2. Instance/occasion: <strong>Baar</strong> (Sanskrit <strong>Vara</strong> Turn/Occasion!) / '
        '<strong>Dafa</strong> (Arabic <strong>Daf\'ah</strong> Push/Single stroke!) = <em>Time (Occasion)</em>!'
    ),
    245: (
        '<strong>Momento</strong> (Latin <em>Momentum</em> Moving scale-tipping instant!) | '
        '<strong>Instante</strong> (<strong>In- + Stare</strong> Standing right now!) = <em>Moment</em>!',
        '<strong>Pal</strong> (Eyeblink unit!) / '
        '<strong>Lamha</strong> (Arabic <strong>Lamhah</strong> Quick glance/Flash!) = <em>Moment</em>!'
    ),
    246: (
        '<strong>Minuto</strong> (Latin <em>Minuta</em> Made tiny [<em>Minute / Diminish</em>] = 1/60th tiny slice of hour!) = <em>Minute</em>!',
        '<strong>Minute</strong> (Latin <em>Minuta</em> Small division of an hour!) = <em>Minute</em>!'
    ),
    247: (
        '<strong>Hora</strong> (Greek/Latin <em>Hora</em> Fixed season/60-min hour [origin of <em>Hour</em>]!) = <em>Hour</em>!',
        '<strong>Ghanta</strong> (Sanskrit <strong>Ghanta [Tamil மணி Mani = Bell/Hour!]</strong> — temple bell rung on the hour!) = <em>Hour</em>!'
    ),
    251: (
        '<strong>Tarde</strong> (Latin <em>Tardus</em> Later part of the sun’s arc [<em>Tardy</em>]!) = <em>Afternoon</em>!',
        '<strong>Dopahar</strong> (<strong>Do</strong> Two + <strong>Pahar</strong> Watch/3-hour shift = Midday 2nd watch!) = <em>Afternoon</em>!'
    ),
    252: (
        '<strong>Tarde</strong> (Late afternoon!) | '
        '<strong>Noche (temprano)</strong> (Latin <em>Nox</em> Nightfall early edge [<em>Nocturnal</em>]!) = <em>Evening</em>!',
        '<strong>Shaam</strong> (Persian <strong>Sham</strong> Dusk/Sunset twilight!) = <em>Evening</em>!'
    ),
    257: (
        '1. 10 years: <strong>Década</strong> (Greek <em>Deka</em> Ten [<em>Decade</em>]!) = <em>Decade</em>!<br>'
        '2. 100 years: <strong>Siglo</strong> (Latin <em>Saeculum</em> Lifetime/100-year age [<em>Secular</em>]!) = <em>Century</em>!',
        '1. 10 years: <strong>Das saal</strong> (<strong>Das</strong> Ten [<em>Deka</em>] + <strong>Saal</strong> Years!) = <em>Decade</em>!<br>'
        '2. 100 years: <strong>Sadi / sau saal</strong> (Arabic <strong>Sadi</strong> Century [from Persian <em>Sad</em> Hundred] / <strong>Sau saal</strong> 100 Years!) = <em>Century</em>!'
    ),
    258: (
        '<strong>Estación (del año)</strong> (Latin <em>Statio</em> Standing phase of the year [<em>Station</em>]!) | '
        '<strong>Temporada</strong> (<strong>Tiempo</strong> Time span!) = <em>Season</em>!',
        '<strong>Mausam</strong> (Arabic <strong>Mawsim [Tamil மௌசம் = Fixed Time/Monsoon Season!]</strong>!) = <em>Season</em>!'
    ),
    259: (
        '1. Season: <strong>Primavera</strong> (<strong>Prima</strong> First + <strong>Vera</strong> True spring bloom!) = <em>Spring (Season)</em>!<br>'
        '2. Coil: <strong>Resorte</strong> (<strong>Re-</strong> Back + <strong>Sortir</strong> Leap [<em>Resort</em>]!) | '
        '<strong>Muelle</strong> (Soft elastic coil!) = <em>Spring (Coil)</em>!',
        '1. Season: <strong>Basant</strong> (Sanskrit <strong>Vasanta [Tamil வசந்தம் Vasantham = Springtime!]</strong>!) = <em>Spring (Season)</em>!<br>'
        '2. Coil: <strong>Spring</strong> (Old English <em>Springan</em> Leap/Bounce back up!) = <em>Spring (Coil)</em>!'
    ),
    261: (
        '<strong>Otoño</strong> (Latin <em>Autumnus</em> Ripening harvest season -> <em>Autumn</em>!) = <em>Autumn</em>!',
        '<strong>Patjhad</strong> (<strong>Patta</strong> Leaf + <strong>Jhadna</strong> Shed/Fall off = Leaf-shedding season!) = <em>Autumn</em>!'
    ),
    264: (
        '<strong>Calendario</strong> (Latin <em>Kalendarium</em> Account book settled on the <em>Kalends</em> [1st of each month]!) = <em>Calendar</em>!',
        '<strong>Calendar</strong> (Latin <em>Kalendarium</em> Monthly debt & date ledger!) = <em>Calendar</em>!'
    ),
}
