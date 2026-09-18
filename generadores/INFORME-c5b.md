# Informe · Unidad 5 de 4.º de ESO · Electrónica y neumática · **segunda mitad**

Rama `c5b`. Las cuatro sesiones que faltaban (S5 a S8) escritas y montadas sobre la
primera mitad, que **no se ha tocado**. La unidad queda con **8 sesiones escritas y
0 pendientes**, la página abre, las **ocho** escenas calculan y el verificador pasa
**230 comprobaciones sin fallos**.

> El encargo pedía «escribe `INFORME.md`». Lo dejo donde están los otros trece,
> `generadores/INFORME-<rama>.md`, que es la convención del repositorio
> (`INFORME-c5.md` es el de la primera mitad de esta misma unidad y
> `INFORME-c4b.md` el del encargo gemelo de la unidad 4).

---

## Qué hay entregado

| Fichero | Qué es |
|---|---|
| `4eso/Tecnologia/tema5/index.html` | La unidad entera, 412 KB, regenerada |
| `generadores/c5b_texto.py` | El texto de S5 a S8 y el test de la unidad |
| `generadores/c5b_escenas.py` | Escenas de S5 (la placa) y S6 (el arranque) |
| `generadores/c5b_escenas2.py` | Escenas de S7 (la secuencia) y S8 (la cadena) |
| `generadores/c5b_fotos.py` + `creditos_c5b.json` | Descarga de Commons con licencias |
| `img/c5b-protoboard.jpg` … `c5b-bornes.jpg` | Cinco fotos nuevas de Commons |
| `generadores/c5_build.py` | Tocado en tres sitios: importa `c5b_texto`, sustituye las cuatro `pendiente=True` y añade una regla CSS |
| `generadores/c5_comprueba.py` | Ampliado: las cuentas de S5 a S8 rehechas en Python |
| `generadores/c5_verifica.py` | Ampliado: de 110 a **230** comprobaciones |
| `generadores/c5_capturas.py` | Ampliado: 23 → **49** capturas |

`4eso/Tecnologia/index.html` **no se ha tocado**, como pedía el encargo.

Cómo se regenera todo:

```
/home/ubuntu/venv/bin/python generadores/c5_build.py          # 8 sesiones, 8 escritas
/home/ubuntu/venv/bin/python generadores/comprueba_paginas.py # 23 paginas, ningun NUL
/home/ubuntu/venv/bin/python generadores/c5_comprueba.py      # las cuentas, en Python
/home/ubuntu/venv/bin/python generadores/c5_verifica.py       # 230 OK, 0 fallos
/home/ubuntu/venv/bin/python generadores/c5_capturas.py       # PNG en /tmp/c5-capturas
```

---

## La cadena de las cuatro sesiones

Mantuve los cuatro títulos del encargo. La cadena causal encaja: cada una nace del
fracaso de la anterior, y las cuatro **aterrizan en el proyecto decidido** (riego
automático, con ventilación y lámpara como variantes).

| | Sesión | El problema con el que abre | Lo que deja abierto |
|---|---|---|---|
| S5 | Del esquema al montaje | En Tinkercad va y en la placa no | Ya está montado; ahora el programa |
| S6 | El programa que decide | La bomba arranca antes de que el programa exista | Ya sé leer y accionar; ¿y si el actuador es de 24 V? |
| S7 | Electroválvulas y secuencias | La chapa pide 24 V, 125 mA… y 2 bar | Las siete piezas sueltas; ¿y juntas? |
| S8 | El automatismo completo | Funciona, y hay que **entregarlo** | Cierra la unidad |

Y el hilo que se repite tres veces, a propósito, porque es lo que hay que llevarse:
**en electrónica «al aire» nunca quiere decir «a cero»** (la LDR de la S1, la base
de la S6, el nudo del sensor de la S5).

---

## ⚠️ Dos cosas de la primera mitad que se han quedado desfasadas

