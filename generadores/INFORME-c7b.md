# Informe · segunda mitad de la unidad 7 de 4.º (Robótica y automatismos)

Rama `c7b`. Sesiones **5, 6, 7 y 8**, escritas sobre la primera mitad ya
publicada. La página queda con **8 sesiones escritas y 0 pendientes**.

```
~/venv/bin/python generadores/c7_build.py     -> 8 sesiones (8 escritas, 0 pendientes)
~/venv/bin/python generadores/c7_verifica.py  -> 643 comprobaciones, 0 fallos
~/venv/bin/python generadores/c7b_lint.py     -> sin emojis, sin NUL, entidades cerradas
```

La página pasa de 199 KB a **384 KB**. El verificador pasa de 245 comprobaciones
a **643** (las 245 son las que declara `generadores/INFORME-c7.md`).

No se ha tocado nada de las sesiones 1 a 4 ni `4eso/Tecnologia/index.html`.

> **Nota de sitio.** El encargo pedía `INFORME.md` y ahí está, en la raíz. La
> primera mitad hizo lo mismo y luego se recogió como
> `generadores/INFORME-c7.md`; los de las otras unidades están como
> `generadores/INFORME-c4b.md`, `-c9b.md`, etc. Si prefieres esa convención es
> un `git mv INFORME.md generadores/INFORME-c7b.md`.

---

## 1 · Qué hay escrito

| | Título | Escena nueva | Foto | Vídeo |
|---|---|---|---|---|
| **S5** | En Tinkercad funcionaba | `BANCO` (`r5-`) | protoboard abierta por detrás | métodos de alimentación |
| **S6** | Lo apagas el viernes a 60°. El lunes cree que está en cero | `CASA` (`r6-`) | final de carrera de una Prusa i3 | homing y punto cero en CNC |
| **S7** | «No va a pasar» no es una respuesta | `PEOR` (`r7-`) | celda de soldadura vallada | seguridad en celdas robóticas |
| **S8** | «¿Funciona?» no se contesta con un sí | `ENTERO` (`r8-`) | Shakey (SRI, 1969) | la película original de Shakey |

Ficheros nuevos:

- `generadores/c7b_escenas.py` — escenas de S5 y S6.
- `generadores/c7b_escenas2.py` — escenas de S7 y S8.
- `generadores/c7b_texto.py` — el texto de las cuatro sesiones, sus fichas de
  práctica, sus cierres y el test `c7b`.
- `generadores/c7b_busca.py`, `c7b_fotos.py` — con los que se buscaron, se
  comprobó la licencia y **se miraron** las fotos candidatas.
- `generadores/c7b_capturas.py` — recorta las 17 vistas de las escenas nuevas a
  PNG, que es la única manera de ver si un dibujo está bien dibujado.
- `generadores/c7b_numeros.py` — imprime, desde los gemelos en Python del
  verificador, **todas las cifras que cita el texto**. Ninguna cifra de la
  página se ha escrito de memoria: se copia de aquí.
- `generadores/c7b_texto_plano.py` — vuelca el texto visible de las sesiones 5
  a 8 para releerlo como lo lee un alumno, no como lo escribe el generador.
- `generadores/c7b_lint.py` — busca emojis, bytes NUL y entidades HTML sin
  cerrar en la página generada.
- `img/c7-protoboard-contactos.jpg`, `c7-final-carrera.jpg`,
  `c7-celda-vallada.jpg`, `c7-shakey.jpg`.

Cambios en ficheros existentes: `generadores/c7_build.py` (importa `c7b_texto`
y sustituye los cuatro `pendiente=True`) y `generadores/c7_verifica.py`
(ampliado, ver §5).

---

## 2 · La decisión de fondo: el proyecto ya está elegido

La primera mitad rota entre los cinco candidatos porque cuando se escribió el
proyecto no estaba decidido. Estas cuatro aterrizan en lo que dice
`PROYECTOS.md` (bloque DECIDIDO, 18-sep-2026): **riego automático** como
proyecto principal, con **ventilación** y **lámpara** como variantes.

Cómo se ha repartido:

- **S5** abre con el aviso de que a partir de aquí el proyecto va en serio, y
  su escena deja elegir el actuador entre **bomba, servo, ventilador y tira de
  LED**: cada grupo encuentra el suyo y la cuenta es la misma.
