# Informe · 4.º de ESO · Tecnología · Unidad 2

**Diseño y fabricación: del material al producto** · CE2 (2.1, 2.2) · CE3 (3.1, 3.2) · CE5 (5.1)
Rama `c2`. Escrito el 18 de septiembre de 2026.

> Nota de sitio: las unidades hermanas dejan su informe en `generadores/INFORME-c4.md`,
> `INFORME-c5.md`, `INFORME-c6.md`. El encargo pedía literalmente `INFORME.md`, así que está en la
> raíz. Si prefieres la convención de las otras, muévelo a `generadores/INFORME-c2.md`.

---

## Lo entregado

| Fichero | Qué es |
|---|---|
| `4eso/Tecnologia/tema2/index.html` | La página, 200 KB, 8 sesiones (4 escritas, 4 pendientes) |
| `4eso/Tecnologia/tema2/lectura-tema2.pdf` | La lectura de aula: 30 párrafos numerados + 10 preguntas |
| `generadores/c2_build.py` | El generador de la página |
| `generadores/c2_escenas.py` | Escenas de las sesiones 1 y 2 |
| `generadores/c2_escenas2.py` | Escenas de las sesiones 3 y 4 |
| `generadores/c2_lectura.py` | El generador del PDF |
| `generadores/c2_verifica.py` | El verificador: **184 comprobaciones, 0 fallos** |
| `generadores/c2_capturas.py` | Saca foto de cada escena para mirarla (dos estados cada una) |
| `generadores/c2_fotos.py` | Busca, comprueba licencia y baja las fotos de Commons |
| `generadores/guion_c2.txt` | El guion de la voz |
| `audio/c2-fabricacion.mp3` + `_env_c2-fabricacion.json` | La voz (115,8 s) y su envolvente para el avatar |
| `img/c2-*.jpg` | Cinco fotos de Wikimedia Commons |

**No he tocado `4eso/Tecnologia/index.html`**, como pediste. Tampoco ningún fichero anterior: el
`git status` antes del commit solo tenía altas.

---

## Las cuatro sesiones

Mantuve tu propuesta de las cuatro; solo la afiné en dos sitios, y lo explico abajo.

| | Título | La escena calcula |
|---|---|---|
| **S1** | Cuatro veces veinticinco no son cien | La misma tapa acotada **en cadena** y **desde el borde**, con los mismos cuatro errores |
| **S2** | Dos piezas de ocho milímetros que no encajan | Juego máximo, juego mínimo y **tipo de ajuste** a partir de las cuatro desviaciones |
| **S3** | Lo que se pega no se repara | Lo que aguantan tornillos, remaches y pegado, con **los dos modos de fallo** |
| **S4** | La misma tapa, tres maneras de hacerla | Coste, tiempo de tus manos, tiempo de máquina y tolerancia de las tres técnicas |

Pendientes, con el título que propongo: **S5** Modelarlo en 3D (Tinkercad, es el 5.1) · **S6**
Organizar la fabricación (hoja de procesos) · **S7** Montar y ajustar · **S8** Contarlo y
defenderlo (el 3.2, el expediente y la exposición).

### Los tres proyectos, repartidos a propósito

Como pedías, nada en abstracto y sin que salga siempre el riego:

- **B · aviso de aula mal ventilada** → la **tapa de cuatro agujeros** de la S1, que vuelve en la
  S4 como la pieza que se fabrica. Es el hilo que cierra la unidad.
- **A · riego automático** → el **eje del depósito basculante** de la S2.
- **C · lámpara de estudio** → el **brazo unido a la base** de la S3.

### Los dos cambios que le hice a tu propuesta

1. **La S1 no termina en «acota desde una referencia»**, termina en *acotar es decir qué es lo que
   no se puede mover*. El error acumulado está calculado (peor caso `n·e`, típico `√n·e`), pero la
   conclusión que se lleva el alumno no es «la cadena es mala»: es que **la cadena y la referencia
   dicen cosas distintas** y hay que elegir. Si no, en la S4 no entienden por qué se redibuja.
