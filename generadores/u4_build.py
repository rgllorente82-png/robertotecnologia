# -*- coding: utf-8 -*-
"""2.o TyD · U4 · Estructuras."""
import io, os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from unidad_base import pagina, bloque, ficha, pregunta
from avatar_flat import componente

ENV = json.load(io.open('_env_u4.json', encoding='utf-8'))

NARRADOR = componente(
    idc='narr-u4',
    titulo=u'Por qu&eacute; aguanta una estructura',
    quien=u'La idea que organiza todo el tema, en medio minuto',
    mp3='../../../audio/u4-estructuras.mp3',
    envolvente=ENV,
    nota=u'Audio propio, generado con voz neuronal. La boca sigue el volumen real de la voz.')

VIDEO = u'''
      <div class="escena">
        <div class="escena-barra"><span class="escena-titulo">El tri&aacute;ngulo y el cuadrado, en movimiento</span></div>
        <div class="lienzo" style="padding:0">
          <video controls preload="metadata" style="width:100%;height:auto;display:block"
                 poster="../../../video/triangulacion.jpg">
            <source src="../../../video/triangulacion.mp4" type="video/mp4">
            Tu navegador no puede reproducir v&iacute;deo.
            <a href="../../../video/triangulacion.mp4">Desc&aacute;rgalo aqu&iacute;</a>.
          </video>
        </div>
        <div class="pie">F&iacute;jate en una cosa mientras lo ves: <b>ninguna barra cambia de longitud</b>.
          Lo &uacute;nico que se mueve son los &aacute;ngulos. Y aun as&iacute;, el cuadrado se desploma y el tri&aacute;ngulo no.
          <br><br>V&iacute;deo propio, hecho con manim, con voz propia. Es material de la web, bajo la misma licencia. Las dos fotos del final proceden de Wikimedia Commons: torre de alta tensi&oacute;n de <i>HighVoltage 5576</i> (CC0) y &laquo;Paris, Eiffelturm 2014&raquo; de <i>Dietmar Rabich</i> (<a href="https://creativecommons.org/licenses/by-sa/4.0/deed.es">CC BY-SA 4.0</a>).</div>
      </div>
'''

