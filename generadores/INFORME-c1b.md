# Informe · Tema 1 de 4.º de ESO · sesiones 5 a 8

**El proyecto tecnológico: detectar, idear, planificar.** Rama `c1b`.
La unidad queda con **8 sesiones escritas y 0 pendientes**.

> **Nombre del fichero.** El encargo pedía `INFORME.md` y aquí está. Pero las
> unidades hermanas siguen el patrón `generadores/INFORME-<clave>.md` (la
> primera mitad de esta misma unidad está en `generadores/INFORME-c1.md`). Si
> al recoger esto choca con los `INFORME.md` de las otras unidades que se
> están escribiendo en paralelo, **renómbralo a `generadores/INFORME-c1b.md`**:
> no lo enlaza nadie.
>
> Por lo mismo: el commit lleva dentro `ENCARGO.md`, porque el encargo pedía
> `git add -A`. Si cada unidad trae el suyo, quítalo al recoger.

---

## 1 · Qué he tocado

| Fichero | Qué es |
|---|---|
| `generadores/c1_build.py` | **Modificado.** Le he añadido el texto de las sesiones 5 a 8, el segundo test y las cuatro entradas de la barra. No he tocado ni una línea de las sesiones 1 a 4. |
| `generadores/c1_escenas3.py` | **Nuevo.** Escenas de S5 (el cuaderno como grafo de decisiones) y S6 (la fusión a tres bandas). |
| `generadores/c1_escenas4.py` | **Nuevo.** Escenas de S7 (el reloj del guion) y S8 (el plan contra lo que pasó, dos paneles). |
| `generadores/c1_fotos2.py` | **Nuevo.** Baja de Commons las cuatro fotos nuevas y guarda sus fichas. |
| `generadores/creditos_c1b.json` | **Nuevo.** Las fichas de licencia tal y como las devolvió la API. |
| `generadores/c1_capturas2.py` | **Nuevo.** Capturas de las escenas nuevas, incluidos los estados que sólo salen al pulsar. Los PNG van a `/tmp/c1b`, no al repositorio. |
| `generadores/c1_verifica.py` | **Ampliado.** De 117 comprobaciones a **304**. Pulsa todos los controles nuevos y **también los viejos**. |
| `img/c1-cuaderno.jpg` · `c1-scriptorium.jpg` · `c1-raton.jpg` · `c1-sidney.jpg` | **Nuevas.** Las cuatro fotos. |
| `4eso/Tecnologia/tema1/index.html` | Regenerado. 334 KB. |

**No he tocado `4eso/Tecnologia/index.html`**, como pedía el encargo. Tampoco
la lectura de aula ni nada de las sesiones 1 a 4.

Para rehacerlo:

```
/home/ubuntu/venv/bin/python generadores/c1_fotos2.py    # sólo si faltan las imágenes
/home/ubuntu/venv/bin/python generadores/c1_build.py
/home/ubuntu/venv/bin/python generadores/c1_verifica.py  # 304 comprobaciones, 0 fallos
/home/ubuntu/venv/bin/python generadores/c1_capturas2.py # para mirarlo con los ojos
```

---

## 2 · El hilo, y cómo entra cada sesión

La regla de la primera mitad la he mantenido entera: **ninguna sesión empieza
enunciando la fase**. Cada una empieza con el alumno haciéndolo mal y viéndolo.

| | Cómo entra | Qué falla delante del alumno | Y entonces aparece |
|---|---|---|---|
| S5 | «¿Por qué vuestro umbral es 38 y no 43?» | Nadie del grupo lo sabe, y han pasado **dos semanas** | El asiento del cuaderno, y las flechas de qué cuelga de qué |
| S6 | «Cada uno su párrafo, y lo juntamos» | Se pierde un párrafo **sin que nadie se entere** | Fusión a tres bandas, historial, fuente única de verdad |
| S7 | «Cuenta el proyecto en 60 segundos» | Al segundo 60 nadie sabe todavía qué hace el aparato | El orden que no es el cronológico, y el reloj del guion |
| S8 | «¿Ha salido bien el proyecto?» | «Sí, bueno, nos faltó tiempo»: no hay ni un número dentro | Desviación, camino crítico real y el factor de estimación |

