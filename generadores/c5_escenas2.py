# -*- coding: utf-8 -*-
u"""Escenas de las sesiones 3 y 4 de la U5 de 4.o: neumatica.

  ESCENA_CILINDRO  S3 - corte de un cilindro con la cuenta F = p x A hecha
                   delante. Los diametros del dibujo estan a escala entre si;
                   el recorrido no, y sale dicho dentro de la escena.
  ESCENA_MANDO     S4 - circuito neumatico con simbolos ISO 1219. Las cajas de
                   las valvulas se desplazan como se desplaza el distribuidor
                   de verdad, y las lineas con presion se calculan a partir del
                   estado de las valvulas, no estan pintadas de antemano.

De donde salen los numeros:

  F = p x A     1 bar = 0,1 N/mm2. Con D = 32 mm y 6 bar:
                A = pi 32^2 / 4 = 804,2 mm2  ->  F = 0,6 x 804,2 = 482,5 N,
                que son los 49 kg que dan las tablas de cualquier fabricante
                para un cilindro de 32 a 6 bar.

  d vastago     tabla normalizada ISO 15552: 12->6, 16->6, 20->8, 25->10,
                32->12, 40->16, 50->20, 80->25, 100->25.

  muelle        en un cilindro de simple efecto el muelle de retorno se come
                el equivalente a unos 0,5 bar de la carrera de avance. Aqui se
                modela asi (0,05 N/mm2 x A) y sale dicho en pantalla.

  consumo       el aire se paga en litros NORMALES: el volumen geometrico por
                la presion absoluta (p + 1). Es la cuenta que hace cualquier
                tabla de dimensionado de compresores.

  asiento       una valvula de asiento de 2 mm de paso deja pasar del orden de
                100 NL/min a 6 bar. El caudal va con el area, asi que
                d = 2 x raiz(Q/100). Es una regla de tanteo, no una norma, y
                sale dicho en el pie de la escena.
"""

