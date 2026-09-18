# -*- coding: utf-8 -*-
"""Las escenas interactivas de las sesiones 4, 5 y 6 de la U9.

Mismo criterio que u9_escenas.py: SVG y JavaScript a mano, sin librerias, y
todas CALCULAN. Ninguna lleva dentro una tabla de resultados escrita a mano.

  ESCENA_LICENCIAS  S4 · el mezclador. Se eligen las piezas que has metido en el
                    trabajo y sale la licencia que puede llevar el resultado,
                    aplicando las reglas de las cuatro condiciones (BY, NC, ND,
                    SA) una por una. El dominio publico por antiguedad se
                    CALCULA con el plazo legal y con el ano de HOY, no con una
                    fecha escrita a mano.
  ESCENA_PISAR      S5 · la probabilidad de que dos personas toquen el mismo
                    apartado es el problema del cumpleanos, con su formula
                    exacta; y el numero de trozos que se pierden al juntar las
                    copias a mano es una esperanza matematica, no una
                    estimacion.
  ESCENA_LECTOR     S6 · lo que anuncia un lector de pantalla, deducido de la
                    estructura de la pagina. Los tiempos salen de contar
                    palabras y dividir por la velocidad de locucion.
  ESCENA_CONTRASTE  S6 · la razon de contraste de la WCAG 2, con su formula
                    exacta (luminancia relativa sRGB). El numero que sale es
                    comprobable contra cualquier otra herramienta.

Geometria: cada escena dice arriba de que tamano es su lienzo y como se
reparte. Nada esta puesto a ojo.

Las cadenas de JS llevan \\uXXXX y no entidades HTML: una entidad HTML dentro de
una cadena de JavaScript se dibuja como seis caracteres y descuadra el ancho.
El pie de cada escena, en cambio, se pone con innerHTML, y ahi las entidades van
bien.
"""


def _js(s):
    """Un texto de Python, listo para ir dentro de una cadena de JavaScript."""
    out = []
    for ch in s:
        if ch == u'\\':
            out.append(u'\\\\')
        elif ch == u"'":
            out.append(u"\\'")
        elif ord(ch) < 128:
            out.append(ch)
        else:
            out.append(u'\\u%04x' % ord(ch))
    return u''.join(out)


def _lit(s):
    return u"'" + _js(s) + u"'"


# ===========================================================================
# S4 · El mezclador de licencias
#
# Lienzo 640 x 330.
#   Rotulo de la tabla      y = 22
#   Ocho filas de 26 px, la i-esima con el borde superior en y = 32 + 26*i,
#     asi que la ultima ocupa 214..238. Dentro de cada fila:
#       semaforo   cx = 30                (circulo de r = 6)
#       nombre     x  = 46   (12 px)      hasta x = 330
#       licencia   x  = 336  (11 px)      hasta x = 452
#       veredicto  x  = 618, anclado a la derecha (11 px): 166 px, y el
#                  veredicto mas largo -"dominio publico desde 2016", 26
#                  caracteres- gasta 11*0.6*26 = 172 px en la tipografia mono.
#                  Por eso los veredictos largos se abrevian en TEXTO_CORTO.
#   Cuadro del resultado    y = 250..314   (x 16..624)
#     titulo del resultado  y = 276  (15 px)
#     razon                 y = 300  (11.5 px, 88 caracteres como mucho)
#
# Las reglas: ND no se puede modificar (pero si acompanar sin tocarlo), SA
# obliga al resultado a llevar SA, NC obliga al resultado a llevar NC, y SA sin
# NC junto con NC es INCOMPATIBLE -CC BY-SA no admite la condicion de no
# comercial-. El dominio publico por antiguedad se calcula con el plazo del
# texto refundido de la Ley de Propiedad Intelectual: 80 anos para los autores
# fallecidos antes del 7-12-1987 y 70 para los de despues, contados desde el 1
# de enero del ano siguiente al de la muerte.
# ===========================================================================
_PIEZAS_JS = u"""
        var PIEZAS = [
          {id:'texto',  n:'Tu texto y tus dibujos',
           lic:'Obra tuya',                    tipo:'propio'},
          {id:'foto',   n:'Una foto sacada de Wikimedia Commons',
           lic:'CC BY-SA 4.0',                 tipo:'cc', by:1, nc:0, nd:0, sa:1,
           autor:'Prosthetic Head', obra:'Colour Sensor Macro',
           url:'commons.wikimedia.org/wiki/File:Colour_Sensor_Macro.jpg'},
          {id:'musica', n:'M\\u00fasica de fondo de un banco de sonidos',
           lic:'CC BY-NC 4.0',                 tipo:'cc', by:1, nc:1, nd:0, sa:0,
           autor:'Mar Ib\\u00e1\\u00f1ez', obra:'Tema de apertura',
           url:'el banco de sonidos donde la encontraste'},
          {id:'icono',  n:'Un icono de una colecci\\u00f3n libre',
           lic:'CC0 (renuncia)',               tipo:'cc', by:0, nc:0, nd:0, sa:0},
          {id:'video',  n:'Un trozo de v\\u00eddeo de otro canal',
           lic:'CC BY-ND 4.0',                 tipo:'cc', by:1, nc:0, nd:1, sa:0,
           autor:'Canal Divulga', obra:'C\\u00f3mo pandea una barra',
           url:'el enlace del v\\u00eddeo'},
          {id:'blog',   n:'Una foto que has encontrado en un blog',
           lic:'Todos los derechos reservados', tipo:'reservados'},
          {id:'grab35', n:'Un grabado antiguo, autor fallecido en 1935',
           lic:'\\u00bfDominio p\\u00fablico?',  tipo:'muerte', muerte:1935,
           autor:'Ricardo Mar\\u00edn', obra:'Grabado del taller',
           url:'de d\\u00f3nde lo hayas sacado'},
          {id:'grab62', n:'Otro grabado, autor fallecido en 1962',
           lic:'\\u00bfDominio p\\u00fablico?',  tipo:'muerte', muerte:1962}
        ];
"""

