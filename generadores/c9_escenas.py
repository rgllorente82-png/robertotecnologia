# -*- coding: utf-8 -*-
"""4.o Tecnologia - Tema 9 - Escenas de las sesiones 1 y 2.

Las dos calculan de verdad. Ningun numero de la pantalla esta escrito a mano:
todos salen de la cuenta que la propia escena declara.

  MERCADO (S1)  Por que se fabrica una cosa y no otra. Para cada problema
      calcula el PRECIO MINIMO que habria que cobrar para recuperar lo que
      cuesta desarrollarlo, lo compara con lo que puede pagar quien lo sufre,
      y de ahi saca el beneficio esperado. Las barras van en escala
      logaritmica con signo, porque los casos se llevan cinco ordenes de
      magnitud y en lineal no se veria nada. Se puede reordenar por beneficio
      o por personas atendidas: el orden NO coincide, y esa es la sesion.

  SITIO (S2)  Dos modos en una escena.
      A - "El columpio que saca agua": las horas de bombeo que hacen falta al
          dia para el objetivo que anunciaba la PlayPump. Sale de dividir el
          agua que hace falta entre el caudal, y da mas horas de las que tiene
          un dia.
      B - "Tu proyecto en tres sitios": el balance de energia de los tres
          proyectos del curso en el instituto, en una aldea sin red y en un
          huerto al que se sube una vez al mes. Lo que se lleva la energia no
          es el actuador: es la placa esperando.

Los numeros de partida estan DECLARADOS dentro de cada escena, con su origen:
los que vienen de una fuente lo dicen, y los que son orden de magnitud nuestro
tambien lo dicen.

Nota de implementacion: los mandos se montan UNA vez y despues solo se
recalcula. Si se reconstruye el HTML de los mandos en cada evento 'input', el
deslizador que estas arrastrando desaparece a mitad del arrastre.

Clases CSS con prefijo propio (q1-, q2-). Nada que empiece por test-, y ningun
id que empiece por ses- (el JS de la barra de sesiones esconde todo lo que
empiece asi).

Estas cadenas NO pasan por ningun formateo con %.
"""