ESCENA = u'''
      <div class="escena" id="esc-esf">
        <div class="escena-barra">
          <span class="escena-titulo">Los cinco esfuerzos &middot; pulsa uno</span>
          <div class="seg" id="seg-esf">
            <button type="button" data-e="0" aria-pressed="true">Tracci&oacute;n</button>
            <button type="button" data-e="1">Compresi&oacute;n</button>
            <button type="button" data-e="2">Flexi&oacute;n</button>
            <button type="button" data-e="3">Torsi&oacute;n</button>
            <button type="button" data-e="4">Cortadura</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 210" id="svg-esf" role="img"
               aria-label="Los cinco esfuerzos: traccion, compresion, flexion, torsion y cortadura"></svg>
        </div>
        <div class="pie" id="pie-esf"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-esf');
        var pie = document.getElementById('pie-esf');
        var seg = document.getElementById('seg-esf');
        if(!svg) return;
        var sel = 0;

        var E = [
          {n:'Tracci&oacute;n',  d:'Dos fuerzas tiran en sentidos opuestos y <b>alargan</b> la pieza. '
            + 'La cuerda de un columpio, el cable de una gr&uacute;a. El acero aguanta muy bien; el hormig&oacute;n, fatal.'},
          {n:'Compresi&oacute;n', d:'Las fuerzas aprietan y tienden a <b>acortar</b> la pieza. Las patas de una silla, '
            + 'un pilar. Ojo: si es larga y delgada no se aplasta, <b>se dobla de golpe</b>. Eso es el pandeo.'},
          {n:'Flexi&oacute;n',    d:'La fuerza llega perpendicular y la pieza <b>se curva</b>. Una estanter&iacute;a con libros. '
            + 'Al curvarse, arriba se comprime y abajo se estira: la flexi&oacute;n es las dos cosas a la vez.'},
          {n:'Torsi&oacute;n',    d:'Dos fuerzas la hacen <b>girar sobre su eje</b>. Escurrir un trapo, girar una llave. '
            + 'Es el m&aacute;s traicionero: muchas estructuras se calculan pensando solo en cargas verticales.'},
          {n:'Cortadura',  d:'Dos fuerzas pr&oacute;ximas y opuestas tienden a <b>cortar</b> la pieza, como unas tijeras. '
            + 'As&iacute; trabajan tornillos y remaches. Por eso un tornillo mal elegido no se dobla: se secciona.'}
        ];

        function flecha(x1,y1,x2,y2,col){
          var dx=x2-x1, dy=y2-y1, L=Math.hypot(dx,dy), ux=dx/L, uy=dy/L;
          var bx=x2-ux*11, by=y2-uy*11, nx=-uy, ny=ux;
          return '<path d="M'+x1+' '+y1+' L'+bx.toFixed(1)+' '+by.toFixed(1)+'" stroke="'+col+'" stroke-width="3.5" stroke-linecap="round"></path>'
               + '<path d="M'+x2+' '+y2+' L'+(bx+nx*5).toFixed(1)+' '+(by+ny*5).toFixed(1)
               + ' L'+(bx-nx*5).toFixed(1)+' '+(by-ny*5).toFixed(1)+' Z" fill="'+col+'"></path>';
        }

        function pinta(){
          var m = '', R='var(--goo-rojo)', A='var(--goo-azul)', X=190, Y=95, W=260, H=34;
          if(sel === 0){        /* traccion: la pieza se alarga */
            m += '<rect x="'+(X-14)+'" y="'+Y+'" width="'+(W+28)+'" height="'+H+'" rx="3" fill="var(--accent-soft)" stroke="'+A+'" stroke-width="2.5"></rect>';
            m += flecha(X-30, Y+H/2, X-90, Y+H/2, R) + flecha(X+W+30, Y+H/2, X+W+90, Y+H/2, R);
          } else if(sel === 1){ /* compresion: mas corta y ancha */
            m += '<rect x="'+(X+16)+'" y="'+(Y-6)+'" width="'+(W-32)+'" height="'+(H+12)+'" rx="3" fill="var(--accent-soft)" stroke="'+A+'" stroke-width="2.5"></rect>';
            m += flecha(X-70, Y+H/2, X+8, Y+H/2, R) + flecha(X+W+70, Y+H/2, X+W-8, Y+H/2, R);
          } else if(sel === 2){ /* flexion: curvada */
            m += '<path d="M'+X+' '+Y+' q130 46 '+W+' 0 v'+H+' q-130 46 -'+W+' 0 Z" fill="var(--accent-soft)" stroke="'+A+'" stroke-width="2.5"></path>';
            m += flecha(X+W/2, Y-52, X+W/2, Y+22, R);
            m += '<path d="M'+(X-6)+' '+(Y+H+6)+' h18 M'+(X+W-12)+' '+(Y+H+6)+' h18" stroke="var(--ink-soft)" stroke-width="5"></path>';
            m += '<text x="'+(X+W/2)+'" y="'+(Y-60)+'" text-anchor="middle" class="rotulo-svg" style="font-size:10px">carga</text>';
            m += '<text x="'+(X+40)+'" y="'+(Y+14)+'" class="rotulo-svg" style="font-size:9.5px">se comprime</text>';
            m += '<text x="'+(X+40)+'" y="'+(Y+H+28)+'" class="rotulo-svg" style="font-size:9.5px">se estira</text>';
          } else if(sel === 3){ /* torsion: secciones giradas */
            m += '<rect x="'+X+'" y="'+Y+'" width="'+W+'" height="'+H+'" rx="3" fill="var(--accent-soft)" stroke="'+A+'" stroke-width="2.5"></rect>';
            for(var k=1;k<6;k++){
              var xx = X + k*W/6, inc = (k-3)*5;
              m += '<path d="M'+xx+' '+(Y+inc)+' L'+xx+' '+(Y+H+inc)+'" stroke="'+A+'" stroke-width="1.6" opacity=".7"></path>';
            }
            m += '<path d="M'+(X-52)+' '+(Y+H/2)+' a26 26 0 1 1 8 18" fill="none" stroke="'+R+'" stroke-width="3.5"></path>';
            m += '<path d="M'+(X-44)+' '+(Y+H/2+18)+' l10 -3 l-2 11 Z" fill="'+R+'"></path>';
            m += '<path d="M'+(X+W+52)+' '+(Y+H/2)+' a26 26 0 1 0 -8 18" fill="none" stroke="'+R+'" stroke-width="3.5"></path>';
            m += '<path d="M'+(X+W+44)+' '+(Y+H/2+18)+' l-10 -3 l2 11 Z" fill="'+R+'"></path>';
          } else {              /* cortadura: dos mitades desplazadas */
            m += '<rect x="'+X+'" y="'+(Y-7)+'" width="'+(W/2)+'" height="'+H+'" rx="3" fill="var(--accent-soft)" stroke="'+A+'" stroke-width="2.5"></rect>';
            m += '<rect x="'+(X+W/2)+'" y="'+(Y+7)+'" width="'+(W/2)+'" height="'+H+'" rx="3" fill="var(--accent-soft)" stroke="'+A+'" stroke-width="2.5"></rect>';
            m += '<path d="M'+(X+W/2)+' '+(Y-20)+' V'+(Y+H+20)+'" stroke="'+R+'" stroke-width="1.5" stroke-dasharray="5 4"></path>';
            m += flecha(X+40, Y-26, X+W/2-14, Y-26, R) + flecha(X+W-40, Y+H+26, X+W/2+14, Y+H+26, R);
          }
          svg.innerHTML = m;
          pie.innerHTML = '<b>'+E[sel].n+'.</b> '+E[sel].d;
        }
        seg.addEventListener('click', function(e){
          var b=e.target.closest('button[data-e]'); if(!b) return;
          seg.querySelectorAll('button').forEach(function(x){x.setAttribute('aria-pressed', x===b?'true':'false');});
          sel=+b.dataset.e; pinta();
        });
        pinta();
      })();
      </script>
'''

