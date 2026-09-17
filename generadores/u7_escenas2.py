# -*- coding: utf-8 -*-
"""Las tres escenas interactivas de las sesiones 4, 5 y 6 de la U7.

Mismo criterio que u7_escenas.py: SVG y JavaScript a mano, sin librerias, y
todo numero que aparece en pantalla sale de una cuenta hecha en el momento.
Cada escena dice arriba de que tamano es su lienzo y como se reparte.

Las tres calculan de verdad:
  · la del conversor mide el error de cuantificacion muestra a muestra;
  · la del planificador SIMULA el reparto por turnos y cronometra el resultado;
  · la del diagnostico filtra el conjunto de sospechosos con cada respuesta.
"""

# ---------------------------------------------------------------------------
# S4 · Del mundo a los numeros: muestreo y cuantificacion
#
# Lienzo 640 x 366.
#   Ejes   x  64..604 (540 px = 1 milisegundo)
#          y  44..244 (200 px = 5 V  ->  40 px por voltio)
#   Rotulos del eje de tiempos en y 260, y el titulillo de la tira en y 286:
#          26 px entre lineas de 10 px, que es lo que hace falta para que no se
#          toquen (las dos empiezan en x = 64).
#   Tira de lo que se guarda: 12 casillas de 42 px con 3 de hueco, y 296..336
#          -> 12*45 - 3 = 537 <= 540.  x_i = 64 + 45*i
#   El "y N mas" NO cabe detras de la casilla 12 (sobraban 33 px de 540): va
#          alineado a la derecha en la linea del titulillo.
#
# La senal es la misma siempre (si cambiara al tocar los botones no se podria
# comparar):   v(t) = 2,5 + 1,6 sen(2 pi t) + 0,6 sen(6 pi t + 1),  t en [0,1] ms
#   -> un tono de 1 kHz con un armonico de 3 kHz encima. Su maximo teorico es
#      2,5 + 2,2 = 4,7 V y su minimo 0,3 V: cabe entera en la escala de 0 a 5 V
#      sin recortarse por arriba ni por abajo, que es lo que se busca.
#   -> los 3 kHz estan elegidos a proposito: la opcion mas floja son 8 medidas
#      en 1 ms, o sea 8.000 por segundo, que es MAS del doble de 3 kHz. Asi
#      ninguno de los tres ajustes cae por debajo de Nyquist y la escena nunca
#      ensena aliasing, que a esta edad solo confundiria: lo que se ve empeorar
#      es el error de cuantificacion, que es de lo que va la sesion.
#
# Cuantificacion: con n bits hay 2^n valores, que se reparten los 5 V en
#   2^n - 1 escalones. El error maximo posible es medio escalon; el error MEDIO
#   que sale en pantalla no es ese, es la media de los errores reales de las
#   muestras, calculada en el momento.
# ---------------------------------------------------------------------------
ESCENA_ADC = u'''
      <div class="escena" id="esc-adc">
        <div class="escena-barra">
          <span class="escena-titulo">De la onda a la lista de n&uacute;meros</span>
          <div class="seg" id="seg-adc-bits">
            <button type="button" data-b="2">2 bits</button>
            <button type="button" data-b="4" aria-pressed="true">4 bits</button>
            <button type="button" data-b="8">8 bits</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 366" id="svg-adc" role="img"
               aria-label="Una onda continua medida a intervalos y anotada con un n&uacute;mero entero en cada medida"></svg>
        </div>
        <div class="escena-barra" id="seg-adc-mu-caja">
          <span class="escena-titulo">Cada cu&aacute;nto se mira</span>
          <div class="seg" id="seg-adc-mu">
            <button type="button" data-m="8">8 medidas</button>
            <button type="button" data-m="16" aria-pressed="true">16 medidas</button>
            <button type="button" data-m="32">32 medidas</button>
          </div>
        </div>
        <div class="pie" id="pie-adc"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-adc');
        if(!svg) return;
        var pie  = document.getElementById('pie-adc');
        var segB = document.getElementById('seg-adc-bits');
        var segM = document.getElementById('seg-adc-mu');

        var X0 = 64, X1 = 604, Y0 = 44, Y1 = 244;   /* caja de los ejes */
        var VMAX = 5;                                /* el sensor da de 0 a 5 V */
        var bits = 4, muestras = 16;

        /* La onda. t va de 0 a 1 y son los mil primeros microsegundos. */
        function onda(t){
          return 2.5 + 1.6 * Math.sin(2 * Math.PI * t)
                     + 0.6 * Math.sin(6 * Math.PI * t + 1);
        }
        function px(t){ return X0 + (X1 - X0) * t; }
        function py(v){ return Y1 - (Y1 - Y0) * v / VMAX; }

        function es(x, dec){
          return x.toFixed(dec).replace('.', ',');
        }
        function miles(x){
          return Math.round(x).toLocaleString('es-ES');
        }

        /* Todo lo que la escena dice sale de aqui: se mide, se redondea al
           escalon mas cercano y se compara con lo que habia de verdad.      */
        function calcula(){
          var niveles = Math.pow(2, bits);
          var escalon = VMAX / (niveles - 1);
          var m = [], suma = 0, peor = 0;
          for(var i = 0; i < muestras; i++){
            var t = i / muestras;
            var v = onda(t);
            var codigo = Math.round(v / escalon);
            if(codigo < 0) codigo = 0;
            if(codigo > niveles - 1) codigo = niveles - 1;
            var rec = codigo * escalon;
            var err = Math.abs(v - rec);
            suma += err;
            if(err > peor) peor = err;
            m.push({t:t, v:v, codigo:codigo, rec:rec, err:err});
          }
          return {niveles:niveles, escalon:escalon, m:m,
                  medio:suma / muestras, peor:peor,
                  porSeg:muestras * 1000,                    /* 1 ms de ventana */
                  bytesSeg:muestras * 1000 * bits / 8};
        }

        function pinta(){
          var R = calcula(), m = '', i;

          /* ---- rejilla de escalones: solo si se pueden contar ---- */
          if(R.niveles <= 16){
            for(i = 0; i < R.niveles; i++){
              var y = py(i * R.escalon);
              m += '<path d="M' + X0 + ' ' + y.toFixed(1) + ' H' + X1 + '" stroke="var(--line-soft)" '
                 + 'stroke-width="1" stroke-dasharray="2 4"></path>';
            }
          }

          /* ---- ejes ---- */
          m += '<path d="M' + X0 + ' ' + Y0 + ' V' + Y1 + ' H' + X1 + '" fill="none" '
             + 'stroke="var(--line)" stroke-width="1.5"></path>';
          for(i = 0; i <= 5; i++){
            m += '<text x="' + (X0 - 8) + '" y="' + (py(i) + 4) + '" text-anchor="end" '
               + 'class="rotulo-svg" style="font-size:10px">' + i + ' V</text>';
          }
          m += '<text x="' + X0 + '" y="' + (Y1 + 16) + '" class="rotulo-svg" '
             + 'style="font-size:10px">0</text>';
          m += '<text x="' + X1 + '" y="' + (Y1 + 16) + '" text-anchor="end" class="rotulo-svg" '
             + 'style="font-size:10px">1 mil\\u00e9sima de segundo</text>';
          m += '<text x="' + X0 + '" y="' + (Y0 - 14) + '" class="rotulo-svg" '
             + 'style="font-size:10px;fill:var(--c-analog)">LO QUE LLEGA DEL MICR\\u00d3FONO</text>';
          m += '<text x="' + X1 + '" y="' + (Y0 - 14) + '" text-anchor="end" class="rotulo-svg" '
             + 'style="font-size:10px;fill:var(--c-digital)">LO QUE GUARDA LA M\\u00c1QUINA</text>';

          /* ---- la onda de verdad: 270 trozos, que a esta escala es una curva ---- */
          var d = '';
          for(i = 0; i <= 270; i++){
            var t = i / 270;
            d += (i ? ' L' : 'M') + px(t).toFixed(1) + ' ' + py(onda(t)).toFixed(1);
          }
          m += '<path d="' + d + '" fill="none" stroke="var(--c-analog)" stroke-width="2"></path>';

          /* ---- la escalera: cada medida se mantiene hasta la siguiente ---- */
          var e = '';
          for(i = 0; i < R.m.length; i++){
            var xa = px(R.m[i].t), xb = px((i + 1) / muestras), yv = py(R.m[i].rec);
            e += (i ? ' L' : 'M') + xa.toFixed(1) + ' ' + yv.toFixed(1)
               + ' L' + xb.toFixed(1) + ' ' + yv.toFixed(1);
          }
          m += '<path d="' + e + '" fill="none" stroke="var(--c-digital)" stroke-width="2"></path>';

          /* ---- el error de cada medida, dibujado a escala ---- */
          for(i = 0; i < R.m.length; i++){
            var x = px(R.m[i].t);
            m += '<path d="M' + x.toFixed(1) + ' ' + py(R.m[i].v).toFixed(1)
               + ' V' + py(R.m[i].rec).toFixed(1) + '" stroke="var(--c-analog)" '
               + 'stroke-width="1" stroke-dasharray="2 2" opacity=".8"></path>';
            m += '<circle cx="' + x.toFixed(1) + '" cy="' + py(R.m[i].v).toFixed(1)
               + '" r="2.6" fill="var(--c-analog)"></circle>';
          }

          /* ---- la tira de lo que de verdad se guarda ---- */
          m += '<text x="64" y="286" class="rotulo-svg" style="font-size:10px">'
             + 'LO QUE SE ESCRIBE EN LA MEMORIA</text>';
          var caben = Math.min(12, R.m.length);
          if(R.m.length > caben){
            m += '<text x="604" y="286" text-anchor="end" class="rotulo-svg" '
               + 'style="font-size:10px">\\u2026 y ' + (R.m.length - caben)
               + ' MEDIDAS M\\u00c1S</text>';
          }
          for(i = 0; i < caben; i++){
            var cx = 64 + i * 45;
            m += '<rect x="' + cx + '" y="296" width="42" height="40" rx="2" '
               + 'fill="var(--surface-2)" stroke="var(--line)" stroke-width="1"></rect>';
            m += '<text x="' + (cx + 21) + '" y="322" text-anchor="middle" class="rotulo-svg" '
               + 'style="font-size:15px;fill:var(--c-digital);font-weight:500">'
               + R.m[i].codigo + '</text>';
          }
          m += '<text x="64" y="354" class="rotulo-svg" style="font-size:10.5px">'
             + 'n\\u00fameros enteros de 0 a ' + (R.niveles - 1)
             + ' \\u00b7 ni ondas, ni voltios: n\\u00fameros</text>';

          svg.innerHTML = m;

          pie.innerHTML =
              'Con <b>' + bits + ' bits</b> hay <b>' + R.niveles + ' valores</b> posibles, que se '
            + 'reparten los 5 V en <b>' + (R.niveles - 1) + ' escalones</b> de <b>' + es(R.escalon, 3)
            + ' V</b> cada uno. Midiendo <b>' + muestras + ' veces</b> en esa mil\\u00e9sima de segundo, '
            + 'el error <b>medio</b> que sale es de <b>' + es(R.medio, 3) + ' V</b> y el peor de todos, '
            + '<b>' + es(R.peor, 3) + ' V</b>.'
            + '<br><span style="font-size:12.5px">A ese ritmo ser\\u00edan <b>'
            + miles(R.porSeg) + ' medidas por segundo</b>, o sea <b>' + miles(R.bytesSeg)
            + ' bytes cada segundo</b> y <b>' + es(R.bytesSeg * 60 / 1e6, 2)
            + ' MB por minuto</b>. Sube los bits y baja el error; sube las medidas y la escalera se '
            + 'pega m\\u00e1s a la curva. Las dos cosas <b>cuestan sitio</b>, y ah\\u00ed est\\u00e1 '
            + 'todo el problema.</span>';
        }

        function elige(seg, b){
          seg.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
        }
        segB.addEventListener('click', function(e){
          var b = e.target.closest('button[data-b]'); if(!b) return;
          elige(segB, b); bits = +b.dataset.b; pinta();
        });
        segM.addEventListener('click', function(e){
          var b = e.target.closest('button[data-m]'); if(!b) return;
          elige(segM, b); muestras = +b.dataset.m; pinta();
        });
        pinta();
      })();
      </script>
'''


