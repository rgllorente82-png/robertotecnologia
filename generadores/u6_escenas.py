# -*- coding: utf-8 -*-
"""Las tres escenas interactivas de la U6, en SVG y JavaScript a mano.

Van aparte del texto porque son largas y porque la simbologia se comparte: las
tres dibujan con la misma biblioteca de simbolos (window.U6), que sigue la
norma IEC 60617 / UNE-EN 60617, la que se usa en Europa. Ojo con el detalle que
mas se equivoca: la resistencia es un RECTANGULO, no el zigzag americano.

Ninguna de estas cadenas pasa por formateo %% de Python: se concatenan tal cual,
asi que los % literales del JavaScript estan a salvo.
"""

# --------------------------------------------------------------------------
# Biblioteca de simbolos. Se emite una sola vez en la pagina.
# --------------------------------------------------------------------------
SIMBOLOS = u'''
      <script>
      /* Simbologia normalizada (IEC 60617). Todas las medidas estan en
         unidades del viewBox y se calculan, no se ponen a ojo: el aspa de la
         lampara toca la circunferencia a 45 grados exactos, las celdas de la
         pila se reparten con paso constante y el brazo del interruptor abre
         30 grados sobre la horizontal.                                      */
      window.U6 = (function(){
        var INK = 'var(--ink)', SUP = 'var(--surface)';

        function cable(x1, y1, x2, y2, col, gr){
          return '<path d="M' + x1 + ' ' + y1 + ' L' + x2 + ' ' + y2 + '" fill="none" stroke="'
               + col + '" stroke-width="' + (gr || 2.4) + '" stroke-linecap="round"></path>';
        }
        function trazo(d, col, gr, guion){
          return '<path d="' + d + '" fill="none" stroke="' + col + '" stroke-width="' + (gr || 2.4)
               + '" stroke-linecap="round" stroke-linejoin="round"'
               + (guion ? ' stroke-dasharray="7 6"' : '') + '></path>';
        }
        function nodo(x, y, col){
          return '<circle cx="' + x + '" cy="' + y + '" r="3.6" fill="' + (col || INK) + '"></circle>';
        }
        function texto(x, y, t, extra){
          return '<text x="' + x + '" y="' + y + '" class="rotulo-svg"'
               + (extra || '') + '>' + t + '</text>';
        }

        /* Pila / bateria, en vertical y con el + arriba. Una celda = una barra
           larga (positivo) y una barra corta y gruesa (negativo). Paso 22.
           Devuelve tambien los dos bornes, para que la escena tire el cable.  */
        function pila(cx, cy, celdas, col){
          var paso = 22, h = (celdas - 1) * paso + 11, y0 = cy - h / 2, m = '';
          for(var i = 0; i < celdas; i++){
            var yl = y0 + i * paso, ys = yl + 11;
            m += cable(cx - 18, yl, cx + 18, yl, col, 2.2);   /* barra larga: + */
            m += cable(cx - 9,  ys, cx + 9,  ys, col, 5);     /* barra corta: - */
          }
          m += texto(cx + 24, y0 + 5, '+');
          m += texto(cx + 24, y0 + h + 5, '\\u2212');
          return {svg: m, mas: y0, menos: y0 + h};
        }

        /* Lampara. Circulo con aspa; el aspa toca el circulo a 45 grados, o
           sea a r/raiz(2) del centro en las dos direcciones.                 */
        function lampara(cx, cy, r, col, brillo){
          var k = r * Math.SQRT1_2, m = '';
          /* Encendida, el aspa se dibuja oscura pase lo que pase: sobre el
             amarillo, la tinta clara del modo oscuro no se lee.             */
          if(brillo > 0.45) col = '#202124';
          if(brillo > 0){
            m += '<circle cx="' + cx + '" cy="' + cy + '" r="' + (r * 2).toFixed(1)
               + '" fill="var(--goo-amarillo)" opacity="' + (0.45 * brillo).toFixed(3) + '"></circle>';
          }
          m += '<circle cx="' + cx + '" cy="' + cy + '" r="' + r + '" fill="'
             + (brillo > 0 ? 'var(--goo-amarillo)' : SUP) + '" fill-opacity="'
             + (brillo > 0 ? (0.06 + 0.94 * brillo).toFixed(3) : '1')
             + '" stroke="' + col + '" stroke-width="2.4"></circle>';
          m += trazo('M' + (cx - k).toFixed(2) + ' ' + (cy - k).toFixed(2)
                   + ' L' + (cx + k).toFixed(2) + ' ' + (cy + k).toFixed(2)
                   + ' M' + (cx - k).toFixed(2) + ' ' + (cy + k).toFixed(2)
                   + ' L' + (cx + k).toFixed(2) + ' ' + (cy - k).toFixed(2), col, 2.4);
          return m;
        }

        /* Resistencia: rectangulo 56 x 22, sin relleno. NO es el zigzag: el
           zigzag es la norma americana y aqui no se usa.                     */
        function resistencia(cx, cy, col, vertical){
          var w = vertical ? 22 : 56, h = vertical ? 56 : 22;
          return '<rect x="' + (cx - w / 2) + '" y="' + (cy - h / 2) + '" width="' + w
               + '" height="' + h + '" fill="' + SUP + '" stroke="' + col
               + '" stroke-width="2.4"></rect>';
        }

        /* Interruptor horizontal. Cerrado: recto entre los dos contactos.
           Abierto: el brazo sube 30 grados, con la misma longitud.           */
        function interruptor(x1, x2, y, cerrado, col){
          var L = x2 - x1, m = nodo(x1, y, col) + nodo(x2, y, col);
          if(cerrado) m += cable(x1, y, x2, y, col, 2.4);
          else m += cable(x1, y, x1 + L * Math.cos(Math.PI / 6), y - L * Math.sin(Math.PI / 6), col, 2.4);
          return m;
        }

        /* Pulsador normalmente abierto: como el interruptor, pero con el boton
           encima. Al soltarlo vuelve solo, y por eso se dibuja abierto.      */
        function pulsador(x1, x2, y, col){
          var xm = (x1 + x2) / 2;
          var m = nodo(x1, y, col) + nodo(x2, y, col);
          m += cable(x1, y, x2, y - 12, col, 2.4);
          m += cable(xm, y - 6, xm, y - 24, col, 2);
          m += cable(xm - 9, y - 24, xm + 9, y - 24, col, 2.8);
          return m;
        }

        /* Diodo LED: triangulo contra la barra, en el sentido en que deja
           pasar, y las dos flechas de la luz que sale.                       */
        function led(cx, cy, col){
          var m = '<path d="M' + (cx - 11) + ' ' + (cy - 11) + ' L' + (cx - 11) + ' ' + (cy + 11)
                + ' L' + (cx + 11) + ' ' + cy + ' Z" fill="' + SUP + '" stroke="' + col
                + '" stroke-width="2.2" stroke-linejoin="round"></path>';
          m += cable(cx + 11, cy - 11, cx + 11, cy + 11, col, 2.8);
          /* Las dos flechas de la luz, a 45 grados hacia arriba y a la
             derecha. La punta se dibuja con dos barbas a 25 grados del
             trazo, calculadas, para que apunten de verdad adonde apuntan.  */
          var ang = -Math.PI / 4, L = 12, B = 6, ab = 25 * Math.PI / 180;
          for(var i = 0; i < 2; i++){
            var x0 = cx - 7 + i * 12, y0 = cy - 15;
            var x1 = x0 + L * Math.cos(ang), y1 = y0 + L * Math.sin(ang);
            m += cable(x0, y0, x1, y1, col, 1.8);
            m += cable(x1, y1, x1 + B * Math.cos(ang + Math.PI - ab),
                               y1 + B * Math.sin(ang + Math.PI - ab), col, 1.8);
            m += cable(x1, y1, x1 + B * Math.cos(ang + Math.PI + ab),
                               y1 + B * Math.sin(ang + Math.PI + ab), col, 1.8);
          }
          return m;
        }

        /* Aparato de medida o motor: circulo con la letra dentro. */
        function medidor(cx, cy, letra, col){
          return '<circle cx="' + cx + '" cy="' + cy + '" r="14" fill="' + SUP + '" stroke="'
               + col + '" stroke-width="2.2"></circle>'
               + '<text x="' + cx + '" y="' + (cy + 5) + '" text-anchor="middle" class="rotulo-svg"'
               + ' style="font-size:13px;fill:' + col + '">' + letra + '</text>';
        }

        return {cable: cable, trazo: trazo, nodo: nodo, texto: texto, pila: pila,
                lampara: lampara, resistencia: resistencia, interruptor: interruptor,
                pulsador: pulsador, led: led, medidor: medidor};
      })();
      </script>
'''


