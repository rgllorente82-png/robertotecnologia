# -*- coding: utf-8 -*-
"""4.o Tecnologia - Tema 6 - Escenas de las sesiones 1 y 2.

Las dos calculan de verdad; no hay ningun numero escrito a mano en la pantalla.

  BLOQUES_Y_CODIGO (S1)  Ejecuta el MISMO programa en las dos representaciones a
      la vez y con la aritmetica del tipo que elija el alumno: un int de 16 bits
      se desborda de verdad (33.000 -> -32.536) y trunca de verdad (0 + 0,5 = 0).
      La cuenta "ideal" se lleva aparte en coma flotante para poder ense&ntilde;ar la
      diferencia. El Serial imprime como imprime Arduino: dos decimales en float.

  CONVERSOR (S2)  El escalon del conversor A/D. La tension del pin sale de un
      modelo fisico declarado (divisor con LDR, TMP36, sonda de humedad), el
      numero sale de floor(V/Vref*2^n) y la franja de tensiones que dan ese mismo
      numero se dibuja y se escribe. Los decimales que no existen se tachan.

Las clases CSS llevan prefijo propio (c1-, c2-) para no chocar con las del
portal ni con las de las escenas de 2.o. Nada de nombres que empiecen por test-.

Los textos de estas cadenas NO pasan por ningun formateo con %, asi que el
modulo de JavaScript se escribe con un solo %.
"""

