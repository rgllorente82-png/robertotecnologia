# -*- coding: utf-8 -*-
"""2.o TyD · U9 (web) · Herramientas digitales y difusion.

Sesiones 1, 2 y 3 escritas; 4, 5 y 6 marcadas como pendientes.
Las escenas interactivas viven en u9_escenas.py.

    ~/venv/bin/python generadores/u9_build.py

Escribe 2eso/TyD/tema9/index.html relativo a la raiz del repo (el padre de
generadores/), no a una ruta absoluta: asi corre igual en el portatil y aqui.
Necesita el venv porque las anchuras de las tipografias salen de las tablas AFM
que trae reportlab (ver u9_metricas.py); la pagina que sale no depende de nada.

Ojo con la numeracion: esto es el TEMA 9 de la web y la UNIDAD 11 del libro
(criterios 2.1, 4.1, 6.1, 6.2 y 6.3). Ver CURRICULO.md e INFORME-tema9.md. En el
texto no aparece ningun numero de tema -se dice "la unidad de internet", no "el
tema 8"-, igual que en la U7 y la U8: si algun dia se renumera, no hay que
reescribir nada.

Esta unidad cierra el circulo que abrio la de representacion grafica: alli el
criterio 4.1 era explicar una idea con un dibujo a mano, y aqui es producirla y
difundirla con herramientas digitales. Es el MISMO criterio, y se dice en las
dos puntas para que el alumno lo vea.
"""
import io, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unidad_base import pagina, bloque, ficha, pregunta
import avatar_flat
from u9_escenas import (ESCENA_MAQUETA, ESCENA_ESTILOS, ESCENA_MAPA,
                        ESCENA_PESO, ESCENA_AULA, ESCENA_CARRERA)

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
''' % (idv, vid, titulo, titulo, canal, nota, vid)


ENV = json.load(io.open(os.path.join(RAIZ, '_env_u9-digitales.json'), encoding='utf-8'))
NARRADOR = avatar_flat.componente(
    'narr-u9', u'De d&oacute;nde sale esta unidad',
    u'Hasta ahora eras el que mira; a partir de aqu&iacute; eres el que publica',
    '../../../audio/u9-digitales.mp3', ENV,
    u'Voz sintetizada sobre gui&oacute;n propio. La boca sigue el volumen real de la voz: se mueve '
    u'cuando habla y se para en los silencios.')


# ==========================================================================
# SESION 1 · El documento que no se rompe
# ==========================================================================
S1 = (
  bloque('00', u'Reto inicial &middot; 10 min', u'''
      <p>De la unidad de internet sales sabiendo c&oacute;mo llega a tu pantalla lo que pides y
         qui&eacute;n lo ve pasar por el camino. Todo eso lo mirabas t&uacute;. A partir de hoy le
         damos la vuelta a la pregunta: <b>ya no eres el que mira, eres el que publica</b>.</p>
      <p>Y produciendo pasa una cosa que todo el mundo ha vivido.</p>

''' + NARRADOR + u'''
      <div class="aviso">
        <span class="n-tag">El encargo</span>
        Terminas el trabajo el domingo en casa. El lunes lo abres en el ordenador del aula para
        imprimirlo y <b>no es el mismo</b>: los t&iacute;tulos han cambiado de letra, la segunda
        foto se ha ido sola a la p&aacute;gina siguiente y donde ten&iacute;as seis p&aacute;ginas
        ahora hay ocho. Escribe en el cuaderno <b>tres explicaciones posibles</b> de qu&eacute; ha
        pasado. Cinco minutos, y sin mirar a nadie.
      </div>

      <p>Las tres que salen siempre son estas: <i>se ha corrompido el fichero</i>, <i>el programa
         del instituto es una versi&oacute;n vieja</i> y <i>lo guard&eacute; mal</i>. Las tres
         suenan razonables y las tres son falsas, y hay una prueba que las tumba de golpe:</p>

      <div class="reto-piensa">
        <span class="n-tag">Mira el texto antes de seguir</span>
        <p>&iquest;Falta alguna <b>palabra</b>? &iquest;Ha cambiado alguna <b>letra</b>?
           &iquest;Se ha perdido alg&uacute;n <b>p&aacute;rrafo</b>?</p>
        <p style="margin-top:8px">No. Est&aacute; <b>todo</b>, entero y en orden. Si el fichero
           estuviera roto faltar&iacute;a algo; si se hubiera guardado mal, tambi&eacute;n. Lo
           &uacute;nico que ha cambiado es <b>c&oacute;mo est&aacute; repartido encima del
           papel</b>.</p>
      </div>

      <p>Eso ya no es una aver&iacute;a: es una pista. Quiere decir que el fichero <b>no guarda una
         foto de la p&aacute;gina</b>. Guarda otra cosa, y la p&aacute;gina se <b>vuelve a
         construir</b> cada vez que alguien lo abre. Si se construye otra vez, se construye con lo
         que haya en <b>ese</b> ordenador. Y ah&iacute; est&aacute; el l&iacute;o.</p>
  ''') +

  bloque('01', u'Teor&iacute;a &middot; 20 min', u'''
      <h3>Lo mismo, y sin embargo distinto</h3>
      <p>Abajo tienes el mismo documento en dos ordenadores. El de la izquierda es donde lo
         escribiste y no se toca. En el de la derecha cambia la <b>letra</b>, el <b>papel</b> y el
         <b>cuerpo</b>, y fíjate en tres cosas: cu&aacute;ntas l&iacute;neas salen, cu&aacute;ntas
         hojas, y <b>en qu&eacute; hoja acaba la segunda foto</b>.</p>

''' + ESCENA_MAQUETA + u'''
      <p>Ninguna palabra se ha movido de sitio en el fichero. Lo que se mueve es el
         <b>dibujo</b>, porque el dibujo se hace en el &uacute;ltimo momento.</p>

      <div class="copiar">
        <h4>La idea que ordena toda la unidad</h4>
        <p>Un documento guarda <b>dos cosas distintas</b>, y conviene no mezclarlas:</p>
        <ul>
          <li><b>Lo que dice</b>: las letras, las palabras, y qu&eacute; papel hace cada trozo
              &mdash;esto es un t&iacute;tulo, esto es un p&aacute;rrafo, esto es un pie de
              foto&mdash;.</li>
          <li><b>C&oacute;mo se ve</b>: con qu&eacute; tipo de letra, de qu&eacute; tama&ntilde;o,
              con cu&aacute;nto margen, en qu&eacute; papel.</li>
        </ul>
        <p>Lo primero viaja dentro del fichero. Lo segundo lo <b>decide el programa al abrirlo</b>,
           con lo que tenga ese ordenador. Por eso el mismo fichero se ve distinto en dos sitios
           sin que nadie lo haya estropeado.</p>
      </div>

      <h3>Esto no lo invent&oacute; el ordenador</h3>
      <p>Separar lo que un texto dice de la forma que tiene encima del papel es una idea vieja. Un
         escriba copiaba las dos cosas a la vez: cada letra que dibujaba era, al mismo tiempo, el
         contenido y su forma. Con los <b>tipos m&oacute;viles</b> eso se parte en dos oficios: uno
         <b>compone</b> las palabras y otro decide <b>con qu&eacute; tipos</b> se imprimen.</p>

