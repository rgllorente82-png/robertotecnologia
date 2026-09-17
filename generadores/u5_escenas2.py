# -*- coding: utf-8 -*-
"""Las escenas interactivas de las sesiones 4, 5 y 6 de la U5, en SVG y JavaScript a mano.

Van aparte de u5_build.py porque son largas. Cuatro escenas y un test:

  ESC_BIELA        biela-manivela, con la cinematica de verdad y la grafica del piston
  ESC_TRANSFORMA   leva y seguidor (tres perfiles), tornillo-tuerca y pinon-cremallera
  ESC_PLANTILLA    la plantilla de las ruedas de carton de la sesion 5
  ESC_CADENA       la maquina entera de la sesion 6: etapas encadenadas
  TEST + CSS_TEST  la autoevaluacion que se corrige sola

Reglas que se siguen en todas, las mismas que en las escenas 1 a 3:

  - Ninguna cadena pasa por formateo % de Python: se concatenan tal cual, asi que
    los % literales del JavaScript estan a salvo.
  - Los numeros que salen en pantalla se CALCULAN. No hay ni una tabla escrita a
    mano: si la escena dice 60 %, es porque ha resuelto la ecuacion.
  - La geometria tambien se calcula. El piston va donde dice la cinematica de la
    biela-manivela, y el perfil de la leva y la altura del seguidor salen de la
    MISMA funcion, asi que no pueden discrepar.
"""

# ============================================================================
# ESCENA 4.1 - Biela-manivela
# ============================================================================
# La posicion del piston NO es un seno. Sale de la cinematica exacta:
#
#     x(t) = r*cos(t) + raiz(L^2 - r^2*sen^2(t))     (desde el eje de giro)
#     s(t) = (L + r) - x(t)                          (recorrido desde el PMS)
#
# De ahi salen las dos cosas que ensena la escena: que la carrera es 2r exacto,
# valga lo que valga la biela, y que a un cuarto de vuelta el piston NO esta a
# media carrera, y cuanto se pasa depende de lo larga que sea la biela.
#
# Las tres bielas son 2,5 r, 4 r y 8 r. La corta no baja de 2,5 r a proposito:
# por debajo de eso el piston entraria dentro del circulo que barre la manivela,
# que es justamente por lo que no existen motores asi.
ESC_BIELA = u'''
      <div class="escena" id="esc-biela">
        <div class="escena-barra">
          <span class="escena-titulo">La manivela gira &middot; el pist&oacute;n va y viene</span>
          <div class="seg" id="seg-biela">
            <button type="button" data-b="corta">Biela corta</button>
            <button type="button" data-b="normal" aria-pressed="true">Biela normal</button>
            <button type="button" data-b="larga">Biela larga</button>
            <button type="button" data-b="muerto">&#9673; Punto muerto</button>
            <button type="button" data-b="pausa">&#9208; Parar</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 380" id="svg-biela" role="img"
               aria-label="Mecanismo de biela y manivela: la manivela gira y el pist&oacute;n va y viene
                           dentro del cilindro, con la gr&aacute;fica de su recorrido a lo largo de una vuelta"></svg>
        </div>
        <div class="pie" id="pie-biela"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-biela');
        var pie = document.getElementById('pie-biela');
        var seg = document.getElementById('seg-biela');
        if(!svg) return;

        var ESC = 1.3;              /* pixeles por milimetro */
        var Rmm = 40;               /* radio de la manivela, en mm */
        /* El mecanismo va a media altura: arriba estan los numeros y abajo la
           grafica, y la biela barre toda la banda de en medio.                */
        var CX = 130, CY = 176;     /* centro de giro de la manivela */
        var BIELAS = {corta: 100, normal: 160, larga: 320};   /* longitud L, en mm */
        var cual = 'normal', ang = 0, girando = true, raf = null, ultimo = 0;

        var AZ = 'var(--goo-azul)', RO = 'var(--goo-rojo)', VE = 'var(--goo-verde)',
            GR = 'var(--ink-soft)', TI = 'var(--ink)', LI = 'var(--line)';

        /* La cinematica, medida desde el eje de giro. */
        function xPiston(t, r, L){
          var s = r*Math.sin(t);
          return r*Math.cos(t) + Math.sqrt(L*L - s*s);
        }
        function rot(x, y, t, col, tam, anc){
          return '<text x="' + x + '" y="' + y + '" class="rotulo-svg"'
               + (anc ? ' text-anchor="' + anc + '"' : '')
               + ' style="font-size:' + (tam || 11) + 'px;fill:' + (col || GR) + '">' + t + '</text>';
        }
        /* Los dos rotulos que van pegados a piezas que se mueven llevan halo del
           color del fondo: pasan por encima del cilindro y del circulo de la
           manivela, y sin halo hay angulos en los que no se leen. */
        function pegado(x, y, t, col){
          return '<text x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" text-anchor="middle" '
               + 'class="rotulo-svg" paint-order="stroke" stroke="var(--surface)" stroke-width="3.5" '
               + 'stroke-linejoin="round" style="font-size:11px;fill:' + col + '">' + t + '</text>';
        }

        function pinta(){
          var Lmm = BIELAS[cual];
          var r = Rmm*ESC, L = Lmm*ESC;
          var t = ang;
          var xp = CX + xPiston(t, r, L);                 /* pasador del piston, en px */
          var xPMS = CX + L + r, xPMI = CX + L - r;       /* los dos extremos del recorrido */
          var smm = (L + r - (xp - CX))/ESC;              /* recorrido desde el PMS, en mm */
          var pinx = CX + r*Math.cos(t), piny = CY + r*Math.sin(t);
          var m = '';

          /* --- la bancada --- */
          m += '<path d="M40 ' + CY + ' H' + (xPMS + 30).toFixed(1) + '" stroke="' + LI
             + '" stroke-width="1.2" stroke-dasharray="7 5"></path>';

          /* --- el cilindro: tiene que contener al piston en todo su recorrido --- */
          var xa = xPMI - 22, xb = xPMS + 22, alto = 58;
          m += '<path d="M' + xa.toFixed(1) + ' ' + (CY-alto/2) + ' H' + xb.toFixed(1) + ' V' + (CY+alto/2)
             + ' H' + xa.toFixed(1) + '" fill="var(--surface-2)" stroke="' + GR + '" stroke-width="2.4"></path>';

          /* --- los dos puntos muertos, marcados sobre el cilindro --- */
          m += '<path d="M' + xPMI.toFixed(1) + ' ' + (CY-alto/2-7) + ' V' + (CY+alto/2+7)
             + ' M' + xPMS.toFixed(1) + ' ' + (CY-alto/2-7) + ' V' + (CY+alto/2+7)
             + '" stroke="' + RO + '" stroke-width="1.6" stroke-dasharray="4 4"></path>';
          m += rot(xPMI, CY+alto/2+22, 'PMI', RO, 10.5, 'middle');
          m += rot(xPMS, CY+alto/2+22, 'PMS', RO, 10.5, 'middle');

          /* --- la biela --- */
          m += '<path d="M' + pinx.toFixed(1) + ' ' + piny.toFixed(1) + ' L' + xp.toFixed(1)
             + ' ' + CY + '" stroke="' + GR + '" stroke-width="7" stroke-linecap="round"></path>';

          /* --- el piston --- */
          m += '<rect x="' + (xp-16).toFixed(1) + '" y="' + (CY-alto/2+5) + '" width="32" height="'
             + (alto-10) + '" rx="3" fill="var(--accent-soft)" stroke="' + AZ + '" stroke-width="2.2"></rect>';
          m += '<circle cx="' + xp.toFixed(1) + '" cy="' + CY + '" r="4.5" fill="' + AZ + '"></circle>';

          /* --- la manivela: eje, brazo y mu&ntilde;eta. Nada de disco entero: el disco
                 se meteria dentro del cilindro cuando la biela es corta, que es
                 justo lo que no puede pasar en una maquina de verdad.          */
          m += '<circle cx="' + CX + '" cy="' + CY + '" r="' + r.toFixed(1)
             + '" fill="none" stroke="' + RO + '" stroke-width="1.2" stroke-dasharray="3 4"></circle>';
          m += '<path d="M' + CX + ' ' + CY + ' L' + pinx.toFixed(1) + ' ' + piny.toFixed(1)
             + '" stroke="' + TI + '" stroke-width="8" stroke-linecap="round"></path>';
          m += '<circle cx="' + CX + '" cy="' + CY + '" r="9" fill="var(--surface)" stroke="' + TI
             + '" stroke-width="3"></circle>';
          m += '<circle cx="' + pinx.toFixed(1) + '" cy="' + piny.toFixed(1) + '" r="6" fill="' + RO + '"></circle>';
          m += rot(CX, CY+r+34, 'manivela', GR, 11, 'middle');
          /* la palabra sola: la medida va arriba, con los numeros. Va en el centro
             de la biela y separada 16 px en PERPENDICULAR a ella (hacia arriba),
             que es la unica manera de que no se le monte encima al eje de la
             manivela cuando la biela pasa por delante. */
          var ddx = xp - pinx, ddy = CY - piny, dl = Math.sqrt(ddx*ddx + ddy*ddy);
          m += pegado((pinx + xp)/2 + 16*ddy/dl, (piny + CY)/2 - 16*ddx/dl, 'biela', GR);

          /* --- los numeros --- */
          var enMuerto = Math.abs(Math.sin(t)) < 0.06;
          var grados = Math.round(t*180/Math.PI) % 360;
          m += rot(20, 24, '&aacute;ngulo de la manivela: ' + grados + '&deg;', TI, 12.5);
          m += rot(20, 44, 'manivela r = ' + Rmm + ' mm &middot; biela L = ' + Lmm + ' mm ('
                 + (Lmm/Rmm).toFixed(1) + ' veces r)');
          m += rot(20, 64, 'carrera = 2 &middot; r = ' + (2*Rmm) + ' mm', TI, 12.5);
          m += rot(20, 84, 'el pist&oacute;n lleva ' + smm.toFixed(1) + ' mm recorridos desde el PMS');

          /* --- la grafica: la MISMA funcion, muestreada cada 2 grados --- */
          var GX0 = 62, GX1 = 596, GY0 = 292, GY1 = 352;   /* GY0 = PMS, GY1 = PMI */
          m += '<path d="M' + GX0 + ' ' + GY0 + ' H' + GX1 + ' M' + GX0 + ' ' + GY1 + ' H' + GX1
             + ' M' + GX0 + ' ' + GY0 + ' V' + GY1 + '" stroke="' + LI + '" stroke-width="1.4"></path>';
          m += rot(GX0-8, GY0+4, 'PMS', GR, 10, 'end');
          m += rot(GX0-8, GY1+4, 'PMI', GR, 10, 'end');
          var d = '', k;
          for(k = 0; k <= 180; k++){
            var tt = k*2*Math.PI/180;
            var ss = (L + r - xPiston(tt, r, L))/(2*r);     /* 0 en el PMS, 1 en el PMI */
            d += (k ? 'L' : 'M') + (GX0 + (GX1-GX0)*k/180).toFixed(1) + ' '
               + (GY0 + (GY1-GY0)*ss).toFixed(1) + ' ';
          }
          m += '<path d="' + d + '" fill="none" stroke="' + AZ + '" stroke-width="2.6"></path>';

          /* la media carrera, y el cuarto de vuelta: no se cruzan en el mismo sitio */
          var GYm = (GY0+GY1)/2;
          m += '<path d="M' + GX0 + ' ' + GYm + ' H' + GX1 + '" stroke="' + VE
             + '" stroke-width="1.4" stroke-dasharray="5 5"></path>';
          m += rot(GX1+4, GYm+4, 'media', VE, 10);
          var gx90 = GX0 + (GX1-GX0)/4;
          var s90 = (L + r - xPiston(Math.PI/2, r, L))/(2*r);
          m += '<path d="M' + gx90.toFixed(1) + ' ' + GY0 + ' V' + GY1 + '" stroke="' + RO
             + '" stroke-width="1.4" stroke-dasharray="4 4"></path>';
          m += '<circle cx="' + gx90.toFixed(1) + '" cy="' + (GY0 + (GY1-GY0)*s90).toFixed(1)
             + '" r="4.5" fill="' + RO + '"></circle>';
          m += rot(gx90+9, GY0+15, 'a 90&deg; ya ha hecho el ' + Math.round(s90*100) + ' %', RO, 10.5);

          /* donde esta ahora mismo */
          var gxn = GX0 + (GX1-GX0)*(((t % (2*Math.PI)) + 2*Math.PI) % (2*Math.PI))/(2*Math.PI);
          var sn = (L + r - xPiston(t, r, L))/(2*r);
          m += '<circle cx="' + gxn.toFixed(1) + '" cy="' + (GY0 + (GY1-GY0)*sn).toFixed(1)
             + '" r="5" fill="' + AZ + '"></circle>';
          m += rot(GX0, GY1+20, 'una vuelta entera de la manivela, grado a grado', GR, 10.5);
          m += rot(GX1, GY1+20, '360&deg;', GR, 10.5, 'end');

          svg.innerHTML = m;

          var razon = Lmm/Rmm;
          var txt = 'La mu&ntilde;eta de la manivela describe una circunferencia de <b>' + (2*Rmm)
                  + ' mm de di&aacute;metro</b>, y eso es exactamente la <b>carrera</b> del pist&oacute;n: '
                  + 'no cambia por mucho que alargues la biela. Lo que s&iacute; cambia es <b>c&oacute;mo</b> '
                  + 'se recorre. Con esta biela (L = ' + razon.toFixed(1) + ' &middot; r), a un cuarto de '
                  + 'vuelta el pist&oacute;n ya ha hecho el <b>' + Math.round(s90*100) + ' %</b> del camino, '
                  + 'no la mitad. Por eso la curva de abajo no es sim&eacute;trica.';
          if(enMuerto){
            txt = '<b style="color:var(--goo-rojo)">Punto muerto.</b> Manivela, biela y pist&oacute;n est&aacute;n '
                + 'en l&iacute;nea: por mucho que empujes el pist&oacute;n, la fuerza pasa justo por el eje de '
                + 'giro y <b>no hace girar nada</b>. Un motor pasa de aqu&iacute; gracias al <b>volante</b>, '
                + 'una rueda pesada que guarda la inercia de la vuelta anterior. ' + txt;
          }
          pie.innerHTML = txt;
        }

        function cuadro(ts){
          if(!ultimo) ultimo = ts;
          var dt = Math.min(0.05, (ts - ultimo)/1000);
          ultimo = ts;
          ang = (ang + 1.1*dt) % (2*Math.PI);
          pinta();
          raf = girando ? requestAnimationFrame(cuadro) : null;
        }

        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-b]'); if(!b) return;
          var v = b.dataset.b;
          if(v === 'pausa'){
            girando = !girando;
            b.innerHTML = girando ? '&#9208; Parar' : '&#9654; Seguir';
            if(girando && raf === null){ ultimo = 0; raf = requestAnimationFrame(cuadro); }
            return;
          }
          if(v === 'muerto'){
            ang = 0; girando = false; raf = null;
            seg.querySelector('button[data-b="pausa"]').innerHTML = '&#9654; Seguir';
            pinta(); return;
          }
          cual = v;
          seg.querySelectorAll('button[data-b]').forEach(function(x){
            if(x.dataset.b !== 'pausa' && x.dataset.b !== 'muerto')
              x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          pinta();
        });
        pinta();
        raf = requestAnimationFrame(cuadro);
      })();
      </script>
'''


