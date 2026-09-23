# -*- coding: utf-8 -*-
"""2.o TyD · U3 · Materiales: por que las cosas estan hechas de lo que estan hechas."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unidad_base import pagina, bloque, ficha, pregunta

ESCENA = u'''
      <div class="escena" id="esc-bici">
        <div class="escena-barra">
          <span class="escena-titulo">El mismo cuadro de bicicleta, tres materiales</span>
          <div class="seg" id="seg-bici">
            <button type="button" data-b="acero" aria-pressed="true">Acero</button>
            <button type="button" data-b="alu">Aluminio</button>
            <button type="button" data-b="carbono">Fibra de carbono</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 260" id="svg-bici" role="img"
               aria-label="Comparaci&oacute;n de un cuadro de bicicleta en acero, aluminio y fibra de carbono"></svg>
        </div>
        <div class="pie" id="pie-bici"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-bici');
        var pie = document.getElementById('pie-bici');
        var seg = document.getElementById('seg-bici');
        if(!svg) return;

        var M = {
          acero: {nom:'Acero', col:'#7a8590', peso:2.2, precio:120, vida:5, repara:5, co2:2.5,
            txt:'Pesa el doble que el carbono, pero <b>se puede soldar en cualquier taller</b> y aguanta '
              + 'd&eacute;cadas. Si se dobla, avisa antes de romper. Es el material de las bicis que duran toda la vida.'},
          alu:  {nom:'Aluminio', col:'#b9c2cc', peso:1.4, precio:250, vida:3, repara:2, co2:4,
            txt:'El equilibrio de casi todas las bicis de tienda: ligero, no se oxida y sale a un precio '
              + 'razonable. A cambio <b>se fatiga</b>: tras muchos a&ntilde;os de uso puede fallar sin aviso, y '
              + 'soldarlo bien es dif&iacute;cil.'},
          carbono:{nom:'Fibra de carbono', col:'#2f3a45', peso:0.9, precio:900, vida:2, repara:1, co2:7,
            txt:'La mitad de peso que el acero y muy r&iacute;gido: por eso lo usan los profesionales. Pero '
              + '<b>no avisa</b> &mdash;rompe de golpe&mdash;, un golpe tonto lo inutiliza y reciclarlo hoy '
              + 'es pr&aacute;cticamente imposible.'}
        };
        var sel = 'acero';

        function barra(x, y, w, etq, val, max, col, uni){
          var L = 165, p = Math.min(1, val/max);
          var m = '<text x="' + x + '" y="' + (y+11) + '" class="rotulo-svg" style="font-size:11px">' + etq + '</text>';
          m += '<rect x="' + (x+120) + '" y="' + y + '" width="' + L + '" height="13" rx="2" fill="var(--surface-2)"></rect>';
          m += '<rect x="' + (x+120) + '" y="' + y + '" width="' + (L*p).toFixed(1) + '" height="13" rx="2" fill="' + col + '"></rect>';
          m += '<text x="' + (x+120+L+10) + '" y="' + (y+11) + '" class="rotulo-svg" style="font-size:11px">' + uni + '</text>';
          return m;
        }

        function pinta(){
          var d = M[sel], m = '';
          /* Geometria real de una bici de carretera, a escala 0.138 desde mm:
             entre ejes 990 · rueda 680 · vaina 410 · caida del pedalier 70
             tija 540 a 73.5 grados · direccion 140 a 72 grados
             La proporcion rueda/entre-ejes sale 0.34, la real.                */
          var RB={x:52.0,y:150.0}, RD={x:188.6,y:150.0}, PED={x:107.7,y:159.7};
          var SIL={x:86.6,y:88.2}, DA={x:161.8,y:92.2}, DB={x:167.8,y:110.6};
          var SILLIN={x:76.9,y:55.6}, MAN={x:165.8,y:70.2}, R=46.9;

          /* ruedas */
          m += '<circle cx="'+RB.x+'" cy="'+RB.y+'" r="'+R+'" fill="none" stroke="var(--line)" stroke-width="3.5"></circle>';
          m += '<circle cx="'+RD.x+'" cy="'+RD.y+'" r="'+R+'" fill="none" stroke="var(--line)" stroke-width="3.5"></circle>';
          m += '<circle cx="'+RB.x+'" cy="'+RB.y+'" r="3" fill="var(--ink-soft)"></circle>';
          m += '<circle cx="'+RD.x+'" cy="'+RD.y+'" r="3" fill="var(--ink-soft)"></circle>';

          /* horquilla, tija del sillin y manillar, en gris: no son el cuadro */
          m += '<g fill="none" stroke="var(--ink-soft)" stroke-width="4" stroke-linecap="round">'
             + '<path d="M'+DB.x+' '+DB.y+' L'+RD.x+' '+RD.y+'"></path>'
             + '<path d="M'+SIL.x+' '+SIL.y+' L'+SILLIN.x+' '+SILLIN.y+'"></path>'
             + '<path d="M'+DA.x+' '+DA.y+' L'+MAN.x+' '+MAN.y+'"></path>'
             + '</g>';
          /* sillin, inclinado como la tija; manillar, en cuerno */
          m += '<path d="M'+(SILLIN.x-13)+' '+(SILLIN.y+4)+' q13 -7 26 -2" fill="none" '
             + 'stroke="var(--ink-soft)" stroke-width="6" stroke-linecap="round"></path>';
          m += '<path d="M'+(MAN.x-11)+' '+MAN.y+' h16 q8 0 8 8 v6" fill="none" '
             + 'stroke="var(--ink-soft)" stroke-width="4.5" stroke-linecap="round"></path>';

          /* el cuadro: triangulo delantero y triangulo trasero */
          m += '<g fill="none" stroke="'+d.col+'" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round">'
             + '<path d="M'+SIL.x+' '+SIL.y+' L'+DA.x+' '+DA.y+'"></path>'
             + '<path d="M'+PED.x+' '+PED.y+' L'+DB.x+' '+DB.y+'"></path>'
             + '<path d="M'+SIL.x+' '+SIL.y+' L'+PED.x+' '+PED.y+'"></path>'
             + '<path d="M'+DA.x+' '+DA.y+' L'+DB.x+' '+DB.y+'"></path>'
             + '<path d="M'+PED.x+' '+PED.y+' L'+RB.x+' '+RB.y+'"></path>'
             + '<path d="M'+SIL.x+' '+SIL.y+' L'+RB.x+' '+RB.y+'"></path>'
             + '</g>';
          m += '<circle cx="'+PED.x+'" cy="'+PED.y+'" r="6.5" fill="'+d.col+'"></circle>';

          /* nombre del material, bajo la bici */
          m += '<text x="120" y="232" text-anchor="middle" class="rotulo-svg" '
             + 'style="font-size:14px;fill:var(--ink);font-weight:500">' + d.nom + '</text>';

          var y = 34;
          m += barra(250, y, 0, 'Peso',        d.peso,  2.5, d.col, d.peso + ' kg'); y += 26;
          m += barra(250, y, 0, 'Precio',      d.precio, 1000, d.col, d.precio + ' &euro;'); y += 26;
          m += barra(250, y, 0, 'Dura',        d.vida,  5, 'var(--goo-verde)', ['', 'poco','poco','bastante','bastante','mucho'][d.vida] || d.vida); y += 26;
          m += barra(250, y, 0, 'Se repara',   d.repara, 5, 'var(--goo-verde)', ['', 'casi no','poco','normal','normal','f&aacute;cil'][d.repara] || d.repara); y += 26;
          m += barra(250, y, 0, 'Huella CO&#8322;', d.co2, 7, 'var(--goo-rojo)', d.co2 + ' kg/kg'); y += 26;

          svg.innerHTML = m;
          pie.innerHTML = d.txt;
        }
        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-b]'); if(!b) return;
          seg.querySelectorAll('button').forEach(function(x){ x.setAttribute('aria-pressed', x===b?'true':'false'); });
          sel = b.dataset.b; pinta();
        });
        pinta();
      })();
      </script>
'''

S1 = (
  bloque('00', u'Reto inicial &middot; 10 min', u'''
      <p>Coge cualquier objeto que tengas encima de la mesa. El boli, la mochila, la botella, la silla.</p>
      <div class="aviso">
        <span class="n-tag">La pregunta</span>
        <b>&iquest;Por qu&eacute; est&aacute; hecho de eso y no de otra cosa?</b> Cont&eacute;stalo por escrito, en una frase.
      </div>
      <p>Comparad las respuestas. Van a salir tres, y las tres son la misma: <i>porque s&iacute;</i>,
         <i>porque es barato</i> o <i>porque siempre se ha hecho as&iacute;</i>.</p>
      <p>Ninguna explica nada. Y sin embargo alguien tom&oacute; esa decisi&oacute;n, y la tom&oacute; por razones muy
         concretas que se pueden medir.</p>
  ''') +
  bloque('01', u'Teor&iacute;a &middot; 20 min', u'''
      <h3>El mismo objeto, tres materiales</h3>
      <p>Para ver que la elecci&oacute;n no es arbitraria hace falta un objeto que se fabrique <b>igual</b> en
         materiales distintos. La bicicleta sirve perfectamente: el mismo cuadro, la misma forma, y tres
         materiales que se usan de verdad.</p>
''' + ESCENA + u'''
      <p>F&iacute;jate en que <b>ninguno gana en todo</b>. El carbono es el m&aacute;s ligero y el peor de reparar.
         El acero es el m&aacute;s pesado y el que m&aacute;s dura. No hay un material mejor: hay un material
         <b>adecuado para lo que quieres hacer</b>.</p>

      <div class="copiar">
        <h4>Definiciones</h4>
        <p><b>Material t&eacute;cnico</b>: materia prima transformada para poder fabricar objetos con ella.</p>
        <p><b>Propiedad</b>: caracter&iacute;stica de un material que se puede <b>medir</b> y que determina si
           sirve o no para un uso concreto.</p>
        <p>Elegir un material es <b>comparar propiedades frente a lo que necesitas</b>, no buscar el mejor:
           el mejor no existe.</p>
      </div>

      <h3>Qu&eacute; se mide de un material</h3>
      <div class="copiar">
        <h4>Propiedades que hay que conocer</h4>
        <ul>
          <li><b>Dureza</b>: resistencia a ser rayado.</li>
          <li><b>Tenacidad</b>: aguanta golpes sin romperse. Lo contrario es <b>fragilidad</b>.</li>
          <li><b>Elasticidad</b>: se deforma y recupera su forma.</li>
          <li><b>Plasticidad</b>: se deforma y <b>no</b> la recupera. Si es en hilos, <b>ductilidad</b>;
              si es en l&aacute;minas, <b>maleabilidad</b>.</li>
          <li><b>Densidad</b>: cu&aacute;nto pesa un volumen dado. De ah&iacute; sale que algo sea «ligero».</li>
          <li><b>Conductividad</b>: deja pasar el calor o la electricidad. Lo contrario es <b>aislante</b>.</li>
        </ul>
      </div>

      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; no hace falta copiarlo</span>
        <p>Durante casi toda la historia esto no se eligi&oacute;: se usaba <b>lo que hab&iacute;a cerca</b>. Las casas
           del norte se hicieron de madera y las del sur de piedra y barro porque eso era lo que ten&iacute;an a
           mano, no porque nadie comparara propiedades.</p>
        <p>La idea de <b>elegir</b> el material es moderna y depende de dos cosas que antes no exist&iacute;an:
           poder <b>medir</b> las propiedades &mdash;los primeros ensayos sistem&aacute;ticos de resistencia son
           del siglo XVIII&mdash; y poder <b>transportar</b> materiales lejos de donde se extraen. Sin ferrocarril
           no hay elecci&oacute;n de material: hay lo que hay.</p>
      </div>
  ''') +
  bloque('02', u'Pr&aacute;ctica &middot; 25 min', ficha(
    u'Actividad 3 &middot; La autopsia de un objeto',
    [u'1.2', u'2.2'], u'Parejas &middot; 25 min', u'''
          <h4>Qu&eacute; hay que hacer</h4>
          <p>Elegid <b>un objeto del aula</b> que tenga al menos tres piezas de materiales distintos.
             Una silla, una mochila, unas tijeras, un boli.</p>
          <ol class="pasos">
            <li>Dibujadlo y se&ntilde;alad <b>tres piezas</b> de materiales diferentes.</li>
            <li>Para cada pieza: qu&eacute; material cre&eacute;is que es y <b>qu&eacute; dos propiedades</b> lo hac&iacute;an
                adecuado ah&iacute;.</li>
            <li>Para cada pieza: proponed <b>otro material</b> que tambi&eacute;n valdr&iacute;a y decid qu&eacute; se ganar&iacute;a
                y qu&eacute; se perder&iacute;a.</li>
            <li>Elegid la pieza que os parezca <b>peor resuelta</b> y justificad por qu&eacute;.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Las tres piezas son de materiales realmente distintos <b>(2 puntos)</b>.</li>
            <li>Las propiedades citadas son propiedades, no opiniones <b>(3 puntos)</b>.</li>
            <li>La alternativa es razonable y se dice qu&eacute; se pierde <b>(3 puntos)</b>.</li>
            <li>La cr&iacute;tica final est&aacute; argumentada <b>(2 puntos)</b>.</li>
          </ul>
          <div class="nota" style="margin-top:14px">
            <span class="n-tag">Aviso</span>
            «Es de plástico porque es barato» no puntúa. El precio no es una propiedad del material: es una
            consecuencia de sus propiedades, de su abundancia y de c&oacute;mo se fabrica.
          </div>
  ''')) +
  bloque('03', u'Cierre &middot; 5 min', u'''
      <p>Vuelve a la frase que escribiste al empezar la clase. Probablemente pon&iacute;a «porque es barato».</p>
      <p>Ahora podr&iacute;as escribir: <i>es de polipropileno porque es ligero, aislante, no se oxida y se puede
         moldear en caliente en una sola pieza</i>. Eso s&iacute; explica algo, y adem&aacute;s permite discutirlo.</p>
      <ol>
      ''' + pregunta(u'&iquest;Cu&aacute;l es el mejor material para un cuadro de bicicleta?',
                     u'<p>Pregunta trampa: <b>ninguno</b>. Depende de qu&eacute; te importe. Si es el peso, el carbono; si es que dure y se pueda arreglar, el acero; si quieres un equilibrio, el aluminio.</p>')
        + pregunta(u'Diferencia entre elasticidad y plasticidad.',
                   u'<p>En la <b>elasticidad</b> el material recupera su forma al dejar de apretar. En la <b>plasticidad</b> se queda deformado. Una goma es el&aacute;stica; la plastilina, pl&aacute;stica.</p>')
        + pregunta(u'&iquest;Por qu&eacute; el precio no es una propiedad del material?',
                   u'<p>Porque no es una caracter&iacute;stica del material en s&iacute;: es una <b>consecuencia</b> de lo abundante que sea, de lo que cueste extraerlo y de c&oacute;mo se fabrique. El mismo material cambia de precio sin cambiar sus propiedades.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Un material se elige comparando propiedades. Pero antes de medirlas hay que ir un paso atr&aacute;s:
        la pr&oacute;xima sesi&oacute;n va de <b>de d&oacute;nde sale</b> cada material.
      </div>
  '''))

S = [dict(corto=u'&iquest;Por qu&eacute; de eso?', titulo=u'Por qu&eacute; las cosas est&aacute;n hechas de lo que est&aacute;n hechas',
          entradilla=u'Ning&uacute;n material es el mejor. Elegir uno es comparar lo que sabe hacer con lo que t&uacute; necesitas.',
          minutado=[(u"10'", u'Reto'), (u"20'", u'Teor&iacute;a'), (u"25'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')],
          chips=[u'CE1 &middot; 1.2', u'CE2 &middot; 2.2', u'A.3', u'A.7'],
          cuerpo=S1)]

S.append(dict(
 corto=u'Medir propiedades', titulo=u'Medir, no opinar: los ensayos',
 entradilla=u'Una propiedad solo sirve para elegir un material si se puede medir. Y medir significa que cualquiera repita la prueba y le salga lo mismo.',
 minutado=[(u"10'", u'Reto'), (u"20'", u'Teor&iacute;a'), (u"25'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')],
 chips=[u'CE1 &middot; 1.2', u'CE2 &middot; 2.2', u'A.3', u'A.7'],
 cuerpo=(
  bloque('00', u'Reto inicial &middot; 10 min', u"""
      <p>En la primera sesi&oacute;n qued&oacute; claro que un material se elige <b>comparando propiedades</b>.
         Bien. Coge estas dos cosas de la mesa:</p>
      <div class="aviso">
        <span class="n-tag">La pregunta</span>
        <b>&iquest;Cu&aacute;l es m&aacute;s duro, tu boli o la mesa?</b> Cont&eacute;stalo, y sobre todo: <b>&iquest;c&oacute;mo lo
        sabes?</b>
      </div>
      <p>Aqu&iacute; empiezan los problemas. Casi todos contestar&aacute;n «la mesa, porque se nota». Pero <i>notarlo</i>
         no es saberlo. Si dos personas discrepan, &iquest;qui&eacute;n decide?</p>
      <p>Mientras la respuesta sea «se nota», seguimos en las opiniones de la primera sesi&oacute;n. Una propiedad
         solo sirve para elegir si se puede <b>medir</b> &mdash;y medir significa que cualquiera repita la
         prueba y le salga lo mismo.</p>
