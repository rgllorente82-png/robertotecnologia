# -*- coding: utf-8 -*-
import io, os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tema0_base import cabeza, SELLO, aviso_licencia, SITIO, AUTOR_TXT, CARGO
from tema0_contenido import HITOS, NIVELES

BASE = "C:/Users/javie/AppData/Local/Temp/rt-clone"

VIDEO_RI4 = u"""
    <h3>Un repaso r&aacute;pido antes de analizarlo</h3>
    <div class="video" id="video-ri" data-vid="A1lacXFaKow">
      <button type="button" class="video-play" aria-label="Reproducir el v&iacute;deo resumen sobre la Revoluci&oacute;n Industrial">
        <span class="video-tri" aria-hidden="true"></span>
        <span class="video-txt">
          <b>La Revoluci&oacute;n Industrial &middot; resumen</b>
          <span>A toda leche</span>
        </span>
      </button>
      <p class="video-nota">Al verlo, ve anotando los <b>cuatro pasos</b> de la secuencia que has destapado
        antes: qu&eacute; cambi&oacute; en la producci&oacute;n, qu&eacute; excedente gener&oacute;, c&oacute;mo se reorganiz&oacute; la
        sociedad y qu&eacute; problema nuevo apareci&oacute;. Lo usaremos en la actividad.</p>
      <p class="video-nota">El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin cookies de
        seguimiento. Si la red del centro bloquea YouTube,
        <a href="https://www.youtube.com/watch?v=A1lacXFaKow" target="_blank" rel="noopener">&aacute;brelo
        directamente aqu&iacute;</a>. Es obra de su autor y no forma parte del material publicado bajo la
        licencia de esta p&aacute;gina.</p>
    </div>
"""

VIDEO_RI = u"""
    <h3>Ve&aacute;moslo en tres minutos</h3>
    <div class="video" id="video-ri" data-vid="eZtmIClLJWM">
      <button type="button" class="video-play" aria-label="Reproducir el v&iacute;deo sobre la Revoluci&oacute;n Industrial">
        <span class="video-tri" aria-hidden="true"></span>
        <span class="video-txt">
          <b>La Revoluci&oacute;n Industrial</b>
          <span>Happy Learning Espa&ntilde;ol &middot; unos 3 minutos</span>
        </span>
      </button>
      <p class="video-nota">El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin cookies de
        seguimiento. Si la red del centro bloquea YouTube,
        <a href="https://www.youtube.com/watch?v=eZtmIClLJWM" target="_blank" rel="noopener">&aacute;brelo
        directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material publicado bajo
        la licencia de esta p&aacute;gina.</p>
    </div>
"""


