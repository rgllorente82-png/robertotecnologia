# -*- coding: utf-8 -*-
"""Escenas 3 y 4 de la unidad 2 de 4.o (Diseno y fabricacion).

  UNIONES (S4 del catalogo, sesion 3) compara tres maneras de unir las mismas
              dos piezas: tornillos M3, remaches ciegos y pegado. Para cada
              una calcula la fuerza que aguanta con DOS modos de fallo (el
              elemento de union y el aplastamiento del material alrededor del
              agujero) y se queda con el peor, que es el que manda. Las barras
              del grafico son esa fuerza; la raya roja, la carga que hay que
              aguantar. El coeficiente de seguridad es una division.

  TALLER (S4) fabrica la MISMA tapa de la sesion 1 de tres maneras y calcula,
              para cada una, el material que se gasta, lo que cuesta, el
              tiempo de tus manos, el tiempo de maquina y la tolerancia que
              se puede prometer. El volumen de plastico de la impresion sale
              de sumar tapas, pared y relleno, no de un numero inventado.

Los valores de resistencia de los materiales y las velocidades de corte son
ESTIMACIONES DE TALLER, rotuladas como tales dentro de la escena y en la
pagina. Lo que la escena garantiza es que la cuenta que ensena es la cuenta
que hace.

Prefijos CSS propios: un-, tl-. Ninguno empieza por "test-".
"""

