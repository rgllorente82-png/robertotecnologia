# Informe · sesiones 4, 5 y 6 de la unidad 6 de 2.º (Electricidad y electrónica)

Rama `tema6b`. La unidad queda **completa: 6 de 6 sesiones**. Lo que sigue cuenta qué
he hecho, qué he decidido por mi cuenta, qué no me cuadra y **qué hay que mirar antes de
publicarlo**.

---

## 1 · Qué hay nuevo

| Fichero | Qué es |
|---|---|
| `generadores/u6_build.py` | Sustituidas las tres entradas `pendiente=True` por las sesiones 4, 5 y 6 completas. |
| `generadores/u6_escenas2.py` | **Nuevo.** Las tres escenas interactivas nuevas. Usan la biblioteca `window.U6` de `u6_escenas.py`; no he dibujado ni un símbolo por mi cuenta. |
| `generadores/u6_verifica.py` | **Nuevo.** Abre la página en Chromium y pulsa todos los controles de las seis escenas. Sale 0 si todo va bien. |
| `img/u6-contador-viejo.jpg`, `u6-contador-nuevo.jpg`, `u6-led.jpg`, `u6-microbit.jpg` | Cuatro fotos de Wikimedia Commons, con licencia comprobada por la API **y miradas una a una**. |
| `2eso/TyD/index.html` | La tarjeta del tema 6 decía «3 de 6 sesiones publicadas». Ahora dice 6 de 6, con la barra al 100 % y la descripción ampliada. |

Se regenera con `~/venv/bin/python generadores/u6_build.py` y se comprueba con
`~/venv/bin/python generadores/u6_verifica.py` (**pasa entero: 95 comprobaciones**).

### Las tres sesiones

- **S4 · Lo que cuesta tenerlo encendido.** Arranca con una pregunta que no se puede
  contestar con los vatios solos (la bombilla del pasillo toda la noche contra el
  microondas cinco minutos: 72 Wh contra 83 Wh, casi empate; y con una bombilla vieja de
  60 W, 480 Wh, seis veces más). De ahí sale la necesidad de dos magnitudes: P = V × I y
  E = P × t. Luego el kWh, la factura línea a línea, la etiqueta energética y el CO₂.
  Cierra el hilo que la sesión 2 dejó abierto (por qué el hilo del tostador se pone al
  rojo y el cable no: P = I² × R).
- **S5 · El componente que no perdona.** El LED conectado «como una bombilla» se muere;
  la resistencia del compañero no vale porque no está calculada. Diodo, polaridad,
  tensión directa, **el LED no es óhmico** (que es la razón por la que hay que limitar
  desde fuera), R = (Vs − Vf)/I, serie E12 y siempre hacia arriba. Después pulsador
  frente a interruptor, y la micro:bit con sus dos números: 3 V y 5 mA por pin.
- **S6 · Que sirva para algo.** Reto: escribir un problema sin nombrar el aparato.
  Dossier de seis apartados, cuatro proyectos posibles, el test que se corrige solo y el
  cierre del tema, que deja abierta la pregunta del tema 7 («¿y si quiero que decida
  solo?»).

### Las tres escenas, y qué calcula cada una

Ninguna tiene números escritos a mano: todo sale de la cuenta, y el fichero de
verificación comprueba los resultados contra cuentas hechas aparte.

1. **La regleta** (S4). Ocho aparatos que se enchufan. Calcula la corriente de cada uno
   (I = P/230), la suma de potencias, la corriente total, los kWh, los euros y los gramos
   de CO₂ según las horas y el precio que pongas. Compara la corriente contra dos límites
   distintos —los 16 A de la base y la potencia contratada— y distingue **calentar el
   cable** de **hacer saltar el automático**, que es la confusión típica.
2. **El banco del LED** (S5). Fuente, color y corriente deseada; calcula la tensión que
   sobra, la R teórica, busca el valor **E12 que existe de verdad**, recalcula la
   corriente real y la potencia disipada, y avisa si pasas de los 20 mA del LED o de los
   5 mA del pin. Dibuja además una regla logarítmica con los cinco valores E12 vecinos y
   marca dónde cae tu cuenta. El **pulsador del dibujo funciona como un pulsador**:
   alumbra mientras lo mantienes apretado (ratón, dedo o teclado) y se apaga al soltar; el
   interruptor se queda. Con «Quitar la resistencia» el LED se quema y el pie explica que
   ahí no hay número que poner **porque el LED no es óhmico**.
3. **El test** (S6). Diez preguntas: cuatro de calcular con números generados al azar y
   seis de razonar con las opciones barajadas. Se corrige resolviendo la cuenta, no
   comparando contra una lista de respuestas, así que «Otra tanda» da un examen distinto.
   Tolerancia del 2 % para que redondear no cueste un punto. Marcador en SVG con la nota.

---

## 2 · Decisiones que he tomado yo

