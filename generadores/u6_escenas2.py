# -*- coding: utf-8 -*-
"""Las tres escenas interactivas de las sesiones 4, 5 y 6 de la U6.

Van aparte de u6_build.py por el mismo motivo que las tres primeras: son largas
y comparten la biblioteca de simbolos normalizados window.U6, que emite
u6_escenas.py una sola vez en la pagina (SIMBOLOS, en la sesion 1). Aqui no se
dibuja ningun simbolo nuevo a mano: la resistencia sigue siendo un rectangulo.

Las tres calculan de verdad. Ningun numero de los que salen en pantalla esta
escrito a mano: todos salen de una cuenta que se puede repetir en la libreta.
Los DATOS de partida si estan escritos (potencias tipicas de los aparatos,
tensiones tipicas de cada color de LED, precio del kWh), y en cada caso se dice
de donde salen y que hay que mirar para tener el valor real.

Ninguna de estas cadenas pasa por formateo %% de Python: se concatenan tal cual,
asi que los % literales del JavaScript estan a salvo.
"""

# --------------------------------------------------------------------------
# Escena 4 - la regleta: potencias que se suman, corriente que se dispara
# --------------------------------------------------------------------------
# Las potencias son TIPICAS y estan rotuladas como tales en la propia escena.
# Lo que se calcula: I = P / 230 de cada aparato y del conjunto, la energia en
# kWh, el coste y los gramos de CO2. Los dos limites -16 A de la base de
# enchufe y la potencia contratada- se comparan contra la suma calculada.
ESC_REGLETA = u'''
      <style>
        #esc-regleta .ctrl{display:flex;flex-wrap:wrap;gap:14px;align-items:center}
        #esc-regleta .ctrl label{font:400 11.5px var(--f-m);color:var(--ink-soft);
          display:flex;align-items:center;gap:7px}
        #esc-regleta .ctrl input[type=range]{width:104px;accent-color:var(--goo-azul)}
        #esc-regleta .ctrl b{font:500 12px var(--f-m);color:var(--ink);min-width:62px;display:inline-block}
        #esc-regleta .tabla{width:100%;border-collapse:collapse;font:400 13px var(--f-m);margin-top:8px}
        #esc-regleta .tabla td{padding:4px 8px 4px 0;border-bottom:1px solid var(--line-soft);color:var(--ink-soft)}
        #esc-regleta .tabla td:last-child{text-align:right;color:var(--ink);font-weight:500}
        #esc-regleta [data-a]{cursor:pointer}
      </style>
      <div class="escena" id="esc-regleta">
        <div class="escena-barra">
          <span class="escena-titulo">La regleta &middot; enchufa aparatos y mira la corriente</span>
          <div class="seg" id="seg-regleta">
            <button type="button" data-p="2.3" aria-pressed="false">2,3 kW</button>
            <button type="button" data-p="3.45" aria-pressed="true">3,45 kW</button>
            <button type="button" data-p="4.6" aria-pressed="false">4,6 kW</button>
            <button type="button" data-p="5.75" aria-pressed="false">5,75 kW</button>
            <button type="button" data-p="nada">Desenchufar todo</button>
          </div>
        </div>
        <div class="escena-barra">
          <span class="escena-titulo">potencia contratada &#8593;</span>
          <div class="ctrl">
            <label>Horas encendido
              <input type="range" id="reg-h" min="0.5" max="8" step="0.5" value="2"
                     aria-label="Horas que est&aacute;n encendidos los aparatos">
              <b id="reg-ht">2 h</b></label>
            <label>Precio del kWh
              <input type="range" id="reg-p" min="0.05" max="0.45" step="0.01" value="0.27"
                     aria-label="Precio del kilovatio hora en euros">
              <b id="reg-pt">0,27 &euro;</b></label>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 300" id="svg-regleta" role="img"
               aria-label="Ocho aparatos que se pueden enchufar a una regleta, con la corriente de cada uno y un indicador de la corriente total"></svg>
        </div>
        <div class="pie" id="pie-regleta"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-regleta');
        if(!svg || !window.U6) return;
        var S = window.U6, pie = document.getElementById('pie-regleta');
        var seg = document.getElementById('seg-regleta');
        var sH = document.getElementById('reg-h'), sP = document.getElementById('reg-p');
        var tH = document.getElementById('reg-ht'), tP = document.getElementById('reg-pt');

        /* Datos de partida. Las potencias son TIPICAS: la de verdad esta en la
           placa de caracteristicas de cada aparato.                           */
        var AP = [
          {n: 'Cargador m\\u00f3vil', w: 5},
          {n: 'Bombilla LED',        w: 9},
          {n: 'Port\\u00e1til',       w: 45},
          {n: 'Televisor',           w: 100},
          {n: 'Consola',             w: 150},
          {n: 'Microondas',          w: 1000},
          {n: 'Secador de pelo',     w: 2000},
          {n: 'Estufa',              w: 2000}
        ];
        var V = 230;          /* tension de la red en Espana */
        var IBASE = 16;       /* una base de enchufe normal es de 16 A */
        var GCO2 = 258;       /* g de CO2eq por kWh: mix electrico espanol 2025 */
        var IESC = 25;        /* fondo de escala del indicador, en amperios */

        var on = [false, false, false, false, false, false, false, false];
        var contratada = 3.45;   /* kW */

        function coma(x, d){ return x.toFixed(d).replace('.', ','); }

        /* ---- las cuentas: nada de esto esta escrito a mano --------------- */
        function calcula(){
          var P = 0;
          for(var i = 0; i < AP.length; i++) if(on[i]) P += AP[i].w;
          var I = P / V;
          var h = parseFloat(sH.value), precio = parseFloat(sP.value);
          var salta = P > contratada * 1000;
          var kWh = salta ? 0 : P / 1000 * h;
          return {P: P, I: I, h: h, precio: precio, salta: salta,
                  caliente: !salta && I > IBASE,
                  kWh: kWh, euros: kWh * precio, co2: kWh * GCO2,
                  Icontrat: contratada * 1000 / V};
        }

        /* ---- geometria: columna de aparatos a la izquierda --------------- */
        var FX = 18, FW = 274, FY0 = 54, FPASO = 29;

        function fila(i, c){
          var y = FY0 + i * FPASO, a = AP[i], enc = on[i] && !c.salta;
          var col = on[i] ? (c.salta ? 'var(--goo-rojo)' : 'var(--ink)') : 'var(--ink-soft)';
          var m = '<rect x="' + FX + '" y="' + (y - 13) + '" width="' + FW + '" height="26" rx="2"'
                + ' fill="' + (on[i] ? 'var(--surface-2)' : 'none') + '" stroke="var(--line-soft)"'
                + ' stroke-width="1"></rect>';
          /* casilla de enchufado */
          m += '<rect x="' + (FX + 8) + '" y="' + (y - 7) + '" width="14" height="14" rx="2" fill="'
             + (on[i] ? 'var(--goo-verde)' : 'var(--surface)') + '" stroke="' + col
             + '" stroke-width="1.6"></rect>';
          if(on[i]){
            m += S.trazo('M' + (FX + 11) + ' ' + y + ' L' + (FX + 14) + ' ' + (y + 4)
                       + ' L' + (FX + 19) + ' ' + (y - 4), '#fff', 2);
          }
          m += S.texto(FX + 30, y + 4, a.n, ' style="font-size:11.5px;fill:' + col + '"');
          m += S.texto(FX + 205, y + 4, a.w + ' W',
                       ' text-anchor="end" style="font-size:11.5px;fill:' + col + '"');
          /* la corriente de cada aparato, calculada */
          m += S.texto(FX + FW - 8, y + 4, coma(a.w / V, 2) + ' A',
                       ' text-anchor="end" style="font-size:11.5px;fill:'
                       + (enc ? 'var(--goo-azul)' : 'var(--ink-soft)') + '"');
          /* La zona de clic es tambien la de teclado: con el tabulador se
             recorren los ocho aparatos y se enchufan con Intro o espacio.   */
          m += '<rect x="' + FX + '" y="' + (y - 13) + '" width="' + FW + '" height="26"'
             + ' fill="#000" fill-opacity="0" pointer-events="all" data-a="' + i + '"'
             + ' tabindex="0" role="switch" aria-checked="' + (on[i] ? 'true' : 'false')
             + '" aria-label="' + a.n + ', ' + a.w + ' vatios"></rect>';
          return m;
        }

        /* ---- la regleta, arriba a la derecha ----------------------------- */
        var RX = 336, RW = 268, RY = 72, RH = 42;

        function regleta(c){
          var col = c.salta ? 'var(--goo-rojo)' : (c.caliente ? 'var(--goo-amarillo)' : 'var(--ink)');
          var m = '<rect x="' + RX + '" y="' + RY + '" width="' + RW + '" height="' + RH
                + '" rx="6" fill="var(--surface)" stroke="' + col + '" stroke-width="2.4"></rect>';
          /* ocho tomas repartidas con paso constante dentro de la regleta */
          var paso = RW / AP.length, r = 11;
          for(var i = 0; i < AP.length; i++){
            var cx = RX + paso * (i + 0.5), cy = RY + RH / 2;
            var vivo = on[i] && !c.salta;
            m += '<circle cx="' + cx.toFixed(1) + '" cy="' + cy + '" r="' + r + '" fill="'
               + (vivo ? 'var(--goo-verde)' : 'var(--surface-2)') + '" fill-opacity="'
               + (vivo ? '.85' : '1') + '" stroke="' + col + '" stroke-width="1.6"></circle>';
            m += '<circle cx="' + (cx - 4).toFixed(1) + '" cy="' + cy + '" r="1.8" fill="'
               + (vivo ? '#fff' : 'var(--ink-soft)') + '"></circle>';
            m += '<circle cx="' + (cx + 4).toFixed(1) + '" cy="' + cy + '" r="1.8" fill="'
               + (vivo ? '#fff' : 'var(--ink-soft)') + '"></circle>';
            m += '<rect x="' + (cx - 13) + '" y="' + (RY + 3) + '" width="26" height="' + (RH - 6)
               + '" fill="#000" fill-opacity="0" pointer-events="all" data-a="' + i + '"></rect>';
          }
          /* El cable que la alimenta, hasta la base de la pared: por el pasa
             TODA la corriente sumada, y por eso se dibuja mas gordo cuando se
             calienta. Un cable no se deja acabado en el aire.                */
          var xc = RX - 18, yb = RY + RH + 32;
          m += S.trazo('M' + RX + ' ' + (RY + RH / 2) + ' L' + xc + ' ' + (RY + RH / 2)
                     + ' L' + xc + ' ' + yb, col, c.caliente ? 4.5 : 3);
          m += '<rect x="' + (xc - 12) + '" y="' + yb + '" width="24" height="20" rx="3"'
             + ' fill="var(--surface-2)" stroke="' + col + '" stroke-width="1.6"></rect>';
          m += '<circle cx="' + (xc - 5) + '" cy="' + (yb + 10) + '" r="2" fill="' + col + '"></circle>';
          m += '<circle cx="' + (xc + 5) + '" cy="' + (yb + 10) + '" r="2" fill="' + col + '"></circle>';
          m += S.texto(RX, RY + RH + 22, 'por aqu\\u00ed pasa la suma de todas las corrientes',
                       ' style="font-size:10px;fill:' + col + '"');
          return m;
        }

        /* ---- el indicador de corriente, abajo a la derecha --------------- */
        var GX = 346, GW = 258, GY = 214, GH = 15;

        function indicador(c){
          var m = '<rect x="' + GX + '" y="' + GY + '" width="' + GW + '" height="' + GH
                + '" fill="var(--surface-2)" stroke="var(--line)" stroke-width="1.2"></rect>';
          var f = Math.min(c.I, IESC) / IESC;
          var col = c.salta ? 'var(--goo-rojo)'
                  : (c.caliente ? 'var(--goo-amarillo)' : 'var(--goo-verde)');
          m += '<rect x="' + GX + '" y="' + GY + '" width="' + (GW * f).toFixed(1) + '" height="'
             + GH + '" fill="' + col + '"></rect>';
          /* marca de los 16 A de la base y de la potencia contratada */
          function marca(I, etq, c2, arriba){
            var x = GX + Math.min(I, IESC) / IESC * GW;
            var s = S.cable(x, GY - (arriba ? 9 : 0), x, GY + GH + (arriba ? 0 : 9), c2, 1.8);
            /* el rotulo se centra en la marca, pero sin salirse del lienzo */
            var xt = Math.max(GX + 46, Math.min(x, GX + GW - 46));
            s += S.texto(xt, arriba ? GY - 13 : GY + GH + 21, etq,
                         ' text-anchor="middle" style="font-size:9.5px;fill:' + c2 + '"');
            return s;
          }
          m += marca(IBASE, '16 A \\u00b7 la base', 'var(--goo-rojo)', true);
          m += marca(c.Icontrat, coma(c.Icontrat, 1) + ' A \\u00b7 lo contratado',
                     'var(--goo-azul)', false);
          m += S.texto(GX, GY - 13, '0', ' style="font-size:9.5px"');
          m += S.texto(GX + GW, GY - 13, IESC + ' A', ' text-anchor="end" style="font-size:9.5px"');
          return m;
        }

        function pinta(){
          var c = calcula(), m = '';
          for(var i = 0; i < AP.length; i++) m += fila(i, c);
          m += S.texto(FX, 34, 'APARATOS \\u00b7 potencia t\\u00edpica \\u00b7 I = P / 230',
                       ' style="font-size:10.5px;letter-spacing:.1em"');
          m += regleta(c);
          m += indicador(c);

          /* la cuenta, escrita con los numeros de este momento */
          m += S.texto(RX, 158, 'P = ' + c.P + ' W',
                       ' style="font-size:15px;fill:var(--ink)"');
          m += S.texto(RX, 180, 'I = P / V = ' + c.P + ' / 230 = ' + coma(c.I, 2) + ' A',
                       ' style="font-size:13px;fill:var(--goo-azul)"');

          var etq, ecol;
          if(c.salta){ etq = 'SALTA EL AUTOM\\u00c1TICO'; ecol = 'var(--goo-rojo)'; }
          else if(c.caliente){ etq = 'LA BASE, PASADA DE VUELTAS'; ecol = 'var(--goo-amarillo)'; }
          else if(c.P === 0){ etq = 'NADA ENCHUFADO'; ecol = 'var(--ink-soft)'; }
          else { etq = 'TODO EN ORDEN'; ecol = 'var(--goo-verde)'; }
          m += S.texto(RX, 34, etq,
                       ' style="font-size:13px;letter-spacing:.12em;fill:' + ecol + '"');

          svg.innerHTML = m;
          tH.innerHTML = coma(c.h, 1).replace(',0', '') + ' h';
          tP.innerHTML = coma(c.precio, 2) + ' &euro;';
          pinta_pie(c);
          seg.querySelectorAll('button[data-p]').forEach(function(b){
            if(b.dataset.p !== 'nada')
              b.setAttribute('aria-pressed',
                             parseFloat(b.dataset.p) === contratada ? 'true' : 'false');
          });
        }

        function f2(a, b){ return '<tr><td>' + a + '</td><td>' + b + '</td></tr>'; }

        function pinta_pie(c){
          var t;
          if(c.P === 0){
            t = '<b>No has enchufado nada.</b> Enchufa aparatos y mira dos cosas: lo que suman '
              + 'las potencias y lo que suman las corrientes. Est&aacute;n todos <b>en paralelo</b>, '
              + 'as&iacute; que todos reciben los mismos 230 V y sus corrientes se suman &mdash; lo que '
              + 'viste en la sesi&oacute;n anterior, ahora con la factura delante.';
          } else if(c.salta){
            t = '<b>Salta el autom&aacute;tico.</b> Has pedido ' + c.P + ' W y tienes contratados '
              + coma(contratada * 1000, 0) + ' W. El interruptor de control abre el circuito y te '
              + 'quedas sin luz en toda la casa: no es una aver&iacute;a, es lo que has contratado. '
              + 'Apaga algo o contrata m&aacute;s potencia &mdash; y contratar m&aacute;s potencia se paga '
              + '<b>todos los d&iacute;as del mes</b>, la uses o no.';
          } else if(c.caliente){
            t = '<b>' + coma(c.I, 2) + ' A por un cable pensado para 16 A.</b> No salta nada: '
              + 'la potencia contratada te llega. Lo que pasa es que toda esa corriente atraviesa '
              + 'el <b>&uacute;nico cable</b> de la regleta, que se calienta. As&iacute; es como empiezan los '
              + 'incendios por regleta: no por un cortocircuito, sino por sumar aparatos grandes '
              + 'en una sola toma.';
          } else {
            t = '<b>Todo en orden.</b> ' + coma(c.I, 2) + ' A por el cable de la regleta, por '
              + 'debajo de los 16 A de la base, y ' + c.P + ' W por debajo de los '
              + coma(contratada * 1000, 0) + ' W contratados.';
          }
          var f = '<table class="tabla">';
          f += f2('Potencia total &nbsp;<i>P = suma de las potencias</i>', c.P + ' W');
          f += f2('Corriente por el cable &nbsp;<i>I = P / V</i>', coma(c.I, 2) + ' A');
          f += f2('Energ&iacute;a en ' + coma(c.h, 1).replace(',0', '') + ' h &nbsp;<i>E = P &times; t</i>',
                  coma(c.kWh, 3) + ' kWh');
          f += f2('Lo que cuesta &nbsp;<i>E &times; precio</i>', coma(c.euros, 2) + ' &euro;');
          f += f2('CO&#8322; que ha costado &nbsp;<i>E &times; 258 g/kWh</i>',
                  (c.co2 >= 1000 ? coma(c.co2 / 1000, 2) + ' kg' : Math.round(c.co2) + ' g'));
          f += '</table>';
          pie.innerHTML = t + f;
        }

        function conmuta(t){
          var i = parseInt(t.dataset.a, 10);
          on[i] = !on[i];
          pinta();
          /* Al repintar desaparece el elemento que tenia el foco: se le
             devuelve al mismo aparato para poder seguir con el tabulador.   */
          var nuevo = svg.querySelector('[data-a="' + i + '"][tabindex]');
          if(nuevo && nuevo.focus) nuevo.focus();
        }
        svg.addEventListener('click', function(e){
          var t = e.target.closest('[data-a]');
          if(t) conmuta(t);
        });
        svg.addEventListener('keydown', function(e){
          if(e.key !== ' ' && e.key !== 'Enter') return;
          var t = e.target.closest ? e.target.closest('[data-a]') : null;
          if(!t) return;
          e.preventDefault();
          conmuta(t);
        });
        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-p]');
          if(!b) return;
          if(b.dataset.p === 'nada') on = on.map(function(){ return false; });
          else contratada = parseFloat(b.dataset.p);
          pinta();
        });
        sH.addEventListener('input', pinta);
        sP.addEventListener('input', pinta);
        pinta();
      })();
      </script>
'''


