# Informe · Unidad 5 de 4.º de ESO · Electrónica y neumática

Rama `c5`. Cuatro sesiones escritas de ocho, con las otras cuatro marcadas como
pendientes y con título puesto. La página abre, las cuatro escenas calculan y el
verificador pasa **110 comprobaciones sin fallos**.

---

## Qué hay entregado

| Fichero | Qué es |
|---|---|
| `4eso/Tecnologia/tema5/index.html` | La unidad, 204 KB, generada |
| `4eso/Tecnologia/tema5/lectura-tema5.pdf` | Lectura de aula, 4 páginas, 30 párrafos numerados y 10 preguntas |
| `generadores/c5_build.py` | El texto de las cuatro sesiones y el montaje de la página |
| `generadores/c5_escenas.py` | Escenas de S1 (divisor) y S2 (transistor) |
| `generadores/c5_escenas2.py` | Escenas de S3 (cilindro) y S4 (circuito neumático) |
| `generadores/c5_comprueba.py` | Las mismas cuentas rehechas en Python, como patrón |
| `generadores/c5_verifica.py` | Verificador con Chromium: 110 comprobaciones |
| `generadores/c5_capturas.py` | Saca una foto de cada escena, para mirarlas |
| `generadores/c5_lectura.py` | La lectura |
| `generadores/c5_fotos.py` | Descarga de Commons con licencias, y `creditos_c5.json` |
| `generadores/guion_c5.txt` | Guion de la voz |
| `audio/c5-electronica.mp3` + `_env_c5-electronica.json` | Voz (2:14) y envolvente del avatar |
| `img/c5-ntc.jpg`, `c5-transistores.jpg`, `c5-cilindro.jpg`, `c5-valvulas.jpg` | Fotos de Commons |

`4eso/Tecnologia/index.html` **no se ha tocado**, como pedía el encargo.

Cómo se regenera todo:

```
/home/ubuntu/venv/bin/python generadores/c5_build.py
/home/ubuntu/venv/bin/python generadores/c5_lectura.py
/home/ubuntu/venv/bin/python generadores/c5_verifica.py     # 110 OK, 0 fallos
/home/ubuntu/venv/bin/python generadores/c5_capturas.py     # PNG en /tmp/c5-capturas
```

---

## La cadena de las cuatro sesiones

Mantuve las cuatro que proponía el encargo, en el mismo orden, porque la cadena
causal funciona: cada una nace del fracaso de la anterior.

| | Sesión | El problema con el que abre | Lo que deja abierto |
|---|---|---|---|
| S1 | El sensor y el divisor | Enchufas una LDR a `A0` y los números bailan | Ya tengo el número; mover algo no lo he tocado |
| S2 | El transistor | Enchufas la bomba al pin y se quema el pin | Ni con transistor saco 50 kg de empuje |
| S3 | Fuerza con aire | Un servo SG90 levanta 360 gramos | Sé qué cilindro, no sé cómo mandarlo |
| S4 | Mandar el aire | Cierras la llave de paso y el cilindro no vuelve | Faltan las cuatro piezas juntas → S5-S8 |

### Lo que cambié de la propuesta, y por qué

**1. El conversor A/D entra en S1, no queda suelto.** La propuesta terminaba S1
en «tensión que se puede leer». Pero el alumno no lee tensiones: lee un número
entero de 0 a 1023. Sin cerrar ese paso, la sesión deja el trabajo a medias y la
actividad (elegir un umbral) no se puede hacer. S1 va ahora entera de
**resistencia → tensión → número**, y la escena enseña los tres a la vez.

**2. El test va al final de S4, no de S8.** El encargo pide el test en la última
sesión, pero la última sesión está pendiente. Puse un test de 10 preguntas al
cierre de S4 cubriendo S1-S4, rotulado como «Comprueba lo de estas cuatro
sesiones». **Decisión a revisar cuando se escriban S5-S8**: o se mueve al final,
o se deja este como test de media unidad y se añade otro. Yo dejaría los dos.

**3. Añadí la válvula selectora de circuito a S4.** No estaba en la propuesta y
hacía falta: ver más abajo, en «Un error que encontré y corregí».

---

## Un error que encontré y corregí

Al mirar la captura del circuito de la **función O** vi que estaba mal, y era un
error técnico de verdad, no un fallo de dibujo.

Dos válvulas 3/2 NC en paralelo **no hacen la función O**. Cuando aprietas una,
la otra sigue conectando esa misma línea con su vía 3, y el aire se escapa a la
atmósfera antes de llegar a pilotar nada. Por eso existe la **válvula selectora
de circuito** (válvula O, antirretorno doble), que lleva una bolita que la
presión empuja contra la entrada sin aire, tapándola.

Está corregido en tres sitios: la escena la dibuja con su bolita moviéndose al
lado que toca, el pie lo explica, y hay un bloque **PARA LA LIBRETA** nuevo
titulado «La trampa de la función O».

