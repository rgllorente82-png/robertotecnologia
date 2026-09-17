# -*- coding: utf-8 -*-
"""Las tres escenas interactivas de la U7. SVG + JavaScript a mano, sin librerias.

Se separan del texto porque son lo unico del tema que hay que leer como codigo.
Geometria: todas las coordenadas estan calculadas, no puestas a ojo. Cada escena
dice arriba de que tamano es su lienzo y como se reparte.
"""

# ---------------------------------------------------------------------------
# S1 · La misma maquina, otro programa
#
# Lienzo 640 x 344. Tres cajas, con 16 px de margen y 20 px entre columnas:
#   MEMORIA   x  16..258  (242 de ancho)   y  26..332
#                                          6 celdas de 27 px con 5 px de hueco
#   CPU       x 278..624  (346 de ancho)   y  26..226
#   SALIDA    x 278..624                   y 240..332
# Las tres lamparas de fase reparten 346-2*14 = 318 en 3 de 100 con 9 de hueco.
# El texto de la fase se parte a 44 caracteres: el interior de la caja mide
# 318 px y Roboto Mono a 11 px gasta unos 6,6 px por caracter -> 48 caben justos,
# asi que 44 deja margen. Por eso las cadenas de JS llevan \\uXXXX y no entidades
# HTML: una entidad cuenta seis caracteres al medir y solo uno al dibujarse.
# ---------------------------------------------------------------------------
ESCENA_CPU = u'''
      <div class="escena" id="esc-cpu">
        <div class="escena-barra">
          <span class="escena-titulo">La misma m&aacute;quina, otro programa</span>
          <div class="seg" id="seg-cpu-prog">
            <button type="button" data-p="0" aria-pressed="true">Luz fija</button>
            <button type="button" data-p="1">Parpadeo</button>
            <button type="button" data-p="2">Contador</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 344" id="svg-cpu" role="img"
               aria-label="Un procesador ejecutando paso a paso las instrucciones guardadas en la memoria"></svg>
        </div>
        <div class="escena-barra" id="seg-cpu-ctrl-caja">
          <span class="escena-titulo">Controles</span>
          <div class="seg" id="seg-cpu-ctrl">
            <button type="button" data-c="paso">&#9654;&#124; Un paso</button>
            <button type="button" data-c="auto">&#9654;&#9654; Autom&aacute;tico</button>
            <button type="button" data-c="reset">&#8635; Reiniciar</button>
          </div>
        </div>
        <div class="pie" id="pie-cpu"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-cpu');
        if(!svg) return;
        var pie  = document.getElementById('pie-cpu');
        var segP = document.getElementById('seg-cpu-prog');
        var segC = document.getElementById('seg-cpu-ctrl');

        /* Tres programas para UNA sola maquina. El dibujo del procesador no
           cambia nunca: lo unico que cambia es la lista de la izquierda.      */
        var PROGS = [
          {nom:'Luz fija',  ins:['ENCIENDE', 'PARA']},
          {nom:'Parpadeo',  ins:['ENCIENDE', 'ESPERA', 'APAGA', 'ESPERA', 'VUELVE A 1']},
          {nom:'Contador',  ins:['SUMA 1', 'ENCIENDE', 'APAGA', 'VUELVE A 1']}
        ];
        var QUE = {
          'ENCIENDE'  : 'poner la bombilla a 1',
          'APAGA'     : 'poner la bombilla a 0',
          'ESPERA'    : 'no hacer nada durante un paso',
          'SUMA 1'    : 'sumar 1 a la cuenta',
          'VUELVE A 1': 'volver a la instrucci\\u00f3n 1',
          'PARA'      : 'detenerse'
        };
        var FASES = ['BUSCA', 'DESCODIFICA', 'EJECUTA'];

        var prog = 0, pc = 0, fase = 0, luz = 0, cuenta = 0, parado = false, timer = null;

        /* Parte un texto en lineas de como mucho n caracteres, sin cortar palabras.
           Hace falta porque SVG no sabe hacer saltos de linea el solo.           */
        function parte(t, n){
          var pal = t.split(' '), l = [''];
          for(var i = 0; i < pal.length; i++){
            var cand = (l[l.length - 1] + ' ' + pal[i]).trim();
            if(l[l.length - 1] && cand.length > n) l.push(pal[i]);
            else l[l.length - 1] = cand;
          }
          return l;
        }

        function lineas(t, x, y, salto, estilo){
          return parte(t, 44).slice(0, 2).map(function(s, i){
            return '<text x="' + x + '" y="' + (y + i * salto) + '" class="rotulo-svg" style="'
                 + estilo + '">' + s + '</text>';
          }).join('');
        }

        function caja(x, y, w, h, etq){
          return '<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="2" '
               + 'fill="var(--surface)" stroke="var(--line)" stroke-width="1.5"></rect>'
               + '<text x="'+(x+10)+'" y="'+(y+16)+'" class="rotulo-svg">'+etq+'</text>';
        }

        function pinta(){
          var P = PROGS[prog], m = '';

          /* ---- columna de memoria: una celda por instruccion ---- */
          m += caja(16, 26, 242, 306, 'MEMORIA');
          for(var i = 0; i < P.ins.length; i++){
            var y = 46 + i * 32;
            var activa = (i === pc && !parado);
            m += '<rect x="28" y="'+y+'" width="218" height="27" rx="2" fill="'
               + (activa ? 'var(--accent-soft)' : 'var(--surface-2)')
               + '" stroke="'+(activa ? 'var(--goo-azul)' : 'var(--line)')+'" stroke-width="'
               + (activa ? '2' : '1')+'"></rect>';
            m += '<text x="38" y="'+(y+18)+'" class="rotulo-svg" style="font-size:11px">'+(i+1)+'</text>';
            m += '<text x="58" y="'+(y+18)+'" class="rotulo-svg" style="font-size:12px;fill:var(--ink)'
               + (activa ? ';font-weight:500' : '')+'">'+P.ins[i]+'</text>';
          }
          m += '<text x="28" y="322" class="rotulo-svg" style="font-size:10.5px">'
             + 'software \\u00b7 se cambia sin tocar nada</text>';

          /* ---- el procesador ---- */
          m += caja(278, 26, 346, 200, 'PROCESADOR (CPU)');
          for(var f = 0; f < 3; f++){
            var fx = 292 + f * 109, on = (f === fase && !parado);
            m += '<rect x="'+fx+'" y="54" width="100" height="26" rx="2" fill="'
               + (on ? 'var(--goo-azul)' : 'var(--surface-2)')+'" stroke="'
               + (on ? 'var(--goo-azul)' : 'var(--line)')+'" stroke-width="1.5"></rect>';
            m += '<text x="'+(fx+50)+'" y="71" text-anchor="middle" class="rotulo-svg" '
               + 'style="font-size:9.5px;font-weight:500;fill:'+(on ? '#fff' : 'var(--ink-soft)')
               + '">'+FASES[f]+'</text>';
          }
          /* El ciclo vuelve al principio: de debajo de EJECUTA (centro x=560) a
             debajo de BUSCA (centro x=342), con la punta de flecha hacia arriba. */
          m += '<path d="M560 82 v12 H342 v-6" fill="none" stroke="var(--line)" '
             + 'stroke-width="1.5" stroke-dasharray="4 3"></path>';
          m += '<path d="M342 79 l-5 9 h10 Z" fill="var(--line)"></path>';
          m += '<text x="451" y="118" text-anchor="middle" class="rotulo-svg" style="font-size:10px">'
             + 'y vuelta a empezar, sin parar</text>';

          m += '<text x="292" y="142" class="rotulo-svg" style="font-size:11.5px;fill:var(--ink)">'
             + 'Contador de programa \\u00b7 PC = '+(parado ? '\\u2014' : (pc+1))+'</text>';
          m += '<text x="292" y="164" class="rotulo-svg" style="font-size:11.5px;fill:var(--ink)">'
             + 'Instrucci\\u00f3n en curso \\u00b7 '+(parado ? 'ninguna' : P.ins[pc])+'</text>';
          m += lineas(parado ? 'La m\\u00e1quina se ha detenido.'
                             : ('Ahora ' + FASES[fase].toLowerCase() + ': ' + textoFase()),
                      292, 186, 15, 'font-size:11px');
          m += '<text x="292" y="218" class="rotulo-svg" style="font-size:10.5px">'
             + 'hardware \\u00b7 siempre el mismo, no cambia nunca</text>';

          /* ---- salida: la bombilla y la cuenta ---- */
          m += caja(278, 240, 346, 92, 'SALIDA');
          var cx = 322, cy = 296;
          if(luz){
            for(var r = 0; r < 8; r++){
              var a = r * Math.PI / 4;
              m += '<path d="M'+(cx+Math.cos(a)*26).toFixed(1)+' '+(cy+Math.sin(a)*26).toFixed(1)
                 + ' L'+(cx+Math.cos(a)*33).toFixed(1)+' '+(cy+Math.sin(a)*33).toFixed(1)
                 + '" stroke="var(--goo-amarillo)" stroke-width="2.5" stroke-linecap="round"></path>';
            }
          }
          m += '<circle cx="'+cx+'" cy="'+cy+'" r="20" fill="'
             + (luz ? 'var(--goo-amarillo)' : 'var(--surface-2)')
             + '" stroke="var(--line)" stroke-width="1.5"></circle>';
          m += '<path d="M'+(cx-7)+' '+(cy+4)+' q7 -14 14 0" fill="none" stroke="'
             + (luz ? '#8a6d00' : 'var(--line)')+'" stroke-width="2"></path>';
          m += '<text x="362" y="301" class="rotulo-svg" style="font-size:11.5px;fill:var(--ink)">'
             + 'bombilla: '+(luz ? '1' : '0')+'</text>';
          m += '<text x="492" y="286" class="rotulo-svg" style="font-size:11px">CUENTA</text>';
          m += '<text x="492" y="318" class="rotulo-svg" '
             + 'style="font-size:26px;fill:var(--ink);font-weight:500">'+cuenta+'</text>';

          svg.innerHTML = m;
          pie.innerHTML = parado
            ? '<b>Programa terminado.</b> Cambia de programa ah&iacute; arriba: ver&aacute;s que el dibujo del '
              + 'procesador no cambia ni un p&iacute;xel. Lo &uacute;nico distinto es la lista de la memoria.'
            : 'La CPU repite tres pasos sin parar: <b>busca</b> la instrucci&oacute;n que toca, la '
              + '<b>descodifica</b> para saber qu&eacute; pide, y la <b>ejecuta</b>. Dale a &laquo;un paso&raquo; '
              + 'tres veces y habr&aacute;s ejecutado una instrucci&oacute;n entera.';
        }

        function textoFase(){
          var ins = PROGS[prog].ins[pc];
          if(fase === 0) return 'traer de la memoria la instrucci\\u00f3n ' + (pc+1);
          if(fase === 1) return 'es ' + ins + ', o sea ' + QUE[ins];
          return QUE[ins];
        }

        function paso(){
          if(parado) return;
          var P = PROGS[prog], ins = P.ins[pc];
          if(fase < 2){ fase++; pinta(); return; }
          /* fase EJECUTA: se aplica el efecto y se decide la siguiente instruccion */
          if(ins === 'ENCIENDE') luz = 1;
          else if(ins === 'APAGA') luz = 0;
          else if(ins === 'SUMA 1') cuenta++;
          if(ins === 'PARA'){ parado = true; para(); pinta(); return; }
          pc = (ins === 'VUELVE A 1') ? 0 : pc + 1;
          if(pc >= P.ins.length) pc = 0;
          fase = 0;
          pinta();
        }

        function para(){
          if(timer){ clearInterval(timer); timer = null; }
          var b = segC.querySelector('[data-c="auto"]');
          b.setAttribute('aria-pressed', 'false');
          b.innerHTML = '\\u25b6\\u25b6 Autom\\u00e1tico';
        }

        function reinicia(){
          para(); pc = 0; fase = 0; luz = 0; cuenta = 0; parado = false; pinta();
        }

        segP.addEventListener('click', function(e){
          var b = e.target.closest('button[data-p]'); if(!b) return;
          segP.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
          prog = +b.dataset.p; reinicia();
        });
        segC.addEventListener('click', function(e){
          var b = e.target.closest('button[data-c]'); if(!b) return;
          if(b.dataset.c === 'paso'){ para(); paso(); }
          else if(b.dataset.c === 'reset'){ reinicia(); }
          else {
            if(timer){ para(); }
            else {
              b.setAttribute('aria-pressed', 'true');
              b.innerHTML = '\\u25a0 Parar';
              timer = setInterval(paso, 520);
            }
          }
        });
        pinta();
      })();
      </script>
'''


