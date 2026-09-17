# Informe · U5 de 2.º de ESO · Mecanismos, sesiones 4, 5 y 6

Rama `tema5b`, worktree aislado. Commit hecho en la rama; **sin push** y sin tocar `main`.

La unidad queda **completa: seis sesiones de seis**.

---

## Lo primero: esta vez sí se ha ejecutado todo

El informe anterior (`generadores/INFORME-tema5.md`) avisaba de que en aquella sesión no se
pudo ejecutar ni una línea de código. Aquí sí: hay **Python, red y un Chromium de verdad**
(Playwright estaba instalado en `~/venv`). Así que:

- el generador se ha ejecutado y **reproduce byte a byte** la página en dos pasadas seguidas;
- la página se ha **abierto en el navegador** y se han pulsado todos los controles de las
  ocho escenas, en los 40 estados que tienen entre todas;
- las licencias de las fotos se han comprobado **por la API de Commons** y, además, las
  imágenes se han **abierto y mirado** una a una;
- los vídeos se han comprobado por **oEmbed** y se ha medido su **duración de verdad**;
- y hay un script nuevo, `generadores/u5_verifica.py`, que deja todo esto repetible.

Lo primero que encontró esa red: **la leva de programa recorría su perfil al revés de lo que
decía su propio texto**. Ver «El fallo que cazó la verificación».

---

## Qué hay dentro

| # | Título | Escena interactiva | Práctica evaluada sobre 10 |
|---|---|---|---|
| 4 | El motor gira y el pistón sube y baja: transformar el movimiento | **Biela-manivela** (3 longitudes de biela, puntos muertos, gráfica del pistón) y **Leva / tornillo-tuerca / piñón-cremallera** (5 modos) | Trazar la leva de una máquina de sellar + el gato + el portón |
| 5 | Dos ruedas de cartón que engranen de verdad | **Plantilla de engranajes**: eliges módulo y dientes y te da los números para el compás | Taller: trazar, recortar, montar y **contar vueltas** |
| 6 | Ningún mecanismo regala nada | **La máquina entera**: dos etapas encadenadas + salida, con velocidad × fuerza = 1 | **Test de 12 preguntas que se corrige solo** |

Minutados: la 4 va 10/20/25/5 como las anteriores; la **5 es de taller** (10/15/**30**/5) y la
**6 de repaso** (5/20/**25**/10). Las seis llevan bloques `PARA LA LIBRETA` separados de los
`SOLO PARA ENTENDERLO`, y las tres nuevas cierran con tres preguntas desplegables.

### El hilo, que es lo que importa

La unidad ya colgaba de una idea —*un mecanismo no crea nada, cambia una cosa por otra*—.
Estas tres la cierran:

- La **4** nace de un corte: hasta aquí *entraba un giro y salía un giro*. Empieza por un
  problema real (tienes un motor y necesitas movimiento recto), deja que el alumno pruebe la
  solución ingenua —**enrollar una cuerda en un tambor**, que es lo que ya sabe de la sesión
  2— y enseña por qué se cae por cuatro sitios: solo tira, no vuelve sola, el tambor engorda
  al enrollarse (**no se puede calcular**) y no aguanta 3.000 vueltas por minuto. Solo
  entonces aparecen los cuatro mecanismos, y cada uno resuelve uno de esos cuatro fallos.
- La **5** nace de un fracaso que van a vivir: recortas dos ruedas de cartón a ojo y **no
  engranan**, por muy bien que recortes. De ahí sale el **módulo**, que es el primer concepto
  del tema que no sirve para predecir sino para **fabricar**.
- La **6** recoge: las relaciones se multiplican, y **velocidad × fuerza = 1** siempre.

Y se cierra el título del tema. La sesión 6 vuelve a *el músculo mueve poco y mal* y deja
abierto el tema 6: todos estos mecanismos necesitan que alguien empuje por un extremo.

---

## Las escenas: qué calcula cada una

Ninguna lleva un número escrito a mano. `u5_verifica.py` lo comprueba leyendo lo que la
escena escribe en pantalla y comparándolo con la cuenta hecha en Python.

**Biela-manivela.** La posición del pistón sale de la cinemática exacta,
`x = r·cos t + √(L² − r²·sen²t)`, no de un seno. De ahí las dos cosas que enseña: que la
**carrera es 2r exacta** valga lo que valga la biela, y que **a un cuarto de vuelta el pistón
no está a media carrera** (60 %, 56 % o 53 % según la biela — medido, no estimado). La
gráfica de abajo se muestrea con esa misma función cada 2°. Los dos puntos muertos se marcan
solos cuando `|sen t| < 0,06`.