Cada cierre deja **deberes concretos** que son el reto de la siguiente (medir
cuánto se tarda en juntar tres trozos, cronometrar el segundo en que se entiende
qué hace el aparato, traer las dos hojas del plan). El cierre de la S4, que ya
estaba escrito, engancha con la S5 sin que haya habido que tocarlo.

**El proyecto ya está decidido y se nota.** De la S5 en adelante todo aterriza
en el **riego automático** (`PROYECTOS.md`, bloque DECIDIDO): las doce decisiones
de la escena de la S5 son las de un grupo de riego, la memoria de la S6 es la
del riego, el guion de la S7 es el del riego y los cinco requisitos de la S8 son
los que la S2 dejó escritos. Las variantes B (ventilación) y C (lámpara) no las
he repetido aquí porque estas cuatro sesiones no dependen del sensor: el
cuaderno, el documento compartido, el guion de tres minutos y la desviación
sirven igual con cualquiera de los tres, y la primera mitad ya rota entre ellos.

---

## 3 · Las escenas: qué calculan, exactamente

Ninguna enseña un número escrito a mano. El verificador rehace cada cuenta en
Python **a partir de la definición**, no copiando el JavaScript, y la compara
con lo que se lee en pantalla.

**S5 · El cuaderno del proyecto.** Doce decisiones con fecha, autor, porqué y
`dep` (de qué cuelgan). Al tirar una abajo, la escena calcula el **cierre
transitivo** del grafo: qué decisiones se van con ella, cuántas sesiones cuesta
rehacerlas y cuántas se salvan. Al lado, la misma cuenta **sin cuaderno**, cuyo
modelo está declarado en el pie: sin flechas hay que volver a mirar *todo lo
decidido después*. El dibujo tampoco está colocado a mano: la columna de cada
nodo es su **nivel** (camino más largo desde una raíz), lo que garantiza que
toda flecha vaya de izquierda a derecha.

Dos cosas deliberadas:

- Una de las doce decisiones **viene sin porqué** («la estructura, contrachapado
  de 5 mm») y la escena la marca en rojo, en el grafo y en la tabla.
- Si se cae la decisión 6 (la bomba), de la que cuelga todo lo posterior, el
  cuaderno **no ahorra ni una sesión**, y la escena lo dice en vez de venderse
  de más. El verificador comprueba ese caso aparte.

**S6 · Trabajar a la vez.** Fusión a tres bandas de verdad, línea por línea:
si sólo uno tocó la línea entra su versión, si la tocaron los dos y coinciden da
igual, y si no coinciden es un **choque**. Con esa fusión compara tres maneras
de trabajar y cuenta cinco cosas: minutos de trabajo perdidos, líneas que chocan,
**avisos que da el programa**, minutos de arreglarlo a mano y ficheros que quedan.

El número que importa es el tercero. Por correo se pierden **22 minutos de Ana
y el programa da 0 avisos**; en línea se pierden 0 minutos y el aviso es 1. Los
minutos de arreglo salen de dos constantes declaradas en el pie (0,75 min por
línea comparada, 2 min por choque hablado).

**S7 · Contarlo en tres minutos.** Seis bloques con sus segundos y con las
palabras escritas. Calcula lo que cabe (segundos × velocidad ÷ 60), lo que se
tardaría de verdad con lo escrito, y el **segundo exacto en que acaba cada
bloque** en el orden que tenga puesto. De ahí sale la **prueba del minuto uno**:

- con «el orden que sale solo» (contar la historia desde el principio), el
  bloque que dice qué hace el aparato acaba en el segundo **165** y no la pasa;
- con «el orden que funciona», en el **55**, y la pasa.

Y el dato que sorprende: a 130 palabras por minuto, en tres minutos caben **390
palabras**, y el guion de ejemplo trae 640. El arranque del aparato se puede
cobrar como tiempo muerto y se ve lo que se come.

**S8 · Del plan a lo que pasó.** Dos paneles.