El encargo pedía decirlas, no arreglarlas. **No las he tocado.**

**1. La primera mitad habla de «los cinco proyectos del curso», y ya son tres.**
Cuando se escribió, `PROYECTOS.md` no tenía el bloque DECIDIDO. Hoy los proyectos
son tres (riego, ventilación, lámpara) y la barrera y el contenedor **están
cortados**. Aparece en dos sitios de `c5_build.py`:

- `S4_TEORIA`, recuadro «La cadena completa de un automatismo»: *«Cualquiera de los
  **cinco** proyectos del curso es la misma cadena»*.
- `S4_PRACTICA`, segunda parte: *«Elegid dos de los **cinco proyectos del catálogo
  del curso** —por ejemplo la **barrera de bicis** y el **contenedor que avisa**—»*.
  Esta es la grave: manda trabajar sobre dos proyectos que ya no existen en el curso.

Arreglarlo es cambiar «cinco» por «tres» en la primera y reescribir los ejemplos de
la segunda. En la S3 pasa algo parecido pero es menos serio, porque allí la barrera y
el contenedor se usan como **ejercicios de dimensionado**, no como «el proyecto del
curso»; yo los dejaría.

**2. El test de la S4 se llama «Comprueba lo de estas cuatro sesiones».** Sigue
valiendo tal cual ahora que existe el de la unidad entera; lo digo solo para que
conste que los dos conviven a propósito (ver abajo).

---

## Las decisiones que he tomado

### 1. Dos tests, con identificadores distintos

`INFORME-c5.md` dejaba abierto qué hacer con el test de la S4. He hecho lo que
recomendaba: **dejar los dos**. El de la S4 cubre S1-S4 (`test('c5', …)`) y el nuevo
cubre la unidad entera (`test('c5b', …)`), con diez preguntas repartidas entre las
ocho sesiones.

El verificador comprueba explícitamente que **no comparten ni un nombre de campo**
(`c5-0…c5-9` frente a `c5b-0…c5b-9`) y que **corregir uno no toca el otro**, que era
el riesgo que avisaba el encargo.

### 2. La frontera con la unidad 4, respetada al pie de la letra

Leí entera la segunda mitad de la unidad 4 (`c4b_texto.py`) antes de escribir. Su
S5-S8 son: **proporcional y PWM**, **programar el control** (`millis()`, media,
margen, dosis, tope), **calibrar la sonda con una báscula y dónde clavarla**, y
**protocolo de prueba y defensa del proyecto**. Nada de eso entra aquí.

Esto obligó a **cambiar lo que la primera mitad anunciaba** para S6. El cierre de la
S4 y el `INFORME-c5.md` proponían «umbrales, histéresis, el `if` que no parpadea»,
que es exactamente la S6 de la unidad 4. El encargo lo corrige («tu S6 va pegada al
montaje»), y así está escrito: la S6 va del **sentido del divisor**, de **qué hace un
pin antes de que exista tu programa** y de que **la medida es ratiométrica**. La
parte de «decidir» se nombra y se manda a la unidad 4, con una frase explícita dentro
del recuadro de la libreta.

Quedan **tres roces** que un humano debería mirar:

- **La media de diez lecturas.** Está en la S6 de la unidad 4 (como línea de control)
  y en mi `leeSensor()` (como parte de la función que habla con la placa). Es la misma
  línea de código en dos sitios. No creo que moleste —aparece con papeles distintos—
  pero si queréis quitarla de un lado, quitadla del mío.
- **La lista de puesta en marcha.** La unidad 4 tiene una (S7) sobre el agua y la
  colocación; la mía (S8) es **eléctrica y por orden de conexión**, con un polímetro.
  No se solapan en contenido, pero se llaman casi igual. Sugiero renombrar la mía a
  «puesta en tensión» si os choca.