""") +
  bloque('01', u'Teor&iacute;a &middot; 20 min', u"""
      <h3>Medir la dureza sin ning&uacute;n aparato</h3>
      <p>La dureza fue de las primeras propiedades que se consiguieron medir, y se hizo de la forma m&aacute;s
         simple imaginable: <b>ver qui&eacute;n raya a qui&eacute;n</b>. Si A raya a B, A es m&aacute;s duro. Sin discusi&oacute;n
         posible.</p>

      <div class="escena" id="esc-mohs">
        <div class="escena-barra">
          <span class="escena-titulo">Ensayo de rayado &middot; elige con qu&eacute; rayas y a qui&eacute;n</span>
          <div class="seg" id="seg-mohs">
            <button type="button" data-m="reset">&#8635; Empezar de nuevo</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 240" id="svg-mohs" role="img"
               aria-label="Ensayo de rayado entre materiales seg&uacute;n la escala de Mohs"></svg>
        </div>
        <div class="pie" id="pie-mohs"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-mohs');
        var pie = document.getElementById('pie-mohs');
        var seg = document.getElementById('seg-mohs');
        if(!svg) return;

        /* dureza en la escala de Mohs, de 1 a 10 */
        var MAT = [
          {n:'U&ntilde;a',      d:2.5, c:'#f3d3b3'},
          {n:'Cobre',     d:3.0, c:'#c98a4b'},
          {n:'Hierro',    d:4.5, c:'#8d99a6'},
          {n:'Vidrio',    d:5.5, c:'#bfe0e8'},
          {n:'Acero',     d:6.5, c:'#7a8590'},
          {n:'Cuarzo',    d:7.0, c:'#e8e4da'},
          {n:'Diamante',  d:10,  c:'#dff1f7'}
        ];
        var raya = null, rayado = null;

        function pinta(){
          var m = '', X = 30, W = 82;
          MAT.forEach(function(x, i){
            var px = X + i*W;
            var sel = (raya === i) ? 'var(--goo-azul)' : ((rayado === i) ? 'var(--goo-rojo)' : 'var(--line)');
            m += '<g class="mat" data-i="' + i + '" style="cursor:pointer">';
            m += '<rect x="' + px + '" y="60" width="66" height="58" rx="4" fill="' + x.c +
                 '" stroke="' + sel + '" stroke-width="' + ((raya===i||rayado===i) ? 3.5 : 1.5) + '"></rect>';
            /* si esta siendo rayado y pierde, se le dibuja el arana~zo */
            if(rayado === i && raya !== null && MAT[raya].d > x.d){
              m += '<path d="M' + (px+12) + ' 78 L' + (px+54) + ' 100" stroke="#5f6368" stroke-width="2.5"></path>';
              m += '<path d="M' + (px+14) + ' 92 L' + (px+50) + ' 106" stroke="#5f6368" stroke-width="1.8"></path>';
            }
            m += '<text x="' + (px+33) + '" y="134" text-anchor="middle" class="rotulo-svg" '
               + 'style="font-size:10.5px">' + x.n + '</text>';
            m += '<text x="' + (px+33) + '" y="148" text-anchor="middle" class="rotulo-svg" '
               + 'style="font-size:9.5px;opacity:.65">' + x.d + '</text>';
            m += '</g>';
          });
          m += '<text x="30" y="30" class="rotulo-svg" style="font-size:11px">'
             + 'DUREZA CRECIENTE &#8594; &nbsp;&nbsp;escala de Mohs, de 1 a 10</text>';
          m += '<text x="30" y="186" class="rotulo-svg" style="font-size:11px;fill:var(--goo-azul)">'
             + '1 &middot; pulsa el material con el que rayas</text>';
          m += '<text x="30" y="204" class="rotulo-svg" style="font-size:11px;fill:var(--goo-rojo)">'
             + '2 &middot; pulsa el material al que rayas</text>';
          svg.innerHTML = m;

          if(raya === null){
            pie.innerHTML = 'La dureza no se mide con un aparato: se mide <b>a ver qui&eacute;n raya a qui&eacute;n</b>. '
              + 'Elige primero el material con el que rayas.';
          } else if(rayado === null){
            pie.innerHTML = 'Rayas con <b>' + MAT[raya].n + '</b> (dureza ' + MAT[raya].d + '). '
              + 'Ahora elige a qui&eacute;n intentas rayar.';
          } else {
            var a = MAT[raya], b = MAT[rayado];
            if(a.d > b.d){
              pie.innerHTML = '<b>' + a.n + ' raya a ' + b.n + '.</b> ' + a.d + ' es mayor que ' + b.d
                + ', as&iacute; que deja marca. Y esto es una <b>medida</b>, no una opini&oacute;n: lo repite cualquiera '
                + 'y sale lo mismo.';
            } else if (a.d === b.d){
              pie.innerHTML = 'Misma dureza: <b>ninguno raya al otro</b>. Cuando eso pasa, se les asigna el '
                + 'mismo n&uacute;mero en la escala.';
            } else {
              pie.innerHTML = '<b>' + a.n + ' no puede rayar a ' + b.n + '.</b> ' + a.d + ' es menor que '
                + b.d + '. Aqu&iacute; el que se lleva la marca es el que raya.';
            }
          }
        }

        svg.addEventListener('click', function(e){
          var g = e.target.closest('.mat'); if(!g) return;
          var i = +g.dataset.i;
          if(raya === null) raya = i;
          else if(rayado === null) rayado = i;
          else { raya = i; rayado = null; }
          pinta();
        });
        seg.addEventListener('click', function(){ raya = null; rayado = null; pinta(); });
        pinta();
      })();
      </script>

      <div class="copiar">
        <h4>Ensayo</h4>
        <p><b>Ensayo</b>: prueba normalizada que se hace sobre un material para <b>medir</b> una de sus
           propiedades, de forma que el resultado sea el mismo lo haga quien lo haga.</p>
        <p><b>Dureza</b>: resistencia a ser rayado. Se mide con la <b>escala de Mohs</b>, del 1 (talco) al
           10 (diamante). Cada material raya a los de n&uacute;mero menor y es rayado por los de n&uacute;mero mayor.</p>
      </div>

      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; no hace falta copiarlo</span>
        <p>La escala la propuso el mineralogista <b>Friedrich Mohs</b> en 1812, y su genialidad no fue
           cient&iacute;fica sino pr&aacute;ctica: no necesita ning&uacute;n instrumento. Un ge&oacute;logo en mitad del campo pod&iacute;a
           identificar un mineral con la u&ntilde;a, una moneda de cobre y una navaja.</p>
        <p>Es una escala <b>ordinal</b>: dice qui&eacute;n va delante de qui&eacute;n, no cu&aacute;nto. El diamante es un 10 y
           el corind&oacute;n un 9, pero el diamante no es «uno m&aacute;s duro»: es unas cuatro veces m&aacute;s duro. Por eso
           en la industria se usan hoy otras escalas &mdash;Brinell, Rockwell, Vickers&mdash; que s&iacute; dan
           n&uacute;meros proporcionales. La de Mohs sobrevive porque sigue siendo la &uacute;nica que funciona
           sin enchufe.</p>
      </div>

      <h3>Los otros ensayos</h3>
      <div class="copiar">
        <h4>Ensayos mec&aacute;nicos que hay que conocer</h4>
        <ul>
          <li><b>Tracci&oacute;n</b>: se estira la probeta hasta romperla. Mide la resistencia y si el material
              <b>avisa</b> antes de romper.</li>
          <li><b>Compresi&oacute;n</b>: se aplasta. Importa en pilares y estructuras.</li>
          <li><b>Flexi&oacute;n</b>: se apoya por los extremos y se carga en el centro.</li>
          <li><b>Resiliencia</b>: se golpea de un martillazo. Distingue lo <b>tenaz</b> de lo <b>fr&aacute;gil</b>.</li>
          <li><b>Fatiga</b>: se carga y descarga miles de veces. Un material puede aguantar un golpe fuerte
              y romperse por muchos golpes flojos.</li>
        </ul>
      </div>
      <div class="nota">
        <span class="n-tag">De aqu&iacute; sal&iacute;a lo del aluminio</span>
        En la primera sesi&oacute;n el cuadro de aluminio dec&iacute;a «se fatiga: puede fallar sin aviso». Ahora ya
        sabes de d&oacute;nde sale ese dato: de un <b>ensayo de fatiga</b>, no de la impresi&oacute;n de nadie.
      </div>
