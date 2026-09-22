# -*- coding: utf-8 -*-
"""Lectura de aula de la U7: 30 parrafos numerados y 10 preguntas, en PDF.

    python generadores/u7_lectura.py   ->  2eso/TyD/tema9/lectura-tema9.pdf

El hilo es una sola averia -pulsas una tecla y no sale nada- y el texto recorre
la maquina entera buscandole la causa. Asi la lectura no es un resumen del tema:
es el tema visto desde el sitio donde el alumno se lo encuentra de verdad.

Los datos que llevan cifra estan comprobados uno a uno; van anotados donde toca.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lectura

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PARRAFOS = [
  (u'h', u'La tecla que no responde'),

  u'Pulsas una tecla en clase y en la pantalla no aparece nada. Antes de decidir que el ordenador '
  u'&laquo;est&aacute; roto&raquo;, conviene saber cu&aacute;ntas piezas distintas tienen que funcionar '
  u'seguidas para que salga una sola letra. Son m&aacute;s de las que imaginas, y cualquiera de ellas '
  u'puede ser la culpable.',

  u'Debajo de cada tecla hay una l&aacute;mina que, al bajar, cierra un contacto el&eacute;ctrico. Dentro '
  u'del teclado, un chip diminuto vigila sin parar esa rejilla de contactos y detecta cu&aacute;l se ha '
  u'cerrado. F&iacute;jate en lo que env&iacute;a: <b>no env&iacute;a la letra A</b>. Env&iacute;a un '
  u'n&uacute;mero que identifica la posici&oacute;n de esa tecla, y nada m&aacute;s.',

  u'Ese n&uacute;mero viaja por el cable USB o por Bluetooth hasta la <b>placa base</b>, que es la '
  u'l&aacute;mina verde donde est&aacute; enchufado todo: la red de carreteras por la que circulan los '
  u'datos entre los componentes. Si esa ruta se corta, el teclado funciona perfectamente y el ordenador '
  u'no se entera de nada.',

  (u'h', u'Las dos mitades: hardware y software'),

  u'A partir de aqu&iacute; no se entiende nada sin una idea, y es la m&aacute;s importante de todas: en un '
  u'ordenador, <b>la m&aacute;quina y las instrucciones son dos cosas separadas</b>. El <b>hardware</b> es '
  u'todo lo que puedes tocar: la placa, los chips, la pantalla. El <b>software</b> son las instrucciones, '
  u'que no pesan, no se tocan y no se gastan.',

  u'Esa separaci&oacute;n no es un capricho de vocabulario: es la raz&oacute;n de que exista el ordenador. '
  u'En un circuito normal el comportamiento est&aacute; <i>en los cables</i>, as&iacute; que cada '
  u'comportamiento nuevo obliga a montar otro circuito. Si quieres que una bombilla parpadee, montas uno; '
  u'si adem&aacute;s quieres que cuente, montas otro. Y cambiar de idea significa volver a coger el soldador.',

  u'En 1945 ya hab&iacute;a una m&aacute;quina que calculaba de verdad, el <b>ENIAC</b>, y se programaba '
  u'exactamente as&iacute;: enchufando y desenchufando cables en sus paneles. Cambiar de problema pod&iacute;a '
  u'costar d&iacute;as de trabajo. La m&aacute;quina era prodigiosa y el m&eacute;todo, un callej&oacute;n sin '
  u'salida.',

  u'La idea que lo resolvi&oacute; ven&iacute;a de mucho antes, y no de la inform&aacute;tica sino de '
  u'<b>tejer</b>. Hacia 1805, Joseph Marie Jacquard mont&oacute; un telar que le&iacute;a <b>tarjetas '
  u'perforadas</b>: el dibujo de la tela no estaba en el telar, estaba en las tarjetas. Cambiabas las '
  u'tarjetas y el mismo telar tej&iacute;a otra cosa.',

  u'En 1945 John von Neumann escribi&oacute; lo mismo para las m&aacute;quinas de calcular: guardar el '
  u'programa <b>en la misma memoria que los datos</b>. Si el programa es un n&uacute;mero m&aacute;s, se '
  u'carga y se cambia igual de r&aacute;pido que un n&uacute;mero. La primera m&aacute;quina que lo hizo de '
  u'verdad arranc&oacute; en Manchester el <b>21 de junio de 1948</b>, y casi todo lo que hoy llamamos '
  u'ordenador sigue ese esquema.',

  (u'h', u'El procesador, que no piensa'),

  u'La pieza que lee esa lista de instrucciones y la obedece es el procesador, la <b>CPU</b>. Se le llama '
  u'&laquo;el cerebro del ordenador&raquo; y es una comparaci&oacute;n mala, porque un cerebro decide y la '
  u'CPU no decide nada: repite tres pasos, siempre en el mismo orden, mientras tenga corriente.',

  u'Los tres pasos son: <b>busca</b> en la memoria la instrucci&oacute;n que toca, la <b>descodifica</b> '
  u'para averiguar qu&eacute; pide, y la <b>ejecuta</b>. Y vuelve a empezar. Todo lo que hace un ordenador '
  u'&mdash;un videojuego, una videollamada, este texto&mdash; son millones de vueltas a esos tres pasos.',

  u'El <b>reloj</b> del procesador marca el ritmo de ese ciclo. Uno de 3 GHz recibe 3.000 millones de '
  u'pulsos por segundo. Cuidado con la frase que se oye siempre: <b>no</b> son 3.000 millones de '
  u'instrucciones. Hay instrucciones que gastan varios pulsos y procesadores que resuelven varias a la vez. '
  u'Los gigahercios miden el <i>ritmo</i>, no el trabajo.',

  u'En 1971 Intel consigui&oacute; meter una CPU entera en una sola pastilla de silicio: el <b>4004</b>, con '
  u'unos 2.300 transistores. Un procesador de m&oacute;vil de hoy lleva decenas de miles de millones, y hace '
  u'exactamente lo mismo que aquel: buscar, descodificar, ejecutar.',

  u'Que el procesador no piense no quiere decir que no se equivoque. En octubre de 1994 el '
  u'matem&aacute;tico Thomas Nicely descubri&oacute; que su Pentium daba mal una divisi&oacute;n: 4.195.835 '
  u'entre 3.145.727. El resultado correcto empieza por 1,33382 y el chip devolv&iacute;a 1,33373. El fallo '
  u'estaba grabado en el silicio, en una tabla interna de la unidad de divisi&oacute;n.',

  u'Ah&iacute; se ve la diferencia entre las dos mitades mejor que en ninguna definici&oacute;n. Un error de '
  u'software se corrige y se vuelve a cargar; uno de hardware <b>no se arregla reinstalando nada</b>. Intel '
  u'se comprometi&oacute; en diciembre de 1994 a cambiar el procesador a quien lo pidiera, y en enero de '
  u'1995 cifr&oacute; el coste de aquello en 475 millones de d&oacute;lares.',

  (u'h', u'Las dos memorias'),

  u'Volvamos a tu letra, que ya va camino del procesador. La CPU no puede trabajar con algo que est&aacute; '
  u'en el disco: necesita tenerlo a mano. Para eso existe la <b>memoria RAM</b>, que es la mesa de trabajo '
  u'donde est&aacute;n, ahora mismo, el sistema operativo, el programa de escritura y tu documento a medio '
  u'escribir.',

  u'Y aqu&iacute; aparece la molestia m&aacute;s com&uacute;n de todas: tienes quince pesta&ntilde;as '
  u'abiertas y el ordenador se arrastra. No es que el procesador sea malo &mdash;con una sola pesta&ntilde;a '
  u'va fino&mdash;. Es que la RAM se ha llenado y el sistema tiene que empezar a bajar cosas al disco y a '
  u'volver a subirlas.',

  u'La diferencia de velocidad entre las dos es dif&iacute;cil de imaginar, porque los n&uacute;meros son '
  u'diminutos. Llegar a un dato que est&aacute; en la RAM cuesta unos <b>80 nanosegundos</b>; a uno que '
  u'est&aacute; en un SSD, alrededor de <b>0,1 mil&eacute;simas</b> de segundo; a uno que est&aacute; en un '
  u'disco duro de platos, unas <b>10 mil&eacute;simas</b>.',

  u'Est&iacute;ralos hasta algo que puedas sentir. Si buscar en la RAM te costara <b>un segundo</b>, buscar '
  u'en el SSD te costar&iacute;a unos <b>21 minutos</b> y buscar en el disco duro, unas <b>35 horas</b>. '
  u'Cuando el ordenador se arrastra, lo que est&aacute; pasando es que ha empezado a hacer viajes de veinte '
  u'minutos para traer cosas que antes ten&iacute;a al lado.',

  u'El segundo problema cl&aacute;sico parece distinto y tiene la misma causa. Apagas de golpe y pierdes lo '
  u'que no hab&iacute;as guardado, pero el fichero de ayer sigue ah&iacute;. La RAM es <b>vol&aacute;til</b>: '
  u'necesita corriente para acordarse, y al cortarla se borra entera. El almacenamiento no lo es, y por eso '
  u'<i>guardar</i> un fichero es, literalmente, copiarlo de la mesa a la estanter&iacute;a. Ah&iacute; se ve '
  u'por qu&eacute; comprar un disco m&aacute;s grande no arregla ninguno de los dos problemas: lo que se llena '
  u'es la mesa, no la estanter&iacute;a.',

  u'El almacenamiento tiene dos formas. El <b>disco duro</b> guarda los datos en platos magn&eacute;ticos que '
  u'giran, con un brazo que lleva el cabezal hasta la pista que toca: hay que <b>mover algo f&iacute;sico</b>, '
  u'y mover algo tarda milisegundos. El <b>SSD</b> no tiene ninguna pieza m&oacute;vil, todo es '
  u'electr&oacute;nico, y por eso arranca el sistema en segundos.',

  u'Antes de los chips, la memoria de trabajo se hac&iacute;a con <b>anillos de ferrita</b> ensartados a mano '
  u'en hilos de cobre: cada anillo, imantado en un sentido o en el otro, guardaba <b>un bit</b>. Uno. Que hoy '
  u'quepan miles de millones de bits en una pastilla del tama&ntilde;o de una u&ntilde;a es, seguramente, el '
  u'salto m&aacute;s grande que ha dado la tecnolog&iacute;a en un siglo.',

  (u'h', u'Lo que hay escrito de verdad'),

  u'Queda la pregunta inc&oacute;moda: &iquest;qu&eacute; hay escrito en esos huecos de memoria? Ni letras, ni '
  u'n&uacute;meros, ni fotos. Solo hay circuitos, y un circuito nada m&aacute;s sabe distinguir dos cosas con '
  u'seguridad: que pase corriente o que no pase.',

  u'La idea que se le ocurre a todo el mundo es usar <i>una tensi&oacute;n para cada letra</i>. No funciona, y '
  u'la cuenta lo demuestra: repartir 5 voltios entre 27 letras deja escalones de 0,19 V. Un cable de verdad se '
  u'calienta y recoge ruido el&eacute;ctrico; con 0,3 V de ruido ya no hay forma de saber qu&eacute; letra ha '
  u'llegado.',

  u'Por eso se renunci&oacute; a la idea brillante y se eligi&oacute; la tonta y segura: <b>dos s&iacute;mbolos '
  u'y nada m&aacute;s</b>, 0 y 1, separados todo lo posible. Se pierde capacidad por cable y se gana no '
  u'equivocarse nunca, que era lo que de verdad hac&iacute;a falta.',

  u'A esa unidad m&iacute;nima se la llama <b>bit</b>. Un bit solo vale 0 o 1, as&iacute; que por s&iacute; solo '
  u'no sirve de mucho; lo que sirve es <b>juntarlos</b>, porque las combinaciones se multiplican. Con ocho bits '
  u'&mdash;un <b>byte</b>&mdash; salen 2<super>8</super> = 256 combinaciones distintas.',

  u'Lo que un byte <i>significa</i> depende de un <b>acuerdo</b> previo. El mismo 01000001 es el n&uacute;mero '
  u'65, es la letra A en la tabla ASCII y es un gris oscuro si lo lees como un nivel de luz. Por eso una foto '
  u'abierta con un editor de texto sale como basura: el programa est&aacute; aplicando el acuerdo equivocado.',

  u'Que ganara el binario no era obvio, y hubo quien lo intent&oacute; de otra forma: en 1958, en la Universidad '
  u'de Mosc&uacute;, se construy&oacute; el <b>Setun</b>, un ordenador <i>ternario</i>, de tres estados, y '
  u'funcionaba. Perdi&oacute; igual, porque fabricar un componente que distinga dos estados es much&iacute;simo '
  u'm&aacute;s barato y m&aacute;s fiable que uno que distinga tres, y esa ventaja se multiplica por los miles '
  u'de millones de componentes de un chip.',

  # Tres parrafos bajo un solo titulillo, y no dos mas uno: si el ultimo lleva
  # titulo propio se queda huerfano al pie de la pagina 3.
  (u'h', u'Entra, sale, y c&oacute;mo se busca la aver&iacute;a'),

  u'Tu letra ya est&aacute; procesada. Falta que alguien la ense&ntilde;e, y de eso se encargan los '
  u'<b>perif&eacute;ricos de salida</b>: la pantalla, los altavoces, la impresora. Los de <b>entrada</b> son los '
  u'que meten informaci&oacute;n en el sistema: el teclado, el rat&oacute;n, el micr&oacute;fono, la '
  u'c&aacute;mara.',

  u'Y falta el que reparte. En tu ordenador hay decenas de programas queriendo la CPU y la RAM a la vez, y '
  u'nadie se pelea: hay un programa especial, el <b>sistema operativo</b>, cuyo trabajo es repartir la '
  u'm&aacute;quina entre todos, arrancarla y esconderte todo lo anterior para que t&uacute; solo tengas que '
  u'pulsar un icono.',

  u'Con esto ya puedes diagnosticar el fallo del primer p&aacute;rrafo, y diagnosticar es <b>descartar por '
  u'partes</b>, no adivinar. Si el teclado ni se ilumina ni responde en ning&uacute;n sitio, sospecha del '
  u'perif&eacute;rico o de su cable; si otros programas s&iacute; reciben letras y uno no, es software; si el '
  u'ordenador se apaga solo al escribir, mira la placa o la alimentaci&oacute;n. Todo el recorrido '
  u'&mdash;contacto, chip, cable, placa, CPU, memoria, tarjeta gr&aacute;fica y pantalla&mdash; ocurre en unas '
  u'mil&eacute;simas de segundo y t&uacute; lo percibes como instant&aacute;neo. Un ordenador no es una caja: '
  u'es una <b>cadena</b>, y una cadena se entiende mirando d&oacute;nde se rompe.',
]

PREGUNTAS = [
  u'Cuando pulsas una tecla, el teclado <b>no</b> env&iacute;a la letra. &iquest;Qu&eacute; env&iacute;a '
  u'exactamente, y por d&oacute;nde llega al resto del ordenador?',

  u'Explica con tus palabras la diferencia entre <b>hardware</b> y <b>software</b>. Despu&eacute;s pon un '
  u'ejemplo de aver&iacute;a de cada tipo que <b>no</b> est&eacute; en el texto, y di c&oacute;mo se '
  u'arreglar&iacute;a cada una.',

  u'&iquest;Qu&eacute; ten&iacute;an en com&uacute;n el telar de Jacquard y la idea de von Neumann? Se&ntilde;ala '
  u'tambi&eacute;n una diferencia importante entre los dos.',

  u'&iquest;Por qu&eacute; es falso decir que un procesador de 3 GHz ejecuta 3.000 millones de instrucciones por '
  u'segundo? &iquest;Qu&eacute; es lo que s&iacute; mide esa cifra?',

  u'Un compa&ntilde;ero dice que su ordenador va lento con muchas pesta&ntilde;as y que va a comprar un disco '
  u'duro m&aacute;s grande. &iquest;Le va a servir? Explica por qu&eacute; usando la comparaci&oacute;n de la '
  u'mesa y la estanter&iacute;a.',

  u'Si buscar un dato en la RAM costara un segundo, &iquest;cu&aacute;nto costar&iacute;a buscarlo en un disco '
  u'duro de platos? Y sobre todo: &iquest;<b>por qu&eacute;</b> tarda tanto un disco duro y un SSD no?',

  u'&iquest;Por qu&eacute; los ordenadores usan dos s&iacute;mbolos y no veintisiete, si con veintisiete '
  u'cabr&iacute;a mucho m&aacute;s por cable? Cita la cuenta que aparece en el texto.',

  u'El byte 01000001, &iquest;qu&eacute; significa? Cuidado con la respuesta: explica de qu&eacute; depende.',

  u'El Setun funcionaba y sobre el papel era m&aacute;s eficiente que un ordenador binario, y aun as&iacute; '
  u'perdi&oacute;. &iquest;Crees que en tecnolog&iacute;a gana siempre la mejor idea? Razona tu respuesta con '
  u'este caso y con otro ejemplo que se te ocurra.',

  u'El ordenador del aula se apaga solo justo cuando escribes. Explica <b>paso a paso y en orden</b> '
  u'c&oacute;mo lo investigar&iacute;as, y di qu&eacute; tendr&iacute;as que comprobar para ir descartando '
  u'causas. No des la respuesta: da el m&eacute;todo.',
]

CFG = dict(
  titulo=u'De una tecla que no responde a los ceros y unos',
  subtitulo=u'Lectura de aula &middot; Tema 7 &middot; El ordenador y sus componentes',
  entradilla=u'Un ordenador no es una caja: es una cadena de piezas que se pasan el trabajo unas a otras. '
             u'Este texto la recorre entera siguiendo una aver&iacute;a que has tenido alguna vez.',
  parrafos=PARRAFOS,
  preguntas=PREGUNTAS,
  curso=u'2.º de ESO · Tecnología y Digitalización',
  tema=u'Tema 9 · Equipos informáticos',
)

if __name__ == '__main__':
    destino = os.path.join(RAIZ, '2eso', 'TyD', 'tema9')
    os.makedirs(destino, exist_ok=True)
    ruta = lectura.genera(CFG, os.path.join(destino, 'lectura-tema9.pdf'))
    n = sum(1 for p in PARRAFOS if not isinstance(p, tuple))
    print('Lectura U7: %s  ·  %d parrafos numerados, %d preguntas, %d bytes' % (
        ruta, n, len(PREGUNTAS), os.path.getsize(ruta)))
