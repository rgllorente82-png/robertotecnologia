# -*- coding: utf-8 -*-
"""2.o TyD - U4 - Sesion 6: ensayo, analisis y test.

Se rompe el puente, se compara con lo que cada grupo habia predicho y se cierra
el tema. El ensayo no es un espectaculo: es la unica forma de saber si el
diseno era bueno, y por eso la prediccion se entrego por escrito antes.

El test se corrige en la propia pagina (generadores/test_auto.py) y explica
SIEMPRE por que, tambien en las que se aciertan.
"""
from unidad_base import bloque, ficha, pregunta
from test_auto import test

# --------------------------------------------------------------------------
# 00 - El ensayo
# --------------------------------------------------------------------------
ENSAYO = u'''
      <p>Hoy se rompen los puentes. Y se rompen en serio: hasta el final, no hasta que da miedo.</p>
      <div class="aviso">
        <span class="n-tag">Protocolo, igual para todos</span>
        El puente se apoya en dos mesas separadas <b>40 cm</b>. Del centro del cord&oacute;n inferior
        cuelga una bolsa. Se van a&ntilde;adiendo pesas <b>de 100 en 100 gramos</b>, esperando cinco
        segundos entre una y otra. Se anota el peso de la <b>&uacute;ltima que aguant&oacute;</b>.
      </div>
      <ol class="pasos">
        <li>Antes de cargar: <b>pesad el puente</b> y anotadlo. Sin ese dato no hay nota.</li>
        <li>Leed en voz alta vuestra <b>predicci&oacute;n</b>: cu&aacute;ntos gramos y por d&oacute;nde va a
            romper. La escribisteis la sesi&oacute;n pasada y no se puede cambiar.</li>
        <li>Cargad. Cuando rompa, <b>parad y mirad</b>: &iquest;qu&eacute; barra ha fallado primero?</li>
        <li>Anotad si esa barra <b>se ha partido</b>, <b>se ha doblado</b> o <b>se ha despegado
            del nudo</b>. No es lo mismo, y lo veremos ahora.</li>
      </ol>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>En un laboratorio de verdad esto se llama <b>ensayo destructivo</b>, y se hace igual: se
           lleva la pieza hasta la rotura porque es la &uacute;nica manera de saber d&oacute;nde estaba el
           l&iacute;mite. Lo que no se puede hacer es ensayar el puente de verdad: por eso se ensayan
           <b>maquetas</b> y probetas, y por eso vuestro trabajo de hoy se parece bastante al de un
           ingeniero.</p>
      </div>
'''

# --------------------------------------------------------------------------
# 01 - Analisis
# --------------------------------------------------------------------------
ANALISIS = u'''
      <h3>Por d&oacute;nde ha roto, y qu&eacute; significa</h3>
      <p>Casi todos los fallos que ver&eacute;is hoy son uno de estos cuatro, y cada uno se&ntilde;ala un
         error de dise&ntilde;o distinto:</p>
      <div class="copiar">
        <h4>Los cuatro fallos y qu&eacute; hay que arreglar</h4>
        <ul>
          <li><b>Una barra comprimida se ha doblado de golpe</b> &rarr; <b>pandeo</b>. La barra era
              demasiado larga y delgada. Se arregla acort&aacute;ndola (m&aacute;s nudos) o engros&aacute;ndola
              (dos palillos pegados).</li>
          <li><b>Una barra estirada se ha partido en seco</b> &rarr; se super&oacute; su
              <b>resistencia a tracci&oacute;n</b>. Es el fallo m&aacute;s honrado: el material ha dado todo
              lo que ten&iacute;a.</li>
          <li><b>Se ha despegado un nudo</b> &rarr; el fallo no era de las barras, sino de la
              <b>uni&oacute;n</b>. Muy com&uacute;n, y muy fastidiado: significa que el puente val&iacute;a m&aacute;s
              de lo que ha demostrado.</li>
          <li><b>El puente se ha tumbado de lado</b> &rarr; falt&oacute; <b>arriostramiento</b>. No es un
              problema de resistencia: es de <b>estabilidad</b>, como la sesi&oacute;n 4.</li>
        </ul>
      </div>
      <p>Ahora comparad con lo que predijisteis:</p>
      <ol class="pasos">
        <li>&iquest;Acertasteis <b>el sitio</b>? Acertar el sitio vale m&aacute;s que acertar el peso: quiere
            decir que hab&iacute;ais entendido por d&oacute;nde iban las fuerzas.</li>
        <li>Calculad vuestro <b>rendimiento</b>: gramos aguantados entre gramos de puente.</li>
        <li>Escribid <b>una sola cosa</b> que cambiar&iacute;ais, y por qu&eacute;. Una, la que m&aacute;s
            hubiera cambiado el resultado.</li>
      </ol>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Es muy probable que el puente m&aacute;s pesado de la clase <b>no</b> sea el que gane. Y que
           alguno que parec&iacute;a fr&aacute;gil quede arriba. Eso no es mala suerte ni chiripa: es
           exactamente lo que dice el tema desde la primera sesi&oacute;n. <b>Una estructura no aguanta
           porque sea fuerte: aguanta porque reparte.</b></p>
      </div>
'''

