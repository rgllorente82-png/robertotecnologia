# Informe · 4.º de ESO · Tema 8 · Sostenibilidad y accesibilidad

Rama `c8`. Entregadas las **cuatro primeras sesiones** de ocho; las otras cuatro
quedan en la barra con su título y el botón desactivado.

> **Dónde está este informe.** El encargo pedía `INFORME.md`. Lo he puesto en
> `generadores/INFORME-c8.md`, que es donde están los once informes anteriores
> (`INFORME-c4.md`, `INFORME-c5.md`, `INFORME-c6.md`…). Si prefieres la raíz, se
> mueve en un segundo.

---

## Qué hay entregado

| Fichero | Qué es |
|---|---|
| `4eso/Tecnologia/tema8/index.html` | La unidad. 212 KB, generada. |
| `4eso/Tecnologia/tema8/lectura-tema8.pdf` | Lectura de aula: 30 párrafos numerados + 10 preguntas, 4 páginas A4. |
| `generadores/c8_build.py` | El generador de la página. |
| `generadores/c8_escenas.py` | Escenas de las sesiones 1 y 2. |
| `generadores/c8_escenas2.py` | Escenas de las sesiones 3 y 4. |
| `generadores/c8_lectura.py` | El PDF de la lectura. |
| `generadores/c8_verifica.py` | Verificador: **196 comprobaciones, 0 fallos**. |
| `generadores/c8_fotos.py` | Consulta la licencia en Commons y baja las cuatro fotos. |
| `generadores/c8_busca.py` | Rastreo de candidatas en Commons (herramienta de trabajo). |
| `generadores/c8_capturas.py` | Recorta cada escena en sus estados **extremos**, que es donde se rompen los dibujos. |
| `generadores/c8_mirada.py` | Captura la página entera de cada sesión. |
| `generadores/guion_c8.txt` | Guion de la voz. |
| `audio/c8-sostenible.mp3` + `_env_c8-sostenible.json` | Voz (2 min 03 s) y su envolvente. |
| `img/c8-*.jpg` | Las cuatro fotos de Commons. |
| `generadores/voz.py` | Recuperado (ver más abajo). |

**No he tocado `4eso/Tecnologia/index.html`.** Ese fichero ya existe en `main`
(el informe de la c6 decía que no; se creó después).

---

## Cómo se ejecuta

```
~/venv/bin/python generadores/c8_lectura.py     # el PDF, primero: la página lo enlaza
~/venv/bin/python generadores/c8_build.py       # la página
~/venv/bin/python generadores/c8_verifica.py    # 196 comprobaciones
~/venv/bin/python generadores/c8_capturas.py    # PNG de los estados extremos, en /tmp/c8/
~/venv/bin/python generadores/c8_mirada.py      # la página entera de cada sesión
```

El orden importa: `unidad_base.lectura()` solo pone el enlace al PDF si el PDF
ya está en la carpeta.

---

## Decisiones, y por qué

### 1. `voz.py` tampoco estaba en esta rama

Igual que le pasó a la c6. No está en `main` ni en la cadena de `c8`; existe en
el commit `83ebf20` (rama `tema7`). Lo he vuelto a poner tal cual, sin cambiarle
una línea.

**Para mirar:** van dos unidades seguidas teniendo que rescatar la misma
herramienta de una rama que nadie ha mezclado. O se mezcla `tema7`/`tema8` en
`main`, o se decide dónde vive `voz.py` y se pone ahí de una vez.

### 2. Las cuatro sesiones: mantengo las cuatro y el orden, con dos cambios de foco

La propuesta estaba bien y la cadena funciona. Lo que he cambiado es **dónde
empieza** cada una, para que ninguna abra por la definición:

- **S1.** La propuesta decía «huella de carbono con datos citados». Eso, solo,
  es una sesión de tabla. La he montado al revés: el alumno **ordena cuatro
  acciones antes de saber nada**, se equivoca, y solo entonces aparece la
  unidad. Y el fallo no se le echa en cara: se le enseña que está **medido** que
  casi todo el mundo falla (Attari y otros, *PNAS*, 2010, 505 personas, se
  quedan cortos por un factor de 2,8 de media).