- **S6** es la que más se parte en dos. La mitad mecánica (referenciar contra
  un final de carrera) es de los grupos que mueven algo; para **ventilación y
  lámpara**, que no mueven nada, hay un recuadro propio —«si tu proyecto no
  mueve nada, tu casa es otra»— con el **arranque conocido**: actuadores
  apagados, descartar las primeras lecturas, comprobar que la lectura es
  posible y dejar constancia de que ha arrancado. **Es la decisión que menos
  seguro tengo**; ver §6.
- **S7 y S8** van sobre el riego en las escenas, pero las prácticas están
  redactadas para que cualquiera de los tres las haga con su máquina: la tabla
  de caso peor de la S7 y la ficha técnica de la S8 son formularios, no
  respuestas.

Las escenas de S7 y S8 comparten constantes con la unidad para que un alumno
pueda llevarse un número de una a otra: la maniobra dura **4 s**, el tope de
tiempo son **6 s**, el brazo mide **210 mm** (el mismo de la sesión 3), la
bomba echa **100 ml/min** y el tope mecánico está a **95°**.

---

## 3 · Lo que enseña cada escena, y qué calcula

Las cuatro simulan de verdad. Ninguna tiene un número escrito a mano.

**S5 · `BANCO`.** Resuelve la tensión del bus tratando el motor frenado como
una resistencia fija (R<sub>m</sub> = 5 / I<sub>frenado</sub>), lo que da una
ecuación cerrada en vez de una resta que se iría a números imposibles:

```
V = (V₀ − R·I_placa) / (1 + R·I_frenado/5)
```

y encima simula **30 segundos de reloj a pasos de 10 ms** con la máquina de
estados de la S4 dentro: si la tensión baja de 2,70 V, la placa se reinicia,
`estado` vuelve a cero, la tierra sigue seca y vuelve a arrancar. Lo medido:

| fuente / montaje | V en el arranque | reinicios en 30 s | maniobra |
|---|---|---|---|
| USB, una fuente | 3,95 V (zona gris) | 0 | sale en 4,2 s |
| pilas AA nuevas | 4,14 V (zona gris) | 0 | sale |
| pilas AA usadas | **2,51 V** | **19** | **no sale** |
| pilas usadas, soldado | 2,61 V | **19** | **no sale** |
| pilas usadas, dos fuentes | 5,03 V | 0 | sale en 4,9 s |
| fuente de 5 V y 2 A | 4,56 V | 0 | sale |

Lo que más me gusta de esta escena es la fila del **soldado**: mejora la
tensión y **no arregla nada**, porque el problema está en la fuente. Y el modo
«sin masa común», donde la máquina no hace absolutamente nada y no hay un solo
cable roto que enseñar.

**S6 · `CASA`.** Ocho referenciados, cada uno saliendo de un sitio distinto.
La repetibilidad sale de tres sumandos declarados: velocidad × periodo del
lazo, velocidad × 18 ms de frenada, y el **±0,30 mm del propio microrruptor**,
que es un suelo que no baja por ir despacio. Con la semilla 5:

| | dispersión | tiempo | choques |
|---|---|---|---|
| una pasada a 200 mm/s | 2,000 mm | 0,49 s | 0 de 8 |
| una pasada a 20 mm/s | 0,400 mm | 4,72 s | 0 de 8 |
| **dos pasadas desde 200** | **0,420 mm** | **0,99 s** | 0 de 8 |
| dos pasadas, microrruptor bueno | 0,060 mm | 1,00 s | 0 de 8 |
| una pasada a 300 con lazo de 60 ms | 12,000 mm | 0,36 s | **8 de 8** |

La última fila es el remate de la sesión 4: un lazo de 60 ms es lo que deja un
`delay(50)` mal puesto, y aquí no pierde eventos, **rompe el carro**.

**S7 · `PEOR`.** Tres fallos en pestañas, cuatro protecciones que se encienden
y se apagan, y una matriz de 4 × 3 que enseña lo que más cuesta creerse: **cada
protección tapa un fallo y solo uno**.

- *Se atasca*: modelo térmico de primer orden, T = 22 + P·R<sub>th</sub>·(1 −
  e<sup>−t/τ</sup>) con P = 7,5 W, R<sub>th</sub> = 16 °C/W y τ = 240 s. Sin
  tope llega a **142 °C** y pasa de 120 °C a los **6,8 min**; con tope se queda
  en **24 °C**. La protección es una línea de código.