*El calendario* corre el método del camino crítico **dos veces**, con el plan y
con lo medido. Las doce tareas son exactamente las de la escena de la S4, con la
espera del material como parámetro. Resultado con los números de partida:

| | Previsto | Real |
|---|---|---|
| Duración | 21 sesiones | **28** |
| Trabajo sumado | 26 | **35** |
| Espera del material | 5 | 7 |
| Camino crítico | 1, 2, 3, 5, 8, 9, 10, 11, 12 | **1, 2, 3, 4, 6, 7, 9, 11, 12** |

**Los dos caminos críticos no son el mismo**, y eso es lo que hace la sesión:
salen del camino crítico la tarea 5 (pedir el material), la 8 (fabricar la
estructura) y la 10 (medir el impacto), y entran la 4 (dibujar), la 6 (Tinkercad)
y la 7 (programar). Lo que se protegió en septiembre no era el peligro. El
factor de estimación (35 ÷ 26 = **1,35**) es el número que se llevan para el
proyecto siguiente.

*Los requisitos* corre los cinco de la S2 contra lo medido, con las medidas
tecleables. Salen **2 de 5**, y la escena recuerda que el de los ocho riegos ya
se sabía imposible desde la sesión 2 (224 puntos de humedad perdidos ÷ 22 por
riego = 10,2 riegos, pase lo que pase): **ahí no falló el aparato, falló el
requisito**, y eso también va en la memoria.

---

## 4 · Fotos: licencia por la API, y miradas una a una

Bajadas con `generadores/c1_fotos2.py`, que lee la licencia de la API de
Commons. Las fichas literales están en `creditos_c1b.json`. **Las he abierto y
mirado las cuatro antes de escribir su pie**, y he corregido tres pies después
de mirarlas.

| Fichero | Original | Autor | Licencia | Qué se ve, y por qué está |
|---|---|---|---|---|
| `c1-cuaderno.jpg` | `File:Otto Hahn's notebook 1938 - Deutsches Museum - Munich.jpg` | J Brew | CC BY-SA 2.0 | Cuaderno abierto sobre una mesa: a la izquierda texto en alemán, a la derecha una columna de medidas con **las fechas de diciembre escritas en el margen** (17.XII, 18.XII, 19.XII…). Es exactamente lo que la sesión pide: un registro fechado el día. |
| `c1-scriptorium.jpg` | `File:James Murray in a scriptorium.jpg` | Autor desconocido | Dominio público | Murray **de pie**, leyendo papeletas, con tres paredes de estanterías llenas de fajos del suelo al techo. Es muy vertical (2326×2974): va limitada a 470 px. |
| `c1-raton.jpg` | `File:Replica of prototype Engelbart mouse, circa 1964, Computer History Museum.jpg` | The wub | CC BY-SA 4.0 | Caja de madera con **un solo botón rojo**, cable trenzado y conector, sobre peana de museo. Se ven las ranuras de las ruedas en el costado. Va limitada a 560 px. |
| `c1-sidney.jpg` | `File:Sydney Opera House - construction - phase 2 1966.jpg` | Robeyclark | CC BY-SA 3.0 | La ópera a medio construir vista desde el agua, con grúas encima y unas conchas ya forradas y otras con las costillas al aire. **Es pequeña (600×600)** y algo blanda; va limitada a 430 px. |

**Correcciones que hice después de mirarlas** (y que es justo el motivo de
mirarlas):

1. El alt del cuaderno decía «dentro de una vitrina de museo». **No hay vitrina
   visible**: está sobre una mesa de madera. Corregido, y aprovechado para citar
   las fechas del margen, que sí se leen.
2. El alt del Scriptorium decía «sentado escribiendo ante un atril». **Murray
   está de pie**, leyendo. Y lo que se ve no son casilleros ordenados sino
   fajos apilados; el pie lo dice ahora así y deja el dato de las 1.029 casillas
   como dato, no como descripción de la foto.
3. Al pie del ratón le he añadido lo que se lee en el cartel de al lado —que
   sólo cabía un botón—, porque es visible en la foto.

