# -*- coding: utf-8 -*-
"""4.o de ESO - Tecnologia - Tema 9 - Tecnologia y sociedad: proyectos de servicio.

    ~/venv/bin/python generadores/c9_build.py

Escribe 4eso/Tecnologia/tema9/index.html. La "c" de los generadores de esta
unidad es de "cuarto": no choca con los u*_ de 2.o.

Ocho sesiones. Aqui estan escritas las CUATRO primeras; las otras cuatro
aparecen en la barra con su titulo y el boton desactivado.

Criterios: CE2 / 2.1 y CE6 / 6.1, 6.2, 6.3. Ver CURRICULO.md.

Es la unidad que cierra el curso: recoge el proyecto y lo mira desde fuera.
El hilo, que es lo que importa:

  S1  Tu aparato funciona. Pero hay tecnologia que funciona desde hace
      decadas y no llega a quien la necesita. No hay conspiracion: hay una
      division. Precio minimo frente a lo que puede pagar quien lo sufre.
      Y el segundo mecanismo, que es el de su instituto: quien decide no es
      quien lo sufre.
  S2  Vale, ya se por que no se fabrica. Peor: cosas que SI se fabricaron,
      SI se pagaron y SI llegaron, y no sirvieron. La solucion buena depende
      del sitio. Aparece "tecnologia apropiada", y el balance de energia de
      sus tres proyectos en tres sitios distintos.
  S3  Ya sabes si sirve y a quien. Ahora hay que defenderlo ante gente que no
      estaba, en seis minutos, con una rubrica que se da por adelantado. Y
      contestar la pregunta incomoda sin inventarse un numero.
  S4  Queda la pregunta mas incomoda: fabricarlo tambien costo algo.
      Cuando devuelve lo que costo? Cierre del curso y test.

Los ejemplos van SIEMPRE con los tres proyectos decididos en PROYECTOS.md
(A riego, B aviso de aula, C lampara), repartidos para que no salga siempre
el riego.
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unidad_base import pagina, bloque, ficha, pregunta
import avatar_flat
from c9_escenas import MERCADO, SITIO
from c9_escenas2 import RUBRICA, RETORNO
from test_auto import test

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USA_AVATAR = [False]


# --------------------------------------------------------------------------
# Piezas repetidas
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


def narrador():
    """La voz de la unidad. Solo se monta si estan el mp3 y su envolvente."""
    env = os.path.join(RAIZ, '_env_c9-sociedad.json')
    mp3 = os.path.join(RAIZ, 'audio', 'c9-sociedad.mp3')
    if not (os.path.exists(env) and os.path.exists(mp3)):
        return u''
    USA_AVATAR[0] = True
    return avatar_flat.componente(
        'narr-c9', u'De qu&eacute; va esta unidad',
        u'Tu aparato funciona y casi no contamina. &iquest;A qui&eacute;n le sirve de verdad, y '
        u'qui&eacute;n decidi&oacute; que ese era el problema que hab&iacute;a que resolver?',
        '../../../audio/c9-sociedad.mp3',
        json.load(io.open(env, encoding='utf-8')),
        u'Voz sintetizada sobre gui&oacute;n propio. La boca sigue el volumen real de la voz.')


# ==========================================================================
# SESION 1 - Quien decide que se fabrica
# ==========================================================================
S1_RETO = u'''
      <p>Llevas el curso entero con el mismo aparato. Lo detectaste, lo dise&ntilde;aste, lo fabricaste,
         lo contaste, lo automatizaste y lo has medido. Y <b>funciona</b>. Esta unidad va de algo que
         no se puede hacer hasta que funciona: <b>mirarlo desde fuera</b>.</p>
'''

S1_RETO_B = u'''
      <div class="aviso">
        <span class="n-tag">El encargo</span>
        Escribid en el cuaderno <b>tres problemas</b> de vuestro barrio o de vuestro centro que se
        podr&iacute;an resolver con tecnolog&iacute;a que <b>ya existe</b>. No que habr&iacute;a que
        inventar: que ya existe y se puede comprar. Tres minutos.
      </div>
      <p>Ahora, al lado de cada uno, escribid <b>por qu&eacute; no est&aacute; resuelto</b>.</p>
      <p>Lo que sale casi siempre es <i>&laquo;no hay dinero&raquo;</i>, <i>&laquo;no
         interesa&raquo;</i> o <i>&laquo;a los de arriba les da igual&raquo;</i>. El problema de esas
         tres frases es que son <b>la misma frase</b>, y sirve para explicarlo todo: lo que explica
         cualquier cosa no explica ninguna. As&iacute; que vamos a cambiarla por una cuenta.</p>
      <p>Empecemos por un dato que no es una opini&oacute;n:</p>
      <div class="def">
        <span class="n-tag">El dato</span>
        Entre <b>1975 y 1999</b> se pusieron a la venta <b>1.393 medicamentos nuevos</b> en el mundo.
        De esos, <b>16</b> eran para enfermedades tropicales y tuberculosis. El <b>1,1 %</b>. Esas
        enfermedades las sufren <b>cientos de millones de personas</b>.
        <span class="credito" style="margin-top:8px">Trouiller, Olliaro, Torreele, Orbinski, Laing y
          Ford (2002). <i>Drug development for neglected diseases: a deficient market and a
          public-health policy failure</i>. The Lancet, 359, 2188-2194.</span>
      </div>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento antes de seguir</span>
        <p>No hay ninguna ley que prohíba fabricar esos medicamentos. No hay nadie reunido en un
           s&oacute;tano decidiendo que no. Y aun as&iacute;, de 1.393 salieron 16.
           <b>&iquest;Qu&eacute; es lo que lo decide, entonces?</b> Escribe tu hip&oacute;tesis en el
           cuaderno. Dentro de diez minutos la comprobamos con n&uacute;meros.</p>
      </div>
'''

S1_TEORIA = u'''
      <p>La respuesta que damos casi todos es: <i>&laquo;se fabrica lo que la gente
         necesita&raquo;</i>. Vamos a ver qu&eacute; pasa si eso fuera verdad.</p>
      <p>Si se fabricara lo que hace falta, los 1.393 medicamentos se repartir&iacute;an m&aacute;s o
         menos como se reparte el da&ntilde;o. El paludismo solo caus&oacute; <b>282 millones de casos</b>
         y <b>610.000 muertes</b> en 2024, seg&uacute;n la Organizaci&oacute;n Mundial de la Salud.
         Con ese peso, deber&iacute;a llevarse una parte grande del reparto. Se llev&oacute; una parte
         min&uacute;scula. <b>La soluci&oacute;n ingenua no explica lo que pasa</b>, as&iacute; que hay
         que cambiarla.</p>
      <div class="copiar">
        <h4>Necesitar y poder pagar no son lo mismo</h4>
        <p>Un mercado no cuenta personas: cuenta <b>euros</b>. Lo que mueve a una empresa no es
           cu&aacute;nta gente sufre un problema, es cu&aacute;nta gente sufre ese problema
           <b>y puede pagar por quit&aacute;rselo</b>. A eso se le llama <b>demanda solvente</b>.</p>
        <p>Cien millones de personas que no tienen un euro <b>no son un mercado</b>. Dos millones que
           pueden pagar trescientos euros al a&ntilde;o, s&iacute;.</p>
      </div>
      <p>Y ahora la cuenta, que es m&aacute;s sencilla de lo que parece. Antes de fabricar nada hay que
         <b>desarrollarlo</b>: dise&ntilde;arlo, probarlo, certificarlo. Eso se paga <b>una vez y por
         adelantado</b>, antes de vender ni una unidad.</p>
      <div class="copiar">
        <h4>La cuenta que decide qu&eacute; se fabrica</h4>
        <p style="font-family:var(--f-m);font-size:14px">precio m&iacute;nimo =
           coste de desarrollo &divide; (personas que lo comprar&aacute;n &times; a&ntilde;os de venta)</p>
        <p>Ese es el precio por debajo del cual la empresa <b>pierde dinero</b>. Despu&eacute;s se
           compara con una sola cosa:</p>
        <ul>
          <li>Si el precio m&iacute;nimo <b>cabe</b> en lo que puede pagar quien lo sufre, se fabrica.</li>
          <li>Si <b>no cabe</b>, no se fabrica. Y no ha hecho falta que nadie lo decida: <b>sale de la
              divisi&oacute;n</b>.</li>
        </ul>
        <p>Por eso una enfermedad que sufren ocho millones de personas muy pobres puede quedarse sin
           medicamento mientras otra que sufren treinta millones de personas con sueldo tiene cuatro.</p>
      </div>
      <p>Pru&eacute;balo. Elige un problema pinchando en su barra, mira la cuenta escrita a la derecha
         y despu&eacute;s mueve los tres mandos. Fíjate sobre todo en el bot&oacute;n de arriba:
         <b>reordena por personas atendidas</b> y mira si el orden cambia.</p>
''' + MERCADO + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>&iquest;Por qu&eacute; aparecen los <b>a&ntilde;os de exclusiva</b> en la cuenta? Por la
           <b>patente</b>. Una patente da al que inventa algo el derecho a ser el &uacute;nico que lo
           fabrica durante <b>veinte a&ntilde;os desde que la solicita</b>, y a cambio le obliga a
           <b>publicar exactamente c&oacute;mo se hace</b>.</p>
        <p>No es un regalo ni es un robo: es un <b>trato</b>, y tiene sus dos caras. Sin patente, el
           primero que copie vende m&aacute;s barato porque no ha pagado el desarrollo, as&iacute; que
           nadie desarrolla nada. Con patente, durante esos a&ntilde;os el precio lo pone uno solo, y
           puede ponerlo donde quiera. Las dos cosas son verdad a la vez.</p>
      </div>

      <h3>El segundo mecanismo, y este lo ten&eacute;is en vuestro instituto</h3>
      <p>Mira otra vez la barra del <b>aire cargado en el aula</b>, que es vuestro proyecto B. Lo que
         paga el que lo sufre es <b>casi cero</b>, y no porque sea pobre.</p>
      <div class="copiar">
        <h4>Quien decide no es quien lo sufre</h4>
        <p>Un alumno pasa cinco horas al d&iacute;a en un aula cargada. Le duele la cabeza, se duerme
           y rinde menos. Y <b>no compra nada</b>: quien compra es el centro, y quien paga es la
           administraci&oacute;n. <b>El que sufre el problema no est&aacute; en la mesa donde se
           decide.</b></p>
        <p>Esto no pasa solo en los institutos. Pasa cada vez que el que <b>elige</b> un aparato, el
           que lo <b>paga</b> y el que lo <b>sufre</b> son personas distintas:</p>
        <ul>
          <li>el que elige la impresora del centro no es el que se pelea con ella;</li>
          <li>el que dise&ntilde;a un mando a distancia con botones de cuatro mil&iacute;metros no
              tiene artrosis;</li>
          <li>el que decide d&oacute;nde va una parada de autob&uacute;s no la espera bajo la lluvia.</li>
        </ul>
        <p>Cuando esos tres papeles se separan, el aparato que sale es peor. Y no porque nadie tenga
           mala intenci&oacute;n.</p>
      </div>
''' + foto('c9-mosquitera.jpg',
           u'Ni&ntilde;os durmiendo bajo una mosquitera tratada con insecticida, colgada sobre la cama',
           u'Una <b>mosquitera tratada con insecticida</b>. No lleva electr&oacute;nica, no lleva '
           u'programa y no hay nada que inventar: existe desde hace d&eacute;cadas, cuesta unos pocos '
           u'euros y evita casos de paludismo mientras dura. Que haya tardado tanto en llegar a donde '
           u'hace falta <b>no es un problema t&eacute;cnico</b>: en la cuenta de arriba, quien la '
           u'necesita no pod&iacute;a pagarla, as&iacute; que hizo falta que el dinero lo pusiera otro.',
           u'HarunaSylvester', u'CC BY-SA 4.0',
           u'https://commons.wikimedia.org/wiki/File:Averting_malaria_by_sleeping_under_an_'
           u'insecticide_treated_net.jpg') + u'''
      <div class="copiar">
        <h4>Cuatro maneras de arreglarlo, sin cambiar de planeta</h4>
        <p>Si el problema est&aacute; en la divisi&oacute;n, hay cuatro sitios donde meter mano:</p>
        <ol>
          <li><b>Dinero p&uacute;blico en el desarrollo.</b> Si el coste de desarrollo ya
              est&aacute; pagado, el precio m&iacute;nimo baja de golpe. Es lo que hace la
              investigaci&oacute;n de las universidades.</li>
          <li><b>Compra garantizada.</b> Alguien se compromete por adelantado a comprar tantas
              unidades a tanto el precio. La empresa ya sabe que recupera antes de empezar.</li>
          <li><b>Premio.</b> Se paga por <b>conseguirlo</b>, no por venderlo. Quien lo gana cobra
              aunque despu&eacute;s lo regale.</li>
          <li><b>Hacerlo sin &aacute;nimo de lucro.</b> Universidades, fundaciones, cooperativas,
              gente que publica el dise&ntilde;o para que cualquiera lo copie.</li>
        </ol>
        <p>Y aqu&iacute; va lo que quiero que te lleves de hoy: <b>vuestro proyecto es la cuarta</b>.
           El aviso de aula bien ventilada no lo va a fabricar nadie porque la cuenta no sale. Por eso
           lo est&aacute;is haciendo vosotros.</p>
      </div>
''' + video('video-c9-olvidadas', 'EydFlOUooN4',
            u'No te olvides de las enfermedades olvidadas (corto documental)',
            u'Canal: Barcelona Institute for Global Health (ISGlobal)',
            u'Un corto de un centro de investigaci&oacute;n sobre las enfermedades que casi no salen '
            u'en la cuenta de arriba.')

S1_PRACTICA = ficha(
    u'Actividad 1 &middot; &iquest;Qui&eacute;n fabricar&iacute;a vuestro proyecto?',
    [u'6.1', u'6.2', u'D.1', u'D.2'], u'Grupos de tres &middot; 20 min', u'''
          <h4>Primera parte &middot; la cuenta, con la escena (10 min)</h4>
          <p>Con la escena de arriba, y anotando <b>la cuenta entera</b> en la libreta, no solo el
             resultado:</p>
          <ol class="pasos">
            <li>Elegid <b>vuestro</b> proyecto (A, B o C) y el problema de la escena que m&aacute;s se
                le parezca. Copiad las cinco l&iacute;neas de la cuenta.</li>
            <li>Con los mandos a 60 %, 10 a&ntilde;os y 0 &euro; de dinero p&uacute;blico,
                &iquest;sale o no sale? Decid <b>en euros</b> cu&aacute;nto sobra o cu&aacute;nto falta
                por persona y a&ntilde;o.</li>
            <li>Buscad <b>el mando m&iacute;nimo</b> que le da la vuelta: el dinero p&uacute;blico
                m&aacute;s peque&ntilde;o con el que deja de dar p&eacute;rdidas. Anotad la cifra.</li>
            <li>Pulsad <b>ordenar por personas atendidas</b>. Copiad los dos &oacute;rdenes, uno
                debajo del otro, y explicad con una frase <b>por qu&eacute;</b> no coinciden.</li>
          </ol>
          <h4>Segunda parte &middot; la misma cuenta, aqu&iacute; dentro (10 min)</h4>
          <p>Un medidor de CO<sub>2</sub> de pared para un aula se compra hecho por unos
             <b>120 &euro;</b>. No hay que inventarlo: est&aacute; en cualquier cat&aacute;logo.</p>
          <ul>
            <li>Contad las aulas de vuestro centro. Multiplicad por 120 &euro;. Esa es la cifra.</li>
            <li>Escribid <b>tres cosas</b> que el centro s&iacute; haya comprado este curso y que
                cuesten parecido. &iquest;Est&aacute;n todas por encima de esto en la lista de
                prioridades? Razonadlo, sin ironías.</li>
            <li>Decid <b>qui&eacute;n</b> tendr&iacute;a que decidirlo: no &laquo;el
                instituto&raquo;, sino un <b>cargo concreto</b>. Averiguadlo.</li>
            <li>Y la de verdad: si el aparato lo constru&iacute;s vosotros por 5 &euro;,
                &iquest;qui&eacute;n tiene que dar permiso para colgarlo en la pared? Escribid a
                qui&eacute;n se lo preguntar&iacute;ais y qu&eacute; le dir&iacute;ais.</li>
          </ul>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>La cuenta de la escena, copiada entera y con unidades <b>(2 puntos)</b>.</li>
            <li>El dinero p&uacute;blico m&iacute;nimo que le da la vuelta, con su cifra
                <b>(2 puntos)</b>.</li>
            <li>La explicaci&oacute;n de por qu&eacute; los dos &oacute;rdenes no coinciden
                <b>(2 puntos)</b>.</li>
            <li>La cuenta de las aulas y las tres compras comparadas <b>(2 puntos)</b>.</li>
            <li>El cargo concreto, con nombre de puesto y no &laquo;el instituto&raquo;
                <b>(2 puntos)</b>.</li>
          </ul>
''')

S1_CIERRE = u'''
      <ol>
      ''' + pregunta(u'&iquest;Por qu&eacute; &laquo;se fabrica lo que la gente necesita&raquo; no '
                     u'explica lo de los 1.393 medicamentos?',
                     u'<p>Porque si fuera verdad el reparto se parecer&iacute;a al del da&ntilde;o, y '
                     u'no se parece: enfermedades que sufren cientos de millones de personas se '
                     u'llevaron el 1,1 %. Lo que se reparte no sigue al da&ntilde;o, sigue al '
                     u'<b>dinero que hay detr&aacute;s de ese da&ntilde;o</b>.</p>') + pregunta(
          u'&iquest;Qu&eacute; es la demanda solvente, y en qu&eacute; se diferencia de la necesidad?',
          u'<p>La <b>necesidad</b> es cu&aacute;nta gente sufre el problema. La <b>demanda '
          u'solvente</b> es cu&aacute;nta gente sufre el problema <b>y puede pagar por '
          u'quit&aacute;rselo</b>. El mercado solo ve la segunda, porque es la &uacute;nica que se '
          u'convierte en euros.</p>') + pregunta(
          u'Escribe la cuenta que decide si algo se fabrica, y di qu&eacute; se compara con qu&eacute;.',
          u'<p><b>Precio m&iacute;nimo = coste de desarrollo &divide; (personas que lo '
          u'comprar&aacute;n &times; a&ntilde;os de venta)</b>. Ese precio m&iacute;nimo se compara '
          u'con <b>lo que puede pagar quien lo sufre</b>. Si no cabe, no se fabrica, y no hace falta '
          u'que nadie lo decida.</p>') + pregunta(
          u'Un medidor de CO<sub>2</sub> de aula existe y cuesta 120 &euro;. &iquest;Por qu&eacute; '
          u'no hay uno en cada clase?',
          u'<p>Porque <b>quien lo sufre no es quien compra</b>. El alumno que aguanta el aula cargada '
          u'no tiene con qu&eacute; comprarlo y no est&aacute; en la mesa donde se decide; el que '
          u'decide no pasa cinco horas ah&iacute; dentro. Cuando el que elige, el que paga y el que '
          u'sufre son tres personas distintas, lo que se compra es peor.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya sabemos por qu&eacute; hay cosas que no se fabrican. Pero hay un caso peor, y es el que
        viene ahora: un aparato que <b>s&iacute;</b> se invent&oacute;, <b>s&iacute;</b> se
        pag&oacute; con dinero de sobra, <b>s&iacute;</b> gan&oacute; un premio del Banco Mundial y
        <b>s&iacute;</b> se instal&oacute; mil veces donde hac&iacute;a falta. Y no sirvi&oacute;.
        No fall&oacute; la financiaci&oacute;n: fall&oacute; <b>una divisi&oacute;n que nadie
        hizo</b>.
      </div>

      <div class="copiar" style="border-color:var(--goo-verde)">
        <h4>Lectura del tema</h4>
        <p>Una sesi&oacute;n entera para leer y contestar. Conviene hacerla <b>pronto</b>, entre
           esta sesi&oacute;n y la siguiente, porque cuenta con detalle los dos casos que van a
           salir despu&eacute;s. <b>30 p&aacute;rrafos numerados</b>: cada uno lee el suyo en voz
           alta, en orden. Despu&eacute;s, diez preguntas por escrito.</p>
        <p style="margin-top:10px"><a href="lectura-tema9.pdf" target="_blank" rel="noopener"
           style="font-family:var(--f-m);font-size:13px;color:var(--goo-verde);font-weight:500">
           &#8595; El columpio que sacaba agua &middot; PDF</a></p>
      </div>
'''


# ==========================================================================
# SESION 2 - Tecnologia apropiada
# ==========================================================================
S2_RETO = u'''
      <p>Esta es la historia de un aparato que lo tuvo <b>todo</b> a favor.</p>
      <div class="aviso">
        <span class="n-tag">La PlayPump, en siete fechas</span>
        <b>1989</b>: Ronnie Stuiver, sondista sudafricano, ense&ntilde;a en una feria agr&iacute;cola un
        tiovivo que, al girar, bombea agua de un pozo. <b>1994</b>: Trevor Field instala los dos
        primeros en KwaZulu-Natal. <b>1999</b>: Nelson Mandela inaugura uno en un colegio.
        <b>2000</b>: premio del Banco Mundial. <b>2006</b>: en la Clinton Global Initiative se
        prometen <b>16,4 millones de d&oacute;lares</b> para instalar m&aacute;s. <b>2008</b>: van mil
        bombas instaladas. <b>2009</b>: PlayPumps International deja de instalar ninguna m&aacute;s.
      </div>
      <p>La idea es preciosa y se entiende en cinco segundos: los ni&ntilde;os juegan, y mientras
         juegan sale agua. El folleto promet&iacute;a <b>2.500 personas por bomba</b> y hasta
         <b>1.400 litros por hora</b> desde cuarenta metros de profundidad.</p>
      <div class="reto-piensa">
        <span class="n-tag">Antes de que te cuente qu&eacute; pas&oacute;</span>
        <p>Haz t&uacute; la cuenta. Una persona necesita unos <b>diez litros al d&iacute;a</b> para
           sobrevivir: beber, cocinar y lavarse lo m&iacute;nimo. Si la bomba tiene que dar de beber a
           2.500 personas y sube 1.400 litros cada hora, <b>&iquest;cu&aacute;ntas horas al d&iacute;a
           tiene que estar girando ese tiovivo?</b></p>
        <p>Es una divisi&oacute;n. H&aacute;zla en el cuaderno <b>antes</b> de tocar la escena.</p>
      </div>
''' + SITIO + u'''
      <p>Con los n&uacute;meros que promet&iacute;a el folleto salen casi <b>dieciocho horas</b> de
         girar sin parar. Cuando alguien fue a medir el caudal de verdad, la cuenta sub&iacute;a a
         <b>veintisiete horas al d&iacute;a</b>. Un d&iacute;a tiene veinticuatro.</p>
      <p>Nadie minti&oacute;, y probablemente nadie hizo la divisi&oacute;n. Y esa divisi&oacute;n
         est&aacute; al alcance de cualquiera de vosotros.</p>
'''

S2_TEORIA = u'''
      <p>La PlayPump no fall&oacute; por falta de dinero ni por mala fe. Fall&oacute; por otra cosa,
         y esa cosa tiene nombre desde 1973.</p>
      <div class="copiar">
        <h4>Tecnolog&iacute;a apropiada</h4>
        <p>Es la que <b>encaja con el sitio donde va a vivir</b>: con la energ&iacute;a que hay
           all&iacute;, con los materiales que se consiguen all&iacute;, con las manos que la van a
           manejar y con el dinero que hay para arreglarla.</p>
        <p>El t&eacute;rmino lo populariz&oacute; el economista <b>E. F. Schumacher</b> en 1973, en un
           libro llamado <i>Lo peque&ntilde;o es hermoso</i>. &Eacute;l la llamaba
           <i>tecnolog&iacute;a intermedia</i>: ni la azada sola ni la cosechadora de cien mil euros,
           sino lo que de verdad se puede mantener funcionando.</p>
        <p><b>Apropiada no quiere decir pobre, ni de segunda, ni sin electr&oacute;nica.</b> Quiere
           decir <b>adecuada a ese sitio</b>. En vuestro instituto, con enchufe, wifi, taller y
           alguien que sabe, un Arduino <b>s&iacute;</b> es tecnolog&iacute;a apropiada. En un huerto
           a tres kil&oacute;metros, puede que no.</p>
      </div>
      <div class="copiar">
        <h4>Las cinco preguntas del sitio</h4>
        <p>Antes de dar por bueno un dise&ntilde;o, se le hacen estas cinco. Si alguna no tiene
           respuesta, el dise&ntilde;o <b>no est&aacute; terminado</b>, aunque funcione en la mesa:</p>
        <ol>
          <li><b>&iquest;De d&oacute;nde sale la energ&iacute;a?</b> Y no vale &laquo;de la
              bater&iacute;a&raquo;: &iquest;y cuando se acabe?</li>
          <li><b>&iquest;Qui&eacute;n lo maneja?</b> &iquest;Sabe? &iquest;Quiere? &iquest;Le
              compensa?</li>
          <li><b>&iquest;Qui&eacute;n lo arregla, y con qu&eacute; pieza?</b> &iquest;A cu&aacute;ntos
              kil&oacute;metros est&aacute; esa pieza y cu&aacute;nto cuesta?</li>
          <li><b>&iquest;Qu&eacute; pasa el d&iacute;a que falla?</b> &iquest;Se nota? &iquest;Se queda
              algo peor que antes de ponerlo?</li>
          <li><b>&iquest;Qui&eacute;n decidi&oacute; que este era el problema?</b> &iquest;Se lo
              pregunt&oacute; alguien a quien lo sufre?</li>
        </ol>
        <p>La PlayPump fallaba en la uno, en la tres y en la cinco. La bomba de mano de toda la vida,
           que era lo que hab&iacute;a antes, no fallaba en ninguna.</p>
      </div>

      <h3>Un aparato que aprueba las cinco</h3>
''' + foto('c9-olla-barro.jpg',
           u'Vendedoras de verdura en un mercado de Ouahigouya, con una vasija de barro dentro de un '
           u'barre&ntilde;o met&aacute;lico en primer plano',
           u'Un mercado en <b>Ouahigouya (Burkina Faso)</b>. Delante, esa vasija de barro metida en un '
           u'barre&ntilde;o es un <b>frigor&iacute;fico</b>: una olla dentro de otra con arena mojada '
           u'en medio. El agua se evapora, y para evaporarse tiene que robar calor de dentro. No lleva '
           u'motor, ni corriente, ni pieza que se rompa. <b>Mohammed Bah Abba</b> lo volvi&oacute; a '
           u'poner en circulaci&oacute;n en el norte de Nigeria en los a&ntilde;os noventa: hizo las '
           u'primeras <b>5.000 unidades</b>, gan&oacute; el Premio Rolex a la Iniciativa en <b>2001</b> '
           u'con sus 75.000 d&oacute;lares y los gast&oacute; en repartirlas. Cuando se rompe una, se '
           u'arregla con barro. Solo funciona donde el aire est&aacute; seco: <b>tambi&eacute;n esto '
           u'depende del sitio</b>.',
           u'Peter Rinker', u'CC BY-SA 3.0',
           u'https://commons.wikimedia.org/wiki/File:Gem%C3%BCseverk%C3%A4uferinnen_mit_Tonkrugk'
           u'%C3%BChler,_Female_vegetable_sellers_with_clay_pot_cooler,_vendeuses_des_l%C3%A9gumes_'
           u'avec_un_canari_frigo,_Ouahigouya,_Burkina_Faso.JPG') + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Ojo con la conclusi&oacute;n f&aacute;cil. Esto <b>no</b> significa que lo sencillo sea
           siempre mejor, ni que la electr&oacute;nica sobre. La olla de barro no enfr&iacute;a por
           debajo de cierta temperatura, no sirve donde el aire est&aacute; h&uacute;medo y no vale
           para una vacuna. <b>No es una nevera mala: es la soluci&oacute;n correcta en un sitio
           concreto</b>, igual que un Arduino es la correcta en el vuestro. Lo apropiado no es una
           categor&iacute;a del aparato: es una relaci&oacute;n entre el aparato y el sitio.</p>
      </div>

      <h3>Ahora el vuestro, y con n&uacute;meros</h3>
      <p>Vuelve a la escena de arriba y cambia al modo <b>&laquo;Tu proyecto en tres sitios&raquo;</b>.
         Elige el proyecto <b>C</b>, la l&aacute;mpara, y ponlo en el instituto. Despu&eacute;s
         mu&eacute;velo a la aldea y al huerto, sin tocar nada m&aacute;s.</p>
      <div class="copiar">
        <h4>La cuenta de la energ&iacute;a, que es la que casi nadie hace</h4>
        <p>La energ&iacute;a que gasta un aparato al d&iacute;a, en <b>vatios-hora</b>:</p>
        <p style="font-family:var(--f-m);font-size:14px">Wh = V &times; A &times; horas</p>
        <p>Y lo que aguanta con lo que tiene guardado:</p>
        <p style="font-family:var(--f-m);font-size:14px">autonom&iacute;a (d&iacute;as) =
           energ&iacute;a guardada (Wh) &divide; consumo al d&iacute;a (Wh)</p>
        <p>Una pila AA alcalina guarda del orden de <b>3,7 Wh</b> (unos 2.500 mAh a 1,5 V), as&iacute;
           que cuatro dan unos <b>15 Wh</b>. Un panel solar de 5 W en un sitio con cuatro horas de sol
           bueno y un rendimiento del 70 % mete unos <b>14 Wh al d&iacute;a</b>.</p>
      </div>
      <div class="copiar">
        <h4>Lo que sale, y no es lo que todo el mundo espera</h4>
        <p>Con el riego autom&aacute;tico, la bomba funciona <b>cuarenta segundos al d&iacute;a</b> y
           se lleva unas cent&eacute;simas de vatio-hora. La placa Arduino, que no hace nada el
           99,95 % del tiempo, se lleva <b>5,4 Wh</b>. O sea: <b>casi toda la energ&iacute;a se va en
           esperar</b>, no en trabajar.</p>
        <p>Consecuencia directa para vuestro proyecto: si alguna vez tiene que ir a pilas, lo que hay
           que atacar <b>no es el actuador</b>. Es el tiempo que la placa est&aacute; despierta sin
           necesidad.</p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>En la escena, marca <b>la placa duerme entre medidas</b>. El consumo baja, pero no baja
           tanto como esperabas: se queda en 12 mA. Es que una placa Uno entera <b>no puede dormir</b>
           del todo. El regulador de tensi&oacute;n, el LED verde de encendido y el chip del puerto USB
           siguen chupando aunque el microcontrolador est&eacute; parado.</p>
        <p>El ATmega328P <b>solo</b>, sin placa, dormido de verdad, baja a <b>mil&eacute;simas</b> de
           eso. Por eso los aparatos a pilas de verdad no llevan dentro una placa Arduino: llevan el
           chip pelado. Es un salto que ya no cabe en 4.&ordm;, pero conviene saber que existe.</p>
      </div>
''' + video('video-c9-nevera', 'wDyCMVmY-Vk',
            u'C&oacute;mo esta nevera que no necesita electricidad salv&oacute; a una empresa de '
            u'cer&aacute;mica india',
            u'Canal: Insider Espa&ntilde;ol',
            u'La misma idea de la olla de barro, llevada a un producto que se vende. Sirve para '
            u'discutir si sigue siendo tecnolog&iacute;a apropiada cuando se convierte en un negocio.')

S2_PRACTICA = ficha(
    u'Actividad 2 &middot; El mismo proyecto en tres sitios, y un redise&ntilde;o',
    [u'6.1', u'6.3', u'D.2', u'D.3'], u'Grupos de tres &middot; 20 min', u'''
          <h4>Primera parte &middot; la tabla (10 min)</h4>
          <p>Con la escena en el modo de los tres sitios, rellenad en la libreta esta tabla para
             <b>vuestro</b> proyecto. Una fila por sitio:</p>
          <ul>
            <li><b>Wh que gasta al d&iacute;a</b>, y qu&eacute; porcentaje se lleva la placa.</li>
            <li><b>Wh que entran al d&iacute;a</b>, o el coste en euros si hay enchufe.</li>
            <li><b>D&iacute;as que aguanta</b> sin que vaya nadie.</li>
            <li><b>Veredicto</b>: sirve / no sirve, y por cu&aacute;l de las cinco preguntas falla.</li>
          </ul>
          <p>Despu&eacute;s repetid la fila del <b>huerto</b> marcando &laquo;la placa duerme&raquo;.
             &iquest;Cu&aacute;ntos d&iacute;as se ganan? &iquest;Llega ya a los treinta?</p>
          <h4>Segunda parte &middot; redise&ntilde;ar para el sitio donde no sirve (10 min)</h4>
          <p>Coged el sitio donde vuestro proyecto <b>suspende</b> y proponed una soluci&oacute;n que
             s&iacute; sirva all&iacute;. Vale cambiar de tecnolog&iacute;a entera. Tres pistas, una
             por proyecto:</p>
          <ul>
            <li><b>A &middot; riego</b>: una botella boca abajo con un gotero de barro riega todos los
                d&iacute;as, no gasta nada y no se estropea. &iquest;Qu&eacute; pierde frente al
                vuestro? Decidlo con honradez.</li>
            <li><b>B &middot; aviso de aula</b>: &iquest;hace falta un piloto encendido las veinticuatro
                horas, o basta con que se encienda cuando hay alguien? Calculad el ahorro.</li>
            <li><b>C &middot; l&aacute;mpara</b>: &iquest;y si en vez de una placa se usa un
                <b>interruptor crepuscular</b> de los que se venden hechos? Buscad qu&eacute; consume.</li>
          </ul>
          <p>Escribid vuestra propuesta en <b>cinco l&iacute;neas</b> y pasadle las <b>cinco
             preguntas del sitio</b>. Si suspende alguna, decidlo: es parte de la respuesta.</p>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>La tabla completa, con los tres sitios y sus n&uacute;meros <b>(3 puntos)</b>.</li>
            <li>El porcentaje que se lleva la placa, bien calculado <b>(1 punto)</b>.</li>
            <li>La fila con la placa dormida, y la conclusi&oacute;n <b>(1 punto)</b>.</li>
            <li>El redise&ntilde;o, con lo que gana <b>y lo que pierde</b> <b>(3 puntos)</b>.</li>
            <li>Las cinco preguntas aplicadas al redise&ntilde;o, sin maquillar <b>(2 puntos)</b>.</li>
          </ul>
''')

S2_CIERRE = u'''
      <ol>
      ''' + pregunta(u'La PlayPump ten&iacute;a dinero, premios y mil instalaciones. &iquest;Por '
                     u'qu&eacute; fall&oacute;?',
                     u'<p>Porque la cuenta no sal&iacute;a: para dar de beber a 2.500 personas '
                     u'hac&iacute;an falta entre 18 y 27 horas de giro al d&iacute;a, y un d&iacute;a '
                     u'tiene 24. Adem&aacute;s se romp&iacute;a y la pieza de repuesto no estaba al '
                     u'alcance de quien la usaba. <b>No fall&oacute; la financiaci&oacute;n: '
                     u'fall&oacute; el encaje con el sitio.</b></p>') + pregunta(
          u'Define tecnolog&iacute;a apropiada sin usar la palabra &laquo;sencillo&raquo;.',
          u'<p>La que <b>encaja con el sitio donde va a vivir</b>: con la energ&iacute;a que hay '
          u'all&iacute;, los materiales que se consiguen all&iacute;, las manos que la van a manejar y '
          u'el dinero que hay para arreglarla. Puede ser electr&oacute;nica y complicada: lo que la '
          u'hace apropiada no es lo que lleva dentro, es la <b>relaci&oacute;n</b> con el sitio.</p>')\
    + pregunta(
          u'En el riego autom&aacute;tico, &iquest;qu&eacute; se lleva casi toda la energ&iacute;a, '
          u'la bomba o la placa? &iquest;Por qu&eacute;?',
          u'<p><b>La placa</b>, y con mucha diferencia. La bomba trabaja cuarenta segundos al '
          u'd&iacute;a; la placa est&aacute; despierta 24 horas gastando 45 mA. Son 5,4 Wh contra '
          u'unas cent&eacute;simas. En un aparato que espera casi todo el rato, <b>el consumo de '
          u'esperar es el consumo</b>.</p>') + pregunta(
          u'Una de las cinco preguntas del sitio no va de t&eacute;cnica. &iquest;Cu&aacute;l, y por '
          u'qu&eacute; est&aacute; ah&iacute;?',
          u'<p>La quinta: <b>&iquest;qui&eacute;n decidi&oacute; que este era el problema?</b> '
          u'Est&aacute; ah&iacute; porque un aparato perfecto que resuelve un problema que nadie '
          u'ten&iacute;a sigue sin servir para nada, y eso no se arregla mejorando el aparato. Es '
          u'la pregunta con la que se abri&oacute; la unidad.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya sabes si tu aparato sirve, d&oacute;nde y a qui&eacute;n. Ahora hay que conseguir que se
        entere alguien que <b>no estaba</b>: seis minutos, tres personas que no han visto nada del
        curso, y una que te va a hacer la pregunta que menos te apetece. La buena noticia es que
        vas a tener <b>la r&uacute;brica por adelantado</b>. La mala es que en cuanto la veas
        te vas a dar cuenta de que el gui&oacute;n que ten&iacute;as pensado suspende.
      </div>
'''


# ==========================================================================
# SESION 3 - Presentar y defender
# ==========================================================================
S3_RETO = u'''
      <p>El d&iacute;a de la defensa hay tres personas sentadas delante que <b>no estaban</b>: no os
         han visto pelearos con el sensor, no saben lo que cost&oacute; que la bomba no se ahogara y
         no tienen ning&uacute;n motivo para ser amables. Ten&eacute;is <b>seis minutos</b>.</p>
      <div class="aviso">
        <span class="n-tag">El encargo</span>
        En pareja y en <b>tres minutos</b>: escribid el gui&oacute;n de esos seis minutos. Solo el
        reparto, con los segundos al lado de cada parte. Sin pensarlo mucho, tal y como lo
        har&iacute;ais si fuera ma&ntilde;ana.
      </div>
      <p>Casi todos los guiones salen parecidos, y se parecen a este:</p>
''' + foto('c9-defensa.jpg',
           u'Un alumno con uniforme de pie detr&aacute;s de una maqueta muy elaborada con monta&ntilde;as, '
           u'aerogeneradores, un r&iacute;o y camiones, y un panel con textos detr&aacute;s',
           u'Una feria de ciencia en la <b>escuela de Niv&iacute;n (Per&uacute;)</b>, en 2018. '
           u'M&iacute;rala un momento antes de seguir: la maqueta es <b>impresionante</b>, y ha '
           u'costado much&iacute;simas horas. Ahora la pregunta inc&oacute;moda, que no va contra '
           u'&eacute;l sino contra todos nosotros: si tuviera seis minutos, &iquest;de qu&eacute; '
           u'crees que hablar&iacute;a m&aacute;s, de la maqueta o de a qui&eacute;n le sirve? '
           u'&iquest;Y t&uacute;?',
           u'Escuela de Niv&iacute;n', u'CC BY-SA 4.0',
           u'https://commons.wikimedia.org/wiki/File:Niv%C3%ADn._Alumno_presenta_una_maqueta_de_'
           u'granja_sostenible.jpg') + u'''
      <div class="reto-piensa">
        <span class="n-tag">Comparad</span>
        <p>Mirad vuestro gui&oacute;n y sumad los segundos que le hab&eacute;is dado a
           <b>c&oacute;mo lo montamos</b>. Despu&eacute;s sumad los que le hab&eacute;is dado a
           <b>a qui&eacute;n le sirve</b> y a <b>qu&eacute; hemos medido</b>. Si la primera cifra es
           mayor que la suma de las otras dos, no pasa nada: le pasa a casi todo el mundo, y hoy vamos
           a ver exactamente cu&aacute;nto cuesta en puntos.</p>
      </div>
'''

S3_TEORIA = u'''
      <p>Lo primero, la r&uacute;brica. La ten&eacute;is <b>antes</b> de preparar la defensa, a
         prop&oacute;sito: una r&uacute;brica que se ense&ntilde;a despu&eacute;s no sirve para
         aprender, sirve para justificar una nota.</p>
      <p>Poned el gui&oacute;n de siempre, mirad la nota, y despu&eacute;s pulsad el otro
         bot&oacute;n. Es el <b>mismo proyecto</b> y los <b>mismos seis minutos</b>.</p>
''' + RUBRICA + u'''
      <div class="copiar">
        <h4>Lo que acaba de pasar</h4>
        <p>El gui&oacute;n de siempre saca <b>4,17</b>. El reparto por peso saca <b>9,67</b>. No ha
           cambiado el proyecto, ni el aparato, ni el tiempo: ha cambiado <b>d&oacute;nde se gastan
           los segundos</b>. Son <b>cinco puntos y medio</b> de diferencia por decidir mal en
           qu&eacute; gastar trescientos sesenta segundos.</p>
        <p>Y la raz&oacute;n es aritm&eacute;tica, no est&eacute;tica: <b>6,5 de los 10 puntos</b>
           son de lo que el aparato hace por alguien, y <b>cero</b> de c&oacute;mo lo montasteis. No
           porque montarlo no tenga m&eacute;rito, sino porque de eso va la unidad 2 y esto es la 9.</p>
      </div>
      <div class="copiar">
        <h4>El orden que funciona, y por qu&eacute; ese</h4>
        <ol>
          <li><b>El problema y de qui&eacute;n es</b> (~1 min). Qui&eacute;n lo sufre, d&oacute;nde y
              c&oacute;mo lo sab&eacute;is. Si en los primeros treinta segundos no se ha dicho a
              qui&eacute;n le sirve, el jurado ya est&aacute; pensando en otra cosa.</li>
          <li><b>Qu&eacute; hace el aparato</b> (~1 min). En una frase, y ense&ntilde;&aacute;ndolo.</li>
          <li><b>La prueba de que funciona</b> (~1 min). Encendedlo. Si hay riesgo de que falle,
              llevad un v&iacute;deo de veinte segundos <b>grabado</b>. Un fallo en directo no baja
              la nota; quedarse sin ense&ntilde;ar nada, s&iacute;.</li>
          <li><b>El impacto, con la cuenta delante</b> (~1,5 min). Litros, vatios-hora o euros, con
              las unidades y con de d&oacute;nde sale cada n&uacute;mero.</li>
          <li><b>Lo que falla y qu&eacute; har&iacute;ais</b> (~1 min). El fallo de verdad, no uno de
              adorno. Esto <b>sube</b> la nota: dice que hab&eacute;is mirado vuestro propio trabajo
              con ojo cr&iacute;tico.</li>
          <li><b>Las preguntas</b> (~0,5 min de vuestra parte).</li>
        </ol>
        <p>Fíjate en que <b>&laquo;c&oacute;mo lo montamos&raquo; no aparece</b>. Si preguntan, se
           cuenta; si no, se queda en la memoria escrita, que es donde le toca.</p>
      </div>

      <h3>La pregunta inc&oacute;moda</h3>
      <p>Va a haber una. No es para pillaros: es para ver si distingu&iacute;s lo que hab&eacute;is
         medido de lo que os hab&eacute;is cre&iacute;do. Se contesta con cuatro movimientos, en este
         orden.</p>
      <div class="copiar">
        <h4>C&oacute;mo se contesta lo que no te apetece que te pregunten</h4>
        <ol>
          <li><b>Repite la pregunta</b> con tus palabras. Ganas cinco segundos y compruebas que la has
              entendido. Si no la has entendido, preg&uacute;ntalo: no es una derrota.</li>
          <li><b>Separa lo que sabes de lo que supones.</b> &laquo;Medimos esto; aquello lo estamos
              suponiendo.&raquo;</li>
          <li><b>Da el dato si lo tienes.</b> Y si no lo tienes, di <b>&laquo;no lo hemos
              medido&raquo;</b>. Esas cuatro palabras suman puntos. Un n&uacute;mero inventado los
              quita todos, y se nota siempre, porque la siguiente pregunta es de d&oacute;nde sale.</li>
          <li><b>Di c&oacute;mo lo averiguar&iacute;as.</b> &laquo;Para saberlo habr&iacute;a que
              medir X durante Y d&iacute;as.&raquo; Esto convierte un agujero en un plan.</li>
        </ol>
        <p>Lo &uacute;nico que no se hace <b>nunca</b>: inventarse un n&uacute;mero.</p>
      </div>
      <div class="copiar">
        <h4>Las cinco que van a caer</h4>
        <ul>
          <li><i>&laquo;Se va la luz una semana en Navidad. &iquest;Qu&eacute; pasa con la
              planta?&raquo;</i> &mdash; proyecto <b>A</b>.</li>
          <li><i>&laquo;Vuestro piloto dice que hay que ventilar y fuera hace cuatro grados.
              &iquest;Qui&eacute;n decide, el aparato o el profesor? &iquest;Y si nadie hace
              caso?&raquo;</i> &mdash; proyecto <b>B</b>.</li>
          <li><i>&laquo;&iquest;Cu&aacute;nto ha costado fabricarlo y cu&aacute;nto ahorra al
              a&ntilde;o?&raquo;</i> &mdash; proyecto <b>C</b>, y esa es la sesi&oacute;n que viene.</li>
          <li><i>&laquo;&iquest;Qui&eacute;n lo arregla cuando vosotros acab&eacute;is 4.&ordm;?&raquo;</i>
              &mdash; los tres.</li>
          <li><i>&laquo;&iquest;Lo hab&eacute;is probado con alguien que no se&aacute;is
              vosotros?&raquo;</i> &mdash; los tres, y es la que m&aacute;s duele.</li>
        </ul>
        <p>Llevadlas contestadas por escrito. No para leerlas: para no estrenaros delante del jurado.</p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>La regla que usa la escena para enlazar tiempo y nivel &mdash;diez segundos para nombrar
           algo, veinticinco para explicarlo, cuarenta y cinco para demostrarlo con un dato&mdash;
           <b>es criterio nuestro</b>, no viene en ning&uacute;n sitio oficial. Est&aacute; puesta para
           que se vea una cosa que de otra manera no se ve: <b>dedicarle cinco segundos a algo es
           exactamente igual que no dedic&aacute;rselos</b>. En la r&uacute;brica no hay medio punto
           por mencionar. Lo que se mide es lo que se demuestra.</p>
      </div>
'''

S3_PRACTICA = ficha(
    u'Actividad 3 &middot; Ensayo cruzado, con la r&uacute;brica en la mano',
    [u'2.1', u'6.3', u'A.2', u'D.4'], u'Dos grupos &middot; 20 min', u'''
          <h4>Antes de empezar (4 min)</h4>
          <p>Cada grupo reparte sus seis minutos con la escena de arriba y anota
             <b>la nota que espera sacar</b>. Ese n&uacute;mero se escribe y se tapa.</p>
          <h4>Primera ronda (8 min)</h4>
          <ol class="pasos">
            <li>El grupo A defiende. <b>Seis minutos y se corta</b>: alguien cronometra de verdad.</li>
            <li>El grupo B puntúa con la r&uacute;brica, fila por fila, poniendo el nivel 0-3 de cada
                una. Sin hablar entre ellos hasta el final.</li>
            <li>El grupo B hace <b>dos preguntas de la lista</b> y <b>una propia</b>. La propia tiene
                que ser sobre algo que no se haya contado.</li>
          </ol>
          <h4>Segunda ronda (8 min)</h4>
          <p>Al rev&eacute;s. Y al terminar, las dos cosas que de verdad ense&ntilde;an:</p>
          <ul>
            <li>Comparad <b>la nota que esper&aacute;bais</b> con <b>la que os ha puesto el otro
                grupo</b>. Anotad la diferencia y, sobre todo, <b>en qu&eacute; fila</b> est&aacute;
                la mayor discrepancia. Casi siempre es la misma: la del impacto.</li>
            <li>Escribid la pregunta que peor hab&eacute;is contestado y, con los cuatro movimientos
                delante, <b>la respuesta que deber&iacute;ais haber dado</b>.</li>
          </ul>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>El reparto de los seis minutos, escrito y razonado <b>(2 puntos)</b>.</li>
            <li>La defensa cabe en el tiempo sin que la corten <b>(1 punto)</b>.</li>
            <li>La r&uacute;brica del otro grupo, rellenada entera y con criterio <b>(2 puntos)</b>.</li>
            <li>La pregunta propia se&ntilde;ala un agujero de verdad <b>(2 puntos)</b>.</li>
            <li>La discrepancia entre las dos notas, con la fila se&ntilde;alada <b>(1 punto)</b>.</li>
            <li>La respuesta reescrita usa los cuatro movimientos y no inventa ning&uacute;n
                n&uacute;mero <b>(2 puntos)</b>.</li>
          </ul>
''')

S3_CIERRE = u'''
      <ol>
      ''' + pregunta(u'&iquest;Por qu&eacute; el mismo proyecto saca 4,17 con un gui&oacute;n y 9,67 '
                     u'con otro?',
                     u'<p>Porque los seis minutos son los mismos pero los puntos no est&aacute;n '
                     u'repartidos igual: <b>6,5 de 10</b> son del problema, la medida, el impacto y '
                     u'lo que falla, y <b>0</b> de c&oacute;mo se mont&oacute;. Gastar cuatro minutos '
                     u'en la parte que vale cero deja sin tiempo a las que valen.</p>') + pregunta(
          u'Te preguntan un dato que no hab&eacute;is medido. &iquest;Qu&eacute; contestas?',
          u'<p><b>&laquo;No lo hemos medido&raquo;</b>, y a continuaci&oacute;n c&oacute;mo lo '
          u'averiguar&iacute;ais: qu&eacute; medir&iacute;ais, con qu&eacute; y durante cu&aacute;nto '
          u'tiempo. Eso convierte un agujero en un plan y suma. Inventarse un n&uacute;mero resta '
          u'todo, porque la siguiente pregunta siempre es de d&oacute;nde sale.</p>') + pregunta(
          u'&iquest;Por qu&eacute; contar lo que falla <b>sube</b> la nota en vez de bajarla?',
          u'<p>Porque lo que se eval&uacute;a no es que el aparato sea perfecto &mdash;no lo es '
          u'ninguno&mdash;, sino que sep&aacute;is mirarlo con ojo cr&iacute;tico y proponer la '
          u'mejora. Es un criterio entero, el 6.3, y vale 1,5 puntos. Ocultar el fallo no lo hace '
          u'desaparecer: lo deja para que lo encuentre el jurado.</p>') + pregunta(
          u'&iquest;Qu&eacute; pasa si el aparato se estropea justo delante del jurado?',
          u'<p>Casi nada, si lo hab&eacute;is previsto: se ense&ntilde;a el v&iacute;deo de veinte '
          u'segundos que lleváis grabado y se dice qu&eacute; ha fallado. Lo que s&iacute; baja la '
          u'nota es <b>quedarse sin ense&ntilde;ar nada</b>, porque ese indicador vale 2 puntos y sin '
          u'prueba se queda en cero.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Queda una pregunta de la lista sin contestar, y es la peor: <b>&iquest;cu&aacute;nto ha
        costado fabricarlo y cu&aacute;nto ahorra al a&ntilde;o?</b> Porque vuestro aparato ahorra
        algo, s&iacute;. Pero fabricarlo tambi&eacute;n cost&oacute; algo, y eso ya est&aacute;
        gastado desde el primer d&iacute;a. La sesi&oacute;n que viene hacemos esa divisi&oacute;n, y
        aviso de que <b>no sale bien</b>.
      </div>
'''


# ==========================================================================
# SESION 4 - Lo que queda
# ==========================================================================
S4_RETO = u'''
      <p>&Uacute;ltima sesi&oacute;n del curso, y empieza con la pregunta que se qued&oacute; colgando.</p>
      <div class="aviso">
        <span class="n-tag">El encargo</span>
        Vuestra l&aacute;mpara autom&aacute;tica apaga la luz cuando no hace falta, o sea que
        <b>ahorra</b>. Fabricarla cost&oacute; unos 25 &euro; de material.
        <b>&iquest;Cu&aacute;ntos a&ntilde;os tarda en devolver lo que cost&oacute;?</b>
        Cinco minutos, con calculadora.
      </div>
      <p>Para hacerla hacen falta tres cosas, y las tres las ten&eacute;is: lo que gasta una bombilla
         LED (unos <b>9 W</b>), las horas que se quedaba encendida de m&aacute;s (pongamos <b>hora y
         media al d&iacute;a</b>) y lo que cuesta el kilovatio hora (del orden de <b>0,15 &euro;</b>).</p>
      <div class="reto-piensa">
        <span class="n-tag">Y una cuarta cosa, que casi nadie mete</span>
        <p>La placa que decide cu&aacute;ndo apagar <b>tambi&eacute;n gasta</b>, y gasta las
           veinticuatro horas. Son 45 mA a 5 V. Calcula cu&aacute;ntos vatios-hora al d&iacute;a son y
           <b>r&eacute;stalos</b> del ahorro antes de dividir. La cifra que sale sorprende a todo el
           mundo.</p>
      </div>
'''

S4_TEORIA = u'''
      <p>La cuenta es esta, y no tiene m&aacute;s misterio:</p>
      <div class="copiar">
        <h4>Cu&aacute;ndo devuelve lo que cost&oacute;</h4>
        <p>Un aparato empieza su vida <b>en n&uacute;meros rojos</b>: lo que cost&oacute; hacerlo ya
           est&aacute; gastado el primer d&iacute;a. A partir de ah&iacute;, cada a&ntilde;o descuenta
           lo que ahorra.</p>
        <p style="font-family:var(--f-m);font-size:14px">saldo(t) =
           ahorro al a&ntilde;o &times; t &minus; lo que cost&oacute;</p>
        <p style="font-family:var(--f-m);font-size:14px">a&ntilde;os en devolverlo =
           lo que cost&oacute; &divide; ahorro al a&ntilde;o</p>
        <p>Y despu&eacute;s, la comparaci&oacute;n que casi nadie hace:</p>
        <p><b>Si tarda m&aacute;s en devolverlo de lo que dura antes de romperse, no lo devuelve
           nunca.</b> Por muy bien que funcione.</p>
      </div>
      <p>Aqu&iacute; est&aacute;n los tres proyectos del curso con esa cuenta hecha. Empieza por la
         <b>C</b>, que es la del reto, y despu&eacute;s mira las otras dos.</p>
''' + RETORNO + u'''
      <div class="copiar">
        <h4>Tres resultados inc&oacute;modos, y los tres son verdad</h4>
        <ul>
          <li><b>C &middot; la l&aacute;mpara.</b> Con una bombilla LED de 9 W, el ahorro neto es de
              menos de medio euro al a&ntilde;o, porque la placa se come <b>el 40 %</b> de lo que
              ahorra. Con esos n&uacute;meros no lo devuelve <b>jam&aacute;s</b>. Pero pon la misma
              l&aacute;mpara donde hay un hal&oacute;geno de 50 W encendido seis horas de m&aacute;s,
              y lo devuelve en <b>menos de seis a&ntilde;os</b>. El aparato es el mismo: cambia
              d&oacute;nde est&aacute; el desperdicio.</li>
          <li><b>A &middot; el riego.</b> Ahorra unos <b>490 litros de agua al a&ntilde;o</b> por
              planta, que est&aacute; muy bien. En euros son menos de un euro, porque en Espa&ntilde;a
              el agua es barata; y la placa se gasta un tercio de eso en electricidad. <b>En litros
              s&iacute; ahorra; en euros casi no.</b> Las dos frases son ciertas y no se contradicen:
              es que <b>el precio de una cosa no mide lo que vale</b>.</li>
          <li><b>B &middot; el aviso de ventilaci&oacute;n.</b> Este da <b>n&uacute;meros rojos a
              prop&oacute;sito</b>. Ventilar cuesta calefacci&oacute;n: cada renovaci&oacute;n
              completa del aire de un aula en invierno son <b>0,75 kWh</b>, y cuatro al d&iacute;a
              durante el curso pasan de <b>500 kWh</b>. Lo que se gana a cambio es aire respirable,
              y eso <b>no se mide en euros</b>.</li>
        </ul>
      </div>
      <div class="copiar">
        <h4>Dos reglas que se llevan de aqu&iacute;</h4>
        <ol>
          <li><b>Hay impactos que no se pueden sumar.</b> Litros, kilovatios hora, euros y horas de
              aire limpio son unidades distintas. Se pueden poner una al lado de otra; no se pueden
              sumar. Quien las suma en un solo n&uacute;mero est&aacute; eligiendo, en secreto,
              cu&aacute;nto vale cada una.</li>
          <li><b>El impacto depende de la escala y del sitio.</b> Un aparato que no se amortiza en
              una l&aacute;mpara se amortiza en treinta aulas, y uno que no ahorra euros en
              Espa&ntilde;a puede ahorrar agua decisiva en otro sitio. Es la misma idea de la
              sesi&oacute;n 2, ahora con la calculadora delante.</li>
        </ol>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Hay una parte de la cuenta que <b>no est&aacute; hecha</b>, y prefiero dec&iacute;rosla a
           que la descubráis vosotros: la <b>energ&iacute;a y los minerales que cost&oacute;
           fabricar</b> la placa, el sensor y los cables. Eso tambi&eacute;n est&aacute; gastado el
           primer d&iacute;a y no aparece en ning&uacute;n sitio de la escena.</p>
        <p>No lo he metido porque <b>no tengo un n&uacute;mero fiable</b> para un Arduino, y meter una
           cifra inventada en una cuenta la estropea entera. Lo que s&iacute; se puede afirmar sin
           riesgo es la <b>direcci&oacute;n</b>: si se contara, el tiempo de retorno ser&iacute;a
           m&aacute;s largo, nunca m&aacute;s corto. Esto tiene nombre &mdash;<b>an&aacute;lisis de
           ciclo de vida</b>&mdash; y es una carrera entera.</p>
      </div>
''' + video('video-c9-acv', 'sC1HmzxOjoQ',
            u'An&aacute;lisis de ciclo de vida: definici&oacute;n de objetivos y alcance',
            u'Canal: Universitat Polit&egrave;cnica de Val&egrave;ncia',
            u'Un v&iacute;deo universitario, m&aacute;s seco que los otros, sobre c&oacute;mo se hace '
            u'de verdad la cuenta que aqu&iacute; hemos dejado a medias.') + u'''

      <h3>Lo que queda del curso</h3>
      <div class="copiar">
        <h4>Las seis cosas del curso, en cristiano</h4>
        <ol>
          <li><b>Mirar y encontrar el problema</b> antes de ponerse a construir nada.</li>
          <li><b>Fabricarlo de verdad</b>, con material y herramienta reales, y sin hacerse da&ntilde;o.</li>
          <li><b>Cont&aacute;rselo a alguien</b> que no estaba, en su idioma y en su tiempo.</li>
          <li><b>Automatizarlo</b>: sensor, umbral, actuador, y un programa que no miente.</li>
          <li><b>Usar las herramientas digitales</b> para simularlo antes de romper nada.</li>
          <li><b>Medir lo que le cuesta al planeta</b>, incluido lo que cuesta el propio aparato.</li>
        </ol>
        <p>Si dentro de diez a&ntilde;os solo te queda una, que sea esta: <b>antes de preguntar si
           funciona, pregunta a qui&eacute;n le sirve y qui&eacute;n eligi&oacute; el problema</b>.</p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p><b>Lo que no cab&iacute;a.</b> Este curso se ha quedado fuera bastante, y conviene saber
           qu&eacute;: el an&aacute;lisis de ciclo de vida hecho en serio, la accesibilidad (dise&ntilde;ar
           para quien no ve, no oye o no puede apretar un bot&oacute;n), el residuo electr&oacute;nico y
           d&oacute;nde acaba, y el derecho a reparar. Cuatro cosas que dan para un curso entero
           cada una.</p>
      </div>
''' + foto('c9-repair-cafe.jpg',
           u'Vista desde arriba de un local con mesas largas donde varias personas reparan una '
           u'l&aacute;mpara y un aspirador con destornilladores y un polímetro',
           u'Un <b>repair caf&eacute;</b>: gente que se junta un s&aacute;bado con sus herramientas '
           u'para arreglar lo que se ha estropeado, en vez de tirarlo. F&iacute;jate en la mesa: '
           u'destornilladores, alicates, un polímetro y una regleta. Es <b>exactamente</b> lo que '
           u'ten&eacute;is en el taller. Un aparato que se puede abrir y arreglar dura m&aacute;s, y '
           u'eso cambia el resultado de la cuenta de arriba <b>m&aacute;s que cualquier mejora del '
           u'dise&ntilde;o</b>: duplicar la vida es duplicar el ahorro sin fabricar nada nuevo.',
           u'Ilvy Njiokiktjien', u'CC BY-SA 3.0',
           u'https://commons.wikimedia.org/wiki/File:Repair_Cafe_by_Ilvy_Njiokiktjien.jpg') + u'''
      <div class="copiar">
        <h4>Por d&oacute;nde se sigue, si esto te ha gustado</h4>
        <ul>
          <li><b>En el instituto</b>: Tecnolog&iacute;a e Ingenier&iacute;a en 1.&ordm; y 2.&ordm; de
              Bachillerato, y Dibujo T&eacute;cnico si lo tuyo ha sido el plano.</li>
          <li><b>En Formaci&oacute;n Profesional</b>: electr&oacute;nica, mecatr&oacute;nica,
              instalaciones, energ&iacute;as renovables, fabricaci&oacute;n. Grado medio y superior,
              y se entra desde aqu&iacute;.</li>
          <li><b>Por tu cuenta, y gratis</b>: Tinkercad sigue siendo gratis cuando acabe el curso, y
              una placa cuesta lo que dos pizzas. Lo que hab&eacute;is aprendido a programar no
              caduca.</li>
          <li><b>Con otros</b>: un repair caf&eacute;, un club de robótica, el huerto del barrio. Lo
              que m&aacute;s ense&ntilde;a de todo esto es arreglar algo de alguien.</li>
        </ul>
      </div>
'''

S4_PRACTICA = ficha(
    u'Actividad 4 &middot; La ficha de impacto de vuestro proyecto',
    [u'6.2', u'6.3', u'D.2', u'D.3', u'D.4'], u'Grupos de tres &middot; 15 min', u'''
          <h4>La ficha (10 min)</h4>
          <p>Una hoja, para vuestro proyecto, con estos seis apartados. Va a la memoria y se usa en la
             defensa:</p>
          <ol class="pasos">
            <li><b>Lo que ahorra, en su unidad propia</b> (litros, Wh o kWh), al a&ntilde;o. Con la
                cuenta escrita, no solo el resultado.</li>
            <li><b>Lo mismo en euros</b>, y el precio que hab&eacute;is usado para convertirlo.</li>
            <li><b>Lo que gasta el propio aparato</b>, restado ya. Si no lo rest&aacute;is, el
                n&uacute;mero de arriba est&aacute; mal.</li>
            <li><b>Lo que cost&oacute;</b> y <b>los a&ntilde;os en devolverlo</b>. Si no lo devuelve
                nunca, se escribe &laquo;nunca&raquo;: es un resultado, no un suspenso.</li>
            <li><b>Un impacto que no cabe en euros</b>, dicho con su unidad propia: personas, horas,
                plantas vivas, grados. Y por qu&eacute; no se puede sumar a lo anterior.</li>
            <li><b>Lo que NO hab&eacute;is contado</b> y sab&eacute;is que existe. Como m&iacute;nimo,
                lo que cost&oacute; fabricar la placa.</li>
          </ol>
          <h4>Y la pregunta del curso (5 min)</h4>
          <p>Debajo de la ficha, cuatro l&iacute;neas contestando a esto, que es con lo que se abri&oacute;
             la unidad:</p>
          <p><b>&iquest;A qui&eacute;n le sirve de verdad vuestro aparato, y qui&eacute;n decidi&oacute;
             que ese era el problema que hab&iacute;a que resolver?</b> Si la respuesta es
             &laquo;lo eligi&oacute; el profesor&raquo;, escribidlo: es la verdad, y a partir de
             ah&iacute; decid <b>qu&eacute; problema habr&iacute;ais elegido vosotros</b> y a
             qui&eacute;n se lo habr&iacute;ais preguntado antes.</p>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>El ahorro en su unidad, con la cuenta entera y las unidades <b>(2 puntos)</b>.</li>
            <li>El consumo del propio aparato, restado <b>(2 puntos)</b>.</li>
            <li>Los a&ntilde;os en devolverlo, comparados con lo que dura <b>(2 puntos)</b>.</li>
            <li>El impacto que no cabe en euros, con su unidad <b>(2 puntos)</b>.</li>
            <li>La respuesta a la pregunta del curso, sin frases hechas <b>(2 puntos)</b>.</li>
          </ul>
''')

PREGUNTAS_TEST = [
    dict(p=u'Entre 1975 y 1999 salieron 1.393 medicamentos nuevos. &iquest;Cu&aacute;ntos eran para '
           u'enfermedades tropicales y tuberculosis?',
         op=[u'Unos 300, alrededor de la quinta parte.', u'16.', u'Ninguno.'],
         ok=1,
         por=u'16 de 1.393, el 1,1 %, seg&uacute;n Trouiller y otros en <i>The Lancet</i> (2002). No '
             u'hay ninguna ley que lo impida: sale de una divisi&oacute;n.'),
    dict(p=u'&iquest;Qu&eacute; es la <b>demanda solvente</b>?',
         op=[u'La cantidad de gente que sufre un problema.',
             u'La gente que sufre un problema <b>y puede pagar</b> por quit&aacute;rselo.',
             u'El dinero que el Estado dedica a un problema.'],
         ok=1,
         por=u'Un mercado no cuenta personas: cuenta euros. Cien millones de personas sin un euro no '
             u'son un mercado; dos millones que pueden pagar, s&iacute;.'),
    dict(p=u'La cuenta que decide si algo se fabrica compara el precio m&iacute;nimo con&hellip;',
         op=[u'lo que cuesta fabricar cada unidad',
             u'lo que puede pagar quien sufre el problema',
             u'lo que cobra la competencia'],
         ok=1,
         por=u'Precio m&iacute;nimo = coste de desarrollo &divide; (personas que lo comprar&aacute;n '
             u'&times; a&ntilde;os de venta). Si no cabe en lo que puede pagar quien lo sufre, no se '
             u'fabrica, y nadie ha tenido que decidirlo.'),
    dict(p=u'Un medidor de CO<sub>2</sub> de aula existe y cuesta unos 120 &euro;. &iquest;Cu&aacute;l '
           u'es la raz&oacute;n principal de que no haya uno en cada clase?',
         op=[u'Que la tecnolog&iacute;a todav&iacute;a no est&aacute; madura.',
             u'Que quien sufre el problema no es quien compra ni quien decide.',
             u'Que consumen demasiada electricidad.'],
         ok=1,
         por=u'El alumno que aguanta el aula cargada no compra nada y no est&aacute; en la mesa donde '
             u'se decide. Cuando el que elige, el que paga y el que sufre son tres personas '
             u'distintas, lo que se compra es peor.'),
    dict(p=u'La PlayPump promet&iacute;a dar agua a 2.500 personas y sub&iacute;a 1.400 litros por '
           u'hora. Con 10 litros por persona y d&iacute;a, &iquest;cu&aacute;ntas horas de giro hacen '
           u'falta al d&iacute;a?',
         op=[u'Unas 2 horas.', u'Unas 18 horas.', u'Unas 6 horas.'],
         ok=1,
         por=u'2.500 &times; 10 = 25.000 litros al d&iacute;a; 25.000 &divide; 1.400 = 17,9 horas. Con '
             u'el caudal medido de verdad sub&iacute;a a 27, y un d&iacute;a tiene 24.'),
    dict(p=u'&iquest;Qu&eacute; quiere decir que una tecnolog&iacute;a sea <b>apropiada</b>?',
         op=[u'Que es lo m&aacute;s sencilla posible, sin electr&oacute;nica.',
             u'Que encaja con la energ&iacute;a, los materiales, las manos y el dinero del sitio '
             u'donde va a vivir.',
             u'Que ha pasado los controles de calidad.'],
         ok=1,
         por=u'Apropiada no es una categor&iacute;a del aparato, es una <b>relaci&oacute;n</b> entre '
             u'el aparato y el sitio. Un Arduino es apropiado en vuestro taller y puede no serlo en '
             u'un huerto sin enchufe.'),
    dict(p=u'En el riego autom&aacute;tico a pilas, &iquest;qu&eacute; se lleva casi toda la '
           u'energ&iacute;a?',
         op=[u'La bomba, que mueve agua.',
             u'La placa, que est&aacute; despierta las 24 horas sin hacer nada.',
             u'El sensor de humedad.'],
         ok=1,
         por=u'La bomba trabaja 40 segundos al d&iacute;a: cent&eacute;simas de vatio hora. La placa '
             u'gasta 45 mA durante 24 horas: 5,4 Wh. En un aparato que espera casi siempre, el '
             u'consumo de esperar <b>es</b> el consumo.'),
    dict(p=u'En la r&uacute;brica de la defensa, &iquest;cu&aacute;nto vale &laquo;c&oacute;mo lo '
           u'montamos, paso a paso&raquo;?',
         op=[u'Es lo que m&aacute;s vale: 3 puntos.', u'Vale 1 punto.', u'Vale 0.'],
         ok=2,
         por=u'Cero, y por eso el gui&oacute;n de siempre saca 4,17 mientras el reparto por peso saca '
             u'9,67 con el mismo proyecto y los mismos seis minutos. Montarlo se eval&uacute;a, pero '
             u'en otra unidad y con la memoria escrita.'),
    dict(p=u'Os preguntan un dato que no hab&eacute;is medido. &iquest;Qu&eacute; es lo mejor que '
           u'pod&eacute;is hacer?',
         op=[u'Dar una cifra aproximada para no quedarse callado.',
             u'Decir &laquo;no lo hemos medido&raquo; y explicar c&oacute;mo lo averiguar&iacute;ais.',
             u'Cambiar de tema y seguir con lo siguiente.'],
         ok=1,
         por=u'Esas cuatro palabras suman: distinguen lo medido de lo supuesto. Un n&uacute;mero '
             u'inventado lo quita todo, porque la siguiente pregunta siempre es de d&oacute;nde sale.'),
    dict(p=u'Un aparato tarda 40 a&ntilde;os en devolver lo que cost&oacute; y se rompe a los 4. '
           u'&iquest;Qu&eacute; significa eso?',
         op=[u'Que hay que esperar m&aacute;s tiempo.',
             u'Que no lo devuelve nunca: se rompe mucho antes de llegar al cero.',
             u'Que la cuenta est&aacute; mal hecha.'],
         ok=1,
         por=u'Si el tiempo de retorno pasa de la vida del aparato, el saldo nunca llega a cero. Eso '
             u'no lo invalida como proyecto escolar, pero s&iacute; invalida el argumento de que '
             u'ahorra dinero. Se dice, y se buscan las unidades en las que s&iacute; ahorra.'),
]

S4_CIERRE = u'''
      <ol>
      ''' + pregunta(u'&iquest;Por qu&eacute; el aviso de ventilaci&oacute;n da n&uacute;meros rojos '
                     u'y aun as&iacute; puede ser buen proyecto?',
                     u'<p>Porque ventilar <b>cuesta</b> calefacci&oacute;n: cada renovaci&oacute;n de '
                     u'un aula en invierno son unos 0,75 kWh, y el curso entero pasa de 500. Lo que '
                     u'da a cambio es aire respirable, y eso <b>no se mide en euros</b>. Los dos '
                     u'impactos son reales y est&aacute;n en unidades distintas: no se pueden sumar, '
                     u'hay que ponerlos uno al lado del otro y decidir.</p>') + pregunta(
          u'La misma l&aacute;mpara autom&aacute;tica no se amortiza nunca en un sitio y se amortiza '
          u'en cinco a&ntilde;os en otro. &iquest;C&oacute;mo puede ser?',
          u'<p>Porque lo que se ahorra no depende del aparato, depende <b>del desperdicio que '
          u'corrige</b>. Sobre una bombilla LED de 9 W apenas hay nada que ahorrar; sobre un '
          u'hal&oacute;geno de 50 W encendido seis horas de m&aacute;s, hay mucho. Es la '
          u'tecnolog&iacute;a apropiada de la sesi&oacute;n 2, ahora con la calculadora.</p>')\
    + pregunta(
          u'&iquest;Qu&eacute; parte de la cuenta del retorno hemos dejado sin hacer, y por qu&eacute;?',
          u'<p>La <b>energ&iacute;a y los materiales que cost&oacute; fabricar</b> la placa y los '
          u'componentes, que ya est&aacute;n gastados el primer d&iacute;a. No se ha hecho porque no '
          u'tenemos un n&uacute;mero fiable, y meter una cifra inventada estropea toda la cuenta. Lo '
          u'que s&iacute; se puede afirmar es la direcci&oacute;n: el retorno ser&iacute;a '
          u'<b>m&aacute;s largo</b>, nunca m&aacute;s corto.</p>') + pregunta(
          u'La pregunta con la que empez&oacute; la unidad: tu aparato funciona y casi no contamina. '
          u'&iquest;Qu&eacute; falta por preguntar?',
          u'<p><b>A qui&eacute;n le sirve de verdad</b> y <b>qui&eacute;n decidi&oacute; que ese era '
          u'el problema</b>. Son las dos preguntas que no se arreglan mejorando el aparato, y las '
          u'&uacute;nicas que siguen valiendo cuando la tecnolog&iacute;a que has aprendido este '
          u'curso se haya quedado vieja.</p>') + u'''
      </ol>
''' + test('c9', u'Lo que tiene que haber quedado de estas cuatro sesiones', PREGUNTAS_TEST) + u'''
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Estas cuatro sesiones os han dado la mirada y las cuentas. Las cuatro que quedan son
        <b>manos</b>: el ciclo de vida completo del aparato, dise&ntilde;arlo para quien no puede
        usarlo como vosotros, mirar d&oacute;nde acaba cuando se tira, y la defensa de verdad ante
        gente de fuera del aula.
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
    dict(corto=u'Qui&eacute;n decide qu&eacute; se fabrica',
         titulo=u'De 1.393 medicamentos nuevos, 16 para lo que mata a m&aacute;s gente',
         entradilla=u'No hace falta una conspiraci&oacute;n para que un problema se quede sin '
                    u'resolver: basta con una divisi&oacute;n. Y la segunda parte pasa en vuestro '
                    u'instituto.',
         minutado=MIN,
         chips=[u'CE6 &middot; 6.1', u'CE6 &middot; 6.2', u'D.1', u'D.2'], cuerpo=S1),
    dict(corto=u'Tecnolog&iacute;a apropiada',
         titulo=u'El columpio que sacaba agua, y las horas que no cab&iacute;an en el d&iacute;a',
         entradilla=u'Dinero, premios y mil instalaciones, y no sirvi&oacute;. La soluci&oacute;n '
                    u'buena depende del sitio, y eso se calcula.',
         minutado=MIN,
         chips=[u'CE6 &middot; 6.1', u'CE6 &middot; 6.3', u'D.2', u'D.3'], cuerpo=S2),
    dict(corto=u'Presentar y defender',
         titulo=u'Seis minutos, tres personas que no estaban y una pregunta inc&oacute;moda',
         entradilla=u'La r&uacute;brica, por adelantado. Y la demostraci&oacute;n de que el mismo '
                    u'proyecto saca 4,17 o 9,67 seg&uacute;n d&oacute;nde gastes los segundos.',
         minutado=MIN,
         chips=[u'CE2 &middot; 2.1', u'CE6 &middot; 6.3', u'A.2', u'D.4'], cuerpo=S3),
    dict(corto=u'Lo que queda',
         titulo=u'&iquest;Cu&aacute;ndo devuelve tu aparato lo que cost&oacute; hacerlo?',
         entradilla=u'La &uacute;ltima cuenta del curso, y no sale bien. Impactos que no se pueden '
                    u'sumar, escala, y por d&oacute;nde seguir.',
         minutado=[(u"10'", u'Reto'), (u"25'", u'Teor&iacute;a'), (u"15'", u'Pr&aacute;ctica'),
                   (u"10'", u'Cierre y test')],
         chips=[u'CE6 &middot; 6.2', u'CE6 &middot; 6.3', u'D.2', u'D.3', u'D.4'], cuerpo=S4),
    dict(corto=u'El ciclo de vida completo', pendiente=True),
    dict(corto=u'Dise&ntilde;ar para todo el mundo', pendiente=True),
    dict(corto=u'D&oacute;nde acaba cuando se tira', pendiente=True),
    dict(corto=u'La defensa de verdad', pendiente=True),
]

CFG = dict(
    ruta='4eso/Tecnologia/tema9/',
    migas=u'<a href="../../../">Materiales</a> &middot; <a href="../../">4.&ordm; ESO</a> '
          u'&middot; <a href="../">Tecnolog&iacute;a</a> &middot; Tema 9',
    h1=u'Tecnolog&iacute;a y sociedad: proyectos de servicio',
    titulo=u'Tema 9 &middot; Tecnolog&iacute;a y sociedad: proyectos de servicio',
    tema=u'Tema 9', curso=u'4.&ordm; de ESO', materia=u'Tecnolog&iacute;a',
    desc=u'Tema 9 de Tecnolog&iacute;a de 4.&ordm; de ESO: qui&eacute;n decide qu&eacute; '
         u'tecnolog&iacute;a se fabrica y cu&aacute;l no, qu&eacute; es la tecnolog&iacute;a '
         u'apropiada, c&oacute;mo se defiende un proyecto con su r&uacute;brica delante y '
         u'cu&aacute;ndo devuelve un aparato lo que cost&oacute; hacerlo.',
    sesiones=S)


if __name__ == '__main__':
    destino = os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema9')
    if not os.path.isdir(destino):
        os.makedirs(destino)
    html = pagina(CFG)
    if USA_AVATAR[0]:
        html = html.replace(u'</style>', avatar_flat.CSS + u'</style>', 1)
    io.open(os.path.join(destino, 'index.html'), 'w', encoding='utf-8', newline='').write(html)
    print('Tema 9 de 4.o generado: %d bytes, %d sesiones (%d escritas, %d pendientes)'
          % (len(html), len(S), sum(1 for x in S if not x.get('pendiente')),
             sum(1 for x in S if x.get('pendiente'))))
