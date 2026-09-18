# -*- coding: utf-8 -*-
"""Las tres escenas nuevas del tema 10: sesiones 4, 5 y 6.

Ninguna es una animacion grabada. Las tres CALCULAN:

  SENSORES (S4)  ejecuta de verdad el bucle "para siempre" de la placa, con su
                 condicional dentro, cien veces por minuto. El numero que
                 aparece en pantalla es la lectura del sensor simulado, y la
                 rama del programa que se ilumina es la que ha salido de
                 comparar ese numero con el umbral. El contador de parpadeos
                 cuenta los cambios REALES de los ultimos seis segundos.

  ROBOT (S5)     simula un robot de dos ruedas (traccion diferencial) buscando
                 una lampara. La luz que recibe cada sensor sale de la ley del
                 inverso del cuadrado por el coseno del angulo; el movimiento,
                 de integrar la cinematica paso a paso. El tiempo y los
                 centimetros recorridos que da al final estan medidos sobre esa
                 simulacion, no escritos a mano.

  DIA (S6)       recorre los 1.440 minutos de un dia, calcula la luz de cada
                 minuto y ejecuta las tres estrategias de encendido sobre esos
                 datos. Las horas, los vatios-hora, los euros y los minutos a
                 oscuras son sumas sobre ese recorrido.

Las clases CSS llevan prefijo propio (sx-, rb-, dj-) para no chocar con las de
la pagina ni con las de la escena de la placa de la sesion 3.
"""