# ==========================================================================
# S1 - La cuenta que decide que se fabrica
# ==========================================================================
MERCADO = u'''
      <div class="escena" id="esc-q1">
        <div class="escena-barra">
          <span class="escena-titulo">La cuenta que decide qu&eacute; se fabrica</span>
          <div class="seg" id="ord-q1">
            <button type="button" data-o="ben" aria-pressed="true">Ordenar por beneficio</button>
            <button type="button" data-o="per">Ordenar por personas atendidas</button>
          </div>
        </div>
        <div class="lienzo">
          <div class="q1">
            <div class="q1-izq">
              <svg viewBox="0 0 470 292" id="svg-q1" role="img"
                   aria-label="Beneficio esperado de cada problema, en millones de euros, en escala logar&iacute;tmica"></svg>
            </div>
            <div class="q1-der">
              <div class="q1-fila">
                <label for="q1-alc">Le llega al</label>
                <input type="range" id="q1-alc" min="5" max="100" step="5" value="60">
                <span class="val" id="q1-valc"></span>
              </div>
              <div class="q1-fila">
                <label for="q1-anios">Lo vende en exclusiva</label>
                <input type="range" id="q1-anios" min="1" max="20" step="1" value="10">
                <span class="val" id="q1-vanios"></span>
              </div>
              <div class="q1-fila">
                <label for="q1-pub">Dinero p&uacute;blico</label>
                <input type="range" id="q1-pub" min="0" max="100" step="1" value="0">
                <span class="val" id="q1-vpub"></span>
              </div>
              <div class="q1-tabla" id="q1-tabla"></div>
            </div>
          </div>
          <p class="q1-lee" id="q1-lee"></p>
        </div>
        <div class="pie" id="q1-pie"></div>
      </div>

      <style>
      .q1{display:flex;gap:18px;flex-wrap:wrap;align-items:flex-start}
      .q1-izq{flex:1 1 400px;min-width:310px}
      .q1-der{flex:1 1 280px;min-width:262px}
      .q1-fila{display:flex;align-items:center;gap:9px;flex-wrap:wrap;margin:0 0 9px;
        font-family:var(--f-m);font-size:12.5px;color:var(--ink)}
      .q1-fila label{min-width:122px}
      .q1-fila input[type="range"]{flex:1 1 100px;min-width:88px;max-width:150px;
        accent-color:var(--goo-azul)}
      .q1-fila .val{font-weight:500;color:var(--goo-azul);min-width:62px;text-align:right}
      .q1-tabla{border:1.5px solid var(--line);border-radius:2px;background:var(--surface);
        padding:9px 11px;font-family:var(--f-m);font-size:12.5px;line-height:1.7;margin-top:4px}
      .q1-tabla .cab{color:var(--goo-azul);font-weight:500;margin-bottom:5px}
      .q1-tabla .f{display:flex;justify-content:space-between;gap:10px}
      .q1-tabla .f span:first-child{color:var(--ink-soft)}
      .q1-tabla .f b{color:var(--ink);font-weight:500;text-align:right}
      .q1-tabla .f.top{border-top:1px solid var(--line-soft);margin-top:5px;padding-top:5px}
      .q1-tabla .f.no b{color:var(--goo-rojo)}
      .q1-tabla .f.si b{color:var(--goo-verde)}
      .q1-lee{font-family:var(--f-m);font-size:13px;line-height:1.75;color:var(--ink-soft);margin:12px 0 0}
      .q1-lee b{color:var(--ink)}
      .q1-lee .grande{font-size:16px;color:var(--goo-azul);font-weight:500}
      .q1-nom{fill:var(--ink);font-family:var(--f-m);font-size:10.5px}
      .q1-nom.sel{font-weight:500;fill:var(--goo-azul)}
      .q1-cif{font-family:var(--f-m);font-size:10.5px;fill:var(--ink-soft)}
      .q1-val{font-family:var(--f-m);font-size:11px;fill:var(--ink);font-weight:500}
      .q1-eje{stroke:var(--line);stroke-width:1}
      .q1-cero{stroke:var(--ink);stroke-width:1.6}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-q1');
        if(!svg) return;
        var ord = document.getElementById('ord-q1');
        var alc = document.getElementById('q1-alc');
        var anios = document.getElementById('q1-anios');
        var pub = document.getElementById('q1-pub');
        var valc = document.getElementById('q1-valc');
        var vanios = document.getElementById('q1-vanios');
        var vpub = document.getElementById('q1-vpub');
        var tabla = document.getElementById('q1-tabla');
        var lee = document.getElementById('q1-lee');
        var pie = document.getElementById('q1-pie');

        /* ---------------------------------------------------------------
           Los seis casos, cada uno con DE DONDE sale su numero.
             per  personas que lo sufren o lo usarian
             paga lo que puede y quiere pagar al ano cada una, en euros
             des  lo que cuesta desarrollarlo y ponerlo en la calle, en M EUR
           Donde pone "orden de magnitud" es estimacion nuestra: la escena no
           demuestra nada sobre un caso concreto, ensena como es la cuenta.
        --------------------------------------------------------------- */
        /* Los nombres van cortos a proposito: el rotulo del dibujo tiene 140 px
           y a 10,5 px de ancho de letra no caben mas de veinte caracteres. */
        var CASOS = [
          {n: 'Paludismo', per: 282e6, paga: 0.50, des: 300,
           f: '282 millones de casos en 2024, seg\\u00fan la hoja informativa de la OMS. Lo que puede '
            + 'pagar al a\\u00f1o una familia en zona end\\u00e9mica es orden de magnitud nuestro.'},
          {n: 'Chagas', per: 8e6, paga: 0.50, des: 300,
           f: 'unos 8 millones de infectados, seg\\u00fan la OMS, casi todos en Am\\u00e9rica Latina. '
            + 'Lo que puede pagar es orden de magnitud nuestro.'},
          {n: 'Colesterol alto', per: 40e6, paga: 250, des: 1000,
           f: 'orden de magnitud nuestro, puesto para tener con qu\\u00e9 comparar: mucha menos gente, '
            + 'y con seguro o con sueldo.'},
          {n: 'Calvicie', per: 30e6, paga: 300, des: 400,
           f: 'orden de magnitud nuestro. De esto no se muere nadie, y es de lo que m\\u00e1s se '
            + 'investiga.'},
          {n: 'Aire del aula (B)', per: 10e6, paga: 0.20, des: 5,
           f: 'orden de magnitud nuestro. Es vuestro proyecto B. Mirad bien lo que paga: el alumno '
            + 'que lo sufre no compra nada, y quien compra no lo sufre.'},
          {n: 'Riego escolar (A)', per: 0.2e6, paga: 2, des: 1,
           f: 'orden de magnitud nuestro. Es vuestro proyecto A, contado como si alguien quisiera '
            + 'fabricarlo y vivir de venderlo.'}
        ];

        var sel = 4, orden = 'ben';

        function miles(t){ return t.replace(/\\B(?=(\\d{3})+(?!\\d))/g, '.'); }
        function coma(x, d){
          var p = x.toFixed(d).split('.');
          return miles(p[0]) + (d ? ',' + p[1] : '');
        }
        /* Millones de euros. Sin "mil M" ni notaciones raras: los miles se
           separan con punto y ya, que asi cabe en el hueco del dibujo. */
        function meur(m){
          return (Math.abs(m) >= 10 ? coma(m, 0) : coma(m, 1)) + ' M\\u20ac';
        }
        function pers(p){
          if(p >= 1e6) return coma(p / 1e6, 1) + ' millones';
          if(p >= 1e3) return coma(p / 1e3, 0) + ' mil';
          return coma(p, 0);
        }
        function f(a, b, cl){
          return '<div class="f ' + (cl || '') + '"><span>' + a + '</span><b>' + b + '</b></div>';
        }
        function log1(v){ return Math.log(1 + Math.abs(v)) / Math.LN10; }

        /* ---- la cuenta, entera y en un solo sitio ---- */
        function calcula(){
          var a = +alc.value / 100, y = +anios.value, p = +pub.value;
          return CASOS.map(function(c, i){
            var atend = c.per * a;                   /* personas a las que les llega */
            var minimo = c.des * 1e6 / (atend * y);  /* EUR por persona y ano para no perder */
            var margen = c.paga + p - minimo;        /* lo que sobra por persona y ano */
            var ben = margen * atend * y / 1e6;      /* beneficio esperado, en M EUR */
            return {i: i, c: c, atend: atend, minimo: minimo, margen: margen, ben: ben,
                    sale: margen > 0};
          });
        }

        function pinta(){
          var d = calcula();
          valc.innerHTML = alc.value + ' %';
          vanios.innerHTML = anios.value + (+anios.value === 1 ? ' a\\u00f1o' : ' a\\u00f1os');
          vpub.innerHTML = coma(+pub.value, 0) + ' \\u20ac';

          var fila = d.slice().sort(function(x, z){
            return orden === 'ben' ? z.ben - x.ben : z.atend - x.atend;
          });

          /* --- escala logaritmica con signo: cada raya multiplica por diez --- */
          var L = 0, R = 0;
          d.forEach(function(x){
            var l = log1(x.ben);
            if(x.ben < 0){ if(l > L) L = l; } else if(l > R) R = l;
          });
          L = Math.min(8, Math.max(1, Math.ceil(L)));
          R = Math.min(8, Math.max(1, Math.ceil(R)));
          var x0 = 156, ancho = 232;
          var pxd = ancho / (L + R);
          var cero = x0 + ancho * L / (L + R);
          function X(m){
            var l = Math.min(log1(m), m < 0 ? L : R) * pxd;
            return cero + (m < 0 ? -l : l);
          }

          var alto = 30, y0 = 42, abajo, s = [];
          abajo = y0 + fila.length * alto;
          var salto = Math.max(1, Math.ceil(46 / pxd));   /* no amontonar los rotulos */

          for(var k = -L; k <= R; k++){
            var vx = cero + (k < 0 ? -1 : 1) * Math.abs(k) * pxd;
            s.push('<line x1="' + vx.toFixed(1) + '" y1="' + (y0 - 12) + '" x2="' + vx.toFixed(1)
                 + '" y2="' + (abajo + 4) + '" class="' + (k === 0 ? 'q1-cero' : 'q1-eje') + '"/>');
            if(k !== 0 && Math.abs(k) % salto === 0){
              var e = Math.abs(k);
              /* a partir de 10.000 el numero no cabe entre raya y raya:
                 se escribe con exponente en superindice */
              var sup = ['\\u2070', '\\u00b9', '\\u00b2', '\\u00b3', '\\u2074',
                         '\\u2075', '\\u2076', '\\u2077', '\\u2078'];
              var etq = (k < 0 ? '\\u2212' : '')
                      + (e >= 4 ? '10' + sup[e] : coma(Math.pow(10, e), 0));
              s.push('<text x="' + vx.toFixed(1) + '" y="' + (abajo + 18)
                   + '" class="q1-cif" text-anchor="middle">' + etq + '</text>');
            }
          }
          s.push('<text x="' + cero.toFixed(1) + '" y="' + (abajo + 18)
               + '" class="q1-cif" text-anchor="middle">0</text>');
          s.push('<text x="' + x0 + '" y="' + (y0 - 22)
               + '" class="q1-cif">beneficio esperado, en millones de euros</text>');
          s.push('<text x="' + x0 + '" y="' + (abajo + 33)
               + '" class="q1-cif">cada raya multiplica por diez</text>');

          fila.forEach(function(x, j){
            var yy = y0 + j * alto;
            var xa = X(x.ben);
            var col = x.ben >= 0 ? 'var(--goo-azul)' : 'var(--goo-rojo)';
            s.push('<text x="150" y="' + (yy + 15) + '" text-anchor="end" class="q1-nom'
                 + (x.i === sel ? ' sel' : '') + '">' + x.c.n + '</text>');
            s.push('<rect x="' + Math.min(cero, xa).toFixed(1) + '" y="' + (yy + 5)
                 + '" width="' + Math.max(1.5, Math.abs(xa - cero)).toFixed(1)
                 + '" height="15" fill="' + col + '"'
                 + (x.i === sel ? ' stroke="var(--ink)" stroke-width="1.5"' : '') + '/>');
            s.push('<text x="' + (x.ben >= 0 ? 396 : 396) + '" y="' + (yy + 17)
                 + '" class="q1-val" text-anchor="start">' + meur(x.ben) + '</text>');
            s.push('<rect x="0" y="' + yy + '" width="470" height="' + alto
                 + '" fill="transparent" style="cursor:pointer" data-i="' + x.i + '"></rect>');
          });
          svg.innerHTML = s.join('');

          /* --- la cuenta escrita, del caso elegido --- */
          var c = d[sel];
          tabla.innerHTML =
            '<div class="cab">' + c.c.n + '</div>'
          + f('lo sufren', pers(c.c.per))
          + f('le llega al ' + alc.value + ' %', pers(c.atend))
          + f('desarrollarlo cuesta', meur(c.c.des))
          + f('precio m\\u00ednimo al a\\u00f1o', coma(c.minimo, 2) + ' \\u20ac', 'top')
          + f('puede pagar al a\\u00f1o', coma(c.c.paga, 2) + ' \\u20ac')
          + (+pub.value ? f('dinero p\\u00fablico', '+ ' + coma(+pub.value, 2) + ' \\u20ac') : '')
          + f(c.sale ? 'sobra al a\\u00f1o' : 'falta al a\\u00f1o',
              coma(Math.abs(c.margen), 2) + ' \\u20ac', c.sale ? 'si' : 'no')
          + f('beneficio esperado', meur(c.ben), 'top ' + (c.sale ? 'si' : 'no'));

          /* --- los dos ordenes, uno al lado del otro --- */
          var porBen = d.slice().sort(function(x, z){ return z.ben - x.ben; });
          var porPer = d.slice().sort(function(x, z){ return z.atend - x.atend; });
          var coinciden = porBen.every(function(x, k){ return x.i === porPer[k].i; });
          var cuantos = d.filter(function(x){ return !x.sale; }).length;
          lee.innerHTML =
            'Con estos mandos, <b>' + cuantos + ' de ' + d.length + '</b>'
          + (cuantos === 1 ? ' da p\\u00e9rdidas: ese no lo fabrica nadie.'
                           : ' dan p\\u00e9rdidas: esos no los fabrica nadie.')
          + '<br>El m\\u00e1s rentable es <b>' + porBen[0].c.n + '</b> ('
          + meur(porBen[0].ben) + '). Al que le llega a m\\u00e1s gente es <b>' + porPer[0].c.n
          + '</b> (' + pers(porPer[0].atend) + ' de personas).<br>'
          + '<span class="grande">' + (coinciden
              ? 'Ahora mismo los dos \\u00f3rdenes coinciden: mueve los mandos hasta que dejen de '
              + 'coincidir, y mira qu\\u00e9 mando lo rompe.'
              : 'Los dos \\u00f3rdenes no coinciden, y nadie ha hecho trampa: lo que puede pagar cada '
              + 'persona multiplica en una cuenta y no en la otra.') + '</span>';

          pie.innerHTML =
            'La cuenta de la escena es esta: <b>precio m\\u00ednimo = coste de desarrollo \\u00f7 '
          + '(personas atendidas \\u00d7 a\\u00f1os de exclusiva)</b>. Si ese precio m\\u00ednimo pasa de lo '
          + 'que puede pagar quien lo sufre, el problema no se resuelve, aunque lo sufra medio mundo. '
          + '<b>' + c.c.n + ':</b> ' + c.c.f + ' Los dos datos de la OMS salen de sus hojas '
          + 'informativas; el resto son <b>\\u00f3rdenes de magnitud nuestros</b>, puestos para que la '
          + 'cuenta tenga con qu\\u00e9 trabajar. Esta escena no demuestra nada sobre un caso concreto: '
          + 'ense\\u00f1a c\\u00f3mo es la cuenta.';
        }

        svg.addEventListener('click', function(e){
          var t = e.target.closest('[data-i]');
          if(!t) return;
          sel = +t.dataset.i;
          pinta();
        });
        ord.addEventListener('click', function(e){
          var b = e.target.closest('button[data-o]');
          if(!b) return;
          orden = b.dataset.o;
          ord.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          pinta();
        });
        [alc, anios, pub].forEach(function(r){ r.addEventListener('input', pinta); });
        pinta();
      })();
      </script>
'''


