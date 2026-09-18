# Tema 10 de 2.º · Programación y robótica · sesiones 4, 5 y 6

Rama `tema10b`. Todo generado, verificado en un Chromium de verdad y mirado con
los ojos. Lo que sigue es lo que he hecho, lo que he decidido por mi cuenta y lo
que conviene que mires tú antes de publicarlo.

---

## 1. Qué hay

| Fichero | Qué es |
|---|---|
| `2eso/TyD/tema10/index.html` | La página, 187 KB, **6 de 6 sesiones escritas** |
| `generadores/u10_s4.py` | S4 · Sensores y entradas |
| `generadores/u10_s5.py` | S5 · El robot |
| `generadores/u10_s6.py` | S6 · Proyecto, rúbrica y test |
| `generadores/u10_escenas2.py` | Las tres escenas nuevas (SENSORES, ROBOT, DIA) |
| `generadores/u10_comprueba.py` | El mismo cálculo repetido en Python: el patrón contra el que se mide |
| `generadores/u10_verifica.py` | 77 comprobaciones en un navegador de verdad |
| `generadores/u10_build.py` | Tocado: importa S4, S5 y S6 y sustituye las tres `pendiente=True` |
| `img/u10-farola-celula.jpg` | Foto de Commons (recortada por mí) |
| `img/u10-tortuga-walter.jpg` | Foto de Commons |
| `2eso/TyD/index.html` | Tocado: la tarjeta del tema 10 decía «2 de 6» y ahora dice «6 de 6» |

Reproducir todo:

```
~/venv/bin/python generadores/u10_build.py
~/venv/bin/python generadores/u10_comprueba.py    # imprime la tabla del patrón
~/venv/bin/python generadores/u10_verifica.py     # sale 0 si todo va bien
```

**`generadores/u10_verifica.py` da TODO CORRECTO: 77 comprobaciones, 0 fallos.**

No había `BRIEF.md`, así que el estándar lo he sacado de S1-S3 (`u10_build.py`,
`u10_robot.py`, `u10_s3.py`) y de `CURRICULO.md`.

---

## 2. Numeración: esto es el tema 10 de la web y la U12 del libro

`CURRICULO.md` avisa de que los números no coinciden. Siguiendo su tabla (la web
junta U3+U4+U5 en el tema 3, así que a partir de ahí va una menos y luego dos),
el tema 10 de la web es la **U12, Programación y robótica**, con los criterios
**5.1, 5.2 y 5.3** y los saberes del bloque C. Coincide con lo que ya traían
S1-S3 y con el encargo.

**En el texto no aparece ningún número de tema**, como en la U7, la U8 y la U9:
digo «la unidad del ordenador», «la unidad de electricidad». Las sesiones sí se
citan por número, pero eso ya lo hacían S2 y S3. Si algún día se renumeran los
temas, no hay que reescribir nada.

---

## 3. El hilo de las tres sesiones

Cada una arranca con una solución ingenua que el alumno escribe solo, la ve
fallar y entonces aparece el concepto:

| | El problema | La solución ingenua | Por qué no vale | El concepto |
|---|---|---|---|---|
| S4 | Que la farola se encienda de noche | Por reloj, «a las 20:00» | El reloj no mira por la ventana | **Sensor**, **condicional**, **umbral** |
| S5 | Que el robot vaya a la lámpara | «Si hay luz, avanza» | Un número no tiene dirección | **Dos entradas**, **lazo cerrado**, **condición de parada** |
| S6 | Que tu montaje sirva de algo | «Funciona, ya está» | Funcionar no es ser mejor que no hacer nada | **Medir el servicio**, no solo el ahorro |

Y se encadenan: S4 acaba diciendo que la farola decide pero **no cambia lo que
va a medir**; S5 empieza justo ahí y ese es el paso de automatismo a robot. S5
acaba con las piezas del curso entero sobre la mesa; S6 las recoge para el
proyecto y cierra el curso.

Dentro de S4 hay además un fallo buscado que no estaba en el encargo y que
creo que merece la pena: **la farola parpadea**. El programa es correcto y aun
así el aparato no sirve, porque ningún sensor da un número limpio. Se arregla con
dos umbrales (histéresis). Está en «solo para entenderlo», con su casilla en la
escena y su contador de parpadeos medido, y se recoge en la práctica y en el test.

---

## 4. Las tres escenas: qué calculan exactamente

Ninguna es una animación grabada, y hay un patrón en Python
(`u10_comprueba.py`) que repite la misma cuenta; `u10_verifica.py` compara los
números de la pantalla con los del patrón, uno a uno.

