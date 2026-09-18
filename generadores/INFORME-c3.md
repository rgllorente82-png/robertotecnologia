# Informe · 4.º de ESO · Tecnología · Tema 3 · Materiales y ciclo de vida

Rama `c3`. Sesiones **1 a 4 de 8** escritas; las otras cuatro quedan con título puesto y
marcadas como pendientes, para que la cadena de la unidad se lea entera desde el primer día.

> El encargo pedía `INFORME.md`. Lo dejo en `generadores/INFORME-c3.md` porque es donde están
> los tres anteriores (`INFORME-c4.md`, `INFORME-c5.md`, `INFORME-c6.md`) y así no se pisan
> entre unidades. Si lo prefieres en la raíz, se mueve en un segundo.

## Qué hay

| Fichero | Qué es |
|---|---|
| `4eso/Tecnologia/tema3/index.html` | La página, 205 KB, generada |
| `4eso/Tecnologia/tema3/lectura-tema3.pdf` | La lectura de aula: 30 párrafos numerados y 10 preguntas, 5 páginas |
| `generadores/c3_build.py` | El generador de la página |
| `generadores/c3_escenas.py` | Escenas de S1 (ciclo de vida) y S2 (energía incorporada) |
| `generadores/c3_escenas2.py` | Escenas de S3 (matriz de decisión) y S4 (reparar) |
| `generadores/c3_lectura.py` | La lectura |
| `generadores/c3_fotos.py` + `creditos_c3.json` | Las ocho fotos de Commons y sus créditos |
| `generadores/c3_verifica.py` | El verificador: **163 comprobaciones, 0 fallos** |
| `generadores/guion_c3.txt`, `audio/c3-materiales.mp3`, `_env_c3-materiales.json` | La voz del avatar (2 min 15 s) |
| `generadores/voz.py` | **Nuevo**: ver más abajo, no existía |

`4eso/Tecnologia/index.html` **no se ha tocado**, como pedías.

---

## La cadena de las cuatro sesiones

Cada sesión abre con un fracaso concreto y cierra abriendo la siguiente:

| | Empieza por | Falla porque | Aparece | Deja abierto |
|---|---|---|---|---|
| S1 | ¿bolsa de plástico o de tela? | contestas mirando el objeto, no su vida | ciclo de vida, unidad funcional, límites del sistema | si manda fabricar, ¿qué hay dentro del material? |
| S2 | fundir aluminio es fácil, luego hacerlo es barato | fundir cuesta 0,97 MJ y hacerlo 186 | energía incorporada, Hall-Héroult, el 95 % | ya sé la mochila, pero no puedo elegir solo por eso |
| S3 | el acero es 26 veces más rígido, luego gana | comparas a igualdad de espesor, no de trabajo | criterios en conflicto, matriz, requisitos eliminatorios | he elegido material, pero el impacto depende de cuánto dure |
| S4 | los auriculares están pegados, qué mala suerte | no es mala suerte, es una decisión con una cuenta detrás | uniones, normalización, índice de reparabilidad, derecho a reparar | (test + lo que queda de unidad) |

## Qué he cambiado de tu propuesta, y por qué

Los cuatro temas son los que pusiste. Lo que he cambiado es **por dónde se entra** y **qué calcula
la escena**:

1. **S1** — tu propuesta era «una escena con un objeto y el reparto de su impacto por etapas».
   La he hecho, pero le he añadido lo que hace que el reparto se entienda: **la gráfica del cruce**
   (en qué año pasa a pesar más usarlo que haberlo fabricado) y un deslizador de **horas al día**.
   Porque lo que decide si manda el uso o la fabricación no es el aparato: es el **ciclo de
   trabajo**. Con eso sale el resultado que más sirve para su proyecto y que no se espera nadie:
   **en el riego, la placa en reposo gasta cuarenta veces más que la bomba** (0,3 W × 24 h frente a
   3,5 W × 3 min). La casilla «se queda enchufado» da la vuelta a la conclusión delante de ellos.

