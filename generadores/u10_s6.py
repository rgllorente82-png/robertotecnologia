# -*- coding: utf-8 -*-
"""2.o TyD - Tema 10 - Sesion 6: proyecto, rubrica y test.

Cierra la unidad y cierra el curso. El proyecto no es "haz algo con la
micro:bit": es buscar un problema de verdad del entorno del alumno y montar el
aparato que lo resuelve, con la misma estructura de las dos sesiones
anteriores (entrada, decision, salida) y con el umbral JUSTIFICADO con
medidas propias.

La escena del dia (u10_escenas2.DIA) recorre los 1.440 minutos de un dia,
calcula la luz de cada minuto y ejecuta encima las tres estrategias de
encendido. Sirve para lo unico que le falta a un proyecto de clase: decidir
si merece la pena, con numeros.

El test se corrige en la propia pagina (generadores/test_auto.py) y explica
SIEMPRE por que, tambien en las que se aciertan.
"""
from unidad_base import bloque, ficha, pregunta
from test_auto import test
from u10_escenas2 import DIA

# --------------------------------------------------------------------------
# 00 - El proyecto
# --------------------------------------------------------------------------
PROYECTO = u'''
      <p>&Uacute;ltima sesi&oacute;n del tema y del curso. Y el encargo no lo pongo yo:</p>
      <div class="aviso">
        <span class="n-tag">El encargo</span>
        Busca <b>una cosa de tu casa o de tu instituto que no funcione bien porque depende de que
        alguien se acuerde</b>, y monta el aparato que se acuerde por &eacute;l.
      </div>
      <p>&laquo;Que alguien se acuerde&raquo; es la pista. Las luces del pasillo que se quedan
         encendidas toda la noche. El grifo que alguien deja abierto. La planta que se seca porque
         nadie la riega. La puerta del aula que se queda abierta con la calefacci&oacute;n puesta. Todo
         eso son automatismos que faltan.</p>
      <div class="copiar">
        <h4>Lo que tiene que tener tu montaje, sin excepci&oacute;n</h4>
        <ol>
          <li>Una <b>entrada</b>: un sensor que mida algo del mundo. No vale un bot&oacute;n, porque
              entonces vuelve a depender de que alguien se acuerde.</li>
          <li>Una <b>decisi&oacute;n</b>: al menos un condicional, con su <b>umbral</b>.</li>
          <li>Una <b>salida</b>: algo que se vea, se oiga o se mueva.</li>
          <li>El umbral <b>justificado con medidas vuestras</b>, anotadas en la libreta. Tres
              medidas m&iacute;nimo, de sitios distintos.</li>
        </ol>
      </div>
      <h3>Seis que caben en una sesi&oacute;n</h3>
      <p>Si no se os ocurre nada, de aqu&iacute;. Los seis se montan con lo que ya sab&eacute;is.</p>
      <div class="copiar">
        <h4>Ideas con su entrada y su salida</h4>
        <ul>
          <li><b>Aviso de planta seca.</b> Dos clavos clavados en la maceta, uno al <b>3V</b> y otro
              a <b>P1</b>, y una resistencia de 10&nbsp;k&Omega; de P1 a GND: el <b>mismo divisor</b>
              que la LDR, pero con la tierra haciendo de resistencia. Mojada conduce y seca no. Sale
              una cara triste cuando hay que regar.</li>
          <li><b>Cartel de aula libre.</b> Sensor de luz: si la clase est&aacute; a oscuras, muestra
              &laquo;LIBRE&raquo;; si hay luz, &laquo;OCUPADA&raquo;.</li>
          <li><b>Medidor de ruido de clase.</b> Micr&oacute;fono, y una barra de LED que sube. Por encima
              de vuestro umbral, una cara enfadada.</li>
          <li><b>Aviso de ventana abierta en invierno.</b> Term&oacute;metro: por debajo de vuestro
              umbral, flecha abajo y pitido.</li>
          <li><b>Cuentapasos de mochila.</b> Aceler&oacute;metro: cuenta sacudidas y muestra el
              n&uacute;mero.</li>
          <li><b>Alarma de caj&oacute;n.</b> Se deja a oscuras dentro del caj&oacute;n; si alguien lo abre,
              entra luz, y suena.</li>
        </ul>
      </div>
      <figure class="foto">
        <img src="../../../img/u10-sensor.jpg" width="1200" height="676" loading="lazy"
             alt="Placa microcontroladora unida por cables de colores a una placa de pruebas con un sensor de temperatura y humedad">
        <figcaption>Las tres piezas en una foto: la <b>placa</b> que decide, el <b>sensor</b> que se entera de lo que pasa y los cables que los unen. No hay m&aacute;s. Con esto y veinte l&iacute;neas de programa ya tienes un aparato que hace algo solo cuando cambia algo de tu casa.
          <br><br>Foto de <b>Bmonster Lab</b> en Pexels. Es de su autor y no forma parte del material
          publicado bajo la licencia de esta p&aacute;gina.</figcaption>
      </figure>

      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>F&iacute;jate en que los seis son <b>el mismo programa</b>: medir, comparar con un umbral,
           actuar. Lo &uacute;nico que cambia es qu&eacute; sensor y qu&eacute; salida. Eso es lo que de verdad
           te llevas del tema: no seis montajes, sino <b>un esqueleto</b> que sirve para los seis y
           para los que se te ocurran.</p>
      </div>
'''

