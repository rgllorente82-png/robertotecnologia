# -*- coding: utf-8 -*-
"""4.o de ESO - Tecnologia - Unidad 2: Diseno y fabricacion, del material al producto.

CE2 (2.1, 2.2) / CE3 (3.1, 3.2) / CE5 (5.1). Saberes A.2, A.2.2, A.3, A.3.1, D.4.

La pregunta que abre la unidad: ya sabes que vas a construir y por que. Como se
pasa de un dibujo a una pieza que encaja de verdad con las demas?

Ocho sesiones, las ocho escritas.

  S1  El dibujo que se puede fabricar: croquis, plano acotado y por que una
      pieza acotada en cadena acumula error.
  S2  Tolerancias y ajustes: por que dos piezas "de 8 mm" no encajan.
  S3  Union de piezas: desmontables y fijas, y que falla de verdad cuando una
      union se rompe.
  S4  Del plano a la pieza: las tecnicas del aula y que cambia en el diseno
      segun como se vaya a fabricar.
  S5  Modelarlo en 3D: modelo por operaciones, parametros y lo que le pasa a
      un agujero al exportarlo a STL.
  S6  Organizar la fabricacion: despiece, plan de corte con sangria, orden de
      operaciones y plantillas.
  S7  Montar y ajustar: la cadena de cotas del montaje, la cota de cierre y
      que pieza se lima.
  S8  Contarlo y defenderlo: el expediente de fabricacion, el control
      dimensional y la defensa de tres minutos.

El proyecto del curso YA ESTA DECIDIDO (PROYECTOS.md, 18-sep-2026): el riego
automatico vertebra 4.o y los grupos eligen entre tres - A riego, B aviso de
aula mal ventilada, C lampara de estudio.

  - La PRIMERA MITAD se escribio antes de esa decision, asi que ensena la
    tecnica rotando entre los tres: la tapa de la S1 y de la S4 es la del
    aviso de ventilacion (B), el eje de la S2 es el del deposito del riego
    (A) y la union de la S3 es la del brazo de la lampara (C).
  - La SEGUNDA MITAD aterriza en el proyecto principal: las cuatro sesiones
    siguen una sola pieza, el SOPORTE DEL DEPOSITO del riego (A), desde el
    modelo hasta la defensa. Se modela en la S5, se corta en la S6, se monta
    en la S7 y se mide y se defiende en la S8, y las medidas de cada sesion
    son las que calculo la anterior. Las variantes B y C se recogen en cada
    practica, que es donde cada grupo mete lo suyo.

Fronteras con las unidades de al lado (4.o se escribio en paralelo):
  - El Gantt, el camino critico y la holgura son de la UNIDAD 1, que ya los
    tiene con su escena. Aqui se nombran y se remite alli: lo de esta unidad
    es el orden de las operaciones DE FABRICACION y el cuello de botella de
    la maquina compartida.
  - El material y su impacto son de la UNIDAD 3. Aqui se dice "de
    contrachapado de 4 mm" y se sigue.
  - La S8 defiende LA PIEZA y como se ha hecho. Contar el proyecto entero es
    de la unidad 1; entregarlo, de la 9.

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
from c2_escenas3 import MODELO, CORTE
from c2_escenas4 import CIERRE, CONTROL
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
    # --- las cuatro de la segunda mitad, comprobadas por oEmbed el 18-sep-2026 ---
    's5': dict(vid='pp1Uxy14neU',
               titulo=u'Tutorial completo de Dise&ntilde;o y Modelado 3D con Tinkercad - 2022',
               canal=u'josemariafmTIC',
               nota=u'La herramienta que vais a usar, de cero. Lo que aqu&iacute; interesa es la '
                    u'parte de <b>agrupar y vaciar</b>: es la resta que hace los agujeros.'),
    's6': dict(vid='rL6ZIaso5KA',
               titulo=u'Aplicaci&oacute;n para optimizar cortes de placas de aglomerados y triplay. '
                      u'CutList Optimizer',
               canal=u'Viejo Roble',
               nota=u'Un carpintero usando una herramienta web gratuita que hace exactamente lo que '
                    u'hace la escena de esta sesi&oacute;n, con tableros de verdad. F&iacute;jate en '
                    u'que lo primero que le pide es el <b>ancho de la sierra</b>.'),
    's7': dict(vid='SmvnY4k2vRg',
               titulo=u'Cadenas de Cotas',
               canal=u'AGD Agencia de Gesti&oacute;n Dimensional',
               nota=u'Lo mismo que esta sesi&oacute;n contado por gente que se dedica a esto en la '
                    u'industria. Va m&aacute;s lejos de lo que se pide en 4.&ordm;, pero la idea de '
                    u'la <b>cota que no dibuja nadie</b> est&aacute; en el primer minuto.'),
    's8': dict(vid='CcogpV4DjNs',
               titulo=u'Presentaci&oacute;n oral de un proyecto',
               canal=u'ULLaudiovisual - Universidad de La Laguna',
               nota=u'Est&aacute; hecho para la universidad y se nota en el registro, as&iacute; que '
                    u'qu&eacute;date con la <b>estructura</b> y con lo que hace con las manos y con '
                    u'la voz, no con el vocabulario.'),
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
# SESION 5 - Modelarlo en 3D
# ==========================================================================
S5_RETO = u'''
      <p>Se acab&oacute; el l&aacute;piz. A partir de aqu&iacute; la unidad sigue <b>una sola
         pieza</b> del proyecto principal, el <b>riego autom&aacute;tico</b>: el
         <b>soporte del dep&oacute;sito</b>, esa U de dos flancos y una base por la que pasa el eje
         sobre el que bascula el dep&oacute;sito, y que lleva el servo metido en medio. La vais a
         modelar hoy, a cortar en la sesi&oacute;n que viene, a montar en la siguiente y a defender
         en la &uacute;ltima.</p>
      <p>&iquest;Por qu&eacute; hace falta modelarla, si el plano de la sesi&oacute;n 1 ya estaba
         bien? Por una raz&oacute;n muy tonta: <b>las m&aacute;quinas no leen planos</b>. El
         l&aacute;ser quiere un fichero de l&iacute;neas y la impresora quiere un fichero de
         s&oacute;lido. El plano es para las personas.</p>
      <p>As&iacute; que el grupo abre <b>Tinkercad</b> y hace lo que hace todo el mundo: arrastra
         cajas, las estira hasta que se parecen al dibujo, escribe las medidas a mano en cada una y
         las coloca a ojo. Y queda <b>bien</b>. En la pantalla no se distingue de un modelo hecho por
         un ingeniero.</p>
      <p>Tres d&iacute;as despu&eacute;s llega el paquete con los servos. Y el servo que ha llegado
         mide <b>23 mm</b> de ancho, no los 20 que hab&iacute;ais supuesto.</p>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento</span>
        <p>Es un cambio de <b>tres mil&iacute;metros</b> en una pieza de tu proyecto.
           &iquest;Cu&aacute;ntas medidas del modelo hay que corregir? Escribe tu n&uacute;mero antes
           de seguir, y escribe tambi&eacute;n <b>c&oacute;mo lo sabr&iacute;as</b>.</p>
      </div>
      <p>La respuesta honrada es: <b>no lo sabes</b>. En un modelo hecho de cajas con medidas escritas
         a mano no hay forma de saber cu&aacute;les depend&iacute;an de ese 20. Hay que repasarlas una
         a una, acordarse de por qu&eacute; se puso cada n&uacute;mero, y rezar. El hueco de dentro
         cambia; si cambia el hueco, cambia el ancho de la base; si cambia el ancho de la base,
         cambia el largo de la varilla del eje&hellip; y si a alguien se le escapa una, esa pieza
         sale mal y no te enteras hasta el montaje.</p>
      <p>Hay otra manera de modelar, y es la de esta sesi&oacute;n: en vez de <b>escribir</b> cada
         medida, se <b>deduce</b> de las anteriores. El ancho de la base no es 28,6: es
         <i>hueco m&aacute;s dos espesores</i>. Entonces cambiar el servo de 20 a 23 es mover
         <b>un</b> n&uacute;mero, y las dem&aacute;s medidas se recalculan solas y sin fallo.</p>
      <div class="aviso">
        <span class="n-tag">Y todav&iacute;a hay una segunda sorpresa</span>
        Aunque el modelo est&eacute; perfecto, el agujero que pone <b>&empty;8,30</b> en el modelo
        sale de la impresora <b>m&aacute;s peque&ntilde;o</b>, y el eje de 8 no pasa. No es culpa de
        la impresora ni del modelo: es del <b>fichero que hay en medio</b>. Y eso tambi&eacute;n se
        calcula.
      </div>
'''

S5_TEORIA = u'''
      <h3>Tres maneras de guardar una pieza en un ordenador</h3>
      <div class="copiar">
        <h4>Malla, s&oacute;lido y param&eacute;trico</h4>
        <p><b>Malla</b> (ficheros <b>STL</b>, OBJ, 3MF): la pieza es una <b>piel de tri&aacute;ngulos</b>.
           Dentro no hay ninguna medida: no se le puede preguntar &laquo;&iquest;cu&aacute;nto mide
           este agujero?&raquo;, porque el agujero no existe como tal, solo hay tri&aacute;ngulos
           puestos en c&iacute;rculo. Es lo que <b>comen las m&aacute;quinas</b>.</p>
        <p><b>S&oacute;lido por operaciones</b> (Tinkercad, FreeCAD, Onshape, Fusion): la pieza no es
           una forma, es <b>la lista de lo que has hecho</b>: un prisma, menos un cilindro, m&aacute;s
           un redondeo. Esa lista se llama <b>&aacute;rbol</b>, y se puede volver atr&aacute;s y
           cambiar el paso 2 sin tocar el 3 ni el 4.</p>
        <p><b>Param&eacute;trico</b>: encima de lo anterior, cada medida puede ser una <b>f&oacute;rmula</b>
           que usa otras. Mueves una y se mueve la pieza entera.</p>
        <p>Regla para saber en cu&aacute;l est&aacute;s: <b>&iquest;puedes cambiar una medida sin
           volver a dibujar?</b> Si la respuesta es no, tienes una malla aunque el programa te
           ense&ntilde;e un s&oacute;lido precioso.</p>
      </div>
      <div class="copiar">
        <h4>Modelar por operaciones: cinco verbos y nada m&aacute;s</h4>
        <ul>
          <li><b>Extruir</b>: coges un perfil plano y lo haces crecer en altura. Es el verbo
              principal: casi todas vuestras piezas son un perfil recortado con un espesor.</li>
          <li><b>Revolucionar</b>: giras un perfil alrededor de un eje. Todo lo que sea redondo por
              fuera &mdash;una polea, un casquillo&mdash; sale de aqu&iacute;.</li>
          <li><b>Restar</b>: metes un cuerpo dentro de otro y lo conviertes en hueco. As&iacute; se
              hacen <b>todos</b> los agujeros. En Tinkercad se llama &laquo;agujero&raquo; y luego
              <b>Agrupar</b>.</li>
          <li><b>Unir</b>: dos cuerpos pasan a ser uno solo.</li>
          <li><b>Repetir</b>: simetr&iacute;a y matriz. Los dos flancos del soporte son
              <b>el mismo</b> reflejado, no dos piezas dibujadas dos veces. Si son lo mismo, se
              modelan una vez.</li>
        </ul>
        <p><b>El orden importa</b>, y esa es la diferencia entre el &aacute;rbol y un dibujo. Si
           redondeas la esquina y <b>despu&eacute;s</b> taladras el agujero al lado, al mover el
           agujero el redondeo sigue donde estaba. Al rev&eacute;s, no.</p>
      </div>
      <div class="copiar">
        <h4>Qu&eacute; es par&aacute;metro y qu&eacute; se deduce</h4>
        <p>Esta es la decisi&oacute;n de la sesi&oacute;n, y no es de programa: es de dise&ntilde;o.</p>
        <p><b>Par&aacute;metro es lo que te imponen desde fuera</b> y t&uacute; no puedes cambiar: el
           ancho del servo que hab&eacute;is comprado, el di&aacute;metro de la varilla que venden, el
           espesor del tablero que hay en el almac&eacute;n. Y una m&aacute;s, que s&iacute; eliges
           t&uacute;: la <b>holgura</b> de la sesi&oacute;n 2.</p>
        <p><b>Todo lo dem&aacute;s se deduce.</b> Si una medida la puedes escribir como cuenta de
           otras, <b>no la escribas como n&uacute;mero</b>. En el soporte:</p>
        <ul>
          <li>&empty; del agujero = &empty; del eje + holgura &nbsp;<i>(sesi&oacute;n 2)</i></li>
          <li>distancia del centro al canto = <b>3</b> &times; &empty; del agujero
              &nbsp;<i>(sesi&oacute;n 3: dos di&aacute;metros en pl&aacute;stico o metal y tres en
              madera o tablero, y el soporte es de contrachapado)</i></li>
          <li>lado del flanco = 2 &times; esa distancia</li>
          <li>hueco interior = ancho del servo + 2 holguras</li>
          <li>ancho de la base = hueco + 2 espesores</li>
        </ul>
        <p>Cinco f&oacute;rmulas, y el modelo entero cuelga de cuatro n&uacute;meros. Tinkercad no
           tiene f&oacute;rmulas, as&iacute; que en Tinkercad esa tabla se escribe <b>en la
           libreta</b> y se aplica a mano &mdash;que sigue siendo infinitamente mejor que no
           tenerla&mdash;. FreeCAD y Onshape s&iacute; las tienen.</p>
      </div>
      <p>Al banco. A la izquierda est&aacute; el modelo que se recalcula; a la derecha, las piezas que
         ya se cortaron con las medidas del primer d&iacute;a. Pulsa <b>Llega el servo de verdad</b>
         antes que nada.</p>
''' + MODELO + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p><b>Por qu&eacute; encoge el agujero, con la cuenta delante.</b> Un fichero STL solo sabe
           guardar tri&aacute;ngulos planos, as&iacute; que al exportar, el programa sustituye cada
           c&iacute;rculo por un <b>pol&iacute;gono de N lados metido dentro</b> de &eacute;l. El
           pol&iacute;gono toca la circunferencia en los v&eacute;rtices y por el medio de cada lado se
           queda hacia dentro.</p>
        <p>Lo que de verdad deja pasar ese agujero no es su di&aacute;metro D, sino la distancia entre
           dos lados opuestos:</p>
        <p style="font-size:17px;text-align:center;margin:10px 0">
           <b>&empty; &uacute;til = D &middot; cos(180&deg; / N)</b></p>
        <p>Con D = 8,30 y N = 16 salen <b>8,14 mm</b>: de las tres d&eacute;cimas de holgura que
           pediste te quedan <b>1,4</b>. Con N = 8 salen 7,67, y el eje de 8 <b>ya no pasa</b>. El
           agujero es el mismo en el modelo; lo que ha cambiado es c&oacute;mo se ha guardado.</p>
        <p>De ah&iacute; salen las dos costumbres del taller: <b>subir la resoluci&oacute;n</b> al
           exportar (en Tinkercad, exportar en &laquo;alta calidad&raquo;) y <b>agrandar los agujeros
           dos o tres d&eacute;cimas</b> en el modelo, que es lo que ya se dijo en la sesi&oacute;n 4
           sin explicar por qu&eacute;.</p>
        <p>Ojo: esto le pasa <b>al STL</b>, no al corte 2D. Los ficheros del l&aacute;ser
           &mdash;<b>DXF</b> y <b>SVG</b>&mdash; s&iacute; saben guardar arcos de verdad. All&iacute;
           el problema es otro, y ya lo viste: la <b>sangr&iacute;a</b> del haz.</p>
      </div>

      <h3>El &aacute;rbol, visto por dentro</h3>
''' + foto('c2-cad-arbol.png',
           u'Ventana de FreeCAD: a la izquierda, el &aacute;rbol del modelo con Body, Pad, Sketch, '
           u'Pocket, Mirrored, Pad001 y Pocket001; a la derecha, en 3D, un soporte gris con dos patas '
           u'y una ventana cuadrada en el centro',
           u'<b>FreeCAD</b> con un soporte mec&aacute;nico terminado. Lo importante no est&aacute; en '
           u'la pieza: est&aacute; en la <b>lista de la izquierda</b>. Se lee de arriba abajo y es '
           u'exactamente lo que se hizo, en orden: un <i>Sketch</i> (un perfil plano), un <i>Pad</i> '
           u'(extruirlo), un <i>Pocket</i> (restar), un <i>Mirrored</i> (repetir en espejo, que es la '
           u'pata de la derecha), otro <i>Pad</i> y otro <i>Pocket</i>. Esa lista <b>es</b> la pieza: '
           u'si abres el primer <i>Sketch</i> y cambias una cota, todo lo de abajo se vuelve a '
           u'calcular. Por eso a esto se le llama modelado <b>por operaciones</b> y no dibujo. '
           u'FreeCAD es libre y gratuito, y hace lo mismo que los programas de pago de la industria. '
           u'Esta imagen es el <b>&uacute;ltimo fotograma</b> de una animaci&oacute;n publicada en '
           u'Commons, recortado para poder leer el &aacute;rbol.',
           u'Donatello29', u'CC BY-SA 4.0',
           u'https://commons.wikimedia.org/wiki/File:Parametric_and_feature-based_modeling_example.gif'
           ) + foto('c2-stl-malla.png',
           u'Pieza en 3D con forma de copa o pomo, gris sobre fondo azul, con toda la superficie '
           u'cubierta de tri&aacute;ngulos peque&ntilde;os que se ven uno a uno',
           u'Y esto es lo que sale al exportar a <b>STL</b>. La pieza de arriba, con su &aacute;rbol y '
           u'sus cotas, se convierte en <b>esto</b>: una bolsa de tri&aacute;ngulos. F&iacute;jate en '
           u'el borde del hueco de la izquierda, donde se ven las caras de canto: lo que parec&iacute;a '
           u'una circunferencia es un <b>pol&iacute;gono</b>. Aqu&iacute; ya no hay agujeros, ni '
           u'cotas, ni orden de operaciones, ni manera de cambiar una medida: hay v&eacute;rtices. '
           u'Por eso <b>el STL no se guarda como copia de seguridad</b> del dise&ntilde;o. El STL es '
           u'el fichero que le das a la m&aacute;quina, como el PDF que mandas a imprimir; el modelo '
           u'de verdad es el otro, y ese es el que hay que conservar.',
           u'Kaboldy', u'CC BY-SA 3.0',
           u'https://commons.wikimedia.org/wiki/File:STL_sample_2.png') + u'''
      <div class="copiar">
        <h4>Antes de darle al bot&oacute;n de exportar</h4>
        <ul>
          <li><b>Unidades en mil&iacute;metros y escala 1:1.</b> La mitad de los desastres de
              impresi&oacute;n son piezas exportadas en pulgadas.</li>
          <li><b>Para el l&aacute;ser: SVG o DXF</b>, con los contornos <b>cerrados</b>, sin
              l&iacute;neas dobles (dos veces la misma raya = dos cortes) y con lo que se corta y lo
              que se graba en <b>capas o colores distintos</b>.</li>
          <li><b>Para la impresora: STL</b>, en alta resoluci&oacute;n, y con la pieza
              <b>cerrada</b>: si la malla tiene un agujero, el laminador no sabe qu&eacute; es dentro
              y qu&eacute; es fuera.</li>
          <li><b>Guarda el modelo, no solo el STL.</b> El STL no se puede volver a editar de verdad.</li>
          <li><b>Versi&oacute;n y fecha en el nombre del fichero.</b>
              <i>soporte_v3_2026-10-14.stl</i>, no <i>soporte_bueno_final_este_si.stl</i>.</li>
        </ul>
      </div>

      <h3>De d&oacute;nde sale todo esto</h3>
      <p>La idea de que un dibujo del ordenador guarde <b>relaciones</b> y no solo puntos es de
         <b>1963</b>: <b>Ivan Sutherland</b> present&oacute; en el MIT un programa llamado
         <b>Sketchpad</b> en el que se dibujaba con un l&aacute;piz de luz sobre una pantalla y se le
         pod&iacute;a decir al ordenador <i>&laquo;estas dos l&iacute;neas son perpendiculares&raquo;</i>
         o <i>&laquo;estos dos segmentos miden lo mismo&raquo;</i>. Al mover una, las dem&aacute;s se
         recolocaban solas para seguir cumpliendo lo prometido. Es el antepasado de todo lo que has
         usado hoy.</p>
      <p>Que eso llegara a la industria tard&oacute; otros veinticinco a&ntilde;os: en <b>1987</b>,
         <b>Pro/ENGINEER</b> fue el primer programa comercial en el que las piezas se hac&iacute;an
         con un &aacute;rbol de operaciones y medidas atadas unas a otras. Antes de eso, cambiar una
         cota en un modelo de ordenador costaba casi lo mismo que cambiarla en el papel.</p>
''' + video('s5')

S5_PRACTICA = ficha(
    u'Actividad 5 &middot; Modelar vuestra pieza con par&aacute;metros',
    [u'CE5 &middot; 5.1', u'CE2 &middot; 2.1'], u'Grupos de 3 &middot; 20 min', u'''
          <h4>Primera parte &middot; Las dos cuentas de la escena (6 min)</h4>
          <ol>
            <li>Con los valores de partida, pulsad <b>Llega el servo de verdad</b>. &iquest;Cu&aacute;ntas
                de las siete medidas deducidas cambian? Anotad <b>cu&aacute;les</b>.</li>
            <li>Mirad la caja roja: &iquest;por qu&eacute; hay que volver a cortar? Copiad el
                n&uacute;mero de mil&iacute;metros de interferencia.</li>
            <li>Bajad las facetas a <b>8</b>. Calculad <b>a mano</b>, con la calculadora,
                8,30 &times; cos(180&deg;/8) y comprobadlo con la escena. Repetid con 16 y con 32.</li>
            <li>&iquest;Cu&aacute;ntas facetas hacen falta como m&iacute;nimo para que un eje de 8
                pase por un agujero de 8,30? La escena lo dice: explicad <b>por qu&eacute;</b> ese
                n&uacute;mero y no otro.</li>
          </ol>
          <h4>Segunda parte &middot; Vuestra tabla de par&aacute;metros (5 min)</h4>
          <p>En la libreta, antes de tocar el ordenador. Dos columnas:</p>
          <table style="width:100%;border-collapse:collapse;font-size:14px;margin:8px 0">
            <tr><td style="padding:5px 6px;border-bottom:1px solid var(--line)"><b>Par&aacute;metros</b> (te los imponen)</td>
                <td style="padding:5px 6px;border-bottom:1px solid var(--line)"><b>Deducidas</b> (f&oacute;rmula)</td></tr>
            <tr><td style="padding:5px 6px">&nbsp;</td><td></td></tr>
          </table>
          <p>M&iacute;nimo <b>cuatro par&aacute;metros</b> y <b>cinco f&oacute;rmulas</b>. Si una
             medida no la sab&eacute;is poner como f&oacute;rmula, preguntaos de qu&eacute; depende:
             casi siempre depende de algo.</p>
          <h4>Tercera parte &middot; Tinkercad (9 min)</h4>
          <ol>
            <li>Modelad <b>una</b> pieza de vuestro proyecto (la del riego, la tapa del aviso o el
                brazo de la l&aacute;mpara), con sus agujeros hechos por <b>resta</b> y las piezas
                repetidas por <b>simetr&iacute;a</b>.</li>
            <li>Exportad <b>STL</b> en alta calidad y <b>SVG</b>.</li>
            <li><b>La prueba de verdad</b>: cambiad un par&aacute;metro (el ancho del servo, el
                espesor del tablero) y <b>cronometrad</b> cu&aacute;nto tard&aacute;is en dejar el
                modelo bien otra vez. Anotad el tiempo y qu&eacute; medidas hab&eacute;is tenido que
                tocar.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Las cuatro respuestas de la escena, con la cuenta del coseno hecha a mano
                <b>(3 puntos)</b>.</li>
            <li>La tabla de par&aacute;metros y f&oacute;rmulas <b>(3 puntos)</b>.</li>
            <li>La pieza modelada y los dos ficheros exportados <b>(2 puntos)</b>.</li>
            <li>El cron&oacute;metro de la prueba y la lista de lo que hubo que tocar
                <b>(2 puntos)</b>.</li>
          </ul>
''')

S5_CIERRE = u'''
      <ol>
      ''' + pregunta(
          u'&iquest;Qu&eacute; diferencia hay entre una malla (STL) y un modelo por operaciones?',
          u'<p>La malla es una <b>piel de tri&aacute;ngulos</b>: no guarda medidas, ni agujeros, ni '
          u'el orden de lo que hiciste, as&iacute; que no se puede editar de verdad. El modelo por '
          u'operaciones guarda <b>la lista de lo que hiciste</b>, y por eso puedes volver al paso 2 y '
          u'cambiarlo. El STL es para la m&aacute;quina; el modelo, para ti.</p>') + pregunta(
          u'&iquest;C&oacute;mo se decide si una medida es un par&aacute;metro o se deduce?',
          u'<p>Es par&aacute;metro <b>lo que te imponen desde fuera</b> y no puedes cambiar: el servo '
          u'que hab&eacute;is comprado, la varilla que venden, el espesor del tablero que hay. '
          u'M&aacute;s la holgura, que la eliges t&uacute;. Todo lo dem&aacute;s, si se puede escribir '
          u'como cuenta de otras medidas, <b>se deduce</b>.</p>') + pregunta(
          u'Un agujero de &empty;10 se exporta con 12 facetas. &iquest;Qu&eacute; di&aacute;metro deja '
          u'pasar de verdad?',
          u'<p>&empty; &uacute;til = 10 &middot; cos(180&deg;/12) = 10 &middot; 0,966 = '
          u'<b>9,66 mm</b>. Se han perdido <b>34 cent&eacute;simas</b> por el camino, y eso es '
          u'm&aacute;s que casi cualquier holgura que hayas pedido. Por eso los agujeros se agrandan '
          u'en el modelo y se exporta en alta resoluci&oacute;n.</p>') + pregunta(
          u'&iquest;Por qu&eacute; se guarda el modelo y no solo el STL?',
          u'<p>Porque el STL <b>no se puede volver a editar</b>: no tiene medidas ni historia. Es como '
          u'guardar el PDF y tirar el documento. El d&iacute;a que cambie el servo, con el modelo '
          u'mueves un n&uacute;mero y con el STL empiezas de cero.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya tienes el fichero. Ahora hay <b>diez piezas</b> que salen de un tablero, <b>una sola</b>
        sierra y <b>tres pares de manos</b>. Y hay una manera de perder media sesi&oacute;n sin
        equivocarse en nada: cortar en el orden que vaya saliendo. En la siguiente vas a ver que el
        mismo despiece cabe en <b>un tablero o en dos</b> seg&uacute;n d&oacute;nde pongas las piezas
        antes de cortar la primera, y que hay operaciones que solo se pueden hacer mientras la pieza
        todav&iacute;a es grande.
      </div>
'''


# ==========================================================================
# SESION 6 - Organizar la fabricacion
# ==========================================================================
S6_RETO = u'''
      <p>Lunes, taller. El grupo del riego llega con el fichero de la sesi&oacute;n anterior, una
         plancha de contrachapado de <b>4 mm</b> y muchas ganas. Empiezan por la pieza m&aacute;s
         grande, la tapa de la caja, y la marcan <b>donde cae el l&aacute;piz</b>, m&aacute;s o menos
         por el medio. La cortan. Luego el frente de la caja, que ya no cabe al lado, as&iacute; que
         se va a una esquina. Luego los dos flancos, cada uno donde queda hueco.</p>
      <p>A la quinta pieza no hay ning&uacute;n trozo entero donde quepa la siguiente. Quedan dos
         piezas por cortar y el tablero est&aacute; lleno de <b>recortes con forma de nada</b>.</p>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento</span>
        <p>Las diez piezas del soporte y de su caja suman <b>29 950 mm&sup2;</b>. El retal era de
           300 &times; 200, o sea <b>60 000 mm&sup2;</b>. Sobraba la mitad del tablero.
           &iquest;C&oacute;mo puede ser que no quepan?</p>
      </div>
      <p>Porque el sitio que sobra <b>no est&aacute; junto</b>. Dos recortes de 50 &times; 200 no son
         un hueco de 100 &times; 200: son dos trozos separados por un corte, y una pieza no se puede
         partir en dos. El tablero no se gasta por su superficie, se gasta <b>por d&oacute;nde
         cortas</b>.</p>
      <p>Y hay una segunda cosa, m&aacute;s fina. Los dos flancos ten&iacute;an que ser <b>iguales</b>.
         Como se marcaron por separado &mdash;uno midiendo con la regla y el otro midiendo con la
         regla otra vez&mdash;, salieron con <b>1,5 mm de diferencia</b>. En la sesi&oacute;n 1 ya
         viste por qu&eacute;: cada medida trae su propio error. Lo nuevo es que aqu&iacute; ese error
         se pod&iacute;a haber evitado del todo <b>sin medir mejor</b>.</p>
      <p>As&iacute; que antes del primer corte hay <b>tres cosas</b> que hay que tener decididas: la
         <b>lista</b> de lo que hay que hacer, <b>d&oacute;nde</b> va cada pieza en el tablero, y en
         <b>qu&eacute; orden</b> se hace cada operaci&oacute;n. Ninguna de las tres se improvisa.</p>
'''

S6_TEORIA = u'''
      <div class="copiar">
        <h4>1 &middot; La lista de materiales, o despiece</h4>
        <p>Una fila por pieza distinta, y una columna de <b>cantidad</b>: dos flancos iguales son
           <b>una fila con un &times;2</b>, no dos piezas dibujadas dos veces.</p>
        <table style="width:100%;border-collapse:collapse;font-size:14px;margin:6px 0">
          <tr><td style="padding:4px 6px;border-bottom:1px solid var(--line)"><b>Ref.</b></td>
              <td style="padding:4px 6px;border-bottom:1px solid var(--line)"><b>Pieza</b></td>
              <td style="padding:4px 6px;border-bottom:1px solid var(--line)"><b>Cant.</b></td>
              <td style="padding:4px 6px;border-bottom:1px solid var(--line)"><b>Material</b></td>
              <td style="padding:4px 6px;border-bottom:1px solid var(--line)"><b>Medidas</b></td></tr>
          <tr><td style="padding:4px 6px">S-01</td><td style="padding:4px 6px">base del soporte</td>
              <td style="padding:4px 6px">1</td><td style="padding:4px 6px">contrachapado 4</td>
              <td style="padding:4px 6px">70 &times; 35</td></tr>
          <tr><td style="padding:4px 6px">S-02</td><td style="padding:4px 6px">flanco</td>
              <td style="padding:4px 6px">2</td><td style="padding:4px 6px">contrachapado 4</td>
              <td style="padding:4px 6px">50 &times; 50</td></tr>
        </table>
        <p>Y <b>aparte</b>, la lista de lo que <b>no se fabrica</b>: el servo, la varilla de 8, los
           tornillos M3, las arandelas, el tubo. Van en otra lista porque se <b>compran</b>, y se
           compran con semanas de antelaci&oacute;n.</p>
        <p>La lista se saca <b>del modelo</b>, no de la memoria. Si una pieza no est&aacute; en el
           modelo, no est&aacute; en la lista, y el d&iacute;a del montaje no est&aacute; encima de la
           mesa.</p>
      </div>
      <div class="copiar">
        <h4>2 &middot; El plan de corte</h4>
        <p>Colocar <b>todas</b> las piezas sobre el tablero, en papel, <b>antes de cortar ninguna</b>.
           Cuatro reglas que lo resuelven casi siempre:</p>
        <ul>
          <li><b>Las grandes primero.</b> Una pieza grande solo cabe en un hueco grande; una
              peque&ntilde;a cabe en cualquier sitio. Al rev&eacute;s te quedas sin sitio para la
              grande.</li>
          <li><b>Las de la misma altura, en la misma fila.</b> As&iacute; el tablero se organiza en
              franjas y no en un puzle imposible.</li>
          <li><b>Descontar la sangr&iacute;a</b> entre pieza y pieza: el ancho que la herramienta
              convierte en serr&iacute;n. Con la marqueter&iacute;a, <b>1,5 mm</b> por corte; con la
              sierra de calar, hasta 2,4; con el l&aacute;ser, 0,2. Diez cortes con una sierra de
              calar son <b>dos cent&iacute;metros</b> de tablero que desaparecen.</li>
          <li><b>La veta manda.</b> Si el tablero tiene veta o dibujo, hay piezas que <b>no se pueden
              girar</b>, y entonces el plan sale peor. Se decide antes, no despu&eacute;s.</li>
        </ul>
        <p>Y una que no es de geometr&iacute;a: <b>cortar el encargo de toda la clase de una vez</b>.
           El hueco que le sobra a un grupo le sirve a otro.</p>
      </div>
      <p>Al banco. Es el despiece completo del riego. Sube los grupos de 1 a 10 y mira la caja verde.</p>
''' + CORTE + u'''
      <div class="copiar">
        <h4>3 &middot; El orden de las operaciones, y por qu&eacute; ese</h4>
        <ul>
          <li><b>Marcar todo de una vez</b>, con el tablero entero y desde la cara que manda
              (sesi&oacute;n 1). Marcar a ratos, entre corte y corte, es cambiar de referencia sin
              darte cuenta.</li>
          <li><b>Taladrar antes de recortar.</b> Mientras la pieza sigue pegada al tablero grande hay
              d&oacute;nde poner el sargento. Una pieza de 40 &times; 25 sujeta con la mano debajo de
              una broca es una <b>h&eacute;lice</b>.</li>
          <li><b>Lo que no se puede deshacer, lo m&aacute;s tarde posible</b>: pintar, barnizar,
              pegar, remachar. Si pintas antes de taladrar, la broca te salta la pintura y hay que
              repintar.</li>
          <li><b>Lijar cada pieza antes de montar.</b> Dentro del conjunto ya no entra la lima.</li>
          <li><b>Montaje en seco antes de pegar nada.</b> Se monta entero con dos tornillos flojos,
              se comprueba, y entonces se aprieta. Esto se ve despacio en la sesi&oacute;n
              siguiente.</li>
        </ul>
        <p>La regla que engloba a todas: <b>primero lo que necesita sujeci&oacute;n o referencia, y al
           final lo que no tiene vuelta atr&aacute;s.</b></p>
      </div>
      <div class="copiar">
        <h4>4 &middot; La plantilla, que arregla lo de los dos flancos</h4>
        <p>Cuando hay <b>varias piezas iguales</b>, no se miden varias veces: se hace <b>una
           plantilla</b> (o <b>g&aacute;libo</b>) y se copia.</p>
        <p>Se fabrica con cuidado <b>una vez</b> &mdash;en cart&oacute;n, en contrachapado, en lo que
           sea&mdash;, se comprueba, y a partir de ah&iacute; todas las piezas se marcan
           <b>contra ella</b>. La diferencia es esta: con la regla, cada pieza trae <b>su</b> error, y
           dos flancos pueden salir con 1,5 mm de diferencia. Con la plantilla, <b>todas las piezas
           traen el mismo error</b>, el de la plantilla. Y un error igual en todas es much&iacute;simo
           menos grave que un error distinto en cada una: las piezas siguen encajando entre
           s&iacute;.</p>
        <p>Lo mismo vale para taladrar: una plantilla con los agujeros hechos, puesta encima, y la
           broca entra por donde le dicen. Eso se llama <b>plantilla de taladrado</b> y es lo que
           hace que veinte piezas salgan iguales.</p>
      </div>
''' + foto('c2-galibo.jpg',
           u'Pieza plana de lat&oacute;n dorado con forma estrellada de contornos rectos, en la '
           u'vitrina de un museo, con una etiqueta debajo que pone Gabarit en laiton, y al lado un '
           u'goni&oacute;metro met&aacute;lico antiguo y varios modelos de madera',
           u'Un <b>g&aacute;libo</b> (<i>gabarit</i>) de lat&oacute;n, en el Museo de Historia Natural '
           u'de Nantes, junto a un <b>goni&oacute;metro de Carangeot</b> de principios del siglo XIX y '
           u'unos modelos de madera de formas cristalinas. Es una plantilla, y la idea es la misma que '
           u'la de vuestros flancos: en vez de medir una forma cada vez que hace falta, se fabrica '
           u'<b>una sola vez, con cuidado</b>, y luego se compara o se copia contra ella. Mira el '
           u'canto: est&aacute; recortado en tramos rectos con &aacute;ngulos concretos, porque lo que '
           u'se quiere comprobar con &eacute;l son esos &aacute;ngulos. Un g&aacute;libo convierte una '
           u'medici&oacute;n &mdash;lenta, y distinta cada vez&mdash; en una <b>comparaci&oacute;n</b>, '
           u'que es r&aacute;pida y siempre igual. Es exactamente lo que hac&iacute;a el calibre pasa '
           u'/ no pasa de la sesi&oacute;n 2, pero para una forma entera.',
           u'Koreller', u'CC BY-SA 4.0',
           u'https://commons.wikimedia.org/wiki/File:Mus%C3%A9um_de_Nantes_-_654_-_Gabarit_en_laiton.jpg'
           ) + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p><b>El que manda en el taller no es la gente, es la m&aacute;quina.</b> Sois tres en el
           grupo, pero hay <b>un</b> taladro de columna para toda la clase. Por muy bien que os
           repart&aacute;is el trabajo, las operaciones de taladro van <b>en fila de a uno</b>, y esa
           fila es la que marca cu&aacute;ndo termina todo el mundo.</p>
        <p>De ah&iacute; salen dos costumbres que ahorran sesiones enteras:</p>
        <ul>
          <li><b>Agrupar por m&aacute;quina, no por pieza.</b> Todas las piezas que hay que taladrar,
              taladradas en la misma tanda, con el taladro puesto a las vueltas que toquen
              (sesi&oacute;n 4) y la plantilla ya colocada. Cambiar de broca y volver a ajustar el
              taladro cuesta m&aacute;s que taladrar.</li>
          <li><b>Mientras uno usa la m&aacute;quina, los otros dos no miran.</b> Lijan, marcan la
              pieza siguiente, preparan el montaje en seco. Si los tres est&aacute;is alrededor del
              taladro, el grupo avanza a la velocidad de uno.</li>
        </ul>
        <p>Calcular <b>cu&aacute;ndo</b> termina el proyecto entero, qu&eacute; tareas pueden
           retrasarse sin que pase nada y cu&aacute;les no, es otra cosa y tiene su propia
           herramienta: el diagrama de Gantt, el camino cr&iacute;tico y la holgura. Eso lo
           hicisteis en la <b>unidad 1</b> y aqu&iacute; no se repite. Lo de esta sesi&oacute;n es lo
           que pasa <b>dentro</b> del taller: qu&eacute; operaci&oacute;n va antes que cu&aacute;l y
           por qu&eacute;.</p>
      </div>
      <div class="copiar">
        <h4>La hoja de ruta</h4>
        <p>Una tabla, y cabe en media hoja. Es el documento que convierte todo lo anterior en algo que
           se puede seguir sin pensar el d&iacute;a del taller:</p>
        <table style="width:100%;border-collapse:collapse;font-size:14px;margin:6px 0">
          <tr><td style="padding:4px 6px;border-bottom:1px solid var(--line)"><b>N.&ordm;</b></td>
              <td style="padding:4px 6px;border-bottom:1px solid var(--line)"><b>Operaci&oacute;n</b></td>
              <td style="padding:4px 6px;border-bottom:1px solid var(--line)"><b>Piezas</b></td>
              <td style="padding:4px 6px;border-bottom:1px solid var(--line)"><b>Con qu&eacute;</b></td>
              <td style="padding:4px 6px;border-bottom:1px solid var(--line)"><b>Antes hay que&hellip;</b></td></tr>
          <tr><td style="padding:4px 6px">1</td><td style="padding:4px 6px">marcar el plan de corte</td>
              <td style="padding:4px 6px">todas</td><td style="padding:4px 6px">regla, escuadra, punta</td>
              <td style="padding:4px 6px">&mdash;</td></tr>
          <tr><td style="padding:4px 6px">2</td><td style="padding:4px 6px">granetear los 6 agujeros</td>
              <td style="padding:4px 6px">S-01, S-02</td><td style="padding:4px 6px">granete</td>
              <td style="padding:4px 6px">1</td></tr>
          <tr><td style="padding:4px 6px">3</td><td style="padding:4px 6px">taladrar &empty;8,3 y &empty;3</td>
              <td style="padding:4px 6px">S-01, S-02</td><td style="padding:4px 6px">taladro de columna</td>
              <td style="padding:4px 6px">2</td></tr>
          <tr><td style="padding:4px 6px">4</td><td style="padding:4px 6px">recortar las piezas</td>
              <td style="padding:4px 6px">todas</td><td style="padding:4px 6px">marqueter&iacute;a</td>
              <td style="padding:4px 6px">3</td></tr>
        </table>
        <p>La &uacute;ltima columna es la importante: es la que impide que alguien recorte antes de
           taladrar porque le apetec&iacute;a.</p>
      </div>
''' + video('s6')

S6_PRACTICA = ficha(
    u'Actividad 6 &middot; Despiece, plan de corte y hoja de ruta',
    [u'CE2 &middot; 2.1 &middot; 2.2', u'CE3 &middot; 3.1'], u'Grupos de 3 &middot; 20 min', u'''
          <h4>Primera parte &middot; La escena, con vuestros datos (6 min)</h4>
          <ol>
            <li>Elegid el tablero y la herramienta que de verdad hay en vuestro centro. Anotad
                <b>tableros</b>, <b>aprovechamiento</b> y <b>tiempo de corte</b> con <b>1 grupo</b>.</li>
            <li>Subid a <b>los grupos que sois en clase</b>. Anotad los mismos tres n&uacute;meros y
                los euros de diferencia. &iquest;Cu&aacute;ntos tableros se ahorra la clase?</li>
            <li>Dejad los grupos como estaban y <b>apagad &laquo;Girar las piezas&raquo;</b>.
                &iquest;Cu&aacute;nto baja el aprovechamiento? &iquest;Cu&aacute;ndo pasa eso de
                verdad?</li>
            <li>Comprobad una cuenta a mano: el aprovechamiento es el &aacute;rea de las piezas
                dividida entre el &aacute;rea de los tableros usados. Hacedla con la calculadora y ved
                que sale lo mismo.</li>
          </ol>
          <h4>Segunda parte &middot; Vuestro despiece y vuestro plan (8 min)</h4>
          <ol>
            <li>La <b>tabla de despiece</b> de vuestro proyecto, con referencia, cantidad, material,
                espesor y medidas. Y <b>aparte</b>, la lista de lo que se compra hecho.</li>
            <li>El <b>plan de corte</b> dibujado a escala en papel cuadriculado, con el tablero de
                verdad que ten&eacute;is y <b>dejando la sangr&iacute;a</b> entre pieza y pieza.
                Escribid el aprovechamiento que os sale.</li>
            <li>Se&ntilde;alad qu&eacute; piezas se repiten y decid <b>con qu&eacute; plantilla</b>
                las vais a marcar.</li>
          </ol>
          <h4>Tercera parte &middot; La hoja de ruta (6 min)</h4>
          <p>Escribid las operaciones en orden, con la columna de <b>&laquo;antes hay que&hellip;&raquo;</b>
             rellenada. M&iacute;nimo <b>ocho</b> operaciones. Y contestad por escrito:</p>
          <ol>
            <li>&iquest;Cu&aacute;l es la primera operaci&oacute;n que hay que hacer, y qu&eacute;
                pasar&iacute;a si la hicierais la tercera?</li>
            <li>&iquest;Cu&aacute;l es la &uacute;ltima que <b>no tiene vuelta atr&aacute;s</b>?</li>
            <li>&iquest;Qu&eacute; est&aacute;n haciendo los otros dos mientras uno taladra?</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Los n&uacute;meros de la escena y la comprobaci&oacute;n a mano <b>(2 puntos)</b>.</li>
            <li>El despiece completo, con cantidades y la lista de compras aparte <b>(2 puntos)</b>.</li>
            <li>El plan de corte a escala, con la sangr&iacute;a y el aprovechamiento
                <b>(3 puntos)</b>.</li>
            <li>La hoja de ruta con las dependencias, y las tres preguntas contestadas
                <b>(3 puntos)</b>.</li>
          </ul>
''')

S6_CIERRE = u'''
      <ol>
      ''' + pregunta(
          u'Las piezas suman 29 950 mm&sup2; y el tablero tiene 60 000. &iquest;Por qu&eacute; puede '
          u'no caber?',
          u'<p>Porque el hueco que sobra <b>no est&aacute; junto</b>. Una pieza no se puede partir, '
          u'as&iacute; que lo que cuenta no es la superficie libre total, sino si queda un '
          u'<b>rect&aacute;ngulo entero</b> donde quepa. Por eso el plan de corte se hace antes de '
          u'cortar, empezando por las piezas grandes.</p>') + pregunta(
          u'&iquest;Qu&eacute; es la sangr&iacute;a y por qu&eacute; hay que dejarla en el plan?',
          u'<p>Es el <b>ancho de material que la herramienta convierte en serr&iacute;n</b> en cada '
          u'pasada: 1,5 mm con la marqueter&iacute;a, 2,4 con la de calar, 0,2 con el l&aacute;ser. Si '
          u'colocas las piezas pegadas en el papel, en el tablero no caben: cada corte se come su '
          u'ancho. Y si cortas por el centro de la raya, adem&aacute;s <b>se come media pieza</b>.</p>'
          ) + pregunta(
          u'&iquest;Por qu&eacute; se taladra antes de recortar?',
          u'<p>Porque mientras la pieza sigue pegada al tablero grande <b>hay d&oacute;nde sujetarla</b> '
          u'con el sargento, y porque la referencia desde la que mediste sigue existiendo. Una pieza '
          u'peque&ntilde;a suelta debajo de una broca se convierte en una h&eacute;lice, y ese es un '
          u'accidente, no un contratiempo.</p>') + pregunta(
          u'Ten&eacute;is que hacer cuatro piezas iguales. &iquest;Por qu&eacute; es mejor una '
          u'plantilla que medir cuatro veces?',
          u'<p>Porque midiendo cuatro veces, <b>cada pieza trae su propio error</b> y salen cuatro '
          u'piezas distintas. Con una plantilla, las cuatro traen <b>el mismo</b> error, el de la '
          u'plantilla, y siguen encajando entre s&iacute;. Un error igual en todas estorba mucho menos '
          u'que un error distinto en cada una.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Llegas a la sesi&oacute;n que viene con todas las piezas cortadas y <b>todas dentro de su
        tolerancia</b>: las has medido una a una y no sobra ni falta nada. Y el dep&oacute;sito no va a
        girar. La medida que lo estropea <b>no est&aacute; en ninguno de tus planos</b>, porque no la
        dibuj&oacute; nadie: sale sola de sumar y restar las otras. Y antes de coger la lima hay que
        decidir una cosa que casi siempre se decide mal: <b>cu&aacute;l de las piezas se lima</b>.
      </div>
'''


# ==========================================================================
# SESION 7 - Montar y ajustar
# ==========================================================================
S7_RETO = u'''
      <p>D&iacute;a de montaje. Las piezas del soporte est&aacute;n cortadas, taladradas y lijadas, y
         el grupo ha hecho algo que casi nadie hace: <b>medirlas todas antes de montar</b>. Est&aacute;n
         <b>las cuatro dentro de su tolerancia</b>. No hay ni una mal.</p>
      <div class="aviso">
        <span class="n-tag">Y sin embargo</span>
        En el grupo de Marta, el carrete del dep&oacute;sito <b>no entra</b> entre los dos flancos: hay
        que forzarlo, y una vez dentro no gira.<br>
        En el grupo de Iv&aacute;n entra sin problema, pero <b>baila</b>: el dep&oacute;sito cabecea
        al inclinarse y tira agua fuera de la maceta.<br>
        En el de Nerea va perfecto.<br><br>
        <b>Los tres han fabricado con el mismo plano y las tres piezas est&aacute;n bien medidas.</b>
      </div>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento</span>
        <p>Si todas las piezas cumplen su cota, &iquest;qu&eacute; medida es la que est&aacute;
           fallando? Busca en el plano <b>d&oacute;nde est&aacute; acotado el hueco que queda</b>
           entre el carrete y el flanco. T&oacute;mate un momento antes de seguir.</p>
      </div>
      <p>No est&aacute;. <b>Esa cota no la dibuj&oacute; nadie</b>, y no se puede dibujar, porque no es
         de ninguna pieza: sale de <b>sumar y restar las otras</b>. El hueco entre flancos mide 23,60,
         el carrete 21,60 y las dos arandelas 0,80 cada una, as&iacute; que lo que sobra es
         23,60 &minus; 21,60 &minus; 0,80 &minus; 0,80 = <b>0,40 mm</b>. Ese 0,40 es lo que decide si
         el dep&oacute;sito gira, aprieta o baila, y no aparece en ning&uacute;n plano de ninguna
         pieza.</p>
      <p>En la sesi&oacute;n 1 viste que los errores <b>se suman a lo largo de una cadena de cotas</b>
         dentro de una pieza, y que la soluci&oacute;n era elegir bien la referencia. Aqu&iacute; pasa
         lo mismo&hellip; con una diferencia incómoda: <b>la cadena atraviesa cuatro piezas
         distintas</b>, y la referencia <b>no la eliges t&uacute;</b>. Te la impone el montaje.</p>
'''

S7_TEORIA = u'''
      <div class="copiar">
        <h4>La cadena de cotas y la cota de cierre</h4>
        <p>Se recorre el montaje <b>de un lado a otro, en l&iacute;nea recta</b>, apuntando cada
           medida que te vas encontrando:</p>
        <ul>
          <li>lo que <b>abre</b> hueco, <b>suma</b> (el hueco entre los flancos);</li>
          <li>lo que <b>ocupa</b> hueco, <b>resta</b> (el carrete, las dos arandelas).</li>
        </ul>
        <p>Lo que queda al final se llama <b>cota de cierre</b>, o cota de juego. Es la que de verdad
           te importa y la &uacute;nica que <b>no est&aacute; dibujada</b>.</p>
        <p style="font-size:17px;text-align:center;margin:10px 0">
           <b>J = (suma de las que abren) &minus; (suma de las que ocupan)</b></p>
        <p>Y ahora viene lo que cuesta creerse la primera vez:</p>
        <p style="font-size:17px;text-align:center;margin:10px 0">
           <b>Tolerancia de J = T<sub>1</sub> + T<sub>2</sub> + T<sub>3</sub> + T<sub>4</sub></b></p>
        <p><b>Todas se suman</b>, tengan el signo que tengan. Una cota que resta tambi&eacute;n
           <b>suma</b> su tolerancia. La raz&oacute;n es f&aacute;cil de ver si te lo imaginas: el peor
           caso es que el hueco salga lo m&aacute;s <b>peque&ntilde;o</b> que puede <b>a la vez</b> que
           el carrete sale lo m&aacute;s <b>grande</b> que puede. Los dos errores empujan <b>hacia el
           mismo lado</b>, aunque las cotas tengan signos contrarios.</p>
        <p>Consecuencia que conviene tener grabada: <b>la cota de cierre es siempre la peor de
           todas</b>, y empeora con cada eslab&oacute;n que a&ntilde;ades.</p>
      </div>
      <p>Al banco. Los cuatro eslabones son los del soporte, y la escena monta <b>200 conjuntos</b>
         con piezas sorteadas dentro de su tolerancia para ense&ntilde;arte cu&aacute;ntos salen mal.</p>
''' + CIERRE + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p><b>El peor caso no pasa casi nunca, y aun as&iacute; es con el que se calcula.</b> Que las
           cuatro piezas se vayan al extremo malo <b>a la vez</b> es como sacar cuatro caras seguidas.
           Por eso al lado est&aacute; la otra cuenta, la <b>ra&iacute;z de la suma de los
           cuadrados</b>:</p>
        <p style="font-size:17px;text-align:center;margin:8px 0">
           <b>T<sub>rss</sub> = &radic;(T<sub>1</sub>&sup2; + T<sub>2</sub>&sup2; + T<sub>3</sub>&sup2;
           + T<sub>4</sub>&sup2;)</b></p>
        <p>Con 0,20 / 0,30 / 0,10 / 0,10 sale <b>0,39</b> frente a los 0,70 del peor caso: casi la
           mitad. Se usa cuando se fabrican muchas piezas y se acepta que <b>unas pocas</b> se tiren.
           En una pieza &uacute;nica, como la vuestra, se calcula con el <b>peor caso</b>: no
           ten&eacute;is repuestos.</p>
        <p><b>Y hay dos arreglos distintos, para dos problemas distintos.</b> Es el error que m&aacute;s
           caro sale:</p>
        <ul>
          <li>Si el juego <b>se sale por un lado</b> (siempre aprieta, o siempre baila), lo que
              est&aacute; mal es el <b>nominal</b>. Se arregla <b>moviendo una medida</b>: el hueco a
              24,00, o el carrete a 21,20. Eso mueve la campana entera <b>sin estrecharla</b>, y no
              cuesta dinero.</li>
          <li>Si el juego <b>vale unas veces s&iacute; y otras no</b>, lo que est&aacute; mal es la
              <b>dispersi&oacute;n</b>. Eso solo se arregla <b>apretando una tolerancia</b>, y eso
              s&iacute; cuesta: m&aacute;quina mejor, m&aacute;s tiempo, m&aacute;s piezas tiradas.</li>
        </ul>
        <p>Y hay un tercer arreglo, que es el m&aacute;s barato de todos y el que nadie mira:
           <b>quitar un eslab&oacute;n</b>. Una arandela menos, o una pieza de una sola vez en vez de
           dos atornilladas, es una tolerancia entera que desaparece de la suma.</p>
      </div>

      <h3>El montaje: en qu&eacute; orden y con qu&eacute; cuidado</h3>
      <div class="copiar">
        <h4>Cinco reglas de montaje</h4>
        <ul>
          <li><b>De dentro hacia fuera.</b> Lo que luego no se puede alcanzar va primero. Antes de
              empezar, mirad el modelo y preguntaos: &laquo;despu&eacute;s de este paso,
              &iquest;a qu&eacute; ya no llego?&raquo;.</li>
          <li><b>Montaje en seco</b>, entero, antes de pegar o apretar nada. Se monta con los
              tornillos flojos y sin pegamento, se comprueba que todo cae en su sitio, y
              <b>entonces</b> se termina.</li>
          <li><b>No apretar del todo hasta que est&eacute; todo puesto.</b> Con los tornillos flojos,
              las piezas se colocan solas donde pueden. Si aprietas el primero a tope, obligas a los
              dem&aacute;s a entrar forzando, y ah&iacute; es donde se rompe un agujero.</li>
          <li><b>Apretar en cruz</b>, no en orden: primero uno, luego el de enfrente, luego los otros
              dos. En orden, la pieza se va inclinando y el &uacute;ltimo tornillo no llega.</li>
          <li><b>La prueba de los cinco minutos</b> (sesi&oacute;n 3): &iquest;se puede sacar la placa
              del aparato ya montado en menos de cinco minutos? Ahora es cuando se comprueba de
              verdad, con el aparato delante.</li>
        </ul>
      </div>
      <div class="copiar">
        <h4>Ajustar: qu&eacute; pieza se lima</h4>
        <p>Cuando no encaja, la reacci&oacute;n es coger la lima y atacar lo primero que se ve. Eso
           convierte un ajuste en una pieza nueva. Cinco reglas:</p>
        <ul>
          <li><b>Medir y decidir cu&aacute;nto, antes de tocar la lima.</b> &laquo;A ver si
              as&iacute;&raquo; no es un m&eacute;todo. Se puede <b>quitar</b> material; no se puede
              poner.</li>
          <li><b>Se lima la pieza que no le hace de referencia a nadie m&aacute;s.</b> Si una cara
              apoya, atornilla o sirve de origen para otras medidas, esa no se toca: al limarla mueves
              todo lo que colgaba de ella.</li>
          <li><b>Se lima la m&aacute;s barata de rehacer</b>, por si te pasas. Entre una pieza de
              cart&oacute;n y una impresa de tres horas, no hay duda.</li>
          <li><b>No se lima donde hay una cota funcional.</b> Si el &uacute;nico sitio por donde se
              puede quitar material es una cara que manda, la pieza hay que <b>rehacerla</b>, y se
              dice.</li>
          <li><b>Si sobra hueco, no se lima: se rellena.</b> Una arandela, un suplemento de cart&oacute;n
              o una vuelta de cinta resuelven un juego de tres d&eacute;cimas, y son reversibles.</li>
        </ul>
        <p>Herramientas del ajuste: la <b>lima</b> y el papel de lija, las <b>arandelas y
           suplementos</b>, el <b>escariador</b> de la sesi&oacute;n 4 para afinar un agujero&hellip;
           y la <b>galga de espesores</b>, que es la que dice cu&aacute;nto hueco hay.</p>
      </div>
''' + foto('c2-galgas.jpg',
           u'Juego de galgas de espesores abierto en abanico sobre una piedra, con doce l&aacute;minas '
           u'de acero de distinto grosor; en el mango se lee M/M, Moore &amp; Wright, Sheffield '
           u'England, 389M, y en las l&aacute;minas se distinguen n&uacute;meros grabados como 70, 10 '
           u'y 80',
           u'Un <b>juego de galgas de espesores</b>, abierto en abanico. Cada l&aacute;mina es una '
           u'chapa de acero de un <b>grosor exacto y grabado</b>: la de 0,10 mide 0,10 y la de 0,70 '
           u'mide 0,70. Sirven para medir justo lo que no se puede medir de ninguna otra manera: '
           u'<b>el hueco que queda entre dos piezas ya montadas</b>, donde no entra un pie de rey. Y '
           u'se usan igual que el calibre pasa / no pasa de la sesi&oacute;n 2: se prueban l&aacute;minas '
           u'hasta encontrar <b>la m&aacute;s gorda que entra</b>; el hueco mide eso. Se pueden apilar '
           u'dos o tres para medir huecos mayores. Este juego es del taller: pone <b>M/M</b> porque es '
           u'm&eacute;trico, y son de <i>Moore &amp; Wright</i>, de Sheffield, uno de los sitios '
           u'donde se invent&oacute; buena parte de esto.',
           u'R. Henrik Nilsson', u'CC BY 4.0',
           u'https://commons.wikimedia.org/wiki/File:1970s_feeler_gauge_0_05_1_mm_model_389M_by_Moore_'
           u'and_Wright_Sheffield_England.jpg') + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p><b>Lo que hace la industria cuando la cota de cierre es imposible.</b> Hay conjuntos en los
           que el juego tiene que quedar dentro de <b>dos cent&eacute;simas</b> &mdash;un pist&oacute;n
           dentro de su cilindro, un rodamiento en su alojamiento&mdash; y fabricar todas las piezas
           con esa precisi&oacute;n costar&iacute;a una fortuna.</p>
        <p>La soluci&oacute;n es una idea preciosa y se llama <b>ajuste selectivo</b>: se fabrican las
           piezas con una tolerancia normal, se <b>miden todas</b>, se reparten en <b>clases</b>
           (los pistones un poco grandes con los cilindros un poco grandes) y se montan
           <b>emparejadas por clase</b>. As&iacute; el juego sale fino sin haber fabricado fino.</p>
        <p>Y tiene el precio que ya conoces de la sesi&oacute;n 2: esas piezas <b>dejan de ser
           intercambiables</b>. El repuesto ya no vale por s&iacute; solo, tiene que ser de su clase.
           Dos siglos despu&eacute;s de Honor&eacute; Blanc, la industria sigue negociando entre lo
           mismo: piezas que encajan con cualquiera, o piezas que encajan muy bien.</p>
      </div>
''' + video('s7')

S7_PRACTICA = ficha(
    u'Actividad 7 &middot; La cadena de cotas de vuestro montaje',
    [u'CE2 &middot; 2.2', u'CE3 &middot; 3.1'], u'Grupos de 3 &middot; 20 min', u'''
          <h4>Primera parte &middot; Los tres arreglos, en la escena (7 min)</h4>
          <p>Partiendo de los valores de partida, anotad en una tabla <b>J nominal</b>, <b>el peor
             caso</b> y <b>cu&aacute;ntos de 200 fallan</b> en cada uno de estos cuatro casos:</p>
          <ol>
            <li>Tal cual est&aacute;.</li>
            <li>Apretando el <b>carrete</b> de &plusmn;0,30 a &plusmn;0,10, sin tocar nada m&aacute;s.</li>
            <li>Volviendo atr&aacute;s y apretando las <b>dos arandelas</b> a &plusmn;0,02, sin tocar
                nada m&aacute;s.</li>
            <li>Volviendo atr&aacute;s y subiendo el <b>hueco nominal</b> a 24,00.</li>
          </ol>
          <p>Y contestad: <b>&iquest;cu&aacute;l de los tres arreglos quita las piezas que no entran, y
             cu&aacute;l quita las que bailan?</b> No es el mismo, y ah&iacute; est&aacute; la
             sesi&oacute;n entera.</p>
          <h4>Segunda parte &middot; Vuestra cadena (8 min)</h4>
          <p>Buscad en vuestro proyecto un sitio donde <b>tres o m&aacute;s piezas</b> se apilen o se
             encajen: el eje entre sus soportes, la tapa dentro de su caja, el LED dentro de su
             agujero y su portaled.</p>
          <ol>
            <li>Dibujadla <b>en l&iacute;nea</b>, con una flecha por eslab&oacute;n y su signo.</li>
            <li>Nominal y tolerancia de cada uno (los de las piezas que compr&aacute;is, mirad la hoja
                del fabricante o medidlos).</li>
            <li>Calculad <b>J nominal</b>, <b>J m&aacute;ximo</b> y <b>J m&iacute;nimo</b>, a mano.</li>
            <li>Decid entre qu&eacute; dos valores <b>ten&iacute;a</b> que estar J para que funcione, y
                si vuestro peor caso cabe ah&iacute; dentro.</li>
          </ol>
          <h4>Tercera parte &middot; El arreglo y el orden (5 min)</h4>
          <p>Si no cabe, calculad <b>los tres arreglos</b> &mdash;apretar el eslab&oacute;n que
             m&aacute;s pesa, mover un nominal, quitar un eslab&oacute;n&mdash; y elegid uno,
             <b>con la raz&oacute;n</b>.</p>
          <p>Y escribid el <b>orden de montaje</b> numerado. Detr&aacute;s de cada paso, una frase:
             <b>&laquo;despu&eacute;s de esto ya no puedo tocar&hellip;&raquo;</b>.</p>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>La tabla de los cuatro casos de la escena y la respuesta de cu&aacute;l arregla
                qu&eacute; <b>(3 puntos)</b>.</li>
            <li>Vuestra cadena dibujada con los signos <b>(2 puntos)</b>.</li>
            <li>Los tres c&aacute;lculos de J y la comparaci&oacute;n con lo que hace falta
                <b>(3 puntos)</b>.</li>
            <li>El orden de montaje con la frase de cada paso <b>(2 puntos)</b>.</li>
          </ul>
''')

S7_CIERRE = u'''
      <ol>
      ''' + pregunta(
          u'&iquest;Qu&eacute; es una cota de cierre y por qu&eacute; no est&aacute; dibujada en '
          u'ning&uacute;n plano?',
          u'<p>Es <b>el hueco que queda</b> al montar, y no es de ninguna pieza: sale de sumar las '
          u'medidas que abren hueco y restar las que lo ocupan. Como no pertenece a ninguna pieza, '
          u'nadie la acota&hellip; y es justo la que decide si el conjunto funciona.</p>') + pregunta(
          u'&iquest;Por qu&eacute; se suman TODAS las tolerancias, tambi&eacute;n las de las cotas que '
          u'restan?',
          u'<p>Porque el peor caso es que el hueco salga lo m&aacute;s peque&ntilde;o posible <b>a la '
          u'vez</b> que lo que va dentro sale lo m&aacute;s grande posible. Los dos errores empujan '
          u'<b>al mismo lado</b> aunque las cotas tengan signos contrarios. Por eso la cota de cierre '
          u'es siempre la peor de la cadena.</p>') + pregunta(
          u'El montaje unas veces aprieta y otras baila. &iquest;Se arregla moviendo un nominal o '
          u'apretando una tolerancia?',
          u'<p><b>Apretando una tolerancia</b>, y la que m&aacute;s pese. Mover el nominal '
          u'<b>desplaza</b> el juego entero hacia un lado, pero no lo estrecha: si antes val&iacute;a '
          u'a veces, seguir&aacute; valiendo a veces. Mover el nominal arregla el caso contrario: el '
          u'que <b>siempre</b> aprieta o <b>siempre</b> baila.</p>') + pregunta(
          u'Dos piezas no encajan. &iquest;Cu&aacute;l se lima?',
          u'<p>La que <b>no le hace de referencia a nadie</b> y la m&aacute;s barata de rehacer; nunca '
          u'la cara que apoya, atornilla o sirve de origen a otras cotas. Y antes de limar, <b>se mide '
          u'y se decide cu&aacute;nto</b>: material se puede quitar, no se puede poner. Si sobra hueco, '
          u'mejor rellenar con una arandela que limar.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya gira. Y ahora llega la pregunta que hunde a la mitad de los proyectos buenos:
        <b>&laquo;&iquest;c&oacute;mo s&eacute; que no ha sido suerte?&raquo;</b>. Ense&ntilde;ar la
        pieza y decir que funciona no demuestra nada: tiene que funcionar <b>por lo que t&uacute;
        dijiste que iba a funcionar</b>. En la &uacute;ltima sesi&oacute;n se monta el expediente de
        fabricaci&oacute;n, se mide la pieza contra su propio plano y se prepara una defensa de tres
        minutos en la que <b>cada frase lleva un n&uacute;mero</b>.
      </div>
'''


# ==========================================================================
# SESION 8 - Contarlo y defenderlo
# ==========================================================================
S8_RETO = u'''
      <p>&Uacute;ltima sesi&oacute;n de la unidad. El soporte est&aacute; terminado, el dep&oacute;sito
         bascula y el servo lo mueve. El grupo lo pone encima de la mesa y dice la frase que se dice
         siempre:</p>
      <div class="aviso">
        <span class="n-tag">La defensa entera, palabra por palabra</span>
        <b>&laquo;Pues esto es el soporte. Nos ha quedado muy bien y funciona.&raquo;</b>
      </div>
      <p>Y entonces les hacen tres preguntas:</p>
      <ol>
        <li>&iquest;Qu&eacute; medida <b>pediste</b> en el hueco entre los flancos, y cu&aacute;nto te
            ha <b>salido</b>?</li>
        <li>&iquest;Por qu&eacute; esa uni&oacute;n es de tornillo y no est&aacute; pegada?</li>
        <li>Si tuvieras que hacer <b>otro igual</b> ma&ntilde;ana, &iquest;te saldr&iacute;a igual?</li>
      </ol>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento</span>
        <p>La pieza funciona. Est&aacute; ah&iacute; y se puede tocar. &iquest;Por qu&eacute; no basta
           con eso? Escribe una raz&oacute;n antes de seguir.</p>
      </div>
      <p>Hay tres razones, y las tres son incómodas:</p>
      <ul>
        <li><b>Funcionar no demuestra que est&eacute; bien hecha.</b> La pieza de Nerea de la
            sesi&oacute;n anterior tambi&eacute;n funcionaba, y funcionaba <b>por suerte</b>: le
            toc&oacute; el lado bueno de la tolerancia. La de al lado, con el mismo plano, no.</li>
        <li><b>Si no sabes qu&eacute; pediste, no puedes repetirlo.</b> Una pieza que no se puede
            volver a hacer igual no es un dise&ntilde;o: es un accidente afortunado.</li>
        <li><b>Si no sabes cu&aacute;nto te has desviado, no sabes qu&eacute; mejorar.</b> No puedes
            decir si el problema es la m&aacute;quina, el plano o el pulso.</li>
      </ul>
      <p>Una pieza no se defiende ense&ntilde;&aacute;ndola. Se defiende con <b>la prueba de que hace lo
         que dijiste que iba a hacer</b>, y esa prueba son <b>n&uacute;meros</b>: lo que pediste, lo
         que mediste, y la diferencia.</p>
      <div class="nota">
        <span class="n-tag">De qu&eacute; va esta sesi&oacute;n, y de qu&eacute; no</span>
        Aqu&iacute; se defiende <b>la pieza y c&oacute;mo se ha fabricado</b>: las tolerancias que
        pediste, las que te han salido, qu&eacute; hubo que limar y por qu&eacute;. Contar el
        <b>proyecto entero</b> &mdash;el problema del que naci&oacute;, la soluci&oacute;n, lo que
        aporta&mdash; se prepar&oacute; en la <b>unidad 1</b>, y la entrega final es de la
        <b>unidad 9</b>. Son tres cosas distintas y se preparan por separado.
      </div>
'''

S8_TEORIA = u'''
      <div class="copiar">
        <h4>El expediente de fabricaci&oacute;n: cinco hojas</h4>
        <p>Es lo que en la industria acompa&ntilde;a a cada pieza. Una hoja cada uno, ni m&aacute;s:</p>
        <ol>
          <li><b>El plano final</b>, acotado y con tolerancias. El <b>de verdad</b>, con los cambios de
              la sesi&oacute;n 4 y de la 5 ya metidos, con su cajet&iacute;n, su <b>versi&oacute;n</b>
              y su fecha. Si no lleva versi&oacute;n, alguien fabricar&aacute; el viejo.</li>
          <li><b>El despiece y el plan de corte</b> de la sesi&oacute;n 6, tal como se
              ejecut&oacute;.</li>
          <li><b>La hoja de ruta</b>, con lo que <b>de verdad</b> pas&oacute;: en qu&eacute; orden se
              hizo y qu&eacute; hubo que repetir.</li>
          <li><b>El control dimensional</b>: la tabla de lo que se pidi&oacute; frente a lo que se
              midi&oacute;.</li>
          <li><b>Las incidencias</b>: qu&eacute; fall&oacute;, qu&eacute; se cambi&oacute; y por
              qu&eacute;. Es la hoja <b>m&aacute;s valiosa de las cinco</b> y la que nadie escribe.
              Un proyecto sin incidencias no es un proyecto perfecto: es un proyecto que no se ha
              mirado.</li>
        </ol>
      </div>
      <div class="copiar">
        <h4>La tabla de control dimensional</h4>
        <p>Cinco columnas. Se rellena con la pieza en una mano y el pie de rey en la otra:</p>
        <table style="width:100%;border-collapse:collapse;font-size:14px;margin:6px 0">
          <tr><td style="padding:4px 6px;border-bottom:1px solid var(--line)"><b>Cota</b></td>
              <td style="padding:4px 6px;border-bottom:1px solid var(--line)"><b>Nominal y tolerancia</b></td>
              <td style="padding:4px 6px;border-bottom:1px solid var(--line)"><b>Medido</b></td>
              <td style="padding:4px 6px;border-bottom:1px solid var(--line)"><b>Desviaci&oacute;n</b></td>
              <td style="padding:4px 6px;border-bottom:1px solid var(--line)"><b>Veredicto</b></td></tr>
          <tr><td style="padding:4px 6px">hueco entre flancos</td>
              <td style="padding:4px 6px">23,60 &plusmn; 0,20</td><td style="padding:4px 6px">23,50</td>
              <td style="padding:4px 6px">&minus;0,10 (50 %)</td><td style="padding:4px 6px">pasa</td></tr>
        </table>
        <p>Dos cosas que parecen detalles y no lo son:</p>
        <ul>
          <li>La desviaci&oacute;n se pone <b>tambi&eacute;n en porcentaje de la tolerancia</b>. Un
              &laquo;pasa&raquo; al 20 % y un &laquo;pasa&raquo; al 95 % son dos cosas muy distintas, y
              la segunda te va a dar un disgusto en la siguiente pieza.</li>
          <li>Se apunta <b>con qu&eacute; se ha medido</b>. Una medida sin instrumento no es una
              medida, y la regla de la sesi&oacute;n 2 sigue valiendo: el instrumento tiene que
              apreciar del orden de <b>diez veces menos</b> que la tolerancia que compruebas.</li>
        </ul>
      </div>
      <p>Al banco. Es tu soporte, con las seis cotas que sali&oacute;n del modelo de la sesi&oacute;n
         5, fabricado y medido.</p>
''' + CONTROL + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p><b>Desajuste y dispersi&oacute;n no son lo mismo, y se arreglan de maneras opuestas.</b></p>
        <ul>
          <li>El <b>desajuste</b> (o error sistem&aacute;tico) empuja <b>todas</b> las medidas al mismo
              lado: el que sierra va siempre por fuera de la raya, el tope est&aacute; corrido, el
              cero del pie de rey no est&aacute; en el cero. Se ve en que los puntos de la escena
              se van todos juntos, y <b>se corrige</b>: mueves el tope y desaparece.</li>
          <li>La <b>dispersi&oacute;n</b> es que cada medida cae donde le da la gana dentro de un
              margen. No se corrige: <b>se aguanta o se cambia de m&aacute;quina</b>.</li>
        </ul>
        <p>Y de ah&iacute; sale la conclusi&oacute;n que cierra la unidad entera, y que no es una
           excusa sino un diagn&oacute;stico: <b>si la tolerancia que escribiste es m&aacute;s
           estrecha que la dispersi&oacute;n de tu m&aacute;quina, la culpa es del plano, no de las
           manos</b>. Ese plano ped&iacute;a algo que nadie pod&iacute;a cumplir con esa
           m&aacute;quina, y eso se decidi&oacute; en la sesi&oacute;n 4, no en el taller. Decirlo en
           la defensa, con el n&uacute;mero delante, vale m&aacute;s que ense&ntilde;ar una pieza
           perfecta.</p>
      </div>

      <h3>C&oacute;mo se mide esto cuando hay dinero de por medio</h3>
''' + foto('c2-cmm.jpg',
           u'Un t&eacute;cnico con guante blanco maneja una m&aacute;quina de medici&oacute;n por '
           u'coordenadas: un palpador desciende sobre una pieza cil&iacute;ndrica de aluminio marcada '
           u'a rotulador rojo, y en la pantalla de al lado se ve la misma pieza en 3D con un mapa de '
           u'colores y una escala que va de -0,02 a +0,02',
           u'Una <b>m&aacute;quina de medici&oacute;n por coordenadas</b> (CMM) en un laboratorio del '
           u'NIST, el instituto de metrolog&iacute;a de Estados Unidos. Es la tabla de control '
           u'dimensional convertida en m&aacute;quina: el palpador va tocando la pieza punto por punto '
           u'y el ordenador compara <b>cada punto medido con el modelo 3D</b> de la sesi&oacute;n 5. '
           u'Mira la pantalla de la izquierda: la pieza est&aacute; pintada por colores, y la '
           u'<b>escala de la derecha va de &minus;0,02 a +0,02</b> mil&iacute;metros. Eso no es un '
           u'dibujo bonito: es la <b>desviaci&oacute;n</b>, cota a cota, de la pieza real respecto a '
           u'lo que ped&iacute;a el plano, que es exactamente la columna que est&aacute;s rellenando '
           u't&uacute; con el pie de rey. Y f&iacute;jate en el rotulador rojo sobre el aluminio: la '
           u'pieza lleva escrito <b>su n&uacute;mero</b>, porque un informe de medici&oacute;n que no '
           u'dice de qu&eacute; pieza es no sirve para nada.',
           u'National Institute of Standards and Technology (NIST)', u'dominio p&uacute;blico',
           u'https://commons.wikimedia.org/wiki/File:Coordinate_Measuring_Machines_(5885465714).jpg'
           ) + u'''
      <div class="copiar">
        <h4>La defensa, en tres minutos</h4>
        <p>Tres minutos son <b>muy poco</b>, y por eso hay que repartirlos antes:</p>
        <ul>
          <li><b>20 s &middot; Qu&eacute; pieza es y qu&eacute; tiene que hacer.</b> Una frase, con un
              n&uacute;mero dentro. &laquo;Es el soporte del dep&oacute;sito; tiene que dejarlo girar
              y aguantar el litro de agua lleno.&raquo;</li>
          <li><b>60 s &middot; La decisi&oacute;n que m&aacute;s cost&oacute;.</b> Una sola, con
              <b>la alternativa que descartasteis</b> y el <b>n&uacute;mero que la descart&oacute;</b>.
              Esto es lo que se eval&uacute;a de verdad.</li>
          <li><b>60 s &middot; Lo que pedisteis y lo que med&iacute;s.</b> Dos o tres cotas de la
              tabla, no las seis. Con la desviaci&oacute;n y el porcentaje.</li>
          <li><b>30 s &middot; Qu&eacute; sali&oacute; mal y qu&eacute; har&iacute;ais distinto.</b>
              Con una cifra.</li>
          <li><b>10 s &middot; Una pregunta que dej&aacute;is abierta.</b> Lo que no os ha dado tiempo
              a comprobar.</li>
        </ul>
        <p>Cuatro reglas mientras habl&aacute;is:</p>
        <ul>
          <li><b>Un n&uacute;mero por frase, y de d&oacute;nde sale.</b> &laquo;Aguanta 495 N, que
              salen de 55 por 3 por 3&raquo;, no &laquo;aguanta bastante&raquo;.</li>
          <li><b>La pieza y el plano, a la vez.</b> Se se&ntilde;ala en la pieza y se se&ntilde;ala en
              el plano. Sin el plano delante, todo suena a opini&oacute;n.</li>
          <li><b>No se lee.</b> Se puede llevar una tarjeta con los n&uacute;meros; leer un texto
              seguido se nota a la primera frase.</li>
          <li><b>Lo que no sab&eacute;is, se dice.</b> &laquo;No lo hemos medido&raquo; es una
              respuesta profesional. Inventarse un n&uacute;mero delante de alguien que sabe es la
              &uacute;nica manera segura de suspender.</li>
        </ul>
      </div>
      <div class="copiar">
        <h4>Las cinco preguntas que os van a hacer</h4>
        <p>Son siempre las mismas, as&iacute; que se llevan preparadas <b>con su n&uacute;mero</b>:</p>
        <ol>
          <li>&iquest;Por qu&eacute; ese material y esa uni&oacute;n, y no otra?</li>
          <li>&iquest;Qu&eacute; tolerancia pediste ah&iacute;, y por qu&eacute; esa y no m&aacute;s
              ancha?</li>
          <li>&iquest;C&oacute;mo sabes que la cumple? &iquest;Con qu&eacute; lo has medido?</li>
          <li>Si se rompe esa pieza, &iquest;c&oacute;mo se cambia? &iquest;Cu&aacute;nto se tarda?</li>
          <li>&iquest;Cu&aacute;nto ha costado, en euros y en sesiones?</li>
        </ol>
      </div>
''' + video('s8')

S8_PRACTICA = ficha(
    u'Actividad 8 &middot; El expediente y la defensa de tres minutos',
    [u'CE3 &middot; 3.1 &middot; 3.2', u'CE2 &middot; 2.2'], u'Grupos de 3 &middot; 15 min', u'''
          <h4>Primera parte &middot; La escena, con vuestra t&eacute;cnica (4 min)</h4>
          <ol>
            <li>Elegid la t&eacute;cnica con la que hab&eacute;is fabricado de verdad. Anotad
                <b>cu&aacute;ntas cotas pasan</b> y cu&aacute;ntas tienen la tolerancia m&aacute;s
                estrecha que la dispersi&oacute;n de esa m&aacute;quina.</li>
            <li>Mueve el desajuste a +0,30. &iquest;Qu&eacute; les pasa a los seis puntos? &iquest;Y
                si en vez de eso cambias de t&eacute;cnica?</li>
            <li>Copiad la frase que genera la escena y <b>cambiadle los n&uacute;meros</b> por los de
                una cota vuestra. Esa es la plantilla de vuestra defensa.</li>
          </ol>
          <h4>Segunda parte &middot; Medir de verdad (5 min)</h4>
          <p>Con la pieza y el pie de rey (o la regla, si no hay otra cosa):</p>
          <ol>
            <li>Elegid <b>tres cotas</b> de vuestra pieza, de las que import&oacute; en el montaje.</li>
            <li>Medid cada una <b>tres veces</b>, quitando y volviendo a poner el instrumento.
                Apuntad las tres lecturas.</li>
            <li>Rellenad la tabla de control dimensional con la media, la desviaci&oacute;n, el
                porcentaje de la tolerancia y el veredicto.</li>
            <li>La diferencia entre vuestra lectura m&aacute;s alta y la m&aacute;s baja es
                <b>vuestra</b> incertidumbre. Escribidla al pie de la tabla. Si es mayor que la
                tolerancia, vuestro veredicto <b>no vale</b>, y hay que decirlo.</li>
          </ol>
          <h4>Tercera parte &middot; Ensayar, con cron&oacute;metro (6 min)</h4>
          <p>Por parejas de grupos. Uno defiende <b>tres minutos</b> con el reparto de arriba; el otro
             cronometra y al final hace <b>dos</b> de las cinco preguntas. Luego al rev&eacute;s.</p>
          <p>El que escucha anota tres cosas: <b>cu&aacute;ntos n&uacute;meros</b> ha dicho el que
             habla, <b>cu&aacute;ntos</b> ven&iacute;an con su origen, y <b>en qu&eacute; momento</b>
             se le fue el tiempo.</p>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Las tres respuestas de la escena y la frase adaptada <b>(2 puntos)</b>.</li>
            <li>La tabla de control dimensional con las tres lecturas y la incertidumbre
                <b>(3 puntos)</b>.</li>
            <li>El expediente completo, las cinco hojas, con la de incidencias escrita de verdad
                <b>(3 puntos)</b>.</li>
            <li>La defensa ensayada: dentro de tiempo y con los n&uacute;meros con su origen
                <b>(2 puntos)</b>.</li>
          </ul>
''')

S8_TEST = test('c2b', u'Lo que tiene que haber quedado de la unidad entera', [
    dict(p=u'Tienes cuatro agujeros acotados <b>desde el mismo borde</b>, con &plusmn;0,2 mm de error '
           u'en cada medida. &iquest;Cu&aacute;nto se puede desviar el cuarto en el peor caso?',
         op=[u'0,8 mm, porque son cuatro medidas',
             u'0,2 mm, y no crece aunque a&ntilde;adas veinte agujeros m&aacute;s',
             u'0,4 mm, la mitad que en cadena'],
         ok=1,
         por=u'Acotando desde una referencia, cada cota sale de la misma cara y <b>solo carga con su '
             u'propio error</b>. El que crece con el n&uacute;mero de cotas es el de la '
             u'acotaci&oacute;n en cadena, donde cada una arranca donde acab&oacute; la anterior.'),

    dict(p=u'En un plano, &iquest;qu&eacute; quiere decir &empty;8 <sup>+0,022</sup><sub>&nbsp;0</sub>?',
         op=[u'que la pieza mide 8,022 mm',
             u'que vale cualquier pieza entre 8,000 y 8,022, y que la tolerancia es de 22 micras',
             u'que hay que fabricarla con un error m&aacute;ximo del 0,022 %'],
         ok=1,
         por=u'La medida &uacute;til no es un n&uacute;mero, es un <b>intervalo</b>: la nominal m&aacute;s '
             u'cada desviaci&oacute;n. La tolerancia es la anchura de ese permiso, 8,022 &minus; 8,000 '
             u'= 0,022 mm = 22 &micro;m, y siempre es positiva.'),

    dict(p=u'Una uni&oacute;n atornillada con un M3 en una pieza de DM de 3 mm (12 N/mm&sup2; de '
           u'aplastamiento). &iquest;Con cu&aacute;nta fuerza falla?',
         op=[u'con 1700 N, que es lo que aguanta el tornillo',
             u'con 108 N, y lo que falla es el DM alrededor del agujero',
             u'con 36 N'],
         ok=1,
         por=u'&sigma; = F / (d &middot; t), as&iacute; que F = 12 &middot; 3 &middot; 3 = <b>108 N</b>. '
             u'Manda <b>siempre el menor de los dos</b> modos de fallo, y con material blando ese '
             u'nunca es el tornillo. Un ni&ntilde;o de 11 kg colgando ya lo rompe.'),

    dict(p=u'&iquest;Por qu&eacute; la t&eacute;cnica de fabricaci&oacute;n no se elige al final, con '
           u'el plano ya terminado?',
         op=[u'porque hay lista de espera para la impresora 3D',
             u'porque cada t&eacute;cnica obliga a dibujar la pieza de otra manera, y elegirla al final '
             u'obliga a redibujar',
             u'porque el profesor lo decide antes'],
         ok=1,
         por=u'La sierra pide rincones redondeados, el l&aacute;ser pide que todo sea plano y que '
             u'descuentes la sangr&iacute;a, y la impresora pide cuidado con los voladizos, con la '
             u'orientaci&oacute;n de las capas y con los agujeros, que salen peque&ntilde;os. '
             u'<b>El dibujo depende de qui&eacute;n lo vaya a hacer.</b>'),

    dict(p=u'&iquest;Qu&eacute; diferencia hay entre un fichero STL y el modelo del que sali&oacute;?',
         op=[u'ninguna, el STL es el modelo comprimido',
             u'el STL es una piel de tri&aacute;ngulos sin medidas ni historia: no se puede volver a '
             u'editar de verdad',
             u'el STL lleva las cotas y el modelo no'],
         ok=1,
         por=u'El modelo guarda <b>el &aacute;rbol de operaciones</b> y las medidas, y por eso puedes '
             u'volver al paso 2 y cambiar una cota. El STL solo guarda v&eacute;rtices: es el fichero '
             u'que le das a la m&aacute;quina, como el PDF que mandas a imprimir. Por eso se guardan '
             u'los dos, y el que no se puede perder es el otro.'),

    dict(p=u'Un agujero de &empty;8,30 se exporta a STL con <b>8</b> facetas. &iquest;Pasa por '
           u'&eacute;l un eje de 8 mm?',
         op=[u'no: el pol&iacute;gono inscrito deja pasar 8,30 &middot; cos(180&deg;/8) = 7,67',
             u's&iacute;, porque el agujero sigue midiendo 8,30',
             u's&iacute;, y adem&aacute;s con m&aacute;s holgura, porque el pol&iacute;gono tiene '
             u'esquinas'],
         ok=0,
         por=u'El STL sustituye el c&iacute;rculo por un pol&iacute;gono <b>metido dentro</b>, que solo '
             u'toca la circunferencia en los v&eacute;rtices. Lo que de verdad pasa es la distancia '
             u'entre lados opuestos: D &middot; cos(180&deg;/N) = 8,30 &middot; 0,924 = <b>7,67 mm</b>. '
             u'Con 16 facetas saldr&iacute;an 8,14, y ah&iacute; ya pasa.'),

    dict(p=u'Las piezas suman 29 950 mm&sup2; y el tablero tiene 60 000. No caben. &iquest;Por '
           u'qu&eacute;?',
         op=[u'porque el tablero se mide por fuera y las piezas por dentro',
             u'porque el hueco que sobra no est&aacute; junto: una pieza no se puede partir en dos '
             u'recortes',
             u'porque falta contar el peso del material'],
         ok=1,
         por=u'Lo que decide no es la superficie libre <b>total</b>, sino si queda un '
             u'<b>rect&aacute;ngulo entero</b> donde quepa la pieza. Por eso el plan de corte se hace '
             u'antes de cortar y se empieza por las piezas grandes: las peque&ntilde;as caben en '
             u'cualquier hueco y las grandes no.'),

    dict(p=u'Diez cortes con una sierra cuya sangr&iacute;a es de 2 mm. &iquest;Cu&aacute;nto tablero '
           u'desaparece?',
         op=[u'nada: la sangr&iacute;a sale del hueco entre piezas',
             u'2 mm, que es lo que mide un corte',
             u'20 mm de ancho de tablero, que es lo que hay que dejar entre pieza y pieza'],
         ok=2,
         por=u'Cada pasada convierte en serr&iacute;n su propio ancho: 10 &times; 2 = <b>20 mm</b>. Por '
             u'eso en el plan de corte las piezas no se pegan unas a otras en el papel. Y si adem&aacute;s '
             u'cortas por el centro de la raya en vez de por fuera, la mitad de esa sangr&iacute;a se la '
             u'come la pieza.'),

    dict(p=u'Un montaje tiene cuatro eslabones con tolerancias de 0,20, 0,30, 0,10 y 0,10 mm, y un juego '
           u'nominal de 0,40. &iquest;Entre qu&eacute; valores puede quedar el juego?',
         op=[u'entre 0,10 y 0,70, porque las tolerancias se compensan',
             u'entre &minus;0,30 y 1,10: todas las tolerancias se suman, tengan el signo que tengan',
             u'siempre 0,40, si las piezas cumplen'],
         ok=1,
         por=u'0,20 + 0,30 + 0,10 + 0,10 = <b>0,70</b>, y J = 0,40 &plusmn; 0,70. Se suman '
             u'<b>todas</b>, tambi&eacute;n las de las cotas que restan, porque el peor caso es que el '
             u'hueco salga m&iacute;nimo <b>a la vez</b> que lo que va dentro sale m&aacute;ximo. Y un '
             u'juego negativo quiere decir que no entra.'),

    dict(p=u'Tus seis cotas est&aacute;n pedidas con &plusmn;0,15 y la sierra con la que las haces '
           u'dispersa &plusmn;0,50. Van a salir mal. &iquest;Qu&eacute; dices en la defensa?',
         op=[u'que el grupo no ten&iacute;a buen pulso y hay que practicar m&aacute;s',
             u'que la tolerancia era m&aacute;s estrecha que la dispersi&oacute;n de la m&aacute;quina, '
             u'as&iacute; que el fallo est&aacute; en el plano y no en las manos',
             u'que la sierra estaba desajustada y hay que mover el tope'],
         ok=1,
         por=u'Con &plusmn;0,50 de dispersi&oacute;n, una cota de &plusmn;0,15 <b>no se puede cumplir</b> '
             u'por bien que se sierre: eso se decidi&oacute; al elegir la t&eacute;cnica, en la '
             u'sesi&oacute;n 4. El <b>desajuste</b> es otra cosa &mdash;empuja todas las medidas al '
             u'mismo lado y se corrige moviendo el tope&mdash;; la dispersi&oacute;n se aguanta o se '
             u'cambia de m&aacute;quina.'),
])

S8_CIERRE = u'''
      <ol>
      ''' + pregunta(
          u'&iquest;Por qu&eacute; no basta con ense&ntilde;ar la pieza y decir que funciona?',
          u'<p>Porque funcionar no demuestra que est&eacute; bien hecha: puede haber tocado el lado '
          u'bueno de la tolerancia. Si no sabes qu&eacute; pediste, <b>no puedes repetirla</b>; si no '
          u'sabes cu&aacute;nto te has desviado, <b>no sabes qu&eacute; mejorar</b>. La prueba de que '
          u'una pieza est&aacute; bien son n&uacute;meros, no que est&eacute; ah&iacute;.</p>'
          ) + pregunta(
          u'&iquest;Cu&aacute;l es la hoja m&aacute;s valiosa del expediente, y por qu&eacute; casi '
          u'nadie la escribe?',
          u'<p>La de <b>incidencias</b>: qu&eacute; fall&oacute;, qu&eacute; se cambi&oacute; y por '
          u'qu&eacute;. Nadie la escribe porque parece que resta, y es al rev&eacute;s: es la que '
          u'demuestra que hab&eacute;is entendido lo que hac&iacute;ais. Un proyecto sin incidencias no '
          u'es perfecto, es un proyecto que <b>no se ha mirado</b>.</p>') + pregunta(
          u'En la tabla de control, &iquest;para qu&eacute; sirve poner la desviaci&oacute;n en '
          u'porcentaje de la tolerancia?',
          u'<p>Porque un &laquo;pasa&raquo; al 20 % y un &laquo;pasa&raquo; al 95 % <b>no son lo '
          u'mismo</b>. El primero se puede repetir; el segundo te va a fallar en la siguiente pieza. '
          u'El veredicto solo dice s&iacute; o no; el porcentaje dice <b>cu&aacute;nto margen te '
          u'queda</b>.</p>') + pregunta(
          u'En la defensa te preguntan un dato que no hab&eacute;is medido. &iquest;Qu&eacute; se '
          u'contesta?',
          u'<p><b>&laquo;No lo hemos medido&raquo;</b>, y si acaso c&oacute;mo lo mediríais. Es una '
          u'respuesta profesional y la usa todo el mundo que trabaja de esto. Inventarse un '
          u'n&uacute;mero delante de alguien que sabe es la &uacute;nica manera segura de que se caiga '
          u'el resto de lo que hab&eacute;is contado, que s&iacute; era verdad.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Lo que llevas de la unidad entera</span>
        Sabes hacer un <b>plano que otro puede fabricar</b> sin preguntarte nada, y elegir desde
        d&oacute;nde se acota. Sabes escribir una cota <b>con su tolerancia</b> y calcular si dos
        piezas van a encajar antes de tocar el material. Sabes decidir c&oacute;mo se unen y qu&eacute;
        falla primero, con la cuenta delante. Sabes qu&eacute; te cuesta cada t&eacute;cnica y
        qu&eacute; te obliga a cambiar en el dibujo. Sabes <b>modelar con par&aacute;metros</b>, para
        que cambiar el servo sea mover un n&uacute;mero y no rehacer el proyecto. Sabes
        <b>organizar el taller</b>: despiece, plan de corte y orden de operaciones. Sabes que el hueco
        que decide si algo funciona <b>no lo dibuja nadie</b>, y sabes calcularlo. Y sabes
        <b>defender la pieza con n&uacute;meros</b> en vez de con adjetivos.
      </div>
      <div class="nota">
        <span class="n-tag">Lo que queda</span>
        Toda esta unidad ha dado el material por supuesto: &laquo;contrachapado de 4&raquo;,
        &laquo;PLA&raquo;, &laquo;aluminio&raquo;, y a seguir. En la <b>unidad 3</b> se abre esa caja:
        de d&oacute;nde sale cada material, qu&eacute; propiedades te obligan a elegir uno u otro y
        <b>qu&eacute; le cuesta al planeta</b> cada una de las decisiones que acabas de tomar
        &mdash;incluida la de pegar en vez de atornillar&mdash;. Y la <b>unidad 9</b> recoge el
        proyecto entero y lo pone delante de gente de fuera.
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
      bloque('03', u'Autoevaluaci&oacute;n &middot; 10 min', S8_TEST) +
      bloque('04', u'Cierre &middot; 5 min', S8_CIERRE))

MIN4 = [(u"10'", u'Reto'), (u"25'", u'Teor&iacute;a'), (u"20'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')]
MIN5 = [(u"10'", u'Reto'), (u"20'", u'Teor&iacute;a'), (u"15'", u'Pr&aacute;ctica'),
        (u"10'", u'Test'), (u"5'", u'Cierre')]

CH1 = [u'CE2 &middot; 2.1', u'CE3 &middot; 3.1', u'A.2 &middot; A.3.1']
CH2 = [u'CE2 &middot; 2.1 &middot; 2.2', u'A.2.2 &middot; A.3']
CH3 = [u'CE2 &middot; 2.2', u'A.3']
CH4 = [u'CE2 &middot; 2.1 &middot; 2.2', u'CE5 &middot; 5.1', u'A.3 &middot; D.4']
CH5 = [u'CE5 &middot; 5.1', u'CE2 &middot; 2.1', u'A.3 &middot; D.4']
CH6 = [u'CE2 &middot; 2.1 &middot; 2.2', u'CE3 &middot; 3.1', u'A.3']
CH7 = [u'CE2 &middot; 2.2', u'CE3 &middot; 3.1', u'A.2.2 &middot; A.3']
CH8 = [u'CE3 &middot; 3.1 &middot; 3.2', u'CE2 &middot; 2.2', u'A.1.4 &middot; A.4']

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

    # --- segunda mitad: las cuatro siguen la MISMA pieza, el soporte del
    #     deposito del riego, desde el modelo hasta la defensa ---
    dict(corto=u'Modelarlo en 3D',
         titulo=u'El servo mide 23 y no 20',
         entradilla=u'Con las medidas escritas a mano, cambiar un dato es repasar el modelo entero y '
                    u'rezar. Con par&aacute;metros, es mover un n&uacute;mero. Y hay un tercer sitio '
                    u'donde el agujero encoge: al exportarlo.',
         minutado=MIN4, chips=CH5, cuerpo=S5),

    dict(corto=u'Organizar la fabricaci&oacute;n',
         titulo=u'Se acab&oacute; el tablero con dos piezas por cortar',
         entradilla=u'Las piezas ocupaban 29 950 mm&sup2; y el tablero ten&iacute;a 60 000. Nadie ha '
                    u'cortado mal: han cortado en el orden que fue saliendo.',
         minutado=MIN4, chips=CH6, cuerpo=S6),

    dict(corto=u'Montar y ajustar',
         titulo=u'La cota que no dibuj&oacute; nadie',
         entradilla=u'Las cuatro piezas est&aacute;n dentro de su tolerancia y el dep&oacute;sito no '
                    u'gira. Lo que falla es una medida que no aparece en ning&uacute;n plano porque '
                    u'no es de ninguna pieza.',
         minutado=MIN4, chips=CH7, cuerpo=S7),

    dict(corto=u'Contarlo y defenderlo',
         titulo=u'&laquo;Nos ha quedado muy bien&raquo; no es una respuesta',
         entradilla=u'Ense&ntilde;as la pieza y funciona. Te preguntan qu&eacute; tolerancia pediste y '
                    u'cu&aacute;nto te has desviado. Ah&iacute; se acaba el proyecto o empieza la '
                    u'defensa.',
         minutado=MIN5, chips=CH8, cuerpo=S8),
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
         u'fijas y desmontables, t&eacute;cnicas de fabricaci&oacute;n del aula, modelado 3D con '
         u'par&aacute;metros, plan de corte, cadena de cotas del montaje y defensa de la pieza con '
         u'control dimensional. Ocho sesiones con escenas interactivas que calculan.',
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
