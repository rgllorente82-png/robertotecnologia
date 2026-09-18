# Informe · 4.º de ESO · Tema 7 · Robótica y automatismos

Rama `c7`. Entregadas las **cuatro primeras sesiones** de ocho; las otras cuatro
quedan en la barra con su título y el botón desactivado.

> **Nota de sitio.** El encargo pedía `INFORME.md` y ahí está, en la raíz. Pero
> las unidades anteriores de esta serie dejaron el suyo en
> `generadores/INFORME-c4.md`, `-c5.md` y `-c6.md`. Si prefieres esa convención,
> es un `git mv INFORME.md generadores/INFORME-c7.md` y ya.

---

## Qué hay entregado

| Fichero | Qué es |
|---|---|
| `4eso/Tecnologia/tema7/index.html` | La unidad. 199 KB, generada. |
| `4eso/Tecnologia/tema7/lectura-tema7.pdf` | Lectura de aula: 30 párrafos numerados + 10 preguntas, 5 páginas A4. |
| `generadores/c7_build.py` | El generador de la página. |
| `generadores/c7_escenas.py` | Escenas de las sesiones 1 y 2. |
| `generadores/c7_escenas2.py` | Escenas de las sesiones 3 y 4. |
| `generadores/c7_lectura.py` | El PDF de la lectura. |
| `generadores/c7_verifica.py` | Verificador: **245 comprobaciones, 0 fallos**. |
| `generadores/c7_fotos.py` | Consulta la licencia en Commons y baja las cuatro fotos. |
| `generadores/c7_busca_fotos.py` | Buscó candidatas y las bajó a `/tmp` para mirarlas. |
| `generadores/c7_capturas.py` | Recorta cada escena a PNG en `/tmp/c7/`. |
| `generadores/c7_mirada.py` | La página entera de cada sesión, en escritorio y en móvil. |
| `generadores/guion_c7.txt` | Guion de la voz. |
| `audio/c7-robotica.mp3` + `_env_c7-robotica.json` | Voz (1 min 30 s) y su envolvente. |
| `img/c7-*.jpg` | Las cuatro fotos de Commons. |
| `generadores/voz.py` | **Recuperado**, ver más abajo. |

**No he tocado `4eso/Tecnologia/index.html`.** Aquí sí existe (a diferencia de lo
que le pasó a la rama `c6`), y está intacto: la tarjeta la pones tú.

---

## Cómo se ejecuta

```
~/venv/bin/python generadores/c7_build.py        # la página
~/venv/bin/python generadores/c7_lectura.py      # el PDF
~/venv/bin/python generadores/c7_verifica.py     # 245 comprobaciones
~/venv/bin/python generadores/c7_capturas.py     # PNG de cada escena en /tmp/c7/
~/venv/bin/python generadores/c7_mirada.py       # la página entera, escritorio y móvil
```

La voz, si hay que rehacerla:

```
~/venv/bin/python generadores/voz.py generadores/guion_c7.txt c7-robotica
```

---

## Decisiones, y por qué

### 1. `generadores/voz.py` no estaba en esta rama, otra vez

Igual que le pasó a `c6`. El fichero existe en las ramas `tema7`/`tema8` de 2.º y
en `e869995` (la U5 de 4.º), pero ninguna es antepasado de `c7`, así que aquí no
había nada. Lo he vuelto a poner **tal cual** desde `e869995`, sin cambiarle una
línea, y va commiteado.

**Para mirar:** ya van dos ramas seguidas recuperándolo a mano. O se mezcla en
`main`, o esto va a volver a pasar en la unidad siguiente.

### 2. La sesión 2 no es la que proponías, y creo que es importante

La propuesta decía: *«Motores: cuál y por qué. Corriente continua, servo y paso a
paso, con la cuenta de par y velocidad, la reductora y el porqué de cada uno.»*

El problema es que **eso ya está dado**, y bien dado, en la **U4, sesión 4**
(`generadores/c4_build.py`). Allí están M = F·d, los kg·cm de los catálogos, la
relación de transmisión, M₂ = M₁/i·η, P = M·ω, el criterio para elegir motor con
su margen de 2, el servo SG90 abierto por dentro y hasta el banco de pruebas con
los engranajes dibujados a escala. Repetirlo aquí habría sido regalarles una
sesión ya vista.

Lo que **no** hay en ninguna unidad, y es justo lo que separa un motor de un
motor de robot, es esta pregunta: **¿el motor sabe dónde está?** Así que la
sesión 2 va por ahí:

- El reto es `delay(2300)` y las cinco pruebas que dan cinco distancias.
- El cuerpo es qué te promete cada motor: el de corriente continua **nada**, el
  servo un ángulo (pero no te contesta), el paso a paso un número de pasos
  contados, y el de encoder la única medida del resultado. Entra el **paso a
  paso**, que en la U4 no aparecía ni de pasada, con su paso angular y sus mm por
  paso.
- Y el cierre es **exactitud frente a precisión**, con la escena midiéndolo.

De paso, esa pareja de palabras vuelve en la sesión 3 (repetibilidad de los
catálogos de robots) y en la lectura (el Unimate). Creo que se gana bastante.

La parte de la propuesta que **sí** está tal cual es la escena: los tres motores
con el mismo encargo, uno al lado de otro.

Las otras tres sesiones van como las proponías, con el orden intacto.

### 3. El proyecto del curso, sin decidir: cómo lo he resuelto

Ningún ejemplo se casa con uno solo. Cada vez que hacía falta un caso concreto he
usado **dos o tres** de los cinco de `PROYECTOS.md`, y las cuatro actividades
piden explícitamente «elegid **dos** de los proyectos del curso».

Dónde aparece cada uno:

| | S1 | S2 | S3 | S4 |
|---|---|---|---|---|
| 1 · Riego | ✔ | ✔ | ✔ | ✔ (piel de la escena) |
| 2 · Ventilación | | | | |
| 3 · Contenedor | ✔ | ✔ | ✔ | ✔ (piel de la escena) |
| 4 · Barrera | | ✔ | | ✔ (piel de la escena) |
| 5 · Lámpara | | ✔ | ✔ | |

**Donde he tenido que elegir, y lo digo porque el encargo lo pedía:**

- **La escena de la sesión 4 lleva tres pieles y no cinco**: barrera, riego y
  contenedor. Es que el **2 (ventilación)** y el **5 (lámpara)** no tienen
  automatismo *de ciclo*: no hay ida ni vuelta, solo un umbral con histéresis,
  que es lo de la U4. Con esos dos, la máquina de estados se queda en dos
  estados y no enseña nada. Si al final el proyecto del curso es el 2 o el 5,
  **la sesión 4 hay que retocarla**: la estructura reposo → actuar → mantener →
  volver no les encaja, y habría que montarla sobre otra cosa (por ejemplo, el
  ciclo de calibración o el de aviso escalonado).
- **La barrera es el ejemplo principal de la S4.** Es el que tiene un evento de
  seguridad de verdad («hay alguien debajo») y sin eso la sesión pierde su mejor
  argumento. En las otras dos pieles ese evento se llama «sigue seco» / «sigue
  lleno», que es lo mismo estructuralmente pero no da miedo.
- **El proyecto 2 (ventilación) no sale en ninguna sesión.** No es olvido: no
  tiene parte móvil, y esta unidad va de moverse por el mundo. Si acaba siendo el
  proyecto elegido, esta unidad es la que menos le va a servir tal cual está.

### 4. Las cuatro escenas: qué calcula cada una

Ninguna enseña un número escrito a mano. Todas las tablas salen de una cuenta que
el verificador **rehace en Python por separado**, escrita a partir de la
definición y no copiada del JavaScript.

- **S1 · El aula.** Una simulación de verdad: 34 × 22 casillas, tres «cerebros»
  (programa grabado, teledirigido, rebote con sensor de choque), dos juegos de
  muebles y una semilla de azar a la vista. Va toda con **enteros y ocho
  direcciones, sin un solo seno**, a propósito: así el navegador y Python dan
  *exactamente* el mismo número, y el verificador puede comparar casilla a
  casilla en vez de «aproximadamente».
  Los números que salen, y que están escritos en el texto de la sesión:

  | | cubierto | choques | pasos |
  |---|---|---|---|
  | grabado, aula como se grabó | 77,3 % | 24 | 242 |
  | grabado, muebles movidos | **47,2 %** | **124** | 242 |
  | sensor, muebles movidos (semilla 7) | 79,7 % | 67 | 900 |

  Me gusta que con el aula recogida **gane el grabado** (más cobertura, menos
  choques, un tercio de los pasos). Es verdad, y evita el sermón de «lo reactivo
  siempre es mejor». Lo que falla no es su eficiencia: es que **no se entera**.

- **S2 · Los tres motores.** El mismo encargo («avanza 500 mm») cinco veces con
  cada motor, con la física de cada uno declarada en el código. Separa el error
  sistemático de la dispersión. Con la rueda bien medida: dispersión de 19,2 mm
  el de tiempo, 1,8 mm el paso a paso, 3,7 mm el del encoder. Con la pila al 70 %
  el de tiempo se queda en 346 mm y a los otros dos **no les pasa nada**.

