# -*- coding: utf-8 -*-
"""Las escenas interactivas de las sesiones 4, 5 y 6 de la U8.

Mismo criterio que u8_escenas.py: SVG y JavaScript a mano, sin librerias, y
todas CALCULAN. Ninguna lleva dentro una tabla de resultados escrita a mano.

  ESCENA_FUERZA    S4 · cuanto aguanta una contrasena. El numero de
                   combinaciones sale de alfabeto^longitud y el tiempo se
                   calcula EN LOGARITMOS, porque 2^128 no cabe en un double.
  ESCENA_HASH      S4 · lo que la web guarda de verdad. Lleva un SHA-256
                   escrito entero aqui dentro: el hash que sale es el de
                   verdad, comprobable contra cualquier otra herramienta.
  ESCENA_NUBE      S5 · simulacion de sitios donde vive un archivo. El que
                   sobrevive a cada desastre sale de aplicar las reglas al
                   estado, no de una tabla de casos; y la regla 3-2-1 se
                   evalua contando.
  ESCENA_DERECHOS  S6 · el plazo legal de respuesta y la edad para consentir,
                   calculados sobre el calendario de verdad (con el arrastre
                   de fin de mes, que es donde falla todo el mundo).

Geometria: cada escena dice arriba de que tamano es su lienzo y como se
reparte. Nada esta puesto a ojo.

Las cadenas de JS llevan \\uXXXX y no entidades HTML: una entidad HTML dentro
de una cadena de JavaScript se dibuja como seis caracteres y descuadra el ancho.
"""

