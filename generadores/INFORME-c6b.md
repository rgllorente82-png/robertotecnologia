# Informe · segunda mitad de la unidad 6 de 4.º (Programación, IoT e inteligencia artificial)

Sesiones **5, 6, 7 y 8**, escritas sobre la primera mitad ya publicada. La página
queda con **8 sesiones escritas y 0 pendientes**.

```
~/venv/bin/python generadores/c6_build.py      -> 8 sesiones (8 escritas, 0 pendientes)
~/venv/bin/python generadores/c6_verifica.py   -> 591 comprobaciones, 0 fallos
~/venv/bin/python generadores/comprueba_paginas.py -> 23 páginas, ninguna rota
~/venv/bin/python generadores/comprueba_tests.py   -> tema 6: 2 tests, 22 preguntas, bien
```

No se ha tocado nada de las sesiones 1 a 4 ni `4eso/Tecnologia/index.html`.

---

## 1 · Qué hay escrito

| | Título | Escena nueva | Foto | Vídeo |
|---|---|---|---|---|
| **S5** | La bomba arrancó a las tres de la mañana | `HISTORICO` (`mem-`) | el ATmega328 por dentro | media móvil en Arduino |
| **S6** | Llevaba seis días callado, y eso parecía buena señal | `AVISO` (`avi-`) | ESP-01 sobre un DHT11 | ESP8266 subiendo datos |
| **S7** | Acierta el 93 %. Con los vuestros. | `DATOS` (`dat-`) | las *computers* de Harvard, hacia 1890 | qué es el sobreajuste |
| **S8** | Tres minutos, funcionando, delante de gente | `SISTEMA` (`sis-`) | seta de emergencia de un cuadro de mandos | máquinas de estados en Arduino |

**Ficheros nuevos**

- `generadores/c6b_escenas.py` — escenas de S5 y S6.
- `generadores/c6b_escenas2.py` — escenas de S7 y S8.
- `generadores/c6b_texto.py` — el texto de las cuatro sesiones, sus fichas de
  práctica, sus cierres y el test `c6b`.
- `generadores/c6b_gemelos.py` — **los cuatro modelos escritos otra vez en
  Python**, para que el verificador pueda comparar. Ver §5.
- `generadores/c6b_fotos.py` — comprobación de licencia y descarga de las cuatro fotos.
- `generadores/c6b_mirada.py` — capturas de las escenas, para **mirarlas**.
- `generadores/c6b_tabla.py` — saca de la página las tablas que se citan en el
  texto, para que las cifras escritas sean exactamente las que ve el alumno.
- `generadores/c6b_lee.py` — vuelca el texto de una sesión para releerlo seguido.
- `img/c6-atmega328-die.jpg`, `c6-esp8266-dht11.jpg`, `c6-computers-harvard.jpg`,
  `c6-seta-emergencia.jpg`.

**Ficheros tocados**: `generadores/c6_build.py` (importa `c6b_texto` y sustituye
los cuatro `pendiente=True`) y `generadores/c6_verifica.py` (ampliado, §5).

---

## 2 · La decisión de fondo: el proyecto ya está elegido

La primera mitad rota entre los cinco candidatos porque cuando se escribió el
proyecto no estaba decidido. Estas cuatro sesiones aterrizan en lo que dice
`PROYECTOS.md` (bloque DECIDIDO, 18-sep-2026): **riego automático** como
principal, con **ventilación** y **lámpara** como variantes.

**Las cuatro escenas llevan los tres proyectos en pestañas**, con el mismo
modelo detrás y solo cambiando el sensor, el actuador y el guion del día. Es
deliberado: así el grupo que eligió B o C no tiene que traducir de un ejemplo
ajeno, que es el punto donde la unidad 4 dice que menos seguro está. El texto y
las fichas de práctica dicen siempre «vuestro proyecto», y los ejemplos de la
prosa van sobre el riego con la variante entre paréntesis.

Las cuatro escenas comparten además el hilo: la S8 usa la **media de 10** de la
S5 y la política **evento + latido** de la S6, y lo dice en el pie. Un alumno
puede llevarse un número de la S5 a la S8 y le cuadra.

---

## 3 · Lo que enseña cada escena, y qué calcula

Las cuatro simulan de verdad. **Ninguna tiene un número escrito a mano**: todas
las cifras de las tablas y de los textos salen de recorrer la simulación al
pulsar, y todas están comparadas contra un gemelo en Python (§5).

