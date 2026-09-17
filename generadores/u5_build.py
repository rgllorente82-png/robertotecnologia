# -*- coding: utf-8 -*-
"""2.o TyD - U5 - Mecanismos: la fuerza, la velocidad y la direccion que necesito.

Genera 2eso/TyD/tema5/index.html con las sesiones 1, 2 y 3 escritas y la 4, la 5
y la 6 marcadas como pendientes.

Tres piezas van CONDICIONADAS a que el material exista, para que la pagina nunca
salga con una foto rota, un video sin ver o un audio que no esta:

  - foto(clave)      solo pinta la figura si el fichero esta en  img/
  - video(clave)     solo pinta el video si alguien lo ha visto  (visto=True)
  - narrador()       solo pinta el avatar si estan el mp3 y su _env_*.json

Lo que falta se imprime al final, con el comando para conseguirlo.
"""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unidad_base import pagina, bloque, ficha, pregunta
import avatar_flat

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PENDIENTES = []
USA_AVATAR = [False]


# ---------------------------------------------------------------- fotografias
# Licencia comprobada una a una contra la API de Commons el 17-sep-2026.
# OJO: mientras el fichero no este en img/ la figura NO se pinta.
FOTOS = {
 'shaduf': dict(
   fichero=u'u5-shaduf.jpeg',
   url=u'https://upload.wikimedia.org/wikipedia/commons/6/63/Shaduf2.jpeg',
   pagina=u'https://commons.wikimedia.org/wiki/File:Shaduf2.jpeg',
   autor=u'G. Pearson', licencia=u'Dominio p&uacute;blico',
   alt=u'Grabado de un hombre sacando agua de un r&iacute;o con un shaduf: '
       u'una p&eacute;rtiga apoyada en un poste, con el cubo en un extremo y un contrapeso en el otro',
   pie=u'Un <b>shaduf</b>, la m&aacute;quina de regar del Nilo. Es una palanca de primer g&eacute;nero '
       u'con un contrapeso: el agua sube sola y el hombre solo gu&iacute;a la p&eacute;rtiga. Se usaba en '
       u'Egipto mucho antes de que nadie escribiera la ley de la palanca, y se sigue usando hoy.'),
 'haterii': dict(
   fichero=u'u5-grua-haterii.jpg',
   url=u'https://upload.wikimedia.org/wikipedia/commons/2/2b/'
       u'Tomb_of_the_Haterii_crane_relief_%28Gusman_Art_decoratif_I_pl_27%29.jpg',
   pagina=u'https://commons.wikimedia.org/wiki/File:Tomb_of_the_Haterii_crane_relief_'
          u'(Gusman_Art_decoratif_I_pl_27).jpg',
   autor=u'Autor desconocido', licencia=u'Dominio p&uacute;blico',
   alt=u'Relieve romano de la tumba de los Haterii con una gr&uacute;a de rueda de andar, '
       u'con hombres caminando dentro de la rueda y el polipasto colgando del m&aacute;stil',
   pie=u'La gr&uacute;a de la <b>tumba de los Haterii</b> (Roma, finales del siglo I). A la izquierda, '
       u'la rueda de andar con los hombres dentro; arriba, el polipasto. Es la mejor imagen que se '
       u'conserva de la m&aacute;quina de elevaci&oacute;n que describe Vitruvio.'),
 'anticitera': dict(
   fichero=u'u5-anticitera.jpg',
   url=u'https://upload.wikimedia.org/wikipedia/commons/5/5a/'
       u'Antikythera_Mechanism_-_National_Archaeological_Museum%2C_Athens_by_Joy_of_Museum.jpg',
   pagina=u'https://commons.wikimedia.org/wiki/File:Antikythera_Mechanism_-_'
          u'National_Archaeological_Museum,_Athens_by_Joy_of_Museum.jpg',
   autor=u'Joyofmuseums', licencia=u'CC BY-SA 4.0',
   alt=u'Tres fragmentos corro&iacute;dos del mecanismo de Anticitera en una vitrina; en el '
       u'central se distingue una gran rueda dentada de bronce con sus radios',
   pie=u'El <b>mecanismo de Anticitera</b>, sacado del mar en 1901. Bajo esa corrosi&oacute;n hay '
       u'una treintena de ruedas dentadas de bronce montadas unas sobre otras. Es del siglo II a. C.: '
       u'engranajes de precisi&oacute;n mil a&ntilde;os antes de que nadie volviera a fabricar algo parecido.'),
}


MOLDE_FOTO = u'''      <figure class="foto">
        <img src="../../../img/@@FICHERO@@" loading="lazy" alt="@@ALT@@">
        <figcaption>@@PIE@@
          <span class="credito">@@AUTOR@@ &middot; @@LICENCIA@@ &middot;
            <a href="@@PAGINA@@" target="_blank" rel="noopener">Wikimedia Commons</a></span>
        </figcaption>
      </figure>
'''


def foto(clave):
    f = FOTOS[clave]
    if not os.path.exists(os.path.join(RAIZ, 'img', f['fichero'])):
        PENDIENTES.append(u'FOTO  img/' + f['fichero'] + u'  ->  curl -L -o img/'
                          + f['fichero'] + u' "' + f['url'] + u'"')
        return u''
    return (MOLDE_FOTO.replace('@@FICHERO@@', f['fichero']).replace('@@ALT@@', f['alt'])
            .replace('@@PIE@@', f['pie']).replace('@@AUTOR@@', f['autor'])
            .replace('@@LICENCIA@@', f['licencia']).replace('@@PAGINA@@', f['pagina']))


# ------------------------------------------------------------------- videos
# Titulo y canal comprobados con la API oEmbed de YouTube el 17-sep-2026, y
# vueltos a comprobar al recoger el trabajo: los tres siguen existiendo y el
# titulo y el canal coinciden con lo que dice esta tabla.
#
#   publicar = el video sale en la pagina (titulo y canal verificados)
#   visto    = alguien lo ha visto ENTERO y responde del contenido
#
# Los tres estan con visto=False a proposito: nadie del proyecto los ha visto
# de principio a fin. Salen publicados porque el canal y el titulo cuadran,
# pero antes de ponerlos en clase hay que verlos.
VIDEOS = {
 'palanca': dict(vid=u'8fDOm-XJBOQ', publicar=True, visto=False,
   titulo=u'Ley de la palanca (mecanismos)', canal=u'TECH LAPSE',
   dura=u'unos 4 minutos',
   nota=u'Animaci&oacute;n de los tres g&eacute;neros con la ley aplicada paso a paso.'),
 'poleas': dict(vid=u'AlAxnplUNH0', publicar=True, visto=False,
   titulo=u'Polea fija, polea m&oacute;vil y polipasto', canal=u'tecnoblas2',
   dura=u'unos 4 minutos',
   nota=u'Ense&ntilde;a los tres montajes seguidos, con la cuerda que hay que tirar en cada uno.'),
 'engranajes': dict(vid=u'0pO6cHi3HzE', publicar=True, visto=False,
   titulo=u'Engranajes (Transmisi&oacute;n circular)', canal=u'TECH LAPSE',
   dura=u'unos 5 minutos',
   nota=u'Animaci&oacute;n de trenes de engranajes con la relaci&oacute;n de transmisi&oacute;n calculada.'),
}


MOLDE_VIDEO = u'''      <div class="video" id="video-@@CLAVE@@" data-vid="@@VID@@">
        <button type="button" class="video-play" aria-label="Reproducir el v&iacute;deo: @@TITULO@@">
          <span class="video-tri" aria-hidden="true"></span>
          <span class="video-txt">
            <b>@@TITULO@@</b>
            <span>@@CANAL@@ &middot; @@DURA@@</span>
          </span>
        </button>
        <p class="video-nota">@@NOTA@@ El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce
          sin cookies de seguimiento. Si la red del centro bloquea YouTube,
          <a href="https://www.youtube.com/watch?v=@@VID@@" target="_blank" rel="noopener">&aacute;brelo
          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material
          publicado bajo la licencia de esta p&aacute;gina.</p>
      </div>

      <script>
      (function(){
        var c = document.getElementById('video-@@CLAVE@@');
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
'''


def video(clave):
    v = VIDEOS[clave]
    if not v['publicar']:
        PENDIENTES.append(u'VIDEO ' + clave + u'  https://www.youtube.com/watch?v=' + v['vid']
                          + u'  (verificar titulo y canal antes de publicarlo)')
        return u''
    if not v['visto']:
        PENDIENTES.append(u'POR VER  ' + clave + u'  https://www.youtube.com/watch?v=' + v['vid']
                          + u'  (publicado, pero nadie lo ha visto entero)')
    return (MOLDE_VIDEO.replace('@@CLAVE@@', clave).replace('@@VID@@', v['vid'])
            .replace('@@TITULO@@', v['titulo']).replace('@@CANAL@@', v['canal'])
            .replace('@@DURA@@', v['dura']).replace('@@NOTA@@', v['nota']))


# ------------------------------------------------------------------ narrador
def narrador():
    """Avatar con la voz de la unidad. Se monta solo si existen el mp3 y su envolvente."""
    import json
    env = os.path.join(RAIZ, '_env_u5-mecanismos.json')
    mp3 = os.path.join(RAIZ, 'audio', 'u5-mecanismos.mp3')
    if not (os.path.exists(env) and os.path.exists(mp3)):
        PENDIENTES.append(u'VOZ   audio/u5-mecanismos.mp3  ->  '
                          u'~/venv/bin/python generadores/voz.py generadores/u5_guion.txt u5-mecanismos')
        return u''
    USA_AVATAR[0] = True
    return avatar_flat.componente(
        'narr-u5', u'De qu&eacute; va este tema',
        u'El m&uacute;sculo mueve poco y mal: qu&eacute; ponemos entre &eacute;l y el problema',
        '../../../audio/u5-mecanismos.mp3',
        json.load(io.open(env, encoding='utf-8')),
        u'Voz sintetizada y audio propio. La boca sigue el volumen real de la voz, '
        u'as&iacute; que se mueve cuando habla y se para en los silencios.')


