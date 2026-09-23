# -*- coding: utf-8 -*-
"""2.o TyD - U4 - Sesion 5: construir.

La sesion junta las cuatro anteriores en un encargo con material tasado, y
trae la escena mas seria de la unidad: un banco donde el alumno pone y quita
diagonales y la pagina le dice si la estructura AGUANTA o si es un mecanismo.

Y no lo dice contando barras. Monta la matriz de la estructura -una fila por
barra con su vector unitario, mas las filas de los apoyos- y calcula su rango
por eliminacion gaussiana. Si el rango no llega a 2 x numero de nudos, la
estructura tiene movimiento, y ademas se saca el vector del nucleo y se anima:
el alumno VE por donde se mueve.

Eso permite ensenar algo que con la cuenta sola no se puede: que se puede
tener el numero justo de barras y moverse igual, si estan mal repartidas.
"""
from unidad_base import bloque, ficha, pregunta

# --------------------------------------------------------------------------
# 00 - Reto
# --------------------------------------------------------------------------
RETO = u'''
      <p>Hasta ahora has analizado estructuras que ya estaban hechas. Hoy te toca al rev&eacute;s.</p>
      <div class="aviso">
        <span class="n-tag">El encargo</span>
        Construir un <b>puente de 40 cm de luz</b> que aguante el mayor peso posible, con
        <b>20 palillos de brocheta, 1 metro de cinta de carrocero y cola blanca</b>. Nada m&aacute;s.
        El puente no puede apoyarse en nada que no sean los dos bordes.
      </div>
      <p>Y la nota no es el peso que aguante. Es <b>esto</b>:</p>
      <div class="def">
        <b>puntuaci&oacute;n = peso que aguanta &divide; peso del puente</b>
      </div>
      <p>Con esa regla, hacerlo m&aacute;s gordo <b>no ayuda</b>: sube el numerador, pero tambi&eacute;n el
         denominador. Gana quien coloque el material donde trabaja, que es exactamente lo que llevas
         cuatro sesiones viendo.</p>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Esta forma de puntuar no es un invento para complicar: es la que se usa de verdad. En un
           puente real, <b>la mayor parte de lo que aguanta se la come su propio peso</b>. Cuanto
           m&aacute;s largo es, peor: un puente de 1.000 metros se sostiene a s&iacute; mismo a duras penas, y
           por eso los grandes son colgantes, que es la familia m&aacute;s ligera.</p>
      </div>
'''