### S5 · `HISTORICO`

Un día entero (720 medidas, una cada 2 min) del sensor del proyecto, con ruido
de ±12 unidades y **seis picos de un instante** de 300 a 699 unidades. Cuatro
reglas de decisión y dos tipos de dato. Medido sobre el riego con umbral 600:

| regla | arranques de más | tarda de media | bytes |
|---|---|---|---|
| el último valor | **5 de 8** | +3 min | 2 |
| media de 5 | 2 de 4 | +5 min | 10 |
| media de 10 | 0 de 2 | +11 min | 20 |
| media de 20 | 0 de 2 | +20 min | 40 |
| **mediana de 5** | **0 de 2** | +7 min | **10** |
| mediana de 9 | 0 de 2 | +11 min | 18 |
| tendencia con N=20 | 5 de 5 | **−9 min** | 40 |

El hallazgo que justifica la sesión, y que no me esperaba al empezar: **la media
no quita el pico, lo estira**. Con media de 5 las falsas alarmas *suben* respecto
al último valor (12 frente a 5 medidas mal decididas), porque el pico pasa de
contaminar una medida a contaminar cinco. La mediana de 5 hace con **10 bytes**
lo que a la media le cuesta 20. Y la tendencia es la única que se **adelanta**
(−9 min), a cambio de disparar 5 arranques falsos de 5.

El panel de código se reescribe con la N, el umbral y el tipo que haya puestos,
y con `byte` añade el `/ 4`.

### S6 · `AVISO`

Catorce días a pasos de 5 minutos (4.032 pasos), con las incidencias del
proyecto, una **caída de red de nueve horas el día 6** y una casilla para que el
aparato **se quede mudo el día 9**. Medido sobre el riego, con el aparato mudo:

| política | salen | llegan | incidencias que nadie supo | ¿se descubre el silencio? |
|---|---|---|---|---|
| periódico cada 5 min | 2.736 | 2.628 | 2 | sí, en 5 min |
| periódico cada 1 h | 228 | 219 | 2 | sí, en 1 h |
| por evento (último valor) | 42 | 30 | 2 | **NO** |
| por evento (media de 10) | 26 | 20 | 2 | **NO** |
| evento + latido de 6 h | 59 | 53 | 2 | sí, en 9,3 h |
| evento + latido de 2 h | 231 | 222 | 2 | sí, en 1,3 h |

Tres cosas que salen medidas y que sostienen la sesión:

1. **Por evento a secas, el silencio no se descubre nunca.** El latido es lo que
   pone el silencio del lado de las averías.
2. **La cola de memoria convierte una incidencia perdida en una sabida tarde.**
   La tercera incidencia del riego cae *entera* dentro de la caída de red (está
   puesta ahí a propósito): sin cola, `no se supo nunca`; con cola y reintento,
   se supo **siete horas tarde**. El modelo reintenta en cuanto vuelve la red,
   no cuando toca mandar algo nuevo; con lo segundo el aviso tardaba 106 horas,
   y eso no es guardar, es perder despacio.
3. **Decidir con el último valor dispara más mensajes** que decidir con la media
   de 10 (42 frente a 26), con las mismas incidencias. Es el enganche con la S5.

Un resultado que me obligó a reescribir un párrafo: **el latido da una falsa
alarma con casi cualquier plazo** cuando la red se cae nueve horas (sin caída de
red, cero falsas con cualquier plazo). No es un defecto del diseño: desde el
lado que recibe, «aparato roto» y «red caída» **son el mismo silencio**. La
sesión lo dice así, que es más honrado y más útil que la versión que tenía
escrita antes de medirlo.

### S7 · `DATOS`

Las 120 medidas que recogería la clase: **cuatro jornadas de 30**, que barren el
**mismo** margen de magnitud real y que solo se diferencian en el **desvío de su
sensor** (0, +45, −45 y **+180** unidades: la cuarta es otra maceta). La regla
de verdad es `magnitud + 1,2 · tendencia > 560`, y el modelo no la conoce.
Medido sobre el riego con 40 ejemplos:

| | en sus ejemplos | en los de prueba | modelo tonto | umbral a mano |
|---|---|---|---|---|
| al azar, solo la lectura | 78 % | 75 % | 50 % | 80 % |
| al azar, lectura + tendencia | 98 % | **93 %** | 50 % | 80 % |
| por jornada, solo la lectura | 85 % | 73 % | 50 % | 60 % |
| por jornada, lectura + tendencia | **100 %** | **73 %** | 50 % | 60 % |

