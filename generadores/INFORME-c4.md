# Informe · Unidad 4 de 4.º de ESO · Mecanismos y sistemas de control

Rama `c4`. CE4 · criterio 4.1 · saberes B.1 a B.4.
Escritas las **cuatro primeras sesiones** de ocho; las otras cuatro quedan marcadas como
pendientes, con el título que propongo para cada una.

---

## Lo que hay

| Fichero | Qué es |
|---|---|
| `4eso/Tecnologia/tema4/index.html` | La página. 187 KB, 8 sesiones (4 escritas). Generada. |
| `4eso/Tecnologia/tema4/lectura-tema4.pdf` | Lectura de aula. 4 páginas, 30 párrafos numerados, 10 preguntas. |
| `generadores/c4_build.py` | Genera la página. Texto de las cuatro sesiones + el test. |
| `generadores/c4_escenas.py` | Las cuatro escenas (SVG + JS a mano, sin librerías). |
| `generadores/c4_lectura.py` | Genera el PDF con `lectura.py`. |
| `generadores/c4_verifica.py` | Abre la página en Chromium y pulsa todo. **124 comprobaciones, 0 fallos.** |
| `generadores/guion_c4.txt` | Guion de la voz de presentación. |
| `audio/c4-control.mp3` + `_env_c4-control.json` | Voz (110 s) y su envolvente para el avatar. |
| `img/c4-*.jpg` | Cuatro fotos de Commons. |

**No he tocado `4eso/Tecnologia/index.html`**, como pedías.

Para regenerarlo todo:

```
~/venv/bin/python generadores/c4_build.py
~/venv/bin/python generadores/c4_lectura.py
~/venv/bin/python generadores/c4_verifica.py
```

---

## La secuencia, y los dos cambios que he hecho a tu propuesta

El guion de las cuatro sesiones lo he mantenido tal cual. Dos decisiones dentro:

**1. El lazo cerrado de la S1 es todo-nada, a propósito.** Podía haber puesto un control
proporcional en la S1 (queda más «fino» y el error residual da juego), pero entonces la S3 tendría
que presentar un controlador nuevo justo cuando toca examinar el que ya conoce. Así la cadena es:
la S1 enseña **la idea** con el controlador más tonto posible, y la S3 vuelve a **ese mismo**
controlador para mirarle el precio. El proporcional queda como la sesión 5, que es donde de verdad
hace falta.

**2. He metido la saturación en la S1, que no estaba en tu guion.** Si solo se ve que el lazo
cerrado aguanta las perturbaciones, el alumno se queda con «cerrado = mejor», que es exactamente
lo que Maxwell tuvo que desmontar en 1868. Así que la escena tiene un segundo mando —las pérdidas—
y a partir de 10 W/°C **el lazo cerrado tampoco llega**, porque necesitaría más del 100 % de la
resistencia. Sale de la misma cuenta que ya está en pantalla, no hay que explicar nada nuevo, y
deja dicho que un lazo cerrado corrige mientras le quede actuador.

### Las cuatro que faltan, tal como las propongo

| | Título | Qué resuelve |
|---|---|---|
| S5 | Control proporcional | El lazo de la S1 dejaba error y el de la S3 oscilaba: las dos cosas se afinan aquí. De ahí sale el nombre del PID sin tener que entrar en él. |
| S6 | Programarlo en Arduino | Del pseudocódigo de la S3 al *sketch*, simulado en Tinkercad Circuits. |
| S7 | Montarlo de verdad | Un pin de Arduino no mueve un motor: transistor, puente en H, relé. Finales de carrera, seguridad, qué pasa al cortar la luz. |
| S8 | El sistema entero | Montar el proyecto completo, meterle la perturbación a mano y medir. Y el **test final de la unidad**. |

---

## El proyecto del curso sigue sin decidir, y la unidad no lo necesita

Ninguna cuenta de la unidad depende de cuál se elija. Donde hacía falta un ejemplo he usado varios:

- **S1** · el riego (1) abre la unidad; los ejemplos de clasificar son domésticos.
- **S2** · la escena trae **tres** proyectos completos y conmutables: riego (1), ventilación (2) y
  lámpara (5). La gracia es que el diagrama de bloques **no cambia** al pasar de uno a otro.
- **S4** · barrera (4) y contenedor/depósito (3), que son los que tienen mecanismo.
- Las prácticas piden siempre «elegid uno de los cinco».

**Dónde he tenido que elegir por mi cuenta y conviene que lo mires:**

