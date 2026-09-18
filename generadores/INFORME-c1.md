# Informe · Tema 1 de 4.º de ESO · El proyecto tecnológico: detectar, idear, planificar

Rama `c1`. Sesiones **1 a 4 de 8** escritas; las otras cuatro quedan en la barra
con su título y el botón desactivado.

> Nota de nombre: el encargo pedía `INFORME.md`. Lo he dejado como
> `generadores/INFORME-c1.md` para no pisar los de las unidades 4, 5 y 6, que ya
> siguen ese patrón en la misma carpeta.

---

## 1 · Qué hay

| Fichero | Qué es |
|---|---|
| `4eso/Tecnologia/tema1/index.html` | La unidad. 174 KB, generada, nunca editada a mano. |
| `4eso/Tecnologia/tema1/lectura-tema1.pdf` | La lectura de aula, 4 páginas, 30 párrafos numerados y 10 preguntas. |
| `generadores/c1_build.py` | El texto de las cuatro sesiones y el montaje de la página. |
| `generadores/c1_escenas.py` | Escenas de S1 (la cuenta del problema) y S2 (el requisito ejecutado). |
| `generadores/c1_escenas2.py` | Escenas de S3 (matriz de decisión) y S4 (Gantt con camino crítico). |
| `generadores/c1_lectura.py` | La lectura en PDF. Comprueba sola que son 30 y 10. |
| `generadores/c1_fotos.py` | Baja las cuatro fotos de Commons y guarda sus fichas. |
| `generadores/creditos_c1.json` | Las fichas de licencia tal y como las devolvió la API. |
| `generadores/c1_verifica.py` | El verificador: **117 comprobaciones, 0 fallos**. |
| `generadores/c1_capturas.py` · `c1_mirada.py` | Capturas para mirar el dibujo con los ojos. Dejan los PNG en `/tmp`, no en el repo. |
| `generadores/guion_c1.txt` · `audio/c1-proyecto.mp3` · `_env_c1-proyecto.json` | La voz de presentación (100 s) y su envolvente para el avatar. |
| `generadores/voz.py` | Copiado del repositorio principal, donde estaba sin versionar. Hace falta para regenerar el audio. |
| `img/c1-*.jpg` | Las cuatro fotos. |

No he tocado `4eso/Tecnologia/index.html`, como pedía el encargo.

Para rehacerlo todo desde cero:

```
/home/ubuntu/venv/bin/python generadores/c1_fotos.py      # sólo si faltan las imágenes
/home/ubuntu/venv/bin/python generadores/voz.py generadores/guion_c1.txt c1-proyecto
/home/ubuntu/venv/bin/python generadores/c1_lectura.py
/home/ubuntu/venv/bin/python generadores/c1_build.py
/home/ubuntu/venv/bin/python generadores/c1_verifica.py
```

---

## 2 · El hilo, y por qué este y no el de la propuesta

La propuesta del encargo (problema → requisitos → alternativas → planificar) me
parece la correcta y la he mantenido entera. Lo que he cambiado es **cómo entra
cada sesión**: ninguna empieza enunciando la fase. Cada una empieza con el
alumno haciéndolo mal y viéndolo.

| | Cómo entra | Qué falla delante del alumno | Y entonces aparece |
|---|---|---|---|
| S1 | «Escribid qué queréis construir» | Nadie puede decir a quién le hace falta | Problema ≠ solución, y la cuenta que lo mide |
| S2 | «Pasadle vuestro encargo al grupo de al lado» | Los dos lo cumplen y entregan cosas distintas | Las cuatro piezas de un requisito |
| S3 | «Cinco maneras, sin juzgar ninguna» | Cinco encima de la mesa y ninguna manera de elegir | Divergir/converger y la matriz |
| S4 | «¿Cuántas sesiones creéis?» (lo escriben en S3) | Dijeron 10 y son 21 | Dependencias, espera, holgura, camino crítico |

Los tres proyectos de `PROYECTOS.md` aparecen repartidos y no siempre el riego:

- **S1**: los tres casos de la escena son A (riego), B (ventilación) y C (lámpara),
  y la enseñanza del bloque «solo para entenderlo» sale de comparar **B con C**.
- **S2**: el ensayo de 14 días es el del riego (A), porque es el que da una serie
  de datos con la que se puede correr un requisito. El requisito de ejemplo del
  cierre es de la **lámpara** (lux), y el de seguridad habla de las tres.
- **S3**: alternativas del riego, incluida una **sin electrónica**.
- **S4**: el Gantt vale para los tres.