# ---------------------------------------------------------------------------
# S4 · Cuanto aguanta una contrasena
#
# Lienzo 640 x 400.
#   Panel del analisis      x  16..624   y  32..136
#   Panel de "y si le anades" x 16..624  y 148..240
#       cuatro cajas de 140 px en x = 32, 180, 328, 476. La cifra y la unidad
#       van en DOS lineas: "802,2 millones de anos" son 22 caracteres y a 12 px
#       gasta 7,92 px cada uno -> 174 px, que no caben en 140.
#   Barras comparativas     y 268..392
#       rotulo  x  24..238   ·  barra  x 246..546  ·  cifra x 554..624
#       Escala: 140 bits = 300 px -> 2,143 px por bit. El ejemplo mas largo
#       (la B del reto) da 114,1 bits = 245 px, asi que no se sale.
#
# Anchos de texto comprobados contra el ancho util (592 px) con el gasto real
# de Roboto Mono en .rotulo-svg, que lleva letter-spacing .06em: cada caracter
# ocupa 0,66 veces el tamano de letra. A 12,5 px caben 71 caracteres; a 11,5,
# 78. Por eso el recuento y la lista de familias van en dos lineas separadas.
#
# La cuenta: combinaciones = alfabeto^longitud, y el tiempo medio es la mitad
# del espacio dividido por los intentos por segundo. 2^128 no cabe en un
# numero de JavaScript, asi que TODO se hace en logaritmos decimales y solo se
# convierte a numero al final, cuando ya se sabe que cabe.
#
# Los tres ritmos son ordenes de magnitud NUESTROS, no medidas, y va dicho en
# el pie. Lo que no depende del ritmo -y es lo que ensena la escena- es que
# anadir un caracter multiplica por el tamano del alfabeto.
# ---------------------------------------------------------------------------
ESCENA_FUERZA = u'''
      <div class="escena" id="esc-fuerza">
        <div class="escena-barra">
          <span class="escena-titulo">Cu&aacute;nto aguanta</span>
          <div class="seg" id="seg-fuerza">
            <button type="button" data-r="1e2">Prob&aacute;ndola en la web</button>
            <button type="button" data-r="1e5" aria-pressed="true">Con la lista robada</button>
            <button type="button" data-r="1e11">&hellip;y mal guardada</button>
          </div>
        </div>
        <div class="escena-barra">
          <span class="escena-titulo">Escribe una y mira</span>
          <div class="seg">
            <label style="font:400 12px var(--f-m);color:var(--ink-soft)">
              <input id="fz-txt" type="text" value="Ab3$x!Qz" maxlength="40"
                     style="font:400 12px var(--f-m);padding:5px 7px;border:1.5px solid var(--line);
                            border-radius:2px;background:var(--surface);color:var(--ink);width:250px">
            </label>
            <button type="button" data-f="frase">Pon una frase</button>
            <button type="button" data-f="corta">Pon una rara y corta</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 400" id="svg-fuerza" role="img"
               aria-label="C&aacute;lculo de cu&aacute;ntas combinaciones tiene una contrase&ntilde;a y cu&aacute;nto se tarda en probarlas todas"></svg>
        </div>
        <div class="pie" id="pie-fuerza"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-fuerza');
        if(!svg) return;
        var pie = document.getElementById('pie-fuerza');
        var seg = document.getElementById('seg-fuerza');
        var inp = document.getElementById('fz-txt');

        /* Cuantos simbolos distintos podria haber en cada sitio. Es una
           estimacion nuestra del "alfabeto", y va dicha en el pie. */
        var FAMILIAS = [
          {re:/[a-z]/,                n:26, etq:'min\\u00fasculas'},
          {re:/[A-Z]/,                n:26, etq:'MAY\\u00daSCULAS'},
          {re:/[0-9]/,                n:10, etq:'n\\u00fameros'},
          {re:/ /,                    n: 1, etq:'espacio'},
          {re:/[\\u00e1\\u00e9\\u00ed\\u00f3\\u00fa\\u00fc\\u00f1\\u00c1\\u00c9\\u00cd\\u00d3\\u00da\\u00dc\\u00d1]/,
                                      n:14, etq:'tildes y \\u00f1'},
          {re:/[^a-zA-Z0-9 \\u00e1\\u00e9\\u00ed\\u00f3\\u00fa\\u00fc\\u00f1\\u00c1\\u00c9\\u00cd\\u00d3\\u00da\\u00dc\\u00d1]/,
                                      n:32, etq:'signos'}
        ];

        var RITMOS = {
          '1e2' : {v:1e2,  etq:'100 por segundo',
                   nota:'prob\\u00e1ndola en la propia web, que te corta a los pocos fallos'},
          '1e5' : {v:1e5,  etq:'100.000 por segundo',
                   nota:'con la lista robada, si la web la guard\\u00f3 como hay que guardarla'},
          '1e11': {v:1e11, etq:'100.000 millones por segundo',
                   nota:'con la lista robada, si la web la guard\\u00f3 de cualquier manera'}
        };
        var ritmo = '1e5';

        /* Ejemplos fijos. La cuenta de los cuatro sale de las MISMAS funciones
           que la de lo que escribe el alumno: aqui no hay ningun numero a mano.
           "pega" no es un calculo, es un aviso nuestro sobre ese ejemplo.
           El ultimo es la contrasena B del reto, a proposito: asi el numero que
           sale en el pie es el mismo que han calculado a mano. */
        var EJEMPLOS = [
          {t:'Rt7!q',      nota:'cinco caracteres, muy rara'},
          {t:'Pelusa2012',  nota:'un nombre y un a\\u00f1o',
           pega:'no es al azar: eso lo prueba cualquiera de los primeros'},
          {t:'zanahoriaverde', nota:'catorce min\\u00fasculas'},
          {t:'tres cabras en el tejado', nota:'la B del reto, 24 caracteres'}
        ];

        var L2 = Math.log(2) / Math.log(10);     /* log10(2) */

        function alfabeto(s){
          var n = 0, ets = [];
          for(var i = 0; i < FAMILIAS.length; i++)
            if(FAMILIAS[i].re.test(s)){ n += FAMILIAS[i].n; ets.push(FAMILIAS[i].etq); }
          return {n:n, etq:ets.join(' + ')};
        }
        /* bits = longitud x log2(alfabeto). Se cuenta por CODIGOS, no por
           bytes: una "\\u00f1" es un sitio, no dos. */
        function bits(s){
          var a = alfabeto(s);
          if(!a.n || !s.length) return 0;
          return s.length * Math.log(a.n) / Math.log(2);
        }
        /* log10 de los segundos que se tarda de media: la mitad del espacio
           entre los intentos por segundo. En logaritmos, para que no se
           desborde: 2^128 no cabe en un numero de JavaScript. */
        function logSeg(b, r){ return b * L2 - L2 - Math.log(r) / Math.log(10); }

        function coma(n, d){ return n.toFixed(d).replace('.', ','); }

        var UNI = [[1,'segundos'], [60,'minutos'], [3600,'horas'],
                   [86400,'d\\u00edas'], [31557600,'a\\u00f1os']];

        /* Devuelve la cifra y la unidad por separado, porque en las cajas
           estrechas de abajo van en dos lineas y no caben juntas. */
        function humanoP(ls){
          if(ls < 0) return {n:'menos de', u:'un segundo'};
          var i = 0, k;
          for(k = 0; k < UNI.length; k++)
            if(ls - Math.log(UNI[k][0]) / Math.log(10) >= 0) i = k;
          var l = ls - Math.log(UNI[i][0]) / Math.log(10);
          if(i === UNI.length - 1){
            if(l >= 9)  return {n:'10^' + Math.round(l), u:'a\\u00f1os'};
            if(l >= 6)  return {n:coma(Math.pow(10, l - 6), 1), u:'millones de a\\u00f1os'};
          }
          var v = Math.pow(10, l);
          return {n:(v < 10 ? coma(v, 1) : Math.round(v).toLocaleString('es-ES')),
                  u:UNI[i][1]};
        }
        function humano(ls){ var h = humanoP(ls); return h.n + ' ' + h.u; }

        function esc(s){
          return String(s).replace(/&/g,'&#38;').replace(/</g,'&#60;').replace(/>/g,'&#62;');
        }
        function corta(s, n){ return s.length > n ? s.slice(0, n - 1) + '\\u2026' : s; }

        function pinta(){
          var s = inp.value, a = alfabeto(s), b = bits(s), R = RITMOS[ritmo];
          var m = '', i;

          /* ---------------- panel 1: lo que has escrito ---------------- */
          m += '<rect x="16" y="32" width="608" height="104" rx="2" fill="var(--surface)" '
             + 'stroke="var(--goo-azul)" stroke-width="2"></rect>';
          m += '<text x="32" y="52" class="rotulo-svg" style="font-size:10px">LO QUE HAS '
             + 'ESCRITO</text>';

          if(!s.length){
            m += '<text x="32" y="86" class="rotulo-svg" style="font-size:14px;fill:var(--ink)">'
               + 'Escribe algo ah\\u00ed arriba.</text>';
          } else {
            /* dos lineas: el recuento cabe en una, la lista de familias no.
               A 11,5 px caben 78 caracteres en los 592 de ancho util. */
            m += '<text x="32" y="72" class="rotulo-svg" style="font-size:12.5px">'
               + s.length + ' caracteres  \\u00b7  en cada sitio cabe uno de ' + a.n + '</text>';
            m += '<text x="32" y="90" class="rotulo-svg" style="font-size:11.5px">'
               + esc(corta(a.etq, 76)) + '</text>';
            m += '<text x="32" y="114" class="rotulo-svg" '
               + 'style="font-size:15px;fill:var(--ink);font-weight:500">'
               + 'Hay 1 entre 10^' + Math.round(b * L2)
               + '   \\u00b7   ' + coma(b, 1) + ' bits</text>';
            m += '<text x="32" y="130" class="rotulo-svg" style="font-size:12px;'
               + 'fill:var(--goo-azul)">A ' + R.etq + ' se tarda de media: '
               + humano(logSeg(b, R.v)) + '</text>';
          }

          /* ------- panel 2: lo que pasa por anadir un caracter mas ------- */
          m += '<rect x="16" y="148" width="608" height="92" rx="2" fill="var(--surface-2)" '
             + 'stroke="var(--line)" stroke-width="1.5"></rect>';
          m += '<text x="32" y="168" class="rotulo-svg" style="font-size:10px">Y SI LE A\\u00d1ADES '
             + 'CARACTERES DE LOS QUE YA LLEVA (sin poner nada raro)</text>';
          for(i = 0; i < 4; i++){
            var L = s.length + i;
            var bb = a.n ? L * Math.log(a.n) / Math.log(2) : 0;
            var x = 32 + i * 148, h = humanoP(logSeg(bb, R.v));
            m += '<rect x="' + x + '" y="180" width="140" height="50" rx="2" fill="var(--surface)" '
               + 'stroke="' + (i ? 'var(--line)' : 'var(--goo-azul)') + '" stroke-width="1.5"></rect>';
            m += '<text x="' + (x + 70) + '" y="196" text-anchor="middle" class="rotulo-svg" '
               + 'style="font-size:9.5px">' + L + ' caracteres'
               + (i ? '' : '  (la tuya)') + '</text>';
            m += '<text x="' + (x + 70) + '" y="213" text-anchor="middle" class="rotulo-svg" '
               + 'style="font-size:13.5px;fill:' + (i ? 'var(--ink)' : 'var(--goo-azul)')
               + ';font-weight:500">' + h.n + '</text>';
            m += '<text x="' + (x + 70) + '" y="226" text-anchor="middle" class="rotulo-svg" '
               + 'style="font-size:9.5px">' + h.u + '</text>';
          }

          /* ---------------- panel 3: barras comparativas ---------------- */
          m += '<text x="24" y="268" class="rotulo-svg" style="font-size:10px">LO TUYO, AL LADO '
             + 'DE OTRAS  \\u00b7  cada barra es lo grande que es el mont\\u00f3n</text>';
          var FILAS = [{t:s, nota:'lo que has escrito', mia:1}].concat(EJEMPLOS);
          for(i = 0; i < FILAS.length; i++){
            var F = FILAS[i], y = 288 + i * 24, fb = bits(F.t);
            var ancho = Math.max(0, Math.min(300, fb / 140 * 300));
            var color = F.mia ? 'var(--goo-azul)' : (F.pega ? 'var(--goo-rojo)' : 'var(--ink-soft)');
            m += '<text x="24" y="' + y + '" class="rotulo-svg" style="font-size:11px;fill:'
               + (F.mia ? 'var(--goo-azul)' : 'var(--ink-soft)') + '">'
               + esc(corta(F.t || '(nada)', 26)) + '</text>';
            m += '<rect x="246" y="' + (y - 11) + '" width="' + ancho.toFixed(1) + '" height="14" '
               + 'rx="1" fill="' + color + '" opacity="' + (F.mia ? '.9' : '.6') + '"></rect>';
            m += '<text x="554" y="' + y + '" class="rotulo-svg" style="font-size:11px">'
               + coma(fb, 1) + ' bits</text>';
            if(F.pega)
              m += '<text x="' + (250 + ancho) + '" y="' + y + '" class="rotulo-svg" '
                 + 'style="font-size:10px;fill:var(--goo-rojo)">  \\u2190 ojo</text>';
          }

          svg.innerHTML = m;

          /* ------------------------- el pie ------------------------- */
          /* Las dos del reto, calculadas aqui igual que todo lo demas. El
             exponente va con floor y se dice "mas de": redondeando a 19 no
             cuadraria con las dieciocho cifras que han contado a mano. */
          var bA = bits('Ab3$x!Qz'), bB = bits('tres cabras en el tejado');
          pie.innerHTML =
              'Ritmo elegido: <b>' + R.etq + '</b> \\u2014 ' + R.nota + '. '
            + 'Cambia de ritmo y f&iacute;jate en una cosa: <b>cambian todos los tiempos, pero no '
            + 'cambia qui&eacute;n gana</b>. Las barras son las mismas.'
            + '<br>Las dos del reto: la <b>A</b> tiene ' + coma(bA, 1) + ' bits y la <b>B</b> '
            + coma(bB, 1) + '. Esos <b>' + Math.round(bB - bA) + ' bits de diferencia</b> son '
            + 'm&aacute;s de <b>10<sup>' + Math.floor((bB - bA) * L2) + '</sup> veces</b> m&aacute;s '
            + 'mont&oacute;n. Y la B te la acuerdas.'
            + '<br><span style="font-size:12.5px">Las cuentas son de verdad: combinaciones = '
            + '<b>alfabeto elevado a la longitud</b>, y el tiempo es la mitad de eso entre los '
            + 'intentos por segundo. Dos avisos honrados: los <b>tres ritmos son &oacute;rdenes de '
            + 'magnitud nuestros</b>, no medidas; y la cuenta <b>solo vale si la contrase&ntilde;a '
            + 'es al azar</b>. Si es tu nombre, tu equipo o tu fecha de nacimiento, no hay ese '
            + 'mont&oacute;n: hay un pu&ntilde;ado, porque son las primeras que se prueban. Por eso '
            + '<i>Pelusa2012</i> sale con barra larga y aun as&iacute; va marcada en rojo.</span>';
        }

        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-r]'); if(!b) return;
          ritmo = b.dataset.r;
          seg.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
          pinta();
        });
        document.querySelectorAll('#esc-fuerza button[data-f]').forEach(function(b){
          b.addEventListener('click', function(){
            inp.value = (b.dataset.f === 'frase')
              ? 'tres cabras en el tejado' : 'X7$k!2Qz';
            pinta();
          });
        });
        inp.addEventListener('input', pinta);
        pinta();
      })();
      </script>
'''


