# Informe · 4.º de ESO · Tema 9 · Tecnología y sociedad: proyectos de servicio

Rama `c9`. Entregadas las **cuatro primeras sesiones** de ocho; las otras cuatro
quedan en la barra con su título y el botón desactivado.

---

## Qué hay entregado

| Fichero | Qué es |
|---|---|
| `4eso/Tecnologia/tema9/index.html` | La unidad. 194 KB, generada. |
| `4eso/Tecnologia/tema9/lectura-tema9.pdf` | Lectura de aula: 30 párrafos numerados + 10 preguntas, 4 páginas A4. |
| `generadores/c9_build.py` | El generador de la página. |
| `generadores/c9_escenas.py` | Escenas de las sesiones 1 y 2. |
| `generadores/c9_escenas2.py` | Escenas de las sesiones 3 y 4. |
| `generadores/c9_lectura.py` | El PDF de la lectura. |
| `generadores/c9_verifica.py` | Verificador: **99 comprobaciones, 0 fallos**. |
| `generadores/c9_fotos.py` | Consulta la licencia en Commons y baja las cuatro fotos. |
| `generadores/c9_capturas.py` | Recorta cada escena a PNG, para mirarlas. Admite el ancho: `… 420` para el móvil. |
| `generadores/c9_mirada.py` | Captura la página entera de cada sesión. |
| `generadores/guion_c9.txt` | Guion de la voz. |
| `generadores/voz.py` | **Recuperado**, ver más abajo. |
| `audio/c9-sociedad.mp3` + `_env_c9-sociedad.json` | Voz (1 min 46 s) y su envolvente. |
| `img/c9-*.jpg` | Las cuatro fotos de Commons. |

**No he tocado `4eso/Tecnologia/index.html`.**

## Cómo se ejecuta

```
~/venv/bin/python generadores/c9_build.py        # la página
~/venv/bin/python generadores/c9_lectura.py      # el PDF
~/venv/bin/python generadores/c9_verifica.py     # 99 comprobaciones
~/venv/bin/python generadores/c9_capturas.py     # PNG de cada escena en /tmp/c9/
~/venv/bin/python generadores/c9_capturas.py 420 # lo mismo, a ancho de móvil
```

---

## Lo primero: una cosa que NO me cuadra, y que decides tú

**La sesión 3 se sale de los criterios que me diste.** El encargo dice
`CE2 · 2.1 · CE6 · 6.1 · 6.2 · 6.3`, y `CURRICULO.md` asigna a la U9 exactamente
`2.1 · 6.1 · 6.2 · 6.3`. Pero «presentar y defender el proyecto ante otra gente»
es literalmente la **CE3** (criterios 3.1 y 3.2), que en el mapa inverso vive en
las unidades 1 y 2, no aquí.

No he quitado la sesión, porque tu propuesta la pedía y porque cierra el curso
donde toca. Lo que he hecho es **girarla hacia los criterios que sí son de esta
unidad**: la rúbrica de la defensa no evalúa oratoria, evalúa **impacto**. De
los 10 puntos, **6,5 son de 6.1, 6.2 y 6.3** (a quién le sirve, la medida
propia, el impacto calculado, lo que falla) y **2,0 son de 2.1** (el aparato
terminado, funcionando delante del jurado). El indicador «cómo lo montamos, paso
a paso» **vale 0**, y eso es el contenido de la sesión.

Aun así, si quieres que los chips digan `CE3 · 3.1` en la S3, es cambiar una
línea. **Lo dejo señalado en vez de decidirlo yo.**

Segunda cosa menor del currículo: **los saberes de 4.º no están transcritos en
`CURRICULO.md`** (el bloque que hay, A.1 a E.2 con texto, es el de 2.º). He
puesto los chips `A.2`, `D.1`…`D.4` copiando los códigos de la tabla de
criterios, pero **no sé qué dice cada uno**. Si al transcribirlos no encajan,
son cuatro chips que cambiar.

---

## El hilo de las cuatro sesiones

Cambié poco de tu propuesta: el orden es el tuyo y los cuatro títulos también.
Lo que sí decidí es **dónde cae el peso de cada una**, y en dos de ellas no es
donde parecía:

| S | Lo que abre | La cuenta que la sostiene | Lo que deja abierto |
|---|---|---|---|
| 1 | De 1.393 medicamentos nuevos, 16 | precio mínimo = desarrollo ÷ (personas × años) | Vale, eso no se fabrica. ¿Y lo que sí se fabricó y no sirvió? |
| 2 | La PlayPump, con sus siete fechas | horas = (personas × litros) ÷ caudal | Ya sé si sirve y a quién. Ahora que se entere alguien. |
| 3 | Seis minutos y tres desconocidos | nota = Σ peso × nivel/3, con el tiempo de tope | Falta la pregunta peor: ¿compensa? |
| 4 | ¿Cuándo devuelve lo que costó? | saldo(t) = ahorro × t − coste | — (cierra el curso) |

**La S1 lleva un segundo mecanismo que no estaba en tu propuesta y que creo que
es el que más les va a doler**: no solo «no se fabrica lo que no da dinero», sino
**«quien decide no es quien lo sufre»**. El ejemplo es su propio instituto: un
medidor de CO₂ de aula existe y cuesta 120 €, y el alumno que aguanta el aula
cargada no compra nada ni está en la mesa donde se decide. La actividad de la S1
les hace contar las aulas del centro, multiplicar, y averiguar **el cargo
concreto** que tendría que firmar eso.

**La S2 no va de la PlayPump**: la PlayPump es el gancho (diez minutos). El
cuerpo es el **balance de energía de sus tres proyectos en tres sitios**, y el
resultado que enseña es que en un aparato a pilas **el consumo no es del
actuador, es de la placa esperando**: la bomba del riego se lleva 0,03 Wh al día
y la placa 5,40. El 99 %.

**La S4 da resultados incómodos a propósito, y los tres son verdad.** Lo digo
aquí porque es lo que un humano tiene que revisar antes de llevarlo a clase:

- La lámpara con una bombilla **LED de 9 W** tarda **233 años** en devolver lo
  que costó. La misma lámpara sobre un **halógeno de 50 W** encendido seis horas
  de más lo devuelve en **6,4**.
- El riego ahorra **490 litros al año** y **0,68 €**. En litros sí; en euros,
  no, porque el agua en España es barata. Las dos frases son ciertas.
- El aviso de ventilación **da números rojos**: ventilar cuesta calefacción
  (0,75 kWh por renovación de un aula, 528 kWh al curso con cuatro al día), y lo
  que da a cambio no se mide en euros.

Esa es la lección de cierre: **hay impactos que no se pueden sumar**, y **el
impacto depende de la escala y del sitio**. No es un error de la unidad que las
cuentas salgan mal: es lo que se quiere enseñar. Pero conviene que lo sepas
antes de que un grupo te diga «entonces nuestro proyecto no vale para nada», que
lo van a decir. En la S4 está escrito el contraargumento.

---

## Las cuatro sesiones pendientes: he puesto títulos

Aparecen desactivadas pero con título, para que se vea la forma entera. Mi
propuesta, encadenada con lo escrito:

| S | Título corto | Qué resuelve | Qué deja abierto |
|---|---|---|---|
| 5 | El ciclo de vida completo | La cuenta que la S4 deja a medias: la energía y los minerales de fabricar la placa. Análisis de ciclo de vida de verdad. | Ya sé lo que cuesta. ¿Y si no puedo usarlo? |
| 6 | Diseñar para todo el mundo | Accesibilidad: el aparato para quien no ve, no oye o no puede apretar. Se rediseñan los tres proyectos. | ¿Y cuando se tira? |
| 7 | Dónde acaba cuando se tira | Residuo electrónico, derecho a reparar, y qué pasa con su propio prototipo en junio. | Ya está todo. A defenderlo. |
| 8 | La defensa de verdad | La defensa real ante gente de fuera, con la rúbrica de la S3 y el test de toda la unidad. | — |

**El test está en la S4, no en la S8.** El encargo pide «el test de la última
sesión», y la última es la 8, que está pendiente. He puesto uno de 10 preguntas
al final de la S4, titulado «lo que tiene que haber quedado de **estas cuatro
sesiones**». Cuando se escriban las otras cuatro, lo suyo es dejar este donde
está y añadir otro al final. **Esto lo decides tú.**

