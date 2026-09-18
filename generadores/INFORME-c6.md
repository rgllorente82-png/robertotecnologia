# Informe · 4.º de ESO · Tema 6 · Programación, IoT e inteligencia artificial

Rama `c6`. Entregadas las **cuatro primeras sesiones** de ocho; las otras cuatro
quedan en la barra con su título y el botón desactivado.

---

## Qué hay entregado

| Fichero | Qué es |
|---|---|
| `4eso/Tecnologia/tema6/index.html` | La unidad. 188 KB, generada. |
| `4eso/Tecnologia/tema6/lectura-tema6.pdf` | Lectura de aula: 30 párrafos numerados + 10 preguntas, 5 páginas A4. |
| `generadores/c6_build.py` | El generador de la página. |
| `generadores/c6_escenas.py` | Escenas de las sesiones 1 y 2. |
| `generadores/c6_escenas2.py` | Escenas de las sesiones 3 y 4. |
| `generadores/c6_lectura.py` | El PDF de la lectura. |
| `generadores/c6_verifica.py` | Verificador: **116 comprobaciones, 0 fallos**. |
| `generadores/c6_fotos.py` | Consulta la licencia en Commons y baja las cuatro fotos. |
| `generadores/c6_capturas.py` | Recorta cada escena a PNG, para mirarlas. |
| `generadores/c6_mirada.py` | Captura la página entera de cada sesión. |
| `generadores/guion_c6.txt` | Guion de la voz. |
| `audio/c6-programacion.mp3` + `_env_c6-programacion.json` | Voz (1 min 51 s) y su envolvente. |
| `img/c6-*.{jpg,png}` | Las cuatro fotos de Commons. |

**No he tocado `4eso/Tecnologia/index.html`.** De hecho no existe todavía: en
`4eso/Tecnologia/` solo estaba `tema0/`.

---

## Cómo se ejecuta

```
~/venv/bin/python generadores/c6_build.py        # la página
~/venv/bin/python generadores/c6_lectura.py      # el PDF
~/venv/bin/python generadores/c6_verifica.py     # 116 comprobaciones
~/venv/bin/python generadores/c6_capturas.py     # PNG de cada escena en /tmp/c6/
```

---

## Decisiones, y por qué

### 1. Tuve que recuperar `generadores/voz.py`

**No estaba en esta rama.** Existe en `tema7`/`tema8` (commits `83ebf20` y
`106266b`), pero ninguno de los dos es antepasado de `c6`, así que aquí no había
fichero. Lo he vuelto a poner tal cual estaba en `83ebf20`, sin cambiarle nada.

**Para mirar:** o esas ramas se mezclan en `main`, o hay que decidir dónde vive
la herramienta. Ahora mismo hay dos copias idénticas en dos ramas distintas y
ninguna en `main`.

### 2. El orden de las cuatro sesiones: casi el propuesto, con un cambio de foco

Mantengo las cuatro y el orden. Lo que sí he cambiado es **dónde está el peso de
la sesión 1**. La propuesta decía «el salto de 2.º: bloques y C++ al lado». Eso,
solo, es una sesión de sintaxis y se les cae encima. Lo he montado así:

- El gancho es **mandarle el programa a otro grupo**: una captura de pantalla no
  se ejecuta, no se busca, no se compara y no se le pega el ejemplo de la hoja de
  características del sensor. Ese es un problema real y de 15 años.
- Pero el **cuerpo** de la sesión es el tipo, y se enseña **fallando**: con `int`
  y paso 0,5 el contador se queda en 0 para siempre; con `int` y paso 1000 se
  desborda a las 33 vueltas y da un número negativo. Las dos cosas pasan **sin
  avisar**, y esa es la frase que quiero que se lleven: un programa que se para
  se arregla, uno que miente hay que pillarlo.

El resto va como se propuso.

### 3. Las cuatro sesiones pendientes: he puesto títulos

Aparecen desactivadas en la barra pero **con título**, para que se vea la forma
entera de la unidad. Mi propuesta, encadenada con lo escrito y sin pisar la U7
(robótica, criterio 4.1):