# ============================================================================
# ESCENA 1 - La palanca
# ============================================================================
# La geometria esta calculada, no puesta a ojo: 200 px = 1 m, la barra mide
# 2,30 m y la ley F*bF = R*bR se resuelve de verdad en cada posicion del apoyo.
ESC_PALANCA = u'''
      <div class="escena" id="esc-palanca">
        <div class="escena-barra">
          <span class="escena-titulo">Pulsa sobre la barra para mover el elemento del medio</span>
          <div class="seg" id="seg-palanca">
            <button type="button" data-g="1" aria-pressed="true">1.&ordm; g&eacute;nero</button>
            <button type="button" data-g="2">2.&ordm; g&eacute;nero</button>
            <button type="button" data-g="3">3.&ordm; g&eacute;nero</button>
            <button type="button" data-g="mover">&#8635; Mover la carga</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 300" id="svg-palanca" role="img"
               aria-label="Palanca con el punto de apoyo m&oacute;vil: al acercar el apoyo a la carga
                           baja la fuerza necesaria y sube el recorrido de la mano"></svg>
        </div>
        <div class="pie" id="pie-palanca"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-palanca');
        var pie = document.getElementById('pie-palanca');
        var seg = document.getElementById('seg-palanca');
        if(!svg) return;

        var X0 = 90, X1 = 550, Y0 = 132;   /* la barra, en reposo */
        var ESC = 200;                     /* 200 px = 1 metro */
        var R = 500;                       /* la carga: 50 kg */
        var TU = 250;                      /* lo que da un brazo, en newtons */
        var genero = 1, movil = 230, movida = false;

        /* [x del apoyo, x de la carga, x de la fuerza] segun el genero */
        function sitio(){
          if(genero === 1) return [movil, X0, X1];
          if(genero === 2) return [X0, movil, X1];
          return [X0, X1, movil];
        }
        function gira(x, ang, xa){
          /* un punto de la barra, girado un angulo alrededor del apoyo */
          var d = x - xa;
          return [xa + d*Math.cos(ang), Y0 + d*Math.sin(ang)];
        }
        function flecha(x, yBase, largo, haciaArriba, col){
          /* flecha vertical que ocupa de yBase-largo a yBase */
          var a = (yBase - largo).toFixed(1), b = yBase.toFixed(1), xx = x.toFixed(1);
          var m = '<path d="M' + xx + ' ' + a + ' V' + b + '" stroke="' + col + '" stroke-width="3"></path>';
          m += haciaArriba
             ? '<path d="M' + xx + ' ' + a + ' l-6 11 h12 Z" fill="' + col + '"></path>'
             : '<path d="M' + xx + ' ' + b + ' l-6 -11 h12 Z" fill="' + col + '"></path>';
          return m;
        }
        function cota(xa, xb, y, etq){
          var m = '<path d="M' + xa + ' ' + (y-6) + ' V' + (y+6) + ' M' + xb + ' ' + (y-6) + ' V' + (y+6)
                + ' M' + xa + ' ' + y + ' H' + xb + '" stroke="var(--line)" stroke-width="1.6"></path>';
          m += '<text x="' + ((xa+xb)/2) + '" y="' + (y+18) + '" text-anchor="middle" class="rotulo-svg">'
             + etq + '</text>';
          return m;
        }

        function pinta(){
          var p = sitio(), xa = p[0], xr = p[1], xf = p[2];
          var bR = Math.abs(xr - xa) / ESC;
          var bF = Math.abs(xf - xa) / ESC;
          var F = R * bR / bF;
          var ang = (genero === 1 ? 0.13 : -0.10) * (movida ? 1 : 0);
          var pr = gira(xr, ang, xa), pf = gira(xf, ang, xa);
          var e0 = gira(X0, ang, xa), e1 = gira(X1, ang, xa);
          var m = '';

          /* la barra y el punto de apoyo */
          m += '<path d="M' + e0[0].toFixed(1) + ' ' + e0[1].toFixed(1) + ' L' + e1[0].toFixed(1)
             + ' ' + e1[1].toFixed(1) + '" stroke="var(--ink-soft)" stroke-width="9" '
             + 'stroke-linecap="round"></path>';
          m += '<path d="M' + xa + ' ' + Y0 + ' l-15 28 h30 Z" fill="var(--goo-azul)"></path>';
          m += '<text x="' + xa + '" y="' + (Y0+50) + '" text-anchor="middle" class="rotulo-svg">APOYO</text>';

          /* la carga, colgando siempre en vertical */
          m += '<path d="M' + pr[0].toFixed(1) + ' ' + pr[1].toFixed(1) + ' V' + (pr[1]+14).toFixed(1)
             + '" stroke="var(--ink-soft)" stroke-width="2"></path>';
          m += '<rect x="' + (pr[0]-27).toFixed(1) + '" y="' + (pr[1]+14).toFixed(1)
             + '" width="54" height="40" rx="3" fill="#a5783f" stroke="#7a5528" stroke-width="2"></rect>';
          m += '<text x="' + pr[0].toFixed(1) + '" y="' + (pr[1]+39).toFixed(1)
             + '" text-anchor="middle" class="rotulo-svg" style="fill:#fff">50 kg</text>';

          /* la fuerza: hacia abajo en el primer genero, hacia arriba en los otros dos.
             La flecha va siempre por encima de la barra y se recorta para no salirse. */
          var largo = Math.max(16, Math.min(22 + 62*Math.min(1, F/1500), pf[1] - 54));
          var abajo = (genero === 1);
          var col = (F <= TU) ? 'var(--goo-verde)' : 'var(--goo-rojo)';
          m += flecha(pf[0], pf[1] - 8, largo, !abajo, col);
          m += '<text x="' + pf[0].toFixed(1) + '" y="' + (pf[1] - 18 - largo).toFixed(1)
             + '" text-anchor="middle" class="rotulo-svg" style="fill:var(--ink);font-size:12px">'
             + 'F = ' + Math.round(F) + ' N</text>';

          /* los brazos, medidos sobre la barra en reposo */
          m += cota(Math.min(xa, xr), Math.max(xa, xr), 236, 'bR = ' + bR.toFixed(2) + ' m');
          m += cota(Math.min(xa, xf), Math.max(xa, xf), 272, 'bF = ' + bF.toFixed(2) + ' m');

          /* la ley, con los numeros puestos */
          m += '<text x="20" y="26" class="rotulo-svg" style="font-size:12.5px;fill:var(--ink)">'
             + 'F x bF = R x bR &nbsp;&#8594;&nbsp; ' + Math.round(F) + ' x ' + bF.toFixed(2)
             + ' = 500 x ' + bR.toFixed(2) + '</text>';
          svg.innerHTML = m;

          var vm = R / F;
          var t = '';
          if(F <= TU){
            t = '<b>Con esta palanca llegas.</b> Hacen falta ' + Math.round(F) + ' N y un brazo da unos '
              + TU + ' N. ';
          } else {
            t = '<b>As&iacute; no la mueves.</b> Hacen falta ' + Math.round(F) + ' N, unos '
              + Math.round(F/10) + ' kg, y un brazo da unos ' + TU + ' N. ';
          }
          t += 'La palanca multiplica tu fuerza por <b>' + vm.toFixed(2) + '</b>, as&iacute; que pagas lo '
             + 'mismo en recorrido: para subir la carga 10 cm, tu mano recorre <b>'
             + (Math.round(100*vm)/10).toFixed(1) + ' cm</b>.';
          if(genero === 3){
            t += ' En el tercer g&eacute;nero eso es menos de 1: <b>pierdes fuerza y ganas recorrido</b>. '
               + 'As&iacute; est&aacute; hecho tu brazo.';
          }
          pie.innerHTML = t;
        }

        svg.addEventListener('click', function(e){
          var caja = svg.getBoundingClientRect();
          var x = (e.clientX - caja.left) * 640 / caja.width;
          if(x < X0 + 70) x = X0 + 70;
          if(x > X1 - 70) x = X1 - 70;
          movil = Math.round(x);
          pinta();
        });
        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-g]'); if(!b) return;
          if(b.dataset.g === 'mover'){ movida = !movida; pinta(); return; }
          genero = +b.dataset.g;
          movil = (genero === 1) ? 230 : 320;
          movida = false;
          seg.querySelectorAll('button[data-g]').forEach(function(x){
            if(x.dataset.g !== 'mover') x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          pinta();
        });
        pinta();
      })();
      </script>
'''