- **La defensa.** La unidad 4 (S8) tiene el guion de tres minutos. La mía dice
  explícitamente que la defensa es de allí y que de aquí salen **tres papeles**
  (esquema, lista de conexiones y un número medido). Está subordinada a propósito.

### 3. La escena de la S7 no es el proyecto del curso, y es a propósito

Las otras tres escenas nuevas van del riego (y, la de la S8, de las tres variantes).
La de la S7 es una **prensa con dos cilindros** haciendo A+ B+ A− B−.

**Por qué.** El proyecto del curso tiene **un** actuador, y con un actuador no hay
secuencia: se enciende y se apaga. El problema del orden —que es el contenido de la
sesión y es lo que pide el saber de neumática— necesita dos. Puse la secuencia
canónica, que además es la que el alumno se va a encontrar en cualquier libro y en
cualquier vídeo.

El puente al proyecto está escrito, en un recuadro propio: vuestra secuencia tiene
dos pasos, vuestro «final de carrera» **es la sonda**, y la pregunta *«¿ha llegado ya
el agua?»* es exactamente *«¿ha llegado ya el cilindro?»*. La actividad se hace sobre
el proyecto de cada grupo, no sobre la prensa.

**Cambié la historia de la máquina a mitad de camino** y conviene saberlo: empecé con
A = mordaza y B = punzón, y al mirar la captura vi que con esa historia la secuencia
canónica A+ B+ A− B− **suelta la pieza con el punzón dentro**, o sea que el ejemplo de
libro salía siendo un fallo. Con A = empujador (coloca la pieza) y B = punzón, la
secuencia canónica es correcta y el fallo aparece solo cuando saltas por tiempo. El
contador de choques mide justo eso: cuántas veces ha **empezado a bajar** el punzón
con la pieza sin colocar.

### 4. El «impacto» entra, pero solo como número

La última parte de la escena de la S8 calcula lo que gasta el automatismo **en
reposo** (0,22 W las 8760 horas del año) y lo que gasta el actuador. Es de esta unidad
porque sale del presupuesto de corriente, que es electricidad. **Comparar los dos
platos de la balanza —lo que ahorras frente a lo que cuesta fabricar y tirar el
aparato— lo mando a la unidad 8**, con esa frase dentro del texto. Por eso tampoco
he puesto chips de CE6 en la sesión: `CURRICULO.md` manda 6.x a U8 y U9.

---

## Las escenas: qué calcula cada una

Ninguna lleva dentro una tabla de resultados. `c5_comprueba.py` rehace las cuatro
cuentas nuevas en Python —mirando la física, no copiando el JavaScript— y
`c5_verifica.py` compara lo que la página enseña con lo que sale de ahí.

**S5 · La placa de pruebas.** Es la que más me gusta y la que más trabajo ha dado.
**Los nudos no están escritos en ninguna parte**: se calculan con un *union-find*
sobre los 224 agujeros, uniendo primero lo que una placa de pruebas une por dentro
(cada columna de cinco, cada raíl entero, y el canal central que no une nada) y
después lo que unen los puentes. De ahí sale la lista de conexiones **real**, que se
compara con las nueve del esquema, y de ahí sale el circuito que ha quedado, que no
siempre es el que se quería. Seis montajes: bien, sonda en la misma fila, transistor
girado, puente en la misma fila, sin masa común y diodo al revés. Un polímetro con
cinco puntos de prueba enseña la tensión **calculada** en cada uno.

Hay un detalle que me costó y que conviene apuntar: para saber si un **puente une
algo** hay que guardar la raíz de cada agujero **antes** de poner los cables. Después
de unirlos, los dos extremos de un puente son siempre el mismo nudo, lo una o no lo
una, y la comprobación sale bien siempre. Está resuelto con una foto del union-find
en `soloPlaca`.

Los tres casos más bonitos, todos resueltos con ecuaciones en el momento:

- **Sonda en la misma grapa**: la grapa la cortocircuita, el nudo se queda colgando de
  los 5 V y la cuenta se clava en **1023**.