- **S4.** La propuesta decía «cuánto consume de verdad lo que has montado». La
  abro con **una apuesta escrita**: nueve días con una pila de 9 V. La respuesta
  son **menos de seis horas**, y ese factor 40 de error es el que abre la
  sesión. Sin la apuesta escrita antes, el número no impresiona a nadie.

Las S2 y S3 van como se proponían. En la S2 he añadido una cosa que no estaba
en el encargo y que me parece la clave de la sesión: **la rampa añadida al final
no cabe, y eso se demuestra con una división**. 18 cm al 8 % son 2,25 m de
rampa, más 1,50 m libres en cada punta: 5,25 m de pasillo. No hace falta ningún
sermón, hace falta el número.

### 3. El proyecto del curso: no me he casado con ninguno

Cada vez que hace falta un caso concreto salen **dos o tres** de los cinco de
`PROYECTOS.md`:

- **S1**, el reto y la práctica: el aula, y el aparato de cada grupo sin
  nombrarlo.
- **S2**, la caja en la pared: vale para los cinco, porque los cinco tienen una
  caja y un mando. El proyecto 4 (barrera) es el que más se beneficia, porque en
  el catálogo su impacto declarado **es literalmente** la accesibilidad.
- **S3**, los tres casos a clasificar: auriculares, impresora y router, más el
  aparato propio del grupo.
- **S4**, la escena trae las piezas de los cinco: sonda de humedad de suelo (1),
  DHT11 (2), ultrasonidos (3), servo SG90 (4), LED y módulo wifi (5 y 2).

**Donde sí he tenido que elegir:**

- La **bomba** del proyecto 1 no está en la lista de piezas de la escena de la
  S4. El servo SG90 en movimiento (250 mA) cubre el mismo orden de magnitud, así
  que la cuenta sale igual de bien, pero si el proyecto acaba siendo el riego
  conviene añadirla: es una línea en `PIEZAS` de `c8_escenas2.py` y otra en
  `c8_verifica.py`.
- La escena de la S2 dibuja **una caja rectangular de 26 × 17 cm** en una pared.
  Es una elección mía para tener algo a escala; si el proyecto del curso es la
  barrera, el alzado tendría que llevar además la propia barrera.

### 4. El test: está en la sesión 4, no en la 8

Igual que en la c6, y por el mismo motivo: la última sesión escrita es la 4. Son
**10 preguntas** tituladas «Lo que tiene que haber quedado de **estas cuatro
sesiones**». Cuando se escriban las cuatro que faltan, lo suyo es dejar este
donde está y añadir otro al final de la S8. **Esto lo decides tú.**

### 5. Las cuatro sesiones pendientes: he puesto títulos

Aparecen desactivadas pero **con título**, para que se vea la forma entera de la
unidad. Mi propuesta, encadenada con lo escrito y sin pisar la U3 (materiales y
ciclo de vida) ni la U9 (tecnología y sociedad):

| S | Título corto | Qué resuelve | Qué deja abierto |
|---|---|---|---|
| 5 | El residuo que dejas | Qué hay dentro de tu aparato el día que se tira, qué se recupera y qué decide eso. RAEE. | Ya sé lo que pesa cada trozo por separado |
| 6 | La cuenta completa | Un número solo para todo el proyecto: materiales + energía + fin de vida, con la técnica de la S1. | Tengo el número, y es malo |
| 7 | Rediseñar con lo medido | Una pasada entera de rediseño, con un antes y un después medidos. | Ya está mejor. ¿Y cómo lo cuento? |
| 8 | Defender el impacto | Presentar y defender el impacto ante otros. Test de la unidad entera. | — |

El cierre de la S4 ya engancha con la S5 (lo que lleva dentro y el pegamento).

---

## Las escenas: qué calculan exactamente

Ninguna enseña un número que no salga de una cuenta. El verificador rehace cada
cuenta **en Python y a partir de la definición** (de la norma, de la fórmula de
la WCAG, de la hoja de características), no copiando el JavaScript, y las
compara.

