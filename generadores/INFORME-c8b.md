# Informe · 4.º de ESO · Tema 8 · Sostenibilidad y accesibilidad · sesiones 5 a 8

Rama `c8b`. Entregada la **segunda mitad** de la unidad. La página pasa de
**4 sesiones escritas y 4 pendientes** a **8 escritas y 0 pendientes**.

> **Dónde está este informe.** El encargo pedía `INFORME.md` y ahí está, en la
> raíz. Los once informes anteriores viven en `generadores/INFORME-c*.md`; si
> prefieres la convención de la carpeta, esto se mueve a
> `generadores/INFORME-c8b.md` en un segundo. **No he tocado el de la primera
> mitad** (`generadores/INFORME-c8.md`).

---

## Qué hay entregado

| Fichero | Qué es |
|---|---|
| `4eso/Tecnologia/tema8/index.html` | La unidad entera. 410 KB (antes 211). Regenerada. |
| `generadores/c8_build.py` | **Modificado**: las cuatro sesiones nuevas, el segundo test y una regla de CSS. |
| `generadores/c8_escenas3.py` | **Nuevo**: el modelo compartido `window.C8B` y las escenas de la S5 y la S6. |
| `generadores/c8_escenas4.py` | **Nuevo**: las escenas de la S7 y la S8. |
| `generadores/c8_verifica.py` | **Ampliado**: de 196 a **369 comprobaciones, 0 fallos**. |
| `generadores/c8_fotos.py` | **Modificado**: las cuatro fotos nuevas, con su licencia consultada por la API. |
| `generadores/c8_mirada.py` | **Modificado**: captura las ocho sesiones, no las cuatro primeras. |
| `generadores/c8b_mirada.py` | **Nuevo**: captura cada escena nueva en los estados que cuentan otra historia. |
| `img/c8-raee-pilas.jpg`, `c8-fotovoltaica.jpg`, `c8-boton-peatonal.jpg`, `c8-poster.jpg` | Las cuatro fotos de Commons. |

**No he tocado `4eso/Tecnologia/index.html`**, como pedía el encargo. Tampoco
he tocado nada de las sesiones 1 a 4, ni `unidad_base.py`, ni `test_auto.py`,
ni ningún generador de otra unidad.

### Cómo se ejecuta

```
~/venv/bin/python generadores/c8_build.py       # la página
~/venv/bin/python generadores/c8_verifica.py    # 369 comprobaciones, sale 0 si todo va
~/venv/bin/python generadores/comprueba_tests.py  # que los dos tests no se pisen
~/venv/bin/python generadores/comprueba_paginas.py
~/venv/bin/python generadores/c8b_mirada.py     # PNG en /tmp/c8b/esc/, para mirarlos
```

---

## El hilo de las cuatro sesiones

La primera mitad enseñaba la técnica con ejemplos. Esta la aplica a lo que el
alumno tiene encima de la mesa, y termina en algo que se defiende.

| | Con qué problema abre | Qué falla al intentarlo | Qué concepto aparece |
|---|---|---|---|
| **S5** | «¿Cuántos gramos de residuo habéis generado?» | Se cuenta **lo que se ve**: sale diez veces menos | Inventario por fracción y por plazo · recorte ≠ sobrante |
| **S6** | «¿Compensa?» con seis números en seis libretas | Sumar no se puede (unidades distintas) y un total solo no contesta | Cuenta completa · punto de equilibrio · el dato que no existe va como **banda** |
| **S7** | Cinco propuestas de rediseño que suenan bien | Cuatro tocan la barra pequeña y una rompe un requisito | Los requisitos se escriben **antes** · kg de CO₂e por año de servicio |
| **S8** | «Eso te lo has inventado» | «Lo pone en internet» y «lo hemos calculado nosotros» no se sostienen | Cifra defendible · **no se discute, se recalcula** |

Cada sesión recoge la anterior y deja abierta la siguiente. La S5 cierra con
«la balanza no ordena por daño», que es literalmente el problema de la S6; la
S6 cierra con «ahora vais a querer bajarlo», que es la S7; y la S7 cierra con
«falta que aguante cuando alguien lo ataque», que es la S8.

---

