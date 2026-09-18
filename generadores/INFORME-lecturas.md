# Las cuatro lecturas de aula que faltaban en 2.º de ESO

Rama `lecturas`. Temas 2, 3, 4 y 10. Todo generado, comprobado leyendo los PDF
(no la lista de Python) y mirado con los ojos página a página.

---

## 1. Qué hay

| Fichero | Qué es |
|---|---|
| `2eso/TyD/tema2/lectura-tema2.pdf` | «Dibujar lo que todavía no existe» · 30 párrafos + 10 preguntas · 4 pág. |
| `2eso/TyD/tema3/lectura-tema3.pdf` | «De dónde sale un lápiz» · 30 + 10 · 4 pág. |
| `2eso/TyD/tema4/lectura-tema4.pdf` | «Por qué se caen los puentes» · 30 + 10 · 4 pág. |
| `2eso/TyD/tema10/lectura-tema10.pdf` | «El primer programa se escribió para una máquina que no existía» · 30 + 10 · 4 pág. |
| `generadores/u2_lectura.py` · `u3_lectura.py` · `u4_lectura.py` · `u10_lectura.py` | El texto de cada una |
| `generadores/comprueba_lecturas.py` | Comprueba **las diez** lecturas abriendo el PDF |

Reproducir todo:

```
~/venv/bin/python generadores/u2_lectura.py
~/venv/bin/python generadores/u3_lectura.py
~/venv/bin/python generadores/u4_lectura.py
~/venv/bin/python generadores/u10_lectura.py
~/venv/bin/python generadores/comprueba_lecturas.py     # sale 0 si todo va bien
```

Siguen el patrón de `u5_lectura.py` y `u9_lectura.py` sin tocar `lectura.py`:
misma cabecera de nombre/grupo/fecha/nota, mismos titulillos sin numerar y la
misma comprobación de 30 párrafos y 10 preguntas antes de escribir el PDF.

## 2. El recuento, hecho sobre el PDF

`comprueba_lecturas.py` abre cada PDF, saca el texto, y cuenta los números de
párrafo comprobando que van **1, 2, 3… sin saltos ni repetidos** (no vale que
haya treinta números sueltos), que hay diez preguntas y que la cabecera para
rellenar a mano está. De paso pasa por las seis que ya existían:

```
tema1    3 pag  31 parrafos  10 preguntas  cabecera:si  OK
tema2    4 pag  30 parrafos  10 preguntas  cabecera:si  OK
tema3    4 pag  30 parrafos  10 preguntas  cabecera:si  OK
tema4    4 pag  30 parrafos  10 preguntas  cabecera:si  OK
tema5    4 pag  30 parrafos  10 preguntas  cabecera:si  OK
tema6    4 pag  31 parrafos  10 preguntas  cabecera:si  OK
tema7    4 pag  30 parrafos  10 preguntas  cabecera:si  OK
tema8    5 pag  32 parrafos  10 preguntas  cabecera:si  OK
tema9    4 pag  30 parrafos  10 preguntas  cabecera:si  OK
tema10   4 pag  30 parrafos  10 preguntas  cabecera:si  OK

TODO CORRECTO
```

Los cuatro nuevos llevan **30 párrafos justos**, para que el reparto en voz alta
cuadre con una clase. Las ocho primeras preguntas son de buscar en el texto o de
calcular; **las dos últimas son de opinión razonada** en las cuatro, como pide el
pie que imprime `lectura.py`.

## 3. De qué va cada una, y qué he cambiado de tu propuesta

**Ninguna resume su unidad.** En las cuatro hay guiños explícitos («como viste en
la sesión 4», «vuelve a tu ensayo de palillos») para que el alumno reconozca lo
que ya sabe, pero la historia es nueva.

**Tema 2 · «Dibujar lo que todavía no existe».** Tu propuesta, tal cual, con un
hilo: un plano es una orden de trabajo que tiene que significar lo mismo para
quien la firma y para quien la ejecuta. La catedral que se dibujaba a tamaño real
en un suelo de yeso y se cortaba contra plantillas → Monge, que inventó la
proyección resolviendo un problema de fortificaciones y no pudo publicarla en
treinta y cuatro años porque era secreto militar → Blanc y las piezas
intercambiables → la norma (Whitworth, Baltimore, el A4). Añado una cosa que no
estaba en la unidad y la cierra: la **tolerancia**. Sin decir cuánto error se
admite, un plano no fabrica nada, y eso explica por qué el dibujo solo no bastó.