- *Alguien mete la mano*: distancia = velocidad × (10 + 20 + 18) ms. A 400 mm/s
  son **19 mm**; a 800, **38**. La energía se da además traducida a algo que se
  puede imaginar: 0,02 J = **dejar caer 7 g desde 30 cm**.
- *Se va la luz*: el desfase entre lo que la máquina cree y dónde está el
  mecanismo, en grados **y en milímetros de punta** con la fórmula L·ε de la
  sesión 3. Y el detalle que cierra el círculo con la S5: **separar las fuentes
  creó un fallo nuevo**, porque un relé enclavado se queda abierto aunque la
  placa se muera. Doce horas a 100 ml/min son **72 litros**.

**S8 · `ENTERO`.** Veinticuatro horas minuto a minuto con las cuatro cosas de
la unidad como cuatro interruptores. El día trae cuatro sucesos y **cada uno lo
aguanta exactamente uno** de los cuatro:

| | agua a la planta | agua en el suelo | humedad mínima | reinicios | motor bloqueado | golpes |
|---|---|---|---|---|---|---|
| nada puesto | 0 ml | 0 ml | **4,2 %** | **287** | 0 min | 0 |
| solo alimentación | 400 ml | **4600 ml** | 16,2 % | 1 | 0 min | 0 |
| sin topes | 1000 ml | 200 ml | 26,3 % | 1 | **120 min** | 0 |
| sin máquina de estados | 1000 ml | 200 ml | 26,2 % | 1 | 6 min | **1** |
| **las cuatro** | 1000 ml | 200 ml | 26,2 % | 1 | 6 min | 0 |

(«Golpes» es las veces que el brazo siguió moviéndose con la mano delante. Es
la única columna que distingue la fila de «sin máquina de estados» de la de
abajo, y eso es exactamente lo que hay que ver: un fallo que no cuesta agua.)

Dos hallazgos que el texto explota:

1. Sin **alimentación separada** no se puede demostrar ninguna de las otras
   tres: el día entero da cero mililitros. Hay un orden para arreglar las
   cosas y ese es el primero.
2. Quitar los **topes** cambia los minutos de motor bloqueado de 6 a 120 y
   **no cambia la humedad de la planta** (26,2 frente a 26,3 %). Hay fallos que
   no se ven en el resultado, y ese es el argumento de la sesión 7 entero.

Y los 200 ml del suelo **no bajan a cero** ni con las cuatro puestas: son los
dos minutos en que la válvula estuvo abierta durante el apagón. El texto lo
dice en vez de disimularlo, porque es la diferencia entre «no falla» y «falla
lo mínimo que se puede».

---

## 4 · Decisiones que conviene revisar

1. **El test de la S8 usa `test('c7b', ...)`**, con sus propios `name="c7b-N"`.
   El verificador comprueba que los dos tests conviven, que hay 30 radios `c7-N`
   y 30 `c7b-N`, y que contestar uno no marca nada en el otro. Ninguna clase CSS
   nueva empieza por `test-`; los prefijos son `r5-`, `r6-`, `r7-` y `r8-`.

2. **Los modelos son modelos, no medidas.** Las resistencias internas de las
   pilas, los 18 ms de frenada, los ±0,30 mm del microrruptor barato, los
   16 °C/W del motor y los 0,9 → 1,8 puntos de humedad por hora son **valores
   razonables elegidos por nosotros**. Lo que se sostiene es la forma de las
   curvas y la comparación entre dos configuraciones. Los dos números que
   **sí** están en una hoja de características son los umbrales de la placa
   (2,7 V de brown-out y 4,5 V para 16 MHz) y así se dice en la página.

3. **El `masa` de la escena de la S7 iba con `step="20"` y el valor por defecto
   era 250**, que no cae en la rejilla: el navegador lo redondeaba a 260 sin
   avisar y el verificador no cuadraba. Se cambió a `step="10"`. Lo cacé
   escribiendo el verificador, no leyendo el código. Conviene recordarlo para
   otras escenas: **un `value` fuera del `step` se mueve solo**.

4. **Los redondeos se comparan con `jsround`, no con `round`.** `Math.round`
   de JavaScript manda el 0,5 hacia arriba y el `round` de Python lo manda al
   par: el ángulo de 40,5° salía 41 en pantalla y 40 en el gemelo. El
   verificador ya traía ese ayudante de la primera mitad; ahora lo usan también
   las comprobaciones nuevas.