## Decisiones, y por qué

### 1. Una sola cuenta para las cuatro escenas

`c8_escenas3.DATOS` deja en `window.C8B` el modelo del proyecto (las tres
variantes decididas el 18-sep) y **la cuenta**, una sola. Las cuatro escenas la
llaman; ninguna tiene aritmética propia.

Eso no es elegancia: es lo que permite que la escena de la **S7 pruebe diez
rediseños uno a uno** rehaciendo la cuenta entera con cada uno, y que la de la
**S8 recorra las 64 combinaciones** de seis hipótesis. Si cada escena tuviera su
cuenta, esos dos números serían mentira.

Las cuatro escenas hacen `if(!window.C8B) return;`: si ese bloque no cargara, se
callan en vez de pintar cualquier cosa.

### 2. El proyecto del curso: aterrizado en las tres variantes, sin excepción

Todo lo de la segunda mitad sale de `PROYECTOS.md`, bloque DECIDIDO. Las cuatro
escenas llevan arriba los mismos tres botones —**Riego · Ventilación ·
Lámpara**— y **cada variante da un resultado distinto**, que es lo que impide
copiar el trabajo de otro grupo:

- En la S6, el **riego no compensa en CO₂ nunca**, el **aviso compensa en menos
  de dos años por el peor extremo de la banda**, y la **lámpara depende**.
- En la S7, «medir cada media hora» **no rompe nada en el riego** y **rompe el
  requisito de reaccionar a tiempo en la lámpara y en el aviso**.
- En la S8, la conclusión del aviso aguanta 36 de 64 combinaciones y la de la
  lámpara, 0 de 64.

Ninguno de esos nueve resultados está escrito a mano: todos salen de la cuenta,
y el verificador los rehace en Python.

### 3. Que el riego NO compense es una decisión, y la defiendo

Es el resultado más incómodo de la unidad y me lo he encontrado al hacer la
cuenta, no lo he buscado: **regar a mano no cuesta casi CO₂, así que no hay nada
que devolver**. El ahorro de agua tampoco salva el balance (unos 8 L al año).

Podía haber maquillado la comparación. He hecho lo contrario: la escena calcula
**al revés** cuánto tendría que costar regar a mano para que hubiera punto de
equilibrio —y dice cuántos filetes de ternera son, enlazando con la S1— y la
sesión dedica un bloque PARA LA LIBRETA entero a por qué eso **no hunde el
proyecto**: lo que aporta el riego es que la planta sigue viva nueve días sin
nadie, y eso se declara **en otra columna y con su propia medida**.

Me parece la mejor página de las cuatro, pero **es una decisión tuya**: si
prefieres que el proyecto principal del curso no salga perdiendo en la única
columna que la clase va a mirar, se puede cambiar el indicador del riego (por
ejemplo, contar el coste de reponer la planta muerta). **No lo he hecho porque
ese número no lo tengo medido y habría que inventarlo.**

### 4. La electrónica entra como banda, y eso lo obligaba la unidad 3

La unidad 3, en su sesión 8, escribe literalmente «no calculado» en la casilla
del CO₂ de la electrónica, y explica por qué: no hay dato publicado y **de los
megajulios no se saca con un factor**. Si yo ahora pusiera un número, la unidad
8 contradiría a la 3 en la misma web.

Así que la S6 convierte ese hueco en el centro de la sesión: **dos deslizadores**
(por lo bajo y por lo alto), una **banda** en la cascada y en las curvas, y un
**punto de equilibrio que es un intervalo**. El resultado pedagógico es mejor
que el número: *el ancho de la franja es un resultado*, y cuando la franja se
come la decisión (la lámpara) ya sabes exactamente qué hay que ir a medir.

Es también lo que hace que la S8 tenga sentido: la primera objeción del banco es
«el peso de la electrónica te lo has inventado», y la escena la contesta poniendo
la banda en su extremo malo.

### 5. La geometría de la S5 se calcula, no se dibuja

La escena del inventario **coloca de verdad** las piezas de N grupos sobre una
plancha de 1.220 × 610 con un empaquetado por filas —el mismo que se hace con la
sierra: se corta una tira a lo ancho y de ahí salen las piezas de esa altura—, y
de esa colocación salen **tres áreas distintas**:

- **piezas**, lo que acaba en los aparatos;
- **recorte**, los huecos entre piezas: no sirven para nada;
- **sobrante**, la franja entera de debajo: **es material si alguien la guarda**.

Esa tercera distinción es el corazón de la sesión y solo se ve dibujándola.
El verificador rehace el empaquetado en Python y compara las tres áreas; con seis
grupos de riego coinciden al gramo (362,9 / 32,4 / 944,3 g).

⚠️ El empaquetado por filas es **criterio nuestro y está rotulado como tal**: un
taller de verdad aprovecha algo más, así que el recorte que sale es un **techo**,
no una medida.

### 6. Los cinco requisitos de la S7 se calculan; no son etiquetas

Es lo que separa esta escena de una lista de casillas:

- **«Aguanta los nueve días»** sale de dividir la capacidad de la pila entre la
  corriente media *que resulte de los cambios marcados* (la cuenta de la S4). Con
  pilas no llega; con pilas **y** durmiendo, sí.
- **«Reacciona a tiempo»** depende de la variante.
- **«Lo usa cualquiera»** es el artículo 23.2.a de la Orden TMA/851/2021, el
  mismo de la S2.
- **«Devolver la placa» está vetado** mientras la carcasa vaya pegada, y la
  escena dice por qué. Es, además, el mejor rediseño de la unidad: **estaba
  escondido detrás de otro**, y eso solo se descubre pulsando.

Hay un bloque «solo para entenderlo» dedicado a la trampa del gráfico: bajar el
pulsador a 1,00 m **no mueve la barra de CO₂ ni un milímetro** y es probablemente
el cambio más importante de los diez. Por eso los requisitos van **arriba y en
semáforo**, fuera del número: *lo que no tiene barra en el gráfico desaparece de
la discusión*. Ahí es donde la accesibilidad y la sostenibilidad de esta unidad
se tocan de verdad, y no antes.

### 7. La S8 enumera las 64 combinaciones de verdad

Seis objeciones → 2⁶ = 64 combinaciones de hipótesis. La escena las recorre una
a una, pinta una cuadrícula de 64 cuadritos y dice en cuántas aguanta la
conclusión. Y para saber **cuál manda**, empareja cada combinación con su gemela
—la misma más esa objeción— y cuenta en cuántas parejas la conclusión pasa de
aguantar a caerse. Con el aviso, la que manda es siempre la misma: **«eso solo
ahorra si la gente hace caso»**. O sea que el dato más frágil del proyecto no es
electrónico.

Para el punto de equilibrio la S8 usa **el extremo malo de la banda**, a
propósito: si aguanta en el peor caso, aguanta.

**Una cosa que tuve que añadir al mirarla.** Con la lámpara salía *0 de 64* y no
había ninguna manera de salir de ahí: un callejón sin salida pedagógico. Le he
puesto al alumno la palanca que sí la arregla, que no es argumentar: la casilla
**«el curso que viene otro grupo monta su proyecto con vuestra placa»**, o sea el
rediseño de la S7. Con eso y prometiendo más vida, vuelven a salir cuadritos
verdes. El cierre de la unidad queda así: **a veces un número no se defiende
mejor, se rediseña.**

### 8. El test de la S8: `c8b`, 14 preguntas, la unidad entera

Identificador **distinto** del de la S4 (`c8`), como pedía el encargo. El
verificador comprueba además lo que de verdad importaba: que **los dos tests no
comparten ni un solo `name` de radio**, y que corregir uno no toca el otro.
`comprueba_tests.py` da «bien» para el tema 8.

Ninguna clase CSS nueva empieza por `test-`; las del módulo empiezan por `ta`.
Los prefijos de las escenas nuevas son `o5-`, `o6-`, `o7-`, `o8-`, y ningún id
empieza por `ses-`.

---

## Continuidad con la unidad 3, que era media tarea del encargo

**No he vuelto a explicar el ciclo de vida ni cómo se pasa de megajulios a CO₂.**
La S6 enlaza a `../tema3/` y lo usa:

- Los **factores de los materiales son los de la unidad 3, copiados sin tocar una
  cifra** de `c3_escenas4.py`: `co2 por kilo = kWh eléctricos por kilo × factor de
  la red + la parte que no sale del enchufe`.
- Las **masas de las tres piezas de cada variante son las de la unidad 3**
  (60 g de contrachapado en el riego, 20 en el aviso, 80 en la lámpara). Lo que
  añado es de qué tamaño son, porque hoy hay que colocarlas en la plancha.
- Los **2,29 kg de CO₂ por kilo de PET incinerado** salen de la fórmula que se
  calculó allí.
- La unidad 3 dejó dos frases diciendo que esto era del tema 8 («el inventario de
  tu propia basura» y «sumar la cuenta entera de vuestro proyecto»). **Las dos
  están cumplidas**, en la S5 y en la S6.

**Una reconciliación que tuve que hacer y que está declarada en el pie de la
escena.** En la unidad 3, la fila del riego se llama «tornillería **y bomba**» y
vale 14 g: allí solo contaba el material. Aquí la bomba va en la lista de
electrónica, porque lo que decide su contenedor no es de qué está hecha, es que
lleva un motor. **Los 14 g no se han tocado**, así que la masa total del riego en
esta unidad es algo mayor que en la 3. Está dicho en la escena, pero **míralo**:
es el único sitio donde las dos unidades no cuadran exactamente.

### Fronteras respetadas

- El **inventario del residuo del grupo** es de la S5; la **máquina del
  reciclado** (la cadena de cuatro etapas, el 0,581) se queda en la unidad 3, y
  hay un bloque que lo dice.
- **Contar el proyecto** es de la unidad 1, **la memoria de impacto escrita** es
  de la unidad 3 (S8) y **entregarlo a alguien** es de la unidad 9. La S8 lleva
  un bloque «solo para entenderlo» que nombra las tres y dice que lo de hoy es
  solo sostener los números cuando alguien los empuja.
- El **diseño universal** está explicado en la S2 y aquí **no se vuelve a
  explicar**: aparece como **requisito** en el semáforo de la S7.

---

## Lo que encontré mal, y no he tocado

### En la primera mitad (como pedía el encargo, lo digo y no lo toco)

1. **La bomba no está en la escena de la S4.** El informe anterior ya lo dejó
   apuntado como algo a hacer «si el proyecto acaba siendo el riego». Pues ha
   acabado siéndolo: el riego es **el proyecto principal del curso**. Añadirla es
   una línea en `PIEZAS` de `c8_escenas2.py` y otra en `c8_verifica.py`. **No lo
   he hecho porque el encargo dice no reescribir la primera mitad**, pero ahora
   es más que un detalle.
2. **La escena de la S2 dibuja una caja de 26 × 17 cm** elegida antes de que
   hubiera proyecto. Con el riego decidido, encaja razonablemente; solo lo dejo
   anotado.
3. No he encontrado ningún **error** en las sesiones 1 a 4: he rehecho a mano
   los cuatro cálculos que citan (los 2,25 m de rampa, los 39 mm del pulsador, el
   44 % del regulador y los tres órdenes de magnitud) y salen.

### En mi propio texto, corregido por la propia escena

Lo apunto porque es exactamente el método que enseña la unidad, aplicado a mí:

- Escribí que guardar el sobrante era «el cambio de mayor efecto de toda la
  unidad». **Falso**: en masa de residuo manda, pero en kilos de CO₂ son 24 g al
  año. Corregido, y además ahora lo usa la S5 para avisar de que masa e impacto
  no dan el mismo ganador.
- Escribí que el RAEE era «lo que menos pesa». **Falso**: con el alimentador de
  pared son 130 de 412 g, un tercio. Reescrito el titular de la escena, la nota
  de cierre y una pregunta del test.
- Escribí que la sexta idea buena de la S7 estaba «en la sesión 5». **Falso**: la
  grande es reutilizar la placa, que vale cuatro o cinco veces más. Corregido.
- La S6 daba «no hay punto de equilibrio» en un caso en el que las curvas **sí**
  se cruzaban por el extremo bueno de la banda. Eran tres casos y yo tenía dos.