""") +
  bloque('02', u'Pr&aacute;ctica &middot; 25 min', ficha(
    u'Actividad 4 &middot; Montar una escala de dureza del aula',
    [u'1.2', u'2.2'], u'Grupos de tres &middot; 25 min', u"""
          <h4>Qu&eacute; hay que hacer</h4>
          <p>Vais a construir <b>vuestra propia escala de Mohs</b> con lo que hay en el aula. Nada de
             aparatos: solo rayar.</p>
          <ol class="pasos">
            <li>Reunid <b>seis objetos</b> de materiales distintos: u&ntilde;a, goma, moneda, l&aacute;piz, llave,
                tijeras, un trozo de baldosa, lo que ten&eacute;is.</li>
            <li>Rayad <b>cada uno con cada uno</b>. Son quince parejas. Anotad en una tabla qui&eacute;n raya a
                qui&eacute;n.</li>
            <li><b>Ordenadlos</b> de menos a m&aacute;s duro a partir de esos resultados.</li>
            <li>Comprobad que el orden es <b>coherente</b>: si A raya a B y B raya a C, A tiene que rayar
                a C. Si no se cumple, algo hab&eacute;is medido mal. Repetid esa pareja.</li>
            <li>Intercambiad la tabla con otro grupo. &iquest;Os sale el mismo orden?</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>La tabla de quince parejas est&aacute; completa <b>(3 puntos)</b>.</li>
            <li>El orden final se deduce de la tabla, no de lo que os parec&iacute;a <b>(3 puntos)</b>.</li>
            <li>Hab&eacute;is comprobado la coherencia y repetido lo que fallaba <b>(2 puntos)</b>.</li>
            <li>Est&aacute; anotada la comparaci&oacute;n con el otro grupo <b>(2 puntos)</b>.</li>
          </ul>
          <div class="nota" style="margin-top:14px">
            <span class="n-tag">Lo que de verdad se est&aacute; evaluando</span>
            El paso 5. Si a dos grupos les sale el mismo orden con los mismos objetos, acab&aacute;is de
            demostrar que eso <b>es una medida</b>. Si os sale distinto, hay que averiguar por qu&eacute; &mdash;y
            esa investigaci&oacute;n vale m&aacute;s que la tabla.
          </div>
  """)) +
  bloque('03', u'Cierre &middot; 5 min', u"""
      <p>Volved a la pregunta del principio: &iquest;qu&eacute; es m&aacute;s duro, el boli o la mesa?</p>
      <p>Ya no hace falta contestar «se nota». Ahora se contesta <b>rayando</b>, y si alguien discrepa, se
         repite la prueba delante de &eacute;l.</p>
      <ol>
      """ + pregunta(u'&iquest;Qu&eacute; es un ensayo y en qu&eacute; se diferencia de una impresi&oacute;n?',
                     u'<p>Es una prueba <b>normalizada</b>: hecha siempre igual, de modo que el resultado no dependa de qui&eacute;n la haga. Una impresi&oacute;n s&iacute; depende de qui&eacute;n la tenga.</p>')
        + pregunta(u'Un material aguanta un martillazo pero se rompe tras meses de vibraci&oacute;n. &iquest;Qu&eacute; ensayo lo detecta?',
                   u'<p>El de <b>fatiga</b>, que carga y descarga miles de veces. El de resiliencia solo mide el golpe &uacute;nico, y ese lo aguantaba.</p>')
        + pregunta(u'&iquest;Por qu&eacute; se dice que la escala de Mohs es ordinal?',
                   u'<p>Porque dice <b>qui&eacute;n va delante de qui&eacute;n, pero no cu&aacute;nto</b>. Del 9 al 10 hay mucha m&aacute;s diferencia que del 1 al 2, aunque el salto de n&uacute;mero sea el mismo.</p>') + u"""
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Elegir y medir: hecho. Toca mirar de cerca una familia de materiales, la m&aacute;s joven
        de todas: <b>los pl&aacute;sticos</b>, que hubo que inventar.
      </div>
  """))))


S.append(dict(
 corto=u'La madera', titulo=u'La madera: el &uacute;nico material que crece',
 entradilla=u'Por qu&eacute; la le&ntilde;a se raja siempre a lo largo, y por qu&eacute; esa respuesta explica desde el contrachapado hasta el mueble de tu casa.',
 minutado=[(u"10'", u'Reto'), (u"20'", u'Teor&iacute;a'), (u"25'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')],
 chips=[u'CE1 &middot; 1.2', u'CE2 &middot; 2.2', u'A.3', u'A.7'],
 cuerpo=(
  bloque('00', u'Reto inicial &middot; 10 min', u"""
      <p>Una pregunta de las que parecen tontas y no lo son:</p>
      <div class="aviso">
        <span class="n-tag">La pregunta</span>
        <b>&iquest;Por qu&eacute; la le&ntilde;a se raja siempre a lo largo y nunca a lo ancho?</b>
      </div>
      <p>Todo el mundo lo ha visto, nadie lo ha pensado. Y la respuesta explica pr&aacute;cticamente todo lo que
         hay que saber sobre la madera, incluido por qu&eacute; hubo que inventar el contrachapado.</p>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; no hace falta copiarlo</span>
        <p>La madera tiene una rareza que ning&uacute;n otro material de este tema comparte: <b>es el &uacute;nico que
           crece</b>. No se funde, no se moldea, no se sintetiza. Se corta de algo que estuvo vivo y que
           pas&oacute; d&eacute;cadas construy&eacute;ndose a s&iacute; mismo, con una estructura orientada a aguantar su propio
           peso y el viento.</p>
        <p>Por eso sus propiedades <b>dependen de la direcci&oacute;n</b>. Esa idea tiene nombre &mdash;anisotrop&iacute;a&mdash;
           y es rar&iacute;sima: el acero se comporta igual lo mires por donde lo mires. La madera no.</p>
      </div>