# ==========================================================================
# S3 - Tres uniones para las mismas dos piezas
# ==========================================================================
UNIONES = u'''
      <div class="escena" id="esc-un">
        <div class="escena-barra">
          <span class="escena-titulo">El brazo de la l&aacute;mpara, unido a su base &middot; tres maneras, y la que falla primero</span>
          <div class="seg">
            <button type="button" data-a="reset">Valores de partida</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 690 334" id="svg-un" role="img"
               aria-label="Junta a solape con sus tornillos y comparaci&oacute;n de la fuerza que aguanta cada tipo de uni&oacute;n"></svg>
          <div class="un-mandos">
            <div class="un-fila">
              <label for="un-mat">Material de las dos piezas</label>
              <select id="un-mat">
                <option value="0" selected>PLA impreso en 3D</option>
                <option value="1">Contrachapado</option>
                <option value="2">DM (tablero de fibras)</option>
                <option value="3">Metacrilato</option>
                <option value="4">Aluminio</option>
              </select>
            </div>
            <div class="un-fila">
              <label for="un-t">Espesor de la pieza</label>
              <input type="range" id="un-t" min="2" max="10" step="1" value="3">
              <span class="val" id="un-t-v">3 mm</span>
            </div>
            <div class="un-fila">
              <label for="un-n">Tornillos (o remaches)</label>
              <input type="range" id="un-n" min="1" max="4" step="1" value="2">
              <span class="val" id="un-n-v">2</span>
            </div>
            <div class="un-fila">
              <label for="un-sol">Solape de las dos piezas</label>
              <input type="range" id="un-sol" min="6" max="40" step="1" value="20">
              <span class="val" id="un-sol-v">20 mm</span>
            </div>
            <div class="un-fila">
              <label for="un-f">Lo que tiene que aguantar</label>
              <input type="range" id="un-f" min="10" max="900" step="10" value="150">
              <span class="val" id="un-f-v">150 N</span>
            </div>
          </div>
          <div class="un-tablero">
            <div class="un-caja" id="un-c-tor">
              <h5>Tornillos M3 con tuerca</h5>
              <p class="un-num" id="un-tor-max">&mdash;</p>
              <p class="un-det" id="un-tor-det"></p>
            </div>
            <div class="un-caja" id="un-c-rem">
              <h5>Remaches ciegos &empty;3,2</h5>
              <p class="un-num" id="un-rem-max">&mdash;</p>
              <p class="un-det" id="un-rem-det"></p>
            </div>
            <div class="un-caja" id="un-c-peg">
              <h5>Pegado en todo el solape</h5>
              <p class="un-num" id="un-peg-max">&mdash;</p>
              <p class="un-det" id="un-peg-det"></p>
            </div>
          </div>
          <p class="un-cuenta" id="un-cuenta"></p>
        </div>
        <div class="pie" id="pie-un"></div>
      </div>

      <style>
      .un-mandos{margin-top:10px}
      .un-fila{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:0 0 7px;
        font-family:var(--f-m);font-size:12.5px;color:var(--ink)}
      .un-fila label{min-width:212px}
      .un-fila input[type="range"]{flex:1 1 150px;min-width:120px;accent-color:var(--goo-azul)}
      .un-fila select{flex:1 1 220px;font-family:var(--f-m);font-size:12.5px;padding:5px 7px;
        border:1.5px solid var(--line);border-radius:2px;background:var(--surface);color:var(--ink)}
      .un-fila .val{font-weight:500;color:var(--goo-azul);min-width:62px;text-align:right}
      .un-tablero{display:flex;gap:11px;flex-wrap:wrap;margin-top:12px}
      .un-caja{flex:1 1 200px;min-width:196px;border:1.5px solid var(--line);border-radius:2px;
        padding:11px 13px;background:var(--surface)}
      .un-caja h5{margin:0 0 6px;font:500 11.5px var(--f-m);letter-spacing:.05em;text-transform:uppercase;
        color:var(--ink-soft)}
      .un-caja.aguanta{border-left:5px solid var(--goo-verde)}
      .un-caja.rompe{border-left:5px solid var(--goo-rojo)}
      .un-num{margin:0;font-family:var(--f-m);font-size:21px;font-weight:500;color:var(--ink)}
      .un-det{margin:5px 0 0;font-family:var(--f-m);font-size:11.5px;line-height:1.75;color:var(--ink-soft)}
      .un-det b{color:var(--ink)}
      .un-cuenta{margin:12px 0 0;font-family:var(--f-m);font-size:12.5px;line-height:1.7;color:var(--ink-soft)}
      .un-cuenta b{color:var(--ink)}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-un');
        if(!svg) return;
        var caja = document.getElementById('esc-un');
        var pie  = document.getElementById('pie-un');

        /* ---- los numeros de los materiales ------------------------------
           apl: hasta cuanto aguanta el material el APLASTAMIENTO del borde
                del agujero, en N/mm2 (megapascales).
           peg: lo que aguanta a cortadura una junta pegada con cianoacrilato
                o epoxi sobre ese material, en N/mm2.
           Son ESTIMACIONES DE TALLER, redondeadas, para comparar ordenes de
           magnitud: no son valores de calculo de una norma.               */
        var MAT = [
          {n: 'PLA impreso',   apl: 55,  peg: 6},
          {n: 'contrachapado', apl: 25,  peg: 8},
          {n: 'DM',            apl: 12,  peg: 7},
          {n: 'metacrilato',   apl: 70,  peg: 9},
          {n: 'aluminio',      apl: 180, peg: 12}
        ];

        /* Tornillo M3 de acero clase 4.8: seccion del vastago y limite a
           cortadura que se toma como 0,6 de su resistencia a traccion.    */
        var D_TOR = 3, A_TOR = Math.PI * 9 / 4;          /* 7,07 mm2 */
        var TAU_TOR = 240;                               /* N/mm2 */
        var F_TOR = A_TOR * TAU_TOR;                     /* 1697 N */
        var D_REM = 3.2, F_REM = 700;                    /* remache ciego de aluminio */
        var ANCHO = 20;                                  /* ancho de las piezas, mm */

        var v = {mat: 0, t: 3, n: 2, sol: 20, f: 150};

        function n0(x){ return Math.round(x).toString(); }
        function n1(x){ return x.toFixed(1).replace('.', ','); }

        function calcula(){
          var M = MAT[v.mat];
          var aplTor = M.apl * D_TOR * v.t;              /* por tornillo */
          var aplRem = M.apl * D_REM * v.t;              /* por remache  */
          var tor = v.n * Math.min(F_TOR, aplTor);
          var rem = v.n * Math.min(F_REM, aplRem);
          var area = v.sol * ANCHO;
          var peg = M.peg * area;
          return {M: M, aplTor: aplTor, aplRem: aplRem, tor: tor, rem: rem,
                  peg: peg, area: area,
                  falloTor: (aplTor < F_TOR) ? 'pieza' : 'tornillo',
                  falloRem: (aplRem < F_REM) ? 'pieza' : 'remache'};
        }

        function pinta(){
          var C = calcula();
          var m = '';

          /* =============== la junta, a escala =============== */
          var ESC = 3.6, X0 = 56, LP = 70;      /* dos piezas de 70 mm */
          var total = 2 * LP - v.sol;
          var px = function(mm){ return X0 + mm * ESC; };
          var yT = 34, hT = ANCHO * ESC;

          m += '<text x="' + X0 + '" y="24" class="etq">La junta a solape, a escala &middot; '
             + 'dos piezas de ' + ANCHO + ' mm de ancho y ' + v.t + ' mm de espesor</text>';
          /* pieza de la izquierda */
          m += '<rect x="' + px(0) + '" y="' + yT + '" width="' + (LP * ESC).toFixed(1)
             + '" height="' + hT.toFixed(1) + '" fill="var(--surface-2)" stroke="currentColor"'
             + ' stroke-width="1.4"/>';
          /* pieza de la derecha, desplazada */
          m += '<rect x="' + px(LP - v.sol).toFixed(1) + '" y="' + (yT + 8) + '" width="'
             + (LP * ESC).toFixed(1) + '" height="' + hT.toFixed(1)
             + '" fill="none" stroke="currentColor" stroke-width="1.4" stroke-dasharray="6 3"/>';
          /* el solape */
          m += '<rect x="' + px(LP - v.sol).toFixed(1) + '" y="' + yT + '" width="'
             + (v.sol * ESC).toFixed(1) + '" height="' + hT.toFixed(1)
             + '" fill="#1a73e8" opacity=".14"/>';
          /* los tornillos, repartidos por el solape */
          var k, cy = yT + hT / 2;
          for(k = 0; k < v.n; k++){
            var pos = (LP - v.sol) + v.sol * (k + 1) / (v.n + 1);
            m += '<circle cx="' + px(pos).toFixed(1) + '" cy="' + cy.toFixed(1) + '" r="'
               + (D_TOR / 2 * ESC).toFixed(1) + '" fill="var(--paper)" stroke="#ea4335" stroke-width="2"/>';
          }
          /* las flechas de la carga */
          function flecha(x, dir){
            return '<line x1="' + x + '" y1="' + cy.toFixed(1) + '" x2="' + (x + dir * 34)
                 + '" y2="' + cy.toFixed(1) + '" stroke="#ea4335" stroke-width="2.2"/>'
                 + '<path d="M ' + (x + dir * 34) + ' ' + cy.toFixed(1) + ' l ' + (-dir * 9) + ' -5 l 0 10 Z"'
                 + ' fill="#ea4335"/>';
          }
          m += flecha(px(0), -1) + flecha(+px(total).toFixed(1), 1);
          m += '<text x="' + px(total / 2).toFixed(1) + '" y="' + (yT + hT + 20)
             + '" class="ejeq" text-anchor="middle">solape ' + v.sol + ' mm &middot; &aacute;rea pegada '
             + n0(C.area) + ' mm&sup2;</text>';

          /* =============== las tres barras =============== */
          var BY = 176, ALTO = 26, SEP = 46, BX0 = 190, BX1 = 648;
          var tope = Math.max(C.tor, C.rem, C.peg, v.f) * 1.14;
          var bx = function(F){ return BX0 + (BX1 - BX0) * F / tope; };

          m += '<text x="30" y="156" class="etq">Lo que aguanta cada uni&oacute;n, en newtons</text>';

          function barra(y, rot, F, col){
            var s = '<text x="' + (BX0 - 10) + '" y="' + (y + 17)
                  + '" class="ejeq" text-anchor="end">' + rot + '</text>';
            s += '<rect x="' + BX0 + '" y="' + y + '" width="' + (bx(F) - BX0).toFixed(1)
               + '" height="' + ALTO + '" fill="' + col + '" opacity="'
               + (F >= v.f ? '.78' : '.42') + '"/>';
            s += '<text x="' + (bx(F) + 8).toFixed(1) + '" y="' + (y + 18) + '" class="etq">'
               + n0(F) + ' N</text>';
            return s;
          }
          m += barra(BY, 'tornillos M3 &times; ' + v.n, C.tor, '#1a73e8');
          m += barra(BY + SEP, 'remaches &times; ' + v.n, C.rem, '#34a853');
          m += barra(BY + 2 * SEP, 'pegado', C.peg, '#fbbc04');

          /* la raya de la carga */
          var xf = bx(v.f);
          m += '<line x1="' + xf.toFixed(1) + '" y1="' + (BY - 12) + '" x2="' + xf.toFixed(1)
             + '" y2="' + (BY + 2 * SEP + ALTO + 12) + '" stroke="#ea4335" stroke-width="2"/>'
             + '<text x="' + Math.min(xf, BX1 - 90).toFixed(1) + '" y="' + (BY + 2 * SEP + ALTO + 27)
             + '" class="etq" text-anchor="middle" fill="#ea4335">hay que aguantar ' + v.f
             + ' N</text>';

          svg.innerHTML = m;

          /* ---------------- los numeros ---------------- */
          function pon(idNum, idDet, idCaja, F, texto){
            document.getElementById(idNum).innerHTML = n0(F) + ' N';
            document.getElementById(idDet).innerHTML = texto
              + '<br>Coeficiente de seguridad: <b>' + n1(F / v.f) + '</b>'
              + (F >= v.f ? '' : ' &mdash; <b>no llega</b>');
            var c = document.getElementById(idCaja);
            c.classList.toggle('aguanta', F >= v.f);
            c.classList.toggle('rompe', F < v.f);
          }

          pon('un-tor-max', 'un-tor-det', 'un-c-tor', C.tor,
              'El tornillo aguanta ' + n0(F_TOR) + ' N a cortadura.<br>'
              + 'El ' + C.M.n + ' aguanta ' + C.M.apl + ' &times; ' + D_TOR + ' &times; ' + v.t
              + ' = <b>' + n0(C.aplTor) + ' N</b> antes de que el agujero se ovale.<br>'
              + 'Manda el menor de los dos: falla <b>' + (C.falloTor === 'pieza' ? 'la pieza' : 'el tornillo')
              + '</b>. Con ' + v.n + ': <b>' + n0(C.tor) + ' N</b>.<br>'
              + 'Se desmonta en un minuto y la pieza sale entera.');

          pon('un-rem-max', 'un-rem-det', 'un-c-rem', C.rem,
              'El remache aguanta ' + n0(F_REM) + ' N.<br>'
              + 'El ' + C.M.n + ' aguanta ' + C.M.apl + ' &times; ' + n1(D_REM) + ' &times; ' + v.t
              + ' = <b>' + n0(C.aplRem) + ' N</b>.<br>'
              + 'Manda el menor: falla <b>' + (C.falloRem === 'pieza' ? 'la pieza' : 'el remache')
              + '</b>. Con ' + v.n + ': <b>' + n0(C.rem) + ' N</b>.<br>'
              + 'Para quitarlo hay que <b>taladrarle la cabeza</b>.');

          pon('un-peg-max', 'un-peg-det', 'un-c-peg', C.peg,
              'Aguanta ' + C.M.peg + ' N por cada mm&sup2; pegado.<br>'
              + C.M.peg + ' &times; ' + v.sol + ' &times; ' + ANCHO + ' = <b>' + n0(C.peg) + ' N</b>.<br>'
              + 'No lleva agujeros: <b>no debilita la pieza</b> y reparte la carga por toda el '
              + '&aacute;rea.<br>No se desmonta: para abrirlo hay que <b>romper algo</b>.');

          var mejor = Math.max(C.tor, C.rem, C.peg);
          document.getElementById('un-cuenta').innerHTML =
            '<b>Aplastamiento</b>: &sigma; = F / (d &middot; t). El material cede cuando el borde del '
            + 'agujero no aguanta la presi&oacute;n del tornillo. Por eso el espesor <b>t</b> multiplica '
            + 'y el di&aacute;metro tambi&eacute;n: un tornillo gordo en una pieza fina aguanta lo mismo '
            + 'que uno fino en una gorda. <b>Pegado</b>: &tau; = F / &aacute;rea, y el &aacute;rea crece '
            + 'con el solape, que es gratis. La m&aacute;s fuerte de las tres aqu&iacute; aguanta <b>'
            + n0(mejor) + ' N</b>, ' + n1(mejor / v.f) + ' veces la carga.';

          pie.innerHTML =
            '<b>Baja el espesor a 2 mm y mira qui&eacute;n se cae.</b> El tornillo no se entera: sigue '
            + 'aguantando sus ' + n0(F_TOR) + ' N. El que se rinde es la pieza, porque el agujero se '
            + 'ovala. Y ah&iacute; est&aacute; la moraleja de la sesi&oacute;n: <b>en un proyecto de '
            + 'clase, la uni&oacute;n casi nunca falla por el tornillo</b>. Sube el solape del pegado y '
            + 'mira lo barato que sale ganar fuerza&hellip; y lee la &uacute;ltima l&iacute;nea de esa '
            + 'caja antes de decidirte. Los valores de resistencia son <b>estimaciones de taller</b> '
            + 'para comparar, no datos de una norma de c&aacute;lculo.';
        }

        function refresca(){
          document.getElementById('un-t-v').innerHTML = v.t + ' mm';
          document.getElementById('un-n-v').innerHTML = '' + v.n;
          document.getElementById('un-sol-v').innerHTML = v.sol + ' mm';
          document.getElementById('un-f-v').innerHTML = v.f + ' N';
          pinta();
        }
        ['t', 'n', 'sol', 'f'].forEach(function(clave){
          var r = document.getElementById('un-' + clave);
          r.addEventListener('input', function(){ v[clave] = +r.value; refresca(); });
        });
        var sel = document.getElementById('un-mat');
        sel.addEventListener('change', function(){ v.mat = +sel.value; refresca(); });

        caja.addEventListener('click', function(ev){
          if(!ev.target.closest('button[data-a="reset"]')) return;
          v = {mat: 0, t: 3, n: 2, sol: 20, f: 150};
          sel.value = '0';
          document.getElementById('un-t').value = 3;
          document.getElementById('un-n').value = 2;
          document.getElementById('un-sol').value = 20;
          document.getElementById('un-f').value = 150;
          refresca();
        });

        refresca();
      })();
      </script>
'''


