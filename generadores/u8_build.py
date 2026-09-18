# -*- coding: utf-8 -*-
"""2.o TyD · U8 (web) · Internet, datos y seguridad.

Las SEIS sesiones escritas. Las escenas interactivas viven en u8_escenas.py
(las cinco de las sesiones 1 a 3) y en u8_escenas2.py (las cuatro de las
sesiones 4 a 6). El test que cierra la unidad sale de test_auto.py, con las
diez preguntas en PREGUNTAS_U8, aqui abajo: son de TODO el tema, no solo de la
ultima sesion.

    python generadores/u8_build.py

Escribe 2eso/TyD/tema8/index.html relativo a la raiz del repo (el padre de
generadores/), no a una ruta absoluta: asi corre igual en el portatil y aqui.

Ojo con la numeracion: esto es el TEMA 8 de la web y la UNIDAD 10 del libro
(criterios 6.1, 6.2 y 6.3; saberes del bloque D). Ver CURRICULO.md e INFORME.md.
En el texto no aparece ningun numero de tema -se dice "la unidad del ordenador",
no "el tema 7"-, igual que en la U7: si algun dia se renumera, no hay que
reescribir nada.
"""
import io, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unidad_base import pagina, bloque, ficha, pregunta
from test_auto import test
import avatar_flat
from u8_escenas import (ESCENA_RUTA, ESCENA_DNS, ESCENA_ESPIA, ESCENA_CLAVE,
                        ESCENA_HUELLA)
from u8_escenas2 import (ESCENA_FUERZA, ESCENA_HASH, ESCENA_NUBE,
                         ESCENA_DERECHOS)

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# --------------------------------------------------------------------------
# Piezas repetidas: la foto acreditada y el video que no se carga solo.
# --------------------------------------------------------------------------
def foto(src, alt, pie, autor, licencia, commons):
    return u'''      <figure class="foto">
        <img src="../../../img/%s" alt="%s" loading="lazy">
        <figcaption>%s
          <span class="credito">%s &middot; %s &middot;
            <a href="%s" target="_blank" rel="noopener">Wikimedia Commons</a></span>
        </figcaption>
      </figure>
''' % (src, alt, pie, autor, licencia, commons)


def video(idv, vid, titulo, canal, nota):
    return u'''      <div class="video" id="%s" data-vid="%s">
        <button type="button" class="video-play" aria-label="Reproducir el v&iacute;deo: %s">
          <span class="video-tri" aria-hidden="true"></span>
          <span class="video-txt">
            <b>%s</b>
            <span>%s</span>
          </span>
        </button>
        <p class="video-nota">%s El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin
          cookies de seguimiento. Si la red del centro bloquea YouTube,
          <a href="https://www.youtube.com/watch?v=%s" target="_blank" rel="noopener">&aacute;brelo
          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material
          publicado bajo la licencia de esta p&aacute;gina.</p>
      </div>

      <script>
      (function(){
        var c = document.getElementById('%s');
        if(!c) return;
        var b = c.querySelector('.video-play');
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
      })();
      </script>
''' % (idv, vid, titulo, titulo, canal, nota, vid, idv)


ENV = json.load(io.open(os.path.join(RAIZ, '_env_u8-internet.json'), encoding='utf-8'))
NARRADOR = avatar_flat.componente(
    'narr-u8', u'De d&oacute;nde sale esta unidad',
    u'Una m&aacute;quina sola ya la tienes; ahora hay millones y est&aacute;n conectadas',
    '../../../audio/u8-internet.mp3', ENV,
    u'Voz sintetizada sobre gui&oacute;n propio. La boca sigue el volumen real de la voz: se mueve '
    u'cuando habla y se para en los silencios.')


