# -*- coding: utf-8 -*-
u"""Repone los diagramas y las fotos que los generadores no saben producir.

Por que existe. El 20-sep-2026 entraron quince diagramas SVG, la lamina del
Codice Atlantico y la foto del puente de folios, y entraron ESCRITOS EN EL HTML,
sin pasar por ningun generador. El 21-sep bastaron unos cuantos `uN_build.py`
para borrarlos todos sin un aviso: la pagina segui compilando igual, solo que
sin sus figuras. Diecisiete, y ninguna se echaba de menos hasta abrir la pagina.

Mientras esas figuras no esten dentro de los generadores, este script las vuelve
a poner despues de cada build. Cada una se ancla a un trozo de HTML vecino que
si produce el generador, y no se duplica: si la imagen ya esta en la pagina, no
hace nada. Se puede volver a pasar.

Lo suyo seria que cada figura viviera en el generador de su unidad. Hasta que
eso se haga, esto es la red.
"""
import io, os, sys, json

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FIGURAS = json.loads(u'''[
 {
  "pagina": "2eso/TyD/tema10/index.html",
  "img": "conditional-if-else.svg",
  "ancla": "</code>,\\n           <code>bot&oacute;n A pulsado</code>.</p>\\n        <p><b>Umbral</b>: el n&uacute;mero con el que se compara. Es una <b>decisi&oacute;n tuya</b>, no un\\n           dato del sensor, y es lo que de verdad hay que ajustar en un automatismo.</p>\\n      </div>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/conditional-if-else.svg\\" width=\\"1000\\" height=\\"700\\" loading=\\"lazy\\"\\n             alt=\\"Diagrama de flujo de condicionales: si condici&oacute;n entonces acci&oacute;n\\">\\n        <figcaption><b>Estructura de un condicional: SI ... ENTONCES ... SI NO ...</b> El programa compara dos valores (condici&oacute;n), obtiene S&iacute; o NO, y ejecuta uno de dos caminos. En el ejemplo: si temperatura &lt; 20, encender calefacci&oacute;n; si no, apagarla. La indentaci&oacute;n (los espacios al inicio de la l&iacute;nea) marca qu&eacute; c&oacute;digo va dentro de cada rama. Un programa sin condicionales no podr&iacute;a adaptarse al mundo: siempre har&iacute;a lo mismo.\\n          <span class=\\"credito\\">Elaboraci&oacute;n propia &middot; CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "2eso/TyD/tema6/index.html",
  "img": "electric-circuit-basics.svg",
  "ancla": "</li>\\n          <li><b>Cortocircuito</b>: hay un camino de vuelta <b>sin receptor</b>, solo cable. La\\n              corriente se dispara, el generador se calienta y algo se quema.</li>\\n        </ul>\\n      </div>\\n\\n      <h3>C&oacute;mo se dibuja: simbolog&iacute;a normalizada</h3>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/electric-circuit-basics.svg\\" width=\\"1000\\" height=\\"600\\" loading=\\"lazy\\"\\n             alt=\\"Circuito el&eacute;ctrico b&aacute;sico con s&iacute;mbolos normalizados: bater&iacute;a, cables, carga, interruptor y s&iacute;mbolos de componentes\\">\\n        <figcaption>Los <b>elementos b&aacute;sicos de un circuito el&eacute;ctrico</b> y los s&iacute;mbolos normalizados que se usan en los esquemas. Voltaje, corriente, resistencia y la ley de Ohm que los une.\\n          <span class=\\"credito\\">Elaboraci&oacute;n propia &middot; CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "2eso/TyD/tema6/index.html",
  "img": "electrical-power-energy.svg",
  "ancla": "</b>, y es la que\\n         viene escrita en la factura. Confundirlas es el error que hace que una casa pague de m&aacute;s\\n         todos los meses.</p>\\n  \\n    </section>\\n    <section class=\\"bloque\\">\\n      <div class=\\"rotulo\\"><span class=\\"num\\">01</span> Teor&iacute;a &middot; 20 min</div>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/electrical-power-energy.svg\\" width=\\"1000\\" height=\\"600\\" loading=\\"lazy\\"\\n             alt=\\"Potencia eléctrica y energía: diferencia entre vatios y kilovatio-hora\\">\\n        <figcaption>La <b>potencia (P)</b> mide lo que gastas EN ESTE MOMENTO, en vatios. La <b>energía (E)</b> mide lo que acumulas en el tiempo, en kilovatio-hora (kWh). Es la diferencia entre el brillo actual de la bombilla (potencia) y la factura de electricidad (energía). P = V × I. E = P × t. Mezclar estas dos es el error más frecuente en problemas de electricidad.\\n          <span class=\\"credito\\">Elaboraci&oacute;n propia &middot; CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "2eso/TyD/tema5/index.html",
  "img": "forces-newtons-laws.svg",
  "ancla": "</button><button type=\\"button\\" data-ses=\\"6\\">S6 &middot; Repaso y test</button></nav>\\n  </div>\\n</header>\\n\\n<main id=\\"contenido\\" tabindex=\\"-1\\" class=\\"wrap\\">\\n\\n  <div id=\\"ses-1\\">\\n    <div class=\\"ses-head\\">\\n      <div class=\\"eyebrow\\">Sesi&oacute;n 1 &middot; 60 minutos</div>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/forces-newtons-laws.svg\\" width=\\"1000\\" height=\\"700\\" loading=\\"lazy\\"\\n             alt=\\"Las tres leyes de Newton: inercia, F=ma y acción-reacción\\">\\n        <figcaption>Las <b>tres leyes de Newton</b> explican todo lo que va a pasar en este tema: 1ª Ley (inercia): sin fuerza, un objeto sigue igual. 2ª Ley (F = m·a): más fuerza produce más aceleración. 3ª Ley (acción-reacción): toda fuerza tiene una pareja que va en dirección contraria. Las máquinas simples (palancas, poleas, engranajes) son formas inteligentes de repartir y modificar las fuerzas, pero no crean fuerza de la nada.\\n          <span class=\\"credito\\">Elaboraci&oacute;n propia &middot; CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "2eso/TyD/tema5/index.html",
  "img": "lever-classes.svg",
  "ancla": "</i></li>\\n          <li><b>Tercer g&eacute;nero</b> &mdash; la <b>fuerza en medio</b>. Siempre <b>pierde</b>\\n              fuerza y gana recorrido y velocidad.\\n              <i>Pinzas de depilar, ca&ntilde;a de pescar, tu propio brazo.</i></li>\\n        </ul>\\n      </div>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/lever-classes.svg\\" width=\\"1000\\" height=\\"750\\" loading=\\"lazy\\"\\n             alt=\\"Las tres clases de palancas: fulcro en medio, carga en medio, esfuerzo en medio\\">\\n        <figcaption><strong>Las tres clases de palancas:</strong> Orden de posiciones, ventaja mec&aacute;nica y ejemplos de cada clase\\n          <span class=\\"credito\\">Elaboraci&oacute;n propia &middot; CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "2eso/TyD/tema3/index.html",
  "img": "material-properties.svg",
  "ancla": "<b>maleabilidad</b>.</li>\\n          <li><b>Densidad</b>: cu&aacute;nto pesa un volumen dado. De ah&iacute; sale que algo sea «ligero».</li>\\n          <li><b>Conductividad</b>: deja pasar el calor o la electricidad. Lo contrario es <b>aislante</b>.</li>\\n        </ul>\\n      </div>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/material-properties.svg\\" width=\\"1000\\" height=\\"700\\" loading=\\"lazy\\"\\n             alt=\\"Propiedades mecánicas, térmicas, eléctricas y otras de los materiales\\">\\n        <figcaption>Las <b>propiedades de los materiales</b> se dividen en varias categorías: mecánicas (resistencia, dureza, elasticidad), térmicas (conductividad, punto de fusión), eléctricas (conductividad, semiconductores, aislantes) y otras (densidad, corrosión, trabajabilidad, sostenibilidad). Cada propiedad tiene límites, y el ingeniero elige el material cuyas propiedades se ajustan a lo que necesita, buscando el equilibrio entre prestaciones y coste.\\n          <span class=\\"credito\\">Elaboraci&oacute;n propia &middot; CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "2eso/TyD/tema6/index.html",
  "img": "ohms-law-triangle.svg",
  "ancla": "<a href=\\"https://www.youtube.com/watch?v=tpt9FlNYq4k\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. Es obra de su autor y no forma parte del material publicado bajo la\\n          licencia de esta p&aacute;gina.</p>\\n      </div>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/ohms-law-triangle.svg\\" width=\\"1000\\" height=\\"700\\" loading=\\"lazy\\"\\n             alt=\\"Tensi&oacute;n, intensidad y resistencia: el tri&aacute;ngulo de Ohm\\">\\n        <figcaption><strong>La ley de Ohm:</strong> La tensi&oacute;n (empu&aacute;n), la intensidad (caudal) y la resistencia (estorbo) se relacionan con V = I &times; R. Tapar lo que buscas y multiplicar (o dividir) los otros dos.\\n          <span class=\\"credito\\">Elaboraci&oacute;n propia &middot; CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "2eso/TyD/tema10/index.html",
  "img": "programming_robotics_concepts.svg",
  "ancla": "<b>pasar desfilando</b> de derecha a izquierda. Eso tambi&eacute;n\\n           es una decisi&oacute;n de dise&ntilde;o de alguien: con 25 luces, o desfila o no se puede.</p>\\n      </div>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/programming_robotics_concepts.svg\\" width=\\"1000\\" height=\\"600\\" loading=\\"lazy\\"\\n             alt=\\"Conceptos de programación: sensores, bloques de programación (bucles, condicionales, variables), algoritmos y estructura de un programa\\">\\n        <figcaption>Los conceptos clave de programación y robótica: sensores que entienden el mundo, bloques que lo controlan (bucles, condicionales, variables),\\n          y la estructura básica de un programa en micro:bit con inicialización y bucle infinito.</figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "2eso/TyD/tema6/index.html",
  "img": "series-parallel-circuits.svg",
  "ancla": "<b>exactamente al rev&eacute;s</b>, y saber cu&aacute;l es cu&aacute;l es lo que\\n         impide que se te queme una regleta.</p>\\n  \\n    </section>\\n    <section class=\\"bloque\\">\\n      <div class=\\"rotulo\\"><span class=\\"num\\">01</span> Teor&iacute;a &middot; 20 min</div>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/series-parallel-circuits.svg\\" width=\\"1200\\" height=\\"500\\" loading=\\"lazy\\"\\n             alt=\\"Comparaci&oacute;n de circuitos en serie y paralelo con bombillas LED\\">\\n        <figcaption>En <b>serie</b>, todas las bombillas comparten el mismo camino: si se funde una, se corta el circuito completo. En <b>paralelo</b>, cada bombilla tiene su propio camino: si se funde una, las dem&aacute;s siguen luciendo. Las dos formas de entender c&oacute;mo se cablean las casas.\\n          <span class=\\"credito\\">Elaboraci&oacute;n propia &middot; CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "2eso/TyD/tema5/index.html",
  "img": "simple-machines.svg",
  "ancla": "</script>\\n\\n  \\n    </section>\\n    <section class=\\"bloque\\">\\n      <div class=\\"rotulo\\"><span class=\\"num\\">01</span> Teor&iacute;a &middot; 20 min</div>\\n\\n      <h3>Una barra, un punto y un trato</h3>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/simple-machines.svg\\" width=\\"1200\\" height=\\"500\\" loading=\\"lazy\\"\\n             alt=\\"Las 6 máquinas simples: palanca, rueda y eje, polea, plano inclinado, cuña y tornillo\\">\\n        <figcaption>Las <b>seis máquinas simples</b> que han resuelto todos los problemas de fuerza desde la antigüedad. Todas siguen el mismo principio: cambian fuerza por distancia. Aumentas uno, pierdes el otro. La ventaja mecánica es el intercambio.\\n          <span class=\\"credito\\">Elaboración propia · CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "2eso/TyD/tema4/index.html",
  "img": "structural-stresses.svg",
  "ancla": "</p>\\n\\n    </section>\\n    <section class=\\"bloque\\">\\n      <div class=\\"rotulo\\"><span class=\\"num\\">01</span> Teor&iacute;a &middot; 25 min</div>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/structural-stresses.svg\\" width=\\"1000\\" height=\\"700\\" loading=\\"lazy\\"\\n             alt=\\"Los cinco esfuerzos en estructuras: compresión, tensión, flexión, torsión y cortante\\">\\n        <figcaption>Los <b>cinco esfuerzos básicos</b> que pueden afectar a una estructura: compresión (se aplasta), tensión (se estira), flexión (se dobla), torsión (se retuerce) y cortante (se cizalla). Cada material tiene un límite diferente para cada uno, y el ingeniero elige el material y la forma para que el esfuerzo máximo sea menor que su límite de ruptura.\\n          <span class=\\"credito\\">Elaboraci&oacute;n propia &middot; CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "2eso/TyD/tema4/index.html",
  "img": "structures-types.svg",
  "ancla": "<b>La forma de la estructura se elige\\n           para que el material trabaje solo en el esfuerzo que aguanta.</b></p>\\n        <p><b>C&oacute;digo de color de la unidad:</b> azul = pieza comprimida, rojo = pieza estirada,\\n           naranja = fuerza que llega de fuera.</p>\\n      </div>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/structures-types.svg\\" width=\\"1000\\" height=\\"400\\" loading=\\"lazy\\"\\n             alt=\\"Tres tipos principales de estructuras: viga, arco y celosía\\">\\n        <figcaption>Tipos de estructuras: <b>viga</b> (resiste flexión), <b>arco</b> (resiste compresión), <b>celosía</b> (barras en tracción/compresión). Cada estructura transfiere las fuerzas de manera distinta según su forma.</figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "2eso/TyD/tema4/index.html",
  "img": "triangulation-structures.svg",
  "ancla": "</li>\\n        </ul>\\n        <p><b>Estructura</b>: conjunto de elementos que soporta las cargas de un objeto y las conduce\\n           hasta el suelo sin romperse ni deformarse demasiado.</p>\\n      </div>\\n\\n      <h3>El truco que lo cambia todo: triangular</h3>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/triangulation-structures.svg\\" width=\\"1000\\" height=\\"600\\" loading=\\"lazy\\"\\n             alt=\\"Comparación entre rectángulo que se deforma y triángulo rígido\\">\\n        <figcaption>El <b>rectángulo es flexible</b>: sus vértices pueden moverse, deformando la figura. El <b>triángulo es indeformable</b>: con tres lados fijos, todos los ángulos quedan determinados. Triangular una estructura (añadir diagonales) crea triángulos internos que impiden cualquier deformación. Este es el principio fundamental de grúas, torres, puentes y cualquier estructura que soporte cargas.\\n          <span class=\\"credito\\">Elaboraci&oacute;n propia &middot; CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "2eso/TyD/tema4/index.html",
  "img": "u4-puente-folios.jpg",
  "ancla": "</li>\\n          <li><b>El puente se ha tumbado de lado</b> &rarr; falt&oacute; <b>arriostramiento</b>. No es un\\n              problema de resistencia: es de <b>estabilidad</b>, como la sesi&oacute;n 4.</li>\\n        </ul>\\n      </div>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/u4-puente-folios.jpg\\" width=\\"345\\" height=\\"265\\" loading=\\"lazy\\"\\n             style=\\"max-width:345px;margin:0 auto\\"\\n             alt=\\"Puente de celosía construido con tubos de papel enrollado, visto desde arriba\\">\\n        <figcaption>Uno terminado, para comparar con el vuestro. Mirad tres cosas: <b>no hay ni un\\n        rectángulo</b> —todo son triángulos, que es lo único que no se deforma—; las dos cerchas\\n        laterales están <b>unidas entre sí</b> por barras arriba y abajo, y eso es el arriostramiento\\n        que impide que el puente se tumbe de lado; y cada barra es un <b>canuto</b>, no un folio plano:\\n        el mismo papel, puesto de otra forma, aguanta kilos. Las uniones son el punto débil de todos\\n        los puentes de papel, y aquí se ve por qué: son las únicas piezas que no puedes enrollar.</figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "2eso/TyD/tema3/index.html",
  "img": "materials_wood_metal_plastic.svg",
  "ancla": "<div class=\\"entender\\">\\n        <span class=\\"e-tag\\">Solo para entenderlo &middot; no hace falta copiarlo</span>\\n        <p>Durante casi toda la historia esto no se eligi&oacute;: se usaba <b>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/materials_wood_metal_plastic.svg\\" width=\\"960\\" height=\\"400\\" loading=\\"lazy\\"\\n             alt=\\"Comparación de tres materiales técnicos comunes: madera, metal y plástico, con sus propiedades y aplicaciones\\">\\n        <figcaption>Los tres materiales técnicos más comunes: cada uno tiene propiedades distintas que lo hacen\\n          adecuado para usos diferentes. No hay un «mejor»; hay el <b>adecuado para lo que quieres</b>.</figcaption>\\n      </figure>",
  "modo": "despues"
 },
 {
  "pagina": "2eso/TyD/tema3/index.html",
  "img": "mohs_hardness_scale.svg",
  "ancla": "</b>: dice qui&eacute;n va delante de qui&eacute;n, no cu&aacute;nto. El diamante es un 10 y\\n           el corind&oacute;n un 9, pero el diamante no es «uno m&aacute;s duro»: es unas cuatro veces m&aacute;s duro. Por eso\\n           en la industria se usan hoy otras escalas &mdash;Brinell, Rockwell, Vickers&mdash; que s&iacute; dan\\n           n&uacute;meros proporcionales. La de Mohs sobrevive porque sigue siendo la &uacute;nica que funciona\\n           sin enchufe.</p>\\n      </div>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/mohs_hardness_scale.svg\\" width=\\"640\\" height=\\"500\\" loading=\\"lazy\\"\\n             alt=\\"Escala de Mohs: 10 minerales ordenados por dureza creciente desde el talco hasta el diamante\\">\\n        <figcaption>La <b>escala de Mohs</b> de 1 a 10: una ordenación que sigue un principio simple:\\n          si A raya a B, A es más duro. Sin aparatos, sin opiniones. Solo física.</figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "4eso/Tecnologia/tema5/index.html",
  "img": "c5-reductora.jpg",
  "ancla": "<b>hidr&aacute;ulica</b> (aceite, que no se comprime), y por eso las\\n              excavadoras son hidr&aacute;ulicas y no neum&aacute;ticas.</li>\\n        </ul>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/c5-reductora.jpg\\" width=\\"1200\\" height=\\"800\\" loading=\\"lazy\\"\\n             alt=\\"Detalle de un tren de engranajes met&aacute;licos y un tornillo sin fin dentro de una reductora\\">\\n        <figcaption>La v&iacute;a que acabas de descartar, por dentro: <b>un motor peque&ntilde;o y un tren de engranajes</b> que cambia vueltas por par. Funciona &mdash; de ah&iacute; sale el par que te falta &mdash;, pero fíjate en cu&aacute;ntas piezas hay que meter, y en que basta con que una se atasque para que el motor siga tirando contra ella hasta quemarse.\\n          <br><br>Foto de <b>Rodrigo Pharazz</b> en Pexels. Es de su autor y no forma parte del material publicado bajo la licencia de esta p&aacute;gina.</figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "4eso/Tecnologia/tema8/index.html",
  "img": "c8-reparar.jpg",
  "ancla": "<li><b>Trabajo.</b> Horas vuestras, o de alguien que tiene que acordarse de algo cada\\n              curso.</li>\\n          <li><b>Prestaci&oacute;n perdida.</b> Algo que el aparato dejaba de hacer. Es la que no se\\n              apunta, y es la que rompe requisitos.</li>\\n        </ul>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/c8-reparar.jpg\\" width=\\"1200\\" height=\\"800\\" loading=\\"lazy\\"\\n             alt=\\"T&eacute;cnico soldando con una lupa sobre una placa de circuito en un banco de trabajo\\">\\n        <figcaption>El cambio que no aparece en ninguna de las tres columnas: <b>que el aparato dure m&aacute;s</b>. Arreglar una placa gasta un soldador y media hora; fabricar la de repuesto gasta el mineral, la f&aacute;brica y el transporte otra vez. Por eso la cuenta honrada no es la del aparato: es la del aparato <b>dividido entre los a&ntilde;os que va a durar</b>.\\n          <br><br>Foto de <b>Kaboompics</b> en Pexels. Es de su autor y no forma parte del material publicado bajo la licencia de esta p&aacute;gina.</figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "2eso/TyD/tema4/index.html",
  "img": "u4-puente-palillos.jpg",
  "ancla": "<div id=\\"ses-5\\" hidden>\\n    <div class=\\"ses-head\\">\\n      <div class=\\"eyebrow\\">Sesi&oacute;n 5 &middot; 60 minutos</div>\\n      <h2>El puente de 40 cent&iacute;metros</h2>\\n      <p>Veinte folios enrollados en canutos. La nota no es lo que aguante: es lo que aguante dividido por lo que pese.</p>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/u4-puente-palillos.jpg\\" width=\\"412\\" height=\\"227\\" loading=\\"lazy\\" style=\\"max-width:412px;margin:0 auto\\"\\n             alt=\\"Puente de arco construido con palos de helado pegados, apoyado en una superficie\\">\\n        <figcaption>Otro que sali&oacute; de esta misma sesi&oacute;n, con palos de helado. Mirad c&oacute;mo est&aacute; resuelto: es un <b>arco</b>, y el arco lleva toda la carga a <b>compresi&oacute;n</b> hasta los dos apoyos &mdash; por eso aguanta con piezas que sueltas no aguantan nada. Fijaos tambi&eacute;n en el punto d&eacute;bil: los palos se solapan de dos en dos, y donde se unen es donde se abre.\\n          <br><br>Foto de <b>Roberto P. Garc&iacute;a Llorente</b>, del taller. Bajo la misma licencia que esta p&aacute;gina.</figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "4eso/Tecnologia/tema4/index.html",
  "img": "c4-cohete.mp4",
  "ancla": "</p>\\n        <p>Pero el grifo de tu ducha <b>no</b> es un interruptor. Lo abres <b>un poco</b>. Esta\\n           sesi&oacute;n va de darle a la m&aacute;quina ese &laquo;un poco&raquo;.</p>\\n      </div>",
  "figura": "<div class=\\"escena\\">\\n        <div class=\\"escena-barra\\"><span class=\\"escena-titulo\\">Control proporcional a tama&ntilde;o real &middot; 13 segundos</span></div>\\n        <div class=\\"lienzo\\" style=\\"padding:0;background:#000;display:flex;justify-content:center\\">\\n          <video controls preload=\\"none\\" muted playsinline style=\\"width:auto;max-width:100%;max-height:60vh;display:block\\"\\n                 poster=\\"../../../video/c4-cohete.jpg\\">\\n            <source src=\\"../../../video/c4-cohete.mp4\\" type=\\"video/mp4\\">\\n            Tu navegador no puede reproducir v&iacute;deo.\\n            <a href=\\"../../../video/c4-cohete.mp4\\">Desc&aacute;rgalo aqu&iacute;</a>.\\n          </video>\\n        </div>\\n        <div class=\\"pie\\">Los dos propulsores laterales de un Falcon Heavy, bajando a la vez. Un motor de cohete <b>no se enciende y se apaga</b> para frenar: eso ser&iacute;a todo-nada, y a esa velocidad la primera correcci&oacute;n de m&aacute;s te estrella. Lo que hace es <b>regular el empuje sin parar</b> seg&uacute;n lo que le queda por bajar, que es justo lo que acabas de programar t&uacute;: cuanto mayor es el error, mayor la respuesta. Y llega con velocidad casi cero al tocar.<br><br>V&iacute;deo de <b>SpaceX</b>, v&iacute;a Wikimedia Commons, <b>CC BY 2.0</b>. Recomprimido para la web.</div>\\n      </div>",
  "modo": "antes"
 },
 {
  "pagina": "4eso/Tecnologia/tema7/index.html",
  "img": "c7-caminante.mp4",
  "ancla": "<a href=\\"https://www.youtube.com/watch?v=cwf-cURBUkI\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "figura": "<div class=\\"escena\\">\\n        <div class=\\"escena-barra\\"><span class=\\"escena-titulo\\">Camina, y no es un robot &middot; 8 segundos</span></div>\\n        <div class=\\"lienzo\\" style=\\"padding:0;background:#000;display:flex;justify-content:center\\">\\n          <video controls preload=\\"none\\" muted playsinline style=\\"width:auto;max-width:100%;max-height:60vh;display:block\\"\\n                 poster=\\"../../../video/c7-caminante.jpg\\">\\n            <source src=\\"../../../video/c7-caminante.mp4\\" type=\\"video/mp4\\">\\n            Tu navegador no puede reproducir v&iacute;deo.\\n            <a href=\\"../../../video/c7-caminante.mp4\\">Desc&aacute;rgalo aqu&iacute;</a>.\\n          </video>\\n        </div>\\n        <div class=\\"pie\\">Baja la rampa &eacute;l solo, con paso de persona. Y por dentro <b>no hay nada</b>: ni motor, ni sensor, ni programa, ni una pila. Lo &uacute;nico que lo mueve es la gravedad y la forma de sus piernas. Si la frontera fuera <i>parecerlo</i> o <i>moverse solo</i>, esto ser&iacute;a un robot &mdash; y no lo es, porque no se entera de nada.<br><br>V&iacute;deo de <b>Steven H. Collins</b>, v&iacute;a Wikimedia Commons, <b>CC BY-SA 3.0</b>, la misma licencia de esta p&aacute;gina.</div>\\n      </div>",
  "modo": "antes"
 },
 {
  "pagina": "4eso/Tecnologia/tema7/index.html",
  "img": "c7-robot-paquetes.mp4",
  "ancla": "<i>parecerlo</i> o <i>moverse solo</i>, esto ser&iacute;a un robot &mdash; y no lo es, porque no se entera de nada.<br><br>V&iacute;deo de <b>Steven H. Collins</b>, v&iacute;a Wikimedia Commons, <b>CC BY-SA 3.0</b>, la misma licencia de esta p&aacute;gina.</div>\\n      </div>",
  "figura": "<div class=\\"escena\\">\\n        <div class=\\"escena-barra\\"><span class=\\"escena-titulo\\">Esto s&iacute; lo es &middot; 8 segundos</span></div>\\n        <div class=\\"lienzo\\" style=\\"padding:0;background:#000;display:flex;justify-content:center\\">\\n          <video controls preload=\\"none\\" muted playsinline style=\\"width:auto;max-width:100%;max-height:60vh;display:block\\"\\n                 poster=\\"../../../video/c7-robot-paquetes.jpg\\">\\n            <source src=\\"../../../video/c7-robot-paquetes.mp4\\" type=\\"video/mp4\\">\\n            Tu navegador no puede reproducir v&iacute;deo.\\n            <a href=\\"../../../video/c7-robot-paquetes.mp4\\">Desc&aacute;rgalo aqu&iacute;</a>.\\n          </video>\\n        </div>\\n        <div class=\\"pie\\">El mismo criterio, al rev&eacute;s. Este brazo no repite un movimiento aprendido: las bolsas llegan <b>cada vez en un sitio distinto</b>, y &eacute;l mira, decide y coge. Qu&iacute;tale la c&aacute;mara y no puede hacer nada &mdash; ah&iacute; est&aacute; la frontera de la sesi&oacute;n: <b>enterarse de lo que hay fuera</b>.<br><br>V&iacute;deo de <i>newscreators</i>, v&iacute;a Wikimedia Commons, <b>CC BY 3.0</b>.</div>\\n      </div>",
  "modo": "antes"
 }
]''')


def main():
    puestas = saltadas = perdidas = 0
    for f in FIGURAS:
        ruta = os.path.join(RAIZ, f['pagina'])
        if not os.path.exists(ruta):
            perdidas += 1
            print(u'   no existe la pagina: %s' % f['pagina'])
            continue
        s = io.open(ruta, encoding='utf-8').read()
        # el fichero puede colgar de img/ o de video/: se mira el nombre a secas
        if f['img'] in s:
            saltadas += 1
            continue
        if s.count(f['ancla']) != 1:
            perdidas += 1
            print(u'   ancla perdida para %s en %s' % (f['img'], f['pagina']))
            continue
        i = s.index(f['ancla'])
        if f.get('modo') == 'despues':
            s = s[:i] + f['figura'] + u'\n      ' + s[i:]
        else:
            j = i + len(f['ancla'])
            s = s[:j] + u'\n\n      ' + f['figura'] + s[j:]
        io.open(ruta, 'w', encoding='utf-8', newline='').write(s)
        puestas += 1
    print(u'%d figuras repuestas, %d ya estaban%s'
          % (puestas, saltadas, u', %d SIN SITIO' % perdidas if perdidas else u''))
    return 1 if perdidas else 0


if __name__ == '__main__':
    sys.exit(main())