⚠️ La biela corta es **2,5 r** y no menos a propósito: por debajo de eso el pistón entraría
dentro del círculo que barre la manivela, que es justamente por lo que no existen motores
así. Por el mismo motivo la manivela se dibuja como brazo y muñequilla, no como disco.

**Leva.** El perfil se dibuja como curva polar `r(α)` y la altura del seguidor sale de **esa
misma función** evaluada en la dirección del seguidor: no hay dos códigos que puedan
discrepar. La gráfica de la derecha, igual. Tres perfiles: excéntrica (un círculo con el eje
descentrado — su ecuación polar *es la misma* que la del pistón, y el texto lo dice),
«de programa» (sube 150°, dwell 90°, cae 60°, descansa 60°) y cuatro lóbulos de martinete.

⚠️ El seguidor es **de punta y sobre la vertical del eje**. Solo en ese caso la altura es
exactamente `r(α)`; con un rodillo habría que corregir el perfil. Está dicho en la sesión.

**Tornillo-tuerca.** El filete avanza un paso por vuelta y la tuerca con él (vive en el mismo
surco), así que lo que se ve y lo que dice el contador no se separan nunca. El gato del coche
se calcula entero: VM = 2πR/paso = 314, fuerza 32 N (unos 3,2 kg) y **31,4 metros de mano
para 10 cm de coche**. Ese número ridículo es el remate del tema.

**Piñón-cremallera.** Mismo módulo y mismos dientes que la cremallera que ya asomaba al final
de la sesión 3 (m = 4 mm, z = 12 → 150,8 mm por vuelta), para que el alumno reconozca el
dibujo. Lo nuevo aquí es la escala en milímetros y el contador de recorrido.

**Plantilla de engranajes (sesión 5).** No es un adorno: es **la herramienta de la práctica**.
Eliges módulo (4/5/6) y dientes (6-30 y 6-48) y te da, calculados, los dos radios del compás,
el ángulo entre dientes, el paso y la **distancia entre centros**, que es donde van las
chinchetas. La escala del dibujo se recalcula para que las dos ruedas quepan siempre.

**La máquina entera (sesión 6).** Dos etapas de transmisión encadenadas (directo, dos
reductores, sin fin 1/40, multiplicador) y cuatro salidas (eje, cremallera, tornillo, biela).
Calcula rpm, avance o carrera, factor de fuerza y el producto. El producto sale **1** siempre,
y eso es el tema entero en un número.

**El test.** Doce preguntas, cuatro opciones. Al corregir marca la elegida y la correcta,
despliega la explicación de cada una, da la nota sobre 10 y **dice a qué sesiones volver**
contando los fallos por sesión. Avisa de las que se hayan dejado en blanco y se puede repetir.

---

## Decisiones que he tomado, y por qué

### 1. En la sesión 5 no hay micro:bit, y es a propósito

El encargo daba a elegir («micro:bit… o simplemente cartón»). He ido a **cartón**:

- Lo que se quiere medir es la relación de transmisión **contando dientes y contando
  vueltas**. Contar vueltas a mano es exactamente la medida que hay que hacer; meter una
  placa en medio no la mejora, la esconde.
- Las formas fiables de que un micro:bit cuente vueltas necesitan **hardware que no he podido
  probar** (un imán pegado a la rueda y el magnetómetro, o una chincheta cerrando contacto
  contra papel de aluminio en P0). Con 30 alumnos y sin haberlo montado nunca, eso es
  media clase perdida en depurar contactos.
- Y el cartón cuesta **0 €**, que es lo que pedía el encargo.

Si se quiere micro:bit en el tema, el sitio natural es la **sesión 6 como ampliación**, y
habría que probarlo con la placa delante antes de escribirlo.

### 2. Las fotos: licencia comprobada **y** mirada

Tres nuevas. Las tres verificadas contra la API de Commons el 17-sep-2026 **y abiertas y
miradas** (el encargo avisaba de que los títulos engañan):

| Clave | Fichero | Licencia | Autor | Qué es, mirándola |
|---|---|---|---|---|
| `biela` | `u5-biela-locomotora.jpg` | CC BY 3.0 | Abderitestatos | Bajos de la locomotora Ec 4/5 n.º 11 (1911). Se ve la cadena entera: cilindro → vástago → biela → muñequilla fuera del centro de la rueda. Es la mejor foto posible para esta sesión |
| `levas` | `u5-arbol-levas.jpg` | CC BY 4.0 | Elmschrat | Dos árboles de levas en vitrina (Museo de la Industria de Chemnitz). Las levas están **giradas distinto** entre sí, que es el detalle que explica el pie |
| `linterna` | `u5-rueda-linterna.jpg` | Dominio público (HABS/NPS) | Historic American Buildings Survey | Engranaje de madera de un molino de Long Island: rueda con dientes postizos + linterna de barrotes. Es literalmente lo que van a hacer con cartón |