''' + foto('u9-tipos-moviles.jpg',
           u'Cajas de madera llenas de tipos de plomo y un componedor met&aacute;lico con una frase '
           u'compuesta al rev&eacute;s',
           u'Una <b>caja de tipos</b>: cada letra es una pieza suelta de plomo, y est&aacute;n '
           u'guardadas por letras, no por palabras. En el componedor met&aacute;lico hay una frase '
           u'ya compuesta &mdash;se lee del rev&eacute;s y boca abajo, porque al imprimir se da la '
           u'vuelta&mdash;. Lo importante para hoy: <b>la frase y los tipos son cosas distintas</b>. '
           u'La misma frase se puede componer con otros tipos sin cambiar una palabra, que es '
           u'exactamente lo que le pasa a tu trabajo al abrirlo en otro ordenador.',
           u'Willi Heidelbach', u'CC BY 2.5',
           u'https://commons.wikimedia.org/wiki/File:Metal_movable_type.jpg') + u'''
      <h3>Tres maneras de guardar un texto</h3>
      <div class="copiar">
        <h4>Formatos de fichero</h4>
        <p><b>Formato</b>: la manera acordada de ordenar los bytes dentro de un fichero para que
           otro programa sepa leerlos. La extensi&oacute;n del nombre &mdash;<i>.txt</i>,
           <i>.odt</i>, <i>.pdf</i>&mdash; solo es una <b>etiqueta</b> que avisa de cu&aacute;l es.</p>
        <table>
          <tr><th>Familia</th><th>Qu&eacute; guarda</th><th>Para qu&eacute; sirve</th></tr>
          <tr><td><b>Texto plano</b> (.txt, .csv)</td>
              <td>Solo las letras, una detr&aacute;s de otra. Nada m&aacute;s.</td>
              <td>Lo abre cualquier cosa y durar&aacute; siempre. No tiene t&iacute;tulos ni
                  negritas.</td></tr>
          <tr><td><b>Documento con marcas</b> (.odt, .docx)</td>
              <td>Las letras <b>y</b> las marcas que dicen qu&eacute; papel hace cada trozo.</td>
              <td>Para escribir y seguir cambiando. Se redibuja al abrirlo.</td></tr>
          <tr><td><b>P&aacute;gina fija</b> (.pdf)</td>
              <td>D&oacute;nde va cada letra, y las letras mismas <b>metidas dentro</b>.</td>
              <td>Para entregar. Se ve igual en todas partes; cuesta editarlo.</td></tr>
        </table>
      </div>

      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; no hace falta copiarlo</span>
        <p>Un fichero <i>.odt</i> o <i>.docx</i> no es un bloque m&aacute;gico: es una
           <b>carpeta comprimida</b>. Si le cambias la extensi&oacute;n a <i>.zip</i> y lo abres,
           dentro hay ficheros de texto con el contenido por un lado y el aspecto por otro. Lo
           vais a hacer en la pr&aacute;ctica, y es la manera m&aacute;s r&aacute;pida de creerse
           todo lo de hoy.</p>
        <p>El de <i>.odt</i> se llama <b>OpenDocument</b>, y es una <b>norma p&uacute;blica</b>
           desde 2006: cualquiera puede leer c&oacute;mo est&aacute; hecho y escribir un programa
           que lo abra. Eso importa m&aacute;s de lo que parece cuando el trabajo que quieres
           recuperar tiene quince a&ntilde;os y el programa con el que lo hiciste ya no existe.</p>
      </div>

      <h3>Marcar no es pintar</h3>
      <p>Aqu&iacute; est&aacute; el h&aacute;bito que hay que cambiar. Casi todo el mundo hace los
         t&iacute;tulos as&iacute;: seleccionar, negrita, subir el tama&ntilde;o, centrar. El
         resultado <b>parece</b> un t&iacute;tulo. Pero el programa no ha entendido que sea un
         t&iacute;tulo: para &eacute;l sigue siendo texto normal que resulta que est&aacute; en
         negrita.</p>
      <p>Compru&eacute;balo. En la escena de abajo, pide el &iacute;ndice de las dos maneras.</p>

''' + ESCENA_ESTILOS + u'''
      <div class="copiar">
        <h4>Estilo</h4>
        <p><b>Estilo</b>: una <b>etiqueta</b> que le pones a un trozo de texto para decir
           qu&eacute; es &mdash;T&iacute;tulo 1, T&iacute;tulo 2, Normal, Cita&mdash;. El aspecto
           de cada etiqueta se define <b>una sola vez</b>, aparte.</p>
        <p>De ah&iacute; salen tres cosas que a mano no se pueden hacer:</p>
        <ul>
          <li>El <b>&iacute;ndice se genera solo</b>, con sus n&uacute;meros de p&aacute;gina, y se
              actualiza cuando el documento crece.</li>
          <li>Cambiar el aspecto de todos los t&iacute;tulos cuesta <b>un retoque</b>, no uno por
              t&iacute;tulo.</li>
          <li>Un lector de pantalla &mdash;lo que usa una persona ciega&mdash; puede ir
              <b>saltando de apartado en apartado</b>. Si no hay estilos, no hay apartados a los
              que saltar.</li>
        </ul>
        <p>Regla corta: <b>marcar lo que algo es, no pintar lo que parece</b>.</p>
      </div>

      <h3>Y entonces, &iquest;por qu&eacute; el PDF se ve igual?</h3>
      <p>Porque hace justo lo contrario, y a prop&oacute;sito. Un PDF no deja nada por decidir: ya
         lleva calculada la posici&oacute;n de cada letra, y adem&aacute;s se lleva <b>las letras
         dentro</b>, incrustadas, para no depender de las que tenga el ordenador de enfrente.
         Vuelve a la escena de arriba y pulsa <b>&laquo;Mandarlo en PDF&raquo;</b>: los botones
         siguen funcionando y la hoja ya no se mueve.</p>

      <div class="copiar">
        <h4>PDF</h4>
        <p><b>PDF</b> (<i>formato de documento port&aacute;til</i>): un formato que guarda la
           <b>p&aacute;gina ya maquetada</b> &mdash;posiciones y tipograf&iacute;as
           incluidas&mdash;, en vez de guardar el texto y dejar que se redibuje.</p>
        <p>Lo que ganas: se ve <b>igual en cualquier sitio</b> y se imprime igual. Es el formato
           para <b>entregar</b>.</p>
        <p>Lo que pierdes, y hay que saberlo:</p>
        <ul>
          <li><b>Editarlo cuesta</b>: est&aacute; pensado para leerse, no para seguir
              escribi&eacute;ndolo. El original se guarda aparte.</li>
          <li><b>No se adapta</b> a una pantalla peque&ntilde;a: en el m&oacute;vil hay que hacer
              zoom, porque la p&aacute;gina es fija por definici&oacute;n.</li>
          <li>Si se hace mal &mdash;por ejemplo escaneando papel&mdash;, dentro no hay texto sino
              una foto: no se puede buscar ni copiar, y un lector de pantalla no puede leerlo.</li>
        </ul>
      </div>

      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; no hace falta copiarlo</span>
        <p>Los tipos m&oacute;viles no son de Gutenberg: en China ya los usaba <b>Bi Sheng</b> hacia
           <b>1040</b>, de cer&aacute;mica, y el libro impreso con tipos de metal m&aacute;s antiguo
           que se conserva es coreano, el <i>Jikji</i>, de <b>1377</b>. Lo que Gutenberg mont&oacute;
           en Maguncia hacia <b>1450</b> fue el <b>sistema entero</b>: la aleaci&oacute;n para
           fundir tipos iguales miles de veces, la tinta que agarraba en el metal y una prensa que
           apretaba fuerte y parejo.</p>
        <p>El PDF es mucho m&aacute;s reciente. Lo sac&oacute; la empresa <b>Adobe</b> en
           <b>1993</b>, y al principio hab&iacute;a que pagar por el programa que lo le&iacute;a.
           Les fue mal: nadie manda un fichero que el otro no puede abrir. Cuando regalaron el
           lector, el formato se comi&oacute; el mundo. En <b>2008</b> dej&oacute; de ser suyo y
           pas&oacute; a ser una <b>norma internacional</b> (ISO 32000), o sea, de nadie. Esa es la
           raz&oacute;n de fondo por la que hoy puedes mandar un PDF a cualquiera sin preguntar
           qu&eacute; tiene instalado.</p>
      </div>