⚠️ **Una duda sobre el ratón que conviene que mires.** Commons lo titula
*Replica of prototype Engelbart mouse*, pero el cartel que se ve al fondo de la
propia foto dice «Gift of SRI International, 102633685», que suena a pieza
original y no a réplica. He puesto en el pie lo que dice Commons («Commons lo
cataloga como réplica») para no afirmar lo que no sé. Si te importa la
distinción, hay que preguntárselo al museo.

---

## 5 · Vídeos: título y canal comprobados, **nadie se los ha visto enteros**

Comprobados por oEmbed (`generadores/oembed.py`) el 18-sep-2026. **No los he
visto.** Sé cómo se llaman y quién los firma, y nada más. Antes de ponerlos
delante de una clase hay que verlos enteros; el de la S7, además, hay que verlo
**con el cronómetro**, que es lo que se le pide al alumno.

| Sesión | ID | Título (el que devuelve YouTube) | Canal |
|---|---|---|---|
| S6 | `Odwo6i52skU` | Cómo usar el historial de versiones en Google Docs | Javier Fernández |
| S7 | `DZY3HGwBBVg` | Mi Tesis en 3 minutos - Lucila García | UNLitoral |

**S5 y S8 se quedan sin vídeo a propósito**, igual que la S2 de la primera
mitad. Busqué los dos:

- Para el cuaderno de proyecto, lo que hay en español son guías universitarias
  de cuaderno de laboratorio en PDF (buenas, pero no son vídeo ni son para 15
  años) y vídeos de papelería.
- Para la desviación y el sesgo de planificación, lo que hay son charlas de
  gestión de proyectos para empresa. Ninguno aporta nada por encima de lo que
  ya hace la escena, y prefiero dejarlo vacío antes que rellenar.

⚠️ El de la S6 es de Google Docs. Si el centro usa Nextcloud o Moodle, el vídeo
sigue valiendo para entender qué es un historial, pero el menú se llama distinto.
Está dicho en la nota del propio vídeo.

---

## 6 · Datos comprobados, y lo que he dejado fuera

Contrastado el 18-sep-2026 contra Wikipedia, salvo donde se dice otra cosa.

**Comprobado y usado:**

- **Otto Hahn**: experimento decisivo la noche del **16 al 17 de diciembre de
  1938** con Fritz Strassmann; carta a Lise Meitner del **19 de diciembre**;
  Meitner y Frisch dan la interpretación en **enero de 1939**; **Nobel de
  Química de 1944 sólo para Hahn**. El cuaderno está en el Deutsches Museum
  (lo dice la propia ficha de Commons).
- **Oxford English Dictionary**: adoptado por la Philological Society el 7 de
  enero de **1858**; **más de 800 voluntarios**; **2.500.000 papeletas en
  1880**; **1.029 casillas** en el Scriptorium; **mil papeletas al día**;
  primer fascículo el 1 de febrero de **1884**, el 125.º y último el 19 de abril
  de **1928**.
- **La palabra perdida (*bondmaid*)**: sus papeletas se cayeron detrás de unos
  libros y la palabra no salió en el tomo, publicado en 1888. ⚠️ Esto lo he
  contrastado en **dos fuentes secundarias**, no en la propia OED. Es la parte
  menos sólida de la sesión 6, aunque es de las más citadas. En el texto no
  doy el año del tomo ni el nombre de la palabra en inglés para no colgarme de
  un dato que no he visto en fuente primaria.
- **La demostración de Engelbart**: **9 de diciembre de 1968**, Fall Joint
  Computer Conference, San Francisco; **90 minutos**; **unas 1.000 personas**;
  ratón, ventanas, hipertexto, videoconferencia y **editor colaborativo en
  tiempo real**; **dos enlaces de microondas** desde Menlo Park; pantalla de
  **6,7 m**.
- **Ópera de Sídney**: concurso ganado por **Jørn Utzon** en **1957**;
  presupuesto original **7 millones** de dólares australianos y fecha prevista
  el **26 de enero de 1963**; inauguración el **20 de octubre de 1973**; coste
  final **102 millones**. La foto es de 1966.