1. **La escena de S4 es una regleta, no una factura interactiva.** Me pareció que
   enganchaba mucho mejor con la sesión 3 (todo está en paralelo → las corrientes se
   suman → por eso se calienta la regleta) y de paso da el susto útil. La factura va como
   tabla en la teoría y como ejercicio en la práctica.
2. **La factura de ejemplo es mía y cuadra.** 30 días, 3,45 kW, 250 kWh: 10,35 + 45,00 =
   55,35 → +5,11 % de impuesto = 2,83 → +0,81 de alquiler → base 58,99 → +21 % de IVA =
   12,39 → **71,38 €**, o sea **0,2855 €/kWh reales** frente a los 0,18 de la tarifa. Los
   precios de los dos términos van rotulados como «de ejemplo»; los porcentajes van
   fechados en septiembre de 2026 y avisando de que cambian.
3. **En S6 la «escena» es un formulario HTML con un marcador SVG**, no un dibujo. Un test
   que se corrige solo no da para dibujo, y el encargo pedía la autoevaluación. El
   marcador (los diez recuadros, la barra y la nota) sí se dibuja a partir del resultado.
4. **La parte de MakeCode de la actividad 5 es opcional** («si hay micro:bit») y vale un
   solo punto: programar es la U12 y no quiero adelantarla. La micro:bit entra aquí como
   **fuente de 3 V con un límite de 5 mA**, que es lo que obliga a calcular.
5. **La sesión 6 lleva otro minutado** (5 / 35 / 15 / 5) porque es proyecto, no clase.
   Está como `MIN6` en `u6_build.py`.
6. **He tocado un dato de la teoría de S5 que había escrito mal yo mismo**: decía que el
   salto del 20 % entre valores E12 «es la tolerancia con la que se fabrican». No lo es:
   el salto es del ~21 % y la tolerancia de una E12 es **±10 %**, que es lo que hace que
   los márgenes de dos vecinas se toquen. Está corregido y explicado así.

---

## 3 · Comprobaciones hechas

**Vídeos.** Título y canal comprobados con la **API oEmbed de YouTube** el 17-sep-2026:

| Sesión | ID | Canal | Título |
|---|---|---|---|
| S4 | `9qWYeA5y_r0` | Ruben Sebastian | Potencia y energía eléctrica: ¿Cuánto costará? |
| S5 | `Bw4nVt8eQkw` | ITC MENTOR Academy | Cómo CALCULAR la RESISTENCIA para un LED ⚡ (Ley de Ohm FÁCIL) |

⚠️ **Nadie los ha visto enteros.** Sé que existen, que están públicos y que el título y el
canal son los que pongo; no sé qué dicen en el minuto siete. **Hay que verlos antes de
mandárselos a un alumno.** En S6 no he puesto vídeo: es una sesión de hacer, y no
encontré ninguno que aportara algo que no estuviera ya en la página.

**Imágenes.** Licencia consultada por la API de Commons y **cada una abierta y mirada**:

| Fichero | Autor | Licencia |
|---|---|---|
| `u6-contador-viejo.jpg` | RobbieIanMorrison | CC BY 4.0 |
| `u6-contador-nuevo.jpg` | RobbieIanMorrison | CC BY 4.0 |
| `u6-led.jpg` | oomlout | CC BY-SA 2.0 |
| `u6-microbit.jpg` | SimonWaldherr | CC BY 4.0 |

Los pies dicen **solo lo que se ve en la foto**: los 65.521,9 kWh y el «375 U/kWh» del
contador viejo, los «000000 kWh» y el «500 imp/kWh» del nuevo, los cinco anillos del borde
de la micro:bit. Dos avisos:

- El aviso de licencia de la página dice que «dos [fotos] son de dominio público por su
  antigüedad»: sigue siendo cierto después de añadir estas cuatro (Ohm y la lámpara de
  Edison).
- **Los títulos engañan, confirmado.** Descarté
  `File:Stanley Electric BR5064X Closeup of the 5mm LED..jpg`: el título promete un
  primer plano del chip y es una macro desenfocada de varias cúpulas sin patas ni chip
  visibles. Si no llego a abrirla, la pongo.

**La página.** `u6_verifica.py` comprueba: cero errores de JavaScript, las seis escenas
pintan y responden, los números que sacan coinciden con las cuentas de referencia, las
siete fotos cargan con su tamaño real, los cinco vídeos están y el diferido funciona, cada
sesión tiene sus bloques de libreta y su ficha, y **nada se sale del `viewBox`** de ningún
SVG (esta última cazó dos rótulos largos). Mirado además a ojo, en claro y en oscuro.

---

## 4 · Datos de fuera: de dónde sale cada número

