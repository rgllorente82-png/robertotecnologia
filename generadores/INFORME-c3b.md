# Informe · Tema 3 de 4.º de ESO · sesiones 5 a 8

**Materiales y ciclo de vida.** Rama `c3b`.
La unidad queda con **8 sesiones escritas y 0 pendientes**.

> **Nombre del fichero.** El encargo pedía `INFORME.md` y aquí está. Pero las
> unidades hermanas siguen el patrón `generadores/INFORME-<clave>.md` (la
> primera mitad de esta misma unidad está en `generadores/INFORME-c3.md`). Si
> al recoger esto choca con los `INFORME.md` de las otras unidades que se están
> escribiendo en paralelo, **renómbralo a `generadores/INFORME-c3b.md`**: no lo
> enlaza nadie.
>
> Por lo mismo, el commit lleva dentro `ENCARGO.md`, porque el encargo pedía
> `git add -A`. Si cada unidad trae el suyo, quítalo al recoger.

---

## 1 · Qué he tocado

| Fichero | Qué es |
|---|---|
| `generadores/c3_build.py` | **Modificado.** Le he añadido el texto de las sesiones 5 a 8, el segundo test y las cuatro entradas de la barra. **No he tocado ni una línea de las sesiones 1 a 4**: lo único que he quitado del fichero viejo son las cuatro líneas `pendiente=True` y el párrafo del docstring que decía que el proyecto no estaba decidido. |
| `generadores/c3_escenas3.py` | **Nuevo.** Escenas de S5 (la cadena de rendimientos) y S6 (el mismo kilo, dos facturas). |
| `generadores/c3_escenas4.py` | **Nuevo.** Escenas de S7 (veinte años de servicio, cuatro maneras) y S8 (la ficha de impacto y su análisis de sensibilidad). |
| `generadores/c3_fotos2.py` | **Nuevo.** Baja de Commons las siete fotos nuevas, lee su licencia por la API y las añade a `creditos_c3.json` sin pisar las ocho viejas. Lleva además la lista de **descartadas con el motivo**. |
| `generadores/c3_smoke.py` | **Nuevo.** Banco de pruebas: monta una página suelta con las cuatro escenas nuevas y nada más, las abre en Chromium y avisa de errores de JS o de rótulos que se salgan del lienzo. Sirve para depurar sin regenerar el tema entero. |
| `generadores/c3_capturas.py` | **Nuevo.** Capturas de las escenas nuevas en sus estados interesantes, en claro **y en oscuro**. Los PNG van a `/tmp/c3b`, no al repositorio. |
| `generadores/c3_verifica.py` | **Ampliado.** De **163** comprobaciones a **482**. Pulsa todos los controles nuevos y **vuelve a pasar todas las pruebas viejas** de las escenas 1 a 4, sin tocarlas. |
| `generadores/creditos_c3.json` | Siete entradas nuevas, escritas por la API de Commons. |
| `img/c3-balas-latas.jpg` · `c3-vidrio-verde.jpg` · `c3-vidrio-mezcla.jpg` · `c3-horno-cemento.jpg` · `c3-presa.jpg` · `c3-cajas.jpg` · `c3-etiqueta.jpg` | **Nuevas.** Las siete fotos. |
| `4eso/Tecnologia/tema3/index.html` | Regenerado. 363 KB. |

**No he tocado `4eso/Tecnologia/index.html`**, como pedía el encargo. Tampoco la
lectura de aula ni nada de las sesiones 1 a 4.

Para rehacerlo:

```
/home/ubuntu/venv/bin/python generadores/c3_fotos2.py       # sólo si faltan las imágenes
/home/ubuntu/venv/bin/python generadores/c3_build.py
/home/ubuntu/venv/bin/python generadores/c3_verifica.py     # 482 comprobaciones, 0 fallos
/home/ubuntu/venv/bin/python generadores/comprueba_paginas.py
/home/ubuntu/venv/bin/python generadores/c3_capturas.py     # para mirarlo con los ojos
```

---

## 2 · El hilo, y cómo entra cada sesión

He mantenido entera la regla de la primera mitad: **ninguna sesión empieza
enunciando el concepto**. Cada una empieza con una cuenta que el alumno puede
hacer y que le sale al revés de lo que esperaba.

