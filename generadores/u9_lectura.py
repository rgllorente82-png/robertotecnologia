# -*- coding: utf-8 -*-
"""Lectura de aula de la U9: 30 parrafos numerados y 10 preguntas, en PDF.

    ~/venv/bin/python generadores/u9_lectura.py

Deja 2eso/TyD/tema9/lectura-tema9.pdf. Ocupa una sesion entera: cada alumno lee
un parrafo en voz alta, en orden, y despues se contesta por escrito.

Los parrafos son 30 justos, y esta comprobado abajo: si se anade uno hay que
quitar otro, porque el reparto en voz alta depende de que sean treinta.

Cuenta la misma historia que las tres sesiones pero por el lado del oficio: la
imprenta parte el texto de su forma, la fotografia parte la imagen en casillas
y la pantalla acaba obligando a partir lo que dices de lo que enseñas.
"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lectura

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

P = [
    ('h', u'Un trabajo que llega roto'),

    u'El domingo por la tarde el trabajo estaba terminado. Seis páginas, los títulos en su sitio, '
    u'las dos fotos donde tenían que estar. El lunes por la mañana se abre en el ordenador del '
    u'aula para imprimirlo y aquello ya no se parece: los títulos han cambiado de letra, la '
    u'segunda foto se ha subido sola a la página siguiente y donde había seis páginas ahora hay '
    u'ocho.',

    u'La primera reacción siempre es la misma: el fichero se ha estropeado. Es una explicación '
    u'razonable y es falsa, y se comprueba en diez segundos. ¿Falta alguna palabra? ¿Ha cambiado '
    u'alguna letra? ¿Se ha perdido algún párrafo? No: está todo, entero y en orden. Si estuviera '
    u'roto faltaría algo, así que lo que ha pasado es otra cosa, y esa otra cosa es una de las '
    u'ideas más útiles de la informática: un documento no guarda una fotografía de la página. '
    u'Guarda el texto y unas marcas, y la página se vuelve a construir entera cada vez que alguien '
    u'lo abre.',

    u'Y si se vuelve a construir, se construye con lo que haya en ese ordenador concreto. Si la '
    u'letra que usaste no está instalada, el programa pone otra parecida. Si esa otra es un poco '
    u'más ancha, las palabras ocupan un poco más, las líneas cortan por otro sitio, hacen falta '
    u'más líneas, y todo lo que venía debajo se desplaza. Nadie ha movido la foto: la foto se ha '
    u'quedado donde estaba, detrás de un texto que ahora es más largo.',

    ('h', u'Una idea vieja: lo que dice y cómo se ve'),

    u'Separar lo que un texto dice de la forma que tiene encima del papel no lo inventó el '
    u'ordenador. Un escriba medieval copiaba las dos cosas a la vez: cada letra que dibujaba era, '
    u'al mismo tiempo, el contenido y su forma, y no había manera de tener una sin la otra.',

    u'Con los tipos móviles eso se parte en dos oficios. Uno compone las palabras colocando piezas '
    u'de plomo en un componedor; otro decide con qué tipos se imprimen. La misma frase se puede '
    u'componer con una letra u otra sin cambiar ni una palabra. Es exactamente lo que le pasa a tu '
    u'trabajo cuando cambia de ordenador.',

    u'Conviene decir que los tipos móviles no son de Gutenberg. En China ya los usaba Bi Sheng '
    u'hacia 1040, hechos de cerámica, y el libro impreso con tipos de metal más antiguo que se '
    u'conserva es coreano, el Jikji, de 1377. Lo que Gutenberg montó en Maguncia hacia 1450 fue el '
    u'sistema completo: una aleación que permitía fundir miles de tipos iguales, una tinta que '
    u'agarraba en el metal y una prensa que apretaba fuerte y parejo.',

    u'De esa separación salen las tres familias de formatos que hoy usamos a diario. El texto '
    u'plano guarda solo las letras, una detrás de otra, y nada más: lo abre cualquier programa y '
    u'seguirá abriéndose dentro de cincuenta años, pero no tiene títulos ni negritas. El documento '
    u'de procesador guarda las letras y, además, las marcas que dicen qué papel hace cada trozo.',

    u'La tercera familia es la página fija, el PDF, y hace justo lo contrario que las otras dos: '
    u'no deja nada por decidir. Lleva calculada la posición exacta de cada letra y se lleva dentro '
    u'las propias tipografías, para no depender de las que tenga el ordenador de enfrente. Por eso '
    u'se ve igual en todas partes.',

    u'Todo tiene un precio. Un PDF cuesta de editar, porque está pensado para leerse y no para '
    u'seguir escribiéndolo, y no se adapta a una pantalla pequeña: en el móvil hay que hacer zoom, '
    u'porque la página es fija por definición. La regla práctica es sencilla: se entrega en PDF y '
    u'se guarda aparte el original, que es el que todavía se puede tocar.',

    ('h', u'Marcar no es pintar'),

    u'Casi todo el mundo hace los títulos de la misma manera: seleccionar, poner en negrita, subir '
    u'el tamaño, centrar. El resultado parece un título. Pero el programa no ha entendido nada: '
    u'para él sigue habiendo texto normal que resulta que está en negrita y más grande.',

    u'La prueba está en el índice automático. Si se pide con los títulos pintados a mano, sale '
    u'vacío, y no es un fallo del programa: nunca se le ha dicho cuáles de esas líneas son '
    u'títulos. Marcar algo con un estilo es decirle qué es; ponerlo en negrita es solo decirle '
    u'cómo se dibuja.',

    u'Un estilo es una etiqueta —Título 1, Título 2, Normal, Cita— que se le pone a un trozo de '
    u'texto, y cuyo aspecto se define una sola vez y aparte. De ahí salen tres cosas que a mano '
    u'no se pueden conseguir por mucho tiempo que se les eche.',

    u'La primera: el índice se genera solo, con sus números de página, y se actualiza cuando el '
    u'documento crece. La segunda: cambiar el aspecto de todos los títulos cuesta un retoque, y no '
    u'uno por título, que es donde siempre se queda alguno distinto. La tercera, la que menos se '
    u'cuenta: un lector de pantalla, que es lo que usa una persona ciega, puede ir saltando de '
    u'apartado en apartado. Si no hay estilos, no hay apartados a los que saltar.',

    ('h', u'Una imagen es, literalmente, una rejilla'),

    u'La segunda pieza de producir algo son las imágenes, y ahí la sorpresa llega en forma de '
    u'aviso: la presentación del grupo pesa cuarenta y ocho megas y no se puede enviar. Dentro no '
    u'hay cuarenta y ocho megas de ideas: hay once fotografías.',

    u'Detrás del objetivo de un móvil hay una rejilla de casillas diminutas, cada una con un '
    u'filtro de color delante, y cada casilla mide cuánta luz le llega. La fotografía es la lista '
    u'de esas medidas. No es una comparación: es literalmente lo que hay dentro del aparato.',

    u'Con eso se puede hacer la cuenta. Una cámara de móvil corriente hace fotos de 4.032 por '
    u'3.024 puntos, que son 12.192.768 puntos: eso significa «doce megapíxeles». Si cada punto '
    u'guarda su color en tres bytes, la foto ocupa 36.578.304 bytes, unos 35 megas. Una sola.',

    u'Pero el móvil dice que esa foto ocupa tres megas. Faltan treinta y dos, y hay dos '
    u'explicaciones distintas. La primera se llama compresión: guardar lo mismo ocupando menos. La '
    u'segunda es más incómoda: puede que la mitad de esos puntos no hicieran falta para nada.',

    u'Comprimir se puede hacer de dos maneras. Sin pérdida, aprovechando lo que se repite: '
    u'doscientos píxeles blancos seguidos se guardan como «doscientos blancos», y al abrir la '
    u'imagen sale exactamente la misma. Con pérdida, tirando información de la que el ojo no se '
    u'entera, sobre todo los cambios de color muy finos; al abrirla sale una imagen parecida, no '
    u'la misma.',

    u'De ahí sale la regla de qué formato usar. Las fotografías van en JPEG, que tira lo que no se '
    u'nota y ahorra muchísimo. Los dibujos, los esquemas y las capturas de pantalla van en PNG, '
    u'que no tira nada y comprime bien las zonas planas. Al revés, los dos quedan mal: un dibujo '
    u'en JPEG sale con sombras sucias alrededor de las letras, y una foto en PNG apenas ahorra '
    u'sitio.',

    u'Hay una tercera manera de guardar una imagen que no es una rejilla en absoluto: guardar las '
    u'instrucciones para dibujarla. Una circunferencia de tal radio aquí, una recta hasta allí, '
    u'rellena de este color. Eso es una imagen vectorial, y el formato se llama SVG.',

    u'La diferencia se ve al ampliar. Un mapa de bits ampliado enseña sus casillas, porque no hay '
    u'más detalle guardado: el que no está no aparece. Una imagen vectorial se vuelve a dibujar al '
    u'tamaño que haga falta y sigue igual de fina, desde un carné hasta una pancarta, pesando lo '
    u'mismo siempre. Por eso los logotipos, los iconos y los planos van en vectorial, y las '
    u'fotografías no: describir una cara con circunferencias y rectas necesitaría millones de '
    u'instrucciones y ocuparía más que guardar los píxeles.',

    u'Queda la frase que arregla la presentación de cuarenta y ocho megas: una imagen no tiene '
    u'tamaño, tiene píxeles. Preguntar cuántos centímetros mide una foto no tiene respuesta hasta '
    u'que alguien decide cuántos píxeles pone en cada centímetro. Y en una diapositiva proyectada '
    u'se ven, como mucho, 1.920 por 1.080. Todo lo que se lleve por encima de eso ocupa, viaja, '
    u'tarda en abrirse y no lo ve nadie.',

    ('h', u'Leer va más rápido que escuchar'),

    u'La tercera pieza es contarlo. Cinco minutos, de pie, delante de la clase. Y lo que sale casi '
    u'siempre son quince diapositivas con todo el texto escrito, por una razón comprensible: si '
    u'está ahí, no se me olvida.',

    u'El problema es de aritmética. Una persona lee en silencio a unas doscientas palabras por '
    u'minuto y escucha bastante más despacio. Si la diapositiva lleva sesenta palabras, la clase '
    u'termina de leerla en dieciocho segundos, y tú todavía estás hablando de ella cuarenta '
    u'segundos después. Durante esos veintidós segundos ya saben cómo acaba la frase y no les '
    u'queda nada que sacar de lo que dices.',

    u'La salida no es quitar texto como quien pide un favor, sino separar tres cosas que se suelen '
    u'aplastar en una. El guion es lo que vas a decir, y va en las notas o en una ficha en la '
    u'mano: no se proyecta. La diapositiva es lo que hay que ver mientras hablas: una idea. El '
    u'documento es lo que se llevan para consultar después, y ese sí lleva todo el texto.',

    u'Con las imágenes de una presentación hay una prueba que no admite discusión y dura tres '
    u'segundos: tapar la imagen con la mano. Si la diapositiva se entiende igual, esa imagen '
    u'decoraba y está quitando atención. Si deja de entenderse, la imagen estaba explicando algo, '
    u'y esa se queda.',

    u'Y hay algo que no es cuestión de gusto: si la letra se lee desde el fondo o no se lee. El '
    u'cuerpo que eliges se convierte en milímetros de mayúscula sobre la pantalla, el proyector '
    u'los multiplica por lo que estire la imagen, y desde la última fila hace falta una altura '
    u'mínima. Con una pantalla de dos metros y medio y un aula de nueve metros de fondo salen '
    u'veinticuatro puntos exactos. En otra clase sale otro número, y por eso se mide en vez de '
    u'discutirlo.',

    u'Que esto importa de verdad lo dice un caso serio. En 2003 se desintegró al volver a la '
    u'atmósfera el transbordador Columbia y murieron siete personas. La comisión que investigó el '
    u'accidente dedicó un apartado de su informe a la manera de comunicarse dentro de la NASA: los '
    u'análisis sobre el daño del ala se habían presentado en diapositivas en vez de en informes '
    u'técnicos, y la advertencia importante estaba en el tercer nivel de una lista, en letra más '
    u'pequeña que el titular tranquilizador.',

    u'La conclusión no fue que las diapositivas sean peligrosas. Fue que resumir tiene un precio: '
    u'cuando algo se aplasta hasta caber en una línea, se pierde justo lo que lo hacía importante. '
    u'Por eso en la lista de antes hay una tercera cosa, el documento: lo que no cabe en la '
    u'diapositiva no se borra, se escribe en otro sitio.',

    u'Las tres piezas de esta unidad dicen lo mismo con tres materiales distintos. Un documento se '
    u'porta bien cuando lo que dice va separado de cómo se ve. Una imagen pesa lo justo cuando '
    u'sabes cuántos de sus puntos llegan de verdad a verse. Y una presentación funciona cuando lo '
    u'que se ve y lo que se dice no compiten. Al principio del curso aprendiste a explicar una '
    u'idea con un dibujo para que otro pudiera construirla sin preguntarte nada; esto es lo mismo, '
    u'con otras herramientas.',
]

PREGUNTAS = [
    u'Un trabajo se abre en otro ordenador y se ve distinto, pero no falta ninguna palabra. '
    u'Explica qué ha pasado, sin usar la palabra «error».',
    u'¿Qué guarda un fichero de texto plano que no guarda un documento de procesador, y al revés?',
    u'¿Por qué un PDF se ve igual en cualquier ordenador? Di también dos cosas que se pierdan al '
    u'entregar algo en PDF.',
    u'Alguien pone un título en negrita y más grande, y el índice automático le sale vacío. '
    u'Explícale por qué, y qué tendría que haber hecho.',
    u'Escribe la cuenta completa del peso en bruto de una foto de 4.032 × 3.024 puntos. Pon las '
    u'unidades en cada paso.',
    u'Explica con tus palabras la diferencia entre comprimir con pérdida y sin pérdida, y di qué '
    u'formato usarías para una foto de un paisaje y cuál para una captura de pantalla.',
    u'¿Por qué un logotipo se guarda en vectorial y una fotografía no? Da una razón para cada uno.',
    u'Una diapositiva lleva 80 palabras. Calcula cuánto tarda la clase en leerla a 200 palabras '
    u'por minuto, y di qué pasa si tú vas a hablar 50 segundos sobre ella.',
    u'Quieres meter una foto de 12 megapíxeles en una diapositiva. ¿Es buena idea dejarla tal '
    u'cual? Razónalo con números y di qué harías.',
    u'De todo lo que has leído, ¿qué vas a cambiar en el próximo trabajo que entregues? Elige una '
    u'sola cosa y explica por qué esa y no otra.',
]


if __name__ == '__main__':
    n = sum(1 for p in P if not isinstance(p, tuple))
    if n != 30:
        sys.exit(u'Tienen que ser 30 parrafos numerados y hay %d' % n)
    if len(PREGUNTAS) != 10:
        sys.exit(u'Tienen que ser 10 preguntas y hay %d' % len(PREGUNTAS))

    destino = os.path.join(RAIZ, '2eso', 'TyD', 'tema9')
    os.makedirs(destino, exist_ok=True)
    ruta = os.path.join(destino, 'lectura-tema9.pdf')
    lectura.genera(dict(
        titulo=u'Lo que dice y cómo se ve',
        subtitulo=u'Por qué un trabajo llega roto, cuánto pesa de verdad una foto y por qué la '
                  u'clase deja de escucharte',
        entradilla=u'Tres historias que parecen distintas y son la misma: la imprenta separó el '
                   u'texto de su forma, la fotografía partió la imagen en casillas y la pantalla '
                   u'acabó obligando a separar lo que dices de lo que enseñas.',
        parrafos=P, preguntas=PREGUNTAS,
        curso=u'2.º de ESO · Tecnología y Digitalización',
        tema=u'Tema 9 · Herramientas digitales y difusión'), ruta)
    print(u'%s  ·  %d párrafos numerados, %d preguntas, %d bytes'
          % (ruta, n, len(PREGUNTAS), os.path.getsize(ruta)))