# --------------------------------------------------------------------------
# Lamina de simbologia. No es interactiva: es la chuleta que se copia.
# --------------------------------------------------------------------------
TABLA_SIMBOLOS = u'''
      <div class="escena" id="esc-simb">
        <div class="escena-barra">
          <span class="escena-titulo">Simbolog&iacute;a normalizada &middot; IEC 60617 (la que se usa en Europa)</span>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 300" id="svg-simb" role="img"
               aria-label="L&aacute;mina con los diez s&iacute;mbolos normalizados que se usan en el tema"></svg>
        </div>
        <div class="pie">Dibujar &laquo;una bombillita&raquo; en vez del c&iacute;rculo con el aspa no es un
          capricho de notaci&oacute;n: el s&iacute;mbolo est&aacute; normalizado para que un esquema tuyo lo entienda
          alguien que no hable tu idioma. <b>Copia esta l&aacute;mina en la libreta</b>: la vas a usar el
          resto del tema.</div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-simb');
        if(!svg || !window.U6) return;
        var S = window.U6, INK = 'var(--ink)';

        /* Dos columnas de cinco filas. El simbolo se centra en cx y el rotulo
           empieza 46 px mas a la derecha, igual en las diez celdas.          */
        var COL = [40, 350], FIL = [42, 92, 142, 192, 242], m = '';

        var celda = [
          ['Conductor', function(x, y){ return S.cable(x - 26, y, x + 26, y, INK, 2.4); }],
          ['Uni\\u00f3n de conductores', function(x, y){
              return S.cable(x - 26, y, x + 26, y, INK, 2.4) + S.cable(x, y - 18, x, y + 18, INK, 2.4)
                   + S.nodo(x, y, INK); }],
          ['Cruce SIN uni\\u00f3n', function(x, y){
              return S.cable(x - 26, y, x + 26, y, INK, 2.4) + S.cable(x, y - 18, x, y + 18, INK, 2.4); }],
          /* La pila en horizontal, que es como se dibuja en un esquema de
             linea. Dos celdas: barra larga (+) y barra corta y gruesa (-).  */
          ['Pila o bater\\u00eda', function(x, y){
              var m2 = S.cable(x - 34, y, x - 11, y, INK, 2.4);
              m2 += S.cable(x - 11, y - 16, x - 11, y + 16, INK, 2.2);
              m2 += S.cable(x - 2,  y - 8,  x - 2,  y + 8,  INK, 5);
              m2 += S.cable(x + 7,  y - 16, x + 7,  y + 16, INK, 2.2);
              m2 += S.cable(x + 16, y - 8,  x + 16, y + 8,  INK, 5);
              m2 += S.cable(x + 16, y, x + 34, y, INK, 2.4);
              m2 += S.texto(x - 15, y - 21, '+', ' text-anchor="middle" style="font-size:13px"');
              return m2; }],
          ['Interruptor', function(x, y){
              return S.cable(x - 30, y, x - 15, y, INK, 2.4) + S.interruptor(x - 15, x + 15, y, false, INK)
                   + S.cable(x + 15, y, x + 30, y, INK, 2.4); }],
          ['Pulsador', function(x, y){
              return S.cable(x - 30, y, x - 15, y, INK, 2.4) + S.pulsador(x - 15, x + 15, y, INK)
                   + S.cable(x + 15, y, x + 30, y, INK, 2.4); }],
          ['L\\u00e1mpara', function(x, y){
              return S.cable(x - 30, y, x - 15, y, INK, 2.4) + S.lampara(x, y, 15, INK, 0)
                   + S.cable(x + 15, y, x + 30, y, INK, 2.4); }],
          ['Resistencia', function(x, y){
              return S.cable(x - 30, y, x - 24, y, INK, 2.4) + S.resistencia(x, y, INK, false)
                   + S.cable(x + 24, y, x + 30, y, INK, 2.4); }],
          ['Motor', function(x, y){
              return S.cable(x - 30, y, x - 14, y, INK, 2.4) + S.medidor(x, y, 'M', INK)
                   + S.cable(x + 14, y, x + 30, y, INK, 2.4); }],
          ['Diodo LED', function(x, y){
              return S.cable(x - 30, y, x - 11, y, INK, 2.4) + S.led(x, y, INK)
                   + S.cable(x + 11, y, x + 30, y, INK, 2.4); }]
        ];

        for(var i = 0; i < celda.length; i++){
          var x = COL[Math.floor(i / 5)], y = FIL[i % 5];
          m += celda[i][1](x, y);
          m += S.texto(x + 46, y + 5, celda[i][0], ' style="font-size:12.5px;fill:var(--ink)"');
        }
        svg.innerHTML = m;
      })();
      </script>
'''