def cuerpo(k, n):
    es2 = (k == '2eso')
    clave = 'c2' if es2 else 'c4'
    hitos_js = json.dumps([{'id': h['id'], 'pos': h['pos'], 'ep': h['ep'], 't': h['t'], 'c': h[clave]}
                           for h in HITOS], ensure_ascii=False)

    # --- 01 teoria, distinta por nivel ---
    if es2:
        teoria = u"""
      <h3>Empecemos por una pregunta tonta</h3>
      <p>Cuenta cu&aacute;ntos objetos has usado hoy desde que has abierto los ojos hasta llegar a clase.
         La alarma, la luz, el grifo, la ropa, el desayuno envasado, el autob&uacute;s, la mochila, el boli.
         Ninguno de esos objetos existe en la naturaleza. <b>Todos los ha fabricado alguien</b> para resolver
         un problema que alguien ten&iacute;a.</p>
      <p>Eso es la tecnolog&iacute;a: no los aparatos, sino <b>la forma de resolver problemas fabricando cosas</b>.</p>

      <div class="def">
        <span class="n-tag">Definici&oacute;n</span>
        <p><b>Tecnolog&iacute;a</b> es el conjunto de conocimientos, t&eacute;cnicas y herramientas que usamos para
        crear objetos y sistemas que <b>resuelven necesidades</b> de las personas.</p>
      </div>

      <h3>T&eacute;cnica, tecnolog&iacute;a y ciencia no son lo mismo</h3>
      <p>Se confunden mucho, y en el examen se pregunta. La diferencia est&aacute; en <b>qu&eacute; responde cada una</b>:</p>
      <ul>
        <li><b>La t&eacute;cnica</b> responde a <i>c&oacute;mo se hace</i>. Es la habilidad de hacer algo bien: soldar,
            serrar recto, hacer pan. Se aprende practicando y se transmite imitando. <b>No necesita saber por qu&eacute;
            funciona.</b></li>
        <li><b>La ciencia</b> responde a <i>por qu&eacute; ocurre</i>. Busca explicar la naturaleza. No pretende
            fabricar nada: quiere entender.</li>
        <li><b>La tecnolog&iacute;a</b> responde a <i>c&oacute;mo resuelvo este problema</i>. Coge lo que sabe la ciencia
            y lo que sabe hacer la t&eacute;cnica y lo junta para crear una soluci&oacute;n.</li>
      </ul>
      <div class="nota">
        <span class="n-tag">Para que se te quede</span>
        Un alfarero del Neol&iacute;tico ten&iacute;a <b>t&eacute;cnica</b>: sab&iacute;a hacer vasijas perfectas sin tener ni idea
        de qu&iacute;mica. Un qu&iacute;mico de hoy tiene <b>ciencia</b>: sabe qu&eacute; le pasa a la arcilla a 900&nbsp;&deg;C. Una
        f&aacute;brica de cer&aacute;mica usa <b>tecnolog&iacute;a</b>: junta las dos cosas para producir mil platos iguales.
      </div>
      <div class="escena">
        <div class="escena-barra"><span class="escena-titulo">C&oacute;mo se relacionan los tres</span></div>
        <div class="lienzo">
          <svg viewBox="0 0 640 300" role="img"
               aria-label="La t&eacute;cnica y la ciencia confluyen en la tecnolog&iacute;a, que a su vez devuelve preguntas a la ciencia">

            <!-- TECNICA -->
            <rect x="26" y="26" width="220" height="92" rx="3" fill="var(--surface)" stroke="var(--goo-amarillo)" stroke-width="2.5"/>
            <text x="46" y="52" style="font:500 14px var(--f-b);fill:var(--ink)">T&Eacute;CNICA</text>
            <text x="46" y="72" style="font:400 12px var(--f-m);fill:var(--goo-amarillo)">&iquest;C&Oacute;MO SE HACE?</text>
            <text x="46" y="94" style="font:400 12.5px var(--f-b);fill:var(--ink-soft)">Saber hacerlo con las manos.</text>
            <text x="46" y="110" style="font:400 12.5px var(--f-b);fill:var(--ink-soft)">Se aprende imitando.</text>
            <!-- mano con herramienta -->
            <g transform="translate(196,58)" stroke="#9a7326" stroke-width="2.2" fill="none" stroke-linecap="round">
              <path d="M0 22 q-6 -4 -6 -12 v-8 M4 22 v-22 M10 22 v-18 M16 22 q6 -2 6 -10"/>
              <path d="M-8 22 h30 v8 h-30 Z" fill="#fbbc04" opacity=".3" stroke="none"/>
            </g>

            <!-- CIENCIA -->
            <rect x="394" y="26" width="220" height="92" rx="3" fill="var(--surface)" stroke="var(--goo-verde)" stroke-width="2.5"/>
            <text x="414" y="52" style="font:500 14px var(--f-b);fill:var(--ink)">CIENCIA</text>
            <text x="414" y="72" style="font:400 12px var(--f-m);fill:var(--goo-verde)">&iquest;POR QU&Eacute; OCURRE?</text>
            <text x="414" y="94" style="font:400 12.5px var(--f-b);fill:var(--ink-soft)">Explicar la naturaleza.</text>
            <text x="414" y="110" style="font:400 12.5px var(--f-b);fill:var(--ink-soft)">Se publica y se comprueba.</text>
            <!-- lupa -->
            <g transform="translate(566,58)" stroke="#1e6b33" stroke-width="2.4" fill="none">
              <circle cx="8" cy="10" r="10"/><path d="M16 18 l10 10" stroke-linecap="round"/>
            </g>

            <!-- flechas de entrada -->
            <path d="M136 122 L136 152 L290 152 L290 176" fill="none" stroke="var(--goo-amarillo)" stroke-width="2.2"/>
            <path d="M290 184 l-5 -10 h10 Z" fill="var(--goo-amarillo)"/>
            <path d="M504 122 L504 152 L350 152 L350 176" fill="none" stroke="var(--goo-verde)" stroke-width="2.2"/>
            <path d="M350 184 l-5 -10 h10 Z" fill="var(--goo-verde)"/>

            <!-- TECNOLOGIA -->
            <rect x="152" y="186" width="336" height="88" rx="3" fill="var(--accent-soft)" stroke="var(--goo-azul)" stroke-width="2.5"/>
            <text x="176" y="214" style="font:500 15px var(--f-b);fill:var(--ink)">TECNOLOG&Iacute;A</text>
            <text x="176" y="234" style="font:400 12px var(--f-m);fill:var(--goo-azul)">&iquest;C&Oacute;MO LO RESUELVO?</text>
            <text x="176" y="256" style="font:400 12.5px var(--f-b);fill:var(--ink-soft)">Junta las dos para resolver un problema real.</text>
            <g transform="translate(436,206)" stroke="#1a5fb4" stroke-width="2.4" fill="none">
              <circle cx="14" cy="22" r="11"/><circle cx="14" cy="22" r="3.4" fill="#1a5fb4"/>
              <path d="M14 8 v5 M14 31 v5 M0 22 h5 M23 22 h5 M4 12 l3.5 3.5 M20.5 28.5 l3.5 3.5 M24 12 l-3.5 3.5 M7.5 28.5 l-3.5 3.5" stroke-linecap="round"/>
            </g>

            <!-- flecha de vuelta -->
            <path d="M488 230 L560 230 L560 160 L560 122" fill="none" stroke="var(--goo-azul)"
                  stroke-width="1.8" stroke-dasharray="6 4"/>
            <path d="M560 114 l-5 10 h10 Z" fill="var(--goo-azul)"/>
            <text x="572" y="180" style="font:400 10px var(--f-m);fill:var(--goo-azul)">y a veces</text>
            <text x="572" y="193" style="font:400 10px var(--f-m);fill:var(--goo-azul)">va por</text>
            <text x="572" y="206" style="font:400 10px var(--f-m);fill:var(--goo-azul)">delante</text>
          </svg>
        </div>
        <div class="pie">La t&eacute;cnica aporta el <b>saber hacer</b> y la ciencia el <b>saber por qu&eacute;</b>. La tecnolog&iacute;a
          los junta para resolver un problema concreto. Y la flecha de puntos importa: a veces la tecnolog&iacute;a
          funciona antes de que la ciencia sepa explicarla, y es ella la que obliga a investigar.</div>
      </div>


      <h3>La tecnolog&iacute;a siempre empieza por una necesidad</h3>
      <p>Nadie inventa por inventar. Detr&aacute;s de cada objeto hay alguien que ten&iacute;a un problema:</p>
      <ol class="pasos">
        <li>Aparece una <b>necesidad</b> &mdash;tengo fr&iacute;o, no llego, no puedo cortar esto&mdash;.</li>
        <li>Se busca una <b>soluci&oacute;n</b> con lo que se sabe y con los materiales que hay.</li>
        <li>Se <b>fabrica</b> y se prueba.</li>
        <li>Si funciona, se <b>mejora</b> y se ense&ntilde;a a otros. Si no, se cambia.</li>
      </ol>

      <div class="escena">
        <div class="escena-barra"><span class="escena-titulo">El bucle que lleva funcionando 2,6 millones de a&ntilde;os</span></div>
        <div class="lienzo">
          <svg viewBox="0 0 640 260" role="img"
               aria-label="Ciclo: necesidad, soluci&oacute;n, fabricar y probar, mejorar, y vuelta a empezar">
            <g font-family="var(--f-b)">
              <!-- 1 -->
              <circle cx="90" cy="130" r="52" fill="var(--surface)" stroke="var(--goo-rojo)" stroke-width="2.5"/>
              <text x="90" y="118" text-anchor="middle" style="font:500 13px var(--f-b);fill:var(--ink)">NECESIDAD</text>
              <text x="90" y="138" text-anchor="middle" style="font:400 11px var(--f-b);fill:var(--ink-soft)">tengo fr&iacute;o,</text>
              <text x="90" y="152" text-anchor="middle" style="font:400 11px var(--f-b);fill:var(--ink-soft)">no llego</text>
              <circle cx="90" cy="130" r="52" fill="none" stroke="var(--goo-rojo)" stroke-width="2.5"/>
              <text x="90" y="62" text-anchor="middle" style="font:500 15px var(--f-m);fill:var(--goo-rojo)">1</text>

              <!-- 2 -->
              <circle cx="250" cy="130" r="52" fill="var(--surface)" stroke="var(--goo-amarillo)" stroke-width="2.5"/>
              <text x="250" y="118" text-anchor="middle" style="font:500 13px var(--f-b);fill:var(--ink)">IDEA</text>
              <text x="250" y="138" text-anchor="middle" style="font:400 11px var(--f-b);fill:var(--ink-soft)">con lo que s&eacute;</text>
              <text x="250" y="152" text-anchor="middle" style="font:400 11px var(--f-b);fill:var(--ink-soft)">y lo que hay</text>
              <text x="250" y="62" text-anchor="middle" style="font:500 15px var(--f-m);fill:#9a7326">2</text>

              <!-- 3 -->
              <circle cx="410" cy="130" r="52" fill="var(--surface)" stroke="var(--goo-verde)" stroke-width="2.5"/>
              <text x="410" y="118" text-anchor="middle" style="font:500 13px var(--f-b);fill:var(--ink)">FABRICO</text>
              <text x="410" y="138" text-anchor="middle" style="font:400 11px var(--f-b);fill:var(--ink-soft)">y lo pruebo</text>
              <text x="410" y="62" text-anchor="middle" style="font:500 15px var(--f-m);fill:var(--goo-verde)">3</text>

              <!-- 4 -->
              <circle cx="570" cy="130" r="52" fill="var(--surface)" stroke="var(--goo-azul)" stroke-width="2.5"/>
              <text x="570" y="118" text-anchor="middle" style="font:500 13px var(--f-b);fill:var(--ink)">MEJORO</text>
              <text x="570" y="138" text-anchor="middle" style="font:400 11px var(--f-b);fill:var(--ink-soft)">y lo ense&ntilde;o</text>
              <text x="570" y="152" text-anchor="middle" style="font:400 11px var(--f-b);fill:var(--ink-soft)">a otros</text>
              <text x="570" y="62" text-anchor="middle" style="font:500 15px var(--f-m);fill:var(--goo-azul)">4</text>

              <!-- flechas -->
              <path d="M146 130 h44" fill="none" stroke="var(--ink-soft)" stroke-width="2"/>
              <path d="M198 130 l-10 -5 v10 Z" fill="var(--ink-soft)"/>
              <path d="M306 130 h44" fill="none" stroke="var(--ink-soft)" stroke-width="2"/>
              <path d="M358 130 l-10 -5 v10 Z" fill="var(--ink-soft)"/>
              <path d="M466 130 h44" fill="none" stroke="var(--ink-soft)" stroke-width="2"/>
              <path d="M518 130 l-10 -5 v10 Z" fill="var(--ink-soft)"/>

              <!-- vuelta -->
              <path d="M570 186 v34 H90 v-34" fill="none" stroke="var(--ink-soft)" stroke-width="2" stroke-dasharray="7 5"/>
              <path d="M90 184 l-5 10 h10 Z" fill="var(--ink-soft)"/>
              <text x="330" y="238" text-anchor="middle" style="font:400 11px var(--f-m);fill:var(--ink-soft)">Y SI NO FUNCIONA, VUELTA A EMPEZAR</text>
            </g>
          </svg>
        </div>
        <div class="pie">Es el mismo bucle para una piedra tallada y para un cohete. Y es exactamente lo que
          vas a hacer t&uacute; en cada proyecto de este curso.</div>
      </div>
      <p>Ese bucle lleva funcionando dos millones y medio de a&ntilde;os, y es exactamente lo que vas a hacer t&uacute;
         este curso en cada proyecto.</p>
      <h3>Y la digitalizaci&oacute;n, &iquest;qu&eacute; es?</h3>
      <p>La asignatura se llama <b>Tecnolog&iacute;a y Digitalizaci&oacute;n</b>, as&iacute; que conviene aclarar la segunda
         mitad. Y de entrada, un aviso: digitalizaci&oacute;n <b>no</b> significa &laquo;usar ordenadores&raquo;.</p>
      <div class="def">
        <span class="n-tag">Definici&oacute;n</span>
        <p><b>Digitalizar</b> es convertir informaci&oacute;n en n&uacute;meros para que una m&aacute;quina pueda guardarla,
        copiarla, enviarla y transformarla. <b>Digitalizaci&oacute;n</b>, en sentido amplio, es lo que le pasa a
        una sociedad entera cuando casi toda su informaci&oacute;n y casi todos sus procesos funcionan as&iacute;.</p>
      </div>
      <p>Se entiende mejor con un disco. Un vinilo guarda la m&uacute;sica como un <b>surco f&iacute;sico</b>: cada copia
         del surco pierde un poco de calidad, y si se raya, se estrope&oacute; para siempre. Un archivo de m&uacute;sica
         guarda esa misma canci&oacute;n como una <b>lista de n&uacute;meros</b>. Y los n&uacute;meros se copian exactos,
         infinitas veces, sin perder nada y casi sin coste. Ah&iacute; est&aacute; toda la diferencia.</p>
      <h4>Qué hay dentro de cada uno</h4>
      <p>Los dos guardan la misma canción. Pero si te acercas con una lupa, lo que encuentras no se parece
         en nada.</p>

      <div class="escena">
        <div class="escena-barra">
          <span class="escena-titulo">El surco y la lista de números</span>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 330" role="img"
               aria-label="Un disco de vinilo con su surco continuo ampliado, y un archivo de audio con su lista de números ampliada">

            <!-- ================= VINILO ================= -->
            <text class="rotulo-svg" x="110" y="22" text-anchor="middle" style="font-size:11px">DISCO DE VINILO</text>

            <circle cx="110" cy="130" r="88" fill="#1b1b1f" stroke="var(--ink)" stroke-width="1.5"/>
            <g fill="none" stroke="#3a3a42" stroke-width="1">
              <circle cx="110" cy="130" r="80"/><circle cx="110" cy="130" r="74"/>
              <circle cx="110" cy="130" r="68"/><circle cx="110" cy="130" r="62"/>
              <circle cx="110" cy="130" r="56"/><circle cx="110" cy="130" r="50"/>
              <circle cx="110" cy="130" r="44"/><circle cx="110" cy="130" r="38"/>
            </g>
            <circle cx="110" cy="130" r="30" fill="var(--goo-rojo)"/>
            <circle cx="110" cy="130" r="30" fill="none" stroke="var(--ink)" stroke-width="1"/>
            <text x="110" y="126" text-anchor="middle" style="font-size:8px;fill:#fff;font-family:var(--f-m)">LA MISMA</text>
            <text x="110" y="137" text-anchor="middle" style="font-size:8px;fill:#fff;font-family:var(--f-m)">CANCI&Oacute;N</text>
            <circle cx="110" cy="130" r="3.6" fill="#1b1b1f"/>

            <!-- brazo y aguja -->
            <path d="M196 56 L150 106" stroke="var(--ink-soft)" stroke-width="3.5" stroke-linecap="round"/>
            <circle cx="198" cy="54" r="6" fill="var(--ink-soft)"/>
            <path d="M150 106 L146 114" stroke="var(--ink)" stroke-width="2.5" stroke-linecap="round"/>

            <!-- lupa sobre el surco -->
            <circle cx="110" cy="252" r="46" fill="var(--surface)" stroke="var(--goo-rojo)" stroke-width="2"/>
            <path d="M143 285 L163 305" stroke="var(--goo-rojo)" stroke-width="4" stroke-linecap="round"/>
            <path d="M143 219 L146 114" stroke="var(--goo-rojo)" stroke-width=".9" stroke-dasharray="4 3"/>
            <clipPath id="lupaV"><circle cx="110" cy="252" r="46"/></clipPath>
            <g clip-path="url(#lupaV)">
              <path d="M62 252 C72 230 82 274 92 250 C102 226 112 276 122 248 C132 224 142 272 152 250 C160 232 164 262 170 252"
                    fill="none" stroke="var(--goo-rojo)" stroke-width="2.4"/>
              <path d="M62 268 C72 246 82 290 92 266 C102 242 112 292 122 264 C132 240 142 288 152 266 C160 248 164 278 170 268"
                    fill="none" stroke="#c9ccd1" stroke-width="1.6"/>
              <path d="M62 236 C72 214 82 258 92 234 C102 210 112 260 122 232 C132 208 142 256 152 234 C160 216 164 246 170 236"
                    fill="none" stroke="#c9ccd1" stroke-width="1.6"/>
            </g>
            <text class="rotulo-svg" x="110" y="316" text-anchor="middle" style="font-size:9.5px;fill:var(--goo-rojo)">UN SURCO CONTINUO</text>

            <!-- ================= ARCHIVO ================= -->
            <text class="rotulo-svg" x="440" y="22" text-anchor="middle" style="font-size:11px">ARCHIVO DE AUDIO</text>

            <!-- movil -->
            <rect x="386" y="36" width="108" height="188" rx="12" fill="var(--surface)" stroke="var(--ink)" stroke-width="2"/>
            <rect x="394" y="48" width="92" height="164" rx="5" fill="var(--surface-2)"/>
            <rect x="404" y="58" width="72" height="52" rx="4" fill="var(--goo-verde)" opacity=".35"/>
            <text x="440" y="88" text-anchor="middle" style="font-size:8px;fill:var(--ink-soft);font-family:var(--f-m)">LA MISMA</text>
            <text x="440" y="99" text-anchor="middle" style="font-size:8px;fill:var(--ink-soft);font-family:var(--f-m)">CANCI&Oacute;N</text>
            <!-- onda -->
            <g stroke="var(--goo-verde)" stroke-width="2.4" stroke-linecap="round">
              <path d="M408 136 v12"/><path d="M415 128 v28"/><path d="M422 132 v20"/><path d="M429 122 v40"/>
              <path d="M436 130 v24"/><path d="M443 124 v36"/><path d="M450 134 v16"/><path d="M457 126 v32"/>
              <path d="M464 131 v22"/><path d="M471 137 v10"/>
            </g>
            <!-- barra de reproduccion -->
            <rect x="404" y="172" width="72" height="4" rx="2" fill="var(--line)"/>
            <rect x="404" y="172" width="42" height="4" rx="2" fill="var(--goo-verde)"/>
            <circle cx="446" cy="174" r="4.5" fill="var(--goo-verde)"/>
            <path d="M406 192 l11 7 l-11 7 Z" fill="var(--ink-soft)"/>
            <text x="476" y="203" text-anchor="end" style="font-size:8.5px;fill:var(--ink-soft);font-family:var(--f-m)">cancion.mp3</text>

            <!-- lupa sobre los numeros -->
            <circle cx="440" cy="252" r="46" fill="var(--surface)" stroke="var(--goo-verde)" stroke-width="2"/>
            <path d="M473 285 L493 305" stroke="var(--goo-verde)" stroke-width="4" stroke-linecap="round"/>
            <path d="M474 222 L466 212" stroke="var(--goo-verde)" stroke-width=".9" stroke-dasharray="4 3"/>
            <clipPath id="lupaD"><circle cx="440" cy="252" r="46"/></clipPath>
            <g clip-path="url(#lupaD)" style="font-family:var(--f-m);font-size:11px;fill:var(--goo-verde)">
              <text x="404" y="232">18 42 61</text>
              <text x="404" y="248">57 33 09</text>
              <text x="404" y="264">-12 -45 -60</text>
              <text x="404" y="280">-38 -07 25</text>
            </g>
            <text class="rotulo-svg" x="440" y="316" text-anchor="middle" style="font-size:9.5px;fill:var(--goo-verde)">UNA LISTA DE N&Uacute;MEROS</text>

            <!-- separador -->
            <path d="M275 40 L275 300" stroke="var(--line)" stroke-width="1" stroke-dasharray="5 5"/>
            <text class="rotulo-svg" x="275" y="168" text-anchor="middle" style="font-size:13px;fill:var(--ink)">vs</text>
          </svg>
        </div>
        <div class="pie">A la izquierda, una <b>onda física</b> tallada en plástico: la aguja la recorre y la convierte
          en sonido. A la derecha, <b>números</b>: 42 quiere decir que en ese instante el altavoz debe estar en esa
          posición. Un plato lee un surco; un móvil lee una lista.</div>
      </div>

      <h4>Escúchalo</h4>
      <p>La misma melodía, guardada de las dos maneras. Dale a copiar varias veces y vuelve a escuchar
         las dos: ahí está toda la diferencia.</p>

      <div class="escena" id="esc-audio">
        <div class="escena-barra">
          <span class="escena-titulo">Vinilo frente a archivo digital</span>
          <div class="seg" id="seg-audio">
            <button type="button" data-a="copiar">Copiar una vez &#9654;</button>
            <button type="button" data-a="reset">&#8635; Empezar de nuevo</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 230" id="svg-audio" role="img"
               aria-label="Comparación entre una grabación analógica que se degrada al copiarse y un archivo digital que no"></svg>
        </div>
        <div class="pie" id="pie-audio">Las dos copias son la original. Todavía suenan igual.</div>
      </div>

      <div class="nota">
        <span class="n-tag">Por qué pasa esto</span>
        El vinilo guarda un <b>surco continuo</b>: al copiarlo, la aguja añade un poco de ruido y pierde un
        poco de agudos. Poco, pero cada vez. El archivo guarda <b>números</b>: copiar un 7 da un 7, siempre.
        Por eso una copia de una copia de una copia digital es idéntica a la original, y la analógica no.
      </div>

      <div class="aviso">
        <span class="n-tag">Nota</span>
        La melodía que escuchas no es ninguna canción: la genera tu propio navegador con unas pocas líneas de
        código, sin descargar nada. El ruido del vinilo también está fabricado a propósito para que oigas el
        efecto.
      </div>

      <script>
      (function(){
        var svgA = document.getElementById('svg-audio');
        var pieA = document.getElementById('pie-audio');
        var segA = document.getElementById('seg-audio');
        if(!svgA) return;

        var gen = 0, MAXG = 6, ctx = null;
        /* melodia propia, en semitonos sobre La3 = 220 Hz */
        var NOTAS = [0, 4, 7, 12, 7, 4, 0, -5, 0, 4, 7, 4];
        var DUR = 0.26;

        function hz(semi){ return 220 * Math.pow(2, semi/12); }

        function suena(analogico){
          try{
            ctx = ctx || new (window.AudioContext || window.webkitAudioContext)();
          }catch(e){ pieA.textContent = 'Tu navegador no deja reproducir sonido aquí.'; return; }
          if(ctx.state === 'suspended') ctx.resume();
          var t0 = ctx.currentTime + 0.05;
          var master = ctx.createGain();
          master.gain.value = 0.9;

          /* la copia analogica pierde agudos: filtro cada vez mas cerrado */
          var salida = master;
          if(analogico){
            var lp = ctx.createBiquadFilter();
            lp.type = 'lowpass';
            lp.frequency.value = Math.max(900, 9000 - gen * 1350);
            master.connect(lp); salida = lp;
          }
          salida.connect(ctx.destination);

          NOTAS.forEach(function(n, i){
            var o = ctx.createOscillator(), g = ctx.createGain();
            o.type = 'triangle';
            var f = hz(n);
            /* wow and flutter: la velocidad del plato no es perfecta */
            if(analogico && gen > 0) f *= 1 + (Math.random()-0.5) * 0.004 * gen;
            o.frequency.value = f;
            var ini = t0 + i*DUR;
            g.gain.setValueAtTime(0.0001, ini);
            g.gain.exponentialRampToValueAtTime(0.22, ini + 0.02);
            g.gain.exponentialRampToValueAtTime(0.0001, ini + DUR*0.92);
            o.connect(g); g.connect(salida);
            o.start(ini); o.stop(ini + DUR);
          });

          /* ruido de superficie y chasquidos, solo en las copias analogicas */
          if(analogico && gen > 0){
            var dur = NOTAS.length * DUR;
            var buf = ctx.createBuffer(1, Math.ceil(ctx.sampleRate*dur), ctx.sampleRate);
            var d = buf.getChannelData(0);
            var nivel = 0.006 * gen;
            for(var s = 0; s < d.length; s++){
              d[s] = (Math.random()*2 - 1) * nivel;
              if(Math.random() < 0.00012 * gen) d[s] = (Math.random()*2-1) * 0.55;  /* chasquido */
            }
            var src = ctx.createBufferSource(); src.buffer = buf;
            var gn = ctx.createGain(); gn.gain.value = 1;
            src.connect(gn); gn.connect(ctx.destination);
            src.start(t0);
          }
        }

        function onda(x0, y0, w, h, ruido, agudos, pasos){
          var p = '', N = 150;
          for(var i = 0; i <= N; i++){
            var t = i/N, x = x0 + t*w;
            var v = Math.sin(t*Math.PI*6) * agudos + Math.sin(t*Math.PI*17) * 0.32 * agudos;
            if(pasos) v = Math.round(v*6)/6;
            v += (Math.random()*2-1) * ruido;
            var y = y0 + h/2 - v*(h/2.4);
            p += (i ? ' L' : 'M') + x.toFixed(1) + ' ' + y.toFixed(1);
          }
          return p;
        }

        function pinta(){
          var deg = gen / MAXG;
          var m = '';
          /* vinilo */
          m += '<text class="rotulo-svg" x="24" y="26" style="font-size:11px">VINILO &middot; SURCO CONTINUO</text>';
          m += '<path d="' + onda(24, 36, 592, 66, 0.055*gen, Math.max(0.28, 1 - deg*0.72), false) +
               '" fill="none" stroke="var(--goo-rojo)" stroke-width="1.6"></path>';
          /* digital */
          m += '<text class="rotulo-svg" x="24" y="140" style="font-size:11px">ARCHIVO &middot; LISTA DE N&Uacute;MEROS</text>';
          m += '<path d="' + onda(24, 150, 592, 66, 0, 1, true) +
               '" fill="none" stroke="var(--goo-verde)" stroke-width="1.6"></path>';
          m += '<text class="rotulo-svg" x="616" y="26" text-anchor="end" style="font-size:10px;fill:var(--goo-rojo)">' +
               (gen === 0 ? 'ORIGINAL' : 'COPIA ' + gen) + '</text>';
          m += '<text class="rotulo-svg" x="616" y="140" text-anchor="end" style="font-size:10px;fill:var(--goo-verde)">' +
               (gen === 0 ? 'ORIGINAL' : 'COPIA ' + gen + ' &middot; ID&Eacute;NTICA') + '</text>';
          svgA.innerHTML = m;

          var b = svgA.parentElement.parentElement.querySelector('#btns-audio');
          if(gen === 0) pieA.innerHTML = 'Las dos son el original. Todav&iacute;a suenan igual. Pulsa <b>Copiar</b>.';
          else if(gen < MAXG) pieA.innerHTML = 'Copia n&uacute;mero <b>' + gen + '</b>. El vinilo ha perdido agudos y ha ganado ruido. El archivo sigue siendo el mismo.';
          else pieA.innerHTML = 'Copia n&uacute;mero <b>' + gen + '</b>. El vinilo casi no se entiende. El archivo digital es <b>bit a bit id&eacute;ntico</b> al original.';
        }

        segA.addEventListener('click', function(e){
          var b = e.target.closest('button[data-a]'); if(!b) return;
          if(b.dataset.a === 'copiar') gen = Math.min(gen + 1, MAXG);
          else gen = 0;
          pinta();
        });

        svgA.addEventListener('click', function(e){
          var y = e.offsetY / svgA.getBoundingClientRect().height * 230;
          suena(y < 115);
        });

        /* botones de escucha bajo el lienzo */
        var barra = document.createElement('div');
        barra.className = 'pie';
        barra.id = 'btns-audio';
        barra.innerHTML = '<div class="seg">' +
          '<button type="button" id="play-vin">&#9654; Escuchar el vinilo</button>' +
          '<button type="button" id="play-dig">&#9654; Escuchar el archivo</button></div>';
        pieA.parentElement.insertBefore(barra, pieA);
        barra.querySelector('#play-vin').addEventListener('click', function(){ suena(true); });
        barra.querySelector('#play-dig').addEventListener('click', function(){ suena(false); });

        pinta();
      })();
      </script>

      <p>Cuando eso mismo le ocurre a las fotos, a los libros, al dinero, a las clases, a los planos y a las
         m&aacute;quinas de una f&aacute;brica, cambian tres cosas de golpe:</p>
      <ul>
        <li><b>Copiar deja de costar.</b> Mandar un archivo a mil personas cuesta lo mismo que mandarlo a una.</li>
        <li><b>La distancia deja de importar.</b> Un plano llega a Alemania en un segundo.</li>
        <li><b>Las m&aacute;quinas pueden trabajar con esa informaci&oacute;n.</b> Un archivo se puede buscar, medir,
            corregir solo y mandar directamente a una impresora 3D para que lo fabrique.</li>
      </ul>
      <div class="aviso">
        <span class="n-tag">Las dos caras</span>
        Todo eso vale igual para lo malo. Un bulo se copia tan barato como una enciclopedia, tus datos viajan
        tan r&aacute;pido como tus fotos, y quien no tiene conexi&oacute;n o no sabe manejarse se queda fuera de cosas
        b&aacute;sicas: la cita del m&eacute;dico, el banco o los deberes. Eso &uacute;ltimo se llama <b>brecha digital</b>.
      </div>
      <p>Por eso la asignatura junta las dos palabras: <b>la digitalizaci&oacute;n es la tecnolog&iacute;a de nuestra
         &eacute;poca</b>, igual que la m&aacute;quina de vapor lo fue del siglo XIX. Y como con cualquier tecnolog&iacute;a,
         aqu&iacute; no basta con saber usarla: hay que entender c&oacute;mo funciona por dentro y decidir qu&eacute; queremos
         hacer con ella.</p>
"""
    else:
        teoria = u"""
      <h3>Una definici&oacute;n que aguante</h3>
      <p>La palabra viene del griego <i>t&eacute;chne</i> (arte, oficio) y <i>log&iacute;a</i> (estudio, tratado). Literalmente,
         <b>el estudio de c&oacute;mo se hacen las cosas</b>. Esa etimolog&iacute;a ya contiene la clave: la tecnolog&iacute;a no
         es el objeto, es el <b>conocimiento</b> que permite producirlo.</p>

      <div class="def">
        <span class="n-tag">Definici&oacute;n</span>
        <p><b>Tecnolog&iacute;a</b>: conjunto organizado de conocimientos cient&iacute;ficos, t&eacute;cnicos y emp&iacute;ricos,
        junto con los medios materiales y los procedimientos, que se aplica de forma sistem&aacute;tica al dise&ntilde;o
        y producci&oacute;n de bienes y servicios destinados a satisfacer necesidades humanas.</p>
      </div>

      <h3>Tres conceptos que conviene no mezclar</h3>
      <div class="reto-piensa">
        <span class="n-tag">Antes de mirar</span>
        <p>Dibuja en el cuaderno una tabla con <b>tres filas</b> &mdash;t&eacute;cnica, ciencia y
           tecnolog&iacute;a&mdash; y <b>tres columnas</b>:</p>
        <ol style="margin:8px 0 8px 0">
          <li><b>Pregunta</b> &middot; &iquest;a qu&eacute; pregunta responde cada una?</li>
          <li><b>Busca</b> &middot; &iquest;qu&eacute; persigue: hacer algo bien, entender algo o resolver algo?</li>
          <li><b>Se transmite</b> &middot; &iquest;c&oacute;mo pasa ese saber de unos a otros?</li>
        </ol>
        <p>Una o dos palabras por casilla, no m&aacute;s. Cuando la tengas, comprueba.</p>
      </div>
      <details class="resp revela"><summary>Comprobar la tabla</summary><div class="resp-cuerpo">
      <table style="width:100%;border-collapse:collapse;font-size:14.5px;margin:14px 0">
        <tr style="text-align:left;border-bottom:2px solid var(--ink)">
          <th style="padding:8px 6px"></th><th style="padding:8px 6px">Pregunta</th>
          <th style="padding:8px 6px">Busca</th><th style="padding:8px 6px">Se transmite</th></tr>
        <tr style="border-bottom:1px solid var(--line)">
          <td style="padding:8px 6px"><b>T&eacute;cnica</b></td><td style="padding:8px 6px"><i>&iquest;C&oacute;mo se hace?</i></td>
          <td style="padding:8px 6px">Destreza</td><td style="padding:8px 6px">Imitaci&oacute;n y pr&aacute;ctica</td></tr>
        <tr style="border-bottom:1px solid var(--line)">
          <td style="padding:8px 6px"><b>Ciencia</b></td><td style="padding:8px 6px"><i>&iquest;Por qu&eacute; ocurre?</i></td>
          <td style="padding:8px 6px">Explicaci&oacute;n</td><td style="padding:8px 6px">Publicaci&oacute;n y m&eacute;todo</td></tr>
        <tr><td style="padding:8px 6px"><b>Tecnolog&iacute;a</b></td><td style="padding:8px 6px"><i>&iquest;C&oacute;mo lo resuelvo?</i></td>
          <td style="padding:8px 6px">Soluci&oacute;n eficaz</td><td style="padding:8px 6px">Dise&ntilde;o, norma y patente</td></tr>
      </table>
      <p>La t&eacute;cnica es <b>anterior</b> a la ciencia en millones de a&ntilde;os: se tallaba piedra sin saber nada de
         mineralog&iacute;a y se fund&iacute;a bronce sin conocer la tabla peri&oacute;dica. Solo desde el siglo XVIII la ciencia
         empieza a guiar sistem&aacute;ticamente a la t&eacute;cnica, y de esa uni&oacute;n nace la tecnolog&iacute;a moderna.</p>
      </div></details>

      <div class="escena">
        <div class="escena-barra"><span class="escena-titulo">C&oacute;mo se relacionan los tres</span></div>
        <div class="lienzo">
          <svg viewBox="0 0 640 300" role="img"
               aria-label="La t&eacute;cnica y la ciencia confluyen en la tecnolog&iacute;a, que a su vez devuelve preguntas a la ciencia">

            <!-- TECNICA -->
            <rect x="26" y="26" width="220" height="92" rx="3" fill="var(--surface)" stroke="var(--goo-amarillo)" stroke-width="2.5"/>
            <text x="46" y="52" style="font:500 14px var(--f-b);fill:var(--ink)">T&Eacute;CNICA</text>
            <text x="46" y="72" style="font:400 12px var(--f-m);fill:var(--goo-amarillo)">&iquest;C&Oacute;MO SE HACE?</text>
            <text x="46" y="94" style="font:400 12.5px var(--f-b);fill:var(--ink-soft)">Saber hacerlo con las manos.</text>
            <text x="46" y="110" style="font:400 12.5px var(--f-b);fill:var(--ink-soft)">Se aprende imitando.</text>
            <!-- mano con herramienta -->
            <g transform="translate(196,58)" stroke="#9a7326" stroke-width="2.2" fill="none" stroke-linecap="round">
              <path d="M0 22 q-6 -4 -6 -12 v-8 M4 22 v-22 M10 22 v-18 M16 22 q6 -2 6 -10"/>
              <path d="M-8 22 h30 v8 h-30 Z" fill="#fbbc04" opacity=".3" stroke="none"/>
            </g>

            <!-- CIENCIA -->
            <rect x="394" y="26" width="220" height="92" rx="3" fill="var(--surface)" stroke="var(--goo-verde)" stroke-width="2.5"/>
            <text x="414" y="52" style="font:500 14px var(--f-b);fill:var(--ink)">CIENCIA</text>
            <text x="414" y="72" style="font:400 12px var(--f-m);fill:var(--goo-verde)">&iquest;POR QU&Eacute; OCURRE?</text>
            <text x="414" y="94" style="font:400 12.5px var(--f-b);fill:var(--ink-soft)">Explicar la naturaleza.</text>
            <text x="414" y="110" style="font:400 12.5px var(--f-b);fill:var(--ink-soft)">Se publica y se comprueba.</text>
            <!-- lupa -->
            <g transform="translate(566,58)" stroke="#1e6b33" stroke-width="2.4" fill="none">
              <circle cx="8" cy="10" r="10"/><path d="M16 18 l10 10" stroke-linecap="round"/>
            </g>

            <!-- flechas de entrada -->
            <path d="M136 122 L136 152 L290 152 L290 176" fill="none" stroke="var(--goo-amarillo)" stroke-width="2.2"/>
            <path d="M290 184 l-5 -10 h10 Z" fill="var(--goo-amarillo)"/>
            <path d="M504 122 L504 152 L350 152 L350 176" fill="none" stroke="var(--goo-verde)" stroke-width="2.2"/>
            <path d="M350 184 l-5 -10 h10 Z" fill="var(--goo-verde)"/>

            <!-- TECNOLOGIA -->
            <rect x="152" y="186" width="336" height="88" rx="3" fill="var(--accent-soft)" stroke="var(--goo-azul)" stroke-width="2.5"/>
            <text x="176" y="214" style="font:500 15px var(--f-b);fill:var(--ink)">TECNOLOG&Iacute;A</text>
            <text x="176" y="234" style="font:400 12px var(--f-m);fill:var(--goo-azul)">&iquest;C&Oacute;MO LO RESUELVO?</text>
            <text x="176" y="256" style="font:400 12.5px var(--f-b);fill:var(--ink-soft)">Junta las dos para resolver un problema real.</text>
            <g transform="translate(436,206)" stroke="#1a5fb4" stroke-width="2.4" fill="none">
              <circle cx="14" cy="22" r="11"/><circle cx="14" cy="22" r="3.4" fill="#1a5fb4"/>
              <path d="M14 8 v5 M14 31 v5 M0 22 h5 M23 22 h5 M4 12 l3.5 3.5 M20.5 28.5 l3.5 3.5 M24 12 l-3.5 3.5 M7.5 28.5 l-3.5 3.5" stroke-linecap="round"/>
            </g>

            <!-- flecha de vuelta -->
            <path d="M488 230 L560 230 L560 160 L560 122" fill="none" stroke="var(--goo-azul)"
                  stroke-width="1.8" stroke-dasharray="6 4"/>
            <path d="M560 114 l-5 10 h10 Z" fill="var(--goo-azul)"/>
            <text x="572" y="180" style="font:400 10px var(--f-m);fill:var(--goo-azul)">y a veces</text>
            <text x="572" y="193" style="font:400 10px var(--f-m);fill:var(--goo-azul)">va por</text>
            <text x="572" y="206" style="font:400 10px var(--f-m);fill:var(--goo-azul)">delante</text>
          </svg>
        </div>
        <div class="pie">La t&eacute;cnica aporta el <b>saber hacer</b> y la ciencia el <b>saber por qu&eacute;</b>. La tecnolog&iacute;a
          los junta para resolver un problema concreto. Y la flecha de puntos importa: a veces la tecnolog&iacute;a
          funciona antes de que la ciencia sepa explicarla, y es ella la que obliga a investigar.</div>
      </div>

      <div class="reto-piensa">
        <span class="n-tag">Piensa</span>
        <p>Parece l&oacute;gico que la ciencia vaya primero y la tecnolog&iacute;a aplique lo que aquella descubre.
           <b>&iquest;Se te ocurre alg&uacute;n caso en que ocurriera al rev&eacute;s?</b> Una tecnolog&iacute;a que funcionara
           antes de que nadie supiera explicar por qu&eacute;.</p>
      </div>
      <details class="resp revela"><summary>Ver un caso</summary><div class="resp-cuerpo">
        <p>La <b>m&aacute;quina de vapor</b>. Watt vend&iacute;a m&aacute;quinas que mov&iacute;an f&aacute;bricas enteras d&eacute;cadas antes
           de que Carnot y Clausius formularan la termodin&aacute;mica. De hecho fue al rev&eacute;s de lo esperable:
           la necesidad de mejorar el rendimiento de esas m&aacute;quinas es lo que <b>oblig&oacute; a crear la
           ciencia</b> que las explicaba.</p>
        <p>Conclusi&oacute;n: la relaci&oacute;n no es de una sola direcci&oacute;n. <b>La tecnolog&iacute;a tambi&eacute;n empuja a
           la ciencia.</b></p>
      </div></details>

      <h3>Por qu&eacute; la tecnolog&iacute;a explica la historia</h3>
      <p>Los grandes cortes hist&oacute;ricos no los marcan las batallas, sino los cambios en <b>c&oacute;mo se produce</b>.
         Cada tecnolog&iacute;a decisiva desencadena la misma secuencia:</p>
      <div class="reto-piensa">
        <span class="n-tag">Antes de mirar</span>
        <p>Toda tecnolog&iacute;a decisiva desencadena la misma secuencia de cuatro pasos.
           <b>&iquest;Cu&aacute;les dir&iacute;as que son?</b> Piensa en la agricultura o en la imprenta y ve
           destapando uno a uno.</p>
      </div>
      <ol class="pasos secuencia" id="secuencia-hist">
        <li class="oculto"><b>Cambia lo que se puede producir</b> y con cu&aacute;nto esfuerzo.</li>
        <li class="oculto">Eso genera <b>excedente</b> y modifica qui&eacute;n trabaja en qu&eacute;.</li>
        <li class="oculto">La <b>estructura social se reorganiza</b>: aparecen oficios, clases y poderes nuevos.</li>
        <li class="oculto">Surgen <b>problemas in&eacute;ditos</b> que la sociedad tarda en regular.</li>
      </ol>
      <div class="seg"><button type="button" id="btn-secuencia">Destapar el siguiente paso &#9654;</button></div>
      <p>Ese cuarto punto es el que m&aacute;s te interesa hoy: la agricultura trajo el hambre estacional y la guerra
         por la tierra; la industria, la contaminaci&oacute;n y el trabajo infantil; lo digital, la desinformaci&oacute;n y
         la brecha. <b>Ninguna tecnolog&iacute;a es neutral en sus consecuencias</b>, aunque s&iacute; lo sea en su intenci&oacute;n.</p>
      <h3>La digitalizaci&oacute;n como tecnolog&iacute;a de &eacute;poca</h3>
      <p>Conviene precisar el t&eacute;rmino, porque se usa con tres sentidos que no son intercambiables:</p>
      <p>Son estos tres. Intenta definirlos antes de destaparlos:</p>
      <details class="resp revela"><summary>1 &middot; Digitalizar, en sentido estricto</summary>
        <div class="resp-cuerpo"><p>Convertir una se&ntilde;al o un soporte anal&oacute;gico en una representaci&oacute;n
        num&eacute;rica discreta &mdash;muestrear y cuantificar&mdash;. Escanear un plano.</p></div></details>
      <details class="resp revela"><summary>2 &middot; Digitalizaci&oacute;n de procesos</summary>
        <div class="resp-cuerpo"><p>Redise&ntilde;ar una actividad para que el flujo de informaci&oacute;n sea digital
        de principio a fin. <b>No consiste en escanear la factura, sino en que ya no haya factura en
        papel.</b></p></div></details>
      <details class="resp revela"><summary>3 &middot; Transformaci&oacute;n digital, en sentido amplio</summary>
        <div class="resp-cuerpo"><p>El cambio estructural que todo eso provoca en la econom&iacute;a, el trabajo,
        la cultura y el poder.</p></div></details>
      <p>Lo que hace singular a esta tecnolog&iacute;a es una propiedad econ&oacute;mica poco intuitiva: el <b>coste
         marginal de reproducci&oacute;n es pr&aacute;cticamente cero</b>. Producir la copia n&uacute;mero un mill&oacute;n cuesta
         lo mismo que producir la segunda.</p>
      <div class="reto-piensa">
        <span class="n-tag">Antes de mirar</span>
        <p>Esa sola propiedad explica casi todo lo que ves a tu alrededor en internet.
           <b>&iquest;Qu&eacute; consecuencias se te ocurren?</b> Piensa en por qu&eacute; hay servicios enormes que no te
           cobran nada, y en por qu&eacute; son siempre las mismas cuatro empresas.</p>
      </div>
      <details class="resp revela"><summary>Ver las consecuencias</summary><div class="resp-cuerpo">
      <p>De esa propiedad se derivan casi todos los fen&oacute;menos que observas: plataformas globales, contenidos
         aparentemente gratuitos financiados con datos, concentraci&oacute;n de mercado en muy pocas empresas y
         una propiedad intelectual dif&iacute;cil de hacer cumplir.</p>

      <div class="escena">
        <div class="escena-barra">
          <span class="escena-titulo">Coste de producir copias</span>
          <div class="seg"><button type="button" id="tabla-coste" aria-pressed="false">Ver los datos</button></div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 300" id="svg-coste" role="img"
               aria-label="Gráfico de líneas: el coste de producir copias analógicas crece de forma constante mientras el de las digitales se mantiene plano tras la primera">
            <!-- rejilla -->
            <g stroke="var(--line-soft)" stroke-width="1">
              <path d="M70 40 H600"/><path d="M70 92 H600"/><path d="M70 144 H600"/>
              <path d="M70 196 H600"/>
            </g>
            <path d="M70 248 H600" stroke="var(--ink-soft)" stroke-width="1.5"/>
            <path d="M70 40 V248" stroke="var(--ink-soft)" stroke-width="1.5"/>

            <!-- eje Y -->
            <g class="ejeq" text-anchor="end">
              <text x="60" y="44">2.000 €</text><text x="60" y="96">1.500 €</text>
              <text x="60" y="148">1.000 €</text><text x="60" y="200">500 €</text>
              <text x="60" y="252">0 €</text>
            </g>
            <!-- eje X -->
            <g class="ejeq" text-anchor="middle">
              <text x="70" y="268">0</text><text x="203" y="268">250</text>
              <text x="336" y="268">500</text><text x="468" y="268">750</text>
              <text x="600" y="268">1.000</text>
              <text x="336" y="288" style="font-size:10.5px">COPIAS PRODUCIDAS</text>
            </g>

            <!-- analogico: 2 euros por copia -->
            <path d="M70 248 L600 40" fill="none" stroke="var(--c-analog)" stroke-width="2"
                  stroke-linecap="round"/>
            <!-- digital: 300 euros de produccion y ya -->
            <path d="M70 248 L83 217 L600 216" fill="none" stroke="var(--c-digital)" stroke-width="2"
                  stroke-linecap="round"/>

            <!-- etiquetas directas -->
            <circle cx="600" cy="40" r="4.5" fill="var(--c-analog)" stroke="var(--surface)" stroke-width="2"/>
            <text x="592" y="34" text-anchor="end" class="etq">ANAL&Oacute;GICO &middot; 2.000 &euro;</text>
            <circle cx="600" cy="216" r="4.5" fill="var(--c-digital)" stroke="var(--surface)" stroke-width="2"/>
            <text x="592" y="210" text-anchor="end" class="etq">DIGITAL &middot; 300 &euro;</text>
          </svg>
        </div>
        <div class="pie">
          <p style="margin:0 0 8px">Un disco prensado cuesta unos 2&nbsp;&euro; por unidad: mil copias son mil
            veces ese coste. Un archivo cuesta producirlo <b>una vez</b> &mdash;grabar, mezclar, masterizar&mdash;
            y a partir de ah&iacute; la copia n&uacute;mero mil cuesta pr&aacute;cticamente lo mismo que la segunda: nada.</p>
          <p style="margin:0"><b>Eso es el coste marginal cero</b>, y de ah&iacute; sale casi todo lo dem&aacute;s:
            por qu&eacute; hay servicios enormes que no te cobran, por qu&eacute; el que llega primero se lo queda todo,
            y por qu&eacute; la propiedad intelectual se volvi&oacute; tan dif&iacute;cil de hacer cumplir.</p>
          <table id="datos-coste" hidden style="width:100%;border-collapse:collapse;font-size:13.5px;margin-top:12px">
            <tr style="text-align:left;border-bottom:2px solid var(--ink)">
              <th style="padding:6px">Copias</th><th style="padding:6px">Anal&oacute;gico</th><th style="padding:6px">Digital</th></tr>
            <tr style="border-bottom:1px solid var(--line)"><td style="padding:6px">1</td><td style="padding:6px">302 &euro;</td><td style="padding:6px">300 &euro;</td></tr>
            <tr style="border-bottom:1px solid var(--line)"><td style="padding:6px">250</td><td style="padding:6px">500 &euro;</td><td style="padding:6px">300 &euro;</td></tr>
            <tr style="border-bottom:1px solid var(--line)"><td style="padding:6px">500</td><td style="padding:6px">1.000 &euro;</td><td style="padding:6px">300 &euro;</td></tr>
            <tr style="border-bottom:1px solid var(--line)"><td style="padding:6px">750</td><td style="padding:6px">1.500 &euro;</td><td style="padding:6px">300 &euro;</td></tr>
            <tr><td style="padding:6px">1.000</td><td style="padding:6px">2.000 &euro;</td><td style="padding:6px">300 &euro;</td></tr>
          </table>
        </div>
      </div>
      <script>
      (function(){
        var b = document.getElementById('tabla-coste'), t = document.getElementById('datos-coste');
        if(!b || !t) return;
        b.addEventListener('click', function(){
          t.hidden = !t.hidden;
          b.setAttribute('aria-pressed', t.hidden ? 'false' : 'true');
          b.textContent = t.hidden ? 'Ver los datos' : 'Ocultar los datos';
        });
      })();
      </script>

      </div></details>
      <p>A esto se suma una segunda propiedad: la informaci&oacute;n digital es <b>procesable por m&aacute;quinas</b>.
         No solo se guarda y se transmite, sino que se puede buscar, cruzar, analizar y usar para entrenar
         sistemas que toman decisiones. Ah&iacute; es donde la digitalizaci&oacute;n deja de ser una cuesti&oacute;n t&eacute;cnica
         y pasa a ser una cuesti&oacute;n pol&iacute;tica: qui&eacute;n tiene los datos, con qu&eacute; criterio decide el algoritmo
         y qui&eacute;n responde cuando se equivoca.</p>
      <div class="aviso">
        <span class="n-tag">Para el debate</span>
        A la digitalizaci&oacute;n se le atribuye ser <b>inmaterial</b>, y no lo es. Los centros de datos consumen
        electricidad y agua, los dispositivos requieren minerales cr&iacute;ticos extra&iacute;dos en condiciones a
        menudo cuestionables, y la obsolescencia genera un residuo electr&oacute;nico que crece m&aacute;s r&aacute;pido que
        cualquier otro. La nube est&aacute; hecha de hierro, cobre y refrigeraci&oacute;n. Evaluar una tecnolog&iacute;a
        exige contar tambi&eacute;n lo que no se ve.
      </div>
"""

    # --- 03 practica ---
    if es2:
        practica = u"""
          <h4>Qu&eacute; hay que hacer</h4>
          <ol class="pasos">
            <li>Elige <b>un objeto</b> que hayas usado hoy. Cualquiera, cuanto m&aacute;s tonto mejor: una cuchara,
                una cremallera, un boli.</li>
            <li>Escribe qu&eacute; <b>necesidad</b> resuelve. En una frase.</li>
            <li>Explica c&oacute;mo se resolv&iacute;a esa misma necesidad <b>hace 200 a&ntilde;os</b>. Y hace 2.000.</li>
            <li>Di qu&eacute; <b>t&eacute;cnica</b> hace falta para fabricarlo y qu&eacute; <b>ciencia</b> hay detr&aacute;s.</li>
            <li>Termina con una predicci&oacute;n: &iquest;c&oacute;mo crees que ser&aacute; dentro de 50 a&ntilde;os?</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>La necesidad est&aacute; bien identificada y no se confunde con el objeto <b>(3 puntos)</b>.</li>
            <li>La comparaci&oacute;n hist&oacute;rica es correcta y concreta <b>(3 puntos)</b>.</li>
            <li>Distingue bien t&eacute;cnica de ciencia <b>(3 puntos)</b>.</li>
            <li>La predicci&oacute;n est&aacute; razonada, no es una ocurrencia <b>(1 punto)</b>.</li>
          </ul>"""
    else:
        practica = u"""
          <h4>Qu&eacute; hay que hacer</h4>
          <p>An&aacute;lisis por parejas de <b>una tecnolog&iacute;a decisiva</b> a elegir entre las nueve de la l&iacute;nea del
             tiempo. Entrega: una cara de folio, estructurada as&iacute;.</p>
          <ol class="pasos">
            <li><b>Qu&eacute; problema resolv&iacute;a</b> y qu&eacute; se hac&iacute;a antes.</li>
            <li><b>Qu&eacute; hizo falta</b> para que apareciera: &iquest;conocimiento cient&iacute;fico previo, destreza
                t&eacute;cnica acumulada, un material nuevo, una necesidad econ&oacute;mica?</li>
            <li><b>Qu&eacute; cambi&oacute; en la sociedad</b>: trabajo, poblaci&oacute;n, ciudades, poder.</li>
            <li><b>Qu&eacute; problema nuevo cre&oacute;</b> y cu&aacute;nto tard&oacute; en regularse, si es que se regul&oacute;.</li>
            <li><b>Paralelismo con hoy</b>: qu&eacute; tecnolog&iacute;a actual est&aacute; en una fase parecida y por qu&eacute;.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Los cuatro primeros apartados est&aacute;n completos y documentados <b>(4 puntos)</b>.</li>
            <li>Distingue las aportaciones de la ciencia y de la t&eacute;cnica en el caso elegido <b>(2 puntos)</b>.</li>
            <li>El an&aacute;lisis de consecuencias va m&aacute;s all&aacute; de lo obvio <b>(2 puntos)</b>.</li>
            <li>El paralelismo con el presente est&aacute; argumentado <b>(2 puntos)</b>.</li>
          </ul>"""

    # --- 04 cierre ---
    if es2:
        cierre = u"""
        <li>Un carpintero que hace sillas preciosas pero no sabe explicar por qu&eacute; la madera se comba, &iquest;tiene t&eacute;cnica, ciencia o tecnolog&iacute;a?
          <details class="resp"><summary>Ver respuesta</summary><div class="resp-cuerpo"><p><b>T&eacute;cnica.</b> Sabe hacerlo muy bien, que es justo lo que define a la t&eacute;cnica. Le falta la explicaci&oacute;n, que ser&iacute;a la ciencia.</p></div></details></li>
        <li>&iquest;Cu&aacute;l dir&iacute;as que fue la primera tecnolog&iacute;a de la historia?
          <details class="resp"><summary>Ver respuesta</summary><div class="resp-cuerpo"><p><b>La piedra tallada</b>, hace unos 2,6 millones de a&ntilde;os. Es la primera vez que se fabrica una herramienta a prop&oacute;sito en vez de usar lo que se encuentra.</p></div></details></li>
        <li>Di una cosa buena y una mala que haya tra&iacute;do internet.
          <details class="resp"><summary>Ver respuesta</summary><div class="resp-cuerpo"><p>Respuesta abierta. Buena: acceso al conocimiento desde cualquier sitio. Mala: bulos, adicci&oacute;n o que quien no tiene conexi&oacute;n se queda fuera de todo. Lo importante es que veas que <b>casi toda tecnolog&iacute;a trae las dos cosas a la vez</b>.</p></div></details></li>"""
    else:
        cierre = u"""
        <li>&iquest;Por qu&eacute; se dice que la t&eacute;cnica es anterior a la ciencia?
          <details class="resp"><summary>Ver respuesta</summary><div class="resp-cuerpo"><p>Porque durante millones de a&ntilde;os se fabricaron herramientas eficaces <b>sin ninguna explicaci&oacute;n te&oacute;rica</b> de por qu&eacute; funcionaban: se tallaba s&iacute;lex sin mineralog&iacute;a y se fund&iacute;a bronce sin qu&iacute;mica. La ciencia solo empieza a guiar sistem&aacute;ticamente a la t&eacute;cnica a partir del siglo XVIII.</p></div></details></li>
        <li>Pon un ejemplo de tecnolog&iacute;a que empujara a la ciencia, y no al rev&eacute;s.
          <details class="resp"><summary>Ver respuesta</summary><div class="resp-cuerpo"><p>La <b>m&aacute;quina de vapor</b>: funcionaba y se vend&iacute;a d&eacute;cadas antes de que Carnot y Clausius formularan la termodin&aacute;mica. Fue la necesidad de mejorar su rendimiento la que oblig&oacute; a desarrollar esa ciencia.</p></div></details></li>
        <li>&iquest;Es neutral la tecnolog&iacute;a? Justifica la respuesta.
          <details class="resp"><summary>Ver respuesta</summary><div class="resp-cuerpo"><p>Puede serlo en su <b>intenci&oacute;n</b>, pero nunca en sus <b>consecuencias</b>. Toda tecnolog&iacute;a reparte de forma desigual beneficios y perjuicios, favorece a unos grupos sobre otros y abre problemas que nadie hab&iacute;a previsto. Por eso su evaluaci&oacute;n no es solo t&eacute;cnica: tambi&eacute;n es &eacute;tica y pol&iacute;tica.</p></div></details></li>"""

    reto = (u"""<p>Sin mirar el m&oacute;vil: escribe en 60 segundos <b>cinco objetos</b> que hayas usado hoy antes de
        entrar en clase. Ahora t&aacute;chalos todos menos uno, el que m&aacute;s te costar&iacute;a vivir sin &eacute;l.</p>
      <p>&iquest;Lo tienes? Pues alguien tuvo que <b>inventarlo</b>, alguien tuvo que aprender a <b>fabricarlo</b>
        y alguien tuvo que averiguar <b>por qu&eacute; funciona</b>. Esas tres cosas son distintas, y hoy vamos a
        separarlas.</p>"""
        if es2 else
        u"""<p>Escribe una definici&oacute;n de <b>tecnolog&iacute;a</b> en una sola frase, sin mirar nada. Tienes dos minutos.</p>
      <details class="resp revela"><summary>Solo cuando ya la tengas escrita</summary>
        <div class="resp-cuerpo">
          <p>Comprueba una cosa: <b>&iquest;has escrito una lista de aparatos?</b> Si tu definici&oacute;n menciona
             m&oacute;viles, ordenadores o m&aacute;quinas, es probable que hayas definido <b>los productos</b> de la
             tecnolog&iacute;a y no la tecnolog&iacute;a misma.</p>
          <p>No pasa nada: es lo que contesta casi todo el mundo, y precisamente por eso empezamos aqu&iacute;.
             <b>Guarda tu frase</b> sin corregirla. La revisaremos al final de la sesi&oacute;n, cuando tengas
             con qu&eacute; compararla.</p>
        </div></details>""")

    return u"""
<header class="top">
  <div class="wrap">
    <div class="eyebrow">%(migas)s</div>
    <h1>%(h1)s</h1>
    <nav class="sesiones" aria-label="Sesiones del tema">
      <button type="button" aria-pressed="true">Sesi&oacute;n &uacute;nica &middot; 60 min</button>
    </nav>
  </div>
</header>

<main class="wrap">
  <div class="ses-head">
    <div class="eyebrow">Sesi&oacute;n introductoria &middot; 60 minutos</div>
    <h2>%(titulo_h2)s</h2>
    <p>%(entradilla)s</p>
    <div class="minutado">
      <span class="min"><b>5'</b> Reto inicial</span>
      <span class="min"><b>20'</b> Teor&iacute;a</span>
      <span class="min"><b>15'</b> L&iacute;nea del tiempo</span>
      <span class="min"><b>15'</b> Pr&aacute;ctica</span>
      <span class="min"><b>5'</b> Cierre</span>
    </div>
    <div class="chips">%(chips)s</div>
  </div>

  <section class="bloque">
    <div class="rotulo"><span class="num">00</span> Reto inicial &middot; 5 min</div>
    %(reto)s
  </section>

  <section class="bloque">
    <div class="rotulo"><span class="num">01</span> Teor&iacute;a &middot; 20 min</div>
    %(teoria)s
  </section>

  <section class="bloque">
    <div class="rotulo"><span class="num">02</span> La tecnolog&iacute;a desde el principio &middot; 15 min</div>
    <p>Dos millones y medio de a&ntilde;os en una l&iacute;nea. Pulsa cada hito para ver qu&eacute; cambi&oacute;.
       Fíjate en una cosa mientras avanzas: <b>las distancias entre hitos se acortan</b>.</p>
    <div class="escena" id="esc-tiempo">
      <div class="escena-barra">
        <span class="escena-titulo">De la piedra tallada a la inteligencia artificial</span>
        <div class="seg" id="seg-tiempo">
          <button type="button" data-ir="ant" aria-pressed="false">&#9664; Anterior</button>
          <button type="button" data-ir="sig" aria-pressed="true">Siguiente &#9654;</button>
          <button type="button" data-ir="voz" aria-pressed="false">&#128266; Que lo cuente</button>
          <button type="button" data-ir="stop" aria-pressed="false">&#9632; Parar</button>
        </div>
      </div>
      <div class="lienzo">
        <svg viewBox="0 0 640 210" id="svg-tiempo" role="img" aria-label="L&iacute;nea del tiempo de la tecnolog&iacute;a"></svg>
      </div>
      <div class="pie" id="pie-tiempo">
        <div class="narra">
          <div class="avatar-caja" id="avatar-caja"></div>
          <div class="globo"><span id="txt-tiempo"></span>
            <div class="avatar-dice" id="avatar-dice"></div></div>
        </div>
        <div id="sel-voz" style="margin-top:10px"></div>
        <p class="voz-no" id="aviso-voz" hidden>Este navegador no puede leer el texto en voz alta. El
          contenido est&aacute; escrito arriba.</p>
      </div>
    </div>
    <div class="nota">
      <span class="n-tag">Lo que dice la l&iacute;nea</span>
      Entre la piedra tallada y la agricultura pasaron <b>dos millones y medio de a&ntilde;os</b>. Entre la
      m&aacute;quina de vapor y el chip, doscientos. Entre el chip y la IA que llevas en el bolsillo, cincuenta.
      La tecnolog&iacute;a no avanza a ritmo constante: <b>se acelera</b>, porque cada invento se apoya en todos
      los anteriores.
    </div>
    <h3>Las cuatro revoluciones industriales</h3>
    <p>Cuatro momentos en que cambi&oacute; <b>la forma de fabricar</b>, y con ella el mundo entero. F&iacute;jate en qui&eacute;n hace el trabajo en cada foto.</p>
    <div class="galeria-ri">
        <figure class="foto">
          <img src="../../../img/ri1-telar.jpg" alt="Telar mec&aacute;nico en una f&aacute;brica textil de 1835" loading="lazy">
          <figcaption><b>1.&ordf; revoluci&oacute;n</b> &middot; Telar mec&aacute;nico, 1835. El vapor mueve las m&aacute;quinas; las personas pasan a vigilarlas.
            <span class="credito">T. Allom y J. Tingle &middot; Dominio p&uacute;blico &middot; <a href="https://commons.wikimedia.org/wiki/File:Powerloom%%20weaving%%20in%%201835.jpg" target="_blank" rel="noopener">Wikimedia Commons</a></span>
          </figcaption>
        </figure>
        <figure class="foto">
          <img src="../../../img/ri2-ford.jpg" alt="Cadena de montaje de la f&aacute;brica Ford en 1913" loading="lazy">
          <figcaption><b>2.&ordf; revoluci&oacute;n</b> &middot; Cadena de montaje de Ford, 1913. Electricidad y producci&oacute;n en serie: el coche deja de ser un lujo.
            <span class="credito">Autor desconocido &middot; Dominio p&uacute;blico &middot; <a href="https://commons.wikimedia.org/wiki/File:Ford%%20assembly%%20line%%20-%%201913.jpg" target="_blank" rel="noopener">Wikimedia Commons</a></span>
          </figcaption>
        </figure>
        <figure class="foto">
          <img src="../../../img/ri3-intel4004.jpg" alt="Microprocesador Intel 4004 de 1971 visto de cerca" loading="lazy">
          <figcaption><b>3.&ordf; revoluci&oacute;n</b> &middot; El Intel 4004, 1971. Un ordenador entero en una pieza del tama&ntilde;o de una u&ntilde;a.
            <span class="credito">Thomas Nguyen &middot; CC BY-SA 4.0 &middot; <a href="https://commons.wikimedia.org/wiki/File:Intel%%20C4004.jpg" target="_blank" rel="noopener">Wikimedia Commons</a></span>
          </figcaption>
        </figure>
        <figure class="foto">
          <img src="../../../img/ri4-robots.jpg" alt="Brazos rob&oacute;ticos industriales apilando pan en una f&aacute;brica" loading="lazy">
          <figcaption><b>4.&ordf; revoluci&oacute;n</b> &middot; Robots coordinados por software. Las m&aacute;quinas ya no solo ejecutan: deciden.
            <span class="credito">KUKA Roboter GmbH &middot; Dominio p&uacute;blico &middot; <a href="https://commons.wikimedia.org/wiki/File:Factory%%20Automation%%20Robotics%%20Palettizing%%20Bread.jpg" target="_blank" rel="noopener">Wikimedia Commons</a></span>
          </figcaption>
        </figure>
    </div>

%(video)s
    <h3>La m&aacute;quina que lo empez&oacute; todo</h3>
    <p>De todos los hitos de la l&iacute;nea, ninguno cambi&oacute; tanto en tan poco tiempo. Merece una mirada de cerca.</p>
        <figure class="foto">
          <img src="../../../img/vapor-watt.jpg" alt="M&aacute;quina de vapor de Watt conservada en Madrid" loading="lazy">
          <figcaption>Una m&aacute;quina de vapor de Watt conservada en la Escuela de Ingenieros Industriales de Madrid. No es una r&eacute;plica: es una de aquellas m&aacute;quinas, y puedes ir a verla.
            <span class="credito">Nicol&aacute;s P&eacute;rez &middot; CC BY-SA 3.0 &middot; <a href="https://commons.wikimedia.org/wiki/File:Maquina_vapor_Watt_ETSIIM.jpg" target="_blank" rel="noopener">Wikimedia Commons</a></span>
          </figcaption>
        </figure>
        <figure class="foto">
          <img src="../../../img/vapor-grabado.png" alt="Grabado t&eacute;cnico de la m&aacute;quina de Boulton y Watt de 1784" loading="lazy">
          <figcaption>El grabado original de la m&aacute;quina de Boulton &amp; Watt, 1784. Es un <b>plano t&eacute;cnico</b>, y por eso sabemos hoy exactamente c&oacute;mo estaba hecha. Sin ese dibujo, la m&aacute;quina se habr&iacute;a perdido con quien la construy&oacute;.
            <span class="credito">Robert Henry Thurston &middot; Dominio p&uacute;blico &middot; <a href="https://commons.wikimedia.org/wiki/File:SteamEngine%%20Boulton%%26Watt%%201784.png" target="_blank" rel="noopener">Wikimedia Commons</a></span>
          </figcaption>
        </figure>

  </section>

  <section class="bloque">
    <div class="rotulo"><span class="num">03</span> Pr&aacute;ctica &middot; 15 min</div>
    <div class="ficha">
      <div class="ficha-cab">
        <span>Actividad 0 &middot; %(act)s</span>
        <span class="chips"><span class="chip">1.1</span><span class="chip">A.1</span></span>
        <span>%(modo)s</span>
      </div>
      <div class="ficha-cuerpo">%(practica)s</div>
    </div>
  </section>

  <section class="bloque">
    <div class="rotulo"><span class="num">04</span> Cierre &middot; 5 min</div>
    <p>Ticket de salida. Responde primero en el cuaderno; despu&eacute;s despliega y comprueba.</p>
    <ol>%(cierre)s</ol>
    <div class="nota">
      <span class="n-tag">A partir de aqu&iacute;</span>
      %(siguiente)s
    </div>
  </section>

  %(licencia)s
</main>

<footer><div class="wrap">Tema 0 &middot; %(curso)s &middot; %(materia)s</div></footer>
<script>
var HITOS = %(hitos_js)s;
(function(){
  var svg = document.getElementById('svg-tiempo');
  var pie = document.getElementById('pie-tiempo');
  var seg = document.getElementById('seg-tiempo');
  if(!svg) return;
  var X0 = 42, X1 = 598, Y = 92, i = 0;
  var avisoVoz = document.getElementById('aviso-voz');

  /* ---------- avatar que cambia de epoca y narra ---------- */
  var CARAS = {
    piedra:  {pelo:'<path d="M14 26 q4 -14 18 -14 q14 0 18 14 q-6 -4 -18 -4 q-12 0 -18 4 Z" fill="#6b4f3a"/>'
                   +'<path d="M18 20 l-5 -7 M46 20 l5 -7" stroke="#6b4f3a" stroke-width="3" stroke-linecap="round"/>',
              prop:'<path d="M70 44 l16 -16 q4 -4 8 0 q4 4 0 8 l-16 16 q-4 4 -8 0 q-4 -4 0 -8 Z" fill="#8a6a4a" stroke="#5f472f" stroke-width="1.5"/>',
              dice:'¡Con esto corto lo que quiera!'},
    fuego:   {pelo:'<path d="M14 26 q4 -14 18 -14 q14 0 18 14 q-6 -4 -18 -4 q-12 0 -18 4 Z" fill="#6b4f3a"/>',
              prop:'<path d="M78 56 v-20" stroke="#8a6a4a" stroke-width="5" stroke-linecap="round"/>'
                   +'<path d="M78 36 q-9 -7 0 -18 q9 11 0 18 Z" fill="#fbbc04"/>'
                   +'<path d="M78 33 q-5 -4 0 -10 q5 6 0 10 Z" fill="#ea4335"/>',
              dice:'El fuego no se inventa: se cuida.'},
    agri:    {pelo:'<path d="M8 22 h48 l-6 -6 h-36 Z" fill="#d9a441"/><path d="M10 22 h44" stroke="#b5862c" stroke-width="2"/>',
              prop:'<path d="M78 58 v-26" stroke="#9a7326" stroke-width="3" stroke-linecap="round"/>'
                   +'<path d="M78 34 q-7 -5 -6 -12 q7 2 6 12 M78 34 q7 -5 6 -12 q-7 2 -6 12" fill="#34a853"/>',
              dice:'Ya no persigo la comida: la siembro.'},
    rueda:   {pelo:'<path d="M14 24 q4 -12 18 -12 q14 0 18 12 q-6 -3 -18 -3 q-12 0 -18 3 Z" fill="#4a3b2f"/>',
              prop:'<circle cx="80" cy="44" r="16" fill="none" stroke="#8a6a4a" stroke-width="4"/>'
                   +'<circle cx="80" cy="44" r="3.5" fill="#8a6a4a"/>'
                   +'<path d="M80 30 v28 M66 44 h28 M70 34 l20 20 M90 34 l-20 20" stroke="#8a6a4a" stroke-width="2"/>',
              dice:'Redonda. No parece gran cosa, pero lo es.'},
    imprenta:{pelo:'<path d="M10 20 h44 v5 h-44 Z M20 20 v-6 h24 v6" fill="#2f3a45"/>',
              prop:'<path d="M64 30 h30 v28 h-30 Z" fill="#fff" stroke="#5f6368" stroke-width="2"/>'
                   +'<path d="M79 30 v28" stroke="#5f6368" stroke-width="2"/>'
                   +'<path d="M68 38 h8 M68 44 h8 M83 38 h8 M83 44 h8" stroke="#9aa0a6" stroke-width="1.6"/>',
              dice:'Cientos de copias en una semana.'},
    vapor:   {pelo:'<path d="M16 22 h32 v3 h-32 Z M22 22 v-14 h20 v14" fill="#2f3a45"/>',
              prop:'<circle cx="80" cy="44" r="13" fill="none" stroke="#5f6368" stroke-width="4"/>'
                   +'<circle cx="80" cy="44" r="4" fill="#5f6368"/>'
                   +'<path d="M80 27 v6 M80 55 v6 M63 44 h6 M91 44 h6 M69 33 l4 4 M87 51 l4 4 M91 33 l-4 4 M73 51 l-4 4" stroke="#5f6368" stroke-width="3" stroke-linecap="round"/>',
              dice:'Trabaja sin cansarse. Ni un músculo.'},
    electri: {pelo:'<path d="M14 24 q4 -12 18 -12 q14 0 18 12 q-6 -3 -18 -3 q-12 0 -18 3 Z" fill="#3a3a42"/>',
              prop:'<path d="M80 30 a12 12 0 0 1 8 21 v5 h-16 v-5 a12 12 0 0 1 8 -21 Z" fill="#fbbc04" stroke="#9a7326" stroke-width="1.6"/>'
                   +'<path d="M72 58 h16 M74 62 h12" stroke="#9a7326" stroke-width="2.4" stroke-linecap="round"/>',
              dice:'La energía llega por un cable.'},
    electro: {pelo:'<path d="M14 24 q4 -12 18 -12 q14 0 18 12 q-6 -3 -18 -3 q-12 0 -18 3 Z" fill="#2f3a45"/>',
              prop:'<rect x="66" y="32" width="28" height="24" rx="2" fill="#34a853" stroke="#1e6b33" stroke-width="1.6"/>'
                   +'<g stroke="#1e6b33" stroke-width="2"><path d="M72 32 v-5 M80 32 v-5 M88 32 v-5 M72 56 v5 M80 56 v5 M88 56 v5"/></g>'
                   +'<rect x="74" y="40" width="12" height="8" fill="#1e6b33"/>',
              dice:'Un interruptor diminuto. Millones de ellos.'},
    digital: {pelo:'<path d="M14 24 q4 -12 18 -12 q14 0 18 12 q-6 -3 -18 -3 q-12 0 -18 3 Z" fill="#2f3a45"/>',
              prop:'<rect x="68" y="26" width="24" height="36" rx="4" fill="#fff" stroke="#202124" stroke-width="2"/>'
                   +'<rect x="71" y="31" width="18" height="24" fill="#e8f0fe"/>'
                   +'<path d="M74 38 h12 M74 43 h12 M74 48 h8" stroke="#4285f4" stroke-width="1.8"/>'
                   +'<circle cx="80" cy="59" r="1.6" fill="#202124"/>',
              dice:'Esto tiene más potencia que el Apolo 11.'}
  };

  function dibujaAvatar(id, hablando){
    var c = CARAS[id] || CARAS.piedra;
    var boca = hablando
      ? '<ellipse cx="32" cy="46" rx="6" ry="5" fill="#8c3b2e"/>'
      : '<path d="M25 45 q7 6 14 0" fill="none" stroke="#8c3b2e" stroke-width="2.6" stroke-linecap="round"/>';
    return '<svg viewBox="0 0 104 72" class="avatar' + (hablando ? ' habla' : '') + '" aria-hidden="true">'
      + '<ellipse cx="32" cy="38" rx="21" ry="23" fill="#f3d3b3" stroke="#c9a583" stroke-width="1.5"/>'
      + c.pelo
      + '<circle cx="24" cy="34" r="3.4" fill="#2f3a45"/><circle cx="40" cy="34" r="3.4" fill="#2f3a45"/>'
      + '<circle cx="25.2" cy="32.8" r="1.2" fill="#fff"/><circle cx="41.2" cy="32.8" r="1.2" fill="#fff"/>'
      + '<circle cx="17" cy="45" r="3.2" fill="#ea4335" opacity=".22"/>'
      + '<circle cx="47" cy="45" r="3.2" fill="#ea4335" opacity=".22"/>'
      + boca + c.prop + '</svg>';
  }

  /* ---------- voz ---------- */
  var vozES = null, hayVoz = ('speechSynthesis' in window);
  /* las voces dependen del navegador y del sistema; se ordenan por calidad conocida */
  function puntua(v){
    var n = (v.name || '').toLowerCase();
    var p = 0;
    if(/natural|neural/.test(n)) p += 100;   /* Edge: Microsoft ... Online (Natural) */
    if(/online/.test(n))         p += 40;
    if(/premium|enhanced/.test(n)) p += 60;  /* macOS/iOS mejoradas */
    if(/google/.test(n))         p += 50;    /* Chrome de escritorio */
    if(/^es-es/i.test(v.lang))   p += 10;    /* castellano antes que otras variantes */
    if(v.localService === false) p += 5;
    return p;
  }
  function vocesES(){
    if(!hayVoz) return [];
    return window.speechSynthesis.getVoices()
      .filter(function(v){ return /^es/i.test(v.lang); })
      .sort(function(a, b){ return puntua(b) - puntua(a); });
  }
  function eligeVoz(){
    var vs = vocesES();
    if(!vs.length) return;
    var guardada = null;
    try{ guardada = localStorage.getItem('voz-tema0'); }catch(e){}
    vozES = vs.filter(function(v){ return v.name === guardada; })[0] || vs[0];
    pintaSelector(vs);
  }
  function pintaSelector(vs){
    var cont = document.getElementById('sel-voz');
    if(!cont || vs.length < 2) return;
    cont.innerHTML = '<label style="font-family:var(--f-m);font-size:11px;color:var(--ink-soft)">Voz: ' +
      '<select id="voz-pick" style="font:inherit;padding:3px 6px;border:1px solid var(--line);' +
      'border-radius:2px;background:var(--surface);color:var(--ink);max-width:230px">' +
      vs.map(function(v){
        return '<option value="' + v.name + '"' + (vozES && v.name === vozES.name ? ' selected' : '') + '>' +
               v.name.replace(/Microsoft |Spanish \(Spain\)|- /g, '').trim() + '</option>';
      }).join('') + '</select></label>';
    cont.querySelector('#voz-pick').addEventListener('change', function(){
      vozES = vs.filter(function(v){ return v.name === this.value; }.bind(this))[0] || vozES;
      try{ localStorage.setItem('voz-tema0', vozES.name); }catch(e){}
      calla();
    });
  }
  if(hayVoz){ eligeVoz(); window.speechSynthesis.onvoiceschanged = eligeVoz; }

  function limpia(html){
    var d = document.createElement('div'); d.innerHTML = html;
    return d.textContent.replace(/\s+/g, ' ').trim();
  }

  function calla(){
    if(hayVoz) window.speechSynthesis.cancel();
    pintaAvatar(false);
  }

  function narra(){
    if(!hayVoz){
      avisoVoz.hidden = false;
      return;
    }
    window.speechSynthesis.cancel();
    var h = HITOS[i];
    var u = new SpeechSynthesisUtterance(limpia(h.t) + '. ' + limpia(h.ep) + '. ' + limpia(h.c));
    u.lang = 'es-ES';
    if(vozES) u.voice = vozES;
    u.rate = 0.98; u.pitch = 1.06;
    u.onstart = function(){ pintaAvatar(true); };
    u.onend = function(){ pintaAvatar(false); };
    u.onerror = function(){ pintaAvatar(false); };
    window.speechSynthesis.speak(u);
  }


  function pinta(){
    var m = '<path class="eje-t" d="M' + X0 + ' ' + Y + ' L' + X1 + ' ' + Y + '"></path>';
    HITOS.forEach(function(h, k){
      var x = X0 + (X1 - X0) * h.pos;
      var arriba = k %% 2 === 0;
      var yt = arriba ? Y - 30 : Y + 30;
      m += '<path class="eje-t" d="M' + x.toFixed(1) + ' ' + Y + ' L' + x.toFixed(1) + ' ' + yt + '"></path>';
      m += '<circle class="hito' + (k === i ? ' on' : '') + '" data-k="' + k + '" cx="' + x.toFixed(1) +
           '" cy="' + Y + '" r="' + (k === i ? 8 : 5.5) + '"></circle>';
      m += '<text class="rotulo-svg" x="' + x.toFixed(1) + '" y="' + (arriba ? yt - 6 : yt + 14) +
           '" text-anchor="middle" style="font-size:9.5px' + (k === i ? ';fill:var(--goo-azul);font-weight:500' : '') +
           '">' + h.ep + '</text>';
    });
    m += '<text class="rotulo-svg" x="' + X0 + '" y="' + (Y + 68) + '" style="font-size:9px">PASADO</text>';
    m += '<text class="rotulo-svg" x="' + X1 + '" y="' + (Y + 68) + '" text-anchor="end" style="font-size:9px">HOY</text>';
    svg.innerHTML = m;
    var h = HITOS[i];
    document.getElementById('txt-tiempo').innerHTML =
      '<b>' + h.t + '</b> &middot; <span style="font-family:var(--f-m);font-size:12.5px">' + h.ep + '</span><br>' + h.c;
    document.getElementById('avatar-dice').textContent = '— ' + (CARAS[h.id] ? CARAS[h.id].dice : '');
    pintaAvatar(false);
  }
  svg.addEventListener('click', function(e){
    var c = e.target.closest('.hito'); if(!c) return;
    calla(); i = Number(c.dataset.k); pinta();
  });
  function pintaAvatar(hablando){
    var caja = document.getElementById('avatar-caja');
    if(caja) caja.innerHTML = dibujaAvatar(HITOS[i].id, hablando);
  }
  seg.addEventListener('click', function(e){
    var b = e.target.closest('button[data-ir]'); if(!b) return;
    var a = b.dataset.ir;
    if(a === 'voz'){ narra(); return; }
    if(a === 'stop'){ calla(); return; }
    calla();
    i = a === 'sig' ? Math.min(i + 1, HITOS.length - 1) : Math.max(i - 1, 0);
    pinta();
  });
  pinta();
})();

(function(){
  var ol = document.getElementById('secuencia-hist');
  var b  = document.getElementById('btn-secuencia');
  if(!ol || !b) return;
  var items = Array.prototype.slice.call(ol.querySelectorAll('li'));
  var n = 0;
  b.addEventListener('click', function(){
    if(n >= items.length) return;
    items[n].classList.remove('oculto');
    n++;
    if(n >= items.length){ b.disabled = true; b.textContent = 'Los cuatro pasos'; }
    else b.textContent = 'Destapar el paso ' + (n + 1) + ' ▶';
  });
})();

(function(){
  var c = document.getElementById('video-ri');
  if(!c) return;
  var b = c.querySelector('.video-play');
  b.addEventListener('click', function(){
    var f = document.createElement('iframe');
    f.src = 'https://www.youtube-nocookie.com/embed/' + c.dataset.vid + '?autoplay=1&rel=0&modestbranding=1';
    f.title = b.querySelector('.video-txt b').textContent;
    f.allow = 'accelerometer; autoplay; encrypted-media; picture-in-picture';
    f.referrerPolicy = 'strict-origin-when-cross-origin';
    f.allowFullscreen = true;
    b.replaceWith(f);
  });
})();
</script>
%(sello)s
</body>
</html>""" % dict(
        migas=n['migas'], h1=n['h1'], titulo_h2=n['h1'], entradilla=n['entradilla'],
        chips=u''.join([u'<span class="chip%s">%s</span>' % (' sab' if '.' not in c or c.startswith('A') else '', c) for c in n['chips']]),
        reto=reto, teoria=teoria, practica=practica, cierre=cierre,
        act=u'De un objeto a su historia' if es2 else u'An&aacute;lisis de una tecnolog&iacute;a decisiva',
        modo=u'Individual &middot; 15 min' if es2 else u'Parejas &middot; 15 min',
        siguiente=(u'Ya sabes qu&eacute; es la tecnolog&iacute;a y de d&oacute;nde viene. A partir del tema 1 empezamos a hacerla: '
                   u'analizar objetos, dibujarlos y construirlos.' if es2 else
                   u'Con el vocabulario fijado, el curso entra en materia: an&aacute;lisis de sistemas t&eacute;cnicos, '
                   u'dise&ntilde;o y evaluaci&oacute;n de soluciones.'),
        video=(VIDEO_RI if es2 else VIDEO_RI4),
        licencia=aviso_licencia(n['titulo'], SITIO + '/' + n['ruta']),
        curso=n['curso'], materia=n['materia'], hitos_js=hitos_js, sello=SELLO)


for k, n in NIVELES.items():
    canon = SITIO + '/' + n['ruta']
    html = cabeza(n['titulo'], n['desc'], canon) + cuerpo(k, n)
    p = os.path.join(BASE, n['ruta'], 'index.html')
    io.open(p, 'w', encoding='utf-8', newline='').write(html)
    print('generado: %s  (%d bytes)' % (n['ruta'], len(html)))