ESCENA_LICENCIAS = u'''
      <div class="escena" id="esc-licencias">
        <div class="escena-barra">
          <span class="escena-titulo">Lo tuyo y lo que has cogido con licencia libre</span>
          <div class="seg" id="seg-lic-a">
            <button type="button" data-p="texto" aria-pressed="true">Tu texto</button>
            <button type="button" data-p="foto" aria-pressed="true">Foto CC BY-SA</button>
            <button type="button" data-p="musica">M&uacute;sica CC BY-NC</button>
            <button type="button" data-p="icono" aria-pressed="true">Icono CC0</button>
            <button type="button" data-p="video">V&iacute;deo CC BY-ND</button>
          </div>
        </div>
        <div class="escena-barra">
          <span class="escena-titulo">Y estas tres, que traen sorpresa</span>
          <div class="seg" id="seg-lic-b">
            <button type="button" data-p="blog">Foto de un blog</button>
            <button type="button" data-p="grab35">Grabado de 1935</button>
            <button type="button" data-p="grab62">Grabado de 1962</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 330" id="svg-licencias" role="img"
               aria-label="Las piezas que has metido en el trabajo, si se pueden usar y qu&eacute; licencia puede llevar el resultado"></svg>
        </div>
        <div class="pie" id="pie-licencias"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-licencias');
        if(!svg) return;
        var pie = document.getElementById('pie-licencias');

        var HOY = new Date().getFullYear();   /* el ano de verdad, no uno escrito */

''' + _PIEZAS_JS + u'''
        var sel = {texto:true, foto:true, icono:true};

        function escapa(s){
          return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
        }
        function texto(x, y, t, op){
          op = op || {};
          return '<text x="'+x+'" y="'+y+'" class="rotulo-svg" style="font-size:'+(op.s || 11)
               + 'px'+(op.c ? ';fill:'+op.c : '')+(op.p ? ';font-weight:500' : '')
               + (op.a ? ';text-anchor:'+op.a : '')+(op.f ? ';font-family:var(--f-b)' : '')
               + ';letter-spacing:0">'+t+'</text>';
        }

        var COLOR = {v:'var(--goo-verde)', a:'var(--goo-amarillo)', r:'var(--goo-rojo)'};

        /* ---- la cuenta: se aplican las reglas pieza a pieza ---- */
        function calcula(){
          var puestas = PIEZAS.filter(function(p){ return sel[p.id]; });
          var est = {}, citas = [];
          var by = false, nc = false, sa = false, saEsNC = false;
          var bloqueo = null, usables = 0;

          puestas.forEach(function(p){
            if(p.tipo === 'propio'){
              est[p.id] = {c:'v', v:'es tuya: decides t\\u00fa'};
              usables++;
              return;
            }
            if(p.tipo === 'reservados'){
              /* El veredicto va corto a proposito: a 10,5 px en la tipografia
                 mono, 13 caracteres ocupan 82 px y empiezan en x = 536, que
                 queda a la derecha de donde acaba la licencia mas larga (519). */
              est[p.id] = {c:'r', v:'falta permiso'};
              bloqueo = bloqueo || 'reservados';
              return;
            }
            if(p.tipo === 'muerte'){
              /* Plazo del TRLPI: 80 anos si el autor murio antes del 7-12-1987 y
                 70 si murio despues, contados desde el 1 de enero del ano
                 siguiente al de la muerte. Por eso el "+ 1". */
              var anios = p.muerte < 1987 ? 80 : 70;
              var libre = p.muerte + anios + 1;
              p._libre = libre; p._anios = anios;
              if(libre <= HOY){
                est[p.id] = {c:'v', v:'libre desde ' + libre};
                usables++;
                if(p.autor) citas.push({obra:p.obra, autor:p.autor,
                                        lic:'Dominio p\\u00fablico', url:p.url});
              } else {
                est[p.id] = {c:'r', v:'protegida hasta ' + (libre - 1)};
                bloqueo = bloqueo || 'plazo';
              }
              return;
            }
            /* piezas con licencia Creative Commons */
            if(p.nd){
              est[p.id] = {c:'a', v:'s\\u00ed, pero sin tocarlo'};
              usables++;
              if(p.by) citas.push(p);
              return;
            }
            if(p.by){ by = true; citas.push(p); }
            if(p.nc){ nc = true; }
            if(p.sa){ sa = true; if(p.nc) saEsNC = true; }
            est[p.id] = {c:'v', v: p.by ? 's\\u00ed, citando al autor' : 's\\u00ed, sin condiciones'};
            usables++;
          });

          /* CC BY-SA obliga a que el resultado sea CC BY-SA, y CC BY-SA no
             admite la condicion de no comercial: las dos juntas no se pueden. */
          var choque = sa && nc && !saEsNC;
          if(choque && !bloqueo){
            /* Cuando el problema es el choque, las dos piezas que chocan se
               marcan en ambar: cada una por separado se puede usar, y eso es
               justo lo que despista. */
            puestas.forEach(function(p){
              if(p.tipo === 'cc' && !p.nd && (p.sa || p.nc)){
                est[p.id] = {c:'a', v:'choca con la otra'};
              }
            });
          }

          var res, razon, ok;
          if(bloqueo === 'reservados'){
            ok = false;
            res = 'NO lo puedes publicar';
            razon = 'Hay una pieza con todos los derechos reservados: sin permiso por escrito '
                  + 'del autor, no se puede.';
          } else if(bloqueo === 'plazo'){
            ok = false;
            res = 'NO lo puedes publicar todav\\u00eda';
            razon = 'Que una obra sea antigua no quiere decir que sea libre: hay una que '
                  + 'todav\\u00eda est\\u00e1 en plazo.';
          } else if(choque){
            ok = false;
            res = 'Estas dos no se pueden mezclar';
            razon = 'CompartirIgual obliga a publicar en CC BY-SA, y CC BY-SA no admite la '
                  + 'condici\\u00f3n NoComercial.';
          } else if(sa){
            ok = true;
            res = 'CC BY' + (nc ? '-NC' : '') + '-SA 4.0, obligatoria';
            razon = 'CompartirIgual: quien te deja su pieza te obliga a dejar la tuya en las '
                  + 'mismas condiciones.';
          } else if(nc){
            ok = true;
            res = 'CC BY-NC 4.0 (o m\\u00e1s cerrada)';
            razon = 'Hay una pieza NoComercial: con ella dentro, tu trabajo no se puede usar para '
                  + 'ganar dinero.';
          } else if(by){
            ok = true;
            res = 'La que t\\u00fa quieras, citando';
            razon = 'Nadie te obliga a una licencia concreta, pero cada autor tiene que aparecer '
                  + 'con su nombre.';
          } else {
            ok = true;
            res = 'La que t\\u00fa quieras';
            razon = 'Todo lo que has metido es tuyo o no tiene condiciones. Esta web elige '
                  + 'CC BY-SA 4.0.';
          }
          return {puestas:puestas, est:est, citas:citas, res:res, razon:razon, ok:ok,
                  usables:usables, choque:choque, sa:sa, nc:nc, by:by, bloqueo:bloqueo};
        }

        function pinta(){
          var c = calcula();
          var s = '';

          s += texto(20, 22, 'LO QUE HAS METIDO EN EL TRABAJO  \\u00b7  '
                   + c.puestas.length + ' DE ' + PIEZAS.length + ' PIEZAS', {s:10.5, p:1});

          PIEZAS.forEach(function(p, i){
            var y = 32 + 26*i, dentro = !!sel[p.id];
            var e = c.est[p.id];
            s += '<rect x="16" y="'+y+'" width="608" height="24" fill="'
               + (dentro ? 'var(--surface-2)' : 'none')+'" stroke="var(--line-soft)" '
               + 'stroke-width="1"></rect>';
            if(dentro){
              s += '<circle cx="30" cy="'+(y+12)+'" r="6" fill="'+COLOR[e.c]+'"></circle>';
            } else {
              s += '<circle cx="30" cy="'+(y+12)+'" r="6" fill="none" stroke="var(--line)" '
                 + 'stroke-width="1.5"></circle>';
            }
            s += texto(46, y+16, escapa(p.n),
                       {s:12, f:1, c: dentro ? 'var(--ink)' : 'var(--ink-soft)'});
            s += texto(336, y+16, escapa(p.lic), {s:10.5,
                       c: dentro ? 'var(--ink-soft)' : 'var(--line)'});
            s += texto(618, y+16, dentro ? e.v : 'no la usas',
                       {s:10.5, a:'end', p:dentro, c: dentro ? COLOR[e.c] : 'var(--line)'});
          });

          s += '<rect x="16" y="250" width="608" height="64" fill="'
             + (c.ok ? 'var(--accent-soft)' : 'var(--surface-2)')+'" stroke="'
             + (c.ok ? 'var(--goo-verde)' : 'var(--goo-rojo)')+'" stroke-width="2"></rect>';
          s += texto(32, 272, c.ok ? 'TU TRABAJO PUEDE SALIR CON:' : 'AS\\u00cd NO:', {s:10, p:1});
          s += texto(32, 294, c.res, {s:16, p:1, f:1,
                     c: c.ok ? 'var(--goo-verde)' : 'var(--goo-rojo)'});

          svg.innerHTML = s;

          var t = '<b>' + c.razon + '</b> ';
          if(c.choque && !c.bloqueo){
            t += 'Es el enredo que casi nadie ve venir: las dos piezas son <b>libres</b> y aun '
               + 'as\\u00ed no se pueden juntar. &laquo;Libre&raquo; no es una sola cosa.';
          } else if(c.bloqueo === 'plazo'){
            var g = PIEZAS.filter(function(p){ return sel[p.id] && p.tipo === 'muerte'
                                                      && p._libre > HOY; })[0];
            t += 'El autor muri&oacute; en <b>' + g.muerte + '</b>, as&iacute; que el plazo son '
               + '<b>' + g._anios + ' a&ntilde;os</b> contados desde el 1 de enero de '
               + (g.muerte + 1) + ': entra en dominio p&uacute;blico el <b>1 de enero de '
               + g._libre + '</b>. Hoy estamos en ' + HOY + '.';
          }
          if(c.citas.length){
            t += '<br><b>Lo que tienes que escribir debajo de cada una:</b><br>'
               + c.citas.map(function(p){
                   return '<span style="font-family:var(--f-m);font-size:12px">'
                        + escapa(p.obra) + ' &middot; ' + escapa(p.autor) + ' &middot; '
                        + escapa(p.lic) + ' &middot; ' + escapa(p.url) + '</span>';
                 }).join('<br>');
          }
          t += '<br><span style="font-size:12.5px">Las reglas se aplican una a una: '
             + '<b>ND</b> no deja modificar, <b>SA</b> obliga a publicar igual, <b>NC</b> '
             + 'obliga a que no se gane dinero y <b>BY</b> obliga a citar. El a&ntilde;o de '
             + 'dominio p&uacute;blico sale del plazo legal y del a&ntilde;o de <b>hoy</b> '
             + '(' + HOY + '), no de una fecha escrita aqu&iacute;. Se supone que lo mezclas todo '
             + 'en <b>una sola obra</b>; si cada pieza va suelta, cada una conserva la suya.'
             + '</span>';
          pie.innerHTML = t;
        }

        [document.getElementById('seg-lic-a'),
         document.getElementById('seg-lic-b')].forEach(function(caja){
          caja.addEventListener('click', function(e){
            var b = e.target.closest('button[data-p]'); if(!b) return;
            var id = b.dataset.p;
            sel[id] = !sel[id];
            b.setAttribute('aria-pressed', sel[id] ? 'true' : 'false');
            pinta();
          });
        });

        pinta();
      })();
      </script>
'''