# --------------------------------------------------------------------------
# Escena 1 - montar el circuito a base de cables
# --------------------------------------------------------------------------
ESC_CIRCUITO = u'''
      <style>
        #esc-circuito [data-w]{cursor:pointer}
        #esc-circuito .marcador{display:flex;flex-wrap:wrap;gap:8px;margin-top:4px}
      </style>
      <div class="escena" id="esc-circuito">
        <div class="escena-barra">
          <span class="escena-titulo">Banco de montaje &middot; pon los cables que creas que hacen falta</span>
          <div class="seg" id="seg-circuito">
            <button type="button" data-w="c1" aria-pressed="false">Cable de arriba</button>
            <button type="button" data-w="c2" aria-pressed="false">Cable de abajo</button>
            <button type="button" data-w="c3" aria-pressed="false">Puente</button>
            <button type="button" data-w="int" aria-pressed="false">Interruptor</button>
            <button type="button" data-w="reset">Vaciar</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 300" id="svg-circuito" role="img"
               aria-label="Banco de montaje: una pila, una l&aacute;mpara, un interruptor y tres cables que se pueden poner y quitar"></svg>
        </div>
        <div class="pie" id="pie-circuito"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-circuito');
        if(!svg || !window.U6) return;
        var S = window.U6, pie = document.getElementById('pie-circuito');
        var seg = document.getElementById('seg-circuito');

        /* Geometria del banco. Cuatro nodos en rectangulo; la pila ocupa el
           lado izquierdo y la lampara el derecho.                            */
        var A = {x: 130, y: 70}, B = {x: 500, y: 70},
            C = {x: 500, y: 230}, D = {x: 130, y: 230};
        var IX1 = 290, IX2 = 350;          /* contactos del interruptor */
        var PX = 572;                       /* el puente pasa por aqui */
        var RL = 17;                        /* radio de la lampara */

        var est = {c1: false, c2: false, c3: false, int: false};

        /* ---- que hace el circuito con lo que hay puesto ------------------
           Nodos A B C D. La pila es siempre la arista A-D y la lampara la
           arista B-C. Los hilos son c1 (A-B, solo si el interruptor esta
           cerrado), c2 (D-C) y c3 (B-C, que salta la lampara).
           Cortocircuito = la pila se ve a si misma por hilo, sin lampara.    */
        function conectados(aristas, p, q){
          var padre = {A: 'A', B: 'B', C: 'C', D: 'D'};
          function raiz(x){ while(padre[x] !== x) x = padre[x]; return x; }
          for(var i = 0; i < aristas.length; i++){
            var r1 = raiz(aristas[i][0]), r2 = raiz(aristas[i][1]);
            if(r1 !== r2) padre[r1] = r2;
          }
          return raiz(p) === raiz(q);
        }
        function hilos(){
          var a = [];
          if(est.c1 && est.int) a.push(['A', 'B']);
          if(est.c2) a.push(['D', 'C']);
          if(est.c3) a.push(['B', 'C']);
          return a;
        }
        function diagnostico(){
          var h = hilos();
          if(conectados(h, 'A', 'D')) return 'corto';
          if(conectados(h.concat([['B', 'C']]), 'A', 'D')) return 'luce';
          return 'abierto';
        }

        var MSG = {
          nada: '<b>No has puesto nada todav&iacute;a.</b> La pila empuja, s&iacute;, pero las cargas no '
              + 'tienen por d&oacute;nde ir. Sin camino no hay corriente: ni poca, ni mucha. Ninguna.',
          medio: '<b>Falta el camino de vuelta.</b> Un solo cable no vale por mucho que lo conectes '
              + 'bien. Las cargas tienen que poder <b>volver a la pila</b>, o no se mueven. Prueba a '
              + 'poner tambi&eacute;n el otro cable.',
          apagado: '<b>El camino est&aacute; completo, pero el interruptor est&aacute; abierto.</b> Y eso '
              + 'no es un fallo: es exactamente para lo que sirve un interruptor. Un hueco de un '
              + 'mil&iacute;metro en el anillo apaga el circuito entero.',
          luce: '<b>Circuito cerrado: la l&aacute;mpara luce.</b> Hay un &uacute;nico anillo que sale de la '
              + 'pila, atraviesa la l&aacute;mpara y vuelve a la pila. Los cuatro elementos est&aacute;n: '
              + 'generador, conductores, receptor y control.',
          corto: '<b>Cortocircuito.</b> El puente une los dos lados de la l&aacute;mpara, as&iacute; que la '
              + 'corriente tiene un camino de cobre sin nada que la estorbe y se va por ah&iacute;. La '
              + 'l&aacute;mpara se queda a oscuras y la pila se calienta. En una pr&aacute;ctica esto es una '
              + 'pila quemada; en una instalaci&oacute;n de verdad, un incendio.',
          puente: '<b>El puente solo no hace nada.</b> Ser&aacute; un atajo cuando haya por d&oacute;nde llegar '
              + 'hasta &eacute;l. De momento sigue sin haber anillo.'
        };

        function mensaje(d){
          if(d === 'corto') return MSG.corto;
          if(d === 'luce')  return MSG.luce;
          if(est.c1 && est.c2 && !est.int) return MSG.apagado;
          if(!est.c1 && !est.c2 && !est.c3) return MSG.nada;
          if(!est.c1 && !est.c2) return MSG.puente;
          return MSG.medio;
        }

        function pinta(){
          var d = diagnostico();
          var INK = 'var(--ink)', OFF = 'var(--line)';
          var col = d === 'corto' ? 'var(--goo-rojo)' : INK;
          var m = '';

          /* --- lo que no esta puesto, en gris y a rayas, con su + --------- */
          function fantasma(dd, cx, cy){
            var s = S.trazo(dd, OFF, 2.2, true);
            s += '<circle cx="' + cx + '" cy="' + cy + '" r="11" fill="var(--surface)" stroke="'
               + OFF + '" stroke-width="1.6"></circle>';
            s += S.texto(cx, cy + 5, '+', ' text-anchor="middle" style="font-size:15px"');
            return s;
          }

          var dArr = 'M' + A.x + ' ' + A.y + ' L' + IX1 + ' ' + A.y
                   + ' M' + IX2 + ' ' + A.y + ' L' + B.x + ' ' + B.y;
          var dAba = 'M' + D.x + ' ' + D.y + ' L' + C.x + ' ' + C.y;
          var dPue = 'M' + B.x + ' ' + B.y + ' L' + PX + ' ' + B.y
                   + ' L' + PX + ' ' + C.y + ' L' + C.x + ' ' + C.y;

          m += est.c1 ? S.trazo(dArr, col, 2.6) : fantasma(dArr, 210, A.y);
          m += est.c2 ? S.trazo(dAba, col, 2.6) : fantasma(dAba, 315, D.y);
          m += est.c3 ? S.trazo(dPue, col, 2.6) : fantasma(dPue, PX, 150);

          /* --- la pila, siempre puesta: tres celdas de 1,5 V = 4,5 V ------ */
          var p = S.pila(A.x, 150, 3, d === 'corto' ? 'var(--goo-rojo)' : INK);
          m += S.cable(A.x, A.y, A.x, p.mas, col, 2.6);
          m += S.cable(A.x, p.menos, A.x, D.y, col, 2.6);
          m += p.svg;
          m += S.texto(A.x - 32, 148, '4,5 V', ' text-anchor="end"');
          m += S.texto(A.x - 32, 166, 'tres celdas', ' text-anchor="end" style="font-size:10px"');

          /* --- el interruptor, en el cable de arriba ---------------------- */
          if(est.c1){
            m += S.interruptor(IX1, IX2, A.y, est.int, col);
            m += S.texto(IX1 - 4, A.y - 34, 'interruptor', ' style="font-size:10px"');
          }

          /* --- la lampara, siempre puesta -------------------------------- */
          var luce = d === 'luce';
          m += S.cable(B.x, B.y, B.x, 150 - RL, col, 2.6);
          m += S.cable(B.x, 150 + RL, B.x, C.y, col, 2.6);
          m += S.lampara(B.x, 150, RL, luce ? 'var(--ink)' : (d === 'corto' ? 'var(--ink-soft)' : 'var(--ink)'),
                         luce ? 1 : 0);
          m += S.texto(B.x - 32, 154, luce ? 'enciende' : 'apagada',
                       ' text-anchor="end" style="font-size:11px;fill:'
                       + (luce ? 'var(--goo-verde)' : 'var(--ink-soft)') + '"');

          /* --- nodos donde el puente se pega al circuito ------------------ */
          if(est.c3){ m += S.nodo(B.x, B.y, col); m += S.nodo(C.x, C.y, col); }

          /* --- el veredicto, arriba a la izquierda ------------------------ */
          var etq = {abierto: 'CIRCUITO ABIERTO', luce: 'CIRCUITO CERRADO',
                     corto: 'CORTOCIRCUITO'}[d];
          var ecol = {abierto: 'var(--ink-soft)', luce: 'var(--goo-verde)',
                      corto: 'var(--goo-rojo)'}[d];
          m += S.texto(24, 34, etq, ' style="font-size:13px;letter-spacing:.12em;fill:' + ecol + '"');

          /* --- zonas de clic, encima de todo y sin pintar ----------------- */
          function zona(dd, ancho, id){
            return '<path d="' + dd + '" fill="none" stroke="#000" stroke-opacity="0" stroke-width="'
                 + ancho + '" pointer-events="stroke" data-w="' + id + '"></path>';
          }
          m += zona(dArr, 22, 'c1');
          m += zona(dAba, 22, 'c2');
          m += zona(dPue, 22, 'c3');
          if(est.c1){
            m += '<rect x="' + (IX1 - 12) + '" y="' + (A.y - 45) + '" width="' + (IX2 - IX1 + 24)
               + '" height="58" fill="#000" fill-opacity="0" pointer-events="all" data-w="int"></rect>';
          }

          svg.innerHTML = m;
          pie.innerHTML = mensaje(d);
          seg.querySelectorAll('button[data-w]').forEach(function(b){
            if(est.hasOwnProperty(b.dataset.w))
              b.setAttribute('aria-pressed', est[b.dataset.w] ? 'true' : 'false');
          });
        }

        function pulsa(w){
          if(w === 'reset'){ est = {c1: false, c2: false, c3: false, int: false}; }
          else if(est.hasOwnProperty(w)){ est[w] = !est[w]; }
          else return;
          pinta();
        }
        svg.addEventListener('click', function(e){
          var t = e.target.closest('[data-w]');
          if(t) pulsa(t.dataset.w);
        });
        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-w]');
          if(b) pulsa(b.dataset.w);
        });
        pinta();
      })();
      </script>
'''