# ============================================================================
# ESCENA 4.2 - Leva, tornillo-tuerca y pinon-cremallera
# ============================================================================
# La leva se dibuja como una curva polar r(alfa) y la altura del seguidor sale de
# ESA MISMA funcion evaluada en la direccion del seguidor: no hay dos codigos que
# puedan discrepar. El seguidor es de PUNTA y va por la vertical que pasa por el
# centro de giro; solo en ese caso la altura es exactamente r(alfa). Con un
# seguidor de rodillo habria que corregir el perfil, y se dice en la sesion.
ESC_TRANSFORMA = u'''
      <div class="escena" id="esc-transforma">
        <div class="escena-barra">
          <span class="escena-titulo">Tres maneras m&aacute;s de cambiar la naturaleza del movimiento</span>
          <div class="seg" id="seg-transforma">
            <button type="button" data-t="suave" aria-pressed="true">Leva exc&eacute;ntrica</button>
            <button type="button" data-t="prog">Leva de programa</button>
            <button type="button" data-t="golpes">Leva de 4 golpes</button>
            <button type="button" data-t="torn">Tornillo y tuerca</button>
            <button type="button" data-t="crem">Pi&ntilde;&oacute;n y cremallera</button>
            <button type="button" data-t="pausa">&#9208; Parar</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 346" id="svg-transforma" role="img"
               aria-label="Leva con seguidor, tornillo con tuerca y pi&ntilde;&oacute;n con cremallera, con
                           la altura del seguidor y el avance por vuelta calculados"></svg>
        </div>
        <div class="pie" id="pie-transforma"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-transforma');
        var pie = document.getElementById('pie-transforma');
        var seg = document.getElementById('seg-transforma');
        if(!svg) return;

        var AZ = 'var(--goo-azul)', RO = 'var(--goo-rojo)', VE = 'var(--goo-verde)',
            GR = 'var(--ink-soft)', TI = 'var(--ink)', LI = 'var(--line)',
            S2 = 'var(--surface-2)', SU = 'var(--accent-soft)';
        var modo = 'suave', ang = 0, girando = true, raf = null, ultimo = 0;

        function rot(x, y, t, col, tam, anc){
          return '<text x="' + x + '" y="' + y + '" class="rotulo-svg"'
               + (anc ? ' text-anchor="' + anc + '"' : '')
               + ' style="font-size:' + (tam || 11) + 'px;fill:' + (col || GR) + '">' + t + '</text>';
        }
        function norm(a){ a = a % (2*Math.PI); return a < 0 ? a + 2*Math.PI : a; }

        /* ------------- los tres perfiles de leva, en mm de radio --------------
           Los tres con el mismo radio minimo y la misma carrera, para poder
           compararlos: lo unico que cambia es la LEY con la que suben.        */
        /* Base ancha y poca carrera: asi el circulo base se ve como un circulo
           y el lobulo se ve como un escalon pegado a el. Con la base estrecha
           y la carrera grande que habia antes, la pieza sal&iacute;a con forma de
           patata y no se reconoc&iacute;a como una leva.                         */
        var RMIN = 26, H = 18;
        function perfil(a){
          if(modo === 'suave'){
            /* exc&eacute;ntrica de verdad: un circulo con el eje descentrado. Su
               ecuacion polar es LA MISMA que la del piston de la escena anterior. */
            var e = H/2, Rc = RMIN + H/2, s = Math.sin(a);
            return e*Math.cos(a) + Math.sqrt(Rc*Rc - e*e*s*s);
          }
          /* OJO con el sentido. El seguidor toca la leva en alfa = -90 - fase, o
             sea que segun gira la leva va recorriendo su perfil HACIA ATRAS. Si
             el perfil se escribe en alfa a secas, el programa se ejecuta del
             reves: esta leva sub&iacute;a de golpe y ca&iacute;a despacio, justo
             lo contrario de lo que dice el texto. Midiendo g desde la posicion
             de contacto inicial, g ES el angulo girado y el perfil se lee como
             se escribe.                                                        */
          var g = norm(-a - Math.PI/2)*180/Math.PI;
          if(modo === 'prog'){
            /* Reparto: sube 90, se queda arriba 90 (un cuarto de vuelta), cae de
               golpe en 45 y descansa 135 abajo.
               Antes suba 150 y se quedaba arriba 90, o sea que dos tercios de la
               leva estaban al radio maximo y la pieza salia con forma de bulto
               en vez de con forma de leva. Con el descanso de abajo ocupando mas
               de un tercio de la vuelta, el circulo base se ve, y el lobulo
               tambien: la forma vuelve a leerse como el programa que es.       */
            if(g < 30)  return RMIN + H*(1 - Math.cos(Math.PI*g/30))/2;
            if(g < 120) return RMIN + H;
            if(g < 132) return RMIN + H*(1 + Math.cos(Math.PI*(g-120)/12))/2;
            return RMIN;
          }
          /* cuatro lobulos de 50 grados, uno cada 90: la leva del martinete.
             Entre lobulo y lobulo hay 40 grados de reposo, para que cada subida
             se lea como un GOLPE y no como un bamboleo continuo. */
          var d = g % 90; if(d > 45) d -= 90;
          if(Math.abs(d) >= 25) return RMIN;
          return RMIN + H*(1 + Math.cos(Math.PI*d/25))/2;
        }

        function leva(){
          /* Geometria: la leva abajo a la izquierda, el seguidor subiendo por su
             vertical hasta una guia fija, y el muelle entre la guia y el collarin.
             Las alturas estan calculadas para que el muelle se COMPRIMA al subir
             el seguidor (de 56 px estirado a 12 px comprimido) y para que ni la
             leva ni el vastago pisen el bloque de numeros de arriba.           */
          var E = 1.9, cx = 180, cy = 248, m = '', fase = ang;
          var YG = 110;                          /* cara de abajo de la guia fija */
          /* El seguidor esta en la vertical de arriba, o sea en el angulo -90 de
             pantalla. Un punto de la leva de angulo propio alfa se dibuja en
             alfa + fase, asi que el que toca al seguidor es alfa = -90 - fase. */
          var aCont = -Math.PI/2 - fase;
          var hCont = perfil(aCont);
          var yT = cy - hCont*E;                 /* la punta del seguidor */
          var yCol = yT - 38;                    /* cara de arriba del collarin */

          /* --- el perfil, punto a punto --- */
          var d = '', k, a, rr;
          for(k = 0; k <= 720; k++){
            a = k*Math.PI/360; rr = perfil(a)*E;
            d += (k ? 'L' : 'M') + (cx + rr*Math.cos(a + fase)).toFixed(1) + ' '
               + (cy + rr*Math.sin(a + fase)).toFixed(1) + ' ';
          }
          d += 'Z';
          m += '<path d="' + d + '" fill="' + SU + '" stroke="' + AZ + '" stroke-width="2.2"></path>';
          m += '<path d="M' + cx + ' ' + cy + ' L' + (cx + RMIN*E*0.8*Math.cos(fase)).toFixed(1)
             + ' ' + (cy + RMIN*E*0.8*Math.sin(fase)).toFixed(1) + '" stroke="' + TI
             + '" stroke-width="2.4"></path>';
          m += '<circle cx="' + cx + '" cy="' + cy + '" r="6" fill="' + TI + '"></circle>';
          m += rot(cx - (RMIN+H)*E - 10, cy + 4, 'la leva', AZ, 11, 'end');

          /* --- el seguidor: punta, vastago, collarin, guia fija y muelle ---
                 El muelle es el que BAJA al seguidor: la leva solo sabe empujar. */
          m += '<path d="M' + cx + ' ' + yT.toFixed(1) + ' l-7 -13 h14 Z" fill="' + RO + '"></path>';
          m += '<path d="M' + cx + ' ' + (yT-12).toFixed(1) + ' V' + (YG-12) + '" stroke="' + GR
             + '" stroke-width="6" stroke-linecap="round"></path>';
          m += '<rect x="' + (cx-24) + '" y="' + yCol.toFixed(1) + '" width="48" height="12" rx="2" '
             + 'fill="' + S2 + '" stroke="' + GR + '" stroke-width="2"></rect>';
          m += '<rect x="' + (cx-36) + '" y="' + (YG-14) + '" width="72" height="14" fill="' + S2
             + '" stroke="' + GR + '" stroke-width="2"></rect>';
          m += rot(cx+44, YG-2, 'gu&iacute;a fija', GR, 10.5);
          var mu = '';
          for(k = 0; k <= 8; k++){
            mu += (k ? 'L' : 'M') + (cx + (k % 2 ? 13 : -13)) + ' '
                + (YG + (yCol - YG)*k/8).toFixed(1) + ' ';
          }
          m += '<path d="' + mu + '" fill="none" stroke="' + VE + '" stroke-width="2"></path>';
          m += rot(cx+22, (YG + yCol)/2 + 4, 'muelle', VE, 10.5);
          m += rot(cx - 46, (yT + yCol)/2, 'seguidor', RO, 10.5, 'end');

          /* --- la grafica: la MISMA funcion, una vuelta entera --- */
          /* La grafica empieza en 320 y el rotulo es corto a proposito: en un
             movil estrecho el navegador redondea el cuerpo de letra hacia arriba
             y los textos crecen un 20 % largo respecto al viewBox. */
          var GX0 = 320, GX1 = 618, GY0 = 180, GY1 = 300;
          m += '<path d="M' + GX0 + ' ' + GY0 + ' H' + GX1 + ' M' + GX0 + ' ' + GY1 + ' H' + GX1
             + ' M' + GX0 + ' ' + GY0 + ' V' + GY1 + '" stroke="' + LI + '" stroke-width="1.4"></path>';
          var g = '';
          for(k = 0; k <= 180; k++){
            /* el eje de la grafica es el angulo GIRADO, no el propio de la leva */
            var f = k*2*Math.PI/180, hh = perfil(-Math.PI/2 - f);
            g += (k ? 'L' : 'M') + (GX0 + (GX1-GX0)*k/180).toFixed(1) + ' '
               + (GY1 - (GY1-GY0)*(hh-RMIN)/H).toFixed(1) + ' ';
          }
          m += '<path d="' + g + '" fill="none" stroke="' + AZ + '" stroke-width="2.6"></path>';
          m += '<circle cx="' + (GX0 + (GX1-GX0)*(norm(fase)/(2*Math.PI))).toFixed(1) + '" cy="'
             + (GY1 - (GY1-GY0)*(hCont-RMIN)/H).toFixed(1) + '" r="5" fill="' + RO + '"></circle>';
          m += rot(GX0, GY0-12, 'altura del seguidor en una vuelta', TI, 11);
          m += rot(GX0, GY1+18, '0&deg;', GR, 10);
          m += rot(GX1, GY1+18, '360&deg;', GR, 10, 'end');
          m += rot(GX0-6, GY0+4, 'arriba', GR, 10, 'end');
          m += rot(GX0-6, GY1+4, 'abajo', GR, 10, 'end');

          /* --- los numeros, arriba del todo y sin pisar nada --- */
          m += rot(20, 24, 'radio m&iacute;nimo ' + RMIN + ' mm, radio m&aacute;ximo ' + (RMIN+H)
                 + ' mm', TI, 12.5);
          m += rot(20, 44, 'carrera = r m&aacute;x &minus; r m&iacute;n = ' + H + ' mm', TI, 12.5);
          m += rot(20, 62, 'ahora el seguidor toca la leva a ' + hCont.toFixed(1) + ' mm del eje');
          m += rot(20, 80, 'o sea, ' + (hCont-RMIN).toFixed(1)
                 + ' mm por encima de su punto m&aacute;s bajo');
          svg.innerHTML = m;

          if(modo === 'suave'){
            pie.innerHTML = 'Una <b>exc&eacute;ntrica</b>: un disco redondo con el eje descentrado. Sube y baja '
              + 'suave, y la curva de la derecha se parece mucho a la del pist&oacute;n de la escena anterior. '
              + 'No es casualidad: <b>es la misma cuenta</b>. La carrera vale el doble de lo que hayas '
              + 'descentrado el eje.';
          } else if(modo === 'prog'){
            pie.innerHTML = 'Aqu&iacute; est&aacute; la gracia de la leva: <b>la forma es el programa</b>. Esta '
              + 'sube, <b>se queda arriba un cuarto de vuelta</b>, cae de golpe y descansa el resto '
              + 'de la vuelta. Ninguno de '
              + 'los mecanismos anteriores sabe hacer eso: la biela-manivela solo sabe ir y venir siempre igual. '
              + 'Si quieres otro movimiento, <b>recortas otra leva</b>.';
          } else {
            pie.innerHTML = 'Cuatro l&oacute;bulos: <b>cuatro golpes por vuelta</b>. Es la leva del '
              + '<b>martinete</b> de una herrer&iacute;a, movido por una rueda de agua: de las primeras '
              + 'm&aacute;quinas que hicieron un trabajo repetitivo sin un brazo detr&aacute;s.';
          }
        }

        function tornillo(){
          var E = 6, PASO = 5;                  /* px por mm, y mm que avanza por vuelta */
          var p = PASO*E;                       /* el paso, en pixeles */
          var yE = 132, Rc = 15, Rx = 25, XA = 70, XB = 470, m = '';
          var vueltas = ang/(2*Math.PI);
          var avance = vueltas*PASO;

          /* --- el nucleo --- */
          m += '<rect x="' + XA + '" y="' + (yE-Rc) + '" width="' + (XB-XA) + '" height="' + (2*Rc)
             + '" fill="' + S2 + '" stroke="none"></rect>';

          /* --- el filete. La cresta de arriba y la de abajo van desfasadas medio
                 paso: eso es lo que hace que se vea que da la vuelta. Avanza lo
                 mismo que la tuerca, porque la tuerca vive metida en ese surco. */
          var k, xc, fase = (avance*E) % p;
          for(k = -2; k < (XB-XA)/p + 2; k++){
            xc = XA + k*p + fase;
            var a = xc - 0.30*p, b = xc - 0.10*p, c = xc + 0.10*p, e2 = xc + 0.30*p, s = p/2;
            m += '<path d="M' + (a+s).toFixed(1) + ' ' + (yE+Rc) + ' L' + (a+p).toFixed(1) + ' ' + (yE-Rc)
               + '" stroke="' + GR + '" stroke-width="1.1" opacity=".38" stroke-dasharray="3 3"></path>';
            m += '<path d="M' + a.toFixed(1) + ' ' + (yE-Rc) + ' L' + b.toFixed(1) + ' ' + (yE-Rx)
               + ' L' + c.toFixed(1) + ' ' + (yE-Rx) + ' L' + e2.toFixed(1) + ' ' + (yE-Rc)
               + ' L' + (e2+s).toFixed(1) + ' ' + (yE+Rc) + ' L' + (c+s).toFixed(1) + ' ' + (yE+Rx)
               + ' L' + (b+s).toFixed(1) + ' ' + (yE+Rx) + ' L' + (a+s).toFixed(1) + ' ' + (yE+Rc)
               + ' Z" fill="var(--surface)" stroke="' + GR + '" stroke-width="1.5" '
               + 'stroke-linejoin="round"></path>';
          }
          /* se tapa lo que se sale por los dos extremos */
          m += '<rect x="0" y="' + (yE-Rx-3) + '" width="' + XA + '" height="' + (2*Rx+6)
             + '" fill="var(--surface)"></rect>';
          m += '<rect x="' + XB + '" y="' + (yE-Rx-3) + '" width="' + (640-XB) + '" height="' + (2*Rx+6)
             + '" fill="var(--surface)"></rect>';
          m += '<path d="M' + XA + ' ' + (yE-Rc) + ' H' + XB + ' M' + XA + ' ' + (yE+Rc) + ' H' + XB
             + '" stroke="' + GR + '" stroke-width="1.6"></path>';

          /* --- la manivela, a la derecha --- */
          m += '<path d="M' + XB + ' ' + yE + ' H' + (XB+40) + '" stroke="' + GR + '" stroke-width="7"></path>';
          m += '<path d="M' + (XB+40) + ' ' + yE + ' L' + (XB+40) + ' '
             + (yE + 34*Math.cos(ang)).toFixed(1) + '" stroke="' + TI
             + '" stroke-width="5" stroke-linecap="round"></path>';
          m += '<circle cx="' + (XB+40) + '" cy="' + (yE + 34*Math.cos(ang)).toFixed(1)
             + '" r="6" fill="' + RO + '"></circle>';
          m += rot(XB+56, yE-10, 'manivela', GR, 10.5);

          /* --- la tuerca, que es lo que avanza --- */
          var xt = XA + 50 + (avance*E) % (XB - XA - 130);
          m += '<rect x="' + (xt-24).toFixed(1) + '" y="' + (yE-Rx-11) + '" width="48" height="'
             + (2*Rx+22) + '" rx="3" fill="' + SU + '" stroke="' + AZ + '" stroke-width="2.4"></rect>';
          m += rot(xt, yE-Rx-20, 'tuerca', AZ, 10.5, 'middle');
          m += '<path d="M' + (xt+32).toFixed(1) + ' ' + (yE+Rx+32) + ' h42" stroke="' + RO
             + '" stroke-width="3"></path>';
          m += '<path d="M' + (xt+74).toFixed(1) + ' ' + (yE+Rx+32) + ' l-12 -6 v12 Z" fill="' + RO + '"></path>';
          m += rot(xt-32, yE+Rx+36, 'avanza', RO, 10.5, 'end');

          /* --- los numeros: todo sale de paso x vueltas --- */
          m += rot(20, 24, 'paso del tornillo: ' + PASO + ' mm &mdash; lo que avanza en UNA vuelta', TI, 12.5);
          m += rot(20, 44, 'vueltas dadas: ' + vueltas.toFixed(2) + ' &nbsp;&#8594;&nbsp; avance = '
                 + PASO + ' &times; ' + vueltas.toFixed(2) + ' = ' + avance.toFixed(1) + ' mm', TI, 12.5);

          /* --- el gato del coche, con la cuenta hecha --- */
          var Rman = 250, carga = 10000;        /* mm de palanca y newtons de carga */
          var vuelta = 2*Math.PI*Rman;
          var VM = vuelta/PASO, F = carga/VM;
          var v10 = 100/PASO, camino = v10*vuelta/1000;
          var y0 = 236;
          m += '<path d="M20 ' + y0 + ' H620" stroke="' + LI + '" stroke-width="1.4"></path>';
          /* estos cuatro rotulos son los mas largos de toda la unidad: en el
             movil los textos crecen respecto al viewBox, asi que van justos */
          m += rot(20, y0+22, 'EL GATO DEL COCHE &middot; palanca ' + Rman
                 + ' mm, coche de 1.000 kg = 10.000 N', TI, 12);
          m += rot(20, y0+42, 'una vuelta de tu mano son 2&pi; &times; ' + Rman + ' = '
                 + Math.round(vuelta) + ' mm, y el coche sube ' + PASO + ' mm');
          m += rot(20, y0+62, 'ventaja mec&aacute;nica = ' + Math.round(vuelta) + ' / ' + PASO + ' = '
                 + Math.round(VM) + ' &nbsp;&#8594;&nbsp; haces ' + F.toFixed(0) + ' N, unos '
                 + (F/10).toFixed(1) + ' kg', VE, 12);
          m += rot(20, y0+82, 'y lo pagas: ' + v10 + ' vueltas y ' + camino.toFixed(1)
                 + ' m de mano para 10 cm de coche', RO, 12);
          svg.innerHTML = m;

          pie.innerHTML = 'El tornillo-tuerca es el <b>campe&oacute;n en fuerza</b> de todo el tema: '
            + 'multiplica por <b>' + Math.round(VM) + '</b>, as&iacute; que un coche de mil kilos lo levanta '
            + 'cualquiera. Y el precio es el de siempre, pero exagerado: <b>' + camino.toFixed(1)
            + ' metros</b> de mano para diez cent&iacute;metros de coche. Adem&aacute;s <b>no se puede mover '
            + 'al rev&eacute;s</b>: el peso del coche no consigue hacer girar al tornillo. Por eso el coche '
            + 'se queda arriba solo.';
        }

        function cremallera(){
          var E = 2, MOD = 4, Z = 12;           /* px por mm, modulo en mm, dientes */
          var rp = MOD*Z/2;                     /* radio primitivo, en mm */
          var avanceVuelta = Math.PI*MOD*Z;     /* mm que corre la cremallera por vuelta */
          var vueltas = ang/(2*Math.PI);
          var m = '', YP = 150, cx = 320;
          var rpp = rp*E, cy = YP - rpp;
          var pas = 2*Math.PI/Z, p = rpp*pas;   /* el paso, en pixeles */
          /* la fase se deja acotada a una vuelta: como el dibujo se repite cada
             diente y una vuelta son Z dientes exactos, no se ve ning&uacute;n salto */
          var fase = -(ang % (2*Math.PI));
          var yCres = YP - MOD*E, yRaiz = YP + 1.25*MOD*E;
          var XA = 60, XB = 580, alto = 30;

          m += '<rect x="' + XA + '" y="' + yRaiz + '" width="' + (XB-XA) + '" height="' + alto
             + '" fill="' + S2 + '" stroke="' + GR + '" stroke-width="2"></rect>';
          /* el perfil de la cremallera, de un tiron de XA a XB: asi los dientes
             quedan unidos por la linea de fondo, como en la escena 3 */
          var d = '', k, xc, hay = false;
          for(k = -12; k < 34; k++){
            /* los dientes del pinon, desenrollados; el signo es el de la escena 3 */
            xc = cx - rpp*(fase + k*pas - Math.PI/2) + p/2;
            if(xc < XA + 10 || xc > XB - 10) continue;
            if(!hay){ d += 'M' + (XA+2).toFixed(1) + ' ' + yRaiz.toFixed(1) + ' '; hay = true; }
            d += 'L' + (xc - 0.27*p).toFixed(1) + ' ' + yRaiz.toFixed(1)
               + ' L' + (xc - 0.17*p).toFixed(1) + ' ' + yCres.toFixed(1)
               + ' L' + (xc + 0.17*p).toFixed(1) + ' ' + yCres.toFixed(1)
               + ' L' + (xc + 0.27*p).toFixed(1) + ' ' + yRaiz.toFixed(1) + ' ';
          }
          if(hay){
            d += 'L' + (XB-2).toFixed(1) + ' ' + yRaiz.toFixed(1);
            m += '<path d="' + d + '" fill="' + S2 + '" stroke="' + AZ + '" stroke-width="2.2"></path>';
          }

          /* --- el pinon --- */
          var ra = rpp + MOD*E, rf = rpp - 1.25*MOD*E, dd = '';
          for(k = 0; k < Z; k++){
            var t = fase + k*pas;
            var pts = [[t - pas*0.27, rf], [t - pas*0.17, ra], [t + pas*0.17, ra], [t + pas*0.27, rf]];
            for(var j = 0; j < 4; j++){
              dd += (dd === '' ? 'M' : 'L') + (cx + pts[j][1]*Math.cos(pts[j][0])).toFixed(1) + ' '
                  + (cy + pts[j][1]*Math.sin(pts[j][0])).toFixed(1) + ' ';
            }
          }
          dd += 'Z';
          m += '<path d="' + dd + '" fill="' + SU + '" stroke="' + AZ + '" stroke-width="1.6"></path>';
          m += '<circle cx="' + cx + '" cy="' + cy.toFixed(1) + '" r="' + (rpp*0.3).toFixed(1)
             + '" fill="var(--surface)" stroke="' + GR + '" stroke-width="2"></circle>';
          m += '<path d="M' + cx + ' ' + cy.toFixed(1) + ' L' + (cx + rpp*0.85*Math.cos(fase)).toFixed(1)
             + ' ' + (cy + rpp*0.85*Math.sin(fase)).toFixed(1) + '" stroke="' + TI
             + '" stroke-width="2.5"></path>';

          /* --- una escala de milimetros, para leer los tamanos del dibujo --- */
          var yR = yRaiz + alto + 10;
          m += '<path d="M' + XA + ' ' + yR + ' H' + XB + '" stroke="' + GR + '" stroke-width="1.6"></path>';
          for(k = 0; k*10*E <= XB - XA; k++){
            var xx = XA + k*10*E;
            m += '<path d="M' + xx.toFixed(1) + ' ' + yR + ' v' + ((k % 5 === 0) ? 11 : 5)
               + '" stroke="' + GR + '" stroke-width="1.2"></path>';
            if(k % 5 === 0) m += rot(xx, yR+26, k*10, GR, 9.5, 'middle');
          }
          m += rot(XB+4, yR+26, 'mm', GR, 9.5);
          m += rot(XA, yR+44, 'escala del dibujo: mide con ella el di&aacute;metro del pi&ntilde;&oacute;n '
                 + 'y el paso de los dientes', GR, 10.5);

          m += rot(20, 24, 'pi&ntilde;&oacute;n de ' + Z + ' dientes, m&oacute;dulo ' + MOD
                 + ' mm &nbsp;&#8594;&nbsp; di&aacute;metro = ' + MOD + ' &times; ' + Z + ' = '
                 + (MOD*Z) + ' mm', TI, 12.5);
          m += rot(20, 44, 'por vuelta corre su contorno entero: &pi; &times; ' + (MOD*Z) + ' = '
                 + avanceVuelta.toFixed(1) + ' mm', TI, 12.5);
          m += rot(20, 322, 'vueltas: ' + vueltas.toFixed(2) + ' &nbsp;&#8594;&nbsp; la cremallera lleva '
                 + (vueltas*avanceVuelta).toFixed(0) + ' mm recorridos', TI, 12.5);
          svg.innerHTML = m;

          pie.innerHTML = 'Es el &uacute;nico de los cuatro que da un movimiento recto <b>tan largo como '
            + 'quieras</b>: basta con alargar la barra. Y funciona <b>en los dos sentidos</b>: el '
            + 'pi&ntilde;&oacute;n mueve a la cremallera, y la cremallera mueve al pi&ntilde;&oacute;n. Por eso '
            + 'notas los baches de la carretera en el volante. Avance por vuelta: <b>'
            + avanceVuelta.toFixed(1) + ' mm</b>, que es el contorno del pi&ntilde;&oacute;n.';
        }

        function pinta(){
          if(modo === 'torn') return tornillo();
          if(modo === 'crem') return cremallera();
          return leva();
        }

        function cuadro(ts){
          if(!ultimo) ultimo = ts;
          var dt = Math.min(0.05, (ts - ultimo)/1000);
          ultimo = ts;
          ang += (modo === 'torn' ? 1.9 : 0.7)*dt;
          /* los contadores se reinician al dar la vuelta al dibujo, para que el
             numero que se lee y lo que se ve no se separen nunca */
          if(modo === 'torn' && ang > 9*2*Math.PI) ang -= 9*2*Math.PI;
          if(modo === 'crem' && ang > 4*2*Math.PI) ang -= 4*2*Math.PI;
          pinta();
          raf = girando ? requestAnimationFrame(cuadro) : null;
        }

        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-t]'); if(!b) return;
          if(b.dataset.t === 'pausa'){
            girando = !girando;
            b.innerHTML = girando ? '&#9208; Parar' : '&#9654; Seguir';
            if(girando && raf === null){ ultimo = 0; raf = requestAnimationFrame(cuadro); }
            return;
          }
          modo = b.dataset.t; ang = 0;
          seg.querySelectorAll('button[data-t]').forEach(function(x){
            if(x.dataset.t !== 'pausa') x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          pinta();
        });
        pinta();
        raf = requestAnimationFrame(cuadro);
      })();
      </script>
'''


