# -*- coding: utf-8 -*-
"""Escenas 1 y 2 de la unidad 2 de 4.o (Diseno y fabricacion).

Ninguna es una animacion grabada: las dos CALCULAN, y el numero que sale en
pantalla es el resultado de la cuenta que la escena ensena al lado.

  COTAS (S1)   fabrica la misma tapa dos veces, acotada EN CADENA y acotada
               DESDE UNA REFERENCIA, con el mismo error en cada medida. Los
               cuatro errores de la pieza se sortean con un generador
               reproducible y se ensenan uno a uno: la desviacion del ultimo
               agujero en cadena es la SUMA de los cuatro, y desde referencia
               es solo el suyo. El veredicto (entra el LED de 5 mm por el
               agujero de 6) sale de comparar la desviacion con el margen de
               0,5 mm, no esta escrito a mano.

  AJUSTE (S2)  el eje y el agujero. Con las cuatro desviaciones que se le den,
               calcula juego maximo, juego minimo y de ahi el TIPO de ajuste
               (con juego, indeterminado o con apriete). El diagrama de zonas
               esta a escala de verdad, en micras, con la linea cero en su
               sitio, y la banda de juego es una recta numerica real.

Las clases CSS llevan prefijo propio (ct-, aj-) para no chocar entre ellas ni
con las de la pagina. Ninguna empieza por "test-".
"""