# ---------------------------------------------------------------------------
# S5 · El reparto de la CPU
#
# Lienzo 640 x 326.
#   Franja de tiempo (el reparto):  x 20..620 (600 px)   y 44..96
#   Debajo de la franja van DOS lineas -los extremos del eje y la nota del gris-
#   antes del titulillo de la leyenda, que por eso no puede subir de y = 162.
#   Leyenda: cinco filas de 30 px a partir de y = 170  ->  170..320
#
# La escena SIMULA el reparto por turnos (round robin) y cronometra lo que sale.
# Cambiar de programa no es gratis: hay que guardar donde iba uno y recuperar
# donde iba el otro. Se cobra C = 0,05 ms por cambio, que es el orden de
# magnitud de un cambio de contexto real contando el efecto sobre la cache.
#
# Los cinco programas y lo que piden suman 377 ms de CPU. Salen solos:
#   turno de 0,1 ms -> la tecla responde en ~15 ms, pero un tercio de la
#                      maquina se va en cambiar de programa;
#   turno de 100 ms -> la maquina se aprovecha entera y la tecla tarda ~0,26 s,
#                      que ya se nota al escribir.
# ---------------------------------------------------------------------------
ESCENA_PLAN = u'''
      <div class="escena" id="esc-plan">
        <div class="escena-barra">
          <span class="escena-titulo">Una CPU, cinco programas: qui&eacute;n entra y cu&aacute;nto</span>
          <div class="seg" id="seg-plan">
            <button type="button" data-q="0.1">Turnos de 0,1 ms</button>
            <button type="button" data-q="10" aria-pressed="true">de 10 ms</button>
            <button type="button" data-q="100">de 100 ms</button>
            <button type="button" data-q="nada">Sin repartir</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 326" id="svg-plan" role="img"
               aria-label="Reparto del tiempo de una CPU entre cinco programas, con el tiempo que tarda cada uno en terminar"></svg>
        </div>
        <div class="pie" id="pie-plan"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-plan');
        if(!svg) return;
        var pie = document.getElementById('pie-plan');
        var seg = document.getElementById('seg-plan');

        /* Lo que pide cada programa de CPU, en milisegundos. La tecla va la
           ultima de la cola a proposito: es la que menos pide y la que mas
           prisa tiene, que es el caso incomodo de verdad.                    */
        var P = [
          {n:'Antivirus',      ms:120, c:'var(--goo-verde)'},
          {n:'Navegador',      ms:40,  c:'var(--goo-azul)'},
          {n:'Actualizaci\\u00f3n', ms:200, c:'var(--goo-amarillo)'},
          {n:'M\\u00fasica',        ms:15,  c:'var(--ink-soft)'},
          {n:'Tu tecla',       ms:2,   c:'var(--goo-rojo)'}
        ];
        var CAMBIO = 0.05;      /* ms que cuesta cambiar de programa */
        var X0 = 20, X1 = 620, YA = 44, HA = 52;
        var q = 10;             /* ms de turno; el texto 'nada' = sin repartir */

        function es(x, dec){ return x.toFixed(dec).replace('.', ','); }

        /* El reparto de verdad: se va dando turno a cada programa que aun tenga
           trabajo, y se cobra el cambio cada vez que entra otro.              */
        function simula(turno){
          var queda = P.map(function(p){ return p.ms; });
          var tramos = [], t = 0, util = 0, fin = P.map(function(){ return 0; });
          var vivo = function(){ return queda.some(function(r){ return r > 1e-9; }); };
          var vueltas = 0;
          while(vivo() && vueltas < 100000){
            vueltas++;
            for(var i = 0; i < P.length; i++){
              if(queda[i] <= 1e-9) continue;
              var d = (turno === null) ? queda[i] : Math.min(turno, queda[i]);
              tramos.push({i:i, t0:t, d:d});
              t += d; util += d; queda[i] -= d;
              if(queda[i] <= 1e-9) fin[i] = t;
              if(vivo()){ tramos.push({i:-1, t0:t, d:CAMBIO}); t += CAMBIO; }
            }
          }
          return {tramos:tramos, total:t, util:util, fin:fin,
                  cambios:tramos.filter(function(x){ return x.i < 0; }).length};
        }

        function pinta(){
          var turno = (q === 'nada') ? null : q;
          var R = simula(turno), m = '', i;

          /* Se dibujan los primeros tramos, no los miles que salen con turnos
             cortos: la franja es una ventana, y debajo pone de cuanto es.     */
          var n = Math.min(R.tramos.length, 130);
          var ventana = R.tramos[n - 1].t0 + R.tramos[n - 1].d;
          var ex = function(t){ return X0 + (X1 - X0) * t / ventana; };

          m += '<text x="' + X0 + '" y="28" class="rotulo-svg" style="font-size:10px">'
             + 'QUI\\u00c9N TIENE LA CPU, MILISEGUNDO A MILISEGUNDO</text>';

          for(i = 0; i < n; i++){
            var s = R.tramos[i], xa = ex(s.t0), w = Math.max(0.6, ex(s.t0 + s.d) - xa);
            m += '<rect x="' + xa.toFixed(2) + '" y="' + YA + '" width="' + w.toFixed(2)
               + '" height="' + HA + '" fill="'
               + (s.i < 0 ? 'var(--line)' : P[s.i].c) + '"></rect>';
          }
          m += '<rect x="' + X0 + '" y="' + YA + '" width="' + (X1 - X0) + '" height="' + HA
             + '" fill="none" stroke="var(--line)" stroke-width="1.5"></rect>';
          m += '<text x="' + X0 + '" y="' + (YA + HA + 16) + '" class="rotulo-svg" '
             + 'style="font-size:10px">0 ms</text>';
          m += '<text x="' + X1 + '" y="' + (YA + HA + 16) + '" text-anchor="end" '
             + 'class="rotulo-svg" style="font-size:10px">' + es(ventana, 2) + ' ms'
             + (R.tramos.length > n ? ' \\u00b7 de ' + es(R.total, 1) + ' ms en total' : '')
             + '</text>';
          m += '<rect x="' + X0 + '" y="' + (YA + HA + 24) + '" width="13" height="11" '
             + 'fill="var(--line)"></rect>';
          m += '<text x="' + (X0 + 19) + '" y="' + (YA + HA + 34) + '" class="rotulo-svg" '
             + 'style="font-size:10px">gris = cambiar de programa, que no calcula nada</text>';

          /* ---- la leyenda, con lo que ha tardado cada uno ---- */
          m += '<text x="' + X0 + '" y="162" class="rotulo-svg" style="font-size:10px">'
             + 'PROGRAMA \\u00b7 LO QUE PIDE \\u00b7 CU\\u00c1NDO ACABA</text>';
          for(i = 0; i < P.length; i++){
            var y = 170 + i * 30;
            m += '<rect x="' + X0 + '" y="' + y + '" width="14" height="14" rx="2" fill="'
               + P[i].c + '"></rect>';
            m += '<text x="' + (X0 + 24) + '" y="' + (y + 12) + '" class="rotulo-svg" '
               + 'style="font-size:12px;fill:var(--ink)">' + P[i].n + '</text>';
            m += '<text x="300" y="' + (y + 12) + '" text-anchor="end" class="rotulo-svg" '
               + 'style="font-size:11.5px">pide ' + P[i].ms + ' ms</text>';
            m += '<text x="' + X1 + '" y="' + (y + 12) + '" text-anchor="end" class="rotulo-svg" '
               + 'style="font-size:12px;fill:'
               + (i === 4 ? 'var(--goo-rojo);font-weight:500' : 'var(--ink)') + '">acaba a los '
               + es(R.fin[i], 1) + ' ms</text>';
            m += '<path d="M' + X0 + ' ' + (y + 22) + ' H' + X1 + '" stroke="var(--line-soft)" '
               + 'stroke-width="1"></path>';
          }

          svg.innerHTML = m;

          var rend = 100 * R.util / R.total;
          var tecla = R.fin[4];
          pie.innerHTML = (turno === null
              ? '<b>Sin repartir:</b> cada programa se queda la CPU hasta que acaba. '
              : '<b>Turnos de ' + es(turno, 1) + ' ms:</b> cada programa calcula ese rato y le toca al '
                + 'siguiente. ')
            + 'Tu tecla aparece en pantalla a los <b>' + es(tecla, 1) + ' ms</b>'
            + (tecla > 120 ? ' &mdash;eso ya se nota al escribir&mdash;' : '')
            + ', y de todo el tiempo transcurrido la m&aacute;quina dedica el <b>' + es(rend, 1)
            + ' %</b> a calcular: el resto se va en los <b>' + R.cambios.toLocaleString('es-ES')
            + ' cambios</b> de programa.'
            + '<br><span style="font-size:12.5px">Prueba los cuatro botones y mira las dos cifras a '
            + 'la vez: <b>no hay un valor bueno</b>. Turno corto, responde al momento y se gasta la '
            + 'm&aacute;quina en cambiar; turno largo, se aprovecha entera y se nota el tir&oacute;n. '
            + 'Los sistemas de verdad se quedan en unos pocos milisegundos, por esto mismo. Modelo '
            + 'simplificado: aqu&iacute; hay un solo n&uacute;cleo, nadie espera al disco y todos los '
            + 'programas valen lo mismo.</span>';
        }

        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-q]'); if(!b) return;
          seg.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
          q = (b.dataset.q === 'nada') ? 'nada' : +b.dataset.q;
          pinta();
        });
        pinta();
      })();
      </script>
'''