---

## Las escenas: qué calcula exactamente cada una

Ninguna enseña un número que no salga de una cuenta. El verificador rehace cada
cuenta **en Python y a partir de la definición**, no copiando el JavaScript, y
las compara.

**S1 · «La cuenta que decide qué se fabrica».** Seis problemas, cada uno con
personas afectadas, lo que puede pagar cada una y lo que cuesta desarrollarlo.
Calcula el **precio mínimo** (`desarrollo ÷ (atendidas × años)`), lo compara con
lo que puede pagar quien lo sufre, y de ahí el beneficio esperado. Tres mandos:
alcance, años de exclusiva y **dinero público por persona y año**, que es el que
enseña las cuatro salidas del §«cuatro maneras de arreglarlo».

Las barras van en **escala logarítmica con signo**, rotulado («cada raya
multiplica por diez»), porque los casos se llevan cinco órdenes de magnitud: de
−276 M€ a 59.000 M€. En lineal solo se vería una barra.

Y lo que es la sesión entera: el botón **«ordenar por personas atendidas»**
cambia el orden. El verificador comprueba que los dos órdenes **no coinciden**
con los valores de partida; si alguien toca los datos y pasan a coincidir, el
verificador falla, que es lo que quiero.

**S2 · «¿Aguanta aquí?», dos modos.**
- *El columpio*: `horas = (personas × litros) ÷ caudal`. Con lo que prometía el
  folleto (2.500 personas, 1.400 L/h, 10 L por persona) salen **17,9 h/día**, que
  todavía caben en el día. Bajando el caudal al que se midió de verdad, **27,2 h**,
  que no caben. Dibuja además cuántos niños harían falta girando a la vez.
- *Tu proyecto en tres sitios*: `Wh = V × A × horas`, con tres proyectos, tres
  sitios (enchufe / panel de 5 W / cuatro pilas AA), casilla de «la placa duerme»
  y casilla de módulo de wifi. Saca el consumo diario, el porcentaje que se lleva
  la placa, y la autonomía o el coste anual en euros según el sitio.

**S3 · «Reparte los seis minutos».** La rúbrica viva: siete filas con su peso
(suman 10), los segundos que le das a cada una y el nivel que quieres enseñar.
Calcula el **nivel que el tiempo sostiene**, corta a los 360 s en el orden en que
se presenta, y saca la nota. Dice además **la mejora más rentable** (peso ×
niveles que faltan) y **el minuto peor gastado** (puntos por minuto).

Los dos guiones de ejemplo, con el mismo proyecto y los mismos seis minutos:
**4,17** el de siempre (cuatro minutos de «cómo lo montamos», que vale 0) y
**9,67** el reparto por peso.

**S4 · «¿Cuándo devuelve lo que costó?».** `saldo(t) = ahorro × t − coste`,
dibujado como recta con el cruce por cero marcado. Coste fijo (60 €) separado
del coste por unidad (25 €), para que la **escala** se note: con 200 aparatos el
retorno de la lámpara-halógeno baja de 6,4 a 1,9 años, y **nunca por debajo de
1,9**, porque cada aparato cuesta 25 € (el verificador comprueba ese tope).

---

## Dos fallos que encontré y arreglé, y que le pueden pasar a otra unidad

1. **`display:flex` de una clase le gana al atributo `hidden` del navegador.**
   La fila de «la bombilla es 9 / 20 / 50 W» de la S4 se seguía viendo con los
   proyectos A y B, porque `.q4-fila{display:flex}` tiene más especificidad que
   la regla `[hidden]{display:none}` del navegador. Arreglado con
   `.q4-fila[hidden]{display:none}`. **El verificador ahora mira el `display`
   calculado, no el atributo**, que es la única manera de cazarlo.

