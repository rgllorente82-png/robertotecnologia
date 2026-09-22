# -*- coding: utf-8 -*-
"""2.o TyD · U7 · El ordenador y sus componentes.

Las seis sesiones, escritas. Las escenas interactivas viven aparte:
u7_escenas.py las de las sesiones 1 a 3 y u7_escenas2.py las de las 4 a 6.

    python generadores/u7_build.py

Escribe 2eso/TyD/tema9/index.html relativo a la raiz del repo (el padre de
generadores/), no a una ruta absoluta: asi corre igual en el portatil y aqui.
"""
import io, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unidad_base import pagina, bloque, ficha, pregunta
from test_auto import test
import avatar_flat
from u7_escenas import ESCENA_CPU, ESCENA_RAM, ESCENA_BITS
from u7_escenas2 import ESCENA_ADC, ESCENA_PLAN, ESCENA_DIAG

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


ENV = json.load(io.open(os.path.join(RAIZ, '_env_u7-ordenador.json'), encoding='utf-8'))
NARRADOR = avatar_flat.componente(
    'narr-u7', u'De d&oacute;nde sale esta unidad',
    u'Por qu&eacute; un cable no basta y hubo que inventar la m&aacute;quina que obedece listas',
    '../../../audio/u7-ordenador.mp3', ENV,
    u'Voz sintetizada sobre gui&oacute;n propio. La boca sigue el volumen real de la voz: se mueve '
    u'cuando habla y se para en los silencios.')


# ==========================================================================
# SESION 1 · Una maquina que no sabe hacer nada
# ==========================================================================
S1 = (
  bloque('00', u'Reto inicial &middot; 10 min', u'''
      <p>En la unidad de electricidad lo dejaste montado: una pila, un interruptor y una bombilla.
         Pulsas, se enciende. Sueltas, se apaga. Funciona, y funciona siempre igual.</p>

''' + NARRADOR + u'''
      <div class="aviso">
        <span class="n-tag">El encargo</span>
        Coge ese circuito y haz que la bombilla <b>parpadee dos veces</b> cuando pulsas,
        <b>tres veces</b> si mantienes el dedo, y que adem&aacute;s <b>lleve la cuenta</b> de cu&aacute;ntas
        veces la has encendido hoy. Dib&uacute;jalo.
      </div>

      <p>Int&eacute;ntalo de verdad durante cinco minutos, con lo que sabes de electricidad. Vais a llegar
         todos al mismo sitio, y conviene llegar para verlo:</p>
      <ul>
        <li>Para el parpadeo hace falta <b>otro montaje</b>: algo que corte y devuelva la corriente solo.</li>
        <li>Para distinguir el toque del dedo mantenido, <b>otro m&aacute;s</b>.</li>
        <li>Para contar, <b>otro</b>.</li>
        <li>Y ma&ntilde;ana, cuando te pida una cosa distinta, <b>vuelta a empezar con el soldador</b>.</li>
      </ul>

      <div class="reto-piensa">
        <span class="n-tag">La pregunta que abre el tema</span>
        <p>Si cada comportamiento nuevo obliga a un circuito nuevo, <b>&iquest;cu&aacute;ntos circuitos
           distintos habr&iacute;a que fabricar</b> para que una sola m&aacute;quina pudiera hacer todo lo que
           hace un m&oacute;vil?</p>
      </div>

      <p>La respuesta es que no hay n&uacute;mero: son infinitos, porque cada d&iacute;a se inventa un
         comportamiento nuevo. Por ese camino no se llega. Hac&iacute;a falta otra idea, y cost&oacute; siglo y medio
         encontrarla.</p>
  ''') +
  bloque('01', u'Teor&iacute;a &middot; 20 min', u'''
      <h3>La idea: una m&aacute;quina que no sepa hacer nada en concreto</h3>
      <p>Si el problema es que el comportamiento est&aacute; <b>en los cables</b>, la salida es sacarlo de
         ah&iacute;. Se construye <b>una sola m&aacute;quina</b>, siempre la misma, que por s&iacute; sola no hace nada
         interesante: solo sabe leer una lista de &oacute;rdenes muy simples y obedecerlas una detr&aacute;s de otra.
         El comportamiento ya no est&aacute; soldado: est&aacute; <b>escrito</b>, y lo escrito se cambia en un segundo.</p>

      <p>Prueba la m&aacute;quina de abajo. Tiene seis &oacute;rdenes y nada m&aacute;s. Cambia de programa arriba y
         fíjate en <b>qu&eacute; cambia del dibujo</b>: la respuesta es que nada del procesador, solo la lista.</p>

''' + ESCENA_CPU + u'''
      <div class="copiar">
        <h4>Las dos mitades de un ordenador</h4>
        <p><b>Hardware</b>: todo lo que se puede tocar. La placa, los chips, los cables, la pantalla.
           Si falla, se cambia la pieza.</p>
        <p><b>Software</b>: las instrucciones. No se toca, no pesa y no se gasta. Si falla, se corrige
           y se vuelve a cargar.</p>
        <p>Un ordenador es <b>una m&aacute;quina de prop&oacute;sito general</b>: no est&aacute; hecha para una tarea,
           sino para ejecutar cualquier lista de instrucciones que le des.</p>
      </div>

      <h3>Qui&eacute;n obedece la lista: la CPU</h3>
      <p>La pieza que lee la lista y la obedece es el <b>procesador</b>. No es un cerebro y no decide
         nada: hace tres cosas, en este orden, y vuelve a empezar. Sin parar, mientras tenga corriente.</p>

      <div class="copiar">
        <h4>La CPU y su ciclo</h4>
        <p><b>CPU</b> (<i>unidad central de proceso</i>): el componente que ejecuta las instrucciones
           del programa.</p>
        <p>Repite siempre el mismo <b>ciclo de tres pasos</b>:</p>
        <ol>
          <li><b>Busca</b> en la memoria la instrucci&oacute;n que toca.</li>
          <li>La <b>descodifica</b>: averigua qu&eacute; orden es y qu&eacute; hay que hacer.</li>
          <li>La <b>ejecuta</b>, y anota cu&aacute;l es la siguiente.</li>
        </ol>
        <p>El <b>reloj</b> marca el ritmo de ese ciclo. Una CPU de <b>3 GHz</b> recibe
           <b>3.000 millones de pulsos de reloj por segundo</b>.</p>
      </div>

      <div class="nota">
        <span class="n-tag">Ojo con una frase que se oye mucho</span>
        &laquo;3 GHz son 3.000 millones de instrucciones por segundo&raquo; <b>no es cierto</b>. Son
        3.000 millones de <i>pulsos de reloj</i>. Hay instrucciones que gastan varios pulsos y CPU
        modernas que resuelven varias a la vez. Los gigahercios miden el <b>ritmo</b>, no el trabajo.
      </div>

''' + foto('u7-eniac.jpg',
           u'Dos personas trabajando junto al ENIAC en 1947, con paneles llenos de cables conectados a mano',
           u'El <b>ENIAC</b>, hacia 1947. Mira los paneles de la izquierda: esa mara&ntilde;a de cables <b>es</b> '
           u'el programa. Cambiarlo significaba desenchufar y volver a enchufar a mano, y eso llevaba '
           u'd&iacute;as. Exactamente el problema del reto de hoy, pero ocupando la sala entera que ves.',
           u'Autor desconocido (US Army)', u'Dominio p&uacute;blico',
           u'https://commons.wikimedia.org/wiki/File:Glen_Beck_and_Betty_Snyder_program_the_ENIAC_in_building_328_at_the_Ballistic_Research_Laboratory.jpg') + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; no hace falta copiarlo</span>
        <p>La idea de sacar las instrucciones fuera de la m&aacute;quina no naci&oacute; en la inform&aacute;tica: naci&oacute;
           <b>tejiendo</b>. Hacia 1805 Joseph Marie Jacquard mont&oacute; un telar que le&iacute;a <b>tarjetas
           perforadas</b>: el dibujo de la tela no estaba en el telar, estaba en las tarjetas. Cambiabas
           las tarjetas y el mismo telar tej&iacute;a otra cosa.</p>
        <p>En 1945 el ENIAC ya calculaba, pero se programaba recableando. La alternativa que gan&oacute; la
           escribi&oacute; ese mismo a&ntilde;o <b>John von Neumann</b> en un informe sobre la m&aacute;quina siguiente,
           el EDVAC: guardar el programa <b>en la misma memoria que los datos</b>. Si el programa es un
           n&uacute;mero m&aacute;s, se carga y se cambia igual de r&aacute;pido que un n&uacute;mero.</p>
        <p>La primera m&aacute;quina que lo hizo de verdad ech&oacute; a andar en Manchester el <b>21 de junio de
           1948</b>. Casi todo lo que hoy llamamos ordenador sigue ese mismo esquema, ochenta a&ntilde;os
           despu&eacute;s.</p>
      </div>

''' + foto('ri3-intel4004.jpg',
           u'Microprocesador Intel 4004 de 1971 visto de cerca sobre fondo blanco',
           u'El <b>Intel 4004</b>, 1971: la primera vez que una CPU entera cupo en una sola pastilla. '
           u'Llevaba unos <b>2.300 transistores</b>. Un procesador de m&oacute;vil de hoy lleva <b>decenas de '
           u'miles de millones</b>, y hace exactamente lo mismo que este: buscar, descodificar, ejecutar.',
           u'Thomas Nguyen', u'CC BY-SA 4.0',
           u'https://commons.wikimedia.org/wiki/File:Intel%20C4004.jpg') +
  video('video-cpu', '-ZTekGoR8uQ',
        u'&iquest;C&oacute;mo funciona un procesador? Desde un transistor hasta una CPU',
        u'Hardware 360&ordm; &middot; en espa&ntilde;ol',
        u'Para ver qu&eacute; hay debajo del ciclo de tres pasos: c&oacute;mo un mont&oacute;n de interruptores '
        u'microsc&oacute;picos acaban siendo un procesador.')) +

  bloque('02', u'Pr&aacute;ctica &middot; 25 min', ficha(
    u'Actividad 7.1 &middot; Escribe un programa para una m&aacute;quina tonta',
    [u'6.1'], u'Parejas &middot; 25 min &middot; sobre 10', u'''
          <h4>Con qu&eacute; cuentas</h4>
          <p>Solo con estas seis &oacute;rdenes, las mismas de la escena de arriba. No hay m&aacute;s.</p>
          <div class="copiar">
            <h4>Juego de instrucciones</h4>
            <ul>
              <li><b>ENCIENDE</b> &middot; pone la bombilla a 1</li>
              <li><b>APAGA</b> &middot; pone la bombilla a 0</li>
              <li><b>ESPERA</b> &middot; deja pasar un paso sin hacer nada</li>
              <li><b>SUMA 1</b> &middot; suma 1 a la cuenta</li>
              <li><b>VUELVE A n</b> &middot; la siguiente instrucci&oacute;n ser&aacute; la n&uacute;mero <i>n</i>
                  (en la escena solo aparece <i>VUELVE A 1</i>, pero vosotros pod&eacute;is saltar a
                  cualquiera)</li>
              <li><b>PARA</b> &middot; la m&aacute;quina se detiene</li>
            </ul>
          </div>
          <div class="nota">
            <span class="n-tag">Antes de empezar</span>
            La escena de arriba <b>no es un editor</b>: trae tres programas hechos y no se le pueden
            escribir otros. Los vuestros van en el cuaderno, y se comprueban <b>ejecut&aacute;ndolos a
            mano</b>, fase por fase, igual que hace ella.
          </div>
          <h4>Qu&eacute; hay que hacer</h4>
          <ol class="pasos">
            <li>Escribid, numerada, la lista de instrucciones que hace que la bombilla
                <b>parpadee tres veces y luego se pare</b>. Mirad antes el programa
                &laquo;Parpadeo&raquo; de la escena: hace casi eso, pero no para nunca.</li>
            <li>Escribid otra que <b>parpadee sin parar y vaya contando</b> los parpadeos.</li>
            <li>Haced la <b>tabla del ciclo</b> de la primera: una fila por paso, con tres columnas
                &mdash;<i>PC</i>, <i>fase</i> y <i>qu&eacute; pasa</i>&mdash; hasta completar
                <b>las cuatro primeras instrucciones</b> (doce filas).</li>
            <li>Con estas seis &oacute;rdenes hay cosas que <b>no se pueden</b> programar. Poned un ejemplo
                concreto, e inventad <b>la instrucci&oacute;n que har&iacute;a falta</b> para resolverlo,
                explicando qu&eacute; hace exactamente.</li>
            <li>Una frase final: en todo lo que hab&eacute;is hecho, <b>&iquest;qu&eacute; era hardware y qu&eacute; era
                software?</b></li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>El primer programa funciona y para donde debe <b>(2 puntos)</b>.</li>
            <li>El segundo usa bien el salto y no se olvida de contar <b>(2 puntos)</b>.</li>
            <li>La tabla del ciclo tiene las doce filas y las fases en orden <b>(3 puntos)</b>.</li>
            <li>La instrucci&oacute;n inventada resuelve de verdad el ejemplo que hab&eacute;is puesto
                <b>(2 puntos)</b>.</li>
            <li>La frase final distingue bien las dos mitades <b>(1 punto)</b>.</li>
          </ul>
          <div class="nota" style="margin-top:14px">
            <span class="n-tag">Aviso</span>
            &laquo;El programa es software y el ordenador es hardware&raquo; no puntúa: eso ya lo pon&iacute;a
            el enunciado. Hay que se&ntilde;alarlo <b>en lo vuestro</b>, y la lista de instrucciones que
            hab&eacute;is escrito en el cuaderno tambi&eacute;n cuenta.
          </div>
  ''')) +

  bloque('03', u'Cierre &middot; 5 min', u'''
      <p>Vuelve al dibujo imposible del principio. Ya no hace falta: una sola m&aacute;quina, y el
         comportamiento escrito aparte.</p>
      <ol>
      ''' + pregunta(u'&iquest;Por qu&eacute; se dice que un ordenador es una m&aacute;quina &laquo;de prop&oacute;sito general&raquo;?',
                     u'<p>Porque no est&aacute; construido para una tarea concreta. La m&aacute;quina es siempre la misma y lo que cambia es la <b>lista de instrucciones</b>, as&iacute; que vale para cualquier cosa que se pueda escribir como lista.</p>')
        + pregunta(u'Los tres pasos del ciclo de la CPU, en orden.',
                   u'<p><b>Busca</b> la instrucci&oacute;n en la memoria, la <b>descodifica</b> para saber qu&eacute; pide y la <b>ejecuta</b>. Y vuelve a empezar.</p>')
        + pregunta(u'Se te estropea el altavoz del m&oacute;vil. &iquest;Hardware o software? &iquest;Y si el m&oacute;vil suena, pero una aplicaci&oacute;n concreta no?',
                   u'<p>El altavoz roto es <b>hardware</b>: hay que cambiar la pieza. Si el resto suena y falla solo una aplicaci&oacute;n, es <b>software</b>: se corrige la instrucci&oacute;n equivocada y se vuelve a cargar. Distinguirlo es lo primero que se hace al reparar algo.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        La CPU <b>busca</b> la instrucci&oacute;n. &iquest;D&oacute;nde? La escena ten&iacute;a una caja llamada
        &laquo;memoria&raquo; y la hemos usado sin preguntar qu&eacute; hay dentro. Resulta que no hay una
        memoria, hay <b>dos</b>, y confundirlas explica las dos cosas que m&aacute;s te molestan de un
        ordenador.
      </div>

      <div class="copiar" style="border-color:var(--goo-verde)">
        <h4>Lectura del tema</h4>
        <p>Una sesi&oacute;n entera dedicada a leer y contestar. <b>30 p&aacute;rrafos numerados</b>: cada uno
           lee el suyo en voz alta, en orden. Despu&eacute;s, diez preguntas por escrito.</p>
        <p style="margin-top:10px"><a href="lectura-tema9.pdf" target="_blank" rel="noopener"
           style="font-family:var(--f-m);font-size:13px;color:var(--goo-verde);font-weight:500">
           &#8595; De una tecla que no responde a los ceros y unos &middot; PDF</a></p>
      </div>
  '''))


