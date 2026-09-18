# -*- coding: utf-8 -*-
"""4.o de ESO - Tecnologia - Unidad 2: Diseno y fabricacion, del material al producto.

CE2 (2.1, 2.2) / CE3 (3.1, 3.2) / CE5 (5.1). Saberes A.2, A.2.2, A.3, A.3.1, D.4.

La pregunta que abre la unidad: ya sabes que vas a construir y por que. Como se
pasa de un dibujo a una pieza que encaja de verdad con las demas?

Ocho sesiones. Aqui van escritas las CUATRO PRIMERAS; las otras cuatro quedan
marcadas como pendientes, con el titulo que se propone para cada una.

  S1  El dibujo que se puede fabricar: croquis, plano acotado y por que una
      pieza acotada en cadena acumula error.
  S2  Tolerancias y ajustes: por que dos piezas "de 8 mm" no encajan.
  S3  Union de piezas: desmontables y fijas, y que falla de verdad cuando una
      union se rompe.
  S4  Del plano a la pieza: las tecnicas del aula y que cambia en el diseno
      segun como se vaya a fabricar.

El proyecto del curso YA ESTA DECIDIDO (PROYECTOS.md, 18-sep-2026): el riego
automatico vertebra 4.o y los grupos eligen entre tres - A riego, B aviso de
aula mal ventilada, C lampara de estudio. La unidad esta escrita con los tres
y se reparten a proposito: la tapa de la S1 y de la S4 es la del aviso de
ventilacion (B), el eje de la S2 es el del deposito del riego (A) y la union
de la S3 es la del brazo de la lampara (C).

La placa de 4.o es Arduino, no micro:bit.
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unidad_base import pagina, bloque, ficha, pregunta
from c2_escenas import COTAS, AJUSTE
from c2_escenas2 import UNIONES, TALLER
from test_auto import test
import avatar_flat

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USA_AVATAR = [False]
PENDIENTES = []


# --------------------------------------------------------------------------
# Piezas comunes
# --------------------------------------------------------------------------
def foto(fichero, alt, pie, autor, licencia, pagina_commons):
    if not os.path.exists(os.path.join(RAIZ, 'img', fichero)):
        PENDIENTES.append(u'FALTA LA FOTO img/' + fichero)
        return u''
    return u'''      <figure class="foto">
        <img src="../../../img/%s" alt="%s" loading="lazy">
        <figcaption>%s
          <span class="credito">%s &middot; %s &middot;
            <a href="%s" target="_blank" rel="noopener">Wikimedia Commons</a></span>
        </figcaption>
      </figure>
''' % (fichero, alt, pie, autor, licencia, pagina_commons)


# Titulo y canal comprobados uno a uno con la API oEmbed de YouTube el
# 18-sep-2026. Lo que la API dice es QUIEN lo firma y COMO se llama; no dice
# si el video es bueno. NADIE DEL PROYECTO LOS HA VISTO ENTEROS: hay que verlos
# antes de ponerlos en clase.
VIDEOS = {
    's1': dict(vid='NC7AdFJDx4M',
               titulo=u'Acotaci&oacute;n de una pieza &middot; Tecnolog&iacute;a ESO',
               canal=u'Francisco Jose',
               nota=u'La misma pieza acotada de dos maneras distintas, con el l&aacute;piz encima '
                    u'del papel.'),
    's2': dict(vid='961O25IM1ZI',
               titulo=u'Tolerancia dimensional: tipos de ajustes, c&aacute;lculo y selecci&oacute;n',
               canal=u'Mat&iacute;as G. Ottini | Ingenier&iacute;a y Dise&ntilde;o',
               nota=u'Va m&aacute;s all&aacute; de lo que se pide aqu&iacute; &mdash;entra en la '
                    u'notaci&oacute;n ISO completa&mdash;, pero el porqu&eacute; de los tres tipos de '
                    u'ajuste est&aacute; muy bien contado.'),
    's3': dict(vid='vcpl2baqin4',
               titulo=u'&iquest;Cu&aacute;l es mejor? Bul&oacute;n, remache o soldadura',
               canal=u'Tecnica X',
               nota=u'La misma pregunta de esta sesi&oacute;n, con piezas de verdad y a escala de '
                    u'taller met&aacute;lico.'),
    's4': dict(vid='Tz168RtMZJU',
               titulo=u'Aumenta la resistencia de tus piezas impresas en 3D: &iquest;qu&eacute; '
                      u'orientaci&oacute;n es mejor?',
               canal=u'Control 3D',
               nota=u'El ejemplo m&aacute;s claro de que <b>el dise&ntilde;o depende de c&oacute;mo se '
                    u'fabrique</b>: la misma pieza, girada, aguanta otra cosa.'),
}


def video(clave):
    v = VIDEOS[clave]
    return u'''      <div class="video" id="video-c2-%s" data-vid="%s">
        <button type="button" class="video-play" aria-label="Reproducir el v&iacute;deo: %s">
          <span class="video-tri" aria-hidden="true"></span>
          <span class="video-txt">
            <b>%s</b>
            <span>%s</span>
          </span>
        </button>
        <p class="video-nota">%s <b>Nadie del proyecto lo ha visto entero:</b> est&aacute;n
          comprobados el t&iacute;tulo y el canal, no el contenido. El v&iacute;deo no se carga hasta
          que lo pulsas, y se reproduce sin cookies de seguimiento. Si la red del centro bloquea
          YouTube, <a href="https://www.youtube.com/watch?v=%s" target="_blank" rel="noopener">&aacute;brelo
          directamente aqu&iacute;</a>. Es obra de su autor y no forma parte del material publicado
          bajo la licencia de esta p&aacute;gina.</p>
      </div>
''' % (clave, v['vid'], v['titulo'], v['titulo'], v['canal'], v['nota'], v['vid'])


def narrador():
    """La voz de la unidad. Solo se monta si estan el mp3 y su envolvente."""
    env = os.path.join(RAIZ, '_env_c2-fabricacion.json')
    mp3 = os.path.join(RAIZ, 'audio', 'c2-fabricacion.mp3')
    if not (os.path.exists(env) and os.path.exists(mp3)):
        PENDIENTES.append(u'VOZ  audio/c2-fabricacion.mp3  ->  '
                          u'~/venv/bin/python generadores/voz.py generadores/guion_c2.txt c2-fabricacion')
        return u''
    USA_AVATAR[0] = True
    return avatar_flat.componente(
        'narr-c2', u'De qu&eacute; va esta unidad',
        u'Ya sabes qu&eacute; vas a construir. Ahora hay que hacerlo, y que encaje',
        '../../../audio/c2-fabricacion.mp3',
        json.load(io.open(env, encoding='utf-8')),
        u'Voz sintetizada sobre gui&oacute;n propio. La boca sigue el volumen real de la voz: se '
        u'mueve cuando habla y se para en los silencios.')


# ==========================================================================
# SESION 1 - El dibujo que se puede fabricar
# ==========================================================================
S1_RETO = narrador() + u'''
      <p>En la unidad 1 decidisteis qu&eacute; ibais a construir y por qu&eacute;. Ahora empieza la
         parte en la que se rompen los proyectos: <b>hacerlo</b>.</p>
      <p>Vamos con el grupo que ha elegido el <b>aviso de aula mal ventilada</b>. Han repartido el
         trabajo, que es lo l&oacute;gico: dos montan la placa con el sensor DHT11 y los tres LED, y
         otro fabrica la <b>tapa frontal</b>, que es la que se ve desde el aula. En la tapa hay que
         hacer <b>cuatro agujeros de 6 mm</b>: tres para que asomen los LED y uno para el pulsador de
         prueba. En la placa, esos cuatro componentes est&aacute;n soldados <b>cada 25 mm</b>.</p>
      <p>As&iacute; que le pasan un papel al que hace la tapa:</p>
      <div class="aviso">
        <span class="n-tag">El encargo, tal cual se lo dieron</span>
        <b>&laquo;Una tapa de 120 &times; 60, con cuatro agujeros de 6 mm cada 25 mm.&raquo;</b>
        Est&aacute; claro, no tiene ninguna ambig&uuml;edad y cualquiera lo entiende a la primera.
      </div>
      <p>El compa&ntilde;ero lo hace bien. Coge la regla, marca el primer agujero a 25 mm del borde.
         Desde ese, mide otros 25 y marca el segundo. Desde el segundo, otros 25. Y desde el tercero,
         otros 25. Cuatro agujeros, cuatro medidas, cada una impecable. Taladra.</p>
      <p>Llega el d&iacute;a del montaje: <b>los dos primeros LED entran y los dos &uacute;ltimos no</b>.</p>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento</span>
        <p>Nadie se ha equivocado m&aacute;s de <b>dos d&eacute;cimas de mil&iacute;metro</b> en
           ninguna medida: dos d&eacute;cimas es menos que el grosor de la raya del l&aacute;piz.
           &iquest;C&oacute;mo puede ser que el cuarto agujero est&eacute; casi un mil&iacute;metro
           fuera de sitio? &iquest;De qui&eacute;n es la culpa?</p>
      </div>
      <p>De nadie, y eso es lo incómodo. El fallo no est&aacute; en las manos: est&aacute; en
         <b>el papel</b>. Al decir &laquo;cada 25 mm&raquo; se pidió que cada agujero se midiera
         <b>desde el anterior</b>, y eso hace que el error de la primera medida siga ah&iacute; cuando
         se marca la cuarta. Los errores no se compensan: <b>se suman</b>.</p>
      <p>Cuatro medidas de 25 con dos d&eacute;cimas de error cada una pueden dejar el &uacute;ltimo
         agujero a <b>0,8 mm</b> de donde ten&iacute;a que estar. Y un LED de 5 mm por un agujero de 6
         solo tiene <b>medio mil&iacute;metro</b> de margen a cada lado.</p>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>En 2.&ordm; ya viste que describir una pieza con palabras no funciona: tres personas
           construyen tres mesas distintas. La conclusi&oacute;n de entonces fue &laquo;hay que
           dibujarlo&raquo;. Esta sesi&oacute;n a&ntilde;ade la mitad que faltaba: <b>no basta con
           dibujarlo bien, hay que acotarlo bien</b>. Un dibujo precioso con las cotas mal puestas
           produce piezas que no encajan, y el que fabrica no tiene forma de saberlo.</p>
      </div>
'''

S1_TEORIA = u'''
      <h3>Dos dibujos que no son lo mismo</h3>
      <div class="copiar">
        <h4>Croquis y plano</h4>
        <p><b>Croquis</b>: dibujo <b>a mano alzada</b>, sin escala, hecho para pensar y para hablar con
           los del grupo. Se hace deprisa, se tacha y se rehace. Puede llevar medidas, pero sus
           proporciones no valen: no se mide sobre un croquis.</p>
        <p><b>Plano</b> (o dibujo de fabricaci&oacute;n): dibujo <b>a escala</b>, con instrumentos o con
           un programa, hecho para que <b>otra persona fabrique la pieza sin preguntarte nada</b>. Es
           un documento: se archiva, se firma y se le pone fecha.</p>
        <p>La prueba para saber si tu plano est&aacute; terminado es siempre la misma: <b>&iquest;podr&iacute;a
           fabricarlo alguien que no ha estado en ninguna de vuestras reuniones?</b> Si para entenderlo
           hace falta que t&uacute; est&eacute;s al lado, no es un plano todav&iacute;a.</p>
      </div>
      <div class="copiar">
        <h4>Lo que lleva un plano para poder fabricarse</h4>
        <ul>
          <li>Las <b>vistas</b> necesarias, y solo esas. Una pieza plana con agujeros pasantes se
              resuelve con <b>una vista y el espesor apuntado</b>.</li>
          <li>Las <b>cotas</b>: los n&uacute;meros, en <b>mil&iacute;metros</b> y sin escribir la
              unidad.</li>
          <li>La <b>escala</b> (1:1, 1:2, 2:1&hellip;). Las cotas son <b>siempre la medida real</b>,
              aunque el dibujo est&eacute; reducido.</li>
          <li>El <b>material</b> y el <b>espesor</b>.</li>
          <li>El <b>cajet&iacute;n</b>, abajo a la derecha: qu&eacute; pieza es, qui&eacute;n la ha
              dibujado, cu&aacute;ndo y qu&eacute; versi&oacute;n es. Sin la versi&oacute;n,
              alguien fabricar&aacute; el plano viejo. Pasa siempre.</li>
        </ul>
      </div>

      <h3>Las reglas de acotaci&oacute;n, y por qu&eacute; existen</h3>
      <p>Las normas de acotaci&oacute;n (en Espa&ntilde;a, la UNE-EN ISO 129) parecen una lista de
         man&iacute;as. No lo son: cada regla est&aacute; ah&iacute; porque alguien fabricó mal una
         pieza por no seguirla.</p>
      <div class="copiar">
        <h4>Las que importan de verdad</h4>
        <ul>
          <li><b>Las cotas van fuera de la pieza</b>, sobre l&iacute;neas auxiliares finas que salen
              del contorno y <b>no lo tocan</b> (se dejan 1-2 mm). Dentro no se lee y se confunde con
              el dibujo.</li>
          <li><b>Cada medida, una sola vez.</b> Si la misma cota aparece en dos vistas y un d&iacute;a
              cambi&aacute;is una y se os olvida la otra, ten&eacute;is dos planos en el mismo papel.</li>
          <li><b>Ninguna cota de m&aacute;s.</b> Si pones 25 + 25 + 25 + 25 <b>y adem&aacute;s</b> el
              total de 100, est&aacute;s dando una orden que <b>no se puede cumplir</b>: las cuatro
              medidas reales nunca van a sumar 100 exactos. Es el error m&aacute;s frecuente, y el
              m&aacute;s da&ntilde;ino, porque parece que ayuda.</li>
          <li><b>Los agujeros se acotan por su centro</b> y por su <b>di&aacute;metro</b>, con el
              s&iacute;mbolo <b>&empty;</b> delante. Nunca por el borde del agujero: el borde no se
              puede medir con nada.</li>
          <li><b>Cotas que se puedan medir con lo que hay.</b> Si en el taller solo hay una regla
              apoyada en el canto de la pieza, acota <b>desde ese canto</b>. Una cota entre dos centros
              de agujero es preciosa en el papel y no se puede comprobar con una regla.</li>
          <li>Las cifras se escriben <b>encima de la l&iacute;nea de cota</b> y se leen desde abajo o
              desde la derecha: nunca del rev&eacute;s.</li>
        </ul>
      </div>

      <h3>Y ahora, la regla que da nombre a la sesi&oacute;n</h3>
      <div class="copiar">
        <h4>De d&oacute;nde se mide: tres maneras</h4>
        <p><b>Acotaci&oacute;n en cadena</b> (o en serie): cada cota arranca donde termin&oacute; la
           anterior. 25 &middot; 25 &middot; 25 &middot; 25. Es la que sale sola con una regla, y es la
           que <b>acumula error</b>.</p>
        <p><b>Acotaci&oacute;n desde una referencia</b> (en paralelo, o con l&iacute;nea de referencia
           com&uacute;n): todas las cotas se miden <b>desde la misma cara</b>. 25 &middot; 50 &middot;
           75 &middot; 100. Cada agujero solo carga con <b>su</b> error.</p>
        <p><b>Mixta</b>: la de verdad. Se acota desde una referencia lo que tiene que encajar con otra
           pieza, y en cadena lo que da igual que se mueva un poco.</p>
        <p><b>La referencia se elige, no sale sola.</b> Se elige la cara que de verdad manda: la que
           apoya, la que se atornilla, la que toca a la otra pieza.</p>
      </div>
      <p>Abajo est&aacute;n las dos tapas, fabricadas por el mismo operario, con <b>exactamente los
         mismos cuatro errores</b>. Lo &uacute;nico que cambia es desde d&oacute;nde se midi&oacute;.
         Pulsa &laquo;Otra pieza&raquo; varias veces antes de sacar conclusiones.</p>
''' + COTAS + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p><b>Cu&aacute;nto se acumula, con n&uacute;meros.</b> Si cada medida se puede equivocar como
           mucho <b>e</b>, y encadenas <b>n</b> cotas, el &uacute;ltimo punto puede estar a
           <b>n &middot; e</b> de su sitio. Con 4 cotas y e = 0,2 mm, eso es <b>0,8 mm</b>. Midiendo
           todo desde la misma cara, el peor caso se queda en <b>e</b> = 0,2 mm, y no crece aunque
           a&ntilde;adas veinte agujeros m&aacute;s.</p>
        <p>En la pr&aacute;ctica no suele darse el peor caso, porque unos errores tiran para arriba y
           otros para abajo. Lo t&iacute;pico es que en cadena la desviaci&oacute;n crezca con la
           <b>ra&iacute;z</b> del n&uacute;mero de cotas: &radic;n &middot; e. Con 4 cotas,
           &radic;4 = 2, o sea <b>el doble</b>. Mejor que ocho veces, pero sigue siendo peor que
           acotar desde el borde. Y sobre todo: <b>no lo controlas</b>. Una pieza te sale bien y la
           siguiente no.</p>
        <p>Conviene sacar la conclusi&oacute;n buena, que no es &laquo;la cadena es mala&raquo;. La
           cadena dice <b>&laquo;lo que me importa es la distancia entre estos dos&raquo;</b> y la
           referencia dice <b>&laquo;lo que me importa es d&oacute;nde est&aacute; cada uno respecto al
           borde&raquo;</b>. Acotar es <b>decir qu&eacute; es lo que no se puede mover</b>. Por eso no
           se puede acotar una pieza sin saber con qui&eacute;n va a encajar.</p>
      </div>

      <h3>De d&oacute;nde sale todo esto</h3>
      <p>La acotaci&oacute;n normalizada no naci&oacute; en una clase de dibujo: naci&oacute; en las
         f&aacute;bricas, cuando la pieza ya no la hac&iacute;a la misma persona que la hab&iacute;a
         pensado. Mientras el que dise&ntilde;a y el que lima son el mismo, un croquis basta. En cuanto
         el plano viaja &mdash;a otra nave, a otra ciudad, a otro pa&iacute;s&mdash;, todo lo que el
         plano no diga se convierte en una pieza mal hecha.</p>
''' + foto('c2-plano-1914.jpg',
           u'Plano de fabricaci&oacute;n de 1911 de la General Electric: dos vistas de un disco con '
           u'radios, dos secciones, un alzado seccionado y el cajet&iacute;n abajo a la derecha, todo '
           u'cubierto de cotas',
           u'Un plano de fabricaci&oacute;n de verdad: la <b>brida y la ara&ntilde;a del inducido</b> '
           u'de un generador, dibujado en la General Electric de Schenectady (Nueva York) en '
           u'<b>abril de 1911</b>. Mira tres cosas. Primero, el <b>cajet&iacute;n</b> de abajo a la '
           u'derecha: qui&eacute;n lo empez&oacute;, qui&eacute;n lo pas&oacute; a limpio, qui&eacute;n '
           u'lo inspeccion&oacute;, con fecha, y el n&uacute;mero de plano <i>M-1130859</i>. Segundo, '
           u'las <b>secciones</b> AA y CC, que est&aacute;n ah&iacute; para poder acotar lo que no se '
           u've por fuera. Y tercero, lo que de verdad importa para la sesi&oacute;n siguiente: hay '
           u'cotas escritas con <b>tres decimales</b> &mdash;18.500, 19.525&mdash; y al lado la '
           u'palabra <i>Fit</i>, ajuste. Ya en 1911 alguien sab&iacute;a que un n&uacute;mero redondo '
           u'no basta cuando dos piezas tienen que encajar.',
           u'Griffin, Charles Lewis (1867-) y Adams, Charles Clyde (1882-)',
           u'sin restricciones de copyright conocidas',
           u'https://commons.wikimedia.org/wiki/File:Machine_drawing;_a_practical_guide_to_the_standard_'
           u'methods_of_graphical_representation_of_machines,_including_complete_detail_drawings_of_a_'
           u'duplex_pump_and_of_a_direct-current_generator_(1914)_(14774400291).jpg') + u'''
      <div class="nota">
        <span class="n-tag">Cuidado con una confusi&oacute;n muy com&uacute;n</span>
        <b>La escala no cambia las cotas.</b> Si dibujas una pieza de 120 mm a escala 1:2, en el papel
        mide 60 mm&hellip; y la cota que escribes es <b>120</b>. La cota dice siempre la medida de la
        pieza real, no la del dibujo. Por eso, en un plano bien hecho, <b>nunca hace falta medir con
        la regla sobre el papel</b>: si tienes que hacerlo, es que falta una cota.
      </div>
''' + video('s1')

S1_PRACTICA = ficha(
    u'Actividad 1 &middot; Acotar una pieza vuestra, de las dos maneras',
    [u'CE2 &middot; 2.1', u'CE3 &middot; 3.1'], u'Grupos de 3 &middot; 20 min', u'''
          <h4>Primera parte &middot; Medir en la escena (6 min)</h4>
          <p>Con la escena de las dos tapas, dejad el error en <b>&plusmn;0,20 mm</b> y pulsad
             <b>Otra pieza</b> diez veces seguidas. Anotad en una tabla, para cada intento:</p>
          <ul>
            <li>La desviaci&oacute;n del cuarto agujero <b>en cadena</b>.</li>
            <li>La desviaci&oacute;n del cuarto agujero <b>desde el borde</b>.</li>
          </ul>
          <ol>
            <li>&iquest;Cu&aacute;ntas veces de diez ha fallado cada una?</li>
            <li>Pulsad <b>Peor caso</b>. &iquest;Cu&aacute;nto sale en cadena? Comprobadlo con la
                cuenta n &middot; e, sin la escena.</li>
            <li>Subid el error hasta que <b>tambi&eacute;n</b> falle la de la derecha. &iquest;Qu&eacute;
                valor hace falta? &iquest;Por qu&eacute; ese y no otro?</li>
          </ol>
          <h4>Segunda parte &middot; Vuestra pieza (10 min)</h4>
          <p>Elegid una pieza <b>plana</b> de vuestro proyecto que lleve al menos <b>tres agujeros</b>:
             la tapa del aviso de ventilaci&oacute;n, el soporte del dep&oacute;sito del riego o la
             base de la l&aacute;mpara. Dibujadla dos veces en la libreta, a l&aacute;piz y con regla,
             a escala 1:1 si cabe:</p>
          <ul>
            <li>Una vez <b>acotada en cadena</b>.</li>
            <li>Otra vez <b>acotada desde la referencia</b> que hay&aacute;is elegido&hellip; y
                escribid <b>por qu&eacute; esa cara y no otra</b>. Esa frase vale tanto como el dibujo.</li>
          </ul>
          <p>Las dos con su &empty; en los agujeros, su espesor apuntado y su cajet&iacute;n.</p>
          <h4>Tercera parte &middot; La prueba del plano (4 min)</h4>
          <p>Intercambiad la libreta con <b>otro grupo</b>, sin decir ni una palabra. Cada grupo escribe
             en el plano que le ha tocado:</p>
          <ol>
            <li>Una cosa que <b>no puede fabricar</b> porque falta una cota.</li>
            <li>Una cota que <b>sobra</b> o est&aacute; repetida.</li>
            <li>Una cota que no podr&iacute;a <b>medir</b> con una regla.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>La tabla de los diez intentos y el peor caso comprobado a mano <b>(3 puntos)</b>.</li>
            <li>Los dos planos completos, con &empty;, espesor y cajet&iacute;n <b>(4 puntos)</b>.</li>
            <li>La justificaci&oacute;n de la referencia elegida <b>(2 puntos)</b>.</li>
            <li>Las tres pegas encontradas en el plano del otro grupo <b>(1 punto)</b>.</li>
          </ul>
''')

S1_CIERRE = u'''
      <ol>
      ''' + pregunta(
          u'&iquest;Por qu&eacute; una pieza acotada en cadena acumula error y una acotada desde una '
          u'referencia no?',
          u'<p>Porque en cadena cada cota <b>arranca donde acab&oacute; la anterior</b>, as&iacute; que '
          u'se lleva encima todos los errores anteriores. Desde una referencia, cada cota sale de la '
          u'misma cara, que no se ha movido, y solo carga con su propio error.</p>') + pregunta(
          u'Cuatro cotas de 25 mm, con &plusmn;0,2 mm de error en cada una. &iquest;D&oacute;nde puede '
          u'acabar el cuarto agujero?',
          u'<p>En el peor caso, a 4 &middot; 0,2 = <b>0,8 mm</b> de su sitio. Acotando desde el borde, '
          u'el peor caso es <b>0,2 mm</b>, y no crece aunque pongas m&aacute;s agujeros.</p>') + pregunta(
          u'Si ya has puesto 25, 25, 25 y 25, &iquest;por qu&eacute; no puedes poner adem&aacute;s el '
          u'total de 100?',
          u'<p>Porque ser&iacute;a una <b>cota de m&aacute;s</b>: cinco &oacute;rdenes para cuatro '
          u'medidas. Las cuatro reales nunca van a sumar 100 exactos, as&iacute; que el que fabrica '
          u'tiene que desobedecer alguna, y no le has dicho cu&aacute;l. Se pone lo que manda, y lo '
          u'dem&aacute;s se deja fuera (o entre par&eacute;ntesis, como cota <b>informativa</b>).</p>'
          ) + pregunta(
          u'&iquest;Qu&eacute; cara de la pieza se elige como referencia?',
          u'<p>La que de verdad manda en el montaje: la que <b>apoya</b>, la que se <b>atornilla</b> o '
          u'la que <b>toca a la otra pieza</b>. No la que quede m&aacute;s c&oacute;moda de dibujar. '
          u'Acotar es decir qu&eacute; es lo que no se puede mover.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Con el agujero de <b>&empty;6</b> y el LED de <b>&empty;5</b> te sobraba medio mil&iacute;metro
        a cada lado, y por eso esta sesi&oacute;n ha bastado. Pero en el riego hay un
        <b>eje de 8 mm</b> que tiene que girar dentro de un agujero de 8 mm, y ah&iacute; medio
        mil&iacute;metro es un desastre. Peor: <b>nadie ha fabricado nunca una pieza de 8,000 mm</b>.
        En la siguiente sesi&oacute;n dejamos de escribir la medida que queremos y empezamos a escribir
        <b>entre qu&eacute; dos n&uacute;meros nos vale</b>.
      </div>
'''


# ==========================================================================
# SESION 2 - Tolerancias y ajustes
# ==========================================================================
S2_RETO = u'''
      <p>Cambiamos de proyecto. En el <b>riego autom&aacute;tico</b>, una de las versiones no lleva
         bomba: lleva un <b>dep&oacute;sito que bascula</b>, y un servo que lo inclina cuando toca
         regar. El dep&oacute;sito gira sobre un <b>eje de 8 mm</b> que apoya en dos agujeros del
         soporte.</p>
      <p>El plano est&aacute; perfecto: acotado desde la referencia, con su &empty;, su espesor y su
         cajet&iacute;n. Pone <b>&empty;8</b> en el eje y <b>&empty;8</b> en el agujero. Se reparten el
         trabajo entre dos grupos y vuelven las piezas.</p>
      <div class="aviso">
        <span class="n-tag">Lo que llega al montaje</span>
        En el grupo de Marta, <b>el eje no entra</b>: hay que meterlo a martillazos y, una vez dentro,
        el dep&oacute;sito no gira.<br>
        En el grupo de Iv&aacute;n, <b>el eje baila</b>: entra solo, se sale solo y el dep&oacute;sito
        cabecea tanto que derrama agua fuera de la maceta.
      </div>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento</span>
        <p>Los dos grupos ten&iacute;an el <b>mismo plano</b>, que ped&iacute;a 8 mm, y los dos han
           hecho 8 mm. &iquest;Qui&eacute;n se ha equivocado? Escr&iacute;belo antes de seguir.</p>
      </div>
      <p>Nadie. Y aqu&iacute; est&aacute; la idea que cuesta tragar la primera vez:</p>
      <p><b>Nunca en la historia se ha fabricado una pieza de 8,000 mm.</b> Ni con una lima, ni con un
         torno, ni con la m&aacute;quina m&aacute;s cara que exista. Lo que sale de cualquier
         m&aacute;quina es 8,03, o 7,98, o 8,0007. Siempre hay un decimal m&aacute;s abajo en el que la
         pieza deja de medir lo que ped&iacute;as. Si mides con m&aacute;s precisi&oacute;n, lo que
         encuentras no es el 8,000: es otro error m&aacute;s peque&ntilde;o.</p>
      <p>As&iacute; que escribir <b>&empty;8</b> en un plano donde dos piezas tienen que encajar es,
         literalmente, <b>no haber dicho nada</b>. La pregunta buena no es &laquo;&iquest;cu&aacute;nto
         mide?&raquo;. Es <b>&laquo;&iquest;entre qu&eacute; dos n&uacute;meros me vale?&raquo;</b>.</p>
'''

S2_TEORIA = u'''
      <div class="copiar">
        <h4>Las palabras, con la pieza delante</h4>
        <ul>
          <li><b>Medida nominal</b>: el n&uacute;mero redondo del que se habla. Los <b>8 mm</b> del eje.
              Es una etiqueta, no una medida: puede que ninguna pieza real la tenga.</li>
          <li><b>Desviaci&oacute;n superior</b> y <b>desviaci&oacute;n inferior</b>: cu&aacute;nto se
              puede pasar y cu&aacute;nto se puede quedar corto, respecto de la nominal. Se escriben
              como &empty;8 <sup>+0,022</sup><sub>&nbsp;0</sub>.</li>
          <li><b>Medida m&aacute;xima</b> y <b>m&iacute;nima</b>: nominal m&aacute;s cada
              desviaci&oacute;n. Aqu&iacute;, 8,022 y 8,000.</li>
          <li><b>Tolerancia</b>: la diferencia entre las dos, <b>0,022 mm</b>. Es la
              <b>anchura del permiso</b> que le das al taller. Siempre es positiva.</li>
          <li><b>Micra</b> (&micro;m): la mil&eacute;sima de mil&iacute;metro. Las tolerancias se hablan
              en micras porque en mil&iacute;metros sale todo lleno de ceros. 0,022 mm =
              <b>22 &micro;m</b>.</li>
        </ul>
        <p>Regla que ahorra discusiones: <b>la tolerancia no es un fallo que se permite, es una
           decisi&oacute;n de dise&ntilde;o</b>. Apretarla cuesta dinero y tiempo; dejarla ancha cuesta
           que la pieza no valga. Elegirla es tu trabajo, no el del que fabrica.</p>
      </div>
      <div class="copiar">
        <h4>El ajuste, que no vive en ninguna de las dos piezas</h4>
        <p>Un <b>ajuste</b> es lo que pasa cuando juntas <b>una pareja</b> de piezas: el eje y su
           agujero. Dos cuentas lo deciden todo:</p>
        <p style="font-size:17px;text-align:center;margin:10px 0">
           <b>Juego m&aacute;ximo = Agujero<sub>m&aacute;x</sub> &minus; Eje<sub>m&iacute;n</sub></b><br>
           <b>Juego m&iacute;nimo = Agujero<sub>m&iacute;n</sub> &minus; Eje<sub>m&aacute;x</sub></b></p>
        <p>Y seg&uacute;n c&oacute;mo salgan:</p>
        <ul>
          <li><b>Ajuste con juego</b>: el juego m&iacute;nimo es <b>positivo</b>. El agujero es siempre
              mayor que el eje. Entra sin forzar y gira. Es el del eje del dep&oacute;sito.</li>
          <li><b>Ajuste con apriete</b>: el juego m&aacute;ximo es <b>negativo</b>. El eje es siempre
              mayor. Hay que meterlo a presi&oacute;n, y luego no se mueve. Es el de un rodamiento en
              su alojamiento.</li>
          <li><b>Ajuste indeterminado</b>: el juego m&iacute;nimo es negativo y el m&aacute;ximo,
              positivo. <b>Unas veces entra suelto y otras aprieta</b>, y no puedes saber cu&aacute;l te
              va a tocar.</li>
        </ul>
        <p>Y una consecuencia que conviene ver ya:</p>
        <p style="font-size:16px;text-align:center;margin:10px 0">
           <b>Juego m&aacute;x &minus; Juego m&iacute;n = tolerancia del agujero + tolerancia del eje</b></p>
        <p>O sea: <b>lo que var&iacute;a el ajuste es la suma de los dos permisos</b>. Apretar solo uno
           de los dos sirve de poco; hay que mirar la pareja.</p>
      </div>
      <p>Al banco. Mueve las cuatro desviaciones y mira cambiar el tipo de ajuste. Empieza por los
         preajustes hechos, y deja para el final el que pone &laquo;a ojo, con regla y sierra&raquo;.</p>
''' + AJUSTE + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p><b>El indeterminado es el peor sitio donde estar</b>, y es donde acaban casi todos los
           proyectos de clase sin saberlo. No es que las piezas salgan mal: es que el mismo plano
           produce piezas que giran y piezas que no, y no hay manera de saber cu&aacute;l te toca hasta
           tenerla en la mano. Un proyecto que funciona &laquo;a veces&raquo; casi siempre tiene un
           ajuste indeterminado dentro.</p>
        <p><b>Por qu&eacute; el agujero se deja quieto y se mueve el eje.</b> F&iacute;jate en los
           preajustes: el agujero empieza casi siempre en <b>+0</b>. No es casualidad. Los agujeros se
           hacen con <b>brocas y escariadores</b>, que vienen en medidas fijas: tienes la de 8 y la de
           8,5, y no hay nada en medio. El eje, en cambio, se lima, se tornea o se compra en la medida
           que quieras. As&iacute; que <b>se fija el agujero y se juega con el eje</b>. Eso se llama
           <b>sistema de agujero &uacute;nico</b>, y es el que se usa casi siempre.</p>
        <p>Hay un sistema internacional entero para nombrar esto con dos caracteres &mdash;
           <b>H7/g6</b> y compa&ntilde;&iacute;a, la norma <b>ISO 286</b>&mdash;, donde la letra dice
           <b>d&oacute;nde</b> se coloca la zona respecto a la l&iacute;nea cero y el n&uacute;mero dice
           <b>cu&aacute;nto</b> mide. En 4.&ordm; no hace falta manejarlo: basta con entender qu&eacute;
           hay debajo, que es exactamente lo que acabas de mover con los mandos.</p>
      </div>

      <h3>Con qu&eacute; se mide eso, y qu&eacute; puedes prometer</h3>
      <p>Hay una trampa que hay que desmontar antes de seguir. Puedes escribir &plusmn;0,02 mm en un
         plano con mucha seguridad, pero si en el taller solo hay una regla, <b>no tienes forma de saber
         si la pieza cumple</b>. Y una tolerancia que no se puede comprobar no es una tolerancia: es un
         deseo.</p>
''' + foto('c2-calibre.jpg',
           u'Detalle de un pie de rey met&aacute;lico: la regla principal graduada en cent&iacute;metros, '
           u'el nonio deslizante grabado con 0,02 mm, las bocas grandes para exteriores y las '
           u'peque&ntilde;as de arriba para interiores',
           u'Un <b>pie de rey</b> (o calibre). En el cursor est&aacute; grabado lo &uacute;nico que de '
           u'verdad importa: <b>0,02 mm</b>. Esa es su <b>resoluci&oacute;n</b>, lo m&aacute;s fino que '
           u'puede distinguir, y sale del <b>nonio</b>, la escalita de abajo: sus divisiones son un '
           u'pel&iacute;n m&aacute;s cortas que las de la regla de arriba, y basta con ver '
           u'<b>cu&aacute;l de ellas coincide</b> con una raya de la regla para leer las '
           u'cent&eacute;simas, sin tener que apreciar nada a ojo. F&iacute;jate en que tiene '
           u'<b>dos parejas de bocas</b>: las grandes, abajo, miden por fuera; las peque&ntilde;as de '
           u'arriba miden por dentro, que es como se mide un agujero. Regla de taller: para poder '
           u'comprobar una tolerancia, el instrumento tiene que apreciar <b>del orden de diez veces '
           u'menos</b> que lo que quieres medir.',
           u'ArtMechanic', u'CC BY-SA 3.0',
           u'https://commons.wikimedia.org/wiki/File:Messschieber.jpg') + u'''
      <div class="copiar">
        <h4>Lo que puedes prometer con lo que tienes</h4>
        <table style="width:100%;border-collapse:collapse;font-size:14.5px">
          <tr><td style="padding:5px 6px;border-bottom:1px solid var(--line)"><b>Con qu&eacute; mides</b></td>
              <td style="padding:5px 6px;border-bottom:1px solid var(--line)"><b>Aprecia</b></td>
              <td style="padding:5px 6px;border-bottom:1px solid var(--line)"><b>Tolerancia que puedes comprobar</b></td></tr>
          <tr><td style="padding:5px 6px">Regla de acero</td><td style="padding:5px 6px">0,5 mm</td>
              <td style="padding:5px 6px">&plusmn;1 mm, y con optimismo</td></tr>
          <tr><td style="padding:5px 6px">Pie de rey</td><td style="padding:5px 6px">0,02 mm</td>
              <td style="padding:5px 6px">&plusmn;0,1 mm c&oacute;modo; &plusmn;0,05 apurando</td></tr>
          <tr><td style="padding:5px 6px">Micr&oacute;metro</td><td style="padding:5px 6px">0,01 mm</td>
              <td style="padding:5px 6px">&plusmn;0,02 mm</td></tr>
          <tr><td style="padding:5px 6px">Calibre pasa / no pasa</td><td style="padding:5px 6px">&mdash;</td>
              <td style="padding:5px 6px">la que le hayan hecho, y sin leer nada</td></tr>
        </table>
        <p>Los n&uacute;meros de esta tabla son <b>orientaci&oacute;n de taller</b>, no una norma.</p>
      </div>
''' + foto('c2-pasa-nopasa.jpg',
           u'Calibre tamp&oacute;n cil&iacute;ndrico de acero de unos 100 mm, con dos extremos de '
           u'di&aacute;metro distinto; en el mango van grabados GO 29.94 y NO GO 29.97',
           u'Un <b>calibre tamp&oacute;n pasa / no pasa</b>, y la idea de esta sesi&oacute;n convertida '
           u'en un trozo de acero. En el mango est&aacute; grabado todo: un extremo mide '
           u'<b>29,94 mm</b> y el otro <b>29,97 mm</b>. Para saber si un agujero est&aacute; bien, no '
           u'se mide ni se lee nada: se prueban los dos extremos. El de <b>29,94 tiene que entrar</b> '
           u'(si no entra, el agujero se ha quedado peque&ntilde;o) y el de <b>29,97 no tiene que '
           u'entrar</b> (si entra, se ha pasado). El agujero est&aacute; bien si cae en esa ventana de '
           u'<b>0,03 mm</b>, y la comprobaci&oacute;n la puede hacer cualquiera en dos segundos, sin '
           u'saber leer un nonio. As&iacute; se controlaba la producci&oacute;n en serie antes de que '
           u'existiera la electr&oacute;nica.',
           u'Glenn McKechnie', u'CC BY-SA 3.0',
           u'https://commons.wikimedia.org/wiki/File:GaugePlugSpecialGoNoGo.jpg') + u'''
      <h3>Por qu&eacute; hizo falta inventar esto</h3>
      <p>Durante casi toda la historia, las cosas se hac&iacute;an <b>por parejas</b>. El armero
         limaba el ca&ntilde;&oacute;n, limaba la pieza que iba dentro y las ajustaba <b>la una a la
         otra</b> hasta que iban bien. Funcionaba, y funcionaba muy bien. Pero ten&iacute;a un precio
         escondido: si se romp&iacute;a una pieza, <b>la de repuesto no val&iacute;a</b>, porque
         estaba hecha para otro conjunto. Hab&iacute;a que llevar el aparato entero a un taller y
         volver a ajustar.</p>
      <ul>
        <li><b>1785</b>, Par&iacute;s. El armero <b>Honor&eacute; Blanc</b> ense&ntilde;a una cosa que
            parece un truco de feria: desmonta varios mecanismos de disparo, mezcla las piezas en
            cajones, coge piezas al azar y monta mecanismos que funcionan. Entre el p&uacute;blico
            est&aacute; <b>Thomas Jefferson</b>, entonces embajador de Estados Unidos en Francia, que
            se queda tan impresionado que escribe a su gobierno para contarlo.</li>
        <li>La idea se bautiza como <b>intercambiabilidad</b>, y cambia la manera de fabricar: cada
            pieza se hace contra <b>el plano</b>, no contra la pieza de al lado. Para que eso pueda
            funcionar hay que decir, por primera vez, <b>cu&aacute;nto se puede desviar cada una</b>.
            Ah&iacute; nace la tolerancia.</li>
        <li><b>1841</b>. <b>Joseph Whitworth</b> propone en Inglaterra <b>una sola rosca</b> para
            todos: mismo perfil, mismo &aacute;ngulo, mismo paso para cada di&aacute;metro. Hasta
            entonces cada taller hac&iacute;a la suya, y un tornillo solo entraba en su tuerca. Es el
            primer est&aacute;ndar industrial que se impone de verdad, y es la raz&oacute;n de que hoy
            una tuerca M3 comprada en cualquier sitio entre en un tornillo M3 comprado en cualquier
            otro.</li>
      </ul>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Merece la pena ver lo que esto significa para vosotros. Vuestro <b>servo SG90</b>, vuestros
           <b>tornillos M3</b>, vuestra <b>varilla de 8</b> y vuestros <b>cables Dupont</b> vienen de
           f&aacute;bricas distintas, de pa&iacute;ses distintos, que no se han hablado nunca. Y encajan.
           Eso no es magia ni suerte: es que todas fabrican contra <b>la misma norma, con su tolerancia
           escrita</b>. La intercambiabilidad es una de las tecnolog&iacute;as m&aacute;s invisibles y
           m&aacute;s importantes que existen.</p>
      </div>
''' + video('s2')

S2_PRACTICA = ficha(
    u'Actividad 2 &middot; Elegir el ajuste de vuestro proyecto',
    [u'CE2 &middot; 2.1 &middot; 2.2'], u'Parejas &middot; 20 min', u'''
          <h4>Primera parte &middot; Las cuentas, a mano (7 min)</h4>
          <p>Sin la escena, en la libreta. Un eje y un agujero de nominal <b>8 mm</b>:</p>
          <ul>
            <li>Agujero: desviaciones <b>+0 / +0,022</b></li>
            <li>Eje: desviaciones <b>&minus;0,028 / &minus;0,013</b></li>
          </ul>
          <ol>
            <li>Escribid las cuatro medidas (agujero m&aacute;x y m&iacute;n, eje m&aacute;x y
                m&iacute;n).</li>
            <li>Calculad <b>juego m&aacute;ximo</b> y <b>juego m&iacute;nimo</b>. &iquest;Qu&eacute;
                tipo de ajuste es?</li>
            <li>Comprobad que juego m&aacute;x &minus; juego m&iacute;n es igual a la suma de las dos
                tolerancias.</li>
            <li>Ahora <b>subid el eje 30 micras</b> (las dos desviaciones). &iquest;Sigue girando?
                &iquest;Qu&eacute; tipo de ajuste ha pasado a ser?</li>
          </ol>
          <p>Comprobad los cuatro resultados en la escena. Si no coinciden, uno de los dos est&aacute;
             mal: averiguad cu&aacute;l <b>antes</b> de seguir.</p>
          <h4>Segunda parte &middot; Vuestra pareja de piezas (8 min)</h4>
          <p>Buscad en vuestro proyecto <b>dos piezas que tengan que encajar</b>: el eje del
             dep&oacute;sito y su soporte, la tapa del aviso y su caja, el brazo de la l&aacute;mpara y
             su casquillo. Decidid:</p>
          <ol>
            <li>&iquest;Ten&eacute;is que <b>girar</b>, <b>deslizar</b> o <b>no moveros nunca</b>?</li>
            <li>Elegid las cuatro desviaciones y escribid las dos cotas como ir&iacute;an en el plano.</li>
            <li>Calculad los dos juegos y decid qu&eacute; ajuste os sale.</li>
            <li>&iquest;Pod&eacute;is <b>comprobar</b> esa tolerancia con lo que hay en el aula? Si la
                respuesta es no, <b>ensanchadla</b> hasta que s&iacute;, y anotad la nueva.</li>
          </ol>
          <h4>Tercera parte &middot; Si hay pie de rey (5 min)</h4>
          <p>Medid tres veces la <b>misma</b> varilla, asent&aacute;ndola bien entre las bocas y
             anotando las tres lecturas. &iquest;Salen iguales? La diferencia entre vuestra lectura
             m&aacute;s alta y la m&aacute;s baja es <b>vuestra</b> incertidumbre, y ninguna tolerancia
             m&aacute;s estrecha que eso os la pod&eacute;is creer.</p>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Las cuatro cuentas del ejercicio, con el tipo de ajuste <b>(4 puntos)</b>.</li>
            <li>Las dos cotas de vuestras piezas, bien escritas <b>(3 puntos)</b>.</li>
            <li>La decisi&oacute;n de si se puede comprobar, y el ajuste de la tolerancia
                <b>(3 puntos)</b>.</li>
          </ul>
''')

S2_CIERRE = u'''
      <ol>
      ''' + pregunta(
          u'&iquest;Por qu&eacute; poner &laquo;&empty;8&raquo; a secas en dos piezas que tienen que '
          u'encajar es no haber dicho nada?',
          u'<p>Porque ninguna m&aacute;quina fabrica un 8,000: lo que sale es algo cercano. Si no dices '
          u'<b>entre qu&eacute; dos n&uacute;meros</b> te vale, el taller puede darte un 8,3 y un 7,7 y '
          u'haber cumplido tu plano. La medida &uacute;til no es un n&uacute;mero, es un '
          u'<b>intervalo</b>.</p>') + pregunta(
          u'Agujero de 8,000 a 8,022 y eje de 7,972 a 7,987. &iquest;Qu&eacute; ajuste sale?',
          u'<p>Juego m&aacute;ximo = 8,022 &minus; 7,972 = <b>0,050 mm</b>. Juego m&iacute;nimo = '
          u'8,000 &minus; 7,987 = <b>0,013 mm</b>. Los dos positivos, as&iacute; que es un '
          u'<b>ajuste con juego</b>: gira siempre, salgan como salgan las piezas.</p>') + pregunta(
          u'&iquest;Qu&eacute; tiene de malo un ajuste indeterminado?',
          u'<p>Que el mismo plano produce <b>piezas que entran sueltas y piezas que aprietan</b>, sin '
          u'que puedas saber cu&aacute;l te toca. No es que est&eacute;n mal hechas: est&aacute; mal '
          u'elegido el ajuste. Un proyecto que funciona &laquo;a veces&raquo; suele tener uno de '
          u'estos dentro.</p>') + pregunta(
          u'&iquest;Por qu&eacute; se fija el agujero y se juega con el eje?',
          u'<p>Porque los agujeros salen de <b>brocas y escariadores de medidas fijas</b> y el eje se '
          u'puede limar, tornear o comprar en la medida que quieras. Es m&aacute;s barato mover lo que '
          u'se puede mover. Se llama <b>sistema de agujero &uacute;nico</b>.</p>') + pregunta(
          u'Tu tolerancia es &plusmn;0,02 mm y en el aula solo hay una regla. &iquest;Qu&eacute; pasa?',
          u'<p>Que esa tolerancia <b>no existe</b>: no puedes comprobar si la pieza cumple, as&iacute; '
          u'que no puedes aceptarla ni rechazarla. Una tolerancia que no se puede medir con lo que hay '
          u'es un deseo, no una especificaci&oacute;n. O consigues un pie de rey, o la ensanchas.</p>'
          ) + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya tienes piezas que encajan. Ahora hay que <b>sujetarlas unas a otras</b>, y ah&iacute; hay una
        decisi&oacute;n que parece de taller y en realidad es de dise&ntilde;o: si la uni&oacute;n se
        puede volver a abrir o no. Adem&aacute;s vas a ver una cuenta que sorprende a todo el mundo: un
        tornillo M3 de acero aguanta <b>170 kilos</b>, y aun as&iacute; vuestra uni&oacute;n se va a
        romper con <b>quince</b>. El tornillo no tiene la culpa.
      </div>
'''


# ==========================================================================
# SESION 3 - Union de piezas
# ==========================================================================
S3_RETO = u'''
      <p>Tercer proyecto, la <b>l&aacute;mpara de estudio que se ajusta sola</b>. El brazo se une a la
         base, y el grupo lo resuelve como se resuelve todo cuando quedan diez minutos de clase: un
         chorro de <b>silicona caliente</b>. Queda firme, aguanta, y se van a casa contentos.</p>
      <p>Tres semanas despu&eacute;s hay que cambiar el LED, que va dentro del brazo. Para llegar a
         &eacute;l hay que abrir la uni&oacute;n. Y para abrir la uni&oacute;n hay que
         <b>romper la pieza</b>.</p>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento</span>
        <p>La silicona hizo su trabajo: uni&oacute; las dos piezas y aguant&oacute;. Entonces,
           &iquest;fue una mala decisi&oacute;n? &iquest;Y qu&eacute; habr&iacute;a hecho falta saber
           <b>antes</b> de pegar para decidirlo bien?</p>
      </div>
      <p>Hac&iacute;a falta saber una cosa que no es t&eacute;cnica: <b>si esa uni&oacute;n se iba a
         tener que abrir alguna vez</b>. Y eso no se descubre montando: se decide dibujando.</p>
      <p>Pero hay una segunda sorpresa en esta sesi&oacute;n, y es de n&uacute;meros. Supongamos que en
         vez de pegar hubieran puesto <b>un tornillo M3</b>. Miras la tabla y ves que un tornillo M3 de
         acero aguanta del orden de <b>1700 newtons</b>, que son unos <b>170 kilos</b> colgando.</p>
      <div class="aviso">
        <span class="n-tag">La cuenta que enga&ntilde;a</span>
        &laquo;El brazo pesa 300 gramos y alguien puede empujarlo con dos kilos de fuerza. El tornillo
        aguanta 170. <b>Sobra por ochenta veces.</b>&raquo;<br><br>
        Y sin embargo, esa uni&oacute;n se rompe. Con el brazo impreso en PLA de <b>3 mm</b> de
        espesor, la uni&oacute;n de un tornillo falla alrededor de los <b>500 newtons</b>: la tercera
        parte. Y si el brazo fuera de DM, con <b>110</b>.
      </div>
      <p>El tornillo no se rompe. Lo que se rompe es <b>el material que hay alrededor del
         agujero</b>. Y eso se calcula.</p>
'''

S3_TEORIA = u'''
      <div class="copiar">
        <h4>Dos familias, y la pregunta que las separa</h4>
        <p><b>Uniones desmontables</b>: se pueden abrir y volver a cerrar <b>sin estropear nada</b>, y
           tantas veces como haga falta. Tornillo con tuerca, tornillo rosca-chapa, perno, pasador,
           chaveta, brida, im&aacute;n, encaje a presi&oacute;n.</p>
        <p><b>Uniones fijas</b>: para abrirlas hay que <b>destruir algo</b>, la uni&oacute;n o la
           pieza. Pegado, soldadura, remachado, ajuste con apriete, soldadura de pl&aacute;stico.</p>
        <p>La pregunta para elegir <b>no</b> es cu&aacute;l aguanta m&aacute;s. Es:
           <b>&iquest;esto se va a tener que abrir alguna vez?</b> Para cambiar una pila, arreglar una
           aver&iacute;a, reciclar el aparato al final o simplemente corregir un error de montaje.
           Si la respuesta es s&iacute;, la decisi&oacute;n ya est&aacute; tomada.</p>
      </div>
      <div class="copiar">
        <h4>Qu&eacute; falla de verdad cuando una uni&oacute;n se rompe</h4>
        <p>Una uni&oacute;n no falla &laquo;en general&raquo;. Falla por un sitio concreto, y hay que
           calcular <b>los dos candidatos</b> y quedarse con el peor.</p>
        <p><b>1 &middot; El elemento de uni&oacute;n</b>, cortado por el plano de la junta:</p>
        <p style="font-size:17px;text-align:center;margin:8px 0">
           <b>&tau; = F / A</b>, con A = &pi; &middot; d&sup2; / 4</p>
        <p>Un tornillo M3 tiene A = &pi; &middot; 3&sup2; / 4 = <b>7,07 mm&sup2;</b>. Un acero corriente
           de clase 4.8 aguanta a cortadura del orden de <b>240 N/mm&sup2;</b>, as&iacute; que
           7,07 &middot; 240 &asymp; <b>1700 N</b> por tornillo.</p>
        <p><b>2 &middot; El material alrededor del agujero</b>, aplastado por el tornillo:</p>
        <p style="font-size:17px;text-align:center;margin:8px 0">
           <b>&sigma; = F / (d &middot; t)</b></p>
        <p>d es el di&aacute;metro del tornillo y <b>t el espesor de la pieza</b>. El &aacute;rea que
           recibe el empuje es el rect&aacute;ngulo que proyecta el tornillo contra la pared del
           agujero. Un PLA impreso aguanta ah&iacute; unos <b>55 N/mm&sup2;</b>; en 3 mm de espesor,
           55 &middot; 3 &middot; 3 = <b>495 N</b>. Ese es el n&uacute;mero que manda.</p>
        <p><b>3 &middot; Si es pegado</b>, lo que trabaja es toda el &aacute;rea de contacto:</p>
        <p style="font-size:17px;text-align:center;margin:8px 0">
           <b>&tau; = F / &aacute;rea pegada</b></p>
        <p>Y el &aacute;rea la eliges t&uacute; al dibujar el solape. <b>Es lo &uacute;nico gratis de
           toda la sesi&oacute;n</b>: alargar un solape no cuesta dinero.</p>
      </div>
      <p>En el banco est&aacute;n las tres a la vez, sobre las mismas dos piezas. Empieza bajando el
         <b>espesor</b> y mira qui&eacute;n se cae primero.</p>
''' + UNIONES + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p><b>En vuestros proyectos, el tornillo nunca es el problema.</b> Un M3 de acero aguanta 1700 N
           y vuestras piezas son de pl&aacute;stico o de tablero de 3 mm. Para que el tornillo llegara a
           enterarse har&iacute;a falta que la pieza aguantara antes, y no lo hace. Por eso, cuando una
           uni&oacute;n de clase se rompe, lo que ves es <b>el agujero ovalado</b> o un trozo de borde
           arrancado, no un tornillo partido.</p>
        <p>Esto tiene una consecuencia pr&aacute;ctica que cuesta cuatro c&eacute;ntimos: si la
           uni&oacute;n va justa, <b>no pongas un tornillo m&aacute;s gordo, pon una arandela</b>. La
           arandela no toca el agujero, pero reparte el apriete de la cabeza sobre mucha m&aacute;s
           superficie de la pieza, que es justo lo que se estaba hundiendo.</p>
        <p><b>Una simplificaci&oacute;n que conviene declarar.</b> Aqu&iacute; se supone que la carga la
           lleva el tornillo apoyado contra el borde del agujero. En una uni&oacute;n bien apretada, una
           parte la lleva el <b>rozamiento</b> entre las dos piezas, y entonces aguanta m&aacute;s.
           Calcular sin contar con ese rozamiento es lo que se hace siempre que no se puede garantizar
           el apriete, y deja el resultado <b>del lado seguro</b>.</p>
      </div>
      <div class="copiar">
        <h4>Reglas de taller para que la uni&oacute;n no se caiga tonta</h4>
        <ul>
          <li><b>Distancia al borde</b>: el centro del agujero, al menos a <b>2 di&aacute;metros</b> del
              canto en pl&aacute;stico o metal, y a <b>3</b> en madera o tablero. M&aacute;s cerca, el
              tornillo <b>arranca un trozo de borde</b> en vez de aplastar el agujero, y eso pasa de
              golpe y sin avisar.</li>
          <li><b>Arandela siempre</b> bajo la tuerca y, en material blando, tambi&eacute;n bajo la
              cabeza.</li>
          <li><b>Si vibra, se afloja.</b> Un motor vibra. Tuerca autoblocante, arandela de presi&oacute;n
              o una gota de laca de u&ntilde;as en la rosca.</li>
          <li><b>No rosques directamente en DM</b>: se deshace. Tornillo pasante con tuerca, o inserto.</li>
          <li><b>En PLA impreso, mejor pasante con tuerca</b> que roscado en el pl&aacute;stico: la
              rosca impresa se pela a la segunda vez que abres.</li>
          <li><b>Dos tornillos, no uno.</b> Con uno solo, la pieza gira alrededor de &eacute;l.</li>
        </ul>
      </div>

      <h3>Lo fijo, visto de cerca</h3>
''' + foto('c2-remaches.jpg',
           u'Dos remaches ciegos de cabeza blanca sobre fondo claro: el de arriba entero, con su '
           u'v&aacute;stago met&aacute;lico recto; el de abajo ya colocado, con el cuerpo abierto en '
           u'p&eacute;talos por el otro extremo',
           u'Dos <b>remaches ciegos</b>, de los que sujetan una matr&iacute;cula. Arriba, sin usar. '
           u'Abajo, despu&eacute;s de pasar por la remachadora: el v&aacute;stago de acero ha tirado '
           u'hacia atr&aacute;s y ha <b>deformado el cuerpo</b>, que se ha abierto en p&eacute;talos por '
           u'la cara de detr&aacute;s y ha aprisionado las dos piezas. Se llaman <b>ciegos</b> porque '
           u'se ponen desde <b>un solo lado</b>: no hace falta llegar por detr&aacute;s, y eso los hace '
           u'perfectos para un tubo o una caja cerrada. Ahora mira el de abajo y hazte la pregunta de '
           u'esta sesi&oacute;n: <b>&iquest;c&oacute;mo lo quitas?</b> No hay manera de devolverlo a su '
           u'forma. Hay que <b>taladrarle la cabeza</b> y perder el remache. Eso es exactamente lo que '
           u'quiere decir <i>uni&oacute;n fija</i>: no es que sea m&aacute;s fuerte, es que la '
           u'deformaci&oacute;n que la hace fuerte no se deshace.',
           u'Cjp24', u'CC BY-SA 4.0',
           u'https://commons.wikimedia.org/wiki/File:Blind_rivets_before_and_after_strain.jpg') + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p><b>Lo que se pega no se repara, y eso tiene consecuencias fuera del taller.</b> La misma
           decisi&oacute;n que acabas de tomar para el brazo de la l&aacute;mpara la toman todos los
           d&iacute;as en las f&aacute;bricas de m&oacute;viles, de auriculares y de electrodom&eacute;sticos.
           Pegar es m&aacute;s r&aacute;pido, m&aacute;s barato, queda m&aacute;s fino y no se ven
           tornillos. Y convierte una bater&iacute;a gastada en un aparato entero a la basura.</p>
        <p>Por eso la Uni&oacute;n Europea lleva a&ntilde;os empujando el <b>derecho a reparar</b>: si
           un aparato no se puede abrir, tampoco se puede arreglar <b>ni separar para reciclar</b>, y
           entonces el problema deja de ser tuyo y pasa a ser de todos. Esto se mira despacio en la
           <b>unidad 3</b>, cuando toque el ciclo de vida de los materiales, y vuelve en la
           <b>unidad 8</b>, con el impacto. Qu&eacute;date con esto: <b>la manera de unir dos piezas es
           una decisi&oacute;n ambiental</b>, aunque no lo parezca.</p>
        <p>Y no es una regla ciega: hay uniones que <b>deben</b> ser fijas. Un remache no se afloja con
           las vibraciones, una soldadura no deja entrar agua y un ajuste con apriete no se sale solo.
           Lo que no vale es pegar <b>por comodidad</b> algo que se va a tener que abrir.</p>
      </div>
''' + video('s3')

S3_PRACTICA = ficha(
    u'Actividad 3 &middot; El mapa de uniones de vuestro proyecto',
    [u'CE2 &middot; 2.2'], u'Grupos de 3 &middot; 20 min', u'''
          <h4>Primera parte &middot; El mapa (7 min)</h4>
          <p>Listad <b>todas</b> las uniones de vuestro proyecto: pieza con pieza, pieza con placa,
             placa con caja, caja con pared. Suelen salir entre seis y diez. Para cada una, una fila en
             la libreta:</p>
          <table style="width:100%;border-collapse:collapse;font-size:14px;margin:8px 0">
            <tr><td style="padding:5px 6px;border-bottom:1px solid var(--line)"><b>Qu&eacute; une</b></td>
                <td style="padding:5px 6px;border-bottom:1px solid var(--line)"><b>&iquest;Se abrir&aacute; alguna vez?</b></td>
                <td style="padding:5px 6px;border-bottom:1px solid var(--line)"><b>Tipo elegido</b></td>
                <td style="padding:5px 6px;border-bottom:1px solid var(--line)"><b>Por qu&eacute;</b></td></tr>
            <tr><td style="padding:5px 6px">&nbsp;</td><td></td><td></td><td></td></tr>
            <tr><td style="padding:5px 6px">&nbsp;</td><td></td><td></td><td></td></tr>
          </table>
          <p>La columna del medio se contesta con un caso concreto: &laquo;s&iacute;, para cambiar la
             pila&raquo;, &laquo;no, nunca&raquo;. No vale &laquo;puede ser&raquo;.</p>
          <h4>Segunda parte &middot; La uni&oacute;n cr&iacute;tica (8 min)</h4>
          <p>De todas, elegid <b>la que m&aacute;s fuerza aguanta</b> y calculadla en la libreta, con
             todos los pasos:</p>
          <ol>
            <li>&iquest;Qu&eacute; fuerza tiene que aguantar? Estimadla, pero <b>decid de d&oacute;nde
                sale el n&uacute;mero</b> (el peso de lo que cuelga, un empuj&oacute;n de 20 N, el tir&oacute;n
                de alguien que se engancha con el cable&hellip;).</li>
            <li>Con el material y el espesor que ten&eacute;is, calculad el <b>aplastamiento</b>:
                &sigma; &middot; d &middot; t.</li>
            <li>Comparadlo con lo que aguanta el tornillo. <b>&iquest;Qui&eacute;n falla primero?</b></li>
            <li>Sacad el <b>coeficiente de seguridad</b> y comprobadlo en la escena.</li>
          </ol>
          <p>Si sale por debajo de <b>2</b>, arregladlo, y hay tres maneras: m&aacute;s tornillos, m&aacute;s
             espesor o cambiar a pegado con m&aacute;s solape. <b>Calculad las tres</b> y decid cu&aacute;l
             eleg&iacute;s.</p>
          <h4>Tercera parte &middot; La prueba de los cinco minutos (5 min)</h4>
          <p>Mirad vuestro mapa y contestad por escrito: <b>&iquest;se puede sacar la placa Arduino del
             aparato montado en menos de cinco minutos, sin romper nada?</b> Si la respuesta es no,
             cambiad una uni&oacute;n de la lista y decid cu&aacute;l. Lo vais a agradecer el d&iacute;a
             que se os quede colgado el programa.</p>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>El mapa completo, con la columna del porqu&eacute; contestada <b>(3 puntos)</b>.</li>
            <li>El c&aacute;lculo de la uni&oacute;n cr&iacute;tica, con todos los pasos y las unidades
                <b>(4 puntos)</b>.</li>
            <li>Las tres maneras de arreglarlo, calculadas, y la elegida <b>(2 puntos)</b>.</li>
            <li>La prueba de los cinco minutos, contestada y con la consecuencia <b>(1 punto)</b>.</li>
          </ul>
''')

S3_CIERRE = u'''
      <ol>
      ''' + pregunta(
          u'&iquest;Cu&aacute;l es la pregunta que decide si una uni&oacute;n debe ser fija o '
          u'desmontable?',
          u'<p><b>&iquest;Esto se va a tener que abrir alguna vez?</b> Para cambiar una pila, reparar '
          u'una aver&iacute;a, corregir un montaje o separar los materiales al reciclar. No es una '
          u'pregunta de resistencia: es de ciclo de vida.</p>') + pregunta(
          u'Un tornillo M3 aguanta 1700 N y la uni&oacute;n se rompe con 500. &iquest;Qu&eacute; ha '
          u'pasado?',
          u'<p>Ha fallado <b>la pieza, no el tornillo</b>. El material se aplasta alrededor del '
          u'agujero: &sigma; = F / (d &middot; t). Con PLA de 55 N/mm&sup2; y 3 mm de espesor, '
          u'55 &middot; 3 &middot; 3 = 495 N. Manda <b>siempre el menor de los dos</b>.</p>'
          ) + pregunta(
          u'&iquest;Por qu&eacute; doblar el solape de una junta pegada dobla lo que aguanta?',
          u'<p>Porque en el pegado &tau; = F / &aacute;rea, y el &aacute;rea es el solape por el ancho. '
          u'Doble &aacute;rea, doble fuerza. Y a diferencia de poner m&aacute;s tornillos, alargar un '
          u'solape <b>no cuesta nada</b>: es la mejor manera que hay de ganar resistencia dibujando.</p>'
          ) + pregunta(
          u'&iquest;Por qu&eacute; no se pone el agujero pegado al borde de la pieza?',
          u'<p>Porque entonces el tornillo no aplasta el agujero: <b>arranca el trozo de borde</b> que '
          u'tiene delante, de golpe y sin avisar. La regla de taller es dejar <b>2 di&aacute;metros</b> '
          u'en pl&aacute;stico o metal y <b>3</b> en madera.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya tienes el plano, las tolerancias y las uniones decididas. Falta la pregunta que lo cambia
        todo hacia atr&aacute;s: <b>&iquest;con qu&eacute; lo vas a hacer?</b> Porque la misma pieza
        sale de tres maneras distintas &mdash;con la sierra, con el l&aacute;ser o con la
        impresora&mdash;, y cada una cuesta otro dinero, tarda otro rato y <b>clava otra cota</b>. Vas
        a descubrir que la t&eacute;cnica no se elige al final: obliga a cambiar el dibujo.
      </div>
'''


# ==========================================================================
# SESION 4 - Del plano a la pieza
# ==========================================================================
S4_RETO = u'''
      <p>&Uacute;ltima pieza del recorrido, y volvemos a la <b>tapa del aviso de ventilaci&oacute;n</b>
         con la que empez&oacute; la unidad. Ya est&aacute; bien acotada, ya sabes qu&eacute;
         tolerancia le puedes prometer y ya sabes c&oacute;mo se va a sujetar. Queda lo &uacute;ltimo:
         hacerla.</p>
      <p>En el aula hay tres maneras. Y en clase, la conversaci&oacute;n es siempre la misma:</p>
      <div class="aviso">
        <span class="n-tag">Lo que dice todo el mundo el primer d&iacute;a</span>
        <b>&laquo;La imprimimos en 3D, que queda mucho mejor.&raquo;</b>
      </div>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento</span>
        <p>Hay <b>una</b> impresora 3D en el departamento y <b>diez grupos</b> en clase. Una tapa como
           esa tarda unos <b>30 minutos</b> de m&aacute;quina. &iquest;Cu&aacute;nto tarda en estar
           impresa la tapa del &uacute;ltimo grupo de la cola? Haz la cuenta antes de seguir.</p>
      </div>
      <p>Cinco horas. Es decir: <b>casi dos semanas de clases de Tecnolog&iacute;a</b>, y eso si nada
         se despega de la cama, que se despega. La misma tapa, cortada con la sierra, est&aacute;
         terminada al final de la sesi&oacute;n de hoy, y cortada con el l&aacute;ser, en cinco
         minutos.</p>
      <p>Pero el tiempo y el dinero son la parte f&aacute;cil. Lo importante viene ahora, y es lo que
         convierte esta sesi&oacute;n en una sesi&oacute;n de <b>dise&ntilde;o</b> y no de taller:
         <b>cada t&eacute;cnica te obliga a dibujar la pieza de otra manera</b>. No se elige la
         t&eacute;cnica al final, mirando el plano terminado. Se elige antes, porque decide lo que
         puedes dibujar.</p>
'''

S4_TEORIA = u'''
      <div class="copiar">
        <h4>Lo que hay en el aula, y qu&eacute; hace cada cosa</h4>
        <ul>
          <li><b>Medir y marcar</b>: regla, escuadra, gramil, punta de trazar y <b>granete</b>. El
              granete hace una picadura donde va el agujero, y sin &eacute;l la broca <b>patina</b> y
              el agujero sale donde quiere. Es el paso que m&aacute;s se salta y el que m&aacute;s
              piezas estropea.</li>
          <li><b>Cortar</b>: sierra de marqueter&iacute;a (curvas, despacio), segueta y sierra de arco
              (rectos), c&uacute;ter y regla met&aacute;lica (cart&oacute;n pluma, PVC fino),
              <b>cortadora l&aacute;ser</b> si el centro la tiene.</li>
          <li><b>Taladrar</b>: taladro de columna mucho mejor que de mano, porque entra perpendicular.
              La pieza <b>siempre sujeta</b> con el sargento, nunca con la mano.</li>
          <li><b>Rebajar y afinar</b>: lima, papel de lija de grano grueso a fino. Es lo que convierte
              una pieza cortada en una pieza que <b>encaja</b>, y es donde se ajusta lo que la
              m&aacute;quina no clav&oacute;.</li>
          <li><b>Fabricaci&oacute;n aditiva</b>: la impresora 3D, que no quita material sino que lo
              <b>a&ntilde;ade</b> capa a capa. Es la &uacute;nica de la lista que puede hacer formas
              huecas por dentro.</li>
        </ul>
      </div>
      <div class="copiar">
        <h4>La cuenta del taladro: a qu&eacute; vueltas va cada broca</h4>
        <p>Una broca no se define por las vueltas, sino por la <b>velocidad de corte</b> V<sub>c</sub>:
           lo deprisa que pasa el filo por el material, en metros por minuto. Cada material tiene la
           suya, y de ah&iacute; salen las revoluciones:</p>
        <p style="font-size:18px;text-align:center;margin:10px 0">
           <b>n = 1000 &middot; V<sub>c</sub> / (&pi; &middot; D)</b></p>
        <p>n en revoluciones por minuto, V<sub>c</sub> en m/min y <b>D el di&aacute;metro de la broca
           en mil&iacute;metros</b>.</p>
        <p><b>Ejemplo.</b> Un agujero de &empty;6 en contrachapado, con V<sub>c</sub> = 40 m/min:</p>
        <p style="text-align:center;margin:8px 0">n = 1000 &middot; 40 / (&pi; &middot; 6) = 40000 / 18,85
           = <b>2122 rpm</b></p>
        <p>Y ahora lo que de verdad hay que llevarse: <b>D est&aacute; dividiendo</b>. Con la broca de
           12 mm, el mismo material pide la mitad de vueltas, <b>1061 rpm</b>. Por eso una broca gorda
           a las vueltas de una fina <b>quema la madera, funde el pl&aacute;stico y se estropea</b>: el
           filo va al doble de velocidad aunque el motor gire igual.</p>
        <p>Orientaci&oacute;n de V<sub>c</sub> para brocas de acero r&aacute;pido (HSS), en m/min:
           madera y tablero <b>30-60</b>, pl&aacute;sticos <b>30-50</b>, aluminio <b>60-100</b>, acero
           <b>20-30</b>. Son valores de taller, no una norma.</p>
      </div>
      <div class="copiar">
        <h4>Una cosa m&aacute;s sobre los agujeros, que enlaza con la sesi&oacute;n 2</h4>
        <p>Un agujero taladrado <b>siempre sale m&aacute;s grande que la broca</b>: entre una y dos
           d&eacute;cimas, porque la broca cabecea un poco al entrar. Nunca sale m&aacute;s
           peque&ntilde;o.</p>
        <p>De ah&iacute; salen dos consecuencias pr&aacute;cticas: que el agujero se acota siempre
           <b>hacia arriba</b> (+0 / +0,1 y no &plusmn;0,05), y que si quieres una medida fina hay que
           taladrar por debajo y terminar con un <b>escariador</b>, que es una broca sin punta que solo
           repasa la pared.</p>
      </div>
      <p>Al banco. Es la misma tapa de la sesi&oacute;n 1, con las mismas cotas, hecha de tres maneras.
         Mira las tres columnas a la vez: no hay una ganadora.</p>
''' + TALLER + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p><b>Dise&ntilde;ar para fabricar.</b> Esto es lo que hay que llevarse de la sesi&oacute;n, y
           no es una lista de m&aacute;quinas: es que <b>el dibujo cambia seg&uacute;n qui&eacute;n lo
           vaya a hacer</b>.</p>
        <ul>
          <li><b>Si va a la sierra</b>: l&iacute;neas rectas y &aacute;ngulos abiertos. Cada curva la
              pagas en minutos, y un rinc&oacute;n en &aacute;ngulo recto por dentro <b>no se puede
              serrar</b>: hay que taladrarlo primero. Pon un <b>redondeo</b> en las esquinas interiores
              y ya est&aacute; resuelto.</li>
          <li><b>Si va al l&aacute;ser</b>: todo tiene que ser <b>plano</b>. No hay rebajes a media
              altura ni piezas con relieve: lo que sale es un perfil recortado. A cambio, las curvas
              son gratis. Y hay que descontar del dibujo la <b>sangr&iacute;a</b> del haz, unas dos
              d&eacute;cimas que se evaporan: si dibujas una ranura de 3,0 para una pieza de 3,0, la
              ranura sale de 3,2 y queda floja.</li>
          <li><b>Si va a la impresora</b>: puedes hacer formas que no salen de ninguna otra manera,
              pero (1) lo que <b>vuele m&aacute;s de 45&deg;</b> pide soporte, que luego hay que
              arrancar y deja la cara fea; (2) la pieza es un montón de capas pegadas, y
              <b>se parte por donde se pegan</b>, as&iacute; que hay que orientarla de modo que la
              fuerza no intente separarlas; y (3) los agujeros verticales salen un poco
              <b>peque&ntilde;os</b>, as&iacute; que se dibujan dos o tres d&eacute;cimas de
              m&aacute;s.</li>
        </ul>
        <p>Y la regla que engloba a las tres: <b>la pieza m&aacute;s barata es la que no hay que
           fabricar</b>. Antes de dibujar nada, mira si eso ya existe: una escuadra, un perfil, una
           varilla calibrada, una caja de conexiones. En un proyecto de ocho sesiones, cada pieza que
           te ahorras es media sesi&oacute;n que dedicas a que funcione.</p>
      </div>

      <h3>La m&aacute;quina que se imprime a s&iacute; misma</h3>
''' + foto('c2-impresion3d.jpg',
           u'Impresora 3D Prusa i3 de estructura negra con muchas piezas amarillas de pl&aacute;stico '
           u'impreso, imprimiendo un jarr&oacute;n naranja en el que se distinguen las capas',
           u'Una <b>Prusa i3</b>, del proyecto <b>RepRap</b>, imprimiendo un jarr&oacute;n. Dos cosas '
           u'que mirar. La primera, en la pieza naranja: se ven <b>las capas</b>, una encima de otra, '
           u'y eso explica por qu&eacute; una pieza impresa se parte con m&aacute;s facilidad <b>en el '
           u'sentido en que se separan las capas</b> que en cualquier otro. La segunda, y es la '
           u'buena: casi todas las <b>piezas amarillas de la m&aacute;quina</b> &mdash;los soportes de '
           u'las varillas, el carro, el extrusor&mdash; <b>est&aacute;n impresas</b>. RepRap naci&oacute; '
           u'en 2005 en la Universidad de Bath con esa idea: una m&aacute;quina que fabrica la mayor '
           u'parte de las piezas de otra m&aacute;quina igual, con los planos publicados para que '
           u'cualquiera la copie. La tecnolog&iacute;a era de 1984, patentada por Chuck Hull, pero '
           u'estuvo veinte a&ntilde;os en manos de la industria; cuando las patentes fueron caducando y '
           u'apareci&oacute; RepRap, se llen&oacute; de impresoras el mundo. La que hay en tu instituto '
           u'desciende de esta.',
           u'John Abella', u'CC BY 2.0',
           u'https://commons.wikimedia.org/wiki/File:Prusa_i3_-_RepRap_3D_printer_printing.jpg') + u'''
      <div class="copiar">
        <h4>Seguridad, que no es un tr&aacute;mite</h4>
        <ul>
          <li><b>Gafas siempre</b> que haya viruta, taladro o corte. Un ojo no se repara.</li>
          <li><b>La pieza, sujeta</b>: sargento o mordaza. Una pieza peque&ntilde;a sujeta con la mano
              en el taladro se convierte en una h&eacute;lice.</li>
          <li><b>Pelo recogido, mangas cerradas, nada colgando</b> del cuello ni de las mu&ntilde;ecas.</li>
          <li><b>La broca y la pieza reci&eacute;n taladrada queman.</b> Y la boquilla de la impresora
              va a <b>200&nbsp;&deg;C</b>.</li>
          <li><b>Se limpia con un cepillo</b>, nunca con la mano ni soplando.</li>
          <li>Con el l&aacute;ser: <b>extracci&oacute;n encendida y tapa cerrada</b>, y nunca cortar
              PVC &mdash;suelta cloro&mdash; ni nada que no sepas qu&eacute; es.</li>
        </ul>
      </div>
''' + video('s4')

S4_PRACTICA = ficha(
    u'Actividad 4 &middot; La hoja de fabricaci&oacute;n de vuestra pieza',
    [u'CE2 &middot; 2.1', u'CE5 &middot; 5.1'], u'Grupos de 3 &middot; 15 min', u'''
          <h4>Primera parte &middot; Las vueltas del taladro (4 min)</h4>
          <p>En la libreta, con la f&oacute;rmula y todos los pasos:</p>
          <ol>
            <li>&iquest;A qu&eacute; revoluciones hay que taladrar un &empty;8 en contrachapado, con
                V<sub>c</sub> = 40 m/min?</li>
            <li>&iquest;Y un &empty;3 en el mismo material?</li>
            <li>El taladro del aula tiene poleas para 500, 1000, 1500 y 2500 rpm. &iquest;Cu&aacute;l
                eleg&iacute;s para cada uno, y por qu&eacute; se elige <b>por debajo</b> y no por
                encima?</li>
          </ol>
          <h4>Segunda parte &middot; Elegir t&eacute;cnica, con n&uacute;meros (6 min)</h4>
          <p>Coged <b>la pieza m&aacute;s grande</b> de vuestro proyecto y metedla en la escena con sus
             medidas de verdad. Rellenad esta tabla en la libreta:</p>
          <table style="width:100%;border-collapse:collapse;font-size:14px;margin:8px 0">
            <tr><td style="padding:5px 6px;border-bottom:1px solid var(--line)"><b>T&eacute;cnica</b></td>
                <td style="padding:5px 6px;border-bottom:1px solid var(--line)"><b>Coste</b></td>
                <td style="padding:5px 6px;border-bottom:1px solid var(--line)"><b>Tus manos</b></td>
                <td style="padding:5px 6px;border-bottom:1px solid var(--line)"><b>La m&aacute;quina</b></td>
                <td style="padding:5px 6px;border-bottom:1px solid var(--line)"><b>Tolerancia</b></td></tr>
            <tr><td style="padding:5px 6px">A mano</td><td></td><td></td><td></td><td></td></tr>
            <tr><td style="padding:5px 6px">L&aacute;ser</td><td></td><td></td><td></td><td></td></tr>
            <tr><td style="padding:5px 6px">Impresi&oacute;n 3D</td><td></td><td></td><td></td><td></td></tr>
          </table>
          <p>Y decidid, <b>con dos n&uacute;meros de la tabla en la frase</b>. Si en el centro no hay
             l&aacute;ser, decidlo y elegid entre las otras dos: un &laquo;no se puede&raquo; razonado
             vale igual.</p>
          <h4>Tercera parte &middot; Rehacer el dibujo (5 min)</h4>
          <p>Ahora lo importante. Volved al plano de la sesi&oacute;n 1 y <b>escribid dos cambios</b>
             que hay que hacerle para que se pueda fabricar con la t&eacute;cnica que hab&eacute;is
             elegido. Por ejemplo: redondear las esquinas interiores para la sierra, quitar un rebaje
             que el l&aacute;ser no puede hacer, agrandar dos d&eacute;cimas los agujeros para la
             impresora, girar la pieza para que las capas no trabajen a favor de la rotura&hellip;</p>
          <p>Cada cambio, con <b>la raz&oacute;n t&eacute;cnica al lado</b>. Esto es lo que se
             eval&uacute;a de verdad.</p>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Las revoluciones de las dos brocas, con los pasos, y la polea justificada
                <b>(3 puntos)</b>.</li>
            <li>La tabla de las tres t&eacute;cnicas con vuestras medidas <b>(3 puntos)</b>.</li>
            <li>La decisi&oacute;n con dos n&uacute;meros en la frase <b>(1 punto)</b>.</li>
            <li>Los dos cambios en el plano, con su raz&oacute;n t&eacute;cnica <b>(3 puntos)</b>.</li>
          </ul>
''')

S4_TEST = test('c2', u'Lo que tiene que haber quedado de estas cuatro sesiones', [
    dict(p=u'Marcas cuatro agujeros midiendo cada uno desde el anterior, 25 mm cada vez, y te '
           u'equivocas como mucho 0,2 mm en cada medida. En el peor caso, &iquest;d&oacute;nde puede '
           u'acabar el cuarto?',
         op=[u'a 0,2 mm de su sitio, porque ese es el error de una medida',
             u'a 0,8 mm de su sitio',
             u'a 0,05 mm, porque los errores se compensan entre s&iacute;'],
         ok=1,
         por=u'En cadena, cada cota arranca donde acab&oacute; la anterior, as&iacute; que los errores '
             u'se <b>suman</b>: 4 &middot; 0,2 = <b>0,8 mm</b>. Acotando las cuatro desde el mismo '
             u'borde, el peor caso se habr&iacute;a quedado en 0,2 mm.'),

    dict(p=u'&iquest;Por qu&eacute; est&aacute; mal poner en el plano 25 + 25 + 25 + 25 <b>y '
           u'adem&aacute;s</b> el total de 100?',
         op=[u'porque 25 &middot; 4 no es 100',
             u'porque es una cota de m&aacute;s: pide algo que no se puede cumplir y no dice cu&aacute;l '
             u'de las cinco manda',
             u'porque las cotas totales nunca se ponen en un plano'],
         ok=1,
         por=u'Las cuatro medidas reales nunca van a sumar 100 exactos. Al poner las cinco cotas, el '
             u'que fabrica tiene que <b>desobedecer alguna</b> y no le has dicho cu&aacute;l. Se pone '
             u'la que manda; el total, si acaso, entre par&eacute;ntesis y como cota informativa.'),

    dict(p=u'Un agujero va de 8,000 a 8,022 mm y su eje, de 7,972 a 7,987. &iquest;Qu&eacute; ajuste '
           u'es?',
         op=[u'con juego: el m&iacute;nimo es 0,013 y el m&aacute;ximo, 0,050',
             u'indeterminado, porque los n&uacute;meros se solapan',
             u'con apriete: el eje siempre entra forzando'],
         ok=0,
         por=u'Juego m&aacute;ximo = 8,022 &minus; 7,972 = 0,050. Juego m&iacute;nimo = 8,000 &minus; '
             u'7,987 = 0,013. Los <b>dos positivos</b>, as&iacute; que el agujero es siempre mayor que '
             u'el eje: gira, salgan como salgan las piezas.'),

    dict(p=u'&iquest;Qu&eacute; quiere decir que un ajuste sea <b>indeterminado</b>?',
         op=[u'que hay que medirlo para saber cu&aacute;nto mide',
             u'que unas veces las piezas entran sueltas y otras aprietan, y no se puede saber de '
             u'antemano cu&aacute;l toca',
             u'que el plano no lleva tolerancias'],
         ok=1,
         por=u'El juego m&iacute;nimo sale negativo y el m&aacute;ximo, positivo: la zona del eje y la '
             u'del agujero se solapan. El mismo plano da piezas que giran y piezas que no, y eso es '
             u'justo lo que no se puede permitir en una pieza que <b>tiene</b> que girar.'),

    dict(p=u'El juego de un ajuste var&iacute;a entre 0,013 y 0,050 mm. Si aprietas la tolerancia del '
           u'agujero de 22 a 11 micras y no tocas el eje&hellip;',
         op=[u'el juego pasa a variar la mitad, de 0,013 a 0,031',
             u'el juego deja de variar: sale siempre el mismo',
             u'no cambia nada, porque el juego lo marca el eje'],
         ok=0,
         por=u'Lo que var&iacute;a el juego es <b>la suma de las dos tolerancias</b>: 22 + 15 = 37 '
             u'micras, que es justo 0,050 &minus; 0,013. Si el agujero baja a 11, la suma pasa a 26 '
             u'micras y el juego va de 0,013 a 0,039. Baja, pero <b>no a la mitad</b>: la otra '
             u'tolerancia sigue ah&iacute;.'),

    dict(p=u'Un tornillo M3 de acero aguanta unos 1700 N. Lo pones en una pieza de PLA de 3 mm, que '
           u'aguanta 55 N/mm&sup2; de aplastamiento. &iquest;Con cu&aacute;nta fuerza falla la '
           u'uni&oacute;n?',
         op=[u'con 1700 N, que es lo que aguanta el tornillo',
             u'con unos 495 N, y lo que falla es la pieza',
             u'con 165 N, porque hay que dividir entre los 3 mm'],
         ok=1,
         por=u'&sigma; = F / (d &middot; t), as&iacute; que F = 55 &middot; 3 &middot; 3 = '
             u'<b>495 N</b>. Manda <b>siempre el menor de los dos</b> modos de fallo, y en nuestros '
             u'proyectos ese casi nunca es el tornillo: es el material de alrededor del agujero, que '
             u'se ovala.'),

    dict(p=u'&iquest;Por qu&eacute; un remache es una uni&oacute;n fija?',
         op=[u'porque es m&aacute;s fuerte que un tornillo',
             u'porque para ponerlo hay que deformarlo, y esa deformaci&oacute;n no se deshace: para '
             u'quitarlo hay que taladrarlo',
             u'porque va pegado adem&aacute;s de remachado'],
         ok=1,
         por=u'Lo que hace fija una uni&oacute;n no es la fuerza, es que <b>abrirla destruya algo</b>. '
             u'El remache se abre en p&eacute;talos por la cara de detr&aacute;s y no hay manera de '
             u'devolverlo a su forma: hay que taladrarle la cabeza y perderlo.'),

    dict(p=u'Una junta pegada con 20 mm de solape aguanta 2400 N. Si doblas el solape a 40 mm&hellip;',
         op=[u'aguanta lo mismo: lo que manda es el pegamento, no el tama&ntilde;o',
             u'aguanta el doble, unos 4800 N, y no cuesta un c&eacute;ntimo m&aacute;s',
             u'aguanta cuatro veces m&aacute;s'],
         ok=1,
         por=u'En el pegado, &tau; = F / &aacute;rea. Doble &aacute;rea, doble fuerza. Es lineal, no al '
             u'cuadrado, porque solo crece el solape y no el ancho. Y es la &uacute;nica manera de '
             u'ganar resistencia que sale gratis: se gana <b>dibujando</b>.'),

    dict(p=u'&iquest;A qu&eacute; revoluciones va una broca de &empty;8 en contrachapado, con una '
           u'velocidad de corte de 40 m/min?',
         op=[u'unas 1592 rpm',
             u'unas 320 rpm',
             u'unas 5000 rpm, que es lo que da el taladro'],
         ok=0,
         por=u'n = 1000 &middot; V<sub>c</sub> / (&pi; &middot; D) = 40000 / (&pi; &middot; 8) = '
             u'40000 / 25,13 = <b>1592 rpm</b>. F&iacute;jate en que D <b>divide</b>: la broca gorda '
             u'pide menos vueltas, y por eso a las vueltas de una fina quema la madera.'),

    dict(p=u'Necesitas un agujero de &empty;8 con tolerancia de 22 micras para que un eje gire justo. '
           u'Con lo que hay en el aula&hellip;',
         op=[u'lo hace el l&aacute;ser, que clava 0,15 mm',
             u'lo hace la impresora 3D, que clava 0,3 mm',
             u'ninguna de las tres llega: hay que taladrar por debajo y repasar con escariador, y '
             u'comprar el eje ya calibrado'],
         ok=2,
         por=u'22 micras son 0,022 mm. El l&aacute;ser da &plusmn;0,15 y la impresora &plusmn;0,3: '
             u'est&aacute;n <b>un orden de magnitud por encima</b>. Por eso los ejes de un proyecto no '
             u'se fabrican, se compran calibrados, y lo que se ajusta es el agujero, con escariador o '
             u'a lima, midiendo.'),
])

S4_CIERRE = u'''
      <ol>
      ''' + pregunta(
          u'&iquest;Por qu&eacute; se dice que la t&eacute;cnica de fabricaci&oacute;n no se elige al '
          u'final?',
          u'<p>Porque <b>cambia el dibujo</b>. Si va a la sierra, fuera las curvas y redondeo en los '
          u'rincones; si va al l&aacute;ser, todo plano y descontando la sangr&iacute;a; si va a la '
          u'impresora, cuidado con los voladizos y con la orientaci&oacute;n de las capas. Elegirla al '
          u'final obliga a redibujar.</p>') + pregunta(
          u'&iquest;Por qu&eacute; una broca gorda tiene que ir a menos revoluciones que una fina?',
          u'<p>Porque lo que importa es la velocidad del <b>filo</b>, y el filo de una broca gorda '
          u'recorre m&aacute;s camino en cada vuelta. En n = 1000 V<sub>c</sub> / (&pi; D), el '
          u'di&aacute;metro <b>divide</b>: al doble de di&aacute;metro, la mitad de vueltas.</p>'
          ) + pregunta(
          u'&iquest;Por qu&eacute; el tiempo de m&aacute;quina no es lo mismo que el tiempo de tus '
          u'manos?',
          u'<p>Porque la m&aacute;quina se comparte. Cinco minutos tuyos preparando el archivo y treinta '
          u'de impresora parecen treinta y cinco&hellip; hasta que hay diez grupos y una sola '
          u'impresora, y entonces el plazo real es de <b>cinco horas</b>. En un proyecto con fecha, el '
          u'cuello de botella manda m&aacute;s que el coste.</p>') + pregunta(
          u'&iquest;Cu&aacute;l es la pieza m&aacute;s barata de todas?',
          u'<p><b>La que no hay que fabricar.</b> Antes de dibujar, mira si existe: una escuadra, un '
          u'perfil, una varilla calibrada, una caja. Cada pieza que te ahorras es media sesi&oacute;n '
          u'para que el aparato funcione, que es de lo que va el curso.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Lo que llevas hasta aqu&iacute;</span>
        Sabes hacer un plano que otra persona puede fabricar sin preguntarte nada, y sabes elegir
        desde d&oacute;nde se acota y por qu&eacute;. Sabes escribir una cota <b>con su tolerancia</b>
        y calcular si dos piezas van a encajar antes de tocar el material. Sabes decidir c&oacute;mo se
        unen, con la cuenta delante y sabiendo qu&eacute; falla primero. Y sabes qu&eacute; cuesta cada
        t&eacute;cnica y qu&eacute; te obliga a cambiar en el dibujo. <b>Eso ya es un dise&ntilde;o que
        se puede defender, y que se puede fabricar dos veces igual.</b>
      </div>
      <div class="copiar" style="border-color:var(--goo-verde)">
        <h4>Lectura del tema</h4>
        <p>Una sesi&oacute;n entera dedicada a leer y contestar. <b>30 p&aacute;rrafos numerados</b>:
           cada uno lee el suyo en voz alta, en orden. Despu&eacute;s, diez preguntas por escrito.
           Cuenta de d&oacute;nde sale todo esto: un armero franc&eacute;s que mezcl&oacute; las piezas
           en cajones, un ingl&eacute;s que decidi&oacute; c&oacute;mo ten&iacute;an que ser todas las
           roscas del mundo, y lo que pasa cuando dos f&aacute;bricas hacen la misma pieza con dos
           definiciones distintas del metro.</p>
        <p style="margin-top:10px"><a href="lectura-tema2.pdf" target="_blank" rel="noopener"
           style="font-family:var(--f-m);font-size:13px;color:var(--goo-verde);font-weight:500">
           &#8595; Piezas que no se hab&iacute;an visto nunca &middot; PDF</a></p>
      </div>
      <div class="nota">
        <span class="n-tag">Lo que queda</span>
        Quedan cuatro sesiones. Hasta aqu&iacute; todo se ha hecho a l&aacute;piz: falta
        <b>modelarlo en 3D</b> en Tinkercad y sacar de ah&iacute; el plano y el fichero para la
        m&aacute;quina, que es el criterio 5.1. Despu&eacute;s hay que <b>organizar la
        fabricaci&oacute;n</b> &mdash;qui&eacute;n hace qu&eacute;, en qu&eacute; orden y con
        qu&eacute; material&mdash;, <b>montar y ajustar</b>, que es cuando aparecen las piezas que no
        encajan y hay que decidir cu&aacute;l se lima, y por &uacute;ltimo <b>contarlo y
        defenderlo</b>: el expediente del proyecto y la exposici&oacute;n, que es el criterio 3.2 y
        vale tanto como el aparato.
      </div>
'''


# ==========================================================================
# Montaje de la pagina
# ==========================================================================
S1 = (bloque('00', u'Reto inicial &middot; 10 min', S1_RETO) +
      bloque('01', u'Teor&iacute;a &middot; 25 min', S1_TEORIA) +
      bloque('02', u'Pr&aacute;ctica &middot; 20 min', S1_PRACTICA) +
      bloque('03', u'Cierre &middot; 5 min', S1_CIERRE))

S2 = (bloque('00', u'Reto inicial &middot; 10 min', S2_RETO) +
      bloque('01', u'Teor&iacute;a &middot; 25 min', S2_TEORIA) +
      bloque('02', u'Pr&aacute;ctica &middot; 20 min', S2_PRACTICA) +
      bloque('03', u'Cierre &middot; 5 min', S2_CIERRE))

S3 = (bloque('00', u'Reto inicial &middot; 10 min', S3_RETO) +
      bloque('01', u'Teor&iacute;a &middot; 25 min', S3_TEORIA) +
      bloque('02', u'Pr&aacute;ctica &middot; 20 min', S3_PRACTICA) +
      bloque('03', u'Cierre &middot; 5 min', S3_CIERRE))

S4 = (bloque('00', u'Reto inicial &middot; 10 min', S4_RETO) +
      bloque('01', u'Teor&iacute;a &middot; 20 min', S4_TEORIA) +
      bloque('02', u'Pr&aacute;ctica &middot; 15 min', S4_PRACTICA) +
      bloque('03', u'Autoevaluaci&oacute;n &middot; 10 min', S4_TEST) +
      bloque('04', u'Cierre &middot; 5 min', S4_CIERRE))

MIN4 = [(u"10'", u'Reto'), (u"25'", u'Teor&iacute;a'), (u"20'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')]

CH1 = [u'CE2 &middot; 2.1', u'CE3 &middot; 3.1', u'A.2 &middot; A.3.1']
CH2 = [u'CE2 &middot; 2.1 &middot; 2.2', u'A.2.2 &middot; A.3']
CH3 = [u'CE2 &middot; 2.2', u'A.3']
CH4 = [u'CE2 &middot; 2.1 &middot; 2.2', u'CE5 &middot; 5.1', u'A.3 &middot; D.4']

S = [
    dict(corto=u'El plano que se fabrica',
         titulo=u'Cuatro veces veinticinco no son cien',
         entradilla=u'Acotas una tapa en cadena, la fabricas y el &uacute;ltimo agujero se ha ido casi '
                    u'un mil&iacute;metro. Nadie se ha equivocado: se han sumado cuatro errores '
                    u'diminutos.',
         minutado=MIN4, chips=CH1, cuerpo=S1),

    dict(corto=u'Tolerancias y ajustes',
         titulo=u'Dos piezas de ocho mil&iacute;metros que no encajan',
         entradilla=u'Nadie ha fabricado nunca una pieza de 8,000 mm. La pregunta buena no es '
                    u'cu&aacute;nto mide, sino entre qu&eacute; dos n&uacute;meros te vale.',
         minutado=MIN4, chips=CH2, cuerpo=S2),

    dict(corto=u'Uniones',
         titulo=u'Lo que se pega no se repara',
         entradilla=u'El tornillo aguanta 170 kilos y la uni&oacute;n se rompe con quince. No falla el '
                    u'tornillo: falla el material de alrededor del agujero, y eso se calcula.',
         minutado=MIN4, chips=CH3, cuerpo=S3),

    dict(corto=u'Del plano a la pieza',
         titulo=u'La misma tapa, tres maneras de hacerla',
         entradilla=u'Mismo plano, tres presupuestos. Y solo una de las tres te da la cota que pediste '
                    u'&mdash;spoiler: ninguna te da la del eje&mdash;.',
         minutado=[(u"10'", u'Reto'), (u"20'", u'Teor&iacute;a'), (u"15'", u'Pr&aacute;ctica'),
                   (u"10'", u'Test'), (u"5'", u'Cierre')],
         chips=CH4, cuerpo=S4),

    # --- las cuatro que faltan, con el titulo que se propone para cada una ---
    dict(corto=u'Modelarlo en 3D', pendiente=True),
    dict(corto=u'Organizar la fabricaci&oacute;n', pendiente=True),
    dict(corto=u'Montar y ajustar', pendiente=True),
    dict(corto=u'Contarlo y defenderlo', pendiente=True),
]

CFG = dict(
    ruta='4eso/Tecnologia/tema2/',
    migas=u'<a href="../../../">Materiales</a> &middot; <a href="../../">4.&ordm; ESO</a> '
          u'&middot; <a href="../">Tecnolog&iacute;a</a> &middot; Tema 2',
    h1=u'Dise&ntilde;o y fabricaci&oacute;n: del material al producto',
    titulo=u'Tema 2 &middot; Dise&ntilde;o y fabricaci&oacute;n',
    tema=u'Tema 2', curso=u'4.&ordm; de ESO', materia=u'Tecnolog&iacute;a',
    desc=u'Unidad 2 de Tecnolog&iacute;a de 4.&ordm; de ESO: croquis y plano acotado, acotaci&oacute;n '
         u'en cadena frente a acotaci&oacute;n desde una referencia, tolerancias y ajustes, uniones '
         u'fijas y desmontables, y t&eacute;cnicas de fabricaci&oacute;n del aula. Con escenas '
         u'interactivas que calculan.',
    sesiones=S)


if __name__ == '__main__':
    destino = os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema2')
    if not os.path.isdir(destino):
        os.makedirs(destino)
    html = pagina(CFG)
    if USA_AVATAR[0]:
        html = html.replace(u'</style>', avatar_flat.CSS + u'</style>', 1)
    io.open(os.path.join(destino, 'index.html'), 'w', encoding='utf-8', newline='').write(html)
    escritas = sum(1 for x in S if not x.get('pendiente'))
    print('Tema 2 de 4.o generado: %d bytes, %d sesiones (%d escritas, %d pendientes)'
          % (len(html), len(S), escritas, len(S) - escritas))
    for p in PENDIENTES:
        print('  PENDIENTE  ' + p)
