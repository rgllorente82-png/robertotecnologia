# -*- coding: utf-8 -*-
"""2.o TyD · U8 (web) · Internet, datos y seguridad.

Sesiones 1, 2 y 3 escritas; 4, 5 y 6 marcadas como pendientes.
Las escenas interactivas viven en u8_escenas.py.

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
import avatar_flat
from u8_escenas import (ESCENA_RUTA, ESCENA_DNS, ESCENA_ESPIA, ESCENA_CLAVE,
                        ESCENA_HUELLA)

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
  dict(corto=u'Contrase&ntilde;as', pendiente=True),
  dict(corto=u'La nube', pendiente=True),
  dict(corto=u'Tus derechos', pendiente=True),
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
