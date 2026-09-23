# -*- coding: utf-8 -*-
u"""Escenas de las sesiones 1 y 2 de la U5 de 4.o. SVG + JavaScript a mano.

Todas CALCULAN. Ninguna lleva dentro una tabla de resultados escrita a mano:
si en pantalla sale un numero, ese numero sale de una cuenta hecha en el
momento con los valores que el alumno ha puesto.

  ESCENA_DIVISOR     S1 - divisor de tension con LDR o NTC. Modelo de la LDR
                     (ley de potencia) y de la NTC (ecuacion B), divisor
                     resistivo y conversor de 10 bits del Arduino. La curva
                     se traza punto a punto, 170 muestras, cada vez que se
                     toca un control.
  ESCENA_TRANSISTOR  S2 - transistor como interruptor. Corriente de base,
                     margen de saturacion, Vce, potencia disipada y el pico
                     inductivo al cortar, con y sin diodo de rueda libre.

Las cadenas de JS llevan \\uXXXX y no entidades HTML: una entidad HTML dentro
de una cadena de JavaScript se dibuja como seis caracteres y descuadra el
ancho de la caja que la contiene.

Los modelos, y de donde salen:

  LDR      R(E) = 10 kΩ * (E / 10 lux) ^ -0,7
           Es la ley de potencia con la que se describen las LDR de sulfuro de
           cadmio. Los dos numeros (10 kΩ a 10 lux, gamma 0,7) son los de
           una GL5528, que es la que viene en los kits de Arduino. No es la
           medida de una LDR concreta: es el modelo, y sale dicho en la escena.

  NTC      R(T) = 10 kΩ * exp( 3950 * (1/T - 1/298,15) )   con T en kelvin
           Ecuacion B (o de Steinhart simplificada) de una NTC 10k B3950.
           Comprobacion: a 0 C da 33,6 kΩ y a 50 C da 3,59 kΩ, que es
           lo que pone la tabla del fabricante (33,6 y 3,60).

  BC547    beta = 100 (valor de diseno, conservador), Vbe = 0,7 V,
           Vce_sat = 0,2 V, Ic_max = 100 mA, Vceo = 45 V.
  TIP120   Darlington: beta = 1000, Vbe = 1,6 V (son dos uniones en cascada),
           Vce_sat = 1,0 V, Ic_max = 5 A, Vceo = 60 V.
"""

