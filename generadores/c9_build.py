# -*- coding: utf-8 -*-
"""4.o de ESO - Tecnologia - Tema 9 - Tecnologia y sociedad: proyectos de servicio.

    ~/venv/bin/python generadores/c9_build.py

Escribe 4eso/Tecnologia/tema9/index.html. La "c" de los generadores de esta
unidad es de "cuarto": no choca con los u*_ de 2.o.

Ocho sesiones, las ocho escritas.

Criterios: CE2 / 2.1 y CE6 / 6.1, 6.2, 6.3. Ver CURRICULO.md.

Es la unidad que cierra el curso: recoge el proyecto y lo mira desde fuera.
La primera mitad es para MIRAR; la segunda, para que el aparato SALGA DEL
AULA y le sirva a alguien. El hilo, que es lo que importa:

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
      Cuando devuelve lo que costo? Test de las cuatro primeras.
  S5  Sabes lo que cuesta, pero no a quien le sirve. "Seria util" no es un
      requisito: lo pone una persona con nombre, se saca preguntando y se
      escribe con un numero y una unidad. Recoge la quinta pregunta del
      sitio, que la S2 dejo abierta.
  S6  Supon que lo consigues todo y el dia de la entrega funciona. Tres
      semanas despues la sonda esta comida por electrolisis y nadie se ha
      enterado. Cinco anos de mantenimiento en manos de OTRO, dia a dia. NO
      es el impacto ambiental (unidad 8) ni el residuo (unidad 3).
  S7  La etiqueta de la S6 resuelve una semana. Para CONTINUARLO hacen falta
      manual, esquema y, sobre todo, permiso: sin licencia, todos los
      derechos reservados. Aqui entra el CC BY-SA del pie de esta web.
  S8  Lo unico que no se puede ensayar: darselo. Prueba de aceptacion
      acordada ANTES, hecha delante, y escrito que se hace si no pasa.
      Cierre de la unidad y test de las ocho (identificador c9b, distinto
      del c9 de la S4: si se repite, los dos tests comparten ids del HTML y
      dejan de funcionar los dos).

Los ejemplos van SIEMPRE con los tres proyectos decididos en PROYECTOS.md
(A riego, B aviso de aula, C lampara). En la primera mitad rotan porque el
proyecto del curso aun no estaba decidido; en la segunda el riego es el
principal y los otros dos son las variantes, tal y como quedo en PROYECTOS.md.
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
from c9_escenas3 import REQUISITOS, MANTENIMIENTO
from c9_escenas4 import CONTINUAR, ACEPTACION
from test_auto import test

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USA_AVATAR = [False]


# --------------------------------------------------------------------------
# Piezas repetidas
# --------------------------------------------------------------------------
def foto(src, alt, pie, autor, licencia, commons, estilo=u''):
    """estilo: para las fotos verticales. Una foto 9:16 a todo el ancho de la
    columna se come dos pantallas de movil, asi que se le pone un ancho
    maximo y se centra. La imagen NO se recorta: se ensena entera."""
    return u'''      <figure class="foto"%s>
        <img src="../../../img/%s" alt="%s" loading="lazy">
        <figcaption>%s
          <span class="credito">%s &middot; %s &middot;
            <a href="%s" target="_blank" rel="noopener">Wikimedia Commons</a></span>
        </figcaption>
      </figure>
''' % (u' style="%s"' % estilo if estilo else u'', src, alt, pie, autor, licencia, commons)


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
        Estas cuatro sesiones os han dado la mirada y las cuentas. Las cuatro que quedan sirven para
        que el aparato <b>salga del aula</b>: para qui&eacute;n es exactamente, lo que cuesta
        mantenerlo vivo cuando vosotros ya no est&eacute;is, c&oacute;mo se deja para que otro pueda
        continuarlo, y c&oacute;mo se entrega de verdad a quien lo va a usar.
      </div>
'''


# ==========================================================================
# SESION 5 - Para quien, exactamente
# ==========================================================================
S5_RETO = u'''
      <p>La segunda mitad de la unidad cambia de sitio. Las cuatro sesiones anteriores eran para
         <b>mirar</b>: qui&eacute;n decide, d&oacute;nde encaja, c&oacute;mo se cuenta, qu&eacute;
         cuesta. Las cuatro que vienen son para que el aparato <b>salga del aula</b> y le sirva a
         alguien de verdad. Y eso empieza por saber a qui&eacute;n.</p>
      <p>En la sesi&oacute;n 2 dejamos una pregunta sin contestar. Era la quinta de las cinco del
         sitio: <b>&iquest;qui&eacute;n decidi&oacute; que este era el problema?</b> Hoy toca.</p>
      <div class="aviso">
        <span class="n-tag">El encargo</span>
        En pareja y en <b>dos minutos</b>: escribid <b>en una frase</b> para qui&eacute;n es vuestro
        proyecto. Sin adornos y sin pensarlo mucho.
      </div>
      <p>Casi todas las frases se parecen a estas tres:</p>
      <ul>
        <li><i>&laquo;Para el instituto, para ahorrar agua.&raquo;</i></li>
        <li><i>&laquo;Para que no se sequen las plantas.&raquo;</i></li>
        <li><i>&laquo;Para concienciar sobre el consumo.&raquo;</i></li>
      </ul>
      <p>Las tres tienen el mismo agujero, y es gordo: <b>dentro no hay nadie</b>. El instituto no
         riega, no se olvida y no se va quince d&iacute;as en agosto. Las plantas tampoco cambian
         pilas. Y &laquo;concienciar&raquo; no lo comprueba nadie nunca.</p>
      <p>Ahora mirad estas tres frases. Las dijo una persona de verdad, la profesora que lleva el
         huerto del centro, cuando le preguntaron:</p>
      <div class="def">
        <span class="n-tag">Lo que dijo, literal</span>
        <p style="margin:0 0 7px"><i>&laquo;Del 20 de julio al 1 de septiembre aqu&iacute; no viene
           nadie.&raquo;</i></p>
        <p style="margin:0 0 7px"><i>&laquo;El enchufe m&aacute;s cercano est&aacute; en el taller, a
           cuarenta metros.&raquo;</i></p>
        <p style="margin:0"><i>&laquo;Lo que se me muere no es la lechuga: son los
           semilleros.&raquo;</i></p>
      </div>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento antes de seguir</span>
        <p>Una de las tres <b>obliga a cambiar el aparato</b>, otra es una <b>limitaci&oacute;n que
           no pod&eacute;is tocar</b> y la tercera <b>cambia el proyecto entero</b>. Decid cu&aacute;l
           es cu&aacute;l, y por qu&eacute;. Despu&eacute;s tachad vuestra frase de antes y volved a
           escribirla, pero con <b>un nombre propio y una fecha dentro</b>.</p>
      </div>
'''

S5_TEORIA = u'''
      <p>La diferencia entre las frases de la profesora y las vuestras no es que ella sepa m&aacute;s
         de tecnolog&iacute;a. Es que las suyas <b>se pueden comprobar</b> y las vuestras no.</p>
      <div class="copiar">
        <h4>Un requisito es una frase que se puede comprobar</h4>
        <p>Para que una frase sea un requisito le tienen que caber tres cosas:</p>
        <ol>
          <li>un <b>n&uacute;mero con su unidad</b>, o una <b>prueba</b> que se pueda hacer delante
              de alguien;</li>
          <li><b>qui&eacute;n lo pidi&oacute;</b>, con nombre;</li>
          <li>y <b>c&oacute;mo se sabr&aacute;</b> si se cumple o no.</li>
        </ol>
        <p><i>&laquo;Que sea fiable&raquo;</i> no es un requisito: es un deseo.
           <i>&laquo;Que aguante 43 d&iacute;as sin que vaya nadie&raquo;</i> s&iacute;, porque el 15
           de septiembre se mira la planta y o est&aacute; viva o no lo est&aacute;.</p>
      </div>
      <div class="copiar">
        <h4>Tres cosas distintas, y conviene no mezclarlas</h4>
        <ul>
          <li><b>Requisito</b>: lo que tiene que conseguir. Lleva n&uacute;mero.
              <i>Quince d&iacute;as.</i></li>
          <li><b>Restricci&oacute;n</b>: lo que <b>no pod&eacute;is cambiar</b> por mucho que
              quer&aacute;is. <i>Por el pasillo no pasa un cable.</i> No se discute: se dise&ntilde;a
              con ella dentro.</li>
          <li><b>Deseo</b>: lo que estar&iacute;a bien. <i>Que quede bonito.</i> No se tira, pero va
              al final de la lista y se dice que va al final.</li>
        </ul>
        <p>La trampa m&aacute;s com&uacute;n es apuntar una restricci&oacute;n como si fuera un deseo.
           Entonces se dise&ntilde;a ignor&aacute;ndola y el d&iacute;a de la entrega no cabe por la
           puerta.</p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Ojo con la <b>soluci&oacute;n disfrazada de necesidad</b>. Cuando alguien te dice
           <i>&laquo;lo que hace falta aqu&iacute; es una app&raquo;</i>, no te est&aacute; contando su
           problema: te est&aacute; dando su soluci&oacute;n, que probablemente sea peor que la tuya
           porque &eacute;l no sabe qu&eacute; se puede construir. La pregunta que lo deshace es
           tonta y funciona siempre: <b>&laquo;&iquest;y eso para qu&eacute; te
           servir&iacute;a?&raquo;</b>. Se repite hasta que sale algo que no es un aparato. Suele
           hacer falta preguntarlo tres veces.</p>
      </div>

      <h3>C&oacute;mo se pregunta, que tampoco es obvio</h3>
      <p>Una entrevista mal hecha devuelve lo que t&uacute; quer&iacute;as o&iacute;r. La gente es
         amable y te dice que s&iacute;. As&iacute; que no se preguntan opiniones: se preguntan
         <b>hechos del pasado</b>.</p>
''' + foto('c9-entrevista.jpg',
           u'Dos personas frente a un port&aacute;til: una teclea y la otra, con una hoja de notas '
           u'escritas a mano, observa y se&ntilde;ala la pantalla',
           u'Una <b>prueba con la persona que lo va a usar</b>. Lo que se est&aacute; probando '
           u'aqu&iacute; es una p&aacute;gina web y no un riego, pero la t&eacute;cnica es la misma '
           u'y el detalle importante est&aacute; a la izquierda: <b>ese papel</b>. El que mira no '
           u'est&aacute; ense&ntilde;ando nada ni explicando c&oacute;mo funciona &mdash;eso lo '
           u'estropear&iacute;a&mdash;: est&aacute; <b>apuntando lo que hace el otro</b> mientras lo '
           u'hace. De la entrevista hay que salir con el papel lleno, no con una impresi&oacute;n '
           u'general.',
           u'Samuel Mann', u'CC BY 2.0',
           u'https://commons.wikimedia.org/wiki/File:Project_User_Experience_Testing_'
           u'(9719939867).jpg') + u'''
      <div class="copiar">
        <h4>Cinco preguntas que s&iacute; sacan requisitos</h4>
        <ol>
          <li><b>&iquest;Qu&eacute; haces ahora, exactamente?</b> Paso a paso, hoy. No
              qu&eacute; te gustar&iacute;a hacer.</li>
          <li><b>&iquest;Cu&aacute;ndo fue la &uacute;ltima vez que sali&oacute; mal? &iquest;Qu&eacute;
              pas&oacute;?</b> Aqu&iacute; salen los n&uacute;meros de verdad.</li>
          <li><b>&iquest;Cu&aacute;nto tiempo tienes para esto a la semana?</b> Porque el aparato le
              va a pedir algo de tiempo, y si no lo tiene, sobra.</li>
          <li><b>&iquest;Qu&eacute; pasa si falla y nadie se entera?</b> Lo que hay que proteger
              est&aacute; en esa respuesta.</li>
          <li><b>&iquest;Qu&eacute; es lo que yo no puedo cambiar?</b> Paredes, enchufes, horarios,
              normas del centro, personas.</li>
        </ol>
        <p>Y una regla que vale m&aacute;s que las cinco: <b>se anota lo que dice, entre
           comillas</b>. No lo que t&uacute; entiendes. En cuanto lo resumes con tus palabras, le has
           metido dentro tu soluci&oacute;n sin darte cuenta.</p>
      </div>

      <h3>De las comillas al n&uacute;mero</h3>
      <p>En la escena est&aacute;n los tres destinatarios con sus frases literales. Los mandos de la
         derecha son <b>vuestro aparato</b>, el que ten&eacute;is montado, y no cambian al cambiar de
         persona: el aparato es el mismo. Lo que cambia es lo que le piden.</p>
      <p>Empieza por <b>la vecina</b>, que es el caso amable, y ll&eacute;valo hasta que cumpla los
         tres. Despu&eacute;s pasa al <b>huerto</b> sin tocar nada.</p>
''' + REQUISITOS + u'''
      <div class="copiar">
        <h4>Lo que acaba de pasar</h4>
        <p>Con la vecina se llega: seis pilas, ocho litros de dep&oacute;sito y la placa durmiendo, y
           cumple <b>los tres</b>. Con el huerto <b>no se llega ni forzando los mandos al
           m&aacute;ximo</b>, y no porque el aparato sea peor: es que el bancal pide 6 litros al
           d&iacute;a y 43 d&iacute;as sin nadie son <b>258 litros</b>. Eso no es un dep&oacute;sito:
           es un bid&oacute;n de los grandes, o una toma de agua.</p>
        <p>En el aula de infantil pasa lo mismo por otro lado: la placa gasta 1,45 Wh al d&iacute;a
           durmiendo, y 90 d&iacute;as son 130 Wh, o sea <b>treinta y seis pilas</b>. Con ocho llega
           a 20 d&iacute;as de los 90.</p>
        <p>Conclusi&oacute;n, y es la de la sesi&oacute;n: cuando un mando no da para tanto, <b>lo que
           hay que cambiar no es el mando: es el dise&ntilde;o</b>. En el huerto, un enchufe y una
           toma de agua. En infantil, un enchufe. Y eso se sabe <b>antes</b> de construir si se
           pregunta antes de construir.</p>
      </div>
      <div class="copiar">
        <h4>Priorizar, que es decir que no</h4>
        <p>Una lista de requisitos sin orden no sirve, porque el d&iacute;a que falte tiempo
           &mdash;y va a faltar&mdash; no se sabr&aacute; qu&eacute; recortar. Se ordenan en tres
           montones:</p>
        <ul>
          <li><b>Sin esto no sirve.</b> Si falla uno, el aparato no se entrega.</li>
          <li><b>Esto lo mejora.</b> Se hace si da tiempo, y se dice que es as&iacute;.</li>
          <li><b>Esto es un lujo.</b> Se apunta para que no se olvide, y se deja para otro.</li>
        </ul>
        <p>La regla: <b>si todo est&aacute; en el primer mont&oacute;n, no hab&eacute;is
           priorizado</b>, os hab&eacute;is limitado a copiar la lista. Y quien decide el orden no
           sois vosotros: es quien lo va a usar.</p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>&iquest;Y los requisitos que <b>no son n&uacute;meros</b>? <i>&laquo;No leen.
           Ninguno&raquo;</i> no tiene unidades, y aun as&iacute; es el requisito m&aacute;s duro de
           esa aula. No se tiran: se convierten en una <b>comprobaci&oacute;n</b>, o sea en algo que
           se hace delante de la persona y que <b>puede salir mal</b>. En este caso: ense&ntilde;arle
           la se&ntilde;al a un ni&ntilde;o de cuatro a&ntilde;os y preguntarle qu&eacute; hay que
           hacer. Si no lo sabe, no cumple.</p>
        <p>Esa idea &mdash;convertir lo que no es un n&uacute;mero en algo que se comprueba
           delante&mdash; es toda la sesi&oacute;n 8.</p>
      </div>
'''

S5_PRACTICA = ficha(
    u'Actividad 5 &middot; La entrevista, y la lista con n&uacute;meros',
    [u'6.1', u'6.3', u'D.1', u'D.4'], u'Grupos de tres &middot; 20 min', u'''
          <h4>Primera parte &middot; la entrevista cruzada (10 min)</h4>
          <p>No hace falta salir del aula. Cada grupo recibe una <b>ficha de destinatario</b> (el
             conserje, la maestra de infantil, la vecina, quien lleva el huerto) con cuatro datos
             suyos que <b>no</b> puede soltar si no se los preguntan. Las frases de la escena de
             arriba sirven de modelo para escribir esas fichas: cuatro l&iacute;neas por persona,
             una de ellas la inc&oacute;moda.</p>
          <ol class="pasos">
            <li>Escribid vuestras <b>seis preguntas</b>: las cinco de la libreta m&aacute;s una
                vuestra. La vuestra tiene que ser sobre algo que os preocupe del aparato.</li>
            <li>Entrevistad al otro grupo, <b>cinco minutos</b>, y anotad sus respuestas
                <b>entre comillas</b>. Literal. Un secretario solo para eso.</li>
            <li>Cambiad los papeles y repetid.</li>
          </ol>
          <h4>Segunda parte &middot; la lista (10 min)</h4>
          <p>Con lo que ten&eacute;is anotado, una tabla de <b>seis filas</b>. Una por frase:</p>
          <ul>
            <li>la <b>frase literal</b>, entre comillas;</li>
            <li>si es <b>requisito, restricci&oacute;n o deseo</b>;</li>
            <li>el <b>n&uacute;mero con su unidad</b>, si lo lleva, o <b>c&oacute;mo se
                comprueba</b> si no lo lleva;</li>
            <li>el <b>mont&oacute;n</b>: sin esto no sirve / lo mejora / es un lujo;</li>
            <li>y lo que da <b>vuestro aparato</b> hoy, con la cuenta hecha.</li>
          </ul>
          <p>Por lo menos <b>tres</b> de las seis tienen que acabar en un n&uacute;mero, y una de
             ellas tiene que ser de <b>autonom&iacute;a</b>: cu&aacute;ntos d&iacute;as aguanta sin
             que vaya nadie. Esa la calcul&aacute;is con la escena y con la cuenta escrita.</p>
          <p>Y debajo, dos l&iacute;neas: <b>&iquest;cu&aacute;l de los seis os obliga a cambiar el
             dise&ntilde;o?</b> Si ninguno, es que hab&eacute;is entrevistado mal.</p>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Las seis frases, literales y entrecomilladas <b>(2 puntos)</b>.</li>
            <li>La clasificaci&oacute;n en requisito, restricci&oacute;n y deseo, bien razonada
                <b>(2 puntos)</b>.</li>
            <li>Los tres n&uacute;meros con unidad, y la cuenta de la autonom&iacute;a entera
                <b>(2 puntos)</b>.</li>
            <li>Las comprobaciones de los que no son n&uacute;meros, y que puedan salir mal
                <b>(2 puntos)</b>.</li>
            <li>Los tres montones, con al menos uno fuera del primero <b>(1 punto)</b>.</li>
            <li>El requisito que obliga a cambiar el dise&ntilde;o, se&ntilde;alado
                <b>(1 punto)</b>.</li>
          </ul>
''')

S5_CIERRE = u'''
      <ol>
      ''' + pregunta(u'&iquest;Qu&eacute; le falta a &laquo;nuestro proyecto es para el instituto, '
                     u'para ahorrar agua&raquo;?',
                     u'<p>Le falta <b>una persona dentro</b> y le falta un n&uacute;mero. El '
                     u'instituto no riega, no se olvida y no se va de vacaciones. Sin alguien '
                     u'concreto no hay requisitos, y sin requisitos no hay manera de saber si el '
                     u'aparato sirve: solo de saber si funciona, que es otra cosa.</p>') + pregunta(
          u'Distingue requisito, restricci&oacute;n y deseo con un ejemplo de cada uno.',
          u'<p><b>Requisito</b>: lo que tiene que conseguir, con n&uacute;mero &mdash;'
          u'&laquo;aguantar quince d&iacute;as&raquo;&mdash;. <b>Restricci&oacute;n</b>: lo que no '
          u'pod&eacute;is cambiar &mdash;&laquo;por el pasillo no pasa un cable&raquo;&mdash;; se '
          u'dise&ntilde;a con ella dentro. <b>Deseo</b>: lo que estar&iacute;a bien '
          u'&mdash;&laquo;que quede bonito&raquo;&mdash;; va al final de la lista y se dice.</p>')\
    + pregunta(
          u'El mismo aparato cumple con la vecina y suspende en el huerto. &iquest;Por qu&eacute;?',
          u'<p>Porque el requisito lo pone la persona, no el aparato. La vecina se va <b>15 '
          u'd&iacute;as</b> y tiene cinco macetas que piden medio litro al d&iacute;a: son 7,6 '
          u'litros. El huerto est&aacute; <b>43 d&iacute;as</b> solo y el bancal pide 6 litros al '
          u'd&iacute;a: son <b>258 litros</b>. No cabe en ning&uacute;n dep&oacute;sito que pod&aacute;is '
          u'poner, as&iacute; que all&iacute; hay que cambiar el dise&ntilde;o, no los mandos.</p>')\
    + pregunta(
          u'La maestra dice &laquo;no leen, ninguno&raquo;. No hay n&uacute;mero. '
          u'&iquest;Se tira ese requisito?',
          u'<p>No: se convierte en una <b>comprobaci&oacute;n</b>. Se le ense&ntilde;a la '
          u'se&ntilde;al a un ni&ntilde;o de cuatro a&ntilde;os y se le pregunta qu&eacute; hay que '
          u'hacer. Si no lo sabe, no cumple. Un requisito sin n&uacute;mero sigue valiendo mientras '
          u'haya una manera de comprobarlo <b>que pueda salir mal</b>.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya sab&eacute;is para qui&eacute;n es y qu&eacute; os pide. Supongamos que lo
        consegu&iacute;s todo y que el d&iacute;a de la entrega funciona. La sesi&oacute;n que viene
        empieza <b>tres semanas despu&eacute;s</b>, con la sonda de humedad en la mano: los dos
        clavos est&aacute;n negros y el aparato lleva seis d&iacute;as diciendo que la tierra
        est&aacute; mojada. Nadie lo ha tocado. Nadie se ha enterado.
      </div>
'''


# ==========================================================================
# SESION 6 - Lo que cuesta mantenerlo
# ==========================================================================
S6_RETO = u'''
      <p>Han pasado tres semanas desde que lo dejasteis funcionando. Sacad la sonda de humedad de la
         tierra y miradla a contraluz.</p>
      <div class="aviso">
        <span class="n-tag">El encargo</span>
        Uno de los dos clavos est&aacute; <b>comido</b>: picado, m&aacute;s fino y con una costra
        verdosa. El otro est&aacute; casi entero. En el cuaderno, <b>tres minutos</b>:
        &iquest;por qu&eacute; uno s&iacute; y el otro no?
      </div>
      <p>No es mala suerte ni es que el clavo fuera malo. Pasar corriente continua por tierra mojada
         es <b>hacer la electr&oacute;lisis</b>, y en una electr&oacute;lisis el electrodo positivo
         se disuelve. Le pasa a todo el mundo que mide humedad con dos clavos, y por eso las sondas
         que se venden hechas o son <b>capacitivas</b> o solo se alimentan el instante en que miden.
         El aparato no se ha roto: se ha <b>gastado</b>, que es distinto y mucho m&aacute;s
         com&uacute;n.</p>
      <div class="reto-piensa">
        <span class="n-tag">Pero lo importante no es el clavo</span>
        <p>La sonda lleva seis d&iacute;as dando una lectura falsa. El aparato est&aacute; encendido,
           el LED verde luce y la planta se est&aacute; secando. Escribid dos cosas en el
           cuaderno:</p>
        <p style="margin-top:7px"><b>&iquest;Cu&aacute;ntos d&iacute;as tardar&iacute;a alguien en
           enterarse?</b> Y despu&eacute;s, lo que de verdad cuesta: <b>&iquest;qui&eacute;n es ese
           alguien?</b> Con nombre y apellido, no &laquo;el centro&raquo;.</p>
      </div>
      <p>Eso de ah&iacute; es la sesi&oacute;n de hoy. <b>No</b> vamos a hablar de lo que contamina
         &mdash;eso fue la unidad 8&mdash; ni de d&oacute;nde acaba cuando se tira &mdash;eso fue la
         3&mdash;. Vamos a hablar de algo m&aacute;s corto y m&aacute;s incómodo: <b>cu&aacute;nto
         tiempo sigue vivo vuestro aparato cuando vosotros ya no est&aacute;is</b>.</p>
'''

S6_TEORIA = u'''
      <p>En la sesi&oacute;n 4 dijimos que el aparato cost&oacute; 25 &euro; de material. Esa cifra
         es verdad y es la menos importante de todas.</p>
      <div class="copiar">
        <h4>El precio no es el coste</h4>
        <p>El <b>precio</b> es lo que pagas el primer d&iacute;a. El <b>coste</b> es lo que te va a
           costar tenerlo, y se cuenta a un plazo:</p>
        <p style="font-family:var(--f-m);font-size:14px">coste a 5 a&ntilde;os = material inicial
           + lo que se gasta (pilas, piezas, agua) + <b>las horas de quien lo cuida</b></p>
        <p>La tercera es la que nadie suma, porque no se factura. Pero <b>alguien las pone</b>: el
           conserje que sube al huerto, la maestra que cambia cuatro pilas, el jefe de departamento
           que pide un recambio. Que no se cobre no significa que sea gratis; significa que lo paga
           alguien que no sale en la cuenta.</p>
      </div>
      <div class="copiar">
        <h4>Las cuatro preguntas del mantenimiento</h4>
        <p>Son hermanas de las cinco preguntas del sitio de la sesi&oacute;n 2, pero miran al futuro
           en vez de al lugar:</p>
        <ol>
          <li><b>&iquest;Qu&eacute; se gasta, y cada cu&aacute;nto?</b> Agua, pilas, la propia sonda.
              Con un n&uacute;mero de d&iacute;as, no con un &laquo;de vez en cuando&raquo;.</li>
          <li><b>&iquest;Qui&eacute;n va a ir?</b> Con nombre.</li>
          <li><b>&iquest;Cu&aacute;nto tarda en enterarse de que hay que ir?</b> Porque el aparato no
              llama por tel&eacute;fono.</li>
          <li><b>&iquest;D&oacute;nde est&aacute; el recambio y cu&aacute;nto tarda en llegar?</b>
              El caj&oacute;n del taller no es lo mismo que tres semanas de env&iacute;o.</li>
        </ol>
        <p>Y la quinta, que es la que mata: <b>&iquest;qui&eacute;n ir&aacute; cuando vosotros ya no
           est&eacute;is?</b></p>
      </div>
      <p>La escena recorre los <b>1.825 d&iacute;as</b> siguientes a la entrega, uno a uno. Cada cosa
         que se gasta tiene su reloj; cuando una se agota, el aparato <b>se para</b> y no vuelve
         hasta que alguien va. Empieza tal y como est&aacute; ahora mismo vuestro montaje.</p>
''' + MANTENIMIENTO + u'''
      <div class="copiar">
        <h4>Lo que sale, y no lo arregla ning&uacute;n destornillador</h4>
        <ul>
          <li><b>Tal y como est&aacute;</b> &mdash;pilas, dos clavos, dos litros de dep&oacute;sito y
              vosotros cuid&aacute;ndolo&mdash; hay que ir <b>72 veces</b>, son <b>22 horas</b> de
              alguien... y aun as&iacute; el aparato <b>se para para siempre el d&iacute;a 273</b>,
              tres d&iacute;as despu&eacute;s de que dej&eacute;is de pasaros por all&iacute;.
              Funcion&oacute; el <b>7 %</b> de los cinco a&ntilde;os.</li>
          <li><b>Con enchufe, sonda capacitiva, dep&oacute;sito grande y el conserje</b>: <b>5
              visitas</b>, <b>1,7 horas</b> y <b>98 % de disponibilidad</b>. El mismo aparato, el
              mismo problema y la misma gente.</li>
          <li>Entre esos dos extremos no hay nada m&aacute;s caro: la sonda capacitiva cuesta
              2,50 &euro;. Lo que cambia son <b>decisiones</b>, no presupuesto.</li>
        </ul>
      </div>
      <div class="copiar">
        <h4>Disponibilidad: no es &laquo;funciona&raquo;, es cu&aacute;nto tiempo funciona</h4>
        <p style="font-family:var(--f-m);font-size:14px">disponibilidad =
           d&iacute;as funcionando &divide; d&iacute;as totales</p>
        <p>Un aparato que <b>aguanta cuatro d&iacute;as</b> y <b>tarda dos en volver</b> est&aacute;
           disponible cuatro de cada seis d&iacute;as: el <b>67 %</b>. Con las mismas piezas, si
           solo aguanta <b>dos</b> y tarda <b>cuatro</b>, baja al <b>33 %</b>.</p>
        <p>O sea que lo que manda no es solo lo r&aacute;pido que se arregla: es la relaci&oacute;n
           entre <b>cu&aacute;nto aguanta</b> y <b>cu&aacute;nto tarda en volver</b>. Y de los dos,
           el f&aacute;cil de mover es el primero. Por eso la palanca m&aacute;s potente de todas no
           es arreglar mejor: es <b>que no haga falta ir</b>.</p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Fíjate en d&oacute;nde est&aacute;n los mandos que mueven el resultado: <b>de d&oacute;nde
           sale la energ&iacute;a</b>, <b>cu&aacute;nto guarda el dep&oacute;sito</b> y <b>qu&eacute;
           sonda lleva</b>. Los tres son decisiones que se toman <b>dise&ntilde;ando</b>, meses antes
           de que haya nada que mantener. El &uacute;nico mando que es de mantenimiento de verdad
           &mdash;qui&eacute;n va&mdash; lo mueve menos que los otros tres.</p>
        <p>De ah&iacute; la frase de la sesi&oacute;n, y conviene que se quede: <b>el mantenimiento
           no se decide manteniendo, se decide dise&ntilde;ando.</b></p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Compara el proyecto <b>C</b> con enchufe &mdash;cero visitas, 100 % de tiempo
           funcionando&mdash; con el <b>A</b>. Es una tentaci&oacute;n concluir que el C es mejor
           proyecto, y no lo es: en la sesi&oacute;n 4 vimos que era el que <b>menos ahorraba</b>,
           tan poco que no devolv&iacute;a nunca lo que cost&oacute;. <b>Lo que menos mantenimiento
           pide suele ser lo que menos hace.</b> Un aparato que no toca nada tampoco arregla
           nada.</p>
      </div>
''' + foto('c9-bomba-averiada.jpg',
           u'Dos hombres reparan una bomba de mano de pozo en la calle de un pueblo; la tapa '
           u'est&aacute; abierta, hay dos llaves y un tornillo en el suelo y sale agua por el ca&ntilde;o',
           u'Reparando una <b>bomba de mano</b> de pozo. M&iacute;rala con calma, porque est&aacute; '
           u'todo: la tapa abierta, <b>dos llaves fijas y un tornillo en el suelo</b>, gente del '
           u'sitio con las manos dentro y agua saliendo por el ca&ntilde;o. En la sesi&oacute;n 2 '
           u'dijimos que la bomba de mano de toda la vida le ganaba a la PlayPump. No le ganaba '
           u'bombeando m&aacute;s: le ganaba <b>porque esto se puede hacer</b>, con piezas normales, '
           u'llaves normales y alguien de all&iacute; que sabe. Esta escena no sale en ninguna foto '
           u'de inauguraci&oacute;n, y es la que decide si el aparato sigue vivo dentro de cinco '
           u'a&ntilde;os.',
           u'Tsumoses', u'CC BY-SA 4.0',
           u'https://commons.wikimedia.org/wiki/File:Repair_handpump.jpg',
           u'max-width:440px;margin-left:auto;margin-right:auto') + u'''
      <div class="copiar">
        <h4>El cuaderno de mantenimiento, que es media hoja</h4>
        <p>Va pegado <b>al propio aparato</b>, por dentro de la tapa. No en una carpeta.</p>
        <ul>
          <li><b>Qu&eacute; hay que hacer</b>, en una l&iacute;nea por cosa.</li>
          <li><b>Cada cu&aacute;ntos d&iacute;as</b>, con el n&uacute;mero.</li>
          <li><b>Qui&eacute;n</b>, con nombre y no con cargo.</li>
          <li><b>D&oacute;nde est&aacute; el recambio</b> y qu&eacute; pone exactamente en la
              caja.</li>
          <li><b>C&oacute;mo se sabe que hay que hacerlo</b>: qu&eacute; se ve o qu&eacute; deja de
              verse.</li>
          <li>Y unas casillas en blanco para <b>apuntar la fecha</b> cada vez que se hace. Eso es lo
              que convierte un plan en un historial.</li>
        </ul>
      </div>
'''

S6_PRACTICA = ficha(
    u'Actividad 6 &middot; El plan a cinco a&ntilde;os, y la etiqueta que se pega dentro',
    [u'6.2', u'6.3', u'D.2', u'D.3'], u'Grupos de tres &middot; 20 min', u'''
          <h4>Primera parte &middot; la cuenta (10 min)</h4>
          <p>Para <b>vuestro</b> proyecto, en la libreta y con la escena delante:</p>
          <ol class="pasos">
            <li>Listad <b>todo lo que se gasta</b>, con los d&iacute;as que dura cada cosa. Como
                m&iacute;nimo: la energ&iacute;a, el sensor y, si riega, el agua.</li>
            <li>Elegid <b>qui&eacute;n</b> lo mantiene y cu&aacute;nto tarda en enterarse. Anotad su
                nombre de verdad, y si no lo sab&eacute;is, ese es el primer problema.</li>
            <li>Sacad de la escena las <b>cinco cifras</b>: veces que hay que ir, horas, euros de
                piezas, d&iacute;as parado y disponibilidad. Copiadlas con el montaje <b>tal y como
                est&aacute; hoy</b>.</li>
            <li>Ahora cambiad <b>una sola cosa</b> del dise&ntilde;o y volved a sacarlas. La que
                m&aacute;s suba la disponibilidad. Escribid cu&aacute;l era y cu&aacute;nto la
                sube.</li>
            <li>Y la pregunta que no se puede esquivar: <b>&iquest;llega vivo a los cinco
                a&ntilde;os?</b> Si no, decid el d&iacute;a exacto en que se muere y por qu&eacute;
                pieza.</li>
          </ol>
          <h4>Segunda parte &middot; la etiqueta (10 min)</h4>
          <p>Media cuartilla, escrita a mano y a tama&ntilde;o legible, para pegar <b>por dentro de
             la tapa</b> del aparato. Con las seis columnas de la libreta. Tiene que servirle a
             alguien que <b>no ha hablado con vosotros nunca</b>.</p>
          <p>Prueba de que est&aacute; bien: <b>d&aacute;dsela a otro grupo</b> y que os digan, sin
             preguntaros nada, qu&eacute; tendr&iacute;an que hacer el mi&eacute;rcoles que viene. Si
             tienen que preguntar, no est&aacute; terminada.</p>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>La lista de lo que se gasta, con los d&iacute;as de cada cosa <b>(2 puntos)</b>.</li>
            <li>Las cinco cifras del montaje de hoy, copiadas con sus unidades
                <b>(2 puntos)</b>.</li>
            <li>El cambio de dise&ntilde;o y cu&aacute;nto sube la disponibilidad
                <b>(2 puntos)</b>.</li>
            <li>La respuesta a si llega vivo a los cinco a&ntilde;os, con el d&iacute;a y la pieza
                <b>(1 punto)</b>.</li>
            <li>La etiqueta, con las seis columnas y con un nombre propio dentro
                <b>(2 puntos)</b>.</li>
            <li>Que otro grupo la entienda sin preguntaros <b>(1 punto)</b>.</li>
          </ul>
''')

S6_CIERRE = u'''
      <ol>
      ''' + pregunta(u'&iquest;Por qu&eacute; se come uno de los dos clavos de la sonda y el otro '
                     u'no?',
                     u'<p>Porque pasar corriente continua por tierra mojada es hacer una '
                     u'<b>electr&oacute;lisis</b>, y en una electr&oacute;lisis se disuelve el '
                     u'electrodo <b>positivo</b>. No es un defecto del montaje: le pasa a cualquier '
                     u'sonda de dos clavos alimentada todo el rato. Se arregla alimentando la sonda '
                     u'solo el instante en que se mide, o poniendo una sonda '
                     u'<b>capacitiva</b>.</p>') + pregunta(
          u'El aparato cost&oacute; 25 &euro;. &iquest;Por qu&eacute; esa cifra no dice lo que '
          u'cuesta?',
          u'<p>Porque el precio es lo que pagas el primer d&iacute;a y el coste es lo que te cuesta '
          u'tenerlo: hay que sumarle <b>lo que se gasta</b> (pilas, piezas, agua) y sobre todo '
          u'<b>las horas de quien lo cuida</b>. Esas horas no se facturan, pero las pone alguien. '
          u'En el caso de partida son 22 horas en cinco a&ntilde;os, m&aacute;s de trece veces el '
          u'precio del material.</p>') + pregunta(
          u'Un aparato aguanta cuatro d&iacute;as y tarda dos en volver. &iquest;Qu&eacute; '
          u'disponibilidad tiene? &iquest;Y si aguanta dos y tarda cuatro?',
          u'<p>El <b>67 %</b> en el primer caso (cuatro d&iacute;as de cada seis) y el <b>33 %</b> '
          u'en el segundo (dos de cada seis), <b>con las mismas piezas</b>. Lo que manda es la '
          u'relaci&oacute;n entre cu&aacute;nto aguanta y cu&aacute;nto tarda en volver, y de los '
          u'dos el f&aacute;cil de mover es el primero: <b>que no haga falta ir</b>.</p>')\
    + pregunta(
          u'&iquest;Cu&aacute;l es el mando que m&aacute;s sube la disponibilidad, y por qu&eacute; '
          u'sorprende?',
          u'<p>Los que m&aacute;s la suben son <b>de d&oacute;nde sale la energ&iacute;a</b>, '
          u'<b>cu&aacute;nto guarda el dep&oacute;sito</b> y <b>qu&eacute; sonda lleva</b>: los '
          u'tres son decisiones de <b>dise&ntilde;o</b>, tomadas meses antes de que hubiera nada que '
          u'mantener. El &uacute;nico que es de mantenimiento &mdash;qui&eacute;n va&mdash; mueve '
          u'menos. De ah&iacute;: <b>el mantenimiento se decide dise&ntilde;ando</b>.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        La etiqueta de hoy resuelve <b>una</b> semana. Pero imagina que tres a&ntilde;os
        despu&eacute;s alguien quiere <b>continuar</b> el proyecto: no cambiar la pila, sino
        cogerlo, mejorarlo y volverlo a poner. Abre la caja del armario y encuentra el aparato, un
        manojo de cables sin etiquetas y un papel que pone <i>&laquo;umbral 430&raquo;</i>.
        &iquest;Cu&aacute;nto tarda? Y una pregunta que no se le ocurre a nadie:
        <b>&iquest;puede?</b>
      </div>
'''


# ==========================================================================
# SESION 7 - Que otro lo pueda continuar
# ==========================================================================
S7_RETO = u'''
      <p>Curso 2029. Un grupo de 4.&ordm; est&aacute; buscando proyecto y el profesor abre el armario
         del taller: <i>&laquo;Mirad, esto lo hicieron unos hace tres a&ntilde;os. Funcionaba.&raquo;</i>
         Dentro de la caja est&aacute;n el aparato, un manojo de cables de colores sin una sola
         etiqueta y un
         papel con dos palabras escritas a boli: <b>umbral 430</b>.</p>
      <div class="aviso">
        <span class="n-tag">El encargo</span>
        En pareja y en <b>tres minutos</b>: escribid las <b>cinco preguntas</b> que se har&iacute;a
        ese grupo, en el orden exacto en que se les ocurrir&iacute;an.
      </div>
      <p>Las listas se parecen mucho: <i>&iquest;qu&eacute; es esto?</i>, <i>&iquest;c&oacute;mo va
         conectado?</i>, <i>&iquest;d&oacute;nde est&aacute; el programa?</i>, <i>&iquest;430 de
         qu&eacute;?</i>, <i>&iquest;funciona todav&iacute;a?</i>. Todas se contestan con
         <b>tiempo</b>: si nadie lo dej&oacute; escrito, hay que volver a averiguarlo.</p>
      <div class="reto-piensa">
        <span class="n-tag">Falta una, y no se le ocurre a casi nadie</span>
        <p>Supongamos que consiguen contestarlas todas. Lo arreglan, lo mejoran, lo dejan
           precioso... y lo quieren <b>publicar</b>, o ense&ntilde;arlo en una feria, o d&aacute;rselo
           a otro centro.</p>
        <p>La pregunta que falta es esta: <b>&iquest;pueden?</b> &iquest;Qui&eacute;n les ha dado
           permiso? Escribid vuestra respuesta antes de seguir. Casi todo el mundo contesta
           <i>&laquo;claro, si no pone nada&raquo;</i>, y esa respuesta es exactamente la
           contraria de la verdadera.</p>
      </div>
'''

S7_TEORIA = u'''
      <p>Vamos por partes: primero el tiempo, que se calcula, y luego el permiso, que no.</p>
      <p>La escena tiene dos modos. En el primero, <b>marcad lo que dej&aacute;is en la caja</b> y
         mirad lo que le cuesta al siguiente grupo lo que no hab&eacute;is dejado. Empezad con todo
         sin marcar, que es como se queda una caja cuando nadie se ocupa.</p>
''' + CONTINUAR + u'''
      <div class="copiar">
        <h4>Lo que acaba de pasar</h4>
        <p>Sin nada escrito, al siguiente grupo le cuesta <b>10 horas y 10 minutos</b> volver al
           punto donde vosotros lo dejasteis. Tiene <b>ocho sesiones</b>, o sea 6 horas y 40 minutos,
           para hacer la unidad entera. <b>No le cabe</b>: as&iacute; que no lo contin&uacute;a, lo
           tira y empieza de cero.</p>
        <p>Dejarlo todo escrito os cuesta <b>1 hora y 45 minutos</b>. Cada minuto vuestro le ahorra a
           &eacute;l <b>casi seis</b>. No hay ninguna otra decisi&oacute;n del proyecto con esa
           rentabilidad.</p>
      </div>
      <div class="copiar">
        <h4>El paquete m&iacute;nimo, y por qu&eacute; cada cosa</h4>
        <ol>
          <li><b>D&oacute;nde est&aacute; guardado.</b> Y que siga existiendo: la carpeta del
              departamento, no la cuenta del instituto que se borra cuando os vais.</li>
          <li><b>El esquema el&eacute;ctrico</b>, con qu&eacute; va a qu&eacute; pin.</li>
          <li><b>La lista de piezas</b>, con la referencia exacta y d&oacute;nde se compran.</li>
          <li><b>El programa</b>, el fichero de verdad. No una captura de pantalla.</li>
          <li><b>El programa comentado</b>: por qu&eacute; el umbral es 430 y no 500.</li>
          <li><b>C&oacute;mo se calibr&oacute;</b>, paso a paso, con los dos n&uacute;meros que
              sal&iacute;an.</li>
          <li><b>Una hoja de manual</b>: qu&eacute; hace, c&oacute;mo se usa, qu&eacute; falla.</li>
          <li><b>Una foto</b> del montaje terminado.</li>
          <li><b>La licencia</b>, escrita dentro del propio documento.</li>
        </ol>
        <p>La primera anula a todas las dem&aacute;s. Un paquete perfecto en un sitio que desaparece
           vale cero, y por eso en la escena la casilla de arriba apaga el resto.</p>
      </div>
      <div class="copiar">
        <h4>El esquema no es la foto</h4>
        <p>La foto dice <b>c&oacute;mo qued&oacute;</b>: este cable rojo cruzando por encima del
           sensor. El esquema dice <b>qu&eacute; es</b>: la salida del sensor va a A0, y el positivo
           de la bomba al pin 9 a trav&eacute;s del transistor.</p>
        <p>La diferencia salta cuando algo cambia. Si el sensor que usasteis ya no se vende,
           con la foto est&aacute;s perdido y con el esquema no, porque el esquema dice <b>qu&eacute;
           papel</b> hac&iacute;a esa pieza. Por eso el dibujo t&eacute;cnico se invent&oacute;: para
           que un dise&ntilde;o sobreviva a las piezas concretas con las que se hizo la primera
           vez.</p>
      </div>
''' + foto('c9-esquema-1917.jpg',
           u'Esquema el&eacute;ctrico a l&iacute;nea del receptor de radio SCR-54, con la antena, la '
           u'toma de tierra, las bobinas con sus tomas numeradas, los condensadores variables, el '
           u'detector y la clavija de los auriculares',
           u'El esquema del <b>receptor de radio SCR-54</b>, que el ej&eacute;rcito de Estados '
           u'Unidos us&oacute; en la Primera Guerra Mundial. Tiene m&aacute;s de <b>cien '
           u'a&ntilde;os</b> y con &eacute;l todav&iacute;a se puede montar el aparato, porque no '
           u'dice <i>&laquo;el cable rojo va por encima&raquo;</i>: dice qu&eacute; hace cada pieza '
           u'&mdash;antena, tierra, inductancia primaria, condensador variable, detector, clavija '
           u'del tel&eacute;fono&mdash; y c&oacute;mo se conectan entre s&iacute;. F&iacute;jate en '
           u'los n&uacute;meros de las bobinas: ah&iacute; est&aacute;n hasta las tomas, que es la '
           u'informaci&oacute;n que en vuestro proyecto equivale al umbral 430. <b>Eso</b> es lo que '
           u'hay que dejar en la caja.',
           u'Signal Corps, U.S. Army', u'Dominio p&uacute;blico',
           u'https://commons.wikimedia.org/wiki/File:SCR-54_schematic.jpg') + u'''

      <h3>Y ahora el permiso</h3>
      <p>Cambiad la escena al segundo modo, <b>&laquo;lo que deja hacer la licencia&raquo;</b>.
         Empezad por la primera opci&oacute;n, la de <b>no poner nada</b>, que es lo que hace casi
         todo el mundo.</p>
      <div class="copiar">
        <h4>Sin licencia no es de todos: es solo tuyo</h4>
        <p>Los derechos de autor <b>no hay que pedirlos</b>. Nacen solos, en el momento en que
           hac&eacute;is algo original, sin registrar nada y sin poner ning&uacute;n s&iacute;mbolo.
           Eso quiere decir que lo que no lleva licencia tiene, por defecto, <b>todos los derechos
           reservados</b>.</p>
        <p>As&iacute; que el grupo de 2029 puede mirarlo y puede copiarlo para &eacute;l, pero
           <b>no puede publicarlo, ni repartirlo, ni ense&ntilde;arlo como suyo mejorado</b>. Y no
           porque vosotros no quisierais: porque no dijisteis nada, y para el derecho callarse es
           decir que no.</p>
        <p>Poner una licencia no es regalar el trabajo. Es <b>dar permiso por escrito</b> y decir
           hasta d&oacute;nde.</p>
      </div>
      <div class="copiar">
        <h4>Las letras, y qu&eacute; a&ntilde;ade cada una</h4>
        <ul>
          <li><b>BY</b> (reconocimiento): haz lo que quieras, pero <b>di de qui&eacute;n es</b>. Va
              en todas las licencias Creative Commons menos en CC0.</li>
          <li><b>SA</b> (compartir igual): tu versi&oacute;n se publica <b>con esta misma
              licencia</b>. Es lo que impide que alguien coja algo abierto, lo mejore y lo
              cierre.</li>
          <li><b>NC</b> (no comercial): nadie puede ganar dinero con ello. Suena bien y tiene un
              efecto que no se espera: deja fuera a la Wikipedia, a una editorial que lo imprima al
              coste y al AMPA de vuestro propio centro.</li>
          <li><b>ND</b> (sin obra derivada): se puede repartir, pero <b>no modificar</b>. Para un
              proyecto t&eacute;cnico es la peor de todas: continuar es modificar.</li>
          <li><b>CC0</b>: renuncias a todo, ni siquiera hace falta que te citen.</li>
        </ul>
      </div>
      <p>Prueba en la escena las cinco y mira la cadena de tres generaciones: vosotros, el grupo de
         2029 y el de 2032. Fíjate en <b>d&oacute;nde se corta</b>.</p>
      <div class="copiar">
        <h4>Esta p&aacute;gina lleva CC BY-SA 4.0. Mira el pie</h4>
        <p>Baja al final de esta p&aacute;gina, o mira la esquina de abajo a la derecha: pone
           <b>CC BY-SA 4.0</b> y el nombre del autor. Eso significa, exactamente, que t&uacute;
           puedes:</p>
        <ul>
          <li>copiar estos apuntes, imprimirlos y repartirlos;</li>
          <li>cambiarlos, quitarles lo que no te sirva y a&ntilde;adirles lo tuyo;</li>
          <li>incluso venderlos impresos;</li>
        </ul>
        <p>a cambio de dos cosas: <b>citar de qui&eacute;n salieron</b> y <b>publicar tu
           versi&oacute;n con la misma licencia</b>, para que el siguiente pueda hacer lo mismo
           contigo.</p>
        <p>Eso es lo que se llama <b>copyleft</b>: no es lo contrario del derecho de autor, es el
           derecho de autor usado al rev&eacute;s, para obligar a que lo que salga de aqu&iacute;
           siga abierto.</p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>&iquest;Por qu&eacute; esta web es BY-SA y no BY-NC, que parece m&aacute;s protectora? Por
           dos razones, y las dos tienen coste. La primera: <b>NC bloquea usos que interesan</b>
           &mdash;que la Wikipedia coja un esquema, que una copister&iacute;a lo imprima cobrando el
           papel, que una asociaci&oacute;n lo use en un taller de pago&mdash;. La segunda:
           <b>&laquo;comercial&raquo; no est&aacute; definido con precisi&oacute;n</b>, y una duda de
           ese tipo hace que la gente prudente no lo use.</p>
        <p>Y la contrapartida, que es honrada decir: <b>SA le quita una libertad al siguiente</b>,
           la de cerrar su versi&oacute;n. Es una decisi&oacute;n, no un descuido, y se puede estar
           en contra. Lo que no se puede es no decidir: eso es lo que hace la primera opci&oacute;n
           de la escena.</p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Esto es un resumen para entenderlo y <b>no es asesoramiento legal</b>. El texto que manda
           es el de cada licencia, en creativecommons.org, y hay matices que aqu&iacute; se han
           dejado fuera a prop&oacute;sito. Adem&aacute;s, las licencias Creative Commons est&aacute;n
           pensadas para <b>obras</b> &mdash;textos, dibujos, esquemas, fotos&mdash;. Para el
           <b>programa</b> se suelen usar otras (MIT, GPL) y para el <b>hardware</b>, otras m&aacute;s
           (CERN OHL). En 4.&ordm; vale con poner CC BY-SA a todo y saber que existe la
           diferencia.</p>
      </div>
''' + video('video-c9-cc', '8Ec4Pgs8ClA',
            u'Qu&eacute; son y c&oacute;mo funcionan las licencias Creative Commons',
            u'Canal: &Aacute;rtica - Centro Cultural Online',
            u'Las mismas letras que acabamos de ver, contadas por gente que se dedica a esto. '
            u'Sirve para repasar antes de elegir la vuestra.')

S7_PRACTICA = ficha(
    u'Actividad 7 &middot; El paquete de entrega, hecho de verdad',
    [u'2.1', u'6.3', u'A.2', u'D.4'], u'Grupos de tres &middot; 20 min', u'''
          <h4>Se reparte el trabajo (1 min)</h4>
          <p>Uno hace el <b>esquema</b>, otro el <b>manual</b> y otro la <b>lista de piezas y la
             licencia</b>. En paralelo, que si no, no cabe.</p>
          <h4>Las tres piezas (14 min)</h4>
          <ul>
            <li><b>El esquema</b>, a mano y con regla o en Tinkercad: cada componente con su nombre,
                cada cable con el <b>pin</b> al que va, y la alimentaci&oacute;n se&ntilde;alada.
                Tiene que poderse montar mirando solo el papel.</li>
            <li><b>El manual</b>, una hoja y no m&aacute;s, con cuatro apartados: <i>qu&eacute;
                hace</i>, <i>c&oacute;mo se enciende y se usa</i>, <i>c&oacute;mo se cambia el
                umbral</i> y <i>qu&eacute; falla y c&oacute;mo se ve</i>. Escrito para alguien que no
                estaba.</li>
            <li><b>La lista de piezas</b> con referencia y sitio de compra, y debajo, en una sola
                l&iacute;nea, la <b>licencia</b> y el nombre de los tres autores.</li>
          </ul>
          <h4>La prueba, que es lo que de verdad eval&uacute;a (5 min)</h4>
          <p>Intercambiad los paquetes con otro grupo. El otro grupo tiene que poder decir, <b>sin
             preguntaros nada</b>:</p>
          <ol class="pasos">
            <li>qu&eacute; hace el aparato, en una frase;</li>
            <li>a qu&eacute; pin va el sensor;</li>
            <li>d&oacute;nde se compra la pieza m&aacute;s rara;</li>
            <li>y si <b>podr&iacute;an</b> publicar su versi&oacute;n modificada, y con qu&eacute;
                condiciones.</li>
          </ol>
          <p>Cada cosa que tengan que preguntaros es un agujero del paquete. Apuntadlas: esa lista
             es parte de la entrega.</p>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>El esquema, con todos los pines y la alimentaci&oacute;n <b>(3 puntos)</b>.</li>
            <li>El manual, con los cuatro apartados y en una hoja <b>(2 puntos)</b>.</li>
            <li>La lista de piezas, con referencias de verdad <b>(1 punto)</b>.</li>
            <li>La licencia, escrita entera y con los autores <b>(1 punto)</b>.</li>
            <li>Que el otro grupo conteste las cuatro preguntas sin ayuda <b>(2 puntos)</b>.</li>
            <li>La lista de agujeros que os han encontrado, apuntada sin excusas
                <b>(1 punto)</b>.</li>
          </ul>
''')

S7_CIERRE = u'''
      <ol>
      ''' + pregunta(u'Vuestro proyecto no lleva ninguna licencia. &iquest;Qu&eacute; puede hacer '
                     u'con &eacute;l quien lo encuentre dentro de tres a&ntilde;os?',
                     u'<p>Casi nada. Los derechos de autor <b>nacen solos</b> en cuanto se hace la '
                     u'obra, sin registrar nada, as&iacute; que lo que no dice nada tiene '
                     u'<b>todos los derechos reservados</b>. Puede mirarlo y copiarlo para s&iacute; '
                     u'mismo, pero no publicarlo ni repartir su versi&oacute;n. <b>Callarse es '
                     u'decir que no.</b></p>') + pregunta(
          u'&iquest;Qu&eacute; a&ntilde;ade el <b>SA</b> de CC BY-SA, y qu&eacute; cuesta?',
          u'<p>A&ntilde;ade que <b>la versi&oacute;n del siguiente se publica con la misma '
          u'licencia</b>, o sea que lo que salga de vuestro trabajo <b>sigue abierto</b> para el de '
          u'despu&eacute;s. Lo que cuesta es que le quita al siguiente la libertad de cerrar su '
          u'versi&oacute;n. Es una decisi&oacute;n con dos caras, y esta web la ha tomado: '
          u'm&iacute;rale el pie.</p>') + pregunta(
          u'&iquest;Por qu&eacute; el esquema vale m&aacute;s que una foto del montaje?',
          u'<p>Porque la foto dice <b>c&oacute;mo qued&oacute;</b> y el esquema dice <b>qu&eacute; '
          u'es</b>. El d&iacute;a que una pieza ya no se vende, el esquema sigue valiendo porque '
          u'dice qu&eacute; papel hac&iacute;a esa pieza y con qu&eacute; se puede sustituir. Con la '
          u'foto sola hay que adivinarlo.</p>') + pregunta(
          u'De todo el paquete, &iquest;cu&aacute;l es la cosa que anula a las dem&aacute;s si '
          u'falta?',
          u'<p><b>D&oacute;nde est&aacute; guardado</b>, y que ese sitio siga existiendo. Un '
          u'paquete impecable dentro de una cuenta que se borra cuando os vais, o en el '
          u'port&aacute;til de uno de vosotros, dentro de tres a&ntilde;os no existe. Cuesta cinco '
          u'minutos y vale m&aacute;s que las otras ocho cosas juntas.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">&Uacute;ltima sesi&oacute;n</span>
        Ya sab&eacute;is para qui&eacute;n es, cu&aacute;nto cuesta mantenerlo y c&oacute;mo se deja
        para que otro siga. Queda lo &uacute;nico que no se puede ensayar: <b>d&aacute;rselo</b>. Y
        ah&iacute; hay una palabra que no vale, y es la que dice todo el mundo:
        <i>&laquo;ya est&aacute;, funciona&raquo;</i>.
      </div>
'''


# ==========================================================================
# SESION 8 - Entregarlo de verdad
# ==========================================================================
S8_RETO = u'''
      <p>&Uacute;ltimo d&iacute;a. Dos grupos entregan su riego la misma tarde, en el mismo sitio y a
         la misma persona.</p>
      <div class="aviso">
        <span class="n-tag">Grupo 1</span>
        <i>&laquo;Ya est&aacute;. Funciona: lo hemos probado esta ma&ntilde;ana en el taller y va
        perfecto.&raquo;</i>
      </div>
      <div class="aviso">
        <span class="n-tag">Grupo 2</span>
        <i>&laquo;Acordamos esto hace dos semanas y lo hacemos ahora, delante de usted: ponemos la
        sonda en la maceta seca y en menos de dos minutos la bomba tiene que echar <b>entre 80 y 120
        mililitros</b> &mdash;lo medimos en este vaso&mdash; y el LED tiene que ponerse verde. Lo
        repetimos <b>tres veces</b> y tienen que salir <b>dos</b>. Si no salen, nos lo llevamos y
        volvemos el martes con el problema resuelto.&raquo;</i>
      </div>
      <div class="reto-piensa">
        <span class="n-tag">Dos preguntas, y la segunda es la buena</span>
        <p>La f&aacute;cil: <b>&iquest;cu&aacute;l de los dos grupos se va a casa con el aparato
           debajo del brazo?</b></p>
        <p style="margin-top:7px">La de verdad: <b>&iquest;cu&aacute;l de los dos duerme mejor esta
           noche?</b> Y sobre todo, &iquest;qu&eacute; pasa dentro de un mes, cuando la planta se
           seque, en cada uno de los dos casos?</p>
      </div>
      <p>El grupo 1 no ha mentido. El problema de <i>&laquo;funciona&raquo;</i> es otro: <b>no se
         puede comprobar</b>. Y lo que no se puede comprobar no se puede cerrar, as&iacute; que se
         queda abierto para siempre. Dentro de un mes, cuando algo falle, la conversaci&oacute;n
         ser&aacute; <i>&laquo;pues a m&iacute; no me funciona&raquo;</i> contra <i>&laquo;pues a
         nosotros s&iacute;&raquo;</i>, y esa no la gana nadie.</p>
'''

S8_TEORIA = u'''
      <p>Lo que hizo el grupo 2 tiene nombre, y se usa igual en una obra, en un hospital y en un
         programa de ordenador.</p>
      <div class="copiar">
        <h4>La prueba de aceptaci&oacute;n</h4>
        <p>Es la prueba que decide si lo entregado <b>se acepta o no se acepta</b>. Lleva cinco
           cosas, y si le falta una no sirve:</p>
        <ol>
          <li><b>Qu&eacute; se mide</b>, con su unidad. Mililitros, segundos, lux.</li>
          <li><b>Con qu&eacute; se mide.</b> Este vaso, este cron&oacute;metro, este term&oacute;metro.
              Si la medida depende del aparato de medir, se dice cu&aacute;l.</li>
          <li><b>Entre qu&eacute; y qu&eacute;</b> se considera bien. Una <b>banda</b>, no un
              n&uacute;mero exacto: ninguna medida sale dos veces igual.</li>
          <li><b>Cu&aacute;ntas veces</b> se repite y <b>cu&aacute;ntas</b> tienen que salir.</li>
          <li><b>Qui&eacute;n est&aacute; delante</b> cuando se hace.</li>
        </ol>
        <p>Y dos condiciones que no son parte de la prueba pero la sostienen:</p>
        <ul>
          <li>se <b>acuerda antes</b> de construir el aparato, o por lo menos antes de terminarlo;</li>
          <li>est&aacute; escrito <b>qu&eacute; se hace si no pasa</b>.</li>
        </ul>
      </div>
      <div class="copiar">
        <h4>Una prueba tiene que poder fallar</h4>
        <p><i>&laquo;Encendemos el aparato y se enciende&raquo;</i> no es una prueba: es un
           tr&aacute;mite, porque no hay ning&uacute;n aparato de la clase que pueda suspenderla.</p>
        <p>La regla, y es la que separa una prueba de un adorno: <b>si no te imaginas
           suspendi&eacute;ndola, no est&aacute;s comprobando nada</b>.</p>
      </div>
      <p>Ahora lo interesante. Una prueba se puede apretar o aflojar, y no da igual. En la escena
         est&aacute;n las tres pruebas del curso; empieza por la del riego, tal y como la dijo el
         grupo 2 pero exigiendo que salgan <b>las tres de tres</b>.</p>
''' + ACEPTACION + u'''
      <div class="copiar">
        <h4>Lo que acaba de pasar, y es lo m&aacute;s &uacute;til de la sesi&oacute;n</h4>
        <p>Con la banda de 80 a 120 mL y un aparato que de verdad echa 100 de media, <b>una medida
           suelta cae dentro el 73 % de las veces</b>. Parece mucho. Pero si exiges que salgan
           <b>tres de tres</b>, la probabilidad de aprobar es 0,73 &times; 0,73 &times; 0,73:
           <b>el 39 %</b>. O sea que un aparato que est&aacute; bien suspende <b>seis de cada
           diez</b> entregas.</p>
        <p>Cambia a <b>dos de tres</b>, sin tocar nada m&aacute;s: aprueba el <b>82 %</b>. Y el
           aparato malo &mdash;el que echa 55 mL&mdash; sigue suspendiendo: aprueba el <b>2 %</b>.
           <b>Esa es la prueba que hay que acordar</b>, y no se encuentra a ojo: se calcula.</p>
        <p>Consecuencia contraintuitiva: <b>cada repetici&oacute;n que a&ntilde;ades exigiendo que
           salgan todas te lo pone m&aacute;s dif&iacute;cil a ti</b>, no al aparato.</p>
      </div>
      <div class="copiar">
        <h4>Las dos maneras de equivocarse</h4>
        <ul>
          <li><b>Suspender algo que est&aacute; bien.</b> La banda es demasiado estrecha para lo que
              var&iacute;a la medida, o pides demasiadas repeticiones seguidas. Te llevas a casa un
              aparato que serv&iacute;a.</li>
          <li><b>Aprobar algo que est&aacute; mal.</b> La banda es tan ancha que la pasa cualquier
              cosa. Entregas un aparato que no sirve, y encima con un papel firmado.</li>
        </ul>
        <p>Y lo importante: <b>estrechar la banda cambia una por la otra</b>. No existe la prueba
           perfecta. Existe la prueba <b>acordada</b>, que es la que las dos partes han mirado antes
           sabiendo lo que les jugaban.</p>
      </div>
      <div class="copiar">
        <h4>El acta de entrega: una hoja y dos firmas</h4>
        <ol>
          <li><b>Qu&eacute; se entrega.</b> El aparato, el manual, el esquema, las piezas de
              repuesto que sobran y d&oacute;nde est&aacute; todo lo dem&aacute;s. Esto es la
              sesi&oacute;n 7.</li>
          <li><b>A qui&eacute;n</b>, con nombre, y en qu&eacute; fecha.</li>
          <li><b>Qu&eacute; prueba se ha hecho</b> y <b>qu&eacute; ha salido</b>: los n&uacute;meros
              de las tres repeticiones, no &laquo;correcto&raquo;.</li>
          <li><b>Qu&eacute; queda pendiente</b>, si queda algo, <b>y para cu&aacute;ndo</b>.</li>
          <li><b>Qui&eacute;n lo mantiene</b> y cada cu&aacute;nto. Esto es la sesi&oacute;n 6.</li>
          <li><b>Las dos firmas.</b> Que no son un formalismo: son las dos personas diciendo que
              han visto lo mismo.</li>
        </ol>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>&iquest;En qu&eacute; se diferencia esto de la defensa de la sesi&oacute;n 3? En casi
           todo. All&iacute; hay un <b>tribunal</b> que os pone una nota y se va; aqu&iacute; hay una
           <b>persona</b> que se lleva el aparato a su sitio y se queda con &eacute;l. La defensa
           <b>termina</b> cuando acaban los seis minutos. La entrega <b>empieza</b> ah&iacute;: a
           partir de la firma, el aparato es de otro y lo que falle lo sufre &eacute;l.</p>
        <p>Por eso la entrega no se puntúa con una r&uacute;brica de exposici&oacute;n: se comprueba
           con una medida.</p>
      </div>
''' + foto('c9-inspeccion.jpg',
           u'Una mujer con bata blanca mira por un microscopio de laboratorio una pieza colocada '
           u'bajo el objetivo, en una sala llena de puestos iguales',
           u'<b>Control de calidad</b> en una f&aacute;brica de circuitos integrados, hacia los '
           u'a&ntilde;os setenta. Su trabajo no es fabricar: es <b>poder decir que no</b>. Y para '
           u'que eso signifique algo tiene que haber escrito <b>de antemano</b> qu&eacute; se mira y '
           u'a partir de qu&eacute; se rechaza; si no, lo que hay es una opini&oacute;n con '
           u'microscopio. F&iacute;jate adem&aacute;s en algo que suele pasar desapercibido: quien '
           u'comprueba <b>no es quien lo ha hecho</b>. En vuestra entrega, ese alguien distinto es '
           u'el destinatario, y por eso la prueba se hace delante de &eacute;l.',
           u'Intel Free Press', u'CC BY 2.0',
           u'https://commons.wikimedia.org/wiki/File:Quality_Inspection.jpg') + u'''
      <div class="copiar">
        <h4>Y si no pasa la prueba, &iquest;qu&eacute;?</h4>
        <p>Hay tres salidas honradas, y se eligen delante de la persona:</p>
        <ol>
          <li><b>Nos lo llevamos y volvemos con fecha.</b> La mejor, si hay tiempo. Se apunta el
              d&iacute;a.</li>
          <li><b>Se entrega con una limitaci&oacute;n escrita.</b> <i>&laquo;Echa 70 mL en vez de
              100: riega bien las macetas peque&ntilde;as y no llega para la grande.&raquo;</i>
              Vale, pero tiene que estar en el acta y la persona tiene que decir que le sirve
              as&iacute;.</li>
          <li><b>No se entrega.</b> Tambi&eacute;n es un resultado, y es mucho mejor que entregar
              algo que va a fallar en su casa.</li>
        </ol>
        <p>Y una salida deshonrada, que hay que saber reconocer porque es la m&aacute;s tentadora:
           <b>cambiar la prueba despu&eacute;s de verla fallar</b>. Ensanchar la banda de 80-120 a
           50-150 cuando ya sabes que has echado 60. Eso no es aprobar: es borrar el examen.</p>
      </div>

      <h3>Lo que queda cuando os vais</h3>
      <p>Esta unidad ha ido quitando capas. Empez&oacute; con qui&eacute;n decide qu&eacute; se
         fabrica, sigui&oacute; con si encaja en el sitio, con c&oacute;mo se cuenta y con
         cu&aacute;nto cuesta. Y las cuatro &uacute;ltimas sesiones han sido una sola pregunta partida
         en cuatro: <b>&iquest;esto le sirve a alguien de verdad, cuando nosotros ya no
         estemos?</b></p>
      <div class="copiar">
        <h4>Las cuatro, en una frase cada una</h4>
        <ol>
          <li><b>Para qui&eacute;n:</b> un requisito es una frase que se puede comprobar, y la pone
              una persona con nombre.</li>
          <li><b>Mantenerlo:</b> el mantenimiento no se decide manteniendo, se decide
              dise&ntilde;ando.</li>
          <li><b>Continuarlo:</b> lo que no dejas escrito lo paga el siguiente en horas, y sin
              licencia ni siquiera puede empezar.</li>
          <li><b>Entregarlo:</b> &laquo;funciona&raquo; no se puede comprobar; una banda, tres
              repeticiones y una firma, s&iacute;.</li>
        </ol>
        <p>Si dentro de diez a&ntilde;os solo te queda una frase de las cuatro, que sea esta:
           <b>un proyecto no termina cuando funciona, termina cuando funciona en manos de otro</b>.</p>
      </div>
'''

S8_PRACTICA = ficha(
    u'Actividad 8 &middot; La prueba, el acta, y la entrega delante de alguien',
    [u'2.1', u'6.1', u'6.3', u'D.4'], u'Grupos de tres &middot; 15 min', u'''
          <h4>Primera parte &middot; la prueba, calculada (7 min)</h4>
          <ol class="pasos">
            <li>Escribid <b>qu&eacute; promet&eacute;is</b>, en una frase con un n&uacute;mero y su
                unidad. Una sola cosa, la m&aacute;s importante para vuestro destinatario.</li>
            <li>Decid <b>con qu&eacute;</b> se mide y d&oacute;nde exactamente (&laquo;el vaso
                medidor del taller&raquo;, &laquo;el lux&oacute;metro del m&oacute;vil, apoyado en el
                centro de la mesa&raquo;).</li>
            <li>Con la escena, buscad la <b>banda y el n&uacute;mero de repeticiones</b> con los que
                un aparato bueno apruebe <b>por encima del 80 %</b> y uno malo <b>por debajo del
                20 %</b>. Copiad las dos probabilidades.</li>
            <li>Escribid las <b>tres salidas</b> por si no pasa, y decid cu&aacute;l elegir&iacute;ais
                vosotros y por qu&eacute;.</li>
          </ol>
          <h4>Segunda parte &middot; el acta, y la entrega (8 min)</h4>
          <p>Una hoja con los seis apartados de la libreta. Y despu&eacute;s, la entrega de verdad:
             otro grupo hace de destinatario con la ficha de la sesi&oacute;n 5.</p>
          <ul>
            <li>Le le&eacute;is la prueba <b>antes</b> de hacerla, y &eacute;l tiene derecho a decir
                que no le vale y a pedir otra cosa. Negociadla.</li>
            <li>Se hace delante, con las repeticiones acordadas, y se <b>apuntan los
                n&uacute;meros</b>, salgan como salgan.</li>
            <li>Se rellena el acta y se firma. Si no ha pasado, se escribe cu&aacute;l de las tres
                salidas y con qu&eacute; fecha.</li>
          </ul>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Lo que promet&eacute;is, en una frase con n&uacute;mero y unidad
                <b>(1 punto)</b>.</li>
            <li>Con qu&eacute; se mide y d&oacute;nde, sin ambig&uuml;edad <b>(1 punto)</b>.</li>
            <li>La banda y las repeticiones, con las dos probabilidades copiadas de la escena
                <b>(2 puntos)</b>.</li>
            <li>Que la prueba <b>pueda suspender</b>: el aparato malo por debajo del 20 %
                <b>(1 punto)</b>.</li>
            <li>El acta con los seis apartados <b>(2 puntos)</b>.</li>
            <li>Los n&uacute;meros de las repeticiones apuntados tal cual, sin maquillar
                <b>(2 puntos)</b>.</li>
            <li>La salida elegida si no pasa, con fecha <b>(1 punto)</b>.</li>
          </ul>
''')

PREGUNTAS_TEST_B = [
    dict(p=u'Entre 1975 y 1999, de 1.393 medicamentos nuevos solo 16 fueron para enfermedades '
           u'tropicales. &iquest;Qu&eacute; lo decidi&oacute;?',
         op=[u'Una decisi&oacute;n pol&iacute;tica tomada en una reuni&oacute;n.',
             u'Una divisi&oacute;n: el precio m&iacute;nimo no cab&iacute;a en lo que puede pagar '
             u'quien lo sufre.',
             u'Que a&uacute;n no se sab&iacute;a c&oacute;mo fabricarlos.'],
         ok=1,
         por=u'Precio m&iacute;nimo = coste de desarrollo &divide; (personas que lo '
             u'comprar&aacute;n &times; a&ntilde;os de venta). Si no cabe, no se fabrica, y no hace '
             u'falta que nadie lo decida.'),
    dict(p=u'&iquest;Qu&eacute; quiere decir que una tecnolog&iacute;a sea <b>apropiada</b>?',
         op=[u'Que es lo m&aacute;s sencilla posible.',
             u'Que encaja con la energ&iacute;a, los materiales, las manos y el dinero del sitio '
             u'donde va a vivir.',
             u'Que ha pasado los controles de calidad.'],
         ok=1,
         por=u'Es una <b>relaci&oacute;n</b> entre el aparato y el sitio, no una categor&iacute;a '
             u'del aparato. La PlayPump fall&oacute; por eso, no por falta de dinero.'),
    dict(p=u'En la r&uacute;brica de la defensa, &iquest;cu&aacute;nto vale &laquo;c&oacute;mo lo '
           u'montamos, paso a paso&raquo;?',
         op=[u'Es lo que m&aacute;s vale.', u'Vale 1 punto.', u'Vale 0.'],
         ok=2,
         por=u'Cero: 6,5 de los 10 puntos son de lo que el aparato hace por alguien. Por eso el '
             u'mismo proyecto saca 4,17 con un gui&oacute;n y 9,67 con otro.'),
    dict(p=u'&laquo;Nuestro riego es para el instituto, para ahorrar agua.&raquo; '
           u'&iquest;Qu&eacute; le falta a esa frase?',
         op=[u'Nada: dice para qui&eacute;n es y para qu&eacute; sirve.',
             u'Una persona concreta dentro, y un n&uacute;mero que se pueda comprobar.',
             u'Decir cu&aacute;nto ha costado el material.'],
         ok=1,
         por=u'El instituto no riega, no se olvida y no se va de vacaciones. Sin alguien con '
             u'nombre no hay requisitos, y sin requisitos no hay manera de saber si sirve.'),
    dict(p=u'&iquest;Cu&aacute;l de estas tres frases es un <b>requisito</b>?',
         op=[u'&laquo;Que sea fiable.&raquo;',
             u'&laquo;Que quede bonito.&raquo;',
             u'&laquo;Que aguante 43 d&iacute;as sin que vaya nadie.&raquo;'],
         ok=2,
         por=u'Lleva n&uacute;mero, unidad y una manera de comprobarlo: el 15 de septiembre se mira '
             u'la planta. Las otras dos son deseos: no hay forma de saber si se cumplen.'),
    dict(p=u'El mismo riego cumple con la vecina (15 d&iacute;as) y suspende en el huerto '
           u'(43 d&iacute;as). &iquest;Por qu&eacute;?',
         op=[u'Porque el aparato del huerto est&aacute; peor montado.',
             u'Porque el bancal pide 6 L al d&iacute;a y 43 d&iacute;as son 258 litros, que no caben '
             u'en ning&uacute;n dep&oacute;sito que puedan poner.',
             u'Porque en el huerto hace m&aacute;s calor y las pilas duran menos.'],
         ok=1,
         por=u'Es el mismo aparato. Lo que cambia es el requisito, y lo pone la persona. Cuando el '
             u'mando no da para tanto, lo que hay que cambiar es el <b>dise&ntilde;o</b>: una toma '
             u'de agua y un enchufe.'),
    dict(p=u'Se come uno de los dos clavos de la sonda de humedad y el otro no. '
           u'&iquest;Por qu&eacute;?',
         op=[u'Porque el clavo era de peor calidad.',
             u'Por <b>electr&oacute;lisis</b>: pasar corriente continua por tierra mojada disuelve '
             u'el electrodo positivo.',
             u'Porque le da el sol a ese lado.'],
         ok=1,
         por=u'Le pasa a cualquier sonda de dos clavos alimentada todo el rato. Se arregla '
             u'aliment&aacute;ndola solo al medir, o con una sonda capacitiva.'),
    dict(p=u'&iquest;Cu&aacute;l de estas decisiones sube m&aacute;s la disponibilidad del riego a '
           u'cinco a&ntilde;os?',
         op=[u'Que quien lo cuida vaya m&aacute;s deprisa cuando se entera.',
             u'Enchufarlo, poner un dep&oacute;sito grande y una sonda que dure.',
             u'Comprar dos recambios de cada pieza.'],
         ok=1,
         por=u'Las tres primeras son de <b>dise&ntilde;o</b>, y llevan el aparato del 7 % al 98 % del '
             u'tiempo funcionando. El mantenimiento no se decide manteniendo, se decide '
             u'dise&ntilde;ando.'),
    dict(p=u'Dej&aacute;is el proyecto sin poner ninguna licencia. &iquest;Qu&eacute; pasa?',
         op=[u'Que al no decir nada, cualquiera puede hacer con &eacute;l lo que quiera.',
             u'Que tiene <b>todos los derechos reservados</b>: nadie puede publicarlo ni continuarlo '
             u'legalmente.',
             u'Que hay que registrarlo antes de que tenga derechos.'],
         ok=1,
         por=u'Los derechos de autor nacen solos al crear la obra, sin registrar nada. Para el '
             u'derecho, <b>callarse es decir que no</b>. Poner la licencia es dar permiso por '
             u'escrito.'),
    dict(p=u'Prometes 100 mL, la banda es de 80 a 120 y una medida cae dentro el 73 % de las veces. '
           u'Si exiges <b>tres de tres</b>, &iquest;cu&aacute;ntas veces apruebas?',
         op=[u'El 73 %, igual que una sola medida.',
             u'El 39 %: 0,73 &times; 0,73 &times; 0,73.',
             u'M&aacute;s del 73 %, porque tienes tres oportunidades.'],
         ok=1,
         por=u'Cada repetici&oacute;n que exiges que salga te lo pone m&aacute;s dif&iacute;cil a ti, '
             u'no al aparato. Con <b>dos de tres</b> subes al 82 % y el aparato malo sigue '
             u'suspendiendo: aprueba solo el 2 %.'),
]

S8_CIERRE = u'''
      <ol>
      ''' + pregunta(u'&iquest;Por qu&eacute; &laquo;ya est&aacute;, funciona&raquo; no es una '
                     u'entrega?',
                     u'<p>Porque <b>no se puede comprobar</b>, y lo que no se puede comprobar no se '
                     u'puede cerrar. Dentro de un mes, cuando algo falle, la conversaci&oacute;n '
                     u'ser&aacute; &laquo;a m&iacute; no me funciona&raquo; contra &laquo;a nosotros '
                     u's&iacute;&raquo;, y esa discusi&oacute;n no la gana nadie. Una banda, unas '
                     u'repeticiones y una firma s&iacute; se pueden comprobar.</p>') + pregunta(
          u'Nombra las cinco cosas que lleva una prueba de aceptaci&oacute;n.',
          u'<p><b>Qu&eacute;</b> se mide con su unidad, <b>con qu&eacute;</b> se mide, <b>entre '
          u'qu&eacute; y qu&eacute;</b> se da por bueno, <b>cu&aacute;ntas veces</b> se repite y '
          u'cu&aacute;ntas tienen que salir, y <b>qui&eacute;n est&aacute; delante</b>. Y dos '
          u'condiciones: se acuerda <b>antes</b>, y est&aacute; escrito qu&eacute; se hace si no '
          u'pasa.</p>') + pregunta(
          u'&iquest;Por qu&eacute; exigir m&aacute;s repeticiones seguidas os perjudica a vosotros?',
          u'<p>Porque las probabilidades se multiplican. Si una medida cae dentro el 73 % de las '
          u'veces, tres seguidas son 0,73&sup3; = <b>39 %</b>: un aparato que est&aacute; bien '
          u'suspende seis de cada diez entregas. Exigiendo <b>dos de tres</b> sube al 82 % y el '
          u'aparato malo sigue fuera. Eso no se acierta a ojo: se calcula.</p>') + pregunta(
          u'La prueba falla delante del destinatario. &iquest;Qu&eacute; se puede hacer y '
          u'qu&eacute; no?',
          u'<p>Se puede: <b>llev&aacute;rselo y volver con fecha</b>; <b>entregarlo con una '
          u'limitaci&oacute;n escrita</b> que la persona acepte; o <b>no entregarlo</b>, que '
          u'tambi&eacute;n es un resultado. Lo que no se puede es <b>cambiar la prueba '
          u'despu&eacute;s de verla fallar</b>: ensanchar la banda cuando ya sabes el resultado no '
          u'es aprobar, es borrar el examen.</p>') + u'''
      </ol>
''' + test('c9b', u'Lo que tiene que haber quedado de la unidad entera', PREGUNTAS_TEST_B) + u'''
      <div class="nota">
        <span class="n-tag">Y con esto se acaba</span>
        Ocho sesiones para una idea sola, que no se parece en nada a la que ten&iacute;ais en
        septiembre: <b>hacer que funcione es la mitad f&aacute;cil</b>. La otra mitad es que le
        sirva a alguien, que siga vivo cuando os vay&aacute;is, que otro pueda seguir y que
        hay&aacute;is dejado por escrito c&oacute;mo se comprueba. Dentro de un mes id a ver
        vuestro aparato: ah&iacute; est&aacute; la nota de verdad.
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
      bloque('01', u'Teor&iacute;a &middot; 25 min', S8_TEORIA) +
      bloque('02', u'Pr&aacute;ctica &middot; 15 min', S8_PRACTICA) +
      bloque('03', u'Cierre y test &middot; 10 min', S8_CIERRE))

MIN = [(u"10'", u'Reto'), (u"25'", u'Teor&iacute;a'), (u"20'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')]
MIN_TEST = [(u"10'", u'Reto'), (u"25'", u'Teor&iacute;a'), (u"15'", u'Pr&aacute;ctica'),
            (u"10'", u'Cierre y test')]

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
         minutado=MIN_TEST,
         chips=[u'CE6 &middot; 6.2', u'CE6 &middot; 6.3', u'D.2', u'D.3', u'D.4'], cuerpo=S4),
    dict(corto=u'Para qui&eacute;n, exactamente',
         titulo=u'&laquo;Ser&iacute;a &uacute;til&raquo; no es un requisito; quince d&iacute;as de '
                u'agosto s&iacute;',
         entradilla=u'Se pasa de &laquo;esto le viene bien a todo el mundo&raquo; a la lista de una '
                    u'persona con nombre. Se entrevista, se anota entre comillas y se convierte en '
                    u'n&uacute;meros.',
         minutado=MIN,
         chips=[u'CE6 &middot; 6.1', u'CE6 &middot; 6.3', u'D.1', u'D.4'], cuerpo=S5),
    dict(corto=u'Lo que cuesta mantenerlo',
         titulo=u'Lo que se rompe primero es lo que nadie sab&iacute;a que hab&iacute;a que hacer',
         entradilla=u'No el impacto ambiental, sino la vida &uacute;til en manos de otro: qui&eacute;n '
                    u'cambia la pila, d&oacute;nde est&aacute; el recambio y qu&eacute; pasa cuando '
                    u'vosotros ya no est&aacute;is.',
         minutado=MIN,
         chips=[u'CE6 &middot; 6.2', u'CE6 &middot; 6.3', u'D.2', u'D.3'], cuerpo=S6),
    dict(corto=u'Que otro lo pueda continuar',
         titulo=u'Dentro de tres a&ntilde;os alguien abre la caja: &iquest;qu&eacute; encuentra?',
         entradilla=u'Manual, esquema y licencia. Lo que cuesta escribirlo, lo que le ahorra al '
                    u'siguiente, y por qu&eacute; &laquo;no poner nada&raquo; no significa '
                    u'&laquo;es de todos&raquo;.',
         minutado=MIN,
         chips=[u'CE2 &middot; 2.1', u'CE6 &middot; 6.3', u'A.2', u'D.4'], cuerpo=S7),
    dict(corto=u'Entregarlo de verdad',
         titulo=u'&laquo;Funciona&raquo; no es una entrega; entre 80 y 120 mililitros, s&iacute;',
         entradilla=u'La prueba de aceptaci&oacute;n, acordada de antemano y hecha delante de quien '
                    u'lo recibe. Y qu&eacute; se hace, por escrito, si no pasa.',
         minutado=MIN_TEST,
         chips=[u'CE2 &middot; 2.1', u'CE6 &middot; 6.1', u'CE6 &middot; 6.3', u'D.4'], cuerpo=S8),
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
         u'apropiada, c&oacute;mo se defiende un proyecto, cu&aacute;ndo devuelve lo que '
         u'cost&oacute; hacerlo, c&oacute;mo se sacan requisitos de una persona concreta, '
         u'qu&eacute; cuesta mantenerlo cinco a&ntilde;os, c&oacute;mo se documenta con licencia '
         u'libre y c&oacute;mo se entrega con una prueba de aceptaci&oacute;n.',
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