### S1 · «La báscula»

Ocho acciones. Cada barra es `cantidad × factor`, y las de electricidad llevan
además `× intensidad de la red`. Las cantidades **se pueden editar** y todo se
recalcula, incluido el juego.

- El **gráfico es logarítmico a propósito**: entre 0,05 kg y 103 kg hay un factor
  2.000 y en escala lineal las cuatro barras de abajo no se verían. El
  verificador comprueba que lo es (la barra mayor no puede ser mil veces la
  menor).
- **En amarillo, lo que depende de la red; en azul, lo que no.** Al pasar de
  España (146 g/kWh) a la media mundial (471), las amarillas se multiplican por
  3,2 y las azules **no se mueven ni un pelo**. El verificador comprueba las dos
  cosas. Esa es la idea que quiero que se lleven.
- El **juego de ordenar** se corrige contra la cuenta de la propia escena, no
  contra una respuesta guardada: si el alumno cambia una cantidad, cambia la
  solución. Sale barajado (si no, salía ya resuelto). El verificador comprueba
  que las cartas marcadas en verde son exactamente las que están en su sitio.

### S2 · «El comprobador de diseño universal»

Un **alzado a escala** con cuatro criterios, cada uno con su artículo delante.

- La **escala se recalcula sola** para que la rampa entera quepa, y la escena
  escribe cuántos centímetros vale un píxel. El **ángulo que se ve es
  arctan(pendiente)**: el verificador lee las líneas del SVG y mide su pendiente
  de verdad, para los siete casos que prueba.
- La rampa se **trocea en tramos de 9,00 m como máximo** con sus rellanos de
  1,50 m, y suma el metro y medio libre de cada punta. Un desnivel de 80 cm al
  6 % ocupa **17,83 m de acera**, y se ve.
- El **pulsador**: superficie = πr², comparada con los 12 cm² del art. 23.2.a. La
  escena calcula además el diámetro mínimo, 2·√(12/π) = **39,1 mm**.
- El **contraste** es la fórmula de la WCAG entera (linealizar los canales,
  0,2126·R + 0,7152·G + 0,0722·B, y (L+0,05)/(L+0,05)), y enseña los dos valores
  de luminancia. Hay además una **muestra en vivo** de los dos colores dentro de
  la ficha, que es donde se ve de verdad si se lee.
- **Las dos figuras están a escala**, en centímetros: 1,70 m de pie y 1,30 m
  sentada, con la rueda de 60 cm y el asiento a 48. Si no lo estuvieran, el
  dibujo mentiría sobre el tamaño de la rampa, que es de lo que va todo esto.
- La escena **dice en su pie lo que NO mide** y la norma sí exige: anchura libre
  de paso, pendiente transversal, pasamanos, pavimento táctil, avisador acústico
  y vibración del pulsador. Un alzado es una vista.

### S3 · «Reparar o tirar»

Dos gráficos con **el mismo eje horizontal**, los años que conservas el aparato,
y esa coincidencia es la sesión entera: mientras la batería empeora, la huella
por año de servicio mejora.

- Batería: `capacidad = 100 − 20·ciclos/ciclos80`, anclado al mínimo del
  Reglamento (UE) 2023/1670 (80 % a los 800 ciclos). Se puede cambiar a 400 o
  1.200. **Por debajo del 80 % la curva va a trazos**, porque ahí el modelo está
  extrapolando.
- Huella por año: `(fabricación + uso·años)/años`, una hipérbola dibujada punto a
  punto. El **consumo de uso no está escrito a mano**: sale de los ciclos al año
  que resultan de cómo carga el alumno el móvil.
- La tabla compara reparar contra tirar a tres años, en kg y en euros, y el
  verificador comprueba que el ahorro en kg es exactamente fabricación menos
  batería.

### S4 · «El presupuesto de energía»

`corriente media = Σ(corriente × fracción de tiempo)`, `autonomía = capacidad /
corriente media`. Tres placas, seis piezas, cuatro pilas, periodo logarítmico de
1 s a 1 hora.

