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
  "pagina": "2eso/TyD/tema12/index.html",
  "img": "conditional-if-else.svg",
  "ancla": "</code>,\\n           <code>bot&oacute;n A pulsado</code>.</p>\\n        <p><b>Umbral</b>: el n&uacute;mero con el que se compara. Es una <b>decisi&oacute;n tuya</b>, no un\\n           dato del sensor, y es lo que de verdad hay que ajustar en un automatismo.</p>\\n      </div>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/conditional-if-else.svg\\" width=\\"1000\\" height=\\"700\\" loading=\\"lazy\\"\\n             alt=\\"Diagrama de flujo de condicionales: si condici&oacute;n entonces acci&oacute;n\\">\\n        <figcaption><b>Estructura de un condicional: SI ... ENTONCES ... SI NO ...</b> El programa compara dos valores (condici&oacute;n), obtiene S&iacute; o NO, y ejecuta uno de dos caminos. En el ejemplo: si temperatura &lt; 20, encender calefacci&oacute;n; si no, apagarla. La indentaci&oacute;n (los espacios al inicio de la l&iacute;nea) marca qu&eacute; c&oacute;digo va dentro de cada rama. Un programa sin condicionales no podr&iacute;a adaptarse al mundo: siempre har&iacute;a lo mismo.\\n          <span class=\\"credito\\">Elaboraci&oacute;n propia &middot; CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "2eso/TyD/tema8/index.html",
  "img": "electric-circuit-basics.svg",
  "ancla": "</li>\\n          <li><b>Cortocircuito</b>: hay un camino de vuelta <b>sin receptor</b>, solo cable. La\\n              corriente se dispara, el generador se calienta y algo se quema.</li>\\n        </ul>\\n      </div>\\n\\n      <h3>C&oacute;mo se dibuja: simbolog&iacute;a normalizada</h3>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/electric-circuit-basics.svg\\" width=\\"1000\\" height=\\"600\\" loading=\\"lazy\\"\\n             alt=\\"Circuito el&eacute;ctrico b&aacute;sico con s&iacute;mbolos normalizados: bater&iacute;a, cables, carga, interruptor y s&iacute;mbolos de componentes\\">\\n        <figcaption>Los <b>elementos b&aacute;sicos de un circuito el&eacute;ctrico</b> y los s&iacute;mbolos normalizados que se usan en los esquemas. Voltaje, corriente, resistencia y la ley de Ohm que los une.\\n          <span class=\\"credito\\">Elaboraci&oacute;n propia &middot; CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "2eso/TyD/tema8/index.html",
  "img": "electrical-power-energy.svg",
  "ancla": "</b>, y es la que\\n         viene escrita en la factura. Confundirlas es el error que hace que una casa pague de m&aacute;s\\n         todos los meses.</p>\\n  \\n    </section>\\n    <section class=\\"bloque\\">\\n      <div class=\\"rotulo\\"><span class=\\"num\\">01</span> Teor&iacute;a &middot; 20 min</div>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/electrical-power-energy.svg\\" width=\\"1000\\" height=\\"600\\" loading=\\"lazy\\"\\n             alt=\\"Potencia eléctrica y energía: diferencia entre vatios y kilovatio-hora\\">\\n        <figcaption>La <b>potencia (P)</b> mide lo que gastas EN ESTE MOMENTO, en vatios. La <b>energía (E)</b> mide lo que acumulas en el tiempo, en kilovatio-hora (kWh). Es la diferencia entre el brillo actual de la bombilla (potencia) y la factura de electricidad (energía). P = V × I. E = P × t. Mezclar estas dos es el error más frecuente en problemas de electricidad.\\n          <span class=\\"credito\\">Elaboraci&oacute;n propia &middot; CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "2eso/TyD/tema7/index.html",
  "img": "forces-newtons-laws.svg",
  "ancla": "</button><button type=\\"button\\" data-ses=\\"6\\">S6 &middot; Repaso y test</button></nav>\\n  </div>\\n</header>\\n\\n<main id=\\"contenido\\" tabindex=\\"-1\\" class=\\"wrap\\">\\n\\n  <div id=\\"ses-1\\">\\n    <div class=\\"ses-head\\">\\n      <div class=\\"eyebrow\\">Sesi&oacute;n 1 &middot; 60 minutos</div>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/forces-newtons-laws.svg\\" width=\\"1000\\" height=\\"700\\" loading=\\"lazy\\"\\n             alt=\\"Las tres leyes de Newton: inercia, F=ma y acción-reacción\\">\\n        <figcaption>Las <b>tres leyes de Newton</b> explican todo lo que va a pasar en este tema: 1ª Ley (inercia): sin fuerza, un objeto sigue igual. 2ª Ley (F = m·a): más fuerza produce más aceleración. 3ª Ley (acción-reacción): toda fuerza tiene una pareja que va en dirección contraria. Las máquinas simples (palancas, poleas, engranajes) son formas inteligentes de repartir y modificar las fuerzas, pero no crean fuerza de la nada.\\n          <span class=\\"credito\\">Elaboraci&oacute;n propia &middot; CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "2eso/TyD/tema7/index.html",
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
  "pagina": "2eso/TyD/tema8/index.html",
  "img": "ohms-law-triangle.svg",
  "ancla": "<a href=\\"https://www.youtube.com/watch?v=tpt9FlNYq4k\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. Es obra de su autor y no forma parte del material publicado bajo la\\n          licencia de esta p&aacute;gina.</p>\\n      </div>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/ohms-law-triangle.svg\\" width=\\"1000\\" height=\\"700\\" loading=\\"lazy\\"\\n             alt=\\"Tensi&oacute;n, intensidad y resistencia: el tri&aacute;ngulo de Ohm\\">\\n        <figcaption><strong>La ley de Ohm:</strong> La tensi&oacute;n (empuj&oacute;n), la intensidad (caudal) y la resistencia (estorbo) se relacionan con V = I &times; R. Tapar lo que buscas y multiplicar (o dividir) los otros dos.\\n          <span class=\\"credito\\">Elaboraci&oacute;n propia &middot; CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "2eso/TyD/tema12/index.html",
  "img": "programming_robotics_concepts.svg",
  "ancla": "<b>pasar desfilando</b> de derecha a izquierda. Eso tambi&eacute;n\\n           es una decisi&oacute;n de dise&ntilde;o de alguien: con 25 luces, o desfila o no se puede.</p>\\n      </div>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/programming_robotics_concepts.svg\\" width=\\"1000\\" height=\\"600\\" loading=\\"lazy\\"\\n             alt=\\"Conceptos de programación: sensores, bloques de programación (bucles, condicionales, variables), algoritmos y estructura de un programa\\">\\n        <figcaption>Los conceptos clave de programación y robótica: sensores que entienden el mundo, bloques que lo controlan (bucles, condicionales, variables),\\n          y la estructura básica de un programa en micro:bit con inicialización y bucle infinito.</figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "2eso/TyD/tema8/index.html",
  "img": "series-parallel-circuits.svg",
  "ancla": "<b>exactamente al rev&eacute;s</b>, y saber cu&aacute;l es cu&aacute;l es lo que\\n         impide que se te queme una regleta.</p>\\n  \\n    </section>\\n    <section class=\\"bloque\\">\\n      <div class=\\"rotulo\\"><span class=\\"num\\">01</span> Teor&iacute;a &middot; 20 min</div>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/series-parallel-circuits.svg\\" width=\\"1200\\" height=\\"500\\" loading=\\"lazy\\"\\n             alt=\\"Comparaci&oacute;n de circuitos en serie y paralelo con bombillas LED\\">\\n        <figcaption>En <b>serie</b>, todas las bombillas comparten el mismo camino: si se funde una, se corta el circuito completo. En <b>paralelo</b>, cada bombilla tiene su propio camino: si se funde una, las dem&aacute;s siguen luciendo. Las dos formas de entender c&oacute;mo se cablean las casas.\\n          <span class=\\"credito\\">Elaboraci&oacute;n propia &middot; CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "2eso/TyD/tema7/index.html",
  "img": "simple-machines.svg",
  "ancla": "</script>\\n\\n  \\n    </section>\\n    <section class=\\"bloque\\">\\n      <div class=\\"rotulo\\"><span class=\\"num\\">01</span> Teor&iacute;a &middot; 20 min</div>\\n\\n      <h3>Una barra, un punto y un trato</h3>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/simple-machines.svg\\" width=\\"1200\\" height=\\"500\\" loading=\\"lazy\\"\\n             alt=\\"Las 6 máquinas simples: palanca, rueda y eje, polea, plano inclinado, cuña y tornillo\\">\\n        <figcaption>Las <b>seis máquinas simples</b> que han resuelto todos los problemas de fuerza desde la antigüedad. Todas siguen el mismo principio: cambian fuerza por distancia. Aumentas uno, pierdes el otro. La ventaja mecánica es el intercambio.\\n          <span class=\\"credito\\">Elaboración propia · CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "2eso/TyD/tema6/index.html",
  "img": "structural-stresses.svg",
  "ancla": "</p>\\n\\n    </section>\\n    <section class=\\"bloque\\">\\n      <div class=\\"rotulo\\"><span class=\\"num\\">01</span> Teor&iacute;a &middot; 25 min</div>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/structural-stresses.svg\\" width=\\"1000\\" height=\\"700\\" loading=\\"lazy\\"\\n             alt=\\"Los cinco esfuerzos en estructuras: compresión, tracción, flexión, torsión y cortadura\\">\\n        <figcaption>Los <b>cinco esfuerzos básicos</b> que pueden afectar a una estructura: compresión (se aplasta), tracción (se estira), flexión (se dobla), torsión (se retuerce) y cortadura (se cizalla). Cada material tiene un límite diferente para cada uno, y el ingeniero elige el material y la forma para que el esfuerzo máximo sea menor que su límite de ruptura.\\n          <span class=\\"credito\\">Elaboraci&oacute;n propia &middot; CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "2eso/TyD/tema6/index.html",
  "img": "structures-types.svg",
  "ancla": "<b>La forma de la estructura se elige\\n           para que el material trabaje solo en el esfuerzo que aguanta.</b></p>\\n        <p><b>C&oacute;digo de color de la unidad:</b> azul = pieza comprimida, rojo = pieza estirada,\\n           naranja = fuerza que llega de fuera.</p>\\n      </div>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/structures-types.svg\\" width=\\"1000\\" height=\\"400\\" loading=\\"lazy\\"\\n             alt=\\"Tres tipos principales de estructuras: viga, arco y celosía\\">\\n        <figcaption>Tipos de estructuras: <b>viga</b> (resiste flexión), <b>arco</b> (resiste compresión), <b>celosía</b> (barras en tracción/compresión). Cada estructura transfiere las fuerzas de manera distinta según su forma.</figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "2eso/TyD/tema6/index.html",
  "img": "triangulation-structures.svg",
  "ancla": "</li>\\n        </ul>\\n        <p><b>Estructura</b>: conjunto de elementos que soporta las cargas de un objeto y las conduce\\n           hasta el suelo sin romperse ni deformarse demasiado.</p>\\n      </div>\\n\\n      <h3>El truco que lo cambia todo: triangular</h3>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/triangulation-structures.svg\\" width=\\"1000\\" height=\\"600\\" loading=\\"lazy\\"\\n             alt=\\"Comparación entre rectángulo que se deforma y triángulo rígido\\">\\n        <figcaption>El <b>rectángulo es flexible</b>: sus vértices pueden moverse, deformando la figura. El <b>triángulo es indeformable</b>: con tres lados fijos, todos los ángulos quedan determinados. Triangular una estructura (añadir diagonales) crea triángulos internos que impiden cualquier deformación. Este es el principio fundamental de grúas, torres, puentes y cualquier estructura que soporte cargas.\\n          <span class=\\"credito\\">Elaboraci&oacute;n propia &middot; CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "2eso/TyD/tema6/index.html",
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
  "pagina": "2eso/TyD/tema6/index.html",
  "img": "u4-puente-palillos.jpg",
  "ancla": "<div id=\\"ses-5\\" hidden>\\n    <div class=\\"ses-head\\">\\n      <div class=\\"eyebrow\\">Sesi&oacute;n 5 &middot; 60 minutos</div>\\n      <h2>El puente de 40 cent&iacute;metros</h2>\\n      <p>Veinte folios enrollados en canutos. La nota no es lo que aguante: es lo que aguante dividido por lo que pese.</p>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/u4-puente-palillos.jpg\\" width=\\"412\\" height=\\"227\\" loading=\\"lazy\\" style=\\"max-width:412px;margin:0 auto\\"\\n             alt=\\"Puente de arco construido con palos de helado pegados, apoyado en una superficie\\">\\n        <figcaption>Otro que sali&oacute; de esta misma sesi&oacute;n, con palos de helado. Mirad c&oacute;mo est&aacute; resuelto: es un <b>arco</b>, y el arco lleva toda la carga a <b>compresi&oacute;n</b> hasta los dos apoyos &mdash; por eso aguanta con piezas que sueltas no aguantan nada. Fijaos tambi&eacute;n en el punto d&eacute;bil: los palos se solapan de dos en dos, y donde se unen es donde se abre.\\n          <br><br>Foto de <b>Roberto P. Garc&iacute;a Llorente</b>, del taller. Bajo la misma licencia que esta p&aacute;gina.</figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "4eso/Tecnologia/tema4/index.html",
  "img": "c4-cohete.mp4",
  "ancla": "</p>\\n        <p>Pero el grifo de tu ducha <b>no</b> es un interruptor. Lo abres <b>un poco</b>. Esta\\n           sesi&oacute;n va de darle a la m&aacute;quina ese &laquo;un poco&raquo;.</p>\\n      </div>",
  "figura": "<div class=\\"escena\\" id=\\"esc-cohete\\">\\n        <div class=\\"escena-barra\\"><span class=\\"escena-titulo\\">Control proporcional a tama&ntilde;o real &middot; 13 segundos</span></div>\\n        <div class=\\"lienzo\\" style=\\"padding:0;background:#000;display:flex;justify-content:center\\">\\n          <video controls preload=\\"none\\" muted playsinline style=\\"width:auto;max-width:100%;max-height:60vh;display:block\\"\\n                 poster=\\"../../../video/c4-cohete.jpg\\">\\n            <source src=\\"../../../video/c4-cohete.mp4\\" type=\\"video/mp4\\">\\n            Tu navegador no puede reproducir v&iacute;deo.\\n            <a href=\\"../../../video/c4-cohete.mp4\\">Desc&aacute;rgalo aqu&iacute;</a>.\\n          </video>\\n        </div>\\n        <div class=\\"pie\\" role=\\"status\\" aria-live=\\"polite\\" aria-atomic=\\"true\\">Los dos propulsores laterales de un Falcon Heavy, bajando a la vez. Un motor de cohete <b>no se enciende y se apaga</b> para frenar: eso ser&iacute;a todo-nada, y a esa velocidad la primera correcci&oacute;n de m&aacute;s te estrella. Lo que hace es <b>regular el empuje sin parar</b> seg&uacute;n lo que le queda por bajar, que es justo lo que acabas de programar t&uacute;: cuanto mayor es el error, mayor la respuesta. Y llega con velocidad casi cero al tocar.<br><br>V&iacute;deo de <b>SpaceX</b>, v&iacute;a Wikimedia Commons, <b>CC BY 2.0</b>. Recomprimido para la web.</div>\\n      </div>",
  "modo": "antes"
 },
 {
  "pagina": "4eso/Tecnologia/tema7/index.html",
  "img": "c7-caminante.mp4",
  "ancla": "<a href=\\"https://www.youtube.com/watch?v=cwf-cURBUkI\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "figura": "<div class=\\"escena\\" id=\\"esc-caminante\\">\\n        <div class=\\"escena-barra\\"><span class=\\"escena-titulo\\">Camina, y no es un robot &middot; 8 segundos</span></div>\\n        <div class=\\"lienzo\\" style=\\"padding:0;background:#000;display:flex;justify-content:center\\">\\n          <video controls preload=\\"none\\" muted playsinline style=\\"width:auto;max-width:100%;max-height:60vh;display:block\\"\\n                 poster=\\"../../../video/c7-caminante.jpg\\">\\n            <source src=\\"../../../video/c7-caminante.mp4\\" type=\\"video/mp4\\">\\n            Tu navegador no puede reproducir v&iacute;deo.\\n            <a href=\\"../../../video/c7-caminante.mp4\\">Desc&aacute;rgalo aqu&iacute;</a>.\\n          </video>\\n        </div>\\n        <div class=\\"pie\\" role=\\"status\\" aria-live=\\"polite\\" aria-atomic=\\"true\\">Baja la rampa &eacute;l solo, con paso de persona. Y por dentro <b>no hay nada</b>: ni motor, ni sensor, ni programa, ni una pila. Lo &uacute;nico que lo mueve es la gravedad y la forma de sus piernas. Si la frontera fuera <i>parecerlo</i> o <i>moverse solo</i>, esto ser&iacute;a un robot &mdash; y no lo es, porque no se entera de nada.<br><br>V&iacute;deo de <b>Steven H. Collins</b>, v&iacute;a Wikimedia Commons, <b>CC BY-SA 3.0</b>, la misma licencia de esta p&aacute;gina.</div>\\n      </div>",
  "modo": "antes"
 },
 {
  "pagina": "4eso/Tecnologia/tema7/index.html",
  "img": "c7-robot-paquetes.mp4",
  "ancla": "<i>parecerlo</i> o <i>moverse solo</i>, esto ser&iacute;a un robot &mdash; y no lo es, porque no se entera de nada.<br><br>V&iacute;deo de <b>Steven H. Collins</b>, v&iacute;a Wikimedia Commons, <b>CC BY-SA 3.0</b>, la misma licencia de esta p&aacute;gina.</div>\\n      </div>",
  "figura": "<div class=\\"escena\\" id=\\"esc-robot-paquetes\\">\\n        <div class=\\"escena-barra\\"><span class=\\"escena-titulo\\">Esto s&iacute; lo es &middot; 8 segundos</span></div>\\n        <div class=\\"lienzo\\" style=\\"padding:0;background:#000;display:flex;justify-content:center\\">\\n          <video controls preload=\\"none\\" muted playsinline style=\\"width:auto;max-width:100%;max-height:60vh;display:block\\"\\n                 poster=\\"../../../video/c7-robot-paquetes.jpg\\">\\n            <source src=\\"../../../video/c7-robot-paquetes.mp4\\" type=\\"video/mp4\\">\\n            Tu navegador no puede reproducir v&iacute;deo.\\n            <a href=\\"../../../video/c7-robot-paquetes.mp4\\">Desc&aacute;rgalo aqu&iacute;</a>.\\n          </video>\\n        </div>\\n        <div class=\\"pie\\" role=\\"status\\" aria-live=\\"polite\\" aria-atomic=\\"true\\">El mismo criterio, al rev&eacute;s. Este brazo no repite un movimiento aprendido: las bolsas llegan <b>cada vez en un sitio distinto</b>, y &eacute;l mira, decide y coge. Qu&iacute;tale la c&aacute;mara y no puede hacer nada &mdash; ah&iacute; est&aacute; la frontera de la sesi&oacute;n: <b>enterarse de lo que hay fuera</b>.<br><br>V&iacute;deo de <i>newscreators</i>, v&iacute;a Wikimedia Commons, <b>CC BY 3.0</b>.</div>\\n\\n      <div class=\\"escena\\" id=\\"esc-robot-baila\\">\\n        <div class=\\"escena-barra\\"><span class=\\"escena-titulo\\">Y este, &iquest;qu&eacute; es? &middot; 24 segundos</span></div>\\n        <div class=\\"lienzo\\" style=\\"padding:0;background:#000;display:flex;justify-content:center\\">\\n          <video controls preload=\\"none\\" muted playsinline style=\\"width:auto;max-width:100%;max-height:60vh;display:block\\"\\n                 poster=\\"../../../video/c7-robot-baila.jpg\\">\\n            <source src=\\"../../../video/c7-robot-baila.mp4\\" type=\\"video/mp4\\">\\n            Tu navegador no puede reproducir v&iacute;deo.\\n            <a href=\\"../../../video/c7-robot-baila.mp4\\">Desc&aacute;rgalo aqu&iacute;</a>.\\n          </video>\\n        </div>\\n        <div class=\\"pie\\" role=\\"status\\" aria-live=\\"polite\\" aria-atomic=\\"true\\">Shenzhen, marzo de 2025: un humanoide chino baila la escena del hacha de <i>Kung Fu Sion</i> con dos personas, y lo hace mejor que ellas. Aqu&iacute; la frontera no est&aacute; tan clara, y por eso vale la pena pararse: la <b>coreograf&iacute;a va grabada</b> &mdash;eso es programa, como el lavavajillas&mdash;, pero el equilibrio <b>no</b>: mientras baila est&aacute; midiendo su propia inclinaci&oacute;n cientos de veces por segundo y corrigiendo los tobillos, o se caer&iacute;a al primer giro. O sea que s&iacute; se entera de algo del mundo: <b>de s&iacute; mismo</b>. &iquest;Basta eso para llamarlo robot? Discutidlo con el criterio de la sesi&oacute;n en la mano.<br><br>V&iacute;deo de <b>China News Service</b>, v&iacute;a Wikimedia Commons, <b>CC BY 4.0</b>. Recortado y recomprimido.</div>\\n      </div>\\n      </div>",
  "modo": "antes"
 },
 {
  "pagina": "2eso/TyD/tema7/index.html",
  "img": "u5-vibrador-olivos.mp4",
  "ancla": "</p>\\n        <p>Merece la pena pensarlo: durante catorce a&ntilde;os, la mejor m&aacute;quina de vapor del\\n           mundo llev&oacute; un mecanismo peor <b>por un motivo legal, no t&eacute;cnico</b>. La\\n           tecnolog&iacute;a no la deciden solo los ingenieros.</p>\\n      </div>",
  "figura": "<div class=\\"escena\\" id=\\"esc-olivos\\">\\n        <div class=\\"escena-barra\\"><span class=\\"escena-titulo\\">Transformar el movimiento, en el campo &middot; 18 segundos</span></div>\\n        <div class=\\"lienzo\\" style=\\"padding:0;background:#000;display:flex;justify-content:center\\">\\n          <video controls preload=\\"none\\" muted playsinline style=\\"width:auto;max-width:100%;max-height:60vh;display:block\\"\\n                 poster=\\"../../../video/u5-vibrador-olivos.jpg\\">\\n            <source src=\\"../../../video/u5-vibrador-olivos.mp4\\" type=\\"video/mp4\\">\\n            Tu navegador no puede reproducir v&iacute;deo.\\n            <a href=\\"../../../video/u5-vibrador-olivos.mp4\\">Desc&aacute;rgalo aqu&iacute;</a>.\\n          </video>\\n        </div>\\n        <div class=\\"pie\\" role=\\"status\\" aria-live=\\"polite\\" aria-atomic=\\"true\\">Una cosechadora de aceituna. El tractor solo sabe hacer una cosa: <b>girar</b>. Y lo que hace falta para que caiga la aceituna no es girar, es <b>sacudir</b>. Dentro de esa pinza hay unas masas descentradas dando vueltas: al girar tiran hacia un lado, media vuelta despu&eacute;s tiran hacia el otro, y el &aacute;rbol entero vibra. Giro convertido en vaiv&eacute;n, como la biela, pero a cuarenta sacudidas por segundo.<br><br>V&iacute;deo de <b>Jared Gulian</b>, v&iacute;a Wikimedia Commons, <b>CC BY 3.0</b>. Recortado y recomprimido.</div>\\n      </div>",
  "modo": "antes"
 },
 {
  "pagina": "4eso/Tecnologia/tema7/index.html",
  "img": "c7-robot-baila.mp4",
  "ancla": "</b>, y &eacute;l mira, decide y coge. Qu&iacute;tale la c&aacute;mara y no puede hacer nada &mdash; ah&iacute; est&aacute; la frontera de la sesi&oacute;n: <b>enterarse de lo que hay fuera</b>.<br><br>V&iacute;deo de <i>newscreators</i>, v&iacute;a Wikimedia Commons, <b>CC BY 3.0</b>.</div>",
  "figura": "<div class=\\"escena\\" id=\\"esc-robot-baila\\">\\n        <div class=\\"escena-barra\\"><span class=\\"escena-titulo\\">Y este, &iquest;qu&eacute; es? &middot; 24 segundos</span></div>\\n        <div class=\\"lienzo\\" style=\\"padding:0;background:#000;display:flex;justify-content:center\\">\\n          <video controls preload=\\"none\\" muted playsinline style=\\"width:auto;max-width:100%;max-height:60vh;display:block\\"\\n                 poster=\\"../../../video/c7-robot-baila.jpg\\">\\n            <source src=\\"../../../video/c7-robot-baila.mp4\\" type=\\"video/mp4\\">\\n            Tu navegador no puede reproducir v&iacute;deo.\\n            <a href=\\"../../../video/c7-robot-baila.mp4\\">Desc&aacute;rgalo aqu&iacute;</a>.\\n          </video>\\n        </div>\\n        <div class=\\"pie\\" role=\\"status\\" aria-live=\\"polite\\" aria-atomic=\\"true\\">Shenzhen, marzo de 2025: un humanoide chino baila la escena del hacha de <i>Kung Fu Sion</i> con dos personas, y lo hace mejor que ellas. Aqu&iacute; la frontera no est&aacute; tan clara, y por eso vale la pena pararse: la <b>coreograf&iacute;a va grabada</b> &mdash;eso es programa, como el lavavajillas&mdash;, pero el equilibrio <b>no</b>: mientras baila est&aacute; midiendo su propia inclinaci&oacute;n cientos de veces por segundo y corrigiendo los tobillos, o se caer&iacute;a al primer giro. O sea que s&iacute; se entera de algo del mundo: <b>de s&iacute; mismo</b>. &iquest;Basta eso para llamarlo robot? Discutidlo con el criterio de la sesi&oacute;n en la mano.<br><br>V&iacute;deo de <b>China News Service</b>, v&iacute;a Wikimedia Commons, <b>CC BY 4.0</b>. Recortado y recomprimido.</div>\\n      </div>",
  "modo": "antes"
 },
 {
  "pagina": "4eso/Tecnologia/tema2/index.html",
  "img": "c2-protesis.jpg",
  "ancla": "<b>dise&ntilde;o</b> y no de taller:\\n         <b>cada t&eacute;cnica te obliga a dibujar la pieza de otra manera</b>. No se elige la\\n         t&eacute;cnica al final, mirando el plano terminado. Se elige antes, porque decide lo que\\n         puedes dibujar.</p>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/c2-protesis.jpg\\" width=\\"1200\\" height=\\"848\\" loading=\\"lazy\\"\\n             alt=\\"Mano prot&eacute;sica impresa en 3D, con los dedos articulados mediante tornillos y las capas del filamento a la vista\\">\\n        <figcaption>Una mano prot&eacute;sica impresa y montada por investigadores de la FDA. Sirve para\\n          cerrar la comparaci&oacute;n de esta sesi&oacute;n, porque <b>las otras dos maneras no pueden\\n          hacerla</b>: esos huecos interiores no los saca una fresa, y un molde para una sola pieza\\n          costar&iacute;a m&aacute;s que la m&aacute;quina. Hay dos cosas que mirar de cerca: las\\n          <b>l&iacute;neas horizontales</b> del filamento, que son las capas y tambi&eacute;n por donde\\n          rompe si tiras en esa direcci&oacute;n, y que las articulaciones van <b>atornilladas</b> y no\\n          pegadas &mdash; con lo que sabes de la sesi&oacute;n anterior, ya puedes decir por qu&eacute;.\\n          <br><br>Foto de la <b>U.S. Food and Drug Administration</b>, v&iacute;a Wikimedia Commons,\\n          <b>dominio p&uacute;blico</b>.</figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "4eso/Tecnologia/tema1/index.html",
  "img": "problem-vs-solution.svg",
  "ancla": "<b>ejecutar</b> la frase encima de ellos, como si fuera una\\n         cuenta. Si la frase no se puede ejecutar, en junio no podr&eacute;is demostrar que el\\n         proyecto ha salido bien, y la nota ser&aacute; una discusi&oacute;n.</p>\\n\\n    </section>",
  "figura": "<figure class=\\"foto\\">\\n      <img src=\\"../../../img/problem-vs-solution.svg\\" width=\\"1000\\" height=\\"700\\" loading=\\"lazy\\"\\n           alt=\\"Diferencia cr&iacute;tica entre plantear un problema y proponer una soluci&oacute;n\\">\\n      <figcaption><strong>Un problema no es una idea:</strong> Un problema describe qu&eacute; va mal; una soluci&oacute;n propone c&oacute;mo arreglarlo. Si confundes los dos, no tienes criterios para comparar las opciones ni para elegir entre ellas.\\n        <span class=\\"credito\\">Elaboraci&oacute;n propia &middot; CC BY-SA 4.0</span>\\n      </figcaption>\\n    </figure>",
  "modo": "antes"
 },
 {
  "pagina": "4eso/Tecnologia/tema1/index.html",
  "img": "design-thinking-process.svg",
  "ancla": "<b>25'</b> Teor&iacute;a</span><span class=\\"min\\"><b>20'</b> Pr&aacute;ctica</span><span class=\\"min\\"><b>5'</b> Cierre</span></div>\\n      <div class=\\"chips\\"><span class=\\"chip\\">CE1 &middot; 1.2</span><span class=\\"chip\\">CE5 &middot; 5.1</span><span class=\\"chip sab\\">A.1</span><span class=\\"chip sab\\">A.3</span></div>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/design-thinking-process.svg\\" width=\\"1200\\" height=\\"600\\" loading=\\"lazy\\"\\n             alt=\\"Design Thinking: 6 fases - Empatizar, Definir, Idear, Prototipar, Validar, Implementar, con retroalimentaci&oacute;n iterativa\\">\\n        <figcaption>El <b>Design Thinking</b> en seis fases: <b>Empatizar</b> (entender el usuario), <b>Definir</b> (concretar el problema), <b>Idear</b> (generar muchas opciones), <b>Prototipar</b> (construir r&aacute;pido y barato), <b>Validar</b> (probar con usuarios), <b>Implementar</b> (versi&oacute;n final). La flecha roja de retroalimentaci&oacute;n indica que si falla, vuelves atr&aacute;s a idear, no al principio. Cada iteraci&oacute;n ense&ntilde;a m&aacute;s que cien reuniones de planificaci&oacute;n.\\n          <span class=\\"credito\\">Elaboraci&oacute;n propia &middot; CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "4eso/Tecnologia/tema1/index.html",
  "img": "project-phases-timeline.svg",
  "ancla": "</b> Pr&aacute;ctica</span><span class=\\"min\\"><b>10'</b> Cierre y test</span></div>\\n      <div class=\\"chips\\"><span class=\\"chip\\">CE1 &middot; 1.3</span><span class=\\"chip\\">CE3 &middot; 3.1</span><span class=\\"chip\\">CE5 &middot; 5.1</span><span class=\\"chip sab\\">A.1</span><span class=\\"chip sab\\">A.1.4</span></div>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/project-phases-timeline.svg\\" width=\\"1000\\" height=\\"500\\" loading=\\"lazy\\"\\n             alt=\\"Fases del proyecto: Planificaci&oacute;n, Dise&ntilde;o, Construcci&oacute;n, Pruebas y Presentaci&oacute;n\\">\\n        <figcaption>Las <b>cinco fases de un proyecto tecnol&oacute;gico</b>: planificaci&oacute;n, dise&ntilde;o, construcci&oacute;n, pruebas y presentaci&oacute;n. Cu&aacute;nto dura cada una depende del proyecto, y la fase m&aacute;s larga no es por eso la cr&iacute;tica: el <b>camino cr&iacute;tico</b> es la cadena de tareas con holgura <b>cero</b>, y es un retraso en una de esas tareas el que retrasa el proyecto entero. La escena de esta sesi&oacute;n lo calcula.\\n          <span class=\\"credito\\">Elaboraci&oacute;n propia &middot; CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "4eso/Tecnologia/tema2/index.html",
  "img": "cad-workflow.svg",
  "ancla": "<span class=\\"min\\"><b>25'</b> Teor&iacute;a</span><span class=\\"min\\"><b>20'</b> Pr&aacute;ctica</span><span class=\\"min\\"><b>5'</b> Cierre</span></div>\\n      <div class=\\"chips\\"><span class=\\"chip\\">CE2 &middot; 2.1</span><span class=\\"chip\\">CE3 &middot; 3.1</span><span class=\\"chip sab\\">A.2 &middot; A.3.1</span></div>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/cad-workflow.svg\\" width=\\"1000\\" height=\\"550\\" loading=\\"lazy\\"\\n             alt=\\"Flujo CAD: Idea, Dibujo 2D, Modelo 3D, Simulaci&oacute;n, CAM/Fabricaci&oacute;n\\">\\n        <figcaption>El <b>flujo de CAD</b> (Computer-Aided Design): (1) <b>Idea</b> en papel, (2) <b>Dibujo 2D</b> con vistas ortogonales y cotas precisas, (3) <b>Modelo 3D</b> param&eacute;trico (todo conectado: cambiar una cota actualiza la pieza entera), (4) <b>Simular</b> (fuerzas, movimiento, esfuerzos), (5) <b>CAM</b> (traducir a G-code para CNC o impresora 3D). Software: AutoCAD/SolidWorks para industria, FreeCAD/Tinkercad para educaci&oacute;n. La ventaja: ver la pieza en 3D antes de fabricar. Lo que no hace es quitar los errores: la tolerancia de cada m&aacute;quina, la sangr&iacute;a del l&aacute;ser y el agujero que encoge al exportar el STL siguen ah&iacute;, y de eso va este tema.\\n          <span class=\\"credito\\">Elaboraci&oacute;n propia &middot; CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "4eso/Tecnologia/tema2/index.html",
  "img": "manufacturing-methods.svg",
  "ancla": "<b>15'</b> Pr&aacute;ctica</span><span class=\\"min\\"><b>10'</b> Test</span><span class=\\"min\\"><b>5'</b> Cierre</span></div>\\n      <div class=\\"chips\\"><span class=\\"chip\\">CE2 &middot; 2.1 &middot; 2.2</span><span class=\\"chip\\">CE5 &middot; 5.1</span><span class=\\"chip sab\\">A.3 &middot; D.4</span></div>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/manufacturing-methods.svg\\" width=\\"1000\\" height=\\"600\\" loading=\\"lazy\\"\\n             alt=\\"M&eacute;todos de fabricaci&oacute;n: Sustractiva (quitar material) frente a Aditiva (a&ntilde;adir material capa a capa)\\">\\n        <figcaption><b>Fabricaci&oacute;n sustractiva frente a aditiva</b>. La sustractiva parte de un bloque o un tablero y le <b>quita</b> material (sierra, taladro, lima, cortadora l&aacute;ser): lo que sobra es residuo. La aditiva lo <b>a&ntilde;ade</b> capa a capa (impresora 3D) y es la &uacute;nica que puede hacer formas huecas por dentro, pero es la m&aacute;s lenta: con una impresora para diez grupos, la cola dura casi dos semanas de clase. No hay una ganadora, y se elige antes de dibujar, porque cada t&eacute;cnica decide lo que puedes dibujar.\\n          <span class=\\"credito\\">Elaboraci&oacute;n propia &middot; CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "4eso/Tecnologia/tema3/index.html",
  "img": "material-lifecycle.svg",
  "ancla": "<p>Sumar las cinco con un m&eacute;todo comprobable se llama <b>an&aacute;lisis de ciclo de\\n           vida</b> (ACV). Est&aacute; normalizado en las <b>ISO 14040 y 14044</b>, que son las que\\n           dicen c&oacute;mo hay que hacerlo para que dos estudios distintos se puedan comparar.</p>\\n      </div>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/material-lifecycle.svg\\" width=\\"1000\\" height=\\"500\\" loading=\\"lazy\\"\\n             alt=\\"Ciclo de vida del material: Extracción, Procesamiento, Fabricación, Distribución, Uso, y opción de Reciclaje o Vertedero\\">\\n        <figcaption>El <b>ciclo de vida del material</b>: desde la extracción del mineral en la mina hasta el uso y el final del producto. Cada fase consume energía y genera residuos, y cuál pesa más depende del aparato: por eso la cuenta se hace etapa por etapa. La economía circular busca que el material vuelva a entrar (reciclaje) en lugar de acabar en vertedero, recuperando la energía ya invertida.\\n          <span class=\\"credito\\">Elaboración propia · CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "4eso/Tecnologia/tema3/index.html",
  "img": "embodied-energy-comparison.svg",
  "ancla": "<span class=\\"credito\\">UC Rusal Photo Gallery &middot; CC BY 2.0 &middot;\\n            <a href=\\"https://commons.wikimedia.org/wiki/File:Bratsk_Aluminium_Smelter_(34948024336).jpg\\" target=\\"_blank\\" rel=\\"noopener\\">Wikimedia Commons</a></span>\\n        </figcaption>\\n      </figure>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/embodied-energy-comparison.svg\\" width=\\"1000\\" height=\\"700\\" loading=\\"lazy\\"\\n             alt=\\"Energ&iacute;a incorporada de materiales: madera aserrada 10 MJ, acero 25 MJ, aluminio 186 MJ\\">\\n        <figcaption><b>La &quot;mochila energ&eacute;tica&quot; de cada material</b>. Un kilo de madera aserrada lleva incorporados unos 10 MJ (el contrachapado, 15); el acero, 25 MJ; el aluminio, 186 MJ. <b>No es lo mismo que fundir</b> (eso cuesta 1 MJ en el horno): es toda la energ&iacute;a del proceso: mina, refiner&iacute;a, transporte, electr&oacute;lisis en el caso del aluminio. Esta energ&iacute;a ya est&aacute; gastada el d&iacute;a que compras el material.\\n          <span class=\\"credito\\">Elaboraci&oacute;n propia &middot; CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "4eso/Tecnologia/tema4/index.html",
  "img": "open-closed-loop-control.svg",
  "ancla": "<b>lo &uacute;nico</b> que distingue los dos lazos.</p>\\n        <p><b>Perturbaci&oacute;n</b>: todo lo que cambia el resultado y no hab&iacute;as previsto.\\n           El fr&iacute;o, la puerta abierta, el conserje.</p>\\n      </div>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/open-closed-loop-control.svg\\" width=\\"1000\\" height=\\"700\\" loading=\\"lazy\\"\\n             alt=\\"Lazo abierto vs lazo cerrado: diferencia entre control sin sensor y control con realimentaci&oacute;n\\">\\n        <figcaption><b>Lazo abierto vs Lazo cerrado: la realimentaci&oacute;n es la clave</b>. En lazo abierto, das una orden y ya: la bomba bombea 30 segundos, punto. En lazo cerrado, un <b>sensor mide</b> qué pasó, un <b>comparador decide</b> si hay que cambiar la orden, y <b>realimenta</b> esa decisión al actuador. Resultado: el sistema se adapta al entorno en tiempo real.\\n          <span class=\\"credito\\">Elaboraci&oacute;n propia &middot; CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "4eso/Tecnologia/tema4/index.html",
  "img": "mechanical-advantage-levers.svg",
  "ancla": "</p>\\n      <p><b>Levantar</b> un peso y <b>girarlo desde un extremo</b> no son la misma cosa.</p>\\n\\n    </section>\\n    <section class=\\"bloque\\">\\n      <div class=\\"rotulo\\"><span class=\\"num\\">01</span> Teor&iacute;a &middot; 20 min</div>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/mechanical-advantage-levers.svg\\" width=\\"1000\\" height=\\"600\\" loading=\\"lazy\\"\\n             alt=\\"Palancas de clase 1 y clase 2 mostrando ventaja mec&aacute;nica y distancias\\">\\n        <figcaption>Las <b>palancas como m&aacute;quinas simples</b> demuestran el principio fundamental de la mec&aacute;nica: <b>cambias fuerza por distancia</b>. En la palanca de clase 1 el fulcro est&aacute; entre la fuerza y la carga: si est&aacute; m&aacute;s cerca de la carga, aplicas menos fuerza pero recorres m&aacute;s distancia; si est&aacute; m&aacute;s cerca de tu mano, es al rev&eacute;s. La ventaja mec&aacute;nica es el cociente entre la distancia de entrada y la distancia de salida. La misma regla de oro aplica en todos los mecanismos: ganas en fuerza, pierdes en velocidad; ganas en velocidad, pierdes en fuerza.\\n          <span class=\\"credito\\">Elaboraci&oacute;n propia &middot; CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "4eso/Tecnologia/tema4/index.html",
  "img": "c4-cohete.jpg",
  "ancla": "</p>\\n        <p>Pero el grifo de tu ducha <b>no</b> es un interruptor. Lo abres <b>un poco</b>. Esta\\n           sesi&oacute;n va de darle a la m&aacute;quina ese &laquo;un poco&raquo;.</p>\\n      </div>",
  "figura": "<div class=\\"escena\\">\\n        <div class=\\"escena-barra\\"><span class=\\"escena-titulo\\">Control proporcional a tama&ntilde;o real &middot; 13 segundos</span></div>\\n        <div class=\\"lienzo\\" style=\\"padding:0;background:#000;display:flex;justify-content:center\\">\\n          <video controls preload=\\"none\\" muted playsinline style=\\"width:auto;max-width:100%;max-height:60vh;display:block\\"\\n                 poster=\\"../../../video/c4-cohete.jpg\\">\\n            <source src=\\"../../../video/c4-cohete.mp4\\" type=\\"video/mp4\\">\\n            Tu navegador no puede reproducir v&iacute;deo.\\n            <a href=\\"../../../video/c4-cohete.mp4\\">Desc&aacute;rgalo aqu&iacute;</a>.\\n          </video>\\n        </div>\\n        <div class=\\"pie\\">Los dos propulsores laterales de un Falcon Heavy, bajando a la vez. Un motor de cohete <b>no se enciende y se apaga</b> para frenar: eso ser&iacute;a todo-nada, y a esa velocidad la primera correcci&oacute;n de m&aacute;s te estrella. Lo que hace es <b>regular el empuje sin parar</b> seg&uacute;n lo que le queda por bajar, que es justo lo que acabas de programar t&uacute;: cuanto mayor es el error, mayor la respuesta. Y llega con velocidad casi cero al tocar.<br><br>V&iacute;deo de <b>SpaceX</b>, v&iacute;a Wikimedia Commons, <b>CC BY 2.0</b>. Recomprimido para la web.</div>\\n      </div>",
  "modo": "antes"
 },
 {
  "pagina": "4eso/Tecnologia/tema5/index.html",
  "img": "transistor-basics.svg",
  "ancla": "</p>\\n      </div>\\n\\n    </section>\\n    <section class=\\"bloque\\">\\n      <div class=\\"rotulo\\"><span class=\\"num\\">01</span> Teor&iacute;a &middot; 25 min</div>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/transistor-basics.svg\\" width=\\"1000\\" height=\\"600\\" loading=\\"lazy\\"\\n             alt=\\"El transistor como interruptor y amplificador, con aplicaciones prácticas\\">\\n        <figcaption>El <b>transistor</b> es el componente que revolucionó la electrónica moderna: permite que una pequeña corriente de control abra o cierre el paso a una corriente mucho mayor. Como interruptor electrónico, permite que Arduino controle motores, bombas y electroválvulas. Como amplificador, es la base de radios, equipos de audio y toda la electrónica analógica. Inventado en 1947, un transistor moderno cuesta apenas 1 céntimo.\\n          <span class=\\"credito\\">Elaboraci&oacute;n propia &middot; CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "4eso/Tecnologia/tema6/index.html",
  "img": "iot-system-architecture.svg",
  "ancla": "</b>: la direcci&oacute;n del servidor y el <b>protocolo</b>, que es el\\n              idioma en que se escribe el mensaje.</li>\\n        </ul>\\n        <p>Todo lo dem&aacute;s que viaja es <b>sobre</b>: sirve para que el mensaje llegue y se\\n           entienda, no para medir nada.</p>\\n      </div>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/iot-system-architecture.svg\\" width=\\"1000\\" height=\\"700\\" loading=\\"lazy\\"\\n             alt=\\"Arquitectura IoT: capa de sensores, capa de procesamiento local con Arduino, capa de nube e inteligencia\\">\\n        <figcaption><b>De los sensores a las decisiones</b>. En el huerto hay sensores que miden humedad, temperatura y luz. Un Arduino local los lee y toma decisiones simples (si humedad &lt; 40%, riega). <b>Sin internet, funciona igual: es automatismo</b>. Pero si se conecta a la nube, puede aprender. La nube ve el histórico, detecta patrones (a las 9 AM siempre hace más calor), y optimiza: \\"próxima vez, riega solo 15 minutos\\". Eso es IoT: <b>local + inteligencia remota</b>.\\n          <span class=\\"credito\\">Elaboraci&oacute;n propia &middot; CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "4eso/Tecnologia/tema7/index.html",
  "img": "robot-vs-automation.svg",
  "ancla": "<span class=\\"credito\\">Chris Bartle &middot; CC BY 2.0 &middot;\\n            <a href=\\"https://commons.wikimedia.org/wiki/File:Roomba_time-lapse.jpg\\" target=\\"_blank\\" rel=\\"noopener\\">Wikimedia Commons</a></span>\\n        </figcaption>\\n      </figure>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/robot-vs-automation.svg\\" width=\\"1000\\" height=\\"600\\" loading=\\"lazy\\"\\n             alt=\\"Comparaci&oacute;n entre un automatismo (lavavajillas) y un robot (aspiradora): el automatismo ejecuta sin enterarse, el robot percibe el entorno\\">\\n        <figcaption>La frontera: <b>un robot percibe el entorno y decide basándose en ello</b>. Un automatismo ejecuta su programa pase lo que pase. El lavavajillas no es un robot, aunque sea automático; la Roomba sí, aunque sea más simple.\\n          <span class=\\"credito\\">Elaboración propia · CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "4eso/Tecnologia/tema7/index.html",
  "img": "c7-caminante.jpg",
  "ancla": "<a href=\\"https://www.youtube.com/watch?v=cwf-cURBUkI\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "figura": "<div class=\\"escena\\">\\n        <div class=\\"escena-barra\\"><span class=\\"escena-titulo\\">Camina, y no es un robot &middot; 8 segundos</span></div>\\n        <div class=\\"lienzo\\" style=\\"padding:0;background:#000;display:flex;justify-content:center\\">\\n          <video controls preload=\\"none\\" muted playsinline style=\\"width:auto;max-width:100%;max-height:60vh;display:block\\"\\n                 poster=\\"../../../video/c7-caminante.jpg\\">\\n            <source src=\\"../../../video/c7-caminante.mp4\\" type=\\"video/mp4\\">\\n            Tu navegador no puede reproducir v&iacute;deo.\\n            <a href=\\"../../../video/c7-caminante.mp4\\">Desc&aacute;rgalo aqu&iacute;</a>.\\n          </video>\\n        </div>\\n        <div class=\\"pie\\">Baja la rampa &eacute;l solo, con paso de persona. Y por dentro <b>no hay nada</b>: ni motor, ni sensor, ni programa, ni una pila. Lo &uacute;nico que lo mueve es la gravedad y la forma de sus piernas. Si la frontera fuera <i>parecerlo</i> o <i>moverse solo</i>, esto ser&iacute;a un robot &mdash; y no lo es, porque no se entera de nada.<br><br>V&iacute;deo de <b>Steven H. Collins</b>, v&iacute;a Wikimedia Commons, <b>CC BY-SA 3.0</b>, la misma licencia de esta p&aacute;gina.</div>\\n      </div>",
  "modo": "antes"
 },
 {
  "pagina": "4eso/Tecnologia/tema7/index.html",
  "img": "motor-types-comparison.svg",
  "ancla": "<b>calibrar</b>.</p>\\n        <p><b>Y el encoder tampoco es magia.</b> Cuenta lo que gira <b>la rueda</b>, no lo que avanza\\n           <b>el robot</b>. Si la rueda patina, el encoder dice que todo va perfecto. Por eso en la\\n           escena la moqueta le hace lo mismo que al paso a paso.</p>\\n      </div>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/motor-types-comparison.svg\\" width=\\"1000\\" height=\\"700\\" loading=\\"lazy\\"\\n             alt=\\"Comparaci&oacute;n de tres tipos de motores: DC (r&aacute;pido, barato, no sabe d&oacute;nde est&aacute;), servo (posici&oacute;n exacta, 0-180 grados), stepper (preciso paso a paso)\\">\\n        <figcaption>Tres de los motores de la tabla: <b>corriente continua, servo y paso a paso</b>. El de corriente continua no sabe dónde está. El servo va a un ángulo exacto, pero solo en unos 180°. El paso a paso lo sabe a base de contar pasos. La escena de arriba no lleva servo: compara la corriente continua por tiempo, el paso a paso y la corriente continua con encoder.\\n          <span class=\\"credito\\">Elaboración propia · CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "4eso/Tecnologia/tema7/index.html",
  "img": "state-machine-concept.svg",
  "ancla": "</p>\\n        <p>Las casillas que dejes en blanco son, exactamente, <b>por donde se va a romper</b> el\\n           automatismo el d&iacute;a que lo pongas en el pasillo.</p>\\n      </div>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/state-machine-concept.svg\\" width=\\"1000\\" height=\\"700\\" loading=\\"lazy\\"\\n             alt=\\"Concepto de m&aacute;quina de estados: semáforo con tres estados (rojo, amarillo, verde) y transiciones entre ellos; ejemplo de Roomba con estados (espera, explorando, obstáculo, cargando)\\">\\n        <figcaption><b>Máquina de estados</b>: cada círculo es un estado, las flechas son transiciones, y cada transición tiene una condición (cuándo sucede). El semáforo es determinista (siempre pasa el mismo tiempo). La Roomba tiene transiciones basadas en sensores: si choca, gira; si batería baja, va a cargarse.\\n          <span class=\\"credito\\">Elaboración propia · CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "4eso/Tecnologia/tema8/index.html",
  "img": "product-lifecycle-sustainability.svg",
  "ancla": "</p>\\n        <p>F&iacute;jate en lo que dice ese 76 %: <b>fabricarlo pesa cuatro veces m&aacute;s que\\n           usarlo</b>. Gu&aacute;rdalo, porque en la sesi&oacute;n 3 lo vamos a necesitar entero.</p>\\n      </div>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/product-lifecycle-sustainability.svg\\" width=\\"1000\\" height=\\"700\\" loading=\\"lazy\\"\\n             alt=\\"Ciclo de vida de un producto en cinco fases, y el reparto de su huella en un m&oacute;vil, el iPhone 17 de 256 GB: fabricarlo 76 %, cargarlo 18 %, traerlo 4 % y deshacerse de &eacute;l 1 %\\">\\n        <figcaption><b>D&oacute;nde est&aacute; el impacto ambiental real</b>. El ciclo de vida de un producto pasa por cinco fases, y cu&aacute;l pesa m&aacute;s depende del aparato. En un m&oacute;vil manda la <b>fabricaci&oacute;n</b>: en el iPhone 17 de arriba, fabricarlo es el 76 % y cargarlo durante tres a&ntilde;os, el 18 %. Por eso lo que m&aacute;s baja su huella es <b>que dure</b>: la fabricaci&oacute;n se paga una sola vez y se reparte entre los a&ntilde;os que se use.\\n          <span class=\\"credito\\">Elaboraci&oacute;n propia &middot; CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "4eso/Tecnologia/tema9/index.html",
  "img": "appropriate-technology.svg",
  "ancla": "</b> Quiere\\n           decir <b>adecuada a ese sitio</b>. En vuestro instituto, con enchufe, wifi, taller y\\n           alguien que sabe, un Arduino <b>s&iacute;</b> es tecnolog&iacute;a apropiada. En un huerto\\n           a tres kil&oacute;metros, puede que no.</p>\\n      </div>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/appropriate-technology.svg\\" width=\\"1000\\" height=\\"700\\" loading=\\"lazy\\"\\n             alt=\\"Tecnolog&iacute;a apropiada vs inadecuada: ejemplo de riego autom&aacute;tico con IA versus sensor de humedad y electrov&aacute;lvula\\">\\n        <figcaption><b>Tecnolog&iacute;a apropiada vs inadecuada</b>. Un robot inteligente con IA para riego es demasiado para la tarea, cuesta miles de euros, se rompe sin remedio y falla por completo si se daña. Un simple sensor de humedad m&aacute;s una electrov&aacute;lvula es <b>la soluci&oacute;n justa</b>: cuesta decenas de euros, dura a&ntilde;os, y si falla se cambia en minutos.\\n          <span class=\\"credito\\">Elaboraci&oacute;n propia &middot; CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "4eso/Tecnologia/tema9/index.html",
  "img": "evaluation-criteria-matrix.svg",
  "ancla": "<b>dedicarle cinco segundos a algo es\\n           exactamente igual que no dedic&aacute;rselos</b>. En la r&uacute;brica no hay medio punto\\n           por mencionar. Lo que se mide es lo que se demuestra.</p>\\n      </div>\\n\\n    </section>",
  "figura": "<figure class=\\"foto\\">\\n      <img src=\\"../../../img/evaluation-criteria-matrix.svg\\" width=\\"1000\\" height=\\"700\\" loading=\\"lazy\\" alt=\\"Matriz de evaluación de rúbrica: criterios de puntuación para proyecto de riego automático\\">\\n      <figcaption><b>Matriz de evaluación.</b> Una rúbrica hace tres cosas: (1) sabes antes de empezar exactamente qué se va a valorar, (2) todos los profesores puntúan igual porque usan los mismos criterios, (3) tú puedes mejorar sabiendo precisamente dónde están los puntos. La rúbrica no es castigo, es transparencia.\\n        <span class=\\"credito\\">Elaboración propia &middot; CC BY-SA 4.0</span>\\n      </figcaption>\\n    </figure>",
  "modo": "antes"
 },
 {
  "pagina": "4eso/Tecnologia/tema5/index.html",
  "img": "transistor-switch-concept.svg",
  "ancla": "<p>Mira las cuatro barras de la escena. Cambia la carga, cambia la resistencia de base y mira\\n         cu&aacute;ndo se pone verde el letrero.</p>\\n\\n      <div class=\\"escena\\" id=\\"esc-tr\\">\\n        <div class=\\"escena-barra\\">\\n          <span class=\\"escena-titulo\\">",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/transistor-switch-concept.svg\\" width=\\"1000\\" height=\\"700\\" loading=\\"lazy\\"\\n             alt=\\"El transistor como interruptor: comparaci&oacute;n entre base sin se&ntilde;al y con se&ntilde;al\\">\\n        <figcaption><b>El transistor como interruptor inteligente</b>. Con 0 V en la base: transistor bloqueado, comportamiento como interruptor ABIERTO, no fluye corriente. Con 5 V en la base: transistor conduciendo (saturado), comportamiento como interruptor CERRADO, fluye corriente. Una corriente peque&ntilde;a en la base (~10 mA) controla una corriente enorme en el colector (~500 mA): es la amplificaci&oacute;n.\\n          <span class=\\"credito\\">Elaboraci&oacute;n propia &middot; CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
  "modo": "despues"
 },
 {
  "pagina": "4eso/Tecnologia/tema6/index.html",
  "img": "iot-architecture.svg",
  "ancla": "</section>\\n    <section class=\\"bloque\\">\\n      <div class=\\"rotulo\\"><span class=\\"num\\">01</span> Teor&iacute;a &middot; 25 min</div>\\n\\n      <p>Que esto no es nuevo lo demuestra la primera c&aacute;mara que se puso en la red, y lo que se\\n         ve&iacute;a en ella era tan importante como esto:</p>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/iot-architecture.svg\\" width=\\"1000\\" height=\\"400\\" loading=\\"lazy\\"\\n             alt=\\"Arquitectura IoT: Sensores y dispositivos inteligentes env&iacute;an datos a trav&eacute;s de gateway a la nube para an&aacute;lisis, que devuelven decisiones a los actuadores\\">\\n        <figcaption>La <b>arquitectura IoT</b> (Internet de las Cosas): sensores y dispositivos miden el mundo real y transmiten datos a trav&eacute;s de protocolos inal&aacute;mbricos (WiFi, Bluetooth, LTE, LoRaWAN) hasta un gateway que centraliza la comunicaci&oacute;n. Desde la nube se analizan los datos, y la aplicaci&oacute;n decide qu&eacute; hacer y env&iacute;a &oacute;rdenes de vuelta a los actuadores. El termostato inteligente de tu casa es exactamente esto: detecta temperatura, la env&iacute;a a internet, tu tel&eacute;fono compara con lo que deseas, y activa la calefacci&oacute;n.\\n          <span class=\\"credito\\">Elaboraci&oacute;n propia &middot; CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
  "modo": "despues"
 },
 {
  "pagina": "4eso/Tecnologia/tema8/index.html",
  "img": "embodied-energy-comparison.svg",
  "ancla": "<section class=\\"bloque\\">\\n      <div class=\\"rotulo\\"><span class=\\"num\\">02</span> Pr&aacute;ctica &middot; 20 min</div>\\n      <div class=\\"ficha\\">\\n        <div class=\\"ficha-cab\\">\\n          <span>Actividad 1 &middot; La huella de este aula, y la vuestra</span>\\n          <span class=\\"chips\\"><span class=\\"chip\\">6.1</span><span class=\\"chip\\">6.2</span><span class=\\"chip\\">D.1</span>",
  "figura": "<figure class=\\"foto\\">\\n      <img src=\\"../../../img/embodied-energy-comparison.svg\\" width=\\"1000\\" height=\\"700\\" loading=\\"lazy\\" alt=\\"Comparaci&oacute;n de energ&iacute;a incorporada: aluminio, acero, plástico, papel, madera - producción, transporte, reciclaje\\">\\n      <figcaption><b>Energ&iacute;a incorporada en materiales.</b> La electricidad que enciendes ahora tiene un costo claro: el kWh multiplicado por la potencia. Pero cada cosa que fabricas ya trae consigo horas de energía anterior: la que cost&oacute; extraer, refinar, transportar y transformar. El aluminio cuesta quince veces m&aacute;s que el acero en esa energ&iacute;a fantasma. Eso no quiere decir que no se use: solo que el coste est&aacute; repartido y no sale de tu factura.\\n        <span class=\\"credito\\">Elaboraci&oacute;n propia &middot; CC BY-SA 4.0</span>\\n      </figcaption>\\n    </figure>",
  "modo": "despues"
 },
 {
  "pagina": "4eso/Tecnologia/tema9/index.html",
  "img": "solution-impact-matrix.svg",
  "ancla": "<section class=\\"bloque\\">\\n      <div class=\\"rotulo\\"><span class=\\"num\\">02</span> Pr&aacute;ctica &middot; 20 min</div>\\n      <div class=\\"ficha\\">\\n        <div class=\\"ficha-cab\\">\\n          <span>Actividad 3 &middot; Ensayo cruzado, con la r&uacute;brica en la mano</span>\\n          <span class=\\"chips\\"><span class=\\"chip\\">2.1</span><span class=\\"chip\\">6.3</span>",
  "figura": "<figure class=\\"foto\\">\\n      <img src=\\"../../../img/solution-impact-matrix.svg\\" width=\\"1000\\" height=\\"700\\" loading=\\"lazy\\" alt=\\"Matriz de impacto: efectividad vs complejidad de soluciones tecnológicas\\">\\n      <figcaption><b>Matriz de impacto.</b> Antes de comprometerte con una solución, gráfica dos preguntas: ¿realmente resuelve el problema? (efectividad), ¿cuánto trabajo cuesta implementarla? (complejidad). La zona verde es donde quieres estar: alta efectividad, baja complejidad. La zona roja es la trampa: parece fácil pero no funciona.\\n        <span class=\\"credito\\">Elaboración propia &middot; CC BY-SA 4.0</span>\\n      </figcaption>\\n    </figure>",
  "modo": "despues"
 },
 {
  "pagina": "4eso/Tecnologia/tema1/index.html",
  "img": "ytb:1R9eg3MCfWk",
  "ancla": "data-vid=\\"1R9eg3MCfWk\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c1-observar\\" data-vid=\\"1R9eg3MCfWk\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: &iquest;Qu&eacute; es y c&oacute;mo hacer una observaci&oacute;n de usuarios?\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>&iquest;Qu&eacute; es y c&oacute;mo hacer una observaci&oacute;n de usuarios?</b>\\n            <span>Canal: Design Thinking 24 7 by Jorge Huertas</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">C&oacute;mo se observa sin preguntar y sin dirigir la respuesta, con ejemplos. Es la parte que m&aacute;s se salta todo el mundo. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=1R9eg3MCfWk\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema1/index.html",
  "img": "ytb:Kr2QQ_q7Axc",
  "ancla": "data-vid=\\"Kr2QQ_q7Axc\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c1-pugh\\" data-vid=\\"Kr2QQ_q7Axc\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Matriz Pugh: t&eacute;cnica de selecci&oacute;n de alternativas\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Matriz Pugh: t&eacute;cnica de selecci&oacute;n de alternativas</b>\\n            <span>Canal: Tecnol&oacute;gico de Monterrey | Innovaci&oacute;n Educativa</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">La versi&oacute;n original del m&eacute;todo, la de comparar contra una referencia. Est&aacute; explicada para universidad, pero se sigue bien. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=Kr2QQ_q7Axc\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema1/index.html",
  "img": "ytb:kbgiwFNxsG4",
  "ancla": "data-vid=\\"kbgiwFNxsG4\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c1-gantt\\" data-vid=\\"kbgiwFNxsG4\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: GanttProject &middot; tareas, dependencias y camino cr&iacute;tico\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>GanttProject &middot; tareas, dependencias y camino cr&iacute;tico</b>\\n            <span>Canal: VideoTutoriales Education</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">La herramienta que vais a usar en la pr&aacute;ctica. GanttProject es libre y gratuito, y marca el camino cr&iacute;tico solo. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=kbgiwFNxsG4\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema1/index.html",
  "img": "ytb:Odwo6i52skU",
  "ancla": "data-vid=\\"Odwo6i52skU\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c1-historial\\" data-vid=\\"Odwo6i52skU\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: C&oacute;mo usar el historial de versiones en Google Docs\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>C&oacute;mo usar el historial de versiones en Google Docs</b>\\n            <span>Canal: Javier Fern&aacute;ndez</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">D&oacute;nde est&aacute; el historial, c&oacute;mo se lee y c&oacute;mo se vuelve a una versi&oacute;n anterior. Es lo que vais a hacer en la pr&aacute;ctica; si el centro usa otra herramienta, el men&uacute; se llama igual. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=Odwo6i52skU\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema1/index.html",
  "img": "ytb:DZY3HGwBBVg",
  "ancla": "data-vid=\\"DZY3HGwBBVg\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c1-tresmin\\" data-vid=\\"DZY3HGwBBVg\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Mi Tesis en 3 minutos &middot; Lucila Garc&iacute;a\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Mi Tesis en 3 minutos &middot; Lucila Garc&iacute;a</b>\\n            <span>Canal: UNLitoral</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Una presentaci&oacute;n de tres minutos de verdad, de las de concurso. V&eacute;dla con el cron&oacute;metro y apuntad dos cosas: en qu&eacute; segundo entend&eacute;is de qu&eacute; va, y cu&aacute;ntas veces mira el papel. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=DZY3HGwBBVg\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema2/index.html",
  "img": "ytb:NC7AdFJDx4M",
  "ancla": "data-vid=\\"NC7AdFJDx4M\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c2-s1\\" data-vid=\\"NC7AdFJDx4M\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Acotaci&oacute;n de una pieza &middot; Tecnolog&iacute;a ESO\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Acotaci&oacute;n de una pieza &middot; Tecnolog&iacute;a ESO</b>\\n            <span>Francisco Jose</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">La misma pieza acotada de dos maneras distintas, con el l&aacute;piz encima del papel. <b>Nadie del proyecto lo ha visto entero:</b> est&aacute;n\\n          comprobados el t&iacute;tulo y el canal, no el contenido. El v&iacute;deo no se carga hasta\\n          que lo pulsas, y se reproduce sin cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;, <a href=\\"https://www.youtube.com/watch?v=NC7AdFJDx4M\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. Es obra de su autor y no forma parte del material publicado\\n          bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema2/index.html",
  "img": "ytb:961O25IM1ZI",
  "ancla": "data-vid=\\"961O25IM1ZI\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c2-s2\\" data-vid=\\"961O25IM1ZI\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Tolerancia dimensional: tipos de ajustes, c&aacute;lculo y selecci&oacute;n\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Tolerancia dimensional: tipos de ajustes, c&aacute;lculo y selecci&oacute;n</b>\\n            <span>Mat&iacute;as G. Ottini | Ingenier&iacute;a y Dise&ntilde;o</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Va m&aacute;s all&aacute; de lo que se pide aqu&iacute; &mdash;entra en la notaci&oacute;n ISO completa&mdash;, pero el porqu&eacute; de los tres tipos de ajuste est&aacute; muy bien contado. <b>Nadie del proyecto lo ha visto entero:</b> est&aacute;n\\n          comprobados el t&iacute;tulo y el canal, no el contenido. El v&iacute;deo no se carga hasta\\n          que lo pulsas, y se reproduce sin cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;, <a href=\\"https://www.youtube.com/watch?v=961O25IM1ZI\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. Es obra de su autor y no forma parte del material publicado\\n          bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema2/index.html",
  "img": "ytb:vcpl2baqin4",
  "ancla": "data-vid=\\"vcpl2baqin4\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c2-s3\\" data-vid=\\"vcpl2baqin4\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: &iquest;Cu&aacute;l es mejor? Bul&oacute;n, remache o soldadura\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>&iquest;Cu&aacute;l es mejor? Bul&oacute;n, remache o soldadura</b>\\n            <span>Tecnica X</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">La misma pregunta de esta sesi&oacute;n, con piezas de verdad y a escala de taller met&aacute;lico. <b>Nadie del proyecto lo ha visto entero:</b> est&aacute;n\\n          comprobados el t&iacute;tulo y el canal, no el contenido. El v&iacute;deo no se carga hasta\\n          que lo pulsas, y se reproduce sin cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;, <a href=\\"https://www.youtube.com/watch?v=vcpl2baqin4\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. Es obra de su autor y no forma parte del material publicado\\n          bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema2/index.html",
  "img": "ytb:Tz168RtMZJU",
  "ancla": "data-vid=\\"Tz168RtMZJU\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c2-s4\\" data-vid=\\"Tz168RtMZJU\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Aumenta la resistencia de tus piezas impresas en 3D: &iquest;qu&eacute; orientaci&oacute;n es mejor?\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Aumenta la resistencia de tus piezas impresas en 3D: &iquest;qu&eacute; orientaci&oacute;n es mejor?</b>\\n            <span>Control 3D</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">El ejemplo m&aacute;s claro de que <b>el dise&ntilde;o depende de c&oacute;mo se fabrique</b>: la misma pieza, girada, aguanta otra cosa. <b>Nadie del proyecto lo ha visto entero:</b> est&aacute;n\\n          comprobados el t&iacute;tulo y el canal, no el contenido. El v&iacute;deo no se carga hasta\\n          que lo pulsas, y se reproduce sin cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;, <a href=\\"https://www.youtube.com/watch?v=Tz168RtMZJU\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. Es obra de su autor y no forma parte del material publicado\\n          bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema2/index.html",
  "img": "ytb:pp1Uxy14neU",
  "ancla": "data-vid=\\"pp1Uxy14neU\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c2-s5\\" data-vid=\\"pp1Uxy14neU\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Tutorial completo de Dise&ntilde;o y Modelado 3D con Tinkercad - 2022\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Tutorial completo de Dise&ntilde;o y Modelado 3D con Tinkercad - 2022</b>\\n            <span>josemariafmTIC</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">La herramienta que vais a usar, de cero. Lo que aqu&iacute; interesa es la parte de <b>agrupar y vaciar</b>: es la resta que hace los agujeros. <b>Nadie del proyecto lo ha visto entero:</b> est&aacute;n\\n          comprobados el t&iacute;tulo y el canal, no el contenido. El v&iacute;deo no se carga hasta\\n          que lo pulsas, y se reproduce sin cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;, <a href=\\"https://www.youtube.com/watch?v=pp1Uxy14neU\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. Es obra de su autor y no forma parte del material publicado\\n          bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema2/index.html",
  "img": "ytb:rL6ZIaso5KA",
  "ancla": "data-vid=\\"rL6ZIaso5KA\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c2-s6\\" data-vid=\\"rL6ZIaso5KA\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Aplicaci&oacute;n para optimizar cortes de placas de aglomerados y triplay. CutList Optimizer\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Aplicaci&oacute;n para optimizar cortes de placas de aglomerados y triplay. CutList Optimizer</b>\\n            <span>Viejo Roble</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Un carpintero usando una herramienta web gratuita que hace exactamente lo que hace la escena de esta sesi&oacute;n, con tableros de verdad. F&iacute;jate en que lo primero que le pide es el <b>ancho de la sierra</b>. <b>Nadie del proyecto lo ha visto entero:</b> est&aacute;n\\n          comprobados el t&iacute;tulo y el canal, no el contenido. El v&iacute;deo no se carga hasta\\n          que lo pulsas, y se reproduce sin cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;, <a href=\\"https://www.youtube.com/watch?v=rL6ZIaso5KA\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. Es obra de su autor y no forma parte del material publicado\\n          bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema2/index.html",
  "img": "ytb:SmvnY4k2vRg",
  "ancla": "data-vid=\\"SmvnY4k2vRg\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c2-s7\\" data-vid=\\"SmvnY4k2vRg\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Cadenas de Cotas\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Cadenas de Cotas</b>\\n            <span>AGD Agencia de Gesti&oacute;n Dimensional</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Lo mismo que esta sesi&oacute;n contado por gente que se dedica a esto en la industria. Va m&aacute;s lejos de lo que se pide en 4.&ordm;, pero la idea de la <b>cota que no dibuja nadie</b> est&aacute; en el primer minuto. <b>Nadie del proyecto lo ha visto entero:</b> est&aacute;n\\n          comprobados el t&iacute;tulo y el canal, no el contenido. El v&iacute;deo no se carga hasta\\n          que lo pulsas, y se reproduce sin cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;, <a href=\\"https://www.youtube.com/watch?v=SmvnY4k2vRg\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. Es obra de su autor y no forma parte del material publicado\\n          bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema2/index.html",
  "img": "ytb:CcogpV4DjNs",
  "ancla": "data-vid=\\"CcogpV4DjNs\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c2-s8\\" data-vid=\\"CcogpV4DjNs\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Presentaci&oacute;n oral de un proyecto\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Presentaci&oacute;n oral de un proyecto</b>\\n            <span>ULLaudiovisual - Universidad de La Laguna</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Est&aacute; hecho para la universidad y se nota en el registro, as&iacute; que qu&eacute;date con la <b>estructura</b> y con lo que hace con las manos y con la voz, no con el vocabulario. <b>Nadie del proyecto lo ha visto entero:</b> est&aacute;n\\n          comprobados el t&iacute;tulo y el canal, no el contenido. El v&iacute;deo no se carga hasta\\n          que lo pulsas, y se reproduce sin cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;, <a href=\\"https://www.youtube.com/watch?v=CcogpV4DjNs\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. Es obra de su autor y no forma parte del material publicado\\n          bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema3/index.html",
  "img": "ytb:y3_KltoL5l8",
  "ancla": "data-vid=\\"y3_KltoL5l8\\"",
  "figura": "<div class=\\"video\\" id=\\"vid-c3-acv\\" data-vid=\\"y3_KltoL5l8\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: An&aacute;lisis del Ciclo de Vida del Producto (ACV) seg&uacute;n ISO\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>An&aacute;lisis del Ciclo de Vida del Producto (ACV) seg&uacute;n ISO</b>\\n            <span>Canal: TuProfeDeFP</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Repasa las etapas y las normas ISO 14040 y 14044 con un ejemplo hecho. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=y3_KltoL5l8\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema3/index.html",
  "img": "ytb:tJePkigCQ_U",
  "ancla": "data-vid=\\"tJePkigCQ_U\\"",
  "figura": "<div class=\\"video\\" id=\\"vid-c3-hall\\" data-vid=\\"tJePkigCQ_U\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Proceso Hall-H&eacute;roult / Electr&oacute;lisis de la al&uacute;mina para obtener aluminio\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Proceso Hall-H&eacute;roult / Electr&oacute;lisis de la al&uacute;mina para obtener aluminio</b>\\n            <span>Canal: Questions Of Science</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">La reacci&oacute;n y el montaje de la cuba, paso a paso. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=tJePkigCQ_U\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema3/index.html",
  "img": "ytb:_EA6VL1Zj0s",
  "ancla": "data-vid=\\"_EA6VL1Zj0s\\"",
  "figura": "<div class=\\"video\\" id=\\"vid-c3-planta\\" data-vid=\\"_EA6VL1Zj0s\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: As&iacute; funciona una planta de selecci&oacute;n\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>As&iacute; funciona una planta de selecci&oacute;n</b>\\n            <span>Canal: Ecoembes Espa&ntilde;a</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Las cintas, el im&aacute;n, las corrientes de Foucault y los separadores &oacute;pticos de la segunda etapa, funcionando. <b>Ojo con qui&eacute;n lo firma</b>: Ecoembes es el sistema que gestiona esos envases, o sea que tiene inter&eacute;s en que la planta salga bien en el v&iacute;deo. Para <b>ver la m&aacute;quina</b> vale; para las <b>cifras</b>, usa la escena y di de d&oacute;nde sale cada una. Eso es exactamente lo que aprendiste a preguntar en la sesi&oacute;n 1. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=_EA6VL1Zj0s\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema3/index.html",
  "img": "ytb:aB2mK5QKyvY",
  "ancla": "data-vid=\\"aB2mK5QKyvY\\"",
  "figura": "<div class=\\"video\\" id=\\"vid-c3-circular\\" data-vid=\\"aB2mK5QKyvY\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: &iquest;Qu&eacute; es la econom&iacute;a circular?\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>&iquest;Qu&eacute; es la econom&iacute;a circular?</b>\\n            <span>Canal: Ministerio para la Transici&oacute;n Ecol&oacute;gica y el Reto Demogr&aacute;fico</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">La versi&oacute;n oficial, en tres minutos y en espa&ntilde;ol. Mientras lo ves, haz lo que llevas dos sesiones aprendiendo: <b>cuenta cu&aacute;ntas veces dice &laquo;reciclar&raquo; y cu&aacute;ntas dice &laquo;reparar&raquo; o &laquo;prevenir&raquo;</b>, y comp&aacute;ralo con el orden del art&iacute;culo 4 que acabas de copiar. Un v&iacute;deo institucional tambi&eacute;n es alguien contando algo con un inter&eacute;s. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=aB2mK5QKyvY\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema4/index.html",
  "img": "ytb:2SHQTUvvVuM",
  "ancla": "data-vid=\\"2SHQTUvvVuM\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c4-s1\\" data-vid=\\"2SHQTUvvVuM\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Sistemas de control &middot; Rob&oacute;tica\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Sistemas de control &middot; Rob&oacute;tica</b>\\n            <span>STEM con Pablo</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Un repaso corto a lo de esta sesi&oacute;n, con m&aacute;s ejemplos de los dos tipos de lazo. <b>Nadie del proyecto lo ha visto entero:</b> est&aacute;n\\n          comprobados el t&iacute;tulo y el canal, no el contenido. El v&iacute;deo no se carga hasta\\n          que lo pulsas, y se reproduce sin cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;, <a href=\\"https://www.youtube.com/watch?v=2SHQTUvvVuM\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. Es obra de su autor y no forma parte del material publicado\\n          bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema4/index.html",
  "img": "ytb:zJ5TP_kkT2E",
  "ancla": "data-vid=\\"zJ5TP_kkT2E\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c4-s2\\" data-vid=\\"zJ5TP_kkT2E\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Tecnolog&iacute;a de control: tipos de sistemas de control autom&aacute;tico\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Tecnolog&iacute;a de control: tipos de sistemas de control autom&aacute;tico</b>\\n            <span>Guillermo A. Pennesi</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">El diagrama de bloques dibujado y explicado caja por caja. <b>Nadie del proyecto lo ha visto entero:</b> est&aacute;n\\n          comprobados el t&iacute;tulo y el canal, no el contenido. El v&iacute;deo no se carga hasta\\n          que lo pulsas, y se reproduce sin cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;, <a href=\\"https://www.youtube.com/watch?v=zJ5TP_kkT2E\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. Es obra de su autor y no forma parte del material publicado\\n          bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema4/index.html",
  "img": "ytb:i_GwbZLur2Y",
  "ancla": "data-vid=\\"i_GwbZLur2Y\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c4-s3\\" data-vid=\\"i_GwbZLur2Y\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Term&oacute;stato on-off sin y con hist&eacute;resis\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Term&oacute;stato on-off sin y con hist&eacute;resis</b>\\n            <span>sergiotecnoedu</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">El mismo experimento de la escena, montado con componentes de verdad. <b>Nadie del proyecto lo ha visto entero:</b> est&aacute;n\\n          comprobados el t&iacute;tulo y el canal, no el contenido. El v&iacute;deo no se carga hasta\\n          que lo pulsas, y se reproduce sin cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;, <a href=\\"https://www.youtube.com/watch?v=i_GwbZLur2Y\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. Es obra de su autor y no forma parte del material publicado\\n          bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema4/index.html",
  "img": "ytb:3JA5UTvTfYE",
  "ancla": "data-vid=\\"3JA5UTvTfYE\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c4-s4\\" data-vid=\\"3JA5UTvTfYE\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Transmisi&oacute;n por engranajes: caracter&iacute;sticas y c&aacute;lculo\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Transmisi&oacute;n por engranajes: caracter&iacute;sticas y c&aacute;lculo</b>\\n            <span>Daniel Reynaga</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Repaso de la relaci&oacute;n de transmisi&oacute;n de 2.&ordm;, con el paso al par que se hace en esta sesi&oacute;n. <b>Nadie del proyecto lo ha visto entero:</b> est&aacute;n\\n          comprobados el t&iacute;tulo y el canal, no el contenido. El v&iacute;deo no se carga hasta\\n          que lo pulsas, y se reproduce sin cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;, <a href=\\"https://www.youtube.com/watch?v=3JA5UTvTfYE\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. Es obra de su autor y no forma parte del material publicado\\n          bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema4/index.html",
  "img": "ytb:wkPI1BDp63E",
  "ancla": "data-vid=\\"wkPI1BDp63E\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c4-s5\\" data-vid=\\"wkPI1BDp63E\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: 1. Acci&oacute;n de CONTROL PROPORCIONAL &middot; Explicaci&oacute;n sencilla\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>1. Acci&oacute;n de CONTROL PROPORCIONAL &middot; Explicaci&oacute;n sencilla</b>\\n            <span>Sergio A. Casta&ntilde;o Giraldo</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">La acci&oacute;n proporcional sola, que es justo la de esta sesi&oacute;n, antes de meter la integral y la derivativa. <b>Nadie del proyecto lo ha visto entero:</b> est&aacute;n\\n          comprobados el t&iacute;tulo y el canal, no el contenido. El v&iacute;deo no se carga hasta\\n          que lo pulsas, y se reproduce sin cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;, <a href=\\"https://www.youtube.com/watch?v=wkPI1BDp63E\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. Es obra de su autor y no forma parte del material publicado\\n          bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema4/index.html",
  "img": "ytb:hq999kZk3Hg",
  "ancla": "data-vid=\\"hq999kZk3Hg\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c4-s6\\" data-vid=\\"hq999kZk3Hg\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Arduino: c&oacute;mo reemplazar delay() por millis()\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Arduino: c&oacute;mo reemplazar delay() por millis()</b>\\n            <span>Guillermo Gerard: Vide&iacute;tos para mi futuro yo</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">El patr&oacute;n de <code>millis()</code> explicado despacio. La parte del desbordamiento va m&aacute;s all&aacute; de 4.&ordm;, pero merece o&iacute;rla. <b>Nadie del proyecto lo ha visto entero:</b> est&aacute;n\\n          comprobados el t&iacute;tulo y el canal, no el contenido. El v&iacute;deo no se carga hasta\\n          que lo pulsas, y se reproduce sin cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;, <a href=\\"https://www.youtube.com/watch?v=hq999kZk3Hg\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. Es obra de su autor y no forma parte del material publicado\\n          bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema4/index.html",
  "img": "ytb:gfY_il4CW_M",
  "ancla": "data-vid=\\"gfY_il4CW_M\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c4-s7\\" data-vid=\\"gfY_il4CW_M\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: C&oacute;mo utilizar un sensor de humedad de suelo con Arduino &middot; Sistema de riego\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>C&oacute;mo utilizar un sensor de humedad de suelo con Arduino &middot; Sistema de riego</b>\\n            <span>Automatizaci&oacute;n para Todos</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">La sonda de humedad en la mano, con el mismo montaje que vais a hacer vosotros. <b>Nadie del proyecto lo ha visto entero:</b> est&aacute;n\\n          comprobados el t&iacute;tulo y el canal, no el contenido. El v&iacute;deo no se carga hasta\\n          que lo pulsas, y se reproduce sin cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;, <a href=\\"https://www.youtube.com/watch?v=gfY_il4CW_M\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. Es obra de su autor y no forma parte del material publicado\\n          bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema4/index.html",
  "img": "ytb:MdCUvPTvpCo",
  "ancla": "data-vid=\\"MdCUvPTvpCo\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c4-s8\\" data-vid=\\"MdCUvPTvpCo\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Huerto inteligente con Arduino: DHT11, humedad de suelo, bomba de agua, sensor de nivel y LCD\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Huerto inteligente con Arduino: DHT11, humedad de suelo, bomba de agua, sensor de nivel y LCD</b>\\n            <span>Agricultura Electronica</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Un sistema entero montado, con el sensor de nivel del dep&oacute;sito que aqu&iacute; sale en la lista de fallos. <b>Nadie del proyecto lo ha visto entero:</b> est&aacute;n\\n          comprobados el t&iacute;tulo y el canal, no el contenido. El v&iacute;deo no se carga hasta\\n          que lo pulsas, y se reproduce sin cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;, <a href=\\"https://www.youtube.com/watch?v=MdCUvPTvpCo\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. Es obra de su autor y no forma parte del material publicado\\n          bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema5/index.html",
  "img": "ytb:lD1O4KYJF9A",
  "ancla": "data-vid=\\"lD1O4KYJF9A\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c5-divisor\\" data-vid=\\"lD1O4KYJF9A\\">\\n        <button type=\\"button\\" class=\\"video-play\\"\\n                aria-label=\\"Reproducir el v&iacute;deo: 75.- Curso de electr&oacute;nica &middot; Divisor de voltaje con LDR (fotorresistencia)\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>75.- Curso de electr&oacute;nica &middot; Divisor de voltaje con LDR (fotorresistencia)</b>\\n            <span>Shakmuria</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">El mismo divisor, montado y medido con el pol&iacute;metro delante. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce\\n          sin cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=lD1O4KYJF9A\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          en otra pesta&ntilde;a</a>.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema5/index.html",
  "img": "ytb:TE_pQ8pyL80",
  "ancla": "data-vid=\\"TE_pQ8pyL80\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c5-transistor\\" data-vid=\\"TE_pQ8pyL80\\">\\n        <button type=\\"button\\" class=\\"video-play\\"\\n                aria-label=\\"Reproducir el v&iacute;deo: C&oacute;mo activar un rel&eacute; con transistor para Arduino o Raspberry (clase 48)\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>C&oacute;mo activar un rel&eacute; con transistor para Arduino o Raspberry (clase 48)</b>\\n            <span>ACADENAS</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">El mismo montaje llevado a un rel&eacute;, que es la carga con bobina m&aacute;s descarada de todas. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce\\n          sin cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=TE_pQ8pyL80\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          en otra pesta&ntilde;a</a>.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema5/index.html",
  "img": "ytb:0qBAGGq711o",
  "ancla": "data-vid=\\"0qBAGGq711o\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c5-cilindro\\" data-vid=\\"0qBAGGq711o\\">\\n        <button type=\\"button\\" class=\\"video-play\\"\\n                aria-label=\\"Reproducir el v&iacute;deo: Funcionamiento de un cilindro de simple y doble efecto\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Funcionamiento de un cilindro de simple y doble efecto</b>\\n            <span>Jos&eacute; Acu&ntilde;a</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">El corte del cilindro en movimiento, con el muelle y las dos tomas. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce\\n          sin cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=0qBAGGq711o\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          en otra pesta&ntilde;a</a>.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema5/index.html",
  "img": "ytb:3WvLarEkYK0",
  "ancla": "data-vid=\\"3WvLarEkYK0\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c5-mando\\" data-vid=\\"3WvLarEkYK0\\">\\n        <button type=\\"button\\" class=\\"video-play\\"\\n                aria-label=\\"Reproducir el v&iacute;deo: Mando directo e indirecto de un cilindro de doble efecto (FluidSIM)\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Mando directo e indirecto de un cilindro de doble efecto (FluidSIM)</b>\\n            <span>ALV Electronics</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Los dos circuitos montados en FluidSIM, que es el simulador con el que se dibuja esto profesionalmente. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce\\n          sin cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=3WvLarEkYK0\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          en otra pesta&ntilde;a</a>.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema5/index.html",
  "img": "ytb:OvlutalHXoM",
  "ancla": "data-vid=\\"OvlutalHXoM\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c5b-s5\\" data-vid=\\"OvlutalHXoM\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Como funciona una protoboard &middot; Electronica basica\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Como funciona una protoboard &middot; Electronica basica</b>\\n            <span>Ivan Espinoza</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Las grapas de cinco y los railes, vistos por dentro. <b>Nadie del proyecto lo ha visto entero:</b> est&aacute;n\\n          comprobados el t&iacute;tulo y el canal, no el contenido. El v&iacute;deo no se carga\\n          hasta que lo pulsas, y se reproduce sin cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;, <a href=\\"https://www.youtube.com/watch?v=OvlutalHXoM\\" target=\\"_blank\\"\\n          rel=\\"noopener\\">&aacute;brelo en otra pesta&ntilde;a</a>. Es obra de su autor y no forma\\n          parte del material publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema5/index.html",
  "img": "ytb:pvetokUpfzQ",
  "ancla": "data-vid=\\"pvetokUpfzQ\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c5b-s6\\" data-vid=\\"pvetokUpfzQ\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Arduino desde cero en Espa&ntilde;ol &middot; Cap&iacute;tulo 85 &middot; Pull-up y Pull-down &iquest;cu&aacute;ndo y por qu&eacute; usar?\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Arduino desde cero en Espa&ntilde;ol &middot; Cap&iacute;tulo 85 &middot; Pull-up y Pull-down &iquest;cu&aacute;ndo y por qu&eacute; usar?</b>\\n            <span>Bitwise Ar</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">El mismo problema del pin al aire, con el pulsador en vez de con la base del transistor. <b>Nadie del proyecto lo ha visto entero:</b> est&aacute;n\\n          comprobados el t&iacute;tulo y el canal, no el contenido. El v&iacute;deo no se carga\\n          hasta que lo pulsas, y se reproduce sin cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;, <a href=\\"https://www.youtube.com/watch?v=pvetokUpfzQ\\" target=\\"_blank\\"\\n          rel=\\"noopener\\">&aacute;brelo en otra pesta&ntilde;a</a>. Es obra de su autor y no forma\\n          parte del material publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema5/index.html",
  "img": "ytb:H3_xq9FLT1s",
  "ancla": "data-vid=\\"H3_xq9FLT1s\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c5b-s7\\" data-vid=\\"H3_xq9FLT1s\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Secuencia 2: A+ B+ A&minus; B&minus; [M&eacute;todo Paso a Paso]\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Secuencia 2: A+ B+ A&minus; B&minus; [M&eacute;todo Paso a Paso]</b>\\n            <span>Jose Luis Sarmiento</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">La misma secuencia de esta sesi&oacute;n, resuelta con el m&eacute;todo paso a paso. <b>Nadie del proyecto lo ha visto entero:</b> est&aacute;n\\n          comprobados el t&iacute;tulo y el canal, no el contenido. El v&iacute;deo no se carga\\n          hasta que lo pulsas, y se reproduce sin cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;, <a href=\\"https://www.youtube.com/watch?v=H3_xq9FLT1s\\" target=\\"_blank\\"\\n          rel=\\"noopener\\">&aacute;brelo en otra pesta&ntilde;a</a>. Es obra de su autor y no forma\\n          parte del material publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema5/index.html",
  "img": "ytb:9SKD_p9sFcI",
  "ancla": "data-vid=\\"9SKD_p9sFcI\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c5b-s8\\" data-vid=\\"9SKD_p9sFcI\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Arduino desde cero en Espa&ntilde;ol &middot; Cap&iacute;tulo 50 &middot; Alimentaci&oacute;n para proyectos: bater&iacute;as, fuentes, ATX PC\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Arduino desde cero en Espa&ntilde;ol &middot; Cap&iacute;tulo 50 &middot; Alimentaci&oacute;n para proyectos: bater&iacute;as, fuentes, ATX PC</b>\\n            <span>Bitwise Ar</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">De d&oacute;nde sacar la corriente que pide el automatismo entero. <b>Nadie del proyecto lo ha visto entero:</b> est&aacute;n\\n          comprobados el t&iacute;tulo y el canal, no el contenido. El v&iacute;deo no se carga\\n          hasta que lo pulsas, y se reproduce sin cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;, <a href=\\"https://www.youtube.com/watch?v=9SKD_p9sFcI\\" target=\\"_blank\\"\\n          rel=\\"noopener\\">&aacute;brelo en otra pesta&ntilde;a</a>. Es obra de su autor y no forma\\n          parte del material publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema6/index.html",
  "img": "ytb:7uV4Jh30Oho",
  "ancla": "data-vid=\\"7uV4Jh30Oho\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c6-setup\\" data-vid=\\"7uV4Jh30Oho\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Las funciones setup y loop &middot; Curso de Arduino: De Cero a Maker\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Las funciones setup y loop &middot; Curso de Arduino: De Cero a Maker</b>\\n            <span>Canal: H&eacute;ctor P&eacute;rez</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Doce minutos con el entorno de Arduino delante, por si quieres ver escribir el sketch de cero antes de la pr&aacute;ctica. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=7uV4Jh30Oho\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema6/index.html",
  "img": "ytb:ddOaXUWQxbI",
  "ancla": "data-vid=\\"ddOaXUWQxbI\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c6-analog\\" data-vid=\\"ddOaXUWQxbI\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Potenci&oacute;metro con Arduino y Tinkercad &middot; leer entradas analógicas\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Potenci&oacute;metro con Arduino y Tinkercad &middot; leer entradas analógicas</b>\\n            <span>Canal: Novatech</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">El montaje exacto de la pr&aacute;ctica, hecho en Tinkercad, por si quer&eacute;is verlo antes de montarlo. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=ddOaXUWQxbI\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema6/index.html",
  "img": "ytb:RpjSwriOi9U",
  "ancla": "data-vid=\\"RpjSwriOi9U\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c6-mqtt\\" data-vid=\\"RpjSwriOi9U\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Qu&eacute; es MQTT\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Qu&eacute; es MQTT</b>\\n            <span>Canal: Easy Learning</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Una introducci&oacute;n al protocolo, con el br&oacute;ker y los temas. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=RpjSwriOi9U\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema6/index.html",
  "img": "ytb:fP_f-aNZFLo",
  "ancla": "data-vid=\\"fP_f-aNZFLo\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c6-sesgos\\" data-vid=\\"fP_f-aNZFLo\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Sesgos algor&iacute;tmicos en la inteligencia artificial\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Sesgos algor&iacute;tmicos en la inteligencia artificial</b>\\n            <span>Canal: Fundaci&oacute;n VTR</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Casos reales de modelos que aprendieron lo que hab&iacute;a en sus ejemplos, con las consecuencias que tuvo. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=fP_f-aNZFLo\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema6/index.html",
  "img": "ytb:Pl79Ni3NUsY",
  "ancla": "data-vid=\\"Pl79Ni3NUsY\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c6-media\\" data-vid=\\"Pl79Ni3NUsY\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Filtro Digital Pasa Bajos con Arduino Media Movil\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Filtro Digital Pasa Bajos con Arduino Media Movil</b>\\n            <span>Canal: Electgpl</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">La media m&oacute;vil escrita en Arduino, con el osciloscopio delante para ver la se&ntilde;al antes y despu&eacute;s. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=Pl79Ni3NUsY\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema6/index.html",
  "img": "ytb:asVv6VZId_o",
  "ancla": "data-vid=\\"asVv6VZId_o\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c6-esp\\" data-vid=\\"asVv6VZId_o\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: ESP8266: Subir datos a un servidor mediante WiFi\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>ESP8266: Subir datos a un servidor mediante WiFi</b>\\n            <span>Canal: Prometec</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">El m&oacute;dulo de la foto, mandando datos de verdad a un servidor. Sirve para ver el montaje y los comandos antes de intentarlo. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=asVv6VZId_o\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema6/index.html",
  "img": "ytb:MR0YTI5OB9I",
  "ancla": "data-vid=\\"MR0YTI5OB9I\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c6-overfit\\" data-vid=\\"MR0YTI5OB9I\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: &iquest;Qu&eacute; es el Overfitting? Explicaci&oacute;n del sobreajuste sencilla en espa&ntilde;ol\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>&iquest;Qu&eacute; es el Overfitting? Explicaci&oacute;n del sobreajuste sencilla en espa&ntilde;ol</b>\\n            <span>Canal: Tech Portal Formaci&oacute;n</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">El mismo problema visto desde el lado del modelo: aprenderse los ejemplos en vez de aprender el problema. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=MR0YTI5OB9I\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema6/index.html",
  "img": "ytb:z3geTtX4Fvo",
  "ancla": "data-vid=\\"z3geTtX4Fvo\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c6-estados\\" data-vid=\\"z3geTtX4Fvo\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Programar Arduino como si fuera una m&aacute;quina de estados finitos\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Programar Arduino como si fuera una m&aacute;quina de estados finitos</b>\\n            <span>Canal: Construyendo a Chispas</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">La m&aacute;quina de estados escrita de cero en Arduino, con el <code>switch</code> delante. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=z3geTtX4Fvo\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema7/index.html",
  "img": "ytb:cwf-cURBUkI",
  "ancla": "data-vid=\\"cwf-cURBUkI\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c7-aspirador\\" data-vid=\\"cwf-cURBUkI\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: C&oacute;mo Funciona y se Ensambla un Robot Aspirador\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>C&oacute;mo Funciona y se Ensambla un Robot Aspirador</b>\\n            <span>Canal: Ciencia y Tecnolog&iacute;a al Desnudo</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">El aparato por dentro: d&oacute;nde est&aacute;n los sensores de choque, los de desnivel y los motores. Vedlo con las tres preguntas del recuadro delante. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=cwf-cURBUkI\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema7/index.html",
  "img": "ytb:e4VCK1N8JvM",
  "ancla": "data-vid=\\"e4VCK1N8JvM\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c7-pap\\" data-vid=\\"e4VCK1N8JvM\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: &iquest;Qu&eacute; es un motor paso a paso? &middot; Introducci&oacute;n\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>&iquest;Qu&eacute; es un motor paso a paso? &middot; Introducci&oacute;n</b>\\n            <span>Canal: Cimech 3D</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">C&oacute;mo se mueve por dentro y c&oacute;mo se elige uno. Es la pieza de la foto de arriba, en marcha. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=e4VCK1N8JvM\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema7/index.html",
  "img": "ytb:9zSRNXRuX0g",
  "ancla": "data-vid=\\"9zSRNXRuX0g\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c7-brazo\\" data-vid=\\"9zSRNXRuX0g\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Cinem&aacute;tica directa e inversa de un robot de 2 grados de libertad &middot; m&eacute;todo geom&eacute;trico\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Cinem&aacute;tica directa e inversa de un robot de 2 grados de libertad &middot; m&eacute;todo geom&eacute;trico</b>\\n            <span>Canal: Sistemas Din&aacute;micos y Control</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">El mismo brazo de la escena, con las dos cuentas hechas a mano en la pizarra. La parte de la inversa es de nivel Bachillerato: sirve para ver de d&oacute;nde salen los dos codos. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=9zSRNXRuX0g\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema7/index.html",
  "img": "ytb:IrBwtuUwqbM",
  "ancla": "data-vid=\\"IrBwtuUwqbM\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c7-estados\\" data-vid=\\"IrBwtuUwqbM\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Controlando tiempos con Arduino\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Controlando tiempos con Arduino</b>\\n            <span>Canal: Jorge Garc&iacute;a Ochoa de Aspuru</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Un automatismo real con <code>millis()</code> y transiciones por tiempo, sin un solo <code>delay()</code>. Es el paso siguiente al c&oacute;digo de la escena. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=IrBwtuUwqbM\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema7/index.html",
  "img": "ytb:pbJGJvgaS2c",
  "ancla": "data-vid=\\"pbJGJvgaS2c\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c7-s5\\" data-vid=\\"pbJGJvgaS2c\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: [TUTORIAL] 02 - M&eacute;todos de alimentaci&oacute;n para Arduino\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>[TUTORIAL] 02 - M&eacute;todos de alimentaci&oacute;n para Arduino</b>\\n            <span>Rob&oacute;tica para todos</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Las maneras de dar de comer a la placa y lo que aguanta cada una. Es la columna izquierda de la escena de arriba, con las piezas en la mano. <b>Nadie del proyecto lo ha visto entero:</b> est&aacute;n\\n          comprobados el t&iacute;tulo y el canal, no el contenido. El v&iacute;deo no se carga hasta\\n          que lo pulsas, y se reproduce sin cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;, <a href=\\"https://www.youtube.com/watch?v=pbJGJvgaS2c\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. Es obra de su autor y no forma parte del material publicado\\n          bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema7/index.html",
  "img": "ytb:6HPv_NHF9nk",
  "ancla": "data-vid=\\"6HPv_NHF9nk\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c7-s6\\" data-vid=\\"6HPv_NHF9nk\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: HOMING Y PUNTO CERO. CNC (Control Num&eacute;rico Computarizado)\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>HOMING Y PUNTO CERO. CNC (Control Num&eacute;rico Computarizado)</b>\\n            <span>Walter Jos&eacute; Horianski</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">El referenciado en una m&aacute;quina de control num&eacute;rico, que es lo mismo que va a hacer vuestro robot pero con tres ejes y un cabezal que corta. <b>Nadie del proyecto lo ha visto entero:</b> est&aacute;n\\n          comprobados el t&iacute;tulo y el canal, no el contenido. El v&iacute;deo no se carga hasta\\n          que lo pulsas, y se reproduce sin cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;, <a href=\\"https://www.youtube.com/watch?v=6HPv_NHF9nk\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. Es obra de su autor y no forma parte del material publicado\\n          bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema7/index.html",
  "img": "ytb:AtNxx-jaIt4",
  "ancla": "data-vid=\\"AtNxx-jaIt4\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c7-s7\\" data-vid=\\"AtNxx-jaIt4\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Seguridad en Celdas Rob&oacute;ticas\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Seguridad en Celdas Rob&oacute;ticas</b>\\n            <span>CIDESI-SECIHTI</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">C&oacute;mo se protege una celda con robots de verdad. Va sobre una norma industrial (ISO 10218) que se sale de 4.&ordm;; lo que interesa aqu&iacute; es el <b>orden</b> de las medidas, que es el mismo que el del recuadro. <b>Nadie del proyecto lo ha visto entero:</b> est&aacute;n\\n          comprobados el t&iacute;tulo y el canal, no el contenido. El v&iacute;deo no se carga hasta\\n          que lo pulsas, y se reproduce sin cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;, <a href=\\"https://www.youtube.com/watch?v=AtNxx-jaIt4\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. Es obra de su autor y no forma parte del material publicado\\n          bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema7/index.html",
  "img": "ytb:GmU7SimFkpU",
  "ancla": "data-vid=\\"GmU7SimFkpU\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c7-s8\\" data-vid=\\"GmU7SimFkpU\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Shakey: Experiments in Robot Planning and Learning (1972)\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Shakey: Experiments in Robot Planning and Learning (1972)</b>\\n            <span>Stanford University Libraries</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">La pel&iacute;cula original del SRI, la del robot de la foto. <b>Est&aacute; en ingl&eacute;s y no lleva subt&iacute;tulos</b>, pero se entiende mirando: se ve al robot percibir, decidir y actuar &mdash;y equivocarse&mdash; en 1972. <b>Nadie del proyecto lo ha visto entero:</b> est&aacute;n\\n          comprobados el t&iacute;tulo y el canal, no el contenido. El v&iacute;deo no se carga hasta\\n          que lo pulsas, y se reproduce sin cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;, <a href=\\"https://www.youtube.com/watch?v=GmU7SimFkpU\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. Es obra de su autor y no forma parte del material publicado\\n          bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema8/index.html",
  "img": "ytb:3mJog1DXZ3s",
  "ancla": "data-vid=\\"3mJog1DXZ3s\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c8-huella\\" data-vid=\\"3mJog1DXZ3s\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: La huella de carbono &middot; &iquest;C&oacute;mo podemos reducirla?\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>La huella de carbono &middot; &iquest;C&oacute;mo podemos reducirla?</b>\\n            <span>Canal: Naeco</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Un repaso corto al concepto y a c&oacute;mo se calcula, por si quieres o&iacute;rlo contado de otra manera antes de la pr&aacute;ctica. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=3mJog1DXZ3s\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema8/index.html",
  "img": "ytb:M_Abq9pave8",
  "ancla": "data-vid=\\"M_Abq9pave8\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c8-accesibilidad\\" data-vid=\\"M_Abq9pave8\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Conoce m&aacute;s sobre la accesibilidad universal en menos de 2 minutos\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Conoce m&aacute;s sobre la accesibilidad universal en menos de 2 minutos</b>\\n            <span>Canal: Incluyeme.com</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Dos minutos para fijar la diferencia entre adaptar y dise&ntilde;ar desde el principio. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=M_Abq9pave8\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema8/index.html",
  "img": "ytb:nO2RWjrKfMc",
  "ancla": "data-vid=\\"nO2RWjrKfMc\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c8-obsolescencia\\" data-vid=\\"nO2RWjrKfMc\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Obsolescencia programada y medio ambiente &middot; Directiva (UE) 2024/825\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Obsolescencia programada y medio ambiente &middot; Directiva (UE) 2024/825</b>\\n            <span>Canal: Universitat Polit&egrave;cnica de Val&egrave;ncia</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">De una serie universitaria sobre el marco legal. Es m&aacute;s seco que los otros, pero es de los pocos sitios donde esto se cuenta con la norma delante. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=nO2RWjrKfMc\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema8/index.html",
  "img": "ytb:kd3nZ7HmoxY",
  "ancla": "data-vid=\\"kd3nZ7HmoxY\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c8-consumo\\" data-vid=\\"kd3nZ7HmoxY\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Midiendo el consumo de un Arduino UNO\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Midiendo el consumo de un Arduino UNO</b>\\n            <span>Canal: Prometec</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">La medida hecha delante de la c&aacute;mara, con el mult&iacute;metro en serie. Mirad las cifras que le salen y comparadlas con las de la escena. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=kd3nZ7HmoxY\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema8/index.html",
  "img": "ytb:oD9QDlNhNeA",
  "ancla": "data-vid=\\"oD9QDlNhNeA\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c8-raee\\" data-vid=\\"oD9QDlNhNeA\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: C&oacute;mo se gestionan los residuos electr&oacute;nicos (RAEE)\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>C&oacute;mo se gestionan los residuos electr&oacute;nicos (RAEE)</b>\\n            <span>Canal: Asegre</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Para ver qu&eacute; pasa despu&eacute;s del contenedor. &#9888; <b>Ojo con qui&eacute;n lo firma</b>: Asegre es la asociaci&oacute;n de las empresas que gestionan esos residuos, o sea que tiene inter&eacute;s en que el proceso salga bien en el v&iacute;deo. Para <b>ver la m&aacute;quina</b> vale; para las <b>cifras</b>, usad la escena y decid de d&oacute;nde sale cada una. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=oD9QDlNhNeA\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema8/index.html",
  "img": "ytb:Cg_9mGWrsKA",
  "ancla": "data-vid=\\"Cg_9mGWrsKA\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c8-retorno\\" data-vid=\\"Cg_9mGWrsKA\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: C&aacute;lculo sencillo de retorno de inversi&oacute;n con placas solares\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>C&aacute;lculo sencillo de retorno de inversi&oacute;n con placas solares</b>\\n            <span>Canal: Carlos Codina &middot; Tu Asesor Energ&eacute;tico</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">La misma cuenta de hoy, hecha en <b>euros</b> en vez de en kilos de CO&#8322;: inversi&oacute;n dividida entre ahorro al a&ntilde;o. F&iacute;jate en dos cosas. Una: es la <b>misma divisi&oacute;n</b> y da <b>otro n&uacute;mero</b>, porque la unidad es otra. Dos: quien lo cuenta <b>vende asesor&iacute;a energ&eacute;tica</b>, as&iacute; que interesa mirar qu&eacute; mete y qu&eacute; deja fuera de su cuenta. Es el l&iacute;mite de la sesi&oacute;n 1, aplicado a un v&iacute;deo de YouTube. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=Cg_9mGWrsKA\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema8/index.html",
  "img": "ytb:4VReody58_0",
  "ancla": "data-vid=\\"4VReody58_0\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c8-ecodiseno\\" data-vid=\\"4VReody58_0\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: &iquest;Qu&eacute; es el ecodise&ntilde;o y el dise&ntilde;o sostenible? No es lo mismo\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>&iquest;Qu&eacute; es el ecodise&ntilde;o y el dise&ntilde;o sostenible? No es lo mismo</b>\\n            <span>Canal: Dise&ntilde;o industrial y estrat&eacute;gico con Irene Ramos</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Una dise&ntilde;adora industrial contando por qu&eacute; el ecodise&ntilde;o no es poner materiales reciclados ni pintarlo de verde, sino decidir en el momento en que a&uacute;n se puede decidir. Es la misma idea de la rampa de la sesi&oacute;n 2, contada desde el otro lado. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=4VReody58_0\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema8/index.html",
  "img": "ytb:v1w23sxy5Ro",
  "ancla": "data-vid=\\"v1w23sxy5Ro\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c8-greenwashing\\" data-vid=\\"v1w23sxy5Ro\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Greenwashing e informaci&oacute;n ambiental en productos\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Greenwashing e informaci&oacute;n ambiental en productos</b>\\n            <span>Canal: GIZ M&eacute;xico</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Qu&eacute; es una afirmaci&oacute;n ambiental que no se puede comprobar, contado con ejemplos de producto. Es el reto de hoy visto desde el otro lado: no c&oacute;mo se defiende un n&uacute;mero, sino c&oacute;mo se detecta a quien no puede defender el suyo. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=v1w23sxy5Ro\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema9/index.html",
  "img": "ytb:EydFlOUooN4",
  "ancla": "data-vid=\\"EydFlOUooN4\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c9-olvidadas\\" data-vid=\\"EydFlOUooN4\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: No te olvides de las enfermedades olvidadas (corto documental)\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>No te olvides de las enfermedades olvidadas (corto documental)</b>\\n            <span>Canal: Barcelona Institute for Global Health (ISGlobal)</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Un corto de un centro de investigaci&oacute;n sobre las enfermedades que casi no salen en la cuenta de arriba. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=EydFlOUooN4\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema9/index.html",
  "img": "ytb:wDyCMVmY-Vk",
  "ancla": "data-vid=\\"wDyCMVmY-Vk\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c9-nevera\\" data-vid=\\"wDyCMVmY-Vk\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: C&oacute;mo esta nevera que no necesita electricidad salv&oacute; a una empresa de cer&aacute;mica india\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>C&oacute;mo esta nevera que no necesita electricidad salv&oacute; a una empresa de cer&aacute;mica india</b>\\n            <span>Canal: Insider Espa&ntilde;ol</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">La misma idea de la olla de barro, llevada a un producto que se vende. Sirve para discutir si sigue siendo tecnolog&iacute;a apropiada cuando se convierte en un negocio. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=wDyCMVmY-Vk\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema9/index.html",
  "img": "ytb:sC1HmzxOjoQ",
  "ancla": "data-vid=\\"sC1HmzxOjoQ\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c9-acv\\" data-vid=\\"sC1HmzxOjoQ\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: An&aacute;lisis de ciclo de vida: definici&oacute;n de objetivos y alcance\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>An&aacute;lisis de ciclo de vida: definici&oacute;n de objetivos y alcance</b>\\n            <span>Canal: Universitat Polit&egrave;cnica de Val&egrave;ncia</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Un v&iacute;deo universitario, m&aacute;s seco que los otros, sobre c&oacute;mo se hace de verdad la cuenta que aqu&iacute; hemos dejado a medias. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=sC1HmzxOjoQ\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "4eso/Tecnologia/tema9/index.html",
  "img": "ytb:8Ec4Pgs8ClA",
  "ancla": "data-vid=\\"8Ec4Pgs8ClA\\"",
  "figura": "<div class=\\"video\\" id=\\"video-c9-cc\\" data-vid=\\"8Ec4Pgs8ClA\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Qu&eacute; son y c&oacute;mo funcionan las licencias Creative Commons\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Qu&eacute; son y c&oacute;mo funcionan las licencias Creative Commons</b>\\n            <span>Canal: &Aacute;rtica - Centro Cultural Online</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Las mismas letras que acabamos de ver, contadas por gente que se dedica a esto. Sirve para repasar antes de elegir la vuestra. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=8Ec4Pgs8ClA\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "2eso/TyD/tema6/index.html",
  "img": "ytb:Yv0cECrFydk",
  "ancla": "data-vid=\\"Yv0cECrFydk\\"",
  "figura": "<div class=\\"video\\" id=\\"video-u4s2\\" data-vid=\\"Yv0cECrFydk\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo sobre tipos de estructuras\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Tipos de estructuras</b>\\n            <span>Elena Zubi &middot; Tecnolog&iacute;a 2.&ordm; ESO</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">V&eacute;alo despu&eacute;s de la escena, no antes: la gracia est&aacute; en que reconozcas\\n          las familias que ya has visto. Ve anotando <b>un ejemplo nuevo</b> de cada una que no\\n          hayamos nombrado aqu&iacute;.</p>\\n        <p class=\\"video-nota\\">El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin cookies de\\n          seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=Yv0cECrFydk\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material publicado\\n          bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "2eso/TyD/tema7/index.html",
  "img": "ytb:8fDOm-XJBOQ",
  "ancla": "data-vid=\\"8fDOm-XJBOQ\\"",
  "figura": "<div class=\\"video\\" id=\\"video-palanca\\" data-vid=\\"8fDOm-XJBOQ\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Ley de la palanca (mecanismos)\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Ley de la palanca (mecanismos)</b>\\n            <span>TECH LAPSE &middot; 2 minutos</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Animaci&oacute;n de los tres g&eacute;neros con la ley aplicada paso a paso. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce\\n          sin cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=8fDOm-XJBOQ\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "2eso/TyD/tema7/index.html",
  "img": "ytb:AlAxnplUNH0",
  "ancla": "data-vid=\\"AlAxnplUNH0\\"",
  "figura": "<div class=\\"video\\" id=\\"video-poleas\\" data-vid=\\"AlAxnplUNH0\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Polea fija, polea m&oacute;vil y polipasto\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Polea fija, polea m&oacute;vil y polipasto</b>\\n            <span>tecnoblas2 &middot; 7 minutos y medio</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Ense&ntilde;a los tres montajes seguidos, con la cuerda que hay que tirar en cada uno. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce\\n          sin cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=AlAxnplUNH0\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "2eso/TyD/tema7/index.html",
  "img": "ytb:0pO6cHi3HzE",
  "ancla": "data-vid=\\"0pO6cHi3HzE\\"",
  "figura": "<div class=\\"video\\" id=\\"video-engranajes\\" data-vid=\\"0pO6cHi3HzE\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Engranajes (Transmisi&oacute;n circular)\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Engranajes (Transmisi&oacute;n circular)</b>\\n            <span>TECH LAPSE &middot; 2 minutos y medio</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Animaci&oacute;n de trenes de engranajes con la relaci&oacute;n de transmisi&oacute;n calculada. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce\\n          sin cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=0pO6cHi3HzE\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "2eso/TyD/tema7/index.html",
  "img": "ytb:Dyee1JVYsd0",
  "ancla": "data-vid=\\"Dyee1JVYsd0\\"",
  "figura": "<div class=\\"video\\" id=\\"video-biela\\" data-vid=\\"Dyee1JVYsd0\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: La biela - manivela (mecanismo de transformaci&oacute;n)\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>La biela - manivela (mecanismo de transformaci&oacute;n)</b>\\n            <span>TECH LAPSE &middot; poco m&aacute;s de 2 minutos</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Del mismo profesor que los v&iacute;deos de la palanca y de los engranajes, as&iacute; que usa el mismo vocabulario que hemos usado en clase. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce\\n          sin cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=Dyee1JVYsd0\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "2eso/TyD/tema8/index.html",
  "img": "ytb:PFP9LsBdnLA",
  "ancla": "data-vid=\\"PFP9LsBdnLA\\"",
  "figura": "<div class=\\"video\\" id=\\"video-PFP9LsBdnLA\\" data-vid=\\"PFP9LsBdnLA\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: El circuito el&eacute;ctrico y sus componentes\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>El circuito el&eacute;ctrico y sus componentes</b>\\n            <span>Clases Particulares en &Aacute;vila</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Rep&aacute;salo en v&iacute;deo y <b>anota una cosa</b>: cada vez que aparezca un componente, p&aacute;ralo y dibuja su s&iacute;mbolo de memoria antes de mirarlo. Si no te sale, es que a&uacute;n no lo tienes.</p>\\n        <p class=\\"video-nota\\">El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin cookies de\\n          seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=PFP9LsBdnLA\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. Es obra de su autor y no forma parte del material publicado bajo la\\n          licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "2eso/TyD/tema8/index.html",
  "img": "ytb:tpt9FlNYq4k",
  "ancla": "data-vid=\\"tpt9FlNYq4k\\"",
  "figura": "<div class=\\"video\\" id=\\"video-tpt9FlNYq4k\\" data-vid=\\"tpt9FlNYq4k\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Circuitos el&eacute;ctricos: ley de Ohm y potencia\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Circuitos el&eacute;ctricos: ley de Ohm y potencia</b>\\n            <span>El Traductor de Ingenier&iacute;a</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Va un poco m&aacute;s all&aacute; de esta sesi&oacute;n: habla tambi&eacute;n de <b>potencia</b>, que es la sesi&oacute;n 4. De momento qu&eacute;date con la parte de la ley de Ohm y toma nota de la otra: la vas a necesitar.</p>\\n        <p class=\\"video-nota\\">El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin cookies de\\n          seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=tpt9FlNYq4k\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. Es obra de su autor y no forma parte del material publicado bajo la\\n          licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "2eso/TyD/tema8/index.html",
  "img": "ytb:OVDqVpnRltw",
  "ancla": "data-vid=\\"OVDqVpnRltw\\"",
  "figura": "<div class=\\"video\\" id=\\"video-OVDqVpnRltw\\" data-vid=\\"OVDqVpnRltw\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Circuito el&eacute;ctrico con serie y paralelo &middot; Tecnolog&iacute;a 2.&ordm; ESO\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Circuito el&eacute;ctrico con serie y paralelo &middot; Tecnolog&iacute;a 2.&ordm; ESO</b>\\n            <span>Academia Usero Estepona</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Un ejercicio resuelto paso a paso, del mismo nivel que el vuestro. Hacedlo vosotros primero en la libreta, con el v&iacute;deo pausado, y comparad despu&eacute;s.</p>\\n        <p class=\\"video-nota\\">El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin cookies de\\n          seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=OVDqVpnRltw\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. Es obra de su autor y no forma parte del material publicado bajo la\\n          licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "2eso/TyD/tema8/index.html",
  "img": "ytb:9qWYeA5y_r0",
  "ancla": "data-vid=\\"9qWYeA5y_r0\\"",
  "figura": "<div class=\\"video\\" id=\\"video-9qWYeA5y_r0\\" data-vid=\\"9qWYeA5y_r0\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Potencia y energ&iacute;a el&eacute;ctrica: &iquest;cu&aacute;nto costar&aacute;?\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Potencia y energ&iacute;a el&eacute;ctrica: &iquest;cu&aacute;nto costar&aacute;?</b>\\n            <span>Ruben Sebastian</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Otra explicaci&oacute;n de lo mismo, con ejercicios resueltos. Antes de darle al play, calcula t&uacute; lo que cuesta tener encendida la luz de tu habitaci&oacute;n tres horas al d&iacute;a durante un mes: as&iacute; el v&iacute;deo te corrige en vez de cont&aacute;rtelo.</p>\\n        <p class=\\"video-nota\\">El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin cookies de\\n          seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=9qWYeA5y_r0\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. Es obra de su autor y no forma parte del material publicado bajo la\\n          licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "2eso/TyD/tema8/index.html",
  "img": "ytb:Bw4nVt8eQkw",
  "ancla": "data-vid=\\"Bw4nVt8eQkw\\"",
  "figura": "<div class=\\"video\\" id=\\"video-Bw4nVt8eQkw\\" data-vid=\\"Bw4nVt8eQkw\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: C&oacute;mo calcular la resistencia para un LED (ley de Ohm f&aacute;cil)\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>C&oacute;mo calcular la resistencia para un LED (ley de Ohm f&aacute;cil)</b>\\n            <span>ITC MENTOR Academy</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">La misma cuenta que acabas de hacer, contada por otra persona. Ve con la libreta delante y comprueba que usa <b>exactamente</b> la misma f&oacute;rmula: tensi&oacute;n de la fuente menos tensi&oacute;n del LED, dividido entre la corriente que t&uacute; decides.</p>\\n        <p class=\\"video-nota\\">El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin cookies de\\n          seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=Bw4nVt8eQkw\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. Es obra de su autor y no forma parte del material publicado bajo la\\n          licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "2eso/TyD/tema9/index.html",
  "img": "ytb:-ZTekGoR8uQ",
  "ancla": "data-vid=\\"-ZTekGoR8uQ\\"",
  "figura": "<div class=\\"video\\" id=\\"video-cpu\\" data-vid=\\"-ZTekGoR8uQ\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: &iquest;C&oacute;mo funciona un procesador? Desde un transistor hasta una CPU\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>&iquest;C&oacute;mo funciona un procesador? Desde un transistor hasta una CPU</b>\\n            <span>Hardware 360&ordm; &middot; en espa&ntilde;ol</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Para ver qu&eacute; hay debajo del ciclo de tres pasos: c&oacute;mo un mont&oacute;n de interruptores microsc&oacute;picos acaban siendo un procesador. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=-ZTekGoR8uQ\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "2eso/TyD/tema9/index.html",
  "img": "ytb:o3gGXwY-1uI",
  "ancla": "data-vid=\\"o3gGXwY-1uI\\"",
  "figura": "<div class=\\"video\\" id=\\"video-mem\\" data-vid=\\"o3gGXwY-1uI\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Diferencias entre SSD, disco duro y memoria RAM\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Diferencias entre SSD, disco duro y memoria RAM</b>\\n            <span>Inform&aacute;ticaI3J &middot; en espa&ntilde;ol &middot; unos 6 minutos</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Repasa los tres componentes con piezas reales en la mano. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=o3gGXwY-1uI\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "2eso/TyD/tema9/index.html",
  "img": "ytb:iRpB3TVCCtE",
  "ancla": "data-vid=\\"iRpB3TVCCtE\\"",
  "figura": "<div class=\\"video\\" id=\\"video-bin\\" data-vid=\\"iRpB3TVCCtE\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: &iquest;Por qu&eacute; los ordenadores usan el sistema binario?\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>&iquest;Por qu&eacute; los ordenadores usan el sistema binario?</b>\\n            <span>EDteam &middot; en espa&ntilde;ol</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Cuenta la misma historia del reto de hoy: por qu&eacute; dos estados y no diez. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=iRpB3TVCCtE\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "2eso/TyD/tema9/index.html",
  "img": "ytb:9GxcNyGQsuk",
  "ancla": "data-vid=\\"9GxcNyGQsuk\\"",
  "figura": "<div class=\\"video\\" id=\\"video-adc\\" data-vid=\\"9GxcNyGQsuk\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Muestreo / Cuantificaci&oacute;n / Codificaci&oacute;n\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Muestreo / Cuantificaci&oacute;n / Codificaci&oacute;n</b>\\n            <span>Universitat Polit&egrave;cnica de Val&egrave;ncia &middot; en espa&ntilde;ol</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Los mismos tres pasos de hoy, contados con la se&ntilde;al delante. Es de un canal universitario y el nivel est&aacute; por encima del de clase: m&iacute;ralo para fijar el vocabulario, no para aprender de cero. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=9GxcNyGQsuk\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "2eso/TyD/tema9/index.html",
  "img": "ytb:vnJCudAed08",
  "ancla": "data-vid=\\"vnJCudAed08\\"",
  "figura": "<div class=\\"video\\" id=\\"video-so\\" data-vid=\\"vnJCudAed08\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Microaprendizaje: &iquest;Qu&eacute; es un sistema operativo?\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Microaprendizaje: &iquest;Qu&eacute; es un sistema operativo?</b>\\n            <span>Educar Portal &middot; en espa&ntilde;ol</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Un repaso corto de las funciones que acabas de copiar, por si alguna se ha quedado a medias. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=vnJCudAed08\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "2eso/TyD/tema9/index.html",
  "img": "ytb:pMG7x0XnCU8",
  "ancla": "data-vid=\\"pMG7x0XnCU8\\"",
  "figura": "<div class=\\"video\\" id=\\"video-diag\\" data-vid=\\"pMG7x0XnCU8\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: C&oacute;mo diagnosticar problemas en mi PC\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>C&oacute;mo diagnosticar problemas en mi PC</b>\\n            <span>Edutin Academy &middot; curso de mantenimiento &middot; en espa&ntilde;ol</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">El mismo m&eacute;todo aplicado a un equipo real, con las herramientas delante. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=pMG7x0XnCU8\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "2eso/TyD/tema10/index.html",
  "img": "ytb:u1xxZ8r2rRc",
  "ancla": "data-vid=\\"u1xxZ8r2rRc\\"",
  "figura": "<div class=\\"video\\" id=\\"video-cables\\" data-vid=\\"u1xxZ8r2rRc\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: C&oacute;mo funciona internet: los cables submarinos que conectan al mundo\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>C&oacute;mo funciona internet: los cables submarinos que conectan al mundo</b>\\n            <span>Un Mundo Inmenso &middot; en espa&ntilde;ol</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Para ver por d&oacute;nde va f&iacute;sicamente eso que llamamos &laquo;la nube&raquo;: barcos, cables y mapas. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=u1xxZ8r2rRc\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "2eso/TyD/tema10/index.html",
  "img": "ytb:U0iiT41OI3I",
  "ancla": "data-vid=\\"U0iiT41OI3I\\"",
  "figura": "<div class=\\"video\\" id=\\"video-https\\" data-vid=\\"U0iiT41OI3I\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Qu&eacute; significa que una web empiece por HTTPS\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Qu&eacute; significa que una web empiece por HTTPS</b>\\n            <span>Oficina de Seguridad del Internauta (INCIBE) &middot; en espa&ntilde;ol</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">La versi&oacute;n oficial y corta de lo mismo, del organismo p&uacute;blico espa&ntilde;ol de ciberseguridad. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=U0iiT41OI3I\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "2eso/TyD/tema10/index.html",
  "img": "ytb:L1EqDetsFKU",
  "ancla": "data-vid=\\"L1EqDetsFKU\\"",
  "figura": "<div class=\\"video\\" id=\\"video-cookies\\" data-vid=\\"L1EqDetsFKU\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Qu&eacute; son las cookies y c&oacute;mo funcionan, en 1 minuto\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Qu&eacute; son las cookies y c&oacute;mo funcionan, en 1 minuto</b>\\n            <span>Fundaci&oacute;n Cibervoluntarios &middot; en espa&ntilde;ol</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Un minuto, para fijar la diferencia entre la cookie que hace falta y la que te sigue. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=L1EqDetsFKU\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "2eso/TyD/tema10/index.html",
  "img": "ytb:Q-jjSRovIIA",
  "ancla": "data-vid=\\"Q-jjSRovIIA\\"",
  "figura": "<div class=\\"video\\" id=\\"video-2fa\\" data-vid=\\"Q-jjSRovIIA\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Activaci&oacute;n del Doble Factor de Autenticaci&oacute;n\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Activaci&oacute;n del Doble Factor de Autenticaci&oacute;n</b>\\n            <span>UOC &middot; Universitat Oberta de Catalunya &middot; en espa&ntilde;ol</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Para ver el paso a paso de activarlo, que es m&aacute;s f&aacute;cil de lo que parece. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=Q-jjSRovIIA\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "2eso/TyD/tema10/index.html",
  "img": "ytb:PM_M4Iz6I4o",
  "ancla": "data-vid=\\"PM_M4Iz6I4o\\"",
  "figura": "<div class=\\"video\\" id=\\"video-321\\" data-vid=\\"PM_M4Iz6I4o\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Backup 3-2-1, el m&eacute;todo definitivo para mantener a salvo tus datos\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Backup 3-2-1, el m&eacute;todo definitivo para mantener a salvo tus datos</b>\\n            <span>Xataka &middot; en espa&ntilde;ol</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">La misma regla contada con ejemplos de aparatos de hoy. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=PM_M4Iz6I4o\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "2eso/TyD/tema10/index.html",
  "img": "ytb:p3nATAVU6kM",
  "ancla": "data-vid=\\"p3nATAVU6kM\\"",
  "figura": "<div class=\\"video\\" id=\\"video-derechos\\" data-vid=\\"p3nATAVU6kM\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Cu&aacute;les son tus derechos de protecci&oacute;n de datos personales\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Cu&aacute;les son tus derechos de protecci&oacute;n de datos personales</b>\\n            <span>Agencia Espa&ntilde;ola de Protecci&oacute;n de Datos &middot; en espa&ntilde;ol</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Los mismos derechos contados por el organismo que se encarga de hacerlos cumplir. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=p3nATAVU6kM\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "2eso/TyD/tema11/index.html",
  "img": "ytb:pSBpSSbx9Ps",
  "ancla": "data-vid=\\"pSBpSSbx9Ps\\"",
  "figura": "<div class=\\"video\\" id=\\"video-pdf\\" data-vid=\\"pSBpSSbx9Ps\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: &iquest;Qu&eacute; es un PDF?\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>&iquest;Qu&eacute; es un PDF?</b>\\n            <span>Micro Conocimiento &middot; en espa&ntilde;ol</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Un minuto y medio para fijar por qu&eacute; se manda en PDF lo que tiene que verse igual en todas partes. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=pSBpSSbx9Ps\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "2eso/TyD/tema11/index.html",
  "img": "ytb:RZywV73MDGM",
  "ancla": "data-vid=\\"RZywV73MDGM\\"",
  "figura": "<div class=\\"video\\" id=\\"video-vector\\" data-vid=\\"RZywV73MDGM\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: &iquest;Qu&eacute; diferencia hay entre una imagen vectorial y un mapa de bits?\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>&iquest;Qu&eacute; diferencia hay entre una imagen vectorial y un mapa de bits?</b>\\n            <span>Micro Conocimiento &middot; en espa&ntilde;ol</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Un minuto, del mismo canal que el v&iacute;deo del PDF, para fijar la distinci&oacute;n. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=RZywV73MDGM\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "2eso/TyD/tema11/index.html",
  "img": "ytb:zRoxXHR_-Ac",
  "ancla": "data-vid=\\"zRoxXHR_-Ac\\"",
  "figura": "<div class=\\"video\\" id=\\"video-presentar\\" data-vid=\\"zRoxXHR_-Ac\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Muerte por PowerPoint: trucos para no aburrir a la audiencia\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Muerte por PowerPoint: trucos para no aburrir a la audiencia</b>\\n            <span>La Hoguera Bloguera &middot; en espa&ntilde;ol</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Los errores de siempre, vistos desde fuera. Lo que dice se solapa con la r&uacute;brica de arriba: comprobadlo mientras lo veis. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=zRoxXHR_-Ac\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "2eso/TyD/tema11/index.html",
  "img": "ytb:ksmzVNMJhZ4",
  "ancla": "data-vid=\\"ksmzVNMJhZ4\\"",
  "figura": "<div class=\\"video\\" id=\\"video-licencias\\" data-vid=\\"ksmzVNMJhZ4\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: &iquest;Qu&eacute; es Creative Commons? (y sus tipos de licencia)\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>&iquest;Qu&eacute; es Creative Commons? (y sus tipos de licencia)</b>\\n            <span>OpenWebinars &middot; en espa&ntilde;ol</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Las mismas cuatro condiciones contadas de otra manera. Mientras lo ves, ve diciendo en voz alta qu&eacute; obliga cada letra: si te sale sola, lo tienes. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=ksmzVNMJhZ4\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "2eso/TyD/tema11/index.html",
  "img": "ytb:8ZKlKAAh6HI",
  "ancla": "data-vid=\\"8ZKlKAAh6HI\\"",
  "figura": "<div class=\\"video\\" id=\\"video-lector\\" data-vid=\\"8ZKlKAAh6HI\\">\\n        <button type=\\"button\\" class=\\"video-play\\" aria-label=\\"Reproducir el v&iacute;deo: Lector de pantalla: manejar una web\\">\\n          <span class=\\"video-tri\\" aria-hidden=\\"true\\"></span>\\n          <span class=\\"video-txt\\">\\n            <b>Lector de pantalla: manejar una web</b>\\n            <span>Universidad de Alicante &middot; en espa&ntilde;ol</span>\\n          </span>\\n        </button>\\n        <p class=\\"video-nota\\">Una web recorrida de verdad con un lector de pantalla. Mientras lo veis, contad cu&aacute;ntas veces salta de encabezado en encabezado: es exactamente lo de la escena de arriba, pero con una p&aacute;gina real. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin\\n          cookies de seguimiento. Si no se ve aqu&iacute; &mdash;porque la red del centro bloquee YouTube o porque ese\\n          v&iacute;deo no se deje empotrar&mdash;,\\n          <a href=\\"https://www.youtube.com/watch?v=8ZKlKAAh6HI\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>",
  "modo": "reemplaza"
 },
 {
  "pagina": "2eso/TyD/tema7/index.html",
  "img": "u5-vibrador-olivos.jpg",
  "ancla": "</p>\\n        <p>Merece la pena pensarlo: durante catorce a&ntilde;os, la mejor m&aacute;quina de vapor del\\n           mundo llev&oacute; un mecanismo peor <b>por un motivo legal, no t&eacute;cnico</b>. La\\n           tecnolog&iacute;a no la deciden solo los ingenieros.</p>\\n      </div>",
  "figura": "<div class=\\"escena\\">\\n        <div class=\\"escena-barra\\"><span class=\\"escena-titulo\\">Transformar el movimiento, en el campo &middot; 18 segundos</span></div>\\n        <div class=\\"lienzo\\" style=\\"padding:0;background:#000;display:flex;justify-content:center\\">\\n          <video controls preload=\\"none\\" muted playsinline style=\\"width:auto;max-width:100%;max-height:60vh;display:block\\"\\n                 poster=\\"../../../video/u5-vibrador-olivos.jpg\\">\\n            <source src=\\"../../../video/u5-vibrador-olivos.mp4\\" type=\\"video/mp4\\">\\n            Tu navegador no puede reproducir v&iacute;deo.\\n            <a href=\\"../../../video/u5-vibrador-olivos.mp4\\">Desc&aacute;rgalo aqu&iacute;</a>.\\n          </video>\\n        </div>\\n        <div class=\\"pie\\">Una cosechadora de aceituna. El tractor solo sabe hacer una cosa: <b>girar</b>. Y lo que hace falta para que caiga la aceituna no es girar, es <b>sacudir</b>. Dentro de esa pinza hay unas masas descentradas dando vueltas: al girar tiran hacia un lado, media vuelta despu&eacute;s tiran hacia el otro, y el &aacute;rbol entero vibra. Giro convertido en vaiv&eacute;n, como la biela, pero a cuarenta sacudidas por segundo.<br><br>V&iacute;deo de <b>Jared Gulian</b>, v&iacute;a Wikimedia Commons, <b>CC BY 3.0</b>. Recortado y recomprimido.</div>\\n      </div>",
  "modo": "antes"
 },
 {
  "pagina": "2eso/TyD/tema9/index.html",
  "img": "computer-architecture.svg",
  "ancla": "</p>\\n      </div>\\n\\n      <h3>Qui&eacute;n obedece la lista: la CPU</h3>\\n      <p>La pieza que lee la lista y la obedece es el <b>procesador</b>. No es un cerebro y no decide\\n         nada: hace tres cosas, en este orden, y vuelve a empezar. Sin parar, mientras tenga corriente.</p>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/computer-architecture.svg\\" width=\\"1000\\" height=\\"600\\" loading=\\"lazy\\"\\n             alt=\\"Arquitectura del ordenador: CPU, RAM, Almacenamiento, Entrada/Salida, interconectados por bus de datos\\">\\n        <figcaption>La <b>arquitectura de Von Neumann</b>: todo ordenador tiene estos cinco componentes: la CPU que procesa, la RAM que guarda lo que se est&aacute; usando, el almacenamiento que persiste, y los perif&eacute;ricos de <b>entrada</b> y de <b>salida</b>, que meten y sacan la informaci&oacute;n. Todo conectado por <b>buses de datos</b> que transportan n&uacute;meros. El bus es como una carretera en la que circulan &oacute;rdenes y datos a un ritmo que se mide en gigahercios.\\n          <span class=\\"credito\\">Elaboraci&oacute;n propia &middot; CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "2eso/TyD/tema9/index.html",
  "img": "os-process-management.svg",
  "ancla": "</div>\\n    <section class=\\"bloque\\">\\n      <div class=\\"rotulo\\"><span class=\\"num\\">00</span> Reto inicial &middot; 10 min</div>\\n\\n      <p>Dos cosas que ya te han pasado, y que todo el mundo cuenta como si fueran mala suerte:</p>\\n      <ol>\\n        <li>Abres muchas pesta&ntilde;as y el ordenador empieza a <b>arrastrarse</b>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/os-process-management.svg\\" width=\\"1000\\" height=\\"500\\" loading=\\"lazy\\"\\n             alt=\\"Sistema Operativo: Time sharing de CPU, aislamiento de memoria entre procesos, y gesti&oacute;n de archivos\\">\\n        <figcaption>La RAM no es de un solo programa: en el centro del dibujo, varios programas <b>se reparten</b> la mesa, y por eso con quince pesta&ntilde;as se llena. Quien reparte ese sitio, y tambi&eacute;n los turnos de CPU y los archivos, es el <b>sistema operativo (SO)</b>, que ver&aacute;s en la sesi&oacute;n 5. Mientras ves varios programas funcionando a la vez, el SO alterna entre ellos por turnos de unos pocos milisegundos (time sharing). Cada programa est&aacute; en su propia zona de memoria, protegido del resto. El SO tambi&eacute;n organiza tus archivos en carpetas y controla qui&eacute;n puede leer o escribir en cada uno. Todo eso que funciona &laquo;m&aacute;gicamente&raquo; lo hace el SO sin que t&uacute; le digas nada.\\n          <span class=\\"credito\\">Elaboraci&oacute;n propia &middot; CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
  "modo": "despues"
 },
 {
  "pagina": "2eso/TyD/tema9/index.html",
  "img": "binary-representation.svg",
  "ancla": "</div>\\n    <section class=\\"bloque\\">\\n      <div class=\\"rotulo\\"><span class=\\"num\\">00</span> Reto inicial &middot; 10 min</div>\\n\\n      <p>De la unidad de electricidad te llevaste un hecho que ahora vale oro: por un cable\\n         <b>pasa corriente o no pasa</b>. Eso es todo lo que un cable sabe distinguir con seguridad.</p>\\n\\n      <div class=\\"aviso\\">",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/binary-representation.svg\\" width=\\"1000\\" height=\\"550\\" loading=\\"lazy\\"\\n             alt=\\"Representaci&oacute;n binaria: bits, bytes, y potencias de 2 para guardar informaci&oacute;n\\">\\n        <figcaption>Los <b>bits y bytes</b>: la unidad b&aacute;sica de informaci&oacute;n es un <b>bit</b> (0 &oacute; 1). Ocho bits hacen un <b>byte</b> (256 valores posibles). Con <b>N bits</b> se pueden representar <b>2^N valores</b>: 8 bits para un car&aacute;cter, 1 KB para un p&aacute;rrafo, 1 MB para una foto peque&ntilde;a, 1 GB para un cuarto de hora de v&iacute;deo. Todo el ordenador habla en potencias de dos porque los circuitos internos solo saben decir s&iacute; o no.\\n          <span class=\\"credito\\">Elaboraci&oacute;n propia &middot; CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
  "modo": "despues"
 },
 {
  "pagina": "2eso/TyD/tema10/index.html",
  "img": "network-layers-osi.svg",
  "ancla": "</h3>\\n      <p>Prueba la red de abajo. Pide el v&iacute;deo y, <b>mientras los paquetes van de camino</b>, corta un\\n         cable pulsando encima. Fíjate en dos cosas: en qu&eacute; pasa con el paquete que iba justo por\\n         ah&iacute;, y en el orden en el que llegan los seis.</p>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/network-layers-osi.svg\\" width=\\"1000\\" height=\\"600\\" loading=\\"lazy\\"\\n             alt=\\"Modelo OSI de 7 capas: F&iacute;sica, Enlace, Red, Transporte, Sesi&oacute;n, Presentaci&oacute;n, Aplicaci&oacute;n, con protocolos y ejemplos pr&aacute;cticos en cada capa\\">\\n        <figcaption>Internet va por <b>capas</b>, una encima de otra, y cada una solo habla con la suya del otro lado. Este dibujo es el modelo que las ordena (se llama <b>OSI</b> y cuenta siete), y no hace falta aprend&eacute;rselo. Lo que ves en esta sesi&oacute;n est&aacute; en las de abajo: los <b>cables</b> y el WiFi, y encima la de <b>red</b>, la de la <b>direcci&oacute;n IP</b> y los <b>routers</b>, que decide por d&oacute;nde va cada paquete. El navegador, arriba del todo, no necesita saber c&oacute;mo est&aacute;n conectadas las m&aacute;quinas.\\n          <span class=\\"credito\\">Elaboraci&oacute;n propia &middot; CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "2eso/TyD/tema10/index.html",
  "img": "http-vs-https-security.svg",
  "ancla": "</h3>\\n      <p>Aqu&iacute; entra el <b>candado</b>. En la escena de abajo escribe un usuario y una contrase&ntilde;a\\n         &mdash;inventados, no los tuyos&mdash; y ve pulsando cada salto del camino con\\n         <b>http</b> y con <b>https</b>. Mira sobre todo los dos extremos.</p>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/http-vs-https-security.svg\\" width=\\"1000\\" height=\\"700\\" loading=\\"lazy\\"\\n             alt=\\"HTTP vs HTTPS: comparaci&oacute;n de seguridad entre datos sin cifrar y datos cifrados\\">\\n        <figcaption><b>HTTP vs HTTPS: qu&eacute; protege el candado</b>. En HTTP los datos viajan en texto limpio: cualquiera en el camino (red Wi-Fi pública, router del ISP&hellip;) puede verlo. <b>Tus contraseñas están expuestas.</b> En HTTPS los datos viajan cifrados: aunque alguien los intercepte, solo ve un galimatías. El candado del navegador significa que está activado. Pero cuidado: HTTPS protege que nadie <b>vea</b> lo que envías, no que <b>sea real</b> el sitio (ojo con phishing).\\n          <span class=\\"credito\\">Elaboraci&oacute;n propia &middot; CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
  "modo": "antes"
 },
 {
  "pagina": "2eso/TyD/tema11/index.html",
  "img": "file-formats.svg",
  "ancla": "</div>\\n    <section class=\\"bloque\\">\\n      <div class=\\"rotulo\\"><span class=\\"num\\">00</span> Reto inicial &middot; 10 min</div>\\n\\n      <p>De la unidad de internet sales sabiendo c&oacute;mo llega a tu pantalla lo que pides y\\n         qui&eacute;n lo ve pasar por el camino. Todo eso lo mirabas t&uacute;. A partir de hoy le\\n         damos la vuelta a la pregunta: <b>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/file-formats.svg\\" width=\\"1000\\" height=\\"600\\" loading=\\"lazy\\"\\n             alt=\\"Formatos de archivo: TXT, DOCX, PDF, JPG/PNG, MP4, HTML, MP3 - contenido, ventajas y desventajas\\">\\n        <figcaption>Los <b>formatos de archivo</b> m&aacute;s comunes: un <b>.TXT</b> es s&oacute;lo texto (ligero, universal). Un <b>.DOCX</b> guarda formato, estilos y metadatos (flexible, pesado). Un <b>.PDF</b> congela la posici&oacute;n (se ve igual siempre, pero es dif&iacute;cil de editar). Las <b>im&aacute;genes</b> son grillas de p&iacute;xeles. Los <b>videos</b> son fotogramas + audio. La diferencia entre guardar &laquo;qu&eacute; dice&raquo; (texto, c&oacute;digo) y guardar &laquo;c&oacute;mo se ve&raquo; (imagen, PDF) es fundamental: lo primero ocupa poco, lo segundo mucho.\\n          <span class=\\"credito\\">Elaboraci&oacute;n propia &middot; CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
  "modo": "despues"
 },
 {
  "pagina": "2eso/TyD/tema11/index.html",
  "img": "image-pixels-color.svg",
  "ancla": "</div>\\n    <section class=\\"bloque\\">\\n      <div class=\\"rotulo\\"><span class=\\"num\\">00</span> Reto inicial &middot; 10 min</div>\\n\\n      <p>El grupo termina la presentaci&oacute;n: catorce diapositivas y once fotos. Al ir a\\n         subirla, el aviso de siempre: <b>48 MB</b>, demasiado. Y lo raro es que ah&iacute; dentro\\n         no hay 48 MB de ideas.</p>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/image-pixels-color.svg\\" width=\\"1000\\" height=\\"650\\" loading=\\"lazy\\"\\n             alt=\\"Una imagen es una grilla de p&iacute;xeles con color RGB: resoluci&oacute;n, tama&ntilde;o de archivo, y modelo de color\\">\\n        <figcaption>Una <b>imagen digital es una grilla de p&iacute;xeles</b>, cada uno con un n&uacute;mero que es su color (RGB: rojo, verde, azul, 0-255 cada uno). La <b>resoluci&oacute;n</b> dice cu&aacute;ntos p&iacute;xeles: 1920&times;1080 Full HD son 2 millones de p&iacute;xeles. Cada p&iacute;xel necesita 3 bytes (uno por cada color), as&iacute; que una foto sin comprimir pesa unos 6 MB. Con compresi&oacute;n JPG baja a 500 KB. Por eso tu m&oacute;vil toma fotos de 4.032&times;3.024: parecen 35 MB pero se transforman en 3 MB.\\n          <span class=\\"credito\\">Elaboraci&oacute;n propia &middot; CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
  "modo": "despues"
 },
 {
  "pagina": "2eso/TyD/tema11/index.html",
  "img": "image-resolution-filesize.svg",
  "ancla": "<a href=\\"https://www.youtube.com/watch?v=RZywV73MDGM\\" target=\\"_blank\\" rel=\\"noopener\\">&aacute;brelo\\n          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material\\n          publicado bajo la licencia de esta p&aacute;gina.</p>\\n      </div>\\n\\n    </section>",
  "figura": "<figure class=\\"foto\\">\\n      <img src=\\"../../../img/image-resolution-filesize.svg\\" width=\\"1000\\" height=\\"700\\" loading=\\"lazy\\" alt=\\"Comparaci&oacute;n de resoluci&oacute;n de imagen: baja, media y alta, con p&iacute;xeles y tama&ntilde;o de archivo\\">\\n      <figcaption><b>Resoluci&oacute;n y tama&ntilde;o de archivo.</b> Tres destinos distintos piden resoluciones distintas: un icono se queda en 100 &times; 100 p&iacute;xeles, una foto para la web o las redes en 800 &times; 600 y una para imprimir en 4000 &times; 3000. En bruto, el peso crece al mismo ritmo que los p&iacute;xeles, porque cada uno son 3 bytes: el doble de p&iacute;xeles, el doble de peso. Lo que enga&ntilde;a es el tama&ntilde;o: con el doble de ancho y el doble de alto hay <b>cuatro veces</b> m&aacute;s p&iacute;xeles, y pesa cuatro veces m&aacute;s. Los pesos de las tarjetas son aproximados; abajo est&aacute; la cuenta en bruto de la foto grande.\\n        <span class=\\"credito\\">Elaboraci&oacute;n propia &middot; CC BY-SA 4.0</span>\\n      </figcaption>\\n    </figure>",
  "modo": "antes"
 },
 {
  "pagina": "2eso/TyD/tema11/index.html",
  "img": "digital-collaboration.svg",
  "ancla": "<span class=\\"min\\"><b>20'</b> Teor&iacute;a</span><span class=\\"min\\"><b>25'</b> Pr&aacute;ctica</span><span class=\\"min\\"><b>5'</b> Cierre</span></div>\\n      <div class=\\"chips\\"><span class=\\"chip\\">CE2 &middot; 2.1</span><span class=\\"chip\\">CE4 &middot; 4.1</span><span class=\\"chip sab\\">B.1 &middot; B.3</span></div>",
  "figura": "<figure class=\\"foto\\">\\n        <img src=\\"../../../img/digital-collaboration.svg\\" width=\\"1000\\" height=\\"550\\" loading=\\"lazy\\"\\n             alt=\\"Colaboraci&oacute;n digital: emails vs nube compartida, comentarios, y historial de versiones\\">\\n        <figcaption>La <b>colaboraci&oacute;n digital moderna</b>: el m&eacute;todo antiguo de emails genera conflictos (Ana edita v1, Bob edita v1, &iquest;cu&aacute;l es correcta?). Con <b>nube compartida</b> (Google Docs, OneDrive) hay UNA versi&oacute;n que se sincroniza al instante. Los <b>comentarios</b> permiten feedback sin cambiar el texto. El <b>historial</b> guarda todas las versiones anteriores. Un &uacute;nico documento, un &uacute;nico due&ntilde;o, todo el mundo viendo lo mismo.\\n          <span class=\\"credito\\">Elaboraci&oacute;n propia &middot; CC BY-SA 4.0</span>\\n        </figcaption>\\n      </figure>",
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
        # la clave puede ser un fichero o 'yt:<id>' para un bloque de YouTube
        marca = f['img'][3:] if f['img'].startswith('yt:') else f['img']
        if marca in s and f.get('modo') != 'reemplaza':
            saltadas += 1
            continue
        # modo 'reemplaza': el build SI produce el bloque, pero con otro texto
        # (las notas de los videos de YouTube son mas cortas en el generador).
        if f.get('modo') == 'reemplaza':
            ini = s.find(f['ancla'])
            if ini < 0:
                perdidas += 1
                print(u'   no encuentro el bloque de %s en %s' % (f['img'], f['pagina']))
                continue
            ini = s.rfind(u'<div class="video"', 0, ini + 1)
            prof = 0
            fin = -1
            import re as _re
            for m in _re.finditer(r'<div\b|</div>', s[ini:]):
                prof += 1 if m.group(0) == '<div' else -1
                if prof == 0:
                    fin = ini + m.end()
                    break
            if fin < 0:
                perdidas += 1
                continue
            if s[ini:fin] == f['figura']:
                saltadas += 1
                continue
            s = s[:ini] + f['figura'] + s[fin:]
            io.open(ruta, 'w', encoding='utf-8', newline='').write(s)
            puestas += 1
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
