# -*- coding: utf-8 -*-
u"""4.o de ESO - Tecnologia - Tema 3 - Escenas de las sesiones 5 y 6.

Las dos CALCULAN. No hay un solo numero escrito a mano en la pantalla.

  CADENA (S5)   Que le pasa de verdad a un kilo de material cuando lo echas al
                contenedor. Los rendimientos de las cuatro etapas se
                MULTIPLICAN, y de ahi sale el rendimiento del sistema. Con ese
                rendimiento se calculan dos cosas mas: el techo del contenido
                reciclado (no se puede fabricar con mas reciclado del que
                vuelve) y cuanto queda del kilo original despues de n vueltas,
                que es q elevado a n.

                Ademas separa CICLO CERRADO de CICLO ABIERTO: si la fraccion
                va mezclada, el material sale con otra composicion y ya no
                vuelve al mismo producto. Entonces q vale cero y la curva se
                muere en la primera vuelta. Eso se ve.

  CARBONO (S6)  El mismo kilo, dos facturas. La energia incorporada de cada
                material (la de la sesion 2, sin tocarla) al lado de sus kilos
                de CO2 equivalente, y estos SE CALCULAN:

                    CO2 = kWh electricos x factor de la red + lo que no viene
                          de quemar energia

                El factor de la red es un deslizador, asi que el mismo kilo de
                aluminio pasa de 4,3 a 18,1 kg de CO2 sin cambiar de material.
                Las filas van ordenadas por MJ; si las barras de CO2 no bajan
                en escalera, es que el orden no es el mismo. Eso es la sesion.

Prefijos CSS propios (m5-, m6-). Ninguna clase empieza por test-.
Las cadenas de JS llevan \\uXXXX y no entidades HTML: una entidad dentro de una
cadena de JavaScript que va a un <text> de SVG es un riesgo que no hace falta
correr, y ademas descuadraria el calculo del ancho.
Estos textos NO pasan por ningun formateo con %, asi que el % va una sola vez.

--------------------------------------------------------------------------
DE DONDE SALEN LOS NUMEROS
--------------------------------------------------------------------------
S5 - RENDIMIENTOS DE LA CADENA

Los cuatro rendimientos de cada fraccion son ORDEN DE MAGNITUD y van rotulados
como criterio nuestro dentro de la propia escena. Los dos primeros ---llegar al
contenedor y salir de la planta de clasificacion--- son ademas DESLIZADORES,
justo porque son los que mas varian de un municipio a otro y los que mas mandan
en el resultado. La tasa de captura de partida es del orden de la que publican
los sistemas de recogida europeos para cada fraccion; el resto (preparacion y
horno) es del orden de lo que se lee en la literatura de proceso:

    fraccion      captura  clasif.  prepar.  horno   producto
    latas de Al     0,70     0,95     0,92    0,95   0,581
    botella PET     0,60     0,90     0,85    0,95   0,436
    acero envase    0,85     0,97     0,95    0,93   0,728
    vidrio          0,70     0,92     0,95    0,98   0,600
    carton          0,85     0,93     0,88    0,90   0,626

Por que se pierde en cada una, que es lo que hay que entender:
  - captura: acaba en la basura de siempre, en el suelo o en el contenedor
    equivocado.
  - clasificacion: la planta no acierta el 100 %; lo que se va al rechazo se
    incinera o se entierra.
  - preparacion: quitar lo que no es el material. En la lata es el LACADO, que
    hay que quemar antes de fundir; en la botella, el tapon y la etiqueta; en
    el carton, el agua y las tintas.
  - horno o proceso: el metal que se queda en la escoria, el vidrio que se va
    en finos, la fibra que se rompe y se cuela por la tela.

Las energias (MJ/kg) son las MISMAS de la sesion 2, sin tocar: Ashby, salvo el
aluminio, que es del International Aluminium Institute (186 y 8,3).

S6 - CO2

El modelo tiene DOS sumandos declarados y esta puesto asi para que el alumno
pueda comprobarlo:

    CO2 (kg/kg) = kWh electricos por kilo x factor de la red (kg CO2 / kWh)
                + lo que no viene de la electricidad

Y la energia queda amarrada a la sesion 2:

    MJ primarios = kWh x 3,6 x 2,0  +  lo que no es electricidad

o sea que la parte termica de cada material es ep - kWh x 7,2, y no se puede
mover sin mover la tabla de la sesion 2.

  material            ep(MJ/kg)  kWh/kg   no-electrico (kg CO2/kg)
  aluminio primario     186       14,1        4,00
  PET virgen             84        1,2        1,90
  acero de alto horno    25        0,5        1,90
  contrachapado          15        0,5        0,55
  aluminio reciclado      8,3      0,6        0,20
  hormigon                1,1      0,02       0,12

El 4,00 del aluminio primario es NUESTRA SUMA, y va declarada por partes:

    anodos de carbono que se consumen        ~2,0 kg CO2/kg Al
    PFC del efecto anodo                     ~0,3
    alumina (proceso Bayer), mina y colada   ~1,7
                                             ----
                                              4,0

De los tres, el primero es el que tiene apoyo: sustituir los anodos de carbono
por anodos inertes se cifra en unas 2 t de CO2e menos por tonelada de aluminio,
o sea que eso es lo que ponen los anodos. Los otros dos son estimacion nuestra.

Con esa suma, la escena da:

    14,1 x 0,02 + 4,00 =  4,28   ruta hidroelectrica (Islandia)
    14,1 x 0,146 + 4,00 =  6,06   con la red espanola de 2024
    14,1 x 0,86 + 4,00 = 16,13   con un mix muy cargado de carbon
    14,1 x 1,00 + 4,00 = 18,10   con una central de carbon

que es el orden de magnitud de lo que se publica para esas rutas. ⚠️ En la
pagina NO se atribuye ninguna de esas cuatro cifras a ninguna institucion: la
atribucion al International Aluminium Institute se queda donde estaba, en los
186 y los 8,3 MJ/kg de la sesion 2, que es lo que esta contrastado. Ver
INFORME.md.

El del acero sale bien por el mismo camino: 0,5 x 0,146 + 1,90 = 1,97 kg/kg,
y la ruta alto horno - convertidor se publica en 2,2-2,3 t por tonelada de
acero bruto. El del PET, 1,2 x 0,146 + 1,90 = 2,08, contra los 2,2-2,4 que se
publican para la resina virgen.

Dos numeros mas que NO son estimacion, sino quimica, y por eso la pagina los
deja calculados a la vista:

  - Carbono del PET. El PET es C10H8O4, masa molar 192 g/mol, con 120 g de
    carbono. Si se incinera, cada kilo suelta 120/192 x 44/12 = 2,29 kg de CO2.
  - Carbono de la madera. Una madera seca es carbono en un 45 % de su masa, asi
    que un kilo lleva dentro 0,45 x 44/12 = 1,65 kg de CO2 que estuvieron en el
    aire. Eso SOLO cuenta si el bosque se repone y mientras la madera no se
    queme ni se pudra, y la norma de declaraciones ambientales lo pone en un
    modulo aparte justamente por eso. Va dicho en la pagina. Fijate en que, si
    se marcan las dos casillas a la vez, la madera vuelve a positivo por si
    sola: lo que lleva dentro y lo que suelta al quemarse son el mismo carbono.
  - Calcinacion del cemento. CaCO3 (100) -> CaO (56) + CO2 (44). Un clinker con
    un 65 % de CaO suelta 0,65 / 56 x 44 = 0,51 kg de CO2 por kilo de clinker
    SIN QUEMAR NADA. Va en el texto de la sesion.

Factores de la red electrica, kg de CO2 por kWh:
    Islandia ~0,02 (hidraulica y geotermica)  ·  Espana 2024 0,146
    mix electrico mundial del aluminio ~0,86  ·  central de carbon ~1,00
El 0,146 de Espana en 2024 es el mismo dato que usa la unidad 8.
"""