# ---------------------------------------------------------------------------
# S4 · Lo que la web guarda de verdad
#
# Lienzo 640 x 348.
#   Panel A  "lo que se guarda de ti"      x 16..624   y  32..146
#   Panel B  "y de otra persona igual"     x 16..624   y 158..254
#   Panel C  "cambia una letra"            x 16..624   y 266..340
#
#   El hash se parte en dos lineas de 32 cifras. Roboto Mono a 13 px con el
#   letter-spacing de .rotulo-svg (0,06 em) gasta 13*0,66 = 8,58 px por
#   caracter: 32 x 8,58 = 275 px, y hay 592 de sitio. Cabe de sobra.
#
# El SHA-256 esta escrito entero aqui abajo y es el de verdad: el hash que
# sale se puede comprobar contra cualquier otra herramienta. Las constantes no
# estan copiadas de ningun sitio, son las que manda la norma (los 32 bits
# decimales de las raices cuadradas de los 8 primeros primos y de las raices
# cubicas de los 64 primeros) y el verificador comprueba el vector oficial
# sha256("abc") = ba7816bf...15ad antes de dar la escena por buena.
#
# Las "sales" son dos cadenas fijas que hacen de ejemplo. En una web de verdad
# cada usuario lleva la suya, sacada al azar el dia que se registra.
# ---------------------------------------------------------------------------
ESCENA_HASH = u'''
      <div class="escena" id="esc-hash">
        <div class="escena-barra">
          <span class="escena-titulo">Lo que la web guarda de ti</span>
          <div class="seg" id="seg-hash">
            <button type="button" data-s="no" aria-pressed="true">Sin sal</button>
            <button type="button" data-s="si">Con sal</button>
          </div>
        </div>
        <div class="escena-barra">
          <span class="escena-titulo">Tu contrase&ntilde;a</span>
          <div class="seg">
            <label style="font:400 12px var(--f-m);color:var(--ink-soft)">
              <input id="hs-txt" type="text" value="tres cabras" maxlength="32"
                     style="font:400 12px var(--f-m);padding:5px 7px;border:1.5px solid var(--line);
                            border-radius:2px;background:var(--surface);color:var(--ink);width:230px">
            </label>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 348" id="svg-hash" role="img"
               aria-label="La huella sha-256 de una contrase&ntilde;a, la de otra persona con la misma contrase&ntilde;a y la de la misma cambiando una letra"></svg>
        </div>
        <div class="pie" id="pie-hash"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-hash');
        if(!svg) return;
        var pie = document.getElementById('pie-hash');
        var seg = document.getElementById('seg-hash');
        var inp = document.getElementById('hs-txt');

        /* ---------------------- SHA-256, entero ---------------------- */
        var H0 = [
          0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
          0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19];
        var K = [
          0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
          0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
          0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
          0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
          0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
          0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
          0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
          0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
          0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
          0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
          0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
          0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
          0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
          0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
          0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
          0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2];

        function rotr(x, n){ return ((x >>> n) | (x << (32 - n))) >>> 0; }

        function bytes(s){
          if(window.TextEncoder) return Array.from(new TextEncoder().encode(s));
          var r = [], e = unescape(encodeURIComponent(s));
          for(var i = 0; i < e.length; i++) r.push(e.charCodeAt(i));
          return r;
        }

        function sha256(texto){
          var msg = bytes(texto), bitLen = msg.length * 8;
          var b = msg.slice();
          b.push(0x80);
          while(b.length % 64 !== 56) b.push(0);
          /* los 64 bits de la longitud, en big-endian. Con textos de esta
             escena la parte alta es siempre cero, pero se escribe igual. */
          b.push(0, 0, 0, 0,
                 (bitLen >>> 24) & 255, (bitLen >>> 16) & 255,
                 (bitLen >>> 8) & 255, bitLen & 255);

          var H = H0.slice(), w = new Array(64), i, t;
          for(i = 0; i < b.length; i += 64){
            for(t = 0; t < 16; t++)
              w[t] = ((b[i+t*4] << 24) | (b[i+t*4+1] << 16)
                    | (b[i+t*4+2] << 8) | b[i+t*4+3]) >>> 0;
            for(t = 16; t < 64; t++){
              var x = w[t-15], y = w[t-2];
              var s0 = (rotr(x, 7) ^ rotr(x, 18) ^ (x >>> 3)) >>> 0;
              var s1 = (rotr(y, 17) ^ rotr(y, 19) ^ (y >>> 10)) >>> 0;
              w[t] = (w[t-16] + s0 + w[t-7] + s1) >>> 0;
            }
            var a = H[0], bb = H[1], c = H[2], d = H[3],
                e = H[4], f = H[5], g = H[6], h = H[7];
            for(t = 0; t < 64; t++){
              var S1 = (rotr(e, 6) ^ rotr(e, 11) ^ rotr(e, 25)) >>> 0;
              var ch = ((e & f) ^ (~e & g)) >>> 0;
              var t1 = (h + S1 + ch + K[t] + w[t]) >>> 0;
              var S0 = (rotr(a, 2) ^ rotr(a, 13) ^ rotr(a, 22)) >>> 0;
              var mj = ((a & bb) ^ (a & c) ^ (bb & c)) >>> 0;
              var t2 = (S0 + mj) >>> 0;
              h = g; g = f; f = e; e = (d + t1) >>> 0;
              d = c; c = bb; bb = a; a = (t1 + t2) >>> 0;
            }
            var nu = [a, bb, c, d, e, f, g, h];
            for(t = 0; t < 8; t++) H[t] = (H[t] + nu[t]) >>> 0;
          }
          return H.map(function(v){ return ('0000000' + v.toString(16)).slice(-8); }).join('');
        }
        window.__sha256 = sha256;      /* lo usa el verificador */

        /* Dos sales de ejemplo. En una web de verdad cada usuario lleva la
           suya, sacada al azar el dia que se registra. */
        var SAL_A = 'a9f3c1d0', SAL_B = '5e20b7aa';
        var conSal = false;

        function cambiaUna(s){
          if(!s.length) return s;
          var c = s[0], n = (c === 'a') ? 'b' : (c === 'A' ? 'B' : 'a');
          return n + s.slice(1);
        }
        function distintas(x, y){
          var n = 0;
          for(var i = 0; i < x.length; i++) if(x[i] !== y[i]) n++;
          return n;
        }
        function esc(s){
          return String(s).replace(/&/g,'&#38;').replace(/</g,'&#60;').replace(/>/g,'&#62;');
        }

        function dosLineas(m, h, x, y){
          m += '<text x="' + x + '" y="' + y + '" class="rotulo-svg" '
             + 'style="font-size:13px;fill:var(--ink)">' + h.slice(0, 32) + '</text>';
          m += '<text x="' + x + '" y="' + (y + 18) + '" class="rotulo-svg" '
             + 'style="font-size:13px;fill:var(--ink)">' + h.slice(32) + '</text>';
          return m;
        }

        function pinta(){
          var s = inp.value;
          var hA = sha256(conSal ? SAL_A + s : s);
          var hB = sha256(conSal ? SAL_B + s : s);
          var hC = sha256(conSal ? SAL_A + cambiaUna(s) : cambiaUna(s));
          var iguales = (hA === hB);
          var m = '';

          /* ---------------- panel A: lo tuyo ---------------- */
          m += '<rect x="16" y="32" width="608" height="114" rx="2" fill="var(--surface)" '
             + 'stroke="var(--goo-azul)" stroke-width="2"></rect>';
          m += '<text x="32" y="52" class="rotulo-svg" style="font-size:10px">T\\u00da ESCRIBES'
             + (conSal ? ', Y LA WEB LE PEGA DELANTE TU SAL (' + SAL_A + ')' : '') + '</text>';
          m += '<text x="32" y="76" class="rotulo-svg" '
             + 'style="font-size:14px;fill:var(--goo-azul);font-weight:500">'
             + esc(conSal ? SAL_A + s : (s || '(nada)')) + '</text>';
          m += '<text x="32" y="98" class="rotulo-svg" style="font-size:10px">Y LO QUE SE GUARDA '
             + 'ES ESTO, QUE ES LO \\u00daNICO QUE SE GUARDA</text>';
          m = dosLineas(m, hA, 32, 118);

          /* ------------- panel B: otra persona igual ------------- */
          m += '<rect x="16" y="158" width="608" height="96" rx="2" fill="var(--surface)" '
             + 'stroke="' + (iguales ? 'var(--goo-rojo)' : 'var(--goo-verde)') + '" '
             + 'stroke-width="2"></rect>';
          m += '<text x="32" y="178" class="rotulo-svg" style="font-size:10px">OTRA PERSONA QUE HA '
             + 'PUESTO EXACTAMENTE LA MISMA CONTRASE\\u00d1A'
             + (conSal ? ' (su sal es ' + SAL_B + ')' : '') + '</text>';
          m = dosLineas(m, hB, 32, 202);
          /* A 12,5 px caben 71 caracteres en los 592 utiles: las dos frases
             estan medidas para no pasar de ahi. */
          m += '<text x="32" y="242" class="rotulo-svg" style="font-size:12.5px;fill:'
             + (iguales ? 'var(--goo-rojo)' : 'var(--goo-verde)') + ';font-weight:500">'
             + (iguales
                ? 'Le sale LA MISMA l\\u00ednea que a ti, y eso se ve en la lista.'
                : 'Le sale OTRA, con la misma contrase\\u00f1a. Eso es lo que hace la sal.')
             + '</text>';

          /* ------------- panel C: cambia una letra ------------- */
          var n = distintas(hA, hC);
          m += '<rect x="16" y="266" width="608" height="74" rx="2" fill="var(--surface-2)" '
             + 'stroke="var(--line)" stroke-width="1.5"></rect>';
          m += '<text x="32" y="286" class="rotulo-svg" style="font-size:10px">Y AHORA CAMBIA UNA '
             + 'SOLA LETRA, LA PRIMERA:  ' + esc(cambiaUna(s) || '(nada)') + '</text>';
          m += '<text x="32" y="308" class="rotulo-svg" style="font-size:13px;fill:var(--ink)">'
             + hC.slice(0, 32) + '</text>';
          m += '<text x="32" y="330" class="rotulo-svg" style="font-size:12px;fill:var(--goo-azul)">'
             + 'De las 64 cifras han cambiado ' + n + '. No se parecen en nada.</text>';

          svg.innerHTML = m;

          pie.innerHTML =
              'Esa l\\u00ednea de 64 cifras se llama <b>huella</b> (o <i>hash</i>), y tiene tres '
            + 'propiedades que son justo las que hacen falta: de la misma contrase&ntilde;a sale '
            + '<b>siempre la misma</b>, de una contrase&ntilde;a parecida sale una <b>completamente '
            + 'distinta</b>, y <b>de la huella no se puede volver</b> a la contrase&ntilde;a. Por eso '
            + 'una web bien hecha <b>no sabe cu&aacute;l es tu contrase&ntilde;a</b>: cuando entras, '
            + 'calcula la huella de lo que escribes y la compara con la que tiene guardada.'
            + '<br><span style="font-size:12.5px">Prueba a pulsar <b>con sal</b>: la misma '
            + 'contrase&ntilde;a deja de dar la misma l&iacute;nea en dos personas distintas. La sal es '
            + 'un trozo de texto al azar que la web le pega delante a cada usuario, y no es secreta: '
            + 'est&aacute; guardada al lado. No sirve para esconderla, sirve para que <b>dos listas no '
            + 'se puedan cruzar</b>. El SHA-256 de esta escena est&aacute; escrito entero en la '
            + 'p&aacute;gina y es el de verdad: si calculas el de la misma palabra en cualquier otra '
            + 'herramienta, sale exactamente lo mismo.</span>';
        }

        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-s]'); if(!b) return;
          conSal = (b.dataset.s === 'si');
          seg.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
          pinta();
        });
        inp.addEventListener('input', pinta);
        pinta();
      })();
      </script>
'''