# --------------------------------------------------------------------------
# 01 - Diseno, con el banco de triangulacion
# --------------------------------------------------------------------------
ESCENA = u'''
      <div class="escena" id="esc-tri">
        <div class="escena-barra">
          <span class="escena-titulo">Pon diagonales &middot; pulsa en cada cuadro</span>
          <div class="seg" id="seg-tri">
            <button type="button" data-t="vacia">Quitar todas</button>
            <button type="button" data-t="tres">Poner tres</button>
            <button type="button" data-t="trampa">La trampa</button>
            <button type="button" data-t="bien">Bien triangulada</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 700 320" id="svg-tri" role="img"
               aria-label="Celos&iacute;a de cuatro cuadros en la que se ponen y quitan diagonales"></svg>
        </div>
        <div class="pie" id="pie-tri"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-tri');
        var pie = document.getElementById('pie-tri');
        var seg = document.getElementById('seg-tri');
        if(!svg) return;

        var AZ='var(--goo-azul)', RO='var(--goo-rojo)', VE='var(--goo-verde)',
            GR='var(--ink-soft)', TI='var(--ink)';
        var P = 4, ANCHO = 92, ALTO = 92, X0 = 150, Y0 = 232;

        /* nudos: 0..4 abajo, 5..9 arriba */
        var N = [];
        for(var k = 0; k <= P; k++) N.push({x: X0 + k*ANCHO, y: Y0});
        for(k = 0; k <= P; k++) N.push({x: X0 + k*ANCHO, y: Y0 - ALTO});
        var NN = N.length;

        /* diag[k]: 0 ninguna, 1 "/", 2 "\\\\", 3 las dos */
        var diag = [0,0,0,0], t = 0, raf = null;

        function barras(){
          var B = [];
          for(var k = 0; k < P; k++){
            B.push([k, k+1]);                 /* cordon de abajo */
            B.push([P+1+k, P+2+k]);           /* cordon de arriba */
          }
          for(k = 0; k <= P; k++) B.push([k, P+1+k]);   /* montantes */
          for(k = 0; k < P; k++){
            if(diag[k] & 1) B.push([k, P+2+k]);         /* de abajo-izq a arriba-der */
            if(diag[k] & 2) B.push([k+1, P+1+k]);       /* de abajo-der a arriba-izq */
          }
          return B;
        }

        /* --- el analisis de verdad: rango de la matriz de la estructura --- */
        function analiza(B){
          var cols = 2*NN, M = [];
          B.forEach(function(b){
            var a = N[b[0]], c = N[b[1]];
            var dx = c.x - a.x, dy = c.y - a.y, L = Math.hypot(dx, dy);
            var f = new Array(cols).fill(0);
            f[2*b[0]] = dx/L; f[2*b[0]+1] = dy/L;
            f[2*b[1]] = -dx/L; f[2*b[1]+1] = -dy/L;
            M.push(f);
          });
          /* apoyos: el nudo 0 fijo (dos direcciones) y el nudo P sobre rodillo */
          var s1 = new Array(cols).fill(0); s1[0] = 1; M.push(s1);
          var s2 = new Array(cols).fill(0); s2[1] = 1; M.push(s2);
          var s3 = new Array(cols).fill(0); s3[2*P+1] = 1; M.push(s3);

          /* eliminacion gaussiana con pivote parcial */
          var piv = [], fila = 0;
          for(var col = 0; col < cols && fila < M.length; col++){
            var mejor = fila, may = Math.abs(M[fila][col]);
            for(var r = fila+1; r < M.length; r++){
              if(Math.abs(M[r][col]) > may){ may = Math.abs(M[r][col]); mejor = r; }
            }
            if(may < 1e-9) continue;
            var tmp = M[fila]; M[fila] = M[mejor]; M[mejor] = tmp;
            var p = M[fila][col];
            for(var c2 = 0; c2 < cols; c2++) M[fila][c2] /= p;
            for(r = 0; r < M.length; r++){
              if(r === fila) continue;
              var f2 = M[r][col];
              if(Math.abs(f2) < 1e-12) continue;
              for(c2 = 0; c2 < cols; c2++) M[r][c2] -= f2*M[fila][c2];
            }
            piv.push(col); fila++;
          }
          var rango = piv.length;

          /* si le falta rango, hay movimiento: sacamos uno del nucleo */
          var v = null;
          if(rango < cols){
            var libre = -1;
            for(col = 0; col < cols; col++) if(piv.indexOf(col) < 0){ libre = col; break; }
            v = new Array(cols).fill(0); v[libre] = 1;
            for(var i = 0; i < rango; i++) v[piv[i]] = -M[i][libre];
            var norma = Math.max.apply(null, v.map(Math.abs)) || 1;
            v = v.map(function(x){ return x/norma; });
          }
          return {rango: rango, cols: cols, v: v, nb: B.length};
        }

        function pinta(){
          var B = barras(), A = analiza(B);
          var mecanismo = A.rango < A.cols;
          var amp = mecanismo ? 16*Math.sin(t) : 0;
          var Q = N.map(function(n, i){
            return A.v ? {x: n.x + amp*A.v[2*i], y: n.y + amp*A.v[2*i+1]} : {x:n.x, y:n.y};
          });

          var col = mecanismo ? RO : VE;
          var m = '<style>.et{font:12.5px var(--f-m)}.eg{font:11px var(--f-m);letter-spacing:.1em}</style>';

          /* el suelo y los apoyos */
          m += '<path d="M' + (X0-70) + ' ' + (Y0+26) + ' H' + (X0+P*ANCHO+70)
             + '" stroke="' + GR + '" stroke-width="2"></path>';

          B.forEach(function(b){
            m += '<path d="M' + Q[b[0]].x.toFixed(1) + ' ' + Q[b[0]].y.toFixed(1) + ' L'
               + Q[b[1]].x.toFixed(1) + ' ' + Q[b[1]].y.toFixed(1) + '" stroke="' + col
               + '" stroke-width="5" stroke-linecap="round"></path>';
          });
          Q.forEach(function(n){
            m += '<circle cx="' + n.x.toFixed(1) + '" cy="' + n.y.toFixed(1)
               + '" r="5" fill="' + TI + '"></circle>';
          });
          /* apoyos */
          m += '<path d="M' + Q[0].x.toFixed(1) + ' ' + (Q[0].y+5).toFixed(1) + ' l-11 21 h22 Z" '
             + 'fill="none" stroke="' + TI + '" stroke-width="2"></path>';
          m += '<path d="M' + Q[P].x.toFixed(1) + ' ' + (Q[P].y+5).toFixed(1) + ' l-11 21 h22 Z" '
             + 'fill="none" stroke="' + TI + '" stroke-width="2"></path>';
          m += '<circle cx="' + (Q[P].x-6).toFixed(1) + '" cy="' + (Q[P].y+29).toFixed(1)
             + '" r="4" fill="none" stroke="' + TI + '" stroke-width="1.6"></circle>';
          m += '<circle cx="' + (Q[P].x+6).toFixed(1) + '" cy="' + (Q[P].y+29).toFixed(1)
             + '" r="4" fill="none" stroke="' + TI + '" stroke-width="1.6"></circle>';

          /* los botones invisibles de cada cuadro */
          for(var k = 0; k < P; k++){
            m += '<rect x="' + (X0 + k*ANCHO + 14) + '" y="' + (Y0 - ALTO + 14) + '" width="'
               + (ANCHO-28) + '" height="' + (ALTO-28) + '" fill="transparent" '
               + 'style="cursor:pointer" data-cuadro="' + k + '"></rect>';
            if(!diag[k]){
              m += '<text x="' + (X0 + k*ANCHO + ANCHO/2) + '" y="' + (Y0 - ALTO/2 + 5)
                 + '" text-anchor="middle" class="et" fill="' + GR + '" style="pointer-events:none">pulsa</text>';
            }
          }

          /* el veredicto, y la cuenta al lado para poder compararlos */
          var cuenta = A.nb + 3;
          m += '<text x="560" y="40" class="eg" fill="' + GR + '">LA CUENTA</text>';
          m += '<text x="560" y="62" class="et" fill="' + TI + '">barras: ' + A.nb + '</text>';
          m += '<text x="560" y="80" class="et" fill="' + TI + '">+ apoyos: 3</text>';
          m += '<text x="560" y="98" class="et" fill="' + TI + '">total ' + cuenta + '</text>';
          m += '<text x="560" y="116" class="et" fill="' + GR + '">hacen falta ' + A.cols + '</text>';
          m += '<text x="560" y="148" class="eg" fill="' + GR + '">LA REALIDAD</text>';
          m += '<text x="560" y="170" class="et" fill="' + col + '">'
             + (mecanismo ? 'SE MUEVE' : 'AGUANTA') + '</text>';
          m += '<text x="560" y="190" class="et" fill="' + GR + '">rango ' + A.rango
             + ' de ' + A.cols + '</text>';

          svg.innerHTML = m;

          var texto;
          if(!mecanismo){
            texto = '<b>Aguanta.</b> Cada cuadro tiene su diagonal, as&iacute; que no queda ni un solo '
                  + 'cuadril&aacute;tero suelto. La estructura ya no puede cambiar de forma sin que alguna '
                  + 'barra cambie de longitud.';
          } else if(cuenta >= A.cols){
            texto = '<b>Se mueve, y la cuenta sal&iacute;a bien.</b> Tienes barras de sobra, pero est&aacute;n '
                  + 'mal repartidas: hay un cuadro con dos diagonales, que no hac&iacute;an falta, y otro '
                  + 'sin ninguna, que es por donde se dobla. <b>Contar barras no basta</b>: hay que '
                  + 'mirar d&oacute;nde est&aacute;n.';
          } else {
            texto = '<b>Se mueve.</b> Queda al menos un cuadril&aacute;tero sin diagonal, y un '
                  + 'cuadril&aacute;tero articulado se desploma en rombo sin estirar ning&uacute;n lado. '
                  + 'M&iacute;ralo: la animaci&oacute;n va exactamente por donde la estructura cede.';
          }
          pie.innerHTML = texto;
        }

        svg.addEventListener('click', function(e){
          var r = e.target.closest('[data-cuadro]'); if(!r) return;
          var k = +r.dataset.cuadro;
          diag[k] = (diag[k] + 1) % 4;
          pinta();
        });
        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-t]'); if(!b) return;
          seg.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          var v = b.dataset.t;
          if(v === 'vacia')  diag = [0,0,0,0];
          if(v === 'tres')   diag = [1,1,1,0];
          if(v === 'trampa') diag = [3,1,1,0];
          if(v === 'bien')   diag = [1,2,1,2];
          pinta();
        });

        function cuadro(){ t += 0.05; pinta(); raf = requestAnimationFrame(cuadro); }
        raf = requestAnimationFrame(cuadro);
      })();
      </script>
'''