# --------------------------------------------------------------------------
# Escena 2 - el banco de Ohm
# --------------------------------------------------------------------------
ESC_OHM = u'''
      <style>
        #esc-ohm .ctrl{display:flex;flex-wrap:wrap;gap:14px;align-items:center}
        #esc-ohm .ctrl label{font:400 11.5px var(--f-m);color:var(--ink-soft);
          display:flex;align-items:center;gap:7px}
        #esc-ohm .ctrl input[type=range]{width:120px;accent-color:var(--goo-azul)}
        #esc-ohm .ctrl b{font:500 12px var(--f-m);color:var(--ink);min-width:54px;display:inline-block}
      </style>
      <div class="escena" id="esc-ohm">
        <div class="escena-barra">
          <span class="escena-titulo">Banco de Ohm &middot; mueve el empuj&oacute;n y el estorbo</span>
          <div class="ctrl">
            <label>Tensi&oacute;n
              <input type="range" id="ohm-v" min="1.5" max="24" step="0.5" value="4.5"
                     aria-label="Tensi&oacute;n en voltios">
              <b id="ohm-vt">4,5 V</b></label>
            <label>Resistencia
              <input type="range" id="ohm-r" min="2" max="60" step="1" value="9"
                     aria-label="Resistencia en ohmios">
              <b id="ohm-rt">9 &#8486;</b></label>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 300" id="svg-ohm" role="img"
               aria-label="Circuito con amper&iacute;metro y volt&iacute;metro, y gr&aacute;fica de la intensidad frente a la tensi&oacute;n"></svg>
        </div>
        <div class="pie" id="pie-ohm"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-ohm');
        if(!svg || !window.U6) return;
        var S = window.U6, pie = document.getElementById('pie-ohm');
        var sV = document.getElementById('ohm-v'), sR = document.getElementById('ohm-r');
        var tV = document.getElementById('ohm-vt'), tR = document.getElementById('ohm-rt');

        /* --- el circuito, a la izquierda --- */
        var A = {x: 95, y: 80}, B = {x: 265, y: 80}, C = {x: 265, y: 220}, D = {x: 95, y: 220};
        var XA = 175, XV = 200;             /* amperimetro y voltimetro */
        /* --- la grafica, a la derecha: rectangulo de 240 x 180 ----------- */
        var GX = 360, GY = 250, GW = 240, GH = 180, VMAX = 24, IMAX = 3;
        function gx(v){ return GX + v / VMAX * GW; }
        function gy(i){ return GY - Math.min(i, IMAX) / IMAX * GH; }

        function coma(x, dec){ return x.toFixed(dec).replace('.', ','); }

        function pinta(){
          var V = parseFloat(sV.value), R = parseFloat(sR.value), I = V / R;
          var caliente = Math.min(1, (V * I) / 12);      /* solo para el color */
          var col = I > IMAX ? 'var(--goo-rojo)' : 'var(--ink)';
          var m = '';

          /* ---- circuito ---- */
          var p = S.pila(A.x, 150, 2, col);
          m += S.cable(A.x, A.y, A.x, p.mas, col, 2.4);
          m += S.cable(A.x, p.menos, A.x, D.y, col, 2.4);
          m += p.svg;
          m += S.texto(A.x - 26, 155, coma(V, 1) + ' V',
                       ' text-anchor="end" style="font-size:12px;fill:var(--ink)"');

          m += S.cable(A.x, A.y, XA - 14, A.y, col, 2.4);
          m += S.medidor(XA, A.y, 'A', col);
          m += S.cable(XA + 14, A.y, B.x, A.y, col, 2.4);
          m += S.cable(A.x, D.y, C.x, C.y, col, 2.4);
          m += S.cable(B.x, B.y, B.x, 122, col, 2.4);
          m += S.cable(B.x, 178, B.x, C.y, col, 2.4);

          /* voltimetro en paralelo con la resistencia, por dentro del anillo:
             asi no se pisa con la grafica, que empieza en x = 360.          */
          m += S.trazo('M' + B.x + ' 110 L' + XV + ' 110 L' + XV + ' 136', col, 2.4);
          m += S.trazo('M' + XV + ' 164 L' + XV + ' 190 L' + B.x + ' 190', col, 2.4);
          m += S.medidor(XV, 150, 'V', col);
          m += S.nodo(B.x, 110, col); m += S.nodo(B.x, 190, col);

          /* la resistencia se colorea segun lo que se calienta */
          m += '<rect x="' + (B.x - 11) + '" y="122" width="22" height="56" fill="var(--goo-rojo)"'
             + ' opacity="' + (0.75 * caliente).toFixed(3) + '"></rect>';
          m += S.resistencia(B.x, 150, col, true);
          m += S.texto(B.x + 20, 155, R + ' \\u2126', ' style="font-size:12px;fill:var(--ink)"');

          m += S.texto(XA, A.y - 26, 'amper\\u00edmetro (en serie)',
                       ' style="font-size:10px" text-anchor="middle"');
          m += S.texto(XV, 242, 'volt\\u00edmetro (en paralelo)',
                       ' style="font-size:10px" text-anchor="middle"');

          /* ---- grafica I frente a V ---- */
          m += S.trazo('M' + GX + ' ' + (GY - GH) + ' L' + GX + ' ' + GY + ' L' + (GX + GW) + ' ' + GY,
                       'var(--line)', 2);
          var vt = [0, 6, 12, 18, 24], it = [0, 0.5, 1, 1.5, 2, 2.5, 3];
          vt.forEach(function(v){
            m += S.cable(gx(v), GY, gx(v), GY + 5, 'var(--line)', 1.5);
            m += S.texto(gx(v), GY + 19, v, ' text-anchor="middle" style="font-size:10px"');
          });
          it.forEach(function(i){
            m += S.cable(GX - 5, gy(i), GX, gy(i), 'var(--line)', 1.5);
            m += S.texto(GX - 9, gy(i) + 4, coma(i, 1), ' text-anchor="end" style="font-size:10px"');
          });
          m += S.texto(GX + GW, GY + 34, 'tensi\\u00f3n (V)', ' text-anchor="end" style="font-size:10.5px"');
          m += S.texto(GX - 30, GY - GH - 8, 'intensidad (A)', ' style="font-size:10.5px"');

          /* La recta I = V/R. Se recorta donde primero se salga del cuadro. */
          var vFin = Math.min(VMAX, IMAX * R);
          m += S.cable(gx(0), gy(0), gx(vFin), gy(vFin / R), 'var(--goo-azul)', 2.6);

          /* punto de trabajo. Si la corriente se sale por arriba se dice, en
             vez de dibujar un punto que miente sobre donde esta.             */
          var px = gx(V), py = gy(I), fuera = I > IMAX;
          /* La guia horizontal solo se dibuja si el punto esta donde dice:
             con el punto recortado marcaria una corriente que no es.        */
          m += S.trazo('M' + px + ' ' + GY + ' L' + px + ' ' + py
                     + (fuera ? '' : ' L' + GX + ' ' + py), 'var(--ink-soft)', 1.4, true);
          m += '<circle cx="' + px + '" cy="' + py + '" r="6" fill="'
             + (fuera ? 'var(--goo-rojo)' : 'var(--goo-azul)') + '"></circle>';
          if(fuera){
            m += S.texto(GX + GW, GY - GH + 18, 'fuera de escala',
                         ' text-anchor="end" style="font-size:10px;fill:var(--goo-rojo)"');
          }

          svg.innerHTML = m;
          tV.innerHTML = coma(V, 1) + ' V';
          tR.innerHTML = R + ' &#8486;';

          var aviso = '';
          if(I > IMAX){
            aviso = ' <b style="color:var(--goo-rojo)">Ojo: m&aacute;s de 3 A.</b> Una pila de petaca '
                  + 'no puede dar esto, y una fuente de laboratorio s&iacute;: la resistencia se pondr&iacute;a '
                  + 'al rojo y acabar&iacute;a rota.';
          } else if(I > 1){
            aviso = ' Con esta corriente la resistencia ya se calienta de forma apreciable.';
          }
          pie.innerHTML = '<b>I = V / R = ' + coma(V, 1) + ' / ' + R + ' = ' + coma(I, 3)
            + ' A</b> &middot; es decir, ' + Math.round(I * 1000) + ' mA.'
            + ' La recta azul es la ley de Ohm para esta resistencia: pasa por el origen y su '
            + 'inclinaci&oacute;n depende <b>solo</b> de R. Si mueves la tensi&oacute;n, el punto se desliza '
            + 'por la recta; si mueves la resistencia, cambia la recta entera.' + aviso;
        }
        sV.addEventListener('input', pinta);
        sR.addEventListener('input', pinta);
        pinta();
      })();
      </script>
'''


