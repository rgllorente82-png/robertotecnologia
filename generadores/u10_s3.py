# -*- coding: utf-8 -*-
"""2.o TyD - Tema 10 - Sesion 3: la placa de verdad (micro:bit).

Hasta aqui todo pasaba dentro de la pantalla. Esta sesion da el salto al mundo
fisico, y lo hace con una placa simulada en la propia pagina: 25 LED, los
botones A y B, y tres programas que se ejecutan de verdad, con el bloque que
se esta ejecutando marcado.

El simulador no es un adorno: permite que el alumno pruebe antes de tener la
placa delante, y que quien no tenga placa en casa pueda hacer los deberes.
"""
from unidad_base import bloque, ficha, pregunta

# --------------------------------------------------------------------------
# 00 - Reto
# --------------------------------------------------------------------------
RETO = u'''
      <p>Tu robot de las dos sesiones anteriores hace lo que le mandas. Pero pru&eacute;balo con esto:</p>
      <div class="aviso">
        <span class="n-tag">El encargo</span>
        Haz que tu programa <b>encienda una luz de verdad</b>. O que sepa si hace fr&iacute;o. O que se
        entere de que alguien ha pulsado un bot&oacute;n.
      </div>
      <p>No puede. Y no es que le falte una instrucci&oacute;n: es que <b>le falta cuerpo</b>. Un programa,
         solo, no toca nada del mundo. Para que lo toque hacen falta dos cosas que el ordenador de
         la sesi&oacute;n de entrada y salida del tema 9 ya ten&iacute;a, pero que aqu&iacute; se ven much&iacute;simo mejor:</p>
      <ul>
        <li><b>Entradas</b>: por donde le llega al programa lo que pasa fuera. Un bot&oacute;n, un
            sensor de luz, un term&oacute;metro.</li>
        <li><b>Salidas</b>: por donde el programa cambia algo fuera. Una luz, un altavoz, un motor.</li>
      </ul>
      <p>Una placa como la <b>micro:bit</b> es exactamente eso: un ordenador min&uacute;sculo con las
         entradas y las salidas <b>a la vista</b>, para que se entienda qu&eacute; est&aacute; pasando.</p>
'''