**S4 · El banco de sensores.** Ejecuta el bucle `para siempre` **diez veces por
segundo**, con su condicional dentro, y pinta en verde la rama que se está
ejecutando en ese instante. La línea de evaluación (`¿37 < 50? → SÍ`) sale de la
comparación real. Tres programas: farola (un umbral), invernadero (`si no, si`
con dos umbrales y el orden importando) y ruido (donde el número **no** se
compara, se convierte: `redondear(nivel × 5 ÷ 255)` columnas). El contador de
parpadeos cuenta los **cambios reales de estado** de los últimos 6 s, sobre una
lectura a la que se le suma ruido aleatorio de ±12.

**S5 · El robot.** Simulación de un robot de **tracción diferencial**, integrada
paso a paso cada 50 ms:

- mesa de 120 × 75 cm a 3,6 px/cm; chasis 12 × 14 cm; ruedas separadas los 10 cm
  del eje; sensores 6 cm por delante y 4 cm a cada lado, mirando 30° hacia fuera.
  **El dibujo está a esa escala**, no aproximado.
- luz de cada sensor = `255 · cos α · (20 cm / r)²`, acotada a 255 con un suelo de
  6 cm. Es la ley del inverso del cuadrado con el coseno del ángulo, que es lo
  que hace la aleta de cartón: dar direccionalidad.
- cinemática: `v = (vi+vd)/2·VMAX`, `ω = (vi−vd)·VMAX/EJE`, e integración de
  `θ`, `x`, `y`.
- los segundos, los centímetros recorridos y la distancia a la que se para salen
  de esa simulación. Con la lámpara y la salida de fábrica: regla 1 se cae de la
  mesa a los 3,8 s sin acercarse a menos de 60 cm; regla 2 pasa a 1 cm de la
  lámpara y sigue de largo; regla 3 se para a 25 cm en 4,9 s y 65 cm de recorrido.

La lámpara se mueve pulsando en la mesa y la salida se gira de 30 en 30, así que
los tres resultados no son un guion: cambian con lo que haga el alumno.

**S6 · El día entero.** Recorre los **1.440 minutos** del día, calcula la luz de
cada minuto y ejecuta encima las tres estrategias. Horas, Wh, € al año y minutos
a oscuras son sumas sobre ese recorrido; la potencia y el precio del kWh los pone
el alumno. Con los valores de fábrica (umbral 60, 9 W, 0,15 €/kWh):

| | Horas | Wh/día | €/año | A oscuras |
|---|---|---|---|---|
| Siempre encendida | 24,0 | 216 | 11,83 | nunca |
| Por reloj | 11,0 | 99 | 5,42 | **98 min** |
| Por sensor | 13,2 | 119 | 6,51 | nunca |

Y con el día de tormenta el reloj se va a **343 min** a oscuras. Ahí está el
argumento de S4, con la cuenta hecha: el reloj es el que menos gasta *y* el peor.

---

## 5. Lo que he decidido yo, y por qué (mira esto)

**a) El montaje de S5 no lleva ruedas obligatoriamente, y eso es a propósito.**
Con pinzas de cocodrilo solo hay **tres** pines de señal (P0, P1, P2, que son los
anillos grandes). Dos motores y dos sensores son cuatro cosas y **no caben**. En
vez de esconderlo, lo he puesto como contenido: es un problema de diseño real, de
los que obligan a elegir. Hay tres montajes:

- **A · el cerebro, sin motores** (< 1 € por grupo): cartón, dos LDR con sus
  10 kΩ en P0 y P1, y la placa muestra la flecha de lo que haría. Prueba el
  algoritmo completo; lo único que falta son las ruedas.
- **B1**: servos en P0 y P1 y **un solo** sensor, el de luz integrado, con el
  truco de Grey Walter (avanzar girando y comparar con la medida anterior).
- **B2**: dos LDR en P0/P1 y los servos en **P8 y P16**, que son los dos pines
  libres. Requiere placa de conexiones de borde.

**Esto es lo que más me gustaría que revisaras**: si en tu aula hay servos y
placas de conexiones, a lo mejor prefieres que B2 sea el montaje principal y A el
de repuesto. Cambiar el orden es tocar solo la ficha de la actividad 5.

**b) Aviso eléctrico que he puesto como no negociable.** Los servos **no** se
alimentan de la placa: el conector de borde da **190 mA** como mucho (dato de
`tech.microbit.org`) y dos micro-servos piden bastante más. Portapilas aparte y
GND común. Y los servos van montados en espejo, así que para ir recto se les
manda 0 y 180, no el mismo número.

**c) Los chips de saberes C.3 y C.4 son una conjetura.** `CURRICULO.md` no trae
transcritos los enunciados de C.1 a C.4 (solo dice que existen y a qué criterios
acompañan). He repartido: S4 → C.2 · C.3; S5 → C.3 · C.4; S6 → C.3 · C.4, por
plausibilidad. **Si tienes la diapositiva con los enunciados, conviene
contrastarlo**; es un cambio de una línea por sesión en `u10_build.py`.

