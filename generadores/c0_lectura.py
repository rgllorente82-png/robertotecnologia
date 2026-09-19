# -*- coding: utf-8 -*-
u"""Lectura de aula del tema 0 de 4.o: 30 parrafos numerados y 10 preguntas, en PDF.

    python generadores/c0_lectura.py

Deja 4eso/Tecnologia/tema0/lectura-tema0.pdf. Era, con el tema 0 de 2.o, la
unica unidad del sitio sin lectura.

No repite la de 2.o. Alli se cuenta como se separaron las tres preguntas;
aqui se coge una sola idea —que el coste de hacer una copia mas puede ser
practicamente cero— y se sigue hasta donde llega, que es mucho mas lejos de lo
que parece: explica por que hay servicios enormes que no cobran, por que se los
quedan siempre las mismas empresas y por que la propiedad intelectual dejo de
poder aplicarse como estaba escrita. Termina donde tiene que terminar en 4.o:
en que esa informacion, ademas de copiarse gratis, la procesan maquinas que
deciden sobre personas, y en que la nube esta hecha de hierro y de agua.

Datos que van con fecha y que son de manual:

  - Gutenberg imprime la Biblia de 42 lineas hacia 1455 en Maguncia.
  - El Estatuto de la Reina Ana, la primera ley de derechos de autor, es de
    1710, en Gran Bretana: llega dos siglos y medio DESPUES de la imprenta.
  - Watt patenta el condensador separado en 1769; Carnot publica en 1824.
  - La primera linea telegrafica publica de Morse, Washington-Baltimore, 1844.
  - El transistor es de 1947 y el microprocesador Intel 4004 de 1971.

Las cifras de coste que aparecen son las de la escena de la unidad, y se
manejan con el mismo modelo: unos 300 euros de produccion, iguales para los
dos soportes, y unos 2 euros por disco prensado. Quien quiera comprobarlo
tiene el verificador en t0_verifica.py.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lectura

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

P = [
    ('h', u'Una propiedad rara'),

    u'Casi todo lo que se fabrica obedece a una regla que parece obvia: hacer dos cuesta más que '
    u'hacer uno. Dos sillas, dos ladrillos, dos camisas. Puedes abaratar la segunda —comprar madera '
    u'en cantidad, montar una cadena—, pero nunca conseguirás que salga gratis. Siempre hay un '
    u'material que gastar y unas horas que pagar.',

    u'Los economistas le pusieron nombre a eso hace tiempo: <b>coste marginal</b>, lo que cuesta '
    u'producir <i>una unidad más</i> de algo que ya estás produciendo. Durante toda la historia '
    u'conocida, el coste marginal de cualquier cosa ha sido mayor que cero.',

    u'Ponlo en números con un disco. Grabar, mezclar y masterizar una canción cuesta, pongamos, '
    u'unos 300&nbsp;€. Ese gasto se paga <b>una sola vez</b>, y es exactamente el mismo tanto si '
    u'luego la sacas en vinilo como si la sacas en archivo: hay que grabarla igual.',

    u'A partir de ahí empiezan a separarse. Prensar cada vinilo cuesta unos 2&nbsp;€. Mil vinilos '
    u'son 300 de producción más 2.000 de prensado: <b>2.300&nbsp;€</b>. Mil copias del archivo son '
    u'300&nbsp;€, los mismos que una. Y un millón de copias del archivo siguen siendo, más o menos, '
    u'esos mismos 300&nbsp;€.',

    u'Esa es toda la anomalía, y cabe en una frase: <b>la copia número un millón cuesta lo mismo '
    u'que la segunda, y las dos cuestan prácticamente nada</b>. No es una mejora de eficiencia. Es '
    u'una regla distinta.',

    ('h', u'Lo que se deduce de ahí'),

    u'De una propiedad tan pequeña salen consecuencias enormes, y conviene deducirlas una a una en '
    u'vez de aprendérselas. La primera: si servir a un cliente más no te cuesta nada, entonces '
    u'<b>regalar el servicio deja de ser una locura</b>. Puedes dárselo a mil millones de personas '
    u'sin arruinarte.',

    u'Segunda: si es gratis, alguien lo paga. Y lo que se paga con lo que tú aportas, que son tus '
    u'datos y tu atención. No es una maldad escondida; es la única manera de sostener algo cuyo '
    u'precio de producción es cero.',

    u'Tercera, y es la que más se nota al mirar alrededor: el que llega primero se lo queda casi '
    u'todo. Si a ti te cuesta lo mismo servir a diez que a diez millones, y a tu competidor '
    u'también, el que ya tiene diez millones puede gastar más en mejorar el producto sin subir el '
    u'precio. Por eso hay <b>cuatro o cinco empresas</b> donde antes había cientos de imprentas, '
    u'discográficas y periódicos.',

    u'Cuarta: la propiedad intelectual deja de poder aplicarse como estaba escrita. Una ley pensada '
    u'para un mundo donde copiar costaba dinero y dejaba rastro no funciona cuando copiar es apretar '
    u'una tecla. No es que la gente se volviera menos honrada: es que cambió el coste de la '
    u'infracción.',

    u'Y hay una quinta, que es la que menos se dice. Si copiar y repartir sale gratis, lo que '
    u'escasea deja de ser la copia y pasa a ser otra cosa: <b>el rato que alguien dedica a '
    u'mirarla</b>. Hay más canciones publicadas de las que podrías escuchar en varias vidas. Por '
    u'eso lo que se pelea ya no es la distribución, que no cuesta nada, sino la atención, que '
    u'sigue siendo tan limitada como siempre.',

    u'Y conviene ver que esto ya había pasado antes, más despacio. Hacia 1455 Gutenberg imprimió en '
    u'Maguncia su Biblia de 42 líneas, y por primera vez copiar un libro dejó de exigir un año de '
    u'trabajo de un copista. El coste por copia no llegó a cero, pero se desplomó.',

    u'Mira ahora la fecha de la respuesta legal: la primera ley de derechos de autor, el '
    u'<b>Estatuto de la Reina Ana</b>, es de <b>1710</b> en Gran Bretaña. Dos siglos y medio después '
    u'de la imprenta. Las reglas siempre llegan tarde a la tecnología, y ese retraso no es una '
    u'anécdota: es una propiedad del sistema.',

    ('h', u'De dónde sale que la información sean números'),

    u'Para que copiar salga gratis hace falta algo previo: que lo que copias sea <b>contable</b>. '
    u'Un surco de vinilo es una forma física, y toda forma física se degrada al copiarse: la aguja '
    u'añade ruido y se come agudos, un poco cada vez.',

    u'Digitalizar, en sentido estricto, es convertir una señal continua en una lista de números, y '
    u'son dos operaciones, no una. <b>Muestrear</b> es quedarse con el valor cada cierto tiempo, '
    u'renunciando a lo que pasa entremedias. <b>Cuantificar</b> es redondear cada valor a uno de una '
    u'lista finita.',

    u'Fíjate en lo que eso significa: digitalizar <b>siempre pierde algo</b>. La diferencia con lo '
    u'analógico no es que no pierda, es que pierde <b>una sola vez</b>, tú eliges cuánto, y a partir '
    u'de ahí ya no se pierde nada más por mucho que copies. Copiar un 7 da un 7.',

    u'Y esto tampoco necesita ordenadores. En 1844 se abrió la primera línea telegráfica pública '
    u'entre Washington y Baltimore, y por ella viajaban las letras convertidas en dos símbolos: '
    u'punto y raya. Un siglo antes del primer ordenador, el lenguaje ya se había vuelto contable.',

    u'Lo que faltaba era hacerlo barato, y eso lo trajeron el <b>transistor</b>, en 1947, y el '
    u'<b>microprocesador</b>, con el Intel 4004 de 1971. A partir de ahí, contar y copiar números '
    u'pasó a costar tan poco que dejó de merecer la pena medirlo.',

    ('h', u'Hay tres cosas distintas y se llaman igual'),

    u'Cuando alguien dice «digitalización» puede estar diciendo tres cosas que no son '
    u'intercambiables, y casi todas las discusiones sobre el tema son dos personas usando la palabra '
    u'en dos sentidos distintos.',

    u'<b>Digitalizar</b> es lo del párrafo 14: pasar un soporte a números. Escanear un plano. '
    u'<b>Digitalizar un proceso</b> es rediseñar la actividad entera para que la información sea '
    u'digital de principio a fin; no es escanear la factura, es que ya no haya factura en papel. Y '
    u'<b>transformación digital</b> es el cambio que todo eso provoca en la economía, el trabajo, la '
    u'cultura y el poder.',

    u'Y no es una distinción de diccionario: se falla continuamente. Un centro que compra '
    u'tabletas para que los alumnos lean en ellas los mismos apuntes, los mismos días y con los '
    u'mismos exámenes ha <b>digitalizado un soporte</b> y no ha tocado el proceso. Ha gastado '
    u'dinero en la acepción primera creyendo que compraba la segunda, y no le va a salir ninguna '
    u'de las ventajas que esperaba.',

    u'La diferencia entre las dos primeras no es de grado, es de fondo. Escanear la factura deja el '
    u'proceso igual y añade un paso. Quitar la factura cambia quién hace qué, y ahí es donde '
    u'aparecen las ganancias de verdad y también los despidos.',

    ('h', u'Lo que sí es nuevo'),

    u'Hasta aquí todo se ha deducido de una propiedad económica. Pero la información digital tiene '
    u'una segunda propiedad, y esa sí que no tiene precedente: <b>es procesable por máquinas</b>. No '
    u'solo se guarda y se transmite; se busca, se cruza, se analiza y se usa para entrenar sistemas.',

    u'Piénsalo con un ejemplo. Un archivo de cartas en papel se puede guardar durante siglos sin que '
    u'pase nada. Ese mismo archivo digitalizado se puede cruzar en un segundo con otros veinte, y de '
    u'ese cruce sale información sobre personas que nadie escribió en ninguna carta.',

    u'Y ahí la digitalización deja de ser una cuestión técnica. Cuando un sistema entrenado con '
    u'datos decide quién recibe un crédito, quién pasa un filtro de currículums o a quién revisa una '
    u'inspección, aparecen tres preguntas que no tienen respuesta técnica: <b>quién tiene los '
    u'datos</b>, <b>con qué criterio decide el algoritmo</b> y <b>quién responde cuando se '
    u'equivoca</b>.',

    u'Son preguntas políticas, en el sentido literal de la palabra: van de cómo se organiza una '
    u'sociedad. Y no las contesta quien programa el sistema, igual que no era el ingeniero de la '
    u'máquina de vapor quien decidía la jornada laboral en la fábrica.',

    ('h', u'La nube pesa'),

    u'Queda un último malentendido, y es el más cómodo de todos: creer que lo digital es '
    u'<b>inmaterial</b>. La palabra «nube» ayuda bastante a creérselo.',

    u'No lo es. Los centros de datos son naves llenas de máquinas que consumen electricidad sin '
    u'parar y agua para refrigerarse. Los dispositivos necesitan minerales que hay que extraer, a '
    u'menudo en condiciones que nadie enseña en los anuncios. Y la obsolescencia genera un residuo '
    u'electrónico que crece más deprisa que ningún otro.',

    u'O sea que el coste marginal de <b>copiar</b> es casi cero, pero el de <b>guardar, servir y '
    u'fabricar el aparato desde el que miras</b> no lo es en absoluto. Confundir las dos cosas es el '
    u'error que hay detrás de casi todas las cuentas alegres que verás sobre este asunto.',

    u'Por eso, cuando alguien te dé un número sobre el impacto de una tecnología, la primera '
    u'pregunta no es si el número es grande o pequeño: es <b>qué entra en la cuenta</b>. Solo la '
    u'electricidad de usarlo, o también fabricarlo, o también traerlo, o también tirarlo. Un número '
    u'sin límite declarado no se puede comparar con ningún otro.',

    u'Y esa es, en el fondo, la actitud que se te pide este curso. No la de quien está en contra ni '
    u'la de quien está a favor: la de quien pregunta de dónde sale el número, qué entra en la cuenta '
    u'y a quién le toca cada parte. Evaluar una tecnología exige contar también lo que no se ve.',
]

PREGUNTAS = [
    u'Explica qué es el coste marginal y por qué la lectura dice que, hasta lo digital, siempre '
    u'había sido mayor que cero.',
    u'Con los datos de los párrafos 3 y 4, calcula lo que cuestan 1, 250 y 5.000 copias en vinilo y '
    u'en archivo. Haz una tabla y di a partir de cuántas copias el vinilo cuesta el doble que el '
    u'archivo.',
    u'De las cuatro consecuencias que se deducen del coste marginal cero, elige la que te parezca '
    u'menos evidente y explícala con un servicio que uses.',
    u'La imprenta es de hacia 1455 y la primera ley de derechos de autor de 1710. ¿Qué dice la '
    u'lectura que demuestra ese hueco de dos siglos y medio? Busca un ejemplo actual del mismo '
    u'retraso.',
    u'¿Qué son muestrear y cuantificar? ¿Por qué dice la lectura que digitalizar siempre pierde '
    u'algo, y por qué eso no es un inconveniente frente al vinilo?',
    u'El telégrafo de 1844 era digital y no había ordenadores. Explica por qué eso obliga a '
    u'corregir la definición de digitalización que usa casi todo el mundo.',
    u'Distingue los tres sentidos de «digitalización» con un ejemplo propio de cada uno, sacado de '
    u'tu instituto o de una tienda que conozcas.',
    u'¿Por qué dice la lectura que la segunda propiedad —que la información sea procesable por '
    u'máquinas— convierte la digitalización en una cuestión política? Nombra las tres preguntas que '
    u'no tienen respuesta técnica.',
    u'«La nube pesa.» Justifica la afirmación con tres cosas físicas distintas, y explica qué error '
    u'de cuentas denuncia el párrafo 28.',
    u'Coge un titular reciente que dé una cifra sobre el impacto de una tecnología y aplícale la '
    u'pregunta del párrafo 29: ¿qué entra en esa cuenta y qué se queda fuera? Contéstalo en cinco o '
    u'seis líneas.',
]


if __name__ == '__main__':
    n = sum(1 for p in P if not isinstance(p, tuple))
    if n < 30:
        sys.exit(u'Tienen que ser 30 parrafos numerados como minimo y hay %d' % n)
    if len(PREGUNTAS) != 10:
        sys.exit(u'Tienen que ser 10 preguntas y hay %d' % len(PREGUNTAS))

    destino = os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema0')
    os.makedirs(destino, exist_ok=True)
    ruta = os.path.join(destino, 'lectura-tema0.pdf')
    lectura.genera(dict(
        titulo=u'La copia que no cuesta nada',
        subtitulo=u'Una sola propiedad económica, seguida hasta el final: de por qué hay servicios '
                  u'gratis a por qué la nube está hecha de agua y de cobre',
        entradilla=u'Hacer dos cosas siempre costó más que hacer una. Con la información digital '
                   u'dejó de ser verdad, y de esa única anomalía salen casi todos los fenómenos que '
                   u'ves a tu alrededor. Esta lectura los deduce uno a uno, en vez de enumerarlos.',
        parrafos=P, preguntas=PREGUNTAS,
        curso=u'4.º de ESO · Tecnología',
        tema=u'Tema 0 · Tecnología, técnica y sociedad'), ruta)
    print(u'%s  ·  %d párrafos numerados, %d preguntas, %d bytes'
          % (ruta, n, len(PREGUNTAS), os.path.getsize(ruta)))