Se sirve la **versión reducida que genera la propia Commons** (`thumburl`, 1920 px), no un
recorte mío, para no tener que declarar obra derivada por haberla escalado. Excepción: la del
molino venía en PNG de 1,3 MB; como es **dominio público**, se ha recodificado a JPEG (266 kB).

⚠️ **Se ha corregido el aviso de licencia de esta página.** `tema0_base.py` fabrica, para
todas las unidades, la frase *«Dos son de dominio público por su antigüedad»*. Con estas tres
ya no cuadra: son **tres** de dominio público y una lo es por ser obra de un organismo
público de EE. UU., no por su edad. La frase se sustituye **solo en la página del tema 5**,
desde `u5_build.py`, para no tocar un fichero que comparten las siete unidades. Va con un
`assert`: si el molde común cambia, el generador **falla a gritos** en vez de publicar una
frase falsa. **Convendría arreglarlo en el molde y quitar el parche.**

### 3. Los vídeos: verificados de nombre, **no vistos**

El de la sesión 4 es **`Dyee1JVYsd0`, «La biela - manivela (mecanismo de transformación)», de
TECH LAPSE** — el mismo profesor que los de la palanca y los engranajes, así que usa el mismo
vocabulario que la unidad. Va con `visto=False`: **nadie del proyecto lo ha visto entero.**

⚠️ **Las duraciones de los tres vídeos anteriores estaban mal.** Decían «unos 4, 4 y 5
minutos» y no lo son. Medidas cargando cada vídeo en el reproductor de YouTube (IFrame API,
`getDuration`):

| Clave | ID | Ponía | Es |
|---|---|---|---|
| `palanca` | `8fDOm-XJBOQ` | unos 4 minutos | **2:00** |
| `poleas` | `AlAxnplUNH0` | unos 4 minutos | **7:33** |
| `engranajes` | `0pO6cHi3HzE` | unos 5 minutos | **2:19** |
| `biela` | `Dyee1JVYsd0` | — | **2:16** |

Corregidas en la tabla `VIDEOS`. La de poleas importa para el minutado: son 7 minutos y medio,
no 4, y eso es un tercio del bloque de teoría.

### 4. La sesión 5 no lleva vídeo, y la 6 tampoco

El encargo pedía vídeo «**cuando aporte algo**». La 5 es de taller: lo que hay que mirar es la
plantilla de la escena, que da los números con los que se traza. Y la 6 es repaso y test.
Busqué vídeo de engranajes de cartón y lo que hay es TikTok y Pinterest, nada citable.

### 5. La geometría, calculada

Todo lo que tiene proporciones está resuelto, no puesto a ojo. Además del detalle de la biela
corta de arriba:

- En la **plantilla**, las proporciones del diente son las normalizadas (cabeza = 1 módulo por
  fuera de la primitiva, pie = 1,25 hacia dentro) y la rueda conducida gira a `−ang·z1/z2` con
  el desfase que mete un diente de la motriz en un hueco de la otra.
- Las dos etiquetas `z1`/`z2` van en una **línea común arriba, con guía punteada**: puestas
  cada una sobre su rueda, la de la pequeña se monta sobre la grande en cuanto los tamaños se
  separan.
- ⚠️ **El perfil del diente es un trapecio radial, no una evolvente**, aquí igual que en las
  escenas 1-3. Es correcto en radio, número de dientes y sentido de giro, pero **no es un
  plano de taller**. La sesión 5 lo dice dentro del bloque de libreta, y lo aprovecha: los
  dientes de cartón van a dar trompicones, y ese trompicón *es* el problema que resuelve la
  evolvente.

### 6. Móvil: los rótulos de los SVG crecen un 20 % largo

Descubierto midiendo con el navegador a 380 px de ancho: Chromium redondea hacia arriba el
cuerpo de letra de los `<text>` de un SVG escalado, así que un rótulo que cabe en el portátil
**sale cortado en el móvil** (el `<svg>` recorta por defecto lo que se sale del viewBox).

Todos los rótulos de la unidad se han apretado hasta que caben a 380 px, y de paso se ha
arreglado **un solape que ya estaba en la sesión 3** (los dos rótulos del tornillo sin fin
visto por el extremo iban a 13 px y se montaban; ahora van a 18). `u5_verifica.py` mide las
ocho escenas a 1200 px **y a 380 px**.