| Dato | Valor | Fuente |
|---|---|---|
| Precio del kWh, hogares españoles | 0,2669 €/kWh (2.º sem. 2025, impuestos incl., banda 2.500-5.000 kWh/año) | **Eurostat**, `nrg_pc_204`, consultado por su API el 17-sep-2026 |
| CO₂ del mix eléctrico español | 258 g CO₂eq/kWh (energía producida en 2025) | CNMC, vía la tabla histórica de la Oficina Catalana del Canvi Climàtic |
| IVA e impuesto eléctrico | 21 % y 5,11 % | Vigentes desde el 1-jun-2026 |
| Etiqueta energética | Escala A-G desde el 1-mar-2021; kWh/año en frigoríficos, kWh/100 ciclos en lavadoras | Reglamento (UE) 2017/1369 |
| micro:bit | Pines a 3 V, **máx. 5 mA por pin**, 90 mA (V1) / 270 mA (V2) por el conector | `tech.microbit.org`, página del conector de borde |
| Armonización 220 → 230 V | CENELEC HD 472 S1 | Consultado para el pie de foto de los contadores |

---

## 5 · Lo que no me cuadra o hay que decidir

1. **Las tensiones directas de los LED son las que más me chirrían.** Uso rojo 2,0 ·
   amarillo 2,1 · verde 2,2 · azul y blanco 3,2 V, y en el texto digo que son típicas y
   que el valor bueno está en la hoja de características. Pero el **verde es ambiguo de
   verdad**: el verde clásico (GaP) ronda 2,1-2,2 V y el verde brillante moderno (InGaN)
   se va a 3,0-3,2, con lo que **con la micro:bit uno funciona y el otro no**. Si en el
   aula hay una bolsa concreta de LED, lo suyo es medir uno de cada color con el
   polímetro y ajustar la tabla de `COLORES` en `u6_escenas2.py` y la del bloque de
   libreta. Es el único sitio donde un alumno puede montar bien la cuenta y ver otra cosa
   en la mesa.
2. **Los 5 mA por pin de la micro:bit son la cifra prudente.** Es la que da la
   documentación oficial y con la que he hecho los ejemplos, pero el chip de la V2 admite
   más en modo «high drive». Me he quedado con 5 mA a propósito: en 2.º prefiero que
   calculen con el límite conservador. Si en algún taller hace falta más brillo, esto hay
   que revisarlo con la placa concreta delante.
3. **Las potencias de los aparatos de la escena son típicas, no medidas.** Están
   rotuladas como «potencia típica» en la propia escena y el texto manda mirar la placa de
   características. Si Roberto quiere otros aparatos o valores de su aula, se cambian en
   la lista `AP`.
4. **La factura de ejemplo lleva precios inventados** (0,10 €/kW·día y 0,18 €/kWh) para
   que las cuentas salgan redondas y comprobables. Son plausibles y el total cae justo
   donde dice Eurostat, pero **no son la tarifa de nadie**. Si preferís una factura real
   anonimizada, la tabla se cambia en cinco minutos: está en `S4`, en el `<table
   id="factura-ej">`, y las cuentas del texto que dependen de ella son dos (el 0,2855 y el
   59 %).
5. **Falta una imagen de la etiqueta energética**, que es lo que más ayudaría en esa parte
   de S4. No la he puesto porque las de Commons son SVG (el buscador del repositorio
   filtra `filetype:bitmap`) y porque el diseño de la etiqueta viene fijado por el
   reglamento: prefiero no meter una imagen cuya situación legal no he comprobado del
   todo. **Lo razonable sería dibujarla nosotros** en SVG, como una escena más, con las
   flechas A-G y el número de kWh; se puede hacer en una sesión de trabajo.
6. **`2eso/index.html` tiene el contador desfasado**: la tarjeta de 2.º TyD dice «4 de 18
   sesiones publicadas» y las publicadas de verdad son 31 de 43 contando este tema. No lo
   he tocado porque no sé si ese 18 responde a otro criterio; lo dejo apuntado.
7. **La lectura del tema no la he tocado.** Sigue siendo la misma de 31 párrafos, que
   cubre las sesiones 1 a 3. Ahora que el tema llega hasta la factura y el LED, **se queda
   corta**: valdría la pena añadirle una tanda de párrafos sobre potencia y consumo, o
   dejar claro que la lectura cubre solo la primera mitad.

---

## 6 · Lo que debería mirar un humano antes de publicar

- [ ] **Ver los dos vídeos enteros.** Es lo único que no puedo garantizar.
- [ ] **Medir un LED de cada color** de los que haya en el aula y ajustar la tabla de
      tensiones directas, sobre todo el verde (punto 5.1).
- [ ] **Decidir sobre la factura**: dejar la de ejemplo o poner una real anonimizada.
- [ ] Repasar que la **rúbrica del proyecto** (3 puntos al esquema, 3 a los cálculos)
      encaja con cómo evalúas tú el resto de la unidad.
- [ ] Comprobar en un **móvil de verdad** las escenas nuevas. Escalan con el `viewBox`
      como las tres anteriores, así que en pantalla pequeña la letra de la lista de
      aparatos queda igual de fina que la de las escenas ya publicadas; no es peor que lo
      que hay, pero tampoco es cómodo.
- [ ] Si se publica, **ejecutar `u6_verifica.py` después de cualquier cambio**: está
      escrito para que cazar una fórmula rota sea automático.
