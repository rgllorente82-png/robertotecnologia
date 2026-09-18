# Informe · segunda mitad de la unidad 4 de 4.º (Mecanismos y sistemas de control)

Sesiones **5, 6, 7 y 8**, escritas sobre la primera mitad ya publicada. La página
queda con **8 sesiones escritas y 0 pendientes**.

```
~/venv/bin/python generadores/c4_build.py      -> 8 sesiones (8 escritas, 0 pendientes)
~/venv/bin/python generadores/c4_verifica.py   -> 433 comprobaciones, 0 fallos
```

No se ha tocado nada de las sesiones 1 a 4 ni `4eso/Tecnologia/index.html`.

---

## 1 · Qué hay escrito

| | Título | Escena nueva | Foto | Vídeo |
|---|---|---|---|---|
| **S5** | Ni a tope ni parado | `PROPORCIONAL` (`pr-`) | válvula termostática | control proporcional |
| **S6** | El lunes había un charco | `SKETCH` (`sk-`) | Arduino IDE con `Blink` | `delay` → `millis` |
| **S7** | La sonda del compañero no te vale | `SONDA` (`so-`) | sondas de suelo con cinta métrica | sensor de humedad con Arduino |
| **S8** | Rómpelo tú antes de que lo rompa diciembre | `SEMANA` (`sm-`) | programador de riego de grifo | huerto inteligente completo |

Ficheros nuevos:

- `generadores/c4b_escenas.py` — escenas de S5 y S6.
- `generadores/c4b_escenas2.py` — escenas de S7 y S8.
- `generadores/c4b_texto.py` — el texto de las cuatro sesiones, sus fichas de
  práctica, sus cierres y el test `c4b`.
- `generadores/c4b_busca.py`, `c4b_fotos.py`, `c4b_mirada.py` — los scripts con
  los que se buscaron, se comprobaron y **se miraron** las cuatro fotos.
- `img/c4-valvula-termostatica.jpg`, `c4-arduino-ide.png`,
  `c4-sondas-profundidad.jpg`, `c4-programador-riego.jpg`.

Cambios en ficheros existentes: `generadores/c4_build.py` (importa
`c4b_texto` y sustituye los cuatro `pendiente=True`) y
`generadores/c4_verifica.py` (ampliado, ver §5).

---

## 2 · La decisión de fondo: el proyecto ya está elegido

La primera mitad rota entre los cinco candidatos porque cuando se escribió el
proyecto no estaba decidido. Estas cuatro sesiones aterrizan en lo que dice
`PROYECTOS.md` (bloque DECIDIDO, 18-sep-2026): **riego automático** como
proyecto principal, con las variantes de **ventilación** y **lámpara**.

Cómo se ha repartido eso:

- **S5** es la única que trata las tres variantes a la vez, y a propósito: la
  escena las pone en pestañas con el **mismo modelo detrás**, para que se vea
  que el control es el mismo y solo cambian el sensor y el actuador. Ahí es
  donde el grupo que ha elegido B o C encuentra su caso.
- **S6, S7 y S8 van todas sobre el riego.** No es pereza: son las tres
  sesiones de *montaje* y la escena tiene que ser una maceta concreta con
  números concretos. Cada una pregunta algo distinto —el programa (S6), dónde
  va el sensor (S7), el sistema entero comparado con las alternativas (S8)— y
  las prácticas están redactadas para que el grupo de ventilación o de lámpara
  traduzca a lo suyo. **Si a la vista del aula parece poco para esos dos
  grupos, es lo primero que yo cambiaría.**

Las cuatro escenas de riego comparten las mismas constantes físicas, y eso es
deliberado: 1 punto de humedad = 5 ml, bomba de 100 ml/min, la maceta pierde la
mitad de su agua en unas 42 h. Un alumno puede llevarse un número de la S6 a la
S8 y le cuadra.

---

## 3 · Lo que enseña cada escena, y qué calcula

Las cuatro simulan de verdad. Ninguna tiene un número escrito a mano.