- **S3 · El brazo.** Cinemática directa con las cuentas a la vista, espacio de
  trabajo dibujado a escala (0,45 px/mm) y el problema inverso **resuelto** por
  el teorema del coseno para poder enseñar lo único que importa en 4.º: que hay
  **dos** soluciones, o ninguna. En la libreta solo va la directa; la inversa
  está rotulada como de Bachillerato.

- **S4 · La máquina de estados.** Ejecutable: cuatro estados, cinco eventos, la
  tabla de 20 casillas que se enciende sola, el código con la línea del estado
  resaltada y el actuador dibujado en su ángulo. Y el modo «espagueti con
  `delay()`», que cuenta los eventos que se come y las veces que baja la barrera
  con alguien debajo.

### 5. Dos cosas que tuve que arreglar después de mirar las capturas

Las dos las cazó el ojo, no el verificador, y por eso conviene seguir mirando los
PNG:

- **La mancha del error del brazo era invisible.** A 0,45 px/mm, ±4,6 mm son dos
  píxeles: el texto decía «mira la mancha roja» y no había nada que mirar. Ahora
  hay una **lupa ×10 con su regla de 5 mm** en una esquina de la escena, y se ve
  perfectamente que el error es un paralelogramo alargado, no un círculo.
- **El actuador de la sesión 4 parecía un mando deslizante.** Era una barra verde
  con un círculo negro en el extremo, y a 0° se confundía con un control. Ahora
  tiene mástil, suelo y punta roja, y se lee como lo que es.

### 6. La lectura: cinco casos reales con fecha

`4eso/Tecnologia/tema7/lectura-tema7.pdf`, 30 párrafos justos (lo comprueba un
`assert`) y 10 preguntas, las dos últimas de opinión razonada.

| Historia | Fecha | Qué sesión sostiene |
|---|---|---|
| Elmer y Elsie, las tortugas de Grey Walter (Bristol) | 1948-1951 | S1: con dos válvulas ya hay comportamiento |
| Robert Williams, planta de Ford en Flat Rock (Michigan) | 25-ene-1979 | S1: aquel brazo no percibía nada, y siguió trabajando |
| Opportunity atascado en Purgatory Dune (Marte) | abr-jun 2005 | S2: el encoder mide la rueda, no el suelo |
| El Unimate de General Motors (Nueva Jersey) | 1961 | S3: repetibilidad no es exactitud |
| Mars Pathfinder y sus reinicios | jul-1997 | S4: el programa era correcto; fallaba *cuándo* |

**Aviso sobre el caso de Robert Williams.** Es una muerte, contada con nombre y
apellidos. La he metido porque es el argumento más fuerte de toda la unidad —la
máquina hizo exactamente lo que se le dijo y no podía enterarse de nada más— y
está contada sin ningún morbo, con la solución de ingeniería detrás (vallas,
barreras de luz) y con el párrafo siguiente dedicado a los robots colaborativos
de hoy, que sí perciben. Dicho esto: **es tu clase y es tu decisión**. Si
prefieres quitarla, son los párrafos 7 a 12 de `c7_lectura.py` y hay que meter
otros seis para que sigan siendo 30.

---

## Lo que deberías mirar tú

### Los vídeos: **nadie se los ha visto enteros**

De los cuatro he comprobado por la **API oEmbed de YouTube** que el identificador
existe, y con qué título y qué canal aparece. Eso es todo lo que dice esa API. No
dice si el vídeo es bueno, ni si a mitad se pone a vender un curso, ni si el
canal ha cambiado de manos. **Hay que verlos.**

| Sesión | ID | Título que devuelve oEmbed | Canal |
|---|---|---|---|
| S1 | `cwf-cURBUkI` | Cómo Funciona y se Ensambla un Robot Aspirador | Ciencia y Tecnología al Desnudo |
| S2 | `e4VCK1N8JvM` | Qué es un motor paso a paso? \| Introducción | Cimech 3D |
| S3 | `9zSRNXRuX0g` | Cinemática Directa en Inversa de un Robot de 2 Grados de Libertad \| Método Geométrico | Sistemas Dinámicos y Control |
| S4 | `IrBwtuUwqbM` | Controlando tiempos con Arduino | Jorge García Ochoa de Aspuru |

El de la S3 es el más arriesgado: es de nivel universitario y la parte de la
inversa se sale de 4.º. Lo he presentado así en la nota que lleva debajo («la
parte de la inversa es de nivel Bachillerato»), pero si te parece demasiado, se
cambia.