2. **La S3 no va de listas de uniones**, va de **qué falla de verdad**. La familia
   fija/desmontable está (y el enlace con la U3 también), pero el corazón de la sesión es la cuenta
   del aplastamiento: el tornillo M3 aguanta 1700 N y la unión se rompe con 495 porque el PLA cede
   alrededor del agujero. Es el momento en que la sesión deja de ser vocabulario.

La cadena entre sesiones queda: plano → tolerancia → unión → fabricación, y **la S4 vuelve sobre
las tres anteriores**: la tapa es la de la S1, la tolerancia que compara es la del eje de la S2, y
el veredicto es que **ninguna de las tres técnicas del aula llega a esa cota**. Ese es el remate.

---

## Decisiones que conviene que sepas

**La escena de la S1 sortea, pero no miente.** Los cuatro errores de cada pieza salen de un
generador congruencial con semilla fija, se enseñan uno a uno en pantalla con dos decimales, y son
*exactamente* los que se usan en el dibujo. El verificador repite el mismo sorteo en Python y los
compara uno a uno. El botón «Otra pieza» es lo que hace ver que en cadena unas veces cuela y otras
no, que es la mitad del argumento.

**Las escenas dibujan a escala de verdad**, con dos excepciones rotuladas dentro del dibujo: la
*lupa* del cuarto agujero de la S1 (dice a cuántas veces la escala de arriba está) y el diagrama de
zonas de la S2 (está en micras, con su propia escala automática y la línea cero en su sitio). Las
regletas, la tapa, los agujeros y la junta a solape sí están a escala 1:k y lo he comprobado
midiendo sobre la captura.

**Miré las ocho capturas** (cada escena con los valores de partida y con los mandos en un extremo)
y corregí cinco colisiones de rótulo que no cazaba ningún test, más el hueco muerto de la S4: ahí
el `viewBox` se recalcula según lo alta que quede la tapa.

**Un fallo de verdad que cazó el verificador.** Escribí en la escena de la S4 que «el relleno casi
no cuenta, lo que manda es el espesor». Es **falso**, y la cuenta lo dice: con la tapa de 3 mm,
subir el relleno del 10 al 100 % pasa el coste de 0,31 a 0,53 €, y doblar el espesor solo lo lleva
a 0,39. Lo cambié por lo que sí es cierto y sí se puede comprobar en pantalla: **las tapas son 1,6
mm fijos** (el 83 % del plástico en la pieza de partida), así que **doblar el espesor no dobla el
material**, y el relleno actúa solo sobre el trozo de en medio, de modo que en pieza fina mueve
poco y en pieza gruesa manda. El verificador comprueba ahora las tres cosas.

---

## Lo que hay que mirar antes de llevarlo a clase

### 1 · Los vídeos: **nadie los ha visto enteros**

Comprobé título y canal uno a uno con la API oEmbed de YouTube el 18-sep-2026. Eso dice quién lo
firma y cómo se llama, **no si el vídeo es bueno ni si es apropiado**.

| Sesión | ID | Título | Canal |
|---|---|---|---|
| S1 | `NC7AdFJDx4M` | Acotación de una pieza · Tecnología ESO | Francisco Jose |
| S2 | `961O25IM1ZI` | Tolerancia dimensional: tipos de ajustes, cálculo y selección | Matías G. Ottini |
| S3 | `vcpl2baqin4` | ¿Cuál es mejor? Bulón, remache o soldadura | Tecnica X |
| S4 | `Tz168RtMZJU` | Aumenta la resistencia de tus piezas impresas en 3D | Control 3D |

El de la S2 va **por encima del nivel de 4.º** (entra en la notación ISO completa). Lo dejé porque
la parte del *porqué* de los tres ajustes está bien contada, y lo aviso en la nota del vídeo. Si al
verlo te parece que confunde más que ayuda, se quita sin tocar nada más.

### 2 · Las fotos: licencia por API **y** miradas una a una

Las cinco están abiertas y vistas; los pies describen lo que de verdad se ve, no lo que dice el
título del fichero.