- **Colector y emisor cambiados**: el transistor **sigue conduciendo**, pero como
  seguidor de emisor. Se resuelve el sistema (Ib = (Vpila − Vpin + Vbe) /
  ((β+1)·Rcarga − Rb)) y salen 0,12 mA de base, 116 mA de carga y **2,77 V** en la
  bomba de los 6. No quema nada, y por eso es el fallo que más tarde hace perder.
- **Diodo al revés**: conduce en régimen y **cortocircuita la pila**. Con 1 Ω de
  resistencia interna salen 5,10 A por un 1N4007 que admite 1 A.

**S6 · Los seis primeros segundos.** Simulación paso a paso, de 2 en 2 ms sobre 6 s
(3000 pasos), rehecha entera al tocar cualquier control. Reset, gestor de arranque
(~1 s con los pines en entrada), `setup()` y lazo, con la tensión de alimentación
cayendo cuando arranca la bomba. Tres cosas que enseña y que no se ven leyendo código:

- **La bomba arranca 1000 ms antes de que el programa exista**, y con la resistencia
  de 10 kΩ de base a masa, 0 ms.
- **En el pin 13 son tres golpes**, porque el gestor de arranque parpadea el LED de la
  placa, que está en ese pin.
- **La pescadilla que se muerde la cola**: con una sola fuente y 4 Ω de resistencia
  interna, la bomba tira → la tensión baja de 4,3 V → el micro se reinicia → suelta la
  bomba → la tensión sube → arranca otra vez. **142 veces en seis segundos**, y el
  programa no llega a ejecutarse nunca. Desde fuera parece que el programa está mal.

Nota de dibujo: los bajones duran 2 ms y el eje mide 6 s, así que un bajón **no llega
ni a un píxel**. La curva de tensión se dibuja como **envolvente** (máximo y mínimo por
píxel), que es como se dibuja cualquier onda densa y aquí además es lo único que
enseña el problema. Con la curva punto a punto, la gráfica salía plana y mentía.

**S7 · La secuencia.** Dos cilindros con sus 5/2 (monoestables o biestables),
cuatro finales de carrera y una máquina de estados que salta **por tiempo** o **por
final de carrera**. Las velocidades salen de v = Q/A. El **diagrama espacio-fase** de
abajo no está dibujado: se traza con las posiciones de los últimos 2,4 segundos, con
las rayas de cambio de paso puestas donde de verdad cambió. Cuatro cosas que se ven:

- Por final de carrera, subir la carga **alarga el ciclo y no rompe el orden**.
- Por tiempo, la misma carga hace que el punzón baje con la pieza sin colocar.
- Con el final de carrera b1 aflojado, la secuencia **se para** y el vigilante dice en
  qué paso. Parado es malo; seguir es peor, y se puede comparar.
- Al cortar la corriente, las monoestables vuelven al reposo y las biestables se
  quedan donde iban. Es la diferencia que decide cuál se compra.

**S8 · La cadena entera.** Los siete eslabones de la unidad encadenados, con el número
de cada uno y seis averías que se inyectan. Reutiliza los modelos de las sesiones
anteriores: divisor y conversor de la S1, transistor y diodo de la S2, masa común de
la S5. Las dos averías que **no rompen nada y no dan error** son las que más enseñan:
la R fija de 1 MΩ (el divisor funciona, pero la cuenta no pasa de 58 y el umbral está
en 700: el sistema no puede actuar nunca) y la pila gastada (funciona, solo que rinde
menos, y como la medida es ratiométrica el sistema no tiene manera de enterarse).

### Un error mío que cacé mirando la escena

