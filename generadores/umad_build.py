# -*- coding: utf-8 -*-
u"""2.o TyD · Tema 4 · La madera.

Tema NUEVO (22-sep-2026): sale de abrir el antiguo tema 3 «Materiales de uso
tecnico» en las tres unidades del libro de Revuela (3 Materiales, 4 Madera,
5 Metales), que es como se da en clase. El contenido sigue el Tema 4 del libro
«Tecnologia y Digitalizacion I · Revuela · Andalucia» (SM), ISBN 978-84-1392-885-2,
y la forma es la del resto del sitio: reto, teoria, practica y cierre.
"""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from unidad_base import pagina, bloque, ficha, pregunta
from test_auto import test

# ---------------------------------------------------------------- sesion 1 ---
S1_C = u'''
      <p>Coge un l&aacute;piz de madera y m&iacute;ralo de canto. Esa pieza <b>estuvo viva</b>: creci&oacute; unos
      mil&iacute;metros al a&ntilde;o, bebi&oacute; agua por dentro y se defendi&oacute; de los insectos. Ning&uacute;n otro material
      del taller puede decir eso.</p>
      <p><b>La pregunta de hoy:</b> si cortas un tronco por la mitad, ver&aacute;s que la madera del centro
      es m&aacute;s oscura que la de fuera. &iquest;Por qu&eacute;? &iquest;Y cu&aacute;l de las dos usar&iacute;as para hacer un mueble
      que tiene que durar?</p>
'''

S1_T = u'''
      <p>La <b>madera</b> es el material que forma el tronco de los &aacute;rboles. Por dentro son
      <b>fibras de celulosa</b> pegadas con <b>lignina</b>: por eso es resistente en el sentido de la
      fibra y se raja en el sentido contrario.</p>

      <div class="escena">
        <div class="escena-barra"><span class="escena-titulo">Las cinco capas del tronco &middot; de fuera adentro</span></div>
        <div class="lienzo">
          <svg viewBox="0 0 640 260" role="img" aria-label="Corte de un tronco con sus cinco capas: corteza, cambium, albura, duramen y medula">
            <g transform="translate(320,130)">
              <circle r="120" fill="#8a6134"/>
              <circle r="112" fill="#c9a06a"/>
              <circle r="104" fill="#f0d9b2"/>
              <circle r="64"  fill="#b9834a"/>
              <circle r="14"  fill="#6f4a25"/>
              <g stroke="#00000022" fill="none">
                <circle r="84"/><circle r="94"/><circle r="74"/>
              </g>
            </g>
            <g font-family="system-ui, sans-serif" font-size="13" fill="#2b3240">
              <g stroke="#2b3240" stroke-width="1"><path d="M320 10v18M470 60l-22 16M470 130h-24M470 200l-30-22M320 250v-18"/></g>
              <text x="320" y="8"   text-anchor="middle" font-weight="600">A &middot; Corteza</text>
              <text x="476" y="60">B &middot; C&aacute;mbium</text>
              <text x="476" y="134">C &middot; Albura</text>
              <text x="476" y="206">D &middot; Duramen</text>
              <text x="320" y="262" text-anchor="middle" font-weight="600">E &middot; M&eacute;dula</text>
            </g>
          </svg>
        </div>
        <div class="pie">Dibujo propio. Los anillos finos que se ven dentro son los <b>anillos de
          crecimiento</b>: uno por a&ntilde;o, y por eso se puede saber la edad del &aacute;rbol cont&aacute;ndolos.</div>
      </div>

      <table class="tabla-ancha">
        <thead><tr><th>Capa</th><th>D&oacute;nde est&aacute;</th><th>Qu&eacute; hace</th></tr></thead>
        <tbody>
          <tr><td><b>Corteza</b></td><td>La capa exterior</td><td>Protege al tronco</td></tr>
          <tr><td><b>C&aacute;mbium</b></td><td>Capa fina, entre la corteza y la madera</td><td>Transporta sustancias y <b>hace crecer</b> al &aacute;rbol</td></tr>
          <tr><td><b>Albura</b></td><td>La madera de fuera</td><td>M&aacute;s clara y blanda: es la m&aacute;s <b>joven</b></td></tr>
          <tr><td><b>Duramen</b></td><td>La madera de dentro</td><td>M&aacute;s oscura y dura: es la m&aacute;s <b>antigua</b></td></tr>
          <tr><td><b>M&eacute;dula</b></td><td>El centro</td><td>La parte central del tronco</td></tr>
        </tbody>
      </table>
      <p>Ah&iacute; est&aacute; la respuesta al reto: lo oscuro del centro es el <b>duramen</b>, y es el que se
      busca para un mueble que tenga que durar.</p>

      <div class="caja caja-nuestro">
        <span class="n-tag">Lo que suele caer en el examen</span>
        <p>Las capas se preguntan <b>en orden y con su funci&oacute;n</b>. Truco para no liarlos:
        <b>albura</b> suena a <i>alba</i>, blanca; <b>duramen</b> lleva dentro <i>duro</i>.</p>
      </div>

      <figure class="foto">
        <img src="../../../img/umad-anillos.jpg" alt="Tocón serrado visto desde arriba, con decenas de anillos concéntricos y grietas que salen del centro" loading="lazy">
        <figcaption>Un <b>tocón</b> visto desde arriba. Cada anillo es <b>un año</b>: la franja clara crece en primavera y la línea oscura, en verano. Las grietas que salen del centro son de <b>secado</b>: la madera encoge al perder agua, y encoge más en el sentido de los anillos que hacia el centro. Es lo mismo que le pasa a un mueble hecho con madera sin secar.
          <span class="credito">Paul VanDerWerf &middot; CC BY 2.0 &middot;
            <a href="https://commons.wikimedia.org/wiki/File:Tree_Rings_-_Flickr_-_Me_in_ME.jpg" target="_blank" rel="noopener">Wikimedia Commons</a></span>
        </figcaption>
      </figure>

      <h3>Y una cosa que no es obvia: la madera quema en verde</h3>
      <p>Al arder, la madera suelta <b>menos CO<sub>2</sub> del que el &aacute;rbol absorbi&oacute;</b> mientras
      crec&iacute;a. Por eso se dice que su <b>balance de carbono es negativo</b> y cuenta como energ&iacute;a
      renovable &mdash; siempre que salga de una <b>explotaci&oacute;n sostenible</b>, es decir, que se
      replante lo que se tala.</p>
'''