# ==========================================================================
# S4 - La misma tapa, tres maneras de fabricarla
# ==========================================================================
TALLER = u'''
      <div class="escena" id="esc-tl">
        <div class="escena-barra">
          <span class="escena-titulo">La tapa de la sesi&oacute;n 1, fabricada de tres maneras &middot; lo que cuesta, lo que tarda y lo que clava</span>
          <div class="seg">
            <button type="button" data-a="reset">Valores de partida</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 690 430" id="svg-tl" role="img"
               aria-label="La tapa acotada y las barras de tiempo de las tres t&eacute;cnicas de fabricaci&oacute;n"></svg>
          <div class="tl-mandos">
            <div class="tl-fila">
              <label for="tl-l">Largo de la tapa</label>
              <input type="range" id="tl-l" min="110" max="220" step="5" value="120">
              <span class="val" id="tl-l-v">120 mm</span>
            </div>
            <div class="tl-fila">
              <label for="tl-a">Ancho</label>
              <input type="range" id="tl-a" min="30" max="90" step="5" value="60">
              <span class="val" id="tl-a-v">60 mm</span>
            </div>
            <div class="tl-fila">
              <label for="tl-t">Espesor</label>
              <input type="range" id="tl-t" min="2" max="6" step="1" value="3">
              <span class="val" id="tl-t-v">3 mm</span>
            </div>
            <div class="tl-fila">
              <label for="tl-r">Relleno de la impresi&oacute;n 3D</label>
              <input type="range" id="tl-r" min="10" max="100" step="5" value="20">
              <span class="val" id="tl-r-v">20 %</span>
            </div>
          </div>
          <div class="tl-tablero">
            <div class="tl-caja" id="tl-c-mano">
              <h5>Sierra de marqueter&iacute;a y taladro</h5>
              <p class="tl-num" id="tl-mano-n">&mdash;</p>
              <p class="tl-det" id="tl-mano-d"></p>
            </div>
            <div class="tl-caja" id="tl-c-laser">
              <h5>Corte l&aacute;ser</h5>
              <p class="tl-num" id="tl-laser-n">&mdash;</p>
              <p class="tl-det" id="tl-laser-d"></p>
            </div>
            <div class="tl-caja" id="tl-c-3d">
              <h5>Impresi&oacute;n 3D</h5>
              <p class="tl-num" id="tl-3d-n">&mdash;</p>
              <p class="tl-det" id="tl-3d-d"></p>
            </div>
          </div>
          <p class="tl-cuenta" id="tl-cuenta"></p>
        </div>
        <div class="pie" id="pie-tl"></div>
      </div>

      <style>
      .tl-mandos{margin-top:10px}
      .tl-fila{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:0 0 7px;
        font-family:var(--f-m);font-size:12.5px;color:var(--ink)}
      .tl-fila label{min-width:212px}
      .tl-fila input[type="range"]{flex:1 1 150px;min-width:120px;accent-color:var(--goo-azul)}
      .tl-fila .val{font-weight:500;color:var(--goo-azul);min-width:66px;text-align:right}
      .tl-tablero{display:flex;gap:11px;flex-wrap:wrap;margin-top:12px}
      .tl-caja{flex:1 1 200px;min-width:196px;border:1.5px solid var(--line);border-radius:2px;
        padding:11px 13px;background:var(--surface)}
      .tl-caja h5{margin:0 0 6px;font:500 11.5px var(--f-m);letter-spacing:.05em;text-transform:uppercase;
        color:var(--ink-soft)}
      .tl-num{margin:0;font-family:var(--f-m);font-size:20px;font-weight:500;color:var(--ink)}
      .tl-det{margin:5px 0 0;font-family:var(--f-m);font-size:11.5px;line-height:1.75;color:var(--ink-soft)}
      .tl-det b{color:var(--ink)}
      .tl-cuenta{margin:12px 0 0;font-family:var(--f-m);font-size:12.5px;line-height:1.7;color:var(--ink-soft)}
      .tl-cuenta b{color:var(--ink)}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-tl');
        if(!svg) return;
        var caja = document.getElementById('esc-tl');
        var pie  = document.getElementById('pie-tl');

        /* ---- constantes de taller ---------------------------------------
           TODAS son estimaciones nuestras, medidas a ojo en un taller de
           instituto, salvo la densidad del PLA. Sirven para comparar, no
           para presupuestar.                                              */
        var RHO_PLA = 1.24;        /* g/cm3 */
        var EUR_KG = 20;           /* euros el kilo de filamento */
        var EUR_M2_MM = 3;         /* euros el m2 de contrachapado, por mm de espesor */
        var CAUDAL = 8;            /* mm3/s que deposita una impresora de instituto */
        var PARED = 0.8, TAPA = 0.8;
        var MIN_MARCAR = 6, MIN_AGUJERO = 1.5;
        var MIN_LASER = 4, MIN_3D = 5;
        var N_AG = 4, D_AG = 6, PASO = 25;
        var GRUPOS = 10;           /* cuantos grupos se pelean por la impresora */

        var TOL = {mano: 0.5, laser: 0.15, tresd: 0.3};
        var MARGEN_LED = 0.5;      /* (6 - 5) / 2, el de la sesion 1 */
        var TOL_EJE = 0.022;       /* la del agujero que gira justo, sesion 2 */

        var v = {l: 120, a: 60, t: 3, r: 20};

        function n2(x){ return x.toFixed(2).replace('.', ','); }
        function n1(x){ return x.toFixed(1).replace('.', ','); }
        function n0(x){ return Math.round(x).toString(); }

        function calcula(){
          var Apla = v.l * v.a;
          var Aagj = N_AG * Math.PI * D_AG * D_AG / 4;
          var Aneta = Apla - Aagj;
          var Lper = 2 * (v.l + v.a);
          var Lagj = N_AG * Math.PI * D_AG;

          /* --- a mano: se compra el rectangulo entero y se sierra --- */
          var costeTabla = Apla * EUR_M2_MM * v.t / 1e6;
          var vSierra = 80 / v.t;                       /* mm por minuto */
          var manoManos = MIN_MARCAR + Lper / vSierra + N_AG * MIN_AGUJERO;

          /* --- laser: mismo material, la maquina corta todo --- */
          var vLaser = 40 / v.t;                        /* mm por segundo */
          var laserMaq = (Lper + Lagj) / vLaser / 60;   /* minutos */

          /* --- impresion 3D: tapas + pared + relleno --- */
          var hNucleo = Math.max(0, v.t - 2 * TAPA);
          var vSkin = (v.t <= 2 * TAPA ? v.t : 2 * TAPA) * Aneta;
          var Ainterior = Math.max(0, (v.l - 2 * PARED) * (v.a - 2 * PARED));
          var vPared = (Apla - Ainterior) * hNucleo;
          var vRelleno = (v.r / 100) * Math.max(0, Ainterior - Aagj) * hNucleo;
          var vMat = vSkin + vPared + vRelleno;
          var masa = vMat / 1000 * RHO_PLA;
          var coste3d = masa / 1000 * EUR_KG;
          var maq3d = vMat / CAUDAL / 60;

          return {Apla: Apla, Aneta: Aneta, Lper: Lper, Lagj: Lagj,
                  costeTabla: costeTabla, vSierra: vSierra, manoManos: manoManos,
                  vLaser: vLaser, laserMaq: laserMaq,
                  vSkin: vSkin, vPared: vPared, vRelleno: vRelleno, vMat: vMat,
                  masa: masa, coste3d: coste3d, maq3d: maq3d};
        }

        function pinta(){
          var C = calcula();
          var m = '';

          /* =============== la tapa, a escala =============== */
          var ESC = 2.1, X0 = 92, Y0 = 34;
          var px = function(mm){ return X0 + mm * ESC; };
          var py = function(mm){ return Y0 + mm * ESC; };
          var yb = py(v.a);

          m += '<text x="30" y="22" class="etq">La tapa, dibujada a escala &middot; '
             + v.l + ' &times; ' + v.a + ' &times; ' + v.t + ' mm &middot; '
             + N_AG + ' agujeros de &empty;' + D_AG + ' a ' + PASO + ' mm del borde</text>';
          m += '<rect x="' + px(0) + '" y="' + Y0 + '" width="' + (v.l * ESC).toFixed(1)
             + '" height="' + (v.a * ESC).toFixed(1) + '" rx="2" fill="var(--surface-2)"'
             + ' stroke="currentColor" stroke-width="1.5"/>';
          var k, cy = py(v.a / 2);
          for(k = 1; k <= N_AG; k++){
            m += '<circle cx="' + px(k * PASO).toFixed(1) + '" cy="' + cy.toFixed(1) + '" r="'
               + (D_AG / 2 * ESC).toFixed(1) + '" fill="var(--paper)" stroke="#1a73e8" stroke-width="1.8"/>';
          }
          /* la cota del largo, como se aprendio en la sesion 1: desde el borde */
          var yc = yb + 26;
          m += '<line x1="' + px(0) + '" y1="' + yc + '" x2="' + px(v.l).toFixed(1) + '" y2="' + yc
             + '" stroke="currentColor" stroke-width="1.1"/>'
             + '<path d="M ' + (px(0) + 7) + ' ' + (yc - 3) + ' L ' + px(0) + ' ' + yc + ' L '
             + (px(0) + 7) + ' ' + (yc + 3) + ' Z" fill="currentColor"/>'
             + '<path d="M ' + (px(v.l) - 7).toFixed(1) + ' ' + (yc - 3) + ' L ' + px(v.l).toFixed(1)
             + ' ' + yc + ' L ' + (px(v.l) - 7).toFixed(1) + ' ' + (yc + 3) + ' Z" fill="currentColor"/>'
             + '<rect x="' + (px(v.l / 2) - 17).toFixed(1) + '" y="' + (yc - 9)
             + '" width="34" height="13" fill="var(--surface)"/>'
             + '<text x="' + px(v.l / 2).toFixed(1) + '" y="' + (yc + 1)
             + '" class="ejeq" text-anchor="middle">' + v.l + '</text>';

          /* =============== las barras de tiempo =============== */
          /* La altura de la tapa cambia con el ancho, asi que el bloque de
             barras se coloca debajo de donde haya quedado y el viewBox se
             ajusta: sin esto queda un hueco enorme con las tapas estrechas. */
          var ALTO = 24, SEP = 40, BX0 = 208, BX1 = 636;
          var TY = yc + 34, BY = TY + 18;
          var tot = [C.manoManos, MIN_LASER + C.laserMaq, MIN_3D + C.maq3d];
          var tope = Math.max(tot[0], tot[1], tot[2], 130) * 1.1;
          var bx = function(t){ return BX0 + (BX1 - BX0) * t / tope; };

          m += '<text x="30" y="' + TY + '" class="etq">Tiempo hasta tener la pieza, en minutos '
             + '&middot; lleno = tus manos, rayado = la m&aacute;quina sola</text>';

          function barra(y, rot, manos, maquina, col){
            var s = '<text x="' + (BX0 - 10) + '" y="' + (y + 16)
                  + '" class="ejeq" text-anchor="end">' + rot + '</text>';
            s += '<rect x="' + BX0 + '" y="' + y + '" width="' + (bx(manos) - BX0).toFixed(1)
               + '" height="' + ALTO + '" fill="' + col + '" opacity=".8"/>';
            if(maquina > 0){
              s += '<rect x="' + bx(manos).toFixed(1) + '" y="' + y + '" width="'
                 + (bx(manos + maquina) - bx(manos)).toFixed(1) + '" height="' + ALTO
                 + '" fill="' + col + '" opacity=".25" stroke="' + col + '" stroke-width="1.2"/>';
            }
            s += '<text x="' + (bx(manos + maquina) + 8).toFixed(1) + '" y="' + (y + 17)
               + '" class="etq">' + n0(manos + maquina) + ' min</text>';
            return s;
          }
          m += barra(BY, 'a mano', C.manoManos, 0, '#ea4335');
          m += barra(BY + SEP, 'l&aacute;ser', MIN_LASER, C.laserMaq, '#34a853');
          m += barra(BY + 2 * SEP, 'impresi&oacute;n 3D', MIN_3D, C.maq3d, '#1a73e8');

          /* la raya de las dos sesiones de taller */
          var x2 = bx(120), fondo = BY + 2 * SEP + ALTO;
          if(x2 <= BX1){
            m += '<line x1="' + x2.toFixed(1) + '" y1="' + (BY - 12) + '" x2="' + x2.toFixed(1)
               + '" y2="' + (fondo + 10) + '" stroke="currentColor" stroke-width="1.6"'
               + ' stroke-dasharray="5 4" opacity=".6"/>'
               + '<text x="' + x2.toFixed(1) + '" y="' + (fondo + 25)
               + '" class="ejeq" text-anchor="middle">dos sesiones de taller</text>';
          }

          svg.setAttribute('viewBox', '0 0 690 ' + (fondo + 34));
          svg.innerHTML = m;

          /* ---------------- los numeros ---------------- */
          function veredicto(tol){
            return (tol <= MARGEN_LED ? 'el LED de &empty;5 pasa por el agujero de &empty;6'
                                      : '<b>el LED puede no pasar</b>')
                 + '; para el agujero del eje de la sesi&oacute;n 2 (&plusmn;0,022 mm) <b>'
                 + (tol <= TOL_EJE ? 'vale' : 'no llega, ni de lejos') + '</b>';
          }

          document.getElementById('tl-mano-n').innerHTML =
            n2(C.costeTabla) + ' &euro; &middot; ' + n0(C.manoManos) + ' min';
          document.getElementById('tl-mano-d').innerHTML =
            'Material: ' + n0(C.Apla) + ' mm&sup2; de contrachapado de ' + v.t + ' mm = <b>'
            + n2(C.costeTabla) + ' &euro;</b>.<br>'
            + 'Serrar ' + n0(C.Lper) + ' mm a ' + n0(C.vSierra) + ' mm/min = '
            + n0(C.Lper / C.vSierra) + ' min, m&aacute;s ' + MIN_MARCAR + ' de marcar y '
            + N_AG + ' &times; ' + n1(MIN_AGUJERO) + ' de taladrar.<br>'
            + 'Tolerancia: <b>&plusmn;' + n1(TOL.mano) + ' mm</b> &mdash; ' + veredicto(TOL.mano) + '.<br>'
            + 'Dise&ntilde;a con l&iacute;neas rectas: cada curva la pagas con la sierra.';

          document.getElementById('tl-laser-n').innerHTML =
            n2(C.costeTabla) + ' &euro; &middot; ' + n0(MIN_LASER + C.laserMaq) + ' min';
          document.getElementById('tl-laser-d').innerHTML =
            'Mismo material, mismo coste: <b>' + n2(C.costeTabla) + ' &euro;</b>.<br>'
            + 'Corta ' + n0(C.Lper + C.Lagj) + ' mm (contorno y agujeros) a ' + n1(C.vLaser)
            + ' mm/s = <b>' + n1(C.laserMaq) + ' min</b> de m&aacute;quina, m&aacute;s ' + MIN_LASER
            + ' de preparar el archivo.<br>'
            + 'Tolerancia: <b>&plusmn;' + n2(TOL.laser) + ' mm</b> &mdash; ' + veredicto(TOL.laser) + '.<br>'
            + 'Todo tiene que ser <b>plano</b>: no hay rebajes a media altura. Y el haz se come '
            + '~0,2 mm, que hay que descontar del dibujo.';

          document.getElementById('tl-3d-n').innerHTML =
            n2(C.coste3d) + ' &euro; &middot; ' + n0(MIN_3D + C.maq3d) + ' min';
          document.getElementById('tl-3d-d').innerHTML =
            'Pl&aacute;stico: tapas ' + n0(C.vSkin) + ' + pared ' + n0(C.vPared) + ' + relleno '
            + n0(C.vRelleno) + ' = <b>' + n0(C.vMat) + ' mm&sup3;</b> &rarr; ' + n1(C.masa)
            + ' g &rarr; <b>' + n2(C.coste3d) + ' &euro;</b>.<br>'
            + n0(C.vMat) + ' / ' + CAUDAL + ' mm&sup3;/s = <b>' + n0(C.maq3d)
            + ' min</b> de m&aacute;quina. Con ' + GRUPOS + ' grupos y una impresora, la cola es de <b>'
            + n1(C.maq3d * GRUPOS / 60) + ' h</b>.<br>'
            + 'Tolerancia: <b>&plusmn;' + n1(TOL.tresd) + ' mm</b> &mdash; ' + veredicto(TOL.tresd) + '.<br>'
            + 'Puedes hacer formas que no salen de un plano&hellip; pero lo que vuele m&aacute;s de '
            + '45&deg; pide soporte, y los agujeros salen un poco peque&ntilde;os.';

          var pc = 100 * C.vSkin / C.vMat;
          document.getElementById('tl-cuenta').innerHTML =
            '<b>Por qu&eacute; doblar el espesor no dobla el pl&aacute;stico.</b> Las tapas de arriba y '
            + 'de abajo son <b>' + n1(2 * TAPA) + ' mm fijos</b>, se ponga el espesor que se ponga: '
            + 'ahora mismo se llevan el <b id="tl-pc">' + n0(pc) + '</b> % del material. Lo &uacute;nico '
            + 'que crece al engordar la pieza es <b>el trozo de en medio</b>. Dobla el espesor, mira el '
            + 'coste y vuelve. El relleno act&uacute;a <b>solo sobre ese trozo</b>, as&iacute; que en '
            + 'una pieza fina mueve poco y en una gruesa manda. '
            + 'Y ojo a la columna de tolerancia: <b>ninguna de las tres</b> te da la cota del eje que '
            + 'pediste en la sesi&oacute;n 2. Por eso los ejes se compran calibrados y lo que se '
            + 'fabrica es el agujero.';

          pie.innerHTML =
            '<b>La misma pieza, el mismo plano, tres presupuestos distintos.</b> Fíjate en que el '
            + 'l&aacute;ser y la impresora casi no te cuestan <b>tiempo tuyo</b>: te cuestan tiempo de '
            + 'm&aacute;quina, que es otra cosa, porque se comparte. Sube el espesor y mira c&oacute;mo '
            + 'se va la impresi&oacute;n mientras el l&aacute;ser apenas se entera. El deslizador del '
            + 'espesor se para en 6 mm porque una cortadora de instituto no suele pasar de ah&iacute; '
            + 'en contrachapado. Los tiempos y los precios son <b>estimaciones de taller</b>, no un '
            + 'presupuesto.';
        }

        function refresca(){
          document.getElementById('tl-l-v').innerHTML = v.l + ' mm';
          document.getElementById('tl-a-v').innerHTML = v.a + ' mm';
          document.getElementById('tl-t-v').innerHTML = v.t + ' mm';
          document.getElementById('tl-r-v').innerHTML = v.r + ' %';
          pinta();
        }
        ['l', 'a', 't', 'r'].forEach(function(clave){
          var r = document.getElementById('tl-' + clave);
          r.addEventListener('input', function(){ v[clave] = +r.value; refresca(); });
        });

        caja.addEventListener('click', function(ev){
          if(!ev.target.closest('button[data-a="reset"]')) return;
          v = {l: 120, a: 60, t: 3, r: 20};
          document.getElementById('tl-l').value = 120;
          document.getElementById('tl-a').value = 60;
          document.getElementById('tl-t').value = 3;
          document.getElementById('tl-r').value = 20;
          refresca();
        });

        refresca();
      })();
      </script>
'''