# ---------------------------------------------------------------------------
# S3 - El cilindro y la cuenta de la fuerza
#
# Lienzo 640 x 380.
#   Eje del cilindro en y = 118. Suelo en y = 174.
#   Escala de diametros: 1,7 px por mm (50 mm -> 85 px). El RECORRIDO del
#   dibujo es fijo, 150 px, y no esta a esa escala: con 200 mm de carrera y
#   1,7 px/mm harian falta 340 px y no cabe. Sale avisado dentro del lienzo.
#       tapa trasera   x  58.. 70
#       camisa         x  70..300
#       tapa delantera x 300..312
#       embolo         x xe..xe+14,  xe de 78 a 228
#       vastago        de xe+14 a xtip = 336 + (xe-78)   ->  336..486
#       caja           xtip..xtip+72, y 62..174
#   Barras de fuerza: rotulo hasta x=210, barra de 218 a 548, valor en 556.
# ---------------------------------------------------------------------------
ESCENA_CILINDRO = u'''
      <div class="escena" id="esc-cil">
        <div class="escena-barra">
          <span class="escena-titulo">Fuerza = presi&oacute;n &times; superficie</span>
          <div class="seg" id="seg-cil-tipo">
            <button type="button" data-t="doble" aria-pressed="true">Doble efecto</button>
            <button type="button" data-t="simple">Simple efecto</button>
          </div>
        </div>
        <div class="escena-barra">
          <span class="escena-titulo">Di&aacute;metro del &eacute;mbolo</span>
          <div class="seg" id="seg-cil-d">
            <button type="button" data-d="12">12</button>
            <button type="button" data-d="16">16</button>
            <button type="button" data-d="20">20</button>
            <button type="button" data-d="25">25</button>
            <button type="button" data-d="32" aria-pressed="true">32</button>
            <button type="button" data-d="40">40</button>
            <button type="button" data-d="50">50 mm</button>
          </div>
        </div>
        <div class="escena-barra">
          <label class="ctrl" style="flex:1 1 230px">
            <span>Presi&oacute;n</span>
            <input id="cil-p" type="range" min="10" max="100" value="60" step="5">
            <b id="cil-p-val">6,0 bar</b>
          </label>
          <label class="ctrl" style="flex:1 1 230px">
            <span>Caja que hay que empujar</span>
            <input id="cil-m" type="range" min="0" max="200" value="60" step="5">
            <b id="cil-m-val">60 kg</b>
          </label>
          <div class="seg" id="seg-cil-mov">
            <button type="button" data-a="av">Avanzar</button>
            <button type="button" data-a="re">Retroceder</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 380" id="svg-cil" role="img"
               aria-label="Corte de un cilindro neum&aacute;tico empujando una caja, con las fuerzas calculadas"></svg>
        </div>
        <div class="pie" id="pie-cil"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-cil');
        if(!svg) return;
        var pie = document.getElementById('pie-cil');
        var segT = document.getElementById('seg-cil-tipo');
        var segD = document.getElementById('seg-cil-d');
        var segM = document.getElementById('seg-cil-mov');
        var pIn = document.getElementById('cil-p'), pTx = document.getElementById('cil-p-val');
        var mIn = document.getElementById('cil-m'), mTx = document.getElementById('cil-m-val');

        var K = 1.7;              /* pixeles por milimetro, solo en diametro */
        var CARRERA = 200;        /* mm */
        var CICLOS = 12;          /* ciclos por minuto, para el consumo */
        var MU = 0.4;             /* rozamiento caja de madera sobre acero */
        var G = 9.81;
        var VASTAGO = {12:6, 16:6, 20:8, 25:10, 32:12, 40:16, 50:20};

        var tipo = 'doble', D = 32, pos = 0, destino = 0, raf = null;

        function coma(n, d){ return n.toFixed(d).replace('.', ','); }
        function newton(f){ return coma(f, f < 100 ? 1 : 0) + ' N'; }

        /* -------------------- toda la cuenta, en un sitio -------------------- */
        function calcula(){
          var p = +pIn.value / 10;              /* bar */
          var m = +mIn.value;                   /* kg  */
          var d = VASTAGO[D];
          var Aav = Math.PI * D * D / 4;
          var Aret = Math.PI * (D * D - d * d) / 4;
          var Fmuelle = 0.05 * Aav;             /* el muelle se come ~0,5 bar */
          var Fav, Fret;
          if(tipo === 'doble'){
            Fav = p * 0.1 * Aav;
            Fret = p * 0.1 * Aret;
          } else {
            Fav = p * 0.1 * Aav - Fmuelle;
            Fret = Fmuelle;                     /* al volver solo tira el muelle */
          }
          var Fnec = MU * m * G;
          /* litros normales por ciclo: volumen geometrico x presion absoluta */
          var vol = (tipo === 'doble' ? (Aav + Aret) : Aav) * CARRERA / 1e6 * (p + 1);
          return {p:p, m:m, d:d, Aav:Aav, Aret:Aret, Fmuelle:Fmuelle, Fav:Fav,
                  Fret:Fret, Fnec:Fnec, mueve:Fav > Fnec, vol:vol,
                  caudal:vol * CICLOS};
        }

        /* ----------------------------- dibujo ----------------------------- */
        function caja(x, y, w, h, relleno, borde, grosor){
          return '<rect x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" width="'
               + Math.max(0, w).toFixed(1) + '" height="' + Math.max(0, h).toFixed(1)
               + '" rx="1.5" fill="' + relleno + '" stroke="' + borde
               + '" stroke-width="' + grosor + '"></rect>';
        }
        function hilo(d, color, grosor, guion){
          return '<path d="' + d + '" fill="none" stroke="' + (color || 'var(--ink-soft)')
               + '" stroke-width="' + (grosor || 2) + '" stroke-linecap="round"'
               + (guion ? ' stroke-dasharray="' + guion + '"' : '') + '></path>';
        }
        function rot(x, y, txt, est, anchor){
          return '<text x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" class="rotulo-svg"'
               + (anchor ? ' text-anchor="' + anchor + '"' : '')
               + (est ? ' style="' + est + '"' : '') + '>' + txt + '</text>';
        }
        function barra(y, etq, valor, frac, color){
          var W = 330;
          var s = rot(210, y + 4, etq, 'font-size:10.5px', 'end');
          s += caja(218, y - 9, W, 18, 'var(--surface-2)', 'var(--line)', 1);
          s += caja(218, y - 9, Math.max(2, W * Math.min(1, frac)), 18, color, color, 1);
          s += rot(556, y + 4, valor, 'font-size:12px;fill:var(--ink);font-weight:500');
          return s;
        }

        function pinta(){
          var r = calcula();
          var EJE = 118, SUELO = 174;
          var Dpx = D * K, dpx = r.d * K;
          var pared = 6;
          /* El embolo recorre 194 px, que es el hueco real que le queda dentro
             de la camisa (x 70..300) descontando sus propios 14 px y 2 de
             holgura contra cada tapa. Asi el dibujo se ve lleno al final. */
          var xe = 78 + pos * 194;
          var xtip = 336 + (xe - 78);
          var s = '';

          s += rot(16, 22, 'CORTE DEL CILINDRO', 'font-size:10.5px');
          s += rot(624, 22, 'los di\\u00e1metros est\\u00e1n a escala entre s\\u00ed; el recorrido no',
                   'font-size:9px', 'end');

          /* suelo */
          s += hilo('M16 ' + SUELO + ' H624', 'var(--ink-soft)', 2);
          for(var i = 0; i < 39; i++)
            s += hilo('M' + (18 + i * 16) + ' ' + SUELO + ' l-6 8', 'var(--line)', 1.5);

          /* soporte del cilindro */
          s += caja(120, EJE + Dpx / 2 + pared, 120, SUELO - (EJE + Dpx / 2 + pared),
                    'var(--surface-2)', 'var(--line)', 1.5);

          /* camisa: dos paredes y el hueco del embolo */
          var yInt = EJE - Dpx / 2, hInt = Dpx;
          s += caja(70, yInt - pared, 230, pared, 'var(--surface-2)', 'var(--ink-soft)', 1.5);
          s += caja(70, yInt + hInt, 230, pared, 'var(--surface-2)', 'var(--ink-soft)', 1.5);
          s += caja(70, yInt, 230, hInt, 'var(--paper)', 'none', 0);
          /* tapas */
          s += caja(58, yInt - pared, 12, hInt + 2 * pared, 'var(--surface-2)', 'var(--ink-soft)', 1.5);
          s += caja(300, yInt - pared, 12, hInt + 2 * pared, 'var(--surface-2)', 'var(--ink-soft)', 1.5);

          /* camara trasera con presion cuando avanza */
          var avanzando = (destino === 1);
          s += caja(70, yInt, xe - 70, hInt, avanzando ? 'var(--accent-soft)' : 'var(--surface)',
                    'none', 0);
          if(tipo === 'doble')
            s += caja(xe + 14, yInt, 300 - (xe + 14), hInt,
                      avanzando ? 'var(--surface)' : 'var(--accent-soft)', 'none', 0);

          /* Muelle del simple efecto. En un corte el muelle rodea al vastago,
             asi que se dibujan DOS zigzags, uno arriba y otro abajo, dentro
             del hueco anular que queda entre el vastago y la camisa. */
          if(tipo === 'simple'){
            var x0 = xe + 14, x1 = 298;
            var amp = Math.max(1.5, (hInt / 2 - dpx / 2) / 2 - 1);
            var cen = (hInt / 2 + dpx / 2) / 2;
            var n = Math.max(6, Math.round((x1 - x0) / 13));
            for(var lado = -1; lado <= 1; lado += 2){
              var dm = '';
              for(i = 0; i <= n; i++){
                var xx = x0 + (x1 - x0) * i / n;
                var yy = EJE + lado * cen + (i % 2 ? -amp : amp);
                dm += (i ? ' L' : 'M') + xx.toFixed(1) + ' ' + yy.toFixed(1);
              }
              s += hilo(dm, 'var(--goo-rojo)', 1.8);
            }
          }

          /* embolo y vastago */
          s += caja(xe, yInt + 1, 14, hInt - 2, 'var(--ink-soft)', 'var(--ink)', 1.5);
          s += caja(xe + 14, EJE - dpx / 2, xtip - (xe + 14), dpx,
                    'var(--surface-2)', 'var(--ink-soft)', 1.5);

          /* la caja que hay que empujar */
          s += caja(xtip, SUELO - 112, 72, 112, r.mueve ? 'var(--surface)' : 'var(--surface-2)',
                    r.mueve ? 'var(--goo-verde)' : 'var(--goo-rojo)', 2);
          s += rot(xtip + 36, SUELO - 62, r.m + ' kg',
                   'font-size:14px;fill:var(--ink);font-weight:500', 'middle');
          s += rot(xtip + 36, SUELO - 44, '\\u03bc = ' + coma(MU, 1), 'font-size:9.5px', 'middle');

          /* tomas de aire: salen por arriba de las tapas, que es donde se ven */
          var yT = yInt - pared;
          s += hilo('M64 ' + yT.toFixed(1) + ' V' + (yT - 22).toFixed(1), 'var(--goo-azul)', 2);
          s += rot(64, yT - 27, '1', 'font-size:10px;fill:var(--goo-azul)', 'middle');
          if(tipo === 'doble'){
            s += hilo('M306 ' + yT.toFixed(1) + ' V' + (yT - 22).toFixed(1), 'var(--goo-azul)', 2);
            s += rot(306, yT - 27, '2', 'font-size:10px;fill:var(--goo-azul)', 'middle');
          } else {
            /* el simple efecto no lleva segunda toma: lleva un respiradero, y
               si se tapa, el cilindro no sale porque comprime el aire de dentro */
            s += hilo('M306 ' + yT.toFixed(1) + ' V' + (yT - 14).toFixed(1), 'var(--ink-soft)', 1.6);
            s += '<path d="M300 ' + (yT - 14).toFixed(1) + ' L312 ' + (yT - 14).toFixed(1)
               + ' L306 ' + (yT - 26).toFixed(1) + ' Z" fill="none" stroke="var(--ink-soft)" stroke-width="1.6"></path>';
            s += rot(318, yT - 18, 'respiradero', 'font-size:9px');
          }

          /* cotas del diametro */
          s += hilo('M46 ' + yInt + ' H' + 58, 'var(--goo-azul)', 1, '3 3');
          s += hilo('M46 ' + (yInt + hInt) + ' H58', 'var(--goo-azul)', 1, '3 3');
          s += hilo('M50 ' + yInt + ' V' + (yInt + hInt), 'var(--goo-azul)', 1.5);
          s += rot(44, EJE + 4, D + '', 'font-size:11px;fill:var(--goo-azul)', 'end');

          /* ========================= las barras ========================= */
          var maxF = Math.max(r.Fav, r.Fret, r.Fnec, 1);
          s += rot(16, 216, 'LAS FUERZAS, A LA MISMA ESCALA', 'font-size:10.5px');
          s += barra(246, 'Empuja al avanzar', newton(r.Fav), r.Fav / maxF,
                     r.mueve ? 'var(--goo-verde)' : 'var(--goo-amarillo)');
          s += barra(282, tipo === 'doble' ? 'Tira al retroceder' : 'Tira el muelle al volver',
                     newton(r.Fret), r.Fret / maxF, 'var(--goo-azul)');
          s += barra(318, 'Hace falta para mover la caja', newton(r.Fnec), r.Fnec / maxF,
                     'var(--goo-rojo)');
          s += rot(16, 358, 'Aire gastado: ' + coma(r.vol, 2)
                   + ' litros normales por ciclo \\u00b7 a ' + CICLOS + ' ciclos por minuto, '
                   + coma(r.caudal, 1) + ' NL/min', 'font-size:10.5px;fill:var(--ink)');

          svg.innerHTML = s;

          /* ========================== el pie ========================== */
          var txt = '<b>' + D + ' mm</b> de &eacute;mbolo son <b>A = &pi; &middot; ' + D
            + '&sup2; / 4 = ' + coma(r.Aav, 1) + ' mm&sup2;</b>. A ' + coma(r.p, 1)
            + ' bar (' + coma(r.p * 0.1, 2) + ' N por mm&sup2;) el aire empuja con <b>'
            + coma(r.p * 0.1, 2) + ' &times; ' + coma(r.Aav, 1) + ' = '
            + newton(r.p * 0.1 * r.Aav) + '</b>';
          if(tipo === 'simple')
            txt += ', menos los ' + newton(r.Fmuelle) + ' que se come el muelle: <b>'
                 + newton(r.Fav) + '</b>';
          txt += ', o sea <b>' + coma(r.Fav / G, 1) + ' kg de fuerza</b>.';

          txt += '<br>Al volver, el aire empuja por el lado del v&aacute;stago, que <b>tapa parte '
               + 'del &eacute;mbolo</b>: quedan ' + coma(r.Aret, 1) + ' mm&sup2; de los '
               + coma(r.Aav, 1) + '. ';
          txt += tipo === 'doble'
            ? 'Por eso un cilindro de doble efecto <b>tira menos de lo que empuja</b>: '
              + newton(r.Fret) + ' frente a ' + newton(r.Fav) + '.'
            : 'En el de simple efecto ni siquiera entra aire por ah&iacute;: vuelve el muelle, y '
              + 'con &eacute;l solo se cuenta con ' + newton(r.Fret) + '.';

          txt += '<br>La caja de ' + r.m + ' kg no hay que levantarla, hay que <b>arrastrarla</b>: '
               + 'con &mu; = ' + coma(MU, 1) + ' cuesta ' + coma(MU, 1) + ' &times; ' + r.m
               + ' &times; 9,81 = <b>' + newton(r.Fnec) + '</b>. ';
          txt += r.mueve
            ? 'Sobran ' + newton(r.Fav - r.Fnec) + ': <b>la mueve</b>.'
            : '<b>No la mueve.</b> Y no se arregla subiendo la presi&oacute;n sin m&aacute;s (la red '
              + 'de un taller da 6 bar y poco m&aacute;s): se arregla con un &eacute;mbolo mayor, '
              + 'que es lo &uacute;nico que crece al cuadrado.';

          pie.innerHTML = txt
            + '<br><span style="font-size:12.5px">La fuerza de la cuenta es la <b>te&oacute;rica</b>: '
            + 'en un cilindro real el rozamiento de las juntas se lleva entre un 5 y un 10 %, y por '
            + 'eso los cat&aacute;logos dan la fuerza con un coeficiente. El muelle del simple efecto '
            + 'se modela aqu&iacute; como el equivalente a <b>0,5 bar</b>. Los di&aacute;metros de '
            + 'v&aacute;stago son los normalizados (ISO 15552). El aire se mide en <b>litros '
            + 'normales</b>: el volumen del cilindro por la presi&oacute;n absoluta, porque ese aire '
            + 'hubo que comprimirlo antes.</span>';
        }

        /* ------------------------- movimiento ------------------------- */
        function anima(){
          var r = calcula();
          var meta = destino;
          if(meta === 1 && !r.mueve) meta = pos;     /* no tiene fuerza: no se mueve */
          var paso = 0.022;
          if(Math.abs(pos - meta) < paso){ pos = meta; pinta(); raf = null; return; }
          pos += (meta > pos ? paso : -paso);
          pinta();
          raf = requestAnimationFrame(anima);
        }
        function mueve(a){
          destino = (a === 'av') ? 1 : 0;
          if(raf) cancelAnimationFrame(raf);
          raf = requestAnimationFrame(anima);
        }

        function pulsa(cont, attr, fn){
          cont.addEventListener('click', function(e){
            var b = e.target.closest('button[' + attr + ']');
            if(!b) return;
            cont.querySelectorAll('button').forEach(function(x){
              x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
            });
            fn(b.getAttribute(attr));
          });
        }
        pulsa(segT, 'data-t', function(v){ tipo = v; pinta(); });
        pulsa(segD, 'data-d', function(v){ D = +v; pinta(); });
        pulsa(segM, 'data-a', function(v){ mueve(v); });
        pIn.addEventListener('input', function(){
          pTx.textContent = coma(+pIn.value / 10, 1) + ' bar'; pinta();
        });
        mIn.addEventListener('input', function(){
          mTx.textContent = mIn.value + ' kg'; pinta();
        });

        pinta();
      })();
      </script>
'''