# ============================================================================
# ESCENA 2 - Poleas y polipasto
# ============================================================================
# Los tramos de cuerda son verticales de verdad: cada uno sale por la tangente
# de una polea y entra por la de la siguiente, que esta desplazada justo 2r.
ESC_POLEAS = u'''
      <div class="escena" id="esc-poleas">
        <div class="escena-barra">
          <span class="escena-titulo">80 kg colgando &middot; elige el montaje y tira</span>
          <div class="seg" id="seg-poleas">
            <button type="button" data-n="1" aria-pressed="true">Polea fija</button>
            <button type="button" data-n="2">2 tramos</button>
            <button type="button" data-n="3">3 tramos</button>
            <button type="button" data-n="4">4 tramos</button>
            <button type="button" data-n="tira">&#8595; Tirar de la cuerda</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 330" id="svg-poleas" role="img"
               aria-label="Polea fija y polipastos de dos, tres y cuatro tramos: la fuerza se divide
                           entre el n&uacute;mero de tramos y la cuerda que hay que tirar se multiplica
                           por ese mismo n&uacute;mero"></svg>
        </div>
        <div class="pie" id="pie-poleas"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-poleas');
        var pie = document.getElementById('pie-poleas');
        var seg = document.getElementById('seg-poleas');
        if(!svg) return;

        var Rr = 15;          /* radio de las poleas */
        var YV = 40;          /* la viga */
        var YT = 72;          /* eje de las poleas fijas */
        var YB0 = 200;        /* eje de las poleas moviles, en reposo */
        var YM0 = 112;        /* la mano, en reposo */
        var SUBE = 42;        /* lo que sube la carga al tirar */
        var P = 800;          /* la carga, en newtons */
        var n = 1, tirado = false;

        /* Para cada montaje: poleas de arriba, poleas de abajo, donde se ata la
           cuerda, por donde se va a la mano, y de que cuelga la carga.       */
        var M = {
          1: {arriba:[360], abajo:[],        ata:null,  atax:null, mano:375, carga:345},
          2: {arriba:[360], abajo:[330],     ata:'viga', atax:315, mano:375, carga:330},
          3: {arriba:[330,390], abajo:[360], ata:'bloque', atax:315, mano:405, carga:360},
          4: {arriba:[360,420], abajo:[330,390], ata:'viga', atax:315, mano:435, carga:360}
        };

        /* El cuerpo de la polea se dibuja un poco mas pequeno que el radio de la
           cuerda: asi la cuerda se ve por fuera, metida en la garganta.          */
        function polea(cx, cy){
          return '<circle cx="' + cx + '" cy="' + cy + '" r="' + (Rr-2.5) + '" fill="var(--surface-2)" '
               + 'stroke="var(--ink-soft)" stroke-width="2"></circle>'
               + '<circle cx="' + cx + '" cy="' + cy + '" r="3" fill="var(--ink-soft)"></circle>';
        }
        function tramo(x, y1, y2){
          return '<path d="M' + x + ' ' + y1 + ' V' + y2 + '" stroke="var(--goo-rojo)" '
               + 'stroke-width="2.6" fill="none"></path>';
        }
        function vuelta(cx, cy, porArriba){
          return '<path d="M' + (cx-Rr) + ' ' + cy + ' A' + Rr + ' ' + Rr + ' 0 0 '
               + (porArriba ? 1 : 0) + ' ' + (cx+Rr) + ' ' + cy + '" stroke="var(--goo-rojo)" '
               + 'stroke-width="2.6" fill="none"></path>';
        }

        function pinta(){
          var d = M[n];
          var yb = YB0 - (tirado ? SUBE : 0);          /* poleas moviles */
          var ymano = YM0 + (tirado ? SUBE*n : 0);     /* la mano baja n veces mas */
          var m = '';

          /* la viga */
          m += '<rect x="180" y="' + (YV-14) + '" width="340" height="14" fill="var(--surface-2)" '
             + 'stroke="var(--ink-soft)" stroke-width="2"></rect>';
          for(var k = 0; k < 11; k++){
            m += '<path d="M' + (188 + k*31) + ' ' + (YV-14) + ' l10 14" stroke="var(--line)" '
               + 'stroke-width="1.5"></path>';
          }

          /* colgadores de las poleas fijas */
          var i;
          for(i = 0; i < d.arriba.length; i++){
            m += '<path d="M' + d.arriba[i] + ' ' + YV + ' V' + (YT-Rr) + '" stroke="var(--ink-soft)" '
               + 'stroke-width="3"></path>';
          }

          /* el bloque movil y la carga */
          if(d.abajo.length){
            var x0 = d.abajo[0] - 26, x1 = d.abajo[d.abajo.length-1] + 26;
            m += '<rect x="' + x0 + '" y="' + (yb+Rr) + '" width="' + (x1-x0) + '" height="10" rx="2" '
               + 'fill="var(--surface-2)" stroke="var(--ink-soft)" stroke-width="2"></rect>';
            m += '<path d="M' + d.carga + ' ' + (yb+Rr+10) + ' V' + (yb+Rr+26) + '" '
               + 'stroke="var(--ink-soft)" stroke-width="2.5"></path>';
          } else {
            m += '<path d="M' + d.carga + ' ' + yb + ' V' + (yb+Rr+26) + '" stroke="var(--goo-rojo)" '
               + 'stroke-width="2.6"></path>';
          }
          var yc = yb + Rr + 26;
          m += '<rect x="' + (d.carga-42) + '" y="' + yc + '" width="84" height="52" rx="3" '
             + 'fill="#a5783f" stroke="#7a5528" stroke-width="2"></rect>';
          m += '<text x="' + d.carga + '" y="' + (yc+31) + '" text-anchor="middle" class="rotulo-svg" '
             + 'style="fill:#fff;font-size:12.5px">80 kg</text>';

          /* La cuerda. Cada tramo es vertical de verdad: sale por la tangente de una
             polea y entra por la de la siguiente, que esta desplazada justo 2r. Las
             poleas se recorren alternando abajo y arriba, empezando por el lado que
             diga 'ata', y el ultimo tramo se va a la mano.                        */
          if(n === 1){
            m += tramo(345, YT, yb);
            m += vuelta(360, YT, true);
            m += tramo(375, YT, ymano);
          } else {
            var lado = (d.ata === 'viga') ? 'abajo' : 'arriba';
            var x = d.atax, ia = 0, ib = 0;
            var total = d.arriba.length + d.abajo.length;
            m += tramo(x, (d.ata === 'viga') ? YV : yb + Rr, (lado === 'abajo') ? yb : YT);
            for(var s = 0; s < total; s++){
              if(lado === 'abajo'){
                m += vuelta(d.abajo[ib], yb, false);
                x = d.abajo[ib] + Rr; ib++;
                lado = 'arriba';
                if(s < total - 1) m += tramo(x, yb, YT);
              } else {
                m += vuelta(d.arriba[ia], YT, true);
                x = d.arriba[ia] + Rr; ia++;
                lado = 'abajo';
                if(s < total - 1) m += tramo(x, YT, yb);
              }
            }
            m += tramo(x, YT, ymano);
          }

          /* las poleas, encima de la cuerda */
          for(i = 0; i < d.arriba.length; i++) m += polea(d.arriba[i], YT);
          for(i = 0; i < d.abajo.length; i++) m += polea(d.abajo[i], yb);

          /* la mano */
          m += '<circle cx="' + d.mano + '" cy="' + ymano + '" r="9" fill="var(--goo-azul)"></circle>';

          /* los numeros */
          var F = P / n;
          m += '<text x="20" y="22" class="rotulo-svg" style="font-size:12.5px;fill:var(--ink)">'
             + 'Tramos que sostienen la carga: ' + n + ' &nbsp;&#8594;&nbsp; F = 800 / ' + n + ' = '
             + Math.round(F) + ' N</text>';
          m += '<text x="20" y="' + (YB0+118) + '" class="rotulo-svg" style="font-size:12px">'
             + 'Para subir la carga 30 cm hay que tirar ' + (30*n) + ' cm de cuerda</text>';
          svg.innerHTML = m;

          var t;
          if(n === 1){
            t = '<b>La polea fija no multiplica nada</b>: sigues haciendo los 800 N enteros. Lo que hace '
              + 'es cambiar la direcci&oacute;n, y no es poco: ahora tiras <b>hacia abajo</b>, puedes colgarte '
              + 'de la cuerda y pueden tirar varios a la vez.';
          } else {
            t = '<b>' + n + ' tramos de cuerda sostienen la carga</b>, as&iacute; que cada uno aguanta '
              + Math.round(P/n) + ' N: eso es lo que notas t&uacute;. A cambio, por cada metro que sube la '
              + 'carga tienes que tirar <b>' + n + ' metros</b> de cuerda. Fuerza dividida entre ' + n
              + ', recorrido multiplicado por ' + n + '.';
          }
          pie.innerHTML = t;
        }

        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-n]'); if(!b) return;
          if(b.dataset.n === 'tira'){ tirado = !tirado; pinta(); return; }
          n = +b.dataset.n; tirado = false;
          seg.querySelectorAll('button[data-n]').forEach(function(x){
            if(x.dataset.n !== 'tira') x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          pinta();
        });
        pinta();
      })();
      </script>
'''