# ---------------------------------------------------------------------------
# S2 · La mesa y la estanteria
#
# Lienzo 640 x 330.
#   MESA (RAM)      x  16..312 (296)  6 huecos: 2 columnas de 130 x 62,
#                                     x = 30 y 168 ; y = 74, 146, 218
#   ESTANTERIA      x 332..624 (292)  rejilla 12 x 8 de cuadros de 20 px
#                                     con 2 px de hueco: 12*22 = 264 <= 268
# Tiempos usados (ordenes de magnitud tipicos, ns):
#   RAM 80 ns · SSD 100.000 ns (0,1 ms) · disco duro 10.000.000 ns (10 ms)
# ---------------------------------------------------------------------------
ESCENA_RAM = u'''
      <div class="escena" id="esc-ram">
        <div class="escena-barra">
          <span class="escena-titulo">La mesa de trabajo y la estanter&iacute;a</span>
          <div class="seg" id="seg-ram">
            <button type="button" data-r="abre">+ Abrir un programa</button>
            <button type="button" data-r="cierra">&#8722; Cerrar uno</button>
            <button type="button" data-r="apaga">&#9211; Apagar y encender</button>
            <button type="button" data-r="reset">&#8635; Reiniciar</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 330" id="svg-ram" role="img"
               aria-label="Comparaci&oacute;n entre la memoria RAM, con pocos huecos y muy r&aacute;pida, y el almacenamiento, enorme y lento"></svg>
        </div>
        <div class="pie" id="pie-ram"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-ram');
        if(!svg) return;
        var pie = document.getElementById('pie-ram');
        var seg = document.getElementById('seg-ram');

        var HUECOS = 6;              /* huecos de la mesa */
        var T_RAM  = 80;             /* ns */
        var T_SSD  = 100000;         /* ns  = 0,1 ms */
        var NOMBRES = ['Navegador', 'Pesta\\u00f1a 1', 'Pesta\\u00f1a 2', 'Editor', 'M\\u00fasica',
                       'Pesta\\u00f1a 3', 'Pesta\\u00f1a 4', 'Pesta\\u00f1a 5', 'V\\u00eddeo', 'Juego'];
        var COLOR = ['var(--goo-azul)', 'var(--goo-verde)', 'var(--goo-amarillo)',
                     'var(--goo-rojo)', 'var(--goo-azul)', 'var(--goo-verde)'];
        var abiertos = 0, apagado = false;

        function medio(){
          if(abiertos === 0) return T_RAM;
          var dentro = Math.min(abiertos, HUECOS), fuera = abiertos - dentro;
          return (dentro * T_RAM + fuera * T_SSD) / abiertos;
        }

        function caja(x, y, w, h, etq, sub){
          return '<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="2" fill="var(--surface)" '
               + 'stroke="var(--line)" stroke-width="1.5"></rect>'
               + '<text x="'+(x+12)+'" y="'+(y+18)+'" class="rotulo-svg" '
               + 'style="font-size:11.5px;fill:var(--ink);font-weight:500">'+etq+'</text>'
               + '<text x="'+(x+12)+'" y="'+(y+34)+'" class="rotulo-svg" style="font-size:10.5px">'+sub+'</text>';
        }

        function pinta(){
          var m = '', i, x, y;
          var dentro = apagado ? 0 : Math.min(abiertos, HUECOS);
          var fuera  = apagado ? 0 : Math.max(0, abiertos - HUECOS);

          /* ---- la mesa: la RAM ---- */
          m += caja(16, 26, 296, 288, 'MESA DE TRABAJO &#183; memoria RAM',
                    '6 huecos &#183; 80 ns &#183; se borra al apagar');
          for(i = 0; i < HUECOS; i++){
            x = 30 + (i % 2) * 138;
            y = 74 + Math.floor(i / 2) * 72;
            var lleno = i < dentro;
            m += '<rect x="'+x+'" y="'+y+'" width="130" height="62" rx="2" fill="'
               + (lleno ? COLOR[i % COLOR.length] : 'var(--surface-2)')
               + '" stroke="var(--line)" stroke-width="1.5" '
               + (lleno ? '' : 'stroke-dasharray="4 3"')+'></rect>';
            if(lleno){
              m += '<text x="'+(x+65)+'" y="'+(y+30)+'" text-anchor="middle" class="rotulo-svg" '
                 + 'style="font-size:11.5px;fill:#fff;font-weight:500">'+NOMBRES[i]+'</text>';
              m += '<text x="'+(x+65)+'" y="'+(y+46)+'" text-anchor="middle" class="rotulo-svg" '
                 + 'style="font-size:10px;fill:#fff;opacity:.9">80 ns</text>';
            } else {
              m += '<text x="'+(x+65)+'" y="'+(y+36)+'" text-anchor="middle" class="rotulo-svg" '
                 + 'style="font-size:10.5px">hueco libre</text>';
            }
          }

          /* ---- la estanteria: el almacenamiento ---- */
          m += caja(332, 26, 292, 288, 'ESTANTER&#205;A &#183; almacenamiento',
                    'enorme &#183; 0,1 ms &#183; no se borra nunca');
          for(i = 0; i < 96; i++){
            x = 344 + (i % 12) * 22;
            y = 52 + Math.floor(i / 12) * 22;
            var ocupado = (i % 3 !== 2);            /* la estanteria esta casi llena */
            m += '<rect x="'+x+'" y="'+y+'" width="20" height="20" rx="1" fill="'
               + (ocupado ? 'var(--line)' : 'var(--surface)')
               + '" stroke="var(--line)" stroke-width="1"></rect>';
          }
          /* lo que no cabe en la mesa y ha tenido que bajar a la estanteria */
          for(i = 0; i < fuera && i < 4; i++){
            x = 344 + i * 68;
            m += '<rect x="'+x+'" y="234" width="64" height="44" rx="2" fill="var(--goo-rojo)" '
               + 'stroke="var(--goo-rojo)" stroke-width="1.5"></rect>';
            m += '<text x="'+(x+32)+'" y="252" text-anchor="middle" class="rotulo-svg" '
               + 'style="font-size:9.5px;fill:#fff;font-weight:500">'+NOMBRES[HUECOS+i]+'</text>';
            m += '<text x="'+(x+32)+'" y="268" text-anchor="middle" class="rotulo-svg" '
               + 'style="font-size:9px;fill:#fff;opacity:.95">0,1 ms</text>';
          }
          if(fuera > 0){
            m += '<text x="344" y="300" class="rotulo-svg" style="font-size:10.5px;fill:var(--goo-rojo)">'
               + 'No caben en la mesa: se buscan aqu\\u00ed.</text>';
          }

          /* ---- flecha entre las dos cajas ---- */
          m += '<path d="M312 168 h20" stroke="var(--ink-soft)" stroke-width="1.5" '
             + 'stroke-dasharray="3 3" fill="none"></path>';

          svg.innerHTML = m;

          var t = medio(), veces = t / T_RAM;
          var txt;
          if(apagado){
            txt = '<b>Has apagado y vuelto a encender.</b> La mesa est&aacute; vac&iacute;a: la RAM es '
                + '<b>vol&aacute;til</b>, necesita corriente para acordarse y al cortarla pierde todo lo que '
                + 'ten&iacute;a. La estanter&iacute;a sigue igual de llena: el almacenamiento <b>no</b> es vol&aacute;til. '
                + 'Por eso lo que no hab&iacute;as guardado ya no est&aacute;.';
          } else if(abiertos === 0){
            txt = 'Nada abierto. Ve abriendo programas y mira qu&eacute; pasa cuando se acaben los huecos.';
          } else if(fuera === 0){
            txt = 'Abiertos: <b>'+abiertos+' de 6</b>. Todo cabe en la mesa, as&iacute; que el procesador tiene '
                + 'todo a mano: <b>80 ns</b> por acceso. El ordenador va fino.';
          } else {
            txt = 'Abiertos: <b>'+abiertos+'</b>, y en la mesa solo caben 6. El sistema baja '+fuera
                + ' a la estanter&iacute;a y los sube cuando hacen falta. Tiempo medio de acceso: '
                + '<b>'+Math.round(t).toLocaleString('es-ES')+' ns</b>, es decir <b>'+Math.round(veces)
                + ' veces m&aacute;s lento</b>. Esto es exactamente lo que notas cuando el ordenador se arrastra.';
          }
          pie.innerHTML = txt + '<br><span style="font-size:12.5px">Modelo simplificado: en un ordenador '
            + 'de verdad no todo se vuelve lento a la vez, y el intercambio se hace por trozos, no por '
            + 'programas enteros. La idea s&iacute; es exacta: cuando la mesa se llena hay que ir a la '
            + 'estanter&iacute;a, y eso cuesta <b>miles de veces m&aacute;s</b>.</span>';
        }

        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-r]'); if(!b) return;
          var c = b.dataset.r;
          if(c === 'abre'){ apagado = false; if(abiertos < 10) abiertos++; }
          else if(c === 'cierra'){ apagado = false; if(abiertos > 0) abiertos--; }
          else if(c === 'apaga'){ apagado = true; abiertos = 0; }
          else { apagado = false; abiertos = 0; }
          pinta();
        });
        pinta();
      })();
      </script>
'''