""") +
  bloque('01', u'Teor&iacute;a &middot; 20 min', u"""
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
        <div class="pie" id="pie-veta"></div>
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
          <li><b>Maderas blandas</b>: de <b>con&iacute;feras</b>, que crecen r&aacute;pido &mdash;pino,
              abeto&mdash;. Baratas, ligeras, f&aacute;ciles de trabajar. Es lo que hay en el taller del instituto.</li>
          <li><b>Maderas duras</b>: de <b>frondosas</b>, de crecimiento lento &mdash;roble, haya, nogal&mdash;.
              Caras, pesadas, resistentes y bonitas. Muebles y suelos.</li>
        </ul>
        <p>Cuidado con los nombres: <b>la balsa es una madera dura</b> aunque se corte con la u&ntilde;a. La
           clasificaci&oacute;n es bot&aacute;nica, no de dureza real.</p>
      </div>

      <figure class="foto">
        <img src="../../../img/u3-madera.jpg" width="1200" height="675" loading="lazy"
             alt="Tabla de pino cepillada con tres nudos redondos y la veta desvi&aacute;ndose alrededor de cada uno">
        <figcaption>Esto es <b>pino</b>, la madera blanda del taller del instituto. Tres <b>nudos</b> y la veta desvi&aacute;ndose para rodearlos: un nudo es donde estaba una <b>rama</b>, y la fibra del tronco tuvo que abrirse para dejarla salir. De ah&iacute; salen las dos cosas que m&aacute;s te van a pasar cortando: la madera se raja <b>a lo largo de la fibra</b> y nunca a lo ancho, y una tabla con un nudo en medio es m&aacute;s d&eacute;bil justo ah&iacute;.
          <br><br>Foto de <b>Eleonora Vokueva</b> en Pexels. Es de su autor y no forma parte del material
          publicado bajo la licencia de esta p&aacute;gina.</figcaption>
      </figure>

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
""") +
  bloque('02', u'Pr&aacute;ctica &middot; 25 min', ficha(
    u'Actividad 5 &middot; Identificar maderas en el aula',
    [u'1.2', u'2.2'], u'Parejas &middot; 25 min', u"""
          <h4>Qu&eacute; hay que hacer</h4>
          <p>El aula est&aacute; llena de madera y de derivados, y casi nadie distingue unos de otros.</p>
          <ol class="pasos">
            <li>Encontrad <b>cinco piezas</b> de madera o derivado: mesa, silla, puerta, estanter&iacute;a,
                marco, regla.</li>
            <li>Para cada una, decid si es <b>maciza, contrachapado, aglomerado, DM o chapada</b>. Pista:
                mirad el <b>canto</b>, que es donde se ve la verdad.</li>
            <li>Justificad cada respuesta con <b>lo que hab&eacute;is visto</b>, no con lo que os parece: «se ven
                virutas en el canto», «se ven capas finas», «la veta de la cara no sigue en el canto».</li>
            <li>Para cada pieza: &iquest;por qu&eacute; cre&eacute;is que se eligi&oacute; ese material y no madera maciza?</li>
            <li>Buscad una pieza donde, en vuestra opini&oacute;n, <b>se eligi&oacute; mal</b>. Explicad por qu&eacute;.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Las cinco piezas est&aacute;n identificadas <b>(3 puntos)</b>.</li>
            <li>Cada identificaci&oacute;n se justifica con una observaci&oacute;n concreta <b>(3 puntos)</b>.</li>
            <li>Las razones de la elecci&oacute;n son t&eacute;cnicas o econ&oacute;micas, no opiniones <b>(2 puntos)</b>.</li>
            <li>La cr&iacute;tica final est&aacute; argumentada <b>(2 puntos)</b>.</li>
          </ul>
          <div class="nota" style="margin-top:14px">
            <span class="n-tag">D&oacute;nde mirar</span>
            <b>El canto lo delata todo.</b> Si ves virutas grandes, aglomerado. Si ves capas finas como un
            hojaldre, contrachapado. Si es liso y uniforme como cart&oacute;n muy duro, DM. Si la veta de la cara
            no contin&uacute;a por el canto, est&aacute; chapado.
          </div>
  """)) +
  bloque('03', u'Cierre &middot; 5 min', u"""
      <p>Volvamos a la le&ntilde;a del principio. Se raja a lo largo porque a lo largo solo hay que
         <b>separar fibras</b>, y eso es f&aacute;cil. A lo ancho habr&iacute;a que <b>romperlas</b>, y eso es
         much&iacute;simo m&aacute;s dif&iacute;cil.</p>
      <p>Y de ah&iacute; sale todo lo dem&aacute;s: por qu&eacute; las vigas se ponen con la veta a lo largo, por qu&eacute; una
         regla de madera se parte siempre igual, y por qu&eacute; alguien tuvo la idea de cruzar las capas.</p>
      <ol>
      """ + pregunta(u'&iquest;Qu&eacute; significa que la madera sea anis&oacute;tropa?',
                     u'<p>Que <b>sus propiedades cambian seg&uacute;n la direcci&oacute;n</b>. Aguanta mucho a lo largo de la veta y poco a lo ancho. El acero, en cambio, se comporta igual en todas.</p>')
        + pregunta(u'&iquest;Qu&eacute; problema resuelve exactamente el contrachapado?',
                   u'<p>La <b>anisotrop&iacute;a</b>. Al cruzar la veta de cada capa 90&deg;, ninguna direcci&oacute;n queda d&eacute;bil: para partirlo habr&iacute;a que separar las fibras de una capa y romper las de la siguiente.</p>')
        + pregunta(u'La balsa se corta con la u&ntilde;a. &iquest;Es madera blanda?',
                   u'<p>No: es <b>madera dura</b>. La clasificaci&oacute;n es bot&aacute;nica &mdash;hoja caduca o perenne&mdash;, no de dureza real. Es de los pocos casos donde el nombre enga&ntilde;a.</p>') + u"""
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        La madera creci&oacute;. Los metales hay que <b>sacarlos de una piedra</b>, y eso cambia absolutamente
        todo: el precio, la energ&iacute;a que cuestan y lo que se puede hacer con ellos.
      </div>
  """))))


S.append(dict(
 corto=u'Metales', titulo=u'Los metales: hay que sacarlos de una piedra',
 entradilla=u'Una piedra no se parece a una espada. Entender ese salto explica el precio de los metales, su huella y por qu&eacute; se reciclan tanto.',
 minutado=[(u"10'", u'Reto'), (u"20'", u'Teor&iacute;a'), (u"25'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')],
 chips=[u'CE1 &middot; 1.2', u'CE2 &middot; 2.2', u'CE7 &middot; 7.1', u'A.7', u'E.1'],
 cuerpo=(
  bloque('00', u'Reto inicial &middot; 10 min', u"""
      <p>La madera se corta de un &aacute;rbol: se ve el &aacute;rbol, se ve la tabla, se entiende. Con el metal hay
         un salto que no es evidente en absoluto.</p>
      <div class="aviso">
        <span class="n-tag">La pregunta</span>
        Una piedra no se parece en nada a una espada. <b>&iquest;C&oacute;mo se le ocurri&oacute; a alguien que dentro de
        esa piedra hab&iacute;a metal?</b> &iquest;Y c&oacute;mo consigui&oacute; sacarlo?
      </div>
      <p>Pi&eacute;nsalo en serio treinta segundos antes de seguir. No hay ninguna pista en el aspecto de un
         mineral que sugiera que calent&aacute;ndolo mucho, con las cosas adecuadas al lado, sale un l&iacute;quido
         brillante.</p>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; no hace falta copiarlo</span>
        <p>Probablemente fue un accidente, y probablemente ocurri&oacute; en un horno de cer&aacute;mica. Al cocer
           vasijas se alcanzan temperaturas altas, y si el barro o la le&ntilde;a llevaban mineral de cobre,
           alguien encontr&oacute; gotas de metal entre las cenizas.</p>
        <p>Lo interesante no es el hallazgo: es que <b>alguien se diera cuenta de que se pod&iacute;a repetir</b>.
           Eso ya no es suerte, es el principio de la metalurgia. Y separa la Edad de Piedra de todo lo
           dem&aacute;s: por primera vez el ser humano no usa un material que encuentra, sino uno que
           <b>fabrica</b>.</p>
      </div>