# --------------------------------------------------------------------------
# 02 - El test
# --------------------------------------------------------------------------
PREGUNTAS = [
 dict(p=u'Una estructura aguanta, sobre todo, porque&hellip;',
      op=[u'tiene mucho material y es muy pesada',
          u'reparte la fuerza entre sus piezas hasta llevarla al suelo',
          u'est&aacute; hecha de un material muy duro'],
      ok=1,
      por=u'Es la idea que organiza el tema entero. Una torre de celos&iacute;a est&aacute; casi hueca y '
          u'aguanta m&aacute;s viento que un muro macizo del mismo peso.'),
 dict(p=u'Una pieza larga y delgada que se comprime&hellip;',
      op=[u'se aplasta poco a poco',
          u'se dobla de golpe hacia un lado: pandea',
          u'se estira por el centro'],
      ok=1,
      por=u'El <b>pandeo</b> es el fallo t&iacute;pico de la compresi&oacute;n en piezas esbeltas, y ocurre '
          u'mucho antes de que el material llegue a aplastarse. Por eso los pilares altos son gruesos.'),
 dict(p=u'&iquest;Por qu&eacute; el tri&aacute;ngulo es indeformable y el cuadrado no?',
      op=[u'porque el tri&aacute;ngulo tiene menos lados y pesa menos',
          u'porque fijados los tres lados, los tres &aacute;ngulos quedan determinados',
          u'porque los tri&aacute;ngulos se hacen siempre con material m&aacute;s resistente'],
      ok=1,
      por=u'Un cuadrado articulado se desploma en rombo <b>sin que ning&uacute;n lado cambie de '
          u'longitud</b>. En el tri&aacute;ngulo eso es imposible: no hay otra forma con esos tres lados.'),
 dict(p=u'La piedra aguanta muy bien comprimida y se parte estirada. &iquest;Qu&eacute; forma le da eso?',
      op=[u'el arco, que la mantiene siempre apretada',
          u'la viga recta, que es la m&aacute;s sencilla',
          u'el cable, que es la m&aacute;s ligera'],
      ok=0,
      por=u'Es el invento romano: dar a la piedra una forma curva para que cada pieza est&eacute; '
          u'<b>aplastada contra la siguiente</b> y ninguna reciba un tir&oacute;n. A cambio, el arco '
          u'empuja hacia fuera y hay que sujetarlo con contrafuertes.'),
 dict(p=u'Un arco de piedra, adem&aacute;s de bajar la carga, hace algo molesto en sus apoyos:',
      op=[u'los levanta hacia arriba',
          u'los empuja hacia fuera',
          u'los retuerce'],
      ok=1,
      por=u'De ah&iacute; los <b>contrafuertes</b> de las catedrales y los estribos de los puentes de '
          u'piedra: si el arco se puede abrir por abajo, se cae.'),
 dict(p=u'Con la misma cantidad de acero, &iquest;qu&eacute; secci&oacute;n aguanta m&aacute;s a flexi&oacute;n?',
      op=[u'un cuadrado macizo, porque est&aacute; lleno',
          u'un perfil en I, con el material lejos del eje',
          u'da igual: lo que cuenta es cu&aacute;nto acero hay'],
      ok=1,
      por=u'El material que est&aacute; junto al eje neutro <b>no trabaja, solo pesa</b>. Con 400 mm&sup2; '
          u'de acero, el perfil en I aguanta unas <b>doce veces</b> m&aacute;s que el cuadrado macizo.'),
 dict(p=u'Dos armarios id&eacute;nticos, uno vac&iacute;o y otro lleno de libros repartidos por igual. '
        u'&iquest;Cu&aacute;l vuelca antes?',
      op=[u'el lleno, porque pesa m&aacute;s',
          u'el vac&iacute;o, porque pesa menos',
          u'los dos al mismo &aacute;ngulo'],
      ok=2,
      por=u'El peso total <b>no aparece</b> en la condici&oacute;n de vuelco. Lo que decide es la anchura '
          u'de la base y la <b>altura</b> del centro de gravedad, y en los dos est&aacute; a la misma altura.'),
 dict(p=u'Un cuerpo no vuelca mientras&hellip;',
      op=[u'la vertical de su centro de gravedad caiga dentro de su base de sustentaci&oacute;n',
          u'su centro de gravedad est&eacute; dentro del material',
          u'ninguna de sus piezas se rompa'],
      ok=0,
      por=u'Volcar y romperse son <b>dos problemas distintos</b>. Una estructura con todas sus piezas '
          u'perfectas se cae igual si la vertical del CDG se sale de la base.'),
 dict(p=u'En una celos&iacute;a, la cuenta de barras sale justa. &iquest;Seguro que es r&iacute;gida?',
      op=[u's&iacute;: si la cuenta sale, aguanta',
          u'no: pueden estar mal repartidas y quedar un cuadro sin diagonal',
          u'solo si es de acero'],
      ok=1,
      por=u'La cuenta es <b>necesaria pero no suficiente</b>. Con dos diagonales en un cuadro y '
          u'ninguna en otro sale el n&uacute;mero justo y la estructura se mueve igual.'),
 dict(p=u'En el ensayo, un puente rompe porque una barra <b>se dobla de golpe</b>. &iquest;Qu&eacute; '
        u'hab&iacute;a que haber hecho?',
      op=[u'usar m&aacute;s cinta en los nudos',
          u'acortar esa barra con un nudo intermedio, o doblarla con otro palillo',
          u'hacer todo el puente m&aacute;s pesado'],
      ok=1,
      por=u'Doblarse de golpe es <b>pandeo</b>, y el pandeo depende sobre todo de lo <b>larga y '
          u'delgada</b> que sea la pieza comprimida. M&aacute;s cinta no arregla un pandeo, y m&aacute;s peso '
          u'empeora la nota.'),
]