# ===========================================================================
# S5 · Si nos lo vamos pasando, nos pisamos
#
# Lienzo 640 x 380.
#   Tres tarjetas arriba: y 32..142, anchura 196, en x = 16, 222 y 428
#     (16 + 196 = 212, +10 de hueco = 222; 222 + 196 = 418, +10 = 428;
#      428 + 196 = 624, que es justo el margen derecho).
#     rotulo en dos lineas  y +18 y +32   ·   cifra y +82   ·   unidad y +100
#   Dibujo                  y 154..300
#     modo "nos lo pasamos": N+1 iconos de 34 x 44 con 14 de hueco, centrados
#       en la franja 16..624, con el rotulo debajo en y = 262
#     modo "un solo documento": N circulos de persona en x = 46, un icono
#       grande en x 150..214 y el historial en x 300..612
#   Frase de cierre         y 312..368
#
# La probabilidad es la del problema del cumpleanos, exacta:
#   p = 1 - (S/S)(S-1/S)...(S-N+1/S)
# y los trozos que se pierden son la esperanza del numero de personas menos el
# numero esperado de apartados distintos elegidos:
#   E = N - S*(1 - (1 - 1/S)^N)
# Las dos son cuentas cerradas, no simulaciones ni estimaciones.
# ===========================================================================
ESCENA_PISAR = u'''
      <div class="escena" id="esc-pisar">
        <div class="escena-barra">
          <span class="escena-titulo">El grupo y el trabajo</span>
          <div class="seg" id="seg-pis-g">
            <button type="button" data-n="2">2 personas</button>
            <button type="button" data-n="3">3</button>
            <button type="button" data-n="4" aria-pressed="true">4</button>
            <button type="button" data-n="5">5</button>
            <button type="button" data-n="6">6</button>
            <button type="button" data-s="4">4 apartados</button>
            <button type="button" data-s="8" aria-pressed="true">8</button>
            <button type="button" data-s="12">12</button>
            <button type="button" data-s="20">20</button>
          </div>
        </div>
        <div class="escena-barra">
          <span class="escena-titulo">Y c&oacute;mo trabaj&aacute;is</span>
          <div class="seg" id="seg-pis-m">
            <button type="button" data-m="pasa" aria-pressed="true">Nos lo pasamos por el m&oacute;vil</button>
            <button type="button" data-m="uno">Un solo documento</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 380" id="svg-pisar" role="img"
               aria-label="Probabilidad de que dos personas toquen el mismo apartado, ficheros en circulaci&oacute;n y trabajo que se pierde"></svg>
        </div>
        <div class="pie" id="pie-pisar"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-pisar');
        if(!svg) return;
        var pie = document.getElementById('pie-pisar');

        var N = 4, S = 8, modo = 'pasa';

        function texto(x, y, t, op){
          op = op || {};
          return '<text x="'+x+'" y="'+y+'" class="rotulo-svg" style="font-size:'+(op.s || 11)
               + 'px'+(op.c ? ';fill:'+op.c : '')+(op.p ? ';font-weight:500' : '')
               + (op.a ? ';text-anchor:'+op.a : '')+(op.f ? ';font-family:var(--f-b)' : '')
               + ';letter-spacing:0">'+t+'</text>';
        }
        function num(v, d){
          return v.toFixed(d === undefined ? 1 : d).replace('.', ',');
        }

        /* ---- las dos cuentas ---- */
        function choque(){
          /* Problema del cumpleanos: probabilidad de que al menos dos de las N
             personas elijan el mismo apartado de los S que hay. */
          if(N > S) return 1;
          var libre = 1;
          for(var i = 0; i < N; i++) libre *= (S - i) / S;
          return 1 - libre;
        }
        function perdidos(){
          /* Esperanza de cuantas ediciones se sobrescriben al juntar las copias
             a mano quedandose con una por apartado: personas menos apartados
             distintos elegidos. */
          return N - S * (1 - Math.pow(1 - 1/S, N));
        }

        function icono(x, y, col, relleno){
          /* Icono de fichero de 34 x 44 con la esquina doblada. */
          var s = '<path d="M'+x+' '+y+' h24 l10 10 v34 h-34 Z" fill="'+(relleno || 'var(--surface)')
                + '" stroke="'+col+'" stroke-width="1.8" stroke-linejoin="round"></path>';
          s += '<path d="M'+(x+24)+' '+y+' v10 h10" fill="none" stroke="'+col
             + '" stroke-width="1.8" stroke-linejoin="round"></path>';
          for(var i = 0; i < 3; i++){
            s += '<path d="M'+(x+7)+' '+(y+20+i*7)+' h20" stroke="'+col
               + '" stroke-width="1.4" opacity=".5"></path>';
          }
          return s;
        }

        function tarjeta(x, r1, r2, cifra, unidad, col){
          var s = '<rect x="'+x+'" y="32" width="196" height="110" fill="var(--surface-2)" '
                + 'stroke="var(--line)" stroke-width="1"></rect>';
          s += '<rect x="'+x+'" y="32" width="196" height="3" fill="'+col+'"></rect>';
          s += texto(x+14, 62, r1, {s:10, p:1});
          s += texto(x+14, 76, r2, {s:10, p:1});
          s += texto(x+14, 114, cifra, {s:30, p:1, f:1, c:col});
          s += texto(x+14, 132, unidad, {s:10.5});
          return s;
        }

        function pinta(){
          var p = choque(), perd = modo === 'pasa' ? perdidos() : 0;
          var ficheros = modo === 'pasa' ? N + 1 : 1;
          var compara = modo === 'pasa' ? S * N : 0;
          var s = '';

          s += tarjeta(16, 'PROBABILIDAD DE QUE DOS',
                       'TOQUEN EL MISMO APARTADO', num(p*100) + ' %', 'sin ponerse de acuerdo',
                       p > 0.5 ? 'var(--goo-rojo)' : 'var(--goo-amarillo)');
          s += tarjeta(222, 'FICHEROS DISTINTOS',
                       'DANDO VUELTAS', String(ficheros),
                       ficheros === 1 ? 'uno, y siempre el mismo' : 'y ninguno es el bueno',
                       ficheros === 1 ? 'var(--goo-verde)' : 'var(--goo-rojo)');
          s += tarjeta(428, 'DE MEDIA, TROZOS DE',
                       'TRABAJO QUE SE PIERDEN', num(perd),
                       perd === 0 ? 'no se pierde nada' : 'por cada vuelta',
                       perd === 0 ? 'var(--goo-verde)' : 'var(--goo-rojo)');

          if(modo === 'pasa'){
            var total = ficheros*34 + (ficheros-1)*14;
            var x0 = 16 + (608 - total)/2;
            s += texto(20, 170, 'EL MISMO TRABAJO, EN ' + ficheros + ' SITIOS A LA VEZ',
                       {s:10, p:1});
            for(var i = 0; i < ficheros; i++){
              var x = x0 + i*48;
              s += icono(x, 190, i === 0 ? 'var(--goo-azul)' : 'var(--goo-rojo)');
              s += texto(x+17, 250, i === 0 ? 'original'
                         : String.fromCharCode(65 + i - 1), {s:10, a:'middle'});
            }
            s += texto(20, 276, 'Para juntarlo hay que mirar los ' + S + ' apartados en cada copia: '
                       + compara + ' comparaciones a mano.', {s:12, f:1, c:'var(--goo-rojo)'});
          } else {
            s += texto(20, 170, 'EL MISMO TRABAJO, EN UN SOLO SITIO', {s:10, p:1});
            for(var j = 0; j < N; j++){
              /* N va de 2 a 6: las personas se reparten entre y = 190 e y = 290 */
              var cy = 190 + j*(100/(N - 1));
              s += '<circle cx="46" cy="'+cy.toFixed(1)+'" r="10" fill="none" '
                 + 'stroke="var(--goo-azul)" stroke-width="1.8"></circle>';
              s += '<path d="M60 '+cy.toFixed(1)+' L144 220" stroke="var(--goo-azul)" '
                 + 'stroke-width="1.2" opacity=".55"></path>';
            }
            s += icono(150, 198, 'var(--goo-verde)', 'var(--surface)');
            s += texto(167, 262, 'uno', {s:10, a:'middle'});
            s += texto(300, 176, 'EL HISTORIAL: TODAS LAS VERSIONES SIGUEN AH\\u00cd', {s:10, p:1});
            for(var k = 0; k < 5; k++){
              var yy = 190 + k*20;
              s += '<rect x="300" y="'+yy+'" width="'+(300 - k*26)+'" height="14" fill="'
                 + (k === 0 ? 'var(--goo-verde)' : 'var(--line-soft)')+'" opacity="'
                 + (k === 0 ? '.85' : '1')+'"></rect>';
              s += texto(608, yy+11, k === 0 ? 'ahora' : 'hace ' + k + 'h',
                         {s:9.5, a:'end'});
            }
            s += texto(20, 276, 'Se sigue tocando lo mismo, pero no se pierde: se ve qui\\u00e9n '
                       + 'escribe y se puede volver atr\\u00e1s.', {s:12, f:1,
                        c:'var(--goo-verde)'});
          }

          s += '<rect x="16" y="312" width="608" height="56" fill="var(--surface-2)"></rect>';
          var frase;
          if(modo === 'pasa'){
            frase = p > 0.5
              ? 'M\\u00e1s de la mitad de las veces, dos de vosotros escriben encima del mismo '
                + 'apartado.'
              : 'Aun as\\u00ed, una de cada ' + Math.round(1/Math.max(p, 0.0001))
                + ' veces alguien reescribe lo que ya hab\\u00eda hecho otro.';
          } else {
            frase = 'La probabilidad de arriba no baja: lo que baja a cero es lo que se pierde.';
          }
          s += texto(34, 346, frase, {s:13.5, f:1,
                     c: modo === 'pasa' ? 'var(--goo-rojo)' : 'var(--goo-verde)'});

          svg.innerHTML = s;

          var t = 'Con <b>' + N + ' personas</b> y <b>' + S + ' apartados</b>, la probabilidad de '
                + 'que al menos dos elijan el mismo es <b>' + num(p*100) + ' %</b>. Sale de una '
                + 'cuenta cerrada, la misma con la que se calcula que en una clase de treinta haya '
                + 'dos cumplea&ntilde;os el mismo d&iacute;a: se multiplica lo que queda libre '
                + 'cada vez &mdash;' + S + '/' + S + ' &times; ' + (S-1) + '/' + S
                + ' &times; &hellip;&mdash; y se resta de uno. ';
          if(modo === 'pasa'){
            t += 'Y al juntar las copias a mano qued&aacute;ndose con una versi&oacute;n de cada '
               + 'apartado, de media se tiran <b>' + num(perd) + ' apartados ya escritos</b> por '
               + 'vuelta, despu&eacute;s de <b>' + compara + ' comparaciones</b>.';
          } else {
            t += 'Lo importante: <b>la probabilidad es exactamente la misma</b>. Trabajar en un '
               + 'solo documento <b>no evita</b> que dos toqu&eacute;is lo mismo; evita que se '
               + '<b>pierda</b>, porque se ve en directo qui&eacute;n escribe d&oacute;nde y '
               + 'porque queda guardado lo que hab&iacute;a antes.';
          }
          t += '<br><span style="font-size:12.5px">Las dos cifras son cuentas exactas, no '
             + 'simulaciones: la probabilidad es la del problema del cumplea&ntilde;os y los '
             + 'trozos perdidos son una <b>media</b> (por eso salen con decimales: en una vuelta '
             + 'concreta ser&aacute;n 0, 1 o 2). Lo que s&iacute; es un supuesto nuestro es que '
             + 'cada uno empieza por donde le apetece; ponerse de acuerdo antes es gratis y baja '
             + 'esa probabilidad a cero.</span>';
          pie.innerHTML = t;
        }

        function marca(caja, attr, valor){
          caja.querySelectorAll('button['+attr+']').forEach(function(b){
            b.setAttribute('aria-pressed',
              b.getAttribute(attr) === String(valor) ? 'true' : 'false');
          });
        }
        var cajaG = document.getElementById('seg-pis-g');
        var cajaM = document.getElementById('seg-pis-m');
        cajaG.addEventListener('click', function(e){
          var b = e.target.closest('button'); if(!b) return;
          if(b.dataset.n){ N = +b.dataset.n; marca(cajaG, 'data-n', N); }
          else if(b.dataset.s){ S = +b.dataset.s; marca(cajaG, 'data-s', S); }
          else return;
          pinta();
        });
        cajaM.addEventListener('click', function(e){
          var b = e.target.closest('button[data-m]'); if(!b) return;
          modo = b.dataset.m; marca(cajaM, 'data-m', modo); pinta();
        });

        pinta();
      })();
      </script>
'''