# ==========================================================================
# S5 - La cadena de rendimientos
#
# Lienzo 660 x 420.
#   Cascada:    cinco filas, y = 52 + i*30, barra de x=250 a x=530 (280 px),
#               22 de alto. El porcentaje, a la derecha en x=538.
#   Separador:  y = 210
#   Curva:      marco L=90 R=636 T=250 B=372
#               x(n) = 90 + (n/10)*546      n = vueltas, 0..10
#               y(v) = 372 - v*122          v = fraccion, 0..1
# ==========================================================================
CADENA = u'''
      <div class="escena" id="esc-m5">
        <div class="escena-barra">
          <span class="escena-titulo">De un kilo que echas al contenedor, &iquest;cu&aacute;nto vuelve a ser material?</span>
          <div class="seg" id="seg-m5-fr">
            <button type="button" data-f="lata" aria-pressed="true">Latas de aluminio</button>
            <button type="button" data-f="pet">Botellas de PET</button>
            <button type="button" data-f="acero">Acero</button>
            <button type="button" data-f="vidrio">Vidrio</button>
            <button type="button" data-f="carton">Cart&oacute;n</button>
          </div>
        </div>
        <div class="escena-barra">
          <label class="ctrl" style="flex:1 1 250px">
            <span>Llega al contenedor que le toca</span>
            <input id="m5-capt" type="range" min="10" max="100" value="70" step="1">
            <b id="m5-capt-v">70 %</b>
          </label>
          <label class="ctrl" style="flex:1 1 250px">
            <span>Acierta la planta de clasificaci&oacute;n</span>
            <input id="m5-sep" type="range" min="50" max="100" value="95" step="1">
            <b id="m5-sep-v">95 %</b>
          </label>
        </div>
        <div class="escena-barra">
          <label class="ctrl"><input type="checkbox" id="m5-mezcla">
            <span>Va mezclado con otras cosas del mismo material</span></label>
          <label class="ctrl" style="flex:1 1 220px">
            <span>Vueltas al ciclo</span>
            <input id="m5-ciclos" type="range" min="1" max="10" value="3" step="1">
            <b id="m5-ciclos-v">3 vueltas</b>
          </label>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 660 420" id="svg-m5" role="img"
               aria-label="Cascada con lo que queda de un kilo despu&eacute;s de cada etapa del reciclado, y curva de lo que sigue en el mismo uso despu&eacute;s de varias vueltas"></svg>
        </div>
        <div class="m1-tabla" id="tabla-m5"></div>
        <div class="pie" id="pie-m5"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-m5');
        if(!svg) return;
        var tabla = document.getElementById('tabla-m5');
        var pie   = document.getElementById('pie-m5');
        var segF  = document.getElementById('seg-m5-fr');
        var sCapt = document.getElementById('m5-capt');
        var sSep  = document.getElementById('m5-sep');
        var sCic  = document.getElementById('m5-ciclos');
        var cMez  = document.getElementById('m5-mezcla');

        /* ---------------- los datos, todos declarados ----------------
           capt  llega al contenedor que le toca, en tanto por ciento
           sep   la planta de clasificacion lo manda al monton bueno
           prep  sobrevive a quitarle lo que no es el material
           fus   sale del horno o del proceso convertido en material
           ep    MJ/kg sacandolo del mineral      (sesion 2)
           er    MJ/kg por la via reciclada       (sesion 2)
           pierde   que es lo que se queda por el camino en la preparacion
           cerra    a donde va si se recoge separado
           abierto  a donde va si va mezclado                              */
        var FR = {
          lata: {nom:'Latas de aluminio', capt:70, sep:95, prep:0.92, fus:0.95,
            ep:186, er:8.3, col:'#4285f4',
            pierde:'el lacado, que hay que quemar antes de fundir',
            cerra:'chapa de lata otra vez',
            abierto:'aleaci\\u00f3n de moldeo: bloques de motor, no latas'},
          pet: {nom:'Botellas de PET', capt:60, sep:90, prep:0.85, fus:0.95,
            ep:84, er:45, col:'#34a853',
            pierde:'el tap\\u00f3n, la etiqueta y el agua del lavado',
            cerra:'botella otra vez, botella a botella',
            abierto:'fibra textil o relleno: de ah\\u00ed ya no vuelve'},
          acero: {nom:'Acero de envase', capt:85, sep:97, prep:0.95, fus:0.93,
            ep:25, er:10, col:'#ea4335',
            pierde:'el esta\\u00f1o del recubrimiento y la pintura',
            cerra:'acero otra vez, sin perder propiedades',
            abierto:'acero con cobre dentro, que ya no se puede quitar'},
          vidrio: {nom:'Vidrio de envase', capt:70, sep:92, prep:0.95, fus:0.98,
            ep:15, er:9, col:'#fbbc05',
            pierde:'tapas, cer\\u00e1mica, porcelana y los finos',
            cerra:'botella del mismo color',
            abierto:'lana de vidrio o \\u00e1rido: ya no es envase'},
          carton: {nom:'Cart\\u00f3n y papel', capt:85, sep:93, prep:0.88, fus:0.90,
            ep:25, er:12, col:'#9334e6',
            pierde:'grapas, pl\\u00e1sticos, tintas y el agua del p\\u00faper',
            cerra:'cart\\u00f3n otra vez, con la fibra m\\u00e1s corta',
            abierto:'cart\\u00f3n gris de la peor calidad'}
        };
        var ETAPAS = ['Se pone en el mercado', 'Llega al contenedor',
                      'Sale de la clasificaci\\u00f3n', 'Pasa la preparaci\\u00f3n',
                      'Sale del horno'];
        var NMAX = 10;

        var fr = 'lata';

        function n(v, d){
          d = (d === undefined) ? 1 : d;
          return v.toLocaleString('es-ES', {minimumFractionDigits:d, maximumFractionDigits:d});
        }

        /* ---------------- las cuentas ---------------- */
        function calcula(){
          var F = FR[fr];
          var capt = +sCapt.value / 100, sep = +sSep.value / 100;
          var pasos = [1, capt, sep, F.prep, F.fus];
          var acum = [1], a = 1;
          for(var i = 1; i < pasos.length; i++){ a *= pasos[i]; acum.push(a); }
          var eta = a;                       /* rendimiento de toda la cadena */
          var q = cMez.checked ? 0 : eta;    /* lo que vuelve AL MISMO uso */
          var vueltas = +sCic.value;
          var queda = Math.pow(q, vueltas);
          var kgRecogidos = eta > 0 ? 1 / eta : 0;
          return {F:F, capt:capt, sep:sep, pasos:pasos, acum:acum, eta:eta, q:q,
                  vueltas:vueltas, queda:queda, kgRecogidos:kgRecogidos,
                  ahorro: (F.ep - F.er) * eta};
        }

        /* ---------------- dibujo ---------------- */
        function dibuja(){
          var c = calcula(), F = c.F, s = '';

          s += '<text x="24" y="22" class="etq">De 1 kg de ' + F.nom.toLowerCase()
             + ' puesto en el mercado</text>';
          s += '<text x="24" y="38" class="ejeq">cada etapa se lleva su parte, y las partes se multiplican</text>';

          /* ---- la cascada ---- */
          var X0 = 250, W = 280;
          for(var i = 0; i < 5; i++){
            var y = 52 + i * 30;
            var w = W * c.acum[i];
            s += '<text x="24" y="' + (y + 16) + '" class="ejeq">' + ETAPAS[i] + '</text>';
            if(w < W - 0.4){
              s += '<rect x="' + (X0 + w).toFixed(1) + '" y="' + y + '" width="' + (W - w).toFixed(1)
                 + '" height="22" fill="var(--goo-rojo)" opacity=".13"/>';
            }
            s += '<rect x="' + X0 + '" y="' + y + '" width="' + w.toFixed(1)
               + '" height="22" fill="' + F.col + '" opacity="' + (i === 4 ? 1 : 0.55) + '"/>';
            s += '<rect x="' + X0 + '" y="' + y + '" width="' + W
               + '" height="22" fill="none" stroke="var(--line)" stroke-width="1"/>';
            s += '<text x="' + (X0 + W + 8) + '" y="' + (y + 16) + '" class="etq">'
               + n(100 * c.acum[i]) + ' %</text>';
          }
          s += '<line x1="24" y1="210" x2="636" y2="210" stroke="var(--line)" stroke-width="1"/>';

          /* ---- la curva de las vueltas ---- */
          s += '<text x="24" y="232" class="etq">De ese kilo, cu\\u00e1nto sigue en el MISMO uso tras n vueltas</text>';
          var L = 90, R = 636, T = 250, B = 372;
          var px = function(v){ return L + (v / NMAX) * (R - L); };
          var py = function(v){ return B - v * (B - T); };
          s += '<rect x="' + L + '" y="' + T + '" width="' + (R-L) + '" height="' + (B-T)
             + '" fill="none" stroke="var(--line)" stroke-width="1"/>';
          for(var g = 0; g <= 4; g++){
            var vv = g / 4, yy = py(vv);
            s += '<line x1="' + L + '" y1="' + yy.toFixed(1) + '" x2="' + R + '" y2="' + yy.toFixed(1)
               + '" stroke="var(--line-soft)" stroke-width="1"/>';
            s += '<text x="84" y="' + (yy + 4).toFixed(1) + '" text-anchor="end" class="ejeq">'
               + Math.round(100 * vv) + ' %</text>';
          }
          for(g = 0; g <= NMAX; g++){
            s += '<text x="' + px(g).toFixed(1) + '" y="388" text-anchor="middle" class="ejeq">'
               + g + '</text>';
          }
          s += '<text x="' + ((L+R)/2) + '" y="406" text-anchor="middle" class="ejeq">vueltas al ciclo</text>';

          var pts = [];
          for(g = 0; g <= NMAX; g++){
            pts.push(px(g).toFixed(1) + ',' + py(Math.pow(c.q, g)).toFixed(1));
          }
          s += '<polyline points="' + pts.join(' ') + '" fill="none" stroke="' + F.col
             + '" stroke-width="2.6"/>';
          var mx = px(c.vueltas), my = py(c.queda);
          s += '<circle cx="' + mx.toFixed(1) + '" cy="' + my.toFixed(1)
             + '" r="5.5" fill="var(--surface)" stroke="' + F.col + '" stroke-width="2.5"/>';
          var der = mx < (L + R) / 2;
          s += '<text x="' + (mx + (der ? 11 : -11)).toFixed(1) + '" y="' + (my - 9).toFixed(1)
             + '" class="etq"' + (der ? '' : ' text-anchor="end"') + '>'
             + n(100 * c.queda, 1) + ' %</text>';

          svg.innerHTML = s;

          /* ---- la tabla ---- */
          var f = '';
          f += '<div class="m1-fila"><span>Llega al contenedor que le toca</span><span>'
             + n(1000, 0) + ' g &times; ' + n(c.capt, 2) + ' = <b>' + n(1000 * c.acum[1], 0) + ' g</b></span></div>';
          f += '<div class="m1-fila"><span>Acierta la planta de clasificaci&oacute;n</span><span>'
             + n(1000 * c.acum[1], 0) + ' g &times; ' + n(c.sep, 2) + ' = <b>'
             + n(1000 * c.acum[2], 0) + ' g</b></span></div>';
          f += '<div class="m1-fila"><span>Preparaci&oacute;n &mdash; fuera ' + F.pierde
             + '</span><span>' + n(1000 * c.acum[2], 0) + ' g &times; ' + n(F.prep, 2) + ' = <b>'
             + n(1000 * c.acum[3], 0) + ' g</b></span></div>';
          f += '<div class="m1-fila"><span>Sale del horno o del proceso</span><span>'
             + n(1000 * c.acum[3], 0) + ' g &times; ' + n(F.fus, 2) + ' = <b>'
             + n(1000 * c.acum[4], 0) + ' g</b></span></div>';
          f += '<div class="m1-fila suma"><span>Rendimiento de toda la cadena</span><span>'
             + n(c.capt, 2) + ' &times; ' + n(c.sep, 2) + ' &times; ' + n(F.prep, 2) + ' &times; '
             + n(F.fus, 2) + ' = ' + n(100 * c.eta, 1) + ' %</span></div>';
          f += '<div class="m1-fila"><span>Para tener 1 kg de material reciclado hay que recoger</span><span>'
             + '1 &divide; ' + n(c.eta, 3) + ' = <b>' + n(c.kgRecogidos, 2) + ' kg</b></span></div>';
          f += '<div class="m1-fila"><span>Techo del contenido reciclado: no puede entrar m&aacute;s del que vuelve</span><span><b>'
             + n(100 * c.eta, 1) + ' %</b></span></div>';
          f += '<div class="m1-fila"><span>Energ&iacute;a que se salva de verdad por cada kilo puesto en el mercado</span><span>'
             + '(' + n(F.ep, 1) + ' &minus; ' + n(F.er, 1) + ') &times; ' + n(c.eta, 3)
             + ' = <b>' + n(c.ahorro, 1) + ' MJ</b></span></div>';
          f += '<div class="m1-fila"><span>D&oacute;nde acaba</span><span>'
             + (cMez.checked ? F.abierto : F.cerra) + '</span></div>';
          f += '<div class="m1-fila"><span>Del kilo de partida, tras ' + c.vueltas
             + ' vuelta' + (c.vueltas === 1 ? '' : 's') + ' en el mismo uso</span><span>'
             + n(c.q, 3) + ' elevado a ' + c.vueltas + ' = <b>' + n(100 * c.queda, 2)
             + ' %</b></span></div>';
          tabla.innerHTML = f;

          /* ---- el veredicto ---- */
          var t;
          if(cMez.checked){
            t = 'Mezclado, el material sale con otra composici\\u00f3n: ' + F.abierto
              + '. Sigue siendo reciclar y sigue ahorrando energ\\u00eda, pero es un <b>ciclo '
              + 'abierto</b>: baja un escal\\u00f3n y ya no vuelve a subir. Por eso la curva de '
              + 'abajo se muere en la primera vuelta.';
          } else {
            t = 'De cada kilo vuelven <b>' + n(1000 * c.eta, 0) + ' gramos</b>. El material aguanta '
              + 'las vueltas que quieras &mdash;eso es verdad&mdash;, pero el <b>sistema</b> se deja '
              + 'un ' + n(100 * (1 - c.eta), 0) + ' % en cada una: despu\\u00e9s de ' + c.vueltas
              + ' queda el ' + n(100 * c.queda, 1) + ' % del kilo original.';
          }
          pie.innerHTML = t + ' <br>Los cuatro rendimientos son <b>orden de magnitud</b> y criterio '
            + 'nuestro; los dos primeros se mueven porque son los que m\\u00e1s cambian de un sitio a '
            + 'otro. Los MJ/kg son los de la sesi\\u00f3n 2.';
        }

        /* ---------------- controles ---------------- */
        function rotulos(){
          sCapt.nextElementSibling.textContent = sCapt.value + ' %';
          sSep.nextElementSibling.textContent = sSep.value + ' %';
          sCic.nextElementSibling.textContent = sCic.value
            + (sCic.value === '1' ? ' vuelta' : ' vueltas');
        }
        segF.addEventListener('click', function(e){
          var b = e.target.closest('button'); if(!b) return;
          fr = b.dataset.f;
          segF.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x.dataset.f === fr ? 'true' : 'false');
          });
          sCapt.value = FR[fr].capt;
          sSep.value  = FR[fr].sep;
          rotulos(); dibuja();
        });
        [sCapt, sSep, sCic].forEach(function(x){
          x.addEventListener('input', function(){ rotulos(); dibuja(); });
        });
        cMez.addEventListener('change', dibuja);

        rotulos();
        dibuja();
      })();
      </script>
'''


