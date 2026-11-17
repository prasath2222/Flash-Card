# Deep atomic word-by-word mnemonics for Split 7 (#1263 - #1362)

DATA_S7 = {
    1263: (
        '<strong>Noticias</strong> (From <strong>Notus</strong> Known [root of <em>Notice</em>] = Newly made-known updates!) | '
        '<strong>Prensa</strong> (Latin <strong>Premere</strong> Press [as in <em>Printing Press</em>]!) | '
        '<strong>Medios</strong> (Latin <strong>Medius</strong> Middle channel carrying messages = <em>Media</em>!) = <em>News / Media / Press</em>!',
        '<strong>Khabrein</strong> (Arabic <strong>Khabar [Spoken Tamil கபர் = Word/Report!]</strong> + <strong>-ein</strong> Plural!) / '
        '<strong>News</strong> (From <strong>New</strong> Fresh events + <strong>-s</strong>!) / '
        '<strong>Media</strong> (Latin <strong>Medius</strong> Middle channel conveying info!) = <em>News / Media</em>!'
    ),
    1264: (
        '<strong>Emitir</strong> (<strong>E-</strong> Out + <strong>Mittere</strong> Send [root of <em>Emit</em>] = Send out signals!) | '
        '<strong>Transmitir</strong> (<strong>Trans-</strong> Across + <strong>Mittere</strong> Send [<em>Transmit</em>]!) = <em>Broadcast</em>!',
        '<strong>Live dikhana</strong> (<strong>Live</strong> Real-time active + <strong>Dikhana</strong> Cause to see [from <strong>Dekhna</strong> Look]!) / '
        '<strong>Broadcast</strong> (<strong>Broad</strong> Wide across + <strong>Cast</strong> Scatter/Throw signals far!) = <em>Broadcast</em>!'
    ),
    1265: (
        '1. Banner title: <strong>Titular</strong> (<strong>Título</strong> Title + <strong>-ar</strong> Banner!) | '
        '<strong>Encabezado</strong> (<strong>En-</strong> At + <strong>Cabeza</strong> Head [<em>Capital</em>] = Top header!) = <em>Headline</em>!<br>'
        '2. Written story: <strong>Artículo</strong> (Latin <em>Articulus</em> Distinct joined section/clause [<em>Article</em>]!) = <em>Article</em>!',
        '1. Banner title: <strong>Headline</strong> (<strong>Head</strong> Top + <strong>Line</strong> Row!) / '
        '<strong>Mukhya khabar</strong> (<strong>Mukhya [Tamil முக்கிய = Main!]</strong> + <strong>Khabar</strong> News!) = <em>Headline</em>!<br>'
        '2. Written story: <strong>Article</strong> (Latin <em>Articulus</em> Distinct section!) / '
        '<strong>Lekh</strong> (Sanskrit <strong>Lekha = Drawn/Written lines [Tamil இலக்கியம்]</strong>!) = <em>Article</em>!'
    ),
    1266: (
        '1. Informant reference: <strong>Fuente</strong> (Latin <em>Fons / Fontis</em> Flowing spring [<em>Fountain / Font</em>] = Origin!) = <em>Source</em>!<br>'
        '2. Unauthorized secret reveal: <strong>Filtración / filtrar</strong> (Latin <em>Filtrum</em> Strainer — secrets seeping through a <em>Filter</em>!) = <em>Leak</em>!',
        '1. Informant reference: <strong>Source</strong> (Latin <em>Surgere</em> Rise up — spring where story rises!) / '
        '<strong>Zariya</strong> (Arabic <strong>Dhari\'ah</strong> Reaching channel/medium!) = <em>Source</em>!<br>'
        '2. Unauthorized secret reveal: <strong>Khabar leak hona</strong> (<strong>Khabar</strong> News + <strong>Leak</strong> Drip out + <strong>Hona</strong>!) / '
        '<strong>Parda khulna</strong> (<strong>Parda</strong> Curtain + <strong>Khulna</strong> Open!) = <em>Leak</em>!'
    ),
    1267: (
        '1. Daily news sheet: <strong>Periódico</strong> (Greek <strong>Peri-</strong> Around + <strong>Hodos</strong> Path = Cyclical paper!) | '
        '<strong>Diario</strong> (From <strong>Día</strong> Day = Daily issue!) = <em>Newspaper</em>!<br>'
        '2. Periodical: <strong>Revista</strong> (<strong>Re-</strong> Again + <strong>Vista</strong> View [<em>Review</em>] = Monthly visual issue!) = <em>Magazine</em>!',
        '1. Daily news sheet: <strong>Akhbar</strong> (Arabic plural of <strong>Khabar [Tamil கபர் = News!]</strong> = Collected news sheets!) = <em>Newspaper</em>!<br>'
        '2. Periodical: <strong>Magazine</strong> (Arabic <strong>Makhazin</strong> Storehouse — storehouse of stories!) = <em>Magazine</em>!'
    ),
    1268: (
        '1. Biased influence: <strong>Propaganda</strong> (<strong>Pro-</strong> Forward + <strong>Pagare</strong> Fasten/Plant = Planting ideas [<em>Propagate</em>]!) = <em>Propaganda</em>!<br>'
        '2. Official redaction: <strong>Censura</strong> (Latin <em>Censere</em> Judge/Cut out [<em>Censor</em>]!) = <em>Censorship</em>!',
        '1. Biased influence: <strong>Propaganda</strong> (Latin <em>Propagare</em> Multiply/Plant spin!) / '
        '<strong>Prachaar</strong> (<strong>Pra-</strong> Forth + <strong>Chaar</strong> Spread/Move [<strong>Tamil பிரச்சாரம் Prachaaram!</strong>]!) = <em>Propaganda</em>!<br>'
        '2. Official redaction: <strong>Censorship</strong> (Latin <em>Censor</em> Assessor + <strong>-ship</strong>!) / '
        '<strong>Pabandi</strong> (<strong>Paa</strong> Foot + <strong>Band</strong> Tie [<strong>Tamil பந்த் Closed!</strong>] = Ban/Restriction!) = <em>Censorship</em>!'
    ),
    1269: (
        '1. Gossip: <strong>Rumor</strong> (Latin <em>Rumor</em> Murmured buzz/noise!) | '
        '<strong>Cotilleo</strong> (<strong>Cotilla</strong> Corset-lace chat — whispering chitchat!) = <em>Rumor</em>!<br>'
        '2. Exposure: <strong>Escándalo</strong> (Greek <em>Skandalon</em> Stumbling trap [<em>Scandal</em>]!) = <em>Scandal</em>!',
        '1. Gossip: <strong>Afwah</strong> (Arabic plural of <strong>Fauh</strong> Mouth — flying from mouth to mouth!) = <em>Rumor</em>!<br>'
        '2. Exposure: <strong>Scandal</strong> (Greek <em>Skandalon</em> Trap causing public fall!) / '
        '<strong>Badnaami</strong> (<strong>Bad</strong> Bad + <strong>Naam</strong> Name [<strong>Tamil நாமம்!</strong>] = Ill-fame!) = <em>Scandal</em>!'
    ),
    1270: (
        '<strong>Declaración</strong> (<strong>De-</strong> Out + <strong>Clarus</strong> Clear [<em>Declare</em>] = Make plain!) | '
        '<strong>Comunicado</strong> (<strong>Com-</strong> Common + <strong>Unus</strong> One = Shared bulletin [<em>Communiqué</em>]!) = <em>Statement / Release</em>!',
        '<strong>Bayaan</strong> (Arabic <strong>Bayan</strong> Making clear/Unfolding truth!) / '
        '<strong>Press release</strong> (<strong>Press</strong> News printers + <strong>Re-</strong> Back + <strong>Lease</strong> Let go = Issued notice!) = <em>Statement / Release</em>!'
    ),
    1271: (
        '1. Gathered crowd: <strong>Público</strong> (<strong>Populus</strong> People!) | '
        '<strong>Audiencia</strong> (Latin <strong>Audire</strong> Hear [<em>Audio</em>] = Listeners!) = <em>Audience</em>!<br>'
        '2. Screen watcher: <strong>Espectador</strong> (<strong>Spectare</strong> Watch [<em>Spectator</em>]!) | '
        '<strong>Televidente</strong> (<strong>Tele-</strong> Far + <strong>Videre</strong> See!) = <em>Viewer</em>!<br>'
        '3. Audio hearer: <strong>Oyente</strong> (From <strong>Oír</strong> Hear [<em>Audire</em>]!) = <em>Listener</em>!',
        '1. Gathered crowd: <strong>Audience</strong> (Latin <strong>Audire</strong> Hear!) / '
        '<strong>Log</strong> (Sanskrit <strong>Loka [Tamil உலகம் Ulagam = World/People!]</strong>!) = <em>Audience</em>!<br>'
        '2. Screen watcher: <strong>Dekhne wala</strong> (<strong>Dekhna</strong> Watch + <strong>Wala</strong> One!) / '
        '<strong>Viewer</strong> (<strong>View</strong> Look + <strong>-er</strong>!) = <em>Viewer</em>!<br>'
        '3. Audio hearer: <strong>Sunne wala</strong> (<strong>Sunna</strong> Hear + <strong>Wala</strong> One!) / '
        '<strong>Listener</strong> (<strong>Listen</strong> + <strong>-er</strong>!) = <em>Listener</em>!'
    ),
    1272: (
        '1. Learning: <strong>Educación</strong> (<strong>E-</strong> Out + <strong>Ducere</strong> Lead [draw out talent!]) | '
        '<strong>Formación</strong> (<strong>Forma</strong> Shape/Mold — shaping skill!) = <em>Education</em>!<br>'
        '2. Scholastic adj: <strong>Académico / académica</strong> (Plato’s Athens grove <em>Akademeia</em>!) = <em>Academic</em>!',
        '1. Learning: <strong>Padhai-likhai</strong> (<strong>Padhna</strong> Read + <strong>Likhna</strong> Write!) / '
        '<strong>Education</strong> (<strong>E-</strong> Out + <strong>Ducere</strong> Lead mind forward!) = <em>Education</em>!<br>'
        '2. Scholastic adj: <strong>Padhai se juda</strong> (<strong>Padhai</strong> Study + <strong>Juda</strong> Connected!) / '
        '<strong>Academic</strong> (Greek <em>Akademeia</em> — scholarly Plato grove!) = <em>Academic</em>!'
    ),
    1273: (
        '1. Learner: <strong>Estudiante</strong> (<strong>Estudiar</strong> Study [<em>Student</em>]!) | '
        '<strong>Alumno / alumna</strong> (Latin <em>Alere</em> Nourish/Raise = Mentally nourished pupil [<em>Alumni</em>]!) = <em>Student / Pupil</em>!<br>'
        '2. Class peer: <strong>Compañero de clase</strong> (<strong>Com-</strong> With + <strong>Panis</strong> Bread + <strong>Clase</strong> Class!) = <em>Classmate</em>!',
        '1. Learner: <strong>Student</strong> (Latin <em>Studere</em> Be eager/Strive!) / '
        '<strong>Padhne wala</strong> (<strong>Padhna</strong> Read/Study + <strong>Wala</strong> One!) = <em>Student / Pupil</em>!<br>'
        '2. Class peer: <strong>Classmate</strong> (<strong>Class</strong> + <strong>Mate</strong> Sharer!) / '
        '<strong>Saath padhne wala</strong> (<strong>Saath</strong> Together + <strong>Padhne wala</strong> Studying one!) = <em>Classmate</em>!'
    ),
    1274: (
        '<strong>Profesor / profesora</strong> (<strong>Pro-</strong> Forth + <strong>Fateri</strong> Speak openly [<em>Profess</em>]!) | '
        '<strong>Maestro / maestra</strong> (Latin <strong>Magister</strong> Master/Chief teacher!) = <em>Teacher / Professor</em>!',
        '<strong>Teacher</strong> (<strong>Teach</strong> Show/Guide + <strong>-er</strong>!) / '
        '<strong>Sir</strong> (Latin <em>Senior</em> Elder respected master!) / '
        '<strong>Ma\'am</strong> (Latin <em>Mea Domina</em> My Lady!) = <em>Teacher</em>!'
    ),
    1275: (
        '1. School headmaster: <strong>Director</strong> (<strong>Di-</strong> Apart + <strong>Regere</strong> Rule/Steer!) | '
        '<strong>Rector</strong> (Latin <em>Regere</em> Ruler/Steerer!) = <em>Principal</em>!<br>'
        '2. Primary/main: <strong>Principal</strong> (<strong>Primus</strong> First + <strong>Capere</strong> Take [<em>Prince</em>] = Chief/Main!) = <em>Principal / Main</em>!',
        '1. School headmaster: <strong>Principal</strong> (Latin <strong>Primus</strong> First + <strong>Capere</strong> Take = #1 Head of school!) = <em>Principal</em>!<br>'
        '2. Primary/main: <strong>Khaas</strong> (Arabic <strong>Khass</strong> Special/Exclusive!) / '
        '<strong>Mukhya</strong> (Sanskrit <strong>Mukha</strong> Face/Head [<strong>Tamil முக்கிய Mukkiyam = Main!</strong>]!) = <em>Main / Primary</em>!'
    ),
    1276: (
        '1. Room: <strong>Aula</strong> (Greek <em>Aule</em> Open hall/court!) | '
        '<strong>Salón de clases</strong> (<strong>Salón</strong> Hall + <strong>Clases</strong> Class!) = <em>Classroom</em>!<br>'
        '2. Board: <strong>Pizarra / pizarrón</strong> (Dark split slate rock slab -> chalkboard!) = <em>Blackboard</em>!',
        '1. Room: <strong>Class / classroom</strong> (Latin <em>Classis</em> Called-together rank + <strong>Room</strong>!) = <em>Classroom</em>!<br>'
        '2. Board: <strong>Board / blackboard</strong> (<strong>Black</strong> Dark slate + <strong>Board</strong> Flat plank!) = <em>Blackboard</em>!'
    ),
    1277: (
        '1. Chalk: <strong>Tiza</strong> (Nahuatl <em>Tizatl</em> White chalk clay earth!) = <em>Chalk</em>!<br>'
        '2. Marker: <strong>Marcador</strong> (<strong>Marcar</strong> Mark!) | '
        '<strong>Plumón</strong> (From <strong>Pluma</strong> Feather/Quill + <strong>-ón</strong> Thick pen!) = <em>Marker</em>!<br>'
        '3. Rubber/duster: <strong>Borrador</strong> (<strong>Borrar</strong> Wipe/Erase!) | '
        '<strong>Goma</strong> (Tree sap <em>Gum</em> rubber!) = <em>Eraser</em>!',
        '1. Chalk: <strong>Chalk</strong> (Latin <em>Calx</em> Limestone rock powder [<em>Calcium</em>]!) = <em>Chalk</em>!<br>'
        '2. Marker: <strong>Marker</strong> (Old English <em>Mearc</em> Boundary sign + <strong>-er</strong>!) = <em>Marker</em>!<br>'
        '3. Rubber/duster: <strong>Duster</strong> (<strong>Dust</strong> Wipe chalk dust + <strong>-er</strong>!) / '
        '<strong>Eraser</strong> (<strong>E-</strong> Out + <strong>Radere</strong> Scrape [<em>Erase</em>]!) = <em>Eraser / Duster</em>!'
    ),
    1278: (
        '1. Course book: <strong>Libro de texto</strong> (<strong>Libro</strong> Bark/Book [<em>Library</em>] + <strong>Texto</strong> Woven words [<em>Textile</em>]!) = <em>Textbook</em>!<br>'
        '2. Exercise copy: <strong>Cuaderno</strong> (Latin <em>Quaternio</em> Four folded sheets!) | '
        '<strong>Libreta</strong> (<strong>Libro</strong> Book + <strong>-eta</strong> Little!) = <em>Notebook</em>!',
        '1. Course book: <strong>Kitaab</strong> (Arabic <strong>Kitab</strong> Bound stitched writings!) / '
        '<strong>Textbook</strong> (<strong>Text</strong> Woven script + <strong>Book</strong>!) = <em>Textbook</em>!<br>'
        '2. Exercise copy: <strong>Copy</strong> (Latin <em>Copia</em> Plenty/Transcript sheets!) / '
        '<strong>Notebook</strong> (<strong>Note</strong> Mark down + <strong>Book</strong>!) = <em>Notebook</em>!'
    ),
    1279: (
        '1. Document jacket: <strong>Carpeta</strong> (Latin <em>Carpere</em> Plucked thick felt cover holding papers!) | '
        '<strong>Archivador</strong> (<strong>Archivo</strong> Records box [<em>Archive</em>]!) = <em>Folder / File</em>!<br>'
        '2. Papers: <strong>Documento</strong> (Latin <em>Docere</em> Teach/Prove [<em>Doctor</em>] = Written proof!) = <em>Document</em>!',
        '1. Document jacket: <strong>Folder</strong> (<strong>Fold</strong> Bend over papers + <strong>-er</strong>!) / '
        '<strong>File</strong> (Latin <em>Filum</em> Thread stringing papers together!) = <em>Folder / File</em>!<br>'
        '2. Papers: <strong>Document</strong> (Latin <em>Docere</em> Evidence!) / '
        '<strong>Kagazaat</strong> (<strong>Kagaz [Tamil காகிதம் Kaagitham = Paper!]</strong> + <strong>-aat</strong> Plural papers!) = <em>Document</em>!'
    ),
    1280: (
        '1. Pen: <strong>Bolígrafo</strong> (<strong>Bola</strong> Rolling ballpoint + <strong>Grafo</strong> Writer!) | '
        '<strong>Pluma</strong> (Feather quill [<em>Plume</em>]!) = <em>Pen</em>!<br>'
        '2. Pencil: <strong>Lápiz</strong> (Latin <em>Lapis</em> Dark slate stone [<em>Lapidary</em>]!) = <em>Pencil</em>!<br>'
        '3. Measuring ruler: <strong>Regla</strong> (Latin <em>Regula</em> Straight rod [<em>Regular / Rule</em>]!) = <em>Ruler</em>!',
        '1. Pen: <strong>Pen</strong> (Latin <em>Penna</em> Feather quill!) / '
        '<strong>Kalam</strong> (Arabic <strong>Qalam</strong> Cut reed pen [Greek <em>Kalamos</em>]!) = <em>Pen</em>!<br>'
        '2. Pencil: <strong>Pencil</strong> (Latin <em>Penicillus</em> Little painter’s brush/tail!) = <em>Pencil</em>!<br>'
        '3. Measuring ruler: <strong>Scale</strong> (Latin <em>Scala</em> Graduated ladder steps!) / '
        '<strong>Ruler</strong> (<em>Regula</em> Straight rod!) / '
        '<strong>Patri</strong> (Flat wooden strip/plank!) = <em>Ruler</em>!'
    ),
    1281: (
        '1. Unit: <strong>Lección</strong> (Latin <em>Legere</em> Read aloud [<em>Lecture / Lesson</em>]!) | '
        '<strong>Clase</strong> (Structured group period = <em>Class</em>!) = <em>Lesson</em>!<br>'
        '2. Formal talk: <strong>Conferencia</strong> (<strong>Con-</strong> Together + <strong>Ferre</strong> Bring topics!) | '
        '<strong>Clase magistral</strong> (<strong>Magister</strong> Master’s talk!) = <em>Lecture</em>!',
        '1. Unit: <strong>Sabaq</strong> (Arabic <strong>Sabaq</strong> Ahead/Assigned course portion — life lesson!) / '
        '<strong>Lesson</strong> (Latin <em>Legere</em> Reading unit!) = <em>Lesson</em>!<br>'
        '2. Formal talk: <strong>Lecture</strong> (Latin <em>Lectura</em> Reading aloud to class!) = <em>Lecture</em>!'
    ),
    1282: (
        '1. Daily homework: <strong>Tarea</strong> (Arabic <em>Tariha</em> Assigned task!) | '
        '<strong>Deberes</strong> (From <strong>Deber</strong> Owe — what you owe the teacher [<em>Duty</em>]!) = <em>Homework</em>!<br>'
        '2. Graded project: <strong>Trabajo</strong> (Effort/Work!) | '
        '<strong>Asignación</strong> (<strong>Ad-</strong> + <strong>Signare</strong> Mark/Assign!) = <em>Assignment</em>!<br>'
        '3. Composition: <strong>Ensayo</strong> (<strong>Ex-</strong> + <strong>Agere</strong> Weigh/Try out [<em>Essay</em>]!) | '
        '<strong>Redacción</strong> (<strong>Re-</strong> + <strong>Dactare</strong> Draft/Edit!) = <em>Essay</em>!',
        '1. Daily homework: <strong>Homework</strong> (<strong>Home</strong> + <strong>Work</strong> done after school!) = <em>Homework</em>!<br>'
        '2. Graded project: <strong>Assignment</strong> (<strong>Ad-</strong> To + <strong>Sign</strong> Mark + <strong>-ment</strong> Allotted task!) = <em>Assignment</em>!<br>'
        '3. Composition: <strong>Essay</strong> (Old French <em>Essai</em> Trial/Attempt to argue an idea!) = <em>Essay</em>!'
    ),
    1283: (
        '<strong>Examen</strong> (Latin <em>Examen</em> Weighing scale’s tongue — testing/weighing knowledge!) | '
        '<strong>Prueba</strong> (Latin <em>Proba</em> Proving test [<em>Probe / Proof</em>]!) = <em>Exam / Test</em>!',
        '<strong>Exam</strong> (Latin <em>Exigere</em> Weigh accurately!) / '
        '<strong>Imtehan</strong> (Arabic <strong>Imtihan</strong> Trial/Test of skill!) / '
        '<strong>Test</strong> (Latin <em>Testum</em> Earthen pot used to assay gold purity!) = <em>Exam / Test</em>!'
    ),
    1284: (
        '1. Mark evaluation: <strong>Nota</strong> (Latin <em>Nota</em> Written mark!) | '
        '<strong>Calificación</strong> (<strong>Cual-</strong> Quality + <strong>-ficar</strong> Make = Grade!) = <em>Grade / Mark</em>!<br>'
        '2. Points total: <strong>Puntuación / puntaje</strong> (<strong>Punto</strong> Point/Dot!) = <em>Score</em>!<br>'
        '3. Standing tier: <strong>Puesto</strong> (Placed position!) | <strong>Rango</strong> (Row/Tier [<em>Rank</em>]!) = <em>Rank</em>!',
        '1. Mark evaluation: <strong>Marks / number / grade</strong> (<strong>Mark</strong> Stamp | <strong>Number</strong> Count | <strong>Grade</strong> Latin <em>Gradus</em> Step!) = <em>Grade / Marks</em>!<br>'
        '2. Points total: <strong>Score</strong> (Old Norse <em>Skor</em> Notch cut in a tally stick!) = <em>Score</em>!<br>'
        '3. Standing tier: <strong>Rank</strong> (Germanic <em>Hring</em> Ring/Row in order!) = <em>Rank</em>!'
    ),
    1285: (
        '<strong>Semestre</strong> (<strong>Sex-</strong> Six + <strong>Mensis</strong> Month = Six-month school half!) | '
        '<strong>Período escolar</strong> (<strong>Período</strong> Cycle + <strong>Escolar</strong> School!) = <em>Semester / Term</em>!',
        '<strong>Semester</strong> (<strong>Sex-</strong> Six + <strong>Mensis</strong> Month = Half-year term!) / '
        '<strong>Term</strong> (Latin <em>Terminus</em> Fixed end/boundary time block!) = <em>Semester / Term</em>!'
    ),
    1286: (
        '1. Grant award: <strong>Beca</strong> (Old doctor’s cape/hood stipend backing scholars!) = <em>Scholarship</em>!<br>'
        '2. Course fees: <strong>Matrícula</strong> (Registering onto the mother roll [<em>Matrix</em>]!) | '
        '<strong>Colegiatura</strong> (<strong>Colegio</strong> School + <strong>-tura</strong> Fee!) = <em>Tuition</em>!',
        '1. Grant award: <strong>Scholarship</strong> (<strong>Scholar</strong> Student [Greek <em>Skhole</em> Study] + <strong>-ship</strong> Grant!) = <em>Scholarship</em>!<br>'
        '2. Course fees: <strong>Fees</strong> (Old English <em>Feoh</em> Livestock/Payment!) / '
        '<strong>Padhai ka kharcha</strong> (<strong>Padhai</strong> Study + <strong>Kharcha [Tamil செலவு]</strong> Expense!) = <em>Tuition</em>!'
    ),
    1287: (
        '1. University graduation: <strong>Título universitario</strong> (Official Title!) | '
        '<strong>Carrera</strong> (Study track/Race [<em>Career</em>]!) = <em>Degree</em>!<br>'
        '2. Parchment award: <strong>Diploma</strong> (Greek <em>Diploma</em> Folded-in-two official paper!) | '
        '<strong>Certificado</strong> (<strong>Certo</strong> Certain + <strong>-ficar</strong> Make sure!) = <em>Diploma / Certificate</em>!',
        '1. University graduation: <strong>Degree</strong> (<strong>De-</strong> Down + <strong>Gradus</strong> Step — academic step earned!) = <em>Degree</em>!<br>'
        '2. Parchment award: <strong>Certificate</strong> (<strong>Certus</strong> Certain + <strong>Facere</strong> Make!) / '
        '<strong>Diploma</strong> (Greek <em>Di-</em> Two + <em>Ploos</em> Folded document!) = <em>Certificate / Diploma</em>!'
    ),
    1288: (
        '1. Commencement: <strong>Graduación</strong> (Latin <em>Gradus</em> Step — stepping up a rank!) = <em>Graduation</em>!<br>'
        '2. College grounds: <strong>Campus universitario</strong> (Latin <em>Campus</em> Open flat field [<em>Camp</em>] + University!) = <em>Campus</em>!',
        '1. Commencement: <strong>Graduation</strong> (Latin <em>Gradus</em> Rank/Step completed!) = <em>Graduation</em>!<br>'
        '2. College grounds: <strong>Campus</strong> (Latin <em>Campus</em> Open level college lawn!) = <em>Campus</em>!'
    ),
    1289: (
        '1. Knowledge field: <strong>Ciencia</strong> (Latin <em>Scientia</em> Knowing [from <em>Scire</em> Know]!) = <em>Science</em>!<br>'
        '2. Probe / investigator: <strong>Investigación / investigador</strong> (<strong>In-</strong> + <strong>Vestigium</strong> Footprint — tracking clues!) = <em>Research / Researcher</em>!',
        '1. Knowledge field: <strong>Science</strong> (Latin <em>Scire</em> Know by tested proof!) = <em>Science</em>!<br>'
        '2. Probe / investigator: <strong>Research</strong> (<strong>Re-</strong> Again + <strong>Search</strong> Circle/Look!) / '
        '<strong>Khoj</strong> (Sanskrit <strong>Kshod</strong> Digging/Seeking hidden truth!) = <em>Research</em>!'
    ),
    1290: (
        '<strong>Historia</strong> (Greek <em>Historia</em> Inquiry/Recorded witness account [twin of <em>Story</em>]!) = <em>History</em>!',
        '<strong>Itihaas</strong> (Sanskrit <strong>Iti-</strong> Thus + <strong>Ha-</strong> Verily + <strong>Aasa</strong> Happened — "Thus indeed it happened"!) / '
        '<strong>Tareekh</strong> (Arabic <strong>Ta\'rikh</strong> Dating eras/Chronicled date [<strong>Tamil தேதி Thethi</strong>]!) = <em>History</em>!'
    ),
    1291: (
        '<strong>Geografía</strong> (Greek <strong>Geo-</strong> Earth + <strong>Graphein</strong> Write/Map = Mapping the Earth!) = <em>Geography</em>!',
        '<strong>Geography</strong> (Greek <strong>Geo-</strong> Earth + <strong>Graphia</strong> Drawing/Description = Map of lands!) = <em>Geography</em>!'
    ),
    1292: (
        '<strong>Matemáticas / mates</strong> (Greek <em>Mathema</em> What is learned/Exact calculation science!) = <em>Math / Mathematics</em>!',
        '<strong>Maths</strong> (Greek <em>Mathema</em> Pure knowledge/Number logic!) / '
        '<strong>Hisaab</strong> (Arabic <strong>Hisab [Spoken Tamil ஹிஸாப் = Reckoning/Accounts!]</strong>!) = <em>Math</em>!'
    ),
    1293: (
        '<strong>Física</strong> (Greek <em>Physis</em> Natural growth/Nature of matter & energy [<em>Physical</em>]!) = <em>Physics</em>!',
        '<strong>Physics</strong> (Greek <em>Physis</em> Nature — laws governing matter, force & motion!) = <em>Physics</em>!'
    ),
    1294: (
        '<strong>Química</strong> (Arabic <em>Al-Kimiya</em> / Greek <em>Khemeia</em> Art of smelting & mixing elements!) = <em>Chemistry</em>!',
        '<strong>Chemistry</strong> (From <strong>Alchemy</strong> — art of mixing & transforming atoms/substances!) = <em>Chemistry</em>!'
    ),
    1295: (
        '<strong>Biología</strong> (Greek <strong>Bio-</strong> Life + <strong>-logía</strong> Study of [<em>Logos</em>]!) = <em>Biology</em>!',
        '<strong>Biology</strong> (Greek <strong>Bios</strong> Life + <strong>Logos</strong> Study — science of living things!) = <em>Biology</em>!'
    ),
    1296: (
        '<strong>Literatura</strong> (Latin <strong>Littera</strong> Letter of the alphabet — art of written letters!) = <em>Literature</em>!',
        '<strong>Literature</strong> (Latin <em>Littera</em> Written letter — crafted books, poetry & prose!) = <em>Literature</em>!'
    ),
    1297: (
        '1. Thinking inquiry: <strong>Filosofía</strong> (Greek <strong>Philo-</strong> Love + <strong>Sophia</strong> Wisdom!) = <em>Philosophy</em>!<br>'
        '2. Moral code: <strong>Ética</strong> (Greek <em>Ethos</em> Custom/Character) | '
        '<strong>Moral</strong> (Latin <em>Mores</em> Conduct!) = <em>Ethics / Moral</em>!',
        '1. Thinking inquiry: <strong>Philosophy</strong> (Greek <strong>Philo-</strong> Lover + <strong>Sophia</strong> Wisdom = Love of truth!) = <em>Philosophy</em>!<br>'
        '2. Moral code: <strong>Ethics</strong> (Greek <em>Ethos</em> Character!) / '
        '<strong>Sahi-galat</strong> (<strong>Sahi</strong> Right/True + <strong>Galat</strong> Wrong/Error!) = <em>Ethics</em>!'
    ),
    1298: (
        '1. Mind science: <strong>Psicología</strong> (Greek <strong>Psyche</strong> Mind/Soul + <strong>-logía</strong> Study!) = <em>Psychology</em>!<br>'
        '2. Conduct: <strong>Comportamiento</strong> (<strong>Com-</strong> + <strong>Portar</strong> Carry oneself!) | '
        '<strong>Conducta</strong> (<strong>Con-</strong> + <strong>Ducere</strong> Lead oneself!) = <em>Behavior</em>!',
        '1. Mind science: <strong>Psychology</strong> (Greek <strong>Psyche</strong> Breath/Soul + <strong>Logos</strong> Study!) = <em>Psychology</em>!<br>'
        '2. Conduct: <strong>Bartaav</strong> (Sanskrit <strong>Vart</strong> Move/Deal with others!) / '
        '<strong>Rawaiya</strong> (Persian <strong>Rawish</strong> Way of walking/treating people!) = <em>Behavior</em>!'
    ),
    1299: (
        '1. Tongue: <strong>Idioma</strong> (Greek <em>Idioma</em> Unique speech!) | '
        '<strong>Lengua</strong> (Latin <em>Lingua</em> Tongue organ [<em>Lingual</em>]!) = <em>Language</em>!<br>'
        '2. Syntax: <strong>Gramática</strong> (Greek <em>Gramma</em> Letter rules!) = <em>Grammar</em>!<br>'
        '3. Words stock: <strong>Vocabulario</strong> (<strong>Voz</strong> Voice + <strong>-ario</strong> Word bank!) = <em>Vocabulary</em>!',
        '1. Tongue: <strong>Bhasha</strong> (Sanskrit <strong>Bhash [Tamil பாஷை Baashai = Speech/Language!]</strong>!) / '
        '<strong>Zabaan</strong> (Persian <strong>Zaban</strong> Tongue/Language!) = <em>Language</em>!<br>'
        '2. Syntax: <strong>Grammar</strong> (Greek <em>Gramma</em> Written letter rules!) = <em>Grammar</em>!<br>'
        '3. Words stock: <strong>Vocabulary</strong> (Latin <em>Vocabulum</em> Word name from <em>Vox</em> Voice!) = <em>Vocabulary</em>!'
    ),
    1300: (
        '<strong>Laboratorio</strong> (Latin <strong>Laborare</strong> Work/Toil + <strong>-torio</strong> Workshop = Scientist’s workbench!) = <em>Laboratory / Lab</em>!',
        '<strong>Lab</strong> (Short for <strong>Laboratorium</strong> — room equipped for scientific work & tests!) = <em>Lab</em>!'
    ),
    1301: (
        '1. Empirical test: <strong>Experimento</strong> (<strong>Ex-</strong> Out + <strong>Periri</strong> Try [<em>Peril / Experience</em>]!) | '
        '<strong>Prueba</strong> (Latin <em>Proba</em> Trial!) = <em>Experiment</em>!<br>'
        '2. Verb - try out: <strong>Experimentar</strong> (Put a hypothesis on trial!) = <em>Experiment</em>!',
        '1. Empirical test: <strong>Experiment</strong> (<strong>Ex-</strong> Out + <strong>Periri</strong> Try!) / '
        '<strong>Aazmana</strong> (Persian <strong>Azmudan</strong> Test/Put to trial!) = <em>Experiment</em>!<br>'
        '2. Verb - try out: <strong>Experiment karna</strong> (Run test) / '
        '<strong>Aazma kar dekhna</strong> (<strong>Aazmana</strong> Try + <strong>Dekhna</strong> See outcome!) = <em>Try out</em>!'
    ),
    1302: (
        '<strong>Teoría</strong> (Greek <em>Theoria</em> Contemplation/Seeing pattern [<em>Theater</em>]!) | '
        '<strong>Principio</strong> (<strong>Primus</strong> First + <strong>Capere</strong> Take = Foundation rule [<em>Principle</em>]!) = <em>Theory / Principle</em>!',
        '<strong>Theory</strong> (Greek <em>Theoria</em> Clear framework explanation!) / '
        '<strong>Niyam</strong> (Sanskrit <strong>Ni-</strong> Down + <strong>Yam</strong> Bind [<strong>Tamil நியமம் Niyamam = Rule/Law!</strong>]!) = <em>Theory / Principle</em>!'
    ),
    1303: (
        '1. Found existing: <strong>Descubrimiento</strong> (<strong>Des-</strong> Un- + <strong>Cubrir</strong> Cover = Pulling the veil off something already there!) = <em>Discovery</em>!<br>'
        '2. Created new: <strong>Invento / invención</strong> (<strong>In-</strong> Upon + <strong>Venire</strong> Come = Creating brand-new device!) = <em>Invention</em>!',
        '1. Found existing: <strong>Khoj</strong> (Digging out & uncovering what already existed!) = <em>Discovery</em>!<br>'
        '2. Created new: <strong>Invention</strong> (<strong>In-</strong> Upon + <strong>Venire</strong> Come across/Create!) / '
        '<strong>Nayi cheez banana</strong> (<strong>Nayi</strong> New + <strong>Cheez</strong> Thing + <strong>Banana</strong> Build!) = <em>Invention</em>!'
    ),
    1304: (
        '1. Records: <strong>Datos</strong> (Latin <em>Datum</em> Given facts!) = <em>Data</em>!<br>'
        '2. Probability math: <strong>Estadísticas</strong> (Latin <em>Status</em> State facts — counting state numbers!) = <em>Statistics</em>!<br>'
        '3. Breakdown study: <strong>Análisis</strong> (Greek <strong>Ana-</strong> Up + <strong>Lyein</strong> Loosen/Unbind into parts!) = <em>Analysis</em>!',
        '1. Records: <strong>Data</strong> (Latin <em>Datum</em> Things given as raw facts!) = <em>Data</em>!<br>'
        '2. Probability math: <strong>Statistics</strong> (Latin <em>Status</em> State-survey numbers!) = <em>Statistics</em>!<br>'
        '3. Breakdown study: <strong>Analysis</strong> (Greek <strong>Ana-</strong> Apart + <strong>Lysis</strong> Unbinding parts!) = <em>Analysis</em>!'
    ),
    1305: (
        '1. Dimension size: <strong>Medida / medición</strong> (Latin <em>Metiri</em> Measure [<em>Meter</em>]!) = <em>Measurement</em>!<br>'
        '2. Specimen piece: <strong>Muestra</strong> (From <strong>Mostrar</strong> Show [<em>Demonstrate</em>] = Sample shown!) = <em>Sample</em>!',
        '1. Dimension size: <strong>Naap</strong> (Sanskrit <strong>Maapa</strong> Measuring length/size!) = <em>Measurement</em>!<br>'
        '2. Specimen piece: <strong>Sample</strong> (Latin <em>Exemplum</em> Taken out specimen to show the whole!) = <em>Sample</em>!'
    ),
    1306: (
        '<strong>Fórmula</strong> (<strong>Forma</strong> Shape + <strong>-ula</strong> Tiny = Compact rule recipe!) | '
        '<strong>Ecuación</strong> (<strong>Equus</strong> Equal + <strong>-ación</strong> = Balancing two sides equally!) = <em>Formula / Equation</em>!',
        '<strong>Formula</strong> (Latin <em>Forma</em> Mold/Pattern + <strong>-ula</strong> Compact — concise math recipe!) = <em>Formula</em>!'
    ),
    1307: (
        '<strong>Materia</strong> (Latin <em>Mater</em> Mother wood/stuff forming all things!) | '
        '<strong>Sustancia</strong> (<strong>Sub-</strong> Under + <strong>Stare</strong> Stand = Underlying essence!) = <em>Matter / Substance</em>!',
        '<strong>Cheez</strong> (Persian <strong>Chiz</strong> Physical object/Material!) / '
        '<strong>Substance</strong> (<strong>Sub-</strong> Under + <strong>Stare</strong> Stand — real core stuff!) = <em>Matter / Substance</em>!'
    ),
    1308: (
        '1. Atom unit: <strong>Átomo</strong> (Greek <strong>A-</strong> Not + <strong>Temnein</strong> Cut = Un-cuttable tiny unit!) = <em>Atom</em>!<br>'
        '2. Compound bond: <strong>Molécula</strong> (Latin <strong>Moles</strong> Mass + <strong>-cula</strong> Tiny = Clustered atoms!) = <em>Molecule</em>!',
        '1. Atom unit: <strong>Atom</strong> (Greek <strong>A-</strong> Un- + <strong>Tomos</strong> Cut = Indivisible particle!) = <em>Atom</em>!<br>'
        '2. Compound bond: <strong>Molecule</strong> (Latin <em>Moles</em> Mass + <strong>-cule</strong> Little cluster!) = <em>Molecule</em>!'
    ),
    1309: (
        '1. Power capacity: <strong>Energía</strong> (Greek <strong>En-</strong> In + <strong>Ergon</strong> Work [<em>Erg</em>] = Work inside!) = <em>Energy</em>!<br>'
        '2. Vector push/pull: <strong>Fuerza</strong> (Latin <em>Fortis</em> Strong [<em>Fort / Force</em>]!) = <em>Force</em>!',
        '1. Power capacity: <strong>Energy</strong> (Greek <strong>En-</strong> In + <strong>Ergon</strong> Work!) / '
        '<strong>Taakat</strong> (Arabic <strong>Taqah [Spoken Tamil தாகத் = Strength!]</strong>!) = <em>Energy</em>!<br>'
        '2. Vector push/pull: <strong>Zor</strong> (Persian <strong>Zor</strong> Physical push/power!) / '
        '<strong>Force</strong> (Latin <em>Fortis</em> Strong!) = <em>Force</em>!'
    ),
    1310: (
        '1. Planetary pull: <strong>Gravedad</strong> (Latin <strong>Gravis</strong> Heavy [<em>Grave</em>] = Earth pull!) = <em>Gravity</em>!<br>'
        '2. Movement: <strong>Movimiento</strong> (From <strong>Mover</strong> Move!) = <em>Motion</em>!<br>'
        '3. Velocity rate: <strong>Velocidad</strong> (<strong>Velox</strong> Swift [<em>Velocity</em>]!) | '
        '<strong>Rapidez</strong> (<strong>Rápido</strong> Rapid/Fast!) = <em>Speed</em>!',
        '1. Planetary pull: <strong>Gravity</strong> (Latin <em>Gravis</em> Heavy downward pull!) = <em>Gravity</em>!<br>'
        '2. Movement: <strong>Harkat</strong> (Arabic <strong>Harakah</strong> Stirring/Motion!) = <em>Motion</em>!<br>'
        '3. Velocity rate: <strong>Speed</strong> (Old English <em>Sped</em> Swift success!) / '
        '<strong>Raftaar</strong> (Persian <strong>Raftan</strong> Go/Walk + <strong>-aar</strong> Pace!) = <em>Speed</em>!'
    ),
    1311: (
        '1. Matter quantity: <strong>Masa</strong> (Greek <em>Maza</em> Kneaded lump of dough — bulk of matter!) = <em>Mass</em>!<br>'
        '2. Heaviness: <strong>Peso</strong> (Latin <em>Pensum</em> Hung & weighed [<em>Pensive / Pound</em>]!) = <em>Weight</em>!',
        '1. Matter quantity: <strong>Mass</strong> (Greek <em>Maza</em> Lumped quantity of stuff!) = <em>Mass</em>!<br>'
        '2. Heaviness: <strong>Vajan</strong> (Arabic <strong>Wazn</strong> Scale-balanced heaviness!) = <em>Weight</em>!'
    ),
    1312: (
        '1. Physical force: <strong>Presión</strong> (<strong>Premere</strong> Press hard + <strong>-ión</strong>!) = <em>Pressure</em>!<br>'
        '2. Mental strain: <strong>Presión</strong> (Push) | <strong>Tensión</strong> (<strong>Tendere</strong> Stretch tight!) = <em>Mental Strain</em>!',
        '1. Physical force: <strong>Dabav</strong> (From <strong>Dabna / Dabaana</strong> Press down — pushing force!) / '
        '<strong>Pressure</strong> (<em>Premere</em> Press!) = <em>Pressure</em>!<br>'
        '2. Mental strain: <strong>Tanaav</strong> (Sanskrit <strong>Tan [Tamil தந்தி String!]</strong> = Stretched tight wire!) / '
        '<strong>Tension</strong> (<em>Tendere</em> Stretch!) = <em>Strain / Tension</em>!'
    ),
    1313: (
        '<strong>Radiación</strong> (From <strong>Radio</strong> Spoke/Beam spreading out from a hub [<em>Radiate</em>]!) | '
        '<strong>Rayo</strong> (Spoke beam / Lightning bolt [<em>Ray</em>]!) = <em>Radiation / Ray</em>!',
        '<strong>Kiran</strong> (Sanskrit <strong>Kirana [Tamil கிரணம் Kiranam = Sunbeam!]</strong>!) / '
        '<strong>Radiation</strong> (Latin <em>Radius</em> Hub-spoke beams shooting outward!) = <em>Radiation / Ray</em>!'
    ),
    1314: (
        '1. Power: <strong>Electricidad</strong> (Greek <em>Elektron</em> Amber that sparks when rubbed!) = <em>Electricity</em>!<br>'
        '2. Current flow: <strong>Corriente eléctrica</strong> (<strong>Correr</strong> Run/Flow [<em>Current</em>] + Electric!) = <em>Current</em>!<br>'
        '3. Potential: <strong>Voltaje</strong> (Italian pioneer Alessandro <strong>Volta</strong>!) = <em>Voltage</em>!',
        '1. Power: <strong>Bijli</strong> (Sanskrit <strong>Vidyut</strong> Lightning bolt [<strong>Tamil மின்னல்</strong>]!) / '
        '<strong>Electricity</strong> (Greek <em>Elektron</em> Amber spark!) = <em>Electricity</em>!<br>'
        '2. Current flow: <strong>Current</strong> (Latin <em>Currere</em> Running stream!) = <em>Current</em>!<br>'
        '3. Potential: <strong>Voltage</strong> (Inventor <strong>Volta</strong> + <strong>-age</strong> Push!) = <em>Voltage</em>!'
    ),
    1315: (
        '<strong>Imán / magnético</strong> (French <em>Aimant</em> "Loving" stone pulling iron | Greek <em>Magnesia</em> hill where lodestone was found!) = <em>Magnet / Magnetic</em>!',
        '<strong>Chumbak</strong> (Sanskrit <strong>Chumb</strong> Kiss/Attract — iron-kissing stone!) / '
        '<strong>Magnetic</strong> (Greek <em>Magnesia</em> Ore hill pulling iron!) = <em>Magnet / Magnetic</em>!'
    ),
    1316: (
        '<strong>Tecnología</strong> (Greek <strong>Tekhne</strong> Craft/Skill + <strong>-logía</strong> Knowledge!) | '
        '<strong>Digital</strong> (Latin <strong>Digitus</strong> Finger/Counter — 1s & 0s counted on fingers!) = <em>Technology / Digital</em>!',
        '<strong>Technology</strong> (Greek <strong>Tekhne</strong> Craft tool + <strong>Logos</strong> System!) / '
        '<strong>Digital</strong> (Latin <em>Digitus</em> Finger — binary digit steps!) = <em>Technology / Digital</em>!'
    ),
    1317: (
        '<strong>Pantalla</strong> (Light shield/Lamp shade -> glowing glass face!) | '
        '<strong>Monitor</strong> (Latin <em>Monere</em> Warn/Display/Watch over!) = <em>Screen / Monitor</em>!',
        '<strong>Screen</strong> (Germanic <em>Skerm</em> Partition wall displaying images!) / '
        '<strong>Display</strong> (<strong>Dis-</strong> Un- + <strong>Plicare</strong> Fold = Unfold to show!) = <em>Screen / Display</em>!'
    ),
    1318: (
        '<strong>Teclado</strong> (From <strong>Tecla</strong> Piano/Typewriter Key + <strong>-ado</strong> Set of keys!) = <em>Keyboard</em>!',
        '<strong>Keyboard</strong> (<strong>Key</strong> Latch/Button [Old English <em>Caeg</em>] + <strong>Board</strong> Flat plank!) = <em>Keyboard</em>!'
    ),
    1319: (
        '1. Hardcopy machine: <strong>Impresora</strong> (<strong>Im-</strong> In + <strong>Premere</strong> Press ink onto paper!) = <em>Printer</em>!<br>'
        '2. Image digitizer: <strong>Escáner</strong> (Latin <em>Scandere</em> Climb step-by-step across a page [<em>Scan</em>]!) = <em>Scanner</em>!',
        '1. Hardcopy machine: <strong>Printer</strong> (<strong>Im- + Premere</strong> Stamp/Press ink + <strong>-er</strong>!) = <em>Printer</em>!<br>'
        '2. Image digitizer: <strong>Scanner</strong> (Latin <em>Scandere</em> Sweep line-by-line + <strong>-er</strong>!) = <em>Scanner</em>!'
    ),
    1320: (
        '1. Voice input: <strong>Micrófono / micro</strong> (Greek <strong>Mikros</strong> Tiny + <strong>Phone</strong> Sound!) = <em>Microphone</em>!<br>'
        '2. Audio output: <strong>Altavoz</strong> (<strong>Alta</strong> Loud + <strong>Voz</strong> Voice!) | '
        '<strong>Parlante</strong> (<strong>Parlar</strong> Talk [<em>Parlor</em>] + <strong>-ante</strong>!) = <em>Speaker</em>!',
        '1. Voice input: <strong>Mic</strong> (Short for <strong>Mikros</strong> Tiny + <strong>Phone</strong> Sound!) = <em>Mic</em>!<br>'
        '2. Audio output: <strong>Speaker</strong> (<strong>Speak</strong> Voice + <strong>-er</strong> Device projecting voice!) = <em>Speaker</em>!'
    ),
    1321: (
        '<strong>Cable</strong> (Latin <em>Capulum</em> Strong halter rope [<em>Cable</em>]!) | '
        '<strong>Alambre</strong> (From Latin <em>Aeramen</em> Copper/Bronze wire!) = <em>Cable / Wire</em>!',
        '<strong>Taar</strong> (Sanskrit <strong>Tantra</strong> Stretched string/wire [<strong>Tamil தந்தி Thanthi = Wire/Telegraph!</strong>]!) / '
        '<strong>Cable</strong> (Latin <em>Capulum</em> Thick twisted line!) = <em>Cable / Wire</em>!'
    ),
    1322: (
        '1. Physical computer parts: <strong>Hardware</strong> (<strong>Hard</strong> Solid metal/chips + <strong>Ware</strong> Goods!) = <em>Hardware</em>!<br>'
        '2. Digital applications: <strong>Software</strong> (<strong>Soft</strong> Intangible code + <strong>Ware</strong> Goods!) = <em>Software</em>!',
        '1. Physical computer parts: <strong>Hardware</strong> (<strong>Hard</strong> Touch-solid gear + <strong>Ware</strong> Goods!) = <em>Hardware</em>!<br>'
        '2. Digital applications: <strong>Software</strong> (<strong>Soft</strong> Non-physical instructions + <strong>Ware</strong> Goods!) = <em>Software</em>!'
    ),
    1323: (
        '<strong>Código</strong> (Latin <em>Codex</em> Wooden tablet rulebook [<em>Code</em>]!) | '
        '<strong>Programa</strong> (Greek <strong>Pro-</strong> Before + <strong>Gramma</strong> Written plan!) = <em>Code / Program</em>!',
        '<strong>Code</strong> (Latin <em>Codex</em> Law/Cipher book!) / '
        '<strong>Program</strong> (Greek <strong>Pro-</strong> Ahead + <strong>Graphein</strong> Written sequence!) = <em>Code / Program</em>!'
    ),
    1324: (
        '1. Connection web: <strong>Red</strong> (Latin <em>Rete</em> Woven fishing net [<em>Retina / Network</em>]!) = <em>Network</em>!<br>'
        '2. Host system: <strong>Servidor</strong> (From <strong>Servir</strong> Serve data requests [<em>Server</em>]!) = <em>Server</em>!',
        '1. Connection web: <strong>Network</strong> (<strong>Net</strong> Woven mesh + <strong>Work</strong> Interlinked system!) = <em>Network</em>!<br>'
        '2. Host system: <strong>Server</strong> (Latin <em>Servire</em> Serve + <strong>-er</strong> Machine serving files!) = <em>Server</em>!'
    ),
    1325: (
        '<strong>Memoria</strong> (Latin <em>Memor</em> Mindful/Recalling [<em>Memory</em>]!) | '
        '<strong>Almacenamiento</strong> (Arabic <em>Al-Makhzan</em> Warehouse/Storehouse [<em>Almacén</em>]!) = <em>Memory / Storage</em>!',
        '<strong>Memory</strong> (Latin <em>Memor</em> Retaining!) / '
        '<strong>Storage</strong> (Old French <em>Estor</em> Supplies laid up + <strong>-age</strong>!) = <em>Memory / Storage</em>!'
    ),
    1326: (
        '<strong>Chip</strong> (Tiny sliced flake of silicon wafer!) | '
        '<strong>Procesador</strong> (<strong>Pro-</strong> Forward + <strong>Cedere</strong> Go = Step-by-step calculator [<em>Processor</em>]!) = <em>Chip / Processor</em>!',
        '<strong>Chip</strong> (Chopped thin wafer slice of silicon!) / '
        '<strong>Processor</strong> (<strong>Pro-</strong> Forward + <strong>Cedere</strong> Move instructions!) = <em>Chip / Processor</em>!'
    ),
    1327: (
        '1. Wave transmission: <strong>Señal</strong> (Latin <em>Signum</em> Sign/Beacon [<em>Signal</em>]!) = <em>Signal</em>!<br>'
        '2. Space relay: <strong>Satélite</strong> (Latin <em>Satelles</em> Attendant guard orbiting a king/planet!) = <em>Satellite</em>!',
        '1. Wave transmission: <strong>Signal</strong> (Latin <em>Signum</em> Guiding mark/wave!) = <em>Signal</em>!<br>'
        '2. Space relay: <strong>Satellite</strong> (Latin <em>Satelles</em> Orbiting escort around Earth!) = <em>Satellite</em>!'
    ),
    1328: (
        '<strong>Dispositivo</strong> (<strong>Dis-</strong> Apart + <strong>Ponere</strong> Place = Arranged gadget!) | '
        '<strong>Aparato</strong> (<strong>Ad-</strong> + <strong>Parare</strong> Prepare = Ready gear [<em>Apparatus</em>]!) = <em>Device</em>!',
        '<strong>Device</strong> (Latin <em>Dividere</em> Divide/Design cleanly — clever engineered gadget!) / '
        '<strong>Machine</strong> (Greek <em>Mekhane</em> Contrivance/Engine!) = <em>Device / Machine</em>!'
    ),
    1329: (
        '1. Stock fabric/matter: <strong>Material</strong> (From <em>Materia</em> Mother-timber/building stuff!) = <em>Material</em>!<br>'
        '2. Metallic element: <strong>Metal</strong> (Greek <em>Metallon</em> Mined ore/quarry!) = <em>Metal</em>!',
        '1. Stock fabric/matter: <strong>Saamaan</strong> (Persian <strong>Saman [Tamil சாமான் = Goods/Things!]</strong>) / '
        '<strong>Maal</strong> (Arabic <strong>Mal</strong> Goods/Stock) / '
        '<strong>Material</strong> (<em>Materia</em> Raw stuff!) = <em>Material</em>!<br>'
        '2. Metallic element: <strong>Metal</strong> (Greek <em>Metallon</em> Dug-up ore!) = <em>Metal</em>!'
    ),
    1330: (
        '1. Iron: <strong>Hierro / fierro</strong> (Latin <em>Ferrum</em> Iron [chemical symbol <strong>Fe</strong>, <em>Ferrous</em>]!) = <em>Iron</em>!<br>'
        '2. Steel alloy: <strong>Acero</strong> (Latin <em>Acies</em> Sharp edge [<em>Acumen</em>] — hard blade iron!) = <em>Steel</em>!',
        '1. Iron: <strong>Loha</strong> (Sanskrit <strong>Loha = Reddish Iron/Metal [Tamil இரும்பு / லோகம்!]</strong>!) = <em>Iron</em>!<br>'
        '2. Steel alloy: <strong>Steel</strong> (Germanic <em>Stahlaz</em> Firm/Standing hard alloy!) = <em>Steel</em>!'
    ),
    1331: (
        '1. Copper: <strong>Cobre</strong> (Latin <em>Cuprum</em> Metal from <em>Cyprus</em> island [chemical symbol <strong>Cu</strong>]!) = <em>Copper</em>!<br>'
        '2. Bronze: <strong>Bronce</strong> (Persian <em>Birinj</em> Alloyed bell metal [<em>Bronze</em>]!) = <em>Bronze</em>!<br>'
        '3. Aluminum: <strong>Aluminio</strong> (From <em>Alum</em> mineral salt — light silver metal!) = <em>Aluminum</em>!',
        '1. Copper: <strong>Taamba</strong> (Sanskrit <strong>Tamra = Dark-red [Tamil தாமிரம் Taamiram = Copper!]</strong>!) = <em>Copper</em>!<br>'
        '2. Bronze: <strong>Kaansa</strong> (Sanskrit <strong>Kamsya [Tamil வெண்கலம்]</strong> Cast bell bronze!) / '
        '<strong>Bronze</strong> (Persian <em>Birinj</em> Copper-tin alloy!) = <em>Bronze</em>!<br>'
        '3. Aluminum: <strong>Aluminum</strong> (From <em>Alumen</em> bitter crystal mineral!) = <em>Aluminum</em>!'
    ),
    1332: (
        '1. Clay block: <strong>Ladrillo</strong> (Latin <em>Laterculus</em> Baked flat clay tile/brick!) = <em>Brick</em>!<br>'
        '2. Powder bond: <strong>Cemento</strong> (Latin <em>Caementum</em> Chipped quarry stone binder!) = <em>Cement</em>!<br>'
        '3. Aggregate concrete: <strong>Hormigón</strong> (From <em>Formar</em> Poured in molds!) | '
        '<strong>Concreto</strong> (<strong>Con-</strong> + <strong>Crescere</strong> Grow solid together!) = <em>Concrete</em>!',
        '1. Clay block: <strong>Eent</strong> (Sanskrit <strong>Ishtaka [Tamil செங்கல் = Baked Brick]</strong>!) = <em>Brick</em>!<br>'
        '2. Powder bond: <strong>Cement</strong> (Latin <em>Caedere</em> Cut stone dust glue!) = <em>Cement</em>!<br>'
        '3. Aggregate concrete: <strong>Concrete</strong> (<strong>Con-</strong> Together + <strong>Crescere</strong> Harden into one stone!) = <em>Concrete</em>!'
    ),
    1333: (
        '<strong>Arcilla</strong> (Latin <em>Argilla</em> White potter’s earth!) | '
        '<strong>Barro</strong> (Wet river mud/clay!) | '
        '<strong>Cerámica</strong> (Greek <em>Keramos</em> Kiln-fired potter’s clay!) = <em>Clay / Ceramic</em>!',
        '<strong>Chikni mitti</strong> (<strong>Chikni</strong> Smooth/Greasy + <strong>Mitti</strong> Earth/Soil!) / '
        '<strong>Ceramic</strong> (Greek <em>Keramos</em> Fired pottery clay!) = <em>Clay / Ceramic</em>!'
    ),
    1334: (
        '1. Hard resin: <strong>Plástico</strong> (Greek <em>Plassein</em> Moldable/Shapeable [<em>Plastic</em>]!) = <em>Plastic</em>!<br>'
        '2. Elastic latex: <strong>Goma</strong> (Tree resin <em>Gum</em>!) | '
        '<strong>Caucho</strong> (Quechua <em>Cauchuc</em> "Weeping wood" rubber tree sap!) = <em>Rubber</em>!',
        '1. Hard resin: <strong>Plastic</strong> (Greek <em>Plassein</em> Easy to mold into shapes!) = <em>Plastic</em>!<br>'
        '2. Elastic latex: <strong>Rubber</strong> (From <strong>Rub</strong> — first used by Joseph Priestley to rub out pencil marks!) = <em>Rubber</em>!'
    ),
    1335: (
        '<strong>Cuero</strong> (Latin <em>Corium</em> Tough animal hide!) | '
        '<strong>Piel</strong> (Latin <em>Pellis</em> Skin/Pelt [<em>Pelt / Peel</em>]!) = <em>Leather</em>!',
        '<strong>Chamda</strong> (Sanskrit <strong>Charma = Hide/Skin [Tamil சருமம் Charmam = Skin/Leather!]</strong>!) = <em>Leather</em>!'
    ),
    1336: (
        '<strong>Tela</strong> (Latin <em>Tela</em> Woven web/cloth [related to <em>Textile</em>]!) | '
        '<strong>Tejido</strong> (From <strong>Tejer</strong> Weave threads [<em>Text</em>]!) = <em>Cloth / Fabric</em>!',
        '<strong>Kapda</strong> (Sanskrit <strong>Karpata</strong> Torn rag/woven garment!) / '
        '<strong>Fabric</strong> (Latin <em>Fabrica</em> Skilled craftwork woven at loom!) = <em>Cloth / Fabric</em>!'
    ),
    1337: (
        '1. Cotton: <strong>Algodón</strong> (Arabic <em>Al-Qutun</em> Fluffy white boll [origin of <em>Cotton</em>]!) = <em>Cotton</em>!<br>'
        '2. Wool: <strong>Lana</strong> (Latin <em>Lana</em> Sheep fleece [<em>Lanolin</em>]!) = <em>Wool</em>!<br>'
        '3. Silk: <strong>Seda</strong> (Latin <em>Seta</em> Fine bristle/silky thread [<em>Silk / Satin</em>]!) = <em>Silk</em>!',
        '1. Cotton: <strong>Sooti / rui / cotton</strong> (Sanskrit <strong>Sutra</strong> Thread [<strong>Tamil சூத்திரம்</strong>] / Bolls / Arabic <em>Al-Qutn</em>!) = <em>Cotton</em>!<br>'
        '2. Wool: <strong>Oon</strong> (Sanskrit <strong>Urna</strong> Sheep fleece!) = <em>Wool</em>!<br>'
        '3. Silk: <strong>Resham / silk</strong> (Persian <em>Abresham</em> Fine spun cocoon fiber / Chinese root <em>Si</em>!) = <em>Silk</em>!'
    ),
    1338: (
        '1. Art discipline: <strong>Arte</strong> (Latin <em>Ars</em> Skilled craft/joining!) = <em>Art</em>!<br>'
        '2. Artwork piece: <strong>Obra de arte</strong> (<strong>Obra</strong> Work [<em>Opus</em>] + <strong>Arte</strong> Art!) = <em>Artwork</em>!<br>'
        '3. Tour de force: <strong>Obra maestra</strong> (<strong>Obra</strong> Work + <strong>Maestra</strong> Master’s!) = <em>Masterpiece</em>!',
        '1. Art discipline: <strong>Kala</strong> (Sanskrit <strong>Kala [Tamil கலை Kalai = Fine Art/Skill!]</strong>!) / <strong>Art</strong> (Latin <em>Ars</em> Craft!) = <em>Art</em>!<br>'
        '2. Artwork piece: <strong>Kala / art</strong> (Finished creative work [<strong>Tamil கலை</strong>]!) = <em>Artwork</em>!<br>'
        '3. Tour de force: <strong>Masterpiece</strong> (<strong>Master</strong> + <strong>Piece</strong>) / <strong>Kamaal ki cheez</strong> (<strong>Kamaal</strong> Wonder + <strong>Cheez</strong> Thing!) = <em>Masterpiece</em>!'
    ),
    1339: (
        '1. Outline drawing: <strong>Boceto</strong> (Italian <em>Bozzo</em> Rough uncarved stone/outline!) | '
        '<strong>Dibujo</strong> (Pencil/ink line drawing!) = <em>Sketch</em>!<br>'
        '2. Face likeness: <strong>Retrato</strong> (<strong>Re-</strong> Back + <strong>Traer</strong> Draw [<em>Portrait</em>]!) = <em>Portrait</em>!',
        '1. Outline drawing: <strong>Sketch</strong> (Greek <em>Skhedios</em> Done swiftly offhand!) = <em>Sketch</em>!<br>'
        '2. Face likeness: <strong>Tasveer</strong> (Arabic <strong>Taswir</strong> Forming an image/form!) / '
        '<strong>Portrait</strong> (<strong>Pro-</strong> Forth + <strong>Trahere</strong> Draw!) = <em>Portrait</em>!'
    ),
    1340: (
        '1. Statue effigy: <strong>Estatua</strong> (Latin <strong>Stare</strong> Stand still!) | '
        '<strong>Escultura</strong> (Latin <strong>Sculpere</strong> Carve [<em>Sculpt</em>]!) = <em>Statue / Sculpture</em>!<br>'
        '2. Historic site: <strong>Monumento</strong> (Latin <strong>Monere</strong> Remind/Remember = Memory landmark!) = <em>Monument</em>!',
        '1. Statue effigy: <strong>Moorti</strong> (Sanskrit <strong>Murti [Tamil மூர்த்தி Moorthy = Embodied Idol/Statue!]</strong>!) / '
        '<strong>Statue</strong> (<em>Stare</em> Stand!) = <em>Statue / Sculpture</em>!<br>'
        '2. Historic site: <strong>Itihaasik imaarat</strong> (<strong>Itihaasik</strong> Historic + <strong>Imaarat</strong> Edifice!) / '
        '<strong>Monument</strong> (<em>Monere</em> Remind!) = <em>Monument</em>!'
    ),
    1341: (
        '1. Hall: <strong>Galería</strong> (Covered arched walkway displaying paintings [<em>Gallery</em>]!) = <em>Gallery</em>!<br>'
        '2. Showing event: <strong>Exposición</strong> (<strong>Ex-</strong> Out + <strong>Ponere</strong> Place = Put out on show!) | '
        '<strong>Muestra</strong> (<strong>Mostrar</strong> Show!) = <em>Exhibition</em>!',
        '1. Hall: <strong>Gallery</strong> (Medieval covered portico hall lined with artworks!) = <em>Gallery</em>!<br>'
        '2. Showing event: <strong>Exhibition</strong> (<strong>Ex-</strong> Out + <strong>Habere</strong> Hold out in view!) = <em>Exhibition</em>!'
    ),
    1342: (
        '1. Platform: <strong>Escenario</strong> (Greek <em>Skene</em> Stage tent!) | <strong>Tablas</strong> (Wooden stage planks!) = <em>Stage</em>!<br>'
        '2. Playhouse building: <strong>Teatro</strong> (Greek <em>Theatron</em> Viewing place!) = <em>Theater</em>!<br>'
        '3. Theatrical play: <strong>Obra de teatro</strong> (Stage work!) | <strong>Drama</strong> (Greek <em>Dran</em> Act/Do!) = <em>Drama</em>!',
        '1. Platform: <strong>Stage</strong> (Latin <em>Stare</em> Raised standing platform!) = <em>Stage</em>!<br>'
        '2. Playhouse building: <strong>Theatre</strong> (Greek <em>Theasthai</em> Gaze/Watch!) = <em>Theatre</em>!<br>'
        '3. Theatrical play: <strong>Naatak</strong> (Sanskrit <strong>Nataka [Tamil நாடகம் Naadagam = Play/Dance-drama!]</strong>!) / '
        '<strong>Drama</strong> (Greek <em>Dran</em> Action!) = <em>Drama</em>!'
    ),
    1343: (
        '1. Humorous: <strong>Comedia</strong> (Greek <strong>Komos</strong> Merry revel + <strong>Aeidein</strong> Sing = Cheerful play!) = <em>Comedy</em>!<br>'
        '2. Sorrowful: <strong>Tragedia</strong> (Greek <em>Tragos</em> Goat + <em>Oide</em> Solemn song = Sad drama!) = <em>Tragedy</em>!',
        '1. Humorous: <strong>Comedy</strong> (Greek <em>Komoidia</em> Festive song!) / '
        '<strong>Hasi-mazaak</strong> (<strong>Hasi</strong> Laughter + <strong>Mazaak</strong> Jest [<strong>Tamil மஜா!</strong>]!) = <em>Comedy</em>!<br>'
        '2. Sorrowful: <strong>Tragedy</strong> (Greek <em>Tragoidia</em> Grave fate play!) / '
        '<strong>Haadsa</strong> (Arabic <strong>Hadithah</strong> Sudden calamitous event!) = <em>Tragedy</em>!'
    ),
    1344: (
        '1. Live show: <strong>Actuación</strong> (<strong>Acto</strong> Act/Do!) | '
        '<strong>Función</strong> (<strong>Fungi</strong> Perform a role [<em>Function</em>]!) = <em>Performance</em>!<br>'
        '2. Practice run: <strong>Ensayo</strong> (<strong>Ex-</strong> + <strong>Agere</strong> Test/Try out run!) = <em>Rehearsal</em>!',
        '1. Live show: <strong>Performance</strong> (<strong>Per-</strong> Through + <strong>Fournir</strong> Carry out/Complete stage act!) = <em>Performance</em>!<br>'
        '2. Practice run: <strong>Rehearsal</strong> (<strong>Re-</strong> Again + <strong>Hearse</strong> Rake/Harrow — repeating lines over & over!) / '
        '<strong>Practice</strong> (Greek <em>Praktikos</em> Doing drill!) = <em>Rehearsal</em>!'
    ),
    1345: (
        '1. View cut: <strong>Escena</strong> (Greek <em>Skene</em> Stage backdrop/Scene!) = <em>Scene</em>!<br>'
        '2. Screenplay text: <strong>Guión</strong> (From <strong>Guía</strong> Guide — line-by-line guide for actors!) = <em>Script</em>!',
        '1. View cut: <strong>Scene</strong> (Greek <em>Skene</em> Painted stage set/shot!) = <em>Scene</em>!<br>'
        '2. Screenplay text: <strong>Script</strong> (Latin <em>Scribere</em> Written manuscript!) = <em>Script</em>!'
    ),
    1346: (
        '1. Acoustic art: <strong>Música</strong> (Greek <em>Mousike</em> Art of the nine Muses!) = <em>Music</em>!<br>'
        '2. Track: <strong>Canción</strong> (Latin <em>Cantus</em> Chant [<em>Chant / Cantata</em>]!) | '
        '<strong>Tema</strong> (Greek <em>Thema</em> Musical motif [<em>Theme</em>]!) = <em>Song</em>!',
        '1. Acoustic art: <strong>Music</strong> (Greek <em>Mousa</em> Muse!) / '
        '<strong>Sangeet</strong> (<strong>Sam-</strong> Together + <strong>Geet</strong> Sung [<strong>Tamil சங்கீதம் Sangeetham!</strong>]!) = <em>Music</em>!<br>'
        '2. Track: <strong>Gaana / geet</strong> (Sanskrit <strong>Gana / Gita [Tamil கீதம் Geetham = Hymn/Song!]</strong>!) = <em>Song</em>!'
    ),
    1347: (
        '1. Melodic line: <strong>Melodía</strong> (Greek <strong>Melos</strong> Song limb + <strong>Oide</strong> Singing tune!) = <em>Melody</em>!<br>'
        '2. Cadence beat: <strong>Ritmo</strong> (Greek <em>Rhysmos</em> Measured flowing beat!) | '
        '<strong>Compás</strong> (<strong>Com-</strong> With + <strong>Paso</strong> Step = Beat measure!) = <em>Rhythm</em>!',
        '1. Melodic line: <strong>Sur</strong> (Sanskrit <strong>Svara [Tamil சுரம் Suram = Musical Note!]</strong>!) / '
        '<strong>Dhun</strong> (Sanskrit <strong>Dhwani [Tamil தொனி = Sound/Resonance!]</strong>!) = <em>Melody / Tune</em>!<br>'
        '2. Cadence beat: <strong>Rhythm</strong> (Greek <em>Rhysmos</em> Flow!) / '
        '<strong>Taal</strong> (Sanskrit <strong>Tala [Tamil தாளம் Thaalam = Hand-clap Beat!]</strong>!) = <em>Rhythm</em>!'
    ),
    1348: (
        '<strong>Letra (de la canción)</strong> (Latin <em>Littera</em> Written letters/Words of the <em>Canción</em> song!) = <em>Lyrics</em>!',
        '<strong>Lyrics</strong> (Greek <em>Lyra</em> Lyre harp — words written to be sung to a lyre!) / '
        '<strong>Gaane ke bol</strong> (<strong>Gaana</strong> Song + <strong>Bol</strong> Spoken words from <em>Bolna</em>!) = <em>Lyrics</em>!'
    ),
    1349: (
        '1. Music: <strong>Instrumento musical</strong> (<strong>In-</strong> + <strong>Struere</strong> Build/Equip [<em>Instrument</em>] + Musical!) = <em>Musical Instrument</em>!<br>'
        '2. Tool/measuring device: <strong>Instrumento</strong> (Tool!) | '
        '<strong>Aparato</strong> (<strong>Ad-</strong> + <strong>Parare</strong> Prepare = Apparatus!) = <em>Instrument / Device</em>!',
        '1. Music: <strong>Instrument</strong> (<strong>In-</strong> + <strong>Struere</strong> Equip/Fit out for music!) = <em>Instrument</em>!<br>'
        '2. Tool/measuring device: <strong>Auzaar</strong> (Arabic plural of <strong>Wizr</strong> Burden-bearing tools/gear!) / '
        '<strong>Tool</strong> (Old English <em>Tol</em> Hand implement!) = <em>Tool / Instrument</em>!'
    ),
    1350: (
        '<strong>Guitarra</strong> (Greek <em>Kithara</em> Six-string lute!) | '
        '<strong>Piano</strong> (Italian <em>Piano-forte</em> "Soft-Loud" keyed instrument!) | '
        '<strong>Violín</strong> (Latin <em>Vitula</em> Bowed string instrument!) = <em>Guitar / Piano / Violin</em>!',
        '<strong>Guitar</strong> (Greek <em>Kithara</em> Plucked strings!) / '
        '<strong>Piano</strong> (Italian <em>Piano-forte</em> Soft-and-loud hammers!) / '
        '<strong>Violin</strong> (Latin <em>Vitula</em> Bowed fiddle!) = <em>Guitar / Piano / Violin</em>!'
    ),
    1351: (
        '1. Percussion: <strong>Tambor</strong> (Arabic <em>Tunbur</em> Struck drum [<em>Tambourine</em>]!) | '
        '<strong>Batería</strong> (From <strong>Batir</strong> Beat/Batter = Drum battery kit!) = <em>Drum</em>!<br>'
        '2. Flute pipe: <strong>Flauta</strong> (Latin <em>Flatus</em> Blown breath [<em>Inflate</em>]!) = <em>Flute</em>!',
        '1. Percussion: <strong>Dholak</strong> (Resonant two-headed hand drum — <em>Dhol</em> + small <em>-ak</em>!) / '
        '<strong>Drum</strong> (Hollow taut-skin beat!) = <em>Drum</em>!<br>'
        '2. Flute pipe: <strong>Baansuri</strong> (<strong>Baans</strong> Bamboo reed + <strong>Suri</strong> Musical breath pipe!) = <em>Flute</em>!'
    ),
    1352: (
        '1. Live recital: <strong>Concierto</strong> (<strong>Con-</strong> Together + <strong>Certare</strong> Strive/Harmonize = Live ensemble!) = <em>Concert</em>!<br>'
        '2. Music group: <strong>Banda</strong> (Grouped band!) | '
        '<strong>Orquesta</strong> (Greek <em>Orkhestra</em> Front-stage pit for musicians!) = <em>Band / Orchestra</em>!',
        '1. Live recital: <strong>Concert</strong> (<strong>Con-</strong> Together + <strong>Certare</strong> Play in harmony!) = <em>Concert</em>!<br>'
        '2. Music group: <strong>Band</strong> (Germanic <em>Bindan</em> Bound group!) / '
        '<strong>Orchestra</strong> (Greek <em>Orkhestra</em> Stage ensemble pit!) = <em>Band / Orchestra</em>!'
    ),
    1353: (
        '1. Game contest: <strong>Deporte</strong> (<strong>Des-</strong> Away + <strong>Portar</strong> Carry — carry mind away from work to play [origin of <em>Sport</em>]!) = <em>Sport</em>!<br>'
        '2. Player: <strong>Atleta</strong> (Greek <em>Athlon</em> Prize contest!) | '
        '<strong>Deportista</strong> (One playing <em>Deporte</em>!) = <em>Athlete</em>!',
        '1. Game contest: <strong>Khel</strong> (Sanskrit <strong>Khela</strong> Play/Sporting leap!) / '
        '<strong>Sport</strong> (Short for <em>Disport</em> — play away from work!) = <em>Sport</em>!<br>'
        '2. Player: <strong>Khilaadi</strong> (From <strong>Khelna</strong> Play + <strong>-aadi</strong> Expert player!) / '
        '<strong>Athlete</strong> (Greek <em>Athlon</em> Contest prize fighter!) = <em>Athlete</em>!'
    ),
    1354: (
        '<strong>Estadio</strong> (Greek <em>Stadion</em> Fixed 600-foot running track & tiered arena [<em>Stadium</em>]!) = <em>Stadium</em>!',
        '<strong>Stadium</strong> (Greek <em>Stadion</em> Ancient running track!) / '
        '<strong>Maidaan</strong> (Arabic <strong>Maidan [Tamil மைதானம் Maidaanam = Open Field!]</strong>!) = <em>Stadium / Ground</em>!'
    ),
    1355: (
        '<strong>Fútbol</strong> (<strong>Foot</strong> + <strong>Ball</strong>) | '
        '<strong>Críquet</strong> (Old English <em>Cricc</em> Crooked bat/wicket staff!) | '
        '<strong>Tenis</strong> (Old French <em>Tenez!</em> "Hold/Receive!" shouted on serve!) = <em>Football / Cricket / Tennis</em>!',
        '<strong>Football</strong> (<strong>Foot</strong> + <strong>Ball</strong>) / '
        '<strong>Cricket</strong> (Crooked bat/stump game!) / '
        '<strong>Tennis</strong> (French <em>Tenez!</em> "Take this serve!") = <em>Football / Cricket / Tennis</em>!'
    ),
    1356: (
        '<strong>Carrera</strong> (Latin <em>Carrus</em> Chariot wheel track [<em>Career / Car</em>] = Foot/chariot race!) | '
        '<strong>Maratón</strong> (Greek plain of <em>Marathon</em> — 26-mile messenger run!) = <em>Race / Marathon</em>!',
        '<strong>Race</strong> (Old Norse <em>Ras</em> Swift rush/current!) / '
        '<strong>Daud</strong> (Sanskrit <strong>Dhav</strong> Run fast/Sprint!) / '
        '<strong>Marathon</strong> (Greek town <em>Marathon</em> — epic 42km run!) = <em>Race / Marathon</em>!'
    ),
    1357: (
        '1. Trail walk: <strong>Senderismo</strong> (<strong>Sendero</strong> Path/Trail + <strong>-ismo</strong>!) | '
        '<strong>Caminata</strong> (From <strong>Caminar</strong> Walk!) = <em>Hiking</em>!<br>'
        '2. Tent sleep: <strong>Acampar / campamento</strong> (From <strong>Campo</strong> Open field [<em>Camp</em>]!) = <em>Camping</em>!',
        '1. Trail walk: <strong>Hiking</strong> (Brisk long country tramp/march!) / '
        '<strong>Pahaadi safar</strong> (<strong>Pahaad</strong> Mountain + Arabic <strong>Safar</strong> Journey!) = <em>Hiking</em>!<br>'
        '2. Tent sleep: <strong>Camping</strong> (Latin <em>Campus</em> Field pitch!) / '
        '<strong>Dera daalna</strong> (<strong>Dera</strong> Tent shelter + <strong>Daalna</strong> Pitch/Drop!) = <em>Camping</em>!'
    ),
    1358: (
        '1. Play activity: <strong>Juego</strong> (Latin <em>Jocus</em> Jest/Play [<em>Joke / Jocular</em>]!) = <em>Game</em>!<br>'
        '2. Head-to-head match: <strong>Partido</strong> (Split 2-side game!) | '
        '<strong>Encuentro</strong> (<strong>En-</strong> + <strong>Contra</strong> Face-to-face clash!) = <em>Match</em>!<br>'
        '3. Series championship: <strong>Torneo</strong> (From <strong>Tornar</strong> Turn/Joust [<em>Tournament</em>]!) | '
        '<strong>Campeonato</strong> (<strong>Campeón</strong> Champion!) = <em>Tournament</em>!',
        '1. Play activity: <strong>Khel</strong> (Play!) / '
        '<strong>Game</strong> (Old English <em>Gamen</em> Joy/Amusement!) = <em>Game</em>!<br>'
        '2. Head-to-head match: <strong>Match</strong> (Paired equal rival!) / '
        '<strong>Muqabla</strong> (Arabic <strong>Muqabalah</strong> Standing face-to-face!) = <em>Match</em>!<br>'
        '3. Series championship: <strong>Tournament</strong> (Knights turning in jousts — knockout rounds!) = <em>Tournament</em>!'
    ),
    1359: (
        '1. Cup goblet: <strong>Trofeo</strong> (Greek <em>Tropaion</em> Victory monument where foe turned back!) | '
        '<strong>Copa</strong> (Latin <em>Cuppa</em> Drinking bowl [<em>Cup</em>]!) = <em>Trophy</em>!<br>'
        '2. Medallion disc: <strong>Medalla</strong> (Latin <em>Metallum</em> Struck metal coin disc [<em>Medal</em>]!) = <em>Medal</em>!',
        '1. Cup goblet: <strong>Trophy</strong> (Greek <em>Tropaion</em> Victory prize!) / '
        '<strong>Cup</strong> (Latin <em>Cuppa</em> Prize vessel!) = <em>Trophy / Cup</em>!<br>'
        '2. Medallion disc: <strong>Medal</strong> (Latin <em>Metallum</em> Cast metal victory coin!) = <em>Medal</em>!'
    ),
    1360: (
        '<strong>Campeón / campeona</strong> (Latin <em>Campus</em> Arena fighter — winner of the field [<em>Champion</em>]!) | '
        '<strong>Ganador</strong> (From <strong>Ganar</strong> Earn/Win [<em>Gain</em>] + <strong>-dor</strong>!) = <em>Champion / Winner</em>!',
        '<strong>Champion</strong> (Latin <em>Campus</em> Field combat victor!) / '
        '<strong>Jeetne wala</strong> (<strong>Jeet [Tamil ஜெயம் Jeyam = Victory!]</strong> + <strong>Wala</strong> One!) = <em>Champion / Winner</em>!'
    ),
    1361: (
        '1. Team mentor trainer: <strong>Entrenador / entrenadora</strong> (<strong>En-</strong> + <strong>Tren</strong> Drag/Drill [<em>Train</em>] + <strong>-dor</strong>!) = <em>Coach</em>!<br>'
        '2. Umpire official: <strong>Árbitro</strong> (Latin <em>Arbiter</em> Witness/Judge [<em>Arbitrator</em>]!) = <em>Referee</em>!',
        '1. Team mentor trainer: <strong>Coach</strong> (Hungarian <em>Kocsi</em> Carriage carrying students forward!) / '
        '<strong>Trainer</strong> (<strong>Train</strong> Drill/Draw + <strong>-er</strong>!) = <em>Coach</em>!<br>'
        '2. Umpire official: <strong>Referee</strong> (<strong>Re-</strong> Back + <strong>Ferre</strong> Carry disputes to!) / '
        '<strong>Umpire</strong> (Old French <em>Nomper</em> Non-peer impartial 3rd judge!) = <em>Referee / Umpire</em>!'
    ),
    1362: (
        '<strong>Ejercicio</strong> (<strong>Ex-</strong> Out + <strong>Arcere</strong> Keep busy/Practice [<em>Exercise</em>]!) | '
        '<strong>Entrenamiento</strong> (<strong>Entrenar</strong> Train + <strong>-miento</strong>!) | '
        '<strong>Condición física</strong> (Physical shape!) = <em>Exercise / Fitness</em>!',
        '<strong>Exercise</strong> (<strong>Ex-</strong> Out + <strong>Arcere</strong> Work muscles!) / '
        '<strong>Kasrat</strong> (Arabic <strong>Kathrat</strong> Abounding vigorous practice!) / '
        '<strong>Fitness</strong> (<strong>Fit</strong> Well-suited shape + <strong>-ness</strong>!) = <em>Exercise / Fitness</em>!'
    ),
}
