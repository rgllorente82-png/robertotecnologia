# -*- coding: utf-8 -*-
"""Las cuatro escenas de la unidad 4 de 4.o (Mecanismos y sistemas de control).

Ninguna es una animacion grabada. Las cuatro INTEGRAN o CALCULAN de verdad, y
el numero que sale en pantalla es siempre el resultado de la cuenta que la
propia escena ensena al lado:

  LAZO (S1)   integra por Euler, con paso de 1 s, el mismo modelo termico en
              dos hornos a la vez: uno en lazo abierto (potencia fija, la que
              se calibro en fabrica) y otro en lazo cerrado (mide, compara y
              corrige). Las dos curvas del grafico son esa integracion. Las
              temperaturas finales que anuncia el pie se obtienen aparte, del
              equilibrio  u*P = k*(T - Tamb),  y la simulacion converge a
              ellas: si dejaran de coincidir, el verificador lo caza.

  BLOQUES (S2) ejecuta el lazo del diagrama diez veces por segundo simulado.
              Los numeros que aparecen DENTRO de cada bloque son los que
              circulan de verdad: la magnitud fisica, la lectura del sensor
              (con su recta de calibracion), la consigna convertida a esas
              mismas unidades, el error y la orden. El interruptor de la
              realimentacion corta la flecha de vuelta y deja el mismo
              aparato en lazo abierto, con temporizador.

  TODONADA (S3) simula tres horas de una habitacion con caldera y termostato
              de dos posiciones, con paso de 2 s. Los ciclos por hora, la
              amplitud, la media y el porcentaje de tiempo encendida NO estan
              escritos: se miden sobre la ultima hora de esa simulacion.

  MOTOR (S4)  dibuja el par de engranajes con GEOMETRIA CORRECTA (radio
              primitivo r = m*z/2, los dos con el mismo modulo, distancia
              entre ejes r1+r2 y el desfase de medio paso que hace que
              engranen) y calcula el par necesario, el par disponible tras la
              reductora, la velocidad de salida y el tiempo de maniobra.

Las clases CSS llevan prefijo propio (lz-, bq-, tn-, mt-) para no chocar entre
ellas ni con las de la pagina. Ninguna empieza por "test-".
"""

