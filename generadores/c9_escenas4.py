# -*- coding: utf-8 -*-
"""4.o Tecnologia - Tema 9 - Escenas de las sesiones 7 y 8.

  CONTINUAR (S7)  Dos modos en una escena.
      A - "Lo que tarda el siguiente". Marcas lo que dejas escrito y la escena
          suma los MINUTOS que le cuesta al grupo que lo coja dentro de tres
          anos reconstruir lo que falta, y los compara con las ocho sesiones
          que tiene. Saca ademas cuantos minutos ahorra despues cada minuto
          que gastas ahora. Hay una casilla que las tumba todas: si no dices
          DONDE esta guardado, da igual lo bien escrito que este.
      B - "Lo que deja hacer la licencia". Cinco licencias con sus permisos
          declarados como banderas, y cinco cosas que querria hacer el
          siguiente. La tabla NO esta escrita: sale de evaluar cada cosa
          contra las banderas de la licencia elegida. Y se dibuja la cadena
          de tres generaciones, para ver donde se cierra.

  ACEPTACION (S8)  "La prueba que acordais antes". Una prueba de aceptacion
      es una banda -entre tanto y tanto-, unas repeticiones y cuantas tienen
      que salir. La escena calcula, con la campana de Gauss y la binomial, la
      probabilidad de que APRUEBE un aparato que esta bien y la de que apruebe
      uno que esta mal. Las dos a la vez, porque una prueba que no suspende a
      nadie no comprueba nada.

Todo numero de la pantalla sale de una cuenta declarada en la propia escena.

Clases e ids con prefijo q7-, q8-. Nada que empiece por test- ni por ses-.
Estas cadenas NO pasan por ningun formateo con %.
"""

