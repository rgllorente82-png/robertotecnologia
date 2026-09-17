# -*- coding: utf-8 -*-
"""Lectura de aula de la U8: 30 parrafos numerados y 10 preguntas, en PDF.

    python generadores/u8_lectura.py   ->  2eso/TyD/tema8/lectura-tema8.pdf

El hilo es un solo gesto -le das al play en el recreo- y el texto lo sigue hasta
el final: que viaja, quien lo ve pasar y que dejas por el camino. Asi la lectura
no es un resumen del tema: es el tema contado desde donde el alumno lo vive.

Los datos que llevan cifra estan comprobados uno a uno; los dos que vienen de
fuera (los ingresos de 2025 y el numero de usuarios) van con su fuente en el
propio parrafo, que es donde tiene que estar.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lectura

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PARRAFOS = [
  (u'h', u'Le das al play'),

  u'Recreo. Sacas el m&oacute;vil, le das a un v&iacute;deo y el v&iacute;deo empieza. Ha tardado menos de un '
  u'segundo y no ha pasado nada raro, as&iacute; que no te has parado a pensarlo. Conviene pararse, porque '
  u'ese v&iacute;deo <b>no estaba dentro del m&oacute;vil</b>: estaba guardado en una m&aacute;quina que puede '
  u'estar a cinco mil kil&oacute;metros, y en ese segundo ha cruzado medio mundo.',

  u'Antes de seguir, la pregunta honrada: si te pidieran dise&ntilde;ar eso, &iquest;c&oacute;mo lo har&iacute;as? '
  u'Casi todo el mundo contesta lo mismo, y no es ninguna tonter&iacute;a: <b>una l&iacute;nea reservada</b> '
  u'desde donde est&aacute; el v&iacute;deo hasta tu m&oacute;vil. El tel&eacute;fono funcion&oacute; exactamente '
  u'as&iacute; durante cien a&ntilde;os, y al principio hab&iacute;a una persona enchufando el cable a mano.',

  u'La idea se cae con tres cuentas. Una l&iacute;nea reservada la usa <b>una sola persona</b> mientras dure '
  u'el env&iacute;o. Para que en un instituto de 600 personas cualquiera pudiera hablar con cualquiera '
  u'har&iacute;an falta 600 &times; 599 &divide; 2 = <b>179.700 cables</b>, y en el mundo hay unos 5.500 '
  u'millones de usuarios. Y si a mitad de camino se corta el cable, se pierde todo y hay que empezar '
  u'de cero.',

  (u'h', u'Trozos numerados'),

  u'Lo que se hace es casi lo contrario de reservar: <b>no reservar nada</b>. Lo que quieras mandar se '
  u'parte en trozos, y cada trozo lleva escrito de d&oacute;nde viene, a d&oacute;nde va y <b>qu&eacute; '
  u'n&uacute;mero de trozo es</b>. Se llaman <b>paquetes</b>. Se sueltan a la red y cada uno se busca la '
  u'vida por su cuenta.',

  u'De ah&iacute; salen tres consecuencias que parecen defectos y son justo lo contrario. Los paquetes de '
  u'un mismo v&iacute;deo <b>pueden ir por caminos distintos</b>. Pueden <b>llegar desordenados</b>, y da '
  u'igual, porque el destino los coloca por su n&uacute;mero antes de ense&ntilde;ar nada. Y el mismo cable '
  u'lo usan a la vez miles de conversaciones, porque nadie lo tiene reservado.',

  u'&iquest;Y si uno se pierde por el camino? Se nota enseguida: falta un n&uacute;mero. El destino '
  u'<b>vuelve a pedir ese</b>, y nada m&aacute;s que ese. Compara eso con la l&iacute;nea reservada, donde '
  u'cortar el cable obligaba a repetirlo todo. La red no es fr&aacute;gil por estar hecha de trozos: es '
  u'robusta <i>porque</i> est&aacute; hecha de trozos.',

  u'Para que un paquete sepa a d&oacute;nde va, cada m&aacute;quina de la red tiene un n&uacute;mero que la '
  u'identifica: su <b>direcci&oacute;n IP</b>, como 192.0.2.41. Con el formato cl&aacute;sico hay '
  u'2<sup>32</sup> = 4.294.967.296 direcciones, unos 4.300 millones. Somos 8.000 millones de personas y '
  u'muchas tenemos varios aparatos: <b>no llegan</b>. Por eso existe el formato nuevo, IPv6, con '
  u'2<sup>128</sup>, un 34 seguido de 37 cifras.',

  u'En cada cruce del camino hay una m&aacute;quina que mira la direcci&oacute;n de destino y decide por '
  u'd&oacute;nde sale el paquete: el <b>router</b>. Dos detalles que no son obvios. No elige el camino '
  u'm&aacute;s corto en kil&oacute;metros, sino el que <b>tarda menos</b>, que depende de por d&oacute;nde va '
  u'el cable y de cu&aacute;nta gente lo est&eacute; usando. Y si un camino se cae, <b>recalcula solo</b>.',

  u'Eso de aguantar con trozos rotos no es casualidad: es lo que se buscaba. La idea de trocear los '
  u'mensajes se les ocurri&oacute; por separado a <b>Paul Baran</b> en Estados Unidos (1964) y a '
  u'<b>Donald Davies</b> en el Reino Unido (1965), que fue quien los llam&oacute; <i>paquetes</i>. La '
  u'primera red que lo hizo, ARPANET, mand&oacute; su primer mensaje el <b>29 de octubre de 1969</b>: iban '
  u'a escribir LOGIN, el sistema se cay&oacute; despu&eacute;s de la O, y el primer mensaje de Internet fue '
  u'&laquo;LO&raquo;.',

  u'Falta una pieza: t&uacute; no escribes 192.0.2.41, escribes un nombre. Traducirlo es trabajo del '
  u'<b>DNS</b>, la agenda de Internet, que no est&aacute; en un sitio sino repartida: se pregunta a quien '
  u'lleva los <b>.es</b>, ese dice qui&eacute;n lleva ese dominio, y ese da el n&uacute;mero. La respuesta se '
  u'guarda un rato &mdash;la <b>cach&eacute;</b>&mdash; y por eso la segunda visita a un sitio arranca antes.',

  u'Conviene separar dos cosas que se confunden siempre. <b>Internet</b> es la red que mueve paquetes, y '
  u'es de 1969. La <b>web</b> &mdash;las p&aacute;ginas enlazadas entre s&iacute;&mdash; funciona <i>encima</i> '
  u'de Internet y la invent&oacute; Tim Berners-Lee en el CERN en 1989, veinte a&ntilde;os despu&eacute;s. El '
  u'correo, las videollamadas o los juegos en red van por Internet y tampoco son la web.',

  u'&iquest;Y por d&oacute;nde va todo esto f&iacute;sicamente? Sobre todo por <b>cables submarinos</b>: '
  u'fibras de vidrio del grosor de un pelo, metidas en acero y pl&aacute;stico, tiradas por el fondo del '
  u'mar. Dentro, la se&ntilde;al son pulsos de luz a unos <b>200.000 km/s</b>. De Madrid a Nueva York hay '
  u'5.800 km, as&iacute; que la luz tarda <b>29 mil&eacute;simas de segundo</b> en llegar. Eso no lo mejora '
  u'nadie: por m&aacute;s megas que contrates, la f&iacute;sica no se compra.',

  (u'h', u'Qui&eacute;n lo ve pasar'),

  u'Ahora la parte inc&oacute;moda. Tus paquetes han pasado por diez o veinte m&aacute;quinas que <b>no son '
  u'tuyas</b>: el router del instituto, el de tu operador, unos cuantos por el camino. Todas ellas '
  u'<b>tienen que leer la direcci&oacute;n</b>, o no sabr&iacute;an d&oacute;nde mandarlo. La pregunta es '
  u'qu&eacute; m&aacute;s pueden leer.',

  u'La soluci&oacute;n que se le ocurre a cualquiera es un <b>c&oacute;digo</b>: cambiar cada letra por otra, '
  u'como hac&iacute;a Julio C&eacute;sar corriendo el abecedario unas posiciones. Es ingenioso y no sirve. '
  u'Hay 26 maneras de correr un abecedario de 26 letras, una de ellas es dejarlo igual: <b>25 pruebas</b>. '
  u'Un secreto que se acaba probando entero no es un secreto.',

  u'Y hay un problema peor, que no es de matem&aacute;ticas. Si lo secreto es <b>el m&eacute;todo</b>, el '
  u'd&iacute;a que una sola persona se va de la lengua hay que cambi&aacute;rselo <b>a todo el mundo a la '
  u'vez</b>. Con mil millones de usuarios, eso no se puede hacer.',

  u'La respuesta lleva escrita desde <b>1883</b>, cuando un profesor holand&eacute;s de idiomas, Auguste '
  u'Kerckhoffs, public&oacute; un art&iacute;culo sobre criptograf&iacute;a militar: el <b>m&eacute;todo tiene '
  u'que poder ser p&uacute;blico</b> y lo &uacute;nico secreto tiene que ser la <b>clave</b>. As&iacute;, si se '
  u'escapa una clave, se cambia esa clave y ya est&aacute;. Los sistemas que se usan hoy est&aacute;n '
  u'publicados enteros, precisamente para que todo el mundo intente romperlos.',

  u'El ejemplo m&aacute;s caro de hacerlo al rev&eacute;s es la <b>Enigma</b>, la m&aacute;quina con la que el '
  u'ej&eacute;rcito alem&aacute;n cifraba en la Segunda Guerra Mundial. La m&aacute;quina era el m&eacute;todo y '
  u'la colocaci&oacute;n de sus rotores, la clave. Cre&iacute;an que el m&eacute;todo era secreto; no lo era, '
  u'porque se capturaron m&aacute;quinas, y a partir de ah&iacute; matem&aacute;ticos polacos y luego '
  u'brit&aacute;nicos leyeron sus mensajes durante a&ntilde;os.',

  u'Hoy, cuando una direcci&oacute;n empieza por <b>http</b>, lo que mandas viaja tal cual y cualquier salto '
  u'del camino puede leerlo y cambiarlo. Cuando empieza por <b>https</b>, va cifrado, y eso es lo que '
  u'significa el candado del navegador. El candado dice tres cosas: que nadie del camino puede leerlo, '
  u'que nadie puede cambiarlo sin que se note, y que est&aacute;s hablando con el due&ntilde;o de <i>ese</i> '
  u'dominio.',

  u'Igual de importante es lo que el candado <b>no</b> dice. No dice que la web sea honrada: una tienda '
  u'falsa tambi&eacute;n puede tener candado, porque el candado certifica <b>qui&eacute;n</b> es, no si es de '
  u'fiar. No esconde <b>a qu&eacute; sitio</b> te conectas, solo lo que dices dentro. Y no protege los '
  u'extremos: en tu m&oacute;vil y en el servidor el texto est&aacute; claro, porque si no, no se podr&iacute;a '
  u'usar.',

  u'Queda un problema precioso. Para cifrar hac&iacute;a falta una clave que tengan los dos, pero t&uacute; y '
  u'esa web <b>no os hab&eacute;is visto nunca</b> y todo lo que dig&aacute;is pasa por m&aacute;quinas de '
  u'otros. La salida es una cuenta con una propiedad rara: cada uno elige un n&uacute;mero secreto, hace '
  u'una operaci&oacute;n y manda <b>el resultado</b>; con el resultado del otro, los dos llegan al mismo '
  u'n&uacute;mero final. Quien lo ha o&iacute;do todo tiene los resultados, pero deshacer esa cuenta hacia '
  u'atr&aacute;s es lo que nadie sabe hacer en un tiempo razonable. Tu navegador lo hace con cada web, solo, '
  u'antes de empezar.',

  u'Con eso se entiende lo de la <b>wifi abierta</b>. Hace quince a&ntilde;os era un problema serio, porque '
  u'casi toda la web iba en http: conectarse en una cafeter&iacute;a y entrar en el correo era mandar la '
  u'contrase&ntilde;a escrita delante de quien quisiera mirar. Hoy casi todo va cifrado y <b>ese</b> '
  u'problema est&aacute; resuelto. Sigue estando el otro: quien controla la red ve <b>a qu&eacute; sitios '
  u'entras</b>, y puede ense&ntilde;arte una p&aacute;gina suya pidi&eacute;ndote que instales algo o que '
  u'aceptes un aviso raro. Ah&iacute; ya no te protege el cifrado; te protege no aceptar.',

  (u'h', u'Lo que dejas al pasar'),

  u'Si nadie puede leer lo que mandas, aparece una pregunta raras veces bien contestada: &iquest;de '
  u'd&oacute;nde sale entonces todo lo que saben de ti? Empecemos por el dinero. La aplicaci&oacute;n que '
  u'm&aacute;s usas no te ha costado nada y en la empresa que la hace trabajan decenas de miles de '
  u'personas. Ese dinero sale de alg&uacute;n sitio.',

  u'La empresa que tiene Instagram y WhatsApp public&oacute; sus cuentas de 2025 en enero de 2026: '
  u'<b>200.966 millones de d&oacute;lares</b> de ingresos, casi todos de publicidad, y <b>3.580 millones '
  u'de personas</b> usando sus aplicaciones cada d&iacute;a. Haz la divisi&oacute;n: salen unos <b>56 '
  u'd&oacute;lares por persona y a&ntilde;o</b>, menos de cinco al mes. Por ti solo pagan poco m&aacute;s que '
  u'un bocadillo; lo que vale una fortuna es la <b>suma</b>, y sobre todo saber <b>a qui&eacute;n</b> se le '
  u'ense&ntilde;a cada anuncio.',

  u'Ah&iacute; est&aacute; la respuesta, y no tiene nada de pel&iacute;cula de esp&iacute;as. Una parte de lo que '
  u'saben <b>se la damos nosotros</b>, simplemente usando el servicio: qu&eacute; miras, cu&aacute;nto rato te '
  u'quedas en cada cosa, a qui&eacute;n sigues, d&oacute;nde est&aacute;s, qu&eacute; escribes e incluso qu&eacute; '
  u'escribes y luego borras sin enviar. Nada de eso hay que interceptarlo: se lo entregas al llegar.',

  u'La otra parte la da el aparato solo. Para ense&ntilde;arte bien una p&aacute;gina, tu navegador cuenta '
  u'qu&eacute; tama&ntilde;o tiene la pantalla, en qu&eacute; idioma la quieres, qu&eacute; sistema llevas, '
  u'cu&aacute;ntos n&uacute;cleos tiene el procesador. Cada dato suelto no dice nada; <b>la combinaci&oacute;n '
  u's&iacute;</b>. Se llama <b>huella digital</b>, y funciona igual que reconocer a alguien de espaldas: '
  u'ning&uacute;n rasgo es raro, pero todos juntos casi no se repiten.',

  u'Lo importante de la huella es que <b>no se borra</b>. Una <b>cookie</b> &mdash;un dato que una web '
  u'guarda dentro de tu navegador para reconocerte&mdash; s&iacute; se puede ver y borrar. La huella no te '
  u'la ha puesto nadie: es c&oacute;mo es tu aparato. Es la diferencia entre que te peguen una pegatina en '
  u'la espalda y que te reconozcan por la cara.',

  u'De cookies hay dos clases y no est&aacute; de m&aacute;s distinguirlas. Las <b>propias</b> las pone la web '
  u'en la que est&aacute;s, y muchas hacen falta de verdad: mantener la sesi&oacute;n abierta, acordarse del '
  u'idioma, guardar el carrito. Las <b>de terceros</b> las pone otra empresa a trav&eacute;s de esa web, y '
  u'como est&aacute; en muchas webs a la vez, puede ir juntando por d&oacute;nde pasas.',

  u'Los <b>permisos</b> del m&oacute;vil son la tercera puerta, y la que m&aacute;s se regala. &laquo;Permitir '
  u'ubicaci&oacute;n&raquo; no significa que alguien sepa d&oacute;nde est&aacute;s ahora: significa que puede '
  u'apuntarlo cada cinco minutos. Son 12 puntos por hora, <b>288 al d&iacute;a</b> y <b>8.640 al mes</b>. '
  u'Con los de 0:00 a 6:00 sale d&oacute;nde duermes; con los de la ma&ntilde;ana, a qu&eacute; centro vas. '
  u'Nadie ha le&iacute;do nada tuyo: han sumado puntos en un mapa.',

  u'Nada de esto lo invent&oacute; Internet. Las <b>tarjetas de fidelizaci&oacute;n</b> de los supermercados '
  u'hacen lo mismo desde hace d&eacute;cadas y el trato es transparente: descuento a cambio de que la '
  u'tienda sepa qu&eacute; compras y cada cu&aacute;nto. Lo que ha cambiado no es el trato, es el '
  u'<b>coste</b>: antes hab&iacute;a que fabricar tarjetas y pasarlas por un lector, y ahora se hace solo, '
  u'con todo el mundo y a la vez.',

  u'Cuando saber sale casi gratis, hace falta una ley, y la hay. El <b>Reglamento General de '
  u'Protecci&oacute;n de Datos</b> es europeo y se aplica desde el <b>25 de mayo de 2018</b>: obliga a '
  u'pedirte permiso, a decirte para qu&eacute;, a dejarte <b>ver</b> lo que tienen tuyo, <b>corregirlo</b> y '
  u'pedir que lo <b>borren</b>, y a avisarte si hay una fuga. De ah&iacute; salen los avisos de cookies. '
  u'Muchos est&aacute;n mal hechos a prop&oacute;sito &mdash;aceptar bien grande, rechazar escondido&mdash;, y '
  u'eso tambi&eacute;n lo prohíbe la ley; en Espa&ntilde;a se le puede reclamar gratis a la Agencia '
  u'Espa&ntilde;ola de Protecci&oacute;n de Datos.',

  u'Terminamos donde empezamos, con el v&iacute;deo del recreo. En ese segundo ha habido un nombre '
  u'traducido a un n&uacute;mero, un mensaje partido en trozos numerados, unos cuantos routers eligiendo '
  u'camino, una clave acordada delante de todo el mundo y unos cuantos datos tuyos entregados sin '
  u'que nadie te los robara. Ninguna de esas cosas es buena ni mala por s&iacute; misma.',

  u'Y esa es la idea con la que conviene salir de aqu&iacute;. Esto no se estudia para tener miedo de '
  u'Internet, que adem&aacute;s ser&iacute;a in&uacute;til: lo vas a seguir usando, y bien usado es '
  u'extraordinario. Se estudia para <b>decidir mejor</b>, que es otra cosa. Quien sabe lo que hace un '
  u'permiso decide si lo da; quien sabe qu&eacute; protege un candado sabe qu&eacute; mirar antes de escribir '
  u'una contrase&ntilde;a. Entender c&oacute;mo funciona una cosa es lo &uacute;nico que convierte a un usuario '
  u'en alguien que elige.',
]

PREGUNTAS = [
  u'&iquest;Por qu&eacute; no se reserva una l&iacute;nea entera para cada conversaci&oacute;n, como hac&iacute;a '
  u'el tel&eacute;fono antiguo? Cita <b>dos</b> de las tres razones que da el texto, con sus n&uacute;meros.',

  u'Explica con tus palabras qu&eacute; lleva escrito un <b>paquete</b> adem&aacute;s de su trozo de '
  u'informaci&oacute;n, y para qu&eacute; sirve cada una de esas tres cosas.',

  u'Un router recibe un paquete. &iquest;Qu&eacute; mira y qu&eacute; decide? &iquest;Por qu&eacute; el texto dice '
  u'que <b>no</b> elige el camino m&aacute;s corto?',

  u'&iquest;Qu&eacute; hace el DNS, y por qu&eacute; hace falta si la red ya sabe llevar paquetes? Explica '
  u'tambi&eacute;n para qu&eacute; sirve la <b>cach&eacute;</b>.',

  u'&iquest;Por qu&eacute; contratar una conexi&oacute;n m&aacute;s r&aacute;pida no reduce los 29 milisegundos '
  u'que tarda la luz en llegar a Nueva York? Usa la comparaci&oacute;n que se te ocurra, pero razona la '
  u'diferencia.',

  u'El c&oacute;digo de C&eacute;sar falla por dos motivos distintos, y uno de ellos no es de '
  u'matem&aacute;ticas. Explica los dos.',

  u'Enumera las <b>tres</b> cosas que garantiza el candado y las <b>tres</b> que no. Despu&eacute;s '
  u'contesta: si una p&aacute;gina que te pide la contrase&ntilde;a tiene candado, &iquest;puedes fiarte? '
  u'&iquest;Qu&eacute; habr&iacute;a que mirar?',

  u'&iquest;Cu&aacute;l es la diferencia entre una <b>cookie</b> y la <b>huella digital</b>? &iquest;Por '
  u'qu&eacute; borrar las cookies no borra la huella?',

  u'El texto dice que lo de los datos &laquo;no lo invent&oacute; Internet&raquo; y pone el ejemplo de las '
  u'tarjetas de fidelizaci&oacute;n. &iquest;Te parece que es <b>lo mismo</b> o que hay alguna diferencia '
  u'importante? Razona tu respuesta con lo que dice el texto y con lo que pienses t&uacute;.',

  u'Una aplicaci&oacute;n que te gusta mucho te pide el permiso de ubicaci&oacute;n y no lo necesita para '
  u'funcionar. &iquest;Qu&eacute; haces, y por qu&eacute;? No hay respuesta correcta: lo que se valora es que '
  u'la decisi&oacute;n est&eacute; razonada con lo que has le&iacute;do.',
]

CFG = dict(
  titulo=u'El viaje de un vídeo, y quién lo ve pasar',
  subtitulo=u'Lectura de aula &middot; Tema 8 &middot; Internet, datos y seguridad',
  entradilla=u'Le das al play en el recreo y el v&iacute;deo empieza. Este texto sigue ese gesto hasta el '
             u'final: qu&eacute; viaja, por d&oacute;nde, qui&eacute;n lo ve pasar y qu&eacute; dejas t&uacute; '
             u'por el camino sin que nadie te lo robe.',
  parrafos=PARRAFOS,
  preguntas=PREGUNTAS,
  curso=u'2.º de ESO · Tecnología y Digitalización',
  tema=u'Tema 8 · Internet, datos y seguridad',
)

if __name__ == '__main__':
    destino = os.path.join(RAIZ, '2eso', 'TyD', 'tema8')
    os.makedirs(destino, exist_ok=True)
    ruta = lectura.genera(CFG, os.path.join(destino, 'lectura-tema8.pdf'))
    n = sum(1 for p in PARRAFOS if not isinstance(p, tuple))
    print('Lectura U8: %s  ·  %d parrafos numerados, %d preguntas, %d bytes' % (
        ruta, n, len(PREGUNTAS), os.path.getsize(ruta)))