# --------------------------------------------------------------------------
# 01 - Merece la pena, y la rubrica
# --------------------------------------------------------------------------
MERECE = u'''
      <p>Falta lo que casi nadie hace y separa un montaje de un proyecto: <b>comprobar que la
         soluci&oacute;n es mejor que no hacer nada</b>. Y eso son n&uacute;meros.</p>
      <p>Aqu&iacute; tienes un d&iacute;a entero, minuto a minuto, y las tres maneras de encender una farola:
         dejarla siempre encendida, ponerle un horario o ponerle un sensor como el tuyo. Mueve tu
         umbral y mira la tabla.</p>
''' + DIA + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Con el d&iacute;a despejado el <b>reloj</b> parece la mejor opci&oacute;n: es el que menos gasta.
           Pero mira la &uacute;ltima columna: deja m&aacute;s de <b>hora y media</b> de calle a oscuras todos
           los d&iacute;as, y el sensor no deja ni un minuto. Un automatismo no se juzga solo por lo que ahorra,
           sino por <b>el servicio que da</b>.</p>
        <p>Y ahora pulsa <b>d&iacute;a de tormenta</b>. El reloj se hunde: deja m&aacute;s de <b>cinco
           horas</b> sin luz, porque a las dos de la tarde no ve&iacute;a nada y el horario dec&iacute;a que
           era de d&iacute;a. El sensor, que no sabe qu&eacute; hora es, acierta igual que siempre. Es la
           misma raz&oacute;n de la sesi&oacute;n 4, ahora con la cuenta hecha.</p>
        <p>Cambia tambi&eacute;n la potencia de la bombilla y el precio del kWh: son los dos datos que
           t&uacute; pondr&iacute;as de tu factura. Todo lo dem&aacute;s lo recalcula la p&aacute;gina.</p>
      </div>
      <div class="copiar">
        <h4>Las tres preguntas que cierran cualquier proyecto</h4>
        <ol>
          <li>&iquest;<b>Funciona</b>? Se demuestra ense&ntilde;&aacute;ndolo, no cont&aacute;ndolo.</li>
          <li>&iquest;Es <b>mejor</b> que no hacer nada? Se demuestra con dos n&uacute;meros comparados.</li>
          <li>&iquest;Qu&eacute; pasa cuando algo <b>falla</b>? Qu&eacute; hace tu aparato si se acaba la pila
              o el sensor se ensucia.</li>
        </ol>
      </div>