TEST = (u'''
      <p>Diez preguntas sobre todo el tema. Se corrigen aqu&iacute; mismo, y cada una explica por
         qu&eacute; &mdash;tambi&eacute;n las que aciertes&mdash;. No cuenta para nota: es para que sepas por
         d&oacute;nde andas antes del examen.</p>
''' + test('u4', u'Lo que tiene que haber quedado del tema', PREGUNTAS))

# --------------------------------------------------------------------------
# 03 - Cierre
# --------------------------------------------------------------------------
CIERRE = u'''
      <p>Con esto se cierra el tema. Si te quedas con tres frases, que sean estas:</p>
      <div class="copiar">
        <h4>El tema en tres frases</h4>
        <ol>
          <li>Una estructura <b>no aguanta porque sea fuerte: aguanta porque reparte</b>, y lo que
              decide es d&oacute;nde est&aacute; el material, no cu&aacute;nto hay.</li>
          <li>La <b>forma</b> se elige para que cada material trabaje en el esfuerzo que aguanta
              bien, y el <b>tri&aacute;ngulo</b> es la &uacute;nica figura que no se deforma.</li>
          <li>Hay que aprobar <b>dos ex&aacute;menes</b>: no romperse (resistencia) y no volcarse
              (estabilidad). Son problemas distintos.</li>
        </ol>
      </div>
      <h3>Y una estructura tambi&eacute;n se juzga por lo que cuesta al planeta</h3>
      <p>Una viga puede aguantar perfectamente y aun as&iacute; ser una mala elecci&oacute;n. En una
      construcci&oacute;n, buena parte del impacto no est&aacute; en el uso: est&aacute; en <b>fabricar los
      materiales</b>. Un kilo de acero arrastra mucha m&aacute;s energ&iacute;a que un kilo de madera.</p>
      <p>De ah&iacute; salen tres criterios que hoy se piden a un <b>edificio sostenible</b>:</p>
      <ul>
        <li><b>Menos material y mejor colocado</b>: es exactamente lo que hace la triangulaci&oacute;n y
            lo que hace un perfil en doble T. Ahorrar material es ahorrar energ&iacute;a.</li>
        <li><b>Materiales de cerca y de origen conocido</b>: la madera de gesti&oacute;n sostenible y el
            &aacute;rido de la propia zona evitan miles de kil&oacute;metros de cami&oacute;n.</li>
        <li><b>Que se pueda desmontar</b>: una estructura atornillada se desmonta y sus piezas se
            reutilizan; una hormigonada entera acaba en escombro.</li>
      </ul>
      <div class="caja caja-nuestro">
        <span class="n-tag">La pregunta que lo resume</span>
        <p>Cuando termines tu puente de palillos, hazte la misma pregunta que un ingeniero:
        <b>&iquest;aguanta lo mismo con menos material?</b> Esa pregunta es, a la vez, la de la nota
        y la de la sostenibilidad.</p>
      </div>

      <div class="nota">
        <span class="n-tag">Siguiente tema</span>
        Todo lo que has construido hasta ahora ten&iacute;a que <b>quedarse quieto</b>: una estructura
        que se mueve es una estructura que ha fallado. En el tema siguiente pasa justo lo
        contrario &mdash;queremos que se mueva, y que se mueva donde nosotros digamos&mdash;, y eso
        son los <b>mecanismos</b>.
      </div>
'''

S6 = (bloque('00', u'El ensayo &middot; 20 min', ENSAYO) +
      bloque('01', u'An&aacute;lisis &middot; 15 min', ANALISIS) +
      bloque('02', u'Test &middot; 20 min', TEST) +
      bloque('03', u'Cierre &middot; 5 min', CIERRE))