### Un choque de números entre las dos mitades, y cómo lo he resuelto

La S4 dice que el montaje del riego come **85 mA** (Uno 45 + LED 15 + sonda 25).
Mi modelo llevaba 50. **He puesto 85**, que es literalmente el número del reto de
la S4, y he dejado el comentario en el código para que no se vuelva a mover. Para
la lámpara uso **60 mA y solo el control**: la tira LED no entra ahí porque sus
vatios ya están en la columna del ahorro, y contarla dos veces sería un error
silencioso.

---

## Datos que un humano tiene que mirar antes de publicar

Todos están rotulados dentro de la página, en el pie de su escena o en el pie de
foto, pero los junto aquí:

| Dato | De dónde sale | Qué hay que hacer |
|---|---|---|
| **Banda de la electrónica, 2 a 20 kg CO₂e** | Orden de magnitud de estudios de placas pequeñas. **No es una medida.** | Es el dato que sostiene media unidad. O se busca una fuente citable, o se deja como banda (que es lo honrado y lo que hace la escena). |
| **Retorno energético de un panel solar, «uno o dos años»** | Bibliografía de análisis de ciclo de vida, de memoria. Va rotulado como orden de magnitud en el pie de foto. | **Comprobarlo** contra IEA-PVPS o similar antes de publicar, o quitar la cifra y dejar solo la pregunta. |
| **Gas natural, 0,202 kg CO₂/kWh** | Valor habitual. | Contrastar con la tabla del MITECO del año que toque. |
| **Pilas: 0,20 kg CO₂e una de 9 V, 0,10 una AA** | Estimación. Declarado en la escena como el peor apoyado después de la electrónica. | Ídem. |
| **Agua de red, 0,3 g CO₂/L** | Estimación. | Ídem. Mueve poquísimo el resultado. |
| **Transporte, 0,015 / 0,100 / 0,550 kg CO₂ por t·km** | Órdenes de magnitud habituales, no tabla oficial. | Mueve gramos a estas masas; poco riesgo. |
| **Contrachapado, 1,80 kg/m² a 4 mm** | Densidad ~450 kg/m³ (chopo). El de abedul pesa el doble. | La escena ya dice «pesa la vuestra». |
| **RD 110/2015: tiendas de más de 400 m² recogen RAEE pequeños sin obligación de compra** | Cita legal. | **Verificar el artículo exacto** antes de que un alumno vaya a una tienda con esto. |
| **Directiva (UE) 2024/825** (afirmaciones ambientales genéricas y «neutro en carbono») | Cita legal. El texto dice «los plazos se están cumpliendo justo ahora, en 2026» y manda comprobar en el DOUE. | Confirmar la fecha de aplicación y si ya hay transposición española. |
| **El aula del aviso: 144 m³, ΔT 12 °C, caldera al 90 %** | Modelo nuestro, declarado entero en el pie. | Si tu aula es otra, el número cambia; es un mando que se puede añadir. |

### Los cuatro vídeos: **nadie los ha visto enteros**

Comprobé **título y canal por oEmbed** de los cuatro, y solo eso. Ninguno se ha
visto de principio a fin.

| Sesión | Vídeo | Canal | Aviso que lleva en la página |
|---|---|---|---|
| S5 | Cómo se gestionan los RAEE | Asegre | Digo que **Asegre es la asociación de las empresas que gestionan esos residuos** y que tiene interés en que el proceso salga bien en el vídeo. Mismo criterio que la unidad 3 con Ecoembes. |
| S6 | Cálculo de retorno de inversión con placas solares | Carlos Codina, asesor energético | Digo que **vende asesoría energética** y que su retorno está en **euros**, no en kilos: misma división, otra unidad, otro número. |
| S7 | ¿Qué es el ecodiseño? No es lo mismo | Irene Ramos, diseño industrial | Sin conflicto declarado. |
| S8 | Greenwashing e información ambiental en productos | GIZ México | Institucional. |

Los tres primeros los elegí, además, **porque se pueden criticar**: dos de ellos
llevan su conflicto de interés dentro y la sesión lo usa.

### Las cuatro fotos: licencia por API **y** miradas una a una

