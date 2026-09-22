# -*- coding: utf-8 -*-
u"""Lectura de aula del tema 5 de 2.o (Metales): 30 parrafos y 10 preguntas.

    ~/rt/venv/bin/python generadores/umet_lectura.py

Deja  2eso/TyD/tema5/lectura-tema5.pdf

No repite la unidad. La unidad va de donde salen los metales, sus propiedades y
sus tipos; esto va de QUE PASA CUANDO EL METAL NO ES EL QUE TENIA QUE SER, con
un solo caso: los remaches del Titanic. Enlaza con la union por remache de la
sesion 5 y con tenacidad y fragilidad de la sesion 3.

Prudencia con el dato: los analisis de los anios noventa sobre remaches
recuperados del pecio apuntan a un exceso de escoria; se cuenta asi, como lo
que apuntan los analisis, no como sentencia.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lectura
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

P = [
    ('h', u'Tres millones de piezas del tama&ntilde;o de un dedo'),

    u'El <b>Titanic</b> se hundi&oacute; la noche del 14 al 15 de abril de 1912, en su primer viaje, despu&eacute;s '
    u'de rozar un iceberg. Eso lo sabe todo el mundo. Lo que casi nadie sabe es que la pregunta que '
    u'los ingenieros llevan un siglo haci&eacute;ndose no es sobre el hielo: es sobre el metal.',

    u'Porque el iceberg no abri&oacute; un tajo en el casco, como se cuenta. Lo que hizo fue mucho m&aacute;s '
    u'discreto: una serie de <b>aberturas estrechas</b> repartidas a lo largo del costado, con una '
    u'superficie total sorprendentemente peque&ntilde;a. Suficiente para hundir el barco en dos horas y '
    u'media.',

    u'Y esas aberturas aparecieron, sobre todo, <b>por las juntas</b>. Es decir, por donde las planchas '
    u'de acero estaban unidas unas a otras. Para entender qu&eacute; pas&oacute; hay que mirar la pieza m&aacute;s '
    u'peque&ntilde;a y m&aacute;s repetida del barco.',

    ('h', u'C&oacute;mo se un&iacute;a el acero en 1912'),

    u'Hoy un casco se <b>suelda</b>: se funde el metal de las dos planchas hasta que quedan una sola '
    u'pieza. En 1912 la soldadura el&eacute;ctrica todav&iacute;a no estaba madura para algo de ese tama&ntilde;o, as&iacute; que '
    u'los barcos se montaban con <b>remaches</b>.',

    u'Un remache es un v&aacute;stago met&aacute;lico con cabeza. Se mete al rojo por un agujero que atraviesa las '
    u'dos planchas y, por el otro lado, se machaca hasta formar una segunda cabeza. Al enfriarse '
    u'encoge y aprieta. Es una uni&oacute;n <b>fija</b>: para deshacerla hay que destruirla.',

    u'El Titanic llevaba alrededor de <b>tres millones de remaches</b>. Puestos uno a uno, por '
    u'cuadrillas de cuatro hombres: uno calentaba, otro lo llevaba, otro lo sujetaba y otro lo '
    u'machacaba. Miles de piezas id&eacute;nticas hechas a mano, y ah&iacute; est&aacute; el problema.',

    u'Y hay un detalle que lo explica casi todo: aquellas cuadrillas cobraban <b>por remache '
    u'puesto</b>. Cuando hay que colocar tres millones de piezas a mano y contrarreloj, la prisa no '
    u'es un defecto del trabajador: es c&oacute;mo estaba montado el trabajo.',

    ('h', u'Dos metales distintos en el mismo barco'),

    u'En la parte central del casco, donde las planchas eran m&aacute;s gruesas, se usaron remaches de '
    u'<b>acero</b> puestos con m&aacute;quina hidr&aacute;ulica. En la proa y en la popa, donde la forma se curva y '
    u'la m&aacute;quina no entraba, se usaron remaches de <b>hierro forjado</b> colocados a mano.',

    u'El hierro forjado no es acero. Ya sabes por el tema que la diferencia est&aacute; en el <b>carbono</b>, '
    u'y que el hierro casi puro es blando y d&uacute;ctil. Para un remache eso no es malo: precisamente se '
    u'quiere que deforme al golpearlo.',

    u'El problema no era el hierro. Era lo que llevaba <b>dentro</b>. El hierro forjado de la &eacute;poca se '
    u'obten&iacute;a con un proceso que dejaba hilos de <b>escoria</b> atrapados en el metal. Un poco de '
    u'escoria es normal y hasta conveniente. Demasiada, no.',

    u'Los an&aacute;lisis hechos en los a&ntilde;os noventa sobre remaches recuperados del pecio apuntan a que '
    u'muchos de los de proa ten&iacute;an un <b>contenido de escoria muy por encima</b> de lo que era '
    u'habitual, y mal repartido: en hilos gruesos en lugar de fibras finas.',

    u'Un remache as&iacute; aguanta bien de pie, sujetando peso. Lo que no aguanta bien es un <b>golpe '
    u'seco</b>. Y menos a&uacute;n a la temperatura del Atl&aacute;ntico norte en abril, unos dos grados bajo cero '
    u'en el agua.',

    u'Conviene decir una cosa para no ser injustos con los constructores. Los astilleros de la &eacute;poca '
    u'no ten&iacute;an forma de mirar dentro de un remache. No exist&iacute;an los <b>ensayos no destructivos</b> '
    u'que hoy permiten ver una grieta con ultrasonidos o con rayos X sin romper la pieza.',

    u'Se compraba el hierro al proveedor, se confiaba en su palabra y se miraba el resultado por '
    u'fuera. Si el remache parec&iacute;a bien puesto, estaba bien puesto. Todo lo que hemos contado sobre '
    u'la escoria se ha sabido <b>ochenta a&ntilde;os despu&eacute;s</b>, con piezas sacadas del fondo del mar.',

    ('h', u'Por qu&eacute; el fr&iacute;o importa tanto'),

    u'Aqu&iacute; entra una propiedad que ya conoces: la <b>tenacidad</b>, que es la capacidad de un '
    u'material de encajar un golpe sin romperse. Su contraria es la <b>fragilidad</b>: romperse de '
    u'golpe, sin avisar y sin deformarse antes.',

    u'Muchos aceros tienen una mala costumbre: al bajar la temperatura <b>pierden tenacidad</b>. El '
    u'mismo acero que a veinte grados se abolla, a veinte bajo cero se parte como un cristal. Esto se '
    u'descubri&oacute; a base de disgustos, y el Titanic fue uno de ellos.',

    u'El acero de las planchas del Titanic era normal para su &eacute;poca, pero llevaba m&aacute;s <b>azufre</b> '
    u'del que hoy se admite, y eso empeora justamente esa transici&oacute;n. En agua helada, ese acero '
    u'estaba en su peor momento.',

    u'As&iacute; que junta las tres cosas: planchas de acero que en fr&iacute;o se vuelven fr&aacute;giles, unidas con '
    u'remaches de hierro con demasiada escoria, y un impacto lateral que recorre el costado durante '
    u'unos segundos.',

    u'La reconstrucci&oacute;n m&aacute;s aceptada es que el iceberg no rasg&oacute; el acero: hizo <b>saltar las cabezas '
    u'de los remaches</b>. Al perder el remache, las planchas se separaron un poco por la junta, y '
    u'por ah&iacute; entr&oacute; el agua. Kil&oacute;metros de junta, unos cent&iacute;metros abiertos.',

    u'Piensa un momento en la escala. Tres millones de remaches significan tres millones de '
    u'oportunidades de que uno salga mal. Si fallara solo uno de cada mil, ser&iacute;an <b>tres mil</b> '
    u'remaches defectuosos repartidos por el casco, y bastaba con que unos cuantos coincidieran en '
    u'la misma junta.',

    u'Esa es una idea que vale para cualquier proyecto, tambi&eacute;n para el tuyo: cuando una uni&oacute;n se '
    u'repite muchas veces, <b>la calidad media no basta</b>. Lo que decide es la peor de todas, '
    u'porque por ah&iacute; empieza el fallo.',

    ('h', u'Lo que hizo la industria despu&eacute;s'),

    u'De un fallo as&iacute; no se sale con m&aacute;s material, sino con <b>saber m&aacute;s del material</b>. En las '
    u'd&eacute;cadas siguientes se normaliz&oacute; la composici&oacute;n de los aceros, se limit&oacute; el azufre y el f&oacute;sforo y '
    u'se empez&oacute; a exigir ensayos de impacto <b>a la temperatura de servicio</b>, no a temperatura '
    u'ambiente.',

    u'Tambi&eacute;n cambi&oacute; la uni&oacute;n. Los cascos pasaron a <b>soldarse</b>, que ahorra peso, mano de obra y '
    u'los tres millones de puntos d&eacute;biles. Aunque la soldadura trajo su propio problema, que cost&oacute; '
    u'otros barcos: una grieta en un casco soldado ya no se detiene en la junta siguiente, porque no '
    u'hay juntas.',

    u'Esa es la parte que conviene no olvidar: cada soluci&oacute;n t&eacute;cnica trae su propio fallo nuevo. No '
    u'se trata de encontrar la uni&oacute;n perfecta, sino de <b>saber cu&aacute;l falla</b> y vigilar eso.',

    ('h', u'Lo que esto le debe al tema'),

    u'Repasa lo que has ido usando sin darte cuenta. <b>Mena y ganga</b>: la escoria del remache es '
    u'pariente de la ganga, lo que no era metal y se col&oacute; igualmente. <b>Alto horno</b>: la caliza '
    u'estaba ah&iacute; justamente para atrapar impurezas.',

    u'<b>El carbono manda</b>: hierro dulce, acero y fundici&oacute;n son el mismo elemento con distinta '
    u'cantidad de carbono, y de ah&iacute; salen materiales que se comportan de forma completamente '
    u'distinta. <b>Tenacidad y fragilidad</b>: la propiedad que decidi&oacute; aquella noche.',

    u'<b>Uniones</b>: remache o soldadura, fija o desmontable, cada una con su ventaja y su punto '
    u'd&eacute;bil. Y <b>ensayos</b>: la &uacute;nica manera de saber si un material es el que dice ser es probarlo, '
    u'y probarlo en las condiciones en las que va a trabajar.',

    u'Si alguien te dice que el Titanic se hundi&oacute; &laquo;por un iceberg&raquo;, no est&aacute; mintiendo, pero se '
    u'queda muy corto. Se hundi&oacute; porque unas piezas del tama&ntilde;o de un dedo no eran del material que '
    u'deb&iacute;an ser, y nadie ten&iacute;a entonces la forma de comprobarlo.',

    u'Por eso la ficha t&eacute;cnica de un material no es papeleo. Un metal no se elige por su aspecto ni '
    u'por su nombre: se elige por lo que <b>se ha medido</b> de &eacute;l. Y se comprueba que lo que llega al '
    u'taller es lo que se pidi&oacute;.',

    u'Una &uacute;ltima cosa, para que el barco no quede como un museo. Ese acero sigue ah&iacute; abajo, a casi '
    u'cuatro kil&oacute;metros, y lleva un siglo <b>oxid&aacute;ndose</b>: unas bacterias se alimentan del hierro y '
    u'van formando los carámbanos de herrumbre que se ven en las fotograf&iacute;as. El pecio se est&aacute; '
    u'comiendo solo, por la misma propiedad qu&iacute;mica que estudiaste en la sesi&oacute;n 3.',
]

PREGUNTAS = [
    u'&iquest;Por qu&eacute; se dice en el texto que el iceberg no &laquo;rasg&oacute;&raquo; el casco? Explica qu&eacute; pas&oacute; en '
    u'realidad seg&uacute;n la reconstrucci&oacute;n m&aacute;s aceptada.',
    u'Explica c&oacute;mo se coloca un remache y por qu&eacute; es una uni&oacute;n fija y no desmontable.',
    u'En el Titanic hab&iacute;a remaches de dos materiales distintos y en zonas distintas. &iquest;Cu&aacute;les eran y '
    u'por qu&eacute; se us&oacute; cada uno donde se us&oacute;?',
    u'&iquest;Qu&eacute; es la escoria y de d&oacute;nde sale? Relaciona tu respuesta con lo que hace la caliza en el '
    u'alto horno.',
    u'Define tenacidad y fragilidad con tus palabras y pon un ejemplo de cada una con materiales del '
    u'taller.',
    u'&iquest;Por qu&eacute; la temperatura del agua fue importante aquella noche? &iquest;Qu&eacute; le pasa a muchos aceros '
    u'cuando baja la temperatura?',
    u'Despu&eacute;s del hundimiento, la industria hizo dos cambios: uno en la composici&oacute;n del acero y otro '
    u'en la forma de unir las planchas. Di cu&aacute;les fueron y qu&eacute; problema resolv&iacute;a cada uno.',
    u'El texto dice que la soldadura trajo su propio problema nuevo. &iquest;Cu&aacute;l era? Explica con tus '
    u'palabras por qu&eacute; una junta puede llegar a ser &uacute;til.',
    u'Un siglo despu&eacute;s el pecio se sigue deshaciendo. &iquest;Qu&eacute; propiedad qu&iacute;mica de los metales explica '
    u'eso, y qu&eacute; tres formas de proteger un metal conoces?',
    u'Imagina que tienes que elegir el material para una pieza que va a trabajar a veinte grados bajo '
    u'cero y va a recibir golpes. &iquest;Qu&eacute; le pedir&iacute;as al fabricante antes de comprarla? Nombra al '
    u'menos dos comprobaciones y di por qu&eacute; cada una.',
]

if __name__ == '__main__':
    n = sum(1 for p in P if not isinstance(p, tuple))
    if n < 30:
        sys.exit(u'Tienen que ser 30 parrafos numerados como minimo y hay %d' % n)
    if len(PREGUNTAS) != 10:
        sys.exit(u'Tienen que ser 10 preguntas y hay %d' % len(PREGUNTAS))
    destino = os.path.join(RAIZ, '2eso', 'TyD', 'tema5')
    os.makedirs(destino, exist_ok=True)
    ruta = os.path.join(destino, 'lectura-tema5.pdf')
    lectura.genera(dict(
        titulo=u'Los remaches del Titanic',
        subtitulo=u'Tres millones de piezas del tamaño de un dedo, y la noche en que unas cuantas '
                  u'no eran del material que debían ser',
        entradilla=u'El barco no se hundió por un tajo en el casco. Se hundió porque unas piezas '
                   u'pequeñas, hechas a mano y con demasiada escoria dentro, saltaron con el frío. '
                   u'Todo lo que hizo falta para entenderlo está en este tema.',
        parrafos=P, preguntas=PREGUNTAS,
        curso=u'2.º de ESO · Tecnología y Digitalización',
        tema=u'Tema 5 · Metales'), ruta)
    print(u'%s  ·  %d párrafos numerados, %d preguntas, %d bytes'
          % (ruta, n, len(PREGUNTAS), os.path.getsize(ruta)))