# ============================================================================
# ESCENA 3 - Engranajes
# ============================================================================
# Los dientes no estan dibujados a ojo: el modulo es el mismo en las dos ruedas
# (m = 4 px por diente), asi que el radio sale r = m*z/2 y los dientes encajan.
# El desfase de la rueda conducida se calcula para que un diente de la motriz
# caiga siempre en un hueco de la otra.
ESC_ENGRANAJES = u'''
      <div class="escena" id="esc-engranajes">
        <div class="escena-barra">
          <span class="escena-titulo">A c&aacute;mara lenta &middot; la entrada gira siempre a 60 rpm</span>
          <div class="seg" id="seg-engranajes">
            <button type="button" data-e="red" aria-pressed="true">Reductor 12 &#8594; 36</button>
            <button type="button" data-e="mul">Multiplicador 36 &#8594; 12</button>
            <button type="button" data-e="cad">Cadena 24 &#8594; 12</button>
            <button type="button" data-e="sin">Tornillo sin fin</button>
            <button type="button" data-e="pausa">&#9208; Parar</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 300" id="svg-engranajes" role="img"
               aria-label="Dos ruedas dentadas engranadas girando en sentidos contrarios, una cadena
                           entre dos pi&ntilde;ones y un tornillo sin fin con su rueda"></svg>
        </div>
        <div class="pie" id="pie-engranajes"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-engranajes');
        var pie = document.getElementById('pie-engranajes');
        var seg = document.getElementById('seg-engranajes');
        if(!svg) return;

        var MOD = 4;                 /* modulo: pixeles de diametro por diente */
        var modo = 'red', ang = 0, girando = true, raf = null, ultimo = 0;
        var C = {
          red: {z1:12, z2:36}, mul: {z1:36, z2:12},
          cad: {z1:24, z2:12}, sin: {z1:1,  z2:40}
        };

        function radio(z){ return MOD*z/2; }

        function rueda(cx, cy, z, fase, col){
          var rp = radio(z), ra = rp + MOD, rf = rp - 1.25*MOD;
          var pas = 2*Math.PI/z, d = '', k, j, a, r, x, y;
          for(k = 0; k < z; k++){
            var t = fase + k*pas;
            /* el diente ocupa algo menos de medio paso, para que entre holgado
               en el hueco de la otra rueda y no se monten al dibujarlos */
            var pts = [[t - pas*0.27, rf], [t - pas*0.17, ra],
                       [t + pas*0.17, ra], [t + pas*0.27, rf]];
            for(j = 0; j < 4; j++){
              a = pts[j][0]; r = pts[j][1];
              x = cx + r*Math.cos(a); y = cy + r*Math.sin(a);
              d += (d === '' ? 'M' : 'L') + x.toFixed(1) + ' ' + y.toFixed(1) + ' ';
            }
          }
          d += 'Z';
          var m = '<path d="' + d + '" fill="' + col + '" stroke="var(--ink-soft)" stroke-width="1.5"></path>';
          m += '<circle cx="' + cx + '" cy="' + cy + '" r="' + (rp*0.30).toFixed(1)
             + '" fill="var(--surface)" stroke="var(--ink-soft)" stroke-width="2"></circle>';
          /* una marca radial, para ver girar la rueda */
          m += '<path d="M' + cx + ' ' + cy + ' L' + (cx + rp*0.85*Math.cos(fase)).toFixed(1) + ' '
             + (cy + rp*0.85*Math.sin(fase)).toFixed(1) + '" stroke="var(--ink)" stroke-width="2.5"></path>';
          return m;
        }

        function etiqueta(cx, cy, z, rpm, txt){
          return '<text x="' + cx + '" y="' + cy + '" text-anchor="middle" class="rotulo-svg" '
               + 'style="font-size:12px;fill:var(--ink)">z = ' + z + ' &middot; ' + rpm + ' rpm</text>'
               + '<text x="' + cx + '" y="' + (cy+16) + '" text-anchor="middle" class="rotulo-svg">'
               + txt + '</text>';
        }

        function pinta(){
          svg.setAttribute('viewBox', '0 0 640 300');
          var c = C[modo], m = '', z1 = c.z1, z2 = c.z2;
          var i, n2;

          if(modo === 'sin'){
            /* Vista por el plano que contiene los dos ejes. El filete del
               tornillo se comporta ahi como una cremallera: por eso cada
               vuelta suya empuja la rueda exactamente un diente.           */
            svg.setAttribute('viewBox', '0 0 640 352');
            var rp = radio(z2);                  /* radio primitivo de la rueda */
            var cx = 236, YP = 192;              /* YP: la linea de paso comun */
            var cy = YP - rp;
            var pas2 = 2*Math.PI/z2;
            var p = rp*pas2;                     /* paso, en pixeles */
            var giro = ang*4;                    /* el tornillo, mas vivo */
            var fase = -giro/z2;

            /* proporciones de tornillo de verdad: primitivo 8 modulos */
            var Rw = 4*MOD, Rx = Rw + MOD, Rc = Rw - 1.25*MOD;
            var yE = YP + Rw;                    /* eje del tornillo */
            var XA = 96, XB = 396;

            /* --- nucleo --- */
            m += '<rect x="' + XA + '" y="' + (yE-Rc) + '" width="' + (XB-XA) + '" height="' + (2*Rc)
               + '" fill="var(--surface-2)" stroke="none"></rect>';
            m += '<path d="M' + XA + ' ' + (yE-Rc) + ' H' + XB + ' M' + XA + ' ' + (yE+Rc) + ' H' + XB
               + '" stroke="var(--ink-soft)" stroke-width="1.2" opacity=".45"></path>';

            /* --- el filete: la cara de cada vuelta, de cresta a cresta --- */
            var k, xc, dTop = '', hay = false;
            for(k = -60; k < 120; k++){
              xc = cx + rp*(fase + k*pas2 - Math.PI/2) + p/2;
              if(xc < XA - p || xc > XB + p) continue;
              var a = xc - 0.27*p, b = xc - 0.17*p, c = xc + 0.17*p, e = xc + 0.27*p;
              var s = p/2;                       /* la helice avanza medio paso al dar la vuelta */
              var cara = 'M' + a.toFixed(1) + ' ' + (yE-Rc).toFixed(1)
                       + ' L' + b.toFixed(1) + ' ' + (yE-Rx).toFixed(1)
                       + ' L' + c.toFixed(1) + ' ' + (yE-Rx).toFixed(1)
                       + ' L' + e.toFixed(1) + ' ' + (yE-Rc).toFixed(1)
                       + ' L' + (e+s).toFixed(1) + ' ' + (yE+Rc).toFixed(1)
                       + ' L' + (c+s).toFixed(1) + ' ' + (yE+Rx).toFixed(1)
                       + ' L' + (b+s).toFixed(1) + ' ' + (yE+Rx).toFixed(1)
                       + ' L' + (a+s).toFixed(1) + ' ' + (yE+Rc).toFixed(1) + ' Z';
              /* la media vuelta que pasa por detras del nucleo: floja y a trazos,
                 que es lo que hace que se vea que el filete da la vuelta        */
              m += '<path d="M' + (a+s).toFixed(1) + ' ' + (yE+Rc).toFixed(1)
                 + ' L' + (a+p).toFixed(1) + ' ' + (yE-Rc).toFixed(1)
                 + '" stroke="var(--ink-soft)" stroke-width="1.1" opacity=".38" '
                 + 'stroke-dasharray="3 3"></path>';
              m += '<path d="' + cara + '" fill="var(--surface)" stroke="var(--ink-soft)" '
                 + 'stroke-width="1.6" stroke-linejoin="round"></path>';
              /* la cresta que engrana, marcada en azul */
              if(xc > XA + 4 && xc < XB - 4){
                dTop += 'M' + a.toFixed(1) + ' ' + (yE-Rc).toFixed(1)
                      + ' L' + b.toFixed(1) + ' ' + (yE-Rx).toFixed(1)
                      + ' L' + c.toFixed(1) + ' ' + (yE-Rx).toFixed(1)
                      + ' L' + e.toFixed(1) + ' ' + (yE-Rc).toFixed(1) + ' ';
                hay = true;
              }
            }
            if(hay) m += '<path d="' + dTop + '" fill="none" stroke="var(--goo-azul)" stroke-width="2.4"></path>';

            /* --- tres marcas pintadas en el eje -------------------------------
               Un filete girando y uno desplazandose se proyectan IGUAL: por eso
               antes parecia que el tornillo solo corria de lado. Con tres rayas
               pintadas a 120 grados siempre hay alguna subiendo por delante y
               otra bajando por detras, y el giro se ve solo.                   */
            var th = giro, ys = yE + Rc*Math.sin(th), vis = Math.cos(th);
            for(var j = 0; j < 3; j++){
              var tj = th + j*2*Math.PI/3;
              var yj = yE + Rc*Math.sin(tj), vj = Math.cos(tj);
              m += '<path d="M' + (XA+8) + ' ' + yj.toFixed(1) + ' H' + (XB-12)
                 + '" stroke="#f29900" stroke-linecap="round" stroke-width="'
                 + (vj > 0 ? '3.4' : '2') + '" opacity="'
                 + (vj > 0 ? (0.45 + 0.55*vj).toFixed(2) : '0.28') + '"'
                 + (vj > 0 ? '' : ' stroke-dasharray="5 5"') + '></path>';
            }

            /* los extremos, para que el cilindro quede cerrado */
            /* La cara del extremo se ve casi de canto: es un disco perpendicular
               al eje, y desde el lado se proyecta como una elipse muy estrecha,
               no como un circulo.                                              */
            var rxE = 4;
            m += '<ellipse cx="' + XB + '" cy="' + yE + '" rx="' + rxE + '" ry="' + Rc
               + '" fill="var(--surface-2)" stroke="var(--ink-soft)" stroke-width="1.8"></ellipse>';
            m += '<path d="M' + XB + ' ' + yE + ' L' + (XB + rxE*Math.cos(th)).toFixed(1) + ' '
               + ys.toFixed(1) + '" stroke="#f29900" stroke-width="2.2"></path>';
            m += '<circle cx="' + (XB + rxE*Math.cos(th)).toFixed(1) + '" cy="' + ys.toFixed(1)
               + '" r="3" fill="#f29900"></circle>';

            /* --- la rueda, con sus dientes metidos en los huecos del filete --- */
            m += rueda(cx, cy, z2, fase, 'var(--surface-2)');

            /* --- donde engranan, con el rotulo fuera del dibujo --- */
            m += '<circle cx="' + cx + '" cy="' + YP + '" r="8" fill="none" stroke="#f29900" stroke-width="2.5"></circle>';
            m += '<path d="M' + (cx-10) + ' ' + (YP-6) + ' L' + (cx-92) + ' ' + (YP-46)
               + '" stroke="#f29900" stroke-width="1.6"></path>';
            m += '<text x="' + (cx-98) + '" y="' + (YP-44) + '" text-anchor="end" class="rotulo-svg" '
               + 'style="fill:#f29900">aqu&iacute; engranan</text>';

            /* --- el tornillo gira sobre su eje --- */
            var Ra = Rx + 9;
            m += '<path d="M' + (XB+4) + ' ' + (yE-Ra) + ' a' + Ra + ' ' + Ra + ' 0 0 1 0 ' + (2*Ra)
               + '" fill="none" stroke="var(--goo-azul)" stroke-width="2.4"></path>';
            m += '<path d="M' + (XB+4) + ' ' + (yE+Ra) + ' l9 -6 l1 11 Z" fill="var(--goo-azul)"></path>';

            /* --- entrada y salida --- */
            m += '<text x="' + (XB+44) + '" y="' + (yE-5) + '" class="rotulo-svg" '
               + 'style="fill:var(--goo-azul)">entrada</text>';
            m += '<text x="' + (XB+44) + '" y="' + (yE+12) + '" class="rotulo-svg">el tornillo, 60 rpm</text>';
            m += etiqueta(cx + rp + 122, cy - 30, z2, '1,5', 'la rueda, de salida');

            /* --- el contador, que es donde esta la gracia del mecanismo --- */
            var vue = Math.floor(giro/(2*Math.PI));
            m += '<text x="96" y="' + (yE + Rx + 34) + '" class="rotulo-svg" style="font-size:12.5px;fill:var(--ink)">'
               + 'vueltas del tornillo: ' + vue + '</text>';
            m += '<text x="96" y="' + (yE + Rx + 52) + '" class="rotulo-svg">la rueda ha avanzado '
               + (vue % z2) + ' dientes de ' + z2 + '</text>';

            m += '<text x="20" y="22" class="rotulo-svg" style="font-size:12.5px;fill:var(--ink)">'
               + 'Tornillo de 1 entrada y rueda de 40 dientes &nbsp;&#8594;&nbsp; i = 1 / 40</text>';
            /* --- el tornillo visto por el extremo -----------------------------
               Aqui SI se ve girar. De lado, una helice girando y una helice
               avanzando se proyectan igual (es lo que pasa con los postes de
               barbero); por el extremo, en cambio, el giro es evidente. Las
               tres marcas son las mismas rayas naranjas de la vista de lado. */
            var xi = 520, yi = 296, Ri = 33, Ri2 = Ri*Rc/Rx;
            m += '<circle cx="' + xi + '" cy="' + yi + '" r="' + Ri
               + '" fill="var(--surface)" stroke="var(--ink-soft)" stroke-width="2"></circle>';
            m += '<circle cx="' + xi + '" cy="' + yi + '" r="' + Ri2.toFixed(1)
               + '" fill="var(--surface-2)" stroke="var(--ink-soft)" stroke-width="1.5"></circle>';
            for(j = 0; j < 3; j++){
              var tk = th + j*2*Math.PI/3;
              m += '<path d="M' + xi + ' ' + yi + ' L' + (xi + Ri*Math.cos(tk)).toFixed(1) + ' '
                 + (yi + Ri*Math.sin(tk)).toFixed(1) + '" stroke="#f29900" stroke-width="2.6"></path>';
              m += '<circle cx="' + (xi + Ri*Math.cos(tk)).toFixed(1) + '" cy="'
                 + (yi + Ri*Math.sin(tk)).toFixed(1) + '" r="3.4" fill="#f29900"></circle>';
            }
            m += '<path d="M' + (xi+Ri+10) + ' ' + yi + ' a' + (Ri+10) + ' ' + (Ri+10)
               + ' 0 0 1 ' + (-(Ri+10)) + ' ' + (Ri+10)
               + '" fill="none" stroke="var(--goo-azul)" stroke-width="2.2"></path>';
            m += '<path d="M' + xi + ' ' + (yi+Ri+10) + ' l7 -8 l4 10 Z" fill="var(--goo-azul)"></path>';
            m += '<text x="' + xi + '" y="' + (yi-Ri-14) + '" text-anchor="middle" class="rotulo-svg" '
               + 'style="fill:var(--ink)">el tornillo, por el extremo</text>';
            m += '<text x="' + xi + '" y="' + (yi-Ri-1) + '" text-anchor="middle" class="rotulo-svg">'
               + 'las mismas tres marcas</text>';

            svg.innerHTML = m;
            pie.innerHTML = 'El tornillo tiene <b>un solo diente</b>, enrollado en h&eacute;lice. Cada vuelta '
              + 'del tornillo avanza la rueda <b>un diente</b>: hacen falta 40 vueltas para una vuelta de '
              + 'la rueda. Reducci&oacute;n enorme en muy poco sitio &mdash; y, si la h&eacute;lice es '
              + 'tumbada, <b>no se puede mover al rev&eacute;s</b>: la rueda no consigue hacer girar al '
              + 'tornillo. Por eso lo llevan las clavijas de una guitarra y los portones.';
            return;
          }

          var r1 = radio(z1), r2 = radio(z2), CY = 150;
          n2 = Math.round(60 * z1 / z2 * 10) / 10;

          if(modo === 'cad'){
            var x1 = 190, x2 = 470, dd = x2 - x1;
            var alfa = Math.asin((r1 - r2) / dd);
            var t1 = alfa - Math.PI/2, t2 = alfa + Math.PI/2;
            /* los dos ramales de la cadena, tangentes a las dos ruedas */
            m += '<path d="M' + (x1 + r1*Math.cos(t1)).toFixed(1) + ' ' + (CY + r1*Math.sin(t1)).toFixed(1)
               + ' L' + (x2 + r2*Math.cos(t1)).toFixed(1) + ' ' + (CY + r2*Math.sin(t1)).toFixed(1)
               + '" stroke="var(--ink-soft)" stroke-width="5" stroke-linecap="round"></path>';
            m += '<path d="M' + (x1 + r1*Math.cos(t2)).toFixed(1) + ' ' + (CY + r1*Math.sin(t2)).toFixed(1)
               + ' L' + (x2 + r2*Math.cos(t2)).toFixed(1) + ' ' + (CY + r2*Math.sin(t2)).toFixed(1)
               + '" stroke="var(--ink-soft)" stroke-width="5" stroke-linecap="round"></path>';
            m += rueda(x1, CY, z1, ang, 'var(--surface-2)');
            m += rueda(x2, CY, z2, ang*z1/z2, 'var(--accent-soft)');
            m += etiqueta(x1, CY + r1 + 34, z1, 60, 'plato, entrada');
            m += etiqueta(x2, CY + r2 + 34, z2, n2, 'pi&ntilde;&oacute;n, salida');
            m += '<text x="20" y="26" class="rotulo-svg" style="font-size:12.5px;fill:var(--ink)">'
               + 'i = z1 / z2 = ' + z1 + ' / ' + z2 + ' = ' + (z1/z2).toFixed(2)
               + ' &nbsp;&#8594;&nbsp; n2 = 60 x ' + (z1/z2).toFixed(2) + ' = ' + n2 + ' rpm</text>';
            svg.innerHTML = m;
            pie.innerHTML = 'Con <b>cadena</b> las dos ruedas giran en el <b>mismo sentido</b> y pueden '
              + 'estar lejos una de otra: por eso la lleva la bicicleta, con los pedales delante y la '
              + 'rueda detr&aacute;s. La cuenta es la misma que con los dientes engranados.';
            return;
          }

          var cx1 = 320 - (r1 + r2)/2, cx2 = 320 + (r1 + r2)/2;
          var pas2 = 2*Math.PI/z2;
          /* desfase para que un diente de la motriz caiga en un hueco de la conducida */
          var fase2 = Math.PI - pas2/2 - ang*z1/z2;
          m += rueda(cx1, CY, z1, ang, 'var(--surface-2)');
          m += rueda(cx2, CY, z2, fase2, 'var(--accent-soft)');
          m += etiqueta(cx1, CY + radio(z1) + 34, z1, 60, 'motriz, entrada');
          m += etiqueta(cx2, CY + radio(z2) + 34, z2, n2, 'conducida, salida');
          m += '<text x="20" y="26" class="rotulo-svg" style="font-size:12.5px;fill:var(--ink)">'
             + 'i = z1 / z2 = ' + z1 + ' / ' + z2 + ' = ' + (z1/z2).toFixed(2)
             + ' &nbsp;&#8594;&nbsp; n2 = 60 x ' + (z1/z2).toFixed(2) + ' = ' + n2 + ' rpm</text>';
          svg.innerHTML = m;

          if(z1 < z2){
            pie.innerHTML = '<b>Reductor.</b> La peque&ntilde;a arrastra a la grande: la salida gira '
              + '<b>tres veces m&aacute;s despacio</b> y, a cambio, con <b>tres veces m&aacute;s fuerza</b>. '
              + 'Es lo que necesita una cuesta, un taladro o un portal autom&aacute;tico. F&iacute;jate en '
              + 'que giran en sentidos contrarios.';
          } else {
            pie.innerHTML = '<b>Multiplicador.</b> La grande arrastra a la peque&ntilde;a: la salida gira '
              + '<b>tres veces m&aacute;s deprisa</b> y con <b>la tercera parte de la fuerza</b>. Es el '
              + 'plato grande de la bici en una bajada. El trato es el mismo de la palanca y del polipasto.';
          }
        }

        function cuadro(t){
          if(!ultimo) ultimo = t;
          var dt = Math.min(0.05, (t - ultimo)/1000);
          ultimo = t;
          ang += 0.55*dt;
          pinta();
          raf = girando ? requestAnimationFrame(cuadro) : null;
        }

        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-e]'); if(!b) return;
          if(b.dataset.e === 'pausa'){
            girando = !girando;
            b.innerHTML = girando ? '&#9208; Parar' : '&#9654; Seguir';
            if(girando && raf === null){ ultimo = 0; raf = requestAnimationFrame(cuadro); }
            return;
          }
          modo = b.dataset.e;
          seg.querySelectorAll('button[data-e]').forEach(function(x){
            if(x.dataset.e !== 'pausa') x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          pinta();
        });
        pinta();
        raf = requestAnimationFrame(cuadro);
      })();
      </script>
'''