| S | Título corto | Qué resuelve | Qué deja abierto |
|---|---|---|---|
| 5 | Decidir con memoria | El umbral solo no basta: si la lectura tiembla en el umbral, la bomba parpadea. Histéresis y estados. | Ya decide bien, pero sigo montándolo a trozos |
| 6 | Montar el aviso de verdad | El envío punta a punta, en Tinkercad y con un módulo de wifi. Qué cuesta de verdad. | Tengo datos míos, muchos |
| 7 | Entrenar con vuestros datos | Recoger ejemplos del propio proyecto, etiquetarlos y medir los tres números. | ¿Y quién decide qué, en todo esto? |
| 8 | El sistema completo | Qué decide la placa, qué el servidor y qué el modelo. Memoria del proyecto y test de la unidad. | — |

El cierre de la S4 ya engancha con la S5 (el umbral que tiembla).

### 4. El test: está en la sesión 4, no en la 8

El encargo pide «el test de la última sesión». La última sesión de la unidad es
la 8 y está pendiente, así que he puesto **un test de 10 preguntas al final de la
S4**, titulado «Lo que tiene que haber quedado de **estas cuatro sesiones**».
Cuando se escriban las cuatro que faltan, lo suyo es dejar este donde está (cierra
el primer bloque) y añadir otro al final de la S8 con toda la unidad. **Esto lo
decides tú.**

### 5. El proyecto del curso: no me he casado con ninguno

Cada vez que hace falta un caso concreto salen **dos o tres** de los cinco de
`PROYECTOS.md`, nunca uno solo:

- **S1**, elegir el tipo: riego (1), contenedor (3) y ventilación (2).
- **S2**, calcular el escalón: ventilación (2, TMP36), lámpara (5, LDR) y riego (1).
- **S3**, diseñar el mensaje: riego (1) y ventilación (2), y la escena trae las
  tres magnitudes (humedad, temperatura, distancia) para que valga también el
  contenedor (3).
- **S4**, el clasificador: riego (1) y ventilación (2) son los dos conjuntos de
  datos; el reto inicial usa el contenedor (3) y el riego (1).

**Donde sí he tenido que elegir, y hay que saberlo:**

- La escena del conversor lleva **tres sensores concretos** con su modelo físico:
  sonda de humedad, LDR y TMP36. El proyecto 4 (barrera con servo) se queda sin
  sensor propio en esa escena, porque un pulsador es digital y no tiene escalón
  que enseñar. Si el proyecto del curso acaba siendo la barrera, hay que añadir
  el **ultrasonidos** a la escena; es media hora.
- **Los ejemplos hablan de micro:bit solo para decir que este curso es Arduino.**
  Ojo, que `PROYECTOS.md` todavía describe los cinco candidatos con micro:bit en
  el coste («con micro:bit reutilizable del centro»), aunque el punto 1 del final
  ya dice que en 4.º es Arduino. Conviene actualizar ese párrafo del catálogo.

### 6. Un Arduino Uno no se conecta a la red, y lo digo en la página

La sesión 3 va de IoT y la placa de 4.º es un Uno, que **no tiene wifi ni
Ethernet**. Lo he dicho explícitamente en un bloque de «solo para entenderlo»:
hace falta un ESP8266, una ESP32 en su lugar o una tarjeta de Ethernet, y eso
cambia el presupuesto. **Para mirar:** si el proyecto va a llevar aviso remoto de
verdad, esa compra hay que preverla, y a lo mejor conviene que la placa del curso
sea directamente una **ESP32** (que además es de 32 bits, con lo que el ejemplo
del desbordamiento de la S1 habría que reescribirlo).

---

## Las escenas: qué calculan exactamente

Ninguna enseña un número que no salga de una cuenta. El verificador rehace cada
cuenta **en Python y a partir de la definición**, no copiando el JavaScript, y las
compara.

**S1 · «El mismo programa, en los dos idiomas».** Ejecuta el programa instrucción
a instrucción en las dos representaciones a la vez (bloque iluminado ↔ línea
iluminada) y con la aritmética del tipo elegido:
- `int` = 16 bits con signo: trunca hacia cero y **da la vuelta** de verdad
  (40 × 1000 = 40.000 → **−25.536**, comprobado contra el patrón de Python).
