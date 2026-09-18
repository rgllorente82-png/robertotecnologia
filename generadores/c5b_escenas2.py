# -*- coding: utf-8 -*-
u"""Escenas de las sesiones 7 y 8 de la U5 de 4.o. SVG + JavaScript a mano.

  ESCENA_SECUENCIA  S7 - una prensa con dos cilindros haciendo A+ B+ A- B-.
                    La secuencia la lleva una maquina de estados que salta de
                    paso por TIEMPO o por FINAL DE CARRERA, y las posiciones se
                    integran con la velocidad que deja pasar la valvula. El
                    diagrama espacio-fase de abajo NO esta dibujado: se traza
                    con lo que acaba de pasar.

  ESCENA_CADENA     S8 - el automatismo entero de las tres variantes del
                    proyecto, con el numero de cada eslabon calculado y un
                    inyector de averias para ver por donde se rompe.

De donde salen los numeros:

  velocidad         v = Q / A. El caudal que deja pasar la valvula (NL/min) se
                    convierte en volumen por segundo a la presion de trabajo y
                    se reparte sobre el area del embolo. Con Q = 200 NL/min a
                    6 bar, un cilindro de 25 mm saca 100 mm de vastago en
                    0,10 s. Los tiempos son de ese orden en una prensa de
                    verdad; la animacion va a camara lenta y sale dicho.

  carga             se modela como una perdida de velocidad proporcional:
                    v = v_max (1 - F_carga / F_cilindro). Es una
                    SIMPLIFICACION nuestra, y sale dicha en la escena. Lo que
                    si es exacto es que por encima de F_cilindro no se mueve.

  fuga del ADC      la hoja del ATmega328P admite hasta 1 uA de fuga en una
                    entrada analogica y recomienda no pasar de 10 kohmios de
                    impedancia de fuente. 1 uA sobre 500 kohmios son 0,5 V, o
                    sea 100 cuentas de error: por eso una resistencia fija de
                    1 Mohmio estropea la medida aunque el divisor este bien.

  electrovalvula    3 W a 24 V -> 125 mA, que es lo que pone la chapa de la
                    foto de esta sesion. Presion minima de pilotaje 2 bar en
                    las servopilotadas, que es el dato que mas sorprende.
"""