# ==========================================================================
# S1 - Los dos hornos: lazo abierto y lazo cerrado, a la vez
# ==========================================================================
LAZO = u'''
      <div class="escena" id="esc-lz">
        <div class="escena-barra">
          <span class="escena-titulo">Dos hornos, la misma orden &middot; mete la perturbaci&oacute;n y mira qui&eacute;n la aguanta</span>
          <div class="seg">
            <button type="button" data-a="play" id="lz-play">&#9654; Marcha</button>
            <button type="button" data-a="hora">Avanza 1 hora</button>
            <button type="button" data-a="reset">Reiniciar</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 680 310" id="svg-lz" role="img"
               aria-label="Gr&aacute;fico de la temperatura de dos hornos frente al tiempo, con la consigna de 180 grados"></svg>
          <div class="lz-mandos">
            <div class="lz-fila">
              <label for="lz-tamb">Temperatura de la cocina</label>
              <input type="range" id="lz-tamb" min="-5" max="25" step="1" value="20">
              <span class="val" id="lz-tamb-v">20 &deg;C</span>
            </div>
            <div class="lz-fila">
              <label for="lz-k">P&eacute;rdidas (puerta mal cerrada)</label>
              <input type="range" id="lz-k" min="6" max="15" step="1" value="6">
              <span class="val" id="lz-k-v">6 W/&deg;C</span>
            </div>
          </div>
          <div class="lz-tablero">
            <div class="lz-caja lz-ab">
              <h5>Lazo abierto &middot; la tostadora</h5>
              <p class="lz-num" id="lz-ta">20,0 &deg;C</p>
              <p class="lz-det" id="lz-da"></p>
            </div>
            <div class="lz-caja lz-ce">
              <h5>Lazo cerrado &middot; el horno con term&oacute;stato</h5>
              <p class="lz-num" id="lz-tc">20,0 &deg;C</p>
              <p class="lz-det" id="lz-dc"></p>
            </div>
          </div>
        </div>
        <div class="pie" id="pie-lz"></div>
      </div>

      <style>
      .lz-mandos{margin-top:10px}
      .lz-fila{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:0 0 8px;
        font-family:var(--f-m);font-size:12.5px;color:var(--ink)}
      .lz-fila label{min-width:210px}
      .lz-fila input[type="range"]{flex:1 1 160px;min-width:130px;accent-color:var(--goo-azul)}
      .lz-fila .val{font-weight:500;color:var(--goo-azul);min-width:72px;text-align:right}
      .lz-tablero{display:flex;gap:12px;flex-wrap:wrap;margin-top:12px}
      .lz-caja{flex:1 1 250px;min-width:230px;border:1.5px solid var(--line);border-radius:2px;
        padding:11px 13px;background:var(--surface)}
      .lz-caja h5{margin:0 0 6px;font:500 12px var(--f-m);letter-spacing:.06em;text-transform:uppercase;
        color:var(--ink-soft)}
      .lz-ab{border-left:5px solid var(--goo-rojo)}
      .lz-ce{border-left:5px solid var(--goo-azul)}
      .lz-num{margin:0;font-family:var(--f-m);font-size:24px;font-weight:500;color:var(--ink)}
      .lz-det{margin:5px 0 0;font-family:var(--f-m);font-size:12px;line-height:1.7;color:var(--ink-soft)}
      .lz-det b{color:var(--ink)}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-lz');
        if(!svg) return;
        var caja = document.getElementById('esc-lz');
        var pie  = document.getElementById('pie-lz');

        /* ---- el modelo, el mismo para los dos hornos ------------------
           Un horno pequeno de laboratorio. Balance de energia:
             C * dT/dt = u*P - k*(T - Tamb)
           C capacidad termica (J por grado), k perdidas (W por grado),
           P potencia de la resistencia, u la fraccion que se le aplica.   */
        var C = 3000, P = 1500, TREF = 180;
        var K0 = 6, TAMB0 = 20;               /* condiciones de calibracion */
        var U0 = K0 * (TREF - TAMB0) / P;     /* = 0,64 exactamente         */

        var v = {tamb: 20, k: 6};
        var Ta, Tc, t, hist, corriendo = false, raf = null;

        function reinicia(){
          Ta = v.tamb; Tc = v.tamb; t = 0; hist = [[0, Ta, Tc]];
          corriendo = false;
          document.getElementById('lz-play').innerHTML = '&#9654; Marcha';
          pinta();
        }

        function paso(dt){
          /* Euler explicito con dt = 1 s: a esta escala es de sobra estable
             (la constante de tiempo del horno es C/k, de 200 a 500 s).     */
          var ua = U0;                           /* abierto: siempre lo mismo */
          var uc = (Tc < TREF) ? 1 : 0;          /* cerrado: mide y decide    */
          Ta += dt * (ua * P - v.k * (Ta - v.tamb)) / C;
          Tc += dt * (uc * P - v.k * (Tc - v.tamb)) / C;
          t += dt;
          if(t % 10 === 0) hist.push([t, Ta, Tc]);
          if(hist.length > 900) hist.shift();
        }

        /* ---- lo que dice la cuenta, sin simular ---------------------- */
        function finAbierto(){ return v.tamb + U0 * P / v.k; }
        function necesariaCerrado(){ return v.k * (TREF - v.tamb) / P; }
        function finCerrado(){
          var u = necesariaCerrado();
          return (u <= 1) ? TREF : v.tamb + P / v.k;
        }

        function n1(x){ return x.toFixed(1).replace('.', ','); }
        function n0(x){ return Math.round(x).toString(); }

        function ejeX(){ return Math.max(600, Math.ceil(t / 600) * 600); }

        function pinta(){
          var X0 = 58, X1 = 500, Y0 = 26, Y1 = 262, TMAX = 260;
          var tmax = ejeX();
          var px = function(s){ return X0 + (X1 - X0) * s / tmax; };
          var py = function(T){ return Y1 - (Y1 - Y0) * Math.min(T, TMAX) / TMAX; };
          var m = '';

          /* rejilla y eje de temperatura */
          var g, yy;
          for(g = 0; g <= 250; g += 50){
            yy = py(g);
            m += '<line x1="' + X0 + '" y1="' + yy.toFixed(1) + '" x2="' + X1
               + '" y2="' + yy.toFixed(1) + '" stroke="currentColor" stroke-width="1" opacity=".13"/>'
               + '<text x="' + (X0 - 7) + '" y="' + (yy + 4).toFixed(1)
               + '" class="ejeq" text-anchor="end">' + g + '</text>';
          }
          /* eje de tiempo, en minutos */
          var mn;
          for(mn = 0; mn <= tmax / 60; mn += (tmax > 1800 ? 10 : 5)){
            var xx = px(mn * 60);
            m += '<line x1="' + xx.toFixed(1) + '" y1="' + Y1 + '" x2="' + xx.toFixed(1)
               + '" y2="' + (Y1 + 4) + '" stroke="currentColor" stroke-width="1" opacity=".35"/>'
               + '<text x="' + xx.toFixed(1) + '" y="' + (Y1 + 17)
               + '" class="ejeq" text-anchor="middle">' + mn + '</text>';
          }
          m += '<text x="' + X0 + '" y="' + (Y0 - 10) + '" class="ejeq">grados</text>'
             + '<text x="' + X1 + '" y="' + (Y1 + 31) + '" class="ejeq" text-anchor="end">minutos</text>';

          /* la consigna */
          m += '<line x1="' + X0 + '" y1="' + py(TREF).toFixed(1) + '" x2="' + X1
             + '" y2="' + py(TREF).toFixed(1) + '" stroke="currentColor" stroke-width="1.5"'
             + ' stroke-dasharray="6 4" opacity=".55"/>'
             + '<text x="' + (X1 - 4) + '" y="' + (py(TREF) - 6).toFixed(1)
             + '" class="etq" text-anchor="end">consigna 180 &deg;C</text>';

          /* las dos curvas: son la integracion, punto a punto */
          var i, da = '', dc = '';
          for(i = 0; i < hist.length; i++){
            da += (i ? ' L ' : 'M ') + px(hist[i][0]).toFixed(1) + ' ' + py(hist[i][1]).toFixed(1);
            dc += (i ? ' L ' : 'M ') + px(hist[i][0]).toFixed(1) + ' ' + py(hist[i][2]).toFixed(1);
          }
          m += '<path d="' + dc + '" fill="none" stroke="#1a73e8" stroke-width="2.4"/>'
             + '<path d="' + da + '" fill="none" stroke="#ea4335" stroke-width="2.4"/>';

          /* los dos termometros, a escala */
          var term = function(cx, T, col, rot){
            var h = 168 * Math.min(T, TMAX) / TMAX;
            return '<rect x="' + (cx - 9) + '" y="60" width="18" height="172" rx="9" fill="none"'
                 + ' stroke="currentColor" stroke-width="1.6" opacity=".45"/>'
                 + '<rect x="' + (cx - 5) + '" y="' + (232 - h).toFixed(1) + '" width="10" height="'
                 + (h + 4).toFixed(1) + '" rx="5" fill="' + col + '"/>'
                 + '<circle cx="' + cx + '" cy="244" r="14" fill="' + col + '"/>'
                 + '<text x="' + cx + '" y="272" class="etq" text-anchor="middle">' + rot + '</text>'
                 + '<text x="' + cx + '" y="288" class="ejeq" text-anchor="middle">'
                 + n0(T) + ' &deg;C</text>';
          };
          m += term(566, Ta, '#ea4335', 'abierto') + term(636, Tc, '#1a73e8', 'cerrado');

          /* leyenda, en la fila de encima del grafico para no taparlo */
          m += '<rect x="' + (X0 + 62) + '" y="' + (Y0 - 14) + '" width="11" height="3" fill="#ea4335"/>'
             + '<text x="' + (X0 + 78) + '" y="' + (Y0 - 10) + '" class="ejeq">lazo abierto</text>'
             + '<rect x="' + (X0 + 172) + '" y="' + (Y0 - 14) + '" width="11" height="3" fill="#1a73e8"/>'
             + '<text x="' + (X0 + 188) + '" y="' + (Y0 - 10) + '" class="ejeq">lazo cerrado</text>';

          svg.innerHTML = m;

          /* ---- los tableros ---- */
          document.getElementById('lz-ta').innerHTML = n1(Ta) + ' &deg;C';
          document.getElementById('lz-tc').innerHTML = n1(Tc) + ' &deg;C';
          var ea = Ta - TREF, ec = Tc - TREF;
          document.getElementById('lz-da').innerHTML =
            'Potencia aplicada: <b>' + n0(U0 * 100) + ' %</b> (' + n0(U0 * P) + ' W), '
            + 'siempre la misma.<br>Error ahora: <b>' + (ea >= 0 ? '+' : '') + n1(ea) + ' &deg;C</b>'
            + '<br>Se quedar&aacute; en ' + n0(v.tamb) + ' + 0,64 &times; 1500 / ' + v.k
            + ' = <b>' + n0(finAbierto()) + ' &deg;C</b>';
          var un = necesariaCerrado();
          document.getElementById('lz-dc').innerHTML =
            'Potencia aplicada: <b>' + ((Tc < TREF) ? '100 %' : '0 %')
            + '</b>, la que haga falta en cada momento.<br>Error ahora: <b>'
            + (ec >= 0 ? '+' : '') + n1(ec) + ' &deg;C</b>'
            + '<br>Necesita ' + v.k + ' &times; (180 &minus; ' + n0(v.tamb) + ') / 1500 = <b>'
            + n0(un * 100) + ' %</b> de media'
            + (un <= 1 ? ', y lo tiene.' : ', y solo tiene el 100 %: <b>no llega</b>.');

          pie.innerHTML =
            '<b>Minuto ' + n1(t / 60) + '.</b> Los dos hornos llevan la misma resistencia y las '
            + 'mismas p&eacute;rdidas. El de la izquierda aplica el <b>64&nbsp;%</b> que alguien '
            + 'calcul&oacute; un d&iacute;a con la cocina a 20&nbsp;&deg;C y la puerta bien cerrada; '
            + 'el de la derecha <b>mira el term&oacute;metro</b> antes de decidir. Mueve los dos '
            + 'mandos y mira qui&eacute;n se entera.'
            + (un > 1 ? ' <b>Ojo:</b> con estas p&eacute;rdidas ni el cerrado llega a 180&nbsp;&deg;C. '
                      + 'Un lazo cerrado corrige mientras le quede resistencia que dar; cuando la '
                      + 'gasta toda, se acab&oacute;.' : '');
        }

        function cuadro(){
          var i;
          for(i = 0; i < 20; i++) paso(1);      /* 20 s de horno por cuadro */
          pinta();
          if(corriendo) raf = requestAnimationFrame(cuadro);
        }

        caja.addEventListener('click', function(e){
          var b = e.target.closest('button[data-a]');
          if(!b) return;
          if(b.dataset.a === 'play'){
            corriendo = !corriendo;
            b.innerHTML = corriendo ? '&#10073;&#10073; Pausa' : '&#9654; Marcha';
            if(corriendo) raf = requestAnimationFrame(cuadro);
            else if(raf) cancelAnimationFrame(raf);
          } else if(b.dataset.a === 'hora'){
            var i;
            for(i = 0; i < 3600; i++) paso(1);
            pinta();
          } else {
            if(raf) cancelAnimationFrame(raf);
            reinicia();
          }
        });

        function mando(id, clave, sufijo){
          var r = document.getElementById(id);
          r.addEventListener('input', function(){
            v[clave] = +r.value;
            document.getElementById(id + '-v').innerHTML = r.value + sufijo;
            pinta();
          });
        }
        mando('lz-tamb', 'tamb', ' &deg;C');
        mando('lz-k', 'k', ' W/&deg;C');

        reinicia();
      })();
      </script>
'''