- **Falacia de la planificación**: el término es de **Kahneman y Tversky,
  1979**. El estudio de **Buehler, Griffin y Ross (1994)**: **37 estudiantes**
  dijeron **33,9 días** y tardaron **55,5**, y sólo el **30 %** acabó dentro del
  plazo que ellos mismos se habían puesto.

**Dejado fuera por no poder comprobarlo:**

- **La velocidad al hablar en español.** Hay estudios de tasa silábica, pero no
  he podido abrir el original para citar la cifra, y las que circulan por la web
  son de blogs. Así que en la escena la velocidad es **un campo de entrada con
  130 de partida, rotulado como criterio nuestro**, y la actividad de la S7
  consiste en **medir la propia con un cronómetro**. Me parece mejor pedagogía
  que citar un número, pero si tienes una fuente buena, se pone en el pie.
- **Cuánto más se tarda en el primer ensayo en voz alta.** Lo digo en el texto
  sin número, como criterio, y pidiendo que lo midan ellos.

---

## 7 · Fronteras con las otras unidades

He respetado las tres que marcaba el encargo, y lo he hecho **explícito dentro
de la página** para que no se solape en clase. En la S7 hay un bloque «solo para
entenderlo» que dice literalmente:

> Lo de hoy es **cómo se cuenta**: el guion, el reloj, el orden y el ensayo.
> **Defender una pieza que habéis fabricado** —por qué ese material, por qué ese
> corte— es otra cosa y llega en el tema 2. Y **enseñárselo a alguien de fuera
> del centro**, que cambia el vocabulario entero, es del tema 9.

Y además:

- **La S5 es el registro, no la memoria.** Hay un bloque PARA LA LIBRETA entero
  dedicado a separar las dos cosas, y la memoria final no se explica aquí: sólo
  se dice que se escribirá *con el cuaderno delante*.
- **No hay impacto ambiental en ninguna de las cuatro sesiones.** En la S8 la
  tarea 10 del Gantt se llama «Medir el impacto» —viene de la escena de la S4,
  que no he tocado—, pero no se explica nada de eso: sólo se usa como una tarea
  más del calendario.

⚠️ **Dos sitios donde creo que puedo pisarme con otra unidad, y no lo puedo
comprobar porque sólo veo la mía:**

1. **El historial de versiones y los documentos compartidos (S6)** encajan
   también en la unidad 6 (*Programación, IoT e IA*), que lleva el criterio 5.1
   igual que esta. Yo lo he tratado como herramienta de trabajo en grupo —fuente
   única de verdad, permisos, recuperar lo borrado— y **no toco nada de control
   de versiones de código ni de repositorios**. Si la 6 lo cuenta también, lo
   que sobra es lo mío, que es más básico.
2. **El factor de estimación (S8)** es material que también podría reclamar la
   unidad 9 (*proyectos de servicio*) al cerrar el curso. Aquí cierra **esta**
   unidad, que es la que puso el plan.

---

## 8 · Cosas que he visto en la primera mitad y **no he tocado**

Ninguna es un error de bulto. Las dejo apuntadas, como pedía el encargo.

1. **La lectura de aula está enlazada dos veces.** El cierre de la S1 tiene un
   bloque «Lectura del tema» con su enlace a mano, y además `unidad_base.py`
   añade solo la caja «LECTURA DE AULA» al final de la página en cuanto
   encuentra el PDF. No molesta, pero es redundante.
2. **Un rótulo de la matriz de la S3 está a medias.** En `c1_escenas2.py`, el
   criterio «Cumple el encargo» tiene de ayuda `sensor + actuador programados;
   1 = no lleva`, y le falta el `5 = ` del principio que sí llevan los otros
   cuatro. Se ve en la cabecera de la tabla.
3. **La producción del Segway** se dice parada «en junio de 2020». Lo que consta
   es que **el anuncio** fue en junio de 2020; la última unidad salió algo
   después. Es matizable, no falso.