# ==========================================================================
# S2 - El sitio manda: dos modos en una escena
# ==========================================================================
SITIO = u'''
      <div class="escena" id="esc-q2">
        <div class="escena-barra">
          <span class="escena-titulo">&iquest;Aguanta aqu&iacute;? &middot; la cuenta del sitio</span>
          <div class="seg" id="modo-q2">
            <button type="button" data-m="a" aria-pressed="true">El columpio que saca agua</button>
            <button type="button" data-m="b">Tu proyecto en tres sitios</button>
          </div>
        </div>
        <div class="lienzo">
          <div class="q2">
            <div class="q2-izq">
              <svg viewBox="0 0 440 256" id="svg-q2" role="img"
                   aria-label="Horas de bombeo que hacen falta al d&iacute;a, o balance de energ&iacute;a del aparato"></svg>
            </div>
            <div class="q2-der">
              <div id="q2-ma" class="q2-mandos">
                <div class="q2-fila">
                  <label for="q2-gente">Personas por bomba</label>
                  <input type="range" id="q2-gente" min="100" max="5000" step="100" value="2500">
                  <span class="val" id="v-q2-gente"></span>
                </div>
                <div class="q2-fila">
                  <label for="q2-litros">Litros por persona y d&iacute;a</label>
                  <input type="range" id="q2-litros" min="5" max="50" step="1" value="10">
                  <span class="val" id="v-q2-litros"></span>
                </div>
                <div class="q2-fila">
                  <label for="q2-caudal">Caudal real de la bomba</label>
                  <input type="range" id="q2-caudal" min="200" max="1600" step="20" value="1400">
                  <span class="val" id="v-q2-caudal"></span>
                </div>
                <div class="q2-fila">
                  <label for="q2-juego">Horas que juega un ni&ntilde;o</label>
                  <input type="range" id="q2-juego" min="0.5" max="8" step="0.5" value="2">
                  <span class="val" id="v-q2-juego"></span>
                </div>
              </div>
              <div id="q2-mb" class="q2-mandos" hidden>
                <div class="q2-fila">
                  <label>Proyecto</label>
                  <div class="seg" id="q2-proy">
                    <button type="button" data-p="0" aria-pressed="true">A &middot; riego</button>
                    <button type="button" data-p="1">B &middot; aula</button>
                    <button type="button" data-p="2">C &middot; l&aacute;mpara</button>
                  </div>
                </div>
                <div class="q2-fila">
                  <label>Sitio</label>
                  <div class="seg" id="q2-sitio">
                    <button type="button" data-s="0" aria-pressed="true">Instituto</button>
                    <button type="button" data-s="1">Aldea</button>
                    <button type="button" data-s="2">Huerto</button>
                  </div>
                </div>
                <div class="q2-fila">
                  <label for="q2-uso" id="q2-rotuso">Uso del actuador</label>
                  <input type="range" id="q2-uso" min="0" max="300" step="5" value="40">
                  <span class="val" id="v-q2-uso"></span>
                </div>
                <label class="q2-chk"><input type="checkbox" id="q2-duerme">
                  la placa duerme entre medidas</label>
                <label class="q2-chk"><input type="checkbox" id="q2-wifi">
                  le a&ntilde;ado un m&oacute;dulo de wifi</label>
              </div>
              <div class="q2-tabla" id="q2-tabla"></div>
            </div>
          </div>
          <p class="q2-lee" id="q2-lee"></p>
        </div>
        <div class="pie" id="q2-pie"></div>
      </div>

      <style>
      .q2{display:flex;gap:18px;flex-wrap:wrap;align-items:flex-start}
      .q2-izq{flex:1 1 380px;min-width:300px}
      .q2-der{flex:1 1 296px;min-width:272px}
      .q2-fila{display:flex;align-items:center;gap:9px;flex-wrap:wrap;margin:0 0 9px;
        font-family:var(--f-m);font-size:12.5px;color:var(--ink)}
      .q2-fila label{min-width:138px}
      .q2-fila input[type="range"]{flex:1 1 96px;min-width:86px;max-width:150px;
        accent-color:var(--goo-azul)}
      .q2-fila .val{font-weight:500;color:var(--goo-azul);min-width:70px;text-align:right}
      .q2-fila .seg button{padding:5px 9px;font-size:11.5px}
      .q2-chk{display:flex;align-items:center;gap:8px;font-family:var(--f-m);font-size:12.5px;
        margin:0 0 9px;color:var(--ink);cursor:pointer}
      .q2-chk input{accent-color:var(--goo-azul)}
      .q2-tabla{border:1.5px solid var(--line);border-radius:2px;background:var(--surface);
        padding:9px 11px;font-family:var(--f-m);font-size:12.5px;line-height:1.7;margin-top:4px}
      .q2-tabla .f{display:flex;justify-content:space-between;gap:10px}
      .q2-tabla .f span:first-child{color:var(--ink-soft)}
      .q2-tabla .f b{color:var(--ink);font-weight:500;text-align:right}
      .q2-tabla .f.top{border-top:1px solid var(--line-soft);margin-top:5px;padding-top:5px}
      .q2-tabla .f.no b{color:var(--goo-rojo)}
      .q2-tabla .f.si b{color:var(--goo-verde)}
      .q2-lee{font-family:var(--f-m);font-size:13px;line-height:1.75;color:var(--ink-soft);margin:12px 0 0}
      .q2-lee b{color:var(--ink)}
      .q2-lee .grande{font-size:16px;color:var(--goo-azul);font-weight:500}
      .q2-lee .malo{color:var(--goo-rojo)}
      .q2-rot{fill:var(--ink-soft);font-family:var(--f-m);font-size:11px}
      .q2-etq{fill:var(--ink);font-family:var(--f-m);font-size:11.5px;font-weight:500}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-q2');
        if(!svg) return;
        var modo = document.getElementById('modo-q2');
        var panelA = document.getElementById('q2-ma');
        var panelB = document.getElementById('q2-mb');
        var tabla = document.getElementById('q2-tabla');
        var lee = document.getElementById('q2-lee');
        var pie = document.getElementById('q2-pie');
        var rotUso = document.getElementById('q2-rotuso');
        var ctl = {};
        ['gente', 'litros', 'caudal', 'juego', 'uso', 'duerme', 'wifi'].forEach(function(k){
          ctl[k] = document.getElementById('q2-' + k);
        });
        function V(k){ return +ctl[k].value; }

        var M = 'a', proy = 0, sitio = 0;

        function miles(t){ return t.replace(/\\B(?=(\\d{3})+(?!\\d))/g, '.'); }
        function coma(x, d){
          if(!isFinite(x)) return '\\u221e';
          var p = x.toFixed(d).split('.');
          return miles(p[0]) + (d ? ',' + p[1] : '');
        }
        function f(a, b, cl){
          return '<div class="f ' + (cl || '') + '"><span>' + a + '</span><b>' + b + '</b></div>';
        }

        /* ==============================================================
           MODO A - el columpio que saca agua
           ============================================================== */
        function modoA(){
          var gente = V('gente'), litros = V('litros'), caudal = V('caudal'), juego = V('juego');
          var agua = gente * litros;                 /* litros al dia */
          var horas = agua / caudal;                 /* horas de bombeo al dia */
          var ninos = horas / juego;                 /* cuantos girando a la vez */
          var cabe = horas <= 24;

          document.getElementById('v-q2-gente').innerHTML = coma(gente, 0);
          document.getElementById('v-q2-litros').innerHTML = coma(litros, 0) + ' L';
          document.getElementById('v-q2-caudal').innerHTML = coma(caudal, 0) + ' L/h';
          document.getElementById('v-q2-juego').innerHTML = coma(juego, 1) + ' h';

          var x0 = 42, ancho = 360, esc = ancho / 30;   /* el dibujo llega a 30 h */
          var s = [];
          s.push('<text x="' + x0 + '" y="30" class="q2-rot">un d\\u00eda tiene 24 horas</text>');
          s.push('<rect x="' + x0 + '" y="40" width="' + (24 * esc).toFixed(1)
               + '" height="24" fill="none" stroke="var(--line)" stroke-width="1.5"/>');
          for(var h = 0; h <= 24; h += 6){
            var hx = x0 + h * esc;
            s.push('<line x1="' + hx.toFixed(1) + '" y1="40" x2="' + hx.toFixed(1)
                 + '" y2="70" stroke="var(--line)" stroke-width="1"/>');
            s.push('<text x="' + hx.toFixed(1) + '" y="84" class="q2-rot" text-anchor="middle">'
                 + h + '</text>');
          }
          s.push('<text x="' + x0 + '" y="110" class="q2-rot">horas que hay que bombear cada d\\u00eda</text>');
          var anc = Math.min(horas, 30) * esc;
          s.push('<rect x="' + x0 + '" y="118" width="' + anc.toFixed(1)
               + '" height="28" fill="' + (cabe ? 'var(--goo-verde)' : 'var(--goo-rojo)') + '"/>');
          if(horas > 30){
            s.push('<path d="M' + (x0 + ancho + 2) + ' 118 l 9 7 l -9 7 l 9 7 l -9 7" fill="none" '
                 + 'stroke="var(--goo-rojo)" stroke-width="2.5"/>');
          }
          s.push('<line x1="' + (x0 + 24 * esc).toFixed(1) + '" y1="112" x2="'
               + (x0 + 24 * esc).toFixed(1) + '" y2="154" stroke="var(--ink)" stroke-width="1.6" '
               + 'stroke-dasharray="4 3"/>');
          s.push('<text x="' + (x0 + Math.min(anc, ancho - 60) + 7).toFixed(1)
               + '" y="137" class="q2-etq">' + coma(horas, 1) + ' h</text>');
          s.push('<text x="' + x0 + '" y="180" class="q2-rot">ni\\u00f1os girando a la vez, si cada uno '
               + 'juega ' + coma(juego, 1) + ' h</text>');
          var np = Math.min(Math.round(ninos), 40);
          for(var i = 0; i < np; i++){
            s.push('<circle cx="' + (x0 + 7 + (i % 20) * 13) + '" cy="'
                 + (196 + Math.floor(i / 20) * 15) + '" r="5" fill="var(--goo-azul)"/>');
          }
          if(ninos > 40) s.push('<text x="' + (x0 + 268) + '" y="216" class="q2-rot">y m\\u00e1s</text>');
          s.push('<text x="' + (x0 + 320) + '" y="205" class="q2-etq" text-anchor="end">'
               + coma(ninos, 1) + '</text>');
          svg.innerHTML = s.join('');

          tabla.innerHTML =
            f('agua que hace falta al d\\u00eda', coma(agua, 0) + ' L')
          + f('la bomba sube', coma(caudal, 0) + ' L cada hora')
          + f('horas de bombeo al d\\u00eda', coma(horas, 1) + ' h', 'top ' + (cabe ? 'si' : 'no'))
          + f('y un d\\u00eda tiene', '24 h')
          + f('ni\\u00f1os girando a la vez', coma(ninos, 1), ninos <= 3 ? 'si' : 'no');

          lee.innerHTML = cabe
            ? '<span class="grande">Con estos n\\u00fameros cabe en un d\\u00eda: ' + coma(horas, 1)
              + ' horas de las 24.</span> Ahora baja el caudal a lo que daba la bomba de verdad, o '
              + 'sube las personas, y mira cu\\u00e1ndo deja de caber.'
            : '<span class="grande malo">No cabe: hacen falta ' + coma(horas, 1)
              + ' horas de bombeo y un d\\u00eda tiene 24.</span> Y eso contando con que el columpio '
              + 'gire sin parar, sin domingos y sin vacaciones. Para conseguirlo tendr\\u00edan que estar '
              + 'dando vueltas ' + coma(ninos, 1) + ' ni\\u00f1os a la vez, todo el rato. '
              + '<b>Esta divisi\\u00f3n no la hizo nadie antes de instalar mil de estas bombas.</b>';

          pie.innerHTML =
            'La cuenta es una divisi\\u00f3n: <b>horas = (personas \\u00d7 litros) \\u00f7 caudal</b>. Los '
          + 'valores de partida son los que anunciaba la propia PlayPump: <b>2.500 personas por '
          + 'bomba</b> y <b>hasta 1.400 litros por hora</b> desde 40 metros de profundidad. Los 10 '
          + 'litros por persona y d\\u00eda son un m\\u00ednimo de supervivencia, no un consumo normal: en '
          + 'Espa\\u00f1a se pasa de los cien. Cuando alguien fue a medir el caudal de verdad, la cuenta '
          + 'daba <b>27 horas de juego al d\\u00eda</b>.';
        }

        /* ==============================================================
           MODO B - tu proyecto en tres sitios
           ==============================================================
           Consumos DECLARADOS. Los dos de la placa son medidas tipicas de una
           placa Uno ENTERA (regulador y LED de encendido incluidos), no datos
           de la hoja de caracteristicas del chip: un ATmega328P pelado y
           dormido consume muchisimo menos que 12 mA.                        */
        var PLACA_DESPIERTA = 45;      /* mA a 5 V */
        var PLACA_DORMIDA = 12;        /* mA de media: el regulador no duerme */
        var WIFI_mA = 70;              /* mA mientras el modulo habla */
        var WIFI_SEG = 5;              /* segundos que dura cada envio */
        var WIFI_ENVIOS = 48;          /* envios al dia: uno cada media hora */

        var PROY = [
          {n: 'A \\u00b7 Riego autom\\u00e1tico', act: 'la bomba', mA: 500,
           rot: 'Segundos de bomba al d\\u00eda', min: 0, max: 300, paso: 5, ini: 40,
           uni: function(v){ return coma(v, 0) + ' s'; },
           seg: function(v){ return v; }},
          {n: 'B \\u00b7 Aviso de aula mal ventilada', act: 'el piloto de tres colores', mA: 20,
           rot: 'Horas de piloto encendido', min: 0, max: 24, paso: 1, ini: 24,
           uni: function(v){ return coma(v, 0) + ' h'; },
           seg: function(v){ return v * 3600; }},
          {n: 'C \\u00b7 L\\u00e1mpara que se ajusta sola', act: 'el LED de potencia', mA: 200,
           rot: 'Horas de luz al d\\u00eda', min: 0, max: 12, paso: 0.5, ini: 3,
           uni: function(v){ return coma(v, 1) + ' h'; },
           seg: function(v){ return v * 3600; }}
        ];

        var SITIOS = [
          {n: 'Instituto con enchufe', tipo: 'red', precio: 0.15,
           d: 'Hay enchufe, hay wifi, hay taller y hay alguien que sabe. La energ\\u00eda no es el '
            + 'problema: aqu\\u00ed lo que se mide es el dinero.'},
          {n: 'Aldea sin red el\\u00e9ctrica', tipo: 'sol', panel: 5, sol: 4, rend: 0.7, bat: 20,
           d: 'Un panel de 5 W, unas cuatro horas de sol de las buenas y una bater\\u00eda peque\\u00f1a. '
            + 'La pieza de repuesto m\\u00e1s cercana est\\u00e1 a un d\\u00eda de viaje.'},
          {n: 'Huerto a 3 km del pueblo', tipo: 'pilas', pilas: 15, visita: 30,
           d: 'Ni enchufe ni sitio para el panel: cuatro pilas AA. Alguien sube a verlo <b>una vez al '
            + 'mes</b>, y ese d\\u00eda es el \\u00fanico en que se pueden cambiar.'}
        ];

        function modoB(){
          var P = PROY[proy], S = SITIOS[sitio];
          rotUso.innerHTML = P.rot;
          document.getElementById('v-q2-uso').innerHTML = P.uni(V('uso'));

          var whPlaca = (ctl.duerme.checked ? PLACA_DORMIDA : PLACA_DESPIERTA) / 1000 * 5 * 24;
          var whAct = P.mA / 1000 * 5 * (P.seg(V('uso')) / 3600);
          var whWifi = ctl.wifi.checked
                     ? WIFI_mA / 1000 * 5 * (WIFI_SEG * WIFI_ENVIOS / 3600) : 0;
          var total = whPlaca + whAct + whWifi;
          var pcPlaca = total > 0 ? 100 * whPlaca / total : 0;

          var disp = 0, autonomia = Infinity, rot = '', veredicto = '', bien = false, euros = 0;
          if(S.tipo === 'red'){
            disp = total;
            euros = total * 365 / 1000 * S.precio;
            rot = 'lo da el enchufe';
            bien = true;
            veredicto = 'Aqu\\u00ed sobra energ\\u00eda, as\\u00ed que lo que hay que mirar es el recibo: '
                      + '<b>' + coma(euros, 2) + ' \\u20ac al a\\u00f1o</b> de electricidad.';
          } else if(S.tipo === 'sol'){
            disp = S.panel * S.sol * S.rend;
            autonomia = total > 0 ? S.bat / total : Infinity;
            bien = disp >= total;
            rot = 'entra al d\\u00eda \\u00b7 panel de ' + S.panel + ' W';
            veredicto = bien
              ? 'El panel mete <b>' + coma(disp, 1) + ' Wh al d\\u00eda</b> y el aparato gasta '
                + coma(total, 2) + ': cabe. Con la bater\\u00eda llena aguanta <b>'
                + coma(autonomia, 1) + ' d\\u00edas</b> seguidos sin sol.'
              : 'El panel mete <b>' + coma(disp, 1) + ' Wh al d\\u00eda</b> y el aparato gasta '
                + coma(total, 2) + ': <b>no llega</b>. La bater\\u00eda se vac\\u00eda en '
                + coma(autonomia, 1) + ' d\\u00edas y ya no se vuelve a llenar.';
          } else {
            /* Aqui no entra energia todos los dias: lo que hay es lo que llevan
               guardado las pilas. La columna de la derecha mide eso, y por eso
               su rotulo dice otra cosa. */
            disp = S.pilas;
            autonomia = total > 0 ? S.pilas / total : Infinity;
            bien = autonomia >= S.visita;
            rot = 'guardan cuatro pilas AA';
            veredicto = bien
              ? 'Las pilas aguantan <b>' + coma(autonomia, 1) + ' d\\u00edas</b> y alguien sube cada '
                + S.visita + ': llega.'
              : 'Las pilas aguantan <b>' + coma(autonomia, 1) + ' d\\u00edas</b> y nadie sube hasta el '
                + 'd\\u00eda ' + S.visita + '. El aparato se queda apagado <b>'
                + coma(S.visita - autonomia, 0) + ' d\\u00edas de cada mes</b>, y nadie se entera.';
          }

          /* ---- dos columnas: lo que gasta y lo que hay ---- */
          var s = [], base = 196, altoMax = 118;
          var tope = Math.max(total, disp, 0.001);
          function H(v){ return Math.max(1, altoMax * v / tope); }
          var trozos = [
            {v: whPlaca, c: 'var(--goo-rojo)', n: 'la placa esperando'},
            {v: whAct, c: 'var(--goo-azul)', n: P.act},
            {v: whWifi, c: 'var(--goo-amarillo)', n: 'el wifi'}
          ];
          var yac = base;
          trozos.forEach(function(t){
            if(t.v <= 0) return;
            var hh = H(t.v);
            yac -= hh;
            s.push('<rect x="72" y="' + yac.toFixed(1) + '" width="86" height="' + hh.toFixed(1)
                 + '" fill="' + t.c + '"/>');
          });
          s.push('<text x="115" y="' + (base + 16) + '" class="q2-rot" text-anchor="middle">'
               + 'gasta al d\\u00eda</text>');
          s.push('<text x="115" y="' + (base + 31) + '" class="q2-etq" text-anchor="middle">'
               + coma(total, 2) + ' Wh</text>');
          if(S.tipo === 'red'){
            s.push('<rect x="252" y="' + (base - altoMax) + '" width="86" height="' + altoMax
                 + '" fill="none" stroke="var(--goo-verde)" stroke-width="2" stroke-dasharray="5 4"/>');
            s.push('<text x="295" y="' + (base - altoMax / 2 + 4)
                 + '" class="q2-etq" text-anchor="middle">sin l\\u00edmite</text>');
            s.push('<text x="295" y="' + (base + 31) + '" class="q2-etq" text-anchor="middle">'
                 + coma(euros, 2) + ' \\u20ac/a\\u00f1o</text>');
          } else {
            var hd = H(disp);
            s.push('<rect x="252" y="' + (base - hd).toFixed(1) + '" width="86" height="'
                 + hd.toFixed(1) + '" fill="var(--goo-verde)"/>');
            s.push('<text x="295" y="' + (base + 31) + '" class="q2-etq" text-anchor="middle">'
                 + coma(disp, 1) + ' Wh</text>');
          }
          s.push('<text x="295" y="' + (base + 16) + '" class="q2-rot" text-anchor="middle">'
               + rot + '</text>');
          if(S.tipo === 'pilas'){
            s.push('<text x="295" y="' + (base + 46) + '" class="q2-rot" text-anchor="middle">'
                 + '= ' + coma(autonomia, 1) + ' d\\u00edas, y hacen falta ' + S.visita + '</text>');
          }
          s.push('<line x1="40" y1="' + base + '" x2="400" y2="' + base
               + '" stroke="var(--ink)" stroke-width="1.5"/>');
          s.push('<text x="40" y="24" class="q2-rot">de lo que gasta, ' + coma(pcPlaca, 0)
               + ' % se lo lleva la placa esperando</text>');
          /* La leyenda va ARRIBA: abajo esta la nota de los dias de las pilas y
             las dos se pisaban. El ancho de letra de Roboto Mono a 11 px anda
             por los 7 px, y con 6,2 los rotulos se solapaban entre ellos. */
          var lx = 40;
          trozos.forEach(function(t){
            if(t.v <= 0) return;
            s.push('<rect x="' + lx.toFixed(1) + '" y="36" width="9" height="9" fill="'
                 + t.c + '"/>');
            s.push('<text x="' + (lx + 13).toFixed(1) + '" y="45" class="q2-rot">'
                 + t.n + '</text>');
            lx += 26 + t.n.length * 7.0;
          });
          svg.innerHTML = s.join('');

          tabla.innerHTML =
            f('la placa, 24 h al d\\u00eda', coma(whPlaca, 2) + ' Wh')
          /* tres decimales solo cuando hacen falta: "3,000 Wh" se lee como tres
             mil, y son tres. */
          + f(P.act, coma(whAct, whAct < 0.1 ? 3 : 2) + ' Wh')
          + (ctl.wifi.checked ? f('el m\\u00f3dulo de wifi', coma(whWifi, 2) + ' Wh') : '')
          + f('gasta al d\\u00eda', coma(total, 2) + ' Wh', 'top')
          + (S.tipo === 'red'
              ? f('cuesta de luz al a\\u00f1o', coma(euros, 2) + ' \\u20ac', 'si')
              : f('aguanta sin que nadie venga', coma(autonomia, 1) + ' d\\u00edas',
                  bien ? 'si' : 'no'));

          lee.innerHTML = '<b>' + S.n + '.</b> ' + S.d + '<br><span class="grande'
                        + (bien ? '' : ' malo') + '">' + veredicto + '</span>';

          pie.innerHTML =
            'Todo sale de <b>Wh = V \\u00d7 A \\u00d7 horas</b>, con la placa a 5 V. Consumos que usa la '
          + 'escena: placa Arduino Uno entera despierta, <b>' + PLACA_DESPIERTA + ' mA</b>; con el '
          + 'chip dormido, <b>' + PLACA_DORMIDA + ' mA</b> de media. Esas dos son <b>medidas '
          + 't\\u00edpicas de la placa entera</b>, con su regulador y su LED de encendido, no datos de '
          + 'hoja de caracter\\u00edsticas: un ATmega328P solo y dormido baja a mil\\u00e9simas de eso, y '
          + 'por eso los aparatos a pilas de verdad no llevan una placa Uno. Bomba 500 mA, LED de '
          + 'potencia 200 mA, piloto 20 mA, m\\u00f3dulo de wifi ' + WIFI_mA + ' mA durante '
          + WIFI_SEG + ' s en cada uno de los ' + WIFI_ENVIOS + ' env\\u00edos del d\\u00eda. Cuatro pilas '
          + 'AA alcalinas se cuentan como <b>15 Wh</b> en total. Los tres sitios son inventados; las '
          + 'cuentas que se hacen en ellos, no.';
        }

        function pinta(){ if(M === 'a') modoA(); else modoB(); }

        modo.addEventListener('click', function(e){
          var b = e.target.closest('button[data-m]');
          if(!b) return;
          M = b.dataset.m;
          modo.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          panelA.hidden = (M !== 'a');
          panelB.hidden = (M !== 'b');
          pinta();
        });
        document.getElementById('q2-proy').addEventListener('click', function(e){
          var b = e.target.closest('button[data-p]');
          if(!b) return;
          proy = +b.dataset.p;
          this.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          var P = PROY[proy];
          ctl.uso.min = P.min; ctl.uso.max = P.max; ctl.uso.step = P.paso; ctl.uso.value = P.ini;
          pinta();
        });
        document.getElementById('q2-sitio').addEventListener('click', function(e){
          var b = e.target.closest('button[data-s]');
          if(!b) return;
          sitio = +b.dataset.s;
          this.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          pinta();
        });
        ['gente', 'litros', 'caudal', 'juego', 'uso'].forEach(function(k){
          ctl[k].addEventListener('input', pinta);
        });
        ['duerme', 'wifi'].forEach(function(k){
          ctl[k].addEventListener('change', pinta);
        });
        pinta();
      })();
      </script>
'''
