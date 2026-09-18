# -*- coding: utf-8 -*-
"""Sesiones 5 a 8 de la unidad 6 de 4.o: la SEGUNDA MITAD.

La primera mitad (c6_build.py) ensena la tecnica -codigo, conversor A/D, IoT y
entrenar un clasificador- con ejemplos que van rotando entre los cinco
candidatos, porque cuando se escribio el proyecto del curso no estaba decidido.
Ya lo esta (PROYECTOS.md, bloque DECIDIDO del 18-sep-2026): el curso se vertebra
con el RIEGO AUTOMATICO, y cada grupo elige entre riego (A), aviso de aula mal
ventilada (B) y lampara de estudio (C). Los tres son el mismo esquema con otro
sensor y otro actuador, asi que las cuatro escenas de aqui los llevan TODAS en
pestanas: nadie tiene que traducir de un proyecto ajeno.

  S5  Decidir con memoria. El programa decide con el numero de este instante, y
      un numero de un instante puede ser mentira. Guardar las ultimas N y
      decidir con todas: media, mediana, tendencia. Lo que quita cada una, lo
      que retrasa y lo que ocupa. Escena con un dia entero de medidas.
  S6  Montar el aviso de verdad. El Uno no tiene wifi: tres caminos con su
      precio. Y despues, cada cuanto hablar. Periodico, por evento, evento con
      latido. La averia mas peligrosa es la que no hace ruido. Escena con dos
      semanas, una caida de red y un aparato que se queda mudo.
  S7  Entrenar con vuestros datos. Las 120 medidas de la clase, y el numero que
      sale segun COMO las partas: 93 % al azar, 73 % dejando fuera una jornada.
      Donde acaba lo que se puede decir con esos datos.
  S8  El sistema completo. El programa entero como maquina de estados, el modo
      seguro, y la ficha de numeros con la que se defiende. Cuatro averias que
      se encienden a mano. Y el test de toda la unidad, con identificador
      propio (c6b), porque repetir el de la S4 romperia los dos.

FRONTERAS con las unidades de al lado, acordadas al escribir:
  - La HISTERESIS y el control (todo-nada, proporcional, la banda) son de la
    unidad 4. Aqui la S5 va de GUARDAR valores y decidir con el historico, que
    es programacion y datos, no control. Donde se rozan se dice y se remite.
  - La ELECTRONICA entre el pin y el actuador es de la unidad 5.
  - PRESENTAR Y DEFENDER es el criterio 3.1, que vive en las unidades 1 y 2.
    Aqui se prepara el CONTENIDO tecnico de esa defensa, no la defensa.
  - El IMPACTO ambiental se mide, pero su tratamiento es de la unidad 8.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unidad_base import ficha, pregunta
from test_auto import test
from c6b_escenas import HISTORICO, AVISO
from c6b_escenas2 import DATOS, SISTEMA

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PENDIENTES = []


def foto(fichero, alt, pie, autor, licencia, pagina_commons, ancho=None):
    if not os.path.exists(os.path.join(RAIZ, 'img', fichero)):
        PENDIENTES.append(u'FALTA LA FOTO img/' + fichero)
        return u''
    estilo = u' style="max-width:%dpx;margin-left:auto;margin-right:auto"' % ancho if ancho else u''
    return u'''      <figure class="foto"%s>
        <img src="../../../img/%s" alt="%s" loading="lazy">
        <figcaption>%s
          <span class="credito">%s &middot; %s &middot;
            <a href="%s" target="_blank" rel="noopener">Wikimedia Commons</a></span>
        </figcaption>
      </figure>
''' % (estilo, fichero, alt, pie, autor, licencia, pagina_commons)


# Titulo y canal comprobados uno a uno con la API oEmbed de YouTube el
# 18-sep-2026. Lo que la API dice es QUIEN lo firma y COMO se llama; no dice si
# el video es bueno. NADIE DEL PROYECTO LOS HA VISTO ENTEROS: hay que verlos
# antes de ponerlos en clase.
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


# ==========================================================================
# SESION 5 - Decidir con memoria
# ==========================================================================
S5_RETO = u'''
      <p>A estas alturas vuestro aparato ya est&aacute; montado y ya decide solo. Lee el sensor con
         <code>analogRead()</code>, compara con un umbral y mueve el actuador. En la mesa del taller
         funciona, y se ve funcionar. Enhorabuena: eso es un sistema de control, y lo hab&eacute;is
         hecho vosotros.</p>
      <div class="aviso">
        <span class="n-tag">Lo que pas&oacute; el fin de semana</span>
        Lo dej&aacute;is enchufado el viernes con el registro puesto. El lunes lo mir&aacute;is:
        <b>la bomba arranc&oacute; nueve veces</b>, tres de ellas de madrugada, y la tierra est&aacute;
        empapada. <i>(En el grupo de ventilaci&oacute;n, el aviso de &laquo;abrid la ventana&raquo;
        salt&oacute; a las 03:14 con el aula vac&iacute;a. En el de la l&aacute;mpara, se encendi&oacute;
        sola a mediod&iacute;a.)</i> Nadie toc&oacute; nada.
      </div>
      <p>Lo primero que se propone siempre es subir el umbral. Prob&aacute;ndolo se ve el problema:
         subes el umbral lo bastante para que no salten esos nueve arranques y entonces
         <b>tampoco salta cuando hace falta</b>. Lo segundo que se propone es meter un
         <code>delay()</code> largo, y eso ya sab&eacute;is de la unidad 4 que deja al programa
         <b>ciego</b> mientras dura.</p>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento antes de seguir</span>
        <p>Tu programa da una vuelta al <code>loop()</code> muchas veces por segundo, y en cada una
           toma la decisi&oacute;n entera con <b>un solo n&uacute;mero</b>: el que acaba de leer.
           &iquest;Qu&eacute; tiene que ser verdad de ese n&uacute;mero para que eso funcione?
           Escr&iacute;belo en el cuaderno antes de pasar el rat&oacute;n por debajo.</p>
      </div>
      <p>Tiene que ser verdad que <b>ninguna medida suelta miente</b>. Y eso es falso en todos los
         sensores del mundo. Basta con que alguien roce la sonda al pasar, que una sombra cruce por
         delante de la LDR o que se abra la puerta del aula un segundo: el sensor da un valor que no
         corresponde a nada, el programa se lo cree y act&uacute;a.</p>
      <p>El fallo no est&aacute; en el umbral ni en el sensor. Est&aacute; en que <b>tu programa no se
         acuerda de nada</b>. Cada vuelta empieza de cero, sin saber qu&eacute; le&iacute;a hace un
         minuto. Y una medida sola no se puede contrastar con nada.</p>
'''

S5_TEORIA = u'''
      <p>Para que el programa se acuerde hay que <b>guardar</b> las medidas. Y guardar, en una placa
         como esta, es ocupar un sitio que se puede contar.</p>
''' + foto('c6-atmega328-die.jpg',
           u'Fotograf&iacute;a al microscopio del interior de un chip ATmega328: un cuadrado de '
           u'circuitos con hilos dorados soldados alrededor',
           u'Esto es el <b>ATmega328</b> por dentro: el chip que lleva el Arduino Uno, abierto y '
           u'fotografiado al microscopio a 20 aumentos. Es <b>la misma foto</b> que miraste en la '
           u'unidad 5, cuando segu&iacute;as un hilo hasta la patilla <code>A0</code>; hoy toca '
           u'mirar otra cosa. El cuadrado entero mide unos <b>3 mil&iacute;metros '
           u'de lado</b>; los hilos que salen por los bordes son los que van a las patillas. F&iacute;jate '
           u'en que hay dos clases de paisaje: las zonas que parecen <b>papel cuadriculado</b>, con el '
           u'mismo dibujo repetido miles de veces, son <b>memoria</b> (una celda copiada una y otra vez); '
           u'las zonas revueltas son l&oacute;gica. Ah&iacute; dentro conviven tres memorias: '
           u'<b>32 kB de Flash</b> para tu programa, <b>1 kB de EEPROM</b> que sobrevive al apagado y '
           u'<b>2 kB de SRAM</b> para las variables. El hist&oacute;rico de esta sesi&oacute;n va en esos '
           u'2 kB, y por eso se cuenta cada byte.',
           u'Markus Kammerstetter', u'CC BY 4.0',
           u'https://commons.wikimedia.org/wiki/File:Atmel_atmega328_mz_20x.jpg') + u'''
      <div class="copiar">
        <h4>El hist&oacute;rico, y el truco para que no crezca</h4>
        <p>Un <b>hist&oacute;rico</b> son las <b>N &uacute;ltimas</b> medidas guardadas. No todas: las
           N &uacute;ltimas, porque las de hace dos horas ya no dicen nada y la memoria no da.</p>
        <p>Para que ocupe siempre lo mismo se escribe <b>encima de la m&aacute;s vieja</b> dando la
           vuelta. Eso se llama <b>buffer circular</b>, y son cuatro l&iacute;neas:</p>
        <pre style="font-family:var(--f-m);font-size:12.5px;line-height:1.6;margin:8px 0;white-space:pre-wrap">const byte N = 10;      // cu&aacute;ntas medidas guardo
int  hist[N];           // 20 bytes de los 2048
byte pos = 0;           // por d&oacute;nde voy escribiendo

void guarda(int x) {
  hist[pos] = x;        // escribo encima de la m&aacute;s vieja
  pos = (pos + 1) % N;  // al llegar al final, vuelvo al principio
}</pre>
        <p>El <code>%</code> es el <b>resto de la divisi&oacute;n</b>. Cuando <code>pos</code> llega a
           N, <code>N % N</code> vale 0 y vuelve a empezar. Sin esa l&iacute;nea, el array se sale por
           el final y el programa escribe encima de otras variables: en un Arduino <b>eso no da
           error</b>, da n&uacute;meros raros en cualquier otro sitio del programa.</p>
      </div>
      <div class="copiar">
        <h4>Lo que cabe de verdad en 2.048 bytes</h4>
        <table style="width:100%;border-collapse:collapse;font-size:14.5px">
          <tr style="text-align:left;border-bottom:1.5px solid var(--line)">
            <th>guardando cada medida en&hellip;</th><th>bytes por medida</th><th>caben</th></tr>
          <tr><td><code>byte</code> (0 a 255, hay que dividir la lectura entre 4)</td><td>1</td><td>2.048</td></tr>
          <tr><td><code>int</code> (la lectura entera, 0 a 1023)</td><td>2</td><td>1.024</td></tr>
          <tr><td><code>long</code></td><td>4</td><td>512</td></tr>
          <tr><td><code>float</code></td><td>4</td><td>512</td></tr>
        </table>
        <p style="margin-top:10px">Esos son los m&aacute;ximos <b>te&oacute;ricos</b>: en la realidad el
           programa necesita sitio para todo lo dem&aacute;s, as&iacute; que un hist&oacute;rico
           razonable es de <b>decenas</b> de medidas, no de miles. Con medidas cada dos minutos,
           <b>20 medidas son 40 minutos</b> de memoria.</p>
      </div>
      <p>Ya tienes las medidas guardadas. La pregunta ahora es qu&eacute; hacer con ellas, y hay
         cuatro respuestas que se usan de verdad. La escena las tiene todas, sobre un d&iacute;a entero
         de vuestro sensor. Empieza con <b>el &uacute;ltimo valor</b>, que es lo que tienes hoy, y mira
         la fila de arriba de la tabla.</p>
''' + HISTORICO + u'''
      <div class="copiar">
        <h4>Las cuatro maneras de decidir, y lo que cuesta cada una</h4>
        <table style="width:100%;border-collapse:collapse;font-size:14px">
          <tr style="text-align:left;border-bottom:1.5px solid var(--line)">
            <th>regla</th><th>qu&eacute; quita</th><th>qu&eacute; cuesta</th></tr>
          <tr><td><b>el &uacute;ltimo valor</b></td><td>nada</td><td>2 bytes. Se cree cualquier pico.</td></tr>
          <tr><td><b>media de N</b></td><td>el ruido peque&ntilde;o</td>
              <td>2N bytes y un <b>retraso de N/2 medidas</b>. Al pico no lo quita: lo
                  <b>reparte entre N medidas</b>, o sea que lo estira.</td></tr>
          <tr><td><b>mediana de N</b></td><td>el pico, entero</td>
              <td>2N bytes, un retraso parecido, y adem&aacute;s hay que <b>ordenar</b> (otra copia
                  del array y mucho m&aacute;s tiempo de c&aacute;lculo).</td></tr>
          <tr><td><b>tendencia</b></td><td>nada; <b>adelanta</b> el aviso</td>
              <td>2N bytes y <b>falsas alarmas</b> cada vez que la se&ntilde;al sube un rato y se
                  para.</td></tr>
        </table>
        <p style="margin-top:10px"><b>Media y mediana no son lo mismo y no sirven para lo mismo.</b>
           La media es para el ruido de siempre; la mediana, para el valor absurdo de un instante.
           En la escena, con el riego, la <b>mediana de 5</b> deja los arranques falsos en cero con
           <b>10 bytes</b>; a la media le hace falta N = 10 para lo mismo, o sea el doble.</p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Hay una media que <b>no guarda nada</b> y que en placas muy justas se usa mucho:</p>
        <pre style="font-family:var(--f-m);font-size:12.5px;margin:6px 0;white-space:pre-wrap">float m = 0;
void bucle() {
  m = m * 0.9 + leer() * 0.1;   // 4 bytes en total, sin array
}</pre>
        <p>Cada medida nueva pesa un 10 % y todo lo anterior pesa el 90 %. Se llama <b>media
           exponencial</b> y alisa parecido a una media de unas 10 medidas <b>ocupando 4 bytes en vez
           de 20</b>. La pega: como no guarda las medidas, <b>no puedes hacer la mediana con ella</b>
           ni mirar atr&aacute;s para ver qu&eacute; pas&oacute;. Si lo que te sobran son picos, no te
           sirve.</p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Una trampa que viene directa de la sesi&oacute;n 1. Para hacer la media hay que sumar:</p>
        <pre style="font-family:var(--f-m);font-size:12.5px;margin:6px 0;white-space:pre-wrap">int suma = 0;
for (byte i = 0; i &lt; N; i++) suma += hist[i];</pre>
        <p>Con N = 20 y lecturas de hasta 1023, la suma llega a <b>20.460</b>: cabe en un
           <code>int</code>, que aguanta hasta 32.767. Con <b>N = 40</b> la suma llega a
           <b>40.920</b>, y ya <b>no cabe</b>: desborda y la media sale negativa. El programa no avisa
           de nada, exactamente igual que en la sesi&oacute;n 1. Se arregla poniendo
           <code>long suma = 0;</code>, que son 2 bytes m&aacute;s <b>una sola vez</b>.</p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>En la escena puedes guardar cada medida en un <code>byte</code> dividi&eacute;ndola entre 4.
           Ocupa <b>la mitad</b> y los resultados cambian muy poco: el error que mete esa divisi&oacute;n
           es de <b>4 unidades</b>, y el ruido propio del sensor ya es de &plusmn;12. Ninguna
           precisi&oacute;n que el sensor no tiene se gana guardando m&aacute;s bytes. Es la misma idea
           de los decimales de la sesi&oacute;n 2, ahora en la memoria.</p>
      </div>
      <div class="nota">
        <span class="n-tag">Ojo, que esto no es lo de la unidad 4</span>
        En la unidad 4 arreglasteis que el actuador se encendiera y se apagara sin parar
        <b>separando el umbral de encender del de apagar</b>: eso es la <b>hist&eacute;resis</b>, y es
        control. Aqu&iacute; el problema es otro: la <b>medida</b> es mala. Las dos cosas se pueden
        (y se suelen) poner a la vez, y son independientes: la hist&eacute;resis no quita un pico, y
        la mediana no quita un rebote alrededor del umbral.
      </div>
''' + video('video-c6-media', 'Pl79Ni3NUsY',
            u'Filtro Digital Pasa Bajos con Arduino Media Movil',
            u'Canal: Electgpl',
            u'La media m&oacute;vil escrita en Arduino, con el osciloscopio delante para ver la se&ntilde;al '
            u'antes y despu&eacute;s.')

S5_PRACTICA = ficha(
    u'Actividad 5 &middot; Ponerle memoria a vuestro programa',
    [u'4.2', u'5.1', u'C.1', u'C.2'], u'Parejas &middot; 20 min', u'''
          <h4>Primera parte &middot; el buffer circular en Tinkercad (8 min)</h4>
          <p>Partid del sketch que ya ten&eacute;is. A&ntilde;adidle el hist&oacute;rico de
             <b>N = 10</b> y sacad por el monitor serie <b>tres</b> n&uacute;meros separados por comas:
             la lectura de este instante, la media de las 10 y la mediana de las 10.</p>
          <ol class="pasos">
            <li>Copiad en la libreta las tres funciones: <code>guarda()</code>, la de la media y la de
                la mediana.</li>
            <li>Con el potenci&oacute;metro puesto, dadle un <b>golpe seco</b> al eje y volvedlo a la
                posici&oacute;n de antes. Anotad qu&eacute; hacen los tres n&uacute;meros.</li>
            <li>Decid <b>cu&aacute;ntos bytes</b> ocupa vuestro hist&oacute;rico y qu&eacute; porcentaje
                es de los 2.048.</li>
          </ol>
          <h4>Segunda parte &middot; elegir la regla, con n&uacute;meros (8 min)</h4>
          <p>Con la escena puesta en <b>vuestro</b> proyecto y el umbral que tengáis, rellenad esta
             tabla anotando lo que dice la escena:</p>
          <table style="width:100%;border-collapse:collapse;font-size:14.5px;margin:8px 0">
            <tr style="text-align:left;border-bottom:1.5px solid var(--line)">
              <th>regla</th><th>arranques de m&aacute;s</th><th>tarda de media</th><th>bytes</th></tr>
            <tr><td>el &uacute;ltimo valor</td><td></td><td></td><td></td></tr>
            <tr><td>media de 5</td><td></td><td></td><td></td></tr>
            <tr><td>media de 20</td><td></td><td></td><td></td></tr>
            <tr><td>mediana de 5</td><td></td><td></td><td></td></tr>
            <tr><td>tendencia con N = 20</td><td></td><td></td><td></td></tr>
          </table>
          <p>Y debajo, en <b>dos frases</b>: qu&eacute; regla vais a poner en vuestro proyecto y
             <b>por qu&eacute; esa</b>. La respuesta tiene que nombrar cu&aacute;l de los dos fallos
             os duele m&aacute;s &mdash;actuar de m&aacute;s o enteraros tarde&mdash;, que es lo que
             visteis en la sesi&oacute;n 4.</p>
          <h4>Tercera parte &middot; la cuenta que no falla sola (4 min)</h4>
          <p>Vuestro compa&ntilde;ero escribe <code>int suma = 0;</code> y hace la media de
             <b>N = 40</b> lecturas de hasta 1023. Calculad cu&aacute;nto vale la suma en el peor caso,
             decid si cabe y escribid la correcci&oacute;n.</p>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>El sketch saca los tres n&uacute;meros y el buffer da la vuelta bien <b>(3 puntos)</b>.</li>
            <li>Lo que hace cada n&uacute;mero ante el golpe, anotado <b>(1 punto)</b>.</li>
            <li>La tabla de las cinco reglas, completa <b>(2 puntos)</b>.</li>
            <li>La regla elegida, justificada con el coste de los dos fallos <b>(2 puntos)</b>.</li>
            <li>La cuenta del desbordamiento, hecha y corregida <b>(2 puntos)</b>.</li>
          </ul>
''')

S5_CIERRE = u'''
      <ol>
      ''' + pregunta(u'&iquest;Por qu&eacute; subir el umbral no arregla los arranques de madrugada?',
                     u'<p>Porque el problema no es <b>d&oacute;nde</b> est&aacute; el umbral, sino que '
                     u'una medida suelta puede ser falsa. Si subes el umbral lo bastante para que no '
                     u'lo cruce un pico de 300 unidades, tampoco lo cruza el problema de verdad.</p>'
                     ) + pregunta(
          u'&iquest;Qu&eacute; hace <code>pos = (pos + 1) % N;</code> y qu&eacute; pasa si se te olvida?',
          u'<p>Hace que el &iacute;ndice <b>vuelva a 0</b> al llegar al final, para escribir encima de '
          u'la medida m&aacute;s vieja. Sin esa l&iacute;nea el programa escribe <b>fuera del '
          u'array</b>, encima de otras variables. En Arduino eso no da error: da n&uacute;meros raros '
          u'en otro sitio del programa, que es peor.</p>') + pregunta(
          u'La media y la mediana ocupan los mismos bytes. &iquest;Para qu&eacute; sirve cada una?',
          u'<p>La <b>media</b> alisa el ruido de siempre, pero a un pico enorme no lo quita: lo '
          u'reparte entre las N medidas, o sea que lo <b>estira</b>. La <b>mediana</b> ordena y se '
          u'queda con la de en medio, as&iacute; que un valor absurdo se va a un extremo y <b>no '
          u'entra en la cuenta</b>. Para picos, mediana; para ruido, media.</p>') + pregunta(
          u'&iquest;Qu&eacute; se paga por poner una media de 20 en vez de una de 5?',
          u'<p>Tres cosas: <b>30 bytes m&aacute;s</b> de memoria, un <b>retraso</b> de unas 10 '
          u'medidas en enterarse (con medidas cada 2 minutos, 20 minutos) y m&aacute;s tiempo de '
          u'c&aacute;lculo en cada vuelta. Alisar no es gratis.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya decide bien, y ya no se cree cualquier cosa. Pero sigue decidiendo <b>en el aula y para
        s&iacute; mismo</b>. En la sesi&oacute;n 3 dise&ntilde;asteis el mensaje que tendr&iacute;a que
        salir de la placa; nunca lleg&oacute; a salir. Y hay un detalle que se pasa por alto hasta que
        toca montarlo: <b>un Arduino Uno no tiene wifi</b>.
      </div>
'''


# ==========================================================================
# SESION 6 - Montar el aviso de verdad
# ==========================================================================
S6_RETO = u'''
      <p>En la sesi&oacute;n 3 escribisteis el mensaje de vuestro aparato: qui&eacute;n, qu&eacute;,
         cu&aacute;ndo y a d&oacute;nde, con su tema de MQTT y todo. Estaba muy bien. Y no ha salido
         del cuaderno.</p>
      <div class="aviso">
        <span class="n-tag">El encargo de hoy</span>
        Que salga. Ten&eacute;is delante un Arduino Uno, que <b>no tiene wifi, ni Ethernet, ni
        bluetooth</b>: no lleva nada con lo que hablar con el mundo salvo el cable USB.
        <b>Dos minutos</b>: escribid en el cuaderno c&oacute;mo sale de esa aula el dato,
        con lo que cuesta cada opci&oacute;n.
      </div>
      <p>Las tres respuestas que valen son estas, y conviene saberlas <b>con su precio</b>, porque
         esto va en la memoria del proyecto:</p>
      <div class="copiar">
        <h4>Tres maneras de sacar el dato, con su pega</h4>
        <table style="width:100%;border-collapse:collapse;font-size:14.5px">
          <tr style="text-align:left;border-bottom:1.5px solid var(--line)">
            <th>c&oacute;mo</th><th>cuesta</th><th>la pega</th></tr>
          <tr><td>Por el <b>cable USB</b> a un ordenador del aula, que lee el puerto serie y lo
                  sube &eacute;l</td><td><b>0 &euro;</b></td>
              <td>hace falta un ordenador encendido al lado, todo el rato</td></tr>
          <tr><td>A&ntilde;adirle un <b>m&oacute;dulo ESP-01</b> y hablarle por comandos AT</td>
              <td>~<b>2 &euro;</b></td>
              <td>va a 3,3 V (el Uno da 5 V: hace falta adaptar) y come bastante corriente</td></tr>
          <tr><td>Cambiar el Uno por un <b>ESP32</b>, que ya trae wifi dentro</td>
              <td>~<b>5 &euro;</b></td>
              <td>hay que rehacer el montaje y las entradas anal&oacute;gicas son distintas</td></tr>
        </table>
        <p style="margin-top:10px">Ninguna es &laquo;la buena&raquo;. En un aula con un ordenador fijo,
           la primera es la m&aacute;s barata y la m&aacute;s f&aacute;cil de depurar. Para una planta
           en un pasillo, no vale.</p>
      </div>
      <p>Supongamos que ya lo hab&eacute;is resuelto y el dato sale. Queda la pregunta que casi nadie
         hace, y que es la de hoy: <b>&iquest;cada cu&aacute;nto?</b> La respuesta que sale sola es
         &laquo;cada 30 segundos, as&iacute; est&aacute; al d&iacute;a&raquo;.</p>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento</span>
        <p>Haz la cuenta: cada 30 segundos son <b>2.880 mensajes al d&iacute;a</b>, y
           <b>40.320</b> en las dos semanas de vacaciones. &iquest;Cu&aacute;ntos vas a leer t&uacute;?
           Y la segunda, que es la importante: si el aparato se estropea y <b>deja de mandar</b>,
           &iquest;c&oacute;mo te enteras?</p>
      </div>
      <p>La primera pregunta tiene una respuesta inc&oacute;moda: ninguno. Un aviso que llega
         cuarenta mil veces <b>no es un aviso</b>, es un ruido de fondo, y a la tercera se silencia la
         notificaci&oacute;n. La segunda tiene una respuesta peor: <b>no te enteras</b>. Un aparato
         estropeado se queda callado, y callado es exactamente lo que hace cuando todo va bien.</p>
'''

S6_TEORIA = u'''
      <p>Antes de nada, mira lo que hay que a&ntilde;adirle al Uno. Es esto, y es diminuto:</p>
''' + foto('c6-esp8266-dht11.jpg',
           u'M&oacute;dulo ESP-01 azul montado encima de una placa peque&ntilde;a que lleva un sensor '
           u'DHT11, tambi&eacute;n azul, con su rejilla de agujeros',
           u'Arriba, un <b>ESP-01</b>: un m&oacute;dulo con el chip <b>ESP8266</b> dentro de esa latita '
           u'met&aacute;lica, y con la <b>antena de wifi dibujada en el propio circuito impreso</b> '
           u'&mdash;el zigzag dorado de la derecha&mdash;. No hay m&aacute;s antena que esa pista de '
           u'cobre. Debajo, en azul claro y con su rejilla, un <b>DHT11</b>, que es el sensor de '
           u'temperatura y humedad del proyecto de ventilaci&oacute;n. El conjunto entero mide unos '
           u'<b>2,5 cm</b> y cuesta unos pocos euros. Ojo con una cosa que no se ve en la foto: el '
           u'ESP-01 funciona a <b>3,3 V</b>, y un Arduino Uno saca <b>5 V</b> por sus patillas; '
           u'conectarlos directamente estropea el m&oacute;dulo.',
           u'Nowforever', u'CC BY-SA 4.0',
           u'https://commons.wikimedia.org/wiki/File:ESP8266_with_DHT11.jpg') + u'''
      <p>Con eso resuelto, lo de hoy: <b>cu&aacute;ndo hablar</b>. Hay tres maneras, y se eligen; no
         se heredan del ejemplo que hayas copiado.</p>
      <div class="copiar">
        <h4>Las tres pol&iacute;ticas de aviso</h4>
        <ul>
          <li><b>Peri&oacute;dico</b>: mandas una medida cada X minutos, pase lo que pase. Sencillo de
              programar y sencillo de dibujar en una gr&aacute;fica. Genera much&iacute;simos mensajes y
              la mayor&iacute;a no dicen nada nuevo.</li>
          <li><b>Por evento</b>: mandas un mensaje <b>cuando algo cambia</b> &mdash;empieza el
              problema, se acaba el problema&mdash; y, si el problema sigue, lo repites cada X minutos
              para que no se olvide. Poqu&iacute;simos mensajes y todos dicen algo.</li>
          <li><b>Por evento con latido</b>: lo anterior, m&aacute;s un mensaje cada pocas horas que
              solo dice <b>&laquo;sigo aqu&iacute;&raquo;</b>. Es el que se usa en serio, y ahora
              ver&aacute;s por qu&eacute;.</li>
        </ul>
      </div>
      <p>En la escena tienes dos semanas de vuestro proyecto, con sus incidencias de verdad y una
         <b>ca&iacute;da de red de nueve horas</b> el d&iacute;a 6. Antes de tocar nada,
         <b>marca la casilla &laquo;el aparato se queda mudo el d&iacute;a 9&raquo;</b>: es la
         aver&iacute;a de la que va esta sesi&oacute;n. Y ahora haz tres cosas y mira cada vez la fila
         <b>&laquo;el silencio del aparato&raquo;</b>:</p>
      <ol>
        <li>con <b>peri&oacute;dico</b>, baja el mando de &laquo;cada&raquo; hasta 5 minutos;</li>
        <li>p&aacute;salo a <b>por evento</b>;</li>
        <li>y despu&eacute;s a <b>evento + latido</b>.</li>
      </ol>
''' + AVISO + u'''
      <div class="copiar">
        <h4>El latido, y por qu&eacute; no es un capricho</h4>
        <p>Un aparato que avisa solo cuando pasa algo tiene un agujero: <b>estropeado y tranquilo se
           ven igual</b>. Los dos son silencio.</p>
        <p>El <b>latido</b> (en ingl&eacute;s <i>heartbeat</i>) lo arregla poniendo el silencio del lado
           de las averías: el aparato manda cada X horas un mensaje que solo dice que sigue vivo, y
           el que recibe <b>da la alarma si no le llega nada</b> en un plazo, normalmente el doble.
           Con eso, el fallo deja de ser invisible.</p>
        <p>El precio hay que decirlo: el latido <b>gasta</b> mensajes, datos y bater&iacute;a aunque no
           pase nada. Con latido de 1 hora salen <b>231</b> mensajes en dos semanas; con latido de
           6 horas, <b>59</b>; con latido de un d&iacute;a, <b>33</b>. Y cuanto m&aacute;s espaciado,
           m&aacute;s tarda en descubrirse el silencio: con 6 horas se descubre <b>9,3 horas</b>
           despu&eacute;s de que el aparato se calle; con un d&iacute;a, m&aacute;s de <b>27</b>.</p>
      </div>
      <div class="copiar">
        <h4>Lo que el latido <b>no</b> puede distinguir</h4>
        <p>Quita la ca&iacute;da de red en la escena y prueba latidos de 1 h, 6 h y un d&iacute;a: cero
           falsas alarmas siempre. Vu&eacute;lvela a poner: aparece <b>una falsa alarma</b> con casi
           cualquier latido, y no es un fallo del dise&ntilde;o.</p>
        <p>El que recibe solo sabe una cosa: <b>ha dejado de llegarme</b>. Y eso puede ser el aparato
           roto, la red del centro ca&iacute;da, el router apagado o el servidor de vacaciones.
           <b>Desde el otro lado no se distinguen</b>, porque todas se ven igual: silencio.</p>
        <p>As&iacute; que la decisi&oacute;n no es &laquo;c&oacute;mo evito las falsas alarmas&raquo;
           sino <b>&laquo;cu&aacute;nto silencio estoy dispuesto a aguantar antes de ir a mirar&raquo;</b>.
           Si la red del centro se cae todas las semanas y tu plazo es de doce horas, vas a tener una
           alarma falsa por semana, y a la cuarta nadie ir&aacute; a mirar. Esa es la conversaci&oacute;n
           que hay que tener, y es de dise&ntilde;o, no de programaci&oacute;n.</p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Esto no lo hemos inventado nosotros: viene <b>dentro</b> del protocolo MQTT que visteis en
           la sesi&oacute;n 3. Cuando un aparato se conecta al br&oacute;ker le dice dos cosas:</p>
        <ul>
          <li>un <b>Keep Alive</b>, que es el latido: si el br&oacute;ker no oye nada en vez y media ese
              tiempo, da la conexi&oacute;n por perdida;</li>
          <li>y un <b>mensaje de despedida</b> (en el protocolo se llama literalmente
              <i>Will</i>, testamento): un mensaje que el aparato deja escrito al conectarse y que
              <b>publica el br&oacute;ker en su nombre</b> si se cae sin avisar.</li>
        </ul>
        <p>O sea: la gente que dise&ntilde;&oacute; el protocolo para vigilar oleoductos por
           sat&eacute;lite ya sab&iacute;a que el problema no era mandar el dato, sino <b>enterarse de
           que ha dejado de llegar</b>.</p>
      </div>
      <div class="copiar">
        <h4>Qu&eacute; se hace cuando no hay red</h4>
        <p>Dos decisiones, y las dos son vuestras:</p>
        <ol>
          <li><b>&iquest;Se guarda o se tira?</b> Si se guarda, hace falta una <b>cola</b> en memoria.
              Con 1.200 bytes libres y mensajes de 24 bytes caben <b>50</b>. Cuando se llena, lo
              siguiente se pierde igual: una cola no es infinita, solo aplaza el problema.</li>
          <li><b>&iquest;Se reintenta?</b> Guardar sin reintentar es <b>perder despacio</b>: si el
              aparato solo vac&iacute;a la cola cuando le toca mandar algo nuevo, un aviso del martes
              puede no salir hasta el jueves. El aparato tiene que <b>volver a intentarlo solo</b> en
              cuanto vuelva la red.</li>
        </ol>
        <p>En la escena, con el riego y &laquo;por evento&raquo;: <b>sin cola</b>, la incidencia del
           d&iacute;a 6 &mdash;que cae entera dentro de la ca&iacute;da&mdash; <b>no se supo nunca</b>.
           Con cola, se supo <b>siete horas tarde</b>. No es lo mismo, y ninguna de las dos cosas es
           gratis.</p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>En la escena hay un mando que parece que no pinta nada aqu&iacute;: <b>con qu&eacute; decide
           la placa</b>. C&aacute;mbialo de &laquo;el &uacute;ltimo valor&raquo; a &laquo;la media de
           10&raquo; y mira la fila azul del dibujo.</p>
        <p>Con el &uacute;ltimo valor, en cada borde de una incidencia la lectura tiembla alrededor del
           umbral y el estado cambia varias veces seguidas: salen <b>42</b> mensajes en vez de
           <b>26</b> por el mismo n&uacute;mero de incidencias. La pol&iacute;tica de aviso es la misma;
           lo que ha cambiado es <b>la sesi&oacute;n anterior</b>. Lo que decidiste sobre la memoria
           te sale en la factura de datos.</p>
      </div>
''' + video('video-c6-esp', 'asVv6VZId_o',
            u'ESP8266: Subir datos a un servidor mediante WiFi',
            u'Canal: Prometec',
            u'El m&oacute;dulo de la foto, mandando datos de verdad a un servidor. Sirve para ver el '
            u'montaje y los comandos antes de intentarlo.')

S6_PRACTICA = ficha(
    u'Actividad 6 &middot; El contrato de avisos de vuestro proyecto',
    [u'4.2', u'5.1', u'C.3', u'C.4'], u'Grupos de tres &middot; 20 min', u'''
          <h4>Primera parte &middot; c&oacute;mo sale el dato (5 min)</h4>
          <p>Elegid <b>uno</b> de los tres caminos de la tabla de arriba para vuestro proyecto y
             escribid, en la libreta: cu&aacute;l, <b>cu&aacute;nto cuesta</b>, qu&eacute; hace falta
             adem&aacute;s (&iquest;un ordenador encendido? &iquest;un adaptador de 3,3 V?) y
             qu&eacute; pasa si eso falla.</p>
          <h4>Segunda parte &middot; medir las tres pol&iacute;ticas (7 min)</h4>
          <p>Con la escena en <b>vuestro</b> proyecto, la ca&iacute;da de red puesta y el aparato mudo
             marcado, anotad esta tabla:</p>
          <table style="width:100%;border-collapse:collapse;font-size:14.5px;margin:8px 0">
            <tr style="text-align:left;border-bottom:1.5px solid var(--line)">
              <th>pol&iacute;tica</th><th>mensajes que llegan</th><th>al d&iacute;a</th>
              <th>incidencias que no se supieron</th><th>&iquest;se descubre el silencio?</th></tr>
            <tr><td>peri&oacute;dico cada 5 min</td><td></td><td></td><td></td><td></td></tr>
            <tr><td>peri&oacute;dico cada 1 h</td><td></td><td></td><td></td><td></td></tr>
            <tr><td>por evento</td><td></td><td></td><td></td><td></td></tr>
            <tr><td>evento + latido de 6 h</td><td></td><td></td><td></td><td></td></tr>
          </table>
          <h4>Tercera parte &middot; escribir el contrato (8 min)</h4>
          <p>Un <b>contrato de avisos</b> son seis l&iacute;neas que caben en media hoja y que
             cualquiera del grupo tiene que poder leer en voz alta. Escribid las vuestras:</p>
          <ol class="pasos">
            <li><b>Qu&eacute; se manda</b>: los campos, con sus unidades (los de la sesi&oacute;n 3).</li>
            <li><b>Cu&aacute;ndo</b>: qu&eacute; hecho dispara un mensaje.</li>
            <li><b>Cada cu&aacute;nto se repite</b> mientras el problema siga.</li>
            <li><b>Cada cu&aacute;nto es el latido</b>, y por qu&eacute; ese plazo y no otro.</li>
            <li><b>Qu&eacute; pasa si no hay red</b>: cu&aacute;ntos mensajes se guardan y cu&aacute;ndo
                se reintenta.</li>
            <li><b>Qu&eacute; hace quien recibe</b> si deja de llegarle todo: cu&aacute;nto espera antes
                de preocuparse y <b>a qui&eacute;n avisa</b>, con nombre.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>El camino elegido, con su precio y su pega <b>(2 puntos)</b>.</li>
            <li>La tabla de las cuatro filas, completa <b>(3 puntos)</b>.</li>
            <li>Las seis l&iacute;neas del contrato, todas <b>(3 puntos)</b>.</li>
            <li>El plazo del latido est&aacute; <b>razonado</b> con la ca&iacute;da de red
                <b>(1 punto)</b>.</li>
            <li>La l&iacute;nea 6 se&ntilde;ala a una persona concreta <b>(1 punto)</b>.</li>
          </ul>
''')

S6_CIERRE = u'''
      <ol>
      ''' + pregunta(u'Un Arduino Uno no tiene wifi. Di dos maneras de sacar el dato del aula y su pega.',
                     u'<p>Por el <b>cable USB</b> a un ordenador que lo suba &eacute;l (0 &euro;, pero '
                     u'hace falta el ordenador encendido al lado) o con un <b>m&oacute;dulo ESP-01</b> '
                     u'(unos 2 &euro;, pero va a 3,3 V y hay que adaptar la tensi&oacute;n). La tercera '
                     u'es cambiar el Uno por un <b>ESP32</b>, que ya lo trae.</p>') + pregunta(
          u'&iquest;Por qu&eacute; avisar cada 30 segundos es peor que avisar por evento?',
          u'<p>Porque son <b>2.880 mensajes al d&iacute;a</b> y casi ninguno dice nada nuevo. Un aviso '
          u'que llega miles de veces deja de leerse: la gente silencia la notificaci&oacute;n y '
          u'entonces no se entera ni de los que s&iacute; importaban. Y encima gasta datos y '
          u'bater&iacute;a.</p>') + pregunta(
          u'&iquest;Qu&eacute; es un latido y qu&eacute; problema resuelve?',
          u'<p>Un mensaje cada pocas horas que solo dice <b>&laquo;sigo aqu&iacute;&raquo;</b>. Resuelve '
          u'que un aparato estropeado y un aparato tranquilo <b>se ven igual</b>: los dos callan. Con '
          u'latido, el que recibe puede dar la alarma si no le llega nada en un plazo. Es lo mismo que '
          u'hace el <i>Keep Alive</i> de MQTT.</p>') + pregunta(
          u'Se cae la red nueve horas y ten&eacute;is una cola de 50 mensajes en memoria. '
          u'&iquest;Basta con guardarlos?',
          u'<p>No. Hacen falta las dos cosas: <b>guardar</b> y <b>reintentar</b>. Si el aparato solo '
          u'vac&iacute;a la cola cuando le toca mandar algo nuevo, un aviso puede quedarse dentro '
          u'd&iacute;as. Y aunque reintente, la cola tiene tope: cuando caben 50 y llegan 60, diez se '
          u'pierden.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya mide bien, decide bien y avisa bien. Todo eso funciona porque <b>t&uacute; escribiste la
        regla</b>. En la sesi&oacute;n 4 entrenaste un modelo con puntos que pusiste con el
        rat&oacute;n y sal&iacute;a bonito. Ahora vas a entrenarlo con <b>vuestras medidas de
        verdad</b>, y el primer n&uacute;mero que salga va a ser estupendo. Ese es el problema.
      </div>
'''


# ==========================================================================
# SESION 7 - Entrenar con vuestros datos
# ==========================================================================
S7_RETO = u'''
      <p>En la sesi&oacute;n 4 entrenaste un clasificador pinchando puntos en un plano. Sal&iacute;a
         una recta, la recta separaba y todo el mundo qued&oacute; contento. Los puntos los
         invent&aacute;bamos nosotros.</p>
      <div class="aviso">
        <span class="n-tag">El encargo de hoy</span>
        Vuestro aparato lleva d&iacute;as midiendo. Coged <b>120 medidas</b> guardadas &mdash;treinta
        de cada una de cuatro jornadas&mdash; y poned a cada una, <b>a mano</b>, si en ese momento
        hac&iacute;a falta actuar o no. Entrenad con 40 y probad con otras 40 elegidas al azar.
      </div>
      <p>Sale un <b>93 %</b>. En un trabajo de clase eso se escribe en negrita y se pasa a la
         siguiente diapositiva.</p>
      <p>Antes de eso, hac&eacute;is una cosa que no estaba prevista: le prest&aacute;is el modelo al
         grupo de al lado para que lo pruebe en <b>su</b> maceta. Y ah&iacute; se cae.</p>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento</span>
        <p>Las 40 medidas con las que has comprobado el modelo, <b>&iquest;de d&oacute;nde han
           salido?</b> De las mismas cuatro jornadas y de las mismas macetas con las que entrenaste.
           Entonces, ese 93 %, &iquest;qu&eacute; pregunta contesta <b>exactamente</b>?</p>
      </div>
      <p>Contesta a &laquo;&iquest;c&oacute;mo le va en estas cuatro macetas?&raquo;. Y la pregunta que
         te importa era otra: <b>&laquo;&iquest;c&oacute;mo le va en una maceta que no ha visto?&raquo;</b>
         Son dos preguntas distintas, tienen dos respuestas distintas, y la diferencia entre las dos no
         est&aacute; en el modelo ni en los datos: est&aacute; en <b>c&oacute;mo los has partido</b>.</p>
'''

S7_TEORIA = u'''
      <div class="copiar">
        <h4>Cuatro cosas, y en este orden</h4>
        <ol>
          <li><b>Recoger.</b> Medidas de verdad, con su hora, de tu sensor. No valen las de internet:
              tu sensor no lee como el suyo.</li>
          <li><b>Etiquetar.</b> Una persona mira cada medida y escribe la respuesta correcta. Esto lo
              hace alguien, una a una, y es la parte cara.</li>
          <li><b>Partir.</b> Separar unos ejemplos para entrenar y <b>otros para probar</b>, y decidir
              con qu&eacute; criterio se separan. Aqu&iacute; se gana o se pierde todo.</li>
          <li><b>Medir.</b> Los tres n&uacute;meros de la sesi&oacute;n 4, y uno m&aacute;s que
              a&ntilde;adimos hoy.</li>
        </ol>
      </div>
      <p>La escena tiene las 120 medidas. Cambia el mando de <b>&laquo;parto los datos&raquo;</b> de
         <b>al azar</b> a <b>por jornada</b> y no toques nada m&aacute;s: ni los ejemplos, ni el modelo,
         ni el n&uacute;mero de ejemplos. Mira las dos filas de acierto.</p>
''' + DATOS + u'''
      <div class="copiar">
        <h4>Lo que acaba de pasar</h4>
        <p>Los mismos 40 ejemplos. El mismo modelo. El mismo acierto sobre los suyos. Y el acierto
           sobre los de prueba baja de un <b>93 %</b> a un <b>73 %</b>.</p>
        <p>No es que el modelo se haya estropeado: es que la primera vez le estabas preguntando
           <b>por lo que ya sab&iacute;a</b>. Cuando el conjunto de prueba viene del mismo sitio, del
           mismo d&iacute;a y del mismo sensor que el de entrenamiento, el n&uacute;mero que sale est&aacute;
           <b>inflado</b>. En ingl&eacute;s a esto se le llama <i>data leakage</i>; en castellano,
           <b>fuga</b>: informaci&oacute;n del conjunto de prueba que se ha colado en el de
           entrenamiento sin que nadie la invitara.</p>
        <p><b>La regla, que es de las que se escriben en la primera p&aacute;gina:</b> el conjunto de
           prueba tiene que ser de <b>otro d&iacute;a, otro sitio u otro aparato</b>. Si no puedes
           conseguir eso, di en la memoria que tu n&uacute;mero es un <b>techo</b>, no una medida.</p>
      </div>
      <div class="copiar">
        <h4>Los dos suelos que hay que superar</h4>
        <p>En la sesi&oacute;n 4 aparecieron los tres n&uacute;meros. Hoy hacen falta los cuatro:</p>
        <ol>
          <li>Acierto sobre <b>sus propios ejemplos</b>. No dice nada.</li>
          <li>Acierto sobre <b>los de prueba</b>, bien separados. Es la medida.</li>
          <li>Lo que acertar&iacute;a el <b>modelo tonto</b> que dice siempre lo mismo. Primer suelo.</li>
          <li><b>Lo que acertar&iacute;a un <code>si</code> de una l&iacute;nea</b>: el mejor umbral que
              puedas escribir a mano. Segundo suelo, y es el que se olvida.</li>
        </ol>
        <p>Si tu modelo no le gana a los dos, <b>no lo pongas</b>. Un <code>si</code> se lee, se
           depura, se explica en la defensa y cabe en 2 kB de memoria. Un modelo entrenado, ninguna de
           las cuatro cosas.</p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Dale a la escena <b>&laquo;solo la lectura&raquo;</b> y mira la fila del umbral. Con una
           sola caracter&iacute;stica, <b>entrenar y poner un umbral son exactamente lo mismo</b>: el
           modelo solo puede aprender un n&uacute;mero a partir del cual dice que s&iacute;. Toda la
           gracia de entrenar aparece cuando le das <b>dos o m&aacute;s</b> caracter&iacute;sticas y la
           regla que las combina no es evidente. Con la lectura <b>y</b> la tendencia
           &mdash;lo que guardasteis en la sesi&oacute;n 5&mdash; el acierto sube de un 75 % a un
           93 %.</p>
      </div>
      <p>Y queda la pregunta de la que nadie habla: <b>&iquest;cu&aacute;ntos ejemplos hacen
         falta?</b> La curva de abajo de la escena lo dice para estos datos. Y para tener una idea de
         lo que significa &laquo;muchos&raquo;, mira esta foto:</p>
''' + foto('c6-computers-harvard.jpg',
           u'Fotograf&iacute;a antigua en blanco y negro: seis mujeres sentadas a dos mesas llenas de '
           u'papeles y placas fotogr&aacute;ficas, en una sala con estanter&iacute;as de libros y cajas',
           u'Observatorio de la Universidad de Harvard, hacia <b>1890</b>. Estas mujeres &mdash;de pie, '
           u'<b>Williamina Fleming</b>; entre las sentadas est&aacute; muy probablemente <b>Annie Jump '
           u'Cannon</b>&mdash; se dedicaban a mirar placas fotogr&aacute;ficas del cielo con lupa y '
           u'<b>escribir a mano, estrella por estrella</b>, a qu&eacute; tipo pertenec&iacute;a cada '
           u'una. Su cargo se llamaba literalmente <i>computer</i>, computadora: la persona que hace '
           u'las cuentas. De ese trabajo sali&oacute; el <b>Cat&aacute;logo Henry Draper</b>, publicado '
           u'entre 1918 y 1924, con <b>225.300 estrellas clasificadas</b>. Todo conjunto de ejemplos '
           u'etiquetados del mundo, incluidos los que entrenan la IA de la que se habla hoy, empieza '
           u'con gente haciendo esto.',
           u'Harvard University Archives', u'dominio p&uacute;blico',
           u'https://commons.wikimedia.org/wiki/File:Observatory_data_analysis_by_women_computers,_circa_1890.jpg') + u'''
      <div class="copiar">
        <h4>D&oacute;nde acaba lo que pod&eacute;is decir</h4>
        <p>Con 120 medidas de cuatro macetas de un aula, y con la comprobaci&oacute;n hecha como es
           debido, pod&eacute;is afirmar esto y nada m&aacute;s:</p>
        <p style="border-left:4px solid var(--goo-verde);padding-left:12px;margin:10px 0">
           &laquo;Un modelo entrenado con 40 medidas de tres macetas de nuestra aula acert&oacute; el
           <b>73 %</b> en una cuarta maceta que no hab&iacute;a visto, frente al <b>50 %</b> de un
           modelo que dijera siempre lo mismo. No sabemos c&oacute;mo se comporta con otra tierra, otro
           sensor ni en otra &eacute;poca del a&ntilde;o.&raquo;</p>
        <p>Eso es una frase verdadera y defendible. <b>&laquo;Hemos hecho una IA que detecta cu&aacute;ndo
           regar&raquo; no lo es</b>, y en la defensa la primera pregunta va a ser esa. Cuarenta
           medidas no son un modelo: son un indicio.</p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Dos detalles t&eacute;cnicos de la escena, por si los notas:</p>
        <ul>
          <li>El entrenamiento es el mismo perceptr&oacute;n de la sesi&oacute;n 4, pero
              <b>de bolsillo</b>: va guardando los mejores pesos que ha encontrado. Hace falta porque
              estos ejemplos <b>no se pueden separar del todo</b> con una recta, y sin eso el
              resultado depender&iacute;a de con qu&eacute; ejemplo acab&oacute; la &uacute;ltima
              pasada. Lo invent&oacute; Stephen Gallant en 1990, treinta a&ntilde;os despu&eacute;s del
              perceptr&oacute;n original.</li>
          <li>La curva de acierto <b>no sube en l&iacute;nea recta</b>: da saltos. Con conjuntos de
              prueba de 30 o 40 ejemplos, un ejemplo mal clasificado son dos o tres puntos
              porcentuales. Con estos tama&ntilde;os hay que leer la <b>tendencia</b>, no las
              diferencias de tres puntos.</li>
        </ul>
      </div>
''' + video('video-c6-overfit', 'MR0YTI5OB9I',
            u'&iquest;Qu&eacute; es el Overfitting? Explicaci&oacute;n del sobreajuste sencilla en espa&ntilde;ol',
            u'Canal: Tech Portal Formaci&oacute;n',
            u'El mismo problema visto desde el lado del modelo: aprenderse los ejemplos en vez de '
            u'aprender el problema.')

S7_PRACTICA = ficha(
    u'Actividad 7 &middot; &iquest;Modelo o <code>si</code>? Decidirlo con n&uacute;meros',
    [u'4.2', u'5.1', u'C.1', u'C.4'], u'Parejas &middot; 20 min', u'''
          <h4>Primera parte &middot; etiquetar de verdad (6 min)</h4>
          <p>Coged <b>veinte</b> lecturas de vuestro registro (las de la sesi&oacute;n 5 valen) y
             poned a cada una, a mano, un <b>S&iacute;</b> o un <b>No</b>: &iquest;hab&iacute;a que
             actuar en ese momento? Cronometrad cu&aacute;nto tard&aacute;is.</p>
          <ol class="pasos">
            <li>Anotad los <b>segundos por ejemplo</b> y calculad cu&aacute;nto costar&iacute;a etiquetar
                500, y cu&aacute;nto 10.000.</li>
            <li>Anotad <b>en cu&aacute;ntas dudasteis</b>. Si dud&aacute;is vosotros, el modelo tampoco
                va a saberlo: eso es un l&iacute;mite de los datos, no del modelo.</li>
          </ol>
          <h4>Segunda parte &middot; la tabla que decide (8 min)</h4>
          <p>Con la escena en <b>vuestro</b> proyecto y <b>40 ejemplos</b>, rellenad las cuatro
             combinaciones:</p>
          <table style="width:100%;border-collapse:collapse;font-size:14.5px;margin:8px 0">
            <tr style="text-align:left;border-bottom:1.5px solid var(--line)">
              <th></th><th>en sus ejemplos</th><th>en los de prueba</th><th>modelo tonto</th>
              <th>umbral a mano</th></tr>
            <tr><td>al azar, solo la lectura</td><td></td><td></td><td></td><td></td></tr>
            <tr><td>al azar, lectura + tendencia</td><td></td><td></td><td></td><td></td></tr>
            <tr><td>por jornada, solo la lectura</td><td></td><td></td><td></td><td></td></tr>
            <tr><td>por jornada, lectura + tendencia</td><td></td><td></td><td></td><td></td></tr>
          </table>
          <p>Debajo, contestad: &iquest;cu&aacute;l de las cuatro filas es la que hay que escribir en
             la memoria del proyecto, y <b>por qu&eacute;</b>?</p>
          <h4>Tercera parte &middot; la decisi&oacute;n, escrita (6 min)</h4>
          <p>Escribid el p&aacute;rrafo que ir&aacute; en vuestra memoria. Tiene que decir tres cosas:</p>
          <ol class="pasos">
            <li>Si en vuestro aparato va a haber un <b>modelo entrenado</b> o un <b><code>si</code>
                con un umbral</b>.</li>
            <li><b>Con qu&eacute; n&uacute;mero</b> de la tabla lo justific&aacute;is.</li>
            <li>Una frase, como la del recuadro verde, que diga <b>hasta d&oacute;nde</b> vale lo que
                hab&eacute;is medido y d&oacute;nde deja de valer.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Las veinte etiquetas puestas y el tiempo cronometrado <b>(2 puntos)</b>.</li>
            <li>Las cuentas de 500 y 10.000 ejemplos <b>(1 punto)</b>.</li>
            <li>La tabla de las cuatro filas, completa <b>(3 puntos)</b>.</li>
            <li>Se elige la fila <b>por jornada</b> y se explica por qu&eacute; <b>(2 puntos)</b>.</li>
            <li>El p&aacute;rrafo de la memoria dice hasta d&oacute;nde vale <b>(2 puntos)</b>.</li>
          </ul>
''')

S7_CIERRE = u'''
      <ol>
      ''' + pregunta(u'Tu modelo acierta el 93 % con los datos partidos al azar y el 73 % dejando '
                     u'fuera una jornada. &iquest;Cu&aacute;l de los dos escribes en la memoria?',
                     u'<p>El <b>73 %</b>. El otro est&aacute; inflado: los ejemplos de prueba ven&iacute;an '
                     u'de las mismas jornadas y el mismo sensor con los que entrenaste, as&iacute; que '
                     u'contestaba a &laquo;&iquest;c&oacute;mo le va donde ya ha estado?&raquo;, que no '
                     u'es la pregunta.</p>') + pregunta(
          u'&iquest;Qu&eacute; es una fuga entre el conjunto de entrenamiento y el de prueba?',
          u'<p>Que los dos se parecen demasiado porque comparten algo &mdash;el mismo d&iacute;a, el '
          u'mismo aparato, el mismo sitio&mdash;, y entonces el acierto sobre los de prueba mide una '
          u'cosa m&aacute;s f&aacute;cil que la de verdad. Se evita partiendo por d&iacute;a, por '
          u'aparato o por sitio, nunca al azar sin pensarlo.</p>') + pregunta(
          u'&iquest;Por qu&eacute; hay que comparar el modelo con un <code>si</code> de una '
          u'l&iacute;nea, y no solo con el modelo tonto?',
          u'<p>Porque un <code>si</code> con un buen umbral suele acertar bastante, y <b>es mejor por '
          u'todo lo dem&aacute;s</b>: se lee, se depura, se explica en la defensa y cabe en la placa. '
          u'Si el modelo no le gana claramente al <code>si</code>, no compensa.</p>') + pregunta(
          u'&iquest;Qu&eacute; se puede afirmar con 40 medidas de tres macetas de vuestra aula?',
          u'<p>Que el modelo acert&oacute; <b>ese porcentaje</b> en <b>una cuarta maceta de esa misma '
          u'aula</b>, y nada m&aacute;s. No se puede decir nada de otra tierra, otro sensor ni otra '
          u'&eacute;poca. Cuarenta medidas no son un modelo: son un indicio, y en la memoria se '
          u'escribe como indicio.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya tienes las cuatro piezas: mide, se acuerda, decide y avisa. Y dentro de tres semanas hay
        que <b>ense&ntilde;arlo funcionando</b>, tres minutos, delante de gente. Lo que se cae en esa
        mesa casi nunca es el sensor: es algo que el programa <b>no ten&iacute;a previsto</b>. As&iacute;
        que la &uacute;ltima sesi&oacute;n va de romperlo t&uacute; antes.
      </div>
'''


# ==========================================================================
# SESION 8 - El sistema completo
# ==========================================================================
S8_RETO = u'''
      <p>Se acab&oacute; de a&ntilde;adir piezas. Hoy se junta todo y se prepara lo &uacute;nico que
         va a ver el que venga a mirarlo: <b>el aparato funcionando</b>, tres minutos, con gente
         delante que no sabe qu&eacute; es un <code>analogRead()</code>.</p>
      <div class="aviso">
        <span class="n-tag">El encargo de hoy</span>
        <b>Dos minutos</b>, sin mirar la pantalla: escribid en el cuaderno <b>qu&eacute; hace vuestro
        programa</b>, l&iacute;nea a l&iacute;nea, si el d&iacute;a antes de la presentaci&oacute;n
        alguien saca la sonda del tiesto al limpiar y no la vuelve a meter.
      </div>
      <p>La respuesta honesta es siempre la misma: <b>riega</b>. Y luego vuelve a regar. Y sigue
         regando, porque la sonda al aire da una lectura de tierra sequ&iacute;sima y el programa hace
         exactamente lo que le mandasteis.</p>
      <p>Lo ingenuo aqu&iacute; es &laquo;lo probamos otra vez antes de presentarlo&raquo;. Probar que
         funciona <b>no demuestra nada</b>: solo repite el caso bueno, que es el &uacute;nico que ya
         sab&iacute;as que funcionaba. Lo que hay que probar es lo otro.</p>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento</span>
        <p>Vuestro programa tiene una l&iacute;nea que dice, m&aacute;s o menos,
           <code>si media &gt; 700 entonces riega</code>. &iquest;D&oacute;nde podr&iacute;a
           poner, en esa l&iacute;nea, <b>&laquo;esta lectura no me la creo&raquo;</b>?</p>
      </div>
      <p>En ning&uacute;n sitio. Y no es por torpeza: es porque un programa escrito como una lista de
         instrucciones que se ejecutan una detr&aacute;s de otra <b>no tiene d&oacute;nde guardar
         &laquo;en qu&eacute; situaci&oacute;n estoy&raquo;</b>. Para poder desconfiar hace falta que
         el programa sepa en qu&eacute; estado est&aacute;, y eso se escribe de otra manera.</p>
'''

S8_TEORIA = u'''
      <div class="copiar">
        <h4>El programa como m&aacute;quina de estados</h4>
        <p>Una <b>m&aacute;quina de estados</b> es un programa escrito as&iacute;: en cada momento
           est&aacute; en <b>uno</b> de unos pocos estados con nombre, en cada estado hace una cosa
           distinta, y se pasa de uno a otro solo por las <b>transiciones</b> que t&uacute; hayas
           dibujado. No es un invento para esto: es como se escriben los sem&aacute;foros, los cajeros,
           los ascensores y los lavavajillas.</p>
        <pre style="font-family:var(--f-m);font-size:12.5px;line-height:1.6;margin:8px 0;white-space:pre-wrap">enum Estado { ARRANQUE, VIGILANDO, ACTUANDO, ESPERA, SEGURO };
Estado estado = ARRANQUE;

void loop() {
  int x = leer();
  guarda(x);
  if (estado != SEGURO &amp;&amp; sospechoso()) { estado = SEGURO; avisa("me paro"); }

  switch (estado) {
    case ARRANQUE:  if (historicoLleno()) estado = VIGILANDO;        break;
    case VIGILANDO: if (media() &gt; UMBRAL) estado = ACTUANDO;         break;
    case ACTUANDO:  actua(); avisa("he actuado"); estado = ESPERA;   break;
    case ESPERA:    if (millis() - t &gt; ESPERA_MS) estado = VIGILANDO; break;
    case SEGURO:    /* no hace nada, y no sale solo */               break;
  }
}</pre>
        <p>Dos cosas que solo se pueden escribir as&iacute;: el estado <b>ESPERA</b>, que impide volver
           a actuar antes de que se note lo anterior, y el estado <b>SEGURO</b>, que no existe en
           ninguna lista de instrucciones y que es el que salva el proyecto.</p>
      </div>
      <p>Aqu&iacute; tienes el sistema entero corriendo catorce d&iacute;as, con los cinco estados
         dibujados arriba. Mueve el mando de <b>instante</b> y mira c&oacute;mo se ilumina uno u otro.
         Y despu&eacute;s enciende la primera aver&iacute;a &mdash;<b>la sonda se sale del
         tiesto</b>&mdash; con el <b>modo seguro quitado</b>.</p>
''' + SISTEMA + u'''
      <div class="copiar">
        <h4>El modo seguro</h4>
        <p><b>Modo seguro</b>: el estado en el que el aparato <b>deja de actuar</b>, se queda quieto y
           <b>avisa de que se ha parado</b>. No es un fallo: es la respuesta prevista a que algo no
           cuadre.</p>
        <p>Hay que decidir <b>tres</b> cosas, y son de examen:</p>
        <ol>
          <li><b>Qu&eacute; lo dispara.</b> No vale &laquo;si algo va mal&raquo;. Tienen que ser
              condiciones que el programa pueda comprobar. Las dos de la escena valen para cualquiera
              de los tres proyectos:
              <ul>
                <li>la lectura <b>no se ha movido nada en seis horas</b> (un sensor de verdad siempre
                    tiembla un poco: si no tiembla, es que no est&aacute; midiendo);</li>
                <li>ha tenido que actuar <b>m&aacute;s de ocho veces en 24 horas</b> (si tu planta
                    necesita ocho riegos en un d&iacute;a, el problema no es la planta).</li>
              </ul></li>
          <li><b>Qu&eacute; hace mientras.</b> Lo m&aacute;s seguro suele ser <b>no hacer nada</b>,
              pero hay que pensarlo: en la l&aacute;mpara, quedarse apagada es seguro; en un
              calefactor, no.</li>
          <li><b>C&oacute;mo se sale.</b> Y la respuesta correcta es: <b>a mano</b>. Del modo seguro
              no se sale solo, porque si se saliera solo volver&iacute;a a meterse, y a salir, y el
              aviso se convertir&iacute;a en ruido.</li>
        </ol>
      </div>
''' + foto('c6-seta-emergencia.jpg',
           u'Cuadro de mandos gris con una seta roja de emergencia sobre un rect&aacute;ngulo amarillo, '
           u'dos pulsadores blancos rotulados JOG, un piloto rojo y un interruptor ON/OFF',
           u'El modo seguro de toda la vida, en su versi&oacute;n de hierro: la <b>seta de '
           u'emergencia</b> de un cuadro de mandos de taller. F&iacute;jate en dos detalles que son '
           u'exactamente las decisiones de arriba. Primero, el <b>color y el fondo amarillo</b> est&aacute;n '
           u'normalizados para que se encuentre sin pensar. Y segundo, las <b>flechas circulares</b> '
           u'dibujadas encima: para soltarla hay que <b>girarla</b>, no basta con volver a pulsar. '
           u'Salir del paro tiene que costar, y tiene que hacerlo una persona. Tu <code>case SEGURO</code> '
           u'hace lo mismo con software.',
           u'Cjp24', u'CC BY-SA 3.0',
           u'https://commons.wikimedia.org/wiki/File:Emergency_stop_button.jpg') + u'''
      <div class="copiar">
        <h4>La ficha con la que se defiende un proyecto</h4>
        <p>En la presentaci&oacute;n no se defiende una opini&oacute;n: se defienden <b>n&uacute;meros
           medidos</b>. Estos son los que hay que llevar, y todos salen de la escena o de vuestro
           propio registro:</p>
        <ol>
          <li><b>Cu&aacute;ntas veces actu&oacute;</b> en el periodo, y <b>cu&aacute;ntas de m&aacute;s</b>.</li>
          <li><b>Cu&aacute;nto tiempo estuvo el problema sin resolver</b>, y cu&aacute;nto se pas&oacute;
              de rosca. Son <b>dos</b> filas, no una: los dos fallos de la sesi&oacute;n 4.</li>
          <li><b>Cu&aacute;ntos avisos mand&oacute;</b> y cu&aacute;ntos llegaron.</li>
          <li><b>Cu&aacute;ntos registros guard&oacute;</b> y cu&aacute;ntos no cupieron.</li>
          <li><b>Cu&aacute;ntas veces entr&oacute; en modo seguro</b> y por qu&eacute;.</li>
          <li><b>Cu&aacute;nto tard&oacute; una persona en enterarse</b> de la primera aver&iacute;a.</li>
          <li><b>En qu&eacute; estado acab&oacute;.</b></li>
        </ol>
        <p>Y despu&eacute;s, una tabla de <b>aver&iacute;as</b>: qu&eacute; le hicisteis, qu&eacute;
           hizo &eacute;l y qu&eacute; fila de arriba se movi&oacute;. Esa tabla es la que separa un
           proyecto que <b>funciona</b> de uno que <b>funcion&oacute; el d&iacute;a de la foto</b>.</p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Dos datos del Arduino Uno que salen en la escena y conviene saber de d&oacute;nde vienen:</p>
        <ul>
          <li>La <b>EEPROM</b> son <b>1.024 bytes</b>, y es la &uacute;nica memoria de la placa que
              sobrevive al apagado. A 8 bytes por registro caben <b>128 registros</b>: guardando uno
              cada media hora se llena en <b>2 d&iacute;as y 16 horas</b>. Por eso el mando de
              &laquo;guardo solo cuando pasa algo&raquo; cambia tanto.</li>
          <li>Cada celda de esa EEPROM aguanta unas <b>100.000 escrituras</b> y se gasta. Un registro
              cada media hora durante un curso son unas 12.000: cabe de sobra. Un registro por
              segundo se la carga en <b>un d&iacute;a</b>. En la memoria RAM esto no pasa; en la
              EEPROM, s&iacute;.</li>
        </ul>
        <p>Y un pariente cercano del modo seguro, un piso m&aacute;s abajo: el <b>perro guardi&aacute;n</b>
           (<i>watchdog</i>) que el propio chip lleva dentro. Es un contador que hay que poner a cero
           cada poco desde el programa; si el programa se cuelga y deja de hacerlo, el contador llega
           al final y <b>reinicia la placa</b>. La misma idea que el latido de la sesi&oacute;n 6:
           dejar de dar se&ntilde;ales de vida <b>es</b> una se&ntilde;al.</p>
      </div>
      <div class="nota">
        <span class="n-tag">D&oacute;nde acaba esta unidad</span>
        Aqu&iacute; se prepara <b>el contenido t&eacute;cnico</b> de la defensa: la m&aacute;quina de
        estados, el modo seguro y la ficha de n&uacute;meros. C&oacute;mo se presenta &mdash;el
        gui&oacute;n, los apoyos, hablar en p&uacute;blico&mdash; es el criterio 3.1 y se trabaja en
        las unidades 1 y 2. El <b>impacto ambiental</b> de lo que hab&eacute;is construido se mide
        aqu&iacute; como una fila m&aacute;s, pero se trata en la <b>unidad 8</b>.
      </div>
''' + video('video-c6-estados', 'z3geTtX4Fvo',
            u'Programar Arduino como si fuera una m&aacute;quina de estados finitos',
            u'Canal: Construyendo a Chispas',
            u'La m&aacute;quina de estados escrita de cero en Arduino, con el <code>switch</code> '
            u'delante.')

S8_PRACTICA = ficha(
    u'Actividad 8 &middot; R&oacute;mpelo t&uacute; y prepara la ficha',
    [u'4.2', u'5.1', u'C.1', u'C.3', u'C.4'], u'Grupos de tres &middot; 20 min', u'''
          <h4>Primera parte &middot; vuestra m&aacute;quina de estados (7 min)</h4>
          <p>Dibujad en la libreta los estados de <b>vuestro</b> proyecto, con una flecha por cada
             transici&oacute;n y, encima de cada flecha, <b>la condici&oacute;n que la dispara</b>. Y
             al lado, escribid el <code>switch</code> con sus <code>case</code>: no hace falta que
             compile, hace falta que est&eacute;n todos los estados.</p>
          <p>Dos preguntas que hay que contestar dentro del dibujo: <b>&iquest;qu&eacute; dispara
             vuestro modo seguro?</b> (dos condiciones comprobables, no &laquo;si algo va mal&raquo;)
             y <b>&iquest;c&oacute;mo se sale de &eacute;l?</b></p>
          <h4>Segunda parte &middot; la tabla de aver&iacute;as (7 min)</h4>
          <p>Con la escena en vuestro proyecto, encended las aver&iacute;as <b>de una en una</b> y
             anotad qu&eacute; fila de la ficha se mueve:</p>
          <table style="width:100%;border-collapse:collapse;font-size:14.5px;margin:8px 0">
            <tr style="text-align:left;border-bottom:1.5px solid var(--line)">
              <th>aver&iacute;a</th><th>sin protecci&oacute;n</th><th>con protecci&oacute;n</th>
              <th>qu&eacute; fila lo delata</th></tr>
            <tr><td>la sonda se sale</td><td></td><td></td><td></td></tr>
            <tr><td>se cae la red</td><td></td><td></td><td></td></tr>
            <tr><td>se va la luz</td><td></td><td></td><td></td></tr>
            <tr><td>nadie mira el m&oacute;vil</td><td></td><td></td><td></td></tr>
          </table>
          <p>Y una pregunta con trampa: con la sonda fuera y el modo seguro puesto, el tiempo con el
             problema sin resolver <b>sube</b>. &iquest;Est&aacute; entonces el modo seguro
             empeorando las cosas? Contestad en dos frases.</p>
          <h4>Tercera parte &middot; los tres minutos (6 min)</h4>
          <p>Escribid el gui&oacute;n de la demostraci&oacute;n, con los tiempos marcados:</p>
          <ol class="pasos">
            <li><b>0:00-0:30</b> &mdash; el problema, en una frase, y d&oacute;nde est&aacute; en el
                centro.</li>
            <li><b>0:30-1:30</b> &mdash; el aparato funcionando. Decid <b>c&oacute;mo vais a provocar
                que act&uacute;e</b> delante de la gente, sin esperar a que se seque una maceta.</li>
            <li><b>1:30-2:15</b> &mdash; <b>lo romp&eacute;is vosotros</b> delante de todos (sacad la
                sonda) y ense&ntilde;&aacute;is el modo seguro y el aviso en el m&oacute;vil.</li>
            <li><b>2:15-3:00</b> &mdash; tres n&uacute;meros de la ficha y la frase de hasta
                d&oacute;nde vale lo que hab&eacute;is medido.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>El diagrama de estados, con las condiciones en las flechas <b>(2 puntos)</b>.</li>
            <li>El <code>switch</code>, con todos los estados <b>(2 puntos)</b>.</li>
            <li>Las dos condiciones del modo seguro son <b>comprobables</b> <b>(1 punto)</b>.</li>
            <li>La tabla de aver&iacute;as, completa <b>(2 puntos)</b>.</li>
            <li>La respuesta a la pregunta con trampa dice que el modo seguro <b>no arregla, avisa</b>
                <b>(1 punto)</b>.</li>
            <li>El gui&oacute;n de tres minutos, con la rotura dentro <b>(2 puntos)</b>.</li>
          </ul>
''')

PREGUNTAS_TEST_B = [
    dict(p=u'La bomba de vuestro riego arranc&oacute; de madrugada con la tierra mojada. '
           u'&iquest;Cu&aacute;l es la causa m&aacute;s probable?',
         op=[u'El umbral estaba demasiado bajo y hay que subirlo.',
             u'Una medida suelta dio un valor falso y el programa, que decide con una sola medida, '
             u'se la crey&oacute;.',
             u'El conversor A/D se estrope&oacute;.'],
         ok=1,
         por=u'Basta con que alguien roce la sonda para que una lectura no corresponda a nada. Si el '
             u'programa decide con el valor de ese instante, act&uacute;a. Subir el umbral no lo '
             u'arregla: lo sube tambi&eacute;n para los casos de verdad.'),
    dict(p=u'&iquest;Qu&eacute; hace la l&iacute;nea <code>pos = (pos + 1) % N;</code> de un buffer '
           u'circular?',
         op=[u'Calcula la media de las N medidas.',
             u'Hace que el &iacute;ndice vuelva a 0 al llegar al final, para escribir encima de la '
             u'medida m&aacute;s vieja.',
             u'Divide la lectura entre N para que quepa en un byte.'],
         ok=1,
         por=u'Es el resto de la divisi&oacute;n: cuando <code>pos</code> llega a N, <code>N % N</code> '
             u'vale 0. Sin esa l&iacute;nea el programa escribe fuera del array, encima de otras '
             u'variables, y en Arduino eso no da error.'),
    dict(p=u'Tu sensor da de vez en cuando un pico enorme de un solo instante. &iquest;Media o '
           u'mediana?',
         op=[u'Media, que es m&aacute;s f&aacute;cil de programar.',
             u'Mediana: el pico se va a un extremo de la lista ordenada y no entra en la cuenta.',
             u'Da igual, las dos hacen lo mismo con los mismos bytes.'],
         ok=1,
         por=u'La media <b>reparte</b> el pico entre las N medidas, o sea que lo estira: contamina N '
             u'decisiones en vez de una. La mediana lo <b>tira</b>. Ocupan los mismos bytes, pero no '
             u'sirven para lo mismo.'),
    dict(p=u'&iquest;Qu&eacute; se paga siempre por decidir con la media de N medidas, haya picos o no?',
         op=[u'Nada, alisar es gratis.',
             u'2N bytes de memoria y un retraso de unas N/2 medidas en enterarse.',
             u'Que el conversor pierde resoluci&oacute;n.'],
         ok=1,
         por=u'La memoria se cuenta (2N bytes de los 2.048 de un Uno) y el retraso tambi&eacute;n: con '
             u'medidas cada dos minutos, una media de 20 tarda unos 20 minutos en enterarse de un '
             u'cambio.'),
    dict(p=u'<code>int suma = 0;</code> y luego se suman 40 lecturas de hasta 1023. '
           u'&iquest;Qu&eacute; pasa?',
         op=[u'Nada: 40.920 cabe de sobra.',
             u'Se desborda, porque un <code>int</code> llega a 32.767, y la media sale mal sin que el '
             u'programa avise.',
             u'El compilador da un error y no deja subir el sketch.'],
         ok=1,
         por=u'Es el mismo desbordamiento de la sesi&oacute;n 1, ahora escondido en el acumulador de '
             u'la media. Se arregla con <code>long suma = 0;</code>, que son 2 bytes m&aacute;s una '
             u'sola vez.'),
    dict(p=u'Vuestro Arduino Uno tiene que mandar el dato fuera del aula. &iquest;Qu&eacute; hace falta?',
         op=[u'Nada, el Uno lleva wifi.',
             u'Un ordenador que lea el puerto serie, o un m&oacute;dulo ESP-01 (~2 &euro;), o cambiar '
             u'la placa por un ESP32.',
             u'Activar el wifi por software en el <code>setup()</code>.'],
         ok=1,
         por=u'El Uno no tiene wifi ni Ethernet. Las tres soluciones tienen precio y pega, y eso va en '
             u'la memoria del proyecto: el m&oacute;dulo ESP-01, adem&aacute;s, funciona a 3,3 V y el '
             u'Uno saca 5 V.'),
    dict(p=u'&iquest;Para qu&eacute; sirve un <b>latido</b> si el aparato ya avisa cuando pasa algo?',
         op=[u'Para que la gr&aacute;fica quede m&aacute;s bonita.',
             u'Porque un aparato estropeado y uno tranquilo se ven igual: los dos callan. El latido '
             u'hace que el silencio se pueda detectar.',
             u'Para sincronizar la hora de la placa con el servidor.'],
         ok=1,
         por=u'Con avisos solo por evento, dejar de mandar no se distingue de que todo vaya bien. El '
             u'latido pone el silencio del lado de las aver&iacute;as. Es lo que hace el '
             u'<i>Keep Alive</i> de MQTT.'),
    dict(p=u'Se cae la red nueve horas y el aparato guarda en memoria lo que no puede mandar. '
           u'&iquest;Basta?',
         op=[u'S&iacute;: si se guarda, no se pierde nada.',
             u'No: hace falta adem&aacute;s <b>reintentar</b> al volver la red, y aun as&iacute; la '
             u'cola tiene tope.',
             u'No: hay que mandarlo todo dos veces por si acaso.'],
         ok=1,
         por=u'Guardar sin reintentar es perder despacio: el aviso puede quedarse dentro d&iacute;as. '
             u'Y con 1.200 bytes y mensajes de 24 caben 50: lo que llegue despu&eacute;s se pierde '
             u'igual.'),
    dict(p=u'Entrenas con 40 medidas y pruebas con otras 40 <b>elegidas al azar de las mismas '
           u'jornadas</b>. Sale un 93 %. &iquest;Qu&eacute; mide ese n&uacute;mero?',
         op=[u'C&oacute;mo le ir&aacute; en cualquier maceta.',
             u'C&oacute;mo le va en esas mismas jornadas y con ese mismo sensor, que no es la pregunta '
             u'que importa.',
             u'Que el modelo est&aacute; bien entrenado y ya se puede usar.'],
         ok=1,
         por=u'Es una <b>fuga</b>: el conjunto de prueba comparte d&iacute;a, sitio y sensor con el de '
             u'entrenamiento. Dejando fuera una jornada entera, el mismo modelo con los mismos '
             u'ejemplos baja al 73 %.'),
    dict(p=u'&iquest;Con qu&eacute; dos cosas hay que comparar siempre un modelo entrenado?',
         op=[u'Con otro modelo m&aacute;s grande y con uno m&aacute;s peque&ntilde;o.',
             u'Con el modelo tonto que dice siempre lo mismo, y con el mejor <code>si</code> de una '
             u'l&iacute;nea que puedas escribir a mano.',
             u'Con el mismo modelo entrenado dos veces, para ver si sale igual.'],
         ok=1,
         por=u'Son los dos suelos. Si no les gana a los dos, no lo pongas: un <code>si</code> se lee, '
             u'se depura, se explica en la defensa y cabe en 2 kB de memoria.'),
    dict(p=u'&iquest;Qu&eacute; es exactamente el <b>modo seguro</b> de vuestro aparato?',
         op=[u'Un modo que arregla la aver&iacute;a y sigue funcionando.',
             u'Un estado en el que deja de actuar, se queda quieto, avisa de que se ha parado y del '
             u'que <b>no se sale solo</b>.',
             u'Bajar la potencia del actuador a la mitad hasta que alguien lo mire.'],
         ok=1,
         por=u'No arregla nada: para la m&aacute;quina y pide un humano. Y se sale a mano a '
             u'prop&oacute;sito, igual que una seta de emergencia, que hay que girar para soltarla.'),
    dict(p=u'Con la sonda fuera del tiesto y <b>sin</b> modo seguro, el aparato manda 216 avisos, y 198 de '
           u'ellos dicen &laquo;he regado&raquo;. &iquest;Por qu&eacute; es eso peor que no mandar ninguno?',
         op=[u'Porque gasta datos.',
             u'Porque ninguno de esos avisos dice que algo va mal: son los mismos que mandar&iacute;a '
             u'si todo fuera bien, solo que muchos.',
             u'Porque llena la EEPROM.'],
         ok=1,
         por=u'Una aver&iacute;a que se manifiesta como &laquo;m&aacute;s de lo normal&raquo; no se '
             u'detecta sola: hace falta que el programa sospeche y mande un aviso <b>distinto</b>. Si '
             u'no, el que recibe ve actividad y supone que todo va bien.'),
]

S8_CIERRE = u'''
      <ol>
      ''' + pregunta(u'&iquest;Por qu&eacute; no se puede escribir &laquo;esta lectura no me la '
                     u'creo&raquo; dentro de un <code>si media &gt; 700</code>?',
                     u'<p>Porque para desconfiar hay que <b>comparar con algo</b>: con lo que le&iacute;a '
                     u'antes, con cu&aacute;ntas veces ha actuado hoy, con en qu&eacute; situaci&oacute;n '
                     u'est&aacute;. Un programa escrito como una lista de instrucciones no guarda nada '
                     u'de eso. Una m&aacute;quina de estados s&iacute;.</p>') + pregunta(
          u'Dad dos condiciones <b>comprobables</b> que puedan disparar el modo seguro.',
          u'<p>Que la lectura <b>no se haya movido nada en seis horas</b> (un sensor de verdad siempre '
          u'tiembla: si no tiembla, no est&aacute; midiendo) y que el aparato haya tenido que actuar '
          u'<b>m&aacute;s de ocho veces en 24 horas</b>. Las dos las puede comprobar el programa; '
          u'&laquo;si algo va mal&raquo; no.</p>') + pregunta(
          u'Con la sonda fuera y el modo seguro puesto, el tiempo con la tierra seca <b>sube</b>. '
          u'&iquest;Es entonces peor el modo seguro?',
          u'<p>No, pero hay que decirlo bien: el modo seguro <b>no arregla el problema, lo hace '
          u'visible</b>. Para la m&aacute;quina y pide un humano. Sin &eacute;l la planta no est&aacute; '
          u'mejor: est&aacute; ahogada por doscientos riegos, y nadie se ha enterado. Lo que hace el '
          u'modo seguro es cambiar un fallo silencioso por uno que avisa.</p>') + pregunta(
          u'&iquest;Qu&eacute; tiene que llevar la ficha con la que defend&eacute;is el proyecto?',
          u'<p><b>N&uacute;meros medidos</b>, no impresiones: veces que actu&oacute; y de ellas '
          u'cu&aacute;ntas de m&aacute;s, tiempo con el problema sin resolver y tiempo pasado de rosca, '
          u'avisos mandados y llegados, registros guardados y perdidos, veces en modo seguro, '
          u'cu&aacute;nto tard&oacute; alguien en enterarse y en qu&eacute; estado acab&oacute;. Y '
          u'debajo, la tabla de aver&iacute;as que le hicisteis vosotros.</p>') + u'''
      </ol>
''' + test('c6b', u'Lo que tiene que haber quedado de la unidad entera', PREGUNTAS_TEST_B) + u'''
      <div class="nota">
        <span class="n-tag">Y con esto se cierra la unidad</span>
        Empezaste con un programa de bloques que no se pod&iacute;a ni mandar por el m&oacute;vil y
        acabas con un aparato que mide de verdad, se acuerda de lo que ha visto, decide, avisa a
        alguien, guarda lo que cabe y <b>sabe pararse cuando algo no cuadra</b>. Lo que queda de curso
        le a&ntilde;ade movimiento (<b>unidad 7</b>, rob&oacute;tica), le pasa la factura ambiental
        (<b>unidad 8</b>) y pregunta a qui&eacute;n sirve (<b>unidad 9</b>). Pero el aparato, como
        aparato, ya est&aacute; terminado. Y sabes decir hasta d&oacute;nde llega, que es la parte que
        casi nadie sabe hacer.
      </div>
'''


# ==========================================================================
# El armado de las cuatro sesiones
# ==========================================================================
MIN = [(u"10'", u'Reto'), (u"25'", u'Teor&iacute;a'), (u"20'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')]
MIN8 = [(u"10'", u'Reto'), (u"22'", u'Teor&iacute;a'), (u"20'", u'Pr&aacute;ctica'),
        (u"8'", u'Cierre y test')]


def sesiones(bloque):
    """Devuelve las cuatro sesiones en el formato que espera unidad_base.pagina."""
    s5 = (bloque('00', u'Reto inicial &middot; 10 min', S5_RETO) +
          bloque('01', u'Teor&iacute;a &middot; 25 min', S5_TEORIA) +
          bloque('02', u'Pr&aacute;ctica &middot; 20 min', S5_PRACTICA) +
          bloque('03', u'Cierre &middot; 5 min', S5_CIERRE))
    s6 = (bloque('00', u'Reto inicial &middot; 10 min', S6_RETO) +
          bloque('01', u'Teor&iacute;a &middot; 25 min', S6_TEORIA) +
          bloque('02', u'Pr&aacute;ctica &middot; 20 min', S6_PRACTICA) +
          bloque('03', u'Cierre &middot; 5 min', S6_CIERRE))
    s7 = (bloque('00', u'Reto inicial &middot; 10 min', S7_RETO) +
          bloque('01', u'Teor&iacute;a &middot; 25 min', S7_TEORIA) +
          bloque('02', u'Pr&aacute;ctica &middot; 20 min', S7_PRACTICA) +
          bloque('03', u'Cierre &middot; 5 min', S7_CIERRE))
    s8 = (bloque('00', u'Reto inicial &middot; 10 min', S8_RETO) +
          bloque('01', u'Teor&iacute;a &middot; 22 min', S8_TEORIA) +
          bloque('02', u'Pr&aacute;ctica &middot; 20 min', S8_PRACTICA) +
          bloque('03', u'Cierre y test &middot; 8 min', S8_CIERRE))
    return [
        dict(corto=u'Decidir con memoria',
             titulo=u'La bomba arranc&oacute; a las tres de la ma&ntilde;ana',
             entradilla=u'Tu programa decide con el n&uacute;mero de este instante, y un n&uacute;mero '
                        u'de un instante puede ser mentira. Guardar las &uacute;ltimas cuesta bytes, '
                        u'y los bytes se cuentan.',
             minutado=MIN, chips=[u'CE4 &middot; 4.2', u'CE5 &middot; 5.1', u'C.1', u'C.2'],
             cuerpo=s5),
        dict(corto=u'Montar el aviso de verdad',
             titulo=u'Llevaba seis d&iacute;as callado, y eso parec&iacute;a buena se&ntilde;al',
             entradilla=u'El mensaje de la sesi&oacute;n 3 no ha salido del cuaderno. Hoy sale, con un '
                        u'Uno que no tiene wifi. Y hay que decidir cada cu&aacute;nto hablar, que es '
                        u'm&aacute;s dif&iacute;cil de lo que parece.',
             minutado=MIN, chips=[u'CE4 &middot; 4.2', u'CE5 &middot; 5.1', u'C.3', u'C.4'],
             cuerpo=s6),
        dict(corto=u'Entrenar con vuestros datos',
             titulo=u'Acierta el 93 %. Con los vuestros.',
             entradilla=u'Los mismos ejemplos y el mismo modelo dan 93 % o 73 % seg&uacute;n una cosa '
                        u'que casi nadie mira: c&oacute;mo has partido los datos.',
             minutado=MIN, chips=[u'CE4 &middot; 4.2', u'CE5 &middot; 5.1', u'C.1', u'C.4'],
             cuerpo=s7),
        dict(corto=u'El sistema completo',
             titulo=u'Tres minutos, funcionando, delante de gente',
             entradilla=u'Todo junto: el programa entero como m&aacute;quina de estados, el modo '
                        u'seguro y la ficha de n&uacute;meros con la que se defiende. R&oacute;mpelo '
                        u't&uacute; antes de que lo rompa el jurado.',
             minutado=MIN8,
             chips=[u'CE4 &middot; 4.2', u'CE5 &middot; 5.1', u'C.1', u'C.3', u'C.4'],
             cuerpo=s8),
    ]