| | Cómo entra | Qué falla delante del alumno | Y entonces aparece |
|---|---|---|---|
| S5 | «El aluminio es reciclable al 100 % e infinitas veces» | Es **verdad**… y aun así sólo el 34 % del aluminio nuevo es reciclado | Reciclable ≠ reciclado. Los rendimientos **se multiplican**, y el ciclo cerrado frente al abierto |
| S6 | La misma tapa de aluminio, dos fábricas | Los MJ son idénticos y el CO₂ va de 4,3 a 18,1 | El factor de emisión, el CO₂ que no viene de quemar nada, y el carbono prestado de la madera |
| S7 | «¿Qué hay que hacer? Reciclarlo» | Un aparato que dura 10 años sin reciclar gana por 4 a 1 | La jerarquía del artículo 4, los bucles de corto a largo, y el efecto rebote |
| S8 | Cinco frases de memorias reales | Tres no se pueden comprobar, y cada una falla por una sesión distinta | Los nueve apartados, la etiqueta de procedencia y el análisis de sensibilidad |

Cada cierre deja abierta la siguiente con una pregunta concreta, y el cierre de
la S4 —que ya estaba escrito y no he tocado— engancha con la S5 sin forzar
nada: prometía «qué le pasa de verdad a cada fracción cuando la echas al
contenedor», y eso es exactamente la S5.

**El proyecto ya está decidido y se nota desde la primera línea de la S5.** De
`PROYECTOS.md`, bloque DECIDIDO (18-sep-2026): riego automático como principal,
con ventilación y lámpara como variantes. Las **tres** salen por su nombre en
las escenas de la S7 y la S8, con **los números de la escena de la sesión 1 de
esta misma unidad**, para que el alumno reconozca su propio aparato:

| variante | MJ de fabricarlo | MJ de usarlo un año |
|---|---|---|
| riego | 85 | 19 |
| ventilación | 66 | 22 |
| lámpara | 76 | 55 |

Salen de la escena de la S1 con sus ajustes de partida (mochila 60 MJ, placa
enchufada, contando pérdidas de la central). No son inventados: son los de la
primera mitad, sumados.

---

## 3 · Las escenas: qué calculan, exactamente

Ninguna enseña un número escrito a mano. El verificador rehace cada cuenta en
Python **a partir de la definición**, no copiando el JavaScript.

### S5 · La cadena de rendimientos

Cinco fracciones (latas, PET, acero, vidrio, cartón). Cuatro etapas cuyos
rendimientos **se multiplican**: captura, clasificación, preparación y horno.
Los dos primeros son deslizadores, porque son los que más varían y los que más
mandan. De ahí salen, calculados:

- lo que queda después de cada etapa, en gramos;
- el **techo del contenido reciclado** (no puede entrar más del que vuelve);
- los kilos que hay que recoger para tener uno de material reciclado;
- la **energía que se salva de verdad por kilo puesto en el mercado**, que no es
  el ahorro por kilo reciclado: en el aluminio son 103 MJ, no 178. Los dos
  números son correctos y contestan a preguntas distintas, y la escena lo dice;
- y la curva de **q elevado a n**: cuánto del kilo original sigue en el mismo
  uso tras n vueltas.

La casilla **«va mezclado»** pone q a cero y la curva se muere en la primera
vuelta. Ese dibujo **es** el ciclo abierto, y es el momento de la sesión.

El segundo techo no está en la escena sino en el texto, porque es una cuenta de
dos líneas que quiero que hagan a mano: si el consumo crece un 3 % al año y los
productos duran 15, la chatarra de hoy viene de un mercado que era
1 ÷ 1,03¹⁵ = 0,64 veces el de hoy. Juntando los dos techos, 0,58 × 0,64 = 37 %,
que se parece mucho al 34 % real. **Explica el orden de magnitud sin acusar a
nadie**, y ésa es la parte que más me interesaba de la sesión.

### S6 · El mismo kilo, dos facturas

Seis materiales con dos columnas: MJ/kg (los de la S2, **sin tocar**) y kg de
CO₂e/kg, que se calculan:

```
CO2 = kWh eléctricos por kilo × factor de la red + lo que no viene del enchufe
```

Y la energía queda amarrada a la sesión 2: `MJ = kWh × 3,6 × 2,0 + lo térmico`,
o sea que **la parte térmica de cada material es `ep − kWh × 7,2`** y no se
puede mover sin mover la tabla de la S2.

Las filas van ordenadas por MJ. **Si las barras de CO₂ no bajan en escalera, el
orden no es el mismo**, y la escena lo dice con nombres y puestos. Con los
ajustes de partida el orden coincide pero las distancias no (el aluminio tiene
2,2 veces la energía del PET y 2,9 veces su CO₂); al marcar el carbono de la
madera, el contrachapado se va a negativo y el orden **sí** cambia en tres
posiciones.

Dos números de la sesión no son estimación sino química, y por eso van
calculados a la vista en el texto:

- **PET incinerado**: C₁₀H₈O₄, masa molar 192, de los que 120 son carbono.
  120/192 × 44/12 = **2,29 kg de CO₂ por kilo**.
- **Madera**: 45 % de carbono × 44/12 = **1,65 kg de CO₂** guardados dentro.
- **Calcinación del cemento**: CaCO₃ → CaO + CO₂, con un clínker al 65 % de cal,
  0,65 ÷ 56 × 44 = **0,51 kg de CO₂ por kilo de clínker sin quemar nada**.

Lo mejor de la escena sale solo: si marcas **las dos** casillas de la madera a
la vez, vuelve a positivo, porque lo que lleva dentro y lo que suelta al
quemarse **son el mismo carbono**. No hay ninguna línea de código que lo
imponga; sale de restar y sumar el mismo 1,65.

### S7 · Veinte años de servicio, cuatro maneras

No hay fórmula cerrada: la escena **recorre el calendario evento a evento** y
suma. Por eso los marcadores dibujados en la línea de tiempo *son* los eventos
que se han sumado. Cuatro estrategias, que son la jerarquía del artículo 4
puesta a hacer cuentas: tirar, reciclar (bucle largo), reparar (bucle corto) y
las dos cosas.

Con el riego y los ajustes de partida:

| | Total 20 años | Frente a tirar |
|---|---|---|
| Fabricar, usar, tirar | 805 MJ | — |
| Reciclar al final | 720 MJ | −85 |
| Reparar | 586 MJ | −219 |
| Reparar y reciclar | 565 MJ | −240 |

**El bucle corto ahorra dos veces y media lo que el largo**, que es la lección.

Y lleva el contrapeso honrado: el **efecto rebote**. Con la lámpara al 100 % de
rebote, reparar **pierde** (2.388 frente a 1.480 de tirarlo), y la escena lo
dice con todas las letras en vez de esconderlo. Me parece la parte más
importante de esa sesión: enseña que la conclusión depende de una hipótesis que
hay que declarar.

Hay también un **punto de equilibrio** que la práctica pide buscar: subir el
coste de la reparación hasta que reparar deje de ganar. Ese valor es una
**especificación de repuesto**, y es un resultado de ingeniería de verdad.

### S8 · La ficha de impacto, y de qué depende

Las tres variantes decididas, con tres piezas configurables cada una (material y
masa). Calcula el inventario completo, los MJ por año de servicio y el CO₂ de
los materiales. Y encima corre el **análisis de sensibilidad**: mueve cada dato
incierto a sus dos extremos con todo lo demás quieto, y ordena las barras por lo
que mueven.

Con el riego de partida (electrónica 60 MJ, 5 años, red española):

| | Recorrido | Mueve |
|---|---|---|
| 1 · Mochila de la electrónica | 23,5 → 59,5 MJ/año | **36,0** |
| 2 · Lo que gasta al año | 22,0 → 50,5 | 28,5 |
| 3 · Años que va a durar | 25,3 → 50,3 | 25,0 |
| 4 · Material de la 1.ª pieza | 31,5 → 33,6 | **2,1** |
| 5 · Masa de las piezas | 31,4 → 31,7 | 0,3 |

**El dato que no tienen mueve diecisiete veces más que el material de la pieza
mayor**, que es lo que llevan dos sesiones discutiendo. Eso es incómodo a
propósito, y la escena y el texto se encargan de que no se lea como «la sesión 3
fue una pérdida de tiempo»: la matriz decidía bien una cosa pequeña, y en cuanto
la pieza crece o el material es caro en energía, esa barra crece con ella.

Con la lámpara el orden **cambia** —manda «lo que gasta al año», con 82,5—, y
ése es el remate: la sensibilidad no es una propiedad del método, es una
propiedad de tu aparato.

La escena termina redactando la **frase que se puede copiar en la memoria**, con
los números dentro y con la condición pegada. Eso también se calcula.

⚠️ **El CO₂ de la electrónica va sin número, con la palabra «no calculado».** Es
deliberado y está explicado dentro de la página: no hay dato publicado, y de los
megajulios no se saca con un factor porque eso es justo lo que la S6 demuestra
que no se puede hacer. Si prefieres que ahí vaya una cifra, hay que decidir cuál
y de dónde sale; yo creo que el hueco declarado enseña más.

---

## 4 · Fotos: licencia por la API, y miradas una a una

Bajadas con `generadores/c3_fotos2.py`, que lee la licencia de la API de
Commons. Las fichas literales están en `creditos_c3.json`. **Las he abierto y
mirado las siete antes de escribir su pie.**

