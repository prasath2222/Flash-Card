import re, json

split1_raw = """
1.  I — Hindi: Main | Spanish: Yo
2.  YOU — 1. Informal: Hindi: Tum / Tu | Spanish: Tú | 2. Formal / Plural: Hindi: Aap / Aap log | Spanish: Usted / Ustedes
3.  HE — Hindi: Woh | Spanish: Él
4.  SHE — Hindi: Woh | Spanish: Ella
5.  IT — 1. Object: Hindi: Yeh / Woh / Ise | Spanish: Lo / La / Esto
6.  WE — Hindi: Hum / Hum log | Spanish: Nosotros / Nosotras
7.  THEY — Hindi: Woh log | Spanish: Ellos / Ellas
8.  ME — Hindi: Mujhe / Mujhko | Spanish: Me / Mí
9.  HIM — Hindi: Use / Usko | Spanish: Lo / Le
10. HER — 1. Object: Hindi: Use / Usko | Spanish: La / Le | 2. Possessive: Hindi: Uski / Uska | Spanish: Su / Sus
11. US — Hindi: Humein / Humko | Spanish: Nos
12. THEM — Hindi: Unhein / Unko | Spanish: Los / Las / Les
13. MYSELF — Hindi: Main khud / Apne aap | Spanish: Yo mismo / Me
14. YOURSELF — Hindi: Tum khud / Aap khud | Spanish: Tú mismo / Te
15. HIMSELF — Hindi: Woh khud / Apne aap | Spanish: Él mismo / Se
16. HERSELF — Hindi: Woh khud / Apne aap | Spanish: Ella misma / Se
17. ITSELF — Hindi: Apne aap / Khud | Spanish: Por sí mismo / Se
18. OURSELVES — Hindi: Hum khud | Spanish: Nosotros mismos / Nos
19. YOURSELVES — Hindi: Aap log khud | Spanish: Ustedes mismos / Se
20. THEMSELVES — Hindi: Woh log khud | Spanish: Ellos mismos / Se
21. MY — Hindi: Mera / Meri / Mere | Spanish: Mi / Mis
22. YOUR — 1. Informal: Hindi: Tumhara / Tumhari | Spanish: Tu / Tus | 2. Formal: Hindi: Aapka / Aapki | Spanish: Su / Sus
23. HIS — Hindi: Uska / Uski / Uske | Spanish: Su / Sus
24. OUR — Hindi: Hamara / Hamari / Hamare | Spanish: Nuestro / Nuestra
25. THEIR — Hindi: Unka / Unki / Unke | Spanish: Su / Sus
26. ITS — Hindi: Iska / Iski / Uska | Spanish: Su / Sus
27. MINE — Hindi: Mera / Meri | Spanish: Mío / Mía
28. YOURS — Hindi: Tumhara / Aapka | Spanish: Tuyo / Suya
29. HERS — Hindi: Uska / Uski | Spanish: Suyo / Suya
30. OURS — Hindi: Hamara / Hamari | Spanish: Nuestro / Nuestra
31. THEIRS — Hindi: Unka / Unki | Spanish: Suyo / Suya
32. WHOSE — Hindi: Kiska / Kiski / Kiske | Spanish: De quién
33. THIS — Hindi: Yeh / Is | Spanish: Este / Esta / Esto
34. THAT — Hindi: Woh / Us | Spanish: Ese / Esa / Eso / Aquel
35. THESE — Hindi: Yeh / Yeh sab | Spanish: Estos / Estas
36. THOSE — Hindi: Woh / Woh sab | Spanish: Esos / Esas
37. SOMEONE — Hindi: Koi / Kisi ne | Spanish: Alguien
38. ANY — Hindi: Koi bhi / Kuch bhi | Spanish: Cualquier / Algún / Ningún
39. SOMETHING — Hindi: Kuch / Koi cheez | Spanish: Algo
40. SOMEWHERE — Hindi: Kahin / Kahin par | Spanish: En algún lugar
41. ANYONE — Hindi: Koi bhi | Spanish: Cualquiera / Alguien
42. ANYTHING — Hindi: Kuch bhi | Spanish: Cualquier cosa / Nada (in negatives)
43. ANYWHERE — Hindi: Kahin bhi | Spanish: En cualquier lugar
44. EVERYONE — Hindi: Sab / Sab log | Spanish: Todos / Todo el mundo
45. EVERYTHING — Hindi: Sab kuch | Spanish: Todo
46. EVERYWHERE — Hindi: Har jagah | Spanish: En todas partes / Por todos lados
47. NO ONE — Hindi: Koi nahi | Spanish: Nadie
48. NOTHING — Hindi: Kuch nahi | Spanish: Nada
49. NOWHERE — Hindi: Kahin nahi | Spanish: En ninguna parte
50. A — Hindi: Ek | Spanish: Un / Una
51. THE — Hindi: Woh | Spanish: El / La / Los / Las
52. ALL — Hindi: Sab / Saara / Sabhi | Spanish: Todo / Todos
53. EVERY — Hindi: Har / Har ek | Spanish: Cada
54. EACH — Hindi: Har ek / Ek-ek | Spanish: Cada uno / Cada
55. BOTH — Hindi: Dono | Spanish: Ambos / Los dos
56. EITHER — 1. One or other: Hindi: Dono mein se koi ek | Spanish: Cualquiera de los dos | 2. Negative agreement: Hindi: Bhi nahi | Spanish: Tampoco
57. NEITHER — Hindi: Dono mein se koi nahi | Spanish: Ninguno de los dos / Ni
58. SOME — Hindi: Kuch / Thoda | Spanish: Algunos / Un poco de
59. ENOUGH — Hindi: Kaafi / Bas | Spanish: Suficiente / Bastante
60. NONE — Hindi: Ek bhi nahi / Koi nahi | Spanish: Ninguno / Nada
61. SELF — Hindi: Khud / Apne aap | Spanish: Mismo / Auto-
62. OTHER — Hindi: Doosra / Aur | Spanish: Otro / Otra
63. ANOTHER — Hindi: Ek aur / Doosra | Spanish: Otro más / Otra
64. SUCH — Hindi: Aisa / Is tarah ka | Spanish: Tal / Tan / Así
65. SAME — Hindi: Same / Wahi | Spanish: Mismo / Igual
66. DIFFERENT — Hindi: Alag / Different | Spanish: Diferente / Distinto
67. SEVERAL — Hindi: Kai / Kayi saare | Spanish: Varios / Varias
68. MANY — Hindi: Bohot saare / Kai | Spanish: Muchos / Muchas
69. MUCH — Hindi: Zyada / Bohot | Spanish: Mucho / Mucha
70. FEW — Hindi: Kuch / Thode se | Spanish: Pocos / Pocas
71. LITTLE — 1. Small size: Hindi: Chhota | Spanish: Pequeño | 2. Small amount: Hindi: Thoda / Kam | Spanish: Poco
72. WHAT — Hindi: Kya | Spanish: Qué
73. WHERE — Hindi: Kahan | Spanish: Dónde
74. WHEN — Hindi: Kab (question) / Jab (condition) | Spanish: Cuándo
75. WHY — Hindi: Kyun | Spanish: Por qué
76. WHO — Hindi: Kaun | Spanish: Quién
77. WHOM — Hindi: Kisse / Kisko | Spanish: A quién
78. WHICH — Hindi: Kaun sa / Kaun si | Spanish: Cuál / Qué
79. HOW — Hindi: Kaise | Spanish: Cómo
80. HOW MUCH — Hindi: Kitna / Kitne ka (price) | Spanish: Cuánto
81. HOW MANY — Hindi: Kitne | Spanish: Cuántos / Cuántas
82. HOW LONG — Hindi: Kitni der / Kitna samay | Spanish: Cuánto tiempo
83. HOW FAR — Hindi: Kitni door | Spanish: Qué tan lejos / A qué distancia
84. HOW OFTEN — Hindi: Kitni baar / Kab kab | Spanish: Cada cuánto / Con qué frecuencia
85. WHAT KIND — Hindi: Kaisa / Kis tarah ka | Spanish: Qué tipo de / Qué clase de
86. WHICH ONE — Hindi: Kaun sa wala | Spanish: Cuál
87. BE — 1. Permanent/Identity: Hindi: Hona | Spanish: Ser | 2. Location/Condition: Hindi: Rehna / Hona | Spanish: Estar
88. HAVE — Hindi: Paas hona / Rakhna | Spanish: Tener / Haber (auxiliary)
89. DO — Hindi: Karna | Spanish: Hacer
90. CAN — 1. Ability: Hindi: Sakna | Spanish: Poder | 2. Container: Hindi: Can / Dibba | Spanish: Lata
91. COULD — 1. Past ability: Hindi: Sakta tha | Spanish: Podía | 2. Polite request: Hindi: Sakte hain | Spanish: Podría / Podrías
92. WILL — 1. Future marker: Hindi: -ega / -egi / -enge | Spanish: (future tense) | 2. Legal paper: Hindi: Vasiyat | Spanish: Testamento
93. WOULD — 1. Polite desire: Hindi: Chahenge | Spanish: Me gustaría / Quisiera | 2. Past routine: Hindi: Kiya karte the | Spanish: Solía
94. SHALL — Hindi: Karein kya / -enge | Spanish: Deberíamos / (future)
95. SHOULD — Hindi: Chahiye | Spanish: Debería / Deberías
96. MUST — Hindi: Zaroor chahiye / Karna hi hoga | Spanish: Deber / Tener que
97. MAY — 1. Possibility: Hindi: Ho sakta hai / Shayad | Spanish: Puede que / Quizás | 2. Permission: Hindi: Kya main ... sakta hoon | Spanish: Poder
98. MIGHT — Hindi: Shayad hi / Ho sakta hai | Spanish: Podría / Puede que
99. NEED — Hindi: Zaroorat hona / Chahiye | Spanish: Necesitar
100. USED TO — Hindi: Kiya karta tha / Aadat thi | Spanish: Solía
101. OUGHT TO — Hindi: Chahiye (moral duty) | Spanish: Debería
102. WHATEVER — Hindi: Jo kuch bhi / Kuch bhi | Spanish: Lo que sea / Cualquier cosa que
103. WHENEVER — Hindi: Jab bhi | Spanish: Cuando sea / Cada vez que
104. IN — Hindi: Mein / Ke andar | Spanish: En / Dentro de
105. ON — Hindi: Par / Ke oopar | Spanish: Sobre / En / Encima de
106. AT — Hindi: Par / Mein (location/time) | Spanish: En / A
107. TO — Hindi: Ko / Ki taraf | Spanish: A / Hacia / Para
108. FROM — Hindi: Se | Spanish: De / Desde
109. FOR — Hindi: Ke liye | Spanish: Para / Por
110. OF — Hindi: Ka / Ki / Ke | Spanish: De
111. WITH — Hindi: Ke saath | Spanish: Con
112. WITHOUT — Hindi: Ke bina | Spanish: Sin
113. BY — Hindi: Ke zariye / Se / Tak (time limit) | Spanish: Por / En / Para (deadline)
114. ABOUT — Hindi: Ke baare mein / Lagbhag (approx) | Spanish: Sobre / De / Alrededor de
115. INTO — Hindi: Ke andar (motion) | Spanish: En / Dentro de
116. OUT OF — Hindi: Se baahar | Spanish: Fuera de
117. UP — Hindi: Oopar | Spanish: Arriba
118. DOWN — Hindi: Neeche | Spanish: Abajo
119. OVER — Hindi: Ke oopar se / Khatam (finished) | Spanish: Por encima de / Terminado
120. UNDER — Hindi: Ke neeche | Spanish: Debajo de / Bajo
121. ABOVE — Hindi: Ke oopar | Spanish: Encima de / Por encima de
122. BELOW — Hindi: Ke neeche | Spanish: Debajo de / Por debajo de
123. BETWEEN — Hindi: Ke beech mein (two items) | Spanish: Entre
124. AMONG — Hindi: Ke beech mein (three or more) | Spanish: Entre / En medio de
125. THROUGH — Hindi: Ke zariye / Mein se ho kar | Spanish: A través de / Por
126. ACROSS — Hindi: Ke paar | Spanish: Al outro lado de / A través de
127. ALONG — Hindi: Ke kinaare / Saath-saath | Spanish: A lo largo de / Por
128. AROUND — Hindi: Chaaron taraf / Lagbhag | Spanish: Alrededor de / Cerca de
129. BEHIND — Hindi: Ke peeche | Spanish: Detrás de
130. IN FRONT OF — Hindi: Ke saamne | Spanish: Delante de / Frente a
131. BESIDE — Hindi: Ke bagal mein / Paas | Spanish: Al lado de / Junto a
132. NEAR — Hindi: Paas / Aas-paas | Spanish: Cerca de
133. FAR — Hindi: Door | Spanish: Lejos
134. INSIDE — Hindi: Andar / Ke andar | Spanish: Dentro / Adentro
135. OUTSIDE — Hindi: Baahar / Ke baahar | Spanish: Fuera / Afuera
136. WITHIN — Hindi: Ke andar (time/limit) | Spanish: Dentro de
137. BEYOND — Hindi: Ke pare / Us paar | Spanish: Más allá de
138. TOWARD — Hindi: Ki taraf | Spanish: Hacia
139. AGAINST — Hindi: Ke khilaaf / Ke viruddh | Spanish: Contra / En contra de
140. BEFORE — Hindi: Se pehle | Spanish: Antes de
141. AFTER — Hindi: Ke baad | Spanish: Después de
142. DURING — Hindi: Ke dauran | Spanish: Durante
143. SINCE — 1. Time: Hindi: Tab se / Se | Spanish: Desde | 2. Reason: Hindi: Kyunki | Spanish: Ya que / Puesto que
144. UNTIL — Hindi: Jab tak / Tak | Spanish: Hasta
145. AGO — Hindi: Pehle | Spanish: Hace
146. DESPITE — Hindi: Ke bawajood | Spanish: A pesar de
147. EXCEPT — Hindi: Ko chhodkar / Ke alawa | Spanish: Excepto / Menos / Salvo
148. INSTEAD OF — Hindi: Ke bajaay | Spanish: En lugar de / En vez de
149. ACCORDING TO — Hindi: Ke mutabiq / Ke hisaab se | Spanish: Según
150. BECAUSE OF — Hindi: Ki wajah se | Spanish: Debido a / Por culpa de
151. AND — Hindi: Aur | Spanish: Y / E
152. OR — Hindi: Ya | Spanish: O / U
153. BUT — Hindi: Lekin / Par / Magar | Spanish: Pero / Sino
154. SO — 1. Therefore: Hindi: Isliye / Toh | Spanish: Así que / Por lo tanto | 2. Degree: Hindi: Itna | Spanish: Tan
155. BECAUSE — Hindi: Kyunki | Spanish: Porque
156. IF — Hindi: Agar | Spanish: Si
157. UNLESS — Hindi: Jab tak na / Agar nahi | Spanish: A menos que
158. ALTHOUGH — Hindi: Haalaanki / Bhale hi | Spanish: Aunque
159. WHILE — Hindi: Jabki / Us waqt | Spanish: Mientras
160. WHETHER — Hindi: Chahe / Ki kya | Spanish: Si
161. AS — 1. Manner: Hindi: Jaise | Spanish: Como | 2. Reason: Hindi: Kyunki | Spanish: Ya que
162. THAN — Hindi: Se (comparisons) | Spanish: Que / De
163. WHEREAS — Hindi: Jabki | Spanish: Mientras que
164. HOWEVER — Hindi: Lekin / Phir bhi | Spanish: Sin embargo
165. THEREFORE — Hindi: Isiliye | Spanish: Por lo tanto / Por eso
166. MOREOVER — Hindi: Iske alawa | Spanish: Además
167. OTHERWISE — Hindi: Warna | Spanish: Si no / De lo contrario
168. MEANWHILE — Hindi: Is dauran / Tab tak | Spanish: Mientras tanto
169. INSTEAD — Hindi: Iske bajaay | Spanish: En su lugar / En cambio
170. BESIDES — Hindi: Waise bhi / Ke alawa | Spanish: Además / Aparte de
171. THUS — Hindi: Is tarah / Isiliye | Spanish: Así / Por lo tanto
172. FOR EXAMPLE — Hindi: Jaise ki / Udaharan ke liye | Spanish: Por ejemplo
173. IN FACT — Hindi: Asal mein / Sach toh yeh hai | Spanish: De hecho / En realidad
174. ALWAYS — Hindi: Hamesha | Spanish: Siempre
175. USUALLY — Hindi: Aam taur par | Spanish: Normalmente / Por lo general
176. OFTEN — Hindi: Aksar / Baar-baar | Spanish: A menudo / Frecuentemente
177. SOMETIMES — Hindi: Kabhi-kabhi | Spanish: A veces
178. OCCASIONALLY — Hindi: Kabhi-kabaar | Spanish: De vez en cuando
179. RARELY — Hindi: Bohot kam / Shayad hi kabhi | Spanish: Rara vez / Casi nunca
180. NEVER — Hindi: Kabhi nahi | Spanish: Nunca / Jamás
181. EVER — Hindi: Kabhi | Spanish: Alguna vez / Jamás
182. NOW — Hindi: Abhi / Ab | Spanish: Ahora
183. THEN — 1. At that time: Hindi: Tab | Spanish: Entonces | 2. Next: Hindi: Phir | Spanish: Luego
184. TODAY — Hindi: Aaj | Spanish: Hoy
185. TOMORROW — Hindi: Kal (future) | Spanish: Mañana
186. YESTERDAY — Hindi: Kal (past) | Spanish: Ayer
187. TONIGHT — Hindi: Aaj raat | Spanish: Esta noche
188. SOON — Hindi: Jaldi / Jaldi hi | Spanish: Pronto
189. ALREADY — Hindi: Pehle se hi | Spanish: Ya
190. STILL — Hindi: Abhi bhi | Spanish: Todavía / Aún
191. EARLY — Hindi: Jaldi | Spanish: Temprano
192. LATE — Hindi: Der / Deri se | Spanish: Tarde
193. SUDDENLY — Hindi: Achanak | Spanish: De repente
194. RECENTLY — Hindi: Haal hi mein | Spanish: Recientemente / Hace poco
195. IMMEDIATELY — Hindi: Turant / Abhi ke abhi | Spanish: Inmediatamente / Enseguida
196. FINALLY — Hindi: Aakhirkaar | Spanish: Finalmente / Por fin
197. EVENTUALLY — Hindi: Aage chal kar / Aakhir mein | Spanish: Con el tiempo / Al final
198. AGAIN — Hindi: Phir se / Dobaara | Spanish: Otra vez / De nuevo
199. DAILY — Hindi: Rozana / Har roz | Spanish: Diariamente / A diario
200. WEEKLY — Hindi: Har hafte | Spanish: Semanalmente
201. MONTHLY — Hindi: Har mahine | Spanish: Mensualmente
202. YEARLY — Hindi: Har saal / Saalaana | Spanish: Anualmente / Al año
203. HERE — Hindi: Yahan / Idhar | Spanish: Aquí / Acá
204. THERE — Hindi: Wahan / Udhar | Spanish: Allí / Ahí / Allá
205. AHEAD — Hindi: Aage | Spanish: Adelante / Delante
206. FORWARD — Hindi: Aage ki taraf | Spanish: Hacia adelante
207. BACKWARD — Hindi: Peeche ki taraf | Spanish: Hacia atrás
208. UPSTAIRS — Hindi: Oopar / Seedhiyon ke oopar | Spanish: Arriba / En el piso de arriba
209. DOWNSTAIRS — Hindi: Neeche / Seedhiyon ke neeche | Spanish: Abajo / En la planta baja
210. MORE — Hindi: Aur / Zyada | Spanish: Más
211. MOST — Hindi: Sabse zyada / Zyadatar | Spanish: La mayoría / El más
212. LESS — Hindi: Kam | Spanish: Menos
213. LEAST — Hindi: Sabse kam | Spanish: El menos / Lo mínimo
214. ONLY — Hindi: Sirf / Bas | Spanish: Solo / Solamente
215. ALMOST — Hindi: Lagbhag / Bas hone hi wala | Spanish: Casi
216. QUITE — Hindi: Kaafi | Spanish: Bastante
217. RATHER — Hindi: Kaafi / Balki | Spanish: Más bien / Bastante
218. VERY — Hindi: Bohot | Spanish: Muy
219. TOO — 1. Also: Hindi: Bhi | Spanish: También | 2. Excess: Hindi: Bohot zyada | Spanish: Demasiado
220. EXTREMELY — Hindi: Behad / Bohot hi zyada | Spanish: Extremadamente
221. REALLY — Hindi: Sach mein / Asal mein | Spanish: Realmente / De verdad
222. ESPECIALLY — Hindi: Khaaskar | Spanish: Especialmente / Sobre todo
223. JUST — 1. Only: Hindi: Sirf / Bas | Spanish: Solo | 2. Recently: Hindi: Abhi abhi | Spanish: Acabar de (+ inf) | 3. Fair: Hindi: Sahi / Nyaay-poorna | Spanish: Justo
224. EVEN — Hindi: Yahan tak ki / Bhi | Spanish: Incluso / Hasta
225. ALSO — Hindi: Bhi | Spanish: También
226. YES — Hindi: Haan / Ji haan | Spanish: Sí
227. NO — Hindi: Nahi / Na | Spanish: No
228. NOT — Hindi: Nahi | Spanish: No
229. MAYBE — Hindi: Shayad | Spanish: Tal vez / Quizás
230. PROBABLY — Hindi: Shayad / Pakka hi lagbhag | Spanish: Probablemente
231. DEFINITELY — Hindi: Pakka / Zaroor | Spanish: Definitivamente / Sin duda
232. ACTUALLY — Hindi: Asal mein / Sach mein | Spanish: En realidad / De hecho
233. TRULY — Hindi: Sachmuch / Dil se | Spanish: Verdaderamente / Realmente
"""