# ==========================================================================
# S7 - Que otro lo pueda continuar
# ==========================================================================
CONTINUAR = u'''
      <div class="escena" id="esc-q7">
        <div class="escena-barra">
          <span class="escena-titulo">&iquest;Puede otro continuarlo?</span>
          <div class="seg" id="q7-modo">
            <button type="button" data-m="a" aria-pressed="true">Lo que tarda el siguiente</button>
            <button type="button" data-m="b">Lo que deja hacer la licencia</button>
          </div>
        </div>
        <div class="lienzo">
          <div class="q7">
            <div class="q7-izq">
              <svg viewBox="0 0 460 210" id="svg-q7" role="img"
                   aria-label="Minutos que le cuesta al siguiente grupo reconstruir lo que no dejaste escrito"></svg>
            </div>
            <div class="q7-der">
              <div id="q7-ma">
                <p class="q7-rotder">Lo que dej&aacute;is en la caja</p>
                <div class="q7-lista" id="q7-lista"></div>
              </div>
              <div id="q7-mb" hidden>
                <p class="q7-rotder">La licencia que le pon&eacute;is</p>
                <div class="seg q7-lic" id="q7-lic">
                  <button type="button" data-l="0" aria-pressed="true">Sin decir nada</button>
                  <button type="button" data-l="1">CC BY</button>
                  <button type="button" data-l="2">CC BY-SA</button>
                  <button type="button" data-l="3">CC BY-NC</button>
                  <button type="button" data-l="4">CC0</button>
                </div>
                <div class="q7-mat" id="q7-mat"></div>
              </div>
              <div class="q7-tabla" id="q7-tabla"></div>
            </div>
          </div>
          <p class="q7-lee" id="q7-lee"></p>
        </div>
        <div class="pie" id="q7-pie"></div>
      </div>

      <style>
      .q7{display:flex;gap:18px;flex-wrap:wrap;align-items:flex-start}
      .q7-izq{flex:1 1 380px;min-width:300px}
      .q7-der{flex:1 1 300px;min-width:272px}
      .q7-rotder{font-family:var(--f-m);font-size:11px;letter-spacing:.08em;text-transform:uppercase;
        color:var(--ink-soft);margin:0 0 9px}
      .q7-lista label{display:flex;gap:8px;align-items:flex-start;font-family:var(--f-m);
        font-size:12.5px;line-height:1.5;margin:0 0 7px;cursor:pointer;color:var(--ink)}
      .q7-lista input{margin-top:2px;flex:none;accent-color:var(--goo-azul)}
      .q7-lista small{display:block;color:var(--ink-soft);font-size:11px}
      .q7-lista label.clave{border-left:3px solid var(--goo-amarillo);padding-left:7px}
      .q7-lic{margin-bottom:10px}
      .q7-lic button{padding:5px 8px;font-size:11px}
      .q7-mat{font-family:var(--f-m);font-size:12px;line-height:1.5}
      .q7-mat .m{display:flex;gap:8px;align-items:flex-start;margin:0 0 7px;
        border-bottom:1px solid var(--line-soft);padding-bottom:6px}
      .q7-mat .m:last-child{border-bottom:0}
      .q7-mat .v{flex:none;width:62px;font-weight:500;text-align:right;white-space:nowrap}
      .q7-mat .v.si{color:var(--goo-verde)}
      .q7-mat .v.no{color:var(--goo-rojo)}
      .q7-mat .v.med{color:var(--ink-soft)}
      .q7-mat small{display:block;color:var(--ink-soft);font-size:11px}
      .q7-tabla{border:1.5px solid var(--line);border-radius:2px;background:var(--surface);
        padding:9px 11px;font-family:var(--f-m);font-size:12.5px;line-height:1.7;margin-top:10px}
      .q7-tabla .f{display:flex;justify-content:space-between;gap:10px}
      .q7-tabla .f span:first-child{color:var(--ink-soft)}
      .q7-tabla .f b{color:var(--ink);font-weight:500;text-align:right}
      .q7-tabla .f.top{border-top:1px solid var(--line-soft);margin-top:5px;padding-top:5px}
      .q7-tabla .f.no b{color:var(--goo-rojo)}
      .q7-tabla .f.si b{color:var(--goo-verde)}
      .q7-lee{font-family:var(--f-m);font-size:13px;line-height:1.75;color:var(--ink-soft);margin:12px 0 0}
      .q7-lee b{color:var(--ink)}
      .q7-lee .grande{font-size:16px;color:var(--goo-azul);font-weight:500}
      .q7-lee .malo{color:var(--goo-rojo)}
      .q7-rot{fill:var(--ink-soft);font-family:var(--f-m);font-size:11px}
      .q7-etq{fill:var(--ink);font-family:var(--f-m);font-size:11.5px;font-weight:500}
      .q7-num{fill:#fff;font-family:var(--f-m);font-size:10.5px;font-weight:500}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-q7');
        if(!svg) return;
        var segModo = document.getElementById('q7-modo');
        var segLic = document.getElementById('q7-lic');
        var ma = document.getElementById('q7-ma');
        var mb = document.getElementById('q7-mb');
        var lista = document.getElementById('q7-lista');
        var mat = document.getElementById('q7-mat');
        var tabla = document.getElementById('q7-tabla');
        var lee = document.getElementById('q7-lee');
        var pie = document.getElementById('q7-pie');

        /* ---- constantes DECLARADAS ----
           Los minutos son estimacion nuestra, hecha a ojo de taller: lo que
           tarda de verdad un grupo de 4.o en reconstruir cada cosa. No hay
           fuente para esto y no la vamos a inventar. */
        var SESION = 50;            /* minutos utiles de una sesion de 60 */
        var SESIONES = 8;           /* lo que dura una unidad */

        var COSAS = [
          {k: 'sitio', c: 'd\\u00f3nde est\\u00e1',
           n: 'D&oacute;nde est&aacute; guardado, y que siga existiendo',
           d: 'una carpeta del departamento, no el Drive de una cuenta que caduca en junio',
           poner: 5, falta: 0, clave: true},
          {k: 'foto', c: 'la foto', n: 'Una foto del montaje terminado',
           d: 'para saber c&oacute;mo iba colocado', poner: 3, falta: 20},
          {k: 'esquema', c: 'el esquema', n: 'El esquema el&eacute;ctrico, con los pines',
           d: 'sin esto hay que reconstruir seis conexiones midiendo, y se quema alguna placa',
           poner: 25, falta: 95},
          {k: 'piezas', c: 'las piezas',
           n: 'La lista de piezas, con referencia y d&oacute;nde se compra',
           d: 'identificar un sensor por la serigraf&iacute;a lleva su rato', poner: 10, falta: 35},
          {k: 'codigo', c: 'el programa', n: 'El programa, el fichero .ino de verdad',
           d: 'no una captura de pantalla del programa', poner: 2, falta: 300},
          {k: 'comenta', c: 'comentado', n: 'El programa comentado',
           d: 'por qu&eacute; el umbral es 430 y no 500', poner: 20, falta: 60},
          {k: 'calibra', c: 'la calibraci\\u00f3n', n: 'C&oacute;mo se calibr&oacute;, paso a paso',
           d: 'tierra seca, tierra mojada y los dos n&uacute;meros que sal&iacute;an',
           poner: 8, falta: 45},
          {k: 'manual', c: 'el manual',
           n: 'Una hoja: qu&eacute; hace, c&oacute;mo se usa, qu&eacute; falla',
           d: 'la que lee quien lo recibe, no quien lo construy&oacute;', poner: 30, falta: 55},
          {k: 'licencia', c: 'la licencia', n: 'La licencia, escrita en el propio documento',
           d: 'sin esto no hay permiso, y eso no se arregla con horas', poner: 2, falta: 0}
        ];

        /* Banderas de cada licencia. De aqui sale la tabla: NO esta escrita. */
        var LIC = [
          {n: 'Sin decir nada', copia: 'privada', deriva: false, publica: false,
           comercial: false, cita: false, sa: false,
           d: 'no es que no tenga licencia: es que los tiene <b>todos los derechos '
            + 'reservados</b> por defecto, desde el momento en que lo hac&eacute;is y sin '
            + 'registrar nada'},
          {n: 'CC BY', copia: 'si', deriva: true, publica: true, comercial: true,
           cita: true, sa: false,
           d: 'haz lo que quieras, pero <b>di de qui&eacute;n es</b>'},
          {n: 'CC BY-SA', copia: 'si', deriva: true, publica: true, comercial: true,
           cita: true, sa: true,
           d: 'lo mismo, y adem&aacute;s <b>tu versi&oacute;n se publica con esta misma '
            + 'licencia</b>. Es la de esta p&aacute;gina: m&iacute;rale el pie'},
          {n: 'CC BY-NC', copia: 'si', deriva: true, publica: true, comercial: false,
           cita: true, sa: false,
           d: 'citando, s&iacute;, pero <b>nadie puede sacarle dinero</b>, ni siquiera un AMPA '
            + 'para pagar el material'},
          {n: 'CC0', copia: 'si', deriva: true, publica: true, comercial: true,
           cita: false, sa: false,
           d: 'lo sueltas del todo: <b>ni siquiera hace falta que te citen</b>'}
        ];

        /* Lo que querria hacer el siguiente. Cada una se evalua contra las
           banderas de arriba y devuelve 2 (si), 1 (a medias) o 0 (no). */
        var QUIERE = [
          {n: 'Montarlo otra vez en su clase',
           v: function(L){ return L.copia === 'si' ? 2 : (L.copia === 'privada' ? 1 : 0); },
           nota: function(L){ return L.copia === 'privada'
             ? 'para &eacute;l s&iacute;, pero no lo puede colgar en ning&uacute;n sitio' : ''; }},
          {n: 'Cambiarlo y publicar su versi&oacute;n',
           v: function(L){ return (L.deriva && L.publica) ? 2 : 0; }, nota: function(){ return ''; }},
          {n: 'Que el AMPA lo venda en la fiesta para sacar fondos',
           v: function(L){ return L.comercial ? 2 : 0; },
           nota: function(L){ return L.comercial ? '' : 'da igual que sea para el cole: '
             + 'vender es vender'; }},
          {n: 'Meter vuestro esquema en la Wikipedia',
           v: function(L){ return (L.publica && L.comercial && L.deriva) ? 2 : 0; },
           nota: function(L){ return (L.publica && L.comercial && L.deriva) ? ''
             : 'la Wikipedia es CC BY-SA y permite uso comercial: lo que no lo permite, no entra'; }},
          {n: 'Publicar su versi&oacute;n con candado, para que el de despu&eacute;s ya no pueda',
           v: function(L){ return (L.deriva && !L.sa) ? 2 : 0; },
           nota: function(L){ return L.sa ? 'esto es lo &uacute;nico que a&ntilde;ade el SA, y es '
             + 'justo lo que hace que lo vuestro siga abierto dentro de diez a&ntilde;os' : ''; }}
        ];

        /* Arranca en "sin decir nada", que es lo que hace todo el mundo, y es
           donde empieza el texto de la sesion. Ojo: si se cambia, hay que
           cambiar tambien el aria-pressed del boton de arriba, o la escena
           ensena una licencia con otra marcada. */
        var modo = 'a', lic = 0;
        var puesto = {};
        COSAS.forEach(function(c){ puesto[c.k] = false; });

        function coma(x, d){
          var p = Math.abs(x).toFixed(d).split('.');
          var e = p[0].replace(/\\B(?=(\\d{3})+(?!\\d))/g, '.');
          return (x < 0 ? '\\u2212' : '') + e + (d ? ',' + p[1] : '');
        }
        function mmhh(m){
          var h = Math.floor(m / 60), r = Math.round(m - h * 60);
          return (h ? h + ' h ' : '') + r + ' min';
        }
        function f(a, b, cl){
          return '<div class="f ' + (cl || '') + '"><span>' + a + '</span><b>' + b + '</b></div>';
        }

        function monta(){
          lista.innerHTML = COSAS.map(function(c){
            return '<label' + (c.clave ? ' class="clave"' : '') + '><input type="checkbox" data-k="'
                 + c.k + '"><span>' + c.n + '<small>' + c.d
                 + ' &middot; escribirlo cuesta ' + c.poner + ' min</small></span></label>';
          }).join('');
          lista.querySelectorAll('input[data-k]').forEach(function(i){
            i.addEventListener('change', function(){
              puesto[i.dataset.k] = i.checked;
              pinta();
            });
          });
        }

        /* ---- la cuenta entera, en un sitio ---- */
        function calcula(){
          /* Si no se dice donde esta guardado, lo demas es como si no estuviera:
             existe en algun sitio, pero el siguiente no lo va a encontrar. */
          var hayCarpeta = puesto.sitio;
          var faltan = COSAS.filter(function(c){
            return c.falta > 0 && (!hayCarpeta || !puesto[c.k]);
          });
          var reconstruir = faltan.reduce(function(a, c){ return a + c.falta; }, 0);
          var escribir = COSAS.reduce(function(a, c){
            return a + (puesto[c.k] ? c.poner : 0); }, 0);
          var todo = COSAS.reduce(function(a, c){ return a + c.poner; }, 0);
          var todoFalta = COSAS.reduce(function(a, c){ return a + c.falta; }, 0);
          /* lo que ya le has ahorrado al siguiente: la suma de lo que le
             habria costado cada cosa que si has dejado */
          var ahorrado = todoFalta - reconstruir;
          var presupuesto = SESION * SESIONES;
          return {faltan: faltan, reconstruir: reconstruir, escribir: escribir, todo: todo,
                  todoFalta: todoFalta, ahorrado: ahorrado,
                  presupuesto: presupuesto, hayCarpeta: hayCarpeta,
                  sesiones: reconstruir / SESION,
                  ahorro: escribir > 0 ? ahorrado / escribir : 0,
                  conLicencia: puesto.licencia};
        }

        function pintaA(){
          var c = calcula();

          /* ---------- barras: lo que le cuesta al siguiente cada agujero ---------- */
          var x0 = 8, ancho = 268, y0 = 40, fila = 18, rot = 108;
          var maxf = 300;
          var s = [];
          s.push('<text x="' + x0 + '" y="16" class="q7-rot">minutos que le cuesta al siguiente '
               + 'cada cosa que no dejes</text>');
          var ordenadas = COSAS.filter(function(x){ return x.falta > 0; });
          ordenadas.forEach(function(x, j){
            var y = y0 + j * fila;
            var falta = !c.hayCarpeta || !puesto[x.k];
            var w = ancho * x.falta / maxf;
            s.push('<rect x="' + (x0 + rot) + '" y="' + (y - 9) + '" width="' + w.toFixed(1)
                 + '" height="11" fill="' + (falta ? 'var(--goo-rojo)' : 'var(--goo-verde)')
                 + '" opacity="' + (falta ? '0.85' : '0.3') + '"/>');
            s.push('<text x="' + x0 + '" y="' + y + '" class="q7-rot">' + x.c + '</text>');
            s.push('<text x="' + (x0 + rot + 4 + w).toFixed(1) + '" y="' + y + '" class="q7-rot">'
                 + (falta ? x.falta + ' min' : 'lo dejaste') + '</text>');
          });

          /* la regla del presupuesto: lo que tiene el siguiente grupo */
          var yb = y0 + ordenadas.length * fila + 26;
          var wtot = Math.min(1, c.reconstruir / c.presupuesto) * ancho;
          s.push('<text x="' + x0 + '" y="' + (yb - 10) + '" class="q7-rot">'
               + 'lo que tiene el siguiente grupo: ' + SESIONES + ' sesiones = '
               + c.presupuesto + ' min</text>');
          s.push('<rect x="' + x0 + '" y="' + yb + '" width="' + ancho
               + '" height="22" fill="none" stroke="var(--ink)" stroke-width="1.4"/>');
          s.push('<rect x="' + x0 + '" y="' + yb + '" width="' + wtot.toFixed(1)
               + '" height="22" fill="' + (c.reconstruir > c.presupuesto
                   ? 'var(--goo-rojo)' : 'var(--goo-azul)') + '" opacity="0.8"/>');
          if(c.reconstruir > c.presupuesto){
            s.push('<path d="M' + (x0 + ancho + 4) + ' ' + yb + ' l 9 6 l -9 5 l 9 6 l -9 5" '
                 + 'fill="none" stroke="var(--goo-rojo)" stroke-width="2.5"/>');
          }
          s.push('<text x="' + (x0 + 6) + '" y="' + (yb + 15) + '" class="q7-num">'
               + mmhh(c.reconstruir) + ' solo en volver al punto de partida</text>');
          s.push('<text x="' + x0 + '" y="' + (yb + 40) + '" class="q7-etq">'
               + (c.reconstruir > c.presupuesto
                   ? 'No le cabe: lo tira y empieza de cero.'
                   : 'Le cabe, y le sobran ' + mmhh(c.presupuesto - c.reconstruir)
                     + ' para mejorarlo.') + '</text>');
          svg.setAttribute('viewBox', '0 0 460 ' + (yb + 54));
          svg.innerHTML = s.join('');

          tabla.innerHTML =
            f('cosas que dejas', COSAS.filter(function(x){ return puesto[x.k]; }).length
              + ' de ' + COSAS.length)
          + f('te cuesta escribirlas', mmhh(c.escribir))
          + f('le cuesta al siguiente', mmhh(c.reconstruir), 'top '
              + (c.reconstruir > c.presupuesto ? 'no' : 'si'))
          + f('en sesiones suyas', coma(c.sesiones, 1) + ' de ' + SESIONES)
          + f('cada minuto tuyo le ahorra', coma(c.ahorro, 1) + ' min')
          + f('lleva licencia', c.conLicencia ? 's\\u00ed' : 'no',
              'top ' + (c.conLicencia ? 'si' : 'no'));

          var v;
          if(!c.hayCarpeta){
            v = '<span class="grande malo">No has dicho d&oacute;nde est&aacute; guardado.</span> '
              + 'Da igual lo bien escrito que est&eacute; todo lo dem&aacute;s: si vive en el Drive de '
              + 'una cuenta del instituto que se borra cuando os vais, o en el port&aacute;til de uno '
              + 'de vosotros, dentro de tres a&ntilde;os <b>no existe</b>. Es la casilla de arriba, y '
              + 'cuesta cinco minutos.';
          } else if(c.reconstruir > c.presupuesto){
            v = '<span class="grande malo">Al siguiente le cuesta ' + mmhh(c.reconstruir)
              + ' volver a donde vosotros lo dejasteis.</span> Tiene ' + SESIONES
              + ' sesiones para toda la unidad. Se le va entera en reconstruir, as&iacute; que no lo '
              + 'continu&uacute;a: <b>lo tira y empieza de cero</b>, y vuestro trabajo se pierde. '
              + 'Escribirlo todo os habr&iacute;a costado ' + mmhh(c.todo) + '.';
          } else if(c.reconstruir === 0){
            v = '<span class="grande">Est&aacute; todo: el siguiente puede ponerse a mejorarlo el '
              + 'primer d&iacute;a.</span> Os ha costado ' + mmhh(c.escribir)
              + ', o sea ' + coma(c.escribir / SESION, 1) + ' sesiones vuestras, y le ahorra '
              + mmhh(c.ahorrado) + ' a &eacute;l: <b>' + coma(c.ahorro, 1)
              + ' minutos suyos por cada minuto vuestro</b>. '
              + (c.conLicencia ? '' : '<b class="malo">Pero le falta la licencia, y eso no se '
                  + 'arregla con horas: sin ella no tiene permiso.</b>');
          } else {
            v = '<span class="grande">Le cuesta ' + mmhh(c.reconstruir)
              + ', o sea ' + coma(c.sesiones, 1) + ' sesiones de las ' + SESIONES
              + ' que tiene.</span> Le cabe, pero se le va ah&iacute;. Cada minuto que hab&eacute;is '
              + 'gastado escribiendo le ahorra <b>' + coma(c.ahorro, 1) + ' minutos</b> a &eacute;l.';
          }
          lee.innerHTML = v;

          pie.innerHTML =
            'Los minutos de cada fila son <b>estimaci&oacute;n nuestra</b>, hecha a ojo de taller: '
          + 'no hay ninguna fuente que mida cu&aacute;nto tarda un grupo de 4.&ordm; en reconstruir un '
          + 'esquema, y prefiero decirlo a inventarme una. Lo que <b>no</b> es estimaci&oacute;n es la '
          + 'forma de la cuenta: <b>lo que no dejas escrito lo paga el siguiente en tiempo</b>, y ese '
          + 'tiempo sale de las mismas ocho sesiones que ten&eacute;is vosotros. La casilla de arriba '
          + '&mdash;d&oacute;nde est&aacute; guardado&mdash; anula a todas las dem&aacute;s a '
          + 'prop&oacute;sito: un documento perfecto en un sitio que desaparece vale cero.';
        }

        function pintaB(){
          var L = LIC[lic];
          var r = QUIERE.map(function(Q){ return {Q: Q, v: Q.v(L), nota: Q.nota(L)}; });
          var si = r.filter(function(x){ return x.v === 2; }).length;

          /* ---------- la cadena de tres generaciones ---------- */
          var s = [];
          var cajas = ['Vosotros, 2026', 'El grupo de 2029', 'El de 2032'];
          var bx = 10, bw = 124, bh = 46, gap = 34, by = 52;
          s.push('<text x="' + bx + '" y="20" class="q7-rot">qu\\u00e9 pasa con vuestro trabajo '
               + 'en las dos manos siguientes</text>');
          var puedeSeguir = L.deriva && L.publica;
          var sigueAbierto = puedeSeguir && L.sa;
          for(var i = 0; i < 3; i++){
            var x = bx + i * (bw + gap);
            var viva = i === 0 || (puedeSeguir && (i === 1 || sigueAbierto));
            s.push('<rect x="' + x + '" y="' + by + '" width="' + bw + '" height="' + bh
                 + '" fill="' + (viva ? 'var(--goo-verde)' : 'var(--surface-2)')
                 + '" opacity="' + (viva ? '0.28' : '1') + '" stroke="'
                 + (viva ? 'var(--goo-verde)' : 'var(--line)') + '" stroke-width="1.6"/>');
            s.push('<text x="' + (x + bw / 2) + '" y="' + (by + 20)
                 + '" class="q7-etq" text-anchor="middle">' + cajas[i] + '</text>');
            s.push('<text x="' + (x + bw / 2) + '" y="' + (by + 36)
                 + '" class="q7-rot" text-anchor="middle">'
                 + (viva ? 'puede seguir' : 'no le llega') + '</text>');
            if(i < 2){
              var ax = x + bw, cy = by + bh / 2, puede = (i === 0 ? puedeSeguir : sigueAbierto);
              s.push('<line x1="' + (ax + 4) + '" y1="' + cy + '" x2="' + (ax + gap - 4)
                   + '" y2="' + cy + '" stroke="'
                   + (puede ? 'var(--goo-verde)' : 'var(--goo-rojo)') + '" stroke-width="2.5"/>');
              if(!puede){
                s.push('<path d="M' + (ax + 12) + ' ' + (cy - 7) + ' l 10 14 M'
                     + (ax + 22) + ' ' + (cy - 7) + ' l -10 14" '
                     + 'stroke="var(--goo-rojo)" stroke-width="2.8" fill="none"/>');
              }
            }
          }
          s.push('<text x="' + bx + '" y="' + (by + bh + 28) + '" class="q7-etq">' + L.n
               + ': le deja hacer ' + si + ' de las ' + QUIERE.length + ' cosas</text>');
          s.push('<text x="' + bx + '" y="' + (by + bh + 48) + '" class="q7-rot">'
               + (sigueAbierto
                   ? 'y lo que salga de aqu\\u00ed sigue abierto, obligatoriamente'
                   : (puedeSeguir ? 'pero el siguiente puede cerrarlo, y ah\\u00ed se acaba'
                                  : 'nadie puede continuarlo legalmente')) + '</text>');
          svg.setAttribute('viewBox', '0 0 460 ' + (by + bh + 62));
          svg.innerHTML = s.join('');

          mat.innerHTML = '<p class="q7-rot" style="margin:0 0 8px;font-family:var(--f-m)">'
            + L.d + '</p>'
            + r.map(function(x){
                var cl = x.v === 2 ? 'si' : (x.v === 1 ? 'med' : 'no');
                var tx = x.v === 2 ? 's\\u00ed' : (x.v === 1 ? 'a medias' : 'no');
                return '<div class="m"><span class="v ' + cl + '">' + tx + '</span><span>'
                     + x.Q.n + (x.nota ? '<small>' + x.nota + '</small>' : '') + '</span></div>';
              }).join('');

          tabla.innerHTML =
            f('le dejas hacer', si + ' de ' + QUIERE.length)
          + f('hay que citaros', L.cita ? 's\\u00ed' : 'no')
          + f('puede sacarle dinero', L.comercial ? 's\\u00ed' : 'no',
              L.comercial ? '' : 'no')
          + f('su versi\\u00f3n sigue libre', L.sa ? 'obligatoriamente' : 'solo si le apetece',
              'top ' + (L.sa ? 'si' : 'no'));

          lee.innerHTML = (L.sa
            ? '<span class="grande">Con CC BY-SA, lo que salga de vuestro trabajo <b>sigue siendo '
              + 'de todos</b>.</span> Es la &uacute;nica de las cinco que lo garantiza, y es la que '
              + 'lleva esta p&aacute;gina: baja al pie y lo ver&aacute;s. A cambio, el siguiente '
              + 'pierde una libertad: la de cerrar su versi&oacute;n. <b>Eso es una decisi&oacute;n, '
              + 'no un descuido.</b>'
            : (lic === 0
              ? '<span class="grande malo">Sin licencia no es que sea de todos: es que es solo '
                + 'vuestro.</span> Los derechos de autor no hay que pedirlos, salen solos en cuanto '
                + 'hac&eacute;is algo. Si no dec&iacute;s nada, el que lo encuentre dentro de tres '
                + 'a&ntilde;os <b>no tiene permiso</b> para publicarlo ni para seguir con &eacute;l, '
                + 'aunque vosotros no os acord&eacute;is ni de haberlo hecho.'
              : '<span class="grande">Le dej&aacute;is hacer ' + si + ' de las '
                + QUIERE.length + '.</span> ' + (L.comercial
                  ? 'Pero el siguiente puede <b>cerrar su versi&oacute;n</b>: lo mejora y ya no lo '
                    + 'comparte. Si eso os molesta, la que quer&eacute;is es la SA.'
                  : 'Ojo con el NC: parece m&aacute;s protector y lo que hace es <b>dejar fuera</b> '
                    + 'a quien quiera usarlo en serio, incluida la Wikipedia y el AMPA de vuestro '
                    + 'propio centro.')));

          pie.innerHTML =
            'La tabla de la derecha <b>no est&aacute; escrita a mano</b>: cada licencia se declara '
          + 'aqu&iacute; como cinco banderas (deja copiar, deja modificar, deja publicar, deja usarlo '
          + 'para ganar dinero, obliga a citar, obliga a la misma licencia) y cada fila se calcula '
          + 'preguntando a esas banderas. Es un resumen para entenderlo, <b>no es asesoramiento '
          + 'legal</b>: el texto que manda es el de cada licencia en creativecommons.org. Lo que '
          + 's&iacute; conviene grabarse es lo de arriba del todo: <b>sin decir nada, todos los '
          + 'derechos quedan reservados</b>. Poner la licencia no es regalar: es <b>dar permiso</b>, '
          + 'y sin permiso escrito nadie con dos dedos de frente va a continuar vuestro trabajo.';
        }

        function pinta(){ if(modo === 'a') pintaA(); else pintaB(); }

        segModo.addEventListener('click', function(e){
          var b = e.target.closest('button[data-m]');
          if(!b) return;
          modo = b.dataset.m;
          ma.hidden = (modo !== 'a');
          mb.hidden = (modo !== 'b');
          this.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          pinta();
        });
        segLic.addEventListener('click', function(e){
          var b = e.target.closest('button[data-l]');
          if(!b) return;
          lic = +b.dataset.l;
          this.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          pinta();
        });
        monta();
        pinta();
      })();
      </script>
'''