4. En varios sitios del texto de las sesiones 1 a 4 conviven letras acentuadas
   literales (`renglón`, `puntúa`, `mustió`) con las mismas escritas como
   entidad HTML. Como la página va en UTF-8 declarado, se ve bien; es sólo
   inconsistencia de estilo, y yo he seguido la misma mezcla.

---

## 9 · Decisiones que conviene que mires

1. **El test de la S8 tiene 12 preguntas, no 10.** Cubre la unidad entera:
   **una por cada sesión de la 1 a la 4** (problema frente a solución, las
   cuatro piezas del requisito, los pesos de la matriz, la holgura) y **dos por
   cada una de la 5 a la 8**. Por eso me he salido de las diez de la S4. Usa el identificador **`c1b`**,
   como pedía el encargo. El verificador comprueba expresamente que **los dos
   tests no comparten ni un nombre de grupo de radios** y que **ningún `id` se
   repite en la página**, que era el riesgo.

2. **Los datos de la escena de la S8 son de ejemplo, y eso cambia cómo se da la
   sesión.** Esta sesión se da **dos veces**: hoy, para aprender a cerrar un
   proyecto, y otra vez en junio con los números de verdad. Lo digo en el reto
   de la sesión. Si prefieres que se dé sólo en junio, el texto aguanta, pero
   entonces la unidad se queda con siete sesiones en el primer trimestre.

3. **Las duraciones reales están elegidas para que el camino crítico cambie.**
   No es casualidad: es la lección de la sesión, y sin ella la escena sólo diría
   «tardasteis más». Lo he elegido para que la tarea que se lleva el retraso sea
   **programar** (de 3 a 7 sesiones), que es lo que pasa de verdad en un aula la
   primera vez que se toca Arduino. Es criterio mío y es discutible.

4. **Las puntuaciones de minutos de la S6 son inventadas** (12, 4, 6 para Ana;
   8, 6, 9 para Beto) y está dicho en el pie. Lo que no es inventado es la
   fusión: eso se calcula.

5. **El coste de arreglar a mano** en la S6 sale de dos constantes nuestras
   (0,75 min por línea comparada y 2 min por choque hablado). Están declaradas
   en el pie de la escena. Si te parecen optimistas, se cambian en `MINCOMPARA`
   y `MINHABLAR`.

6. **La actividad de la S6 pide montar una carpeta compartida** con los tres
   como editores. Eso depende de que el centro tenga cuentas para el alumnado.
   Si no las hay, la alternativa es hacerlo con una sola cuenta del grupo y
   perder la mitad de la gracia (no se ve quién hizo qué en el historial). Lo
   he escrito sin nombrar marca, pero el vídeo sí es de Google Docs.

7. **La actividad de la S7 necesita cronómetro y que los grupos se escuchen
   entre ellos.** En un aula de 30 eso son 10 grupos y no da tiempo a que todos
   presenten. La actividad está escrita para que **cada grupo presente sólo al
   de al lado**, en paralelo, y es ruidoso a propósito. Si prefieres que
   presenten a toda la clase, hace falta otra sesión.

---

## 10 · Cosas que sé que quedan flojas

- **La escena de la S5 tiene un grafo de doce nodos.** En un móvil el SVG se
  escala y los rótulos de dentro de las cajas quedan pequeños. La tabla de
  debajo dice lo mismo con todas las letras, así que la escena no se pierde,
  pero el dibujo en pantalla pequeña es decorativo más que legible.
- **La escena de la S6 tiene seis casillas y un desplegable.** Es la más
  «formulario» de las cuatro y la que menos se disfruta mirando. La probé sin
  las casillas —sólo los tres modos— y entonces el alumno no puede quitar el
  choque y ver que desaparece, que es lo único que demuestra que la fusión se
  calcula de verdad. Me he quedado con las casillas.
- **La prueba del minuto uno depende de que el guion tenga un bloque marcado
  como «el que dice qué hace el aparato».** En la escena está marcado; en el
  guion de un grupo, hay que decidirlo, y es justo la discusión que quiero que
  tengan. Pero en la actividad puede quedar difuso.
- **La S8 es larga**: dos paneles de escena, tabla de calendario, tabla de
  requisitos y un test de doce preguntas en 10 minutos de cierre. El test se
  puede mandar para casa sin perder nada: se corrige solo en el navegador.