C = u'''
      <p>Mira el edificio m&aacute;s alto que se vea desde la ventana. Ahora piensa en un temporal de los de
         verdad.</p>
      <div class="aviso">
        <span class="n-tag">El dato</span>
        El viento empuja la fachada de un rascacielos con una fuerza que equivale a <b>varias toneladas
        empujando de lado</b>. Y el edificio no vuelca: como mucho, su punta se balancea unos cent&iacute;metros.
      </div>
      <p><b>&iquest;Por qu&eacute; no se cae?</b> Cont&eacute;stalo por escrito antes de seguir.</p>
      <p>La respuesta habitual es «porque es muy fuerte» o «porque tiene mucho hormig&oacute;n». Y no es eso:
         hay torres el&eacute;ctricas que est&aacute;n <b>casi huecas</b>, pesan una fracci&oacute;n de lo que parece, y aguantan
         vendavales a&ntilde;o tras a&ntilde;o.</p>
'''

T = u'''
      <h3>No aguanta porque sea fuerte: aguanta porque reparte</h3>
''' + NARRADOR + u'''
      <p>Cuando una fuerza llega a una estructura, <b>no se queda donde llega</b>. Cada pieza se la pasa a
         la siguiente y la conduce hasta el suelo. Y seg&uacute;n c&oacute;mo est&eacute; colocada, cada pieza sufre un tipo
         distinto de esfuerzo.</p>
''' + ESCENA + u'''
      <div class="copiar">
        <h4>Los cinco esfuerzos</h4>
        <ul>
          <li><b>Tracci&oacute;n</b>: la alargan.</li>
          <li><b>Compresi&oacute;n</b>: la acortan o aplastan. Si es larga y delgada, <b>pandea</b>.</li>
          <li><b>Flexi&oacute;n</b>: la curvan. Es compresi&oacute;n arriba y tracci&oacute;n abajo a la vez.</li>
          <li><b>Torsi&oacute;n</b>: la retuercen sobre su eje.</li>
          <li><b>Cortadura</b>: tienden a cortarla, como unas tijeras.</li>
        </ul>
        <p><b>Estructura</b>: conjunto de elementos que soporta las cargas de un objeto y las conduce
           hasta el suelo sin romperse ni deformarse demasiado.</p>
      </div>

      <h3>El truco que lo cambia todo: triangular</h3>
''' + VIDEO + u'''
      <div class="copiar">
        <h4>Triangulaci&oacute;n</h4>
        <p><b>El tri&aacute;ngulo es la &uacute;nica figura indeformable</b> con barras articuladas: fijados los tres
           lados, los tres &aacute;ngulos quedan determinados y no hay otra forma posible.</p>
        <p><b>Triangular</b> una estructura es dividirla en tri&aacute;ngulos con barras diagonales, llamadas
           <b>tirantes</b> o <b>riostras</b>. Es lo que ves en las torres el&eacute;ctricas, las gr&uacute;as, las cerchas
           de los tejados y la Torre Eiffel.</p>
      </div>

      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; no hace falta copiarlo</span>
        <p>Que la torsi&oacute;n no es un detalle menor lo demostr&oacute; el <b>puente de Tacoma Narrows</b>. Se abri&oacute;
           al tr&aacute;fico el 1 de julio de 1940, con un vano central de 853 metros y un tablero estrecho
           rigidizado con vigas macizas en lugar de celos&iacute;as trianguladas.</p>
        <p>El 7 de noviembre de ese mismo a&ntilde;o, con un viento de unos <b>68 km/h</b> &mdash;una ventolera de
           oto&ntilde;o, nada excepcional&mdash;, el tablero entr&oacute; en oscilaci&oacute;n de torsi&oacute;n, se retorci&oacute; durante
           m&aacute;s de una hora y se hundi&oacute;. No hubo v&iacute;ctimas humanas.</p>
        <p>El puente estaba calculado para vientos muy superiores. <b>El fallo estuvo en la forma, no en
           la fuerza.</b> El que se construy&oacute; en su lugar cambi&oacute; aquellas vigas macizas por celos&iacute;as
           trianguladas abiertas, que dejan pasar el aire. Sigue en servicio.</p>
      </div>
'''