# ---------------------------------------------------------------------------
# S5 · Donde vive un archivo, y que pasa cuando pasa algo
#
# Lienzo 640 x 430.
#   Cuatro sitios   x = 16, 172, 328, 484, de 140 px   y  44..176
#       (16+140=156, +16 de hueco = 172 ... el ultimo acaba en 624)
#   Panel del veredicto    x 16..624   y 192..284
#   Panel de la regla 3-2-1 x 16..624  y 296..420
#       cuatro contadores en x = 40, 188, 336, 484
#
# Esto NO es una tabla de casos. Cada sitio tiene estado y version, y cada
# desastre es una regla que se aplica a los sitios que cumplen una condicion:
#   borrar        -> al portatil y a TODO lo que este sincronizado con el
#   romper        -> al portatil
#   inundar       -> a todo lo que este en casa
#   perder cuenta -> a todo lo que este en la nube
# Quien sobrevive sale de mirar el estado despues, y la regla 3-2-1 de contar.
# Por eso sale solo la leccion de la sesion: se puede cumplir el 3-2-1 al pie
# de la letra y perderlo todo con un borrado, si las tres copias se sincronizan.
# ---------------------------------------------------------------------------
ESCENA_NUBE = u'''
      <div class="escena" id="esc-nube">
        <div class="escena-barra">
          <span class="escena-titulo">D&oacute;nde vive tu archivo</span>
          <div class="seg" id="seg-nube-que">
            <button type="button" data-q="nube" aria-pressed="true">La nube</button>
            <button type="button" data-q="disco">Disco en el caj&oacute;n</button>
            <button type="button" data-q="insti">Copia en el insti</button>
            <button type="button" data-q="dsync">El disco, sincronizado</button>
          </div>
        </div>
        <div class="escena-barra">
          <span class="escena-titulo">Y ahora pasa esto</span>
          <div class="seg" id="seg-nube-pasa">
            <button type="button" data-p="trabaja">Paso un d&iacute;a trabajando</button>
            <button type="button" data-p="copia">Hago la copia</button>
            <button type="button" data-p="borra">Lo borro sin querer</button>
            <button type="button" data-p="rompe">Se rompe el port&aacute;til</button>
            <button type="button" data-p="casa">Se inunda mi casa</button>
            <button type="button" data-p="cuenta">Pierdo la cuenta</button>
            <button type="button" data-p="reset">&#8635; Reiniciar</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 430" id="svg-nube" role="img"
               aria-label="Los sitios donde vive una copia de un archivo y cu&aacute;les sobreviven a cada desastre"></svg>
        </div>
        <div class="pie" id="pie-nube"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-nube');
        if(!svg) return;
        var pie = document.getElementById('pie-nube');

        var BASE = [
          {id:'port',  etq:'TU PORT\\u00c1TIL', sub:'donde trabajas',
           soporte:'el port\\u00e1til', sitio:'casa',  sync:1, fija:1},
          {id:'nube',  etq:'LA NUBE',          sub:'carpeta sincronizada',
           soporte:'la nube',          sitio:'fuera', sync:1},
          {id:'disco', etq:'DISCO EXTERNO',    sub:'en el caj\\u00f3n',
           soporte:'un disco',         sitio:'casa',  sync:0},
          {id:'insti', etq:'COPIA EN EL INSTI', sub:'otro disco',
           soporte:'un disco',         sitio:'fuera', sync:0}
        ];

        var act, E, dia, discoSync, ultimo;

        function reset(){
          act = {port:1, nube:1, disco:0, insti:0};
          discoSync = false;
          dia = 3;
          E = {};
          BASE.forEach(function(S){ E[S.id] = {estado:'bien', dia:dia}; });
          ultimo = '';
          marca();
        }
        /* El portatil es el original y se comporta como sincronizado: lo que le
           pasa a el lo copian los demas sincronizados. El disco externo puede
           estar sincronizado o no, y ese es el interruptor que importa. */
        function sincro(S){ return S.id === 'disco' ? discoSync : !!S.sync; }
        function puestos(){ return BASE.filter(function(S){ return act[S.id]; }); }

        function trabaja(){
          dia++;
          puestos().forEach(function(S){
            if(S.fija || sincro(S)){ E[S.id].estado = 'bien'; E[S.id].dia = dia; }
          });
          ultimo = 'Has trabajado un d\\u00eda m\\u00e1s. Lo que va sincronizado se ha puesto al d\\u00eda solo.';
        }
        function copia(){
          var n = 0;
          puestos().forEach(function(S){
            if(!S.fija && !sincro(S)){ E[S.id].estado = 'bien'; E[S.id].dia = dia; n++; }
          });
          ultimo = n ? ('Copia hecha en ' + n + ' sitio' + (n > 1 ? 's' : '') + '.')
                     : 'No tienes ning\\u00fan sitio donde hacerla que no vaya sincronizado.';
        }
        function rompe(cond, como, texto){
          puestos().forEach(function(S){ if(cond(S)) E[S.id].estado = como; });
          ultimo = texto;
        }

        function esc(s){
          return String(s).replace(/&/g,'&#38;').replace(/</g,'&#60;').replace(/>/g,'&#62;');
        }
        function caja(x, y, w, h, relleno, borde, grosor, guion){
          return '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" rx="2" '
               + 'fill="' + relleno + '" stroke="' + borde + '" stroke-width="' + grosor + '"'
               + (guion ? ' stroke-dasharray="5 4"' : '') + '></rect>';
        }

        var PALABRA = {bien:'est\\u00e1 ah\\u00ed', borrado:'BORRADO', roto:'NO LLEGAS'};
        var COLOR   = {bien:'var(--goo-verde)', borrado:'var(--goo-rojo)', roto:'var(--goo-rojo)'};

        function pinta(){
          var m = '', i;
          var hay = puestos();
          var vivos = hay.filter(function(S){ return E[S.id].estado === 'bien'; });
          var mejor = vivos.length
            ? Math.max.apply(null, vivos.map(function(S){ return E[S.id].dia; })) : 0;

          /* A 11 px cada caracter gasta 7,26: aqui caben 85 desde x=16, y con
             el rotulo largo que habia antes se salía del lienzo en un movil. */
          m += '<text x="16" y="24" class="rotulo-svg">VAS POR EL D\\u00cdA ' + dia
             + '  \\u00b7  pon y quita sitios arriba, y haz que pase algo abajo</text>';

          /* ------------------------- los sitios ------------------------- */
          for(i = 0; i < BASE.length; i++){
            var S = BASE[i], x = 16 + i * 156, cx = x + 70, on = !!act[S.id];
            var st = E[S.id].estado;
            m += caja(x, 44, 140, 132, on ? 'var(--surface)' : 'var(--surface-2)',
                      on ? (st === 'bien' ? 'var(--goo-verde)' : 'var(--goo-rojo)') : 'var(--line)',
                      on ? 2 : 1.5, !on);
            m += '<text x="' + cx + '" y="66" text-anchor="middle" class="rotulo-svg" '
               + 'style="font-size:10.5px;fill:' + (on ? 'var(--ink)' : 'var(--ink-soft)')
               + ';font-weight:500">' + S.etq + '</text>';
            m += '<text x="' + cx + '" y="82" text-anchor="middle" class="rotulo-svg" '
               + 'style="font-size:9px">' + S.sub + '</text>';
            if(!on){
              m += '<text x="' + cx + '" y="116" text-anchor="middle" class="rotulo-svg" '
                 + 'style="font-size:11px">no la tienes</text>';
              continue;
            }
            m += '<text x="' + cx + '" y="114" text-anchor="middle" class="rotulo-svg" '
               + 'style="font-size:12.5px;fill:' + COLOR[st] + ';font-weight:500">'
               + PALABRA[st] + '</text>';
            m += '<text x="' + cx + '" y="132" text-anchor="middle" class="rotulo-svg" '
               + 'style="font-size:9.5px">' + (st === 'bien'
                  ? 'con lo del d\\u00eda ' + E[S.id].dia : 'no te sirve') + '</text>';
            m += '<text x="' + cx + '" y="152" text-anchor="middle" class="rotulo-svg" '
               + 'style="font-size:8.5px">' + (S.sitio === 'casa' ? 'en tu casa' : 'fuera de tu casa')
               + '</text>';
            m += '<text x="' + cx + '" y="166" text-anchor="middle" class="rotulo-svg" '
               + 'style="font-size:8.5px;fill:' + (sincro(S) ? 'var(--goo-rojo)' : 'var(--goo-verde)')
               + '">' + (sincro(S) ? 'va sincronizado' : 'copia aparte') + '</text>';
          }

          /* ------------------------ el veredicto ------------------------ */
          var salvado = vivos.length > 0;
          m += caja(16, 192, 608, 92, 'var(--surface)',
                    salvado ? 'var(--goo-verde)' : 'var(--goo-rojo)', 2);
          m += '<text x="32" y="214" class="rotulo-svg" style="font-size:10px">'
             + '\\u00bfPUEDES RECUPERAR EL ARCHIVO?</text>';
          m += '<text x="32" y="244" class="rotulo-svg" style="font-size:17px;fill:'
             + (salvado ? 'var(--goo-verde)' : 'var(--goo-rojo)') + ';font-weight:500">'
             + (salvado ? 'S\\u00cd' : 'NO. No queda ni una copia buena.') + '</text>';
          var linea;
          if(salvado){
            var perdidos = dia - mejor;
            linea = (vivos.length > 1
                     ? 'Te quedan ' + vivos.length + ' sitios'
                     : 'Te queda 1 sitio')
                  + ', y lo m\\u00e1s nuevo es del d\\u00eda ' + mejor + ': '
                  + (perdidos === 0
                     ? 'no pierdes nada.'
                     : 'pierdes ' + perdidos + ' d\\u00eda' + (perdidos > 1 ? 's' : '')
                       + ' de trabajo.');
          } else {
            linea = 'Todo lo que ten\\u00edas estaba o en el mismo sitio o sincronizado con \\u00e9l.';
          }
          m += '<text x="32" y="268" class="rotulo-svg" style="font-size:11.5px">'
             + esc(linea) + '</text>';

          /* ----------------------- la regla 3-2-1 ----------------------- */
          var soportes = [];
          hay.forEach(function(S){ if(soportes.indexOf(S.soporte) < 0) soportes.push(S.soporte); });
          var fuera = hay.filter(function(S){ return S.sitio === 'fuera'; }).length;
          var aparte = hay.filter(function(S){ return !sincro(S); }).length;
          var cumple = (hay.length >= 3) && (soportes.length >= 2) && (fuera >= 1);

          m += caja(16, 296, 608, 124, 'var(--surface-2)', 'var(--line)', 1.5);
          m += '<text x="32" y="318" class="rotulo-svg" style="font-size:10px">LA REGLA 3-2-1, '
             + 'CONTANDO LO QUE TIENES PUESTO</text>';
          var CONT = [
            [hay.length,       3, 'COPIAS EN TOTAL', 'hacen falta 3'],
            [soportes.length,  2, 'SOPORTES DISTINTOS', 'hacen falta 2'],
            [fuera,            1, 'FUERA DE TU CASA', 'hace falta 1'],
            [aparte,           1, 'QUE NO SE SINCRONIZAN', 'las dem\\u00e1s no cuentan']
          ];
          for(i = 0; i < CONT.length; i++){
            var C = CONT[i], xx = 40 + i * 148, ok = C[0] >= C[1];
            /* La cifra y el "de N" van en el MISMO <text>, con la cifra en un
               tspan: así el texto se lee entero ("2 de 3") y no pegado. */
            m += '<text x="' + xx + '" y="356" class="rotulo-svg" style="font-size:11px">'
               + '<tspan style="font-size:22px;font-weight:500;fill:'
               + (ok ? 'var(--goo-verde)' : 'var(--goo-rojo)') + '">' + C[0] + '</tspan>'
               + ' de ' + C[1] + '</text>';
            m += '<text x="' + xx + '" y="376" class="rotulo-svg" style="font-size:9.5px">'
               + C[2] + '</text>';
            m += '<text x="' + xx + '" y="388" class="rotulo-svg" style="font-size:9px">'
               + C[3] + '</text>';
          }
          m += '<text x="32" y="410" class="rotulo-svg" style="font-size:12px;fill:'
             + (cumple ? 'var(--goo-verde)' : 'var(--ink-soft)') + '">'
             + (cumple
                ? 'Cumples la regla 3-2-1.'
                  + (aparte < 1 ? '  Y aun as\\u00ed, un borrado se lo lleva TODO.' : '')
                : 'Todav\\u00eda no cumples la regla 3-2-1.')
             + '</text>';

          svg.innerHTML = m;

          pie.innerHTML = (ultimo ? '<b>' + ultimo + '</b> ' : '')
            + 'Prueba esto, que es el experimento de la sesi&oacute;n: deja puesta <b>la nube</b>, '
            + 'pon el <b>disco</b> y ponlo <b>sincronizado</b>. Ya tienes tres copias, en dos '
            + 'soportes, una fuera: la regla 3-2-1 <b>cumplida</b>. Ahora dale a '
            + '&laquo;lo borro sin querer&raquo;.'
            + '<br><span style="font-size:12.5px">Lo que ves no sale de una lista de casos: cada '
            + 'desastre es una regla que se aplica a los sitios que cumplen una condici&oacute;n '
            + '(lo que est&aacute; en casa, lo que est&aacute; en la nube, lo que va sincronizado), y '
            + 'los cuatro n&uacute;meros de abajo salen de contar. Los d&iacute;as son para que se '
            + 'vea otra cosa que no se suele contar: una copia de seguridad <b>siempre va con '
            + 'retraso</b>, y lo que se pierde es lo que hiciste desde la &uacute;ltima.</span>';
        }

        function marca(){
          document.querySelectorAll('#seg-nube-que button').forEach(function(b){
            var q = b.dataset.q;
            var on = (q === 'dsync') ? discoSync : !!act[q];
            b.setAttribute('aria-pressed', on ? 'true' : 'false');
          });
          pinta();
        }

        document.getElementById('seg-nube-que').addEventListener('click', function(e){
          var b = e.target.closest('button[data-q]'); if(!b) return;
          if(b.dataset.q === 'dsync'){
            discoSync = !discoSync;
            ultimo = discoSync
              ? 'El disco se queda enchufado y se sincroniza solo: ya no es una copia aparte.'
              : 'El disco vuelve al caj\\u00f3n: ahora s\\u00ed es una copia aparte.';
          } else {
            act[b.dataset.q] = act[b.dataset.q] ? 0 : 1;
            E[b.dataset.q] = {estado:'bien', dia:dia};
            ultimo = '';
          }
          marca();
        });

        document.getElementById('seg-nube-pasa').addEventListener('click', function(e){
          var b = e.target.closest('button[data-p]'); if(!b) return;
          var p = b.dataset.p;
          if(p === 'trabaja') trabaja();
          else if(p === 'copia') copia();
          else if(p === 'borra')
            rompe(function(S){ return S.fija || sincro(S); }, 'borrado',
                  'Lo has borrado en el port\\u00e1til. Todo lo sincronizado lo ha borrado tambi\\u00e9n, y en un segundo.');
          else if(p === 'rompe')
            rompe(function(S){ return !!S.fija; }, 'roto',
                  'El port\\u00e1til ya no arranca.');
          else if(p === 'casa')
            rompe(function(S){ return S.sitio === 'casa'; }, 'roto',
                  'El agua se ha llevado todo lo que ten\\u00edas en casa, estuviera enchufado o no.');
          else if(p === 'cuenta')
            rompe(function(S){ return S.soporte === 'la nube'; }, 'roto',
                  'Sin cuenta no hay nube: los archivos siguen ah\\u00ed, pero no son tuyos ni te dejan entrar.');
          else { reset(); return; }
          pinta();
        });

        reset();
      })();
      </script>
'''