2. **S2** — tu enunciado decía «reciclar aluminio ahorra el 95 % porque la electrólisis es lo caro».
   Lo he construido al revés para que lo demuestren ellos: primero calculan con física de toda la
   vida lo que cuesta **fundir** un kilo (m·cp·ΔT + m·L_f = 971 kJ), y el 186 aparece como el hueco
   que hay que explicar. El 95 % sale entonces como una división, no como un dato.

3. **S3** — aquí está el cambio grande. Una matriz de decisión con materiales **no es honesta si
   compara a igualdad de espesor**: el acero es 26 veces más rígido que el contrachapado, pero para
   una tapa que aguante lo mismo necesita 1,35 mm frente a 4,00, y aun así pesa 317 g frente a 72.
   Así que la escena **dimensiona cada candidato** con la rigidez a flexión (t ∝ (E_ref/E)^⅓) antes
   de puntuar, y de ahí salen masa, precio y energía. Además he separado **requisitos eliminatorios**
   de **criterios ponderados**, que es lo que de verdad cambia la respuesta: sin requisitos el
   contrachapado gana casi siempre; marcas «va a estar mojado» y gana otro.

4. **S4** — tu propuesta era la taxonomía de uniones más el derecho a reparar. La he mantenido,
   pero la escena no es un catálogo: es **la cuenta que decide de verdad** (tiempo × tarifa + pieza
   + riesgo, contra el 60 % del precio de uno nuevo) más un índice de reparabilidad calcado del
   francés. Así el alumno ve que el pegamento no es «malo»: es que mete minutos, y los minutos son
   euros.

Las cuatro pendientes las he titulado así, y son discutibles: **S5 Del residuo a la materia**,
**S6 De megajulios a CO₂**, **S7 Economía circular**, **S8 La memoria de impacto**.

## El proyecto del curso, que no está decidido

Ninguna sesión depende de un proyecto concreto. Donde hacía falta un ejemplo van dos o tres de los
cinco del catálogo. **Donde he tenido que elegir:**

- La escena de S1 trae **tres** aparatos: aviso de ventilación, riego y lámpara. Son los tres que
  tienen ciclos de trabajo distintos (24 h, 3 min y 3 h al día), que es lo que la escena enseña. El
  contenedor y la barrera se habrían solapado con alguno de ellos.
- Los tres botones de prioridades de S3 son **riego, lámpara y contenedor**.
- La pieza de S3 es **una tapa de 200 × 150 mm**. Hacía falta una geometría concreta para poder
  calcular espesores; es la que sirve a los cinco proyectos (carcasa, base o soporte).

Si el proyecto acaba siendo uno solo, lo único que habría que retocar son esos rótulos.

## Los datos: qué está comprobado y qué no

**Comprobado hoy (18-sep-2026) contra fuente:**

- **Aluminio: 186 MJ/kg primario y 8,3 MJ/kg reciclado** → International Aluminium Institute, datos
  de 2019, de la mina a la fundición. El ahorro sale **95,5 %**, que es exactamente el titular del
  95 %. Es el único par de la unidad con fuente de primera mano, y por eso el titular se apoya en él.
- **Constantes físicas** (T_f, c_p, L_f de aluminio, acero, cobre): comprobados los calores latentes
  dividiendo el molar entre el peso molar (Al 10,71/26,98 = 397 J/g ✓, Fe 13,81/55,85 = 247 ✓,
  Cu 13,26/63,55 = 209 ✓).
- **Cártel Phoebus**: 23-dic-1924, Ginebra, Osram/Philips/Compagnie des Lampes/GE, 1.000 h frente a
  las 1.500-2.000 de entonces, multas en francos suizos, disuelto en 1939.
- **Punta del Monumento a Washington**: 1884, ~2,85 kg (100 onzas), la mayor pieza de aluminio
  fundida hasta entonces, 225 $, precio del aluminio comparable al de la plata.
