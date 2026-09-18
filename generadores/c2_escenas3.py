# -*- coding: utf-8 -*-
"""Escenas 5 y 6 de la unidad 2 de 4.o (Diseno y fabricacion).

Las dos CALCULAN. Ningun numero de los que salen en pantalla esta escrito a
mano en ningun sitio: todos son el resultado de la cuenta que la escena ensena
justo al lado.

  MODELO (S5)  el soporte del deposito del riego, modelado DOS VECES sobre los
               mismos cinco parametros: el "modelo vivo", donde cada medida se
               deduce de los parametros con una formula, y el "modelo tonto",
               donde las medidas se escribieron a mano el primer dia y ahi se
               han quedado. Mueve un parametro y la escena recalcula la cadena
               entera del vivo, congela el tonto y mide la INTERFERENCIA que
               aparece entre los dos, en milimetros.
               Ademas modela lo que le pasa al agujero al exportarlo a STL: el
               circulo se convierte en un poligono INSCRITO de N lados, asi que
               el diametro que de verdad deja pasar es D*cos(pi/N). De ahi sale
               la holgura real, y tambien el numero minimo de facetas que hace
               falta para que el eje entre, que es ceil(pi/arccos(ds/D)).

  CORTE (S6)   el plan de corte del despiece completo del riego sobre tableros
               de verdad. Empaqueta las piezas con un algoritmo de estantes
               (mayor altura primero, primer hueco que sirva), descontando la
               SANGRIA de la herramienta entre pieza y pieza, y calcula cuantos
               tableros hacen falta, el aprovechamiento, lo que se tira y lo
               que cuesta. Y compara cortar los N grupos juntos frente a darle
               un tablero a cada uno, que es la moraleja de la sesion.

Los precios y las velocidades de corte son ESTIMACIONES DE TALLER, rotuladas
como tales dentro de la escena. Lo que la escena garantiza es que la cuenta que
ensena es la cuenta que hace.

Prefijos CSS propios: md-, co-. Ninguno empieza por "test-".
"""