# ==========================================================================
# S4 - El banco de sensores
# ==========================================================================
SENSORES = u'''
      <div class="escena" id="esc-sx">
        <div class="escena-barra">
          <span class="escena-titulo">El banco de sensores &middot; mueve el mando y mira qu&eacute; decide</span>
          <div class="seg" id="seg-sx">
            <button type="button" data-p="0" aria-pressed="true">Farola</button>
            <button type="button" data-p="1">Invernadero</button>
            <button type="button" data-p="2">Ruido</button>
          </div>
        </div>
        <div class="lienzo">
          <div class="sx">
            <div class="sx-izq">
              <svg viewBox="0 0 320 200" id="svg-sx" role="img"
                   aria-label="Pantalla de 25 LED de una micro:bit que se enciende seg&uacute;n lo que mide el sensor"></svg>
              <div class="sx-mandos" id="mandos-sx"></div>
            </div>
            <div class="sx-der">
              <div class="sx-prog" id="prog-sx"></div>
              <p class="sx-eval" id="eval-sx"></p>
            </div>
          </div>
        </div>
        <div class="pie" id="pie-sx"></div>
      </div>

      <style>
      .sx{display:flex;gap:18px;flex-wrap:wrap;align-items:flex-start}
      .sx-izq{flex:1 1 320px;min-width:270px}
      .sx-der{flex:1 1 300px;min-width:260px}
      .sx-mandos{margin-top:10px}
      .sx-fila{display:flex;align-items:center;gap:9px;flex-wrap:wrap;margin:0 0 8px;
        font-family:var(--f-m);font-size:12.5px;color:var(--ink)}
      .sx-fila label{min-width:104px}
      .sx-fila input[type="range"]{flex:1 1 130px;min-width:110px;accent-color:var(--goo-azul)}
      .sx-fila input[type="number"]{width:64px;font-family:var(--f-m);font-size:12.5px;padding:4px 5px;
        border:1.5px solid var(--line);border-radius:2px;background:var(--surface);color:var(--ink)}
      .sx-fila .val{font-weight:500;color:var(--goo-azul);min-width:54px;text-align:right}
      .sx-chk{display:flex;align-items:center;gap:7px;font-family:var(--f-m);font-size:12.5px;
        color:var(--ink-soft);margin:0 0 6px;cursor:pointer}
      .sx-chk input{accent-color:var(--goo-azul)}
      .sx-prog{border:1.5px solid var(--line);border-radius:2px;background:var(--surface);padding:10px 12px;
        font-family:var(--f-m);font-size:12.5px;line-height:1.7}
      .sx-prog .b{display:block;padding:3px 8px;border-left:4px solid var(--line);margin:2px 0;border-radius:2px}
      .sx-prog .b.ev{border-left-color:var(--goo-azul);background:var(--accent-soft)}
      .sx-prog .b.on{border-left-color:var(--goo-verde);background:rgba(52,168,83,.14)}
      .sx-prog .s1{margin-left:16px}
      .sx-prog .s2{margin-left:32px}
      .sx-eval{font-family:var(--f-m);font-size:12.5px;color:var(--ink-soft);line-height:1.65;margin:10px 0 0}
      .sx-eval b{color:var(--ink)}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-sx');
        if(!svg) return;
        var caja = document.getElementById('esc-sx');
        var mandos = document.getElementById('mandos-sx');
        var prog = document.getElementById('prog-sx');
        var evalu = document.getElementById('eval-sx');
        var pie = document.getElementById('pie-sx');
        var seg = document.getElementById('seg-sx');

        /* ---- iconos de 5x5, los mismos que dibuja MakeCode ---- */
        var ICO = {
          lleno: '#####' + '#####' + '#####' + '#####' + '#####',
          vacio: '.....' + '.....' + '.....' + '.....' + '.....',
          abajo: '..#..' + '..#..' + '..#..' + '#.#.#' + '.###.',
          arriba:'.###.' + '#.#.#' + '..#..' + '..#..' + '..#..',
          bien:  '.....' + '....#' + '...#.' + '#.#..' + '.#...',
          grito: '..#..' + '..#..' + '..#..' + '.....' + '..#..'
        };

        var luz = [], i;
        for(i = 0; i < 25; i++) luz.push(0);

        function pinta_icono(clave){
          var g = ICO[clave];
          for(var k = 0; k < 25; k++) luz[k] = g.charAt(k) === '#' ? 1 : 0;
        }
        function pinta_barra(n){
          /* n columnas encendidas, de izquierda a derecha */
          for(var y = 0; y < 5; y++)
            for(var x = 0; x < 5; x++) luz[y*5+x] = (x < n) ? 1 : 0;
        }

        /* ---- estado ---- */
        var modo = 0, reloj = null;
        var v = {luz:128, temp:20, son:60, umbral:50, apagar:80,
                 frio:10, calor:28, uruido:150, tiembla:false, hist:false};
        var encendida = false, cambios = [];

        /* generador de numeros al azar para el temblor del sensor */
        function tembleque(){ return Math.round((Math.random()*2 - 1) * 12); }

        var MANDOS = [
          '<div class="sx-fila"><label>Luz que le da</label>'
          + '<input type="range" id="sx-luz" min="0" max="255" step="1" value="128">'
          + '<span class="val" id="sx-luz-v">128</span></div>'
          + '<div class="sx-fila"><label>Umbral: enciende por debajo de</label>'
          + '<input type="number" id="sx-umbral" min="0" max="255" step="1" value="50"></div>'
          + '<label class="sx-chk"><input type="checkbox" id="sx-tiembla"> el sensor tiembla '
          + '(como el de verdad)</label>'
          + '<label class="sx-chk"><input type="checkbox" id="sx-hist"> y apaga por encima de '
          + '<input type="number" id="sx-apagar" min="0" max="255" step="1" value="80" '
          + 'style="width:58px;margin-left:4px"></label>',

          '<div class="sx-fila"><label>Temperatura</label>'
          + '<input type="range" id="sx-temp" min="-5" max="45" step="1" value="20">'
          + '<span class="val" id="sx-temp-v">20 &deg;C</span></div>'
          + '<div class="sx-fila"><label>Aviso de fr&iacute;o por debajo de</label>'
          + '<input type="number" id="sx-frio" min="-5" max="45" step="1" value="10"></div>'
          + '<div class="sx-fila"><label>Aviso de calor por encima de</label>'
          + '<input type="number" id="sx-calor" min="-5" max="45" step="1" value="28"></div>',

          '<div class="sx-fila"><label>Ruido que hay</label>'
          + '<input type="range" id="sx-son" min="0" max="255" step="1" value="60">'
          + '<span class="val" id="sx-son-v">60</span></div>'
          + '<div class="sx-fila"><label>Avisa por encima de</label>'
          + '<input type="number" id="sx-uruido" min="0" max="255" step="1" value="150"></div>'
        ];

        var PIES = [
          '<b>Farola autom&aacute;tica.</b> El bucle <i>para siempre</i> se ejecuta diez veces por '
          + 'segundo: lee el sensor, compara con el umbral y decide. La rama verde es la que se '
          + 'est&aacute; ejecutando ahora mismo.',
          '<b>Aviso de invernadero.</b> Tres respuestas con dos comparaciones. Las condiciones se '
          + 'miran <b>en orden</b>, y en cuanto una se cumple, las de abajo ya no se miran.',
          '<b>Medidor de ruido.</b> Aqu&iacute; el n&uacute;mero del sensor no se compara: se '
          + '<b>convierte</b> en el n&uacute;mero de columnas encendidas con una cuenta.'
        ];

        /* ---- el programa que se ve a la derecha ---- */
        function bloques(rama){
          if(modo === 0){
            return '<span class="b ev">para siempre</span>'
              + '<span class="b s1 ' + (rama === 'si' ? 'on' : '') + '">si  <b>nivel de luz</b> &lt; '
              + v.umbral + (v.hist ? ' (y estaba apagada)' : '') + '  entonces</span>'
              + '<span class="b s2 ' + (rama === 'si' ? 'on' : '') + '">encender los 25 LED</span>'
              + '<span class="b s1 ' + (rama === 'no' ? 'on' : '') + '">si no</span>'
              + '<span class="b s2 ' + (rama === 'no' ? 'on' : '') + '">borrar la pantalla</span>';
          }
          if(modo === 1){
            return '<span class="b ev">para siempre</span>'
              + '<span class="b s1 ' + (rama === 'frio' ? 'on' : '') + '">si  <b>temperatura</b> &lt; '
              + v.frio + '  entonces</span>'
              + '<span class="b s2 ' + (rama === 'frio' ? 'on' : '') + '">mostrar flecha abajo</span>'
              + '<span class="b s1 ' + (rama === 'calor' ? 'on' : '') + '">si no, si  <b>temperatura</b> &gt; '
              + v.calor + '  entonces</span>'
              + '<span class="b s2 ' + (rama === 'calor' ? 'on' : '') + '">mostrar flecha arriba</span>'
              + '<span class="b s1 ' + (rama === 'bien' ? 'on' : '') + '">si no</span>'
              + '<span class="b s2 ' + (rama === 'bien' ? 'on' : '') + '">mostrar la marca de bien</span>';
          }
          return '<span class="b ev">para siempre</span>'
            + '<span class="b s1 on">poner <b>nivel</b> a <b>nivel de sonido</b></span>'
            + '<span class="b s1 on">poner <b>columnas</b> a redondear(<b>nivel</b> &times; 5 &divide; 255)</span>'
            + '<span class="b s1 on">dibujar <b>columnas</b> columnas</span>'
            + '<span class="b s1 ' + (rama === 'grito' ? 'on' : '') + '">si  <b>nivel</b> &gt; '
            + v.uruido + '  entonces avisar</span>';
        }

        /* ---- el dibujo: los 25 LED y el sensor que toque ---- */
        function pinta(){
          var m = '', x, y;
          /* la placa, a la derecha; el sensor se dibuja fuera, a la izquierda,
             para que su rotulo se lea sobre el fondo claro y no sobre el negro */
          m += '<rect x="110" y="10" width="200" height="150" rx="12" fill="#1a1a1a"></rect>';
          for(y = 0; y < 5; y++){
            for(x = 0; x < 5; x++){
              var on = luz[y*5+x];
              m += '<rect x="' + (164 + x*20) + '" y="' + (38 + y*20) + '" width="13" height="13" rx="2" fill="'
                 + (on ? '#ff3b30' : '#3a3a3a') + '" stroke="' + (on ? '#ff8a80' : '#4a4a4a')
                 + '" stroke-width="1"></rect>';
            }
          }
          var nom = ['sensor de luz', 'term&oacute;metro', 'micr&oacute;fono'][modo];
          m += '<circle cx="55" cy="80" r="17" fill="var(--surface-2)" stroke="var(--line)" '
             + 'stroke-width="1.5"></circle>';
          if(modo === 0){
            m += '<path d="M55 56 v-9 M40 64 l-6-6 M70 64 l6-6" stroke="#c99a05" stroke-width="2" '
               + 'stroke-linecap="round"></path>';
            m += '<circle cx="55" cy="80" r="8" fill="#fbbc04" opacity="'
               + (0.15 + 0.85*v.luz/255).toFixed(2) + '"></circle>';
          } else if(modo === 1){
            var h = 18 * Math.max(0, Math.min(1, (v.temp + 5) / 50));
            m += '<rect x="52" y="' + (89 - h).toFixed(1) + '" width="6" height="' + h.toFixed(1)
               + '" fill="#ea4335"></rect>';
            m += '<rect x="51" y="67" width="8" height="24" rx="4" fill="none" stroke="var(--ink-soft)" '
               + 'stroke-width="1.5"></rect>';
          } else {
            var r = 4 + 10*v.son/255;
            m += '<circle cx="55" cy="80" r="' + r.toFixed(1) + '" fill="#4285f4"></circle>';
          }
          m += '<line x1="72" y1="80" x2="108" y2="80" stroke="var(--ink-soft)" stroke-width="1.5"></line>';
          m += '<path d="M102 76 l6 4 -6 4" fill="none" stroke="var(--ink-soft)" stroke-width="1.5"></path>';
          m += '<text x="55" y="113" text-anchor="middle" class="sx-rot">' + nom + '</text>';
          m += '<text x="160" y="185" text-anchor="middle" class="sx-rot">'
             + 'entrada &rarr; decisi&oacute;n &rarr; salida</text>';
          m += '<style>.sx-rot{fill:var(--ink-soft);font-family:var(--f-m);font-size:10.5px}</style>';
          svg.innerHTML = m;
        }

        /* ---- una vuelta del bucle "para siempre" ---- */
        function vuelta(){
          var t, rama, txt;
          if(modo === 0){
            var real = v.luz;
            var leido = v.tiembla ? Math.max(0, Math.min(255, real + tembleque())) : real;
            var antes = encendida;
            if(v.hist){
              if(!encendida && leido < v.umbral) encendida = true;
              else if(encendida && leido > v.apagar) encendida = false;
            } else {
              encendida = leido < v.umbral;
            }
            t = Date.now();
            if(encendida !== antes) cambios.push(t);
            while(cambios.length && t - cambios[0] > 6000) cambios.shift();
            pinta_icono(encendida ? 'lleno' : 'vacio');
            rama = encendida ? 'si' : 'no';
            txt = '<b>nivel de luz = ' + leido + '</b>'
                + (v.tiembla ? ' <i>(hay ' + real + ', pero el sensor tiembla)</i>' : '')
                + ' &middot; &iquest;' + leido + ' &lt; ' + v.umbral + '? &rarr; <b>'
                + (leido < v.umbral ? 'S&Iacute;' : 'NO') + '</b>'
                + (v.hist ? ' &middot; con dos umbrales: ' + (encendida ? 'sigue encendida' : 'sigue apagada') : '')
                + ' &rarr; la farola est&aacute; <b>' + (encendida ? 'encendida' : 'apagada') + '</b>'
                + '<br>Ha cambiado <b>' + cambios.length + '</b> ' + (cambios.length === 1 ? 'vez' : 'veces')
                + ' en los &uacute;ltimos 6 segundos.';
          } else if(modo === 1){
            if(v.temp < v.frio){ rama = 'frio'; pinta_icono('abajo'); }
            else if(v.temp > v.calor){ rama = 'calor'; pinta_icono('arriba'); }
            else { rama = 'bien'; pinta_icono('bien'); }
            txt = '<b>temperatura = ' + v.temp + ' &deg;C</b>'
                + ' &middot; &iquest;' + v.temp + ' &lt; ' + v.frio + '? &rarr; '
                + (v.temp < v.frio ? '<b>S&Iacute;</b>, y ya no se mira nada m&aacute;s'
                                   : 'NO &middot; &iquest;' + v.temp + ' &gt; ' + v.calor + '? &rarr; '
                                     + (v.temp > v.calor ? '<b>S&Iacute;</b>' : 'NO, as&iacute; que se queda con el <i>si no</i>'))
                + ' &rarr; avisa de <b>' + (rama === 'frio' ? 'fr&iacute;o' : (rama === 'calor' ? 'calor' : 'que todo va bien')) + '</b>';
          } else {
            var col = Math.round(v.son * 5 / 255);
            pinta_barra(col);
            rama = v.son > v.uruido ? 'grito' : '';
            if(rama === 'grito') pinta_icono('grito');
            txt = '<b>nivel de sonido = ' + v.son + '</b> &middot; columnas = redondear('
                + v.son + ' &times; 5 &divide; 255) = <b>' + col + '</b>'
                + ' &middot; &iquest;' + v.son + ' &gt; ' + v.uruido + '? &rarr; <b>'
                + (rama === 'grito' ? 'S&Iacute;, avisa' : 'NO') + '</b>';
          }
          pinta();
          prog.innerHTML = bloques(rama);
          evalu.innerHTML = txt;
        }

        /* ---- mandos ---- */
        function num(id, campo, min, max){
          var e = document.getElementById(id);
          if(!e) return;
          e.addEventListener('input', function(){
            var n = parseInt(e.value, 10);
            if(isNaN(n)) return;
            v[campo] = Math.max(min, Math.min(max, n));
          });
        }
        function montaMandos(){
          mandos.innerHTML = MANDOS[modo];
          if(modo === 0){
            var sl = document.getElementById('sx-luz'), sv = document.getElementById('sx-luz-v');
            sl.value = v.luz; sv.textContent = v.luz;
            sl.addEventListener('input', function(){ v.luz = +sl.value; sv.textContent = v.luz; });
            num('sx-umbral', 'umbral', 0, 255);
            num('sx-apagar', 'apagar', 0, 255);
            document.getElementById('sx-tiembla').addEventListener('change', function(e){
              v.tiembla = e.target.checked; cambios = [];
            });
            document.getElementById('sx-hist').addEventListener('change', function(e){
              v.hist = e.target.checked; cambios = [];
            });
          } else if(modo === 1){
            var st = document.getElementById('sx-temp'), tv = document.getElementById('sx-temp-v');
            st.value = v.temp; tv.innerHTML = v.temp + ' &deg;C';
            st.addEventListener('input', function(){ v.temp = +st.value; tv.innerHTML = v.temp + ' &deg;C'; });
            num('sx-frio', 'frio', -5, 45);
            num('sx-calor', 'calor', -5, 45);
          } else {
            var ss = document.getElementById('sx-son'), nv = document.getElementById('sx-son-v');
            ss.value = v.son; nv.textContent = v.son;
            ss.addEventListener('input', function(){ v.son = +ss.value; nv.textContent = v.son; });
            num('sx-uruido', 'uruido', 0, 255);
          }
          pie.innerHTML = PIES[modo];
        }

        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-p]'); if(!b) return;
          seg.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          modo = +b.dataset.p; cambios = []; encendida = false;
          montaMandos(); vuelta();
        });

        montaMandos();
        vuelta();
        reloj = setInterval(vuelta, 100);
      })();
      </script>
'''