- **Índice de reparabilidad francés**: obligatorio desde el 1-ene-2021, nota /10, cinco criterios de
  dos puntos, cinco familias de producto; desde 2025 lo sustituye el índice de durabilidad.
- **Directiva (UE) 2024/1799**: 13-jun-2024, plazo de transposición 31-jul-2026, España llegó tarde.
- **Reglamento (UE) 2023/1542**: baterías extraíbles y sustituibles por el usuario desde el
  18-feb-2027, prohíbe tornillos propietarios y adhesivos con calor o disolvente, repuestos 7 años.
- **Estudio danés de bolsas** (Danish EPA, 2018, Environmental Project n.º 1985): algodón
  convencional, 52 usos para empatar en cambio climático y hasta 7.100 mirando todos los
  indicadores. En la página va **con su pega dicha**: es un estudio danés que da por hecho que la
  bolsa acaba incinerada y no cuenta el abandono en el medio.

**⚠️ NO comprobado contra la fuente, y conviene que lo mires:**

- **Las demás energías incorporadas** (acero 25, cobre 60, vidrio 15, PET 84, PLA 50, madera 10,
  contrachapado 15, cartón 25, hormigón 1,1 MJ/kg) las he puesto como **valor central del rango de
  Ashby, *Materials and the Environment***, y así van rotuladas en la página. Son los valores que
  se citan siempre en esas tablas, pero **no he abierto el libro ni el CES**. Si esas cifras van a
  quedar publicadas, merece la pena contrastarlas con el libro o con la base ICE (Hammond & Jones)
  y ajustar. La página ya avisa de que son órdenes de magnitud y que cada cifra se mueve un 20 %.
- **Intensidad energética del transporte** (barco 0,16 · tren 0,23 · camión 0,94 · avión
  8,3 MJ/(t·km)): misma situación, son las de la tabla de transporte de Ashby y no las he
  contrastado. La conclusión que sostienen —el avión gasta ~52 veces más que el barco— es robusta
  aunque los números bailen.
- **Módulo de Young del contrachapado (8 GPa) y del PLA impreso (3,0 GPa)**: son los que más varían.
  El contrachapado depende de la dirección de las chapas (7-10 GPa) y el PLA impreso, del relleno y
  de la orientación de las capas (2,5-3,5). Está dicho en la cabecera del generador; **no está
  dicho dentro de la página** y quizá debería.
- **Coeficiente de paso a energía primaria de la electricidad**: uso **2,0**, redondeo del 1,954 del
  documento reconocido del RITE de **2016**. Con el mix de hoy sale más bajo, así que la escena
  **exagera la etapa de uso**. Lo digo en la página, pero si quieres un número actual hay que ir al
  documento vigente.

**Sin fuente publicada, y por eso es un deslizador:**

- **La mochila de la electrónica** (placa Arduino + sensor + cableado). **No hay ACV publicado de
  una placa Arduino.** En vez de inventarme un número, lo he puesto como deslizador de 20 a 200 MJ
  con el rótulo «no hay dato publicado: muévelo», y la sesión usa eso para enseñar **análisis de
  sensibilidad**: con 60 MJ el cruce cae en el año 3 y manda el uso; con 200 MJ se va al año 9 y
  manda la fabricación. Me parece la salida honesta, pero **es una decisión mía y la puedes
  revocar**: si prefieres un valor fijo, hay que buscarle fuente.

**Criterio nuestro, rotulado como tal dentro de la página:**

- Las puntuaciones de 0 a 10 de S3 (aguanta un golpe, se trabaja en el taller, aguanta el agua,
  aguanta el calor): experiencia de taller, van con asterisco y con su nota al pie.
- Los tiempos de desmontaje por tipo de unión de S4 (1,2 min un tornillo, 16 min un pegado…): del
  orden de lo que dan los estudios de tiempo de desmontaje, pero no son ninguno de ellos.
