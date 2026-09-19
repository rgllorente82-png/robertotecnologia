# -*- coding: utf-8 -*-
u"""Lectura de aula del tema 0 de 2.o: 30 parrafos numerados y 10 preguntas, en PDF.

    python generadores/u0_lectura.py

Deja 2eso/TyD/tema0/lectura-tema0.pdf. Era, junto con el tema 0 de 4.o, la
unica unidad del sitio sin lectura: las otras diecinueve la tienen.

Cuenta el tema por su espina dorsal —tecnica, ciencia y tecnologia— pero sin
definirlas de entrada: se llega a cada una viendo primero que hacia falta.
Primero dos millones de anos de saber hacer sin saber por que; luego el limite
que eso tiene y que se ve cuando algo se cae; luego la pregunta nueva; y solo
al final las dos juntas.

Datos que van con fecha y que son de manual:

  - Las herramientas de piedra talladas a proposito mas antiguas conocidas
    tienen unos 2,6 millones de anos y son del este de Africa. El estilo se
    llama olduvayense por la garganta de Olduvai, en Tanzania, que es donde se
    describio, aunque las piezas de alli sean mas recientes: por eso el parrafo
    dice «el este de Africa» y no «Olduvai» al dar la fecha.
  - La boveda del coro de la catedral de Beauvais se desplomo en 1284.
  - Watt patenta el condensador separado en 1769; Carnot publica sus
    «Reflexiones» en 1824, y la termodinamica se formula despues.
  - La primera linea telegrafica publica de Morse, Washington-Baltimore, es de
    1844, un siglo antes del primer ordenador.

Lo que no he podido comprobar en fuente se ha quedado fuera, por mucho que se
repita: no hay aqui ninguna cifra de cuanta gente hacia falta para tallar una
piedra ni de cuantas catedrales se cayeron.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lectura

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

P = [
    ('h', u'La primera vez que alguien fabricó algo'),

    u'Hace unos <b>2,6 millones de años</b>, en algún punto del este de África, alguien cogió una '
    u'piedra y golpeó con ella otra piedra. No para romperla: para arrancarle una lasca y quedarse '
    u'con el filo. Hasta ese día las herramientas se <b>encontraban</b>; desde ese día se '
    u'<b>fabrican</b>. Es la frontera más importante de esta asignatura y no la cruzó ningún genio: '
    u'la cruzó alguien que tenía hambre y un problema que resolver.',

    u'Lo asombroso no es la piedra. Lo asombroso es que la misma forma de golpear aparece en sitios '
    u'separados por cientos de kilómetros y por miles de años. Eso solo puede significar una cosa: '
    u'alguien se lo <b>enseñó</b> a alguien, que se lo enseñó a otro. La herramienta se puede '
    u'perder; el gesto de hacerla, no, mientras haya quien lo repita.',

    u'A ese saber hacer se le llama <b>técnica</b>, y responde a una pregunta muy concreta: '
    u'<i>¿cómo se hace?</i> Se aprende practicando, se transmite imitando y no necesita ninguna '
    u'explicación. El que talla bien no sabe nada de mineralogía. Sabe dónde golpear.',

    u'Y funciona. Funciona tan bien que casi toda la historia de la humanidad cabe dentro de esa '
    u'frase: gente que sabía hacer cosas excelentes sin tener ni idea de por qué salían bien.',

    ('h', u'Dos millones de años haciendo bien sin saber por qué'),

    u'Un alfarero del Neolítico metía la arcilla en el fuego y sacaba vasijas que aguantaban el agua '
    u'y el uso diario. No sabía que a unos 900 grados la arcilla cambia por dentro y ya no vuelve a '
    u'deshacerse en agua. Pero sabía cuánta leña, cuánto rato y de qué color tenía que estar el '
    u'fuego. Lo sabía <b>de verdad</b>, mejor de lo que tú y yo lo sabremos nunca.',

    u'Con el bronce pasó lo mismo: se funde cobre con estaño y sale un metal mucho más duro que '
    u'cualquiera de los dos por separado. Nadie sabía por qué. La receta viajó de taller en taller '
    u'durante siglos; el motivo tardó milenios en llegar, y llegó por otro camino.',

    u'Esta manera de saber tiene un límite, y conviene verlo claro porque es la razón de todo lo '
    u'que viene después: <b>cuando algo falla, no sabes por qué</b>. Y si no sabes por qué, no '
    u'puedes arreglarlo a propósito. Solo puedes volver a probar y esperar.',

    u'Tiene un segundo límite, aún peor: no se le pueden hacer preguntas. A una técnica no le puedes '
    u'preguntar «¿y si lo hago el doble de grande?». No hay a quién preguntárselo. Hay que '
    u'construirlo y mirar qué pasa.',

    u'En 1284 se desplomó la bóveda del coro de la catedral de Beauvais, en Francia. Era la más alta '
    u'que se había levantado nunca. Nadie pudo decir qué había fallado, porque no existía todavía la '
    u'manera de calcularlo. Se reconstruyó con <b>más piedra y más columnas</b>: es decir, por si '
    u'acaso. Así se trabajaba, y así se trabajó durante muchísimo tiempo.',

    ('h', u'Alguien empieza a preguntar por qué'),

    u'Mucho después aparece otra pregunta, y es una pregunta rara, porque quien la hace no quiere '
    u'fabricar nada: <i>¿por qué ocurre?</i> Quiere entender cómo funciona el mundo, y punto. No le '
    u'pide permiso a ninguna utilidad.',

    u'Eso es la <b>ciencia</b>. Busca una <b>explicación</b>, y tiene dos costumbres que la técnica '
    u'nunca tuvo: se <b>publica</b> y se <b>comprueba</b>. Lo que alguien afirma lo puede repetir '
    u'otro en otro sitio, y si no le sale igual, lo dice.',

    u'Fíjate en la diferencia, porque es de fondo. Una técnica se guarda: es el modo de vida de '
    u'quien la tiene. Una ciencia se publica precisamente para que la ataquen. Lo que aguanta ese '
    u'ataque durante años es lo que acaba llamándose conocimiento.',

    u'Y cuidado con el orden, que es lo que más se confunde: la técnica es <b>muchísimo</b> más '
    u'antigua que la ciencia. Millones de años de la primera, unos pocos siglos de la segunda. '
    u'Durante casi todo el camino, la humanidad supo hacer sin saber por qué.',

    ('h', u'Juntar las dos cosas'),

    u'La <b>tecnología</b> responde a una tercera pregunta, distinta de las otras dos: '
    u'<i>¿cómo resuelvo este problema?</i> Y para contestarla coge lo que la ciencia sabe y lo que '
    u'la técnica sabe hacer, y lo junta.',

    u'El ejemplo cabe en una frase. El alfarero tenía técnica: le salían vasijas perfectas. Un '
    u'químico de hoy tiene ciencia: sabe qué le pasa a la arcilla a 900 grados. Una fábrica de '
    u'cerámica tiene <b>tecnología</b>: usa las dos cosas para sacar mil platos iguales, y el número '
    u'mil es igual que el número uno.',

    u'Parece entonces que el camino va siempre en el mismo sentido: primero la ciencia descubre y '
    u'luego la tecnología aplica. Pues no siempre. A veces va justo al revés, y el caso más famoso '
    u'es una máquina que estuvo funcionando durante décadas sin que nadie supiera explicarla.',

    u'En 1769 James Watt patentó el <b>condensador separado</b>. No inventó la máquina de vapor: le '
    u'añadió una pieza que la hacía gastar mucho menos. Con ese cambio, las máquinas de vapor '
    u'empezaron a mover fábricas enteras, y luego barcos, y luego trenes.',

    u'La ciencia que explica por qué una máquina de vapor puede aprovechar una parte del calor y no '
    u'toda —la <b>termodinámica</b>— llegó después. Sadi Carnot publicó su libro en 1824, y el resto '
    u'se fue formulando a lo largo de aquel siglo. O sea: medio siglo largo de máquinas funcionando '
    u'antes de la teoría.',

    u'Y llegó <b>porque</b> las máquinas existían. Lo que empujó a esos científicos fue una pregunta '
    u'muy práctica: por qué se desperdicia tanto carbón y cuánto se podría aprovechar como máximo. '
    u'La tecnología no solo usa a la ciencia; a veces la obliga a nacer.',

    ('h', u'Todo empieza por una necesidad'),

    u'Nadie inventa por inventar. Detrás de cada objeto que has usado hoy hay alguien que tenía un '
    u'problema: tengo frío, no llego, no puedo cortar esto, se me olvida. Primero está la '
    u'<b>necesidad</b>; el objeto viene después.',

    u'Y luego el bucle, que es siempre el mismo: se busca una solución con lo que se sabe y con lo '
    u'que hay, se fabrica, se prueba, y si funciona se mejora y se enseña a otros. Si no funciona, '
    u'se cambia. Ese bucle es igual para una piedra tallada y para un cohete, y es exactamente lo '
    u'que vas a hacer tú en cada proyecto de este curso.',

    u'Fíjate en «con lo que hay», porque manda más de lo que parece. Las casas del norte de Europa '
    u'se hicieron de madera y las del sur de piedra y barro. No fue una elección de estilo: era lo '
    u'que había cerca. Poder <b>elegir</b> el material es cosa moderna, y hace falta transporte '
    u'barato para poder hacerlo.',

    u'Hay un cuarto paso del que casi nadie habla, y es el que más te va a hacer pensar: toda '
    u'tecnología importante <b>cambia la sociedad</b>, y al cambiarla crea problemas que antes no '
    u'existían.',

    u'La agricultura es el caso de manual. Trajo el excedente —guardar comida para después—, y con '
    u'él la especialización, la propiedad, las jerarquías y la escritura, que nació para llevar las '
    u'cuentas de las cosechas y no para escribir poemas. Y trajo también el hambre cuando venía mal '
    u'año y la guerra por la tierra, que antes no se peleaba.',

    u'Por eso conviene no decir que una tecnología es buena o mala en sí misma. Lo que sí se puede '
    u'decir, y hay que decirlo, es que <b>nunca es neutral en sus consecuencias</b>: siempre '
    u'favorece a unos más que a otros y siempre abre un problema que nadie había previsto.',

    ('h', u'Y ahora, números'),

    u'La asignatura se llama Tecnología <b>y Digitalización</b>, así que hay que aclarar la segunda '
    u'mitad. Y lo primero es quitarse de encima el error más extendido: digitalizar <b>no</b> '
    u'significa «usar ordenadores».',

    u'Digitalizar es convertir información en <b>números</b>, para que una máquina pueda guardarla, '
    u'copiarla, enviarla y transformarla. El ordenador es una consecuencia de eso, no su definición.',

    u'La diferencia se ve mejor con música. Un vinilo guarda la canción como un <b>surco</b>, una '
    u'forma física. Cada vez que copias un surco, la aguja añade un poco de ruido y se come un poco '
    u'de agudos. Poco, pero cada vez. Una copia de una copia de una copia ya no suena igual.',

    u'Un archivo guarda esa misma canción como una <b>lista de números</b>. Y copiar un 7 da un 7, '
    u'siempre. La copia número mil es idéntica a la primera, no cuesta prácticamente nada y se puede '
    u'mandar a la otra punta del mundo. Ahí está toda la diferencia, y de ahí sale casi todo lo '
    u'demás.',

    u'Que esto no va de ordenadores se demuestra con una fecha. En 1844 se abrió la primera línea '
    u'telegráfica pública entre Washington y Baltimore, y por ella iban las letras convertidas en '
    u'dos únicos símbolos: punto y raya. Un siglo antes del primer ordenador, alguien ya había '
    u'convertido el lenguaje en señales contables.',

    u'Eso es lo que tienes delante este curso. Dos millones y medio de años de gente resolviendo '
    u'problemas con lo que tenía a mano, y una manera nueva de guardar lo que sabemos que hace que '
    u'copiar no cueste nada. A partir del tema 1 dejas de leerlo y empiezas a hacerlo: analizar un '
    u'objeto, dibujarlo, construirlo y comprobar si cumple lo que prometía.',
]

PREGUNTAS = [
    u'Según la lectura, ¿qué cambió exactamente hace 2,6 millones de años? Fíjate en que la '
    u'respuesta no es «apareció la piedra tallada».',
    u'¿Por qué dice el párrafo 2 que lo asombroso no es la piedra, sino que la misma forma de '
    u'golpear aparezca en sitios muy separados? ¿Qué demuestra eso?',
    u'Escribe en una tabla de tres filas a qué pregunta responde la técnica, a qué responde la '
    u'ciencia y a qué responde la tecnología. Una línea por cada una, con tus palabras.',
    u'La lectura dice que la técnica tiene dos límites. Explícalos los dos, y pon un ejemplo tuyo '
    u'de algo que sepas hacer sin saber por qué funciona.',
    u'¿Qué pasó en Beauvais en 1284 y por qué se reconstruyó «por si acaso»? ¿Qué le faltaba a '
    u'quien lo levantó?',
    u'La ciencia se publica y la técnica se guarda. Explica por qué eso no es una manía de cada '
    u'una, sino que tiene que ver con para qué sirve cada una.',
    u'Cuenta el caso de Watt y la termodinámica con las fechas de la lectura, y di qué demuestra '
    u'sobre el orden entre ciencia y tecnología.',
    u'Coge un objeto cualquiera de tu casa y recorre con él los cuatro pasos del bucle: qué '
    u'necesidad resuelve, con qué se resolvió, cómo se probó y qué problema nuevo ha traído.',
    u'«Ninguna tecnología es neutral en sus consecuencias.» Explica la frase con la agricultura, y '
    u'después inténtalo con el móvil.',
    u'Un amigo te dice que digitalizar es pasar las cosas al ordenador. Corrígele en cuatro o cinco '
    u'líneas, usando el vinilo y el telégrafo de 1844.',
]


if __name__ == '__main__':
    n = sum(1 for p in P if not isinstance(p, tuple))
    if n < 30:
        sys.exit(u'Tienen que ser 30 parrafos numerados como minimo y hay %d' % n)
    if len(PREGUNTAS) != 10:
        sys.exit(u'Tienen que ser 10 preguntas y hay %d' % len(PREGUNTAS))

    destino = os.path.join(RAIZ, '2eso', 'TyD', 'tema0')
    os.makedirs(destino, exist_ok=True)
    ruta = os.path.join(destino, 'lectura-tema0.pdf')
    lectura.genera(dict(
        titulo=u'Las tres preguntas',
        subtitulo=u'Cómo se hace, por qué ocurre y cómo lo resuelvo: tres preguntas parecidas que '
                  u'costó dos millones y medio de años separar',
        entradilla=u'Casi nada de lo que has tocado hoy existe en la naturaleza. Alguien lo pensó, '
                   u'alguien aprendió a fabricarlo y alguien averiguó por qué funciona. Esas tres '
                   u'cosas no son la misma, y confundirlas es el error más repetido de esta '
                   u'asignatura.',
        parrafos=P, preguntas=PREGUNTAS,
        curso=u'2.º de ESO · Tecnología y Digitalización',
        tema=u'Tema 0 · ¿Qué es la tecnología?'), ruta)
    print(u'%s  ·  %d párrafos numerados, %d preguntas, %d bytes'
          % (ruta, n, len(PREGUNTAS), os.path.getsize(ruta)))