- `long` = 32 bits. `float` = 4 bytes, con `Math.fround()` para que la precisión
  sea la de un float de verdad y no la de un double de JavaScript.
- El monitor serie imprime **como imprime Arduino**: los `float`, con dos
  decimales.
- La barra de memoria: 2 bytes de 2.048, y caben 1.024 variables como esa.

**S2 · «El escalón del conversor».** La tensión del pin sale de un modelo físico
**declarado dentro de la escena**:
- Humedad: modelo lineal de una sonda resistiva (rotulado como modelo, no como
  hoja de características).
- Luz: divisor de tensión con una LDR, `R = 10 kΩ · (E/10)^−0,7` y 10 kΩ fijos.
- Temperatura: **TMP36 de su hoja de características**, 0,5 V + 10 mV/°C.

El número sale de `floor(V/Vref · 2^bits)`, la escalera se dibuja escalón a
escalón, y la franja de tensiones que dan ese mismo número se dibuja **y se
escribe**. Se pueden cambiar los bits (8/10/12) y la referencia (5 / 3,3 / 1,1 V):
el escalón cambia, y con 1,1 V el sensor se **sale de escala** y la escena lo dice.
Los decimales que el escalón no sostiene salen **tachados en rojo**.

**S3 · «El mensaje, byte a byte».** Construye la cadena de verdad en los tres
formatos y la cuenta carácter a carácter:
- texto plano: `aula12;hum;38;2026-09-18T10:05:00Z\n` = **35 B**;
- MQTT `PUBLISH`: 4 B de cabecera binaria + tema + carga = **41 B**;
- HTTP + JSON: petición entera con sus `\r\n` = **194 B**, de los que solo el
  33 % es dato.

De ahí salen los mensajes al día, los bytes al mes y las filas guardadas en un
curso. `+40 B` de TCP/IP (20 de IPv4 + 20 de TCP) y `+22 B` de TLS (5 de cabecera
de registro + 1 de tipo + 16 de sello) son opcionales y están desglosados en el
pie. **He dicho explícitamente que los 22 B no incluyen el saludo inicial**, que
es mucho más largo, y no he puesto una cifra para el saludo porque depende de la
configuración y no la he podido verificar.

**S4 · «Entrénalo tú».** Un perceptrón de verdad: pesos `w₁`, `w₂`, `b`, paso de
aprendizaje 0,08, tope de 200 pasadas, regla de actualización clásica. El alumno
pone los ejemplos pinchando. Se miden **tres** cosas juntas, que casi nunca se
enseñan juntas:

| Conjunto | acierta en los suyos | en los 24 de prueba | modelo tonto |
|---|---|---|---|
| Repartidos | 100 % | 100 % | 65 % |
| **Sesgados** (todos en la franja de abajo) | **100 %** | **75 %** | 65 % |
| El caso de 1969 (XOR, cuatro grupos) | 60 % | 63 % | 50 % |

Los 24 datos de prueba se dibujan como cuadrados huecos y **los que falla salen
tachados**: con los sesgados se ve dónde falla, que es lo que se quiere enseñar.
El XOR no converge nunca y la escena lo explica con Minsky y Papert.

---

## Un fallo que encontré y arreglé, y que conviene saber

**Un `id` que empiece por `ses-` desaparece al navegar.** El JavaScript de
`unidad_base.NAV_JS` hace `document.querySelectorAll('[id^="ses-"]')` y oculta
todo lo que no sea el panel de la sesión activa. Yo le había puesto `id="ses-c4"`
a un botón de la escena 4, y al cambiar de sesión **el botón se escondía**.

Está arreglado (ahora es `c4-sesgados`) y el verificador lo comprueba: no puede
haber ningún elemento con `id` que empiece por `ses-` salvo los paneles
`ses-1`…`ses-8`. **Esto le puede pasar a cualquier unidad**: merece la pena
copiar esa comprobación a los otros verificadores.