- El umbral del **60 %** por encima del cual nadie repara: regla del sector, no norma.
- El **25 %** del precio que cuesta destrozar algo al abrir, el **70 %** que se recupera reciclando
  bien, el **35 %** de rendimiento del horno, los **0,5 MJ/kg** de recogida y tratamiento.
- El **índice de reparabilidad** de la escena: cuatro sumandos, calcado del francés pero
  simplificado. La página dice expresamente que **no es el oficial**.

## Fotos y vídeos

**Ocho fotos de Wikimedia Commons.** Licencia comprobada por la API (`c3_fotos.py` la escribe en
`creditos_c3.json`, y la página la lee de ahí: el crédito no se teclea a mano). **Las ocho las he
abierto y mirado una a una:**

| Clave | Qué se ve de verdad | Licencia |
|---|---|---|
| `c3-portacontenedores` | El *Maersk Hanoi* cargando en Koper, seis grúas pórtico | CC BY-SA 4.0 |
| `c3-agbogbloshie` | Gente quemando cable entre humo espeso, Acra 2019 | CC BY-SA 4.0 |
| `c3-bauxita` | Cantera de bauxita anegada en Otranto, roca roja y lago verde | CC BY-SA 4.0 |
| `c3-electrolisis` | Dos operarios sobre la fila de cubas de Bratsk | CC BY 2.0 |
| `c3-chatarra` | Cubos prensados de chatarra de aluminio en un contenedor | CC BY-SA 3.0 |
| `c3-monobloc` | La silla blanca de plástico, con la marca de inyección visible | CC BY 2.0 |
| `c3-pentalobular` | Tres puntas pentalobulares (P2, P5, P6) al microscopio | CC BY-SA 4.0 |
| `c3-repair-cafe` | Un *repair café*: aspirador, lámpara, polímetro, destornilladores | CC BY-SA 3.0 |

Dos avisos sobre estas fotos:

- **Agbogbloshie.** Es la más dura de las ocho y es a propósito: es la quinta etapa del ciclo de
  vida. El pie dice **qué está pasando y por qué** (queman el plástico para sacar el cobre, que vale
  60 MJ/kg y se paga) y **que el asentamiento fue desalojado y demolido en julio de 2021**, para no
  presentarlo en presente ni repetir el cliché de «el mayor vertedero electrónico del mundo», que
  está discutido. Aun así, **mírala antes de darla en clase y decide tú**.
- **Bratsk.** Es una nave de cubas de verdad y abajo se ven los cierres numerados, pero el
  protagonista de la foto son los dos operarios, no las cubas. Es lo mejor que hay en Commons con
  licencia libre; si encuentras una de la línea de cubas, mejora.

**Dos vídeos**, con **título y canal comprobados por oEmbed hoy**:

- S1 · `y3_KltoL5l8` — «Análisis del Ciclo de Vida del Producto (ACV) según ISO», canal **TuProfeDeFP**.
- S2 · `tJePkigCQ_U` — «Proceso Hall-Héroult / Electrólisis de la alúmina para obtener aluminio»,
  canal **Questions Of Science**.

⚠️ **Nadie los ha visto enteros.** oEmbed dice quién los firma y cómo se llaman; no dice si son
buenos ni si el minuto 4 dice una barbaridad. Hay que verlos antes de proyectarlos.

No he puesto vídeo en S3 ni en S4. En S4 lo natural sería el documental **«Comprar, tirar, comprar»**
(Cosima Dannoritzer, 2010, TVE), que está citado en el texto por su nombre, pero no he encontrado un
enlace estable que pudiera comprobar, así que **no lo he empotrado**.

## La voz: `voz.py` no existía

El encargo daba por hecho `generadores/voz.py`, y **no está en el repositorio** (ni en `HEAD` ni en
el historial), aunque sí están los mp3 y los `_env_*.json` de las unidades anteriores. Lo he
reescrito a partir del formato que consume `avatar_flat.componente()`:

- síntesis con **piper**, modelo `es_ES-davefx-medium` (está en la caché de HuggingFace de la
  máquina), todo local y a coste cero;