# ==========================================================================
# S5 - El robot que busca la lampara
# ==========================================================================
# La mesa mide 120 x 75 cm y se dibuja a 3,6 px/cm, con 14 px de margen.
# El robot mide 12 cm de ancho, sus dos ruedas estan separadas 10 cm (esa es
# la distancia que manda en el giro) y los dos sensores van 6 cm por delante
# del centro, separados 8 cm y mirando 30 grados hacia fuera cada uno.
ROBOT = u'''
      <div class="escena" id="esc-rb">
        <div class="escena-barra">
          <span class="escena-titulo">El robot, suelto en la mesa &middot; elige la regla y su&eacute;ltalo</span>
          <div class="seg" id="seg-rb">
            <button type="button" data-p="0" aria-pressed="true">1 &middot; Si hay luz, avanza</button>
            <button type="button" data-p="1">2 &middot; Gira hacia la luz</button>
            <button type="button" data-p="2">3 &middot; Y para al llegar</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 460 322" id="svg-rb" role="img"
               aria-label="Vista desde arriba de una mesa con una l&aacute;mpara y un robot de dos ruedas que la busca"></svg>
          <div class="rb-bot">
            <button type="button" class="ir" data-a="ir">&#9654; Soltar el robot</button>
            <button type="button" data-a="giro">&#8630; Girar la salida 30&deg;</button>
            <button type="button" data-a="reset">Reiniciar</button>
            <span class="rb-pista">Pulsa en la mesa para mover la l&aacute;mpara</span>
          </div>
          <p class="rb-est" id="est-rb"></p>
        </div>
        <div class="pie" id="pie-rb"></div>
      </div>

      <style>
      .rb-bot{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:10px 0 8px}
      .rb-bot button{font-family:var(--f-m);font-size:12.5px;border:1.5px solid var(--line);
        background:var(--surface);color:var(--ink);border-radius:2px;padding:7px 11px;cursor:pointer}
      .rb-bot button:hover{border-color:var(--goo-azul);color:var(--goo-azul)}
      .rb-bot button.ir{background:var(--goo-azul);border-color:var(--goo-azul);color:#fff}
      .rb-bot button.ir:hover{color:#fff}
      .rb-pista{font-family:var(--f-m);font-size:11.5px;color:var(--ink-soft)}
      .rb-est{font-family:var(--f-m);font-size:12.5px;line-height:1.7;margin:0;color:var(--ink)}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-rb');
        if(!svg) return;
        var caja = document.getElementById('esc-rb');
        var est = document.getElementById('est-rb');
        var pie = document.getElementById('pie-rb');
        var seg = document.getElementById('seg-rb');

        /* --- la mesa, en centimetros --- */
        var ANCHO = 120, ALTO = 75, ESC = 3.6, M = 14;
        function px(c){ return M + c*ESC; }

        /* --- el robot, en centimetros --- */
        var EJE = 10;        /* separacion entre las dos ruedas */
        var ADEL = 6;        /* los sensores van 6 cm por delante del centro */
        var SEP = 4;         /* y separados 4 cm a cada lado */
        var ABRE = 30 * Math.PI / 180;   /* cada sensor mira 30 grados hacia fuera */
        var VMAX = 14;       /* cm por segundo con la rueda a tope */
        var DT = 0.05;       /* cada vuelta del bucle son 50 ms */

        var lampara = {x: 96, y: 18};
        var salida = {x: 16, y: 58, th: 0.25};
        var rob, regla = 0, reloj = null, rastro = [], tiempo = 0, camino = 0, fin = '', cerca = 999;

        function reinicia(){
          rob = {x: salida.x, y: salida.y, th: salida.th};
          rastro = [[rob.x, rob.y]]; tiempo = 0; camino = 0; fin = ''; cerca = 999;
          if(reloj){ clearInterval(reloj); reloj = null; }
          pinta(lee());
        }

        /* --- cuanta luz recibe un sensor: inverso del cuadrado por el coseno
               del angulo. A 20 cm y mirando de frente marca 255. --- */
        function luzEn(sx, sy, nx, ny){
          var dx = lampara.x - sx, dy = lampara.y - sy;
          var r = Math.sqrt(dx*dx + dy*dy);
          if(r < 6) r = 6;
          var cos = (dx*nx + dy*ny) / r;
          if(cos <= 0) return 0;
          return Math.round(Math.min(255, 255 * cos * 400 / (r*r)));
        }

        function lee(){
          var c = Math.cos(rob.th), s = Math.sin(rob.th);
          var ca = Math.cos(ABRE), sa = Math.sin(ABRE);
          /* en esta vista la y crece hacia abajo: la derecha del robot es (-s, c) */
          var iz = {x: rob.x + ADEL*c + SEP*s, y: rob.y + ADEL*s - SEP*c};
          var de = {x: rob.x + ADEL*c - SEP*s, y: rob.y + ADEL*s + SEP*c};
          var nIz = {x: c*ca + s*sa, y: s*ca - c*sa};
          var nDe = {x: c*ca - s*sa, y: s*ca + c*sa};
          return {iz: iz, de: de,
                  Ei: luzEn(iz.x, iz.y, nIz.x, nIz.y),
                  Ed: luzEn(de.x, de.y, nDe.x, nDe.y)};
        }

        /* --- la decision: exactamente lo que el alumno escribiria en bloques --- */
        function decide(L){
          var media = (L.Ei + L.Ed) / 2;
          if(regla === 0){
            if(media > 5) return {vi: 1, vd: 1, q: 'hay luz (media ' + Math.round(media) + ' &gt; 5): avanza recto'};
            return {vi: 0, vd: 0, q: 'no llega luz (media ' + Math.round(media) + ' &le; 5): quieto'};
          }
          if(regla === 2 && media > 190)
            return {vi: 0, vd: 0, para: true, q: 'la media es ' + Math.round(media) + ' &gt; 190: <b>ha llegado</b>'};
          if(L.Ei > L.Ed + 4) return {vi: 0.15, vd: 1, q: L.Ei + ' &gt; ' + L.Ed + ': gira a la <b>izquierda</b>'};
          if(L.Ed > L.Ei + 4) return {vi: 1, vd: 0.15, q: L.Ed + ' &gt; ' + L.Ei + ': gira a la <b>derecha</b>'};
          return {vi: 1, vd: 1, q: 'los dos marcan casi lo mismo: recto'};
        }

        function vuelta(){
          var L = lee(), d = decide(L);
          if(d.para){
            fin = 'llegada';
            cerca = Math.sqrt(Math.pow(rob.x - lampara.x, 2) + Math.pow(rob.y - lampara.y, 2));
            parar(); pinta(L, d); return;
          }
          var v = (d.vi + d.vd) / 2 * VMAX;
          var om = (d.vi - d.vd) * VMAX / EJE;
          rob.th += om * DT;
          rob.x += v * Math.cos(rob.th) * DT;
          rob.y += v * Math.sin(rob.th) * DT;
          tiempo += DT; camino += Math.abs(v) * DT;
          var dl = Math.sqrt(Math.pow(rob.x - lampara.x, 2) + Math.pow(rob.y - lampara.y, 2));
          if(dl < cerca) cerca = dl;
          if(rob.x < 4 || rob.x > ANCHO - 4 || rob.y < 4 || rob.y > ALTO - 4){
            rob.x = Math.max(4, Math.min(ANCHO - 4, rob.x));
            rob.y = Math.max(4, Math.min(ALTO - 4, rob.y));
            fin = 'borde'; parar();
          }
          if(tiempo > 40 && !fin){ fin = 'tiempo'; parar(); }
          var u = rastro[rastro.length - 1];
          if(Math.abs(u[0] - rob.x) + Math.abs(u[1] - rob.y) > 0.8) rastro.push([rob.x, rob.y]);
          pinta(L, d);
        }

        function parar(){ if(reloj){ clearInterval(reloj); reloj = null; } }

        function pinta(L, d){
          var m = '<style>.rb-t{fill:var(--ink-soft);font-family:var(--f-m);font-size:10.5px}</style>';
          /* la mesa */
          m += '<rect x="' + M + '" y="' + M + '" width="' + (ANCHO*ESC) + '" height="' + (ALTO*ESC)
             + '" fill="var(--surface)" stroke="var(--line)" stroke-width="1.5"></rect>';
          var g;
          for(g = 20; g < ANCHO; g += 20)
            m += '<line x1="' + px(g) + '" y1="' + M + '" x2="' + px(g) + '" y2="' + px(ALTO)
               + '" stroke="var(--line-soft)" stroke-width="1"></line>';
          for(g = 20; g < ALTO; g += 20)
            m += '<line x1="' + M + '" y1="' + px(g) + '" x2="' + px(ANCHO) + '" y2="' + px(g)
               + '" stroke="var(--line-soft)" stroke-width="1"></line>';
          m += '<text x="' + px(ANCHO) + '" y="' + (px(ALTO) + 16) + '" text-anchor="end" '
             + 'class="rb-t">la mesa mide 120 &times; 75 cm</text>';
          /* la lampara */
          var lx = px(lampara.x), ly = px(lampara.y);
          m += '<circle cx="' + lx + '" cy="' + ly + '" r="34" fill="#fbbc04" opacity=".13"></circle>';
          m += '<circle cx="' + lx + '" cy="' + ly + '" r="20" fill="#fbbc04" opacity=".18"></circle>';
          m += '<circle cx="' + lx + '" cy="' + ly + '" r="8" fill="#fbbc04" stroke="#c99a05" stroke-width="1.5"></circle>';
          m += '<text x="' + lx + '" y="' + (ly - 15) + '" text-anchor="middle" class="rb-t">l&aacute;mpara</text>';
          /* el rastro */
          if(rastro.length > 1){
            var p = rastro.map(function(q){ return px(q[0]).toFixed(1) + ',' + px(q[1]).toFixed(1); }).join(' ');
            m += '<polyline points="' + p + '" fill="none" stroke="var(--goo-azul)" stroke-width="1.5" '
               + 'stroke-dasharray="3 3" opacity=".7"></polyline>';
          }
          /* el robot, dibujado a escala: chasis de 12 x 14 cm, las dos ruedas
             separadas los 10 cm del eje y los sensores donde de verdad van */
          var gr = rob.th * 180 / Math.PI;
          var LAR = 14*ESC/2, ANC = 12*ESC/2, RU = EJE*ESC/2;
          m += '<g transform="translate(' + px(rob.x).toFixed(1) + ',' + px(rob.y).toFixed(1)
             + ') rotate(' + gr.toFixed(1) + ')">';
          m += '<rect x="' + (-LAR) + '" y="' + (-ANC) + '" width="' + (2*LAR) + '" height="'
             + (2*ANC) + '" rx="4" fill="var(--surface-2)" stroke="var(--ink-soft)" '
             + 'stroke-width="1.5"></rect>';
          [-RU, RU].forEach(function(cy){
            m += '<rect x="-13" y="' + (cy - 2.2).toFixed(1) + '" width="14.4" height="4.4" rx="1" '
               + 'fill="var(--ink)"></rect>';
          });
          m += '<circle cx="' + (-LAR + 6) + '" cy="0" r="3" fill="none" stroke="var(--ink-soft)" '
             + 'stroke-width="1.2"></circle>';
          /* la aleta de carton que separa los dos sensores */
          m += '<line x1="' + (ADEL*ESC - 4) + '" y1="0" x2="' + (LAR + 8) + '" y2="0" '
             + 'stroke="var(--goo-rojo)" stroke-width="2.5"></line>';
          var ci = L ? L.Ei : 0, cd = L ? L.Ed : 0;
          m += '<circle cx="' + (ADEL*ESC) + '" cy="' + (-SEP*ESC) + '" r="5" fill="#fbbc04" opacity="'
             + (0.12 + 0.88*ci/255).toFixed(2) + '" stroke="var(--ink-soft)" stroke-width="1"></circle>';
          m += '<circle cx="' + (ADEL*ESC) + '" cy="' + (SEP*ESC) + '" r="5" fill="#fbbc04" opacity="'
             + (0.12 + 0.88*cd/255).toFixed(2) + '" stroke="var(--ink-soft)" stroke-width="1"></circle>';
          m += '</g>';
          /* las dos lecturas, debajo de la mesa: ahi no tapan nunca nada */
          m += '<text x="' + M + '" y="' + (px(ALTO) + 16) + '" class="rb-t">'
             + 'sensor izquierdo <tspan class="rb-n">' + (L ? L.Ei : 0) + '</tspan>'
             + '  &middot;  sensor derecho <tspan class="rb-n">' + (L ? L.Ed : 0) + '</tspan></text>';
          m += '<style>.rb-n{fill:var(--goo-azul);font-weight:500}</style>';
          svg.innerHTML = m;

          var t = '';
          if(d) t += '<b>' + (L.Ei) + '</b> a la izquierda &middot; <b>' + (L.Ed) + '</b> a la derecha '
                   + '&rarr; ' + d.q + '<br>';
          if(fin === 'llegada')
            t += '<b style="color:var(--goo-verde)">Ha llegado.</b> Se ha parado a <b>'
               + cerca.toFixed(0) + ' cm</b> de la l&aacute;mpara, tras '
               + tiempo.toFixed(1).replace('.', ',')
               + ' s y ' + Math.round(camino) + ' cm de recorrido. No se para porque sepa la '
               + 'distancia: se para porque la luz ha pasado de 190.';
          else if(fin === 'borde' && cerca < 15)
            t += '<b style="color:var(--goo-rojo)">Ha pasado a ' + cerca.toFixed(0)
               + ' cm de la l&aacute;mpara y ha seguido de largo</b> hasta caerse de la mesa. '
               + 'Nadie le hab&iacute;a dicho cu&aacute;ndo parar.';
          else if(fin === 'borde')
            t += '<b style="color:var(--goo-rojo)">Se ha ca&iacute;do de la mesa</b> sin acercarse: '
               + 'lo m&aacute;s cerca que ha estado son ' + cerca.toFixed(0) + ' cm. Llevaba '
               + tiempo.toFixed(1).replace('.', ',') + ' s y ' + Math.round(camino)
               + ' cm de recorrido.';
          else if(fin === 'tiempo')
            t += '<b style="color:var(--goo-rojo)">Cuarenta segundos dando vueltas</b> sin llegar.';
          est.innerHTML = t;
        }

        var PIES = [
          '<b>Regla 1.</b> Un solo n&uacute;mero: la media de los dos sensores, que es exactamente lo '
          + 'que tendr&iacute;as con <b>uno solo</b>. Dice <b>cu&aacute;nta</b> luz hay, pero no dice '
          + '<b>por d&oacute;nde</b>: el robot sale recto hacia donde estuviera mirando.',
          '<b>Regla 2.</b> Ahora se comparan <b>dos</b> entradas entre s&iacute;. Cada vuelta del bucle mide, '
          + 'decide y mueve las ruedas; el resultado cambia la siguiente medida. Eso es un <b>lazo cerrado</b>.',
          '<b>Regla 3.</b> La misma, con una <b>condici&oacute;n de parada</b>. Sin ella el robot llega a la '
          + 'l&aacute;mpara y sigue empujando, porque nadie le ha dicho que ya est&aacute;.'
        ];

        caja.querySelector('[data-a="ir"]').addEventListener('click', function(){
          if(reloj) return;
          if(fin) reinicia();
          reloj = setInterval(vuelta, 50);
        });
        caja.querySelector('[data-a="reset"]').addEventListener('click', reinicia);
        caja.querySelector('[data-a="giro"]').addEventListener('click', function(){
          salida.th += 30 * Math.PI / 180;
          reinicia();
        });
        svg.addEventListener('click', function(e){
          var r = svg.getBoundingClientRect();
          var x = (e.clientX - r.left) / r.width * 460;
          var y = (e.clientY - r.top) / r.height * 322;
          var cx = (x - M) / ESC, cy = (y - M) / ESC;
          if(cx < 2 || cx > ANCHO - 2 || cy < 2 || cy > ALTO - 2) return;
          lampara.x = cx; lampara.y = cy;
          reinicia();
        });
        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-p]'); if(!b) return;
          seg.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          regla = +b.dataset.p; pie.innerHTML = PIES[regla]; reinicia();
        });

        pie.innerHTML = PIES[0];
        reinicia();
      })();
      </script>
'''