""") +
  bloque('01', u'Teor&iacute;a &middot; 20 min', u"""
      <h3>El metal cuesta energ&iacute;a, y eso lo explica casi todo</h3>
      <p>La diferencia esencial con la madera: el metal <b>no existe puro en la naturaleza</b> salvo
         excepciones. Est&aacute; combinado con otros elementos formando un <b>mineral</b>, y separarlo exige
         meter much&iacute;sima energ&iacute;a.</p>

      <div class="escena" id="esc-metal">
        <div class="escena-barra">
          <span class="escena-titulo">Lo que cuesta un kilo de metal</span>
          <div class="seg" id="seg-metal">
            <button type="button" data-m="aluminio" aria-pressed="true">Aluminio</button>
            <button type="button" data-m="acero">Acero</button>
            <button type="button" data-m="cobre">Cobre</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 250" id="svg-metal" role="img"
               aria-label="Energ&iacute;a necesaria para producir un kilo de metal desde el mineral frente a reciclarlo"></svg>
        </div>
        <div class="pie" id="pie-metal"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-metal');
        var pie = document.getElementById('pie-metal');
        var seg = document.getElementById('seg-metal');
        if(!svg) return;

        /* kWh por kg, valores redondeados de fuentes industriales */
        var MET = {
          aluminio:{n:'Aluminio', mineral:'Bauxita', virgen:45, reciclado:2.3, col:'#b9c2cc',
            txt:'Sacar aluminio de la bauxita exige <b>electrolisis</b>: pasar corriente a lo bruto durante '
              + 'horas. Por eso las f&aacute;bricas de aluminio se ponen al lado de centrales el&eacute;ctricas. '
              + 'Reciclarlo solo pide fundirlo, y eso es <b>el 5&nbsp;% de la energ&iacute;a</b>. Una lata reciclada '
              + 'ahorra veinte veces lo que cuesta hacerla nueva.'},
          acero:{n:'Acero', mineral:'Hematita', virgen:14, reciclado:5.5, col:'#7a8590',
            txt:'El hierro se saca del mineral en un <b>alto horno</b>, quem&aacute;ndolo con carb&oacute;n a 1.500&nbsp;&deg;C. '
              + 'Reciclarlo cuesta menos de la mitad, y adem&aacute;s es el material m&aacute;s reciclado del mundo: es '
              + '<b>magn&eacute;tico</b>, as&iacute; que separarlo de la basura es trivial.'},
          cobre:{n:'Cobre', mineral:'Calcopirita', virgen:16, reciclado:1.5, col:'#c98a4b',
            txt:'Reciclar cobre cuesta <b>menos del 10&nbsp;%</b> que extraerlo. Y eso explica un problema '
              + 'muy real: el robo de cable. No se roba por el cable, se roba porque el cobre recuperado '
              + 'vale casi lo mismo que el nuevo.'}
        };
        var sel = 'aluminio';

        function pinta(){
          var d = MET[sel], m = '';
          var X = 168, W = 372, MAX = 46;

          function fila(y, etq, val, col, sub){
            var w = W * val / MAX;
            var s = '<text x="' + (X-12) + '" y="' + (y+16) + '" text-anchor="end" class="rotulo-svg" '
                  + 'style="font-size:11.5px;fill:var(--ink)">' + etq + '</text>';
            s += '<rect x="' + X + '" y="' + y + '" width="' + W + '" height="24" rx="3" fill="var(--surface-2)"></rect>';
            s += '<rect x="' + X + '" y="' + y + '" width="' + w.toFixed(1) + '" height="24" rx="3" fill="' + col + '"></rect>';
            s += '<text x="' + (X + w + 10) + '" y="' + (y+16) + '" class="rotulo-svg" '
               + 'style="font-size:12px;fill:var(--ink);font-weight:500">' + val + ' kWh</text>';
            s += '<text x="' + (X-12) + '" y="' + (y+30) + '" text-anchor="end" class="rotulo-svg" '
               + 'style="font-size:9.5px;opacity:.7">' + sub + '</text>';
            return s;
          }

          m += '<text x="' + (X-12) + '" y="34" text-anchor="end" class="rotulo-svg" style="font-size:11px">'
             + d.n.toUpperCase() + '</text>';
          m += fila(56,  'Desde el mineral', d.virgen,    d.col,               'a partir de ' + d.mineral);
          m += fila(136, 'Reciclado',        d.reciclado, 'var(--goo-verde)',  'fundiendo chatarra');

          var ahorro = Math.round((1 - d.reciclado/d.virgen) * 100);
          m += '<text x="' + (X + W/2) + '" y="222" text-anchor="middle" class="rotulo-svg" '
             + 'style="font-size:15px;fill:var(--goo-verde);font-weight:500">'
             + 'Reciclar ahorra el ' + ahorro + ' % de la energ&iacute;a</text>';
          svg.innerHTML = m;
          pie.innerHTML = d.txt;
        }
        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-m]'); if(!b) return;
          seg.querySelectorAll('button').forEach(function(x){ x.setAttribute('aria-pressed', x===b?'true':'false'); });
          sel = b.dataset.m; pinta();
        });
        pinta();
      })();
      </script>

      <p>Mira esas barras un momento m&aacute;s. <b>No son datos de ecolog&iacute;a: son datos de econom&iacute;a.</b> Un
         material que cuesta 45 kWh producir y 2 reciclar tiene el reciclaje garantizado, porque sale
         a cuenta aunque a nadie le importe el planeta.</p>

      <div class="copiar">
        <h4>De la piedra al metal</h4>
        <p><b>Mineral</b>: roca que contiene el metal combinado con otros elementos.</p>
        <p><b>Metalurgia</b>: conjunto de t&eacute;cnicas para separar el metal de su mineral y trabajarlo.</p>
        <p><b>Aleaci&oacute;n</b>: mezcla de un metal con otros elementos para mejorar sus propiedades. Casi
           nada se fabrica con metales puros.</p>
      </div>

      <h3>Los dos grandes grupos</h3>
      <div class="copiar">
        <h4>F&eacute;rricos y no f&eacute;rricos</h4>
        <ul>
          <li><b>F&eacute;rricos</b>: contienen hierro. <b>Acero</b> (hierro + carbono, hasta 2&nbsp;%) y
              <b>fundici&oacute;n</b> (m&aacute;s de 2&nbsp;%). Baratos, resistentes y <b>magn&eacute;ticos</b>, pero se
              <b>oxidan</b>.</li>
          <li><b>No f&eacute;rricos</b>: sin hierro. <b>Aluminio</b> (ligero, no se oxida por dentro),
              <b>cobre</b> (el mejor conductor asequible), <b>zinc</b>, <b>esta&ntilde;o</b>, <b>plomo</b>.</li>
          <li>Aleaciones cl&aacute;sicas: <b>bronce</b> (cobre + esta&ntilde;o), <b>lat&oacute;n</b> (cobre + zinc),
              <b>acero inoxidable</b> (acero + cromo).</li>
        </ul>
      </div>

      <div class="nota">
        <span class="n-tag">Un truco que siempre funciona</span>
        &iquest;Es f&eacute;rrico? <b>Ac&eacute;rcale un im&aacute;n.</b> Si se pega, lleva hierro. Es el mismo truco que usan las
        plantas de reciclaje para separar miles de toneladas al d&iacute;a: un electroim&aacute;n gigante sobre una
        cinta transportadora.
      </div>

      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>El aluminio es el <b>tercer elemento m&aacute;s abundante</b> de la corteza terrestre, m&aacute;s que el
           hierro. Y sin embargo en 1850 val&iacute;a m&aacute;s que el oro: Napoleón III reservaba los cubiertos de
           aluminio para sus invitados de honor y daba los de oro al resto.</p>
        <p>&iquest;Por qu&eacute;? Porque nadie sab&iacute;a separarlo. El aluminio est&aacute; tan bien agarrado a su mineral que
           hizo falta la <b>electricidad</b> para arrancarlo, y eso no lleg&oacute; hasta 1886. En veinte a&ntilde;os
           pas&oacute; de metal precioso a material de envase. <b>El valor de un material no depende de lo raro
           que sea, sino de lo que cueste obtenerlo.</b></p>
      </div>
""") +
  bloque('02', u'Pr&aacute;ctica &middot; 25 min', ficha(
    u'Actividad 6 &middot; Auditor&iacute;a met&aacute;lica del aula',
    [u'1.2', u'7.1'], u'Parejas &middot; 25 min', u"""
          <h4>Qu&eacute; hay que hacer</h4>
          <p>Con un im&aacute;n peque&ntilde;o, de los de la nevera, se puede auditar un aula entera.</p>
          <ol class="pasos">
            <li>Encontrad <b>seis piezas met&aacute;licas</b>: patas de mesa, tornillos, bisagras, el marco de
                la ventana, una lata, el cable de un cargador.</li>
            <li>Pasad el im&aacute;n por cada una y clasificadlas en <b>f&eacute;rricas</b> y <b>no f&eacute;rricas</b>.</li>
            <li>Para cada una, proponed <b>qu&eacute; metal o aleaci&oacute;n</b> es y en qu&eacute; os bas&aacute;is: color, peso,
                si se oxida, si conduce.</li>
            <li>Para cada una, <b>&iquest;por qu&eacute; ese metal ah&iacute;?</b> Una raz&oacute;n t&eacute;cnica, no &laquo;porque s&iacute;&raquo;.</li>
            <li>Elegid la que os parezca <b>m&aacute;s cara de producir</b> y justificadlo con lo visto en la
                escena de la energ&iacute;a.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Las seis piezas est&aacute;n clasificadas con el im&aacute;n <b>(2 puntos)</b>.</li>
            <li>La propuesta de metal se justifica con algo observable <b>(3 puntos)</b>.</li>
            <li>Las razones de uso son t&eacute;cnicas <b>(3 puntos)</b>.</li>
            <li>La estimaci&oacute;n de coste energ&eacute;tico est&aacute; razonada <b>(2 puntos)</b>.</li>
          </ul>
          <div class="nota" style="margin-top:14px">
            <span class="n-tag">Ojo con una trampa</span>
            El <b>acero inoxidable</b> de algunos fregaderos y cubiertos <b>no se pega al im&aacute;n</b> aunque
            lleva hierro: el cromo y el n&iacute;quel le cambian la estructura interna. Si os pasa, no lo
            tach&eacute;is: anotadlo. Es justo la clase de excepci&oacute;n que merece la pena descubrir.
          </div>
  """)) +
  bloque('03', u'Cierre &middot; 5 min', u"""
      <p>Volvamos a la piedra del principio. Entre aquella piedra y una espada hay <b>energ&iacute;a</b>: mucho
         calor, mucho tiempo y mucho trabajo.</p>
      <p>Y esa energ&iacute;a no desaparece cuando el objeto se tira. Sigue ah&iacute;, dentro del metal. Por eso
         reciclar no es un gesto simb&oacute;lico: es <b>recuperar la energ&iacute;a que ya se gast&oacute;</b>.</p>
      <ol>
      """ + pregunta(u'&iquest;Por qu&eacute; el aluminio val&iacute;a m&aacute;s que el oro en 1850 si es abundant&iacute;simo?',
                     u'<p>Porque nadie sab&iacute;a separarlo de su mineral: hizo falta la electricidad, que no lleg&oacute; hasta 1886. <b>El valor depende de lo que cueste obtenerlo</b>, no de lo raro que sea.</p>')
        + pregunta(u'&iquest;Qu&eacute; diferencia hay entre acero y fundici&oacute;n?',
                   u'<p>La cantidad de <b>carbono</b>. Hasta el 2&nbsp;por ciento es acero; por encima, fundici&oacute;n. M&aacute;s carbono da m&aacute;s dureza pero tambi&eacute;n m&aacute;s fragilidad.</p>')
        + pregunta(u'Reciclar aluminio ahorra casi toda la energ&iacute;a. &iquest;Por qu&eacute; tanto?',
                   u'<p>Porque lo caro era <b>separarlo del mineral por electrolisis</b>, y eso ya est&aacute; hecho. Reciclar solo exige fundirlo, que es much&iacute;simo m&aacute;s barato.</p>') + u"""
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        La madera creci&oacute;. El metal se arranc&oacute; de una piedra. Los <b>pl&aacute;sticos</b> no estaban ah&iacute;:
        hubo que inventarlos, mol&eacute;cula a mol&eacute;cula. Y ese es otro salto distinto.
      </div>
  """))))


S.append(dict(
 corto=u'Pl&aacute;sticos', titulo=u'Los pl&aacute;sticos: hubo que inventarlos',
 entradilla=u'No estaban en ninguna parte esperando a que alguien los encontrara. Y se inventaron, ir&oacute;nicamente, para dejar de matar elefantes.',
 minutado=[(u"10'", u'Reto'), (u"20'", u'Teor&iacute;a'), (u"25'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')],
 chips=[u'CE1 &middot; 1.2', u'CE2 &middot; 2.2', u'CE7 &middot; 7.1', u'A.7', u'E.1'],
 cuerpo=(
  bloque('00', u'Reto inicial &middot; 10 min', u"""
      <p>La madera creci&oacute;. El metal estaba dentro de una piedra. Con los pl&aacute;sticos pasa algo distinto:</p>
      <div class="aviso">
        <span class="n-tag">El dato</span>
        <b>Los pl&aacute;sticos no exist&iacute;an.</b> No estaban en ning&uacute;n sitio esperando a que alguien los
        encontrara. Hubo que <b>inventarlos</b>.
      </div>
      <p>&iquest;Y por qu&eacute; se inventaron? Aqu&iacute; viene lo bueno, y no es lo que esperas.</p>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; no hace falta copiarlo</span>
        <p>En 1863, una empresa de billares de Nueva York ofreci&oacute; <b>10.000 d&oacute;lares</b> &mdash;una fortuna
           entonces&mdash; a quien encontrara un sustituto del <b>marfil</b> para las bolas. Se estaban
           quedando sin elefantes, y con ellos sin negocio.</p>
        <p>John Wesley Hyatt gan&oacute; el premio en 1869 con el <b>celuloide</b>. Funcionaba, aunque con un
           inconveniente memorable: era tan inflamable que, seg&uacute;n contaban los due&ntilde;os de los salones, a
           veces el choque de dos bolas provocaba un peque&ntilde;o estallido y los vaqueros sacaban la pistola.</p>
        <p>El primer pl&aacute;stico totalmente sint&eacute;tico lleg&oacute; en 1907: la <b>baquelita</b>, de Leo Baekeland.
           Y merece la pena quedarse con la iron&iacute;a: <b>los pl&aacute;sticos se inventaron para dejar de matar
           elefantes y tortugas</b>. Hoy son el s&iacute;mbolo del problema ambiental. Ninguna tecnolog&iacute;a nace
           buena ni mala: nace resolviendo algo, y crea lo siguiente.</p>
      </div>