Un solo mando, y el número pasa de 93 % a 73 % **sin cambiar ni los ejemplos ni
el modelo ni el acierto sobre los suyos**. Eso vale para los tres proyectos
(ventilación 93 → 77, lámpara 88 → 67), y el verificador lo comprueba como
aserción en los tres.

Los otros dos hallazgos: **con una sola característica, entrenar y poner un
umbral son lo mismo** (78/75 frente a un umbral a mano que saca 80 %), y en ese
caso el `si` de una línea **gana**; y la tendencia —lo que se guardó en la S5—
sube el acierto de 75 % a 93 %.

### S8 · `SISTEMA`

Catorce días del sistema entero como **máquina de estados** (ARRANQUE,
VIGILANDO, ACTUANDO, ESPERA, MODO SEGURO), con cuatro averías que se encienden a
mano y tres protecciones que se quitan. La salida es la ficha de defensa:

| | riegos | de más | tierra seca | encharcada | avisos | registros | se entera |
|---|---|---|---|---|---|---|---|
| sin averías | 5 | 0 | 1,9 h | 0 | 58 | 128, **544 perdidos** | — |
| sonda fuera, **sin** modo seguro | **198** | **197** | 40 min | **9,5 días** | 216 | 128, 544 perdidos | **NO se entera** |
| sonda fuera, **con** modo seguro | 6 | 5 | **3,7 días** | 1,4 días | 62 | 128, 544 perdidos | día 5, 15:55 |
| lo mismo, pero es puente | 6 | 5 | 3,7 días | 1,4 días | 62 | igual | día 8, 00:00 |
| se cae la red | 5 | 0 | 1,9 h | 0 | 58, 1 esperó **3,8 h** | igual | — |
| corte de luz, sin reloj | 5 | 0 | 1,0 h | 0 | 58 | 17, **7 sin hora** | — |
| corte de luz, con reloj de pila | 5 | 0 | 1,0 h | 0 | 58 | 17, 0 sin hora | — |
| guardo solo cuando pasa algo | 5 | 0 | 1,9 h | 0 | 58 | **16, 0 perdidos** | — |

Lo mejor de esta escena es lo incómodo: **con el modo seguro puesto, el tiempo
con la tierra seca SUBE** (de 40 min a 3,7 días). Está explotado en el texto, en
una pregunta con trampa de la práctica y en el ticket de salida: el modo seguro
no arregla nada, **cambia un fallo silencioso por uno que avisa**. Sin él la
planta no está mejor: está ahogada nueve días y medio y nadie se ha enterado.

Y un hallazgo que sale gratis y que no esperaba: **sin averías ninguna, el
sistema ya pierde 544 registros**, porque los 1.024 bytes de EEPROM de un
Arduino Uno se llenan el **día 3 a las 16:00** guardando uno cada media hora.
Los datos con los que ibas a defender el proyecto son los de los tres primeros
días. Con «guardo solo cuando pasa algo» son 16 registros y no se pierde ninguno.

---

## 4 · Decisiones que conviene revisar

1. **El test de la S8 usa `test('c6b', ...)`**, con sus propios `name="c6b-N"`.
   El verificador comprueba que los dos conviven, que hay **30 radios `c6-N` y
   36 `c6b-N`** y que contestar uno no marca nada en el otro. Ninguna clase CSS
   nueva empieza por `test-`; los prefijos son `mem-`, `avi-`, `dat-` y `sis-`,
   y ningún identificador empieza por `ses-`.

2. **El generador de azar es un Lehmer (MINSTD, ×16807 mod 2³¹−1)**, no el LCG
   clásico. Con `1103515245` el producto se sale de los 2⁵³ que un `double`
   guarda exacto y JavaScript y Python dejan de dar lo mismo, así que el
   verificador no podría rehacer la cuenta. Es la misma decisión que se tomó en
   la unidad 4, por la misma razón.

3. **Los picos de la S5 se sortean aparte del ruido y son siempre seis.** La
   primera versión los sorteaba uno por medida con probabilidad fija, y a un
   proyecto le tocaban 3 y a otro 14: la comparación entre reglas estaba
   midiendo la suerte de la semilla. Lo cacé mirando la tabla del gemelo, no
   leyendo el código.