# ==========================================================================
# SESION 2 · Donde se guarda: RAM y almacenamiento
# ==========================================================================
S2 = (
  bloque('00', u'Reto inicial &middot; 10 min', u'''
      <p>Dos cosas que ya te han pasado, y que todo el mundo cuenta como si fueran mala suerte:</p>
      <ol>
        <li>Abres muchas pesta&ntilde;as y el ordenador empieza a <b>arrastrarse</b>. No se apaga, no da
            error: va lento y punto.</li>
        <li>Se va la luz y <b>pierdes el trabajo</b> que no hab&iacute;as guardado. El fichero de ayer sigue
            ah&iacute;; lo de hace dos minutos, no.</li>
      </ol>

      <div class="aviso">
        <span class="n-tag">La pregunta</span>
        &iquest;Son <b>dos problemas distintos</b> o son <b>el mismo</b>? Cont&eacute;stalo por escrito, y
        a&ntilde;ade: &iquest;arreglar&iacute;a alguno de los dos comprar un <b>disco m&aacute;s grande</b>?
      </div>

      <p>Comparad las respuestas. Van a salir dos, y las dos son falsas:</p>
      <ul>
        <li><b>&laquo;Va lento porque el procesador es malo&raquo;.</b> Si fuera eso, ir&iacute;a igual de
            lento con una sola pesta&ntilde;a. Y no: con una va bien.</li>
        <li><b>&laquo;Va lento porque no tengo espacio&raquo;.</b> Ponle un disco de 4 TB: el fichero de
            ayer seguir&aacute; ah&iacute;, seguir&aacute;s perdiendo lo de hace dos minutos y seguir&aacute; arrastr&aacute;ndose
            con quince pesta&ntilde;as. No has tocado el problema.</li>
      </ul>

      <div class="reto-piensa">
        <span class="n-tag">Piensa antes de seguir</span>
        <p>Si el disco grande no arregla ninguno de los dos, es que <b>el sitio donde est&aacute; lo que se
           pierde no es el disco</b>. Entonces, &iquest;d&oacute;nde est&aacute;?</p>
      </div>
  ''') +

  bloque('01', u'Teor&iacute;a &middot; 20 min', u'''
      <h3>Por qu&eacute; hacen falta dos memorias y no una</h3>
      <p>Lo ideal ser&iacute;a una sola memoria enorme, instant&aacute;nea y que no se borre. No existe: lo r&aacute;pido
         sale car&iacute;simo y lo barato sale lento. As&iacute; que se hacen <b>dos</b>, con papeles distintos.</p>
      <p>La comparaci&oacute;n que lo explica es tu propia mesa de estudio. En la <b>mesa</b> caben pocos
         libros, pero los tienes a mano. En la <b>estanter&iacute;a</b> cabe todo, pero hay que levantarse.</p>

''' + ESCENA_RAM + u'''
      <div class="copiar">
        <h4>Las dos memorias</h4>
        <p><b>Memoria RAM</b>: donde est&aacute; lo que se est&aacute; usando <b>ahora mismo</b>. Muy r&aacute;pida,
           peque&ntilde;a y <b>vol&aacute;til</b>: al cortar la corriente se borra entera.</p>
        <p><b>Almacenamiento</b> (disco duro o SSD): donde se guarda lo que tiene que <b>seguir ah&iacute;
           ma&ntilde;ana</b>. Enorme, mucho m&aacute;s lento y <b>no vol&aacute;til</b>.</p>
        <p>Un programa no se ejecuta desde el disco: primero se <b>carga</b> en la RAM, y la CPU trabaja
           siempre contra la RAM.</p>
      </div>

      <h3>Cu&aacute;nto es &laquo;m&aacute;s lento&raquo;, en n&uacute;meros</h3>
      <p>&laquo;R&aacute;pido&raquo; y &laquo;lento&raquo; no dicen nada hasta que se miden. Estos son los
         &oacute;rdenes de magnitud t&iacute;picos de hoy:</p>

      <div class="copiar">
        <h4>Tiempo en llegar a un dato</h4>
        <table>
          <tr><th>D&oacute;nde est&aacute;</th><th>Tarda</th><th>Veces m&aacute;s que la RAM</th></tr>
          <tr><td>Memoria RAM</td><td>80 ns</td><td>1</td></tr>
          <tr><td>SSD</td><td>0,1 ms</td><td>1.250</td></tr>
          <tr><td>Disco duro con platos</td><td>10 ms</td><td>125.000</td></tr>
        </table>
        <p>Un <b>nanosegundo</b> (ns) es la mil millon&eacute;sima parte de un segundo; un
           <b>milisegundo</b> (ms), la mil&eacute;sima.</p>
      </div>

      <p>Esos n&uacute;meros son tan peque&ntilde;os que no significan nada. As&iacute; que se estiran: imagina que ir a
         buscar un dato a la RAM te costara <b>un segundo</b>. Multiplicando los tres por el mismo
         factor, que es 12,5 millones:</p>

      <div class="copiar">
        <h4>Lo mismo, a escala humana</h4>
        <ul>
          <li>Buscar en la <b>RAM</b>: <b>1 segundo</b>. Alargas el brazo.</li>
          <li>Buscar en el <b>SSD</b>: <b>21 minutos</b>. Bajas a la biblioteca.</li>
          <li>Buscar en el <b>disco duro</b>: <b>35 horas</b>. Vas a otra ciudad y vuelves.</li>
        </ul>
      </div>

      <p>Con eso las dos molestias del principio dejan de ser mala suerte y pasan a ser
         <b>consecuencias</b>. Se te llena la mesa: el sistema empieza a bajar cosas a la estanter&iacute;a y a
         subirlas, y cada viaje cuesta mil veces m&aacute;s. Se va la luz: la mesa se vac&iacute;a, porque la RAM
         necesita corriente para acordarse.</p>

''' + foto('u7-ram-ddr4.jpg',
           u'M&oacute;dulo de memoria RAM DDR4 visto de frente, con ocho chips negros sobre la placa verde',
           u'Un m&oacute;dulo de <b>RAM</b> de 16 GB. Los ocho rect&aacute;ngulos negros son los chips donde est&aacute;n '
           u'las celdas; la tira dorada de abajo es por donde se enchufa a la placa. Se cambia en un '
           u'minuto y sin soldar: es de las pocas reparaciones que puedes hacer t&uacute;.',
           u'PantheraLeo1359531', u'CC BY 4.0',
           u'https://commons.wikimedia.org/wiki/File:16_GiB-DDR4-RAM-Riegel_RAM019FIX_Small_Crop_90_PCNT.png') +
    foto('u7-disco-abierto.jpg',
         u'Disco duro abierto donde se ve el plato met&aacute;lico brillante y el brazo con el cabezal de lectura',
         u'Un <b>disco duro</b> abierto. El plato gira a miles de vueltas por minuto y el brazo lleva el '
         u'cabezal hasta la pista que toca. Ah&iacute; est&aacute; el problema: hay que <b>mover algo f&iacute;sico</b>, '
         u'y mover algo tarda milisegundos. Un <b>SSD</b> no tiene ninguna pieza que se mueva, y por eso '
         u'arranca el sistema en segundos.',
         u'Zzubnik', u'Dominio p&uacute;blico',
         u'https://commons.wikimedia.org/wiki/File:Open_hard-drive.jpg') + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; no hace falta copiarlo</span>
        <p>Antes de los chips, la memoria de trabajo de los ordenadores fue esto: una rejilla de
           <b>anillos de ferrita</b> ensartados en hilos de cobre. Cada anillo se imanta en un sentido o
           en el otro, y eso guarda <b>un bit</b>. Uno. Y a diferencia de la RAM de hoy,
           <b>no se borraba al apagar</b>.</p>
        <p>Lo impresionante es c&oacute;mo se fabricaba: <b>ensartando los anillos a mano</b>, uno a uno, con
           aguja. Haz la cuenta con el m&oacute;dulo de la foto de arriba. Tiene 16 GB, o sea
           <b>137.438.953.472 bits</b>. A un anillo por segundo, sin dormir ni parar,
           ser&iacute;an m&aacute;s de <b>4.300 a&ntilde;os</b>.</p>
      </div>

''' + foto('u7-nucleos-ferrita.jpg',
           u'Primer plano de una memoria de n&uacute;cleos de ferrita: peque&ntilde;os anillos oscuros ensartados en una rejilla de hilos rojos',
           u'Memoria de <b>n&uacute;cleos de ferrita</b>, conservada en el Museo de Inform&aacute;tica Hist&oacute;rica de '
           u'la Universidad de Zaragoza. Cada anillo oscuro es <b>un bit</b>. Cu&eacute;ntalos en la foto y '
           u'ver&aacute;s la memoria completa de un ordenador entero.',
           u'Jos&eacute; Luis Briz Velasco', u'CC BY-SA 4.0',
           u'https://commons.wikimedia.org/wiki/File:Museo_de_Inform%C3%A1tica_Hist%C3%B3rica_(MIH)_-_UNIZAR_-_Magnetic-core_memory_close_up.jpg') +
  video('video-mem', 'o3gGXwY-1uI',
        u'Diferencias entre SSD, disco duro y memoria RAM',
        u'Inform&aacute;ticaI3J &middot; en espa&ntilde;ol &middot; unos 6 minutos',
        u'Repasa los tres componentes con piezas reales en la mano.')) +

  bloque('02', u'Pr&aacute;ctica &middot; 25 min', ficha(
    u'Actividad 7.2 &middot; La factura de la lentitud',
    [u'6.1'], u'Parejas &middot; 25 min &middot; sobre 10', u'''
          <h4>El caso</h4>
          <p>Un ordenador del aula tiene <b>8 GB de RAM</b> y un <b>disco duro de platos de 500 GB</b>,
             del que est&aacute;n usados 180 GB. Un alumno lo tiene as&iacute; ahora mismo:</p>
          <div class="copiar">
            <h4>Lo que ocupa cada cosa en la RAM</h4>
            <table>
              <tr><th>Programa</th><th>RAM</th></tr>
              <tr><td>Sistema operativo</td><td>2,5 GB</td></tr>
              <tr><td>Navegador con 12 pesta&ntilde;as, a 0,35 GB cada una</td><td>?</td></tr>
              <tr><td>Editor de textos</td><td>0,8 GB</td></tr>
              <tr><td>Reproductor de m&uacute;sica</td><td>0,4 GB</td></tr>
              <tr><td>Antivirus</td><td>0,6 GB</td></tr>
            </table>
          </div>
          <h4>Qu&eacute; hay que hacer</h4>
          <ol class="pasos">
            <li>Calculad cu&aacute;nta RAM <b>pide en total</b>, y decid si cabe en los 8 GB. Si no cabe,
                <b>cu&aacute;nto falta</b>.</li>
            <li>Con lo que no cabe el sistema tiene que ir al disco. Con los datos de la tabla de
                tiempos, decid <b>cu&aacute;ntas veces m&aacute;s</b> tarda en llegar a un dato que est&eacute; en ese
                disco duro que a uno que est&eacute; en la RAM.</li>
            <li>El alumno <b>cierra dos pesta&ntilde;as</b>. Rehaced la cuenta. &iquest;Cabe ya? Escribid en una
                frase qu&eacute; acaba de demostrar eso.</li>
            <li>Hay <b>60 euros</b> y dos opciones, que cuestan lo mismo:
                <b>(A)</b> a&ntilde;adir 8 GB de RAM, o <b>(B)</b> cambiar el disco duro por un SSD de 500 GB.
                Elegid una y <b>justificadla con n&uacute;meros</b>, no con opiniones. Decid tambi&eacute;n qu&eacute;
                problema <b>no</b> arregla la que hab&eacute;is elegido.</li>
            <li>Al alumno se le apaga el ordenador de golpe. Decid <b>exactamente qu&eacute; pierde</b> y
                <b>qu&eacute; no</b>, y por qu&eacute;.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>La suma est&aacute; bien y se dice cu&aacute;nto falta <b>(2 puntos)</b>.</li>
            <li>El factor de lentitud est&aacute; bien sacado de la tabla <b>(2 puntos)</b>.</li>
            <li>La conclusi&oacute;n del paso 3 no se queda en &laquo;cabe&raquo;: explica <b>por qu&eacute;</b> importa
                <b>(2 puntos)</b>.</li>
            <li>La elecci&oacute;n de compra va con n&uacute;meros y admite qu&eacute; deja sin resolver <b>(3 puntos)</b>.</li>
            <li>La respuesta sobre el apag&oacute;n distingue vol&aacute;til de no vol&aacute;til <b>(1 punto)</b>.</li>
          </ul>
          <div class="nota" style="margin-top:14px">
            <span class="n-tag">Aviso</span>
            En el paso 4 <b>no hay una respuesta correcta &uacute;nica</b>: las dos se pueden defender. Lo que
            se puntúa es el razonamiento. Lo que no vale es &laquo;el SSD porque es mejor&raquo;.
          </div>
  ''')) +

  bloque('03', u'Cierre &middot; 5 min', u'''
      <ol>
      ''' + pregunta(u'&iquest;Por qu&eacute; se pierde lo que no has guardado, pero no lo de ayer?',
                     u'<p>Porque lo que est&aacute;s escribiendo est&aacute; en la <b>RAM</b>, que es <b>vol&aacute;til</b>: necesita corriente para acordarse. Lo de ayer est&aacute; en el <b>almacenamiento</b>, que no la necesita. <i>Guardar</i> es precisamente copiar de una a otro.</p>')
        + pregunta(u'Tienes 8 GB de RAM y un disco de 1 TB. &iquest;Por qu&eacute; el ordenador va lento con muchas pesta&ntilde;as si te sobra tanto disco?',
                   u'<p>Porque lo que se llena es la <b>RAM</b>, no el disco. Cuando no cabe, el sistema empieza a mover datos al disco y a traerlos de vuelta, y el disco es miles de veces m&aacute;s lento. Sobrar disco no ayuda: el problema es el tama&ntilde;o de la mesa, no el de la estanter&iacute;a.</p>')
        + pregunta(u'&iquest;Por qu&eacute; un SSD arranca el sistema mucho antes que un disco duro de platos?',
                   u'<p>Porque en el disco duro hay que <b>mover piezas</b>: el plato gira y el brazo se coloca. Eso tarda milisegundos. En un SSD no se mueve nada, todo es electr&oacute;nico, y cada acceso cuesta unas cien veces menos.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Hay huecos en la RAM y huecos en el disco. Queda la pregunta inc&oacute;moda:
        <b>&iquest;qu&eacute; hay escrito dentro de un hueco?</b> No hay letras, ni n&uacute;meros, ni fotos. Solo hay
        cables, y un cable nada m&aacute;s sabe decir dos cosas.
      </div>
  '''))