### Las fotos: cuatro puestas, dos descartadas después de mirarlas

Las cuatro llevan licencia comprobada por la API de Commons **y las he abierto
una a una**. Eso segundo es lo que no comprueba ninguna API, y aquí se ha notado:

| Clave | Fichero de Commons | Autor | Licencia |
|---|---|---|---|
| S1 `c7-roomba-recorrido.jpg` | `File:Roomba time-lapse.jpg` | Chris Bartle | CC BY 2.0 |
| S2 `c7-rotor-paso-a-paso.jpg` | `File:Stepper motor rotor.jpg` | Dolly1010 | CC BY 3.0 |
| S3 `c7-scara.jpg` | `File:SCARA mit Stocker.jpg` | Hirata Robotics GmbH | **CC BY-SA 3.0 de** |
| S4 `c7-programador-lavadora.jpg` | `File:Machine laver programmateur.jpg` | Lac 16 | CC BY-SA 3.0 |

**Descartadas al abrirlas**, y las dejo apuntadas en `c7_fotos.py` para que no las
vuelva a elegir nadie:

- `File:UNIMATE PUMA 200 Robot Arm (6202074596).jpg`: es el primer plano de **un
  solo eslabón visto desde abajo**. No se le ve ni una articulación, que es justo
  lo que hacía falta para contar grados de libertad.
- `File:Programmable Logic Controller (PLC) CPU226.jpg`: 500 × 500 px, dentro de
  su caja de cartón y con la **marca de agua de una tienda** encima. La licencia
  dice CC BY-SA 4.0 y la foto parece de un catálogo ajeno.

**Dos cosas que conviene que mires:**

1. La del **SCARA** es **CC BY-SA 3.0 de** (la versión alemana de la licencia).
   Como todas las fotos de la web, conserva su propia licencia y va con su
   crédito, así que no hay problema; lo digo porque es la primera de esta serie
   con una licencia localizada.
2. La descripción de Commons del **rotor** dice solo «Stepper motor rotor»: **no
   dice el modelo ni el paso angular**. Por eso el pie no afirma nada de *ese*
   rotor: dice cómo es «el tipo más común, el de 1,8° por paso», con sus 50
   dientes. Si quieres afinar más, habría que encontrar una foto con ficha.

### Dudas y cosas que no me cuadran

1. **No sé qué son B.1, B.2, B.3 y B.4.** `CURRICULO.md` dice que el criterio 4.1
   de 4.º cubre los saberes «B.1 · B.2 · B.3 · B.4» y que el bloque B es
   «Comunicar ideas»… **pero eso es la lista de 2.º**. Para 4.º el documento no
   transcribe los saberes del bloque B en ningún sitio. He repartido los chips
   por sesión de forma razonable (B.1 en la de conceptos, B.2/B.3 donde hay
   esquemas y tablas, B.4 donde hay programación), pero **me lo estoy
   inventando**. Es el punto que más falta hace comprobar contra el BOJA, y no
   solo para esta unidad: afecta también a la U4 y a la U5.
2. **El dato de la indemnización de 1983** en la lectura (párrafo 11) lo doy sin
   cifra a propósito: he encontrado la cifra citada en varios sitios, pero no la
   he podido contrastar con una fuente que me convenza, así que digo «un jurado
   condenó al fabricante a indemnizar a su familia» y ya.
3. **Purgatory Dune**: lo que sí está firme es la fecha (se atascó a finales de
   abril de 2005 y salió a principios de junio) y el mecanismo (las ruedas
   giraban y el vehículo no avanzaba). **No doy ninguna cifra de cuánto marcó la
   odometría frente a lo que avanzó de verdad**, porque los números que circulan
   no coinciden entre sí. Si encuentras uno bueno, el párrafo 16 lo agradece.
4. **La escena de la S1 dibuja un robot que se mueve por casillas y en ocho
   direcciones.** Un aspirador de verdad va en cualquier dirección. Lo he hecho
   así para que la cuenta sea exacta y reproducible, y **lo dice el pie de la
   escena**; pero es una simplificación y conviene que la digas en clase.
5. **La velocidad de la escena de la S2 es un modelo, no una medida.** Los 220
   mm/s de calibración, el 0,82 de la moqueta, el 1 % y el 6 % de deslizamiento y
   el umbral de 300 mm/s para perder pasos son **números elegidos por mí para que
   el fenómeno se vea**, no medidos en un robot. El comportamiento (la pila
   afecta al de tiempo y no a los otros, la moqueta afecta a todos) sí es el
   real. Está dicho en el texto que es un modelo declarado, pero si quieres
   números de un motor concreto, hay que medirlos.
