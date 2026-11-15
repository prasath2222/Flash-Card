import json
import os

INDEX_PATH = "index.html"
BACKUP_PATH = "data/backup_original_cards.json"

# Clean Wikimedia Commons photo upgrades for mismatched / weak Split 7 images
IMAGE_UPGRADES = {
    1270: "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Bogalusa_Mayor_Tyrin_Truong_Press_Conference_01.jpg/960px-Bogalusa_Mayor_Tyrin_Truong_Press_Conference_01.jpg",
    1284: "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/School_report_card.jpg/960px-School_report_card.jpg",
    1288: "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Student_Graduation_at_Powidz_%289617252%29.jpg/960px-Student_Graduation_at_Powidz_%289617252%29.jpg",
    1296: "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Old_books_-_old_textures.jpg/960px-Old_books_-_old_textures.jpg",
    1311: "https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/Weighing_scales_and_weights_-_Goritsky_monastery%2C_Pereslavl_museum.jpg/960px-Weighing_scales_and_weights_-_Goritsky_monastery%2C_Pereslavl_museum.jpg",
    1348: "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Chorus_sheet_music_%28Unsplash%29.jpg/960px-Chorus_sheet_music_%28Unsplash%29.jpg",
    1355: "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Adidas_soccer_ball_on_a_grass_pitch_%28Unsplash%29.jpg/960px-Adidas_soccer_ball_on_a_grass_pitch_%28Unsplash%29.jpg",
    1360: "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Simone_Biles_at_the_2016_Olympics_all-around_gold_medal_podium_%2828262782114%29.jpg/960px-Simone_Biles_at_the_2016_Olympics_all-around_gold_medal_podium_%2828262782114%29.jpg",
}