| Fichero | Original | Autor | Licencia | Qué se ve, y por qué está |
|---|---|---|---|---|
| `c3-balas-latas.jpg` | `File:Greenville Public Works, ECVC Recycling Sorting facility - 14.jpg` | Greenville, NC | Dominio público | Pared de balas de latas prensadas y, en primer plano y desenfocadas, **latas caídas por el suelo**. El pie usa las dos cosas: la pintura que llevan todas (tercera etapa de la cadena) y que la pérdida gorda **no se ve en ninguna foto** porque pasa dentro del horno. |
| `c3-vidrio-verde.jpg` | `File:Glas aus Aufbereitungsanlage grün…` | Alter Fritz | CC BY-SA 3.0 | Casco verde y ámbar sobre mesa clara, con **una moneda de un euro** de escala. Ciclo cerrado. |
| `c3-vidrio-mezcla.jpg` | `File:Glas aus Aufbereitungsanlage bunt…` | Alter Fritz | CC BY-SA 3.0 | El mismo montaje, la misma moneda y el mismo fotógrafo, pero con verde, ámbar, incoloro y un trozo azul. Ciclo abierto. **Van en pareja, en `galeria-ri`**: el par es el argumento. |
| `c3-horno-cemento.jpg` | `File:Cement kiln in Gorazdze Cement plant.JPG` | Jb957 | CC0 | Horno rotatorio inclinado sobre sus rodillos, **con un coche aparcado debajo** que da la escala, y la torre de ciclones al fondo. |
| `c3-presa.jpg` | `File:Karahnjukar-dam.jpg` | Christoph Hess | CC BY-SA 3.0 | Presa de escollera con la carretera de coronación encima y una caseta al pie. |
| `c3-cajas.jpg` | `File:Crates of empty Club Mate bottles at 31c3.jpg` | JkoLd19d | CC0 | Un suelo entero de cajas amarillas con botellas retornables **todas iguales y muchas rayadas** de haber pasado ya varias veces. El pie usa las dos cosas: el bucle corto exige envase **normalizado**. |
| `c3-etiqueta.jpg` | `File:EU washing machines label.jpg` | European Commission | Attribution | La etiqueta energética actual, A–G, con **kWh por 100 ciclos** (la unidad funcional de la S1, literalmente) y el QR arriba a la derecha. |

**Miradas y descartadas**, con el motivo, y la lista está escrita dentro de
`c3_fotos2.py` para no volver a bajarlas dentro de un mes:

1. ⚠️ **`File:Refrigerator new label.jpg`.** El título dice *new label* y lo que
   se ve es la etiqueta **vieja**, la de A+++ a D, con el pie «2010/XYZ». La
   escala se rescaló a A–G en 2021. Es exactamente el caso de título que miente
   del que avisa el encargo, y me lo comí hasta que abrí el fichero.
2. **`File:Fjardaal alcoa.jpg`**, la fábrica de aluminio de Reyðarfjörður. Se ve
   como una mancha de dos milímetros al fondo de un fiordo: el pie diría
   «fábrica de aluminio» y se verían montañas. Es la torre Eiffel otra vez. Por
   eso la S6 lleva la **presa** y no la fábrica.
3. **`File:Cement-plant.jpg`.** Enseña muy bien el horno y la torre, pero es una
   foto de catálogo retocada (césped y cielo pegados). Cambiada por la de
   Gorażdże, que además es CC0.
4. **`File:Bottle crates (Pfand kisten).jpg`**: buena, pero el original mide
   449 × 410 y a ancho de página se ve pastosa.
5. **`File:Aberthaw Cement Works1.jpg`**: 640 × 480 y el horno rotatorio no se
   distingue desde esa distancia.
6. **`File:Cans... (32952295076).jpg`**: muy buena pared de balas; gana la de
   Greenville porque además enseña lo que se cae al suelo y es de dominio
   público.

---

## 5 · Vídeos: título y canal comprobados, **nadie se los ha visto enteros**

Comprobados por oEmbed (`generadores/oembed.py`) el 18-sep-2026. **No los he
visto.** Sé cómo se llaman y quién los firma, y nada más. Antes de ponerlos
delante de una clase hay que verlos enteros.

| Sesión | ID | Título (el que devuelve YouTube) | Canal |
|---|---|---|---|
| S5 | `_EA6VL1Zj0s` | Así funciona una planta de selección | Ecoembes España |
| S7 | `aB2mK5QKyvY` | ¿Qué es la economía circular? | Ministerio para la Transición Ecológica y el Reto Demográfico |