# ---------------------------------------------------------------------------
# S6 · El calendario de tus derechos
#
# Lienzo 640 x 372.
#   Panel del derecho elegido   x 16..624   y  30..126
#   Linea de tiempo                          y 152..252
#       eje de x=60 a x=596 (536 px). x(d) = 60 + d/d3 * 536, con d3 los dias
#       que van del envio al final de la prorroga. Las marcas NO estan a
#       tercios: van donde caen de verdad, porque los meses no miden igual.
#   Panel de la edad            x 16..624   y 264..360
#
# Las fechas del eje van en corto ("18 sep 2026") y no en largo: la del envio
# se ancla a la izquierda y la del mes al centro, y en largo (24 caracteres,
# 182 px) se pisan. En corto son 11 caracteres, 84 px, y no se tocan ni en el
# peor reparto. Las fechas completas se dan en el pie, que es de donde las
# copian para la practica.
#
# Las dos cuentas son de calendario de verdad:
#   · sumar meses ARRASTRA el fin de mes: 31 de enero + 1 mes = 28 de febrero
#     (o 29 si el ano es bisiesto). Es donde falla todo el mundo, y por eso la
#     funcion recorta el dia al ultimo del mes de destino.
#   · la edad se calcula en anos, meses y dias, pidiendo prestados los dias del
#     mes anterior cuando hacen falta.
#
# Los datos legales estan comprobados en la fuente y citados en el texto de la
# sesion: plazo de un mes prorrogable otros dos (RGPD art. 12.3) y catorce anos
# para consentir en Espana (LO 3/2018, art. 7).
# ---------------------------------------------------------------------------
ESCENA_DERECHOS = u'''
      <div class="escena" id="esc-derechos">
        <div class="escena-barra">
          <span class="escena-titulo">Qu&eacute; puedes exigir, y cu&aacute;ndo te tienen que contestar</span>
          <div class="seg" id="seg-der">
            <button type="button" data-d="acceso" aria-pressed="true">Acceso</button>
            <button type="button" data-d="rect">Rectificaci&oacute;n</button>
            <button type="button" data-d="supr">Supresi&oacute;n</button>
            <button type="button" data-d="port">Portabilidad</button>
          </div>
        </div>
        <div class="escena-barra">
          <span class="escena-titulo">Pon tus fechas</span>
          <div class="seg">
            <label style="font:400 12px var(--f-m);color:var(--ink-soft)">lo pides el
              <input id="der-envio" type="date"
                     style="font:400 12px var(--f-m);padding:5px 7px;border:1.5px solid var(--line);
                            border-radius:2px;background:var(--surface);color:var(--ink)">
            </label>
            <label style="font:400 12px var(--f-m);color:var(--ink-soft)">naciste el
              <input id="der-nac" type="date"
                     style="font:400 12px var(--f-m);padding:5px 7px;border:1.5px solid var(--line);
                            border-radius:2px;background:var(--surface);color:var(--ink)">
            </label>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 372" id="svg-derechos" role="img"
               aria-label="Qu&eacute; derecho est&aacute;s ejerciendo, el plazo que tienen para contestarte y si ya tienes edad para decidir t&uacute; solo"></svg>
        </div>
        <div class="pie" id="pie-derechos"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-derechos');
        if(!svg) return;
        var pie = document.getElementById('pie-derechos');
        var seg = document.getElementById('seg-der');
        var inE = document.getElementById('der-envio');
        var inN = document.getElementById('der-nac');

        var MESES = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto',
                     'septiembre','octubre','noviembre','diciembre'];
        var CORTO = ['ene','feb','mar','abr','may','jun','jul','ago',
                     'sep','oct','nov','dic'];
        var EDAD_ES = 14;      /* LO 3/2018, art. 7 */

        /* La linea "a" va en una sola linea de 13 px: 68 caracteres como
           mucho. La "b" se parte sola en dos de 12 px, 70 cada una. */
        var DER = {
          acceso: {n:'ACCESO', art:'RGPD, art\\u00edculo 15',
            a:'Que te ense\\u00f1en TODO lo que tienen tuyo, y de d\\u00f3nde lo sacaron.',
            b:'No vale un resumen: tienen que darte una copia, y adem\\u00e1s decirte para qu\\u00e9 lo usan y a qui\\u00e9n se lo dan.'},
          rect:   {n:'RECTIFICACI\\u00d3N', art:'RGPD, art\\u00edculo 16',
            a:'Que arreglen lo que tengan mal: un apellido, una fecha, un dato.',
            b:'Es el derecho m\\u00e1s f\\u00e1cil de ganar, porque un dato equivocado no lo defiende nadie.'},
          supr:   {n:'SUPRESI\\u00d3N', art:'RGPD, art\\u00edculo 17',
            a:'Que lo borren. Es el que la prensa llama "derecho al olvido".',
            b:'No siempre gana: si hay una ley que les obliga a guardarlo, se guarda. Pero te tienen que decir por qu\\u00e9.'},
          port:   {n:'PORTABILIDAD', art:'RGPD, art\\u00edculo 20',
            a:'Que te den lo tuyo en un archivo que puedas abrir y llevarte.',
            b:'Es el que impide que una aplicaci\\u00f3n te tenga atrapado por guardar dentro tus a\\u00f1os de fotos.'}
        };
        var sel = 'acceso';

        /* Parte un texto en lineas de n caracteres como mucho, sin cortar
           palabras. Igual que en la escena del espia de la sesion 2. */
        function parte(t, n){
          var pal = t.split(' '), l = [''];
          for(var i = 0; i < pal.length; i++){
            var cand = (l[l.length-1] + ' ' + pal[i]).trim();
            if(l[l.length-1] && cand.length > n) l.push(pal[i]);
            else l[l.length-1] = cand;
          }
          return l;
        }

        /* ---------------------- calendario de verdad ---------------------- */
        function dd(n){ return (n < 10 ? '0' : '') + n; }
        function iso(f){ return f.getFullYear() + '-' + dd(f.getMonth()+1) + '-' + dd(f.getDate()); }
        function deIso(s){
          var p = (s || '').split('-');
          if(p.length !== 3) return null;
          var f = new Date(+p[0], +p[1] - 1, +p[2]);
          return isNaN(f.getTime()) ? null : f;
        }
        function hoy(){
          var d = new Date();
          return new Date(d.getFullYear(), d.getMonth(), d.getDate());
        }
        function diasDelMes(a, m){ return new Date(a, m + 1, 0).getDate(); }
        /* Sumar meses ARRASTRA: el 31 de enero mas un mes es el 28 de febrero,
           no el 3 de marzo. Se recorta el dia al ultimo del mes de destino. */
        function masMeses(f, n){
          var a = f.getFullYear(), m = f.getMonth() + n, d = f.getDate();
          a += Math.floor(m / 12);
          m = ((m % 12) + 12) % 12;
          return new Date(a, m, Math.min(d, diasDelMes(a, m)));
        }
        function dias(a, b){ return Math.round((b - a) / 86400000); }
        function largo(f){
          return f.getDate() + ' de ' + MESES[f.getMonth()] + ' de ' + f.getFullYear();
        }
        function breve(f){
          return f.getDate() + ' ' + CORTO[f.getMonth()] + ' ' + f.getFullYear();
        }
        function edad(nac, ref){
          var a = ref.getFullYear() - nac.getFullYear();
          var m = ref.getMonth() - nac.getMonth();
          var d = ref.getDate() - nac.getDate();
          if(d < 0){
            m--;
            d += diasDelMes(ref.getFullYear(), (ref.getMonth() + 11) % 12);
          }
          if(m < 0){ a--; m += 12; }
          return {a:a, m:m, d:d};
        }

        function esc(s){
          return String(s).replace(/&/g,'&#38;').replace(/</g,'&#60;').replace(/>/g,'&#62;');
        }

        function pinta(){
          var D = DER[sel], m = '';
          var env = deIso(inE.value) || hoy();
          var un = masMeses(env, 1), tres = masMeses(env, 3);
          var d1 = dias(env, un), d3 = dias(env, tres);
          var H = hoy(), dh = dias(env, H);

          /* ------------------ panel del derecho elegido ------------------ */
          m += '<rect x="16" y="30" width="608" height="96" rx="2" fill="var(--surface)" '
             + 'stroke="var(--goo-azul)" stroke-width="2"></rect>';
          m += '<text x="32" y="52" class="rotulo-svg" style="font-size:10px">EL DERECHO DE '
             + D.n + '  \\u00b7  ' + D.art + '</text>';
          m += '<text x="32" y="76" class="rotulo-svg" style="font-size:13px;fill:var(--ink)">'
             + D.a + '</text>';
          var lb = parte(D.b, 70);      /* 70 x 7,92 px = 554, y hay 592 */
          for(var j = 0; j < lb.length && j < 2; j++)
            m += '<text x="32" y="' + (98 + j * 17) + '" class="rotulo-svg" '
               + 'style="font-size:12px">' + lb[j] + '</text>';

          /* ------------------------ linea de tiempo ------------------------ */
          m += '<text x="24" y="152" class="rotulo-svg" style="font-size:10px">LO QUE PUEDEN '
             + 'TARDAR EN CONTESTARTE  \\u00b7  ' + d3 + ' d\\u00edas en total, y no los pone el '
             + 'calendario a ojo</text>';

          var X = function(d){ return 60 + (d3 ? d / d3 : 0) * 536; };
          m += '<path d="M60 202 H596" stroke="var(--line)" stroke-width="2.5"></path>';
          /* el tramo del mes obligatorio, en verde; la prorroga, en amarillo */
          m += '<path d="M60 202 H' + X(d1).toFixed(1) + '" stroke="var(--goo-verde)" '
             + 'stroke-width="6" opacity=".55"></path>';
          m += '<path d="M' + X(d1).toFixed(1) + ' 202 H596" stroke="var(--goo-amarillo)" '
             + 'stroke-width="6" opacity=".55"></path>';

          var HITOS = [
            {d:0,  etq:'lo env\\u00edas', f:env,  anc:'start', col:'var(--ink)'},
            {d:d1, etq:'l\\u00edmite normal', f:un, anc:'middle', col:'var(--goo-verde)'},
            {d:d3, etq:'con pr\\u00f3rroga', f:tres, anc:'end',   col:'var(--goo-amarillo)'}
          ];
          for(var i = 0; i < HITOS.length; i++){
            var T = HITOS[i], x = X(T.d);
            m += '<path d="M' + x.toFixed(1) + ' 190 V214" stroke="' + T.col
               + '" stroke-width="2.5"></path>';
            m += '<text x="' + x.toFixed(1) + '" y="232" text-anchor="' + T.anc
               + '" class="rotulo-svg" style="font-size:11.5px;fill:var(--ink)">'
               + breve(T.f) + '</text>';
            m += '<text x="' + x.toFixed(1) + '" y="248" text-anchor="' + T.anc
               + '" class="rotulo-svg" style="font-size:9.5px;fill:' + T.col.replace('goo-amarillo', 'amar-texto').replace('goo-verde', 'verde-texto') + '">'
               + T.etq + (T.d ? '  (' + T.d + ' d\\u00edas)' : '') + '</text>';
          }
          if(dh >= 0 && dh <= d3){
            var xh = X(dh);
            m += '<path d="M' + xh.toFixed(1) + ' 174 V202" stroke="var(--goo-rojo)" '
               + 'stroke-width="2" stroke-dasharray="4 3"></path>';
            m += '<text x="' + xh.toFixed(1) + '" y="170" text-anchor="middle" class="rotulo-svg" '
               + 'style="font-size:10px;fill:var(--goo-rojo)">hoy</text>';
          }

          /* -------------------------- la edad -------------------------- */
          var nac = deIso(inN.value), puede = null, txt;
          m += '<rect x="16" y="264" width="608" height="96" rx="2" fill="var(--surface-2)" '
             + 'stroke="var(--line)" stroke-width="1.5"></rect>';
          m += '<text x="32" y="286" class="rotulo-svg" style="font-size:10px">\\u00bfPUEDES DECIDIR '
             + 'T\\u00da SOLO SOBRE TUS DATOS?  \\u00b7  en Espa\\u00f1a, desde los ' + EDAD_ES
             + ' a\\u00f1os</text>';
          if(!nac || nac > H){
            m += '<text x="32" y="314" class="rotulo-svg" style="font-size:13px;fill:var(--ink)">'
               + 'Pon ah\\u00ed arriba tu fecha de nacimiento.</text>';
          } else {
            var ed = edad(nac, H);
            puede = ed.a >= EDAD_ES;
            var cumple = new Date(nac.getFullYear() + EDAD_ES, nac.getMonth(), nac.getDate());
            m += '<text x="32" y="312" class="rotulo-svg" style="font-size:14px;fill:var(--ink)">'
               + 'Hoy tienes ' + ed.a + ' a\\u00f1os, ' + ed.m + ' meses y ' + ed.d
               + ' d\\u00edas.</text>';
            txt = puede
              ? 'S\\u00ed: puedes dar tu permiso t\\u00fa solo, y tambi\\u00e9n retirarlo t\\u00fa solo.'
              : 'Todav\\u00eda no. Hasta el ' + largo(cumple) + ' el permiso lo dan tus padres '
                + 'o tutores: te quedan ' + dias(H, cumple) + ' d\\u00edas.';
            var lt = parte(txt, 68);    /* a 12,5 px son 8,25 px cada uno */
            for(j = 0; j < lt.length && j < 2; j++)
              m += '<text x="32" y="' + (334 + j * 17) + '" class="rotulo-svg" '
                 + 'style="font-size:12.5px;fill:'
                 + (puede ? 'var(--verde-texto)' : 'var(--amar-texto)') + '">'
                 + esc(lt[j]) + '</text>';
          }

          svg.innerHTML = m;

          pie.innerHTML =
              'Tus dos fechas l&iacute;mite, completas: <b>' + largo(un) + '</b> la normal ('
            + d1 + ' d&iacute;as) y <b>' + largo(tres) + '</b> con pr&oacute;rroga ('
            + d3 + ' d&iacute;as). C&oacute;pialas, que hacen falta para la pr&aacute;ctica.'
            + '<br>Cambia la fecha de env&iacute;o y mira los d&iacute;as del total: <b>no siempre salen '
            + 'los mismos</b>. Un mes no es &laquo;treinta d&iacute;as&raquo;, es <b>hasta el mismo '
            + 'n&uacute;mero del mes siguiente</b>, y cuando ese n&uacute;mero no existe se recorta: '
            + 'el <b>31 de enero m&aacute;s un mes es el 28 de febrero</b>. Pru&eacute;balo.'
            + '<br><span style="font-size:12.5px">Los dos plazos son los de la ley y est&aacute;n '
            + 'comprobados en la fuente: <b>un mes</b> para contestarte, que pueden alargar '
            + '<b>otros dos</b> si la cosa es complicada, y entonces te lo tienen que avisar '
            + '(RGPD, art. 12). Y los <b>catorce a&ntilde;os</b> para consentir t&uacute; solo los '
            + 'pone la ley espa&ntilde;ola (Ley Org&aacute;nica 3/2018, art. 7): el reglamento europeo '
            + 'dice diecis&eacute;is, y deja que cada pa&iacute;s lo baje hasta trece. Espa&ntilde;a lo '
            + 'dej&oacute; en catorce.</span>';
        }

        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-d]'); if(!b) return;
          sel = b.dataset.d;
          seg.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
          pinta();
        });
        inE.addEventListener('change', pinta);
        inN.addEventListener('change', pinta);
        inE.addEventListener('input', pinta);
        inN.addEventListener('input', pinta);

        /* Arranca con hoy y con alguien que hoy cumple justo trece anos: asi la
           primera vez que se abre dice "todavia no", que es el caso de casi
           toda la clase. */
        (function(){
          var h = hoy();
          inE.value = iso(h);
          inN.value = iso(new Date(h.getFullYear() - 13, h.getMonth(), h.getDate()));
        })();
        pinta();
      })();
      </script>
'''