# ============================================================================
# ESCENA 5 - La plantilla de las ruedas de carton
# ============================================================================
# Es la herramienta de la practica, no un adorno: el alumno elige modulo y
# dientes, y la escena le da los numeros con los que va a trazar con compas y
# transportador. Todo sale de d = m*z; no hay ni una medida tabulada.
ESC_PLANTILLA = u'''
      <div class="escena" id="esc-plantilla">
        <div class="escena-barra">
          <span class="escena-titulo">Tu plantilla &middot; elige, y ap&uacute;ntate los n&uacute;meros</span>
          <div class="seg" id="seg-plantilla">
            <button type="button" data-p="m4">m&oacute;dulo 4</button>
            <button type="button" data-p="m5">m&oacute;dulo 5</button>
            <button type="button" data-p="m6" aria-pressed="true">m&oacute;dulo 6</button>
            <button type="button" data-p="z1-">&minus; z1</button>
            <button type="button" data-p="z1+">+ z1</button>
            <button type="button" data-p="z2-">&minus; z2</button>
            <button type="button" data-p="z2+">+ z2</button>
            <button type="button" data-p="gira">&#8635; Comprobar girando</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 424" id="svg-plantilla" role="img"
               aria-label="Dos ruedas dentadas dibujadas a escala con el m&oacute;dulo y el n&uacute;mero de
                           dientes elegidos, con los di&aacute;metros y la distancia entre centros calculados"
               preserveAspectRatio="xMidYMid meet"></svg>
        </div>
        <div class="pie" id="pie-plantilla"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-plantilla');
        var pie = document.getElementById('pie-plantilla');
        var seg = document.getElementById('seg-plantilla');
        if(!svg) return;

        var AZ = 'var(--goo-azul)', RO = 'var(--goo-rojo)', VE = 'var(--goo-verde)',
            GR = 'var(--ink-soft)', TI = 'var(--ink)', LI = 'var(--line)',
            SU = 'var(--accent-soft)';
        var mod = 6, z1 = 12, z2 = 24, ang = 0, girando = false, raf = null, ultimo = 0;

        function rot(x, y, t, col, tam, anc){
          return '<text x="' + x + '" y="' + y + '" class="rotulo-svg"'
               + (anc ? ' text-anchor="' + anc + '"' : '')
               + ' style="font-size:' + (tam || 11) + 'px;fill:' + (col || GR) + '">' + t + '</text>';
        }
        function rueda(cx, cy, z, fase, E){
          /* E: pixeles por milimetro. Proporciones normalizadas: la cabeza del
             diente sale un modulo por fuera de la primitiva y el pie entra 1,25. */
          var rp = mod*z/2*E, ra = rp + mod*E, rf = rp - 1.25*mod*E;
          var pas = 2*Math.PI/z, d = '', k, j;
          for(k = 0; k < z; k++){
            var t = fase + k*pas;
            var pts = [[t - pas*0.27, rf], [t - pas*0.17, ra], [t + pas*0.17, ra], [t + pas*0.27, rf]];
            for(j = 0; j < 4; j++){
              d += (d === '' ? 'M' : 'L') + (cx + pts[j][1]*Math.cos(pts[j][0])).toFixed(1) + ' '
                 + (cy + pts[j][1]*Math.sin(pts[j][0])).toFixed(1) + ' ';
            }
          }
          d += 'Z';
          var m = '<path d="' + d + '" fill="' + SU + '" stroke="' + AZ + '" stroke-width="1.6"></path>';
          /* la circunferencia primitiva: la que de verdad manda */
          m += '<circle cx="' + cx.toFixed(1) + '" cy="' + cy + '" r="' + rp.toFixed(1)
             + '" fill="none" stroke="' + RO + '" stroke-width="1.4" stroke-dasharray="5 4"></circle>';
          m += '<circle cx="' + cx.toFixed(1) + '" cy="' + cy + '" r="4" fill="' + TI + '"></circle>';
          /* la marca que el alumno pinta con boli para contar vueltas */
          m += '<path d="M' + cx.toFixed(1) + ' ' + cy + ' L' + (cx + rp*0.8*Math.cos(fase)).toFixed(1)
             + ' ' + (cy + rp*0.8*Math.sin(fase)).toFixed(1) + '" stroke="' + TI
             + '" stroke-width="2.4"></path>';
          return m;
        }

        function pinta(){
          var d1 = mod*z1, d2 = mod*z2;              /* diametros primitivos, en mm */
          var de1 = d1 + 2*mod, de2 = d2 + 2*mod;    /* diametros exteriores */
          var a = (d1 + d2)/2;                       /* distancia entre centros */
          var paso = Math.PI*mod;                    /* mm de contorno por diente */
          var i = z1/z2;

          /* la escala se calcula para que quepan las dos a lo ancho y la mayor a lo alto */
          var ancho = de1/2 + a + de2/2;
          var E = Math.min(430/ancho, 196/Math.max(de1, de2));
          var cy = 126, cx1 = 320 - a*E/2, cx2 = 320 + a*E/2;
          var m = '';

          m += rueda(cx1, cy, z1, ang, E);
          /* la conducida gira al reves y con la relacion exacta; el desfase mete
             un diente de la motriz en un hueco de la otra */
          m += rueda(cx2, cy, z2, -ang*z1/z2 + Math.PI - Math.PI/z2, E);
          /* Las dos etiquetas van en la MISMA linea de arriba, con una guia hasta
             su rueda: si cada una se pone sobre la suya, la de la peque&ntilde;a
             acaba encima de la grande en cuanto los tama&ntilde;os se separan. */
          var yTop = cy - Math.max(de1, de2)*E/2 - 14;
          m += '<path d="M' + cx1.toFixed(1) + ' ' + (yTop+5) + ' V' + (cy - de1*E/2 - 2).toFixed(1)
             + ' M' + cx2.toFixed(1) + ' ' + (yTop+5) + ' V' + (cy - de2*E/2 - 2).toFixed(1)
             + '" stroke="' + AZ + '" stroke-width="1" stroke-dasharray="3 3" opacity=".55"></path>';
          m += rot(cx1, yTop, 'z1 = ' + z1, AZ, 12.5, 'middle');
          m += rot(cx2, yTop, 'z2 = ' + z2, AZ, 12.5, 'middle');

          var yc = cy + Math.max(de1, de2)*E/2 + 24;
          m += '<path d="M' + cx1.toFixed(1) + ' ' + (yc-6) + ' V' + (yc+6) + ' M' + cx2.toFixed(1)
             + ' ' + (yc-6) + ' V' + (yc+6) + ' M' + cx1.toFixed(1) + ' ' + yc + ' H' + cx2.toFixed(1)
             + '" stroke="' + VE + '" stroke-width="1.6"></path>';
          m += rot((cx1+cx2)/2, yc+18, 'distancia entre centros = ' + a.toFixed(1) + ' mm', VE, 11, 'middle');

          /* --- la chuleta para trazarlas: todo calculado --- */
          m += '<path d="M20 278 H620" stroke="' + LI + '" stroke-width="1.4"></path>';
          m += rot(20, 296, 'PARA TRAZARLAS CON COMP&Aacute;S Y TRANSPORTADOR', TI, 12);
          m += rot(20, 316, 'm&oacute;dulo m = ' + mod + ' mm &nbsp;&middot;&nbsp; paso = &pi; &times; '
                 + mod + ' = ' + paso.toFixed(1) + ' mm de contorno por diente', TI, 12);
          m += rot(20, 338, 'con el comp&aacute;s, en mm: radio primitivo y radio exterior');
          m += rot(20, 358, 'rueda 1 (z1 = ' + z1 + '): ' + (d1/2).toFixed(1) + ' y '
                 + (de1/2).toFixed(1) + ' &middot; un diente cada ' + (360/z1).toFixed(1) + '&deg;');
          m += rot(20, 376, 'rueda 2 (z2 = ' + z2 + '): ' + (d2/2).toFixed(1) + ' y '
                 + (de2/2).toFixed(1) + ' &middot; un diente cada ' + (360/z2).toFixed(1) + '&deg;');
          m += rot(20, 396, 'las dos chinchetas van a ' + a.toFixed(1) + ' mm una de otra', VE, 12);
          m += rot(20, 416, 'i = ' + z1 + ' / ' + z2 + ' = ' + i.toFixed(3) + ' &nbsp;&#8594;&nbsp; '
                 + (1/i).toFixed(2) + ' vueltas de z1 por cada una de z2', TI, 12);
          svg.innerHTML = m;

          var t = 'Las dos ruedas engranan porque tienen el <b>mismo m&oacute;dulo</b>, o sea dientes del '
                + 'mismo tama&ntilde;o. El di&aacute;metro no lo eliges t&uacute;: sale de la cuenta '
                + '<b>d = m &times; z</b> = ' + mod + ' &times; ' + z1 + ' = ' + d1 + ' mm y '
                + mod + ' &times; ' + z2 + ' = ' + d2 + ' mm.';
          if(z1 < 8 || z2 < 8){
            t += ' <b style="color:var(--goo-rojo)">Con tan pocos dientes el hueco sale enorme y la rueda '
               + 'deja de parecer redonda</b>: en cart&oacute;n, de ocho para arriba.';
          }
          pie.innerHTML = t;
        }

        function cuadro(ts){
          if(!ultimo) ultimo = ts;
          var dt = Math.min(0.05, (ts - ultimo)/1000);
          ultimo = ts;
          ang += 0.6*dt;
          pinta();
          raf = girando ? requestAnimationFrame(cuadro) : null;
        }

        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-p]'); if(!b) return;
          var v = b.dataset.p;
          if(v === 'gira'){
            girando = !girando;
            b.innerHTML = girando ? '&#9208; Parar' : '&#8635; Comprobar girando';
            if(girando && raf === null){ ultimo = 0; raf = requestAnimationFrame(cuadro); }
            return;
          }
          if(v.charAt(0) === 'm'){
            mod = +v.slice(1);
            seg.querySelectorAll('button[data-p]').forEach(function(x){
              if(x.dataset.p.charAt(0) === 'm' && x.dataset.p !== 'm')
                x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
            });
          }
          else if(v === 'z1-') z1 = Math.max(6, z1 - 1);
          else if(v === 'z1+') z1 = Math.min(30, z1 + 1);
          else if(v === 'z2-') z2 = Math.max(6, z2 - 1);
          else if(v === 'z2+') z2 = Math.min(48, z2 + 1);
          pinta();
        });
        pinta();
      })();
      </script>
'''