5. **El generador de azar es el mismo LCG de las escenas 1 y 2** (×1664525 con
   `Math.imul`), que sí se puede rehacer exacto en Python. No se ha cambiado
   nada de eso.

6. **En la página no hay ni un emoji** y no hay bytes NUL: lo comprueba
   `c7b_lint.py` en cada compilación.

---

## 5 · Qué comprueba el verificador ampliado

`generadores/c7_verifica.py` pasa a **643 comprobaciones**. Lo nuevo:

- **S5**: catorce combinaciones de (fuente, montaje, cableado, actuador, largo)
  contra un gemelo en Python, comparando resistencia, desglose, corriente,
  tensión en el arranque y en marcha, reinicios y si la maniobra se completa.
  Y las cinco afirmaciones de la sesión como aserciones: el USB cae en zona
  gris, las pilas usadas reinician, soldar no lo arregla, dos fuentes sí, y sin
  masa común no se mueve nada.
- **S6**: nueve combinaciones de (velocidad, lazo, interruptor, modo, semilla)
  contra el gemelo, incluyendo **los ocho ceros uno a uno**. Y las lecciones:
  despacio dispersa menos pero tarda más; dos pasadas dan la dispersión de la
  lenta en el tiempo de la rápida; el interruptor bueno baja el suelo a la
  mitad y más; un lazo de 60 ms a 300 mm/s choca las ocho veces y uno de 2 ms,
  ninguna.
- **S7**: los tres modos contra sus tres fórmulas (cinco casos de atasco, seis
  de la mano, seis de la luz), más la matriz de 12 casillas, más que **las
  otras tres protecciones no le hacen nada al atasco** (la misma temperatura
  con todas encendidas que solo con el tope), más que la referencia al arrancar
  **no tapa** el relé enclavado.
- **S8**: ocho combinaciones de los cuatro interruptores contra el gemelo, once
  cifras por combinación. Y el barrido que demuestra que cada interruptor mueve
  un número distinto.
- **Los dos tests**, por separado, y que no se pisan los `name`.
- Bloques de libreta, «solo para entenderlo», escena, vídeo, foto (≥ 900 px) y
  crédito para las **ocho** sesiones, no solo las cuatro primeras.
- Que hay ocho botones de sesión, ninguno deshabilitado, ocho cuerpos y ningún
  rótulo de «sesión en preparación».
- Que los cuatro vídeos nuevos llevan el aviso de que nadie los ha visto.

Los gemelos en Python están escritos **a partir de la definición**, no copiados
del JavaScript: si una escena dejara de calcular y empezara a fingir, la
comparación lo caza.

---

## 6 · Dudas y cosas que debería mirar un humano

1. **Los cuatro vídeos: nadie los ha visto enteros.** Título y canal
   comprobados con la API oEmbed de YouTube el 18-sep-2026, y eso es todo lo
   que dice la API. La página lo advierte en cada uno. **Hay que verlos antes
   de ponerlos en clase.** Dos avisos concretos:
   - el de la **S7** (`AtNxx-jaIt4`, «Seguridad en Celdas Robóticas») va sobre
     la norma ISO 10218, que se sale de 4.º; lo que interesa es el orden de las
     medidas;
   - el de la **S8** (`GmU7SimFkpU`) es la película original del SRI de 1972 y
     **está en inglés, sin subtítulos**. Lo he puesto porque se entiende
     mirando y porque cierra la unidad con el robot de la foto, pero si en el
     aula eso no funciona, se quita y no se pierde nada del hilo.

2. **Colisión de títulos con la unidad 5.** Su sesión 5, todavía pendiente, se
   llama **exactamente igual que la mía: «Del esquema al montaje»** (ver
   `generadores/c5_build.py:1239`), y su sesión 8 pendiente es «El automatismo
   completo», muy cerca de mi «El robot entero». Como la 5 no está escrita, he
   seguido adelante con el título que anunciaba el cierre de mi sesión 4, pero
   **esto hay que resolverlo entre las dos unidades**. Mi propuesta: lo que yo
   trato es **de dónde sale la corriente de cada cosa y cómo se sujeta**; lo que
   le queda a la unidad 5 es **qué pieza va entre el pin y el actuador**
   (transistor, MOSFET, relé, diodo de recirculación) y cómo se calcula. La
   página lo dice con esas palabras en un recuadro de la S5.

