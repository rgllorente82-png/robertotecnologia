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

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHIPS = [u'CE3 &middot; 3.1', u'A.6']
# Las dos fotos historicas son verticales y muy largas: a todo el ancho de la
# columna se comen dos pantallas enteras. Se les pone tope de alto y se centran.
# (Va por marcador y no con %% porque este texto pasa por formateo de Python.)
ALTA = u'width:auto;max-width:100%;max-height:520px;margin:0 auto'
MIN = [(u"10'", u'Reto'), (u"20'", u'Teor&iacute;a'), (u"25'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')]


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
        Ya sabes qu&eacute; forma tiene que tener el montaje. Pero una pila de petaca se puede agarrar
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
      <p>Ya sabes montar un anillo y ya sabes calcularlo. Ahora complicamos lo m&iacute;nimo posible:
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
        <p style="margin-top:10px"><a href="lectura-tema6.pdf" target="_blank" rel="noopener"
           style="font-family:var(--f-m);font-size:13px;color:var(--goo-verde);font-weight:500">
           &#8595; Un cable no hace nada &middot; PDF</a></p>
      </div>

      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya sabes calcular qu&eacute; corriente circula y c&oacute;mo repartirla. Falta la pregunta que acaba
        llegando a casa en un papel: <b>&iquest;cu&aacute;nto cuesta tener esto encendido?</b> Para eso hacen
        falta dos conceptos nuevos, la <b>potencia</b> y el <b>consumo</b>.
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
  dict(corto=u'Potencia y consumo', pendiente=True),
  dict(corto=u'LED y pulsadores', pendiente=True),
  dict(corto=u'Proyecto y test', pendiente=True),
]

CFG = dict(
 ruta='2eso/TyD/tema6/',
 migas=u'<a href="../../../">Materiales</a> &middot; <a href="../../">2.&ordm; ESO</a> &middot; '
       u'<a href="../">TyD</a> &middot; Tema 6',
 h1=u'Electricidad y electr&oacute;nica',
 titulo=u'Tema 6 &middot; Electricidad y electr&oacute;nica',
 tema=u'Tema 6', curso=u'2.&ordm; de ESO', materia=u'Tecnolog&iacute;a y Digitalizaci&oacute;n',
 desc=u'Tema 6 de Tecnolog&iacute;a y Digitalizaci&oacute;n de 2.&ordm; de ESO: el circuito el&eacute;ctrico, '
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

    destino = os.path.join(RAIZ, '2eso', 'TyD', 'tema6', 'index.html')
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    io.open(destino, 'w', encoding='utf-8', newline='').write(html)
    print('U6 generada: %d bytes, %d sesiones (%d escritas)' % (
        len(html), len(SESIONES), sum(1 for s in SESIONES if not s.get('pendiente'))))