La función Y (dos 3/2 en serie) sí es correcta con válvulas normales, y se
queda como estaba.

---

## El argumento del mando indirecto: la propuesta obvia no se sostiene

Empecé a montar S4 con la idea de que el mando indirecto es **más rápido**
(tubos de potencia cortos frente a tubos largos). Hice la cuenta y **no sale**.

Con un modelo de «llenar el volumen al caudal nominal de la válvula», un mando
directo con una 5/2 manual de 600 NL/min y 10 m de tubo de Ø4 tarda ~0,20 s,
mientras que el indirecto suma el llenado del tubo de mando por el pulsador
pequeño (~0,21 s) más el llenado del cilindro (~0,12 s) = ~0,33 s. El indirecto
sale **peor**. El argumento de la velocidad, tal como se cuenta a veces, no
aguanta la cuenta cuando la válvula manual también es de potencia.

Así que no lo escribí. Lo que la escena calcula es el argumento que **sí** es
correcto y además es el de los libros:

- El caudal que pide el cilindro sale de su volumen por los ciclos por minuto.
- Ese caudal exige un **diámetro de paso** en la válvula (regla de tanteo: un
  asiento de 2 mm pasa ~100 NL/min a 6 bar, y el caudal va con el área).
- Abrir ese paso contra 6 bar cuesta **F = p·A + muelle** en el dedo.
- Con mando directo esa fuerza **crece con el cilindro**; con indirecto el botón
  es siempre el mismo.

Con Ø32 a 20 ciclos salen 4,8 N (nada) y con Ø100 a 50 ciclos salen 24,1 N
(2,5 kg con un dedo, cientos de veces al día). **La escena arranca en el caso
en el que el mando directo todavía vale**, a propósito: el alumno tiene que
romperlo él subiendo el diámetro. En el texto, las otras razones (tubos, poder
combinar señales, seguridad) van como razones, no como cuentas.

---

## Las escenas: qué calcula cada una

Ninguna lleva dentro una tabla de resultados. Todo se recalcula al tocar un
control, y `c5_comprueba.py` rehace las mismas cuentas en Python —mirando la
física, no copiando el JavaScript— para que el verificador las compare.

**S1 · El divisor.** Modelo de LDR (ley de potencia de una GL5528: 10 kΩ a
10 lux, γ = 0,7) y de NTC (ecuación B de una 10 kΩ B3950; comprobada contra
tabla: 33,6 kΩ a 0 °C y 3,59 kΩ a 50 °C). Divisor resistivo, conversor de 10
bits. La curva se traza con 170 muestras calculadas una a una y se marca por
bisección el punto donde el sensor vale lo mismo que la resistencia fija. Se
puede cambiar sensor, resistencia fija (1/4,7/10/47 kΩ) y montaje (sensor
arriba o abajo). El pie dice cuántos escalones se mueve la cuenta si la luz se
duplica, y avisa cuando son menos de cinco: es la manera de ver de un vistazo
que una resistencia fija mal elegida deja el circuito ciego.

**S2 · El transistor.** Corriente de base, ganancia, margen de saturación, Vce,
potencia disipada, límite del pin (20 mA) y límite del transistor. Dos
transistores (BC547 y TIP120 Darlington, con su Vbe de 1,6 V) y cuatro cargas.
El pico inductivo se calcula con V = L·ΔI/Δt y se dibuja en escala logarítmica
contra la Vceo del transistor, con y sin diodo de rueda libre. El dibujo pinta
el camino colector-emisor en verde **solo** si el montaje es sano: si el
transistor no aguanta o el pin va sobrecargado, no puede decir que todo va bien.

**S3 · El cilindro.** F = p·A con los diámetros normalizados y los vástagos de
la ISO 15552. Fuerza de avance y de retroceso (el vástago tapa área), muelle del
simple efecto modelado como 0,5 bar equivalentes, consumo en litros normales, y
la caja que hay que arrastrar con μ = 0,4. **Si no hay fuerza, el vástago no se
mueve**: la animación hace caso a la cuenta, y el verificador lo comprueba
midiendo dónde está la caja en el dibujo antes y después.

**S4 · El circuito.** Símbolos ISO 1219 dibujados a mano: 5/2 y 3/2 con sus
cuadros, flechas de paso, vías tapadas con la T, muelles, pulsadores, pilotaje,
escapes, fuente de presión y selectora. **Las cajas se deslizan**, que es lo que
hace el distribuidor de verdad: no se mueven los tubos, se mueve el cuadro que
está en servicio. Las líneas con presión se calculan a partir del estado de las
válvulas; no están pintadas de antemano. Cuatro circuitos: directo, indirecto, Y
y O.

---

## Lo que miré con los ojos, no solo con un test