---

## 3 · Las escenas: qué calculan, exactamente

Ninguna enseña un número escrito a mano. El verificador rehace cada cuenta en
Python, **escrita otra vez a partir de la definición**, y la compara con lo que
se lee en pantalla.

**S1 · La cuenta del problema.** `afectados × veces/semana × coste × semanas`,
con selector de unidad (min, h, L, €) y conversiones declaradas en el bloque
PARA LA LIBRETA. Calcula además:
- el acumulado semana a semana, dibujado, con la línea de «solo a ti» al lado;
- la **semana en que el problema se come una referencia** (ceil(ref / coste
  semanal)): riego → semana 18, aula → semana 1, lámpara → semana 3;
- las equivalencias (horas, sesiones, jornadas, kWh, garrafas, bañeras).

Con el caso «quiero hacer un robot», tres de las cuatro casillas no se pueden
rellenar y **la escena se niega a dar un número**, dice cuáles faltan y no
dibuja nada. Es el punto de la sesión.

**S2 · El requisito, ejecutado.** Simula 14 días del prototipo (56 lecturas,
una cada 6 h): parte de 62 %, resta la evaporación y riega al bajar del umbral,
subiendo 22 puntos y gastando 0,18 L. De esa serie mide humedad mínima, media,
agua, número de riegos y horas por debajo del 40 %. Cada requisito del alumno se
convierte en una comparación y **se corre contra esos datos**: PASA / NO PASA
con el valor medido al lado. Los requisitos mal escritos no se pueden correr y
la escena dice **qué pieza les falta**.

Dos cosas que salen de los números y que están explotadas en el texto:

- Subir el umbral sube la humedad mínima y sube el gasto. El compromiso es real
  y se ve cambiando un campo.
- **«8 riegos o menos en 14 días» es imposible con cualquier umbral**, y la
  razón se calcula a mano: 56 × 4 = 224 puntos perdidos, 22 por riego → 10,2
  riegos. El umbral decide cuándo se riega, no cuántas veces. Está comprobado en
  el verificador para los 41 umbrales de 20 a 60.

**S3 · Matriz de decisión.** Suma ponderada de 4 alternativas × 5 criterios, con
pesos y notas editables. Lo que la hace algo más que una tabla:
- calcula el **margen** entre la primera y la segunda y avisa cuando es menor
  del 5 % del máximo (con los pesos de clase lo es: 2 puntos de 85);
- hace un **análisis de sensibilidad** por fuerza bruta: para cada criterio,
  busca el peso más cercano que cambiaría la elegida, y lo dice. Con los pesos de
  partida hay dos criterios que la vuelcan;
- el botón «todos los pesos a 1» **cambia la ganadora** (gana el gotero), que es
  la demostración de que lo que hay que justificar son los pesos.

**S4 · Gantt con camino crítico.** Doce tareas, dependencias y una **espera de 5
sesiones** por el material (el pedido). Hace las dos pasadas del método:
adelante (ES/EF), atrás (LS/LF), holgura y camino crítico. Plan de partida: el
trabajo suma **26 sesiones**, el proyecto dura **21** y el trimestre tiene **24**.
Al alargar una tarea recalcula todo y dice **qué tareas se ha llevado por
delante** comparando con el plan inicial:

- tarea 6 (holgura 2) + 2 sesiones → no se mueve nada;
- tarea 6 + 3 → el proyecto pasa a 22 (retraso de 3 en la tarea, de 1 en el
  proyecto);
- tarea 8 (crítica) + 1 → arrastra a 4 tareas y el proyecto a 22.

---

## 4 · Fotos: licencia consultada por la API y miradas una a una

Las cuatro se han bajado con `generadores/c1_fotos.py`, que lee la licencia de
la API de Commons (no de memoria), y **las he abierto y mirado** antes de
escribir su pie. Las fichas literales están en `creditos_c1.json`.