# ---------------------------------------------------------------------------
# S3 · Ocho interruptores
#
# Lienzo 640 x 306.
#   Ocho interruptores: margen 30 a cada lado -> 580 utiles / 8 = 72,5 por celda.
#   Cada uno mide 60 de ancho, asi que el hueco es de 12,5. x_i = 30 + 72,5*i
#   Caja de lecturas: x 30..610, y 196..296, partida en tres columnas iguales
#   de 193,3 (los rotulos van centrados en 126,7 / 320 / 513,3).
# ---------------------------------------------------------------------------
ESCENA_BITS = u'''
      <div class="escena" id="esc-bits">
        <div class="escena-barra">
          <span class="escena-titulo">Ocho interruptores, tres significados</span>
          <div class="seg" id="seg-bits">
            <button type="button" data-b="cero">Todos a 0</button>
            <button type="button" data-b="reto">&#9873; Reto</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 306" id="svg-bits" role="img"
               aria-label="Ocho interruptores que forman un byte, le&iacute;do como n&uacute;mero, como letra y como nivel de gris"></svg>
        </div>
        <div class="pie" id="pie-bits"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-bits');
        if(!svg) return;
        var pie = document.getElementById('pie-bits');
        var seg = document.getElementById('seg-bits');

        var bits = [0,0,0,0,0,0,0,0];      /* bits[0] es el de peso 128 */
        var PESOS = [128, 64, 32, 16, 8, 4, 2, 1];
        var objetivo = null;

        function valor(){
          var v = 0;
          for(var i = 0; i < 8; i++) if(bits[i]) v += PESOS[i];
          return v;
        }

        /* ASCII imprimible: del 32 al 126. Lo de fuera no se dibuja. */
        function letra(v){
          if(v === 32) return ['espacio', true];
          if(v === 10) return ['salto de l\\u00ednea', true];
          if(v < 32 || v > 126) return ['no imprimible', false];
          var c = String.fromCharCode(v);
          return [(c === '<' ? '&#60;' : c === '&' ? '&#38;' : c), true];
        }

        function pinta(){
          var v = valor(), m = '', i;

          m += '<text x="30" y="24" class="rotulo-svg">PULSA LOS INTERRUPTORES</text>';
          m += '<text x="610" y="24" text-anchor="end" class="rotulo-svg" style="font-size:10.5px">'
             + 'cerrado = pasa corriente = 1</text>';

          for(i = 0; i < 8; i++){
            var x = 30 + i * 72.5, on = bits[i];
            m += '<g class="bit-sw" data-i="'+i+'" style="cursor:pointer">';
            m += '<rect x="'+x.toFixed(1)+'" y="36" width="60" height="118" rx="3" fill="'
               + (on ? 'var(--accent-soft)' : 'var(--surface-2)')+'" stroke="'
               + (on ? 'var(--goo-azul)' : 'var(--line)')+'" stroke-width="'+(on ? 2 : 1.5)+'"></rect>';
            /* peso de la posicion */
            m += '<text x="'+(x+30).toFixed(1)+'" y="54" text-anchor="middle" class="rotulo-svg" '
               + 'style="font-size:11px">'+PESOS[i]+'</text>';
            /* Interruptor con la simbologia de la unidad de electricidad:
               palanca TUMBADA y tocando el otro borne = cerrado = pasa = 1;
               palanca LEVANTADA, con hueco de aire = abierto = no pasa = 0.
               Los dos bornes van en x = bx y bx+18, ambos a y = 112.         */
            var bx = x + 21, col = on ? 'var(--goo-azul)' : 'var(--ink-soft)';
            m += '<path d="M'+(x+6).toFixed(1)+' 112 H'+(bx-3.5).toFixed(1)+'" stroke="'+col+'" '
               + 'stroke-width="2"></path>';
            m += '<path d="M'+(bx+21.5).toFixed(1)+' 112 H'+(x+54).toFixed(1)+'" stroke="'+col+'" '
               + 'stroke-width="2"></path>';
            /* La palanca mide 18 y pivota en el borne izquierdo: cerrada llega al
               otro borne, y abierta gira 35 grados -> (18*cos35, 18*sin35) =
               (14,7 ; 10,3), o sea que se queda a 3,3 px del borne. Se ve el hueco. */
            m += '<path d="M'+bx.toFixed(1)+' 112 L'+(on ? (bx+18).toFixed(1)+' 112'
                                                         : (bx+14.7).toFixed(1)+' 101.7')+'" stroke="'
               + col+'" stroke-width="3" stroke-linecap="round"></path>';
            m += '<circle cx="'+bx.toFixed(1)+'" cy="112" r="3.5" fill="'+col+'"></circle>';
            m += '<circle cx="'+(bx+18).toFixed(1)+'" cy="112" r="3.5" fill="'+col+'"></circle>';
            /* el bit que sale de ahi */
            m += '<text x="'+(x+30).toFixed(1)+'" y="146" text-anchor="middle" class="rotulo-svg" '
               + 'style="font-size:20px;font-weight:500;fill:'
               + (on ? 'var(--goo-azul)' : 'var(--ink-soft)')+'">'+(on ? 1 : 0)+'</text>';
            m += '</g>';
          }

          /* el byte escrito, en dos grupos de cuatro para poder leerlo */
          var b = bits.join('');
          m += '<text x="320" y="182" text-anchor="middle" class="rotulo-svg" '
             + 'style="font-size:17px;letter-spacing:.22em;fill:var(--ink);font-weight:500">'
             + b.slice(0,4)+' '+b.slice(4)+'</text>';

          /* las tres lecturas del mismo byte */
          m += '<rect x="30" y="196" width="580" height="100" rx="2" fill="var(--surface)" '
             + 'stroke="var(--line)" stroke-width="1.5"></rect>';
          m += '<path d="M223.3 196 v100 M416.7 196 v100" stroke="var(--line)" stroke-width="1"></path>';

          m += '<text x="126.7" y="220" text-anchor="middle" class="rotulo-svg" '
             + 'style="font-size:10px">COMO N&#218;MERO</text>';
          m += '<text x="126.7" y="262" text-anchor="middle" class="rotulo-svg" '
             + 'style="font-size:30px;fill:var(--ink);font-weight:500">'+v+'</text>';
          m += '<text x="126.7" y="284" text-anchor="middle" class="rotulo-svg" '
             + 'style="font-size:10.5px">de 0 a 255</text>';

          var L = letra(v);
          m += '<text x="320" y="220" text-anchor="middle" class="rotulo-svg" '
             + 'style="font-size:10px">COMO LETRA (ASCII)</text>';
          m += '<text x="320" y="264" text-anchor="middle" class="rotulo-svg" style="font-size:'
             + (L[0].length > 2 ? '15' : '32')+'px;fill:'+(L[1] ? 'var(--ink)' : 'var(--ink-soft)')
             + ';font-weight:500">'+L[0]+'</text>';
          m += '<text x="320" y="284" text-anchor="middle" class="rotulo-svg" '
             + 'style="font-size:10.5px">tabla ASCII</text>';

          m += '<text x="513.3" y="220" text-anchor="middle" class="rotulo-svg" '
             + 'style="font-size:10px">COMO NIVEL DE GRIS</text>';
          m += '<rect x="485.3" y="230" width="56" height="40" rx="2" fill="rgb('+v+','+v+','+v+')" '
             + 'stroke="var(--line)" stroke-width="1.5"></rect>';
          m += '<text x="513.3" y="284" text-anchor="middle" class="rotulo-svg" '
             + 'style="font-size:10.5px">0 negro &#183; 255 blanco</text>';

          svg.innerHTML = m;

          var txt;
          if(objetivo !== null && v === objetivo){
            txt = '<b>&#161;Eso es!</b> Has formado el ' + objetivo + '. Prueba otro reto, o fíjate en '
                + 'una cosa: solo hay <b>una</b> manera de formar cada n&uacute;mero. Ocho interruptores dan '
                + '<b>256</b> combinaciones distintas, ni una m&aacute;s ni una menos.';
          } else if(objetivo !== null){
            txt = 'Reto: forma el <b>' + objetivo + '</b>. Vas por el ' + v + '. Truco: empieza por el '
                + 'interruptor m&aacute;s gordo que quepa y sigue con los siguientes.';
          } else {
            txt = 'El mismo byte, <b>tres lecturas distintas</b>. Los ocho interruptores no cambian; lo que '
                + 'cambia es el <b>acuerdo</b> sobre c&oacute;mo hay que leerlos. Prueba el 65, el 97 y el 32.';
          }
          pie.innerHTML = txt;
        }

        svg.addEventListener('click', function(e){
          var g = e.target.closest('.bit-sw'); if(!g) return;
          var i = +g.dataset.i; bits[i] = bits[i] ? 0 : 1; pinta();
        });
        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-b]'); if(!b) return;
          if(b.dataset.b === 'cero'){ bits = [0,0,0,0,0,0,0,0]; objetivo = null; }
          else { objetivo = 1 + Math.floor(Math.random() * 254); bits = [0,0,0,0,0,0,0,0]; }
          pinta();
        });
        pinta();
      })();
      </script>
'''