# --------------------------------------------------------------------------
# 01 - Teoria, con el simulador
# --------------------------------------------------------------------------
ESCENA = u'''
      <div class="escena" id="esc-mb">
        <div class="escena-barra">
          <span class="escena-titulo">La placa, funcionando &middot; elige un programa</span>
          <div class="seg" id="seg-mb">
            <button type="button" data-p="0" aria-pressed="true">Dibujo libre</button>
            <button type="button" data-p="1">Contador</button>
            <button type="button" data-p="2">Dado</button>
          </div>
        </div>
        <div class="lienzo">
          <div class="mb">
            <div class="mb-izq">
              <svg viewBox="0 0 320 250" id="svg-mb" role="img"
                   aria-label="Placa micro:bit con sus 25 LED y sus botones A y B"></svg>
              <div class="mb-bot">
                <button type="button" data-b="A">Bot&oacute;n A</button>
                <button type="button" data-b="B">Bot&oacute;n B</button>
                <button type="button" data-b="R">Reiniciar</button>
              </div>
            </div>
            <div class="mb-der">
              <div class="mb-prog" id="prog-mb"></div>
              <p class="mb-nota" id="nota-mb"></p>
            </div>
          </div>
        </div>
        <div class="pie" id="pie-mb"></div>
      </div>

      <style>
      .mb{display:flex;gap:18px;flex-wrap:wrap;align-items:flex-start}
      .mb-izq{flex:1 1 320px;min-width:280px}
      .mb-der{flex:1 1 280px;min-width:250px}
      .mb-bot{display:flex;gap:8px;margin-top:10px;flex-wrap:wrap}
      .mb-bot button{font-family:var(--f-m);font-size:13px;border:1.5px solid var(--goo-azul);
        background:var(--goo-azul);color:#fff;border-radius:2px;padding:9px 15px;cursor:pointer}
      .mb-bot button[data-b="R"]{background:var(--surface);color:var(--ink-soft);border-color:var(--line)}
      .mb-prog{border:1.5px solid var(--line);border-radius:2px;background:var(--surface);padding:10px 12px;
        font-family:var(--f-m);font-size:13px;line-height:1.75}
      .mb-prog .blq{display:block;padding:3px 8px;border-left:4px solid var(--line);margin:2px 0;border-radius:2px}
      .mb-prog .blq.ev{border-left-color:var(--goo-azul);background:var(--accent-soft)}
      .mb-prog .blq.act{border-left-color:var(--goo-verde);background:rgba(52,168,83,.12)}
      .mb-prog .sang{margin-left:18px}
      .mb-nota{font-family:var(--f-m);font-size:12.5px;color:var(--ink-soft);line-height:1.6;margin:10px 0 0}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-mb');
        if(!svg) return;
        var caja = document.getElementById('esc-mb');
        var prog = document.getElementById('prog-mb');
        var nota = document.getElementById('nota-mb');
        var pie  = document.getElementById('pie-mb');
        var seg  = document.getElementById('seg-mb');

        var AZ='var(--goo-azul)', RO='var(--goo-rojo)', GR='var(--ink-soft)', TI='var(--ink)';

        /* --- las 25 luces, como en la placa: fila 0 arriba --- */
        var luz = [], k;
        for(k = 0; k < 25; k++) luz.push(0);
        var modo = 0, cuenta = 0, dado = 0, resaltado = -1, temp = null;

        /* Digitos de 3x5, que es lo que hace la placa de verdad con un numero
           de una cifra: mas ancho no cabe y por eso los numeros largos pasan
           desfilando.                                                        */
        var CIF = ['111101101101111','010110010010111','111001111100111','111001111001111',
                   '101101111001001','111100111001111','111100111101111','111001001001001',
                   '111101111101111','111101111001111'];
        /* Las caras del dado, en la cuadricula de 5 por 5 */
        var CARA = {1:[[2,2]], 2:[[0,0],[4,4]], 3:[[0,0],[2,2],[4,4]],
                    4:[[0,0],[4,0],[0,4],[4,4]], 5:[[0,0],[4,0],[2,2],[0,4],[4,4]],
                    6:[[0,0],[4,0],[0,2],[4,2],[0,4],[4,4]]};

        function apaga(){ for(var i = 0; i < 25; i++) luz[i] = 0; }
        function pon(x, y, v){ if(x>=0 && x<5 && y>=0 && y<5) luz[y*5+x] = v; }

        function muestraCifra(n){
          apaga();
          var g = CIF[n], i;
          for(i = 0; i < 15; i++) if(g[i] === '1') pon(1 + (i % 3), Math.floor(i/3), 1);
        }
        function muestraCara(n){
          apaga();
          (CARA[n] || []).forEach(function(p){ pon(p[0], p[1], 1); });
        }

        function patron(){
          /* el mismo formato que usa MakeCode para el bloque "mostrar LEDs" */
          var t = '', y, x;
          for(y = 0; y < 5; y++){
            for(x = 0; x < 5; x++) t += luz[y*5+x] ? '#' : '.';
            t += (y < 4 ? '<br>' : '');
          }
          return t;
        }

        var PROG = [
          {n:'Dibujo libre',
           blq: function(){
             return '<span class="blq ev">al iniciar</span>'
                  + '<span class="blq sang' + (resaltado===0?' act':'') + '">mostrar LEDs</span>'
                  + '<span class="blq sang" style="border-left-color:transparent">'
                  + '<code>' + patron() + '</code></span>'; },
           d:'Pulsa en las luces para dibujar. A la derecha tienes el bloque <b>mostrar LEDs</b> tal '
            +'y como lo escribe MakeCode: cada almohadilla es un LED encendido. Eso es lo que hay '
            +'dentro del bloque bonito que arrastras.'},
          {n:'Contador',
           blq: function(){
             return '<span class="blq ev">al iniciar</span>'
                  + '<span class="blq sang">poner <b>cuenta</b> a 0</span>'
                  + '<span class="blq ev' + (resaltado===1?' act':'') + '">al pulsar el bot&oacute;n A</span>'
                  + '<span class="blq sang' + (resaltado===1?' act':'') + '">cambiar <b>cuenta</b> en 1</span>'
                  + '<span class="blq ev' + (resaltado===2?' act':'') + '">al pulsar el bot&oacute;n B</span>'
                  + '<span class="blq sang' + (resaltado===2?' act':'') + '">cambiar <b>cuenta</b> en -1</span>'
                  + '<span class="blq ev">para siempre</span>'
                  + '<span class="blq sang">mostrar n&uacute;mero <b>cuenta</b></span>'; },
           d:'Aqu&iacute; aparece la pieza que faltaba: una <b>variable</b>. <b>cuenta</b> es un cajón con '
            +'nombre donde la placa guarda un n&uacute;mero entre pulsaci&oacute;n y pulsaci&oacute;n. Sin ella, '
            +'la placa no recordar&iacute;a nada y siempre mostrar&iacute;a lo mismo.'},
          {n:'Dado',
           blq: function(){
             return '<span class="blq ev' + (resaltado===3?' act':'') + '">al pulsar el bot&oacute;n B</span>'
                  + '<span class="blq sang' + (resaltado===3?' act':'') + '">poner <b>tirada</b> a n&uacute;mero al azar entre 1 y 6</span>'
                  + '<span class="blq sang' + (resaltado===3?' act':'') + '">mostrar la cara de <b>tirada</b></span>'; },
           d:'Un dado de verdad, en tres bloques. En la placa el bot&oacute;n B se cambia por '
            +'<b>al agitar</b>, que usa el aceler&oacute;metro: el mismo programa, con otra entrada.'}
        ];

        function pinta(){
          var m = '', x, y, i;
          /* la placa */
          m += '<rect x="26" y="14" width="268" height="176" rx="14" fill="#1a1a1a"></rect>';
          m += '<rect x="26" y="190" width="268" height="34" fill="#1a1a1a"></rect>';
          for(i = 0; i < 5; i++){
            m += '<rect x="' + (40 + i*54) + '" y="196" width="34" height="28" rx="3" fill="#caa54a"></rect>';
          }
          /* las 25 luces */
          for(y = 0; y < 5; y++){
            for(x = 0; x < 5; x++){
              var on = luz[y*5+x];
              m += '<rect x="' + (112 + x*20) + '" y="' + (44 + y*20) + '" width="13" height="13" rx="2" '
                 + 'fill="' + (on ? '#ff3b30' : '#3a3a3a') + '" stroke="' + (on ? '#ff8a80' : '#4a4a4a')
                 + '" stroke-width="1" style="cursor:pointer" data-luz="' + (y*5+x) + '"></rect>';
            }
          }
          /* los dos botones */
          [['A', 62], ['B', 246]].forEach(function(b){
            m += '<circle cx="' + b[1] + '" cy="102" r="20" fill="#333" stroke="#666" stroke-width="2"></circle>';
            m += '<text x="' + b[1] + '" y="107" text-anchor="middle" '
               + 'style="font:600 15px var(--f-m);fill:#eee">' + b[0] + '</text>';
          });
          m += '<text x="160" y="240" text-anchor="middle" style="font:11px var(--f-m);fill:' + GR
             + '">los 25 LED son la salida &middot; A y B son entradas</text>';
          svg.innerHTML = m;
          prog.innerHTML = PROG[modo].blq();
          pie.innerHTML = '<b>' + PROG[modo].n + '.</b> ' + PROG[modo].d;
        }

        function marca(n){
          resaltado = n; pinta();
          if(temp) clearTimeout(temp);
          temp = setTimeout(function(){ resaltado = -1; pinta(); }, 700);
        }

        function reinicia(){
          apaga(); cuenta = 0; dado = 0; resaltado = -1;
          if(modo === 1){ muestraCifra(0); nota.innerHTML = 'La cuenta va por <b>0</b>.'; }
          else if(modo === 2){ nota.innerHTML = 'Pulsa <b>B</b> para tirar.'; }
          else { nota.innerHTML = 'Pulsa en las luces para dibujar tu icono.'; }
          pinta();
        }

        svg.addEventListener('click', function(e){
          var r = e.target.closest('[data-luz]');
          if(!r || modo !== 0) return;
          var i = +r.dataset.luz;
          luz[i] = luz[i] ? 0 : 1;
          marca(0);
        });

        caja.querySelectorAll('[data-b]').forEach(function(b){
          b.addEventListener('click', function(){
            var q = b.dataset.b;
            if(q === 'R'){ reinicia(); return; }
            if(modo === 1){
              if(q === 'A'){ cuenta++; marca(1); }
              else { cuenta--; marca(2); }
              if(cuenta > 9 || cuenta < 0){
                nota.innerHTML = 'La cuenta va por <b>' + cuenta + '</b>. En la placa de verdad un '
                  + 'n&uacute;mero de m&aacute;s de una cifra <b>pasa desfilando</b>, porque en 5 por 5 no cabe.';
                apaga(); pinta(); return;
              }
              muestraCifra(cuenta);
              nota.innerHTML = 'La cuenta va por <b>' + cuenta + '</b>.';
              pinta();
            } else if(modo === 2){
              if(q !== 'B'){ nota.innerHTML = 'Este programa solo escucha al bot&oacute;n <b>B</b>. '
                  + 'El A no hace nada porque <b>no hay ning&uacute;n bloque</b> que lo escuche.'; return; }
              dado = 1 + Math.floor(Math.random()*6);
              muestraCara(dado); marca(3);
              nota.innerHTML = 'Ha salido un <b>' + dado + '</b>. Vuelve a pulsar: sale otro, '
                + 'y ese es el sentido de <i>al azar</i>.';
            } else {
              nota.innerHTML = 'En este programa los botones no hacen nada: no hay ning&uacute;n bloque '
                + 'que los escuche. Dibuja pulsando en las luces.';
            }
          });
        });

        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-p]'); if(!b) return;
          seg.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          modo = +b.dataset.p; reinicia();
        });

        reinicia();
      })();
      </script>
'''