# ==========================================================================
# S1 - La tapa de cuatro agujeros: en cadena y desde una referencia
# ==========================================================================
COTAS = u'''
      <div class="escena" id="esc-ct">
        <div class="escena-barra">
          <span class="escena-titulo">La misma tapa, acotada de dos maneras &middot; el mismo operario, los mismos errores</span>
          <div class="seg">
            <button type="button" data-a="otra" id="ct-otra">Otra pieza</button>
            <button type="button" data-a="peor" id="ct-peor" aria-pressed="false">Peor caso</button>
            <button type="button" data-a="reset">Reiniciar</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 690 422" id="svg-ct" role="img"
               aria-label="La misma tapa acotada en cadena y desde una referencia, con la posici&oacute;n real de los cuatro agujeros"></svg>
          <div class="ct-mandos">
            <div class="ct-fila">
              <label for="ct-e">Lo que te equivocas en <b>cada</b> medida</label>
              <input type="range" id="ct-e" min="5" max="100" step="5" value="20">
              <span class="val" id="ct-e-v">&plusmn;0,20 mm</span>
            </div>
            <p class="ct-err" id="ct-errores"></p>
          </div>
          <div class="ct-tablero">
            <div class="ct-caja ct-cad">
              <h5>Acotada en cadena</h5>
              <p class="ct-num" id="ct-cad-desv">+0,00 mm</p>
              <p class="ct-det" id="ct-cad-det"></p>
            </div>
            <div class="ct-caja ct-ref">
              <h5>Acotada desde el borde</h5>
              <p class="ct-num" id="ct-ref-desv">+0,00 mm</p>
              <p class="ct-det" id="ct-ref-det"></p>
            </div>
          </div>
          <p class="ct-cuenta" id="ct-cuenta"></p>
        </div>
        <div class="pie" id="pie-ct"></div>
      </div>

      <style>
      .ct-mandos{margin-top:10px}
      .ct-fila{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:0 0 8px;
        font-family:var(--f-m);font-size:12.5px;color:var(--ink)}
      .ct-fila label{min-width:250px}
      .ct-fila input[type="range"]{flex:1 1 160px;min-width:130px;accent-color:var(--goo-azul)}
      .ct-fila .val{font-weight:500;color:var(--goo-azul);min-width:88px;text-align:right}
      .ct-err{margin:4px 0 0;font-family:var(--f-m);font-size:12px;line-height:1.7;color:var(--ink-soft)}
      .ct-err b{color:var(--ink)}
      .ct-tablero{display:flex;gap:12px;flex-wrap:wrap;margin-top:12px}
      .ct-caja{flex:1 1 250px;min-width:230px;border:1.5px solid var(--line);border-radius:2px;
        padding:11px 13px;background:var(--surface)}
      .ct-caja h5{margin:0 0 6px;font:500 12px var(--f-m);letter-spacing:.06em;text-transform:uppercase;
        color:var(--ink-soft)}
      .ct-cad{border-left:5px solid var(--goo-rojo)}
      .ct-ref{border-left:5px solid var(--goo-azul)}
      .ct-num{margin:0;font-family:var(--f-m);font-size:24px;font-weight:500;color:var(--ink)}
      .ct-det{margin:5px 0 0;font-family:var(--f-m);font-size:12px;line-height:1.7;color:var(--ink-soft)}
      .ct-det b{color:var(--ink)}
      .ct-cuenta{margin:12px 0 0;font-family:var(--f-m);font-size:12.5px;line-height:1.7;color:var(--ink-soft)}
      .ct-cuenta b{color:var(--ink)}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-ct');
        if(!svg) return;
        var caja = document.getElementById('esc-ct');
        var pie  = document.getElementById('pie-ct');

        /* ---- la pieza, en milimetros -------------------------------------
           La tapa frontal del aviso de aula mal ventilada (proyecto B):
           cuatro agujeros de 6 mm en fila, cada 25 mm, por los que asoman
           tres LED de 5 mm y el pulsador de prueba. Un LED entra por su
           agujero mientras su centro no se desvie mas de (6-5)/2 = 0,5 mm. */
        var LARGO = 120, ALTO = 16, PASO = 25, N = 4;
        var D_AGUJERO = 6, D_LED = 5;
        var MARGEN = (D_AGUJERO - D_LED) / 2;

        var e = 0.20;            /* lo que se equivoca cada medida, en mm */
        var peor = false;
        var semilla = 20260918;
        var dn = [];             /* los cuatro errores, normalizados de -1 a 1 */

        function azar(){
          semilla = (semilla * 1664525 + 1013904223) % 4294967296;
          return semilla / 4294967296;
        }
        function tira(){
          dn = [];
          for(var i = 0; i < N; i++){
            var u = azar() * 2 - 1;
            /* dos decimales, para que el numero que se ensena sea EL que se usa */
            dn.push(Math.round(u * 100) / 100);
          }
        }
        function errores(){
          if(!peor) return dn;
          return [1, 1, 1, 1];      /* todos al mismo lado: el peor caso */
        }

        /* ---- las dos piezas ---------------------------------------------
           En cadena cada cota se mide desde el agujero anterior, asi que el
           error se ARRASTRA: la posicion del agujero k lleva encima la suma
           de los k primeros errores. Desde el borde, cada cota se mide
           siempre desde la misma cara, y cada agujero solo carga el suyo.  */
        function piezas(){
          var d = errores(), cad = [], ref = [], acc = 0, k;
          for(k = 0; k < N; k++){
            acc += d[k] * e;
            cad.push({nom: PASO * (k + 1), real: PASO * (k + 1) + acc, desv: acc});
            ref.push({nom: PASO * (k + 1), real: PASO * (k + 1) + d[k] * e, desv: d[k] * e});
          }
          return {cad: cad, ref: ref};
        }

        function n2(x){ return (x >= 0 ? '+' : '\\u2212') + Math.abs(x).toFixed(2).replace('.', ','); }
        function m2(x){ return x.toFixed(2).replace('.', ','); }

        function pinta(){
          var P = piezas();
          var ESC = 3.8, X0 = 72;                /* px por milimetro, a escala */
          var px = function(mm){ return X0 + mm * ESC; };
          var m = '';

          /* ------------- una regleta, con sus agujeros y su rotulo ------- */
          function regleta(y, datos, rotulo){
            var s = '<text x="' + X0 + '" y="' + (y - 9) + '" class="etq">' + rotulo + '</text>';
            s += '<rect x="' + px(0) + '" y="' + y + '" width="' + (LARGO * ESC).toFixed(1)
               + '" height="' + (ALTO * ESC).toFixed(1) + '" rx="2" fill="var(--surface-2)"'
               + ' stroke="currentColor" stroke-width="1.4" opacity=".9"/>';
            var cy = y + ALTO * ESC / 2, k;
            for(k = 0; k < N; k++){
              /* donde tenia que estar: eje de trazos */
              s += '<line x1="' + px(datos[k].nom).toFixed(1) + '" y1="' + (y - 4)
                 + '" x2="' + px(datos[k].nom).toFixed(1) + '" y2="' + (y + ALTO * ESC + 4)
                 + '" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3" opacity=".5"/>';
              /* donde ha salido: el agujero de verdad */
              var entra = Math.abs(datos[k].desv) <= MARGEN;
              s += '<circle cx="' + px(datos[k].real).toFixed(1) + '" cy="' + cy.toFixed(1)
                 + '" r="' + (D_AGUJERO / 2 * ESC).toFixed(1) + '" fill="var(--paper)" stroke="'
                 + (entra ? '#34a853' : '#ea4335') + '" stroke-width="2"/>';
            }
            return s;
          }

          /* ------------- una cota, con sus flechas y su numero ----------- */
          function cota(x1, x2, y, txt){
            var a = px(x1), b = px(x2);
            return '<line x1="' + a.toFixed(1) + '" y1="' + y + '" x2="' + b.toFixed(1)
                 + '" y2="' + y + '" stroke="currentColor" stroke-width="1.1"/>'
                 + '<path d="M ' + (a + 7).toFixed(1) + ' ' + (y - 3) + ' L ' + a.toFixed(1) + ' ' + y
                 + ' L ' + (a + 7).toFixed(1) + ' ' + (y + 3) + ' Z" fill="currentColor"/>'
                 + '<path d="M ' + (b - 7).toFixed(1) + ' ' + (y - 3) + ' L ' + b.toFixed(1) + ' ' + y
                 + ' L ' + (b - 7).toFixed(1) + ' ' + (y + 3) + ' Z" fill="currentColor"/>'
                 + '<rect x="' + ((a + b) / 2 - 13).toFixed(1) + '" y="' + (y - 9)
                 + '" width="26" height="13" fill="var(--surface)"/>'
                 + '<text x="' + ((a + b) / 2).toFixed(1) + '" y="' + (y + 1)
                 + '" class="ejeq" text-anchor="middle">' + txt + '</text>';
          }

          /* ---- arriba: acotada en cadena ---- */
          m += regleta(28, P.cad, 'Acotada EN CADENA: cada agujero, desde el anterior');
          var k;
          for(k = 0; k < N; k++) m += cota(k * PASO, (k + 1) * PASO, 106, '25');

          /* ---- abajo: acotada desde el borde ---- */
          m += regleta(144, P.ref, 'Acotada DESDE EL BORDE: las cuatro, desde la misma cara');
          for(k = 0; k < N; k++) m += cota(0, (k + 1) * PASO, 222 + k * 16, '' + ((k + 1) * PASO));

          /* ---- el detalle del ultimo agujero, de cerca ---- */
          var LUP = 14;                     /* px por mm en la lupa */
          function lupa(cx, cy, desv, rot, col){
            var entra = Math.abs(desv) <= MARGEN;
            var s = '<text x="' + cx + '" y="' + (cy - 48) + '" class="ejeq" text-anchor="middle">'
                  + rot + '</text>';
            /* donde tenia que estar el agujero */
            s += '<circle cx="' + cx + '" cy="' + cy + '" r="' + (D_AGUJERO / 2 * LUP)
               + '" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3" opacity=".55"/>';
            /* el agujero de verdad, desplazado */
            s += '<circle cx="' + (cx + desv * LUP).toFixed(1) + '" cy="' + cy + '" r="'
               + (D_AGUJERO / 2 * LUP) + '" fill="var(--paper)" stroke="' + col + '" stroke-width="2.2"/>';
            /* el LED, que no se mueve: lo sujeta la placa */
            s += '<circle cx="' + cx + '" cy="' + cy + '" r="' + (D_LED / 2 * LUP)
               + '" fill="' + (entra ? '#34a853' : '#ea4335') + '" opacity=".55"/>';
            s += '<text x="' + cx + '" y="' + (cy + 52) + '" class="etq" text-anchor="middle">'
               + (entra ? 'el LED pasa' : 'el LED no pasa') + '</text>';
            return s;
          }
          m += '<text x="' + X0 + '" y="294" class="etq">El cuarto agujero visto de cerca, a '
             + (LUP / ESC).toFixed(1).replace('.', ',') + ' veces la escala de arriba</text>';
          m += lupa(210, 358, P.cad[N - 1].desv, 'en cadena', '#ea4335');
          m += lupa(480, 358, P.ref[N - 1].desv, 'desde el borde', '#1a73e8');

          svg.innerHTML = m;

          /* ---------------- los numeros ---------------- */
          var d = errores();
          document.getElementById('ct-errores').innerHTML =
            'Los cuatro errores de <b>esta</b> pieza: '
            + d.map(function(x, i){
                return 'e' + (i + 1) + ' = <b id="ct-e' + (i + 1) + '">' + n2(x * e) + '</b>';
              }).join(' &middot; ');

          var cadD = P.cad[N - 1].desv, refD = P.ref[N - 1].desv;
          var cadP = P.cad.filter(function(h){ return Math.abs(h.desv) <= MARGEN; }).length;
          var refP = P.ref.filter(function(h){ return Math.abs(h.desv) <= MARGEN; }).length;

          document.getElementById('ct-cad-desv').innerHTML = n2(cadD) + ' mm';
          document.getElementById('ct-cad-det').innerHTML =
            'El 4.&ordm; agujero lleva encima la <b>suma de los cuatro</b>:<br>'
            + d.map(function(x){ return n2(x * e); }).join(' ') + ' = <b>' + n2(cadD) + ' mm</b>'
            + '<br>Peor caso posible: 4 &times; ' + m2(e) + ' = <b>&plusmn;' + m2(4 * e) + ' mm</b>'
            + '<br>Agujeros que pasan: <b id="ct-cad-pasan">' + cadP + '</b> de 4';

          document.getElementById('ct-ref-desv').innerHTML = n2(refD) + ' mm';
          document.getElementById('ct-ref-det').innerHTML =
            'El 4.&ordm; agujero solo lleva <b>el suyo</b>:<br>'
            + '<b>' + n2(refD) + ' mm</b>'
            + '<br>Peor caso posible: <b>&plusmn;' + m2(e) + ' mm</b>, mida el que mida'
            + '<br>Agujeros que pasan: <b id="ct-ref-pasan">' + refP + '</b> de 4';

          document.getElementById('ct-cuenta').innerHTML =
            'Margen para que el LED pase: (' + D_AGUJERO + ' &minus; ' + D_LED + ') / 2 = <b>'
            + m2(MARGEN) + ' mm</b>. &nbsp;En cadena, el peor caso crece con el n&uacute;mero de cotas '
            + '(<b>n &middot; e</b> = 4 &middot; ' + m2(e) + ' = ' + m2(4 * e) + ' mm); desde el borde '
            + 'se queda en <b>e</b> = ' + m2(e) + ' mm por muchos agujeros que a&ntilde;adas. '
            + 'Al azar no suele salir el peor caso: lo t&iacute;pico es que crezca con la '
            + '<b>ra&iacute;z</b> del n&uacute;mero de cotas, &radic;4 &middot; ' + m2(e) + ' = '
            + m2(2 * e) + ' mm. Sigue siendo el doble.';

          pie.innerHTML =
            '<b>Las dos tapas se han fabricado con el mismo operario y los mismos cuatro errores.</b> '
            + 'Lo &uacute;nico que cambia es desde d&oacute;nde se midi&oacute; cada cota. Pulsa '
            + '&laquo;Otra pieza&raquo; unas cuantas veces: la de la derecha casi siempre pasa y la de '
            + 'la izquierda se cae sola. Sube el error de cada medida hasta que falle tambi&eacute;n la '
            + 'de la derecha, y mira <b>cu&aacute;nto</b> hace falta para eso.';
        }

        caja.addEventListener('click', function(ev){
          var b = ev.target.closest('button[data-a]');
          if(!b) return;
          if(b.dataset.a === 'otra'){
            tira(); pinta();
          } else if(b.dataset.a === 'peor'){
            peor = !peor;
            b.setAttribute('aria-pressed', peor ? 'true' : 'false');
            pinta();
          } else {
            peor = false;
            document.getElementById('ct-peor').setAttribute('aria-pressed', 'false');
            semilla = 20260918;
            var r = document.getElementById('ct-e');
            r.value = 20; e = 0.20;
            document.getElementById('ct-e-v').innerHTML = '&plusmn;0,20 mm';
            tira(); pinta();
          }
        });

        var rango = document.getElementById('ct-e');
        rango.addEventListener('input', function(){
          e = (+rango.value) / 100;
          document.getElementById('ct-e-v').innerHTML = '&plusmn;' + e.toFixed(2).replace('.', ',') + ' mm';
          pinta();
        });

        tira();
        pinta();
      })();
      </script>
'''