La avería de la **R fija de 1 MΩ** la había escrito para enseñar la **corriente de
fuga** del pin del conversor: 1 µA sobre medio megaohmio son 0,5 V de error. Hice la
cuenta con los valores de verdad y **no sale**: con la sonda entre 5 y 60 kΩ, la
impedancia que ve el pin es de 40 kΩ y el error son 0,04 V, ocho cuentas. Lo que de
verdad rompe esa avería es otra cosa, y más simple: la fija es **veinte veces** mayor
que el sensor, se queda con casi toda la tensión y la cuenta no llega nunca al umbral.
Está reescrito así, con la cuenta hecha barriendo el rango entero del sensor, y la
fuga se cuenta después como segunda razón con **su número real**, no con uno inventado.

---

## Lo que miré con los ojos, no solo con un test

El script saca ahora **49 capturas**. De las 26 nuevas he abierto **17**, y varias
de ellas tres o cuatro veces mientras arreglaba lo que enseñaban; las nueve que no
he mirado son variantes muy próximas a otra que sí (por ejemplo `pla-mojada` frente
a `pla-ok`, o `cad-ventilacion` frente a `cad-lampara`). **Quedan por mirar**, y
están ahí para que alguien las abra. De las que sí miré salieron, entre otras cosas:

- El **puente que no unía nada** daba siempre por bueno (ver arriba): lo vi porque en
  el montaje correcto la lista decía «8 de 9».
- La avería **«sin masa común»** se estaba explicando con el texto de **«el puente en
  la misma fila»**, porque compartían estado interno. Ahora son dos estados distintos
  y el verificador comprueba los dos títulos.
- La escena de la S6 dibujaba **una línea plana** donde tenía que haber 142 bajones.
- Las **dos 5/2 de la S7** tenían el muelle y la bobina dibujados en un sitio fijo
  mientras el cuerpo se desplazaba, así que al conmutar el muelle se quedaba flotando
  a medio centímetro de su válvula. Ahora los accionamientos van pegados al cuerpo y
  las **vías numeradas** (1, 3, 5 abajo; 4, 2 arriba) se quedan sobre la ventana, que
  es la convención correcta y la que ya usaba la S4.
- Rótulos pisándose en ocho sitios (el polímetro sobre su propia caja, «MASA Arduino»
  metiéndose en el panel de la derecha, el cuerpo del TIP120 sobre la Rb, «el
  empujador se retira» sobre su condición, «umbral 700» encima de la curva…).
- Los cables de `A0` y `D9` **salían fuera del lienzo** y se cortaban. Ahora bajan al
  canal central o suben al hueco de los raíles y salen por ahí, que además es lo que
  se hace de verdad.
- El veredicto «al actuador le falta tensión» **saltaba en el montaje sano**, porque
  comparaba con la tensión nominal del actuador y no con la que le llega con un
  Darlington saturado. Un TIP120 se queda con 1 V siempre: eso es normal, no una
  avería. Ahora se compara contra la fuente sana y el 1 V se explica en el pie.
- Con la **pila gastada**, el último eslabón ponía **NO** en rojo. Y la bomba
  **sí** se mueve, solo que peor: decirlo así era mentir, y encima tapaba justo lo
  que hace difícil esa avería. Ahora pone **A MEDIAS** en ámbar.
- La captura de **b1 aflojado** salía antes de que el vigilante hubiera saltado (la
  escena va a cámara lenta y el guion esperaba tres segundos), así que la foto
  enseñaba una máquina funcionando tan tranquila. Es la única vez que el fallo
  estaba en el guion de capturas y no en la escena, pero si no se abre no se ve.

---

## Imágenes y vídeos

**Cinco fotos nuevas de Wikimedia Commons**, licencia comprobada por la API y
**abierta y mirada una a una** (créditos en `generadores/creditos_c5b.json`):