**d) El minutado de S6 no es el de las demás.** 15' proyecto + 15' escena +
20' test + 10' cierre, en vez de 10/25/20/5. El cierre lleva 10 porque además de
cerrar el tema cierra el curso, y eso da para una conversación.

**e) La histéresis (S4) es contenido añadido por mí**, no estaba en el encargo.
Va en «solo para entenderlo» y en la práctica, no en definición de libreta, para
que no infle el temario. Si te parece que sobra en 2.º, se quita el `<h3>` «El
fallo que tiene tu farola» y la casilla de la escena sigue funcionando.

---

## 6. Vídeos e imágenes: qué he comprobado y qué no

**Vídeos.** Título y canal comprobados con la API oEmbed
(`generadores/oembed.py`). **Nadie los ha visto enteros**: sé quién los firma y
cómo se llaman, no si son buenos ni qué dicen minuto a minuto.

| Sesión | ID | Título | Canal |
|---|---|---|---|
| S4 | `2xwc5lwDzJg` | Sensor de luz solar con micro:bit \| Programación en MAKECODE | CienciaTec |
| S5 | `wQE82derooc` | Mechanical Tortoise (1951) | British Pathé |

- El de S5 es **archivo de British Pathé**, canal fiable, y está en inglés: lo
  digo en el pie, porque lo que hay que mirar se ve y no se cuenta.
- El de S4 es de un **canal pequeño** (`@profe.steaman`). Está en español y va
  justo de lo que hace la actividad, pero es el que menos aval tiene de los dos.
  **Míralo antes de publicar.** Si no te convence, hay una alternativa buena en
  inglés y de fuente oficial: `TKhCr-dQMBY`, «Behind the MakeCode Hardware ·
  Light Sensor on micro:bit», del canal **Microsoft MakeCode**, que explica
  precisamente que la micro:bit mide la luz con sus propios LED.
- **S6 no lleva vídeo, a propósito.** Es proyecto + test: los 60 minutos están
  repartidos y un vídeo se comería el tiempo de la demostración. Si lo quieres,
  dímelo y busco uno.

**Imágenes.** Licencia comprobada por la API de Commons (`wikimedia.py`) y las
dos **abiertas y miradas** una a una:

| Fichero | Autor | Licencia | Comentario |
|---|---|---|---|
| `u10-farola-celula.jpg` | Bidgee | CC BY 3.0 | **La he recortado** (la célula es un bulto azul diminuto y en el original no se veía). El recorte está declarado en el pie, como exige la licencia. |
| `u10-tortuga-walter.jpg` | Anders Sandberg | CC BY 2.0 | Es una **réplica**, no la tortuga original, y así lo digo. La foto está tomada en la mesa de un taller y se ve el desorden de detrás; me pareció preferible a no tener imagen, porque el mástil de la fotocélula se distingue bien. |

Además **reutilizo** `img/u7-ldr.jpg` (Suyash Dwivedi, CC BY-SA 4.0), la misma
LDR de la unidad del ordenador, y lo digo en el texto: es un guiño deliberado.

---

## 7. Datos técnicos: de dónde sale cada cifra

Ninguna va de memoria. Las que aparecen en el texto:

| Dato | Fuente |
|---|---|
| Nivel de luz de 0 a 255 | `makecode.microbit.org/reference/input/light-level` |
| Nivel de sonido de 0 a 255, solo v2 | `makecode.microbit.org/reference/input/sound-level` |
| `leer pin analógico` de 0 a 1023 | `makecode.microbit.org/reference/pins/analog-read-pin` |
| La luz se mide **con los propios LED** | `tech.microbit.org/hardware/`: «repeatedly switching some of the LED drive pins into inputs and sampling the voltage decay time» |
| El termómetro mide el **chip**, ±5 °C sin calibrar | `tech.microbit.org/hardware/`: «on-board core temperature sensor… provides an estimate of ambient temperature» |
| 190 mA por el conector de borde | `tech.microbit.org/hardware/` |
| P0, P1, P2 anillos grandes; P8 y P16 libres; P3-P10 compartidos con la pantalla | `microbit.pinout.xyz` |
| Tortugas de Grey Walter, Bristol, 1948-49; una sola fotocélula; dos motores; caseta de recarga; **la fotocélula iba en la dirección y barría el cuarto** | Wikipedia (*Elmer and Elsie*, *William Grey Walter*) + IEEE Spectrum, «Meet the Roomba's Ancestor: The Cybernetic Tortoise»: «The photocell was attached to the steering mechanism, and as the tortoise searched, it moved forward in a circular pattern» |
| Festival of Britain, 1951 | IEEE Spectrum, mismo artículo |