- **La primera mitad no sabe que existe la segunda.** El pie de la escena de la
  S2 ya promete que «en la sesión 8 lo sustituiremos por los datos de vuestro
  prototipo», y la S8 lo cumple; pero el cierre de la S4 habla de «la sesión en
  la que se decide si la memoria la escribís a lo largo del curso o la noche de
  antes», y mi S5 va de **cuaderno**, no de memoria. Encaja, pero el cierre de
  la S4 apunta un poco más alto de lo que la S5 entrega. No lo he tocado.

---

## 11 · Comprobado

- **`generadores/c1_verifica.py`: 304 comprobaciones, 0 fallos.** Abre la página
  en Chromium, pulsa **los ocho** botones de sesión, comprueba que cada una
  tiene sus cuatro bloques y su práctica repartida en cinco trozos de nota, y
  vuelve a pasar **todas las pruebas viejas** de las escenas 1 a 4 sin tocarlas.
  De las nuevas:
  - **S5**: las doce filas, la decisión sin porqué, las 24 cajas y las 17
    flechas del grafo, y **cuatro caídas distintas** contrastando el cierre
    transitivo y el coste contra un cálculo hecho aparte en Python (con una
    pila, no con la relajación del JavaScript). Incluido el caso en el que el
    cuaderno no ahorra nada.
  - **S6**: los cinco contadores en los **tres modos** y con los dos «últimos
    que guardan», contra una fusión rehecha en Python; que por correo se pierden
    22 minutos con 0 avisos; y que al quitar el cambio del presupuesto de Ana el
    choque desaparece.
  - **S7**: los dos presets, el segundo exacto en que acaba el bloque clave
    (165 y 55), las palabras que caben a dos velocidades, el arranque cobrado, y
    **subir el bloque cuatro puestos** y que la prueba del minuto uno pase.
  - **S8**: las doce filas con previsto, real, desvío y las dos criticidades;
    las cinco cajas; los dos caminos críticos y **qué entra y qué sale**; tocar
    una duración y la espera del material; y los cinco requisitos con su
    veredicto y su desviación, tecleando encima de una medida.
  - **Los dos tests**: que el de la unidad tiene doce, que da 12 de 12 y 11 de
    12 fallando una a propósito, que **no comparte nombres de radios** con el de
    la S4, que contestar uno no toca el otro, y que **ningún `id` se repite**.
  - Que **ninguna clase CSS empieza por `test-`**. Los prefijos nuevos son
    `p5-`, `p6-`, `p7-` y `p8-`.
- **Miradas las cuatro escenas en captura** (`c1_capturas2.py`), en claro y en
  oscuro, y arreglados cinco defectos que el verificador no podía ver:
  1. En el grafo de la S5, las flechas se pintaban de rojo también **hacia** la
     decisión caída, dando a entender que las de antes estaban afectadas. Ahora
     sólo se pinta el camino por el que se propaga.
  2. En la S5 y en la S6, los rellenos de color eran semitransparentes y **las
     flechas se veían por debajo, cruzando el texto de las cajas**. Llevan un
     rectángulo opaco debajo.
  3. En la S7, la línea del minuto uno cruzaba el rótulo de la segunda barra y
     se leía «de|verdad». Ahora va en dos trozos, uno por barra.
  4. En la S8, «fin del trimestre» se comía los números de sesión del 24 y del
     26, y al ponerlo a la derecha se salía del dibujo. Va a la izquierda de la
     línea y en su propio renglón.
  5. En la tabla de requisitos, el desvío se pintaba de verde o rojo **por el
     signo**, y eso engañaba: un −22 % de humedad es malo y un +40 % de
     distancia al agua es bueno. Ahora el color va por CUMPLE / NO CUMPLE.
- **Comprobado en modo oscuro**: había tres textos en blanco fijo (`#fff`) que
  en oscuro caían sobre colores claros. Van con `var(--surface)` o `var(--ink)`.
- **La página no lleva ningún byte NUL** y ningún `id` duplicado.