# --------------------------------------------------------------------------
# Escena 5 - el LED y su resistencia limitadora
# --------------------------------------------------------------------------
# Calcula R = (Vs - Vf) / I, busca el valor E12 que existe de verdad y vuelve a
# calcular la corriente REAL con ese valor. El pulsador de la escena se
# comporta como un pulsador: alumbra mientras se tiene apretado.
ESC_LED = u'''
      <style>
        #esc-led .ctrl{display:flex;flex-wrap:wrap;gap:12px;align-items:center}
        #esc-led .ctrl label{font:400 11.5px var(--f-m);color:var(--ink-soft);
          display:flex;align-items:center;gap:7px}
        #esc-led .ctrl input[type=range]{width:116px;accent-color:var(--goo-azul)}
        #esc-led .ctrl b{font:500 12px var(--f-m);color:var(--ink);min-width:56px;display:inline-block}
        #esc-led .tabla{width:100%;border-collapse:collapse;font:400 13px var(--f-m);margin-top:8px}
        #esc-led .tabla td{padding:4px 8px 4px 0;border-bottom:1px solid var(--line-soft);color:var(--ink-soft)}
        #esc-led .tabla td:last-child{text-align:right;color:var(--ink);font-weight:500}
        #esc-led [data-clic]{cursor:pointer}
      </style>
      <div class="escena" id="esc-led">
        <div class="escena-barra">
          <span class="escena-titulo">Banco del LED &middot; calcula su resistencia</span>
          <div class="seg" id="seg-led-f">
            <button type="button" data-f="0" aria-pressed="true">micro:bit 3 V</button>
            <button type="button" data-f="1" aria-pressed="false">Pila 4,5 V</button>
            <button type="button" data-f="2" aria-pressed="false">USB 5 V</button>
            <button type="button" data-f="3" aria-pressed="false">Pila 9 V</button>
          </div>
        </div>
        <div class="escena-barra">
          <div class="seg" id="seg-led-c">
            <button type="button" data-c="0" aria-pressed="true">Rojo</button>
            <button type="button" data-c="1" aria-pressed="false">Amarillo</button>
            <button type="button" data-c="2" aria-pressed="false">Verde</button>
            <button type="button" data-c="3" aria-pressed="false">Azul</button>
            <button type="button" data-c="4" aria-pressed="false">Blanco</button>
          </div>
          <div class="ctrl">
            <label>Corriente que quieres
              <input type="range" id="led-i" min="2" max="20" step="1" value="5"
                     aria-label="Corriente que quieres que pase por el LED, en miliamperios">
              <b id="led-it">5 mA</b></label>
          </div>
        </div>
        <div class="escena-barra">
          <div class="seg" id="seg-led-m">
            <button type="button" data-m="pulsador" aria-pressed="true">Pulsador</button>
            <button type="button" data-m="interruptor" aria-pressed="false">Interruptor</button>
            <button type="button" data-m="sinr" aria-pressed="false">Quitar la resistencia</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 300" id="svg-led" role="img"
               aria-label="Circuito con una fuente, un pulsador, un LED y su resistencia limitadora, y la escala de valores de resistencia que existen en el comercio"></svg>
        </div>
        <div class="pie" id="pie-led"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-led');
        if(!svg || !window.U6) return;
        var S = window.U6, pie = document.getElementById('pie-led');
        var segF = document.getElementById('seg-led-f'), segC = document.getElementById('seg-led-c');
        var segM = document.getElementById('seg-led-m');
        var sI = document.getElementById('led-i'), tI = document.getElementById('led-it');

        /* Datos de partida. Las tensiones directas son TIPICAS de cada color:
           la del LED que tengas en la mano esta en su hoja de caracteristicas. */
        /* El nombre se rotula a la izquierda de la fuente y se sale del lienzo
           si es largo: por eso van cortos.                                   */
        var FUENTES = [
          {n: 'micro:bit P0', v: 3,   celdas: 0, tope: 5},
          {n: 'Pila petaca',  v: 4.5, celdas: 3, tope: 0},
          {n: 'USB',          v: 5,   celdas: 0, tope: 0},
          {n: 'Pila de 9 V',  v: 9,   celdas: 6, tope: 0}
        ];
        var COLORES = [
          {n: 'rojo',     vf: 2.0, c: '#ea4335'},
          {n: 'amarillo', vf: 2.1, c: '#fbbc04'},
          {n: 'verde',    vf: 2.2, c: '#34a853'},
          {n: 'azul',     vf: 3.2, c: '#4285f4'},
          {n: 'blanco',   vf: 3.2, c: '#e8eaed'}
        ];
        var IMAXLED = 20;      /* un LED de 5 mm corriente aguanta 20 mA */
        /* Serie E12: los valores de resistencia que existen en la caja. */
        var E12B = [10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82], E12 = [];
        for(var d = 0; d < 5; d++)
          for(var q = 0; q < E12B.length; q++) E12.push(E12B[q] * Math.pow(10, d));

        var fu = 0, co = 0, modo = 'pulsador', sinR = false, cerrado = false;

        function coma(x, d){ return x.toFixed(d).replace('.', ','); }
        function rot(r){ return r >= 1000 ? coma(r / 1000, r % 1000 ? 1 : 0) + ' k\\u2126'
                                          : r + ' \\u2126'; }

        /* ---- la cuenta entera, paso por paso ---------------------------- */
        function calcula(){
          var Vs = FUENTES[fu].v, Vf = COLORES[co].vf, Iobj = parseFloat(sI.value) / 1000;
          var sobra = Vs - Vf;
          if(sobra <= 0.05){
            return {Vs: Vs, Vf: Vf, Iobj: Iobj, sobra: sobra, imposible: true, I: 0};
          }
          var Rteo = sobra / Iobj, Rreal = null;
          for(var i = 0; i < E12.length; i++){
            if(E12[i] >= Rteo){ Rreal = E12[i]; break; }
          }
          if(Rreal === null) Rreal = E12[E12.length - 1];
          var I = sinR ? null : sobra / Rreal;           /* A */
          return {Vs: Vs, Vf: Vf, Iobj: Iobj, sobra: sobra, imposible: false,
                  Rteo: Rteo, Rreal: Rreal, I: I,
                  Pr: I === null ? 0 : I * I * Rreal,    /* W disipados en R */
                  pasado: I !== null && I * 1000 > IMAXLED,
                  pin: FUENTES[fu].tope > 0 && I !== null && I * 1000 > FUENTES[fu].tope};
        }

        /* ---- geometria del circuito ------------------------------------- */
        var AX = 140, TY = 84, BY = 226, DX = 550;   /* anillo */
        var PX1 = 210, PX2 = 270;                    /* contactos del mando */
        var LEDX = 410;                              /* el LED, en el cable de arriba */

        function pinta(){
          var c = calcula();
          /* Sin resistencia el LED no "luce": se quema. Se dibuja fundido.  */
          var quemado = cerrado && sinR && !c.imposible;
          var luce = cerrado && !c.imposible && !sinR;
          var brillo = 0;
          if(luce && c.I !== null) brillo = Math.min(1, (c.I * 1000) / 12);
          var col = 'var(--ink)', m = '';
          var colFallo = quemado ? 'var(--goo-rojo)' : col;

          /* --- fuente --- */
          var F = FUENTES[fu];
          if(F.celdas){
            var p = S.pila(AX, 155, F.celdas, colFallo);
            m += p.svg;
            m += S.cable(AX, TY, AX, p.mas, colFallo, 2.4);
            m += S.cable(AX, p.menos, AX, BY, colFallo, 2.4);
          } else {
            m += '<rect x="' + (AX - 30) + '" y="125" width="60" height="60" rx="3"'
               + ' fill="var(--surface)" stroke="' + colFallo + '" stroke-width="2.4"></rect>';
            m += S.texto(AX, 150, fu === 0 ? 'P0' : 'USB',
                         ' text-anchor="middle" style="font-size:13px;fill:var(--ink)"');
            m += S.texto(AX, 168, 'GND', ' text-anchor="middle" style="font-size:11px"');
            m += S.cable(AX, TY, AX, 125, colFallo, 2.4);
            m += S.cable(AX, 185, AX, BY, colFallo, 2.4);
          }
          m += S.texto(AX - 34, 112, F.n, ' text-anchor="end" style="font-size:11px"');
          m += S.texto(AX - 34, 128, coma(F.v, 1) + ' V',
                       ' text-anchor="end" style="font-size:13px;fill:var(--ink)"');

          /* --- cable de arriba: mando, LED y resistencia --- */
          m += S.cable(AX, TY, PX1, TY, colFallo, 2.4);
          if(modo === 'interruptor'){
            m += S.interruptor(PX1, PX2, TY, cerrado, colFallo);
            m += S.texto((PX1 + PX2) / 2, TY + 26, 'interruptor',
                         ' text-anchor="middle" style="font-size:10px"');
          } else {
            /* pulsador normalmente abierto; al apretarlo, los contactos se
               tocan, y por eso cerrado se dibuja como un puente recto.      */
            if(cerrado){
              m += S.nodo(PX1, TY, colFallo) + S.nodo(PX2, TY, colFallo);
              m += S.cable(PX1, TY, PX2, TY, colFallo, 2.4);
              var xm = (PX1 + PX2) / 2;
              m += S.cable(xm, TY - 6, xm, TY - 18, colFallo, 2);
              m += S.cable(xm - 9, TY - 18, xm + 9, TY - 18, colFallo, 2.8);
            } else {
              m += S.pulsador(PX1, PX2, TY, colFallo);
            }
            m += S.texto((PX1 + PX2) / 2, TY + 26, 'pulsador',
                         ' text-anchor="middle" style="font-size:10px"');
          }
          m += '<rect x="' + (PX1 - 14) + '" y="' + (TY - 46) + '" width="' + (PX2 - PX1 + 28)
             + '" height="62" fill="#000" fill-opacity="0" pointer-events="all"'
             + ' data-clic="mando" tabindex="0" role="button"'
             + ' aria-label="Accionar el mando del circuito"></rect>';

          m += S.cable(PX2, TY, LEDX - 11, TY, colFallo, 2.4);
          /* el LED, con su color y su brillo */
          if(quemado){
            m += S.led(LEDX, TY, 'var(--goo-rojo)');
            m += S.texto(LEDX, TY + 30, 'quemado',
                         ' text-anchor="middle" style="font-size:11px;fill:var(--goo-rojo)"');
          } else {
            if(brillo > 0){
              m += '<circle cx="' + LEDX + '" cy="' + TY + '" r="30" fill="' + COLORES[co].c
                 + '" opacity="' + (0.5 * brillo).toFixed(3) + '"></circle>';
            }
            m += S.led(LEDX, TY, col);
            m += S.texto(LEDX, TY + 30, 'LED ' + COLORES[co].n + ' \\u00b7 Vf = '
                       + coma(c.Vf, 1) + ' V',
                         ' text-anchor="middle" style="font-size:10.5px"');
          }
          m += S.cable(LEDX + 11, TY, DX, TY, colFallo, 2.4);

          /* --- lado derecho: la resistencia, o el hueco que deja --- */
          m += S.cable(DX, TY, DX, 127, colFallo, 2.4);
          if(sinR){
            m += S.trazo('M' + DX + ' 127 L' + DX + ' 183', 'var(--goo-rojo)', 2.4, true);
            m += S.texto(DX - 12, 158, 'sin resistencia',
                         ' text-anchor="end" style="font-size:10.5px;fill:var(--goo-rojo)"');
          } else {
            m += S.resistencia(DX, 155, colFallo, true);
            if(!c.imposible){
              m += S.texto(DX - 16, 152, rot(c.Rreal),
                           ' text-anchor="end" style="font-size:13px;fill:var(--ink)"');
            }
            m += S.texto(DX - 16, 168, 'limitadora', ' text-anchor="end" style="font-size:10px"');
          }
          m += S.cable(DX, 183, DX, BY, colFallo, 2.4);
          m += S.cable(DX, BY, AX, BY, colFallo, 2.4);

          /* corriente calculada, escrita sobre el cable de vuelta */
          var txtI;
          if(!cerrado) txtI = 'circuito abierto \\u00b7 I = 0';
          else if(c.imposible) txtI = 'I = 0 \\u00b7 no hay tensi\\u00f3n de sobra';
          else if(sinR) txtI = 'I = descontrolada';
          else txtI = 'I = ' + coma(c.I * 1000, 1) + ' mA';
          m += S.texto(320, BY - 10, txtI, ' text-anchor="middle" style="font-size:12px;fill:'
                     + (cerrado && !c.imposible && !sinR ? 'var(--goo-azul)' : 'var(--ink-soft)') + '"');

          /* --- la regla de valores que existen de verdad --- */
          if(!c.imposible && !sinR) m += reglaE12(c);

          /* --- veredicto --- */
          var v = veredicto(c);
          m += S.texto(18, 34, v.etq,
                       ' style="font-size:13px;letter-spacing:.12em;fill:' + v.col + '"');

          svg.innerHTML = m;
          tI.innerHTML = Math.round(parseFloat(sI.value)) + ' mA';
          pinta_pie(c, v);
          marca(segF, 'f', String(fu));
          marca(segC, 'c', String(co));
          segM.querySelectorAll('button[data-m]').forEach(function(b){
            b.setAttribute('aria-pressed',
              b.dataset.m === 'sinr' ? (sinR ? 'true' : 'false')
                                     : (b.dataset.m === modo ? 'true' : 'false'));
          });
        }

        function marca(cont, attr, val){
          cont.querySelectorAll('button[data-' + attr + ']').forEach(function(b){
            b.setAttribute('aria-pressed', b.dataset[attr] === val ? 'true' : 'false');
          });
        }

        /* Ventana de cinco valores E12 alrededor del elegido, colocados en
           escala logaritmica: es como estan repartidos de verdad.           */
        function reglaE12(c){
          var i = E12.indexOf(c.Rreal);
          var a = Math.max(0, Math.min(i - 2, E12.length - 5)), ven = E12.slice(a, a + 5);
          var X0 = 150, X1 = 520, Y = 268;
          var l0 = Math.log(ven[0]), l1 = Math.log(ven[4]);
          function px(r){ return X0 + (Math.log(r) - l0) / (l1 - l0) * (X1 - X0); }
          var m = S.cable(X0 - 14, Y, X1 + 14, Y, 'var(--line)', 1.6);
          m += S.texto(X0 - 22, Y + 4, 'E12', ' text-anchor="end" style="font-size:10px"');
          for(var k = 0; k < 5; k++){
            var x = px(ven[k]), es = ven[k] === c.Rreal;
            m += S.cable(x, Y - 5, x, Y + 5, es ? 'var(--goo-verde)' : 'var(--line)', es ? 2.6 : 1.6);
            m += S.texto(x, Y + 19, rot(ven[k]), ' text-anchor="middle" style="font-size:9.5px;fill:'
                       + (es ? 'var(--goo-verde)' : 'var(--ink-soft)') + '"');
          }
          /* donde cae la cuenta exacta, si entra en la ventana dibujada */
          var rt = c.Rteo;
          if(rt >= ven[0] && rt <= ven[4]){
            var xt = px(rt);
            m += S.trazo('M' + xt.toFixed(1) + ' ' + (Y - 20) + ' L' + xt.toFixed(1) + ' ' + (Y - 7),
                         'var(--goo-azul)', 2);
            m += S.texto(xt, Y - 24, 'tu cuenta: ' + rot(Math.round(rt)),
                         ' text-anchor="middle" style="font-size:9.5px;fill:var(--goo-azul)"');
          }
          return m;
        }

        function veredicto(c){
          if(c.imposible)
            return {etq: 'NO PUEDE ENCENDER', col: 'var(--goo-rojo)', k: 'imposible'};
          if(sinR) return {etq: 'SIN RESISTENCIA \\u00b7 NO LO HAGAS', col: 'var(--goo-rojo)', k: 'sinr'};
          if(c.pin) return {etq: 'PASA DEL L\\u00cdMITE DEL PIN', col: 'var(--goo-amarillo)', k: 'pin'};
          if(c.pasado) return {etq: 'DEMASIADA CORRIENTE', col: 'var(--goo-amarillo)', k: 'pasado'};
          if(c.I * 1000 < 3) return {etq: 'ENCIENDE, PERO POCO', col: 'var(--goo-azul)', k: 'flojo'};
          return {etq: 'CALCULADO Y CORRECTO', col: 'var(--goo-verde)', k: 'bien'};
        }

        function f2(a, b){ return '<tr><td>' + a + '</td><td>' + b + '</td></tr>'; }

        function pinta_pie(c, v){
          var t, f = '';
          if(c.imposible){
            t = '<b>Con ' + coma(c.Vs, 1) + ' V no puedes encender un LED de '
              + coma(c.Vf, 1) + ' V.</b> Al LED le hace falta su tensi&oacute;n directa para empezar '
              + 'a conducir, y aqu&iacute; la fuente se queda corta: le faltan <b>'
              + coma(Math.abs(c.sobra), 1) + ' V</b>. No hay resistencia que lo arregle, '
              + 'porque la resistencia solo puede <b>quitar</b> tensi&oacute;n, nunca a&ntilde;adirla. '
              + 'Cambia de color o de fuente.';
          } else {
            f = '<table class="tabla">';
            f += f2('Tensi&oacute;n que sobra &nbsp;<i>V<sub>s</sub> &minus; V<sub>f</sub></i>',
                    coma(c.Vs, 1) + ' &minus; ' + coma(c.Vf, 1) + ' = ' + coma(c.sobra, 1) + ' V');
            f += f2('Resistencia que sale &nbsp;<i>R = (V<sub>s</sub> &minus; V<sub>f</sub>) / I</i>',
                    coma(c.sobra, 1) + ' / ' + coma(c.Iobj, 3) + ' = ' + coma(c.Rteo, 0)
                    + ' &#8486;');
            f += f2('La que existe en la caja &nbsp;<i>serie E12</i>', rot(c.Rreal));
            f += f2('Corriente de verdad &nbsp;<i>I = (V<sub>s</sub> &minus; V<sub>f</sub>) / R</i>',
                    sinR ? 'sin control' : coma(c.I * 1000, 1) + ' mA');
            f += f2('Calor en la resistencia &nbsp;<i>P = I&sup2; &times; R</i>',
                    sinR ? '&mdash;' : coma(c.Pr * 1000, 0) + ' mW');
            f += '</table>';

            if(v.k === 'sinr'){
              t = '<b>Sin resistencia, la ley de Ohm no te salva.</b> Y no porque la ley falle, '
                + 'sino porque <b>el LED no es &oacute;hmico</b>: su corriente no es proporcional a la '
                + 'tensi&oacute;n, se dispara en cuanto pasas de su tensi&oacute;n directa. No hay un n&uacute;mero '
                + 'que poner aqu&iacute;, y por eso mismo el LED se destruye en un instante. La '
                + 'resistencia s&iacute; es &oacute;hmica: la pones para que sea <b>ella</b> la que decida la '
                + 'corriente.';
            } else if(v.k === 'pin'){
              t = '<b>' + coma(c.I * 1000, 1) + ' mA es demasiado para un pin de la micro:bit.</b> '
                + 'El fabricante da un m&aacute;ximo de <b>5 mA por pin</b>. El LED lucir&iacute;a, pero est&aacute;s '
                + 'forzando la placa. Baja la corriente que pides hasta 5 mA o menos, y la '
                + 'resistencia te saldr&aacute; m&aacute;s grande.';
            } else if(v.k === 'pasado'){
              t = '<b>Te has pasado del LED.</b> Un LED de 5 mm normal aguanta unos <b>20 mA</b> '
                + 'de forma continua. Con ' + coma(c.I * 1000, 1) + ' mA alumbra m&aacute;s, s&iacute;, y dura '
                + 'menos. Pide menos corriente.';
            } else if(v.k === 'flojo'){
              t = '<b>Enciende, pero se ve poco.</b> Con ' + coma(c.I * 1000, 1) + ' mA el LED '
                + 'alumbra d&eacute;bil. Es lo que pasa cuando eliges una resistencia por costumbre en '
                + 'vez de calcularla: no se rompe nada, simplemente no hace su trabajo.';
            } else {
              t = '<b>Bien calculado.</b> Pides ' + Math.round(c.Iobj * 1000) + ' mA, la cuenta da '
                + coma(c.Rteo, 0) + ' &#8486;, coges la primera que existe por encima &mdash;'
                + rot(c.Rreal) + '&mdash; y por el LED pasan ' + coma(c.I * 1000, 1) + ' mA. '
                + '<b>Siempre hacia arriba</b>: si cogieras la de abajo pasar&iacute;a m&aacute;s corriente '
                + 'de la que pediste.';
            }
            if(!cerrado){
              t = '<b>El circuito est&aacute; abierto.</b> ' + (modo === 'pulsador'
                ? 'Mant&eacute;n apretado el pulsador del dibujo para que luzca: en cuanto lo sueltes, se apaga.'
                : 'Pulsa el interruptor del dibujo: se queda como lo dejes.') + '<br><br>' + t;
            }
          }
          pie.innerHTML = t + f;
        }

        /* ---- el mando: aqui esta la diferencia entre los dos ------------- */
        function aprieta(){ cerrado = true; pinta(); }
        function suelta(){ if(modo === 'pulsador'){ cerrado = false; pinta(); } }

        svg.addEventListener('mousedown', function(e){
          if(!e.target.closest('[data-clic="mando"]')) return;
          e.preventDefault();
          if(modo === 'interruptor'){ cerrado = !cerrado; pinta(); }
          else aprieta();
        });
        svg.addEventListener('touchstart', function(e){
          if(!e.target.closest('[data-clic="mando"]')) return;
          e.preventDefault();
          if(modo === 'interruptor'){ cerrado = !cerrado; pinta(); }
          else aprieta();
        }, {passive: false});
        document.addEventListener('mouseup', suelta);
        document.addEventListener('touchend', suelta);
        /* Con el teclado, el pulsador se queda pulsado mientras se mantiene
           la barra o el Enter, igual que con el raton.                      */
        svg.addEventListener('keydown', function(e){
          if(!e.target.closest || !e.target.closest('[data-clic="mando"]')) return;
          if(e.key !== ' ' && e.key !== 'Enter') return;
          e.preventDefault();
          if(e.repeat) return;
          if(modo === 'interruptor'){ cerrado = !cerrado; pinta(); }
          else aprieta();
        });
        svg.addEventListener('keyup', function(e){
          if(e.key === ' ' || e.key === 'Enter') suelta();
        });

        segF.addEventListener('click', function(e){
          var b = e.target.closest('button[data-f]');
          if(!b) return;
          fu = parseInt(b.dataset.f, 10);
          pinta();
        });
        segC.addEventListener('click', function(e){
          var b = e.target.closest('button[data-c]');
          if(!b) return;
          co = parseInt(b.dataset.c, 10);
          pinta();
        });
        segM.addEventListener('click', function(e){
          var b = e.target.closest('button[data-m]');
          if(!b) return;
          if(b.dataset.m === 'sinr') sinR = !sinR;
          else { modo = b.dataset.m; cerrado = false; }
          pinta();
        });
        sI.addEventListener('input', pinta);
        pinta();
      })();
      </script>
'''