# ==========================================================================
# S6 - El mismo kilo, dos facturas
#
# Lienzo 660 x 410.
#   Cabeceras:  y = 56
#   Seis filas: y = 70 + i*34, barras de 22 de alto
#       MJ    : de x=170 hacia la derecha, 140 px como mucho; el valor en
#               x=360 alineado a la derecha
#       CO2   : el cero en x=420. A la derecha caben 176 px, porque el valor
#               va SIEMPRE alineado a la derecha en x=636 y se reserva su
#               hueco; a la izquierda caben 40, que es lo que hay hasta el
#               valor de los MJ. La escala es la MISMA a los dos lados: de ahi
#               el minimo de las dos. Sin esa reserva, con la casilla del
#               carbono de la madera marcada la barra negativa se metia encima
#               del numero de los megajulios.
#   Separador:  y = 274
#   Desglose:   el cero en x=300; lo positivo hasta 260 px (x=560, y el total
#               cabe en 568..636) y lo negativo hasta 180 px (x=120)
# ==========================================================================
CARBONO = u'''
      <div class="escena" id="esc-m6">
        <div class="escena-barra">
          <span class="escena-titulo">El mismo kilo, dos facturas: megajulios y kilos de CO&#8322;</span>
          <div class="seg" id="seg-m6-mix">
            <button type="button" data-x="isl">Islandia</button>
            <button type="button" data-x="esp" aria-pressed="true">Red espa&ntilde;ola 2024</button>
            <button type="button" data-x="mun">Mix mundial del aluminio</button>
            <button type="button" data-x="car">Central de carb&oacute;n</button>
          </div>
        </div>
        <div class="escena-barra">
          <label class="ctrl" style="flex:1 1 280px">
            <span>CO&#8322; de la electricidad</span>
            <input id="m6-red" type="range" min="10" max="1000" value="146" step="2">
            <b id="m6-red-v">146 g/kWh</b>
          </label>
          <label class="ctrl" style="flex:1 1 200px">
            <span>Masa de la pieza</span>
            <input id="m6-masa" type="range" min="5" max="300" value="100" step="5">
            <b id="m6-masa-v">1,00 kg</b>
          </label>
        </div>
        <div class="escena-barra">
          <span class="escena-titulo">Desglose de</span>
          <div class="seg" id="seg-m6-mat">
            <button type="button" data-m="alp" aria-pressed="true">Al primario</button>
            <button type="button" data-m="pet">PET</button>
            <button type="button" data-m="fe">Acero</button>
            <button type="button" data-m="mad">Contrachapado</button>
            <button type="button" data-m="alr">Al reciclado</button>
            <button type="button" data-m="hor">Hormig&oacute;n</button>
          </div>
        </div>
        <div class="escena-barra">
          <label class="ctrl"><input type="checkbox" id="m6-bio">
            <span>Contar el carbono que la madera lleva dentro</span></label>
          <label class="ctrl"><input type="checkbox" id="m6-fin">
            <span>Contar lo que suelta si al final se quema</span></label>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 660 410" id="svg-m6" role="img"
               aria-label="Megajulios por kilo y kilos de CO&#8322; equivalente por kilo de seis materiales, y desglose del material elegido"></svg>
        </div>
        <div class="m1-tabla" id="tabla-m6"></div>
        <div class="pie" id="pie-m6"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-m6');
        if(!svg) return;
        var tabla = document.getElementById('tabla-m6');
        var pie   = document.getElementById('pie-m6');
        var segX  = document.getElementById('seg-m6-mix');
        var segM  = document.getElementById('seg-m6-mat');
        var sRed  = document.getElementById('m6-red');
        var sMasa = document.getElementById('m6-masa');
        var cBio  = document.getElementById('m6-bio');
        var cFin  = document.getElementById('m6-fin');

        /* ---------------- los datos, todos declarados ----------------
           ep    MJ/kg de energia primaria, los de la sesion 2
           kwh   kWh electricos por kilo
           proc  kg de CO2e por kilo que NO vienen de la electricidad
           cfin  kg de CO2 por kilo que suelta si al final se quema
           bio   kg de CO2 por kilo que lleva dentro (solo la madera)      */
        var MAT = [
          {k:'alp', nom:'Aluminio primario',  ep:186, kwh:14.1, proc:4.00, cfin:0,    bio:0,    col:'#4285f4'},
          {k:'pet', nom:'PET virgen',         ep:84,  kwh:1.2,  proc:1.90, cfin:2.29, bio:0,    col:'#34a853'},
          {k:'fe',  nom:'Acero de alto horno',ep:25,  kwh:0.5,  proc:1.90, cfin:0,    bio:0,    col:'#ea4335'},
          {k:'mad', nom:'Contrachapado',      ep:15,  kwh:0.5,  proc:0.55, cfin:1.65, bio:1.65, col:'#b06d2a'},
          {k:'alr', nom:'Aluminio reciclado', ep:8.3, kwh:0.6,  proc:0.20, cfin:0,    bio:0,    col:'#8ab4f8'},
          {k:'hor', nom:'Hormig\\u00f3n',     ep:1.1, kwh:0.02, proc:0.12, cfin:0,    bio:0,    col:'#9aa0a6'}
        ];
        var MIX = {
          isl: {f:20,   nom:'Islandia'},
          esp: {f:146,  nom:'la red espa\\u00f1ola de 2024'},
          mun: {f:860,  nom:'el mix mundial del aluminio'},
          car: {f:1000, nom:'una central de carb\\u00f3n'}
        };
        var PRIM = 2.0;    /* MJ primarios por MJ electrico, igual que en la sesion 1 */

        var mat = 'alp';

        function n(v, d){
          d = (d === undefined) ? 2 : d;
          return v.toLocaleString('es-ES', {minimumFractionDigits:d, maximumFractionDigits:d});
        }

        function calcula(){
          var f = +sRed.value / 1000;        /* kg de CO2 por kWh */
          var m = +sMasa.value / 100;        /* kg */
          var filas = MAT.map(function(M){
            var elec = M.kwh * f;
            var fin  = cFin.checked ? M.cfin : 0;
            var bio  = cBio.checked ? M.bio : 0;
            return {M:M, elec:elec, proc:M.proc, fin:fin, bio:bio,
                    co2: elec + M.proc + fin - bio,
                    mjElec: M.kwh * 3.6 * PRIM, mjTerm: M.ep - M.kwh * 3.6 * PRIM};
          });
          var porMJ  = filas.slice().sort(function(a,b){ return b.M.ep - a.M.ep; });
          var porCO2 = filas.slice().sort(function(a,b){ return b.co2 - a.co2; });
          var sel = filas[0];
          filas.forEach(function(x){ if(x.M.k === mat) sel = x; });
          return {f:f, m:m, filas:filas, porMJ:porMJ, porCO2:porCO2, sel:sel};
        }

        function dibuja(){
          var c = calcula(), s = '';
          var maxMJ = 0, maxPos = 0, maxNeg = 0;
          c.filas.forEach(function(r){
            if(r.M.ep > maxMJ) maxMJ = r.M.ep;
            if(r.co2 > maxPos) maxPos = r.co2;
            if(-r.co2 > maxNeg) maxNeg = -r.co2;
          });
          if(maxMJ <= 0) maxMJ = 1;

          s += '<text x="24" y="22" class="etq">Un kilo de cada material, con ' + n(1000 * c.f, 0)
             + ' g de CO\\u2082 por kWh</text>';
          s += '<text x="24" y="38" class="ejeq">ordenados por megajulios; si las barras de CO\\u2082 no bajan en escalera, el orden cambia</text>';
          s += '<text x="170" y="56" class="ejeq">MJ por kilo</text>';
          s += '<text x="420" y="56" class="ejeq">kg de CO\\u2082e por kilo</text>';

          /* una sola escala para el CO2, con sitio distinto a cada lado */
          var XM = 170, WM = 140, X0 = 420;
          var k = maxPos > 0 ? 176 / maxPos : 1;
          if(maxNeg > 0) k = Math.min(k, 40 / maxNeg);
          if(!isFinite(k) || k <= 0) k = 1;

          c.porMJ.forEach(function(r, i){
            var y = 70 + i * 34;
            var act = (r.M.k === mat);
            s += '<text x="24" y="' + (y + 16) + '" class="' + (act ? 'etq' : 'ejeq') + '">'
               + r.M.nom + '</text>';
            var w = WM * r.M.ep / maxMJ;
            s += '<rect x="' + XM + '" y="' + y + '" width="' + w.toFixed(1)
               + '" height="22" fill="' + r.M.col + '" opacity="' + (act ? 1 : 0.55) + '"/>';
            s += '<text x="360" y="' + (y + 16) + '" text-anchor="end" class="ejeq">'
               + n(r.M.ep, 1) + '</text>';
            var wc = Math.abs(r.co2) * k;
            s += '<rect x="' + (r.co2 >= 0 ? X0 : (X0 - wc)).toFixed(1) + '" y="' + y + '" width="'
               + wc.toFixed(1) + '" height="22" fill="'
               + (r.co2 >= 0 ? r.M.col : '#34a853') + '" opacity="' + (act ? 1 : 0.55) + '"/>';
            s += '<text x="636" y="' + (y + 16) + '" text-anchor="end" class="ejeq">'
               + n(r.co2, 2) + '</text>';
          });
          s += '<line x1="' + X0 + '" y1="64" x2="' + X0 + '" y2="266" stroke="var(--line)" stroke-width="1.5"/>';
          s += '<line x1="24" y1="274" x2="636" y2="274" stroke="var(--line)" stroke-width="1"/>';

          /* ---- el desglose del material elegido ---- */
          var r = c.sel, M = r.M;
          s += '<text x="24" y="296" class="etq">De d\\u00f3nde salen los ' + n(r.co2 * c.m, 2)
             + ' kg de CO\\u2082 de tu pieza de ' + n(c.m, 2) + ' kg</text>';
          var CX = 300, Y = 310, H = 28;
          var partes = [[r.elec * c.m, '#4285f4'], [r.proc * c.m, '#5f6368'], [r.fin * c.m, '#fbbc05']];
          var negat = r.bio * c.m, tot = 0;
          partes.forEach(function(p){ tot += p[0]; });
          var k2 = tot > 0 ? 260 / tot : 260;
          if(negat > 0) k2 = Math.min(k2, 180 / negat);

          var x = CX;
          partes.forEach(function(p){
            var w = p[0] * k2;
            if(w > 0.4){
              s += '<rect x="' + x.toFixed(1) + '" y="' + Y + '" width="' + w.toFixed(1)
                 + '" height="' + H + '" fill="' + p[1] + '"/>';
            }
            x += w;
          });
          if(negat > 0){
            var wn = negat * k2;
            s += '<rect x="' + (CX - wn).toFixed(1) + '" y="' + Y + '" width="' + wn.toFixed(1)
               + '" height="' + H + '" fill="#34a853"/>';
            s += '<text x="' + (CX - wn - 6).toFixed(1) + '" y="' + (Y + 19)
               + '" text-anchor="end" class="ejeq">\\u2212' + n(negat, 2) + '</text>';
          }
          s += '<line x1="' + CX + '" y1="' + (Y - 7) + '" x2="' + CX + '" y2="' + (Y + H + 7)
             + '" stroke="var(--ink)" stroke-width="1.5"/>';
          /* El titulo de arriba ya da el NETO; aqui van los dos lados con su
             signo, que si no el 0,62 de la derecha parec&iacute;a contradecir
             al -1,03 del t&iacute;tulo. */
          s += '<text x="' + (x + 8).toFixed(1) + '" y="' + (Y + 19) + '" class="etq">+'
             + n(tot, 2) + '</text>';

          var lx = 24;
          [['electricidad', '#4285f4'], ['todo lo dem\\u00e1s', '#5f6368'],
           ['al quemarlo', '#fbbc05'], ['lo que lleva dentro', '#34a853']].forEach(function(t){
            s += '<rect x="' + lx + '" y="360" width="10" height="10" fill="' + t[1] + '"/>';
            s += '<text x="' + (lx + 15) + '" y="369" class="ejeq">' + t[0] + '</text>';
            lx += 28 + t[0].length * 6.6;
          });
          s += '<text x="24" y="392" class="ejeq">' + M.nom + ': ' + n(M.kwh, 2)
             + ' kWh/kg a ' + n(1000 * c.f, 0) + ' g de CO\\u2082 el kWh, m\\u00e1s '
             + n(M.proc, 2) + ' kg que no salen del enchufe</text>';

          svg.innerHTML = s;

          /* ---- la tabla ---- */
          var f = '';
          f += '<div class="m1-fila"><span>Energ&iacute;a el&eacute;ctrica de ' + M.nom.toLowerCase()
             + '</span><span>' + n(M.kwh, 2) + ' kWh/kg &times; 3,6 &times; 2,0 = <b>'
             + n(r.mjElec, 1) + ' MJ/kg</b></span></div>';
          f += '<div class="m1-fila"><span>Lo dem&aacute;s de sus ' + n(M.ep, 1)
             + ' MJ/kg: la mina, el horno, la cola&hellip; y, en el pl&aacute;stico, el '
             + 'petr&oacute;leo que se convierte en material en vez de quemarse</span><span><b>'
             + n(r.mjTerm, 1) + ' MJ/kg</b></span></div>';
          f += '<div class="m1-fila"><span>CO&#8322; de la electricidad</span><span>'
             + n(M.kwh, 2) + ' kWh/kg &times; ' + n(c.f, 3) + ' kg/kWh = <b>'
             + n(r.elec, 2) + ' kg/kg</b></span></div>';
          f += '<div class="m1-fila"><span>CO&#8322; que no viene de la electricidad</span><span><b>'
             + n(M.proc, 2) + ' kg/kg</b></span></div>';
          if(cFin.checked){
            f += '<div class="m1-fila"><span>Si al final se quema</span><span>'
               + (M.cfin > 0 ? '+ <b>' + n(M.cfin, 2) + ' kg/kg</b>' : 'no lleva carbono propio') + '</span></div>';
          }
          if(cBio.checked){
            f += '<div class="m1-fila"><span>Carbono que lleva dentro</span><span>'
               + (M.bio > 0 ? '&minus; <b>' + n(M.bio, 2) + ' kg/kg</b>' : 'no lleva carbono del aire') + '</span></div>';
          }
          f += '<div class="m1-fila suma"><span>Total del material</span><span>'
             + n(r.co2, 2) + ' kg de CO&#8322;e por kilo</span></div>';
          f += '<div class="m1-fila"><span>Tu pieza de ' + n(c.m, 2) + ' kg</span><span>'
             + n(c.m, 2) + ' &times; ' + n(M.ep, 1) + ' = <b>' + n(c.m * M.ep, 1)
             + ' MJ</b> y ' + n(c.m, 2) + ' &times; ' + n(r.co2, 2) + ' = <b>'
             + n(c.m * r.co2, 2) + ' kg de CO&#8322;e</b></span></div>';
          var al = MAT[0];
          f += '<div class="m1-fila"><span>El MISMO kilo de aluminio primario, seg&uacute;n el enchufe</span><span>'
             + 'Islandia <b>' + n(al.kwh * 0.020 + al.proc, 2) + '</b> &middot; carb&oacute;n <b>'
             + n(al.kwh * 1.000 + al.proc, 2) + '</b> kg de CO&#8322;e</span></div>';
          tabla.innerHTML = f;

          /* ---- el veredicto: donde NO coinciden los dos ordenes ---- */
          var cambios = [];
          c.porMJ.forEach(function(x, i){
            var j = c.porCO2.indexOf(x);
            if(j !== i){
              cambios.push(x.M.nom + ' (n\\u00ba ' + (i+1) + ' en energ\\u00eda, n\\u00ba '
                           + (j+1) + ' en CO\\u2082)');
            }
          });
          var alp = c.filas[0], pet = c.filas[1];
          var rel = pet.co2 !== 0 ? alp.co2 / pet.co2 : 0;
          var t = 'El aluminio primario tiene <b>' + n(alp.M.ep / pet.M.ep, 1) + ' veces</b> la '
                + 'energ\\u00eda del PET y, con este enchufe, <b>' + n(rel, 1) + ' veces</b> su '
                + 'CO\\u2082. Energ\\u00eda y CO\\u2082 <b>no son la misma magnitud</b>: '
                + (cambios.length
                   ? 'y aqu\\u00ed adem\\u00e1s cambia el orden &mdash; ' + cambios.join('; ') + '.'
                   : 'aqu\\u00ed el orden coincide, pero las distancias no.');
          pie.innerHTML = t + ' <br>El sumando el\\u00e9ctrico <b>se calcula</b>; el otro es una suma '
            + 'nuestra, declarada por partes: en el aluminio primario, 2,0 de los \\u00e1nodos de '
            + 'carbono que se consumen, 0,3 de los PFC del efecto \\u00e1nodo y 1,7 de la mina, la '
            + 'al\\u00famina y la colada. Los MJ/kg son los de la sesi\\u00f3n 2, sin tocar.';
        }

        /* ---------------- controles ---------------- */
        function rotulos(){
          sRed.nextElementSibling.textContent = sRed.value + ' g/kWh';
          sMasa.nextElementSibling.textContent = n(+sMasa.value / 100) + ' kg';
        }
        segX.addEventListener('click', function(e){
          var b = e.target.closest('button'); if(!b) return;
          segX.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          sRed.value = MIX[b.dataset.x].f;
          rotulos(); dibuja();
        });
        segM.addEventListener('click', function(e){
          var b = e.target.closest('button'); if(!b) return;
          mat = b.dataset.m;
          segM.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x.dataset.m === mat ? 'true' : 'false');
          });
          dibuja();
        });
        [sRed, sMasa].forEach(function(x){
          x.addEventListener('input', function(){
            segX.querySelectorAll('button').forEach(function(b){ b.setAttribute('aria-pressed','false'); });
            rotulos(); dibuja();
          });
        });
        [cBio, cFin].forEach(function(x){ x.addEventListener('change', dibuja); });

        rotulos();
        dibuja();
      })();
      </script>
'''