**Tema 3 · «De dónde sale un lápiz».** Elegí el objeto, que tú dejabas abierto.
El lápiz es el caso perfecto de «la mina o el bosque»: lleva literalmente las
dos, más una tercera pieza de una piedra (la virola de aluminio) y una cuarta de
un árbol que se ordeña (la goma). Y no repite la bicicleta de la sesión 1. Las
cifras de energía del aluminio son **las mismas que ya da la escena de la sesión
4** (45 kWh/kg, reciclar ahorra el 95 %), para que el alumno las reconozca.
Termina donde termina la unidad: de las tres erres, en un lápiz solo funciona la
primera, porque está fabricado para no poder separarse nunca.

**Tema 4 · «Por qué se caen los puentes».** Aquí me he separado más. El Tacoma
**ya está contado en la sesión 1** con sus datos, así que lo uso como punto de
partida conocido y explico lo que allí no cabía (por qué el viento no tuvo que
empujar más fuerte que el puente: la energía se acumulaba vuelta a vuelta) y qué
regla dejó escrita. Y en vez de «alguna pasarela, algún andamio» en abstracto,
van cinco casos concretos, cada uno con un modo de fallo distinto:

1. **Tacoma, 1940** — la forma, no la fuerza → túnel de viento obligatorio.
2. **Pasarela del Milenio, Londres, 2000** — una carga en la que nadie había
   pensado (el empuje lateral de la gente) → hoy se calcula. Nunca estuvo cerca
   de romperse: era segura y era insoportable, y eso también es un fallo.
3. **Hyatt Regency, Kansas City, 1981** — un detalle cambiado por teléfono
   durante la obra → cualquier cambio es un cálculo nuevo, por escrito. Y la
   lección de que **casi nunca falla la viga, falla la unión**, que es
   exactamente lo que les pasa a los puentes de palillos.
4. **I-35W, Minneapolis, 2007** — un error de diseño dormido cuarenta años, que
   despertó cuando el puente llevaba encima capas y capas de asfalto → enlaza
   con la nota de la sesión 5 (lo que aguanta ÷ lo que pesa).
5. **Willow Island, 1978** — el andamio que pediste: una estructura está en su
   peor momento **mientras se construye**.

Sin morbo: los muertos se dicen en una línea, una sola vez, y lo que se
desarrolla en cada caso es qué se aprendió. Aun así, **míralo tú** (punto 6).

**Tema 10 · «El primer programa se escribió para una máquina que no existía».**
Tu propuesta con un añadido: el telar de Jacquard al principio, porque es donde
nace literalmente «escribir aparte lo que la máquina tiene que hacer», y porque
permite cerrar con lo que hace el alumno en la sesión 3 (arrastrar un `.hex` sin
tocar un solo componente). La respuesta a «por qué tardó cien años» son dos
razones, y la segunda me parece la que más enseña: no había material para
construirla, y **a nadie le dolía bastante como para pagarla**. La lectura acaba
en una frase de Lovelace —la máquina no origina nada, hace lo que sepamos
ordenarle— que es palabra por palabra el cierre de tu unidad.

## 4. Datos comprobados, uno a uno

Todos contrastados en esta sesión, no de memoria.

**Tema 2.** Solo se conservan **dos** suelos de trazado medievales en Inglaterra:
York (en un desván construido hacia 1290) y Wells; se dibujaba a tamaño real
sobre yeso y de ahí salían plantillas de madera o chapa. Villard de Honnecourt:
**33 hojas** de pergamino, hacia 1225-1235, BnF, MS Fr 19093. Monge: el método
sale de calcular zonas a cubierto del fuego enemigo en **1765**, el ejército le
impide publicarlo, lo enseña en 1795 y publica *Géométrie descriptive* en **1799**
(34 años). Honoré Blanc: **8 de julio de 1785**, patio de Vincennes, **50** llaves
de fusil desmontadas y remontadas con las piezas mezcladas; Jefferson montó
varias él mismo y lo escribió a su gobierno el 30 de agosto de 1785. Whitney,
1801: Merritt Roe Smith y Robert B. Gordon documentaron que aquellas piezas
estaban ajustadas a mano para la ocasión — por eso lo cuento como aviso.
Whitworth: paper de **1841** en la Institution of Civil Engineers, ángulo de
**55°**, de uso general hacia 1860. Baltimore: incendio del **7 de febrero de
1904**, del orden de **600** acoplamientos distintos en el país, norma única
acordada en 1905 y vigente. Papel: Lichtenberg describe la proporción en una
carta de **1786**, Porstmann la junta con el A0 = 1 m² en la norma alemana **DIN
476 (1922)**, que pasa a ser **ISO 216 en 1975**.