6. **La escena de la S1 no tiene botón de «cambiar la suerte»**: tiene un campo
   de semilla, que es mejor para el aula (todos ponen la misma y salen los mismos
   números) pero menos evidente. Si en clase resulta incómodo, se le añade un
   botón que ponga una semilla al azar en dos líneas.

---

## Las cuatro sesiones que faltan

Salen en la barra desactivadas **pero con título**, para que se vea la forma
entera de la unidad desde el primer día. Mi propuesta, encadenada con lo escrito
y sin pisar la U5 (electrónica y neumática) ni la U6 (programación e IoT):

| S | Título corto | Qué resuelve | Qué deja abierto |
|---|---|---|---|
| 5 | Del esquema al montaje | El pin da 20 mA y el motor pide 800. Driver (L298N / A4988), alimentación separada y **masa común**, que es el fallo número uno. Y por qué la placa se reinicia al arrancar el motor. | Ya se mueve, pero cada vez que lo enciendo empieza en un sitio distinto |
| 6 | Que sepa volver a casa | Finales de carrera, la maniobra de **homing** y por qué todo robot la hace al encender. Repetibilidad medida en el aula: diez idas y vueltas con una regla. | Ya sabe dónde está; no sé qué hace si algo va mal |
| 7 | Seguridad y caso peor | El caso peor, el paro de emergencia que corta **potencia** y no software, qué pasa si se va la luz a mitad de maniobra y quién responde. Recoge el caso de la lectura. | Tengo las piezas; falta que sea un aparato |
| 8 | El robot entero | Integrar sensor, motor, máquina de estados y carcasa. Medirlo (tiempo de ciclo, consumo, fallos por cada cien ciclos) y defenderlo. Enlaza con la CE3. | Cierra la unidad y entrega el proyecto automatizado |

La 5 y la 6 son las que más falta hacen: son el escalón que se traga las horas de
taller de verdad.

---

## Verificación

`generadores/c7_verifica.py` abre la página en un Chromium de verdad y da
**245 comprobaciones con 0 fallos**. Lo que comprueba, por si sirve de mapa:

- Que no hay ni un error de JavaScript ni de consola, al principio y al final.
- **S1**: seis combinaciones de cerebro × muebles × semilla, comparando casillas
  libres, casillas limpiadas, porcentaje, choques y pasos **con la simulación
  rehecha en Python**. Que el grabado pierde más de 25 puntos al mover los
  muebles. Que el grabado lee 0 sensores y el de sensor los lee 900 veces. Que el
  teledirigido no se mueve sin órdenes y cuenta las que le das.
- **S2**: trece combinaciones de motor, distancia, diámetro, pila, velocidad,
  suelo y semilla, comparando **las cinco llegadas una a una**, la media, la
  dispersión y el sesgo. Que la pila hunde al de tiempo y no toca a los otros dos.
  Que con la rueda mal medida el paso a paso sigue siendo preciso. Que a 400 mm/s
  el paso a paso pierde pasos y el del encoder no. Que el diámetro **no** cambia
  nada en el motor de tiempo, que es lo que dice la tabla.
- **S3**: seis juegos de ángulos y longitudes, comparando codo, punta, distancia
  al hombro y los dos radios del espacio de trabajo. El error angular para tres
  configuraciones. Y el problema inverso: que salen dos soluciones, que son el
  mismo ángulo cambiado de signo, y que **metiendo cada una en la cinemática
  directa la punta cae en el objetivo**. Más los dos casos sin solución.
- **S4**: una secuencia de 36 eventos escogida para pasar por **las veinte
  casillas**, comparando el estado después de cada uno con una máquina reescrita
  en Python. Que la transición de seguridad existe. Que en modo espagueti se
  pierden los eventos y baja con alguien debajo. Que las tres pieles recorren las
  mismas casillas.
- El test (10 de 10, explicaciones, borrar y repetir), los bloques PARA LA
  LIBRETA y SOLO PARA ENTENDERLO de cada sesión, una foto y un vídeo por sesión
  con su crédito y cargando a más de 900 px, el enlace a la lectura, que no hay
  ids repetidos, que ningún control se llama `ses-algo` y que **no hay ni una
  clase CSS que empiece por `test-`**.

Además, `c7_mirada.py` comprueba a ojo la maqueta a 900 px y a 390 px. La tabla
de transiciones de la S4 se salía por la derecha en móvil y ahora se desliza
dentro de su caja: a 360, 390 y 768 px **no hay ni un elemento que se salga**.