TEORIA = u'''
      <p>La micro:bit es una placa del tama&ntilde;o de media tarjeta de cr&eacute;dito. Lo interesante es
         que todo lo que tiene <b>se ve</b>:</p>
      <div class="copiar">
        <h4>Qu&eacute; lleva una micro:bit</h4>
        <ul>
          <li><b>25 LED</b> en cuadr&iacute;cula de 5 &times; 5: la salida m&aacute;s visible.</li>
          <li><b>Dos botones</b>, A y B: las entradas m&aacute;s sencillas.</li>
          <li><b>Sensores</b> dentro: aceler&oacute;metro (sabe si la mueves), br&uacute;jula, term&oacute;metro,
              micr&oacute;fono. La luz la mide con sus propios LED.</li>
          <li><b>Pines</b> en el borde dorado: por ah&iacute; se le conectan cosas de fuera.</li>
          <li><b>Radio</b>: puede hablar con otras micro:bit sin cables.</li>
        </ul>
        <h4>Los dos bloques que lo organizan todo</h4>
        <p><b>Al iniciar</b>: lo que se hace <b>una sola vez</b>, al encender.</p>
        <p><b>Para siempre</b>: lo que se repite <b>sin parar</b> mientras la placa tenga corriente.
           Es un <b>bucle infinito</b>, y aqu&iacute; no es un error: es lo normal. Una m&aacute;quina que
           vigila algo tiene que estar mirando siempre.</p>
      </div>
      <p>Prueba la placa aqu&iacute; mismo. Los tres programas funcionan de verdad, y a la derecha
         tienes los bloques que los escriben.</p>
''' + ESCENA + u'''
      <div class="copiar">
        <h4>Definici&oacute;n</h4>
        <p><b>Variable</b>: un caj&oacute;n con nombre donde el programa guarda un dato para
           <b>acordarse de &eacute;l m&aacute;s tarde</b>. Sin variables, un programa no puede recordar
           nada entre una cosa y la siguiente.</p>
        <h4>Los tres bloques que ya sabes usar</h4>
        <ul>
          <li><b>Secuencia</b>: una instrucci&oacute;n detr&aacute;s de otra. Sesi&oacute;n 1.</li>
          <li><b>Bucle</b>: repetir. Sesi&oacute;n 2, y aqu&iacute; el <i>para siempre</i>.</li>
          <li><b>Evento</b>: <i>al pulsar el bot&oacute;n A</i>. El programa <b>espera</b> a que pase
              algo, en vez de ir seguido.</li>
        </ul>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>F&iacute;jate en el programa del dado: si pulsas <b>A</b>, no pasa nada. Y no es que est&eacute;
           roto: es que <b>no hay ning&uacute;n bloque que escuche al bot&oacute;n A</b>. La placa no
           ignora el bot&oacute;n por capricho; sencillamente nadie le ha dicho qu&eacute; hacer con &eacute;l.</p>
        <p>Y prueba a subir el contador por encima de 9. El n&uacute;mero deja de caber en 5 &times; 5, y
           la placa de verdad lo hace <b>pasar desfilando</b> de derecha a izquierda. Eso tambi&eacute;n
           es una decisi&oacute;n de dise&ntilde;o de alguien: con 25 luces, o desfila o no se puede.</p>
      </div>
'''