SPLIT7_UPDATES = {
    1263: {
        "es": "Noticias / prensa / medios",
        "hi": "Khabrein / news / media",
        "tamil": "செய்திகள் / பத்திரிகை / ஊடகம்",
        "shortcutEs": '<strong>Noticias</strong> ≈ Direct sibling of <strong>"Notices"</strong> (breaking announcements) → TV/paper <em>News</em>! | <strong>Prensa</strong> ≈ Direct sibling of <strong>"Press"</strong> (printing press)! | <strong>Medios</strong> ≈ Direct sibling of <strong>"Media"</strong>!',
        "shortcutHi": '<strong>Khabrein</strong> ≈ <strong>Spoken Tamil கபர் (Khabar = News/Word!)</strong> → Plural <em>Khabrein</em> = Daily <em>News</em>! | <strong>News / media</strong> ≈ Breaking TV alerts (<em>News</em>) & social channels (<em>Media</em>) spoken directly across India!',
    },
    1264: {
        "es": "Emitir / transmitir",
        "hi": "Live dikhana / broadcast",
        "tamil": "ஒளிபரப்பு",
        "shortcutEs": '<strong>Emitir</strong> ≈ Direct sibling of <strong>"Emit"</strong> (send out signals/radio waves)! | <strong>Transmitir</strong> ≈ Direct sibling of <strong>"Transmit"</strong> → Live TV/radio <em>Broadcast</em>!',
        "shortcutHi": '<strong>Live dikhana</strong> ≈ <strong>Live</strong> + <strong>Dikhana ("De-khaana" = To show visually)</strong> → Showing an event live on screen! | <strong>Broadcast</strong> ≈ Public TV/radio airing signal!',
    },
    1265: {
        "es": "1. Banner title: Titular / encabezado | 2. Written story: Artículo",
        "hi": "1. Banner title: Headline / mukhya khabar | 2. Written story: Article / lekh",
        "tamil": "1. தலைப்புச் செய்தி (Banner title) / 2. கட்டுரை (Written story)",
        "shortcutEs": '1. Banner title: <strong>Titular</strong> ≈ Direct sibling of <strong>"Title"</strong> → Big front-page <em>Headline</em>! | <strong>Encabezado</strong> ≈ <strong>En- + Cabeza (Head!)</strong> → Top-of-the-page header!<br>2. Written story: <strong>Artículo</strong> ≈ Direct match with English <strong>"Article"</strong> (full newspaper write-up)!',
        "shortcutHi": '1. Banner title: <strong>Headline</strong> ≈ Bold top newspaper banner line! | <strong>Mukhya khabar</strong> ≈ <strong>Mukhya (Tamil முக்கிய = Main!)</strong> + <strong>Khabar (News)</strong> → Top story = <em>Headline</em>!<br>2. Written story: <strong>Article</strong> ≈ Full editorial report! | <strong>Lekh</strong> ≈ <strong>Tamil இலக்கியம் / எழுத்து (Write)</strong> → Written column = <em>Article (Lekh)</em>!',
    },
    1266: {
        "es": "1. Informant reference: Fuente | 2. Unauthorized secret reveal: Filtración / filtrar",
        "hi": "1. Informant reference: Source / zariya | 2. Unauthorized secret reveal: Khabar leak hona / parda khulna",
        "tamil": "1. ஆதார மூலம் (Informant reference) / 2. ரகசியக் கசிவு (Unauthorized secret reveal)",
        "shortcutEs": '1. Informant reference: <strong>Fuente</strong> ≈ Same root as <strong>"Fountain / Font"</strong> → Where news originates = <em>Source</em>!<br>2. Unauthorized secret reveal: <strong>Filtración / filtrar</strong> ≈ Direct sibling of <strong>"Filter / Filtrate"</strong> → Secret info dripping past a filter = <em>Leak</em>!',
        "shortcutHi": '1. Informant reference: <strong>Source</strong> ≈ Origin point of a story! | <strong>Zariya</strong> ≈ Means "Channel / Medium" (<em>Kis zariye se?</em> = Through which insider <em>Source</em>?)!<br>2. Unauthorized secret reveal: <strong>Khabar leak hona</strong> ≈ Secret news (<em>Khabar</em>) slipping out! | <strong>Parda khulna</strong> ≈ <strong>Parda (Curtain)</strong> + <strong>Khulna (Open)</strong> → Lifting the curtain on a secret = <em>Leak</em>!',
    },
    1267: {
        "es": "1. Daily news sheet: Periódico / diario | 2. Periodical: Revista",
        "hi": "1. Daily news sheet: Akhbar | 2. Periodical: Magazine",
        "tamil": "1. செய்தித்தாள் (Daily news sheet) / 2. வார/மாத இதழ் (Periodical)",
        "shortcutEs": '1. Daily news sheet: <strong>Periódico</strong> ≈ Direct sibling of <strong>"Periodical"</strong> (printed daily news)! | <strong>Diario</strong> ≈ Sibling of <strong>"Diary / Daily" (Día = Day)</strong> → Daily <em>Newspaper</em>!<br>2. Periodical: <strong>Revista</strong> ≈ <strong>Re- + Vista (View/Look again)</strong> → Glossy monthly <em>Review / Magazine</em>!',
        "shortcutHi": '1. Daily news sheet: <strong>Akhbar</strong> ≈ Plural of <strong>Khabar (News)</strong> + Sounds like <strong>"Ask-Paper"</strong> → Morning <em>Newspaper (Akhbar)</em> with tea!<br>2. Periodical: <strong>Magazine</strong> ≈ Glossy weekly or monthly picture book!',
    },
    1268: {
        "es": "1. Biased influence: Propaganda | 2. Official redaction: Censura",
        "hi": "1. Biased influence: Propaganda / prachaar | 2. Official redaction: Censorship / pabandi",
        "tamil": "1. பிரச்சாரம் (Biased influence) / 2. தணிக்கை (Official redaction)",
        "shortcutEs": '1. Biased influence: <strong>Propaganda</strong> ≈ 100% identical to English <strong>"Propaganda"</strong> (pushing one political view)!<br>2. Official redaction: <strong>Censura</strong> ≈ Direct sibling of English <strong>"Censor / Censorship"</strong> → Official blackout!',
        "shortcutHi": '1. Biased influence: <strong>Propaganda</strong> ≈ One-sided political hype! | <strong>Prachaar</strong> ≈ <strong>Tamil பிரச்சாரம் (Prachaaram!)</strong> → Identical word across Tamil & Hindi = Publicity / <em>Propaganda</em>!<br>2. Official redaction: <strong>Censorship</strong> ≈ Cutting scenes/articles! | <strong>Pabandi</strong> ≈ <strong>Pa-bandh (Tightly bound/restricted)</strong> → Official ban = <em>Censorship</em>!',
    },
    1269: {
        "es": "1. Gossip: Rumor / cotilleo | 2. Exposure: Escándalo",
        "hi": "1. Gossip: Afwah | 2. Exposure: Scandal / badnaami",
        "tamil": "1. வதந்தி (Gossip) / 2. அவதூறு ஊழல் (Exposure)",
        "shortcutEs": '1. Gossip: <strong>Rumor</strong> ≈ 100% identical to English <strong>"Rumor"</strong>! | <strong>Cotilleo</strong> ≈ Sounds like <strong>"Coat-Tell-You"</strong> (whispering gossip behind someone’s coat)!<br>2. Exposure: <strong>Escándalo</strong> ≈ Direct sibling of <strong>"Scandal"</strong>!',
        "shortcutHi": '1. Gossip: <strong>Afwah</strong> ≈ Sounds like blowing <strong>"Off-Air / Hot-Air"</strong> → Unverified street whisper = <em>Rumor (Afwah)</em>!<br>2. Exposure: <strong>Scandal</strong> ≈ Public outrage! | <strong>Badnaami</strong> ≈ <strong>Bad (Bad) + Naam (Name — Tamil நாமம்!)</strong> = Giving someone a <em>Bad Name / Scandal</em>!',
    },
    1270: {
        "es": "Declaración / comunicado",
        "hi": "Bayaan / press release",
        "tamil": "அதிகாரப்பூர்வ அறிக்கை",
        "shortcutEs": '<strong>Declaración</strong> ≈ Direct sibling of <strong>"Declaration"</strong>! | <strong>Comunicado</strong> ≈ Direct sibling of <strong>"Communiqué / Communicate"</strong> → Official news <em>Statement / Release</em>!',
        "shortcutHi": '<strong>Bayaan</strong> ≈ Think <strong>"By-An-Official"</strong> spoken testimony in front of mics = Official <em>Statement (Bayaan)</em>! | <strong>Press release</strong> ≈ Official written bulletin to journalists!',
    },
    1271: {
        "es": "1. Gathered crowd: Público / audiencia | 2. Screen watcher: Espectador / televidente | 3. Audio hearer: Oyente",
        "hi": "1. Gathered crowd: Audience / log | 2. Screen watcher: Dekhne wala / viewer | 3. Audio hearer: Sunne wala / listener",
        "tamil": "1. பார்வையாளர் கூட்டம் (Gathered crowd) / 2. தொலைக்காட்சி பார்வையாளர் (Screen watcher) / 3. கேட்பவர் (Audio hearer)",
        "shortcutEs": '1. Gathered crowd: <strong>Público</strong> ≈ <strong>"Public"</strong> crowd! | <strong>Audiencia</strong> ≈ <strong>"Audience"</strong>!<br>2. Screen watcher: <strong>Espectador</strong> ≈ <strong>"Spectator"</strong>! | <strong>Televidente</strong> ≈ <strong>Tele (TV) + Vidente (Vision)</strong> = TV <em>Viewer</em>!<br>3. Audio hearer: <strong>Oyente</strong> ≈ From <strong>Oír ("Oh-ear!" = Hear)</strong> → Radio/podcast <em>Listener</em>!',
        "shortcutHi": '1. Gathered crowd: <strong>Audience</strong> ≈ Hall crowd! | <strong>Log</strong> ≈ Everyday Hindi word for <strong>People (Tamil உலகம் / Loka)</strong>!<br>2. Screen watcher: <strong>Dekhne wala</strong> ≈ <strong>Dekhna (See) + Wala (-er)</strong> = Watcher / <em>Viewer</em>!<br>3. Audio hearer: <strong>Sunne wala</strong> ≈ <strong>Sunna (Listen) + Wala (-er)</strong> = Hearer / <em>Listener</em>!',
    },
    1272: {
        "es": "1. Learning: Educación / formación | 2. Scholastic adj: Académico / académica",
        "hi": "1. Learning: Padhai-likhai / education | 2. Scholastic adj: Padhai se juda / academic",
        "tamil": "1. கல்வி (Learning) / 2. கல்வி சார்ந்த (Scholastic adj)",
        "shortcutEs": '1. Learning: <strong>Educación</strong> ≈ Direct sibling of <strong>"Education"</strong>! | <strong>Formación</strong> ≈ Direct sibling of <strong>"Formation / Training"</strong> (shaping a student’s mind)!<br>2. Scholastic adj: <strong>Académico / académica</strong> ≈ Direct sibling of <strong>"Academic"</strong>!',
        "shortcutHi": '1. Learning: <strong>Padhai-likhai</strong> ≈ <strong>Padhai (Reading/Study — Tamil படிப்பு!)</strong> + <strong>Likhai (Writing)</strong> → Reading & writing = <em>Education</em>! | <strong>Education</strong> ≈ Formal schooling!<br>2. Scholastic adj: <strong>Padhai se juda</strong> ≈ "Connected to study (Padhai)" = <em>Academic</em>!',
    },
    1273: {
        "es": "1. Learner: Estudiante / alumno / alumna | 2. Class peer: Compañero de clase",
        "hi": "1. Learner: Student / padhne wala | 2. Class peer: Classmate / saath padhne wala",
        "tamil": "1. மாணவர் / மாணவி (Learner) / 2. வகுப்புத் தோழர் (Class peer)",
        "shortcutEs": '1. Learner: <strong>Estudiante</strong> ≈ <strong>"Student"</strong>! | <strong>Alumno / alumna</strong> ≈ Sibling of <strong>"Alumni / Alumnus"</strong> (school pupil)!<br>2. Class peer: <strong>Compañero de clase</strong> ≈ <strong>Compañero ("Companion") + de clase (of class)</strong> = <em>Classmate</em>!',
        "shortcutHi": '1. Learner: <strong>Padhne wala</strong> ≈ <strong>Padhna (Study — Tamil படி!)</strong> + <strong>Wala (-er)</strong> = One who studies = <em>Student / Pupil</em>! | <strong>Student</strong> ≈ Uniform school learner!<br>2. Class peer: <strong>Saath padhne wala</strong> ≈ <strong>Saath (Together) + Padhne wala (Studying)</strong> = <em>Classmate</em>!',
    },
    1274: {
        "es": "Profesor / profesora / maestro / maestra",
        "hi": "Teacher / sir / ma'am",
        "tamil": "ஆசிரியர் / பேராசிரியர்",
        "shortcutEs": '<strong>Profesor / profesora</strong> ≈ Direct match with English <strong>"Professor"</strong>! | <strong>Maestro / maestra</strong> ≈ Direct sibling of <strong>"Master / Maestro"</strong> → Wise school <em>Teacher</em>!',
        "shortcutHi": '<strong>Teacher / sir / ma\'am</strong> ≈ Across all of India (just like in Tamil Nadu), students warmly call their school or college educator <strong>"Sir"</strong>, <strong>"Ma\'am"</strong>, or <strong>"Teacher"</strong>!',
    },
    1275: {
        "es": "1. School headmaster: Director / rector | 2. Primary/main: Principal",
        "hi": "1. School headmaster: Principal | 2. Primary/main: Khaas / mukhya",
        "tamil": "1. பள்ளி முதல்வர் (School headmaster) / 2. முதன்மையான (Primary/main)",
        "shortcutEs": '1. School headmaster: <strong>Director</strong> ≈ <strong>"Director"</strong> of the school! | <strong>Rector</strong> ≈ University <strong>"Rector" / Head</strong>!<br>2. Primary/main: <strong>Principal</strong> ≈ 100% identical to English <strong>"Principal"</strong> (top/main)!',
        "shortcutHi": '1. School headmaster: <strong>Principal</strong> ≈ Head of every school!<br>2. Primary/main: <strong>Khaas</strong> ≈ <strong>Spoken Tamil காஸ் (Special/Chief!)</strong> | <strong>Mukhya</strong> ≈ <strong>Tamil முக்கிய (Mukkiyam = Main/Primary!)</strong> — 100% same word!',
    },
    1276: {
        "es": "1. Room: Aula / salón de clases | 2. Board: Pizarra / pizarrón",
        "hi": "1. Room: Class / classroom | 2. Board: Board / blackboard",
        "tamil": "1. வகுப்பறை (Room) / 2. கரும்பலகை (Board)",
        "shortcutEs": '1. Room: <strong>Aula</strong> ≈ Sounds like study <strong>"Hall-a"</strong>! | <strong>Salón de clases</strong> ≈ <strong>Salón ("Salon / Hall") + Clases</strong> = <em>Classroom</em>!<br>2. Board: <strong>Pizarra / pizarrón</strong> ≈ Slate board hung in class ("Piece-of-Slate") = <em>Blackboard</em>!',
        "shortcutHi": '1. Room: <strong>Class / classroom</strong> ≈ Study hall where students sit with desks!<br>2. Board: <strong>Board / blackboard</strong> ≈ Front wall slate board for chalk/marker writing!',
    },
    1277: {
        "es": "1. Chalk: Tiza | 2. Marker: Marcador / plumón | 3. Rubber/duster: Borrador / goma",
        "hi": "1. Chalk: Chalk | 2. Marker: Marker | 3. Rubber/duster: Duster / eraser",
        "tamil": "1. சுண்ணாம்புக் கட்டி (Chalk) / 2. மார்க்கர் பேனா (Marker) / 3. அழிப்பான் (Rubber/duster)",
        "shortcutEs": '1. Chalk: <strong>Tiza</strong> ≈ Sounds like tiny dusty stick (<strong>"Chalk-Tease-a"</strong>) writing on slate!<br>2. Marker: <strong>Marcador</strong> ≈ <strong>"Marker"</strong>! | <strong>Plumón</strong> ≈ Thick felt-tip <strong>"Plume / Pen"</strong>!<br>3. Rubber/duster: <strong>Borrador</strong> ≈ Wipes away = <em>Board Duster</em>! | <strong>Goma</strong> ≈ <strong>"Gum"</strong> rubber = <em>Pencil Eraser</em>!',
        "shortcutHi": '1. Chalk: <strong>Chalk</strong> ≈ White stick used on blackboards!<br>2. Marker: <strong>Marker</strong> ≈ Ink pen used on whiteboards!<br>3. Rubber/duster: <strong>Duster</strong> (dusts off the blackboard) / <strong>Eraser</strong> (rubs out pencil marks in notebooks)!',
    },
    1278: {
        "es": "1. Course book: Libro de texto | 2. Exercise copy: Cuaderno / libreta",
        "hi": "1. Course book: Kitaab / textbook | 2. Exercise copy: Copy / notebook",
        "tamil": "1. பாடப்புத்தகம் (Course book) / 2. நோட்டுப் புத்தகம் (Exercise copy)",
        "shortcutEs": '1. Course book: <strong>Libro de texto</strong> ≈ <strong>Libro ("Library book") + de texto (text)</strong> = <em>Textbook</em>!<br>2. Exercise copy: <strong>Cuaderno</strong> ≈ Think <strong>"Quad-folded"</strong> lined sheets! | <strong>Libreta</strong> ≈ <strong>Libro (Book) + -eta (Small)</strong> = Pocket <em>Notebook</em>!',
        "shortcutHi": '1. Course book: <strong>Kitaab</strong> ≈ Classic everyday word for <em>Book</em> (<em>Kitaab-ghar</em> = Bookstore)! | <strong>Textbook</strong> ≈ School course book!<br>2. Exercise copy: <strong>Copy</strong> ≈ Across Indian schools, students always call their ruled exercise notebook a <strong>"Copy"</strong>!',
    },
    1279: {
        "es": "1. Document jacket: Carpeta / archivador | 2. Papers: Documento",
        "hi": "1. Document jacket: Folder / file | 2. Papers: Document / kagazaat",
        "tamil": "1. கோப்புறை (Document jacket) / 2. ஆவணம் (Papers)",
        "shortcutEs": '1. Document jacket: <strong>Carpeta</strong> ≈ Sounds like stiff cardboard <strong>"Carpet-Fold"</strong> holding papers = <em>Folder</em>! | <strong>Archivador</strong> ≈ Sibling of <strong>"Archive"</strong> = Ring <em>File / Binder</em>!<br>2. Papers: <strong>Documento</strong> ≈ Direct match with <strong>"Document"</strong>!',
        "shortcutHi": '1. Document jacket: <strong>Folder / file</strong> ≈ Plastic or cardboard sleeve holding office sheets!<br>2. Papers: <strong>Kagazaat</strong> ≈ Plural of <strong>Kagaz (Tamil காகிதம் = Paper!)</strong> → Important legal/office sheets = <em>Documents (Kagazaat)</em>!',
    },
    1280: {
        "es": "1. Pen: Bolígrafo / pluma | 2. Pencil: Lápiz | 3. Measuring ruler: Regla",
        "hi": "1. Pen: Pen / kalam | 2. Pencil: Pencil | 3. Measuring ruler: Scale / ruler / patri",
        "tamil": "1. பேனா (Pen) / 2. பென்சில் (Pencil) / 3. அளவுகோல் (Measuring ruler)",
        "shortcutEs": '1. Pen: <strong>Bolígrafo</strong> ≈ <strong>Boli (Ballpoint!) + Grafo (Write)</strong>! | <strong>Pluma</strong> ≈ Feather <strong>"Plume"</strong> quill pen!<br>2. Pencil: <strong>Lápiz</strong> ≈ Think drawing <strong>"Lap-lines"</strong> on paper = <em>Pencil</em>!<br>3. Measuring ruler: <strong>Regla</strong> ≈ Direct sibling of <strong>"Regular / Ruler"</strong> (straight 12-inch edge)!',
        "shortcutHi": '1. Pen: <strong>Kalam</strong> ≈ Classic word for a writing pen (like <em>Kalam-dawaat</em> / pen & ink)! | <strong>Pen</strong> ≈ Ballpoint!<br>2. Pencil: <strong>Pencil</strong> ≈ Graphite writing stick!<br>3. Measuring ruler: <strong>Scale</strong> (used across India for a plastic 15cm ruler!) | <strong>Patri</strong> ≈ Flat wooden/steel measuring strip = <em>Ruler (Patri)</em>!',
    },
    1281: {
        "es": "1. Unit: Lección / clase | 2. Formal talk: Conferencia / clase magistral",
        "hi": "1. Unit: Sabaq / lesson | 2. Formal talk: Lecture",
        "tamil": "1. பாடம் (Unit) / 2. விரிவுரை (Formal talk)",
        "shortcutEs": '1. Unit: <strong>Lección</strong> ≈ Direct match with <strong>"Lesson"</strong>! | <strong>Clase</strong> ≈ <strong>"Class"</strong> session!<br>2. Formal talk: <strong>Conferencia</strong> ≈ Professor’s <strong>"Conference"</strong> talk! | <strong>Clase magistral</strong> ≈ "Master’s class" = University <em>Lecture</em>!',
        "shortcutHi": '1. Unit: <strong>Sabaq</strong> ≈ Classic word for a taught moral/chapter ("Learn your <em>Sabaq</em> well!") = <em>Lesson</em>! | <strong>Lesson</strong> ≈ Book chapter!<br>2. Formal talk: <strong>Lecture</strong> ≈ Long college classroom talk by a professor!',
    },
    1282: {
        "es": "1. Daily homework: Tarea / deberes | 2. Graded project: Trabajo / asignación | 3. Composition: Ensayo / redacción",
        "hi": "1. Daily homework: Homework | 2. Graded project: Assignment | 3. Composition: Essay",
        "tamil": "1. வீட்டுப்பாடம் (Daily homework) / 2. ஒப்படைப்புப் பணி (Graded project) / 3. கட்டுரை (Composition)",
        "shortcutEs": '1. Daily homework: <strong>Tarea</strong> ≈ Sounds like <strong>"Task-area"</strong>! | <strong>Deberes</strong> ≈ From <strong>Deber ("Duty")</strong> = After-school duties (<em>Homework</em>)!<br>2. Graded project: <strong>Trabajo</strong> (Work) / <strong>Asignación</strong> (<strong>"Assignment"</strong>)!<br>3. Composition: <strong>Ensayo</strong> (<strong>"Essay"</strong>!) / <strong>Redacción</strong> (<strong>"Redaction / Write-up"</strong>)!',
        "shortcutHi": '1. Daily homework: <strong>Homework</strong> ≈ Take-home school practice sheets!<br>2. Graded project: <strong>Assignment</strong> ≈ Take-home graded college project!<br>3. Composition: <strong>Essay</strong> ≈ Multi-paragraph school composition!',
    },
    1283: {
        "es": "Examen / prueba",
        "hi": "Exam / imtehan / test",
        "tamil": "தேர்வு / வினாடி வினா",
        "shortcutEs": '<strong>Examen</strong> ≈ Direct match with <strong>"Exam"</strong>! | <strong>Prueba</strong> ≈ Direct sibling of <strong>"Prove / Probe"</strong> → Classroom test to prove what you know = <em>Test / Quiz</em>!',
        "shortcutHi": '<strong>Imtehan</strong> ≈ Famous Bollywood/daily word <strong>"Imtehan"</strong> (<em>Zindagi ka imtehan</em> = Test of life!) → Formal school/board <em>Exam / Test</em>! | <strong>Exam / test</strong> ≈ Timed answer sheets!',
    },
    1284: {
        "es": "1. Mark evaluation: Nota / calificación | 2. Points total: Puntuación / puntaje | 3. Standing tier: Puesto / rango",
        "hi": "1. Mark evaluation: Marks / number / grade | 2. Points total: Score | 3. Standing tier: Rank",
        "tamil": "1. மதிப்பெண் தரம் (Mark evaluation) / 2. மொத்தப் புள்ளிகள் (Points total) / 3. தரவரிசை (Standing tier)",
        "shortcutEs": '1. Mark evaluation: <strong>Nota</strong> ("Report Note") / <strong>Calificación</strong> ("Qualification mark") = Report-card <em>Grade</em>!<br>2. Points total: <strong>Puntuación / puntaje</strong> ≈ Root of <strong>"Points"</strong> = Game/exam <em>Score</em>!<br>3. Standing tier: <strong>Puesto</strong> ("Post/Place") / <strong>Rango</strong> (<strong>"Rank"</strong>)!',
        "shortcutHi": '1. Mark evaluation: <strong>Marks / number / grade</strong> ≈ In India everyone asks <em>"Kitne number aaye?"</em> (How many <em>Marks</em> on your report card?)!<br>2. Points total: <strong>Score</strong> ≈ Running total on board/test!<br>3. Standing tier: <strong>Rank</strong> ≈ 1st/2nd/3rd position in class!',
    },
    1285: {
        "es": "Semestre / período escolar",
        "hi": "Semester / term",
        "tamil": "பருவம் / கல்விப் பருவம்",
        "shortcutEs": '<strong>Semestre</strong> ≈ Direct match with <strong>"Semester"</strong> (6-month half-year)! | <strong>Período escolar</strong> ≈ <strong>Period + School ("Escolar")</strong> = School <em>Term</em>!',
        "shortcutHi": '<strong>Semester / term</strong> ≈ 6-month college half (<em>Semester</em>) or 3–4 month school exam division (<em>Term</em>)!',
    },
    1286: {
        "es": "1. Grant award: Beca | 2. Course fees: Matrícula / colegiatura",
        "hi": "1. Grant award: Scholarship | 2. Course fees: Fees / padhai ka kharcha",
        "tamil": "1. கல்வி உதவித்தொகை (Grant award) / 2. கல்விக் கட்டணம் (Course fees)",
        "shortcutEs": '1. Grant award: <strong>Beca</strong> ≈ Sounds like <strong>"Back-a-student!"</strong> → Money backing a topper’s studies = <em>Scholarship</em>!<br>2. Course fees: <strong>Matrícula</strong> (<strong>"Matriculation"</strong> enrollment fee) / <strong>Colegiatura</strong> (<strong>"College"</strong> fee) = <em>Tuition</em>!',
        "shortcutHi": '1. Grant award: <strong>Scholarship</strong> ≈ Merit cash grant paying for studies!<br>2. Course fees: <strong>Padhai ka kharcha</strong> ≈ <strong>Padhai (Study — Tamil படிப்பு!)</strong> + <strong>Kharcha (Expense — செலவு!)</strong> = Cost of studying = <em>Tuition / Fees</em>!',
    },
    1287: {
        "es": "1. University graduation: Título universitario / carrera | 2. Parchment award: Diploma / certificado",
        "hi": "1. University graduation: Degree | 2. Parchment award: Certificate / diploma",
        "tamil": "1. பல்கலைக்கழகப் பட்டம் (University graduation) / 2. சான்றிதழ் / பட்டயம் (Parchment award)",
        "shortcutEs": '1. University graduation: <strong>Título universitario</strong> ≈ University <strong>"Title"</strong>! | <strong>Carrera</strong> ≈ <strong>"Career"</strong> major!<br>2. Parchment award: <strong>Diploma</strong> (<strong>"Diploma"</strong>!) / <strong>Certificado</strong> (<strong>"Certificate"</strong>!)!',
        "shortcutHi": '1. University graduation: <strong>Degree</strong> ≈ B.A. / B.Tech / Master’s university title!<br>2. Parchment award: <strong>Certificate / diploma</strong> ≈ Framed merit parchment for completing a skill course or workshop!',
    },
    1288: {
        "es": "1. Commencement: Graduación | 2. College grounds: Campus universitario",
        "hi": "1. Commencement: Graduation | 2. College grounds: Campus",
        "tamil": "1. பட்டமளிப்பு விழா (Commencement) / 2. கல்லூரி வளாகம் (College grounds)",
        "shortcutEs": '1. Commencement: <strong>Graduación</strong> ≈ Direct sibling of <strong>"Graduation"</strong> (throwing black caps in the air)!<br>2. College grounds: <strong>Campus universitario</strong> ≈ 100% identical to <strong>"University Campus"</strong>!',
        "shortcutHi": '1. Commencement: <strong>Graduation</strong> ≈ Convocation ceremony wearing robes and tossing mortarboard caps!<br>2. College grounds: <strong>Campus</strong> ≈ University lawns, hostels, and lecture blocks together!',
    },
    1289: {
        "es": "1. Knowledge field: Ciencia | 2. Probe / investigator: Investigación / investigador",
        "hi": "1. Knowledge field: Science | 2. Probe / investigator: Research / khoj",
        "tamil": "1. அறிவியல் (Knowledge field) / 2. ஆராய்ச்சி / ஆராய்ச்சியாளர் (Probe / investigator)",
        "shortcutEs": '1. Knowledge field: <strong>Ciencia</strong> ≈ Direct sibling of <strong>"Science"</strong>!<br>2. Probe / investigator: <strong>Investigación / investigador</strong> ≈ Direct sibling of <strong>"Investigation / Investigator"</strong> → Deep scientific probing = <em>Research / Researcher</em>!',
        "shortcutHi": '1. Knowledge field: <strong>Science</strong> ≈ Physics, Chemistry, and Biology lab knowledge!<br>2. Probe / investigator: <strong>Khoj</strong> ≈ Digging/searching deeply for a hidden truth (<strong>Khojna</strong> = To search) = <em>Research / Discovery</em>!',
    },
    1290: {
        "es": "Historia",
        "hi": "Itihaas / tareekh",
        "tamil": "வரலாறு",
        "shortcutEs": '<strong>Historia</strong> ≈ Direct match with English <strong>"History"</strong> (chronicle of past empires)!',
        "shortcutHi": '<strong>Itihaas</strong> ≈ <strong>Tamil இதிகாசம் (Idhihaasam = Great Epic / History!)</strong> → 100% same word! | <strong>Tareekh</strong> ≈ Famous court phrase <em>"Tareekh pe tareekh!"</em> = Dates of the past = <em>History</em>!',
    },
    1291: {
        "es": "Geografía",
        "hi": "Geography",
        "tamil": "புவியியல்",
        "shortcutEs": '<strong>Geografía</strong> ≈ Direct sibling of English <strong>"Geography" (Geo = Earth + Graph = Map/Write)</strong>!',
        "shortcutHi": '<strong>Geography</strong> ≈ School map, continents, rivers, and globe study (or formal <em>Bhugol</em> — <em>Bhu</em> = Earth like Tamil <em>Bhoomi</em>)!',
    },
    1292: {
        "es": "Matemáticas / mates",
        "hi": "Maths / hisaab",
        "tamil": "கணிதம்",
        "shortcutEs": '<strong>Matemáticas / mates</strong> ≈ Direct match with English <strong>"Mathematics / Maths"</strong>!',
        "shortcutHi": '<strong>Hisaab</strong> ≈ Used in spoken Tamil <strong>இசாப் / கணக்கு</strong> → Everyday shopkeeping count (<em>"Hisaab do!"</em> = Calculate the numbers!) = <em>Maths</em>! | <strong>Maths</strong> ≈ Numbers & algebra!',
    },
    1293: {
        "es": "Física",
        "hi": "Physics",
        "tamil": "இயற்பியல்",
        "shortcutEs": '<strong>Física</strong> ≈ Direct match with English <strong>"Physics"</strong> (study of physical forces, gravity, and light)!',
        "shortcutHi": '<strong>Physics</strong> ≈ Science of Newton’s cradle, motion, forces, electricity, and energy!',
    },
    1294: {
        "es": "Química",
        "hi": "Chemistry",
        "tamil": "வேதியியல்",
        "shortcutEs": '<strong>Química</strong> ≈ Same root as <strong>"Chemical / Alchemy"</strong> → Mixing colored liquids in beakers = <em>Chemistry</em>!',
        "shortcutHi": '<strong>Chemistry</strong> ≈ Periodic table, reactions, acids, and colorful glass beakers in a lab!',
    },
    1295: {
        "es": "Biología",
        "hi": "Biology",
        "tamil": "உயிரியல்",
        "shortcutEs": '<strong>Biología</strong> ≈ Direct match with English <strong>"Biology" (Bio = Life + Logy = Study)</strong>!',
        "shortcutHi": '<strong>Biology</strong> ≈ Science of living cells, plants, animals, and bacteria in petri dishes!',
    },
    1296: {
        "es": "Literatura",
        "hi": "Literature",
        "tamil": "இலக்கியம்",
        "shortcutEs": '<strong>Literatura</strong> ≈ Direct match with English <strong>"Literature"</strong> (classic novels, poetry, and written masterpieces)!',
        "shortcutHi": '<strong>Literature</strong> ≈ Classic bound novels, poetry shelves, and timeless storytelling!',
    },
    1297: {
        "es": "1. Thinking inquiry: Filosofía | 2. Moral code: Ética / moral",
        "hi": "1. Thinking inquiry: Philosophy | 2. Moral code: Ethics / sahi-galat",
        "tamil": "1. தத்துவம் (Thinking inquiry) / 2. அறநெறி (Moral code)",
        "shortcutEs": '1. Thinking inquiry: <strong>Filosofía</strong> ≈ Direct match with <strong>"Philosophy"</strong> (Philo = Love + Sophia = Wisdom)!<br>2. Moral code: <strong>Ética</strong> (<strong>"Ethics"</strong>!) / <strong>Moral</strong> (<strong>"Moral"</strong>!)!',
        "shortcutHi": '1. Thinking inquiry: <strong>Philosophy</strong> ≈ Deep thinking about life and truth (like Rodin’s Thinker)!<br>2. Moral code: <strong>Sahi-galat</strong> ≈ <strong>Sahi (Right — Spoken Tamil சரி!)</strong> + <strong>Galat (Wrong!)</strong> → Judging right vs wrong = <em>Ethics / Morals</em>!',
    },
    1298: {
        "es": "1. Mind science: Psicología | 2. Conduct: Comportamiento / conducta",
        "hi": "1. Mind science: Psychology | 2. Conduct: Bartaav / rawaiya",
        "tamil": "1. உளவியல் (Mind science) / 2. நடத்தை (Conduct)",
        "shortcutEs": '1. Mind science: <strong>Psicología</strong> ≈ Direct match with <strong>"Psychology"</strong> (same silent P: <em>Psyche</em> = Mind)!<br>2. Conduct: <strong>Comportamiento</strong> (<strong>"Comportment"</strong> = how you carry yourself) / <strong>Conducta</strong> (<strong>"Conduct"</strong>)!',
        "shortcutHi": '1. Mind science: <strong>Psychology</strong> ≈ Science of how thoughts and feelings work!<br>2. Conduct: <strong>Bartaav / rawaiya</strong> ≈ <strong>Bartaav</strong> (How you treat people) & <strong>Rawaiya</strong> ("Attitude / Way" — Rhymes with <em>Way-ya</em>) = <em>Behavior / Attitude</em>!',
    },
    1299: {
        "es": "1. Tongue: Idioma / lengua | 2. Syntax: Gramática | 3. Words stock: Vocabulario",
        "hi": "1. Tongue: Bhasha / zabaan | 2. Syntax: Grammar | 3. Words stock: Vocabulary",
        "tamil": "1. மொழி (Tongue) / 2. இலக்கணம் (Syntax) / 3. சொற்களஞ்சியம் (Words stock)",
        "shortcutEs": '1. Tongue: <strong>Idioma</strong> (<strong>"Idiom"</strong>) / <strong>Lengua</strong> (literally <strong>"Tongue"</strong> = Tamil நாக்கு/மொழி)!<br>2. Syntax: <strong>Gramática</strong> ≈ Direct match with <strong>"Grammar"</strong>!<br>3. Words stock: <strong>Vocabulario</strong> ≈ Direct match with <strong>"Vocabulary"</strong>!',
        "shortcutHi": '1. Tongue: <strong>Bhasha</strong> ≈ <strong>Tamil பாஷை (Baashai = Language!)</strong> | <strong>Zabaan</strong> ≈ Literally "Tongue/Speech"!<br>2. Syntax: <strong>Grammar</strong> ≈ Sentence rules!<br>3. Words stock: <strong>Vocabulary</strong> ≈ Word power you are mastering right now!',
    },
    1300: {
        "es": "Laboratorio",
        "hi": "Lab",
        "tamil": "ஆய்வகம்",
        "shortcutEs": '<strong>Laboratorio</strong> ≈ Direct match with English <strong>"Laboratory"</strong>!',
        "shortcutHi": '<strong>Lab</strong> ≈ Science testing room filled with microscopes, test tubes, and lab coats!',
    },
    1301: {
        "es": "1. Empirical test: Experimento / prueba | 2. Verb - try out: Experimentar",
        "hi": "1. Empirical test: Experiment / aazmana | 2. Verb - try out: Experiment karna / aazma kar dekhna",
        "tamil": "1. அறிவியல் பரிசோதனை (Empirical test) / 2. பரிசோதித்துப் பார் (Verb: try out)",
        "shortcutEs": '1. Empirical test: <strong>Experimento</strong> (<strong>"Experiment"</strong>!) / <strong>Prueba</strong> (<strong>"Proof / Test"</strong>!)<br>2. Verb - try out: <strong>Experimentar</strong> ≈ Adding <strong>-ar</strong> makes <strong>"To Experiment / Try out"</strong>!',
        "shortcutHi": '1. Empirical test: <strong>Aazmana</strong> ≈ Testing/trying out something new! | <strong>Experiment</strong> ≈ Lab trial!<br>2. Verb - try out: <strong>Aazma kar dekhna</strong> ≈ <strong>Aazma kar</strong> (By testing) + <strong>Dekhna</strong> (See what happens) = <em>Try out / Experiment</em>!',
    },
    1302: {
        "es": "Teoría / principio",
        "hi": "Theory / niyam",
        "tamil": "கோட்பாடு / அடிப்படை விதி",
        "shortcutEs": '<strong>Teoría</strong> ≈ Direct match with English <strong>"Theory"</strong>! | <strong>Principio</strong> ≈ Direct sibling of English <strong>"Principle"</strong> (first rule)!',
        "shortcutHi": '<strong>Theory</strong> ≈ Scientific explanation like Einstein’s relativity! | <strong>Niyam</strong> ≈ 100% identical to <strong>Tamil நியமம் / நியதி (Niyamam = Fixed Law / Principle!)</strong>!',
    },
    1303: {
        "es": "1. Found existing: Descubrimiento | 2. Created new: Invento / invención",
        "hi": "1. Found existing: Khoj | 2. Created new: Invention / nayi cheez banana",
        "tamil": "1. கண்டுபிடிப்பு (Found existing) / 2. புதிய உருவாக்கம் (Created new)",
        "shortcutEs": '1. Found existing: <strong>Descubrimiento</strong> ≈ <strong>Des- (Un-) + Cubrir ("Cover")</strong> → Literally <strong>"Un-covering" (Discovery)</strong> of something already out there!<br>2. Created new: <strong>Invento / invención</strong> ≈ Direct match with <strong>"Invention"</strong>!',
        "shortcutHi": '1. Found existing: <strong>Khoj</strong> ≈ Finding an existing hidden star, land, or cure = <em>Discovery (Khoj)</em>!<br>2. Created new: <strong>Nayi cheez banana</strong> ≈ <strong>Nayi cheez</strong> (New thing) + <strong>Banana</strong> (To build) = Building something brand new = <em>Invention</em>!',
    },
    1304: {
        "es": "1. Records: Datos | 2. Probability math: Estadísticas | 3. Breakdown study: Análisis",
        "hi": "1. Records: Data | 2. Probability math: Statistics | 3. Breakdown study: Analysis",
        "tamil": "1. தரவுகள் (Records) / 2. புள்ளியியல் (Probability math) / 3. பகுப்பாய்வு (Breakdown study)",
        "shortcutEs": '1. Records: <strong>Datos</strong> ≈ Direct match with <strong>"Data"</strong>!<br>2. Probability math: <strong>Estadísticas</strong> ≈ Direct match with <strong>"Statistics"</strong>!<br>3. Breakdown study: <strong>Análisis</strong> ≈ Direct match with <strong>"Analysis"</strong>!',
        "shortcutHi": '1. Records: <strong>Data</strong> ≈ Raw digital numbers & database records!<br>2. Probability math: <strong>Statistics</strong> ≈ Averages, percentages, and charts!<br>3. Breakdown study: <strong>Analysis</strong> ≈ Deep step-by-step inspection of facts!',
    },
    1305: {
        "es": "1. Dimension size: Medida / medición | 2. Specimen piece: Muestra",
        "hi": "1. Dimension size: Naap | 2. Specimen piece: Sample",
        "tamil": "1. அளவீடு (Dimension size) / 2. சோதனை மாதிரி (Specimen piece)",
        "shortcutEs": '1. Dimension size: <strong>Medida / medición</strong> ≈ Sibling of <strong>"Measure / Dimension"</strong> (measuring tape length)!<br>2. Specimen piece: <strong>Muestra</strong> ≈ From <strong>Mostrar ("Demonstrate / Show")</strong> → Tiny piece shown to prove quality = <em>Sample</em>!',
        "shortcutHi": '1. Dimension size: <strong>Naap</strong> ≈ Tailor’s measuring tape reading (<em>Naap lena</em> = Take measurements — sounds like "Tape/Snap" a size)!<br>2. Specimen piece: <strong>Sample</strong> ≈ Small blood swab or free trial piece!',
    },
    1306: {
        "es": "Fórmula / ecuación",
        "hi": "Formula",
        "tamil": "சூத்திரம் / சமன்பாடு",
        "shortcutEs": '<strong>Fórmula</strong> ≈ Direct match with <strong>"Formula"</strong>! | <strong>Ecuación</strong> ≈ Direct match with <strong>"Equation" (Equa = Equal "=")</strong>!',
        "shortcutHi": '<strong>Formula</strong> ≈ Famous math recipe like <em>E = mc²</em> (<em>"Sahi formula lagao!"</em> = Apply the right <em>Formula / Equation</em>)!',
    },
    1307: {
        "es": "Materia / sustancia",
        "hi": "Cheez / substance",
        "tamil": "பருப்பொருள் / வேதிப்பொருள்",
        "shortcutEs": '<strong>Materia</strong> ≈ Direct match with <strong>"Matter"</strong>! | <strong>Sustancia</strong> ≈ Direct match with <strong>"Substance"</strong> (solid/liquid/gas stuff)!',
        "shortcutHi": '<strong>Cheez</strong> ≈ Any tangible physical object/thing in front of you! | <strong>Substance</strong> ≈ Specific pure chemical material inside a vial!',
    },
    1308: {
        "es": "1. Atom unit: Átomo | 2. Compound bond: Molécula",
        "hi": "1. Atom unit: Atom | 2. Compound bond: Molecule",
        "tamil": "1. அணு (Atom unit) / 2. மூலக்கூறு (Compound bond)",
        "shortcutEs": '1. Atom unit: <strong>Átomo</strong> ≈ Direct match with <strong>"Atom"</strong> (Greek <em>A-tomos</em> = uncuttable unit)!<br>2. Compound bond: <strong>Molécula</strong> ≈ Direct match with <strong>"Molecule"</strong> (bonded ball-and-stick group)!',
        "shortcutHi": '1. Atom unit: <strong>Atom</strong> ≈ Single smallest proton/electron unit of matter!<br>2. Compound bond: <strong>Molecule</strong> ≈ Two or more atoms linked together like H₂O!',
    },
    1309: {
        "es": "1. Power capacity: Energía | 2. Vector push/pull: Fuerza",
        "hi": "1. Power capacity: Energy / taakat | 2. Vector push/pull: Zor / force",
        "tamil": "1. ஆற்றல் (Power capacity) / 2. விசை / பலம் (Vector push/pull)",
        "shortcutEs": '1. Power capacity: <strong>Energía</strong> ≈ Direct match with <strong>"Energy"</strong>!<br>2. Vector push/pull: <strong>Fuerza</strong> ≈ Direct sibling of <strong>"Force"</strong> (pushing a heavy door)!',
        "shortcutHi": '1. Power capacity: <strong>Taakat</strong> ≈ <strong>Spoken Tamil தாகத்து / பலம்</strong> (Body strength / stamina)! | <strong>Energy</strong> ≈ Solar/battery power!<br>2. Vector push/pull: <strong>Zor</strong> ≈ <em>"Zor lagake haisha!"</em> (Push with full <em>Force</em>!)!',
    },
    1310: {
        "es": "1. Planetary pull: Gravedad | 2. Movement: Movimiento | 3. Velocity rate: Velocidad / rapidez",
        "hi": "1. Planetary pull: Gravity | 2. Movement: Harkat | 3. Velocity rate: Speed / raftaar",
        "tamil": "1. புவியீர்ப்பு விசை (Planetary pull) / 2. இயக்கம் (Movement) / 3. வேகம் (Velocity rate)",
        "shortcutEs": '1. Planetary pull: <strong>Gravedad</strong> ≈ <strong>"Gravity"</strong>!<br>2. Movement: <strong>Movimiento</strong> ≈ <strong>"Movement"</strong>!<br>3. Velocity rate: <strong>Velocidad</strong> (<strong>"Velocity"</strong>!) / <strong>Rapidez</strong> (<strong>"Rapidness"</strong>)!',
        "shortcutHi": '1. Planetary pull: <strong>Gravity</strong> ≈ Earth pulling Newton’s apple down!<br>2. Movement: <strong>Harkat</strong> ≈ Any tiny physical twitch or motion (<em>"Harkat mein aana!"</em> = Come into <em>Motion</em>)!<br>3. Velocity rate: <strong>Raftaar</strong> ≈ Famous Hindi word for blazing vehicle/train <em>Speed</em>!',
    },
    1311: {
        "es": "1. Matter quantity: Masa | 2. Heaviness: Peso",
        "hi": "1. Matter quantity: Mass | 2. Heaviness: Vajan",
        "tamil": "1. பொருண்மை (Matter quantity) / 2. எடை (Heaviness)",
        "shortcutEs": '1. Matter quantity: <strong>Masa</strong> ≈ Direct match with <strong>"Mass"</strong> (total matter inside)!<br>2. Heaviness: <strong>Peso</strong> ≈ Sibling of <strong>"Peso / Poise"</strong> (pounds/kg pulling down on a balance scale = <em>Weight</em>)!',
        "shortcutHi": '1. Matter quantity: <strong>Mass</strong> ≈ Physics amount of matter in an object!<br>2. Heaviness: <strong>Vajan</strong> ≈ Everyday bazaar word when weighing fruit or gym plates: <em>"Kitna vajan hai?"</em> = How much <em>Weight</em>?!',
    },
    1312: {
        "es": "1. Physical force: Presión | 2. Mental strain: Presión / tensión",
        "hi": "1. Physical force: Dabav / pressure | 2. Mental strain: Tanaav / tension",
        "tamil": "1. இயற்பியல் அழுத்தம் (Physical force) / 2. மன அழுத்தம் (Mental strain)",
        "shortcutEs": '1. Physical force: <strong>Presión</strong> ≈ Direct sibling of <strong>"Press / Pressure"</strong> (gauge dial psi)!<br>2. Mental strain: <strong>Presión / tensión</strong> ≈ Direct match with <strong>"Pressure / Tension"</strong>!',
        "shortcutHi": '1. Physical force: <strong>Dabav</strong> ≈ From <strong>Dabana</strong> (Press/Push down physically — like pressing a button or gauge!) = <em>Pressure</em>!<br>2. Mental strain: <strong>Tanaav</strong> ≈ Tightly stretched wire ("Tense-up!") = <em>Mental Tension / Strain</em>!',
    },
    1313: {
        "es": "Radiación / rayo",
        "hi": "Kiran / radiation",
        "tamil": "கதிர்வீச்சு / ஒளிக்கதிர்",
        "shortcutEs": '<strong>Radiación</strong> ≈ Direct match with <strong>"Radiation"</strong> (X-ray / nuclear waves)! | <strong>Rayo</strong> ≈ Direct match with <strong>"Ray"</strong> (sunlight beam or X-ray)!',
        "shortcutHi": '<strong>Kiran</strong> ≈ <strong>Tamil கிரணம் (Kiranam = Sunbeam/Ray!)</strong> → 100% same word (famous Indian name <em>Kiran</em> = Ray of light!) | <strong>Radiation</strong> ≈ Invisible X-rays!',
    },
    1314: {
        "es": "1. Power: Electricidad | 2. Current flow: Corriente eléctrica | 3. Potential: Voltaje",
        "hi": "1. Power: Bijli / electricity | 2. Current flow: Current | 3. Potential: Voltage",
        "tamil": "1. மின்சாரம் (Power) / 2. மின்னோட்டம் (Current flow) / 3. மின்னழுத்தம் (Potential)",
        "shortcutEs": '1. Power: <strong>Electricidad</strong> ≈ Direct match with <strong>"Electricity"</strong>!<br>2. Current flow: <strong>Corriente eléctrica</strong> ≈ <strong>"Current + Electric"</strong>!<br>3. Potential: <strong>Voltaje</strong> ≈ Direct match with <strong>"Voltage"</strong>!',
        "shortcutHi": '1. Power: <strong>Bijli</strong> ≈ Everyday word when power goes out ("<em>Bijli chali gayi!</em>") or lightning flashes!<br>2. Current flow: <strong>Current</strong> ≈ Live wire flow ("Current lag jayega!")!<br>3. Potential: <strong>Voltage</strong> ≈ High/low power spike on stabilizers!',
    },
    1315: {
        "es": "Imán / magnético",
        "hi": "Chumbak / magnetic",
        "tamil": "காந்தம் / காந்த ஈர்ப்பு",
        "shortcutEs": '<strong>Imán</strong> ≈ Think metal pulled <strong>"In-to-Man"</strong> like magic iron attraction = <em>Magnet</em>! | <strong>Magnético</strong> ≈ Direct match with <strong>"Magnetic"</strong>!',
        "shortcutHi": '<strong>Chumbak</strong> ≈ Sounds like steel pieces going <strong>"Chum-Back!" (Kissing back together!)</strong> → Metal snapping together = <em>Magnet (Chumbak)</em>!',
    },
    1316: {
        "es": "Tecnología / digital",
        "hi": "Technology / digital",
        "tamil": "தொழில்நுட்பம் / டிஜிட்டல்",
        "shortcutEs": '<strong>Tecnología</strong> ≈ Direct match with <strong>"Technology"</strong>! | <strong>Digital</strong> ≈ 100% identical to <strong>"Digital"</strong>!',
        "shortcutHi": '<strong>Technology / digital</strong> ≈ Robotics, smartphones, UPI payments, and modern machines spoken verbatim across Hindi!',
    },
    1317: {
        "es": "Pantalla / monitor",
        "hi": "Screen / display",
        "tamil": "திரை / கணினித் திரை",
        "shortcutEs": '<strong>Pantalla</strong> ≈ Flat <strong>"Panel"</strong> you watch! | <strong>Monitor</strong> ≈ 100% identical to <strong>"Monitor"</strong> (desk PC display)!',
        "shortcutHi": '<strong>Screen / display</strong> ≈ Phone glass or PC monitor you are reading right now!',
    },
    1318: {
        "es": "Teclado",
        "hi": "Keyboard",
        "tamil": "விசைப்பலகை (கீபோர்டு)",
        "shortcutEs": '<strong>Teclado</strong> ≈ From <strong>Tecla (Button/Key — sounds like "Tick-la!" key clicking)</strong> → Row of keys = <em>Keyboard</em>!',
        "shortcutHi": '<strong>Keyboard</strong> ≈ Plastic typing board with A-Z keys and spacebar!',
    },
    1319: {
        "es": "1. Hardcopy machine: Impresora | 2. Image digitizer: Escáner",
        "hi": "1. Hardcopy machine: Printer | 2. Image digitizer: Scanner",
        "tamil": "1. அச்சுப்பொறி (Hardcopy machine) / 2. ஸ்கேனர் (Image digitizer)",
        "shortcutEs": '1. Hardcopy machine: <strong>Impresora</strong> ≈ Root of <strong>"Impress / Imprint"</strong> → Pressing ink onto paper = <em>Printer</em>!<br>2. Image digitizer: <strong>Escáner</strong> ≈ Direct match with <strong>"Scanner"</strong> (Es- + canner)!',
        "shortcutHi": '1. Hardcopy machine: <strong>Printer</strong> ≈ Laser/inkjet office machine spitting out paper printouts!<br>2. Image digitizer: <strong>Scanner</strong> ≈ Glass lid machine digitizing IDs and photos!',
    },
    1320: {
        "es": "1. Voice input: Micrófono / micro | 2. Audio output: Altavoz / parlante",
        "hi": "1. Voice input: Mic | 2. Audio output: Speaker",
        "tamil": "1. ஒலிவாங்கி / மைக் (Voice input) / 2. ஒலிபெருக்கி (Audio output)",
        "shortcutEs": '1. Voice input: <strong>Micrófono / micro</strong> ≈ Direct match with <strong>"Microphone / Mic"</strong>!<br>2. Audio output: <strong>Altavoz</strong> ≈ <strong>Alto (High/Loud) + Voz ("Voice")</strong> = Loudspeaker! | <strong>Parlante</strong> ≈ From <strong>Parlar ("Parlor / Speak")</strong>!',
        "shortcutHi": '1. Voice input: <strong>Mic</strong> ≈ Handheld stage voice pickup!<br>2. Audio output: <strong>Speaker</strong> ≈ Boombox or Bluetooth sound box!',
    },
    1321: {
        "es": "Cable / alambre",
        "hi": "Taar / cable",
        "tamil": "கேபிள் / மின்கம்பி",
        "shortcutEs": '<strong>Cable</strong> ≈ 100% identical to <strong>"Cable"</strong>! | <strong>Alambre</strong> ≈ Thin bare metal filament inside a cord (like "Aluminum-Wire") = <em>Wire</em>!',
        "shortcutHi": '<strong>Taar</strong> ≈ <strong>Tamil தந்தி / கம்பி</strong> (Even classic Indian Telegrams were called <strong>"Taar"</strong> because messages ran over copper <em>Wire (Taar)</em>!) | <strong>Cable</strong> ≈ Thick insulated cord!',
    },
    1322: {
        "es": "1. Physical computer parts: Hardware | 2. Digital applications: Software",
        "hi": "1. Physical computer parts: Hardware | 2. Digital applications: Software",
        "tamil": "1. வன்பொருள் (Physical computer parts) / 2. மென்பொருள் (Digital applications)",
        "shortcutEs": '1. Physical computer parts: <strong>Hardware</strong> ≈ 100% identical international computing term!<br>2. Digital applications: <strong>Software</strong> ≈ 100% identical international computing term!',
        "shortcutHi": '1. Physical computer parts: <strong>Hardware</strong> ≈ Solid chips, keyboard, and motherboard you can touch!<br>2. Digital applications: <strong>Software</strong> ≈ Code, apps, and OS inside the computer!',
    },
    1323: {
        "es": "Código / programa",
        "hi": "Code / program",
        "tamil": "நிரல் குறியீடு / மென்பொருள் நிரல்",
        "shortcutEs": '<strong>Código</strong> ≈ Direct match with <strong>"Code"</strong>! | <strong>Programa</strong> ≈ Direct match with <strong>"Program"</strong>!',
        "shortcutHi": '<strong>Code / program</strong> ≈ Lines of Python/JS instructions written by developers!',
    },
    1324: {
        "es": "1. Connection web: Red | 2. Host system: Servidor",
        "hi": "1. Connection web: Network | 2. Host system: Server",
        "tamil": "1. இணைய வலையமைப்பு (Connection web) / 2. சேவையகம் (Host system)",
        "shortcutEs": '1. Connection web: <strong>Red</strong> ≈ Originally a fisherman’s tangled <strong>"Net"</strong> (caught in a spider-web of wires) → Internet <em>Network (Red)</em>!<br>2. Host system: <strong>Servidor</strong> ≈ Direct match with <strong>"Server"</strong> (serves data)!',
        "shortcutHi": '1. Connection web: <strong>Network</strong> ≈ Mobile signal & Wi-Fi mesh!<br>2. Host system: <strong>Server</strong> ≈ Main cloud host computer (like <em>"Server down hai!"</em>)!',
    },
    1325: {
        "es": "Memoria / almacenamiento",
        "hi": "Memory / storage",
        "tamil": "நினைவகம் / சேமிப்பகம்",
        "shortcutEs": '<strong>Memoria</strong> ≈ Direct match with <strong>"Memory"</strong>! | <strong>Almacenamiento</strong> ≈ From <strong>Almacén ("Warehouse/Store")</strong> → Space holding files = <em>Storage</em>!',
        "shortcutHi": '<strong>Memory / storage</strong> ≈ Phone RAM (<em>Memory</em>) and GB disk space (<em>Storage</em> — <em>"Storage full ho gaya!"</em>)!',
    },
    1326: {
        "es": "Chip / procesador",
        "hi": "Chip / processor",
        "tamil": "மைக்ரோ சிப் / கணினி செயலி",
        "shortcutEs": '<strong>Chip</strong> ≈ 100% identical to <strong>"Silicon Chip"</strong>! | <strong>Procesador</strong> ≈ Direct match with <strong>"Processor"</strong>!',
        "shortcutHi": '<strong>Chip / processor</strong> ≈ Tiny silicon wafer brain inside every phone and PC!',
    },
    1327: {
        "es": "1. Wave transmission: Señal | 2. Space relay: Satélite",
        "hi": "1. Wave transmission: Signal | 2. Space relay: Satellite",
        "tamil": "1. சிக்னல் அலை (Wave transmission) / 2. செயற்கைக்கோள் (Space relay)",
        "shortcutEs": '1. Wave transmission: <strong>Señal</strong> ≈ Direct match with <strong>"Signal"</strong>!<br>2. Space relay: <strong>Satélite</strong> ≈ Direct match with <strong>"Satellite"</strong>!',
        "shortcutHi": '1. Wave transmission: <strong>Signal</strong> ≈ Tower bars on a phone!<br>2. Space relay: <strong>Satellite</strong> ≈ Solar-winged craft orbiting Earth for GPS & TV!',
    },
    1328: {
        "es": "Dispositivo / aparato",
        "hi": "Device / machine",
        "tamil": "மின்னணு கருவி",
        "shortcutEs": '<strong>Dispositivo</strong> ≈ Built/<strong>Disposed</strong> neatly to perform a task = Electronic <em>Device</em>! | <strong>Aparato</strong> ≈ Direct match with <strong>"Apparatus"</strong>!',
        "shortcutHi": '<strong>Device / machine</strong> ≈ Smartphone, tablet, gadget, or mechanical tool!',
    },
    1329: {
        "es": "1. Stock fabric/matter: Material | 2. Metallic element: Metal",
        "hi": "1. Stock fabric/matter: Saamaan / maal / material | 2. Metallic element: Metal",
        "tamil": "1. மூலப்பொருள் (Stock fabric/matter) / 2. உலோகம் (Metallic element)",
        "shortcutEs": '1. Stock fabric/matter: <strong>Material</strong> ≈ 100% identical to <strong>"Material"</strong>!<br>2. Metallic element: <strong>Metal</strong> ≈ 100% identical to <strong>"Metal"</strong>!',
        "shortcutHi": '1. Stock fabric/matter: <strong>Saamaan / maal</strong> ≈ Everyday workshop & Tamil <strong>சாமான் (Saamaan = Goods/Stuff!)</strong> = Raw stock/materials!<br>2. Metallic element: <strong>Metal</strong> ≈ Shiny hard ore like steel or iron!',
    },
    1330: {
        "es": "1. Iron: Hierro / fierro | 2. Steel alloy: Acero",
        "hi": "1. Iron: Loha | 2. Steel alloy: Steel",
        "tamil": "1. இரும்பு (Iron) / 2. எஃகு / ஸ்டீல் (Steel alloy)",
        "shortcutEs": '1. Iron: <strong>Hierro / fierro</strong> ≈ Direct root of <strong>"Ferrous / Ferric (Fe)"</strong> (chemical symbol Fe for <em>Iron</em>)!<br>2. Steel alloy: <strong>Acero</strong> ≈ Think sharp, razor-hard <strong>"Ace-Arrow"</strong> tip = Forged <em>Steel</em>!',
        "shortcutHi": '1. Iron: <strong>Loha</strong> ≈ Sounds like heavy <strong>"Low-Hard!"</strong> → Heavy dark bridge <em>Iron (Loha)</em> (<em>Loha manna</em> = Respect strength)!<br>2. Steel alloy: <strong>Steel</strong> ≈ Stainless kitchenware & beams!',
    },
    1331: {
        "es": "1. Copper: Cobre | 2. Bronze: Bronce | 3. Aluminum: Aluminio",
        "hi": "1. Copper: Taamba | 2. Bronze: Kaansa / bronze | 3. Aluminum: Aluminum",
        "tamil": "1. தாமிரம் / செம்பு (Copper) / 2. வெண்கலம் (Bronze) / 3. அலுமினியம் (Aluminum)",
        "shortcutEs": '1. Copper: <strong>Cobre</strong> ≈ Direct match with <strong>"Copper"</strong>!<br>2. Bronze: <strong>Bronce</strong> ≈ Direct match with <strong>"Bronze"</strong>!<br>3. Aluminum: <strong>Aluminio</strong> ≈ Direct match with <strong>"Aluminum"</strong>!',
        "shortcutHi": '1. Copper: <strong>Taamba</strong> ≈ <strong>Tamil தாமிரம் (Thaamiram!)</strong> → 100% same root! Traditional reddish water vessels = <em>Copper (Taamba)</em>!<br>2. Bronze: <strong>Kaansa</strong> ≈ <strong>Tamil வெண்கலம் / கஞ்சம் (Bronze thali/medals!)</strong>!<br>3. Aluminum: <strong>Aluminum</strong> ≈ Foil & lightweight utensils!',
    },
    1332: {
        "es": "1. Clay block: Ladrillo | 2. Powder bond: Cemento | 3. Aggregate concrete: Hormigón / concreto",
        "hi": "1. Clay block: Eent | 2. Powder bond: Cement | 3. Aggregate concrete: Concrete",
        "tamil": "1. செங்கல் (Clay block) / 2. சிமெண்ட் (Powder bond) / 3. கான்கிரீட் (Aggregate concrete)",
        "shortcutEs": '1. Clay block: <strong>Ladrillo</strong> ≈ Baked red wall blocks stacked on a <strong>"Ladder-row"</strong> = <em>Brick</em>!<br>2. Powder bond: <strong>Cemento</strong> ≈ <strong>"Cement"</strong>!<br>3. Aggregate concrete: <strong>Hormigón</strong> (Poured hard foundation) / <strong>Concreto</strong> (<strong>"Concrete"</strong>)!',
        "shortcutHi": '1. Clay block: <strong>Eent</strong> ≈ Classic construction word ("<em>Eent se eent bajana</em>" = Smash baked red clay <em>Bricks</em>)!<br>2. Powder bond: <strong>Cement</strong> ≈ Grey bag powder!<br>3. Aggregate concrete: <strong>Concrete</strong> ≈ Mixed gravel, sand, and cement!',
    },
    1333: {
        "es": "Arcilla / barro / cerámica",
        "hi": "Chikni mitti / ceramic",
        "tamil": "களிமண் / பீங்கான்",
        "shortcutEs": '<strong>Arcilla</strong> ≈ Smooth potter’s earth ("Art-Clay")! | <strong>Barro</strong> ≈ Wet spinning mud on a potter’s wheel! | <strong>Cerámica</strong> ≈ Direct match with <strong>"Ceramic"</strong>!',
        "shortcutHi": '<strong>Chikni mitti</strong> ≈ <strong>Chikni (Smooth/Slick) + Mitti (Earth/Soil)</strong> → Slippery wet clay shaped by hands into pots = <em>Clay (Chikni mitti)</em>! | <strong>Ceramic</strong> ≈ Glazed fired cups/tiles!',
    },
    1334: {
        "es": "1. Hard resin: Plástico | 2. Elastic latex: Goma / caucho",
        "hi": "1. Hard resin: Plastic | 2. Elastic latex: Rubber",
        "tamil": "1. பிளாஸ்டிக் (Hard resin) / 2. ரப்பர் (Elastic latex)",
        "shortcutEs": '1. Hard resin: <strong>Plástico</strong> ≈ Direct match with <strong>"Plastic"</strong>!<br>2. Elastic latex: <strong>Goma</strong> (Elastic <strong>"Gum"</strong>!) / <strong>Caucho</strong> (Raw rainforest <strong>Caoutchouc</strong> latex sap = <em>Rubber</em>)!',
        "shortcutHi": '1. Hard resin: <strong>Plastic</strong> ≈ Bottles, buckets, and molded caps!<br>2. Elastic latex: <strong>Rubber</strong> ≈ Bouncy black car tires and stretch bands!',
    },
    1335: {
        "es": "Cuero / piel",
        "hi": "Chamda",
        "tamil": "தோல் (லெதர்)",
        "shortcutEs": '<strong>Cuero</strong> ≈ Think tanned cow-hide ("Cow-ero") jacket! | <strong>Piel</strong> ≈ Direct sibling of <strong>"Pelt / Peel"</strong> (animal skin/leather)!',
        "shortcutHi": '<strong>Chamda</strong> ≈ <strong>Tamil சருமம் (Charumam = Skin/Hide!)</strong> → Same root → Tanned hide for wallets, belts, and shoes = <em>Leather (Chamda)</em>!',
    },
    1336: {
        "es": "Tela / tejido",
        "hi": "Kapda / fabric",
        "tamil": "துணி / நெசவுத் துணி",
        "shortcutEs": '<strong>Tela</strong> ≈ Root of <strong>"Textiles"</strong> ("Tailor cuts the <em>Tela</em>")! | <strong>Tejido</strong> ≈ Woven <strong>"Tissue/Texture"</strong> → Woven <em>Cloth / Fabric</em>!',
        "shortcutHi": '<strong>Kapda</strong> ≈ Think tailor’s <strong>"Cupboard-Cloth"</strong> → Every shirt, sari, and curtain bolt = <em>Cloth / Fabric (Kapda)</em>!',
    },
    1337: {
        "es": "1. Cotton: Algodón | 2. Wool: Lana | 3. Silk: Seda",
        "hi": "1. Cotton: Sooti / rui / cotton | 2. Wool: Oon | 3. Silk: Resham / silk",
        "tamil": "1. பருத்தி (Cotton) / 2. கம்பளி (Wool) / 3. பட்டு (Silk)",
        "shortcutEs": '1. Cotton: <strong>Algodón</strong> ≈ Soft white puffs ("All-Good-Down"!) = <em>Cotton</em>!<br>2. Wool: <strong>Lana</strong> ≈ Fluffy winter fleece (<strong>"Llama-wool"</strong>)!<br>3. Silk: <strong>Seda</strong> ≈ Shiny smooth <strong>"Satin / Silk"</strong> (sounds like "Say-Daa-silk"!)!',
        "shortcutHi": '1. Cotton: <strong>Sooti</strong> (woven <em>Soot</em>/thread — <strong>Tamil சூத்ரம்/பருத்தி</strong>) & <strong>Rui</strong> (fluffy raw cotton)!<br>2. Wool: <strong>Oon</strong> ≈ Cozy winter sweater yarn = <em>Wool (Oon)</em>!<br>3. Silk: <strong>Resham</strong> ≈ Classic glossy <em>Resham ki dori</em> = <em>Silk</em>!',
    },
    1338: {
        "es": "1. Art discipline: Arte | 2. Artwork piece: Obra de arte | 3. Tour de force: Obra maestra",
        "hi": "1. Art discipline: Kala / art | 2. Artwork piece: Kala / art | 3. Tour de force: Masterpiece / kamaal ki cheez",
        "tamil": "1. கலை (Art discipline) / 2. கலைப்படைப்பு (Artwork piece) / 3. தலைசிறந்த படைப்பு (Tour de force)",
        "shortcutEs": '1. Art discipline: <strong>Arte</strong> ≈ <strong>"Art"</strong>!<br>2. Artwork piece: <strong>Obra de arte</strong> ≈ <strong>"Work (Opus) of Art"</strong>!<br>3. Tour de force: <strong>Obra maestra</strong> ≈ <strong>"Master Work"</strong> (like the Mona Lisa) = <em>Masterpiece</em>!',
        "shortcutHi": '1. Art discipline: <strong>Kala</strong> ≈ 100% identical to <strong>Tamil கலை (Kalai = Art!)</strong>!<br>2. Artwork piece: <strong>Kala / art</strong> ≈ Framed painting or craft!<br>3. Tour de force: <strong>Kamaal ki cheez</strong> ≈ <strong>Kamaal (Wonder/Marvel) + Ki cheez (Thing)</strong> = Genius <em>Masterpiece</em>!',
    },
    1339: {
        "es": "1. Outline drawing: Boceto / dibujo | 2. Face likeness: Retrato",
        "hi": "1. Outline drawing: Sketch | 2. Face likeness: Tasveer / portrait",
        "tamil": "1. பென்சில் ஓவியம் (Outline drawing) / 2. முக உருவப்படம் (Face likeness)",
        "shortcutEs": '1. Outline drawing: <strong>Boceto</strong> ≈ Rough charcoal outline ("Box-it-out") = <em>Sketch</em>! | <strong>Dibujo</strong> ≈ Artist’s pencil drawing!<br>2. Face likeness: <strong>Retrato</strong> ≈ Direct match with <strong>"Portrait"</strong> (P-o-r-t-r-a-i-t → Retrato)!',
        "shortcutHi": '1. Outline drawing: <strong>Sketch</strong> ≈ Quick pencil outline before painting!<br>2. Face likeness: <strong>Tasveer</strong> ≈ Classic Hindi word for a framed face photo or painted likeness = <em>Portrait / Picture (Tasveer)</em>!',
    },
    1340: {
        "es": "1. Statue effigy: Estatua / escultura | 2. Historic site: Monumento",
        "hi": "1. Statue effigy: Moorti / statue | 2. Historic site: Itihaasik imaarat / monument",
        "tamil": "1. சிற்பம் / சிலை (Statue effigy) / 2. நினைவுச்சின்னம் (Historic site)",
        "shortcutEs": '1. Statue effigy: <strong>Estatua</strong> (<strong>"Statue"</strong>!) / <strong>Escultura</strong> (<strong>"Sculpture"</strong>!)!<br>2. Historic site: <strong>Monumento</strong> ≈ Direct match with <strong>"Monument"</strong>!',
        "shortcutHi": '1. Statue effigy: <strong>Moorti</strong> ≈ <strong>Tamil மூர்த்தி (Moorthi = Carved Idol / Statue!)</strong> → 100% same word!<br>2. Historic site: <strong>Itihaasik imaarat</strong> ≈ <strong>Itihaasik (Tamil இதிகாச = Historical!)</strong> + <strong>Imaarat (Building)</strong> = Taj-like historic <em>Monument</em>!',
    },
    1341: {
        "es": "1. Hall: Galería | 2. Showing event: Exposición / muestra",
        "hi": "1. Hall: Gallery | 2. Showing event: Exhibition",
        "tamil": "1. கலைக்கூடம் (Hall) / 2. கண்காட்சி (Showing event)",
        "shortcutEs": '1. Hall: <strong>Galería</strong> ≈ Direct match with <strong>"Gallery"</strong> (white-wall art hall)!<br>2. Showing event: <strong>Exposición</strong> (<strong>"Exposition"</strong>) / <strong>Muestra</strong> ("Show/Display") = Art <em>Exhibition</em>!',
        "shortcutHi": '1. Hall: <strong>Gallery</strong> ≈ Museum hallway lined with framed paintings!<br>2. Showing event: <strong>Exhibition</strong> ≈ Public art & museum showcase event!',
    },
    1342: {
        "es": "1. Platform: Escenario / tablas | 2. Playhouse building: Teatro | 3. Theatrical play: Obra de teatro / drama",
        "hi": "1. Platform: Stage | 2. Playhouse building: Theatre | 3. Theatrical play: Naatak / drama",
        "tamil": "1. நாடக மேடை (Platform) / 2. நாடக அரங்கம் (Playhouse building) / 3. மேடை நாடகம் (Theatrical play)",
        "shortcutEs": '1. Platform: <strong>Escenario</strong> (<strong>"Scenery/Stage"</strong>) / <strong>Tablas</strong> (literally wooden <strong>"Tables/Planks"</strong> actors walk on)!<br>2. Playhouse building: <strong>Teatro</strong> (<strong>"Theater"</strong>)!<br>3. Theatrical play: <strong>Obra de teatro / drama</strong> = <em>Stage Play / Drama</em>!',
        "shortcutHi": '1. Platform: <strong>Stage</strong> ≈ Spotlight wooden floor!<br>2. Playhouse building: <strong>Theatre</strong> ≈ Velvet-seat playhouse!<br>3. Theatrical play: <strong>Naatak</strong> ≈ <strong>Tamil நாடகம் (Naadagam = Drama / Play!)</strong> — 100% same word ("<em>Naatak mat karo!</em>" = Stop acting!)!',
    },
    1343: {
        "es": "1. Humorous: Comedia | 2. Sorrowful: Tragedia",
        "hi": "1. Humorous: Comedy / hasi-mazaak | 2. Sorrowful: Tragedy / haadsa",
        "tamil": "1. நகைச்சுவை (Humorous) / 2. துயர நாடகம் / சோகம் (Sorrowful)",
        "shortcutEs": '1. Humorous: <strong>Comedia</strong> ≈ Direct match with <strong>"Comedy"</strong> (laughing theater mask)!<br>2. Sorrowful: <strong>Tragedia</strong> ≈ Direct match with <strong>"Tragedy"</strong> (weeping mask)!',
        "shortcutHi": '1. Humorous: <strong>Hasi-mazaak</strong> ≈ <strong>Hasi (Laughter) + Mazaak (Joke)</strong> = Fun & <em>Comedy</em>!<br>2. Sorrowful: <strong>Haadsa</strong> ≈ Heartbreaking accident or calamity = Real-life <em>Tragedy (Haadsa)</em>!',
    },
    1344: {
        "es": "1. Live show: Actuación / función | 2. Practice run: Ensayo",
        "hi": "1. Live show: Performance | 2. Practice run: Rehearsal / practice",
        "tamil": "1. மேடை நிகழ்ச்சி (Live show) / 2. ஒத்திகை (Practice run)",
        "shortcutEs": '1. Live show: <strong>Actuación</strong> (<strong>"Acting"</strong>) / <strong>Función</strong> ("Live Show <strong>Function</strong>")!<br>2. Practice run: <strong>Ensayo</strong> ≈ Same root as <strong>"Assay / Trial run"</strong> → Testing every line before opening night = <em>Rehearsal</em>!',
        "shortcutHi": '1. Live show: <strong>Performance</strong> ≈ Live concert or stage recital in front of fans!<br>2. Practice run: <strong>Rehearsal / practice</strong> ≈ Pre-show backstage dry run!',
    },
    1345: {
        "es": "1. View cut: Escena | 2. Screenplay text: Guión",
        "hi": "1. View cut: Scene | 2. Screenplay text: Script",
        "tamil": "1. திரைப்படக் காட்சி (View cut) / 2. திரைக்கதை (Screenplay text)",
        "shortcutEs": '1. View cut: <strong>Escena</strong> ≈ Direct match with <strong>"Scene"</strong> (Es- + cena → clapboard movie cut)!<br>2. Screenplay text: <strong>Guión</strong> ≈ Film <strong>"Guide"</strong> page telling actors what to say = <em>Script</em>!',
        "shortcutHi": '1. View cut: <strong>Scene</strong> ≈ Film shoot marked on a director’s clapperboard!<br>2. Screenplay text: <strong>Script</strong> ≈ Printed dialogue booklet actors memorize!',
    },
    1346: {
        "es": "1. Acoustic art: Música | 2. Track: Canción / tema",
        "hi": "1. Acoustic art: Music / sangeet | 2. Track: Gaana / geet",
        "tamil": "1. இசை (Acoustic art) / 2. பாடல் (Track)",
        "shortcutEs": '1. Acoustic art: <strong>Música</strong> ≈ Direct match with <strong>"Music"</strong>!<br>2. Track: <strong>Canción</strong> (Root of <strong>"Chant"</strong>!) / <strong>Tema</strong> (Musical <strong>"Theme"</strong>!) = <em>Song</em>!',
        "shortcutHi": '1. Acoustic art: <strong>Sangeet</strong> ≈ <strong>Tamil சங்கீதம் (Sangeetham = Classical Music!)</strong> — 100% identical!<br>2. Track: <strong>Gaana</strong> (<strong>Tamil கானம்</strong> = Melody song!) & <strong>Geet</strong> (<strong>Tamil கீதம்</strong> = Song/Hymn!)!',
    },
    1347: {
        "es": "1. Melodic line: Melodía | 2. Cadence beat: Ritmo / compás",
        "hi": "1. Melodic line: Sur / dhun | 2. Cadence beat: Rhythm / taal",
        "tamil": "1. இனிய ராகம் / மெட்டு (Melodic line) / 2. தாளம் / லயம் (Cadence beat)",
        "shortcutEs": '1. Melodic line: <strong>Melodía</strong> ≈ Direct match with <strong>"Melody / Tune"</strong>!<br>2. Cadence beat: <strong>Ritmo</strong> (<strong>"Rhythm"</strong>!) / <strong>Compás</strong> (Beat count keeping time like a musical compass)!',
        "shortcutHi": '1. Melodic line: <strong>Sur</strong> (<strong>Tamil சுரம் / ஸ்வரம் = Musical Note!</strong>) & <strong>Dhun</strong> ("Catchy <strong>Tune</strong> humming in your head")!<br>2. Cadence beat: <strong>Taal</strong> ≈ <strong>Tamil தாளம் (Thaalam = Tabla/Beat Cycle!)</strong> — 100% identical!',
    },
    1348: {
        "es": "Letra (de la canción)",
        "hi": "Lyrics / gaane ke bol",
        "tamil": "பாடல் வரிகள்",
        "shortcutEs": '<strong>Letra (de la canción)</strong> ≈ Literally the <strong>"Letters / Words of the song"</strong> printed on music sheets = <em>Lyrics</em>!',
        "shortcutHi": '<strong>Gaane ke bol</strong> ≈ <strong>Gaane (Song’s) + Bol (Spoken words — "Bolo!")</strong> = Words sung in a song = <em>Lyrics</em>! | <strong>Lyrics</strong> ≈ Written song lines!',
    },
    1349: {
        "es": "1. Music: Instrumento musical | 2. Tool/measuring device: Instrumento / aparato",
        "hi": "1. Music: Instrument | 2. Tool/measuring device: Auzaar / tool",
        "tamil": "1. இசைக்கருவி (Music) / 2. தொழில்நுட்பக் கருவி (Tool/measuring device)",
        "shortcutEs": '1. Music: <strong>Instrumento musical</strong> ≈ Direct match with <strong>"Musical Instrument"</strong>!<br>2. Tool/measuring device: <strong>Instrumento / aparato</strong> ≈ Direct match with <strong>"Instrument / Apparatus"</strong>!',
        "shortcutHi": '1. Music: <strong>Instrument</strong> ≈ Sitar, violin, or flute played by musicians!<br>2. Tool/measuring device: <strong>Auzaar</strong> ≈ Mechanic’s or surgeon’s precision steel implement = <em>Tool / Instrument</em>!',
    },
    1350: {
        "es": "Guitarra / piano / violín",
        "hi": "Guitar / piano / violin",
        "tamil": "கிடார் / பியானோ / வயலின்",
        "shortcutEs": '<strong>Guitarra / piano / violín</strong> ≈ Almost 100% identical spelling & sound to <strong>"Guitar / Piano / Violin"</strong>!',
        "shortcutHi": '<strong>Guitar / piano / violin</strong> ≈ All three acoustic string and key instruments are called by the exact same names across Hindi & Tamil!',
    },
    1351: {
        "es": "1. Percussion: Tambor / batería | 2. Flute pipe: Flauta",
        "hi": "1. Percussion: Dholak / drum | 2. Flute pipe: Baansuri",
        "tamil": "1. மேளம் / டிரம் (Percussion) / 2. புல்லாங்குழல் (Flute pipe)",
        "shortcutEs": '1. Percussion: <strong>Tambor</strong> ≈ Sibling of <strong>"Tambourine"</strong>! | <strong>Batería</strong> (Drum <strong>"Battery"</strong> kit)!<br>2. Flute pipe: <strong>Flauta</strong> ≈ Direct match with <strong>"Flute"</strong>!',
        "shortcutHi": '1. Percussion: <strong>Dholak / drum</strong> ≈ Iconic Indian two-headed wedding hand-drum (<em>Dhol / Dholak</em>) & Western <em>Drum</em>!<br>2. Flute pipe: <strong>Baansuri</strong> ≈ Made from <strong>Baans (Bamboo!)</strong> → Bamboo wind pipe = <em>Flute</em>!',
    },
    1352: {
        "es": "1. Live recital: Concierto | 2. Music group: Banda / orquesta",
        "hi": "1. Live recital: Concert | 2. Music group: Band / orchestra",
        "tamil": "1. இசைக் கச்சேரி (Live recital) / 2. இசைக்குழு (Music group)",
        "shortcutEs": '1. Live recital: <strong>Concierto</strong> ≈ Direct match with <strong>"Concert"</strong>!<br>2. Music group: <strong>Banda</strong> (<strong>"Band"</strong>) / <strong>Orquesta</strong> (<strong>"Orchestra"</strong>)!',
        "shortcutHi": '1. Live recital: <strong>Concert</strong> ≈ Live ticketed arena/stage musical show!<br>2. Music group: <strong>Band / orchestra</strong> ≈ Group of singers and instrumentalists playing together!',
    },
    1353: {
        "es": "1. Game contest: Deporte | 2. Player: Atleta / deportista",
        "hi": "1. Game contest: Khel / sport | 2. Player: Khilaadi / athlete",
        "tamil": "1. விளையாட்டு (Game contest) / 2. விளையாட்டு வீரர் (Player)",
        "shortcutEs": '1. Game contest: <strong>Deporte</strong> ≈ Sounds like <strong>"Dis-port / Sport"</strong> (athletic activity)!<br>2. Player: <strong>Atleta</strong> (<strong>"Athlete"</strong>!) / <strong>Deportista</strong> (One who plays <em>Deporte</em>)!',
        "shortcutHi": '1. Game contest: <strong>Khel</strong> ≈ Active physical play & fun (<em>Khelna</em> = To play) = <em>Sport</em>!<br>2. Player: <strong>Khilaadi</strong> ≈ Famous Bollywood word ("<em>Khiladi</em>" = Master Player / Competing <em>Athlete</em>)!',
    },
    1354: {
        "es": "Estadio",
        "hi": "Stadium / maidaan",
        "tamil": "விளையாட்டு அரங்கம் (ஸ்டேடியம்)",
        "shortcutEs": '<strong>Estadio</strong> ≈ Direct match with English <strong>"Stadium"</strong> (mega tiered sports arena)!',
        "shortcutHi": '<strong>Stadium / maidaan</strong> ≈ Massive roaring cricket bowl (<em>Stadium</em>) or open grassy sports field (<em>Maidaan</em> = <strong>Tamil மைதானம்</strong>)!',
    },
    1355: {
        "es": "Fútbol / críquet / tenis",
        "hi": "Football / cricket / tennis",
        "tamil": "கால்பந்து / கிரிக்கெட் / டென்னிஸ்",
        "shortcutEs": '<strong>Fútbol / críquet / tenis</strong> ≈ Phonetic Spanish spellings directly mirroring <strong>"Football / Cricket / Tennis"</strong>!',
        "shortcutHi": '<strong>Football / cricket / tennis</strong> ≈ World’s top three ball games — used identically across everyday Hindi & Tamil!',
    },
    1356: {
        "es": "Carrera / maratón",
        "hi": "Race / daud / marathon",
        "tamil": "ஓட்டப்பந்தயம் / மாரத்தான்",
        "shortcutEs": '<strong>Carrera</strong> ≈ Sibling of <strong>"Career / Racing Track"</strong> (fast sprint to the finish line)! | <strong>Maratón</strong> ≈ Direct match with <strong>"Marathon"</strong>!',
        "shortcutHi": '<strong>Daud</strong> ≈ Fast sprinting footsteps (<em>"Daud lagao!"</em> = Run fast!) = Track <em>Race</em>! | <strong>Race / marathon</strong> ≈ Competitive running distance!',
    },
    1357: {
        "es": "1. Trail walk: Senderismo / caminata | 2. Tent sleep: Acampar / campamento",
        "hi": "1. Trail walk: Hiking / pahaadi safar | 2. Tent sleep: Camping / dera daalna",
        "tamil": "1. மலை நடைப்பயணம் (Trail walk) / 2. முகாமிடுதல் (Tent sleep)",
        "shortcutEs": '1. Trail walk: <strong>Senderismo</strong> (Hiking on a <em>Sendero</em> trail) / <strong>Caminata</strong> (From <strong>Caminar = Walk</strong>)!<br>2. Tent sleep: <strong>Acampar / campamento</strong> ≈ <strong>"Camp / Encampment"</strong>!',
        "shortcutHi": '1. Trail walk: <strong>Pahaadi safar</strong> ≈ <strong>Pahaadi (Mountain) + Safar (Journey/Trek)</strong> = Mountain trek = <em>Hiking</em>!<br>2. Tent sleep: <strong>Dera daalna</strong> ≈ Pitching a canvas tent camp ("Dropping camp"!) = <em>Camping</em>!',
    },
    1358: {
        "es": "1. Play activity: Juego | 2. Head-to-head match: Partido / encuentro | 3. Series championship: Torneo / campeonato",
        "hi": "1. Play activity: Khel / game | 2. Head-to-head match: Match / muqabla | 3. Series championship: Tournament",
        "tamil": "1. விளையாட்டு (Play activity) / 2. நேரடிப் போட்டி (Head-to-head match) / 3. தொடர் சாம்பியன்ஷிப் (Series championship)",
        "shortcutEs": '1. Play activity: <strong>Juego</strong> ≈ Sibling of <strong>"Jocular / Joke / Game"</strong>!<br>2. Head-to-head match: <strong>Partido</strong> (Split 2-team contest) / <strong>Encuentro</strong> (<strong>"Encounter"</strong>)!<br>3. Series championship: <strong>Torneo</strong> (<strong>"Tournament"</strong>!) / <strong>Campeonato</strong> (<strong>"Championship"</strong>)!',
        "shortcutHi": '1. Play activity: <strong>Khel / game</strong> ≈ Fun board, video, or field play!<br>2. Head-to-head match: <strong>Muqabla</strong> ≈ Famous word ("<em>Muqabla!</em>" = Face-off showdown between two rivals) = <em>Match</em>!<br>3. Series championship: <strong>Tournament</strong> ≈ Multi-round cup series!',
    },
    1359: {
        "es": "1. Cup goblet: Trofeo / copa | 2. Medallion disc: Medalla",
        "hi": "1. Cup goblet: Trophy / cup | 2. Medallion disc: Medal",
        "tamil": "1. வெற்றிக் கோப்பை (Cup goblet) / 2. பதக்கம் (Medallion disc)",
        "shortcutEs": '1. Cup goblet: <strong>Trofeo</strong> (<strong>"Trophy"</strong>!) / <strong>Copa</strong> (<strong>"Cup"</strong> goblet)!<br>2. Medallion disc: <strong>Medalla</strong> ≈ Direct match with <strong>"Medal"</strong>!',
        "shortcutHi": '1. Cup goblet: <strong>Trophy / cup</strong> ≈ Gleaming golden winner’s World Cup!<br>2. Medallion disc: <strong>Medal</strong> ≈ Gold/silver/bronze ribbon worn around the neck!',
    },
    1360: {
        "es": "Campeón / campeona / ganador",
        "hi": "Champion / jeetne wala",
        "tamil": "சாம்பியன் / வெற்றியாளர்",
        "shortcutEs": '<strong>Campeón / campeona</strong> ≈ Direct match with <strong>"Champion"</strong>! | <strong>Ganador</strong> ≈ From <strong>Ganar (To "Gain" victory)</strong> = <em>Winner</em>!',
        "shortcutHi": '<strong>Jeetne wala</strong> ≈ <strong>Jeet (Victory — Tamil ஜெயம்!) + Wala (-er)</strong> = The victorious one = <em>Winner (Jeetne wala)</em>! | <strong>Champion</strong> ≈ #1 title holder!',
    },
    1361: {
        "es": "1. Team mentor trainer: Entrenador / entrenadora | 2. Umpire official: Árbitro",
        "hi": "1. Team mentor trainer: Coach / trainer | 2. Umpire official: Referee / umpire",
        "tamil": "1. விளையாட்டுப் பயிற்சியாளர் (Team mentor trainer) / 2. போட்டி நடுவர் (Umpire official)",
        "shortcutEs": '1. Team mentor trainer: <strong>Entrenador / entrenadora</strong> ≈ Direct match with <strong>"Trainer"</strong> (En- + Train-ador)!<br>2. Umpire official: <strong>Árbitro</strong> ≈ Direct sibling of <strong>"Arbitrator"</strong> (whistle-blowing rules judge) = <em>Referee</em>!',
        "shortcutHi": '1. Team mentor trainer: <strong>Coach / trainer</strong> ≈ Sideline strategist guiding athletes!<br>2. Umpire official: <strong>Referee / umpire</strong> ≈ Whistle-blowing or boundary-calling match official!',
    },
    1362: {
        "es": "Ejercicio / entrenamiento / condición física",
        "hi": "Exercise / kasrat / fitness",
        "tamil": "உடற்பயிற்சி / உடல் தகுதி",
        "shortcutEs": '<strong>Ejercicio</strong> ≈ Direct match with <strong>"Exercise"</strong>! | <strong>Entrenamiento</strong> ≈ <strong>"Training"</strong> workout! | <strong>Condición física</strong> ≈ Literally <strong>"Physical Condition"</strong> = <em>Fitness</em>!',
        "shortcutHi": '<strong>Kasrat</strong> ≈ Classic akhada / gym word for vigorous sweat-breaking push-ups & physical workout (<em>"Roz kasrat karo!"</em> = Do daily <em>Exercise</em>!) | <strong>Exercise / fitness</strong> ≈ Healthy workout routine!',
    },
}