ℹ️ **Lo que NO he tocado:** a 380 px el documento entero mide 440 px de ancho y se puede
arrastrar de lado. Pasa **igual en los temas 3, 4, 6 y 7**, que no he escrito yo, así que es
del molde común y no de esta unidad. Lo dejo apuntado.

### 7. El CSS del test se inyecta, no se mete en el molde

Igual que se hace con el del narrador: `CSS_TEST` entra desde `u5_build.py` en el `<style>` de
esta página. El molde `tema0_base.py` lo comparten las siete unidades y esto solo lo usa la
sesión 6. El tinte de acierto/fallo va en `rgba()` de los hexadecimales de marca y no en
`color-mix`, para que funcione también en navegadores viejos de aula; se ha comprobado en
**claro y en oscuro**.

### 8. La coma decimal

Los números de las escenas salen con **punto** decimal (`0.500`, `150.8`), porque es lo que ya
hacían las escenas 1 a 3 y he preferido que la unidad sea coherente consigo misma. La nota del
test sí va con coma (`10,0 sobre 10`), porque es una nota escolar. **En español lo correcto es
la coma en los dos sitios**: si se quiere cambiar, hay que hacerlo en las ocho escenas a la
vez, no solo en las mías. Lo dejo señalado en vez de dejar la unidad a medias.

---

## El fallo que cazó la verificación

El cruce de números detectó que la **leva de programa** empezaba a media caída en vez de abajo.
La causa es fina y merece quedar escrita: el seguidor toca la leva en el ángulo `−90° − φ`, o
sea que **según gira, va recorriendo el perfil hacia atrás**. Escrito el perfil en `α` a secas,
el programa se ejecutaba del revés: la leva *subía de golpe y caía despacio*, justo lo
contrario de lo que decía su propio texto («sube despacio, se queda arriba, cae de golpe»).
Se mide `g` desde la posición de contacto inicial y ya coinciden dibujo, gráfica y texto.

Sin abrir el navegador esto no se ve: el dibujo era una leva perfectamente válida.

---

## Lo que no me cuadra (y no me he inventado)

### 1. El número de la unidad — **sigue sin resolverse**

El informe anterior ya lo levantó y nadie lo ha decidido. `CURRICULO.md` dice que Mecanismos es
la **U7** del libro y que la U5 son *Materiales de uso técnico (II)*; el aviso del propio
`CURRICULO.md` explica que **la web va con otra numeración** y que `tema5 → U7 Mecanismos`. O
sea que **la web está bien** y la tabla de abajo del documento («U5 Materiales») es la que
confunde, porque mezcla números de libro y números de web en la misma columna. Sigo llamándolo
tema 5 porque es lo que manda para el alumno y lo que dice el mapa, pero **alguien debería
limpiar esa tabla**.

### 2. Los chips curriculares

He puesto los mismos que las sesiones 1-3, **`CE1 · 1.2` y `CE3 · 3.1`**, por coherencia dentro
de la unidad. Pero, siendo estrictos con `CURRICULO.md`, a la U7 le toca **solo el 3.1**: el
1.2 está mapeado a U1·U3·U4·U5. El 1.2 («entender cómo funcionan las cosas antes de
construir») describe bien lo que hacen estas sesiones, así que no lo he quitado, pero **es una
decisión del autor, no mía**. Se cambia en `CHIPS` y se regenera.

Sigo sin poner chips de **saberes**: el criterio 3.1 remite a `A.4 · A.5 · A.6` y
`CURRICULO.md` dice que A.1 a A.5 están *pendientes de transcribir de la diapositiva 11*. No
cito lo que no sé.

### 3. La lectura del tema no cubre las sesiones 4, 5 y 6

`generadores/u5_lectura.py` (30 párrafos + 10 preguntas) es de palanca, poleas y engranajes.
No la he tocado porque el encargo pedía las tres sesiones, pero **la unidad ya no acaba en los
engranajes**: le faltan la transformación del movimiento y el módulo. Son unos 8-10 párrafos
más y 2-3 preguntas. Dime y lo hago.

### 4. El taller de 30 minutos: es apretado, y no lo he probado con cartón

Trazar con compás y transportador, recortar y montar, en 30 minutos, con 13 años. Las cuentas
del material sí están hechas:

- Con **módulo 6**, la rueda de 24 dientes mide **156 mm de diámetro exterior**: cabe en un A4
  (210 mm). La de 36 mediría 228 y **no cabría**; por eso la escena avisa y por eso la tercera
  rueda del tren es otra de 12.