**S5 · `PROPORCIONAL`.** Integra por Euler `dX/dt = (libre + gmax·u − X)/τ`
para los tres proyectos, con dos controladores a elegir. Mide sobre el último
40 % de la simulación media, oscilación, error permanente, ciclos y gasto del
actuador. Y **al lado enseña la cuenta**:

```
error permanente = |consigna − libre| / (1 + Gmax/BP)
```

El verificador comprueba las dos cosas por separado: la medida contra una
simulación gemela en Python, y la medida contra la fórmula. El hallazgo que
justifica la sesión: todo-nada acierta de media pero oscila; el proporcional no
oscila pero se queda corto **siempre**, y cuánto se queda corto sale de una
cuenta de una línea. De ahí se nombra la acción integral sin desarrollarla.

**S6 · `SKETCH`.** Ejecuta el programa del riego durante siete días con el
ruido del sensor dentro, y el panel de código **se reescribe** con lo que haya
marcado. La maceta tiene **tiempo muerto de verdad** (10 min hasta que el agua
llega a la sonda), que es lo que hunde al que riega «hasta que la sonda diga
basta». Resultados medidos:

| | agua | charco | bomba en seco | mínimo | máximo |
|---|---|---|---|---|---|
| todo puesto | 467 ml | 0 | 0 min | 31,3 % | 40,0 % |
| sin la media de 10 | 533 ml | 0 | 0 | 34,6 % | 41,5 % |
| sin dosis | 750 ml | 0 | 0 | 31,4 % | 81,9 % |
| sin dosis y sin tope | 1483 ml | 799 ml | 1039 min | 24,3 % | 100 % |
| `delay()` sin dosis | 1483 ml | 1126 ml | 4635 min | 8,5 % | 100 % |
| sonda averiada, con tope | 1200 ml | 192 ml | 0 | 31,5 % | 100 % |
| sonda averiada, sin tope | 1483 ml | 874 ml | 83 min | 24,9 % | 100 % |

Lo que más me gusta de esta escena es que **el tope de seguridad no cambia nada
hasta que marcas la avería**. Eso está explotado en el texto y en la práctica.

**S7 · `SONDA`.** Maceta de dos compartimentos (costra de 1,5 cm que se evapora
deprisa, cepellón donde bebe la raíz) con percolación entre ellos. La sonda
mide una mezcla de los dos según profundidad y distancia al gotero. Con la
sonda en el charco (1 cm, pegada al gotero): **500 ml/semana, 306 de
evaporación y 41 % de rendimiento**; en la raíz (6 cm, a 3 cm): **400 ml, 261
y 43 %**. Cien mililitros por semana —una quinta parte del gasto— por mover la
sonda cinco centímetros. La dosis tiene además un punto óptimo: pequeña
desperdicia por evaporación, grande encharca la raíz (con 120 s la raíz llega
al 69 %).

**S8 · `SEMANA`.** Las mismas dos semanas, la misma maceta y el mismo tiempo
con tres sistemas a la vez. Cierra el problema con el que abre la S1 (las
vacaciones de Navidad), ahora con números:

| | agua | mínimo | horas marchita |
|---|---|---|---|
| a mano | 0 ml | 0,0 % | 301 h |
| temporizador 100 ml/día | 1500 ml | 12,0 % | 13 h |
| lazo cerrado | 1467 ml | 29,9 % | 0 h |

Y lo importante: **ninguna dosis fija del temporizador pasa las dos semanas sin
apuro** (40 → 157 h marchita; 100 → 13 h; 160 → 85 h; 250 → 190 h; 300 →
210 h). Eso es, medido, lo que la S1 decía con palabras. Con la avería de la
sonda, el lazo cerrado pasa a ser el peor de los tres, y el texto lo dice en
vez de esconderlo.

---

## 4 · Decisiones que conviene revisar