# ==========================================================================
# S2 - El diagrama de bloques con numeros dentro
# ==========================================================================
BLOQUES = u'''
      <div class="escena" id="esc-bq">
        <div class="escena-barra">
          <span class="escena-titulo">El diagrama, con los n&uacute;meros de verdad circulando por dentro</span>
          <div class="seg" id="seg-bq">
            <button type="button" data-p="0" aria-pressed="true">Riego</button>
            <button type="button" data-p="1">Ventilaci&oacute;n</button>
            <button type="button" data-p="2">L&aacute;mpara</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 690 300" id="svg-bq" role="img"
               aria-label="Diagrama de bloques de un sistema de control con los valores num&eacute;ricos dentro de cada bloque"></svg>
          <div class="bq-mandos">
            <div class="bq-fila">
              <label for="bq-mag" id="bq-mag-l">Magnitud</label>
              <input type="range" id="bq-mag" min="0" max="100" step="1" value="25">
              <span class="val" id="bq-mag-v"></span>
            </div>
            <div class="bq-fila">
              <label for="bq-ref" id="bq-ref-l">Consigna</label>
              <input type="range" id="bq-ref" min="0" max="100" step="1" value="40">
              <span class="val" id="bq-ref-v"></span>
            </div>
            <label class="bq-chk"><input type="checkbox" id="bq-abierto">
              cortar la realimentaci&oacute;n (y trabajar con temporizador, como en lazo abierto)</label>
            <div class="seg">
              <button type="button" data-a="ir" id="bq-ir">&#9654; Poner en marcha</button>
              <button type="button" data-a="reset">Reiniciar</button>
            </div>
          </div>
          <p class="bq-cuenta" id="bq-cuenta"></p>
        </div>
        <div class="pie" id="pie-bq"></div>
      </div>

      <style>
      .bq-mandos{margin-top:10px}
      .bq-fila{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:0 0 8px;
        font-family:var(--f-m);font-size:12.5px;color:var(--ink)}
      .bq-fila label{min-width:225px}
      .bq-fila input[type="range"]{flex:1 1 150px;min-width:130px;accent-color:var(--goo-azul)}
      .bq-fila .val{font-weight:500;color:var(--goo-azul);min-width:78px;text-align:right}
      .bq-chk{display:flex;align-items:center;gap:8px;font-family:var(--f-m);font-size:12.5px;
        color:var(--ink-soft);margin:0 0 9px;cursor:pointer;line-height:1.5}
      .bq-chk input{accent-color:var(--goo-azul);flex:none}
      .bq-cuenta{margin:11px 0 0;font-family:var(--f-m);font-size:12.5px;line-height:1.8;
        color:var(--ink-soft);border-left:4px solid var(--goo-azul);padding:6px 0 6px 12px}
      .bq-cuenta b{color:var(--ink)}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-bq');
        if(!svg) return;
        var caja  = document.getElementById('esc-bq');
        var seg   = document.getElementById('seg-bq');
        var pie   = document.getElementById('pie-bq');
        var cuenta= document.getElementById('bq-cuenta');

        function n1(x){ return x.toFixed(1).replace('.', ','); }
        function n0(x){ return Math.round(x).toString(); }

        /* ------------------------------------------------------------------
           Tres de los cinco proyectos del catalogo. Cada uno trae su recta de
           calibracion (la que se mide en clase con el sensor en la mano) y su
           modelo de como cambia la magnitud fisica. Lo que NO cambia de uno a
           otro es el diagrama: esa es toda la gracia.
           ------------------------------------------------------------------ */
        var PROY = [
          { nom:'Riego de la planta del aula',
            mag:'Humedad del suelo', uni:' %', min:0, max:100, ini:20, ref:40,
            sensor:'Sonda capacitiva en A0',
            /* medido en clase: en aire 620, hundida en agua 280 */
            lee:  function(x){ return Math.round(620 - 3.4 * x); },
            cuenta: function(x){ return 'lectura = 620 &minus; 3,4 &times; ' + n1(x) + ' = <b>'
                                      + this.lee(x) + '</b>'; },
            calib:'620 &minus; 3,4 &times; humedad',
            /* seco = lectura ALTA -> el error positivo pide bomba */
            err:  function(L, Lr){ return L - Lr; },
            errTxt:'error = lectura &minus; consigna',
            actua:'Bomba',
            /* el agua sube la humedad; el sol la baja */
            avanza: function(x, on){ return x + (on ? 0.55 : 0) - 0.03; },
            orden: function(e){ return e > 0; },
            ordenTxt:'si error &gt; 0 &rarr; bomba ON',
            tfijo: 38,
            pie:'<b>Riego autom&aacute;tico.</b> El sensor no da humedad: da un n&uacute;mero entre '
              + '280 y 620. La consigna hay que traducirla a ESE idioma antes de poder restar.' },

          { nom:'Aviso de aula mal ventilada',
            mag:'CO&#8322; en el aula', uni:' ppm', min:400, max:2000, ini:1500, ref:800,
            sensor:'M&oacute;dulo digital por I&sup2;C',
            lee:  function(x){ return Math.round(x); },
            cuenta: function(x){ return 'lectura = <b>' + this.lee(x) + ' ppm</b> (el m&oacute;dulo '
                                      + 'ya entrega la unidad f&iacute;sica: aqu&iacute; no hay que traducir nada)'; },
            calib:'el m&oacute;dulo ya da ppm',
            err:  function(L, Lr){ return L - Lr; },
            errTxt:'error = medida &minus; consigna',
            actua:'Ventilador',
            avanza: function(x, on){ return x + (on ? -22 : 0) + 6; },
            orden: function(e){ return e > 0; },
            ordenTxt:'si error &gt; 0 &rarr; ventilador ON',
            tfijo: 45,
            pie:'<b>Ventilaci&oacute;n.</b> Cuando el sensor ya habla en unidades f&iacute;sicas, el '
              + 'bloque de conversi&oacute;n desaparece&hellip; pero el diagrama es exactamente el mismo.' },

          { nom:'L&aacute;mpara de estudio que se ajusta sola',
            mag:'Luz que entra por la ventana', uni:' lx', min:0, max:600, ini:120, ref:300,
            sensor:'LDR con divisor, en A0',
            /* medido en clase: a oscuras 90, con la persiana abierta 870 */
            lee:  function(x){ return Math.round(90 + 1.3 * x); },
            cuenta: function(x){ return 'lectura = 90 + 1,3 &times; ' + n0(x) + ' = <b>'
                                      + this.lee(x) + '</b>'; },
            calib:'90 + 1,3 &times; lux',
            /* aqui falta luz cuando la lectura es BAJA */
            invertido: true,
            err:  function(L, Lr){ return Lr - L; },
            errTxt:'error = consigna &minus; lectura',
            actua:'LED de la l&aacute;mpara',
            /* el LED ilumina la MISMA mesa que mira el sensor: por eso se muerde la cola */
            avanza: function(x, on){ return x; },
            aporta: 260,
            orden: function(e){ return e > 0; },
            ordenTxt:'si error &gt; 0 &rarr; LED ON',
            tfijo: 30,
            pie:'<b>L&aacute;mpara.</b> Aqu&iacute; el actuador ilumina <b>la misma mesa</b> que mira el '
              + 'sensor. Encender cambia lo que se va a medir un instante despu&eacute;s: eso es '
              + 'realimentaci&oacute;n en estado puro, y por eso parpadea.' }
        ];

        var p = 0, ext = 20, ref = 40, abierto = false;
        var on = false, t = 0, tRestante = 0, corriendo = false, raf = null;
        var serie = [];

        function P(){ return PROY[p]; }

        /* magnitud que VE el sensor = la de fuera + lo que aporte el actuador */
        function magnitud(){
          var d = P();
          return ext + (d.aporta && on ? d.aporta : 0);
        }

        function reinicia(){
          var d = P();
          ext = d.ini; ref = d.ref;
          on = false; t = 0; tRestante = 0; serie = [];
          corriendo = false;
          document.getElementById('bq-ir').innerHTML = '&#9654; Poner en marcha';
          var r = document.getElementById('bq-mag');
          r.min = d.min; r.max = d.max; r.value = ext;
          var q = document.getElementById('bq-ref');
          q.min = d.min; q.max = d.max; q.value = ref;
          document.getElementById('bq-mag-l').innerHTML = d.mag;
          document.getElementById('bq-ref-l').innerHTML = 'Consigna (lo que le pides)';
          document.getElementById('bq-mag-v').innerHTML = n0(ext) + d.uni;
          document.getElementById('bq-ref-v').innerHTML = n0(ref) + d.uni;
          pinta();
        }

        function paso(){
          var d = P();
          t += 0.1;
          if(abierto){
            /* lazo abierto: el temporizador manda, la medida no se mira */
            if(tRestante > 0){ on = true; tRestante -= 0.1; }
            else on = false;
          } else {
            var L  = d.lee(magnitud());
            var Lr = d.lee(ref);
            on = d.orden(d.err(L, Lr));
          }
          ext = Math.min(d.max, Math.max(d.min, d.avanza(ext, on)));
          if(Math.round(t * 10) % 2 === 0){
            serie.push(magnitud());
            if(serie.length > 220) serie.shift();
          }
        }

        /* --------- el dibujo del diagrama, con sus numeros dentro -------- */
        function bloque(x, y, w, h, rot, val, activo){
          return '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h
               + '" rx="3" fill="var(--surface)" stroke="' + (activo ? '#34a853' : 'currentColor')
               + '" stroke-width="' + (activo ? 2.4 : 1.6) + '" opacity="' + (activo ? 1 : .85) + '"/>'
               + '<text x="' + (x + w / 2) + '" y="' + (y + 17)
               + '" class="ejeq" text-anchor="middle">' + rot + '</text>'
               + '<text x="' + (x + w / 2) + '" y="' + (y + 40)
               + '" class="etq" text-anchor="middle" style="font-size:14px">' + val + '</text>';
        }
        function flecha(x1, y1, x2, y2, tenue){
          return '<path d="M ' + x1 + ' ' + y1 + ' L ' + x2 + ' ' + y2
               + '" stroke="currentColor" stroke-width="1.8" fill="none" marker-end="url(#bqp)"'
               + (tenue ? ' opacity=".22" stroke-dasharray="5 4"' : '') + '/>';
        }

        function pinta(){
          var d = P();
          var M  = magnitud();
          var L  = d.lee(M);
          var Lr = d.lee(ref);
          var e  = abierto ? 0 : d.err(L, Lr);
          /* La orden que se ENSENA es la que sale de los numeros que se ensenan,
             este el lazo corriendo o parado: si no, el diagrama dice una cosa y
             el actuador otra. */
          var orden = abierto ? (tRestante > 0) : d.orden(e);
          var m = '<defs><marker id="bqp" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7"'
                + ' markerHeight="7" orient="auto-start-reverse">'
                + '<path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>';

          m += bloque(14, 34, 96, 52, 'CONSIGNA', n0(ref) + d.uni, false);
          m += flecha(110, 60, 142, 60);
          /* comparador */
          m += '<circle cx="164" cy="60" r="21" fill="var(--surface)" stroke="'
             + (abierto ? 'currentColor' : '#34a853') + '" stroke-width="'
             + (abierto ? 1.6 : 2.4) + '"' + (abierto ? ' opacity=".35"' : '') + '/>'
             + '<text x="164" y="66" class="etq" text-anchor="middle" style="font-size:17px">'
             + (abierto ? '?' : '&#8722;') + '</text>'
             + '<text x="164" y="24" class="ejeq" text-anchor="middle">COMPARADOR</text>';
          m += flecha(185, 60, 219, 60, abierto);
          m += bloque(220, 34, 116, 52, 'CONTROLADOR',
                      abierto ? ('t = ' + n1(Math.max(0, tRestante)) + ' s') : ('error ' + n0(e)),
                      !abierto);
          m += flecha(336, 60, 370, 60);
          m += bloque(371, 34, 116, 52, 'ACTUADOR', orden ? 'ON' : 'OFF', orden);
          m += flecha(487, 60, 521, 60);
          m += bloque(522, 34, 152, 52, 'PROCESO', n0(M) + d.uni, false);

          /* la flecha de vuelta: la realimentacion */
          var tenue = abierto;
          m += '<path d="M 598 86 L 598 132" stroke="currentColor" stroke-width="1.8" fill="none"'
             + (tenue ? ' opacity=".22" stroke-dasharray="5 4"' : '') + '/>';
          m += bloque(462, 108, 136, 48, 'SENSOR', n0(L), !abierto);
          m += '<path d="M 462 132 L 164 132 L 164 89" stroke="currentColor" stroke-width="1.8"'
             + ' fill="none" marker-end="url(#bqp)"'
             + (tenue ? ' opacity=".22" stroke-dasharray="5 4"' : '') + '/>';
          if(tenue){
            m += '<line x1="292" y1="118" x2="324" y2="146" stroke="#ea4335" stroke-width="3"/>'
               + '<line x1="324" y1="118" x2="292" y2="146" stroke="#ea4335" stroke-width="3"/>'
               + '<text x="308" y="166" class="etq" text-anchor="middle" style="fill:#ea4335">'
               + 'realimentaci&oacute;n cortada</text>';
          }
          /* la consigna, traducida al idioma del sensor. Va a la izquierda del
             comparador para no montarse encima de la flecha de vuelta. */
          if(!abierto){
            m += '<text x="14" y="162" class="ejeq">la consigna, traducida a cuentas: '
               + Lr + '</text>';
          }

          /* --------- la tira de papel: la magnitud contra el tiempo -------- */
          var X0 = 30, X1 = 660, Y0 = 190, Y1 = 278;
          var lo = d.min, hi = d.max + (d.aporta || 0);
          var py = function(x){ return Y1 - (Y1 - Y0) * (x - lo) / (hi - lo); };
          m += '<rect x="' + X0 + '" y="' + Y0 + '" width="' + (X1 - X0) + '" height="' + (Y1 - Y0)
             + '" fill="none" stroke="currentColor" stroke-width="1" opacity=".22"/>';
          m += '<line x1="' + X0 + '" y1="' + py(ref).toFixed(1) + '" x2="' + X1 + '" y2="'
             + py(ref).toFixed(1) + '" stroke="currentColor" stroke-width="1.4" stroke-dasharray="6 4"'
             + ' opacity=".55"/>'
             + '<text x="' + (X1 - 4) + '" y="' + (py(ref) - 5).toFixed(1)
             + '" class="ejeq" text-anchor="end">consigna</text>';
          var i, dd = '';
          for(i = 0; i < serie.length; i++){
            dd += (i ? ' L ' : 'M ') + (X0 + (X1 - X0) * i / 220).toFixed(1)
                + ' ' + py(serie[i]).toFixed(1);
          }
          if(serie.length > 1){
            m += '<path d="' + dd + '" fill="none" stroke="#1a73e8" stroke-width="2"/>';
          } else {
            m += '<circle cx="' + X0 + '" cy="' + py(M).toFixed(1) + '" r="3.5" fill="#1a73e8"/>'
               + '<text x="' + ((X0 + X1) / 2) + '" y="' + (Y0 + 36)
               + '" class="ejeq" text-anchor="middle">pulsa &laquo;Poner en marcha&raquo; y el lazo '
               + 'se pone a trabajar solo</text>';
          }
          m += '<text x="' + (X0 + 4) + '" y="' + (Y0 + 13) + '" class="ejeq">' + d.mag + '</text>';

          svg.innerHTML = m;

          /* --------- la cuenta escrita, paso por paso -------- */
          var txt = '<b>' + d.sensor + '.</b> ' + d.cuenta(M) + '<br>';
          if(abierto){
            txt += 'Sin realimentaci&oacute;n no hay resta que hacer: el controlador solo sabe '
                 + '<b>cu&aacute;nto tiempo le queda</b> de los ' + d.tfijo + ' s que alguien '
                 + 'cronometr&oacute; un d&iacute;a. Quedan <b>' + n1(Math.max(0, tRestante)) + ' s</b>.';
          } else {
            txt += 'Consigna de ' + n0(ref) + d.uni + ' en el idioma del sensor: <b>' + Lr + '</b><br>'
                 + d.errTxt + ' = ' + (d.invertido ? (Lr + ' &minus; ' + L) : (L + ' &minus; ' + Lr))
                 + ' = <b>' + n0(e) + '</b> &rarr; ' + d.ordenTxt + ' &rarr; <b>'
                 + (orden ? 'ENCENDIDO' : 'APAGADO') + '</b>';
          }
          cuenta.innerHTML = txt;
          pie.innerHTML = d.pie;

          /* el mando hace tambien de indicador: cuando el lazo corre, la
             magnitud la mueve el actuador y no la mano */
          document.getElementById('bq-mag').value = ext;
          document.getElementById('bq-mag-v').innerHTML = n0(ext) + d.uni;
        }

        function cuadro(){
          var i;
          for(i = 0; i < 2; i++) paso();
          pinta();
          if(corriendo) raf = requestAnimationFrame(cuadro);
        }

        seg.addEventListener('click', function(ev){
          var b = ev.target.closest('button[data-p]');
          if(!b) return;
          seg.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          p = +b.dataset.p;
          if(raf) cancelAnimationFrame(raf);
          reinicia();
        });

        caja.addEventListener('click', function(ev){
          var b = ev.target.closest('button[data-a]');
          if(!b) return;
          if(b.dataset.a === 'ir'){
            corriendo = !corriendo;
            b.innerHTML = corriendo ? '&#10073;&#10073; Pausa' : '&#9654; Poner en marcha';
            if(corriendo){ if(abierto) tRestante = P().tfijo; raf = requestAnimationFrame(cuadro); }
            else if(raf) cancelAnimationFrame(raf);
          } else {
            if(raf) cancelAnimationFrame(raf);
            reinicia();
          }
        });

        document.getElementById('bq-mag').addEventListener('input', function(){
          ext = +this.value;
          document.getElementById('bq-mag-v').innerHTML = n0(ext) + P().uni;
          pinta();
        });
        document.getElementById('bq-ref').addEventListener('input', function(){
          ref = +this.value;
          document.getElementById('bq-ref-v').innerHTML = n0(ref) + P().uni;
          pinta();
        });
        document.getElementById('bq-abierto').addEventListener('change', function(){
          abierto = this.checked;
          if(abierto) tRestante = P().tfijo;
          pinta();
        });

        reinicia();
      })();
      </script>
'''