''' + ficha(
    u'Actividad 6 &middot; Tu automatismo',
    [u'5.1', u'5.3', u'C.3', u'C.4'], u'Grupos de 3 &middot; evaluable sobre 10', u'''
          <h4>Qu&eacute; se entrega</h4>
          <ol class="pasos">
            <li>El <b>montaje</b> funcionando, aunque sea en el simulador de MakeCode.</li>
            <li>Una <b>hoja</b> con: el problema en una frase, el esquema de entrada &rarr;
                decisi&oacute;n &rarr; salida, las <b>tres medidas</b> con las que hab&eacute;is elegido el
                umbral y el programa en bloques (captura o dibujo).</li>
            <li>Una <b>demostraci&oacute;n</b> de dos minutos delante de la clase, provocando el
                cambio a mano: tapando el sensor, soplando, agitando.</li>
          </ol>
          <h4>R&uacute;brica</h4>
          <table class="rubrica">
            <tr><th>Qu&eacute; se mira</th><th>Bien (todo)</th><th>Regular (la mitad)</th><th>Mal (cero)</th><th>Puntos</th></tr>
            <tr><td>El problema es real y est&aacute; bien contado</td>
                <td>Una frase clara, y se entiende a qui&eacute;n le pasa</td>
                <td>Se entiende pero es un invento de clase</td>
                <td>No hay problema: hay un cacharro</td><td><b>2</b></td></tr>
            <tr><td>Entrada, decisi&oacute;n y salida</td>
                <td>Las tres, y el sensor no es un bot&oacute;n</td>
                <td>Falta una o la entrada es un bot&oacute;n</td>
                <td>Solo hace un dibujito al iniciar</td><td><b>2</b></td></tr>
            <tr><td>El umbral, justificado</td>
                <td>Tres medidas propias y una raz&oacute;n</td>
                <td>Hay medidas pero el umbral no sale de ellas</td>
                <td>Un n&uacute;mero copiado</td><td><b>2</b></td></tr>
            <tr><td>Funciona delante de la clase</td>
                <td>Responde al cambio y vuelve atr&aacute;s</td>
                <td>Responde a veces</td>
                <td>No responde</td><td><b>2</b></td></tr>
            <tr><td>Sab&eacute;is explicar qu&eacute; hace y qu&eacute; falla</td>
                <td>Explic&aacute;is el bucle y una situaci&oacute;n en que fallar&iacute;a</td>
                <td>Explic&aacute;is lo que hace pero no d&oacute;nde falla</td>
                <td>Le&eacute;is el programa en voz alta</td><td><b>2</b></td></tr>
          </table>
          <div class="nota">
            <span class="n-tag">Lo que m&aacute;s puntos da y menos cuesta</span>
            La tercera fila. Tres medidas anotadas en la libreta son cinco minutos de trabajo y son
            lo que separa un proyecto de tecnolog&iacute;a de una manualidad.
          </div>
''') + u'''
      <style>
      table.rubrica{width:100%;border-collapse:collapse;font-size:13.5px;margin:10px 0}
      table.rubrica th,table.rubrica td{border:1px solid var(--line);padding:7px 9px;
        vertical-align:top;text-align:left}
      table.rubrica th{background:var(--surface-2);font-family:var(--f-m);font-size:11.5px;
        letter-spacing:.05em;text-transform:uppercase;color:var(--ink-soft);font-weight:500}
      table.rubrica td:last-child,table.rubrica th:last-child{text-align:center;white-space:nowrap}
      @media (max-width:560px){table.rubrica{font-size:12.5px}
        table.rubrica th,table.rubrica td{padding:5px 6px}}
      </style>
