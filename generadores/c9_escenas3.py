# -*- coding: utf-8 -*-
"""4.o Tecnologia - Tema 9 - Escenas de las sesiones 5 y 6.

  REQUISITOS (S5)  "De lo que dijo a lo que se mide". Tres destinatarios de
      verdad -el huerto del instituto, la vecina que se va quince dias y el
      aula de infantil-, cada uno con las frases LITERALES que soltaria en la
      entrevista. Cada frase se traduce a una de tres cosas: un requisito con
      su numero, una restriccion o una comprobacion que no es un numero. La
      escena coge el aparato que tienen montado en el taller (los mandos de la
      derecha son SU diseno, no el del destinatario) y calcula si pasa cada
      requisito y por cuanto margen.

      La cadena de cuentas es larga a proposito, porque es la que hay que
      saber hacer: superficie del bancal x lamina de riego -> litros al dia;
      litros al dia / capacidad del deposito -> dias; miliamperios x voltios x
      horas -> vatios hora al dia; vatios hora guardados / consumo -> dias de
      pila. Y una regla de senalizacion para la senal luminosa.

      Lo que ensena: el MISMO aparato aprueba con la vecina y suspende en el
      huerto, y no porque sea peor. El requisito lo pone la persona.

  MANTENIMIENTO (S6)  "Cinco anos en manos de otro". Simula dia a dia los
      1.825 dias siguientes a la entrega: se gasta el agua, se gastan las
      pilas, se come la sonda. Cuando algo se agota, el aparato se PARA hasta
      que alguien va, y cuanto tarda ese alguien depende de quien sea y de
      donde este el recambio. Hay una fecha de abandono en el dia 270: la
      suposicion es que para entonces ya no se pasa por alli ninguno de los
      autores. Es la suposicion mas importante de la escena y se dice en el pie.

      Saca las horas de otra persona, los euros a cinco anos, los dias parado
      y la disponibilidad. Lo que ensena: el mantenimiento no se decide
      manteniendo, se decide DISENANDO.

Todo numero de la pantalla sale de una cuenta declarada en la propia escena.
Los datos de partida estan declarados con su origen, y lo que es orden de
magnitud nuestro lo dice.

Clases e ids con prefijo q5-, q6-. Nada que empiece por test- ni por ses-.
Estas cadenas NO pasan por ningun formateo con %.
"""