def parse_split1():
    entries = {}
    for line in split1_raw.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        m = re.match(r"^\d+\.\s+([A-Z0-9\s\(\)\-\'\"]+?)\s+[—\-]\s+(.*)$", line)
        if not m:
            continue
        word = m.group(1).strip()
        content = m.group(2).strip()
        
        # Check if multi-sense (e.g. 1. ... | 2. ...)
        if re.match(r"^1\.\s+", content):
            # parse senses
            # Senses like: 1. Informal: Hindi: Tum / Tu | Spanish: Tú | 2. Formal / Plural: Hindi: Aap / Aap log | Spanish: Usted / Ustedes
            # or: 1. Object: Hindi: Yeh / Woh / Ise | Spanish: Lo / La / Esto
            senses = re.split(r"\s*\|\s*(?=\d+\.\s+)", content)
            hi_parts = []
            es_parts = []
            for s in senses:
                sm = re.match(r"^(\d+\.\s*[^:]*?):\s*Hindi:\s*([^|]+)\s*\|\s*Spanish:\s*(.+)$", s.strip())
                if sm:
                    label = sm.group(1).strip()
                    h = sm.group(2).strip()
                    e = sm.group(3).strip()
                    hi_parts.append(f"{label}: {h}")
                    es_parts.append(f"{label}: {e}")
                else:
                    # fallback
                    hi_m = re.search(r"Hindi:\s*([^|]+)", s)
                    es_m = re.search(r"Spanish:\s*([^|]+)", s)
                    if hi_m and es_m:
                        hi_parts.append(hi_m.group(1).strip())
                        es_parts.append(es_m.group(1).strip())
            hi_val = " | ".join(hi_parts)
            es_val = " | ".join(es_parts)
        else:
            # Single sense: Hindi: Main | Spanish: Yo
            hi_m = re.search(r"Hindi:\s*([^|]+)", content)
            es_m = re.search(r"Spanish:\s*(.+)$", content)
            hi_val = hi_m.group(1).strip() if hi_m else ""
            es_val = es_m.group(1).strip() if es_m else ""

        entries[word] = {"hi": hi_val, "es": es_val}
    return entries

if __name__ == "__main__":
    entries = parse_split1()
    print("Parsed entries:", len(entries))
    for k in list(entries.keys())[:10]:
        print(f"[{k}] => hi: {entries[k]['hi']} | es: {entries[k]['es']}")
    for k in ["YOU", "IT", "HER", "EITHER", "BE", "CAN", "WILL", "JUST"]:
        if k in entries:
            print(f"Multi-sense check [{k}] => hi: {entries[k]['hi']} | es: {entries[k]['es']}")