# ==========================================================================
# S1 - El mismo programa, en bloques y en codigo
# ==========================================================================
BLOQUES_Y_CODIGO = u'''
      <div class="escena" id="esc-c1">
        <div class="escena-barra">
          <span class="escena-titulo">El mismo programa, en los dos idiomas &middot; ejec&uacute;talo</span>
          <div class="seg" id="seg-c1">
            <button type="button" data-t="int" aria-pressed="true">int</button>
            <button type="button" data-t="long">long</button>
            <button type="button" data-t="float">float</button>
          </div>
        </div>
        <div class="lienzo">
          <div class="c1">
            <div class="c1-col">
              <p class="c1-rot">Bloques &middot; lo que hac&iacute;as en 2.&ordm;</p>
              <svg viewBox="0 0 300 360" id="svg-c1" role="img"
                   aria-label="Pila de bloques con al iniciar y para siempre; se ilumina el bloque que se est&aacute; ejecutando"></svg>
            </div>
            <div class="c1-col">
              <p class="c1-rot">C&oacute;digo &middot; C++ de Arduino</p>
              <div class="c1-cod" id="cod-c1"></div>
              <p class="c1-rot">Monitor serie</p>
              <div class="c1-serie" id="serie-c1"></div>
            </div>
          </div>
          <div class="c1-mandos">
            <div class="c1-fila">
              <label for="c1-paso">cuenta = cuenta +</label>
              <input type="number" id="c1-paso" value="1" step="0.5" min="-2000" max="2000">
              <span class="c1-ayuda">prueba 1, luego 0,5, luego 1000</span>
            </div>
            <div class="c1-fila">
              <button type="button" data-a="paso">Una instrucci&oacute;n</button>
              <button type="button" data-a="vuelta">Una vuelta entera</button>
              <label for="c1-n">Dar</label>
              <input type="number" id="c1-n" value="40" min="1" max="5000" step="1">
              <button type="button" data-a="tanda">vueltas de golpe</button>
              <button type="button" data-a="reinicia">Reiniciar</button>
            </div>
          </div>
          <div class="c1-caja">
            <div class="c1-var" id="var-c1"></div>
            <div class="c1-ram">
              <svg viewBox="0 0 320 44" id="ram-c1" role="img"
                   aria-label="Barra con los 2048 bytes de memoria de la placa y lo que ocupa la variable"></svg>
            </div>
          </div>
          <p class="c1-est" id="est-c1"></p>
        </div>
        <div class="pie" id="pie-c1"></div>
      </div>

      <style>
      .c1{display:flex;gap:18px;flex-wrap:wrap;align-items:flex-start}
      .c1-col{flex:1 1 280px;min-width:250px}
      .c1-rot{font-family:var(--f-m);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;
        color:var(--ink-soft);margin:0 0 6px}
      .c1-col + .c1-col .c1-rot{margin-top:12px}
      .c1-col + .c1-col .c1-rot:first-child{margin-top:0}
      .c1-cod{border:1.5px solid var(--line);border-radius:2px;background:var(--surface);
        font-family:var(--f-m);font-size:12.5px;line-height:1.6;overflow-x:auto}
      .c1-cod .ln{display:flex;gap:10px;padding:1px 8px 1px 0;white-space:pre}
      .c1-cod .ln i{flex:none;width:26px;text-align:right;color:var(--ink-soft);font-style:normal;
        font-size:11px;background:var(--surface-2);padding-right:5px}
      .c1-cod .ln.ev{background:var(--accent-soft)}
      .c1-cod .ln.ev i{background:var(--goo-azul);color:#fff}
      .c1-cod b{color:var(--goo-azul);font-weight:500}
      .c1-serie{border:1.5px solid var(--line);border-radius:2px;background:var(--surface);
        font-family:var(--f-m);font-size:12.5px;line-height:1.55;padding:7px 10px;height:92px;
        overflow-y:auto;color:var(--ink)}
      .c1-serie .vacio{color:var(--ink-soft)}
      .c1-mandos{margin-top:12px}
      .c1-fila{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:0 0 8px;
        font-family:var(--f-m);font-size:12.5px;color:var(--ink)}
      .c1-fila input[type="number"]{width:78px;font-family:var(--f-m);font-size:12.5px;padding:4px 5px;
        border:1.5px solid var(--line);border-radius:2px;background:var(--surface);color:var(--ink)}
      .c1-fila button{font-family:var(--f-m);font-size:12.5px;border:1.5px solid var(--line);
        background:var(--surface);color:var(--ink);border-radius:2px;padding:6px 10px;cursor:pointer}
      .c1-fila button:hover{border-color:var(--goo-azul);color:var(--goo-azul)}
      .c1-ayuda{color:var(--ink-soft)}
      .c1-caja{display:flex;gap:16px;flex-wrap:wrap;align-items:center;margin-top:6px}
      .c1-var{flex:1 1 300px;font-family:var(--f-m);font-size:12.5px;line-height:1.7;color:var(--ink-soft)}
      .c1-var b{color:var(--ink)}
      .c1-var .num{color:var(--goo-azul);font-weight:500}
      .c1-ram{flex:1 1 240px;min-width:220px}
      .c1-est{font-family:var(--f-m);font-size:12.5px;line-height:1.65;color:var(--ink-soft);margin:10px 0 0}
      .c1-est b{color:var(--ink)}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-c1');
        if(!svg) return;
        var caja = document.getElementById('esc-c1');
        var cod = document.getElementById('cod-c1');
        var serie = document.getElementById('serie-c1');
        var vbox = document.getElementById('var-c1');
        var ram = document.getElementById('ram-c1');
        var est = document.getElementById('est-c1');
        var pie = document.getElementById('pie-c1');
        var seg = document.getElementById('seg-c1');
        var campoPaso = document.getElementById('c1-paso');
        var campoN = document.getElementById('c1-n');

        /* ---- los tipos, tal y como son en una placa AVR de 8 bits ---- */
        var TIPOS = {
          'int':   {bytes: 2, min: -32768, max: 32767, entero: true},
          'long':  {bytes: 4, min: -2147483648, max: 2147483647, entero: true},
          'float': {bytes: 4, min: null, max: null, entero: false}
        };
        var RAM_PLACA = 2048;          /* bytes de SRAM de un Arduino UNO */

        /* ---- el programa: una sola lista, dos representaciones ---- */
        var PASOS = [
          {g: 0, blq: 'poner el pin 13 como salida',        ln: 3},
          {g: 0, blq: 'abrir el monitor serie a 9600',      ln: 4},
          {g: 1, blq: 'cambiar cuenta por PASO',            ln: 8, ef: 'suma'},
          {g: 1, blq: 'escribir cuenta en el serie',        ln: 9, ef: 'imprime'},
          {g: 1, blq: 'encender el LED del pin 13',         ln: 10, ef: 'on'},
          {g: 1, blq: 'esperar 200 ms',                     ln: 11},
          {g: 1, blq: 'apagar el LED del pin 13',           ln: 12, ef: 'off'},
          {g: 1, blq: 'esperar 200 ms',                     ln: 13}
        ];

        var tipo = 'int', paso = 1, i = 0;
        var cuenta = 0, ideal = 0, vueltas = 0, led = false, desborde = false;
        var salida = [];

        function T(){ return TIPOS[tipo]; }

        /* "+ 0,5" para el codigo; "0,5" a secas para el rotulo del bloque */
        function textoPaso(){
          return (paso < 0 ? '- ' : '+ ') + String(Math.abs(paso)).replace('.', ',');
        }
        function soloPaso(){ return String(paso).replace('.', ','); }

        /* --- guardar un numero en una variable de este tipo: es AQUI donde el
               tipo deja de ser un adorno y se nota --- */
        function guarda(v){
          var t = T();
          if(!t.entero) return Math.fround(v);        /* float de 4 bytes, de verdad */
          var n = Math.trunc(v);                       /* C++ trunca hacia cero */
          var rango = t.max - t.min + 1;
          var w = ((n - t.min) % rango + rango) % rango + t.min;
          if(w !== n) desborde = true;
          return w;
        }

        /* --- como lo escribe el Serial de Arduino: los float, con 2 decimales --- */
        function comoSerial(v){
          return T().entero ? String(v) : v.toFixed(2);
        }
        function bonito(v){
          return (T().entero ? String(v) : String(Math.round(v * 10000) / 10000)).replace('.', ',');
        }

        function ejecuta(){
          var s = PASOS[i];
          if(s.ef === 'suma'){ ideal = ideal + paso; cuenta = guarda(cuenta + paso); }
          else if(s.ef === 'imprime'){ salida.push(comoSerial(cuenta)); if(salida.length > 400) salida.shift(); }
          else if(s.ef === 'on') led = true;
          else if(s.ef === 'off') led = false;
          i++;
          if(i >= PASOS.length){ i = 2; vueltas++; }   /* setup no se repite */
        }

        function vuelta(){
          var tope = 0;
          do { ejecuta(); tope++; } while(i !== 2 && tope < 40);
        }

        /* --- una tanda: se salta el dibujo y solo hace la aritmetica --- */
        function tanda(n){
          while(i < 2) ejecuta();            /* setup se ejecuta si no lo habia hecho ya */
          for(var k = 0; k < n; k++){
            ideal = ideal + paso;
            cuenta = guarda(cuenta + paso);
            salida.push(comoSerial(cuenta));
            if(salida.length > 400) salida.shift();
            vueltas++;
          }
          i = 2; led = false;
        }

        function reinicia(){
          i = 0; cuenta = 0; ideal = 0; vueltas = 0;
          led = false; desborde = false; salida = [];
          pinta();
        }

        /* ---- dibujo de los bloques: las alturas se calculan, no se copian ---- */
        function pintaBloques(){
          var AN = 214, AL = 26, HUE = 5, X = 16, SANGRIA = 14;
          var m = '<style>.c1b{font:11.5px var(--f-m)}.c1h{font:500 12px var(--f-m)}</style>';
          var y = 14;
          [0, 1].forEach(function(g){
            var col = g === 0 ? 'var(--goo-verde)' : 'var(--goo-azul)';
            var rot = g === 0 ? 'al iniciar' : 'para siempre';
            m += '<rect x="' + X + '" y="' + y + '" width="' + AN + '" height="' + AL
               + '" rx="4" fill="' + col + '"></rect>'
               + '<text x="' + (X + 11) + '" y="' + (y + 17.5) + '" class="c1h" fill="#fff">'
               + rot + '</text>';
            y += AL + HUE;
            PASOS.forEach(function(s, k){
              if(s.g !== g) return;
              var act = (k === i);
              var txt = s.ef === 'suma' ? ('cambiar cuenta por ' + soloPaso()) : s.blq;
              m += '<rect x="' + (X + SANGRIA) + '" y="' + y + '" width="' + (AN - SANGRIA)
                 + '" height="' + AL + '" rx="4" fill="' + (act ? 'var(--accent-soft)' : 'var(--surface)')
                 + '" stroke="' + (act ? 'var(--goo-azul)' : 'var(--line)')
                 + '" stroke-width="' + (act ? 2.2 : 1.3) + '"></rect>'
                 + '<text x="' + (X + SANGRIA + 10) + '" y="' + (y + 17) + '" class="c1b" fill="var(--ink)">'
                 + txt + '</text>';
              y += AL + 4;
            });
            y += 14;
          });
          /* el LED del pin 13, que es lo unico que se ve desde fuera */
          m += '<circle cx="272" cy="30" r="12" fill="' + (led ? 'var(--goo-rojo)' : 'var(--surface-2)')
             + '" stroke="var(--line)" stroke-width="1.5"></circle>'
             + '<text x="272" y="56" text-anchor="middle" class="c1b" fill="var(--ink-soft)">pin 13</text>';
          svg.innerHTML = m;
        }

        function pintaCodigo(){
          var decl = tipo + ' cuenta = 0;';
          var suma = '  cuenta = cuenta ' + textoPaso().replace(',', '.') + ';';
          var L = [decl, '', 'void setup() {', '  pinMode(13, OUTPUT);',
                   '  Serial.begin(9600);', '}', '', 'void loop() {', suma,
                   '  Serial.println(cuenta);', '  digitalWrite(13, HIGH);',
                   '  delay(200);', '  digitalWrite(13, LOW);', '  delay(200);', '}'];
          var activa = PASOS[i] ? PASOS[i].ln : -1;
          var h = '';
          L.forEach(function(t, k){
            var esc = t.replace(/&/g, '&amp;').replace(/</g, '&lt;');
            if(k === 0) esc = '<b>' + tipo + '</b>' + esc.slice(tipo.length);
            h += '<div class="ln' + (k === activa ? ' ev' : '') + '"><i>' + (k + 1) + '</i>'
               + (esc || ' ') + '</div>';
          });
          cod.innerHTML = h;
        }

        function pintaSerie(){
          if(!salida.length){ serie.innerHTML = '<span class="vacio">Todav&iacute;a no ha escrito nada.</span>'; return; }
          serie.innerHTML = salida.slice(-60).join('<br>');
          serie.scrollTop = serie.scrollHeight;
        }

        function pintaRam(){
          var t = T(), AN = 300, X = 10, Y = 9, AL = 16;
          var ancho = Math.max(2.5, AN * t.bytes / RAM_PLACA);
          var caben = Math.floor(RAM_PLACA / t.bytes);
          ram.innerHTML = '<style>.c1r{font:10.5px var(--f-m);fill:var(--ink-soft)}</style>'
            + '<rect x="' + X + '" y="' + Y + '" width="' + AN + '" height="' + AL
            + '" fill="var(--surface-2)" stroke="var(--line)" stroke-width="1.2"></rect>'
            + '<rect x="' + X + '" y="' + Y + '" width="' + ancho.toFixed(2) + '" height="' + AL
            + '" fill="var(--goo-azul)"></rect>'
            + '<text x="' + X + '" y="' + (Y + AL + 11) + '" class="c1r">'
            + t.bytes + ' B de ' + RAM_PLACA + ' &middot; caben ' + caben + ' variables como esta</text>';
        }

        function pintaVar(){
          var t = T();
          var rango = t.entero ? ('de ' + t.min + ' a ' + t.max)
            : 'unos 7 d&iacute;gitos de precisi&oacute;n, no m&aacute;s';
          vbox.innerHTML = '<b>cuenta</b> &middot; tipo <b>' + tipo + '</b> &middot; ocupa <b>'
            + t.bytes + ' bytes</b> &middot; ' + rango
            + '<br>vale <span class="num">' + bonito(cuenta) + '</span>'
            + ' &middot; vueltas del <b>loop</b>: <span class="num">' + vueltas + '</span>';
        }

        function pintaEstado(){
          var t = T(), h = '';
          var dif = ideal - cuenta;
          if(desborde){
            h += '<b style="color:var(--goo-rojo)">Se ha desbordado.</b> Un <b>' + tipo
               + '</b> solo llega a ' + t.max + '. Al pasarse, no da error: <b>da la vuelta</b> '
               + 'y sigue por ' + t.min + '. Por eso cuenta vale ahora ' + bonito(cuenta)
               + ' cuando la suma de verdad iba por ' + String(ideal).replace('.', ',') + '. ';
          }
          if(t.entero && Math.abs(dif) > 0.0001 && !desborde){
            h += '<b style="color:var(--goo-rojo)">La cuenta no es la que pediste.</b> Sumando '
               + textoPaso() + ' ' + vueltas + ' veces deber&iacute;a valer '
               + String(Math.round(ideal * 10000) / 10000).replace('.', ',')
               + ', y vale <b>' + bonito(cuenta) + '</b>: se han perdido '
               + String(Math.round(dif * 10000) / 10000).replace('.', ',') + ' por el camino. '
               + 'No es un fallo de la placa: has dicho que cuenta es un <b>' + tipo
               + '</b>, y en un entero <b>no caben los decimales</b>, as&iacute; que cada suma los tira. ';
          }
          if(!h && vueltas > 0){
            h = 'La cuenta va bien: ' + vueltas + ' vueltas &times; ' + textoPaso()
              + ' = <b>' + bonito(cuenta) + '</b>. ';
          }
          if(!t.entero && vueltas > 0){
            h += 'Fíjate en el serie: un <b>float</b> se imprime con <b>dos decimales</b> '
               + 'salvo que pidas otra cosa.';
          }
          if(!vueltas) h = 'Pulsa <b>una instrucci&oacute;n</b> y sigue a la vez el bloque '
                         + 'iluminado y la l&iacute;nea iluminada: son lo mismo dicho de dos maneras.';
          est.innerHTML = h;
          pie.innerHTML = 'setup() se ejecuta <b>una vez</b> y loop() <b>para siempre</b>: son '
            + '&laquo;al iniciar&raquo; y &laquo;para siempre&raquo; con otro nombre. Lo que no ten&iacute;an '
            + 'los bloques es la primera l&iacute;nea: ah&iacute; hay que decir <b>de qu&eacute; tipo</b> es cada '
            + 'variable, y el tipo decide cu&aacute;ntos bytes ocupa, hasta d&oacute;nde cuenta y si admite '
            + 'decimales.';
        }

        function pinta(){ pintaBloques(); pintaCodigo(); pintaSerie(); pintaRam(); pintaVar(); pintaEstado(); }

        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-t]'); if(!b) return;
          seg.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          tipo = b.dataset.t; reinicia();
        });
        campoPaso.addEventListener('input', function(){
          var v = parseFloat(campoPaso.value);
          paso = isNaN(v) ? 0 : v;
          reinicia();
        });
        caja.querySelector('[data-a="paso"]').addEventListener('click', function(){ ejecuta(); pinta(); });
        caja.querySelector('[data-a="vuelta"]').addEventListener('click', function(){ vuelta(); pinta(); });
        caja.querySelector('[data-a="tanda"]').addEventListener('click', function(){
          var n = parseInt(campoN.value, 10);
          if(!n || n < 1) return;
          tanda(Math.min(n, 5000)); pinta();
        });
        caja.querySelector('[data-a="reinicia"]').addEventListener('click', reinicia);

        reinicia();
      })();
      </script>
'''