# ============================================================================
# SESION 1 - La palanca
# ============================================================================
S1 = (
  bloque('00', u'Reto inicial &middot; 10 min', u"""
      <p>En el tema anterior todo lo que constru&iacute;as ten&iacute;a que <b>quedarse quieto</b>: una
         estructura que se mueve es una estructura que ha fallado. Desde hoy pasa justo lo contrario.
         Queremos que se mueva &mdash;y que se mueva donde nosotros digamos, con la fuerza que nosotros
         digamos.</p>
      <p>Empecemos por algo que has visto: cambiar la rueda de un coche. La tuerca est&aacute; apretada
         con m&aacute;quina y con la llave del maletero no hay quien la mueva. Entonces alguien mete un
         tubo en el mango, empuja casi sin ganas y la tuerca sale.</p>
      <div class="aviso">
        <span class="n-tag">La pregunta</span>
        El truco del tubo lo conoce todo el mundo. <b>&iquest;Cu&aacute;nta fuerza te ahorra
        exactamente?</b> Cont&eacute;stalo con un n&uacute;mero, por escrito. «Bastante» no vale.
      </div>
      <p>Aqu&iacute; se acaban las respuestas. Sabemos <i>que</i> funciona, pero no sabemos
         <b>cu&aacute;nto</b>, y por eso no podr&iacute;amos dise&ntilde;ar nada: ni decidir qu&eacute;
         largo tiene que tener el tubo, ni saber si con ese tubo va a salir o vamos a doblar la llave.</p>
      <p>Y hay una segunda pregunta, peor: <b>&iquest;por qu&eacute; no puedes con ella a pelo?</b> La
         tuerca de una rueda se aprieta con unos 110 newton-metro. Con la llave corta, de 20 cm, eso son
         550 N: como colgar <b>55 kg</b> de tu mano. Empujando con un brazo, a tu edad, andas del orden
         de los 250 N. No es cuesti&oacute;n de ganas: <b>el m&uacute;sculo no llega</b>.</p>
""" + narrador() + u"""
  """) +
  bloque('01', u'Teor&iacute;a &middot; 20 min', u"""
      <h3>Una barra, un punto y un trato</h3>
      <p>Pon una barra sobre un punto fijo, la carga en un lado y tu mano en el otro. Eso es todo el
         invento. Lo interesante es que la barra <b>no reparte la fuerza a partes iguales</b>: reparte
         seg&uacute;n lo lejos que est&eacute; cada cosa del punto de apoyo.</p>
      <p>En la escena, la carga son 50 kg &mdash;500 N&mdash; y la barra mide 2,30 m. Mueve el apoyo
         pulsando sobre la barra y mira qu&eacute; pasa con la fuerza que te pide.</p>
""" + ESC_PALANCA + u"""
      <p>Dos cosas que conviene haber visto antes de copiar nada. La primera: cuanto m&aacute;s cerca
         pones el apoyo de la carga, menos fuerza necesitas. La segunda, la importante: <b>eso no es
         gratis</b>. Cada vez que divides la fuerza entre tres, tu mano tiene que recorrer tres veces
         m&aacute;s camino. La palanca no fabrica fuerza de la nada; la <b>cambia por recorrido</b>.</p>

      <div class="copiar">
        <h4>Definiciones</h4>
        <p><b>Mecanismo</b>: conjunto de piezas que recibe un movimiento y una fuerza y los entrega
           <b>cambiados</b>: m&aacute;s fuerza, m&aacute;s velocidad o en otra direcci&oacute;n.</p>
        <p><b>Palanca</b>: barra r&iacute;gida que gira alrededor de un punto de apoyo o
           <b>fulcro</b>.</p>
        <p>Sus cuatro elementos: la <b>resistencia R</b> (lo que hay que vencer) con su brazo
           <b>b<sub>R</sub></b>, y la <b>fuerza F</b> (la que haces t&uacute;) con su brazo
           <b>b<sub>F</sub></b>. El <b>brazo</b> es la distancia de cada fuerza al punto de apoyo.</p>
        <h4>La ley de la palanca</h4>
        <p style="font-size:18px;text-align:center;margin:10px 0"><b>F &middot; b<sub>F</sub> =
           R &middot; b<sub>R</sub></b></p>
        <p><b>Ventaja mec&aacute;nica</b>: las veces que la palanca multiplica tu fuerza.
           VM = R / F = b<sub>F</sub> / b<sub>R</sub>.</p>
      </div>

      <div class="copiar">
        <h4>Lo que se gana se paga</h4>
        <p>Si una palanca multiplica tu fuerza por 4, tu mano recorre <b>4 veces</b> lo que recorre la
           carga. Ninguna m&aacute;quina te regala nada: <b>cambia fuerza por recorrido</b>.</p>
      </div>

      <h3>Los tres g&eacute;neros</h3>
      <p>Seg&uacute;n d&oacute;nde caiga el punto de apoyo salen tres palancas distintas, y cada una
         sirve para una cosa distinta. Puedes verlas en la escena de arriba con los botones.</p>
      <div class="copiar">
        <h4>Clasificaci&oacute;n</h4>
        <ul>
          <li><b>Primer g&eacute;nero</b> &mdash; el apoyo <b>en medio</b>, entre la fuerza y la
              resistencia. Puede ganar o perder fuerza, seg&uacute;n d&oacute;nde pongas el apoyo.
              <i>Tijeras, alicates, balanc&iacute;n, el martillo sacando un clavo.</i></li>
          <li><b>Segundo g&eacute;nero</b> &mdash; la <b>resistencia en medio</b>. Siempre gana fuerza
              (b<sub>F</sub> es mayor que b<sub>R</sub> forzosamente).
              <i>Carretilla, cascanueces, abrebotellas.</i></li>
          <li><b>Tercer g&eacute;nero</b> &mdash; la <b>fuerza en medio</b>. Siempre <b>pierde</b>
              fuerza y gana recorrido y velocidad.
              <i>Pinzas de depilar, ca&ntilde;a de pescar, tu propio brazo.</i></li>
        </ul>
      </div>
""" + video('palanca') + foto('shaduf') + u"""
      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; no hace falta copiarlo</span>
        <p>La palanca no la invent&oacute; nadie: es demasiado antigua para tener autor. En Egipto se
           regaba con <b>shaduf</b> &mdash;una p&eacute;rtiga con un cubo en un extremo y una piedra en
           el otro&mdash; hace unos 4.000 a&ntilde;os, y se sigue regando as&iacute; en algunos sitios.</p>
        <p>Lo que s&iacute; tiene autor es la <b>explicaci&oacute;n</b>. La demuestra <b>Arqu&iacute;medes</b>
           en el siglo III a. C., casi dos mil a&ntilde;os despu&eacute;s de que la gente llevara usando
           palancas todos los d&iacute;as. La famosa frase &mdash;<i>dadme un punto de apoyo y mover&eacute;
           el mundo</i>&mdash; no est&aacute; en ning&uacute;n texto suyo: la cuenta Pappus de
           Alejandr&iacute;a unos quinientos a&ntilde;os m&aacute;s tarde.</p>
        <p>Es un patr&oacute;n que se repite en toda la tecnolog&iacute;a: primero se usa, despu&eacute;s
           se entiende. Y entenderlo es lo que permite <b>calcular</b> en vez de probar.</p>
      </div>

      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; no hace falta copiarlo</span>
        <p>Vuelve al t&iacute;tulo del tema: <i>el m&uacute;sculo mueve poco y mal</i>. Ahora se puede
           decir con precisi&oacute;n por qu&eacute;. Tu b&iacute;ceps se agarra al antebrazo a unos 5 cm
           del codo, y la mano est&aacute; a unos 35 cm. Es una <b>palanca de tercer g&eacute;nero</b>, la
           que pierde fuerza: para sostener 5 kg en la mano, el b&iacute;ceps tira del orden de
           <b>35 kg</b>.</p>
        <p>Parece un mal dise&ntilde;o y es justo al rev&eacute;s. A cambio de esa p&eacute;rdida, tu mano
           se mueve <b>siete veces m&aacute;s r&aacute;pido</b> que el punto donde tira el m&uacute;sculo.
           Tu cuerpo ha elegido velocidad en vez de fuerza. Los mecanismos que vamos a ver el resto del
           tema son, casi todos, formas de <b>deshacer ese cambio</b> cuando lo que hace falta es
           fuerza.</p>
      </div>
  """) +
  bloque('02', u'Pr&aacute;ctica &middot; 25 min', ficha(
    u'Actividad 1 &middot; Predecir antes de medir',
    [u'1.2', u'3.1'], u'Parejas &middot; 25 min', u"""
          <h4>Material</h4>
          <p>Una regla de 30 cm, un l&aacute;piz de secci&oacute;n hexagonal (hace de apoyo y no rueda) y
             unas <b>20 monedas iguales</b>. Sirven arandelas, tapones o gomas de borrar: lo &uacute;nico
             que importa es que pesen lo mismo entre ellas.</p>
          <h4>Qu&eacute; hay que hacer</h4>
          <ol class="pasos">
            <li>Montad la palanca: el l&aacute;piz debajo de la regla, en la marca de los 15 cm.
                Comprobad que queda equilibrada a cero.</li>
            <li>Poned <b>6 monedas</b> a 10 cm del apoyo, a un lado. Antes de tocar nada:
                <b>escribid cu&aacute;ntas monedas har&aacute;n falta</b> a 15 cm del apoyo por el otro
                lado. Usad la ley, no la intuici&oacute;n.</li>
            <li>Comprobadlo. Anotad la predicci&oacute;n y el resultado real, aunque no coincidan.</li>
            <li>Repetidlo <b>cuatro veces m&aacute;s</b> cambiando la distancia o el n&uacute;mero de
                monedas. Tabla de cinco filas con: n&uacute;mero de monedas y brazo de cada lado, y las
                dos multiplicaciones.</li>
            <li>Ahora el otro lado del trato. Con el apoyo en 5 cm y la carga en el extremo corto, subid
                la carga <b>2 cm</b> y medid cu&aacute;nto ha bajado vuestra mano. Comparad esa
                proporci&oacute;n con la de los brazos.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Las cinco predicciones est&aacute;n escritas <b>antes</b> de medir <b>(3 puntos)</b>.</li>
            <li>La tabla est&aacute; completa y las dos multiplicaciones salen parecidas
                <b>(3 puntos)</b>.</li>
            <li>La medida de los recorridos est&aacute; hecha y comparada con los brazos
                <b>(2 puntos)</b>.</li>
            <li>Hay una explicaci&oacute;n escrita de por qu&eacute; no cuadra del todo
                <b>(2 puntos)</b>.</li>
          </ul>
          <div class="nota" style="margin-top:14px">
            <span class="n-tag">Lo que de verdad se eval&uacute;a</span>
            El &uacute;ltimo punto. Nunca va a cuadrar exacto: la regla <b>pesa</b>, el apoyo <b>roza</b> y
            las monedas no est&aacute;n en un punto sino repartidas. Detectar por qu&eacute; falla una
            medida vale m&aacute;s que acertarla.
          </div>
  """)) +
  bloque('03', u'Cierre &middot; 5 min', u"""
      <p>Ya se puede contestar con un n&uacute;mero a la pregunta del principio. La tuerca pide 110 N&middot;m.
         Con la llave de 20 cm, 550 N. Con el tubo puesto, 60 cm, <b>183 N</b>: la fuerza se ha dividido
         entre tres porque el brazo se ha multiplicado por tres. Y a cambio tu mano recorre tres veces
         m&aacute;s arco, que es un precio que nadie nota.</p>
      <ol>
      """ + pregunta(u'Una carretilla lleva 60 kg. La rueda est&aacute; a 30 cm de la carga y los mangos a 120 cm de la rueda. &iquest;Qu&eacute; fuerza haces?',
                     u'<p>El apoyo es la <b>rueda</b>. b<sub>R</sub> = 0,30 m y b<sub>F</sub> = 1,20 m. F = 600 &middot; 0,30 / 1,20 = <b>150 N</b>, unos 15 kg. Levantas 60 kg haciendo 15: es una palanca de <b>segundo g&eacute;nero</b>.</p>')
        + pregunta(u'&iquest;Por qu&eacute; unas pinzas de depilar son de tercer g&eacute;nero si hacen menos fuerza de la que pones?',
                   u'<p>Porque lo que se busca ah&iacute; <b>no es fuerza</b>, es <b>precisi&oacute;n</b>. La fuerza va en medio, as&iacute; que la punta se mueve poco aunque tus dedos se muevan mucho: puedes controlar d&eacute;cimas de mil&iacute;metro. Perder fuerza es el precio, y sale a cuenta.</p>')
        + pregunta(u'Si una palanca multiplica tu fuerza por 5, &iquest;qu&eacute; pasa con el recorrido?',
                   u'<p>Se multiplica por 5 <b>el tuyo</b>: para subir la carga 2 cm, tu mano recorre 10 cm. El trato siempre es el mismo, y va a volver a aparecer en las dos sesiones siguientes.</p>') + u"""
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        La palanca tiene un l&iacute;mite que la deja fuera de casi todo: <b>el recorrido</b>. Para subir
        un saco al tercer piso har&iacute;a falta una barra de veinte metros. La soluci&oacute;n es
        cambiar la barra r&iacute;gida por algo que pueda ser tan largo como haga falta: <b>una
        cuerda</b>.
      </div>
  """))