# ---------------------------------------------------------------------------
# S4 - Mando directo e indirecto, con simbolos ISO 1219
#
# Lienzo 640 x 450.
#   Cilindro doble efecto:  cuerpo x 340..500, y 56..104 (eje y=80)
#                           embolo xp de 346 a 426; vastago hasta 512+(xp-346)
#                           tomas por debajo de las tapas, en x=337 y x=503
#   Valvula 5/2:  lado S=54, VENTANA x 420..474, y 200..254
#                 reposo    -> caja x 366..474 (manda el cuadro DERECHO)
#                 accionada -> caja x 420..528 (manda el cuadro IZQUIERDO)
#                 vias sobre la ventana: abajo 5@429 1@447 3@465 ; arriba 4@438 2@456
#   Pulsador P1:  lado 44, ventana x  60..104, y 340..384
#   Pulsador P2:  lado 44, ventana x 196..240, y 262..306
#                 (a distinta altura A PROPOSITO: asi la linea que une la
#                  salida de P1 con la entrada de P2 no cruza ninguna caja)
#   Rail de presion y=410 ; fuente: circulo r=11 en (280, 428)
#   Linea de pilotaje: sube por x=330 hasta y=227 y entra por la izquierda
#
# Las cajas de las valvulas SE DESPLAZAN, que es lo que hace el distribuidor
# de verdad: las tuberias no se mueven, se mueve el cuadro que esta en servicio.
# ---------------------------------------------------------------------------
ESCENA_MANDO = u'''
      <div class="escena" id="esc-man">
        <div class="escena-barra">
          <span class="escena-titulo">El mismo cilindro, mandado de cuatro maneras</span>
          <div class="seg" id="seg-man-circ">
            <button type="button" data-c="directo" aria-pressed="true">Mando directo</button>
            <button type="button" data-c="indirecto">Mando indirecto</button>
            <button type="button" data-c="y">Dos manos (Y)</button>
            <button type="button" data-c="o">Cualquiera (O)</button>
          </div>
        </div>
        <div class="escena-barra">
          <div class="seg" id="seg-man-pul">
            <button type="button" data-b="1">Pulsador 1</button>
            <button type="button" data-b="2">Pulsador 2</button>
          </div>
          <div class="seg" id="seg-man-d">
            <button type="button" data-d="32" aria-pressed="true">&Oslash; 32</button>
            <button type="button" data-d="50">&Oslash; 50</button>
            <button type="button" data-d="80">&Oslash; 80</button>
            <button type="button" data-d="100">&Oslash; 100 mm</button>
          </div>
          <label class="ctrl">
            <span>Ciclos por minuto</span>
            <input id="man-c" type="range" min="2" max="60" value="20" step="1">
            <b id="man-c-val">20</b>
          </label>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 450" id="svg-man" role="img"
               aria-label="Circuito neum&aacute;tico con simbolog&iacute;a ISO 1219: cilindro de doble efecto, v&aacute;lvula 5/2 y pulsadores 3/2"></svg>
        </div>
        <div class="pie" id="pie-man"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-man');
        if(!svg) return;
        var pie = document.getElementById('pie-man');
        var segC = document.getElementById('seg-man-circ');
        var segP = document.getElementById('seg-man-pul');
        var segD = document.getElementById('seg-man-d');
        var cIn = document.getElementById('man-c'), cTx = document.getElementById('man-c-val');

        var PRES = 6, CARRERA = 200, F_MUELLE = 4;   /* bar, mm, N del muelle del pulsador */
        var Q_REF = 100, D_REF = 2;                  /* 2 mm de paso -> 100 NL/min a 6 bar */
        var VASTAGO = {32:12, 50:20, 80:25, 100:25};

        var circuito = 'directo', p1 = false, p2 = false, D = 32;
        var pos = 0, raf = null;

        function coma(n, d){ return n.toFixed(d).replace('.', ','); }

        /* --------- la logica: que valvula esta accionada y que linea tiene aire --------- */
        function senal(){
          if(circuito === 'y') return p1 && p2;
          if(circuito === 'o') return p1 || p2;
          return p1;
        }
        function usaP2(){ return circuito === 'y' || circuito === 'o'; }
        function hayPulsadores(){ return circuito !== 'directo'; }

        /* ------------------------- las cuentas ------------------------- */
        function calcula(){
          var d = VASTAGO[D];
          var Aav = Math.PI * D * D / 4;
          var Aret = Math.PI * (D * D - d * d) / 4;
          var vol = (Aav + Aret) * CARRERA / 1e6 * (PRES + 1);   /* NL por ciclo */
          var ciclos = +cIn.value;
          var Q = vol * ciclos;                                   /* NL/min */
          /* el caudal va con el area del paso, asi que el diametro va con su raiz */
          var dPaso = D_REF * Math.sqrt(Q / Q_REF);
          var area = Math.PI * dPaso * dPaso / 4;
          var Fdirecto = PRES * 0.1 * area + F_MUELLE;
          var areaSenal = Math.PI * D_REF * D_REF / 4;
          var Findirecto = PRES * 0.1 * areaSenal + F_MUELLE;
          return {Aav:Aav, Aret:Aret, vol:vol, ciclos:ciclos, Q:Q, dPaso:dPaso,
                  Fdirecto:Fdirecto, Findirecto:Findirecto,
                  Qserie: Q_REF / Math.SQRT2};
        }

        /* ---------------------------- utiles ---------------------------- */
        var AZUL = 'var(--goo-azul)', GRIS = 'var(--line)';
        function caja(x, y, w, h, relleno, borde, grosor){
          return '<rect x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" width="' + w
               + '" height="' + h + '" rx="1.5" fill="' + relleno + '" stroke="' + borde
               + '" stroke-width="' + grosor + '"></rect>';
        }
        function hilo(d, viva, grosor){
          return '<path d="' + d + '" fill="none" stroke="' + (viva ? AZUL : GRIS)
               + '" stroke-width="' + (grosor || (viva ? 2.6 : 1.8))
               + '" stroke-linecap="round" stroke-linejoin="round"></path>';
        }
        function linea(d, color, grosor, guion){
          return '<path d="' + d + '" fill="none" stroke="' + color + '" stroke-width="'
               + grosor + '" stroke-linecap="round"'
               + (guion ? ' stroke-dasharray="' + guion + '"' : '') + '></path>';
        }
        function rot(x, y, txt, est, anchor){
          return '<text x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" class="rotulo-svg"'
               + (anchor ? ' text-anchor="' + anchor + '"' : '')
               + (est ? ' style="' + est + '"' : '') + '>' + txt + '</text>';
        }
        /* flecha de paso dentro de un cuadro de valvula */
        function paso(x1, y1, x2, y2){
          var a = Math.atan2(y2 - y1, x2 - x1);
          var s = linea('M' + x1.toFixed(1) + ' ' + y1.toFixed(1) + ' L' + x2.toFixed(1)
                        + ' ' + y2.toFixed(1), 'var(--ink)', 1.8);
          var L = 7;
          s += '<path d="M' + x2.toFixed(1) + ' ' + y2.toFixed(1)
             + ' L' + (x2 - L * Math.cos(a - 0.45)).toFixed(1) + ' '
             + (y2 - L * Math.sin(a - 0.45)).toFixed(1)
             + ' L' + (x2 - L * Math.cos(a + 0.45)).toFixed(1) + ' '
             + (y2 - L * Math.sin(a + 0.45)).toFixed(1)
             + ' Z" fill="var(--ink)"></path>';
          return s;
        }
        /* via cerrada: la T normalizada */
        function tapada(x, y, haciaArriba){
          var g = haciaArriba ? -11 : 11;
          return linea('M' + x + ' ' + y + ' V' + (y + g), 'var(--ink)', 1.8)
               + linea('M' + (x - 7) + ' ' + (y + g) + ' H' + (x + 7), 'var(--ink)', 1.8);
        }
        function escape(x, y){       /* triangulo de escape a la atmosfera */
          return '<path d="M' + (x - 6) + ' ' + (y + 12) + ' L' + (x + 6) + ' ' + (y + 12)
               + ' L' + x + ' ' + y + ' Z" fill="none" stroke="var(--ink-soft)" stroke-width="1.6"></path>';
        }
        function muelle(x, y, h){    /* muelle a la derecha de la caja */
          var d = 'M' + x + ' ' + (y + h / 2), i;
          for(i = 0; i < 4; i++)
            d += ' l4 -6 l4 6';
          return linea(d, 'var(--ink-soft)', 1.6);
        }
        function pulsadorSim(x, y, h){   /* pulsador: vastago con su seta */
          return linea('M' + x + ' ' + (y + h / 2) + ' H' + (x - 12), 'var(--ink)', 1.8)
               + linea('M' + (x - 12) + ' ' + (y + h / 2 - 7) + ' V' + (y + h / 2 + 7),
                       'var(--ink)', 2.6);
        }
        function pilotoSim(x, y, h){     /* pilotaje neumatico: rectangulo */
          return caja(x - 16, y + h / 2 - 9, 16, 18, 'var(--surface)', 'var(--ink-soft)', 1.6);
        }

        /* Valvula selectora de circuito, la "O" de verdad. Sin ella, dos
           pulsadores 3/2 en paralelo NO hacen la funcion O: el que no esta
           pulsado deja escapar el aire por su via 3. La bola se apoya en la
           entrada que NO tiene presion, y asi la tapa.
           Caja de 56 x 32; entradas abajo en x+14 y x+42; salida arriba. */
        function selectora(x, y, a, b){
          var w = 56, h = 32, cx = x + w / 2;
          var ei = x + 14, ed = x + w - 14;
          var s = caja(x, y, w, h, 'var(--surface)', 'var(--ink)', 1.8);
          s += linea('M' + ei + ' ' + (y + h) + ' V' + (y + h / 2 + 4)
                     + ' H' + ed + ' V' + (y + h), 'var(--ink)', 1.6);
          s += linea('M' + cx + ' ' + (y + h / 2 + 4) + ' V' + y, 'var(--ink)', 1.6);
          var bola = (a && !b) ? ed : ((!a && b) ? ei : cx);
          s += '<circle cx="' + bola + '" cy="' + (y + h / 2 + 4) + '" r="7" '
             + 'fill="var(--surface-2)" stroke="var(--ink)" stroke-width="1.6"></circle>';
          return s;
        }

        function pinta(){
          var r = calcula(), s = '', i;
          var on = senal();
          var S5 = 54, S3 = 44;
          var VX = 420, VY = 200;               /* ventana de la 5/2 */
          var bx = on ? VX : VX - S5;           /* donde empieza la caja de la 5/2 */
          /* camisa x 340..490, embolo de 10 px: recorre de 344 a 476 */
          var xp = 344 + pos * 132;
          var xtip = 500 + (xp - 344);

          /* ===================== el cilindro ===================== */
          s += rot(334, 34, 'CILINDRO DE DOBLE EFECTO \\u00b7 \\u00d8 ' + D + ' mm',
                   'font-size:10px');
          s += caja(340, 56, 150, 48, 'var(--surface)', 'var(--ink-soft)', 1.8);
          s += caja(334, 50, 6, 60, 'var(--surface-2)', 'var(--ink-soft)', 1.6);
          s += caja(490, 50, 6, 60, 'var(--surface-2)', 'var(--ink-soft)', 1.6);
          s += caja(340, 56, xp - 340, 48, on ? 'var(--accent-soft)' : 'var(--surface)', 'none', 0);
          if(!on) s += caja(xp + 10, 56, 490 - (xp + 10), 48, 'var(--accent-soft)', 'none', 0);
          s += caja(xp, 57, 10, 46, 'var(--ink-soft)', 'var(--ink)', 1.5);
          s += caja(xp + 10, 76, xtip - (xp + 10), 8, 'var(--surface-2)', 'var(--ink-soft)', 1.5);
          /* tomas del cilindro */
          s += hilo('M337 110 V132', on);
          s += hilo('M493 110 V132', !on);

          /* lineas de la 5/2 al cilindro: la 4 al fondo, la 2 al lado del vastago */
          s += hilo('M438 200 V150 H337 V132', on);
          s += hilo('M456 200 V170 H493 V132', !on);
          s += rot(348, 146, 'sale', 'font-size:9px;fill:' + (on ? AZUL : 'var(--ink-soft)'));
          s += rot(462, 166, 'entra', 'font-size:9px;fill:' + (!on ? AZUL : 'var(--ink-soft)'));

          /* ==================== la valvula 5/2 ==================== */
          /* el rotulo va abajo a la derecha, que es el unico hueco que no
             cruza ninguna tuberia: la de presion sube por x=447 */
          s += rot(624, 300, 'V\\u00c1LVULA 5/2', 'font-size:10.5px;fill:var(--ink)', 'end');
          s += rot(624, 316, 'es la que mueve el cilindro', 'font-size:9px', 'end');
          /* las dos casillas */
          s += caja(bx, VY, S5, S5, 'var(--surface)', 'var(--ink)', 1.8);
          s += caja(bx + S5, VY, S5, S5, 'var(--surface)', 'var(--ink)', 1.8);
          /* dentro de cada casilla. Casilla IZQUIERDA = accionada (1->4, 2->3);
             casilla DERECHA = reposo (1->2, 4->5). */
          var cI = bx, cD = bx + S5;
          s += paso(cI + S5 / 2, VY + S5, cI + S5 / 3, VY);            /* 1 -> 4 */
          s += paso(cI + 2 * S5 / 3, VY, cI + 5 * S5 / 6, VY + S5);    /* 2 -> 3 */
          s += paso(cD + S5 / 2, VY + S5, cD + 2 * S5 / 3, VY);        /* 1 -> 2 */
          s += paso(cD + S5 / 3, VY, cD + S5 / 6, VY + S5);            /* 4 -> 5 */
          /* accionamiento y muelle, pegados a la caja (se mueven con ella) */
          s += (circuito === 'directo') ? pulsadorSim(bx, VY, S5) : pilotoSim(bx, VY, S5);
          s += muelle(bx + 2 * S5 + 2, VY, S5);
          if(circuito === 'directo')
            s += rot(bx - 16, VY - 6, 'lo aprieta el operario', 'font-size:9px', 'end');

          /* vias externas, que NO se mueven */
          s += hilo('M429 254 V266', false);
          s += escape(429, 266);
          s += hilo('M465 254 V266', false);
          s += escape(465, 266);
          s += hilo('M447 254 V410', true);
          /* los rotulos van al LADO de su via: debajo se confunden, porque las
             tres estan a 18 px unas de otras y la del 1 lleva tuberia */
          s += rot(421, 270, '5', 'font-size:9px', 'end');
          s += rot(453, 294, '1', 'font-size:9px');
          s += rot(473, 270, '3', 'font-size:9px');
          s += rot(432, 196, '4', 'font-size:9px', 'end');
          s += rot(462, 196, '2', 'font-size:9px');

          /* ===================== los pulsadores ===================== */
          function valvula32(VX3, VY3, activa, etiqueta){
            var b = activa ? VX3 : VX3 - S3;
            var t = '';
            t += caja(b, VY3, S3, S3, 'var(--surface)', 'var(--ink)', 1.8);
            t += caja(b + S3, VY3, S3, S3, 'var(--surface)', 'var(--ink)', 1.8);
            /* izquierda = accionada: 1 -> 2, y la 3 tapada */
            t += paso(b + S3 / 4, VY3 + S3, b + S3 / 2, VY3);
            t += tapada(b + 3 * S3 / 4, VY3 + S3, true);
            /* derecha = reposo: 1 tapada, 2 -> 3 */
            t += tapada(b + S3 + S3 / 4, VY3 + S3, true);
            t += paso(b + S3 + S3 / 2, VY3, b + S3 + 3 * S3 / 4, VY3 + S3);
            t += pulsadorSim(b, VY3, S3);
            t += muelle(b + 2 * S3 + 2, VY3, S3);
            t += rot(VX3 + S3 + 14, VY3 - 10, etiqueta, 'font-size:9.5px');
            t += rot(VX3 + S3 / 4 - 11, VY3 + S3 + 13, '1', 'font-size:9px');
            t += rot(VX3 + 3 * S3 / 4 + 9, VY3 + S3 + 13, '3', 'font-size:9px');
            t += rot(VX3 + S3 / 2 + 5, VY3 - 7, '2', 'font-size:9px');
            return t;
          }

          if(hayPulsadores()){
            s += valvula32(60, 340, p1, 'P1 \\u00b7 3/2');
            /* via 1 desde el rail, via 3 al escape, via 2 arriba */
            s += hilo('M71 384 V410', true);
            s += hilo('M93 384 V396', false);
            s += escape(93, 396);

            if(usaP2()){
              s += valvula32(196, 262, p2, 'P2 \\u00b7 3/2');
              s += hilo('M229 306 V318', false);
              s += escape(229, 318);
              if(circuito === 'y'){
                /* en serie: la salida de P1 alimenta la entrada de P2 */
                s += hilo('M82 340 V322 H207 V306', p1);
                s += hilo('M218 262 V240 H330 V227 H' + (bx - 16), p1 && p2);
                s += rot(16, 186, 'en serie: hacen falta LOS DOS', 'font-size:9.5px');
              } else {
                /* En paralelo hace falta la SELECTORA: sin ella, el pulsador
                   que no esta apretado se lleva el aire a la atmosfera por su
                   via 3 y la se\\u00f1al no llega nunca. */
                s += hilo('M207 306 V410', true);
                s += hilo('M82 340 V250 H190 V228', p1);
                s += hilo('M218 262 V228', p2);
                s += selectora(176, 196, p1, p2);
                s += hilo('M204 196 V180 H330 V227 H' + (bx - 16), p1 || p2);
                s += rot(170, 216, 'selectora (funci\\u00f3n O)', 'font-size:9px', 'end');
                s += rot(16, 186, 'en paralelo: basta con UNO', 'font-size:9.5px');
              }
            } else {
              s += hilo('M82 340 V240 H330 V227 H' + (bx - 16), p1);
            }
            s += rot(326, 220, 'l\\u00ednea de mando', 'font-size:9px;fill:'
                     + (on ? AZUL : 'var(--ink-soft)'), 'end');
          }

          /* ================== raíl de presi&oacute;n y fuente ================== */
          /* Sin pulsadores el rail empieza en la propia fuente: si no, el tramo
             sale de longitud cero y la 5/2 se queda dibujada sin conectar. */
          var x0 = hayPulsadores() ? 71 : 280;
          s += hilo('M' + x0 + ' 410 H447', true);
          s += hilo('M280 410 V417', true);
          s += '<circle cx="280" cy="428" r="11" fill="var(--surface)" stroke="' + AZUL
             + '" stroke-width="1.8"></circle>';
          s += '<path d="M274 433 L286 433 L280 421 Z" fill="' + AZUL + '"></path>';
          s += rot(296, 432, 'aire comprimido a ' + PRES + ' bar', 'font-size:9.5px');

          /* estado */
          s += rot(16, 22, on ? 'EL CILINDRO SALE' : 'EL CILINDRO EST\\u00c1 DENTRO',
                   'font-size:11px;fill:' + (on ? AZUL : 'var(--ink-soft)') + ';font-weight:500');
          s += rot(16, 40, hayPulsadores()
                   ? 'pulsa los botones de arriba y mira qu\\u00e9 l\\u00ednea se pone azul'
                   : 'el operario aprieta la propia v\\u00e1lvula de potencia', 'font-size:9.5px');

          /* la cuenta del dedo, dibujada */
          var maxF = Math.max(r.Fdirecto, r.Findirecto, 1);
          s += rot(16, 74, 'FUERZA QUE PIDE EL BOT\\u00d3N', 'font-size:9.5px');
          var bar = function(y, etq, f, color){
            var W = 120;
            var t = rot(16, y - 4, etq, 'font-size:9.5px');
            t += caja(16, y, W, 14, 'var(--surface-2)', 'var(--line)', 1);
            t += caja(16, y, Math.max(2, W * f / maxF), 14, color, color, 1);
            t += rot(142, y + 11, coma(f, 1) + ' N', 'font-size:10.5px;fill:var(--ink)');
            return t;
          };
          s += bar(92, 'mando directo', r.Fdirecto,
                   r.Fdirecto > 15 ? 'var(--goo-rojo)' : 'var(--goo-amarillo)');
          s += bar(132, 'mando indirecto', r.Findirecto, 'var(--goo-verde)');

          svg.innerHTML = s;

          /* ========================== el pie ========================== */
          var nombre = {directo:'Mando directo', indirecto:'Mando indirecto',
                        y:'Dos manos (funci\\u00f3n Y)', o:'Cualquiera (funci\\u00f3n O)'}[circuito];
          var txt = '<b>' + nombre + '.</b> ';
          if(circuito === 'directo')
            txt += 'Solo hay una v&aacute;lvula, y por ella pasa <b>todo el aire del cilindro</b>. '
                 + 'El operario aprieta la v&aacute;lvula de potencia.';
          else if(circuito === 'indirecto')
            txt += 'Hay dos v&aacute;lvulas: una peque&ntilde;a que el operario aprieta y que solo '
                 + 'manda una <b>se&ntilde;al</b>, y la 5/2 de potencia, que est&aacute; al lado del '
                 + 'cilindro y es la que mueve el aire de verdad.';
          else if(circuito === 'y')
            txt += 'Los dos pulsadores est&aacute;n <b>en serie</b>: el aire de mando tiene que '
                 + 'atravesar los dos, as&iacute; que hacen falta las dos manos. Es el circuito de '
                 + 'las prensas, y no est&aacute; para incordiar: est&aacute; para que no tengas una '
                 + 'mano dentro mientras la otra pulsa.';
          else
            txt += 'Los dos pulsadores est&aacute;n <b>en paralelo</b>: con cualquiera de los dos '
                 + 'basta. Es la puerta que se abre desde dentro o desde fuera. F&iacute;jate en la '
                 + 'pieza de en medio: es una <b>v&aacute;lvula selectora</b>, y no es un adorno. '
                 + 'Sin ella, el pulsador que <b>no</b> est&aacute;s apretando conecta la '
                 + 'l&iacute;nea con su escape y <b>el aire se va a la calle</b> antes de llegar a '
                 + 'la 5/2. La bolita de dentro se apoya sola en la entrada sin presi&oacute;n y la '
                 + 'tapa.';

          txt += '<br>Un cilindro de <b>&Oslash; ' + D + '</b> gasta <b>' + coma(r.vol, 2)
               + ' NL por ciclo</b>; a ' + r.ciclos + ' ciclos por minuto pide <b>'
               + coma(r.Q, 0) + ' NL/min</b>. Para pasar ese caudal, una v&aacute;lvula de asiento '
               + 'necesita un paso de <b>' + coma(r.dPaso, 2) + ' mm</b>, y abrir ese paso contra '
               + '6 bar cuesta <b>' + coma(r.Fdirecto, 1) + ' N</b> en el dedo. ';
          if(r.Fdirecto > 15)
            txt += 'Eso son <b>' + coma(r.Fdirecto / 9.81, 1) + ' kg apretando con un dedo</b>, '
                 + 'cientos de veces al d&iacute;a. Con <b>mando indirecto</b>, en cambio, el '
                 + 'operario aprieta siempre la misma v&aacute;lvula de se&ntilde;al: <b>'
                 + coma(r.Findirecto, 1) + ' N</b>, d&eacute; igual el cilindro que haya '
                 + 'detr&aacute;s. <b>Eso</b> es lo que se compra con la segunda v&aacute;lvula.';
          else if(r.Fdirecto > r.Findirecto)
            txt += 'Todav&iacute;a se aprieta con el dedo, y la v&aacute;lvula de se&ntilde;al del '
                 + 'mando indirecto pide <b>' + coma(r.Findirecto, 1) + ' N</b>. Sube el '
                 + 'di&aacute;metro o los ciclos y mira c&oacute;mo se dispara la barra de arriba '
                 + 'mientras la de abajo <b>no se mueve</b>.';
          else
            txt += 'Con un cilindro tan peque&ntilde;o, el mando directo <b>ni siquiera es '
                 + 'duro</b>: cuesta menos que la propia v&aacute;lvula de se&ntilde;al ('
                 + coma(r.Findirecto, 1) + ' N). Aqu&iacute; el indirecto no se pone por la fuerza, '
                 + 'se pone por lo otro: tubos cortos y poder combinar se&ntilde;ales. Sube el '
                 + 'di&aacute;metro a 80 o 100 y vuelve a mirar.';

          if(circuito === 'y')
            txt += ' Ojo a un detalle: dos v&aacute;lvulas en serie estrangulan. Dos pasos iguales '
                 + 'seguidos dejan pasar <b>' + coma(r.Qserie, 0) + ' NL/min</b> en vez de '
                 + Q_REF + ', o sea el <b>71 %</b>. Para una se&ntilde;al da igual; si las pusieras '
                 + 'en la l&iacute;nea de potencia, el cilindro saldr&iacute;a m&aacute;s lento.';

          pie.innerHTML = txt
            + '<br><span style="font-size:12.5px">Los s&iacute;mbolos son los de la <b>ISO 1219</b>: '
            + 'cada cuadrado es una posici&oacute;n de la v&aacute;lvula, y lo que se mueve al accionar '
            + 'no son los tubos, es <b>el cuadro que est&aacute; en servicio</b> &mdash; por eso aqu&iacute; '
            + 'la caja se desliza. La numeraci&oacute;n tambi&eacute;n es la de la norma: <b>1</b> presi&oacute;n, '
            + '<b>2</b> y <b>4</b> trabajo, <b>3</b> y <b>5</b> escapes. La regla del paso '
            + '(un asiento de 2 mm deja pasar unos 100 NL/min a 6 bar, y el caudal va con el '
            + '&aacute;rea) es una <b>regla de tanteo</b> para ver de qu&eacute; tama&ntilde;o es el '
            + 'problema, no un dato de cat&aacute;logo.</span>';
        }

        /* ------------------------- movimiento ------------------------- */
        function anima(){
          var meta = senal() ? 1 : 0;
          var paso = 0.035;
          if(Math.abs(pos - meta) < paso){ pos = meta; pinta(); raf = null; return; }
          pos += (meta > pos ? paso : -paso);
          pinta();
          raf = requestAnimationFrame(anima);
        }
        function arranca(){ if(raf) cancelAnimationFrame(raf); raf = requestAnimationFrame(anima); }

        segC.addEventListener('click', function(e){
          var b = e.target.closest('button[data-c]'); if(!b) return;
          segC.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
          circuito = b.dataset.c;
          p1 = p2 = false;
          segP.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', 'false'); });
          arranca();
        });
        segP.addEventListener('click', function(e){
          var b = e.target.closest('button[data-b]'); if(!b) return;
          if(b.dataset.b === '1') p1 = !p1; else p2 = !p2;
          b.setAttribute('aria-pressed', (b.dataset.b === '1' ? p1 : p2) ? 'true' : 'false');
          arranca();
        });
        segD.addEventListener('click', function(e){
          var b = e.target.closest('button[data-d]'); if(!b) return;
          segD.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
          D = +b.dataset.d;
          pinta();
        });
        cIn.addEventListener('input', function(){ cTx.textContent = cIn.value; pinta(); });

        pinta();
      })();
      </script>
'''