# --------------------------------------------------------------------------
# 02 - Practica
# --------------------------------------------------------------------------
PRACTICA = ficha(
    u'Actividad 3 &middot; Tu primer programa en MakeCode',
    [u'5.1', u'5.2', u'C.1', u'C.2'], u'Parejas &middot; 20 min', u'''
          <h4>D&oacute;nde se hace</h4>
          <p>En <b>makecode.microbit.org</b>, que funciona en el navegador y <b>no hay que instalar
             nada</b>. Trae su propia placa simulada, as&iacute; que se puede probar todo aunque no
             haya placas suficientes.</p>
          <h4>Qu&eacute; hay que hacer</h4>
          <ol class="pasos">
            <li><b>El icono.</b> Dibuja el tuyo en la escena de arriba, c&oacute;pialo al bloque
                <b>mostrar LEDs</b> de MakeCode y ponlo dentro de <b>al iniciar</b>.</li>
            <li><b>El contador.</b> Crea la variable <b>cuenta</b> y haz que A sume, B reste y la
                placa muestre el n&uacute;mero. Comprueba qu&eacute; pasa al pasar de 9.</li>
            <li><b>El dado.</b> Cambia el bot&oacute;n B por <b>al agitar</b> y usa
                <i>n&uacute;mero al azar entre 1 y 6</i>. Mu&eacute;stralo con <b>mostrar n&uacute;mero</b>
                primero, y luego dibuja t&uacute; las seis caras con <b>mostrar LEDs</b>.</li>
            <li><b>El fallo buscado.</b> Quita el bloque <i>poner cuenta a 0</i> del contador y
                anota qu&eacute; pasa y por qu&eacute;.</li>
          </ol>
          <div class="nota">
            <span class="n-tag">Si hay placas</span>
            Descargad el archivo <b>.hex</b> y arrastradlo a la unidad MICROBIT, que aparece como
            un pendrive. No hay que instalar nada ni configurar nada.
          </div>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>El icono se muestra al iniciar <b>(2 puntos)</b>.</li>
            <li>El contador usa una <b>variable</b> y responde a los dos botones <b>(3 puntos)</b>.</li>
            <li>El dado funciona con <b>al agitar</b> y con las caras dibujadas <b>(3 puntos)</b>.</li>
            <li>La explicaci&oacute;n del fallo buscado es correcta <b>(2 puntos)</b>.</li>
          </ul>
''')

