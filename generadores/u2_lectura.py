# -*- coding: utf-8 -*-
"""Lectura de aula de la U2 de 2.o (Representacion grafica): 30 parrafos y 10 preguntas.

    ~/venv/bin/python generadores/u2_lectura.py

Deja  2eso/TyD/tema2/lectura-tema2.pdf

No repite la unidad: la unidad ensena a dibujar, y esto cuenta de donde salio esa
manera de dibujar. El hilo es que un plano no es un dibujo bonito, es una orden
de trabajo que tiene que significar lo mismo para quien la firma y para quien la
ejecuta, aunque no se conozcan. Eso costo setecientos anos y tres cosas:
aplanar el mundo (Monge), decir cuanto error se admite (tolerancia) y ponerse de
acuerdo (la norma).

Datos comprobados y su fuente, en INFORME.md. Lo que no se ha podido comprobar
va dicho como estimacion dentro del propio texto.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lectura

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

P = [
    ('h', u'La catedral que se dibujó en el suelo'),

    u'Una catedral gótica tardaba en levantarse cien años o más. Por la obra pasaban cientos de '
    u'canteros, y el maestro que empezaba la fachada llevaba décadas muerto cuando alguien cerraba '
    u'la bóveda. Y sin embargo las piedras encajan. La pregunta que hay que hacerse es dónde estaba '
    u'el plano, porque desde luego no era un papel doblado en el bolsillo de nadie.',

    u'Estaba en el suelo. En una sala alta de la obra se extendían varias capas finas de yeso, y '
    u'sobre ese yeso el maestro dibujaba <b>a tamaño real</b> el perfil de una moldura, el arranque '
    u'de un arco o el despiece de una ventana. Cuando el dibujo ya no hacía falta, se pisaba, se '
    u'echaba una capa nueva y se volvía a empezar. En Inglaterra se conservan dos de aquellos suelos: '
    u'el de la catedral de York, en un desván construido hacia 1290, y el de la catedral de Wells.',

    u'De ese dibujo no salía una hoja con cotas: salía una <b>plantilla</b> de madera o de chapa, '
    u'recortada con la forma exacta. El cantero cortaba la piedra y comprobaba contra la plantilla '
    u'hasta que encajaba. No había ningún número por medio, y por eso funcionaba: nadie tenía que '
    u'saber leer.',

    u'Aquellos canteros dejaban además una <b>marca</b> grabada en cada piedra que labraban, siempre '
    u'la misma. No era una firma de artista: era para cobrar, porque se pagaba por pieza. Es lo más '
    u'parecido a un cajetín que había en el siglo XIII, y dice lo mismo que dice hoy el cajetín: '
    u'quién ha hecho esto.',

    u'El sistema tenía dos agujeros, y los dos son grandes. El primero es que solo funciona si estás '
    u'allí: un suelo de yeso no se puede enviar por correo. El segundo es que todo lo que no cabe en '
    u'una plantilla —el orden del montaje, por qué esa piedra va antes que aquella, qué pasa si el '
    u'terreno cede— vive dentro de la cabeza del maestro. Si el maestro se muere, se muere con él.',

    u'De aquel mundo se conserva un cuaderno famoso, el de Villard de Honnecourt, dibujado hacia '
    u'1225, del que quedan treinta y tres hojas de pergamino en la Biblioteca Nacional de Francia. '
    u'Está lleno de máquinas, animales y edificios. Pero fíjate en lo que es: son <b>apuntes de lo '
    u'que vio</b>, no instrucciones para fabricar. Nadie construiría nada solo con eso.',

    ('h', u'Aplanar el mundo'),

    u'El problema de fondo es el que tú ya has tenido en la sesión de las vistas: el papel tiene dos '
    u'dimensiones y las piezas tienen tres. Dibujada en perspectiva, ninguna cara mide lo suyo, así '
    u'que cualquier cota que pongas encima es mentira. Hacía falta una manera de aplanar el mundo sin '
    u'perder las medidas, y esa manera no se inventó dibujando: se inventó en una fortificación.',

    u'En 1765, Gaspard Monge trabajaba como delineante en una escuela militar francesa. Le tocó un '
    u'encargo muy concreto: calcular qué partes de una fortaleza quedaban a cubierto del fuego '
    u'enemigo. Hasta entonces eso se hacía con cuentas largas, y él lo resolvió proyectando el '
    u'terreno sobre planos perpendiculares y midiendo sobre el dibujo.',

    u'Su método funcionaba tan bien que el ejército francés lo declaró <b>secreto</b> y le prohibió '
    u'publicarlo. Tuvo que esperar a la Revolución: lo enseñó por fin en 1795 y lo publicó en 1799 '
    u'con el nombre de <i>Geometría descriptiva</i>. Entre que lo ideó y que pudo contarlo pasaron '
    u'treinta y cuatro años.',

    u'Piensa un momento en eso: durante treinta y cuatro años, <b>una manera de dibujar fue un '
    u'secreto de Estado</b>. Y lo que tanto se guardaba es exactamente lo que haces tú al sacar el '
    u'alzado, la planta y el perfil de una pieza.',

    u'Aun así, Monge no resuelve el problema entero. Dos personas pueden dibujar las tres vistas '
    u'perfectamente y entenderse mal, porque falta acordar una cosa tan tonta como en qué lado se '
    u'coloca cada vista. Eso no lo dice la geometría: hay que pactarlo. Nosotros usamos el sistema '
    u'europeo y en otros países se usa el americano, que lo pone al revés.',

    ('h', u'La pieza que encaja sin que nadie la lime'),

    u'Hasta bien entrado el siglo XVIII, cada pieza se ajustaba a su sitio a lima, una por una. Un '
    u'fusil no tenía recambios: tenía piezas que solo valían para ese fusil. Si se rompía en '
    u'campaña, el armero fabricaba la pieza <b>para él</b>, midiendo sobre el hueco.',

    u'El 8 de julio de 1785, en el patio del castillo de Vincennes, el armero francés Honoré Blanc '
    u'hizo una demostración que hoy parece un truco de magia: desmontó cincuenta llaves de fusil, '
    u'revolvió todas las piezas y las volvió a montar cogiéndolas a boleo.',

    u'Entre el público estaba Thomas Jefferson, entonces embajador de Estados Unidos en Francia. '
    u'Montó él mismo varias llaves con piezas sacadas al azar, encajaron todas, y aquel mismo agosto '
    u'lo contó por carta a su gobierno. Había visto lo que iba a cambiar la fabricación entera: '
    u'piezas <b>intercambiables</b>.',

    u'Aquí conviene desconfiar de la versión bonita. En los libros escolares suele aparecer una '
    u'demostración parecida de Eli Whitney en 1801, y se cuenta como el origen de todo. Los '
    u'historiadores que han ido a mirar los fusiles que se conservan sostienen que aquellas piezas '
    u'estaban ajustadas a mano y marcadas una por una para la ocasión. La idea tardó décadas más en '
    u'ser verdad de fábrica.',

    u'Porque para que dos piezas hechas por gente que no se conoce encajen no basta con el dibujo. '
    u'Hace falta decir además <b>cuánto error se admite</b>. Ninguna pieza sale exacta: una cota de '
    u'80 nunca significa 80,000000. Significa 80 con un margen, y ese margen se escribe en el plano. '
    u'Se llama <b>tolerancia</b>, y es lo que convierte un dibujo en algo fabricable.',

    u'Y hace falta una manera de comprobarlo que no dependa de la vista de nadie: patrones físicos, '
    u'del tamaño exacto que se admite, con los que se mide la pieza. El de verdad es el «pasa / no '
    u'pasa»: si entra por un lado y no entra por el otro, vale. No hay opinión posible, que es de lo '
    u'que va todo este asunto.',

    ('h', u'Ponerse de acuerdo'),

    u'Un ejemplo de lo caro que sale no pactar nada: los tornillos. Hasta 1841, cada taller inglés '
    u'hacía su propia rosca, con su paso y su ángulo. Ese año, el ingeniero Joseph Whitworth recogió '
    u'tornillos de los principales talleres del país, sacó la media y propuso un sistema único, con '
    u'un ángulo de 55 grados para todas las medidas. Hacia 1860 ya lo usaba casi todo el mundo.',

    u'El 7 de febrero de 1904 se incendió el centro de Baltimore. Llegaron bomberos en tren desde '
    u'Washington, Filadelfia y Nueva York, con sus bombas y sus mangueras. Y sus mangueras <b>no '
    u'enroscaban</b> en las bocas de agua de Baltimore: en Estados Unidos había por entonces del '
    u'orden de seiscientos acoplamientos distintos.',

    u'El fuego ardió más de un día y arrasó decenas de manzanas del centro de la ciudad. Al año '
    u'siguiente se acordó una rosca única para mangueras y bocas de incendio, y sigue siendo la '
    u'norma allí. Quédate con esto, porque explica lo que es una norma: <b>casi siempre es la lista '
    u'de algo que ya salió mal</b>.',

    u'El papel que tienes delante es otro acuerdo. En 1786, el físico Lichtenberg describió en una '
    u'carta la proporción que se conserva al doblar una hoja por la mitad. La idea se olvidó. En 1922 '
    u'el ingeniero Walter Porstmann la juntó con otra —que la hoja grande, el A0, mida exactamente un '
    u'metro cuadrado— y con las dos se escribió la norma alemana DIN 476. En 1975 pasó a ser la norma '
    u'internacional ISO 216. Esa es la serie A de la sesión 5.',

    u'Y no se normalizó solo el papel. Los cinco tipos de línea, las tres partes de una cota, los '
    u'símbolos de los circuitos, los formatos, el cajetín. Todo eso es lo que hace que un plano '
    u'pueda viajar <b>sin carta adjunta</b>: no necesita que nadie lo explique por teléfono.',

    ('h', u'Un plano no describe: ordena'),

    u'El cajetín de la esquina es la marca de cantero de hoy, con más datos: quién lo ha dibujado, '
    u'cuándo, a qué escala y qué número de plano es. Si aparece un fallo, ese recuadro dice a quién '
    u'hay que preguntar. Por eso sin cajetín un plano no está terminado.',

    u'Y por eso un plano es un <b>documento</b>, no un dibujo. Con él se pide una licencia, se '
    u'encarga el material, se firma un presupuesto y se reclama cuando la pieza llega mal. Tiene '
    u'valor legal, igual que un contrato.',

    u'Ahí está la diferencia de fondo con el dibujo artístico, y no es que uno sea más bonito. Un '
    u'cuadro se <b>interpreta</b>: cada persona que lo mira entiende una cosa, y en eso está su '
    u'valor. Un plano se <b>ejecuta</b>: si dos talleres lo entienden distinto, el plano está mal '
    u'hecho.',

    u'Hoy el dibujo se hace en CAD y el fichero puede ir directo a una máquina que corta o a una '
    u'impresora 3D, sin que nadie vuelva a medir nada. Parece que eso lo cambia todo, y cambia menos '
    u'de lo que parece: la máquina sigue necesitando saber qué margen se admite. La tolerancia no ha '
    u'desaparecido; ahora va dentro del fichero.',

    u'Lo que sí sigue sin unificarse es el sistema de vistas. Como hay dos en el mundo, los planos '
    u'llevan en el cajetín un pequeño símbolo que avisa de cuál se ha usado. Un símbolo de un '
    u'centímetro, puesto ahí porque alguien fabricó una pieza al revés.',

    u'Hay una prueba sencilla para saber si lo que has dibujado es un plano o todavía no. Dáselo a '
    u'alguien que no estaba cuando lo pensaste y <b>que no te pueda preguntar nada</b>. Si construye '
    u'lo que tú tenías en la cabeza, es un plano. Si tiene que adivinar algo, ahí falta una cota.',

    u'Fíjate en que lo que se ha ganado en estos setecientos años no es pulso ni precisión de la '
    u'mano. El maestro que dibujaba en el yeso dibujaba muy bien. Lo que no tenía era <b>manera de '
    u'que su dibujo viajara</b>: ni un método para aplanar las tres dimensiones, ni un margen escrito, '
    u'ni unas normas que significaran lo mismo en otra ciudad.',

    u'Y el título de esta lectura hay que leerlo literal. Cuando dibujas la pieza, la pieza no '
    u'existe. El plano no es la copia de nada: <b>es lo primero que existe de ese objeto</b>, y todo '
    u'lo demás —el material, el presupuesto, el taller, la pieza en la mano— viene detrás y viene de '
    u'ahí.',
]

PREGUNTAS = [
    u'¿Dónde estaba el «plano» de una catedral gótica y para qué servía la plantilla? Cita el '
    u'párrafo donde lo has encontrado.',
    u'La lectura dice que aquel sistema tenía dos agujeros grandes. ¿Cuáles eran? Explícalos con tus '
    u'palabras.',
    u'Monge ideó su método en 1765 y lo publicó en 1799. ¿Cuántos años pasaron, y por qué no pudo '
    u'publicarlo antes?',
    u'Explica qué hizo Honoré Blanc en 1785 y por qué a Jefferson le pareció tan importante.',
    u'Un A0 mide un metro cuadrado. Sabiendo que cada formato es la mitad del anterior, ¿cuántos A4 '
    u'caben en un A0? ¿Cuánto mide entonces un A4 en centímetros cuadrados?',
    u'Una cota dice 80 mm con una tolerancia de más o menos 0,2 mm. ¿Entre qué dos medidas puede '
    u'salir la pieza y cuánta diferencia hay, en milímetros, entre la más grande y la más pequeña '
    u'que se aceptan?',
    u'¿Por qué dice la lectura que una norma es «casi siempre la lista de algo que ya salió mal»? '
    u'Contéstalo con el caso de Baltimore.',
    u'¿Con qué compara la lectura el cajetín de un plano de hoy, y qué tienen en común?',
    u'Coge la última lámina que has dibujado en clase y pásale la prueba del párrafo 28: dásela '
    u'mentalmente a alguien que no te puede preguntar nada. ¿La pasaría? Escribe las dos cosas que le '
    u'añadirías.',
    u'La lectura termina diciendo que el plano «es lo primero que existe de ese objeto». ¿Estás de '
    u'acuerdo? Razónalo en cuatro o cinco líneas, con algo que hayas construido o que hayas querido '
    u'construir alguna vez.',
]


if __name__ == '__main__':
    n = sum(1 for p in P if not isinstance(p, tuple))
    if n < 30:
        sys.exit(u'Tienen que ser 30 parrafos numerados como minimo y hay %d' % n)
    if len(PREGUNTAS) != 10:
        sys.exit(u'Tienen que ser 10 preguntas y hay %d' % len(PREGUNTAS))

    destino = os.path.join(RAIZ, '2eso', 'TyD', 'tema2')
    os.makedirs(destino, exist_ok=True)
    ruta = os.path.join(destino, 'lectura-tema2.pdf')
    lectura.genera(dict(
        titulo=u'Dibujar lo que todavía no existe',
        subtitulo=u'De la marca del cantero a la norma: por qué dos personas que no se conocen '
                  u'pueden fabricar la misma pieza',
        entradilla=u'Un plano no es un dibujo bonito de algo. Es una orden de trabajo que tiene que '
                   u'significar exactamente lo mismo para quien la firma y para quien la ejecuta, '
                   u'aunque estén a mil kilómetros y no hablen el mismo idioma. Conseguir eso costó '
                   u'setecientos años.',
        parrafos=P, preguntas=PREGUNTAS,
        curso=u'2.º de ESO · Tecnología y Digitalización',
        tema=u'Tema 2 · Expresión gráfica de un proyecto'), ruta)
    print(u'%s  ·  %d párrafos numerados, %d preguntas, %d bytes'
          % (ruta, n, len(PREGUNTAS), os.path.getsize(ruta)))