# ==========================================================================
# S3 - El termostato de dos posiciones y lo que cuesta
# ==========================================================================
TODONADA = u'''
      <div class="escena" id="esc-tn">
        <div class="escena-barra">
          <span class="escena-titulo">Tres horas de calefacci&oacute;n, simuladas de verdad &middot; toca la hist&eacute;resis</span>
          <div class="seg">
            <button type="button" data-a="reset">Valores de partida</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 690 300" id="svg-tn" role="img"
               aria-label="Gr&aacute;fico de la temperatura de una habitaci&oacute;n con termostato de dos posiciones"></svg>
          <div class="tn-mandos">
            <div class="tn-fila">
              <label for="tn-ref">Consigna del term&oacute;stato</label>
              <input type="range" id="tn-ref" min="16" max="26" step="1" value="21">
              <span class="val" id="tn-ref-v">21 &deg;C</span>
            </div>
            <div class="tn-fila">
              <label for="tn-h">Hist&eacute;resis (ancho de la banda)</label>
              <input type="range" id="tn-h" min="0" max="30" step="1" value="10">
              <span class="val" id="tn-h-v">1,0 &deg;C</span>
            </div>
            <div class="tn-fila">
              <label for="tn-ext">Temperatura de la calle</label>
              <input type="range" id="tn-ext" min="-5" max="18" step="1" value="5">
              <span class="val" id="tn-ext-v">5 &deg;C</span>
            </div>
            <div class="tn-fila">
              <label for="tn-pot">Potencia de la caldera</label>
              <input type="range" id="tn-pot" min="1000" max="5000" step="250" value="2500">
              <span class="val" id="tn-pot-v">2500 W</span>
            </div>
            <label class="tn-chk"><input type="checkbox" id="tn-retardo">
              el term&oacute;stato est&aacute; metido en su caja y se entera tarde (retardo de 2 min)</label>
          </div>
          <div class="tn-tablero" id="tn-tablero"></div>
        </div>
        <div class="pie" id="pie-tn"></div>
      </div>

      <style>
      .tn-mandos{margin-top:10px}
      .tn-fila{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:0 0 8px;
        font-family:var(--f-m);font-size:12.5px;color:var(--ink)}
      .tn-fila label{min-width:225px}
      .tn-fila input[type="range"]{flex:1 1 150px;min-width:130px;accent-color:var(--goo-azul)}
      .tn-fila .val{font-weight:500;color:var(--goo-azul);min-width:74px;text-align:right}
      .tn-chk{display:flex;align-items:center;gap:8px;font-family:var(--f-m);font-size:12.5px;
        color:var(--ink-soft);margin:2px 0 0;cursor:pointer;line-height:1.5}
      .tn-chk input{accent-color:var(--goo-azul);flex:none}
      .tn-tablero{display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(138px,1fr));margin-top:13px}
      .tn-dato{border:1.5px solid var(--line);border-radius:2px;background:var(--surface);padding:9px 11px}
      .tn-dato span{display:block;font-family:var(--f-m);font-size:10.5px;letter-spacing:.06em;
        text-transform:uppercase;color:var(--ink-soft);margin-bottom:3px;line-height:1.4}
      .tn-dato b{font-family:var(--f-m);font-size:18px;font-weight:500;color:var(--ink)}
      .tn-dato.malo b{color:var(--goo-rojo)}
      .tn-dato.bien b{color:var(--goo-verde)}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-tn');
        if(!svg) return;
        var caja = document.getElementById('esc-tn');
        var pie  = document.getElementById('pie-tn');
        var tab  = document.getElementById('tn-tablero');

        function n1(x){ return x.toFixed(1).replace('.', ','); }
        function n2(x){ return x.toFixed(2).replace('.', ','); }
        function n0(x){ return Math.round(x).toString(); }

        /* ---- la habitacion -------------------------------------------
           C * dT/dt = u*P - k*(T - Text).   C y k son los de un dormitorio
           con radiador: la constante de tiempo sale de C/k = 4.167 s, algo
           mas de una hora, que es lo que tarda de verdad en enfriarse.     */
        var C = 250000, K = 60, DT = 2, HORAS = 3;
        var TAU_S = 120;                      /* retardo del sensor, en s   */

        var v = {ref:21, h:1.0, ext:5, pot:2500, retardo:false};

        /* Simula HORAS horas y devuelve la serie y las medidas. Nada de esto
           esta escrito a mano: son cuentas sobre la ultima hora.           */
        function simula(){
          var n = HORAS * 3600 / DT;
          var T = v.ext, Ts = v.ext, on = true;
          var serie = [], cambios = [], i, u, encendidos = 0, ultima = 'on';
          for(i = 0; i < n; i++){
            var medida = v.retardo ? Ts : T;
            /* termostato de dos posiciones con hysteresis simetrica */
            if(on && medida > v.ref + v.h / 2) on = false;
            else if(!on && medida < v.ref - v.h / 2) on = true;
            if(on !== (ultima === 'on')){ cambios.push(i * DT); ultima = on ? 'on' : 'off'; }
            u = on ? 1 : 0;
            if(on) encendidos++;
            T  += DT * (u * v.pot - K * (T - v.ext)) / C;
            Ts += DT * (T - Ts) / TAU_S;
            serie.push([i * DT, T, on]);
          }
          /* las medidas se toman en la ULTIMA hora: la primera es el arranque */
          var desde = (HORAS - 1) * 3600, lo = 1e9, hi = -1e9, suma = 0, cnt = 0, onc = 0;
          for(i = 0; i < serie.length; i++){
            if(serie[i][0] < desde) continue;
            lo = Math.min(lo, serie[i][1]); hi = Math.max(hi, serie[i][1]);
            suma += serie[i][1]; cnt++;
            if(serie[i][2]) onc++;
          }
          var conm = 0;
          for(i = 0; i < cambios.length; i++) if(cambios[i] >= desde) conm++;
          /* un ciclo completo son dos conmutaciones (enciende y apaga) */
          return {serie:serie, ciclos:conm / 2, amplitud:hi - lo, media:suma / Math.max(1, cnt),
                  min:lo, max:hi, uso:100 * onc / Math.max(1, cnt)};
        }

        function pinta(){
          var R = simula();
          var X0 = 58, X1 = 672, Y0 = 20, Y1 = 232;
          var lo = Math.min(v.ref - 3, R.min - 0.6), hi = Math.max(v.ref + 3, R.max + 0.6);
          var px = function(s){ return X0 + (X1 - X0) * s / (HORAS * 3600); };
          var py = function(T){ return Y1 - (Y1 - Y0) * (T - lo) / (hi - lo); };
          /* La escala se elige para que se vea el diente de sierra, y el
             calentamiento inicial arranca desde la temperatura de la calle, muy
             por debajo. Se recorta al marco en vez de reescalar: si no, el
             rizado, que es lo que hay que mirar, se quedaria en una raya. */
          var m = '<defs><clipPath id="tn-marco"><rect x="' + X0 + '" y="' + Y0 + '" width="'
                + (X1 - X0) + '" height="' + (Y1 - Y0) + '"/></clipPath></defs>', g;

          /* banda de la histeresis */
          m += '<rect x="' + X0 + '" y="' + py(v.ref + v.h / 2).toFixed(1) + '" width="' + (X1 - X0)
             + '" height="' + Math.max(1, (py(v.ref - v.h / 2) - py(v.ref + v.h / 2))).toFixed(1)
             + '" fill="#1a73e8" opacity=".10"/>';
          for(g = Math.ceil(lo); g <= hi; g++){
            m += '<line x1="' + X0 + '" y1="' + py(g).toFixed(1) + '" x2="' + X1 + '" y2="'
               + py(g).toFixed(1) + '" stroke="currentColor" stroke-width="1" opacity=".11"/>'
               + '<text x="' + (X0 - 6) + '" y="' + (py(g) + 4).toFixed(1)
               + '" class="ejeq" text-anchor="end">' + g + '</text>';
          }
          var hh;
          for(hh = 0; hh <= HORAS * 60; hh += 30){
            m += '<text x="' + px(hh * 60).toFixed(1) + '" y="' + (Y1 + 16)
               + '" class="ejeq" text-anchor="middle">' + hh + '</text>';
          }

          /* consigna */
          m += '<line x1="' + X0 + '" y1="' + py(v.ref).toFixed(1) + '" x2="' + X1 + '" y2="'
             + py(v.ref).toFixed(1) + '" stroke="currentColor" stroke-width="1.5"'
             + ' stroke-dasharray="6 4" opacity=".6"/>'
             + '<text x="' + (X0 + 5) + '" y="' + (py(v.ref) - 6).toFixed(1) + '" class="etq">consigna '
             + n0(v.ref) + ' &deg;C</text>';

          /* la curva: es la integracion, muestreada para no pintar 5.400 puntos */
          var i, d = '', salto = Math.ceil(R.serie.length / 600);
          for(i = 0; i < R.serie.length; i += salto){
            d += (i ? ' L ' : 'M ') + px(R.serie[i][0]).toFixed(1) + ' ' + py(R.serie[i][1]).toFixed(1);
          }
          m += '<path d="' + d + '" fill="none" stroke="#1a73e8" stroke-width="2"'
             + ' clip-path="url(#tn-marco)"/>';
          if(v.ext < lo){
            m += '<text x="' + (X0 + 5) + '" y="' + (Y1 - 7) + '" class="ejeq">la subida arranca '
               + 'desde los ' + n0(v.ext) + ' &deg;C de la calle, por debajo del recuadro</text>';
          }

          /* la barra de encendido/apagado, debajo */
          var yb = 250;
          m += '<text x="' + (X0 - 6) + '" y="' + (yb + 11)
             + '" class="ejeq" text-anchor="end">caldera</text>';
          var j, tr = null;
          for(j = 0; j < R.serie.length; j++){
            if(R.serie[j][2] && tr === null) tr = R.serie[j][0];
            if((!R.serie[j][2] || j === R.serie.length - 1) && tr !== null){
              m += '<rect x="' + px(tr).toFixed(1) + '" y="' + yb + '" width="'
                 + Math.max(0.6, px(R.serie[j][0]) - px(tr)).toFixed(1)
                 + '" height="15" fill="#ea4335" opacity=".75"/>';
              tr = null;
            }
          }
          m += '<rect x="' + X0 + '" y="' + yb + '" width="' + (X1 - X0)
             + '" height="15" fill="none" stroke="currentColor" stroke-width="1" opacity=".3"/>';
          m += '<text x="' + X0 + '" y="' + (Y0 - 6) + '" class="ejeq">grados dentro de la habitaci&oacute;n</text>';
          m += '<text x="' + (X0 + 2) + '" y="' + (yb + 33) + '" class="ejeq">minutos &middot; las '
             + 'medidas del tablero se toman en la &uacute;ltima hora, cuando ya se ha '
             + 'estabilizado</text>';

          svg.innerHTML = m;

          /* ---- el tablero: todo medido sobre la simulacion ---- */
          var vida = R.ciclos > 0 ? 100000 / R.ciclos : 0;
          var cls = R.ciclos > 20 ? ' malo' : (R.ciclos > 0 ? ' bien' : ' malo');
          tab.innerHTML =
            '<div class="tn-dato' + cls + '"><span>ciclos por hora</span><b id="tn-ciclos">'
              + n1(R.ciclos) + '</b></div>'
          + '<div class="tn-dato"><span>oscilaci&oacute;n</span><b id="tn-amp">'
              + n1(R.amplitud) + ' &deg;C</b></div>'
          + '<div class="tn-dato"><span>temperatura media</span><b id="tn-media">'
              + n1(R.media) + ' &deg;C</b></div>'
          + '<div class="tn-dato"><span>tiempo encendida</span><b id="tn-uso">'
              + n0(R.uso) + ' %</b></div>'
          + '<div class="tn-dato"><span>vida del rel&eacute; (100.000 ciclos)</span><b id="tn-vida">'
              + (R.ciclos > 0 ? n0(vida) + ' h' : '&mdash;') + '</b></div>';

          /* la comprobacion de que la cuenta cuadra: en regimen, el tiempo
             encendida tiene que ser el que pide el balance de energia      */
          var teorico = 100 * K * (R.media - v.ext) / v.pot;
          pie.innerHTML =
            '<b>Hist&eacute;resis de ' + n1(v.h) + ' &deg;C:</b> enciende al bajar de '
            + n1(v.ref - v.h / 2) + ' &deg;C y apaga al pasar de ' + n1(v.ref + v.h / 2) + ' &deg;C. '
            + 'La caldera est&aacute; encendida el <b>' + n1(R.uso) + ' %</b> del tiempo, y el balance '
            + 'de energ&iacute;a dice que ten&iacute;a que ser 60 &times; (' + n1(R.media) + ' &minus; '
            + n0(v.ext) + ') / ' + v.pot + ' = <b>' + n1(teorico) + ' %</b>: la simulaci&oacute;n y la '
            + 'cuenta dicen lo mismo, con unas d&eacute;cimas de diferencia porque en la &uacute;ltima '
            + 'hora no cabe un n&uacute;mero entero de ciclos.'
            + (v.h < 0.25 ? ' <b>Con la banda casi a cero</b> el rel&eacute; conmuta a cada paso de '
                          + 'c&aacute;lculo: en un term&oacute;stato de verdad, eso lo funde.' : '')
            + (v.retardo ? ' <b>Con el sensor dentro de la caja</b> la habitaci&oacute;n oscila '
                         + n1(R.amplitud) + ' &deg;C, m&aacute;s que la banda de ' + n1(v.h)
                         + ' &deg;C que hab&iacute;as puesto: cuando el term&oacute;stato se entera, '
                         + 'la habitaci&oacute;n ya se ha pasado.' : '');
        }

        function mando(id, clave, sufijo, escala){
          var r = document.getElementById(id);
          r.addEventListener('input', function(){
            v[clave] = escala ? (+r.value) * escala : (+r.value);
            document.getElementById(id + '-v').innerHTML =
              (escala ? n1(v[clave]) : r.value) + sufijo;
            pinta();
          });
        }
        mando('tn-ref', 'ref', ' &deg;C');
        mando('tn-h', 'h', ' &deg;C', 0.1);
        mando('tn-ext', 'ext', ' &deg;C');
        mando('tn-pot', 'pot', ' W');
        document.getElementById('tn-retardo').addEventListener('change', function(){
          v.retardo = this.checked; pinta();
        });
        caja.addEventListener('click', function(e){
          if(!e.target.closest('[data-a="reset"]')) return;
          v = {ref:21, h:1.0, ext:5, pot:2500, retardo:false};
          document.getElementById('tn-ref').value = 21;
          document.getElementById('tn-h').value = 10;
          document.getElementById('tn-ext').value = 5;
          document.getElementById('tn-pot').value = 2500;
          document.getElementById('tn-retardo').checked = false;
          document.getElementById('tn-ref-v').innerHTML = '21 &deg;C';
          document.getElementById('tn-h-v').innerHTML = '1,0 &deg;C';
          document.getElementById('tn-ext-v').innerHTML = '5 &deg;C';
          document.getElementById('tn-pot-v').innerHTML = '2500 W';
          pinta();
        });

        pinta();
      })();
      </script>
'''