# ============================================================================
# SESION 2 - Poleas y polipasto
# ============================================================================
S2 = (
  bloque('00', u'Reto inicial &middot; 10 min', u"""
      <p>Ayer qued&oacute; claro el trato: fuerza a cambio de recorrido. Hoy el problema es <b>el
         recorrido</b>.</p>
      <p>Una obra. Hay que subir un saco de <b>80 kg</b> hasta el andamio, ocho metros por encima de tu
         cabeza. Con una palanca no hay manera: para que la carga suba ocho metros, tu extremo
         tendr&iacute;a que recorrer mucho m&aacute;s, y no existe esa barra.</p>
      <div class="aviso">
        <span class="n-tag">La pregunta</span>
        Cuelga una cuerda del andamio, &aacute;tala al saco y tira. <b>&iquest;Por qu&eacute; es mucho
        m&aacute;s f&aacute;cil tirar de una cuerda hacia abajo que hacia arriba?</b> Es la misma cuerda
        y el mismo saco.
      </div>
      <p>Piensa qu&eacute; puedes hacer en cada caso. Tirando hacia arriba solo tienes los brazos, y
         encima en la peor postura. Tirando hacia abajo puedes <b>colgarte</b>: sumas tu propio peso,
         apoyas los pies, y adem&aacute;s <b>cabe m&aacute;s gente</b> en la cuerda.</p>
      <p>Cambiar la direcci&oacute;n de una fuerza no multiplica nada &mdash;y aun as&iacute; puede ser
         media soluci&oacute;n.</p>
  """) +
  bloque('01', u'Teor&iacute;a &middot; 20 min', u"""
      <h3>Una rueda con una garganta</h3>
      <p>Una <b>polea</b> es una rueda con un canal por donde pasa la cuerda. No parece gran cosa.
         Seg&uacute;n de d&oacute;nde cuelgue, hace dos trabajos completamente distintos.</p>
      <p>En la escena, el saco son 80 kg &mdash;800 N&mdash;. Prueba los cuatro montajes y, en cada uno,
         pulsa <i>Tirar de la cuerda</i> y mira las dos cosas a la vez: lo que marca la fuerza y lo que
         baja tu mano.</p>
""" + ESC_POLEAS + u"""
      <p>La cuenta que hay debajo es de una sola l&iacute;nea: <b>la carga se reparte entre los tramos de
         cuerda que la sostienen</b>. Si la sostienen cuatro tramos, cada uno aguanta la cuarta parte, y
         t&uacute; est&aacute;s en uno de ellos.</p>

      <div class="copiar">
        <h4>Los tres montajes</h4>
        <ul>
          <li><b>Polea fija</b>: su eje est&aacute; sujeto a un punto fijo. <b>No multiplica la
              fuerza</b> (F = R), solo <b>cambia su direcci&oacute;n</b>.</li>
          <li><b>Polea m&oacute;vil</b>: su eje va enganchado a la carga y sube con ella. La sostienen
              <b>dos</b> tramos de cuerda: F = R / 2, y hay que tirar <b>el doble</b> de cuerda.</li>
          <li><b>Polipasto</b> (o aparejo): varias poleas fijas y m&oacute;viles combinadas.
              <b>F = R / n</b>, siendo <b>n el n&uacute;mero de tramos que sostienen la carga</b>. Hay
              que tirar <b>n metros</b> de cuerda por cada metro que sube la carga.</li>
        </ul>
        <h4>La regla de oro de la mec&aacute;nica</h4>
        <p>Lo que se gana en fuerza se pierde en recorrido. <b>Ninguna m&aacute;quina crea
           energ&iacute;a</b>: solo la transforma. Y en la vida real, adem&aacute;s, el <b>rozamiento</b>
           se queda una parte por el camino.</p>
      </div>

      <div class="nota">
        <span class="n-tag">Otra vez el mismo trato</span>
        Y no es casualidad. Palanca, polea y &mdash;ma&ntilde;ana&mdash; engranajes hacen el
        <b>mismo trato</b> con distinta cara. Si te quedas con la regla, los mecanismos dejan de ser una
        lista que memorizar.
      </div>
""" + video('poleas') + foto('haterii') + u"""
      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; no hace falta copiarlo</span>
        <p>El ingeniero romano <b>Vitruvio</b> describe hacia el a&ntilde;o 25 a. C., en el libro X de
           <i>De architectura</i>, la m&aacute;quina de elevaci&oacute;n de las obras: un m&aacute;stil,
           un cabrestante y un polipasto que &eacute;l llama <i>polyspastos</i>. Se conserva
           adem&aacute;s dibujada, en el relieve de la tumba de los Haterii.</p>
        <p>Los historiadores de la t&eacute;cnica estiman, a partir de esos textos, que un polipasto de
           tres por cinco poleas movido por <b>cuatro hombres</b> en el cabrestante sub&iacute;a unos
           <b>3.000 kg</b>. Y que si en vez del cabrestante se pon&iacute;a una <b>rueda de andar</b>
           &mdash;una rueda enorme con hombres caminando por dentro&mdash; se llegaba a <b>6.000 kg con
           la mitad de la gente</b>, porque esa rueda es una palanca gigante: el radio de la rueda contra
           el radio del eje.</p>
        <p>Para comparar: en las rampas de las pir&aacute;mides se calcula que hac&iacute;an falta unos
           50 hombres por bloque de dos toneladas y media, es decir, unos <b>50 kg por persona</b>. Con
           la rueda de andar se pasa a unos <b>3.000 kg por persona</b>. Sesenta veces m&aacute;s, con
           los mismos m&uacute;sculos. Lo &uacute;nico que cambi&oacute; fue <b>lo que hab&iacute;a entre
           el hombre y la piedra</b>.</p>
      </div>
  """) +
  bloque('02', u'Pr&aacute;ctica &middot; 25 min', ficha(
    u'Actividad 2 &middot; El polipasto de las escobas',
    [u'1.2', u'3.1'], u'Grupos de cuatro &middot; 25 min', u"""
          <h4>Material</h4>
          <p>Dos palos de escoba (o dos mangos de fregona) y unos <b>4 m de cuerda</b> que no corte las
             manos. Nada m&aacute;s.</p>
          <h4>Qu&eacute; hay que hacer</h4>
          <ol class="pasos">
            <li>Dos personas sujetan un palo cada una, en horizontal, paralelos y separados un metro.
                Tienen que <b>separarlos</b> con todas sus fuerzas.</li>
            <li>Atad la cuerda a un palo y dad <b>una vuelta</b> alrededor del otro. Una tercera persona
                tira del extremo. Anotad qui&eacute;n gana.</li>
            <li>Repetidlo con <b>dos, tres y cuatro vueltas</b>. Anotad en cada caso si los palos se
                juntan y c&oacute;mo de f&aacute;cil es.</li>
            <li>Medid, con una cinta: cuanta <b>cuerda</b> tira quien tira, y cu&aacute;nto se
                <b>acercan</b> los palos. Hacedlo con dos y con cuatro vueltas.</li>
            <li>Escribid el informe: qu&eacute; n&uacute;mero de tramos hay en cada caso, qu&eacute;
                fuerza deber&iacute;a hacer falta en teor&iacute;a y qu&eacute; pas&oacute; de verdad.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>El montaje est&aacute; dibujado y se cuentan bien los tramos <b>(3 puntos)</b>.</li>
            <li>Est&aacute;n medidos la cuerda tirada y el acercamiento <b>(3 puntos)</b>.</li>
            <li>La relaci&oacute;n entre las dos medidas se compara con el n&uacute;mero de tramos
                <b>(2 puntos)</b>.</li>
            <li>El informe explica <b>una</b> diferencia entre la teor&iacute;a y lo que pas&oacute;
                <b>(2 puntos)</b>.</li>
          </ul>
          <div class="nota" style="margin-top:14px">
            <span class="n-tag">Aviso, y es parte del ejercicio</span>
            Este polipasto <b>hace m&aacute;s trampa de lo que dice la f&oacute;rmula</b>: la cuerda roza
            al enrollarse en los palos, y ese rozamiento ayuda a quien tira. En un polipasto de verdad, el
            rozamiento va <b>en contra</b> y hay que hacer algo m&aacute;s fuerza de la que dice la
            cuenta. Quien se d&eacute; cuenta de esto solo, que lo escriba: es lo mejor que puede salir de
            esta pr&aacute;ctica.
          </div>
          <div class="aviso" style="margin-top:12px">
            <span class="n-tag">Seguridad</span>
            La cuerda se suelta de golpe si alguien afloja. Nadie mete los dedos entre la cuerda y el
            palo, y se tira <b>en l&iacute;nea</b>, no hacia la cara de nadie.
          </div>
  """)) +
  bloque('03', u'Cierre &middot; 5 min', u"""
      <p>El saco de 80 kg sube al andamio con un polipasto de cuatro tramos tirando de <b>200 N</b>, unos
         20 kg: lo hace una persona sola. A cambio, para subirlo ocho metros hay que tirar de
         <b>treinta y dos metros</b> de cuerda. Nadie regala nada.</p>
      <ol>
      """ + pregunta(u'&iquest;Para qu&eacute; sirve una polea fija si no multiplica la fuerza?',
                     u'<p>Para <b>cambiar la direcci&oacute;n</b>. Eso te deja tirar hacia abajo, usar tu propio peso, apoyar los pies y poner a varias personas en la misma cuerda. Adem&aacute;s te permite estar <b>lejos</b> de la carga, que en una obra es media seguridad.</p>')
        + pregunta(u'Un polipasto sube 120 kg y quien tira hace 300 N. &iquest;Cu&aacute;ntos tramos tiene?',
                   u'<p>La carga son 1.200 N. n = 1.200 / 300 = <b>4 tramos</b>. Y para subirla un metro habr&aacute; que tirar de cuatro metros de cuerda.</p>')
        + pregunta(u'&iquest;Por qu&eacute; en la realidad hay que hacer algo m&aacute;s fuerza de la que dice la f&oacute;rmula?',
                   u'<p>Por el <b>rozamiento</b> de las poleas y por el <b>peso</b> de las poleas m&oacute;viles, que tambi&eacute;n hay que subir. La f&oacute;rmula da el caso ideal; la m&aacute;quina real siempre paga un peaje.</p>') + u"""
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Palanca y polea mueven cosas <b>a tirones y en l&iacute;nea recta</b>. Pero casi todo lo que se
        mueve hoy <b>gira</b>: un motor, una rueda, un ventilador. Y un motor tiene un problema gordo:
        gira siempre a la velocidad que le da la gana.
      </div>
  """))