# ==========================================================================
# S5 - De lo que dijo a lo que se mide
# ==========================================================================
REQUISITOS = u'''
      <div class="escena" id="esc-q5">
        <div class="escena-barra">
          <span class="escena-titulo">De lo que dijo a lo que se mide</span>
          <div class="seg" id="q5-dest">
            <button type="button" data-d="0" aria-pressed="true">El huerto</button>
            <button type="button" data-d="1">La vecina</button>
            <button type="button" data-d="2">El aula de infantil</button>
          </div>
        </div>
        <div class="lienzo">
          <div class="q5">
            <div class="q5-izq">
              <svg viewBox="0 0 460 200" id="svg-q5" role="img"
                   aria-label="Lo que pidi&oacute; cada persona y lo que da vuestro aparato, requisito a requisito"></svg>
              <div class="q5-frases" id="q5-frases"></div>
            </div>
            <div class="q5-der">
              <p class="q5-rotder">Vuestro aparato, tal y como est&aacute; en el taller</p>
              <div class="q5-fila">
                <label for="q5-pilas">Pilas AA que lleva</label>
                <input type="range" id="q5-pilas" min="2" max="8" step="1" value="4">
                <span class="val" id="v-q5-pilas"></span>
              </div>
              <div class="q5-fila" id="q5-filadep">
                <label for="q5-dep">Dep&oacute;sito de agua</label>
                <input type="range" id="q5-dep" min="0.5" max="20" step="0.5" value="1.5">
                <span class="val" id="v-q5-dep"></span>
              </div>
              <div class="q5-fila">
                <label for="q5-med">Veces que mide al d&iacute;a</label>
                <input type="range" id="q5-med" min="1" max="96" step="1" value="24">
                <span class="val" id="v-q5-med"></span>
              </div>
              <div class="q5-fila" id="q5-filaalt">
                <label for="q5-alt">Alto de la se&ntilde;al</label>
                <input type="range" id="q5-alt" min="4" max="80" step="1" value="8">
                <span class="val" id="v-q5-alt"></span>
              </div>
              <div class="q5-fila">
                <label class="q5-check"><input type="checkbox" id="q5-duerme">
                  La placa duerme entre medidas</label>
              </div>
              <div class="q5-tabla" id="q5-tabla"></div>
            </div>
          </div>
          <p class="q5-lee" id="q5-lee"></p>
        </div>
        <div class="pie" id="q5-pie"></div>
      </div>

      <style>
      .q5{display:flex;gap:18px;flex-wrap:wrap;align-items:flex-start}
      .q5-izq{flex:1 1 400px;min-width:300px}
      .q5-der{flex:1 1 286px;min-width:264px}
      .q5-rotder{font-family:var(--f-m);font-size:11px;letter-spacing:.08em;text-transform:uppercase;
        color:var(--ink-soft);margin:0 0 9px}
      .q5-fila{display:flex;align-items:center;gap:9px;flex-wrap:wrap;margin:0 0 9px;
        font-family:var(--f-m);font-size:12.5px;color:var(--ink)}
      /* Ojo, lo mismo que en la escena del retorno: display:flex le gana al
         [hidden] del navegador, y la fila se quedaba a la vista. */
      .q5-fila[hidden]{display:none}
      .q5-fila label{min-width:138px}
      .q5-fila label.q5-check{min-width:0;display:flex;align-items:center;gap:7px;cursor:pointer}
      .q5-fila input[type="range"]{flex:1 1 92px;min-width:82px;max-width:148px;
        accent-color:var(--goo-azul)}
      .q5-fila .val{font-weight:500;color:var(--goo-azul);min-width:70px;text-align:right}
      .q5-tabla{border:1.5px solid var(--line);border-radius:2px;background:var(--surface);
        padding:9px 11px;font-family:var(--f-m);font-size:12.5px;line-height:1.7;margin-top:4px}
      .q5-tabla .f{display:flex;justify-content:space-between;gap:10px}
      .q5-tabla .f span:first-child{color:var(--ink-soft)}
      .q5-tabla .f b{color:var(--ink);font-weight:500;text-align:right}
      .q5-tabla .f.top{border-top:1px solid var(--line-soft);margin-top:5px;padding-top:5px}
      .q5-tabla .f.no b{color:var(--goo-rojo)}
      .q5-tabla .f.si b{color:var(--goo-verde)}
      .q5-frases{margin-top:12px;border-top:1px solid var(--line-soft);padding-top:10px}
      .q5-fr{display:flex;gap:9px;margin:0 0 9px;font-size:14px;line-height:1.55}
      .q5-fr .et{flex:none;font-family:var(--f-m);font-size:9.5px;letter-spacing:.07em;
        text-transform:uppercase;padding:2px 6px;border-radius:2px;margin-top:3px;height:16px;
        line-height:12px;color:#fff;white-space:nowrap}
      .q5-fr .et.req{background:var(--goo-azul)}
      .q5-fr .et.res{background:var(--ink-soft)}
      .q5-fr .et.pru{background:var(--goo-verde)}
      .q5-fr i{color:var(--ink);font-style:italic}
      .q5-fr small{display:block;color:var(--ink-soft);font-family:var(--f-m);font-size:11.5px;
        line-height:1.5;margin-top:2px}
      .q5-lee{font-family:var(--f-m);font-size:13px;line-height:1.75;color:var(--ink-soft);margin:12px 0 0}
      .q5-lee b{color:var(--ink)}
      .q5-lee .grande{font-size:16px;color:var(--goo-azul);font-weight:500}
      .q5-lee .malo{color:var(--goo-rojo)}
      .q5-rot{fill:var(--ink-soft);font-family:var(--f-m);font-size:11px}
      .q5-etq{fill:var(--ink);font-family:var(--f-m);font-size:11.5px;font-weight:500}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-q5');
        if(!svg) return;
        var segDest = document.getElementById('q5-dest');
        var filaDep = document.getElementById('q5-filadep');
        var filaAlt = document.getElementById('q5-filaalt');
        var tabla = document.getElementById('q5-tabla');
        var frases = document.getElementById('q5-frases');
        var lee = document.getElementById('q5-lee');
        var pie = document.getElementById('q5-pie');
        var duerme = document.getElementById('q5-duerme');
        var ctl = {};
        ['pilas', 'dep', 'med', 'alt'].forEach(function(k){
          ctl[k] = document.getElementById('q5-' + k);
        });
        function V(k){ return +ctl[k].value; }

        /* ---- constantes DECLARADAS ----
           Las tres primeras se midieron en la sesion 2 y se repiten aqui a
           proposito: es el mismo aparato. */
        var VOLT = 5;               /* V de la placa */
        var mA_DESPIERTA = 45;      /* placa Uno despierta, sin dormir nunca */
        var mA_DORMIDA = 12;        /* lo minimo de una Uno: regulador, LED y chip USB */
        var SEG_MEDIDA = 8;         /* segundos que tarda una medida: arrancar el sensor y decidir */
        var mA_BOMBA = 500;         /* bomba sumergible de 3-6 V */
        var CAUDAL = 33;            /* mL por segundo, o sea unos 120 L/h */
        var Wh_PILA = 3.7;          /* una AA alcalina: 2.500 mAh a 1,5 V */
        var REGLA = 200;            /* se lee bien a 200 veces el alto del rotulo */

        var dest = 0;

        function coma(x, d){
          if(!isFinite(x)) return '\\u221e';
          var p = Math.abs(x).toFixed(d).split('.');
          var e = p[0].replace(/\\B(?=(\\d{3})+(?!\\d))/g, '.');
          return (x < 0 ? '\\u2212' : '') + e + (d ? ',' + p[1] : '');
        }
        function f(a, b, cl){
          return '<div class="f ' + (cl || '') + '"><span>' + a + '</span><b>' + b + '</b></div>';
        }

        /* ---------------------------------------------------------------
           Los tres destinatarios. "dijo" son frases de entrevista: la
           traduccion a numero es NUESTRA, y por eso hay que volver a
           ensenarsela a la persona antes de darla por buena.
        --------------------------------------------------------------- */
        var DEST = [
          {n: 'El huerto del instituto', proy: 'A \\u00b7 riego',
           quien: 'la profesora que lleva el huerto',
           riega: true, senal: false,
           sup: 2.0, lam: 3.0,          /* m2 de bancal y mm de riego al dia en agosto */
           sale: '2 m\\u00b2 de bancal \\u00d7 3 mm al d\\u00eda = 6,0 L al d\\u00eda',
           reqs: [
             {n: 'Lo que da el dep\\u00f3sito', c: 'El dep\\u00f3sito', pide: 43, uni: 'd\\u00edas', dec: 1, mas: true,
              v: 'diasAgua'},
             {n: 'Lo que dan las pilas', c: 'Las pilas', pide: 43, uni: 'd\\u00edas', dec: 1, mas: true,
              v: 'diasPila'}
           ],
           dijo: [
             {t: 'req', c: '\\u00abDel 20 de julio al 1 de septiembre aqu\\u00ed no viene nadie.\\u00bb',
              d: 'son 43 d\\u00edas. Es el requisito que manda: el dep\\u00f3sito y las pilas tienen '
               + 'que llegar a 43, no a \\u00abbastantes\\u00bb.'},
             {t: 'res', c: '\\u00abEl enchufe m\\u00e1s cercano est\\u00e1 en el taller, a cuarenta metros.\\u00bb',
              d: 'restricci\\u00f3n: no la pod\\u00e9is cambiar. O va a pilas, o a placa solar, o hay que '
               + 'pedir una toma, y eso ya no es un problema t\\u00e9cnico.'},
             {t: 'pru', c: '\\u00abSi se queda sin agua, la bomba se quema en dos ciclos.\\u00bb',
              d: 'no es un n\\u00famero: es una <b>comprobaci\\u00f3n</b>. Se vac\\u00eda el dep\\u00f3sito '
               + 'delante de ella y la bomba no puede arrancar. O pasa o no pasa.'},
             {t: 'pru', c: '\\u00abLo que se me muere no es la lechuga: son los semilleros.\\u00bb',
              d: 'esta es la frase cara. El problema no era el que hab\\u00edais supuesto, y cambia '
               + 'd\\u00f3nde va la sonda y cu\\u00e1nta agua hace falta. Hab\\u00eda que haberlo '
               + 'preguntado en octubre.'}
           ]},
          {n: 'La vecina del 3.\\u00ba B', proy: 'A \\u00b7 riego de macetas',
           quien: 'una vecina que se va quince d\\u00edas en agosto',
           riega: true, senal: false,
           sup: 0.127, lam: 4.0,       /* cinco macetas de 18 cm de boca */
           sale: '5 macetas de 18 cm \\u2192 0,127 m\\u00b2 \\u00d7 4 mm al d\\u00eda = 0,51 L al d\\u00eda',
           reqs: [
             {n: 'Lo que da el dep\\u00f3sito', c: 'El dep\\u00f3sito', pide: 15, uni: 'd\\u00edas', dec: 1, mas: true,
              v: 'diasAgua'},
             {n: 'Lo que dan las pilas', c: 'Las pilas', pide: 15, uni: 'd\\u00edas', dec: 1, mas: true,
              v: 'diasPila'},
             {n: 'Agua de cada riego', c: 'Cada riego', pide: 100, uni: 'mL', dec: 0, mas: false,
              v: 'mlRiego'}
           ],
           dijo: [
             {t: 'req', c: '\\u00abMe voy el 1 de agosto y vuelvo el 16.\\u00bb',
              d: 'quince d\\u00edas. Ni catorce ni \\u00abunas semanas\\u00bb: hay una fecha, y por eso '
               + 'se puede comprobar.'},
             {t: 'req', c: '\\u00abComo me manches el parqu\\u00e9, te lo devuelvo.\\u00bb',
              d: 'esto s\\u00ed es un n\\u00famero, aunque ella no lo diga as\\u00ed: una maceta de 18 cm '
               + 'absorbe del orden de 100 mL de una vez. M\\u00e1s de eso, se sale por abajo.'},
             {t: 'res', c: '\\u00abPor el pasillo no me pasa un cable, que ah\\u00ed paso la fregona.\\u00bb',
              d: 'restricci\\u00f3n. Hay enchufe en la casa, pero no donde hace falta: el aparato '
               + 'tiene que ir a pilas aunque haya corriente a tres metros.'},
             {t: 'pru', c: '\\u00abY cuando vuelva, quiero saber si ha funcionado.\\u00bb',
              d: 'no es un n\\u00famero: es un <b>LED que se queda encendido</b> si hubo un fallo, o '
               + 'una cuenta de riegos en la pantalla. Se comprueba provocando un fallo delante '
               + 'de ella.'}
           ]},
          {n: 'El aula de infantil de al lado', proy: 'B \\u00b7 aviso de ventilaci\\u00f3n',
           quien: 'la maestra de 4 a\\u00f1os',
           riega: false, senal: true,
           sup: 0, lam: 0,
           sale: 'aqu\\u00ed no hay bomba: el aparato solo mide y avisa',
           reqs: [
             {n: 'Distancia a la que se entiende', c: 'Se entiende a', pide: 6, uni: 'm', dec: 1, mas: true,
              v: 'dist'},
             {n: 'Lo que dan las pilas', c: 'Las pilas', pide: 90, uni: 'd\\u00edas', dec: 1, mas: true,
              v: 'diasPila'}
           ],
           dijo: [
             {t: 'req', c: '\\u00abYo estoy en mi mesa, al fondo, y no me voy a levantar a mirarlo.\\u00bb',
              d: 'mide la clase: son 6 metros. Un r\\u00f3tulo se lee a unas <b>200 veces su '
               + 'altura</b>, as\\u00ed que 6 m piden 30 mm. Los d\\u00edgitos de la pantallita miden 8.'},
             {t: 'req', c: '\\u00abUn trimestre sin que yo tenga que tocar nada.\\u00bb',
              d: '90 d\\u00edas. Y ojo, porque el enchufe libre que hay lo usa el proyector.'},
             {t: 'res', c: '\\u00abTienen cuatro a\\u00f1os: lo que est\\u00e9 a su altura, lo tocan.\\u00bb',
              d: 'restricci\\u00f3n: por encima de 1,40 m y sin cables colgando. No se negocia y no '
               + 'depende de vosotros.'},
             {t: 'res', c: '\\u00abY que no pite, que me los desconcentra.\\u00bb',
              d: 'restricci\\u00f3n: fuera el zumbador. Toda la informaci\\u00f3n tiene que caber en '
               + 'algo que se vea.'},
             {t: 'pru', c: '\\u00abNo leen. Ninguno.\\u00bb',
              d: 'no es un n\\u00famero: la se\\u00f1al tiene que entenderse <b>sin letras</b>. Se '
               + 'comprueba ense\\u00f1\\u00e1ndosela a un ni\\u00f1o de la clase y pregunt\\u00e1ndole '
               + 'qu\\u00e9 hay que hacer.'}
           ]}
        ];

        /* ---- la cuenta entera, en un sitio ---- */
        function calcula(){
          var D = DEST[dest];
          var med = V('med');
          var sDesp = duerme.checked ? Math.min(86400, med * SEG_MEDIDA) : 86400;
          var sDorm = 86400 - sDesp;
          var whPlaca = VOLT * (mA_DESPIERTA * sDesp + mA_DORMIDA * sDorm) / 1000 / 3600;

          var litros = D.sup * D.lam;            /* m2 x mm/dia = L/dia */
          var mlDia = litros * 1000;
          var sBomba = mlDia / CAUDAL;
          var whBomba = VOLT * mA_BOMBA * sBomba / 1000 / 3600;
          var whDia = whPlaca + whBomba;

          var whPilas = Wh_PILA * V('pilas');
          var diasPila = whDia > 0 ? whPilas / whDia : Infinity;
          var diasAgua = mlDia > 0 ? V('dep') * 1000 / mlDia : Infinity;
          var mlRiego = med > 0 ? mlDia / med : mlDia;
          var dist = V('alt') / 1000 * REGLA;

          var c = {D: D, litros: litros, mlDia: mlDia, sBomba: sBomba, whPlaca: whPlaca,
                   whBomba: whBomba, whDia: whDia, whPilas: whPilas, diasPila: diasPila,
                   diasAgua: diasAgua, mlRiego: mlRiego, dist: dist,
                   aguanta: Math.min(diasPila, D.riega ? diasAgua : Infinity)};

          c.reqs = D.reqs.map(function(R){
            var da = c[R.v];
            /* razon = lo que das dividido entre lo que te piden, y al reves
               cuando lo bueno es que salga poco */
            var razon = R.mas ? da / R.pide : R.pide / da;
            return {R: R, da: da, razon: razon, pasa: razon >= 1};
          });
          c.pasan = c.reqs.filter(function(x){ return x.pasa; }).length;
          return c;
        }

        function pinta(){
          var c = calcula(), D = c.D;
          filaDep.hidden = !D.riega;
          filaAlt.hidden = !D.senal;
          document.getElementById('v-q5-pilas').innerHTML = V('pilas') + ' pilas';
          document.getElementById('v-q5-dep').innerHTML = coma(V('dep'), 1) + ' L';
          document.getElementById('v-q5-med').innerHTML = V('med')
            + (V('med') === 1 ? ' vez' : ' veces');
          document.getElementById('v-q5-alt').innerHTML = V('alt') + ' mm';

          /* ---------- una barra por requisito ----------
             Cada fila lleva su rotulo arriba, la barra en medio y la cuenta
             debajo. La barra no comparte linea con el rotulo a proposito: con
             nombres de veinte letras se pisaban. */
          var x0 = 8, ancho = 444, fila = 50, y0 = 22;
          var alto = y0 + c.reqs.length * fila + 22;
          svg.setAttribute('viewBox', '0 0 460 ' + alto);
          var cero = x0 + ancho * 0.45;       /* donde cae "justo lo que pide" */
          var s = [];
          s.push('<text x="' + x0 + '" y="13" class="q5-rot">lo que le piden, y lo que da '
               + 'vuestro aparato</text>');
          s.push('<line x1="' + cero + '" y1="18" x2="' + cero + '" y2="' + (alto - 17)
               + '" stroke="var(--ink)" stroke-width="1.5"/>');
          s.push('<text x="' + cero + '" y="' + (alto - 4)
               + '" class="q5-rot" text-anchor="middle">justo lo que pide</text>');

          c.reqs.forEach(function(x, j){
            var y = y0 + j * fila;
            /* escala logaritmica: diez veces menos cae en el extremo izquierdo,
               cien veces mas en el derecho. Sin log no se veria nada, porque
               los casos se llevan dos ordenes de magnitud. */
            var l = Math.log(Math.max(x.razon, 1e-6)) / Math.LN10;
            var p = Math.max(-1, Math.min(2, l));
            var px = cero + (p >= 0 ? (x0 + ancho - cero) * p / 2 : (cero - x0) * p);
            var col = x.pasa ? 'var(--goo-verde)' : 'var(--goo-rojo)';
            s.push('<text x="' + x0 + '" y="' + (y + 11) + '" class="q5-etq">'
                 + x.R.c + '</text>');
            s.push('<text x="' + (x0 + ancho) + '" y="' + (y + 11)
                 + '" class="q5-etq" text-anchor="end" fill="' + col + '">'
                 + (x.pasa ? '\\u00d7' + coma(x.razon, 1) + ' de margen'
                           : 'se queda en \\u00d7' + coma(x.razon, 2)) + '</text>');
            /* ancho minimo de 2,5 px: si sale justo, la barra mide cero y no se
               veria de que lado ha caido */
            var w = Math.max(2.5, Math.abs(px - cero));
            s.push('<rect x="' + (px >= cero ? cero : cero - w).toFixed(1) + '" y="' + (y + 18)
                 + '" width="' + w.toFixed(1)
                 + '" height="13" fill="' + col + '" opacity="0.85"/>');
            s.push('<text x="' + x0 + '" y="' + (y + 44) + '" class="q5-rot">pide '
                 + coma(x.R.pide, x.R.dec) + ' ' + x.R.uni + ' \\u00b7 da '
                 + coma(x.da, x.R.dec) + ' ' + x.R.uni + '</text>');
          });
          svg.innerHTML = s.join('');

          /* ---------- las frases, y en qu\\u00e9 se convierte cada una ---------- */
          var ET = {req: ['req', 'requisito'], res: ['res', 'restricci\\u00f3n'],
                    pru: ['pru', 'se comprueba']};
          frases.innerHTML = '<p class="q5-rot" style="margin:0 0 9px">Lo que dijo '
            + D.quien + ', y en qu\\u00e9 se convierte cada frase</p>'
            + D.dijo.map(function(x){
                return '<div class="q5-fr"><span class="et ' + ET[x.t][0] + '">' + ET[x.t][1]
                     + '</span><span><i>' + x.c + '</i><small>' + x.d + '</small></span></div>';
              }).join('');

          /* ---------- la cuenta escrita ---------- */
          var t = '';
          if(D.riega){
            t += f('pide al d\\u00eda', coma(c.litros, 2) + ' L')
              +  f('la bomba trabaja', coma(c.sBomba, 0) + ' s al d\\u00eda')
              +  f('echa de una vez', coma(c.mlRiego, 0) + ' mL');
          }
          t += f('la placa gasta', coma(c.whPlaca, 2) + ' Wh al d\\u00eda');
          if(D.riega) t += f('la bomba gasta', coma(c.whBomba, 2) + ' Wh al d\\u00eda');
          t += f('gasta al d\\u00eda', coma(c.whDia, 2) + ' Wh', 'top')
            +  f('lleva guardados', coma(c.whPilas, 1) + ' Wh')
            +  f('lo que dan las pilas', coma(c.diasPila, 1) + ' d\\u00edas');
          if(D.riega) t += f('lo que da el dep\\u00f3sito', coma(c.diasAgua, 1) + ' d\\u00edas');
          if(D.senal) t += f('se entiende a', coma(c.dist, 1) + ' m');
          t += f('aguanta sin que vaya nadie', coma(c.aguanta, 1) + ' d\\u00edas', 'top')
            +  f('requisitos que cumple', c.pasan + ' de ' + c.reqs.length,
                 c.pasan === c.reqs.length ? 'si' : 'no');
          tabla.innerHTML = t;

          /* ---------- el veredicto ---------- */
          var peor = null;
          c.reqs.forEach(function(x){ if(!peor || x.razon < peor.razon) peor = x; });
          var v;
          if(c.pasan === c.reqs.length){
            var npru = D.dijo.filter(function(x){ return x.t === 'pru'; }).length;
            v = '<span class="grande">Con este aparato cumpl\\u00eds los ' + c.reqs.length
              + ' requisitos que se pueden medir.</span> El m\\u00e1s justo es <b>'
              + peor.R.n.toLowerCase() + '</b>, con \\u00d7' + coma(peor.razon, 2)
              + ' de margen. Y abajo ' + (npru === 1
                  ? 'queda una frase que <b>no es un n\\u00famero</b>: esa se comprueba '
                    + 'ense\\u00f1\\u00e1ndosela a '
                  : 'quedan ' + npru + ' frases que <b>no son n\\u00fameros</b>: esas se '
                    + 'comprueban ense\\u00f1\\u00e1ndoselas a ')
              + D.quien + ', y de eso va la sesi\\u00f3n 8.';
          } else {
            v = '<span class="grande malo">Suspende ' + (c.reqs.length - c.pasan) + ' de '
              + c.reqs.length + ' requisitos.</span> El que peor va es <b>' + peor.R.n.toLowerCase()
              + '</b>: pide ' + coma(peor.R.pide, peor.R.dec) + ' ' + peor.R.uni + ' y da '
              + coma(peor.da, peor.R.dec) + ' ' + peor.R.uni + ', o sea que se queda en <b>\\u00d7'
              + coma(peor.razon, 2) + '</b>. Para llegar har\\u00edan falta <b>\\u00d7'
              + coma(1 / peor.razon, 1) + '</b> de lo que tiene ahora. Mira si los mandos de la '
              + 'derecha dan para tanto: a veces no dan, y entonces lo que hay que cambiar '
              + '<b>no es un mando, es el dise\\u00f1o</b>.';
          }
          lee.innerHTML = v;

          pie.innerHTML =
            'Los mandos de la derecha son <b>vuestro aparato</b>; los n\\u00fameros de la izquierda '
          + 'los ha puesto ' + D.quien + '. Las cuentas: el agua que pide la planta es '
          + '<b>superficie \\u00d7 l\\u00e1mina de riego</b> (' + D.sale + '); lo que aguanta el '
          + 'dep\\u00f3sito es <b>litros guardados \\u00f7 litros al d\\u00eda</b>; la energ\\u00eda es '
          + '<b>Wh = V \\u00d7 A \\u00d7 horas</b> con la placa a ' + mA_DESPIERTA + ' mA despierta y '
          + mA_DORMIDA + ' mA dormida, la bomba a ' + mA_BOMBA + ' mA y una AA alcalina con '
          + coma(Wh_PILA, 1) + ' Wh; y la se\\u00f1al se lee a <b>' + REGLA
          + ' veces su altura</b>. <b>Esa \\u00faltima regla es criterio nuestro</b>, una regla de '
          + 'dedo de se\\u00f1alizaci\\u00f3n, no una norma: sirve para ver que la pantallita de 8 mm '
          + 'no llega al fondo de la clase, no para certificar nada. Los litros al d\\u00eda de las '
          + 'plantas son orden de magnitud de verano; los d\\u00edas y los metros los dijo la persona, '
          + 'y esos no se discuten.';
        }

        segDest.addEventListener('click', function(e){
          var b = e.target.closest('button[data-d]');
          if(!b) return;
          dest = +b.dataset.d;
          this.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          pinta();
        });
        ['pilas', 'dep', 'med', 'alt'].forEach(function(k){
          ctl[k].addEventListener('input', pinta);
        });
        duerme.addEventListener('change', pinta);
        pinta();
      })();
      </script>
'''