1. **El test de la S8 usa `test('c4b', ...)`**, con sus propios `name="c4b-N"`.
   El verificador comprueba explícitamente que los dos tests conviven y que
   contestar uno no marca nada en el otro (30 radios `c4-N` y 30 `c4b-N`).
   Ninguna clase CSS nueva empieza por `test-`; los prefijos son `pr-`, `sk-`,
   `so-` y `sm-`.

2. **Los datos de las escenas de riego son un modelo, no una medida.** Está
   dicho dentro de la página, en un recuadro de la S7: el 8 % de costra, las
   10 h de secado de la superficie y el 15 % como punto de marchitez son
   valores razonables elegidos por nosotros. Lo que se sostiene es la forma de
   las curvas y la comparación entre dos configuraciones. Si alguien quiere
   cifras reales de una maceta concreta, hay que medirlas.

3. **El generador de ruido de las escenas es un Lehmer (MINSTD, ×16807)** y no
   el LCG clásico. Motivo: `sem * 1103515245` se sale de los 2⁵³ que un `double`
   guarda exacto, así que el resultado dependía del redondeo del navegador. La
   escena parecía reproducible pero no se podía volver a calcular en Python, y
   el verificador no podía comprobarla. Con 16807 el producto nunca pasa de
   3,6·10¹³ y JS y Python dan el mismo número. **Esto lo cacé escribiendo el
   verificador, no leyendo el código.**

4. **La banda proporcional del riego llega hasta 120** (que es el `Gmax` del
   modelo) y la simulación dura 10 días. Con bandas mayores el lazo se vuelve
   tan lento que en la ventana de medida todavía queda transitorio, y entonces
   la escena mediría una cosa y la fórmula diría otra **delante del alumno**.
   Lo mismo con la ventilación, que pasó de 4 a 8 h simuladas.

5. **Los títulos de los cuatro vídeos llevan emojis decorativos** en YouTube
   (el de la S5, por ejemplo, es «1. Acción de CONTROL PROPORCIONAL ►
   [Explicación Sencilla] 😎 Control PID ☑️»). Se han quitado al ponerlos en la
   página: los emojis los dibuja el sistema operativo y cambian en cada
   aparato. El texto es por lo demás el que devuelve la API.

6. **En la página no hay ni un emoji**, en línea con las otras nueve unidades
   de 4.º (comprobado con `grep`).

---

## 5 · Qué comprueba el verificador ampliado

`generadores/c4_verifica.py` pasa de 124 a **433 comprobaciones**. Lo nuevo:

- **S5**: once combinaciones de (proyecto, controlador, consigna, histéresis,
  banda, perturbación) contra una simulación gemela en Python, más el error
  permanente contra la fórmula. Y las cuatro afirmaciones de la sesión, como
  aserciones: el proporcional no oscila y el todo-nada sí; el todo-nada acierta
  la media y el proporcional no; estrechar la banda reduce el error; la
  perturbación lo agranda.
- **S6**: catorce combinaciones de interruptores contra el gemelo, comparando
  agua, charco, minutos en seco, arranques y mínimo. Y que **el panel de código
  cambia**: sin `millis()` aparece `delay(1800000)`, sin la media aparece
  `return analogRead(A0)`, sin tope desaparece `segsDia >= 150`.
- **S7**: ocho posiciones y dosis contra el gemelo (agua, evaporación,
  rendimiento, mínimo y máximo de la raíz), más los dos botones de preajuste y
  la comparación charco/raíz.
- **S8**: ocho escenarios × tres sistemas contra el gemelo, y el barrido de
  dosis del temporizador que demuestra que no hay ninguna que aguante.
- **Los dos tests**, por separado, y que no se pisan los `name`.
- Bloques de libreta, «solo para entenderlo», vídeo, escena, fotos y créditos
  para las **ocho** sesiones (antes solo las cuatro primeras).
- Que no queda ninguna sesión deshabilitada y que hay ocho cuerpos de sesión.

Los gemelos en Python son código aparte que implementa el mismo modelo: si una
escena dejara de calcular y empezara a fingir, la comparación lo caza.

---

## 6 · Dudas y cosas que debería mirar un humano