S1 = (
  bloque('00', u'Reto inicial &middot; 10 min', S1_C) +
  bloque('01', u'Teor&iacute;a &middot; 25 min', S1_T) +
  bloque('02', u'Pr&aacute;ctica &middot; 20 min', ficha(
    u'La edad del tronco', [u'1.2', u'A.3'], u'Por parejas &middot; 20 min', u'''
          <h4>Qu&eacute; hay que hacer</h4>
          <ol class="pasos">
            <li>Buscad la foto de un <b>corte de tronco</b> (vale un taco de le&ntilde;a de casa).</li>
            <li>Se&ntilde;alad sobre ella las <b>cinco capas</b> con su nombre.</li>
            <li>Contad los anillos y decid <b>cu&aacute;ntos a&ntilde;os</b> ten&iacute;a el &aacute;rbol.</li>
            <li>Mirad el grosor de los anillos: los a&ntilde;os de m&aacute;s lluvia dan anillos m&aacute;s anchos.
                &iquest;Se nota alg&uacute;n a&ntilde;o malo?</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Las cinco capas, bien colocadas <b>(5 puntos)</b>.</li>
            <li>La edad, contada y justificada <b>(3 puntos)</b>.</li>
            <li>La lectura de los anillos anchos y estrechos <b>(2 puntos)</b>.</li>
          </ul>''')) +
  bloque('03', u'Cierre &middot; 5 min', u'''
      <ol class="preguntas">
''' + pregunta(u'&iquest;De qu&eacute; est&aacute; hecha la madera por dentro?',
               u'<p>De <b>fibras de celulosa</b> unidas con <b>lignina</b>.</p>')
    + pregunta(u'&iquest;Cu&aacute;l es m&aacute;s joven, la albura o el duramen?',
               u'<p>La <b>albura</b>: es la de fuera, m&aacute;s clara y m&aacute;s blanda.</p>')
    + pregunta(u'&iquest;Por qu&eacute; se dice que el balance de carbono de la madera es negativo?',
               u'<p>Porque al quemarse suelta <b>menos CO<sub>2</sub> del que el &aacute;rbol absorbi&oacute;</b> al crecer.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya sabes qu&eacute; es la madera. Lo siguiente es c&oacute;mo llega hasta el taller: <b>siete pasos</b>
        del bosque al aserradero, y ninguno se puede saltar.
      </div>
  '''))

# ---------------------------------------------------------------- sesion 2 ---
S2_C = u'''
      <p>Un tabl&oacute;n de pino cuesta unos pocos euros. Entre el &aacute;rbol en pie y ese tabl&oacute;n hay
      <b>siete operaciones</b>, camiones, una sierra enorme y meses de espera.</p>
      <p><b>El reto:</b> poned en orden estas siete palabras sin mirar el libro &mdash;
      <i>secado, apeo, serrado, tronzado, transporte, desramado, descortezado</i> &mdash; y
      justificad por qu&eacute; ese orden y no otro.</p>
'''

S2_T = u'''
      <p>Del bosque al aserradero, en este orden:</p>
      <table class="tabla-ancha">
        <thead><tr><th>#</th><th>Operaci&oacute;n</th><th>En qu&eacute; consiste</th></tr></thead>
        <tbody>
          <tr><td>1</td><td><b>Apeo</b> o tala</td><td>Se corta el tronco cerca de la base y se derriba</td></tr>
          <tr><td>2</td><td><b>Desramado</b></td><td>Se cortan las ramas para dejar el tronco cil&iacute;ndrico</td></tr>
          <tr><td>3</td><td><b>Tronzado</b></td><td>Se corta en trozos para que quepa en el cami&oacute;n</td></tr>
          <tr><td>4</td><td><b>Descortezado</b></td><td>Se quita la corteza y el tronco queda limpio</td></tr>
          <tr><td>5</td><td><b>Transporte</b></td><td>De la zona de tala al aserradero</td></tr>
          <tr><td>6</td><td><b>Serrado</b></td><td>Se corta para obtener las formas comerciales</td></tr>
          <tr><td>7</td><td><b>Secado</b></td><td>Se conservan las piezas hasta que pierden el agua</td></tr>
        </tbody>
      </table>

      <figure class="foto">
        <img src="../../../img/umad-aserradero.jpg" alt="Miles de troncos de pino del mismo largo apilados en el patio de un aserradero, todavía con la corteza" loading="lazy">
        <figcaption>Troncos de pino en el patio de un <b>aserradero</b> de Kemijärvi (Finlandia). Ya están <b>apeados, desramados y tronzados</b>: todos tienen el mismo largo. Y todavía llevan la <b>corteza</b>. En muchos aserraderos grandes el descortezado se hace al llegar, a máquina. Para el examen vale el orden de la tabla.
          <span class="credito">Q0ywo &middot; CC BY-SA 4.0 &middot;
            <a href="https://commons.wikimedia.org/wiki/File:Pine_logs_at_Keitele_Group_sawmill_in_Kemij%C3%A4rvi.jpg" target="_blank" rel="noopener">Wikimedia Commons</a></span>
        </figcaption>
      </figure>
      <div class="caja caja-nuestro">
        <span class="n-tag">Por qu&eacute; el secado va al final y no es un capricho</span>
        <p>La madera reci&eacute;n cortada lleva <b>mucha agua dentro</b>. Si se monta un mueble con ella,
        al secarse encoge &mdash; y lo hace de forma desigual&mdash;: se abren las juntas y la pieza se
        <b>alabea</b>. Por eso el secado es una operaci&oacute;n m&aacute;s, y de las lentas.</p>
      </div>

      <h3>Duras y blandas: no es lo que parece</h3>
      <p>Las maderas de <b>con&iacute;feras</b> (pino, abeto) se llaman <b>blandas</b>: crecen r&aacute;pido, son
      baratas y f&aacute;ciles de trabajar. Las de <b>frondosas</b> (roble, haya, nogal) se llaman
      <b>duras</b>: crecen despacio, cuestan m&aacute;s y aguantan m&aacute;s. La balsa es de frondosa y es la
      madera m&aacute;s blanda que existe, as&iacute; que el nombre es una costumbre del oficio, no una regla.</p>
'''

S2 = (
  bloque('00', u'Reto inicial &middot; 10 min', S2_C) +
  bloque('01', u'Teor&iacute;a &middot; 25 min', S2_T) +
  bloque('02', u'Pr&aacute;ctica &middot; 20 min', ficha(
    u'El viaje de un tabl&oacute;n', [u'1.1', u'A.3', u'A.7'], u'Grupos de tres &middot; 20 min', u'''
          <h4>Qu&eacute; hay que hacer</h4>
          <ol class="pasos">
            <li>Dibujad el <b>diagrama de flujo</b> de las siete operaciones, una caja por paso.</li>
            <li>Al lado de cada caja, escribid <b>qu&eacute; se estropear&iacute;a</b> si ese paso se saltara.</li>
            <li>Buscad qu&eacute; es la <b>colofonia</b> y de qu&eacute; &aacute;rbol sale. Una l&iacute;nea.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Las siete operaciones en orden <b>(5 puntos)</b>.</li>
            <li>La consecuencia de saltarse cada paso <b>(4 puntos)</b>.</li>
            <li>La colofonia <b>(1 punto)</b>.</li>
          </ul>''')) +
  bloque('03', u'Cierre &middot; 5 min', u'''
      <ol class="preguntas">
''' + pregunta(u'&iquest;Qu&eacute; diferencia hay entre tronzar y serrar?',
               u'<p><b>Tronzar</b> es cortar el tronco en trozos para transportarlo; <b>serrar</b> es cortarlo ya en el aserradero para sacar tablas y tablones.</p>')
    + pregunta(u'&iquest;Por qu&eacute; no se puede usar madera reci&eacute;n cortada?',
               u'<p>Porque lleva agua dentro: al secarse <b>encoge y se alabea</b>, y el mueble se abre por las juntas.</p>')
    + pregunta(u'Pino y roble: &iquest;cu&aacute;l es de con&iacute;fera y cu&aacute;l de frondosa?',
               u'<p>El <b>pino</b> es con&iacute;fera (blanda) y el <b>roble</b>, frondosa (dura).</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Con el tabl&oacute;n ya en el taller toca preguntarse qu&eacute; sabe hacer esta madera &mdash;y qu&eacute; hacen
        los <b>tableros</b> que no son madera maciza, que son los que hay en casi todos los muebles.
      </div>
  '''))

# ---------------------------------------------------------------- sesion 3 ---
S3_C = u'''
      <p>Abre el armario de tu habitaci&oacute;n y mira el canto de una balda. Si ves <b>virutas
      prensadas</b>, eso no es madera maciza: es un <b>derivado</b>. Y probablemente el mueble entero
      lo sea.</p>
      <p><b>El reto:</b> &iquest;por qu&eacute; un fabricante de muebles preferir&iacute;a un tablero de virutas antes
      que un tabl&oacute;n de roble? Escribid dos razones antes de seguir.</p>
'''

S3_T = u'''
      <h3>Lo que sabe hacer la madera</h3>
      <ul>
        <li><b>Poco densa</b>: casi todas flotan. De ah&iacute; las barcas.</li>
        <li><b>Aislante</b> del calor y de la electricidad. De ah&iacute; los mangos de herramienta.</li>
        <li><b>Resistente a tracci&oacute;n y a compresi&oacute;n</b>. De ah&iacute; las vigas.</li>
        <li><b>Sonora</b>: transmite el sonido seg&uacute;n su densidad. De ah&iacute; las guitarras &mdash;y el
            corcho como aislante ac&uacute;stico&mdash;.</li>
        <li><b>Biodegradable</b> y no contaminante.</li>
        <li><b>Combustible</b> barato, con el balance de carbono de la sesi&oacute;n&nbsp;1.</li>
      </ul>

      <h3>Por dentro es un manojo de tubos</h3>
<p>El tronco est&aacute; formado por millones de <b>fibras</b> alargadas, paralelas al eje del &aacute;rbol, que
         en vida transportaban agua. Imagina un paquete de pajitas pegadas entre s&iacute;: fuertes a lo largo,
         f&aacute;ciles de separar a lo ancho.</p>

      <div class="escena" id="esc-veta">
        <div class="escena-barra">
          <span class="escena-titulo">Romper una tabla &middot; pulsa para aplicar la fuerza</span>
          <div class="seg" id="seg-veta">
            <button type="button" data-v="larga" aria-pressed="true">A favor de la veta</button>
            <button type="button" data-v="corta">Contra la veta</button>
            <button type="button" data-v="contra">Contrachapado</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 230" id="svg-veta" role="img"
               aria-label="Una tabla se parte con facilidad a favor de la veta y resiste en contra; el contrachapado cruza las capas"></svg>
        </div>
        <div class="pie" id="pie-veta" role="status" aria-live="polite" aria-atomic="true"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-veta');
        var pie = document.getElementById('pie-veta');
        var seg = document.getElementById('seg-veta');
        if(!svg) return;
        var modo = 'larga', roto = false;

        function tabla(){
          var m = '', X = 120, Y = 60, W = 400, H = 90;
          /* cuerpo de la tabla */
          m += '<rect x="' + X + '" y="' + Y + '" width="' + W + '" height="' + H +
               '" rx="3" fill="#d9b382" stroke="#a5783f" stroke-width="2"></rect>';

          if(modo === 'contra'){
            /* tres capas con la veta cruzada */
            for(var c = 0; c < 3; c++){
              var y0 = Y + c*H/3, h = H/3;
              m += '<rect x="' + X + '" y="' + y0 + '" width="' + W + '" height="' + h +
                   '" fill="' + (c===1 ? '#cfa871' : '#d9b382') + '" stroke="#a5783f" stroke-width="1"></rect>';
              if(c === 1){
                for(var k = 0; k < 26; k++){
                  var x = X + 8 + k*15;
                  m += '<path d="M' + x + ' ' + (y0+3) + ' V' + (y0+h-3) + '" stroke="#a5783f" stroke-width="1.3" opacity=".8"></path>';
                }
              } else {
                for(var j = 0; j < 4; j++){
                  var y = y0 + 6 + j*7;
                  m += '<path d="M' + (X+6) + ' ' + y + ' H' + (X+W-6) + '" stroke="#a5783f" stroke-width="1.2" opacity=".8"></path>';
                }
              }
            }
          } else {
            /* veta longitudinal */
            for(var i = 0; i < 9; i++){
              var yy = Y + 9 + i*9.5;
              m += '<path d="M' + (X+6) + ' ' + yy + ' q100 ' + (i%2?4:-4) + ' 200 0 q100 ' + (i%2?-4:4) + ' 194 0" '
                 + 'fill="none" stroke="#a5783f" stroke-width="1.4" opacity=".75"></path>';
            }
          }

          /* la grieta, si se ha roto */
          if(roto && modo === 'larga'){
            m += '<path d="M' + (X+40) + ' ' + (Y+44) + ' l70 -5 l80 8 l90 -6 l80 7 l40 -4" fill="none" '
               + 'stroke="#5b3a16" stroke-width="5" stroke-linecap="round"></path>';
          }

          /* fuerza aplicada */
          var fx = (modo === 'corta') ? X + W/2 : X + W/2;
          if(modo === 'larga' || modo === 'contra'){
            m += '<path d="M' + fx + ' 22 V' + (Y-8) + '" stroke="var(--goo-rojo)" stroke-width="3"></path>';
            m += '<path d="M' + fx + ' ' + Y + ' l-6 -11 h12 Z" fill="var(--goo-rojo)"></path>';
            m += '<path d="M130 ' + (Y+H+16) + ' h30 M480 ' + (Y+H+16) + ' h30" stroke="var(--ink-soft)" stroke-width="4"></path>';
          } else {
            m += '<path d="M' + (X-40) + ' ' + (Y+H/2) + ' H' + (X-8) + '" stroke="var(--goo-rojo)" stroke-width="3"></path>';
            m += '<path d="M' + X + ' ' + (Y+H/2) + ' l-11 -6 v12 Z" fill="var(--goo-rojo)"></path>';
            m += '<path d="M' + (X+W+40) + ' ' + (Y+H/2) + ' H' + (X+W+8) + '" stroke="var(--goo-rojo)" stroke-width="3"></path>';
            m += '<path d="M' + (X+W) + ' ' + (Y+H/2) + ' l11 -6 v12 Z" fill="var(--goo-rojo)"></path>';
          }
          m += '<text x="320" y="186" text-anchor="middle" class="rotulo-svg" style="font-size:10.5px">'
             + (modo==='contra' ? 'TRES CAPAS CON LA VETA CRUZADA' : 'LA VETA VA DE IZQUIERDA A DERECHA') + '</text>';
          return m;
        }

        var TXT = {
          larga: ['Golpea <b>perpendicular a la veta</b>: la fuerza intenta separar las fibras unas de otras. '
                + 'Pulsa el bot&oacute;n otra vez para aplicar la fuerza.',
                  '<b>Se parte, y limpiamente.</b> Las fibras no est&aacute;n pegadas entre s&iacute; con mucha fuerza: '
                + 'basta con separarlas. Por eso la le&ntilde;a se raja de un hachazo y siempre a lo largo.'],
          corta: ['<b>Aqu&iacute; la madera aguanta muchisimo.</b> Ahora la fuerza tira <b>en la direcci&oacute;n de las '
                + 'fibras</b>, y cada fibra es como una cuerda. Romperla exige romper todas las cuerdas a la vez.',
                  ''],
          contra: ['El <b>contrachapado</b> se fabrica pegando capas finas con la veta girada 90 grados en cada una. '
                 + 'Pulsa otra vez para aplicar la misma fuerza que rompi&oacute; la tabla.',
                   '<b>No se parte.</b> Para rajarlo habr&iacute;a que separar las fibras de una capa <b>y</b> romper '
                 + 'las de la siguiente, que est&aacute;n cruzadas. Un invento que no mejora la madera: '
                 + '<b>anula su punto d&eacute;bil</b>.']
        };

        function pinta(){
          svg.innerHTML = tabla();
          var t = TXT[modo];
          pie.innerHTML = (roto && t[1]) ? t[1] : t[0];
        }
        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-v]'); if(!b) return;
          if(b.dataset.v === modo){ roto = !roto; }
          else { modo = b.dataset.v; roto = false; }
          seg.querySelectorAll('button').forEach(function(x){ x.setAttribute('aria-pressed', x===b?'true':'false'); });
          pinta();
        });
        pinta();
      })();
      </script>

      <div class="copiar">
        <h4>La madera, por dentro</h4>
        <p><b>Fibra o veta</b>: direcci&oacute;n en la que est&aacute;n orientadas las c&eacute;lulas alargadas del tronco.</p>
        <p><b>La madera es anis&oacute;tropa</b>: sus propiedades cambian seg&uacute;n la direcci&oacute;n. Resiste mucho
           <b>a lo largo</b> de la veta y poco <b>a lo ancho</b>.</p>
        <p>Los <b>anillos de crecimiento</b> marcan un a&ntilde;o cada uno: claro el de primavera, oscuro el de
           verano. Se pueden contar.</p>
      </div>

      <h3>Blandas y duras</h3>
      <div class="copiar">
        <h4>Los dos grandes grupos</h4>
        <ul>
          <li><b>Maderas blandas</b>: de &aacute;rboles de hoja perenne, que crecen r&aacute;pido &mdash;pino, abeto,
              chopo&mdash;. Baratas, ligeras, f&aacute;ciles de trabajar. Es lo que hay en el taller del instituto.</li>
          <li><b>Maderas duras</b>: de hoja caduca, de crecimiento lento &mdash;roble, haya, nogal&mdash;.
              Caras, pesadas, resistentes y bonitas. Muebles y suelos.</li>
        </ul>
        <p>Cuidado con los nombres: <b>la balsa es una madera dura</b> aunque se corte con la u&ntilde;a. La
           clasificaci&oacute;n es bot&aacute;nica, no de dureza real.</p>
      <figure class="foto">
        <img src="../../../img/u3-madera.jpg" width="1200" height="675" loading="lazy"
             alt="Tabla de pino cepillada con tres nudos redondos y la veta desvi&aacute;ndose alrededor de cada uno">
        <figcaption>Esto es <b>pino</b>, la madera blanda del taller del instituto. Tres <b>nudos</b> y la veta desvi&aacute;ndose para rodearlos: un nudo es donde estaba una <b>rama</b>, y la fibra del tronco tuvo que abrirse para dejarla salir. De ah&iacute; salen las dos cosas que m&aacute;s te van a pasar cortando: la madera se raja <b>a lo largo de la fibra</b> y nunca a lo ancho, y una tabla con un nudo en medio es m&aacute;s d&eacute;bil justo ah&iacute;.
          <br><br>Foto de <b>Eleonora Vokueva</b> en Pexels. Es de su autor y no forma parte del material
          publicado bajo la licencia de esta p&aacute;gina.</figcaption>
      </figure>

      </div>

      <h3>Los derivados: arreglar lo que la madera hace mal</h3>
      <p>Cada derivado se invent&oacute; para resolver <b>un defecto concreto</b> de la madera maciza. No son
         sucedáneos baratos: son soluciones t&eacute;cnicas.</p>
      <div class="copiar">
        <h4>Tableros derivados</h4>
        <ul>
          <li><b>Contrachapado</b>: capas finas encoladas con la veta cruzada 90&deg;.
              <i>Resuelve</i>: la anisotrop&iacute;a y el alabeo.</li>
          <li><b>Aglomerado</b>: virutas prensadas con cola.
              <i>Resuelve</i>: aprovechar restos y hacer tableros grandes y baratos.</li>
          <li><b>DM o MDF</b>: fibras muy finas prensadas.
              <i>Resuelve</i>: dar una superficie lisa y uniforme, perfecta para pintar o chapar.</li>
          <li><b>Chapa</b>: l&aacute;mina fin&iacute;sima de madera noble pegada sobre un tablero barato.
              <i>Resuelve</i>: el aspecto del roble al precio del aglomerado.</li>
        </ul>
      </div>
      <div class="nota">
        <span class="n-tag">Lo que hay que llevarse</span>
        El contrachapado no es «madera peor». Es madera a la que se le ha <b>quitado el punto d&eacute;bil</b>
        cruzando las capas. Es exactamente lo que hace un ingeniero: no busca el material perfecto,
        corrige el defecto del que tiene.
      </div>

      <h3>Los derivados: cuando conviene deshacer la madera para rehacerla</h3>
      <table class="tabla-ancha">
        <thead><tr><th>Tablero</th><th>C&oacute;mo se hace</th><th>C&oacute;mo es</th><th>D&oacute;nde se usa</th></tr></thead>
        <tbody>
          <tr><td><b>Aglomerado</b></td><td>Astillas de madera con cola, prensadas</td>
              <td>Rugoso, poroso, pesado. No admite acabados</td><td>Muebles econ&oacute;micos, forrados de melamina</td></tr>
          <tr><td><b>Contrachapado</b></td><td>L&aacute;minas encoladas y prensadas, cada una girada</td>
              <td>Liso, estable, ligero y resistente</td><td>Uso estructural, muebles, barcos, embalajes</td></tr>
          <tr><td><b>DM (MDF/HDF)</b></td><td>Fibras de madera con resinas, prensadas</td>
              <td>Liso y uniforme. S&iacute; admite acabados. Ligero</td><td>Suelos laminados, molduras, puertas</td></tr>
        </tbody>
      </table>

      <figure class="foto">
        <img src="../../../img/umad-aglomerado.jpg" alt="Trozo de tablero aglomerado visto de canto: astillas de madera de varios tamaños prensadas" loading="lazy">
        <figcaption><b>Aglomerado</b> visto de canto. Se ven las <b>astillas</b> una a una, más finas en las caras y más gordas en el centro. Por eso el canto es rugoso y no se puede pintar: en los muebles va siempre forrado de melamina.
          <span class="credito">D-Kuru &middot; CC BY-SA 3.0 AT &middot;
            <a href="https://commons.wikimedia.org/wiki/File:Particle_board_close_up-horizontal-f22_PNr%C2%B00101.jpg" target="_blank" rel="noopener">Wikimedia Commons</a></span>
        </figcaption>
      </figure>

      <figure class="foto">
        <img src="../../../img/umad-dm.jpg" alt="Tres listones de tablero DM apilados, con los cantos lisos y del mismo color que las caras" loading="lazy">
        <figcaption><b>DM</b> (o MDF): las fibras son tan finas que no se ven. El canto sale tan liso como la cara, y por eso admite pintura y se puede moldurar.
          <span class="credito">Vaderluck &middot; CC BY-SA 3.0 &middot;
            <a href="https://commons.wikimedia.org/wiki/File:MDF_Sample.jpg" target="_blank" rel="noopener">Wikimedia Commons</a></span>
        </figcaption>
      </figure>
      <div class="caja caja-nuestro">
        <span class="n-tag">La respuesta al reto</span>
        <p>Dos razones: <b>cuestan menos</b> y, sobre todo, vienen en <b>tableros grandes y
        uniformes</b> que no tienen nudos ni se alabean. Una tabla maciza de dos metros es cara,
        rara y se mueve con la humedad; un tablero de DM sale siempre igual.</p>
      </div>
'''

S3 = (
  bloque('00', u'Reto inicial &middot; 10 min', S3_C) +
  bloque('01', u'Teor&iacute;a &middot; 25 min', S3_T) +
  bloque('02', u'Pr&aacute;ctica &middot; 20 min', ficha(
    u'&iquest;Flota o se hunde?', [u'1.2', u'7.1', u'A.3'], u'Grupos de tres &middot; 20 min', u'''
          <h4>Qu&eacute; hay que hacer</h4>
          <p>Material: una cubeta con agua y muestras de <b>pino, abeto, roble</b> y, si la hay,
          alguna madera pesada.</p>
          <ol class="pasos">
            <li>Antes de echarlas al agua, <b>apostad</b>: &iquest;cu&aacute;l se hunde m&aacute;s?</li>
            <li>Echadlas y anotad cu&aacute;nto asoma cada una.</li>
            <li>Buscad la <b>densidad</b> de esas tres maderas en internet y ordenadlas.</li>
            <li>La densidad del agua es 1&nbsp;g/cm&sup3;. &iquest;Hay alguna madera que <b>no flote</b>?
                Buscad una.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>La predicci&oacute;n, hecha ANTES y por escrito <b>(2 puntos)</b>.</li>
            <li>Las densidades, con su fuente <b>(4 puntos)</b>.</li>
            <li>Explicar por qu&eacute; flota lo que flota <b>(4 puntos)</b>.</li>
          </ul>''')) +
  bloque('03', u'Cierre &middot; 5 min', u'''
      <ol class="preguntas">
''' + pregunta(u'&iquest;Qu&eacute; diferencia hay entre aglomerado y contrachapado?',
               u'<p>El <b>aglomerado</b> son astillas prensadas con cola; el <b>contrachapado</b>, l&aacute;minas enteras encoladas. El segundo es m&aacute;s resistente y estable.</p>')
    + pregunta(u'&iquest;Qu&eacute; tablero usar&iacute;as para un suelo laminado, y por qu&eacute;?',
               u'<p><b>DM</b> (MDF/HDF): es liso, uniforme y admite acabados, que es lo que hace falta para imitar una superficie.</p>')
    + pregunta(u'&iquest;Por qu&eacute; casi todas las maderas flotan?',
               u'<p>Porque su <b>densidad es menor que la del agua</b> (1&nbsp;g/cm&sup3;).</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya sabes qu&eacute; madera pedir. Ahora, el taller: <b>medir, sujetar, cortar, perforar, lijar,
        unir y dar acabado</b> &mdash; y las gafas puestas.
      </div>
  '''))

# ---------------------------------------------------------------- sesion 4 ---
S4_C = u'''
      <p>En el taller, el 90&nbsp;% de las piezas que salen torcidas no se estropearon al cortar:
      se estropearon <b>al marcar</b> o porque la pieza <b>no estaba sujeta</b>.</p>
      <p><b>El reto:</b> mirad esta lista &mdash;serrucho, sargento, escuadra, lija, barrena&mdash; y
      ordenadla seg&uacute;n cu&aacute;ndo se usa cada una. Luego comprobad si acertasteis.</p>
'''

S4_T = u'''
      <p>Trabajar la madera son siempre las mismas <b>siete operaciones</b>, en este orden:
      <b>medir y marcar &rarr; sujetar &rarr; cortar &rarr; perforar &rarr; limar y lijar &rarr; unir &rarr;
      acabado</b>.</p>

      <table class="tabla-ancha">
        <thead><tr><th>Operaci&oacute;n</th><th>Herramientas</th><th>Seguridad</th></tr></thead>
        <tbody>
          <tr><td><b>Medir y marcar</b></td>
              <td>Escuadra fija y m&oacute;vil, regla met&aacute;lica, l&aacute;piz de carpintero, comp&aacute;s</td>
              <td>Nada especial: orden en la mesa</td></tr>
          <tr><td><b>Sujetar</b></td>
              <td>Tornillo de banco, gato o sargento, pinzas</td>
              <td>Sin colgantes, pulseras ni anillos; pelo recogido; ojo a los atrapamientos</td></tr>
          <tr><td><b>Cortar</b></td>
              <td>Serrucho (a 45&deg;), sierra de costilla, segueta o sierra de marqueter&iacute;a, c&uacute;ter con gu&iacute;a</td>
              <td><b>Guantes</b>. No se corta nunca una pieza suelta</td></tr>
          <tr><td><b>Perforar</b></td>
              <td>Barrena, berbiqu&iacute;, taladro de columna, brocas de madera</td>
              <td><b>Guantes y gafas</b>: saltan virutas</td></tr>
          <tr><td><b>Limar y lijar</b></td>
              <td>Escofina (diente grueso), lima (diente fino), papel de lija</td>
              <td>Guantes: abrasiones</td></tr>
          <tr><td><b>Unir</b></td>
              <td>Cola, clavos, tornillos, espigas</td><td>Cuidado con el martillo y los dedos</td></tr>
          <tr><td><b>Acabado</b></td>
              <td>Barniz, pintura, cera</td><td>Ventilaci&oacute;n: los disolventes se respiran</td></tr>
        </tbody>
      </table>

      <div class="caja caja-oficial">
        <span class="n-tag">Tres reglas del taller que no se negocian</span>
        <ol>
          <li><b>La pieza va sujeta antes de tocarla con un filo.</b></li>
          <li><b>Guantes para cortar; guantes y gafas para taladrar.</b></li>
          <li><b>Si te distraen, paras.</b> El serrucho no espera.</li>
        </ol>
      </div>

      <h3>Escofina o lima: el detalle que se pregunta</h3>
      <p>Las dos quitan material. La <b>escofina</b> tiene los dientes <b>gruesos</b> y se usa para
      el ajuste basto; la <b>lima</b> los tiene <b>finos</b> y se usa para alisar. Primero la
      escofina, despu&eacute;s la lima, y al final el papel de lija.</p>
'''

S4 = (
  bloque('00', u'Reto inicial &middot; 10 min', S4_C) +
  bloque('01', u'Teor&iacute;a &middot; 25 min', S4_T) +
  bloque('02', u'Pr&aacute;ctica &middot; 20 min', ficha(
    u'El marco de 12 por 9', [u'2.2', u'3.1', u'A.7'], u'Por parejas &middot; 20 min', u'''
          <h4>Qu&eacute; hay que hacer</h4>
          <p>Material: listones de pino, cola, lija, escuadra y sargento.</p>
          <ol class="pasos">
            <li><b>Marcad</b> con escuadra y l&aacute;piz cuatro listones para un marco de 12&times;9&nbsp;cm.</li>
            <li><b>Sujetad</b> cada pieza con el sargento antes de serrar. Comprobadlo entre los dos.</li>
            <li><b>Serrad</b> con el serrucho inclinado y con guantes.</li>
            <li><b>Lijad</b> los cuatro cantos y <b>encolad</b> en escuadra.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Las cuatro piezas miden lo que ten&iacute;an que medir, &plusmn;2&nbsp;mm <b>(4 puntos)</b>.</li>
            <li>El marco cierra en escuadra <b>(3 puntos)</b>.</li>
            <li><b>Seguridad</b>: nunca se sierra sin sujetar ni sin guantes <b>(3 puntos)</b>.</li>
          </ul>''')) +
  bloque('03', u'Cierre &middot; 5 min', u'''
      <ol class="preguntas">
''' + pregunta(u'&iquest;Cu&aacute;l es la diferencia entre escofina y lima?',
               u'<p>La <b>escofina</b> tiene dientes gruesos (desbaste) y la <b>lima</b>, finos (alisado).</p>')
    + pregunta(u'&iquest;Qu&eacute; hay que ponerse para taladrar, y por qu&eacute;?',
               u'<p><b>Guantes y gafas</b>: al perforar saltan virutas y hay riesgo de atrapamiento.</p>')
    + pregunta(u'&iquest;Para qu&eacute; sirve el sargento?',
               u'<p>Para <b>sujetar</b> la pieza a la mesa o mantener dos piezas unidas mientras se encolan.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        &Uacute;ltima del tema: fabricar <b>papel reciclado</b> &mdash;que tambi&eacute;n sale de la madera&mdash; y
        cerrar con el test.
      </div>
  '''))

# ---------------------------------------------------------------- sesion 5 ---
S5_C = u'''
      <p>Un mueble casi nunca se rompe por el medio de una tabla. Se rompe <b>por donde estaba
      unido</b>: se descuelga una balda, se afloja una pata, se abre una esquina.</p>
      <p><b>El reto:</b> mirad una silla del aula. &iquest;Cu&aacute;ntas uniones distintas encontr&aacute;is?
      &iquest;Cu&aacute;les se podr&iacute;an <b>desmontar</b> con un destornillador y cu&aacute;les no?</p>
'''

S5_T = u'''
      <p>Las uniones se parten en dos familias, y la diferencia es una sola pregunta:
      <b>&iquest;se puede deshacer sin romper la pieza?</b></p>

      <table class="tabla-ancha">
        <thead><tr><th>Tipo</th><th>Con qu&eacute;</th><th>Cu&aacute;ndo se usa</th></tr></thead>
        <tbody>
          <tr><td rowspan="2"><b>Desmontables</b></td><td>Tornillos para madera</td>
              <td>Lo normal en un mueble: aguanta y se puede abrir</td></tr>
          <tr><td>Herrajes, bisagras, escuadras met&aacute;licas</td>
              <td>Puertas, esquinas que sufren</td></tr>
          <tr><td rowspan="3"><b>Fijas</b></td><td>Cola blanca (acetato de polivinilo)</td>
              <td>La uni&oacute;n m&aacute;s com&uacute;n del taller. Necesita <b>presi&oacute;n y tiempo</b></td></tr>
          <tr><td>Clavos y puntas</td><td>R&aacute;pido y barato; aguanta mal si se tira del clavo</td></tr>
          <tr><td>Espigas encoladas, caja y esp&iacute;ga</td><td>Muebles de calidad: la madera se traba consigo misma</td></tr>
        </tbody>
      </table>

      <div class="caja caja-oficial">
        <span class="n-tag">La regla de la cola</span>
        <p>Una uni&oacute;n encolada aguanta <b>m&aacute;s que la propia madera</b> si se hace bien, y eso
        significa tres cosas: superficies <b>limpias y lijadas</b>, cola en <b>las dos caras</b> y
        <b>sargento puesto</b> hasta que fragua. Sin presi&oacute;n no hay uni&oacute;n; hay dos tablas pegadas.</p>
      </div>

      <h3>El acabado no es para que quede bonito</h3>
      <p>Es para que <b>dure</b>. La madera al aire absorbe humedad, se mancha, la atacan los
      insectos y el sol la agrisa. El acabado la sella.</p>
      <ul>
        <li><b>Lijado fino</b>: siempre <b>en el sentido de la fibra</b>. Al rev&eacute;s se raya y se ve
            para siempre debajo del barniz.</li>
        <li><b>Tapaporos</b>: cierra el poro para que el barniz no se lo trague.</li>
        <li><b>Barniz</b>: transparente, deja ver la veta y protege.</li>
        <li><b>Pintura</b>: tapa la veta; sirve para madera fea o para tableros.</li>
        <li><b>Cera o aceite</b>: acabado mate, se repara pasando otra mano.</li>
      </ul>
      <p>Y una cosa de seguridad: barnices y disolventes <b>se respiran</b>. Ventana abierta.</p>
'''

S5 = (
  bloque('00', u'Reto inicial &middot; 10 min', S5_C) +
  bloque('01', u'Teor&iacute;a &middot; 25 min', S5_T) +
  bloque('02', u'Pr&aacute;ctica &middot; 20 min', ficha(
    u'Tres uniones, y cu&aacute;l aguanta', [u'2.2', u'3.1', u'A.7'], u'Grupos de tres &middot; 20 min', u'''
          <h4>Qu&eacute; hay que hacer</h4>
          <p>Material: seis listones cortos, cola blanca, clavos, tornillos, sargento y un cubo
          con peso (libros valen).</p>
          <ol class="pasos">
            <li>Montad tres uniones en L iguales: una <b>encolada</b>, una <b>clavada</b> y una
                <b>atornillada</b>.</li>
            <li><b>Antes de probar</b>, escribid cu&aacute;l creeis que aguantar&aacute; m&aacute;s y por qu&eacute;.</li>
            <li>Colgad peso poco a poco de cada una y anotad <b>con cu&aacute;nto falla</b>.</li>
            <li>Mirad <b>por d&oacute;nde</b> ha roto cada una: &iquest;por la cola, por la madera o por el clavo?</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>La predicci&oacute;n, hecha antes y por escrito <b>(2 puntos)</b>.</li>
            <li>Las tres uniones, bien ejecutadas &mdash;la encolada, con sargento&mdash; <b>(4 puntos)</b>.</li>
            <li>Explicar <b>por d&oacute;nde</b> rompi&oacute; cada una y qu&eacute; dice eso <b>(4 puntos)</b>.</li>
          </ul>''')) +
  bloque('03', u'Cierre &middot; 5 min', u'''
      <ol class="preguntas">
''' + pregunta(u'&iquest;Qu&eacute; diferencia hay entre una uni&oacute;n desmontable y una fija?',
               u'<p>La desmontable se puede deshacer sin romper la pieza (tornillos, herrajes); la fija, no (cola, clavos, espigas).</p>')
    + pregunta(u'&iquest;Por qu&eacute; una uni&oacute;n encolada necesita sargento?',
               u'<p>Porque la cola solo agarra con <b>presi&oacute;n</b> mientras fragua. Sin apretar, quedan dos tablas pegadas de mentira.</p>')
    + pregunta(u'&iquest;En qu&eacute; sentido se lija antes de barnizar, y por qu&eacute;?',
               u'<p><b>En el sentido de la fibra</b>. Al rev&eacute;s quedan rayas que el barniz deja a la vista para siempre.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        &Uacute;ltima del tema: fabricar <b>papel reciclado</b> &mdash;que tambi&eacute;n sale de la madera&mdash; y
        cerrar con el test.
      </div>
  '''))

# ---------------------------------------------------------------- sesion 6 ---
PREGUNTAS = [
 dict(p=u'&iquest;Cu&aacute;l es la capa m&aacute;s interna de la madera del tronco?',
      op=[u'La albura', u'El duramen', u'El c&aacute;mbium'], ok=1,
      por=u'El duramen es la madera vieja del centro: m&aacute;s oscura y m&aacute;s dura. La albura es la de fuera.'),
 dict(p=u'La madera est&aacute; formada por&hellip;',
      op=[u'fibras de celulosa unidas con lignina', u'resinas y c&aacute;mbium', u'celulosa y silicio'], ok=0,
      por=u'Celulosa (las fibras) y lignina (el pegamento). Es lo que le da resistencia en el sentido de la fibra.'),
 dict(p=u'Ordena: apeo, tronzado, desramado.',
      op=[u'apeo &rarr; desramado &rarr; tronzado', u'desramado &rarr; apeo &rarr; tronzado', u'apeo &rarr; tronzado &rarr; desramado'], ok=0,
      por=u'Primero se derriba (apeo), luego se le quitan las ramas (desramado) y despu&eacute;s se corta en trozos (tronzado).'),
 dict(p=u'&iquest;Por qu&eacute; se seca la madera antes de usarla?',
      op=[u'Para que pese menos en el transporte', u'Porque al secarse encoge y se alabea', u'Para que no arda'], ok=1,
      por=u'Si se monta con agua dentro, al secarse encoge de forma desigual y el mueble se abre.'),
 dict(p=u'Un tablero hecho de astillas prensadas con cola es&hellip;',
      op=[u'contrachapado', u'aglomerado', u'DM'], ok=1,
      por=u'El aglomerado. El contrachapado son l&aacute;minas y el DM, fibras con resina.'),
 dict(p=u'&iquest;Qu&eacute; madera es de con&iacute;fera?',
      op=[u'El roble', u'El nogal', u'El pino'], ok=2,
      por=u'El pino y el abeto son con&iacute;feras (blandas); roble, haya y nogal son frondosas (duras).'),
 dict(p=u'Antes de serrar, lo primero es&hellip;',
      op=[u'sujetar la pieza', u'lijar el canto', u'marcar con el comp&aacute;s'], ok=0,
      por=u'Nunca se corta una pieza suelta: primero el tornillo de banco o el sargento.'),
 dict(p=u'El balance de carbono de la madera es negativo porque&hellip;',
      op=[u'no produce CO&sub2; al arder', u'suelta menos CO&sub2; del que absorbi&oacute; al crecer', u'absorbe CO&sub2; mientras arde'], ok=1,
      por=u'S&iacute; produce CO&sub2; al arder, pero menos del que el &aacute;rbol captur&oacute;. Por eso cuenta como renovable, si la explotaci&oacute;n es sostenible.'),
]

S6_T = u'''
      <p>El papel tambi&eacute;n sale de la madera: es celulosa deshecha y vuelta a secar en l&aacute;minas.
      Hacerlo con papel usado es la forma m&aacute;s r&aacute;pida de ver por dentro de qu&eacute; est&aacute; hecha
      una hoja.</p>
'''

S6 = (
  bloque('00', u'Taller &middot; 25 min', S6_T + ficha(
    u'Fabrica tu propio papel', [u'2.2', u'7.1', u'E.1'], u'Grupos de tres &middot; 25 min', u'''
          <h4>Material</h4>
          <p>Papel usado, agua, una cubeta, un marco con tela de mosquitera y, si hay, una batidora.</p>
          <h4>Qu&eacute; hay que hacer</h4>
          <ol class="pasos">
            <li>Romped el papel en trozos peque&ntilde;os y dejadlo <b>en remojo</b> media hora.</li>
            <li>Batidlo hasta que quede una <b>pasta</b>. Eso son las fibras de celulosa sueltas.</li>
            <li>Echad la pasta en la cubeta con agua y <b>pescadla con el marco</b>, en horizontal.</li>
            <li>Dejad escurrir, prensad con un trapo y poned a <b>secar</b> 24 horas.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>La hoja sale entera y se puede escribir en ella <b>(4 puntos)</b>.</li>
            <li>Explicar d&oacute;nde est&aacute;n <b>las fibras</b> y por qu&eacute; se pegan al secar <b>(4 puntos)</b>.</li>
            <li>Orden y limpieza del puesto <b>(2 puntos)</b>.</li>
          </ul>''')) +
  bloque('01', u'Test &middot; 20 min',
         test('umad', u'Lo que tiene que haber quedado del tema', PREGUNTAS)) +
  bloque('02', u'Cierre &middot; 15 min', u'''
      <h3>Todo el tema, en una tabla</h3>
      <table class="tabla-ancha">
        <thead><tr><th>Pregunta</th><th>Respuesta corta</th></tr></thead>
        <tbody>
          <tr><td>&iquest;Qu&eacute; es la madera?</td><td>Fibras de celulosa unidas con lignina</td></tr>
          <tr><td>&iquest;Qu&eacute; capas tiene el tronco?</td><td>Corteza, c&aacute;mbium, albura, duramen y m&eacute;dula</td></tr>
          <tr><td>&iquest;C&oacute;mo se obtiene?</td><td>Apeo, desramado, tronzado, descortezado, transporte, serrado y secado</td></tr>
          <tr><td>&iquest;Qu&eacute; derivados hay?</td><td>Aglomerado, contrachapado y DM</td></tr>
          <tr><td>&iquest;C&oacute;mo se trabaja?</td><td>Medir, sujetar, cortar, perforar, lijar, unir y dar acabado</td></tr>
          <tr><td>&iquest;Por qu&eacute; es sostenible?</td><td>Balance de carbono negativo y biodegradable, si la explotaci&oacute;n es sostenible</td></tr>
        </tbody>
      </table>
      <div class="nota">
        <span class="n-tag">Siguiente tema</span>
        Del material que crece al material que se funde: <b>los metales</b>, que no se cortan con
        serrucho ni se pegan con cola.
      </div>
  '''))

# ------------------------------------------------------------------ pagina ---
S = [
 dict(corto=u'Qu&eacute; es la madera', titulo=u'Lo que hay dentro de un tronco',
      entradilla=u'Toda pieza de madera estuvo viva, y eso explica casi todo lo que hace despu&eacute;s.',
      minutado=[(u"10'", u'Reto'), (u"25'", u'Teor&iacute;a'), (u"20'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')],
      chips=[u'CE1 &middot; 1.2', u'A.3', u'A.7'], cuerpo=S1),
 dict(corto=u'Del bosque al taller', titulo=u'Siete operaciones y ninguna se salta',
      entradilla=u'Entre el &aacute;rbol en pie y el tabl&oacute;n hay siete pasos. El &uacute;ltimo, el secado, es el que m&aacute;s se olvida y el que m&aacute;s estropea.',
      minutado=[(u"10'", u'Reto'), (u"25'", u'Teor&iacute;a'), (u"20'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')],
      chips=[u'CE1 &middot; 1.1', u'CE1 &middot; 1.2', u'A.3'], cuerpo=S2),
 dict(corto=u'Propiedades y tableros', titulo=u'Por qu&eacute; tu armario no es de madera maciza',
      entradilla=u'La madera flota, a&iacute;sla y suena. Y aun as&iacute;, casi todos los muebles llevan tablero: hay una raz&oacute;n.',
      minutado=[(u"10'", u'Reto'), (u"25'", u'Teor&iacute;a'), (u"20'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')],
      chips=[u'CE1 &middot; 1.2', u'CE7 &middot; 7.1', u'A.3', u'A.7'], cuerpo=S3),
 dict(corto=u'Trabajarla', titulo=u'Medir, sujetar, cortar &mdash; y en ese orden',
      entradilla=u'Casi ninguna pieza sale torcida por serrar mal: sale torcida por marcar mal o por no sujetar.',
      minutado=[(u"10'", u'Reto'), (u"25'", u'Teor&iacute;a'), (u"20'", u'Taller'), (u"5'", u'Cierre')],
      chips=[u'CE2 &middot; 2.2', u'CE3 &middot; 3.1', u'A.7'], cuerpo=S4),
 dict(corto=u'Unir y acabar', titulo=u'Por d&oacute;nde se rompe de verdad un mueble',
      entradilla=u'Casi nada se parte por el medio de una tabla: se suelta por donde estaba unido. Y el acabado no es para que quede bonito.',
      minutado=[(u"10'", u'Reto'), (u"25'", u'Teor&iacute;a'), (u"20'", u'Taller'), (u"5'", u'Cierre')],
      chips=[u'CE2 &middot; 2.2', u'CE3 &middot; 3.1', u'A.7'], cuerpo=S5),
 dict(corto=u'Taller y test', titulo=u'Fabricar papel y cerrar el tema',
      entradilla=u'El papel es madera deshecha. Hacerlo a mano ense&ntilde;a de una vez qu&eacute; son las fibras.',
      minutado=[(u"25'", u'Taller'), (u"20'", u'Test'), (u"15'", u'Cierre')],
      chips=[u'CE2 &middot; 2.2', u'CE7 &middot; 7.1', u'E.1'], cuerpo=S6),
]

CFG = dict(
 ruta='2eso/TyD/tema4/',
 migas=u'<a href="../../../">Materiales</a> &middot; <a href="../../">2.&ordm; ESO</a> &middot; <a href="../">TyD</a> &middot; Tema 4',
 h1=u'Madera',
 titulo=u'Tema 4 &middot; Madera',
 tema=u'Tema 4', curso=u'2.&ordm; de ESO', materia=u'Tecnolog&iacute;a y Digitalizaci&oacute;n',
 desc=u'Tema 4 de Tecnolog&iacute;a y Digitalizaci&oacute;n de 2.&ordm; de ESO: las capas del tronco, la obtenci&oacute;n de la madera, sus propiedades, los tableros derivados y c&oacute;mo se trabaja en el taller.',
 sesiones=S)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(os.path.join(BASE, '2eso/TyD/tema4'), exist_ok=True)
html = pagina(CFG)
io.open(os.path.join(BASE, '2eso/TyD/tema4/index.html'), 'w', encoding='utf-8', newline='').write(html)
print('Tema 4 (Madera) generado: %d bytes, %d sesiones' % (len(html), len(S)))