4. **El perceptrón de la S7 es «de bolsillo»** (se queda con los mejores pesos
   que ha visto), y el de la S4 no. Hace falta porque estos ejemplos **no son
   separables** y sin eso el resultado dependía de con qué ejemplo acabó la
   última pasada: la curva de aprendizaje salía a saltos sin significar nada.
   Está explicado dentro de la página, en el pie de la escena y en un «solo para
   entenderlo», con su cita (Gallant, 1990). **Si a alguien le parece demasiado
   detalle para 4.º, es lo primero que yo quitaría del texto** —pero no del
   código, donde hace falta.

5. **Los guiones de las escenas son nuestros y está dicho dentro de la página.**
   El perfil del día de la S5, las incidencias y la caída de red de la S6, el
   desvío de las cuatro jornadas de la S7 y las cuatro averías de la S8 son
   invención nuestra, elegida para que se parezca a lo que hacen esos sensores.
   Lo que se sostiene es la **comparación** entre opciones, no las fechas ni la
   forma exacta de las curvas. Cada pie de escena lo dice con esas palabras.

6. **Los datos de hardware sí son reales y verificables**: 2.048 bytes de SRAM,
   1.024 de EEPROM y ~100.000 escrituras por celda del ATmega328P; el ESP-01 a
   3,3 V frente a los 5 V del Uno; el *Keep Alive* y el mensaje *Will* de MQTT.
   Los precios (≈2 € el ESP-01, ≈5 € un ESP32, ≈1 € un reloj con pila) son
   órdenes de magnitud de tienda, no presupuestos.

7. **En la página no hay ni un emoji** ni ningún carácter por encima de U+2100
   (comprobado sobre el HTML generado), y `comprueba_paginas.py` no encuentra
   NUL ni caracteres rotos.

---

## 5 · Qué comprueba el verificador ampliado

`generadores/c6_verifica.py` pasa de **116 a 591 comprobaciones**. Lo nuevo se
apoya en `c6b_gemelos.py`, que implementa **los mismos cuatro modelos escritos
otra vez en Python**, a partir de la definición y no copiando el JavaScript. Si
una escena dejara de calcular y empezara a enseñar números escritos a mano, las
dos cuentas dejarían de coincidir.

- **S5**: once combinaciones de (regla, N, tipo de dato, picos sí/no, umbral)
  contra el gemelo, comparando arranques falsos, falsas alarmas, se-le-pasan,
  episodios, retardo y bytes. Más cuatro afirmaciones como aserciones: que la
  mediana de 5 quita lo que la media de 5 no quita, que más N es más retardo,
  que `byte` ocupa la mitad que `int` y que la tendencia se adelanta. Y que el
  panel de código se reescribe (`const byte N = 14`, `ordena(c, N)`, `x / 4`,
  «ni miro lo guardado») y que el mando de N se desactiva con el último valor.
- **S6**: once combinaciones de (proyecto, política, regla, periodo, latido,
  red, cola, mudo) contra el gemelo: salen, llegan, perdidos, incidencias,
  nunca-se-supieron, falsas alarmas de silencio y si el silencio se descubre.
  Más cinco afirmaciones: la proporción de mensajes entre periódico y evento,
  que sin latido no se descubre el silencio, que el último valor dispara más
  mensajes que la media, que la cola convierte un «nunca» en un «tarde» y que un
  latido rápido convierte la caída de red en falsa alarma.
- **S7**: **36 combinaciones** (3 proyectos × 2 cortes × 2 juegos de
  características × 3 tamaños) contra el gemelo, comparando los cuatro números,
  y el umbral a mano **con su valor** (`lectura > 556`). Más, para los tres
  proyectos: que partir por jornada hunde el acierto más de 10 puntos, que aun
  así sigue acertando ≥90 % de los suyos, y que la tendencia sube el acierto.
- **S8**: doce escenarios de averías y protecciones contra el gemelo,
  comparando actuaciones, actuaciones de más, avisos, avisos perdidos,
  registros, bytes de EEPROM, registros que no cupieron, registros sin hora,
  veces en modo seguro y el estado final. Más siete afirmaciones, entre ellas la
  incómoda (el modo seguro deja **más** tiempo sin resolver) y que el mando de
  instante mueve el estado resaltado en el diagrama, que tiene que ser
  exactamente uno.
- **Los dos tests**, por separado y sin pisarse los `name`.
- **Bloques de libreta, «solo para entenderlo», escena, vídeo, foto y crédito**
  para las **ocho** sesiones (antes solo las cuatro primeras), y que no queda
  ninguna sesión deshabilitada ni ningún cuerpo de sesión «en preparación».