**Tema 3.** Grafito de Borrowdale: descubierto **hacia 1564**, el único depósito
de esa pureza que se conoce. Ley inglesa de **1752** contra su robo, con pena de
azotes y un año de trabajos forzados o siete de deportación. **Conté, 1795**:
grafito molido + arcilla, cocido en horno; más arcilla = más dura y más clara (la
escala H/B). Grafito en Mohs: 1-2. Producción de grafito natural: China, **≈77 %
del mundo en 2023** (USGS) — en el texto digo «alrededor de tres cuartas partes».
Cedro de incienso (*Calocedrus decurrens*), del interior de California y el sur de
Oregón, es la madera de referencia para lápices. Aluminio: **4-5 t de bauxita → 2
de alúmina → 1 de aluminio**; la electrolisis Hall-Héroult consume **13-15 kWh por
kilo** (por eso digo «unos 15 de esos 45 kWh son solo la electrolisis»); reciclar
ahorra **≈95 %** (International Aluminium Institute: 186 GJ/t frente a 8,3 GJ/t).
Caucho: *Hevea brasiliensis*; Tailandia + Indonesia + Vietnam ≈ **62-65 %** de la
producción mundial (2022-2023) → en el texto, «cerca de dos tercios».

**Tema 4.** Tacoma: los datos son **los mismos que ya da tu sesión 1** (1 de julio
y 7 de noviembre de 1940, 853 m, ~68 km/h). Pasarela del Milenio: abre el **10 de
junio de 2000**, cierra dos días después, se le ponen **37 amortiguadores
viscosos y 52 de masa**, reabre en **febrero de 2002**. Hyatt Regency: **17 de
julio de 1981**, **114 muertos**; el cambio de una barra larga a dos cortas dobló
la carga en la unión de la pasarela superior; con el diseño original ya solo
llegaba al **60 %** de lo que exigía la normativa municipal y quedó en el **30 %**
(eso es la pregunta 5). El cambio se pidió y se aprobó por teléfono, sin
confirmación escrita. I-35W: **1 de agosto de 2007**, **13 muertos y 145
heridos**; la NTSB atribuye el fallo a cartelas con la mitad del espesor debido,
sumadas al peso añadido al puente con los años y a las cargas de obra de aquel
día. Willow Island: **27 de abril de 1978**, **51 muertos**, andamio cargado sobre
hormigón vertido **18 horas antes**, con ~220 psi cuando hacían falta más de
1.000 (de ahí «alrededor de la quinta parte»); es el peor accidente de
construcción de EE. UU.

**Tema 10.** Jacquard **1804**, sobre Bouchon (1725), Falcon (1728) y Vaucanson
(~1740). Máquina diferencial: empezada en **1822**, nunca terminada por él; el
Science Museum la construyó siguiendo sus planos — parte de cálculo terminada en
**junio de 1991**, impresora en **2002**, más de **8.000 piezas**, resultados de
**31 cifras**. Máquina analítica: desde **1834**, con «molino» y «almacén», entrada
por tarjetas y salto condicional. Lovelace (**1815-1852**): traduce el artículo de
Menabrea (**1842**, a partir de la conferencia de Babbage en Turín de 1840) y lo
publica en **1843** con sus notas A-G: de **66 páginas, 41 son suyas**, unas tres
veces más largas que el original; la nota G calcula números de Bernoulli y se
considera el primer programa publicado. Turing, **1936**. Manchester «Baby»:
primer programa guardado en memoria, **21 de junio de 1948**, **52 minutos** de
ejecución. 1948 − 1843 = **105 años**.

## 5. Lo que NO he podido comprobar del todo (y cómo lo he escrito)

Va todo dicho como aproximación dentro del propio texto, no escondido aquí:

- **Las cinco toneladas de la máquina diferencial.** Las fuentes dan 2,6 t para
  la parte de cálculo y dicen que la impresora pesa «otro tanto». En el texto:
  «entre las dos tienen más de ocho mil piezas y pesan unas cinco toneladas».
