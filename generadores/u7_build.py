# -*- coding: utf-8 -*-
"""2.o TyD · U7 · El ordenador y sus componentes.

Sesiones 1, 2 y 3 escritas; 4, 5 y 6 marcadas como pendientes.
Las escenas interactivas viven en u7_escenas.py.

    python generadores/u7_build.py

Escribe 2eso/TyD/tema7/index.html relativo a la raiz del repo (el padre de
generadores/), no a una ruta absoluta: asi corre igual en el portatil y aqui.
"""
import io, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unidad_base import pagina, bloque, ficha, pregunta
import avatar_flat
from u7_escenas import ESCENA_CPU, ESCENA_RAM, ESCENA_BITS

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
        <p style="margin-top:10px"><a href="lectura-tema7.pdf" target="_blank" rel="noopener"
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
        Ya sabes que hay huecos en la RAM y huecos en el disco. Queda la pregunta inc&oacute;moda:
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
        Ya tienes una m&aacute;quina que procesa informaci&oacute;n ella sola. La pregunta siguiente es la que abre
        la unidad de <b>Internet, datos y seguridad</b>: <b>&iquest;y si hay millones de estas m&aacute;quinas
        y quieren hablar entre ellas?</b>
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
  dict(corto=u'Entrada y salida', pendiente=True),
  dict(corto=u'Sistema operativo', pendiente=True),
  dict(corto=u'Diagnosticar una aver&iacute;a', pendiente=True),
]

CFG = dict(
 ruta='2eso/TyD/tema7/',
 migas=u'<a href="../../../">Materiales</a> &middot; <a href="../../">2.&ordm; ESO</a> '
       u'&middot; <a href="../">TyD</a> &middot; Tema 7',
 h1=u'El ordenador y sus componentes',
 titulo=u'Tema 7 &middot; El ordenador y sus componentes',
 tema=u'Tema 7', curso=u'2.&ordm; de ESO', materia=u'Tecnolog&iacute;a y Digitalizaci&oacute;n',
 desc=u'Tema 7 de Tecnolog&iacute;a y Digitalizaci&oacute;n de 2.&ordm; de ESO: hardware y software, la CPU y '
      u'su ciclo, memoria RAM frente a almacenamiento y representaci&oacute;n binaria de la informaci&oacute;n.',
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
    destino = os.path.join(RAIZ, '2eso', 'TyD', 'tema7')
    os.makedirs(destino, exist_ok=True)
    io.open(os.path.join(destino, 'index.html'), 'w', encoding='utf-8', newline='').write(html)
    print('U7 generada: %d bytes, %d sesiones (%d escritas)' % (
        len(html), len(S), sum(1 for x in S if not x.get('pendiente'))))