---

## 6 · Dudas y cosas que debería mirar un humano

1. **Los cuatro vídeos: nadie los ha visto enteros.** Título y canal
   comprobados con la API oEmbed de YouTube el **18-sep-2026**, y eso es todo lo
   que dice la API. La página lo advierte en cada uno. **Hay que verlos antes de
   ponerlos en clase.** El de la S5 (`Pl79Ni3NUsY`, *Electgpl*) puede entrar en
   filtros de primer orden, que se va de 4.º; el de la S7 (`MR0YTI5OB9I`) habla
   de redes neuronales y puede dar por supuesto más nivel del que hay aquí.

2. ⚠️ **La primera mitad usa un proyecto que ya no existe.** No lo he tocado,
   como dice el encargo. El **contenedor que avisa cuando está lleno** aparece
   en **seis sitios** de `c6_build.py` (líneas 106, 257, 518, 642, 706 y 826), y
   `PROYECTOS.md` lo descartó para 4.º el 18-sep: se va a 2.º porque su gracia
   era la radio entre dos placas y en Arduino eso pide módulo aparte. El caso
   grave es la **línea 706**: el reto inicial entero de la sesión 4 («escribid
   el `si` que distinga papel de plástico») está construido sobre el contenedor,
   así que no es cambiar una palabra. Los otros cinco sí son sustituciones
   pequeñas por lámpara o ventilación. **Esto hay que decidirlo antes de dar la
   unidad**, porque el alumno va a preguntar por un proyecto que no puede elegir.

3. **La foto del ATmega328 no dice qué bloque es qué.** Es una foto del die a
   20 aumentos y se ve perfectamente la diferencia entre las zonas regulares
   (memoria) y las revueltas (lógica), que es lo que afirma el pie. **No he
   podido verificar cuál de los bloques regulares es la SRAM, cuál la Flash y
   cuál la EEPROM**, así que el pie no lo dice: solo enumera las tres memorias
   que hay dentro. Si alguien tiene una identificación fiable, el pie mejora
   mucho señalando el bloque de 2 kB.

4. **La foto de la S7 es de 800 px** (es lo que hay en Commons) y lleva impresa
   abajo la banda de crédito del archivo de Harvard. Pasa el mínimo del
   verificador (600) pero es la de menos resolución de las cuatro.

5. **Roce con la unidad 4, que conviene contrastar con quien la escribió.** La
   frontera acordada está respetada y dicha en la página (un recuadro entero de
   la S5: la histéresis es control y es de la unidad 4; aquí el problema es que
   *la medida* es mala). Pero hay un solape real: la **S6 de la unidad 4** ya
   lleva «la media de 10» como una casilla de su escena del sketch de riego.
   Aquí esa media es el asunto de la sesión, con su coste en bytes y en
   retardo, y el texto lo trata como «ahora vais a ver por qué funcionaba». Creo
   que se sostiene, pero **si alguien da las dos unidades seguidas, que mire si
   suena a repetido**.

6. **La S8 dice explícitamente dónde acaba** (recuadro «Dónde acaba esta
   unidad»): el criterio **3.1**, presentar y defender, es de las unidades 1 y 2,
   y aquí solo se prepara el **contenido técnico** de esa defensa. Por eso la S8
   lleva el chip `C.3` pero **no** un chip de CE3. Si al recoger se prefiere que
   lo lleve, es una línea en `c6b_texto.py`.

7. **Los minutados de la S8 no suman igual que los demás**: 10+22+20+8 en vez de
   10+25+20+5, porque el test de la unidad entera son 12 preguntas y no caben en
   cinco minutos. Es la misma licencia que se tomó la S4 de esta unidad.

8. **La práctica de la S7 pide etiquetar veinte medidas de verdad**, y eso
   supone que el grupo tiene un registro de días anteriores. Está previsto el
   atajo (usar las de la sesión 5), pero **conviene que el profesor ponga a
   registrar los aparatos al empezar la segunda mitad**, no el día de la S7.

9. **`generadores/guion_c6.txt` y el audio del narrador siguen siendo los de la
   primera mitad**, así que la voz de la S1 no menciona nada de las sesiones
   nuevas. No lo he tocado porque el encargo era escribir las sesiones; si se
   regenera el audio, conviene revisarlo.

10. **La lectura de aula (`lectura-tema6.pdf`) no se ha tocado** y sigue
    enlazada una sola vez, desde la sesión 1.