'''

# --------------------------------------------------------------------------
# 02 - El test
# --------------------------------------------------------------------------
PREGUNTAS = [
 dict(p=u'Un algoritmo tiene que ser ordenado, finito y&hellip;',
      op=[u'corto, cuantas menos instrucciones mejor',
          u'sin ambig&uuml;edad: cada instrucci&oacute;n significa una sola cosa',
          u'escrito en ingl&eacute;s, que es el idioma de las m&aacute;quinas'],
      ok=1,
      por=u'Las tres condiciones son <b>ordenado</b>, <b>finito</b> y <b>sin ambig&uuml;edad</b>. '
          u'Que sea corto est&aacute; bien, pero no es una condici&oacute;n; y el idioma da igual: un '
          u'algoritmo se puede escribir en espa&ntilde;ol y en la libreta.'),
 dict(p=u'El robot de la cuadr&iacute;cula choca contra una pared que se ve&iacute;a perfectamente. '
        u'&iquest;Por qu&eacute;?',
      op=[u'porque el programa ten&iacute;a un fallo de sintaxis',
          u'porque la instrucci&oacute;n dec&iacute;a &laquo;avanza&raquo; y la m&aacute;quina obedece',
          u'porque le faltaba un sensor de choque'],
      ok=1,
      por=u'La m&aacute;quina no mira, no interpreta y no corrige: hace lo que pone. Ver la pared es '
          u'trabajo tuyo <b>al escribir el programa</b>. Un sensor de choque ayudar&iacute;a, pero solo '
          u'si el programa tuviera un condicional que lo mirase.'),
 dict(p=u'Un bucle <i>repetir 4 veces</i>, &iquest;hace que la m&aacute;quina trabaje menos?',
      op=[u'no: ejecuta las mismas instrucciones, lo que ahorra es escritura',
          u's&iacute;: agrupa las cuatro en una sola operaci&oacute;n',
          u's&iacute;, porque la memoria ocupa cuatro veces menos'],
      ok=0,
      por=u'Al ejecutarse, las cuatro repeticiones siguen ah&iacute;, una detr&aacute;s de otra. El bucle '
          u'ahorra <b>escritura</b>, y sobre todo permite escribir un programa que depende de un '
          u'n&uacute;mero que <b>todav&iacute;a no conoces</b>.'),
 dict(p=u'&iquest;Cu&aacute;ndo se queda colgado un bucle <i>mientras</i>?',
      op=[u'cuando se repite m&aacute;s de mil veces',
          u'cuando dentro de &eacute;l no pasa nada que pueda cambiar la condici&oacute;n de salida',
          u'cuando la condici&oacute;n es falsa desde el principio'],
      ok=1,
      por=u'Si la condici&oacute;n es falsa desde el principio, el bucle no se ejecuta ni una vez: '
          u'eso no cuelga nada. Lo que cuelga es <b>repetir algo que nunca cambia la condici&oacute;n</b>, '
          u'como girar en una esquina con paredes en las cuatro direcciones.'),
 dict(p=u'&iquest;Para qu&eacute; sirve una variable?',
      op=[u'para hacer el programa m&aacute;s corto',
          u'para que el programa recuerde un dato de una vez para otra',
          u'para guardar el programa cuando se apaga la placa'],
      ok=1,
      por=u'Es un caj&oacute;n con nombre donde se guarda un dato <b>mientras el programa corre</b>. Sin '
          u'la variable <i>cuenta</i>, la placa no sabr&iacute;a por qu&eacute; n&uacute;mero iba. Y ojo: al '
          u'apagar la placa, lo que hay en una variable <b>se pierde</b>.'),
 dict(p=u'<i>Al iniciar</i> y <i>para siempre</i>, &iquest;en qu&eacute; se diferencian?',
      op=[u'<i>al iniciar</i> se ejecuta una vez y <i>para siempre</i> se repite sin parar',
          u'<i>al iniciar</i> es para los sensores y <i>para siempre</i> para los botones',
          u'<i>para siempre</i> solo funciona si la placa est&aacute; enchufada al ordenador'],
      ok=0,
      por=u'<i>Para siempre</i> es un <b>bucle infinito</b>, y aqu&iacute; no es un error: una m&aacute;quina '
          u'que vigila algo tiene que estar mirando siempre. <i>Al iniciar</i> es donde se preparan '
          u'las cosas que se hacen una sola vez.'),
 dict(p=u'&iquest;Qu&eacute; le entrega un sensor al programa?',
      op=[u'una orden de lo que hay que hacer',
          u'un n&uacute;mero, y nada m&aacute;s',
          u'una imagen de lo que est&aacute; pasando'],
      ok=1,
      por=u'Un sensor <b>no ve, no sabe y no entiende</b>: convierte una magnitud f&iacute;sica en un '
          u'n&uacute;mero. Lo que ese n&uacute;mero significa lo decide el programa al <b>compararlo</b> '
          u'con un umbral.'),
 dict(p=u'Tu farola autom&aacute;tica parpadea sin parar al anochecer, y el programa no tiene errores. '
        u'&iquest;Qu&eacute; est&aacute; pasando?',
      op=[u'la lectura tiembla alrededor del umbral y lo cruza una y otra vez',
          u'el bucle <i>para siempre</i> va demasiado r&aacute;pido',
          u'la bombilla est&aacute; fundida'],
      ok=0,
      por=u'Ning&uacute;n sensor da un n&uacute;mero limpio. Si el valor ronda el umbral, unas veces cae por '
          u'encima y otras por debajo. Se arregla con <b>dos umbrales</b>, uno para encender y otro '
          u'm&aacute;s alto para apagar: <b>hist&eacute;resis</b>.'),
 dict(p=u'Un robot con <b>un solo</b> sensor de luz, &iquest;puede ir hacia la l&aacute;mpara?',
      op=[u's&iacute;, si el sensor es lo bastante bueno',
          u'no, mientras no consiga dos medidas que comparar',
          u'no, hace falta obligatoriamente una c&aacute;mara'],
      ok=1,
      por=u'Una medida sola dice <b>cu&aacute;nta</b> luz hay, no <b>por d&oacute;nde</b>. Las dos medidas '
          u'pueden ser dos sensores a la vez (lo que hicimos nosotros) o el mismo sensor en dos '
          u'posiciones distintas, movi&eacute;ndolo (lo que hizo Grey Walter en 1948).'),
 dict(p=u'&iquest;Qu&eacute; es un sistema de <b>lazo cerrado</b>?',
      op=[u'uno que se apaga solo al terminar',
          u'uno en el que el resultado de actuar vuelve a entrar por los sensores y cambia la decisi&oacute;n siguiente',
          u'uno que funciona sin cables'],
      ok=1,
      por=u'Un microondas a tres minutos es de <b>lazo abierto</b>: no prueba la comida. Un horno con '
          u'term&oacute;metro que enciende y apaga la resistencia es de <b>lazo cerrado</b>, y tu robot '
          u'buscando la l&aacute;mpara tambi&eacute;n: al girar cambia lo que va a medir.'),
]

TEST = (u'''
      <p>Diez preguntas de todo el tema. Se corrigen aqu&iacute; mismo, y cada una explica por
         qu&eacute; &mdash;tambi&eacute;n las que aciertes&mdash;. No cuenta para nota: es para que sepas por
         d&oacute;nde andas antes del examen.</p>