- Lo que de verdad enseña: **dormir un Arduino Uno mejora menos del doble**
  (×2,06) porque el regulador, el chip de USB y el LED de encendido siguen
  comiendo; **dormir un ATmega328P pelado mejora 350 veces**. El verificador
  comprueba las dos cifras. Esa diferencia es la respuesta a la pregunta del
  encargo.
- La escena **prueba ella sola cinco cambios posibles**, uno a uno, rehaciendo
  la cuenta entera para cada uno, y dice cuál gana. El verificador rehace esos
  mismos cinco en Python y comprueba que recomienda el bueno y que el factor de
  mejora que anuncia es el calculado.
- Cuando el que gana es «una pila más grande», la escena **lo dice y lo matiza**:
  es la palanca que pesa, ocupa y hay que volver a comprar.
- Distingue dos cosas que casi todos los tutoriales mezclan: el regulador lineal
  **no te quita horas** (deja pasar la misma corriente), te quita **energía**, en
  forma de calor. La escena da las dos cifras por separado.

---

## Las fotos

Las cuatro son de Wikimedia Commons, con la licencia consultada por la API
(`generadores/c8_fotos.py`) **y la imagen abierta y mirada una a una**.

| Sesión | Fichero | Autor | Licencia | Tamaño |
|---|---|---|---|---|
| 1 | `c8-mauna-loa.jpg` | NOAA | dominio público | **666×295** |
| 2 | `c8-rebaje-acera.jpg` | Nick-philly | CC BY-SA 4.0 | 3000×2000 → 1280 |
| 3 | `c8-bombilla-centenaria.jpg` | LPS.1 | CC0 | 1024×1536 |
| 4 | `c8-multimetro.jpg` | Zeroping | CC BY 4.0 | 4032×3024 → 1280 |

**Tres cosas que hay que mirar:**

1. **La de Mauna Loa mide 666 px de ancho y es la más floja de las cuatro.** Es
   una foto aérea antigua de la NOAA, con poco contraste. La historia (Keeling,
   1958, medir donde no hay nada) la sostiene, pero si te parece pobre hay que
   buscar otra. Busqué también la curva de Keeling y las placas conmemorativas;
   un gráfico no me servía, porque la sesión ya tiene un gráfico propio y
   además calculado.
2. **La del multímetro enseña una medida en PARALELO, no en serie.** Las dos
   puntas están a los dos lados de una resistencia, que es como se mide
   *tensión*. Lo he dejado **a propósito** y lo digo en el pie, porque es el
   error que van a cometer: el pie explica que para medir corriente hay que abrir
   el circuito y meter el multímetro dentro, y avisa de que ponerlo en paralelo
   en la escala de mA cortocircuita la pila. Si prefieres una foto de una medida
   correcta, hay que buscarla, porque en Commons no la encontré.
3. **En esa misma foto la placa que asoma es un Arduino Mega, no un Uno** (se ven
   los pines 14 a 33 y el rótulo «COMMUNICATION»). En el pie digo «una placa
   Arduino», sin apellido, a propósito.

## Los vídeos

Título y canal comprobados por oEmbed el 18-sep-2026. **Nadie los ha visto
enteros**: solo está verificado que el vídeo existe, que se llama como digo y
que es del canal que digo. Antes de ponerlos en clase, míralos.

| Sesión | ID | Título | Canal |
|---|---|---|---|
| 1 | `3mJog1DXZ3s` | La huella de carbono · ¿Cómo podemos reducirla? | Naeco |
| 2 | `M_Abq9pave8` | Conoce más sobre la accesibilidad universal en menos de 2 minutos | Incluyeme.com |
| 3 | `nO2RWjrKfMc` | Obsolescencia programada y medio ambiente. Directiva (UE) 2024/825 | Universitat Politècnica de València |
| 4 | `kd3nZ7HmoxY` | Midiendo el consumo de un Arduino UNO | Prometec |

El de la S3 es el más flojo de los cuatro como vídeo (es la parte 14 de 16 de un
curso universitario y es seco), pero es de los pocos sitios donde esto se cuenta
**con la norma delante** en vez de con indignación. Los demás que encontré sobre
obsolescencia programada son justo lo que la sesión intenta corregir: mezclan el
fraude con el límite técnico. Si conoces uno mejor, se cambia el `id` y ya está.