- El tren de tres (12 – 12 – 24) ocupa unos **32 cm** de base entre los extremos: sirve una
  cara de caja de cartón.
- El diente mide 9,4 mm de ancho en la primitiva y 13,5 mm de alto: recortable con tijeras en
  cartón de caja, pero **hay que probarlo**.

Mi apuesta es que cada alumno traza y recorta **una sola rueda** (por eso van en parejas) y que
aun así irá justo. **Si en clase se queda corto**, lo que sobra es el paso 7 (la rueda loca):
está al final justamente para poder soltarlo.

### 5. Dos datos que doy por buenos

- **James Pickard patentó la manivela con volante en 1780** y Watt tuvo que rodear la patente
  con el engranaje *sol y planeta* (de su empleado William Murdoch, patentado por Watt en
  1781) hasta que la de Pickard caducó en **1794**. Contrastado en varias fuentes secundarias,
  no en la patente original.
- El **aserradero de Hierápolis** (siglo III) como máquina más antigua conocida con biela y
  manivela, por su relieve. Es lo que sostiene la bibliografía habitual; no he visto el
  relieve.

Los dos están en un bloque `SOLO PARA ENTENDERLO`, no en lo que se copia.

### 6. Las respuestas del test están en el código de la página

`data-ok` viaja en el HTML. Es una **autoevaluación** —la idea es que se use en casa y se
corrija sola—, no un examen; la propia sesión lo dice («la nota de aquí no cuenta para nada»).
Para examen no vale, y no hay forma de que valga sin un servidor.

---

## La red de seguridad que queda montada

`generadores/u5_verifica.py` — **sale 0 si todo va bien**:

```bash
~/venv/bin/python generadores/u5_build.py
~/venv/bin/python generadores/u5_verifica.py
```

Comprueba, en este orden: errores de JavaScript, ids repetidos y `getElementById` huérfanos;
las seis sesiones con sus cuatro bloques y sus bloques de libreta; que las seis fotos cargan
grandes y que el vídeo no se carga hasta pulsarlo; **la maquetación de las ocho escenas en
todos sus estados, a 1200 px y a 380 px**; **los números de las cinco escenas nuevas contra la
cuenta hecha en Python**; y el test entero (nota, desglose por sesión, aviso de preguntas en
blanco y botón de reiniciar).

Hoy pasa entero. Es la misma idea de `u7_verifica.py`, que dejaba dicho que servía de red a
quien escribiera estas sesiones: la ha hecho.

---

## Checklist para el humano, antes de publicar

**Imprescindible:**

1. `~/venv/bin/python generadores/u5_build.py` y `git diff` vacío. `u5_verifica.py` en verde.
2. **Ver los cuatro vídeos enteros** y poner `visto=True` solo a los que aporten. Hoy los
   cuatro salen publicados (título y canal verificados) pero **nadie los ha visto**.
3. Decidir lo de los chips (punto 2 de «lo que no me cuadra»).
4. **Hacer el taller de la sesión 5 con cartón de verdad** y cronometrarlo antes de llevarlo a
   clase. Es lo único de esta entrega que no se puede verificar desde un teclado.

**Conviene:**

5. Ampliar la lectura a las sesiones 4-6, o decidir que se queda como está.
6. Quitar el parche del aviso de licencia arreglándolo en `tema0_base.py`.
7. Decidir si se pasa toda la unidad a coma decimal (punto 8 de «decisiones»).
8. Mirar el ancho de 440 px en móvil, que es del molde común y afecta a los cinco temas.

---

## Ficheros tocados

Nuevos:

```
generadores/u5_escenas2.py     las cuatro escenas nuevas y el test, con su CSS
generadores/u5_verifica.py     la red: navegador, maquetacion y cruce de numeros
img/u5-biela-locomotora.jpg    CC BY 3.0
img/u5-arbol-levas.jpg         CC BY 4.0
img/u5-rueda-linterna.jpg      dominio publico
INFORME.md                     esto
```

Modificados:

```
generadores/u5_build.py        sesiones 4, 5 y 6; fotos; video; duraciones corregidas
2eso/TyD/tema5/index.html      la pagina, regenerada
2eso/TyD/index.html            la tarjeta del tema 5: de «3 de 6» a «6 de 6»
```

No se ha tocado ningún fichero de otra unidad, ni el molde común (`tema0_base.py`,
`unidad_base.py`). Los tres cambios en la sesión 3 —la separación de dos rótulos del tornillo
sin fin y las duraciones de los vídeos— son de esta unidad y están explicados arriba.
