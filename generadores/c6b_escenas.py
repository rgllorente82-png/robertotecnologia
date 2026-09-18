# -*- coding: utf-8 -*-
"""4.o Tecnologia - Tema 6 - Escenas de las sesiones 5 y 6 (SEGUNDA MITAD).

  HISTORICO (S5)  Un dia entero de medidas del sensor del proyecto, con su
      ruido y sus picos, y CUATRO maneras de decidir con ellas: el ultimo
      valor, la media de N, la mediana de N y la tendencia. La escena dibuja
      las tres senales (la verdad, lo medido y el numero que la regla compara
      con el umbral) y mide lo que cuesta cada una: falsas alarmas, arranques
      de mas, retardo, episodios perdidos y BYTES de memoria. El panel de
      codigo se reescribe con la N que se elija.

  AVISO (S6)  Dos semanas del proyecto funcionando, con sus incidencias de
      verdad, una caida de red de nueve horas y la averia mas peligrosa de
      todas: que el aparato se quede mudo. Tres politicas de aviso (periodico,
      por evento, evento + latido) y el efecto de decidir con el ultimo valor
      o con la media. Mide mensajes, bytes, cuanto tarda una persona en
      enterarse, cuantas incidencias no se supieron nunca y si el silencio se
      descubre o no.

Prefijos CSS propios: mem-, avi-. Sin nombres que empiecen por test-.
Estas cadenas no pasan por ningun formateo con %.

El generador de numeros al azar es un Lehmer (MINSTD, x16807 mod 2^31-1): el
producto nunca pasa de 3,6e13, asi que cabe exacto en un double y JavaScript y
Python dan EXACTAMENTE la misma serie. Con el LCG de 1103515245 no ocurre, y
entonces el verificador no puede rehacer la cuenta.
"""