1. **La lámpara (5) es el único de los tres cuyo actuador ilumina el mismo sitio que mira el
   sensor.** Eso la hace oscilar sola en la escena de la S2, y lo he aprovechado como gancho para
   la S3. Si al final el proyecto es otro, la escena sigue valiendo igual, pero ese puente entre
   sesiones se cuenta con la lámpara.
2. **La S2 usa la ventilación (2) como el caso en que el sensor ya entrega unidades físicas**
   (módulo digital de CO₂) frente a los otros dos, que dan cuentas del 0 al 1023. Me pareció la
   manera más corta de enseñar que el diagrama es el mismo aunque falte la conversión.

---

## ⚠️ Números que me he inventado con criterio, y que hay que mirar

Esto es lo más importante del informe.

**Las rectas de calibración de los sensores son plausibles, no medidas.** En la S2 digo que la
sonda capacitiva marca 620 al aire y 280 en agua, y que la LDR marca 90 a oscuras y 870 con la
persiana abierta. Los órdenes de magnitud y los signos son correctos (una sonda capacitiva **baja**
al mojarse; una LDR con divisor **sube** con la luz), y el texto los presenta como «medido en
clase», que es como se hace de verdad. Pero **yo no los he medido**. Con sondas distintas salen
otros números. Dos salidas: medirlos una vez con el material del centro y sustituirlos, o dejar
claro en clase que son los de un ejemplo y que los suyos serán otros —que además es justo lo que
pide la práctica.

**Los pares de los motores son valores típicos de catálogo, no medidos.**

| Motor | Par | Velocidad | Confianza |
|---|---|---|---|
| Servo SG90 | 1,8 kg·cm a 4,8 V | 0,1 s/60° → 100 rpm | Alta, es el dato del fabricante |
| Motorreductor TT 1:48 | 0,8 kg·cm | 200 rpm a 6 V | Media, varían mucho entre lotes |
| Motor DC de juguete (FA-130) | 0,02 kg·cm | 9.000 rpm a 3 V | **La más floja.** Es un par útil aproximado |

El tercero está sobre todo para que se vea que un motor sin reductora no mueve nada, y en ese papel
funciona aunque el número baile. Aun así, si tienes la hoja de características de los que hay en el
taller, merece la pena cambiarlos: la escena los coge de una lista de tres líneas en
`c4_escenas.py`.

**Lo que es criterio nuestro va rotulado como tal dentro de la página**: el rendimiento η = 0,90 de
un par de engranajes de plástico y la regla de multiplicar el par por 2 como margen aparecen bajo
el rótulo «criterio de clase, no norma oficial».

---

## Saberes B.1 a B.4: no están transcritos

`CURRICULO.md` da los **códigos** de los saberes de 4.º pero no su texto (a diferencia de algunos
de 2.º). Así que **no he repartido los saberes por sesión**: habría tenido que adivinar qué dice
cada uno. Las cuatro sesiones llevan el mismo par de chips, `CE4 · 4.1` y `B.1 a B.4`.

En cuanto tengas el texto de los cuatro, repartirlos es cambiar una línea (`SAB` en
`c4_build.py`).

---

## Las escenas: qué calculan y cómo está comprobado

Las cuatro integran o calculan de verdad. Ninguna lleva un número escrito a mano.

- **S1 · Dos hornos** — integra por Euler, paso de 1 s, el mismo modelo térmico
  `C·dT/dt = u·P − k·(T−T_amb)` en los dos a la vez. El de lazo abierto aplica el 64 % que sale de
  `k₀·(180−20)/P`; el cerrado mide y decide. El botón **«Avanza 1 hora»** integra 3.600 pasos de
  golpe, que es lo que evita que una clase se quede mirando una curva durante diez minutos.
- **S2 · Diagrama de bloques** — ejecuta el lazo 10 veces por segundo simulado. Los números que hay
  **dentro** de cada caja son los que circulan, y debajo está la aritmética escrita entera. El
  interruptor de «cortar la realimentación» deja el mismo aparato en lazo abierto con temporizador.
- **S3 · Termostato** — simula tres horas con paso de 2 s y **mide** sobre la última hora los
  ciclos por hora, la amplitud, la media y el porcentaje de uso. Nada de eso está escrito. Además
  contrasta el porcentaje medido con el que exige el balance de energía, y enseña las dos cuentas
  al lado.