**Los dos llevan en su nota un aviso sobre quién los firma**, y no es un adorno:
es la competencia de la unidad. Del de Ecoembes se dice que es el sistema que
gestiona esos envases y que por tanto tiene interés en que la planta salga bien;
del ministerial se le pide al alumno que **cuente cuántas veces dice
«reciclar» y cuántas «reparar» o «prevenir»** y lo compare con el orden del
artículo 4 que acaba de copiar. ⚠️ Si te parece demasiado punzante para un
vídeo institucional, la nota se quita sin tocar nada más; a mí me parece la
mejor actividad de la sesión.

**S6 y S8 se quedan sin vídeo a propósito.** Busqué para las dos. Para la
conversión a CO₂ lo que hay en español son charlas de huella de carbono para
empresa, que no aportan nada por encima de la escena; para la memoria de impacto
no hay nada que no sea publicidad de consultoras. Prefiero dejarlo vacío antes
que rellenar.

---

## 6 · Datos: qué está comprobado y qué es criterio nuestro

Contrastado el 18-sep-2026 contra Wikipedia salvo donde se dice otra cosa.

**Comprobado y usado:**

- **Jerarquía de residuos**: **Directiva 2008/98/CE, artículo 4**, cinco
  escalones y en ese orden.
- **Aluminio reciclado**: en **Estados Unidos, en 2022**, el secundario fue el
  **34 %** de todo el aluminio nuevo puesto en el mercado. La página lo da
  **como dato de Estados Unidos**, no como dato mundial, porque es lo que
  encontré contrastado.
- **Cuerpo y tapa de la lata son aleaciones distintas**, y eso limita el
  reciclado en ciclo cerrado.
- **Cobre en el acero**: no se elimina con oxígeno ni con cal en el horno; sólo
  se previene separando mejor la chatarra o diluyendo con acero nuevo.
- **Electrólisis del aluminio**: 14–16 MWh por tonelada, o sea los 14,1 kWh/kg
  que ya usaba la sesión 2.
- **Ánodos de carbono**: sustituirlos por ánodos inertes se cifra en unas
  **2 t de CO₂e menos por tonelada de aluminio**. Ése es el único de los tres
  sumandos del «4,00» que tiene apoyo publicado.
- **CF₄ del efecto ánodo**: calienta **unas 6.500 veces** más que el CO₂ y dura
  decenas de miles de años en la atmósfera.
- **Cemento**: **CaCO₃ → CaO + CO₂**; alrededor del **50 %** de las emisiones
  del cemento son de la reacción y un **40 %** de quemar combustible; el cemento
  es entre el **4 y el 8 %** del CO₂ mundial (en la página no doy porcentaje, doy
  «una parte enorme», justamente por ese rango).
- **Kárahnjúkar**: presa de escollera de **193 m**, central de **690 MW**,
  construida para la fábrica de aluminio de **Reyðarfjörður**, en marcha desde
  **2007**.
- **Etiqueta energética**: rescalada a **A–G en 2021** (lavadoras y lavavajillas,
  1 de marzo de 2021) y el consumo se declara en **kWh por 100 ciclos**.
- **Depósito obligatorio en Alemania**: desde **2003**.
- **Red eléctrica española 2024, 146 g de CO₂/kWh**: es el mismo dato que ya usa
  la unidad 8, y lo he reutilizado para que las dos unidades no se contradigan.

**Criterio nuestro, y rotulado como tal dentro de la propia página:**

- Los **cuatro rendimientos de la cadena** de la S5. Los dos primeros son
  deslizadores justo por eso.
- Los **12 MJ por reparación** y el **25 % que devuelve reciclar el aparato
  entero** de la S7. Los dos son deslizadores.
- Los **valores de la sensibilidad** de la S8 (los extremos elegidos: 20–200 MJ,
  2–10 años, ±30 % de masa, mitad o doble de consumo).

**⚠️ Lo que conviene que mires, porque es lo más flojo:**

1. **El «4,00 kg de CO₂ por kilo que no vienen del enchufe» del aluminio
   primario.** Es **suma nuestra** y va declarada por partes en el pie de la
   escena y en el docstring: 2,0 de los ánodos (apoyado), 0,3 de los PFC y 1,7
   de la mina, la alúmina y la colada (estimación nuestra). **En la página no se
   atribuye a ninguna institución**: la atribución al International Aluminium
   Institute se queda donde estaba, en los 186 y los 8,3 MJ/kg de la sesión 2.
   Tenía escrito de memoria que la media mundial publicada eran 16,1 kg CO₂e/kg,
   y como **no he podido abrir la tabla del IAI para comprobarlo**, he quitado
   esa atribución del texto. Si la confirmas, se puede volver a poner: el modelo
   da 16,13 con el mix mundial, o sea que encajaría.