2. **Rehacer una tabla con `innerHTML` desde el evento de un `input` que está
   dentro revienta.** La rúbrica de la S3 se redibujaba entera en cada cambio, y
   el navegador tenía que arrancar el `<input>` que el alumno estaba usando en
   mitad de su propio evento: `Failed to set the 'innerHTML' property […] The node
   to be removed is no longer a child of this node`. Ahora la tabla **se monta una
   vez** y solo se reescriben las celdas que cambian. Tres escenas más de esta
   unidad montan sus mandos una sola vez por el mismo motivo: si se reconstruyen
   en cada `input`, el deslizador desaparece a mitad del arrastre.

Y un error mío, de aritmética, que cazó el verificador: había escrito en el
texto que el reparto por peso sacaba **8,67** y saca **9,67**. Sumé mal a mano.
Está corregido en los cuatro sitios donde salía, y ahora el verificador comprueba
que el número del texto y el que calcula la escena son el mismo.

---

## Las fotos

Las cuatro son de Wikimedia Commons, con la licencia consultada por la API
(`generadores/c9_fotos.py`) **y la imagen abierta y mirada una a una**.

| Sesión | Fichero | Qué se ve | Autor | Licencia | Tamaño |
|---|---|---|---|---|---|
| 1 | `c9-mosquitera.jpg` | Niños durmiendo bajo una mosquitera tratada | HarunaSylvester | CC BY-SA 4.0 | 3840×2160 → 1280 |
| 2 | `c9-olla-barro.jpg` | Mercado de Ouahigouya (Burkina Faso), con una olla de barro refrigeradora en primer plano | Peter Rinker | CC BY-SA 3.0 | 2112×2816 → 1280 |
| 3 | `c9-defensa.jpg` | Un alumno de Nivín (Perú) presentando una maqueta en una feria de ciencia, 2018 | Escuela de Nivín | CC BY-SA 4.0 | 1280×960 |
| 4 | `c9-repair-cafe.jpg` | Un repair café: gente arreglando una lámpara y un aspirador | Ilvy Njiokiktjien | CC BY-SA 3.0 | 3356×4070 → 1280 |

**Dos cosas que deberías mirar tú:**

1. **La foto de la mosquitera es de niños durmiendo.** Es la que mejor cuenta lo
   que quiero contar (una tecnología barata, sin electrónica, que existe hace
   décadas y tardó en llegar), y el pie no los usa como ilustración de pobreza:
   habla del objeto. Pero es una decisión de tono y te la señalo. Si no te
   convence, hay muchas de reparto de mosquiteras en el mismo lote de búsqueda.
2. **La de la feria de ciencia de Nivín la uso con una pregunta incómoda al
   pie**: «la maqueta es impresionante… si tuviera seis minutos, ¿de qué crees
   que hablaría más, de la maqueta o de a quién le sirve?». El pie deja claro que
   la pregunta no va contra él sino contra todos nosotros, pero **está usando el
   trabajo de un alumno identificable como ejemplo de un error**. Me parece que
   se sostiene y que es honesto; si a ti no te lo parece, se cambia el pie sin
   tocar nada más.

## Los vídeos

Título y canal comprobados por oEmbed el 18-sep-2026. **Nadie los ha visto
enteros**: solo está verificado que el vídeo existe, que se llama como digo y
que es del canal que digo. Antes de ponerlos en clase, míralos.

| Sesión | ID | Título | Canal |
|---|---|---|---|
| 1 | `EydFlOUooN4` | No te olvides de las enfermedades olvidadas (corto documental) | Barcelona Institute for Global Health (ISGlobal) |
| 2 | `wDyCMVmY-Vk` | Cómo esta nevera que no necesita electricidad salvó a una empresa de cerámica india | Insider Español |
| 4 | `sC1HmzxOjoQ` | Análisis de ciclo de vida: definición de objetivos y alcance | Universitat Politècnica de València |

**La sesión 3 se queda sin vídeo a propósito.** Busqué sobre defensa de
proyectos y exposición oral y lo que sale en español es material de coaching o
de canales de motivación, que no pasa el listón del resto de la unidad. Prefiero
dejarlo vacío a meter uno malo. Si conoces alguno bueno, entra en una línea.