''' + video('video-pdf', 'pSBpSSbx9Ps',
            u'&iquest;Qu&eacute; es un PDF?',
            u'Micro Conocimiento &middot; en espa&ntilde;ol',
            u'Un minuto y medio para fijar por qu&eacute; se manda en PDF lo que tiene que verse '
            u'igual en todas partes.')) +

  bloque('02', u'Pr&aacute;ctica &middot; 25 min', ficha(
    u'Actividad 9.1 &middot; Abrir un documento por dentro',
    [u'4.1', u'6.1'], u'Parejas &middot; 25 min &middot; sobre 10', u'''
          <div class="nota">
            <span class="n-tag">Con qu&eacute; se hace</span>
            Con el procesador de textos que tengas en el aula o con el de la suite del centro. No
            hace falta instalar nada, y los pasos no dependen de qu&eacute; programa sea: lo que se
            eval&uacute;a es la cuenta y la explicaci&oacute;n, no d&oacute;nde est&aacute; el
            bot&oacute;n.
          </div>
          <h4>Qu&eacute; hay que hacer</h4>
          <ol class="pasos">
            <li><b>El mismo p&aacute;rrafo, dos veces.</b> Copiad un p&aacute;rrafo cualquiera de
                esta p&aacute;gina en un <b>editor de texto plano</b> y gu&aacute;rdadlo como
                <i>.txt</i>. Pegadlo tambi&eacute;n en el procesador y guardadlo como <i>.odt</i>.
                Anotad <b>lo que ocupa cada fichero</b> y contestad: si el texto es el mismo,
                &iquest;<b>qu&eacute; hay</b> en la diferencia?</li>
            <li><b>Abrid el documento por dentro.</b> Haced una copia del <i>.odt</i>,
                cambiadle la extensi&oacute;n a <i>.zip</i> y abridlo. Apuntad <b>cu&aacute;ntos
                ficheros</b> hay dentro y <b>c&oacute;mo se llaman</b>. Buscad en cu&aacute;l
                est&aacute; vuestro texto y en cu&aacute;l est&aacute; el aspecto. Una frase:
                &iquest;por qu&eacute; est&aacute;n en ficheros distintos?</li>
            <li><b>Estilos.</b> Escribid un documento con <b>seis apartados</b> (basta una l&iacute;nea
                de relleno en cada uno). Marcad los t&iacute;tulos con el estilo <i>T&iacute;tulo
                1</i> y <i>T&iacute;tulo 2</i>, y generad el <b>&iacute;ndice autom&aacute;tico</b>.
                Despu&eacute;s cambiad el estilo <i>T&iacute;tulo 1</i> &mdash;otra letra y otro
                color&mdash; y contad <b>cu&aacute;ntos retoques</b> os ha costado.</li>
            <li><b>La cuenta de lo que costar&iacute;a a mano.</b> Cronometrad lo que tard&aacute;is
                en cambiarle el aspecto a <b>dos</b> t&iacute;tulos a mano. Multiplicad por los
                t&iacute;tulos que tendr&iacute;a un trabajo de treinta p&aacute;ginas (contad unos
                <b>dos por p&aacute;gina</b>) y decid el resultado en minutos.</li>
            <li><b>La escena, con n&uacute;meros.</b> En la escena de las dos hojas, anotad las
                <b>l&iacute;neas</b> y las <b>hojas</b> con <i>Helvetica 11 pt en A4</i> y con
                <i>Courier 14 pt en Carta</i>. Calculad en <b>qu&eacute; porcentaje</b> aumentan las
                l&iacute;neas, y decid en qu&eacute; hoja cae la segunda foto en cada caso.</li>
            <li><b>Entregadlo en PDF.</b> Exportad el documento del paso 3 a PDF, abridlo y
                contestad a dos preguntas: &iquest;funciona el &iacute;ndice como enlaces?
                &iquest;Se puede <b>buscar</b> una palabra dentro? Y la importante:
                &iquest;<b>qu&eacute; hab&eacute;is perdido</b> al exportar?</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Los dos tama&ntilde;os est&aacute;n anotados y la explicaci&oacute;n de la
                diferencia habla de <b>marcas</b>, no de &laquo;el programa ocupa m&aacute;s&raquo;
                <b>(2 puntos)</b>.</li>
            <li>El <i>.odt</i> se ha abierto por dentro y se distingue <b>d&oacute;nde est&aacute;
                el texto</b> de d&oacute;nde est&aacute; el aspecto <b>(2 puntos)</b>.</li>
            <li>El &iacute;ndice autom&aacute;tico funciona y el cambio de estilo se ha hecho
                <b>desde el estilo</b> <b>(2 puntos)</b>.</li>
            <li>Las dos cuentas &mdash;los minutos a mano y el porcentaje de la escena&mdash;
                est&aacute;n bien hechas y con unidades <b>(2 puntos)</b>.</li>
            <li>La respuesta sobre el PDF dice qu&eacute; se gana y qu&eacute; se pierde, sin
                quedarse en &laquo;es mejor&raquo; <b>(2 puntos)</b>.</li>
          </ul>
          <div class="nota" style="margin-top:14px">
            <span class="n-tag">Aviso sobre el paso 2</span>
            Trabajad siempre sobre una <b>copia</b>. Cambiarle la extensi&oacute;n al original y
            luego no saber volver atr&aacute;s es la manera m&aacute;s tonta de perder un trabajo.
          </div>
  ''')) +

  bloque('03', u'Cierre &middot; 5 min', u'''
      <p>Vuelve a las tres explicaciones que escribiste al principio. Ninguna hac&iacute;a falta:
         no hab&iacute;a aver&iacute;a. Hab&iacute;a un documento que <b>se vuelve a dibujar cada
         vez</b>, y un aspecto que estaba pegado a mano en vez de estar dicho con estilos.</p>
      <ol>
      ''' + pregunta(u'El mismo fichero se ve distinto en dos ordenadores y no falta ni una palabra. &iquest;Qu&eacute; ha pasado?',
                     u'<p>Que el fichero no guarda una foto de la p&aacute;gina: guarda <b>el texto y sus marcas</b>, y la p&aacute;gina se <b>redibuja</b> al abrirlo con lo que ese ordenador tenga. Si la letra es otra, las palabras ocupan otra cosa, las l&iacute;neas cortan por otro sitio y todo lo de abajo se mueve. No se ha estropeado nada.</p>')
        + pregunta(u'Pones un t&iacute;tulo en negrita y m&aacute;s grande, pero el &iacute;ndice autom&aacute;tico sale vac&iacute;o. &iquest;Por qu&eacute;?',
                   u'<p>Porque le has cambiado el <b>aspecto</b> y no le has dicho <b>qu&eacute; es</b>. Negrita y tama&ntilde;o son pintura; el programa solo ve texto normal. Para que sea un t&iacute;tulo hay que marcarlo con un <b>estilo</b>, y entonces el programa ya sabe qu&eacute; meter en el &iacute;ndice &mdash;y un lector de pantalla, por d&oacute;nde saltar&mdash;.</p>')
        + pregunta(u'&iquest;Cu&aacute;ndo se manda un PDF y cu&aacute;ndo NO?',
                   u'<p>Se manda en PDF lo que est&aacute; <b>terminado</b> y tiene que verse igual en todas partes: la entrega, el cartel, el documento que se imprime. No se manda en PDF lo que a&uacute;n hay que <b>seguir escribiendo</b> o lo que otra persona tiene que retocar, porque editarlo cuesta. El original se guarda siempre aparte.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        En el documento de hoy hab&iacute;a dos fotos, y hemos hablado de d&oacute;nde caen, no de
        lo que pesan. Haz la prueba antes de la pr&oacute;xima clase: mira lo que ocupa
        <b>una sola foto</b> de tu m&oacute;vil. Ahora multipl&iacute;calo por las once que va a
        llevar la presentaci&oacute;n del grupo. <b>&iquest;Cabe?</b>
      </div>

      <div class="copiar" style="border-color:var(--goo-verde)">
        <h4>Lectura del tema</h4>
        <p>Una sesi&oacute;n entera dedicada a leer y contestar. <b>30 p&aacute;rrafos numerados</b>:
           cada uno lee el suyo en voz alta, en orden. Despu&eacute;s, diez preguntas por escrito.</p>
        <p style="margin-top:10px"><a href="lectura-tema9.pdf" target="_blank" rel="noopener"
           style="font-family:var(--f-m);font-size:13px;color:var(--goo-verde);font-weight:500">
           &#8595; Lo que dice y c&oacute;mo se ve &middot; PDF</a></p>
      </div>
  '''))


