# -*- coding: utf-8 -*-
"""2.o TyD - U1 - Sesion 6: el ensayo y la memoria.

Extraida del HTML publicado el 21-sep-2026. Hasta entonces las sesiones 3 a 6
vivian SOLO en 2eso/TyD/tema1/index.html: u1_build.py las daba por pendientes
y cualquier build las borraba. El cuerpo se guarda tal y como quedo despues de
los afinados, que son idempotentes y se pueden volver a pasar.
"""

S6 = u'''
    <section class="bloque">
      <div class="rotulo"><span class="num">00</span> El ensayo &middot; 15 min</div>

      <p>Sacad la hoja del primer d&iacute;a, la de los ocho requisitos. Hoy no se opina sobre el soporte: se le hacen pruebas.</p>
      <div class="copiar">
        <h3 class="h-menor">C&oacute;mo se hace una prueba de verdad</h3>
        <ul>
          <li>Con <b>el m&oacute;vil de verdad</b>, no con uno cualquiera. Si el requisito dec&iacute;a 165 mm
              y 12 mm con funda, se prueba con ese, y si en la clase hay uno m&aacute;s grande, tambi&eacute;n
              con ese. Un soporte que s&oacute;lo aguanta el m&oacute;vil de quien lo hizo no cumple.</li>
          <li>Se <b>mide</b>, no se opina: el &aacute;ngulo con el transportador apoyado en la mesa. Un
              n&uacute;mero vale m&aacute;s que un &laquo;parece que est&aacute; bien&raquo;, y adem&aacute;s se puede
              comparar con el de otra pareja.</li>
          <li>Se prueba <b>lo que va a pasar de verdad</b>: pulsar la pantalla con el dedo, que es
              cuando vuelcan. Se empuja en la parte de arriba, despacio, y se mira si se levanta la
              cola de la costilla.</li>
          <li>Y se prueba lo aburrido: <b>montarlo y desmontarlo cinco veces</b>. Si a la quinta la
              ranura ya no aprieta, el soporte no dura un trimestre, y eso hay que escribirlo.</li>
        </ul>
      </div>
      <div class="reto-piensa">
        <span class="n-tag">Antes de cargar</span>
        <p>Escribid <b>qu&eacute; esper&aacute;is que pase</b>. Luego comparadlo con lo que pasa. Acertar es
           se&ntilde;al de que entend&eacute;is vuestro propio dise&ntilde;o; fallar es la parte interesante.</p>
      </div>
      <p>Y despu&eacute;s de la carga, los requisitos que no son de aguantar: &iquest;cabe en el pasillo que
         dijisteis? &iquest;se pone y se quita sin herramientas? &iquest;se ha hecho alg&uacute;n agujero en la
         pared? Cada uno, con su s&iacute; o su no.</p>
    </section>

    <section class="bloque">
      <div class="rotulo"><span class="num">01</span> Teor&iacute;a &middot; 15 min</div>

      <h3>Evaluar no es opinar</h3>
      <p>Evaluar es comparar lo construido con los <b>requisitos del paso 2</b>, uno a uno, y escribir
         el resultado. Si los requisitos estaban bien escritos &mdash;comprobables, ya sab&eacute;is&mdash;,
         esto se hace sin discutir. Si no lo estaban, hoy se nota.</p>

      <div class="copiar">
        <h4>La tabla de evaluaci&oacute;n</h4>
        <table>
          <thead><tr><th scope="col">Requisito</th><th scope="col">C&oacute;mo se comprueba</th><th scope="col">Resultado</th><th scope="col">&iquest;Cumple?</th></tr></thead>
          <tbody>
            <tr><td>Sujeta un m&oacute;vil de 165 &times; 80 &times; 12</td><td>Probarlo con tres m&oacute;viles</td><td>Los tres aguantan</td><td>S&iacute;</td></tr>
            <tr><td>La pantalla queda entre 60&ordm; y 70&ordm;</td><td>Transportador sobre la mesa</td><td>66&ordm;</td><td>S&iacute;</td></tr>
            <tr><td>No vuelca al pulsar la pantalla</td><td>Empujar arriba con un dedo</td><td>No se levanta</td><td>S&iacute;</td></tr>
            <tr><td>Se monta y desmonta sin herramientas</td><td>Cinco veces seguidas</td><td>A la quinta ya baila</td><td class="no">No</td></tr>
        </table>
      </div>

      <h3>Y cuando alguno dice &laquo;no&raquo;</h3>
      <p>Que salga un <i>no</i> no es un suspenso: es informaci&oacute;n, y es exactamente para lo que
         sirve este paso. Hay <b>tres</b> salidas honradas, y una que no existe:</p>

      <figure class="foto">
        <img src="../../../img/u1-revisar.jpg" width="1200" height="800" loading="lazy"
             alt="Un adolescente revisa con las manos un montaje rojo con cables y una placa, sentado a una mesa">
        <figcaption>No es un soporte de m&oacute;vil, pero es <b>exactamente lo que toca hoy</b>: tener
          delante lo que has construido y meterle mano. Fijaos en que no est&aacute; ense&ntilde;&aacute;ndolo
          ni present&aacute;ndolo &mdash; est&aacute; <b>comprobando</b>. Volver atr&aacute;s a arreglar algo
          que no cumple no es haberlo hecho mal: es el paso 7 funcionando.
          <br><br>Foto de <b>Vanessa Loring</b> en Pexels. Es de su autor y no forma parte del material
          publicado bajo la licencia de esta p&aacute;gina.</figcaption>
      </figure>
      <ol>
        <li><b>Corregir la pieza.</b> En el ejemplo: cortar otra costilla con la ranura un pelo m&aacute;s
              estrecha y volver a cronometrar.</li>
        <li><b>Cambiar el dise&ntilde;o.</b> Se vuelve al paso 4 con lo aprendido. Esto es la vuelta atr&aacute;s
            de la que hablamos el primer d&iacute;a, y es normal.</li>
        <li><b>Cambiar el requisito</b>, si de verdad era irreal &mdash;y explicando por qu&eacute;, con el
            dato de la prueba delante&mdash;.</li>
      </ol>
      <div class="aviso">
        <span class="n-tag">La que no existe</span>
        Borrar el requisito y hacer como que nunca estuvo. Es la &uacute;nica salida que no vale, y es la
        que m&aacute;s se intenta.
      </div>

      <h3>Contarlo: la memoria t&eacute;cnica</h3>
      <p>Un proyecto termina cuando est&aacute; <b>escrito</b>. La memoria no es un resumen bonito del
         final: es el rastro de las decisiones, y por eso casi toda la ten&eacute;is ya hecha en las hojas
         de las sesiones anteriores. Hoy solo se ordena.</p>
      <div class="copiar">
        <h4>&Iacute;ndice de la memoria</h4>
        <ol>
          <li><b>Portada</b>: t&iacute;tulo, autores, curso y fecha.</li>
          <li><b>El problema y los requisitos</b> &middot; de la sesi&oacute;n 1.</li>
          <li><b>Ideas y decisi&oacute;n</b>: las seis ideas y la matriz &middot; de la sesi&oacute;n 2.</li>
          <li><b>Dise&ntilde;o</b>: croquis acotados y lista de materiales &middot; de la sesi&oacute;n 3.</li>
          <li><b>Planificaci&oacute;n</b>: hoja de proceso y Gantt &middot; de la sesi&oacute;n 4.</li>
          <li><b>Construcci&oacute;n</b>: tiempos reales y parte de incidencias &middot; de la sesi&oacute;n 5.</li>
          <li><b>Evaluaci&oacute;n</b>: la tabla de hoy, con los n&uacute;meros de las pruebas.</li>
          <li><b>Conclusi&oacute;n y mejoras</b>: qu&eacute; cambiar&iacute;ais si lo hicierais otra vez.</li>
        </ol>
      </div>
      <div class="nota">
        <span class="n-tag">El apartado 8 es el que m&aacute;s dice de vosotros</span>
        Un &laquo;lo har&iacute;amos igual&raquo; significa casi siempre que no se ha mirado. Un &laquo;har&iacute;amos la ranura de 3,5 mm porque con 4 acab&oacute; bailando&raquo;
        demuestra que hab&eacute;is entendido vuestro propio proyecto.
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; no hace falta copiarlo</span>
        <p>Esto no es una costumbre escolar. Cualquier pieza que vuele en un avi&oacute;n lleva detr&aacute;s
           una carpeta con los ensayos que ha pasado y quien firm&oacute; cada uno, y esa carpeta se guarda
           d&eacute;cadas. Cuando algo falla, lo primero que se abre no es la pieza: es la carpeta.</p>
      </div>
    </section>

    <section class="bloque">
      <div class="rotulo"><span class="num">02</span> La memoria &middot; 15 min</div>
      <div class="ficha">
        <div class="ficha-cab">
          <span>Actividad 6 &middot; Tabla de evaluaci&oacute;n y memoria del proyecto</span>
          <span class="chips"><span class="chip">1.1</span><span class="chip">1.3</span><span class="chip">2.1</span></span>
          <span>Parejas &middot; 15 min</span>
        </div>
        <div class="ficha-cuerpo">
          <h4>Qu&eacute; hay que hacer</h4>
          <ol class="pasos">
            <li>La <b>tabla de evaluaci&oacute;n</b> con <b>todos</b> vuestros requisitos, incluidos los que
                no cumple. Con su columna de <i>c&oacute;mo se comprueba</i> y su resultado medido.</li>
            <li>Para cada <i>no</i>, cu&aacute;l de las <b>tres salidas</b> eleg&iacute;s y por qu&eacute;.</li>
            <li>Montad la memoria con los ocho apartados, grapando lo que ya ten&eacute;is de las
                sesiones anteriores. No hay que volver a escribirlo.</li>
            <li>Escribid el apartado 8 de verdad: <b>dos mejoras concretas</b>, cada una con el dato que
                la justifica.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Est&aacute;n todos los requisitos, tambi&eacute;n los incumplidos <b>(3 puntos)</b>.</li>
            <li>Cada comprobaci&oacute;n tiene un <b>resultado medido</b>, no una impresi&oacute;n <b>(3 puntos)</b>.</li>
            <li>La memoria tiene los ocho apartados y se entiende sin vosotros <b>(2 puntos)</b>.</li>
            <li>Las mejoras son concretas y salen de un dato <b>(2 puntos)</b>.</li>
          </ul>
        </div>
      </div>
    </section>

    <section class="bloque">
      <div class="rotulo"><span class="num">03</span> Test &middot; 10 min</div>

      <p>Diez preguntas de todo el tema. Se corrigen aqu&iacute; mismo, y cada una explica por
         qu&eacute; &mdash;tambi&eacute;n las que aciertes&mdash;. No cuenta para nota: es para que sepas por
         d&oacute;nde andas.</p>
      <div class="ta" id="test-u1">
        <h4>Lo que tiene que haber quedado del tema</h4>

        <div class="ta-p" data-ok="0" role="group" aria-labelledby="test-u1-p1">
          <p id="test-u1-p1">1. Un requisito es&hellip;</p>
          <label class="ta-op"><input type="radio" name="u1-0" value="0">una condici&oacute;n que la soluci&oacute;n tiene que cumplir, escrita para poder comprobarla</label>
          <label class="ta-op"><input type="radio" name="u1-0" value="1">una idea de soluci&oacute;n escrita en una l&iacute;nea</label>
          <label class="ta-op"><input type="radio" name="u1-0" value="2">la lista de materiales que vas a necesitar</label>
          <div class="ta-por"><b>Por qu&eacute;:</b> Es el paso 2 del proceso, y el que decide todo lo dem&aacute;s. Si los requisitos est&aacute;n bien escritos, el paso 7 &mdash;evaluar&mdash; es objetivo: se cumplen o no. Si no los escribiste, nunca sabr&aacute;s si tu soluci&oacute;n es buena, solo si te gusta.</div>
        </div>

        <div class="ta-p" data-ok="2" role="group" aria-labelledby="test-u1-p2">
          <p id="test-u1-p2">2. De estos tres, &iquest;cu&aacute;l est&aacute; bien escrito como requisito?</p>
          <label class="ta-op"><input type="radio" name="u1-1" value="0">Que sea resistente</label>
          <label class="ta-op"><input type="radio" name="u1-1" value="1">Que quede bonito en el aula</label>
          <label class="ta-op"><input type="radio" name="u1-1" value="2">Que sujete un m&oacute;vil de 165 mm sin volcar al tocar la pantalla</label>
          <div class="ta-por"><b>Por qu&eacute;:</b> La prueba es esta: <i>&iquest;podr&iacute;an dos personas discutir sobre si se cumple?</i> Con los dos primeros, s&iacute;. Con el tercero no: se cuelgan 3 kg y se mira. Un requisito bueno se comprueba con una regla, un cron&oacute;metro o un s&iacute;/no.</div>
        </div>

        <div class="ta-p" data-ok="0" role="group" aria-labelledby="test-u1-p3">
          <p id="test-u1-p3">3. Mientras se proponen ideas no se critica ninguna. &iquest;Por qu&eacute;?</p>
          <label class="ta-op"><input type="radio" name="u1-2" value="0">porque criticar corta la generaci&oacute;n, y una idea imposible suele darle a otro una posible</label>
          <label class="ta-op"><input type="radio" name="u1-2" value="1">por educaci&oacute;n, para que nadie se sienta mal</label>
          <label class="ta-op"><input type="radio" name="u1-2" value="2">porque todas las ideas son igual de buenas</label>
          <div class="ta-por"><b>Por qu&eacute;:</b> No todas son igual de buenas &mdash;por eso hay un segundo momento para juzgarlas&mdash;. La raz&oacute;n es pr&aacute;ctica: en cuanto aparece una soluci&oacute;n razonable, el cerebro deja de buscar y empieza a defenderla. Se llama <b>fijaci&oacute;n</b>, y separar proponer de juzgar es lo que la evita.</div>
        </div>

        <div class="ta-p" data-ok="1" role="group" aria-labelledby="test-u1-p4">
          <p id="test-u1-p4">4. La matriz de decisi&oacute;n&hellip;</p>
          <label class="ta-op"><input type="radio" name="u1-3" value="0">elige la mejor idea por ti, si la rellenas bien</label>
          <label class="ta-op"><input type="radio" name="u1-3" value="1">te obliga a decir con qu&eacute; criterio eliges, y deja la decisi&oacute;n por escrito</label>
          <label class="ta-op"><input type="radio" name="u1-3" value="2">sirve para votar a mano alzada m&aacute;s deprisa</label>
          <div class="ta-por"><b>Por qu&eacute;:</b> Si cambias los pesos, cambia el resultado: por eso los pesos hay que justificarlos. La matriz no garantiza acertar, garantiza que la decisi&oacute;n sea <b>rastreable</b>. Y si la que gana no os convence, es que algo importante no estaba puesto por escrito.</div>
        </div>

        <div class="ta-p" data-ok="0" role="group" aria-labelledby="test-u1-p5">
          <p id="test-u1-p5">5. &iquest;En qu&eacute; se diferencian un boceto y un croquis?</p>
          <label class="ta-op"><input type="radio" name="u1-4" value="0">los dos van a mano alzada, pero el croquis lleva las medidas escritas</label>
          <label class="ta-op"><input type="radio" name="u1-4" value="1">el boceto va a escala y el croquis no</label>
          <label class="ta-op"><input type="radio" name="u1-4" value="2">el boceto se hace con regla y el croquis a mano alzada</label>
          <div class="ta-por"><b>Por qu&eacute;:</b> El boceto sirve para <b>pensar</b>; el croquis, para <b>decidir</b>; el plano, a escala y con instrumentos, es el <b>documento</b> con el que otro construye sin preguntarte nada. El que va a escala es el plano, no el boceto.</div>
        </div>

        <div class="ta-p" data-ok="1" role="group" aria-labelledby="test-u1-p6">
          <p id="test-u1-p6">6. En el soporte del ejemplo, la costilla mide 110 mm de largo. Ese n&uacute;mero sale de&hellip;</p>
          <label class="ta-op"><input type="radio" name="u1-5" value="0">la medida a la que se venden las cajas</label>
          <label class="ta-op"><input type="radio" name="u1-5" value="1">tres requisitos sumados: 36 mm por delante, 4 del grueso del respaldo y 70 de cola</label>
          <label class="ta-op"><input type="radio" name="u1-5" value="2">lo que parec&iacute;a bien proporcionado en el dibujo</label>
          <div class="ta-por"><b>Por qu&eacute;:</b> 36 + 4 + 70 = <b>110 mm</b>. Una medida que no puedas justificar con un requisito o con una comprobaci&oacute;n es una medida inventada, y siempre se descubre tarde.</div>
        </div>

        <div class="ta-p" data-ok="2" role="group" aria-labelledby="test-u1-p7">
          <p id="test-u1-p7">7. En el diagrama de Gantt, el secado de la cola ocupa una fila entera aunque no lo haga nadie. &iquest;Por qu&eacute;?</p>
          <label class="ta-op"><input type="radio" name="u1-6" value="0">para que se vea que se ha usado cola</label>
          <label class="ta-op"><input type="radio" name="u1-6" value="1">no deber&iacute;a ocuparla: las esperas no se dibujan</label>
          <label class="ta-op"><input type="radio" name="u1-6" value="2">porque ocupa tiempo, y el Gantt reparte tiempo, no trabajo</label>
          <div class="ta-por"><b>Por qu&eacute;:</b> Una espera que no est&aacute; dibujada aparece igual, pero por sorpresa y cuando ya no queda sesi&oacute;n. Y mientras la cola agarra, el Gantt ense&ntilde;a qu&eacute; otra cosa se puede ir haciendo.</div>
        </div>

        <div class="ta-p" data-ok="1" role="group" aria-labelledby="test-u1-p8">
          <p id="test-u1-p8">8. Una tarea acaba en el minuto 23 y la siguiente no puede empezar hasta el 27. Esos cuatro minutos son&hellip;</p>
          <label class="ta-op"><input type="radio" name="u1-7" value="0">un error de planificaci&oacute;n</label>
          <label class="ta-op"><input type="radio" name="u1-7" value="1">la holgura de esa tarea: lo que puede retrasarse sin retrasar el final</label>
          <label class="ta-op"><input type="radio" name="u1-7" value="2">tiempo perdido que hay que recortar</label>
          <div class="ta-por"><b>Por qu&eacute;:</b> Las tareas con holgura se pueden retrasar un poco sin consecuencias; las que no la tienen son las que mandan en la hora de acabar, y son las que hay que vigilar. Saber cu&aacute;les son es media planificaci&oacute;n.</div>
        </div>

        <div class="ta-p" data-ok="1" role="group" aria-labelledby="test-u1-p9">
          <p id="test-u1-p9">9. Pegas las dos piezas de cart&oacute;n con cola, a tope, en vez de encastrarlas. &iquest;Qu&eacute; va a pasar?</p>
          <label class="ta-op"><input type="radio" name="u1-8" value="0">aguantar&aacute; m&aacute;s que encastradas, porque pega toda la superficie</label>
          <label class="ta-op"><input type="radio" name="u1-8" value="1">aguantar&aacute; poco, y al tirar se llevar&aacute; la capa de papel</label>
          <label class="ta-op"><input type="radio" name="u1-8" value="2">aguantar&aacute; lo mismo, porque la cola de madera vale para todo</label>
          <div class="ta-por"><b>Por qu&eacute;:</b> El cart&oacute;n es <b>papel con aire dentro</b>. La cola se mete en la onda en vez de quedarse en la junta, y lo que acaba fallando no es el pegamento: es el propio cart&oacute;n, que se abre en dos y deja la onda al aire. Por eso aqu&iacute; se une <b>por la forma</b> y no por el pegamento, que adem&aacute;s se desmonta y cabe plano en la mochila.</div>
        </div>

        <div class="ta-p" data-ok="0" role="group" aria-labelledby="test-u1-p10">
          <p id="test-u1-p10">10. Al evaluar, uno de vuestros requisitos no se cumple. &iquest;Qu&eacute; se hace?</p>
          <label class="ta-op"><input type="radio" name="u1-9" value="0">se corrige la pieza, se cambia el dise&ntilde;o, o se cambia el requisito explicando por qu&eacute;</label>
          <label class="ta-op"><input type="radio" name="u1-9" value="1">se borra ese requisito, que al fin y al cabo lo escribisteis vosotros</label>
          <label class="ta-op"><input type="radio" name="u1-9" value="2">nada: el proyecto ya est&aacute; construido y no se puede tocar</label>
          <div class="ta-por"><b>Por qu&eacute;:</b> Un <i>no</i> es informaci&oacute;n, y para eso existe el paso 7. Las tres salidas son honradas y las tres se escriben en la memoria. La que no vale es borrar el requisito y hacer como que nunca estuvo &mdash;y es la que m&aacute;s se intenta&mdash;.</div>
        </div>

        <div class="ta-pie">
          <button type="button" data-a="corregir">Corregir</button>
          <button type="button" class="otra" data-a="otra" hidden>Borrar y repetir</button>
          <span class="ta-nota" role="status" aria-live="polite"></span>
        </div>
        <p class="ta-aviso">Se corrige en tu propio navegador: no se env&iacute;a ni se guarda nada.</p>
      </div>
    </section>

    <section class="bloque">
      <div class="rotulo"><span class="num">04</span> Cierre del tema &middot; 5 min</div>

      <p>Mirad hacia atr&aacute;s. El primer d&iacute;a, con cinco minutos y una hoja, cada grupo escribi&oacute;
         una cosa distinta y no hab&iacute;a forma de decir cu&aacute;l era mejor. Hoy ten&eacute;is un objeto
         construido, una tabla que dice qu&eacute; cumple y qu&eacute; no, y una carpeta con la que otra
         persona podr&iacute;a repetirlo sin vosotros delante. Entre una cosa y otra no ha habido m&aacute;s
         talento: ha habido <b>orden</b>.</p>

      <div class="copiar">
        <h4>El tema entero, en seis l&iacute;neas</h4>
        <ul>
          <li>El <b>proceso tecnol&oacute;gico</b> son siete pasos que hacen que el resultado no dependa de la suerte.</li>
          <li>El paso que decide todo es el <b>2</b>: escribir requisitos <b>comprobables</b>.</li>
          <li>Primero <b>muchas ideas</b> sin criticar; despu&eacute;s se elige con una <b>matriz</b> y con pesos justificados.</li>
          <li>Dise&ntilde;ar es <b>acotar</b>: croquis con medidas y <b>lista de materiales</b>, y cada medida sale de un requisito.</li>
          <li>Planificar es decir <b>qui&eacute;n, con qu&eacute; y en cu&aacute;ntos minutos</b>, y dibujar tambi&eacute;n las esperas.</li>
          <li>Evaluar es <b>volver a la lista del paso 2</b>. Y volver atr&aacute;s no es fracasar: es c&oacute;mo funciona.</li>
        </ul>
      </div>

      <div class="nota">
        <span class="n-tag">Siguiente tema</span>
        En este tema hab&eacute;is dibujado croquis a mano alzada y os ha bastado para cortar cuatro
        piezas. Para algo m&aacute;s complicado no basta: hacen falta <b>vistas</b>, <b>escalas</b>,
        reglas de acotaci&oacute;n y un <b>cajet&iacute;n</b> que diga qui&eacute;n lo firma. Eso es justo lo que trabajasteis en el
        <b>tema 2</b>, que disteis antes que este.
      <!-- enlace al tema siguiente --><p style="margin-top:12px"><a href="../tema3/" style="font-family:var(--f-m);font-size:13px;color:var(--goo-azul);font-weight:500">Ir al tema 3 &middot; Materiales de uso técnico &rarr;</a></p></div>
    </section>'''
