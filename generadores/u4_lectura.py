# -*- coding: utf-8 -*-
"""Lectura de aula de la U4 de 2.o (Estructuras): 30 parrafos y 10 preguntas.

    ~/venv/bin/python generadores/u4_lectura.py

Deja  2eso/TyD/tema6/lectura-tema6.pdf

No repite la unidad: la unidad ensena por que las estructuras aguantan, y esto
va de cinco que no aguantaron y de la frase que cada una dejo escrita en un
reglamento. Ninguno de los cinco fallo por falta de material, que es justo lo
que dice el tema desde la sesion 1.

Sin morbo: los muertos se dicen una vez, en una linea, y lo que se desarrolla es
que se aprendio. Fechas y cifras comprobadas una a una; fuentes en INFORME.md.
Los datos del Tacoma son LOS MISMOS que ya da la sesion 1 de la unidad.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lectura

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

P = [
    ('h', u'Lo que enseña algo que se cae'),

    u'Un puente que aguanta no enseña casi nada. Solo dice que aguantó, y no dice por cuánto: a lo '
    u'mejor le sobraba la mitad, a lo mejor estuvo a punto y nadie se enteró. Un puente que se cae, '
    u'en cambio, dice <b>exactamente dónde estaba el límite</b>. Por eso los ingenieros estudian los '
    u'fallos con un detalle que desde fuera parece morboso y no lo es: es la única forma de saber.',

    u'Aquí hay cinco. Están elegidos porque cada uno falló por un motivo distinto y porque de los '
    u'cinco salió una regla que hoy es obligatoria. Y hay algo que llama la atención cuando se ponen '
    u'juntos: <b>en ninguno de los cinco el problema fue que faltara material</b>. Ni uno. Que es '
    u'justo lo que dice esta unidad desde la primera frase.',

    u'En tres de ellos murió gente. Eso se dice una vez y se sigue, porque lo que importa en esta '
    u'lectura es lo otro: qué se entendió después, y qué frase se escribió en un reglamento para que '
    u'no volviera a pasar. Leer un reglamento sin saber esto es leer una lista de números aburridos.',

    ('h', u'1940 · La forma, no la fuerza'),

    u'El primero ya lo conoces de la sesión 1. El puente de Tacoma Narrows se abrió al tráfico el 1 '
    u'de julio de 1940, con 853 metros de vano central y un tablero estrecho rigidizado con vigas '
    u'macizas en vez de con celosías.',

    u'El 7 de noviembre de ese mismo año, con un viento de unos 68 kilómetros por hora —una '
    u'ventolera de otoño, nada raro—, el tablero se retorció durante más de una hora y se hundió. '
    u'Estaba calculado para vientos muy superiores, y esa es la parte que hay que entender.',

    u'Porque no hubo ningún momento en que el viento empujara con más fuerza de la que aquel puente '
    u'podía aguantar. La fuerza no llegó de golpe desde fuera: <b>se fue acumulando</b>. En cada '
    u'vaivén el aire metía un poco más de energía de la que la estructura era capaz de disipar, y lo '
    u'poco de cada vuelta, multiplicado por miles de vueltas, acabó retorciendo el tablero.',

    u'Y eso pasaba por la forma. Una viga maciza puesta de canto es una pared: el aire no la '
    u'atraviesa, se desprende en remolinos que van saliendo alternativamente por arriba y por abajo, '
    u'y cada remolino da un empujón. El puente que se construyó en su lugar cambió aquellas vigas '
    u'por <b>celosías trianguladas abiertas</b>, que dejan pasar el aire. Sigue en servicio.',

    u'Lo que quedó escrito: que un puente largo hay que probarlo antes en un <b>túnel de viento</b>, '
    u'con una maqueta de la sección del tablero, y ver si se comporta. Hoy eso es obligatorio en '
    u'cualquier puente de cierta luz. En 1940 no se hacía.',

    ('h', u'2000 · Una carga en la que nadie había pensado'),

    u'Londres, 10 de junio de 2000. Se abre al público la pasarela del Milenio sobre el Támesis, una '
    u'estructura de acero muy fina y muy elegante. Aquel primer día la cruzan miles de personas.',

    u'A los pocos minutos empieza a pasar algo que nadie esperaba: la pasarela <b>se mueve de '
    u'lado</b>. No sube y baja, que sería lo normal: se bambolea horizontalmente varios centímetros, '
    u'y la gente se agarra a la barandilla. Dos días después la cierran.',

    u'La explicación que se aceptó es un lazo que se muerde la cola. Cuando notas que el suelo se '
    u'mueve de lado, cambias el paso para no caerte y abres las piernas; al hacerlo empujas de lado. '
    u'Si mucha gente lo hace a la vez y al mismo compás, todos esos empujoncitos van en la misma '
    u'dirección: <b>cuanta más gente, más se mueve; cuanto más se mueve, más empujan</b>.',

    u'Aquí no se equivocó nadie en ninguna cuenta. Aquella fuerza lateral de los peatones no estaba '
    u'en las normas porque hasta entonces <b>nadie la había medido</b>: los cálculos ponían el peso '
    u'de la gente hacia abajo, que es hacia donde pesa.',

    u'La pasarela estuvo cerrada casi dos años. Se le colocaron 37 amortiguadores de fluido y 52 '
    u'amortiguadores de masa —unos pesos que se mueven a contratiempo y se comen el balanceo— y '
    u'volvió a abrir en febrero de 2002. Conviene decirlo claro: <b>nunca estuvo cerca de '
    u'romperse</b>. Era segura y era insoportable, y eso también es un fallo.',

    u'Lo que quedó escrito: que hay que calcular las fuerzas <b>horizontales</b> que hace la gente al '
    u'andar, y que una pasarela no solo tiene que aguantar, también tiene que estarse quieta. Por '
    u'honestidad: en 2021 todavía se publicaban trabajos discutiendo el detalle de por qué ocurre. '
    u'Que algo esté en las normas no significa que esté entendido del todo.',

    ('h', u'1981 · Un detalle cambiado por teléfono'),

    u'Kansas City, 17 de julio de 1981. En el vestíbulo de un hotel hay dos pasarelas interiores '
    u'colgadas del techo, una justo encima de la otra, y esa tarde hay mucha gente encima de las dos. '
    u'Las dos se desploman. Murieron 114 personas.',

    u'El diseño original era este: <b>una sola barra larga</b> colgando del techo, que atravesaba la '
    u'pasarela de arriba y seguía hasta la de abajo. Las dos pasarelas colgaban del techo, cada una '
    u'por su cuenta, y la de arriba solo aguantaba su propio peso.',

    u'Lo que se construyó fue otra cosa: <b>dos barras cortas</b>. Una del techo a la pasarela de '
    u'arriba, y otra que arrancaba de la pasarela de arriba y bajaba a la de abajo. Visto en un '
    u'dibujo pequeño parece lo mismo. No lo es.',

    u'Porque ahora la unión de la pasarela de arriba ya no sostiene una pasarela: sostiene <b>las '
    u'dos</b>. El doble de carga en la misma pieza. Y aquella unión, con el diseño original, ya iba '
    u'justa: no llegaba a lo que exigía la normativa de la ciudad.',

    u'El cambio lo propuso el taller para poder montarlo más fácil, se pidió por teléfono y se '
    u'aprobó por teléfono. Nadie rehízo la cuenta. Lo que quedó escrito: <b>cambiar un detalle '
    u'durante la obra es un cálculo nuevo</b>, por escrito y firmado por quien responde de él. Este '
    u'caso se estudia hoy en las escuelas de ingeniería de medio mundo.',

    u'Y deja una segunda lección que sorprende a todo el mundo: casi nunca falla la viga. <b>Falla la '
    u'unión.</b> Un nudo mal resuelto tira abajo una estructura hecha de piezas perfectas, y eso lo '
    u'has visto tú en pequeño cuando a un puente de canutos se le despega un nudo antes de que se '
    u'rompa ninguna barra.',

    ('h', u'2007 · Un error que durmió cuarenta años'),

    u'Minneapolis, 1 de agosto de 2007, hora punta. Un puente de celosía de acero por el que pasaban '
    u'unos ciento cuarenta mil vehículos al día se viene abajo con los coches encima. Murieron 13 '
    u'y 145 resultaron heridas.',

    u'Lo que encontró la investigación no fue óxido ni un golpe: fue un error de dibujo de los años '
    u'sesenta. Las <b>cartelas</b> —las chapas de acero que atan unas con otras las barras que llegan '
    u'a un nudo— de unos nudos concretos tenían la mitad del espesor que les correspondía. Estaban '
    u'mal desde el primer día.',

    u'Y aguantaron cuarenta años. Lo que las despertó fueron dos cosas que suenan a poca cosa: el '
    u'puente había ido <b>engordando</b> con el tiempo, capa de asfalto sobre capa de asfalto y '
    u'barreras nuevas de hormigón; y aquel día había material de obra amontonado justo encima de la '
    u'zona donde estaban esas cartelas.',

    u'Lo que quedó escrito: que las cartelas hay que calcularlas y revisarlas como cualquier otra '
    u'pieza, cosa que antes no se hacía porque se daban por buenas; y que el peso propio de un puente '
    u'<b>cambia a lo largo de su vida</b> y hay que llevar la cuenta. Un puente no es un objeto '
    u'terminado: es un objeto al que la gente le va añadiendo cosas.',

    u'Vuelve a tu ensayo del puente de canutos. La nota era lo que aguanta dividido por lo que pesa, ¿te '
    u'acuerdas? Pues esto es esa misma división a tamaño real: cada capa de asfalto que se echa '
    u'encima sube el denominador, y lo que sube el denominador se lo quita a lo que el puente todavía '
    u'puede aguantar de los coches.',

    ('h', u'1978 · El día más peligroso es mientras se construye'),

    u'Queda un tipo de fallo del que casi nunca se habla, y es el más frecuente de todos: el que '
    u'ocurre cuando la estructura <b>todavía no está terminada</b>. Sin terminar le faltan piezas, se '
    u'apoya en cosas provisionales, y encima lleva material amontonado y gente trabajando. Es cuando '
    u'peor está y cuando más se la carga.',

    u'Willow Island, en Virginia Occidental, 27 de abril de 1978. Se levantaba una torre de '
    u'refrigeración hormigonando un anillo cada día, y colgando el andamio del anillo del día '
    u'anterior. Aquel día se cargó el andamio sobre un hormigón vertido <b>18 horas antes</b>, que '
    u'tenía alrededor de la quinta parte de la resistencia necesaria. Cayó la torre entera y murieron '
    u'51 trabajadores. Es el peor accidente de construcción de la historia de Estados Unidos.',

    u'Lo que quedó escrito: que el hormigón necesita tiempo para endurecer y que ese tiempo no es una '
    u'recomendación, sino un dato que se comprueba rompiendo probetas; y que <b>el andamio y el '
    u'encofrado también son estructuras</b>, que se calculan y se revisan con el mismo rigor que lo '
    u'que se está construyendo, aunque vayan a durar dos semanas.',

    ('h', u'Lo que se lee en una norma'),

    u'Pon los cinco juntos: la forma del tablero, una carga que nadie había medido, un detalle '
    u'cambiado por teléfono, un error dormido cuarenta años y un hormigón al que no se dejó '
    u'endurecer. Ninguno dice «hacía falta más material». Todos dicen otra cosa: <b>alguien no miró '
    u'por dónde iban las fuerzas</b>.',

    u'Y por eso un reglamento de construcción se lee mal si se lee como una lista de números. Es otra '
    u'cosa. Es <b>la lista de lo que ya se cayó</b>, y cada línea la escribió alguien después de '
    u'pasarse meses mirando un montón de escombros para entender por qué. Cuando te toque cumplir una '
    u'norma que te parezca exagerada, acuérdate de que casi siempre hay una fecha detrás.',
]

PREGUNTAS = [
    u'La lectura dice que en Tacoma «el fallo estuvo en la forma, no en la fuerza». Explícalo y di '
    u'qué se cambió en el puente que se construyó después. Cita el párrafo.',
    u'¿Por qué se movía de lado la pasarela del Milenio? Di quién hacía esa fuerza y por qué se iba '
    u'haciendo más grande.',
    u'¿Qué no estaba en las normas antes del año 2000 y sí está ahora? Escríbelo con tus palabras.',
    u'Explica el cambio que se hizo en las barras del hotel de Kansas City. Puedes ayudarte de un '
    u'dibujo: dos barras cortas en vez de una larga.',
    u'Aquella unión ya solo llegaba, con el diseño original, al 60 % de lo que pedía la norma. Si el '
    u'cambio le puso el doble de carga, ¿a qué porcentaje de lo exigido se quedó?',
    u'En Minneapolis el error llevaba cuarenta años sin dar problemas. Di las dos cosas que lo '
    u'despertaron.',
    u'¿Qué tiene que ver la nota de tu puente de canutos —lo que aguanta dividido por lo que pesa— '
    u'con las capas de asfalto de un puente de verdad?',
    u'¿Por qué el momento más peligroso de una estructura suele ser mientras se está construyendo? '
    u'Da dos razones que estén en el texto.',
    u'De los cinco casos, ¿cuál te parece el que tiene más probabilidades de volver a ocurrir hoy? '
    u'Razona tu respuesta: no vale decir cuál te ha impresionado más.',
    u'La lectura termina diciendo que un reglamento es «la lista de lo que ya se cayó». ¿Se te '
    u'ocurre otro sitio, fuera de la construcción, donde las reglas se hayan escrito de esa misma '
    u'manera? Explica el ejemplo en cuatro o cinco líneas.',
]


if __name__ == '__main__':
    n = sum(1 for p in P if not isinstance(p, tuple))
    if n < 30:
        sys.exit(u'Tienen que ser 30 parrafos numerados como minimo y hay %d' % n)
    if len(PREGUNTAS) != 10:
        sys.exit(u'Tienen que ser 10 preguntas y hay %d' % len(PREGUNTAS))

    destino = os.path.join(RAIZ, '2eso', 'TyD', 'tema6')
    os.makedirs(destino, exist_ok=True)
    ruta = os.path.join(destino, 'lectura-tema6.pdf')
    lectura.genera(dict(
        titulo=u'Por qué se caen los puentes',
        subtitulo=u'Cinco estructuras que fallaron y la frase que cada una dejó escrita en un '
                  u'reglamento',
        entradilla=u'Ninguna de las cinco se cayó por falta de material. Se cayeron por la forma, '
                   u'por una carga en la que nadie había pensado, por un detalle cambiado por '
                   u'teléfono, por un error que durmió cuarenta años y por no dejar endurecer el '
                   u'hormigón. De cada una salió una regla que hoy es obligatoria.',
        parrafos=P, preguntas=PREGUNTAS,
        curso=u'2.º de ESO · Tecnología y Digitalización',
        tema=u'Tema 6 · Estructuras'), ruta)
    print(u'%s  ·  %d párrafos numerados, %d preguntas, %d bytes'
          % (ruta, n, len(PREGUNTAS), os.path.getsize(ruta)))