TEORIA = u'''
      <p>Antes de gastar un solo folio, hay cuatro decisiones que ya sabes tomar. Son las cuatro
         sesiones de este tema, en orden:</p>
      <div class="copiar">
        <h4>Lista de comprobaci&oacute;n antes de construir</h4>
        <ol>
          <li><b>&iquest;Qu&eacute; familia?</b> Con palillos que trabajan bien a compresi&oacute;n y a
              tracci&oacute;n, y con uniones que giran, la respuesta casi siempre es
              <b>triangulada</b>.</li>
          <li><b>&iquest;Est&aacute; todo triangulado?</b> Ni un solo cuadril&aacute;tero suelto.</li>
          <li><b>&iquest;Qu&eacute; secci&oacute;n?</b> Un palillo solo pandea; dos pegados en L o tres en
              tri&aacute;ngulo aguantan mucho m&aacute;s con poco m&aacute;s de peso.</li>
          <li><b>&iquest;Se vuelca?</b> Un puente estrecho se tumba de lado. Hace falta
              <b>arriostrarlo</b>: unir las dos caras con barras transversales.</li>
        </ol>
      </div>
      <p>La segunda es la que m&aacute;s se falla, y es la que puedes probar aqu&iacute; mismo. Pulsa dentro de
         cada cuadro para ir poniendo y quitando diagonales.</p>
''' + ESCENA + u'''
      <div class="copiar">
        <h4>Contar barras no basta</h4>
        <p>Para que una celos&iacute;a plana sea r&iacute;gida hace falta que el n&uacute;mero de barras m&aacute;s los
           apoyos llegue al doble del n&uacute;mero de nudos. Pero eso es solo <b>condici&oacute;n
           necesaria</b>: si las barras est&aacute;n mal repartidas, la cuenta sale y la estructura se
           mueve igual.</p>
        <p>La comprobaci&oacute;n que s&iacute; vale es directa: <b>busca cuadril&aacute;teros sin diagonal</b>.
           Si hay uno, hay movimiento.</p>
      </div>

      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Cuando la escena dice que se mueve, no lo est&aacute; adivinando ni lo lleva escrito. Monta la
           <b>matriz de la estructura</b> &mdash;una fila por barra, con la direcci&oacute;n en la que tira
           de sus dos nudos&mdash; y calcula cu&aacute;ntas de esas filas son independientes. Si faltan,
           existe un movimiento posible, y la animaci&oacute;n que ves es <b>ese</b> movimiento, calculado,
           no dibujado a mano.</p>
        <p>Es exactamente lo que hace un programa de c&aacute;lculo de estructuras antes de empezar: mirar
           si lo que le has dado es una estructura o un mecanismo.</p>
      </div>
'''