# ==========================================================================
# S5 - El soporte del deposito, modelado por parametros
# ==========================================================================
MODELO = u'''
      <div class="escena" id="esc-md">
        <div class="escena-barra">
          <span class="escena-titulo">El soporte del dep&oacute;sito &middot; el mismo modelo con par&aacute;metros y con n&uacute;meros a mano</span>
          <div class="seg">
            <button type="button" data-a="servo">Llega el servo de verdad</button>
            <button type="button" data-a="reset">Valores de partida</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 690 452" id="svg-md" role="img"
               aria-label="El flanco del soporte con su agujero facetado, el conjunto montado con el servo dentro y la cadena de medidas que se deducen unas de otras"></svg>
          <div class="md-mandos">
            <div class="md-fila">
              <label for="md-ds">&empty; del eje que hab&eacute;is comprado</label>
              <input type="range" id="md-ds" min="4" max="12" step="1" value="8">
              <span class="val" id="md-ds-v">8 mm</span>
            </div>
            <div class="md-fila">
              <label for="md-hol">Holgura de montaje que pides</label>
              <input type="range" id="md-hol" min="10" max="100" step="5" value="30">
              <span class="val" id="md-hol-v">0,30 mm</span>
            </div>
            <div class="md-fila">
              <label for="md-as">Ancho del servo que va dentro</label>
              <input type="range" id="md-as" min="15" max="40" step="1" value="20">
              <span class="val" id="md-as-v">20 mm</span>
            </div>
            <div class="md-fila">
              <label for="md-t">Espesor del tablero</label>
              <input type="range" id="md-t" min="2" max="8" step="1" value="4">
              <span class="val" id="md-t-v">4 mm</span>
            </div>
            <div class="md-fila">
              <label for="md-n">Facetas del c&iacute;rculo al exportar el STL</label>
              <input type="range" id="md-n" min="0" max="7" step="1" value="3">
              <span class="val" id="md-n-v">16</span>
            </div>
          </div>
          <div class="md-tablero">
            <div class="md-caja md-vivo">
              <h5>Modelo vivo &middot; cada medida es una f&oacute;rmula</h5>
              <p class="md-num" id="md-vivo-n">&mdash;</p>
              <p class="md-det" id="md-vivo-d"></p>
            </div>
            <div class="md-caja md-tonto">
              <h5>Modelo tonto &middot; medidas escritas a mano</h5>
              <p class="md-num" id="md-tonto-n">&mdash;</p>
              <p class="md-det" id="md-tonto-d"></p>
            </div>
            <div class="md-caja md-stl">
              <h5>Al exportarlo a STL</h5>
              <p class="md-num" id="md-stl-n">&mdash;</p>
              <p class="md-det" id="md-stl-d"></p>
            </div>
          </div>
          <p class="md-cuenta" id="md-cuenta"></p>
        </div>
        <div class="pie" id="pie-md"></div>
      </div>

      <style>
      .md-mandos{margin-top:10px}
      .md-fila{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:0 0 7px;
        font-family:var(--f-m);font-size:12.5px;color:var(--ink)}
      .md-fila label{min-width:262px}
      .md-fila input[type="range"]{flex:1 1 150px;min-width:120px;accent-color:var(--goo-azul)}
      .md-fila .val{font-weight:500;color:var(--goo-azul);min-width:72px;text-align:right}
      .md-tablero{display:flex;gap:11px;flex-wrap:wrap;margin-top:12px}
      .md-caja{flex:1 1 200px;min-width:198px;border:1.5px solid var(--line);border-radius:2px;
        padding:11px 13px;background:var(--surface)}
      .md-caja h5{margin:0 0 6px;font:500 11.5px var(--f-m);letter-spacing:.05em;text-transform:uppercase;
        color:var(--ink-soft)}
      .md-vivo{border-left:5px solid var(--goo-verde)}
      .md-tonto{border-left:5px solid var(--goo-rojo)}
      .md-stl{border-left:5px solid var(--goo-amarillo)}
      .md-num{margin:0;font-family:var(--f-m);font-size:20px;font-weight:500;color:var(--ink)}
      .md-det{margin:5px 0 0;font-family:var(--f-m);font-size:11.5px;line-height:1.75;color:var(--ink-soft)}
      .md-det b{color:var(--ink)}
      .md-cuenta{margin:12px 0 0;font-family:var(--f-m);font-size:12.5px;line-height:1.7;color:var(--ink-soft)}
      .md-cuenta b{color:var(--ink)}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-md');
        if(!svg) return;
        var caja = document.getElementById('esc-md');
        var pie  = document.getElementById('pie-md');

        /* ---- los cinco parametros ---------------------------------------
           ds  diametro del eje que se COMPRA calibrado (S2: el agujero se
               mueve, el eje no)
           hol holgura de montaje que se le pide al agujero
           as  ancho del servo que va metido entre los dos flancos
           t   espesor del tablero
           n   facetas con las que se exporta el circulo a STL            */
        var FACETAS = [6, 8, 12, 16, 24, 32, 48, 64];
        var INI = {ds: 8, hol: 0.30, as: 20, t: 4, ni: 3};
        var v = {ds: 8, hol: 0.30, as: 20, t: 4, ni: 3};

        /* ---- el modelo vivo: siete medidas, todas deducidas -------------
           D      diametro del agujero      = eje + holgura
           borde  distancia del centro al canto = 3 diametros. La regla de la
                  sesion 3 pide 2 en plastico o metal y 3 EN MADERA O TABLERO,
                  y el soporte es de contrachapado: manda el 3.
           W = H  lado del flanco           = 2 veces esa distancia
           hueco  hueco interior            = servo + 2 holguras
           B      ancho exterior de la base = hueco + 2 espesores
           Lb     largo de la base          = lado del flanco + 20 de reborde
           Lv     largo de la varilla       = ancho exterior + 10 de saliente  */
        function vivo(p){
          var D = p.ds + p.hol;
          var borde = 3 * D;
          var W = 2 * borde;
          var hueco = p.as + 2 * p.hol;
          var B = hueco + 2 * p.t;
          return {D: D, borde: borde, W: W, H: W, hueco: hueco, B: B,
                  Lb: W + 20, Lv: B + 10};
        }
        var TONTO = vivo(INI);        /* las medidas del primer dia, congeladas */

        /* El cero negativo: una resta que da -0,0000001 se escribiria "-0,00",
           que en una pantalla de clase parece un error. Se redondea antes. */
        function z(x){ return Math.abs(x) < 0.0005 ? 0 : x; }
        function m1(x){ return z(x).toFixed(1).replace('.', ','); }
        function m2(x){ return z(x).toFixed(2).replace('.', ','); }
        function s2(x){ return (z(x) >= 0 ? '+' : '&minus;')
          + Math.abs(z(x)).toFixed(2).replace('.', ','); }

        function calcula(){
          var V = vivo(v), N = FACETAS[v.ni];
          /* cuantas de las siete medidas deducidas se han movido */
          var claves = ['D', 'borde', 'W', 'hueco', 'B', 'Lb', 'Lv'], movidas = 0, k;
          for(k = 0; k < claves.length; k++){
            if(Math.abs(V[claves[k]] - TONTO[claves[k]]) > 1e-9) movidas++;
          }
          /* las dos interferencias del modelo tonto: las piezas ya estan
             cortadas con las medidas viejas y ahora no admiten lo de hoy */
          var intServo = V.hueco - TONTO.hueco;      /* >0: el servo no entra */
          var intEje = v.ds - TONTO.D;               /* >0: el eje no pasa    */
          var bordeTonto = (TONTO.W - TONTO.D) / 2;  /* lo que queda de canto */
          /* el agujero exportado: poligono INSCRITO de N lados */
          var cosf = Math.cos(Math.PI / N);
          var Def = V.D * cosf;                      /* lo que de verdad pasa */
          var flecha = V.D / 2 * (1 - cosf);         /* material que sobra    */
          var holReal = Def - v.ds;
          /* facetas minimas para que el eje entre: D*cos(pi/N) >= ds */
          var r = v.ds / V.D, nmin;
          nmin = (r >= 1) ? Infinity : Math.ceil(Math.PI / Math.acos(r));
          if(nmin < 3) nmin = 3;
          return {V: V, N: N, movidas: movidas, intServo: intServo, intEje: intEje,
                  bordeTonto: bordeTonto, Def: Def, flecha: flecha, holReal: holReal,
                  nmin: nmin};
        }

        function poligono(cx, cy, r, N, giro){
          var p = [], k, a;
          for(k = 0; k < N; k++){
            a = giro + 2 * Math.PI * k / N;
            p.push((cx + r * Math.cos(a)).toFixed(2) + ',' + (cy + r * Math.sin(a)).toFixed(2));
          }
          return p.join(' ');
        }

        function pinta(){
          var C = calcula(), V = C.V;
          var m = '';
          var ESC = 3.0;                      /* px por mm, FIJO: las piezas crecen */

          /* ============ izquierda: el flanco, de frente ============ */
          var FX = 62, FY = 44;
          m += '<text x="24" y="26" class="etq">El flanco, a escala fija</text>';
          m += '<rect x="' + FX + '" y="' + FY + '" width="' + (V.W * ESC).toFixed(1)
             + '" height="' + (V.H * ESC).toFixed(1) + '" rx="2" fill="var(--surface-2)"'
             + ' stroke="currentColor" stroke-width="1.5"/>';
          var fcx = FX + V.W * ESC / 2, fcy = FY + V.H * ESC / 2;
          /* el agujero ideal, a trazos, y el poligono que de verdad se exporta */
          m += '<circle cx="' + fcx.toFixed(1) + '" cy="' + fcy.toFixed(1) + '" r="'
             + (V.D / 2 * ESC).toFixed(2) + '" fill="none" stroke="currentColor"'
             + ' stroke-width="1" stroke-dasharray="4 3" opacity=".6"/>';
          m += '<polygon points="' + poligono(fcx, fcy, V.D / 2 * ESC, C.N, -Math.PI / 2)
             + '" fill="var(--paper)" stroke="#1a73e8" stroke-width="1.8"/>';
          /* las dos cotas del canto */
          /* El numero va a la IZQUIERDA de la linea de cota: con el eje mas fino
             la pieza se encoge y, puesto a la derecha, el numero le caia encima. */
          function cotaV(x, y1, y2, txt){
            return '<line x1="' + x + '" y1="' + y1 + '" x2="' + x + '" y2="' + y2
                 + '" stroke="currentColor" stroke-width="1"/>'
                 + '<text x="' + (x - 4) + '" y="' + ((y1 + y2) / 2 + 4)
                 + '" class="ejeq" text-anchor="end">' + txt + '</text>';
          }
          m += cotaV(FX - 12, FY, fcy, m1(V.borde));
          m += '<line x1="' + (FX - 17) + '" y1="' + FY + '" x2="' + (FX - 7) + '" y2="' + FY
             + '" stroke="currentColor" stroke-width="1"/>';
          m += '<text x="24" y="' + (FY + V.H * ESC + 18) + '" class="ejeq">lado ' + m1(V.W)
             + ' &middot; &empty; ' + m2(V.D) + ' &middot; canto ' + m1(V.borde) + '</text>';

          /* ============ derecha: el conjunto, de frente ============ */
          var CX = 300, CY0 = 44;
          m += '<text x="290" y="26" class="etq">El conjunto montado &middot; a trazos, lo ya '
             + 'cortado</text>';
          var altoV = v.t + V.H, altoT = INI.t + TONTO.H;
          var base = CY0 + Math.max(altoV, altoT) * ESC;      /* el suelo comun */
          /* las piezas del modelo TONTO, a trazos */
          m += '<rect x="' + CX + '" y="' + (base - INI.t * ESC).toFixed(1) + '" width="'
             + (TONTO.B * ESC).toFixed(1) + '" height="' + (INI.t * ESC).toFixed(1)
             + '" fill="none" stroke="#ea4335" stroke-width="1.3" stroke-dasharray="5 3"/>';
          m += '<rect x="' + CX + '" y="' + (base - (INI.t + TONTO.H) * ESC).toFixed(1)
             + '" width="' + (INI.t * ESC).toFixed(1) + '" height="' + (TONTO.H * ESC).toFixed(1)
             + '" fill="none" stroke="#ea4335" stroke-width="1.3" stroke-dasharray="5 3"/>';
          m += '<rect x="' + (CX + (TONTO.B - INI.t) * ESC).toFixed(1) + '" y="'
             + (base - (INI.t + TONTO.H) * ESC).toFixed(1) + '" width="' + (INI.t * ESC).toFixed(1)
             + '" height="' + (TONTO.H * ESC).toFixed(1)
             + '" fill="none" stroke="#ea4335" stroke-width="1.3" stroke-dasharray="5 3"/>';
          /* las piezas del modelo VIVO, macizas */
          m += '<rect x="' + CX + '" y="' + (base - v.t * ESC).toFixed(1) + '" width="'
             + (V.B * ESC).toFixed(1) + '" height="' + (v.t * ESC).toFixed(1)
             + '" fill="var(--surface-2)" stroke="currentColor" stroke-width="1.5"/>';
          var k2;
          for(k2 = 0; k2 < 2; k2++){
            m += '<rect x="' + (CX + k2 * (V.B - v.t) * ESC).toFixed(1) + '" y="'
               + (base - (v.t + V.H) * ESC).toFixed(1) + '" width="' + (v.t * ESC).toFixed(1)
               + '" height="' + (V.H * ESC).toFixed(1)
               + '" fill="var(--surface-2)" stroke="currentColor" stroke-width="1.5"/>';
          }
          /* el eje, atravesando los dos flancos */
          var ejeY = base - (v.t + V.H / 2) * ESC;
          m += '<rect x="' + (CX - 5 * ESC).toFixed(1) + '" y="' + (ejeY - v.ds / 2 * ESC).toFixed(1)
             + '" width="' + (V.Lv * ESC).toFixed(1) + '" height="' + (v.ds * ESC).toFixed(1)
             + '" rx="1.5" fill="#1a73e8" opacity=".55"/>';
          /* El servo de verdad, apoyado en la base y metido en el hueco que ya
             esta cortado: su cara izquierda deja la holgura contra el flanco
             izquierdo, que es como se monta. Su cara derecha puede llegar como
             mucho hasta el flanco de la derecha menos otra holgura; lo que
             pase de ahi es la INTERFERENCIA, y mide exactamente lo mismo que
             la cuenta de la caja: hueco que pide - hueco que hay. */
          var sAl = 0.85 * v.as, sIzq = INI.t + v.hol, sDer = sIzq + v.as;
          var sLim = INI.t + TONTO.hueco - v.hol;
          var sx = CX + sIzq * ESC;
          m += '<rect x="' + sx.toFixed(1) + '" y="' + (base - (v.t + sAl) * ESC).toFixed(1)
             + '" width="' + (v.as * ESC).toFixed(1) + '" height="' + (sAl * ESC).toFixed(1)
             + '" fill="#34a853" opacity=".3" stroke="#34a853" stroke-width="1.5"/>';
          m += '<text x="' + (sx + v.as * ESC / 2).toFixed(1) + '" y="'
             + (base - (v.t + sAl / 2) * ESC + 4).toFixed(1)
             + '" class="ejeq" text-anchor="middle">servo</text>';
          if(C.intServo > 1e-9){
            m += '<rect x="' + (CX + sLim * ESC).toFixed(1) + '" y="'
               + (base - (v.t + sAl) * ESC).toFixed(1) + '" width="'
               + ((sDer - sLim) * ESC).toFixed(1) + '" height="' + (sAl * ESC).toFixed(1)
               + '" fill="#ea4335" opacity=".5"/>';
            m += '<text x="' + (CX + TONTO.B * ESC / 2).toFixed(1) + '" y="' + (base + 20)
               + '" class="etq" text-anchor="middle" fill="#ea4335">no entra por '
               + m1(C.intServo) + ' mm</text>';
          }
          m += '<text x="290" y="' + (base + 38) + '" class="ejeq">vivo: base de ' + m1(V.B)
             + ' &times; ' + m1(V.Lb) + ' &middot; cortado: ' + m1(TONTO.B) + ' &times; '
             + m1(TONTO.Lb) + '</text>';

          /* ============ abajo a la izquierda: el agujero de cerca ============
             La mitad de abajo empieza donde acaba el conjunto, que crece con
             los parametros. Para que no quede un agujero blanco en medio (ni
             se salga por abajo con los valores grandes), el alto del viewBox
             se recalcula tambien. */
          var YB = base + 74;
          var LUP = 110 / V.D, lx = 118, ly = YB + 74;
          m += '<text x="24" y="' + YB + '" class="ejeq">El agujero exportado, a '
             + Math.round(LUP / ESC) + ' aumentos</text>';
          m += '<circle cx="' + lx + '" cy="' + ly + '" r="' + (V.D / 2 * LUP).toFixed(1)
             + '" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="5 4"'
             + ' opacity=".6"/>';
          m += '<polygon points="' + poligono(lx, ly, V.D / 2 * LUP, C.N, -Math.PI / 2)
             + '" fill="var(--paper)" stroke="#1a73e8" stroke-width="2"/>';
          m += '<circle cx="' + lx + '" cy="' + ly + '" r="' + (v.ds / 2 * LUP).toFixed(1)
             + '" fill="' + (C.holReal >= 0 ? '#34a853' : '#ea4335') + '" opacity=".45"/>';
          m += '<text x="' + lx + '" y="' + (ly + V.D / 2 * LUP + 20).toFixed(1)
             + '" class="etq" text-anchor="middle">' + (C.holReal >= 0 ? 'el eje pasa'
             : 'el eje NO pasa') + '</text>';

          /* ============ abajo a la derecha: la cadena de medidas ============ */
          m += '<text x="290" y="' + YB + '" class="ejeq">De d&oacute;nde sale cada medida</text>';
          var CADENA = [
            ['&empty; eje ' + m1(v.ds) + ' + holgura ' + m2(v.hol), '&empty; agujero = ' + m2(V.D)],
            ['&empty; agujero &times; 3 (en tablero)', 'canto = ' + m1(V.borde)],
            ['canto &times; 2', 'lado del flanco = ' + m1(V.W)],
            ['servo ' + v.as + ' + 2 holguras', 'hueco = ' + m1(V.hueco)],
            ['hueco + 2 espesores', 'ancho de la base = ' + m1(V.B)]
          ];
          var cy0 = YB + 10, i2;
          for(i2 = 0; i2 < CADENA.length; i2++){
            var yy = cy0 + i2 * 27;
            m += '<text x="292" y="' + (yy + 11) + '" class="ejeq">' + CADENA[i2][0] + '</text>';
            m += '<path d="M 494 ' + (yy + 7) + ' L 512 ' + (yy + 7) + ' M 506 ' + (yy + 3)
               + ' L 512 ' + (yy + 7) + ' L 506 ' + (yy + 11) + '" fill="none"'
               + ' stroke="var(--goo-verde)" stroke-width="1.6"/>';
            m += '<text x="518" y="' + (yy + 11) + '" class="etq">' + CADENA[i2][1] + '</text>';
          }

          svg.setAttribute('viewBox', '0 0 690 '
            + Math.ceil(Math.max(ly + V.D / 2 * LUP + 30, cy0 + CADENA.length * 27 + 8)));
          svg.innerHTML = m;

          /* ---------------- los numeros ---------------- */
          /* Los numeros que comprueba c2_verifica.py llevan su propio id: asi
             la comprobacion lee EL numero y no el trozo de frase que le toque. */
          document.getElementById('md-vivo-n').innerHTML =
            C.movidas ? C.movidas + ' de 7 recalculadas' : 'todo en su sitio';
          document.getElementById('md-vivo-d').innerHTML =
            (C.movidas
             ? 'Has movido un par&aacute;metro y la cadena se ha rehecho sola: <b><span '
               + 'id="md-movidas">' + C.movidas + '</span></b> de las siete medidas deducidas han '
               + 'cambiado.<br>'
             : 'Las siete medidas salen de una f&oacute;rmula, y de momento no se ha movido ninguna '
               + '(<span id="md-movidas">0</span>). Mueve un mando y mira.<br>')
            + 'Agujero <b>&empty;' + m2(V.D) + '</b> &middot; flanco <b>' + m1(V.W) + ' &times; '
            + m1(V.H) + '</b> &middot; hueco <b>' + m1(V.hueco) + '</b><br>'
            + 'Base <b>' + m1(V.B) + ' &times; ' + m1(V.Lb) + '</b> &middot; varilla <b>'
            + m1(V.Lv) + '</b><br>Rehacer el plano: <b>cero minutos</b>.';

          /* Las dos frases se montan como DIFERENCIA con su signo, no como
             "sobran tantos" / "faltan tantos": asi el numero que se ensena es
             siempre el mismo que el de la cuenta, valga lo que valga. */
          var tontoTxt =
            'El servo de ' + v.as + ' mm pide ' + m1(V.hueco) + ' de hueco y el cortado tiene '
            + m1(TONTO.hueco) + ': diferencia <b><span id="md-intservo">' + m1(C.intServo)
            + '</span> mm</b>. '
            + (C.intServo > 1e-9 ? '<b>No entra.</b>'
               : (C.intServo < -1e-9 ? 'Entra, y le sobra hueco.' : 'Entra justo.')) + '<br>'
            + 'El eje de ' + m1(v.ds) + ' contra el agujero ya taladrado de ' + m2(TONTO.D)
            + ': diferencia <b><span id="md-inteje">' + m2(C.intEje) + '</span> mm</b>. '
            + (C.intEje > 1e-9 ? '<b>No pasa.</b>' : 'Pasa.') + '<br>'
            + 'Canto del agujero cortado: <b>' + m1(C.bordeTonto) + '</b>, y la regla pide '
            + m1(V.borde) + '.';
          document.getElementById('md-tonto-n').innerHTML =
            (C.intServo > 1e-9 || C.intEje > 1e-9) ? 'hay que cortarlo otra vez' : 'sigue valiendo';
          document.getElementById('md-tonto-d').innerHTML = tontoTxt;

          document.getElementById('md-stl-n').innerHTML =
            '&empty; &uacute;til <span id="md-def">' + m2(C.Def) + '</span>';
          document.getElementById('md-stl-d').innerHTML =
            'Con <b>' + C.N + '</b> facetas, el c&iacute;rculo de &empty;' + m2(V.D)
            + ' se guarda como un pol&iacute;gono <b>inscrito</b>.<br>'
            + '&empty; &uacute;til = ' + m2(V.D) + ' &times; cos(180&deg;/' + C.N + ') = <b>'
            + m2(C.Def) + '</b><br>Holgura real = ' + m2(C.Def) + ' &minus; ' + m1(v.ds)
            + ' = <b><span id="md-holreal">' + s2(C.holReal) + '</span></b>, y ped&iacute;as '
            + m2(v.hol) + '.<br>'
            + (C.nmin === Infinity
               ? 'Con esta holgura <b>no pasa ni con infinitas facetas</b> '
                 + '(<span id="md-nmin">0</span>).'
               : 'Para que pase hacen falta <b><span id="md-nmin">' + C.nmin
                 + '</span> facetas</b> o m&aacute;s.');

          /* Con muchas facetas la diferencia se va por debajo de la centesima y
             la frase quedaria diciendo "no es 4,10 sino 4,10". Se dice lo que
             pasa de verdad: que es pequenisima, pero que no es cero. */
          document.getElementById('md-cuenta').innerHTML =
            'El pol&iacute;gono de N lados metido dentro del c&iacute;rculo toca la circunferencia '
            + 'solo en los <b>v&eacute;rtices</b>; por el medio de cada lado se queda hacia dentro. '
            + 'Lo que de verdad pasa por el agujero es <b>D &middot; cos(180&deg;/N)</b>. '
            + (C.flecha >= 0.005
               ? 'Con ' + C.N + ' facetas eso son <b>' + m2(C.flecha) + ' mm</b> menos de radio: no '
                 + 'pasa &empty;' + m2(V.D) + ', pasa <b>&empty;' + m2(C.Def) + '</b>.'
               : 'Con ' + C.N + ' facetas la diferencia ya no llega a una cent&eacute;sima de '
                 + 'mil&iacute;metro, as&iacute; que en pantalla salen los dos iguales. Pero '
                 + '<b>no es cero</b>: el STL no guarda c&iacute;rculos, guarda tri&aacute;ngulos, '
                 + 'y por muchos que ponga el pol&iacute;gono sigue yendo por dentro.');

          pie.innerHTML =
            '<b>Pulsa &laquo;Llega el servo de verdad&raquo;.</b> Es lo que pasa siempre: el servo '
            + 'que compr&aacute;is mide 23 mm y no los 20 que hab&iacute;ais supuesto. El modelo vivo '
            + 'recalcula la cadena entera y <b>vuelve a estar bien</b>; el tonto no se entera, y las '
            + 'piezas ya cortadas se van a la basura. Luego baja las facetas a 8 y mira lo que le pasa '
            + 'a un agujero que en el plano pon&iacute;a &empty;8,30. El coste en euros y en tiempo de '
            + 'volver a cortar sale en la escena de la sesi&oacute;n 6.';
        }

        function refresca(){
          document.getElementById('md-ds-v').innerHTML = v.ds + ' mm';
          document.getElementById('md-hol-v').innerHTML = m2(v.hol) + ' mm';
          document.getElementById('md-as-v').innerHTML = v.as + ' mm';
          document.getElementById('md-t-v').innerHTML = v.t + ' mm';
          document.getElementById('md-n-v').innerHTML = '' + FACETAS[v.ni];
          pinta();
        }
        function pon(){
          document.getElementById('md-ds').value = v.ds;
          document.getElementById('md-hol').value = Math.round(v.hol * 100);
          document.getElementById('md-as').value = v.as;
          document.getElementById('md-t').value = v.t;
          document.getElementById('md-n').value = v.ni;
          refresca();
        }

        document.getElementById('md-ds').addEventListener('input', function(){
          v.ds = +this.value; refresca(); });
        document.getElementById('md-hol').addEventListener('input', function(){
          v.hol = (+this.value) / 100; refresca(); });
        document.getElementById('md-as').addEventListener('input', function(){
          v.as = +this.value; refresca(); });
        document.getElementById('md-t').addEventListener('input', function(){
          v.t = +this.value; refresca(); });
        document.getElementById('md-n').addEventListener('input', function(){
          v.ni = +this.value; refresca(); });

        caja.addEventListener('click', function(ev){
          var b = ev.target.closest('button[data-a]');
          if(!b) return;
          if(b.dataset.a === 'servo'){ v.as = 23; }
          else { v = {ds: INI.ds, hol: INI.hol, as: INI.as, t: INI.t, ni: INI.ni}; }
          pon();
        });

        refresca();
      })();
      </script>
'''