2. **El crecimiento del 3 % anual y los 15 años de vida** de la cuenta del
   segundo techo (S5). Son **ilustrativos** y así están puestos («si el consumo
   crece un 3 %…»). No afirmo que ésos sean los valores reales de ningún
   material.
3. **El embalse de Kárahnjúkar.** Tenía escrito «esta presa anegó un valle» y lo
   he rebajado a «detrás de ese muro hay un embalse que ocupa lo que antes era
   tierra», que es lo que puedo sostener. Lo que se inundó exactamente no lo he
   podido contrastar.
4. **Cuántas veces se rellena una botella retornable.** Es un número que pedía a
   gritos entrar en el pie de la foto de las cajas y **no lo he puesto**, porque
   no lo he encontrado en fuente que pudiera citar. El pie habla de lo que se ve
   (botellas idénticas y rayadas) y del **envase normalizado**, que es el
   argumento que me interesaba. Si tienes la cifra, el sitio está preparado.
5. **Los 58 °C del compostaje industrial** de la nota sobre bioplásticos. Es la
   condición de la norma de compostabilidad, pero no la he contrastado en esta
   sesión.
6. **El QR de la etiqueta energética.** Tenía escrito que «lleva a la ficha del
   modelo en el registro europeo», y **eso no lo he podido confirmar aquí**. He
   comprobado que el QR está en la imagen y que el registro **EPREL** existe y
   es público, así que el pie dice ahora las dos cosas por separado: que hay un
   QR arriba a la derecha, y que la ficha de cada modelo está en EPREL, donde
   cualquiera puede buscarla. Que el QR apunte precisamente ahí es lo que dice
   el reglamento, pero no lo doy por escrito hasta comprobarlo.

---

## 7 · Fronteras con las otras unidades

He respetado las tres del encargo y las he hecho **explícitas dentro de la
página**, en bloques «solo para entenderlo», para que no se solapen en clase:

- **S5**: «Lo de hoy es el **proceso industrial**: qué le pasa a un kilo de
  material desde que lo sueltas hasta que vuelve a ser materia prima. **El
  inventario de tu propia basura** —qué sobra de vuestra maqueta, cuánto pesa y
  a qué contenedor va cada recorte— es otra cosa y es del **tema 8**.»
- **S6**: «Lo de hoy es la **herramienta**. **Sumar la cuenta entera de vuestro
  proyecto** es el **tema 8**. Aquí se aprende la conversión; allí se hace el
  inventario.»
- **S7**: «Aquí elegís el bucle; **rediseñar el aparato con lo medido** y
  **defender su impacto** son del **tema 8**.»
- **S8**: «Lo de hoy es el **documento**. **Cómo se cuenta en voz alta** es del
  **tema 1**, y **defender el impacto** delante de la clase, con la cuenta
  completa, es del **tema 8**.»

⚠️ **Donde creo que puedo pisarme, y no lo puedo comprobar porque sólo veo mi
unidad:**

1. **El factor de emisión (S6) y la unidad 8.** El encargo me asigna la
   conversión, y eso he hecho. Pero la unidad 8 tiene ya escrita su sesión 1
   («Medir antes de opinar») y allí se explica `huella = cantidad × factor` y el
   CO₂ equivalente, con los mismos 146 g/kWh de la red española de 2024. **Hay
   solape en la definición.** Mi sesión no repite la unidad 8: mi ángulo es el
   que la unidad 8 no puede dar, porque necesita los MJ/kg de mi sesión 2 —que
   **un megajulio no tiene un CO₂**, que hay CO₂ que no sale de quemar nada, y
   que por eso no existe el factor MJ → CO₂—. Aun así, en clase conviene decidir
   **cuál de las dos se da primero**; yo daría la mía, porque la unidad 8 usa la
   herramienta y aquí se construye.
2. **«La memoria de impacto» (mi S8) y «Defender el impacto» (S8 de la unidad 8,
   pendiente).** Los títulos se parecen mucho. He acotado la mía al
   **documento**: nueve apartados, etiqueta de procedencia y análisis de
   sensibilidad, y he dicho dentro de la página que la **defensa** es del tema 8.
   Si quien escriba la segunda mitad de la unidad 8 lee esto: la ficha ya está
   hecha, y lo que falta allí es la cuenta completa del proyecto y la defensa.
3. **El efecto rebote (S7)** también podría reclamarlo la unidad 8 o la 9. Aquí
   entra como contrapeso de la economía circular y no se vuelve a usar.

---

## 8 · Cosas que he visto en la primera mitad y **no he tocado**

Ninguna es un error de bulto. Las dejo apuntadas, como pedía el encargo.