# --------------------------------------------------------------------------
# 02 - Practica
# --------------------------------------------------------------------------
PRACTICA = ficha(
    u'Actividad 13 &middot; El puente de 40 cent&iacute;metros',
    [u'2.1', u'3.1', u'A.4', u'A.5'], u'Grupos de tres &middot; 20 min hoy + la siguiente sesi&oacute;n',
    u'''
          <h4>Material, tasado</h4>
          <p>Por grupo: <b>20 palillos de brocheta, 1 m de cinta de carrocero, cola blanca</b>.
             No se puede usar nada m&aacute;s. Los palillos se pueden cortar.</p>
          <h4>Hoy: dise&ntilde;o (20 min)</h4>
          <ol class="pasos">
            <li>Dibujad el puente <b>a tama&ntilde;o real</b> sobre un folio A3 o dos A4 pegados: 40 cm
                de luz. Ese dibujo es la plantilla sobre la que luego pegar&eacute;is.</li>
            <li>Marcad <b>todos los nudos</b> y comprobad, uno a uno, que no queda ning&uacute;n
                cuadril&aacute;tero sin diagonal.</li>
            <li>Contad los palillos que os pide vuestro dise&ntilde;o. Si pasan de 20, hay que
                simplificar: <b>quitad de donde menos trabaje</b>, nunca las diagonales.</li>
            <li>Decidid c&oacute;mo lo vais a <b>arriostrar</b> para que no se tumbe de lado.</li>
            <li>Escribid una <b>predicci&oacute;n</b>: cu&aacute;ntos gramos creeis que aguantar&aacute; y
                <b>por d&oacute;nde va a romper</b>. Esto se entrega ahora y no se puede cambiar.</li>
          </ol>
          <div class="nota">
            <span class="n-tag">Consejo que vale la nota</span>
            El puente se cuelga de la carga por el centro del cord&oacute;n inferior. El cord&oacute;n
            <b>superior</b> va comprimido y es el que <b>pandea</b>: ah&iacute; es donde compensa doblar
            palillos, y no en el resto.
          </div>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>El dise&ntilde;o a tama&ntilde;o real, con los nudos marcados <b>(2 puntos)</b>.</li>
            <li>No queda ning&uacute;n cuadril&aacute;tero sin triangular <b>(3 puntos)</b>.</li>
            <li>La predicci&oacute;n est&aacute; hecha y razonada, acierte o no <b>(2 puntos)</b>.</li>
            <li>Rendimiento en el ensayo: <b>peso aguantado / peso del puente</b> <b>(3 puntos)</b>.</li>
          </ul>
''')