| Fichero | Original | Autor | Licencia | Qué se ve, de verdad |
|---|---|---|---|---|
| `c5b-protoboard.jpg` | Metal contacts within a breadboard.jpg | Zeroping | CC BY 4.0 | La placa por detrás, sin adhesivo: las tiras cortas de cinco, las largas de los raíles, el hueco del canal y **una grapa sacada** con sus cinco pinzas |
| `c5b-polimetro.jpg` | Multimeter probes on breadboard.jpg | Zeroping | CC BY 4.0 | Las puntas clavadas en agujeros libres de la misma fila, con las letras y los números de la placa legibles |
| `c5b-die.jpg` | Atmel atmega328 mz 20x.jpg | Markus Kammerstetter | CC BY 4.0 | El ATmega328 sin cápsula: el anillo de contactos y los hilos de cada patilla |
| `c5b-bobina.jpg` | Solenoid coil of a pneumatic valve.jpg | Sarah Adrita | CC BY-SA 4.0 | La chapa entera: DC24V, 125 mA, 3 W, 100 % ED, IP 65, y el conector transparente con su circuito dentro |
| `c5b-finales.jpg` | Limit Switches.JPG | Mixabest | CC BY-SA 3.0 | Tres finales de carrera de palanca y rodillo con la **leva** que los acciona |

Dos notas de honestidad, las dos escritas dentro de los pies:

- La foto del **die** no permite señalar dónde está el conversor: haría falta el plano
  del fabricante y no se publica. El pie dice justo eso y se limita a lo que **sí** se
  ve (los contactos, los hilos y que las zonas regulares son memoria).
- La placa que se ve en la foto del polímetro **no es un Uno**: por los pines
  numerados hasta el 33 es una **Mega**. Lo digo en el pie en vez de callármelo.
- En la foto de los bornes, el rótulo dice `BATTERIES 1–8` y los bornes llegan al 12.
  Lo he convertido en la lección de la sesión: **un rótulo no basta, hace falta la
  lista de conexiones**.

**Cuatro vídeos de YouTube**, título y canal comprobados por oEmbed el 18-sep-2026:

| Sesión | ID | Título | Canal |
|---|---|---|---|
| S5 | `OvlutalHXoM` | Como funciona una protoboard · Electronica basica | Ivan Espinoza |
| S6 | `pvetokUpfzQ` | Arduino desde cero en Español · Cap. 85 · Pull-up y Pull-down | Bitwise Ar |
| S7 | `H3_xq9FLT1s` | Secuencia 2: A+ B+ A− B− [Método Paso a Paso] | Jose Luis Sarmiento |
| S8 | `9SKD_p9sFcI` | Arduino desde cero en Español · Cap. 50 · Alimentación para proyectos | Bitwise Ar |

⚠️ **Nadie los ha visto enteros.** Lo comprobado es que existen, que el título y el
canal son los que dice la página y que cargan. Sale dicho en cada uno. Dos son del
mismo canal; si eso no gusta, el de la S8 tiene sustitutos fáciles.

---

## Dudas y cosas que tiene que mirar un humano

**1. Los saberes B.1 a B.4 siguen sin transcribir en `CURRICULO.md`.** He mantenido
el reparto que hizo la primera mitad y lo he extendido: S5 → B.1·B.2, S6 → B.2,
S7 → B.3·B.4, S8 → B.1 a B.4. **Es una hipótesis heredada**, no una lectura del Anexo
II. Hay que contrastarlo antes de que esto se use para calificar.

**2. Cifras que son criterio nuestro o estimación, no medida.** Todas están rotuladas
como tales *dentro* de la página; las junto aquí por si alguna chirría:

- El **umbral de brownout en 4,3 V**. El detector del ATmega328P viene de fábrica en
  2,7 V; los 4,3 V son el punto en el que el regulador y el USB dejan de ser fiables,
  y es **una elección nuestra**.
- El **~1 s del gestor de arranque** (Optiboot). Es la cifra que se maneja; no la he
  medido con un cronómetro.