| Clave | Fichero de Commons | Autor · licencia | Qué se ve, y por qué está |
|---|---|---|---|
| `c8-raee-pilas` | Elektronikavfall.jpg | Frankie Fouganthin · CC BY 4.0 | Punto de recogida sueco con **dos carteles distintos** (pilas y residuo eléctrico) y, debajo, sobre todo **cables y cargadores**: exactamente lo que le va a sobrar al alumno. |
| `c8-fotovoltaica` | Rooftop solar photovoltaic installation.jpg | Marta Victoria · CC BY-SA 4.0 | Dos paneles en un tejado de teja: el ejemplo clásico del retorno. |
| `c8-boton-peatonal` | An Australian pedestrian crossing button.jpg | James Cridland · CC0 | Pulsador con **flecha en relieve** y **botón grande y redondo**: cuatro canales para una sola información, y el criterio de superficie de la S2. |
| `c8-poster` | GD09 Poster Session.jpg | David Eppstein · CC BY-SA 3.0 | Sesión de pósteres: gente **de pie al lado de su número** para que se lo discutan. |

Ninguna es decorativa y en las cuatro el pie describe lo que de verdad se ve en
la imagen. La del pulsador es vertical (3.072 × 4.080) y a todo lo ancho se comía
la pantalla: he añadido **una sola regla de CSS propia de la unidad**
(`.foto.alta img{max-height:560px}`), con el mismo nombre de clase que ya usa la
unidad 3, inyectada al final para no tocar el molde común.

---

## Dudas que te dejo

1. **¿La lectura de aula se queda como está?** El PDF cubre los temas de la S1 y
   la S2 (Keeling y Ed Roberts). Las cuatro sesiones nuevas no tienen lectura, y
   el encargo no la pedía. Si quieres una segunda, hay material de sobra (el
   cártel Phoebus está en el PDF, pero el residuo electrónico y la defensa de
   cifras no).
2. **El riego perdiendo en CO₂** (ver decisión 3). Es lo que más me gustaría que
   miraras con ojos de aula.
3. **¿Dos tests o uno?** He dejado el de la S4 donde estaba y he añadido el de la
   S8 sobre la unidad entera, que es lo que hacen las unidades 1 a 4 y la 9. Son
   24 preguntas en total en la misma página.
4. **La bomba en la escena de la S4** (ver arriba). Si me dices que sí, es un fix
   de cinco minutos.
5. **No hay enlace directo a una sesión de otra unidad.** La S6 enlaza a
   `../tema3/` y dice «sesiones 2 y 6», pero al abrirse siempre cae en la S1
   porque el molde no lee el `#hash` de la URL. Se arreglaría con seis líneas en
   `NAV_JS` de `unidad_base.py` —y funcionaría para las veintitrés páginas—,
   pero es el molde común y **no lo he tocado sin permiso**.

---

## Comprobado antes de entregar

- `c8_build.py` → **8 sesiones escritas, 0 pendientes**, 410 KB.
- `c8_verifica.py` → **369 comprobaciones, 0 fallos**, con las escenas viejas y
  las nuevas. Pulsa los tres botones de variante de cada escena nueva, mueve
  todos los deslizadores, marca y desmarca las casillas, comprueba el veto de la
  S7, y **rehace en Python** el empaquetado de la plancha, el inventario de
  residuo, la cuenta completa, los cinco requisitos, el ranking de rediseños y
  las 64 combinaciones de la S8. Los patrones están escritos otra vez a partir de
  la definición, no copiados del JavaScript.
- Sin errores de JavaScript ni de consola en ninguna de las ocho sesiones.
- `comprueba_tests.py` → tema 8: **2 tests, bien**, sin pisarse.
- `comprueba_paginas.py` → 23 páginas, ninguna con caracteres rotos.
- Las cuatro escenas nuevas **miradas** en PNG en sus estados de arranque y en
  los estados extremos (`/tmp/c8b/esc/`). De ahí salieron cinco arreglos de
  dibujo: rótulos que se pisaban, etiquetas cortadas a mitad de una entidad HTML,
  barras de material invisibles al lado de la banda, y un mensaje de «no se
  cruzan» que aparecía cuando sí se cruzaban.