# ==========================================================================
# SESION 3 · Ceros y unos
# ==========================================================================
S3 = (
  bloque('00', u'Reto inicial &middot; 10 min', u'''
      <p>De la unidad de electricidad te llevaste un hecho que ahora vale oro: por un cable
         <b>pasa corriente o no pasa</b>. Eso es todo lo que un cable sabe distinguir con seguridad.</p>

      <div class="aviso">
        <span class="n-tag">El encargo</span>
        Tienes una m&aacute;quina hecha de cables. Inv&eacute;ntate una forma de guardar ah&iacute; dentro
        <b>tu nombre</b>. Escribe tu m&eacute;todo en el cuaderno antes de seguir leyendo.
      </div>

      <p>La idea que se le ocurre a casi todo el mundo es <b>una tensi&oacute;n para cada letra</b>: 0,2 V
         para la A, 0,4 V para la B, y as&iacute; hasta la Z. Es ingeniosa, y no funciona. Hagamos la cuenta
         que lo demuestra.</p>

      <div class="reto-piensa">
        <span class="n-tag">La cuenta que rompe la idea</span>
        <p>El circuito trabaja a <b>5 V</b> y hacen falta <b>27 letras</b>. Reparte los 5 V entre las
           27: quedan <b>26 escalones</b>, uno cada <b>0,19 V</b>. Ahora piensa en un cable de verdad,
           que se calienta, que tiene un motor al lado y al que le llega ruido el&eacute;ctrico. Con un ruido
           de 0,3 V, <b>&iquest;qu&eacute; letra ha llegado?</b></p>
      </div>

      <p>No hay manera de saberlo: 0,3 V es m&aacute;s de <b>un escal&oacute;n y medio</b>, as&iacute; que la letra
         que llega no tiene por qu&eacute; ser la que sali&oacute;. Y no se arregla midiendo mejor, porque el
         problema no es el aparato, es la <b>distancia entre escalones</b>. Cuantos m&aacute;s s&iacute;mbolos
         metes, m&aacute;s juntos quedan y m&aacute;s f&aacute;cil es confundirlos.</p>

      <p>La salida es rendirse en lo que parec&iacute;a una ventaja: <b>usar solo dos s&iacute;mbolos</b>. Con 0 V y
         5 V los escalones quedan a 5 V de distancia. Ese mismo ruido de 0,3 V ya no confunde
         absolutamente nada. Renuncias a meter mucho por un cable, y a cambio ganas <b>no equivocarte
         nunca</b>.</p>
  ''') +

  bloque('01', u'Teor&iacute;a &middot; 20 min', u'''
      <h3>Con dos s&iacute;mbolos, &iquest;hasta d&oacute;nde se llega?</h3>
      <p>La objeci&oacute;n evidente es que con dos s&iacute;mbolos no cabe nada. Y es falsa, por una raz&oacute;n de
         aritm&eacute;tica: no se usa <b>un</b> cable, se usan <b>varios a la vez</b>, y las combinaciones se
         multiplican.</p>
      <p>Pulsa los ocho interruptores de abajo. Y fíjate en las tres cajas del final: es
         <b>el mismo byte</b> le&iacute;do de tres maneras distintas.</p>

''' + ESCENA_BITS + u'''
      <div class="copiar">
        <h4>Bit y byte</h4>
        <p><b>Bit</b>: la unidad m&iacute;nima de informaci&oacute;n. Dos estados posibles: <b>0</b> o <b>1</b>.
           Es un interruptor.</p>
        <p><b>Byte</b>: un grupo de <b>8 bits</b>. Es la unidad con la que se mide todo lo dem&aacute;s.</p>
        <p>Con <b>n</b> bits salen <b>2<sup>n</sup></b> combinaciones distintas. Con 8 bits,
           <b>2<sup>8</sup> = 256</b>.</p>
        <table>
          <tr><th>Bits</th><th>Combinaciones</th><th>Para qu&eacute; da</th></tr>
          <tr><td>1</td><td>2</td><td>s&iacute; o no</td></tr>
          <tr><td>4</td><td>16</td><td>las cifras del 0 al 15</td></tr>
          <tr><td>8</td><td>256</td><td>una letra, o un nivel de gris</td></tr>
          <tr><td>16</td><td>65.536</td><td>casi cualquier idioma escrito</td></tr>
          <tr><td>24</td><td>16.777.216</td><td>un color de pantalla</td></tr>
        </table>
      </div>

      <h3>C&oacute;mo se lee un byte: el acuerdo</h3>
      <p>Un byte por s&iacute; solo <b>no significa nada</b>. El mismo <b>0100 0001</b> es el n&uacute;mero 65, es
         la letra A y es un gris oscuro. Lo que decide cu&aacute;l de las tres cosas es un <b>acuerdo</b>
         previo sobre c&oacute;mo hay que interpretarlo.</p>

      <div class="copiar">
        <h4>C&oacute;mo se guarda cada cosa</h4>
        <ul>
          <li><b>N&uacute;meros</b>: en <b>binario</b>. Cada posici&oacute;n vale el doble que la de su derecha:
              128, 64, 32, 16, 8, 4, 2, 1. Se suman las que valen 1.</li>
          <li><b>Texto</b>: con una <b>tabla</b> acordada que asigna un n&uacute;mero a cada car&aacute;cter. La
              cl&aacute;sica es <b>ASCII</b>: la A es el 65, la a es el 97, el espacio es el 32.</li>
          <li><b>Im&aacute;genes</b>: la foto se parte en <b>p&iacute;xeles</b> y de cada uno se guarda su color con
              <b>3 bytes</b> (rojo, verde y azul, de 0 a 255 cada uno).</li>
          <li><b>Sonido</b>: se mide la onda <b>miles de veces por segundo</b> y cada medida se guarda
              como un n&uacute;mero.</li>
        </ul>
        <p>Y las unidades: <b>1 kB</b> son mil bytes, <b>1 MB</b> un mill&oacute;n, <b>1 GB</b> mil millones.</p>
      </div>

''' + foto('u7-tarjeta-perforada.jpg',
           u'Tarjeta perforada de ordenador IBM usada, con agujeros rectangulares recortados sobre las filas de cifras impresas',
           u'Una <b>tarjeta perforada</b> de verdad, de las que se usaron hasta los a&ntilde;os ochenta. Tiene '
           u'80 columnas y, en cada posici&oacute;n de cada columna, <b>hay agujero o no lo hay</b>: no existe '
           u'el medio agujero. Es la misma decisi&oacute;n del reto de hoy, tomada con cartulina en vez de con '
           u'cables, y por el mismo motivo: dos estados no se confunden nunca.',
           u'Pete Birkinshaw', u'CC BY 2.0',
           u'https://commons.wikimedia.org/wiki/File:Used_Punchcard_(5151286161).jpg') + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; no hace falta copiarlo</span>
        <p>Que ganara el binario no era obvio, y hubo quien lo intent&oacute; de otra forma. El <b>ENIAC</b>
           era <b>decimal</b>: gastaba diez tubos por cada cifra. Y en 1958, en la Universidad de Mosc&uacute;,
           Nikol&aacute;i Brus&eacute;ntsov construy&oacute; el <b>Setun</b>, un ordenador <b>ternario</b>, de tres estados.
           Sobre el papel era m&aacute;s eficiente, se fabricaron unas cincuenta m&aacute;quinas y funcionaban.</p>
        <p>Perdi&oacute; igual, y no por ser peor idea: porque construir un componente que distinga
           <b>dos</b> estados es much&iacute;simo m&aacute;s barato y m&aacute;s fiable que uno que distinga tres, y esa
           ventaja se multiplica por los miles de millones de componentes que lleva un chip. Gan&oacute; lo
           <b>tonto y seguro</b> sobre lo elegante, que en tecnolog&iacute;a pasa a menudo.</p>
      </div>

''' + video('video-bin', 'iRpB3TVCCtE',
            u'&iquest;Por qu&eacute; los ordenadores usan el sistema binario?',
            u'EDteam &middot; en espa&ntilde;ol',
            u'Cuenta la misma historia del reto de hoy: por qu&eacute; dos estados y no diez.')) +

  bloque('02', u'Pr&aacute;ctica &middot; 25 min', ficha(
    u'Actividad 7.3 &middot; Cu&aacute;nto ocupa lo que haces',
    [u'6.1'], u'Parejas &middot; 25 min &middot; sobre 10', u'''
          <h4>Qu&eacute; hay que hacer</h4>
          <p>Para la parte de letras pod&eacute;is usar la escena de los ocho interruptores: poned el n&uacute;mero
             y leed la letra, o al rev&eacute;s.</p>
          <ol class="pasos">
            <li>Escribid <b>vuestro nombre de pila</b> en ASCII, dos veces: primero en n&uacute;meros y
                despu&eacute;s en binario de 8 bits. Sin acentos y sin e&ntilde;e, que esos no est&aacute;n en la tabla
                b&aacute;sica &mdash;y esa ya es una conclusi&oacute;n: escribid una frase diciendo qu&eacute; problema
                revela eso.</li>
            <li>Calculad <b>cu&aacute;ntos bytes ocupa</b> vuestro nombre.</li>
            <li>Una foto de m&oacute;vil tiene <b>4.000 &times; 3.000 p&iacute;xeles</b>. Calculad cu&aacute;ntos p&iacute;xeles
                son, y cu&aacute;ntos <b>bytes</b> ocupar&iacute;a sin comprimir <b>en color</b> (3 bytes por p&iacute;xel).
                Pasadlo a <b>MB</b>.</li>
            <li>Rehaced la cuenta <b>en blanco y negro</b> (1 byte por p&iacute;xel). &iquest;Cu&aacute;ntas veces menos
                ocupa? Decid <b>por qu&eacute;</b> sale ese factor exacto.</li>
            <li>En una tarjeta de <b>64 GB</b>, &iquest;cu&aacute;ntas de esas fotos en color caben? (Usad
                1 GB = mil millones de bytes.)</li>
            <li>Abrid la galer&iacute;a de un m&oacute;vil y mirad lo que ocupa una foto de verdad: unos
                <b>4 MB</b>, no los que os han salido. <b>&iquest;D&oacute;nde ha ido el resto?</b> No hace falta
                que sep&aacute;is la respuesta t&eacute;cnica; escribid vuestra hip&oacute;tesis.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>El nombre est&aacute; bien codificado en las dos formas <b>(2 puntos)</b>.</li>
            <li>La frase sobre los acentos entiende el problema y no lo despacha <b>(1 punto)</b>.</li>
            <li>La cuenta de la foto en color est&aacute; bien, con las unidades puestas <b>(3 puntos)</b>.</li>
            <li>El factor entre color y blanco y negro est&aacute; bien <b>explicado</b>, no solo calculado
                <b>(2 puntos)</b>.</li>
            <li>El n&uacute;mero de fotos en la tarjeta est&aacute; bien <b>(1 punto)</b>.</li>
            <li>La hip&oacute;tesis final es razonable <b>(1 punto)</b>.</li>
          </ul>
          <div class="nota" style="margin-top:14px">
            <span class="n-tag">Pista para el paso 6</span>
            Mira una foto tuya del cielo. &iquest;Cu&aacute;ntos p&iacute;xeles seguidos crees que son <b>exactamente
            del mismo azul</b>? Guardar tres bytes por cada uno de ellos, uno detr&aacute;s de otro, es
            tirar sitio.
          </div>
  ''')) +

  bloque('03', u'Cierre &middot; 5 min', u'''
      <ol>
      ''' + pregunta(u'&iquest;Por qu&eacute; los ordenadores usan dos s&iacute;mbolos y no diez, si con diez cabr&iacute;a m&aacute;s?',
                     u'<p>Porque con dos los estados quedan <b>lo m&aacute;s separados posible</b> y el ruido el&eacute;ctrico no los confunde. Con diez, los escalones quedan tan juntos que cualquier interferencia cambia el dato. Se renuncia a capacidad por cable a cambio de <b>fiabilidad</b>, y se compensa poniendo muchos cables.</p>')
        + pregunta(u'&iquest;Cu&aacute;ntas combinaciones distintas dan 8 bits, y por qu&eacute; sale ese n&uacute;mero?',
                   u'<p><b>256</b>, porque cada bit duplica las posibilidades del anterior: 2<sup>8</sup> = 256. Van del 0 al 255, que son 256 valores contando el cero.</p>')
        + pregunta(u'El byte 0100 0001 &iquest;es el n&uacute;mero 65, la letra A o un gris oscuro?',
                   u'<p>Las tres cosas, y ninguna por s&iacute; sola. Un byte no significa nada hasta que hay un <b>acuerdo</b> sobre c&oacute;mo leerlo. El programa que lo abre es quien sabe qu&eacute; acuerdo toca: por eso una foto abierta con un editor de texto sale como basura.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Lo que falta del tema</span>
        Con esto ya tienes el n&uacute;cleo: <b>una m&aacute;quina</b> que obedece listas, <b>dos memorias</b> donde
        vive lo que obedece, y <b>ceros y unos</b> como &uacute;nico material. Quedan tres sesiones para
        cerrarlo: c&oacute;mo <b>entra y sale</b> la informaci&oacute;n (los perif&eacute;ricos), qui&eacute;n <b>reparte</b> la
        m&aacute;quina entre todos los programas a la vez (el sistema operativo) y c&oacute;mo se <b>diagnostica</b>
        una aver&iacute;a sabiendo todo esto.
      </div>
      <div class="nota">
        <span class="n-tag">Y despu&eacute;s del tema</span>
        Tienes una m&aacute;quina que procesa informaci&oacute;n ella sola. La pregunta siguiente es la que abre
        la unidad de <b>Internet, datos y seguridad</b>: <b>&iquest;y si hay millones de estas m&aacute;quinas
        y quieren hablar entre ellas?</b>
      </div>
  '''))