| Fichero | Qué es | Licencia |
|---|---|---|
| `c2-plano-1914.jpg` | Plano de fabricación de General Electric, abril de **1911** (publicado en un libro de 1914) | sin restricciones de copyright conocidas |
| `c2-calibre.jpg` | Pie de rey con el nonio grabado **0,02 mm** | CC BY-SA 3.0 · ArtMechanic |
| `c2-pasa-nopasa.jpg` | Calibre tampón con **GO 29.94 / NO GO 29.97** grabados | CC BY-SA 3.0 · Glenn McKechnie |
| `c2-remaches.jpg` | Remaches ciegos antes y después de remachar | CC BY-SA 4.0 · Cjp24 |
| `c2-impresion3d.jpg` | Prusa i3 (RepRap) imprimiendo, con sus piezas amarillas impresas | CC BY 2.0 · John Abella |

Dos matices honestos:

- Del **pie de rey** solo afirmo lo que se lee en el cursor (`0,02 mm`) y lo que se ve (las dos
  parejas de bocas). La ficha de Commons dice que la foto muestra una lectura de 3,58 mm; **yo no
  soy capaz de leerla en la imagen**, así que no lo digo en el pie.
- Los **remaches** son de los de matrícula de coche (cuerpo de plástico). Lo digo en el pie. Sirven
  perfectamente para el argumento (para ponerlo hay que deformarlo), pero no son remaches
  estructurales.

Descartada `File:Go & No-Go gauge.jpg`: es buena foto, pero son calibres de recámara de **arma de
fuego** y no me pareció lo que quieres en una pantalla de clase. El tampón de agujeros enseña lo
mismo y además encaja con el eje de la S2.

### 3 · Los números que son **estimaciones nuestras**, no norma

Están rotulados como tales dentro de las escenas y en el texto, pero los junto aquí porque son lo
que más me gustaría que revisara alguien con taller:

- **Resistencia al aplastamiento** (S3), en N/mm²: PLA 55 · contrachapado 25 · DM 12 · metacrilato
  70 · aluminio 180. Redondeados para comparar órdenes de magnitud.
- **Adhesivo a cortadura** (S3), en N/mm²: 6 a 12 según material. Es el dato más flojo de todos:
  depende muchísimo del pegamento, de la preparación de la superficie y de si la junta trabaja a
  pelado. Ahí el número es orientativo de verdad.
- **Remache ciego Ø3,2 de aluminio**: 700 N. Valor de catálogo típico.
- **Tornillo M3 clase 4.8**: A = π·3²/4 = 7,07 mm² y τ = 0,6 · 400 = 240 N/mm² → **1697 N**. El
  0,6·Rm es el criterio habitual, no una norma que haya podido citar.
- **Velocidades de corte para taladro** (S4): madera 30-60, plásticos 30-50, aluminio 60-100, acero
  20-30 m/min. La fórmula `n = 1000·Vc/(π·D)` sí es la de siempre.
- **Sierra de marquetería** 80/t mm/min · **láser** 40/t mm/s · **impresora** 8 mm³/s ·
  contrachapado 3 €/m² por mm de espesor · PLA 20 €/kg, 1,24 g/cm³. Lo único de aquí que no es una
  estimación es la densidad del PLA.
- **Tolerancias alcanzables**: ±0,5 mm a mano, ±0,15 láser, ±0,3 impresora. Y la sangría del láser,
  ~0,2 mm.

Si tienes cifras mejores medidas en tu taller, cambiarlas es tocar una constante al principio de
`c2_escenas2.py`: todo lo demás se recalcula solo, y el verificador te dirá si algo se descuadra.

### 4 · Lo que decidí **no** poner

**La tabla de grados IT de la ISO 286.** La norma se menciona en un bloque de «solo para
entenderlo» —qué significa la letra y qué significa el número en `H7/g6`— pero **no doy ni un valor
numérico de la tabla**, porque no tengo la norma delante y no me parecía bien escribir de memoria
unas cifras que el alumno va a copiar en la libreta. Si quieres que entre, dime y la añado con la
fuente citada.

### 5 · Las fechas de la lectura