S1 = (
  bloque('00', u'Reto inicial &middot; 10 min', C) +
  bloque('01', u'Teor&iacute;a &middot; 25 min', T) +
  bloque('02', u'Pr&aacute;ctica &middot; 20 min', ficha(
    u'Actividad 9 &middot; La torre de papel',
    [u'2.1', u'3.1'], u'Grupos de tres &middot; 20 min', u'''
          <h4>Qu&eacute; hay que hacer</h4>
          <p>Material: <b>cinco folios y 50 cm de cinta</b>. Nada m&aacute;s.</p>
          <ol class="pasos">
            <li>Construid la torre <b>m&aacute;s alta posible</b> que aguante un libro de texto encima durante
                un minuto.</li>
            <li>Antes de empezar, dibujad el dise&ntilde;o y <b>se&ntilde;alad qu&eacute; esfuerzo</b> sufre cada pieza.</li>
            <li>Al terminar, medid la altura y anotad <b>por d&oacute;nde ha fallado</b> si ha fallado.</li>
            <li>Si se ha doblado una pieza vertical, decid si fue por aplastamiento o por <b>pandeo</b>.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>El dise&ntilde;o previo est&aacute; dibujado y con los esfuerzos se&ntilde;alados <b>(3 puntos)</b>.</li>
            <li>La torre aguanta el libro <b>(2 puntos)</b>.</li>
            <li>Hay triangulaci&oacute;n y se justifica d&oacute;nde y por qu&eacute; <b>(3 puntos)</b>.</li>
            <li>El an&aacute;lisis del fallo es correcto <b>(2 puntos)</b>.</li>
          </ul>
          <div class="nota" style="margin-top:14px">
            <span class="n-tag">Pista que casi nadie usa</span>
            Un folio plano no aguanta nada de pie. <b>Enrollado en tubo, aguanta much&iacute;simo.</b> La
            resistencia no depende solo del material: depende tambi&eacute;n de la <b>forma de la secci&oacute;n</b>.
          </div>
  ''')) +
  bloque('03', u'Cierre &middot; 5 min', u'''
      <p>Vuelve al rascacielos. Ya puedes contestar sin decir «porque es fuerte»: no vuelca porque el
         empuje del viento <b>se reparte</b> entre todas sus piezas y baja hasta el suelo, y porque su
         estructura est&aacute; pensada para que ninguna pieza reciba m&aacute;s de lo que puede.</p>
      <ol>
      ''' + pregunta(u'&iquest;Por qu&eacute; el tri&aacute;ngulo es indeformable y el cuadrado no?',
                     u'<p>Porque fijados los tres lados de un tri&aacute;ngulo, <b>los tres &aacute;ngulos quedan determinados</b>. Un cuadrado, en cambio, se desploma en rombo sin que sus lados cambien de longitud.</p>')
        + pregunta(u'&iquest;Qu&eacute; es el pandeo y en qu&eacute; esfuerzo aparece?',
                   u'<p>Aparece en <b>compresi&oacute;n</b>. Una pieza larga y delgada comprimida no se aplasta: <b>se dobla de golpe</b> hacia un lado. Por eso los pilares altos son gruesos.</p>')
        + pregunta(u'La flexi&oacute;n es en realidad dos esfuerzos a la vez. &iquest;Cu&aacute;les?',
                   u'<p><b>Compresi&oacute;n</b> en la cara que se acorta y <b>tracci&oacute;n</b> en la que se estira. Por eso una viga de hormig&oacute;n lleva las barras de acero abajo: es donde se estira, y el hormig&oacute;n no aguanta tracci&oacute;n.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya sabes que aguante. Pero una estructura que aguanta no hace nada: est&aacute; quieta. Lo siguiente es
        conseguir que <b>algo se mueva</b>, y eso son los mecanismos.
      </div>
  '''))

S = [dict(corto=u'&iquest;Por qu&eacute; no se cae?', titulo=u'Por qu&eacute; no se cae: los cinco esfuerzos',
          entradilla=u'Una estructura no aguanta porque sea fuerte. Aguanta porque reparte.',
          minutado=[(u"10'", u'Reto'), (u"25'", u'Teor&iacute;a'), (u"20'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')],
          chips=[u'CE2 &middot; 2.1', u'CE3 &middot; 3.1', u'A.4', u'A.5'],
          cuerpo=S1)]
for c in [u'Tipos de estructura', u'Perfiles y secciones', u'Estabilidad', u'Construir', u'Proyecto y test']:
    S.append(dict(corto=c, pendiente=True))

CFG = dict(
 ruta='2eso/TyD/tema4/',
 migas=u'<a href="../../../">Materiales</a> &middot; <a href="../../">2.&ordm; ESO</a> &middot; <a href="../">TyD</a> &middot; Tema 4',
 h1=u'Estructuras',
 titulo=u'Tema 4 &middot; Estructuras',
 tema=u'Tema 4', curso=u'2.&ordm; de ESO', materia=u'Tecnolog&iacute;a y Digitalizaci&oacute;n',
 desc=u'Tema 4 de Tecnolog&iacute;a y Digitalizaci&oacute;n de 2.&ordm; de ESO: los cinco esfuerzos, la triangulaci&oacute;n y por qu&eacute; una estructura aguanta.',
 sesiones=S)

BASE = "C:/Users/javie/AppData/Local/Temp/rt-clone"
os.makedirs(os.path.join(BASE, '2eso/TyD/tema4'), exist_ok=True)
html = pagina(CFG)
io.open(os.path.join(BASE, '2eso/TyD/tema4/index.html'), 'w', encoding='utf-8', newline='').write(html)
print('U4 generada: %d bytes, %d sesiones (%d escritas)' % (
    len(html), len(S), sum(1 for x in S if not x.get('pendiente'))))
