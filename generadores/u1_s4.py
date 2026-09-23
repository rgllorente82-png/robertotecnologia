# -*- coding: utf-8 -*-
"""2.o TyD - U1 - Sesion 4: el plan y el reparto.

Extraida del HTML publicado el 21-sep-2026. Hasta entonces las sesiones 3 a 6
vivian SOLO en 2eso/TyD/tema1/index.html: u1_build.py las daba por pendientes
y cualquier build las borraba. El cuerpo se guarda tal y como quedo despues de
los afinados, que son idempotentes y se pueden volver a pasar.
"""

S4 = u'''
    <section class="bloque">
      <div class="rotulo"><span class="num">00</span> Reto inicial &middot; 10 min</div>

      <div class="aviso">
        <span class="n-tag">Dos grupos, el mismo soporte</span>
        Mismo croquis, mismo material, misma hora de empezar y las mismas manos. Al acabar la
        sesi&oacute;n, el grupo A tiene el soporte montado y el grupo B tiene una pieza cortada, la otra a
        medias y a dos personas mirando. <b>&iquest;Qu&eacute; ha pasado?</b>
      </div>
      <div class="reto-piensa">
        <span class="n-tag">Cinco minutos, por parejas</span>
        <p>Escribid <b>tres causas posibles</b>, y al lado de cada una, qu&eacute; habr&iacute;a que haber
           hecho antes de entrar al taller para evitarla.</p>
      </div>
      <p>Poned en com&uacute;n. Casi todas las respuestas caen en tres sitios, y ninguno tiene que ver con lo bien que se maneja un c&uacute;ter:</p>
      <ol>
        <li><b>Nadie sab&iacute;a qu&eacute; le tocaba.</b> Cuatro personas alrededor de la misma pieza y
            ninguna con la siguiente preparada.</li>
        <li><b>El orden era imposible.</b> Se intent&oacute; cortar una ranura en una pieza que a&uacute;n no
            ten&iacute;a contorno, o encastrar sin haber probado antes el ancho de la ranura en un recorte.</li>
        <li><b>Nadie cont&oacute; con las esperas.</b> Hay dos bases de corte para quince parejas, y la cola
            tarda lo que tarda: eso no se acelera dando prisa.</li>
      </ol>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; no hace falta copiarlo</span>
        <p>La idea de dibujar el tiempo en barras la populariz&oacute; <b>Henry Gantt</b> hacia 1910, en
           astilleros y f&aacute;bricas donde nadie pod&iacute;a ver de un vistazo qui&eacute;n estaba
           esperando a qui&eacute;n. No fue el primero: el polaco <b>Karol Adamiecki</b> hab&iacute;a
           dibujado lo mismo en 1896, pero lo public&oacute; en polaco y en ruso y casi nadie se
           enter&oacute; &mdash;una lecci&oacute;n aparte sobre para qu&eacute; sirve escribir las cosas&mdash;.
           Los diagramas de Gantt se usaron para construir barcos en la Primera Guerra Mundial y para
           levantar la presa Hoover. Cien a&ntilde;os despu&eacute;s siguen siendo lo mismo: una fila por
           tarea y una barra tan larga como dure.</p>
      </div>
    </section>

    <section class="bloque">
      <div class="rotulo"><span class="num">01</span> Teor&iacute;a &middot; 20 min</div>

      <h3>Planificar es contestar cuatro preguntas por cada tarea</h3>
      <p>Y las cuatro se contestan <b>antes</b> de coger una herramienta, con el croquis delante.</p>

      <div class="copiar">
        <h4>La hoja de proceso</h4>
        <p>Una fila por tarea, y estas columnas:</p>
        <table>
          <thead><tr><th scope="col">N.&ordm;</th><th scope="col">Tarea</th><th scope="col">Qui&eacute;n</th><th scope="col">Herramienta</th><th scope="col">Previsto</th><th scope="col">Real</th></tr></thead>
          <tbody>
            <tr><td>1</td><td>Medir el grueso del cart&oacute;n y escuadrar el trozo</td><td>Los dos</td><td>Calibre y escuadra</td><td>5 min</td><td></td></tr>
            <tr><td>2</td><td>Trazar la pieza A</td><td>A</td><td>Regla, escuadra y l&aacute;piz</td><td>8 min</td><td></td></tr>
            <tr><td>3</td><td>Trazar la pieza B</td><td>B</td><td>Regla, escuadra y l&aacute;piz</td><td>10 min</td><td></td></tr>
            <tr><td>4</td><td>Cortar el contorno de A</td><td>A</td><td>C&uacute;ter y regla met&aacute;lica</td><td>10 min</td><td></td></tr>
            <tr><td>5</td><td>Cortar el contorno de B</td><td>B</td><td>C&uacute;ter y regla met&aacute;lica</td><td>12 min</td><td></td></tr>
            <tr><td>6</td><td>Cortar las dos ranuras y la muesca</td><td>Los dos</td><td>C&uacute;ter y recorte de prueba</td><td>8 min</td><td></td></tr>
            <tr><td>7</td><td><b>Esperar turno de la base de corte</b></td><td>Nadie</td><td>&mdash;</td><td>10 min</td><td></td></tr>
            <tr><td>8</td><td>Montar, medir el &aacute;ngulo y ajustar</td><td>Los dos</td><td>Transportador</td><td>5 min</td><td></td></tr>
          </tbody>
        </table>
        <p>La columna <b>Real</b> se rellena en el taller. Es la que ense&ntilde;a a calcular tiempos, y
           la que casi nadie rellena.</p>
      </div>

      <h3>El orden no es libre</h3>
      <p>Hay tareas que <b>no pueden empezar</b> hasta que otra termine: no se corta lo que no
         est&aacute; trazado, y no se cortan las ranuras de una pieza que todav&iacute;a no tiene contorno.
         A eso se le llama <b>precedencia</b>, y es lo que convierte una lista en un plan.</p>
      <p>Y hay una tarea especial en la tabla de arriba: la n.&ordm; 7. Dura diez minutos y no la
         hace nadie: es la <b>cola de la base de corte</b>, que en el aula hay dos y sois quince
         parejas. Las esperas <b>tambi&eacute;n ocupan tiempo</b>, y un plan que no las dibuje miente.
         Esta adem&aacute;s es de las peores, porque no depende de vosotros: depende de que los de al
         lado terminen.</p>
      <div class="def">
        <span class="n-tag">Diagrama de Gantt</span>
        Dibujo del plan: una fila por tarea y una barra tan larga como dure, sobre una escala de
        tiempo. De un vistazo se ve qu&eacute; se puede hacer a la vez, qui&eacute;n est&aacute; parado y
        cu&aacute;ndo se termina.
      </div>

      <div class="escena" id="esc-gantt">
        <div class="escena-barra">
          <span class="escena-titulo">El mismo soporte, tres planes distintos</span>
          <div class="seg" id="seg-gantt">
            <button type="button" data-p="solo" aria-pressed="true">Uno detr&aacute;s de otro</button>
            <button type="button" data-p="dos">Repartido entre dos</button>
            <button type="button" data-p="retraso">Y si se atasca una tarea</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 300" id="svg-gantt" role="img"
               aria-label="Diagrama de Gantt del montaje del soporte de m&oacute;vil, con las ocho tareas en tres repartos distintos"></svg>
        </div>
        <div class="pie" id="pie-gantt" role="status" aria-live="polite" aria-atomic="true"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-gantt');
        var pie = document.getElementById('pie-gantt');
        var seg = document.getElementById('seg-gantt');
        if(!svg) return;

        /* las ocho tareas de la hoja de proceso, con su duracion en minutos */
        var TAREAS = [
          {c:'1', n:'Medir y escuadrar', d:5},
          {c:'2', n:'Trazar A',          d:8},
          {c:'3', n:'Trazar B',          d:10},
          {c:'4', n:'Cortar A',          d:10},
          {c:'5', n:'Cortar B',          d:12},
          {c:'6', n:'Ranuras y muesca',  d:8},
          {c:'7', n:'Cola de la base',   d:10, espera:true},
          {c:'8', n:'Montar y medir',    d:5}
        ];

        /* cada plan dice a que minuto empieza cada tarea, quien la hace,
           y cuales estan en el camino que decide el final */
        var PLANES = {
          solo: {
            ini:[0,5,13,23,33,45,53,63], quien:['','','','','','','',''],
            rec:['A','A','A','A','A','A','','A'],
            critica:[1,1,1,1,1,1,1,1], fin:68,
            pie:'Una sola persona, una tarea detr&aacute;s de otra: <b>68 minutos</b>. Los 58 de trabajo m&aacute;s los 10 de cola. No cabe en una sesi&oacute;n, y eso se sabe <b>ahora</b> y no a diez minutos del timbre.'
          },
          dos: {
            ini:[0,5,5,13,15,27,35,45], quien:['AB','A','B','A','B','AB','','AB'],
            rec:['AB','A','B','A','B','AB','','AB'],
            critica:[1,0,1,0,1,1,1,1], fin:50,
            pie:'Repartido entre dos: <b>50 minutos</b>, y cabe. Fijaos en <i>Cortar A</i>: acaba en el minuto 23 y no hace falta hasta el 27, as&iacute; que tiene <b>4 minutos de holgura</b>; <i>Trazar A</i> tiene otros 4. Las otras seis, las de barra maciza, no tienen ninguna: si una se retrasa un minuto, el soporte se retrasa un minuto.'
          },
          retraso: {
            ini:[0,5,5,13,15,37,45,55], dur:[5,8,10,10,22,8,10,5],
            quien:['AB','A','B','A','B','AB','','AB'],
            rec:['AB','A','B','A','B','AB','','AB'],
            critica:[1,0,1,0,1,1,1,1], fin:60,
            pie:'Cortar B se complica &mdash;la muesca se rompe y hay que empezar la pieza otra vez&mdash; y tarda <b>22 minutos</b> en vez de 12. Como estaba en el camino cr&iacute;tico, los 10 minutos de m&aacute;s son 10 minutos de m&aacute;s para todos: <b>60</b>. Si se hubiera atascado <i>Cortar A</i>, que ten&iacute;a holgura, no habr&iacute;a pasado casi nada.'
          }
        };

        /* que tarea no puede empezar hasta que acabe cual (por su numero) */
        var ANTES = {2:[1], 3:[1], 4:[2], 5:[3], 6:[4,5], 7:[6], 8:[7]};

        var X0 = 150, X1 = 616, Y0 = 34, ALTO = 22, HUECO = 6, ESCALA = 70;
        function px(min){ return X0 + (X1 - X0) * min / ESCALA; }

        function pinta(k){
          var P = PLANES[k], m = '', i;

          /* eje de minutos */
          for(i = 0; i <= ESCALA; i += 10){
            m += '<path d="M' + px(i).toFixed(1) + ' ' + (Y0 - 12) + ' V' +
                 (Y0 + TAREAS.length * (ALTO + HUECO)) + '" stroke="var(--line)" stroke-width="1"></path>';
            m += '<text x="' + px(i).toFixed(1) + '" y="' + (Y0 - 17) + '" fill="var(--ink-soft)" ' +
                 'text-anchor="middle" font-family="var(--f-m)" font-size="10">' + i + '</text>';
          }
          m += '<text x="' + (X0 - 10) + '" y="' + (Y0 - 17) + '" fill="var(--ink-soft)" text-anchor="end" ' +
               'font-family="var(--f-m)" font-size="10">minutos</text>';

          TAREAS.forEach(function(t, j){
            var y = Y0 + j * (ALTO + HUECO);
            var dur = (P.dur ? P.dur[j] : t.d);
            var x = px(P.ini[j]), w = px(P.ini[j] + dur) - px(0) - (px(P.ini[j]) - px(0)) + 0;
            w = px(P.ini[j] + dur) - px(P.ini[j]);

            m += '<text x="' + (X0 - 10) + '" y="' + (y + ALTO * 0.68) + '" fill="var(--ink)" ' +
                 'text-anchor="end" font-family="var(--f-m)" font-size="11">' + t.c + '. ' + t.n + '</text>';

            /* la barra maciza es la que no tiene holgura y la hueca a trazos la que si:
               asi se distinguen por la forma, que no depende del tema claro u oscuro */
            var relleno = t.espera ? 'var(--goo-amarillo)'
                                   : (P.critica[j] ? 'var(--goo-azul)' : 'var(--surface-2)');
            var borde   = t.espera ? 'var(--goo-amarillo)' : 'var(--goo-azul)';
            var trazos  = (!t.espera && !P.critica[j]) ? ' stroke-dasharray="5 3"' : '';
            m += '<rect x="' + x.toFixed(1) + '" y="' + y + '" width="' + Math.max(w, 3).toFixed(1) +
                 '" height="' + ALTO + '" rx="2" fill="' + relleno + '" stroke="' + borde +
                 '" stroke-width="1.6"' + trazos + ' opacity="' + (t.espera ? '.55' : '1') + '"></rect>';

            var etiqueta = (t.espera ? 'espera' : (P.quien[j] || '')) ;
            if(etiqueta && w > 26){
              /* el rotulo va DENTRO de la barra, asi que su color depende de si
                 la barra esta rellena o hueca, no del tema: los rellenos son
                 claros en oscuro y saturados en claro, y la tinta oscura se lee
                 encima de los dos */
              var tinta = (!t.espera && !P.critica[j]) ? 'var(--ink)' : 'var(--tinta-sobre)';
              m += '<text x="' + (x + w/2).toFixed(1) + '" y="' + (y + ALTO * 0.68) + '" fill="' +
                   tinta + '" text-anchor="middle" ' +
                   'font-family="var(--f-m)" font-size="10">' + etiqueta + '</text>';
            }
          });

          /* la linea del final */
          var yf = Y0 + TAREAS.length * (ALTO + HUECO);
          m += '<path d="M' + px(P.fin).toFixed(1) + ' ' + (Y0 - 12) + ' V' + (yf + 8) +
               '" stroke="var(--goo-rojo)" stroke-width="2" stroke-dasharray="4 3"></path>';
          m += '<text x="' + px(P.fin).toFixed(1) + '" y="' + (yf + 24) + '" fill="var(--goo-rojo)" ' +
               'text-anchor="end" font-family="var(--f-m)" font-size="11.5">termina en ' + P.fin + ' min</text>';
          /* el timbre */
          m += '<path d="M' + px(60).toFixed(1) + ' ' + (Y0 - 12) + ' V' + (yf + 8) +
               '" stroke="var(--ink-soft)" stroke-width="1.4" stroke-dasharray="2 4"></path>';
          m += '<text x="' + (px(60) + 5).toFixed(1) + '" y="' + (yf + 24) + '" fill="var(--ink-soft)" ' +
               'text-anchor="start" font-family="var(--f-m)" font-size="10.5">timbre</text>';

          svg.innerHTML = m;
          pie.innerHTML = P.pie;
          seg.querySelectorAll('button').forEach(function(b){
            b.setAttribute('aria-pressed', b.dataset.p === k ? 'true' : 'false');
          });
        }
        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-p]');
          if(b) pinta(b.dataset.p);
        });
        pinta('solo');
      })();
      </script>

      <h3>Y antes de entrar al taller: las normas</h3>
      <p>No son una lista de prohibiciones: son las cosas que salen mal todos los cursos. Si una te
         parece exagerada, es que a&uacute;n no la has visto pasar.</p>
      <div class="copiar">
        <h4>Siete normas del taller</h4>
        <ol>
          <li>El <b>c&uacute;ter siempre sobre la base de corte</b>, nunca directamente sobre la mesa. Una
              cuchilla que resbala sobre la madera salta, y salta hacia donde no est&aacute;s mirando.</li>
          <li>La regla que gu&iacute;a el corte es <b>met&aacute;lica</b>. Con una de pl&aacute;stico, el c&uacute;ter
              se come el canto y en ese mismo momento se te va la mano por encima.</li>
          <li>La mano que sujeta la regla va <b>detr&aacute;s del filo y con los dedos arqueados</b>, nunca
              estirados por delante. Y se corta <b>hacia fuera</b>, no hacia el cuerpo.</li>
          <li><b>Varias pasadas suaves</b>, nunca una a lo bestia. El cart&oacute;n de 4 mm no se atraviesa
              de una: quien lo intenta aprieta, el c&uacute;ter se desv&iacute;a y sale torcido, o peor.</li>
          <li><b>Cuchilla nueva o reci&eacute;n partida.</b> Una cuchilla roma no corta menos: obliga a
              apretar m&aacute;s, que es justo lo que hace que patine.</li>
          <li>El c&uacute;ter <b>se cierra en cuanto se suelta</b>, aunque sea un segundo, y no se deja en
              el borde de la mesa. Una herramienta en el borde acaba en un pie.</li>
          <li>Si algo se rompe o se atasca, <b>se para y se avisa</b>. Forzar una herramienta atascada
              es la forma m&aacute;s r&aacute;pida de hacerse da&ntilde;o.</li>
        </ol>
      </div>
      <div class="aviso">
        <span class="n-tag">La regla que m&aacute;s se salta</span>
        La herramienta que m&aacute;s respeto da es la m&aacute;s ruidosa, y la que manda gente a la
        enfermer&iacute;a es el <b>c&uacute;ter</b>: peque&ntilde;o, silencioso y casi siempre empujado hacia la
        mano que sujeta. En este proyecto es la <b>&uacute;nica</b> herramienta que corta, as&iacute; que toda
        la seguridad de la unidad cabe en una frase: <b>dedos arqueados detr&aacute;s de la regla y el
        corte hacia fuera</b>.
      </div>
    </section>

    <section class="bloque">
      <div class="rotulo"><span class="num">02</span> Pr&aacute;ctica &middot; 25 min</div>
      <div class="ficha">
        <div class="ficha-cab">
          <span>Actividad 4 &middot; La hoja de proceso y el Gantt de vuestro soporte</span>
          <span class="chips"><span class="chip">1.2</span><span class="chip">1.3</span></span>
          <span>Parejas &middot; 25 min</span>
        </div>
        <div class="ficha-cuerpo">
          <h4>Qu&eacute; hay que hacer</h4>
          <ol class="pasos">
            <li>Partid vuestro montaje en <b>seis u ocho tareas</b>. Ni tres (demasiado gordas para
                repartirlas) ni veinte (no os va a dar tiempo ni a escribirlas).</li>
            <li>Rellenad la <b>hoja de proceso</b> con sus seis columnas. La de <i>Real</i> se deja en blanco.</li>
            <li>Marcad con una flecha qu&eacute; tarea <b>no puede empezar</b> hasta que acabe otra.</li>
            <li>Dibujad el <b>Gantt</b> en papel cuadriculado: un cuadro = dos minutos. Las esperas
                tambi&eacute;n se dibujan.</li>
            <li>Escribid abajo <b>a qu&eacute; minuto termin&aacute;is</b> y qu&eacute; dos tareas son las que
                mandan en esa cifra.</li>
            <li>Y una &uacute;ltima l&iacute;nea: <b>qu&eacute; hay que traer de casa</b>, si hace falta algo.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Las tareas cubren todo el montaje, sin saltos <b>(2 puntos)</b>.</li>
            <li>Cada una tiene responsable, herramienta y tiempo <b>(2 puntos)</b>.</li>
            <li>Las precedencias son correctas: nada se hace antes de lo que puede <b>(2 puntos)</b>.</li>
            <li>El Gantt aprovecha a las dos personas y dibuja las esperas <b>(2 puntos)</b>.</li>
            <li>Dice a qu&eacute; minuto se termina, y sale de las barras <b>(2 puntos)</b>.</li>
          </ul>
          <div class="nota" style="margin-top:14px">
            <span class="n-tag">Si os sale m&aacute;s de una sesi&oacute;n</span>
            No lo maquill&eacute;is bajando los tiempos hasta que cuadre. Eso es exactamente lo que hace
            que un plan no sirva. Lo que se hace es <b>partirlo en dos d&iacute;as</b> y decidir en qu&eacute;
            tarea se corta, o <b>simplificar el dise&ntilde;o</b>. Las dos son respuestas v&aacute;lidas;
            mentirle a la hoja no.
          </div>

      <figure class="foto">
        <img src="../../../img/u1-grupo-mesa.jpg" width="1200" height="800" loading="lazy"
             alt="Cinco j&oacute;venes de pie alrededor de una mesa con hojas extendidas, se&ntilde;alando y
                  discutiendo el trabajo">
        <figcaption>Un plan se discute <b>de pie y sobre el papel</b>, no en la cabeza de uno. Aqu&iacute; est&aacute;n
          en lo que m&aacute;s cuesta: repartir. Mientras nadie diga en voz alta <b>qui&eacute;n</b> hace cada tarea y
          <b>en cu&aacute;ntos minutos</b>, el reparto no existe &mdash; y el d&iacute;a del taller lo acaba haciendo
          todo el mismo.
          <br><br>Foto de <b>Monstera Production</b> en Pexels. Es de su autor y no forma parte del material
          publicado bajo la licencia de esta p&aacute;gina.</figcaption>
      </figure>
        </div>
      </div>
    </section>

    <section class="bloque">
      <div class="rotulo"><span class="num">03</span> Cierre &middot; 5 min</div>

      <p>Comparad los tiempos totales de las distintas parejas. Van a salir muy distintos, con el
         mismo soporte. Eso no significa que unos sean m&aacute;s r&aacute;pidos: significa que unos han
         contado las esperas y otros no.</p>
      <ol>
        <li>&iquest;Por qu&eacute; la espera de turno de la base de corte ocupa una fila del Gantt si no la hace nadie?
          <details class="resp"><summary>Ver respuesta</summary><div class="resp-cuerpo"><p>Porque ocupa <b>tiempo</b>, y el plan es un reparto del tiempo, no del trabajo. Una espera que no est&aacute; dibujada aparece igual, pero por sorpresa y cuando ya no queda sesi&oacute;n.</p></div></details></li>
        <li>&iquest;Qu&eacute; es la holgura de una tarea?
          <details class="resp"><summary>Ver respuesta</summary><div class="resp-cuerpo"><p>Los minutos que puede retrasarse <b>sin retrasar el final</b>. En el ejemplo, <i>Cortar A</i> acaba en el minuto 23 y no hace falta hasta el 27: tiene 4 minutos de holgura. Las tareas sin holgura son las que hay que vigilar.</p></div></details></li>
        <li>Vais dos en el grupo y una tarea la ten&eacute;is que hacer los dos juntos. &iquest;Eso ayuda o estorba?
          <details class="resp"><summary>Ver respuesta</summary><div class="resp-cuerpo"><p>Estorba, salvo que la tarea lo exija de verdad (sujetar mientras el otro encola, por ejemplo). Mientras los dos est&aacute;is en la misma pieza, <b>ninguna otra avanza</b>. Se ve en el Gantt: una fila ocupada y el resto vac&iacute;o.</p></div></details></li>
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya hay croquis, lista de materiales, hoja de proceso y Gantt. Llega la parte que todo el
        mundo cre&iacute;a que era la &uacute;nica: <b>construirlo</b>. Trae la hoja de proceso, porque la
        columna de <i>Real</i> se rellena sobre la marcha.
      </div>
    </section>'''