- **S4 · Banco de motores** — par necesario, par disponible tras la reductora, velocidad de salida,
  tiempo de maniobra y potencia. Los engranajes están dibujados con **geometría correcta**: los dos
  con el mismo módulo, radio primitivo `r = m·z/2`, cabeza a `+m`, pie a `−1,25m`, ejes a `r₁+r₂` y
  la corona desfasada medio paso para que un diente caiga en un hueco. Nada de patatas: el
  verificador cuenta los dientes dibujados y comprueba que son los `z` pedidos.

**El verificador no se conforma con que la página pinte.** `c4_verifica.py` vuelve a calcular en
Python los mismos modelos y compara uno a uno con lo que hay en pantalla: las dos temperaturas de
la S1 para tres perturbaciones, las cuatro medidas de la S3 para cinco anchos de histéresis, y la
relación, velocidad, par y potencia de la S4 para cinco combinaciones. Si una escena dejara de
calcular y empezara a fingir, salta.

Salida actual: **124 comprobaciones, 0 fallos.**

Dos cosas que la escena de la S4 dice de sí misma, para no engañar:

- La maniobra se anima a la velocidad calculada, pero **con un mínimo de 3 s en pantalla**. Cuando
  la de verdad es más corta, el propio pie lo avisa con el número real.
- Con motores rápidos la barrera sube en 0,2 s, que es absurdo para una barrera. Es correcto y está
  bien que se vea: el arreglo (final de carrera, arranque suave) es materia de la S7.

---

## Vídeos: comprobados, pero sin ver

Cuatro, uno por sesión. **Título y canal verificados por la API oEmbed de YouTube el 18-sep-2026.**
Lo que la API dice es quién los firma y cómo se llaman; **no dice si son buenos, y nadie del
proyecto los ha visto enteros.** La propia página se lo dice al alumno en la nota de cada vídeo.

| Sesión | ID | Título | Canal |
|---|---|---|---|
| S1 | `2SHQTUvvVuM` | Sistemas de control · Robótica | STEM con Pablo |
| S2 | `zJ5TP_kkT2E` | Tecnología de control: tipos de sistemas de control automático | Guillermo A. Pennesi |
| S3 | `i_GwbZLur2Y` | Termostato on-off sin y con histéresis | sergiotecnoedu |
| S4 | `3JA5UTvTfYE` | Transmisión por engranajes: características y cálculo | Daniel Reynaga |

El de la S2 es el que menos me convence: casi todo lo que hay en español sobre diagramas de bloques
es de universidad y va de álgebra de bloques y funciones de transferencia, que aquí no toca. Ese es
de nivel de secundaria, pero si al verlo no encaja, la sesión funciona igual sin él.

---

## Fotos: licencia comprobada por API y **abiertas una a una**

| Fichero | Qué es | Autor | Licencia |
|---|---|---|---|
| `c4-regulador-watt.jpg` | Regulador de bolas de una máquina Boulton & Watt | Dr. Mirko Junge | CC BY 3.0 |
| `c4-arduino-uno.jpg` | Arduino Uno R3 | SparkFun Electronics | CC BY 2.0 |
| `c4-bimetal.jpg` | Dos espirales bimetálicas de termostato | Shorenster | CC BY-SA 3.0 |
| `c4-servo-sg90.jpg` | Micro servo SG90 | Suyash Dwivedi | CC BY-SA 4.0 |

Las cuatro se ven bien y enseñan lo que dice el pie (en la del bimetal se distinguen **las dos
capas** en el canto de la espiral de la derecha, que es justo lo que hay que mirar).

**Un detalle honesto sobre la del servo**: la descripción en Commons dice que es una unidad
*falsificada* de Tower Pro. Visualmente es idéntica a la original y lo que se explica —que dentro
lleva motor, reductora y potenciómetro— vale igual, así que la he dejado y no lo menciono en el
pie. Si prefieres no usar una foto de un clon, dímelo y busco otra.

---

## La lectura

`lectura-tema4.pdf`, 4 páginas, 30 párrafos numerados y 10 preguntas (las dos últimas de opinión
razonada, como marca la plantilla).

No repite las sesiones: cuenta la **historia y el precio**. La cisterna del váter, Ktesibios y el
reloj de agua, el regulador de Watt (incluido que no lo inventó él), los ochenta años que se tardó
en explicarlo, Maxwell, el termostato de Warren Johnson con su gota de mercurio, el acople del
micrófono… y un caso real.