# ============================================================================
# ESCENA 6 - La maquina entera: etapas encadenadas
# ============================================================================
# Recoge el tema: se encadenan etapas, se multiplican las relaciones y se
# comprueba que el producto velocidad x fuerza sale SIEMPRE 1. Cada numero se
# calcula a partir de los dientes, del modulo o del paso.
ESC_CADENA = u'''
      <div class="escena" id="esc-cadena">
        <div class="escena-barra">
          <span class="escena-titulo">Monta la m&aacute;quina &middot; el motor da siempre 1.500 rpm</span>
          <div class="seg" id="seg-cadena">
            <button type="button" data-c="e1">1.&ordf; etapa</button>
            <button type="button" data-c="e2">2.&ordf; etapa</button>
            <button type="button" data-c="sa">Salida</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 330" id="svg-cadena" role="img"
               aria-label="Cadena de mecanismos: motor, dos etapas de transmisi&oacute;n y una de
                           transformaci&oacute;n, con las vueltas y la fuerza calculadas en cada punto"></svg>
        </div>
        <div class="pie" id="pie-cadena"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-cadena');
        var pie = document.getElementById('pie-cadena');
        var seg = document.getElementById('seg-cadena');
        if(!svg) return;

        var AZ = 'var(--goo-azul)', RO = 'var(--goo-rojo)', VE = 'var(--goo-verde)',
            GR = 'var(--ink-soft)', TI = 'var(--ink)', LI = 'var(--line)', S2 = 'var(--surface-2)';
        var RPM = 1500;

        /* Las etapas de TRANSMISION: cada una es una relacion i = z1/z2. */
        var ETAPAS = [
          {n: 'sin nada', c: 'directo', i: 1, d: 'el eje del motor, tal cual'},
          {n: 'reductor 12&#8594;48', c: 'reductor 12&#8594;48', i: 12/48, d: 'z1 = 12, z2 = 48'},
          {n: 'reductor 10&#8594;50', c: 'reductor 10&#8594;50', i: 10/50, d: 'z1 = 10, z2 = 50'},
          {n: 'tornillo sin fin', c: 'sin fin 1&#8594;40', i: 1/40, d: 'rueda de 40 dientes'},
          {n: 'multiplicador 45&#8594;15', c: 'multipl. 45&#8594;15', i: 45/15, d: 'z1 = 45, z2 = 15'}
        ];
        /* Las de TRANSFORMACION: cambian la naturaleza del movimiento. */
        var SALIDAS = [
          {n: 'un eje que gira', c: 'eje que gira', tipo: 'giro'},
          {n: 'pi&ntilde;&oacute;n y cremallera', c: 'pi&ntilde;&oacute;n-cremallera', tipo: 'recto', mod: 2, z: 20},
          {n: 'tornillo y tuerca', c: 'tornillo-tuerca', tipo: 'recto', paso: 2},
          {n: 'biela-manivela', c: 'biela-manivela', tipo: 'vaiv&eacute;n', r: 30}
        ];
        var e1 = 0, e2 = 0, sa = 0;

        function rot(x, y, t, col, tam, anc){
          return '<text x="' + x + '" y="' + y + '" class="rotulo-svg"'
               + (anc ? ' text-anchor="' + anc + '"' : '')
               + ' style="font-size:' + (tam || 11) + 'px;fill:' + (col || GR) + '">' + t + '</text>';
        }
        /* Numero sin ceros de relleno: "200.000" se lee en espanol como doscientos
           mil, y aqui quiere decir doscientos. Con esto sale "200", "0.005" y "1". */
        function num(x, d){
          var s = x.toFixed(d);
          if(s.indexOf('.') >= 0) s = s.replace(/0+$/, '').replace(/\\.$/, '');
          return s;
        }
        function caja(x, y, w, h, titulo, l1, l2, col, tam){
          var m = '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" rx="3" fill="'
                + S2 + '" stroke="' + col + '" stroke-width="2.2"></rect>';
          m += rot(x + w/2, y + 20, titulo, col, 11.5, 'middle');
          if(l1) m += rot(x + w/2, y + 41, l1, TI, tam || 10.5, 'middle');
          if(l2) m += rot(x + w/2, y + 59, l2, GR, 10, 'middle');
          return m;
        }
        function flecha(x1, x2, y, etq){
          var m = '<path d="M' + x1 + ' ' + y + ' H' + (x2-9) + '" stroke="' + GR
                + '" stroke-width="2.4"></path>';
          m += '<path d="M' + x2 + ' ' + y + ' l-11 -6 v12 Z" fill="' + GR + '"></path>';
          /* la etiqueta va DEBAJO de las cajas: entre caja y caja no cabe */
          if(etq) m += rot((x1+x2)/2, 172, etq, TI, 10.5, 'middle');
          return m;
        }

        function pinta(){
          var A = ETAPAS[e1], B = ETAPAS[e2], S = SALIDAS[sa];
          var iTot = A.i*B.i, rpm = RPM*iTot, fuerza = 1/iTot;
          var m = '', Y = 62, H = 78;

          m += caja(16, Y, 92, H, 'MOTOR', RPM + ' rpm', 'fuerza &times; 1', TI);
          m += flecha(108, 148, Y + H/2, '');
          m += caja(148, Y, 144, H, '1.&ordf; ETAPA', A.c, A.d, AZ);
          m += flecha(292, 332, Y + H/2, num(RPM*A.i, 1) + ' rpm');
          m += caja(332, Y, 144, H, '2.&ordf; ETAPA', B.c, B.d, AZ);
          m += flecha(476, 516, Y + H/2, num(rpm, 1) + ' rpm');
          m += caja(516, Y, 112, H, 'SALIDA', S.c, S.tipo, VE, 9.5);

          /* --- lo que sale de verdad, calculado --- */
          var l1, l2;
          if(S.tipo === 'giro'){
            l1 = 'un eje que gira a <b>' + num(rpm, 1) + ' rpm</b>';
            l2 = 'sigue siendo movimiento <b>circular continuo</b>: el mismo que entr&oacute;';
          } else if(S.mod){
            var av = Math.PI*S.mod*S.z;
            l1 = 'la cremallera corre a <b>' + num(av*rpm/1000, 2) + ' m/min</b>';
            l2 = 'avance por vuelta = &pi; &middot; ' + S.mod + ' &middot; ' + S.z + ' = ' + num(av, 1)
               + ' mm, y el movimiento es <b>rectil&iacute;neo</b>';
          } else if(S.paso){
            l1 = 'la tuerca avanza <b>' + num(S.paso*rpm, 1) + ' mm por minuto</b>';
            l2 = 'avance por vuelta = el paso = ' + S.paso + ' mm; movimiento <b>rectil&iacute;neo</b>, '
               + 'y no se deja mover al rev&eacute;s';
          } else {
            l1 = '<b>' + num(rpm, 1) + ' idas y venidas por minuto</b>, de ' + (2*S.r) + ' mm de carrera';
            l2 = 'carrera = 2 &middot; r = 2 &middot; ' + S.r + ' mm; movimiento <b>alternativo</b>';
          }

          /* --- el marcador: el tema entero en tres numeros --- */
          var y0 = 190;
          m += '<path d="M16 ' + y0 + ' H628" stroke="' + LI + '" stroke-width="1.4"></path>';
          m += rot(16, y0+24, 'relaci&oacute;n total = ' + num(A.i, 4) + ' &times; ' + num(B.i, 4)
                 + ' = ' + num(iTot, 5), TI, 12.5);
          m += rot(16, y0+50, 'velocidad &times; ' + num(iTot, 5), iTot < 1 ? RO : VE, 13);
          m += rot(216, y0+50, 'fuerza &times; ' + num(fuerza, 2), iTot < 1 ? VE : RO, 13);
          m += rot(416, y0+50, 'producto = ' + num(Math.round(iTot*fuerza*1000)/1000, 3), TI, 13);
          m += rot(16, y0+76, 'El producto sale 1 siempre, elijas lo que elijas: eso es el tema entero.',
                   GR, 11.5);
          m += rot(16, y0+96, 'En la m&aacute;quina de verdad sale algo menos: el rozamiento se lleva su parte.',
                   GR, 11.5);
          svg.innerHTML = m;

          pie.innerHTML = '<b>' + S.n.charAt(0).toUpperCase() + S.n.slice(1) + '.</b> ' + l1 + '. ' + l2
            + '. La fuerza se ha multiplicado por <b>' + num(fuerza, 2) + '</b> y la velocidad por <b>'
            + num(iTot, 5) + '</b>: uno es justo el inverso del otro, porque <b>ninguna m&aacute;quina '
            + 'regala nada</b>.';
        }

        function etiqueta(b){
          if(b.dataset.c === 'e1') b.innerHTML = '1.&ordf; etapa: ' + ETAPAS[e1].n;
          if(b.dataset.c === 'e2') b.innerHTML = '2.&ordf; etapa: ' + ETAPAS[e2].n;
          if(b.dataset.c === 'sa') b.innerHTML = 'Salida: ' + SALIDAS[sa].n;
        }

        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-c]'); if(!b) return;
          if(b.dataset.c === 'e1') e1 = (e1 + 1) % ETAPAS.length;
          if(b.dataset.c === 'e2') e2 = (e2 + 1) % ETAPAS.length;
          if(b.dataset.c === 'sa') sa = (sa + 1) % SALIDAS.length;
          seg.querySelectorAll('button[data-c]').forEach(etiqueta);
          pinta();
        });
        seg.querySelectorAll('button[data-c]').forEach(etiqueta);
        pinta();
      })();
      </script>
'''