- Que un **pin en entrada haga conducir la base**. Un pin al aire **no se sabe** a qué
  tensión se queda. La escena dibuja el **peor caso**, que es con lo que se diseña, y
  lo dice. Un alumno que lo pruebe puede ver que su placa no arranca la bomba: eso no
  invalida la lección, pero conviene que el profesor lo sepa.
- La **resistencia de 10 kΩ de base a masa como obligatoria en 4.º**. Es criterio
  nuestro, no una norma. Me parece defendible: cuesta dos céntimos y quita un fallo
  entero.
- La **corriente de fuga de 1 µA** del pin analógico es el **máximo** que admite la
  hoja; la típica es mucho menor. Está usada para dar el orden de magnitud del error
  y para explicar de dónde sale la recomendación de los 10 kΩ.
- La **presión mínima de pilotaje de 2 bar** de una servopilotada. Es el valor típico
  de catálogo, no el de un modelo concreto.
- El **modelo de la sonda de suelo** (60 kΩ en seco, 5 kΩ empapada) es nuestro. La
  sonda de verdad se calibra con una báscula, que es la S7 de la unidad 4, y sale
  dicho en las dos escenas que lo usan.
- Los **200 NL/min** de la válvula, la **cámara lenta de 5×** y que la carga baje la
  velocidad **en proporción**: los tres son simplificaciones declaradas en el pie.
  Lo que sí es exacto es que por encima de la fuerza del cilindro no se mueve.
- El **retroceso de los cilindros se calcula a la misma velocidad que el avance**. En
  uno de verdad es algo más rápido, porque la cámara del vástago tiene menos volumen.
  Sale dicho.
- Los **repartos de horas del actuador** del cuadro de consumo (0,4 % el riego, 15 %
  la ventilación, 20 % la lámpara) son estimaciones para dar orden de magnitud, y la
  escena dice dos veces que **lo de cada grupo se mide**.
- La **resistencia interna de 1 Ω** de las cuatro pilas AA.

**3. Sigo sin haber abierto Tinkercad.** Las actividades que lo usan están escritas
por lo que sé que hace. La de la S6 avisa de una cosa concreta: **el arranque no se
puede ver ahí**, porque Tinkercad no simula el gestor de arranque. Esa medida está
puesta como trabajo de placa real a propósito. Si resulta que Tinkercad sí lo simula,
la actividad sigue valiendo y hay que quitar la nota.

**4. Los tiempos de las sesiones.** S5, S6 y S7 llevan el minutado de siempre
(10/25/20/5) y S8 el del test (10/20/15/15). La S7 tiene mucha teoría —la
electroválvula, los dos tipos de válvula, los finales de carrera y la secuencia— y me
temo que **25 minutos se quedan cortos**. Si hay que recortar algo, yo quitaría el
«solo para entenderlo» de la cascada neumática, que es cultura y no criterio.

**5. La escena de la S7 va con `requestAnimationFrame` y no para nunca.** Las otras
siete solo calculan cuando tocas un control. En una pestaña abierta toda la tarde,
esa consume. No he puesto un interruptor de pausa ni un `IntersectionObserver`; si
os preocupa el portátil de alguien, es media hora de trabajo.

**6. El vigilante de la escena de la S7 salta a 1 s de tiempo de modelo**, y el
ejemplo de código del texto dice `> 1000`. Los dos números coinciden a propósito y
están explicados («cinco veces el paso más largo»), pero si cambiáis uno, cambiad el
otro: el verificador espera 7 s de reloj para que el vigilante haya saltado.

**7. El audio del narrador no se ha vuelto a generar.** El de la primera mitad sigue
puesto y sigue siendo correcto: habla de las cuatro piezas, no de las ocho sesiones.
Si queréis que la voz cuente la unidad entera, hay que rehacer `guion_c5.txt` y el
mp3, y eso no estaba en el encargo.

**8. `ENCARGO.md` entra en el repositorio con este commit**, arrastrado por el
`git add -A` que pide el propio encargo, igual que pasó en la primera mitad.
