# -*- coding: utf-8 -*-
"""Escenas 7 y 8 de la unidad 2 de 4.o (Diseno y fabricacion).

  CIERRE (S7)  la cadena de cotas del montaje del deposito: el hueco entre los
               dos flancos, el carrete que va dentro y las dos arandelas. La
               escena calcula la COTA DE CIERRE (el juego que queda) sumando y
               restando los nominales, su peor caso sumando TODAS las
               tolerancias, y la dispersion estadistica por la raiz de la suma
               de cuadrados. Ademas MONTA 200 conjuntos con piezas sorteadas
               dentro de su tolerancia y cuenta cuantos no entran y cuantos
               bailan: el sorteo es reproducible, asi que el mismo dato da
               siempre el mismo resultado y se puede comprobar desde fuera.
               Las barras de abajo son la CONTRIBUCION de cada eslabon al
               total, que es lo que dice cual hay que apretar.

  CONTROL (S8) el control dimensional de las seis cotas del soporte, las que
               salieron del modelo de la sesion 5. La escena fabrica las
               piezas con la tecnica elegida -cada una con la dispersion que
               se le prometio al alumno en la sesion 4- mas un desajuste
               sistematico de la maquina, las mide, y para cada cota calcula
               la desviacion, el porcentaje de la tolerancia consumido y el
               veredicto. De ahi salen, escritas solas, las dos frases con las
               que se defiende la pieza, y la comprobacion de si el conjunto
               de la sesion 7 sigue cerrando.

El modelo de fabricacion (desajuste sistematico mas dispersion uniforme) es
una SIMPLIFICACION declarada dentro de la propia escena. Lo que la escena
garantiza es que la cuenta que ensena es la cuenta que hace.

Prefijos CSS propios: ci-, cd-. Ninguno empieza por "test-".
"""