# ==========================================================================
# S5 - Decidir con el historico
# ==========================================================================
HISTORICO = u'''
      <div class="escena" id="esc-mem">
        <div class="escena-barra">
          <span class="escena-titulo">Un d&iacute;a entero de medidas &middot; y cuatro maneras de decidir con ellas</span>
          <div class="seg" id="seg-mem">
            <button type="button" data-p="0" aria-pressed="true">Riego</button>
            <button type="button" data-p="1">Ventilaci&oacute;n</button>
            <button type="button" data-p="2">L&aacute;mpara</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 700 280" id="svg-mem" role="img"
               aria-label="Un d&iacute;a de medidas del sensor, el n&uacute;mero que calcula la regla y las dos franjas que comparan lo que pasaba de verdad con lo que decidi&oacute; el programa"></svg>
          <div class="mem">
            <div class="mem-der">
              <div class="mem-fila">
                <label>Decido con</label>
                <div class="seg" id="regla-mem">
                  <button type="button" data-r="0" aria-pressed="true">el &uacute;ltimo valor</button>
                  <button type="button" data-r="1">la media</button>
                  <button type="button" data-r="2">la mediana</button>
                  <button type="button" data-r="3">la tendencia</button>
                </div>
              </div>
              <div class="mem-fila">
                <label for="mem-n">Guardo N medidas</label>
                <input type="range" id="mem-n" min="1" max="40" step="1" value="10">
                <span class="val" id="vn-mem"></span>
              </div>
              <div class="mem-fila">
                <label for="mem-u">Umbral</label>
                <input type="range" id="mem-u" min="450" max="800" step="5" value="600">
                <span class="val" id="vu-mem"></span>
              </div>
              <div class="mem-fila">
                <label>Cada medida en</label>
                <div class="seg" id="tipo-mem">
                  <button type="button" data-t="0" aria-pressed="true">int (2 B)</button>
                  <button type="button" data-t="1">byte, &divide;4 (1 B)</button>
                </div>
              </div>
              <label class="mem-chk"><input type="checkbox" id="mem-picos" checked>
                <span>meter los <b>picos</b> de un instante (alguien roza la sonda, pasa una
                sombra, se abre la puerta)</span></label>
              <div class="mem-tabla" id="tabla-mem"></div>
            </div>
            <div class="mem-izq">
              <p class="mem-rot">El programa, con la N que has puesto</p>
              <pre class="mem-cod" id="cod-mem"></pre>
            </div>
          </div>
          <p class="mem-lee" id="lee-mem"></p>
        </div>
        <div class="pie" id="pie-mem"></div>
      </div>

      <style>
      .mem{display:flex;gap:18px;flex-wrap:wrap;align-items:flex-start;margin-top:12px}
      .mem-der{flex:1 1 320px;min-width:290px}
      .mem-izq{flex:1 1 320px;min-width:280px}
      .mem-rot{font-family:var(--f-m);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;
        color:var(--ink-soft);margin:0 0 6px}
      .mem-cod{font-family:var(--f-m);font-size:11.5px;line-height:1.6;margin:0;
        white-space:pre-wrap;border:1.5px solid var(--line);border-radius:2px;background:var(--surface);
        padding:9px 11px;color:var(--ink)}
      .mem-fila{display:flex;align-items:center;gap:9px;flex-wrap:wrap;margin:0 0 9px;
        font-family:var(--f-m);font-size:12.5px;color:var(--ink)}
      .mem-fila label{min-width:116px}
      .mem-fila input[type="range"]{flex:1 1 110px;min-width:95px;accent-color:var(--goo-azul)}
      .mem-fila input[type="range"][disabled]{opacity:.4}
      .mem-fila .val{font-weight:500;color:var(--goo-azul);min-width:88px;text-align:right}
      .mem-fila .seg button{padding:5px 9px;font-size:11.5px}
      .mem-chk{display:flex;align-items:flex-start;gap:7px;font-family:var(--f-m);font-size:12px;
        color:var(--ink-soft);margin:0 0 9px;cursor:pointer;line-height:1.5}
      .mem-chk input{accent-color:var(--goo-azul);margin-top:2px}
      .mem-chk b{color:var(--ink)}
      .mem-tabla{border:1.5px solid var(--line);border-radius:2px;background:var(--surface);
        padding:9px 11px;font-family:var(--f-m);font-size:12px;line-height:1.7}
      .mem-tabla .f{display:flex;justify-content:space-between;gap:10px;align-items:baseline}
      .mem-tabla .f span:first-child{color:var(--ink-soft)}
      .mem-tabla .f b{color:var(--ink);font-weight:500;text-align:right;white-space:nowrap}
      .mem-tabla .f.top{border-top:1px solid var(--line-soft);margin-top:5px;padding-top:5px}
      .mem-tabla .mal b{color:var(--goo-rojo)}
      .mem-tabla .bien b{color:var(--goo-verde)}
      .mem-lee{font-family:var(--f-m);font-size:12.5px;line-height:1.75;color:var(--ink-soft);margin:12px 0 0}
      .mem-lee b{color:var(--ink)}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-mem');
        if(!svg) return;
        var caja = document.getElementById('esc-mem');
        var seg = document.getElementById('seg-mem');
        var segR = document.getElementById('regla-mem');
        var segT = document.getElementById('tipo-mem');
        var cN = document.getElementById('mem-n');
        var cU = document.getElementById('mem-u');
        var cPic = document.getElementById('mem-picos');
        var vn = document.getElementById('vn-mem');
        var vu = document.getElementById('vu-mem');
        var cod = document.getElementById('cod-mem');
        var tabla = document.getElementById('tabla-mem');
        var lee = document.getElementById('lee-mem');
        var pie = document.getElementById('pie-mem');

        /* ---- constantes del modelo ---- */
        var DT = 2;            /* minutos entre medidas */
        var NM = 720;          /* 24 h */
        var I0 = 40;           /* no se mide hasta que cabe el historico mas largo */
        var RUIDO = 12;        /* +- unidades de lectura */
        var PICOS = 6;         /* cuantos picos de un instante tiene el dia */
        var PICO0 = 300, PICOR = 400;   /* lo que sube un pico: de 300 a 699 unidades */
        var HOR = 15;          /* la tendencia mira 15 muestras (30 min) por delante */
        var ATRAS = 45;        /* tope al buscar hacia atras el arranque de un aviso */
        var RAM = 2048;

        var PROY = [
          {nom: 'Riego autom&aacute;tico', sensor: 'la sonda de humedad',
           sube: 'sube cuando la tierra se seca', acc: 'regar', u: 600,
           perfil: [[0, 430], [0.30, 500], [0.38, 520], [0.43, 660], [0.50, 680], [0.52, 380],
                    [0.80, 520], [0.90, 560], [0.94, 680], [1, 700]]},
          {nom: 'Aviso de aula mal ventilada', sensor: 'el sensor de temperatura y humedad',
           sube: 'sube cuando el aula se carga', acc: 'avisar de que hay que abrir', u: 600,
           perfil: [[0, 380], [0.20, 420], [0.30, 700], [0.45, 720], [0.50, 400],
                    [0.60, 690], [0.75, 710], [0.80, 400], [1, 380]]},
          {nom: 'L&aacute;mpara de estudio', sensor: 'la LDR',
           sube: 'sube cuando hay menos luz', acc: 'encender la l&aacute;mpara', u: 600,
           perfil: [[0, 300], [0.30, 290], [0.34, 660], [0.38, 680], [0.42, 300],
                    [0.55, 280], [0.62, 620], [0.70, 760], [0.86, 780], [0.93, 640], [1, 320]]}
        ];
        var REGLAS = ['el &uacute;ltimo valor', 'la media de N', 'la mediana de N', 'la tendencia'];

        var np = 0, regla = 0, tipo = 0;

        /* ---- Lehmer (MINSTD). Cabe exacto en un double: Python da lo mismo ---- */
        var sem = 1;
        function semilla(s){ sem = s % 2147483647; if(sem <= 0) sem += 2147483646; }
        function rnd(){ sem = (sem * 16807) % 2147483647; return (sem - 1) / 2147483646; }

        function U(){ return +cU.value; }
        function Nef(){
          var n = +cN.value;
          if(regla === 0) return 1;
          if(regla === 3) return Math.max(4, n);
          return n;
        }
        function bytesDato(){ return tipo === 1 ? 1 : 2; }
        function guarda(x){ return tipo === 1 ? Math.floor(x / 4) * 4 : x; }

        function perfil(P, f){
          var p = P.perfil;
          for(var k = 1; k < p.length; k++){
            if(f <= p[k][0]){
              var t = (f - p[k - 1][0]) / (p[k][0] - p[k - 1][0]);
              return p[k - 1][1] + t * (p[k][1] - p[k - 1][1]);
            }
          }
          return p[p.length - 1][1];
        }

        /* ---- el dia de medidas: la verdad y lo que ve el sensor ----
           Los picos se sortean APARTE del ruido y son siempre seis, ni uno mas:
           si se sortean uno por medida, a un proyecto le tocan tres y a otro
           catorce, y entonces la comparacion entre reglas mide la suerte. */
        function serie(){
          var P = PROY[np], v = [], m = [], i, k;
          var picos = cPic.checked, pic = {};
          semilla(10203040 + np);
          for(k = 0; k < PICOS; k++){
            var q = I0 + 10 + Math.floor(rnd() * (NM - I0 - 20));
            pic[q] = PICO0 + Math.floor(rnd() * PICOR);
          }
          semilla(70809000 + np);
          for(i = 0; i < NM; i++){
            var vi = perfil(P, i / (NM - 1));
            var x = vi + (rnd() * 2 - 1) * RUIDO + ((picos && pic[i]) ? pic[i] : 0);
            x = Math.round(x);
            if(x < 0) x = 0;
            if(x > 1023) x = 1023;
            v.push(vi); m.push(x);
          }
          return {v: v, m: m, pic: pic};
        }

        /* ---- el numero que la regla compara con el umbral ---- */
        function valorRegla(s, i){
          var n = Nef();
          if(regla === 0) return s[i];
          var w = s.slice(i - n + 1, i + 1), k, t = 0;
          if(regla === 1){
            for(k = 0; k < w.length; k++) t += w[k];
            return t / w.length;
          }
          if(regla === 2){
            var o = w.slice().sort(function(a, b){ return a - b; });
            return (o.length % 2) ? o[(o.length - 1) / 2]
                                  : (o[o.length / 2 - 1] + o[o.length / 2]) / 2;
          }
          var h = Math.floor(n / 2), a = 0, b = 0;
          for(k = 0; k < h; k++){ a += w[k]; b += w[w.length - 1 - k]; }
          a /= h; b /= h;
          return b + ((b - a) / h) * HOR;
        }

        /* ---- medir lo que cuesta la regla, sobre el dia entero ---- */
        function mide(S){
          var u = U(), s = [], i;
          for(i = 0; i < NM; i++) s.push(guarda(S.m[i]));
          var r = [], d = [], vr = [];
          for(i = 0; i < NM; i++){
            vr.push(S.v[i] > u);
            if(i >= I0){ var q = valorRegla(s, i); r.push(q); d.push(q > u); }
            else { r.push(null); d.push(false); }
          }
          var falsas = 0, pasa = 0, arr = 0, arrF = 0, prev = false;
          for(i = I0; i < NM; i++){
            if(d[i] && !vr[i]) falsas++;
            if(!d[i] && vr[i]) pasa++;
            if(d[i] && !prev){ arr++; if(!vr[i]) arrF++; }
            prev = d[i];
          }
          var eps = [], en = false, ini = 0;
          for(i = I0; i < NM; i++){
            if(vr[i] && !en){ en = true; ini = i; }
            else if(!vr[i] && en){ en = false; eps.push([ini, i - 1]); }
          }
          if(en) eps.push([ini, NM - 1]);
          var ret = [], perd = 0;
          eps.forEach(function(e){
            var f = -1, j;
            if(d[e[0]]){
              f = e[0];
              while(f - 1 >= I0 && d[f - 1] && e[0] - (f - 1) <= ATRAS) f--;
            } else {
              for(j = e[0]; j <= e[1]; j++) if(d[j]){ f = j; break; }
            }
            if(f < 0) perd++; else ret.push((f - e[0]) * DT);
          });
          var med = 0;
          ret.forEach(function(x){ med += x; });
          med = ret.length ? med / ret.length : 0;
          return {r: r, d: d, vr: vr, s: s, falsas: falsas, pasa: pasa, arr: arr, arrF: arrF,
                  eps: eps.length, perd: perd, ret: med, nret: ret.length,
                  bytes: Nef() * bytesDato()};
        }

        /* ---- dibujo ---- */
        var X0 = 46, Y0 = 14, AN = 640, AL = 168, VMIN = 200, VMAX = 1023;
        function px(i){ return X0 + i / (NM - 1) * AN; }
        function py(v){ return Y0 + AL - (Math.max(VMIN, Math.min(VMAX, v)) - VMIN) / (VMAX - VMIN) * AL; }

        function linea(a, desde){
          var p = [], i;
          for(i = desde; i < NM; i++){
            if(a[i] === null) continue;
            p.push(px(i).toFixed(1) + ' ' + py(a[i]).toFixed(1));
          }
          return p.join(' L');
        }

        function pinta(S, M){
          var u = U(), i;
          var m = '<style>.memt{font:10px var(--f-m);fill:var(--ink-soft)}'
                + '.meme{font:10.5px var(--f-m);fill:var(--ink)}</style>';
          m += '<rect x="' + X0 + '" y="' + Y0 + '" width="' + AN + '" height="' + AL
             + '" fill="var(--surface)" stroke="var(--line)" stroke-width="1.2"></rect>';
          /* El umbral. El rotulo va FUERA del cuadro, en el margen: dentro se comia
             la curva justo donde mas importa mirarla. */
          m += '<path d="M' + X0 + ' ' + py(u).toFixed(1) + ' H' + (X0 + AN)
             + '" stroke="var(--goo-amarillo)" stroke-width="1.6" stroke-dasharray="5 4"></path>'
             + '<text x="' + (X0 - 6) + '" y="' + (py(u) + 3.5).toFixed(1)
             + '" text-anchor="end" fill="var(--goo-amarillo)" class="memt">' + u + '</text>';
          /* lo medido */
          m += '<path d="M' + linea(S.m, 0) + '" fill="none" stroke="var(--ink-soft)" '
             + 'stroke-width="0.9" opacity=".55"></path>';
          /* La verdad, mas gruesa que la linea azul: la azul se dibuja encima y si
             fueran igual de anchas la verde no se veria en ningun sitio. */
          m += '<path d="M' + linea(S.v, 0) + '" fill="none" stroke="var(--goo-verde)" '
             + 'stroke-width="3"></path>';
          /* el numero que mira la regla */
          m += '<path d="M' + linea(M.r, I0) + '" fill="none" stroke="var(--goo-azul)" '
             + 'stroke-width="1.6"></path>';
          /* las dos franjas */
          var BY = Y0 + AL + 16, BH = 11;
          [[M.vr, BY, 'lo que pasaba', 'var(--goo-verde)'],
           [M.d, BY + BH + 5, 'lo que decidi&oacute;', 'var(--goo-rojo)']].forEach(function(F){
            m += '<rect x="' + X0 + '" y="' + F[1] + '" width="' + AN + '" height="' + BH
               + '" fill="var(--surface-2)" stroke="var(--line)" stroke-width="0.8"></rect>';
            var ini = -1;
            for(i = 0; i <= NM; i++){
              var on = (i < NM) && F[0][i];
              if(on && ini < 0) ini = i;
              if(!on && ini >= 0){
                m += '<rect x="' + px(ini).toFixed(1) + '" y="' + F[1] + '" width="'
                   + Math.max(0.8, px(i - 1) - px(ini)).toFixed(1) + '" height="' + BH
                   + '" fill="' + F[3] + '" opacity=".75"></rect>';
                ini = -1;
              }
            }
            m += '<text x="' + (X0 - 6) + '" y="' + (F[1] + 9) + '" text-anchor="end" class="memt">'
               + F[2] + '</text>';
          });
          /* ejes */
          m += '<text x="' + (X0 - 6) + '" y="' + (Y0 + 9) + '" text-anchor="end" class="memt">'
             + VMAX + '</text>'
             + '<text x="' + (X0 - 6) + '" y="' + (Y0 + AL) + '" text-anchor="end" class="memt">'
             + VMIN + '</text>';
          for(var h = 0; h <= 24; h += 6){
            var x = X0 + h / 24 * AN;
            m += '<text x="' + x.toFixed(1) + '" y="' + (BY + 2 * BH + 22)
               + '" text-anchor="middle" class="memt">' + h + ' h</text>';
          }
          /* el rotulo del eje, en su propia linea: al lado de las horas se pisaban */
          m += '<text x="' + X0 + '" y="' + (BY + 2 * BH + 40) + '" class="meme">lectura de '
             + PROY[np].sensor + ', que ' + PROY[np].sube + '</text>';
          svg.innerHTML = m;
        }

        function codigo(){
          var n = Nef(), t = (tipo === 1) ? 'byte' : 'int';
          var c = 'const byte N = ' + n + ';\\n'
                + t + ' hist[N];              // ' + (n * bytesDato()) + ' bytes de los 2048\\n'
                + 'byte pos = 0;\\n\\n'
                + 'void guarda(int x) {\\n'
                + (tipo === 1 ? '  hist[pos] = x / 4;      // cabe en un byte, pierdo 4 unidades\\n'
                              : '  hist[pos] = x;\\n')
                + '  pos = (pos + 1) % N;    // al llegar al final, vuelvo al principio\\n'
                + '}\\n\\n';
          if(regla === 0){
            c += 'bool hayQue() {\\n  return leer() > ' + U() + ';   // ni miro lo guardado\\n}';
          } else if(regla === 1){
            c += 'bool hayQue() {\\n  long suma = 0;\\n'
               + '  for (byte i = 0; i < N; i++) suma += hist[i];\\n'
               + '  return suma / N > ' + U() + ';\\n}';
          } else if(regla === 2){
            c += 'bool hayQue() {\\n  int c[N];\\n'
               + '  memcpy(c, hist, sizeof(hist));   // otros ' + (n * bytesDato()) + ' bytes\\n'
               + '  ordena(c, N);\\n'
               + '  return c[N / 2] > ' + U() + ';\\n}';
          } else {
            c += 'bool hayQue() {\\n  int h = N / 2;\\n'
               + '  long v = 0, n2 = 0;\\n'
               + '  for (byte i = 0; i < h; i++) { v += hist[i]; n2 += hist[N - 1 - i]; }\\n'
               + '  float pend = (float)(n2 - v) / h / h;\\n'
               + '  return n2 / h + pend * ' + HOR + ' > ' + U() + ';\\n}';
          }
          cod.textContent = (tipo === 1)
            ? c.replace(/hist\\[i\\]/g, 'hist[i] * 4').replace(/c\\[N \\/ 2\\]/g, 'c[N / 2] * 4')
            : c;
        }

        function refresca(){
          var S = serie(), M = mide(S), P = PROY[np], n = Nef();
          cN.disabled = (regla === 0);
          vn.textContent = (regla === 0) ? '1 (ninguna)' : (n + (n !== +cN.value ? ' (m\\u00ednimo)' : ''));
          vu.textContent = U();
          pinta(S, M);
          codigo();

          var fil = function(x, y, cl){
            return '<div class="f ' + (cl || '') + '"><span>' + x + '</span><b>' + y + '</b></div>';
          };
          tabla.innerHTML =
              fil('medidas del d&iacute;a', NM + ' (una cada ' + DT + ' min)')
            + fil('veces que ' + P.acc + ' de m&aacute;s', M.arrF + ' de ' + M.arr + ' arranques',
                  M.arrF > 0 ? 'mal' : 'bien')
            + fil('medidas decididas al rev&eacute;s', (M.falsas + M.pasa) + ' de ' + (NM - I0), 'top')
            + fil('&mdash; falsas alarmas', M.falsas)
            + fil('&mdash; se le pasan', M.pasa)
            + fil('episodios de verdad', M.eps, 'top')
            + fil('&mdash; que no vio ninguno', M.perd, M.perd > 0 ? 'mal' : '')
            + fil('&mdash; tarda de media',
                  (M.ret >= 0 ? '+' : '\\u2212') + Math.abs(Math.round(M.ret)) + ' min')
            + fil('memoria del hist&oacute;rico', M.bytes + ' B de ' + RAM, 'top')
            + fil('&mdash; eso es', (100 * M.bytes / RAM).toFixed(1).replace('.', ',') + ' % de la RAM');

          var h = '';
          if(regla === 0){
            h = 'Est&aacute;s decidiendo con <b>una sola medida</b>: la de este instante. La l&iacute;nea '
              + 'azul y la gris son la misma, porque no hay nada que calcular. Cada pico de un '
              + 'instante se convierte en una decisi&oacute;n: ' + M.arrF + ' de los ' + M.arr
              + ' arranques no ten&iacute;an detr&aacute;s ning&uacute;n problema de verdad.';
          } else if(regla === 1){
            h = 'La media reparte el pico entre ' + n + ' medidas, as&iacute; que lo <b>encoge</b>: '
              + 'uno de ' + PICO0 + ' unidades se queda en ' + Math.round(PICO0 / n) + '. Pero mira '
              + 'las falsas alarmas: no lo quita, lo <b>estira</b>, y ahora el pico contamina '
              + n + ' medidas en vez de una. Y adem&aacute;s la l&iacute;nea azul va <b>por '
              + 'detr&aacute;s</b> de la verde: ese retraso se paga siempre, haya pico o no.';
          } else if(regla === 2){
            h = 'La mediana ordena las ' + n + ' medidas y se queda con la de en medio. Un pico de un '
              + 'instante queda en un extremo de la lista, as&iacute; que <b>no entra en la cuenta</b>: '
              + 'no lo encoge, lo <b>tira</b>. A cambio hay que ordenar, y ordenar cuesta tiempo y '
              + 'otra copia del array.';
          } else {
            h = 'La tendencia no mira solo d&oacute;nde est&aacute;s: mira <b>hacia d&oacute;nde vas</b>. '
              + 'Compara la media de las ' + Math.floor(n / 2) + ' &uacute;ltimas con la de las '
              + Math.floor(n / 2) + ' anteriores y proyecta ' + (HOR * DT) + ' minutos por delante. '
              + 'Por eso la l&iacute;nea azul se <b>adelanta</b> a la verde... y por eso se equivoca '
              + 'cuando la se&ntilde;al sube un rato y luego se para.';
          }
          if(M.ret < 0){
            h += ' Ahora mismo se <b>adelanta</b> ' + Math.abs(Math.round(M.ret))
               + ' minutos de media a que el problema exista de verdad.';
          }
          lee.innerHTML = h;

          pie.innerHTML = '<b>' + P.nom + '.</b> El d&iacute;a tiene ' + NM + ' medidas, una cada '
            + DT + ' minutos. La l&iacute;nea <b style="color:var(--goo-verde)">verde</b> es lo que '
            + 'pasaba de verdad; la gris, lo que lee el sensor (ruido de &plusmn;' + RUIDO
            + ' unidades y picos de un instante); la <b style="color:var(--goo-azul)">azul</b>, el '
            + 'n&uacute;mero que <b>' + REGLAS[regla] + '</b> compara con el umbral. Las cuentas salen '
            + 'de recorrer las ' + (NM - I0) + ' medidas que caben con cualquier N, no de una tabla. '
            + 'El retardo negativo quiere decir que el aviso se adelanta. <b>El perfil del d&iacute;a '
            + 'es nuestro</b>, elegido para que se parezca a lo que hace ese sensor; lo que se '
            + 'sostiene es la comparaci&oacute;n entre las cuatro reglas, no la forma exacta de la curva.';
        }

        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-p]'); if(!b) return;
          seg.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          np = +b.dataset.p; cU.value = PROY[np].u; refresca();
        });
        segR.addEventListener('click', function(e){
          var b = e.target.closest('button[data-r]'); if(!b) return;
          segR.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          regla = +b.dataset.r; refresca();
        });
        segT.addEventListener('click', function(e){
          var b = e.target.closest('button[data-t]'); if(!b) return;
          segT.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          tipo = +b.dataset.t; refresca();
        });
        [cN, cU].forEach(function(x){ x.addEventListener('input', refresca); });
        cPic.addEventListener('change', refresca);

        refresca();
      })();
      </script>
'''


