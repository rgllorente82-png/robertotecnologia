# -*- coding: utf-8 -*-
u"""4.o de ESO - Tecnologia - Tema 7 - Robotica y automatismos.

    ~/venv/bin/python generadores/c7_build.py

Escribe 4eso/Tecnologia/tema7/index.html. La "c" de los generadores de esta
unidad es de "cuarto": no choca con los u*_ de 2.o.

Criterios: CE4 / 4.1 / saberes B.1 a B.4. Ver CURRICULO.md.

La pregunta que abre la unidad: una maquina que se corrige sola ya la tienes
(U4). Que le falta para moverse por el mundo y hacer algo util sin que nadie
la vigile?

Ocho sesiones. Aqui van escritas las CUATRO PRIMERAS; las otras cuatro salen
en la barra con su titulo y el boton desactivado, para que se vea a donde va
la unidad entera desde el primer dia.

El hilo, que es lo que importa:
  S1  Un lavavajillas tiene programa, tiene motores y hasta tiene sensores, y
      no es un robot. La frontera util no es el aspecto: es si la maquina se
      entera del ENTORNO y si lo que hace cambia cuando el entorno cambia.
      Se ve fallar de verdad: el programa grabado pierde media aula en cuanto
      alguien mueve una mesa, y no se entera.
      Deja abierto: en el mundo no hay casillas. Hay motores.
  S2  "Avanza medio metro" no se le puede decir a un motor de corriente
      continua, porque un motor no sabe donde esta. Tres motores con el mismo
      encargo, cinco intentos cada uno, y la pareja de palabras que se lleva
      la sesion: exactitud y precision.
      Deja abierto: ya se cuanto ha girado cada eje; no se donde acaba la punta.
  S3  De los angulos al sitio: cinematica directa de un brazo de dos eslabones.
      Grados de libertad, espacio de trabajo, y el problema inverso planteado
      (dos soluciones, o ninguna). Y el error angular, multiplicado por el brazo.
      Deja abierto: ya se a donde ir; no se en que orden ni que hacer si algo
      llega cuando no toca.
  S4  Maquina de estados: cuatro estados, cinco eventos, veinte casillas. Y el
      delay(), que no es una pausa: es un rato en el que el programa no mira.

El proyecto del curso NO esta decidido (ver PROYECTOS.md e INFORME.md), asi
que ningun ejemplo se casa con uno: cada vez que hace falta un caso concreto
se usan dos o tres de los cinco candidatos.

La placa de 4.o es Arduino, no micro:bit.
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unidad_base import pagina, bloque, ficha, pregunta
import avatar_flat
from c7_escenas import AULA, RECORRIDO
from c7_escenas2 import BRAZO, ESTADOS
from test_auto import test
import c7b_texto

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USA_AVATAR = [False]
PENDIENTES = []


# --------------------------------------------------------------------------
# Piezas repetidas
# --------------------------------------------------------------------------
def foto(src, alt, pie, autor, licencia, commons):
    if not os.path.exists(os.path.join(RAIZ, 'img', src)):
        PENDIENTES.append(u'FALTA LA FOTO img/' + src)
        return u''
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


def narrador():
    """La voz de la unidad. Solo se monta si estan el mp3 y su envolvente."""
    env = os.path.join(RAIZ, '_env_c7-robotica.json')
    mp3 = os.path.join(RAIZ, 'audio', 'c7-robotica.mp3')
    if not (os.path.exists(env) and os.path.exists(mp3)):
        PENDIENTES.append(u'FALTA LA VOZ audio/c7-robotica.mp3')
        return u''
    USA_AVATAR[0] = True
    return avatar_flat.componente(
        'narr-c7', u'De qu&eacute; va esta unidad',
        u'Ya tienes una m&aacute;quina que se corrige sola. &iquest;Qu&eacute; le falta para '
        u'moverse por el mundo y hacer algo &uacute;til sin que nadie la vigile?',
        '../../../audio/c7-robotica.mp3',
        json.load(io.open(env, encoding='utf-8')),
        u'Voz sintetizada sobre gui&oacute;n propio. La boca sigue el volumen real de la voz.')


# ==========================================================================
# SESION 1 - Que es un robot y que no
# ==========================================================================
S1_RETO = u'''
      <p>Llevas tres unidades montando una m&aacute;quina que se apa&ntilde;a sola. En la
         <b>U4</b> hiciste que se corrigiera: un sensor mide, algo compara con la consigna y un
         actuador empuja hasta que el n&uacute;mero cuadra. En la <b>U5</b> le pusiste la
         electr&oacute;nica que hace falta para mover algo de verdad. En la <b>U6</b> la programaste
         y hasta la conectaste para que avisara desde lejos.</p>
      <p>Y con todo eso dentro, a nadie se le ocurrir&iacute;a llamar robot a un horno.</p>
'''

S1_RETO_B = u'''
      <div class="aviso">
        <span class="n-tag">El encargo &middot; tres minutos, en la libreta</span>
        Aqu&iacute; hay nueve m&aacute;quinas. Poned <b>S&iacute;</b> o <b>No</b> en cada una, sin
        pensarlo mucho: <i>lavavajillas &middot; robot aspirador &middot; ascensor &middot;
        sem&aacute;foro &middot; brazo de una f&aacute;brica de coches &middot; coche teledirigido
        &middot; impresora 3D &middot; dron que vuelve solo &middot; molinillo de caf&eacute;</i>.
        Luego escribid <b>en qu&eacute; os hab&eacute;is basado</b>.
      </div>
      <p>Comparad la lista con la del grupo de al lado. No van a coincidir, y lo interesante es
         <b>por qu&eacute;</b>. Las tres razones que aparecen siempre son estas, y las tres se caen
         solas:</p>
      <ul>
        <li>&laquo;<b>Parece un mu&ntilde;eco</b>&raquo;. El brazo de la f&aacute;brica no se parece
            a nada vivo y todo el mundo lo llama robot; un peluche que anda se parece mucho y no lo
            es.</li>
        <li>&laquo;<b>Se mueve</b>&raquo;. El ascensor se mueve, el molinillo se mueve, y la
            impresora 3D se mueve en tres ejes a la vez.</li>
        <li>&laquo;<b>Tiene un programa</b>&raquo;. El lavavajillas tiene un programa y lo cumple
            entero. El sem&aacute;foro tambi&eacute;n.</li>
      </ul>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento antes de seguir</span>
        <p>El lavavajillas tiene adem&aacute;s <b>sensores</b>: un term&oacute;stato que mira la
           temperatura del agua y un press&oacute;stato que mira el nivel. As&iacute; que &laquo;tener
           sensor&raquo; tampoco vale para separarlos. &iquest;Qu&eacute; diferencia hay entonces
           entre lo que mira el lavavajillas y lo que mira el aspirador?</p>
      </div>
      <p>El lavavajillas se mira <b>a s&iacute; mismo</b>: su agua, su temperatura, su tiempo. Le da
         exactamente igual lo que haya dentro. Puedes meter dos platos o veinte, o ninguno, y el
         programa de 1&nbsp;h&nbsp;47&nbsp;min dura 1&nbsp;h&nbsp;47&nbsp;min. El aspirador, en
         cambio, se entera de <b>lo que hay fuera</b>: una pared, una pata de silla, una mochila que
         ayer no estaba.</p>
      <p>Y de ah&iacute; sale la pregunta que s&iacute; separa las nueve m&aacute;quinas de la lista,
         y que cabe en una l&iacute;nea:</p>
      <div class="nota">
        <span class="n-tag">La pregunta</span>
        <b>Si cambias el mundo, &iquest;cambia lo que hace la m&aacute;quina?</b>
      </div>
'''

S1_TEORIA = u'''
      <div class="copiar">
        <h4>Qu&eacute; es un robot</h4>
        <p>Un <b>robot</b> es una m&aacute;quina que <b>percibe su entorno</b>, <b>decide</b> a
           partir de lo que ha percibido y <b>act&uacute;a</b> sobre ese entorno, sin que nadie la
           est&eacute; llevando.</p>
        <p>Son tres cosas, y hay que contestarlas por separado:</p>
        <ol>
          <li><b>&iquest;Percibe el entorno?</b> No basta con tener sensores: hay que mirar
              <b>qu&eacute;</b> miran. Un term&oacute;stato mira la m&aacute;quina; un ultrasonidos
              mira el mundo.</li>
          <li><b>&iquest;Decide?</b> O sea: &iquest;lo que hace depende de lo que ha percibido? Si
              hace lo mismo pase lo que pase, no decide, <b>ejecuta</b>.</li>
          <li><b>&iquest;Act&uacute;a sobre el entorno?</b> Con motores, con una bomba, con una
              v&aacute;lvula. Un programa que solo escribe en una pantalla no act&uacute;a: informa.</li>
        </ol>
        <p>Las tres a la vez, y sin que nadie lo vigile. Falla una y ya no lo es:</p>
        <ul>
          <li>El <b>coche teledirigido</b> falla la 1 y la 2: el que percibe y decide eres t&uacute;.
              Es un actuador con antena.</li>
          <li>El <b>lavavajillas</b> falla la 1 y la 2: sus sensores se miran a s&iacute; mismos y su
              programa no depende de nada de fuera.</li>
          <li>El <b>sem&aacute;foro de tiempo fijo</b> falla la 1. El que lleva una espira en el
              asfalto que cuenta coches, <b>no</b>: ese percibe, decide y act&uacute;a. Est&aacute;
              much&iacute;simo m&aacute;s cerca de ser un robot de lo que parece.</li>
        </ul>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>El brazo de la f&aacute;brica de coches, en cambio, suele <b>fallar la 1</b>: repite una
           secuencia grabada y no mira nada. Todo el mundo lo llama robot, y en la industria se le
           llama as&iacute;, pero lo que hace es de <b>aut&oacute;mata</b>: ejecutar. Por eso a esas
           celdas de fabricaci&oacute;n se las rodea de vallas y se las vac&iacute;a de gente: el
           brazo <b>no se entera</b> de que has entrado.</p>
        <p>No te pelees con la palabra. Lo que sirve son las tres preguntas; la etiqueta la pone
           cada uno.</p>
      </div>

      <h3>Y ahora m&iacute;ralo fallar</h3>
      <p>Aqu&iacute; tienes un aula vista desde arriba, por casillas, y un robot que la limpia. Puedes
         ponerle tres <b>cerebros</b> distintos y luego, con un bot&oacute;n, <b>mover los muebles</b>.
         Empieza por el <b>programa grabado</b> con el aula como estaba, pulsa
         <b>Hasta el final</b> y anota el porcentaje. Despu&eacute;s mueve los muebles y vuelve a
         mirarlo.</p>
''' + AULA + u'''
      <div class="copiar">
        <h4>Lo que acabas de ver, con n&uacute;meros</h4>
        <ul>
          <li>Con el aula <b>como el d&iacute;a que se grab&oacute;</b>, el programa grabado cubre el
              <b>77,3 %</b> en <b>242 pasos</b> y con <b>24</b> choques. El del sensor, con la
              semilla 7, cubre el <b>74,7 %</b> pero necesita <b>900</b> pasos y choca <b>60</b>
              veces. <b>Gana el grabado</b>, y no es raro: sabe por d&oacute;nde ir.</li>
          <li>Mueve los muebles y el programa grabado se queda en el <b>47,2 %</b>, con <b>124</b>
              choques. Ha perdido <b>media aula</b>. El del sensor sube al <b>79,7 %</b>.</li>
          <li>Y lo importante no es el porcentaje: es que el grabado <b>ha chocado 124 veces sin
              enterarse</b>. Ha gastado los pasos igual, contra una mesa, como si estuviera
              limpiando.</li>
        </ul>
        <p>Un robot no es una m&aacute;quina m&aacute;s lista. Es una m&aacute;quina que
           <b>se entera</b>.</p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Cambia la <b>semilla</b> del azar y vuelve a soltar el del sensor. Ver&aacute;s que unas
           veces cubre el 86 % y otras el 58 %: <b>no da siempre lo mismo</b>. El grabado, en cambio,
           da <b>exactamente</b> el mismo n&uacute;mero todas las veces. Las dos cosas son verdad a
           la vez, y las dos cuentan a la hora de elegir: uno es previsible y fr&aacute;gil; el otro,
           robusto e irregular.</p>
      </div>
''' + foto('c7-roomba-recorrido.jpg',
           u'Sal&oacute;n a oscuras fotografiado con exposici&oacute;n larga: el robot aspirador ha '
           u'dejado un rastro de l&iacute;neas amarillas rectas que se cruzan por todo el suelo, con '
           u'algunos bucles cerrados',
           u'Esto no es un dibujo: es una <b>fotograf&iacute;a con el obturador abierto varias '
           u'horas</b>. La l&iacute;nea amarilla es la luz del propio robot aspirador, y lo que se '
           u've es <b>su recorrido entero</b> de una noche. F&iacute;jate: <b>rectas largas que se '
           u'cortan al llegar a un mueble</b> y salen con otro &aacute;ngulo. Eso es exactamente el '
           u'cerebro de &laquo;sensor de choque&raquo; de la escena de arriba, y es el que llevaban '
           u'los primeros modelos, de 2002. Los bucles son la vuelta en espiral que da cuando '
           u'detecta mucha suciedad en un sitio.',
           u'Chris Bartle', u'CC BY 2.0',
           u'https://commons.wikimedia.org/wiki/File:Roomba_time-lapse.jpg') + u'''
      <h3>De d&oacute;nde sale la palabra, y de d&oacute;nde sale el rebote</h3>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p><b>La palabra es de teatro, no de ingenier&iacute;a.</b> La estren&oacute; el checo
           <b>Karel &#268;apek</b> en su obra <i>R.U.R.</i>, escrita en <b>1920</b> y estrenada en
           <b>1921</b>. Viene de <i>robota</i>, que en checo antiguo es el <b>trabajo forzado</b> que
           deb&iacute;a un siervo a su se&ntilde;or. &#268;apek cont&oacute; que la palabra se la
           propuso su hermano <b>Josef</b>, que era pintor. En la obra, los robots no son de metal:
           son de carne artificial, y acaban mal.</p>
        <p><b>El rebote tampoco es de ahora.</b> Entre <b>1948 y 1949</b>, en Bristol, el
           neurofisi&oacute;logo <b>W. Grey Walter</b> construy&oacute; dos m&aacute;quinas del
           tama&ntilde;o de un casco, <i>Elmer</i> y <i>Elsie</i>, con <b>dos v&aacute;lvulas</b>, una
           c&eacute;lula que miraba la luz y un contacto que se cerraba al chocar. Con eso
           buscaban la luz, esquivaban obst&aacute;culos y volv&iacute;an a cargarse solas. Walter
           las llam&oacute; <i>tortugas</i>, y dej&oacute; escrito lo que aqu&iacute; interesa: con
           <b>dos</b> elementos que se miran el uno al otro ya aparece un comportamiento que parece
           intencionado. No hac&iacute;a falta un cerebro grande; hac&iacute;a falta
           <b>realimentaci&oacute;n</b>, que es lo de la U4.</p>
      </div>
''' + video('video-c7-aspirador', 'cwf-cURBUkI',
            u'C&oacute;mo Funciona y se Ensambla un Robot Aspirador',
            u'Canal: Ciencia y Tecnolog&iacute;a al Desnudo',
            u'El aparato por dentro: d&oacute;nde est&aacute;n los sensores de choque, los de '
            u'desnivel y los motores. Vedlo con las tres preguntas del recuadro delante.')

S1_PRACTICA = ficha(
    u'Actividad 1 &middot; La frontera, medida',
    [u'CE4 &middot; 4.1', u'B.1', u'B.2'], u'Parejas &middot; 20 min', u'''
          <h4>Primera parte &middot; los cuatro n&uacute;meros (8 min)</h4>
          <p>Con la escena de arriba, con la <b>semilla 7</b>, y anotando en una tabla de cinco
             columnas (cerebro, muebles, suelo cubierto, choques, pasos):</p>
          <ol class="pasos">
            <li><b>Programa grabado</b> + muebles <i>como el d&iacute;a que se grab&oacute;</i>.
                &laquo;Hasta el final&raquo;. Anotad la fila.</li>
            <li><b>Programa grabado</b> + muebles <i>movidos</i>. Anotad la fila.</li>
            <li><b>Sensor de choque</b> con los dos juegos de muebles. Dos filas m&aacute;s.</li>
          </ol>
          <p>Escribid debajo, en una frase, <b>qu&eacute; columna cambia mucho y cu&aacute;l casi
             no</b>, y por qu&eacute;.</p>
          <h4>Segunda parte &middot; el teledirigido (4 min)</h4>
          <p>Poned <b>Teledirigido</b> y conducidlo <b>un minuto</b> con los botones. Al acabar
             anotad: suelo cubierto, <b>&oacute;rdenes que hab&eacute;is dado</b> y lecturas de
             sensor. Contestad: si os vais de clase, &iquest;qu&eacute; hace la m&aacute;quina?</p>
          <h4>Tercera parte &middot; vuestro proyecto (8 min)</h4>
          <p>Elegid <b>dos</b> de los proyectos del curso &mdash;por ejemplo el <b>riego</b> y el
             <b>contenedor que avisa</b>&mdash; y contestad para cada uno, por escrito, las
             <b>tres preguntas</b> del recuadro:</p>
          <ul>
            <li>&iquest;Qu&eacute; percibe <b>del entorno</b>? (magnitud y sensor concreto)</li>
            <li>&iquest;Qu&eacute; decide, y en funci&oacute;n de qu&eacute;?</li>
            <li>&iquest;Sobre qu&eacute; act&uacute;a?</li>
          </ul>
          <p>Y una cuarta: <b>&iquest;es un robot?</b> Contestad s&iacute; o no y <b>defendedlo</b>
             con vuestras tres respuestas. Las dos contestaciones pueden estar bien; lo que se
             corrige es el argumento.</p>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Las cuatro filas de la tabla, completas <b>(3 puntos)</b>.</li>
            <li>La frase de qu&eacute; columna cambia se&ntilde;ala el programa grabado con los
                muebles movidos <b>(1 punto)</b>.</li>
            <li>Los datos del teledirigido, con las &oacute;rdenes contadas <b>(1 punto)</b>.</li>
            <li>Las tres preguntas contestadas para los dos proyectos, con sensor concreto y no
                &laquo;un sensor&raquo; <b>(3 puntos)</b>.</li>
            <li>La cuarta pregunta va razonada con las tres anteriores <b>(2 puntos)</b>.</li>
          </ul>
''')

S1_CIERRE = u'''
      <ol>
      ''' + pregunta(u'&iquest;Por qu&eacute; un lavavajillas no es un robot, si tiene programa, '
                     u'motores y sensores?',
                     u'<p>Porque sus sensores <b>se miran a s&iacute; mismos</b> (su agua, su '
                     u'temperatura) y lo que hace <b>no depende de lo que haya fuera</b>. Metas dos '
                     u'platos o veinte, el programa dura lo mismo. No percibe el entorno y no decide '
                     u'a partir de &eacute;l: ejecuta.</p>') + pregunta(
          u'Las tres preguntas que hay que hacerle a una m&aacute;quina, de memoria.',
          u'<p><b>1.</b> &iquest;Percibe el <b>entorno</b>? <b>2.</b> &iquest;Lo que hace '
          u'<b>depende</b> de lo que ha percibido? <b>3.</b> &iquest;<b>Act&uacute;a</b> sobre ese '
          u'entorno? Las tres, y sin que nadie la lleve.</p>') + pregunta(
          u'En la escena, el programa grabado pasa del 77 % al 47 % al mover los muebles, y encima '
          u'choca 124 veces. &iquest;Cu&aacute;l de las tres preguntas est&aacute; fallando?',
          u'<p>La <b>primera</b>. No percibe nada, as&iacute; que tampoco puede fallar la segunda: no '
          u'hay nada que decidir. Los 124 choques son la prueba: gasta los pasos contra una mesa '
          u'exactamente igual que si estuviera limpiando, porque <b>no distingue</b> una cosa de la '
          u'otra.</p>') + pregunta(
          u'Un brazo de una f&aacute;brica de coches repite la misma soldadura todo el d&iacute;a. '
          u'&iquest;Es un robot?',
          u'<p>Con las tres preguntas delante: <b>no</b>, porque no percibe el entorno; es un '
          u'<b>aut&oacute;mata</b> muy bueno. La industria lo llama robot, y no pasa nada: lo que hay '
          u'que saber es <b>por qu&eacute; hay que vallarlo</b>. Si entras en su celda, el brazo no '
          u'se entera.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        En la escena el robot avanzaba <b>una casilla</b>, y la casilla siempre med&iacute;a lo mismo.
        En una mesa de taller no hay casillas: hay un motor, un cable y una pila. Y cuando le digas a
        ese motor que avance medio metro vas a descubrir algo inc&oacute;modo:
        <b>un motor no sabe d&oacute;nde est&aacute;</b>.
      </div>

      <div class="copiar" style="border-color:var(--goo-verde)">
        <h4>Lectura del tema</h4>
        <p>Una sesi&oacute;n entera para leer y contestar, y conviene hacerla <b>pronto</b>: cuenta
           de d&oacute;nde vienen las tres ideas de las sesiones siguientes, y las cuenta con tres
           casos reales con fecha. <b>30 p&aacute;rrafos numerados</b>: cada uno lee el suyo en voz
           alta, en orden. Despu&eacute;s, diez preguntas por escrito.</p>
        <p style="margin-top:10px"><a href="lectura-tema7.pdf" target="_blank" rel="noopener"
           style="font-family:var(--f-m);font-size:13px;color:var(--goo-verde);font-weight:500">
           &#8595; La m&aacute;quina que se entera &middot; PDF</a></p>
      </div>
'''


# ==========================================================================
# SESION 2 - El motor no sabe donde esta
# ==========================================================================
S2_RETO = u'''
      <p>Pasamos el robot de la sesi&oacute;n pasada del dibujo a la mesa. Dos motores, dos ruedas,
         una placa y una pila. Y el encargo m&aacute;s corto que existe:</p>
      <div class="aviso">
        <span class="n-tag">El encargo</span>
        Que avance <b>medio metro</b> y pare.
      </div>
      <p>Lo que sale en todas las clases es esto, y es razonable: se cronometra una vez cu&aacute;nto
         tarda en recorrer medio metro &mdash;pongamos 2,3 segundos&mdash; y se escribe.</p>
      <div class="copiar">
        <h4>El primer intento</h4>
        <pre style="font-family:var(--f-m);font-size:13px;line-height:1.55;margin:6px 0;white-space:pre-wrap">digitalWrite(motor, HIGH);
delay(2300);
digitalWrite(motor, LOW);</pre>
      </div>
      <p>Y funciona. La primera vez.</p>
      <ul>
        <li>Lo repites tres veces seguidas: <b>51</b>, <b>49</b> y <b>53</b> cm.</li>
        <li>Lo pruebas al d&iacute;a siguiente, con la pila de ayer: <b>38</b> cm.</li>
        <li>Lo pruebas en el aula de al lado, que tiene moqueta: <b>41</b> cm.</li>
      </ul>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento</span>
        <p>El programa <b>no ha cambiado ni una coma</b> en ninguna de las cinco pruebas. Entonces,
           &iquest;qu&eacute; es exactamente lo que ha cambiado? Y sobre todo: &iquest;qu&eacute; es
           lo que ese programa est&aacute; midiendo de verdad?</p>
      </div>
      <p>Est&aacute; midiendo <b>tiempo</b>. T&uacute; quer&iacute;as <b>distancia</b>. Y esas dos
         cosas solo son lo mismo mientras la velocidad no cambie, que es justo lo &uacute;nico que no
         te puede garantizar nadie: la pila se gasta, la moqueta frena, el eje roza m&aacute;s
         cuando hace fr&iacute;o y el motor tarda en arrancar.</p>
      <p>El problema de fondo no es el <code>delay()</code>. Es que ese motor <b>no tiene ni
         idea de d&oacute;nde est&aacute;</b>, y t&uacute; le est&aacute;s pidiendo que lo sepa.</p>
'''

S2_TEORIA = u'''
      <p>Un actuador no es &laquo;un motor&raquo;. Hay varios, y cada uno te promete una cosa
         distinta. Elegir mal no es que vaya despacio: es que <b>no puedes escribir el programa</b>.</p>
      <div class="copiar">
        <h4>Qu&eacute; te promete cada motor</h4>
        <table style="width:100%;border-collapse:collapse;font-size:14px">
          <tr style="text-align:left;border-bottom:1.5px solid var(--line)">
            <th>motor</th><th>t&uacute; le dices</th><th>&iquest;sabe d&oacute;nde est&aacute;?</th>
            <th>vueltas</th></tr>
          <tr><td><b>Corriente continua</b></td><td>enciende / apaga</td>
              <td><b>no</b>, ni puede</td><td>sin fin</td></tr>
          <tr><td><b>Servo</b></td><td>un <b>&aacute;ngulo</b></td>
              <td>&eacute;l s&iacute;; t&uacute; no</td><td>unos 180&deg;</td></tr>
          <tr><td><b>Paso a paso</b></td><td>un <b>n&uacute;mero de pasos</b></td>
              <td>a base de contar</td><td>sin fin</td></tr>
          <tr><td><b>CC + encoder</b></td><td>enciende, y &eacute;l cuenta</td>
              <td><b>s&iacute;, midiendo</b></td><td>sin fin</td></tr>
        </table>
        <p style="margin-top:10px">El <b>servo</b> ya lo desmontaste en la U4: dentro hay un motor de
           corriente continua, una reductora, un <b>potenci&oacute;metro pegado al eje</b> y un
           circuito que compara. Es el lazo cerrado de la U4 metido en una caja de dos euros. Su
           pega en rob&oacute;tica es doble: <b>no da la vuelta entera</b> y <b>no te contesta</b>.
           Sabe que ha llegado; t&uacute; no te enteras.</p>
      </div>
      <div class="copiar">
        <h4>Las cuentas del paso a paso</h4>
        <p><b>Paso angular</b>: lo que gira el eje en un paso.</p>
        <p style="font-family:var(--f-m);font-size:14px">paso angular = 360&deg; / pasos por vuelta
           &nbsp;&rarr;&nbsp; con 200 pasos: <b>1,8&deg;</b></p>
        <p><b>Mil&iacute;metros por paso</b>, con la rueda montada:</p>
        <p style="font-family:var(--f-m);font-size:14px">mm por paso = &pi; &middot; D / pasos por
           vuelta &nbsp;&rarr;&nbsp; con D = 65 mm y 200 pasos: &pi;&middot;65/200 =
           <b>1,021 mm</b></p>
        <p><b>Pasos para recorrer una distancia</b>:</p>
        <p style="font-family:var(--f-m);font-size:14px">n = distancia / (mm por paso), redondeando
           &nbsp;&rarr;&nbsp; 500 / 1,021 = 489,7 &rarr; <b>490 pasos</b></p>
        <p>Ese redondeo ya te mete <b>0,3 mm</b> de error, y no hay manera de quitarlo: el motor no
           sabe dar tres cuartos de paso.</p>
      </div>
      <p>Al banco de pruebas. El encargo es siempre el mismo &mdash;<b>avanza 500 mm</b>&mdash; y la
         escena lo intenta <b>cinco veces</b> con cada motor, con la f&iacute;sica de cada uno.
         Empieza con todo como est&aacute; y pasa por los tres.</p>
''' + RECORRIDO + u'''
      <div class="copiar">
        <h4>Exactitud y precisi&oacute;n: no son sin&oacute;nimos</h4>
        <p>Piensa en una diana con cinco flechas.</p>
        <ul>
          <li><b>Exactitud</b>: si la <b>media</b> de los tiros cae en el centro. Lo que la estropea
              es un <b>error sistem&aacute;tico</b>, que est&aacute; siempre y siempre hacia el mismo
              lado.</li>
          <li><b>Precisi&oacute;n</b> (o <b>repetibilidad</b>): si los cinco tiros caen <b>juntos</b>,
              den donde den. Lo que la estropea es el <b>ruido</b>, que unas veces sobra y otras
              falta.</li>
        </ul>
        <p>Y ahora, lo que sale en la escena con la rueda y el suelo de partida:</p>
        <ul>
          <li><b>CC por tiempo</b>: dispersi&oacute;n de <b>19,2 mm</b>. No es preciso, y con la pila
              al 70 % se queda en <b>346 mm</b>: tampoco es exacto.</li>
          <li><b>Paso a paso</b>: dispersi&oacute;n de <b>1,8 mm</b>. Muy preciso. Ahora baja el
              di&aacute;metro real a 62 mm: la dispersi&oacute;n <b>sigue</b> en 1,7 mm y la media se
              va a <b>472 mm</b>. Es <b>preciso y est&aacute; equivocado</b>, que es la peor
              combinaci&oacute;n, porque no hay manera de notarlo repitiendo.</li>
          <li><b>CC con encoder</b>: parecido al paso a paso, y adem&aacute;s <b>no pierde pasos</b>
              cuando le pides ir deprisa. Sube la velocidad a 400 mm/s y compara los dos.</li>
        </ul>
        <p>Un error sistem&aacute;tico <b>no se arregla repitiendo la medida</b>. Se arregla
           encontrando la causa.</p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p><b>De d&oacute;nde sale ese di&aacute;metro equivocado.</b> Mides la rueda con un calibre,
           en la mano, y te da 65 mm. La montas, pones el robot encima y el neum&aacute;tico se
           <b>aplasta</b>: el radio de rodadura de verdad es un poco menor. Un 3 % de error en el
           di&aacute;metro es un 3 % de error en <b>toda</b> distancia que recorra, para siempre. Se
           mide al rev&eacute;s: se le manda dar diez vueltas, se mide con una cinta lo que ha
           recorrido y se divide. Eso se llama <b>calibrar</b>.</p>
        <p><b>Y el encoder tampoco es magia.</b> Cuenta lo que gira <b>la rueda</b>, no lo que avanza
           <b>el robot</b>. Si la rueda patina, el encoder dice que todo va perfecto. Por eso en la
           escena la moqueta le hace lo mismo que al paso a paso.</p>
      </div>
''' + foto('c7-rotor-paso-a-paso.jpg',
           u'Rotor cil&iacute;ndrico de un motor paso a paso, fuera del motor, con su eje y con todo '
           u'el contorno cubierto de ranuras finas y paralelas al eje, y barniz verde entre ellas',
           u'El <b>rotor</b> de un motor paso a paso, sacado de su carcasa. Lo que hace que un paso '
           u'valga siempre lo mismo no es la electr&oacute;nica: son esas <b>ranuras</b> que le '
           u'recorren todo el contorno. El rotor se queda quieto en las posiciones en las que sus '
           u'dientes quedan enfrentados con los del estator, y no en las de en medio. En el tipo '
           u'm&aacute;s com&uacute;n, el de <b>1,8&deg; por paso</b>, hay <b>50 dientes</b> y el '
           u'rotor se monta en dos mitades <b>desplazadas medio diente</b> una respecto de la otra: '
           u'50 &times; 4 = 200 posiciones por vuelta. El paso angular est&aacute; <b>mecanizado en '
           u'el metal</b>, y por eso es tan repetible.',
           u'Dolly1010', u'CC BY 3.0',
           u'https://commons.wikimedia.org/wiki/File:Stepper_motor_rotor.jpg') + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <ul>
          <li><b>Micropasos.</b> El driver puede partir cada paso en 2, 4, 8 o 16 trozos. Eso sube la
              <b>resoluci&oacute;n</b> y quita vibraci&oacute;n, pero <b>no</b> sube la exactitud ni
              el par: las posiciones intermedias las sostiene la corriente, no un diente, y se
              pierden en cuanto hay carga.</li>
          <li><b>Un paso a paso parado consume.</b> Para quedarse quieto tiene que seguir haciendo
              par, y eso son amperios yendo a calor. Un servo, igual. Si tu proyecto pasa el 90 % del
              tiempo esperando &mdash;el riego, por ejemplo&mdash;, eso hay que contarlo en el
              presupuesto de bater&iacute;a.</li>
          <li><b>Por qu&eacute; las impresoras 3D llevan paso a paso.</b> Porque la cabeza tiene que
              ir a un sitio <b>exacto</b> y volver, y no hay sitio para un encoder en cada eje. A
              cambio, si un eje pierde pasos, la pieza sale torcida y la impresora <b>sigue tan
              contenta</b>. Eso tambi&eacute;n lo has visto en la escena.</li>
        </ul>
      </div>
''' + video('video-c7-pap', 'e4VCK1N8JvM',
            u'&iquest;Qu&eacute; es un motor paso a paso? &middot; Introducci&oacute;n',
            u'Canal: Cimech 3D',
            u'C&oacute;mo se mueve por dentro y c&oacute;mo se elige uno. Es la pieza de la foto de '
            u'arriba, en marcha.')

S2_PRACTICA = ficha(
    u'Actividad 2 &middot; Exacto, preciso, o ninguna de las dos',
    [u'CE4 &middot; 4.1', u'B.2', u'B.3'], u'Parejas &middot; 20 min', u'''
          <h4>Primera parte &middot; la tabla de los seis (8 min)</h4>
          <p>Con la escena, semilla 11, distancia 500 mm, y anotando <b>media</b> y
             <b>dispersi&oacute;n</b> en una tabla de seis filas:</p>
          <ol class="pasos">
            <li>Los <b>tres motores</b> en baldosa, pila al 100 %, velocidad 200. Tres filas.</li>
            <li>Los <b>tres motores</b> otra vez, con la pila al <b>60 %</b>. Tres filas m&aacute;s.</li>
          </ol>
          <p>Debajo, dos frases: <b>cu&aacute;l es preciso</b> y <b>a cu&aacute;l le afecta la
             pila</b>, con los n&uacute;meros delante. Y una tercera: &iquest;por qu&eacute; a los
             otros dos la pila no les hace nada?</p>
          <h4>Segunda parte &middot; las cuentas a mano (6 min)</h4>
          <p>Sin la escena, con calculadora y escribiendo <b>todos los pasos con sus unidades</b>:</p>
          <ul>
            <li>Motor de <b>200 pasos</b> por vuelta con rueda de <b>65 mm</b>: paso angular, mm por
                paso y <b>pasos para 500 mm</b>. &iquest;Cu&aacute;nto se pasa o se queda corto por
                el redondeo?</li>
            <li>Motor de <b>48 pasos</b> por vuelta con rueda de <b>42 mm</b>: lo mismo. &iquest;Con
                cu&aacute;l de los dos puedes afinar m&aacute;s?</li>
            <li>La rueda se aplasta y en vez de 65 mm rueda como si tuviera <b>63</b>. Si el robot
                cree que ha andado <b>2 metros</b>, &iquest;cu&aacute;ntos cent&iacute;metros ha
                andado de verdad?</li>
          </ul>
          <h4>Tercera parte &middot; el motor de vuestro proyecto (6 min)</h4>
          <p>Elegid <b>dos</b> de los proyectos del curso y, para cada uno, decid qu&eacute; motor
             pondr&iacute;ais. Antes de elegir, contestad esta pregunta, que es la que manda:
             <b>&iquest;qu&eacute; necesito saber: nada, un &aacute;ngulo, o una distancia?</b></p>
          <ul>
            <li>La <b>bomba del riego</b>: &iquest;hace falta saber d&oacute;nde est&aacute; el eje?</li>
            <li>La <b>barrera</b> del aparcamiento de bicis: sube 90&deg; y baja 90&deg;.</li>
            <li>La <b>tapa del contenedor</b>, o el brazo de la l&aacute;mpara.</li>
          </ul>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>La tabla de seis filas, con media y dispersi&oacute;n <b>(3 puntos)</b>.</li>
            <li>Las tres frases, con n&uacute;meros y no con impresiones <b>(2 puntos)</b>.</li>
            <li>Las cuentas del paso a paso, con unidades en cada l&iacute;nea <b>(2 puntos)</b>.</li>
            <li>La cuenta de la rueda aplastada, bien hecha <b>(1 punto)</b>.</li>
            <li>Los dos motores elegidos, justificados con la pregunta de arriba <b>(2 puntos)</b>.</li>
          </ul>
''')

S2_CIERRE = u'''
      <ol>
      ''' + pregunta(u'&iquest;Por qu&eacute; <code>delay(2300)</code> no sirve para avanzar medio '
                     u'metro?',
                     u'<p>Porque mide <b>tiempo</b>, no distancia. Tiempo y distancia solo son lo '
                     u'mismo si la velocidad no cambia, y cambia con la carga de la pila, con el '
                     u'suelo, con el rozamiento y con lo que tarde el motor en arrancar.</p>') + pregunta(
          u'Un motor de 200 pasos por vuelta mueve una rueda de 65 mm. &iquest;Cu&aacute;ntos '
          u'mil&iacute;metros avanza en un paso?',
          u'<p>El per&iacute;metro es &pi;&middot;65 = 204,2 mm, repartidos en 200 pasos: '
          u'<b>1,021 mm por paso</b>. Y el paso angular es 360/200 = <b>1,8&deg;</b>.</p>') + pregunta(
          u'Los cinco intentos caen en 472, 471, 473, 472 y 473 mm, y ped&iacute;as 500. '
          u'&iquest;Qu&eacute; falla, y se arregla repitiendo?',
          u'<p>Es <b>preciso</b> (los cinco caen en 2 mm) y <b>no es exacto</b> (se queda 28 mm '
          u'corto, siempre para el mismo lado). Eso es un <b>error sistem&aacute;tico</b>, y '
          u'<b>no</b> se arregla repitiendo: hay que buscar la causa, que casi siempre es el '
          u'di&aacute;metro de la rueda mal medido o el deslizamiento del suelo.</p>') + pregunta(
          u'&iquest;Por qu&eacute; se dice que un encoder &laquo;cierra el lazo&raquo; y un paso a '
          u'paso no?',
          u'<p>Porque el encoder <b>mide el resultado</b> y el programa puede corregir si no cuadra: '
          u'es el lazo cerrado de la U4. El paso a paso trabaja <b>en lazo abierto</b>: manda pasos y '
          u'da por hecho que se han dado. Si se pierde alguno, ni &eacute;l ni el programa se '
          u'enteran.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya sabes hacer que un eje gire <b>lo que t&uacute; quieras</b> y saber cu&aacute;nto ha
        girado. Pero tu proyecto no te pide &aacute;ngulos: te pide que la punta del brazo acabe
        <b>ah&iacute;</b>, encima de esa maceta. Y de los &aacute;ngulos al sitio hay una cuenta que
        todav&iacute;a no has hecho &mdash; y de vuelta, otra que ni siquiera tiene una sola
        respuesta.
      </div>
'''


# ==========================================================================
# SESION 3 - Grados de libertad y el brazo
# ==========================================================================
S3_RETO = u'''
      <p>Un encargo que vale para casi cualquiera de los proyectos del curso: un <b>brazo</b> encima
         de la mesa que tenga que llegar a varios sitios. El tubo del riego, que tiene que llegar a
         cuatro macetas. El foco de la l&aacute;mpara, que tiene que apuntar a donde est&eacute; el
         libro. El sensor del contenedor, que tiene que asomarse a tres papeleras.</p>
      <p>Empiezas con lo m&aacute;s sencillo que se puede montar: un <b>servo</b> atornillado a la
         mesa con un palo pegado al eje. Ya sabes de la sesi&oacute;n pasada que a un servo se le dice
         un &aacute;ngulo y &eacute;l se coloca.</p>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento</span>
        <p>Con ese &uacute;nico servo, y moviendo el &aacute;ngulo de 0 a 180&deg;, <b>a qu&eacute;
           puntos de la mesa puede llegar la punta del palo</b>? Dib&uacute;jalo en la libreta antes
           de seguir. No es &laquo;a toda la mesa&raquo;.</p>
      </div>
      <p>A una <b>circunferencia</b>, y a nada m&aacute;s. La punta est&aacute; siempre a la misma
         distancia del eje, as&iacute; que solo puede recorrer el borde de un c&iacute;rculo. Si las
         macetas no est&aacute;n justo en ese borde, mala suerte.</p>
      <p>As&iacute; que pones <b>otro servo</b> en la punta del primer palo, con otro palo. Ahora la
         punta ya no est&aacute; atada a una circunferencia: llega a casi toda la mesa. Con dos
         motores lo has arreglado.</p>
      <div class="aviso">
        <span class="n-tag">Y ahora el encargo de verdad</span>
        Que deje la semilla <b>de pie</b>, no tumbada. O que el foco llegue a ese punto
        <b>apuntando hacia abajo</b>, no de lado.
      </div>
      <p>Y eso, con dos motores, <b>no se puede</b>. Puedes elegir el <b>sitio</b>; la
         <b>inclinaci&oacute;n</b> con la que llegas te sale la que te salga. Lo que falta tiene
         nombre, y se cuenta.</p>
'''

S3_TEORIA = u'''
      <div class="copiar">
        <h4>Grados de libertad</h4>
        <p><b>Grado de libertad</b> (GdL): cada movimiento <b>independiente</b> que puede hacer un
           mecanismo. Un servo que gira = 1. Un carro que sube y baja = 1. Dos servos encadenados = 2.</p>
        <p>La regla, que es toda la sesi&oacute;n en una l&iacute;nea:</p>
        <p style="font-size:17px;text-align:center;margin:10px 0"><b>hacen falta tantos grados de
           libertad como cosas quieras controlar a la vez</b></p>
        <ul>
          <li>En un <b>plano</b>: la posici&oacute;n son 2 n&uacute;meros (x, y) &rarr; <b>2 GdL</b>.
              Si adem&aacute;s quieres la orientaci&oacute;n, <b>3</b>.</li>
          <li>En el <b>espacio</b>: 3 para la posici&oacute;n (x, y, z) y 3 para la orientaci&oacute;n
              &rarr; <b>6 GdL</b>. Por eso los brazos de f&aacute;brica tienen <b>seis ejes</b>: no es
              capricho, es el n&uacute;mero justo.</li>
          <li>Con <b>m&aacute;s</b> de los necesarios (7 o m&aacute;s) el brazo puede llegar al mismo
              sitio de infinitas maneras, y eso sirve para esquivar obst&aacute;culos. Es lo que
              tiene tu brazo: mueve el codo sin mover la mano.</li>
        </ul>
      </div>
''' + foto('c7-scara.jpg',
           u'Robot SCARA de laboratorio dentro de su jaula: una columna negra vertical, un primer '
           u'brazo amarillo horizontal rotulado ARM-BASE, un segundo brazo blanco tambi&eacute;n '
           u'horizontal y, colgando de su punta, un eje vertical con una pinza sobre una bandeja de '
           u'piezas',
           u'Un robot <b>SCARA</b>, contando sus grados de libertad uno a uno: <b>1</b> el brazo '
           u'amarillo, que gira sobre la columna negra; <b>2</b> el brazo blanco, que gira sobre la '
           u'punta del amarillo; <b>3</b> el eje que sube y baja; <b>4</b> el giro de la pinza. '
           u'Cuatro, y ni uno m&aacute;s: para coger una pieza de una bandeja y ponerla en otra no '
           u'hace falta inclinarla, as&iacute; que sobran dos de los seis. F&iacute;jate en que los '
           u'dos primeros giran <b>en el mismo plano horizontal</b>: eso es, exactamente, el brazo de '
           u'dos eslabones de la escena de abajo, visto desde arriba.',
           u'Hirata Robotics GmbH', u'CC BY-SA 3.0 de',
           u'https://commons.wikimedia.org/wiki/File:SCARA_mit_Stocker.jpg') + u'''
      <h3>De los &aacute;ngulos al sitio</h3>
      <p>Tienes dos servos. Sabes ponerlos en el &aacute;ngulo que quieras. Falta la cuenta que te
         dice <b>d&oacute;nde acaba la punta</b>, y no es dif&iacute;cil: es un tri&aacute;ngulo
         detr&aacute;s de otro.</p>
      <div class="copiar">
        <h4>Cinem&aacute;tica directa de un brazo plano de dos eslabones</h4>
        <p>Con el hombro en el origen, L&#8321; y L&#8322; las longitudes de los dos eslabones,
           &theta;&#8321; el &aacute;ngulo del hombro medido desde el eje x y &theta;&#8322; el del
           codo:</p>
        <p style="font-family:var(--f-m);font-size:15px;text-align:center;margin:12px 0">
           x = L&#8321;&middot;cos&nbsp;&theta;&#8321; + L&#8322;&middot;cos(&theta;&#8321; + &theta;&#8322;)<br>
           y = L&#8321;&middot;sen&nbsp;&theta;&#8321; + L&#8322;&middot;sen(&theta;&#8321; + &theta;&#8322;)</p>
        <p>Se lee como lo que es: <b>vas al codo</b> (primer sumando) y <b>desde el codo sigues</b>
           (segundo sumando).</p>
        <p>&#9888; <b>El error de todos los a&ntilde;os.</b> &theta;&#8322; se mide respecto al
           <b>primer eslab&oacute;n</b>, no respecto al suelo. Por eso en el segundo sumando aparece
           <b>&theta;&#8321; + &theta;&#8322;</b> y no &theta;&#8322; a secas. Si pones solo
           &theta;&#8322;, la cuenta funciona mientras &theta;&#8321; valga cero y falla en cuanto
           muevas el hombro, que es lo peor que puede pasar: parece que va bien.</p>
      </div>
      <div class="copiar">
        <h4>Espacio de trabajo</h4>
        <p><b>Espacio de trabajo</b>: todos los puntos a los que la punta puede llegar. En este brazo
           es una <b>corona circular</b>:</p>
        <p style="font-family:var(--f-m);font-size:15px;text-align:center;margin:10px 0">
           radio m&aacute;ximo = L&#8321; + L&#8322; &nbsp;&nbsp;&nbsp;
           radio m&iacute;nimo = |L&#8321; &minus; L&#8322;|</p>
        <p>El m&aacute;ximo es el brazo estirado del todo; el m&iacute;nimo, doblado del todo sobre
           s&iacute; mismo. Si L&#8321; = L&#8322; el agujero del centro desaparece y el espacio de
           trabajo es un c&iacute;rculo entero. Si son muy distintos, queda un agujero grande
           <b>justo delante del robot</b>, que es donde suele estar lo que quieres coger.</p>
      </div>
      <p>A la escena. Mueve los cuatro mandos y sigue la cuenta l&iacute;nea a l&iacute;nea en la
         tabla de la derecha: los n&uacute;meros que ves son los de las dos f&oacute;rmulas de arriba
         con tus &aacute;ngulos metidos.</p>
''' + BRAZO + u'''
      <h3>El problema de la vuelta, que es el que necesitas</h3>
      <p>La cuenta que acabas de hacer se llama <b>cinem&aacute;tica directa</b>: de los
         &aacute;ngulos al sitio. Y ahora f&iacute;jate en que <b>no es la que te hace falta</b>. A
         ti nadie te da &aacute;ngulos: a ti te dan una maceta y tienes que averiguar los
         &aacute;ngulos. Eso es la <b>cinem&aacute;tica inversa</b>.</p>
      <p>No la vamos a resolver aqu&iacute;: las cuentas son de Bachillerato. Pero pon la escena en
         <b>Poner un objetivo</b>, pincha en el cuadro y mira lo que te dice, porque lo importante de
         este problema no son las cuentas, son estas tres cosas:</p>
      <div class="copiar">
        <h4>Tres cosas que hay que saber del problema inverso</h4>
        <ol>
          <li><b>Puede no haber soluci&oacute;n.</b> Si el punto est&aacute; m&aacute;s lejos que
              L&#8321;+L&#8322; o m&aacute;s cerca que |L&#8321;&minus;L&#8322;|, no hay
              &aacute;ngulos que valgan. No es que el programa sea malo: es que <b>no existen</b>.</li>
          <li><b>Normalmente hay dos.</b> Al mismo punto se llega con el <b>codo hacia un lado</b> o
              <b>hacia el otro</b>. Las dos son correctas, as&iacute; que alguien tiene que
              <b>elegir</b>: y se elige mirando con cu&aacute;l no chocas contra la pared, contra la
              maceta de al lado o contra tu propio cable.</li>
          <li><b>Con m&aacute;s grados de libertad hay infinitas.</b> Con un brazo de 7 ejes puedes
              poner la mano en un sitio y mover el codo sin que la mano se entere. Esa es la ventaja
              y esa es la complicaci&oacute;n.</li>
        </ol>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>&laquo;Directa&raquo; e &laquo;inversa&raquo; suenan al rev&eacute;s de lo que
           esperar&iacute;as, porque la &uacute;til es la inversa. Los nombres vienen de la
           f&iacute;sica: <b>directo</b> es el problema que va de las causas (los &aacute;ngulos de
           los motores, que son lo que t&uacute; mandas) al efecto (d&oacute;nde acaba la punta), e
           <b>inverso</b> es el que va del efecto a las causas. Los problemas inversos casi siempre
           son m&aacute;s duros, y casi siempre son los que hacen falta.</p>
      </div>

      <h3>Y aqu&iacute; vuelve la sesi&oacute;n 2</h3>
      <p>Pon el mando de <b>error de cada servo</b> en 1&deg; y mira la mancha roja que aparece en la
         punta.</p>
      <div class="copiar">
        <h4>El error de una articulaci&oacute;n se multiplica por el brazo</h4>
        <p>Un &aacute;ngulo peque&ntilde;o &epsilon;, en radianes, a una distancia L del eje, mueve la
           punta:</p>
        <p style="font-family:var(--f-m);font-size:15px;text-align:center;margin:10px 0">
           error en la punta &asymp; L &middot; &epsilon; &nbsp;&nbsp;con&nbsp;&nbsp;
           &epsilon;(rad) = &epsilon;(&deg;) &middot; &pi; / 180</p>
        <p>Un grado son 0,01745 radianes. As&iacute; que <b>1&deg; de error en el hombro</b>, con el
           brazo estirado 210 mm, son 210 &middot; 0,01745 = <b>3,7 mm</b> en la punta. Si adem&aacute;s
           el codo se equivoca otro grado, se suman.</p>
        <p>De aqu&iacute; salen dos decisiones de dise&ntilde;o, y son vuestras:</p>
        <ul>
          <li><b>Brazo m&aacute;s corto</b> &rarr; menos error en la punta, menos alcance. Se paga
              con una cosa o con la otra.</li>
          <li>Si necesitas precisi&oacute;n, el dinero se gasta <b>en el hombro</b>, que es el que
              m&aacute;s multiplica, no en la mu&ntilde;eca.</li>
        </ul>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Cuando mires un cat&aacute;logo de robots, ver&aacute;s que dan la <b>repetibilidad</b>
           (&laquo;&plusmn;0,02 mm&raquo;) y casi nunca la <b>exactitud</b>. Es la misma pareja de
           palabras de la sesi&oacute;n 2, y no es por disimular: un brazo industrial vuelve al mismo
           punto con una fidelidad asombrosa, pero acertar la primera vez en unas coordenadas que
           nunca ha visto es much&iacute;simo m&aacute;s dif&iacute;cil, porque para eso tendr&iacute;a
           que conocer sus propias longitudes con esa misma exactitud. Por eso, en la industria, a un
           brazo se le <b>ense&ntilde;an</b> los puntos llev&aacute;ndolo a mano, uno a uno.</p>
      </div>
''' + video('video-c7-brazo', '9zSRNXRuX0g',
            u'Cinem&aacute;tica directa e inversa de un robot de 2 grados de libertad &middot; '
            u'm&eacute;todo geom&eacute;trico',
            u'Canal: Sistemas Din&aacute;micos y Control',
            u'El mismo brazo de la escena, con las dos cuentas hechas a mano en la pizarra. La parte '
            u'de la inversa es de nivel Bachillerato: sirve para ver de d&oacute;nde salen los dos '
            u'codos.')

S3_PRACTICA = ficha(
    u'Actividad 3 &middot; D&oacute;nde llega y d&oacute;nde no',
    [u'CE4 &middot; 4.1', u'B.2', u'B.3', u'B.4'], u'Parejas &middot; 20 min', u'''
          <h4>Primera parte &middot; la cuenta, y comprobarla (6 min)</h4>
          <p>Con L&#8321; = 120 mm y L&#8322; = 90 mm, anotad en una tabla la posici&oacute;n de la
             punta para estos cuatro juegos de &aacute;ngulos:</p>
          <ul>
            <li>&theta;&#8321; = 0&deg;, &theta;&#8322; = 0&deg;</li>
            <li>&theta;&#8321; = 90&deg;, &theta;&#8322; = 0&deg;</li>
            <li>&theta;&#8321; = 0&deg;, &theta;&#8322; = 90&deg;</li>
            <li>&theta;&#8321; = 35&deg;, &theta;&#8322; = 60&deg;</li>
          </ul>
          <p>El <b>tercero</b> lo hac&eacute;is <b>a mano</b>, con la calculadora en grados y
             escribiendo los cuatro sumandos, y despu&eacute;s lo compar&aacute;is con la escena.
             Si no os da lo mismo, mirad si hab&eacute;is escrito &theta;&#8321;+&theta;&#8322; donde
             tocaba.</p>
          <h4>Segunda parte &middot; el espacio de trabajo (5 min)</h4>
          <p>Con esas mismas longitudes, calculad el radio m&aacute;ximo y el m&iacute;nimo y
             <b>dibujad la corona en la libreta a escala 1:2</b> (1 mm de papel = 2 mm de brazo), con
             el comp&aacute;s.</p>
          <p>Poned luego en la escena un objetivo a unos <b>40 mm</b> del hombro y otro a unos
             <b>250 mm</b>. Copiad lo que dice la escena en cada caso y explicad <b>con la
             f&oacute;rmula</b> por qu&eacute; no llega.</p>
          <h4>Tercera parte &middot; los dos codos (4 min)</h4>
          <p>Poned un objetivo que s&iacute; est&eacute; dentro y anotad los <b>dos</b> pares de
             &aacute;ngulos. Pulsad los dos botones para ver el brazo en cada postura. Escribid:
             si hubiera una pared a la izquierda del robot, <b>cu&aacute;l de las dos
             elegir&iacute;ais</b> y por qu&eacute;.</p>
          <h4>Cuarta parte &middot; el error (5 min)</h4>
          <p>Con el error de servo a <b>1&deg;</b>, anotad los mil&iacute;metros de la punta con
             L&#8321;=120/L&#8322;=90 y luego con L&#8321;=160/L&#8322;=140. Comprobad uno de los dos
             con la f&oacute;rmula L &middot; &epsilon;. Decidid para vuestro proyecto:
             &iquest;brazo largo o corto? Una frase, con el n&uacute;mero dentro.</p>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Los cuatro puntos de la tabla <b>(2 puntos)</b>.</li>
            <li>El tercero hecho a mano, con los cuatro sumandos escritos <b>(2 puntos)</b>.</li>
            <li>La corona dibujada a escala, con sus dos radios <b>(2 puntos)</b>.</li>
            <li>Los dos casos que no llegan, explicados con la f&oacute;rmula <b>(1 punto)</b>.</li>
            <li>Los dos codos anotados y la elecci&oacute;n razonada <b>(1,5 puntos)</b>.</li>
            <li>El error en mil&iacute;metros, comprobado con L&middot;&epsilon; <b>(1,5 puntos)</b>.</li>
          </ul>
''')

S3_CIERRE = u'''
      <ol>
      ''' + pregunta(u'&iquest;Cu&aacute;ntos grados de libertad hacen falta para poner una pieza en '
                     u'un sitio del espacio <b>y</b> con una inclinaci&oacute;n concreta?',
                     u'<p><b>Seis</b>: tres para la posici&oacute;n (x, y, z) y tres para la '
                     u'orientaci&oacute;n. Por eso los brazos industriales cl&aacute;sicos tienen '
                     u'seis ejes. Un SCARA tiene cuatro porque para dejar piezas en una bandeja no '
                     u'hace falta inclinarlas.</p>') + pregunta(
          u'Escribe la cinem&aacute;tica directa del brazo de dos eslabones, y di d&oacute;nde '
          u'est&aacute; la trampa.',
          u'<p>x = L&#8321;cos&theta;&#8321; + L&#8322;cos(&theta;&#8321;+&theta;&#8322;), '
          u'y = L&#8321;sen&theta;&#8321; + L&#8322;sen(&theta;&#8321;+&theta;&#8322;). La trampa es '
          u'el <b>&theta;&#8321;+&theta;&#8322;</b>: el &aacute;ngulo del codo se mide respecto al '
          u'primer eslab&oacute;n, as&iacute; que hay que sumarle el del hombro. Con '
          u'&theta;&#8321;=0 no se nota, y ah&iacute; est&aacute; el peligro.</p>') + pregunta(
          u'L&#8321; = 120 mm y L&#8322; = 90 mm. &iquest;Puede la punta llegar a un punto que '
          u'est&aacute; a 25 mm del hombro?',
          u'<p><b>No.</b> El radio m&iacute;nimo es |120 &minus; 90| = <b>30 mm</b>: el brazo, '
          u'doblado del todo sobre s&iacute; mismo, no se acerca m&aacute;s. Ese punto est&aacute; en '
          u'el <b>agujero</b> del espacio de trabajo, y no hay &aacute;ngulos que valgan.</p>') + pregunta(
          u'Tus dos servos se equivocan 1&deg; cada uno y el brazo mide 210 mm estirado. '
          u'&iquest;De cu&aacute;ntos mil&iacute;metros estamos hablando en la punta?',
          u'<p>1&deg; = 0,01745 rad. Solo el hombro ya mueve la punta 210 &middot; 0,01745 = '
          u'<b>3,7 mm</b>, y el codo suma lo suyo. Del orden de <b>medio cent&iacute;metro</b>. '
          u'Por eso el error angular se paga caro: <b>se multiplica por la longitud del brazo</b>.</p>'
          ) + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya sabes a d&oacute;nde tiene que ir el brazo y con qu&eacute; &aacute;ngulos. Pero un
        automatismo no es <b>un</b> movimiento: es una secuencia, con esperas, con topes y con cosas
        que llegan <b>cuando no toca</b>. Prueba a escribir eso con <code>if</code> y
        <code>delay()</code> y en una tarde tendr&aacute;s un programa que no entiende ni quien lo
        escribi&oacute;.
      </div>
'''


# ==========================================================================
# SESION 4 - Programar el automatismo: la maquina de estados
# ==========================================================================
S4_RETO = u'''
      <p>La barrera del aparcamiento de bicis, esa cuyo par ya calculaste en la U4. El encargo cabe
         en una l&iacute;nea: <b>si alguien pasa la tarjeta, la barrera sube, espera un poco y
         baja</b>.</p>
      <div class="copiar">
        <h4>El primer programa, que sale solo</h4>
        <pre style="font-family:var(--f-m);font-size:13px;line-height:1.55;margin:6px 0;white-space:pre-wrap">void loop() {
  if (tarjetaValida()) {
    subirBarrera();
    delay(3000);
    delay(5000);        // la barrera, esperando
    bajarBarrera();
    delay(3000);
  }
}</pre>
      </div>
      <p>Diez l&iacute;neas, funciona a la primera y se entiende. Y entonces empiezan las preguntas
         de clase, que son todas razonables:</p>
      <div class="aviso">
        <span class="n-tag">Las preguntas</span>
        &iquest;Y si pasan la tarjeta <b>mientras est&aacute; subiendo</b>?<br>
        &iquest;Y si cuando toca bajar hay <b>alguien debajo</b>?<br>
        &iquest;Y si el fin de carrera no llega nunca porque algo la ha atascado?<br>
        &iquest;Y si pasan <b>dos tarjetas seguidas</b>?
      </div>
      <p>Intentadlo. Cada pregunta se arregla a&ntilde;adiendo una variable
         (<code>bool subiendo</code>, <code>bool hayAlguien</code>&hellip;) y un
         <code>if</code> m&aacute;s. A la tercera, el programa tiene seis banderas y nadie es capaz de
         decir qu&eacute; hace si se levantan dos a la vez. A eso se le llama <b>c&oacute;digo
         espagueti</b>, y no se arregla escribiendo mejor: se arregla cambiando de herramienta.</p>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento</span>
        <p>Antes de las banderas hay un problema m&aacute;s gordo, y est&aacute; en la l&iacute;nea
           <code>delay(3000)</code>. &iquest;Qu&eacute; est&aacute; haciendo la placa durante esos
           tres segundos? Y sobre todo: <b>&iquest;qu&eacute; NO est&aacute; haciendo?</b></p>
      </div>
      <p>No est&aacute; mirando. <b>Un <code>delay()</code> no es una pausa: es un rato en el que el
         programa se va del mundo.</b> Si durante esos tres segundos alguien se mete debajo de la
         barrera, la placa no se entera &mdash;ni entonces ni despu&eacute;s&mdash;, porque ese
         evento no se ha guardado en ning&uacute;n sitio. Simplemente pas&oacute; mientras
         nadie miraba.</p>
'''

S4_TEORIA = u'''
      <p>La herramienta que ordena esto no se invent&oacute; para Arduino ni para robots. Se usa en
         los sem&aacute;foros, en los ascensores, en los cajeros y en los protocolos de internet, y
         consiste en dejar de preguntarse <i>&laquo;&iquest;qu&eacute; hago ahora?&raquo;</i> para
         preguntarse <i>&laquo;<b>&iquest;d&oacute;nde estoy</b>, y qu&eacute; acaba de
         llegar?&raquo;</i>.</p>
      <div class="copiar">
        <h4>M&aacute;quina de estados</h4>
        <p>Una <b>m&aacute;quina de estados finitos</b> es una forma de escribir un automatismo con
           cuatro piezas:</p>
        <ul>
          <li><b>Estados</b>: la lista, cerrada, de situaciones en las que puede estar el sistema.
              La barrera est&aacute; <i>cerrada</i>, <i>subiendo</i>, <i>abierta</i> o <i>bajando</i>.
              En una, y solo en una.</li>
          <li><b>Eventos</b>: lo que puede llegar de fuera. Una tarjeta, un fin de carrera que se
              cierra, un sensor que se activa, un segundo que pasa.</li>
          <li><b>Transiciones</b>: qu&eacute; evento te lleva de qu&eacute; estado a qu&eacute; otro.</li>
          <li><b>Acciones</b>: lo que se hace <b>mientras</b> est&aacute;s en cada estado (motor
              subiendo, bomba parada, luz encendida).</li>
        </ul>
        <p><b>La regla de oro</b>: en cada vuelta de <code>loop()</code> se mira <b>una vez</b>
           qu&eacute; ha llegado y se decide <b>una vez</b>. Y por lo tanto: <b>ni un
           <code>delay()</code></b>. El tiempo se mide con <code>millis()</code>, que te dice
           cu&aacute;ntos milisegundos lleva encendida la placa <b>sin parar el programa</b>.</p>
      </div>
      <div class="copiar">
        <h4>La tabla de transiciones</h4>
        <p>Se dibuja una tabla con los <b>estados en las filas</b> y los <b>eventos en las
           columnas</b>. Cuatro estados y cinco eventos son <b>4 &times; 5 = 20 casillas</b>.</p>
        <p>Y hay que contestarlas <b>todas</b>, <b>una a una</b>, aunque muchas respuestas sean
           &laquo;<b>no hacer nada</b>&raquo;. Esa es toda la gracia del m&eacute;todo: la tabla te
           <b>obliga</b> a plantearte casos que no se te habr&iacute;an ocurrido nunca, como
           &laquo;&iquest;y si llega una tarjeta mientras baja?&raquo;.</p>
        <p>Las casillas que dejes en blanco son, exactamente, <b>por donde se va a romper</b> el
           automatismo el d&iacute;a que lo pongas en el pasillo.</p>
      </div>
      <p>Abajo tienes la m&aacute;quina montada y <b>funcionando</b>. Pulsa los eventos y mira tres
         cosas a la vez: el diagrama, la l&iacute;nea de c&oacute;digo que te toca y la tabla de
         casillas, que se va encendiendo. El reto es <b>encenderlas las veinte</b>.</p>
      <p>Y cuando la tengas dominada, cambia a <b>Espagueti con delay()</b> y repite la jugada.</p>
''' + ESTADOS + u'''
      <div class="copiar">
        <h4>C&oacute;mo se escribe en Arduino</h4>
        <ul>
          <li>Los estados, <b>con nombre</b>, no con n&uacute;meros:
              <code>enum Estado { CERRADA, SUBIENDO, ABIERTA, BAJANDO };</code></li>
          <li>Una sola variable: <code>Estado estado = CERRADA;</code></li>
          <li>Dentro de <code>loop()</code>, un <code>switch (estado)</code> con un
              <code>case</code> por estado, y dentro de cada <code>case</code> las transiciones que
              salen de &eacute;l. <b>Nunca</b> un <code>case</code> sin su <code>break;</code>.</li>
          <li>Para esperar: al entrar en el estado se guarda <code>t0 = millis();</code> y en cada
              vuelta se comprueba <code>if (millis() - t0 &gt; ESPERA) ...</code></li>
        </ul>
        <p>Mira las dos versiones de c&oacute;digo de la escena, una al lado de la otra. La de estados
           es m&aacute;s larga; tambi&eacute;n es la &uacute;nica que se puede leer dentro de un mes y
           la &uacute;nica en la que se puede a&ntilde;adir un caso sin romper los otros.</p>
      </div>
      <div class="copiar">
        <h4>Y la misma m&aacute;quina sirve para los tres proyectos</h4>
        <p>Cambia la piel de la escena a <b>Riego</b> y a <b>Contenedor</b>: los estados se llaman de
           otra manera, los eventos tambi&eacute;n, y las <b>flechas son las mismas</b>.</p>
        <table style="width:100%;border-collapse:collapse;font-size:14px;margin-top:8px">
          <tr style="text-align:left;border-bottom:1.5px solid var(--line)">
            <th></th><th>Barrera</th><th>Riego</th><th>Contenedor</th></tr>
          <tr><td>reposo</td><td>cerrada</td><td>en espera</td><td>vigilando</td></tr>
          <tr><td>actuando</td><td>subiendo</td><td>regando</td><td>avisando</td></tr>
          <tr><td>manteniendo</td><td>abierta</td><td>dejando calar</td><td>aviso puesto</td></tr>
          <tr><td>volviendo</td><td>bajando</td><td>cerrando</td><td>apagando</td></tr>
        </table>
        <p style="margin-top:10px">Eso no es casualidad: <b>reposo &rarr; actuar &rarr; mantener
           &rarr; volver</b> es el esqueleto de casi cualquier automatismo de un ciclo. Cuando
           montes el tuyo, empieza por ah&iacute; y luego a&ntilde;ade lo que le falte.</p>
      </div>
''' + foto('c7-programador-lavadora.jpg',
           u'Programador electromec&aacute;nico de lavadora desmontado: el mando blanco arriba, una '
           u'pila de discos de pl&aacute;stico traslúcido en el centro y, a los dos lados, hileras de '
           u'contactos met&aacute;licos de los que salen decenas de cables de colores',
           u'Una m&aacute;quina de estados hecha de <b>metal</b>: el programador de una lavadora '
           u'antigua (Candy). Esa pila de discos del centro son <b>levas</b>, y cada una tiene '
           u'recortado su propio perfil; al girar, sus salientes abren y cierran los contactos de los '
           u'lados, que son los que dan corriente al motor, a la resistencia y a la bomba. <b>El '
           u'programa es la forma de las levas</b>, y el estado es, literalmente, el &aacute;ngulo en '
           u'el que est&aacute;. Un motorcito lo hace avanzar poco a poco, y de ah&iacute; el '
           u'&laquo;clac&raquo; cada pocos segundos. F&iacute;jate en lo que <b>no</b> puede hacer: '
           u'volver atr&aacute;s, saltarse una fase o reaccionar a algo. Solo <b>avanza</b>. Es el '
           u'lavavajillas de la sesi&oacute;n 1, abierto por dentro.',
           u'Lac 16', u'CC BY-SA 3.0',
           u'https://commons.wikimedia.org/wiki/File:Machine_laver_programmateur.jpg') + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p><b>Un detalle de <code>millis()</code> que se cobra caro.</b> <code>millis()</code>
           devuelve un <code>unsigned long</code> de 4 bytes, as&iacute; que llega hasta
           4.294.967.295 milisegundos y despu&eacute;s <b>vuelve a cero</b>. Eso son
           <b>49 d&iacute;as y 17 horas</b>. Es la misma trampa del desbordamiento de la U6, ahora en
           un aparato que se queda enchufado en un pasillo.</p>
        <p>Lo bueno es que tiene arreglo, y es gratis: escribir siempre
           <code>millis() - t0 &gt; ESPERA</code> y <b>nunca</b>
           <code>millis() &gt; t0 + ESPERA</code>. La primera forma funciona incluso el d&iacute;a que
           el contador da la vuelta, porque la resta entre enteros sin signo tambi&eacute;n da la
           vuelta y el resultado sale bien. La segunda se queda colgada hasta 49 d&iacute;as.</p>
        <p><b>Y de d&oacute;nde viene todo esto.</b> La idea es de mucho antes que los ordenadores
           dom&eacute;sticos: <b>Warren McCulloch</b> y <b>Walter Pitts</b> la publicaron en
           <b>1943</b> pensando en neuronas, y en los cincuenta le pusieron forma <b>George H.
           Mealy</b> (1955) y <b>Edward F. Moore</b> (1956), los dos en los laboratorios Bell. La
           diferencia entre los dos modelos que llevan su nombre cabe en una l&iacute;nea: en una
           m&aacute;quina de <b>Moore</b> la salida depende <b>solo del estado</b>; en una de
           <b>Mealy</b> depende del estado <b>y</b> del evento. Lo que has usado aqu&iacute; es de
           Moore, que es la que se lee mejor.</p>
      </div>
''' + video('video-c7-estados', 'IrBwtuUwqbM',
            u'Controlando tiempos con Arduino',
            u'Canal: Jorge Garc&iacute;a Ochoa de Aspuru',
            u'Un automatismo real con <code>millis()</code> y transiciones por tiempo, sin un solo '
            u'<code>delay()</code>. Es el paso siguiente al c&oacute;digo de la escena.')

S4_PRACTICA = ficha(
    u'Actividad 4 &middot; Las veinte casillas',
    [u'CE4 &middot; 4.1', u'B.2', u'B.3', u'B.4'], u'Grupos de tres &middot; 15 min', u'''
          <h4>Primera parte &middot; cubrir la tabla (5 min)</h4>
          <p>En la escena, en modo <b>M&aacute;quina de estados</b>, pulsad eventos hasta que se
             enciendan <b>las veinte casillas</b>. Anotad:</p>
          <ol class="pasos">
            <li>Cu&aacute;ntos eventos os ha costado.</li>
            <li><b>Cu&aacute;les han sido las tres &uacute;ltimas</b> en encenderse. No es casualidad:
                son las que nadie prueba nunca.</li>
            <li>Copiad en la libreta, de esas tres, <b>qu&eacute; dice la escena que pasa</b>.</li>
          </ol>
          <h4>Segunda parte &middot; el espagueti (4 min)</h4>
          <p>Cambiad a <b>Espagueti con delay()</b> y reiniciad. Pulsad la petici&oacute;n para
             arrancar la secuencia y, mientras corre, id pulsando <b>&laquo;hay alguien
             debajo&raquo;</b> y los dem&aacute;s eventos. Anotad los <b>eventos perdidos</b> y las
             <b>veces que ha bajado con alguien debajo</b>.</p>
          <p>Escribid dos frases: qu&eacute; habr&iacute;a pasado con una barrera de verdad, y
             <b>por qu&eacute; el programa no puede arreglarlo despu&eacute;s</b>.</p>
          <h4>Tercera parte &middot; la tabla de vuestro proyecto (6 min)</h4>
          <p>Elegid <b>dos</b> de los proyectos del curso y, para cada uno:</p>
          <ol class="pasos">
            <li>La lista de <b>estados</b> (tres, cuatro o cinco; no m&aacute;s).</li>
            <li>La lista de <b>eventos</b>, incluyendo <b>uno de seguridad</b> y el paso del tiempo.</li>
            <li>La <b>tabla</b> dibujada y <b>rellena entera</b>, con &laquo;no hace nada&raquo;
                donde toque.</li>
          </ol>
          <p>Marcad con un c&iacute;rculo las casillas que <b>no se os hab&iacute;an ocurrido</b>
             hasta dibujar la tabla. Esas son las que valen la actividad.</p>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Las veinte casillas cubiertas y las tres &uacute;ltimas anotadas <b>(2 puntos)</b>.</li>
            <li>Los datos del espagueti, con las dos frases <b>(2 puntos)</b>.</li>
            <li>Estados y eventos de los dos proyectos, con su evento de seguridad
                <b>(2 puntos)</b>.</li>
            <li>Las dos tablas <b>completas</b>: ni una casilla en blanco <b>(3 puntos)</b>.</li>
            <li>Las casillas marcadas con c&iacute;rculo, y son de verdad las raras
                <b>(1 punto)</b>.</li>
          </ul>
''')

PREGUNTAS_TEST = [
    dict(p=u'&iquest;Cu&aacute;l es la pregunta que mejor separa un robot de una m&aacute;quina '
           u'automática cualquiera?',
         op=[u'&iquest;Tiene motores y un programa dentro?',
             u'Si cambias el mundo a su alrededor, &iquest;cambia lo que hace?',
             u'&iquest;Se parece a una persona o a un animal?'],
         ok=1,
         por=u'Un lavavajillas tiene motores, programa y hasta sensores, pero sus sensores se miran '
             u'a s&iacute; mismos y su programa dura lo mismo con dos platos que con veinte. Un robot '
             u'<b>percibe el entorno</b>, decide a partir de eso y act&uacute;a sobre &eacute;l.'),
    dict(p=u'En la escena de la sesi&oacute;n 1, al mover los muebles el programa grabado baja del '
           u'77 % al 47 % y choca 124 veces. &iquest;Qu&eacute; le falta?',
         op=[u'M&aacute;s pasos: con m&aacute;s tiempo acabar&iacute;a el aula.',
             u'Percibir el entorno: gasta los pasos contra una mesa igual que si limpiara, porque no '
             u'distingue una cosa de otra.',
             u'Un motor m&aacute;s potente para apartar los muebles.'],
         ok=1,
         por=u'No es cuesti&oacute;n de tiempo ni de fuerza. El programa grabado <b>no lee nada</b>: '
             u'repite la lista que se grab&oacute; el d&iacute;a que se grab&oacute;, y los 124 '
             u'choques los da sin enterarse de ninguno.'),
    dict(p=u'&iquest;Por qu&eacute; <code>digitalWrite(motor, HIGH); delay(2300);</code> no sirve '
           u'para avanzar medio metro?',
         op=[u'Porque 2300 milisegundos son muy pocos.',
             u'Porque mide tiempo, y tiempo y distancia solo son lo mismo si la velocidad no cambia '
             u'&mdash; y cambia con la pila, con el suelo y con el rozamiento.',
             u'Porque <code>delay()</code> no funciona con motores.'],
         ok=1,
         por=u'El programa no ha cambiado entre una prueba y otra: lo que cambia es la velocidad. '
             u'Con la pila a media carga, el mismo programa se queda en 38 cm.'),
    dict(p=u'Un motor paso a paso de 200 pasos por vuelta mueve una rueda de 65 mm de '
           u'di&aacute;metro. &iquest;Cu&aacute;nto avanza en un paso?',
         op=[u'&pi;&middot;65/200 = 1,021 mm', u'65/200 = 0,325 mm', u'360/200 = 1,8 mm'],
         ok=0,
         por=u'Lo que avanza es el <b>per&iacute;metro</b> repartido entre los pasos: '
             u'&pi;&middot;65 = 204,2 mm entre 200 pasos. El 1,8 no son mil&iacute;metros: son los '
             u'<b>grados</b> que gira el eje en cada paso.'),
    dict(p=u'Los cinco intentos de un robot dan 472, 471, 473, 472 y 473 mm, y hab&iacute;as pedido '
           u'500. &iquest;C&oacute;mo se llama eso y c&oacute;mo se arregla?',
         op=[u'Es falta de precisi&oacute;n, y se arregla haciendo m&aacute;s intentos y tomando la '
             u'media.',
             u'Es preciso pero inexacto: hay un error sistem&aacute;tico, y solo se arregla buscando '
             u'la causa (el di&aacute;metro de la rueda, el deslizamiento).',
             u'Es normal en cualquier motor y no tiene arreglo.'],
         ok=1,
         por=u'Los cinco caen en 2 mm: <b>precisi&oacute;n</b> excelente. Pero los cinco se quedan '
             u'cortos hacia el mismo lado: eso es un <b>error sistem&aacute;tico</b>, y repetir la '
             u'medida no lo quita, porque est&aacute; en todas las medidas.'),
    dict(p=u'&iquest;Cu&aacute;ntos grados de libertad hacen falta para dejar una pieza en un punto '
           u'del espacio <b>con</b> una inclinaci&oacute;n determinada?',
         op=[u'Tres: x, y, z.', u'Seis: tres de posici&oacute;n y tres de orientaci&oacute;n.',
             u'Los que tenga el robot; no hay un n&uacute;mero.'],
         ok=1,
         por=u'Tres n&uacute;meros dicen d&oacute;nde, y otros tres dicen c&oacute;mo est&aacute; '
             u'puesta. De ah&iacute; los <b>seis ejes</b> de los brazos industriales. Un SCARA lleva '
             u'cuatro porque para dejar piezas en una bandeja no hace falta inclinarlas.'),
    dict(p=u'En el brazo de dos eslabones, &iquest;por qu&eacute; la segunda parte de la '
           u'f&oacute;rmula lleva cos(&theta;&#8321;+&theta;&#8322;) y no cos&nbsp;&theta;&#8322;?',
         op=[u'Por un convenio de los cat&aacute;logos de robots.',
             u'Porque &theta;&#8322; se mide respecto al primer eslab&oacute;n, no respecto al eje x: '
             u'para saber c&oacute;mo est&aacute; el segundo eslab&oacute;n hay que sumar los dos.',
             u'Porque as&iacute; el resultado sale en grados y no en radianes.'],
         ok=1,
         por=u'Es el fallo cl&aacute;sico, y lo peor es que con &theta;&#8321; = 0 la f&oacute;rmula '
             u'mala <b>tambi&eacute;n acierta</b>: solo se cae cuando mueves el hombro.'),
    dict(p=u'Pones un objetivo dentro del espacio de trabajo del brazo de dos eslabones. '
           u'&iquest;Cu&aacute;ntos juegos de &aacute;ngulos lo alcanzan?',
         op=[u'Uno, siempre.', u'Dos, uno con el codo hacia cada lado.', u'Ninguno.'],
         ok=1,
         por=u'Por eso la cinem&aacute;tica <b>inversa</b> es la dif&iacute;cil: no da una '
             u'respuesta, da dos, y alguien tiene que elegir mirando con cu&aacute;l no choca el '
             u'codo. Fuera del espacio de trabajo no hay ninguna.'),
    dict(p=u'&iquest;Qu&eacute; es lo que hace de verdad <code>delay(3000)</code> dentro de un '
           u'automatismo?',
         op=[u'Guardar los eventos que lleguen para atenderlos en cuanto acabe.',
             u'Dejar al programa tres segundos sin mirar nada: lo que llegue mientras tanto se '
             u'pierde y no queda registrado en ning&uacute;n sitio.',
             u'Bajar el consumo de la placa durante tres segundos.'],
         ok=1,
         por=u'No es una pausa: es un rato fuera del mundo. Y lo m&aacute;s probable que llegue '
             u'mientras no miras es justo el evento de seguridad. Por eso el tiempo se cuenta con '
             u'<code>millis()</code>.'),
    dict(p=u'Un automatismo con 4 estados y 5 eventos. &iquest;Cu&aacute;ntas casillas tiene su '
           u'tabla de transiciones y cu&aacute;ntas hay que contestar?',
         op=[u'9 casillas, una por estado y por evento.',
             u'20 casillas, y hay que contestarlas todas, aunque muchas sean &laquo;no hacer '
             u'nada&raquo;.',
             u'Solo las que se usan: las dem&aacute;s sobran.'],
         ok=1,
         por=u'4 &times; 5 = <b>20</b>. Las que dejes en blanco son exactamente por donde se va a '
             u'romper el automatismo, porque son los casos que no te has planteado. Contestar '
             u'&laquo;no hace nada&raquo; <b>es</b> contestar.'),
]

S4_CIERRE = u'''
      <ol>
      ''' + pregunta(u'&iquest;Qu&eacute; cuatro piezas tiene una m&aacute;quina de estados?',
                     u'<p><b>Estados</b> (en cu&aacute;l est&aacute;s, y solo en uno), <b>eventos</b> '
                     u'(lo que puede llegar), <b>transiciones</b> (qu&eacute; evento te lleva de '
                     u'd&oacute;nde a d&oacute;nde) y <b>acciones</b> (lo que se hace mientras est&aacute;s '
                     u'en cada estado).</p>') + pregunta(
          u'&iquest;Por qu&eacute; se prohíbe <code>delay()</code> y se usa <code>millis()</code>?',
          u'<p>Porque durante un <code>delay()</code> el programa <b>no mira nada</b>: los eventos '
          u'que llegan se pierden sin dejar rastro. Con <code>millis()</code> el programa sigue dando '
          u'vueltas al <code>loop()</code> y solo <b>comprueba</b> si ya ha pasado el tiempo.</p>'
          ) + pregunta(
          u'Tu automatismo lleva enchufado en el pasillo dos meses y se queda colgado un d&iacute;a. '
          u'&iquest;Qu&eacute; ser&iacute;a lo primero que mirar&iacute;as?',
          u'<p>Si has escrito <code>millis() &gt; t0 + ESPERA</code>. <code>millis()</code> da la '
          u'vuelta a los <b>49 d&iacute;as y 17 horas</b>, y escrito as&iacute; el automatismo se '
          u'queda esperando. Escrito <code>millis() - t0 &gt; ESPERA</code> funciona igual antes y '
          u'despu&eacute;s de la vuelta.</p>') + pregunta(
          u'&iquest;Por qu&eacute; la misma m&aacute;quina de cuatro estados sirve para la barrera, '
          u'para el riego y para el contenedor?',
          u'<p>Porque los tres son automatismos <b>de un ciclo</b>: reposo &rarr; actuar &rarr; '
          u'mantener &rarr; volver. Lo que cambia son los <b>r&oacute;tulos</b> y qu&eacute; sensor '
          u'dispara cada evento; las flechas son las mismas. Por eso conviene empezar siempre por ese '
          u'esqueleto.</p>') + u'''
      </ol>
''' + test('c7', u'Lo que tiene que haber quedado de estas cuatro sesiones', PREGUNTAS_TEST) + u'''
      <div class="nota">
        <span class="n-tag">Lo que queda de unidad</span>
        Ya tienes el programa bien escrito y la tabla rellena. Lo que falta es lo que de verdad da
        trabajo: <b>montarlo</b> sin que la placa se reinicie cada vez que arranca el motor
        &mdash;que es lo que va a pasar&mdash;, conseguir que <b>vuelva a casa</b> y encuentre su
        cero, y decidir qu&eacute; hace el aparato el d&iacute;a que se le va la luz a mitad de
        maniobra. Eso son las cuatro sesiones siguientes.
      </div>
'''


# ==========================================================================
# La unidad
# ==========================================================================
S1 = (bloque('00', u'Reto inicial &middot; 10 min', S1_RETO + narrador() + S1_RETO_B) +
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
      bloque('01', u'Teor&iacute;a &middot; 25 min', S4_TEORIA) +
      bloque('02', u'Pr&aacute;ctica &middot; 15 min', S4_PRACTICA) +
      bloque('03', u'Cierre y test &middot; 10 min', S4_CIERRE))

MIN = [(u"10'", u'Reto'), (u"25'", u'Teor&iacute;a'), (u"20'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')]

S = [
    dict(corto=u'Qu&eacute; es un robot',
         titulo=u'Un lavavajillas tiene programa, motores y sensores. Y no es un robot',
         entradilla=u'La frontera &uacute;til no es el aspecto ni el programa: es si la m&aacute;quina '
                    u'se entera de lo que hay fuera. Se ve fallar en un aula a la que alguien le ha '
                    u'movido las mesas.',
         minutado=MIN, chips=[u'CE4 &middot; 4.1', u'B.1', u'B.2'], cuerpo=S1),
    dict(corto=u'El motor no sabe d&oacute;nde est&aacute;',
         titulo=u'&laquo;Avanza medio metro&raquo;: cinco pruebas, cinco distancias',
         entradilla=u'Un <code>delay()</code> mide tiempo, no distancia. Tres motores con el mismo '
                    u'encargo, y la pareja de palabras que hay que separar: exactitud y '
                    u'precisi&oacute;n.',
         minutado=MIN, chips=[u'CE4 &middot; 4.1', u'B.2', u'B.3'], cuerpo=S2),
    dict(corto=u'Grados de libertad y el brazo',
         titulo=u'Con un servo llegas a una circunferencia. Y las macetas no est&aacute;n ah&iacute;',
         entradilla=u'Cu&aacute;ntos grados de libertad hacen falta, d&oacute;nde acaba la punta de '
                    u'un brazo de dos eslabones, y por qu&eacute; el problema de la vuelta no tiene '
                    u'una respuesta sino dos.',
         minutado=MIN, chips=[u'CE4 &middot; 4.1', u'B.2', u'B.3', u'B.4'], cuerpo=S3),
    dict(corto=u'M&aacute;quina de estados',
         titulo=u'Un <code>delay()</code> no es una pausa: es un rato sin mirar',
         entradilla=u'Cuatro estados, cinco eventos y veinte casillas que hay que contestar una a '
                    u'una. Las que dejes en blanco son por donde se rompe.',
         minutado=[(u"10'", u'Reto'), (u"25'", u'Teor&iacute;a'), (u"15'", u'Pr&aacute;ctica'),
                   (u"10'", u'Cierre y test')],
         chips=[u'CE4 &middot; 4.1', u'B.2', u'B.3', u'B.4'], cuerpo=S4),
]

# --- la segunda mitad, escrita aparte en c7b_texto.py ---
# Aqui la unidad cambia de marcha: el proyecto del curso YA esta decidido
# (PROYECTOS.md, bloque DECIDIDO del 18-sep-2026), asi que las sesiones 5 a 8
# no rotan ejemplos: aterrizan en el riego automatico y en sus dos variantes.
S += c7b_texto.sesiones(bloque)
PENDIENTES.extend(c7b_texto.PENDIENTES)

CFG = dict(
    ruta='4eso/Tecnologia/tema7/',
    migas=u'<a href="../../../">Materiales</a> &middot; <a href="../../">4.&ordm; ESO</a> '
          u'&middot; <a href="../">Tecnolog&iacute;a</a> &middot; Tema 7',
    h1=u'Rob&oacute;tica y automatismos',
    titulo=u'Tema 7 &middot; Rob&oacute;tica y automatismos',
    tema=u'Tema 7', curso=u'4.&ordm; de ESO', materia=u'Tecnolog&iacute;a',
    desc=u'Tema 7 de Tecnolog&iacute;a de 4.&ordm; de ESO: qu&eacute; es un robot y qu&eacute; no, '
         u'motores de corriente continua, servo y paso a paso, grados de libertad y cinem&aacute;tica '
         u'de un brazo, y la m&aacute;quina de estados como herramienta para programar un '
         u'automatismo.',
    sesiones=S)


if __name__ == '__main__':
    destino = os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema7')
    if not os.path.isdir(destino):
        os.makedirs(destino)
    html = pagina(CFG)
    if USA_AVATAR[0]:
        html = html.replace(u'</style>', avatar_flat.CSS + u'</style>', 1)
    io.open(os.path.join(destino, 'index.html'), 'w', encoding='utf-8', newline='').write(html)
    print('Tema 7 de 4.o generado: %d bytes, %d sesiones (%d escritas, %d pendientes)'
          % (len(html), len(S), sum(1 for x in S if not x.get('pendiente')),
             sum(1 for x in S if x.get('pendiente'))))
    for p in PENDIENTES:
        print('  !! ' + p)