# ==========================================================================
# S2 - El eje y el agujero: juego, aprieto y lo que hay en medio
# ==========================================================================
AJUSTE = u'''
      <div class="escena" id="esc-aj">
        <div class="escena-barra">
          <span class="escena-titulo">El eje del dep&oacute;sito y su agujero &middot; mueve las cuatro desviaciones y mira qu&eacute; ajuste sale</span>
          <div class="seg">
            <button type="button" data-a="reset">Valores de partida</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 690 314" id="svg-aj" role="img"
               aria-label="Diagrama de zonas de tolerancia del agujero y del eje, y banda de juego resultante"></svg>
          <div class="aj-mandos">
            <div class="aj-fila">
              <label for="aj-pre">Prueba uno hecho</label>
              <select id="aj-pre">
                <option value="0">Gira suelto (bisagra del dep&oacute;sito)</option>
                <option value="1" selected>Gira justo, sin bailar</option>
                <option value="2">Entra a mano&hellip; o no entra</option>
                <option value="3">A presi&oacute;n: ya no sale</option>
                <option value="4">A ojo, con regla y sierra</option>
              </select>
            </div>
            <div class="aj-fila">
              <label for="aj-d">Medida nominal &empty;</label>
              <input type="range" id="aj-d" min="3" max="20" step="1" value="8">
              <span class="val" id="aj-d-v">8 mm</span>
            </div>
            <div class="aj-dos">
              <div class="aj-grupo aj-ag">
                <h6>El agujero del soporte</h6>
                <div class="aj-fila">
                  <label for="aj-ai">desviaci&oacute;n inferior</label>
                  <input type="range" id="aj-ai" min="-500" max="500" step="5" value="0">
                  <span class="val" id="aj-ai-v">0 &micro;m</span>
                </div>
                <div class="aj-fila">
                  <label for="aj-as">desviaci&oacute;n superior</label>
                  <input type="range" id="aj-as" min="-500" max="500" step="5" value="22">
                  <span class="val" id="aj-as-v">+22 &micro;m</span>
                </div>
              </div>
              <div class="aj-grupo aj-ej">
                <h6>El eje</h6>
                <div class="aj-fila">
                  <label for="aj-ei">desviaci&oacute;n inferior</label>
                  <input type="range" id="aj-ei" min="-500" max="500" step="5" value="-28">
                  <span class="val" id="aj-ei-v">&minus;28 &micro;m</span>
                </div>
                <div class="aj-fila">
                  <label for="aj-es">desviaci&oacute;n superior</label>
                  <input type="range" id="aj-es" min="-500" max="500" step="5" value="-13">
                  <span class="val" id="aj-es-v">&minus;13 &micro;m</span>
                </div>
              </div>
            </div>
          </div>
          <div class="aj-tablero">
            <div class="aj-caja">
              <h5>Lo que puede salir de la m&aacute;quina</h5>
              <p class="aj-det" id="aj-medidas"></p>
            </div>
            <div class="aj-caja" id="aj-caja-v">
              <h5>El ajuste que sale</h5>
              <p class="aj-num" id="aj-tipo">&mdash;</p>
              <p class="aj-det" id="aj-det"></p>
            </div>
          </div>
        </div>
        <div class="pie" id="pie-aj"></div>
      </div>

      <style>
      .aj-mandos{margin-top:10px}
      .aj-fila{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:0 0 7px;
        font-family:var(--f-m);font-size:12.5px;color:var(--ink)}
      .aj-fila label{min-width:168px}
      .aj-fila input[type="range"]{flex:1 1 130px;min-width:110px;accent-color:var(--goo-azul)}
      .aj-fila select{flex:1 1 200px;font-family:var(--f-m);font-size:12.5px;padding:5px 7px;
        border:1.5px solid var(--line);border-radius:2px;background:var(--surface);color:var(--ink)}
      .aj-fila .val{font-weight:500;color:var(--goo-azul);min-width:74px;text-align:right}
      .aj-dos{display:flex;gap:12px;flex-wrap:wrap;margin-top:6px}
      .aj-grupo{flex:1 1 300px;min-width:270px;border:1.5px solid var(--line);border-radius:2px;
        padding:10px 12px;background:var(--surface)}
      .aj-grupo h6{margin:0 0 7px;font:500 11.5px var(--f-m);letter-spacing:.07em;text-transform:uppercase;
        color:var(--ink-soft)}
      .aj-ag{border-left:5px solid var(--goo-azul)}
      .aj-ej{border-left:5px solid var(--goo-rojo)}
      .aj-tablero{display:flex;gap:12px;flex-wrap:wrap;margin-top:12px}
      .aj-caja{flex:1 1 260px;min-width:240px;border:1.5px solid var(--line);border-radius:2px;
        padding:11px 13px;background:var(--surface)}
      .aj-caja h5{margin:0 0 6px;font:500 12px var(--f-m);letter-spacing:.06em;text-transform:uppercase;
        color:var(--ink-soft)}
      .aj-num{margin:0;font-family:var(--f-m);font-size:19px;font-weight:500;color:var(--ink);line-height:1.3}
      .aj-det{margin:5px 0 0;font-family:var(--f-m);font-size:12px;line-height:1.75;color:var(--ink-soft)}
      .aj-det b{color:var(--ink)}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-aj');
        if(!svg) return;
        var caja = document.getElementById('esc-aj');
        var pie  = document.getElementById('pie-aj');

        /* Todo se lleva en MICRAS (milesimas de milimetro) porque es donde
           viven las tolerancias de verdad, y se ensena en mm donde hace
           falta leerlo como una medida.                                    */
        var v = {d: 8, ai: 0, as: 22, ei: -28, es: -13};

        var PRE = [
          {n: 'suelto',  ai: 0, as: 58, ei: -80, es: -40},
          {n: 'justo',   ai: 0, as: 22, ei: -28, es: -13},
          {n: 'dudoso',  ai: 0, as: 15, ei: 0,   es: 9},
          {n: 'apriete', ai: 0, as: 15, ei: 23,  es: 32},
          {n: 'a ojo',   ai: -500, as: 500, ei: -500, es: 500}
        ];

        function mm(um){ return (um / 1000).toFixed(3).replace('.', ','); }
        function um(x){ return (x >= 0 ? '+' : '\\u2212') + Math.abs(Math.round(x)); }

        /* ---- la cuenta entera, que es toda la sesion -------------------- */
        function calcula(){
          var agMin = v.d * 1000 + v.ai, agMax = v.d * 1000 + v.as;
          var ejMin = v.d * 1000 + v.ei, ejMax = v.d * 1000 + v.es;
          var jMax = agMax - ejMin;          /* agujero mas grande, eje mas fino */
          var jMin = agMin - ejMax;          /* agujero mas pequeno, eje mas gordo */
          var tipo, clase;
          if(jMin > 0){ tipo = 'Con juego'; clase = 'juego'; }
          else if(jMax < 0){ tipo = 'Con apriete'; clase = 'apriete'; }
          else { tipo = 'Indeterminado'; clase = 'dudoso'; }
          return {agMin: agMin, agMax: agMax, ejMin: ejMin, ejMax: ejMax,
                  jMax: jMax, jMin: jMin, tipo: tipo, clase: clase,
                  tAg: v.as - v.ai, tEj: v.es - v.ei};
        }

        function pinta(){
          var C = calcula();
          var m = '';

          /* =============== diagrama de zonas, en micras =============== */
          var Y0 = 100;                       /* la linea cero */
          var tope = Math.max(Math.abs(v.ai), Math.abs(v.as),
                              Math.abs(v.ei), Math.abs(v.es), 20);
          var ESC = 58 / tope;                /* px por micra */
          var py = function(u){ return Y0 - u * ESC; };

          m += '<text x="30" y="18" class="etq">Zonas de tolerancia, en micras (mil&eacute;simas de mil&iacute;metro)</text>';
          /* la linea cero */
          m += '<line x1="30" y1="' + Y0 + '" x2="660" y2="' + Y0
             + '" stroke="currentColor" stroke-width="1.6"/>'
             + '<text x="660" y="' + (Y0 - 6) + '" class="ejeq" text-anchor="end">l&iacute;nea cero &middot; &empty; '
             + v.d + ',000 mm</text>';

          function zona(x, w, a, b, col, rot, med1, med2){
            var y1 = py(Math.max(a, b)), y2 = py(Math.min(a, b));
            var h = Math.max(3, y2 - y1);
            return '<rect x="' + x + '" y="' + y1.toFixed(1) + '" width="' + w + '" height="'
                 + h.toFixed(1) + '" fill="' + col + '" opacity=".28" stroke="' + col
                 + '" stroke-width="1.8"/>'
                 + '<text x="' + (x + w / 2) + '" y="' + (py(Math.max(a, b)) - 8).toFixed(1)
                 + '" class="ejeq" text-anchor="middle">' + um(Math.max(a, b)) + ' &micro;m</text>'
                 + '<text x="' + (x + w / 2) + '" y="' + (py(Math.min(a, b)) + 15).toFixed(1)
                 + '" class="ejeq" text-anchor="middle">' + um(Math.min(a, b)) + ' &micro;m</text>'
                 + '<text x="' + (x + w / 2) + '" y="190" class="etq" text-anchor="middle">' + rot + '</text>'
                 + '<text x="' + (x + w / 2) + '" y="204" class="ejeq" text-anchor="middle">' + med1 + '</text>'
                 + '<text x="' + (x + w / 2) + '" y="218" class="ejeq" text-anchor="middle">' + med2 + '</text>';
          }
          m += zona(120, 180, v.ai, v.as, '#1a73e8', 'EL AGUJERO',
                    'de ' + mm(C.agMin) + ' mm', 'a ' + mm(C.agMax) + ' mm');
          m += zona(392, 180, v.ei, v.es, '#ea4335', 'EL EJE',
                    'de ' + mm(C.ejMin) + ' mm', 'a ' + mm(C.ejMax) + ' mm');

          /* =============== la banda de juego, recta numerica =============== */
          var BX0 = 120, BX1 = 620, BY = 272;
          var lim = Math.max(Math.abs(C.jMax), Math.abs(C.jMin), 10) * 1.25;
          var bx = function(u){ return (BX0 + BX1) / 2 + u / lim * (BX1 - BX0) / 2; };

          m += '<text x="30" y="250" class="etq">El juego que sale: de ' + um(C.jMin)
             + ' a ' + um(C.jMax) + ' &micro;m</text>';
          m += '<line x1="' + BX0 + '" y1="' + BY + '" x2="' + BX1 + '" y2="' + BY
             + '" stroke="currentColor" stroke-width="1" opacity=".45"/>';
          /* el cero, que es la frontera entre entrar y no entrar */
          m += '<line x1="' + bx(0).toFixed(1) + '" y1="' + (BY - 26) + '" x2="' + bx(0).toFixed(1)
             + '" y2="' + (BY + 16) + '" stroke="currentColor" stroke-width="1.4" stroke-dasharray="5 3"/>'
             + '<text x="' + bx(0).toFixed(1) + '" y="' + (BY + 30)
             + '" class="ejeq" text-anchor="middle">0 &micro;m</text>';
          var col = C.clase === 'juego' ? '#34a853' : (C.clase === 'apriete' ? '#1a73e8' : '#fbbc04');
          var x1 = bx(Math.min(C.jMin, C.jMax)), x2 = bx(Math.max(C.jMin, C.jMax));
          m += '<rect x="' + x1.toFixed(1) + '" y="' + (BY - 16) + '" width="'
             + Math.max(3, x2 - x1).toFixed(1) + '" height="20" fill="' + col + '" opacity=".75"/>';
          /* los dos extremos no se rotulan: el titulo de arriba ya dice los dos
             numeros, y con la banda estrecha se pisaban entre ellos. */
          m += '<text x="' + (BX0 - 6) + '" y="' + (BY + 4) + '" class="ejeq" text-anchor="end">aprieta</text>'
             + '<text x="' + (BX1 + 6) + '" y="' + (BY + 4) + '" class="ejeq">baila</text>';

          svg.innerHTML = m;

          /* ---------------- los numeros ---------------- */
          document.getElementById('aj-medidas').innerHTML =
            '<b>Agujero</b>: de ' + mm(C.agMin) + ' a ' + mm(C.agMax) + ' mm '
            + '&nbsp;(tolerancia ' + Math.round(C.tAg) + ' &micro;m)<br>'
            + '<b>Eje</b>: de ' + mm(C.ejMin) + ' a ' + mm(C.ejMax) + ' mm '
            + '&nbsp;(tolerancia ' + Math.round(C.tEj) + ' &micro;m)<br>'
            + 'Juego m&aacute;ximo = ' + mm(C.agMax) + ' &minus; ' + mm(C.ejMin)
            + ' = <b id="aj-jmax">' + um(C.jMax) + '</b> &micro;m<br>'
            + 'Juego m&iacute;nimo = ' + mm(C.agMin) + ' &minus; ' + mm(C.ejMax)
            + ' = <b id="aj-jmin">' + um(C.jMin) + '</b> &micro;m<br>'
            + 'Y f&iacute;jate: ' + um(C.jMax) + ' &minus; (' + um(C.jMin)
            + ') = <b id="aj-suma">' + Math.round(C.jMax - C.jMin) + '</b> &micro;m, que es justo '
            + Math.round(C.tAg) + ' + ' + Math.round(C.tEj) + '.';

          var t = document.getElementById('aj-tipo');
          t.innerHTML = C.tipo;
          t.style.color = col;
          var txt;
          if(C.clase === 'juego'){
            txt = 'El agujero es <b>siempre</b> mayor que el eje, salgan como salgan. '
                + 'Entra sin forzar y gira. Cuanto m&aacute;s juego, m&aacute;s baila: con '
                + um(C.jMax) + ' &micro;m en el peor caso, el dep&oacute;sito se mueve '
                + mm(C.jMax) + ' mm antes de que el eje toque.';
          } else if(C.clase === 'apriete'){
            txt = 'El eje es <b>siempre</b> mayor que el agujero. No entra a mano: hay que meterlo a '
                + 'presi&oacute;n o enfriar el eje. Una vez dentro, no se mueve nunca m&aacute;s&hellip; '
                + 'y para sacarlo, o lo rompes o lo calientas.';
          } else {
            txt = '<b>Unas veces entra suelto y otras aprieta</b>, y no puedes saber cu&aacute;l te va a '
                + 'tocar hasta que la tengas en la mano. Es el peor sitio donde estar: el mismo plano '
                + 'da piezas que giran y piezas que no. Si quieres que gire, baja el eje; si quieres que '
                + 'no se mueva, s&uacute;belo. Lo que no vale es quedarse aqu&iacute; sin saberlo.';
          }
          document.getElementById('aj-det').innerHTML = txt;

          pie.innerHTML =
            '<b>Ninguna m&aacute;quina fabrica un 8,000.</b> Lo que fabrica es algo entre dos '
            + 'n&uacute;meros, y esos dos n&uacute;meros los eliges t&uacute;. El ajuste no vive en el '
            + 'eje ni en el agujero: vive en <b>la pareja</b>. Prueba el &uacute;ltimo preajuste, el de '
            + 'la regla y la sierra: es el que ten&eacute;is en el taller, y explica por qu&eacute; el '
            + 'eje de un proyecto de clase casi nunca se fabrica &mdash;se compra una varilla calibrada&mdash; '
            + 'y lo que se ajusta es el agujero.';
        }

        function mando(id, clave){
          var r = document.getElementById(id);
          r.addEventListener('input', function(){
            v[clave] = +r.value;
            refresca();
          });
        }
        function refresca(){
          document.getElementById('aj-d-v').innerHTML = v.d + ' mm';
          document.getElementById('aj-ai-v').innerHTML = um(v.ai) + ' &micro;m';
          document.getElementById('aj-as-v').innerHTML = um(v.as) + ' &micro;m';
          document.getElementById('aj-ei-v').innerHTML = um(v.ei) + ' &micro;m';
          document.getElementById('aj-es-v').innerHTML = um(v.es) + ' &micro;m';
          document.getElementById('aj-d').value = v.d;
          document.getElementById('aj-ai').value = v.ai;
          document.getElementById('aj-as').value = v.as;
          document.getElementById('aj-ei').value = v.ei;
          document.getElementById('aj-es').value = v.es;
          pinta();
        }
        mando('aj-d', 'd');
        mando('aj-ai', 'ai');
        mando('aj-as', 'as');
        mando('aj-ei', 'ei');
        mando('aj-es', 'es');

        var sel = document.getElementById('aj-pre');
        sel.addEventListener('change', function(){
          var p = PRE[+sel.value];
          v.ai = p.ai; v.as = p.as; v.ei = p.ei; v.es = p.es;
          refresca();
        });

        caja.addEventListener('click', function(ev){
          var b = ev.target.closest('button[data-a="reset"]');
          if(!b) return;
          sel.value = '1';
          v = {d: 8, ai: 0, as: 22, ei: -28, es: -13};
          refresca();
        });

        refresca();
      })();
      </script>
'''