# ==========================================================================
# S6 - Cinco anos en manos de otro
# ==========================================================================
MANTENIMIENTO = u'''
      <div class="escena" id="esc-q6">
        <div class="escena-barra">
          <span class="escena-titulo">Cinco a&ntilde;os en manos de otro</span>
          <div class="seg" id="q6-proy">
            <button type="button" data-p="0" aria-pressed="true">A &middot; riego</button>
            <button type="button" data-p="1">B &middot; aula</button>
            <button type="button" data-p="2">C &middot; l&aacute;mpara</button>
          </div>
        </div>
        <div class="lienzo">
          <div class="q6">
            <div class="q6-izq">
              <svg viewBox="0 0 460 216" id="svg-q6" role="img"
                   aria-label="Cinco a&ntilde;os d&iacute;a a d&iacute;a: cu&aacute;ndo funciona el aparato y cu&aacute;ndo est&aacute; parado"></svg>
            </div>
            <div class="q6-der">
              <div class="q6-fila">
                <label>Qui&eacute;n lo mantiene</label>
                <div class="seg" id="q6-quien">
                  <button type="button" data-q="0" aria-pressed="true">Vosotros</button>
                  <button type="button" data-q="1">El conserje</button>
                  <button type="button" data-q="2">El departamento</button>
                </div>
              </div>
              <div class="q6-fila">
                <label>De d&oacute;nde saca la energ&iacute;a</label>
                <div class="seg" id="q6-alim">
                  <button type="button" data-a="0" aria-pressed="true">Pilas</button>
                  <button type="button" data-a="1">Enchufe</button>
                </div>
              </div>
              <div class="q6-fila" id="q6-filasonda">
                <label>La sonda de humedad</label>
                <div class="seg" id="q6-sonda">
                  <button type="button" data-s="0" aria-pressed="true">Dos clavos</button>
                  <button type="button" data-s="1">Clavos, con corte</button>
                  <button type="button" data-s="2">Capacitiva</button>
                </div>
              </div>
              <div class="q6-fila" id="q6-filadep">
                <label for="q6-dep">Dep&oacute;sito de agua</label>
                <input type="range" id="q6-dep" min="1" max="200" step="1" value="2">
                <span class="val" id="v-q6-dep"></span>
              </div>
              <div class="q6-fila">
                <label for="q6-rec">El recambio est&aacute; a</label>
                <input type="range" id="q6-rec" min="0" max="21" step="1" value="0">
                <span class="val" id="v-q6-rec"></span>
              </div>
              <div class="q6-tabla" id="q6-tabla"></div>
            </div>
          </div>
          <p class="q6-lee" id="q6-lee"></p>
        </div>
        <div class="pie" id="q6-pie"></div>
      </div>

      <style>
      .q6{display:flex;gap:18px;flex-wrap:wrap;align-items:flex-start}
      .q6-izq{flex:1 1 390px;min-width:300px}
      .q6-der{flex:1 1 292px;min-width:268px}
      .q6-fila{display:flex;align-items:center;gap:9px;flex-wrap:wrap;margin:0 0 9px;
        font-family:var(--f-m);font-size:12.5px;color:var(--ink)}
      .q6-fila[hidden]{display:none}
      .q6-fila label{min-width:136px}
      .q6-fila input[type="range"]{flex:1 1 92px;min-width:82px;max-width:148px;
        accent-color:var(--goo-azul)}
      .q6-fila .val{font-weight:500;color:var(--goo-azul);min-width:66px;text-align:right}
      .q6-fila .seg button{padding:5px 8px;font-size:11px}
      .q6-tabla{border:1.5px solid var(--line);border-radius:2px;background:var(--surface);
        padding:9px 11px;font-family:var(--f-m);font-size:12.5px;line-height:1.7;margin-top:4px}
      .q6-tabla .f{display:flex;justify-content:space-between;gap:10px}
      .q6-tabla .f span:first-child{color:var(--ink-soft)}
      .q6-tabla .f b{color:var(--ink);font-weight:500;text-align:right}
      .q6-tabla .f.top{border-top:1px solid var(--line-soft);margin-top:5px;padding-top:5px}
      .q6-tabla .f.no b{color:var(--goo-rojo)}
      .q6-tabla .f.si b{color:var(--goo-verde)}
      .q6-lee{font-family:var(--f-m);font-size:13px;line-height:1.75;color:var(--ink-soft);margin:12px 0 0}
      .q6-lee b{color:var(--ink)}
      .q6-lee .grande{font-size:16px;color:var(--goo-azul);font-weight:500}
      .q6-lee .malo{color:var(--goo-rojo)}
      .q6-rot{fill:var(--ink-soft);font-family:var(--f-m);font-size:11px}
      .q6-etq{fill:var(--ink);font-family:var(--f-m);font-size:11.5px;font-weight:500}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-q6');
        if(!svg) return;
        var segProy = document.getElementById('q6-proy');
        var segQuien = document.getElementById('q6-quien');
        var segAlim = document.getElementById('q6-alim');
        var segSonda = document.getElementById('q6-sonda');
        var filaSonda = document.getElementById('q6-filasonda');
        var filaDep = document.getElementById('q6-filadep');
        var tabla = document.getElementById('q6-tabla');
        var lee = document.getElementById('q6-lee');
        var pie = document.getElementById('q6-pie');
        var dep = document.getElementById('q6-dep');
        var rec = document.getElementById('q6-rec');

        /* ---- constantes DECLARADAS ---- */
        var DIAS = 1825;            /* cinco anos */
        var ABANDONO = 270;         /* el dia que deja de ir el ultimo de los autores */
        var MIN_RUTINA = 15;        /* minutos de ir, rellenar y volver */
        var MIN_AVERIA = 40;        /* minutos de desmontar, cambiar la pieza y probar */
        var HORA = 12;              /* EUR la hora de trabajo de una persona, orden de magnitud */
        var Wh_PILA = 3.7, PILAS = 4;
        var EUR_PILAS = 3.20, EUR_CLAVOS = 0.30, EUR_CAPA = 2.50,
            EUR_DHT = 2.00, EUR_LDR = 0.20;

        /* quien lo mantiene: cuanto tarda en enterarse y en ir, y hasta cuando esta */
        var QUIEN = [
          {n: 'vosotros', tarda: 2, hasta: ABANDONO,
           d: 'sois los que m\\u00e1s corr\\u00e9is, y dej\\u00e1is de ir a los ' + ABANDONO
            + ' d\\u00edas'},
          {n: 'el conserje', tarda: 7, hasta: DIAS,
           d: 'pasa por all\\u00ed una vez por semana, y sigue el curso que viene'},
          {n: 'el departamento', tarda: 30, hasta: DIAS,
           d: 'se acuerda cuando alguien se queja, pero no se va'}
        ];
        var SONDA = [
          {n: 'dos clavos galvanizados, con corriente siempre', vida: 20, eur: EUR_CLAVOS},
          {n: 'los mismos clavos, alimentados solo al medir', vida: 180, eur: EUR_CLAVOS},
          {n: 'sonda capacitiva', vida: 1100, eur: EUR_CAPA}
        ];

        var proy = 0, quien = 0, alim = 0, sonda = 0;

        function coma(x, d){
          if(!isFinite(x)) return '\\u221e';
          var p = Math.abs(x).toFixed(d).split('.');
          var e = p[0].replace(/\\B(?=(\\d{3})+(?!\\d))/g, '.');
          return (x < 0 ? '\\u2212' : '') + e + (d ? ',' + p[1] : '');
        }
        function f(a, b, cl){
          return '<div class="f ' + (cl || '') + '"><span>' + a + '</span><b>' + b + '</b></div>';
        }

        var PROY = [
          {n: 'A \\u00b7 riego autom\\u00e1tico', riega: true, litros: 0.51, wh: 1.45,
           sensor: null},
          {n: 'B \\u00b7 aviso de aula', riega: false, litros: 0, wh: 1.45,
           sensor: {n: 'el sensor de temperatura y humedad', vida: 1100, eur: EUR_DHT}},
          {n: 'C \\u00b7 l\\u00e1mpara', riega: false, litros: 0, wh: 1.45,
           sensor: {n: 'la resistencia de luz', vida: 5000, eur: EUR_LDR}}
        ];

        /* ---------------------------------------------------------------
           La simulacion: dia a dia, 1.825 dias. Se gasta lo que se gasta;
           cuando algo se agota el aparato se PARA, y no vuelve hasta que
           alguien va. Si ya no queda nadie, no vuelve nunca.
        --------------------------------------------------------------- */
        function simula(){
          var P = PROY[proy], Q = QUIEN[quien];
          var espera = +rec.value;
          var litrosDia = P.riega ? P.litros : 0;
          var whDia = alim === 1 ? 0 : P.wh;            /* con enchufe no se gastan pilas */
          var piezas = [];
          if(P.riega){
            piezas.push({n: 'rellenar el dep\\u00f3sito', vida: litrosDia > 0
                           ? (+dep.value) / litrosDia : Infinity, eur: 0, rutina: true});
            piezas.push({n: 'cambiar la sonda', vida: SONDA[sonda].vida,
                         eur: SONDA[sonda].eur, rutina: false});
          }
          if(P.sensor) piezas.push({n: 'cambiar ' + P.sensor.n, vida: P.sensor.vida,
                                    eur: P.sensor.eur, rutina: false});
          if(whDia > 0) piezas.push({n: 'cambiar las pilas',
                                     vida: Wh_PILA * PILAS / whDia, eur: EUR_PILAS, rutina: true});

          /* reloj de cada pieza: cuando le toca */
          var toca = piezas.map(function(p){ return p.vida; });
          var visitas = [], parones = [];
          var parado = false, vuelve = 0, diasParado = 0, minutos = 0, euros = 0;
          var muere = null;

          for(var d = 0; d <= DIAS; d++){
            if(parado){
              diasParado++;
              if(d >= vuelve){
                parado = false;
                parones[parones.length - 1].fin = d;
              }
              continue;
            }
            for(var i = 0; i < piezas.length; i++){
              if(d >= toca[i]){
                /* se ha agotado: el aparato se para aqui mismo */
                parado = true;
                var hayQuien = d <= Q.hasta;
                var demora = hayQuien ? Q.tarda + (piezas[i].rutina ? 0 : espera) : Infinity;
                vuelve = d + demora;
                parones.push({ini: d, fin: isFinite(vuelve) ? vuelve : DIAS, porque: piezas[i].n});
                if(hayQuien){
                  visitas.push({d: d, n: piezas[i].n});
                  minutos += piezas[i].rutina ? MIN_RUTINA : MIN_AVERIA;
                  euros += piezas[i].eur;
                  toca[i] = d + demora + piezas[i].vida;
                } else {
                  toca[i] = Infinity;
                  if(muere === null) muere = d;
                }
                break;
              }
            }
          }
          var horas = minutos / 60;
          return {P: P, Q: Q, visitas: visitas, parones: parones,
                  diasParado: diasParado, horas: horas, euros: euros,
                  coste: euros + horas * HORA,
                  disp: 100 * (DIAS - diasParado) / DIAS,
                  muere: muere};
        }

        function pinta(){
          var P = PROY[proy];
          filaSonda.hidden = !P.riega;
          filaDep.hidden = !P.riega;
          document.getElementById('v-q6-dep').innerHTML = dep.value + ' L';
          document.getElementById('v-q6-rec').innerHTML = (+rec.value === 0 ? 'el caj\\u00f3n'
            : (+rec.value === 1 ? '1 d\\u00eda' : rec.value + ' d\\u00edas'));

          var r = simula();

          /* ---------- la tira de cinco anos ---------- */
          var x0 = 20, ancho = 424, y = 60, hh = 30;
          function X(d){ return x0 + ancho * d / DIAS; }
          var s = [];
          s.push('<text x="' + x0 + '" y="15" class="q6-rot">cinco a\\u00f1os, d\\u00eda a d\\u00eda: '
               + 'verde funcionando, rojo parado</text>');
          s.push('<rect x="' + x0 + '" y="' + y + '" width="' + ancho + '" height="' + hh
               + '" fill="var(--goo-verde)" opacity="0.55"/>');
          r.parones.forEach(function(p){
            var w = Math.max(0.7, X(p.fin) - X(p.ini));
            s.push('<rect x="' + X(p.ini).toFixed(1) + '" y="' + y + '" width="' + w.toFixed(1)
                 + '" height="' + hh + '" fill="var(--goo-rojo)" opacity="0.85"/>');
          });
          s.push('<rect x="' + x0 + '" y="' + y + '" width="' + ancho + '" height="' + hh
               + '" fill="none" stroke="var(--ink)" stroke-width="1.2"/>');
          /* las visitas, una raya por cada vez que alguien tiene que ir */
          r.visitas.forEach(function(v){
            s.push('<line x1="' + X(v.d).toFixed(1) + '" y1="' + (y + hh + 2) + '" x2="'
                 + X(v.d).toFixed(1) + '" y2="' + (y + hh + 11)
                 + '" stroke="var(--goo-azul)" stroke-width="1" opacity="0.7"/>');
          });
          s.push('<text x="' + x0 + '" y="' + (y + hh + 26) + '" class="q6-rot">'
               + (r.visitas.length ? 'cada raya azul es una vez que alguien tiene que ir ('
                   + r.visitas.length + ')' : 'nadie tiene que ir ni una sola vez') + '</text>');
          /* la fecha en que los autores se van */
          s.push('<line x1="' + X(ABANDONO).toFixed(1) + '" y1="' + (y - 14) + '" x2="'
               + X(ABANDONO).toFixed(1) + '" y2="' + (y + hh + 4)
               + '" stroke="var(--goo-amarillo)" stroke-width="2" stroke-dasharray="4 3"/>');
          s.push('<text x="' + (X(ABANDONO) + 4).toFixed(1) + '" y="' + (y - 18)
               + '" class="q6-etq">aqu\\u00ed dej\\u00e1is de ir</text>');
          /* eje de anos */
          for(var a = 0; a <= 5; a++){
            var xa = X(a * 365);
            s.push('<line x1="' + xa.toFixed(1) + '" y1="' + (y + hh) + '" x2="' + xa.toFixed(1)
                 + '" y2="' + (y + hh + 16) + '" stroke="var(--line)" stroke-width="1"/>');
            /* el ultimo rotulo cae justo en el borde: si va centrado, se sale */
            s.push('<text x="' + xa.toFixed(1) + '" y="' + (y + hh + 44)
                 + '" class="q6-rot" text-anchor="' + (a === 5 ? 'end' : 'middle') + '">a\\u00f1o '
                 + a + '</text>');
          }
          /* el resultado, grande */
          s.push('<text x="' + x0 + '" y="' + (y + hh + 76) + '" class="q6-etq">'
               + 'funcion\\u00f3 el ' + coma(r.disp, 0) + ' % del tiempo \\u00b7 '
               + coma(r.horas, 1) + ' h de otra persona \\u00b7 ' + coma(r.coste, 0)
               + ' \\u20ac</text>');
          s.push('<text x="' + x0 + '" y="' + (y + hh + 94) + '" class="q6-rot">'
               + 'lo mantiene ' + r.Q.n + '</text>');
          s.push('<text x="' + x0 + '" y="' + (y + hh + 110) + '" class="q6-rot">'
               + r.Q.d + '</text>');
          svg.setAttribute('viewBox', '0 0 460 ' + (y + hh + 120));
          svg.innerHTML = s.join('');

          /* ---------- la cuenta escrita ---------- */
          var t = f('veces que hay que ir', r.visitas.length + '')
            + f('horas de otra persona', coma(r.horas, 1) + ' h')
            + f('en piezas y pilas', coma(r.euros, 2) + ' \\u20ac')
            + f('esas horas, a ' + HORA + ' \\u20ac/h', coma(r.horas * HORA, 2) + ' \\u20ac')
            + f('mantenerlo cinco a\\u00f1os', coma(r.coste, 2) + ' \\u20ac', 'top')
            + f('d\\u00edas parado', coma(r.diasParado, 0) + ' de ' + coma(DIAS, 0))
            + f('disponibilidad', coma(r.disp, 1) + ' %', r.disp >= 90 ? 'si' : 'no');
          if(r.muere !== null){
            t += f('se queda parado para siempre', 'el d\\u00eda ' + coma(r.muere, 0), 'top no');
          } else {
            t += f('llega vivo a los cinco a\\u00f1os', 's\\u00ed', 'top si');
          }
          tabla.innerHTML = t;

          /* ---------- el veredicto ---------- */
          var v;
          if(!r.visitas.length && !r.diasParado){
            v = '<span class="grande">Cinco a\\u00f1os y nadie ha tenido que ir ni una vez.</span> '
              + 'Aqu\\u00ed no hay nada que se gaste: ni agua que reponer, ni pilas, y el sensor dura '
              + 'm\\u00e1s que el proyecto. Ojo con la conclusi\\u00f3n f\\u00e1cil: en la sesi\\u00f3n 4 '
              + 'vimos que este mismo aparato era el que <b>menos ahorraba</b>. <b>Lo que menos '
              + 'mantenimiento pide suele ser lo que menos hace.</b>';
          } else if(r.muere !== null){
            v = '<span class="grande malo">El d\\u00eda ' + coma(r.muere, 0) + ' se para y ya no '
              + 'vuelve a arrancar.</span> No se ha roto nada caro: se ha agotado algo que '
              + 'alguien ten\\u00eda que reponer, y para entonces <b>ya no quedaba ese alguien</b>. '
              + 'Funcion\\u00f3 el ' + coma(r.disp, 0) + ' % de los cinco a\\u00f1os. Prueba a cambiar '
              + 'qui\\u00e9n lo mantiene, y despu\\u00e9s prueba a quitar lo que se agota.';
          } else {
            v = '<span class="grande">Hay que ir <b>' + r.visitas.length + '</b> veces en cinco '
              + 'a\\u00f1os: ' + coma(r.horas, 1) + ' horas de ' + r.Q.n + '.</span> En piezas son '
              + coma(r.euros, 2) + ' \\u20ac, pero esas horas valen ' + coma(r.horas * HORA, 2)
              + ' \\u20ac si se pagaran, y <b>alguien las pone aunque no se paguen</b>. El aparato '
              + 'cost\\u00f3 25 \\u20ac de material: mantenerlo cuesta <b>'
              + coma(r.coste / 25, 1) + ' veces</b> eso. Y estuvo parado ' + coma(r.diasParado, 0)
              + ' d\\u00edas esperando a que alguien fuera.';
          }
          lee.innerHTML = v;

          pie.innerHTML =
            'La escena recorre los <b>' + coma(DIAS, 0) + ' d\\u00edas</b> uno a uno. Cada cosa que se gasta '
          + 'tiene su reloj: el dep\\u00f3sito dura <b>litros \\u00f7 litros al d\\u00eda</b>, las pilas '
          + '<b>' + coma(Wh_PILA * PILAS, 1) + ' Wh \\u00f7 lo que gasta al d\\u00eda</b> '
          + '(' + coma(PROY[proy].wh, 2) + ' Wh con la placa durmiendo, de la sesi\\u00f3n 5), y la '
          + 'sonda lo que dure su tipo. La raya amarilla est\\u00e1 en el <b>d\\u00eda ' + ABANDONO
          + '</b>: es marzo del curso siguiente, cuando suponemos que ya no se pasa por all\\u00ed '
          + 'ninguno de vosotros \\u2014unos se han ido del centro y los que siguen tienen otras '
          + 'cosas\\u2014. <b>Es una suposici\\u00f3n nuestra, y es la m\\u00e1s importante de la '
          + 'escena.</b> Cuando algo se agota el aparato <b>se para</b> y no vuelve '
          + 'hasta que alguien va: eso tarda lo que tarde esa persona m\\u00e1s lo que tarde el '
          + 'recambio. Las <b>vidas de las sondas</b> ('
          + SONDA.map(function(x){ return coma(x.vida, 0) + ' d\\u00edas ' + x.n.split(',')[0]; })
                 .join(', ')
          + ') son orden de magnitud nuestro: los clavos con corriente permanente se comen por '
          + '<b>electr\\u00f3lisis</b> en semanas, y eso s\\u00ed es un hecho comprobable en el taller. '
          + 'La hora de trabajo a ' + HORA + ' \\u20ac es orden de magnitud, y <b>no se factura a '
          + 'nadie</b>: est\\u00e1 puesta para que se vea que el tiempo de una persona no es gratis '
          + 'por el hecho de no cobrarse. <b>Lo que aqu\\u00ed no se cuenta</b>: que la bomba se '
          + 'estropea si arranca con el dep\\u00f3sito seco. Suponemos que vuestro aparato se da '
          + 'cuenta y no la arranca, porque eso era justo uno de los requisitos de la sesi\\u00f3n 5. '
          + 'Si no lo hiciera, habr\\u00eda que sumar una bomba quemada cada vez que se queda seco.';
        }

        function conecta(cont, attr, set){
          cont.addEventListener('click', function(e){
            var b = e.target.closest('button[' + attr + ']');
            if(!b) return;
            set(+b.getAttribute(attr));
            this.querySelectorAll('button').forEach(function(x){
              x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
            });
            pinta();
          });
        }
        conecta(segProy, 'data-p', function(v){ proy = v; });
        conecta(segQuien, 'data-q', function(v){ quien = v; });
        conecta(segAlim, 'data-a', function(v){ alim = v; });
        conecta(segSonda, 'data-s', function(v){ sonda = v; });
        dep.addEventListener('input', pinta);
        rec.addEventListener('input', pinta);
        pinta();
      })();
      </script>
'''