# --------------------------------------------------------------------------
# 03 - Cierre
# --------------------------------------------------------------------------
CIERRE = u'''
      <ol>
      ''' + pregunta(
          u'&iquest;Qu&eacute; diferencia hay entre <i>al iniciar</i> y <i>para siempre</i>?',
          u'<p><i>Al iniciar</i> se ejecuta <b>una sola vez</b>, al encender la placa. '
          u'<i>Para siempre</i> se repite <b>sin parar</b> mientras haya corriente: es un bucle '
          u'infinito, y aqu&iacute; es justo lo que se quiere.</p>') + pregunta(
          u'&iquest;Para qu&eacute; sirve una variable?',
          u'<p>Para que el programa <b>recuerde</b> un dato de una vez para otra. Sin la variable '
          u'<i>cuenta</i>, la placa no sabr&iacute;a por qu&eacute; n&uacute;mero iba y siempre mostrar&iacute;a '
          u'lo mismo.</p>') + pregunta(
          u'En el programa del dado pulsas A y no pasa nada. &iquest;Est&aacute; estropeada la placa?',
          u'<p><b>No.</b> No hay ning&uacute;n bloque que escuche al bot&oacute;n A, as&iacute; que la placa no '
          u'tiene nada que hacer con &eacute;l. Una m&aacute;quina no ignora: es que no se le ha dicho.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Los botones los pulsas t&uacute;. Pero la placa tiene <b>sensores</b>, y eso es otra cosa: puede
        enterarse de que hace fr&iacute;o, de que se ha quedado a oscuras o de que la han movido,
        <b>sin que nadie le diga nada</b>. Ah&iacute; empieza a parecerse a un robot.
      </div>
'''

S3 = (bloque('00', u'Reto inicial &middot; 10 min', RETO) +
      bloque('01', u'Teor&iacute;a &middot; 25 min', TEORIA) +
      bloque('02', u'Pr&aacute;ctica &middot; 20 min', PRACTICA) +
      bloque('03', u'Cierre &middot; 5 min', CIERRE))