Un esquema mal dibujado enseña mal y eso no lo caza ningún test. Saqué 24
capturas con `c5_capturas.py` y las abrí una a una. De ahí salieron, entre
otras, estas correcciones:

- La **fuente de presión estaba dibujada sin conectar** en el circuito de mando
  directo: el tramo de raíl salía de longitud cero. Habría enseñado un circuito
  imposible.
- El **muelle del cilindro de simple efecto** salía como dos rayas planas. Ahora
  son dos zigzags dentro del hueco anular entre el vástago y la camisa, que es
  donde está el muelle de verdad en un corte.
- El **émbolo se quedaba a medio camino** en las dos escenas de cilindro: el
  recorrido del dibujo era más corto que el hueco disponible y parecía que el
  cilindro no llegaba al final.
- Rótulos pisándose en cinco sitios (las vías 5/1/3 de la 5/2, los nombres de
  los pulsadores, el nombre del transistor sobre la patilla C, la etiqueta
  «cuenta» saliéndose del lienzo).
- El texto del cuadro de estado del transistor **se salía de su caja**. Está
  recortado a 42 caracteres, que es lo que caben en 272 px con Roboto Mono a
  10 px.
- Y el error de la función O que cuento arriba.

---

## Imágenes y vídeos

**Cuatro fotos de Wikimedia Commons**, licencia comprobada por la API y **abierta
y mirada una a una** (créditos completos en `generadores/creditos_c5.json`):

| Fichero | Original | Autor | Licencia |
|---|---|---|---|
| `c5-ntc.jpg` | NTC Thermistor.jpg | Soumyapatra13 | CC BY-SA 4.0 |
| `c5-transistores.jpg` | Transistorer (cropped).jpg | Mister rf | CC BY-SA 3.0 |
| `c5-cilindro.jpg` | Pneumatic cylinder 2172.jpg | Mixabest | CC BY-SA 3.0 |
| `c5-valvulas.jpg` | Innenleben eines Astronauten, pneumatic control unit.jpg | Blonder1984 | CC BY-SA 4.0 |

En S1 se reutiliza `img/u7-ldr.jpg`, que ya estaba en el repositorio y ya venía
verificada.

⚠️ **La foto de la NTC no es la NTC que van a usar.** Es un disco verde marcado
`08D050`, o sea una NTC **limitadora de corriente de arranque de 8 Ω**, no una de
medir. Lo comprobé al abrirla. La dejé porque la foto es nítida, está en su
placa con la serigrafía `TH1` visible, y **convertí el problema en la lección**:
el pie explica qué es, cómo se lee el número y en qué se diferencia de la de
10 kΩ que usarán ellos. Si prefieres una de medir, hay que buscar otra en
Commons; yo no encontré ninguna claramente mejor sin gastar más peticiones (la
API tira 429 en cuanto le haces dos seguidas).

**Cuatro vídeos de YouTube**, título y canal comprobados por oEmbed:

| Sesión | ID | Título | Canal |
|---|---|---|---|
| S1 | `lD1O4KYJF9A` | 75.- Curso de electrónica.- Divisor de voltaje con LDR (Fotorresistencia). | Shakmuria |
| S2 | `TE_pQ8pyL80` | Como activar rele con transistor para arduino o raspberry (Clase 48) | ACADENAS |
| S3 | `0qBAGGq711o` | Funcionamiento Cilindro de Simple y Doble efecto | José Acuña |
| S4 | `3WvLarEkYK0` | Mando directo e indirecto de un cilindro de doble efecto \| FluidSim | ALV Electronics |

⚠️ **Nadie los ha visto enteros.** Lo comprobado es que existen, que el título y
el canal son los que dice la página y que cargan. El contenido no está revisado.
Los cuatro se cargan solo al pulsarlos y sin cookies de seguimiento.

---

## Que la unidad sirva con cualquiera de los cinco proyectos

Los ejemplos van siempre de dos o tres en dos o tres, nunca casados con uno:

- **S1**: riego automático, lámpara que se ajusta sola y aviso de aula mal
  ventilada. La actividad se hace con LDR, y una nota explica que con una NTC o
  con una sonda de humedad resistiva la pieza es exactamente la misma.
- **S2**: bomba de riego (250 mA), tira de LED (800 mA) y relé (70 mA). El alumno
  dimensiona **dos de las tres**, a elegir.
- **S3**: barrera de bicis, tapa de contenedor y empujador de cajas. Dos de tres.
- **S4**: barrera de bicis y contenedor que avisa, con la función Y aplicada a
  uno de los dos.

**El único sitio donde hubo que elegir** es la actividad de S1, que da por hecho
que el montaje de clase es con LDR y resistencia fija de 10 kΩ, porque hay que
dar números concretos para que la práctica sea evaluable. Está envuelto en una
nota que dice cómo cambia con los otros sensores.