1. **Los cuatro vídeos: nadie los ha visto enteros.** Están comprobados título
   y canal con la API oEmbed de YouTube el 18-sep-2026, y eso es todo lo que
   dice la API. La página lo advierte en cada uno. **Hay que verlos antes de
   ponerlos en clase.** El de la S6 (`hq999kZk3Hg`) entra en el desbordamiento
   de `millis()` y en aritmética binaria, que se va de 4.º; el de la S5
   (`wkPI1BDp63E`) es el primero de una serie de control PID y puede que dé por
   supuesto más nivel del que hay.

2. **La foto de la S6 tiene los menús en japonés.** Es una captura del Arduino
   IDE 2 con el ejemplo `Blink`, y se eligió porque muestra literalmente los dos
   `delay(1000)` que la sesión critica. El pie lo dice. Si molesta, hay
   alternativas en Commons en inglés (`File:Arduino IDE on Windows 10.png`,
   CC BY-SA 4.0) pero son de menos resolución y no se lee el código.

3. **El punto de marchitez del 15 %** aparece en tres escenas como línea roja.
   Es una convención didáctica: el valor real depende de la textura del suelo.
   Está advertido en la página, pero si el departamento tiene un dato mejor,
   cambiarlo es una constante en tres sitios (`c4b_escenas.py` y
   `c4b_escenas2.py`, busca `15`).

4. **La práctica de la S7 pide pesar la maceta seca**, y eso son dos semanas
   sin regar. Está previsto el atajo (secar un vaso de la misma tierra en el
   radiador y hacer la regla de tres), pero conviene que el profesor arranque
   esa pesada **al principio del tema**, no el día de la sesión 7.

5. **Los grupos de ventilación y lámpara.** Como digo en §2, las sesiones 6, 7
   y 8 van sobre el riego y ellos traducen. Creo que aguanta, pero es la
   decisión que menos seguro tengo.

6. **Una cosa de la primera mitad, que no he tocado** (el encargo dice que la
   diga en vez de arreglarla): en la sesión 4, el bloque «Solo para entenderlo»
   de las tres maneras de arreglar la barrera afirma que acortar el brazo de 80
   a 40 cm baja el par «al **cuadrado**», y da 1,5 kg·cm frente a 6,0. El
   número es correcto (baja a la cuarta parte) pero la palabra no: el par es
   proporcional a **L²** y por eso al mitad de longitud queda la cuarta parte.
   Decir «baja al cuadrado» es ambiguo y un alumno puede leerlo como «se eleva
   al cuadrado». Sugerencia: «baja **a la cuarta parte**, porque el listón
   mitad de largo pesa la mitad **y** tiene el brazo mitad».

7. **Fronteras con las unidades de al lado.** Creo que están respetadas y así
   lo dice la página:
   - la electrónica entre el pin y el actuador (divisor, transistor, relé) se
     **usa montada** y se remite explícitamente a la **unidad 5**;
   - la S6 programa **el control** (el lazo que gira, la dosis, el margen, el
     tope) y remite a la **unidad 6** para programación como materia, datos e
     IoT;
   - el impacto se mide como **prueba del sistema** y se remite a la
     **unidad 8** para tratarlo.

   Los dos sitios donde creo que puede haber roce, y que un humano debería
   contrastar con quien escriba esas unidades:
   - **PWM y `analogWrite`** están explicados en la S5. Son la manera de
     entregar una orden proporcional, así que aquí hacen falta; pero si la
     unidad 6 los explica también, hay que decidir quién los introduce y quién
     los da por sabidos.
   - **El patrón de `millis()`** está explicado en la S6. Es un patrón de
     programación, no de control, pero sin él no hay control que funcione. Mismo
     caso.

8. **`generadores/guion_c4.txt` sigue siendo el de la primera mitad**, así que
   la voz del narrador de la S1 no menciona nada de las sesiones nuevas. No lo
   he tocado porque el encargo era escribir las sesiones, pero si se regenera
   el audio conviene revisarlo.