# ==========================================================================
# SESION 1 · Como llega un video a tu movil
# ==========================================================================
S1 = (
  bloque('00', u'Reto inicial &middot; 10 min', u'''
      <p>De la unidad del ordenador te llevaste una m&aacute;quina que sabe hacer una sola cosa muy bien:
         buscar una instrucci&oacute;n, obedecerla y volver a empezar. Una m&aacute;quina sola, encima de una
         mesa, con sus ceros y sus unos guardados dentro.</p>
      <p>Coges el m&oacute;vil, le das a un v&iacute;deo y el v&iacute;deo aparece. Y <b>el v&iacute;deo no estaba
         dentro</b>.</p>

''' + NARRADOR + u'''
      <div class="aviso">
        <span class="n-tag">El encargo</span>
        Dibuja en el cuaderno c&oacute;mo llega ese v&iacute;deo desde donde est&eacute; guardado hasta tu pantalla.
        No vale &laquo;por el aire&raquo;: hay que decir <b>qu&eacute; viaja</b>, <b>por d&oacute;nde</b> y
        <b>c&oacute;mo sabe a d&oacute;nde ir</b>. Cinco minutos.
      </div>

      <p>Casi todo el mundo dibuja lo mismo, y es una idea razonable: <b>una l&iacute;nea reservada</b> desde
         el sitio donde est&aacute; el v&iacute;deo hasta tu m&oacute;vil, y el v&iacute;deo pasando por ella de una
         pieza. No es una tonter&iacute;a: el tel&eacute;fono funcion&oacute; exactamente as&iacute; durante
         <b>cien a&ntilde;os</b>, y hab&iacute;a alguien enchufando el cable a mano.</p>

''' + foto('u8-centralita.jpg',
           u'Fila de operadoras de tel&eacute;fono sentadas ante una centralita manual, conectando clavijas con cables',
           u'Una <b>centralita telef&oacute;nica</b> en 1955. Cuando alguien llamaba, una operadora enchufaba '
           u'f&iacute;sicamente un cable entre dos agujeros: durante toda la conversaci&oacute;n, ese camino '
           u'quedaba <b>reservado</b> para esas dos personas, lo usaran o no. Es exactamente el dibujo que '
           u'acabas de hacer, y por eso conviene ver d&oacute;nde se rompe.',
           u'Adolph B. Rice Studio &middot; The Library of Virginia',
           u'Sin restricciones conocidas de derechos',
           u'https://commons.wikimedia.org/wiki/File:City,_telephone_room_(2898490491).jpg') + u'''
      <p>Vamos a romperla con tres cuentas. H&aacute;zlas t&uacute;, no las leas:</p>

      <div class="reto-piensa">
        <span class="n-tag">Las tres cuentas</span>
        <p><b>1.</b> El v&iacute;deo ocupa <b>500 MB</b> y la l&iacute;nea mueve <b>50 megabits por segundo</b>.
           Como un byte son 8 bits, son 4.000 megabits: <b>80 segundos</b> con la l&iacute;nea entera para ti
           solo. &iquest;Cu&aacute;ntas personas pueden ver un v&iacute;deo a la vez por esa l&iacute;nea?</p>
        <p><b>2.</b> En un instituto de <b>600 personas</b>, para que cualquiera pueda hablar con
           cualquiera hacen falta cables <b>uno a uno</b>. Son 600 &times; 599 &divide; 2 =
           <b>179.700 cables</b>. Ahora repite la cuenta con los <b>5.500 millones</b> de personas que,
           aproximadamente, usan hoy Internet.</p>
        <p><b>3.</b> Si a mitad de env&iacute;o una excavadora corta el cable, &iquest;cu&aacute;nto del
           v&iacute;deo se ha salvado?</p>
      </div>

      <p>Las tres respuestas van en la misma direcci&oacute;n. Una sola persona por l&iacute;nea; un
         n&uacute;mero de cables que no cabe ni escrito; y si se corta, vuelta a empezar desde cero. La idea
         de <b>reservar un camino</b> no se puede arreglar: hay que tirarla.</p>

      <p>Y lo que la sustituye es casi lo contrario: <b>no reservar nada</b>. Partir lo que quieras mandar
         en trozos, <b>numerarlos</b>, ponerle a cada uno la direcci&oacute;n de destino y soltarlos a la red
         para que se busquen la vida. Suena a desastre. Funciona.</p>
  ''') +

  bloque('01', u'Teor&iacute;a &middot; 20 min', u'''
      <h3>Internet no manda el v&iacute;deo: manda trozos numerados</h3>
      <p>Prueba la red de abajo. Pide el v&iacute;deo y, <b>mientras los paquetes van de camino</b>, corta un
         cable pulsando encima. Fíjate en dos cosas: en qu&eacute; pasa con el paquete que iba justo por
         ah&iacute;, y en el orden en el que llegan los seis.</p>

''' + ESCENA_RUTA + u'''
      <div class="copiar">
        <h4>Paquetes</h4>
        <p><b>Paquete</b>: cada uno de los trozos en que se parte lo que se manda por Internet. Adem&aacute;s
           de su trozo de datos, lleva escrito <b>de d&oacute;nde viene</b>, <b>a d&oacute;nde va</b> y
           <b>qu&eacute; n&uacute;mero de trozo es</b>.</p>
        <p>Consecuencias, y son las tres que hay que entender:</p>
        <ul>
          <li>Los paquetes de una misma cosa <b>pueden ir por caminos distintos</b>.</li>
          <li>Pueden <b>llegar desordenados</b>, y da igual: el destino los coloca por su n&uacute;mero.</li>
          <li>Si <b>falta uno</b>, el destino lo nota (falta un n&uacute;mero) y lo <b>vuelve a pedir</b>.
              No hay que repetir el env&iacute;o entero.</li>
        </ul>
        <p>El mismo cable lo usan a la vez miles de conversaciones, porque nadie lo tiene reservado: los
           paquetes de unos y de otros van <b>entremezclados</b>.</p>
      </div>

      <h3>Para llegar hace falta una direcci&oacute;n</h3>
      <p>Un paquete sin direcci&oacute;n de destino es un sobre sin nada escrito. Por eso cada m&aacute;quina
         conectada a la red tiene un n&uacute;mero que la identifica.</p>

      <div class="copiar">
        <h4>Direcci&oacute;n IP</h4>
        <p><b>Direcci&oacute;n IP</b>: el n&uacute;mero que identifica a una m&aacute;quina dentro de la red. La
           cl&aacute;sica se escribe en cuatro trozos de 0 a 255, como <b>192.0.2.41</b>.</p>
        <p>Con ese formato hay <b>2<sup>32</sup> = 4.294.967.296</b> direcciones distintas: unos
           <b>4.300 millones</b>. Compara con los <b>8.000 millones</b> de personas que hay en el mundo, y
           ten en cuenta que muchas tienen m&oacute;vil, ordenador, consola y televisi&oacute;n. <b>No llegan.</b></p>
        <p>Por eso existe el formato nuevo, <b>IPv6</b>, con <b>2<sup>128</sup></b> direcciones: un 34
           seguido de 37 cifras m&aacute;s. No se van a acabar.</p>
      </div>

      <h3>Qui&eacute;n decide por d&oacute;nde va cada paquete</h3>
      <p>En la escena, los paquetes eleg&iacute;an camino solos. No es magia: en cada cruce hay una
         m&aacute;quina que mira la direcci&oacute;n de destino y decide por d&oacute;nde sale.</p>

      <div class="copiar">
        <h4>Router</h4>
        <p><b>Router</b> (encaminador): m&aacute;quina que recibe paquetes, mira la <b>direcci&oacute;n de
           destino</b> de cada uno y lo manda por el mejor camino que conoce <b>en ese momento</b>.</p>
        <p>Dos cosas que no son obvias:</p>
        <ul>
          <li>No elige el camino <b>m&aacute;s corto en kil&oacute;metros</b>, sino el que <b>tarda menos</b>,
              que depende de por d&oacute;nde va el cable y de cu&aacute;nta gente lo est&eacute; usando.</li>
          <li>Si un camino se cae, <b>recalcula</b>. Nadie tiene que arreglarlo a mano: por eso la red
              sigue funcionando aunque se rompan trozos.</li>
        </ul>
        <p>El router de tu casa hace esto mismo, en peque&ntilde;o, entre tus aparatos y la calle.</p>
      </div>

''' + foto('u8-imp-arpanet.jpg',
           u'Armario met&aacute;lico gris con la placa Interface Message Processor, el primer router de ARPANET',
           u'El <b>primer router de la historia</b>, de 1969: un armario de 400 kg llamado '
           u'<i>Interface Message Processor</i>. Hac&iacute;a exactamente lo que hace el de tu casa &mdash;mirar '
           u'a d&oacute;nde va cada paquete y mandarlo por ah&iacute;&mdash;, pero pesaba como una nevera llena '
           u'y costaba lo que una casa de entonces. Se fabricaron para conectar entre s&iacute; los cuatro '
           u'primeros centros de la red.',
           u'Steve Jurvetson', u'CC BY 2.0',
           u'https://commons.wikimedia.org/wiki/File:ARPANET_first_router.jpg') + u'''
      <h3>Y los nombres: la agenda</h3>
      <p>T&uacute; no escribes 192.0.2.41 en el navegador. Escribes un nombre. Pero la red <b>solo sabe ir a
         un n&uacute;mero</b>, as&iacute; que alguien tiene que traducir, y eso ocurre <b>antes</b> de que
         empiece a llegar nada.</p>

''' + ESCENA_DNS + u'''
      <div class="copiar">
        <h4>DNS y cach&eacute;</h4>
        <p><b>DNS</b> (sistema de nombres de dominio): la agenda de Internet. Traduce un
           <b>nombre</b> (aula.example.es) en una <b>direcci&oacute;n IP</b> (192.0.2.41).</p>
        <p>No hay una lista gigante en un sitio: est&aacute; <b>repartida</b>. Se pregunta a quien lleva los
           <b>.es</b>, ese dice qui&eacute;n lleva <b>example.es</b>, y ese da el n&uacute;mero.</p>
        <p><b>Cach&eacute;</b>: guardar un rato una respuesta que acabas de recibir, para no tener que
           volver a pedirla. Es lo que hace que la segunda visita a un sitio empiece antes.</p>
      </div>

      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; no hace falta copiarlo</span>
        <p>Trocear los mensajes se le ocurri&oacute; a dos personas por separado y casi a la vez:
           <b>Paul Baran</b> en Estados Unidos (1964) y <b>Donald Davies</b> en el Reino Unido (1965), que
           fue quien los llam&oacute; <i>packets</i>, paquetes. Baran buscaba una red que <b>siguiera
           funcionando con trozos rotos</b>, y esa es justo la propiedad que probaste cortando cables en
           la escena.</p>
        <p>La primera red que lo hizo de verdad, <b>ARPANET</b>, mand&oacute; su primer mensaje el
           <b>29 de octubre de 1969</b>, entre dos ordenadores de California: uno en la Universidad de
           Los &Aacute;ngeles y otro en un centro de investigaci&oacute;n a 600 km. Iban a escribir
           <i>LOGIN</i>. Se escribi&oacute; la L, se escribi&oacute; la O, y el sistema se cay&oacute;. El primer
           mensaje de Internet fue <b>&laquo;LO&raquo;</b>.</p>
        <p>Una distinci&oacute;n que casi nadie hace: <b>Internet no es la web</b>. Internet es la red que
           mueve paquetes, y es de 1969. La <b>web</b> es una cosa que funciona <i>encima</i> de ella
           &mdash;p&aacute;ginas enlazadas entre s&iacute;&mdash;, y la invent&oacute; <b>Tim Berners-Lee</b> en el
           CERN en 1989, veinte a&ntilde;os despu&eacute;s. El correo, los juegos en red o las videollamadas
           tampoco son la web: van por Internet, por su cuenta.</p>
      </div>

      <h3>Lo &uacute;nico que no se puede acelerar</h3>
      <p>Por los cables submarinos la se&ntilde;al va en pulsos de luz dentro de una fibra de vidrio, a unos
         <b>200.000 km/s</b>. De Madrid a Nueva York hay unos <b>5.800 km</b> en l&iacute;nea recta, as&iacute;
         que la luz tarda <b>29 milisegundos</b> en llegar &mdash;y otros 29 en volver la respuesta&mdash;.
         Eso <b>no lo puede mejorar nadie</b>: ni un cable mejor ni un router m&aacute;s caro. Es f&iacute;sica.</p>

''' + foto('u8-cable-submarino.png',
           u'Secci&oacute;n de un cable submarino de comunicaciones con sus capas rotuladas en espa&ntilde;ol',
           u'Un <b>cable submarino</b> por dentro. En el centro, del grosor de un pelo, van las '
           u'<b>fibras &oacute;pticas</b>: por ah&iacute; pasa todo. El resto &mdash;el tubo de cobre, los '
           u'tensores de acero, el polietileno&mdash; est&aacute; para que aguante la presi&oacute;n del fondo del '
           u'mar, el agua salada y el ancla de alg&uacute;n barco. M&aacute;s del 95 % del tr&aacute;fico entre '
           u'continentes va por cables como este, no por sat&eacute;lite.',
           u'Traducido por Paconi', u'Dominio p&uacute;blico',
           u'https://commons.wikimedia.org/wiki/File:Submarine_cable_cross-section-es_svg.png') +
  video('video-cables', 'u1xxZ8r2rRc',
        u'C&oacute;mo funciona internet: los cables submarinos que conectan al mundo',
        u'Un Mundo Inmenso &middot; en espa&ntilde;ol',
        u'Para ver por d&oacute;nde va f&iacute;sicamente eso que llamamos &laquo;la nube&raquo;: barcos, '
        u'cables y mapas.')) +

  bloque('02', u'Pr&aacute;ctica &middot; 25 min', ficha(
    u'Actividad 8.1 &middot; La cuenta de los cables y la cuenta de los paquetes',
    [u'6.1'], u'Parejas &middot; 25 min &middot; sobre 10', u'''
          <h4>Qu&eacute; hay que hacer</h4>
          <ol class="pasos">
            <li><b>Los cables que no caben.</b> Calculad cu&aacute;ntos cables uno a uno hacen falta para
                <b>5</b>, para <b>10</b> y para <b>600</b> personas (la f&oacute;rmula es
                <i>n &times; (n &minus; 1) &divide; 2</i>). Escribid despu&eacute;s una frase: si al pasar de
                10 a 600 personas los cables se multiplican por tanto, <b>&iquest;qu&eacute; pasar&iacute;a con
                5.500 millones?</b></li>
            <li><b>El troceo.</b> Un v&iacute;deo de <b>500 MB</b> (500.000.000 de bytes) se parte en paquetes.
                Cada paquete lleva <b>1.500 bytes</b> en total, de los cuales <b>40</b> son de
                &laquo;sobre&raquo; (de d&oacute;nde viene, a d&oacute;nde va, qu&eacute; n&uacute;mero es) y el
                resto, v&iacute;deo. Calculad:
                <ul>
                  <li>cu&aacute;ntos <b>bytes de v&iacute;deo</b> lleva cada paquete;</li>
                  <li>cu&aacute;ntos <b>paquetes</b> hacen falta;</li>
                  <li>cu&aacute;ntos <b>bytes</b> se van en sobres y qu&eacute; <b>porcentaje</b> del total son.</li>
                </ul></li>
            <li><b>El camino.</b> Con el mapa de la escena y estos costes &mdash;SERV-R1: 3 &middot;
                SERV-R2: 5 &middot; R1-R3: 5 &middot; R1-R4: 4 &middot; R2-R4: 4 &middot; R2-R5: 5 &middot;
                R3-R4: 3 &middot; R4-R5: 3 &middot; R3-R6: 6 &middot; R4-R6: 5 &middot; R4-R7: 7 &middot;
                R5-R7: 5 &middot; R6-M&Oacute;VIL: 3 &middot; R7-M&Oacute;VIL: 3&mdash;, encontrad
                <b>a mano</b> el camino m&aacute;s r&aacute;pido y su tiempo. Despu&eacute;s <b>cortad R4-R6</b> y
                volved a hacerlo. Comprobadlo luego en la escena.</li>
            <li><b>La traza.</b> Escribid, numerados y en orden, <b>todos los pasos</b> que ocurren desde
                que escribes un nombre en el navegador hasta que ves el primer trozo de v&iacute;deo. Tienen
                que aparecer: el nombre, el DNS, la direcci&oacute;n IP, los paquetes, los routers y la
                recomposici&oacute;n.</li>
            <li><b>El l&iacute;mite f&iacute;sico.</b> La luz va por la fibra a <b>200.000 km/s</b>. Calculad
                cu&aacute;nto tarda en recorrer <b>5.800 km</b> (Madrid&ndash;Nueva York) y cu&aacute;nto
                tarda la ida y la vuelta. Contestad: si pagas una conexi&oacute;n el doble de r&aacute;pida,
                &iquest;baja ese tiempo? &iquest;<b>Por qu&eacute;</b>?</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Las tres cuentas de cables est&aacute;n bien y la frase final entiende lo que significan
                <b>(2 puntos)</b>.</li>
            <li>El troceo est&aacute; completo, con el porcentaje y las unidades puestas <b>(2 puntos)</b>.</li>
            <li>Los dos caminos son correctos y coinciden con lo que hace la escena <b>(2 puntos)</b>.</li>
            <li>La traza tiene los seis elementos <b>en el orden correcto</b> <b>(2 puntos)</b>.</li>
            <li>El tiempo de la luz est&aacute; bien y la respuesta del &laquo;por qu&eacute;&raquo; distingue
                <b>velocidad</b> de <b>retardo</b> <b>(2 puntos)</b>.</li>
          </ul>
          <div class="nota" style="margin-top:14px">
            <span class="n-tag">Aviso sobre el paso 5</span>
            Contratar m&aacute;s megas es <b>ensanchar la tuber&iacute;a</b>, no acortarla. Cabe m&aacute;s agua
            por segundo, pero la primera gota sigue tardando lo mismo en llegar. Por eso en los juegos
            en red se habla del <i>ping</i> y no de los megas.
          </div>
  ''')) +

  bloque('03', u'Cierre &middot; 5 min', u'''
      <p>Vuelve al dibujo del principio. Aquella l&iacute;nea reservada ya no est&aacute;: lo que hay es un
         mont&oacute;n de trozos numerados compartiendo cables con los de todo el mundo.</p>
      <ol>
      ''' + pregunta(u'&iquest;Por qu&eacute; no se reserva un camino entero para cada conversaci&oacute;n, como hac&iacute;a el tel&eacute;fono antiguo?',
                     u'<p>Porque no cabe. Har&iacute;an falta tantos caminos como parejas posibles de usuarios, y cada uno quedar&iacute;a reservado aunque no se usara. Compartiendo los cables entre paquetes de todo el mundo, la misma red sirve para much&iacute;simas m&aacute;s conversaciones a la vez.</p>')
        + pregunta(u'Los paquetes de un v&iacute;deo llegan en el orden 1, 4, 2, 3. &iquest;Se ve mal el v&iacute;deo?',
                   u'<p>No. Cada paquete lleva escrito <b>su n&uacute;mero</b>, as&iacute; que el destino los coloca en su sitio antes de ense&ntilde;ar nada. Y si uno no llega, se nota enseguida &mdash;falta un n&uacute;mero&mdash; y se vuelve a pedir solo ese.</p>')
        + pregunta(u'Escribes un nombre en el navegador. &iquest;Qu&eacute; pasa antes de que empiece a llegar la p&aacute;gina?',
                   u'<p>Hay que traducir el nombre en un <b>n&uacute;mero</b>, porque la red solo sabe ir a n&uacute;meros. De eso se encarga el <b>DNS</b>. Si nadie ten&iacute;a guardada la respuesta, hay que preguntarla en varios sitios, y eso tarda unas d&eacute;cimas de segundo antes de que empiece lo dem&aacute;s.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        En la escena, tu paquete pas&oacute; por <b>cuatro m&aacute;quinas que no son tuyas</b>. En Internet de
        verdad suelen ser entre diez y veinte, y no son de nadie que conozcas. La pregunta incómoda es
        obvia: <b>&iquest;qui&eacute;n puede leer lo que va escrito dentro?</b>
      </div>

      <div class="copiar" style="border-color:var(--goo-verde)">
        <h4>Lectura del tema</h4>
        <p>Una sesi&oacute;n entera dedicada a leer y contestar. <b>30 p&aacute;rrafos numerados</b>: cada uno
           lee el suyo en voz alta, en orden. Despu&eacute;s, diez preguntas por escrito.</p>
        <p style="margin-top:10px"><a href="lectura-tema8.pdf" target="_blank" rel="noopener"
           style="font-family:var(--f-m);font-size:13px;color:var(--goo-verde);font-weight:500">
           &#8595; El viaje de un v&iacute;deo, y qui&eacute;n lo ve pasar &middot; PDF</a></p>
      </div>
  '''))


# ==========================================================================
# SESION 2 · Quien ve lo que mandas
# ==========================================================================
S2 = (
  bloque('00', u'Reto inicial &middot; 10 min', u'''
      <p>Lo dejamos en una pregunta: tus paquetes pasan por m&aacute;quinas de otros. El router del
         instituto, el de tu operador, unos cuantos por el camino, y a veces un cable que cruza el
         Atl&aacute;ntico. <b>Todos ellos tienen que leer la direcci&oacute;n de destino</b> para saber por
         d&oacute;nde mandarlo; la pregunta es qu&eacute; m&aacute;s pueden leer.</p>

      <div class="aviso">
        <span class="n-tag">El encargo</span>
        Tienes que pasarle una nota con un n&uacute;mero secreto a alguien del fondo de la clase, y la nota
        va a pasar por <b>ocho manos</b>. Inv&eacute;ntate un sistema para que solo lo entienda quien
        t&uacute; quieres. Escr&iacute;belo en el cuaderno antes de seguir.
      </div>

      <p>La idea que sale siempre es un <b>c&oacute;digo</b>: cambiar cada letra por otra. La versi&oacute;n
         m&aacute;s sencilla es correr el abecedario unas cuantas posiciones, y tiene 2.000 a&ntilde;os: la
         usaba Julio C&eacute;sar. Aqu&iacute; va un mensaje cifrado as&iacute;. <b>Descifradlo</b>, sin ayuda,
         y cronometrad cu&aacute;nto os cuesta:</p>

      <div class="reto-piensa">
        <span class="n-tag">A ver qu&eacute; pone</span>
        <p style="font-family:var(--f-m);font-size:17px;letter-spacing:.06em">HO HADPHQ HV HO YLHUQHV</p>
        <p style="margin-top:8px">Pista, si hace falta: prueba a correr cada letra <b>una</b> posici&oacute;n
           hacia atr&aacute;s. Si no sale, prueba <b>dos</b>. Si no, tres&hellip;</p>
      </div>

      <p>Sale en un par de minutos, y esa es justo la mala noticia. Hagamos la cuenta que lo explica:
         el abecedario que se usa para esto tiene <b>26 letras</b>, as&iacute; que hay <b>26 maneras</b> de
         correrlo, y una de ellas es dejarlo igual. <b>Veinticinco pruebas.</b> Un secreto que se acaba
         probando entero no es un secreto: es un rato de espera.</p>

      <p>Y hay un problema todav&iacute;a peor, que no es de matem&aacute;ticas. Imagina que el secreto es
         <b>el m&eacute;todo</b> &mdash;&laquo;corremos el abecedario&raquo;&mdash;. El d&iacute;a que uno solo
         de los que lo usan se va de la lengua, <b>hay que cambi&aacute;rselo a todo el mundo a la vez</b>.
         Y si el sistema lo usan mil millones de personas, eso no se puede hacer.</p>

      <div class="reto-piensa">
        <span class="n-tag">La pregunta que ordena el resto de la sesi&oacute;n</span>
        <p>Si el m&eacute;todo no puede ser secreto, porque es imposible mantenerlo escondido,
           <b>&iquest;qu&eacute; parte tiene que serlo?</b></p>
      </div>
  ''') +

  bloque('01', u'Teor&iacute;a &middot; 20 min', u'''
      <h3>Lo p&uacute;blico y lo secreto</h3>
      <p>La respuesta la escribi&oacute; un profesor holand&eacute;s de idiomas, <b>Auguste Kerckhoffs</b>, en un
         art&iacute;culo sobre criptograf&iacute;a militar de <b>1883</b>, y
         desde entonces no ha cambiado: el <b>m&eacute;todo</b> tiene que poder ser p&uacute;blico, y lo
         &uacute;nico secreto tiene que ser la <b>clave</b>. As&iacute;, si se te escapa la clave, cambias la
         clave y ya est&aacute;; no hay que reinventar nada.</p>

      <div class="copiar">
        <h4>Cifrar</h4>
        <p><b>Cifrar</b>: transformar un mensaje con una <b>clave</b>, de manera que sin esa clave no se
           pueda volver a leer. <b>Descifrar</b> es deshacerlo.</p>
        <p>La regla que aguanta desde 1883: <b>el m&eacute;todo es p&uacute;blico, la clave es secreta</b>.
           Los sistemas que se usan hoy est&aacute;n publicados enteros, para que cualquiera intente
           romperlos: el que sobrevive a eso es el que se usa.</p>
        <p>Lo que hace fuerte a una clave es <b>cu&aacute;ntas hay</b>. Con el c&oacute;digo de C&eacute;sar hay
           25 claves &uacute;tiles. Con las de hoy hay <b>2<sup>128</sup></b>, un 3 seguido de 38 cifras.</p>
      </div>

      <h3>Qu&eacute; ve exactamente el que est&aacute; en medio</h3>
      <p>Aqu&iacute; entra el <b>candado</b>. En la escena de abajo escribe un usuario y una contrase&ntilde;a
         &mdash;inventados, no los tuyos&mdash; y ve pulsando cada salto del camino con
         <b>http</b> y con <b>https</b>. Mira sobre todo los dos extremos.</p>

''' + ESCENA_ESPIA + u'''
      <div class="copiar">
        <h4>http y https</h4>
        <p><b>http</b>: la manera de pedir p&aacute;ginas <b>sin cifrar</b>. Lo que mandas viaja tal cual, y
           cualquiera de los saltos del camino puede leerlo y cambiarlo.</p>
        <p><b>https</b>: lo mismo, pero <b>cifrado de extremo a extremo del camino</b>. Es lo que significa
           el candado del navegador.</p>
        <p>El candado dice tres cosas, y solo tres:</p>
        <ol>
          <li>Nadie del camino puede <b>leer</b> lo que mandas.</li>
          <li>Nadie del camino puede <b>cambiarlo</b> sin que se note.</li>
          <li>Est&aacute;s hablando con el <b>due&ntilde;o de ese dominio</b>, y no con otro que se hace pasar
              por &eacute;l.</li>
        </ol>
      </div>

      <div class="copiar" style="border-color:var(--goo-rojo)">
        <h4>Lo que el candado NO dice</h4>
        <ul>
          <li>No dice que la web sea <b>honrada</b>. Una tienda falsa puede tener candado: el candado
              certifica <b>qui&eacute;n</b> es, no si es de fiar.</li>
          <li>No esconde <b>a qu&eacute; sitio</b> te conectas. El de en medio suele ver el nombre del
              dominio, cu&aacute;ndo entras y cu&aacute;nto ocupa lo que te bajas; lo que no ve es el contenido.</li>
          <li>No protege los <b>extremos</b>. En tu m&oacute;vil y en el servidor, el texto est&aacute; claro:
              tiene que estarlo, o no se podr&iacute;a usar.</li>
        </ul>
      </div>

      <h3>El problema gordo: ponerse de acuerdo en la clave</h3>
      <p>Si el candado cifra con una clave, <b>t&uacute; y la web ten&eacute;is que tener la misma</b>. Pero no
         os hab&eacute;is visto nunca, no hay manera de qued&aacute;is antes, y todo lo que os dig&aacute;is va a
         pasar por esas diez m&aacute;quinas de otros. Parece imposible: cualquier cosa que mandes para
         acordar la clave la oye el de en medio.</p>
      <p>Pues se puede. Mira los n&uacute;meros de abajo y cambia los secretos con los botones.</p>

''' + ESCENA_CLAVE + u'''
      <div class="copiar">
        <h4>Acordar una clave a la vista de todos</h4>
        <p>Cada uno elige un <b>n&uacute;mero secreto</b> que no ense&ntilde;a a nadie, hace una cuenta con
           &eacute;l y manda <b>el resultado</b>. Con el resultado del otro y su propio secreto, los dos
           llegan al <b>mismo n&uacute;mero final</b>, que ser&aacute; la clave.</p>
        <p>Quien lo ha visto todo tiene los n&uacute;meros p&uacute;blicos, pero <b>no los secretos</b>, y
           deshacer esa cuenta hacia atr&aacute;s es lo que no sabe hacer nadie en un tiempo razonable.</p>
        <p>Esto lo hace tu navegador, solo y en menos de un segundo, <b>con cada web</b> antes de empezar.
           Y una clave distinta cada vez.</p>
      </div>

      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; no hace falta copiarlo</span>
        <p>El ejemplo m&aacute;s caro de la historia de guardar el m&eacute;todo en vez de la clave es la
           m&aacute;quina de la foto. La <b>Enigma</b> cifraba con unos rotores que se colocaban cada
           d&iacute;a en una posici&oacute;n distinta: la posici&oacute;n era la clave, y la m&aacute;quina, el
           m&eacute;todo. El ej&eacute;rcito alem&aacute;n cre&iacute;a que el m&eacute;todo era secreto; no lo era,
           porque se capturaron m&aacute;quinas, y a partir de ah&iacute; el trabajo de matem&aacute;ticos
           polacos y despu&eacute;s brit&aacute;nicos consigui&oacute; leer mensajes durante a&ntilde;os.</p>
        <p>Lo que se aprendi&oacute; no fue &laquo;hay que esconder mejor la m&aacute;quina&raquo;. Fue justo lo
           contrario, y es lo que hacemos ahora: <b>publicar el m&eacute;todo entero</b>, que lo ataque todo
           el mundo durante a&ntilde;os, y si sobrevive, usarlo. Un sistema que solo aguanta mientras nadie
           sabe c&oacute;mo funciona no aguanta nada.</p>
      </div>

''' + foto('u8-enigma.jpg',
           u'M&aacute;quina de cifrado Enigma con su teclado y su caja de madera abierta',
           u'Una <b>Enigma</b>, del Museo de la Comunicaci&oacute;n de Berl&iacute;n. Se escrib&iacute;a en el '
           u'teclado y se encend&iacute;a la letra cifrada. El m&eacute;todo era la m&aacute;quina; la clave, '
           u'c&oacute;mo se colocaban los rotores ese d&iacute;a. Cuando el m&eacute;todo dej&oacute; de ser '
           u'secreto, el sistema entero se vino abajo.',
           u'Museum f&uuml;r Kommunikation Berlin', u'CC BY 4.0',
           u'https://commons.wikimedia.org/wiki/File:Enigma_I_cipher_machine_Museum_of_Communication_Berlin_cropped.jpg') + u'''
      <h3>La wifi abierta: por qu&eacute; era un problema y por qu&eacute; lo sigue siendo a medias</h3>
      <p>En una wifi abierta, cualquiera que est&eacute; cerca puede recoger lo que pasa por el aire. Hace
         quince a&ntilde;os eso era gordo: casi toda la web iba en <b>http</b>, o sea, en texto claro.
         Conectarse a la wifi de una cafeter&iacute;a y entrar en tu correo era mandar la contrase&ntilde;a
         escrita delante de quien quisiera mirar.</p>
      <p>Hoy casi todo va en <b>https</b>, y ese problema concreto est&aacute; resuelto. Lo que queda:</p>
      <div class="copiar">
        <h4>Qu&eacute; pasa hoy en una wifi abierta</h4>
        <ul>
          <li><b>Ya no se lee</b> lo que mandas a sitios con candado.</li>
          <li><b>S&iacute; se ve a d&oacute;nde vas</b>: qu&eacute; sitios visitas, cu&aacute;ndo y cu&aacute;nto
              tiempo. Eso tambi&eacute;n dice mucho de una persona.</li>
          <li>Quien monta la red puede <b>ense&ntilde;arte una p&aacute;gina suya</b> pidi&eacute;ndote que
              instales algo o que aceptes un aviso raro. Ah&iacute; ya no te protege el cifrado: te protege
              que no aceptes.</li>
        </ul>
        <p>Regla pr&aacute;ctica: en una red que no conoces, <b>mirar cosas s&iacute;</b>; <b>instalar</b> nada y
           <b>saltarse</b> un aviso de seguridad, nunca.</p>
      </div>

''' + video('video-https', 'U0iiT41OI3I',
            u'Qu&eacute; significa que una web empiece por HTTPS',
            u'Oficina de Seguridad del Internauta (INCIBE) &middot; en espa&ntilde;ol',
            u'La versi&oacute;n oficial y corta de lo mismo, del organismo p&uacute;blico espa&ntilde;ol de '
            u'ciberseguridad.')) +

  bloque('02', u'Pr&aacute;ctica &middot; 25 min', ficha(
    u'Actividad 8.2 &middot; Qu&eacute; protege el candado y qu&eacute; no',
    [u'6.2'], u'Parejas &middot; 25 min &middot; sobre 10', u'''
          <h4>Qu&eacute; hay que hacer</h4>
          <ol class="pasos">
            <li><b>Cifrar y descifrar.</b> Escribid una frase corta y cifradla corriendo el abecedario
                <b>cinco</b> posiciones. Intercambiadla con otra pareja <b>sin decirles el n&uacute;mero</b>
                y cronometrad cu&aacute;nto tardan en leerla. Anotad el tiempo: es la medida de lo que vale
                ese sistema.</li>
            <li><b>Cu&aacute;ntas claves hay.</b> Rellenad la tabla suponiendo una m&aacute;quina que prueba
                <b>mil millones de claves por segundo</b>:
                <ul>
                  <li>C&eacute;sar: 25 claves. &iquest;Cu&aacute;nto tarda?</li>
                  <li>Una clave antigua de 56 bits: 2<sup>56</sup> = 72.000.000.000.000.000 (setenta y dos
                      mil billones). &iquest;Cu&aacute;ntos <b>a&ntilde;os</b>?</li>
                  <li>Una de hoy, de 128 bits: 2<sup>128</sup>, que es <b>2<sup>72</sup></b> veces la
                      anterior, o sea un 47 seguido de 20 ceros de veces m&aacute;s. Con decir el orden de
                      magnitud basta: no hace falta el n&uacute;mero exacto.</li>
                </ul>
                Y una frase: <b>&iquest;por qu&eacute; a&ntilde;adir un bit a la clave no la mejora un poco,
                sino que la mejora el doble?</b></li>
            <li><b>A mirar de verdad.</b> Abrid tres p&aacute;ginas que us&eacute;is (la del instituto, una de
                noticias y una tienda). De cada una anotad: &iquest;empieza por <b>https</b>? Pulsando el
                candado, <b>&iquest;a nombre de qui&eacute;n</b> est&aacute; el certificado y <b>qui&eacute;n</b>
                lo ha emitido?</li>
            <li><b>El caso de la wifi del centro comercial.</b> Est&aacute;s conectado a una wifi abierta.
                Decid, y <b>justificad con lo de hoy</b>, qu&eacute; puede saber quien controle esa red en
                cada caso:
                <ul>
                  <li>miras un v&iacute;deo en una web con candado;</li>
                  <li>entras en una tienda con candado y compras algo;</li>
                  <li>visitas seis p&aacute;ginas distintas en media hora.</li>
                </ul></li>
            <li><b>La trampa.</b> Te llega un mensaje con un enlace a
                <i>notas-instituto.ejemplo-alumnos.com</i>. La p&aacute;gina <b>tiene candado</b>, es
                clavada a la del centro y te pide tu usuario y tu contrase&ntilde;a. Contestad:
                &iquest;el candado garantiza que sea la buena? <b>&iquest;Qu&eacute; hay que mirar</b>, y
                qu&eacute; har&iacute;ais?</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>El cifrado y el descifrado est&aacute;n bien hechos, con el tiempo anotado <b>(2 puntos)</b>.</li>
            <li>Los c&aacute;lculos de la tabla est&aacute;n bien y la frase del bit se entiende <b>(2 puntos)</b>.</li>
            <li>Las tres p&aacute;ginas est&aacute;n comprobadas de verdad, con lo que dice cada certificado
                <b>(2 puntos)</b>.</li>
            <li>Los tres casos de la wifi distinguen <b>contenido</b> de <b>destino</b> <b>(2 puntos)</b>.</li>
            <li>La respuesta de la trampa dice que hay que mirar el <b>dominio</b> y no el candado
                <b>(2 puntos)</b>.</li>
          </ul>
          <div class="nota" style="margin-top:14px">
            <span class="n-tag">Aviso</span>
            En el paso 5 no hay que entrar en ning&uacute;n sitio ni probar nada: se contesta por escrito.
            Y si alguna vez os llega de verdad un mensaje as&iacute;, lo que se hace es no pulsar y entrar
            <b>escribiendo vosotros la direcci&oacute;n de siempre</b>.
          </div>
  ''')) +

  bloque('03', u'Cierre &middot; 5 min', u'''
      <ol>
      ''' + pregunta(u'&iquest;Por qu&eacute; el m&eacute;todo de cifrado se publica, en vez de guardarlo en secreto?',
                     u'<p>Porque un secreto que tiene que saber mucha gente no se aguanta, y el d&iacute;a que se escapa hay que cambi&aacute;rselo a todo el mundo a la vez. Publicando el m&eacute;todo, lo &uacute;nico secreto es la <b>clave</b>: si se escapa una clave, se cambia esa y ya. Adem&aacute;s, un m&eacute;todo publicado lo puede intentar romper todo el mundo, y el que sobrevive es de fiar.</p>')
        + pregunta(u'Est&aacute;s en una wifi abierta y entras en una web con candado. &iquest;Qu&eacute; puede saber quien controle esa wifi?',
                   u'<p>Puede saber <b>a qu&eacute; sitio</b> te has conectado, cu&aacute;ndo y cu&aacute;nto ocupa lo que has movido. No puede saber <b>qu&eacute; le has dicho</b> ni qu&eacute; te ha contestado. El candado protege el contenido, no el destino.</p>')
        + pregunta(u'Una p&aacute;gina que te pide la contrase&ntilde;a tiene candado. &iquest;Es de fiar?',
                   u'<p>No necesariamente. El candado solo certifica que est&aacute;s hablando <b>con el due&ntilde;o de ese dominio</b>, sin que nadie escuche por el camino. Si el dominio es falso, el candado tambi&eacute;n protege perfectamente&hellip; la conversaci&oacute;n con el falso. Lo que hay que mirar es el <b>nombre del dominio</b>.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Resumen de hoy: por el camino, nadie lee lo que mandas. Entonces queda una pregunta rara.
        Si nadie lo lee&hellip; <b>&iquest;de d&oacute;nde sale todo lo que las empresas saben de ti?</b>
        Porque saben, y bastante.
      </div>
  '''))


# ==========================================================================
# SESION 3 · Tus datos valen dinero
# ==========================================================================
S3 = (
  bloque('00', u'Reto inicial &middot; 10 min', u'''
      <p>Piensa en la aplicaci&oacute;n que m&aacute;s usas. Ahora contesta a tres preguntas, en este orden:</p>
      <ol>
        <li>&iquest;Cu&aacute;nto has pagado por ella? <b>Nada.</b></li>
        <li>&iquest;Cu&aacute;nta gente trabaja en la empresa que la hace? <b>Decenas de miles de personas.</b></li>
        <li>&iquest;De d&oacute;nde sale ese dinero?</li>
      </ol>

      <div class="aviso">
        <span class="n-tag">El encargo</span>
        &laquo;De la publicidad&raquo; vale como respuesta, pero es la mitad. La otra mitad es la
        pregunta de verdad: <b>&iquest;por qu&eacute; vale tanto un anuncio ah&iacute;</b>, si un cartel en la
        calle lo ve much&iacute;sima m&aacute;s gente y cuesta mucho menos? Cont&eacute;stalo por escrito.
      </div>

      <p>Antes de comparar respuestas, una cuenta con n&uacute;meros p&uacute;blicos. Los de la empresa que
         tiene Instagram y WhatsApp, publicados por ella misma en enero de 2026:</p>

      <div class="reto-piensa">
        <span class="n-tag">Haz la divisi&oacute;n</span>
        <p>Ingres&oacute; <b>200.966 millones de d&oacute;lares</b> en 2025, casi todos de publicidad.
           Usan sus aplicaciones <b>3.580 millones de personas</b> al d&iacute;a.</p>
        <p style="margin-top:8px"><b>&iquest;Cu&aacute;nto dinero le dej&oacute; de media cada persona en un
           a&ntilde;o?</b> &iquest;Y al mes?</p>
      </div>

      <p>Salen unos <b>56 d&oacute;lares al a&ntilde;o</b>, menos de <b>5 al mes</b>. Ah&iacute; est&aacute; lo
         interesante: por ti, suelto, pagan poco m&aacute;s que un bocadillo. Lo que vale una fortuna es
         <b>la suma</b> &mdash;3.580 millones de personas&mdash; y, sobre todo, <b>saber a qui&eacute;n se le
         ense&ntilde;a cada anuncio</b>. Un cartel en la calle lo ve todo el mundo; un anuncio ah&iacute; lo ve
         exactamente quien interesa.</p>

      <div class="reto-piensa">
        <span class="n-tag">Y entonces</span>
        <p>Para eso hay que saber cosas de cada uno. Pero en la sesi&oacute;n anterior vimos que
           <b>nadie puede leer</b> lo que mandas por el camino. &iquest;De d&oacute;nde sale entonces lo que
           saben?</p>
      </div>

      <p>De dos sitios, y ninguno es el de las pel&iacute;culas. El primero: <b>se lo damos nosotros</b> al
         usar el servicio &mdash;lo que miras, cu&aacute;nto rato, a qui&eacute;n sigues, d&oacute;nde est&aacute;s,
         qu&eacute; escribes y qu&eacute; borras sin enviar&mdash;. El segundo: <b>el aparato se identifica
         solo</b>, sin que nadie le pregunte. Vamos a ver el segundo, que es el que casi nadie conoce.</p>
  ''') +

  bloque('01', u'Teor&iacute;a &middot; 20 min', u'''
      <h3>Tu navegador habla m&aacute;s de la cuenta</h3>
      <p>Para ense&ntilde;arte una p&aacute;gina bien, tu navegador tiene que contar cosas: qu&eacute; tama&ntilde;o
         tiene la pantalla, en qu&eacute; idioma la quieres, qu&eacute; sistema llevas. Cada dato por separado
         no dice nada. <b>Juntos, s&iacute;.</b></p>
      <p>La escena de abajo no es un ejemplo inventado: son <b>tus datos, le&iacute;dos ahora mismo</b> en el
         aparato desde el que est&aacute;s mirando esto.</p>

''' + ESCENA_HUELLA + u'''
      <div class="copiar">
        <h4>Huella digital</h4>
        <p><b>Huella digital</b> (o <i>fingerprinting</i>): reconocer un aparato por la <b>combinaci&oacute;n</b>
           de datos que da su navegador, sin guardarle nada dentro.</p>
        <p>Funciona por la misma raz&oacute;n que reconoces a alguien de espaldas: ning&uacute;n rasgo suelto
           es raro, pero la combinaci&oacute;n de todos casi no se repite.</p>
        <p>Lo importante: <b>no se borra</b>. Puedes borrar las cookies, cambiar de modo inc&oacute;gnito o
           reiniciar el m&oacute;vil, y la huella sigue siendo la misma, porque no es algo que te hayan
           puesto: <b>es c&oacute;mo es tu aparato</b>.</p>
      </div>

      <div class="copiar">
        <h4>Cookies y permisos</h4>
        <p><b>Cookie</b>: un dato peque&ntilde;o que una web guarda <b>dentro de tu navegador</b> y que le
           vuelve a llegar cada vez que entras. Sirve para reconocerte.</p>
        <ul>
          <li><b>Cookies propias</b>: las pone la web en la que est&aacute;s. Muchas hacen falta de verdad
              &mdash;mantener la sesi&oacute;n abierta, acordarse del idioma, el carrito de la compra&mdash;.</li>
          <li><b>Cookies de terceros</b>: las pone <i>otra</i> empresa a trav&eacute;s de esa web, y como
              est&aacute; en muchas webs a la vez, puede ir juntando <b>por d&oacute;nde pasas</b>.</li>
        </ul>
        <p><b>Permiso</b>: lo que una aplicaci&oacute;n te pide para llegar a algo del m&oacute;vil
           &mdash;c&aacute;mara, micr&oacute;fono, ubicaci&oacute;n, contactos, fotos&mdash;. Se concede una vez
           y sigue concedido hasta que lo quitas.</p>
      </div>

      <h3>Qu&eacute; se saca de un permiso, en n&uacute;meros</h3>
      <p>&laquo;Ubicaci&oacute;n&raquo; suena a que alguien sabe d&oacute;nde est&aacute;s ahora. Es bastante
         m&aacute;s que eso, y se ve haciendo la cuenta.</p>

      <div class="copiar">
        <h4>La cuenta de la ubicaci&oacute;n</h4>
        <p>Una aplicaci&oacute;n con permiso de ubicaci&oacute;n en segundo plano puede apuntar d&oacute;nde
           est&aacute;s cada <b>5 minutos</b>:</p>
        <ul>
          <li>60 &divide; 5 = <b>12 puntos por hora</b></li>
          <li>12 &times; 24 = <b>288 puntos al d&iacute;a</b></li>
          <li>288 &times; 30 = <b>8.640 puntos al mes</b></li>
        </ul>
        <p>Con los puntos <b>de 0:00 a 6:00</b> sale d&oacute;nde duermes. Con los de <b>8:00 a 15:00</b>,
           a qu&eacute; centro vas. Con los del fin de semana, a qu&eacute; te dedicas y con qui&eacute;n. Nadie
           ha le&iacute;do nada tuyo: solo ha sumado puntos en un mapa.</p>
      </div>

      <h3>El trueque, que no es nuevo</h3>
      <p>Esto no lo invent&oacute; Internet. Lo invent&oacute; el comercio, y el contrato siempre ha sido el
         mismo: <b>te doy algo a cambio de saber de ti</b>.</p>

''' + foto('u8-tarjeta-fidelizacion.jpg',
           u'Tarjeta de fidelizaci&oacute;n de pl&aacute;stico de un supermercado sobre una tela clara',
           u'Una <b>tarjeta de fidelizaci&oacute;n</b> de supermercado, de las que hay en todos los pa&iacute;ses. '
           u'El trato es transparente: te hacen descuento y, a cambio, la tienda sabe <b>qu&eacute; compras, '
           u'cu&aacute;ndo y cada cu&aacute;nto</b>. Lo que ha cambiado con Internet no es el trato: es el '
           u'<b>coste</b>. Antes hab&iacute;a que fabricar tarjetas y pasarlas por un lector; ahora se hace '
           u'solo, con todo el mundo y a la vez.',
           u'Donald Trung Quoc Don', u'CC BY-SA 4.0',
           u'https://commons.wikimedia.org/wiki/File:Supercoop_card,_Winschoten_(2020)_01.jpg') + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; no hace falta copiarlo</span>
        <p>Cuando recoger datos pas&oacute; a costar casi nada, hizo falta una ley, y la hay. El
           <b>Reglamento General de Protecci&oacute;n de Datos</b> es europeo, se aprob&oacute; en <b>2016</b> y
           se aplica desde el <b>25 de mayo de 2018</b> en los veintisiete pa&iacute;ses. Dice cosas muy
           concretas:</p>
        <ul>
          <li>Tienen que <b>pedirte permiso</b>, y no vale esconderlo en cuarenta p&aacute;ginas.</li>
          <li>Tienen que decirte <b>para qu&eacute;</b>, y no pueden usarlo para otra cosa.</li>
          <li>Puedes pedir <b>ver</b> lo que tienen tuyo, <b>corregirlo</b> y que lo <b>borren</b>.</li>
          <li>Si hay una fuga, tienen que <b>avis&aacute;rtelo</b>.</li>
        </ul>
        <p>De ah&iacute; salen los avisos de cookies que te encuentras en todas partes. Est&aacute;n mal
           hechos a prop&oacute;sito muchas veces &mdash;el bot&oacute;n de aceptar gordo y el de rechazar
           escondido&mdash;, y eso tambi&eacute;n lo prohíbe la ley; multar a todo el mundo es otra historia.
           En Espa&ntilde;a, quien se encarga es la <b>Agencia Espa&ntilde;ola de Protecci&oacute;n de Datos</b>,
           y se le puede reclamar gratis.</p>
      </div>

''' + video('video-cookies', 'L1EqDetsFKU',
            u'Qu&eacute; son las cookies y c&oacute;mo funcionan, en 1 minuto',
            u'Fundaci&oacute;n Cibervoluntarios &middot; en espa&ntilde;ol',
            u'Un minuto, para fijar la diferencia entre la cookie que hace falta y la que te sigue.')) +

  bloque('02', u'Pr&aacute;ctica &middot; 25 min', ficha(
    u'Actividad 8.3 &middot; Auditor&iacute;a de tu propio m&oacute;vil',
    [u'6.3'], u'Individual &middot; 25 min &middot; sobre 10', u'''
          <div class="nota">
            <span class="n-tag">Antes de empezar</span>
            Esto se hace <b>en tu m&oacute;vil y para tu cuaderno</b>. No se entrega ninguna captura, no se
            ense&ntilde;a la pantalla a nadie y no hay que decir en voz alta qu&eacute; aplicaciones tienes.
            Quien no traiga m&oacute;vil lo hace con el ordenador del aula, que tambi&eacute;n tiene ajustes
            de privacidad.
          </div>
          <h4>Qu&eacute; hay que hacer</h4>
          <ol class="pasos">
            <li><b>Cuenta.</b> En <i>Ajustes &rarr; Privacidad</i> (o <i>Aplicaciones &rarr; Permisos</i>),
                anota cu&aacute;ntas aplicaciones tienen concedido cada permiso:
                <b>ubicaci&oacute;n</b>, <b>micr&oacute;fono</b>, <b>c&aacute;mara</b>, <b>contactos</b> y
                <b>fotos</b>. Una tabla de cinco filas.</li>
            <li><b>Juzga tres.</b> Elige <b>tres</b> aplicaciones que te hayan sorprendido y contesta, para
                cada una: &iquest;<b>necesita</b> ese permiso para hacer lo que hace? Si crees que s&iacute;,
                explica para qu&eacute;. Si crees que no, dilo y <b>qu&iacute;taselo</b> ah&iacute; mismo.</li>
            <li><b>La cuenta de los puntos.</b> Rehaz la cuenta de la ubicaci&oacute;n con los datos de
                clase y escribe <b>tres cosas concretas</b> que se pueden deducir de tus 8.640 puntos de
                un mes. Que sean cosas que <b>t&uacute;</b> podr&iacute;as deducir de los puntos de otra
                persona.</li>
            <li><b>Tu huella.</b> En la escena de arriba, anota <b>cu&aacute;ntos bits</b> te salen y
                <b>cu&aacute;nta gente</b> comparte tu combinaci&oacute;n. Comp&aacute;ralo con el de al lado:
                &iquest;os sale lo mismo? &iquest;<b>Qu&eacute; rasgo</b> os diferencia? Y una pregunta que
                hay que razonar: si los dos ten&eacute;is el <b>mismo modelo de m&oacute;vil</b>,
                &iquest;ten&eacute;is la misma huella?</li>
            <li><b>El dinero.</b> Con los dos n&uacute;meros del principio de la sesi&oacute;n, calcula lo que
                ingresa esa empresa <b>por persona y a&ntilde;o</b> y <b>por persona y d&iacute;a</b>. Y
                contesta: si por cada uno ganan tan poco, <b>&iquest;por qu&eacute; se pelean tanto por
                tenerte un rato m&aacute;s?</b></li>
            <li><b>Una decisi&oacute;n.</b> Escribe <b>una sola frase</b>: algo que hayas decidido cambiar
                &mdash;o no cambiar&mdash; despu&eacute;s de esto, <b>y por qu&eacute;</b>. Vale perfectamente
                &laquo;no voy a cambiar nada, porque me compensa&raquo; si va razonado.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>La tabla de permisos est&aacute; hecha sobre el aparato de verdad <b>(2 puntos)</b>.</li>
            <li>Las tres aplicaciones est&aacute;n <b>razonadas</b>, no solo listadas <b>(2 puntos)</b>.</li>
            <li>Las tres deducciones de la ubicaci&oacute;n son concretas y posibles <b>(2 puntos)</b>.</li>
            <li>La comparaci&oacute;n de huellas est&aacute; hecha y la pregunta del mismo modelo est&aacute;
                bien razonada <b>(2 puntos)</b>.</li>
            <li>Las dos divisiones est&aacute;n bien y la frase final est&aacute; justificada <b>(2 puntos)</b>.</li>
          </ul>
          <div class="nota" style="margin-top:14px">
            <span class="n-tag">Sobre el paso 4</span>
            Dos m&oacute;viles del mismo modelo dan muchos rasgos iguales, pero casi nunca todos: el idioma,
            las aplicaciones instaladas, el brillo o el nivel de bater&iacute;a cambian cosas. Lo interesante
            es justo eso: <b>cu&aacute;ntos rasgos hacen falta</b> para distinguir a dos personas parecidas.
          </div>
  ''')) +

  bloque('03', u'Cierre &middot; 5 min', u'''
      <ol>
      ''' + pregunta(u'Si con https nadie puede leer lo que mandas, &iquest;c&oacute;mo saben tanto de ti?',
                     u'<p>Porque no hace falta leer nada por el camino. Una parte <b>se la damos nosotros</b> al usar el servicio: lo que miramos, cu&aacute;nto rato, d&oacute;nde estamos, qu&eacute; permisos concedemos. Y otra parte la da el aparato solo, con su <b>huella</b> y con las <b>cookies</b>. El cifrado protege el camino; no protege lo que entregas al llegar.</p>')
        + pregunta(u'&iquest;Qu&eacute; diferencia hay entre una cookie y la huella digital?',
                   u'<p>La cookie es algo que te <b>ponen dentro</b> del navegador, as&iacute; que se puede ver y <b>borrar</b>. La huella no te la pone nadie: es la <b>combinaci&oacute;n</b> de c&oacute;mo es tu aparato, y por eso sigue ah&iacute; aunque borres todo. Una es una pegatina; la otra, reconocerte por la cara.</p>')
        + pregunta(u'Una aplicaci&oacute;n de linterna te pide permiso de ubicaci&oacute;n. &iquest;Qu&eacute; piensas?',
                   u'<p>Que una linterna es una bombilla: no necesita saber d&oacute;nde est&aacute;s para encenderse. Cuando un permiso <b>no le hace falta</b> a la aplicaci&oacute;n para funcionar, lo normal es que lo pida <b>para otra cosa</b>, y esa otra cosa suele ser venderlo. Se le quita y se comprueba si sigue funcionando: casi siempre, s&iacute;.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Lo que llevas del tema</span>
        Ya tienes las tres capas: <b>c&oacute;mo llega</b> lo que pides (paquetes, direcciones, routers y
        nombres), <b>qui&eacute;n lo ve pasar</b> (y por qu&eacute; el candado protege unas cosas y otras no) y
        <b>qu&eacute; dejas t&uacute; por el camino</b> sin que nadie te lo robe.
      </div>
      <div class="nota">
        <span class="n-tag">Lo que falta</span>
        Quedan tres sesiones para cerrarlo: c&oacute;mo se guarda una <b>contrase&ntilde;a</b> y por qu&eacute;
        lo que manda es lo larga que sea; qu&eacute; es de verdad <b>la nube</b> y d&oacute;nde est&aacute;
        exactamente esa foto tuya; y qu&eacute; <b>derechos</b> tienes sobre tus datos y c&oacute;mo se
        ejercen, que son gratis y casi nadie los usa.
      </div>
      <div class="nota">
        <span class="n-tag">Y despu&eacute;s del tema</span>
        Sabes c&oacute;mo funciona la red y qu&eacute; rastro deja. La unidad siguiente le da la vuelta a la
        pregunta: ya no eres quien mira, sino quien <b>publica</b>. C&oacute;mo se produce y se difunde algo
        propio con estas herramientas &mdash;y ah&iacute; se cierra el c&iacute;rculo que abriste en la unidad
        de representaci&oacute;n gr&aacute;fica, cuando aprendiste a explicar lo que hab&iacute;as hecho.
      </div>
  '''))


# ==========================================================================
# SESION 4 · La contrasena: larga gana a rara
# ==========================================================================
S4 = (
  bloque('00', u'Reto inicial &middot; 10 min', u'''
      <p>De la sesi&oacute;n anterior te llevas una idea inc&oacute;moda: casi todo lo que saben de ti
         <b>se lo damos nosotros</b>. Pero hay una parte que no se da. Tus mensajes, tus notas, las
         fotos que no has publicado. Eso est&aacute; detr&aacute;s de una puerta, y esa puerta la cierra
         <b>una palabra</b>.</p>
      <p>Sobre c&oacute;mo tiene que ser esa palabra te han dado mil veces la misma receta: may&uacute;sculas,
         n&uacute;meros y alg&uacute;n signo raro. Vamos a <b>comprobarla</b>, que es distinto de
         cre&eacute;rsela.</p>

      <div class="aviso">
        <span class="n-tag">El encargo</span>
        Aqu&iacute; van dos contrase&ntilde;as. Escribe en el cuaderno <b>cu&aacute;l de las dos aguanta
        m&aacute;s</b> y por qu&eacute;. No vale &laquo;la primera, porque es m&aacute;s rara&raquo;:
        hay que decir <b>cu&aacute;ntas hay</b> de cada clase.
        <div style="font-family:var(--f-m);font-size:15px;margin-top:10px;line-height:1.9">
          <b>A)</b> Ab3$x!Qz<br>
          <b>B)</b> tres cabras en el tejado
        </div>
      </div>

      <p>Casi toda la clase elige la <b>A</b>, y con motivo: es la que <i>parece</i> dif&iacute;cil. La B se
         lee de un vistazo, no tiene un solo n&uacute;mero y parece una tonter&iacute;a. Hagamos la
         cuenta, que para eso est&aacute;.</p>

      <div class="reto-piensa">
        <span class="n-tag">Las dos cuentas</span>
        <p><b>1.</b> En la A hay <b>8</b> sitios y en cada uno puede ir una letra (52, contando
           may&uacute;sculas), un n&uacute;mero (10) o un signo (unos 32): <b>94</b> cosas. Son
           94 &times; 94 &times; &hellip; ocho veces: <b>94<sup>8</sup></b>. Hazlo por pasos, que
           as&iacute; cabe en cualquier calculadora: 94<sup>2</sup> = 8.836; ese al cuadrado,
           94<sup>4</sup> = 78.074.896; y ese al cuadrado,
           <b>94<sup>8</sup> = 6.095.689.385.410.816</b>. Cuenta las cifras: <b>16</b>.</p>
        <p><b>2.</b> En la B hay <b>24</b> sitios, y en cada uno solo cabe una min&uacute;scula o un
           espacio: <b>27</b> cosas. Son <b>27<sup>24</sup></b>, y ese s&iacute; se sale de la
           calculadora. Te lo damos hecho: es un <b>2 seguido de 34 cifras</b>.</p>
        <p><b>3.</b> Con las cifras de cada uno, contesta: <b>&iquest;cu&aacute;ntas veces m&aacute;s
           grande es el mont&oacute;n de la B?</b></p>
      </div>

      <p>La B no gana por poco: gana por <b>un 1 seguido de dieciocho ceros</b> de veces. Un trill&oacute;n.
         Y es la que parec&iacute;a de broma.</p>

      <p>El motivo es que las dos cosas que le puedes hacer a una contrase&ntilde;a <b>no valen
         igual</b>:</p>
      <ul>
        <li><b>Hacerla rara</b> agranda el alfabeto: pasas de 26 letras a 94 teclas. Eso multiplica
            el mont&oacute;n <b>una sola vez</b>.</li>
        <li><b>Hacerla larga</b> a&ntilde;ade sitios. Y <b>cada sitio nuevo vuelve a multiplicar</b> por
            el alfabeto entero.</li>
      </ul>

      <div class="reto-piensa">
        <span class="n-tag">Y ahora la cuenta que lo remata</span>
        <p>Partimos de ocho min&uacute;sculas: 26<sup>8</sup> = 208.827.064.576.</p>
        <p style="margin-top:8px">&middot; Si la llenas de may&uacute;sculas, n&uacute;meros y signos
           &rarr; 94<sup>8</sup>. Has multiplicado el mont&oacute;n por <b>29.190</b>.</p>
        <p>&middot; Si la dejas en min&uacute;sculas y le a&ntilde;ades <b>cuatro letras m&aacute;s</b>
           &rarr; 26<sup>12</sup>. Has multiplicado por <b>456.976</b>.</p>
        <p style="margin-top:8px">Cuatro letras de nada valen <b>quince veces m&aacute;s</b> que
           llenarla de s&iacute;mbolos. Y las cuatro letras <b>te las acuerdas</b>.</p>
      </div>
  ''') +

  bloque('01', u'Teor&iacute;a &middot; 20 min', u'''
      <h3>Lo que hace fuerte a una contrase&ntilde;a es el mont&oacute;n</h3>
      <p>Escribe abajo lo que quieras y mira los n&uacute;meros. Prueba primero algo corto y raro,
         despu&eacute;s algo largo y f&aacute;cil, y f&iacute;jate en las cuatro cajas del medio: son la
         misma contrase&ntilde;a con <b>un carácter m&aacute;s</b> cada vez.</p>

''' + ESCENA_FUERZA + u'''
      <div class="copiar">
        <h4>El mont&oacute;n</h4>
        <p>Una contrase&ntilde;a es fuerte cuando es <b>una de un mont&oacute;n enorme</b>. El
           mont&oacute;n se calcula as&iacute;:</p>
        <p style="font-family:var(--f-m);font-size:15px;text-align:center;margin:10px 0">
           combinaciones = alfabeto <sup>longitud</sup></p>
        <ul>
          <li><b>Alfabeto</b>: cu&aacute;ntas cosas distintas pueden ir en cada sitio (26 si solo hay
              min&uacute;sculas, 62 con may&uacute;sculas y n&uacute;meros, unas 94 con todo).</li>
          <li><b>Longitud</b>: cu&aacute;ntos sitios hay.</li>
        </ul>
        <p>La consecuencia, que es toda la sesi&oacute;n en una l&iacute;nea: <b>a&ntilde;adir un
           carácter multiplica el mont&oacute;n por el alfabeto entero; hacerla rara solo agranda el
           alfabeto, y una sola vez</b>.</p>
        <p>Por eso <b>larga gana a rara</b>. Y hay un premio de regalo: una contrase&ntilde;a larga y
           f&aacute;cil <b>te la acuerdas</b>, y la que te acuerdas es la que no acabas apuntada en un
           papel ni repetida en diez sitios.</p>
      </div>

      <div class="copiar" style="border-color:var(--goo-rojo)">
        <h4>Pero esa cuenta solo vale si es al azar</h4>
        <p>El mont&oacute;n de arriba supone que <b>todas las combinaciones son igual de probables</b>.
           Con tu nombre, tu equipo, tu a&ntilde;o de nacimiento, el nombre de tu perro o la frase de
           una canci&oacute;n, eso <b>deja de ser verdad</b>: quien prueba no empieza por
           <i>aaaaaaaa</i>, empieza por ah&iacute;.</p>
        <p>Por eso en la escena <i>Pelusa2012</i> sale con la barra larga y va marcada en rojo: la
           cuenta dice que es grande, y la realidad dice que no, porque <b>no es al azar</b>.</p>
        <p>La regla que sobrevive: <b>larga, y que no salga de ning&uacute;n sitio</b>. Ni de tu vida ni
           de un libro.</p>
      </div>

      <h3>Entonces, &iquest;c&oacute;mo se pierden las contrase&ntilde;as?</h3>
      <p>Aqu&iacute; hay algo que no cuadra. Si el mont&oacute;n es tan gordo que no se acaba nunca, nadie
         deber&iacute;a entrar en ninguna cuenta jam&aacute;s. Y sin embargo pasa todos los d&iacute;as.
         &iquest;Por d&oacute;nde?</p>
      <p>No por tu puerta: <b>por la del otro lado</b>. Las contrase&ntilde;as casi nunca se adivinan una
         a una &mdash;eso es lo que acabas de ver que no sale a cuenta&mdash;: <b>se escapan de las
         webs, a millones y de golpe</b>. As&iacute; que la pregunta que importa es otra: cuando te
         registras, <b>&iquest;qu&eacute; guarda exactamente esa web?</b></p>
      <p>La respuesta ingenua es &laquo;mi contrase&ntilde;a, en una lista&raquo;. Si fuera eso, el
         d&iacute;a que alguien se llevara la lista tendr&iacute;a las de todo el mundo y no
         habr&iacute;a nada que hacer. Por eso una web bien hecha <b>no guarda tu contrase&ntilde;a</b>.
         Escribe una abajo y mira lo que guarda de verdad.</p>

''' + ESCENA_HASH + u'''
      <div class="copiar">
        <h4>Huella (o <i>hash</i>)</h4>
        <p><b>Huella</b>: el resultado de pasar un texto por una cuenta que siempre da el mismo
           n&uacute;mero de cifras y que <b>no se puede deshacer</b>.</p>
        <p>Tiene tres propiedades, y son justo las tres que hacen falta:</p>
        <ol>
          <li>Del <b>mismo</b> texto sale <b>siempre la misma</b> huella.</li>
          <li>De un texto <b>parecido</b> sale una huella <b>completamente distinta</b>.</li>
          <li>De la huella <b>no se puede volver</b> al texto.</li>
        </ol>
        <p>Por eso una web bien hecha <b>no sabe cu&aacute;l es tu contrase&ntilde;a</b>. Cuando entras,
           calcula la huella de lo que escribes y la compara con la que tiene guardada. Si coinciden,
           te abre.</p>
        <p>Y de ah&iacute; sale una se&ntilde;al que puedes usar hoy mismo: si se te olvida la
           contrase&ntilde;a y una web <b>te la manda por correo tal cual</b>, es que la ten&iacute;a
           guardada en claro. Una bien hecha no puede: solo puede darte una <b>nueva</b>.</p>
      </div>

      <div class="copiar">
        <h4>La sal</h4>
        <p><b>Sal</b>: un trozo de texto al azar que la web le pega delante a tu contrase&ntilde;a
           <b>antes</b> de calcular la huella. Cada usuario lleva la suya.</p>
        <p>No es secreta &mdash;est&aacute; guardada al lado&mdash; y no sirve para esconder nada. Sirve
           para que <b>dos personas con la misma contrase&ntilde;a no tengan la misma huella</b>, y
           as&iacute; una lista robada no se pueda cruzar con otra. Pruébalo en la escena: pulsa
           &laquo;con sal&raquo; y mira c&oacute;mo las dos l&iacute;neas dejan de coincidir.</p>
      </div>

      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; no hace falta copiarlo</span>
        <p>Hay un detalle que parece un error y no lo es: las cuentas que se usan para guardar
           contrase&ntilde;as est&aacute;n hechas <b>a prop&oacute;sito para ir lentas</b>. En cualquier
           otro sitio de la inform&aacute;tica se pelea por ir r&aacute;pido; aqu&iacute;, al
           rev&eacute;s. La raz&oacute;n es la escena de antes: t&uacute; entras <b>una vez</b> y no
           notas si tarda dos d&eacute;cimas, pero quien tenga una lista robada tiene que probar
           <b>millones</b>, y esas dos d&eacute;cimas le multiplican el trabajo por un mill&oacute;n.</p>
        <p>Eso explica los tres ritmos de la escena de arriba. El del medio y el de la derecha son la
           misma lista robada: lo &uacute;nico que cambia es si la web hizo bien los deberes. Con las
           contrase&ntilde;as <b>cortas y comunes</b> da igual lo que hiciera, porque esas se
           encuentran igual; con una <b>larga</b>, no se encuentra ninguna de las dos maneras. Por eso
           la longitud te protege incluso de los errores <b>de otro</b>.</p>
      </div>

      <h3>El problema de verdad no es esa contrase&ntilde;a: es repetirla</h3>
      <p>Y aqu&iacute; llega el sitio donde de verdad se pierde todo. Piensa en cu&aacute;ntas cuentas
         tienes &mdash;el correo, el instituto, dos o tres juegos, la tienda de zapatillas, el foro
         aquel que abriste una vez&mdash;. Ahora piensa en cu&aacute;ntas <b>comparten
         contrase&ntilde;a</b>.</p>

      <div class="copiar" style="border-color:var(--goo-rojo)">
        <h4>Repetirla</h4>
        <p>Si pones la misma contrase&ntilde;a en varios sitios, su fuerza <b>ya no la decides
           t&uacute;</b>: la decide <b>la web peor hecha de todas aquellas en las que la has
           puesto</b>. Ese foro que abriste una vez y del que no te acuerdas.</p>
        <p>Porque el d&iacute;a que a esa web se le escape la lista, lo que se escapa no es una puerta:
           son <b>todas las que abre esa llave</b>. Y como el usuario suele ser tu correo, ni siquiera
           hay que averiguar d&oacute;nde probarla.</p>
        <p>De todas, hay una que no es una puerta m&aacute;s: <b>la del correo</b>. Con el correo se
           recuperan casi todas las dem&aacute;s, as&iacute; que quien entra ah&iacute; entra en todo lo
           dem&aacute;s sin saber ninguna otra contrase&ntilde;a. <b>Esa va distinta de todas, larga, y
           con segundo factor.</b></p>
      </div>

      <h3>Si tienen que ser largas y distintas, no caben en la cabeza</h3>
      <p>Y es verdad: no caben. Cuarenta contrase&ntilde;as largas y distintas no se acuerda nadie. Esa
         es exactamente la raz&oacute;n de que exista la herramienta siguiente, y no al rev&eacute;s.</p>

      <div class="copiar">
        <h4>Gestor de contrase&ntilde;as</h4>
        <p><b>Gestor de contrase&ntilde;as</b>: un programa que <b>inventa</b> una contrase&ntilde;a
           larga y al azar para cada sitio, las <b>guarda cifradas</b> y las <b>escribe por ti</b>
           cuando entras.</p>
        <p>Te deja tener que acordarte de <b>una sola</b>: la que abre el gestor. Esa s&iacute; tiene
           que ser larga, tuya y que no salga de ning&uacute;n sitio.</p>
        <p>Y hace una cosa que se cuenta poco y vale mucho: <b>no escribe la contrase&ntilde;a en una
           web que no sea la buena</b>. &Eacute;l mira el dominio, y el dominio no lo enga&ntilde;a una
           p&aacute;gina clavada a la del instituto. T&uacute; s&iacute; te puedes distraer; &eacute;l
           no.</p>
        <p>Los navegadores llevan uno dentro, y hay programas libres que valen para todo. Gratis,
           los dos.</p>
      </div>

      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; no hace falta copiarlo</span>
        <p>La objeci&oacute;n salta sola, y es buena: <b>&laquo;&iquest;y si me roban el gestor? Lo
           pierdo todo de golpe&raquo;</b>. Es verdad que pone los huevos en una cesta. La respuesta
           tiene dos partes.</p>
        <p>La primera: lo que hay dentro est&aacute; <b>cifrado con tu contrase&ntilde;a maestra</b>, y
           quien se lleve el fichero se lleva ruido &mdash;la escena del candado, otra vez&mdash;. La
           segunda, y es la que decide: lo que haces si no lo usas <b>tampoco es seguro</b>. Es repetir
           la misma en veinte sitios, y eso ya sabes lo que vale. No se compara el gestor con lo ideal;
           se compara con <b>lo que hay</b>.</p>
      </div>

      <h3>Y por si acaso: una segunda cerradura</h3>
      <p>Todo lo anterior protege la contrase&ntilde;a. Pero una contrase&ntilde;a se puede perder de
         maneras que no dependen de lo larga que sea: te la ve alguien por encima del hombro, la
         escribes sin darte cuenta en una p&aacute;gina que imita a la buena, se te escapa en un
         ordenador prestado. Por eso la segunda idea no es hacerla mejor: es que <b>haga falta algo
         m&aacute;s</b>.</p>

''' + foto('u8-llave-2fa.jpg',
           u'Llave de seguridad USB negra con un bot&oacute;n dorado, sobre una tela clara',
           u'Una <b>llave de seguridad</b>: un segundo factor de los de tocar. Se enchufa o se acerca al '
           u'm&oacute;vil y hay que <b>ponerle el dedo encima</b> para entrar. Quien te robe la '
           u'contrase&ntilde;a estar&aacute; probablemente a mil kil&oacute;metros, y esto no lo puede '
           u'copiar por un cable: hay que tenerlo en la mano. No hace falta comprar una &mdash;el '
           u'c&oacute;digo del m&oacute;vil hace el mismo papel&mdash;, pero se ve muy bien en la foto '
           u'de qu&eacute; estamos hablando.',
           u'Tony Webster', u'CC BY 2.0',
           u'https://commons.wikimedia.org/wiki/File:Yubikey_USB_2FA_U2F_Security_Token_(46900270791).jpg') + u'''
      <div class="copiar">
        <h4>Segundo factor</h4>
        <p><b>Segundo factor</b> (o verificaci&oacute;n en dos pasos): pedir <b>dos cosas de clases
           distintas</b> para entrar. Normalmente <b>algo que sabes</b> (la contrase&ntilde;a) m&aacute;s
           <b>algo que tienes</b> (el m&oacute;vil, una llave).</p>
        <p>Funciona porque quien te roba la contrase&ntilde;a <b>no est&aacute; donde est&aacute;s
           t&uacute;</b>: est&aacute; lejos, con una lista, y no tiene tu tel&eacute;fono en la mano.</p>
        <p>De mejor a peor, y todos mejor que nada:</p>
        <ul>
          <li><b>Llave f&iacute;sica</b>: hay que tenerla y tocarla. La m&aacute;s dura.</li>
          <li><b>Aplicaci&oacute;n de c&oacute;digos</b>: el m&oacute;vil genera un n&uacute;mero nuevo
              cada 30 segundos, sin conexi&oacute;n. Gratis y muy buena.</li>
          <li><b>C&oacute;digo por SMS</b>: el m&aacute;s d&eacute;bil de los tres, porque un
              n&uacute;mero de tel&eacute;fono se puede acabar desviando. Aun as&iacute;, <b>mucho mejor
              que no tener nada</b>.</li>
        </ul>
        <p>Cuando lo actives te dar&aacute;n unos <b>c&oacute;digos de recuperaci&oacute;n</b>. Son para
           el d&iacute;a que pierdas el m&oacute;vil: se guardan <b>en papel</b>, fuera del
           tel&eacute;fono. Si no, el d&iacute;a que se te caiga al agua te quedas fuera t&uacute;.</p>
      </div>

''' + video('video-2fa', 'Q-jjSRovIIA',
            u'Activaci&oacute;n del Doble Factor de Autenticaci&oacute;n',
            u'UOC &middot; Universitat Oberta de Catalunya &middot; en espa&ntilde;ol',
            u'Para ver el paso a paso de activarlo, que es m&aacute;s f&aacute;cil de lo que parece.')) +

  bloque('02', u'Pr&aacute;ctica &middot; 25 min', ficha(
    u'Actividad 8.4 &middot; La cuenta de tu propia puerta',
    [u'6.2', u'6.3'], u'Individual &middot; 25 min &middot; sobre 10', u'''
          <div class="nota">
            <span class="n-tag">Antes de empezar</span>
            En el cuaderno <b>no se escribe ninguna contrase&ntilde;a de verdad</b>, y en la escena
            tampoco: si quieres probar la tuya, escribe <b>una parecida</b> &mdash;igual de larga y del
            mismo estilo&mdash;, que la cuenta sale igual. La escena no manda nada a ninguna parte, pero
            no escribir la tuya por ah&iacute; es una costumbre que conviene coger.
          </div>
          <h4>Qu&eacute; hay que hacer</h4>
          <ol class="pasos">
            <li><b>Las dos del reto, terminadas.</b> Escribe 94<sup>8</sup> con los tres pasos
                (94<sup>2</sup>, 94<sup>4</sup>, 94<sup>8</sup>) y d&eacute;jalo apuntado con sus 16
                cifras. Debajo, la comparaci&oacute;n con las 35 de la B y <b>cu&aacute;ntas veces
                m&aacute;s</b> es.</li>
            <li><b>La tabla que decide.</b> Rellena esta tabla de combinaciones:
                <ul>
                  <li>8 caracteres, solo min&uacute;sculas (26<sup>8</sup>)</li>
                  <li>8 caracteres, con todo (94<sup>8</sup>)</li>
                  <li>12 caracteres, solo min&uacute;sculas (26<sup>12</sup>)</li>
                  <li>16 caracteres, solo min&uacute;sculas (26<sup>16</sup>)</li>
                </ul>
                Y contesta en una frase: <b>&iquest;qu&eacute; sube m&aacute;s el mont&oacute;n</b>,
                llenar de s&iacute;mbolos una de 8, o dejarla en min&uacute;sculas y alargarla?</li>
            <li><b>La escena, con el ritmo cambiado.</b> Escribe una de <b>8</b> caracteres con de todo
                y anota el tiempo; escribe una de <b>20</b> en min&uacute;sculas y anota el suyo. Ahora
                cambia el ritmo a los tres y anota los seis tiempos. Contesta: al cambiar de ritmo,
                <b>&iquest;cambia cu&aacute;l de las dos gana?</b> &iquest;Por qu&eacute;?</li>
            <li><b>Cuenta tus puertas.</b> Sin escribir ninguna contrase&ntilde;a ni decir de
                qu&eacute; sitio es: &iquest;en cu&aacute;ntos sitios tienes cuenta? &iquest;En
                cu&aacute;ntos de ellos has puesto <b>la misma</b>? Escribe solo los dos
                n&uacute;meros, y debajo una frase: si la peor de esas webs pierde su lista,
                <b>&iquest;cu&aacute;ntas puertas se abren?</b></li>
            <li><b>La huella.</b> En la escena del <i>hash</i>, escribe una palabra cualquiera y anota
                sus <b>ocho primeras cifras</b>. B&oacute;rrala, escr&iacute;bela otra vez:
                &iquest;sale igual? Cambia una letra: &iquest;cu&aacute;ntas de las 64 cifras cambian?
                Y contesta lo importante: si una web solo guarda <b>esto</b>, &iquest;puede
                <b>decirte</b> cu&aacute;l era tu contrase&ntilde;a cuando se te olvide?
                &iquest;Qu&eacute; es lo &uacute;nico que puede hacer?</li>
            <li><b>Tu plan, en tres l&iacute;neas.</b> Una: c&oacute;mo vas a hacer la del correo (sin
                escribirla). Dos: si vas a usar gestor y cu&aacute;l. Tres: en qu&eacute; dos cuentas
                vas a activar el segundo factor esta semana. Vale decir &laquo;no voy a cambiar
                nada&raquo; si lo razonas con n&uacute;meros.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>La potencia est&aacute; hecha por pasos y la comparaci&oacute;n es correcta
                <b>(2 puntos)</b>.</li>
            <li>La tabla est&aacute; completa y la frase final distingue <b>alargar</b> de
                <b>complicar</b> <b>(2 puntos)</b>.</li>
            <li>Los seis tiempos est&aacute;n anotados y se ve que el orden <b>no depende del ritmo</b>
                <b>(2 puntos)</b>.</li>
            <li>Las dos cuentas de las puertas est&aacute;n hechas y la frase entiende el
                efecto domin&oacute; <b>(2 puntos)</b>.</li>
            <li>La prueba de la huella est&aacute; hecha y se contesta que la web <b>no puede
                devolv&eacute;rtela</b>, solo darte una nueva <b>(2 puntos)</b>.</li>
          </ul>
          <div class="nota" style="margin-top:14px">
            <span class="n-tag">Sobre el paso 3</span>
            Los tiempos cambian mucho de un ritmo a otro &mdash;de a&ntilde;os a horas&mdash;, y eso
            asusta. Lo que hay que mirar no es el n&uacute;mero: es que <b>la larga gana en los tres</b>.
            Cuando una conclusi&oacute;n aguanta con supuestos muy distintos, es que la
            conclusi&oacute;n es buena.
          </div>
  ''')) +

  bloque('03', u'Cierre &middot; 5 min', u'''
      <ol>
      ''' + pregunta(u'&iquest;Por qu&eacute; una contrase&ntilde;a larga y f&aacute;cil gana a una corta y rara?',
                     u'<p>Porque <b>cada carácter que a&ntilde;ades multiplica</b> el mont&oacute;n por el alfabeto entero, mientras que hacerla rara <b>solo agranda el alfabeto, y una vez</b>. Partiendo de ocho min&uacute;sculas, llenarla de s&iacute;mbolos la multiplica por 29.190 y a&ntilde;adirle cuatro letras la multiplica por 456.976. Y encima la larga te la acuerdas.</p>')
        + pregunta(u'Una web bien hecha, &iquest;qu&eacute; guarda cuando te registras?',
                   u'<p>No guarda tu contrase&ntilde;a: guarda su <b>huella</b>, que es una cuenta que no se puede deshacer, normalmente con una <b>sal</b> delante. Cuando entras, calcula la huella de lo que escribes y la compara. Por eso, si se te olvida, una web bien hecha <b>no puede mand&aacute;rtela</b>: solo puede darte una nueva.</p>')
        + pregunta(u'Tienes una contrase&ntilde;a larguísima, pero la misma en ocho sitios. &iquest;Es fuerte?',
                   u'<p>No. Su fuerza ya no la decides t&uacute;: la decide <b>la peor de esas ocho webs</b>. El d&iacute;a que a una se le escape la lista, se abren las ocho puertas a la vez, porque adem&aacute;s el usuario suele ser el mismo correo. Larga <b>y distinta</b> en cada sitio; y para poder hacerlo, un gestor.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya sabes cerrar la puerta. Pero hay una pregunta que no hemos hecho todav&iacute;a, y es de las
        raras: detr&aacute;s de esa puerta, <b>&iquest;d&oacute;nde est&aacute;n exactamente tus
        cosas?</b> La foto que subiste ayer no est&aacute; &laquo;en el m&oacute;vil&raquo;, y
        &laquo;en la nube&raquo; no es una respuesta: es el nombre de la pregunta.
      </div>
  '''))


# ==========================================================================
# SESION 5 · La nube
# ==========================================================================
S5 = (
  bloque('00', u'Reto inicial &middot; 10 min', u'''
      <p>Ya sabes cerrar la puerta. Vamos con lo que hay detr&aacute;s, que es una pregunta que casi
         nadie se hace: la foto que subiste ayer, <b>&iquest;d&oacute;nde est&aacute;?</b></p>
      <p>Hay una manera de comprobar que no est&aacute; donde crees, y se hace en diez segundos.</p>

      <div class="aviso">
        <span class="n-tag">El encargo</span>
        Pon el m&oacute;vil en <b>modo avi&oacute;n</b> &mdash;sin datos, sin wifi&mdash; y abre la
        aplicaci&oacute;n donde guardas las fotos. Baja del todo, hasta las del a&ntilde;o pasado, y
        <b>intenta abrir tres</b>. Despu&eacute;s escribe en el cuaderno <b>qu&eacute; ha pasado</b> y,
        sobre todo, <b>d&oacute;nde estaban las que s&iacute; se han abierto y d&oacute;nde las que
        no</b>.
      </div>

      <p>Sale lo mismo en casi todos los m&oacute;viles: las de esta semana se abren y las viejas
         aparecen borrosas, o no aparecen. Las que se abren estaban <b>ah&iacute; dentro</b>. Las otras
         no estaban: estaba <b>una miniatura</b>, como el cartel de una pel&iacute;cula que no
         tienes.</p>

      <p>Si le preguntas a alguien d&oacute;nde est&aacute;n las que faltan, la respuesta es
         &laquo;en la nube&raquo;. Y eso no es una respuesta: es <b>el nombre de la pregunta</b>. As&iacute;
         que vamos a contestarla de verdad. Piensa estas tres, que tienen respuesta concreta:</p>

      <div class="reto-piensa">
        <span class="n-tag">Tres preguntas con respuesta</span>
        <p><b>1.</b> Esa foto ocupa unos megas. Los megas est&aacute;n escritos en alg&uacute;n sitio
           f&iacute;sico. <b>&iquest;Qui&eacute;n paga la luz de ese sitio?</b></p>
        <p><b>2.</b> Ese sitio est&aacute; en un pa&iacute;s. <b>&iquest;En cu&aacute;l?</b>
           &iquest;Sabes siquiera en qu&eacute; continente?</p>
        <p><b>3.</b> Si dejas de pagar, o si te cierran la cuenta por lo que sea,
           <b>&iquest;qu&eacute; pasa con la foto?</b></p>
      </div>

      <p>Las tres tienen respuesta, y las tres apuntan a lo mismo: eso que llamamos nube <b>no
         est&aacute; en el aire</b>. Est&aacute; en un disco, dentro de un ordenador, dentro de un
         edificio que tiene una direcci&oacute;n, un due&ntilde;o, una factura de la luz y las leyes del
         pa&iacute;s donde est&eacute;. Se parece bastante a esto:</p>

''' + foto('u8-datacenter.jpg',
           u'Filas de ordenadores apilados en estanter&iacute;as met&aacute;licas, iluminados por luces azules, en la sala de un centro de datos',
           u'&laquo;La nube&raquo;, por dentro. Son <b>ordenadores en estanter&iacute;as</b>, uno encima de '
           u'otro, en una sala con aire acondicionado a tope &mdash;porque calientan&mdash; y con '
           u'generadores por si se va la luz. Las lucecitas azules quedan muy bien en la foto; lo que '
           u'de verdad importa de este sitio es lo aburrido: que tiene <b>una direcci&oacute;n postal, '
           u'un due&ntilde;o y un pa&iacute;s</b>. Tu foto est&aacute; en uno de esos discos.',
           u'BalticServers.com', u'CC BY-SA 3.0',
           u'https://commons.wikimedia.org/wiki/File:BalticServers_data_center.jpg') + u'''
      <p>De ah&iacute; sale la frase que ordena toda la sesi&oacute;n, y que no es un insulto sino una
         descripci&oacute;n: <b>la nube es el ordenador de otro</b>. En cuanto lo dices as&iacute;, las
         preguntas que hay que hacer se ordenan solas.</p>
  ''') +

  bloque('01', u'Teor&iacute;a &middot; 20 min', u'''
      <div class="copiar">
        <h4>La nube</h4>
        <p><b>La nube</b>: guardar tus archivos o hacer tus cuentas en <b>ordenadores de otra empresa</b>,
           a los que llegas por Internet, en vez de en el aparato que tienes delante.</p>
        <p>No es una tecnolog&iacute;a nueva ni m&aacute;gica: es la de siempre, <b>en el edificio de
           otro</b>. Lo que cambia es de qui&eacute;n es la m&aacute;quina, qui&eacute;n la cuida y
           qui&eacute;n pone las condiciones.</p>
      </div>

      <h3>Qu&eacute; se gana y qu&eacute; se pierde</h3>
      <p>Y se gana bastante. Por eso la usa todo el mundo, y estar&iacute;a mal contarlo como si fuera
         una trampa: es un <b>trato</b>, y como todos los tratos tiene dos columnas.</p>

      <div class="copiar">
        <h4>El trato de la nube</h4>
        <table>
          <tr><th>Lo que ganas</th><th>Lo que sueltas</th></tr>
          <tr><td>Llegas desde cualquier aparato, est&eacute;s donde est&eacute;s.</td>
              <td>Hace falta <b>conexi&oacute;n</b>. Sin ella, no hay archivos.</td></tr>
          <tr><td>No compras discos ni los cambias cuando se rompen.</td>
              <td>Pagas <b>todos los meses, para siempre</b>, y el precio lo ponen ellos.</td></tr>
          <tr><td>Si se rompe un disco suyo, ellos tienen m&aacute;s copias y no te enteras.</td>
              <td>Si <b>pierdes la cuenta</b>, lo pierdes todo de golpe, aunque los discos est&eacute;n
                  perfectos.</td></tr>
          <tr><td>Se comparte con un enlace, sin copiar nada.</td>
              <td>Est&aacute; en su m&aacute;quina: <b>sus normas y las leyes de su pa&iacute;s</b>.</td></tr>
        </table>
        <p>Dicho corto: <b>cambias trastos por dependencia</b>. Para much&iacute;simas cosas compensa. Lo
           que no compensa es hacerlo <b>sin saberlo</b>.</p>
      </div>

      <div class="reto-piensa">
        <span class="n-tag">Una cuenta que nadie hace hasta que le toca</span>
        <p>Tienes <b>60 GB</b> arriba y se te rompe el port&aacute;til. Te compras otro y te lo bajas
           todo. Tu conexi&oacute;n baja a <b>50 megabits por segundo</b>, que est&aacute; bien.</p>
        <p style="margin-top:8px">60 GB son <b>480.000 megabits</b>. Entre 50: <b>9.600 segundos</b>,
           o sea <b>2 horas y 40 minutos</b> sin poder hacer nada. Y si la conexi&oacute;n es de
           <b>5 Mbit/s</b> &mdash;la de casa de tu abuela, o la del pueblo en agosto&mdash;, son
           <b>96.000 segundos: casi 27 horas</b>.</p>
        <p style="margin-top:8px">Subir es gota a gota y no te enteras. <b>Bajar es de golpe</b>, y el
           d&iacute;a que lo necesites ser&aacute; justo el d&iacute;a que tengas prisa.</p>
      </div>

      <h3>Y ahora la confusi&oacute;n que cuesta cara</h3>
      <p>Casi todo el mundo cree que, por tener las cosas en la nube, <b>ya tiene copia de
         seguridad</b>. Es la creencia m&aacute;s extendida de esta unidad y es <b>falsa</b>. Y no es un
         detalle: es la diferencia entre perder un trabajo de tres semanas o no perderlo.</p>
      <p>Abajo tienes los sitios donde puede vivir un archivo. Ponlos y qu&iacute;talos, haz que pase
         algo y mira qui&eacute;n sobrevive. Empieza por el experimento que dice el pie.</p>

''' + ESCENA_NUBE + u'''
      <div class="copiar" style="border-color:var(--goo-rojo)">
        <h4>Sincronizar NO es copia de seguridad</h4>
        <p><b>Sincronizar</b>: que dos sitios tengan <b>siempre lo mismo</b>. Cambias algo aqu&iacute; y
           cambia all&iacute;, en segundos.</p>
        <p><b>Copia de seguridad</b>: guardar aparte <b>c&oacute;mo estaban las cosas en un
           momento</b>, y que eso <b>no cambie</b> aunque el original cambie.</p>
        <p>Y ah&iacute; est&aacute; la diferencia entera:</p>
        <ul>
          <li>Sincronizar te salva de que <b>se rompa el aparato</b>: el archivo est&aacute; en otro
              sitio.</li>
          <li>Sincronizar <b>no te salva de ti</b>. Si lo borras, lo borra. Si lo estropeas, lo
              estropea. <b>Copia el desastre, y lo copia r&aacute;pido</b>, que es lo que se le pide.</li>
        </ul>
        <p>Por eso la carpeta sincronizada es <b>comod&iacute;sima</b> y <b>no es una copia de
           seguridad</b>. Son dos herramientas distintas para dos miedos distintos, y hacen falta las
           dos.</p>
      </div>

      <h3>Entonces, &iquest;cu&aacute;ntas copias hacen falta?</h3>
      <p>La respuesta lleva d&eacute;cadas siendo la misma, y tiene la ventaja de que se recuerda con
         tres n&uacute;meros. Lo bonito es que <b>cada n&uacute;mero mata un desastre distinto</b>.</p>

      <div class="copiar">
        <h4>La regla 3-2-1</h4>
        <p><b>3</b> copias en total (el original y dos m&aacute;s) &middot; en <b>2</b> soportes
           distintos &middot; con <b>1</b> de ellas <b>fuera de casa</b>.</p>
        <ul>
          <li>El <b>3</b> mata el fallo suelto: que se rompa una cosa no te deja sin nada, y que se
              rompan dos a la vez el mismo d&iacute;a es raro.</li>
          <li>El <b>2</b> mata el fallo que se lleva un tipo entero: un modelo de disco que sale malo,
              o un programa que te borra todo lo que tenga delante.</li>
          <li>El <b>1</b> mata el fallo que se lleva un <b>sitio</b> entero: un incendio, una
              inundaci&oacute;n, un robo. Si las tres copias est&aacute;n en el mismo caj&oacute;n, son
              una.</li>
        </ul>
        <p>Y un cuarto n&uacute;mero que la regla no dice y la escena s&iacute;: de esas copias,
           <b>las que van sincronizadas cuentan poco</b>, porque repiten lo que le pase al original.
           Al menos una tiene que estar <b>aparte de verdad</b>.</p>
      </div>

''' + foto('u8-cintas.jpg',
           u'Pasillo entre estanter&iacute;as rojas llenas de bobinas de cinta magn&eacute;tica numeradas',
           u'Un <b>archivo de copias de seguridad</b> en cinta magn&eacute;tica, de los a&ntilde;os setenta. '
           u'Cada bobina lleva su n&uacute;mero y su fecha, est&aacute;n en una sala <b>aparte</b> y '
           u'<b>no cambian</b>: eso es exactamente lo que hace que sean copias de seguridad y no una '
           u'carpeta sincronizada. La tecnolog&iacute;a s&iacute; ha cambiado &mdash;hoy son cartuchos '
           u'peque&ntilde;os, no bobinas&mdash;, pero las bibliotecas y los bancos siguen usando cinta '
           u'por lo mismo de siempre: sale barata, dura d&eacute;cadas y, cuando est&aacute; en la '
           u'estanter&iacute;a, <b>no est&aacute; enchufada a nada</b>.',
           u'Linda Bartlett &middot; National Cancer Institute', u'Dominio p&uacute;blico',
           u'https://commons.wikimedia.org/wiki/File:Computer_tapes.jpg') + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; no hace falta copiarlo</span>
        <p>Queda un cabo suelto, y es justo: &laquo;pero mi nube tiene <b>papelera</b>, y guarda
           versiones viejas&raquo;. Es verdad, y ayuda mucho: la papelera de treinta d&iacute;as salva
           el borrado tonto, que es el m&aacute;s frecuente de todos. Pero f&iacute;jate en lo que es
           exactamente: una copia de seguridad <b>que gestiona otro, dentro de la misma cuenta y con un
           plazo que pone &eacute;l</b>. Si el problema es la cuenta &mdash;te la cierran, la pierdes,
           te la quitan&mdash;, la papelera se va con ella. Por eso cuenta como <b>media red</b>, no
           como la copia de fuera.</p>
        <p>Y hay un detalle que cambia la escala de todo esto: lo que de verdad hace da&ntilde;o no es
           perder un archivo, es <b>no enterarte de que lo has perdido</b>. Una copia que nadie ha
           probado a recuperar no es una copia: es una suposici&oacute;n. En sitios donde esto va en
           serio, lo que se apunta en el calendario no es el d&iacute;a de hacer la copia, sino el
           d&iacute;a de <b>probar a restaurarla</b>.</p>
      </div>

''' + video('video-321', 'PM_M4Iz6I4o',
            u'Backup 3-2-1, el m&eacute;todo definitivo para mantener a salvo tus datos',
            u'Xataka &middot; en espa&ntilde;ol',
            u'La misma regla contada con ejemplos de aparatos de hoy.')) +

  bloque('02', u'Pr&aacute;ctica &middot; 25 min', ficha(
    u'Actividad 8.5 &middot; &iquest;Sobrevivir&iacute;as?',
    [u'6.1', u'6.3'], u'Parejas &middot; 25 min &middot; sobre 10', u'''
          <h4>Qu&eacute; hay que hacer</h4>
          <ol class="pasos">
            <li><b>El experimento del pie.</b> En la escena: dejad la <b>nube</b>, a&ntilde;adid el
                <b>disco</b> y ponedlo <b>sincronizado</b>. Anotad los cuatro n&uacute;meros de la regla
                3-2-1 y si la cumpl&iacute;s. Ahora dadle a <b>&laquo;lo borro sin querer&raquo;</b> y anotad
                qu&eacute; queda. Escribid la moraleja en <b>una frase</b>.</li>
            <li><b>Y arregladlo.</b> Quitad el sincronizado del disco, reiniciad y repetid el mismo
                borrado. &iquest;Qu&eacute; cambia? Anotad los cuatro n&uacute;meros otra vez y decid
                <b>cu&aacute;l de los cuatro</b> es el que os ha salvado.</li>
            <li><b>Los cuatro desastres.</b> Montad la combinaci&oacute;n que os parezca buena y
                probad los cuatro: borrado, port&aacute;til roto, casa inundada y cuenta perdida. Haced
                una tabla de cuatro filas: <b>desastre &middot; qu&eacute; sobrevive &middot;
                cu&aacute;ntos d&iacute;as de trabajo pierdes</b>. Si alguno os deja sin nada, cambiad
                el montaje hasta que no.</li>
            <li><b>La cuenta de bajarlo todo.</b> Ten&eacute;is <b>250 GB</b> arriba (250.000 MB).
                Calculad cu&aacute;nto se tarda en bajarlo a <b>50 Mbit/s</b> y a <b>5 Mbit/s</b>.
                Acordaos de que un byte son 8 bits. Dad el resultado en <b>horas</b>.</li>
            <li><b>La cuenta del dinero.</b> Una nube de 2 TB cuesta del orden de <b>10 &euro; al
                mes</b>. Calculad lo que son <b>diez a&ntilde;os</b>. Comparadlo con lo que cuesta un
                disco externo de 2 TB (buscadlo). Y contestad: &iquest;quiere decir eso que el disco es
                mejor? <b>Decid qu&eacute; da cada uno que el otro no da.</b></li>
            <li><b>Vuestro plan de verdad.</b> Escribid el plan 3-2-1 para <b>vuestros trabajos del
                curso</b>: qu&eacute; tres sitios, qu&eacute; dos soportes, cu&aacute;l est&aacute;
                fuera de casa, y <b>cada cu&aacute;nto</b> toca hacer la copia. Tiene que ser un plan
                que pod&aacute;is cumplir de verdad esta semana, no uno bonito.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>El experimento est&aacute; hecho y la moraleja dice que <b>lo sincronizado copia el
                borrado</b> <b>(2 puntos)</b>.</li>
            <li>La segunda vuelta identifica el n&uacute;mero que salva: <b>las que no se
                sincronizan</b> <b>(2 puntos)</b>.</li>
            <li>La tabla de los cuatro desastres est&aacute; completa, con los d&iacute;as perdidos
                <b>(2 puntos)</b>.</li>
            <li>Las dos cuentas (horas y euros) est&aacute;n bien, con las unidades puestas
                <b>(2 puntos)</b>.</li>
            <li>El plan tiene los tres n&uacute;meros y una <b>periodicidad</b> realista
                <b>(2 puntos)</b>.</li>
          </ul>
          <div class="nota" style="margin-top:14px">
            <span class="n-tag">Sobre el paso 5</span>
            La respuesta buena <b>no</b> es &laquo;el disco, porque sale m&aacute;s barato&raquo;. El
            disco no se sincroniza solo, no llega desde el m&oacute;vil y, si se moja, se moja. La nube
            no te salva de un borrado y depende de una cuenta. Cada uno tapa el agujero del otro: por
            eso la regla pide <b>dos soportes</b> y no el mejor de los dos.
          </div>
  ''')) +

  bloque('03', u'Cierre &middot; 5 min', u'''
      <ol>
      ''' + pregunta(u'&iquest;Qu&eacute; es &laquo;la nube&raquo;, dicho sin adornos?',
                     u'<p>El <b>ordenador de otro</b>. Tus archivos est&aacute;n en discos que no son tuyos, en un edificio con direcci&oacute;n, due&ntilde;o, factura de la luz y las leyes de su pa&iacute;s. A cambio de eso ganas llegar desde cualquier sitio y no tener que comprar ni arreglar trastos.</p>')
        + pregunta(u'Tienes la carpeta sincronizada con la nube. Borras un trabajo sin querer. &iquest;Lo tienes a salvo?',
                   u'<p>No. Lo sincronizado <b>copia el borrado</b>, y en segundos: para eso est&aacute; hecho. Te salva de que se rompa el port&aacute;til, no de que te equivoques t&uacute;. Para eso hace falta una copia <b>aparte</b>, que no cambie cuando cambie el original. (La papelera de la nube salva muchas veces, pero tiene plazo y vive dentro de la misma cuenta.)</p>')
        + pregunta(u'&iquest;Por qu&eacute; la regla pide una copia <b>fuera de casa</b>?',
                   u'<p>Porque hay desastres que no se llevan un aparato: se llevan <b>un sitio entero</b>. Un incendio, una inundaci&oacute;n o un robo se llevan por igual el port&aacute;til y el disco del caj&oacute;n de al lado. Tres copias en la misma habitaci&oacute;n son, para esos casos, <b>una sola copia</b>.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Repasa lo que llevas: por d&oacute;nde viaja lo tuyo, qui&eacute;n lo ve pasar, qu&eacute; se
        recoge, c&oacute;mo se cierra la puerta y en qu&eacute; edificio acaba todo. En cinco sesiones
        siempre ha decidido <b>otro</b>. La &uacute;ltima va de lo contrario: <b>qu&eacute; puedes
        exigir t&uacute;</b>, a qui&eacute;n, y en cu&aacute;ntos d&iacute;as te tienen que contestar.
        Es gratis y casi nadie lo usa.
      </div>
  '''))


# ==========================================================================
# SESION 6 · Tus derechos, y el test que cierra la unidad
#
# Las diez preguntas son de TODO el tema, no solo de esta sesion: dos de cada
# una de las cinco anteriores mas la de hoy. Cada una explica por que, tambien
# cuando se acierta.
# ==========================================================================
PREGUNTAS_U8 = [
 dict(p=u'&iquest;Por qu&eacute; Internet no reserva un camino entero para cada conversaci&oacute;n?',
      op=[u'porque los cables no aguantar&iacute;an el peso de tantos datos',
          u'porque no cabe: har&iacute;an falta tantos caminos como parejas de usuarios, y cada uno '
          u'quedar&iacute;a ocupado sin usarse',
          u'porque los paquetes viajan m&aacute;s r&aacute;pido que una l&iacute;nea reservada'],
      ok=1,
      por=u'Es la cuenta de la primera sesi&oacute;n: en un instituto de 600 personas ya salen 179.700 '
          u'cables. Al trocear y <b>compartir</b>, el mismo cable sirve para much&iacute;simas '
          u'conversaciones a la vez. La velocidad no tiene nada que ver.'),
 dict(p=u'Escribes un nombre en el navegador. &iquest;Qu&eacute; pasa <b>antes</b> de que empiece a llegar la p&aacute;gina?',
      op=[u'se cifra el nombre con el candado',
          u'se parte el nombre en paquetes y se manda',
          u'hay que traducir el nombre a una direcci&oacute;n IP, y de eso se encarga el DNS'],
      ok=2,
      por=u'La red <b>solo sabe ir a n&uacute;meros</b>. El <b>DNS</b> es la agenda que convierte '
          u'aula.example.es en 192.0.2.41. Si nadie ten&iacute;a la respuesta guardada, hay que '
          u'preguntarla en varios sitios, y eso tarda unas d&eacute;cimas <b>antes</b> de todo lo '
          u'dem&aacute;s.'),
 dict(p=u'Est&aacute;s en una wifi abierta y entras en una web con candado. &iquest;Qu&eacute; puede saber quien controle esa wifi?',
      op=[u'nada en absoluto: el candado lo tapa todo',
          u'a qu&eacute; sitio te conectas y cu&aacute;nto mueves, pero no qu&eacute; dices',
          u'tu contrase&ntilde;a, porque la wifi es abierta'],
      ok=1,
      por=u'El candado protege el <b>contenido</b>, no el <b>destino</b>. Ve con qui&eacute;n hablas, '
          u'cu&aacute;ndo y cu&aacute;nto ocupa; no ve qu&eacute; le dices. Y eso, repetido durante un '
          u'rato, tambi&eacute;n cuenta bastante de una persona.'),
 dict(p=u'En criptograf&iacute;a, &iquest;qu&eacute; tiene que ser secreto?',
      op=[u'el m&eacute;todo, para que nadie sepa c&oacute;mo funciona',
          u'la clave; el m&eacute;todo se publica entero a prop&oacute;sito',
          u'los dos, y por eso se cambian cada d&iacute;a'],
      ok=1,
      por=u'Es la regla de Kerckhoffs, de 1883. Un secreto que tiene que saber mucha gente <b>no se '
          u'aguanta</b>, y si se escapa hay que cambi&aacute;rselo a todos a la vez. Publicando el '
          u'm&eacute;todo, si se escapa una clave se cambia <b>esa</b> y ya. Adem&aacute;s, un '
          u'm&eacute;todo publicado lo puede intentar romper todo el mundo.'),
 dict(p=u'&iquest;Cu&aacute;l es la diferencia entre una <i>cookie</i> y la huella digital del navegador?',
      op=[u'ninguna: son dos nombres para lo mismo',
          u'la cookie te la ponen dentro y se puede borrar; la huella es c&oacute;mo es tu aparato, y no se borra',
          u'la huella la pones t&uacute; y la cookie la pone la web'],
      ok=1,
      por=u'Una es una <b>pegatina</b> que te pegan y puedes quitar; la otra es <b>reconocerte por la '
          u'cara</b>: la combinaci&oacute;n de pantalla, idioma, zona horaria y dem&aacute;s. Por eso '
          u'borrar las cookies o abrir una ventana de inc&oacute;gnito no cambia la huella.'),
 dict(p=u'Partiendo de ocho min&uacute;sculas, &iquest;qu&eacute; sube m&aacute;s el mont&oacute;n de combinaciones?',
      op=[u'llenarla de may&uacute;sculas, n&uacute;meros y signos (&times;29.190)',
          u'a&ntilde;adirle cuatro letras min&uacute;sculas m&aacute;s (&times;456.976)',
          u'las dos cosas suben lo mismo'],
      ok=1,
      por=u'Porque <b>cada carácter nuevo multiplica</b> por el alfabeto entero, mientras que hacerla '
          u'rara <b>agranda el alfabeto una sola vez</b>. Las cuatro letras ganan por quince veces, y '
          u'encima te las acuerdas, que es lo que hace que no acabes repiti&eacute;ndola.'),
 dict(p=u'Una web bien hecha, cuando te registras, guarda&hellip;',
      op=[u'tu contrase&ntilde;a, cifrada con la clave de la empresa',
          u'tu contrase&ntilde;a tal cual, pero en un servidor muy protegido',
          u'la <b>huella</b> de tu contrase&ntilde;a (con una sal delante), que no se puede deshacer'],
      ok=2,
      por=u'Por eso una web bien hecha <b>no sabe</b> cu&aacute;l es tu contrase&ntilde;a: compara '
          u'huellas. Y de ah&iacute; sale una se&ntilde;al que puedes usar: si al olvidarla te la '
          u'mandan <b>tal cual</b> por correo, es que la ten&iacute;an guardada en claro.'),
 dict(p=u'Tienes la carpeta sincronizada con la nube y borras un trabajo sin querer. &iquest;Est&aacute; a salvo?',
      op=[u's&iacute;, porque la nube es una copia de seguridad',
          u'no: lo sincronizado copia el borrado, y en segundos',
          u's&iacute;, porque la nube guarda todo para siempre'],
      ok=1,
      por=u'Sincronizar es <b>tener siempre lo mismo</b> en dos sitios: para eso est&aacute; hecho, y lo '
          u'hace tambi&eacute;n con los desastres. Te salva de que se rompa el aparato, no de que te '
          u'equivoques t&uacute;. Una copia de seguridad es otra cosa: <b>c&oacute;mo estaban las cosas '
          u'antes</b>, guardado aparte y sin cambiar.'),
 dict(p=u'En la regla 3-2-1, &iquest;para qu&eacute; sirve el <b>1</b> (una copia fuera de casa)?',
      op=[u'para poder llegar a ella desde el m&oacute;vil',
          u'para que sea m&aacute;s barata',
          u'para el desastre que se lleva un sitio entero: fuego, agua o robo'],
      ok=2,
      por=u'Cada n&uacute;mero mata un desastre distinto. Tres copias en el mismo caj&oacute;n son, '
          u'ante un incendio, <b>una sola copia</b>. Por eso una tiene que estar en otro sitio '
          u'f&iacute;sico.'),
 dict(p=u'Pides a una empresa que te ense&ntilde;e los datos que tiene tuyos. &iquest;Qu&eacute; te ampara?',
      op=[u'nada: es un favor, y pueden no contestarte',
          u'el derecho de acceso, gratis, y tienen un mes para contestar (dos m&aacute;s si avisan)',
          u'solo puedes pedirlo con un abogado y pagando una tasa'],
      ok=1,
      por=u'No es un favor: es un <b>derecho</b> con art&iacute;culo (RGPD, art. 15), <b>plazo</b> (un '
          u'mes, prorrogable otros dos avisando) y <b>&aacute;rbitro</b> (la Agencia Espa&ntilde;ola de '
          u'Protecci&oacute;n de Datos, a la que se reclama gratis). Y en Espa&ntilde;a, desde los '
          u'<b>14 a&ntilde;os</b>, lo ejerces t&uacute; solo.'),
]


S6 = (
  bloque('00', u'Reto inicial &middot; 10 min', u'''
      <p>Cinco sesiones mirando c&oacute;mo funciona esto por dentro, y en las cinco ha decidido
         <b>otro</b>: qu&eacute; se recoge, d&oacute;nde se guarda, cu&aacute;nto dura. Hoy va de lo
         contrario.</p>

      <div class="aviso">
        <span class="n-tag">El encargo</span>
        Hace dos a&ntilde;os te hiciste una cuenta en una aplicaci&oacute;n que ya no usas. Siguen
        teniendo tus datos ah&iacute; dentro. <b>Escribe el mensaje que les mandar&iacute;as</b> para
        que lo borren todo. Cinco l&iacute;neas, como si lo fueras a enviar. Cinco minutos.
      </div>

      <p>Ahora leed tres en voz alta. Van a parecerse much&iacute;simo, y casi todos empiezan igual:
         <i>&laquo;Hola, buenas, quer&iacute;a preguntar si ser&iacute;a posible que&hellip;&raquo;</i>.
         Es un mensaje educado, razonable y <b>completamente in&uacute;til</b>. Vamos a ver por
         qu&eacute;, porque el motivo no es c&oacute;mo est&aacute; escrito.</p>

      <div class="reto-piensa">
        <span class="n-tag">Las tres preguntas que lo hunden</span>
        <p><b>1.</b> Est&aacute;s pidiendo un <b>favor</b>. &iquest;Qu&eacute; pasa si te dicen que
           no? &iquest;Y si no te contestan?</p>
        <p><b>2.</b> &iquest;<b>Cu&aacute;ndo</b> te tienen que contestar? Si no pones fecha, no hay
           fecha, y &laquo;ya lo miraremos&raquo; puede durar tres a&ntilde;os.</p>
        <p><b>3.</b> Si pasan de ti, <b>&iquest;a qui&eacute;n se lo cuentas?</b> &iquest;Hay alguien
           por encima de ellos?</p>
      </div>

      <p>Las tres respuestas, con un mensaje as&iacute;, son la misma: <b>nada, nunca y a nadie</b>. Y
         ah&iacute; est&aacute; el fallo, que no es de educaci&oacute;n ni de redacci&oacute;n: es que
         has pedido <b>un favor</b> cuando ten&iacute;as en la mano <b>un derecho</b>.</p>

      <p>La diferencia no es una manera de hablar. Un derecho trae tres cosas que un favor no trae
         nunca: un <b>nombre y un art&iacute;culo</b>, un <b>plazo</b> y un <b>&aacute;rbitro</b> al que
         acudir cuando no te hacen caso. Con esas tres, el mismo mensaje pasa de s&uacute;plica a
         obligaci&oacute;n. Vamos a por ellas.</p>
  ''') +

  bloque('01', u'Teor&iacute;a &middot; 20 min', u'''
      <h3>Estos derechos existen y tienen n&uacute;mero</h3>
      <p>En la sesi&oacute;n de los datos apareci&oacute; de pasada una ley, el <b>Reglamento General de
         Protecci&oacute;n de Datos</b> &mdash;europeo, de 2016, en vigor desde el 25 de mayo de
         2018&mdash;. All&iacute; sirvi&oacute; para explicar de d&oacute;nde salen los avisos de
         cookies. Hoy la vamos a usar para otra cosa: para <b>pedir</b>.</p>
      <p>Elige un derecho abajo, pon la fecha de hoy y mira el calendario. Despu&eacute;s cambia la
         fecha de env&iacute;o a un <b>31 de enero</b> y fíjate en lo que hace el plazo.</p>

''' + ESCENA_DERECHOS + u'''
      <div class="copiar">
        <h4>Los cuatro que m&aacute;s vas a usar</h4>
        <table>
          <tr><th>Derecho</th><th>Qu&eacute; puedes exigir</th></tr>
          <tr><td><b>Acceso</b><br><span style="font-size:12.5px">RGPD, art. 15</span></td>
              <td>Que te ense&ntilde;en <b>todo</b> lo que tienen tuyo, de d&oacute;nde lo sacaron, para
                  qu&eacute; lo usan y a qui&eacute;n se lo dan. Con copia, no con un resumen.</td></tr>
          <tr><td><b>Rectificaci&oacute;n</b><br><span style="font-size:12.5px">art. 16</span></td>
              <td>Que <b>arreglen</b> lo que tengan mal. Es el m&aacute;s f&aacute;cil de ganar: un dato
                  equivocado no lo defiende nadie.</td></tr>
          <tr><td><b>Supresi&oacute;n</b><br><span style="font-size:12.5px">art. 17</span></td>
              <td>Que lo <b>borren</b>. Es el que la prensa llama &laquo;derecho al olvido&raquo;. No
                  siempre gana &mdash;a veces una ley les obliga a guardarlo&mdash;, pero
                  <b>te tienen que decir por qu&eacute;</b>.</td></tr>
          <tr><td><b>Portabilidad</b><br><span style="font-size:12.5px">art. 20</span></td>
              <td>Que te den lo tuyo en un <b>archivo que puedas abrir</b>, para llev&aacute;rtelo a
                  otro sitio. Es el que impide que una aplicaci&oacute;n te tenga atrapado por guardar
                  dentro tus a&ntilde;os de fotos.</td></tr>
        </table>
        <p>Hay dos m&aacute;s que conviene saber que existen: <b>oposici&oacute;n</b> (que dejen de
           usarlos para algo, t&iacute;picamente publicidad) y <b>limitaci&oacute;n</b> (que los
           congelen mientras se discute si son correctos).</p>
      </div>

      <div class="copiar">
        <h4>El plazo y el &aacute;rbitro</h4>
        <ul>
          <li>Ejercerlos es <b>gratis</b>, y se pide <b>directamente a la empresa</b>: no hace falta
              abogado ni papel del juzgado.</li>
          <li>Tienen <b>un mes</b> para contestar. Pueden alargarlo <b>otros dos</b> si la cosa es
              complicada, pero <b>te lo tienen que avisar dentro del primer mes</b> y decirte por
              qu&eacute;.</li>
          <li>Si no contestan, o si contestan que no y no te convence, se <b>reclama a la Agencia
              Espa&ntilde;ola de Protecci&oacute;n de Datos</b>. Tambi&eacute;n gratis.</li>
        </ul>
        <p>Y ojo con el mes, que no son treinta d&iacute;as: es <b>hasta el mismo n&uacute;mero del mes
           siguiente</b>, y cuando ese n&uacute;mero no existe se recorta. Un 31 de enero m&aacute;s un
           mes es el <b>28 de febrero</b>. Pru&eacute;balo en la escena.</p>
      </div>

      <div class="copiar">
        <h4>La edad para decidir t&uacute; solo</h4>
        <p>En <b>Espa&ntilde;a</b>, a partir de los <b>14 a&ntilde;os</b> puedes dar t&uacute; solo tu
           permiso para que traten tus datos &mdash;y retirarlo t&uacute; solo&mdash;. Lo dice la
           <b>Ley Org&aacute;nica 3/2018, art&iacute;culo 7</b>.</p>
        <p>Por debajo de esa edad, el permiso lo dan tus padres o tutores. Que no es lo mismo que &laquo;no
           puedes usar nada&raquo;: es que <b>el permiso que vale no es el tuyo</b>.</p>
        <p>El reglamento europeo pone <b>16</b> por defecto y deja que cada pa&iacute;s lo baje
           <b>hasta 13</b>. Por eso la edad <b>cambia seg&uacute;n el pa&iacute;s</b>, y por eso no
           sirve de nada lo que hayas o&iacute;do de una aplicaci&oacute;n americana.</p>
      </div>

      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; no hace falta copiarlo</span>
        <p>Que la edad la eligiera cada pa&iacute;s no fue un descuido: fue la &uacute;nica manera de
           que la ley saliera adelante. Los pa&iacute;ses de la Uni&oacute;n ten&iacute;an ya su idea de a
           qu&eacute; edad un adolescente decide sobre lo suyo, y esa idea viene de cada sitio, no de la
           tecnolog&iacute;a. As&iacute; que el reglamento puso un n&uacute;mero por defecto y dej&oacute;
           una horquilla. Espa&ntilde;a eligi&oacute; catorce.</p>
        <p>Y vale la pena fijarse en otra cosa: la edad que se puso aqu&iacute; est&aacute; <b>por debajo
           de la mayor&iacute;a de edad</b>, y no es un despiste. Es que lo que se protege son
           <b>tus</b> datos, y dejar que decidan siempre otros por ti tampoco te protege: te deja
           fuera. Catorce es el punto donde se decidi&oacute; que ya sabes bastante como para
           decidir, y eso incluye poder decir que <b>no</b>.</p>
      </div>

      <h3>Y si te pasa algo</h3>
      <p>Hasta aqu&iacute; hemos hablado de empresas. Pero la mayor&iacute;a de los l&iacute;os no vienen
         de una empresa: vienen de que alguien ha publicado una foto tuya, se ha hecho pasar por ti o
         est&aacute; presionando a alguien con algo que tiene. Para eso hay un camino, y conviene
         sab&eacute;rselo <b>antes</b>, porque el d&iacute;a que pasa no se piensa bien.</p>

      <div class="copiar">
        <h4>Qu&eacute; se hace, y en este orden</h4>
        <ol>
          <li><b>No contestes y no borres nada tuyo.</b> Contestar alimenta; borrar tus propios
              mensajes te quita las pruebas.</li>
          <li><b>Guarda pruebas.</b> Capturas donde se vea la <b>fecha</b>, el <b>nombre de usuario</b>
              y la <b>direcci&oacute;n de la p&aacute;gina</b>. Sin eso, luego no hay nada que
              ense&ntilde;ar.</li>
          <li><b>Cu&eacute;ntaselo a alguien.</b> Un adulto de tu casa o del instituto. Esto no se lleva
              solo, y no por debilidad: porque <b>hace falta alguien que pueda actuar</b>.</li>
          <li><b>Denuncia dentro de la propia aplicaci&oacute;n.</b> Todas tienen bot&oacute;n, y suele
              ser lo m&aacute;s r&aacute;pido de todo.</li>
          <li><b>Llama al 017.</b> Es la l&iacute;nea de ayuda en ciberseguridad del <b>INCIBE</b>,
              organismo p&uacute;blico. <b>Gratuita y confidencial</b>, todos los d&iacute;as de 8:00 a
              23:00. No hay que haber hecho nada mal para llamar.</li>
          <li>Si lo que circula es una <b>foto o un v&iacute;deo de contenido sexual o violento</b>, la
              AEPD tiene un <b>canal prioritario</b> para pedir que se retire con urgencia, sin esperar
              plazos. Y si hay delito, se denuncia a la <b>polic&iacute;a o a la guardia civil</b>.</li>
        </ol>
        <p>Una cosa m&aacute;s, y va en serio: si te han enga&ntilde;ado, <b>la culpa no es tuya</b>.
           Enga&ntilde;an a gente mayor que t&uacute; y con m&aacute;s oficio. Callarse por
           verg&uuml;enza es exactamente lo que espera quien te ha enga&ntilde;ado.</p>
      </div>

''' + foto('u8-aepd.jpg',
           u'Puerta de madera oscura de un edificio con una placa blanca al lado que dice Agencia Espa&ntilde;ola de Protecci&oacute;n de Datos',
           u'Esta puerta est&aacute; en la calle Jorge Juan de Madrid, y detr&aacute;s hay gente '
           u'cobrando un sueldo p&uacute;blico por <b>hacer cumplir</b> lo que has copiado hoy. Se le '
           u'reclama por Internet y <b>gratis</b>. Merece la pena verla: un derecho suena a cosa de '
           u'papel hasta que descubres que tiene <b>portal, timbre y horario</b>.',
           u'Zarateman', u'CC0',
           u'https://commons.wikimedia.org/wiki/File:Madrid_-_Calle_de_Jorge_Juan,_Agencia_Espa%C3%B1ola_de_Protecci%C3%B3n_de_Datos.jpg') +
  video('video-derechos', 'p3nATAVU6kM',
        u'Cu&aacute;les son tus derechos de protecci&oacute;n de datos personales',
        u'Agencia Espa&ntilde;ola de Protecci&oacute;n de Datos &middot; en espa&ntilde;ol',
        u'Los mismos derechos contados por el organismo que se encarga de hacerlos cumplir.')) +

  bloque('02', u'Pr&aacute;ctica &middot; 15 min', ficha(
    u'Actividad 8.6 &middot; El mismo mensaje, pero que sirva',
    [u'6.3'], u'Individual &middot; 15 min &middot; sobre 10', u'''
          <h4>Qu&eacute; hay que hacer</h4>
          <ol class="pasos">
            <li><b>Vuelve a escribirlo.</b> Coge el mensaje del principio de la sesi&oacute;n y
                reescr&iacute;belo como una <b>solicitud</b>. Tiene que llevar, s&iacute; o s&iacute;,
                estas seis cosas:
                <ul>
                  <li>a qui&eacute;n va dirigido y qui&eacute;n eres (nombre y el correo de la cuenta);</li>
                  <li><b>qu&eacute; derecho</b> ejerces, por su nombre y su art&iacute;culo;</li>
                  <li><b>qu&eacute; pides exactamente</b>, sin rodeos;</li>
                  <li>el <b>plazo</b> que tienen, dicho por ti;</li>
                  <li>que si no contestan <b>reclamar&aacute;s a la AEPD</b>;</li>
                  <li>la <b>fecha</b> y c&oacute;mo quieres que te respondan.</li>
                </ul>
                Nada de &laquo;ser&iacute;a posible&raquo; ni de &laquo;por favor&raquo; suplicando.
                Educado s&iacute;; pidiendo favores, no.</li>
            <li><b>Las fechas, calculadas.</b> Pon la de hoy en la escena y anota las <b>dos</b>
                fechas l&iacute;mite (la normal y la de pr&oacute;rroga) con sus d&iacute;as.
                C&oacute;pialas en tu solicitud.</li>
            <li><b>La trampa del calendario.</b> Cambia la fecha de env&iacute;o al <b>31 de enero</b>
                y anota a qu&eacute; d&iacute;a cae el mes. Explica en una frase <b>por qu&eacute;</b>
                no es el 31 de febrero.</li>
            <li><b>Elige bien el derecho.</b> Para cada caso, di cu&aacute;l de los cuatro pedir&iacute;as
                y por qu&eacute;: <b>(a)</b> una tienda tiene mal tu apellido; <b>(b)</b> quieres saber
                qu&eacute; sabe de ti una red social; <b>(c)</b> te cambias de aplicaci&oacute;n de
                m&uacute;sica y quieres llevarte tus listas; <b>(d)</b> quieres que un foro borre tu
                cuenta de hace tres a&ntilde;os.</li>
            <li><b>Tu edad.</b> Pon tu fecha de nacimiento en la escena y anota si <b>hoy</b> puedes
                ejercerlos t&uacute; solo o no. Si todav&iacute;a no, anota <b>qu&eacute; d&iacute;a</b>
                podr&aacute;s y qui&eacute;n lo hace mientras tanto.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>La solicitud lleva las <b>seis</b> cosas <b>(3 puntos)</b>.</li>
            <li>Nombra el derecho <b>con su art&iacute;culo</b> y pide algo concreto <b>(2 puntos)</b>.</li>
            <li>Las dos fechas l&iacute;mite est&aacute;n bien <b>(2 puntos)</b>.</li>
            <li>Los cuatro casos est&aacute;n bien asignados y razonados <b>(2 puntos)</b>.</li>
            <li>La explicaci&oacute;n del 31 de enero es correcta <b>(1 punto)</b>.</li>
          </ul>
          <div class="nota" style="margin-top:14px">
            <span class="n-tag">Esto no es un ejercicio de mentira</span>
            La solicitud que escribas hoy <b>sirve tal cual</b>. Si alguna vez quieres mandarla de
            verdad, la AEPD tiene modelos en su web y se env&iacute;a por el formulario de contacto de
            la propia empresa. Gu&aacute;rdate siempre <b>copia y fecha</b> de lo que mandas: sin eso no
            se puede reclamar despu&eacute;s.
          </div>
  ''')) +

  bloque('03', u'Test &middot; 10 min', u'''
      <p>Diez preguntas de <b>toda la unidad</b>, no solo de hoy. Se corrigen aqu&iacute; mismo y cada
         una explica por qu&eacute; &mdash;tambi&eacute;n las que aciertes&mdash;. No cuenta para nota:
         es para que sepas por d&oacute;nde andas antes del examen.</p>
''' + test('u8', u'Lo que tiene que haber quedado de la unidad', PREGUNTAS_U8)) +

  bloque('04', u'Cierre &middot; 5 min', u'''
      <p>Con esto se cierra la unidad. Si te quedas con cuatro frases, que sean estas:</p>
      <div class="copiar">
        <h4>La unidad en cuatro frases</h4>
        <ol>
          <li>Internet no manda las cosas enteras: las manda en <b>trozos numerados</b> que comparten
              cables con los de todo el mundo y se recomponen al llegar.</li>
          <li>El <b>candado</b> protege lo que dices por el camino; no protege <b>a d&oacute;nde vas</b>,
              ni los extremos, ni te dice si la web es honrada.</li>
          <li>Casi todo lo que saben de ti <b>se lo damos nosotros</b> al usar, o lo cuenta el aparato
              solo. Y lo que guardas <b>est&aacute; en el ordenador de otro</b>.</li>
          <li>Lo que te protege no es tener miedo: es que la contrase&ntilde;a sea <b>larga</b>, que
              haya una <b>copia aparte</b> y que sepas que puedes <b>exigir</b>, gratis y con plazo.</li>
        </ol>
      </div>

      <div class="nota">
        <span class="n-tag">Por qu&eacute; hemos estudiado esto as&iacute;</span>
        En seis sesiones no ha aparecido ni una vez la frase &laquo;Internet es peligroso&raquo;, y no
        es un olvido. Quien tiene miedo no decide: obedece, y hace lo que le digan el &uacute;ltimo
        v&iacute;deo que ha visto o el primero que le llame por tel&eacute;fono. <b>Quien entiende
        c&oacute;mo funciona, decide.</b> Eso es lo que ten&iacute;a que quedar.
      </div>

      <div class="nota">
        <span class="n-tag">Siguiente unidad</span>
        En toda esta unidad has sido quien <b>mira</b>: quien pide un v&iacute;deo, quien se conecta,
        quien deja rastro. La unidad siguiente le da la vuelta y te pone del otro lado, el de quien
        <b>publica</b>: c&oacute;mo se produce y se difunde algo propio con estas herramientas. Y
        ah&iacute; se cierra el c&iacute;rculo que abriste en la unidad de representaci&oacute;n
        gr&aacute;fica, cuando aprendiste a explicar con un plano lo que hab&iacute;as hecho. Era la
        misma pregunta: <b>c&oacute;mo cuentas a otro lo tuyo</b>. Primero a mano; ahora, con todo esto
        detr&aacute;s.
      </div>
  '''))


# ==========================================================================
S = [
  dict(corto=u'C&oacute;mo llega un v&iacute;deo',
       titulo=u'C&oacute;mo llega un v&iacute;deo a tu m&oacute;vil',
       entradilla=u'Reservar un camino de punta a punta no cabe en la aritm&eacute;tica. La salida fue '
                  u'partirlo todo en trozos numerados y dejar que cada uno se busque la vida.',
       minutado=[(u"10'", u'Reto'), (u"20'", u'Teor&iacute;a'), (u"25'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')],
       chips=[u'CE6 &middot; 6.1', u'D.1&ndash;D.4'],
       cuerpo=S1),
  dict(corto=u'Qui&eacute;n ve lo que mandas',
       titulo=u'Qui&eacute;n ve lo que mandas: el candado por dentro',
       entradilla=u'Tus paquetes pasan por diez m&aacute;quinas que no son tuyas. De ah&iacute; sali&oacute; la '
                  u'necesidad de cifrar, y de ah&iacute; sale lo que el candado protege &mdash;y lo que no&mdash;.',
       minutado=[(u"10'", u'Reto'), (u"20'", u'Teor&iacute;a'), (u"25'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')],
       chips=[u'CE6 &middot; 6.1', u'CE6 &middot; 6.2', u'D.2'],
       cuerpo=S2),
  dict(corto=u'Tus datos valen dinero',
       titulo=u'Tus datos valen dinero: qu&eacute; se recoge y a cambio de qu&eacute;',
       entradilla=u'Si nadie puede leer lo que mandas, &iquest;de d&oacute;nde sale lo que saben? De lo que '
                  u'entregamos al usar, y de que el aparato se identifica solo. Con la cuenta delante.',
       minutado=[(u"10'", u'Reto'), (u"20'", u'Teor&iacute;a'), (u"25'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')],
       chips=[u'CE6 &middot; 6.3', u'D.3 &middot; D.4'],
       cuerpo=S3),
  dict(corto=u'Contrase&ntilde;as',
       titulo=u'La contrase&ntilde;a: por qu&eacute; la larga gana a la rara',
       entradilla=u'La receta de siempre &mdash;may&uacute;sculas, n&uacute;meros y un signo raro&mdash; '
                  u'pierde contra una frase f&aacute;cil de recordar. Y se demuestra con una '
                  u'multiplicaci&oacute;n.',
       minutado=[(u"10'", u'Reto'), (u"20'", u'Teor&iacute;a'), (u"25'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')],
       chips=[u'CE6 &middot; 6.2', u'CE6 &middot; 6.3', u'D.2 &middot; D.3'],
       cuerpo=S4),
  dict(corto=u'La nube',
       titulo=u'La nube: el ordenador de otro',
       entradilla=u'Esa foto est&aacute; en un edificio con direcci&oacute;n, due&ntilde;o y factura de '
                  u'la luz. Qu&eacute; se gana, qu&eacute; se suelta, y por qu&eacute; sincronizar no '
                  u'es tener una copia.',
       minutado=[(u"10'", u'Reto'), (u"20'", u'Teor&iacute;a'), (u"25'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')],
       chips=[u'CE6 &middot; 6.1', u'CE6 &middot; 6.3', u'D.1 &middot; D.4'],
       cuerpo=S5),
  dict(corto=u'Tus derechos',
       titulo=u'Tus derechos: lo que puedes exigir, y c&oacute;mo',
       entradilla=u'Un favor se puede negar; un derecho trae art&iacute;culo, plazo y &aacute;rbitro. '
                  u'Los cuatro que vas a usar, la edad a la que decides t&uacute; y el test que cierra '
                  u'la unidad.',
       minutado=[(u"10'", u'Reto'), (u"20'", u'Teor&iacute;a'), (u"15'", u'Pr&aacute;ctica'),
                 (u"10'", u'Test'), (u"5'", u'Cierre')],
       chips=[u'CE6 &middot; 6.3', u'D.3 &middot; D.4'],
       cuerpo=S6),
]

CFG = dict(
 ruta='2eso/TyD/tema8/',
 migas=u'<a href="../../../">Materiales</a> &middot; <a href="../../">2.&ordm; ESO</a> '
       u'&middot; <a href="../">TyD</a> &middot; Tema 8',
 h1=u'Internet, datos y seguridad',
 titulo=u'Tema 8 &middot; Internet, datos y seguridad',
 tema=u'Tema 8', curso=u'2.&ordm; de ESO', materia=u'Tecnolog&iacute;a y Digitalizaci&oacute;n',
 desc=u'Tema 8 de Tecnolog&iacute;a y Digitalizaci&oacute;n de 2.&ordm; de ESO: paquetes, direcciones IP, '
      u'routers y DNS; http frente a https y qu&eacute; protege el candado; huella digital, cookies y '
      u'permisos de las aplicaciones.',
 sesiones=S)


# Dos anadidos al molde: el CSS del avatar (que vive en avatar_flat, no en
# tema0_base) y el de las tablas dentro de los bloques que se copian.
EXTRA_CSS = avatar_flat.CSS + u"""
/* tablas de datos dentro de los bloques que se copian */
.copiar table{border-collapse:collapse;width:100%;margin:10px 0 4px;font-size:14.5px}
.copiar th,.copiar td{border:1px solid var(--line);padding:6px 9px;text-align:left}
.copiar th{background:var(--surface-2);font-family:var(--f-m);font-size:11.5px;
  letter-spacing:.06em;text-transform:uppercase;color:var(--ink-soft);font-weight:500}
.copiar td:first-child{width:52%}
@media (max-width:560px){.copiar table{font-size:13px}.copiar th,.copiar td{padding:5px 6px}}
/* listas dentro de una lista de pasos: que no se peguen al texto de arriba */
.pasos ul{margin:6px 0 2px}
"""

if __name__ == '__main__':
    html = pagina(CFG).replace(u'</style>', EXTRA_CSS + u'</style>', 1)
    destino = os.path.join(RAIZ, '2eso', 'TyD', 'tema8')
    os.makedirs(destino, exist_ok=True)
    io.open(os.path.join(destino, 'index.html'), 'w', encoding='utf-8', newline='').write(html)
    print('U8 generada: %d bytes, %d sesiones (%d escritas)' % (
        len(html), len(S), sum(1 for x in S if not x.get('pendiente'))))