# ============================================================================
# LA AUTOEVALUACION QUE SE CORRIGE SOLA
# ============================================================================
# El CSS no va en tema0_base.py: ese molde lo comparten las siete unidades y
# esto solo lo usa la sesion 6. Se inyecta desde u5_build.py, igual que se hace
# con el CSS del narrador.
#
# La respuesta correcta viaja en el data-ok de cada pregunta, asi que esta en el
# codigo fuente de la pagina. Es una AUTOevaluacion, no un examen: se corrige
# sola porque la idea es que el alumno la use en casa. Para examen, no vale.
CSS_TEST = u"""
.test{background:var(--surface);border:1.5px solid var(--line);border-radius:2px;
  padding:4px 18px 18px;margin:18px 0}
.test ol.test-lista{list-style:none;padding:0;margin:0;counter-reset:tp}
.test .test-p{counter-increment:tp;border-top:1px solid var(--line-soft);padding:16px 0 14px;margin:0}
.test .test-p:first-child{border-top:none}
.test .test-enun{margin:0 0 10px;font-weight:500}
.test .test-enun::before{content:counter(tp) ".";font-family:var(--f-m);color:var(--goo-azul);
  margin-right:8px;font-weight:500}
.test .test-ops{display:grid;gap:6px}
.test .test-ops label{display:flex;gap:10px;align-items:flex-start;padding:8px 11px;cursor:pointer;
  border:1.5px solid var(--line);border-radius:2px;background:var(--surface);font-size:15px}
.test .test-ops label:hover{border-color:var(--goo-azul)}
.test .test-ops input{margin:3px 0 0;flex:none;accent-color:var(--goo-azul)}
.test.hecho .test-ops label{cursor:default}
/* El tinte va en rgba de los hexadecimales de marca, no en color-mix: con una
   capa translucida al 13 % se lee igual sobre el fondo claro y sobre el oscuro,
   y funciona tambien en navegadores viejos de aula. */
.test .op-bien{border-color:var(--goo-verde);background:rgba(52,168,83,.13)}
.test .op-mal{border-color:var(--goo-rojo);background:rgba(234,67,53,.13)}
.test .marca{margin-left:auto;font-family:var(--f-m);font-size:11px;letter-spacing:.08em;
  text-transform:uppercase;white-space:nowrap}
.test .op-bien .marca{color:var(--goo-verde)}
.test .op-mal .marca{color:var(--goo-rojo)}
.test .test-fb{margin:10px 0 0;padding:10px 13px;border-left:4px solid var(--goo-azul);
  background:var(--surface-2);font-size:14.5px}
.test .test-fb p{margin:0}
.test-pie{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin-top:18px;
  padding-top:16px;border-top:2px solid var(--goo-azul)}
.test-pie button{background:var(--goo-azul);border:1.5px solid var(--goo-azul);color:#fff;
  border-radius:2px;padding:9px 18px;font:500 13px var(--f-m);cursor:pointer}
.test-pie button.sec{background:var(--surface);color:var(--goo-azul)}
.test-nota{flex:1;min-width:230px;font-size:14.5px}
.test-nota b.cifra{font-size:22px;font-family:var(--f-m)}
.test-aviso{font-size:13.5px;color:var(--goo-rojo);margin:8px 0 0}
@media print{.test-ops input{display:none}}
"""