# ---------------------------------------------------------------------------
# S7 - La secuencia
#
# Lienzo 640 x 440.
#   Cilindro A (mordaza):  camisa x 46..190, y  44..76 ; vastago hasta 250..
#   Cilindro B (punzon):   camisa x 46..190, y 100..132
#   Finales de carrera: a0 (46, 88) a1 (256, 88) ; b0 (46,144) b1 (256,144)
#   Pieza de trabajo: x 300..360, y 60..120
#   Panel de pasos: x 384..632, y 34..150
#   Valvulas 5/2: A en x 46..200 y 176..232 ; B en x 236..390, misma y
#   Panel de numeros: x 410..632, y 170..250
#   Diagrama espacio-fase: x 60..620, y 280..410 (dos bandas de 46)
# ---------------------------------------------------------------------------
ESCENA_SECUENCIA = u'''
      <div class="escena" id="esc-sec">
        <div class="escena-barra">
          <span class="escena-titulo">A+ B+ A&minus; B&minus; &middot; una mordaza y un punz&oacute;n</span>
          <div class="seg" id="seg-sec-modo">
            <button type="button" data-m="fdc" aria-pressed="true">Salta por final de carrera</button>
            <button type="button" data-m="tiempo">Salta por tiempo</button>
          </div>
        </div>
        <div class="escena-barra">
          <div class="seg" id="seg-sec-val">
            <button type="button" data-v="mono" aria-pressed="true">V&aacute;lvulas monoestables</button>
            <button type="button" data-v="bi">V&aacute;lvulas biestables</button>
          </div>
          <div class="seg" id="seg-sec-fallo">
            <button type="button" data-a="no" aria-pressed="true">Todo bien</button>
            <button type="button" data-a="b1">Final de carrera b1 aflojado</button>
          </div>
          <div class="seg" id="seg-sec-luz">
            <button type="button" data-l="on" aria-pressed="true">Con corriente</button>
            <button type="button" data-l="off">Corte de corriente</button>
          </div>
        </div>
        <div class="escena-barra">
          <label class="ctrl" style="flex:1 1 230px">
            <span>Lo que cuesta empujar la pieza</span>
            <input id="sec-carga" type="range" min="0" max="100" value="20" step="1">
            <b id="sec-carga-val">20 %</b>
          </label>
          <label class="ctrl" style="flex:1 1 230px">
            <span>Tiempo de cada paso (por tiempo)</span>
            <input id="sec-t" type="range" min="8" max="40" value="16" step="1">
            <b id="sec-t-val">0,16 s</b>
          </label>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 450" id="svg-sec" role="img"
               aria-label="Dos cilindros neum&aacute;ticos haciendo la secuencia A m&aacute;s, B m&aacute;s, A menos, B menos, con sus v&aacute;lvulas y el diagrama de espacio y fase"></svg>
        </div>
        <div class="pie" id="pie-sec"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-sec');
        if(!svg) return;
        var pie  = document.getElementById('pie-sec');
        var segM = document.getElementById('seg-sec-modo');
        var segV = document.getElementById('seg-sec-val');
        var segA = document.getElementById('seg-sec-fallo');
        var segL = document.getElementById('seg-sec-luz');
        var cIn = document.getElementById('sec-carga'), cTx = document.getElementById('sec-carga-val');
        var tIn = document.getElementById('sec-t'), tTx = document.getElementById('sec-t-val');

        var PRES = 6, CARRERA = 100, QVALV = 200;    /* bar, mm, NL/min */
        var LENTO = 5;                                /* camara lenta: 5 veces */
        var T_VIGILANTE = 1.0;   /* s: cinco veces el paso mas largo sin carga */
        var CIL = {A:{d:25, n:'A \\u00b7 empujador \\u00d8 25'},
                   B:{d:32, n:'B \\u00b7 punz\\u00f3n \\u00d8 32'}};

        var modo = 'fdc', tipoV = 'mono', fallo = 'no', corriente = true;
        var pos = {A:0, B:0}, paso = 1, tPaso = 0, tModelo = 0;
        var traza = [], choques = 0, ciclos = 0, tCicloIni = 0, tCiclo = null;
        var bloqueado = false, ultimo = null, raf = null, peligroAnt = false;

        function coma(n, d){ return n.toFixed(d).replace('.', ','); }

        /* ---------------------- las cuentas de siempre ---------------------- */
        function area(d){ return Math.PI * d * d / 4; }                 /* mm2 */
        function fuerza(d){ return PRES * 0.1 * area(d); }              /* N */
        /* Volumen que hay que meter para una carrera, en litros normales, y de
           ahi el tiempo que tarda con el caudal de la valvula. */
        function tCarrera(d){
          var vol = area(d) * CARRERA / 1e6 * (PRES + 1);               /* NL */
          return vol / QVALV * 60;                                       /* s */
        }
        /* La carga solo afecta al empujador cuando sale, que es el que arrastra
           la pieza. Modelo simple y declarado: la velocidad baja en proporcion
           a lo que se lleva la carga de la fuerza disponible. */
        function velocidad(cil, saliendo){
          var d = CIL[cil].d;
          var v = CARRERA / tCarrera(d);                                 /* mm/s */
          if(cil === 'A' && saliendo){
            var f = +cIn.value / 100;
            v = v * (1 - f);
          }
          return Math.max(0, v) / CARRERA;                               /* por unidad/s */
        }

        /* ------------------- la maquina de estados ------------------- */
        /* Cuatro pasos. En cada uno, que se manda y con que se sale de el. */
        var PASOS = [
          {n:1, txt:'A+', cil:'A', dir:1, fdc:'a1', nom:'coloca la pieza'},
          {n:2, txt:'B+', cil:'B', dir:1, fdc:'b1', nom:'marca la pieza'},
          {n:3, txt:'A\\u2212', cil:'A', dir:0, fdc:'a0', nom:'vuelve el empujador'},
          {n:4, txt:'B\\u2212', cil:'B', dir:0, fdc:'b0', nom:'sube el punz\\u00f3n'}
        ];
        function sensor(k){
          if(k === 'a0') return pos.A <= 0.001;
          if(k === 'a1') return pos.A >= 0.999;
          if(k === 'b0') return pos.B <= 0.001;
          if(k === 'b1') return (fallo === 'b1') ? false : (pos.B >= 0.999);
          return false;
        }
        /* Que quiere cada valvula AHORA. Sin corriente, una monoestable se va
           a su reposo (los dos cilindros dentro) y una biestable se queda. */
        function orden(){
          if(!corriente){
            if(tipoV === 'mono') return {A:0, B:0};
            return ultimo || {A:0, B:0};
          }
          var o = {A:ultimo ? ultimo.A : 0, B:ultimo ? ultimo.B : 0};
          var p = PASOS[paso - 1];
          o[p.cil] = p.dir;
          return o;
        }

        function avanza(dt){
          var o = orden();
          ultimo = o;
          var k, v, obj;
          for(k in pos){
            obj = o[k];
            v = velocidad(k, obj === 1);
            if(obj === 1 && pos[k] < 1) pos[k] = Math.min(1, pos[k] + v * dt);
            else if(obj === 0 && pos[k] > 0)
              pos[k] = Math.max(0, pos[k] - velocidad(k, false) * dt);
          }
          /* La regla de la maquina: el punzon no puede estar BAJANDO si la
             pieza no esta colocada del todo. Se cuenta el choque una vez por
             episodio, no una por fotograma. */
          var peligro = (o.B === 1 && pos.B < 0.999 && pos.A < 0.95);
          if(peligro && !peligroAnt) choques++;
          peligroAnt = peligro;

          if(corriente){
            tPaso += dt;
            var p = PASOS[paso - 1];
            var salta = (modo === 'tiempo') ? (tPaso >= +tIn.value / 100) : sensor(p.fdc);
            bloqueado = (modo === 'fdc') && (tPaso > T_VIGILANTE) && !salta;
            if(salta){
              tPaso = 0;
              paso = paso === 4 ? 1 : paso + 1;
              if(paso === 1){
                ciclos++;
                tCiclo = tModelo - tCicloIni;
                tCicloIni = tModelo;
              }
            }
          }
          tModelo += dt;
          traza.push({t:tModelo, a:pos.A, b:pos.B, p:paso, c:corriente});
          while(traza.length && traza[0].t < tModelo - 2.4) traza.shift();
        }

        /* ---------------------------- dibujo ---------------------------- */
        function caja(x, y, w, h, relleno, borde, grosor, rx){
          return '<rect x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" width="'
               + Math.max(0, w).toFixed(1) + '" height="' + h.toFixed(1) + '" rx="'
               + (rx === undefined ? 1.5 : rx) + '" fill="' + relleno + '" stroke="' + borde
               + '" stroke-width="' + grosor + '"></rect>';
        }
        function linea(d, color, grosor, guion){
          return '<path d="' + d + '" fill="none" stroke="' + color + '" stroke-width="'
               + grosor + '" stroke-linecap="round" stroke-linejoin="round"'
               + (guion ? ' stroke-dasharray="' + guion + '"' : '') + '></path>';
        }
        function rot(x, y, txt, est, anchor){
          return '<text x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" class="rotulo-svg"'
               + (anchor ? ' text-anchor="' + anchor + '"' : '')
               + (est ? ' style="' + est + '"' : '') + '>' + txt + '</text>';
        }
        function fdcSim(x, y, activo, etq){
          var col = activo ? 'var(--goo-verde)' : 'var(--ink-soft)';
          var s = caja(x - 8, y - 7, 16, 14, 'var(--surface)', col, 1.6);
          s += '<circle cx="' + x + '" cy="' + (y - 12) + '" r="3.5" fill="none" stroke="'
             + col + '" stroke-width="1.5"></circle>';
          s += linea('M' + x + ' ' + (y - 7) + ' V' + (y - 9), col, 1.5);
          s += rot(x, y + 18, etq, 'font-size:8.5px;fill:' + col, 'middle');
          return s;
        }
        /* Cilindro de doble efecto en corte, con el embolo donde toca. */
        function cilindro(x, y, w, h, p, nom, mandaFuera){
          var xe = x + 6 + p * (w - 22);
          var s = caja(x, y, w, h, 'var(--surface)', 'var(--ink-soft)', 1.8);
          s += caja(x, y, xe - x, h, mandaFuera ? 'var(--accent-soft)' : 'var(--surface)',
                    'none', 0);
          if(!mandaFuera)
            s += caja(xe + 10, y, (x + w) - (xe + 10), h, 'var(--accent-soft)', 'none', 0);
          s += caja(x, y, w, h, 'none', 'var(--ink-soft)', 1.8);
          s += caja(xe, y + 2, 10, h - 4, 'var(--ink-soft)', 'var(--ink)', 1.4);
          s += linea('M' + (xe + 10) + ' ' + (y + h / 2) + ' H' + (x + w + 52),
                     'var(--ink)', 4);
          s += caja(x + w + 52, y - 4, 12, h + 8, 'var(--surface-2)', 'var(--ink-soft)', 1.4);
          s += rot(x, y - 8, nom, 'font-size:9px');
          return s;
        }
        /* 5/2 compacta: dos cuadros, bobina a la izquierda, muelle o segunda
           bobina a la derecha. La caja en servicio se desplaza, como en la S4. */
        /* 5/2 en simbologia ISO 1219, con la convencion de la sesion 4: las
           TUBERIAS no se mueven -se dibujan sobre la ventana, que es la
           posicion de reposo- y lo que se desplaza es el cuerpo de la valvula,
           con sus accionamientos pegados. */
        function valvula(x, y, activa, nom, bi){
          var S = 40, s = '', i2;
          var vx = x + 20;                       /* donde esta la ventana */
          var bx = activa ? vx : vx - S;         /* donde empieza el cuerpo */
          s += rot(vx, y + S + 32, nom, 'font-size:9px');
          s += caja(vx, y, S, S, 'var(--surface-2)', 'var(--line)', 1, 1);
          s += caja(bx, y, S * 2, S, 'var(--surface)', 'var(--ink-soft)', 1.6, 1);
          s += linea('M' + (bx + S) + ' ' + y + ' V' + (y + S), 'var(--ink-soft)', 1.6);
          /* flechas cruzadas en un cuadro y rectas en el otro */
          s += linea('M' + (bx + 9) + ' ' + (y + S - 7) + ' L' + (bx + 31) + ' ' + (y + 7),
                     'var(--ink)', 1.5);
          s += linea('M' + (bx + 31) + ' ' + (y + S - 7) + ' L' + (bx + 9) + ' ' + (y + 7),
                     'var(--ink)', 1.5);
          s += linea('M' + (bx + S + 12) + ' ' + (y + S - 7) + ' V' + (y + 7),
                     'var(--ink)', 1.5);
          s += linea('M' + (bx + S + 28) + ' ' + (y + S - 7) + ' V' + (y + 7),
                     'var(--ink)', 1.5);
          /* la bobina, pegada al cuerpo por la izquierda */
          s += caja(bx - 20, y + S / 2 - 10, 20, 20,
                    activa && corriente ? 'var(--accent-soft)' : 'var(--surface)',
                    activa && corriente ? 'var(--goo-azul)' : 'var(--ink-soft)', 1.6);
          s += linea('M' + (bx - 16) + ' ' + (y + S / 2 - 6) + ' l12 12', 'var(--ink-soft)', 1.4);
          /* y por la derecha, la segunda bobina o el muelle */
          if(bi){
            s += caja(bx + S * 2, y + S / 2 - 10, 20, 20,
                      !activa && corriente ? 'var(--accent-soft)' : 'var(--surface)',
                      !activa && corriente ? 'var(--goo-azul)' : 'var(--ink-soft)', 1.6);
            s += linea('M' + (bx + S * 2 + 4) + ' ' + (y + S / 2 - 6) + ' l12 12',
                       'var(--ink-soft)', 1.4);
          } else {
            var mx = bx + S * 2 + 2, d = 'M' + mx + ' ' + (y + S / 2);
            for(i2 = 0; i2 < 3; i2++) d += ' l5 -6 l5 6';
            s += linea(d, 'var(--ink-soft)', 1.5);
          }
          /* Las cinco vias numeradas: presion y escapes abajo (1, 3, 5) y las
             dos salidas de trabajo arriba (4, 2). Van sobre la VENTANA. */
          var abajo = [[vx + 8, '5'], [vx + 20, '1'], [vx + 32, '3']];
          var arriba = [[vx + 14, '4'], [vx + 26, '2']];
          for(i2 = 0; i2 < abajo.length; i2++){
            s += linea('M' + abajo[i2][0] + ' ' + (y + S) + ' v10', 'var(--ink-soft)', 1.5);
            s += rot(abajo[i2][0], y + S + 20, abajo[i2][1], 'font-size:8px', 'middle');
          }
          for(i2 = 0; i2 < arriba.length; i2++){
            s += linea('M' + arriba[i2][0] + ' ' + y + ' v-10', 'var(--ink-soft)', 1.5);
            s += rot(arriba[i2][0], y - 14, arriba[i2][1], 'font-size:8px', 'middle');
          }
          /* el triangulo de la presion, en la via 1 */
          s += '<path d="M' + (vx + 15) + ' ' + (y + S + 10) + ' L' + (vx + 25) + ' '
             + (y + S + 10) + ' L' + (vx + 20) + ' ' + (y + S + 2)
             + ' Z" fill="none" stroke="var(--ink-soft)" stroke-width="1.4"></path>';
          return s;
        }

        function pinta(){
          var s = '', i;
          var o = ultimo || {A:0, B:0};

          /* ==================== los dos cilindros ==================== */
          s += rot(10, 24, 'LA PRENSA', 'font-size:10.5px');
          s += cilindro(56, 44, 134, 32, pos.A, CIL.A.n, o.A === 1);
          s += cilindro(56, 100, 134, 32, pos.B, CIL.B.n, o.B === 1);
          s += fdcSim(30, 88, sensor('a0'), 'a0');
          s += fdcSim(266, 88, sensor('a1'), 'a1');
          s += fdcSim(30, 152, sensor('b0'), 'b0');
          s += fdcSim(266, 152, sensor('b1'), 'b1');
          if(fallo === 'b1')
            s += rot(266, 184, 'aflojado', 'font-size:8.5px;fill:var(--goo-rojo)', 'middle');

          /* la pieza: colocada si el empujador ha llegado al final */
          var puesta = pos.A >= 0.95;
          s += caja(300, 60, 56, 40, puesta ? 'var(--accent-soft)' : 'var(--surface-2)',
                    puesta ? 'var(--goo-azul)' : 'var(--goo-rojo)', 1.8);
          s += rot(328, 84, 'pieza', 'font-size:9px', 'middle');
          s += rot(328, 112, puesta ? 'en su sitio' : 'sin colocar',
                   'font-size:9px;fill:' + (puesta ? 'var(--goo-verde)' : 'var(--goo-rojo)'),
                   'middle');
          if(peligroAnt)
            s += rot(328, 128, '\\u00a1y baja igual!',
                     'font-size:9px;fill:var(--goo-rojo)', 'middle');

          /* ==================== panel de pasos ==================== */
          var X = 384;
          s += rot(X, 24, 'LA SECUENCIA, PASO A PASO', 'font-size:10.5px');
          for(i = 0; i < PASOS.length; i++){
            var p = PASOS[i], act = (paso === p.n) && corriente;
            var yy = 34 + i * 29;
            s += caja(X, yy, 248, 25, act ? 'var(--accent-soft)' : 'var(--surface)',
                      act ? 'var(--goo-azul)' : 'var(--line)', act ? 2 : 1.2);
            s += rot(X + 10, yy + 17, p.n + '. ' + p.txt,
                     'font-size:11px;fill:var(--ink);font-weight:500');
            s += rot(X + 52, yy + 17, p.nom, 'font-size:9.5px');
            s += rot(X + 240, yy + 17,
                     modo === 'fdc' ? ('hasta ' + p.fdc) : ('hasta ' + coma(+tIn.value / 100, 2) + ' s'),
                     'font-size:9px;fill:' + (act ? 'var(--goo-azul)' : 'var(--ink-soft)'), 'end');
          }
          if(bloqueado)
            s += rot(X, 165, 'PARADA en el paso ' + paso + ': espera a '
                     + PASOS[paso - 1].fdc, 'font-size:10px;fill:var(--goo-rojo)');
          else if(!corriente)
            s += rot(X, 165, 'Sin corriente manda la v\\u00e1lvula',
                     'font-size:10px;fill:var(--goo-rojo)');

          /* ==================== las dos valvulas ==================== */
          s += rot(10, 190, 'LAS DOS 5/2 QUE LAS MANDAN', 'font-size:10.5px');
          s += valvula(50, 216, o.A === 1, 'v\\u00e1lvula de A', tipoV === 'bi');
          s += valvula(240, 216, o.B === 1, 'v\\u00e1lvula de B', tipoV === 'bi');

          /* ==================== numeros ==================== */
          var NX = 384;
          var NUM = [
            ['fuerza de A', Math.round(fuerza(CIL.A.d)) + ' N'],
            ['fuerza de B', Math.round(fuerza(CIL.B.d)) + ' N'],
            ['A sale en', coma(CARRERA / (velocidad('A', true) * CARRERA || 1e9), 3) + ' s'],
            ['B sale en', coma(tCarrera(CIL.B.d), 3) + ' s'],
            ['ciclo medido', tCiclo === null ? '\\u2014' : coma(tCiclo, 2) + ' s'],
            ['choques', '' + choques]
          ];
          for(i = 0; i < NUM.length; i++){
            var cx = NX + (i % 3) * 84, cy = 206 + Math.floor(i / 3) * 34;
            var mal = (NUM[i][0] === 'choques' && choques > 0);
            s += caja(cx, cy, 80, 30, 'var(--surface)',
                      mal ? 'var(--goo-rojo)' : 'var(--line)', 1.2);
            s += rot(cx + 6, cy + 12, NUM[i][0], 'font-size:8px');
            s += rot(cx + 6, cy + 25, NUM[i][1], 'font-size:11px;fill:'
                     + (mal ? 'var(--goo-rojo)' : 'var(--ink)') + ';font-weight:500');
          }

          /* ============ diagrama espacio-fase, trazado de lo que pasa ============ */
          var GX = 60, GR = 620, GY = 318, GH = 38;
          s += rot(10, 304, 'DIAGRAMA ESPACIO-FASE \\u00b7 lo que acaba de pasar',
                   'font-size:10.5px');
          var t1 = tModelo, t0 = t1 - 2.4;
          var gx = function(t){ return GX + (t - t0) / 2.4 * (GR - GX); };
          var bandas = [['A', 'a', GY, 'var(--goo-azul)'],
                        ['B', 'b', GY + GH + 20, 'var(--goo-verde)']];
          for(i = 0; i < bandas.length; i++){
            var bn = bandas[i], by = bn[2];
            s += caja(GX, by, GR - GX, GH, 'var(--surface-2)', 'var(--line)', 1);
            s += rot(GX - 8, by + 10, bn[0] + ' fuera', 'font-size:8.5px', 'end');
            s += rot(GX - 8, by + GH - 2, bn[0] + ' dentro', 'font-size:8.5px', 'end');
            var d = '';
            for(var j = 0; j < traza.length; j++){
              var m = traza[j];
              d += (j ? ' L' : 'M') + gx(m.t).toFixed(1) + ' '
                 + (by + GH - m[bn[1]] * GH).toFixed(1);
            }
            s += linea(d, bn[3], 2);
          }
          /* las rayas de cambio de paso, que es lo que hace util el diagrama */
          for(i = 1; i < traza.length; i++){
            if(traza[i].p !== traza[i - 1].p){
              var xx = gx(traza[i].t);
              s += linea('M' + xx.toFixed(1) + ' ' + GY + ' V' + (GY + GH * 2 + 20),
                         'var(--line)', 1, '3 3');
              s += rot(xx, GY - 5, PASOS[traza[i].p - 1].txt,
                       'font-size:8.5px;fill:var(--ink-soft)', 'middle');
            }
          }
          s += rot(GR, GY + GH * 2 + 34, 'los \\u00faltimos 2,4 segundos',
                   'font-size:8.5px', 'end');

          svg.innerHTML = s;

          /* ------------------------- el pie ------------------------- */
          var t = 'La v\\u00e1lvula deja pasar <b>' + QVALV + ' NL/min</b>. El cilindro A mueve '
                + coma(area(CIL.A.d) * CARRERA / 1e6 * (PRES + 1), 3) + ' litros normales por '
                + 'carrera, as\\u00ed que sin carga tarda <b>' + coma(tCarrera(CIL.A.d), 3)
                + ' s</b> en salir; el B, que es m\\u00e1s gordo, tarda <b>'
                + coma(tCarrera(CIL.B.d), 3) + ' s</b>. ';
          var f = +cIn.value;
          if(f > 0 && f < 100)
            t += 'Con la carga al ' + f + ' %, el empujador sale un ' + f
               + ' % m\\u00e1s despacio: <b>' + coma(tCarrera(CIL.A.d) / (1 - f / 100), 3)
               + ' s</b>. ';
          else if(f >= 100)
            t += 'Con la carga al 100 % <b>el empujador no se mueve</b>: la pieza le opone '
               + 'toda la fuerza que el cilindro puede dar. ';

          if(!corriente)
            t += '<b>Corte de corriente.</b> '
               + (tipoV === 'mono'
                  ? 'Las dos v\\u00e1lvulas son monoestables: el muelle las devuelve al reposo y '
                    + 'los dos cilindros <b>se meten</b>. Sabes d\\u00f3nde va a quedarse la '
                    + 'm\\u00e1quina, y eso es lo que se llama <b>estado seguro</b>\\u2026 si '
                    + 'meterse es lo seguro. Aqu\\u00ed la mordaza suelta la pieza.'
                  : 'Las dos v\\u00e1lvulas son biestables: <b>se quedan como estaban</b>. La '
                    + 'm\\u00e1quina se para donde iba, y al volver la corriente <b>nadie sabe '
                    + 'd\\u00f3nde est\\u00e1</b>. Por eso un automatismo con biestables tiene '
                    + 'que empezar leyendo sus finales de carrera antes de mover nada.');
          else if(bloqueado)
            t += '<b>La secuencia se ha parado en el paso ' + paso + '.</b> Est\\u00e1 esperando '
               + 'a <b>' + PASOS[paso - 1].fdc + '</b>, y ese final de carrera no llega a '
               + 'cerrar nunca. Parada: mal. Pero mira lo que pasa con &laquo;salta por '
               + 'tiempo&raquo;: sigue, y eso es peor.';
          else if(choques > 0)
            t += '<b>' + choques + (choques === 1 ? ' vez</b> ha' : ' veces</b> ha')
               + ' empezado a bajar el punz\\u00f3n con la pieza '
               + 'todav\\u00eda sin colocar. Saltar por tiempo quiere decir <b>dar por hecho</b> '
               + 'que el cilindro ha llegado. Cuando la carga cambia, deja de ser verdad, y la '
               + 'm\\u00e1quina no se entera: sigue contando.';
          else if(modo === 'fdc')
            t += 'Saltando por final de carrera, la secuencia <b>se adapta sola</b>: si el '
               + 'empujador va m\\u00e1s lento, el ciclo se alarga '
               + (tCiclo === null ? '' : '(ahora <b>' + coma(tCiclo, 2) + ' s</b>) ')
               + 'y el orden <b>no se rompe</b>. La m\\u00e1quina no adivina: pregunta.';
          else
            t += 'Por tiempo funciona mientras todo se porte. Sube la carga del empujador y '
               + 'mira el contador de choques.';

          pie.innerHTML = t
            + '<br><span style="font-size:12.5px">La animaci&oacute;n va a <b>c&aacute;mara lenta, '
            + 'cinco veces m&aacute;s despacio</b> que lo que dicen los n&uacute;meros, que si no '
            + 'no se ve nada. La velocidad sale de <b>v = Q / A</b>: el caudal que deja pasar la '
            + 'v&aacute;lvula repartido sobre el &aacute;rea del &eacute;mbolo. Que la carga baje '
            + 'la velocidad <b>en proporci&oacute;n</b> es una simplificaci&oacute;n nuestra, y '
            + 'el retroceso se calcula a la misma velocidad que el avance (en un cilindro de '
            + 'verdad es algo m&aacute;s r&aacute;pido, porque la c&aacute;mara del v&aacute;stago '
            + 'tiene menos volumen). Lo que s&iacute; es exacto es que por encima de la fuerza '
            + 'del cilindro no se mueve. '
            + 'El diagrama de abajo <b>no est&aacute; dibujado</b>: se traza con las posiciones '
            + 'de los &uacute;ltimos 2,4 segundos.</span>';
        }

        /* --------------------------- el reloj --------------------------- */
        var tAnt = null;
        function late(ts){
          if(tAnt === null) tAnt = ts;
          var dt = Math.min(0.05, (ts - tAnt) / 1000) / LENTO;
          tAnt = ts;
          avanza(dt);
          pinta();
          raf = requestAnimationFrame(late);
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
        pulsa(segM, 'data-m', function(v){ modo = v; choques = 0; tCiclo = null; });
        pulsa(segV, 'data-v', function(v){ tipoV = v; });
        pulsa(segA, 'data-a', function(v){ fallo = v; choques = 0; });
        pulsa(segL, 'data-l', function(v){
          corriente = (v === 'on');
          if(corriente){ paso = 1; tPaso = 0; }
        });
        cIn.addEventListener('input', function(){
          cTx.textContent = cIn.value + ' %'; choques = 0;
        });
        tIn.addEventListener('input', function(){
          tTx.textContent = coma(+tIn.value / 100, 2) + ' s'; choques = 0;
        });

        raf = requestAnimationFrame(late);
      })();
      </script>
'''