# ===========================================================================
# S6 · Lo que oye quien no ve la pantalla
#
# Lienzo 640 x 400.
#   Rotulo                  y = 22
#   Diez filas con paso de 24 px desde y = 32: la i-esima empieza en 32 + 24*i y
#     mide 22, asi que la decima ocupa 248..270 y deja 12 px hasta los cuadros
#     de abajo. (Con paso 26 se metia debajo de ellos: medido en la captura.)
#     Dentro de cada fila:
#       etiqueta de tipo   x = 24  (9,5 px, mono)  anchura reservada 104 px
#       lo que anuncia     x = 134 (12 px)         hasta x = 620
#   Dos cuadros de cuentas  y 282..386, anchura 300, en x = 16 y 324
#     rotulo y +20 · cifra y +58 · pie y +80
#
# Nada de esto esta escrito a mano: la lista de lo que anuncia el lector se
# DEDUCE de la estructura de la pagina (si el titulo esta marcado como titulo o
# solo pintado, si la imagen tiene texto alternativo o no), y los tiempos salen
# de contar palabras y dividir por la velocidad de locucion.
# ===========================================================================
_PAGINA_JS = u"""
        var PAGINA = [
          {t:'h1', txt:'Nuestro puente de palillos', pal:4},
          {t:'p',  pal:62},
          {t:'img', arch:'DSC_0421.JPG',
           alt:'El puente terminado, visto de lado, con la bolsa de pesas colgando del centro',
           altPal:15},
          {t:'h2', txt:'C\\u00f3mo lo hicimos', pal:3},
          {t:'p',  pal:78},
          {t:'img', arch:'grafico2.png',
           alt:'Gr\\u00e1fico: aguant\\u00f3 1.400 g y rompi\\u00f3 por la diagonal derecha',
           altPal:11},
          {t:'h2', txt:'Lo que aguant\\u00f3', pal:3},
          {t:'p',  pal:54},
          {t:'h2', txt:'Lo que cambiar\\u00edamos', pal:3},
          {t:'p',  pal:41}
        ];
"""