| Fichero | Original | Autor | Licencia | Qué se ve, y por qué está |
|---|---|---|---|---|
| `c1-segway.jpg` | `File:Segway PT (2006).jpg` | Richard from DC, US | CC BY 2.0 | Tres personas con casco en Segway en una plaza de Washington, con coches de policía al fondo. Es una ruta turística: enseña **dónde acabó** el aparato que iba a cambiar las ciudades. |
| `c1-millennium.jpg` | `File:London Millennium Bridge from Saint Paul's.jpg` | Jan Kameníček | CC BY-SA 3.0 | Cenital del puente lleno de peatones. Se ve exactamente la carga de la que habla la sesión: gente andando. Es muy vertical (1536×2304), así que va limitada a 430 px de ancho. |
| `c1-goteo.jpg` | `File:Drip emitter.jpg` | Alan.ca | Dominio público | Primer plano de un gotero con la gota colgando, sobre arcilla expandida y lana de roca. Es la alternativa sin electrónica que obliga a la matriz a ser honesta. El pie dice que es un cultivo hidropónico, que es lo que de verdad se ve. |
| `c1-gantt.jpg` | `File:Henry Gantt.jpg` | Autor desconocido | Dominio público | Retrato. Es pequeño (282×332) y granulado; va limitado a 340 px. |

---

## 5 · Vídeos: título y canal comprobados, **nadie se los ha visto enteros**

Comprobados por oEmbed (`generadores/oembed.py`) el 18-sep-2026. **No los he
visto**: sé cómo se llaman y quién los firma, y nada más. Antes de ponerlos
delante de una clase hay que verlos.

| Sesión | ID | Título (el que devuelve YouTube) | Canal |
|---|---|---|---|
| S1 | `1R9eg3MCfWk` | ¿Qué es y cómo hacer una «OBSERVACIÓN DE USUARIOS»? Paso a paso, incluye ejemplos. Temp 3 - Ep 42 | Design Thinking 24 7 by Jorge Huertas |
| S3 | `Kr2QQ_q7Axc` | Matriz Pugh: técnica de selección de alternativas | Tecnológico de Monterrey \| Innovación Educativa |
| S4 | `kbgiwFNxsG4` | Tutorial Ganttproject - 02/04 Crear tareas y agruparlas. Dependencias entre tareas. Camino crítico. | VideoTutoriales Education |

**S2 se ha quedado sin vídeo a propósito.** Busqué y lo que hay en español sobre
requisitos es ingeniería de software para universidad, o charlas de objetivos
SMART de empresa. Ninguno aporta nada a un alumno de 15 años por encima de lo
que ya hace la escena, y prefiero dejarlo vacío antes que rellenar.

---

## 6 · Datos históricos: qué está comprobado y qué he dejado fuera

Todo contrastado contra Wikipedia el 18-sep-2026.

**Comprobado y usado:**

- **Segway**: presentado el 3-dic-2001 (Dean Kamen); Doerr dijo «más importante
  que internet» y Jobs «tan grande como el PC»; 5.000 $; **140.000 unidades en
  toda su vida comercial**; producción parada en junio de 2020.
- **Puente del Milenio**: abre el 10-jun-2000, 90.000 personas ese día y hasta
  2.000 a la vez; oscilación lateral de hasta 70 mm; cierra el 12-jun-2000;
  reabre el 22-feb-2002; 18,2 M£ de construcción y 5 M£ de reparación;
  37 amortiguadores viscosos y 52 de masa sintonizada; el fenómeno es la
  **excitación lateral sincronizada**.
- **Aeropuerto de Denver**: apertura prevista el 29-oct-1993, real el
  28-feb-1995, 16 meses tarde; el proyecto costó unos 4.800 M$, cerca de
  2.000 M$ por encima de lo previsto; la demostración a la prensa de abril de
  1994 esparció el equipaje; el sistema se apagó en septiembre de 2005.
- **Gantt y Adamiecki**: Gantt (1861-1919) publicó en 1910 y 1915; Adamiecki
  creó el *harmonograma* en 1896 y publicó en *Przegląd Techniczny* en 1909, en
  polaco. Wikipedia lo dice con todas las letras: se quedó con el nombre de
  Gantt porque el de Gantt estaba en inglés.
- **Matriz de Pugh**: Stuart Pugh, 1981.

**Dejado fuera por no poder comprobarlo, aunque circule mucho:**

- Que Kamen predijera vender **10.000 Segway a la semana**. Se cita en todas
  partes pero remite a un libro, no a una fuente que haya podido ver. No
  aparece ni en la página ni en la lectura.
- El **coste diario del retraso de Denver** (se suele dar 1,1 M$/día). Tampoco
  aparece.
- **Quién construyó el sistema de maletas de Denver** (BAE Automated Systems).
  El artículo del aeropuerto no lo dice y el de la empresa no existe en
  Wikipedia. La lectura no nombra al contratista.

---

## 7 · Decisiones que conviene que mires