1. **El `m7-fab` me destapó un defecto de familia.** Mis deslizadores de la S7
   tenían `step="5"` y los valores de partida del aviso (66 MJ) y de la lámpara
   (76) no caen en esa rejilla: el navegador los bajaba a 65 y a 75, el rótulo
   decía una cosa y la cuenta usaba otra. Lo cacé porque el verificador lo
   comparaba con el modelo de Python. **Conviene mirar si pasa lo mismo en las
   escenas viejas**: `m2-masa` (step 5, mínimo 5) y `m4-nuevo`/`m4-tarifa` (step
   5) podrían tener el mismo problema si algún preset cayera fuera de la
   rejilla. Los que hay ahora **sí** caen bien (35, 30, 300, 45), así que hoy no
   falla nada; es una trampa esperando.
2. **La tabla de materiales de la S2 no trae el cartón**, pero el docstring de
   `c3_escenas.py` sí le da 25 MJ/kg. Mi escena de la S5 lo usa. Si algún día se
   completa la tabla de la S2, que sea con ese número.
3. **Convivencia de acentos literales y entidades HTML** en el texto de las
   sesiones 1 a 4. Como la página va en UTF-8 declarado se ve bien; es
   inconsistencia de estilo y yo he seguido la misma mezcla para no desentonar.
4. **El pie de la escena de la S1** dice «Ashby» de las cifras de MJ/kg, pero la
   del aluminio (186) es del International Aluminium Institute, no de Ashby. El
   texto de la sesión 2 sí lo distingue bien; el pie de la escena de la 1 lo
   mete todo en el mismo saco. Es matizable, no falso.

---

## 9 · Decisiones que conviene que mires

1. **El test de la S8 tiene 12 preguntas, no 10.** Cubre la unidad entera: una
   por cada sesión de la 1 a la 4 y **dos por cada una de la 5 a la 8**. Usa el
   identificador **`c3b`**, como pedía el encargo. El verificador comprueba
   expresamente que **los dos tests no comparten ni un nombre de grupo de
   radios**, que contestar uno no toca el otro, y que **ningún `id` se repite en
   la página**. También comprueba que **ninguna clase CSS empieza por `test-`**;
   mis prefijos son `m5-`, `m6-`, `m7-` y `m8-`.

2. **La S5 no hace el inventario de residuos del alumno, y eso puede sorprender.**
   La sesión habla de latas, botellas y vidrio, no de los recortes de su maqueta.
   Es la frontera que pedía el encargo y está dicha dentro de la página, pero si
   en clase alguien espera «hoy pesamos lo que nos ha sobrado», hay que avisar de
   que eso llega en el tema 8.

3. **La S7 puede dar una lectura incómoda: «entonces reciclar no sirve».** Lo he
   peleado en tres sitios distintos del texto (el reto, el pie de la escena y el
   cierre): reciclar **ahorra de verdad**, lo que pasa es que **llega tarde**,
   porque actúa después de fabricar y durar actúa antes. Aun así, es la sesión
   que más depende de cómo se dé en voz alta.

4. **El efecto rebote está a 0 % de partida** en la escena de la S7. Si empezara
   en un valor alto, la conclusión de la sesión saldría del revés desde el
   principio. Prefiero que lo suban ellos y vean romperse su propia conclusión.

5. **La escena de la S8 tiene cuatro segmentadores y seis deslizadores.** Es la
   más «panel de control» de las ocho, y es la más lenta de coger. A cambio es la
   única que produce un entregable. Si te parece demasiado, lo que sobra son las
   tres piezas configurables: con los presets de las tres variantes la sesión se
   sostiene igual.

6. **Los 20 años de horizonte de la S7 son largos para un aula.** Los elegí para
   que el aparato tenga que fabricarse varias veces y la cuenta se vea; con 5
   años no se distinguen las estrategias. Está dicho en el pie que 20 años es la
   **unidad funcional** y que lo que se compara es el servicio, no el aparato.

7. **La práctica de la S5 manda al alumno al pasillo a mirar los contenedores.**
   Es un minuto y es la parte que más se recuerda, pero hay centros donde eso no
   es trivial. La alternativa es que lo traigan mirado de casa.

---

## 10 · Cosas que sé que quedan flojas

- **La escena de la S8 es densa en pantalla pequeña.** El tornado tiene cinco
  filas con dos líneas de rótulo cada una; en un móvil el SVG se escala y los
  rótulos quedan pequeños. La tabla de debajo dice lo mismo con todas las letras
  y en orden, así que la escena no se pierde, pero el dibujo en pantalla pequeña
  es más decorativo que legible.