# ==========================================================================
# S2 - El conversor A/D y su escalon
# ==========================================================================
CONVERSOR = u'''
      <div class="escena" id="esc-c2">
        <div class="escena-barra">
          <span class="escena-titulo">Del mundo al n&uacute;mero &middot; y del n&uacute;mero otra vez al mundo</span>
          <div class="seg" id="seg-c2">
            <button type="button" data-s="0" aria-pressed="true">Humedad del suelo</button>
            <button type="button" data-s="1">Luz (LDR)</button>
            <button type="button" data-s="2">Temperatura (TMP36)</button>
          </div>
        </div>
        <div class="lienzo">
          <div class="c2">
            <div class="c2-izq">
              <svg viewBox="0 0 440 250" id="svg-c2" role="img"
                   aria-label="Escalera del conversor: tensiones en el eje horizontal y n&uacute;mero entero en el vertical"></svg>
            </div>
            <div class="c2-der">
              <div class="c2-fila">
                <label for="c2-mag" id="lab-c2">Magnitud</label>
                <input type="range" id="c2-mag" min="0" max="1000" step="1" value="500">
                <span class="val" id="val-c2"></span>
              </div>
              <div class="c2-fila">
                <label>Conversor</label>
                <div class="seg" id="bits-c2">
                  <button type="button" data-b="8">8 bits</button>
                  <button type="button" data-b="10" aria-pressed="true">10 bits</button>
                  <button type="button" data-b="12">12 bits</button>
                </div>
              </div>
              <div class="c2-fila">
                <label>Referencia</label>
                <div class="seg" id="vref-c2">
                  <button type="button" data-v="5" aria-pressed="true">5 V</button>
                  <button type="button" data-v="3.3">3,3 V</button>
                  <button type="button" data-v="1.1">1,1 V</button>
                </div>
              </div>
              <div class="c2-fila">
                <label for="c2-dec">Decimales que escribo</label>
                <input type="range" id="c2-dec" min="0" max="6" step="1" value="4">
                <span class="val" id="dec-c2"></span>
              </div>
              <div class="c2-tabla" id="tabla-c2"></div>
            </div>
          </div>
          <p class="c2-lee" id="lee-c2"></p>
        </div>
        <div class="pie" id="pie-c2"></div>
      </div>

      <style>
      .c2{display:flex;gap:18px;flex-wrap:wrap;align-items:flex-start}
      .c2-izq{flex:1 1 390px;min-width:300px}
      .c2-der{flex:1 1 290px;min-width:265px}
      .c2-fila{display:flex;align-items:center;gap:9px;flex-wrap:wrap;margin:0 0 9px;
        font-family:var(--f-m);font-size:12.5px;color:var(--ink)}
      .c2-fila label{min-width:118px}
      .c2-fila input[type="range"]{flex:1 1 120px;min-width:100px;accent-color:var(--goo-azul)}
      .c2-fila .val{font-weight:500;color:var(--goo-azul);min-width:72px;text-align:right}
      .c2-fila .seg button{padding:5px 9px;font-size:11.5px}
      .c2-tabla{border:1.5px solid var(--line);border-radius:2px;background:var(--surface);
        padding:9px 11px;font-family:var(--f-m);font-size:12.5px;line-height:1.75;margin-top:4px}
      .c2-tabla .f{display:flex;justify-content:space-between;gap:10px}
      .c2-tabla .f span:first-child{color:var(--ink-soft)}
      .c2-tabla .f b{color:var(--ink);font-weight:500;text-align:right}
      .c2-tabla .f.top{border-top:1px solid var(--line-soft);margin-top:5px;padding-top:5px}
      .c2-lee{font-family:var(--f-m);font-size:13px;line-height:1.75;color:var(--ink-soft);margin:12px 0 0}
      .c2-lee b{color:var(--ink)}
      .c2-lee .grande{font-size:17px;color:var(--goo-azul);font-weight:500}
      .c2-lee .falso{color:var(--goo-rojo);text-decoration:line-through;opacity:.8}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-c2');
        if(!svg) return;
        var caja = document.getElementById('esc-c2');
        var seg = document.getElementById('seg-c2');
        var segBits = document.getElementById('bits-c2');
        var segVref = document.getElementById('vref-c2');
        var mag = document.getElementById('c2-mag');
        var dec = document.getElementById('c2-dec');
        var lab = document.getElementById('lab-c2');
        var valm = document.getElementById('val-c2');
        var vald = document.getElementById('dec-c2');
        var tabla = document.getElementById('tabla-c2');
        var lee = document.getElementById('lee-c2');
        var pie = document.getElementById('pie-c2');

        var VCC = 5.0;                 /* la placa alimenta el sensor a 5 V */

        /* ---- tres sensores, tres modelos DECLARADOS ----
           Cada uno dice que tension pone en el pin para un valor de la magnitud.
           No son adornos: la escalera se dibuja sobre el numero que salga de aqui. */
        var SENSORES = [
          {
            nom: 'Humedad del suelo', uni: '%', rot: 'Humedad del suelo',
            min: 0, max: 100, paso: 1, ini: 35, dec: 0,
            /* sonda resistiva en divisor: seco -> casi Vcc, empapado -> casi 0 */
            v: function(h){ return VCC * (1 - h / 100) * 0.94 + 0.12; },
            /* la inversa, para volver del numero a la magnitud */
            m: function(v){ return 100 * (1 - (v - 0.12) / (VCC * 0.94)); },
            ley: 'V = 5 &middot; (1 &minus; h/100) &middot; 0,94 + 0,12',
            nota: 'Modelo lineal de una sonda resistiva barata. El sensor de verdad no es tan '
                + 'recto y adem&aacute;s se oxida, pero la cuenta del conversor es la misma.'
          },
          {
            nom: 'Luz', uni: 'lux', rot: 'Luz que le llega',
            min: 0, max: 1000, paso: 1, ini: 520, dec: 0, log: [1, 2000],
            /* LDR (10 kilohmios a 10 lux, gamma 0,7) arriba y 10 kilohmios fijos abajo */
            v: function(E){
              var R = 10000 * Math.pow(Math.max(E, 0.05) / 10, -0.7);
              return VCC * 10000 / (10000 + R);
            },
            m: function(v){
              if(v <= 0.0001 || v >= VCC) return null;
              var R = 10000 * (VCC - v) / v;
              return 10 * Math.pow(R / 10000, -1 / 0.7);
            },
            ley: 'R<sub>LDR</sub> = 10 k&Omega; &middot; (E/10)<sup>&minus;0,7</sup> &nbsp;&middot;&nbsp; '
               + 'V = 5 &middot; 10 k / (10 k + R<sub>LDR</sub>)',
            nota: 'Divisor de tensi&oacute;n con una LDR arriba y 10 k&Omega; abajo. El exponente 0,7 '
                + 'es el de una LDR de sulfuro de cadmio corriente.'
          },
          {
            nom: 'Temperatura', uni: '&deg;C', rot: 'Temperatura del aire',
            min: -40, max: 125, paso: 1, ini: 21, dec: 0,
            v: function(T){ return 0.5 + 0.01 * T; },
            m: function(v){ return (v - 0.5) * 100; },
            ley: 'V = 0,5 V + 0,01 V/&deg;C &middot; T',
            nota: 'Es la hoja de caracter&iacute;sticas del TMP36: 500 mV a 0 &deg;C y 10 mV por grado.'
          }
        ];

        var ns = 0, bits = 10, vref = 5.0;

        function S(){ return SENSORES[ns]; }
        function niveles(){ return Math.pow(2, bits); }
        function pasoV(){ return vref / niveles(); }

        /* valor de la magnitud que pide el mando (con escala log si el sensor lo pide) */
        function magnitud(){
          var s = S(), t = +mag.value / 1000;
          if(s.log){
            var a = Math.log(s.log[0]), b = Math.log(s.log[1]);
            return Math.exp(a + t * (b - a));
          }
          return s.min + t * (s.max - s.min);
        }

        function coma(x, d){ return x.toFixed(d).replace('.', ','); }

        function mide(){
          var s = S(), M = magnitud();
          var V = s.v(M);
          var recorta = false;
          if(V > vref){ V = vref; recorta = true; }        /* el pin no puede pasar de Vref */
          if(V < 0){ V = 0; recorta = true; }
          var N = niveles();
          var bruto = Math.floor(V / vref * N);
          var lect = Math.min(N - 1, Math.max(0, bruto));
          /* la formula que usa todo el mundo con Arduino: el fondo de escala es el ultimo numero */
          var Vrec = lect * vref / (N - 1);
          var Mrec = s.m(Vrec);
          /* la franja de tensiones que dan EXACTAMENTE este mismo numero */
          var baja = lect * pasoV(), alta = (lect + 1) * pasoV();
          if(lect === N - 1) alta = vref;
          /* cuanto vale un escalon en unidades de verdad, aqui. En el ultimo numero
             se mide el escalon anterior: si no, saldria cero y mentiria. */
          var kk = Math.min(lect, N - 2);
          var m0 = s.m(kk * vref / (N - 1));
          var m1 = s.m((kk + 1) * vref / (N - 1));
          var pasoM = (m1 === null || m0 === null) ? null : Math.abs(m1 - m0);
          return {M: M, V: V, lect: lect, Vrec: Vrec, Mrec: Mrec, baja: baja, alta: alta,
                  pasoM: pasoM, recorta: recorta, N: N};
        }

        /* ---- la escalera, dibujada escalon a escalon alrededor del punto ---- */
        function pintaEscalera(r){
          var X0 = 52, Y0 = 26, AN = 360, AL = 168;
          var vent = 9;                                   /* escalones a la vista */
          var k0 = Math.max(0, r.lect - Math.floor(vent / 2));
          if(k0 + vent > r.N) k0 = Math.max(0, r.N - vent);
          var vA = k0 * pasoV(), vB = (k0 + vent) * pasoV();
          var px = function(v){ return X0 + (v - vA) / (vB - vA) * AN; };
          var py = function(k){ return Y0 + AL - (k - k0 + 0.5) / vent * AL; };

          var m = '<style>.c2t{font:10.5px var(--f-m);fill:var(--ink-soft)}'
                + '.c2n{font:500 11px var(--f-m);fill:var(--goo-azul)}</style>';
          /* la franja del numero actual, que es lo que hay que ver */
          m += '<rect x="' + px(r.baja).toFixed(1) + '" y="' + Y0 + '" width="'
             + Math.max(1, px(r.alta) - px(r.baja)).toFixed(1) + '" height="' + AL
             + '" fill="var(--accent-soft)"></rect>';
          /* ejes */
          m += '<path d="M' + X0 + ' ' + Y0 + ' V' + (Y0 + AL) + ' H' + (X0 + AN)
             + '" fill="none" stroke="var(--line)" stroke-width="1.5"></path>';
          /* los escalones */
          var d = '';
          for(var k = k0; k < k0 + vent; k++){
            var xa = px(k * pasoV()), xb = px((k + 1) * pasoV()), y = py(k);
            d += (k === k0 ? 'M' : 'L') + Math.max(X0, xa).toFixed(1) + ' ' + y.toFixed(1)
               + 'L' + Math.min(X0 + AN, xb).toFixed(1) + ' ' + y.toFixed(1);
            if(k + 1 < k0 + vent) d += 'L' + Math.min(X0 + AN, xb).toFixed(1) + ' ' + py(k + 1).toFixed(1);
            m += '<text x="' + (X0 - 7) + '" y="' + (y + 3.5) + '" text-anchor="end" class="c2t">'
               + k + '</text>';
          }
          m += '<path d="' + d + '" fill="none" stroke="var(--goo-azul)" stroke-width="2.2"></path>';
          /* la tension de verdad y el punto en el que cae */
          if(r.V >= vA && r.V <= vB){
            m += '<path d="M' + px(r.V).toFixed(1) + ' ' + Y0 + ' V' + (Y0 + AL)
               + '" stroke="var(--goo-rojo)" stroke-width="1.6" stroke-dasharray="4 3"></path>'
               + '<circle cx="' + px(r.V).toFixed(1) + '" cy="' + py(r.lect).toFixed(1)
               + '" r="5" fill="var(--goo-rojo)"></circle>';
          }
          /* rotulos de los ejes */
          m += '<text x="' + X0 + '" y="' + (Y0 + AL + 15) + '" class="c2t">' + coma(vA, 4) + ' V</text>'
             + '<text x="' + (X0 + AN) + '" y="' + (Y0 + AL + 15) + '" text-anchor="end" class="c2t">'
             + coma(vB, 4) + ' V</text>'
             + '<text x="' + X0 + '" y="' + (Y0 - 10) + '" class="c2t">n&uacute;mero que da analogRead()</text>'
             + '<text x="' + (X0 + AN / 2) + '" y="' + (Y0 + AL + 32) + '" text-anchor="middle" class="c2t">'
             + 'tensi&oacute;n en el pin &middot; un escal&oacute;n = ' + coma(pasoV() * 1000, 2) + ' mV</text>';
          /* la franja, escrita */
          m += '<text x="' + (X0 + AN / 2) + '" y="' + (Y0 + AL + 48) + '" text-anchor="middle" class="c2n">'
             + 'todo lo que caiga entre ' + coma(r.baja, 4) + ' V y ' + coma(r.alta, 4)
             + ' V da el mismo ' + r.lect + '</text>';
          svg.innerHTML = m;
        }

        /* cuantos decimales estan sostenidos por el escalon */
        function decimalesReales(p){
          if(!p || !isFinite(p) || p <= 0) return 0;
          return Math.max(0, Math.ceil(-Math.log(p) / Math.LN10));
        }

        function pinta(){
          var s = S(), r = mide();
          lab.innerHTML = s.rot;
          valm.innerHTML = coma(r.M, s.log ? 0 : s.dec) + ' ' + s.uni;
          vald.innerHTML = dec.value;

          pintaEscalera(r);

          /* map() de Arduino hace la division con ENTEROS, y trunca */
          var exacto = r.lect * 100 / (r.N - 1);
          var mapeado = Math.trunc(r.lect * 100 / (r.N - 1));

          var fil = function(a, b, top){
            return '<div class="f' + (top ? ' top' : '') + '"><span>' + a + '</span><b>' + b + '</b></div>';
          };
          tabla.innerHTML =
              fil('tensi&oacute;n en el pin', coma(r.V, 4) + ' V' + (r.recorta ? ' (recortada)' : ''))
            + fil('escal&oacute;n del conversor', coma(pasoV() * 1000, 3) + ' mV')
            + fil('analogRead() devuelve', r.lect + ' de 0 a ' + (r.N - 1))
            + fil('vuelta a voltios', coma(r.Vrec, 4) + ' V', true)
            + fil('vuelta a ' + s.uni.replace('&deg;C', 'grados'),
                  r.Mrec === null ? '&mdash;' : coma(r.Mrec, 2) + ' ' + s.uni)
            + fil('un escal&oacute;n, en ' + s.uni.replace('&deg;C', 'grados'),
                  r.pasoM === null ? '&mdash;' : coma(r.pasoM, 3) + ' ' + s.uni, true)
            + fil('map(lectura, 0, ' + (r.N - 1) + ', 0, 100) &middot; % de la escala',
                  mapeado + ' %')
            + fil('la misma cuenta sin truncar', coma(exacto, 2) + ' %');

          /* el numero con los decimales que pide el alumno, tachando los que no existen */
          var d = +dec.value, fiables = decimalesReales(r.pasoM);
          var txt = (r.Mrec === null) ? '&mdash;' : coma(r.Mrec, d);
          var pintado = txt;
          if(r.Mrec !== null && d > fiables){
            var corte = txt.length - (d - fiables);
            pintado = txt.slice(0, corte) + '<span class="falso">' + txt.slice(corte) + '</span>';
          }
          var h = 'Tu programa escribir&iacute;a <span class="grande">' + pintado + ' ' + s.uni + '</span>. ';
          if(r.Mrec === null){
            h += 'Con esta referencia el sensor ya no dice nada &uacute;til aqu&iacute;.';
          } else if(d > fiables){
            h += '<b style="color:var(--goo-rojo)">Los ' + (d - fiables) + ' &uacute;ltimos d&iacute;gitos '
               + 'no existen.</b> El conversor salta de ' + coma(r.pasoM, 3) + ' ' + s.uni
               + ' en ' + coma(r.pasoM, 3) + ' ' + s.uni + ', as&iacute; que solo puedes escribir <b>'
               + fiables + '</b> decimal' + (fiables === 1 ? '' : 'es') + '. Lo dem&aacute;s son ceros '
               + 'que ha puesto la divisi&oacute;n, no medidas.';
          } else {
            h += 'Esos decimales <b>s&iacute;</b> los sostiene el sensor: el escal&oacute;n vale '
               + coma(r.pasoM, 3) + ' ' + s.uni + '.';
          }
          if(r.recorta){
            h += ' <b style="color:var(--goo-rojo)">Ojo:</b> la tensi&oacute;n del sensor se sale de la '
               + 'referencia de ' + coma(vref, 1) + ' V. Por encima de ah&iacute; el conversor da siempre '
               + (r.N - 1) + ' y <b>ya no distingue nada</b>.';
          }
          lee.innerHTML = h;
          pie.innerHTML = '<b>' + s.nom + '.</b> ' + s.ley + '. ' + s.nota
            + ' El n&uacute;mero de la pantalla sale de esa f&oacute;rmula y de floor(V / Vref &middot; '
            + r.N + '); no hay ninguna cifra escrita a mano.';
        }

        function cambiaSensor(k){
          ns = k;
          var s = S();
          if(s.log){
            var a = Math.log(s.log[0]), b = Math.log(s.log[1]);
            mag.value = Math.round((Math.log(s.ini) - a) / (b - a) * 1000);
          } else {
            mag.value = Math.round((s.ini - s.min) / (s.max - s.min) * 1000);
          }
          pinta();
        }

        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-s]'); if(!b) return;
          seg.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          cambiaSensor(+b.dataset.s);
        });
        segBits.addEventListener('click', function(e){
          var b = e.target.closest('button[data-b]'); if(!b) return;
          segBits.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          bits = +b.dataset.b; pinta();
        });
        segVref.addEventListener('click', function(e){
          var b = e.target.closest('button[data-v]'); if(!b) return;
          segVref.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          vref = +b.dataset.v; pinta();
        });
        mag.addEventListener('input', pinta);
        dec.addEventListener('input', pinta);

        cambiaSensor(0);
      })();
      </script>
'''