---

## De dónde sale cada dato

Todo lo que afirma la unidad está comprobado contra una fuente primaria o contra
una recopilación citada. Por orden de aparición:

**Sesión 1**

- **Intensidad de la red**: 146 g CO₂/kWh en España, 211 en la UE-27 y 471 en el
  mundo, **año 2024**. Our World in Data con datos de Ember, serie
  `carbon-intensity-electricity`, descargada el 18-sep-2026.
- **Cargador vacío, 0,04 W**: informe ambiental del iPhone 17 (Apple,
  septiembre de 2025), tabla final, «Power adapter, no-load».
- **Fabricar un móvil, 55 kg** (256 GB) y **61 kg** (512 GB): mismo informe. El
  reparto **76 % producción / 18 % carga / 4 % transporte / 1 % fin de vida** y
  el supuesto de **tres años de uso** también salen de ahí. Ese 76 % es el dato
  que sostiene toda la sesión 3.
- **Streaming, 0,077 kWh por hora**: estimación de la Agencia Internacional de
  la Energía revisada en **noviembre de 2020** (36 g de CO₂ por hora con la media
  mundial de intensidad; 36/471 ≈ 0,077).
- **Ternera 60 kg/kg y legumbres ~0,9 kg/kg**: Poore y Nemecek, *Science*, 2018,
  vía Our World in Data.
- **Gasolina, 2,31 kg CO₂/L**: es el valor publicado habitual. La unidad **hace
  la derivación delante del alumno** (0,75 kg/L × 86 % de carbono × 44/12 =
  2,37 kg) y dice que sale un 3 % por encima, y por qué.
- **Attari y otros, *PNAS*, 2010**: 505 personas, se quedan cortas por un factor
  de 2,8 de media, y al preguntarles por lo más eficaz dicen «apagar cosas» en
  vez de «cambiar el aparato».
- **Keeling**: marzo de 1958, primera medida ~313 ppm; Año Geofísico
  Internacional (julio 1957 – diciembre 1958); ~325 ppm al final de los sesenta;
  hoy por encima de 420. Observatorio a unos 3.400 m.

**Sesión 2**

- **Orden TMA/851/2021**, de 23 de julio (BOE-A-2021-13488). He leído el texto
  consolidado del BOE, no un resumen. Artículos usados: **14** (rampas: anchura
  1,80 m; tramos de 9,00 m máximo en proyección horizontal; 10 % hasta 3,00 m y
  8 % hasta 9,00 m; rellanos de 1,50 m; espacio libre de 1,50 m al principio y al
  final), **20.6** (vados: 10 % hasta 2,00 m y 8 % hasta 3,00 m; transversal 2 %)
  y **23.2.a** (pulsadores: 0,80 a 1,20 m de altura; 12 cm² de superficie
  mínima; accionables con el puño o con el codo; vibración; flecha en relieve de
  4 cm).
  ⚠️ **Esto deroga la Orden VIV/561/2010**, que es la que sigue apareciendo en la
  mitad de los apuntes y blogs de internet, con cifras distintas (por ejemplo,
  pulsadores de 0,90 a 1,20 m en vez de 0,80 a 1,20). La escena lo dice
  explícitamente en su pie.
- **Siete principios**: Ronald Mace y equipo, North Carolina State University,
  1997.
- **Subtítulos**: estudio del regulador británico de televisión, **2006**:
  7,5 millones de espectadores usaban subtítulos y unos seis millones de ellos no
  tenían pérdida auditiva.
- **WCAG 2.1**, criterio 1.4.3 y la definición de luminancia relativa del W3C.
- **Los tres ejemplos del efecto del corte de acera** los cambié a propósito por
  otros: ver abajo, en «lo que he quitado».

**Sesión 3**