El segundo fallo era mío y solo visual: el sombreado de las dos regiones del
plano de la S4 se pintaba mal cuando la recta se iba fuera del cuadro (`w₂` casi
cero), y salían tres franjas de color en vez de dos. Arreglado, y con
comprobación propia: recorriendo el cuadro por la mitad solo puede haber **un**
cambio de color.

---

## Las fotos

Las cuatro son de Wikimedia Commons, con la licencia consultada por la API
(`generadores/c6_fotos.py`) **y la imagen abierta y mirada una a una**.

| Sesión | Fichero | Autor | Licencia | Tamaño |
|---|---|---|---|---|
| 1 | `c6-arduino-uno.jpg` | Suyash Dwivedi | CC BY-SA 4.0 | 3195×2130 → 1280 |
| 2 | `c6-potenciometro.jpg` | Iainf | CC BY 2.5 | 888×1040 |
| 3 | `c6-cafetera-trojan.png` | Quentin Stafford-Fraser | CC BY-SA 3.0 | **142×159** |
| 4 | `c6-perceptron.jpg` | National Museum of the U.S. Navy | dominio público | 2836×2220 → 1280 |

**Dos cosas que hay que mirar:**

1. **La cafetera de Cambridge mide 142×159 píxeles y no hay nada más grande.** Es
   la imagen original de 1991, así de pequeña. La he puesto a 284 px de ancho con
   `image-rendering: pixelated` y lo digo en el pie («esto es la imagen entera,
   ampliada aquí para que se vea»). Me parece que el tamaño **es** parte de la
   historia, pero si no te convence hay que buscar otra foto para la S3.
2. **En la foto del perceptrón no digo quién es el hombre.** La descripción de
   Commons dice que la máquina es el Mark I Perceptron y que el programa lo
   dirigía Rosenblatt, pero **no identifica a la persona de la foto**, así que en
   el pie describo lo que se ve y no pongo nombre.

## Los vídeos

Título y canal comprobados por oEmbed el 18-sep-2026. **Nadie los ha visto
enteros**: solo está verificado que el vídeo existe, que se llama como digo y que
es del canal que digo. Antes de ponerlos en clase, míralos.

| Sesión | ID | Título | Canal |
|---|---|---|---|
| 1 | `7uV4Jh30Oho` | Las funciones setup y loop · Curso de Arduino: De Cero a Maker | Héctor Pérez |
| 2 | `ddOaXUWQxbI` | Potenciometro con ARDUINO y TINKERCAD · Leer Entradas Analógicas | Novatech |
| 3 | `RpjSwriOi9U` | Qué es MQTT? | Easy Learning |
| 4 | `fP_f-aNZFLo` | Capítulo 5: Sesgos algorítmicos en la Inteligencia Artificial | FUNDACIÓN VTR |

El de la S4 es de una fundación chilena; el vocabulario es de allí. Si suena raro
en clase, se cambia sin tocar nada más que el `id`.

---

## Datos técnicos, y de dónde sale cada uno

Todo lo que afirma la unidad sobre la placa está comprobado contra la hoja de
características del ATmega328P o contra la documentación de Arduino:

- **2.048 bytes de SRAM** en el Uno; `int` = 2 B, `long` = 4 B, `float` = 4 B, y
  **`double` es igual que `float`** en AVR (4 B, no 8).
- Umbrales de una entrada digital a 5 V: **1 por encima de ~3,0 V** (0,6·Vcc),
  **0 por debajo de ~1,5 V** (0,3·Vcc).
- Un `analogRead()` tarda unos **100 µs** (preescalador 128 → 125 kHz; 13 ciclos
  de conversión → 104 µs).
- `map()` hace la división **con enteros y truncando**: `map(5,0,1023,0,100)` = 0.
- `Serial.println(float)` imprime **dos decimales** si no se le pide otra cosa.
- **1023 y 1024 los digo los dos**, y explico la diferencia en un «solo para
  entenderlo»: el escalón vale Vref/1024 y la cuenta de volver se hace entre 1023
  para que el número más alto valga exactamente Vref. Se diferencian en un 0,1 %.
- MQTT: **1999**, Andy Stanford-Clark (IBM) y Arlen Nipper (Arcom), para vigilar
  oleoductos por satélite. Un mensaje mínimo puede ser de **dos bytes**.