""") +
  bloque('01', u'Teor&iacute;a &middot; 20 min', u"""
      <h3>Qu&eacute; es un pl&aacute;stico por dentro</h3>
      <p>Un pl&aacute;stico es un <b>pol&iacute;mero</b>: mol&eacute;culas larguísimas formadas repitiendo una peque&ntilde;a
         unidad miles de veces, como un collar de cuentas iguales. Y casi todo su comportamiento depende
         de <b>c&oacute;mo est&eacute;n esas cadenas entre s&iacute;</b>.</p>

      <div class="escena" id="esc-plast">
        <div class="escena-barra">
          <span class="escena-titulo">Calentar un pl&aacute;stico &middot; pulsa el mechero</span>
          <div class="seg" id="seg-plast">
            <button type="button" data-p="termo" aria-pressed="true">Termopl&aacute;stico</button>
            <button type="button" data-p="estable">Termoestable</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 230" id="svg-plast" role="img"
               aria-label="Al calentarlo, un termopl&aacute;stico se ablanda y se puede remoldear; un termoestable se quema"></svg>
        </div>
        <div class="pie" id="pie-plast"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-plast');
        var pie = document.getElementById('pie-plast');
        var seg = document.getElementById('seg-plast');
        if(!svg) return;
        var tipo = 'termo', fase = 0;   /* 0 frio · 1 calentado · 2 resultado */

        function cadenas(x, y, enredado, quemado){
          var m = '', col = quemado ? '#5b3a16' : (enredado ? '#9aa0a6' : 'var(--goo-azul)');
          for(var i = 0; i < 5; i++){
            var yy = y + i*17;
            if(enredado){
              m += '<path d="M'+x+' '+yy+' q18 -12 34 0 q16 12 34 0 q18 -12 34 0 q16 12 34 0" fill="none" '
                 + 'stroke="'+col+'" stroke-width="4" stroke-linecap="round"></path>';
            } else {
              m += '<path d="M'+x+' '+yy+' h136" fill="none" stroke="'+col+'" stroke-width="4" stroke-linecap="round"></path>';
            }
          }
          /* los enlaces cruzados del termoestable */
          if(tipo === 'estable'){
            for(var j = 0; j < 4; j++){
              for(var k = 0; k < 3; k++){
                var xx = x + 25 + k*45;
                m += '<path d="M'+xx+' '+(y+j*17)+' V'+(y+(j+1)*17)+'" stroke="var(--goo-rojo)" stroke-width="3"></path>';
              }
            }
          }
          return m;
        }

        function pinta(){
          var m = '';
          m += '<text x="40" y="30" class="rotulo-svg" style="font-size:11px">ANTES</text>';
          m += cadenas(40, 60, false, false);
          m += '<text x="250" y="30" text-anchor="middle" class="rotulo-svg" style="font-size:11px">CALOR</text>';
          /* mechero */
          m += '<path d="M250 70 q-14 -18 0 -34 q14 16 0 34 Z" fill="'+(fase?'#fbbc04':'var(--line)')+'"></path>';
          if(fase) m += '<path d="M250 62 q-7 -10 0 -18 q7 10 0 18 Z" fill="#ea4335"></path>';
          m += '<path d="M244 72 h12 v46 h-12 Z" fill="var(--ink-soft)"></path>';
          m += '<path d="M215 140 H285" stroke="var(--line)" stroke-width="2"></path>';

          m += '<text x="420" y="30" class="rotulo-svg" style="font-size:11px">DESPU&Eacute;S</text>';
          if(fase === 0){
            m += '<text x="490" y="105" text-anchor="middle" class="rotulo-svg" style="font-size:12px;opacity:.5">'
               + 'pulsa el mechero</text>';
          } else if(tipo === 'termo'){
            m += cadenas(420, 60, true, false);
          } else {
            m += cadenas(420, 60, false, true);
            m += '<path d="M470 52 q-9 -14 0 -24 q9 12 0 24 Z" fill="#9aa0a6" opacity=".7"></path>';
            m += '<path d="M500 48 q-7 -11 0 -19 q7 10 0 19 Z" fill="#9aa0a6" opacity=".5"></path>';
          }

          m += '<text x="320" y="200" text-anchor="middle" class="rotulo-svg" style="font-size:10.5px">'
             + (tipo === 'termo' ? 'CADENAS SUELTAS, SE PUEDEN DESLIZAR'
                                 : 'CADENAS UNIDAS ENTRE S&Iacute; &middot; LOS PUENTES ROJOS NO SE DESHACEN') + '</text>';
          svg.innerHTML = m;

          if(fase === 0){
            pie.innerHTML = tipo === 'termo'
              ? 'Las cadenas de un <b>termopl&aacute;stico</b> est&aacute;n sueltas, apiladas como espaguetis cocidos. '
                + 'Pulsa el mechero.'
              : 'Un <b>termoestable</b> tiene las cadenas <b>cosidas entre s&iacute;</b> por enlaces qu&iacute;micos, '
                + 'los puentes rojos. Pulsa el mechero.';
          } else if(tipo === 'termo'){
            pie.innerHTML = '<b>Se ablanda y se puede remoldear.</b> Con calor las cadenas deslizan unas sobre '
              + 'otras, y al enfriarse quedan en la nueva forma. Esto se puede repetir muchas veces: por eso '
              + 'un termopl&aacute;stico <b>se recicla</b>.';
          } else {
            pie.innerHTML = '<b>No se ablanda: se quema.</b> Los puentes entre cadenas no se deshacen con el '
              + 'calor, as&iacute; que antes de fundirse el material se descompone. Un termoestable <b>no se puede '
              + 'reciclar</b> fundi&eacute;ndolo: como mucho se tritura y se usa de relleno.';
          }
        }
        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-p]'); if(!b) return;
          seg.querySelectorAll('button').forEach(function(x){ x.setAttribute('aria-pressed', x===b?'true':'false'); });
          tipo = b.dataset.p; fase = 0; pinta();
        });
        svg.addEventListener('click', function(){ fase = fase ? 0 : 1; pinta(); });
        pinta();
      })();
      </script>

      <div class="copiar">
        <h4>Los pl&aacute;sticos</h4>
        <p><b>Pol&iacute;mero</b>: mol&eacute;cula muy larga formada por la repetici&oacute;n de una unidad peque&ntilde;a,
           el <b>mon&oacute;mero</b>.</p>
        <p><b>Termopl&aacute;sticos</b>: cadenas sueltas. Con calor se ablandan y se pueden remoldear muchas
           veces. <b>Se reciclan.</b> PET, PE, PP, PVC, PS.</p>
        <p><b>Termoestables</b>: cadenas unidas entre s&iacute; por enlaces. Con calor <b>se queman sin
           ablandarse</b>. No se reciclan fundi&eacute;ndolos. Baquelita, resinas ep&oacute;xi, poliuretano.</p>
        <p><b>Elast&oacute;meros</b>: cadenas poco unidas y muy enrolladas. Se estiran mucho y recuperan la
           forma. Caucho, goma, silicona.</p>
      </div>

      <h3>El tri&aacute;ngulo de la base</h3>
      <p>Casi todo envase lleva un tri&aacute;ngulo con un n&uacute;mero del 1 al 7. No es decoraci&oacute;n: dice
         <b>de qu&eacute; pl&aacute;stico est&aacute; hecho</b>, y por tanto si se puede reciclar y con qu&eacute;.</p>
      <div class="copiar">
        <h4>C&oacute;digos que conviene reconocer</h4>
        <ul>
          <li><b>1 · PET</b> &mdash; botellas de agua y refresco. Se recicla muy bien.</li>
          <li><b>2 · HDPE</b> &mdash; garrafas, botes de detergente. Se recicla bien.</li>
          <li><b>3 · PVC</b> &mdash; tuber&iacute;as, marcos. Dif&iacute;cil y problem&aacute;tico.</li>
          <li><b>4 · LDPE</b> &mdash; bolsas y film. Se recicla mal por lo fino.</li>
          <li><b>5 · PP</b> &mdash; t&aacute;pers, tapones. Aguanta el microondas.</li>
          <li><b>6 · PS</b> &mdash; porex, bandejas. Voluminoso y poco rentable.</li>
          <li><b>7 · Otros</b> &mdash; caj&oacute;n de sastre. Casi nunca se recicla.</li>
        </ul>
      </div>
      <div class="nota">
        <span class="n-tag">Lo que casi nadie sabe</span>
        <b>El tri&aacute;ngulo no significa que se recicle.</b> Significa de qu&eacute; material es. Un 6 y un 7 llevan
        tri&aacute;ngulo y acaban casi siempre incinerados o en vertedero. El s&iacute;mbolo informa; no promete.
      </div>