# ==========================================================================
# S8 - La prueba de aceptacion
# ==========================================================================
ACEPTACION = u'''
      <div class="escena" id="esc-q8">
        <div class="escena-barra">
          <span class="escena-titulo">La prueba que acord&aacute;is antes</span>
          <div class="seg" id="q8-proy">
            <button type="button" data-p="0" aria-pressed="true">A &middot; riego</button>
            <button type="button" data-p="1">B &middot; aula</button>
            <button type="button" data-p="2">C &middot; l&aacute;mpara</button>
          </div>
        </div>
        <div class="lienzo">
          <div class="q8">
            <div class="q8-izq">
              <svg viewBox="0 0 460 250" id="svg-q8" role="img"
                   aria-label="La banda de aceptaci&oacute;n y c&oacute;mo caen dentro de ella un aparato bueno y uno malo"></svg>
            </div>
            <div class="q8-der">
              <div class="q8-fila">
                <label for="q8-tol">La banda es el objetivo &plusmn;</label>
                <input type="range" id="q8-tol" min="2" max="60" step="1" value="20">
                <span class="val" id="v-q8-tol"></span>
              </div>
              <div class="q8-fila">
                <label for="q8-des">Vuestra media se desv&iacute;a</label>
                <input type="range" id="q8-des" min="-40" max="40" step="1" value="0">
                <span class="val" id="v-q8-des"></span>
              </div>
              <div class="q8-fila">
                <label for="q8-sig">Repeti&eacute;ndolo var&iacute;a &plusmn;</label>
                <input type="range" id="q8-sig" min="1" max="40" step="1" value="18">
                <span class="val" id="v-q8-sig"></span>
              </div>
              <div class="q8-fila">
                <label for="q8-n">Se repite</label>
                <input type="range" id="q8-n" min="1" max="10" step="1" value="3">
                <span class="val" id="v-q8-n"></span>
              </div>
              <div class="q8-fila">
                <label for="q8-k">Tienen que salir</label>
                <input type="range" id="q8-k" min="1" max="10" step="1" value="3">
                <span class="val" id="v-q8-k"></span>
              </div>
              <div class="q8-tabla" id="q8-tabla"></div>
            </div>
          </div>
          <p class="q8-lee" id="q8-lee"></p>
        </div>
        <div class="pie" id="q8-pie"></div>
      </div>

      <style>
      .q8{display:flex;gap:18px;flex-wrap:wrap;align-items:flex-start}
      .q8-izq{flex:1 1 390px;min-width:300px}
      .q8-der{flex:1 1 288px;min-width:266px}
      .q8-fila{display:flex;align-items:center;gap:9px;flex-wrap:wrap;margin:0 0 9px;
        font-family:var(--f-m);font-size:12.5px;color:var(--ink)}
      .q8-fila label{min-width:142px}
      .q8-fila input[type="range"]{flex:1 1 92px;min-width:82px;max-width:148px;
        accent-color:var(--goo-azul)}
      .q8-fila .val{font-weight:500;color:var(--goo-azul);min-width:72px;text-align:right}
      .q8-tabla{border:1.5px solid var(--line);border-radius:2px;background:var(--surface);
        padding:9px 11px;font-family:var(--f-m);font-size:12.5px;line-height:1.7;margin-top:4px}
      .q8-tabla .f{display:flex;justify-content:space-between;gap:10px}
      .q8-tabla .f span:first-child{color:var(--ink-soft)}
      .q8-tabla .f b{color:var(--ink);font-weight:500;text-align:right}
      .q8-tabla .f.top{border-top:1px solid var(--line-soft);margin-top:5px;padding-top:5px}
      .q8-tabla .f.no b{color:var(--goo-rojo)}
      .q8-tabla .f.si b{color:var(--goo-verde)}
      .q8-lee{font-family:var(--f-m);font-size:13px;line-height:1.75;color:var(--ink-soft);margin:12px 0 0}
      .q8-lee b{color:var(--ink)}
      .q8-lee .grande{font-size:16px;color:var(--goo-azul);font-weight:500}
      .q8-lee .malo{color:var(--goo-rojo)}
      .q8-rot{fill:var(--ink-soft);font-family:var(--f-m);font-size:11px}
      .q8-etq{fill:var(--ink);font-family:var(--f-m);font-size:11.5px;font-weight:500}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-q8');
        if(!svg) return;
        var segProy = document.getElementById('q8-proy');
        var tabla = document.getElementById('q8-tabla');
        var lee = document.getElementById('q8-lee');
        var pie = document.getElementById('q8-pie');
        var ctl = {};
        ['tol', 'des', 'sig', 'n', 'k'].forEach(function(x){
          ctl[x] = document.getElementById('q8-' + x);
        });
        function V(x){ return +ctl[x].value; }

        var proy = 0;

        /* Las tres pruebas, una por proyecto. "obj" es lo que promete el
           grupo; "malo" es un aparato que de verdad esta mal, y la prueba
           tiene que suspenderlo. Los dos son medias: cada medida suelta cae
           alrededor de la suya. */
        var PRU = [
          {n: 'A \\u00b7 riego', frase: 'En una maceta seca, el riego echa <b>100 mL</b>',
           obj: 100, uni: 'mL', dec: 0, sig: 18, malo: 55,
           queMalo: 'una bomba a la que le falta presi\\u00f3n y echa 55 mL',
           porque: 'la bomba se controla con un <i>delay</i> y el caudal baja cuando baja el nivel '
                 + 'del dep\\u00f3sito y cuando se gastan las pilas'},
          {n: 'B \\u00b7 aula', frase: 'Con el aula llena, el piloto se pone rojo en <b>120 s</b>',
           obj: 120, uni: 's', dec: 0, sig: 25, malo: 260,
           queMalo: 'un aparato que tarda m\\u00e1s de cuatro minutos en enterarse',
           porque: 'el sensor tiene su propia inercia y el aire del aula no se mezcla igual dos '
                 + 'veces'},
          {n: 'C \\u00b7 l\\u00e1mpara', frase: 'Con la persiana bajada, sobre la mesa hay <b>340 lux</b>',
           obj: 340, uni: 'lux', dec: 0, sig: 12, malo: 230,
           queMalo: 'una l\\u00e1mpara que se queda en 230 lux',
           porque: 'depende de d\\u00f3nde pongas el luxómetro en la mesa, y de la luz que entra '
                 + 'aunque la persiana est\\u00e9 bajada'}
        ];

        function coma(x, d){
          var p = Math.abs(x).toFixed(d).split('.');
          var e = p[0].replace(/\\B(?=(\\d{3})+(?!\\d))/g, '.');
          return (x < 0 ? '\\u2212' : '') + e + (d ? ',' + p[1] : '');
        }
        function pc(x){ return coma(100 * x, 0) + ' %'; }
        function f(a, b, cl){
          return '<div class="f ' + (cl || '') + '"><span>' + a + '</span><b>' + b + '</b></div>';
        }

        /* ---- la campana, sin librerias ----
           erf por la aproximacion 7.1.26 de Abramowitz y Stegun: se equivoca
           como mucho en la septima cifra, o sea mucho menos de lo que se
           equivoca la propia medida. */
        function erf(x){
          var s = x < 0 ? -1 : 1;
          x = Math.abs(x);
          var t = 1 / (1 + 0.3275911 * x);
          var y = 1 - ((((1.061405429 * t - 1.453152027) * t + 1.421413741) * t
                      - 0.284496736) * t + 0.254829592) * t * Math.exp(-x * x);
          return s * y;
        }
        function Phi(z){ return 0.5 * (1 + erf(z / Math.SQRT2)); }
        function dentro(mu, sg, lo, hi){ return Phi((hi - mu) / sg) - Phi((lo - mu) / sg); }
        function comb(n, k){
          var r = 1;
          for(var i = 1; i <= k; i++) r = r * (n - k + i) / i;
          return r;
        }
        function alMenos(n, k, p){
          var s = 0;
          for(var j = k; j <= n; j++) s += comb(n, j) * Math.pow(p, j) * Math.pow(1 - p, n - j);
          return s;
        }
        function campana(mu, sg, x){
          return Math.exp(-(x - mu) * (x - mu) / (2 * sg * sg));
        }

        function calcula(){
          var P = PRU[proy];
          var n = V('n');
          var k = Math.min(V('k'), n);
          var lo = P.obj * (1 - V('tol') / 100), hi = P.obj * (1 + V('tol') / 100);
          var sg = Math.max(1e-6, P.obj * V('sig') / 100);
          var muB = P.obj * (1 + V('des') / 100);
          var muM = P.malo * (1 + V('des') / 100);
          var pB = dentro(muB, sg, lo, hi), pM = dentro(muM, sg, lo, hi);
          return {P: P, n: n, k: k, lo: lo, hi: hi, sg: sg, muB: muB, muM: muM,
                  pB: pB, pM: pM,
                  apB: alMenos(n, k, pB), apM: alMenos(n, k, pM)};
        }

        function pinta(){
          var c = calcula(), P = c.P;
          ctl.k.max = c.n;
          if(+ctl.k.value > c.n) ctl.k.value = c.n;
          document.getElementById('v-q8-tol').innerHTML = V('tol') + ' %';
          document.getElementById('v-q8-des').innerHTML = (V('des') > 0 ? '+' : '') + V('des') + ' %';
          document.getElementById('v-q8-sig').innerHTML = V('sig') + ' %';
          document.getElementById('v-q8-n').innerHTML = c.n + (c.n === 1 ? ' vez' : ' veces');
          document.getElementById('v-q8-k').innerHTML = c.k + ' de ' + c.n;

          /* ---------- las dos campanas y la banda ---------- */
          var x0 = 24, ancho = 416, base = 176, altoMax = 120;
          var lim0 = 0, lim1 = Math.max(P.obj, P.malo, c.hi) * 1.45;
          function X(v){ return x0 + ancho * (v - lim0) / (lim1 - lim0); }
          var s = [];
          s.push('<text x="' + x0 + '" y="16" class="q8-rot">'
               + 'd\\u00f3nde caen las medidas y d\\u00f3nde est\\u00e1 la banda</text>');
          /* la banda */
          s.push('<rect x="' + X(c.lo).toFixed(1) + '" y="' + (base - altoMax - 6) + '" width="'
               + Math.max(1, X(c.hi) - X(c.lo)).toFixed(1) + '" height="' + (altoMax + 6)
               + '" fill="var(--goo-verde)" opacity="0.13"/>');
          [[c.lo, 'm\\u00ednimo'], [c.hi, 'm\\u00e1ximo']].forEach(function(p){
            s.push('<line x1="' + X(p[0]).toFixed(1) + '" y1="' + (base - altoMax - 6) + '" x2="'
                 + X(p[0]).toFixed(1) + '" y2="' + base
                 + '" stroke="var(--goo-verde)" stroke-width="1.8" stroke-dasharray="4 3"/>');
            s.push('<text x="' + X(p[0]).toFixed(1) + '" y="' + (base - altoMax - 11)
                 + '" class="q8-rot" text-anchor="middle">' + coma(p[0], P.dec) + '</text>');
          });
          /* las dos campanas */
          [[c.muM, 'var(--goo-rojo)', 'el que est\\u00e1 mal'],
           [c.muB, 'var(--goo-azul)', 'el vuestro']].forEach(function(q){
            var d = [];
            for(var i = 0; i <= 120; i++){
              var v = lim0 + (lim1 - lim0) * i / 120;
              d.push((i ? 'L' : 'M') + X(v).toFixed(1) + ' '
                   + (base - altoMax * campana(q[0], c.sg, v)).toFixed(1));
            }
            s.push('<path d="' + d.join(' ') + '" fill="none" stroke="' + q[1]
                 + '" stroke-width="2.2"/>');
            s.push('<line x1="' + X(q[0]).toFixed(1) + '" y1="' + (base - altoMax) + '" x2="'
                 + X(q[0]).toFixed(1) + '" y2="' + base + '" stroke="' + q[1]
                 + '" stroke-width="1" opacity="0.5"/>');
          });
          s.push('<line x1="' + x0 + '" y1="' + base + '" x2="' + (x0 + ancho) + '" y2="' + base
               + '" stroke="var(--ink)" stroke-width="1.5"/>');
          for(var t = 0; t <= 4; t++){
            var vx = lim0 + (lim1 - lim0) * t / 4;
            s.push('<line x1="' + X(vx).toFixed(1) + '" y1="' + base + '" x2="' + X(vx).toFixed(1)
                 + '" y2="' + (base + 5) + '" stroke="var(--line)" stroke-width="1"/>');
            s.push('<text x="' + X(vx).toFixed(1) + '" y="' + (base + 18)
                 + '" class="q8-rot" text-anchor="middle">' + coma(vx, 0) + '</text>');
          }
          s.push('<text x="' + (x0 + ancho) + '" y="' + (base + 34)
               + '" class="q8-rot" text-anchor="end">' + P.uni + '</text>');
          s.push('<text x="' + x0 + '" y="' + (base + 52) + '" class="q8-etq" '
               + 'fill="var(--goo-azul)">el vuestro aprueba el ' + pc(c.apB) + ' de las veces</text>');
          s.push('<text x="' + x0 + '" y="' + (base + 70) + '" class="q8-etq" '
               + 'fill="var(--goo-rojo)">el que est\\u00e1 mal, ' + coma(P.malo, P.dec) + ' '
               + P.uni + ', aprueba el ' + pc(c.apM) + '</text>');
          svg.innerHTML = s.join('');

          /* ---------- la cuenta escrita ---------- */
          tabla.innerHTML =
            f('la banda va de', coma(c.lo, P.dec) + ' a ' + coma(c.hi, P.dec) + ' ' + P.uni)
          + f('vuestra media', coma(c.muB, P.dec) + ' ' + P.uni)
          + f('una medida cae dentro', pc(c.pB))
          + f('aprueba la prueba entera', pc(c.apB), 'top ' + (c.apB >= 0.8 ? 'si' : 'no'))
          + f('y el aparato malo aprueba', pc(c.apM), c.apM <= 0.2 ? 'si' : 'no')
          + f('la prueba distingue', (c.apB >= 0.8 && c.apM <= 0.2) ? 's\\u00ed' : 'no',
              'top ' + ((c.apB >= 0.8 && c.apM <= 0.2) ? 'si' : 'no'));

          /* ---------- el veredicto ---------- */
          var v;
          if(c.apB >= 0.8 && c.apM <= 0.2){
            v = '<span class="grande">Esta prueba sirve: aprueba el ' + pc(c.apB)
              + ' de las veces si el aparato est&aacute; bien y solo el ' + pc(c.apM)
              + ' si est&aacute; mal.</span> Que es lo &uacute;nico que se le pide a una prueba: '
              + '<b>que distinga</b>. Fíjate en que no hace falta que apruebe el 100 %: eso solo pasa '
              + 'si la banda es tan ancha que tambi&eacute;n aprueba el malo.';
          } else if(c.apB < 0.8 && c.apM <= 0.2){
            v = '<span class="grande malo">Con esta prueba suspend&eacute;is el '
              + pc(1 - c.apB) + ' de las veces, y eso que el aparato est&aacute; bien.</span> '
              + 'O la banda es demasiado estrecha para lo que var&iacute;a la medida, o est&aacute;is '
              + 'exigiendo que salgan ' + c.k + ' de ' + c.n + ' seguidas. Ojo con esto &uacute;ltimo: '
              + 'si una sola sale bien el ' + pc(c.pB) + ' de las veces, exigir ' + c.n + ' seguidas '
              + 'es pedir ' + pc(Math.pow(c.pB, c.n)) + '. <b>Cada repetici&oacute;n que a&ntilde;ades '
              + 'os pone m&aacute;s dif&iacute;cil aprobar, no m&aacute;s f&aacute;cil.</b>';
          } else if(c.apB >= 0.8){
            v = '<span class="grande malo">Esta prueba la aprueba tambi&eacute;n '
              + P.queMalo + ', el ' + pc(c.apM) + ' de las veces.</span> O sea que no comprueba '
              + 'nada: la pasar&iacute;a cualquier cosa. Una prueba que no puede suspender a nadie '
              + 'es un tr&aacute;mite. <b>Estrecha la banda hasta que el malo se caiga</b>, y mira '
              + 'qu&eacute; le pasa de paso al vuestro.';
          } else {
            v = '<span class="grande malo">Esta prueba suspende a los dos.</span> El vuestro aprueba '
              + 'el ' + pc(c.apB) + ' y el malo el ' + pc(c.apM) + ': no sirve ni para aceptar ni '
              + 'para distinguir. Mira d&oacute;nde est&aacute; vuestra media respecto de la banda: '
              + 'si est&aacute; fuera, lo que hay que arreglar es el aparato, no la prueba.';
          }
          lee.innerHTML = v;

          pie.innerHTML =
            'Lo que promet&eacute;is: <b>' + P.frase + '</b>. Una medida nunca sale dos veces igual '
          + '(' + P.porque + '), as&iacute; que la escena supone que las medidas se reparten en '
          + 'campana alrededor de vuestra media, con la anchura que pon&eacute;is en el mando. De '
          + 'ah&iacute; salen las dos probabilidades: la de que <b>una</b> medida caiga dentro de la '
          + 'banda, y la de que caigan <b>' + c.k + ' de ' + c.n + '</b>, que es la binomial. '
          + '<b>La campana es un modelo</b>, no una ley: la usamos porque es la forma que suele '
          + 'tener un mont&oacute;n de medidas de lo mismo, y porque deja ver lo importante. '
          + 'Lo importante es que hay <b>dos maneras de equivocarse</b>: suspender algo que '
          + 'est&aacute; bien y aprobar algo que est&aacute; mal, y estrechar la banda cambia una '
          + 'por la otra.';
        }

        segProy.addEventListener('click', function(e){
          var b = e.target.closest('button[data-p]');
          if(!b) return;
          proy = +b.dataset.p;
          this.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          ctl.sig.value = PRU[proy].sig;
          pinta();
        });
        ['tol', 'des', 'sig', 'n', 'k'].forEach(function(x){
          ctl[x].addEventListener('input', pinta);
        });
        pinta();
      })();
      </script>
'''