La lectura cuenta la historia de la intercambiabilidad. Las fechas van de mi conocimiento, no de un
documento que haya podido abrir aquí: **Blanc ~1785** y la carta de Jefferson · **Whitney 1801** y
el hallazgo posterior de que las piezas iban marcadas · **Whitworth 1841** · el metro de
platino-iridio **1889** · los bloques patrón de Johansson **hacia 1900** · el metro definido por la
luz **1983** · **Mars Climate Orbiter, 23-sep-1999**, ~125 M$. Todo eso es bastante sólido, pero es
lo que más agradecería que contrastaras antes de repartir el PDF, porque un alumno se lo va a
aprender.

En el párrafo del Mars Climate Orbiter he evitado a propósito hablar de *impulso*: digo «libras de
fuerza» frente a «newtons» y que son unas cuatro veces y media. Es lo correcto sin meterse en
libra-fuerza·segundo, que a esa edad despista.

---

## Cosas del entorno que te afectan a ti

1. **`generadores/voz.py` no está en el repo.** Vive en `/home/ubuntu/rt/generadores/voz.py`, fuera
   del repositorio, y los docstrings de `c4_build.py`, `c5_build.py` y `c6_build.py` lo citan como
   `generadores/voz.py`, que no existe. Generé el audio llamándolo por su ruta real. **No lo he
   copiado dentro** porque es utillaje compartido y no quería tocar nada que no fuera de esta
   unidad, pero merece la pena decidir si entra: ahora mismo nadie puede regenerar una voz
   siguiendo lo que dicen los ficheros.
2. **`c2_capturas.py` acepta una carpeta como argumento.** Por convenio escribe en
   `/tmp/c2-capturas`, como `c5_capturas.py`, pero aquí el entorno no me dejaba escribir en `/tmp`,
   así que le puse el argumento opcional. Con `python generadores/c2_capturas.py` a secas se
   comporta como sus hermanos.
3. **`ENCARGO.md` entra en el commit.** Ya estaba sin seguir cuando llegué, y pediste `git add -A`.
   Si no lo quieres en el repositorio, `git rm --cached ENCARGO.md`.
4. **Las capturas no se commitean**: las miré y borré la carpeta.

---

## Dudas que no he resuelto yo

1. **¿Ocho sesiones incluyen la lectura o son ocho más la lectura?** `CURRICULO.md` dice «8 +
   lectura». He hecho lo mismo que la unidad 4: ocho pestañas de sesión y la lectura aparte, en su
   recuadro. Si en realidad la lectura ocupa una de las ocho, sobra una sesión de las pendientes.
2. **El criterio 3.2 (defender el proyecto) apenas aparece en estas cuatro.** El 3.1 sí está, y
   fuerte, porque un plano acotado *es* comunicar lo que has diseñado —de hecho es la sesión 1
   entera—. Pero «defenderlo ante otra gente» lo he dejado entero para la S8. Si prefieres que se
   asome antes, el sitio natural es la tercera parte de la actividad 1, donde los grupos ya se
   intercambian los planos y se ponen pegas: se puede convertir en una defensa breve de dos minutos.
3. **La S4 tiene un solo bloque de «solo para entenderlo»** (las otras tres tienen dos). Es el de
   diseñar para fabricar, y es largo a propósito porque ahí está la idea de la sesión. Si te parece
   que queda desequilibrado, lo parto en dos.
4. **El vídeo de la S2**, ya comentado: por encima de nivel.
5. **La actividad 2, tercera parte, supone que hay pie de rey en el aula.** Si no lo hay, esa parte
   se cae y hay que reasignar sus 3 puntos. No sé qué tenéis.

---

## Cómo reproducirlo

```
/home/ubuntu/venv/bin/python generadores/c2_fotos.py baja      # las cinco fotos de Commons
/home/ubuntu/venv/bin/python /home/ubuntu/rt/generadores/voz.py generadores/guion_c2.txt c2-fabricacion
/home/ubuntu/venv/bin/python generadores/c2_lectura.py         # el PDF
/home/ubuntu/venv/bin/python generadores/c2_build.py           # la página
/home/ubuntu/venv/bin/python generadores/c2_verifica.py        # 184 comprobaciones
/home/ubuntu/venv/bin/python generadores/c2_capturas.py        # y luego, mirarlas
```