- Perceptrón: artículo de Rosenblatt en **1958**, máquina montada en 1959 en el
  Cornell Aeronautical Laboratory, **400 fotocélulas en 20×20**, pesos con
  **potenciómetros movidos por motores**. Minsky y Papert, **1969**, el XOR.
- Cafetera de Cambridge: **1991**, Quentin Stafford-Fraser y Paul Jardetzky,
  cliente **XCoffee**; a la web en **noviembre de 1993** (Daniel Gordon y Martyn
  Johnson); apagada el **22 de agosto de 2001**.

**Lo único que NO es un dato de hoja de características y va rotulado como tal
dentro de la propia escena:**

- El modelo de la sonda de humedad (`V = 5·(1−h/100)·0,94 + 0,12`) es **mío**, un
  modelo lineal para que la cuenta del conversor tenga con qué trabajar. El pie de
  la escena lo dice: «el sensor de verdad no es tan recto y además se oxida».
- El exponente **0,7** de la LDR: las LDR de sulfuro de cadmio corrientes andan
  entre 0,5 y 0,9. He elegido 0,7 y lo he llamado «el de una LDR corriente». Si te
  parece mucho afirmar, se puede rebajar a «entre 0,5 y 0,9; aquí usamos 0,7».
- La regla que separa de verdad los dos conjuntos de la S4 es inventada; está
  escrita en el pie de la escena, junto al aviso de que **el modelo no la conoce**.

---

## La lectura de aula

`lectura-tema6.pdf`, 5 páginas, **30 párrafos justos** (comprobado por el propio
script, que se niega a generar si no son 30) y 10 preguntas. Título: *Cuando el
aparato decide solo*.

Cuenta las tres ideas de la unidad por el lado de lo que ha costado aprenderlas,
con **tres casos reales con fecha y con factura**, y los tres verificados:

1. **Ariane 5, vuelo 501, 4 de junio de 1996.** Un número de 64 bits metido en una
   variable de 16. 37 segundos de vuelo, 370 millones de dólares. Es la sesión 1.
   Incluye el detalle que más enseña: los dos ordenadores redundantes fallaron
   igual, porque tenían el mismo programa.
2. **Mars Climate Orbiter, 23 de septiembre de 1999.** Libras-fuerza contra
   newtons, factor 4,45. Pasó a 57 km en vez de a 226. 327,6 millones. Es la
   sesión 2: un número no significa nada hasta que alguien dice de qué es.
3. **La herramienta de selección de Amazon, retirada y contada por Reuters en
   octubre de 2018.** Entrenada con diez años de currículos. Es la sesión 4.

Hay un detalle de maqueta menor: el titulillo «Lo que tienen en común» se queda al
final de la página 3 y sus párrafos van en la 4. `lectura.py` no agrupa el
titulillo con lo que le sigue. **No lo he tocado porque `lectura.py` es común a
todas las unidades**, y cambiarlo repagina las otras lecturas. Si quieres, se
arregla en un sitio y se regeneran todas.

---

## Qué debería mirar un humano

1. **El vídeo de la S4** (canal chileno) y, en general, los cuatro vídeos enteros.
2. **La foto de la cafetera a 142 px**: o cuela como está, o hay que buscar otra.
3. **Dónde va el test** (ahora en la S4, cubriendo solo lo escrito).
4. **`voz.py` no estaba en esta rama**: decidir dónde vive.
5. **Si la placa del curso va a llevar wifi**, porque un Uno no lo lleva, y si
   fuera una ESP32 habría que rehacer el ejemplo del desbordamiento de la S1.
6. **`PROYECTOS.md` sigue costeando los cinco proyectos con micro:bit** aunque ya
   esté decidido que en 4.º es Arduino.
7. Si el **exponente 0,7 de la LDR** te parece demasiado concreto para afirmarlo.

## Lo que no he hecho

- Las sesiones 5 a 8 (el encargo pedía las cuatro primeras).
- La tarjeta en `4eso/Tecnologia/index.html`, que la pones tú al recoger. Ese
  fichero **no existe todavía**: en esa carpeta solo hay `tema0/`.