3. **Roce con la segunda mitad de la unidad 4, que ya está publicada.** Su
   sesión 8 («El sistema entero: provocar el fallo, el estado seguro,
   defenderlo con un número») y mi sesión 7 comparten tres cosas: el análisis
   de modos de fallo, la idea de estado seguro y la de provocar el fallo en vez
   de esperarlo. Lo he separado así, y lo digo dentro de la página:
   - la **unidad 4** se lo hace al **lazo de control** (la sonda miente, el
     depósito se acaba, alguien riega a mano);
   - la **unidad 7** se lo hace a la **máquina**: lo que se mueve, lo que
     calienta y lo que puede pillar un dedo.
   Lo que aporto de nuevo y no está en la 4: el **tope de tiempo de maniobra**
   con su cuenta térmica, la **distancia de reacción** de un sensor de
   seguridad, la **jerarquía de medidas** (quitar > guarda > sensor > aviso >
   formación) y la **posición sin corriente como decisión de compra**. Aun así,
   **si alguien lee las dos seguidas va a notar el eco**, y quien coordine las
   unidades debería decidir si sobra algo.

4. **El recuadro del «arranque conocido» para ventilación y lámpara.** Es la
   decisión que menos seguro tengo de toda la entrega. La escena de la S6 es
   mecánica —un carro contra un final de carrera— y esos dos grupos no tienen
   nada que referenciar; lo que reciben es un recuadro de teoría con cuatro
   puntos y una cuarta parte de la práctica redactada para ellos. Creo que
   aguanta, pero **si a la vista del aula parece poco, es lo primero que yo
   cambiaría**: se podría añadir a la escena una pestaña «sin partes móviles»
   que simule las primeras lecturas de un sensor recién encendido.

5. **La práctica de la S7 pide provocar un fallo de verdad.** Está limitada a
   diez segundos con el motor empujando y a los fallos que no rompen nada, y
   así se dice. Aun así, **un profesor debería decidir cuáles se permiten en su
   taller** antes de la sesión, sobre todo si algún grupo tiene agua y
   electrónica cerca.

6. **Dos cosas de la primera mitad que no he tocado** (el encargo dice que las
   diga en vez de arreglarlas):
   - En la **sesión 4**, el código del reto es
     `subirBarrera(); delay(3000); delay(5000); bajarBarrera(); delay(3000);`.
     Los dos `delay()` seguidos, sin nada en medio, se leen como que **el motor
     sigue subiendo durante los cinco segundos de espera**: falta la línea de
     parar. La escena de esa misma sesión sí la tiene (su panel de espagueti
     hace `subir → delay → parar → delay → bajar → delay`). Sugerencia: meter
     `pararMotor();` entre los dos `delay()` del reto, que además hace más
     evidente que son tres fases y no una espera de ocho segundos.
   - El **guion de la voz** (`generadores/guion_c7.txt`) es el de la primera
     mitad: anuncia las cuatro primeras sesiones y cierra con «Ocho sesiones.
     Empezamos», sin mencionar nada de las cuatro nuevas. No lo he tocado
     porque el encargo era escribir las sesiones, pero si se regenera el audio
     conviene añadirle un párrafo.

7. **Fronteras que creo respetadas**, y así lo dice la página con todas las
   letras:
   - el **control proporcional** y el análisis de fallos del **lazo** son de la
     unidad 4, y se remite a ella dos veces;
   - la **electrónica** entre el pin y el actuador se usa ya montada y se
     remite a la unidad 5;
   - el **impacto ambiental** es de la unidad 8 y **a quién sirve el robot** es
     de la 9: las dos aparecen, por su nombre, en el cierre de la sesión 8 como
     las dos preguntas que este tema **no** contesta;
   - la **estructura de una defensa** (a quién, con qué apoyo, cómo se reparte)
     es de las unidades 1 y 2, y se dice; lo que hace la S8 es lo que es propio
     de un robot: encenderlo delante, provocar un fallo en directo y enseñar un
     número medido.

8. **Las cuatro fotos están miradas, una a una**, no solo comprobadas por la
   API. Las descartadas y el motivo están escritos en la cabecera de
   `generadores/c7b_fotos.py`. La que más me costó es la de la S7: es una celda
   de soldadura y **el robot no se ve**, así que el pie no dice que se vea; lo
   que describe es lo que sí está en la imagen —el bastidor, las cortinas y el
   cuadro de mandos **por fuera**—, que es justo el escalón 2 de la jerarquía.
   Si alguien encuentra una con un brazo dentro de su valla, mejor.
