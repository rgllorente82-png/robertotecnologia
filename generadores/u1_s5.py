# -*- coding: utf-8 -*-
"""2.o TyD - U1 - Sesion 5: el taller.

Extraida del HTML publicado el 21-sep-2026. Hasta entonces las sesiones 3 a 6
vivian SOLO en 2eso/TyD/tema1/index.html: u1_build.py las daba por pendientes
y cualquier build las borraba. El cuerpo se guarda tal y como quedo despues de
los afinados, que son idempotentes y se pueden volver a pasar.
"""

S5 = u'''
    <section class="bloque">
      <div class="rotulo"><span class="num">00</span> Antes de empezar &middot; 5 min</div>

      <p>Cinco minutos, y no son burocracia: son los cinco minutos que evitan las dos horas de
         despu&eacute;s. Sobre la mesa, antes de tocar una herramienta:</p>
      <div class="copiar">
        <h3 class="h-menor">Lista de antes de empezar</h3>
        <ul>
          <li>El <b>croquis acotado</b> y la <b>hoja de proceso</b>, a la vista de los dos.</li>
          <li>El material <b>contado</b> contra la lista: si falta algo, se sabe ahora.</li>
          <li>Las <b>gafas</b> puestas y la mesa despejada.</li>
          <li>Un sitio decidido para las <b>piezas terminadas</b>, que si no acaban debajo de un codo.</li>
          <li>Un <b>reloj</b> a la vista: la columna <i>Real</i> hay que rellenarla sobre la marcha, no de memoria al final.</li>
        </ul>
      </div>
      <div class="reto-piensa">
        <span class="n-tag">Treinta segundos</span>
        <p>Mirad vuestro Gantt y decid en voz alta <b>qui&eacute;n empieza con qu&eacute;</b>. Si hay que
           discutirlo ahora, es que el plan no estaba terminado.</p>
      </div>
    </section>

    <section class="bloque">
      <div class="rotulo"><span class="num">01</span> Teor&iacute;a &middot; 15 min</div>

      <h3>Cuatro operaciones, y en este orden</h3>
      <p>Todo lo que vais a hacer hoy es una de estas cuatro cosas: <b>medir y marcar</b>,
         <b>cortar</b>, <b>unir</b> y <b>acabar</b>. Cada una tiene una forma de salir mal.</p>

      <h3>1 &middot; Medir y marcar</h3>
      <p>La regla de carpinter&iacute;a de toda la vida: <b>mide dos veces, corta una</b>. Y dos detalles
         que parecen tonter&iacute;as y no lo son:</p>
      <ul>
        <li>La raya del l&aacute;piz tiene grosor. Un l&aacute;piz normal deja medio mil&iacute;metro, y en
            ocho cortes eso son 8 &times; 0,5 = <b>4 mm</b>: una ranura que ya no aprieta. Por eso se corta
            siempre <b>por fuera de la raya</b>, del lado que se tira.</li>
        <li>Las medidas se toman <b>todas desde el mismo extremo</b>, no una desde cada punta.
            Si encadenas medidas, encadenas errores.</li>
      </ul>
      <p>Se marca con <b>escuadra</b>, apoyando su ala contra el canto de la pieza. Una raya a ojo
         se ve derecha y no lo est&aacute;.</p>

      <h3>2 &middot; Cortar</h3>
      <p>El c&uacute;ter no atraviesa el cart&oacute;n de una pasada, y quien lo intenta lo paga dos veces: se
         desv&iacute;a y encima aplasta la onda. Se hacen <b>tres pasadas</b>. La primera s&oacute;lo marca,
         rompiendo el papel de arriba; la segunda entra en la onda; la tercera termina. Y la regla
         <b>no se mueve entre pasada y pasada</b>, porque si se mueve el corte sale escalonado.</p>
      <p>Para las <b>ranuras</b> hay un truco que ahorra piezas: se cortan los dos lados primero y el
         fondo al final, y el recorte se saca <b>tirando</b>, nunca haciendo palanca con el c&uacute;ter.
         Una ranura empezada por el fondo se abre sola y se lleva la pieza por delante.</p>
      <div class="aviso">
        <span class="n-tag">Los dos &uacute;ltimos cent&iacute;metros</span>
        Casi todos los cortes se estropean al final, cuando el trozo que sobra empieza a colgar y tira
        del papel. Al llegar ah&iacute;, <b>sujeta el recorte con la mano libre</b> y baja el ritmo.
      </div>

      <h3>3 &middot; Unir</h3>
      <p>Y aqu&iacute; viene lo mejor de este proyecto: <b>no hay que unir nada</b>. Las dos piezas se
         sujetan solas porque una entra en la otra. A esa uni&oacute;n se le llama <b>encastre</b>, y no
         lleva ni cola, ni grapas, ni cinta.</p>
      <div class="def">
        <span class="n-tag">Encastre a media madera</span>
        Uni&oacute;n en la que cada pieza lleva una <b>ranura de la mitad de su altura</b>, una desde
        arriba y otra desde abajo, y se cruzan. Se llama as&iacute; desde mucho antes de que hubiera
        cart&oacute;n, porque se hace igual en madera. Aguanta porque <b>trabaja la forma</b>, no el
        pegamento: para separarlas hay que romper una de las dos.
      </div>

      <div class="video" id="video-encastre" data-vid="na5h4AlQTu0">
        <button type="button" class="video-play" aria-label="Reproducir el v&iacute;deo: un &aacute;rbol de Navidad de cart&oacute;n con el mismo encastre">
          <span class="video-tri" aria-hidden="true"></span>
          <span class="video-txt">
            <b>El mismo encastre, con otra silueta</b>
            <span>INNOVANDO IDEAS &middot; &aacute;rbol de Navidad de cart&oacute;n reciclado</span>
          </span>
        </button>
        <p class="video-nota">Es un v&iacute;deo de manualidades, no de clase, y por eso vale: <b>hace
          exactamente lo que acabas de leer</b>. Dos siluetas iguales de cart&oacute;n de una caja, una
          ranura en cada una &mdash;una desde arriba, otra desde abajo&mdash; y se cruzan. Cambia la
          forma del contorno, no la uni&oacute;n. F&iacute;jate en una cosa mientras lo ves: <b>en ning&uacute;n
          momento mide la ranura</b>, la va probando. Con un abeto que solo tiene que quedarse de pie da
          igual; con tu soporte, que tiene que aguantar un m&oacute;vil sin abrirse, no.
          El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce
          sin cookies de seguimiento. Si la red del centro bloquea YouTube,
          <a href="https://www.youtube.com/watch?v=na5h4AlQTu0" target="_blank" rel="noopener">&aacute;brelo
          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material
          publicado bajo la licencia de esta p&aacute;gina.</p>
      </div>
      <p>Que aguante o no depende de un solo n&uacute;mero: <b>el ancho de la ranura</b>. Y ese n&uacute;mero
         no se copia de ning&uacute;n sitio, se mide en tu cart&oacute;n y se prueba en un recorte.</p>

      <div class="escena" id="esc-uniones">
        <div class="escena-barra">
          <span class="escena-titulo">La misma uni&oacute;n, con cuatro soluciones</span>
          <div class="seg" id="seg-uniones">
            <button type="button" data-p="cinta" aria-pressed="true">Solo cinta</button>
            <button type="button" data-p="cola">Solo cola</button>
            <button type="button" data-p="holgado">Ranura holgada</button>
            <button type="button" data-p="justo">Ranura justa</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 300" id="svg-uniones" role="img"
               aria-label="El mismo encastre resuelto con cinta, con cola, con una ranura holgada y con una ranura justa, y c&oacute;mo falla cada uno"></svg>
        </div>
        <div class="pie" id="pie-uniones" role="status" aria-live="polite" aria-atomic="true"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-uniones');
        var pie = document.getElementById('pie-uniones');
        var seg = document.getElementById('seg-uniones');
        if(!svg) return;

        var LIN = 'var(--ink)', SUAVE = 'var(--ink-soft)';
        var VERDE = 'var(--goo-verde)', ROJO = 'var(--goo-rojo)', AMAR = 'var(--goo-amarillo)';

        /* el encastre en cruz, visto de frente: B es la costilla, de canto, y A
           el respaldo con su ranura. Lo que se ensena es que la union depende
           de UN numero: el ancho de la ranura contra el grueso del carton. */
        var AX = 150, AW = 340, AY = 150, AH = 100;     /* la pieza A, de frente */
        var GRUESO = 16;                                /* el carton, a esta escala */

        /* la onda del carton, que es lo que se aplasta cuando la ranura va justa */
        function onda(x, y, w, h){
          var m = '', i;
          for(i = 0; i * 12 < w - 6; i++)
            m += '<path d="M' + (x + 4 + i * 12) + ' ' + (y + 2) + ' q6 ' + (h/2 - 2) + ' 0 ' + (h - 4) +
                 '" stroke="var(--line)" stroke-width="1" fill="none"></path>';
          return m;
        }
        function texto(x,y,s,c,anc,tam){
          return '<text x="' + x + '" y="' + y + '" fill="' + (c||LIN) + '" text-anchor="' + (anc||'middle') +
                 '" font-family="var(--f-m)" font-size="' + (tam||11) + '">' + s + '</text>';
        }
        function flecha(x, y1, y2, c, etiqueta){
          var d = (y2 > y1) ? -9 : 9;
          var m = '<path d="M' + x + ' ' + y1 + ' V' + y2 + '" stroke="' + c + '" stroke-width="2.4"></path>';
          m += '<path d="M' + (x - 6) + ' ' + (y2 + d) + ' L' + x + ' ' + y2 + ' L' + (x + 6) + ' ' + (y2 + d) +
               '" stroke="' + c + '" stroke-width="2.4" fill="none"></path>';
          return m + texto(x + 12, (y1 + y2) / 2, etiqueta, c, 'start', 11);
        }
        /* la costilla B, de canto, entrando por la ranura de A */
        function costilla(hueco, color){
          var x = AX + AW/2 - hueco/2;
          var m = '<rect x="' + (AX + AW/2 - GRUESO/2) + '" y="' + (AY - 66) + '" width="' + GRUESO +
                  '" height="' + (AH + 66) + '" fill="var(--surface)" stroke="' + LIN + '" stroke-width="2.2"></rect>';
          m += onda(AX + AW/2 - GRUESO/2, AY - 66, GRUESO, AH + 66);
          if(hueco > GRUESO){
            m += '<rect x="' + x + '" y="' + (AY + AH - 54) + '" width="' + hueco + '" height="54" fill="' +
                 color + '" opacity=".14"></rect>';
          }
          return m;
        }

        var MODOS = {
          cinta: {
            hueco: GRUESO,
            dibuja: function(){
              var x = AX + AW/2;
              return '<rect x="' + (x - 38) + '" y="' + (AY + AH - 16) + '" width="76" height="10" rx="2" fill="' +
                     ROJO + '" opacity=".45"></rect>' +
                     texto(x + 52, AY + AH - 8, 'una tira de cinta', ROJO, 'start', 10.5);
            },
            veredicto: ['Aguanta una clase', ROJO],
            pie: '<b>Solo cinta.</b> Es lo primero que hace todo el mundo y funciona&hellip; hasta que el soporte lleva un rato en una mochila. La cinta pierde con el calor de la mano y con el polvo del cart&oacute;n, y cuando se despega no avisa: se despega entera de golpe.'
          },
          cola: {
            hueco: GRUESO,
            dibuja: function(){
              var x = AX + AW/2;
              return '<rect x="' + (x - 26) + '" y="' + (AY + AH - 8) + '" width="52" height="7" fill="' +
                     AMAR + '" opacity=".55"></rect>' +
                     texto(x + 40, AY + AH - 2, 'cola en el canto', AMAR, 'start', 10.5);
            },
            veredicto: ['Se lleva el papel', AMAR],
            pie: '<b>Solo cola.</b> El cart&oacute;n es papel con aire dentro, y la cola se mete en la onda en vez de quedarse en la junta. Aguanta m&aacute;s que la cinta, pero al tirar no se despega: <b>se lleva la capa de papel</b> y deja la onda al aire. Y eso ya no tiene arreglo.'
          },
          holgado: {
            hueco: GRUESO + 10,
            dibuja: function(){
              var x = AX + AW/2;
              return flecha(x + 74, AY + AH - 36, AY + AH - 36, AMAR, '') +
                     '<path d="M' + (x + 52) + ' ' + (AY + AH - 30) + ' h26 m-26 12 h26" stroke="' + AMAR +
                     '" stroke-width="2.4"></path>' +
                     texto(x + 84, AY + AH - 22, 'juego: baila', AMAR, 'start', 10.5);
            },
            veredicto: ['Baila', AMAR],
            pie: '<b>Encastre holgado.</b> La ranura sali&oacute; de 6 mm para un cart&oacute;n de 4. Entra suave, da gusto&hellip; y el soporte se mueve. Con el m&oacute;vil encima, ese juego se convierte en balanceo, y el balanceo acaba rompiendo el fondo de la ranura. Una ranura demasiado ancha no se arregla: se corta otra pieza.'
          },
          justo: {
            hueco: GRUESO,
            dibuja: function(){
              var x = AX + AW/2;
              return texto(x + 52, AY + AH - 22, 'entra a presi&oacute;n y ah&iacute; se queda', VERDE, 'start', 10.5);
            },
            veredicto: ['Aguanta, y se desmonta', VERDE],
            pie: '<b>Encastre justo.</b> La ranura mide lo que mide el cart&oacute;n. Entra con un poco de fuerza y ya no se mueve, porque lo que trabaja es <b>la forma</b>, no ning&uacute;n pegamento. Se desmonta cuando quieras y cabe plano en la mochila. Para este soporte, esta.'
          }
        };

        function pinta(k){
          var M = MODOS[k], m = '';
          /* A, de frente, con su ranura: el hueco cambia segun el modo */
          var hx = AX + AW/2 - M.hueco/2;
          m += '<path d="M' + AX + ' ' + AY + ' h' + AW + ' v' + AH + ' h-' + (AX + AW - hx - M.hueco) +
               ' v-54 h-' + M.hueco + ' v54 h-' + (hx - AX) +
               ' Z" fill="var(--surface-2)" stroke="' + LIN + '" stroke-width="2.2" stroke-linejoin="round"></path>';
          m += texto(AX - 8, AY + 26, 'A', SUAVE, 'end', 12);
          m += costilla(M.hueco, M.veredicto[1]);
          m += texto(AX + AW/2, AY - 76, 'B', SUAVE, 'middle', 12);
          m += M.dibuja();
          /* el movil se apoya arriba y empuja hacia atras */
          m += flecha(AX + 56, AY - 50, AY - 10, M.veredicto[1], '');
          m += texto(AX + 68, AY - 34, 'el m&oacute;vil empuja', SUAVE, 'start', 10.5);
          m += '<rect x="20" y="256" width="' + (M.veredicto[0].length * 7.6 + 26) + '" height="26" rx="2" fill="' +
               M.veredicto[1] + '" opacity=".16"></rect>';
          m += texto(33, 273, M.veredicto[0], M.veredicto[1], 'start', 12.5);
          svg.innerHTML = m;
          pie.innerHTML = M.pie;
          seg.querySelectorAll('button').forEach(function(b){
            b.setAttribute('aria-pressed', b.dataset.p === k ? 'true' : 'false');
          });
        }
        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-p]');
          if(b) pinta(b.dataset.p);
        });
        pinta('cinta');
      })();
      </script>

      <p>Si a pesar de todo dais un punto de cola a alguna esquina &mdash;a veces conviene, para que una
         ranura que qued&oacute; un pelo ancha no baile&mdash;, poned <b>poca</b>: el cart&oacute;n se la bebe por
         la onda y la que sobra empapa el papel y lo abomba. Y limpiad la que rebose <b>antes</b> de que
         seque, porque despu&eacute;s no se quita: arranca el papel con ella.</p>

      <h3>4 &middot; Acabar</h3>
      <ul>
        <li>En cart&oacute;n no se lija ni se barniza: se <b>repasan los cantos</b>. Un corte en tres
            pasadas deja pelusa de papel en el borde, y se quita pasando el dedo, no rasc&aacute;ndola
            con el c&uacute;ter.</li>
        <li>Se <b>prueba el encaje antes de forzarlo</b>. Si la costilla no entra con la mano, no
            entra a martillazos: se repasa la ranura con una pasada m&aacute;s, y se vuelve a probar.
            Una ranura se puede ensanchar; no se puede estrechar.</li>
        <li>Se escriben la <b>A</b> y la <b>B</b> en las piezas, y el nombre de los dos en la
            costilla. Parece una tonter&iacute;a hasta que hay veintiocho soportes iguales encima de
            la misma mesa.</li>
      </ul>
    </section>

    <section class="bloque">
      <div class="rotulo"><span class="num">02</span> Taller &middot; 35 min</div>

      <figure class="foto">
        <img src="../../../img/u1-soporte.jpg" width="916" height="690" loading="lazy"
             alt="Primer plano del soporte de m&oacute;vil terminado, de cart&oacute;n: la pieza A hace de respaldo inclinado, la B queda debajo y por delante, y el m&oacute;vil se apoya en las dos. Cada pieza lleva escrita su letra. Detr&aacute;s, desenfocados, la base de corte del taller y recortes de cart&oacute;n">
        <figcaption>As&iacute; queda. Las dos piezas llevan escrita su letra, que es lo que se pide en el
          apartado de acabado: con veintiocho soportes encima de la misma mesa, sin la <b>A</b> y la
          <b>B</b> no hay manera de saber cu&aacute;l es de qui&eacute;n.
          <br><br>Se ve bien la <b>ranura de la pieza A</b>, la que recibe a la B: es un corte
          limpio y recto, del ancho justo. Ah&iacute; se gana o se pierde el proyecto. Y detr&aacute;s,
          desenfocados a prop&oacute;sito, la base de corte y los recortes de cart&oacute;n: no son
          basura, son las <b>pruebas de ranura</b> del paso 6.
          <span class="credito">Roberto P. Garc&iacute;a Llorente &middot; CC BY-SA 4.0</span>
        </figcaption>
      </figure>

      <div class="ficha">
        <div class="ficha-cab">
          <span>Actividad 5 &middot; Construirlo, y anotar lo que de verdad tarda</span>
          <span class="chips"><span class="chip">1.2</span><span class="chip">1.3</span></span>
          <span>Parejas &middot; 35 min</span>
        </div>
        <div class="ficha-cuerpo">
          <h4>Qu&eacute; hay que hacer</h4>
          <ol class="pasos">
            <li>Construir, siguiendo la hoja de proceso <b>en su orden</b>. Si os la salt&aacute;is, apuntad
                por qu&eacute;: eso tambi&eacute;n es informaci&oacute;n.</li>
            <li>Rellenar la columna <b>Real</b> tarea a tarea, con el reloj delante. No al final.</li>
            <li>Cada vez que algo no salga como estaba previsto, una l&iacute;nea en el <b>parte de
                incidencias</b>: qu&eacute; pas&oacute;, qu&eacute; hicisteis y cu&aacute;ntos minutos cost&oacute;.</li>
            <li>Si hay que cambiar una medida, se cambia <b>en el croquis</b> tambi&eacute;n. Un plano que
                no coincide con la pieza es peor que no tener plano.</li>
            <li>Dejar la mesa y las herramientas como estaban. Entra en la nota.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>El objeto est&aacute; montado y se sostiene <b>(2 puntos)</b>.</li>
            <li>Coincide con el croquis, o el croquis se ha corregido <b>(2 puntos)</b>.</li>
            <li>La columna <i>Real</i> est&aacute; rellena tarea a tarea <b>(2 puntos)</b>.</li>
            <li>Hay parte de incidencias, aunque sea para decir que no hubo ninguna <b>(2 puntos)</b>.</li>
            <li>Normas de seguridad y puesto recogido <b>(2 puntos)</b>.</li>
          </ul>
          <div class="aviso" style="margin-top:14px">
            <span class="n-tag">Si algo se rompe</span>
            No es un desastre ni baja la nota por s&iacute; mismo. Lo que cuenta es qu&eacute; hac&eacute;is:
            se apunta en el parte, se decide si se repara o se rehace, y se sigue. Un proyecto sin
            ninguna incidencia anotada casi siempre significa que no se anot&oacute; ninguna.
          </div>
        </div>
      </div>
    </section>

    <section class="bloque">
      <div class="rotulo"><span class="num">03</span> Cierre &middot; 5 min</div>

      <p>Comparad ahora las dos columnas de la hoja de proceso, <i>Previsto</i> y <i>Real</i>. En casi
         todos los grupos la segunda es mayor, y bastante. No es que trabaj&eacute;is despacio: es que
         planificar de memoria sale siempre optimista. Por eso se anota: para que el pr&oacute;ximo Gantt
         sea mejor que este.</p>
      <ol>
        <li>&iquest;Por qu&eacute; se corta por fuera de la raya y no por encima?
          <details class="resp"><summary>Ver respuesta</summary><div class="resp-cuerpo"><p>Porque la raya tiene grosor y la cuchilla tambi&eacute;n. Si cortas por el medio, te comes medio mil&iacute;metro de la pieza buena cada vez; en ocho cortes son 8 &times; 0,5 = <b>4 mm</b>. Se corta del lado del trozo que se tira.</p></div></details></li>
        <li>&iquest;Por qu&eacute; una uni&oacute;n de cart&oacute;n pegada a tope aguanta tan poco?
          <details class="resp"><summary>Ver respuesta</summary><div class="resp-cuerpo"><p>Porque el cart&oacute;n es <b>papel con aire dentro</b>: la cola se mete en la onda en vez de quedarse en la junta, y lo que acaba cediendo no es el pegamento sino el propio cart&oacute;n, que se abre en dos capas. La soluci&oacute;n no es m&aacute;s cola: es unir <b>por la forma</b>, con un encastre.</p></div></details></li>
        <li>&iquest;Por qu&eacute; se prueba la ranura en un recorte antes de cortarla en la pieza buena?
          <details class="resp"><summary>Ver respuesta</summary><div class="resp-cuerpo"><p>Porque el ancho bueno depende del cart&oacute;n que tengas, y una ranura <b>se puede ensanchar pero no estrechar</b>. Si te pasas, la pieza est&aacute; perdida y hay que cortar otra; si te quedas corto, das otra pasada y ya est&aacute;. El recorte cuesta treinta segundos y ahorra una pieza entera.</p></div></details></li>
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya est&aacute; construido. Falta lo &uacute;nico que convierte esto en tecnolog&iacute;a y no en
        manualidades: <b>comprobar si cumple los requisitos que escribisteis el primer d&iacute;a</b>.
        Y contarlo por escrito.
      </div>
    </section>'''