- **La reapertura de la pasarela del Milenio.** Unas fuentes dicen 22 de febrero
  de 2002 y otras 27. En el texto pone solo «febrero de 2002».
- **Por qué se bamboleaba esa pasarela.** La explicación clásica es que la gente
  sincroniza el paso; **en 2021 se publicaron trabajos que discuten el detalle**.
  Lo digo dentro de la lectura, en el párrafo 14, porque me parece que enseña
  algo: que esté en las normas no significa que esté entendido del todo.
- **Quién escribió la nota G.** Hay discusión historiográfica real sobre cuánto
  es de Lovelace y cuánto de Babbage. El párrafo 17 lo cuenta y no lo cierra; lo
  que sí se defiende como suyo es la idea de que la máquina no tiene por qué
  manejar números, que es lo gordo de las notas.
- **Los 140.000 vehículos/día del I-35W** y **los 600 acoplamientos de manguera**:
  van con «unos» y «del orden de», que es como los dan las fuentes.
- **El peso de la virola (0,35 g)** de la pregunta 5 del tema 3 es un dato *que da
  la pregunta*, no una afirmación de la lectura. Si pesas una de verdad y sale
  otra cosa, cambia el número y la cuenta sigue funcionando igual.
- **Cuántos lápices se fabrican al año en el mundo**: circula la cifra de 14-20
  mil millones y no he encontrado fuente seria. **No aparece en la lectura.**

## 6. Lo que deberías mirar tú

1. **El enlace desde la página del tema.** Los PDF están en su carpeta, como
   pedías, pero **no he tocado ningún `index.html`**. Ahora mismo los temas 1, 6,
   7, 8 y 9 enlazan su lectura desde la sesión correspondiente y el 5 no. Si los
   quieres enlazados, el bloque es el de `u9_build.py:354-361`, con `href` y
   título cambiados. Antes de hacerlo hay dos pegas que conviene que sepas:
   - **El tema 2 no tiene generador** en el repo (no existe `u2_build.py`), así
     que ahí habría que editar el HTML a mano.
   - **`u1_build.py`, `u3_build.py`, `u4_build.py` y `tema0_build.py` llevan una
     ruta de Windows escrita a fuego**: `BASE = "C:/Users/javie/AppData/Local/
     Temp/rt-clone"`. Si los ejecutas en el servidor **no escriben en el repo**:
     crean una carpeta `generadores/C:/Users/...` y dejan ahí el `index.html`. Me
     pasó al comprobarlo y borré la carpeta. Comprobado además que lo que generan
     es **idéntico** al `index.html` que hay comprometido, así que el generador es
     fiel; lo que está mal es solo esa línea.
2. **El registro del tema 4.** Tres de los cinco casos llevan muertos (114, 13 y
   51). Está escrito sin detalles y siempre girando hacia lo que se aprendió,
   pero eres tú quien conoce al grupo: si te parece mucho para trece años, el
   caso más fácil de quitar es Willow Island, y entonces el tema del andamio se
   cuenta solo con el párrafo 27, que no tiene ninguna cifra.
3. **El objeto del tema 3.** Elegí el lápiz por mi cuenta. Si prefieres otro (el
   boli, la silla del aula), el esqueleto de la lectura aguanta: son cinco piezas
   y cinco viajes.
4. **La tolerancia en el tema 2.** La meto yo. Tu propia unidad avisa de que el
   currículo no tiene un saber que diga «vistas» ni «acotación» y que todo esto
   entra como «documentación técnica y gráfica básica» del criterio 4.1; la
   tolerancia entra por la misma puerta, pero es decisión tuya si la quieres en
   2.º o la dejas para 3.º.
5. **No llevan solucionario**, igual que las de los temas 5 y 9. Si quieres uno
   para corregir en clase, dilo y lo saco aparte, no dentro del PDF del alumno.
6. **Las preguntas de calcular** son: tema 2 → 5 y 6 (cuántos A4 en un A0, y una
   tolerancia de ±0,2); tema 3 → 5 y 6 (energía de la virola, bauxita por kilo);
   tema 4 → 5 (del 60 % al 30 %); tema 10 → 6 y 7 (105 años, y 41 de 66 = 62 %).
   Repásalas con la calculadora antes de repartirlas, que es lo que se corrige
   delante de toda la clase.