- **La S5 y la S6 se solapan en una idea**: las dos terminan diciendo «depende de
  qué le preguntes». Es intencionado —es el hilo de la unidad desde la S1— pero
  al leerlas seguidas puede sonar repetido.
- **La cuenta del segundo techo (1 ÷ 1,03¹⁵) usa una potencia** y eso en 4.º se
  puede atragantar. Va con el resultado escrito al lado (0,64) para que se pueda
  seguir aunque no se sepa calcular la potencia.
- **La S8 es larga**: escena de dos paneles, ficha de nueve apartados, tornado de
  cinco barras y test de doce preguntas en 15 minutos de cierre. El test se puede
  mandar para casa sin perder nada: se corrige solo en el navegador.
- **El «no calculado» de la electrónica va a generar preguntas.** Está explicado
  dos veces (en un «solo para entenderlo» y en una pregunta del cierre), y aun
  así apuesto a que algún grupo pone un número ahí. Puede que sea bueno.

---

## 11 · Comprobado

- **`generadores/c3_verifica.py`: 482 comprobaciones, 0 fallos.** Abre la página
  en un Chromium de verdad, **con Google Fonts bloqueado a propósito** (que es el
  caso malo: la tipografía de repuesto es un 28 % más ancha), pulsa **los ocho**
  botones de sesión y comprueba que cada una trae sus cuatro bloques, su escena,
  sus bloques PARA LA LIBRETA y SOLO PARA ENTENDERLO y su práctica evaluada.
  Vuelve a pasar **todas las pruebas viejas** de las escenas 1 a 4 sin tocarlas.
  De las nuevas:
  - **S5**: seis configuraciones, contrastando las cuatro etapas en gramos, el
    rendimiento de la cadena, los kilos a recoger, el techo del reciclado, la
    energía salvada y la potencia `q^n`, contra un modelo rehecho en Python. Y el
    caso de mezclado, donde del kilo no queda nada tras tres vueltas.
  - **S6**: ocho configuraciones cruzando material, enchufe, masa y las dos
    casillas. Comprueba además que **los megajulios no se mueven** al cambiar de
    enchufe mientras el CO₂ se multiplica por cuatro, que PET y acero empatan en
    CO₂ con 3,4 veces de diferencia en MJ, y que la madera se va a negativo con
    una casilla y vuelve a positivo con las dos.
  - **S7**: seis configuraciones, contrastando para las **cuatro** estrategias el
    número de fabricaciones, el de reparaciones y el total, contra una simulación
    rehecha recorriendo el calendario en Python. Y los dos resultados de la
    sesión: que reparar ahorra más del doble que reciclar, y que con el rebote al
    100 % reparar pasa a perder.
  - **S8**: cinco configuraciones con las tres variantes y con materiales y masas
    cambiados a mano, contrastando la ficha entera y **el tornado barra a barra y
    en orden** —no vale acertar los números y ponerlos desordenados, porque lo
    que la sesión enseña es el orden—. Más que con la lámpara el primer puesto
    cambia.
  - **Los dos tests**: que el de la unidad tiene doce, que da 12 de 12 y 0 de 12,
    que **no comparte ningún nombre de grupo de radios** con el de la S4, y que
    contestar uno **no toca** el otro.
  - Y que **ningún `id` se repite** en la página y **ninguna clase empieza por
    `test-`**.
- **`generadores/comprueba_paginas.py`: 23 páginas, ninguna con NUL ni
  caracteres rotos.**
- **Miradas las cuatro escenas en captura** (`c3_capturas.py`), en claro **y en
  oscuro**, y arreglados cuatro defectos que el verificador no podía ver:
  1. En la S7, los rótulos del eje de años caían **dentro de la cuarta fila** de
     la línea de tiempo. Se han separado las filas y bajado el eje.
  2. En la S6, la barra negativa del carbono de la madera se metía encima del
     número de los megajulios. Ahora las dos mitades del eje tienen su hueco
     reservado y comparten escala.
  3. En la S6, el desglose ponía «0,62 kg» a la derecha mientras el título decía
     «−1,03 kg» y parecían contradecirse. Ahora se lee «−1,65 … +0,62» y el neto
     está en el título.
  4. En la S5, una fila de la tabla se partía en dos líneas y dejaba una «g»
     suelta. Rótulo acortado.
- **Números del texto recalculados uno a uno** contra las escenas. Dos
  correcciones: la tapa de contrachapado de 72 g da **0,04** kg de CO₂e y no
  0,05; y con la lámpara el primer puesto del tornado es «lo que gasta al año»,
  no «cuánto dura», que es lo que tenía escrito.