**Aviso sobre el último bloque.** Los párrafos 25 a 28 cuentan el caso del Boeing 737 MAX: el
sistema MCAS tomaba el ángulo de **un solo sensor**, y cuando ese sensor mintió cayeron dos aviones
—Lion Air 610 en octubre de 2018 con 189 personas y Ethiopian 302 en marzo de 2019 con 157—. Lo he
metido porque es la manera de que «¿y si el sensor miente?» deje de sonar a manía del profesor, y
porque la conclusión técnica es exactamente la de la unidad. Pero **menciona 346 muertos**, y eso
es decisión tuya, no mía: si para este grupo no toca, el bloque son cuatro párrafos seguidos y se
sustituyen sin tocar nada más (sirve, por ejemplo, un fallo de termostato en un invernadero, aunque
pierde fuerza).

---

## El test

Diez preguntas al final de la S4, con `test_auto.py`. Las diez explican el porqué tanto si se
acierta como si se falla. **No he inventado ninguna clase CSS que empiece por `test-`** (el único
`test-c4` que hay es un `id`, que es lo que genera la propia herramienta).

Ojo a una cosa: **este test cubre S1-S4, no la unidad.** Lo he puesto en la S4 porque es la última
sesión escrita y porque una autoevaluación a mitad de unidad tiene sentido, pero **el test final de
la unidad va en la S8**, cuando existan las ocho. Está rotulado como «lo que tiene que haber
quedado de estas cuatro sesiones» para que no se confunda.

---

## Una cosa que hubo que traer de otra rama

**`generadores/voz.py` no existía en esta rama.** El encargo lo da por hecho, pero solo vive en las
ramas `tema6` y `tema7` y nunca se ha fusionado a `main`. Lo he copiado tal cual (sin tocar una
línea) para que el comando del encargo funcione, y va en el commit.

Alguien tiene que decidir si eso se queda así o si `voz.py` debería subir a `main` de una vez: es
una herramienta común, no de un tema, y va a hacer falta en todas las unidades que lleven voz.

---

## Coherencia con 2.º

- **La relación de transmisión usa exactamente el convenio del tema 5 de 2.º**:
  `i = z₁/z₂ = n₂/n₁`, el 1 es la entrada y el 2 la salida, `i < 1` es reductor. Si eso se cambiara
  alguna vez en 2.º, hay que cambiarlo aquí también.
- Lo nuevo de 4.º respecto a 2.º es el **par**: en 2.º se decía «más fuerza», y aquí se calcula
  `M = F·d`, con la conversión kg·cm → N·m y el porqué físico de que reducir multiplique el par
  (`P = M·ω`, la potencia no se crea).
- La unidad abre recogiendo 2.º («aprendiste a mover cosas, pero el que decidía eras tú») y cierra
  el círculo en la S4, donde se ve que **un servo es el diagrama de la S2 dentro de una caja de dos
  euros**.

---

## Dudas que dejo abiertas

1. **La lectura, ¿es una de las ocho sesiones o va aparte?** `CURRICULO.md` dice «7-8 sesiones **+
   lectura**» para 4.º, así que he asumido que va aparte y que las ocho son de contenido. Si va
   dentro, sobra una sesión de las cuatro pendientes.
2. **`analogRead`, ¿1023 o 1024?** He usado `V = L·5/1023` diciendo que hay 1024 valores posibles
   (del 0 al 1023) y que el 1023 corresponde a 5 V. Es el convenio más común y el que cuadra con
   los dos extremos, pero se ve escrito de las dos maneras y conviene que digas cuál quieres que
   usen, porque se lo van a encontrar.
3. **El número de la tarjeta.** He respetado que no toco `4eso/Tecnologia/index.html`, pero la
   unidad se llama «tema 4» en la ruta y en las migas porque así venía en el encargo. Si en 4.º
   pasa como en 2.º y la numeración de la web acaba desviándose de la del libro, esto habría que
   revisarlo antes de publicar.

---

## Qué miraría un humano, por orden

1. **Los cuatro vídeos**, enteros. Es lo único de la página que no he podido comprobar.
2. **Las rectas de calibración** de la S2 (620/280 y 90/870) y **los pares de los motores** de la S4.
3. **El bloque del 737 MAX** en la lectura: decidir si va o no para este grupo.
4. **El texto de los saberes B.1 a B.4**, para repartirlos por sesión.
5. Las cuatro escenas, tocándolas a mano: la de la S3 es la que más enseña moviendo un solo mando
   (la histéresis) y la que yo pondría en la pizarra digital.