# --------------------------------------------------------------------------
# Escena 3 - serie o paralelo, y que pasa cuando una se funde
# --------------------------------------------------------------------------
ESC_SERIE = u'''
      <style>
        #esc-sp .tabla{width:100%;border-collapse:collapse;font:400 13px var(--f-m);margin-top:2px}
        #esc-sp .tabla td{padding:4px 8px 4px 0;border-bottom:1px solid var(--line-soft);color:var(--ink-soft)}
        #esc-sp .tabla td:last-child{text-align:right;color:var(--ink);font-weight:500}
        #esc-sp .lamp{cursor:pointer}
      </style>
      <div class="escena" id="esc-sp">
        <div class="escena-barra">
          <span class="escena-titulo">Tres l&aacute;mparas iguales &middot; pulsa una para fundirla</span>
          <div class="seg" id="seg-sp">
            <button type="button" data-m="serie" aria-pressed="true">Serie</button>
            <button type="button" data-m="paralelo" aria-pressed="false">Paralelo</button>
            <button type="button" data-m="reparar">Reparar todas</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 300" id="svg-sp" role="img"
               aria-label="Tres l&aacute;mparas conectadas en serie o en paralelo a una pila de 4,5 voltios"></svg>
        </div>
        <div class="pie" id="pie-sp"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-sp');
        if(!svg || !window.U6) return;
        var S = window.U6, pie = document.getElementById('pie-sp');
        var seg = document.getElementById('seg-sp');

        var VP = 4.5, RL = 9;               /* pila de petaca y lamparas de 9 ohmios */
        var IN = VP / RL;                   /* 0,5 A: lo que pide una lampara sola */
        var XS = [200, 330, 460], RR = 19;
        var modo = 'serie', rota = [false, false, false];

        function coma(x, d){ return x.toFixed(d).replace('.', ','); }

        /* --- las cuentas, con la ley de Ohm y nada mas ------------------- */
        function calcula(){
          var vivas = rota.filter(function(r){ return !r; }).length;
          if(modo === 'serie'){
            if(vivas < 3) return {Rt: null, It: 0, Vl: 0, Il: 0, abierto: true, vivas: vivas};
            var Rt = RL * 3, It = VP / Rt;
            return {Rt: Rt, It: It, Vl: It * RL, Il: It, abierto: false, vivas: vivas};
          }
          if(vivas === 0) return {Rt: null, It: 0, Vl: 0, Il: 0, abierto: true, vivas: 0};
          var It2 = IN * vivas;
          return {Rt: RL / vivas, It: It2, Vl: VP, Il: IN, abierto: false, vivas: vivas};
        }
        /* El brillo va con la potencia, que es proporcional al cuadrado de
           la corriente: media corriente es la cuarta parte de luz.          */
        function brillo(I){ var b = (I / IN) * (I / IN); return b > 1 ? 1 : b; }

        function pinta(){
          var c = calcula(), INK = 'var(--ink)';
          var col = c.abierto ? 'var(--ink-soft)' : INK;
          var b = brillo(c.Il), m = '';

          var p = S.pila(80, 160, 3, INK);
          m += p.svg;
          m += S.texto(22, 164, '4,5 V');
          m += S.cable(80, 100, 80, p.mas, col, 2.4);
          m += S.cable(80, p.menos, 80, 220, col, 2.4);

          if(modo === 'serie'){
            /* un unico anillo: las tres lamparas seguidas por arriba */
            var x = 80;
            for(var i = 0; i < 3; i++){
              m += S.cable(x, 100, XS[i] - RR, 100, col, 2.4);
              x = XS[i] + RR;
            }
            m += S.cable(x, 100, 560, 100, col, 2.4);
            m += S.trazo('M560 100 L560 220 L80 220', col, 2.4);
            for(var j = 0; j < 3; j++) m += pintaLampara(XS[j], 100, j, c, b);
            m += S.texto(320, 262, 'Una detr\\u00e1s de otra: un solo camino',
                         ' text-anchor="middle" style="font-size:12px"');
          } else {
            /* Dos carriles y tres ramas verticales entre ellos. Los carriles
               terminan en la ultima rama: un cable que acaba en el aire no se
               deja en un esquema.                                            */
            m += S.cable(80, 100, XS[2], 100, col, 2.4);
            m += S.cable(80, 220, XS[2], 220, col, 2.4);
            for(var k = 0; k < 3; k++){
              var xr = XS[k];
              m += S.cable(xr, 100, xr, 160 - RR, col, 2.4);
              m += S.cable(xr, 160 + RR, xr, 220, col, 2.4);
              m += S.nodo(xr, 100, col); m += S.nodo(xr, 220, col);
              m += pintaLampara(xr, 160, k, c, b);
            }
            m += S.texto(320, 262, 'Cada una por su lado: tres caminos',
                         ' text-anchor="middle" style="font-size:12px"');
          }

          /* veredicto */
          var etq, ecol;
          if(c.abierto){ etq = 'CIRCUITO ABIERTO \\u00b7 TODAS APAGADAS'; ecol = 'var(--goo-rojo)'; }
          else if(c.vivas === 3){ etq = 'LAS TRES LUCEN'; ecol = 'var(--goo-verde)'; }
          else { etq = c.vivas + ' DE 3 SIGUEN LUCIENDO'; ecol = 'var(--goo-verde)'; }
          m += S.texto(22, 36, etq, ' style="font-size:13px;letter-spacing:.12em;fill:' + ecol + '"');

          svg.innerHTML = m;
          pinta_pie(c, b);
          seg.querySelectorAll('button[data-m]').forEach(function(x){
            if(x.dataset.m === 'serie' || x.dataset.m === 'paralelo')
              x.setAttribute('aria-pressed', x.dataset.m === modo ? 'true' : 'false');
          });
        }

        /* El rotulo va debajo en serie (ahi no hay cable) y al lado en
           paralelo (donde debajo pasa la rama vertical).                    */
        function pintaLampara(cx, cy, i, c, b){
          var luce = !rota[i] && !c.abierto;
          var s = '<g class="lamp" data-l="' + i + '">';
          if(rota[i]){
            /* Lampara fundida: el aspa se dibuja partida por el medio, que es
               justo lo que le ha pasado al filamento.                        */
            var k = RR * Math.SQRT1_2, g = 5;
            s += '<circle cx="' + cx + '" cy="' + cy + '" r="' + RR + '" fill="var(--surface)"'
               + ' stroke="var(--ink-soft)" stroke-width="2.4"></circle>';
            [[-1, -1], [1, 1], [-1, 1], [1, -1]].forEach(function(d){
              s += S.cable(cx + d[0] * k, cy + d[1] * k,
                           cx + d[0] * g, cy + d[1] * g, 'var(--goo-rojo)', 2.4);
            });
          } else {
            s += S.lampara(cx, cy, RR, 'var(--ink)', luce ? b : 0);
          }
          var etq = rota[i] ? 'fundida' : 'L' + (i + 1);
          var estilo = 'font-size:' + (rota[i] ? '10' : '11') + 'px'
                     + (rota[i] ? ';fill:var(--goo-rojo)' : '');
          if(modo === 'serie'){
            s += S.texto(cx, cy + 40, etq, ' text-anchor="middle" style="' + estilo + '"');
          } else {
            s += S.texto(cx + RR + 9, cy + 5, etq, ' style="' + estilo + '"');
          }
          s += '<circle cx="' + cx + '" cy="' + cy + '" r="' + (RR + 8)
             + '" fill="#000" fill-opacity="0" pointer-events="all"></circle></g>';
          return s;
        }

        function pinta_pie(c, b){
          var f = '<table class="tabla">';
          f += fila('Resistencia total', c.Rt === null ? 'infinita (abierto)' : coma(c.Rt, 2) + ' &#8486;');
          f += fila('Corriente que da la pila', coma(c.It, 3) + ' A');
          f += fila('Tensi&oacute;n en cada l&aacute;mpara que luce', coma(c.Vl, 2) + ' V');
          f += fila('Corriente por cada l&aacute;mpara que luce', coma(c.Il, 3) + ' A');
          f += fila('Brillo respecto a una l&aacute;mpara sola', Math.round(b * 100) + ' de 100');
          f += '</table>';
          var t;
          if(modo === 'serie' && c.abierto){
            t = '<b>Se ha fundido una y se han apagado las tres.</b> En serie solo hay un camino, y '
              + 'la l&aacute;mpara rota lo ha cortado para todas. Esta es la guirnalda vieja.';
          } else if(modo === 'serie'){
            t = '<b>Las tres en serie brillan poco.</b> Las resistencias se suman (9 + 9 + 9 = 27 '
              + '&#8486;), as&iacute; que la corriente cae a la tercera parte, y como el brillo va con el '
              + 'cuadrado de la corriente, queda en <b>1 de cada 9</b>. La tensi&oacute;n de la pila se '
              + 'reparte: 1,5 V para cada una.';
          } else if(c.abierto){
            t = '<b>Se han fundido las tres.</b> Cada una ten&iacute;a su propio camino, as&iacute; que han '
              + 'ido cayendo de una en una, sin arrastrar a las dem&aacute;s.';
          } else {
            t = '<b>En paralelo cada l&aacute;mpara recibe los 4,5 V completos</b> y brilla igual que si '
              + 'estuviera sola, haya una o haya tres. Lo que cambia es lo que le pides a la pila: '
              + 'la resistencia total <b>baja</b> al a&ntilde;adir l&aacute;mparas y la corriente total '
              + '<b>sube</b>. Esta es tu casa &mdash; y es la raz&oacute;n de que una regleta demasiado '
              + 'cargada se caliente.';
          }
          pie.innerHTML = t + f;
        }
        function fila(a, b){ return '<tr><td>' + a + '</td><td>' + b + '</td></tr>'; }

        svg.addEventListener('click', function(e){
          var g = e.target.closest('[data-l]');
          if(!g) return;
          var i = parseInt(g.dataset.l, 10);
          rota[i] = !rota[i];
          pinta();
        });
        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-m]');
          if(!b) return;
          if(b.dataset.m === 'reparar') rota = [false, false, false];
          else modo = b.dataset.m;
          pinta();
        });
        pinta();
      })();
      </script>
'''