# ==========================================================================
# S6 - El dia entero, en cinco segundos
# ==========================================================================
DIA = u'''
      <div class="escena" id="esc-dj">
        <div class="escena-barra">
          <span class="escena-titulo">Un d&iacute;a entero, minuto a minuto &middot; &iquest;merece la pena tu automatismo?</span>
          <div class="seg" id="seg-dj">
            <button type="button" data-n="0" aria-pressed="true">D&iacute;a despejado</button>
            <button type="button" data-n="1">D&iacute;a de tormenta</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 460 250" id="svg-dj" role="img"
               aria-label="Gr&aacute;fica de la luz a lo largo de un d&iacute;a y las horas que est&aacute; encendida la farola con cada estrategia"></svg>
          <div class="dj-mandos">
            <div class="dj-fila"><label>Enciende por debajo de</label>
              <input type="range" id="dj-umbral" min="5" max="200" step="1" value="60">
              <span class="dj-val" id="dj-umbral-v">60</span></div>
            <div class="dj-fila"><label>Potencia de la bombilla</label>
              <input type="number" id="dj-w" min="1" max="500" step="1" value="9"> W
              <label class="corto">Precio del kWh</label>
              <input type="number" id="dj-eur" min="0.01" max="2" step="0.01" value="0.15"> &euro;</div>
          </div>
          <div class="dj-tabla" id="tabla-dj"></div>
        </div>
        <div class="pie" id="pie-dj"></div>
      </div>

      <style>
      .dj-mandos{margin:10px 0 6px}
      .dj-fila{display:flex;align-items:center;gap:9px;flex-wrap:wrap;margin:0 0 8px;
        font-family:var(--f-m);font-size:12.5px;color:var(--ink)}
      .dj-fila label{min-width:160px}
      .dj-fila label.corto{min-width:auto;margin-left:10px}
      .dj-fila input[type="range"]{flex:1 1 140px;min-width:110px;accent-color:var(--goo-azul)}
      .dj-fila input[type="number"]{width:64px;font-family:var(--f-m);font-size:12.5px;padding:4px 5px;
        border:1.5px solid var(--line);border-radius:2px;background:var(--surface);color:var(--ink)}
      .dj-val{font-weight:500;color:var(--goo-azul);min-width:36px;text-align:right}
      .dj-resumen{font-size:13px;color:var(--ink-soft);margin:10px 0 0;line-height:1.55}
      .dj-resumen b{color:var(--ink)}
      .dj-tabla table{width:100%;border-collapse:collapse;font-family:var(--f-m);font-size:12.5px}
      .dj-tabla th,.dj-tabla td{border:1px solid var(--line);padding:6px 8px;text-align:right}
      .dj-tabla th:first-child,.dj-tabla td:first-child{text-align:left}
      .dj-tabla th{background:var(--surface-2);color:var(--ink-soft);font-weight:500}
      .dj-tabla td b{color:var(--ink)}
      .dj-mal{color:var(--goo-rojo)}
      .dj-bien{color:var(--goo-verde)}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-dj');
        if(!svg) return;
        var tabla = document.getElementById('tabla-dj');
        var pie = document.getElementById('pie-dj');
        var seg = document.getElementById('seg-dj');

        var AMANECE = 480, ANOCHECE = 1240;   /* 8:00 y 20:40, en minutos */
        var OSCURO = 40;                      /* por debajo de esto ya no se ve leer */
        var umbral = 60, vatios = 9, precio = 0.15, nublado = 0;

        /* --- la luz de cada minuto del dia --- */
        function luzMin(t){
          if(t < AMANECE || t > ANOCHECE) return 0;
          var base = 255 * Math.sin(Math.PI * (t - AMANECE) / (ANOCHECE - AMANECE));
          if(nublado){
            var n = 0.5 + 0.5 * Math.sin(t/47) * Math.sin(t/113);
            base *= 0.05 + 0.95 * n * n;
          }
          return Math.round(base);
        }

        /* --- las tres estrategias, sobre esos mismos 1.440 datos --- */
        function encendida(modo, t, L){
          if(modo === 0) return true;                       /* siempre */
          if(modo === 1) return (t >= 1200 || t < 420);      /* de 20:00 a 7:00 */
          return L < umbral;                                 /* con sensor */
        }

        function cuenta(){
          var r = [], modo, t;
          for(modo = 0; modo < 3; modo++) r.push({min: 0, aoscuras: 0, tramos: []});
          var previo = [false, false, false];
          for(t = 0; t < 1440; t++){
            var L = luzMin(t);
            for(modo = 0; modo < 3; modo++){
              var on = encendida(modo, t, L);
              if(on) r[modo].min++;
              if(!on && L < OSCURO) r[modo].aoscuras++;
              if(on && !previo[modo]) r[modo].tramos.push([t, t]);
              if(on && previo[modo]) r[modo].tramos[r[modo].tramos.length - 1][1] = t;
              previo[modo] = on;
            }
          }
          r.forEach(function(x){
            x.horas = x.min / 60;
            x.wh = vatios * x.horas;
            x.anio = x.wh / 1000 * precio * 365;
          });
          return r;
        }

        var NOMBRE = ['Encendida siempre', 'Por reloj (20:00 a 7:00)', 'Por sensor de luz'];

        function pinta(){
          var r = cuenta();
          var X0 = 34, X1 = 448, Y0 = 16, Y1 = 118, W = X1 - X0;
          function xt(t){ return X0 + t * W / 1440; }
          var m = '<style>.dj-t{fill:var(--ink-soft);font-family:var(--f-m);font-size:10px}'
                + '.dj-e{fill:var(--ink);font-family:var(--f-m);font-size:10.5px}</style>';
          /* ejes */
          m += '<line x1="' + X0 + '" y1="' + Y1 + '" x2="' + X1 + '" y2="' + Y1
             + '" stroke="var(--line)" stroke-width="1.5"></line>';
          m += '<line x1="' + X0 + '" y1="' + Y0 + '" x2="' + X0 + '" y2="' + Y1
             + '" stroke="var(--line)" stroke-width="1.5"></line>';
          var h;
          for(h = 0; h <= 24; h += 4){
            m += '<line x1="' + xt(h*60) + '" y1="' + Y1 + '" x2="' + xt(h*60) + '" y2="' + (Y1+4)
               + '" stroke="var(--line)" stroke-width="1"></line>';
            m += '<text x="' + xt(h*60) + '" y="' + (Y1+15) + '" text-anchor="middle" class="dj-t">'
               + h + 'h</text>';
          }
          m += '<text x="4" y="' + (Y0+9) + '" class="dj-t">255</text>';
          m += '<text x="10" y="' + Y1 + '" class="dj-t">0</text>';
          m += '<text x="4" y="' + (Y0-4) + '" class="dj-t">luz</text>';
          /* la curva de luz, minuto a minuto */
          var p = '', t;
          for(t = 0; t < 1440; t += 4)
            p += (p ? ' L' : 'M') + xt(t).toFixed(1) + ' ' + (Y1 - luzMin(t)/255*(Y1-Y0)).toFixed(1);
          m += '<path d="' + p + '" fill="none" stroke="var(--goo-amarillo)" stroke-width="2"></path>';
          /* el umbral que ha puesto el alumno, y el limite de "esta oscuro" */
          var yu = Y1 - umbral/255*(Y1-Y0);
          m += '<line x1="' + X0 + '" y1="' + yu.toFixed(1) + '" x2="' + X1 + '" y2="' + yu.toFixed(1)
             + '" stroke="var(--goo-azul)" stroke-width="1.5" stroke-dasharray="5 4"></line>';
          m += '<text x="' + (X0+5) + '" y="' + (yu-4).toFixed(1) + '" class="dj-e" '
             + 'style="fill:var(--goo-azul)">tu umbral: ' + umbral + '</text>';
          var yo = Y1 - OSCURO/255*(Y1-Y0);
          m += '<line x1="' + X0 + '" y1="' + yo.toFixed(1) + '" x2="' + X1 + '" y2="' + yo.toFixed(1)
             + '" stroke="var(--ink-soft)" stroke-width="1" stroke-dasharray="2 3"></line>';
          /* las tres barras */
          var i;
          for(i = 0; i < 3; i++){
            var y = 148 + i*30;
            m += '<text x="4" y="' + (y - 4) + '" class="dj-e">' + NOMBRE[i] + '</text>';
            m += '<rect x="' + X0 + '" y="' + y + '" width="' + W + '" height="14" fill="var(--surface-2)" '
               + 'stroke="var(--line)" stroke-width="1"></rect>';
            r[i].tramos.forEach(function(tr){
              m += '<rect x="' + xt(tr[0]).toFixed(1) + '" y="' + y + '" width="'
                 + Math.max(1, (xt(tr[1]+1) - xt(tr[0]))).toFixed(1) + '" height="14" '
                 + 'fill="var(--goo-azul)" opacity=".75"></rect>';
            });
          }
          m += '<text x="' + X0 + '" y="243" class="dj-t">azul = la farola est&aacute; encendida</text>';
          svg.innerHTML = m;

          var f = '<table><tr><th>Estrategia</th><th>Horas al d&iacute;a</th><th>Wh al d&iacute;a</th>'
                + '<th>&euro; al a&ntilde;o</th><th>A oscuras sin luz</th></tr>';
          for(i = 0; i < 3; i++){
            var osc = r[i].aoscuras;
            f += '<tr><td>' + NOMBRE[i] + '</td>'
               + '<td><b>' + r[i].horas.toFixed(1).replace('.', ',') + '</b></td>'
               + '<td>' + r[i].wh.toFixed(0) + '</td>'
               + '<td><b>' + r[i].anio.toFixed(2).replace('.', ',') + '</b></td>'
               + '<td class="' + (osc > 0 ? 'dj-mal' : 'dj-bien') + '">'
               + (osc > 0 ? osc + ' min' : 'nunca') + '</td></tr>';
          }
          f += '</table>';
          var ahorro = r[0].anio - r[2].anio;
          /* miles con punto, como se escriben en espanol */
          var mil = (ahorro*1000).toFixed(0).replace(/\\B(?=(\\d{3})+(?!\\d))/g, '.');
          f += '<p class="dj-resumen">Con el sensor, cada farola ahorra <b>'
             + ahorro.toFixed(2).replace('.', ',') + ' &euro; al a&ntilde;o</b> frente a dejarla '
             + 'encendida siempre. Un pueblo con mil farolas: <b>'
             + mil + ' &euro; al a&ntilde;o</b>.</p>';
          tabla.innerHTML = f;
          pie.innerHTML = '<b>Los cuatro n&uacute;meros de cada fila salen de recorrer los 1.440 minutos '
            + 'del d&iacute;a</b> y preguntarle a cada estrategia, minuto a minuto, si enciende o no. '
            + 'La &uacute;ltima columna cuenta los minutos en que hab&iacute;a menos de ' + OSCURO
            + ' de luz y la farola estaba apagada: eso es el servicio que <b>no</b> ha dado.';
        }

        var su = document.getElementById('dj-umbral'), sv = document.getElementById('dj-umbral-v');
        su.addEventListener('input', function(){
          umbral = +su.value; sv.textContent = umbral; pinta();
        });
        document.getElementById('dj-w').addEventListener('input', function(e){
          var n = parseFloat(e.target.value);
          if(!isNaN(n) && n > 0){ vatios = n; pinta(); }
        });
        document.getElementById('dj-eur').addEventListener('input', function(e){
          var n = parseFloat(e.target.value);
          if(!isNaN(n) && n > 0){ precio = n; pinta(); }
        });
        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-n]'); if(!b) return;
          seg.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          nublado = +b.dataset.n; pinta();
        });

        pinta();
      })();
      </script>
'''
