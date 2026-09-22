# -*- coding: utf-8 -*-
u"""Lectura de aula del tema 4 de 2.o (Madera): 30 parrafos y 10 preguntas.

    ~/rt/venv/bin/python generadores/umad_lectura.py

Deja  2eso/TyD/tema4/lectura-tema4.pdf

No repite la unidad. La unidad va de que es la madera, como se obtiene y como
se trabaja; esto va de POR QUE UNA MADERA SUENA Y OTRA NO, con un solo objeto:
la guitarra espaniola. Antonio de Torres sale en el propio libro de Revuela
(Tema 4), asi que el alumno reconoce el nombre.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lectura
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

P = [
    ('h', u'Un instrumento que es casi todo aire'),

    u'Coge una guitarra del aula de m&uacute;sica y sost&eacute;nla con una mano. Pesa poco m&aacute;s de dos kilos, y '
    u'la mayor parte de lo que tienes en la mano es <b>hueco</b>. Es un cajón de madera fina con un '
    u'agujero delante y seis cuerdas tensadas por encima. Nada m&aacute;s.',

    u'Y sin embargo, dos guitarras del mismo tama&ntilde;o, con las mismas cuerdas y la misma forma, pueden '
    u'costar una cincuenta euros y otra quince mil. La diferencia no est&aacute; en el dise&ntilde;o. Est&aacute; en la '
    u'madera y en qui&eacute;n la eligi&oacute;.',

    u'Este texto va de eso: de por qu&eacute; una tabla de &aacute;rbol suena y otra, igual de bonita, no suena. '
    u'Todo lo que vas a leer sale de las propiedades de la madera que ya has estudiado en el tema. '
    u'Aqu&iacute; solo se ven trabajando.',

    ('h', u'El hombre que demostr&oacute; d&oacute;nde est&aacute; el sonido'),

    u'A mediados del siglo XIX, un carpintero de Almer&iacute;a llamado <b>Antonio de Torres</b> se puso a '
    u'construir guitarras. Fij&oacute; el tama&ntilde;o del cuerpo, la longitud de las cuerdas y el modo de '
    u'reforzar la tapa por dentro. La guitarra espa&ntilde;ola que se toca hoy, la de Paco de Luc&iacute;a, es '
    u'b&aacute;sicamente la suya.',

    u'Torres ten&iacute;a una teor&iacute;a incómoda para sus clientes: que el sonido de una guitarra sale casi todo '
    u'de <b>la tapa</b>, la tabla delantera, y que los aros y el fondo importan mucho menos de lo que '
    u'la gente cre&iacute;a &mdash;y de lo que la gente pagaba&mdash;.',

    u'Como no le cre&iacute;an, hizo algo que ning&uacute;n fabricante har&iacute;a hoy: construy&oacute; una guitarra con la '
    u'tapa de buena madera de abeto y <b>los aros y el fondo de cart&oacute;n piedra</b>. Un instrumento de '
    u'pega por detr&aacute;s y de verdad por delante.',

    u'Son&oacute;. No igual que una buena guitarra entera de madera, pero son&oacute; lo bastante como para '
    u'cerrar la discusi&oacute;n. La tapa es la que manda. Esa guitarra se conserva en Barcelona.',

    ('h', u'Por qu&eacute; la tapa es de abeto'),

    u'La tapa tiene que hacer dos cosas a la vez que parecen contrarias: ser <b>muy ligera</b>, para '
    u'moverse con la poca energ&iacute;a que le dan unas cuerdas, y ser <b>bastante r&iacute;gida</b>, para no '
    u'hundirse bajo la tensi&oacute;n de esas mismas cuerdas, que tiran con unos cuarenta kilos.',

    u'Ligero y r&iacute;gido a la vez es exactamente lo que es la madera <b>a lo largo de la fibra</b>. Ya lo '
    u'sabes del tema: el tronco es un manojo de tubos pegados, fort&iacute;simo en el sentido de las fibras '
    u'y f&aacute;cil de partir en el otro. Por eso la tapa se corta <b>siguiendo la veta</b>, de arriba abajo.',

    u'El abeto y el cedro rojo son con&iacute;feras: maderas <b>blandas</b>, poco densas, de fibra larga y '
    u'recta. Son las que mejor cumplen las dos condiciones. Un roble, que es mucho m&aacute;s duro y '
    u'resistente, pesar&iacute;a demasiado para lo mismo.',

    u'Dicho de otra forma: aqu&iacute; una madera &laquo;peor&raquo; es mejor. La dureza no es una virtud '
    u'universal, es una propiedad, y sirve o estorba seg&uacute;n para qu&eacute; sea la pieza.',

    ('h', u'Los anillos que se cuentan con lupa'),

    u'Un lutier &mdash;as&iacute; se llama a quien construye instrumentos de cuerda&mdash; mira una tabla de abeto '
    u'y lo primero que hace es contar los <b>anillos de crecimiento</b>. Cuanto m&aacute;s juntos, mejor.',

    u'Los anillos juntos significan que el &aacute;rbol creci&oacute; <b>despacio</b>: poca agua, poco sol, mucha '
    u'altitud, inviernos largos. Esa madera es m&aacute;s densa, m&aacute;s uniforme y m&aacute;s estable. Un abeto criado '
    u'r&aacute;pido en un valle f&eacute;rtil da anillos anchos y una tapa mediocre.',

    u'Por eso las mejores tapas salen de bosques de monta&ntilde;a, a m&aacute;s de mil metros, de &aacute;rboles que han '
    u'tardado un siglo o m&aacute;s en hacerse. Un &aacute;rbol que ha sufrido suena mejor que uno que lo tuvo '
    u'f&aacute;cil, y esa frase, por una vez, no es una met&aacute;fora: es densidad.',

    u'Una tapa tambi&eacute;n se abre por la mitad y se pegan las dos mitades como un libro, de forma que '
    u'la veta quede sim&eacute;trica. As&iacute; las dos mitades se mueven igual con la humedad y la tapa no se '
    u'tuerce hacia un lado.',

    u'Y hay una pieza m&aacute;s que no es de madera: el <b>aire</b> de dentro. La boca redonda de la tapa '
    u'no est&aacute; ah&iacute; para que se vea el interior, sino para que ese aire entre y salga. La caja y su '
    u'agujero forman un resonador que refuerza los sonidos graves; cambia el di&aacute;metro de la boca y '
    u'cambia el instrumento.',

    ('h', u'Y por qu&eacute; hay que esperar a&ntilde;os'),

    u'La madera reci&eacute;n cortada lleva agua dentro. Al secarse <b>encoge</b>, y no encoge igual en todas '
    u'las direcciones: mucho m&aacute;s a lo ancho que a lo largo. Si se construye antes de tiempo, la tapa '
    u'se agrieta sola en la vitrina de la tienda.',

    u'Un aserradero seca sus tablones en un horno en unos d&iacute;as. Un lutier no: compra la madera y la '
    u'guarda <b>a&ntilde;os</b> en un almac&eacute;n, apilada con listones entre tabla y tabla para que el aire pase. '
    u'Cinco, diez, veinte a&ntilde;os.',

    u'Eso significa que quien construye hoy una guitarra est&aacute; usando madera que compr&oacute; otra persona '
    u'hace d&eacute;cadas, y que la madera que compre hoy la usar&aacute; alguien que quiz&aacute; ni conoce. Es un oficio '
    u'que trabaja a un ritmo que no es el nuestro.',

    ('h', u'Cada pieza, su madera'),

    u'En una guitarra no hay una madera: hay cuatro o cinco, y cada una est&aacute; ah&iacute; por una propiedad '
    u'distinta. Es el mismo razonamiento que hiciste al elegir material para tu proyecto, pero hecho '
    u'por gente que lleva doscientos a&ntilde;os afin&aacute;ndolo.',

    u'La <b>tapa</b>, abeto o cedro: ligera y r&iacute;gida, ya lo hemos visto. El <b>fondo y los aros</b>, '
    u'palosanto o ciprés: m&aacute;s densos y duros, hacen de caja que devuelve el sonido en lugar de '
    u'absorberlo.',

    u'El <b>m&aacute;stil</b>, cedro: estable, que no se tuerza con los cuarenta kilos de tensi&oacute;n ni con los '
    u'cambios de humedad de ir de un sitio a otro. El <b>diapas&oacute;n</b> &mdash;la tabla donde aprietas los '
    u'dedos&mdash;, &eacute;bano: dur&iacute;simo, porque ah&iacute; hay rozamiento constante de cuerdas met&aacute;licas.',

    u'Y dentro, pegadas a la tapa, unas varillas finas llamadas <b>varetas</b>, colocadas en abanico. '
    u'Son la estructura del instrumento: reparten la tensi&oacute;n y deciden qu&eacute; zonas de la tapa vibran '
    u'm&aacute;s. Torres las coloc&oacute; de una manera concreta y todo el mundo la copia desde entonces.',

    u'El &uacute;ltimo paso tambi&eacute;n es t&eacute;cnico: el <b>acabado</b>. Una tapa se barniza con capas '
    u'finísimas, a veces a mu&ntilde;equilla, porque el barniz protege la madera de la humedad y del sudor '
    u'pero <b>a&ntilde;ade peso y rigidez</b>. Demasiado barniz apaga el instrumento; ninguno, lo deja '
    u'indefenso. Es un equilibrio, como casi todo en este tema.',

    u'Por eso a una guitarra le sienta mal el radiador del aula y el maletero del coche en agosto. '
    u'La madera sigue absorbiendo y soltando humedad toda su vida, y con ella se hincha y encoge '
    u'unas d&eacute;cimas de mil&iacute;metro. Poco, pero suficiente para que una tapa tensada se resienta.',

    ('h', u'Lo que esto le debe al tema'),

    u'Vuelve atr&aacute;s un momento y ponle nombre a lo que has le&iacute;do. Elegir el abeto por ligero: '
    u'<b>densidad</b>. Cortar siguiendo la veta: la madera no se comporta igual en todas las '
    u'direcciones. Contar anillos: crecimiento y, otra vez, densidad.',

    u'Guardar la madera a&ntilde;os: el <b>secado</b>, la s&eacute;ptima operaci&oacute;n del camino que va del bosque al '
    u'aserradero. Poner &eacute;bano en el diapas&oacute;n: <b>dureza</b>. Las varetas: una estructura que reparte '
    u'&mdash;lo que ver&aacute;s en el tema 6&mdash;.',

    u'Ninguna de esas decisiones es art&iacute;stica. Todas son t&eacute;cnicas, y todas salen de propiedades que se '
    u'pueden medir. Lo que pasa es que, juntas y bien hechas, suenan.',

    u'Una guitarra de f&aacute;brica de cincuenta euros no est&aacute; mal construida: est&aacute; construida con '
    u'contrachapado en lugar de tapa maciza, porque el contrachapado es barato, estable y no exige '
    u'esperar veinte a&ntilde;os. Cumple su funci&oacute;n. Simplemente no suena, y ahora ya sabes por qu&eacute;.',

    u'Y queda una &uacute;ltima cosa, que es la m&aacute;s rara de todas: las guitarras buenas <b>cambian con el '
    u'tiempo</b>. Tocadas durante a&ntilde;os, la madera de la tapa se asienta y el instrumento suena '
    u'distinto. Es el &uacute;nico material del taller que sigue haciendo algo despu&eacute;s de estar montado.',
]

PREGUNTAS = [
    u'&iquest;Qu&eacute; quiso demostrar Antonio de Torres con la guitarra de aros y fondo de cart&oacute;n piedra? '
    u'&iquest;Lo consigui&oacute;?',
    u'La tapa tiene que ser ligera y r&iacute;gida a la vez. Explica, con lo que sabes de la estructura de la '
    u'madera, por qu&eacute; eso se consigue cortando la tabla en el sentido de la veta.',
    u'&iquest;Por qu&eacute; se usa abeto para la tapa y no roble, si el roble es m&aacute;s resistente? Relaci&oacute;nalo con la '
    u'diferencia entre maderas de con&iacute;fera y de frondosa.',
    u'Un lutier prefiere una tabla con los anillos muy juntos. &iquest;Qu&eacute; le dice eso sobre c&oacute;mo creci&oacute; el '
    u'&aacute;rbol, y por qu&eacute; le interesa?',
    u'Enumera las capas del tronco de un &aacute;rbol y di cu&aacute;l de ellas crees que dar&iacute;a una tapa mejor. '
    u'Justifica la respuesta.',
    u'&iquest;Por qu&eacute; un lutier guarda la madera durante a&ntilde;os en vez de secarla en un horno en unos d&iacute;as? '
    u'&iquest;Qu&eacute; le pasar&iacute;a al instrumento si no lo hiciera?',
    u'Haz una tabla con las cuatro maderas del texto (tapa, aros y fondo, m&aacute;stil y diapas&oacute;n) y escribe '
    u'al lado la propiedad por la que se eligi&oacute; cada una.',
    u'Las varetas del interior de la tapa reparten la tensi&oacute;n de las cuerdas. &iquest;A qu&eacute; se parece eso de '
    u'lo que ver&aacute;s en el tema de estructuras? Explica la semejanza.',
    u'Una guitarra barata lleva contrachapado en lugar de tapa maciza. Di dos ventajas del '
    u'contrachapado para el fabricante y una desventaja para quien la toca.',
    u'Elige un objeto de madera de tu casa y explica, como se ha hecho aqu&iacute; con la guitarra, qu&eacute; '
    u'propiedad de la madera hizo que se eligiera ese material y no otro. Si crees que fue solo por '
    u'precio, dilo y razona por qu&eacute;.',
]

if __name__ == '__main__':
    n = sum(1 for p in P if not isinstance(p, tuple))
    if n < 30:
        sys.exit(u'Tienen que ser 30 parrafos numerados como minimo y hay %d' % n)
    if len(PREGUNTAS) != 10:
        sys.exit(u'Tienen que ser 10 preguntas y hay %d' % len(PREGUNTAS))
    destino = os.path.join(RAIZ, '2eso', 'TyD', 'tema4')
    os.makedirs(destino, exist_ok=True)
    ruta = os.path.join(destino, 'lectura-tema4.pdf')
    lectura.genera(dict(
        titulo=u'La guitarra que suena porque el árbol creció despacio',
        subtitulo=u'Cuatro maderas, veinte años de espera y un carpintero de Almería que lo demostró '
                  u'con cartón piedra',
        entradilla=u'Dos guitarras iguales pueden costar cincuenta euros o quince mil. La diferencia '
                   u'no está en la forma: está en qué tabla se eligió, cómo se cortó y cuánto '
                   u'tiempo estuvo esperando en un almacén.',
        parrafos=P, preguntas=PREGUNTAS,
        curso=u'2.º de ESO · Tecnología y Digitalización',
        tema=u'Tema 4 · Madera'), ruta)
    print(u'%s  ·  %d párrafos numerados, %d preguntas, %d bytes'
          % (ruta, n, len(PREGUNTAS), os.path.getsize(ruta)))