''' + test('u10', u'Lo que tiene que haber quedado del tema', PREGUNTAS))

# --------------------------------------------------------------------------
# 03 - Cierre del tema y del curso
# --------------------------------------------------------------------------
CIERRE = u'''
      <div class="copiar">
        <h4>El tema en tres frases</h4>
        <ol>
          <li>Programar no es saber un idioma raro: es <b>decir las cosas sin dejar huecos</b>, porque
              quien escucha no rellena nada.</li>
          <li>Con tres piezas &mdash;<b>secuencia</b>, <b>bucle</b> y <b>condicional</b>&mdash; y una
              <b>variable</b> para acordarse, se escribe cualquier programa de este curso.</li>
          <li>Una m&aacute;quina se vuelve aut&oacute;noma cuando junta <b>entrada</b>, <b>decisi&oacute;n</b> y
              <b>salida</b>, y lo que hace le cambia lo que va a medir: <b>lazo cerrado</b>.</li>
        </ol>
      </div>
      <h3>Y con esto se cierra el curso</h3>
      <p>Mira atr&aacute;s un momento, porque este tema no ha salido de la nada: est&aacute; hecho de todos
         los anteriores.</p>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>El <b>chasis de cart&oacute;n</b> de tu robot tiene que aguantar el peso de las pilas sin
           doblarse: eso era la unidad de <b>estructuras</b>. Las <b>ruedas</b> giran gracias a un
           motor que transmite movimiento: <b>mecanismos</b>. La <b>LDR con su resistencia</b> es un
           circuito en serie, y funciona porque la <b>tensi&oacute;n se reparte</b> entre las dos:
           <b>electricidad</b>. La placa que
           decide es un ordenador min&uacute;sculo con su entrada, su proceso y su salida: <b>el
           ordenador</b>. El programa lo escribes en una web y lo compartes con tu grupo:
           <b>internet</b> y <b>herramientas digitales</b>. Y el dibujo con el que explicas tu
           montaje es <b>representaci&oacute;n gr&aacute;fica</b>.</p>
        <p>Por eso esta unidad va la &uacute;ltima. No es la m&aacute;s dif&iacute;cil: es la que <b>necesita a
           todas las dem&aacute;s</b>.</p>
      </div>
      <div class="nota">
        <span class="n-tag">Lo que te llevas</span>
        Que una m&aacute;quina no es lista ni tonta: hace <b>exactamente</b> lo que le han dicho. Cuando
        un aparato te haga algo raro &mdash;un m&oacute;vil, una app, un coche&mdash; ya no vas a pensar
        que &laquo;le ha dado por ah&iacute;&raquo;. Vas a pensar que <b>alguien escribi&oacute; eso</b>, y
        que se puede buscar d&oacute;nde. Eso es lo que hace un t&eacute;cnico.
      </div>
'''

S6 = (bloque('00', u'El proyecto &middot; 15 min', PROYECTO) +
      bloque('01', u'&iquest;Merece la pena? &middot; 15 min', MERECE) +
      bloque('02', u'Test &middot; 20 min', TEST) +
      bloque('03', u'Cierre &middot; 10 min', CIERRE))