# ==========================================================================
# S7 - La cadena de cotas del montaje
# ==========================================================================
CIERRE = u'''
      <div class="escena" id="esc-ci">
        <div class="escena-barra">
          <span class="escena-titulo">El dep&oacute;sito entre los dos flancos &middot; el juego que queda no lo decide ninguna pieza sola</span>
          <div class="seg">
            <button type="button" data-a="otra">Otra tanda de 200</button>
            <button type="button" data-a="reset">Valores de partida</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 690 434" id="svg-ci" role="img"
               aria-label="El montaje del dep&oacute;sito con sus cuatro medidas, la recta del juego que queda y la contribuci&oacute;n de cada eslab&oacute;n"></svg>
          <div class="ci-mandos">
            <div class="ci-fila">
              <label for="ci-a">Hueco entre flancos &middot; nominal</label>
              <input type="range" id="ci-a" min="2300" max="2450" step="5" value="2360">
              <span class="val" id="ci-a-v">23,60 mm</span>
            </div>
            <div class="ci-fila">
              <label for="ci-t0">&plusmn; del hueco entre flancos</label>
              <input type="range" id="ci-t0" min="2" max="50" step="1" value="20">
              <span class="val" id="ci-t0-v">0,20 mm</span>
            </div>
            <div class="ci-fila">
              <label for="ci-t1">&plusmn; del carrete del dep&oacute;sito (21,60)</label>
              <input type="range" id="ci-t1" min="2" max="50" step="1" value="30">
              <span class="val" id="ci-t1-v">0,30 mm</span>
            </div>
            <div class="ci-fila">
              <label for="ci-t2">&plusmn; de la arandela izquierda (0,80)</label>
              <input type="range" id="ci-t2" min="2" max="50" step="1" value="10">
              <span class="val" id="ci-t2-v">0,10 mm</span>
            </div>
            <div class="ci-fila">
              <label for="ci-t3">&plusmn; de la arandela derecha (0,80)</label>
              <input type="range" id="ci-t3" min="2" max="50" step="1" value="10">
              <span class="val" id="ci-t3-v">0,10 mm</span>
            </div>
          </div>
          <div class="ci-tablero">
            <div class="ci-caja" id="ci-c-nom">
              <h5>La cota de cierre</h5>
              <p class="ci-num" id="ci-nom-n">&mdash;</p>
              <p class="ci-det" id="ci-nom-d"></p>
            </div>
            <div class="ci-caja" id="ci-c-peor">
              <h5>El peor caso</h5>
              <p class="ci-num" id="ci-peor-n">&mdash;</p>
              <p class="ci-det" id="ci-peor-d"></p>
            </div>
            <div class="ci-caja" id="ci-c-mc">
              <h5>200 montajes de verdad</h5>
              <p class="ci-num" id="ci-mc-n">&mdash;</p>
              <p class="ci-det" id="ci-mc-d"></p>
            </div>
          </div>
          <p class="ci-cuenta" id="ci-cuenta"></p>
        </div>
        <div class="pie" id="pie-ci"></div>
      </div>

      <style>
      .ci-mandos{margin-top:10px}
      .ci-fila{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:0 0 7px;
        font-family:var(--f-m);font-size:12.5px;color:var(--ink)}
      .ci-fila label{min-width:258px}
      .ci-fila input[type="range"]{flex:1 1 150px;min-width:120px;accent-color:var(--goo-azul)}
      .ci-fila .val{font-weight:500;color:var(--goo-azul);min-width:76px;text-align:right}
      .ci-tablero{display:flex;gap:11px;flex-wrap:wrap;margin-top:12px}
      .ci-caja{flex:1 1 200px;min-width:198px;border:1.5px solid var(--line);border-radius:2px;
        padding:11px 13px;background:var(--surface)}
      .ci-caja h5{margin:0 0 6px;font:500 11.5px var(--f-m);letter-spacing:.05em;text-transform:uppercase;
        color:var(--ink-soft)}
      #ci-c-nom{border-left:5px solid var(--goo-azul)}
      #ci-c-peor{border-left:5px solid var(--goo-amarillo)}
      .ci-caja.bien{border-left:5px solid var(--goo-verde)}
      .ci-caja.mal{border-left:5px solid var(--goo-rojo)}
      .ci-num{margin:0;font-family:var(--f-m);font-size:20px;font-weight:500;color:var(--ink)}
      .ci-det{margin:5px 0 0;font-family:var(--f-m);font-size:11.5px;line-height:1.75;color:var(--ink-soft)}
      .ci-det b{color:var(--ink)}
      .ci-cuenta{margin:12px 0 0;font-family:var(--f-m);font-size:12.5px;line-height:1.7;color:var(--ink-soft)}
      .ci-cuenta b{color:var(--ink)}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-ci');
        if(!svg) return;
        var caja = document.getElementById('esc-ci');
        var pie  = document.getElementById('pie-ci');

        /* ---- la cadena: cuatro eslabones con su signo -------------------
           Se recorre el montaje de izquierda a derecha. Lo que ABRE hueco
           suma; lo que lo OCUPA resta. La cota de cierre es lo que sobra. */
        var ESL = [
          {n: 'hueco entre flancos',  s: +1, nom: 23.60, tol: 0.20, col: '#1a73e8'},
          {n: 'carrete del dep&oacute;sito', s: -1, nom: 21.60, tol: 0.30, col: '#34a853'},
          {n: 'arandela izquierda',   s: -1, nom: 0.80,  tol: 0.10, col: '#fbbc04'},
          {n: 'arandela derecha',     s: -1, nom: 0.80,  tol: 0.10, col: '#9334e6'}
        ];
        var JMIN_OK = 0.00;      /* por debajo de esto, el carrete no entra   */
        var JMAX_OK = 0.80;      /* por encima, el dep&oacute;sito cabecea y derrama */
        var N_MC = 200;
        var SEMILLA0 = 20260918;

        var v = {a: 23.60, t: [0.20, 0.30, 0.10, 0.10]};
        var semilla = SEMILLA0;

        /* El cero negativo: una resta que da -0,0000001 se escribiria "-0,00",
           que en una pantalla de clase parece un error. Se redondea antes. */
        function z(x){ return Math.abs(x) < 0.0005 ? 0 : x; }
        function m2(x){ return z(x).toFixed(2).replace('.', ','); }

        function calcula(){
          var nom = [v.a, ESL[1].nom, ESL[2].nom, ESL[3].nom], k;
          var J = 0, Tpeor = 0, rss = 0;
          for(k = 0; k < 4; k++){
            J += ESL[k].s * nom[k];
            Tpeor += v.t[k];
            rss += v.t[k] * v.t[k];
          }
          rss = Math.sqrt(rss);

          /* los 200 montajes: cada pieza cae por igual en cualquier punto de
             su tolerancia. El generador es el mismo de la sesion 1, asi que
             la tanda se puede repetir desde fuera y comprobar. */
          var s = semilla, i, j, mal = 0, baila = 0, jj, muestras = [];
          for(i = 0; i < N_MC; i++){
            jj = 0;
            for(j = 0; j < 4; j++){
              s = (s * 1664525 + 1013904223) % 4294967296;
              jj += ESL[j].s * (nom[j] + (s / 4294967296 * 2 - 1) * v.t[j]);
            }
            muestras.push(jj);
            if(jj < JMIN_OK) mal++;
            else if(jj > JMAX_OK) baila++;
          }
          return {J: J, Tpeor: Tpeor, rss: rss, jmax: J + Tpeor, jmin: J - Tpeor,
                  mal: mal, baila: baila, bien: N_MC - mal - baila, muestras: muestras,
                  nom: nom};
        }

        function pinta(){
          var C = calcula();
          var m = '';

          /* ============ arriba: el montaje, a escala ============ */
          var ESC = 13.5, X0 = 96, T_FLANCO = 4, Y0 = 56, ALTO = 66;
          var px = function(mm){ return X0 + mm * ESC; };
          m += '<text x="24" y="24" class="etq">El montaje, a escala &middot; lo que hay, lo que va '
             + 'dentro y lo que sobra</text>';
          /* los dos flancos */
          m += '<rect x="' + px(-T_FLANCO).toFixed(1) + '" y="' + Y0 + '" width="'
             + (T_FLANCO * ESC).toFixed(1) + '" height="' + ALTO
             + '" fill="var(--surface-2)" stroke="currentColor" stroke-width="1.5"/>';
          m += '<rect x="' + px(v.a).toFixed(1) + '" y="' + Y0 + '" width="'
             + (T_FLANCO * ESC).toFixed(1) + '" height="' + ALTO
             + '" fill="var(--surface-2)" stroke="currentColor" stroke-width="1.5"/>';
          /* lo que va dentro, apilado desde la cara interior izquierda */
          var x = 0, k;
          var pila = [ESL[2], ESL[1], ESL[3]];               /* arandela, carrete, arandela */
          var nomPila = [ESL[2].nom, ESL[1].nom, ESL[3].nom];
          for(k = 0; k < 3; k++){
            m += '<rect x="' + px(x).toFixed(1) + '" y="' + (Y0 + 8) + '" width="'
               + (nomPila[k] * ESC).toFixed(1) + '" height="' + (ALTO - 16)
               + '" fill="' + pila[k].col + '" opacity=".28" stroke="' + pila[k].col
               + '" stroke-width="1.4"/>';
            if(nomPila[k] * ESC > 40){
              m += '<text x="' + px(x + nomPila[k] / 2).toFixed(1) + '" y="' + (Y0 + ALTO / 2 + 4)
                 + '" class="ejeq" text-anchor="middle">' + pila[k].n + '</text>';
            }
            x += nomPila[k];
          }
          /* la cota de cierre, lo que sobra al final */
          var jx0 = px(x), jx1 = px(v.a);
          m += '<rect x="' + Math.min(jx0, jx1).toFixed(1) + '" y="' + (Y0 + 8) + '" width="'
             + Math.max(1.5, Math.abs(jx1 - jx0)).toFixed(1) + '" height="' + (ALTO - 16)
             + '" fill="' + (C.J >= JMIN_OK ? '#ea4335' : '#ea4335') + '" opacity=".55"/>';
          m += '<text x="' + ((jx0 + jx1) / 2).toFixed(1) + '" y="' + (Y0 + ALTO + 16)
             + '" class="etq" text-anchor="middle" fill="#ea4335">J = ' + m2(C.J) + '</text>';
          /* la cota del hueco entero */
          m += '<line x1="' + px(0).toFixed(1) + '" y1="' + (Y0 - 12) + '" x2="' + px(v.a).toFixed(1)
             + '" y2="' + (Y0 - 12) + '" stroke="currentColor" stroke-width="1.1"/>'
             + '<text x="' + px(v.a / 2).toFixed(1) + '" y="' + (Y0 - 16)
             + '" class="ejeq" text-anchor="middle">hueco ' + m2(v.a) + '</text>';

          /* ============ en medio: la recta del juego ============ */
          var RY = 188, RX0 = 152, RX1 = 656;
          var lo = Math.min(C.jmin, JMIN_OK) - 0.15, hi = Math.max(C.jmax, JMAX_OK) + 0.15;
          var rx = function(j){ return RX0 + (RX1 - RX0) * (j - lo) / (hi - lo); };
          m += '<text x="24" y="' + (RY - 40) + '" class="etq">Todo lo que puede valer el juego, en '
             + 'mil&iacute;metros</text>';
          /* la ventana en la que el montaje vale */
          m += '<rect x="' + rx(JMIN_OK).toFixed(1) + '" y="' + (RY - 22) + '" width="'
             + (rx(JMAX_OK) - rx(JMIN_OK)).toFixed(1) + '" height="56" fill="#34a853"'
             + ' opacity=".13"/>';
          m += '<text x="' + ((rx(JMIN_OK) + rx(JMAX_OK)) / 2).toFixed(1) + '" y="' + (RY - 26)
             + '" class="ejeq" text-anchor="middle" fill="#34a853">el montaje vale</text>';
          /* el histograma de los 200 */
          var BINS = 44, cuenta = [], b;
          for(b = 0; b < BINS; b++) cuenta.push(0);
          C.muestras.forEach(function(j){
            var i2 = Math.floor((j - lo) / (hi - lo) * BINS);
            if(i2 < 0) i2 = 0; if(i2 >= BINS) i2 = BINS - 1;
            cuenta[i2]++;
          });
          var tope = Math.max.apply(null, cuenta) || 1;
          var anchoB = (RX1 - RX0) / BINS;
          for(b = 0; b < BINS; b++){
            if(!cuenta[b]) continue;
            var jc = lo + (b + 0.5) * (hi - lo) / BINS;
            var h = 34 * cuenta[b] / tope;
            m += '<rect x="' + (RX0 + b * anchoB).toFixed(1) + '" y="' + (RY + 34 - h).toFixed(1)
               + '" width="' + (anchoB - 0.8).toFixed(1) + '" height="' + h.toFixed(1)
               + '" fill="' + (jc < JMIN_OK ? '#ea4335' : (jc > JMAX_OK ? '#fbbc04' : '#34a853'))
               + '" opacity=".8"/>';
          }
          /* la barra del peor caso y la de la raiz de cuadrados */
          m += '<line x1="' + RX0 + '" y1="' + (RY + 34) + '" x2="' + RX1 + '" y2="' + (RY + 34)
             + '" stroke="currentColor" stroke-width="1.2"/>';
          /* Los rotulos van a la izquierda, en el margen: a la derecha la barra
             llega hasta el borde del lienzo y el texto se sale. */
          m += '<rect x="' + rx(C.jmin).toFixed(1) + '" y="' + (RY + 42) + '" width="'
             + (rx(C.jmax) - rx(C.jmin)).toFixed(1) + '" height="11" fill="#fbbc04" opacity=".8"/>';
          m += '<text x="24" y="' + (RY + 51) + '" class="ejeq">peor caso &plusmn;' + m2(C.Tpeor)
             + '</text>';
          m += '<rect x="' + rx(C.J - C.rss).toFixed(1) + '" y="' + (RY + 57) + '" width="'
             + (rx(C.J + C.rss) - rx(C.J - C.rss)).toFixed(1) + '" height="11" fill="#1a73e8"'
             + ' opacity=".8"/>';
          m += '<text x="24" y="' + (RY + 66) + '" class="ejeq">&radic;&Sigma; cuadrados &plusmn;'
             + m2(C.rss) + '</text>';
          /* la raya del nominal y las del cero */
          m += '<line x1="' + rx(C.J).toFixed(1) + '" y1="' + (RY - 22) + '" x2="'
             + rx(C.J).toFixed(1) + '" y2="' + (RY + 70) + '" stroke="#1a73e8" stroke-width="1.6"/>';
          m += '<line x1="' + rx(0).toFixed(1) + '" y1="' + (RY - 22) + '" x2="' + rx(0).toFixed(1)
             + '" y2="' + (RY + 34) + '" stroke="#ea4335" stroke-width="1.4"'
             + ' stroke-dasharray="4 3"/>';
          m += '<text x="' + rx(0).toFixed(1) + '" y="' + (RY + 82)
             + '" class="ejeq" text-anchor="middle">0,00</text>';
          m += '<text x="' + rx(JMAX_OK).toFixed(1) + '" y="' + (RY + 82)
             + '" class="ejeq" text-anchor="middle">' + m2(JMAX_OK) + '</text>';

          /* ============ abajo: qui&eacute;n aporta cu&aacute;nto ============ */
          var CY = 312, PASO = 27, BX0 = 250, BX1 = 620;
          m += '<text x="24" y="' + (CY - 12) + '" class="etq">Cu&aacute;nto pone cada eslab&oacute;n '
             + 'en el juego total</text>';
          for(k = 0; k < 4; k++){
            var pc = 100 * v.t[k] / C.Tpeor;
            var yy = CY + k * PASO;
            m += '<text x="' + (BX0 - 10) + '" y="' + (yy + 13) + '" class="ejeq"'
               + ' text-anchor="end">' + ESL[k].n + ' &plusmn;' + m2(v.t[k]) + '</text>';
            m += '<rect x="' + BX0 + '" y="' + (yy + 2) + '" width="'
               + ((BX1 - BX0) * pc / 100).toFixed(1) + '" height="15" fill="' + ESL[k].col
               + '" opacity=".75"/>';
            m += '<text x="' + (BX0 + (BX1 - BX0) * pc / 100 + 7).toFixed(1) + '" y="' + (yy + 14)
               + '" class="etq">' + pc.toFixed(0) + ' %</text>';
          }

          svg.innerHTML = m;

          /* ============ los numeros ============
             Los que comprueba c2_verifica.py llevan su propio id, para que la
             comprobacion lea EL numero y no el trozo de frase que le toque. */
          document.getElementById('ci-nom-n').innerHTML =
            'J = <span id="ci-j">' + m2(C.J) + '</span> mm';
          document.getElementById('ci-nom-d').innerHTML =
            m2(v.a) + ' &minus; ' + m2(ESL[1].nom) + ' &minus; ' + m2(ESL[2].nom) + ' &minus; '
            + m2(ESL[3].nom) + ' = <b>' + m2(C.J) + '</b><br>'
            + 'Es la <b>cota de cierre</b>: no la dibuja nadie, sale de las otras cuatro.<br>'
            + 'Para que valga tiene que quedar entre <b>' + m2(JMIN_OK) + '</b> (entra) y <b>'
            + m2(JMAX_OK) + '</b> (no cabecea).';

          var cajaP = document.getElementById('ci-c-peor');
          var okPeor = (C.jmin >= JMIN_OK - 1e-9 && C.jmax <= JMAX_OK + 1e-9);
          cajaP.classList.toggle('bien', okPeor);
          cajaP.classList.toggle('mal', !okPeor);
          document.getElementById('ci-peor-n').innerHTML =
            '<span id="ci-jmin">' + m2(C.jmin) + '</span> a <span id="ci-jmax">' + m2(C.jmax)
            + '</span>';
          document.getElementById('ci-peor-d').innerHTML =
            'Las tolerancias <b>se suman todas</b>, tengan el signo que tengan:<br>'
            + m2(v.t[0]) + ' + ' + m2(v.t[1]) + ' + ' + m2(v.t[2]) + ' + ' + m2(v.t[3])
            + ' = <b><span id="ci-tpeor">' + m2(C.Tpeor) + '</span></b><br>J = ' + m2(C.J)
            + ' &plusmn; ' + m2(C.Tpeor) + '<br>'
            + (okPeor ? 'Cae <b>entero</b> dentro de la ventana: vale siempre.'
                      : 'Se sale de la ventana: <b>hay montajes que no valen</b>.');

          var cajaM = document.getElementById('ci-c-mc');
          cajaM.classList.toggle('bien', C.bien === N_MC);
          cajaM.classList.toggle('mal', C.bien !== N_MC);
          document.getElementById('ci-mc-n').innerHTML =
            '<span id="ci-bien">' + C.bien + '</span> de ' + N_MC + ' bien';
          document.getElementById('ci-mc-d').innerHTML =
            '<b><span id="ci-mal">' + C.mal + '</span></b> no entran (J negativo)<br>'
            + '<b><span id="ci-baila">' + C.baila
            + '</span></b> bailan m&aacute;s de ' + m2(JMAX_OK) + '<br>'
            + 'Eso es un <b>' + (100 * (C.mal + C.baila) / N_MC).toFixed(1).replace('.', ',')
            + ' %</b> de piezas a la basura.<br>Cada pieza se sortea dentro de su tolerancia; '
            + 'el sorteo es <b>siempre el mismo</b> hasta que pulses &laquo;otra tanda&raquo;.';

          var peorEsl = 0, kk;
          for(kk = 1; kk < 4; kk++) if(v.t[kk] > v.t[peorEsl]) peorEsl = kk;
          document.getElementById('ci-cuenta').innerHTML =
            'El <b>peor caso</b> supone que las cuatro piezas se van al extremo malo a la vez, y por '
            + 'eso suma las cuatro tolerancias enteras: ' + m2(C.Tpeor) + ' mm. Eso casi nunca pasa, '
            + 'y por eso al lado est&aacute; la <b>ra&iacute;z de la suma de cuadrados</b>: '
            + '&radic;(' + m2(v.t[0]) + '&sup2; + ' + m2(v.t[1]) + '&sup2; + ' + m2(v.t[2])
            + '&sup2; + ' + m2(v.t[3]) + '&sup2;) = <b><span id="ci-rss">' + m2(C.rss)
            + '</span></b>, que es como la mitad. '
            + 'Con los mismos datos, las barras de abajo dicen d&oacute;nde apretar: el que '
            + 'm&aacute;s pone ahora mismo es <b>' + ESL[peorEsl].n + '</b>, con el '
            + (100 * v.t[peorEsl] / C.Tpeor).toFixed(0) + ' % del total.';

          pie.innerHTML =
            '<b>Aprieta las dos arandelas a &plusmn;0,02 y mira lo poco que cambia.</b> Entre las dos '
            + 'ponen menos de la tercera parte del problema, y adem&aacute;s no las fabricas t&uacute;. '
            + 'Ahora aprieta el <b>carrete</b>, que es el que m&aacute;s pesa, o sube el nominal del '
            + 'hueco: ver&aacute;s que subirlo mueve la campana entera a la derecha sin estrecharla, '
            + 'y apretar una tolerancia la estrecha sin moverla. <b>Son dos arreglos distintos para '
            + 'dos problemas distintos</b>, y confundirlos es el error m&aacute;s caro del montaje. '
            + 'Que cada pieza caiga por igual en cualquier punto de su tolerancia es una '
            + '<b>suposici&oacute;n</b>: en un taller de verdad se parecen m&aacute;s a una campana, '
            + 'y entonces los extremos son todav&iacute;a m&aacute;s raros.';
        }

        function refresca(){
          document.getElementById('ci-a-v').innerHTML = m2(v.a) + ' mm';
          var k;
          for(k = 0; k < 4; k++){
            document.getElementById('ci-t' + k + '-v').innerHTML = m2(v.t[k]) + ' mm';
          }
          pinta();
        }

        document.getElementById('ci-a').addEventListener('input', function(){
          v.a = (+this.value) / 100; refresca(); });
        [0, 1, 2, 3].forEach(function(k){
          document.getElementById('ci-t' + k).addEventListener('input', function(){
            v.t[k] = (+this.value) / 100; refresca();
          });
        });

        caja.addEventListener('click', function(ev){
          var b = ev.target.closest('button[data-a]');
          if(!b) return;
          if(b.dataset.a === 'otra'){
            /* El mismo multiplicador que el sorteo: 2^32 * 1103515245 se sale
               del entero exacto de JavaScript (2^53) y el resultado dejaria de
               ser reproducible. Con 1664525 cabe de sobra. */
            semilla = (semilla * 1664525 + 1013904223) % 4294967296;
          } else {
            semilla = SEMILLA0;
            v = {a: 23.60, t: [0.20, 0.30, 0.10, 0.10]};
            document.getElementById('ci-a').value = 2360;
            document.getElementById('ci-t0').value = 20;
            document.getElementById('ci-t1').value = 30;
            document.getElementById('ci-t2').value = 10;
            document.getElementById('ci-t3').value = 10;
          }
          refresca();
        });

        refresca();
      })();
      </script>
'''