El de la S4 (UPV) es **más seco** que los otros dos: es una clase universitaria.
Lo he puesto porque la unidad deja la cuenta del ciclo de vida a medias
explícitamente y ese vídeo enseña cómo se hace en serio, pero para 15 años puede
ser mucho. Míralo antes.

---

## Datos, y de dónde sale cada uno

Todo lo que la unidad afirma como hecho está comprobado el **18-sep-2026**:

- **1.393 medicamentos nuevos entre 1975 y 1999, de los que 16 eran para
  enfermedades tropicales y tuberculosis** (1,1 %): Trouiller, Olliaro, Torreele,
  Orbinski, Laing y Ford, *Drug development for neglected diseases: a deficient
  market and a public-health policy failure*, **The Lancet 359 (2002), 2188-2194**.
  La cita completa está dentro de la página.
- **Paludismo: 282 millones de casos y 610.000 muertes en 2024, en 80 países.**
  Hoja informativa de la OMS.
- **Chagas: unos 8 millones de infectados, más de 10.000 muertes al año**, la
  mayoría en América Latina. Hoja informativa de la OMS.
- **Benznidazol: en uso médico desde 1971**; en 2012 el único productor era un
  laboratorio público del estado de Pernambuco (Brasil).
- **PlayPump**: Ronnie Stuiver la enseña en una feria en **1989**; Trevor Field
  instala las dos primeras en KwaZulu-Natal en **1994**; Mandela inaugura una en
  **1999**; premio del Banco Mundial en **2000**; **16,4 M$** comprometidos en la
  Clinton Global Initiative de **2006**; **1.000 bombas** en **2008**; se deja de
  instalar en **2009**. Promesa del folleto: **2.500 personas por bomba** y
  **hasta 1.400 L/h desde 40 m**. Estimación crítica: **27 horas de juego al día**.
- **Olla de barro (zeer)**: Mohammed Bah Abba, norte de Nigeria, años noventa,
  primeras **5.000 unidades**; **Premio Rolex a la Iniciativa 2001**, 75.000 $;
  se venden a unos **40 centavos de dólar el par**. Solo funciona con aire seco.
- **Tecnología apropiada / intermedia**: E. F. Schumacher, *Lo pequeño es
  hermoso*, **1973**.
- **Renovar el aire de un aula**: 150 m³ × 1,2 kg/m³ × 1.005 J/(kg·K) × 15 K =
  2,71 MJ = **0,754 kWh**. Es física, con las constantes declaradas dentro de la
  escena.

### Lo que NO es un dato verificado, y va rotulado como tal dentro de la página

Esto es lo que más me importa que revises, porque es donde un material como este
se estropea:

1. **Los seis casos de la escena de la S1 son un modelo, no una fuente.** Solo
   dos cifras vienen de la OMS (los casos de paludismo y los infectados de
   Chagas). Lo que puede pagar cada persona, lo que cuesta desarrollar cada cosa
   y las poblaciones de colesterol, calvicie, aulas y huertos son **órdenes de
   magnitud míos**. El pie de la escena lo dice con estas palabras: «esta escena
   no demuestra nada sobre un caso concreto: enseña cómo es la cuenta». **No he
   buscado un coste real de desarrollo de un medicamento porque las cifras que
   circulan están muy discutidas y no quería apoyarme en ninguna.**
2. **Los 45 mA de una placa Arduino Uno entera despierta y los 12 mA con el chip
   dormido no son datos de hoja de características**: son medidas típicas de la
   placa completa, con su regulador y su LED, que es lo que circula. Está dicho
   dentro de la escena y en la sesión, junto al motivo (un ATmega328P pelado baja
   a milésimas de eso, y por eso los aparatos a pilas de verdad no llevan una
   placa Uno). **Si quieres un número medido, habría que medirlo con una placa
   delante.**
3. **La regla que enlaza tiempo y nivel en la rúbrica de la S3** (10 s para
   nombrar, 25 para explicar, 45 para demostrar con un dato) es **criterio
   nuestro**, no del currículo. Está rotulado como tal dentro de la escena. Los
   pesos de la rúbrica también son míos.
4. **Los tres sitios de la S2** (instituto, aldea, huerto a 3 km) son
   inventados; las cuentas que se hacen en ellos, no. También está dicho.