- mp3 a 48 kbps mono, que es el mismo bitrate que los de c4/c5/c6;
- envolvente de una muestra cada 66 ms, valor eficaz normalizado contra el percentil 98 (no contra
  el máximo, para que un chasquido no deje la boca a medio abrir toda la locución).

Salen **135,3 s y 2.051 muestras**, igual de largo que el de la U5 (134 s, 2.032). ⚠️ **Si aparece el
`voz.py` original, compara los dos antes de quedarte con este**: puede que la envolvente original
se calcule de otra forma.

## El verificador

`c3_verifica.py`: **163 comprobaciones, 0 fallos**. Abre la página en Chromium de verdad y:

- rehace **en Python y a partir de la definición** las cuatro cuentas (ciclo de vida, fusión y
  mezcla, matriz, coste de reparación) y las compara con lo que se lee en pantalla, caso por caso;
- pulsa **86 controles** de escena, sesión por sesión, y comprueba que no hay errores de página;
- contesta el test entero **mal** y luego entero **bien** (0 de 10 y 10 de 10);
- comprueba que los 8 ficheros de foto existen y son JPEG (no vale `naturalWidth`: van con
  `loading="lazy"` y tres sesiones están ocultas al cargar);
- comprueba que **ningún rótulo se sale de su lienzo**, en cada estado de cada escena.

**Un hallazgo que afecta a toda la web, no solo a esta unidad.** La página pide Roboto Mono a
Google Fonts. Si ese dominio está cortado en el centro —o no hay internet—, cae en la tipografía de
máquina del sistema, que es **un 28 % más ancha**, y los rótulos largos de los SVG se recortan. El
verificador **bloquea Google Fonts a propósito** y comprueba el caso malo. Con eso cacé tres
rótulos que se salían y ya están arreglados. **Merece la pena pasar esa misma comprobación por las
unidades de 2.º**, porque el problema es del molde común.

## Dudas y cosas que debería mirar un humano

1. **Las cifras de Ashby.** Es lo único importante que no he podido contrastar contra la fuente. Ver
   arriba.
2. **La mochila de la electrónica como deslizador.** ¿Te convence la solución, o prefieres un valor
   fijo con fuente?
3. **En S3 gana casi siempre el contrachapado.** Es el resultado correcto (para una tapa a flexión,
   la madera es dificilísima de batir) y lo he convertido en lección explícita: *«el contrachapado
   gana casi siempre… hasta que le pones agua o fuego delante»*. Pero si en clase prefieres que la
   matriz reparta más, habría que meter un candidato que la discuta en seco, por ejemplo un
   **sándwich de cartón** o el **aluminio en perfil** en vez de en chapa.
4. **La foto de Agbogbloshie**, por lo dicho arriba.
5. **La transposición española de la Directiva 2024/1799 está en marcha.** El párrafo 27 de la
   lectura dice «España llegó tarde a esa fecha y sigue tramitándola mientras leéis esto». Si se
   aprueba la Ley de Consumo Sostenible, ese párrafo caduca: hay que revisarlo cada curso.
6. **`PROYECTOS.md` se contradice.** La sección de decisiones dice, con fecha 17-sep-2026, que en
   4.º se usa **Arduino**; pero la línea de coste de los candidatos sigue diciendo «con micro:bit
   reutilizable del centro» y las fichas 2 y 3 hablan de la pantalla y de la radio del micro:bit.
   No lo he tocado, pero conviene arreglarlo antes de que confunda a alguien.
7. **Los títulos de las cuatro sesiones pendientes** son mi propuesta, no una decisión. Sobre todo
   la S6 («De megajulios a CO₂»): esa sesión necesita factores de emisión actualizados y esos sí
   que caducan cada año.
8. El test va en la **sesión 4**, que es la última escrita, como en la U5. Cuando se escriban las
   ocho habrá que decidir si se queda ahí, se mueve a la 8 o hay dos.