ESCENA_LECTOR = u'''
      <div class="escena" id="esc-lector">
        <div class="escena-barra">
          <span class="escena-titulo">C&oacute;mo est&aacute; hecha la p&aacute;gina</span>
          <div class="seg" id="seg-lec-m">
            <button type="button" data-m="pintado" aria-pressed="true">Como se hace casi siempre</button>
            <button type="button" data-m="marcado">Marcada de verdad</button>
          </div>
        </div>
        <div class="escena-barra">
          <span class="escena-titulo">Y c&oacute;mo la recorre</span>
          <div class="seg" id="seg-lec-v">
            <button type="button" data-v="todo" aria-pressed="true">Escucharlo todo seguido</button>
            <button type="button" data-v="salta">Saltar de t&iacute;tulo en t&iacute;tulo</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 400" id="svg-lector" role="img"
               aria-label="Lo que un lector de pantalla anuncia de la p&aacute;gina, seg&uacute;n c&oacute;mo est&eacute; marcada"></svg>
        </div>
        <div class="pie" id="pie-lector"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-lector');
        if(!svg) return;
        var pie = document.getElementById('pie-lector');

        var VEL = 180;      /* palabras por minuto de locucion */
        var COSTE_ARCH = 4; /* segundos en deletrear el nombre de un fichero */
        var COSTE_SALTO = 1.2;

''' + _PAGINA_JS + u'''
        var modo = 'pintado', vista = 'todo';

        function escapa(s){
          return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
        }
        function texto(x, y, t, op){
          op = op || {};
          return '<text x="'+x+'" y="'+y+'" class="rotulo-svg" style="font-size:'+(op.s || 11)
               + 'px'+(op.c ? ';fill:'+op.c : '')+(op.p ? ';font-weight:500' : '')
               + (op.a ? ';text-anchor:'+op.a : '')+(op.f ? ';font-family:var(--f-b)' : '')
               + ';letter-spacing:0">'+t+'</text>';
        }
        function seg(v){ return v.toFixed(1).replace('.', ',') + ' s'; }

        /* ---- lo que anuncia el lector, deducido de la estructura ---- */
        function recorre(){
          var filas = [], t = 0, titulos = 0, descritas = 0, saltos = 0;
          PAGINA.forEach(function(b){
            var f = {};
            if(b.t === 'h1' || b.t === 'h2'){
              /* En el modo "como se hace casi siempre" NINGUN titulo esta
                 marcado, tampoco el de la portada: lo normal es escribirlo,
                 centrarlo y subirle el cuerpo, que es justo lo que el programa
                 no entiende. Es lo que ya se vio con el indice automatico. */
              var marcado = (modo === 'marcado');
              f.salta = marcado;
              f.tag = marcado ? (b.t === 'h1' ? 'T\\u00cdTULO 1' : 'T\\u00cdTULO 2') : 'TEXTO';
              f.txt = marcado
                ? 'Encabezado de nivel ' + (b.t === 'h1' ? '1' : '2') + ': ' + b.txt
                : b.txt + '  (el lector no sabe que esto era un t\\u00edtulo)';
              f.c = marcado ? 'var(--goo-verde)' : 'var(--goo-rojo)';
              if(marcado){ titulos++; saltos++; }
              t += b.pal / VEL * 60;
            } else if(b.t === 'p'){
              f.salta = false;
              f.tag = 'P\\u00c1RRAFO';
              f.txt = b.pal + ' palabras de texto seguido';
              f.c = 'var(--ink-soft)';
              t += b.pal / VEL * 60;
            } else {
              var conAlt = modo === 'marcado';
              f.salta = false;
              f.tag = 'IMAGEN';
              f.txt = conAlt ? 'Imagen: ' + b.alt
                             : 'Imagen, ' + b.arch + '  (no hay nada que leer)';
              f.c = conAlt ? 'var(--goo-verde)' : 'var(--goo-rojo)';
              if(conAlt){ descritas++; t += b.altPal / VEL * 60; }
              else t += COSTE_ARCH;
            }
            f.b = b;
            filas.push(f);
          });
          var imgs = PAGINA.filter(function(b){ return b.t === 'img'; }).length;
          var cabec = PAGINA.filter(function(b){ return b.t === 'h1' || b.t === 'h2'; }).length;
          return {filas:filas, todo:t, titulos:titulos, cabec:cabec,
                  descritas:descritas, imgs:imgs, salto: saltos * COSTE_SALTO, saltos:saltos};
        }

        function pinta(){
          var r = recorre();
          var s = '';

          s += texto(20, 22, vista === 'todo'
                   ? 'LO QUE VA DICIENDO, DE ARRIBA ABAJO'
                   : 'LO QUE ENCUENTRA SI PIDE IR DE T\\u00cdTULO EN T\\u00cdTULO', {s:10.5, p:1});

          var visibles = vista === 'todo' ? r.filas : r.filas.filter(function(f){ return f.salta; });
          if(!visibles.length){
            s += '<rect x="16" y="32" width="608" height="52" fill="var(--surface-2)" '
               + 'stroke="var(--goo-rojo)" stroke-width="1.5"></rect>';
            s += texto(32, 64, 'Nada. No hay ni un solo apartado al que saltar.',
                       {s:14, f:1, p:1, c:'var(--goo-rojo)'});
          }
          visibles.forEach(function(f, i){
            var y = 32 + 24*i;
            s += '<rect x="16" y="'+y+'" width="608" height="22" fill="var(--surface-2)"></rect>';
            s += '<rect x="16" y="'+y+'" width="3" height="22" fill="'+f.c+'"></rect>';
            s += texto(24, y+15, f.tag, {s:9.5, c:f.c, p:1});
            s += texto(134, y+15, escapa(f.txt), {s:12, f:1});
          });

          var t1 = r.todo, t2 = r.salto;
          var bien = r.titulos === r.cabec;
          s += '<rect x="16" y="282" width="300" height="104" fill="var(--surface-2)" '
             + 'stroke="var(--line)" stroke-width="1"></rect>';
          s += texto(32, 306, 'ESCUCH\\u00c1NDOLO TODO SEGUIDO', {s:10, p:1});
          s += texto(32, 344, seg(t1), {s:28, p:1, f:1, c:'var(--ink)'});
          s += texto(32, 366, r.descritas + ' de ' + r.imgs + ' im\\u00e1genes descritas  \\u00b7  a '
                   + VEL + ' pal/min', {s:10.5});

          s += '<rect x="324" y="282" width="300" height="104" fill="var(--surface-2)" '
             + 'stroke="var(--line)" stroke-width="1"></rect>';
          s += texto(340, 306, 'SALTANDO DE T\\u00cdTULO EN T\\u00cdTULO', {s:10, p:1});
          s += texto(340, 344, r.titulos + ' de ' + r.cabec,
                     {s:28, p:1, f:1, c: bien ? 'var(--goo-verde)' : 'var(--goo-rojo)'});
          s += texto(340, 366, 'apartados a los que llega'
                   + (r.saltos ? '  \\u00b7  ' + seg(t2) : ''), {s:10.5});

          svg.innerHTML = s;

          var t = 'La p&aacute;gina es la <b>misma</b> en los dos modos: las mismas palabras, las '
                + 'mismas dos im&aacute;genes, los mismos cuatro apartados. Lo &uacute;nico que '
                + 'cambia es si los t&iacute;tulos est&aacute;n <b>marcados</b> como t&iacute;tulos '
                + 'o solo <b>pintados</b> en grande, y si las im&aacute;genes llevan escrito qu&eacute; '
                + 'se ve en ellas. ';
          if(modo === 'pintado'){
            t += 'As&iacute; como est&aacute;, quien no ve la pantalla tiene que tragarse '
               + '<b>' + seg(t1) + '</b> enteros para llegar al final, y las dos im&aacute;genes '
               + 'son <b>dos agujeros</b>: el lector solo puede deletrear el nombre del fichero.';
          } else {
            t += 'Marcada de verdad, los mismos apartados est&aacute;n a <b>' + r.saltos
               + ' pulsaciones</b> de distancia, y las im&aacute;genes <b>dicen lo que '
               + 'ense&ntilde;an</b>. F&iacute;jate en un detalle honrado: escucharla entera '
               + 'ahora cuesta <b>un poco m&aacute;s</b>, porque describir las im&aacute;genes '
               + 'lleva su tiempo. Lo que cambia no es eso: es que <b>ya no hace falta '
               + 'escucharla entera</b>.';
          }
          t += '<br><span style="font-size:12.5px">Los segundos salen de contar las palabras de '
             + 'cada bloque y dividir por ' + VEL + ' palabras por minuto, que es una velocidad de '
             + 'locuci&oacute;n c&oacute;moda; quien usa un lector de pantalla a diario lo pone '
             + 'much&iacute;simo m&aacute;s r&aacute;pido. Lo que no cambia con la velocidad es '
             + 'que <b>sin encabezados no hay nada a lo que saltar</b>. Y ojo: esto es '
             + 'exactamente lo mismo que ya viste con el &iacute;ndice autom&aacute;tico en la '
             + 'primera sesi&oacute;n.</span>';
          pie.innerHTML = t;
        }

        function marca(caja, attr, valor){
          caja.querySelectorAll('button['+attr+']').forEach(function(b){
            b.setAttribute('aria-pressed',
              b.getAttribute(attr) === String(valor) ? 'true' : 'false');
          });
        }
        var cajaM = document.getElementById('seg-lec-m');
        var cajaV = document.getElementById('seg-lec-v');
        cajaM.addEventListener('click', function(e){
          var b = e.target.closest('button[data-m]'); if(!b) return;
          modo = b.dataset.m; marca(cajaM, 'data-m', modo); pinta();
        });
        cajaV.addEventListener('click', function(e){
          var b = e.target.closest('button[data-v]'); if(!b) return;
          vista = b.dataset.v; marca(cajaV, 'data-v', vista); pinta();
        });

        pinta();
      })();
      </script>
'''