# ---------------------------------------------------------------------------
# S1 - El divisor de tension
#
# Lienzo 640 x 380.
#   Columna del circuito, x 16..290:
#       rail +5 V   y=56, de x=52 a x=132
#       rama vertical en x=92
#       componente de arriba  x 74..110, y  78..134
#       nudo de salida        (92, 155), flecha a la caja A0 en x 150..208
#       componente de abajo   x 74..110, y 176..232
#       masa                  (92, 254)
#       los rotulos de cada componente van en x=118, que es el unico hueco que
#       queda: a la izquierda esta el rail y debajo la caja del A0.
#   Grafica, x 300..628:
#       marco util  L=330  R=600  T=72  B=300
#       x(t) = 330 + t*270     t de 0 a 1 sobre el rango del deslizador
#       y(V) = 300 - (V/5)*228
#       eje derecho con la cuenta del conversor (0..1023), rotulos en x=606
# ---------------------------------------------------------------------------
ESCENA_DIVISOR = u'''
      <div class="escena" id="esc-div">
        <div class="escena-barra">
          <span class="escena-titulo">De &laquo;resistencia que cambia&raquo; a &laquo;tensi&oacute;n que se puede leer&raquo;</span>
          <div class="seg" id="seg-div-sensor">
            <button type="button" data-s="ldr" aria-pressed="true">LDR (luz)</button>
            <button type="button" data-s="ntc">NTC (temperatura)</button>
          </div>
        </div>
        <div class="escena-barra">
          <span class="escena-titulo">Resistencia fija</span>
          <div class="seg" id="seg-div-rf">
            <button type="button" data-r="1000">1 k&#8486;</button>
            <button type="button" data-r="4700">4,7 k&#8486;</button>
            <button type="button" data-r="10000" aria-pressed="true">10 k&#8486;</button>
            <button type="button" data-r="47000">47 k&#8486;</button>
          </div>
          <div class="seg" id="seg-div-mont">
            <button type="button" data-m="abajo" aria-pressed="true">Sensor abajo</button>
            <button type="button" data-m="arriba">Sensor arriba</button>
          </div>
        </div>
        <div class="escena-barra">
          <label class="ctrl" style="flex:1">
            <span id="div-etq">Luz que le llega a la LDR</span>
            <input id="div-mag" type="range" min="0" max="1000" value="500" step="1">
            <b id="div-val">100 lux</b>
          </label>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 380" id="svg-div" role="img"
               aria-label="Un divisor de tensi&oacute;n con un sensor y una resistencia fija, y la curva de la tensi&oacute;n de salida"></svg>
        </div>
        <div class="pie" id="pie-div"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-div');
        if(!svg) return;
        var pie = document.getElementById('pie-div');
        var segS = document.getElementById('seg-div-sensor');
        var segR = document.getElementById('seg-div-rf');
        var segM = document.getElementById('seg-div-mont');
        var mag  = document.getElementById('div-mag');
        var etq  = document.getElementById('div-etq');
        var val  = document.getElementById('div-val');

        var VCC = 5, BITS = 1024;
        var sensor = 'ldr', Rf = 10000, montaje = 'abajo';

        /* ---------------- los dos modelos de sensor ---------------- */
        /* LDR de sulfuro de cadmio tipo GL5528: ley de potencia. */
        function Rldr(lux){
          var r = 10000 * Math.pow(Math.max(lux, 1e-3) / 10, -0.7);
          return Math.min(Math.max(r, 60), 3e6);
        }
        /* NTC 10k B3950: ecuacion B. T en grados, se pasa a kelvin. */
        function Rntc(t){
          var K = t + 273.15;
          return 10000 * Math.exp(3950 * (1 / K - 1 / 298.15));
        }
        /* El deslizador va de 0 a 1000 y se reparte sobre el rango del
           sensor: la luz en escala logaritmica (seis decadas) porque una LDR
           trabaja en seis decadas; la temperatura, lineal. */
        function magnitud(t){
          return sensor === 'ldr' ? Math.pow(10, -1 + 6 * t) : -10 + 70 * t;
        }
        function Rsensor(m){ return sensor === 'ldr' ? Rldr(m) : Rntc(m); }

        /* Divisor. El montaje decide quien va arriba y quien abajo, y eso
           decide si mas luz significa mas cuenta o menos. */
        function vsalida(Rs){
          var arriba = (montaje === 'arriba') ? Rs : Rf;
          var abajo  = (montaje === 'arriba') ? Rf : Rs;
          return VCC * abajo / (arriba + abajo);
        }
        function cuenta(v){
          return Math.max(0, Math.min(BITS - 1, Math.round(v / VCC * (BITS - 1))));
        }

        /* Donde el sensor vale lo mismo que la resistencia fija: es el punto
           en el que el divisor es mas sensible. Se busca por biseccion sobre
           el parametro del deslizador, no con una formula a mano, para que
           valga igual con la LDR que con la NTC. */
        function puntoIgual(){
          var f = function(t){ return Math.log(Rsensor(magnitud(t)) / Rf); };
          var a = 0, b = 1;
          if(f(a) * f(b) > 0) return null;
          for(var i = 0; i < 60; i++){
            var c = (a + b) / 2;
            if(f(a) * f(c) <= 0) b = c; else a = c;
          }
          return (a + b) / 2;
        }

        /* ------------------------- formatos ------------------------- */
        function coma(n, d){ return n.toFixed(d).replace('.', ','); }
        function ohm(r){
          if(r >= 1e6) return coma(r / 1e6, 2) + ' M\\u03a9';
          if(r >= 1000) return coma(r / 1000, r >= 100000 ? 0 : 2) + ' k\\u03a9';
          return Math.round(r) + ' \\u03a9';
        }
        function lux(e){
          if(e >= 1000) return coma(e / 1000, 1) + 'k lux';
          if(e >= 10) return Math.round(e) + ' lux';
          if(e >= 1) return coma(e, 1) + ' lux';
          return coma(e, 2) + ' lux';
        }
        function magTxt(m){ return sensor === 'ldr' ? lux(m) : coma(m, 1) + ' \\u00b0C'; }

        /* --------------------------- dibujo -------------------------- */
        function caja(x, y, w, h, relleno, borde, grosor){
          return '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h
               + '" rx="2" fill="' + relleno + '" stroke="' + borde + '" stroke-width="'
               + grosor + '"></rect>';
        }
        function hilo(d, color, grosor, guion){
          return '<path d="' + d + '" fill="none" stroke="' + (color || 'var(--ink-soft)')
               + '" stroke-width="' + (grosor || 2) + '" stroke-linecap="round"'
               + (guion ? ' stroke-dasharray="' + guion + '"' : '') + '></path>';
        }
        function rot(x, y, txt, est, anchor){
          return '<text x="' + x + '" y="' + y + '" class="rotulo-svg"'
               + (anchor ? ' text-anchor="' + anchor + '"' : '')
               + (est ? ' style="' + est + '"' : '') + '>' + txt + '</text>';
        }

        /* Los simbolos son los normalizados, no un adorno. La LDR es la caja
           de resistencia con DOS flechas apuntando hacia ella (la luz que le
           entra). La NTC es la caja con la linea inclinada de "resistencia
           que depende de algo", con su pie horizontal abajo, mas el rotulo
           -t\\u00b0 que dice que el algo es la temperatura y que baja al
           subir. */
        function simboloSensor(x, y, w, h){
          var m = caja(x, y, w, h, 'var(--surface)', 'var(--goo-azul)', 2);
          if(sensor === 'ldr'){
            m += hilo('M' + (x - 24) + ' ' + (y + 12) + ' L' + (x - 6) + ' ' + (y + 21),
                      'var(--goo-amarillo)', 2);
            m += '<path d="M' + (x - 4) + ' ' + (y + 22) + ' l-9 0 l3 6 Z" fill="var(--goo-amarillo)"></path>';
            m += hilo('M' + (x - 24) + ' ' + (y + 30) + ' L' + (x - 6) + ' ' + (y + 39),
                      'var(--goo-amarillo)', 2);
            m += '<path d="M' + (x - 4) + ' ' + (y + 40) + ' l-9 0 l3 6 Z" fill="var(--goo-amarillo)"></path>';
          } else {
            /* la punta se queda 4 px por encima de la caja: mas arriba se
               metia debajo del hilo de salida, que va por y = 155 */
            m += hilo('M' + (x - 20) + ' ' + (y + h + 6) + ' H' + (x - 10)
                      + ' L' + (x + w + 2) + ' ' + (y - 2), 'var(--goo-rojo)', 2);
            m += '<path d="M' + (x + w + 4) + ' ' + (y - 4) + ' l-10 2 l4 6 Z" fill="var(--goo-rojo)"></path>';
            m += rot(x + w + 4, y + h + 10, '\\u2212t\\u00b0', 'font-size:10px;fill:var(--goo-rojo)');
          }
          return m;
        }
        function simboloFija(x, y, w, h){
          return caja(x, y, w, h, 'var(--surface)', 'var(--ink-soft)', 2);
        }

        function pinta(){
          var t = +mag.value / 1000;
          var m0 = magnitud(t);
          var Rs = Rsensor(m0);
          var V = vsalida(Rs);
          var n = cuenta(V);
          var s = '', i;

          /* ================= columna del circuito ================= */
          s += rot(16, 22, 'EL CIRCUITO', 'font-size:10.5px');

          s += hilo('M52 56 H132');
          s += rot(52, 44, '+5 V', 'font-size:10.5px;fill:var(--goo-rojo)');
          s += hilo('M92 56 V78');
          s += hilo('M92 134 V176');
          s += hilo('M92 232 V254');

          var arribaEsSensor = (montaje === 'arriba');
          s += arribaEsSensor ? simboloSensor(74, 78, 36, 56) : simboloFija(74, 78, 36, 56);
          s += arribaEsSensor ? simboloFija(74, 176, 36, 56) : simboloSensor(74, 176, 36, 56);

          /* masa */
          s += hilo('M79 254 H105', 'var(--ink-soft)', 2.5);
          s += hilo('M83 259 H101', 'var(--ink-soft)', 2);
          s += hilo('M87 264 H97', 'var(--ink-soft)', 2);

          /* nudo de salida y flecha al pin */
          s += '<circle cx="92" cy="155" r="3.5" fill="var(--ink)"></circle>';
          s += hilo('M92 155 H144', 'var(--goo-azul)', 2.5);
          s += '<path d="M150 155 l-8 -4 v8 Z" fill="var(--goo-azul)"></path>';
          s += caja(150, 139, 58, 32, 'var(--accent-soft)', 'var(--goo-azul)', 2);
          s += rot(179, 159, 'A0', 'font-size:14px;fill:var(--goo-azul);font-weight:500', 'middle');

          /* rotulos de los dos componentes */
          var nomA = arribaEsSensor ? (sensor === 'ldr' ? 'LDR' : 'NTC') : 'R fija';
          var nomB = arribaEsSensor ? 'R fija' : (sensor === 'ldr' ? 'LDR' : 'NTC');
          var valA = arribaEsSensor ? ohm(Rs) : ohm(Rf);
          var valB = arribaEsSensor ? ohm(Rf) : ohm(Rs);
          var colA = arribaEsSensor ? 'var(--goo-azul)' : 'var(--ink-soft)';
          var colB = arribaEsSensor ? 'var(--ink-soft)' : 'var(--goo-azul)';
          s += rot(120, 100, nomA, 'font-size:11px;fill:' + colA + ';font-weight:500');
          s += rot(120, 116, valA, 'font-size:13px;fill:var(--ink)');
          s += rot(120, 198, nomB, 'font-size:11px;fill:' + colB + ';font-weight:500');
          s += rot(120, 214, valB, 'font-size:13px;fill:var(--ink)');

          s += rot(16, 290, 'TENSI\\u00d3N EN EL NUDO', 'font-size:9.5px');
          s += rot(16, 314, coma(V, 3) + ' V', 'font-size:20px;fill:var(--goo-azul);font-weight:500');
          s += rot(16, 340, 'analogRead() devuelve', 'font-size:9.5px');
          s += rot(16, 364, n, 'font-size:20px;fill:var(--ink);font-weight:500');

          /* ====================== la grafica ====================== */
          var L = 330, R = 600, T = 72, B = 300;
          var px = function(u){ return L + u * (R - L); };
          var py = function(v){ return B - (v / VCC) * (B - T); };

          s += rot(300, 30, sensor === 'ldr'
                   ? 'TENSI\\u00d3N EN A0 SEG\\u00daN LA LUZ QUE HAY'
                   : 'TENSI\\u00d3N EN A0 SEG\\u00daN LA TEMPERATURA', 'font-size:10.5px');
          s += rot(300, 48, 'con esta resistencia fija de ' + ohm(Rf),
                   'font-size:9.5px');

          /* rejilla y ejes */
          for(i = 0; i <= 5; i++){
            var yy = py(i);
            s += hilo('M' + L + ' ' + yy + ' H' + R, 'var(--line-soft)', 1);
            s += rot(L - 7, yy + 4, i + ' V', 'font-size:9.5px', 'end');
            s += rot(R + 7, yy + 4, Math.round(i / VCC * (BITS - 1)), 'font-size:9.5px');
          }
          s += rot(636, T - 14, 'cuenta', 'font-size:9px', 'end');
          s += hilo('M' + L + ' ' + T + ' V' + B, 'var(--line)', 1.5);
          s += hilo('M' + L + ' ' + B + ' H' + R, 'var(--line)', 1.5);

          /* marcas del eje horizontal */
          var marcas = sensor === 'ldr'
            ? [[0, '0,1'], [1/6, '1'], [2/6, '10'], [3/6, '100'], [4/6, '1k'], [5/6, '10k'], [1, '100k']]
            : [[0, '-10'], [1/7, '0'], [2/7, '10'], [3/7, '20'], [4/7, '30'], [5/7, '40'],
               [6/7, '50'], [1, '60']];
          for(i = 0; i < marcas.length; i++){
            var xx = px(marcas[i][0]);
            s += hilo('M' + xx + ' ' + B + ' V' + (B + 5), 'var(--line)', 1.5);
            s += rot(xx, B + 18, marcas[i][1], 'font-size:9.5px', 'middle');
          }
          s += rot((L + R) / 2, B + 34, sensor === 'ldr' ? 'lux (escala logar\\u00edtmica)'
                   : 'grados cent\\u00edgrados', 'font-size:9.5px', 'middle');

          /* la curva: 170 muestras calculadas de una en una */
          var d = '';
          for(i = 0; i <= 170; i++){
            var u = i / 170;
            var vv = vsalida(Rsensor(magnitud(u)));
            d += (i ? ' L' : 'M') + px(u).toFixed(1) + ' ' + py(vv).toFixed(1);
          }
          s += hilo(d, 'var(--goo-azul)', 2.5);

          /* donde el sensor vale lo mismo que la R fija: el tramo util */
          var ti = puntoIgual();
          if(ti !== null && ti > 0.005 && ti < 0.995){
            s += hilo('M' + px(ti).toFixed(1) + ' ' + T + ' V' + B, 'var(--goo-verde)', 1.5, '4 4');
            s += rot(px(ti), T - 4, 'aqu\\u00ed el sensor mide ' + ohm(Rf),
                     'font-size:9px;fill:var(--goo-verde)', 'middle');
          }

          /* punto de trabajo */
          var Xp = px(t), Yp = py(V);
          s += hilo('M' + L + ' ' + Yp.toFixed(1) + ' H' + Xp.toFixed(1), 'var(--goo-rojo)', 1, '3 3');
          s += hilo('M' + Xp.toFixed(1) + ' ' + Yp.toFixed(1) + ' V' + B, 'var(--goo-rojo)', 1, '3 3');
          s += '<circle cx="' + Xp.toFixed(1) + '" cy="' + Yp.toFixed(1)
             + '" r="5.5" fill="var(--goo-rojo)"></circle>';

          svg.innerHTML = s;

          /* ======================== el pie ======================== */
          var arriba = (montaje === 'arriba') ? Rs : Rf;
          var abajo  = (montaje === 'arriba') ? Rf : Rs;
          var paso = VCC / BITS * 1000;

          /* cuanto se mueve la cuenta si la magnitud cambia "un poco": con la
             LDR, el doble de luz; con la NTC, un grado mas. */
          var m2 = sensor === 'ldr' ? m0 * 2 : m0 + 1;
          var n2 = cuenta(vsalida(Rsensor(m2)));
          var salto = Math.abs(n2 - n);
          var cambio = sensor === 'ldr' ? 'el doble de luz (' + magTxt(m2) + ')'
                                        : 'un grado m\\u00e1s (' + magTxt(m2) + ')';

          var txt = '<b>' + magTxt(m0) + '</b> &rarr; el sensor mide <b>' + ohm(Rs)
            + '</b>. El divisor reparte los 5 V: <b>V = 5 &middot; '
            + ohm(abajo) + ' / (' + ohm(arriba) + ' + ' + ohm(abajo) + ') = '
            + coma(V, 3) + ' V</b>. El conversor del Arduino parte esos 5 V en '
            + '<b>1024 escalones</b> de ' + coma(paso, 2) + ' mV, as&iacute; que '
            + '<code>analogRead(A0)</code> devuelve <b>' + n + '</b>.';

          txt += '<br>Con ' + cambio + ' la cuenta pasar&iacute;a a <b>' + n2
               + '</b>: ' + (salto === 0 ? '<b>no se mueve</b>' : 'se mueve <b>' + salto
               + ' escalon' + (salto === 1 ? '' : 'es') + '</b>') + '. ';
          if(salto < 5)
            txt += '<b>Aqu&iacute; el circuito casi no se entera.</b> Prueba otra resistencia fija: '
                 + 'el divisor solo es sensible donde el sensor vale parecido a ella.';
          else
            txt += 'Eso s&iacute; se distingue del ruido, as&iacute; que <b>en esta zona el circuito '
                 + 'sirve</b>.';

          pie.innerHTML = txt
            + '<br><span style="font-size:12.5px">La LDR se calcula con la ley de potencia de una '
            + '<b>GL5528</b> (10 k&#8486; a 10 lux) y la NTC con la ecuaci&oacute;n B de una '
            + '<b>10 k&#8486; B3950</b>. Son <b>los modelos del fabricante</b>, no la medida de la '
            + 'LDR que tengas t&uacute; en la mano: dos LDR del mismo saquito se llevan f&aacute;cil un '
            + '30 %. Lo que s&iacute; es exacto es el divisor y la cuenta del conversor.</span>';
        }

        function refrescaEtq(){
          var t = +mag.value / 1000;
          etq.textContent = sensor === 'ldr' ? 'Luz que le llega a la LDR'
                                             : 'Temperatura de la NTC';
          val.textContent = magTxt(magnitud(t));
        }
        function pulsa(cont, attr, fn){
          cont.addEventListener('click', function(e){
            var b = e.target.closest('button[' + attr + ']');
            if(!b) return;
            cont.querySelectorAll('button').forEach(function(x){
              x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
            });
            fn(b.getAttribute(attr));
            refrescaEtq(); pinta();
          });
        }
        pulsa(segS, 'data-s', function(v){ sensor = v; });
        pulsa(segR, 'data-r', function(v){ Rf = +v; });
        pulsa(segM, 'data-m', function(v){ montaje = v; });
        mag.addEventListener('input', function(){ refrescaEtq(); pinta(); });

        refrescaEtq();
        pinta();
      })();
      </script>
'''