- **Cártel Phoebus**: constituido el **23 de diciembre de 1924** en Ginebra;
  Osram, Philips y General Electric entre otros; norma de 1.000 horas; muestras a
  un laboratorio central en Suiza; tabla de multas en francos suizos; archivos
  municipales de Berlín, media de **1.800 h en 1926** y **1.205 h en el ejercicio
  1933-34**; disuelto en 1939.
- **Bombilla centenaria de Livermore**: encendida desde **1901**, filamento de
  carbón, hoy a unos **4 vatios**.
- **Batterygate**: **Italia (AGCM), 2018, 10 millones de euros**; **Francia
  (DGCCRF), febrero de 2020, 25 millones de euros**, y el motivo declarado es
  **práctica comercial engañosa por omisión**. La explicación técnica (la
  resistencia interna sube con la edad, la tensión se hunde en los picos de
  corriente y el teléfono se apaga) es la que dio Apple y es correcta.
- **Reglamento (UE) 2023/1670**, aplicable desde el **20 de junio de 2025**: 80 %
  de capacidad a los 800 ciclos, 5 años de actualizaciones del sistema operativo
  desde el fin de comercialización, 7 años de piezas de repuesto, resistencia
  mínima a caídas, polvo, agua y arañazos.
- **Directiva (UE) 2024/1799**, derecho a reparar.

**Sesión 4**

- **ATmega328P en power-down, 0,1 µA**: hoja de características. La unidad
  **dice que ese dato está medido a 1,8 V y con todo apagado**, y que en un
  montaje real puede salir diez veces peor sin que eso cambie el orden de
  magnitud.
- **Rendimiento del adaptador, 87,8 % a 230 V**: informe ambiental del iPhone 17.
- **La lectura**: Voyager 1 y 2 (20-ago y 5-sep de 1977), 470 W al lanzarlas, ~4 W
  menos cada año, diez instrumentos científicos, el de rayos cósmicos apagado el
  25-feb-2025 y el de partículas cargadas el 17-abr-2026, quedan dos encendidos,
  y la previsión de los ingenieros es mantener uno entrada la década de 2030.
  Recuperación de la telemetría en 2024 y de los propulsores de balanceo en 2025.
- **La lectura**: Ed Roberts entra en Berkeley en 1962; moción del pleno del
  **28 de septiembre de 1971** (quince esquinas); primeros rebajes oficiales en
  Telegraph Avenue en **1972**.

---

## Los números peor apoyados, dichos aquí y dentro de la propia escena

Esto es lo que menos me gusta y por eso va junto y con nombre:

1. **Fabricar una batería de móvil, 2 kg de CO₂e** (escena de la S3). No tengo
   fuente directa. Sale de aplicar un orden de magnitud habitual en los estudios
   de ciclo de vida (~100 kg CO₂e por kWh de celda de litio) a los 0,014 kWh que
   tiene la batería de un móvil. **La escena lo dice en su pie, con esas
   palabras: es el número peor apoyado de la escena.** Como solo interviene en
   la comparación «reparar frente a tirar», y el otro término son 55 kg, la
   conclusión no cambia aunque el 2 fuera un 6.
2. **18 Wh por carga de móvil** (escena de la S1). Es una estimación nuestra:
   una batería de unos 14 Wh más las pérdidas del cargador. Está rotulado como
   estimación.
3. **Las corrientes de las placas** (escena de la S4): Uno 45/34 mA, Nano 19/17,
   ATmega328P pelado 12/0,05. Son **valores típicos publicados y medidos por
   aficionados**, no de hoja de características. El pie lo dice y la práctica
   pide **medirlos con el multímetro** y escribir al lado si el valor es «medido»
   o «supuesto» —eso vale un punto de la nota, a propósito—.
4. **Pila de 9 V, 500 mAh**. Es la capacidad nominal a poca corriente; a 85 mA da
   bastante menos. El pie lo dice.
5. **Los 4 vatios de la bombilla de Livermore.** Es una cifra muy repetida y
   creíble, pero no la he podido comprobar contra una medida publicada. Si
   resultara ser otra, el argumento de la sesión (durar y alumbrar tiran en
   sentidos contrarios) no se cae, pero el número habría que cambiarlo.

---

## Lo que he quitado a propósito