---

## Dudas y cosas que tiene que mirar un humano

**1. Los saberes B.1 a B.4 no están transcritos en `CURRICULO.md`.** El
documento tiene la tabla criterio → saberes (4.1 → B.1·B.2·B.3·B.4) pero no dice
qué pone en cada uno. Los repartí **por tema, y es una hipótesis mía**:

| Sesión | Chip que he puesto | Por qué |
|---|---|---|
| S1 | B.1 | entradas, sensores, adquisición de la señal |
| S2 | B.2 | salidas, actuadores, electrónica de potencia |
| S3 | B.3 | neumática |
| S4 | B.3 · B.4 | neumática + representación y simbología de circuitos |

Hay que contrastarlo con el Anexo II de la Orden de 30 de mayo de 2023 antes de
que esto se use para calificar.

**2. El test.** Está al final de S4 porque S8 no existe todavía. Decisión
pendiente cuando se escriban S5-S8 (ver arriba).

**3. `generadores/voz.py` entra en el repositorio con este commit, y no lo había
pedido nadie.** El encargo dice que la voz se genera con `generadores/voz.py`,
pero ese fichero **no estaba en git**: existe en el repositorio principal sin
commitear desde siempre, así que en el worktree no había nada. Lo reescribí
idéntico para poder generar el audio. Como el encargo manda commitear con
`git add -A`, ha entrado.

No creo que moleste —sin él, quien clone el repositorio no puede regenerar el
audio de ninguna unidad, ni de esta ni de las de 2.º— pero **la decisión es
tuya** y no era mía: si prefieres que siga fuera, `git rm --cached
generadores/voz.py` y listo. El mp3 y la envolvente están commiteados aparte, así
que quitarlo no rompe la página.

En el mismo saco va `ENCARGO.md`, que también lo ha arrastrado el `git add -A`.

**4. Cifras que son estimaciones, no medidas.** Están rotuladas como tales
*dentro* de la página, pero las dejo aquí juntas por si alguna te chirría:

- El **10-15 % de rendimiento** del aire comprimido (electricidad que acaba en
  trabajo útil). Es una cifra que se maneja en el sector y que repiten los
  fabricantes; **no la he podido rastrear hasta una fuente primaria**. Aparece
  dos veces (S3 y la lectura) y en las dos sale dicho que es una estimación.
- La **regla del paso de la válvula** (2 mm → 100 NL/min a 6 bar, y el caudal va
  con el área). Es una regla de tanteo para ver de qué tamaño es el problema,
  no un dato de catálogo. Sale dicho en el pie de la escena.
- El **muelle del simple efecto** modelado como 0,5 bar equivalentes.
- El **tiempo de corte de 1 µs** y las inductancias de las cargas (5 mH el
  motor, 100 mH la electroválvula): órdenes de magnitud, no medidas.
- Los **modelos de LDR y NTC** son los del fabricante, no la medida de la LDR
  concreta que haya en el aula. Dos LDR del mismo saquito se llevan fácil un
  30 %, y eso sale dicho en la escena.

**5. No he probado Tinkercad.** Las dos actividades que lo usan (S1 y S2) están
escritas por lo que sé que hace, no por haberlo abierto. En concreto, la
actividad de S2 pide comprobar si el simulador avisa o no de que falta el diodo
de rueda libre; lo escribí como **pregunta al alumno**, no como afirmación, justo
porque no lo he verificado. Si lo abres y resulta que sí avisa, la actividad
sigue funcionando (la respuesta cambia, la pregunta no).

**6. El verificador se salta una cosa: el audio.** Comprueba que el componente
del avatar está montado, pero no que el mp3 suene. Eso hay que oírlo (son 2:14).

**7. Diferencia de redondeo Python/JavaScript.** Me costó dos falsos fallos en el
verificador: `toFixed` de JavaScript sube el 0,5 y Python redondea al par
(1,25 → «1,2» en Python, «1,3» en JS). Está resuelto con un helper en
`c5_verifica.py`, pero conviene saberlo para los próximos verificadores.

---

## Lo que queda pendiente (S5 a S8)

Están puestas con título en la navegación, deshabilitadas, para que la cadena de
la unidad se lea entera desde el primer día. El cierre de S4 anuncia las cuatro:

- **S5 · Del esquema al montaje** — protoboard, polímetro, del simulador a la placa.
- **S6 · El programa que decide** — umbrales, histéresis, el `if` que no parpadea.
- **S7 · Electroválvulas y secuencias** — la pieza que es eléctrica por un lado y
  neumática por el otro; finales de carrera y secuencias A+B+A−B−.
- **S8 · El automatismo completo** — el proyecto del curso funcionando entero, e
  impacto.

Son **una propuesta mía**, no del encargo: cámbialas si no encajan con lo que
tengas pensado para el proyecto.