# ---------------------------------------------------------------------------
# S2 - El transistor como interruptor
#
# Lienzo 640 x 430.
#   Columna del circuito, x 16..330:
#       rail +5 V            y=46,  x 60..300
#       carga                x 212..288, y 74..140   (centro x=250)
#       diodo de rueda libre rama por x=168, en paralelo con la carga
#       transistor NPN       circulo (250, 215) r=30
#                            barra de base vertical en x=242, y 199..231
#                            colector (242,205)-(266,193)-(266,168)
#                            emisor   (242,225)-(266,237)-(266,282)
#       Rb                   x 128..184, y 205..225, sobre la patilla de base
#       pin D9               x 16..72,  y 200..230
#       masa comun           y=296, de x=40 a x=266
#   Panel de cuentas, x 352..628:
#       cuatro barras (y 78, 106, 150, 178), escala comun por pareja
#       caja de estado   y 206..266
#       pico de apagado  y 292..414, escala logaritmica de 1 V a 100 kV
# ---------------------------------------------------------------------------
ESCENA_TRANSISTOR = u'''
      <div class="escena" id="esc-tr">
        <div class="escena-barra">
          <span class="escena-titulo">El pin da 20 mA. El motor pide diez veces m&aacute;s</span>
          <div class="seg" id="seg-tr-carga">
            <button type="button" data-c="led">LED &middot; 20 mA</button>
            <button type="button" data-c="bomba" aria-pressed="true">Bomba de riego &middot; 250 mA</button>
            <button type="button" data-c="valv">Electrov&aacute;lvula &middot; 400 mA</button>
            <button type="button" data-c="tira">Tira LED &middot; 800 mA</button>
          </div>
        </div>
        <div class="escena-barra">
          <span class="escena-titulo">Transistor</span>
          <div class="seg" id="seg-tr-tipo">
            <button type="button" data-t="bc547" aria-pressed="true">BC547</button>
            <button type="button" data-t="tip120">TIP120 (Darlington)</button>
          </div>
          <div class="seg">
            <label class="ctrl" style="margin:0">
              <span>Diodo de rueda libre</span>
              <input id="tr-diodo" type="checkbox" checked>
            </label>
          </div>
        </div>
        <div class="escena-barra">
          <label class="ctrl" style="flex:1">
            <span>Resistencia de base</span>
            <input id="tr-rb" type="range" min="0" max="10" value="5" step="1">
            <b id="tr-rb-val">1 k&#8486;</b>
          </label>
          <div class="seg" id="seg-tr-pin">
            <button type="button" data-p="on" aria-pressed="true">Pin a 5 V</button>
            <button type="button" data-p="off">Pin a 0 V</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 430" id="svg-tr" role="img"
               aria-label="Un transistor NPN gobernando una carga desde un pin de Arduino, con las corrientes calculadas"></svg>
        </div>
        <div class="pie" id="pie-tr"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-tr');
        if(!svg) return;
        var pie = document.getElementById('pie-tr');
        var segC = document.getElementById('seg-tr-carga');
        var segT = document.getElementById('seg-tr-tipo');
        var segP = document.getElementById('seg-tr-pin');
        var rbIn = document.getElementById('tr-rb');
        var rbTx = document.getElementById('tr-rb-val');
        var diIn = document.getElementById('tr-diodo');

        var VCC = 5, VPIN = 5, PIN_MAX = 0.020;   /* 20 mA por pin, en amperios */
        var T_CORTE = 1e-6;                        /* lo que tarda en cortar, 1 us */

        /* Cada carga con lo suyo. La inductancia es el orden de magnitud de la
           bobina que lleva dentro: un LED no lleva ninguna. */
        var CARGAS = {
          led:   {n:'LED',            i:0.020, L:0,      sim:'led'},
          bomba: {n:'Bomba de riego', i:0.250, L:0.005,  sim:'motor'},
          valv:  {n:'Electrov\\u00e1lvula', i:0.400, L:0.100, sim:'bobina'},
          tira:  {n:'Tira LED',       i:0.800, L:0,      sim:'tira'}
        };
        var TRANS = {
          bc547:  {n:'BC547',  beta:100,  vbe:0.7, vces:0.2, imax:0.100, vceo:45},
          tip120: {n:'TIP120', beta:1000, vbe:1.6, vces:1.0, imax:5.000, vceo:60}
        };
        var RBS = [100, 220, 330, 470, 680, 1000, 1500, 2200, 3300, 4700, 10000];

        var carga = 'bomba', tipo = 'bc547', pinAlto = true, iRb = 5;

        function coma(n, d){ return n.toFixed(d).replace('.', ','); }
        function mA(a){
          if(a >= 1) return coma(a, 2) + ' A';
          return coma(a * 1000, a < 0.01 ? 2 : (a < 0.1 ? 1 : 0)) + ' mA';
        }
        function ohm(r){ return r >= 1000 ? coma(r / 1000, r % 1000 ? 1 : 0) + ' k\\u03a9'
                                          : r + ' \\u03a9'; }
        function volt(v){
          if(v >= 1000) return coma(v / 1000, 1) + ' kV';
          return coma(v, v < 10 ? 2 : 0) + ' V';
        }

        /* ------------------- toda la cuenta, en un sitio ------------------- */
        function calcula(){
          var C = CARGAS[carga], Q = TRANS[tipo], Rb = RBS[iRb];
          var Ib = pinAlto ? Math.max(0, (VPIN - Q.vbe) / Rb) : 0;
          var Ic_posible = Q.beta * Ib;
          var saturado = Ic_posible >= C.i;
          var Ic = saturado ? C.i : Ic_posible;
          /* En zona activa la carga se comporta como una resistencia: si solo
             pasa la mitad de la corriente, le sobra la mitad de la tension al
             transistor, y esa tension por esa corriente es calor. */
          var Vce = saturado ? Q.vces : VCC * (1 - Ic / C.i);
          var P = Vce * Ic;
          var margen = C.i > 0 ? Ic_posible / C.i : 0;
          var pico = C.L > 0 ? (diIn.checked ? VCC + 0.7 : C.L * C.i / T_CORTE) : 0;
          return {C:C, Q:Q, Rb:Rb, Ib:Ib, Ic:Ic, Ic_posible:Ic_posible,
                  saturado:saturado, Vce:Vce, P:P, margen:margen, pico:pico,
                  pinPasado: Ib > PIN_MAX,
                  transPasado: C.i > Q.imax,
                  energia: 0.5 * C.L * C.i * C.i};
        }

        /* ---------------------------- dibujo ---------------------------- */
        function caja(x, y, w, h, relleno, borde, grosor){
          return '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h
               + '" rx="2" fill="' + relleno + '" stroke="' + borde + '" stroke-width="'
               + grosor + '"></rect>';
        }
        function hilo(d, color, grosor, guion){
          return '<path d="' + d + '" fill="none" stroke="' + (color || 'var(--ink-soft)')
               + '" stroke-width="' + (grosor || 2) + '" stroke-linecap="round"'
               + (guion ? ' stroke-dasharray="' + guion + '"' : '') + '></path>';
        }
        function rot(x, y, txt, est, anchor){
          return '<text x="' + x + '" y="' + y + '" class="rotulo-svg"'
               + (anchor ? ' text-anchor="' + anchor + '"' : '')
               + (est ? ' style="' + est + '"' : '') + '>' + txt + '</text>';
        }
        function barra(x, y, w, etq, valor, frac, color){
          var s = rot(x, y + 4, etq, 'font-size:10px', 'end');
          s += caja(x + 8, y - 8, w, 16, 'var(--surface-2)', 'var(--line)', 1);
          s += caja(x + 8, y - 8, Math.max(2, w * Math.min(1, frac)), 16, color, color, 1);
          s += rot(x + 16 + w, y + 4, valor, 'font-size:11px;fill:var(--ink)');
          return s;
        }

        /* Simbolo de la carga. Las que llevan bobina la llevan DIBUJADA: es lo
           que explica el pico de la ultima parte de la escena. */
        function simboloCarga(sim, x, y, w, h, vivo){
          var cx = x + w / 2, cy = y + h / 2;
          var col = vivo ? 'var(--goo-verde)' : 'var(--line)';
          var s = caja(x, y, w, h, 'var(--surface)', col, 2);
          if(sim === 'motor'){
            s += '<circle cx="' + cx + '" cy="' + cy + '" r="17" fill="none" stroke="'
               + col + '" stroke-width="2"></circle>';
            s += rot(cx, cy + 6, 'M', 'font-size:17px;fill:var(--ink);font-weight:500', 'middle');
          } else if(sim === 'bobina'){
            var d = 'M' + (cx - 24) + ' ' + cy, i;
            for(i = 0; i < 4; i++)
              d += ' a6 6 0 0 1 12 0';
            s += hilo(d, col, 2);
            s += hilo('M' + (cx - 24) + ' ' + (cy + 9) + ' H' + (cx + 24), col, 2);
          } else {
            /* LED: triangulo con la barra y las dos flechitas de luz */
            s += '<path d="M' + (cx - 10) + ' ' + (cy - 10) + ' L' + (cx - 10) + ' '
               + (cy + 10) + ' L' + (cx + 8) + ' ' + cy + ' Z" fill="none" stroke="'
               + col + '" stroke-width="2"></path>';
            s += hilo('M' + (cx + 8) + ' ' + (cy - 11) + ' V' + (cy + 11), col, 2);
            s += hilo('M' + (cx + 6) + ' ' + (cy - 14) + ' l10 -8', col, 1.5);
            s += hilo('M' + (cx + 12) + ' ' + (cy - 10) + ' l10 -8', col, 1.5);
          }
          return s;
        }

        function pinta(){
          var r = calcula(), s = '', i;
          var vivo = r.Ic > 0.001;
          /* el camino colector-emisor solo se pinta de "abierto del todo" si
             ademas el montaje es sano: si el transistor no aguanta o el pin va
             sobrecargado, el dibujo no puede decir que todo va bien */
          var sano = r.saturado && !r.transPasado && !r.pinPasado;

          /* ===================== el circuito ===================== */
          s += rot(16, 22, 'EL CIRCUITO', 'font-size:10.5px');
          s += hilo('M60 46 H300');
          s += rot(60, 34, '+5 V', 'font-size:10.5px;fill:var(--goo-rojo)');

          /* carga */
          s += hilo('M250 46 V74');
          s += simboloCarga(r.C.sim, 212, 74, 76, 66, vivo);
          s += rot(296, 100, r.C.n, 'font-size:10px;fill:var(--ink)');
          s += rot(296, 114, mA(r.C.i), 'font-size:9.5px');
          s += hilo('M250 140 V168');

          /* diodo de rueda libre, en paralelo con la carga y al reves */
          if(diIn.checked){
            s += hilo('M250 60 H168 V92');
            s += '<path d="M156 122 L180 122 L168 100 Z" fill="none" stroke="var(--goo-verde)" stroke-width="2"></path>';
            s += hilo('M156 100 H180', 'var(--goo-verde)', 2.5);
            s += hilo('M168 122 V154 H250', 'var(--goo-verde)', 2);
            s += rot(150, 116, 'diodo', 'font-size:9.5px;fill:var(--goo-verde)', 'end');
          } else {
            s += rot(150, 116, 'sin diodo', 'font-size:9.5px;fill:var(--goo-rojo)', 'end');
            s += hilo('M168 96 l14 14 M182 96 l-14 14', 'var(--goo-rojo)', 2);
          }

          /* transistor NPN */
          s += '<circle cx="234" cy="215" r="30" fill="var(--surface)" stroke="var(--ink-soft)" stroke-width="1.5"></circle>';
          s += hilo('M226 199 V231', 'var(--ink)', 3.5);
          s += hilo('M200 215 H226', 'var(--ink)', 2);
          s += hilo('M226 205 L250 193 V168', sano ? 'var(--goo-verde)' : 'var(--ink-soft)',
                    sano ? 2.5 : 2);
          s += hilo('M226 225 L250 237 V282', sano ? 'var(--goo-verde)' : 'var(--ink-soft)',
                    sano ? 2.5 : 2);
          /* la flecha del emisor, que es lo que dice que es NPN */
          s += '<path d="M246 235 l-11 -3 l3 9 Z" fill="var(--ink)"></path>';
          s += rot(268, 172, r.Q.n, 'font-size:11px;fill:var(--ink);font-weight:500');
          /* las tres patillas, rotuladas donde salen */
          s += rot(258, 188, 'C', 'font-size:10.5px;fill:var(--ink)');
          s += rot(258, 254, 'E', 'font-size:10.5px;fill:var(--ink)');
          s += rot(189, 208, 'B', 'font-size:10.5px;fill:var(--ink)');

          /* resistencia de base y pin */
          s += caja(128, 205, 56, 20, 'var(--surface)', 'var(--ink-soft)', 2);
          s += rot(156, 199, 'Rb = ' + ohm(r.Rb), 'font-size:10px;fill:var(--ink)', 'middle');
          s += hilo('M184 215 H200', pinAlto ? 'var(--goo-azul)' : 'var(--line)', 2);
          s += hilo('M72 215 H128', pinAlto ? 'var(--goo-azul)' : 'var(--line)', 2);
          s += caja(16, 200, 56, 30, pinAlto ? 'var(--accent-soft)' : 'var(--surface)',
                    pinAlto ? 'var(--goo-azul)' : 'var(--line)', 2);
          s += rot(44, 220, 'D9', 'font-size:13px;fill:var(--ink);font-weight:500', 'middle');
          s += rot(44, 190, pinAlto ? '5 V' : '0 V', 'font-size:10px;fill:'
                   + (pinAlto ? 'var(--goo-azul)' : 'var(--ink-soft)'), 'middle');

          /* masa comun: el Arduino y la carga tienen que compartirla */
          s += hilo('M250 282 V296 H40 V230');
          s += hilo('M237 296 H263', 'var(--ink-soft)', 2.5);
          s += hilo('M241 301 H259', 'var(--ink-soft)', 2);
          s += hilo('M245 306 H255', 'var(--ink-soft)', 2);
          s += rot(150, 316, 'la masa es la MISMA para los dos', 'font-size:9px', 'middle');

          /* ==================== panel de cuentas ==================== */
          s += rot(352, 22, 'LAS CUENTAS', 'font-size:10.5px');

          var maxI = Math.max(r.C.i, PIN_MAX);
          s += rot(352, 62, 'CORRIENTE DE LA CARGA', 'font-size:9.5px');
          s += barra(470, 78, 84, 'la carga pide', mA(r.C.i), r.C.i / maxI,
                     r.C.i > PIN_MAX ? 'var(--goo-rojo)' : 'var(--goo-verde)');
          s += barra(470, 106, 84, 'un pin da', mA(PIN_MAX), PIN_MAX / maxI, 'var(--goo-azul)');

          var Ibnec = r.C.i / r.Q.beta;
          var maxB = Math.max(r.Ib, Ibnec, 1e-6);
          s += rot(352, 134, 'CORRIENTE DE BASE', 'font-size:9.5px');
          s += barra(470, 150, 84, 'da la Rb', mA(r.Ib), r.Ib / maxB,
                     r.pinPasado ? 'var(--goo-rojo)' : 'var(--goo-azul)');
          s += barra(470, 178, 84, 'hace falta', mA(Ibnec), Ibnec / maxB, 'var(--ink-soft)');

          /* caja de estado */
          /* El detalle cabe en 42 caracteres: la caja mide 272 px y Roboto
             Mono a 10 px gasta unos 6 px por caracter. */
          var estado, colE, detalle;
          if(r.transPasado){
            estado = 'ESTE TRANSISTOR NO AGUANTA'; colE = 'var(--goo-rojo)';
            detalle = 'admite ' + mA(r.Q.imax) + ' y piden ' + mA(r.C.i);
          } else if(r.pinPasado){
            estado = 'EL PIN VA SOBRECARGADO'; colE = 'var(--goo-rojo)';
            detalle = 'la base pide ' + mA(r.Ib) + ' y el pin da ' + mA(PIN_MAX);
          } else if(!pinAlto){
            estado = 'APAGADO'; colE = 'var(--ink-soft)';
            detalle = 'sin base no pasa nada por el colector';
          } else if(r.saturado){
            estado = 'SATURADO \\u00b7 margen \\u00d7' + coma(r.margen, 1);
            colE = 'var(--goo-verde)';
            detalle = 'Vce = ' + volt(r.Vce) + ' \\u00b7 calienta '
                    + coma(r.P * 1000, 0) + ' mW';
          } else {
            estado = 'A MEDIO ABRIR (zona activa)'; colE = 'var(--goo-amarillo)';
            detalle = 'pasan ' + mA(r.Ic) + ' \\u00b7 calienta '
                    + coma(r.P * 1000, 0) + ' mW';
          }
          s += caja(352, 206, 272, 60, 'var(--surface)', colE, 2);
          s += rot(364, 230, estado, 'font-size:12px;fill:' + colE + ';font-weight:500');
          s += rot(364, 250, detalle, 'font-size:10px');

          /* ============ el pico de apagado, escala logaritmica ============ */
          s += rot(352, 292, 'LO QUE APARECE AL CORTAR', 'font-size:9.5px');
          var LX = 372, RX = 616, YB = 372;
          /* de 1 V a 100 kV: cinco decadas */
          var lg = function(v){ return Math.max(0, Math.min(1, Math.log(Math.max(v, 1)) / Math.LN10 / 5)); };
          s += hilo('M' + LX + ' ' + YB + ' H' + RX, 'var(--line)', 1.5);
          var decs = [[1, '1 V'], [10, '10 V'], [100, '100 V'], [1000, '1 kV'],
                      [10000, '10 kV'], [100000, '100 kV']];
          for(i = 0; i < decs.length; i++){
            var xd = LX + lg(decs[i][0]) * (RX - LX);
            s += hilo('M' + xd.toFixed(1) + ' ' + YB + ' V' + (YB + 5), 'var(--line)', 1.5);
            s += rot(xd, YB + 18, decs[i][1], 'font-size:9px', 'middle');
          }
          /* lo que aguanta el transistor */
          var xv = LX + lg(r.Q.vceo) * (RX - LX);
          s += hilo('M' + xv.toFixed(1) + ' ' + (YB - 46) + ' V' + YB, 'var(--goo-rojo)', 1.5, '4 3');
          s += rot(xv, YB - 50, 'aguanta ' + r.Q.vceo + ' V',
                   'font-size:9px;fill:var(--goo-rojo)', 'middle');

          if(r.C.L === 0){
            s += rot(LX, YB - 20, 'sin bobina no hay pico', 'font-size:10.5px');
          } else {
            var xp = LX + lg(r.pico) * (RX - LX);
            var mata = r.pico > r.Q.vceo;
            s += caja(LX, YB - 26, Math.max(2, xp - LX), 18,
                      mata ? 'var(--goo-rojo)' : 'var(--goo-verde)',
                      mata ? 'var(--goo-rojo)' : 'var(--goo-verde)', 1);
            s += rot(Math.min(xp + 6, RX - 4), YB - 12, volt(r.pico),
                     'font-size:11px;fill:var(--ink);font-weight:500',
                     xp > RX - 70 ? 'end' : 'start');
            if(!pinAlto && mata)
              s += rot(616, YB - 58, 'ADI\\u00d3S TRANSISTOR',
                       'font-size:11px;fill:var(--goo-rojo);font-weight:500', 'end');
          }

          svg.innerHTML = s;

          /* ========================== el pie ========================== */
          var txt = '';
          if(r.transPasado){
            txt = '<b>El ' + r.Q.n + ' no vale para esta carga.</b> Admite como mucho '
                + mA(r.Q.imax) + ' por el colector y aqu&iacute; hacen falta ' + mA(r.C.i)
                + '. No es cuesti&oacute;n de darle m&aacute;s base: hay que cambiar de transistor. '
                + 'Prueba el TIP120.';
          } else if(r.pinPasado){
            txt = '<b>Cuidado: la base se est&aacute; llevando ' + mA(r.Ib) + ' del pin</b>, y un pin '
                + 'de Arduino da ' + mA(PIN_MAX) + '. Con una Rb tan peque&ntilde;a el problema se '
                + 'ha movido: ya no lo tiene el motor, lo tiene el pin. Sube la Rb.';
          } else if(!pinAlto){
            txt = 'Pin a 0 V: sin corriente de base, el transistor <b>no conduce</b> y la carga '
                + 'est&aacute; parada. Vuelve a ponerlo a 5 V y mira las cuatro barras.';
          } else {
            txt = 'Ib = (5 V &minus; ' + coma(r.Q.vbe, 1) + ' V) / ' + ohm(r.Rb) + ' = <b>'
                + mA(r.Ib) + '</b>. Con &beta; = ' + r.Q.beta + ', el transistor puede dejar pasar '
                + 'hasta ' + r.Q.beta + ' &times; ' + mA(r.Ib) + ' = <b>' + mA(r.Ic_posible)
                + '</b>, y la carga pide ' + mA(r.C.i) + '. ';
            if(r.saturado)
              txt += 'Sobra: el transistor est&aacute; <b>saturado</b> con un margen de <b>&times;'
                   + coma(r.margen, 1) + '</b>, se comporta como un interruptor cerrado '
                   + '(Vce = ' + volt(r.Vce) + ') y apenas se calienta ('
                   + coma(r.P * 1000, 0) + ' mW). Un montaje serio busca un margen de 5 a 10.';
            else
              txt += '<b>No llega</b>: el transistor se queda a medio abrir, solo pasan '
                   + mA(r.Ic) + ' y le sobran ' + volt(r.Vce) + ', que se convierten en <b>'
                   + coma(r.P * 1000, 0) + ' mW de calor</b> dentro de una c&aacute;psula del '
                   + 'tama&ntilde;o de un guisante. Baja la Rb.';
          }

          if(r.C.L > 0){
            txt += '<br>Al cortar, la bobina de ' + r.C.n.toLowerCase() + ' ('
                 + coma(r.C.L * 1000, 0) + ' mH) no deja de dar corriente de golpe: '
                 + 'V = L &middot; &Delta;I / &Delta;t = ' + coma(r.C.L * 1000, 0) + ' mH &middot; '
                 + mA(r.C.i) + ' / 1 &micro;s = <b>' + volt(r.C.L * r.C.i / T_CORTE) + '</b>. ';
            if(diIn.checked)
              txt += 'Con el <b>diodo de rueda libre</b> esa corriente se da la vuelta por el '
                   + 'diodo en vez de por el transistor, y la punta se queda en <b>'
                   + volt(r.pico) + '</b>: los 5 V de la alimentaci&oacute;n m&aacute;s los 0,7 del '
                   + 'diodo. Los ' + coma(r.energia * 1e6, 0) + ' &micro;J que llevaba dentro la '
                   + 'bobina se gastan en calentar el diodo, que para eso est&aacute;.';
            else
              txt += 'Sin diodo, esa punta se la come el transistor, que aguanta ' + r.Q.vceo
                   + ' V. <b>Marca la casilla del diodo</b> y mira la barra.';
          }

          pie.innerHTML = txt
            + '<br><span style="font-size:12.5px">Los datos de los transistores son los de sus '
            + 'hojas de caracter&iacute;sticas (&beta; tomada por lo bajo, que es como se dise&ntilde;a). '
            + 'El tiempo de corte de <b>1 &micro;s</b> y las inductancias son &oacute;rdenes de magnitud '
            + 'de estos componentes, no medidas de uno concreto: lo que ense&ntilde;a esta escena es '
            + '<b>de qu&eacute; tama&ntilde;o</b> es el problema, no la cifra exacta. En la realidad la '
            + 'punta nunca llega a esos kilovoltios, porque <b>algo se rompe antes</b>, y ese algo '
            + 'es el transistor.</span>';
        }

        function refrescaRb(){ rbTx.innerHTML = ohm(RBS[iRb]).replace('\\u03a9', '&#8486;'); }
        function pulsa(cont, attr, fn){
          cont.addEventListener('click', function(e){
            var b = e.target.closest('button[' + attr + ']');
            if(!b) return;
            cont.querySelectorAll('button').forEach(function(x){
              x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
            });
            fn(b.getAttribute(attr));
            pinta();
          });
        }
        pulsa(segC, 'data-c', function(v){ carga = v; });
        pulsa(segT, 'data-t', function(v){ tipo = v; });
        pulsa(segP, 'data-p', function(v){ pinAlto = (v === 'on'); });
        rbIn.addEventListener('input', function(){ iRb = +rbIn.value; refrescaRb(); pinta(); });
        diIn.addEventListener('change', pinta);

        refrescaRb();
        pinta();
      })();
      </script>
'''