# ==========================================================================
# S8 - El control dimensional de la pieza terminada
# ==========================================================================
CONTROL = u'''
      <div class="escena" id="esc-cd">
        <div class="escena-barra">
          <span class="escena-titulo">Las seis cotas del soporte, medidas &middot; lo que pediste, lo que te ha salido y qu&eacute; puedes decir</span>
          <div class="seg">
            <button type="button" data-a="otra">Otra pieza</button>
            <button type="button" data-a="reset">Valores de partida</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 690 400" id="svg-cd" role="img"
               aria-label="Las seis cotas del soporte con su banda de tolerancia y la medida real de cada una"></svg>
          <div class="cd-mandos">
            <div class="cd-fila">
              <label for="cd-tec">C&oacute;mo hab&eacute;is fabricado la pieza</label>
              <select id="cd-tec">
                <option value="0" selected>A mano: sierra, lima y taladro</option>
                <option value="1">Cortadora l&aacute;ser</option>
                <option value="2">Impresora 3D</option>
              </select>
            </div>
            <div class="cd-fila">
              <label for="cd-ses">Desajuste de la m&aacute;quina (va siempre al mismo lado)</label>
              <input type="range" id="cd-ses" min="-50" max="50" step="1" value="0">
              <span class="val" id="cd-ses-v">0,00 mm</span>
            </div>
          </div>
          <div class="cd-tablero">
            <div class="cd-caja" id="cd-c-res">
              <h5>El resultado</h5>
              <p class="cd-num" id="cd-res-n">&mdash;</p>
              <p class="cd-det" id="cd-res-d"></p>
            </div>
            <div class="cd-caja" id="cd-c-frase">
              <h5>Lo que puedes decir, con esos n&uacute;meros</h5>
              <p class="cd-det" id="cd-frase-d"></p>
            </div>
          </div>
          <p class="cd-cuenta" id="cd-cuenta"></p>
        </div>
        <div class="pie" id="pie-cd"></div>
      </div>

      <style>
      .cd-mandos{margin-top:10px}
      .cd-fila{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:0 0 7px;
        font-family:var(--f-m);font-size:12.5px;color:var(--ink)}
      .cd-fila label{min-width:292px}
      .cd-fila input[type="range"]{flex:1 1 150px;min-width:120px;accent-color:var(--goo-azul)}
      .cd-fila select{flex:1 1 230px;font-family:var(--f-m);font-size:12.5px;padding:5px 7px;
        border:1.5px solid var(--line);border-radius:2px;background:var(--surface);color:var(--ink)}
      .cd-fila .val{font-weight:500;color:var(--goo-azul);min-width:72px;text-align:right}
      .cd-tablero{display:flex;gap:11px;flex-wrap:wrap;margin-top:12px}
      .cd-caja{flex:1 1 260px;min-width:250px;border:1.5px solid var(--line);border-radius:2px;
        padding:11px 13px;background:var(--surface)}
      .cd-caja h5{margin:0 0 6px;font:500 11.5px var(--f-m);letter-spacing:.05em;text-transform:uppercase;
        color:var(--ink-soft)}
      #cd-c-frase{border-left:5px solid var(--goo-azul);flex:2 1 340px}
      .cd-caja.bien{border-left:5px solid var(--goo-verde)}
      .cd-caja.mal{border-left:5px solid var(--goo-rojo)}
      .cd-num{margin:0;font-family:var(--f-m);font-size:20px;font-weight:500;color:var(--ink)}
      .cd-det{margin:5px 0 0;font-family:var(--f-m);font-size:11.5px;line-height:1.8;color:var(--ink-soft)}
      .cd-det b{color:var(--ink)}
      .cd-cuenta{margin:12px 0 0;font-family:var(--f-m);font-size:12.5px;line-height:1.7;color:var(--ink-soft)}
      .cd-cuenta b{color:var(--ink)}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-cd');
        if(!svg) return;
        var caja = document.getElementById('esc-cd');
        var pie  = document.getElementById('pie-cd');

        /* Las seis cotas salen del modelo de la sesion 5 con el servo de
           23 mm: agujero 8,30 / canto 3 x 8,30 = 24,90 / flanco 49,80 /
           hueco 23,60 / base 31,60 / eje a 4 + 24,90 = 28,90 del suelo. La
           tolerancia de cada una es la que el grupo escribio en su plano. */
        var CAR = [
          {n: 'hueco entre flancos',        nom: 23.60, tol: 0.20},
          {n: '&empty; del agujero del eje', nom: 8.30,  tol: 0.15},
          {n: 'lado del flanco',            nom: 49.80, tol: 0.30},
          {n: 'espesor del flanco',         nom: 4.00,  tol: 0.20},
          {n: 'altura del eje sobre la base', nom: 28.90, tol: 0.40},
          {n: 'ancho exterior de la base',  nom: 31.60, tol: 0.50}
        ];
        /* la dispersion de cada tecnica es la que se prometio en la S4 */
        var TEC = [
          {n: 'la sierra y la lima', disp: 0.50},
          {n: 'el l&aacute;ser',     disp: 0.15},
          {n: 'la impresora 3D',     disp: 0.30}
        ];
        /* el carrete y las arandelas de la sesion 7, para cerrar el conjunto */
        var CARRETE = 21.60, ARANDELAS = 1.60, JMIN_OK = 0.00, JMAX_OK = 0.80;
        var SEMILLA0 = 20260918;

        var v = {tec: 0, ses: 0.00};
        var semilla = SEMILLA0;

        function z(x){ return Math.abs(x) < 0.0005 ? 0 : x; }
        function m2(x){ return z(x).toFixed(2).replace('.', ','); }
        function s2(x){ return (z(x) >= 0 ? '+' : '&minus;')
          + Math.abs(z(x)).toFixed(2).replace('.', ','); }

        function calcula(){
          var s = semilla, T = TEC[v.tec], filas = [], i, pasan = 0;
          for(i = 0; i < CAR.length; i++){
            s = (s * 1664525 + 1013904223) % 4294967296;
            var u = s / 4294967296 * 2 - 1;
            var real = CAR[i].nom + v.ses + u * T.disp;
            var desv = real - CAR[i].nom;
            var pc = 100 * Math.abs(desv) / CAR[i].tol;
            var ok = Math.abs(desv) <= CAR[i].tol + 1e-12;
            if(ok) pasan++;
            filas.push({i: i, real: real, desv: desv, pc: pc, ok: ok});
          }
          /* la cota de cierre de la sesion 7, con el hueco que de verdad ha salido */
          var J = filas[0].real - CARRETE - ARANDELAS;
          var peor = filas[0], mejor = filas[0];
          for(i = 1; i < filas.length; i++){
            if(filas[i].pc > peor.pc) peor = filas[i];
            if(filas[i].pc < mejor.pc) mejor = filas[i];
          }
          return {T: T, filas: filas, pasan: pasan, J: J, peor: peor, mejor: mejor};
        }

        function pinta(){
          var C = calcula();
          var m = '';
          var X0 = 232, XC = 438, SEMI = 172;    /* el centro y el medio ancho del eje */
          var PASO = 52, Y0 = 56;

          /* Nada de negrita aqu&iacute;: dentro de un &lt;text&gt; de SVG, un &lt;b&gt; no es
             una etiqueta conocida y el navegador NO pinta lo que lleva dentro. */
          m += '<text x="24" y="26" class="etq">Cada cota en su escala: de la raya a la marca hay '
             + 'tres veces su tolerancia</text>';

          C.filas.forEach(function(f, k){
            var c = CAR[f.i], y = Y0 + k * PASO;
            /* El punto se queda dentro del lienzo aunque la desviacion se salga
               de la escala: el tope de la derecha va ANTES de la columna de
               medidas, para no escribir el punto encima del numero. */
            var px = function(d){                     /* d en mm, normalizado a la tolerancia */
              var x = XC + SEMI * d / (3 * c.tol);
              return Math.max(X0 - 10, Math.min(XC + SEMI + 14, x));
            };
            /* el nombre y lo que se pidio */
            m += '<text x="' + (X0 - 14) + '" y="' + (y + 4) + '" class="etq" text-anchor="end">'
               + c.n + '</text>';
            m += '<text x="' + (X0 - 14) + '" y="' + (y + 19) + '" class="ejeq" text-anchor="end">'
               + m2(c.nom) + ' &plusmn; ' + m2(c.tol) + '</text>';
            /* la banda de tolerancia */
            m += '<rect x="' + px(-c.tol).toFixed(1) + '" y="' + (y - 11) + '" width="'
               + (px(c.tol) - px(-c.tol)).toFixed(1) + '" height="26" fill="#34a853"'
               + ' opacity=".14"/>';
            m += '<line x1="' + px(-3 * c.tol).toFixed(1) + '" y1="' + (y + 2) + '" x2="'
               + px(3 * c.tol).toFixed(1) + '" y2="' + (y + 2)
               + '" stroke="currentColor" stroke-width="1" opacity=".55"/>';
            /* el nominal y los dos limites */
            [[-c.tol, '#34a853'], [c.tol, '#34a853']].forEach(function(t){
              m += '<line x1="' + px(t[0]).toFixed(1) + '" y1="' + (y - 11) + '" x2="'
                 + px(t[0]).toFixed(1) + '" y2="' + (y + 15) + '" stroke="' + t[1]
                 + '" stroke-width="1.4"/>';
            });
            m += '<line x1="' + XC + '" y1="' + (y - 13) + '" x2="' + XC + '" y2="' + (y + 17)
               + '" stroke="currentColor" stroke-width="1.2" stroke-dasharray="3 3"/>';
            /* la medida real */
            m += '<circle cx="' + px(f.desv).toFixed(1) + '" cy="' + (y + 2) + '" r="6.5" fill="'
               + (f.ok ? '#34a853' : '#ea4335') + '" id="cd-punto-' + f.i + '"/>';
            m += '<text x="' + (XC + SEMI + 34) + '" y="' + (y + 6) + '" class="etq" id="cd-real-'
               + f.i + '">' + m2(f.real) + '</text>';
          });
          m += '<text x="' + XC + '" y="' + (Y0 + 6 * PASO - 18) + '" class="ejeq"'
             + ' text-anchor="middle">lo pedido</text>';
          m += '<text x="' + (XC + SEMI + 34) + '" y="' + (Y0 - 16) + '" class="ejeq">medido</text>';

          svg.setAttribute('viewBox', '0 0 690 ' + (Y0 + 6 * PASO - 6));
          svg.innerHTML = m;

          /* ============ los numeros ============ */
          var cajaR = document.getElementById('cd-c-res');
          cajaR.classList.toggle('bien', C.pasan === CAR.length);
          cajaR.classList.toggle('mal', C.pasan !== CAR.length);
          document.getElementById('cd-res-n').innerHTML =
            '<span id="cd-pasan">' + C.pasan + '</span> de ' + CAR.length + ' cotas';
          var jOK = (C.J >= JMIN_OK && C.J <= JMAX_OK);
          document.getElementById('cd-res-d').innerHTML =
            'Fabricado con <b>' + C.T.n + '</b>, que dispersa &plusmn;' + m2(C.T.disp)
            + ' mm, y con un desajuste de <b>' + s2(v.ses) + '</b>.<br>'
            + 'La peor: <b>' + CAR[C.peor.i].n + '</b>, ' + s2(C.peor.desv) + ' mm, el <b>'
            + '<span id="cd-peorpc">' + C.peor.pc.toFixed(0) + '</span> %</b> de su tolerancia.<br>'
            + 'Cota de cierre de la sesi&oacute;n 7 con el hueco que ha salido: ' + m2(C.filas[0].real)
            + ' &minus; ' + m2(CARRETE) + ' &minus; ' + m2(ARANDELAS) + ' = <b><span id="cd-j">'
            + m2(C.J) + '</span></b> &rarr; ' + (jOK ? 'el dep&oacute;sito <b>gira</b>.'
                                    : (C.J < JMIN_OK ? '<b>no entra</b>.' : '<b>cabecea</b>.'));

          var p = C.peor, mj = C.mejor;
          document.getElementById('cd-frase-d').innerHTML =
            '&laquo;En <b>' + CAR[p.i].n + '</b> ped&iacute; ' + m2(CAR[p.i].nom) + ' &plusmn; '
            + m2(CAR[p.i].tol) + ' y he medido <b>' + m2(p.real) + '</b>: ' + s2(p.desv)
            + ', el ' + p.pc.toFixed(0) + ' % de la tolerancia. '
            + (p.ok ? 'Pasa' + (p.pc > 70 ? ', pero justo' : ' con margen') + '.'
                    : '<b>No pasa.</b>')
            + ' Lo hicimos con ' + C.T.n + ', que dispersa &plusmn;' + m2(C.T.disp) + ', '
            + (CAR[p.i].tol >= C.T.disp
               ? 'as&iacute; que la cota era alcanzable y el fallo es de ejecuci&oacute;n.'
               : 'as&iacute; que <b>esa cota no se pod&iacute;a cumplir</b> con esa m&aacute;quina: '
                 + 'o la ensancho a &plusmn;' + m2(C.T.disp) + ' o esa cara se hace de otra manera.')
            + '&raquo;<br><br>&laquo;La que mejor ha salido es <b>' + CAR[mj.i].n + '</b>: '
            + s2(mj.desv) + ', el ' + mj.pc.toFixed(0) + ' % de su tolerancia.&raquo;';

          var apretables = CAR.filter(function(c){ return c.tol < C.T.disp; }).length;
          document.getElementById('cd-cuenta').innerHTML =
            'Con ' + C.T.n + ' hay <b>' + apretables + ' de ' + CAR.length + '</b> cotas cuya '
            + 'tolerancia es <b>m&aacute;s estrecha que la dispersi&oacute;n de la m&aacute;quina</b>. '
            + 'Esas no dependen de que tengas buen pulso: salgan como salgan, no puedes prometerlas. '
            + 'El <b>desajuste</b> es otra cosa: mueve todas las medidas al mismo lado, se ve en '
            + 'que los puntos se van todos para el mismo sitio, y <b>se corrige</b> (moviendo el tope, '
            + 'la raya o el cero de la m&aacute;quina). La dispersi&oacute;n no se corrige: se '
            + 'aguanta o se cambia de m&aacute;quina.';

          pie.innerHTML =
            '<b>Mueve el desajuste y mira los seis puntos a la vez.</b> Se van todos al mismo lado: '
            + 'eso es un desajuste, y se arregla en un minuto. Ahora d&eacute;jalo en cero y cambia de '
            + 't&eacute;cnica: los puntos se dispersan m&aacute;s o menos, pero cada uno para donde le '
            + 'da la gana. Eso ya no se arregla apretando nada. Y f&iacute;jate en lo importante para '
            + 'la defensa: <b>lo que se cuenta no es &laquo;nos ha quedado muy bien&raquo;</b>, es '
            + 'ped&iacute; esto, med&iacute; esto, me he desviado esto, y esta es la raz&oacute;n. Las '
            + 'medidas se sortean dentro de la dispersi&oacute;n de la t&eacute;cnica: es un '
            + '<b>modelo</b> de lo que hace un taller, no tus piezas de verdad, que las tienes que '
            + 'medir t&uacute;.';
        }

        function refresca(){
          document.getElementById('cd-ses-v').innerHTML = s2(v.ses).replace('&minus;', '\\u2212')
            + ' mm';
          pinta();
        }

        document.getElementById('cd-tec').addEventListener('change', function(){
          v.tec = +this.value; refresca(); });
        document.getElementById('cd-ses').addEventListener('input', function(){
          v.ses = (+this.value) / 100; refresca(); });

        caja.addEventListener('click', function(ev){
          var b = ev.target.closest('button[data-a]');
          if(!b) return;
          if(b.dataset.a === 'otra'){
            /* El mismo multiplicador que el sorteo: 2^32 * 1103515245 se sale
               del entero exacto de JavaScript (2^53) y el resultado dejaria de
               ser reproducible. Con 1664525 cabe de sobra. */
            semilla = (semilla * 1664525 + 1013904223) % 4294967296;
          } else {
            semilla = SEMILLA0;
            v = {tec: 0, ses: 0.00};
            document.getElementById('cd-tec').value = '0';
            document.getElementById('cd-ses').value = 0;
          }
          refresca();
        });

        refresca();
      })();
      </script>
'''