1. **Las ocho sesiones.** Las cuatro pendientes las he titulado así: S5 *El
   cuaderno del proyecto*, S6 *Trabajar a la vez, en digital*, S7 *Contarlo en
   tres minutos*, S8 *Del plan a lo que pasó*. La razón es que los criterios de
   la unidad no son sólo CE1: incluyen **CE3 (3.1 y 3.2, presentar y defender)**
   y **CE5 (5.1, herramientas digitales)**, y con cuatro sesiones sólo de
   detectar/idear/planificar esos dos se quedarían sin tocar. El cierre de la S4
   ya engancha con la S5. Si prefieres otro reparto, se cambia en `S` de
   `c1_build.py` sin tocar nada más.

2. **Los números de los tres casos de la S1 son inventados como ejemplo**, y la
   escena lo dice en su pie y la actividad lo dice otra vez: el trabajo de la
   sesión es salir a medir los del centro. 14 macetas, 24 alumnos, 30 cambios de
   clase a la semana. Si tienes los de verdad, están en `CASOS` dentro de
   `c1_escenas.py`.

3. **El modelo de humedad de la S2 es un modelo, no una medida.** Evaporación
   constante y riego de dosis fija. Está dicho en el pie de la escena, y la
   escena avisa de que en la sesión 8 se sustituirá por los datos del prototipo
   real. Si te parece que de aquí a entonces puede confundir, cámbiame el pie.

4. **Las puntuaciones de la matriz de la S3 son criterio nuestro**, y así va
   rotulado dentro de la escena. Están elegidas para que pase algo didáctico: la
   bomba (el proyecto A, el «principal») **no gana** — gana el servo, y por 2
   puntos de 85, que la propia escena declara insuficientes. Y con los pesos a 1
   gana el gotero. Es a propósito: si la tabla confirmara siempre lo que ya
   habíamos decidido, no enseñaría nada. Pero es una decisión discutible y
   quería que la vieras.

5. **La duración del trimestre (24 sesiones)** la he sacado de `CURRICULO.md`
   (3 sesiones/semana, ~90 útiles al año, tres trimestres → 30, menos evaluación
   y lectura). Es un número redondeado a ojo. Está en un campo editable de la
   escena por si no cuadra con tu calendario.

6. **`voz.py` estaba sin versionar** en el repositorio principal (aparece y
   desaparece en el historial de las ramas de unidad). Lo he metido en la rama
   porque sin él no se puede regenerar el audio. Si lo quitas al recoger, que
   sea a sabiendas.

---

## 8 · Cosas que sé que quedan flojas

- **El gráfico de la S1 son dos rectas.** El coste por semana es constante, así
  que el acumulado es lineal y no hay más que dibujar. Lo que aporta el dibujo
  es la escala y el punto de cruce con la referencia; si te parece poco, la
  alternativa sería pedir el dato semana a semana, y eso ya no lo rellena nadie
  en clase.
- **La escena de la S3 tiene 25 casillas editables.** En un móvil es incómoda.
  La tabla hace scroll horizontal, pero no es lo mismo.
- **La práctica de la S4 son 15 minutos** y montar un Gantt en GanttProject por
  primera vez da para más. Conviene que la primera vez el diagrama esté
  empezado, o que se haga en papel cuadriculado.
- La actividad de la S1 saca a los alumnos del aula 10 minutos. Eso depende
  mucho del centro y de la hora; si no se puede, la alternativa es traer las
  observaciones hechas de casa y usar la sesión entera para medir.

---

## 9 · Comprobado

- `generadores/c1_verifica.py`: **117 comprobaciones, 0 fallos**. Abre la página
  en Chromium, pulsa los cuatro botones de sesión, los cuatro presets de la S1,
  cambia unidades y campos, corre los requisitos de la S2 con tres umbrales
  distintos, intenta comprobar un requisito mal escrito y lo arregla, cambia los
  pesos de la S3 y comprueba la sensibilidad casilla por casilla, mueve tareas en
  el Gantt y contrasta las doce filas de la tabla, y contesta el test entero. Sin
  errores de página ni de consola.
- Las cuatro escenas, **miradas** en captura (`c1_capturas.py`, `c1_mirada.py`):
  arreglé cuatro solapes de etiquetas en los ejes que el verificador no podía
  ver.
- La lectura en PDF, **mirada** página a página: 4 páginas, cabecera para el
  nombre, 30 párrafos numerados y 10 preguntas, las dos últimas de opinión.
- Ninguna clase CSS empieza por `test-` (comprobado en el verificador). Los
  prefijos de las escenas son `p1-`, `p2-`, `p3-` y `p4-`.