def main():
    assert len(SPLIT7_UPDATES) == 100, f"Expected 100 entries, got {len(SPLIT7_UPDATES)}"
    for n in range(1263, 1363):
        assert n in SPLIT7_UPDATES, f"Missing card #{n}"

    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        lines = f.read().splitlines(True)

    # Locate var cardShortcuts = ... and var split7DeckCards = ...
    sc_idx = next(i for i, l in enumerate(lines) if l.startswith("var cardShortcuts = "))
    s7_idx = next(i for i, l in enumerate(lines) if l.startswith("var split7DeckCards = "))

    card_shortcuts = json.loads(lines[sc_idx][len("var cardShortcuts = "):].rstrip().rstrip(";"))
    split7 = json.loads(lines[s7_idx][len("var split7DeckCards = "):].rstrip().rstrip(";"))

    assert len(split7) == 100, f"Expected 100 cards in split7DeckCards, got {len(split7)}"

    updated_by_num = {}
    for c in split7:
        num = c["num"]
        upd = SPLIT7_UPDATES[num]
        c["trans"]["es"] = upd["es"]
        c["trans"]["hi"] = upd["hi"]
        c["hiDevanagari"] = upd["hi"]
        c["tamil"] = upd["tamil"]
        c["shortcutEs"] = upd["shortcutEs"]
        c["shortcutHi"] = upd["shortcutHi"]
        if num in IMAGE_UPGRADES:
            c["imageUrl"] = IMAGE_UPGRADES[num]
            c["gifUrl"] = IMAGE_UPGRADES[num]
        card_shortcuts[str(num)] = {
            "es": upd["shortcutEs"],
            "hi": upd["shortcutHi"],
        }
        updated_by_num[num] = c

    lines[sc_idx] = "var cardShortcuts = " + json.dumps(card_shortcuts, ensure_ascii=False) + ";\n"
    lines[s7_idx] = "var split7DeckCards = " + json.dumps(split7, ensure_ascii=False) + ";\n"

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.writelines(lines)

    # Sync data/backup_original_cards.json
    if os.path.exists(BACKUP_PATH):
        with open(BACKUP_PATH, "r", encoding="utf-8") as f:
            bkp = json.load(f)
        if isinstance(bkp, dict):
            for k, val in bkp.items():
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
        elif isinstance(bkp, list):
            for val in bkp:
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

    print(f"Successfully updated all {len(updated_by_num)} Split 7 cards (#1263-#1362), cardShortcuts, and backup_original_cards.json!")


if __name__ == "__main__":
    main()