# ===========================================================================
# S6 · Si se lee, y cuanto
#
# Lienzo 640 x 320.
#   Muestra                 y 16..146 (x 16..624), pintada con los dos colores
#     titular  y = 62  (26 px)   ·   parrafo y = 98 (17 px)   ·   pie y = 128 (12 px)
#   Cifra y veredictos      y 160..232
#     razon   x  24 (34 px)   ·   tres sellos de 132 px en x = 226, 366 y 506
#   Regla de 1 a 21         y 252..300
#     barra x 24..600 (576 px): la razon r se coloca en 24 + (r-1)/20*576, asi
#     que 1:1 cae en x = 24 y 21:1 en x = 600. Marcas en 3, 4,5 y 7.
#
# La razon de contraste es la de la norma WCAG 2, con su formula exacta:
#   lineal(c) = c/12,92 si c <= 0,03928, y ((c+0,055)/1,055)^2,4 si no
#   L = 0,2126 R + 0,7152 G + 0,0722 B
#   razon = (L_claro + 0,05) / (L_oscuro + 0,05)
# El numero que sale aqui es comprobable contra cualquier otra herramienta.
# ===========================================================================
ESCENA_CONTRASTE = u'''
      <div class="escena" id="esc-contraste">
        <div class="escena-barra">
          <span class="escena-titulo">Los dos colores</span>
          <div class="seg" id="seg-con-c">
            <label style="display:flex;align-items:center;gap:6px;font:400 12px var(--f-m);
                          color:var(--ink-soft)">Letra
              <input type="color" id="con-txt" value="#9aa0a6" aria-label="Color de la letra"
                     style="width:38px;height:28px;padding:0;border:1.5px solid var(--line);
                            border-radius:2px;background:var(--surface);cursor:pointer"></label>
            <label style="display:flex;align-items:center;gap:6px;font:400 12px var(--f-m);
                          color:var(--ink-soft)">Fondo
              <input type="color" id="con-fon" value="#ffffff" aria-label="Color del fondo"
                     style="width:38px;height:28px;padding:0;border:1.5px solid var(--line);
                            border-radius:2px;background:var(--surface);cursor:pointer"></label>
            <button type="button" id="con-gira">&#8646; Cambiarlos de sitio</button>
          </div>
        </div>
        <div class="escena-barra">
          <span class="escena-titulo">O prueba estos</span>
          <div class="seg" id="seg-con-p">
            <button type="button" data-t="#9aa0a6" data-f="#ffffff" aria-pressed="true">El gris de siempre</button>
            <button type="button" data-t="#202124" data-f="#ffffff">Negro sobre blanco</button>
            <button type="button" data-t="#ffffff" data-f="#4285f4">Blanco sobre azul claro</button>
            <button type="button" data-t="#ffffff" data-f="#1a73e8">Blanco sobre azul oscuro</button>
            <button type="button" data-t="#fbbc04" data-f="#ffffff">Amarillo sobre blanco</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 320" id="svg-contraste" role="img"
               aria-label="Muestra de texto con los dos colores elegidos y la raz&oacute;n de contraste que sale de la norma"></svg>
        </div>
        <div class="pie" id="pie-contraste"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-contraste');
        if(!svg) return;
        var pie = document.getElementById('pie-contraste');
        var inTxt = document.getElementById('con-txt');
        var inFon = document.getElementById('con-fon');

        /* ---- la formula de la norma, tal cual ---- */
        function lineal(c){
          c = c / 255;
          return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
        }
        function luminancia(hex){
          var r = parseInt(hex.substr(1, 2), 16),
              g = parseInt(hex.substr(3, 2), 16),
              b = parseInt(hex.substr(5, 2), 16);
          return 0.2126*lineal(r) + 0.7152*lineal(g) + 0.0722*lineal(b);
        }
        function razon(a, b){
          var la = luminancia(a), lb = luminancia(b);
          var claro = Math.max(la, lb), oscuro = Math.min(la, lb);
          return (claro + 0.05) / (oscuro + 0.05);
        }

        function texto(x, y, t, op){
          op = op || {};
          return '<text x="'+x+'" y="'+y+'" class="rotulo-svg" style="font-size:'+(op.s || 11)
               + 'px'+(op.c ? ';fill:'+op.c : '')+(op.p ? ';font-weight:500' : '')
               + (op.a ? ';text-anchor:'+op.a : '')+(op.f ? ';font-family:var(--f-b)' : '')
               + ';letter-spacing:0">'+t+'</text>';
        }
        function num(v){ return v.toFixed(2).replace('.', ','); }

        function sello(x, y, rotulo, vale, umbral){
          var col = vale ? 'var(--goo-verde)' : 'var(--goo-rojo)';
          var s = '<rect x="'+x+'" y="'+y+'" width="132" height="46" fill="none" stroke="'+col
                + '" stroke-width="1.8"></rect>';
          s += texto(x+10, y+18, rotulo, {s:9.5, p:1});
          s += texto(x+10, y+36, (vale ? '\\u2713 pasa' : '\\u2717 no pasa') + '  (' + umbral + ')',
                     {s:12, p:1, c:col, f:1});
          return s;
        }

        function pinta(){
          var ct = inTxt.value, cf = inFon.value;
          var r = razon(ct, cf);
          var s = '';

          /* la muestra, pintada de verdad con los dos colores */
          s += '<rect x="16" y="16" width="608" height="130" fill="'+cf
             + '" stroke="var(--line)" stroke-width="1"></rect>';
          s += '<text x="40" y="62" style="font-family:var(--f-b);font-size:26px;font-weight:700;'
             + 'fill:'+ct+'">Lo que aguant\\u00f3 el puente</text>';
          s += '<text x="40" y="98" style="font-family:var(--f-b);font-size:17px;fill:'+ct+'">'
             + 'Rompi\\u00f3 con 1.400 gramos, por la diagonal de la derecha.</text>';
          s += '<text x="40" y="128" style="font-family:var(--f-m);font-size:12px;fill:'+ct+'">'
             + 'Y esto es el pie de foto, que siempre va m\\u00e1s peque\\u00f1o.</text>';

          s += texto(24, 190, num(r) + ' : 1', {s:34, p:1, f:1});
          s += texto(24, 212, 'RAZ\\u00d3N DE CONTRASTE', {s:10, p:1});
          s += texto(24, 228, ct.toUpperCase() + '  sobre  ' + cf.toUpperCase(), {s:10});

          s += sello(226, 160, 'TEXTO NORMAL', r >= 4.5, '4,5 : 1');
          s += sello(366, 160, 'TEXTO GRANDE', r >= 3,   '3 : 1');
          s += sello(506, 160, 'EXIGENTE (AAA)', r >= 7, '7 : 1');

          /* la regla, de 1 a 21 */
          s += '<rect x="24" y="266" width="576" height="10" fill="var(--surface-2)"></rect>';
          [[3, '3'], [4.5, '4,5'], [7, '7']].forEach(function(m){
            var x = 24 + (m[0] - 1)/20*576;
            s += '<path d="M'+x.toFixed(1)+' 262 v18" stroke="var(--line)" '
               + 'stroke-width="1.5"></path>';
            s += texto(x, 296, m[1], {s:9.5, a:'middle'});
          });
          var xr = 24 + (Math.min(r, 21) - 1)/20*576;
          s += '<path d="M'+xr.toFixed(1)+' 252 l-6 -10 h12 Z" fill="'
             + (r >= 4.5 ? 'var(--goo-verde)' : 'var(--goo-rojo)')+'"></path>';
          s += '<path d="M'+xr.toFixed(1)+' 252 v32" stroke="'
             + (r >= 4.5 ? 'var(--goo-verde)' : 'var(--goo-rojo)')+'" stroke-width="2"></path>';
          s += texto(24, 248, '1 : 1', {s:9.5});
          s += texto(600, 248, '21 : 1', {s:9.5, a:'end'});

          svg.innerHTML = s;

          var t = 'La cifra <b>' + num(r) + ' : 1</b> no es una opini&oacute;n ni una '
                + 'aproximaci&oacute;n: sale de la f&oacute;rmula de la norma internacional de '
                + 'accesibilidad. Se calcula el <b>brillo</b> de cada color &mdash;el verde pesa '
                + 'mucho m&aacute;s que el azul, porque el ojo lo ve mucho mejor&mdash; y se '
                + 'dividen los dos, sumando 0,05 a cada uno para que el negro puro no rompa la '
                + 'divisi&oacute;n. ';
          if(r >= 7){
            t += 'Con este par de colores lee cualquiera, tambi&eacute;n con poca luz o con una '
               + 'pantalla mala.';
          } else if(r >= 4.5){
            t += 'Vale para todo, aunque no va sobrado: prueba a bajarlo un poco y mira '
               + 'd&oacute;nde deja de pasar.';
          } else if(r >= 3){
            t += 'Ojo: vale para un <b>titular</b> grande, pero <b>no</b> para el texto normal '
               + 'ni para el pie de foto. Mira la muestra de arriba: la l&iacute;nea peque&ntilde;a '
               + 'ya cuesta.';
          } else {
            t += 'Esto no lo lee nadie que no tenga la vista perfecta, buena luz y una pantalla '
               + 'buena. Y encima el que lo elige casi nunca es el que no puede leerlo.';
          }
          t += '<br><span style="font-size:12.5px">&laquo;Texto grande&raquo; quiere decir a '
             + 'partir de <b>18 puntos</b>, o de 14 en negrita. Los umbrales &mdash;4,5 y '
             + '3&mdash; son los de la norma <b>WCAG 2</b>, que es la que citan las leyes de '
             + 'accesibilidad; el de 7 es su nivel m&aacute;s exigente. Lo que la norma '
             + '<b>no</b> mira es el color en s&iacute;: dos colores distintos con el mismo '
             + 'brillo dan 1 : 1 y son ilegibles aunque uno sea rojo y el otro verde.</span>';
          pie.innerHTML = t;
        }

        function marcaPreset(){
          document.querySelectorAll('#seg-con-p button').forEach(function(b){
            b.setAttribute('aria-pressed',
              (b.dataset.t === inTxt.value && b.dataset.f === inFon.value) ? 'true' : 'false');
          });
        }
        function actualiza(){ marcaPreset(); pinta(); }

        inTxt.addEventListener('input', actualiza);
        inFon.addEventListener('input', actualiza);
        document.getElementById('seg-con-p').addEventListener('click', function(e){
          var b = e.target.closest('button[data-t]'); if(!b) return;
          inTxt.value = b.dataset.t; inFon.value = b.dataset.f; actualiza();
        });
        document.getElementById('con-gira').addEventListener('click', function(){
          var a = inTxt.value; inTxt.value = inFon.value; inFon.value = a; actualiza();
        });

        actualiza();
      })();
      </script>
'''