**Una cosa que quité por no poder confirmarla**: había escrito que la decisión de
las tortugas la tomaban **dos válvulas de vacío**. Es lo que se repite por todas
partes, pero no lo he encontrado en ninguna de las fuentes que he podido
comprobar, así que lo he dejado en «un circuito electrónico con dos caminos, uno
para cada motor, que funcionaban como dos neuronas», que sí está en Wikipedia.
Si tienes una fuente buena, la frase queda mejor con las válvulas.

---

## 8. Lo que un humano debería mirar antes de publicar

1. **El vídeo de S4** (canal pequeño, sin ver). Alternativa oficial propuesta en
   el apartado 6.
2. **Qué montaje de S5 es el principal** en tu aula: depende de si hay servos y
   placas de conexiones. Ver apartado 5a.
3. **Los saberes C.3 y C.4** de los chips: conjetura mía, ver apartado 5c.
4. **Si la histéresis sobra en 2.º.** Yo creo que no, porque el alumno la ve
   pasar y la mide, pero es criterio tuyo.
5. **La foto de la tortuga**: es una réplica en una mesa desordenada. Si prefieres
   sin foto, el texto se sostiene igual.
6. **El modelo del "día de tormenta"** de la escena de S6 es sintético: una curva
   de seno por un factor de nubes hecho con dos senos. Da un día en el que a
   mediodía se queda por debajo de 40 (una tormenta seria) y por eso el reloj
   falla tanto. Es plausible y sirve para lo que tiene que servir, pero **no son
   datos meteorológicos reales**. Si prefieres que sea menos extremo, se toca el
   `0.05 + 0.95·n²` de `luzMin()` en `u10_escenas2.py` y el mismo en
   `u10_comprueba.py` (están duplicados a propósito, para que el verificador
   tenga con qué comparar).
7. **Amanecer y ocaso** de esa escena están puestos a las 8:00 y las 20:40, que es
   aproximadamente un día de finales de septiembre en Andalucía. No lo he
   calculado con efemérides: es un valor razonable, no un dato.
8. **La lectura del tema** (30 párrafos + 10 preguntas en PDF) que piden los
   criterios de producción de `CURRICULO.md` **no está**: el encargo pedía las
   sesiones 4, 5 y 6 y no la lectura, y las unidades 6 a 9 sí la tienen. Queda
   pendiente.

---

## 9. Cosas que no me cuadraron y no me he inventado

- **El índice de 2.º tenía dos tarjetas desfasadas, y no por descuido: hubo una
  reversión.** `generadores/ordena_indice.py` tiene rutas de Windows
  (`C:\Users\javie\…`) y no se puede ejecutar aquí, así que la tarjeta del tema 10
  la he editado **a mano**: ahora dice «6 de 6» y la barra al 100 %.

  Al mirar por qué decía «2 de 6» encontré esto: el commit `688f748` (la S3) sí
  actualizó la tarjeta a «3 de 6», y el commit siguiente que tocó el índice,
  `255a923` («Recupero el pie del índice…»), la **devolvió a «2 de 6»**. Ese
  commit reconstruyó el fichero a partir de un `indice_bueno.html` anterior, y de
  paso se llevó por delante otra tarjeta:

  > **La del tema 5 dice «3 de 6» y el tema 5 tiene las seis sesiones escritas.**
  > Lo he contado en `2eso/TyD/tema5/index.html`: seis botones de sesión, ninguno
  > deshabilitado. Antes de `255a923` decía «6 de 6» y la barra al 100 %.

  **No la he tocado porque no es de mi encargo**, pero es un cambio de una línea
  en `2eso/TyD/index.html` y te lo dejo localizado. Las demás las he contado y
  están bien: tema 1 «2 de 6» ✓, tema 9 «3 de 6» ✓.
- El narrador de voz (`avatar_flat`) solo aparece en la S1, que es donde lo puso
  el generador. No he añadido voz nueva: no hay guion ni mp3 para las sesiones
  4-6 y no me parecía cosa de inventarlo.
- No hay `BRIEF.md` en el repositorio, ni en la rama ni en `main`.
- **`.git/config` no tenía sección `[user]`**, así que `git commit` se negaba a
  hacer nada («Committer identity unknown») aunque todos los commits anteriores
  están firmados como `rgllorente82-png`. Le he añadido esa sección con esa misma
  identidad, que es la del resto del historial. Es un ajuste local del
  repositorio, no viaja en el commit, y se quita con
  `git config --unset-all user.name` y lo mismo con `user.email`.