# ---------------------------------------------------------------------------
# S8 - La cadena entera
#
# Lienzo 640 x 430.
#   Fila 1 (y  66..122): magnitud, sensor+divisor, conversor, programa
#   Fila 2 (y 176..232): pin y Rb, transistor, actuador
#   Cada caja 140 x 56, separadas 16. Flechas entre ellas con el numero.
#   Cuadro de veredicto: y 256..306
#   Cuadro de consumo:   y 322..414
# ---------------------------------------------------------------------------
ESCENA_CADENA = u'''
      <div class="escena" id="esc-cad">
        <div class="escena-barra">
          <span class="escena-titulo">El automatismo entero, eslab&oacute;n por eslab&oacute;n</span>
          <div class="seg" id="seg-cad-var">
            <button type="button" data-v="A" aria-pressed="true">A &middot; Riego</button>
            <button type="button" data-v="B">B &middot; Ventilaci&oacute;n</button>
            <button type="button" data-v="C">C &middot; L&aacute;mpara</button>
          </div>
        </div>
        <div class="escena-barra">
          <span class="escena-titulo">Aver&iacute;a</span>
          <div class="seg" id="seg-cad-f">
            <button type="button" data-a="no" aria-pressed="true">Ninguna</button>
            <button type="button" data-a="rf">R fija de 1 M&#8486;</button>
            <button type="button" data-a="rb">Rb de 47 k&#8486;</button>
            <button type="button" data-a="masa">Sin masa com&uacute;n</button>
            <button type="button" data-a="dio">Sin diodo</button>
            <button type="button" data-a="pila">Pila gastada</button>
          </div>
        </div>
        <div class="escena-barra">
          <label class="ctrl" style="flex:1">
            <span id="cad-etq">Humedad de la tierra</span>
            <input id="cad-m" type="range" min="0" max="100" value="18" step="1">
            <b id="cad-m-val">18 %</b>
          </label>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 430" id="svg-cad" role="img"
               aria-label="La cadena completa del automatismo: magnitud, sensor, divisor, conversor, programa, transistor y actuador, con el n&uacute;mero de cada paso"></svg>
        </div>
        <div class="pie" id="pie-cad"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-cad');
        if(!svg) return;
        var pie  = document.getElementById('pie-cad');
        var segV = document.getElementById('seg-cad-var');
        var segF = document.getElementById('seg-cad-f');
        var mIn = document.getElementById('cad-m');
        var mTx = document.getElementById('cad-m-val');
        var mEt = document.getElementById('cad-etq');

        var BITS = 1024, IFUGA = 1e-6, TCORTE = 1e-6;
        var VARIANTES = {
          A: {n:'Riego', etq:'Humedad de la tierra', u:' %',
              mag:function(x){ return x; },
              rs:function(x){ var k = 1 - x / 100; return 5000 + 55000 * k * k; },
              rf:10000, umbral:700, mayor:true,
              act:'Bomba 6 V', i:0.250, v:6, L:0.005, vbat:6,
              efecto:'la bomba echa agua a la maceta'},
          B: {n:'Ventilaci\\u00f3n', etq:'Temperatura del aula', u:' \\u00b0C',
              mag:function(x){ return 10 + x * 0.25; },
              rs:function(x){ var T = 10 + x * 0.25 + 273.15;
                              return 10000 * Math.exp(3950 * (1 / T - 1 / 298.15)); },
              rf:10000, umbral:500, mayor:false,
              act:'Ventilador 12 V', i:0.300, v:12, L:0.008, vbat:12,
              efecto:'el ventilador renueva el aire'},
          C: {n:'L\\u00e1mpara', etq:'Luz que hay en la mesa', u:' lux',
              mag:function(x){ return Math.pow(10, -1 + 0.05 * x); },
              rs:function(x){ var E = Math.pow(10, -1 + 0.05 * x);
                              return Math.min(3e6, Math.max(60,
                                     10000 * Math.pow(Math.max(E, 1e-3) / 10, -0.7))); },
              rf:10000, umbral:120, mayor:true,
              act:'Tira LED 12 V', i:0.800, v:12, L:0, vbat:12,
              efecto:'la tira ilumina la mesa'}
        };
        var TIP120 = {beta:1000, vbe:1.6, vces:1.0, imax:5, vceo:60};

        var vr = 'A', fallo = 'no';

        function coma(n, d){ return n.toFixed(d).replace('.', ','); }
        function ohm(r){
          if(r >= 1e6) return coma(r / 1e6, 2) + ' M\\u03a9';
          if(r >= 1000) return coma(r / 1000, 1) + ' k\\u03a9';
          return Math.round(r) + ' \\u03a9';
        }
        function mA(a){
          if(a >= 1) return coma(a, 2) + ' A';
          return coma(a * 1000, a < 0.01 ? 2 : (a < 0.1 ? 1 : 0)) + ' mA';
        }
        function volt(v){
          if(v >= 1000) return coma(v / 1000, 1) + ' kV';
          return coma(v, v < 10 ? 2 : 0) + ' V';
        }
        /* la LDR trabaja en seis decadas: redondear a entero convertiria
           media decada en un cero, que no es lo mismo que "muy poca luz" */
        function lux(e){
          if(e >= 1000) return coma(e / 1000, 1) + 'k lux';
          if(e >= 10) return Math.round(e) + ' lux';
          if(e >= 1) return coma(e, 1) + ' lux';
          return coma(e, 2) + ' lux';
        }

        /* --------------- toda la cadena, en un sitio --------------- */
        function calcula(){
          var V = VARIANTES[vr], x = +mIn.value;
          var VCC = (fallo === 'pila') ? 3.9 : 5.0;
          var RF = (fallo === 'rf') ? 1e6 : V.rf;
          var RB = (fallo === 'rb') ? 47000 : 1500;
          var masa = (fallo !== 'masa');
          var diodo = (fallo !== 'dio');
          var vbat = (fallo === 'pila') ? V.vbat * 0.78 : V.vbat;

          var Rs = V.rs(x);
          var Vnodo = VCC * Rs / (RF + Rs);
          /* impedancia que ve el pin, y el error que mete su corriente de fuga */
          var Rsrc = RF * Rs / (RF + Rs);
          var err = IFUGA * Rsrc;
          var Vmed = Math.max(0, Math.min(VCC, Vnodo + err));
          var cuenta = Math.max(0, Math.min(BITS - 1, Math.round(Vmed / VCC * (BITS - 1))));
          var cuentaIdeal = Math.max(0, Math.min(BITS - 1,
                            Math.round(Vnodo / VCC * (BITS - 1))));
          var quiere = V.mayor ? (cuenta > V.umbral) : (cuenta < V.umbral);
          var quiereIdeal = V.mayor ? (cuentaIdeal > V.umbral) : (cuentaIdeal < V.umbral);

          /* Puede esta R fija llegar al umbral, con el sensor donde sea? Se
             barre el rango entero del sensor y se mira hasta donde llega la
             cuenta. Si el umbral queda fuera, el divisor esta ciego y no hay
             programa que lo arregle. */
          var cMin = 1e9, cMax = -1, xx, Rx, Vx, cx;
          for(xx = 0; xx <= 100; xx += 2){
            Rx = V.rs(xx);
            Vx = VCC * Rx / (RF + Rx);
            cx = Math.max(0, Math.min(BITS - 1, Math.round(Vx / VCC * (BITS - 1))));
            if(cx < cMin) cMin = cx;
            if(cx > cMax) cMax = cx;
          }
          var alcanza = V.mayor ? (cMax > V.umbral) : (cMin < V.umbral);

          var Ib = quiere ? Math.max(0, (VCC - TIP120.vbe) / RB) : 0;
          var icpos = TIP120.beta * Ib;
          var saturado = icpos >= V.i;
          var Ic = masa ? (saturado ? V.i : icpos) : 0;
          var Vce = saturado ? TIP120.vces : vbat * (1 - (V.i ? Ic / V.i : 0));
          var Pot = Vce * Ic;
          /* lo que le llega de verdad al actuador */
          var Vact = masa ? Math.max(0, vbat - Vce) : 0;
          /* Lo que se compara NO es la tension nominal del actuador: un TIP120
             saturado se queda con 1 V siempre, y eso es lo normal. Se compara
             con lo que le llegaria con la fuente sana. */
          var VactSano = V.vbat - TIP120.vces;
          var frac = VactSano > 0 ? Vact / VactSano : 0;
          var pico = (V.L > 0 && !diodo) ? V.L * Ic / TCORTE : (V.L > 0 ? vbat + 0.7 : 0);

          var funciona = masa && quiere && Ic > 0.8 * V.i && frac > 0.9
                      && (quiere === quiereIdeal);
          return {V:V, x:x, VCC:VCC, RF:RF, RB:RB, masa:masa, diodo:diodo, vbat:vbat,
                  Rs:Rs, Vnodo:Vnodo, Rsrc:Rsrc, err:err, Vmed:Vmed, cuenta:cuenta,
                  cuentaIdeal:cuentaIdeal, quiere:quiere, quiereIdeal:quiereIdeal,
                  cMin:cMin, cMax:cMax, alcanza:alcanza,
                  Ib:Ib, icpos:icpos, saturado:saturado, Ic:Ic, Vce:Vce, Pot:Pot,
                  Vact:Vact, frac:frac, pico:pico, funciona:funciona,
                  mag:V.mag(x)};
        }

        /* ---------------------------- dibujo ---------------------------- */
        function caja(x, y, w, h, relleno, borde, grosor){
          return '<rect x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" width="'
               + w.toFixed(1) + '" height="' + h.toFixed(1) + '" rx="2" fill="' + relleno
               + '" stroke="' + borde + '" stroke-width="' + grosor + '"></rect>';
        }
        function linea(d, color, grosor, guion){
          return '<path d="' + d + '" fill="none" stroke="' + color + '" stroke-width="'
               + grosor + '" stroke-linecap="round" stroke-linejoin="round"'
               + (guion ? ' stroke-dasharray="' + guion + '"' : '') + '></path>';
        }
        function rot(x, y, txt, est, anchor){
          return '<text x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" class="rotulo-svg"'
               + (anchor ? ' text-anchor="' + anchor + '"' : '')
               + (est ? ' style="' + est + '"' : '') + '>' + txt + '</text>';
        }
        function flecha(x1, y1, x2, y2, etq, bien){
          var col = bien ? 'var(--goo-verde)' : 'var(--goo-rojo)';
          var s = linea('M' + x1 + ' ' + y1 + ' L' + x2 + ' ' + y2, col, 2);
          s += '<path d="M' + x2 + ' ' + y2 + ' l-7 -4 v8 Z" fill="' + col + '"></path>';
          s += rot((x1 + x2) / 2, y1 - 8, etq, 'font-size:9.5px;fill:' + col, 'middle');
          return s;
        }
        function eslabon(x, y, tit, val, sub, bien){
          var col = bien ? 'var(--line)' : 'var(--goo-rojo)';
          var s = caja(x, y, 128, 56, 'var(--surface)', col, bien ? 1.5 : 2.2);
          s += rot(x + 9, y + 15, tit, 'font-size:8.5px');
          s += rot(x + 9, y + 34, val, 'font-size:14px;fill:'
                   + (bien ? 'var(--ink)' : 'var(--goo-rojo)') + ';font-weight:500');
          s += rot(x + 9, y + 49, sub, 'font-size:8.5px');
          return s;
        }

        function pinta(){
          var r = calcula(), s = '';
          var V = r.V;

          s += rot(10, 24, 'LA CADENA DEL PROYECTO ' + vr + ' \\u00b7 ' + V.n.toUpperCase(),
                   'font-size:10.5px');

          var medidaOK = (r.quiere === r.quiereIdeal) && r.alcanza;
          var f1 = [
            ['lo que pasa fuera',
             vr === 'C' ? lux(r.mag) : coma(r.mag, vr === 'B' ? 1 : 0) + V.u,
             V.etq.toLowerCase(), true],
            ['el sensor', ohm(r.Rs), 'lo que mide ahora', true],
            ['el divisor', coma(r.Vnodo, 2) + ' V', 'con R fija de ' + ohm(r.RF), medidaOK],
            ['analogRead(A0)', '' + r.cuenta,
             r.alcanza ? 'umbral ' + V.umbral
                       : 'no pasa de ' + r.cMax + ' en todo el rango', medidaOK]
          ];
          var i, x = 14;
          for(i = 0; i < f1.length; i++){
            s += eslabon(x, 66, f1[i][0], f1[i][1], f1[i][2], f1[i][3]);
            if(i < f1.length - 1)
              s += flecha(x + 128, 94, x + 148, 94, '', f1[i][3] && f1[i + 1][3]);
            x += 148;
          }

          /* el programa decide: caja aparte, a la derecha de la primera fila */
          s += caja(14, 138, 276, 26, r.quiere ? 'var(--accent-soft)' : 'var(--surface)',
                    r.quiere ? 'var(--goo-azul)' : 'var(--line)', 1.5);
          s += rot(24, 156, 'el programa: ' + (r.quiere ? 'HAY QUE ACTUAR \\u2192 D9 a 5 V'
                                                        : 'no hace falta \\u2192 D9 a 0 V'),
                   'font-size:10.5px;fill:var(--ink)');
          s += linea('M582 122 V150 H290', 'var(--ink-soft)', 1.6);
          s += '<path d="M290 150 l7 -4 v8 Z" fill="var(--ink-soft)"></path>';
          s += linea('M152 164 V176', 'var(--ink-soft)', 1.6);
          s += '<path d="M152 176 l-4 -7 h8 Z" fill="var(--ink-soft)"></path>';

          var baseOK = !r.quiere || r.saturado;
          var salidaOK = !r.quiere || (r.masa && r.Ic > 0);
          var actOK = !r.quiere || (r.masa && r.frac > 0.9);
          var f2 = [
            ['el pin y la Rb', mA(r.Ib), 'Rb de ' + ohm(r.RB), true],
            ['el transistor',
             r.quiere ? (r.saturado ? 'saturado' : 'a medio abrir') : 'cortado',
             r.quiere ? ('Vce ' + coma(r.Vce, 2) + ' V \\u00b7 ' + Math.round(r.Pot * 1000)
                         + ' mW') : 'no conduce', baseOK],
            ['el actuador', mA(r.Ic), V.act + ' \\u00b7 ' + coma(r.Vact, 1) + ' V', actOK]
          ];
          x = 14;
          for(i = 0; i < f2.length; i++){
            s += eslabon(x, 176, f2[i][0], f2[i][1], f2[i][2], f2[i][3]);
            if(i < f2.length - 1)
              s += flecha(x + 128, 204, x + 148, 204, '', f2[i][3] && f2[i + 1][3]);
            x += 148;
          }
          /* el efecto */
          s += caja(458, 176, 168, 56, actOK && r.quiere ? 'var(--accent-soft)' : 'var(--surface)',
                    actOK ? 'var(--line)' : 'var(--goo-rojo)', 1.5);
          /* con la pila gastada el actuador SI se mueve, solo que peor: decir
             que no funciona seria mentir, y ademas es justo lo que hace que
             esa averia sea dificil de encontrar */
          var efecto = !r.quiere ? 'en reposo'
                     : (actOK ? 'S\\u00cd' : (r.Ic > 0.01 ? 'A MEDIAS' : 'NO'));
          s += rot(467, 191, 'el efecto', 'font-size:8.5px');
          s += rot(467, 210, efecto,
                   'font-size:14px;fill:' + (actOK ? 'var(--ink)'
                                             : (r.Ic > 0.01 ? 'var(--goo-amarillo)'
                                                            : 'var(--goo-rojo)'))
                   + ';font-weight:500');
          s += rot(467, 225, V.efecto, 'font-size:8px');
          s += flecha(446, 204, 456, 204, '', actOK);

          /* ---------------- el veredicto ---------------- */
          var tit, col, det;
          if(!r.alcanza){
            tit = 'EL DIVISOR EST\\u00c1 CIEGO'; col = 'var(--goo-rojo)';
            det = 'con la R fija de ' + ohm(r.RF) + ' la cuenta va de ' + r.cMin + ' a '
                + r.cMax + ', y el umbral est\\u00e1 en ' + V.umbral;
          } else if(!r.masa){
            tit = 'SIN MASA COM\\u00daN'; col = 'var(--goo-rojo)';
            det = 'la corriente del actuador no tiene por d\\u00f3nde volver a su fuente';
          } else if(r.quiere && !r.saturado){
            tit = 'EL TRANSISTOR SE QUEDA A MEDIO ABRIR'; col = 'var(--goo-rojo)';
            det = 'con Rb de ' + ohm(r.RB) + ' la base solo da ' + mA(r.Ib) + ': pasan '
                + mA(r.Ic) + ' y ' + Math.round(r.Pot * 1000) + ' mW se van en calor';
          } else if(!medidaOK){
            tit = 'LA MEDIDA MIENTE'; col = 'var(--goo-rojo)';
            det = 'con ' + ohm(r.Rsrc) + ' de impedancia, 1 \\u00b5A de fuga son '
                + coma(r.err, 2) + ' V de error: ' + r.cuenta + ' en vez de ' + r.cuentaIdeal;
          } else if(!r.diodo && V.L > 0){
            tit = 'FUNCIONA HOY'; col = 'var(--goo-amarillo)';
            det = 'pero al cortar aparecen ' + volt(r.pico) + ' y el TIP120 aguanta '
                + TIP120.vceo + ' V';
          } else if(r.frac < 0.9 && r.quiere){
            tit = 'AL ACTUADOR LE FALTA TENSI\\u00d3N'; col = 'var(--goo-amarillo)';
            det = 'recibe ' + coma(r.Vact, 1) + ' V en vez de los ' + coma(V.vbat - 1, 1)
                + ' V de siempre';
          } else if(r.quiere){
            tit = 'LA CADENA ENTERA FUNCIONA'; col = 'var(--goo-verde)';
            det = 'de la magnitud al efecto sin un eslab\\u00f3n roto';
          } else {
            tit = 'EN REPOSO'; col = 'var(--ink-soft)';
            det = 'el programa no pide actuar; mueve el deslizador';
          }
          s += caja(14, 256, 612, 46, 'var(--surface)', col, 2);
          s += rot(26, 277, tit, 'font-size:12.5px;fill:' + col + ';font-weight:500');
          s += rot(26, 294, det, 'font-size:10px');

          /* ---------------- el consumo, que es el numero de la defensa --------- */
          s += rot(14, 322, 'LO QUE GASTA EL AUTOMATISMO, AUNQUE NO ACT\\u00daE',
                   'font-size:10.5px');
          var Ireposo = 0.045;                       /* Arduino Uno en reposo */
          var horas = 24 * 365;
          var kwh = Ireposo * 5 * horas / 1000;
          var kwhAct = r.Ic * V.v * (vr === 'A' ? 0.004 : (vr === 'B' ? 0.15 : 0.20))
                     * horas / 1000;
          var CONS = [
            ['la placa en reposo', mA(Ireposo) + ' \\u00b7 ' + coma(Ireposo * 5, 2) + ' W'],
            ['al a\\u00f1o, sin hacer nada', coma(kwh, 1) + ' kWh'],
            ['el actuador al a\\u00f1o', coma(kwhAct, 1) + ' kWh'],
            ['a 0,15 \\u20ac/kWh', coma((kwh + kwhAct) * 0.15, 2) + ' \\u20ac']
          ];
          x = 14;
          for(i = 0; i < CONS.length; i++){
            s += caja(x, 334, 148, 44, 'var(--surface)', 'var(--line)', 1.2);
            s += rot(x + 9, 350, CONS[i][0], 'font-size:8.5px');
            s += rot(x + 9, 369, CONS[i][1],
                     'font-size:13px;fill:var(--ink);font-weight:500');
            x += 153;
          }
          s += rot(14, 396, 'La placa gasta ' + coma(Ireposo * 5, 2) + ' W las 8760 horas del '
                   + 'a\\u00f1o: es poco, pero no es cero,', 'font-size:9.5px');
          s += rot(14, 410, 'y va en la defensa igual que el agua. El reparto de horas del '
                   + 'actuador es una estimaci\\u00f3n nuestra;', 'font-size:9.5px');
          s += rot(14, 424, 'lo vuestro sale de medirlo.', 'font-size:9.5px');

          svg.innerHTML = s;

          /* ------------------------- el pie ------------------------- */
          var t = '<b>' + V.n + '.</b> ';
          if(!r.alcanza)
            t += 'El divisor sigue siendo un divisor y la f&oacute;rmula sigue valiendo: '
               + '5 &middot; ' + ohm(r.Rs) + ' / (' + ohm(r.RF) + ' + ' + ohm(r.Rs) + ') = <b>'
               + coma(r.Vnodo, 2) + ' V</b>. Lo que pasa es que la R fija es <b>'
               + Math.round(r.RF / r.Rs) + ' veces</b> mayor que el sensor, as&iacute; que se '
               + 'queda con casi toda la tensi&oacute;n y al sensor no le deja sitio: en '
               + '<b>todo</b> el recorrido del sensor la cuenta va de <b>' + r.cMin + ' a '
               + r.cMax + '</b>, y el umbral est&aacute; en ' + V.umbral + '. <b>El sistema no '
               + 'puede actuar nunca</b>, y el programa no tiene ni un fallo. Es la regla de la '
               + 'sesi&oacute;n 1 con vuestros n&uacute;meros: la fija tiene que parecerse al '
               + 'sensor.<br>Y hay una segunda raz&oacute;n, m&aacute;s fina: con esa R fija el '
               + 'pin ve <b>' + ohm(r.Rsrc) + '</b> de impedancia, y la corriente de fuga que '
               + 'admite la hoja del ATmega328P (1 &micro;A) le mete <b>' + coma(r.err, 2)
               + ' V</b> de error. Por eso el fabricante recomienda <b>no pasar de '
               + '10 k&#8486;</b> de impedancia de fuente.';
          else if(!r.masa)
            t += 'La medida es buena, el programa decide bien y la base conduce. Pero '
               + 'las dos masas <b>no est&aacute;n unidas</b>, as&iacute; que la corriente '
               + 'del actuador no tiene camino de vuelta: <b>' + mA(0) + '</b>. Un cable de '
               + 'diez c&eacute;ntimos.';
          else if(r.quiere && !r.saturado)
            t += 'Ib = (' + coma(r.VCC, 1) + ' &minus; 1,6) / ' + ohm(r.RB) + ' = <b>'
               + mA(r.Ib) + '</b>. Con &beta; = 1000 el transistor puede dejar pasar '
               + mA(r.icpos) + ', y el actuador pide ' + mA(V.i) + ': <b>no llega</b>. Se '
               + 'queda a medio abrir, con ' + coma(r.Vce, 2) + ' V encima y <b>'
               + Math.round(r.Pot * 1000) + ' mW</b> de calor dentro.';
          else if(!r.diodo && V.L > 0)
            t += 'Hoy funciona. Pero sin diodo, al cortar la bobina de ' + coma(V.L * 1000, 0)
               + ' mH con ' + mA(r.Ic) + ' pasando: V = L &middot; &Delta;I / &Delta;t = <b>'
               + volt(r.pico) + '</b>, y el TIP120 aguanta ' + TIP120.vceo + ' V. Tres '
               + 'c&eacute;ntimos.';
          else if(r.frac < 0.9 && r.quiere)
            t += 'La pila est&aacute; gastada: da <b>' + coma(r.vbat, 1) + ' V</b> en vez de '
               + V.vbat + '. Al actuador le llegan <b>' + coma(r.Vact, 1) + ' V</b> en vez de '
               + coma(V.vbat - 1, 1) + ', un ' + Math.round(r.frac * 100)
               + ' % de lo normal. No falla: <b>rinde menos</b>, y eso es mucho peor de '
               + 'encontrar, porque nada da error y la cuenta del sensor <b>ni se inmuta</b>: '
               + 'es ratiom&eacute;trica.';
          else if(r.quiere)
            t += 'La magnitud vale ' + (vr === 'C' ? lux(r.mag)
                                                   : coma(r.mag, vr === 'B' ? 1 : 0) + V.u)
               + ', el sensor ' + ohm(r.Rs) + ', el divisor da ' + coma(r.Vnodo, 2)
               + ' V, el conversor <b>' + r.cuenta + '</b>, el umbral est&aacute; en '
               + V.umbral + ' y el programa manda actuar. La base se lleva ' + mA(r.Ib)
               + ', el transistor satura con margen <b>&times;'
               + coma(r.icpos / V.i, 1) + '</b> y el actuador recibe ' + mA(r.Ic) + ' a '
               + coma(r.Vact, 1) + ' V &mdash;el Darlington se queda con 1 V, que es el precio '
               + 'de llevar dos uniones dentro&mdash;. <b>Siete eslabones, y ninguno roto.</b>';
          else
            t += 'El programa no pide actuar: la cuenta es ' + r.cuenta + ' y el umbral '
               + V.umbral + '. Mueve el deslizador hasta que lo pida.';

          pie.innerHTML = t
            + '<br><span style="font-size:12.5px">Todos los n&uacute;meros de esta escena salen '
            + 'de las cuentas de las siete sesiones anteriores, encadenadas: el divisor de la S1, '
            + 'el conversor de la S1, el transistor y el diodo de la S2, la masa com&uacute;n de '
            + 'la S5 y el consumo de esta. Los <b>modelos de los tres sensores</b> (sonda de '
            + 'suelo, NTC 10 k&#8486; B3950 y LDR GL5528) son los del fabricante o los nuestros, '
            + 'y est&aacute;n dichos en sus sesiones. El reparto de horas del actuador es una '
            + 'estimaci&oacute;n para dar orden de magnitud: <b>el vuestro se mide</b>.</span>';
        }

        function refrescaEtq(){
          var V = VARIANTES[vr], x = +mIn.value;
          mEt.textContent = V.etq;
          var m = V.mag(x);
          mTx.textContent = vr === 'C'
            ? lux(m) : coma(m, vr === 'B' ? 1 : 0) + V.u;
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
        pulsa(segV, 'data-v', function(v){ vr = v; });
        pulsa(segF, 'data-a', function(v){ fallo = v; });
        mIn.addEventListener('input', function(){ refrescaEtq(); pinta(); });

        refrescaEtq();
        pinta();
      })();
      </script>
'''