# ---------------------------------------------------------------------------
# S6 · Acotar la averia
#
# Lienzo 640 x 410.
#   Cadena: 7 cajas de 76 px con 11 de hueco -> 7*76 + 6*11 = 598 <= 600.
#           x_i = 21 + 87*i ; y 46..116
#   Pruebas: 6 filas de 32 px con 5 de hueco -> 6*37 - 5 = 217 ; y 146..363
#   Resumen: y 382 y 400
#
# La maquina tiene un eslabon roto, elegido al azar. Cada prueba mira si la
# senal llega hasta un punto: la respuesta NO se saca de una tabla escrita a
# mano, se CALCULA (llega hasta el punto j si el eslabon roto esta despues).
# Con cada respuesta se filtra el conjunto de sospechosos, y lo que cuenta la
# escena -cuantos quedan, cuantas pruebas llevas, cuantas hacian falta- sale
# de ese conjunto. El minimo teorico es techo(log2(7)) = 3.
# ---------------------------------------------------------------------------
ESCENA_DIAG = u'''
      <div class="escena" id="esc-diag">
        <div class="escena-barra">
          <span class="escena-titulo">Un ordenador que no arranca: ac&oacute;talo</span>
          <div class="seg" id="seg-diag">
            <button type="button" data-d="otra">&#9888; Otra aver&iacute;a</button>
            <button type="button" data-d="reset">&#8635; Empezar de nuevo</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 410" id="svg-diag" role="img"
               aria-label="Cadena de siete piezas de un ordenador y seis pruebas para averiguar en cu&aacute;l est&aacute; la aver&iacute;a"></svg>
        </div>
        <div class="pie" id="pie-diag"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-diag');
        if(!svg) return;
        var pie = document.getElementById('pie-diag');
        var seg = document.getElementById('seg-diag');

        /* La cadena de arranque, en orden. Cada eslabon necesita que el
           anterior funcione: por eso se puede partir por la mitad.        */
        var CADENA = [
          ['Corriente',  'enchufe'],
          ['Fuente',     'de la torre'],
          ['Placa',      'y CPU'],
          ['Memoria',    'RAM'],
          ['Disco',      'SSD'],
          ['Sistema',    'operativo'],
          ['Aplicaci\\u00f3n', 'el programa']
        ];
        /* Cada prueba comprueba que TODO lo anterior al corte funciona.
           Tope: 64 caracteres. Del principio del texto (x = 52) al borde
           izquierdo de la respuesta hay unos 460 px, y Roboto Mono a 11,5 px
           gasta 7,2 px por caracter. Con 69 se monta encima de "probar".   */
        var PRUEBAS = [
          '\\u00bfTiene corriente el enchufe? Prueba otro aparato en la regleta.',
          '\\u00bfSe enciende el piloto de la torre y gira el ventilador?',
          '\\u00bfDa el pitido de arranque y sale el logotipo de la BIOS?',
          '\\u00bfCuenta la BIOS toda la memoria que deber\\u00eda haber?',
          '\\u00bfAparece el disco en la lista de arranque de la BIOS?',
          '\\u00bfLlega hasta el escritorio del sistema operativo?'
        ];

        var roto, hechas, sospechosos;

        function nueva(){
          roto = 1 + Math.floor(Math.random() * CADENA.length);   /* 1..7 */
          hechas = {};
          sospechosos = [];
          for(var i = 1; i <= CADENA.length; i++) sospechosos.push(i);
          pinta();
        }

        /* La respuesta no esta escrita en ningun sitio: se deduce. La senal
           llega hasta el corte j si el eslabon roto viene despues.          */
        function responde(j){ return roto > j; }

        function prueba(j){
          if(hechas[j] !== undefined) return;
          var llega = responde(j);
          hechas[j] = llega;
          sospechosos = sospechosos.filter(function(k){
            return llega ? (k > j) : (k <= j);
          });
          pinta();
        }

        function pinta(){
          var m = '', i;
          var resuelto = (sospechosos.length === 1);
          var usadas = Object.keys(hechas).length;

          m += '<text x="21" y="28" class="rotulo-svg" style="font-size:10px">'
             + 'LA CADENA: CADA PIEZA NECESITA QUE FUNCIONE LA ANTERIOR</text>';

          for(i = 0; i < CADENA.length; i++){
            var x = 21 + i * 87, n = i + 1;
            var vivo = sospechosos.indexOf(n) >= 0;
            var culpable = resuelto && sospechosos[0] === n;
            m += '<rect x="' + x + '" y="46" width="76" height="70" rx="2" fill="'
               + (culpable ? 'var(--goo-rojo)' : (vivo ? 'var(--surface)' : 'var(--surface-2)'))
               + '" stroke="' + (culpable ? 'var(--goo-rojo)' : (vivo ? 'var(--goo-azul)' : 'var(--line)'))
               + '" stroke-width="' + (vivo ? 2 : 1) + '"' + (vivo ? '' : ' opacity=".55"') + '></rect>';
            var col = culpable ? '#fff' : (vivo ? 'var(--ink)' : 'var(--ink-soft)');
            m += '<text x="' + (x + 38) + '" y="66" text-anchor="middle" class="rotulo-svg" '
               + 'style="font-size:10px;fill:' + col + '">' + n + '</text>';
            m += '<text x="' + (x + 38) + '" y="88" text-anchor="middle" class="rotulo-svg" '
               + 'style="font-size:11.5px;font-weight:500;fill:' + col + '">' + CADENA[i][0] + '</text>';
            m += '<text x="' + (x + 38) + '" y="104" text-anchor="middle" class="rotulo-svg" '
               + 'style="font-size:9.5px;fill:' + col + '">' + CADENA[i][1] + '</text>';
            if(i < CADENA.length - 1){
              m += '<path d="M' + (x + 78) + ' 81 h7" stroke="var(--line)" stroke-width="1.5"></path>';
            }
          }

          /* ---- las seis pruebas ---- */
          for(i = 0; i < PRUEBAS.length; i++){
            var y = 146 + i * 37, r = hechas[i + 1];
            var hecho = (r !== undefined);
            m += '<g class="pr-fila" data-j="' + (i + 1) + '" style="cursor:'
               + (hecho || resuelto ? 'default' : 'pointer') + '">';
            m += '<rect x="20" y="' + y + '" width="600" height="32" rx="2" fill="'
               + (hecho ? 'var(--surface-2)' : 'var(--surface)') + '" stroke="'
               + (hecho ? (r ? 'var(--goo-verde)' : 'var(--goo-rojo)') : 'var(--line)')
               + '" stroke-width="1.5"></rect>';
            m += '<text x="34" y="' + (y + 21) + '" class="rotulo-svg" style="font-size:11px">'
               + (i + 1) + '</text>';
            m += '<text x="52" y="' + (y + 21) + '" class="rotulo-svg" style="font-size:11.5px;fill:'
               + (hecho ? 'var(--ink-soft)' : 'var(--ink)') + '">' + PRUEBAS[i] + '</text>';
            m += '<text x="606" y="' + (y + 21) + '" text-anchor="end" class="rotulo-svg" '
               + 'style="font-size:11.5px;font-weight:500;fill:'
               + (hecho ? (r ? 'var(--goo-verde)' : 'var(--goo-rojo)') : 'var(--ink-soft)') + '">'
               + (hecho ? (r ? 'S\\u00cd llega' : 'NO llega') : 'probar') + '</text>';
            m += '</g>';
          }

          var minimo = Math.ceil(Math.log(CADENA.length) / Math.log(2));
          m += '<text x="20" y="382" class="rotulo-svg" style="font-size:11.5px;fill:var(--ink)">'
             + 'Sospechosos: ' + sospechosos.length + ' de ' + CADENA.length
             + '  \\u00b7  pruebas usadas: ' + usadas
             + '  \\u00b7  con ' + minimo + ' bien elegidas se acota siempre</text>';
          m += '<text x="20" y="400" class="rotulo-svg" style="font-size:10.5px">'
             + (resuelto ? 'Aver\\u00eda acotada.'
                         : 'Elige la prueba que deje menos sospechosos salga lo que salga.')
             + '</text>';

          svg.innerHTML = m;

          if(resuelto){
            /* Cuantas habrian hecho falta yendo de una en una desde el principio. */
            var unaAuna = (roto < CADENA.length) ? roto : CADENA.length - 1;
            pie.innerHTML = '<b>Lo has acotado: la aver&iacute;a est&aacute; en la pieza '
              + sospechosos[0] + ', ' + CADENA[sospechosos[0] - 1][0].toLowerCase() + '.</b> '
              + 'Has gastado <b>' + usadas + (usadas === 1 ? ' prueba' : ' pruebas') + '</b>. '
              + 'Probando de una en una desde el principio habr&iacute;as necesitado <b>' + unaAuna
              + '</b>. Con siete piezas, <b>' + minimo + ' pruebas bien elegidas</b> bastan '
              + '<i>siempre</i>, salga la aver&iacute;a que salga, porque cada prueba parte en dos lo '
              + 'que queda. Dale a &laquo;otra aver&iacute;a&raquo; e int&eacute;ntalo empezando por '
              + 'la prueba 4.';
          } else if(usadas === 0){
            pie.innerHTML = 'Hay <b>una</b> pieza rota y no sabes cu&aacute;l: siete sospechosos. Cada '
              + 'prueba contesta <b>s&iacute; o no</b>, y con eso se van cayendo sospechosos. La '
              + 'pregunta no es &laquo;qu&eacute; toco primero&raquo;, es <b>qu&eacute; prueba me '
              + 'quita m&aacute;s dudas</b>.';
          } else {
            var ultima = Math.max.apply(null, Object.keys(hechas).map(Number));
            pie.innerHTML = 'Quedan <b>' + sospechosos.length + ' sospechosos</b>: '
              + sospechosos.map(function(k){ return CADENA[k - 1][0].toLowerCase(); }).join(', ')
              + '. ' + (hechas[ultima]
                  ? 'Como la se&ntilde;al <b>s&iacute;</b> llegaba hasta ah&iacute;, todo lo anterior '
                    + 'funciona y ya no hace falta volver a mirarlo.'
                  : 'Como la se&ntilde;al <b>no</b> llegaba, el fallo est&aacute; antes de ese punto: '
                    + 'lo de despu&eacute;s puede estar perfecto y no se sabr&iacute;a.');
          }
        }

        svg.addEventListener('click', function(e){
          var g = e.target.closest('.pr-fila'); if(!g) return;
          if(sospechosos.length === 1) return;
          prueba(+g.dataset.j);
        });
        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-d]'); if(!b) return;
          if(b.dataset.d === 'otra'){ nueva(); }
          else {
            hechas = {};
            sospechosos = [];
            for(var i = 1; i <= CADENA.length; i++) sospechosos.push(i);
            pinta();
          }
        });
        nueva();
      })();
      </script>
'''
