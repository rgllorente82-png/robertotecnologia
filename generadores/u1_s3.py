# -*- coding: utf-8 -*-
"""2.o TyD - U1 - Sesion 3: el croquis acotado.

Extraida del HTML publicado el 21-sep-2026. Hasta entonces las sesiones 3 a 6
vivian SOLO en 2eso/TyD/tema1/index.html: u1_build.py las daba por pendientes
y cualquier build las borraba. El cuerpo se guarda tal y como quedo despues de
los afinados, que son idempotentes y se pueden volver a pasar.
"""

S3 = u'''
    <section class="bloque">
      <div class="rotulo"><span class="num">00</span> Reto inicial &middot; 10 min</div>

      <p>Sacad la idea ganadora de ayer, la que est&aacute; escrita en tres l&iacute;neas.</p>
      <div class="aviso">
        <span class="n-tag">Intercambiad la hoja</span>
        Dadle vuestra idea a la pareja de al lado y coged la suya. Ten&eacute;is <b>cinco minutos</b>
        para dibujar exactamente lo que ellos van a construir. Y una regla: <b>no se puede hablar</b>.
        Si hay que explicarlo de palabra, el papel no sirve.
      </div>
      <p>Pasados los cinco minutos, comparad el dibujo que os han hecho con el que ten&eacute;is en la
         cabeza. No se parecen. Y no es porque dibujen mal: es que vuestra hoja no dec&iacute;a
         cu&aacute;ntas piezas hay, ni cu&aacute;nto mide cada una, ni de qu&eacute; son, ni c&oacute;mo se
         sujetan entre ellas.</p>
      <div class="reto-piensa">
        <span class="n-tag">Antes de seguir</span>
        <p>Subrayad en vuestra hoja todas las palabras que <b>otra persona podr&iacute;a entender de dos
           maneras distintas</b>. Casi siempre son casi todas.</p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; no hace falta copiarlo</span>
        <p>El 23 de septiembre de 1999 la NASA perdi&oacute; la sonda <b>Mars Climate Orbiter</b> al llegar a
           Marte. No fall&oacute; ning&uacute;n motor ni ning&uacute;n ordenador: el equipo que fabric&oacute; la
           sonda entregaba los datos de empuje en <b>libras-fuerza</b> y el que la pilotaba los le&iacute;a
           en <b>newtons</b>. Nadie lo hab&iacute;a escrito, porque a cada equipo le parec&iacute;a evidente.
           La sonda entr&oacute; demasiado bajo en la atm&oacute;sfera y se perdi&oacute;: 125 millones de
           d&oacute;lares por una unidad que nadie puso en el papel. Lo que le ha pasado a vuestra hoja
           es exactamente lo mismo, m&aacute;s barato.</p>
      </div>
    </section>

    <section class="bloque">
      <div class="rotulo"><span class="num">01</span> Teor&iacute;a &middot; 20 min</div>

      <h3>Tres dibujos que no son el mismo dibujo</h3>
      <p>En tecnolog&iacute;a no se dibuja una vez: se dibuja tres, y cada dibujo sirve para una cosa
         distinta. Confundirlos es lo que acaba de pasaros.</p>

      <div class="copiar">
        <h4>Boceto, croquis y plano</h4>
        <ul>
          <li><b>Boceto</b> &middot; a mano alzada y <b>sin medidas</b>. Sirve para <b>pensar</b> y para
              ense&ntilde;ar una idea deprisa. Se hacen muchos y se tiran casi todos.</li>
          <li><b>Croquis</b> &middot; a mano alzada tambi&eacute;n, pero <b>con las medidas escritas</b>. Ya no
              sirve para pensar: sirve para <b>decidir</b>. Es lo que se lleva al taller cuando la pieza
              es sencilla.</li>
          <li><b>Plano</b> &middot; a <b>escala</b>, con instrumentos o con el ordenador, acotado y con
              cajet&iacute;n. Es el <b>documento</b>: con &eacute;l, otra persona construye la pieza sin
              preguntarte nada.</li>
        </ul>
        <p><b>Acotar:</b> escribir sobre el dibujo las medidas que hacen falta para fabricarlo, en
           <b>mil&iacute;metros</b>, y cada una <b>una sola vez</b>.</p>
      </div>

      <figure class="foto">
        <img src="../../../img/u1-trazar-carton.jpg" width="1200" height="800" loading="lazy"
             alt="Manos trazando a l&aacute;piz sobre una plancha de cart&oacute;n, con otras piezas ya recortadas al lado,
                  un cutter, una regla met&aacute;lica y una base de corte">
        <figcaption>Esto es un <b>croquis trabajando</b>: las medidas no est&aacute;n en la hoja, est&aacute;n
          ya sobre el cart&oacute;n. Fijaos en lo que hay en la mesa &mdash;regla, cutter y base de corte&mdash; y en
          las piezas del fondo, <b>que salieron de un dibujo anterior</b>. Nadie corta a ojo: se traza primero,
          y se traza con medidas.
          <br><br>Foto de <b>Roxanne Minnish</b> en Pexels. Es de su autor y no forma parte del material
          publicado bajo la licencia de esta p&aacute;gina.</figcaption>
      </figure>
      <div class="nota">
        <span class="n-tag">Esto ya lo trabajaste en el tema 2</span>
        Aqu&iacute; es un recordatorio de tres l&iacute;neas, no materia nueva: las
        <b>vistas</b>, las <b>escalas</b>, las reglas de acotaci&oacute;n y el <b>cajet&iacute;n</b> los diste
        en el <a href="../tema2/">tema 2, <i>Representaci&oacute;n gr&aacute;fica de un proyecto</i></a>, que va antes que este.
        Lo que cambia hoy es para qu&eacute; lo usas: aqu&iacute; el croquis no es el ejercicio, es el papel con el que
        vais a cortar.
      </div>

      <h3>Lo que no se ve en un dibujo bonito: el despiece</h3>
      <p>Un dibujo del conjunto ense&ntilde;a <b>c&oacute;mo queda</b>. Para construir hace falta adem&aacute;s
         saber cu&aacute;ntas piezas hay, de qu&eacute; son y cu&aacute;nto mide cada una. A separar el conjunto
         en sus piezas se le llama <b>despiece</b>, y a la tabla que las lista, <b>lista de materiales</b>.</p>
      <p>Parece burocracia y es justo lo contrario: es la lista de la compra. Sin ella llegas al taller,
         descubres que te falta la mitad del cart&oacute;n y pierdes la sesi&oacute;n entera.</p>

      <div class="copiar">
        <h4>La lista de materiales</h4>
        <p>Una fila por pieza distinta, y estas columnas:</p>
        <table>
          <thead><tr><th scope="col">Pieza</th><th scope="col">Cant.</th><th scope="col">Material</th><th scope="col">Medidas (mm)</th><th scope="col">De d&oacute;nde sale</th></tr></thead>
          <tbody>
            <tr><td>A &middot; respaldo</td><td>1</td><td>Cart&oacute;n de caja, 4 mm</td><td>90 &times; 120</td><td>Caja de folios</td></tr>
            <tr><td>B &middot; costilla</td><td>1</td><td>Cart&oacute;n de caja, 4 mm</td><td>110 &times; 80</td><td>La misma caja</td></tr>
          </tbody>
        </table>
        <p>Es la lista de un <b>soporte de m&oacute;vil</b>: dos piezas de cart&oacute;n que se encastran en cruz,
           una de pie y otra tumbada. Cero tornillos, cero pegamento y cero euros, porque el cart&oacute;n
           sale de una caja que iba a la basura.</p>
        <p>F&iacute;jate en lo corta que es la lista. Eso no es pobreza de proyecto: es una <b>decisi&oacute;n</b>.
           Cada pieza que a&ntilde;ades es una pieza que hay que trazar, cortar, medir y que puede salir mal.</p>
        <p style="margin-bottom:0"><a class="pdf" href="plantilla-soporte.pdf" download>Descargar la plantilla a tama&ntilde;o real (A4)</a></p>
        <p style="font-size:13px;color:var(--ink-soft);margin-top:8px">Es para la sesi&oacute;n de taller,
           no para esta: aqu&iacute; lo que se aprende es <b>de d&oacute;nde sale cada medida</b>. Y ojo, va
           dibujada para cart&oacute;n de 4 mm; si el vuestro mide otra cosa, la ranura hay que ajustarla.</p>
      </div>

      <h3>Las medidas no se inventan: salen de los requisitos</h3>
      <p>Esta es la parte que de verdad distingue el dise&ntilde;o del dibujo. Cada n&uacute;mero del croquis
         tiene que poder contestar a la pregunta <i>&iquest;y por qu&eacute; ese?</i>. Mirad de d&oacute;nde
         salen los del soporte:</p>
      <ul>
        <li><b>&laquo;Que quepa un m&oacute;vil con funda&raquo;</b> &rarr; el m&aacute;s ancho del aula mide
            <b>80 mm</b>. Dejando <b>5 mm</b> de aire a cada lado, las dos piezas miden 80 + 2 &times; 5 =
            <b>90 mm</b> de ancho. Ni una m&aacute;s: el cart&oacute;n que sobra por los lados no sujeta nada
            y s&iacute; estorba en la mochila.</li>
        <li><b>&laquo;Que la pantalla quede entre 60&ordm; y 70&ordm;&raquo;</b> &rarr; el m&oacute;vil se apoya
            abajo en el tope y arriba en el canto de A. Con el respaldo a <b>80 mm</b> de alto y el tope a
            <b>36 mm</b> por delante, sale un poco m&aacute;s de <b>65&ordm;</b>. Y no se discute a ojo: se
            mide con el <b>transportador</b> cuando est&eacute; montado.</li>
        <li><b>&laquo;Que no vuelque al tocar la pantalla&raquo;</b> &rarr; la costilla lleva <b>70 mm</b> de
            cola por detr&aacute;s del respaldo. Con eso el largo de B sale solo: 36 + 4 + 70 =
            <b>110 mm</b>. Los 4 son el grueso del propio cart&oacute;n de A, que tambi&eacute;n ocupa.</li>
        <li><b>&laquo;Que salga de un A4&raquo;</b> &rarr; las dos piezas se trazan sobre un trozo de
            cart&oacute;n del tama&ntilde;o de un folio, que es lo que se saca de cualquier caja. Una encima
            de otra ocupan <b>110 &times; 210 mm</b>, y caben; <b>lado a lado no</b>, porque har&iacute;an
            falta 90 + 110 = 200 mm de ancho y la hoja s&oacute;lo tiene 210 menos los m&aacute;rgenes de la
            impresora. Ese requisito no se discute: se pone la hoja encima y se mira.</li>
        <li><b>&laquo;Que se monte sin pegamento&raquo;</b> &rarr; encastre en cruz. Cada ranura mide de
            ancho <b>lo que mida tu cart&oacute;n</b> &mdash;m&iacute;delo con el calibre, suele andar por los
            4 mm&mdash; y de profundidad la <b>mitad</b> de la altura: 80 &divide; 2 = <b>40 mm</b>. As&iacute;
            las dos piezas se cruzan y quedan a ras.</li>
      </ul>
      <div class="nota">
        <span class="n-tag">La medida que no te van a dar</span>
        El ancho de la ranura no lo pone este croquis, y no es un olvido: el cart&oacute;n de una caja de
        pl&aacute;tanos no mide lo mismo que el de una de folios. Si la haces m&aacute;s ancha que tu cart&oacute;n,
        el soporte <b>baila</b>; si la haces m&aacute;s estrecha, al meterla a la fuerza <b>revientas la onda</b>
        y ya no agarra nunca. M&iacute;delo, y haz una <b>prueba en un recorte</b> antes de tocar la pieza buena.
      </div>
      <div class="aviso">
        <span class="n-tag">Regla</span>
        Una medida que no puedas justificar con un <b>requisito</b> o con una <b>comprobaci&oacute;n</b>
        es una medida inventada. Y las medidas inventadas se descubren siempre, pero tarde: cuando la
        pieza ya est&aacute; cortada.
      </div>

      <div class="escena" id="esc-definicion">
        <div class="escena-barra">
          <span class="escena-titulo">El mismo soporte, en tres niveles de definici&oacute;n</span>
          <div class="seg" id="seg-definicion">
            <button type="button" data-p="boceto" aria-pressed="true">Boceto</button>
            <button type="button" data-p="croquis">Croquis acotado</button>
            <button type="button" data-p="despiece">Despiece</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 300" id="svg-definicion" role="img"
               aria-label="El mismo soporte de m&oacute;vil dibujado como boceto sin medidas, como croquis acotado en mil&iacute;metros y como despiece de sus dos piezas de cart&oacute;n"></svg>
        </div>
        <div class="pie" id="pie-definicion" role="status" aria-live="polite" aria-atomic="true"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-definicion');
        var pie = document.getElementById('pie-definicion');
        var seg = document.getElementById('seg-definicion');
        if(!svg) return;

        /* geometria del soporte, en milimetros. Todas las medidas salen de un
           requisito y estan escritas aqui una sola vez: si cambia el grueso
           del carton, cambia una linea y el dibujo entero se entera.

           La clave del cacharro: A es MAS ALTA que B. Si las dos midieran lo
           mismo, el movil quedaria tumbado. El desnivel entre la muesca de B
           y el canto de A es lo que le da la inclinacion. */
        var MM = {ancho:90, altoA:120, altoB:80, largo:110, cruce:36, cola:70,
                  grueso:4, ranura:40, muesca_x:14, muesca_w:12, muesca_h:10,
                  movil:165, canto_movil:12};
        /* la escala la manda el movil, que con 165 mm es lo mas alto del dibujo */
        var K = 0.95;                           /* pixeles por milimetro */
        var X0 = 96, YB = 238;                  /* el frente de la base, sobre la mesa */
        function mm(v){ return v * K; }
        function px(mx, my){ return [X0 + mx * K, YB - my * K]; }

        var LIN = 'var(--ink)', SUAVE = 'var(--ink-soft)', AZ = 'var(--goo-azul)';

        function linea(x1,y1,x2,y2,c,w,extra){
          return '<path d="M' + x1.toFixed(1) + ' ' + y1.toFixed(1) + ' L' + x2.toFixed(1) + ' ' + y2.toFixed(1) +
                 '" stroke="' + (c||LIN) + '" stroke-width="' + (w||2) + '" fill="none" ' + (extra||'') + '></path>';
        }
        function texto(x,y,s,c,anc,tam){
          return '<text x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" fill="' + (c||LIN) +
                 '" text-anchor="' + (anc||'middle') + '" font-family="var(--f-m)" font-size="' +
                 (tam||11) + '">' + s + '</text>';
        }
        function cotaH(x1,x2,y,s){
          var m = linea(x1,y,x2,y,AZ,1.2) + linea(x1,y-4,x1,y+4,AZ,1.2) + linea(x2,y-4,x2,y+4,AZ,1.2);
          if(x2 - x1 < 42) return m + texto(x2 + 7, y + 3.5, s, AZ, 'start', 10.5);
          m += '<rect x="' + ((x1+x2)/2 - 15) + '" y="' + (y-9) + '" width="30" height="13" fill="var(--surface)"></rect>';
          return m + texto((x1+x2)/2, y+1.5, s, AZ, 'middle', 10.5);
        }
        function cotaV(x,y1,y2,s){
          var m = linea(x,y1,x,y2,AZ,1.2) + linea(x-4,y1,x+4,y1,AZ,1.2) + linea(x-4,y2,x+4,y2,AZ,1.2);
          if(Math.abs(y2 - y1) < 30) return m + texto(x + 7, (y1+y2)/2 + 3.5, s, AZ, 'start', 10.5);
          m += '<rect x="' + (x-15) + '" y="' + ((y1+y2)/2 - 7) + '" width="30" height="13" fill="var(--surface)"></rect>';
          return m + texto(x, (y1+y2)/2 + 3.5, s, AZ, 'middle', 10.5);
        }

        /* PERFIL: visto de lado, que es donde se ve por que funciona */
        function alzado(acotado){
          var m = '';
          var mx1 = MM.muesca_x - MM.muesca_w/2, mx2 = MM.muesca_x + MM.muesca_w/2;
          var fondo = MM.altoB - MM.muesca_h;

          m += linea(X0 - 30, YB, X0 + mm(MM.largo) + 46, YB, 'var(--line)', 1.5);

          /* B, la costilla: rectangulo con la muesca donde apoya el movil */
          var d = 'M' + px(0,0)[0] + ' ' + px(0,0)[1] +
                  ' L' + px(MM.largo,0)[0] + ' ' + px(MM.largo,0)[1] +
                  ' L' + px(MM.largo,MM.altoB)[0] + ' ' + px(MM.largo,MM.altoB)[1] +
                  ' L' + px(mx2,MM.altoB)[0] + ' ' + px(mx2,MM.altoB)[1] +
                  ' L' + px(mx2,fondo)[0] + ' ' + px(mx2,fondo)[1] +
                  ' L' + px(mx1,fondo)[0] + ' ' + px(mx1,fondo)[1] +
                  ' L' + px(mx1,MM.altoB)[0] + ' ' + px(mx1,MM.altoB)[1] +
                  ' L' + px(0,MM.altoB)[0] + ' ' + px(0,MM.altoB)[1] + ' Z';
          m += '<path d="' + d + '" fill="var(--surface-2)" stroke="' + LIN +
               '" stroke-width="2.4" stroke-linejoin="round"></path>';

          /* A, el respaldo, de canto: una tira del grueso del carton */
          m += '<rect x="' + px(MM.cruce,0)[0] + '" y="' + px(0,MM.altoA)[1] + '" width="' + mm(MM.grueso) +
               '" height="' + mm(MM.altoA) + '" fill="' + LIN + '" stroke="' + LIN + '" stroke-width="1.6"></rect>';

          /* la ranura de A, escondida detras de B: linea de trazos */
          m += linea(px(MM.cruce + MM.grueso/2, 0)[0], px(0,0)[1],
                     px(MM.cruce + MM.grueso/2, MM.ranura)[0], px(0,MM.ranura)[1],
                     SUAVE, 1.4, 'stroke-dasharray="4 3"');

          /* el movil: apoya abajo en la muesca y se recuesta en el canto de A */
          var abajo = px(MM.muesca_x, fondo), arriba = px(MM.cruce, MM.altoA);
          var dx = arriba[0]-abajo[0], dy = arriba[1]-abajo[1];
          var L = Math.sqrt(dx*dx+dy*dy), ux = dx/L, uy = dy/L;
          var fin = [abajo[0] + ux*mm(MM.movil), abajo[1] + uy*mm(MM.movil)];
          var nx = -uy*mm(MM.canto_movil), ny = ux*mm(MM.canto_movil);
          m += '<path d="M' + abajo[0].toFixed(1) + ' ' + abajo[1].toFixed(1) +
               ' L' + fin[0].toFixed(1) + ' ' + fin[1].toFixed(1) +
               ' L' + (fin[0]+nx).toFixed(1) + ' ' + (fin[1]+ny).toFixed(1) +
               ' L' + (abajo[0]+nx).toFixed(1) + ' ' + (abajo[1]+ny).toFixed(1) +
               ' Z" fill="none" stroke="' + SUAVE + '" stroke-width="1.8" stroke-dasharray="6 4"></path>';
          m += texto(fin[0] + nx + 10, fin[1] + ny + 4, 'el m&oacute;vil', SUAVE, 'start', 10.5);
          /* las letras, como van escritas en las piezas de verdad */
          var la = px(MM.cruce + MM.grueso/2, MM.altoA - 6);
          m += linea(la[0], la[1], la[0] + 62, la[1] - 30, SUAVE, 1);
          m += texto(la[0] + 66, la[1] - 26, 'A &middot; respaldo, de canto', SUAVE, 'start', 10.5);
          m += texto(px(MM.largo - 18, 0)[0], px(0, MM.altoB/2 - 6)[1], 'B', LIN, 'middle', 13);

          if(acotado){
            m += cotaH(px(0,0)[0], px(MM.cruce,0)[0], YB + 20, '36');
            m += cotaH(px(0,0)[0], px(MM.largo,0)[0], YB + 42, '110');
            m += cotaV(px(MM.largo,0)[0] + 26, px(0,MM.altoB)[1], YB, '80');
            m += cotaV(px(MM.largo,0)[0] + 58, px(0,MM.altoA)[1], YB, '120');
            m += linea(px(MM.cruce+MM.grueso,MM.altoA)[0], px(0,MM.altoA)[1],
                       px(MM.largo,0)[0] + 58, px(0,MM.altoA)[1], 'var(--line)', 1);
            m += cotaH(px(mx1,0)[0], px(mx2,0)[0], px(0,MM.altoB)[1] - 12, '12');
            m += texto(px(0,0)[0] - 12, px(0,fondo)[1] + 4, '10', AZ, 'end', 10.5);
            m += cotaH(px(MM.cruce,0)[0], px(MM.cruce+MM.grueso,0)[0], px(0,MM.altoB)[1] - 30, '4');
          }
          m += texto(px(MM.largo/2, 0)[0], 40, 'PERFIL', SUAVE, 'middle', 10.5);
          return m;
        }

        /* DETALLE: el encastre en cruz, que es toda la union que lleva */
        function detalle(acotado){
          var XD = 470, YD = 92, KK = 0.95;
          var w = MM.ancho*KK, h = MM.altoA*KK, g = MM.grueso*KK, r = MM.ranura*KK;
          var m = '';

          m += '<path d="M' + XD + ' ' + YD + ' h' + w + ' v' + h + ' h-' + ((w-g)/2) + ' v-' + r +
               ' h-' + g + ' v' + r + ' h-' + ((w-g)/2) + ' Z" fill="var(--surface-2)" stroke="' + LIN +
               '" stroke-width="2.2" stroke-linejoin="round"></path>';
          m += texto(XD + w/2, YD - 12, 'A de frente, y B asomando', SUAVE, 'middle', 10.5);

          m += '<rect x="' + (XD + (w-g)/2) + '" y="' + (YD + h - r) + '" width="' + g + '" height="' + (r + 22) +
               '" fill="var(--surface)" stroke="' + LIN + '" stroke-width="2.2"></rect>';

          if(acotado){
            m += cotaV(XD + (w-g)/2 - 20, YD + h - r, YD + h, '40');
            m += cotaH(XD + (w-g)/2, XD + (w+g)/2, YD + h - r - 12, '4');
            m += cotaH(XD, XD + w, YD + h + 44, '90');
          }
          return m;
        }

        function conjunto(acotado){
          var m = alzado(acotado) + detalle(acotado);
          m += linea(440, 30, 440, 282, 'var(--line)', 1);
          m += texto(240, 294, acotado ? 'Cotas en mil&iacute;metros'
                                       : 'Sin una sola medida: todav&iacute;a es una idea', SUAVE, 'middle', 10.5);
          return m;
        }

        /* las dos piezas, planas, como hay que trazarlas en el carton */
        function despiece(){
          var KK = 1.32, m = '';
          var wA = MM.ancho*KK, hA = MM.altoA*KK, g = MM.grueso*KK, r = MM.ranura*KK;
          var wB = MM.largo*KK, hB = MM.altoB*KK;
          var mx1 = (MM.muesca_x - MM.muesca_w/2)*KK, mx2 = (MM.muesca_x + MM.muesca_w/2)*KK,
              mh = MM.muesca_h*KK;

          var ax = 74, ay = 56;
          m += '<path d="M' + ax + ' ' + ay + ' h' + wA + ' v' + hA + ' h-' + ((wA-g)/2) + ' v-' + r +
               ' h-' + g + ' v' + r + ' h-' + ((wA-g)/2) + ' Z" fill="var(--surface-2)" stroke="' + LIN +
               '" stroke-width="2.2" stroke-linejoin="round"></path>';
          m += texto(ax + wA/2, ay + hA + 24, 'A &middot; respaldo', LIN, 'middle', 11.5);
          m += texto(ax + wA/2, ay + hA + 38, '&times; 1 &middot; 90 &times; 120 &middot; cart&oacute;n 4', SUAVE, 'middle', 10);

          var bx = 330, by = 96, cr = (MM.cruce - MM.grueso/2)*KK, cr2 = (MM.cruce + MM.grueso/2)*KK;
          m += '<path d="M' + bx + ' ' + by + ' h' + mx1 + ' v' + mh + ' h' + (mx2-mx1) + ' v-' + mh +
               ' h' + (cr - mx2) + ' v' + r + ' h' + g + ' v-' + r + ' h' + (wB - cr2) +
               ' v' + hB + ' h-' + wB + ' Z" fill="var(--surface-2)" stroke="' + LIN +
               '" stroke-width="2.2" stroke-linejoin="round"></path>';
          m += texto(bx + wB/2, by + hB + 24, 'B &middot; costilla', LIN, 'middle', 11.5);
          m += texto(bx + wB/2, by + hB + 38, '&times; 1 &middot; 110 &times; 80 &middot; cart&oacute;n 4', SUAVE, 'middle', 10);

          m += texto(320, 294, 'Dos piezas distintas, dos en total: la muesca de B es donde se sienta el m&oacute;vil', SUAVE, 'middle', 10.5);
          return m;
        }

        var MODOS = {
          boceto:   {pinta: function(){ return conjunto(false); },
                     pie: 'El <b>boceto</b> se dibuja a mano alzada y sin medidas. Sirve para pensar y para ense&ntilde;ar la idea en diez segundos. Con esto no se puede construir: no dice cu&aacute;nto mide nada. <i>(Aqu&iacute; va con l&iacute;neas limpias para que se lea en pantalla; en tu cuaderno va a pulso, y da igual que tiemble.)</i>'},
          croquis:  {pinta: function(){ return conjunto(true); },
                     pie: 'El <b>croquis acotado</b> es el mismo dibujo con los n&uacute;meros puestos, en mil&iacute;metros y cada uno una sola vez. Los 90 salen de 80 + 2 &times; 5; los 110, de 36 + 4 + 70; los 40 de la ranura, de 80 &divide; 2. Ya se puede cortar. Tambi&eacute;n va <b>a mano alzada</b>: lo que tiene que estar bien son las cotas, no el pulso.'},
          despiece: {pinta: despiece,
                     pie: 'El <b>despiece</b> es lo que hay que trazar en el cart&oacute;n: dos piezas, planas, con su ranura. Aqu&iacute; se ve que la ranura de A sube desde abajo y la de B baja desde arriba; si las dos fueran por el mismo lado, no habr&iacute;a manera de cruzarlas.'}
        };

        function pinta(k){
          svg.innerHTML = MODOS[k].pinta();
          pie.innerHTML = MODOS[k].pie;
          seg.querySelectorAll('button').forEach(function(b){
            b.setAttribute('aria-pressed', b.dataset.p === k ? 'true' : 'false');
          });
        }
        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-p]');
          if(b) pinta(b.dataset.p);
        });
        pinta('boceto');
      })();
      </script>
    </section>

    <section class="bloque">
      <div class="rotulo"><span class="num">02</span> Pr&aacute;ctica &middot; 25 min</div>
      <div class="ficha">
        <div class="ficha-cab">
          <span>Actividad 3 &middot; El croquis acotado y la lista de piezas</span>
          <span class="chips"><span class="chip">1.2</span><span class="chip">2.1</span></span>
          <span>Parejas &middot; 25 min</span>
        </div>
        <div class="ficha-cuerpo">
          <h4>Qu&eacute; hay que hacer</h4>
          <ol class="pasos">
            <li>Un <b>croquis del conjunto</b>, a mano alzada, con las tres medidas generales: alto, ancho y fondo.</li>
            <li>Un <b>croquis de cada pieza distinta</b>, acotada en mil&iacute;metros. Cada medida, una sola vez.</li>
            <li>La <b>lista de materiales</b> completa, con las cinco columnas: pieza, cantidad, material, medidas y de d&oacute;nde sale.</li>
            <li>Debajo, una l&iacute;nea por cada medida general diciendo <b>de qu&eacute; requisito sale</b>.
                Si alguna no sale de ninguno, o sobra el n&uacute;mero o falta el requisito.</li>
            <li>Volved a pas&aacute;rselo a la pareja de al lado, otra vez <b>sin hablar</b>. Si ahora s&iacute;
                dibujan lo que ten&eacute;is en la cabeza, est&aacute; terminado.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Est&aacute;n todas las piezas y las cantidades cuadran con el croquis <b>(2 puntos)</b>.</li>
            <li>Las cotas est&aacute;n en mil&iacute;metros y ninguna se repite <b>(2 puntos)</b>.</li>
            <li>Cada medida general est&aacute; justificada con un requisito <b>(3 puntos)</b>.</li>
            <li>La lista de materiales dice el material y la medida comercial <b>(2 puntos)</b>.</li>
            <li>La otra pareja reconoce el objeto sin preguntar nada <b>(1 punto)</b>.</li>
          </ul>
          <div class="nota" style="margin-top:14px">
            <span class="n-tag">La prueba de que est&aacute; bien</span>
            No es que quede bonito: es que <b>otra persona lo entienda sin vosotros delante</b>. Ese es
            el trabajo entero de esta sesi&oacute;n, y la raz&oacute;n de que exista el dibujo t&eacute;cnico.
          </div>
        </div>
      </div>
    </section>

    <section class="bloque">
      <div class="rotulo"><span class="num">03</span> Cierre &middot; 5 min</div>

      <p>Hace dos sesiones ten&iacute;ais una frase. Ahora ten&eacute;is un papel con el que otro puede
         ponerse a cortar. Entre una cosa y otra no ha habido ninguna idea nueva: solo decisiones
         tomadas y escritas.</p>
      <ol>
        <li>&iquest;En qu&eacute; se diferencian un boceto y un croquis?
          <details class="resp"><summary>Ver respuesta</summary><div class="resp-cuerpo"><p>En las <b>medidas</b>. Los dos van a mano alzada, pero el boceto sirve para pensar y el croquis para decidir: lleva las cotas escritas, en mil&iacute;metros.</p></div></details></li>
        <li>&iquest;Para qu&eacute; sirve la lista de materiales si el croquis ya lo ense&ntilde;a todo?
          <details class="resp"><summary>Ver respuesta</summary><div class="resp-cuerpo"><p>El croquis ense&ntilde;a c&oacute;mo queda; la lista dice <b>qu&eacute; hay que traer</b>: cu&aacute;ntas piezas, de qu&eacute; material y de qu&eacute; medida comercial. Es la lista de la compra, y sin ella se pierde una sesi&oacute;n de taller.</p></div></details></li>
        <li>La pieza B del ejemplo mide 110 mm de largo. &iquest;De d&oacute;nde sale ese n&uacute;mero?
          <details class="resp"><summary>Ver respuesta</summary><div class="resp-cuerpo"><p>De tres requisitos sumados: 36 mm por delante del respaldo &mdash;lo que hace falta para que la pantalla quede a 66&ordm;&mdash;, m&aacute;s los 4 mm que ocupa el cart&oacute;n del propio respaldo, m&aacute;s 70 mm de cola por detr&aacute;s para que no vuelque al tocar la pantalla. 36 + 4 + 70 = <b>110 mm</b>. Ninguna medida se inventa.</p></div></details></li>
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya sab&eacute;is <b>qu&eacute;</b> hay que construir. Falta lo otro: qui&eacute;n hace cada cosa, con
        qu&eacute; herramienta, en qu&eacute; orden y en cu&aacute;ntos minutos. Sin eso, el grupo que mejor
        dise&ntilde;a puede ser el que no termina.
      </div>
    </section>'''
