# -*- coding: utf-8 -*-
"""2.o TyD - U6 - Electricidad y electronica.

Sesiones 1, 2 y 3 escritas; 4, 5 y 6 marcadas como pendientes.

    ~/venv/bin/python generadores/u6_build.py

El audio del narrador y su envolvente se generan aparte, una sola vez:

    ~/venv/bin/python generadores/voz.py generadores/guion_u6.txt u6-electricidad

Cuidado con el formateo %% de Python: todo el contenido de las sesiones entra
como ARGUMENTO de pagina()/bloque()/ficha(), nunca como plantilla, asi que los
por ciento y los % del JavaScript pasan intactos. La unica plantilla que si
formatea texto propio es avatar_flat.componente(), y ahi no hay ningun %.
"""
import io, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unidad_base import pagina, bloque, ficha, pregunta
import avatar_flat
from u6_escenas import SIMBOLOS, TABLA_SIMBOLOS, ESC_CIRCUITO, ESC_OHM, ESC_SERIE
from u6_escenas2 import ESC_REGLETA, ESC_LED, ESC_TEST

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHIPS = [u'CE3 &middot; 3.1', u'A.6']
# Las dos fotos historicas son verticales y muy largas: a todo el ancho de la
# columna se comen dos pantallas enteras. Se les pone tope de alto y se centran.
# (Va por marcador y no con %% porque este texto pasa por formateo de Python.)
ALTA = u'width:auto;max-width:100%;max-height:520px;margin:0 auto'
MIN = [(u"10'", u'Reto'), (u"20'", u'Teor&iacute;a'), (u"25'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')]
# La sesion 6 reparte distinto: casi todo el tiempo es para el proyecto.
MIN6 = [(u"5'", u'Reto'), (u"35'", u'Proyecto'), (u"15'", u'Entrega'), (u"5'", u'Cierre')]


def video(idv, titulo, canal, nota):
    """Bloque de video que no carga nada de YouTube hasta que se pulsa."""
    return (u'''
      <div class="video" id="video-''' + idv + u'''" data-vid="''' + idv + u'''">
        <button type="button" class="video-play" aria-label="Reproducir el v&iacute;deo: ''' + titulo + u'''">
          <span class="video-tri" aria-hidden="true"></span>
          <span class="video-txt">
            <b>''' + titulo + u'''</b>
            <span>''' + canal + u'''</span>
          </span>
        </button>
        <p class="video-nota">''' + nota + u'''</p>
        <p class="video-nota">El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin cookies de
          seguimiento. Si la red del centro bloquea YouTube,
          <a href="https://www.youtube.com/watch?v=''' + idv + u'''" target="_blank" rel="noopener">&aacute;brelo
          directamente aqu&iacute;</a>. Es obra de su autor y no forma parte del material publicado bajo la
          licencia de esta p&aacute;gina.</p>
      </div>
''')


VIDEO_JS = u'''
      <script>
      (function(){
        document.querySelectorAll('.video[data-vid]').forEach(function(c){
          var b = c.querySelector('.video-play');
          if(!b) return;
          b.addEventListener('click', function(){
            var f = document.createElement('iframe');
            f.src = 'https://www.youtube-nocookie.com/embed/' + c.dataset.vid
                  + '?autoplay=1&rel=0&modestbranding=1';
            f.title = b.querySelector('.video-txt b').textContent;
            f.allow = 'accelerometer; autoplay; encrypted-media; picture-in-picture';
            f.referrerPolicy = 'strict-origin-when-cross-origin';
            f.allowFullscreen = true;
            b.replaceWith(f);
          });
        });
      })();
      </script>
'''


def narrador():
    env = json.load(io.open(os.path.join(RAIZ, '_env_u6-electricidad.json'), encoding='utf-8'))
    return avatar_flat.componente(
        'narr-u6', u'El tema en un minuto',
        u'De d&oacute;nde sale la energ&iacute;a, y qu&eacute; hace falta para llevarla hasta donde quieres',
        '../../../audio/u6-electricidad.mp3', env,
        u'Voz sintetizada y audio propio. La boca sigue el volumen real de la voz: se mueve '
        u'cuando habla y se para en los silencios.')


# ==========================================================================
# SESION 1 - Un cable no hace nada
# ==========================================================================
S1 = (
  bloque('00', u'Reto inicial &middot; 10 min', narrador() + u'''
      <p>En el tema anterior conseguiste que el movimiento llegara de un sitio a otro: engranajes,
         poleas, palancas. Funciona, pero hay un detalle que lo estropea todo: <b>el que empuja
         eres t&uacute;</b>. En cuanto sueltas la manivela, se para.</p>
      <p>Para que se mueva sin ti hace falta energ&iacute;a que venga de otro sitio y que llegue hasta
         donde est&aacute; el mecanismo. Casi siempre llega por un cable. As&iacute; que empecemos por el
         cable.</p>

      <div class="aviso">
        <span class="n-tag">El reto</span>
        Encima de la mesa hay <b>una pila, una bombilla y un solo cable</b>. Dibuja en la libreta,
        en un minuto, c&oacute;mo los conectas para que la bombilla se encienda.
      </div>

      <p>Comparad los dibujos. Van a salir casi todos iguales: un cable que sale del polo positivo
         de la pila y llega al casquillo de la bombilla. Es lo l&oacute;gico: la pila tiene la
         electricidad, la bombilla la necesita, el cable la lleva.</p>
      <p>Pru&eacute;balo. <b>No se enciende.</b> Ni un poco, ni d&eacute;bilmente, ni despu&eacute;s de un rato.
         Nada.</p>

      <div class="reto-piensa">
        <span class="n-tag">Piensa antes de seguir</span>
        <p>Y ahora la pregunta que importa: <b>&iquest;qu&eacute; le falta?</b> No vale contestar &laquo;una pila
           m&aacute;s grande&raquo; ni &laquo;un cable mejor&raquo;. Con la misma pila, el mismo cable y la misma
           bombilla, se puede encender. Lo que falta <b>no es una pieza</b>.</p>
      </div>
  ''') +

  bloque('01', u'Teor&iacute;a &middot; 20 min', u'''
      <h3>Lo que falta no es una pieza: es un anillo</h3>
      <p>La idea de que la electricidad &laquo;va&raquo; de la pila a la bombilla y all&iacute; se gasta es
         c&oacute;moda y es falsa. Las cargas del cobre no se consumen en la bombilla: <b>la atraviesan y
         siguen</b>, y tienen que poder volver a la pila por otro camino.</p>
      <p>Por eso un solo cable no sirve por muy bien que lo conectes. Lo que hace falta es un
         <b>camino cerrado sobre s&iacute; mismo</b>, un anillo. Y esto tiene una consecuencia que cuesta
         creer la primera vez: si en cualquier punto de ese anillo falta un trozo &mdash;aunque sea un
         mil&iacute;metro, aunque sea al otro lado de la habitaci&oacute;n&mdash; <b>no circula nada por ninguna
         parte</b>. No es que circule menos. Es que no circula.</p>
      <p>Compru&eacute;balo t&uacute; mismo. Pon y quita cables, abre y cierra el interruptor, y mira qu&eacute; pasa
         en cada caso.</p>
''' + ESC_CIRCUITO + u'''
      <p>F&iacute;jate en el tercer caso, el del <b>puente</b>. Ah&iacute; el camino est&aacute; cerrad&iacute;simo &mdash;de
         hecho hay dos&mdash; y la l&aacute;mpara sigue apagada. La corriente hace lo mismo que el agua y
         que t&uacute;: coge el camino f&aacute;cil. Si le pones al lado un puente de cobre que no le estorba
         nada, se va por el puente y se salta la l&aacute;mpara.</p>

      <div class="copiar">
        <h4>El circuito</h4>
        <p><b>Circuito el&eacute;ctrico</b>: camino cerrado por el que las cargas salen del generador,
           atraviesan el receptor y vuelven al generador.</p>
        <p>Los <b>cuatro elementos</b> que necesita:</p>
        <ul>
          <li><b>Generador</b>: empuja las cargas. Pila, bater&iacute;a, fuente de alimentaci&oacute;n.</li>
          <li><b>Conductores</b>: llevan las cargas de un sitio a otro. Los cables, de cobre.</li>
          <li><b>Receptor</b>: transforma la energ&iacute;a en algo &uacute;til. L&aacute;mpara, motor, zumbador.</li>
          <li><b>Elemento de control</b>: deja pasar o corta. Interruptor, pulsador, conmutador.</li>
        </ul>
        <h4>Los tres estados</h4>
        <ul>
          <li><b>Circuito abierto</b>: el anillo est&aacute; cortado en alg&uacute;n punto. No circula corriente.</li>
          <li><b>Circuito cerrado</b>: el anillo est&aacute; completo y la corriente atraviesa el receptor.</li>
          <li><b>Cortocircuito</b>: hay un camino de vuelta <b>sin receptor</b>, solo cable. La
              corriente se dispara, el generador se calienta y algo se quema.</li>
        </ul>
      </div>

      <h3>C&oacute;mo se dibuja: simbolog&iacute;a normalizada</h3>
      <p>Un esquema el&eacute;ctrico no es un dibujo del montaje: es un <b>plano</b>. No importa d&oacute;nde
         est&eacute; f&iacute;sicamente cada pieza ni qu&eacute; forma tiene, importa <b>qu&eacute; est&aacute; conectado con
         qu&eacute;</b>. Para eso cada componente tiene un s&iacute;mbolo acordado internacionalmente.</p>
''' + TABLA_SIMBOLOS + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; no hace falta copiarlo</span>
        <p>Todo esto no se pod&iacute;a hacer antes de 1800, y no por falta de ganas. Electricidad
           hab&iacute;a: se acumulaba frotando &aacute;mbar o vidrio y se guardaba en botellas de Leyden. Pero
           era <b>electricidad est&aacute;tica</b>, que se descarga de golpe en una chispa. Serv&iacute;a para
           hacer saltar a los invitados de una fiesta, no para tener una l&aacute;mpara encendida una
           hora.</p>
        <p>Lo que faltaba era un generador que empujara <b>de forma continua</b>. Y apareci&oacute; de una
           discusi&oacute;n cient&iacute;fica que no iba de esto. Luigi Galvani hab&iacute;a visto contraerse las patas
           de una rana muerta al tocarlas con metal, y lo atribu&iacute;a a una &laquo;electricidad animal&raquo;
           propia del ser vivo. <b>Alessandro Volta</b> defend&iacute;a lo contrario: que la rana no
           pintaba nada y que bastaban <b>dos metales distintos</b> con algo h&uacute;medo entre ellos.</p>
        <p>Para ganar la discusi&oacute;n, en 1800 Volta apil&oacute; discos de cinc y de cobre separados por
           cartones empapados en salmuera. Aquel mont&oacute;n daba corriente de manera continua, sin
           rana. Gan&oacute; el argumento y de paso invent&oacute; el primer generador de la historia; de aquel
           mont&oacute;n viene la palabra que usas todos los d&iacute;as: <b>pila</b>.</p>
      </div>

      <figure class="foto">
        <img src="../../../img/u6-pila-volta.jpg" loading="lazy" style="@@ALTA@@"
             alt="Pila de Volta conservada: una columna de discos met&aacute;licos alternados, sujeta por
                  tres varillas de vidrio sobre una base de madera">
        <figcaption>Una <b>pila de Volta</b> conservada, de las que se salvaron del incendio de la
          Exposici&oacute;n del Centenario de Volta en Como, en 1899. Se ven los discos apilados de dos
          metales distintos, separados por los cartones empapados, y las varillas de vidrio
          &mdash;aislante&mdash; que sujetan la columna sin cortocircuitarla.
          <br><br>Fue el primer aparato capaz de mantener una corriente durante horas. Todo lo que
          hay en esta p&aacute;gina empieza aqu&iacute;.
          <span class="credito">Wellcome Collection &middot; CC BY 4.0 &middot;
            <a href="https://commons.wikimedia.org/wiki/File:Voltaic_pile,_Europe,_1800-1899_Wellcome_L0057740.jpg"
               target="_blank" rel="noopener">Wikimedia Commons</a></span>
        </figcaption>
      </figure>
''' + video('PFP9LsBdnLA', u'El circuito el&eacute;ctrico y sus componentes',
            u'Clases Particulares en &Aacute;vila',
            u'Rep&aacute;salo en v&iacute;deo y <b>anota una cosa</b>: cada vez que aparezca un componente, '
            u'p&aacute;ralo y dibuja su s&iacute;mbolo de memoria antes de mirarlo. Si no te sale, es que a&uacute;n no '
            u'lo tienes.')) +

  bloque('02', u'Pr&aacute;ctica &middot; 25 min', ficha(
    u'Actividad 1 &middot; Que encienda, y que se pueda apagar',
    [u'3.1', u'A.6'], u'Parejas &middot; 25 min', u'''
          <h4>Qu&eacute; hay que hacer</h4>
          <p>Primero en la libreta, y despu&eacute;s en el simulador
             <a href="https://www.tinkercad.com/circuits" target="_blank" rel="noopener">Tinkercad
             Circuits</a>, que funciona en el navegador y no hay que instalar nada.</p>
          <ol class="pasos">
            <li><b>Tres esquemas a mano</b>, con simbolog&iacute;a normalizada y regla: el circuito
                abierto, el circuito cerrado y el circuito con interruptor. Rotulad cada elemento
                con su nombre.</li>
            <li><b>Montadlo en Tinkercad</b>: bater&iacute;a de 4,5 V (el bloque de 3 pilas AA),
                interruptor y bombilla. Que encienda al cerrar y apague al abrir.</li>
            <li><b>Provocad un cortocircuito a prop&oacute;sito</b>: un cable que vaya directo de un polo
                de la pila al otro. Copiad <b>literalmente</b> el mensaje que saca el simulador.</li>
            <li>Explicad en <b>dos l&iacute;neas</b> por qu&eacute; se queja, usando la palabra <i>receptor</i>.</li>
            <li>Guardad una captura de cada montaje y pegadlas en la libreta o entregadlas.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Los tres esquemas usan los s&iacute;mbolos normalizados, no dibujitos <b>(3 puntos)</b>.</li>
            <li>El montaje de Tinkercad enciende y apaga de verdad <b>(3 puntos)</b>.</li>
            <li>El cortocircuito est&aacute; reproducido y el mensaje, copiado tal cual <b>(2 puntos)</b>.</li>
            <li>La explicaci&oacute;n habla del camino sin receptor, no de &laquo;que hay mucha
                electricidad&raquo; <b>(2 puntos)</b>.</li>
          </ul>
          <div class="nota" style="margin-top:14px">
            <span class="n-tag">Aviso</span>
            El cortocircuito se hace <b>en el simulador</b>, nunca con una pila de verdad en la
            mano. En el simulador sale un aviso; con una pila de litio en el bolsillo sale humo.
          </div>
  ''')) +

  bloque('03', u'Cierre &middot; 5 min', u'''
      <p>Vuelve al dibujo que hiciste al empezar la clase. Le faltaba el camino de vuelta, y ahora
         sabes que eso no es un detalle: <b>es la definici&oacute;n de circuito</b>.</p>
      <ol>
      ''' + pregunta(u'&iquest;Por qu&eacute; no basta con un cable del polo positivo a la bombilla?',
                     u'<p>Porque las cargas no se gastan en la bombilla: la atraviesan y necesitan <b>volver al generador</b>. Sin camino de vuelta no circula nada.</p>')
        + pregunta(u'Un circuito est&aacute; cerrado y bien montado, pero hay un cable que une los dos bornes de la l&aacute;mpara. &iquest;Qu&eacute; pasa y c&oacute;mo se llama?',
                   u'<p>La corriente se va por el cable, que no le estorba, y la l&aacute;mpara se queda apagada. Es un <b>cortocircuito</b>: hay camino de vuelta sin receptor, la corriente se dispara y el generador se calienta.</p>')
        + pregunta(u'&iquest;Para qu&eacute; sirve exactamente un interruptor?',
                   u'<p>Para <b>abrir el anillo a voluntad</b>. Es un hueco que t&uacute; decides cu&aacute;ndo est&aacute; y cu&aacute;ndo no. Y como basta un hueco en cualquier punto para que se pare todo, da igual d&oacute;nde se ponga.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        La forma del montaje est&aacute; clara. Pero una pila de petaca se puede agarrar
        por los dos polos sin notar nada y un enchufe de casa puede matar, y en los dos hay cargas
        y cobre. La pr&oacute;xima sesi&oacute;n va de <b>qu&eacute; es lo que cambia, y c&oacute;mo se mide</b>.
      </div>
  '''))


# ==========================================================================
# SESION 2 - Tension, intensidad, resistencia y la ley de Ohm
# ==========================================================================
S2 = (
  bloque('00', u'Reto inicial &middot; 10 min', u'''
      <p>En la sesi&oacute;n anterior montaste el anillo. Ahora vamos a mirar <b>qu&eacute; pasa dentro</b>.
         Dos hechos que todo el mundo conoce y que, puestos uno al lado del otro, no cuadran.</p>

      <div class="aviso">
        <span class="n-tag">Dos hechos que chocan</span>
        <p style="margin:0 0 8px"><b>Uno.</b> Una pila de petaca de 4,5 V se puede agarrar con los
           dedos por los dos polos a la vez y no se nota nada. Un enchufe de 230 V puede matar a
           una persona. En los dos casos hay cobre y hay cargas.</p>
        <p style="margin:0"><b>Dos.</b> Enciendes un tostador: el hilo de dentro se pone al rojo y
           el cable que va al enchufe sigue fr&iacute;o. Est&aacute;n uno detr&aacute;s de otro en el mismo camino, o
           sea que por los dos pasa <b>exactamente la misma corriente</b>.</p>
      </div>

      <div class="reto-piensa">
        <span class="n-tag">Piensa antes de seguir</span>
        <p>Escribe una frase que explique <b>los dos hechos a la vez</b>. &iquest;Qu&eacute; es lo que cambia
           de un caso al otro?</p>
      </div>

      <p>Va a salir, seguro, &laquo;es que hay m&aacute;s electricidad&raquo;. El problema de esa respuesta no es
         que sea mentira: es que <b>no sirve para nada</b>. No dice cu&aacute;nta, no se puede medir con
         ning&uacute;n aparato y no permite calcular nada. Y sobre todo: con la misma frase intentas
         explicar dos cosas que son distintas.</p>
      <p>Porque en el primer hecho lo que cambia es el <b>empuj&oacute;n</b>, y en el segundo lo que
         cambia es el <b>estorbo</b>. Son dos magnitudes diferentes, y hay una tercera que las
         relaciona.</p>
  ''') +

  bloque('01', u'Teor&iacute;a &middot; 20 min', u'''
      <h3>Tres magnitudes, y ni una m&aacute;s</h3>
      <p>Todo lo que pasa en un circuito de este curso se describe con tres n&uacute;meros. Si los tienes,
         lo tienes todo.</p>

      <div class="copiar">
        <h4>Las tres magnitudes</h4>
        <ul>
          <li><b>Tensi&oacute;n (V)</b> &middot; el <b>empuj&oacute;n</b>. Diferencia de potencial que el generador
              mantiene entre sus dos bornes. Se mide en <b>voltios</b>, con el <b>volt&iacute;metro</b>,
              conectado <b>en paralelo</b> con lo que quieras medir.</li>
          <li><b>Intensidad (I)</b> &middot; el <b>caudal</b>. Cantidad de carga que atraviesa cada
              segundo un punto del circuito. Se mide en <b>amperios</b>, con el
              <b>amper&iacute;metro</b>, conectado <b>en serie</b>, o sea intercalado en el camino.</li>
          <li><b>Resistencia (R)</b> &middot; el <b>estorbo</b>. Oposici&oacute;n que pone un elemento al paso
              de la corriente. Se mide en <b>ohmios (&#8486;)</b>, con el <b>&oacute;hmetro</b>, y
              siempre con el circuito <b>desconectado</b>.</li>
        </ul>
        <p>La tensi&oacute;n <b>existe aunque no circule nada</b>: una pila en un caj&oacute;n tiene sus 4,5 V.
           La intensidad solo aparece cuando el circuito est&aacute; cerrado.</p>
      </div>

      <h3>La regla que las une</h3>
      <p>Las tres no van por su cuenta. Mueve el empuj&oacute;n y el estorbo en este banco de pruebas y
         mira qu&eacute; le pasa al caudal.</p>
''' + ESC_OHM + u'''
      <p>Dos cosas que conviene ver ah&iacute; y no olvidar. La primera: la gr&aacute;fica es una
         <b>recta que pasa por el origen</b>. Eso es lo que de verdad dice la ley &mdash;que si
         doblas la tensi&oacute;n, se dobla la corriente&mdash; y no es obvio: podr&iacute;a no ser as&iacute;, y de
         hecho en una bombilla caliente o en un LED <b>no lo es</b>. La segunda: cuando bajas mucho
         la resistencia, la corriente se dispara. Eso, dibujado, es el cortocircuito de la sesi&oacute;n
         anterior.</p>

      <div class="copiar">
        <h4>Ley de Ohm</h4>
        <p>En un conductor met&aacute;lico a temperatura constante:</p>
        <p style="font-family:var(--f-m);font-size:17px;text-align:center;margin:10px 0">
           I = V / R &nbsp;&middot;&nbsp; V = I &times; R &nbsp;&middot;&nbsp; R = V / I</p>
        <p>Con <b>V en voltios, R en ohmios e I en amperios</b>. Si mezclas unidades &mdash;milivoltios
           con ohmios, por ejemplo&mdash; el resultado no significa nada.</p>
        <h4>Ejemplo resuelto</h4>
        <p>Pila de 4,5 V y bombilla de 9 &#8486;: &nbsp;I = 4,5 / 9 = <b>0,5 A</b>.</p>
        <p>La misma pila con una bombilla de 18 &#8486;: &nbsp;I = 4,5 / 18 = <b>0,25 A</b>, la mitad
           de corriente y bastante menos luz.</p>
      </div>

      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; no hace falta copiarlo</span>
        <p><b>Georg Simon Ohm</b> public&oacute; esto en 1827, en un libro titulado
           <i>Die galvanische Kette, mathematisch bearbeitet</i>. Lo interesante no es la f&oacute;rmula,
           es c&oacute;mo consigui&oacute; llegar a ella.</p>
        <p>Sus primeros experimentos no cuadraban, y no por culpa de la teor&iacute;a: <b>las pilas de su
           &eacute;poca no daban dos veces seguidas el mismo valor</b>. Ohm cambi&oacute; la pila por un
           <b>par termoel&eacute;ctrico</b> &mdash;dos metales soldados, con una uni&oacute;n caliente y otra
           fr&iacute;a&mdash;, que s&iacute; manten&iacute;a una tensi&oacute;n estable, y solo entonces le salieron los
           n&uacute;meros limpios. Esa es una lecci&oacute;n de Tecnolog&iacute;a m&aacute;s &uacute;til que la propia ley:
           <b>cuando los datos no cuadran, a veces el problema est&aacute; en el aparato de medir</b>.</p>
        <p>No le sirvi&oacute; de mucho al principio. Su libro se recibi&oacute; con frialdad en Alemania y Ohm
           acab&oacute; dimitiendo de su puesto. Tuvo que esperar catorce a&ntilde;os a que la Royal Society de
           Londres le diera la medalla Copley, en 1841. Hoy la unidad de resistencia lleva su
           apellido.</p>
      </div>

      <figure class="foto">
        <img src="../../../img/u6-georg-ohm.jpg" loading="lazy"
             alt="Retrato de Georg Simon Ohm, f&iacute;sico alem&aacute;n, con levita oscura y una condecoraci&oacute;n al cuello">
        <figcaption><b>Georg Simon Ohm</b> (1789-1854). Era profesor de instituto cuando hizo el
          trabajo: no ten&iacute;a laboratorio de universidad ni ayudantes, y el aparato decisivo &mdash;el
          par termoel&eacute;ctrico&mdash; se lo tuvo que buscar para poder fiarse de sus propias medidas.
          <span class="credito">Reproducci&oacute;n de un retrato, h. 1898-1901 &middot; Dominio p&uacute;blico &middot;
            <a href="https://commons.wikimedia.org/wiki/File:Georg_Simon_Ohm3.jpg"
               target="_blank" rel="noopener">Wikimedia Commons</a></span>
        </figcaption>
      </figure>
''' + video('tpt9FlNYq4k', u'Circuitos el&eacute;ctricos: ley de Ohm y potencia',
            u'El Traductor de Ingenier&iacute;a',
            u'Va un poco m&aacute;s all&aacute; de esta sesi&oacute;n: habla tambi&eacute;n de <b>potencia</b>, que es la '
            u'sesi&oacute;n 4. De momento qu&eacute;date con la parte de la ley de Ohm y toma nota de la otra: '
            u'la vas a necesitar.')) +

  bloque('02', u'Pr&aacute;ctica &middot; 25 min', ficha(
    u'Actividad 2 &middot; Predice primero, mide despu&eacute;s',
    [u'3.1', u'A.6'], u'Parejas &middot; 25 min', u'''
          <h4>Qu&eacute; hay que hacer</h4>
          <p>En <a href="https://www.tinkercad.com/circuits" target="_blank" rel="noopener">Tinkercad
             Circuits</a>. Lo importante de esta pr&aacute;ctica es el <b>orden</b>: primero se calcula,
             despu&eacute;s se mide.</p>
          <ol class="pasos">
            <li>Montad un circuito con una <b>pila de 9 V</b>, una resistencia y un
                <b>mult&iacute;metro en serie</b> midiendo intensidad.</li>
            <li>Para cada una de estas tres resistencias &mdash;<b>100 &#8486;, 220 &#8486; y
                1 k&#8486;</b>&mdash;, <b>escribid primero</b> en la libreta qu&eacute; intensidad predec&iacute;s
                con la ley de Ohm. Operaci&oacute;n incluida. Despu&eacute;s simulad y anotad lo que marca.</li>
            <li>Rellenad la tabla: R &middot; I predicha &middot; I medida &middot; diferencia.</li>
            <li>Cambiad la pila por una de <b>4,5 V</b>, repetid con la de 220 &#8486; y comprobad si
                la corriente se ha reducido en la proporci&oacute;n que esperabais.</li>
            <li>Escribid una conclusi&oacute;n de tres l&iacute;neas: &iquest;se cumple la ley? &iquest;d&oacute;nde est&aacute;n las
                diferencias y a qu&eacute; pueden deberse?</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Las tres predicciones est&aacute;n escritas <b>con su operaci&oacute;n</b> y antes de medir
                <b>(3 puntos)</b>.</li>
            <li>La tabla est&aacute; completa y las unidades son correctas <b>(3 puntos)</b>.</li>
            <li>La segunda parte, con la pila de 4,5 V, est&aacute; hecha y comparada <b>(2 puntos)</b>.</li>
            <li>La conclusi&oacute;n interpreta los n&uacute;meros y no los repite <b>(2 puntos)</b>.</li>
          </ul>
          <div class="nota" style="margin-top:14px">
            <span class="n-tag">Aviso</span>
            Si med&iacute;s primero y &laquo;predec&iacute;s&raquo; despu&eacute;s, la actividad vale <b>cero</b>, aunque la
            tabla est&eacute; perfecta. Lo que se eval&uacute;a aqu&iacute; es si vuestro modelo acierta, y eso solo
            se sabe si el modelo habla antes.
          </div>
  ''')) +

  bloque('03', u'Cierre &middot; 5 min', u'''
      <p>Las tres magnitudes tienen ahora nombre, unidad, aparato de medida y una regla que las
         ata. Con eso ya se puede calcular un circuito en vez de opinar sobre &eacute;l.</p>
      <ol>
      ''' + pregunta(u'Una pila de 12 V y una resistencia de 48 &#8486;. &iquest;Qu&eacute; intensidad circula?',
                     u'<p>I = V / R = 12 / 48 = <b>0,25 A</b>, es decir 250 mA.</p>')
        + pregunta(u'Por una l&aacute;mpara pasan 0,3 A cuando se le aplican 6 V. &iquest;Cu&aacute;nto vale su resistencia?',
                   u'<p>R = V / I = 6 / 0,3 = <b>20 &#8486;</b>.</p>')
        + pregunta(u'&iquest;Por qu&eacute; el amper&iacute;metro se conecta en serie y el volt&iacute;metro en paralelo?',
                   u'<p>Porque el amper&iacute;metro mide <b>lo que pasa por un sitio</b>, as&iacute; que tiene que estar en el camino para que la corriente lo atraviese. El volt&iacute;metro mide una <b>diferencia entre dos puntos</b>, as&iacute; que se pone a caballo de esos dos puntos.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Sabes calcular un circuito con una l&aacute;mpara. Pero en una guirnalda vieja se funde una sola
        y se apaga la tira entera, y en tu casa se funde la de la cocina y el sal&oacute;n sigue
        encendido. Las dos tienen varias l&aacute;mparas y una sola fuente. La pr&oacute;xima sesi&oacute;n va de
        <b>las dos &uacute;nicas maneras de conectarlas</b>.
      </div>
  '''))


# ==========================================================================
# SESION 3 - Serie y paralelo
# ==========================================================================
S3 = (
  bloque('00', u'Reto inicial &middot; 10 min', u'''
      <p>Montar un anillo y calcularlo: hecho. Ahora complicamos lo m&iacute;nimo posible:
         en vez de una l&aacute;mpara, <b>dos</b>.</p>

      <div class="aviso">
        <span class="n-tag">El reto</span>
        Una pila y <b>dos l&aacute;mparas</b>. Dibuja, con simbolog&iacute;a normalizada, <b>todas</b> las
        maneras distintas de conectarlas que se te ocurran. Tienes tres minutos.
      </div>

      <p>Comparad los dibujos. Descartando los que son el mismo esquema girado, quedan
         <b>exactamente dos</b>: o las pones una detr&aacute;s de otra en el mismo camino, o le das a cada
         una su propio camino entre los mismos dos puntos. No hay una tercera.</p>
      <p>Y esas dos maneras no son un matiz de dibujante. Compara estas dos situaciones, que
         conoces las dos:</p>
      <ul>
        <li>En una guirnalda vieja se funde <b>una</b> bombilla y se apaga <b>la tira entera</b>.</li>
        <li>En tu casa se funde la de la cocina y el sal&oacute;n <b>sigue encendido</b>.</li>
      </ul>

      <div class="reto-piensa">
        <span class="n-tag">Piensa antes de seguir</span>
        <p>&iquest;Cu&aacute;l de tus dos dibujos es la guirnalda y cu&aacute;l es tu casa? Y la segunda pregunta,
           que es la que se falla: si en un montaje a&ntilde;ades l&aacute;mparas, <b>&iquest;la pila tiene que dar
           m&aacute;s corriente o menos?</b></p>
      </div>

      <p>La respuesta intuitiva es &laquo;menos, porque hay m&aacute;s estorbo&raquo;. En uno de los dos montajes
         es verdad. En el otro es <b>exactamente al rev&eacute;s</b>, y saber cu&aacute;l es cu&aacute;l es lo que
         impide que se te queme una regleta.</p>
  ''') +

  bloque('01', u'Teor&iacute;a &middot; 20 min', u'''
      <h3>Los dos montajes, con las cuentas delante</h3>
      <p>Tres l&aacute;mparas iguales de 9 &#8486; y una pila de 4,5 V. Cambia de montaje, pulsa una
         l&aacute;mpara para fundirla y mira los n&uacute;meros de abajo: est&aacute;n calculados con la ley de Ohm, no
         puestos a mano.</p>
''' + ESC_SERIE + u'''
      <p>Lo que hay que llevarse de ah&iacute; son dos cosas. La primera es la <b>aver&iacute;a</b>: en serie
         una l&aacute;mpara fundida abre el &uacute;nico camino y las apaga todas; en paralelo cada una cae
         sola. La segunda es m&aacute;s sutil y es la que enga&ntilde;a: al a&ntilde;adir l&aacute;mparas en paralelo la
         <b>resistencia total baja</b> y la corriente total <b>sube</b>.</p>
      <p>Tiene sentido si dejas de pensar en &laquo;estorbo&raquo; y piensas en <b>caminos</b>: cada l&aacute;mpara
         que a&ntilde;ades en paralelo es una puerta m&aacute;s por la que salir, y con m&aacute;s puertas abiertas
         sale m&aacute;s gente, no menos.</p>

      <div class="copiar">
        <h4>Conexi&oacute;n en serie</h4>
        <ul>
          <li>Un <b>&uacute;nico camino</b>: la corriente es <b>la misma</b> en todos los elementos.</li>
          <li>Las resistencias se <b>suman</b>: &nbsp;R<sub>T</sub> = R&#8321; + R&#8322; + R&#8323;</li>
          <li>La tensi&oacute;n de la fuente se <b>reparte</b> entre los receptores.</li>
          <li>Si uno falla, se abre el circuito y <b>se paran todos</b>.</li>
        </ul>
        <h4>Conexi&oacute;n en paralelo</h4>
        <ul>
          <li><b>Varios caminos</b> entre los mismos dos puntos: la tensi&oacute;n es <b>la misma</b> en
              todos ellos.</li>
          <li>Las corrientes se <b>suman</b>: &nbsp;I<sub>T</sub> = I&#8321; + I&#8322; + I&#8323;</li>
          <li>La resistencia total <b>baja</b>: &nbsp;1/R<sub>T</sub> = 1/R&#8321; + 1/R&#8322; + 1/R&#8323;
              &nbsp;&mdash; y si son <b>iguales</b>, R<sub>T</sub> = R / n.</li>
          <li>Si uno falla, <b>los dem&aacute;s siguen</b>.</li>
        </ul>
        <h4>Los dos casos, con n&uacute;meros</h4>
        <p>Tres l&aacute;mparas de 9 &#8486; con 4,5 V:</p>
        <ul>
          <li><b>Serie</b>: R<sub>T</sub> = 27 &#8486; &middot; I = 4,5/27 = 0,167 A &middot; cada
              l&aacute;mpara recibe 1,5 V.</li>
          <li><b>Paralelo</b>: R<sub>T</sub> = 9/3 = 3 &#8486; &middot; I<sub>T</sub> = 1,5 A &middot;
              cada l&aacute;mpara recibe 4,5 V y toma 0,5 A.</li>
        </ul>
      </div>

      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; no hace falta copiarlo</span>
        <p>Elegir entre serie y paralelo no es un ejercicio: es una decisi&oacute;n que cost&oacute; dinero de
           verdad. El <b>4 de septiembre de 1882</b>, Thomas Edison puso en marcha la central de
           <b>Pearl Street</b>, en el bajo Manhattan: la primera central comercial de electricidad
           para alumbrado. Repart&iacute;a corriente continua a <b>110 voltios</b> y aquel primer d&iacute;a
           encend&iacute;a unas 400 l&aacute;mparas de poco m&aacute;s de ochenta clientes del barrio.</p>
        <p>Edison cable&oacute; a sus clientes <b>en paralelo</b>. La alternativa exist&iacute;a y estaba en la
           calle: el alumbrado de arco de las farolas iba <b>en serie</b>, y una sola aver&iacute;a dejaba
           a oscuras la l&iacute;nea entera. Para vender luz a domicilio eso era inaceptable, porque
           ning&uacute;n cliente quiere que su l&aacute;mpara dependa de la del vecino.</p>
        <p>La segunda decisi&oacute;n fue menos evidente, y es pura ley de Ohm. Edison dise&ntilde;&oacute; l&aacute;mparas
           de resistencia <b>alta</b>: de una de aquellas l&aacute;mparas de 1880 se conservan los datos
           &mdash;0,94 amperios a 55 voltios, o sea unos <b>58 &#8486;</b>&mdash;. Con filamentos de
           poca resistencia habr&iacute;a hecho falta mucha m&aacute;s corriente por l&aacute;mpara, y m&aacute;s corriente
           significa <b>cables de cobre m&aacute;s gruesos</b>. El cobre enterrado bajo la calle era una
           de las partidas m&aacute;s caras de la instalaci&oacute;n: elegir la resistencia del filamento era, en
           realidad, elegir cu&aacute;nto cobre hab&iacute;a que comprar.</p>
        <p>Y la pega se la puso la misma ley. Con 110 V de corriente continua, la resistencia de los
           propios cables se com&iacute;a la tensi&oacute;n por el camino y Pearl Street apenas daba servicio a
           unas manzanas a la redonda. Llevar la electricidad lejos exig&iacute;a subir mucho la tensi&oacute;n,
           y eso, entonces, solo sab&iacute;a hacerlo la corriente alterna.</p>
      </div>

      <figure class="foto">
        <img src="../../../img/u6-lampara-edison.jpg" loading="lazy" style="@@ALTA@@"
             alt="Fotograf&iacute;a antigua de una l&aacute;mpara de incandescencia de Edison con filamento de
                  carb&oacute;n en horquilla, enroscada en su portal&aacute;mparas">
        <figcaption>Una de las primeras <b>l&aacute;mparas de filamento de carb&oacute;n</b> de Edison, de
          alrededor de 1880. F&iacute;jate en el filamento: largo, finito y doblado en horquilla para que
          quepa. Esa forma no es est&eacute;tica, es la manera de conseguir <b>mucha resistencia</b> en
          poco sitio.
          <br><br>La fuente de la que procede la foto da su consumo: <b>0,94 amperios a 55
          voltios</b>. Esos dos n&uacute;meros son los que puedes usar t&uacute; para calcular su resistencia con
          la ley de Ohm, y salen unos 58 ohmios.
          <span class="credito">Joseph E. Hinds, <i>Popular Electricity</i>, 1910 &middot; Dominio
            p&uacute;blico &middot;
            <a href="https://commons.wikimedia.org/wiki/File:Edison_carbon_filament_light_bulb.jpg"
               target="_blank" rel="noopener">Wikimedia Commons</a></span>
        </figcaption>
      </figure>
''' + video('OVDqVpnRltw', u'Circuito el&eacute;ctrico con serie y paralelo &middot; Tecnolog&iacute;a 2.&ordm; ESO',
            u'Academia Usero Estepona',
            u'Un ejercicio resuelto paso a paso, del mismo nivel que el vuestro. Hacedlo vosotros '
            u'primero en la libreta, con el v&iacute;deo pausado, y comparad despu&eacute;s.')) +

  bloque('02', u'Pr&aacute;ctica &middot; 25 min', ficha(
    u'Actividad 3 &middot; La guirnalda y la casa',
    [u'3.1', u'A.6'], u'Parejas &middot; 25 min', u'''
          <h4>Qu&eacute; hay que hacer</h4>
          <p>En <a href="https://www.tinkercad.com/circuits" target="_blank" rel="noopener">Tinkercad
             Circuits</a>, con <b>tres l&aacute;mparas iguales</b> y una bater&iacute;a de 4,5 V.</p>
          <ol class="pasos">
            <li><b>Montaje en serie.</b> Medid la corriente total y la tensi&oacute;n en cada l&aacute;mpara.
                Anotad tambi&eacute;n c&oacute;mo alumbran.</li>
            <li><b>Montaje en paralelo.</b> Las mismas medidas.</li>
            <li>En cada montaje, <b>retirad una l&aacute;mpara</b> (es la forma de simular que se funde) y
                anotad qu&eacute; pasa con las otras dos.</li>
            <li>Rellenad una tabla comparativa con: R<sub>T</sub> calculada, I total medida, V en
                cada l&aacute;mpara, y qu&eacute; ocurre al fundirse una.</li>
            <li><b>Comprobad las cuentas</b>: calculad R<sub>T</sub> con las f&oacute;rmulas y comparadla
                con V/I medidos. Si no coinciden, decid d&oacute;nde cre&eacute;is que est&aacute; el desajuste.</li>
            <li>Conclusi&oacute;n: &iquest;c&oacute;mo cablear&iacute;ais las luces de esta aula, y por qu&eacute;? Una raz&oacute;n
                t&eacute;cnica y una econ&oacute;mica.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Los dos montajes funcionan y est&aacute;n medidos <b>(3 puntos)</b>.</li>
            <li>La tabla comparativa est&aacute; completa, con unidades <b>(2 puntos)</b>.</li>
            <li>La prueba de la aver&iacute;a est&aacute; hecha en los dos montajes <b>(2 puntos)</b>.</li>
            <li>Las cuentas de R<sub>T</sub> cuadran con lo medido, o se explica por qu&eacute; no
                <b>(2 puntos)</b>.</li>
            <li>La conclusi&oacute;n da las dos razones, t&eacute;cnica y econ&oacute;mica <b>(1 punto)</b>.</li>
          </ul>
          <div class="nota" style="margin-top:14px">
            <span class="n-tag">Pista</span>
            En el montaje en paralelo, mirad el amper&iacute;metro <b>antes y despu&eacute;s</b> de quitar una
            l&aacute;mpara. Ese n&uacute;mero es toda la diferencia entre una instalaci&oacute;n bien calculada y un
            cable caliente.
          </div>
  ''')) +

  bloque('03', u'Cierre &middot; 5 min', u'''
      <p>Con lo de hoy ya puedes mirar una instalaci&oacute;n y decir, sin abrirla, c&oacute;mo est&aacute; cableada:
         si al fundirse una cosa cae todo, va en serie; si no, va en paralelo.</p>
      <ol>
      ''' + pregunta(u'Dos l&aacute;mparas de 6 &#8486; en serie con una pila de 12 V. &iquest;Resistencia total y corriente?',
                     u'<p>R<sub>T</sub> = 6 + 6 = <b>12 &#8486;</b>; I = 12 / 12 = <b>1 A</b>. Cada l&aacute;mpara recibe 6 V, la mitad de la pila.</p>')
        + pregunta(u'Las mismas dos l&aacute;mparas, ahora en paralelo con la misma pila. &iquest;Y ahora?',
                   u'<p>R<sub>T</sub> = 6 / 2 = <b>3 &#8486;</b>; I<sub>T</sub> = 12 / 3 = <b>4 A</b>. Cada l&aacute;mpara recibe los 12 V completos y toma 2 A. Cuatro veces m&aacute;s corriente que en serie.</p>')
        + pregunta(u'&iquest;Por qu&eacute; a Edison le sal&iacute;a m&aacute;s barato hacer l&aacute;mparas de resistencia alta?',
                   u'<p>Porque con m&aacute;s resistencia, la misma tensi&oacute;n da <b>menos corriente</b> (I = V/R), y menos corriente permite <b>cables de cobre m&aacute;s finos</b>. El cobre era una de las partidas m&aacute;s caras de la instalaci&oacute;n.</p>') + u'''
      </ol>

      <div class="copiar" style="border-color:var(--goo-verde)">
        <h4>Lectura del tema</h4>
        <p>Una sesi&oacute;n entera dedicada a leer y contestar. <b>31 p&aacute;rrafos numerados</b>: cada uno lee
           el suyo en voz alta, en orden. Despu&eacute;s, diez preguntas por escrito.</p>
        <p style="margin-top:10px"><a href="lectura-tema8.pdf" target="_blank" rel="noopener"
           style="font-family:var(--f-m);font-size:13px;color:var(--goo-verde);font-weight:500">
           &#8595; Un cable no hace nada &middot; PDF</a></p>
      </div>

      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        La corriente ya sabes calcularla y repartirla. Falta la pregunta que acaba
        llegando a casa en un papel: <b>&iquest;cu&aacute;nto cuesta tener esto encendido?</b> Para eso hacen
        falta dos conceptos nuevos, la <b>potencia</b> y el <b>consumo</b>.
      </div>
  '''))


# ==========================================================================
# SESION 4 - Potencia y consumo
# ==========================================================================
# La factura de ejemplo esta calculada, linea a linea, en el guion de trabajo:
#   10,35 + 45,00 = 55,35 -> +5,11 % de impuesto = 2,83 -> +0,81 de alquiler
#   -> base 58,99 -> +21 % de IVA = 12,39 -> TOTAL 71,38 EUR y 0,2855 EUR/kWh.
FACTURA_CSS = u'''
      <style>
        #factura-ej{width:100%;border-collapse:collapse;font:400 13.5px var(--f-m);margin:14px 0}
        #factura-ej th{text-align:left;font-weight:500;color:var(--ink-soft);font-size:11px;
          letter-spacing:.1em;text-transform:uppercase;padding:0 8px 6px 0;border-bottom:1.5px solid var(--ink)}
        #factura-ej td{padding:6px 8px 6px 0;border-bottom:1px solid var(--line-soft);color:var(--ink-soft)}
        #factura-ej td:last-child{text-align:right;color:var(--ink);white-space:nowrap}
        #factura-ej tr.suma td{color:var(--ink);font-weight:500}
        #factura-ej tr.total td{border-bottom:0;border-top:1.5px solid var(--ink);
          color:var(--ink);font-weight:500;font-size:15px}
      </style>
'''

S4 = (
  bloque('00', u'Reto inicial &middot; 10 min', u'''
      <p>Hasta aqu&iacute;, la corriente y su reparto. Hoy la electricidad
         deja de ser un dibujo en la libreta: hoy son <b>euros</b> y son <b>gramos de CO&#8322;</b>.</p>

      <div class="aviso">
        <span class="n-tag">El reto</span>
        <p style="margin:0">&iquest;Qu&eacute; gasta m&aacute;s electricidad: la <b>bombilla del pasillo</b> encendida
           toda la noche, o el <b>microondas</b> calentando un vaso de leche <b>cinco minutos</b>?
           Contesta en la libreta antes de seguir leyendo, y escribe por qu&eacute;.</p>
      </div>

      <p>Casi todo el mundo dice el microondas, y lo dice con un argumento que suena impecable: el
         microondas es <b>mil vatios</b> y la bombilla son nueve. Es m&aacute;s de cien veces m&aacute;s. No hay
         color.</p>
      <p>Hagamos la cuenta de verdad. Ocho horas de bombilla LED: 9 W durante 8 h son <b>72</b>
         unidades de algo. Cinco minutos de microondas: 1.000 W durante 5/60 de hora son <b>83</b>
         de ese mismo algo. <b>Gana el microondas, pero por los pelos</b>, no por cien veces.</p>
      <p>Y ahora cambia la bombilla por una de las viejas, de 60 W: 60 &times; 8 = <b>480</b>. Casi
         <b>seis veces</b> el microondas. La misma pregunta, la misma bombilla encendida el mismo
         rato, y la respuesta se da la vuelta.</p>

      <div class="reto-piensa">
        <span class="n-tag">Piensa antes de seguir</span>
        <p>Si con los vatios solos no se puede contestar, <b>&iquest;qu&eacute; hace falta?</b> Y una segunda,
           m&aacute;s fina: cuando en casa dicen &laquo;esta bombilla gasta mucho&raquo;, &iquest;est&aacute;n hablando de
           <b>vatios</b> o de otra cosa?</p>
      </div>

      <p>Hacen falta <b>dos</b> magnitudes, no una. Una dice <b>lo deprisa</b> que gastas, y es la
         que viene escrita en el aparato. La otra dice <b>lo que llevas gastado</b>, y es la que
         viene escrita en la factura. Confundirlas es el error que hace que una casa pague de m&aacute;s
         todos los meses.</p>
  ''') +

  bloque('01', u'Teor&iacute;a &middot; 20 min', u'''
      <h3>Lo deprisa que gastas: la potencia</h3>
      <p>En la sesi&oacute;n 2 te quedaste con dos n&uacute;meros: el empuj&oacute;n (V) y el caudal (I). Multiplicarlos
         no es un capricho de f&oacute;rmula: si empujas <b>m&aacute;s fuerte</b> y adem&aacute;s pasa <b>m&aacute;s
         cantidad</b>, la energ&iacute;a que entregas cada segundo crece por los dos lados a la vez.</p>

      <div class="copiar">
        <h4>Potencia el&eacute;ctrica</h4>
        <p><b>Potencia (P)</b>: energ&iacute;a que un aparato transforma <b>cada segundo</b>. Se mide en
           <b>vatios (W)</b>.</p>
        <p style="font-family:var(--f-m);font-size:17px;text-align:center;margin:10px 0">
           P = V &times; I</p>
        <p>Juntando la ley de Ohm salen las otras dos formas, &uacute;tiles cuando no tienes los dos datos:
           &nbsp;<b>P = I&sup2; &times; R</b>&nbsp; y &nbsp;<b>P = V&sup2; / R</b>.</p>
        <p><b>Ejemplo.</b> Un secador de 2.000 W enchufado a 230 V: &nbsp;I = P / V = 2.000 / 230 =
           <b>8,7 A</b>. Por eso los secadores llevan el cable gordo y los cargadores de m&oacute;vil no.</p>
      </div>

      <p>Y aqu&iacute; se cierra algo que qued&oacute; abierto en la sesi&oacute;n 2: <b>por el hilo del tostador y por
         su cable pasa la misma corriente, y solo uno se pone al rojo</b>. Ahora se puede decir con
         una f&oacute;rmula: como P = I&sup2; &times; R y la I es la misma en los dos, el que tiene
         <b>mucha R</b> se lleva casi toda la potencia. El hilo del tostador tiene mucha; el cable de
         cobre, casi ninguna. Ese es exactamente el motivo de que los cables no calienten y las
         resistencias s&iacute;.</p>

      <h3>Lo que llevas gastado: la energ&iacute;a</h3>
      <p>La potencia no dice nada del rato. Para saber lo que has gastado hay que multiplicarla por
         el <b>tiempo</b>, que es justo lo que le faltaba a la pregunta del principio.</p>

      <div class="copiar">
        <h4>Energ&iacute;a y kilovatio-hora</h4>
        <p><b>Energ&iacute;a (E) = P &times; t</b>. En el Sistema Internacional se mide en <b>julios</b>:
           un vatio durante un segundo es un julio.</p>
        <p>El problema del julio es que es <b>rid&iacute;culamente peque&ntilde;o</b> para una casa. Por eso la
           factura usa otra unidad, hecha a la medida del consumo dom&eacute;stico:</p>
        <p style="font-family:var(--f-m);font-size:15px;text-align:center;margin:10px 0">
           1 kWh = 1.000 W durante 1 hora = <b>3.600.000 julios</b></p>
        <p>Para trabajar con ella, la regla pr&aacute;ctica:</p>
        <p style="font-family:var(--f-m);font-size:15px;text-align:center;margin:10px 0">
           E (kWh) = P (kW) &times; t (h) &nbsp;&middot;&nbsp; coste = E &times; precio del kWh</p>
        <p>Ojo con las unidades: la potencia en <b>kilovatios</b> (2.000 W son 2 kW) y el tiempo en
           <b>horas</b> (15 minutos son 0,25 h). Mezclarlas es el fallo m&aacute;s frecuente.</p>
      </div>

      <h3>Por qu&eacute; salta la luz cuando enchufas dos cosas grandes</h3>
      <p>En la sesi&oacute;n anterior viste que en tu casa todo est&aacute; <b>en paralelo</b>: cada aparato
         recibe los mismos 230 V y las corrientes <b>se suman</b>. Si las corrientes se suman y
         P = V &times; I, entonces las <b>potencias tambi&eacute;n se suman</b>. Mira lo que pasa cuando te
         pasas.</p>
''' + ESC_REGLETA + u'''
      <p>Dos l&iacute;mites distintos, y conviene no mezclarlos. El primero es el <b>cable</b>: una base
         de enchufe normal es de <b>16 A</b>, o sea 16 &times; 230 = <b>3.680 W</b>; pasar de ah&iacute; no
         hace saltar nada, simplemente calienta el cable de la regleta. El segundo es la
         <b>potencia contratada</b>: cuando la pasas, el interruptor de control abre el circuito y
         te quedas a oscuras. Y f&iacute;jate en un detalle bonito de las potencias que se contratan:
         3,45 kW son exactamente <b>15 A</b>, y 4,6 kW son <b>20 A</b>. No son n&uacute;meros raros, son
         amperios redondos disfrazados de kilovatios.</p>

      <h3>La factura: d&oacute;nde est&aacute; el dinero</h3>
      <p>Una factura de la luz no es una lista de precios: es <b>dos alquileres sumados</b>. Uno por
         lo que consumes y otro por estar conectado, que se paga aunque te vayas todo el mes de
         viaje. Esta es una factura de ejemplo de un mes de 30 d&iacute;as, con 250 kWh consumidos.</p>
''' + FACTURA_CSS + u'''
      <table id="factura-ej">
        <thead><tr><th>Concepto</th><th>C&oacute;mo sale</th><th>Importe</th></tr></thead>
        <tbody>
          <tr><td>T&eacute;rmino de potencia</td>
              <td>3,45 kW &times; 30 d&iacute;as &times; 0,10 &euro;/kW&middot;d&iacute;a</td><td>10,35 &euro;</td></tr>
          <tr><td>T&eacute;rmino de energ&iacute;a</td>
              <td>250 kWh &times; 0,18 &euro;/kWh</td><td>45,00 &euro;</td></tr>
          <tr class="suma"><td>Suma de los dos t&eacute;rminos</td><td></td><td>55,35 &euro;</td></tr>
          <tr><td>Impuesto el&eacute;ctrico</td><td>5,11 % de 55,35</td><td>2,83 &euro;</td></tr>
          <tr><td>Alquiler del contador</td><td>0,027 &euro;/d&iacute;a &times; 30</td><td>0,81 &euro;</td></tr>
          <tr class="suma"><td>Base imponible</td><td></td><td>58,99 &euro;</td></tr>
          <tr><td>IVA</td><td>21 % de 58,99</td><td>12,39 &euro;</td></tr>
          <tr class="total"><td>Total a pagar</td><td>30 d&iacute;as, 250 kWh</td><td>71,38 &euro;</td></tr>
        </tbody>
      </table>
      <p>Y ahora la pregunta que cambia las decisiones de una casa: <b>&iquest;a cu&aacute;nto te ha salido de
         verdad el kWh?</b> No a 0,18. Divide el total entre los kWh consumidos: 71,38 / 250 =
         <b>0,2855 &euro;/kWh</b>. Un <b>59 % m&aacute;s</b> que el precio que ven&iacute;a anunciado. Todo lo que
         calcules con el precio de la tarifa te saldr&aacute; corto.</p>
      <p>El dato sirve de contraste: seg&uacute;n <b>Eurostat</b>, los hogares espa&ntilde;oles que consumen entre
         2.500 y 5.000 kWh al a&ntilde;o &mdash;esta casa, justo&mdash; pagaron de media <b>0,2669 &euro;/kWh</b>
         con todos los impuestos incluidos en el segundo semestre de 2025. Nuestra factura de ejemplo
         cae donde tiene que caer.</p>

      <div class="copiar">
        <h4>Leer una factura</h4>
        <ul>
          <li><b>T&eacute;rmino de potencia</b>: se paga por los <b>kW contratados y los d&iacute;as</b>, gastes
              o no gastes. Contratar de m&aacute;s es pagar de m&aacute;s todos los d&iacute;as del a&ntilde;o.</li>
          <li><b>T&eacute;rmino de energ&iacute;a</b>: se paga por los <b>kWh</b> que marca el contador.</li>
          <li>Encima van los <b>impuestos</b> y el alquiler del contador.</li>
          <li><b>Precio real del kWh = total &divide; kWh consumidos.</b> Es el &uacute;nico n&uacute;mero con el
              que merece la pena calcular.</li>
        </ul>
        <p style="font-size:13.5px;color:var(--ink-soft);margin-bottom:0">Los porcentajes de esta
           factura son los vigentes en <b>septiembre de 2026</b> (IVA del 21 % e impuesto el&eacute;ctrico
           del 5,11 %) y han cambiado varias veces en los &uacute;ltimos a&ntilde;os. Los precios de los dos
           t&eacute;rminos son de ejemplo: los tuyos est&aacute;n en tu contrato.</p>
      </div>

      <h3>La etiqueta energ&eacute;tica: la letra y el n&uacute;mero</h3>
      <p>Desde el <b>1 de marzo de 2021</b> los electrodom&eacute;sticos vuelven a llevar una escala simple
         de la <b>A a la G</b>, sin los antiguos A+, A++ y A+++, que hab&iacute;an acabado amontonando a
         casi todos los aparatos en la misma casilla. Lo regula el <b>Reglamento (UE) 2017/1369</b>.</p>
      <p>De la etiqueta hay que mirar dos cosas, y la segunda es la que se ignora casi siempre:</p>
      <ul>
        <li>La <b>letra</b> solo sirve para comparar aparatos <b>del mismo tipo</b>. Un frigor&iacute;fico A
            y un horno A no tienen nada que ver.</li>
        <li>El <b>n&uacute;mero</b> de debajo es el que sirve para calcular: <b>kWh al a&ntilde;o</b> en
            frigor&iacute;ficos, <b>kWh por cada 100 ciclos</b> en lavadoras, lavavajillas y secadoras.</li>
      </ul>
      <p><b>Hagamos la cuenta.</b> Dos frigor&iacute;ficos del mismo tama&ntilde;o, uno de 148 kWh/a&ntilde;o y otro de
         296. La diferencia son <b>148 kWh al a&ntilde;o</b>, que a 0,27 &euro;/kWh son <b>39,96 &euro; cada
         a&ntilde;o</b>, y unos <b>38 kg de CO&#8322;</b>. Si el bueno cuesta 120 &euro; m&aacute;s en la tienda, se
         paga solo en <b>tres a&ntilde;os</b>; y un frigor&iacute;fico dura quince.</p>

      <div class="copiar">
        <h4>De los kWh al CO&#8322;</h4>
        <p>Cada kWh que gastas tiene detr&aacute;s unas emisiones, que dependen de con qu&eacute; se ha generado
           esa electricidad. Para el <b>mix el&eacute;ctrico espa&ntilde;ol</b>, la CNMC public&oacute; para la energ&iacute;a
           producida en <b>2025</b> un valor de <b>258 g de CO&#8322;eq por kWh</b>.</p>
        <p style="font-family:var(--f-m);font-size:15px;text-align:center;margin:10px 0">
           CO&#8322; = E (kWh) &times; 258 g/kWh</p>
        <p style="font-size:13.5px;color:var(--ink-soft);margin-bottom:0">Ese n&uacute;mero <b>baja cada
           a&ntilde;o</b> seg&uacute;n entran renovables: en 2015 estaba en 398 g/kWh. Y ojo, es el mix de la red:
           una comercializadora que venda electricidad 100 % renovable certificada declara un valor
           distinto en tu factura.</p>
      </div>

      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; no hace falta copiarlo</span>
        <p>&iquest;Y c&oacute;mo se cuenta un kWh? Durante casi un siglo, con un aparato que hace la
           multiplicaci&oacute;n <b>a mano y sin electr&oacute;nica</b>: el contador de inducci&oacute;n. Dentro hay un
           disco de aluminio entre dos bobinas, una recorrida por la <b>tensi&oacute;n</b> y otra por la
           <b>corriente</b>. El campo de las dos arrastra el disco, y el disco gira tanto m&aacute;s deprisa
           cuanto mayor es el producto V &times; I. O sea, <b>la velocidad del disco es la
           potencia</b>, y las <b>vueltas acumuladas</b> son la energ&iacute;a.</p>
        <p>Por eso un contador viejo lleva escrito algo como <i>375 U/kWh</i>: trescientas setenta y
           cinco vueltas del disco por cada kilovatio-hora. Con un cron&oacute;metro y esa cifra se puede
           medir la potencia de un aparato sin ning&uacute;n instrumento m&aacute;s: se cuenta cu&aacute;nto tarda en dar
           diez vueltas y se hace una regla de tres.</p>
        <p>Los contadores digitales de ahora ya no tienen disco: multiplican V por I muchas veces por
           segundo y suman. Pero conservan la costumbre de anunciar su constante en la placa, ahora
           en forma de <b>impulsos por kWh</b> del piloto que parpadea.</p>
      </div>

      <div class="galeria-ri">
        <figure class="foto">
          <img src="../../../img/u6-contador-viejo.jpg" loading="lazy"
               alt="Contador el&eacute;ctrico Siemens de inducci&oacute;n, con ruedas num&eacute;ricas marcando 65521,9 kWh
                    y un disco met&aacute;lico girando bajo ellas">
          <figcaption>El contador de <b>inducci&oacute;n</b>, el d&iacute;a antes de que lo retiraran. Lleva
            contados <b>65.521,9 kWh</b>. En la placa, los datos que ahora sabes leer: <b>220 V</b>,
            <b>10 (60) A</b> y <b>375 U/kWh</b> &mdash;375 vueltas del disco por cada kilovatio-hora&mdash;.
            <span class="credito">RobbieIanMorrison &middot; CC BY 4.0 &middot;
              <a href="https://commons.wikimedia.org/wiki/File:Siemens_household_electricity_meter_electromechanical_induction_type.jpg"
                 target="_blank" rel="noopener">Wikimedia Commons</a></span>
          </figcaption>
        </figure>
        <figure class="foto">
          <img src="../../../img/u6-contador-nuevo.jpg" loading="lazy"
               alt="Contador el&eacute;ctrico digital moderno con una pantalla que marca 000000 kWh">
          <figcaption>Y el digital que ocup&oacute; su sitio, reci&eacute;n instalado: <b>000000 kWh</b>,
            empezando de cero. Misma placa, otros n&uacute;meros: <b>230 V</b>, <b>50 Hz</b> y
            <b>500 impulsos/kWh</b> en vez de vueltas.
            <span class="credito">RobbieIanMorrison &middot; CC BY 4.0 &middot;
              <a href="https://commons.wikimedia.org/wiki/File:Logarex_smart_household_electricity_meter_build_year_2023.jpg"
                 target="_blank" rel="noopener">Wikimedia Commons</a></span>
          </figcaption>
        </figure>
      </div>
      <p style="font-size:13.5px;color:var(--ink-soft)">Las dos fotos son del mismo cuadro de una
         vivienda de Berl&iacute;n, tomadas con un d&iacute;a de diferencia: la del contador viejo, la v&iacute;spera
         de retirarlo; la del nuevo, el d&iacute;a de instalarlo. All&iacute; la red es la misma que aqu&iacute;
         &mdash;230 V y 50 Hz&mdash;, as&iacute; que lo que se lee en las placas vale igual para un
         contador espa&ntilde;ol. Y f&iacute;jate en un detalle: el viejo dice <b>220 V</b> y el nuevo
         <b>230 V</b>. No es un error de ninguno de los dos: la red europea estaba a 220 V y se
         armoniz&oacute; en 230 V, as&iacute; que el aparato viejo es de antes de aquello.</p>
''' + video('9qWYeA5y_r0', u'Potencia y energ&iacute;a el&eacute;ctrica: &iquest;cu&aacute;nto costar&aacute;?',
            u'Ruben Sebastian',
            u'Otra explicaci&oacute;n de lo mismo, con ejercicios resueltos. Antes de darle al play, '
            u'calcula t&uacute; lo que cuesta tener encendida la luz de tu habitaci&oacute;n tres horas al d&iacute;a '
            u'durante un mes: as&iacute; el v&iacute;deo te corrige en vez de cont&aacute;rtelo.')) +

  bloque('02', u'Pr&aacute;ctica &middot; 25 min', ficha(
    u'Actividad 4 &middot; La factura, y lo que cuesta tu habitaci&oacute;n',
    [u'3.1', u'A.6'], u'Parejas &middot; 25 min', u'''
          <h4>Qu&eacute; hay que hacer</h4>
          <p>Con calculadora y con la escena de la regleta abierta. No hace falta traer ninguna
             factura de casa: la de ejemplo de la teor&iacute;a tiene todos los datos.</p>
          <ol class="pasos">
            <li><b>Comprobad la factura</b> de la teor&iacute;a l&iacute;nea a l&iacute;nea. Rehaced las siete
                operaciones y decid si el total est&aacute; bien. Copiad cada operaci&oacute;n, no solo el
                resultado.</li>
            <li>Calculad el <b>precio real del kWh</b> (total &divide; kWh) y decid cu&aacute;nto se
                equivocar&iacute;a alguien que hiciera sus cuentas con los 0,18 &euro;/kWh de la tarifa.</li>
            <li><b>Inventario de tu habitaci&oacute;n</b>: elegid <b>cuatro aparatos</b>, buscad su
                potencia en la placa de caracter&iacute;sticas o en el cargador (si no la ten&eacute;is a mano,
                usad las de la escena) y estimad las horas que funcionan al d&iacute;a.</li>
            <li>Tabla: aparato &middot; P (W) &middot; h/d&iacute;a &middot; kWh/mes &middot; &euro;/mes &middot;
                g CO&#8322;/mes. Usad el <b>precio real</b> del paso 2 y los 258 g/kWh.</li>
            <li><b>Una decisi&oacute;n.</b> Elegid el aparato que m&aacute;s gasta y proponed un cambio concreto
                (sustituirlo, usarlo menos, apagarlo de otra forma). Calculad cu&aacute;nto se ahorra al
                a&ntilde;o <b>en euros y en kg de CO&#8322;</b>.</li>
            <li>En la escena, encontrad una combinaci&oacute;n de aparatos que <b>caliente la regleta sin
                que salte el autom&aacute;tico</b>, y otra que lo haga saltar. Anotad las dos y explicad
                la diferencia en dos l&iacute;neas.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Las siete operaciones de la factura est&aacute;n rehechas y bien <b>(2 puntos)</b>.</li>
            <li>El precio real del kWh est&aacute; calculado y comparado con el de la tarifa
                <b>(2 puntos)</b>.</li>
            <li>La tabla de los cuatro aparatos est&aacute; completa, con <b>unidades correctas</b>
                <b>(3 puntos)</b>.</li>
            <li>La decisi&oacute;n del paso 5 viene con su ahorro calculado, no con una opini&oacute;n
                <b>(2 puntos)</b>.</li>
            <li>Las dos combinaciones de la escena est&aacute;n anotadas y explicadas <b>(1 punto)</b>.</li>
          </ul>
          <div class="nota" style="margin-top:14px">
            <span class="n-tag">Cuidado con esto</span>
            Un fallo de unidades cuesta la mitad del ejercicio: la potencia va en <b>kW</b> y el
            tiempo en <b>horas</b>. 1.500 W son 1,5 kW, y 20 minutos son 0,33 h. Si en alguna
            casilla os sale un n&uacute;mero absurdo &mdash;una bombilla que cuesta 300 &euro; al mes&mdash;,
            no lo tach&eacute;is: escribid al lado qu&eacute; unidad hab&eacute;is mezclado.
          </div>
  ''')) +

  bloque('03', u'Cierre &middot; 5 min', u'''
      <p>La bombilla del pasillo y el microondas ya se pueden comparar, y no hace falta discutir:
         se multiplica y se mira.</p>
      <ol>
      ''' + pregunta(u'Una estufa de 1.500 W funciona 4 horas al d&iacute;a durante 20 d&iacute;as. &iquest;Cu&aacute;nta energ&iacute;a gasta y cu&aacute;nto cuesta a 0,27 &euro;/kWh?',
                     u'<p>E = 1,5 kW &times; 4 h &times; 20 d&iacute;as = <b>120 kWh</b>. Coste = 120 &times; 0,27 = <b>32,40 &euro;</b>. Y de paso: 120 &times; 258 = <b>31,0 kg de CO&#8322;</b>.</p>')
        + pregunta(u'&iquest;Qu&eacute; corriente pide una vitrocer&aacute;mica de 2.300 W a 230 V? &iquest;Se puede enchufar a una regleta junto a un secador de 2.000 W?',
                   u'<p>I = P / V = 2.300 / 230 = <b>10 A</b>. Con el secador ser&iacute;an 10 + 8,7 = <b>18,7 A</b>, por encima de los <b>16 A</b> de la base: el cable de la regleta se calentar&iacute;a. Y adem&aacute;s 4.300 W superan la potencia contratada m&aacute;s habitual, as&iacute; que probablemente saltar&iacute;a el autom&aacute;tico antes.</p>')
        + pregunta(u'Un frigor&iacute;fico de clase A y otro de clase F. &iquest;Qu&eacute; dato de la etiqueta te dice lo que vas a pagar, la letra o el n&uacute;mero?',
                   u'<p>El <b>n&uacute;mero</b>: los <b>kWh al a&ntilde;o</b>. La letra solo te dice si es de los buenos o de los malos <b>dentro de su familia</b>, y no se puede multiplicar por el precio del kWh. Con el n&uacute;mero s&iacute;: (kWh/a&ntilde;o) &times; precio = euros al a&ntilde;o.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Todo lo que has encendido hasta ahora ha sido una l&aacute;mpara, y una l&aacute;mpara aguanta lo que le
        eches: si le das poco alumbra poco y si le das de m&aacute;s se funde y ya est&aacute;. La pr&oacute;xima
        sesi&oacute;n montas un componente que <b>no perdona</b>: se rompe en el primer segundo si no
        haces la cuenta antes. Es el <b>LED</b>, y est&aacute; en todas las pantallas que miras.
      </div>
  '''))


# ==========================================================================
# SESION 5 - El LED y su resistencia, el pulsador y el interruptor
# ==========================================================================
S5 = (
  bloque('00', u'Reto inicial &middot; 10 min', u'''
      <p>Encima de la mesa, una pila de petaca y un <b>LED</b>. Nada m&aacute;s.</p>

      <div class="aviso">
        <span class="n-tag">El reto</span>
        <p style="margin:0 0 8px">Dibuja en la libreta c&oacute;mo lo conectar&iacute;as para que se encienda.
           Tienes treinta segundos: es el mismo circuito de la primera sesi&oacute;n cambiando la l&aacute;mpara
           por el LED.</p>
        <p style="margin:0"><b>No lo montes todav&iacute;a.</b> Sigue leyendo.</p>
      </div>

      <p>Ese dibujo est&aacute; bien y es exactamente lo que no hay que hacer. Si lo montas, el LED se
         enciende <b>un instante</b> &mdash;a veces ni eso&mdash; y se queda muerto para siempre. No se
         funde como una bombilla, con su filamento partido y su ruidito: simplemente deja de
         alumbrar, y por fuera sigue igual de nuevo.</p>
      <p>Y en la mesa de al lado alguien ha puesto <b>una resistencia</b> en serie y el suyo luce
         perfectamente. Pregunta obligada: &iquest;cu&aacute;l ha puesto? La respuesta que suele salir es
         &laquo;una que hab&iacute;a en la caja&raquo;. As&iacute; que a veces luce, a veces alumbra tan poco que no se ve,
         y a veces se muere igual.</p>

      <div class="reto-piensa">
        <span class="n-tag">Piensa antes de seguir</span>
        <p>Dos preguntas. La primera: <b>&iquest;por qu&eacute; la l&aacute;mpara aguanta y el LED no</b>, si los dos
           est&aacute;n conectados a la misma pila? La segunda, la importante: si hay que ponerle una
           resistencia, <b>&iquest;de cu&aacute;ntos ohmios?</b> Y sobre todo, <b>&iquest;de d&oacute;nde sale ese
           n&uacute;mero?</b></p>
      </div>

      <p>Pista de la sesi&oacute;n 2, donde ya lo avisamos sin darle importancia: la gr&aacute;fica de la ley de
         Ohm es una recta <b>en un conductor met&aacute;lico</b>, y dijimos que en un LED <b>no lo es</b>.
         Ah&iacute; est&aacute; todo el problema de hoy.</p>
  ''') +

  bloque('01', u'Teor&iacute;a &middot; 20 min', u'''
      <h3>Un LED no es una bombilla peque&ntilde;a</h3>
      <p>Un LED es un <b>diodo</b>: un componente que deja pasar la corriente en <b>un solo
         sentido</b>. Si lo conectas al rev&eacute;s no es que alumbre menos, es que no pasa nada en
         absoluto. Por eso sus dos patas no son intercambiables y tiene dos maneras de dec&iacute;rtelo:
         la <b>pata larga es el &aacute;nodo</b> (por ah&iacute; entra la corriente, al polo +) y el borde de la
         c&aacute;psula tiene un <b>chafl&aacute;n plano</b> junto al <b>c&aacute;todo</b> (al polo &minus;).</p>
      <p>Pero lo que de verdad lo diferencia de una l&aacute;mpara es esto: <b>el LED no tiene un valor de
         resistencia</b>. Una l&aacute;mpara de 9 &#8486; tiene 9 &#8486; le pongas la tensi&oacute;n que le pongas
         (mientras no cambie mucho de temperatura), y por eso puedes calcular su corriente con la ley
         de Ohm. Un LED, no. Un LED se comporta as&iacute;:</p>
      <ul>
        <li>Por debajo de cierta tensi&oacute;n, llamada <b>tensi&oacute;n directa</b> (V<sub>f</sub>),
            pr&aacute;cticamente <b>no conduce</b> y no alumbra.</li>
        <li>En cuanto la pasas, la corriente <b>se dispara</b>: unas d&eacute;cimas de voltio de m&aacute;s
            multiplican la corriente por diez.</li>
      </ul>
      <p>Por eso conectarlo directamente a 4,5 V es una sentencia: la pila empuja con 4,5 y el LED
         &laquo;solo quiere&raquo; unos 2, as&iacute; que la corriente sube hasta que algo se rompe. Y por eso mismo
         <b>no puedes calcular la corriente del LED con la ley de Ohm</b>: no hay una R que poner.</p>

      <div class="copiar">
        <h4>El diodo LED</h4>
        <ul>
          <li><b>Conduce en un solo sentido.</b> Pata larga = &aacute;nodo (+). Chafl&aacute;n = c&aacute;todo (&minus;).</li>
          <li>Tiene una <b>tensi&oacute;n directa V<sub>f</sub></b> que depende del <b>color</b>, y que
              apenas cambia aunque cambie la corriente.</li>
          <li><b>No es &oacute;hmico</b>: su corriente no es proporcional a la tensi&oacute;n, as&iacute; que hay que
              <b>limitarla desde fuera</b>.</li>
          <li>Un LED de 5 mm de los normales trabaja bien entre <b>5 y 20 mA</b>. Por encima
              alumbra m&aacute;s y dura mucho menos.</li>
        </ul>
        <h4>Tensiones directas t&iacute;picas</h4>
        <p>Rojo <b>2,0 V</b> &middot; amarillo <b>2,1 V</b> &middot; verde <b>2,2 V</b> &middot; azul y
           blanco <b>3,2 V</b>. Son valores t&iacute;picos para orientarse: el de tu LED est&aacute; en su
           <b>hoja de caracter&iacute;sticas</b>, y dos LED del mismo color de fabricantes distintos pueden
           diferir en varias d&eacute;cimas.</p>
      </div>

      <h3>La resistencia limitadora, y de d&oacute;nde sale su n&uacute;mero</h3>
      <p>La soluci&oacute;n no es un truco: es la ley de Ohm aplicada donde s&iacute; vale. Pon una resistencia
         <b>en serie</b> con el LED. Est&aacute;n en serie, luego por los dos pasa la <b>misma
         corriente</b>, y la tensi&oacute;n de la pila <b>se reparte</b> entre los dos &mdash;exactamente lo
         que viste en la sesi&oacute;n 3&mdash;. Como el LED se queda con su V<sub>f</sub> pase lo que pase,
         <b>todo lo dem&aacute;s cae en la resistencia</b>.</p>
      <p>Y en la resistencia s&iacute; puedes usar Ohm, porque la resistencia s&iacute; es &oacute;hmica. As&iacute; que t&uacute;
         <b>decides</b> la corriente que quieres, y despejas:</p>

      <div class="copiar">
        <h4>C&aacute;lculo de la resistencia limitadora</h4>
        <p style="font-family:var(--f-m);font-size:17px;text-align:center;margin:10px 0">
           R = (V<sub>fuente</sub> &minus; V<sub>f</sub>) / I</p>
        <p>Con la tensi&oacute;n en <b>voltios</b> y la corriente en <b>amperios</b> (10 mA son 0,010 A).</p>
        <p><b>Ejemplo.</b> LED rojo (2,0 V) en un pin de la micro:bit (3 V), y queremos 5 mA:</p>
        <ul>
          <li>Tensi&oacute;n que sobra: 3 &minus; 2,0 = <b>1,0 V</b>.</li>
          <li>R = 1,0 / 0,005 = <b>200 &#8486;</b>.</li>
          <li>De 200 &#8486; no hay: el valor normalizado m&aacute;s pr&oacute;ximo <b>por encima</b> es
              <b>220 &#8486;</b>.</li>
          <li>Con 220 &#8486; la corriente real es 1,0 / 220 = <b>4,5 mA</b>. Perfecto.</li>
        </ul>
        <p><b>Siempre hacia arriba.</b> Si eliges el valor de debajo pasar&aacute; <b>m&aacute;s</b> corriente de
           la que hab&iacute;as decidido, que es justo de lo que te estabas protegiendo.</p>
      </div>

      <p>Eso de que &laquo;de 200 &#8486; no hay&raquo; no es una pega de la tienda del barrio: las resistencias
         se fabrican en <b>series de valores normalizados</b>. La m&aacute;s com&uacute;n en el aula es la
         <b>E12</b>, que solo tiene doce valores por cada d&eacute;cada &mdash;10, 12, 15, 18, 22, 27, 33, 39,
         47, 56, 68 y 82&mdash; multiplicados por 1, 10, 100, 1.000&hellip; De un valor al siguiente hay
         un salto de un 20 % largo, y cada resistencia se fabrica con una tolerancia de
         <b>&plusmn;10 %</b>: una de 100 &#8486; puede ser en realidad de 110 y una de 120 puede ser de
         108. Los m&aacute;rgenes de dos valores vecinos <b>se tocan</b>, as&iacute; que fabricar valores
         intermedios no servir&iacute;a de nada.</p>

      <p>Prueba aqu&iacute; todas las combinaciones que quieras. La escena hace la cuenta entera y luego
         busca la resistencia que existe de verdad. Y el mando de abajo funciona como el que
         elijas: el <b>pulsador</b> solo alumbra <b>mientras lo tienes apretado</b>.</p>
''' + ESC_LED + u'''
      <p>Tres cosas que merece la pena que pruebes ah&iacute; antes de seguir: pon un <b>LED azul en la
         micro:bit</b> y mira por qu&eacute; no hay resistencia que lo arregle; <b>quita la resistencia</b>
         y lee lo que dice el pie; y pasa del pulsador al interruptor para ver la diferencia con el
         dedo, no con la definici&oacute;n.</p>

      <h3>Pulsador e interruptor: parecen lo mismo y no lo son</h3>
      <p>Los dos abren y cierran un circuito. La diferencia est&aacute; en <b>qu&eacute; hacen cuando los
         sueltas</b>, y es una diferencia mec&aacute;nica: el pulsador lleva un <b>muelle</b> dentro.</p>

      <div class="copiar">
        <h4>Los dos elementos de control</h4>
        <ul>
          <li><b>Interruptor</b>: es <b>biestable</b>. Se queda como lo dejes, abierto o cerrado, sin
              que nadie lo sujete. La luz del techo, la l&aacute;mpara de la mesilla.</li>
          <li><b>Pulsador</b>: vuelve solo a su posici&oacute;n de reposo. El m&aacute;s com&uacute;n es el
              <b>normalmente abierto (NA)</b>: cerrado mientras lo aprietas, abierto en cuanto lo
              sueltas. El timbre, el claxon, cada tecla del teclado.</li>
          <li>Tambi&eacute;n hay pulsadores <b>normalmente cerrados (NC)</b>, que hacen lo contrario: el
              bot&oacute;n que detecta que la puerta del frigor&iacute;fico se ha cerrado y apaga la luz.</li>
        </ul>
        <p>Regla para elegir: si lo que mandas tiene que <b>pararse cuando sueltes</b>, pulsador. Si
           tiene que <b>quedarse</b>, interruptor. Un timbre con interruptor suena hasta que alguien
           vuelve a subir; una l&aacute;mpara con pulsador se apaga en cuanto quitas el dedo.</p>
      </div>

      <h3>Con la micro:bit</h3>
      <p>En 2.&ordm; la placa que usamos es la <b>micro:bit</b>. Para lo de hoy nos interesa solo su
         borde inferior: los <b>cinco anillos grandes</b>, que son los que se pinzan con cocodrilo.
         Tres son pines de trabajo (<b>P0</b>, <b>P1</b> y <b>P2</b>) y los otros dos son la
         alimentaci&oacute;n (<b>3V</b> y <b>GND</b>).</p>
      <p>Dos n&uacute;meros que hay que respetar, y que da el propio fabricante: los pines trabajan a
         <b>3 V</b> y cada uno puede dar como mucho <b>5 mA</b>. Con esos dos datos y la f&oacute;rmula de
         arriba ya tienes tu resistencia: 220 &#8486; para un LED rojo. Y tambi&eacute;n tienes la
         explicaci&oacute;n de algo que descubrir&aacute;s en cuanto lo pruebes: un <b>LED azul o blanco no
         funciona</b> en un pin de la micro:bit, porque pide 3,2 V y la placa solo da 3.</p>
      <p>La micro:bit trae adem&aacute;s <b>dos pulsadores ya montados</b>, el A y el B, as&iacute; que para
         empezar no hace falta ni cablear uno.</p>

      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; no hace falta copiarlo</span>
        <p>&iquest;Por qu&eacute; el azul pide m&aacute;s tensi&oacute;n que el rojo? Porque en un LED <b>el color y la
           tensi&oacute;n son la misma cosa vista dos veces</b>. La luz sale cuando una carga cae de un
           escal&oacute;n de energ&iacute;a al de abajo, y la altura de ese escal&oacute;n decide a la vez el
           <b>color</b> del fot&oacute;n que sale y la <b>tensi&oacute;n</b> que hace falta para subir la carga
           ah&iacute;. Azul es m&aacute;s energ&iacute;a por fot&oacute;n que rojo; luego m&aacute;s voltios. No es una casualidad
           del fabricante: no se puede hacer un LED azul de 2 V.</p>
        <p>Y ah&iacute; est&aacute; la historia. Rojos hab&iacute;a desde 1962, y verdes y amarillos poco despu&eacute;s. El
           azul se resisti&oacute; <b>treinta a&ntilde;os</b>: hac&iacute;a falta un material capaz de dar ese escal&oacute;n
           tan alto y que adem&aacute;s se pudiera fabricar sin defectos, y nadie lo consegu&iacute;a. Lo
           resolvieron a principios de los noventa <b>Isamu Akasaki, Hiroshi Amano y Shuji
           Nakamura</b> con nitruro de galio, y por eso les dieron el <b>Nobel de F&iacute;sica de
           2014</b>.</p>
        <p>Que suene a poco: sin azul <b>no hay blanco</b>, porque la luz blanca de un LED se fabrica
           poniendo un f&oacute;sforo amarillo delante de un chip azul. Sin aquel invento no existir&iacute;an ni
           las bombillas LED de tu casa ni la pantalla desde la que lees esto, y la sesi&oacute;n anterior
           &mdash;la de los 9 W frente a los 60 W&mdash; no tendr&iacute;a de qu&eacute; hablar.</p>
      </div>

      <div class="galeria-ri">
        <figure class="foto">
          <img src="../../../img/u6-led.jpg" loading="lazy"
               alt="Diodo LED rojo de 5 mil&iacute;metros con sus dos patas met&aacute;licas, sobre fondo blanco">
          <figcaption>Un <b>LED rojo de 5 mm</b>, el que vas a montar. La c&aacute;psula de pl&aacute;stico no es
            solo una carcasa: hace de lente y de color. En este ejemplar las dos patas est&aacute;n cortadas
            casi a la misma altura, y entonces <b>ya no puedes fiarte de la pata larga</b>: hay que
            buscar el chafl&aacute;n del borde, que marca el c&aacute;todo.
            <span class="credito">oomlout &middot; CC BY-SA 2.0 &middot;
              <a href="https://commons.wikimedia.org/wiki/File:5mm_Red_LED.jpg"
                 target="_blank" rel="noopener">Wikimedia Commons</a></span>
          </figcaption>
        </figure>
        <figure class="foto">
          <img src="../../../img/u6-microbit.jpg" loading="lazy"
               alt="Placa micro:bit v2 vista por detr&aacute;s, con los cinco anillos grandes del conector
                    de borde en la parte inferior">
          <figcaption>La <b>micro:bit v2</b> por detr&aacute;s. Abajo se ven los <b>cinco anillos
            grandes</b> del conector de borde: son P0, P1, P2, 3V y GND, y est&aacute;n rotulados por la
            otra cara. Los dientes dorados finos de entre medias son otros veinte contactos que solo
            se alcanzan con un conector especial.
            <span class="credito">SimonWaldherr &middot; CC BY 4.0 &middot;
              <a href="https://commons.wikimedia.org/wiki/File:BBC_micro_bit_v2.jpg"
                 target="_blank" rel="noopener">Wikimedia Commons</a></span>
          </figcaption>
        </figure>
      </div>
''' + video('Bw4nVt8eQkw', u'C&oacute;mo calcular la resistencia para un LED (ley de Ohm f&aacute;cil)',
            u'ITC MENTOR Academy',
            u'La misma cuenta que acabas de hacer, contada por otra persona. Ve con la libreta '
            u'delante y comprueba que usa <b>exactamente</b> la misma f&oacute;rmula: tensi&oacute;n de la fuente '
            u'menos tensi&oacute;n del LED, dividido entre la corriente que t&uacute; decides.')) +

  bloque('02', u'Pr&aacute;ctica &middot; 25 min', ficha(
    u'Actividad 5 &middot; Calcula, monta y mide',
    [u'3.1', u'A.6'], u'Parejas &middot; 25 min', u'''
          <h4>Qu&eacute; hay que hacer</h4>
          <p>Con material de verdad si lo hay (micro:bit o pila, LED, resistencias, pulsador,
             interruptor y pinzas de cocodrilo) y, si no, en
             <a href="https://www.tinkercad.com/circuits" target="_blank" rel="noopener">Tinkercad
             Circuits</a>. <b>El orden no es negociable: primero la cuenta, luego el montaje.</b></p>
          <ol class="pasos">
            <li><b>La cuenta, en la libreta.</b> Con la fuente que os toque y el color de LED que os
                den: escribid V<sub>fuente</sub>, V<sub>f</sub>, la corriente que eleg&iacute;s y el
                c&aacute;lculo completo de R. Decid cu&aacute;l es el valor E12 que usar&eacute;is y por qu&eacute; el de
                arriba y no el de abajo.</li>
            <li><b>El esquema</b>, con simbolog&iacute;a normalizada: fuente, pulsador, resistencia y LED,
                rotulados con sus valores. Que se note d&oacute;nde est&aacute; el c&aacute;todo.</li>
            <li><b>Montadlo</b> y comprobad que enciende. Si no enciende, <b>antes de tocar nada</b>
                escribid las tres cosas que vais a comprobar y en qu&eacute; orden.</li>
            <li><b>Medid la corriente</b> con el pol&iacute;metro en serie y comparadla con la que
                hab&iacute;ais calculado. Anotad las dos y la diferencia en tanto por ciento.</li>
            <li><b>Cambiad el pulsador por el interruptor</b> y describid en dos l&iacute;neas la
                diferencia, sin usar la palabra &laquo;bot&oacute;n&raquo;.</li>
            <li><b>Si hay micro:bit</b>: en <a href="https://makecode.microbit.org" target="_blank"
                rel="noopener">MakeCode</a>, haced que el LED de P0 parpadee con
                <i>escritura digital</i> y una pausa. Y luego que se encienda solo mientras se
                aprieta el bot&oacute;n A.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>El c&aacute;lculo de R est&aacute; completo y <b>hecho antes</b> de montar <b>(3 puntos)</b>.</li>
            <li>La elecci&oacute;n del valor E12 est&aacute; justificada <b>(1 punto)</b>.</li>
            <li>El esquema usa los s&iacute;mbolos normalizados y respeta la polaridad <b>(2 puntos)</b>.</li>
            <li>El montaje enciende y la corriente medida se parece a la calculada <b>(2 puntos)</b>.</li>
            <li>La diferencia entre pulsador e interruptor est&aacute; bien explicada <b>(1 punto)</b>.</li>
            <li>El programa de MakeCode funciona, o el montaje est&aacute; simulado en Tinkercad
                <b>(1 punto)</b>.</li>
          </ul>
          <div class="nota" style="margin-top:14px">
            <span class="n-tag">Seguridad y material</span>
            El LED va <b>siempre</b> con su resistencia, aunque sea &laquo;un momento para probar&raquo;: ese
            momento es justo lo que tarda en morirse. Y nada de esto se enchufa <b>jam&aacute;s</b> a la
            red: 230 V no es una versi&oacute;n grande de 4,5 V, es otra cosa y mata.
          </div>
  ''')) +

  bloque('03', u'Cierre &middot; 5 min', u'''
      <p>Ya no hace falta preguntarle a nadie qu&eacute; resistencia le pone a su LED: se calcula, y sale
         un n&uacute;mero distinto para cada fuente y cada color.</p>
      <ol>
      ''' + pregunta(u'LED verde (V<sub>f</sub> = 2,2 V) en una pila de 9 V, y quieres que pasen 10 mA. &iquest;Qu&eacute; resistencia le pones?',
                     u'<p>Sobra 9 &minus; 2,2 = <b>6,8 V</b>. R = 6,8 / 0,010 = <b>680 &#8486;</b>, que adem&aacute;s existe tal cual en la serie E12. Con ella pasan exactamente los 10 mA.</p>')
        + pregunta(u'&iquest;Por qu&eacute; no se puede calcular la corriente de un LED con la ley de Ohm, si es un componente el&eacute;ctrico como los dem&aacute;s?',
                   u'<p>Porque <b>no es &oacute;hmico</b>: su corriente no es proporcional a la tensi&oacute;n. Por debajo de su tensi&oacute;n directa no conduce y por encima la corriente se dispara, as&iacute; que no hay una R que meter en la f&oacute;rmula. Lo que s&iacute; es &oacute;hmico es la resistencia que le pones al lado, y por eso es ella la que fija la corriente.</p>')
        + pregunta(u'Quieres que un zumbador suene <b>solo mientras</b> tienes el dedo puesto. &iquest;Pulsador o interruptor? &iquest;Y de qu&eacute; tipo?',
                   u'<p><b>Pulsador normalmente abierto (NA)</b>: cierra el circuito mientras lo aprietas y lo abre en cuanto lo sueltas, porque lleva un muelle que lo devuelve a su sitio. Con un interruptor sonar&iacute;a hasta que volvieras a accionarlo.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Con eso montas y calculas. La &uacute;ltima sesi&oacute;n es la que junta las cinco anteriores:
        <b>un montaje que resuelva un problema de verdad</b>, con su esquema, sus cuentas y su
        presupuesto. Ve pensando d&oacute;nde te hace falta una luz o un aviso que ahora no existe.
      </div>
  '''))


# ==========================================================================
# SESION 6 - Proyecto y autoevaluacion
# ==========================================================================
S6 = (
  bloque('00', u'Reto inicial &middot; 5 min', u'''
      <p>Cinco sesiones montando circuitos que te ponemos nosotros. Hoy el circuito lo eliges
         t&uacute;, y hay una condici&oacute;n: <b>tiene que servir para algo</b>.</p>

      <div class="aviso">
        <span class="n-tag">El reto</span>
        <p style="margin:0">Tres minutos, la libreta y nada m&aacute;s. Escribe <b>tres sitios</b> de tu
           casa, de tu mochila o de esta clase donde falte <b>una luz o un aviso</b> que ahora no
           existe. Sitios de verdad, con nombre: no &laquo;una habitaci&oacute;n&raquo;, sino &laquo;el fondo del
           armario, que no se ve nada cuando busco algo por la ma&ntilde;ana&raquo;.</p>
      </div>

      <p>Comparad la lista. Va a pasar casi seguro que la mayor&iacute;a haya escrito <b>el aparato</b> en
         vez del problema: &laquo;quiero hacer un timbre&raquo;, &laquo;una linterna&raquo;. Y eso, que parece lo mismo,
         te cierra la puerta antes de empezar.</p>
      <p>Porque &laquo;quiero hacer un timbre&raquo; ya ha decidido la soluci&oacute;n. &laquo;<b>Desde mi cuarto no oigo
         cuando llaman a la puerta</b>&raquo; deja abiertas todas: un zumbador, una luz que parpadee &mdash;que
         es mejor si alguien no oye bien&mdash;, o las dos cosas. Esto no es nuevo: es exactamente el
         <b>proceso tecnol&oacute;gico</b> del primer tema. Se empieza por la necesidad, no por el cacharro.</p>

      <div class="reto-piensa">
        <span class="n-tag">Piensa antes de seguir</span>
        <p>Coge el mejor de tus tres y reescr&iacute;belo en <b>una frase que no nombre ning&uacute;n
           componente</b>. Si no puedes, es que ten&iacute;as un cacharro y no un problema.</p>
      </div>
  ''') +

  bloque('01', u'El proyecto &middot; 35 min', u'''
      <h3>Qu&eacute; se entrega, y por qu&eacute; cada cosa</h3>
      <p>Un proyecto de Tecnolog&iacute;a no es el montaje: el montaje es solo la parte que se ve. Lo que
         se entrega es el montaje <b>m&aacute;s los papeles que permiten que otra persona lo repita</b>. Si
         tu circuito funciona y nadie puede reconstruirlo, no has terminado el trabajo.</p>

      <div class="copiar">
        <h4>El dossier del proyecto &middot; seis apartados</h4>
        <ol>
          <li><b>El problema</b>, en una frase y sin nombrar componentes. Qui&eacute;n lo tiene y cu&aacute;ndo.</li>
          <li><b>Las condiciones</b>: qu&eacute; tiene que hacer, con qu&eacute; alimentaci&oacute;n, cu&aacute;nto puede
              costar y de qu&eacute; tama&ntilde;o puede ser.</li>
          <li><b>El esquema el&eacute;ctrico</b> en simbolog&iacute;a normalizada, con los valores rotulados.</li>
          <li><b>Los c&aacute;lculos</b>: la resistencia limitadora, la corriente que circula y la
              potencia. Con sus operaciones, no solo el resultado.</li>
          <li><b>La lista de materiales</b> con cantidades y precios, y el total.</li>
          <li><b>La prueba</b>: qu&eacute; hiciste para comprobar que funciona, qu&eacute; fall&oacute; la primera vez
              y qu&eacute; cambiaste.</li>
        </ol>
      </div>

      <p>El punto 3 no es decoraci&oacute;n. Un esquema en s&iacute;mbolos normalizados es un <b>plano</b>: no
         dice d&oacute;nde est&aacute; cada pieza ni de qu&eacute; color es, dice <b>qu&eacute; est&aacute; conectado con qu&eacute;</b>,
         y lo entiende alguien que no hable tu idioma. Es la misma idea que el tema de
         <b>representaci&oacute;n gr&aacute;fica</b>: dibujar para que no haya dos interpretaciones posibles. Un
         dibujo bonito de tu montaje, con los cables tal como quedaron, sirve para una foto; para
         que otro lo construya, no.</p>

      <h3>Cuatro proyectos que caben en una sesi&oacute;n</h3>
      <p>Puedes proponer el tuyo, pero tiene que llevar <b>al menos un LED con su resistencia
         calculada y un elemento de control bien elegido</b>. Estos cuatro cumplen y caben en el
         tiempo que hay:</p>
      <ul>
        <li><b>Luz de armario.</b> Un LED blanco o rojo que se enciende <b>mientras</b> la puerta
            est&aacute; abierta. Control: pulsador <b>normalmente cerrado</b> apretado por la puerta.
            La gracia est&aacute; en darse cuenta de que aqu&iacute; el pulsador va al rev&eacute;s.</li>
        <li><b>Aviso de puerta.</b> Un zumbador o un LED que avisa en tu cuarto de que llaman.
            Control: pulsador NA. Si usas LED, tendr&aacute;s que discutir si se ve estando de espaldas.</li>
        <li><b>Luz de la bici o de la mochila.</b> LED rojo, interruptor (tiene que quedarse
            encendido) y pila. Calcula cu&aacute;ntas horas dura la pila con tu corriente.</li>
        <li><b>Sem&aacute;foro de dos luces.</b> Un LED verde y uno rojo, cada uno con <b>su</b>
            resistencia &mdash;que no es la misma, porque V<sub>f</sub> no es la misma&mdash; y un
            conmutador que pasa de uno a otro.</li>
      </ul>

      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; no hace falta copiarlo</span>
        <p>Hay una pregunta que aparece siempre en este punto: &laquo;&iquest;y si le pongo <b>dos</b> LED, les
           pongo una resistencia a los dos o una a cada uno?&raquo;. La respuesta corta es <b>una a cada
           uno</b>, y el motivo es bonito.</p>
        <p>Si pones dos LED <b>en paralelo</b> compartiendo una sola resistencia, los dos reciben la
           misma tensi&oacute;n, s&iacute;; pero como no son &oacute;hmicos, unas d&eacute;cimas de diferencia entre ellos
           &mdash;y las hay, aunque sean de la misma bolsa&mdash; hacen que uno se lleve <b>bastante
           m&aacute;s corriente</b> que el otro. Resultado: uno alumbra m&aacute;s, se calienta m&aacute;s, conduce
           todav&iacute;a mejor y se lleva a&uacute;n m&aacute;s corriente. Acaba muriendo el que m&aacute;s luc&iacute;a.</p>
        <p>En <b>serie</b> s&iacute; comparten resistencia sin problema, porque la corriente es
           forzosamente la misma para los dos. Lo que hay que comprobar entonces es que la fuente
           llegue: dos LED rojos en serie ya piden 4 V solo para ellos, y de un pin de 3 V no salen.</p>
      </div>

      <h3>Antes de entregar: comprueba si te lo sabes</h3>
      <p>Este test se corrige solo, aqu&iacute; mismo. Las preguntas de calcular <b>cambian de n&uacute;meros
         cada vez</b>, as&iacute; que no vale aprenderse las respuestas: solo vale saber hacerlas. Tira
         dos o tres tandas.</p>
''' + ESC_TEST + u'''
      <p>Si algo se te resiste, no repitas el test: vuelve a la sesi&oacute;n donde estaba. Las de
         calcular con V, I y R son la <b>sesi&oacute;n 2</b>; las de serie y paralelo, la <b>3</b>; las de
         potencia, kWh y dinero, la <b>4</b>; la del LED, la <b>5</b>.</p>
  ''') +

  bloque('02', u'Entrega &middot; 15 min', ficha(
    u'Actividad 6 &middot; Proyecto final de la unidad',
    [u'3.1', u'A.6'], u'Parejas &middot; se entrega al final', u'''
          <h4>Qu&eacute; hay que entregar</h4>
          <p>El <b>dossier de seis apartados</b> de la teor&iacute;a y el montaje funcionando, real o
             simulado en <a href="https://www.tinkercad.com/circuits" target="_blank"
             rel="noopener">Tinkercad Circuits</a>. Si el montaje no llega a funcionar, se entrega
             igual: el apartado 6 explica hasta d&oacute;nde llegasteis y qu&eacute; hab&iacute;ais descartado ya.</p>
          <ol class="pasos">
            <li>Problema y condiciones escritos <b>antes</b> de elegir componentes.</li>
            <li>Esquema en simbolog&iacute;a IEC, a regla o con un editor, con todos los valores
                rotulados.</li>
            <li>C&aacute;lculo de <b>cada</b> resistencia limitadora, con la corriente que hab&eacute;is
                elegido y por qu&eacute; esa.</li>
            <li>Lista de materiales con precios reales de una tienda de electr&oacute;nica, y el total.</li>
            <li>Montaje y prueba. Una foto o una captura.</li>
            <li>Una frase final: <b>qu&eacute; cambiar&iacute;ais</b> si tuvierais otra sesi&oacute;n.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>El problema est&aacute; planteado como necesidad y no como cacharro <b>(1 punto)</b>.</li>
            <li>El esquema es correcto, normalizado y se entiende sin explicaciones
                <b>(3 puntos)</b>.</li>
            <li>Los c&aacute;lculos est&aacute;n hechos, con sus operaciones y sus unidades <b>(3 puntos)</b>.</li>
            <li>El montaje funciona, o el fallo est&aacute; diagnosticado por escrito <b>(2 puntos)</b>.</li>
            <li>La lista de materiales est&aacute; completa y sumada <b>(1 punto)</b>.</li>
          </ul>
          <div class="nota" style="margin-top:14px">
            <span class="n-tag">El criterio que m&aacute;s cuenta</span>
            Un montaje que funciona por casualidad, sin c&aacute;lculos, vale <b>menos</b> que uno que no
            llega a encender pero trae el esquema bien, la cuenta bien y el fallo localizado por
            escrito. En Tecnolog&iacute;a se eval&uacute;a el m&eacute;todo, porque el m&eacute;todo es lo que sirve la
            pr&oacute;xima vez.
          </div>
  ''')) +

  bloque('03', u'Cierre del tema &middot; 5 min', u'''
      <p>Repasa de d&oacute;nde vienes. Empezaste con una pila, una bombilla y un cable que no encend&iacute;a
         nada, y acabas calculando cu&aacute;nta corriente puede dar un pin de una placa y cu&aacute;nto cuesta
         al a&ntilde;o dejar una luz puesta. Todo eso con <b>tres magnitudes y una regla</b>.</p>

      <div class="copiar">
        <h4>El tema entero, en seis l&iacute;neas</h4>
        <ul>
          <li>La corriente necesita un <b>camino cerrado</b>; sin receptor, es un cortocircuito.</li>
          <li><b>V</b> empuja, <b>I</b> circula, <b>R</b> estorba, y los ata la <b>ley de Ohm</b>.</li>
          <li>En <b>serie</b> se suman las resistencias; en <b>paralelo</b>, las corrientes.</li>
          <li><b>P = V &times; I</b> dice lo deprisa que gastas; <b>E = P &times; t</b>, lo que llevas
              gastado, y se paga en <b>kWh</b>.</li>
          <li>Un <b>LED</b> no es &oacute;hmico: su corriente la fija la resistencia que le pongas.</li>
          <li>El <b>pulsador</b> vuelve solo; el <b>interruptor</b> se queda.</li>
        </ul>
      </div>

      <ol>
      ''' + pregunta(u'Tu montaje enciende cuando lo tocas y se apaga solo al rato. Enumera, en orden, las tres cosas que comprobar&iacute;as.',
                     u'<p>Una respuesta razonable: <b>1)</b> las conexiones que se tocan sin estar sujetas (las pinzas de cocodrilo son la causa m&aacute;s frecuente); <b>2)</b> la pila, midiendo su tensi&oacute;n con el circuito <b>conectado</b>, que es cuando se ve si est&aacute; agotada; <b>3)</b> la polaridad y la temperatura del LED, por si est&aacute; trabajando pasado de corriente. Lo que se eval&uacute;a aqu&iacute; es que haya un <b>orden</b> y un motivo, no la lista exacta.</p>')
        + pregunta(u'&iquest;Por qu&eacute; un esquema normalizado vale m&aacute;s que una foto del montaje?',
                   u'<p>Porque la foto ense&ntilde;a c&oacute;mo qued&oacute;, y el esquema ense&ntilde;a <b>qu&eacute; est&aacute; conectado con qu&eacute;</b>, que es lo &uacute;nico que hace falta para reconstruirlo. Adem&aacute;s se lee igual en cualquier idioma, porque los s&iacute;mbolos est&aacute;n acordados (IEC 60617).</p>')
        + pregunta(u'Todo lo que has montado se enciende porque alguien aprieta algo. &iquest;Qu&eacute; har&iacute;a falta para que se encendiera <b>solo</b> cuando hace falta?',
                   u'<p>Hacen falta dos cosas que este tema no tiene: algo que <b>mida</b> el mundo (un sensor: de luz, de temperatura, de distancia) y algo que <b>decida</b> con esa medida. Lo segundo es una m&aacute;quina que procesa informaci&oacute;n, y eso es justo el tema siguiente.</p>') + u'''
      </ol>

      <div class="copiar" style="border-color:var(--goo-verde)">
        <h4>Lectura del tema</h4>
        <p>Si a&uacute;n no la hab&eacute;is hecho, la lectura va con este tema: <b>31 p&aacute;rrafos numerados</b>,
           uno cada uno en voz alta, y diez preguntas por escrito.</p>
        <p style="margin-top:10px"><a href="lectura-tema8.pdf" target="_blank" rel="noopener"
           style="font-family:var(--f-m);font-size:13px;color:var(--goo-verde);font-weight:500">
           &#8595; Un cable no hace nada &middot; PDF</a></p>
      </div>

      <div class="nota">
        <span class="n-tag">Siguiente tema</span>
        Tienes energ&iacute;a que llega por un cable y sabes gobernarla con el dedo. Lo que falta es
        que decida <b>sola</b>: que mida algo y act&uacute;e en consecuencia. Para eso hace falta una
        m&aacute;quina que procese informaci&oacute;n, y de eso va el <b>tema 7: el ordenador y sus
        componentes</b>.
      </div>
  '''))


# ==========================================================================
SESIONES = [
  dict(corto=u'El circuito', titulo=u'Un cable no hace nada',
       entradilla=u'Tienes pila, tienes cable y tienes bombilla, y aun as&iacute; no se enciende. Lo que '
                  u'falta no es una pieza: es una forma.',
       minutado=MIN, chips=CHIPS, cuerpo=SIMBOLOS + S1),
  dict(corto=u'V, I, R y Ohm', titulo=u'El empuj&oacute;n, el caudal y el estorbo',
       entradilla=u'Tres magnitudes que se miden con tres aparatos distintos, y una regla de cuatro '
                  u'caracteres que las ata a las tres.',
       minutado=MIN, chips=CHIPS, cuerpo=S2),
  dict(corto=u'Serie y paralelo', titulo=u'Una detr&aacute;s de otra, o cada una por su lado',
       entradilla=u'Hay exactamente dos maneras de conectar dos l&aacute;mparas a una pila. Elegir mal '
                  u'una vez cost&oacute; dinero de verdad en 1882.',
       minutado=MIN, chips=CHIPS, cuerpo=S3),
  dict(corto=u'Potencia y consumo', titulo=u'Lo que cuesta tenerlo encendido',
       entradilla=u'La misma electricidad de siempre, ahora medida en euros y en gramos de '
                  u'CO&#8322;. Hacen falta dos magnitudes m&aacute;s: una dice lo deprisa que gastas y '
                  u'otra lo que llevas gastado.',
       minutado=MIN, chips=CHIPS, cuerpo=S4),
  dict(corto=u'LED y pulsadores', titulo=u'El componente que no perdona',
       entradilla=u'Una l&aacute;mpara aguanta lo que le eches. Un LED se muere en el primer segundo '
                  u'si no has hecho la cuenta antes.',
       minutado=MIN, chips=CHIPS, cuerpo=S5),
  dict(corto=u'Proyecto y test', titulo=u'Que sirva para algo',
       entradilla=u'El &uacute;ltimo circuito lo eliges t&uacute;, y tiene que resolver un problema de '
                  u'verdad: con su esquema, sus cuentas y su presupuesto.',
       minutado=MIN6, chips=CHIPS, cuerpo=S6),
]

CFG = dict(
 ruta='2eso/TyD/tema8/',
 migas=u'<a href="../../../">Materiales</a> &middot; <a href="../../">2.&ordm; ESO</a> &middot; '
       u'<a href="../">TyD</a> &middot; Tema 6',
 h1=u'Electricidad y electr&oacute;nica',
 titulo=u'Tema 8 &middot; Electricidad y electr&oacute;nica',
 tema=u'Tema 8', curso=u'2.&ordm; de ESO', materia=u'Tecnolog&iacute;a y Digitalizaci&oacute;n',
 desc=u'Tema 8 de Tecnolog&iacute;a y Digitalizaci&oacute;n de 2.&ordm; de ESO: el circuito el&eacute;ctrico, '
      u'tensi&oacute;n, intensidad, resistencia, ley de Ohm, serie y paralelo y simbolog&iacute;a '
      u'normalizada, con escenas interactivas.',
 sesiones=SESIONES)


if __name__ == '__main__':
    html = pagina(CFG).replace(u'@@ALTA@@', ALTA)
    # El CSS del narrador no esta en el molde comun: se inyecta aqui, que es
    # donde se usa, en vez de tocar tema0_base y afectar a las demas unidades.
    html = html.replace(u'</style>', avatar_flat.CSS + u'</style>', 1)
    # El cargador diferido de los videos, una sola vez para los tres.
    html = html.replace(u'</body>', VIDEO_JS + u'</body>', 1)

    destino = os.path.join(RAIZ, '2eso', 'TyD', 'tema8', 'index.html')
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    io.open(destino, 'w', encoding='utf-8', newline='').write(html)
    print('U6 generada: %d bytes, %d sesiones (%d escritas)' % (
        len(html), len(SESIONES), sum(1 for s in SESIONES if not s.get('pendiente'))))