# ==========================================================================
# SESION 2 · Una imagen pesa lo que pesa
# ==========================================================================
S2 = (
  bloque('00', u'Reto inicial &middot; 10 min', u'''
      <p>El grupo termina la presentaci&oacute;n: catorce diapositivas y once fotos. Al ir a
         subirla, el aviso de siempre: <b>48 MB</b>, demasiado. Y lo raro es que ah&iacute; dentro
         no hay 48 MB de ideas.</p>

      <div class="aviso">
        <span class="n-tag">El encargo</span>
        Antes de leer nada m&aacute;s, escribe un n&uacute;mero en el cuaderno: <b>&iquest;cu&aacute;nto
        crees que ocupa una foto de tu m&oacute;vil?</b> Y otro: <b>&iquest;y cu&aacute;nto
        ocupar&iacute;a esa misma foto si nadie la hubiera comprimido?</b> Si no tienes ni idea del
        segundo, ponlo igual: vamos a comprobarlo en un minuto.
      </div>

      <p>Haz la cuenta t&uacute;, que no tiene truco. Una c&aacute;mara de m&oacute;vil corriente
         hace fotos de <b>4.032 &times; 3.024</b> puntos. Cada punto guarda su color, y un color se
         guarda en <b>3 bytes</b> &mdash;uno de rojo, uno de verde y uno de azul&mdash;:</p>

      <div class="reto-piensa">
        <span class="n-tag">Las dos multiplicaciones</span>
        <p><b>1.</b> 4.032 &times; 3.024 = <b>12.192.768 puntos</b>. Eso es lo que quiere decir
           &laquo;12 megap&iacute;xeles&raquo;: doce millones de puntos.</p>
        <p><b>2.</b> 12.192.768 &times; 3 = <b>36.578.304 bytes</b>, o sea unos <b>35 MB</b>.
           <b>Una sola foto.</b></p>
        <p style="margin-top:8px">Y ahora mira lo que dice tu m&oacute;vil que ocupa esa foto.
           Suele poner entre <b>2 y 4 MB</b>. Sobran unos 32.
           <b>&iquest;D&oacute;nde est&aacute;n?</b></p>
      </div>

      <p>Esa pregunta es la sesi&oacute;n entera, y tiene dos respuestas: una se llama
         <b>compresi&oacute;n</b> y la otra es que a lo mejor <b>no hac&iacute;an falta</b>.</p>

      <p>Antes, la soluci&oacute;n que intenta todo el mundo con la presentaci&oacute;n de 48 MB:
         <b>arrastrar la esquina de la foto para hacerla peque&ntilde;a</b>. Prueba a hacerlo y
         vuelve a mirar lo que ocupa el fichero. <b>Lo mismo.</b> No has cambiado la foto: has
         cambiado <b>c&oacute;mo se dibuja</b>. Es exactamente el error de la sesi&oacute;n
         anterior, otra vez: confundir lo que una cosa <b>es</b> con lo que <b>parece</b>.</p>
  ''') +

  bloque('01', u'Teor&iacute;a &middot; 20 min', u'''
      <h3>Una foto es, literalmente, una rejilla</h3>
      <p>No es una met&aacute;fora. Detr&aacute;s del objetivo del m&oacute;vil hay una rejilla de
         casillas diminutas, cada una con un filtro de color delante, y cada casilla mide
         cu&aacute;nta luz le llega. La foto es la <b>lista de esas medidas</b>.</p>

''' + foto('u9-sensor-rejilla.jpg',
           u'Fotograf&iacute;a a mucho aumento de un sensor de color, con su rejilla de casillas '
           u'rojas, verdes y azules',
           u'Un <b>sensor de color</b> visto a mucho aumento. En el centro, debajo de la lente '
           u'redonda, se ve la <b>rejilla</b>: casillas cuadradas con un filtro rojo, verde o azul '
           u'delante. Cada casilla mide la luz que le llega y devuelve un n&uacute;mero. El de la '
           u'foto es un sensor peque&ntilde;o, de pocas casillas; el de un m&oacute;vil es el mismo '
           u'invento con <b>doce millones</b> de ellas. Cuando decimos que una imagen &laquo;son '
           u'p&iacute;xeles&raquo;, esto es lo que hay debajo.',
           u'Prosthetic Head', u'CC BY-SA 4.0',
           u'https://commons.wikimedia.org/wiki/File:Colour_Sensor_Macro.jpg') + u'''
      <p>Guardar una rejilla tiene una consecuencia incómoda que se ve mejor ampliando. A la
         izquierda de la escena hay un s&iacute;mbolo guardado como <b>casillas</b>; a la derecha,
         el mismo s&iacute;mbolo guardado como <b>instrucciones de dibujo</b>. Acerca los dos.</p>

''' + ESCENA_MAPA + u'''
      <div class="copiar">
        <h4>Mapa de bits y vectorial</h4>
        <p><b>Mapa de bits</b>: la imagen es una <b>rejilla de p&iacute;xeles</b>, y de cada uno se
           guarda su color. Es lo que sale de una c&aacute;mara o de un esc&aacute;ner.
           Formatos: <b>JPEG</b>, <b>PNG</b>, <b>WebP</b>.</p>
        <p><b>Vectorial</b>: la imagen es una <b>lista de instrucciones</b> &mdash;una
           circunferencia de tal radio aqu&iacute;, una l&iacute;nea hasta all&iacute;, rellena de
           este color&mdash;. Se vuelve a dibujar cada vez, al tama&ntilde;o que haga falta.
           Formato: <b>SVG</b>.</p>
        <table>
          <tr><th></th><th>Mapa de bits</th><th>Vectorial</th></tr>
          <tr><td>Al ampliar</td><td>Salen las casillas: no hay m&aacute;s detalle guardado</td>
              <td>Se redibuja y sigue fino, a cualquier tama&ntilde;o</td></tr>
          <tr><td>Lo que pesa</td><td>Depende de cu&aacute;ntos p&iacute;xeles tenga</td>
              <td>Depende de cu&aacute;ntas instrucciones, no del tama&ntilde;o</td></tr>
          <tr><td>Sirve para</td><td>Fotograf&iacute;as</td>
              <td>Logotipos, iconos, planos, esquemas, letras</td></tr>
          <tr><td>No sirve para</td><td>Un logotipo que hay que ampliar</td>
              <td>Una fotograf&iacute;a</td></tr>
        </table>
      </div>

      <p>Por qu&eacute; una foto no puede ser vectorial: har&iacute;a falta una instrucci&oacute;n
         por cada mancha de color, y en una cara hay millones que no se parecen a ning&uacute;n
         c&iacute;rculo ni a ninguna recta. Por qu&eacute; un logotipo no deber&iacute;a ser un
         mapa de bits: porque un logotipo acaba <b>en un carn&eacute; y en una pancarta</b>, y solo
         uno de los dos cabe en la rejilla que guardaste.</p>

      <div class="copiar">
        <h4>Medido, no estimado</h4>
        <p>El s&iacute;mbolo de la escena, guardado de las dos maneras:</p>
        <table>
          <tr><th>Guardado como</th><th>Ocupa</th></tr>
          <tr><td>SVG (instrucciones), a cualquier tama&ntilde;o</td><td><b>244 bytes</b></td></tr>
          <tr><td>PNG de 64 &times; 64</td><td>365 bytes</td></tr>
          <tr><td>PNG de 256 &times; 256</td><td>1.559 bytes</td></tr>
          <tr><td>PNG de 1.024 &times; 1.024</td><td>6.426 bytes</td></tr>
          <tr><td>PNG de 2.048 &times; 2.048</td><td><b>15.254 bytes</b></td></tr>
        </table>
        <p>El vectorial pesa <b>lo mismo siempre</b>. El mapa de bits, para el mismo dibujo y a
           gran tama&ntilde;o, <b>sesenta y dos veces m&aacute;s</b>.</p>
      </div>

      <h3>Una imagen no tiene tama&ntilde;o: tiene p&iacute;xeles</h3>
      <p>Esta frase es la que arregla la presentaci&oacute;n de 48 MB. Preguntar
         &laquo;&iquest;cu&aacute;ntos cent&iacute;metros mide esta foto?&raquo; no tiene respuesta
         hasta que alguien decide <b>cu&aacute;ntos p&iacute;xeles pone en cada
         cent&iacute;metro</b>. Y lo que se ve en una diapositiva proyectada son, como mucho,
         <b>1.920 &times; 1.080</b>: eso es todo lo que puede ense&ntilde;ar el proyector.</p>

''' + ESCENA_PESO + u'''
      <div class="copiar">
        <h4>Resoluci&oacute;n y destino</h4>
        <p><b>P&iacute;xeles</b>: cu&aacute;ntos puntos tiene la imagen. Es lo &uacute;nico que
           lleva dentro el fichero.</p>
        <p><b>Puntos por pulgada (ppp)</b>: cu&aacute;ntos p&iacute;xeles decides poner en cada
           pulgada al imprimir. De ah&iacute; sale el tama&ntilde;o en cent&iacute;metros, y no
           antes.</p>
        <p>Los tres destinos que hay que saberse:</p>
        <ul>
          <li><b>Diapositiva o pantalla</b>: 1.920 p&iacute;xeles de ancho <b>y ni uno m&aacute;s</b>.</li>
          <li><b>Impresi&oacute;n</b>: unos <b>300 ppp</b>. Una A4 entera son 2.480 &times; 3.508.</li>
          <li><b>Miniatura en una web</b>: unos pocos cientos de p&iacute;xeles.</li>
        </ul>
        <p>Todo lo que lleves por encima de eso <b>ocupa, viaja y tarda</b>, y no lo ve nadie.</p>
      </div>

      <h3>Comprimir: tirar lo que no se nota</h3>
      <p>Faltan los 32 MB del principio. Comprimir es guardar lo mismo ocupando menos, y hay dos
         maneras muy distintas de hacerlo.</p>

      <div class="copiar">
        <h4>Compresi&oacute;n sin p&eacute;rdida y con p&eacute;rdida</h4>
        <p><b>Sin p&eacute;rdida</b> (PNG): se aprovecha que hay cosas repetidas &mdash;doscientos
           p&iacute;xeles blancos seguidos se guardan como &laquo;doscientos blancos&raquo;&mdash;.
           Al abrirla sale <b>exactamente</b> la misma imagen. Funciona muy bien con dibujos y
           capturas de pantalla, que tienen zonas planas, y muy mal con fotos.</p>
        <p><b>Con p&eacute;rdida</b> (JPEG): se <b>tira</b> informaci&oacute;n de la que el ojo no
           se entera, sobre todo los cambios de color muy finos. Al abrirla sale una imagen
           <b>parecida</b>, no la misma. Funciona muy bien con fotos.</p>
        <p>Consecuencia que casi nadie sabe: cada vez que guardas un JPEG otra vez, <b>vuelve a
           tirar</b>. Reguardar veinte veces la misma foto la estropea de verdad. Con PNG, no.</p>
      </div>

      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; no hace falta copiarlo</span>
        <p>Medido sobre la foto de la caja de tipos de la sesi&oacute;n anterior, la que est&aacute;
           en esta misma web (1.280 &times; 850): en bruto son <b>3.264.000 bytes</b>; el fichero
           que servimos ocupa <b>437.940</b>. Razón: <b>7,5 a 1</b>. Con la calidad m&aacute;s baja
           bajaba a 164.789 bytes &mdash;casi <b>20 a 1</b>&mdash;, pero ah&iacute; ya se ve
           sucia.</p>
        <p>La misma foto guardada en PNG, que no tira nada, ocupa <b>2.412.762 bytes</b>: apenas
           ahorra. Esa es la prueba de por qu&eacute; las fotos van en JPEG y los dibujos en PNG,
           y no al rev&eacute;s.</p>
        <p>&iexcl;Ojo con el n&uacute;mero! La raz&oacute;n de compresi&oacute;n <b>depende de la
           foto</b>: una pared lisa se comprime much&iacute;simo mejor que una multitud. Por eso
           aqu&iacute; se dice <b>sobre qu&eacute; foto</b> est&aacute; medido, en vez de dar una
           cifra general que no significar&iacute;a nada.</p>
        <p>El JPEG es de <b>1992</b> y el PNG, de <b>1996</b>. El PNG naci&oacute; con prisa, como
           recambio libre de un formato anterior cuya compresi&oacute;n result&oacute; estar
           patentada: de un d&iacute;a para otro, usarlo en un programa pod&iacute;a costar dinero.
           No es una an&eacute;cdota: es la misma raz&oacute;n por la que en la sesi&oacute;n
           anterior interesaba que un formato fuera una norma p&uacute;blica y no propiedad de
           alguien.</p>
      </div>

''' + video('video-vector', 'RZywV73MDGM',
            u'&iquest;Qu&eacute; diferencia hay entre una imagen vectorial y un mapa de bits?',
            u'Micro Conocimiento &middot; en espa&ntilde;ol',
            u'Un minuto, del mismo canal que el v&iacute;deo del PDF, para fijar la '
            u'distinci&oacute;n.')) +

  bloque('02', u'Pr&aacute;ctica &middot; 25 min', ficha(
    u'Actividad 9.2 &middot; Poner una presentaci&oacute;n a dieta',
    [u'4.1', u'6.1'], u'Parejas &middot; 25 min &middot; sobre 10', u'''
          <div class="nota">
            <span class="n-tag">Con qu&eacute; se hace</span>
            Con el editor de im&aacute;genes del aula, o con una aplicaci&oacute;n web que no pida
            cuenta ni instalar nada. Cualquiera sirve, siempre que permita <b>redimensionar</b> y
            <b>guardar eligiendo la calidad</b>. Lo que se eval&uacute;a son las cuentas.
          </div>
          <h4>Qu&eacute; hay que hacer</h4>
          <ol class="pasos">
            <li><b>La cuenta en bruto.</b> Mirad en los datos de una foto vuestra
                &mdash;o de una del aula&mdash; cu&aacute;ntos p&iacute;xeles tiene de ancho y de
                alto. Calculad los <b>p&iacute;xeles totales</b> y el <b>peso en bruto</b>
                (&times; 3 bytes). Pasadlo a MB.</li>
            <li><b>La raz&oacute;n de compresi&oacute;n.</b> Anotad lo que ocupa el fichero
                <b>de verdad</b> y dividid: <i>peso en bruto &divide; peso del fichero</i>. Esa es
                la raz&oacute;n de compresi&oacute;n de <b>esa</b> foto. Comparadla con la de otra
                pareja y escribid una frase explicando <b>por qu&eacute; no os sale lo mismo</b>.</li>
            <li><b>A dieta.</b> Redimensionad la foto a <b>1.920 p&iacute;xeles de ancho</b> y
                guardadla con calidad media. Anotad el peso nuevo y calculad el <b>porcentaje
                ahorrado</b>. Miradlas despu&eacute;s las dos a pantalla completa: &iquest;se nota
                la diferencia?</li>
            <li><b>Lo que sobra, con la escena.</b> Con la escena de los p&iacute;xeles, anotad
                <b>qu&eacute; porcentaje sobra</b> de una foto de 12 Mp para los tres destinos.
                Y contestad: para imprimirla en A4, &iquest;sobra o falta?</li>
            <li><b>Un logotipo, de las dos maneras.</b> Dibujad un s&iacute;mbolo sencillo
                &mdash;dos o tres figuras&mdash; en un editor de dibujo, y guardadlo en <b>SVG</b> y
                en <b>PNG de 1.000 p&iacute;xeles</b>. Anotad los dos pesos, ampliad los dos al
                <b>800 %</b> y describid lo que ve&iacute;s. Abrid adem&aacute;s el SVG con un
                editor de texto y pegad en el cuaderno <b>las tres primeras l&iacute;neas</b>.</li>
            <li><b>La presentaci&oacute;n.</b> Con lo anterior, calculad cu&aacute;nto
                ocupar&iacute;a una presentaci&oacute;n de <b>once fotos</b> antes y despu&eacute;s
                de la dieta, y decid si cabe en un correo (el l&iacute;mite habitual son
                <b>25 MB</b>).</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>El peso en bruto est&aacute; bien calculado, con unidades <b>(2 puntos)</b>.</li>
            <li>La raz&oacute;n de compresi&oacute;n est&aacute; bien y la frase explica que
                <b>depende de la foto</b> <b>(2 puntos)</b>.</li>
            <li>El porcentaje ahorrado al redimensionar est&aacute; bien y va acompa&ntilde;ado de
                la comparaci&oacute;n mirando las dos <b>(2 puntos)</b>.</li>
            <li>Los datos de la escena est&aacute;n tomados de los tres destinos y la respuesta de
                la A4 distingue <b>sobrar</b> de <b>faltar</b> <b>(2 puntos)</b>.</li>
            <li>El logotipo est&aacute; guardado de las dos maneras, con los dos pesos y lo que se
                ve al ampliar <b>(2 puntos)</b>.</li>
          </ul>
          <div class="nota" style="margin-top:14px">
            <span class="n-tag">Aviso sobre el paso 3</span>
            Trabajad sobre una <b>copia</b>. Redimensionar tira p&iacute;xeles <b>para siempre</b>:
            si luego hace falta la foto grande, de la peque&ntilde;a no se saca. Se puede quitar,
            no se puede devolver.
          </div>
  ''')) +

  bloque('03', u'Cierre &middot; 5 min', u'''
      <ol>
      ''' + pregunta(u'Arrastras la esquina de una foto en la diapositiva para hacerla peque&ntilde;a. &iquest;Pesa menos el fichero?',
                     u'<p>No. Has cambiado <b>c&oacute;mo se dibuja</b>, no lo que hay guardado: los doce millones de p&iacute;xeles siguen ah&iacute; enteros. Para que pese menos hay que <b>redimensionar de verdad</b>, o sea, tirar p&iacute;xeles. Es el mismo l&iacute;o de la sesi&oacute;n anterior: confundir lo que una cosa es con lo que parece.</p>')
        + pregunta(u'&iquest;Por qu&eacute; un logotipo se guarda en SVG y una fotograf&iacute;a no?',
                   u'<p>Porque un logotipo son <b>pocas figuras</b> &mdash;c&iacute;rculos, rectas, curvas&mdash; y eso se escribe con unas cuantas instrucciones que se redibujan a cualquier tama&ntilde;o, desde un carn&eacute; hasta una pancarta. Una foto son millones de manchas de color que no se parecen a ninguna figura: describirlas una a una ocupar&iacute;a m&aacute;s que guardar los p&iacute;xeles.</p>')
        + pregunta(u'Tienes una captura de pantalla con texto. &iquest;JPEG o PNG? &iquest;Por qu&eacute;?',
                   u'<p><b>PNG.</b> Una captura tiene zonas planas y bordes muy marcados, que es justo donde el PNG comprime bien <b>sin tirar nada</b>. El JPEG, en cambio, tira los detalles finos, y lo primero que estropea son los bordes de las letras: el texto sale con sombras sucias alrededor.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        La presentaci&oacute;n ya cabe. Ahora hay que <b>contarla en cinco minutos</b> delante de
        la clase. Y ah&iacute; aparece una pregunta que nadie se hace: cuando pones el texto en la
        diapositiva y adem&aacute;s lo dices en voz alta, <b>&iquest;qu&eacute; hace la clase, leer
        o escuchar?</b> No puede hacer las dos cosas, y se puede medir cu&aacute;l gana.
      </div>
  '''))


# ==========================================================================
# SESION 3 · Presentar sin matar de aburrimiento
# ==========================================================================
S3 = (
  bloque('00', u'Reto inicial &middot; 10 min', u'''
      <p>Ya sabes hacer un documento que no se descoloca y meterle im&aacute;genes que no pesan
         media vida. Queda lo m&aacute;s dif&iacute;cil: <b>cinco minutos, de pie, contando lo que
         ha hecho tu grupo</b>.</p>

      <div class="aviso">
        <span class="n-tag">El encargo</span>
        Sin pensarlo mucho, escribe dos cosas en el cuaderno: <b>cu&aacute;ntas diapositivas</b>
        har&iacute;as para esos cinco minutos, y <b>qu&eacute; pondr&iacute;as exactamente</b> en la
        primera. Copia la primera diapositiva tal cual, con sus palabras.
      </div>

      <p>Lo que sale casi siempre: entre <b>doce y veinte</b> diapositivas, y en la primera, un
         t&iacute;tulo y cuatro o cinco frases con lo que hay que decir. Tiene toda la
         l&oacute;gica del mundo: si lo que tengo que contar est&aacute; escrito ah&iacute;, no se
         me olvida.</p>

      <p>El problema es que quien te escucha tiene <b>un solo sitio</b> donde meter palabras, y
         t&uacute; se lo est&aacute;s llenando por dos sitios a la vez. Vamos a medirlo. Pega tu
         primera diapositiva en la caja de abajo &mdash;o usa la que viene puesta&mdash; y mira las
         dos barras.</p>

''' + ESCENA_CARRERA + u'''
      <p>Ese hueco amarillo es lo que hay que entender hoy. No es que la gente sea maleducada: es
         que <b>leer va m&aacute;s r&aacute;pido que escuchar</b>, siempre. Cuando terminan de leer
         tu diapositiva ya saben c&oacute;mo acaba la frase, y t&uacute; todav&iacute;a est&aacute;s
         por la mitad. A partir de ah&iacute; te han dejado de escuchar, y con razón.</p>
  ''') +

  bloque('01', u'Teor&iacute;a &middot; 20 min', u'''
      <h3>La diapositiva no es el gui&oacute;n</h3>
      <p>La soluci&oacute;n no es &laquo;poner menos texto&raquo; como quien pide un favor. Es
         entender <b>para qu&eacute; sirve cada cosa</b>, que son tres cosas distintas y suelen
         estar aplastadas en una.</p>

      <div class="copiar">
        <h4>Tres cosas que no son la misma</h4>
        <ul>
          <li>El <b>gui&oacute;n</b>: lo que vas a <b>decir</b>. Va en las notas del orador o en
              una ficha en la mano. <b>No se proyecta.</b></li>
          <li>La <b>diapositiva</b>: lo que la clase tiene que <b>ver</b> mientras hablas. Una
              idea, y lo que haga falta para entenderla.</li>
          <li>El <b>documento</b>: lo que se llevan para <b>consultar</b> despu&eacute;s. Ese
              s&iacute; lleva todo el texto, y es el de las sesiones anteriores.</li>
        </ul>
        <p>Cuando alguien intenta que la diapositiva haga los tres papeles a la vez, sale una
           p&aacute;gina de libro proyectada en una pared: mala de ver, mala de leer y mala de
           escuchar.</p>
      </div>

      <h3>Una idea por diapositiva</h3>
      <p>La regla pr&aacute;ctica que se deduce de la carrera de antes: si la diapositiva se lee en
         cinco segundos, no compite contigo; si se lee en veinte, s&iacute;. Y como se tarda un
         rato en cada diapositiva, de ah&iacute; sale tambi&eacute;n <b>cu&aacute;ntas caben</b>.</p>

      <div class="copiar">
        <h4>Cuentas que se pueden hacer antes de presentar</h4>
        <ul>
          <li><b>Palabras por diapositiva.</b> M&aacute;s de <b>25</b> y ya est&aacute;s compitiendo
              contigo mismo. Se cuentan, no se calculan a ojo.</li>
          <li><b>Ideas por diapositiva: una.</b> Si al resumirla te salen dos frases con
              &laquo;y adem&aacute;s&raquo;, son dos diapositivas.</li>
          <li><b>Cu&aacute;ntas diapositivas.</b> Si en cada una te vas a parar unos
              <b>40 segundos</b>, en 5 minutos (300 s) caben <b>300 &divide; 40 &asymp; 7</b>. No
              quince.</li>
        </ul>
      </div>

      <h3>La imagen que explica y la que decora</h3>
      <p>Aqu&iacute; hay una prueba que no admite discusi&oacute;n y se hace en tres segundos:</p>

      <div class="reto-piensa">
        <span class="n-tag">La prueba del pulgar</span>
        <p><b>Tapa la imagen con la mano.</b> Si la diapositiva se entiende igual de bien, la
           imagen <b>decoraba</b>. Si deja de entenderse, la imagen <b>explicaba</b>: eso es una
           imagen que se gana el sitio.</p>
      </div>

      <p>Un gr&aacute;fico con los datos de tu ensayo explica. Un esquema de tu mecanismo explica.
         Una foto de un bombillo brillando al lado de un t&iacute;tulo que pone &laquo;ideas&raquo;
         no explica nada: est&aacute; ocupando sitio y atenci&oacute;n.</p>

''' + foto('u9-ponencia.jpg',
           u'Una ponente hablando ante un atril, con un mapa proyectado a su lado en el que solo '
           u'hay cuatro letras rotuladas',
           u'Una ponencia de verdad, en un congreso. Mira la pantalla: <b>no hay ni una frase</b>. '
           u'Hay un mapa con una l&iacute;nea amarilla y cuatro letras. Esa diapositiva no se puede '
           u'leer en voz alta &mdash;no hay nada que leer&mdash;, as&iacute; que solo sirve para lo '
           u'que tiene que servir: <b>ense&ntilde;ar de qu&eacute; est&aacute; hablando ella</b>. '
           u'La imagen explica; la persona cuenta. Y lo que hay que retener no est&aacute; en la '
           u'pared, est&aacute; en lo que dice.',
           u'Mozel W.', u'CC BY-SA 4.0',
           u'https://commons.wikimedia.org/wiki/File:Snjezana_Kordic_keynote_presentation_Hokkaido_University.jpg') + u'''
      <h3>Y una cosa que no es opini&oacute;n: si se lee o no se lee</h3>
      <p>&laquo;Pon la letra grande&raquo; no es un consejo, es una cuenta. El cuerpo de letra que
         eliges en la diapositiva se convierte en mil&iacute;metros sobre la pantalla, y esos
         mil&iacute;metros o llegan a la &uacute;ltima fila o no llegan. Juega con la escena:
         cambia el cuerpo, el tama&ntilde;o de la pantalla y la fila.</p>

''' + ESCENA_AULA + u'''
      <div class="copiar">
        <h4>La cuenta del cuerpo m&iacute;nimo</h4>
        <p>Una diapositiva 16:9 mide <b>33,87 cm de ancho</b> por dentro, y un punto
           tipogr&aacute;fico son <b>0,3528 mm</b>. Con eso:</p>
        <ol>
          <li>Altura de la may&uacute;scula en la diapositiva = <i>cuerpo</i> &times; 0,3528 &times;
              <b>0,72</b>.</li>
          <li>El proyector lo multiplica por <i>ancho proyectado &divide; 0,3387 m</i>.</li>
          <li>Hace falta que el resultado llegue a <b>la distancia dividida entre 200</b>.</li>
        </ol>
        <p>Con una pantalla de <b>2,5 m</b> y una &uacute;ltima fila a <b>9 m</b> salen
           <b>24 pt exactos</b>, y no es casualidad del redondeo: 24 pt son un tercio de pulgada,
           la may&uacute;scula sube 0,24 pulgadas, la pantalla agranda 2,5 m entre 13 pulgadas y
           un tercio&hellip; y da <b>45 mm clavados</b>, que es 9 m entre 200. De ah&iacute; viene
           el consejo de no bajar de 24, que casi siempre se da sin decir de d&oacute;nde sale.</p>
        <p>El <b>0,72</b> es lo que sube una may&uacute;scula respecto al cuerpo. El
           <b>&divide;&nbsp;200</b> es criterio nuestro, no una norma: equivale a que la letra
           llegue al ojo con unos 17 minutos de arco.</p>
      </div>

      <div class="copiar" style="border-color:var(--goo-verde)">
        <h4>Rúbrica: c&oacute;mo se mira una presentaci&oacute;n sin opinar</h4>
        <p>Seis cosas que se <b>cuentan</b>, y que por eso valen para corregir la tuya o la de otro
           grupo:</p>
        <table>
          <tr><th>Qu&eacute; se mira</th><th>C&oacute;mo se comprueba</th></tr>
          <tr><td>Palabras por diapositiva</td><td>Se cuentan. &iquest;Pasa de 25?</td></tr>
          <tr><td>Ideas por diapositiva</td><td>Res&uacute;mela en una frase. &iquest;Salen dos?</td></tr>
          <tr><td>Cuerpo de letra</td><td>&iquest;Baja de 24 pt en alguna?</td></tr>
          <tr><td>Im&aacute;genes</td><td>Prueba del pulgar: &iquest;cu&aacute;ntas decoran?</td></tr>
          <tr><td>Ritmo</td><td>Diapositivas &divide; minutos. &iquest;Pasa de una cada 40 s?</td></tr>
          <tr><td>Procedencia</td><td>&iquest;Est&aacute; dicho de d&oacute;nde sale cada dato y cada foto?</td></tr>
        </table>
      </div>

      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; no hace falta copiarlo</span>
        <p>Esto no es una man&iacute;a de profesor. En <b>2003</b> se desintegr&oacute; al volver a
           la atm&oacute;sfera el transbordador espacial <i>Columbia</i>, y murieron siete
           personas. La comisi&oacute;n oficial que investig&oacute; el accidente dedic&oacute; un
           apartado de su informe a algo inesperado: la <b>manera de comunicarse</b> dentro de la
           NASA. Los an&aacute;lisis t&eacute;cnicos sobre el da&ntilde;o que hab&iacute;a
           sufrido el ala se hab&iacute;an presentado en <b>diapositivas</b> en vez de en informes,
           y en una de ellas la advertencia importante estaba metida en el tercer nivel de una
           lista, en letra m&aacute;s peque&ntilde;a que el titular que dec&iacute;a que todo
           estaba bajo control.</p>
        <p>La comisi&oacute;n no dijo que las diapositivas maten. Dijo que <b>resumir</b> tiene un
           precio: cuando algo se aplasta hasta caber en una l&iacute;nea, se pierde lo que lo
           hac&iacute;a importante. Por eso hay una tercera cosa en la lista de arriba, el
           <b>documento</b>: lo que no cabe en la diapositiva no desaparece, se escribe.</p>
      </div>

''' + video('video-presentar', 'zRoxXHR_-Ac',
            u'Muerte por PowerPoint: trucos para no aburrir a la audiencia',
            u'La Hoguera Bloguera &middot; en espa&ntilde;ol',
            u'Los errores de siempre, vistos desde fuera. Lo que dice se solapa con la '
            u'r&uacute;brica de arriba: comprobadlo mientras lo ve&iacute;s.')) +

  bloque('02', u'Pr&aacute;ctica &middot; 25 min', ficha(
    u'Actividad 9.3 &middot; Rehacer una diapositiva y medir el aula',
    [u'4.1', u'2.1'], u'Parejas &middot; 25 min &middot; sobre 10', u'''
          <h4>Qu&eacute; hay que hacer</h4>
          <ol class="pasos">
            <li><b>Medid vuestra propia diapositiva.</b> Coged la que escribisteis al principio de
                la sesi&oacute;n, contad sus <b>palabras</b> y calculad el tiempo de lectura a
                <b>200 palabras por minuto</b>. Compradlo con los segundos que pensabais dedicarle.
                Comprobadlo luego en la escena.</li>
            <li><b>Rehacedla.</b> Partidla en dos: a la <b>diapositiva</b> se queda <b>una idea</b>
                (menos de 25 palabras, o ninguna si hay una imagen que explique); todo lo
                dem&aacute;s se va a las <b>notas del orador</b>. Pegad las dos versiones en el
                cuaderno, una al lado de la otra.</li>
            <li><b>Medid el aula de verdad.</b> Con pasos, medid <b>a qu&eacute; distancia</b>
                est&aacute; la &uacute;ltima fila de la pizarra y <b>cu&aacute;nto mide de ancho</b>
                la imagen proyectada. Con la escena, calculad el <b>cuerpo m&iacute;nimo</b> que
                hay que usar en esta clase concreta. Escribid el n&uacute;mero.</li>
            <li><b>Comprobadlo.</b> Escribid una palabra con ese cuerpo, proyectadla y que alguien
                la lea desde el fondo. Si no se lee, subid hasta que se lea y anotad la diferencia
                con lo calculado. Y decid a qu&eacute; puede deberse: &iquest;la luz de la clase?
                &iquest;el contraste? &iquest;la tipograf&iacute;a?</li>
            <li><b>Corregid a otro grupo.</b> Con la <b>r&uacute;brica</b> de las seis
                l&iacute;neas, puntuad la presentaci&oacute;n de otra pareja. No vale
                &laquo;est&aacute; bien&raquo;: hay que poner <b>n&uacute;meros</b> en cada fila y
                decir qu&eacute; hay que cambiar.</li>
            <li><b>Ensayad con reloj.</b> Contadlo en voz alta, de pie y cronometrado. Anotad
                cu&aacute;nto os hab&eacute;is pasado o cu&aacute;nto os ha sobrado, y
                <b>qu&eacute; diapositiva</b> sobra.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>El recuento de palabras y el tiempo de lectura est&aacute;n bien hechos
                <b>(2 puntos)</b>.</li>
            <li>La diapositiva rehecha tiene <b>una idea</b> y el resto est&aacute; en las notas, no
                borrado <b>(2 puntos)</b>.</li>
            <li>El aula est&aacute; medida de verdad y el cuerpo m&iacute;nimo sale de la cuenta,
                con unidades <b>(2 puntos)</b>.</li>
            <li>La comprobaci&oacute;n se ha hecho proyectando, y la diferencia est&aacute;
                razonada <b>(2 puntos)</b>.</li>
            <li>La r&uacute;brica del otro grupo lleva <b>n&uacute;meros en las seis filas</b> y una
                propuesta concreta <b>(2 puntos)</b>.</li>
          </ul>
          <div class="nota" style="margin-top:14px">
            <span class="n-tag">Sobre el paso 5</span>
            Corregir a otro grupo es f&aacute;cil si se hace con n&uacute;meros y desagradable si se
            hace con adjetivos. &laquo;Ocho diapositivas tienen m&aacute;s de 25 palabras&raquo; se
            puede arreglar; &laquo;es aburrida&raquo;, no.
          </div>
  ''')) +

  bloque('03', u'Cierre &middot; 5 min', u'''
      <ol>
      ''' + pregunta(u'Si en la diapositiva pones lo que vas a decir, &iquest;por qu&eacute; dejan de escucharte?',
                     u'<p>Porque leer va m&aacute;s r&aacute;pido que escuchar. La clase termina de leer la diapositiva antes de que t&uacute; acabes la frase, y desde ese momento ya sabe c&oacute;mo acaba: no le queda nada que sacar de lo que dices. El texto que ibas a decir <b>no se borra</b>, se pasa a las <b>notas del orador</b>.</p>')
        + pregunta(u'&iquest;C&oacute;mo se sabe si una imagen se gana el sitio en una diapositiva?',
                   u'<p>Con la prueba del pulgar: <b>t&aacute;pala</b>. Si la diapositiva se entiende igual, esa imagen <b>decoraba</b> y estorba. Si al taparla deja de entenderse, es que la imagen estaba <b>explicando</b> algo, y esa se queda.</p>')
        + pregunta(u'&iquest;De d&oacute;nde sale lo de &laquo;no bajes de 24 puntos&raquo;?',
                   u'<p>De una cuenta, no de una costumbre. El cuerpo se convierte en mil&iacute;metros de may&uacute;scula sobre la diapositiva, el proyector lo multiplica por lo que estire la imagen, y desde la &uacute;ltima fila hace falta una altura m&iacute;nima para leer sin esfuerzo. Con una pantalla de 2,5 m y un aula de 9 m de fondo, salen justo 24 pt. En otra clase sale <b>otro n&uacute;mero</b>, y por eso se mide.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Lo que llevas del tema</span>
        Las tres piezas de producir algo: un <b>documento</b> que no se descoloca porque lo que
        dice va separado de c&oacute;mo se ve; unas <b>im&aacute;genes</b> que pesan lo que tienen
        que pesar porque sabes cu&aacute;ntos p&iacute;xeles llegan a verse; y una
        <b>presentaci&oacute;n</b> que se puede corregir con n&uacute;meros en vez de con opiniones.
      </div>
      <div class="nota">
        <span class="n-tag">Lo que falta</span>
        Quedan tres sesiones y van todas de lo mismo: <b>difundir</b>. Qu&eacute; se puede copiar y
        con qu&eacute; condiciones &mdash;derechos de autor, licencias libres y c&oacute;mo se cita
        una foto&mdash;; c&oacute;mo se trabaja <b>a varias manos</b> en el mismo documento sin
        pisarse y sin perder el trabajo de nadie; y c&oacute;mo se <b>publica</b> algo para que
        llegue y para que lo pueda usar todo el mundo, incluida la gente que no ve la pantalla.
      </div>
      <div class="nota">
        <span class="n-tag">Y con esto se cierra un c&iacute;rculo</span>
        Al principio del curso, en la unidad de representaci&oacute;n gr&aacute;fica, aprendiste a
        <b>explicar una idea con un dibujo</b> para que otra persona pudiera construirla sin
        preguntarte nada. Es el <b>mismo criterio del curr&iacute;culo</b> que esta unidad, y no es
        casualidad: aquello era comunicar con un l&aacute;piz y esto es comunicar con un ordenador.
        Lo que no cambia es la exigencia: que quien lo reciba <b>entienda exactamente lo que
        quer&iacute;as decir</b>, sin estar t&uacute; delante.
      </div>
  '''))


# ==========================================================================
S = [
  dict(corto=u'El documento que no se rompe',
       titulo=u'El documento que no se rompe',
       entradilla=u'Un trabajo se descoloca al abrirlo en otro ordenador y no falta ni una palabra. '
                  u'La explicaci&oacute;n reparte la unidad entera: lo que dice y c&oacute;mo se ve '
                  u'son dos cosas.',
       minutado=[(u"10'", u'Reto'), (u"20'", u'Teor&iacute;a'), (u"25'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')],
       chips=[u'CE4 &middot; 4.1', u'CE6 &middot; 6.1', u'B.2 &middot; D.1'],
       cuerpo=S1),
  dict(corto=u'Una imagen pesa lo que pesa',
       titulo=u'Una imagen pesa lo que pesa',
       entradilla=u'Una foto de m&oacute;vil son 35 MB en bruto y el fichero dice 3. Entre esas dos '
                  u'cifras est&aacute;n la rejilla de p&iacute;xeles, la compresi&oacute;n y la '
                  u'diferencia entre guardar casillas y guardar instrucciones.',
       minutado=[(u"10'", u'Reto'), (u"20'", u'Teor&iacute;a'), (u"25'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')],
       chips=[u'CE4 &middot; 4.1', u'CE6 &middot; 6.1', u'B.2 &middot; D.1'],
       cuerpo=S2),
  dict(corto=u'Presentar sin aburrir',
       titulo=u'Presentar sin matar de aburrimiento',
       entradilla=u'Leer va m&aacute;s r&aacute;pido que escuchar, y eso se mide. De ah&iacute; sale '
                  u'todo lo dem&aacute;s: una idea por diapositiva, la imagen que explica y un '
                  u'cuerpo de letra que llega al fondo del aula.',
       minutado=[(u"10'", u'Reto'), (u"20'", u'Teor&iacute;a'), (u"25'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')],
       chips=[u'CE4 &middot; 4.1', u'CE2 &middot; 2.1', u'B.1 &middot; B.3'],
       cuerpo=S3),
  dict(corto=u'Lo que se puede copiar', pendiente=True),
  dict(corto=u'A varias manos', pendiente=True),
  dict(corto=u'Publicar y que llegue', pendiente=True),
]

CFG = dict(
 ruta='2eso/TyD/tema9/',
 migas=u'<a href="../../../">Materiales</a> &middot; <a href="../../">2.&ordm; ESO</a> '
       u'&middot; <a href="../">TyD</a> &middot; Tema 9',
 h1=u'Herramientas digitales y difusi&oacute;n',
 titulo=u'Tema 9 &middot; Herramientas digitales y difusi&oacute;n',
 tema=u'Tema 9', curso=u'2.&ordm; de ESO', materia=u'Tecnolog&iacute;a y Digitalizaci&oacute;n',
 desc=u'Tema 9 de Tecnolog&iacute;a y Digitalizaci&oacute;n de 2.&ordm; de ESO: formatos de '
      u'fichero, estilos frente a formato a mano y por qu&eacute; un PDF se ve igual en todas '
      u'partes; mapa de bits y vectorial, resoluci&oacute;n y compresi&oacute;n; y c&oacute;mo se '
      u'hace una presentaci&oacute;n que se pueda evaluar con n&uacute;meros.',
 sesiones=S)


# Dos anadidos al molde: el CSS del avatar (que vive en avatar_flat, no en
# tema0_base) y el de las tablas dentro de los bloques que se copian, igual que
# en la U8. La tercera regla es de aqui: la escena de la carrera lleva una caja
# de texto dentro de una .escena-barra y, sin esto, en el movil se sale.
EXTRA_CSS = avatar_flat.CSS + u"""
/* tablas de datos dentro de los bloques que se copian */
.copiar table{border-collapse:collapse;width:100%;margin:10px 0 4px;font-size:14.5px}
.copiar th,.copiar td{border:1px solid var(--line);padding:6px 9px;text-align:left}
.copiar th{background:var(--surface-2);font-family:var(--f-m);font-size:11.5px;
  letter-spacing:.06em;text-transform:uppercase;color:var(--ink-soft);font-weight:500}
.copiar td:first-child{width:38%}
@media (max-width:560px){.copiar table{font-size:13px}.copiar th,.copiar td{padding:5px 6px}}
/* listas dentro de una lista de pasos: que no se peguen al texto de arriba */
.pasos ul{margin:6px 0 2px}
/* la caja de texto de la escena de la carrera: que no desborde a lo ancho */
.escena-barra textarea{max-width:100%;box-sizing:border-box}
"""

if __name__ == '__main__':
    html = pagina(CFG).replace(u'</style>', EXTRA_CSS + u'</style>', 1)
    destino = os.path.join(RAIZ, '2eso', 'TyD', 'tema9')
    os.makedirs(destino, exist_ok=True)
    io.open(os.path.join(destino, 'index.html'), 'w', encoding='utf-8', newline='').write(html)
    print('U9 generada: %d bytes, %d sesiones (%d escritas)' % (
        len(html), len(S), sum(1 for x in S if not x.get('pendiente'))))