# --------------------------------------------------------------------------
# 03 - Cierre
# --------------------------------------------------------------------------
CIERRE = u'''
      <p>El d&iacute;a del ensayo se cuelga una bolsa del centro del puente y se van echando pesas hasta
         que rompe. Antes de eso, dos cosas que hay que tener claras.</p>
      <ol>
      ''' + pregunta(
          u'&iquest;Por qu&eacute; la nota es el peso aguantado dividido por el peso del puente?',
          u'<p>Porque si no, ganar&iacute;a siempre el m&aacute;s pesado, y hacer algo pesado no tiene ning&uacute;n '
          u'm&eacute;rito. Dividiendo, se premia <b>colocar bien el material</b>, que es el problema de '
          u'verdad: en un puente grande, casi todo lo que aguanta se lo come su propio peso.</p>') + pregunta(
          u'Si la cuenta de barras sale bien, &iquest;seguro que aguanta?',
          u'<p><b>No.</b> La cuenta es necesaria pero no suficiente: se puede tener el n&uacute;mero justo '
          u'de barras con dos diagonales en un cuadro y ninguna en otro, y entonces se mueve. Hay que '
          u'<b>mirar cuadro por cuadro</b>.</p>') + pregunta(
          u'&iquest;Por d&oacute;nde suele romper un puente de palillos, y por qu&eacute;?',
          u'<p>Por el <b>cord&oacute;n superior</b>, cerca del centro, y casi nunca por rotura: por '
          u'<b>pandeo</b>. Es la pieza m&aacute;s comprimida y m&aacute;s larga, y una pieza larga y delgada '
          u'comprimida se dobla de golpe antes de aplastarse.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Se construye, se ensaya hasta romper y se compara con la predicci&oacute;n. Y se cierra el tema
        con un test para ver qu&eacute; ha quedado.
      </div>
'''

S5 = (bloque('00', u'Reto inicial &middot; 10 min', RETO) +
      bloque('01', u'Dise&ntilde;o &middot; 25 min', TEORIA) +
      bloque('02', u'Pr&aacute;ctica &middot; 20 min', PRACTICA) +
      bloque('03', u'Cierre &middot; 5 min', CIERRE))