# ==========================================================================
# S6 - El aviso que alguien lee
# ==========================================================================
AVISO = u'''
      <div class="escena" id="esc-avi">
        <div class="escena-barra">
          <span class="escena-titulo">Dos semanas del aparato avisando &middot; y qu&eacute; se entera una persona</span>
          <div class="seg" id="seg-avi">
            <button type="button" data-p="0" aria-pressed="true">Riego</button>
            <button type="button" data-p="1">Ventilaci&oacute;n</button>
            <button type="button" data-p="2">L&aacute;mpara</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 700 208" id="svg-avi" role="img"
               aria-label="Catorce d&iacute;as con las incidencias de verdad, la ca&iacute;da de red, los mensajes que salen y los que llegan"></svg>
          <div class="avi">
            <div class="avi-der">
              <div class="avi-fila">
                <label>Aviso</label>
                <div class="seg" id="pol-avi">
                  <button type="button" data-o="0" aria-pressed="true">peri&oacute;dico</button>
                  <button type="button" data-o="1">por evento</button>
                  <button type="button" data-o="2">evento + latido</button>
                </div>
              </div>
              <div class="avi-fila">
                <label for="avi-p">Cada</label>
                <input type="range" id="avi-p" min="0" max="1000" step="1" value="500">
                <span class="val" id="vp-avi"></span>
              </div>
              <div class="avi-fila">
                <label for="avi-l">Latido cada</label>
                <input type="range" id="avi-l" min="0" max="1000" step="1" value="560">
                <span class="val" id="vl-avi"></span>
              </div>
              <div class="avi-fila">
                <label>La placa decide con</label>
                <div class="seg" id="reg-avi">
                  <button type="button" data-r="0" aria-pressed="true">el &uacute;ltimo valor</button>
                  <button type="button" data-r="1">la media de 10</button>
                </div>
              </div>
              <label class="avi-chk"><input type="checkbox" id="avi-red" checked>
                <span>se cae la red el <b>d&iacute;a 6</b>, nueve horas</span></label>
              <label class="avi-chk"><input type="checkbox" id="avi-buf">
                <span>guardar en memoria lo que no se pueda mandar (1.200 B, 50 mensajes)</span></label>
              <label class="avi-chk"><input type="checkbox" id="avi-mudo">
                <span>el aparato se queda <b>mudo</b> el d&iacute;a 9 y ya no vuelve</span></label>
            </div>
            <div class="avi-izq">
              <div class="avi-tabla" id="tabla-avi"></div>
            </div>
          </div>
          <p class="avi-lee" id="lee-avi"></p>
        </div>
        <div class="pie" id="pie-avi"></div>
      </div>

      <style>
      .avi{display:flex;gap:18px;flex-wrap:wrap;align-items:flex-start;margin-top:12px}
      .avi-der{flex:1 1 320px;min-width:290px}
      .avi-izq{flex:1 1 300px;min-width:275px}
      .avi-fila{display:flex;align-items:center;gap:9px;flex-wrap:wrap;margin:0 0 9px;
        font-family:var(--f-m);font-size:12.5px;color:var(--ink)}
      .avi-fila label{min-width:118px}
      .avi-fila input[type="range"]{flex:1 1 110px;min-width:95px;accent-color:var(--goo-azul)}
      .avi-fila input[type="range"][disabled]{opacity:.4}
      .avi-fila .val{font-weight:500;color:var(--goo-azul);min-width:74px;text-align:right}
      .avi-fila .seg button{padding:5px 9px;font-size:11.5px}
      .avi-chk{display:flex;align-items:flex-start;gap:7px;font-family:var(--f-m);font-size:12px;
        color:var(--ink-soft);margin:0 0 8px;cursor:pointer;line-height:1.5}
      .avi-chk input{accent-color:var(--goo-azul);margin-top:2px}
      .avi-chk b{color:var(--ink)}
      .avi-tabla{border:1.5px solid var(--line);border-radius:2px;background:var(--surface);
        padding:9px 11px;font-family:var(--f-m);font-size:12px;line-height:1.7}
      .avi-tabla .f{display:flex;justify-content:space-between;gap:10px;align-items:baseline}
      .avi-tabla .f span:first-child{color:var(--ink-soft)}
      .avi-tabla .f b{color:var(--ink);font-weight:500;text-align:right;white-space:nowrap}
      .avi-tabla .f.top{border-top:1px solid var(--line-soft);margin-top:5px;padding-top:5px}
      .avi-tabla .mal b{color:var(--goo-rojo)}
      .avi-tabla .bien b{color:var(--goo-verde)}
      .avi-lee{font-family:var(--f-m);font-size:12.5px;line-height:1.75;color:var(--ink-soft);margin:12px 0 0}
      .avi-lee b{color:var(--ink)}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-avi');
        if(!svg) return;
        var caja = document.getElementById('esc-avi');
        var seg = document.getElementById('seg-avi');
        var segP = document.getElementById('pol-avi');
        var segR = document.getElementById('reg-avi');
        var cP = document.getElementById('avi-p');
        var cL = document.getElementById('avi-l');
        var cRed = document.getElementById('avi-red');
        var cBuf = document.getElementById('avi-buf');
        var cMudo = document.getElementById('avi-mudo');
        var vp = document.getElementById('vp-avi');
        var vl = document.getElementById('vl-avi');
        var tabla = document.getElementById('tabla-avi');
        var lee = document.getElementById('lee-avi');
        var pie = document.getElementById('pie-avi');

        /* ---- constantes del modelo ---- */
        var DT = 5;              /* minutos por paso */
        var DIAS = 14;
        var NP = DIAS * 1440 / DT;         /* 4032 pasos */
        var MSG = 24;            /* bytes por mensaje, del tama&ntilde;o medido en la sesi&oacute;n 3 */
        var BUF = 1200;          /* bytes de memoria que se dejan para la cola */
        var RUIDO = 45;          /* +- unidades de lectura */
        var RAMPA = 45;          /* la se&ntilde;al cruza el umbral en +-45 min */
        var SALTO = 70;          /* lo que sube la se&ntilde;al por encima y por debajo del umbral */
        var UMB = 600;
        var RED0 = (6 * 1440 + 8 * 60) / DT, RED1 = RED0 + 9 * 60 / DT;
        var MUDO = (9 * 1440 + 12 * 60) / DT;

        var PROY = [
          {nom: 'Riego autom&aacute;tico', qui: 'la planta necesita agua',
           /* la tercera cae ENTERA dentro de la ca&iacute;da de red del d&iacute;a 6, a prop&oacute;sito */
           eps: [[38 * 60, 9 * 60], [105 * 60, 7 * 60], [154 * 60, 5 * 60], [260 * 60, 6 * 60]]},
          {nom: 'Aviso de aula mal ventilada', qui: 'el aula est&aacute; cargada', eps: null},
          {nom: 'L&aacute;mpara de estudio', qui: 'hace falta luz', eps: null}
        ];
        function episodios(k){
          if(PROY[k].eps) return PROY[k].eps;
          var out = [], d;
          if(k === 1){
            for(d = 0; d < DIAS; d++){
              if(d % 7 >= 5) continue;
              out.push([d * 1440 + 11 * 60, 90]);
              out.push([d * 1440 + 17 * 60, 75]);
            }
          } else {
            for(d = 0; d < DIAS; d++) out.push([d * 1440 + 19 * 60, 240]);
          }
          return out;
        }

        var np = 0, pol = 0, reg = 0;

        var sem = 1;
        function semilla(s){ sem = s % 2147483647; if(sem <= 0) sem += 2147483646; }
        function rnd(){ sem = (sem * 16807) % 2147483647; return (sem - 1) / 2147483646; }

        function logi(c, lo, hi){
          return Math.exp(Math.log(lo) + (+c.value / 1000) * (Math.log(hi) - Math.log(lo)));
        }
        function periodo(){ return Math.max(1, Math.round(logi(cP, 5, 720) / 5)) * 5; }   /* min */
        function latido(){ return Math.max(1, Math.round(logi(cL, 60, 1440) / 30)) * 30; } /* min */
        /* El que recibe solo puede dar la alarma si espera algo a un ritmo: el del
           periodico, o el del latido. Con "por evento" a secas no espera nada. */
        function ventana(){ return pol === 0 ? 2 * periodo() : (pol === 2 ? 2 * latido() : 0); }

        function rotula(min){
          if(min < 60) return min + ' min';
          if(min % 60 === 0 && min < 1440) return (min / 60) + ' h';
          if(min === 1440) return '1 d\\u00eda';
          return (min / 60).toFixed(1).replace('.', ',') + ' h';
        }

        /* ---- la simulacion entera: no hay ni un numero escrito a mano ---- */
        function simula(){
          var EPS = episodios(np), i, k;
          var enEp = new Array(NP), lect = new Array(NP);
          for(i = 0; i < NP; i++) enEp[i] = false;
          EPS.forEach(function(e){
            var a = Math.round(e[0] / DT), b = Math.round((e[0] + e[1]) / DT);
            for(k = Math.max(0, a); k < Math.min(NP, b); k++) enEp[k] = true;
          });
          /* la se&ntilde;al cruza el umbral justo en el borde de cada episodio */
          semilla(555000 + np);
          for(i = 0; i < NP; i++){
            var t = i * DT, base = -SALTO;
            EPS.forEach(function(e){
              var a = e[0], b = e[0] + e[1], v;
              if(t >= a - RAMPA && t <= b + RAMPA){
                if(t < a + RAMPA) v = ((t - a) / RAMPA) * SALTO;
                else if(t > b - RAMPA) v = ((b - t) / RAMPA) * SALTO;
                else v = SALTO;
                if(v > base) base = v;
              }
            });
            lect[i] = UMB + base + (rnd() * 2 - 1) * RUIDO;
          }
          /* lo que decide la placa */
          var est = new Array(NP), hist = [];
          for(i = 0; i < NP; i++){
            hist.push(lect[i]);
            if(hist.length > 10) hist.shift();
            if(reg === 0){ est[i] = lect[i] > UMB; }
            else {
              var s = 0;
              for(k = 0; k < hist.length; k++) s += hist[k];
              est[i] = (s / hist.length) > UMB;
            }
          }
          /* los mensajes que salen */
          var P = Math.round(periodo() / DT), L = Math.round(latido() / DT);
          var sale = [];          /* [paso, tipoEsProblema] */
          var prev = false, ultAviso = -1e9, ultSalida = -1e9;
          for(i = 0; i < NP; i++){
            if(cMudo.checked && i >= MUDO) break;
            var manda = false, esProb = est[i];
            if(pol === 0){
              if(i - ultSalida >= P){ manda = true; ultSalida = i; }
            } else {
              if(est[i] !== prev){ manda = true; ultAviso = i; }
              else if(est[i] && i - ultAviso >= P){ manda = true; ultAviso = i; }
              if(pol === 2 && !manda && i - ultSalida >= L){ manda = true; }
            }
            prev = est[i];
            if(manda){ sale.push([i, esProb]); ultSalida = i; }
          }
          /* El viaje. El aparato REINTENTA: en cuanto vuelve la red vacia la cola,
             sin esperar a tener algo nuevo que decir. Si se espera, el aviso que
             guardo el martes puede no salir hasta el jueves, y eso no es guardar:
             es perderlo despacio. */
          var cola = [], llega = [], perdidos = 0, cabe = Math.floor(BUF / MSG), idx = 0;
          for(i = 0; i < NP; i++){
            var caida = cRed.checked && i >= RED0 && i < RED1;
            if(!caida && cola.length){
              for(k = 0; k < cola.length; k++) llega.push([i, cola[k][1], cola[k][0]]);
              cola = [];
            }
            while(idx < sale.length && sale[idx][0] === i){
              var msj = sale[idx]; idx++;
              if(!caida) llega.push([i, msj[1], msj[0]]);
              else if(cBuf.checked && cola.length < cabe) cola.push(msj);
              else perdidos++;
            }
          }
          perdidos += cola.length;
          /* cuanto tarda una persona en enterarse de cada incidencia */
          var espera = [], nunca = 0;
          EPS.forEach(function(e){
            var a = Math.round(e[0] / DT), b = Math.round((e[0] + e[1]) / DT), t = -1;
            for(k = 0; k < llega.length; k++){
              if(llega[k][1] && llega[k][2] >= a && llega[k][2] < b){ t = llega[k][0]; break; }
            }
            if(t < 0) nunca++; else espera.push((t - a) * DT);
          });
          var med = 0;
          espera.forEach(function(x){ med += x; });
          med = espera.length ? med / espera.length : 0;
          /* el silencio: solo se descubre si hay un ritmo esperado */
          var V = Math.round(ventana() / DT), silencio = [], hayRitmo = (pol !== 1);
          if(hayRitmo && V > 0){
            var hubo = new Array(NP);
            for(i = 0; i < NP; i++) hubo[i] = false;
            for(k = 0; k < llega.length; k++) if(llega[k][0] < NP) hubo[llega[k][0]] = true;
            var ult = -1;
            for(i = 0; i < NP; i++){
              if(hubo[i]) ult = i;
              else if(ult >= 0 && i - ult === V) silencio.push(i);
            }
          }
          var primeraTrasMudo = -1, falsas = 0;
          silencio.forEach(function(s){
            if(cMudo.checked && s >= MUDO){ if(primeraTrasMudo < 0) primeraTrasMudo = s; }
            else falsas++;
          });
          return {eps: EPS.length, sale: sale, llega: llega, perdidos: perdidos, nunca: nunca,
                  espera: med, nEsp: espera.length, silencio: silencio, hayRitmo: hayRitmo,
                  mudo: primeraTrasMudo, falsasSil: falsas, enEp: enEp,
                  P: P, L: L, V: V, cabe: cabe};
        }

        /* ---- dibujo: catorce dias en una tira ----
           Los rotulos de cada fila van en un MARGEN a la izquierda: encima de su
           franja se com&iacute;an los numeros de dia. */
        var X0 = 128, AN = 552;
        function px(i){ return X0 + i / NP * AN; }

        function pinta(R){
          var m = '<style>.avit{font:10px var(--f-m);fill:var(--ink-soft)}'
                + '.avie{font:10.5px var(--f-m);fill:var(--ink)}</style>';
          var Y = 14, H = 13, PASO = 26, ABAJO = Y + 3 * PASO + H, i, k;
          /* separadores de dia */
          for(i = 0; i <= DIAS; i++){
            var x = X0 + i / DIAS * AN;
            m += '<path d="M' + x.toFixed(1) + ' ' + Y + ' V' + ABAJO
               + '" stroke="var(--line-soft)" stroke-width="1"></path>';
            if(i < DIAS && i % 2 === 0){
              m += '<text x="' + (x + 2).toFixed(1) + '" y="' + (ABAJO + 13)
                 + '" class="avit">d' + (i + 1) + '</text>';
            }
          }
          var filas = [
            [Y, 'lo que pasaba', 'var(--goo-verde)'],
            [Y + PASO, 'mensajes que salen', 'var(--goo-azul)'],
            [Y + 2 * PASO, 'le llegan a alguien', 'var(--goo-amarillo)'],
            [Y + 3 * PASO, 'alarma de silencio', 'var(--goo-rojo)']
          ];
          filas.forEach(function(F){
            m += '<rect x="' + X0 + '" y="' + F[0] + '" width="' + AN + '" height="' + H
               + '" fill="var(--surface-2)" stroke="var(--line)" stroke-width="0.8"></rect>'
               + '<text x="' + (X0 - 8) + '" y="' + (F[0] + 10) + '" text-anchor="end" class="avit">'
               + F[1] + '</text>';
          });
          /* incidencias */
          var ini = -1;
          for(i = 0; i <= NP; i++){
            var on = (i < NP) && R.enEp[i];
            if(on && ini < 0) ini = i;
            if(!on && ini >= 0){
              m += '<rect x="' + px(ini).toFixed(1) + '" y="' + Y + '" width="'
                 + Math.max(1, px(i) - px(ini)).toFixed(1) + '" height="' + H
                 + '" fill="var(--goo-verde)" opacity=".75"></rect>';
              ini = -1;
            }
          }
          /* la caida de red */
          if(cRed.checked){
            m += '<rect x="' + px(RED0).toFixed(1) + '" y="' + Y + '" width="'
               + Math.max(1.5, px(RED1) - px(RED0)).toFixed(1)
               + '" height="' + (ABAJO - Y) + '" fill="var(--goo-rojo)" opacity=".13"></rect>'
               + '<text x="' + px(RED0).toFixed(1) + '" y="' + (ABAJO + 26)
               + '" class="avit">&#8593; se cae la red</text>';
          }
          if(cMudo.checked){
            m += '<path d="M' + px(MUDO).toFixed(1) + ' ' + Y + ' V' + ABAJO
               + '" stroke="var(--goo-rojo)" stroke-width="1.8" stroke-dasharray="4 3"></path>'
               + '<text x="' + (px(MUDO) + 3).toFixed(1) + '" y="' + (ABAJO + 39)
               + '" class="avit">&#8593; se queda mudo</text>';
          }
          /* mensajes: una raya por mensaje (a partir de cierta densidad se ve como una banda) */
          /* una raya por mensaje, pero sin repetir columna de pixel: con el periodico
             mas rapido salen 4.032 mensajes y no caben 4.032 elementos en 650 px */
          var pinta1 = function(lista, y, col, idx){
            var vistos = {};
            for(var j = 0; j < lista.length; j++){
              var xx = Math.round(px(idx === null ? lista[j] : lista[j][idx]));
              if(vistos[xx]) continue;
              vistos[xx] = 1;
              m += '<path d="M' + xx + ' ' + y + ' v' + H + '" stroke="' + col
                 + '" stroke-width="1" opacity=".85"></path>';
            }
          };
          pinta1(R.sale, Y + PASO, 'var(--goo-azul)', 0);
          pinta1(R.llega, Y + 2 * PASO, 'var(--goo-amarillo)', 0);
          /* la alarma de silencio son uno o dos instantes en dos semanas: si se dibuja
             con el mismo grosor que los mensajes no se ve, asi que lleva su marca */
          R.silencio.forEach(function(s){
            m += '<path d="M' + px(s).toFixed(1) + ' ' + (Y + 3 * PASO - 5) + ' v' + (H + 10)
               + '" stroke="var(--goo-rojo)" stroke-width="2.4"></path>';
          });
          if(!R.hayRitmo){
            m += '<text x="' + (X0 + 6) + '" y="' + (Y + 3 * PASO + 10) + '" class="avit">'
               + 'no la hay: callarse es lo que hace este aparato cuando todo va bien</text>';
          }
          m += '<text x="' + X0 + '" y="' + (ABAJO + 56) + '" class="avie">' + DIAS
             + ' d&iacute;as &middot; ' + PROY[np].nom + ' &middot; una incidencia es que '
             + PROY[np].qui + '</text>';
          svg.innerHTML = m;
        }

        function refresca(){
          cL.disabled = (pol !== 2);
          vp.textContent = rotula(periodo());
          vl.textContent = (pol === 2) ? rotula(latido()) : '\\u2014';
          var R = simula();
          pinta(R);

          var alDia = R.llega.length / DIAS;
          var bytesMes = R.sale.length * MSG * 30 / DIAS;
          var fil = function(x, y, cl){
            return '<div class="f ' + (cl || '') + '"><span>' + x + '</span><b>' + y + '</b></div>';
          };
          tabla.innerHTML =
              fil('mensajes que salen', R.sale.length.toLocaleString('es-ES'))
            + fil('se pierden en la ca&iacute;da', R.perdidos, R.perdidos > 0 ? 'mal' : 'bien')
            + fil('le llegan a una persona', R.llega.length.toLocaleString('es-ES'))
            + fil('&mdash; al d&iacute;a', alDia.toFixed(1).replace('.', ','),
                  alDia > 30 ? 'mal' : '')
            + fil('datos al mes', (bytesMes / 1024).toFixed(1).replace('.', ',') + ' kB', 'top')
            + fil('incidencias', R.eps, 'top')
            + fil('&mdash; no se supieron nunca', R.nunca, R.nunca > 0 ? 'mal' : 'bien')
            + fil('&mdash; se tarda en saberlo', rotula(Math.round(R.espera)))
            + fil('el silencio del aparato',
                  !cMudo.checked ? 'no lo hay'
                  : (R.mudo >= 0 ? ('se descubre en ' + rotula(Math.round((R.mudo - MUDO) * DT)))
                                 : 'NO se descubre'),
                  'top' + (cMudo.checked && R.mudo < 0 ? ' mal' : (cMudo.checked ? ' bien' : '')))
            + fil('falsas alarmas de silencio', R.falsasSil, R.falsasSil > 0 ? 'mal' : '');

          var h = '';
          if(pol === 0){
            h = 'Mandas una medida cada ' + rotula(periodo()) + ' pase lo que pase: '
              + R.sale.length.toLocaleString('es-ES') + ' mensajes en dos semanas, '
              + alDia.toFixed(1).replace('.', ',') + ' al d&iacute;a que le llegan a alguien. '
              + '<b>Nadie lee eso.</b> A cambio, el ritmo es tan fijo que el silencio se nota.';
          } else if(pol === 1){
            h = 'Solo hablas cuando algo cambia: ' + R.sale.length.toLocaleString('es-ES')
              + ' mensajes en dos semanas. Eso s&iacute; se lee. Pero mira la &uacute;ltima fila: si el '
              + 'aparato se estropea y deja de medir, <b>no manda nada</b>... que es exactamente lo '
              + 'mismo que hace cuando todo va bien. El fallo m&aacute;s peligroso es el que no se '
              + 'distingue de la normalidad.';
          } else {
            h = 'Avisas cuando cambia algo <b>y</b> dices &laquo;sigo aqu&iacute;&raquo; cada '
              + rotula(latido()) + '. Con eso, el que recibe puede dar la alarma si no le llega nada '
              + 'en ' + rotula(ventana()) + '. Son ' + R.sale.length.toLocaleString('es-ES')
              + ' mensajes: ' + alDia.toFixed(1).replace('.', ',') + ' al d&iacute;a.';
          }
          if(reg === 0){
            h += ' Y f&iacute;jate en la fila azul: la placa decide con <b>el &uacute;ltimo valor</b>, '
               + 'as&iacute; que en cada borde de una incidencia el estado tiembla y salen mensajes a '
               + 'rachas. Poner la media de 10 &mdash;lo de la sesi&oacute;n anterior&mdash; no cambia '
               + 'el protocolo: cambia <b>cu&aacute;ntas veces se dispara</b>.';
          }
          if(R.perdidos > 0){
            h += ' Se han perdido <b>' + R.perdidos + '</b> mensajes mientras la red estaba ca&iacute;da: '
               + (cBuf.checked ? 'la cola de ' + R.cabe + ' mensajes se llen&oacute;.'
                               : 'sin cola en memoria, lo que no sale en ese momento no sale nunca.');
          }
          lee.innerHTML = h;

          pie.innerHTML = 'Catorce d&iacute;as simulados paso a paso, uno cada ' + DT
            + ' minutos (' + NP.toLocaleString('es-ES') + ' pasos). Cada mensaje se cuenta a <b>'
            + MSG + ' bytes</b>, que es lo que med&iacute;a el PUBLISH de MQTT en la escena de la '
            + 'sesi&oacute;n 3. La cola en memoria son <b>' + BUF + ' bytes</b>, o sea ' + R.cabe
            + ' mensajes. El que recibe da la alarma de silencio si no le llega <b>nada</b> en el '
            + 'doble del latido. <b>Las incidencias y la ca&iacute;da de red son un gui&oacute;n '
            + 'nuestro</b>: lo que se sostiene es la comparaci&oacute;n entre las tres pol&iacute;ticas, '
            + 'no las fechas.';
        }

        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-p]'); if(!b) return;
          seg.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          np = +b.dataset.p; refresca();
        });
        segP.addEventListener('click', function(e){
          var b = e.target.closest('button[data-o]'); if(!b) return;
          segP.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          pol = +b.dataset.o; refresca();
        });
        segR.addEventListener('click', function(e){
          var b = e.target.closest('button[data-r]'); if(!b) return;
          segR.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          reg = +b.dataset.r; refresca();
        });
        [cP, cL].forEach(function(x){ x.addEventListener('input', refresca); });
        [cRed, cBuf, cMudo].forEach(function(x){ x.addEventListener('change', refresca); });

        refresca();
      })();
      </script>
'''