# ==========================================================================
# S6 - El plan de corte del despiece entero
# ==========================================================================
CORTE = u'''
      <div class="escena" id="esc-co">
        <div class="escena-barra">
          <span class="escena-titulo">El despiece del riego sobre el tablero &middot; cu&aacute;ntos hacen falta y cu&aacute;nto se tira</span>
          <div class="seg">
            <button type="button" data-a="girar" id="co-girar" aria-pressed="true">Girar las piezas</button>
            <button type="button" data-a="reset">Valores de partida</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 690 452" id="svg-co" role="img"
               aria-label="Los tableros con las piezas del despiece colocadas por el algoritmo de estantes"></svg>
          <div class="co-mandos">
            <div class="co-fila">
              <label for="co-her">Con qu&eacute; se corta</label>
              <select id="co-her">
                <option value="0">C&uacute;ter y regla (cart&oacute;n pluma)</option>
                <option value="1">Cortadora l&aacute;ser</option>
                <option value="2" selected>Sierra de marqueter&iacute;a</option>
                <option value="3">Sierra de calar</option>
              </select>
            </div>
            <div class="co-fila">
              <label for="co-k">Sangr&iacute;a: lo que se come cada corte</label>
              <input type="range" id="co-k" min="0" max="40" step="1" value="15">
              <span class="val" id="co-k-v">1,5 mm</span>
            </div>
            <div class="co-fila">
              <label for="co-tab">Tablero de partida</label>
              <select id="co-tab">
                <option value="0" selected>Retal de 300 &times; 200</option>
                <option value="1">Media plancha de 400 &times; 300</option>
                <option value="2">Tablero de 600 &times; 400</option>
                <option value="3">Tabla estrecha de 700 &times; 80</option>
              </select>
            </div>
            <div class="co-fila">
              <label for="co-g">Grupos que cortan del mismo tablero</label>
              <input type="range" id="co-g" min="1" max="10" step="1" value="1">
              <span class="val" id="co-g-v">1</span>
            </div>
          </div>
          <div class="co-tablero">
            <div class="co-caja" id="co-c-tab">
              <h5>Tableros y aprovechamiento</h5>
              <p class="co-num" id="co-tab-n">&mdash;</p>
              <p class="co-det" id="co-tab-d"></p>
            </div>
            <div class="co-caja" id="co-c-cor">
              <h5>Corte: longitud y tiempo</h5>
              <p class="co-num" id="co-cor-n">&mdash;</p>
              <p class="co-det" id="co-cor-d"></p>
            </div>
            <div class="co-caja" id="co-c-jun">
              <h5>Juntos o cada uno por su lado</h5>
              <p class="co-num" id="co-jun-n">&mdash;</p>
              <p class="co-det" id="co-jun-d"></p>
            </div>
          </div>
          <p class="co-cuenta" id="co-cuenta"></p>
        </div>
        <div class="pie" id="pie-co"></div>
      </div>

      <style>
      .co-mandos{margin-top:10px}
      .co-fila{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:0 0 7px;
        font-family:var(--f-m);font-size:12.5px;color:var(--ink)}
      .co-fila label{min-width:252px}
      .co-fila input[type="range"]{flex:1 1 150px;min-width:120px;accent-color:var(--goo-azul)}
      .co-fila select{flex:1 1 230px;font-family:var(--f-m);font-size:12.5px;padding:5px 7px;
        border:1.5px solid var(--line);border-radius:2px;background:var(--surface);color:var(--ink)}
      .co-fila .val{font-weight:500;color:var(--goo-azul);min-width:66px;text-align:right}
      .co-tablero{display:flex;gap:11px;flex-wrap:wrap;margin-top:12px}
      .co-caja{flex:1 1 200px;min-width:198px;border:1.5px solid var(--line);border-radius:2px;
        padding:11px 13px;background:var(--surface)}
      .co-caja h5{margin:0 0 6px;font:500 11.5px var(--f-m);letter-spacing:.05em;text-transform:uppercase;
        color:var(--ink-soft)}
      #co-c-tab{border-left:5px solid var(--goo-azul)}
      #co-c-cor{border-left:5px solid var(--goo-amarillo)}
      #co-c-jun{border-left:5px solid var(--goo-verde)}
      .co-num{margin:0;font-family:var(--f-m);font-size:20px;font-weight:500;color:var(--ink)}
      .co-det{margin:5px 0 0;font-family:var(--f-m);font-size:11.5px;line-height:1.75;color:var(--ink-soft)}
      .co-det b{color:var(--ink)}
      .co-cuenta{margin:12px 0 0;font-family:var(--f-m);font-size:12.5px;line-height:1.7;color:var(--ink-soft)}
      .co-cuenta b{color:var(--ink)}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-co');
        if(!svg) return;
        var caja = document.getElementById('esc-co');
        var pie  = document.getElementById('pie-co');

        /* ---- el despiece de UN grupo del riego, en milimetros ------------
           Cada pieza va con la orientacion que tiene en el aparato: la caja de
           la electronica es alta y estrecha, y la pletina del sensor sube
           desde el suelo. Por eso hay piezas TUMBADAS y piezas DE PIE, y por
           eso el boton de girar cambia el reparto: si el tablero tiene veta,
           una pieza de pie no se puede tumbar.                            */
        var DESPIECE = [
          {n: 'base del soporte',   w: 70,  h: 35,  c: 1, col: '#1a73e8'},
          {n: 'flanco',             w: 50,  h: 50,  c: 2, col: '#34a853'},
          {n: 'tapa de la caja',    w: 100, h: 70,  c: 1, col: '#fbbc04'},
          {n: 'frente de la caja',  w: 45,  h: 100, c: 1, col: '#ea4335'},
          {n: 'lateral de la caja', w: 45,  h: 70,  c: 2, col: '#9334e6'},
          {n: 'pletina del sensor', w: 30,  h: 90,  c: 1, col: '#00897b'},
          {n: 'abrazadera',         w: 50,  h: 20,  c: 2, col: '#f4511e'}
        ];
        /* herramientas: sangria en mm y velocidad de corte en mm/min */
        var HER = [
          {n: 'c&uacute;ter',        k: 0.0, vel: 900},
          {n: 'l&aacute;ser',        k: 0.2, vel: 2400},
          {n: 'marqueter&iacute;a',  k: 1.5, vel: 180},
          {n: 'sierra de calar',     k: 2.4, vel: 600}
        ];
        var TAB = [{w: 300, h: 200}, {w: 400, h: 300}, {w: 600, h: 400},
                   {w: 700, h: 80}];
        var ESPESOR = 4;            /* contrachapado de 4 mm */
        var EUR_M2_MM = 3.0;        /* el mismo precio que en la escena de la S4 */

        var v = {her: 2, k: 1.5, tab: 0, g: 1, girar: true};

        /* ---- el empaquetado por ESTANTES ---------------------------------
           1. Se expanden las piezas (las que van por duplicado, dos veces).
           2. Si se pueden girar, se tumban todas: el lado largo, en horizontal.
           3. Se ordenan de mas alta a mas baja; a igual altura, la mas ancha
              primero, y a igualdad, por el orden del despiece. Asi el reparto
              es SIEMPRE el mismo y se puede comprobar a mano.
           4. Cada pieza va al primer estante ya abierto donde quepa a lo
              ancho; si no cabe en ninguno, se abre un estante nuevo debajo;
              si tampoco cabe, se empieza otro tablero.
           La sangria se descuenta ENTRE pieza y pieza y entre estante y
           estante: el canto del tablero se recorta de todas formas.        */
        function empaqueta(nGrupos, W, H, kerf, girar){
          var lista = [], i, j, g;
          for(g = 0; g < nGrupos; g++){
            for(i = 0; i < DESPIECE.length; i++){
              for(j = 0; j < DESPIECE[i].c; j++){
                var p = DESPIECE[i], a = p.w, b = p.h;
                if(girar && b > a){ var s = a; a = b; b = s; }
                lista.push({w: a, h: b, col: p.col, n: p.n, idx: i, g: g});
              }
            }
          }
          lista.forEach(function(p, n){ p.orden = n; });
          lista.sort(function(a, b){
            if(b.h !== a.h) return b.h - a.h;
            if(b.w !== a.w) return b.w - a.w;
            return a.orden - b.orden;
          });

          var tableros = [], fuera = [], area = 0;
          lista.forEach(function(p){
            var t, e, puesto = false;
            for(t = 0; t < tableros.length && !puesto; t++){
              var T = tableros[t];
              for(e = 0; e < T.estantes.length && !puesto; e++){
                var E = T.estantes[e];
                if(p.h <= E.h + 1e-9 && E.x + p.w <= W + 1e-9){
                  p.x = E.x; p.y = E.y; p.t = t;
                  E.x += p.w + kerf;
                  E.piezas.push(p);
                  puesto = true;
                }
              }
              if(!puesto){
                var yN = T.alto === 0 ? 0 : T.alto + kerf;
                if(yN + p.h <= H + 1e-9){
                  var nuevo = {y: yN, h: p.h, x: p.w + kerf, piezas: [p]};
                  p.x = 0; p.y = yN; p.t = t;
                  T.estantes.push(nuevo);
                  T.alto = yN + p.h;
                  puesto = true;
                }
              }
            }
            if(!puesto){
              if(p.w <= W + 1e-9 && p.h <= H + 1e-9){
                var T2 = {estantes: [{y: 0, h: p.h, x: p.w + kerf, piezas: [p]}], alto: p.h};
                p.x = 0; p.y = 0; p.t = tableros.length;
                tableros.push(T2);
              } else {
                fuera.push(p);
                return;
              }
            }
            area += p.w * p.h;
          });
          var colocadas = lista.length - fuera.length;
          return {tableros: tableros, lista: lista, fuera: fuera, area: area,
                  colocadas: colocadas, total: lista.length,
                  nTab: tableros.length};
        }

        function z(x){ return Math.abs(x) < 0.0005 ? 0 : x; }
        function n0(x){ return Math.round(z(x)).toString(); }
        function n1(x){ return z(x).toFixed(1).replace('.', ','); }
        function n2(x){ return z(x).toFixed(2).replace('.', ','); }

        function pinta(){
          var T = TAB[v.tab], W = T.w, H = T.h;
          var P = empaqueta(v.g, W, H, v.k, v.girar);
          var solo = empaqueta(1, W, H, v.k, v.girar);      /* un grupo, un tablero */
          var sueltos = solo.nTab * v.g;                     /* si cada uno va por su lado */
          var areaTab = W * H;
          var aprov = P.nTab ? 100 * P.area / (P.nTab * areaTab) : 0;
          /* el mismo precio de la escena de la S4: euros por m2 y por mm de espesor */
          var euroTab = areaTab * EUR_M2_MM * ESPESOR / 1e6;
          var euroJun = P.nTab * euroTab, euroSue = sueltos * euroTab;

          /* longitud de corte: el perimetro de cada pieza colocada. No se
             descuentan los cortes que dos piezas pegadas comparten, asi que
             es una cota POR ARRIBA, y la escena lo dice. */
          var lcorte = 0;
          P.lista.forEach(function(p){ if(p.t !== undefined) lcorte += 2 * (p.w + p.h); });
          var tmin = lcorte / HER[v.her].vel;

          /* =============== el dibujo =============== */
          var m = '';
          var COLS = P.nTab > 1 ? 2 : 1, VER = P.nTab > 2 ? 2 : 1;
          var ancho = COLS === 1 ? 640 : 316, alto = VER === 1 ? 352 : 172;
          var esc = Math.min(ancho / W, alto / H);
          var muestra = Math.min(P.nTab, 4);
          var i, OY0 = 46, SEP = 34;
          m += '<text x="24" y="24" class="etq">Tablero de ' + W + ' &times; ' + H
             + ' mm &middot; sangr&iacute;a de ' + n1(v.k) + ' mm entre pieza y pieza'
             + (P.nTab > 4 ? ' &middot; se dibujan los 4 primeros de ' + P.nTab : '') + '</text>';
          for(i = 0; i < muestra; i++){
            var ox = 26 + (i % 2) * (ancho + 26), oy = OY0 + Math.floor(i / 2) * (H * esc + SEP);
            if(COLS === 1) ox = 26;
            m += '<rect x="' + ox + '" y="' + oy + '" width="' + (W * esc).toFixed(1)
               + '" height="' + (H * esc).toFixed(1) + '" fill="var(--surface-2)"'
               + ' stroke="currentColor" stroke-width="1.5"/>';
            m += '<text x="' + ox + '" y="' + (oy - 5) + '" class="ejeq">tablero ' + (i + 1)
               + '</text>';
          }
          P.lista.forEach(function(p){
            if(p.t === undefined || p.t >= muestra) return;
            var ox = 26 + (p.t % 2) * (ancho + 26), oy = OY0 + Math.floor(p.t / 2) * (H * esc + SEP);
            if(COLS === 1) ox = 26;
            var x = ox + p.x * esc, y = oy + p.y * esc, w = p.w * esc, h = p.h * esc;
            m += '<rect x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" width="' + w.toFixed(1)
               + '" height="' + h.toFixed(1) + '" fill="' + p.col + '" opacity="'
               + (0.30 + 0.12 * (p.g % 3)) + '" stroke="' + p.col + '" stroke-width="1.2"/>';
            if(w > 42 && h > 17){
              m += '<text x="' + (x + w / 2).toFixed(1) + '" y="' + (y + h / 2 + 4).toFixed(1)
                 + '" class="ejeq" text-anchor="middle">' + p.w + '&times;' + p.h + '</text>';
            }
          });
          var filas = Math.ceil(muestra / (COLS === 1 ? 1 : 2));
          var hTotal = OY0 + filas * (H * esc + SEP) - SEP + 16;
          if(P.fuera.length){
            m += '<text x="24" y="' + (hTotal + 4) + '" class="etq" fill="#ea4335">'
               + P.fuera.length + ' pieza(s) no caben de pie en un tablero de ' + W + ' &times; '
               + H + ': habr&iacute;a que poder girarlas</text>';
            hTotal += 16;
          }
          svg.setAttribute('viewBox', '0 0 690 ' + Math.ceil(hTotal));
          svg.innerHTML = m;

          /* =============== los numeros =============== */
          /* Los numeros que comprueba c2_verifica.py llevan su propio id. */
          document.getElementById('co-tab-n').innerHTML = '<span id="co-ntab">' + P.nTab + '</span>'
            + (P.nTab === 1 ? ' tablero' : ' tableros');
          document.getElementById('co-tab-d').innerHTML =
            '<span id="co-puestas">' + P.colocadas + '</span> piezas de ' + P.total
            + ' colocadas, <span id="co-area">' + n0(P.area) + '</span> mm&sup2; de '
            + 'pieza.<br>Tablero: ' + W + ' &times; ' + H + ' = <b>' + n0(areaTab) + ' mm&sup2;</b>'
            + ' cada uno.<br>Aprovechamiento = ' + n0(P.area) + ' / (' + P.nTab + ' &times; '
            + n0(areaTab) + ') = <b><span id="co-aprov">' + n1(aprov) + '</span> %</b><br>Se tira <b>'
            + n0((P.nTab * areaTab - P.area) / 100) + ' cm&sup2;</b> de tablero.';

          document.getElementById('co-cor-n').innerHTML = '<span id="co-tmin">' + n0(tmin)
            + '</span> min';
          document.getElementById('co-cor-d').innerHTML =
            'Per&iacute;metro de todas las piezas: <b><span id="co-lcorte">' + n0(lcorte / 10)
            + '</span> cm</b>.<br>'
            + 'La ' + HER[v.her].n + ' avanza <b>' + HER[v.her].vel + ' mm/min</b>.<br>'
            + n0(lcorte) + ' / ' + HER[v.her].vel + ' = <b>' + n1(tmin) + ' min</b> de corte.<br>'
            + 'Es una cota <b>por arriba</b>: dos piezas pegadas comparten corte.';

          var ahorro = sueltos - P.nTab;
          document.getElementById('co-jun-n').innerHTML =
            '<span id="co-ahorro">' + ahorro + '</span>'
            + (ahorro > 0 ? (ahorro === 1 ? ' tablero' : ' tableros') + ' de menos'
                          : ' de diferencia');
          document.getElementById('co-jun-d').innerHTML =
            (v.g === 1 ? 'Un grupo solo' : 'Los ' + v.g + ' grupos <b>juntos</b>') + ': ' + P.nTab
            + (P.nTab === 1 ? ' tablero, ' : ' tableros, ') + n2(euroJun) + ' &euro;.<br>'
            + 'Cada grupo <b>por su lado</b>: ' + v.g + ' &times; ' + solo.nTab
            + ' = <span id="co-sueltos">' + sueltos + '</span>'
            + (sueltos === 1 ? ' tablero, ' : ' tableros, ') + n2(euroSue) + ' &euro;.<br>'
            + 'Diferencia: <b><span id="co-eurodif">' + n2(euroSue - euroJun) + '</span> &euro;</b> y <b>'
            + n0((sueltos - P.nTab) * areaTab / 100) + ' cm&sup2;</b> de tablero.<br>'
            + 'Precio de taller: ' + n1(EUR_M2_MM) + ' &euro; por m&sup2; y mil&iacute;metro de '
            + 'espesor, con ' + ESPESOR + ' mm.';

          document.getElementById('co-cuenta').innerHTML =
            'La <b>sangr&iacute;a</b> es el ancho de material que convierte en serr&iacute;n cada '
            + 'pasada. Con la marqueter&iacute;a son 1,5 mm; con el l&aacute;ser, 0,2. Aqu&iacute; se '
            + 'descuenta <b>entre pieza y pieza</b>, que es donde se nota: con ' + n1(v.k)
            + ' mm y ' + P.total + ' piezas, cada fila pierde ese ancho tantas veces como cortes '
            + 'lleve. Y ojo con una cosa que no se ve en el n&uacute;mero: la sangr&iacute;a '
            + 'tambi&eacute;n <b>se come la pieza</b> si cortas por el centro de la raya en vez de '
            + 'por fuera.';

          pie.innerHTML =
            '<b>Sube los grupos de 1 a 10.</b> Con un tablero por grupo salen ' + sueltos
            + ' tableros; cortando el encargo de toda la clase de una vez salen <b>' + P.nTab
            + '</b>. La diferencia no es que el algoritmo sea listo: es que <b>el hueco que le sobra '
            + 'a un grupo le sirve a otro</b>. Prueba tambi&eacute;n la <b>tabla estrecha de '
            + '700 &times; 80</b> y apaga ah&iacute; &laquo;Girar las piezas&raquo;: el frente de la '
            + 'caja mide 100 de alto y la tabla 80, as&iacute; que de pie <b>no cabe de ninguna '
            + 'manera</b>. Si el tablero tiene veta o dibujo, girarla no siempre es una opci&oacute;n, '
            + 'y esa pieza hay que sacarla de otro sitio. El reparto es <b>siempre el mismo</b> con '
            + 'los mismos datos: el algoritmo coloca las piezas m&aacute;s altas primero y no sortea '
            + 'nada.';
        }

        function refresca(){
          document.getElementById('co-k-v').innerHTML = n1(v.k) + ' mm';
          document.getElementById('co-g-v').innerHTML = '' + v.g;
          pinta();
        }

        document.getElementById('co-her').addEventListener('change', function(){
          v.her = +this.value;
          v.k = HER[v.her].k;
          document.getElementById('co-k').value = Math.round(v.k * 10);
          refresca();
        });
        document.getElementById('co-k').addEventListener('input', function(){
          v.k = (+this.value) / 10; refresca(); });
        document.getElementById('co-tab').addEventListener('change', function(){
          v.tab = +this.value; refresca(); });
        document.getElementById('co-g').addEventListener('input', function(){
          v.g = +this.value; refresca(); });

        caja.addEventListener('click', function(ev){
          var b = ev.target.closest('button[data-a]');
          if(!b) return;
          if(b.dataset.a === 'girar'){
            v.girar = !v.girar;
            b.setAttribute('aria-pressed', v.girar ? 'true' : 'false');
          } else {
            v = {her: 2, k: 1.5, tab: 0, g: 1, girar: true};
            document.getElementById('co-her').value = '2';
            document.getElementById('co-k').value = 15;
            document.getElementById('co-tab').value = '0';
            document.getElementById('co-g').value = 1;
            document.getElementById('co-girar').setAttribute('aria-pressed', 'true');
          }
          refresca();
        });

        refresca();
      })();
      </script>
'''