""") +
  bloque('02', u'Pr&aacute;ctica &middot; 25 min', ficha(
    u'Actividad 7 &middot; Leer los tri&aacute;ngulos',
    [u'1.2', u'7.1'], u'Parejas &middot; 25 min', u"""
          <h4>Qu&eacute; hay que hacer</h4>
          <ol class="pasos">
            <li>Reunid <b>seis envases o piezas de pl&aacute;stico</b> y buscad el tri&aacute;ngulo con su n&uacute;mero.
                Suele estar en la base, muy peque&ntilde;o.</li>
            <li>Anotad el n&uacute;mero, el nombre del pl&aacute;stico y para qu&eacute; sirve ese objeto.</li>
            <li>Decid si cada uno es <b>termopl&aacute;stico o termoestable</b>, y en qu&eacute; os bas&aacute;is.</li>
            <li>Para cada uno: <b>&iquest;por qu&eacute; ese pl&aacute;stico y no otro?</b> Pensad en si va al microondas,
                si aguanta golpes, si tiene que ser transparente.</li>
            <li>Buscad uno que, en vuestra opini&oacute;n, <b>no deber&iacute;a ser de pl&aacute;stico</b>. Argumentadlo.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Los seis tri&aacute;ngulos est&aacute;n localizados y anotados <b>(3 puntos)</b>.</li>
            <li>La clasificaci&oacute;n termopl&aacute;stico/termoestable es correcta <b>(2 puntos)</b>.</li>
            <li>Las razones de uso son t&eacute;cnicas <b>(3 puntos)</b>.</li>
            <li>La cr&iacute;tica final est&aacute; argumentada <b>(2 puntos)</b>.</li>
          </ul>
          <div class="nota" style="margin-top:14px">
            <span class="n-tag">Si no encontr&aacute;is el tri&aacute;ngulo</span>
            Eso tambi&eacute;n es un dato, y de los buenos: <b>un envase sin marcar es un envase que nadie
            podr&aacute; separar</b>. Anotadlo como tal.
          </div>
  """)) +
  bloque('03', u'Cierre &middot; 5 min', u"""
      <p>Los pl&aacute;sticos se inventaron para <b>no tener que matar elefantes</b>. Hoy son el s&iacute;mbolo del
         problema ambiental. Las dos cosas son verdad a la vez.</p>
      <p>Esa es probablemente la lecci&oacute;n m&aacute;s importante del tema: <b>ninguna tecnolog&iacute;a nace buena
         ni mala</b>. Nace resolviendo un problema, y al resolverlo crea el siguiente.</p>
      <ol>
      """ + pregunta(u'&iquest;Qu&eacute; diferencia hay entre un termopl&aacute;stico y un termoestable?',
                     u'<p>Las cadenas. En el <b>termopl&aacute;stico</b> est&aacute;n sueltas y con calor deslizan: se remoldea y se recicla. En el <b>termoestable</b> est&aacute;n unidas por enlaces que el calor no deshace: se quema antes de ablandarse.</p>')
        + pregunta(u'&iquest;Qu&eacute; significa exactamente el tri&aacute;ngulo con un n&uacute;mero?',
                   u'<p>Dice <b>de qu&eacute; pl&aacute;stico est&aacute; hecho</b>, nada m&aacute;s. <b>No garantiza que se recicle</b>: un 6 o un 7 lo llevan y casi siempre acaban incinerados.</p>')
        + pregunta(u'Los pl&aacute;sticos se inventaron para sustituir al marfil. &iquest;Qu&eacute; ense&ntilde;a eso?',
                   u'<p>Que una tecnolog&iacute;a puede resolver un problema grave &mdash;la caza de elefantes&mdash; y crear otro distinto d&eacute;cadas despu&eacute;s. Hay que juzgarlas por sus <b>consecuencias completas</b>, no por su intenci&oacute;n.</p>') + u"""
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Elegir un material por sus propiedades es media decisi&oacute;n. Falta la otra mitad: <b>qu&eacute; pasa con &eacute;l
        cuando el objeto se tira</b>. Y el test del tema.
      </div>
  """))))

S.append(dict(
 corto=u'Impacto y test', titulo=u'Qu&eacute; pasa cuando lo tiras',
 entradilla=u'Elegir un material no termina en sus propiedades. La otra mitad de la decisi&oacute;n es qu&eacute; ocurre con &eacute;l despu&eacute;s.',
 minutado=[(u"10'", u'Reto'), (u"20'", u'Teor&iacute;a'), (u"15'", u'Pr&aacute;ctica'), (u"15'", u'Test')],
 chips=[u'CE7 &middot; 7.1', u'CE7 &middot; 7.2', u'A.7', u'E.1', u'E.2'],
 cuerpo=(
  bloque('00', u'Reto inicial &middot; 10 min', u"""
      <p>Una pregunta que parece de otra asignatura y no lo es:</p>
      <div class="aviso">
        <span class="n-tag">La pregunta</span>
        <b>&iquest;D&oacute;nde est&aacute; ahora la botella de agua que te bebiste el mes pasado?</b>
      </div>
      <p>Existe. No ha desaparecido. Est&aacute; en alg&uacute;n sitio concreto, ahora mismo, y lo m&aacute;s probable es
         que siga existiendo cuando t&uacute; tengas cincuenta a&ntilde;os.</p>
      <p>Durante todo este tema hemos elegido materiales mirando lo que saben hacer. Falta la otra mitad
         de la decisi&oacute;n: <b>qu&eacute; pasa con ellos despu&eacute;s</b>.</p>
""") +
  bloque('01', u'Teor&iacute;a &middot; 20 min', u"""
      <h3>El objeto no termina cuando lo tiras</h3>

      <div class="escena" id="esc-ciclo">
        <div class="escena-barra">
          <span class="escena-titulo">El ciclo de vida de una botella &middot; pulsa cada fase</span>
          <div class="seg" id="seg-ciclo">
            <button type="button" data-c="lineal" aria-pressed="true">Modelo lineal</button>
            <button type="button" data-c="circular">Modelo circular</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 240" id="svg-ciclo" role="img"
               aria-label="Ciclo de vida lineal frente a circular de una botella"></svg>
        </div>
        <div class="pie" id="pie-ciclo"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-ciclo');
        var pie = document.getElementById('pie-ciclo');
        var seg = document.getElementById('seg-ciclo');
        if(!svg) return;
        var modo = 'lineal', sel = -1;

        var F = [
          {n:'Extraer',  d:'Se saca <b>petróleo</b>. Una botella de litro y medio necesita unos 100 ml de crudo.'},
          {n:'Fabricar', d:'Se convierte en PET y se moldea. Aqu&iacute; se gasta la mayor parte de la energ&iacute;a.'},
          {n:'Transportar', d:'De la f&aacute;brica al embotellador, de ah&iacute; al supermercado y de ah&iacute; a tu casa.'},
          {n:'Usar',     d:'Tiempo medio de uso de una botella de agua: <b>unos minutos</b>.'},
          {n:'Tirar',    d:'Y aqu&iacute; se decide todo: contenedor amarillo, o no.'}
        ];

        function pinta(){
          var m = '', X = 40, W = 118, Y = 70;
          F.forEach(function(f, i){
            var x = X + i*W;
            var act = (sel === i);
            var col = act ? 'var(--goo-azul)' : 'var(--line)';
            m += '<g class="fase" data-i="'+i+'" style="cursor:pointer">';
            m += '<rect x="'+x+'" y="'+Y+'" width="96" height="46" rx="3" fill="'+(act?'var(--accent-soft)':'var(--surface)')
               + '" stroke="'+col+'" stroke-width="'+(act?3:1.5)+'"></rect>';
            m += '<text x="'+(x+48)+'" y="'+(Y+28)+'" text-anchor="middle" class="rotulo-svg" '
               + 'style="font-size:12px;fill:var(--ink)">'+f.n+'</text>';
            m += '</g>';
            if(i < 4){
              m += '<path d="M'+(x+96)+' '+(Y+23)+' h16" stroke="var(--ink-soft)" stroke-width="2"></path>';
              m += '<path d="M'+(x+118)+' '+(Y+23)+' l-9 -5 v10 Z" fill="var(--ink-soft)"></path>';
            }
          });

          if(modo === 'lineal'){
            m += '<path d="M'+(X+4*W+96)+' '+(Y+23)+' h40" stroke="var(--goo-rojo)" stroke-width="2.5"></path>';
            m += '<path d="M'+(X+4*W+142)+' '+(Y+23)+' l-10 -6 v12 Z" fill="var(--goo-rojo)"></path>';
            m += '<text x="'+(X+4*W+108)+'" y="'+(Y+58)+'" text-anchor="middle" class="rotulo-svg" '
               + 'style="font-size:11px;fill:var(--goo-rojo)">VERTEDERO</text>';
          } else {
            m += '<path d="M'+(X+4*W+48)+' '+(Y+50)+' V190 H'+(X+48)+' V'+(Y+50)+'" fill="none" '
               + 'stroke="var(--goo-verde)" stroke-width="2.5" stroke-dasharray="7 5"></path>';
            m += '<path d="M'+(X+48)+' '+(Y+50)+' l-6 12 h12 Z" fill="var(--goo-verde)"></path>';
            m += '<text x="320" y="208" text-anchor="middle" class="rotulo-svg" '
               + 'style="font-size:11.5px;fill:var(--goo-verde)">RECICLAR &middot; vuelve a ser materia prima</text>';
          }
          m += '<text x="40" y="36" class="rotulo-svg" style="font-size:11px">UNA BOTELLA DE AGUA, DE PRINCIPIO A FIN</text>';
          svg.innerHTML = m;

          if(sel >= 0) pie.innerHTML = '<b>'+F[sel].n+'.</b> '+F[sel].d;
          else if(modo === 'lineal')
            pie.innerHTML = 'El modelo <b>lineal</b>: extraer, fabricar, usar y tirar. Funcion&oacute; mientras '
              + 'los recursos parec&iacute;an infinitos y la basura, invisible. Pulsa cada fase.';
          else
            pie.innerHTML = 'El modelo <b>circular</b>: lo que se tira vuelve a entrar como materia prima. '
              + 'No es reciclar por gusto: es que <b>extraer y fabricar desde cero sale car&iacute;simo</b>, y ah&iacute; se gasta la mayor parte de la energ&iacute;a.';
        }
        svg.addEventListener('click', function(e){
          var g = e.target.closest('.fase'); if(!g) return;
          sel = (sel === +g.dataset.i) ? -1 : +g.dataset.i; pinta();
        });
        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-c]'); if(!b) return;
          seg.querySelectorAll('button').forEach(function(x){ x.setAttribute('aria-pressed', x===b?'true':'false'); });
          modo = b.dataset.c; sel = -1; pinta();
        });
        pinta();
      })();
      </script>

      <div class="copiar">
        <h4>Ciclo de vida</h4>
        <p><b>Ciclo de vida</b>: todas las etapas por las que pasa un producto, desde que se extrae la
           materia prima hasta que se convierte en residuo o vuelve a ser materia prima.</p>
        <p><b>Modelo lineal</b>: extraer, fabricar, usar, tirar. <b>Modelo circular</b>: lo que se tira
           vuelve a entrar como materia prima.</p>
        <p><b>Huella de carbono</b>: cantidad de CO&#8322; que se emite a lo largo de todo ese ciclo.</p>
      </div>

      <h3>Las tres erres, en el orden correcto</h3>
      <div class="copiar">
        <h4>Reducir, reutilizar, reciclar</h4>
        <ol class="pasos">
          <li><b>Reducir</b>: no usarlo. Es la &uacute;nica que ahorra el 100&nbsp;por cien.</li>
          <li><b>Reutilizar</b>: usarlo otra vez tal cual, sin transformarlo.</li>
          <li><b>Reciclar</b>: destruirlo para recuperar el material.</li>
        </ol>
        <p><b>El orden importa</b>, y casi siempre se cuenta al rev&eacute;s. Reciclar es la &uacute;ltima, no la
           primera: sigue gastando energ&iacute;a y transporte.</p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Hay un t&eacute;rmino que conviene conocer: <b>obsolescencia programada</b>, dise&ntilde;ar algo para que
           dure poco. El caso documentado m&aacute;s claro es el <b>c&aacute;rtel Phoebus</b>: en 1924 los grandes
           fabricantes de bombillas acordaron por escrito limitar su duraci&oacute;n a 1.000 horas, cuando ya
           fabricaban algunas de 2.500. Multaban al que se pasara.</p>
        <p>Existe una bombilla encendida desde 1901 en un parque de bomberos de California. La han visto
           millones de personas por internet. No es un milagro: es que se fabric&oacute; antes del acuerdo.</p>
      </div>