# --------------------------------------------------------------------------
# Escena 6 - el test que se corrige solo
# --------------------------------------------------------------------------
# Las preguntas de calculo se generan con numeros al azar y se corrigen
# resolviendolas, no comparando contra una lista de respuestas escritas. Por eso
# el boton "Otra tanda" da un examen distinto cada vez.
ESC_TEST = u'''
      <style>
        #esc-test .preg{border-bottom:1px solid var(--line-soft);padding:13px 0}
        #esc-test .preg:last-of-type{border-bottom:0}
        #esc-test .preg > p{margin:0 0 8px;font-size:15px;color:var(--ink)}
        #esc-test .preg .num{font:500 11px var(--f-m);color:var(--ink-soft);
          letter-spacing:.1em;margin-right:8px}
        #esc-test .ops{display:flex;flex-direction:column;gap:5px}
        #esc-test .ops label{display:flex;gap:8px;align-items:flex-start;font-size:14.5px;
          cursor:pointer;color:var(--ink-soft)}
        #esc-test .ops input{margin-top:4px;accent-color:var(--goo-azul)}
        #esc-test .num-resp{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
        #esc-test .num-resp input{width:120px;background:var(--surface);color:var(--ink);
          border:1.5px solid var(--line);border-radius:2px;padding:7px 9px;font:400 14px var(--f-m)}
        #esc-test .unidad{font:400 13px var(--f-m);color:var(--ink-soft)}
        #esc-test .juicio{margin-top:8px;font-size:14px;padding:8px 11px;border-radius:2px;
          border-left:4px solid var(--line);background:var(--surface-2)}
        #esc-test .juicio.si{border-left-color:var(--goo-verde)}
        #esc-test .juicio.no{border-left-color:var(--goo-rojo)}
        #esc-test .cuerpo{padding:4px 16px 14px}
        #esc-test .botones{display:flex;gap:8px;flex-wrap:wrap;padding:12px 16px;
          border-top:1px solid var(--line)}
        #esc-test .botones button{background:var(--surface);border:1.5px solid var(--goo-azul);
          color:var(--goo-azul);border-radius:2px;padding:8px 16px;font:500 12px var(--f-m);cursor:pointer}
        #esc-test .botones button.flojo{border-color:var(--line);color:var(--ink-soft)}
      </style>
      <div class="escena" id="esc-test">
        <div class="escena-barra">
          <span class="escena-titulo">Autoevaluaci&oacute;n &middot; se corrige sola y cambia cada vez</span>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 120" id="svg-test" role="img"
               aria-label="Marcador con las diez preguntas y la nota"></svg>
        </div>
        <div class="cuerpo" id="test-cuerpo"></div>
        <div class="botones">
          <button type="button" id="test-corrige">Corregir</button>
          <button type="button" id="test-otra" class="flojo">Otra tanda</button>
        </div>
        <div class="pie" id="pie-test"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-test');
        if(!svg) return;
        var cuerpo = document.getElementById('test-cuerpo');
        var pie = document.getElementById('pie-test');
        var S = window.U6;

        function coma(x, d){ return x.toFixed(d).replace('.', ','); }
        function az(a){ return a[Math.floor(Math.random() * a.length)]; }
        function baraja(a){
          a = a.slice();
          for(var i = a.length - 1; i > 0; i--){
            var j = Math.floor(Math.random() * (i + 1)), t = a[i];
            a[i] = a[j]; a[j] = t;
          }
          return a;
        }

        /* ------------------------------------------------------------------
           Las cinco preguntas de calculo. Cada una inventa sus numeros y
           calcula su propia solucion: no hay ninguna respuesta escrita.
        ------------------------------------------------------------------ */
        var CALCULO = [
          function(){                                   /* ley de Ohm */
            var V = az([4.5, 6, 9, 12]), R = az([15, 20, 24, 30, 45, 60]);
            return {t: 'Una pila de <b>' + coma(V, 1) + ' V</b> alimenta una resistencia de <b>'
                     + R + ' &#8486;</b>. &iquest;Qu&eacute; intensidad circula?',
                    u: 'A', sol: V / R, dec: 3,
                    como: 'I = V / R = ' + coma(V, 1) + ' / ' + R + ' = ' + coma(V / R, 3) + ' A'};
          },
          function(){                                   /* serie */
            var R1 = az([4, 5, 6, 8, 10]), R2 = az([6, 12, 15, 20]), V = az([9, 12, 18]);
            var Rt = R1 + R2;
            return {t: 'Dos resistencias de <b>' + R1 + ' &#8486;</b> y <b>' + R2
                     + ' &#8486;</b> <b>en serie</b>, con una pila de <b>' + V
                     + ' V</b>. &iquest;Cu&aacute;nto vale la resistencia total?',
                    u: '&#8486;', sol: Rt, dec: 0,
                    como: 'En serie se suman: R = ' + R1 + ' + ' + R2 + ' = ' + Rt
                        + ' &#8486;. (Y por el circuito circular&iacute;an ' + coma(V / Rt, 3) + ' A.)'};
          },
          function(){                                   /* paralelo */
            var R = az([12, 18, 24, 30, 60]), n = az([2, 3, 4]), V = az([4.5, 9, 12]);
            var Rt = R / n, It = V / Rt;
            return {t: '<b>' + n + ' l&aacute;mparas iguales</b> de <b>' + R
                     + ' &#8486;</b> cada una, conectadas <b>en paralelo</b> a una pila de <b>'
                     + coma(V, 1) + ' V</b>. &iquest;Qu&eacute; corriente total da la pila?',
                    u: 'A', sol: It, dec: 3,
                    como: 'Iguales y en paralelo: R = ' + R + ' / ' + n + ' = ' + coma(Rt, 2)
                        + ' &#8486;, y entonces I = ' + coma(V, 1) + ' / ' + coma(Rt, 2) + ' = '
                        + coma(It, 3) + ' A. Tambi&eacute;n vale sumar las ' + n + ' corrientes de '
                        + coma(V / R, 3) + ' A.'};
          },
          function(){                                   /* potencia */
            var V = az([230, 12, 24]), I = az([0.5, 1.5, 2, 3, 5]);
            return {t: 'Por un aparato conectado a <b>' + V + ' V</b> pasan <b>' + coma(I, 1)
                     + ' A</b>. &iquest;Qu&eacute; potencia tiene?',
                    u: 'W', sol: V * I, dec: 0,
                    como: 'P = V &times; I = ' + V + ' &times; ' + coma(I, 1) + ' = '
                        + coma(V * I, 0) + ' W'};
          },
          function(){                                   /* energia y dinero */
            var P = az([1000, 1200, 1500, 2000, 2200]), h = az([0.5, 1, 1.5, 2]);
            var dias = az([10, 20, 30]), pr = az([0.15, 0.2, 0.25, 0.3]);
            var kWh = P / 1000 * h * dias;
            return {t: 'Un aparato de <b>' + P + ' W</b> funciona <b>' + coma(h, 1)
                     + ' h al d&iacute;a</b> durante <b>' + dias + ' d&iacute;as</b>. Si el kWh cuesta <b>'
                     + coma(pr, 2) + ' &euro;</b>, &iquest;cu&aacute;nto cuesta tenerlo funcionando?',
                    u: '&euro;', sol: kWh * pr, dec: 2,
                    como: 'E = ' + coma(P / 1000, 1) + ' kW &times; ' + coma(h, 1) + ' h &times; '
                        + dias + ' d&iacute;as = ' + coma(kWh, 2) + ' kWh; y ' + coma(kWh, 2)
                        + ' &times; ' + coma(pr, 2) + ' = ' + coma(kWh * pr, 2) + ' &euro;'};
          },
          function(){                                   /* resistencia del LED */
            /* Las mismas tensiones directas que la escena del LED y la teoria. */
            var Vs = az([4.5, 5, 9, 12]), Vf = az([2.0, 2.1, 2.2, 3.2]), I = az([5, 10, 15, 20]);
            var R = (Vs - Vf) / (I / 1000);
            return {t: 'Quieres que por un LED de <b>' + coma(Vf, 1)
                     + ' V</b> pasen <b>' + I + ' mA</b>, y lo conectas a <b>' + coma(Vs, 1)
                     + ' V</b>. &iquest;Qu&eacute; resistencia hay que ponerle en serie?',
                    u: '&#8486;', sol: R, dec: 0,
                    como: 'R = (' + coma(Vs, 1) + ' &minus; ' + coma(Vf, 1) + ') / ' + coma(I / 1000, 3)
                        + ' = ' + coma(R, 0) + ' &#8486;. En la caja cogemos el primer valor '
                        + 'normalizado por encima.'};
          }
        ];

        /* ---- las de razonar. La correcta es siempre la primera de la lista
           y las opciones se barajan al montarlas.                           */
        var CONCEPTO = [
          {t: '&iquest;Qu&eacute; es exactamente un <b>cortocircuito</b>?',
           o: ['Un camino de vuelta al generador <b>sin receptor</b>, solo cable.',
               'Un circuito demasiado corto, con poco cable.',
               'Un circuito abierto por el que no circula corriente.',
               'Cualquier circuito en el que la corriente es alta.'],
           p: 'Lo que lo define no es la corriente alta: la corriente alta es la consecuencia '
            + 'de que no haya receptor que se oponga al paso.'},
          {t: 'Se funde una l&aacute;mpara de las tres que hay <b>en paralelo</b>. &iquest;Qu&eacute; pasa?',
           o: ['Las otras dos siguen luciendo igual, y la pila da menos corriente total.',
               'Se apagan las tres, porque se abre el circuito.',
               'Las otras dos lucen m&aacute;s, porque les llega m&aacute;s tensi&oacute;n.',
               'Las otras dos lucen menos, porque se reparten peor la corriente.'],
           p: 'Cada rama tiene su propio camino y sigue recibiendo la misma tensi&oacute;n. Lo que '
            + 'cambia es el total: una puerta menos, menos corriente en el cable principal.'},
          {t: '&iquest;Por qu&eacute; el <b>amper&iacute;metro</b> se conecta en serie?',
           o: ['Porque mide lo que pasa por un punto, y tiene que estar en el camino.',
               'Porque as&iacute; no se estropea con tensiones altas.',
               'Porque en paralelo marcar&iacute;a siempre cero.',
               'Porque mide la diferencia entre dos puntos del circuito.'],
           p: 'La &uacute;ltima opci&oacute;n describe al volt&iacute;metro, que por eso s&iacute; va en paralelo.'},
          {t: 'La diferencia entre un <b>pulsador</b> y un <b>interruptor</b> es que&hellip;',
           o: ['el pulsador vuelve solo a su posici&oacute;n; el interruptor se queda como lo dejas.',
               'el pulsador deja pasar menos corriente que el interruptor.',
               'el interruptor sirve para corriente alterna y el pulsador para continua.',
               'el pulsador no corta del todo el circuito, solo lo debilita.'],
           p: 'Por eso el timbre lleva pulsador y la l&aacute;mpara del techo lleva interruptor: uno '
            + 'quieres que se apague al soltar y el otro no.'},
          {t: 'Un <b>kWh</b> es&hellip;',
           o: ['una cantidad de <b>energ&iacute;a</b>: la que gasta un aparato de 1.000 W en una hora.',
               'una cantidad de <b>potencia</b>, la que puede dar la instalaci&oacute;n.',
               'lo mismo que un kW, pero escrito de otra forma.',
               'la corriente que pasa por el contador en una hora.'],
           p: 'El kW mide lo deprisa que gastas; el kWh, lo que llevas gastado. Es la diferencia '
            + 'entre la velocidad del coche y los kil&oacute;metros que llevas hechos.'},
          {t: 'En la <b>etiqueta energ&eacute;tica</b> de un frigor&iacute;fico, la letra sirve para&hellip;',
           o: ['comparar aparatos del mismo tipo entre s&iacute;: la A gasta menos que la G.',
               'saber cu&aacute;ntos vatios consume el aparato en cada momento.',
               'saber si el aparato es seguro y cumple la normativa el&eacute;ctrica.',
               'comparar cualquier aparato con cualquier otro, sea del tipo que sea.'],
           p: 'La letra solo compara dentro de la misma familia de productos. El dato que sirve '
            + 'para calcular dinero es el de <b>kWh al a&ntilde;o</b> que viene debajo.'}
        ];

        var preguntas = [];

        function monta(){
          /* cuatro de calculo y seis de concepto, escogidas al azar */
          var c = baraja(CALCULO).slice(0, 4).map(function(f){
            var q = f(); q.tipo = 'num'; return q;
          });
          var k = baraja(CONCEPTO).slice(0, 6).map(function(q){
            var correcta = q.o[0], ops = baraja(q.o);
            return {tipo: 'op', t: q.t, ops: ops, i: ops.indexOf(correcta), p: q.p};
          });
          preguntas = baraja(c.concat(k));

          var h = '';
          preguntas.forEach(function(q, n){
            h += '<div class="preg" id="preg-' + n + '">';
            h += '<p><span class="num">' + (n + 1) + '</span>' + q.t + '</p>';
            if(q.tipo === 'num'){
              h += '<div class="num-resp"><input type="text" inputmode="decimal" data-n="' + n
                 + '" aria-label="Respuesta de la pregunta ' + (n + 1) + '" placeholder="0,00">'
                 + '<span class="unidad">' + q.u + '</span></div>';
            } else {
              h += '<div class="ops">';
              q.ops.forEach(function(o, j){
                h += '<label><input type="radio" name="p' + n + '" value="' + j + '"><span>'
                   + o + '</span></label>';
              });
              h += '</div>';
            }
            h += '</div>';
          });
          cuerpo.innerHTML = h;
          pie.innerHTML = 'Contesta las diez y pulsa <b>Corregir</b>. Los n&uacute;meros se pueden '
            + 'escribir con coma o con punto. En las de calcular se da por buena una diferencia '
            + 'de hasta el <b>2 %</b>, para que redondear no te cueste un punto: lo que se '
            + 'corrige es la cuenta, no los decimales.';
          marcador(null);
        }

        /* Acepta 0,5 y 0.5, y tambien "0,5 A" o "270 ohmios": se queda con las
           cifras. El punto de los miles se distingue del decimal mirando si
           detras van exactamente tres cifras.                               */
        function leeNum(s){
          if(s === null || s === undefined) return null;
          s = String(s).replace(/[^0-9.,\\-]/g, '');
          if(!s) return null;
          if(s.indexOf(',') >= 0) s = s.replace(/\\./g, '').replace(',', '.');
          else if(/^-?\\d{1,3}(\\.\\d{3})+$/.test(s)) s = s.replace(/\\./g, '');
          var x = parseFloat(s);
          return isNaN(x) ? null : x;
        }

        function corrige(){
          var res = preguntas.map(function(q, n){
            var caja = document.getElementById('preg-' + n);
            var bien = false, dicho = null;
            if(q.tipo === 'num'){
              dicho = leeNum(caja.querySelector('input').value);
              /* tolerancia del 2 % sobre la solucion calculada */
              bien = dicho !== null && Math.abs(dicho - q.sol) <= Math.abs(q.sol) * 0.02 + 1e-9;
            } else {
              var m = caja.querySelector('input:checked');
              dicho = m ? parseInt(m.value, 10) : null;
              bien = dicho === q.i;
            }
            var j = caja.querySelector('.juicio');
            if(!j){
              j = document.createElement('div');
              j.className = 'juicio';
              caja.appendChild(j);
            }
            j.className = 'juicio ' + (bien ? 'si' : 'no');
            if(q.tipo === 'num'){
              j.innerHTML = (bien ? '<b>Bien.</b> ' : (dicho === null
                   ? '<b>Sin contestar.</b> ' : '<b>No.</b> Has puesto ' + coma(dicho, q.dec)
                     + ' ' + q.u + '. ')) + q.como;
            } else {
              /* La opcion ya acaba en punto: no se le pone otro detras. */
              j.innerHTML = (bien ? '<b>Bien.</b> ' : '<b>No.</b> La buena era: <i>'
                   + q.ops[q.i].replace(/<[^>]+>/g, '') + '</i> ') + q.p;
            }
            return bien;
          });
          marcador(res);
          var nota = res.filter(Boolean).length;
          var cierre;
          if(nota === 10) cierre = 'Diez de diez. Pulsa <b>Otra tanda</b>: los n&uacute;meros cambian.';
          else if(nota >= 7) cierre = 'Vas bien. Mira las falladas, corrige en la libreta y tira '
            + 'otra tanda: las preguntas de calcular <b>no son las mismas</b> la segunda vez.';
          else if(nota >= 5) cierre = 'Aprobado justo. Rep&aacute;salo: casi siempre lo que falla no es '
            + 'la cuenta, es saber <b>qu&eacute; f&oacute;rmula</b> toca.';
          else cierre = 'Vuelve a la teor&iacute;a de las sesiones 2, 3 y 4 antes de repetir. Lee las '
            + 'explicaciones de abajo una a una: cada una dice el porqu&eacute;, no solo la respuesta.';
          pie.innerHTML = '<b>Nota: ' + nota + ' de 10.</b> ' + cierre;
        }

        /* El marcador se dibuja a partir del resultado, no al reves. */
        function marcador(res){
          var m = '', X0 = 20, W = 600, n = 10, paso = W / n;
          for(var i = 0; i < n; i++){
            var x = X0 + i * paso + 3, w = paso - 6;
            var col = 'var(--surface-2)', bor = 'var(--line)';
            if(res){
              col = res[i] ? 'var(--goo-verde)' : 'var(--goo-rojo)';
              bor = col;
            }
            m += '<rect x="' + x.toFixed(1) + '" y="30" width="' + w.toFixed(1) + '" height="30"'
               + ' rx="2" fill="' + col + '" stroke="' + bor + '" stroke-width="1.4"></rect>';
            m += '<text x="' + (x + w / 2).toFixed(1) + '" y="50" text-anchor="middle"'
               + ' class="rotulo-svg" style="font-size:12px;fill:'
               + (res ? '#202124' : 'var(--ink-soft)') + '">' + (i + 1) + '</text>';
          }
          var nota = res ? res.filter(Boolean).length : null;
          var txt = res ? 'NOTA: ' + nota + ' DE 10' : 'SIN CORREGIR';
          m += '<text x="20" y="18" class="rotulo-svg" style="font-size:12px;letter-spacing:.12em;'
             + 'fill:' + (res ? (nota >= 5 ? 'var(--goo-verde)' : 'var(--goo-rojo)')
                              : 'var(--ink-soft)') + '">' + txt + '</text>';
          /* barra de la nota, con la longitud que le toca */
          if(res){
            m += '<rect x="20" y="78" width="600" height="10" rx="2" fill="var(--surface-2)"'
               + ' stroke="var(--line)" stroke-width="1"></rect>';
            m += '<rect x="20" y="78" width="' + (600 * nota / 10) + '" height="10" rx="2"'
               + ' fill="' + (nota >= 5 ? 'var(--goo-verde)' : 'var(--goo-rojo)') + '"></rect>';
            m += '<text x="320" y="106" text-anchor="middle" class="rotulo-svg"'
               + ' style="font-size:11px">aprobado a partir de 5</text>';
            m += '<rect x="' + (20 + 600 * 0.5) + '" y="72" width="1.6" height="22"'
               + ' fill="var(--ink-soft)"></rect>';
          }
          svg.innerHTML = m;
        }

        document.getElementById('test-corrige').addEventListener('click', corrige);
        document.getElementById('test-otra').addEventListener('click', monta);
        monta();
      })();
      </script>
'''