# ==========================================================================
# S4 - Que motor hace falta
# ==========================================================================
MOTOR = u'''
      <div class="escena" id="esc-mt">
        <div class="escena-barra">
          <span class="escena-titulo">Banco de pruebas &middot; &iquest;con este motor y esta reductora, se mueve o no?</span>
          <div class="seg" id="seg-mt">
            <button type="button" data-m="0" aria-pressed="true">Barrera</button>
            <button type="button" data-m="1">Tambor que iza</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 690 310" id="svg-mt" role="img"
               aria-label="Par de engranajes dibujado a escala y el mecanismo que mueven"></svg>
          <div class="mt-mandos">
            <div class="mt-col">
              <div class="mt-fila">
                <label for="mt-motor">Motor</label>
                <select id="mt-motor">
                  <option value="0">Servo SG90 &middot; 1,8 kg&middot;cm &middot; 100 rpm</option>
                  <option value="1" selected>Motorreductor TT 1:48 &middot; 0,8 kg&middot;cm &middot; 200 rpm</option>
                  <option value="2">Motor DC de juguete &middot; 0,02 kg&middot;cm &middot; 9000 rpm</option>
                </select>
              </div>
              <div class="mt-fila">
                <label for="mt-z1">Dientes del pi&ntilde;&oacute;n (z&#8321;)</label>
                <input type="range" id="mt-z1" min="8" max="40" step="1" value="16">
                <span class="val" id="mt-z1-v">16</span>
              </div>
              <div class="mt-fila">
                <label for="mt-z2">Dientes de la corona (z&#8322;)</label>
                <input type="range" id="mt-z2" min="10" max="120" step="1" value="100">
                <span class="val" id="mt-z2-v">100</span>
              </div>
            </div>
            <div class="mt-col">
              <div class="mt-fila">
                <label for="mt-masa" id="mt-masa-l">Masa que hay que mover</label>
                <input type="range" id="mt-masa" min="20" max="2000" step="10" value="150">
                <span class="val" id="mt-masa-v">150 g</span>
              </div>
              <div class="mt-fila">
                <label for="mt-brazo" id="mt-brazo-l">Longitud del list&oacute;n</label>
                <input type="range" id="mt-brazo" min="10" max="120" step="1" value="80">
                <span class="val" id="mt-brazo-v">80 cm</span>
              </div>
              <div class="mt-fila">
                <label for="mt-contra" id="mt-contra-l">Contrapeso a 8 cm del eje</label>
                <input type="range" id="mt-contra" min="0" max="1500" step="10" value="0">
                <span class="val" id="mt-contra-v">0 g</span>
              </div>
            </div>
          </div>
          <div class="mt-tablero" id="mt-tablero"></div>
        </div>
        <div class="pie" id="pie-mt"></div>
      </div>

      <style>
      .mt-mandos{display:flex;gap:18px;flex-wrap:wrap;margin-top:10px}
      .mt-col{flex:1 1 300px;min-width:270px}
      .mt-fila{display:flex;align-items:center;gap:9px;flex-wrap:wrap;margin:0 0 8px;
        font-family:var(--f-m);font-size:12.5px;color:var(--ink)}
      .mt-fila label{min-width:160px}
      .mt-fila input[type="range"]{flex:1 1 110px;min-width:100px;accent-color:var(--goo-azul)}
      .mt-fila select{flex:1 1 200px;font-family:var(--f-m);font-size:12px;padding:5px;
        border:1.5px solid var(--line);border-radius:2px;background:var(--surface);color:var(--ink)}
      .mt-fila .val{font-weight:500;color:var(--goo-azul);min-width:56px;text-align:right}
      .mt-tablero{display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));margin-top:13px}
      .mt-dato{border:1.5px solid var(--line);border-radius:2px;background:var(--surface);padding:9px 11px}
      .mt-dato span{display:block;font-family:var(--f-m);font-size:10.5px;letter-spacing:.06em;
        text-transform:uppercase;color:var(--ink-soft);margin-bottom:3px;line-height:1.4}
      .mt-dato b{font-family:var(--f-m);font-size:17px;font-weight:500;color:var(--ink)}
      .mt-veredicto{margin:12px 0 0;border:2px solid var(--goo-verde);border-radius:2px;padding:11px 13px;
        font-family:var(--f-m);font-size:13px;line-height:1.7;background:var(--surface)}
      .mt-veredicto.no{border-color:var(--goo-rojo)}
      .mt-veredicto.justo{border-color:var(--goo-amarillo)}
      .mt-veredicto b{font-size:14px}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-mt');
        if(!svg) return;
        var caja = document.getElementById('esc-mt');
        var seg  = document.getElementById('seg-mt');
        var pie  = document.getElementById('pie-mt');
        var tab  = document.getElementById('mt-tablero');

        var G = 9.81, KGCM = 0.0980665;       /* 1 kg*cm = 0,0980665 N*m */
        var RTO = 0.90;                        /* rendimiento del par de engranajes */

        function n1(x){ return x.toFixed(1).replace('.', ','); }
        function n2(x){ return x.toFixed(2).replace('.', ','); }
        function n3(x){ return x.toFixed(3).replace('.', ','); }
        function n0(x){ return Math.round(x).toString(); }

        var MOTORES = [
          {nom:'Servo SG90',              par:1.8,  rpm:100,  nota:'a 4,8 V; 60&deg; en 0,1 s'},
          {nom:'Motorreductor TT 1:48',   par:0.8,  rpm:200,  nota:'a 6 V'},
          {nom:'Motor DC de juguete',     par:0.02, rpm:9000, nota:'tipo FA-130, a 3 V, par &uacute;til'}
        ];

        var v = {mec:0, mot:1, z1:16, z2:100, masa:150, brazo:80, contra:0};
        var u = 0, sentido = 1, raf = null, reloj = null;

        /* ---------------- geometria correcta del engranaje ---------------
           Dos ruedas engranan solo si tienen el MISMO modulo. El radio
           primitivo es r = modulo * z / 2, la cabeza del diente sale un
           modulo por fuera y el pie entra 1,25 modulos. La distancia entre
           ejes es r1 + r2, y para que un diente caiga en un hueco la segunda
           rueda va desfasada medio paso.                                   */
        function rueda(cx, cy, z, mod, fase){
          var r = mod * z / 2, ra = r + mod, rf = Math.max(2, r - 1.25 * mod);
          var p = 2 * Math.PI / z, d = '', k;
          for(k = 0; k < z; k++){
            var a = fase + k * p;
            var Pt = function(rad, off){
              return (cx + rad * Math.cos(a + off)).toFixed(2) + ' '
                   + (cy + rad * Math.sin(a + off)).toFixed(2);
            };
            d += (k ? ' L ' : 'M ') + Pt(rf, -0.30 * p)
               + ' L ' + Pt(r,  -0.25 * p)
               + ' L ' + Pt(ra, -0.14 * p)
               + ' L ' + Pt(ra,  0.14 * p)
               + ' L ' + Pt(r,   0.25 * p)
               + ' L ' + Pt(rf,  0.30 * p)
               + ' A ' + rf.toFixed(2) + ' ' + rf.toFixed(2) + ' 0 0 1 ' + Pt(rf, 0.70 * p);
          }
          return d + ' Z';
        }

        /* ---------------- las cuentas ---------------------------------- */
        function calcula(){
          var M = MOTORES[v.mot];
          var i = v.z1 / v.z2;                        /* i = z1/z2 = n2/n1 */
          var n2v = M.rpm * i;                        /* rpm de salida     */
          var parDisp = M.par / i * RTO;              /* kg*cm en la salida*/
          var parNec, detalle, recorrido, unidades, vueltas = 0.25;
          if(v.mec === 0){
            /* listón uniforme que gira sobre un extremo: el peso tira desde
               el centro, asi que el brazo es L/2. El contrapeso resta.     */
            var Nm = (v.masa / 1000) * G * (v.brazo / 100) / 2
                   - (v.contra / 1000) * G * 0.08;
            parNec = Math.max(0, Nm) / KGCM;
            detalle = 'M = m &middot; g &middot; L/2 &minus; m&#8329; &middot; g &middot; d&#8329; = '
                    + n3(v.masa / 1000) + ' &middot; 9,81 &middot; ' + n2(v.brazo / 200)
                    + (v.contra ? (' &minus; ' + n3(v.contra / 1000) + ' &middot; 9,81 &middot; 0,08') : '')
                    + ' = <b>' + n3(Math.max(0, Nm)) + ' N&middot;m</b>';
            recorrido = 90 / (6 * n2v);               /* 90 grados, a 6*rpm grados/s */
            unidades = 'en subir la barrera 90&deg;';
          } else {
            /* tambor de radio r que iza una masa: M = m*g*r.
               El mando entrega decimas de milimetro por comodidad: 150 -> 15,0 mm */
            var r = v.brazo / 10 / 1000;              /* decimas de mm -> metros */
            var Nm2 = (v.masa / 1000) * G * r;
            parNec = Nm2 / KGCM;
            detalle = 'M = m &middot; g &middot; r = ' + n3(v.masa / 1000) + ' &middot; 9,81 &middot; '
                    + n3(r) + ' = <b>' + n3(Nm2) + ' N&middot;m</b>';
            /* subir 30 cm: vueltas = 0,30 / (2*pi*r) */
            vueltas = 0.30 / (2 * Math.PI * r);
            recorrido = n2v > 0 ? vueltas / n2v * 60 : 0;
            unidades = 'en izar 30 cm';
          }
          var pot = parDisp * KGCM * 2 * Math.PI * n2v / 60;   /* W en la salida */
          return {M:M, i:i, n2:n2v, parDisp:parDisp, parNec:parNec, detalle:detalle,
                  recorrido:recorrido, unidades:unidades, pot:pot, vueltas:vueltas,
                  margen: parNec > 0 ? parDisp / parNec : 99};
        }

        function pinta(){
          var R = calcula();
          var m = '';

          /* ---- posicion del mecanismo y, DE AHI, la de las dos ruedas ----
             El eje de salida es el que manda: la barrera recorre 90 grados y
             el tambor da las vueltas que salen de la cuenta. El pinon gira lo
             que le toca por la relacion, th1 = -th2 / i, y la corona engrana
             con el desfase de medio paso.                                   */
          var th2 = (v.mec === 0) ? u * Math.PI / 2 : u * R.vueltas * 2 * Math.PI;
          var th1 = -th2 / R.i;

          /* ---- el par de engranajes, a escala ---- */
          var WD = 366, HD = 226, X0 = 12, Y0 = 18;
          var mod = Math.min(WD / (v.z1 + v.z2 + 2), HD / (Math.max(v.z1, v.z2) + 2));
          var r1 = mod * v.z1 / 2, r2 = mod * v.z2 / 2;
          var total = mod * (v.z1 + v.z2 + 2);
          var cx1 = X0 + (WD - total) / 2 + r1 + mod;
          var cx2 = cx1 + r1 + r2;
          var cy  = Y0 + HD / 2;
          var p2 = 2 * Math.PI / v.z2;
          m += '<path d="' + rueda(cx1, cy, v.z1, mod, th1)
             + '" fill="var(--accent-soft)" stroke="#1a73e8" stroke-width="1.6"/>'
             + '<circle cx="' + cx1.toFixed(1) + '" cy="' + cy.toFixed(1) + '" r="'
             + Math.max(3, r1 * 0.22).toFixed(1) + '" fill="var(--surface)" stroke="#1a73e8" stroke-width="1.6"/>';
          m += '<path d="' + rueda(cx2, cy, v.z2, mod, Math.PI + p2 / 2 + th2)
             + '" fill="var(--surface-2)" stroke="currentColor" stroke-width="1.6"/>'
             + '<circle cx="' + cx2.toFixed(1) + '" cy="' + cy.toFixed(1) + '" r="'
             + Math.max(3, r2 * 0.18).toFixed(1) + '" fill="var(--surface)" stroke="currentColor" stroke-width="1.6"/>';
          /* Los rotulos van en una franja debajo de las ruedas: encima se los
             comia la corona en cuanto z2 subia un poco. */
          m += '<text x="' + (X0 + 2) + '" y="270" class="etq" style="fill:#1a73e8">z&#8321; = '
             + v.z1 + ' (motor)</text>'
             + '<text x="' + (X0 + 118) + '" y="270" class="etq">z&#8322; = ' + v.z2
             + ' (salida)</text>'
             + '<text x="' + (X0 + 2) + '" y="288" class="ejeq">mismo m&oacute;dulo &middot; '
             + 'r = m&oacute;dulo &middot; z / 2 &middot; ejes a r&#8321; + r&#8322;</text>';

          /* ---- el mecanismo ---- */
          var MX = 400, MW = 278;
          m += '<line x1="' + MX + '" y1="26" x2="' + MX + '" y2="286" stroke="currentColor"'
             + ' stroke-width="1" opacity=".2"/>';
          if(v.mec === 0){
            /* barrera: el liston gira sobre su eje, entre 0 y 90 grados */
            var ang = -th2;
            var ex = MX + 44, ey = 232;
            var L = 8 + v.brazo * 1.55;
            m += '<rect x="' + (MX + 16) + '" y="232" width="56" height="42" fill="var(--surface-2)"'
               + ' stroke="currentColor" stroke-width="1.4"/>'
               + '<line x1="' + (MX + 10) + '" y1="274" x2="' + (MX + MW) + '" y2="274"'
               + ' stroke="currentColor" stroke-width="2" opacity=".5"/>';
            m += '<line x1="' + ex + '" y1="' + ey + '" x2="' + (ex + L * Math.cos(ang)).toFixed(1)
               + '" y2="' + (ey + L * Math.sin(ang)).toFixed(1)
               + '" stroke="#ea4335" stroke-width="7" stroke-linecap="round"/>'
               + '<circle cx="' + ex + '" cy="' + ey + '" r="6" fill="var(--surface)"'
               + ' stroke="currentColor" stroke-width="2"/>';
            if(v.contra > 0){
              m += '<circle cx="' + (ex - 22 * Math.cos(ang)).toFixed(1) + '" cy="'
                 + (ey - 22 * Math.sin(ang)).toFixed(1) + '" r="'
                 + (4 + Math.sqrt(v.contra) / 6).toFixed(1) + '" fill="#fbbc04" stroke="currentColor"'
                 + ' stroke-width="1.4"/>';
            }
            m += '<text x="' + (MX + 12) + '" y="18" class="ejeq">barrera de ' + v.brazo
               + ' cm &middot; ' + v.masa + ' g</text>';
          } else {
            /* tambor que iza: radio a escala, la carga sube de verdad */
            var rmm = v.brazo / 10;                  /* mm */
            var rp = Math.max(9, rmm * 2.6);
            var tx = MX + 100, ty = 84;
            var subida = u * 92;
            m += '<line x1="' + (MX + 10) + '" y1="52" x2="' + (MX + MW) + '" y2="52"'
               + ' stroke="currentColor" stroke-width="3" opacity=".5"/>';
            m += '<circle cx="' + tx + '" cy="' + ty + '" r="' + rp.toFixed(1)
               + '" fill="var(--accent-soft)" stroke="#1a73e8" stroke-width="2"/>'
               + '<circle cx="' + tx + '" cy="' + ty + '" r="3" fill="#1a73e8"/>'
               + '<line x1="' + tx + '" y1="' + (ty - rp).toFixed(1) + '" x2="' + tx + '" y2="52"'
               + ' stroke="currentColor" stroke-width="1.4" opacity=".6"/>';
            var lado = 16 + Math.sqrt(v.masa) * 0.9;
            var cyy = 250 - subida;
            m += '<line x1="' + (tx + rp).toFixed(1) + '" y1="' + ty + '" x2="'
               + (tx + rp).toFixed(1) + '" y2="' + cyy.toFixed(1)
               + '" stroke="currentColor" stroke-width="1.6"/>'
               + '<rect x="' + (tx + rp - lado / 2).toFixed(1) + '" y="' + cyy.toFixed(1)
               + '" width="' + lado.toFixed(1) + '" height="' + lado.toFixed(1)
               + '" fill="#ea4335" opacity=".85" stroke="currentColor" stroke-width="1.2"/>'
               + '<text x="' + (tx + rp).toFixed(1) + '" y="' + (cyy + lado / 2 + 4).toFixed(1)
               + '" class="etq" text-anchor="middle" style="fill:#fff">' + v.masa + ' g</text>';
            m += '<text x="' + (MX + 12) + '" y="18" class="ejeq">tambor de r = ' + n1(rmm)
               + ' mm &middot; carga de ' + v.masa + ' g</text>';
          }

          svg.innerHTML = m;

          /* ---- el tablero ---- */
          tab.innerHTML =
            '<div class="mt-dato"><span>relaci&oacute;n i = z&#8321;/z&#8322;</span><b id="mt-i">'
              + n3(R.i) + '</b></div>'
          + '<div class="mt-dato"><span>vueltas en la salida</span><b id="mt-rpm">'
              + n1(R.n2) + ' rpm</b></div>'
          + '<div class="mt-dato"><span>par que hace falta</span><b id="mt-nec">'
              + n2(R.parNec) + ' kg&middot;cm</b></div>'
          + '<div class="mt-dato"><span>par disponible</span><b id="mt-disp">'
              + n2(R.parDisp) + ' kg&middot;cm</b></div>'
          + '<div class="mt-dato"><span>tarda ' + R.unidades + '</span><b id="mt-t">'
              + (R.n2 > 0 ? n1(R.recorrido) + ' s' : '&mdash;') + '</b></div>'
          + '<div class="mt-dato"><span>potencia en la salida</span><b id="mt-pot">'
              + n2(R.pot) + ' W</b></div>';

          var clase = R.margen >= 2 ? '' : (R.margen >= 1 ? ' justo' : ' no');
          var frase = R.margen >= 2
            ? 'Sirve, y con margen: el par disponible es <b>' + n1(R.margen)
              + ' veces</b> el que hace falta.'
            : (R.margen >= 1
              ? 'Se mueve, pero va justo: solo <b>' + n1(R.margen) + ' veces</b> el par necesario. '
                + 'Con el rozamiento real y el arranque, es probable que se plante.'
              : '<b>No se mueve.</b> El par disponible es solo <b>' + n1(R.margen)
                + ' veces</b> el necesario: el motor se quedar&aacute; zumbando y calent&aacute;ndose.');

          pie.innerHTML =
            '<div class="mt-veredicto' + clase + '" id="mt-veredicto">'
            + '<b>' + R.M.nom + '</b> (' + R.M.nota + ')<br>'
            + 'Par necesario: ' + R.detalle + ' = <b>' + n2(R.parNec) + ' kg&middot;cm</b> '
            + '(dividiendo entre 0,0981)<br>'
            + 'Par disponible: M&#8322; = M&#8321; / i &middot; &eta; = ' + n2(R.M.par) + ' / '
            + n3(R.i) + ' &middot; 0,90 = <b>' + n2(R.parDisp) + ' kg&middot;cm</b><br>'
            + 'Velocidad: n&#8322; = n&#8321; &middot; i = ' + R.M.rpm + ' &middot; ' + n3(R.i)
            + ' = <b>' + n1(R.n2) + ' rpm</b><br>'
            + frase
            + (R.recorrido > 0 && R.recorrido < 3
               ? '<br><i>El dibujo va m&aacute;s lento que la realidad: la maniobra de verdad dura '
                 + n1(R.recorrido) + ' s y en pantalla se alarga a 3 s para poder verla.</i>'
               : '')
            + '</div>';
        }

        /* El dibujo se mueve al ritmo que dice la cuenta: la maniobra completa
           tarda en pantalla los segundos calculados. Si sale tan rapida que no
           se ve (menos de 3 s), se alarga a 3 s y el pie lo dice. */
        function cuadro(ahora){
          if(reloj === null) reloj = ahora;
          var dt = Math.min(0.1, (ahora - reloj) / 1000);
          reloj = ahora;
          var R = calcula();
          var T = Math.max(3, R.recorrido);
          if(T > 0 && isFinite(T)){
            u += sentido * dt / T;
            if(u >= 1){ u = 1; sentido = -1; }
            if(u <= 0){ u = 0; sentido = 1; }
          }
          pinta();
          raf = requestAnimationFrame(cuadro);
        }

        function mando(id, clave, sufijo, f){
          var r = document.getElementById(id);
          r.addEventListener('input', function(){
            v[clave] = +r.value;
            document.getElementById(id + '-v').innerHTML = (f ? f(+r.value) : r.value) + sufijo;
            pinta();
          });
        }
        mando('mt-z1', 'z1', '');
        mando('mt-z2', 'z2', '');
        mando('mt-masa', 'masa', ' g');
        mando('mt-contra', 'contra', ' g');
        document.getElementById('mt-brazo').addEventListener('input', function(){
          v.brazo = +this.value;
          document.getElementById('mt-brazo-v').innerHTML =
            v.mec === 0 ? (v.brazo + ' cm') : (n1(v.brazo / 10) + ' mm');
          pinta();
        });
        document.getElementById('mt-motor').addEventListener('change', function(){
          v.mot = +this.value; pinta();
        });

        seg.addEventListener('click', function(ev){
          var b = ev.target.closest('button[data-m]');
          if(!b) return;
          seg.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          v.mec = +b.dataset.m;
          var br = document.getElementById('mt-brazo');
          if(v.mec === 0){
            br.min = 10; br.max = 120; br.value = 80; v.brazo = 80;
            document.getElementById('mt-brazo-l').innerHTML = 'Longitud del list&oacute;n';
            document.getElementById('mt-brazo-v').innerHTML = '80 cm';
            document.getElementById('mt-masa-l').innerHTML = 'Masa del list&oacute;n';
            document.getElementById('mt-contra-l').innerHTML = 'Contrapeso a 8 cm del eje';
            document.getElementById('mt-contra').disabled = false;
          } else {
            br.min = 50; br.max = 400; br.value = 150; v.brazo = 150;
            document.getElementById('mt-brazo-l').innerHTML = 'Radio del tambor';
            document.getElementById('mt-brazo-v').innerHTML = '15,0 mm';
            document.getElementById('mt-masa-l').innerHTML = 'Masa que se iza';
            document.getElementById('mt-contra-l').innerHTML = 'Contrapeso (aqu&iacute; no aplica)';
            document.getElementById('mt-contra').disabled = true;
            v.contra = 0;
            document.getElementById('mt-contra').value = 0;
            document.getElementById('mt-contra-v').innerHTML = '0 g';
          }
          pinta();
        });

        pinta();
        raf = requestAnimationFrame(cuadro);
      })();
      </script>
'''