""") +
  bloque('02', u'Pr&aacute;ctica &middot; 15 min', ficha(
    u'Actividad 8 &middot; El juicio a un objeto',
    [u'7.1', u'7.2'], u'Grupos de cuatro &middot; 15 min', u"""
          <h4>Qu&eacute; hay que hacer</h4>
          <p>Elegid un objeto cotidiano: una botella de agua, un boli, unos auriculares, un m&oacute;vil.</p>
          <ol class="pasos">
            <li>Reconstruid su <b>ciclo de vida completo</b>, las cinco fases &mdash;extraer, fabricar, transportar, usar y tirar&mdash;, con todo el detalle que pod&aacute;is.</li>
            <li>Se&ntilde;alad en qu&eacute; fase se gasta <b>m&aacute;s energ&iacute;a</b> y en cu&aacute;l se genera m&aacute;s residuo.</li>
            <li>Proponed <b>una mejora por cada erre</b>: una para reducir, una para reutilizar y una para reciclar.</li>
            <li>Decid cu&aacute;l de las tres tendr&iacute;a <b>m&aacute;s efecto</b> y por qu&eacute;.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>El ciclo de vida est&aacute; completo y es realista <b>(3 puntos)</b>.</li>
            <li>La fase cr&iacute;tica est&aacute; bien identificada <b>(2 puntos)</b>.</li>
            <li>Hay una mejora por cada erre y son aplicables <b>(3 puntos)</b>.</li>
            <li>La conclusi&oacute;n razona cu&aacute;l tiene m&aacute;s efecto <b>(2 puntos)</b>.</li>
          </ul>
  """)) +
  bloque('03', u'Test del tema &middot; 15 min', u"""
      <p>Diez preguntas de todo el tema. Contesta primero en el cuaderno y luego despliega cada una.</p>
      <ol>
      """ + pregunta(u'&iquest;Cu&aacute;l es el mejor material?',
                     u'<p><b>Ninguno.</b> No existe. Existe el <b>adecuado</b> para lo que quieres hacer, y se encuentra comparando propiedades con lo que necesitas.</p>')
        + pregunta(u'&iquest;Por qu&eacute; el precio no es una propiedad?',
                   u'<p>Porque no es una caracter&iacute;stica del material: es <b>consecuencia</b> de su abundancia, de lo que cueste extraerlo y de c&oacute;mo se fabrique.</p>')
        + pregunta(u'&iquest;Qu&eacute; es un ensayo?',
                   u'<p>Una prueba <b>normalizada</b> para medir una propiedad, hecha siempre igual para que el resultado no dependa de qui&eacute;n la haga.</p>')
        + pregunta(u'&iquest;Qu&eacute; significa que la madera sea anis&oacute;tropa?',
                   u'<p>Que <b>sus propiedades cambian seg&uacute;n la direcci&oacute;n</b>: mucho a lo largo de la veta, poco a lo ancho.</p>')
        + pregunta(u'&iquest;Qu&eacute; problema resuelve el contrachapado?',
                   u'<p>La anisotrop&iacute;a. Cruzando la veta de cada capa 90 grados, <b>ninguna direcci&oacute;n queda d&eacute;bil</b>.</p>')
        + pregunta(u'&iquest;C&oacute;mo distingues un metal f&eacute;rrico de uno que no lo es?',
                   u'<p>Con un <b>im&aacute;n</b>. Si se pega, lleva hierro. Con la excepci&oacute;n del acero inoxidable, que lo lleva y no se pega.</p>')
        + pregunta(u'&iquest;Por qu&eacute; reciclar aluminio ahorra tant&iacute;sima energ&iacute;a?',
                   u'<p>Porque lo caro es <b>separarlo del mineral por electrolisis</b>, y eso ya se hizo. Reciclar solo exige fundirlo.</p>')
        + pregunta(u'Termopl&aacute;stico y termoestable: la diferencia, y su consecuencia.',
                   u'<p>El primero tiene las cadenas sueltas y con calor se remoldea, as&iacute; que <b>se recicla</b>. El segundo las tiene unidas por enlaces y se quema antes de ablandarse: <b>no se recicla</b> fundi&eacute;ndolo.</p>')
        + pregunta(u'Ordena las tres erres de m&aacute;s a menos eficaz y explica el orden.',
                   u'<p><b>Reducir, reutilizar, reciclar.</b> Reducir es la &uacute;nica que ahorra todo; reutilizar no transforma nada; reciclar todav&iacute;a gasta energ&iacute;a y transporte.</p>')
        + pregunta(u'&iquest;Es la tecnolog&iacute;a buena o mala para el medio ambiente? Razona.',
                   u'<p>Ni una cosa ni otra. El pl&aacute;stico se invent&oacute; para <b>dejar de matar elefantes</b> y hoy es un problema ambiental. Una tecnolog&iacute;a resuelve un problema y al hacerlo crea el siguiente: hay que juzgarla por sus <b>consecuencias completas</b>.</p>') + u"""
      </ol>
      <div class="nota">
        <span class="n-tag">Tema terminado</span>
        Sabes qu&eacute; construir, c&oacute;mo dibujarlo y <b>de qu&eacute; hacerlo</b>. Lo siguiente es mirar de cerca
        cada familia de materiales, empezando por la m&aacute;s antigua: <b>la madera</b>.
      </div>

      <figure class="foto">
        <img src="../../../img/u3-reciclaje.jpg" width="1200" height="900" loading="lazy"
             alt="Trabajadores con uniforme azul separando residuos a mano en una cinta transportadora de una planta de reciclaje">
        <figcaption>El s&iacute;mbolo del tri&aacute;ngulo no recicla nada: <b>esto</b> es reciclar. Una cinta, y gente separando a mano lo que nosotros tiramos junto. Cada vez que un envase va al contenedor equivocado, alguien lo saca de aqu&iacute; &mdash; o no lo saca, y entonces el lote entero pierde valor.
          <br><br>Foto de <b>CP Khanal</b> en Pexels. Es de su autor y no forma parte del material
          publicado bajo la licencia de esta p&aacute;gina.</figcaption>
      </figure>
  """))))


CFG = dict(
 ruta='2eso/TyD/tema3/',
 migas=u'<a href="../../../">Materiales</a> &middot; <a href="../../">2.&ordm; ESO</a> &middot; <a href="../">TyD</a> &middot; Tema 3',
 h1=u'Materiales de uso t&eacute;cnico',
 titulo=u'Tema 3 &middot; Materiales de uso t&eacute;cnico',
 tema=u'Tema 3', curso=u'2.&ordm; de ESO', materia=u'Tecnolog&iacute;a y Digitalizaci&oacute;n',
 desc=u'Tema 3 de Tecnolog&iacute;a y Digitalizaci&oacute;n de 2.&ordm; de ESO: propiedades de los materiales, c&oacute;mo se eligen y qu&eacute; impacto ambiental tienen.',
 sesiones=S)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(os.path.join(BASE, '2eso/TyD/tema3'), exist_ok=True)
html = pagina(CFG)
io.open(os.path.join(BASE, '2eso/TyD/tema3/index.html'), 'w', encoding='utf-8', newline='').write(html)
print('U3 generada: %d bytes, %d sesiones (%d escritas)' % (
    len(html), len(S), sum(1 for x in S if not x.get('pendiente'))))