# ==========================================================================
# SESION 4 · Entrada y salida
# ==========================================================================
S4 = (
  bloque('00', u'Reto inicial &middot; 10 min', u'''
      <p>La sesi&oacute;n pasada acab&oacute; en un sitio inc&oacute;modo: dentro de la m&aacute;quina no hay
         palabras ni im&aacute;genes, solo <b>ceros y unos</b>. Y t&uacute; no eres ceros y unos. La clase
         tampoco.</p>

      <div class="aviso">
        <span class="n-tag">El encargo</span>
        Haz que el ordenador sepa <b>qu&eacute; temperatura hace ahora mismo en el aula</b>. No vale
        mirar el term&oacute;metro y teclear el n&uacute;mero: tiene que enterarse <b>&eacute;l</b>. Escribe
        tu m&eacute;todo antes de seguir.
      </div>

      <p>Van a salir estas tres, y las tres se caen solas:</p>
      <ul>
        <li><b>&laquo;Le pongo un term&oacute;metro dentro&raquo;.</b> Un term&oacute;metro de los de
            mercurio no le dice nada a un cable. La columna sube, y ah&iacute; se queda.</li>
        <li><b>&laquo;Un cable para cada temperatura&raquo;.</b> Uno para 20&nbsp;&deg;C, otro para 21,
            otro para 22&hellip; Ya viste ad&oacute;nde lleva eso en la sesi&oacute;n 3: a un cable por
            s&iacute;mbolo, que es justo lo que no se puede hacer.</li>
        <li><b>&laquo;Que mida y me lo diga&raquo;.</b> Vale, &iquest;y qu&eacute; pasa con 20,5?
            &iquest;Y con 20,53? &iquest;Y con 20,531?</li>
      </ul>

      <div class="reto-piensa">
        <span class="n-tag">El problema de verdad</span>
        <p>La temperatura <b>no va a saltos</b>. Entre 20 y 21 grados hay infinitos valores, y lo mismo
           pasa con la luz que entra por la ventana y con el sonido de tu voz. La m&aacute;quina, en
           cambio, <b>solo tiene escalones</b>. &iquest;C&oacute;mo se mete algo que no tiene escalones
           en una caja que solo sabe contar escalones?</p>
      </div>

      <p>La respuesta honrada es que <b>no se mete</b>. Lo que entra en la m&aacute;quina no es el mundo:
         es una <b>copia con escalones</b>, hecha a prop&oacute;sito, y el oficio consiste en que los
         escalones sean tan peque&ntilde;os que ya no se noten. Hoy vas a ver exactamente cu&aacute;nto
         se pierde por el camino, porque se puede medir.</p>
  ''') +

  bloque('01', u'Teor&iacute;a &middot; 20 min', u'''
      <h3>Primero: algo que traduzca el mundo a voltios</h3>
      <p>Antes de haber n&uacute;meros tiene que haber <b>electricidad</b>, porque es el &uacute;nico
         idioma que entiende la m&aacute;quina. De eso se encargan unos componentes cuya propiedad
         el&eacute;ctrica cambia cuando cambia el mundo:</p>
      <ul>
        <li>Una <b>LDR</b>: cuanta m&aacute;s luz le da, menos resistencia tiene.</li>
        <li>Un <b>termistor</b>: su resistencia cambia con la temperatura.</li>
        <li>Un <b>micr&oacute;fono</b>: el aire empuja una l&aacute;mina y eso genera una tensi&oacute;n
            que sube y baja igual que el sonido.</li>
      </ul>
      <p>Todav&iacute;a no hay ni un n&uacute;mero. Lo que hay es una tensi&oacute;n que sube y baja
         <b>igual que sube y baja el mundo</b>, sin escalones. A eso se le llama se&ntilde;al
         anal&oacute;gica, y es lo que hay que convertir.</p>

      <div class="copiar">
        <h4>Las dos clases de se&ntilde;al</h4>
        <p><b>Se&ntilde;al anal&oacute;gica</b>: var&iacute;a de forma continua y puede tomar
           <b>infinitos valores</b>. La temperatura, el sonido, la luz.</p>
        <p><b>Se&ntilde;al digital</b>: solo puede tomar <b>unos valores concretos</b>, contados. Los
           ceros y unos de la sesi&oacute;n 3.</p>
        <p><b>Sensor</b>: componente que convierte una magnitud f&iacute;sica en una magnitud
           el&eacute;ctrica. Es la puerta de <b>entrada</b> del mundo a la m&aacute;quina.</p>
      </div>

      <h3>Segundo: alguien que le ponga n&uacute;meros a esa tensi&oacute;n</h3>
      <p>El <b>conversor anal&oacute;gico-digital</b> hace dos cosas, y las dos son decisiones que
         alguien tom&oacute;. Cambia los dos controles de la escena y mira los n&uacute;meros de abajo:
         no son adornos, est&aacute;n medidos sobre lo que acabas de dibujar.</p>

''' + ESCENA_ADC + u'''
      <div class="copiar">
        <h4>C&oacute;mo se convierte el mundo en n&uacute;meros</h4>
        <p><b>Muestreo</b>: cada cu&aacute;nto se mira. Se mide un n&uacute;mero de veces por segundo y
           entre medida y medida <b>no se sabe nada</b> de lo que hizo la se&ntilde;al.</p>
        <p><b>Cuantificaci&oacute;n</b>: con cu&aacute;nta finura se anota cada medida. Con <b>n</b> bits
           hay <b>2<sup>n</sup></b> valores posibles, que se reparten toda la escala en
           <b>2<sup>n</sup> &minus; 1</b> escalones.</p>
        <p>La copia <b>nunca</b> es exacta: a la diferencia entre lo que hab&iacute;a y lo que se anota se
           le llama <b>error de cuantificaci&oacute;n</b>, y como mucho es <b>medio escal&oacute;n</b>.</p>
        <p>M&aacute;s bits y m&aacute;s medidas dan una copia m&aacute;s fiel, y <b>siempre</b> cuestan
           m&aacute;s bytes. No hay forma de escapar de ese trato.</p>
      </div>

      <div class="nota">
        <span class="n-tag">Cu&aacute;ntas veces hay que medir</span>
        No vale medir &laquo;a ojo&raquo;: hay una regla. Para no perder un sonido hay que medir
        <b>m&aacute;s del doble de veces por segundo</b> que la frecuencia m&aacute;s alta que se quiera
        guardar. Por eso el tel&eacute;fono, que llega hasta unos 3.400&nbsp;Hz, mide <b>8.000 veces por
        segundo</b>, y un CD, que quiere llegar a los 20.000&nbsp;Hz que oye un o&iacute;do joven, mide
        <b>44.100</b>.
      </div>

      <h3>Tercero: el camino de vuelta</h3>
      <p>Para sacar algo fuera se hace lo mismo al rev&eacute;s. La m&aacute;quina suelta n&uacute;meros y
         un <b>conversor digital-anal&oacute;gico</b> los convierte en una tensi&oacute;n que mueve algo:
         el cono de un altavoz, un motor, la luz de un p&iacute;xel.</p>

      <div class="copiar">
        <h4>Sensores y actuadores</h4>
        <p><b>Sensor</b> &middot; el mundo &rarr; electricidad &rarr; n&uacute;meros. Es
           <b>entrada</b>: LDR, termistor, micr&oacute;fono, sensor de distancia por ultrasonidos,
           bot&oacute;n.</p>
        <p><b>Actuador</b> &middot; n&uacute;meros &rarr; electricidad &rarr; el mundo. Es
           <b>salida</b>: motor, servo, altavoz, LED, electrov&aacute;lvula, resistencia calefactora.</p>
        <p>Un robot no es m&aacute;s que esto: <b>sensores</b> que le cuentan qu&eacute; pasa,
           un programa que decide y <b>actuadores</b> que hacen algo al respecto.</p>
      </div>

      <h3>Y por d&oacute;nde entra y sale todo eso: perif&eacute;ricos y puertos</h3>
      <div class="copiar">
        <h4>Perif&eacute;ricos</h4>
        <p>Perif&eacute;rico es todo aparato que se conecta al ordenador y no es el ordenador.</p>
        <ul>
          <li><b>De entrada</b>: teclado, rat&oacute;n, micr&oacute;fono, c&aacute;mara,
              esc&aacute;ner, lector de c&oacute;digos.</li>
          <li><b>De salida</b>: pantalla, altavoces, impresora, proyector.</li>
          <li><b>Mixtos</b>, que hacen las dos cosas: pantalla t&aacute;ctil, tarjeta de red,
              memoria USB, disco externo, impresora multifunci&oacute;n.</li>
        </ul>
        <p>El <b>puerto</b> es la conexi&oacute;n por la que se enchufan: USB, HDMI, jack de 3,5&nbsp;mm,
           RJ45 de red, ranura de tarjeta SD.</p>
      </div>

      <p>Y aqu&iacute; vuelve una palabra de la sesi&oacute;n 3. Un puerto <b>no es solo un agujero con
         una forma</b>: es un <b>acuerdo</b> sobre cu&aacute;ntos voltios significan 1, en qu&eacute;
         orden van los bits, a qu&eacute; velocidad y qui&eacute;n habla primero. Que cada uno tenga una
         forma distinta es a prop&oacute;sito: as&iacute; no puedes enchufar algo donde su acuerdo no
         vale.</p>

''' + foto('u7-puertos.jpg',
           u'Panel trasero de un ordenador peque&ntilde;o con interruptor, cuatro conectores USB, tres jacks de audio de colores y un conector serie',
           u'La trasera de un ordenador. Cuenta las formas distintas: cuatro <b>USB</b> rectangulares, tres '
           u'<b>jacks</b> de audio (verde la salida, azul la entrada, rosa el micr&oacute;fono) y un '
           u'conector <b>serie</b> de nueve patillas, de los antiguos. Ninguno entra en el hueco de otro, '
           u'y eso <b>no es casualidad</b>: cada uno lleva dentro un acuerdo distinto.',
           u'VIA Gallery, Hsintien (Taiw&aacute;n)', u'CC BY 2.0',
           u'https://commons.wikimedia.org/wiki/File:VIA_AMOS-3000_Back_Panel_I-O_(3305466345).jpg') +
    foto('u7-ldr.jpg',
         u'Primer plano de una LDR: una c&aacute;psula redonda con una pista naranja en zigzag bajo un cristal y dos patillas',
         u'Una <b>LDR</b> de 25&nbsp;mm vista de cerca. Esa pista naranja en zigzag es el sensor: cuando '
         u'le da la luz conduce mejor, y cuando se queda a oscuras conduce peor. No sabe qu&eacute; es la '
         u'luz ni cu&aacute;nta hay; solo <b>cambia de resistencia</b>. Poner un n&uacute;mero a ese '
         u'cambio es trabajo del conversor.',
         u'Suyash Dwivedi', u'CC BY-SA 4.0',
         u'https://commons.wikimedia.org/wiki/File:25mm_light-dependent_resistor_(LDR)_(1).jpg') + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; no hace falta copiarlo</span>
        <p>&iquest;Por qu&eacute; al tel&eacute;fono hay que deletrear &laquo;<i>ese</i>, de Soria&raquo;?
           Porque la voz por tel&eacute;fono se mide <b>8.000 veces por segundo</b> y eso obliga a cortar
           todo lo que suene por encima de unos 3.400&nbsp;Hz. El problema es que la <b>s</b> y la
           <b>f</b> tienen casi toda su energ&iacute;a <b>por encima</b> de esa frecuencia: al cortarlas,
           las dos se quedan en el mismo soplido y dejan de distinguirse.</p>
        <p>No es que el tel&eacute;fono suene mal: es que alguien <b>decidi&oacute;</b> cu&aacute;nto se
           iba a tirar a la basura, a cambio de que la llamada ocupara poco. Esa decisi&oacute;n es
           exactamente la de la escena de arriba, y se tom&oacute; en <b>1962</b>, en Chicago, con el
           primer sistema telef&oacute;nico digital del mundo. Sesenta a&ntilde;os despu&eacute;s sigues
           deletreando por su culpa.</p>
      </div>

''' + video('video-adc', '9GxcNyGQsuk',
            u'Muestreo / Cuantificaci&oacute;n / Codificaci&oacute;n',
            u'Universitat Polit&egrave;cnica de Val&egrave;ncia &middot; en espa&ntilde;ol',
            u'Los mismos tres pasos de hoy, contados con la se&ntilde;al delante. Es de un canal '
            u'universitario y el nivel est&aacute; por encima del de clase: m&iacute;ralo para fijar el '
            u'vocabulario, no para aprender de cero.')) +

  bloque('02', u'Pr&aacute;ctica &middot; 25 min', ficha(
    u'Actividad 7.4 &middot; Elegir un sensor con la cuenta hecha',
    [u'6.1'], u'Parejas &middot; 25 min &middot; sobre 10', u'''
          <h4>El encargo</h4>
          <p>El instituto quiere que un ordenador vigile el <b>invernadero</b> y avise si la temperatura
             se sale de lo normal. Hay que elegir con qu&eacute; finura se mide, y se elige
             <b>calculando</b>, no opinando.</p>
          <div class="copiar">
            <h4>El sensor que os han dado</h4>
            <table>
              <tr><th>Dato</th><th>Valor</th></tr>
              <tr><td>Tensi&oacute;n que da a 0&nbsp;&deg;C</td><td>0 V</td></tr>
              <tr><td>Tensi&oacute;n que da a 50&nbsp;&deg;C</td><td>5 V</td></tr>
              <tr><td>Entre esos dos puntos</td><td>proporcional</td></tr>
            </table>
          </div>
          <h4>Qu&eacute; hay que hacer</h4>
          <ol class="pasos">
            <li>&iquest;Cu&aacute;ntos <b>grados por voltio</b> da este sensor?</li>
            <li>Lo conect&aacute;is a un conversor de <b>8 bits</b>. Calculad cu&aacute;ntos valores
                distintos puede dar, <b>cu&aacute;ntos voltios</b> mide cada escal&oacute;n y, sobre todo,
                <b>a cu&aacute;ntos grados</b> equivale ese escal&oacute;n. Comprobadlo con la escena de
                arriba antes de seguir.</li>
            <li>Os piden distinguir <b>d&eacute;cimas de grado</b>. &iquest;Cu&aacute;ntos escalones hacen
                falta en los 50&nbsp;&deg;C? &iquest;Y cu&aacute;ntos <b>bits</b>? Probad con 8 y con 9
                y decid cu&aacute;l es el primero que vale.</li>
            <li>Ahora el muestreo. Decid <b>cu&aacute;ntas veces por segundo</b> hay que medir la
                temperatura de un invernadero, y cu&aacute;ntas habr&iacute;a que medir el sonido de un
                micr&oacute;fono. Justificadlo con una sola idea: <b>&iquest;cu&aacute;nto puede cambiar
                eso mientras no miras?</b></li>
            <li>Con <b>16 bits</b> (2 bytes por medida) calculad lo que ocupa un d&iacute;a entero
                midiendo <b>una vez por minuto</b>, y lo que ocupar&iacute;a midiendo <b>mil veces por
                segundo</b>. Pasad el segundo a MB. Escribid una frase: medir de m&aacute;s no es
                &laquo;por si acaso&raquo;, &iquest;qu&eacute; es?</li>
            <li>Haced una tabla con <b>ocho aparatos</b> del aula. Para cada uno: si es de
                <b>entrada</b>, de <b>salida</b> o <b>mixto</b>, y <b>por qu&eacute; puerto</b> se
                conecta. Al menos uno tiene que ser mixto, y hay que explicar por qu&eacute; lo es.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Los grados por voltio est&aacute;n bien <b>(1 punto)</b>.</li>
            <li>La cuenta de los 8 bits llega hasta los <b>grados</b>, no se queda en los voltios
                <b>(2 puntos)</b>.</li>
            <li>El n&uacute;mero de bits para la d&eacute;cima de grado est&aacute; justificado con la
                cuenta de escalones <b>(2 puntos)</b>.</li>
            <li>Las dos frecuencias de muestreo se razonan por lo que puede cambiar la magnitud, no
                &laquo;porque el sonido es m&aacute;s r&aacute;pido&raquo; <b>(2 puntos)</b>.</li>
            <li>Las dos cuentas de tama&ntilde;o est&aacute;n bien y con unidades <b>(2 puntos)</b>.</li>
            <li>La tabla de los ocho aparatos distingue bien el mixto <b>(1 punto)</b>.</li>
          </ul>
          <div class="nota" style="margin-top:14px">
            <span class="n-tag">Pista para el paso 3</span>
            Ojo con una trampa: <b>256 valores no son 256 escalones</b>. Si pon&eacute;is los dos
            extremos de la escala, entre ellos quedan <b>255</b>. Con 4 dedos hay 3 huecos.
          </div>
  ''')) +

  bloque('03', u'Cierre &middot; 5 min', u'''
      <ol>
      ''' + pregunta(u'&iquest;Por qu&eacute; una foto o una canci&oacute;n guardadas en un ordenador no son <b>exactamente</b> lo que hab&iacute;a fuera?',
                     u'<p>Porque el mundo cambia de forma continua y la m&aacute;quina solo sabe anotar valores contados. Se mira <b>cada cierto tiempo</b> (muestreo) y cada medida se redondea al <b>escal&oacute;n</b> m&aacute;s cercano (cuantificaci&oacute;n). Lo que se pierde entre medida y medida, y al redondear, ya no vuelve.</p>')
        + pregunta(u'Un conversor de 8 bits y otro de 16 miden el mismo sensor. &iquest;Qu&eacute; cambia?',
                   u'<p>El de 8 bits reparte la escala en 255 escalones y el de 16, en 65.535: los escalones del segundo son unas <b>257 veces m&aacute;s finos</b>, as&iacute; que se equivoca mucho menos. A cambio, cada medida ocupa <b>2 bytes en vez de 1</b>. Fidelidad y tama&ntilde;o van siempre juntos.</p>')
        + pregunta(u'Una pantalla t&aacute;ctil, &iquest;es perif&eacute;rico de entrada o de salida?',
                   u'<p>Las dos cosas: es <b>mixto</b>. Como pantalla saca informaci&oacute;n (salida) y como superficie t&aacute;ctil mete d&oacute;nde has puesto el dedo (entrada). Lo mismo pasa con una memoria USB, de la que se lee y en la que se escribe.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        La informaci&oacute;n entra y sale, eso est&aacute; visto. Ahora mira el ordenador que
        tienes delante: hay <b>una</b> CPU, <b>una</b> memoria, <b>un</b> disco y <b>un</b> teclado, y hay
        doscientos programas abiertos queriendo las cuatro cosas <b>a la vez</b>. No se pelean nunca.
        &iquest;Qui&eacute;n reparte?
      </div>
  '''))