5. **La energía y los minerales que cuesta fabricar la placa no están contados
   en la S4**, y lo digo expresamente en un «solo para entenderlo» y en el pie de
   la escena, con el motivo (no tengo un número fiable) y con lo único que sí se
   puede afirmar: si se contara, el retorno sería **más largo, nunca más corto**.
   Me parece la parte más honrada de la unidad y la que más enseña.
6. Los precios (0,15 €/kWh de luz, 0,10 €/kWh de calefacción, 2 €/m³ de agua) son
   órdenes de magnitud de 2026, declarados en el pie.

---

## La lectura de aula

`lectura-tema9.pdf`, 4 páginas, **30 párrafos justos** (el propio script se niega
a generar si no son 30) y 10 preguntas. Título: *El columpio que sacaba agua*.

Tres casos con fecha, y los tres dicen lo mismo desde un sitio distinto: la
PlayPump (la sesión 2), las enfermedades olvidadas y el benznidazol de 1971 (la
sesión 1), y la olla de barro (el contraejemplo, el que sí encaja).

Las dos últimas preguntas son de opinión razonada, como pide el molde. **La
décima me gusta especialmente y te la señalo**: les pide escribir la división que
haría falta para saber si su proyecto merece la pena, inventarse un número solo
donde no haya manera de conocerlo, y **marcar con un asterisco todos los números
inventados**. El ejercicio no es calcular: es distinguir.

Conviene hacerla **entre la sesión 1 y la 2**, no al final, porque cuenta con
detalle los dos casos que salen después. Está dicho en el recuadro de la S1.

---

## Comprobado

- `~/venv/bin/python generadores/c9_verifica.py` → **99 comprobaciones, 0 fallos**.
  Sin errores de página ni de consola antes ni después de pulsarlo todo.
- Las **14 tomas** de `c9_capturas.py` miradas una a una a 1200 px, y las mismas
  a **420 px** para comprobar que en un móvil no se rompe nada. La tabla de la
  rúbrica se desplaza en horizontal en pantalla estrecha, pero la nota final sale
  en el texto de debajo, así que no se pierde.
- Las **cuatro fotos** las carga el navegador (`naturalWidth > 0`) y existen en
  `img/`.
- **Ningún `id` empieza por `ses-`** salvo los ocho paneles de sesión: es la
  comprobación que la unidad c6 recomendó copiar, y aquí está copiada.
- El **test** corrige bien: 0 de 10 sin contestar y 10 de 10 marcando por
  `data-ok`.

---

## Qué debería mirar un humano

1. **Si la sesión 3 se queda aquí o se va a la CE3.** Es lo primero de este
   informe y es tu decisión, no mía.
2. **Los saberes de 4.º no están transcritos en `CURRICULO.md`**: los chips
   `A.2` y `D.1`…`D.4` son códigos copiados de la tabla, sin texto detrás.
3. **Los tres vídeos, enteros.** Y decidir si el de la UPV es demasiado seco.
4. **El pie de la foto de la feria de Nivín**, que usa el trabajo de un alumno
   identificable como ejemplo de un error común.
5. **La foto de los niños bajo la mosquitera**, por tono.
6. **Que las cuentas de la S4 salen mal a propósito** y que en clase van a decir
   «entonces esto no vale para nada». El contraargumento está escrito, pero es
   una conversación que conviene llevar preparada.
7. **Dónde va el test** (ahora en la S4, cubriendo solo lo escrito).
8. Si los **45 mA / 12 mA** de la placa te parecen demasiado concretos para
   afirmarlos sin haberlos medido.

## Lo que no he hecho

- Las sesiones 5 a 8 (el encargo pedía las cuatro primeras).
- La tarjeta en `4eso/Tecnologia/index.html`, que la pones tú al recoger.
- **`generadores/voz.py` no estaba en esta rama** y lo he vuelto a poner tal cual
  está en el commit `83ebf20`, sin cambiarle nada. Le pasó lo mismo a la unidad
  c6 y su informe ya lo señalaba: **hay copias idénticas en varias ramas y
  ninguna en `main`**. Sigue sin decidirse dónde vive.
