# -*- coding: utf-8 -*-
u"""Sesiones 5 a 8 de la unidad 5 de 4.o: la SEGUNDA MITAD.

La primera mitad (c5_build.py) ensena la tecnica con ejemplos que van rotando,
porque cuando se escribio el proyecto del curso no estaba decidido. Ya lo esta
(PROYECTOS.md, bloque DECIDIDO del 18-sep-2026): el curso se vertebra con el
RIEGO AUTOMATICO y cada grupo elige entre riego (A), aviso de aula mal
ventilada (B) y lampara de estudio (C). Asi que estas cuatro sesiones aterrizan
ahi, y terminan en algo que se ensena y se defiende.

  S5  Del esquema al montaje. Un esquema es una LISTA DE NUDOS; una placa de
      pruebas ya une cosas por dentro. Escena: los nudos se calculan con
      union-find sobre los agujeros y se comparan con los del esquema.
  S6  El programa que decide, pegado al montaje: el signo del if lo manda el
      divisor, el pin es una entrada antes de que exista tu programa, y la
      medida es ratiometrica. Escena: los seis primeros segundos.
  S7  Electrovalvulas y secuencias. La pieza que es electrica por un lado y
      neumatica por el otro, y una secuencia que salta por final de carrera en
      vez de por tiempo. Escena: A+ B+ A- B- con su diagrama espacio-fase.
  S8  El automatismo completo: la cadena entera, el presupuesto de corriente,
      el cuadro de bornes y la puesta en marcha. Escena: los siete eslabones
      con su numero. Y el test de la unidad entera, con identificador PROPIO
      (c5b), que el de la S4 es c5 y comparten los id del HTML.

Fronteras acordadas con las unidades de al lado (encargo del 18-sep-2026):
esta unidad es EL CIRCUITO Y EL AIRE, como se monta y como se manda. La
logica de control -histeresis, proporcional, el lazo, calibrar la sonda,
el protocolo de prueba y la defensa del proyecto- es de la unidad 4, y aqui
se usa ya decidida. La programacion como materia, los datos y el IoT son de
la unidad 6. El impacto ambiental se mide, pero su tratamiento es de la 8.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unidad_base import ficha, pregunta
from test_auto import test
from c5b_escenas import ESCENA_PLACA, ESCENA_ARRANQUE
from c5b_escenas2 import ESCENA_SECUENCIA, ESCENA_CADENA

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PENDIENTES = []


def foto(fichero, alt, pie, autor, licencia, pagina, alta=False):
    if not os.path.exists(os.path.join(RAIZ, 'img', fichero)):
        PENDIENTES.append(u'FALTA LA FOTO img/' + fichero)
        return u''
    return u'''      <figure class="foto%s">
        <img src="../../../img/%s" loading="lazy" alt="%s">
        <figcaption>%s
          <span class="credito">%s &middot; %s &middot;
            <a href="%s" target="_blank" rel="noopener">Wikimedia Commons</a></span>
        </figcaption>
      </figure>
''' % (u' alta' if alta else u'', fichero, alt, pie, autor, licencia, pagina)


# Titulo y canal comprobados uno a uno con la API oEmbed de YouTube el
# 18-sep-2026. La API dice QUIEN lo firma y COMO se llama; no dice si el video
# es bueno. NADIE DEL PROYECTO LOS HA VISTO ENTEROS. De los titulos se han
# quitado los emojis decorativos; el texto es el que devuelve la API.
VIDEOS = {
    's5': dict(vid='OvlutalHXoM',
               titulo=u'Como funciona una protoboard &middot; Electronica basica',
               canal=u'Ivan Espinoza',
               nota=u'Las grapas de cinco y los railes, vistos por dentro.'),
    's6': dict(vid='pvetokUpfzQ',
               titulo=u'Arduino desde cero en Espa&ntilde;ol &middot; Cap&iacute;tulo 85 &middot; '
                      u'Pull-up y Pull-down &iquest;cu&aacute;ndo y por qu&eacute; usar?',
               canal=u'Bitwise Ar',
               nota=u'El mismo problema del pin al aire, con el pulsador en vez de con la base '
                    u'del transistor.'),
    's7': dict(vid='H3_xq9FLT1s',
               titulo=u'Secuencia 2: A+ B+ A&minus; B&minus; [M&eacute;todo Paso a Paso]',
               canal=u'Jose Luis Sarmiento',
               nota=u'La misma secuencia de esta sesi&oacute;n, resuelta con el m&eacute;todo '
                    u'paso a paso.'),
    's8': dict(vid='9SKD_p9sFcI',
               titulo=u'Arduino desde cero en Espa&ntilde;ol &middot; Cap&iacute;tulo 50 &middot; '
                      u'Alimentaci&oacute;n para proyectos: bater&iacute;as, fuentes, ATX PC',
               canal=u'Bitwise Ar',
               nota=u'De d&oacute;nde sacar la corriente que pide el automatismo entero.'),
}


def video(clave):
    v = VIDEOS[clave]
    return u'''      <div class="video" id="video-c5b-%s" data-vid="%s">
        <button type="button" class="video-play" aria-label="Reproducir el v&iacute;deo: %s">
          <span class="video-tri" aria-hidden="true"></span>
          <span class="video-txt">
            <b>%s</b>
            <span>%s</span>
          </span>
        </button>
        <p class="video-nota">%s <b>Nadie del proyecto lo ha visto entero:</b> est&aacute;n
          comprobados el t&iacute;tulo y el canal, no el contenido. El v&iacute;deo no se carga
          hasta que lo pulsas, y se reproduce sin cookies de seguimiento. Si la red del centro
          bloquea YouTube, <a href="https://www.youtube.com/watch?v=%s" target="_blank"
          rel="noopener">&aacute;brelo en otra pesta&ntilde;a</a>. Es obra de su autor y no forma
          parte del material publicado bajo la licencia de esta p&aacute;gina.</p>
      </div>
''' % (clave, v['vid'], v['titulo'], v['titulo'], v['canal'], v['nota'], v['vid'])


CODE = (u'style="font-family:var(--f-m);font-size:12.5px;background:var(--surface-2);'
        u'padding:10px;border-radius:2px;overflow:auto;line-height:1.6"')

GRIS = u'style="color:var(--ink-soft)"'


def tabla(filas, cab=None):
    """Tabla sencilla, con el mismo estilo en linea que usan las otras unidades."""
    td = u'style="padding:5px 7px;border-bottom:1px solid var(--line)"'
    td2 = u'style="padding:5px 7px"'
    s = u'<table style="width:100%;border-collapse:collapse;font-size:14.5px;margin:8px 0">'
    if cab:
        s += u'<tr>' + u''.join(u'<td %s><b>%s</b></td>' % (td, c) for c in cab) + u'</tr>'
    for f in filas:
        s += u'<tr>' + u''.join(u'<td %s>%s</td>' % (td2, c) for c in f) + u'</tr>'
    return s + u'</table>'


# ==========================================================================
# SESION 5 - Del esquema al montaje
# ==========================================================================
S5_RETO = u'''
      <div class="aviso">
        <span class="n-tag">A partir de aqu&iacute; esto va en serio</span>
        Hasta la sesi&oacute;n 4, el proyecto era un ejemplo y los ejemplos iban rotando. Ya no:
        <b>el curso se vertebra con el riego autom&aacute;tico</b>, y cada grupo elige una de tres
        versiones del mismo problema &mdash; <b>A</b> regar la planta del aula, <b>B</b> avisar de
        que el aula est&aacute; cargada, <b>C</b> una l&aacute;mpara que se ajusta sola. Las tres
        son <b>sensor, decisi&oacute;n, actuador</b>, y las cuatro piezas de las sesiones 1 a 4
        valen para las tres. Lo que viene ahora se monta <b>encima de vuestra mesa</b>.
      </div>
      <p>El circuito ya lo ten&eacute;is dibujado: el <b>divisor</b> de la sesi&oacute;n 1 para
         enterarse, y el <b>transistor</b> de la sesi&oacute;n 2 para mover. En Tinkercad funciona:
         mueves el deslizador del sensor y la bomba arranca.</p>
      <p>Lo mont&aacute;is en la placa de pruebas, exactamente igual, y pasa una de estas tres:</p>
      <div class="aviso">
        <span class="n-tag">Las tres que m&aacute;s se repiten</span>
        <ul>
          <li>El monitor serie da <b>1023 siempre</b>, tapes el sensor o no.</li>
          <li>La bomba <b>no se mueve</b>, y el programa es el mismo que funcionaba.</li>
          <li>La bomba se mueve, pero <b>muy despacio</b>, como si le faltara fuerza.</li>
        </ul>
      </div>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un minuto antes de seguir</span>
        <p>El esquema es el mismo. Los componentes son los mismos. El programa es el mismo.
           &iquest;Qu&eacute; hay en la placa de pruebas que <b>no est&aacute; en el esquema</b>?</p>
      </div>
      <p>Hay dos cosas, y las dos son la misma en el fondo.</p>
      <p>La primera: un esquema dice <b>qu&eacute; est&aacute; unido con qu&eacute;</b>, y no dice
         <b>d&oacute;nde va cada cosa</b>. Puedes dibujar el mismo circuito de cien maneras
         distintas y todas son el mismo circuito. En la placa, en cambio, cada componente
         est&aacute; <b>en un sitio</b>, y el sitio decide con qui&eacute;n queda unido.</p>
      <p>La segunda: la placa de pruebas <b>ya une cosas por dentro</b>, sin preguntarte. Y une
         justo las que hacen falta&hellip; si pones los componentes donde toca. Si no, une
         otras.</p>
'''

S5_TEORIA = u'''
      <h3>Un esquema es una lista de nudos</h3>
      <p>Esta es la idea que hay que llevarse, y sirve para toda la vida: cuando un electr&oacute;nico
         mira un esquema <b>no ve dibujos, ve nudos</b>.</p>
      <div class="copiar">
        <h4>Nudo</h4>
        <p><b>Nudo</b> (o <i>nodo</i>, o en ingl&eacute;s <i>net</i>): todo lo que est&aacute; unido
           por cable, sin ning&uacute;n componente en medio. Dentro de un nudo, <b>toda la
           tensi&oacute;n es la misma</b>: no importa la longitud del cable ni la forma del
           dibujo.</p>
        <p>Un esquema, por complicado que parezca, se puede escribir como una <b>lista</b>: un nudo
           por l&iacute;nea y, en cada l&iacute;nea, qu&eacute; patillas caen ah&iacute;. Eso es la
           <b>lista de conexiones</b>, y es lo &uacute;nico que el circuito sabe de s&iacute;
           mismo.</p>
        <h4>La lista del circuito de este proyecto</h4>
        ''' + tabla([
    [u'<b>1</b>', u'+5 V', u'Arduino 5 V &middot; R fija (una patilla)'],
    [u'<b>2</b>', u'nudo del sensor', u'R fija (la otra) &middot; sensor (una patilla) &middot; '
                                      u'Arduino A0'],
    [u'<b>3</b>', u'masa', u'Arduino GND &middot; sensor (la otra) &middot; emisor &middot; '
                           u'&minus; de la pila'],
    [u'<b>4</b>', u'salida D9', u'Arduino D9 &middot; Rb (una patilla)'],
    [u'<b>5</b>', u'base', u'Rb (la otra) &middot; base del transistor'],
    [u'<b>6</b>', u'colector', u'colector &middot; actuador (una patilla) &middot; '
                               u'&aacute;nodo del diodo'],
    [u'<b>7</b>', u'+ de la pila', u'+ de la pila &middot; actuador (la otra) &middot; '
                                   u'c&aacute;todo del diodo'],
], [u'N&ordm;', u'Nudo', u'Qu&eacute; cae en &eacute;l']) + u'''
        <p><b>Siete nudos.</b> Ni uno m&aacute;s. Si tu montaje tiene siete nudos con esas mismas
           patillas dentro, <b>es este circuito</b>, lo hayas colocado como lo hayas colocado. Si
           tiene seis, has unido dos que no deb&iacute;an; si tiene ocho, has dejado uno partido en
           dos.</p>
        <p>F&iacute;jate en el nudo <b>3</b>: la masa del Arduino y el <b>menos de la pila</b>
           est&aacute;n en el <b>mismo</b> nudo. No es un detalle de dibujo: es una l&iacute;nea de
           la lista, y si falta, falta un nudo.</p>
      </div>

      <h3>Lo que la placa de pruebas une por dentro</h3>
      <p>Y ahora la otra mitad. Una placa de pruebas no es un tablero con agujeros: es un
         <b>montaje de grapas met&aacute;licas</b> escondidas debajo.</p>
''' + foto(
    'c5b-protoboard.jpg',
    u'La parte de atr&aacute;s de una placa de pruebas sin su adhesivo, con las tiras '
    u'met&aacute;licas a la vista: dos bancos de tiras cortas separados por un hueco central y '
    u'cuatro tiras largas en los bordes; una de las grapas est&aacute; sacada y puesta al lado',
    u'Una placa de pruebas <b>por detr&aacute;s</b>, con el adhesivo quitado. Cuenta lo que se ve: '
    u'en el centro, dos bancos de <b>tiras cortas</b>, y cada tira corta es <b>una columna de '
    u'cinco agujeros</b>. En los bordes, <b>tiras largas</b> que recorren la placa entera: son los '
    u'<b>railes</b> de alimentaci&oacute;n. Y en medio de los dos bancos, un hueco: ese hueco es el '
    u'<b>canal central</b>, y no une nada, por eso los integrados se montan a caballo. Abajo a la '
    u'derecha est&aacute; una grapa sacada: se ven sus <b>cinco pinzas</b>, una por agujero. Eso es '
    u'todo lo que hay dentro de una placa de pruebas.',
    u'Zeroping', u'CC BY 4.0',
    u'https://commons.wikimedia.org/wiki/File:Metal_contacts_within_a_breadboard.jpg') + u'''
      <div class="copiar">
        <h4>Las tres reglas de una placa de pruebas</h4>
        <ol>
          <li><b>Los cinco agujeros de una columna</b>, dentro de un banco, son <b>un nudo</b>.
              Est&aacute;n unidos por una grapa, siempre, los uses o no.</li>
          <li><b>Cada rail</b> de los bordes es <b>un nudo entero</b> de lado a lado. (En algunas
              placas el rail viene <b>partido por la mitad</b>: m&iacute;ralo antes de fiarte.)</li>
          <li><b>El canal central no une nada.</b> La columna 7 de arriba y la columna 7 de abajo
              son <b>dos nudos distintos</b>. Para unirlos hace falta un puente.</li>
        </ol>
        <h4>Y de ah&iacute; salen los cinco fallos de siempre</h4>
        <ul>
          <li><b>Las dos patillas de un componente en la misma columna.</b> La grapa lo
              cortocircuita: el componente est&aacute; puesto y <b>no est&aacute; en el
              circuito</b>.</li>
          <li><b>Un puente con los dos extremos en la misma mitad.</b> No une nada. Parece que
              cruza el canal y no lo cruza.</li>
          <li><b>El transistor girado.</b> Las tres patillas caben igual de bien al derecho que
              al rev&eacute;s, y la placa no protesta.</li>
          <li><b>El diodo del rev&eacute;s.</b> Tampoco protesta, y este s&iacute; hace da&ntilde;o.</li>
          <li><b>Las dos masas sin unir.</b> Es el nudo 3 partido en dos, y es el m&aacute;s
              dif&iacute;cil de ver, porque en el dibujo son dos s&iacute;mbolos de masa iguales.</li>
        </ul>
      </div>
      <p>Aqu&iacute; est&aacute; el circuito montado. Los <b>nudos de la escena no est&aacute;n
         escritos</b>: se calculan cada vez juntando lo que la placa une por dentro y lo que unen
         los puentes, y luego se comparan con la lista del recuadro de arriba. Prueba los seis
         montajes y mira <b>qu&eacute; l&iacute;nea de la lista se cae</b> en cada uno.</p>
''' + ESCENA_PLACA + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>De los seis, el que m&aacute;s tiempo hace perder es el del <b>transistor girado</b>, y
           por una raz&oacute;n concreta: <b>no rompe nada y no apaga nada</b>. El motor se mueve,
           as&iacute; que parece que el circuito est&aacute; bien y que el problema tiene que estar
           en el programa. Se puede pasar una tarde entera mirando c&oacute;digo.</p>
        <p>Lo que lo caza en diez segundos es el pol&iacute;metro: <b>el emisor tiene que estar a
           0 V</b>. Si marca tres voltios y pico, el emisor no est&aacute; en masa, y si el emisor
           no est&aacute; en masa es que no es el emisor.</p>
      </div>

      <h3>El pol&iacute;metro, y en qu&eacute; orden se mide</h3>
      <p>Buscar un fallo tocando cables al azar puede durar una hora. Con un orden dura cinco
         minutos, y el orden es siempre el mismo: <b>desde la fuente hacia la carga</b>, porque
         cada punto depende del anterior.</p>
''' + foto(
    'c5b-polimetro.jpg',
    u'Dos puntas de pol&iacute;metro, roja y negra, clavadas en agujeros libres de una placa de '
    u'pruebas, en las mismas filas que las patillas de una resistencia y un LED, con una placa '
    u'Arduino a la izquierda',
    u'As&iacute; se mide en una placa de pruebas: <b>las puntas van clavadas en agujeros libres de '
    u'la misma fila</b> que la patilla que quieres medir, no sujetas en el aire con la mano. Como '
    u'los cinco agujeros de la columna son el mismo nudo, da igual en cu&aacute;l de los cinco '
    u'pinches: mides lo mismo, y adem&aacute;s tienes las dos manos libres. F&iacute;jate tambi&eacute;n '
    u'en los <b>n&uacute;meros y las letras</b> impresos en la placa: las columnas van numeradas y '
    u'las filas llevan letra, y eso es lo que te deja escribir en la libreta <b>d&oacute;nde</b> has '
    u'puesto cada cosa. (La placa de la izquierda no es un Uno: por los pines numerados hasta el 33 '
    u'es una <b>Mega</b>.)',
    u'Zeroping', u'CC BY 4.0',
    u'https://commons.wikimedia.org/wiki/File:Multimeter_probes_on_breadboard.jpg') + u'''
      <div class="copiar">
        <h4>Buscar un fallo con el pol&iacute;metro, por orden</h4>
        <p>Selector en <b>tensi&oacute;n continua</b>, y la <b>punta negra siempre en la masa</b>
           (el rail de masa). No se mueve de ah&iacute; en toda la b&uacute;squeda: si mueves las
           dos puntas, no sabes qu&eacute; est&aacute;s midiendo.</p>
        ''' + tabla([
    [u'1', u'el rail de 5 V', u'<b>5 V</b>', u'si no, no llega la alimentaci&oacute;n'],
    [u'2', u'el nudo del sensor', u'entre <b>1 y 4,5 V</b>, y <b>se mueve</b> al tapar o mojar '
                                  u'el sensor',
     u'si est&aacute; clavado en 5 o en 0, el divisor est&aacute; roto'],
    [u'3', u'el pin D9', u'<b>0 o 5 V</b> seg&uacute;n lo que mande el programa',
     u'si no cambia, el programa no est&aacute; decidiendo'],
    [u'4', u'la base', u'<b>1,6 V</b> con un Darlington, 0,7 con un BC547',
     u'si marca 5 V, falta la Rb o la base est&aacute; al aire'],
    [u'5', u'el emisor', u'<b>0 V</b>, siempre',
     u'si no, o no est&aacute; en masa o el transistor est&aacute; girado'],
    [u'6', u'el colector', u'<b>1 V</b> si conduce, <b>la tensi&oacute;n de la pila</b> si no',
     u'la pila entera quiere decir que no pasa corriente'],
], [u'', u'D&oacute;nde', u'Qu&eacute; tiene que salir', u'Y si no sale']) + u'''
        <p><b>Y antes de nada, una medida que no es de tensi&oacute;n:</b> con el pol&iacute;metro
           en <b>continuidad</b> (el s&iacute;mbolo del pitido), comprueba que la <b>masa del
           Arduino y el menos de la pila pitan</b>. Dos segundos, y es el fallo m&aacute;s
           tonto.</p>
      </div>
''' + video('s5') + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; por qu&eacute; esto no se queda as&iacute;</span>
        <p>Una placa de pruebas sirve para <b>probar</b>, y el nombre lo dice en los dos idiomas:
           en ingl&eacute;s se llama <i>breadboard</i>, tabla de cortar el pan, porque los primeros
           montajes de radio de los a&ntilde;os veinte se clavaban literalmente con chinchetas
           sobre una tabla de cocina.</p>
        <p>Lo que tiene de bueno es lo que tiene de malo: <b>los contactos son a presi&oacute;n</b>.
           Eso quiere decir que:</p>
        <ul>
          <li>Una grapa se <b>afloja</b> con el uso, y un contacto flojo da un fallo
              <b>intermitente</b>, que es el peor de todos.</li>
          <li>Cada grapa aguanta del orden de <b>1 amperio</b>, y una tira LED de medio metro pide
              0,8. Va justo.</li>
          <li>Las tiras met&aacute;licas, largas y paralelas, se comportan como
              <b>condensadores</b> peque&ntilde;os entre s&iacute;. A las se&ntilde;ales lentas de
              este curso no les importa; a una se&ntilde;al de radio, s&iacute;, y por eso nadie
              prueba una radio en una placa de pruebas.</li>
        </ul>
        <p>Por eso, cuando el montaje ya funciona, se pasa a <b>placa perforada soldada</b>. El
           circuito es el mismo; lo que cambia es que ya no depende de que nadie roce la mesa.</p>
      </div>
'''

S5_PRACTICA = ficha(
    u'Actividad 5 &middot; La lista de conexiones de vuestro proyecto',
    [u'CE4 &middot; 4.1', u'B.1', u'B.2'], u'Parejas &middot; 20 min &middot; placa de pruebas',
    u'''
          <h4>Primera parte &middot; escribir la lista (6 min)</h4>
          <p>Antes de tocar un cable, escribid en la libreta la <b>lista de nudos de vuestra
             variante</b> (A riego, B ventilaci&oacute;n o C l&aacute;mpara), con el mismo formato
             del recuadro: n&uacute;mero, nombre y qu&eacute; patillas caen dentro.</p>
          <p>Despu&eacute;s, al lado de cada nudo, escribid <b>en qu&eacute; fila y columna de la
             placa</b> lo vais a poner: <i>nudo 2 &rarr; columna 5 del banco de arriba</i>. Eso es
             pasar del esquema al montaje, y se hace <b>en el papel</b>.</p>
          <h4>Segunda parte &middot; montarlo y medirlo (9 min)</h4>
          <p>Montadlo tal cual lo hab&eacute;is escrito y, <b>antes de enchufar la pila del
             actuador</b>, recorred la tabla de las seis medidas. Copiadla en la libreta con una
             columna m&aacute;s: <b>lo que sale de verdad</b>.</p>
          <div class="nota">
            <span class="n-tag">Dos cosas antes de dar tensi&oacute;n</span>
            <b>Una</b>: continuidad entre la masa del Arduino y el menos de la pila. <b>Dos</b>:
            mirad el transistor y decid en voz alta cu&aacute;l es cada patilla, con la hoja de
            caracter&iacute;sticas delante. Un TIP120 en c&aacute;psula TO-220, con la parte
            met&aacute;lica hacia atr&aacute;s y las patillas hacia abajo, va <b>B, C, E de
            izquierda a derecha</b>; un BC547 en TO-92 <b>no</b>, y ah&iacute; es donde se
            equivoca todo el mundo.
          </div>
          <h4>Tercera parte &middot; el fallo del compa&ntilde;ero (5 min)</h4>
          <ol class="pasos">
            <li>Intercambiad la placa con otra pareja. <b>Sin que os miren</b>, meted <b>un</b>
                fallo de los cinco del recuadro. Uno solo.</li>
            <li>La otra pareja lo busca <b>con el pol&iacute;metro</b>, y va apuntando cada medida
                que hace, en orden, con su resultado.</li>
            <li>Gana quien lo encuentre con <b>menos medidas</b>, no quien lo encuentre antes.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>La lista de nudos de vuestra variante, completa y con la masa com&uacute;n dentro
                del nudo 3 <b>(3 puntos)</b>.</li>
            <li>El plan de colocaci&oacute;n escrito <b>antes</b> de montar <b>(2 puntos)</b>.</li>
            <li>La tabla de las seis medidas, rellena con lo medido <b>(3 puntos)</b>.</li>
            <li>La b&uacute;squeda del fallo, con las medidas anotadas en orden
                <b>(2 puntos)</b>.</li>
          </ul>
''')

S5_CIERRE = u'''
      <ol>
      ''' + pregunta(
    u'&iquest;Qu&eacute; es un nudo, y por qu&eacute; da igual c&oacute;mo est&eacute; dibujado '
    u'el esquema?',
    u'<p>Un <b>nudo</b> es todo lo que est&aacute; unido por cable sin ning&uacute;n componente en '
    u'medio, y dentro de un nudo la tensi&oacute;n es la misma en todas partes. Un esquema solo '
    u'dice <b>qu&eacute; patillas caen en qu&eacute; nudo</b>; la forma del dibujo no es '
    u'informaci&oacute;n.</p>') + pregunta(
    u'Pones las dos patillas de la sonda en la columna 5 del mismo banco. &iquest;Qu&eacute; mide '
    u'entonces <code>analogRead</code>?',
    u'<p><b>1023</b>, y no se mueve. La grapa de esa columna cortocircuita la sonda, as&iacute; que '
    u'el nudo del sensor se queda colgando de los 5 V a trav&eacute;s de la R fija, sin nada que '
    u'tire de &eacute;l hacia masa. El sensor est&aacute; puesto, pero <b>no est&aacute; en el '
    u'circuito</b>.</p>') + pregunta(
    u'El emisor marca 3,2 V en vez de 0. &iquest;Qu&eacute; ha pasado?',
    u'<p>O el emisor <b>no est&aacute; unido a masa</b>, o el transistor est&aacute; <b>girado</b> '
    u'y lo que crees que es el emisor es en realidad el colector. En ese caso el transistor sigue '
    u'conduciendo, pero como <b>seguidor</b>: el actuador recibe la mitad de la tensi&oacute;n y va '
    u'lento. No se quema nada, y por eso cuesta tanto encontrarlo.</p>') + pregunta(
    u'&iquest;Por qu&eacute; lo primero que se comprueba es la continuidad entre las dos masas?',
    u'<p>Porque es la l&iacute;nea de la lista que m&aacute;s se olvida y la que m&aacute;s '
    u'despista: en el esquema son <b>dos s&iacute;mbolos de masa id&eacute;nticos</b>, y parece '
    u'que se unen solos. Si no se unen, la corriente del actuador no tiene por d&oacute;nde volver '
    u'a su pila y <b>no pasa nada</b>, con todo lo dem&aacute;s bien.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        La placa ya est&aacute; bien montada y medida. Ahora le metes el programa&hellip; y al
        enchufarlo, <b>la bomba pega un golpe de un segundo antes de que el programa exista</b>. Y
        luego riega cuando la tierra est&aacute; mojada y no riega cuando est&aacute; seca. El
        programa no tiene ni un error. Lo que pasa es que <b>no sabe c&oacute;mo lo has
        montado</b>.
      </div>
'''


# ==========================================================================
# SESION 6 - El programa que decide
# ==========================================================================
S6_RETO = u'''
      <p>El montaje est&aacute; comprobado con el pol&iacute;metro, punto por punto. Sub&iacute;s el
         programa y pasan dos cosas raras seguidas.</p>
      <div class="aviso">
        <span class="n-tag">Las dos cosas raras</span>
        <ul>
          <li>Al enchufar la placa, <b>la bomba arranca sola</b> y se para al cabo de un segundo,
              antes de que el programa haya hecho nada.</li>
          <li>Con la tierra <b>seca</b> no riega. Mojas la tierra y <b>entonces</b> riega.
              Justo al rev&eacute;s.</li>
        </ul>
      </div>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un minuto antes de seguir</span>
        <p>El programa compila, se sube y no tiene un solo error de sintaxis. El circuito est&aacute;
           medido y bien. <b>&iquest;Qu&eacute; sabe la placa que el programa no sabe?</b> Escribe
           dos cosas.</p>
      </div>
      <p>Lo segundo es lo m&aacute;s f&aacute;cil de ver: el <code>if</code> lleva el <b>signo al
         rev&eacute;s</b>. Con el sensor <b>abajo</b> en el divisor, cuanta menos agua hay m&aacute;s
         resistencia tiene la sonda, y m&aacute;s alta sale la cuenta. <b>Seco = cuenta alta.</b> Si
         hubieras montado el sensor arriba, ser&iacute;a al rev&eacute;s. El programa no puede
         adivinarlo: lo decidiste t&uacute; al colocar las dos resistencias.</p>
      <p>Lo primero es m&aacute;s interesante, y es el verdadero tema de esta sesi&oacute;n: cuando
         enchufas la placa, <b>el programa todav&iacute;a no existe</b>. Pasa alrededor de
         <b>un segundo</b> entre que hay tensi&oacute;n y que tu <code>setup()</code> se ejecuta. Y
         durante ese segundo, <b>los pines no est&aacute;n donde t&uacute; crees</b>.</p>
'''

S6_TEORIA = u'''
      <h3>Lo que el programa tiene que saber del circuito</h3>
      <p>Un programa de control tiene dos partes que conviene no mezclar, y en este curso adem&aacute;s
         <b>las escribes en momentos distintos</b>:</p>
      <div class="copiar">
        <h4>Las dos mitades de un programa de control</h4>
        <ul>
          <li><b>La que decide.</b> Umbral, margen, dosis, tope de seguridad. Eso es
              <b>control</b>, y es de la unidad 4: ah&iacute; se decide <b>cu&aacute;nto</b> y
              <b>cu&aacute;ndo</b>.</li>
          <li><b>La que habla con la placa.</b> Qu&eacute; pin, qu&eacute; signo, c&oacute;mo se
              enciende, c&oacute;mo se apaga, y qu&eacute; pasa antes de que arranque nada. Eso es
              <b>esta</b> sesi&oacute;n.</li>
        </ul>
        <p>La manera limpia de separarlas es meter todo lo que sabe de la placa en <b>dos
           funciones</b>, y que el resto del programa no toque un pin jam&aacute;s:</p>
        <pre ''' + CODE + u'''>const int PIN_SONDA = A0;
const int PIN_BOMBA = 9;          <span ''' + GRIS + u'''>// NO el 13: ahora se ver&aacute; por qu&eacute;</span>
const int UMBRAL    = 700;        <span ''' + GRIS + u'''>// sale de calibrar la sonda (unidad 4)</span>

<span ''' + GRIS + u'''>// ---- lo &uacute;nico que sabe c&oacute;mo est&aacute; montada la placa ----</span>
int leeSensor() {
  long suma = 0;
  for (int i = 0; i &lt; 10; i++) suma += analogRead(PIN_SONDA);
  return suma / 10;
}

void acciona(bool encender) {
  digitalWrite(PIN_BOMBA, encender ? HIGH : LOW);
}

<span ''' + GRIS + u'''>// ---- lo que decide: esto es de la unidad 4 ----</span>
void loop() {
  int lectura = leeSensor();
  acciona(lectura &gt; UMBRAL);      <span ''' + GRIS + u'''>// sensor ABAJO: seco = cuenta alta</span>
}</pre>
        <p><b>Por qu&eacute; merece la pena:</b> el d&iacute;a que cambi&eacute;is el sensor de
           sitio, o pas&eacute;is del transistor a un rel&eacute; (que va al rev&eacute;s: muchos
           m&oacute;dulos se activan con <code>LOW</code>), <b>solo se toca
           <code>acciona()</code></b>. El resto del programa no se entera.</p>
      </div>
      <div class="copiar">
        <h4>El signo del <code>if</code>, para las tres variantes</h4>
        ''' + tabla([
    [u'<b>A</b> riego', u'sonda de suelo, abajo', u'seco &rarr; m&aacute;s &#8486; &rarr; '
                                                  u'cuenta <b>alta</b>',
     u'<code>lectura &gt; UMBRAL</code>'],
    [u'<b>B</b> ventilaci&oacute;n', u'NTC, abajo', u'calor &rarr; menos &#8486; &rarr; cuenta '
                                                   u'<b>baja</b>',
     u'<code>lectura &lt; UMBRAL</code>'],
    [u'<b>C</b> l&aacute;mpara', u'LDR, abajo', u'oscuro &rarr; m&aacute;s &#8486; &rarr; cuenta '
                                               u'<b>alta</b>',
     u'<code>lectura &gt; UMBRAL</code>'],
], [u'Variante', u'Sensor y d&oacute;nde va', u'Qu&eacute; pasa con la cuenta',
    u'La l&iacute;nea']) + u'''
        <p>Y si mont&aacute;is el sensor <b>arriba</b> en vez de abajo, <b>los tres signos se dan
           la vuelta</b>. No hay uno correcto: hay el que corresponde a vuestro montaje, y tiene
           que estar <b>escrito en la libreta al lado del esquema</b>.</p>
      </div>

      <h3>Lo que hace un pin antes de que exista tu programa</h3>
      <div class="copiar">
        <h4>Los tres inquilinos del primer segundo</h4>
        <ol>
          <li><b>Reset.</b> Llega la tensi&oacute;n, el micro se pone en marcha. Todos los pines
              quedan configurados como <b>ENTRADA</b>, que es como salen de f&aacute;brica. Una
              entrada <b>no manda</b>: deja el pin al aire.</li>
          <li><b>El gestor de arranque</b> (<i>bootloader</i>). Un programita que ya viene grabado
              y que se queda <b>alrededor de un segundo</b> escuchando por si le mandas un programa
              nuevo desde el ordenador. Ese segundo es suyo, no tuyo, y los pines <b>siguen en
              entrada</b>.</li>
          <li><b>Tu programa.</b> Primero <code>setup()</code>, y desde ah&iacute;
              <code>loop()</code> para siempre.</li>
        </ol>
        <p><b>El problema:</b> tu transistor tiene la base colgada de la Rb, y la Rb colgada de un
           pin que durante ese segundo <b>no est&aacute; mandando nada</b>. Una base al aire recoge
           lo que le llegue. No es seguro que el transistor dispare, pero <b>puede</b>, y con eso
           basta para no dejarlo as&iacute;.</p>
        <h4>Las dos l&iacute;neas de defensa</h4>
        <ul>
          <li><b>Hardware: una resistencia de 10 k&#8486; de la base a masa.</b> Mientras el pin
              est&aacute; al aire, esa resistencia sujeta la base en <b>0 V</b> y el transistor
              est&aacute; cortado con seguridad. Cuando el pin manda de verdad, los 5 V a
              trav&eacute;s de 1,5 k&#8486; ganan de calle: la de 10 k solo se lleva 0,16 mA. Cuesta
              dos c&eacute;ntimos, y en 4.&ordm; es <b>obligatoria</b> en cualquier salida que mueva
              algo.</li>
          <li><b>Software: apagar antes de configurar.</b> En <code>setup()</code>, y en este
              orden:
              <pre ''' + CODE + u'''>void setup() {
  digitalWrite(PIN_BOMBA, LOW);   <span ''' + GRIS + u'''>// primero, para que el pin nunca pase por HIGH</span>
  pinMode(PIN_BOMBA, OUTPUT);     <span ''' + GRIS + u'''>// y ahora ya manda, mandando un cero</span>
  Serial.begin(9600);
}</pre>
              <b>El orden importa.</b> Si pones <code>pinMode</code> primero, el pin pasa a salida
              con lo que hubiera guardado antes; hazlo al rev&eacute;s y el cero est&aacute; puesto
              <b>antes</b> de que el pin sepa mandar.</li>
        </ul>
        <h4>Y una cosa que nadie te cuenta: el pin 13</h4>
        <p>El pin <b>13</b> lleva soldado en la placa el <b>LED marcado L</b>&hellip; y el gestor de
           arranque lo hace <b>parpadear tres veces</b> cada vez que la placa se reinicia. Si
           pusiste ah&iacute; el actuador, tu bomba da <b>tres golpes</b> en cada arranque. No es un
           fallo de nadie: es un pin que <b>ya ten&iacute;a due&ntilde;o</b>.</p>
      </div>
      <p>La escena enciende la placa y simula los <b>seis primeros segundos</b>, de dos en dos
         milisegundos. Mira la banda roja: es la bomba.</p>
''' + ESCENA_ARRANQUE + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; la pescadilla que se muerde la cola</span>
        <p>Pon <b>una fuente para todo</b> y sube la resistencia interna. A partir de cierto punto
           pasa algo que parece imposible: el Arduino <b>se reinicia una y otra vez</b>, y el
           programa no llega a ejecutarse nunca.</p>
        <p>La cadena es esta, y se lee en la gr&aacute;fica de arriba: la bomba arranca &rarr; se
           lleva 250 mA &rarr; esa corriente cae en la resistencia interna de la fuente &rarr; la
           tensi&oacute;n que le llega al Arduino baja &rarr; el micro se reinicia &rarr; al
           reiniciarse suelta la bomba &rarr; la tensi&oacute;n sube &rarr; el micro arranca&hellip;
           y vuelta a empezar, varias veces por segundo.</p>
        <p>Lo que se ve desde fuera es &laquo;el programa se cuelga&raquo;. Y el programa
           est&aacute; perfecto: el problema es que <b>la bomba y el cerebro comparten la misma
           fuente</b>. Por eso, desde la sesi&oacute;n 2, el actuador va con <b>su propia
           pila</b>, y lo &uacute;nico que comparten es la <b>masa</b>.</p>
      </div>

      <h3>Por qu&eacute; la cuenta no cambia aunque la pila se gaste</h3>
      <p>Aqu&iacute; hay algo que sorprende y que conviene entender, porque ahorra trabajo.</p>
      <div class="copiar">
        <h4>La medida es <i>ratiom&eacute;trica</i></h4>
        <p>El divisor da: <b>V = V<sub>cc</sub> &middot; R<sub>s</sub> / (R<sub>f</sub> +
           R<sub>s</sub>)</b>. Y el conversor, por su parte, reparte <b>de 0 a V<sub>cc</sub></b>,
           porque su referencia es la misma alimentaci&oacute;n. As&iacute; que la cuenta es:</p>
        <p class="cuenta">cuenta = 1023 &middot; V / V<sub>cc</sub> =
           1023 &middot; R<sub>s</sub> / (R<sub>f</sub> + R<sub>s</sub>)</p>
        <p><b>V<sub>cc</sub> se ha ido de la f&oacute;rmula.</b> Si la alimentaci&oacute;n baja de
           5,0 a 4,5 V, la tensi&oacute;n del nudo baja tambi&eacute;n&hellip; y la cuenta
           <b>no se mueve</b>. Es una propiedad del montaje, no una casualidad: se llama
           <b>medida ratiom&eacute;trica</b> y es una de las razones por las que el divisor es el
           circuito de sensor m&aacute;s usado del mundo.</p>
        <h4>Y cu&aacute;ndo deja de valer</h4>
        <ul>
          <li>Si el sensor <b>da tensi&oacute;n propia</b> en vez de resistencia (un <b>LM35</b> da
              10 mV por grado, pase lo que pase con la alimentaci&oacute;n), la cuenta
              <b>s&iacute;</b> depende de V<sub>cc</sub>, y hay que usar una referencia estable.</li>
          <li>Si cambias la referencia del conversor a la interna de <b>1,1 V</b>
              (<code>analogReference(INTERNAL)</code>), tambi&eacute;n. Se gana precisi&oacute;n y
              se pierde la ratiometr&iacute;a: no se puede tener todo.</li>
        </ul>
      </div>
''' + foto(
    'c5b-die.jpg',
    u'Fotograf&iacute;a a 20 aumentos del interior de un microcontrolador ATmega328 sin su '
    u'c&aacute;psula: un cuadrado de silicio con estructuras en amarillo, azul y rosa, rodeado por '
    u'un anillo de cuadraditos de contacto con hilos finos soldados a ellos',
    u'El <b>ATmega328 sin la c&aacute;psula de pl&aacute;stico</b>, a veinte aumentos. Lo que se '
    u've de verdad y merece la pena mirar: alrededor del borde hay un anillo de <b>cuadraditos '
    u'met&aacute;licos</b>, y de cada uno sale un <b>hilo</b> negro y fin&iacute;simo hacia fuera. '
    u'Ah&iacute; acaba cada patilla: el pin <code>A0</code> en el que clavas el cable del divisor '
    u'es uno de esos hilos. Y las zonas <b>ordenadas y repetidas</b> &mdash;el rect&aacute;ngulo '
    u'regular de arriba&mdash; son memoria: la memoria siempre se reconoce porque es la misma '
    u'celda copiada un mill&oacute;n de veces. Lo que <b>no</b> se puede hacer es se&ntilde;alar '
    u'd&oacute;nde est&aacute; el conversor anal&oacute;gico-digital: para eso har&iacute;a falta el '
    u'plano del fabricante, y no se publica. Pero est&aacute; ah&iacute;, y no es una idea: es un '
    u'trozo de este silicio.',
    u'Markus Kammerstetter', u'CC BY 4.0',
    u'https://commons.wikimedia.org/wiki/File:Atmel_atmega328_mz_20x.jpg') + u'''
''' + video('s6') + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>La resistencia de 10 k&#8486; de la base a masa es la misma idea que la resistencia
           <i>pull-down</i> de un pulsador, que es lo que cuenta el v&iacute;deo. Cambia el sitio,
           no el problema: <b>un punto que no est&aacute; conectado a nada no tiene tensi&oacute;n
           definida</b>, y eso ya lo viste en la sesi&oacute;n 1 con la LDR al aire.</p>
        <p>Es la tercera vez que aparece la misma idea en esta unidad, y no es casualidad: en
           electr&oacute;nica, <b>&laquo;al aire&raquo; nunca quiere decir &laquo;a cero&raquo;</b>.
           Si quieres un cero, lo tienes que poner.</p>
      </div>
'''

S6_PRACTICA = ficha(
    u'Actividad 6 &middot; Las dos funciones que hablan con vuestra placa',
    [u'CE4 &middot; 4.1', u'B.2'], u'Parejas &middot; 20 min &middot; Tinkercad y placa', u'''
          <h4>Primera parte &middot; el signo, y de d&oacute;nde sale (5 min)</h4>
          <ol class="pasos">
            <li>Con el montaje encendido y el monitor serie abierto, anotad la cuenta en <b>dos
                situaciones extremas</b> de vuestra variante (tierra seca y tierra mojada; sensor
                tapado y sensor a la luz; a temperatura de aula y con la mano encima).</li>
            <li>Escribid la l&iacute;nea del <code>if</code> <b>deducida de esas dos cuentas</b>, no
                copiada de la tabla. Y al lado, en una frase: <i>en nuestro montaje el sensor va
                abajo, as&iacute; que&hellip;</i></li>
          </ol>
          <h4>Segunda parte &middot; las dos funciones (9 min)</h4>
          <p>Escribid <code>leeSensor()</code> y <code>acciona()</code> para vuestro proyecto, con
             su <code>setup()</code>. Tienen que llevar, y se comprueba una por una:</p>
          <ul>
            <li><code>digitalWrite(pin, LOW)</code> <b>antes</b> de <code>pinMode</code>;</li>
            <li>la media de 10 lecturas dentro de <code>leeSensor()</code>;</li>
            <li>el pin del actuador <b>distinto del 13</b>;</li>
            <li>un <code>Serial.print</code> que saque la lectura y lo que se ha mandado.</li>
          </ul>
          <p>Y el <code>loop()</code> con <b>una sola l&iacute;nea de decisi&oacute;n</b>, la que
             traig&aacute;is de la unidad 4. Si en el <code>loop()</code> aparece un
             <code>digitalWrite</code>, no hab&eacute;is separado las dos mitades.</p>
          <h4>Tercera parte &middot; dos medidas (6 min)</h4>
          <ol class="pasos">
            <li><b>El arranque.</b> Con la resistencia de 10 k&#8486; <b>quitada</b>, desenchufad y
                volved a enchufar mirando el actuador. Anotad qu&eacute; hace. Ponedla y repetid.
                Escribid las dos observaciones.</li>
            <li><b>La ratiometr&iacute;a.</b> Anotad la cuenta. Ahora alimentad el Arduino por el
                otro sitio (de USB a pila, o al rev&eacute;s), medid con el pol&iacute;metro
                <b>los 5 V de verdad</b> en el pin 5V y anotad la cuenta otra vez.
                &iquest;Cu&aacute;nto ha cambiado cada una?</li>
          </ol>
          <div class="nota">
            <span class="n-tag">Si no ten&eacute;is la placa a mano</span>
            Las dos funciones se pueden escribir y probar en <b>Tinkercad</b> con un
            potenci&oacute;metro en A0 y un LED en el 9. Lo que <b>no</b> se puede ver ah&iacute; es
            lo del arranque: Tinkercad no simula el gestor de arranque. Esa medida es de la placa de
            verdad, y por eso est&aacute; en esta actividad.
          </div>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>El signo del <code>if</code> <b>deducido de dos medidas</b> vuestras
                <b>(2 puntos)</b>.</li>
            <li>Las dos funciones, con el orden de <code>setup()</code> correcto
                <b>(4 puntos)</b>.</li>
            <li>El <code>loop()</code> sin tocar ning&uacute;n pin <b>(1 punto)</b>.</li>
            <li>Las dos medidas del final, anotadas con n&uacute;meros <b>(3 puntos)</b>.</li>
          </ul>
''')

S6_CIERRE = u'''
      <ol>
      ''' + pregunta(
    u'&iquest;Por qu&eacute; el mismo programa riega al rev&eacute;s en dos montajes distintos?',
    u'<p>Porque el <b>sentido</b> de la cuenta lo decide d&oacute;nde pusiste el sensor en el '
    u'divisor. Con el sensor <b>abajo</b>, m&aacute;s resistencia (m&aacute;s seco) es cuenta '
    u'<b>m&aacute;s alta</b>; con el sensor arriba, al rev&eacute;s. El programa no puede saberlo: '
    u'es informaci&oacute;n del montaje, y tiene que estar escrita.</p>') + pregunta(
    u'&iquest;Qu&eacute; pasa en el primer segundo despu&eacute;s de enchufar, y por qu&eacute; '
    u'importa?',
    u'<p>El micro hace reset y arranca el <b>gestor de arranque</b>, que se queda alrededor de un '
    u'segundo esperando un programa nuevo. Durante todo ese rato <b>los pines est&aacute;n en '
    u'entrada</b>, o sea al aire, y una base al aire puede disparar el transistor. Se arregla con '
    u'una <b>resistencia de 10 k&#8486; de la base a masa</b>.</p>') + pregunta(
    u'&iquest;Por qu&eacute; se escribe <code>digitalWrite(pin, LOW)</code> <b>antes</b> de '
    u'<code>pinMode(pin, OUTPUT)</code>?',
    u'<p>Para que el pin no pase por <code>HIGH</code> ni un microsegundo. Poniendo el cero '
    u'primero, en el momento en que el pin empieza a mandar ya est&aacute; mandando un cero. Al '
    u'rev&eacute;s, el pin pasa a salida con lo que hubiera guardado antes.</p>') + pregunta(
    u'La pila del Arduino se gasta y pasa de 5,0 a 4,6 V. &iquest;Cambia la cuenta del sensor?',
    u'<p><b>No.</b> El divisor da una tensi&oacute;n proporcional a V<sub>cc</sub>, y el conversor '
    u'mide tomando V<sub>cc</sub> como referencia: se cancela. La cuenta solo depende de '
    u'R<sub>s</sub>/(R<sub>f</sub>+R<sub>s</sub>). Eso se llama <b>medida ratiom&eacute;trica</b>. '
    u'Dejar&iacute;a de valer con un sensor que diera tensi&oacute;n propia, como un LM35.</p>'
    ) + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya sabes leer y ya sabes accionar. Pero si tu proyecto mueve algo que pesa, el actuador no
        es una bomba de 6 V: es una <b>electrov&aacute;lvula</b>, y su chapa pone <b>24 V y
        125 mA</b>. Adem&aacute;s tiene una man&iacute;a que no est&aacute; en la chapa: hay
        modelos que <b>no se mueven si no hay 2 bar de aire</b>, por mucha corriente que les
        metas. Y cuando hay m&aacute;s de un cilindro, aparece el problema de verdad: <b>en
        qu&eacute; orden</b>.
      </div>
'''


# ==========================================================================
# SESION 7 - Electrovalvulas y secuencias
# ==========================================================================
S7_RETO = u'''
      <p>En la sesi&oacute;n 4 aprendiste a mandar un cilindro con una v&aacute;lvula 5/2 accionada
         con el dedo. Ahora el que tiene que accionarla es el Arduino, as&iacute; que pides una
         <b>electrov&aacute;lvula</b>: la misma 5/2, pero con una <b>bobina</b> en vez de un
         pulsador.</p>
      <p>Llega, la conectas al pin como conectaste el LED el primer d&iacute;a&hellip; y no pasa
         nada. Antes de seguir, lee su chapa:</p>
''' + foto(
    'c5b-bobina.jpg',
    u'Primer plano de la bobina negra de una electrov&aacute;lvula neum&aacute;tica con los datos '
    u'grabados: DC24V, 3W, Amp. 125mA, Temp. rise 60 grados, 100 % ED, IP 65 y el marcado CE; a su '
    u'derecha, el conector transparente con una resistencia y componentes dentro',
    u'La <b>bobina</b> de una electrov&aacute;lvula neum&aacute;tica, en su m&aacute;quina. '
    u'L&eacute;ela entera, porque lo dice todo: <b>DC24V</b> (corriente continua, 24 voltios), '
    u'<b>125 mA</b>, <b>3 W</b> &mdash;haz la cuenta: 24 &times; 0,125 = 3, los tres datos '
    u'cuadran&mdash;, <b>100 % ED</b> (puede estar encendida el 100 % del tiempo sin quemarse), '
    u'<b>Temp. rise 60 &deg;C</b> (se calienta 60 grados por encima del ambiente: no se toca) y '
    u'<b>IP 65</b> (estanca al polvo y al agua a chorro). A la derecha, el <b>conector</b> '
    u'transparente, y dentro se le ve una resistencia y m&aacute;s piezas: ah&iacute; es donde la '
    u'industria mete el <b>LED indicador y la protecci&oacute;n de la bobina</b>, o sea el diodo de '
    u'la sesi&oacute;n 2, vendido ya dentro del enchufe.',
    u'Sarah Adrita', u'CC BY-SA 4.0',
    u'https://commons.wikimedia.org/wiki/File:Solenoid_coil_of_a_pneumatic_valve.jpg') + u'''
      <div class="reto-piensa">
        <span class="n-tag">Piensa un minuto antes de seguir</span>
        <p>Los tres n&uacute;meros de la chapa cuadran entre s&iacute;. Compara cada uno con lo que
           da un pin de Arduino y escribe <b>cu&aacute;ntos problemas</b> tienes, y de qu&eacute;
           tama&ntilde;o es cada uno.</p>
      </div>
      <p>Son dos, y ya sabes resolver los dos: la <b>tensi&oacute;n</b> (el pin da 5 V y la bobina
         pide 24) y la <b>corriente</b> (el pin da 20 mA y la bobina pide 125). La bobina necesita
         <b>su propia fuente de 24 V</b> y un <b>transistor</b> en medio. Y un <b>diodo</b>, porque
         una bobina es la carga inductiva m&aacute;s descarada que existe.</p>
      <p>Pero hay un tercer problema que <b>no est&aacute; en la chapa</b> y que descubre todo el
         mundo por las malas: hay electrov&aacute;lvulas que, con los 24 V puestos y la bobina
         caliente, <b>no se mueven</b>. Y no est&aacute;n rotas.</p>
'''

S7_TEORIA = u'''
      <h3>Lo f&aacute;cil primero: c&oacute;mo se manda la bobina</h3>
      <div class="copiar">
        <h4>La etapa de potencia de esta bobina, paso a paso</h4>
        <p>Los mismos cuatro pasos de la sesi&oacute;n 2, con los n&uacute;meros de la chapa:</p>
        <p class="cuenta">
          1) I<sub>C</sub> = <b>125 mA</b> (lo pone la chapa)<br>
          2) I<sub>B m&iacute;n</sub> = 125 / 100 = <b>1,25 mA</b> &nbsp;(BC547, &beta; por lo
             bajo)<br>
          3) I<sub>B dise&ntilde;o</sub> = 1,25 &times; 8 = <b>10 mA</b><br>
          4) Rb = (5 &minus; 0,7) / 0,010 = <b>430 &#8486;</b> &rarr; comercial <b>390 &#8486;</b><br>
          Comprobaci&oacute;n: 11 mA &lt; 20 mA del pin &nbsp;&#10003; &nbsp; y 125 mA &lt; 100 mA
          del BC547&hellip; <b>&#10007;</b>
        </p>
        <p>La &uacute;ltima l&iacute;nea es la que salva la placa: el <b>BC547 admite 100 mA</b> por
           el colector y aqu&iacute; hacen falta 125. No vale. Con un <b>BC337</b> (800 mA) o con el
           <b>TIP120</b> que ya ten&eacute;is, s&iacute;. <b>Hacer la comprobaci&oacute;n no es un
           adorno</b>: es lo que decide el componente.</p>
        <h4>Y las tres cosas que no se negocian</h4>
        <ul>
          <li><b>Fuente aparte de 24 V</b> para la bobina. Del Arduino no sale.</li>
          <li><b>Masa com&uacute;n</b> entre esa fuente y el Arduino. Es el nudo 3 de la
              sesi&oacute;n 5.</li>
          <li><b>Diodo de rueda libre</b> en paralelo con la bobina, la raya al positivo. Con
              100 mH y 125 mA cortando en 1 &micro;s, la punta sale de <b>12.500 V</b> en el papel;
              en la realidad no llega, porque <b>algo se rompe antes</b>. Si la bobina viene con el
              conector transparente de la foto, <b>mira dentro</b>: puede que ya lo lleve.</li>
        </ul>
      </div>

      <h3>Lo raro: la que no se mueve aunque le des corriente</h3>
      <div class="copiar">
        <h4>Directa o servopilotada</h4>
        <ul>
          <li><b>De acci&oacute;n directa.</b> La bobina tira del carrete de la v&aacute;lvula ella
              sola. Funciona <b>desde 0 bar</b>, pero la bobina tiene que ser grande, porque tiene
              que vencer toda la presi&oacute;n que empuja sobre el carrete. Se usan en
              v&aacute;lvulas peque&ntilde;as.</li>
          <li><b>Servopilotada</b> (la m&aacute;s com&uacute;n). La bobina solo abre un
              <b>conducto min&uacute;sculo</b>, y es <b>el propio aire de la red</b> el que empuja
              el carrete: es el <b>mando indirecto</b> de la sesi&oacute;n 4, metido dentro de la
              misma pieza. La bobina puede ser peque&ntilde;a y gastar 3 W.</li>
        </ul>
        <p><b>Y de ah&iacute; sale la sorpresa:</b> una servopilotada necesita una
           <b>presi&oacute;n m&iacute;nima de pilotaje</b> &mdash;t&iacute;picamente <b>2 bar</b>,
           y lo dice su cat&aacute;logo&mdash; para tener con qu&eacute; empujar el carrete. Por
           debajo de eso <b>no conmuta</b>, con los 24 V puestos y la bobina caliente.</p>
        <p>Es un fallo precioso de diagnosticar: el pol&iacute;metro dice que la bobina tiene sus
           24 V, la bobina se calienta, y la v&aacute;lvula no hace nada. <b>La pieza
           el&eacute;ctrica funciona y la neum&aacute;tica no, y las dos est&aacute;n dentro del
           mismo bloque.</b></p>
        <h4>Monoestable o biestable</h4>
        ''' + tabla([
    [u'<b>Monoestable</b>', u'una bobina y un <b>muelle</b>',
     u'vuelve sola a su posici&oacute;n de reposo',
     u'hay que mantenerla alimentada todo el rato'],
    [u'<b>Biestable</b>', u'<b>dos bobinas</b>, una a cada lado',
     u'<b>se queda</b> donde estaba',
     u'basta un impulso corto: gasta much&iacute;simo menos'],
], [u'', u'Qu&eacute; lleva', u'Al cortar la corriente', u'Lo que cuesta']) + u'''
        <p><b>C&oacute;mo se elige:</b> no por el gasto, por lo que pasa el d&iacute;a que se va la
           luz. Con <b>monoestables</b>, la m&aacute;quina se va sola a una posici&oacute;n conocida
           &mdash;y t&uacute; eliges cu&aacute;l al decidir qu&eacute; es el reposo&mdash;. Con
           <b>biestables</b>, se queda donde iba y <b>nadie sabe d&oacute;nde est&aacute;</b>: al
           volver la corriente, el programa tiene que <b>leer sus finales de carrera antes de mover
           nada</b>.</p>
      </div>

      <h3>Y ahora el problema de verdad: en qu&eacute; orden</h3>
      <p>Con un solo actuador no hay problema: se enciende y se apaga. Con dos ya hay
         <b>secuencia</b>, y la secuencia es donde se rompen las m&aacute;quinas.</p>
      <p>Imagina una prensa peque&ntilde;a: un cilindro <b>A</b> que sujeta la pieza (la mordaza) y
         un cilindro <b>B</b> que la marca (el punz&oacute;n). El orden es evidente: primero sujetar,
         luego marcar, luego soltar&hellip; no, espera: primero <b>subir</b> el punz&oacute;n y
         <b>luego</b> soltar. Ese detalle es la secuencia.</p>
      <div class="copiar">
        <h4>C&oacute;mo se escribe una secuencia</h4>
        <p>Con el nombre del cilindro y un signo: <b>+</b> es salir, <b>&minus;</b> es entrar. La de
           la prensa es:</p>
        <p class="cuenta">A+ &nbsp; B+ &nbsp; A&minus; &nbsp; B&minus;</p>
        <p>Cuatro pasos. Se lee: <i>sale A, sale B, entra A, entra B</i>. Es una notaci&oacute;n
           universal: cualquier t&eacute;cnico del mundo entiende esas cuatro parejas de
           caracteres.</p>
        <h4>Y c&oacute;mo se sabe cu&aacute;ndo pasar al paso siguiente</h4>
        <p>Hay dos maneras, y <b>una de las dos est&aacute; mal</b>:</p>
        <ul>
          <li><b>Por tiempo.</b> &laquo;Sale A, espero 0,2 s, sale B&raquo;. F&aacute;cil de
              programar y <b>da por hecho</b> que A ha llegado. El d&iacute;a que A vaya m&aacute;s
              despacio &mdash;m&aacute;s carga, menos presi&oacute;n, una junta gastada&mdash; B sale
              igual, porque el programa est&aacute; contando, no mirando.</li>
          <li><b>Por final de carrera.</b> &laquo;Sale A; <b>cuando a1 avise</b>, sale B&raquo;. La
              m&aacute;quina <b>no adivina: pregunta</b>. Si A tarda m&aacute;s, el ciclo se alarga
              y el orden <b>no se rompe</b>.</li>
        </ul>
      </div>
''' + foto(
    'c5b-finales.jpg',
    u'Tres finales de carrera azules con palanca de rodillo, atornillados sobre un ra&iacute;l de '
    u'acero en una instalaci&oacute;n industrial, junto a una placa met&aacute;lica perfilada que '
    u'los acciona al pasar',
    u'Tres <b>finales de carrera</b> montados en una m&aacute;quina de verdad. Mira lo que hay que '
    u'mirar: cada uno tiene una <b>palanca con un rodillo</b> en la punta, y enfrente hay una '
    u'<b>chapa perfilada</b> &mdash;se llama <b>leva</b>&mdash; que los va apretando al pasar. El '
    u'final de carrera <b>no detecta el cilindro</b>: detecta que <b>algo ha pasado por este punto '
    u'exacto</b>, y el punto lo fija la chapa. Por eso hay tres a distinta altura: tres puntos '
    u'distintos del recorrido. Y por eso el rodillo: si fuera un tope recto, la leva lo '
    u'arrancar&iacute;a en una semana.',
    u'Mixabest', u'CC BY-SA 3.0',
    u'https://commons.wikimedia.org/wiki/File:Limit_Switches.JPG') + u'''
      <div class="copiar">
        <h4>Los dos finales de carrera que ver&eacute;is</h4>
        <ul>
          <li><b>Mec&aacute;nico de palanca y rodillo</b>, como los de la foto. Es un interruptor:
              se lee con <code>digitalRead</code> y su resistencia de <i>pull-up</i>, exactamente
              como un pulsador. Barato, robusto y ruidoso (rebota unos milisegundos al cerrar).</li>
          <li><b>Magn&eacute;tico</b>, la cajita sujeta al <b>cuerpo</b> del cilindro con una brida.
              Dentro del &eacute;mbolo hay un im&aacute;n, y el sensor se entera <b>a trav&eacute;s
              de la pared de aluminio</b>. No toca nada, no se desgasta y se coloca deslizando la
              brida. Son las dos cajitas que se ven en la foto del cilindro de la sesi&oacute;n
              3.</li>
        </ul>
        <h4>La secuencia, escrita como m&aacute;quina de estados</h4>
        <pre ''' + CODE + u'''>int paso = 1;
unsigned long tPaso = 0;

void loop() {
  bool a0 = digitalRead(FDC_A0), a1 = digitalRead(FDC_A1);
  bool b0 = digitalRead(FDC_B0), b1 = digitalRead(FDC_B1);

  switch (paso) {
    case 1: valvula(A, FUERA);  if (a1) salta(2); break;   <span ''' + GRIS + u'''>// A+</span>
    case 2: valvula(B, FUERA);  if (b1) salta(3); break;   <span ''' + GRIS + u'''>// B+</span>
    case 3: valvula(A, DENTRO); if (a0) salta(4); break;   <span ''' + GRIS + u'''>// A-</span>
    case 4: valvula(B, DENTRO); if (b0) salta(1); break;   <span ''' + GRIS + u'''>// B-</span>
  }

  <span ''' + GRIS + u'''>// el vigilante: si un paso tarda demasiado, algo va mal</span>
  if (millis() - tPaso &gt; 1000) parada();   <span ''' + GRIS + u'''>// 5 veces el paso m&aacute;s largo</span>
}

void salta(int siguiente) { paso = siguiente; tPaso = millis(); }</pre>
        <p>Tres cosas de este c&oacute;digo, y las tres importan:</p>
        <ol>
          <li><b>Cada <code>case</code> tiene dos l&iacute;neas</b>: qu&eacute; se manda y con
              qu&eacute; se sale. Si te falta la segunda, el paso no acaba nunca.</li>
          <li><b>La orden se repite en cada vuelta.</b> No se manda una vez y se olvida: mientras
              est&eacute;s en el paso 1, A tiene la orden de salir. As&iacute; da igual si la
              v&aacute;lvula se perdi&oacute; el impulso.</li>
          <li><b>El vigilante de tiempo.</b> Esperar a un final de carrera para siempre es una
              m&aacute;quina parada sin que nadie sepa por qu&eacute;. Con el vigilante, en cuanto pasa
              un segundo sin acabar el paso, para y <b>avisa de en qu&eacute; paso se ha quedado</b>, que es la
              informaci&oacute;n que hace falta para arreglarlo. El n&uacute;mero no se elige a
              ojo: se pone <b>unas cinco veces lo que tarda el paso m&aacute;s largo</b>, para
              que no salte con un d&iacute;a malo y s&iacute; salte cuando algo se ha roto.</li>
        </ol>
      </div>
      <p>Aqu&iacute; est&aacute; la prensa. Prueba primero por <b>final de carrera</b> subiendo la
         carga del punz&oacute;n; despu&eacute;s cambia a <b>por tiempo</b> y mira el contador de
         choques. Y luego corta la corriente con cada tipo de v&aacute;lvula.</p>
''' + ESCENA_SECUENCIA + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; c&oacute;mo se hac&iacute;a esto sin programa</span>
        <p>Antes de los aut&oacute;matas, las secuencias se montaban <b>solo con tubos</b>, y hay un
           problema cl&aacute;sico que conviene conocer porque explica por qu&eacute; se
           invent&oacute; el aut&oacute;mata.</p>
        <p>Mira la secuencia A+ B+ A&minus; B&minus;. El final de carrera <b>a1</b> manda salir a B.
           Pero a1 sigue pisado mientras A est&aacute; fuera&hellip; y en el paso 3 hay que meter A,
           o sea mandar la se&ntilde;al contraria a la misma v&aacute;lvula. <b>Las dos
           se&ntilde;ales est&aacute;n presentes a la vez</b> y la v&aacute;lvula no sabe a
           cu&aacute;l hacer caso: se queda bloqueada. Se llama <b>solapamiento de
           se&ntilde;ales</b>, y resolverlo con tubos exige montar un <b>m&eacute;todo de
           cascada</b>, que parte el circuito en grupos y va quitando la presi&oacute;n a los grupos
           que no tocan. Es ingenioso y es un l&iacute;o.</p>
        <p>Con una m&aacute;quina de estados ese problema <b>desaparece</b>: la v&aacute;lvula no
           obedece al final de carrera, obedece al <b>paso</b>, y el paso solo hay uno. El
           <code>switch</code> de arriba <b>es</b> la cascada, hecha con una variable.</p>
        <p>A cambio aparece un problema nuevo: si el programa se cuelga, las v&aacute;lvulas se
           quedan como estaban. Un tubo no se cuelga. Por eso, en las partes de <b>seguridad</b> de
           una m&aacute;quina de verdad &mdash;la seta de emergencia, la puerta&mdash; se sigue
           usando l&oacute;gica de tubos o de contactos, a prop&oacute;sito, y no pasa por el
           programa.</p>
      </div>
      <div class="nota">
        <span class="n-tag">Y en vuestro proyecto, que no tiene dos cilindros</span>
        Cambia el n&uacute;mero de actuadores, no la idea. Vuestra secuencia tiene dos pasos
        &mdash;<i>abrir</i> y <i>esperar</i>&mdash; y vuestro &laquo;final de carrera&raquo; es
        <b>la sonda</b>: la pregunta <i>&iquest;ha llegado ya el agua?</i> es exactamente
        <i>&iquest;ha llegado ya el cilindro?</i>. Escribirlo con un <code>switch</code> de dos
        <code>case</code> os deja sitio para el tercero el d&iacute;a que a&ntilde;ad&aacute;is
        algo. Y el <b>vigilante de tiempo</b> vale igual: si despu&eacute;s de regar la humedad
        no sube en diez minutos, algo pasa y hay que decirlo.
      </div>
''' + video('s7')

S7_PRACTICA = ficha(
    u'Actividad 7 &middot; La electrov&aacute;lvula y la secuencia',
    [u'CE4 &middot; 4.1', u'B.3', u'B.4'], u'Parejas &middot; 20 min', u'''
          <h4>Primera parte &middot; la etapa de potencia (7 min)</h4>
          <p>Ten&eacute;is que mandar <b>dos</b> bobinas con un Arduino. Haced los cuatro pasos,
             escritos, para cada una:</p>
          <ul>
            <li>La de la foto: <b>24 V, 125 mA</b>.</li>
            <li>Una peque&ntilde;a de 12 V que consume <b>2 W</b>. (Primero sacad su corriente.)</li>
          </ul>
          <p>Para cada una: corriente, Ib m&iacute;nima, Ib de dise&ntilde;o, Rb calculada, Rb
             comercial, <b>las dos comprobaciones</b> (los 20 mA del pin y el m&aacute;ximo del
             transistor) y el transistor elegido con su raz&oacute;n. Y dibujad el circuito
             completo de una de las dos, con <b>la fuente, la masa com&uacute;n y el diodo</b>.</p>
          <h4>Segunda parte &middot; en la escena (6 min)</h4>
          <ol class="pasos">
            <li>Modo <b>final de carrera</b>. Anotad el tiempo de ciclo con la carga al 0 %, al
                40 % y al 80 %. &iquest;Se rompe el orden en alg&uacute;n caso?</li>
            <li>Modo <b>por tiempo</b>, con el paso ajustado para que funcione con carga 20 %.
                Ahora subid la carga a 60 % sin tocar nada m&aacute;s y anotad los choques.</li>
            <li>Volved a final de carrera y aflojad <b>b1</b>. &iquest;Qu&eacute; hace la
                m&aacute;quina? Escribid <b>por qu&eacute; pararse es mejor que seguir</b>, y
                qu&eacute; l&iacute;nea del programa avisa de d&oacute;nde se ha parado.</li>
          </ol>
          <h4>Tercera parte &middot; vuestra secuencia (7 min)</h4>
          <p>Escribid la secuencia de <b>vuestro</b> proyecto en dos formatos:</p>
          <ul>
            <li>La <b>tabla de pasos</b>: n&uacute;mero, qu&eacute; se manda, y <b>con qu&eacute;
                se sale de ese paso</b> (la condici&oacute;n, no el tiempo).</li>
            <li>El <code>switch</code> en Arduino, con su <b>vigilante de tiempo</b> y una
                l&iacute;nea que diga qu&eacute; pasa al dispararse.</li>
          </ul>
          <p>Y una frase: <b>si se va la luz a mitad de ciclo, &iquest;d&oacute;nde se queda
             vuestro proyecto, y es ese el sitio donde quer&eacute;is que se quede?</b></p>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Las dos etapas de potencia, con <b>las dos comprobaciones</b> hechas
                <b>(3 puntos)</b>.</li>
            <li>El circuito dibujado con fuente, masa com&uacute;n y diodo <b>(2 puntos)</b>.</li>
            <li>Las tres pruebas de la escena, con n&uacute;meros <b>(2 puntos)</b>.</li>
            <li>La tabla de pasos y el <code>switch</code> con vigilante <b>(2 puntos)</b>.</li>
            <li>La frase del corte de corriente, razonada <b>(1 punto)</b>.</li>
          </ul>
''')

S7_CIERRE = u'''
      <ol>
      ''' + pregunta(
    u'La chapa de una bobina pone 24 V, 125 mA y 3 W. &iquest;Sobra alg&uacute;n dato?',
    u'<p>S&iacute;: los tres no son independientes. <b>24 &times; 0,125 = 3 W</b>. El fabricante '
    u'los pone los tres por comodidad, y a ti te sirven para <b>comprobar que est&aacute;s leyendo '
    u'bien la chapa</b>: si no cuadran, o has le&iacute;do mal o esa chapa no es de esa '
    u'bobina.</p>') + pregunta(
    u'Una electrov&aacute;lvula tiene sus 24 V, la bobina se calienta y no conmuta. '
    u'&iquest;Qu&eacute; miras antes de cambiarla?',
    u'<p>La <b>presi&oacute;n</b>. Si es <b>servopilotada</b>, el que mueve el carrete no es el '
    u'im&aacute;n: es el aire. Sin la presi&oacute;n m&iacute;nima de pilotaje (t&iacute;picamente '
    u'<b>2 bar</b>) no conmuta por mucha corriente que le metas. La parte el&eacute;ctrica '
    u'est&aacute; bien; la que falla es la neum&aacute;tica.</p>') + pregunta(
    u'&iquest;Por qu&eacute; es peor saltar de paso por tiempo que por final de carrera?',
    u'<p>Porque por tiempo la m&aacute;quina <b>da por hecho</b> que el cilindro ha llegado. '
    u'Mientras nada cambie, funciona; en cuanto sube la carga, baja la presi&oacute;n o se gasta una '
    u'junta, el cilindro tarda m&aacute;s y <b>el programa no se entera</b>: manda el paso '
    u'siguiente igual. Por final de carrera, el ciclo se alarga pero <b>el orden se respeta</b>.</p>'
    ) + pregunta(
    u'Se va la luz a mitad de ciclo. &iquest;Qu&eacute; hace una 5/2 monoestable y qu&eacute; hace '
    u'una biestable?',
    u'<p>La <b>monoestable</b> vuelve sola a su reposo, porque la mueve un muelle: la m&aacute;quina '
    u'acaba en una posici&oacute;n <b>conocida</b>, la que t&uacute; elegiste como reposo. La '
    u'<b>biestable</b> se queda donde estaba, as&iacute; que al volver la luz nadie sabe d&oacute;nde '
    u'est&aacute; cada cilindro: el programa <b>tiene que leer los finales de carrera antes de mover '
    u'nada</b>.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya tienes las siete piezas: sensor, divisor, conversor, programa, transistor, actuador y
        aire. La &uacute;ltima sesi&oacute;n las junta y hace las dos preguntas que faltan.
        <b>&iquest;De d&oacute;nde sale la corriente</b> cuando todo funciona a la vez? Y la que
        de verdad separa un proyecto de un montaje: dentro de un mes, cuando algo falle,
        <b>&iquest;lo puede arreglar alguien que no seas t&uacute;?</b>
      </div>
'''


# ==========================================================================
# SESION 8 - El automatismo completo
# ==========================================================================
S8_RETO = u'''
      <p>El automatismo funciona. Lo hab&eacute;is visto: mueves el sensor y el actuador responde.
         Enhorabuena, porque hasta aqu&iacute; no llega todo el mundo.</p>
      <p>Y ahora hay que <b>entregarlo</b>. Que se quede puesto en el aula, funcionando solo, y que
         alguien que no sois vosotros lo pueda mirar cuando falle.</p>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un minuto antes de seguir</span>
        <p>Imagina que est&aacute;s al tel&eacute;fono y alguien tiene tu montaje delante.
           <b>Escribe tres cosas que no le podr&iacute;as explicar</b> sin decir &laquo;el cable
           ese&raquo; o &laquo;el de al lado del rojo&raquo;.</p>
      </div>
      <p>Salen siempre las mismas tres: <b>cu&aacute;l es cada cable</b>, <b>de d&oacute;nde sale la
         corriente</b> y <b>qu&eacute; hay que medir para saber si funciona</b>. Y las tres tienen
         arreglo, y el arreglo no es electr&oacute;nica: es <b>papel</b>.</p>
      <p>Pero antes de eso, una comprobaci&oacute;n. Las siete piezas funcionan una a una.
         &iquest;Funciona la <b>cadena</b>?</p>
'''

S8_TEORIA = u'''
      <h3>La cadena entera, de la magnitud al efecto</h3>
      <p>Todo lo que has montado en esta unidad es <b>una sola cadena</b>, y una cadena se rompe por
         donde quiera. Aqu&iacute; est&aacute;n las tres variantes del proyecto con el n&uacute;mero
         de cada eslab&oacute;n calculado. Mete cada aver&iacute;a y mira <b>d&oacute;nde</b> se
         pone roja la cadena y, sobre todo, <b>qu&eacute; se ve desde fuera</b>.</p>
''' + ESCENA_CADENA + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; las dos aver&iacute;as que no se ven</span>
        <p>De las seis, dos <b>no rompen nada y no dan error</b>, y por eso son las peores: el
           montaje sigue en pie, el pol&iacute;metro no protesta y el programa est&aacute;
           bien.</p>
        <p>La <b>R fija de 1 M&#8486;</b> deja el divisor <b>funcionando</b>: la f&oacute;rmula
           sigue valiendo, la tensi&oacute;n del nudo es exactamente la que dice la cuenta y nada
           da error. Lo que pasa es que esa resistencia es <b>veinte veces</b> mayor que el sensor,
           as&iacute; que se queda con casi toda la tensi&oacute;n y al sensor <b>no le deja
           sitio</b>: mueve el deslizador de punta a punta y mira la cuenta. No pasa de <b>58</b>
           en todo el recorrido. Con un umbral en 700, <b>el sistema no puede actuar nunca</b>, y
           el programa no tiene ni un fallo. Es la regla de la sesi&oacute;n 1 &mdash;la fija se
           parece al sensor&mdash; convertida en una aver&iacute;a.</p>
        <p>Y encima hay una segunda raz&oacute;n para no pasarse con la R fija, que ah&iacute; no
           se ve pero cuenta: el pin del conversor tiene una <b>corriente de fuga</b> que la hoja
           del ATmega328P acota en <b>1 &micro;A</b>, y esa corriente, atravesando la impedancia
           que el pin ve, <b>suma tensi&oacute;n de error</b>. Con 10 k&#8486; son 0,01 V, o sea
           dos cuentas: nada. Con medio meg&oacute;hmio ser&iacute;an <b>medio voltio</b>, o sea
           cien cuentas. Por eso el fabricante recomienda no pasar de <b>10 k&#8486;</b> de
           impedancia de fuente: no es una regla arbitraria, es esa cuenta.</p>
        <p>La <b>pila gastada</b> es todav&iacute;a m&aacute;s traicionera, porque <b>funciona</b>.
           Solo que el actuador recibe menos tensi&oacute;n, as&iacute; que riega menos, ventila
           menos o alumbra menos. Nada da error. Y como la medida del sensor es
           <b>ratiom&eacute;trica</b> (sesi&oacute;n 6), la cuenta ni se inmuta: el sistema no tiene
           manera de enterarse por ah&iacute;. Se caza <b>midiendo</b>, y por eso la puesta en
           marcha lleva un pol&iacute;metro.</p>
      </div>

      <h3>De d&oacute;nde sale la corriente: el presupuesto</h3>
      <p>Hasta ahora cada cosa ten&iacute;a su fuente porque s&iacute;. Un proyecto entregado
         necesita una cuenta, y es una cuenta de sumar.</p>
      <div class="copiar">
        <h4>El presupuesto de corriente, en cuatro columnas</h4>
        <p>Una fila por consumidor, y dos totales distintos que no hay que confundir:</p>
        ''' + tabla([
    [u'Arduino Uno', u'5 V', u'45 mA', u'100 %', u'45 mA'],
    [u'Sonda de suelo', u'5 V', u'0,5 mA', u'100 %', u'0,5 mA'],
    [u'Bomba', u'6 V', u'250 mA', u'0,4 %', u'1 mA'],
    [u'LED de aviso', u'5 V', u'10 mA', u'5 %', u'0,5 mA'],
    [u'<b>Total</b>', u'', u'<b>305 mA</b> (pico)', u'', u'<b>47 mA</b> (medio)'],
], [u'Qu&eacute;', u'A qu&eacute; tensi&oacute;n', u'Cu&aacute;nto pide',
    u'Cu&aacute;nto tiempo', u'Media']) + u'''
        <ul>
          <li>El <b>pico</b> manda en la <b>fuente</b>: tiene que poder dar 305 mA <b>a la vez</b>,
              y se pide con margen. <b>Regla: la fuente, al doble del pico.</b> Aqu&iacute;, una de
              <b>5 V y 1 A</b> va sobrada y cuesta lo mismo que una de 500 mA.</li>
          <li>La <b>media</b> manda en la <b>pila</b>, si va con pila: una de 2000 mAh a 47 mA de
              media dura 2000 / 47 &asymp; <b>42 horas y media</b>. Menos de dos d&iacute;as. Ah&iacute; se ve de
              un vistazo que <b>este proyecto no puede ir con pilas</b>, y eso hay que saberlo
              antes de comprarlas.</li>
        </ul>
        <h4>Y el cable, que tambi&eacute;n cuenta</h4>
        <p>Un cable no es un cable ideal: tiene resistencia, y la corriente que pasa por &eacute;l
           deja parte de la tensi&oacute;n por el camino.</p>
        <p class="cuenta">R = &rho; &middot; L / S &nbsp;&nbsp;&nbsp;
           &Delta;V = I &middot; R &middot; 2 &nbsp;&nbsp;<span style="font-size:12px">(ida y
           vuelta)</span></p>
        <p>Con cobre (&rho; = 0,0172 &#8486;&middot;mm&sup2;/m), <b>3 metros</b> de cable fino de
           <b>0,14 mm&sup2;</b> (el de los kits) y los <b>250 mA</b> de la bomba:</p>
        <p class="cuenta">
          R = 0,0172 &middot; 3 / 0,14 = <b>0,37 &#8486;</b><br>
          &Delta;V = 0,25 &middot; 0,37 &middot; 2 = <b>0,18 V</b>
        </p>
        <p>Dos d&eacute;cimas de voltio de seis: un <b>3 %</b>. Se aguanta. Pero cambia la bomba
           por una <b>tira LED de 800 mA</b> y la misma cuenta da <b>0,59 V</b>: con una tira de
           12 V es un 5 %, todav&iacute;a poco; con una de 6 V ser&iacute;a el <b>10 %</b>, y
           alumbrar&iacute;a menos <b>por culpa del cable</b>. Se arregla con cable m&aacute;s
           gordo o, mejor, <b>acercando la fuente al actuador</b> y dejando largo el cable de
           se&ntilde;al, que casi no lleva corriente.</p>
      </div>

      <h3>Cu&aacute;l es cada cable: el cuadro de bornes</h3>
''' + foto(
    'c5b-bornes.jpg',
    u'Regleta de doce bornes de tornillo numerados del 1 al 12, atornillada a una caja '
    u'met&aacute;lica gris, con cables rojos, negros, marrones, blancos y verdes entrando por '
    u'arriba y por abajo, y una etiqueta impresa encima que pone BATTERIES 1-8',
    u'Un <b>cuadro de bornes</b> de verdad. Cada cable muere en <b>un tornillo numerado</b>, y los '
    u'n&uacute;meros est&aacute;n impresos en la propia regleta: del 1 al 12. As&iacute;, cuando '
    u'hay que decir d&oacute;nde va algo, se dice <b>&laquo;borne 7&raquo;</b> y no &laquo;el cable '
    u'negro de en medio&raquo;, que aqu&iacute; hay cinco. F&iacute;jate tambi&eacute;n en un '
    u'detalle honesto: el r&oacute;tulo de arriba dice <b>BATTERIES 1&ndash;8</b> y los bornes '
    u'llegan al 12. Un r&oacute;tulo <b>no basta</b>: hace falta la <b>lista de conexiones</b> que '
    u'diga qu&eacute; es cada borne, y esa lista va en el papel, no en la chapa.',
    u'tony_duell', u'CC BY 2.0',
    u'https://commons.wikimedia.org/wiki/File:Cabinet_Terminal_Block.jpg') + u'''
      <div class="copiar">
        <h4>Las cuatro reglas del conexionado</h4>
        <ol>
          <li><b>Cada cable, identificado en los dos extremos.</b> Con cinta y rotulador basta. Un
              cable etiquetado solo por un lado no sirve: el problema est&aacute; siempre en el otro
              extremo.</li>
          <li><b>Un color, un significado</b>, y el mismo en todo el montaje: <b>rojo</b> positivo,
              <b>negro</b> masa, y un tercer color para las se&ntilde;ales. No es est&eacute;tica:
              es lo que deja ver un error desde lejos.</li>
          <li><b>La lista de conexiones en papel</b>, la misma de la sesi&oacute;n 5, con una
              columna m&aacute;s: <b>a qu&eacute; borne va</b>. Esa hoja es la que hace que el
              montaje se pueda arreglar.</li>
          <li><b>Nada de cables tirantes.</b> Un cable que hace fuerza acaba soltando su tornillo o
              su soldadura. Se deja siempre un poco de holgura y se sujeta con una brida cerca del
              borne.</li>
        </ol>
        <h4>Y las cuatro protecciones, todas juntas por fin</h4>
        <ul>
          <li><b>El diodo de rueda libre</b> en cada carga con bobina (sesi&oacute;n 2).</li>
          <li><b>La masa com&uacute;n</b> entre las dos fuentes, y una sola (sesi&oacute;n 5).</li>
          <li><b>La resistencia de 10 k&#8486;</b> de la base a masa, para el arranque
              (sesi&oacute;n 6).</li>
          <li><b>Un fusible</b> en el positivo de la fuente de potencia, del <b>doble</b> de la
              corriente de trabajo: con 250 mA, uno de <b>500 mA</b>. Es la &uacute;nica pieza del
              montaje cuyo trabajo es <b>romperse</b>, y por eso es la &uacute;nica que hay que
              poder cambiar sin desmontar nada.</li>
        </ul>
        <p>Y una de colocaci&oacute;n que no cuesta nada: <b>el cable del sensor no va pegado al
           del actuador</b>. Por el del actuador pasan 250 mA que arrancan y paran; por el del
           sensor va una tensi&oacute;n que quieres medir con precisi&oacute;n de cinco
           mil&eacute;simas. Sep&aacute;ralos un par de cent&iacute;metros y, si tienen que
           cruzarse, que se crucen <b>en &aacute;ngulo recto</b>.</p>
      </div>

      <div class="copiar">
        <h4>La puesta en marcha el&eacute;ctrica, por orden</h4>
        <p>Nunca se enchufa todo a la vez. Se va sumando, y en cada paso se mide:</p>
        <ol>
          <li><b>Sin nada enchufado</b>: continuidad entre las dos masas, y <b>ninguna</b>
              continuidad entre positivo y masa (si pita, hay un cortocircuito y a&uacute;n no has
              roto nada).</li>
          <li><b>Solo el Arduino</b>: 5 V en su pin, y el programa corriendo con el monitor serie
              abierto. El actuador <b>desconectado</b>.</li>
          <li><b>Solo la fuente de potencia</b>, con el actuador a&uacute;n fuera: su tensi&oacute;n
              en el borne, y que <b>no se caliente nada</b>.</li>
          <li><b>El actuador, ahora s&iacute;</b>: se manda a mano desde el monitor serie y se mide
              la corriente <b>de verdad</b> con el pol&iacute;metro en serie. &iquest;Coincide con
              la de la etiqueta?</li>
          <li><b>Todo junto, una hora</b>, con el actuador trabajando fuera de donde hace
              da&ntilde;o (el tubo en un vaso, la tira apuntando a la mesa). Al acabar, se
              <b>tocan</b> el transistor, el diodo y la fuente: si queman, hay que mirarlo.</li>
        </ol>
      </div>
''' + video('s8') + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; lo que gasta el aparato que ahorra</span>
        <p>Mira el &uacute;ltimo cuadro de la escena. El Arduino gasta <b>0,22 W</b>, y los gasta
           <b>las 8760 horas del a&ntilde;o</b>, riegue o no riegue. Son unos <b>2 kWh al
           a&ntilde;o</b>: poco dinero, pero <b>no es cero</b>, y va en la defensa igual que el
           agua ahorrada.</p>
        <p>Es un caso peque&ntilde;o de algo grande: casi todo aparato que ahorra algo
           <b>consume por su cuenta</b>, y muchas veces lo consume <b>siempre</b> mientras que lo
           que ahorra lo ahorra <b>a ratos</b>. Hay proyectos en los que la cuenta no sale, y
           saberlo es parte del oficio.</p>
        <p>Comparar los dos platos de esa balanza &mdash;lo que ahorras frente a lo que cuesta
           fabricar, alimentar y tirar el aparato&mdash; es el trabajo de la <b>unidad 8</b>. Lo que
           te llevas de esta unidad es <b>el n&uacute;mero</b>: cu&aacute;nto gasta lo tuyo, medido,
           y no estimado.</p>
      </div>

      <div class="copiar">
        <h4>Lo que se ense&ntilde;a de la parte el&eacute;ctrica</h4>
        <p>Cuando defend&aacute;is el proyecto, la parte de esta unidad cabe en <b>tres cosas</b>, y
           las tres son papeles, no discursos:</p>
        <ol>
          <li><b>El esquema</b>, con los nudos numerados. Un folio.</li>
          <li><b>La lista de conexiones</b>, con la columna de bornes. Otro folio.</li>
          <li><b>Un n&uacute;mero medido</b> de los vuestros: la corriente real del actuador, o el
              consumo en reposo. Medido, con el pol&iacute;metro, no copiado de la etiqueta.</li>
        </ol>
        <p>Con esos tres papeles, cualquiera puede arreglar vuestro montaje. Sin ellos, solo
           pod&eacute;is vosotros, y solo mientras os acord&eacute;is.</p>
      </div>
'''

S8_TEST = test('c5b', u'Lo que tiene que haber quedado de la unidad entera', [
    dict(p=u'Un pin anal&oacute;gico mide tensi&oacute;n, no resistencia. &iquest;Qu&eacute; hace '
           u'el divisor?',
         op=[u'Amplifica la se&ntilde;al d&eacute;bil del sensor',
             u'Convierte el cambio de resistencia del sensor en un cambio de tensi&oacute;n que el '
             u'pin s&iacute; puede leer',
             u'Protege el pin de corrientes altas',
             u'Filtra el ruido el&eacute;ctrico del ambiente'],
         ok=1,
         por=u'Dos resistencias en serie entre 5 V y masa fijan una tensi&oacute;n en el punto de '
             u'en medio: V = 5 &middot; R2 / (R1 + R2). Si una de las dos es el sensor, esa '
             u'tensi&oacute;n se mueve con lo que el sensor mide. Ni amplifica ni protege ni '
             u'filtra: traduce.'),
    dict(p=u'&iquest;Por qu&eacute; hace falta un transistor entre el pin y la bomba?',
         op=[u'Porque el pin da 5 V y la bomba necesita 6',
             u'Porque el transistor convierte la corriente continua en alterna',
             u'Porque el pin da 20 mA y la bomba pide 250: la corriente no cuadra, aunque la '
             u'tensi&oacute;n s&iacute;',
             u'Porque sin &eacute;l el programa no puede apagar la bomba'],
         ok=2,
         por=u'El l&iacute;mite de un pin es de <b>corriente</b>: 20 mA recomendados, 40 como '
             u'm&aacute;ximo absoluto. Una bomba peque&ntilde;a pide 250 mA. El transistor deja '
             u'pasar esa corriente grande, que viene de otra fuente, mandado por una corriente '
             u'peque&ntilde;a por la base.'),
    dict(p=u'Un cilindro de 32 mm a 6 bar. &iquest;Cu&aacute;nto empuja al avanzar?',
         op=[u'96 N', u'193 N', u'482 N', u'1206 N'],
         ok=2,
         por=u'A = &pi; &middot; 32&sup2; / 4 = 804 mm&sup2;. Con 1 bar = 0,1 N/mm&sup2;: '
             u'F = 0,6 &middot; 804 = 482 N, unos 49 kg. El di&aacute;metro va al cuadrado, as&iacute; '
             u'que doblarlo multiplica la fuerza por cuatro.'),
    dict(p=u'&iquest;Por qu&eacute; una llave de paso no sirve para mandar un cilindro de doble '
           u'efecto?',
         op=[u'Porque el aire pasar&iacute;a demasiado despacio',
             u'Porque solo corta la entrada: el aire que ya hay dentro sigue empujando, y hace '
             u'falta abrir el escape del otro lado',
             u'Porque una llave de paso no aguanta 6 bar',
             u'Porque la norma ISO 1219 no tiene s&iacute;mbolo para una llave de paso'],
         ok=1,
         por=u'Un cilindro no se apaga: se vac&iacute;a. Hace falta una v&aacute;lvula '
             u'distribuidora que, al cambiar de posici&oacute;n, mande aire a una c&aacute;mara y '
             u'<b>abra el escape</b> de la otra. Por eso una 5/2 tiene dos escapes, uno por '
             u'salida de trabajo.'),
    dict(p=u'Montas el circuito en la placa de pruebas y metes las dos patillas de la sonda en la '
           u'misma columna de cinco agujeros. &iquest;Qu&eacute; lee <code>analogRead</code>?',
         op=[u'0, porque la sonda est&aacute; cortocircuitada a masa',
             u'Lo mismo que antes: la columna no une nada',
             u'1023 y clavado, porque la grapa cortocircuita la sonda y el nudo se queda colgando '
             u'de los 5 V',
             u'Un valor que baila, porque el pin queda al aire'],
         ok=2,
         por=u'Los cinco agujeros de una columna son un nudo. Con las dos patillas ah&iacute;, la '
             u'sonda queda puenteada y desaparece del circuito: el nudo del sensor solo tiene la '
             u'R fija hacia los 5 V y nada hacia masa, as&iacute; que se va a 5 V. La cuenta se '
             u'clava en 1023 y no se mueve.'),
    dict(p=u'El emisor de tu transistor marca 3,2 V con el pol&iacute;metro. &iquest;Qu&eacute; '
           u'es lo primero que sospechas?',
         op=[u'Que el transistor est&aacute; quemado',
             u'Que la pila est&aacute; gastada',
             u'Que el emisor no est&aacute; en masa: o falta el cable, o el transistor est&aacute; '
             u'girado y eso no es el emisor',
             u'Que la resistencia de base es demasiado grande'],
         ok=2,
         por=u'El emisor de este montaje va a masa, as&iacute; que tiene que marcar 0 V siempre. '
             u'Si marca otra cosa, o no est&aacute; conectado a masa o lo que has medido no es el '
             u'emisor. Con colector y emisor cambiados el transistor sigue conduciendo, como '
             u'seguidor, y el actuador recibe la mitad de tensi&oacute;n: va lento y no se quema '
             u'nada.'),
    dict(p=u'&iquest;Por qu&eacute; se pone una resistencia de 10 k&#8486; entre la base del '
           u'transistor y masa?',
         op=[u'Para limitar la corriente de base, como hace la Rb',
             u'Para que la base no quede al aire mientras el pin est&aacute; en entrada, que es '
             u'todo el primer segundo despu&eacute;s de encender',
             u'Para que el transistor sature antes',
             u'Para descargar el diodo de rueda libre'],
         ok=1,
         por=u'Al encender, todos los pines est&aacute;n en entrada y el gestor de arranque se '
             u'queda alrededor de un segundo. Durante ese rato la base queda al aire y el '
             u'transistor puede disparar. La resistencia a masa la sujeta en 0 V. Quien limita la '
             u'corriente de base es la Rb, que es otra.'),
    dict(p=u'La alimentaci&oacute;n del Arduino baja de 5,0 a 4,6 V. &iquest;Qu&eacute; le pasa a '
           u'la cuenta que devuelve el divisor?',
         op=[u'Baja en la misma proporci&oacute;n',
             u'Sube, porque el conversor tiene menos rango',
             u'No cambia: el conversor mide tomando la alimentaci&oacute;n como referencia, '
             u'as&iacute; que se cancela',
             u'Se vuelve err&aacute;tica'],
         ok=2,
         por=u'cuenta = 1023 &middot; V / Vcc, y V = Vcc &middot; Rs/(Rf+Rs): la Vcc se va de la '
             u'f&oacute;rmula. Se llama medida <b>ratiom&eacute;trica</b>. Dejar&iacute;a de valer '
             u'con un sensor que diera tensi&oacute;n propia (un LM35) o cambiando la referencia '
             u'del conversor.'),
    dict(p=u'Una electrov&aacute;lvula servopilotada tiene sus 24 V, la bobina se calienta y no '
           u'conmuta. &iquest;Qu&eacute; falta?',
         op=[u'Corriente: hay que subir la tensi&oacute;n',
             u'El diodo de rueda libre',
             u'Presi&oacute;n: una servopilotada necesita un m&iacute;nimo (t&iacute;picamente '
             u'2 bar) porque el carrete lo mueve el aire, no el im&aacute;n',
             u'Masa com&uacute;n con el Arduino'],
         ok=2,
         por=u'En una servopilotada la bobina solo abre un conducto peque&ntilde;o; el que empuja '
             u'el carrete es el propio aire de la red. Es mando indirecto metido dentro de la '
             u'pieza. Sin la presi&oacute;n m&iacute;nima no conmuta por mucha corriente que le '
             u'des. (Sin masa com&uacute;n la bobina no se calentar&iacute;a.)'),
    dict(p=u'Tu automatismo pide 305 mA de pico y 47 mA de media. &iquest;Qu&eacute; fuente pides?',
         op=[u'Una de 5 V y 50 mA: lo que manda es la media',
             u'Una de 5 V y 1 A: la fuente se elige por el <b>pico</b>, y con margen',
             u'Una de 5 V y 305 mA exactos, para no desperdiciar',
             u'Da igual: el Arduino regula lo que le sobre'],
         ok=1,
         por=u'La fuente tiene que poder dar lo que se pida <b>a la vez</b>, o sea el pico, y se '
             u'pide con margen (la regla c&oacute;moda es el doble). La media sirve para otra '
             u'cosa: para saber cu&aacute;nto durar&iacute;a una pila. A 47 mA, una de 2000 mAh '
             u'aguanta 42 horas, que es la manera de descubrir que este proyecto no puede ir con '
             u'pilas.'),
])

S8_PRACTICA = ficha(
    u'Actividad 8 &middot; El dosier el&eacute;ctrico del proyecto',
    [u'CE4 &middot; 4.1', u'B.1', u'B.2', u'B.3', u'B.4'], u'Grupos de 3 &middot; 15 min', u'''
          <h4>Primera parte &middot; el presupuesto (5 min)</h4>
          <p>Haced la tabla de las cuatro columnas con <b>vuestros</b> consumidores. El
             <b>porcentaje de tiempo</b> lo estim&aacute;is vosotros y lo justific&aacute;is en una
             l&iacute;nea (&laquo;la bomba riega 100 s al d&iacute;a = 0,12 %&raquo;).</p>
          <ol class="pasos">
            <li>Sacad el <b>pico</b> y la <b>media</b>, y decid la fuente, con su raz&oacute;n.</li>
            <li>Calculad cu&aacute;nto durar&iacute;a una pila de <b>2000 mAh</b> con vuestra
                media. &iquest;Aguanta unas vacaciones?</li>
            <li>Con la longitud real de vuestro cable al actuador, calculad la <b>ca&iacute;da de
                tensi&oacute;n</b>. Si pasa del 5 %, escribid qu&eacute; har&iacute;ais.</li>
          </ol>
          <h4>Segunda parte &middot; el dosier (6 min)</h4>
          <p>Tres papeles, y se entregan:</p>
          <ul>
            <li><b>El esquema</b> de vuestro circuito, con los <b>nudos numerados</b> y las cuatro
                protecciones dibujadas.</li>
            <li><b>La lista de conexiones</b>, con una columna <b>borne</b> y otra <b>color de
                cable</b>.</li>
            <li><b>La hoja de puesta en marcha</b>: los cinco pasos, con un hueco para el valor
                medido en cada uno.</li>
          </ul>
          <h4>Tercera parte &middot; medir de verdad (4 min)</h4>
          <p>Recorred la hoja de puesta en marcha con el montaje delante y rellenad los cinco
             valores. Dos de ellos van a la defensa:</p>
          <ul>
            <li>La <b>corriente real del actuador</b>, medida con el pol&iacute;metro en serie. Y
                al lado, la de la etiqueta. &iquest;Cu&aacute;nto se llevan, y por qu&eacute;?</li>
            <li>El <b>consumo en reposo</b> de todo el sistema. De ah&iacute; sacad los kWh al
                a&ntilde;o.</li>
          </ul>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>El presupuesto con pico, media y la fuente elegida y razonada <b>(3 puntos)</b>.</li>
            <li>La ca&iacute;da en el cable, calculada con vuestra longitud <b>(1 punto)</b>.</li>
            <li>El esquema con los nudos numerados y las cuatro protecciones <b>(3 puntos)</b>.</li>
            <li>La lista de conexiones con bornes y colores <b>(1 punto)</b>.</li>
            <li>Las dos medidas del final, con n&uacute;meros y comentadas <b>(2 puntos)</b>.</li>
          </ul>
''')

S8_CIERRE = u'''
      <ol>
      ''' + pregunta(
    u'&iquest;Para qu&eacute; sirve la columna &laquo;cu&aacute;nto tiempo&raquo; del presupuesto '
    u'de corriente?',
    u'<p>Para sacar la <b>media</b>, que es otra cosa que el pico. El <b>pico</b> decide la '
    u'<b>fuente</b> (tiene que poder darlo todo a la vez). La <b>media</b> decide <b>cu&aacute;nto '
    u'dura una pila</b> y cu&aacute;nta energ&iacute;a gasta al a&ntilde;o. Confundirlas lleva a '
    u'comprar una fuente que no arranca o unas pilas que duran dos d&iacute;as.</p>') + pregunta(
    u'Tu proyecto funciona, pero el actuador rinde menos de lo que deber&iacute;a y nada da error. '
    u'&iquest;Qu&eacute; dos cosas miras?',
    u'<p>La <b>tensi&oacute;n en bornes del actuador</b> mientras trabaja (puede estar bajando la '
    u'fuente o gast&aacute;ndose la pila) y la <b>ca&iacute;da en el cable</b> (con 800 mA y cable '
    u'fino y largo se pierde m&aacute;s de medio voltio). Las dos se miden con el pol&iacute;metro '
    u'<b>con el actuador en marcha</b>: en reposo no se ve nada.</p>') + pregunta(
    u'&iquest;Por qu&eacute; un fusible va en el positivo de la fuente de potencia y no en el del '
    u'Arduino?',
    u'<p>Porque es ah&iacute; donde hay corriente suficiente para hacer da&ntilde;o. Se pone del '
    u'<b>doble</b> de la corriente de trabajo, para que no salte con los arranques normales y '
    u's&iacute; con un cortocircuito. Y va donde se pueda cambiar sin desmontar nada: es la '
    u'&uacute;nica pieza cuyo trabajo es romperse.</p>') + pregunta(
    u'&iquest;Por qu&eacute; tres papeles valen m&aacute;s que una explicaci&oacute;n?',
    u'<p>Porque la explicaci&oacute;n se va con vosotros. El <b>esquema</b> dice qu&eacute; hay, la '
    u'<b>lista de conexiones</b> dice d&oacute;nde est&aacute; cada cable y la <b>hoja de puesta en '
    u'marcha</b> dice qu&eacute; ten&iacute;a que medir cada punto cuando funcionaba. Con eso, otra '
    u'persona lo arregla en marzo; sin eso, no lo arregla nadie, y en junio vosotros tampoco.</p>'
    ) + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Con esto se cierra la unidad</span>
        Empez&oacute; con una LDR colgando de un pin y n&uacute;meros que bailaban. Termina con un
        automatismo montado, medido, documentado y con la corriente contada. Por el camino han
        salido <b>siete piezas</b> &mdash;sensor, divisor, conversor, programa, transistor, aire y
        fuente&mdash; y una idea que se ha repetido tres veces y merece la pena llevarse:
        <b>en electr&oacute;nica, &laquo;al aire&raquo; nunca quiere decir &laquo;a cero&raquo;</b>.
        Si quieres un cero, lo tienes que poner t&uacute;.
      </div>
'''


# ==========================================================================
# el montaje de las cuatro sesiones
# ==========================================================================
MIN = [(u"10'", u'Reto'), (u"25'", u'Teor&iacute;a'),
       (u"20'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')]
MIN_TEST = [(u"10'", u'Reto'), (u"20'", u'Teor&iacute;a'),
            (u"15'", u'Pr&aacute;ctica'), (u"15'", u'Test y cierre')]


def sesiones(bloque):
    """Devuelve las cuatro sesiones montadas, para sumarlas a la lista de la unidad."""
    S5 = (bloque('00', u'Reto inicial &middot; 10 min', S5_RETO) +
          bloque('01', u'Teor&iacute;a &middot; 25 min', S5_TEORIA) +
          bloque('02', u'Pr&aacute;ctica &middot; 20 min', S5_PRACTICA) +
          bloque('03', u'Cierre &middot; 5 min', S5_CIERRE))
    S6 = (bloque('00', u'Reto inicial &middot; 10 min', S6_RETO) +
          bloque('01', u'Teor&iacute;a &middot; 25 min', S6_TEORIA) +
          bloque('02', u'Pr&aacute;ctica &middot; 20 min', S6_PRACTICA) +
          bloque('03', u'Cierre &middot; 5 min', S6_CIERRE))
    S7 = (bloque('00', u'Reto inicial &middot; 10 min', S7_RETO) +
          bloque('01', u'Teor&iacute;a &middot; 25 min', S7_TEORIA) +
          bloque('02', u'Pr&aacute;ctica &middot; 20 min', S7_PRACTICA) +
          bloque('03', u'Cierre &middot; 5 min', S7_CIERRE))
    S8 = (bloque('00', u'Reto inicial &middot; 10 min', S8_RETO) +
          bloque('01', u'Teor&iacute;a &middot; 20 min', S8_TEORIA) +
          bloque('02', u'Pr&aacute;ctica &middot; 15 min', S8_PRACTICA) +
          bloque('03', u'Test y cierre &middot; 15 min', S8_TEST + S8_CIERRE))

    return [
        dict(corto=u'Del esquema al montaje',
             titulo=u'En Tinkercad funcionaba',
             entradilla=u'Un esquema dice qu&eacute; est&aacute; unido con qu&eacute;. Una placa de '
                        u'pruebas ya une cosas por dentro, y no te pregunta.',
             minutado=MIN, chips=[u'CE4 &middot; 4.1', u'B.1', u'B.2'], cuerpo=S5),
        dict(corto=u'El programa que decide',
             titulo=u'El programa no sabe c&oacute;mo lo has montado',
             entradilla=u'Al enchufar, la bomba pega un golpe de un segundo antes de que el '
                        u'programa exista. Y luego riega al rev&eacute;s. No hay ni un error de '
                        u'sintaxis.',
             minutado=MIN, chips=[u'CE4 &middot; 4.1', u'B.2'], cuerpo=S6),
        dict(corto=u'Electrov&aacute;lvulas y secuencias',
             titulo=u'El&eacute;ctrica por un lado, neum&aacute;tica por el otro',
             entradilla=u'La chapa pide 24 V y 125 mA, y adem&aacute;s hay modelos que no se mueven '
                        u'sin 2 bar de aire. Y cuando hay dos cilindros, aparece el orden.',
             minutado=MIN, chips=[u'CE4 &middot; 4.1', u'B.3', u'B.4'], cuerpo=S7),
        dict(corto=u'El automatismo completo',
             titulo=u'Que lo pueda arreglar alguien que no eres t&uacute;',
             entradilla=u'Siete eslabones, una cadena. Y tres papeles, que son lo que separa un '
                        u'proyecto de un montaje que funcion&oacute; una tarde.',
             minutado=MIN_TEST,
             chips=[u'CE4 &middot; 4.1', u'B.1', u'B.2', u'B.3', u'B.4'], cuerpo=S8),
    ]