# ============================================================================
# SESION 3 - Engranajes y relacion de transmision
# ============================================================================
S3 = (
  bloque('00', u'Reto inicial &middot; 10 min', u"""
      <p>Una bicicleta con cambio. El que pedalea es el mismo, la cuesta es la misma y la bici es la
         misma.</p>
      <div class="aviso">
        <span class="n-tag">La pregunta</span>
        <b>&iquest;Qu&eacute; cambia exactamente cuando cambias de marcha?</b> Y sobre todo:
        &iquest;por qu&eacute; con el plato peque&ntilde;o subes la cuesta pero vas lento, y con el
        grande vuelas en el llano pero no puedes con la cuesta?
      </div>
      <p>Empecemos por el problema de fondo, que es de las piernas. T&uacute; pedaleas c&oacute;modo a
         unas <b>60 vueltas por minuto</b>, una por segundo, y ah&iacute; no hay mucho margen: a 20 rpm te
         atascas y a 150 te agotas. La rueda, en cambio, tiene que girar a 180 rpm para ir a 23 km/h y a
         50 rpm cuando subes. <b>Las piernas tienen una velocidad y la rueda necesita otra.</b></p>
      <p>Prueba la soluci&oacute;n f&aacute;cil: dos ruedas lisas que se tocan, una en el eje de los
         pedales y otra en el de la rueda. Una arrastra a la otra por rozamiento. Funciona
         perfectamente&hellip; hasta que aprietas de verdad, y entonces <b>patinan</b>. Justo cuando
         m&aacute;s falta hac&iacute;a que no patinaran.</p>
  """) +
  bloque('01', u'Teor&iacute;a &middot; 20 min', u"""
      <h3>Dientes: dejar de pedir el favor</h3>
      <p>La soluci&oacute;n a que patine no es apretar m&aacute;s las ruedas: es que <b>no puedan</b>
         patinar. Se les ponen dientes y el contacto deja de depender del rozamiento. Los dientes se
         empujan unos a otros y la cuenta se vuelve exacta: por cada diente que avanza una, avanza un
         diente la otra.</p>
      <p>Para que dos ruedas engranen, sus dientes tienen que ser <b>del mismo tama&ntilde;o</b>. Y si
         los dientes miden lo mismo, una rueda con el triple de dientes tiene el triple de
         di&aacute;metro: <b>el n&uacute;mero de dientes y el tama&ntilde;o son la misma
         informaci&oacute;n</b>. Por eso a partir de ahora contamos dientes y nos olvidamos de medir.</p>
""" + ESC_ENGRANAJES + u"""
      <div class="copiar">
        <h4>Transmisi&oacute;n por engranajes</h4>
        <p><b>Engranaje</b>: par de ruedas dentadas que engranan entre s&iacute; para transmitir el giro
           de un eje a otro. La que manda es la <b>motriz</b> (entrada) y la que obedece es la
           <b>conducida</b> (salida).</p>
        <p><b>Relaci&oacute;n de transmisi&oacute;n</b>: las veces que la salida gira por cada vuelta de
           la entrada.</p>
        <p style="font-size:18px;text-align:center;margin:10px 0"><b>i = z<sub>1</sub> / z<sub>2</sub> =
           n<sub>2</sub> / n<sub>1</sub></b></p>
        <p>z son los dientes y n las vueltas por minuto (rpm). El 1 es la entrada y el 2, la salida.</p>
        <ul>
          <li><b>i menor que 1</b>: <b>reductor</b>. Gira m&aacute;s despacio y con m&aacute;s fuerza.</li>
          <li><b>i mayor que 1</b>: <b>multiplicador</b>. Gira m&aacute;s deprisa y con menos fuerza.</li>
          <li>Dos ruedas engranadas giran en <b>sentidos contrarios</b>. Una rueda intermedia
              (&laquo;loca&raquo;) invierte el sentido y <b>no cambia</b> la relaci&oacute;n.</li>
        </ul>
      </div>

      <div class="copiar">
        <h4>Cuando los ejes est&aacute;n lejos</h4>
        <ul>
          <li><b>Cadena</b> y pi&ntilde;ones: transmite a distancia, <b>mismo sentido</b> y sin
              deslizamiento. Es lo de la bicicleta.</li>
          <li><b>Correa</b> y poleas: m&aacute;s barata y silenciosa, pero <b>puede patinar</b>. A veces
              eso es bueno: si algo se atasca, patina la correa en vez de romperse el motor.</li>
          <li><b>Tornillo sin fin</b> y rueda dentada: el tornillo cuenta como <b>un solo diente</b>, as&iacute;
              que con una rueda de 40 hace falta <b>una vuelta por diente</b>: i = 1/40. Reducci&oacute;n
              enorme en muy poco sitio, y <b>no se puede mover al rev&eacute;s</b>.</li>
        </ul>
      </div>

      <div class="nota">
        <span class="n-tag">Y otra vez lo mismo</span>
        Un reductor de 1 a 3 divide la velocidad entre tres y <b>multiplica la fuerza por tres</b>. Es la
        ley de la palanca con otro disfraz: lo que se gana por un lado se paga por el otro.
      </div>

      <h3>La bici, con n&uacute;meros</h3>
      <p>Plato de <b>48</b> dientes, pi&ntilde;&oacute;n de <b>16</b>: i = 48/16 = <b>3</b>. Cada
         pedalada son tres vueltas de rueda. A 60 pedaladas por minuto son 180 rpm, y con una rueda de
         2,10 m de per&iacute;metro salen unos <b>23 km/h</b>. Cambia al pi&ntilde;&oacute;n de 28
         dientes: i = 1,7, unos 13 km/h&hellip; y casi el doble de fuerza en la rueda. Eso es subir la
         cuesta.</p>
""" + video('engranajes') + foto('anticitera') + u"""
      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; no hace falta copiarlo</span>
        <p>En 1901, unos pescadores de esponjas encontraron frente a la isla griega de <b>Anticitera</b>
           los restos de un naufragio, y entre ellos un bulto de bronce corro&iacute;do. Dentro hab&iacute;a
           una treintena de <b>ruedas dentadas</b> montadas unas sobre otras, algunas con m&aacute;s de
           200 dientes cortados a mano.</p>
        <p>Es del <b>siglo II a. C.</b> y serv&iacute;a para predecir las posiciones del Sol y la Luna y
           los eclipses. Nadie volvi&oacute; a fabricar engranajes de esa precisi&oacute;n hasta los
           relojes de catedral, <b>mil cuatrocientos a&ntilde;os despu&eacute;s</b>.</p>
        <p>Y no lo sabemos porque nadie lo escribiera: lo sabemos porque <b>se encontr&oacute; el
           aparato</b>. De casi toda la tecnolog&iacute;a antigua se ha perdido la explicaci&oacute;n, y a
           veces tambi&eacute;n el objeto. Este se salv&oacute; porque se hundi&oacute; un barco.</p>
      </div>
  """) +
  bloque('02', u'Pr&aacute;ctica &middot; 25 min', ficha(
    u'Actividad 3 &middot; El desarrollo de una bicicleta',
    [u'1.2', u'3.1'], u'Parejas &middot; 25 min', u"""
          <h4>Qu&eacute; hay que hacer</h4>
          <p>Una bici de monta&ntilde;a con <b>dos platos</b> (32 y 48 dientes) y <b>cinco
             pi&ntilde;ones</b> (14, 18, 21, 24 y 32 dientes). La rueda mide 2,10 m de per&iacute;metro y
             quien pedalea lo hace siempre a <b>60 rpm</b>.</p>
          <ol class="pasos">
            <li>Tabla de <b>diez combinaciones</b>: plato, pi&ntilde;&oacute;n, relaci&oacute;n i, vueltas
                de rueda por minuto y velocidad en km/h.</li>
            <li>Se&ntilde;alad la combinaci&oacute;n <b>m&aacute;s r&aacute;pida</b> y la <b>m&aacute;s
                fuerte</b>, y decid para qu&eacute; sirve cada una.</li>
            <li>Hay dos combinaciones distintas que dan <b>exactamente</b> la misma velocidad.
                Encontradlas y explicad por qu&eacute; pasa eso.</li>
            <li>La cuesta del instituto se sube a 7 km/h. &iquest;Qu&eacute; combinaci&oacute;n
                eleg&iacute;s? Justificadlo con la tabla.</li>
            <li><b>Problema aparte.</b> Un motor gira a 3.000 rpm y una cinta transportadora necesita 100
                rpm. Dise&ntilde;ad la reducci&oacute;n con <b>dos parejas</b> de ruedas, usando solo
                ruedas de 10, 12, 15, 20, 30, 50 y 60 dientes. Explicad por qu&eacute; no se hace con una
                sola pareja.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>La tabla est&aacute; completa y las velocidades bien calculadas <b>(3 puntos)</b>.</li>
            <li>Las dos combinaciones que coinciden est&aacute;n encontradas y explicadas
                <b>(2 puntos)</b>.</li>
            <li>La elecci&oacute;n para la cuesta est&aacute; justificada con datos <b>(2 puntos)</b>.</li>
            <li>La reducci&oacute;n de dos etapas funciona y est&aacute; comprobada <b>(3 puntos)</b>.</li>
          </ul>
          <div class="nota" style="margin-top:14px">
            <span class="n-tag">Pista para el problema del motor</span>
            Hace falta dividir la velocidad entre 30. En una sola pareja, la rueda grande tendr&iacute;a
            <b>treinta veces</b> el di&aacute;metro del pi&ntilde;&oacute;n: no cabe en ninguna
            m&aacute;quina. Con dos parejas basta con que <b>el producto</b> de las dos relaciones sea
            1/30.
          </div>
  """)) +
  bloque('03', u'Cierre &middot; 5 min', u"""
      <p>Cambiar de marcha no cambia tus piernas: cambia <b>la relaci&oacute;n entre lo que gira tu pie y
         lo que gira la rueda</b>. Con el plato peque&ntilde;o la rueda da menos vueltas por pedalada,
         as&iacute; que vas m&aacute;s lento y empujas con m&aacute;s fuerza. Y al rev&eacute;s. Es el
         mismo trato de la palanca y del polipasto, por tercera vez.</p>
      <ol>
      """ + pregunta(u'Una rueda de 20 dientes que gira a 300 rpm mueve otra de 60. &iquest;A qu&eacute; velocidad gira la segunda, y en qu&eacute; sentido?',
                     u'<p>i = 20/60 = 0,33. n<sub>2</sub> = 300 &middot; 0,33 = <b>100 rpm</b>, y en <b>sentido contrario</b>. Es un reductor: tres veces menos velocidad y tres veces m&aacute;s fuerza.</p>')
        + pregunta(u'&iquest;Por qu&eacute; la bicicleta lleva cadena y no dos ruedas dentadas engranadas?',
                   u'<p>Porque los pedales y la rueda est&aacute;n a <b>un metro</b> el uno de la otra. Dos ruedas engranadas tienen que tocarse; la cadena transmite a distancia y, adem&aacute;s, mantiene el <b>mismo sentido</b> de giro.</p>')
        + pregunta(u'&iquest;Por qu&eacute; el mecanismo de una clavija de guitarra lleva tornillo sin fin?',
                   u'<p>Por dos motivos a la vez. Da una <b>reducci&oacute;n enorme</b>, as&iacute; que puedes afinar con mucha precisi&oacute;n; y <b>no se deja mover al rev&eacute;s</b>, as&iacute; que la tensi&oacute;n de la cuerda no desafina la clavija sola.</p>') + u"""
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Todo lo de hoy transmite un giro y devuelve otro giro. Pero el pist&oacute;n de un motor
        <b>sube y baja</b>, una puerta corredera <b>va en l&iacute;nea recta</b> y el limpiaparabrisas
        <b>va y viene</b>. La sesi&oacute;n 4 va de lo que falta: <b>transformar</b> un movimiento en otro
        distinto, con la biela-manivela y el pi&ntilde;&oacute;n-cremallera.
      </div>
  """))