Tres ejemplos que circulan en todas las charlas de accesibilidad y que **no he
puesto** porque no los he podido apoyar:

- «El **mando a distancia** se inventó para quien no podía levantarse». El primer
  mando de televisión (Zenith, 1950) se vendió por comodidad, no por
  accesibilidad.
- «Los **mensajes de texto** se pensaron para personas sordas». El SMS nació como
  un canal de señalización de la red; que lo adoptaran masivamente las personas
  sordas vino después, y es otra cosa.
- El **teclado QWERTY** y otras historias parecidas.

En su lugar he puesto tres que sí están documentadas: la **máquina de escribir**
de Pellegrino Turri (1808, para una condesa ciega), los **Talking Books** de la
American Foundation for the Blind (1932) y los **mangos gruesos y blandos** que
sacó Sam Farber en 1990 porque su mujer tenía artritis.

---

## La lectura de aula

`lectura-tema8.pdf`, 4 páginas, **30 párrafos justos** (el script se niega a
generar si no son 30) y 10 preguntas. Título: *Lo que no se mide*.

Tres historias, una por idea, y ninguna repite lo que ya está en la página:

1. **Keeling y Mauna Loa**, marzo de 1958. Lo que cuesta medir bien. Incluye el
   detalle que más enseña de todo el texto: **Mauna Loa es un volcán y suelta
   CO₂**, así que hay un procedimiento escrito para descartar las horas en que el
   viento viene del cráter. Medir bien es también saber cuándo tirar un dato.
2. **Los rebajes de acera de Berkeley**, 1971-1972. Contado desde quien lo
   necesitaba: Ed Roberts, los Rolling Quads, las rampas de cemento hechas de
   noche, la moción del 28 de septiembre de 1971 y la losa de Telegraph Avenue.
3. **Las Voyager**, 1977 y contando. Un presupuesto de energía a escala de medio
   siglo, y por qué se pueden reparar a veinte mil millones de kilómetros: porque
   se les puede cambiar el programa y porque llevan margen.

La pregunta 7 es la que más me gusta: pide calcular 470/4 = 117 años y después
explicar **dos motivos por los que esa cuenta no sirve** para predecir el final
de la misión.

Un detalle de maqueta menor, el mismo que se anotó en la c6: `lectura.py` no
agrupa un titulillo con el párrafo que le sigue. Aquí no ha caído mal en ninguna
página, así que no lo he tocado; sigue pendiente de arreglar en un sitio y
regenerar todas las lecturas.

---

## Qué debería mirar un humano

1. **Los cuatro vídeos, enteros.** Solo está comprobado que existen y de quién
   son. El de la S3 es el que más dudas me da.
2. **La foto de Mauna Loa**, 666 px y floja. Y **la del multímetro**, que enseña
   una medida en paralelo a propósito: decide si esa jugada te convence.
3. **Dónde va el test** (ahora en la S4, cubriendo solo lo escrito).
4. **`voz.py` no estaba en esta rama.** Segunda vez. Hay que decidir dónde vive.
5. **Los 2 kg de fabricar una batería**, que es el número peor apoyado de toda la
   unidad.
6. **Los 4 W de la bombilla de Livermore.**
7. **`PROYECTOS.md` sigue costeando los cinco proyectos con micro:bit** («con
   micro:bit reutilizable del centro») aunque el punto 1 del final ya diga que en
   4.º es Arduino. Sigue igual que cuando lo señaló el informe de la c6.
8. **Si el proyecto del curso acaba siendo el riego**, añadir la bomba a la
   escena de la S4 (una línea).
9. **Si la práctica de la S4 se va a hacer de verdad con multímetro**, hace falta
   que haya multímetros y que alguien enseñe a no fundir el fusible. La
   alternativa sin material es hacerla entera con la escena, y entonces el
   apartado «medido / supuesto» de la evaluación se queda sin sentido.

---

## Lo que no he hecho

- Las sesiones 5 a 8 (el encargo pedía las cuatro primeras).
- La tarjeta en `4eso/Tecnologia/index.html`, que la pones tú al recoger.