# ==========================================================================
# SESION 5 · El sistema operativo
# ==========================================================================
S5 = (
  bloque('00', u'Reto inicial &middot; 10 min', u'''
      <p>Empieza mirando, no leyendo. En el equipo del aula abre el administrador de tareas o el monitor
         del sistema y <b>cuenta los procesos</b>. Van a salir decenas, y en Windows m&aacute;s de cien
         &mdash;marca la casilla de ver los de todos los usuarios y crecen otra vez&mdash;. Ahora mira
         cu&aacute;ntos n&uacute;cleos tiene el procesador: cuatro, con suerte ocho.</p>

      <div class="aviso">
        <span class="n-tag">El encargo</span>
        Sois <b>doscientos</b> y hay <b>cuatro sillas</b>. Escribe las <b>reglas</b> del reparto: qui&eacute;n
        se sienta, cu&aacute;nto rato, qui&eacute;n decide y qu&eacute; pasa si uno no quiere levantarse.
      </div>

      <p>Las reglas que escribe todo el mundo la primera vez son estas tres. Y las tres se rompen por el
         mismo sitio:</p>
      <ul>
        <li><b>&laquo;Que cada uno avise cuando termine&raquo;.</b> Basta con que <b>uno</b> no avise
            &mdash;porque se ha colgado, o porque est&aacute; mal escrito&mdash; para que la m&aacute;quina
            entera se quede muerta. Y no es un cuento: los ordenadores <b>personales</b> funcionaron
            as&iacute; hasta los a&ntilde;os noventa, y por eso se colgaban enteros y hab&iacute;a que
            apagarlos a lo bruto.</li>
        <li><b>&laquo;Que cada uno coja la memoria que necesite&raquo;.</b> Dos programas eligen el mismo
            hueco y se machacan los datos el uno al otro. Nadie ha hecho nada mal y los dos fallan.</li>
        <li><b>&laquo;Que cada uno escriba en el disco donde quiera&raquo;.</b> Uno escribe encima de los
            ficheros de otro. O de los tuyos.</li>
      </ul>

      <div class="reto-piensa">
        <span class="n-tag">Lo que falla en las tres</span>
        <p>En las tres est&aacute;s <b>pidiendo que se porten bien</b>. &iquest;Y si uno no quiere? &iquest;Y
           si uno simplemente est&aacute; roto? Un reparto que solo funciona cuando todos colaboran
           <b>no es un reparto</b>: es un deseo.</p>
      </div>

      <p>As&iacute; que hace falta alguien que no pida por favor: que pueda <b>quitar</b> la CPU a un
         programa aunque no quiera soltarla, que <b>impida</b> tocar la memoria del vecino y que sea el
         <b>&uacute;nico</b> que toca el disco. Ese alguien es tambi&eacute;n un programa &mdash;no hay
         magia&mdash;, pero manda sobre los dem&aacute;s: es el <b>sistema operativo</b>.</p>
  ''') +

  bloque('01', u'Teor&iacute;a &middot; 20 min', u'''
      <h3>Repartir la CPU: el turno</h3>
      <p>La escena de abajo reparte una sola CPU entre cinco programas. Los tiempos que salen no
         est&aacute;n escritos: se calculan simulando el reparto, turno a turno. Mira <b>las dos cifras a
         la vez</b>, la de tu tecla y la del porcentaje, y busca el turno que las deje bien a las dos.
         Spoiler: no existe.</p>

''' + ESCENA_PLAN + u'''
      <div class="copiar">
        <h4>El planificador</h4>
        <p><b>Proceso</b>: un programa que se est&aacute; ejecutando, con su trozo de memoria y una anotaci&oacute;n
           de por d&oacute;nde iba.</p>
        <p>El <b>planificador</b> del sistema operativo le da a cada proceso un <b>turno</b> de unos pocos
           milisegundos y, cuando se acaba, <b>se lo quita</b> aunque no haya terminado. Eso se llama
           <b>multitarea con desalojo</b>.</p>
        <p>Como los turnos son cort&iacute;simos, parece que todos los programas van a la vez. <b>No van a
           la vez</b>: van por turnos, muy deprisa.</p>
        <p>Cambiar de programa <b>cuesta tiempo</b>: hay que guardar por d&oacute;nde iba uno y recuperar
           por d&oacute;nde iba el otro. Turnos m&aacute;s cortos responden antes y gastan m&aacute;s
           m&aacute;quina en cambiar.</p>
      </div>

      <div class="nota">
        <span class="n-tag">Y los n&uacute;cleos, entonces</span>
        Un procesador de <b>cuatro n&uacute;cleos</b> s&iacute; hace cuatro cosas a la vez de verdad: son
        cuatro CPU en la misma pastilla. Lo que no cambia es el problema: con 200 procesos y 4
        n&uacute;cleos siguen sobrando 196, y hay que repartir igual. Cuatro sillas, no doscientas.
      </div>

      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; no hace falta copiarlo</span>
        <p><b>20 de julio de 1969</b>, m&oacute;dulo lunar del Apolo 11, a unos minutos de posarse. El
           ordenador de a bordo empieza a dar una alarma: <b>1202</b>. Luego otra, 1201. Significan que
           <b>se ha quedado sin sitio para tanto trabajo</b>: un radar que no hac&iacute;a falta en ese
           momento le estaba robando alrededor del <b>13 %</b> del tiempo de c&aacute;lculo.</p>
        <p>Un ordenador normal de la &eacute;poca se habr&iacute;a colgado, y con &eacute;l el
           alunizaje. Este no, porque su reparto estaba hecho <b>por prioridades</b>: al ver que no
           llegaba, tir&oacute; por la borda las tareas menos importantes, se reinici&oacute; y
           sigui&oacute; calculando lo &uacute;nico que no pod&iacute;a fallar, que era guiar la nave.
           Desde tierra dieron el &laquo;go&raquo; y aterrizaron.</p>
        <p>El programa lo hab&iacute;a escrito el equipo de <b>Margaret Hamilton</b> en el MIT. Lo que
           salv&oacute; el alunizaje no fue un ordenador m&aacute;s potente: fue haber decidido antes
           <b>qu&eacute; se tira cuando no se llega</b>. Eso es exactamente lo que hace el planificador de
           la escena de arriba, solo que en tu mesa nadie se estrella.</p>
      </div>

''' + foto('u7-hamilton.jpg',
           u'Margaret Hamilton de pie junto a una pila de listados de programa impresos tan alta como ella',
           u'<b>Margaret Hamilton</b>, 1969, junto a los listados del programa de vuelo del Apolo que '
           u'dirigi&oacute; su equipo en el MIT. Todo eso son instrucciones, impresas. Ella fue quien '
           u'empez&oacute; a llamar <b>ingenier&iacute;a de software</b> a lo que hac&iacute;an, cuando '
           u'nadie se tomaba en serio que escribir programas fuera ingenier&iacute;a.',
           u'Restauraci&oacute;n de Adam Cuerden sobre foto del MIT', u'Dominio p&uacute;blico',
           u'https://commons.wikimedia.org/wiki/File:Margaret_Hamilton_-_restoration.jpg') +
    foto('u7-dsky.jpg',
         u'Panel DSKY del ordenador del Apolo: luces de aviso a la izquierda, un visor num&eacute;rico arriba a la derecha y un teclado de cifras con teclas VERB y NOUN',
         u'El <b>DSKY</b>, la pantalla y el teclado del ordenador del Apolo. En ese visor de la derecha es '
         u'donde apareci&oacute; el <b>1202</b>. F&iacute;jate en lo que hay: n&uacute;meros y nada '
         u'm&aacute;s. Todo el perif&eacute;rico de entrada y salida de un ordenador que llev&oacute; '
         u'gente a la Luna cabe en esta placa.',
         u'Arnold Reinhold (Computer History Museum)', u'CC BY-SA 4.0',
         u'https://commons.wikimedia.org/wiki/File:Apollo_DSKY_CHM.agr.jpg') + u'''
      <h3>Repartir la memoria: cada uno en su sitio</h3>
      <div class="copiar">
        <h4>Memoria separada</h4>
        <p>El sistema operativo le da a cada proceso <b>su propio trozo de RAM</b> y, con ayuda del
           hardware, <b>impide</b> que toque el de los dem&aacute;s. Un programa que se sale de lo suyo no
           rompe nada ajeno: el sistema <b>lo cierra a &eacute;l</b> y los dem&aacute;s siguen.</p>
        <p>Por eso hoy se cierra <b>una</b> aplicaci&oacute;n y el resto sigue. Antes de que esto
           existiera, un fallo en cualquier programa se llevaba por delante el ordenador entero.</p>
      </div>

      <h3>Repartir el disco: ficheros, carpetas y permisos</h3>
      <div class="copiar">
        <h4>C&oacute;mo se organiza lo guardado</h4>
        <p><b>Fichero</b>: una tira de bytes con un nombre. Nada m&aacute;s.</p>
        <p><b>Carpeta</b>: un fichero especial que contiene una lista de nombres. Por eso se pueden meter
           unas dentro de otras.</p>
        <p><b>Ruta</b>: el camino completo hasta un fichero, carpeta a carpeta
           (<i>Documentos / tema7 / pruebas / notas.txt</i>).</p>
        <p><b>Permisos</b>: para cada fichero, qui&eacute;n puede <b>leerlo</b>, qui&eacute;n puede
           <b>escribirlo</b> y qui&eacute;n puede <b>ejecutarlo</b>. Es lo que evita que un alumno borre
           el sistema o lea el trabajo de otro.</p>
      </div>

      <div class="nota">
        <span class="n-tag">La extensi&oacute;n no es el fichero</span>
        El <b>.jpg</b> del final del nombre no hace que algo sea una foto: es solo una <b>pista</b> para
        que el sistema sepa <b>con qu&eacute; programa</b> abrirlo, es decir, <b>qu&eacute; acuerdo</b> aplicar
        &mdash;la misma palabra de la sesi&oacute;n 3&mdash;. Cambiarle el nombre a <b>.txt</b> no
        convierte la foto en texto; lo &uacute;nico que consigue es que la abra el programa equivocado y
        salga basura. Lo vas a comprobar en la pr&aacute;ctica.
      </div>

      <h3>Y esconderlo todo</h3>
      <p>Falta el trabajo m&aacute;s invisible. Tu programa de dibujo no sabe nada de tu impresora, ni
         falta que le haga: le pide al sistema operativo &laquo;imprime esto&raquo; y el sistema, a
         trav&eacute;s del <b>controlador</b> (el <i>driver</i>) de ese modelo concreto, se entiende con
         ella. Ah&iacute; est&aacute; enganchada la sesi&oacute;n anterior: <b>el sistema operativo es
         quien habla con los perif&eacute;ricos</b>, y por eso puedes cambiar de impresora sin cambiar de
         programas.</p>

      <div class="copiar">
        <h4>Qu&eacute; hace un sistema operativo</h4>
        <ol>
          <li><b>Arrancar</b> la m&aacute;quina y dejarla lista.</li>
          <li><b>Repartir la CPU</b> entre los procesos, por turnos.</li>
          <li><b>Repartir la memoria</b> y que nadie toque la del vecino.</li>
          <li><b>Gestionar ficheros</b>, carpetas y permisos.</li>
          <li><b>Hablar con los perif&eacute;ricos</b> a trav&eacute;s de los controladores.</li>
          <li><b>Dar una interfaz</b> para que t&uacute; solo tengas que pulsar un icono.</li>
        </ol>
        <p>Ejemplos: Windows, macOS, <b>GNU/Linux</b> (el de eduAndos), Android, iOS.</p>
      </div>

''' + video('video-so', 'vnJCudAed08',
            u'Microaprendizaje: &iquest;Qu&eacute; es un sistema operativo?',
            u'Educar Portal &middot; en espa&ntilde;ol',
            u'Un repaso corto de las funciones que acabas de copiar, por si alguna se ha quedado a '
            u'medias.')) +

  bloque('02', u'Pr&aacute;ctica &middot; 25 min', ficha(
    u'Actividad 7.5 &middot; Destripar el equipo del aula',
    [u'6.1'], u'Parejas &middot; 25 min &middot; sobre 10', u'''
          <div class="aviso">
            <span class="n-tag">Antes de tocar nada</span>
            <b>No se cierra ning&uacute;n proceso</b>, <b>no se borra nada</b> y <b>no se usa la
            contrase&ntilde;a de administrador</b>. Cerrar un proceso del sistema al azar puede dejar el
            equipo inservible hasta que se reinicie, y el paso 6 est&aacute; pensado precisamente para
            que os <b>digan que no</b>.
          </div>
          <h4>C&oacute;mo se abre el monitor</h4>
          <p>En Windows, <b>Ctrl + May&uacute;s + Esc</b>. En GNU/Linux, <i>Monitor del sistema</i>. En
             ChromeOS, <b>Buscar + Esc</b>. Anotad cu&aacute;l hab&eacute;is usado.</p>
          <h4>Qu&eacute; hay que hacer</h4>
          <ol class="pasos">
            <li>Con nada abierto, anotad tres cifras: <b>cu&aacute;ntos procesos</b> hay, <b>qu&eacute; %
                de CPU</b> se est&aacute; usando y <b>cu&aacute;nta RAM</b> hay ocupada del total.
                &iquest;Cuadra con lo que esperabais de una m&aacute;quina &laquo;parada&raquo;?</li>
            <li>Ordenad la lista <b>por memoria</b>. Copiad los <b>cinco primeros</b> con lo que ocupa
                cada uno, sumadlos y calculad <b>qu&eacute; porcentaje</b> de la RAM total son. Se&ntilde;alad
                el que m&aacute;s os sorprenda y decid por qu&eacute;.</li>
            <li>Abrid <b>diez pesta&ntilde;as</b> del navegador y volved a mirar la RAM ocupada. Calculad
                <b>cu&aacute;nto ha subido</b> y <b>cu&aacute;nto por pesta&ntilde;a</b>. Comparadlo con
                los 0,35&nbsp;GB por pesta&ntilde;a que daba la actividad 7.2: &iquest;se parece a lo
                que gasta este equipo?</li>
            <li>En vuestra carpeta personal cread el &aacute;rbol <b>tema7 / pruebas /</b> y dentro un
                fichero de texto con una frase vuestra. Anotad su <b>ruta completa</b> y su
                <b>tama&ntilde;o en bytes</b>. Contad las letras de la frase: &iquest;cu&aacute;ntos bytes
                sale por letra? &iquest;Cuadra con la sesi&oacute;n 3?</li>
            <li>Copiad una foto a esa carpeta, cambiadle la extensi&oacute;n a <b>.txt</b> y abridla con
                el editor de texto. Copiad en el cuaderno las <b>tres primeras l&iacute;neas</b> de lo que
                salga y explicad <b>por qu&eacute;</b> sale eso usando la palabra <b>acuerdo</b>.</li>
            <li>Buscad un fichero del sistema (en <i>C:\\Windows</i> o en <i>/usr/bin</i>), mirad sus
                <b>permisos</b> e intentad borrarlo. <b>Aceptad el no.</b> Copiad el mensaje exacto y
                contestad: &iquest;qui&eacute;n lo est&aacute; impidiendo y para proteger a qui&eacute;n?</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Las tres cifras del paso 1 est&aacute;n anotadas con sus unidades <b>(1 punto)</b>.</li>
            <li>La suma de los cinco y el porcentaje est&aacute;n bien <b>(2 puntos)</b>.</li>
            <li>La medida de las pesta&ntilde;as se compara de verdad con la estimaci&oacute;n anterior
                <b>(2 puntos)</b>.</li>
            <li>La ruta es <b>completa</b> y la cuenta de bytes por letra est&aacute; explicada
                <b>(2 puntos)</b>.</li>
            <li>La explicaci&oacute;n del fichero renombrado usa bien la idea de acuerdo y no dice que
                &laquo;se ha roto&raquo; <b>(2 puntos)</b>.</li>
            <li>La respuesta sobre los permisos dice qui&eacute;n lo impide <b>(1 punto)</b>.</li>
          </ul>
          <div class="nota" style="margin-top:14px">
            <span class="n-tag">Aviso sobre el paso 5</span>
            La foto <b>no se estropea</b>: sigue siendo exactamente los mismos bytes. Devolvedle la
            extensi&oacute;n <b>.jpg</b> al terminar y comprobad que se abre igual que antes. Eso es
            parte de la respuesta.
          </div>
  ''')) +

  bloque('03', u'Cierre &middot; 5 min', u'''
      <ol>
      ''' + pregunta(u'Tienes cuarenta programas abiertos y un procesador de cuatro n&uacute;cleos. &iquest;Van los cuarenta a la vez?',
                     u'<p>No. Van <b>cuatro</b> a la vez de verdad, y los cuarenta se turnan en esos cuatro sitios con turnos de unos pocos milisegundos. Lo parece porque los turnos son tan cortos que el ojo no los distingue.</p>')
        + pregunta(u'&iquest;Por qu&eacute; no vale con pedir a cada programa que suelte la CPU cuando termine?',
                   u'<p>Porque basta con que <b>uno</b> no la suelte &mdash;por un fallo o por estar mal escrito&mdash; para colgar la m&aacute;quina entera. El sistema operativo <b>se la quita</b>, no se la pide. Ese es todo el invento.</p>')
        + pregunta(u'Renombras <i>gato.jpg</i> como <i>gato.txt</i>. &iquest;Qu&eacute; ha cambiado dentro del fichero?',
                   u'<p><b>Nada en absoluto</b>: son los mismos bytes en el mismo orden. Lo &uacute;nico que has cambiado es la <b>pista</b> que le das al sistema sobre qu&eacute; acuerdo usar para leerlo, as&iacute; que lo abre el programa equivocado y sale basura. Es el mismo byte con otra lectura, otra vez.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        El mapa est&aacute; entero: una m&aacute;quina que obedece listas, dos memorias, ceros y unos,
        perif&eacute;ricos que traducen y un sistema que lo reparte. La &uacute;ltima sesi&oacute;n es la
        que vas a usar de verdad fuera de clase: <b>una de esas piezas falla y hay que averiguar
        cu&aacute;l</b>, sin tocar cosas al azar y sin gastarse un euro de m&aacute;s.
      </div>
  '''))


# ==========================================================================
# SESION 6 · Diagnosticar una averia
# ==========================================================================
PREGUNTAS_TEST = [
 dict(p=u'&iquest;Por qu&eacute; se dice que un ordenador es una m&aacute;quina de <b>prop&oacute;sito '
        u'general</b>?',
      op=[u'porque lleva muchos componentes distintos dentro',
          u'porque la m&aacute;quina es siempre la misma y lo que cambia es la lista de instrucciones',
          u'porque sirve para trabajar y para jugar'],
      ok=1,
      por=u'Es la idea que abre el tema. El comportamiento no est&aacute; <b>en los cables</b>, est&aacute; '
          u'<b>escrito</b>; por eso el mismo aparato hace hoy una cosa y ma&ntilde;ana otra sin coger el '
          u'soldador.'),
 dict(p=u'Un procesador de <b>3 GHz</b> hace cada segundo&hellip;',
      op=[u'3.000 millones de instrucciones',
          u'3.000 millones de pulsos de reloj, que no es lo mismo',
          u'3.000 millones de operaciones de memoria'],
      ok=1,
      por=u'Los gigahercios miden el <b>ritmo</b>, no el trabajo. Hay instrucciones que gastan varios '
          u'pulsos y procesadores que resuelven varias a la vez, as&iacute; que de la frecuencia sola no '
          u'se deduce cu&aacute;nto rinde.'),
 dict(p=u'Se va la luz de golpe. Pierdes lo que llevabas escrito, pero el fichero de ayer sigue ah&iacute;. '
        u'&iquest;Por qu&eacute;?',
      op=[u'porque el disco guarda copias de seguridad autom&aacute;ticas',
          u'porque lo de hoy estaba en la RAM, que es vol&aacute;til, y lo de ayer en el almacenamiento, '
          u'que no lo es',
          u'porque el procesador no ha tenido tiempo de terminar'],
      ok=1,
      por=u'La <b>RAM</b> necesita corriente para acordarse y al cortarla se borra entera. <i>Guardar</i> '
          u'es exactamente eso: copiar de la mesa a la estanter&iacute;a.'),
 dict(p=u'Tu ordenador se arrastra con quince pesta&ntilde;as, y en el disco te sobran 800 GB. '
        u'&iquest;Qu&eacute; compras?',
      op=[u'un disco m&aacute;s grande, que nunca sobra',
          u'm&aacute;s memoria RAM, que es lo que se ha llenado',
          u'un procesador m&aacute;s r&aacute;pido'],
      ok=1,
      por=u'Lo que se llena es la <b>mesa</b>, no la estanter&iacute;a. Cuando no cabe, el sistema empieza '
          u'a bajar cosas al disco y a subirlas, y cada viaje cuesta <b>miles de veces m&aacute;s</b>. '
          u'Sobrar disco no ayuda en nada.'),
 dict(p=u'Con <b>8 interruptores</b> salen 256 combinaciones. &iquest;Por qu&eacute; ese n&uacute;mero?',
      op=[u'porque 8 &times; 32 = 256',
          u'porque cada interruptor dobla las posibilidades del anterior: 2<sup>8</sup>',
          u'porque es el n&uacute;mero de letras de la tabla ASCII'],
      ok=1,
      por=u'Cada bit que a&ntilde;ades <b>multiplica por dos</b> lo que hab&iacute;a. Con 8 bits van del 0 '
          u'al 255, que son 256 valores contando el cero.'),
 dict(p=u'El byte <b>0100 0001</b>, &iquest;qu&eacute; significa?',
      op=[u'el n&uacute;mero 65, siempre',
          u'la letra A, siempre',
          u'depende del acuerdo con el que se lea: puede ser 65, la A o un gris oscuro'],
      ok=2,
      por=u'Un byte por s&iacute; solo <b>no significa nada</b>. Es el programa que lo abre quien aplica un '
          u'acuerdo u otro, y por eso una foto abierta con un editor de texto sale como basura.'),
 dict(p=u'Mides un sensor con un conversor de 4 bits y luego con uno de 8. &iquest;Qu&eacute; ha mejorado?',
      op=[u'mide m&aacute;s veces por segundo',
          u'los escalones son mucho m&aacute;s finos, as&iacute; que se equivoca menos al anotar cada medida',
          u'no pierde informaci&oacute;n: la copia pasa a ser exacta'],
      ok=1,
      por=u'M&aacute;s bits es <b>cuantificaci&oacute;n</b> m&aacute;s fina: 255 escalones en vez de 15. '
          u'Cu&aacute;ntas veces se mide es otra cosa, el <b>muestreo</b>. Y exacta no es nunca: el error '
          u'se reduce, no desaparece.'),
 dict(p=u'Un motor que mueve la rueda de un robot es&hellip;',
      op=[u'un sensor, porque lo controla el ordenador',
          u'un actuador: convierte una orden el&eacute;ctrica en algo que pasa en el mundo',
          u'un perif&eacute;rico mixto'],
      ok=1,
      por=u'Los <b>sensores</b> meten el mundo en la m&aacute;quina y los <b>actuadores</b> lo sacan. Un '
          u'robot es exactamente eso: sensores, un programa que decide y actuadores.'),
 dict(p=u'&iquest;Por qu&eacute; el sistema operativo <b>quita</b> la CPU a un programa en vez de '
        u'ped&iacute;rsela?',
      op=[u'para que los programas no se hagan demasiado grandes',
          u'porque si dependiera de que cada uno la suelte, bastar&iacute;a uno colgado para parar la '
          u'm&aacute;quina entera',
          u'porque as&iacute; gasta menos bater&iacute;a'],
      ok=1,
      por=u'Un reparto que solo funciona si todos colaboran no es un reparto. Con el turno impuesto, un '
          u'programa colgado se lleva por delante <b>solo a s&iacute; mismo</b>.'),
 dict(p=u'Un ordenador no arranca y sospechas de siete piezas encadenadas. &iquest;Cu&aacute;l es la '
        u'primera prueba?',
      op=[u'la de la pieza m&aacute;s barata de cambiar',
          u'la que parta la cadena por la mitad, porque descarta la mitad conteste lo que conteste',
          u'la primera de la cadena, e ir avanzando una a una'],
      ok=1,
      por=u'Mirando de una en una puedes gastar seis pruebas; partiendo por la mitad bastan <b>tres</b>, '
          u'y siempre. Con mil piezas ser&iacute;an mil frente a diez: por eso no es un truco, es el '
          u'm&eacute;todo.'),
]

S6 = (
  bloque('00', u'Reto inicial &middot; 10 min', u'''
      <p>Entras en el aula 12 y te dicen esto, literal:</p>
      <div class="aviso">
        <span class="n-tag">El parte de aver&iacute;a</span>
        &laquo;El ordenador <b>no va</b>.&raquo;
      </div>
      <p>Tienes dos minutos y el cuaderno. Escribe <b>qu&eacute; haces primero</b>. Sin leer lo de abajo.</p>

      <p>Lo que se escribe casi siempre, y por qu&eacute; ninguna de las cuatro sirve:</p>
      <ul>
        <li><b>&laquo;Reiniciar&raquo;.</b> A veces funciona, y eso es lo peor que te puede pasar:
            funciona y <b>no sabes por qu&eacute;</b>, as&iacute; que volver&aacute; el jueves.</li>
        <li><b>&laquo;Reinstalar el sistema&raquo;.</b> Tres horas de trabajo para arreglar, quiz&aacute;,
            un cable suelto que costaba cero euros y diez segundos.</li>
        <li><b>&laquo;Cambiar la pieza que yo creo&raquo;.</b> Si aciertas es suerte; si no, has cambiado
            una pieza que estaba buena y sigues igual, pero con menos dinero.</li>
        <li><b>&laquo;Mirarlo todo&raquo;.</b> No tienes toda la tarde, y en un taller esa tarde se cobra.</li>
      </ul>

      <div class="reto-piensa">
        <span class="n-tag">D&oacute;nde est&aacute; la trampa</span>
        <p>&laquo;No va&raquo; <b>no es un s&iacute;ntoma</b>: es la falta de informaci&oacute;n. La
           primera pregunta de quien sabe reparar no es <i>&iquest;qu&eacute; cambio?</i>, es
           <b>&iquest;qu&eacute; es exactamente lo que no va?</b></p>
      </div>

      <p>Hoy no se aprende ninguna pieza nueva: ya las conoces todas. Se aprende un <b>m&eacute;todo</b>,
         que es lo &uacute;nico que sigue sirviendo cuando la aver&iacute;a es de un aparato que no
         hab&iacute;as visto nunca.</p>
  ''') +

  bloque('01', u'Teor&iacute;a &middot; 15 min', u'''
      <h3>El s&iacute;ntoma no es la aver&iacute;a</h3>
      <div class="copiar">
        <h4>Dos palabras que no son lo mismo</h4>
        <p><b>S&iacute;ntoma</b>: lo que se ve. &laquo;La pantalla est&aacute; negra.&raquo;</p>
        <p><b>Causa</b>: lo que hay que arreglar. El cable de v&iacute;deo, la fuente, la RAM&hellip;</p>
        <p>Un mismo s&iacute;ntoma puede venir de <b>muchas</b> causas, y una misma causa puede dar
           s&iacute;ntomas distintos. Por eso no se puede ir del s&iacute;ntoma a la pieza de un salto:
           hay que <b>acotar</b>.</p>
      </div>

      <h3>Un ordenador no es una caja: es una cadena</h3>
      <p>Abre el equipo con la mirada antes que con el destornillador. Cada pieza <b>necesita que
         funcione la anterior</b>: sin corriente no hay fuente, sin fuente no hay placa, sin placa no se
         lee la RAM, sin RAM no arranca el sistema y sin sistema no hay programa.</p>

''' + foto('u7-pc-dentro.jpg',
           u'Interior de una torre de ordenador con la fuente de alimentaci&oacute;n arriba, la placa base con el ventilador del procesador, un m&oacute;dulo de RAM, cables de colores y un disco duro abajo a la derecha',
           u'Se&ntilde;ala la cadena en la foto antes de seguir: arriba a la izquierda la <b>fuente de '
           u'alimentaci&oacute;n</b> con sus cables de colores; en el centro la <b>placa base</b> con el '
           u'ventilador del procesador encima; a su derecha, de canto, el m&oacute;dulo de <b>RAM</b>; y '
           u'abajo a la derecha el <b>disco</b>. Todo lo del tema est&aacute; en esta foto.',
           u'DmitroCzegovets', u'CC BY 4.0',
           u'https://commons.wikimedia.org/wiki/File:Computer_2008_inside.jpg') + u'''
      <p>En la escena hay una pieza rota, y no sabes cu&aacute;l. Tampoco vas a abrir nada: solo puedes
         <b>preguntarle a la m&aacute;quina</b>. Prueba primero como saldr&iacute;a de forma natural, de
         la 1 a la 6, y luego vuelve a intentarlo <b>empezando por la 4</b>. Mira el contador de
         sospechosos en las dos.</p>

''' + ESCENA_DIAG + u'''
      <div class="copiar">
        <h4>Acotar</h4>
        <p><b>Acotar</b> es reducir el n&uacute;mero de sospechosos con cada prueba, en vez de adivinar.</p>
        <p>La cadena de arranque, en orden: <b>corriente &rarr; fuente &rarr; placa y CPU &rarr; RAM
           &rarr; disco &rarr; sistema operativo &rarr; aplicaci&oacute;n</b>.</p>
        <p>Una prueba <b>buena</b> es la que <b>parte la cadena por la mitad</b>: conteste lo que
           conteste, te quita la mitad de los sospechosos. Una prueba mala es la que solo descarta uno.</p>
      </div>

      <div class="nota">
        <span class="n-tag">Y esto no es un truco, es una cuenta</span>
        Con <b>siete</b> piezas, mirando de una en una puedes gastar <b>seis</b> pruebas; partiendo por la
        mitad bastan <b>tres</b>, siempre. La diferencia parece poca hasta que crece el problema: con
        <b>mil</b> piezas ser&iacute;an <b>mil</b> pruebas frente a <b>diez</b>. Cada prueba que parte por
        la mitad <b>dobla</b> lo que puedes abarcar, igual que cada bit doblaba las combinaciones en la
        sesi&oacute;n 3. Es la misma cuenta.
      </div>

      <h3>Las cuatro reglas que no se saltan</h3>
      <div class="copiar">
        <h4>C&oacute;mo se busca una aver&iacute;a</h4>
        <ol>
          <li><b>Pregunta y reproduce.</b> Qu&eacute; estabas haciendo, desde cu&aacute;ndo pasa, si pasa
              <b>siempre</b> o a veces. Una aver&iacute;a que no sabes provocar no sabr&aacute;s si la has
              arreglado.</li>
          <li><b>Cambia una sola cosa cada vez.</b> Si cambias tres y empieza a ir, no sabes cu&aacute;l
              era, y las otras dos las has cambiado para nada.</li>
          <li><b>Deshaz lo que no era.</b> Vuelve a dejarlo como estaba antes de probar otra cosa.</li>
          <li><b>An&oacute;talo.</b> Qu&eacute; has probado y qu&eacute; ha salido. Sin eso repites pruebas
              y te enga&ntilde;as.</li>
        </ol>
      </div>

      <div class="nota">
        <span class="n-tag">La trampa de la pantalla</span>
        Si no hay imagen <b>no sabes nada</b> de lo que pasa dentro: la m&aacute;quina puede estar
        arrancando perfectamente y todos los s&iacute;ntomas se ven igual, negros. Por eso lo primero que
        se descarta es <b>lo que te impide ver</b>: el monitor, su cable y la entrada elegida. Es la rama
        que la escena deja fuera <b>a prop&oacute;sito</b>, porque en la vida real es la que m&aacute;s
        confunde.
      </div>

      <h3>La pregunta que m&aacute;s acota de todas</h3>
      <p>Y es gratis, de la sesi&oacute;n 1: <b>&iquest;falla en todo o solo en un sitio?</b> Si el
         teclado no escribe en <b>ning&uacute;n</b> programa, el problema est&aacute; abajo &mdash;el
         perif&eacute;rico, su cable o el sistema&mdash;. Si escribe en todos menos en uno, est&aacute;
         arriba: es <b>software</b> de esa aplicaci&oacute;n. Con una sola pregunta has partido el
         ordenador en dos.</p>

      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; no hace falta copiarlo</span>
        <p><b>9 de septiembre de 1947</b>, Universidad de Harvard. El ordenador Mark II se equivoca. Se
           ponen a acotar, llegan al panel F, abren el <b>rel&eacute; 70</b> y encuentran dentro una
           <b>polilla</b> aplastada. La pegan con cinta adhesiva en el cuaderno de
           incidencias y escriben al lado: <i>&laquo;primer caso real de encontrar un bicho&raquo;</i>. La
           p&aacute;gina se conserva.</p>
        <p>Cuidado con el remate f&aacute;cil: <b>la palabra ya exist&iacute;a</b>. Los ingenieros
           llamaban <i>bugs</i> a los fallos desde los tiempos de Edison, casi setenta a&ntilde;os antes. Lo
           que tiene gracia de aquella anotaci&oacute;n es justo lo contrario de lo que se cuenta: que
           por una vez el bicho <b>era un bicho</b>. Y que para dar con &eacute;l hicieron lo mismo que
           has hecho t&uacute; en la escena: ir cerrando el cerco hasta un rel&eacute; concreto.</p>
      </div>

''' + video('video-diag', 'pMG7x0XnCU8',
            u'C&oacute;mo diagnosticar problemas en mi PC',
            u'Edutin Academy &middot; curso de mantenimiento &middot; en espa&ntilde;ol',
            u'El mismo m&eacute;todo aplicado a un equipo real, con las herramientas delante.')) +

  bloque('02', u'Pr&aacute;ctica &middot; 20 min', ficha(
    u'Actividad 7.6 &middot; Cuatro aver&iacute;as y un m&eacute;todo',
    [u'6.1'], u'Parejas &middot; 20 min &middot; sobre 10', u'''
          <div class="aviso">
            <span class="n-tag">Seguridad</span>
            Aqu&iacute; <b>no se abre ning&uacute;n equipo</b> ni se desenchufa nada sin que el profesor
            est&eacute; delante. Dentro de una fuente de alimentaci&oacute;n hay tensi&oacute;n peligrosa
            <b>incluso desenchufada</b>. Esta actividad es de papel y de escena.
          </div>
          <h4>Qu&eacute; hay que hacer</h4>
          <p>Para <b>cada uno</b> de los cuatro casos, escribid las cuatro cosas: <b>(a)</b> qu&eacute;
             pregunt&aacute;is primero al que lo usa; <b>(b)</b> cu&aacute;l es la prueba que m&aacute;s
             acota, diciendo <b>qu&eacute; concluir&iacute;ais con cada una de las dos respuestas
             posibles</b>; <b>(c)</b> vuestra hip&oacute;tesis principal; <b>(d)</b> c&oacute;mo la
             confirmar&iacute;ais <b>cambiando una sola cosa</b>.</p>
          <ol class="pasos">
            <li>&laquo;Pulso el bot&oacute;n y no pasa <b>absolutamente nada</b>: ni luces, ni ruido, ni
                ventilador.&raquo;</li>
            <li>&laquo;Enciende, oigo el ventilador y las luces van, pero la <b>pantalla sigue
                negra</b>.&raquo;</li>
            <li>&laquo;Arranca bien y llega al escritorio, pero al abrir el <b>programa de dibujo</b> se
                cierra solo. Los dem&aacute;s programas van perfectos.&raquo;</li>
            <li>&laquo;Va bien <b>media hora</b> y se apaga de golpe. Si lo dejo un rato quieto, vuelve a
                encender y otra vez lo mismo.&raquo;</li>
            <li>Volved a la escena. Acotad <b>tres aver&iacute;as distintas</b> y anotad cu&aacute;ntas
                pruebas hab&eacute;is gastado en cada una. Escribid una frase diciendo si hab&eacute;is
                mejorado de la primera a la tercera y <b>qu&eacute; hab&eacute;is cambiado</b> para
                mejorar.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Los cuatro casos llevan sus cuatro apartados <b>(4 puntos, uno por caso)</b>.</li>
            <li>En al menos tres casos, la prueba elegida <b>descarta varias piezas</b> a la vez y se dice
                qu&eacute; significa cada respuesta <b>(3 puntos)</b>.</li>
            <li>El caso 3 se identifica como problema <b>de software</b>, y se dice en qu&eacute; se nota
                <b>(1 punto)</b>.</li>
            <li>El caso 4 relaciona el fallo con <b>el tiempo que lleva encendido</b> y no con lo que se
                estaba haciendo <b>(1 punto)</b>.</li>
            <li>El recuento de la escena est&aacute; hecho y la frase final explica la mejora
                <b>(1 punto)</b>.</li>
          </ul>
          <div class="nota" style="margin-top:14px">
            <span class="n-tag">Aviso</span>
            No se puntúa acertar la aver&iacute;a: se puntúa el <b>m&eacute;todo</b>. Una hip&oacute;tesis
            equivocada con una buena prueba detr&aacute;s vale m&aacute;s que acertar de casualidad, porque
            la primera se puede comprobar y la segunda no.
          </div>
  ''')) +

  bloque('03', u'Test &middot; 12 min', u'''
      <p>Diez preguntas de <b>todo el tema</b>. Se corrigen aqu&iacute; mismo, y cada una explica por
         qu&eacute; &mdash;tambi&eacute;n las que aciertes&mdash;. No cuenta para nota: es para que sepas
         por d&oacute;nde andas antes del examen.</p>
''' + test('u7', u'Lo que tiene que haber quedado del tema', PREGUNTAS_TEST)) +

  bloque('04', u'Cierre &middot; 3 min', u'''
      <div class="copiar">
        <h4>El tema en tres frases</h4>
        <ol>
          <li>Un ordenador es <b>una sola m&aacute;quina</b> que no sabe hacer nada en concreto: obedece
              listas de instrucciones, y por eso sirve para todo.</li>
          <li>Dentro <b>solo hay ceros y unos</b>. Lo que significan depende siempre de un
              <b>acuerdo</b>, y todo lo que entra y sale hay que traducirlo.</li>
          <li>Todo lo dem&aacute;s es <b>reparto</b>: la RAM entre lo que est&aacute;s usando, la CPU entre
              los programas, el disco entre los ficheros. Y cuando algo falla, se <b>acota</b>: no se
              adivina.</li>
        </ol>
      </div>
      <div class="nota">
        <span class="n-tag">Siguiente tema</span>
        Tienes una m&aacute;quina que procesa informaci&oacute;n ella sola. La pregunta que abre el tema
        siguiente es: <b>&iquest;y si hay miles de millones de estas m&aacute;quinas y quieren hablar entre
        ellas?</b> Eso es <b>Internet</b>, y con &eacute;l llegan dos cosas que aqu&iacute; no
        hac&iacute;an falta: saber <b>de qui&eacute;n</b> te f&iacute;as y saber <b>qu&eacute;</b> est&aacute;s
        regalando.
      </div>
  '''))


# ==========================================================================
S = [
  dict(corto=u'Hardware y software',
       titulo=u'Una m&aacute;quina que no sabe hacer nada',
       entradilla=u'Con cables, cada comportamiento nuevo exige un circuito nuevo. La salida fue '
                  u'construir una sola m&aacute;quina y escribirle aparte lo que tiene que hacer.',
       minutado=[(u"10'", u'Reto'), (u"20'", u'Teor&iacute;a'), (u"25'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')],
       chips=[u'CE6 &middot; 6.1', u'D.1&ndash;D.4'],
       cuerpo=S1),
  dict(corto=u'RAM y almacenamiento',
       titulo=u'D&oacute;nde se guarda: la mesa y la estanter&iacute;a',
       entradilla=u'Que el ordenador se arrastre con quince pesta&ntilde;as y que pierdas lo que no has '
                  u'guardado no son dos desgracias: son la misma pieza, la memoria RAM.',
       minutado=[(u"10'", u'Reto'), (u"20'", u'Teor&iacute;a'), (u"25'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')],
       chips=[u'CE6 &middot; 6.1', u'D.1&ndash;D.4'],
       cuerpo=S2),
  dict(corto=u'Ceros y unos',
       titulo=u'Ceros y unos: c&oacute;mo se escribe algo con solo dos s&iacute;mbolos',
       entradilla=u'Un cable solo sabe decir dos cosas. Con eso hay que guardar textos, fotos y '
                  u'canciones &mdash;y se puede, porque las combinaciones se multiplican.',
       minutado=[(u"10'", u'Reto'), (u"20'", u'Teor&iacute;a'), (u"25'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')],
       chips=[u'CE6 &middot; 6.1', u'D.1&ndash;D.4'],
       cuerpo=S3),
  dict(corto=u'Entrada y salida',
       titulo=u'Entrada y salida: traducir el mundo a n&uacute;meros',
       entradilla=u'La temperatura, el sonido y la luz no vienen en escalones, y dentro de la '
                  u'm&aacute;quina todo son escalones. Lo que entra no es el mundo: es una copia, y '
                  u'se puede medir cu&aacute;nto se pierde.',
       minutado=[(u"10'", u'Reto'), (u"20'", u'Teor&iacute;a'), (u"25'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')],
       chips=[u'CE6 &middot; 6.1', u'D.1&ndash;D.4'],
       cuerpo=S4),
  dict(corto=u'Sistema operativo',
       titulo=u'El sistema operativo: qui&eacute;n reparte la m&aacute;quina',
       entradilla=u'Doscientos programas, cuatro n&uacute;cleos y ninguna pelea. Detr&aacute;s hay un '
                  u'programa que no pide las cosas por favor: las quita, las separa y las reparte.',
       minutado=[(u"10'", u'Reto'), (u"20'", u'Teor&iacute;a'), (u"25'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')],
       chips=[u'CE6 &middot; 6.1', u'D.1&ndash;D.4'],
       cuerpo=S5),
  dict(corto=u'Diagnosticar una aver&iacute;a',
       titulo=u'Diagnosticar: acotar en vez de adivinar',
       entradilla=u'&laquo;No va&raquo; no es un s&iacute;ntoma. La sesi&oacute;n no ense&ntilde;a '
                  u'ninguna pieza nueva: ense&ntilde;a el m&eacute;todo para averiguar cu&aacute;l de '
                  u'las que ya conoces ha fallado, y cierra el tema con el test.',
       minutado=[(u"10'", u'Reto'), (u"15'", u'Teor&iacute;a'), (u"20'", u'Pr&aacute;ctica'),
                 (u"12'", u'Test'), (u"3'", u'Cierre')],
       chips=[u'CE6 &middot; 6.1', u'D.1&ndash;D.4'],
       cuerpo=S6),
]

CFG = dict(
 ruta='2eso/TyD/tema9/',
 migas=u'<a href="../../../">Materiales</a> &middot; <a href="../../">2.&ordm; ESO</a> '
       u'&middot; <a href="../">TyD</a> &middot; Tema 7',
 h1=u'El ordenador y sus componentes',
 titulo=u'Tema 9 &middot; El ordenador y sus componentes',
 tema=u'Tema 9', curso=u'2.&ordm; de ESO', materia=u'Tecnolog&iacute;a y Digitalizaci&oacute;n',
 desc=u'Tema 9 de Tecnolog&iacute;a y Digitalizaci&oacute;n de 2.&ordm; de ESO: hardware y software, la CPU y '
      u'su ciclo, memoria RAM frente a almacenamiento, representaci&oacute;n binaria, perif&eacute;ricos y '
      u'conversi&oacute;n anal&oacute;gico-digital, sistema operativo y diagn&oacute;stico de aver&iacute;as.',
 sesiones=S)


# Dos anadidos al molde: el CSS del avatar (que vive en avatar_flat, no en
# tema0_base) y un poco de estilo para las tablas, que la U3 no necesitaba.
EXTRA_CSS = avatar_flat.CSS + u"""
/* tablas de datos dentro de los bloques que se copian */
.copiar table{border-collapse:collapse;width:100%;margin:10px 0 4px;font-size:14.5px}
.copiar th,.copiar td{border:1px solid var(--line);padding:6px 9px;text-align:left}
.copiar th{background:var(--surface-2);font-family:var(--f-m);font-size:11.5px;
  letter-spacing:.06em;text-transform:uppercase;color:var(--ink-soft);font-weight:500}
.copiar td:first-child{width:52%}
@media (max-width:560px){.copiar table{font-size:13px}.copiar th,.copiar td{padding:5px 6px}}
"""

if __name__ == '__main__':
    html = pagina(CFG).replace(u'</style>', EXTRA_CSS + u'</style>', 1)
    destino = os.path.join(RAIZ, '2eso', 'TyD', 'tema9')
    os.makedirs(destino, exist_ok=True)
    io.open(os.path.join(destino, 'index.html'), 'w', encoding='utf-8', newline='').write(html)
    print('U7 generada: %d bytes, %d sesiones (%d escritas)' % (
        len(html), len(S), sum(1 for x in S if not x.get('pendiente'))))