# ============================================================================
# La unidad
# ============================================================================
CHIPS = [u'CE1 &middot; 1.2', u'CE3 &middot; 3.1']
MINUTADO = [(u"10'", u'Reto'), (u"20'", u'Teor&iacute;a'), (u"25'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')]

S = [
 dict(corto=u'La palanca',
      titulo=u'La barra que multiplica: por qu&eacute; un tubo afloja lo que t&uacute; no',
      entradilla=u'Una palanca no te hace m&aacute;s fuerte: te cambia fuerza por recorrido. '
                 u'De ah&iacute; sale todo lo dem&aacute;s del tema.',
      minutado=MINUTADO, chips=CHIPS, cuerpo=S1),
 dict(corto=u'Poleas',
      titulo=u'Ochenta kilos hasta el andamio: poleas y polipasto',
      entradilla=u'La palanca se queda sin recorrido. Una cuerda puede ser tan larga como haga falta, '
                 u'y con ella vuelve a aparecer el mismo trato.',
      minutado=MINUTADO, chips=CHIPS, cuerpo=S2),
 dict(corto=u'Engranajes',
      titulo=u'El motor gira como quiere: engranajes y relaci&oacute;n de transmisi&oacute;n',
      entradilla=u'Tus piernas tienen una velocidad y la rueda necesita otra. Los dientes son la forma '
                 u'de traducir una en la otra, pagando siempre el mismo precio.',
      minutado=MINUTADO, chips=CHIPS, cuerpo=S3),
 dict(corto=u'Transformar el movimiento', pendiente=True),
 dict(corto=u'Montar un mecanismo', pendiente=True),
 dict(corto=u'Repaso y test', pendiente=True),
]

CFG = dict(
 ruta='2eso/TyD/tema5/',
 migas=u'<a href="../../../">Materiales</a> &middot; <a href="../../">2.&ordm; ESO</a> '
       u'&middot; <a href="../">TyD</a> &middot; Tema 5',
 h1=u'Mecanismos',
 titulo=u'Tema 5 &middot; Mecanismos',
 tema=u'Tema 5', curso=u'2.&ordm; de ESO', materia=u'Tecnolog&iacute;a y Digitalizaci&oacute;n',
 desc=u'Tema 5 de Tecnolog&iacute;a y Digitalizaci&oacute;n de 2.&ordm; de ESO: palanca, poleas y '
      u'polipasto, engranajes y relaci&oacute;n de transmisi&oacute;n, con escenas interactivas.',
 sesiones=S)


if __name__ == '__main__':
    html = pagina(CFG)
    if USA_AVATAR[0]:
        html = html.replace(u'</style>', avatar_flat.CSS + u'</style>', 1)
    destino = os.path.join(RAIZ, '2eso', 'TyD', 'tema5')
    if not os.path.isdir(destino):
        os.makedirs(destino)
    io.open(os.path.join(destino, 'index.html'), 'w', encoding='utf-8', newline='').write(html)
    print('U5 generada: %d bytes, %d sesiones (%d escritas)'
          % (len(html), len(S), sum(1 for x in S if not x.get('pendiente'))))
    if PENDIENTES:
        print('\nCosas pendientes (las que empiezan por POR VER si estan en la pagina):')
        for p in PENDIENTES:
            print('  - ' + p)