MOLDE_TEST = u'''      <div class="test" id="test-u5">
        <ol class="test-lista">
@@PREGUNTAS@@        </ol>
        <div class="test-pie">
          <button type="button" id="test-corrige">Corregir el test</button>
          <button type="button" class="sec" id="test-otra" hidden>Volver a empezar</button>
          <div class="test-nota" id="test-nota" hidden></div>
        </div>
        <p class="test-aviso" id="test-aviso" hidden></p>
      </div>

      <script>
      (function(){
        var caja = document.getElementById('test-u5');
        if(!caja) return;
        var bCor = document.getElementById('test-corrige');
        var bOtra = document.getElementById('test-otra');
        var nota = document.getElementById('test-nota');
        var aviso = document.getElementById('test-aviso');
        var pregs = [].slice.call(caja.querySelectorAll('.test-p'));

        function limpia(){
          caja.classList.remove('hecho');
          pregs.forEach(function(p){
            p.querySelectorAll('label').forEach(function(l){
              l.classList.remove('op-bien', 'op-mal');
              var mm = l.querySelector('.marca'); if(mm) mm.remove();
              var inp = l.querySelector('input');
              inp.disabled = false; inp.checked = false;
            });
            p.querySelector('.test-fb').hidden = true;
          });
          nota.hidden = true; aviso.hidden = true; bOtra.hidden = true; bCor.hidden = false;
          caja.scrollIntoView({behavior: 'smooth', block: 'start'});
        }

        function corrige(){
          var bien = 0, sin = 0, fallos = {}, total = pregs.length;
          pregs.forEach(function(p){
            var ok = +p.dataset.ok, ses = p.dataset.ses;
            var marcada = p.querySelector('input:checked');
            var elegida = marcada ? +marcada.value : -1;
            if(elegida < 0) sin++;
            if(elegida === ok){ bien++; } else { fallos[ses] = (fallos[ses] || 0) + 1; }
            p.querySelectorAll('label').forEach(function(l){
              var v = +l.querySelector('input').value;
              l.querySelector('input').disabled = true;
              if(v === ok){
                l.classList.add('op-bien');
                l.insertAdjacentHTML('beforeend',
                  '<span class="marca">' + (v === elegida ? 'bien' : 'era esta') + '</span>');
              } else if(v === elegida){
                l.classList.add('op-mal');
                l.insertAdjacentHTML('beforeend', '<span class="marca">fallo</span>');
              }
            });
            p.querySelector('.test-fb').hidden = false;
          });
          caja.classList.add('hecho');

          var n = Math.round(1000*bien/total)/100;
          var t = '<b class="cifra">' + n.toFixed(1).replace('.', ',') + '</b> sobre 10 &mdash; '
                + bien + ' de ' + total + ' bien. ';
          var ses = Object.keys(fallos).sort();
          if(!ses.length){
            t += 'Pleno. No te queda nada por repasar de este tema.';
          } else {
            var l = ses.map(function(s){
              return 'la <b>sesi&oacute;n ' + s + '</b> (' + fallos[s]
                   + (fallos[s] > 1 ? ' fallos' : ' fallo') + ')';
            });
            t += 'Vuelve a ' + (l.length > 1 ? l.slice(0, -1).join(', ') + ' y ' + l[l.length-1] : l[0]) + '.';
          }
          nota.innerHTML = t; nota.hidden = false;
          if(sin){
            aviso.textContent = 'Has dejado ' + sin + (sin > 1 ? ' preguntas' : ' pregunta')
                              + ' sin contestar; cuentan como falladas.';
            aviso.hidden = false;
          }
          bCor.hidden = true; bOtra.hidden = false;
        }

        bCor.addEventListener('click', corrige);
        bOtra.addEventListener('click', limpia);
      })();
      </script>
'''


def test(preguntas):
    """preguntas: lista de dicts con ses, enun, ops (lista), ok (indice) y fb."""
    trozos = []
    for n, p in enumerate(preguntas):
        ops = u''
        for j, o in enumerate(p['ops']):
            ops += (u'              <label><input type="radio" name="tp%d" value="%d">'
                    u'<span>%s</span></label>\n' % (n + 1, j, o))
        trozos.append(
            u'          <li class="test-p" data-ok="%d" data-ses="%s">\n'
            u'            <p class="test-enun">%s</p>\n'
            u'            <div class="test-ops">\n%s            </div>\n'
            u'            <div class="test-fb" hidden><p>%s</p></div>\n'
            u'          </li>\n' % (p['ok'], p['ses'], p['enun'], ops, p['fb']))
    return MOLDE_TEST.replace(u'@@PREGUNTAS@@', u''.join(trozos))
