# -*- coding: utf-8 -*-
"""2.o TyD - U5 - Mecanismos: la fuerza, la velocidad y la direccion que necesito.

Genera 2eso/TyD/tema5/index.html con las SEIS sesiones escritas.

Las escenas de las sesiones 1 a 3 estan aqui; las de la 4, la 5 y la 6 viven en
u5_escenas2.py, porque el fichero se hacia inmanejable.

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
from u5_escenas2 import (ESC_BIELA, ESC_TRANSFORMA, ESC_PLANTILLA, ESC_CADENA,
                         CSS_TEST, test)
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
 # --- de aqui para abajo, las de las sesiones 4 y 5. Licencia comprobada contra
 # la API de Commons el 17-sep-2026 Y la imagen ABIERTA Y MIRADA una a una: son
 # las tres lo que dice su pie. Se sirve la version reducida que genera la propia
 # Commons (thumburl), no un recorte mio.
 'biela': dict(
   fichero=u'u5-biela-locomotora.jpg',
   url=u'https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/'
       u'11Ec45SMBBauma-20121014viii.jpg/1920px-11Ec45SMBBauma-20121014viii.jpg',
   pagina=u'https://commons.wikimedia.org/wiki/File:11Ec45SMBBauma-20121014viii.jpg',
   autor=u'Abderitestatos', licencia=u'CC BY 3.0',
   alt=u'Bajos de una locomotora de vapor vistos de lado: a la derecha el cilindro, del que sale '
       u'un v&aacute;stago horizontal; ese v&aacute;stago se une a una barra larga que baja hasta '
       u'un pasador montado fuera del centro de la rueda motriz',
   pie=u'Los bajos de una locomotora de vapor de 1911 (la Ec 4/5 n.&ordm; 11 del Dampfbahn Bern). '
       u'Se ve la cadena entera: el <b>cilindro</b>, a la derecha; el <b>v&aacute;stago</b> que sale de '
       u'&eacute;l empujado por el vapor; la <b>biela</b>, esa barra larga; y el pasador donde acaba, '
       u'montado <b>fuera del centro</b> de la rueda: esa es la <b>manivela</b>. El vapor empuja recto '
       u'y la rueda gira.'),
 'levas': dict(
   fichero=u'u5-arbol-levas.jpg',
   url=u'https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/'
       u'1-_nockenwelle.jpg/1920px-1-_nockenwelle.jpg',
   pagina=u'https://commons.wikimedia.org/wiki/File:1-_nockenwelle.jpg',
   autor=u'Elmschrat', licencia=u'CC BY 4.0',
   alt=u'Dos &aacute;rboles de levas de un motor de coche, expuestos en una vitrina: dos ejes de acero '
       u'con una hilera de piezas ovaladas montadas a distintos &aacute;ngulos',
   pie=u'Dos <b>&aacute;rboles de levas</b> de un motor de coche (Museo de la Industria de Chemnitz). '
       u'Cada bulto ovalado es una leva, y cada una abre una v&aacute;lvula. F&iacute;jate en que '
       u'<b>no est&aacute;n giradas igual</b>: esa diferencia de &aacute;ngulo es la que decide en '
       u'qu&eacute; orden se abre cada v&aacute;lvula. El motor entero est&aacute; <b>programado en '
       u'la forma y la posici&oacute;n</b> de estas piezas.'),
 'linterna': dict(
   fichero=u'u5-rueda-linterna.jpg',
   url=u'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/'
       u'Cage_Gear.png/1920px-Cage_Gear.png',
   pagina=u'https://commons.wikimedia.org/wiki/File:Cage_Gear.png',
   autor=u'Historic American Buildings Survey', licencia=u'Dominio p&uacute;blico',
   alt=u'Interior de un molino de viento de madera: una rueda grande con dientes rectangulares de '
       u'madera encajados en el borde engrana con un pi&ntilde;&oacute;n formado por barrotes '
       u'redondos entre dos discos',
   pie=u'El engranaje de madera de un molino de viento de Long Island. A la izquierda, la rueda '
       u'grande con los dientes <b>metidos uno a uno</b> en el borde; a la derecha, la '
       u'<b>linterna</b>: dos discos y unos barrotes redondos que hacen de dientes. Ni una curva '
       u'calculada: un carpintero repartiendo el contorno en partes iguales. Es exactamente lo que '
       u'vas a hacer t&uacute; hoy con cart&oacute;n, y el motivo por el que todo depende de una sola '
       u'medida: <b>lo que mide un diente</b>.'),
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
# vueltos a comprobar al escribir las sesiones 4, 5 y 6: los cuatro existen y el
# titulo y el canal coinciden con lo que dice esta tabla.
#
#   publicar = el video sale en la pagina (titulo y canal verificados)
#   visto    = alguien lo ha visto ENTERO y responde del contenido
#
# Los cuatro estan con visto=False a proposito: nadie del proyecto los ha visto
# de principio a fin. Salen publicados porque el canal y el titulo cuadran, pero
# antes de ponerlos en clase hay que verlos.
#
# OJO - las duraciones estaban MAL. Las tres primeras decian "unos 4/4/5
# minutos" y no lo son. Se han medido cargando cada video en el reproductor de
# YouTube (IFrame API, getDuration) el 17-sep-2026:
#   8fDOm-XJBOQ 2:00   AlAxnplUNH0 7:33   0pO6cHi3HzE 2:19   Dyee1JVYsd0 2:16
VIDEOS = {
 'palanca': dict(vid=u'8fDOm-XJBOQ', publicar=True, visto=False,
   titulo=u'Ley de la palanca (mecanismos)', canal=u'TECH LAPSE',
   dura=u'2 minutos',
   nota=u'Animaci&oacute;n de los tres g&eacute;neros con la ley aplicada paso a paso.'),
 'poleas': dict(vid=u'AlAxnplUNH0', publicar=True, visto=False,
   titulo=u'Polea fija, polea m&oacute;vil y polipasto', canal=u'tecnoblas2',
   dura=u'7 minutos y medio',
   nota=u'Ense&ntilde;a los tres montajes seguidos, con la cuerda que hay que tirar en cada uno.'),
 'engranajes': dict(vid=u'0pO6cHi3HzE', publicar=True, visto=False,
   titulo=u'Engranajes (Transmisi&oacute;n circular)', canal=u'TECH LAPSE',
   dura=u'2 minutos y medio',
   nota=u'Animaci&oacute;n de trenes de engranajes con la relaci&oacute;n de transmisi&oacute;n calculada.'),
 'biela': dict(vid=u'Dyee1JVYsd0', publicar=True, visto=False,
   titulo=u'La biela - manivela (mecanismo de transformaci&oacute;n)', canal=u'TECH LAPSE',
   dura=u'poco m&aacute;s de 2 minutos',
   nota=u'Del mismo profesor que los v&iacute;deos de la palanca y de los engranajes, as&iacute; que '
        u'usa el mismo vocabulario que hemos usado en clase.'),
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
            /* Si el cabo muerto se ata al bloque, el bloque tiene que llegar hasta
               ese punto: si no, la cuerda se queda colgando en el aire.          */
            if(d.ata === 'bloque') x0 = Math.min(x0, d.atax - 9);
            m += '<rect x="' + x0 + '" y="' + (yb+Rr) + '" width="' + (x1-x0) + '" height="10" rx="2" '
               + 'fill="var(--surface-2)" stroke="var(--ink-soft)" stroke-width="2"></rect>';
            m += '<path d="M' + d.carga + ' ' + (yb+Rr+10) + ' V' + (yb+Rr+26) + '" '
               + 'stroke="var(--ink-soft)" stroke-width="2.5"></path>';
          } else {
            m += '<path d="M' + d.carga + ' ' + yb + ' V' + (yb+Rr+26) + '" stroke="var(--goo-rojo)" '
               + 'stroke-width="2.6"></path>';
          }
          var yc = yb + Rr + 26;
          m += '<rect x="' + (d.carga-30) + '" y="' + yc + '" width="60" height="52" rx="3" '
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

          /* El nudo del cabo muerto: ese extremo no cuelga, esta atado. */
          if(n > 1){
            m += '<circle cx="' + d.atax + '" cy="' + ((d.ata === 'viga') ? YV : yb + Rr) + '" '
               + 'r="3.8" fill="var(--goo-rojo)"></circle>';
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
            <button type="button" data-e="cre">Pi&ntilde;&oacute;n y cremallera</button>
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
          cad: {z1:24, z2:12}, sin: {z1:1,  z2:40}, cre: {z1:12, z2:0}
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
          svg.setAttribute('viewBox', '0 0 640 300');
          svg.setAttribute('viewBox', '0 0 640 300');
          var c = C[modo], m = '', z1 = c.z1, z2 = c.z2;
          var i, n2;

          if(modo === 'cre'){
            /* Un pinon engranando con una barra dentada. La barra no gira:
               corre. Es el primer mecanismo del tema que no transmite un giro,
               sino que lo TRANSFORMA en movimiento recto.                    */
            svg.setAttribute('viewBox', '0 0 640 258');
            var rp = radio(z1);
            var cx = 320, YP = 150, cy = YP - rp;
            var pas1 = 2*Math.PI/z1, p = rp*pas1;
            var fase = -ang;
            var yCres = YP - MOD, yRaiz = YP + 1.25*MOD;
            var XA = 70, XB = 570, alto = 34;

            /* cuerpo de la cremallera */
            m += '<rect x="' + XA + '" y="' + yRaiz + '" width="' + (XB-XA) + '" height="' + alto
               + '" fill="var(--surface-2)" stroke="var(--ink-soft)" stroke-width="2"></rect>';

            /* los dientes: los del pinon, desenrollados */
            var d = '', k, xc, hay = false;
            for(k = -80; k < 160; k++){
              /* Al desenrollar hay que respetar de que lado cae cada diente:
                 uno que este a la izquierda del contacto tiene cos(a)<0, o sea
                 x menor. De ahi el signo menos. Con el signo cambiado la
                 cremallera corria justo al reves que el pinon.               */
              xc = cx - rp*(fase + k*pas1 - Math.PI/2) + p/2;
              if(xc < XA + 8 || xc > XB - 8) continue;
              if(!hay){ d += 'M' + (XA+2).toFixed(1) + ' ' + yRaiz.toFixed(1) + ' '; hay = true; }
              d += 'L' + (xc - 0.27*p).toFixed(1) + ' ' + yRaiz.toFixed(1) + ' ';
              d += 'L' + (xc - 0.17*p).toFixed(1) + ' ' + yCres.toFixed(1) + ' ';
              d += 'L' + (xc + 0.17*p).toFixed(1) + ' ' + yCres.toFixed(1) + ' ';
              d += 'L' + (xc + 0.27*p).toFixed(1) + ' ' + yRaiz.toFixed(1) + ' ';
            }
            if(hay){
              d += 'L' + (XB-2).toFixed(1) + ' ' + yRaiz.toFixed(1);
              m += '<path d="' + d + '" fill="var(--surface-2)" stroke="var(--goo-azul)" stroke-width="2.2"></path>';
            }

            m += rueda(cx, cy, z1, fase, 'var(--accent-soft)');

            /* hacia donde corre la cremallera */
            /* el pinon gira en sentido antihorario, asi que su punto de contacto
               -y con el la cremallera- se va hacia la derecha */
            var xf = XB - 130, yf = yRaiz + alto + 26;
            m += '<path d="M' + xf + ' ' + yf + ' H' + (xf+90) + '" stroke="var(--goo-rojo)" stroke-width="3"></path>';
            m += '<path d="M' + (xf+90) + ' ' + yf + ' l-12 -6 v12 Z" fill="var(--goo-rojo)"></path>';
            m += '<text x="' + (xf-10) + '" y="' + (yf+4) + '" text-anchor="end" class="rotulo-svg" '
               + 'style="fill:var(--goo-rojo)">la cremallera no gira: corre</text>';

            m += etiqueta(cx, cy - rp - 34, z1, '60', 'el pi&ntilde;&oacute;n, de entrada');
            m += '<text x="20" y="22" class="rotulo-svg" style="font-size:12.5px;fill:var(--ink)">'
               + 'Pi&ntilde;&oacute;n de 12 dientes, m&oacute;dulo 4 &nbsp;&#8594;&nbsp; una vuelta corre 151 mm</text>';
            svg.innerHTML = m;
            pie.innerHTML = 'Esto ya <b>no es transmitir</b> un giro: es <b>transformarlo</b>. El pi&ntilde;&oacute;n da '
              + 'vueltas y la barra corre en l&iacute;nea recta, tanto como mide el contorno del pi&ntilde;&oacute;n '
              + 'por cada vuelta: &pi; &middot; m&oacute;dulo &middot; dientes = 3,14 &middot; 4 &middot; 12 = <b>151 mm</b>. Es lo que llevan la direcci&oacute;n de un coche, un taladro de columna y '
              + 'las puertas correderas de los garajes. Los mecanismos que transforman el movimiento son '
              + 'la <b>sesi&oacute;n siguiente</b>.';
            return;
          }

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
              /* mismo cuidado con el signo que en la cremallera: el filete
                 tiene que correr hacia donde va el punto de contacto de la rueda */
              xc = cx - rp*(fase + k*pas2 - Math.PI/2) + p/2;
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
            /* 18 px entre los dos rotulos, no 13: en un movil estrecho el
               navegador agranda el cuerpo de letra respecto al viewBox y con 13
               se montaban el uno sobre el otro. */
            m += '<text x="' + xi + '" y="' + (yi-Ri-20) + '" text-anchor="middle" class="rotulo-svg" '
               + 'style="fill:var(--ink)">el tornillo, por el extremo</text>';
            m += '<text x="' + xi + '" y="' + (yi-Ri-2) + '" text-anchor="middle" class="rotulo-svg">'
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



      <h3>Para qu&eacute; sirve esto de verdad: la caja de cambios</h3>
      <p>Un motor de gasolina solo da fuerza en una franja estrecha de vueltas, m&aacute;s o menos
         entre 2.000 y 5.000 por minuto. Pero el coche tiene que arrancar parado en una cuesta
         <i>y</i> tambi&eacute;n ir a 120 por autov&iacute;a. Con una sola relaci&oacute;n es imposible.</p>
      <p>La soluci&oacute;n es exactamente lo que acabas de ver: <b>varios pares de ruedas dentadas</b>
         montados sobre dos ejes, y una palanca que elige cu&aacute;l de ellos transmite.</p>

      <div class="escena" id="esc-caja">
        <div class="escena-barra">
          <span class="escena-titulo">Mete una marcha &middot; el motor gira siempre a 3.000 rpm</span>
          <div class="seg" id="seg-caja">
            <button type="button" data-m="0" aria-pressed="true">1.&ordf;</button>
            <button type="button" data-m="1">2.&ordf;</button>
            <button type="button" data-m="2">3.&ordf;</button>
            <button type="button" data-m="3">4.&ordf;</button>
            <button type="button" data-m="4">5.&ordf;</button>
            <button type="button" data-m="5">Atr&aacute;s</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 700 330" id="svg-caja" role="img"
               aria-label="Caja de cambios: dos ejes con pares de ruedas dentadas de distinto tama&ntilde;o"></svg>
        </div>
        <div class="pie" id="pie-caja"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-caja');
        var pie = document.getElementById('pie-caja');
        var seg = document.getElementById('seg-caja');
        if(!svg) return;

        var M = 3;                     /* modulo, en pixeles de diametro por diente */
        var RPM = 3000;                /* el motor, constante */
        var AZ='var(--goo-azul)', RO='var(--goo-rojo)', GR='var(--ink-soft)',
            TI='var(--ink)', SU='var(--accent-soft)', S2='var(--surface-2)';

        /* Los dos ejes estan a una distancia fija, asi que TODOS los pares
           suman los mismos dientes. Eso no es un capricho del dibujo: es lo
           que obliga la geometria de una caja de cambios de verdad.        */
        var SUMA = 60;
        var MAR = [
          {n:'1.&ordf;', z1:13, z2:47, d:'Arrancar, cuestas, maniobras. El motor da <b>tres vueltas y media</b> '
            +'por cada vuelta de la salida: mucha fuerza y poca velocidad.'},
          {n:'2.&ordf;', z1:19, z2:41, d:'Para coger algo de velocidad sin perder empuje. Es la marcha de '
            +'salir de una rotonda.'},
          {n:'3.&ordf;', z1:24, z2:36, d:'Ciudad. Ya se reparte parecido entre fuerza y velocidad.'},
          {n:'4.&ordf;', z1:28, z2:32, d:'Carretera. Queda poca reducci&oacute;n: casi tanta vuelta a la salida '
            +'como a la entrada.'},
          {n:'5.&ordf;', z1:33, z2:27, d:'Autov&iacute;a. Aqu&iacute; la caja <b>multiplica</b>: la salida gira m&aacute;s '
            +'deprisa que el motor, y por eso no hay fuerza para adelantar sin reducir antes.'},
          {n:'Atr&aacute;s', z1:13, z2:47, loca:20, d:'Los mismos dientes que la primera, pero con una '
            +'<b>rueda intermedia</b> metida en medio. No cambia la relaci&oacute;n: lo &uacute;nico que hace es '
            +'<b>invertir el sentido</b> de giro. Por eso la marcha atr&aacute;s va tan despacio.'}
        ];
        var sel = 0, ang = 0, raf = null, ultimo = 0;

        function radio(z){ return M*z/2; }

        function rueda(cx, cy, z, fase, col, borde){
          var rp = radio(z), ra = rp + M, rf = rp - 1.25*M;
          var pas = 2*Math.PI/z, d = '', k, j, a, r, x, y;
          for(k = 0; k < z; k++){
            var t = fase + k*pas;
            var pts = [[t - pas*0.27, rf], [t - pas*0.17, ra],
                       [t + pas*0.17, ra], [t + pas*0.27, rf]];
            for(j = 0; j < 4; j++){
              a = pts[j][0]; r = pts[j][1];
              x = cx + r*Math.cos(a); y = cy + r*Math.sin(a);
              d += (d === '' ? 'M' : 'L') + x.toFixed(1) + ' ' + y.toFixed(1) + ' ';
            }
          }
          d += 'Z';
          var m = '<path d="' + d + '" fill="' + col + '" stroke="' + borde + '" stroke-width="1.5"></path>';
          m += '<circle cx="' + cx + '" cy="' + cy + '" r="' + (rp*0.22).toFixed(1)
             + '" fill="var(--surface)" stroke="' + borde + '" stroke-width="2"></circle>';
          m += '<path d="M' + cx + ' ' + cy + ' L' + (cx + rp*0.8*Math.cos(fase)).toFixed(1) + ' '
             + (cy + rp*0.8*Math.sin(fase)).toFixed(1) + '" stroke="' + TI + '" stroke-width="2.4"></path>';
          return m;
        }

        function rot(x, y, t, col, tam){
          return '<text x="' + x + '" y="' + y + '" class="rotulo-svg" style="font-size:'
               + (tam || 12) + 'px;fill:' + (col || GR) + '">' + t + '</text>';
        }

        function pinta(){
          var g = MAR[sel];
          var r1 = radio(g.z1), r2 = radio(g.z2);
          var D = radio(SUMA);                 /* distancia entre los dos ejes */
          var cx = 300, y1 = 92, y2 = y1 + D;
          var i = g.z1/g.z2;                   /* relacion de transmision */
          var rpm2 = RPM*i;
          var m = '';

          /* los dos ejes, que no cambian nunca */
          m += '<path d="M40 ' + y1 + ' H660" stroke="' + GR + '" stroke-width="1.2" stroke-dasharray="7 5"></path>';
          m += '<path d="M40 ' + y2 + ' H660" stroke="' + GR + '" stroke-width="1.2" stroke-dasharray="7 5"></path>';
          m += rot(44, y1 - 10, 'EJE DEL MOTOR', GR, 11);
          m += rot(44, y2 + 22, 'EJE DE SALIDA', GR, 11);

          if(g.loca){
            /* La rueda intermedia tiene que tocar a las dos. Su centro sale de
               resolver el triangulo, no de ponerlo a ojo: esta a r1+rl del eje
               de arriba y a rl+r2 del de abajo.                               */
            var rl = radio(g.loca);
            var d1 = r1 + rl, d2 = rl + r2, Dx = D + 34;
            var yl = (Dx*Dx + d1*d1 - d2*d2)/(2*Dx);
            var xl = Math.sqrt(Math.max(0, d1*d1 - yl*yl));
            var y2b = y1 + Dx;
            m += '<path d="M40 ' + y2b + ' H660" stroke="' + GR + '" stroke-width="1.2" stroke-dasharray="7 5"></path>';
            m += rueda(cx, y1, g.z1, ang, SU, AZ);
            m += rueda(cx + xl, y1 + yl, g.loca, -ang*g.z1/g.loca + Math.PI/7, S2, RO);
            m += rueda(cx, y2b, g.z2, ang*g.z1/g.z2 + Math.PI/9, SU, AZ);
            /* el rotulo a la izquierda: a la derecha chocaba con los numeros */
            var xr = cx + xl - rl - 14;
            m += '<text x="' + xr + '" y="' + (y1 + yl - 3) + '" text-anchor="end" '
               + 'class="rotulo-svg" style="fill:' + RO + '">rueda intermedia</text>';
            m += '<text x="' + xr + '" y="' + (y1 + yl + 14) + '" text-anchor="end" '
               + 'class="rotulo-svg" style="fill:' + RO + '">o &laquo;loca&raquo;</text>';
          } else {
            m += rueda(cx, y1, g.z1, ang, SU, AZ);
            m += rueda(cx, y2, g.z2, -ang*g.z1/g.z2 + Math.PI/g.z2, SU, AZ);
          }

          /* los numeros */
          var xt = 470;
          m += rot(xt, 40, 'MARCHA ' + g.n, TI, 13);
          m += rot(xt, 62, 'z del motor: ' + g.z1 + ' dientes');
          m += rot(xt, 80, 'z de salida: ' + g.z2 + ' dientes');
          m += rot(xt, 104, 'i = ' + g.z1 + ' / ' + g.z2 + ' = ' + i.toFixed(2), TI, 13);
          m += rot(xt, 126, 'salida: ' + Math.round(rpm2) + ' rpm', TI, 13);
          m += rot(xt, 146, (i < 1 ? 'fuerza &times; ' + (1/i).toFixed(1)
                                   : 'fuerza &times; ' + (1/i).toFixed(2) + ' (pierde)'),
                   i < 1 ? 'var(--goo-verde)' : RO, 13);
          m += rot(40, 302, 'Todos los pares suman ' + SUMA + ' dientes: los ejes est&aacute;n '
                 + 'a una distancia fija.', GR, 11.5);
          svg.innerHTML = m;
          pie.innerHTML = '<b>' + g.n + '.</b> ' + g.d;
        }

        function cuadro(t){
          if(!ultimo) ultimo = t;
          var dt = Math.min(0.05, (t - ultimo)/1000);
          ultimo = t;
          ang += 0.9*dt;
          pinta();
          raf = requestAnimationFrame(cuadro);
        }

        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-m]'); if(!b) return;
          seg.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          sel = +b.dataset.m; pinta();
        });
        raf = requestAnimationFrame(cuadro);
      })();
      </script>

      <div class="copiar">
        <h4>La caja de cambios</h4>
        <p>Es un conjunto de <b>pares de ruedas dentadas</b> montados sobre dos ejes. La palanca elige
           cu&aacute;l de los pares transmite el giro del motor a las ruedas.</p>
        <ul>
          <li>Marchas <b>cortas</b> (1.&ordf;, 2.&ordf;): mucha reducci&oacute;n &rarr; <b>mucha fuerza y poca
              velocidad</b>. Para arrancar y subir cuestas.</li>
          <li>Marchas <b>largas</b> (4.&ordf;, 5.&ordf;): poca o ninguna reducci&oacute;n &rarr; <b>mucha
              velocidad y poca fuerza</b>. Para carretera.</li>
          <li>La <b>marcha atr&aacute;s</b> a&ntilde;ade una rueda intermedia que solo invierte el sentido.</li>
        </ul>
        <p>Y el trato de siempre: la caja <b>no crea fuerza</b>. Lo que gana en fuerza lo paga en
           vueltas, exactamente igual que la palanca y que el polipasto.</p>
      </div>

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
# SESION 4 - Transformar el movimiento
# ============================================================================
S4 = (
  bloque('00', u'Reto inicial &middot; 10 min', u"""
      <p>Repasa lo de las tres sesiones anteriores y busca lo que tienen en com&uacute;n. La palanca
         recibe un empuj&oacute;n y devuelve un empuj&oacute;n. El polipasto recibe un tir&oacute;n y
         devuelve un tir&oacute;n. Los engranajes reciben un giro y devuelven un giro. <b>Siempre sale
         lo mismo que entr&oacute;</b>, cambiado de tama&ntilde;o pero no de clase.</p>
      <p>Y resulta que casi nada de lo que te rodea funciona as&iacute;. El motor de un coche gira,
         pero dentro lo que hay es un <b>pist&oacute;n que sube y baja</b>. El motor del port&oacute;n
         del garaje gira, pero la puerta <b>corre recta</b>. El limpiaparabrisas <b>va y viene</b>. La
         aguja de una m&aacute;quina de coser <b>sube y baja</b> mientras el motor da vueltas.</p>
      <div class="aviso">
        <span class="n-tag">La pregunta</span>
        Tienes un motor, que solo sabe girar, y necesitas mover algo <b>en l&iacute;nea recta</b>.
        <b>&iquest;C&oacute;mo lo haces?</b> Y la de vuelta, que es m&aacute;s dif&iacute;cil todav&iacute;a:
        dentro del motor la explosi&oacute;n empuja el pist&oacute;n <b>recto</b>&hellip; y por el
        cig&uuml;e&ntilde;al sale un <b>giro</b>. &iquest;Qui&eacute;n hace esa traducci&oacute;n?
      </div>
      <h3>La soluci&oacute;n f&aacute;cil, y por qu&eacute; no sirve</h3>
      <p>Lo primero que se le ocurre a casi todo el mundo ya lo sabes hacer: <b>enrollar una cuerda en
         un tambor</b>. Giras el tambor y la cuerda se recoge, tirando de lo que sea en l&iacute;nea
         recta. Es el torno del pozo de toda la vida, y funciona.</p>
      <p>Funciona para sacar un cubo de agua. Para lo dem&aacute;s se cae por cuatro sitios, y conviene
         verlos uno a uno porque cada uno explica un mecanismo de hoy:</p>
      <ul>
        <li>Una cuerda <b>solo tira</b>. No empuja. La mitad de las m&aacute;quinas necesitan empujar.</li>
        <li><b>No vuelve sola.</b> Para que baje hace falta que algo la baje: la gravedad, otra cuerda,
            un peso.</li>
        <li>Conforme se enrolla, la cuerda se monta sobre s&iacute; misma y el tambor <b>engorda</b>:
            cada vuelta sube un poco m&aacute;s que la anterior. <b>No puedes calcular</b> cu&aacute;nto
            sube por vuelta, y eso descarta la cuerda para cualquier cosa de precisi&oacute;n.</li>
        <li>Y sobre todo: un motor de coche hace <b>3.000 vueltas por minuto</b>. Cincuenta por segundo.
            Una cuerda ah&iacute; no dura ni un minuto.</li>
      </ul>
      <p>As&iacute; que hace falta otra cosa. Cuatro cosas, en realidad, y cada una resuelve un caso
         distinto.</p>
  """) +
  bloque('01', u'Teor&iacute;a &middot; 20 min', u"""
      <h3>Transmitir y transformar no son lo mismo</h3>
      <p>Aqu&iacute; se parte el tema en dos mitades, y el corte es este: en las sesiones anteriores el
         movimiento <b>se transmit&iacute;a</b> &mdash;entraba un giro y sal&iacute;a un giro&mdash;. A
         partir de ahora el movimiento <b>se transforma</b>: entra un giro y sale otra cosa. Cambia la
         <b>naturaleza</b> del movimiento, no solo su tama&ntilde;o.</p>

      <div class="copiar">
        <h4>Las dos familias de mecanismos</h4>
        <ul>
          <li><b>De transmisi&oacute;n</b>: la salida es del <b>mismo tipo</b> que la entrada. Palanca,
              poleas, engranajes, cadena, correa, tornillo sin fin.</li>
          <li><b>De transformaci&oacute;n</b>: la salida es de <b>otro tipo</b>. Casi siempre entra un
              giro y sale un movimiento <b>rectil&iacute;neo</b> (todo seguido en l&iacute;nea recta) o
              <b>alternativo</b> (ir y venir sin parar).</li>
        </ul>
      </div>

      <h3>El primero: biela y manivela</h3>
      <p>Coge una barra y sujeta un extremo a un punto de una rueda que <b>no sea el centro</b>. El otro
         extremo, a algo que solo pueda ir y venir en l&iacute;nea recta. Ya est&aacute;. Ese punto
         descentrado es la <b>manivela</b> y la barra es la <b>biela</b>.</p>
      <p>Mira la escena. Y no mires solo el dibujo: mira la <b>gr&aacute;fica de abajo</b>, que dice
         d&oacute;nde est&aacute; el pist&oacute;n en cada grado de la vuelta. Cambia la longitud de la
         biela con los botones y fíjate en dos cosas: en que la <b>carrera no cambia</b>, y en que la
         curva <b>s&iacute; cambia</b>.</p>
""" + ESC_BIELA + u"""
      <p>La primera es la que hay que quedarse: la carrera del pist&oacute;n es <b>siempre el
         di&aacute;metro de la circunferencia que describe la mu&ntilde;eta</b>, o sea el doble del radio
         de la manivela. Da igual lo larga que sea la biela. Si quieres m&aacute;s recorrido, no alargues
         la biela: <b>descentra m&aacute;s la manivela</b>.</p>
      <p>La segunda es m&aacute;s fina, y es la que explica que un motor suene como suena: el
         pist&oacute;n <b>no va y viene a velocidad constante</b>. A un cuarto de vuelta ya ha recorrido
         m&aacute;s de la mitad del camino, porque la biela, al inclinarse, lo empuja de lado. Cuanto
         m&aacute;s corta es la biela, m&aacute;s brusco es el reparto.</p>

      <div class="copiar">
        <h4>Biela-manivela</h4>
        <p>Transforma un movimiento <b>circular</b> en uno <b>alternativo</b> (de ida y vuelta), y
           tambi&eacute;n al rev&eacute;s.</p>
        <p><b>Carrera = 2 &middot; r</b>, siendo r el radio de la manivela. La longitud de la biela
           <b>no</b> cambia la carrera.</p>
        <p>Funciona igual de bien en los <b>dos sentidos</b>, y es el &uacute;nico que convierte un
           vaiv&eacute;n en <b>vueltas enteras, una detr&aacute;s de otra</b>. Por eso con &eacute;l un
           motor convierte los empujones del pist&oacute;n en giro, y una m&aacute;quina de coser
           convierte el giro en el sube y baja de la aguja.</p>
        <h4>Los puntos muertos</h4>
        <p>Dos veces por vuelta, la biela y la manivela quedan <b>en l&iacute;nea</b>. En esa
           posici&oacute;n el pist&oacute;n empuja justo hacia el eje de giro y <b>no consigue hacer girar
           nada</b>. Para pasar de ah&iacute; hace falta un <b>volante</b>: una rueda pesada que guarda la
           inercia de la vuelta anterior.</p>
      </div>

      <div class="nota">
        <span class="n-tag">Por qu&eacute; te cuesta arrancar la bici cuesta arriba</span>
        Te pasa cuando el pedal se te queda <b>arriba del todo</b>: por mucho que pises, no avanza. Eso es
        un punto muerto, exactamente el mismo. La soluci&oacute;n tambi&eacute;n es la misma: mover el
        pedal un poco para salir de la l&iacute;nea. Y por eso las bielas de una bici van <b>a 180
        grados</b>: cuando una est&aacute; en el punto muerto, la otra est&aacute; en el mejor sitio.
      </div>
""" + video('biela') + foto('biela') + u"""
      <h3>Los otros tres, y qu&eacute; resuelve cada uno</h3>
      <p>La biela-manivela solo sabe hacer una cosa: ir y venir, siempre igual, con la misma carrera. Para
         lo dem&aacute;s hay otros tres mecanismos, y cada uno es el mejor en algo.</p>
""" + ESC_TRANSFORMA + u"""
      <p>La <b>leva</b> merece que te pares un momento, porque es distinta de todo lo que llevas visto.
         En los dem&aacute;s mecanismos, el movimiento que sale est&aacute; decidido de antemano por la
         f&oacute;rmula. En la leva lo decides t&uacute;, <b>dibujando</b>: el radio que tenga la leva en
         cada &aacute;ngulo es la altura a la que va a estar el seguidor cuando pase por ah&iacute;.
         <b>La forma es el programa.</b></p>
      <p>Y tiene el precio de todo lo que empuja en una sola direcci&oacute;n: la leva sabe <b>subir</b>
         el seguidor, pero no sabe bajarlo. Baja por su peso o porque un <b>muelle</b> tira de &eacute;l.
         Si el muelle se rompe, el seguidor se queda arriba.</p>

      <div class="copiar">
        <h4>Los cuatro mecanismos de transformaci&oacute;n</h4>
        <ul>
          <li><b>Pi&ntilde;&oacute;n-cremallera</b>: rueda dentada + barra dentada. Giro &rarr;
              <b>rectil&iacute;neo</b>, tan largo como quieras. Por cada vuelta avanza <b>el contorno del
              pi&ntilde;&oacute;n</b>. <b>Reversible</b>. <i>Direcci&oacute;n del coche, taladro de
              columna, puertas correderas.</i></li>
          <li><b>Tornillo-tuerca</b>: giro &rarr; <b>rectil&iacute;neo</b>, lento y con much&iacute;sima
              fuerza. Por cada vuelta avanza <b>el paso de rosca</b>. <b>No es reversible</b>: la
              h&eacute;lice va tan tumbada que la carga no consigue hacerlo girar, y se queda donde lo
              dejas. <i>Gato del coche, tornillo de banco, sargento, prensa.</i></li>
          <li><b>Biela-manivela</b>: giro &harr; <b>alternativo</b>. Carrera = <b>2 &middot; r</b>.
              <b>Reversible</b>. <i>Motores, m&aacute;quina de coser, sierra de vaiv&eacute;n.</i></li>
          <li><b>Leva y seguidor</b>: giro &rarr; el movimiento que t&uacute; dibujes. Carrera =
              <b>radio m&aacute;ximo &minus; radio m&iacute;nimo</b>. <b>No es reversible</b> y necesita
              <b>muelle</b> para volver. <i>V&aacute;lvulas del motor, martinete, m&aacute;quinas
              autom&aacute;ticas antiguas.</i></li>
        </ul>
        <h4>Y el trato, por cuarta vez</h4>
        <p>El gato del coche multiplica tu fuerza <b>m&aacute;s de 300 veces</b>&hellip; y para subir el
           coche diez cent&iacute;metros tu mano tiene que recorrer m&aacute;s de <b>treinta metros</b>.
           Es la misma regla de la palanca, del polipasto y de los engranajes, llevada al extremo.</p>
      </div>
""" + foto('levas') + u"""
      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; no hace falta copiarlo</span>
        <p>La manivela parece una tonter&iacute;a &mdash;un mango torcido&mdash; y sin embargo tard&oacute;
           siglos en aparecer. Con biela, movida por agua, est&aacute; documentada en el
           <b>aserradero de Hier&aacute;polis</b>, en la actual Turqu&iacute;a, en un relieve del <b>siglo
           III</b>: una rueda de agua mueve, por medio de engranajes y dos bielas, dos sierras que van y
           vienen cortando piedra. Es la m&aacute;quina m&aacute;s antigua que se conoce con biela y
           manivela &mdash;y lo sabemos porque un molinero se la hizo esculpir <b>en su propia
           tumba</b>.</p>
        <p>Y lleg&oacute; a valer tanto que hubo <b>pleitos</b> por ella. En <b>1780</b>, James Pickard
           patent&oacute; en Inglaterra el uso de la manivela con un volante para sacar giro de una
           m&aacute;quina de vapor. <b>James Watt</b>, que estaba en lo mismo, se qued&oacute; fuera: tuvo
           que rodear la patente con otro mecanismo m&aacute;s complicado y peor, el <i>engranaje sol y
           planeta</i>, que patent&oacute; en 1781 a partir de una idea de su empleado William Murdoch.
           En cuanto la patente de Pickard caduc&oacute;, en <b>1794</b>, Boulton y Watt se pasaron a la
           manivela de toda la vida.</p>
        <p>Merece la pena pensarlo: durante catorce a&ntilde;os, la mejor m&aacute;quina de vapor del
           mundo llev&oacute; un mecanismo peor <b>por un motivo legal, no t&eacute;cnico</b>. La
           tecnolog&iacute;a no la deciden solo los ingenieros.</p>
      </div>
  """) +
  bloque('02', u'Pr&aacute;ctica &middot; 25 min', ficha(
    u'Actividad 4 &middot; Dibujar el movimiento que quieres',
    [u'1.2', u'3.1'], u'Parejas &middot; 25 min', u"""
          <h4>Material</h4>
          <p>Comp&aacute;s, transportador, regla y l&aacute;piz. Nada m&aacute;s.</p>
          <h4>Parte A &middot; La leva de una m&aacute;quina de sellar cajas</h4>
          <p>Una cinta transportadora lleva cajas. El sello est&aacute; <b>fijo arriba</b>, y debajo de la
             cinta hay una leva con su seguidor: cuando el seguidor sube, empuja la caja contra el sello.
             Tiene que subir, <b>apretar un rato</b>, bajar y esperar a la caja siguiente. El eje de la
             leva gira a <b>30 rpm</b>, y el seguidor tiene que estar a <b>20 mm</b> del eje cuando
             est&aacute; abajo y a <b>35 mm</b> cuando est&aacute; apretando.</p>
          <ol class="pasos">
            <li>Traza dos circunferencias conc&eacute;ntricas, de <b>20 y 35 mm de radio</b>, y divide la
                vuelta en <b>doce sectores de 30&ordm;</b> con el transportador.</li>
            <li>Marca en cada radio el punto que dice esta tabla, midiendo desde el centro. Va en dos
                mitades para que se lea en el m&oacute;vil; es una sola vuelta:
                <table style="width:100%;border-collapse:collapse;margin:8px 0;font-size:14px">
                  <tr><td style="padding:3px 4px"><b>&aacute;ngulo</b></td>
                      <td style="padding:3px 4px">0&ordm;</td><td style="padding:3px 4px">30&ordm;</td>
                      <td style="padding:3px 4px">60&ordm;</td><td style="padding:3px 4px">90&ordm;</td>
                      <td style="padding:3px 4px">120&ordm;</td><td style="padding:3px 4px">150&ordm;</td></tr>
                  <tr><td style="padding:3px 4px"><b>radio</b></td>
                      <td style="padding:3px 4px">20</td><td style="padding:3px 4px">20</td>
                      <td style="padding:3px 4px">20</td><td style="padding:3px 4px">25</td>
                      <td style="padding:3px 4px">30</td><td style="padding:3px 4px">35</td></tr>
                </table>
                <table style="width:100%;border-collapse:collapse;margin:8px 0;font-size:14px">
                  <tr><td style="padding:3px 4px"><b>&aacute;ngulo</b></td>
                      <td style="padding:3px 4px">180&ordm;</td><td style="padding:3px 4px">210&ordm;</td>
                      <td style="padding:3px 4px">240&ordm;</td><td style="padding:3px 4px">270&ordm;</td>
                      <td style="padding:3px 4px">300&ordm;</td><td style="padding:3px 4px">330&ordm;</td></tr>
                  <tr><td style="padding:3px 4px"><b>radio</b></td>
                      <td style="padding:3px 4px">35</td><td style="padding:3px 4px">35</td>
                      <td style="padding:3px 4px">35</td><td style="padding:3px 4px">28</td>
                      <td style="padding:3px 4px">20</td><td style="padding:3px 4px">20</td></tr>
                </table>
            </li>
            <li>Une los doce puntos con una curva suave, <b>a mano alzada</b>. Eso es la leva.</li>
            <li>Contesta, con la leva delante: <b>&iquest;cu&aacute;nto vale la carrera?</b>
                <b>&iquest;cu&aacute;ntos grados est&aacute; el sello apretando?</b> &iquest;y
                <b>cu&aacute;ntas cajas por minuto</b> sella la m&aacute;quina?</li>
            <li>Dibuja debajo la <b>gr&aacute;fica</b> de la altura del seguidor: el &aacute;ngulo en el
                eje horizontal, la altura en el vertical. Doce puntos y a unirlos.</li>
          </ol>
          <h4>Parte B &middot; Dos problemas de n&uacute;meros</h4>
          <ol class="pasos" start="6">
            <li><b>El gato.</b> Un gato de tornillo tiene una palanca de <b>30 cm</b> y un paso de rosca
                de <b>4 mm</b>. El coche pesa <b>1.200 kg</b> (12.000 N). Calcula: cu&aacute;nto recorre tu
                mano en una vuelta, la ventaja mec&aacute;nica, la fuerza que haces&hellip; y
                <b>cu&aacute;ntos metros recorre tu mano</b> para subir el coche 12 cm.</li>
            <li><b>El port&oacute;n.</b> Una puerta corredera de garaje mide <b>2,40 m</b> y la mueve un
                pi&ntilde;&oacute;n de <b>16 dientes y m&oacute;dulo 3 mm</b>. Calcula el di&aacute;metro
                del pi&ntilde;&oacute;n, lo que avanza la puerta en cada vuelta y <b>cu&aacute;ntas
                vueltas</b> hacen falta para abrirla del todo.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>La leva est&aacute; trazada con los doce radios y los doce puntos medidos
                <b>(3 puntos)</b>.</li>
            <li>Las tres preguntas sobre la leva est&aacute;n contestadas con su n&uacute;mero
                <b>(2 puntos)</b>.</li>
            <li>La gr&aacute;fica de la altura est&aacute; dibujada y se parece a la leva
                <b>(1 punto)</b>.</li>
            <li>El problema del gato est&aacute; completo, <b>incluido el recorrido de la mano</b>
                <b>(2 puntos)</b>.</li>
            <li>El problema del port&oacute;n est&aacute; completo <b>(2 puntos)</b>.</li>
          </ul>
          <div class="nota" style="margin-top:14px">
            <span class="n-tag">Lo que de verdad se eval&uacute;a</span>
            El recorrido de la mano en el gato. Sale un n&uacute;mero <b>rid&iacute;culo</b>, y est&aacute;
            bien: es el precio de multiplicar la fuerza por casi quinientos. Si alguien lo da por
            equivocado porque &laquo;no puede ser tanto&raquo;, ah&iacute; hay una conversaci&oacute;n
            que vale por media clase.
          </div>
  """)) +
  bloque('03', u'Cierre &middot; 5 min', u"""
      <p>Ya est&aacute;n las dos respuestas. De giro a recto: <b>pi&ntilde;&oacute;n-cremallera</b> si
         quieres recorrido, <b>tornillo-tuerca</b> si quieres fuerza, <b>leva</b> si quieres un
         movimiento con su propio gui&oacute;n. Y de recto a giro, uno por encima de todos: la
         <b>biela-manivela</b>, la &uacute;nica que convierte un ir y venir en <b>vueltas enteras</b>,
         una detr&aacute;s de otra. Por eso est&aacute; dentro de todos los motores del mundo. El
         pi&ntilde;&oacute;n-cremallera tambi&eacute;n se deja empujar por los dos lados, pero la barra
         <b>se acaba</b>: da un trozo de giro, no vueltas sin fin.</p>
      <ol>
      """ + pregunta(u'La manivela de una sierra de vaiv&eacute;n tiene 18 mm de radio. &iquest;Cu&aacute;nto recorre la hoja en cada pasada, y qu&eacute; pasa si pongo una biela m&aacute;s larga?',
                     u'<p>La carrera es <b>2 &middot; 18 = 36 mm</b>. Y con una biela m&aacute;s larga la carrera <b>no cambia</b>: sigue siendo 36 mm. Lo &uacute;nico que cambia es que el movimiento sale m&aacute;s suave. Para alargar la pasada hay que <b>descentrar m&aacute;s la manivela</b>.</p>')
        + pregunta(u'&iquest;Por qu&eacute; una leva necesita un muelle y una biela-manivela no?',
                   u'<p>Porque la leva <b>solo empuja</b>: el seguidor se apoya en el perfil y este lo levanta, pero no tiene c&oacute;mo tirar de &eacute;l hacia abajo. El muelle es el que lo hace volver. La biela, en cambio, va <b>atornillada por los dos extremos</b>, as&iacute; que tira y empuja igual de bien.</p>')
        + pregunta(u'Quieres levantar un armario 5 cm para meterle una cu&ntilde;a. &iquest;Tornillo-tuerca o pi&ntilde;&oacute;n-cremallera?',
                   u'<p><b>Tornillo-tuerca</b>, sin dudarlo. El recorrido es cort&iacute;simo &mdash;5 cm&mdash; y la fuerza es enorme, que es justo su terreno. Y adem&aacute;s <b>no se suelta</b> al soltarlo t&uacute;, mientras que la cremallera se ir&iacute;a para abajo con el peso.</p>') + u"""
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Llevas cuatro sesiones de mecanismos y no has tocado ninguno. La pr&oacute;xima toca
        <b>montarlo</b>: dos ruedas dentadas de cart&oacute;n, hechas por ti, que engranen de verdad y
        cuya relaci&oacute;n de transmisi&oacute;n puedas <b>contar girando</b>. Aviso: si las recortas a
        ojo, no engranan. Hay una medida que hay que decidir <b>antes</b> de coger el comp&aacute;s.
      </div>
  """))


# ============================================================================
# SESION 5 - Montar un mecanismo (taller)
# ============================================================================
S5 = (
  bloque('00', u'Reto inicial &middot; 10 min', u"""
      <p>Cuatro sesiones mirando mecanismos. Hoy se monta uno, y se mide.</p>
      <p>El encargo es concreto: un <b>reductor de 1 a 2</b>. Una rueda peque&ntilde;a que arrastre a una
         grande y que la grande d&eacute; <b>media vuelta</b> por cada vuelta de la peque&ntilde;a.
         Material: cart&oacute;n de una caja, dos chinchetas y un trozo de cart&oacute;n de base.
         Presupuesto: <b>cero euros</b>.</p>
      <p>La soluci&oacute;n que se le ocurre a todo el mundo: recorto un c&iacute;rculo, le pinto
         <b>12 dientes</b>; recorto otro el doble de grande, le pinto <b>24</b>; chincheta, chincheta y a
         girar.</p>
      <div class="aviso">
        <span class="n-tag">Lo que pasa de verdad</span>
        <b>No engranan.</b> O se atascan, o los dientes se montan unos encima de otros, o hay un hueco
        por el que la rueda patina media vuelta. Y no es por recortar mal: falla aunque recortes
        perfecto.
      </div>
      <h3>Por qu&eacute; falla</h3>
      <p>Piensa en el punto donde se tocan las dos ruedas. Ah&iacute; los dientes de una tienen que
         meterse en los huecos de la otra, uno detr&aacute;s de otro, sin adelantarse ni retrasarse.
         Para eso hace falta que el diente de una <b>mida exactamente lo mismo</b> que el hueco de la
         otra.</p>
      <p>Y ah&iacute; est&aacute; el error. Al recortar cada rueda por separado, cada uno reparte los
         dientes que le tocan en el contorno que le ha salido, y le sale un diente de un tama&ntilde;o
         distinto. No se trata de ser m&aacute;s cuidadoso: es que <b>se ha elegido mal qu&eacute;
         decidir primero</b>.</p>
      <div class="aviso">
        <span class="n-tag">La pregunta</span>
        &iquest;Qu&eacute; medida hay que decidir <b>antes</b> de coger el comp&aacute;s, y qu&eacute;
        medidas dejan entonces de poder elegirse?
      </div>
  """) +
  bloque('01', u'El trazado &middot; 15 min', u"""
      <h3>Se elige el diente, no la rueda</h3>
      <p>Lo primero que se decide en un engranaje <b>no es el di&aacute;metro</b>: es el
         <b>tama&ntilde;o del diente</b>. Una vez elegido, el di&aacute;metro ya no se elige, <b>se
         calcula</b>.</p>
      <p>El razonamiento es de una l&iacute;nea. Si una rueda tiene z dientes y cada diente ocupa p
         mil&iacute;metros de contorno, su contorno entero mide p &middot; z. Y como el contorno de una
         circunferencia es &pi; &middot; d, sale que <b>d = p &middot; z / &pi;</b>. Ese
         <b>p / &pi;</b> aparece tantas veces que tiene nombre propio: el <b>m&oacute;dulo</b>.</p>

      <div class="copiar">
        <h4>El m&oacute;dulo</h4>
        <p>El <b>m&oacute;dulo m</b> es la medida que fija el <b>tama&ntilde;o del diente</b>. Se da en
           mil&iacute;metros y es lo primero que se elige.</p>
        <p style="font-size:18px;text-align:center;margin:10px 0"><b>d = m &middot; z</b></p>
        <p>d es el <b>di&aacute;metro primitivo</b> &mdash;la circunferencia que de verdad rueda, que no
           es ni la de las puntas ni la del fondo&mdash; y z es el n&uacute;mero de dientes.</p>
        <p><b>Dos ruedas solo engranan si tienen el mismo m&oacute;dulo.</b> Es la regla entera.</p>
        <h4>Las dem&aacute;s medidas salen de ah&iacute;</h4>
        <ul>
          <li><b>Paso</b> (contorno por diente): p = &pi; &middot; m</li>
          <li><b>Di&aacute;metro exterior</b> (hasta la punta): d<sub>e</sub> = d + 2m</li>
          <li><b>&Aacute;ngulo entre dientes</b>: 360&ordm; / z</li>
          <li><b>Distancia entre centros</b> de dos ruedas engranadas:
              <b>(d<sub>1</sub> + d<sub>2</sub>) / 2</b></li>
        </ul>
      </div>

      <p>Prueba en la escena. Cambia el m&oacute;dulo y mira c&oacute;mo crecen las dos ruedas a la vez;
         cambia los dientes y mira c&oacute;mo cambia la distancia entre los centros. Los n&uacute;meros
         de abajo son <b>los que vas a usar ahora mismo</b> con el comp&aacute;s: ap&uacute;ntalos antes
         de empezar.</p>
""" + ESC_PLANTILLA + u"""
      <div class="copiar">
        <h4>C&oacute;mo se traza una rueda dentada</h4>
        <ol>
          <li>Calcula <b>d = m &middot; z</b> y <b>d<sub>e</sub> = d + 2m</b>. Divide los dos entre 2:
              son los dos radios del comp&aacute;s.</li>
          <li>Marca el centro y traza las <b>dos circunferencias</b>.</li>
          <li>Con el transportador, marca <b>un radio cada 360&ordm;/z</b>. Cada radio es el
              <b>centro de un diente</b>.</li>
          <li>A cada lado de ese radio, sobre la circunferencia primitiva, marca <b>un cuarto de paso</b>
              (p/4). Eso da el ancho del diente.</li>
          <li>Une cada marca con la circunferencia exterior y recorta el hueco entre dientes.</li>
          <li>P&iacute;ntale una raya a <b>un diente</b>: es la que vas a seguir para contar vueltas.</li>
        </ol>
        <p>&#9888; Los dientes de verdad no tienen los lados rectos: llevan una curva llamada
           <b>evolvente</b>, que hace que el contacto sea suave. Con cart&oacute;n y tijeras eso no se
           puede trazar, as&iacute; que los haremos rectos. Engranar&aacute;n con alg&uacute;n
           trompic&oacute;n, y es un trompic&oacute;n que vale la pena notar: es exactamente el problema
           que resuelve la evolvente.</p>
      </div>
""" + foto('linterna') + u"""
      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; no hace falta copiarlo</span>
        <p>Durante siglos, los engranajes se hicieron exactamente como los vas a hacer t&uacute;: un
           carpintero repartiendo un contorno en partes iguales. Los molinos de viento y de agua
           llevaban ruedas de varios metros con los dientes <b>metidos uno a uno</b> en el borde, como
           tacos.</p>
        <p>Y eso ten&iacute;a una ventaja que hoy se ha perdido: cuando un diente se romp&iacute;a,
           <b>se cambiaba ese diente</b>. Adem&aacute;s se hac&iacute;an a prop&oacute;sito de una madera
           m&aacute;s blanda que el resto, para que la pieza que se partiera fuese siempre la barata. Hoy
           eso se llama <b>pieza de sacrificio</b> y se sigue usando: el fusible de tu casa es lo mismo.</p>
        <p>Lo que cambi&oacute; con la industria no fue la idea, fue la <b>norma</b>. Cuando el
           m&oacute;dulo se normaliz&oacute;, una rueda hecha en una f&aacute;brica empez&oacute; a
           engranar con otra hecha en otra f&aacute;brica, a mil kil&oacute;metros. Eso es lo que de
           verdad vale del m&oacute;dulo: no que sirva para calcular, sino que sirve para
           <b>ponerse de acuerdo</b>.</p>
      </div>
  """) +
  bloque('02', u'Taller &middot; 30 min', ficha(
    u'Actividad 5 &middot; Un reductor de cart&oacute;n que se pueda medir',
    [u'1.2', u'3.1'], u'Parejas &middot; 30 min', u"""
          <h4>Material, por pareja</h4>
          <p>Cart&oacute;n de caja (dos trozos de una cuartilla y uno grande de base), <b>tres
             chinchetas</b>, comp&aacute;s, transportador, regla, tijeras y un boli. Si hay cart&oacute;n
             ondulado, mejor: aguanta la chincheta sin doblarse.</p>
          <h4>Qu&eacute; hay que hacer</h4>
          <ol class="pasos">
            <li>Trabajad con <b>m&oacute;dulo 6</b>. Uno de los dos traza la rueda de <b>12 dientes</b> y
                el otro la de <b>24</b>, siguiendo los seis pasos del trazado. Antes de dibujar nada,
                <b>escribid en el cuaderno</b> los dos radios y el &aacute;ngulo entre dientes de vuestra
                rueda, sacados de la escena.</li>
            <li>Recortad las dos y clavadlas en la base con las chinchetas, a la <b>distancia entre
                centros</b> que os diga la cuenta. Sin apretar del todo: tienen que girar.</li>
            <li><b>Comprobad que engranan.</b> Si se atascan, mirad de d&oacute;nde viene: casi siempre es
                que un hueco ha quedado estrecho. Ensanchadlo con las tijeras y anotad lo que
                pas&oacute;.</li>
            <li><b>La medida.</b> Con la raya de boli como referencia, dad <b>diez vueltas completas</b>
                a la rueda grande contando en voz alta, y contad cu&aacute;ntas da la peque&ntilde;a.
                Anotad el n&uacute;mero de verdad, salga lo que salga.</li>
            <li>Comparadlo con la cuenta: z<sub>2</sub> / z<sub>1</sub>. &iquest;Cuadra?
                &iquest;En cu&aacute;nto os hab&eacute;is desviado?</li>
            <li>Mirad el <b>sentido</b> de giro de las dos y anotadlo con una flecha en el dibujo.</li>
            <li><b>La rueda loca.</b> Juntaos con otra pareja y pedidles <b>su rueda de 12</b>. Montad un
                tren de tres en l&iacute;nea: vuestra rueda de 12, la de ellos <b>en medio</b> y vuestra
                rueda de 24. Ojo, ahora hay <b>dos distancias entre centros</b> distintas: calculadlas
                antes de clavar nada. Volved a contar diez vueltas: &iquest;ha cambiado la
                relaci&oacute;n? &iquest;y el sentido de giro de la &uacute;ltima?</li>
            <li>Informe, media cara: el dibujo del montaje con las medidas, la tabla de vueltas contadas,
                la relaci&oacute;n medida, la calculada y <b>una explicaci&oacute;n de la diferencia</b>.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Las medidas est&aacute;n calculadas y escritas <b>antes</b> de trazar <b>(2 puntos)</b>.</li>
            <li>Las dos ruedas est&aacute;n trazadas con comp&aacute;s y transportador, no a ojo
                <b>(2 puntos)</b>.</li>
            <li>El montaje <b>gira</b> y los dientes engranan <b>(2 puntos)</b>.</li>
            <li>Las vueltas est&aacute;n contadas y comparadas con la relaci&oacute;n calculada
                <b>(2 puntos)</b>.</li>
            <li>Est&aacute; anotado qu&eacute; hace la rueda loca con la relaci&oacute;n y con el sentido
                <b>(1 punto)</b>.</li>
            <li>El informe explica <b>una</b> causa concreta de la diferencia <b>(1 punto)</b>.</li>
          </ul>
          <div class="nota" style="margin-top:14px">
            <span class="n-tag">Lo que de verdad se eval&uacute;a</span>
            El &uacute;ltimo punto, otra vez. Con cart&oacute;n y tijeras <b>nunca</b> va a salir 2,00
            exacto: el cart&oacute;n se aplasta, la chincheta tiene holgura, los dientes son rectos y no
            de evolvente. Quien mida 2,00 clavado, casi seguro que no ha contado; quien mida 2,1 y sepa
            decir por qu&eacute;, ha entendido el taller.
          </div>
          <div class="aviso" style="margin-top:12px">
            <span class="n-tag">Seguridad y orden</span>
            Las chinchetas se clavan <b>desde arriba</b> y sobre la base, nunca sobre la mesa ni sobre la
            mano. Al acabar se recogen <b>contadas</b>: salieron tres por pareja y vuelven tres. Las
            tijeras, cerradas y por el mango.
          </div>
  """)) +
  bloque('03', u'Cierre &middot; 5 min', u"""
      <p>La pregunta del principio ten&iacute;a una respuesta de tres palabras: <b>el tama&ntilde;o del
         diente</b>. Se elige el m&oacute;dulo, y a partir de ah&iacute; el di&aacute;metro, el
         di&aacute;metro exterior y la distancia entre los ejes <b>ya no se eligen</b>: se calculan. Es la
         primera vez en el tema que una cuenta no sirve para predecir, sino para <b>fabricar</b>.</p>
      <ol>
      """ + pregunta(u'Dos ruedas de m&oacute;dulo 4: una de 20 dientes y otra de 30. &iquest;A qu&eacute; distancia van los ejes?',
                     u'<p>d<sub>1</sub> = 4 &middot; 20 = <b>80 mm</b> y d<sub>2</sub> = 4 &middot; 30 = <b>120 mm</b>. La distancia entre centros es la <b>suma de los radios</b>: (80 + 120) / 2 = <b>100 mm</b>.</p>')
        + pregunta(u'Tienes una rueda de m&oacute;dulo 5 y otra de m&oacute;dulo 3. &iquest;Pueden engranar si las pones a la distancia justa?',
                   u'<p><b>No.</b> Da igual a qu&eacute; distancia las pongas: los dientes de una miden m&aacute;s que los huecos de la otra, as&iacute; que se montan. Para engranar hace falta <b>el mismo m&oacute;dulo</b>, y eso no se arregla moviendo los ejes.</p>')
        + pregunta(u'Quieres una rueda de m&oacute;dulo 6 que mida 90 mm de di&aacute;metro primitivo. &iquest;Cu&aacute;ntos dientes le pones?',
                   u'<p>z = d / m = 90 / 6 = <b>15 dientes</b>. Y si te sale un n&uacute;mero con decimales, no vale: los dientes son enteros. Habr&iacute;a que cambiar el di&aacute;metro o el m&oacute;dulo.</p>') + u"""
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Queda recoger. Cinco sesiones, un mont&oacute;n de mecanismos&hellip; y <b>una sola idea</b>
        debajo de todos ellos. La pr&oacute;xima la ponemos por escrito, montamos una m&aacute;quina
        entera encadenando lo que hemos visto, y hay <b>test que se corrige solo</b>.
      </div>
  """))


# ============================================================================
# SESION 6 - Repaso y test
# ============================================================================
# Las doce preguntas: las de cuenta estan resueltas y comprobadas en Python
# antes de escribirlas (ver el informe). data-ses dice a que sesion mandar al
# alumno si la falla.
PREGUNTAS = [
 dict(ses=u'1', ok=1,
   enun=u'Una llave de 20 cm no puede con una tuerca. Le metes un tubo y la llave pasa a medir 60 cm. '
        u'&iquest;Qu&eacute; le pasa a la fuerza que tienes que hacer?',
   ops=[u'Se multiplica por 3', u'Se divide entre 3',
        u'No cambia: solo es m&aacute;s c&oacute;modo de agarrar', u'Se divide entre 9'],
   fb=u'El brazo de tu fuerza se multiplica por 3, as&iacute; que la fuerza se divide entre 3. '
      u'De F &middot; b<sub>F</sub> = R &middot; b<sub>R</sub>: si b<sub>F</sub> se triplica, F se '
      u'reduce a la tercera parte. Y t&uacute; recorres el triple de arco.'),
 dict(ses=u'1', ok=1,
   enun=u'Una carretilla es una palanca de <b>segundo g&eacute;nero</b>. Eso quiere decir que&hellip;',
   ops=[u'el punto de apoyo est&aacute; en medio',
        u'la resistencia est&aacute; en medio, as&iacute; que siempre gana fuerza',
        u'la fuerza est&aacute; en medio, as&iacute; que siempre pierde fuerza',
        u'no tiene punto de apoyo'],
   fb=u'El apoyo es la rueda, en un extremo; t&uacute; est&aacute;s en el otro, en los mangos; y la '
      u'carga queda <b>en medio</b>. Como b<sub>F</sub> es forzosamente mayor que b<sub>R</sub>, una '
      u'palanca de segundo g&eacute;nero <b>siempre</b> multiplica la fuerza.'),
 dict(ses=u'1', ok=2,
   enun=u'Una palanca multiplica tu fuerza por 5. Para subir la carga 4 cm, tu mano recorre&hellip;',
   ops=[u'4 cm', u'0,8 cm', u'20 cm', u'100 cm'],
   fb=u'Lo que se gana en fuerza se paga en recorrido, y en la misma proporci&oacute;n: '
      u'5 &times; 4 = <b>20 cm</b>. Es la regla de oro, y vale para la palanca, el polipasto, los '
      u'engranajes y el gato del coche.'),
 dict(ses=u'2', ok=2,
   enun=u'Un polipasto sube <b>150 kg</b> y quien tira hace <b>375 N</b>. &iquest;Cu&aacute;ntos tramos '
        u'de cuerda sostienen la carga?',
   ops=[u'2 tramos', u'3 tramos', u'4 tramos', u'5 tramos'],
   fb=u'150 kg son 1.500 N. n = 1.500 / 375 = <b>4 tramos</b>. Y para subir la carga un metro, hay '
      u'que tirar de cuatro metros de cuerda.'),
 dict(ses=u'2', ok=0,
   enun=u'Si una polea fija no multiplica la fuerza, &iquest;para qu&eacute; se pone?',
   ops=[u'Para cambiar la <b>direcci&oacute;n</b> de la fuerza: as&iacute; puedes tirar hacia abajo, '
        u'colgarte y poner a m&aacute;s gente en la cuerda',
        u'Para que la cuerda no se desgaste',
        u'Para dividir la fuerza entre dos',
        u'Para que la carga suba m&aacute;s deprisa'],
   fb=u'Cambiar la direcci&oacute;n no multiplica nada, y aun as&iacute; puede ser media '
      u'soluci&oacute;n: tirando hacia abajo sumas tu propio peso, apoyas los pies y cabe m&aacute;s '
      u'gente en la cuerda. Adem&aacute;s te deja estar <b>lejos</b> de la carga.'),
 dict(ses=u'3', ok=1,
   enun=u'Una rueda de <b>15 dientes</b> que gira a <b>600 rpm</b> mueve a otra de <b>45 dientes</b>. '
        u'&iquest;A cu&aacute;ntas rpm gira la segunda?',
   ops=[u'1.800 rpm', u'200 rpm', u'600 rpm', u'45 rpm'],
   fb=u'i = z<sub>1</sub>/z<sub>2</sub> = 15/45 = 0,33. n<sub>2</sub> = 600 &middot; 0,33 = '
      u'<b>200 rpm</b>, y en sentido contrario. Es un reductor: tres veces menos velocidad y tres '
      u'veces m&aacute;s fuerza.'),
 dict(ses=u'3', ok=3,
   enun=u'&iquest;Qu&eacute; hace una rueda intermedia (una &laquo;loca&raquo;) metida entre otras dos?',
   ops=[u'Multiplica la relaci&oacute;n de transmisi&oacute;n por sus dientes',
        u'Divide la relaci&oacute;n entre sus dientes',
        u'No hace nada: es solo un apoyo',
        u'Invierte el sentido de giro y <b>no cambia</b> la relaci&oacute;n'],
   fb=u'Sus dientes se cancelan en la cuenta: lo que multiplica por un lado lo divide por el otro. '
      u'Lo &uacute;nico que consigue es <b>invertir el sentido</b>. Es exactamente lo que hace la '
      u'marcha atr&aacute;s de un coche.'),
 dict(ses=u'4', ok=1,
   enun=u'La manivela de una biela-manivela tiene <b>25 mm de radio</b>. La carrera del pist&oacute;n '
        u'es&hellip;',
   ops=[u'25 mm', u'50 mm', u'12,5 mm', u'depende de lo larga que sea la biela'],
   fb=u'Carrera = 2 &middot; r = <b>50 mm</b>, que es el di&aacute;metro de la circunferencia que '
      u'describe la mu&ntilde;eta. La biela <b>no</b> influye en la carrera: solo cambia lo brusco que '
      u'es el reparto dentro de cada vuelta.'),
 dict(ses=u'4', ok=2,
   enun=u'Un tornillo de banco tiene un paso de rosca de <b>3 mm</b>. Le das <b>7 vueltas</b>. '
        u'&iquest;Cu&aacute;nto se ha cerrado?',
   ops=[u'3 mm', u'7 mm', u'21 mm', u'2,3 mm'],
   fb=u'El paso es lo que avanza la tuerca en <b>una</b> vuelta, as&iacute; que 3 &times; 7 = '
      u'<b>21 mm</b>. Cuanto m&aacute;s fino sea el paso, m&aacute;s fuerza hace el tornillo y m&aacute;s '
      u'vueltas hay que dar.'),
 dict(ses=u'4', ok=3,
   enun=u'Necesitas que algo suba despacio, se quede quieto arriba un rato, caiga de golpe y espere. Una '
        u'y otra vez. &iquest;Qu&eacute; mecanismo eliges?',
   ops=[u'Pi&ntilde;&oacute;n-cremallera', u'Tornillo-tuerca', u'Biela-manivela',
        u'Leva y seguidor'],
   fb=u'Solo la <b>leva</b> sabe hacer un movimiento con gui&oacute;n propio, porque el gui&oacute;n '
      u'<b>es su forma</b>. La biela-manivela solo sabe ir y venir siempre igual, y los otros dos dan '
      u'un avance constante mientras giren.'),
 dict(ses=u'5', ok=1,
   enun=u'Dos ruedas dentadas de <b>m&oacute;dulo 5 mm</b>, una de <b>16 dientes</b> y otra de '
        u'<b>24</b>. &iquest;A qu&eacute; distancia hay que poner los dos ejes?',
   ops=[u'200 mm', u'100 mm', u'40 mm', u'20 mm'],
   fb=u'd = m &middot; z, as&iacute; que 80 mm y 120 mm. Los ejes van a la <b>suma de los radios</b>: '
      u'(80 + 120) / 2 = <b>100 mm</b>. Si te equivocas en esa medida, las ruedas no engranan por mucho '
      u'que est&eacute;n bien trazadas.'),
 dict(ses=u'6', ok=0,
   enun=u'Un motor de <b>1.500 rpm</b> pasa por un reductor de 12&rarr;48 dientes y luego por un '
        u'<b>tornillo sin fin</b> con una rueda de 40. &iquest;Qu&eacute; sale por el otro lado?',
   ops=[u'9,4 rpm, y la fuerza multiplicada por 160',
        u'9,4 rpm, y la fuerza dividida entre 160',
        u'375 rpm, y la fuerza multiplicada por 40',
        u'9,4 rpm, y la misma fuerza que a la entrada'],
   fb=u'Las relaciones se <b>multiplican</b>: i = (12/48) &middot; (1/40) = 0,00625. '
      u'1.500 &middot; 0,00625 = <b>9,4 rpm</b>. Y la fuerza va justo al rev&eacute;s: '
      u'1 / 0,00625 = <b>160 veces m&aacute;s</b>. Velocidad por 0,00625, fuerza por 160: el producto, '
      u'como siempre, <b>1</b>.'),
]

S6 = (
  bloque('00', u'El tema en una frase &middot; 5 min', u"""
      <p>Cinco sesiones. La palanca, la polea, el polipasto, los engranajes, la cadena, la correa, el
         tornillo sin fin, la caja de cambios, la biela-manivela, la leva, el tornillo-tuerca, el
         pi&ntilde;&oacute;n-cremallera. Parece una lista para memorizar, y no lo es: debajo de los doce
         hay <b>una sola idea</b>.</p>
      <div class="aviso">
        <span class="n-tag">La idea del tema</span>
        <b>Ning&uacute;n mecanismo regala nada.</b> Todos cambian una cosa por otra: fuerza por
        recorrido, velocidad por fuerza, o un tipo de movimiento por otro. Lo que sale multiplicado por
        un lado, sale dividido por el otro. Siempre.
      </div>
      <p>Si te acuerdas de eso, los mecanismos dejan de ser una lista. Y si alguien te ofrece uno que
         multiplica la fuerza <b>sin</b> pedir nada a cambio, ya sabes que te est&aacute; enga&ntilde;ando
         o que se ha equivocado.</p>
  """) +
  bloque('01', u'Repaso &middot; 20 min', u"""
      <h3>Una m&aacute;quina de verdad no lleva un mecanismo: lleva varios</h3>
      <p>Hasta ahora los hemos visto de uno en uno. En una m&aacute;quina de verdad van
         <b>encadenados</b>: el motor entra por un lado, atraviesa dos o tres etapas y por el otro
         extremo sale lo que hace falta.</p>
      <p>Y la cuenta es c&oacute;moda: las relaciones se <b>multiplican</b>. Monta tu m&aacute;quina en
         la escena, pulsando en los tres botones, y vigila el n&uacute;mero de la derecha del
         marcador.</p>
""" + ESC_CADENA + u"""
      <p>Ese <b>producto = 1</b> es el tema entero. Puedes hacer que la salida vaya 160 veces m&aacute;s
         despacio, y entonces ir&aacute; con 160 veces m&aacute;s fuerza. Puedes hacer que vaya tres
         veces m&aacute;s r&aacute;pida, y entonces tendr&aacute; la tercera parte de la fuerza. Lo que no
         puedes es quedarte con las dos cosas.</p>

      <div class="copiar">
        <h4>Cadenas de mecanismos</h4>
        <p>Cuando se encadenan etapas, la relaci&oacute;n total es el <b>producto</b> de las relaciones:
           i<sub>total</sub> = i<sub>1</sub> &middot; i<sub>2</sub> &middot; &hellip;</p>
        <p>La velocidad se multiplica por i<sub>total</sub> y la fuerza por 1 / i<sub>total</sub>. Su
           <b>producto vale 1</b>: ninguna m&aacute;quina crea energ&iacute;a.</p>
        <p>En la m&aacute;quina real sale algo <b>menos</b> de 1, porque el <b>rozamiento</b> se queda
           una parte por el camino. A esa fracci&oacute;n que s&iacute; llega se le llama
           <b>rendimiento</b>.</p>
      </div>

      <h3>Todo el tema, en una tabla</h3>
      <div class="copiar">
        <h4>Los mecanismos de la unidad</h4>
        <table style="width:100%;border-collapse:collapse;font-size:14.5px;margin-top:6px">
          <tr style="border-bottom:1.5px solid var(--line)">
            <td style="padding:5px 6px"><b>Mecanismo</b></td>
            <td style="padding:5px 6px"><b>Qu&eacute; hace</b></td>
            <td style="padding:5px 6px"><b>La cuenta</b></td></tr>
          <tr style="border-bottom:1px solid var(--line-soft)">
            <td style="padding:5px 6px">Palanca</td><td style="padding:5px 6px">multiplica fuerza</td>
            <td style="padding:5px 6px">F &middot; b<sub>F</sub> = R &middot; b<sub>R</sub></td></tr>
          <tr style="border-bottom:1px solid var(--line-soft)">
            <td style="padding:5px 6px">Polea fija</td><td style="padding:5px 6px">cambia la direcci&oacute;n</td>
            <td style="padding:5px 6px">F = R</td></tr>
          <tr style="border-bottom:1px solid var(--line-soft)">
            <td style="padding:5px 6px">Polipasto</td><td style="padding:5px 6px">multiplica fuerza</td>
            <td style="padding:5px 6px">F = R / n</td></tr>
          <tr style="border-bottom:1px solid var(--line-soft)">
            <td style="padding:5px 6px">Engranajes, cadena, correa</td>
            <td style="padding:5px 6px">cambia velocidad y fuerza</td>
            <td style="padding:5px 6px">i = z<sub>1</sub>/z<sub>2</sub> = n<sub>2</sub>/n<sub>1</sub></td></tr>
          <tr style="border-bottom:1px solid var(--line-soft)">
            <td style="padding:5px 6px">Tornillo sin fin</td>
            <td style="padding:5px 6px">reduce much&iacute;simo; no va al rev&eacute;s</td>
            <td style="padding:5px 6px">i = 1 / z</td></tr>
          <tr style="border-bottom:1px solid var(--line-soft)">
            <td style="padding:5px 6px">Pi&ntilde;&oacute;n-cremallera</td>
            <td style="padding:5px 6px">giro &harr; recto largo</td>
            <td style="padding:5px 6px">avance = &pi; &middot; m &middot; z por vuelta</td></tr>
          <tr style="border-bottom:1px solid var(--line-soft)">
            <td style="padding:5px 6px">Tornillo-tuerca</td>
            <td style="padding:5px 6px">giro &rarr; recto, mucha fuerza</td>
            <td style="padding:5px 6px">avance = el paso, por vuelta</td></tr>
          <tr style="border-bottom:1px solid var(--line-soft)">
            <td style="padding:5px 6px">Biela-manivela</td>
            <td style="padding:5px 6px">giro &harr; ir y venir</td>
            <td style="padding:5px 6px">carrera = 2 &middot; r</td></tr>
          <tr>
            <td style="padding:5px 6px">Leva y seguidor</td>
            <td style="padding:5px 6px">giro &rarr; el movimiento que dibujes</td>
            <td style="padding:5px 6px">carrera = r<sub>m&aacute;x</sub> &minus; r<sub>m&iacute;n</sub></td></tr>
        </table>
        <p style="margin-top:10px">Y <b>d = m &middot; z</b> para todo lo que lleve dientes.</p>
      </div>
  """) +
  bloque('02', u'Test &middot; 25 min', u"""
      <p>Doce preguntas de todo el tema. Cont&eacute;stalas <b>primero en el cuaderno</b>, con la cuenta
         escrita cuando haga falta, y luego m&aacute;rcalas aqu&iacute; y pulsa
         <i>Corregir el test</i>. Al corregir te dir&aacute; la nota y a qu&eacute; sesiones tienes que
         volver.</p>
      <div class="nota">
        <span class="n-tag">C&oacute;mo se usa esto</span>
        La nota de aqu&iacute; <b>no cuenta</b> para nada: es para ti. Lo que cuenta es lo que hagas
        despu&eacute;s con las que falles. Puedes repetirlo las veces que quieras.
      </div>
""" + test(PREGUNTAS) + u"""
  """) +
  bloque('03', u'Cierre del tema &middot; 10 min', u"""
      <p>Vuelve al principio del tema: <i>el m&uacute;sculo mueve poco y mal</i>. Ahora se puede decir
         exactamente qu&eacute; quiere decir. Tu brazo es una palanca de tercer g&eacute;nero que
         <b>pierde fuerza a prop&oacute;sito</b> para ganar velocidad, y todo el tema ha sido aprender a
         deshacer ese cambio cuando lo que hace falta es fuerza &mdash;o a llevarlo m&aacute;s
         lejos cuando lo que hace falta es velocidad.</p>
      <ol>
      """ + pregunta(u'Un amigo te dice que ha montado un mecanismo que multiplica la fuerza por 4 sin perder velocidad. &iquest;Qu&eacute; le contestas?',
                     u'<p>Que se ha equivocado midiendo, o que hay algo que no ha mirado. Si la fuerza se multiplica por 4, la velocidad se divide entre 4: el producto es 1. Y en la m&aacute;quina real es <b>menos</b> de 1, porque el rozamiento se lleva su parte. <b>No hay ning&uacute;n mecanismo que regale nada</b>: eso no es una regla de esta asignatura, es una consecuencia de que la energ&iacute;a no se crea.</p>')
        + pregunta(u'De todos los mecanismos del tema, &iquest;cu&aacute;les NO se pueden mover al rev&eacute;s, y qu&eacute; tienen en com&uacute;n?',
                   u'<p>El <b>tornillo sin fin</b> y el <b>tornillo-tuerca</b>, y la <b>leva</b> (que adem&aacute;s necesita muelle). Los dos primeros tienen en com&uacute;n la <b>h&eacute;lice muy tumbada</b>: la salida empuja casi perpendicular al giro y no consigue moverlo. Y eso, que suena a defecto, es justo lo que quieres en un port&oacute;n, en un gato o en una clavija de guitarra: que se quede donde lo has dejado.</p>')
        + pregunta(u'&iquest;Por qu&eacute; casi todos los mecanismos del tema aparecen en una bicicleta?',
                   u'<p>Porque una bici es una m&aacute;quina para <b>traducir</b> un m&uacute;sculo. Los pedales son una <b>manivela</b>; el plato y el pi&ntilde;&oacute;n, una transmisi&oacute;n por <b>cadena</b> con su relaci&oacute;n; los frenos de varilla, <b>palancas</b>; y las bielas van a 180&ordm; para que nunca est&eacute;n las dos en el <b>punto muerto</b>. Toda la bici es este tema.</p>') + u"""
      </ol>
      <div class="nota">
        <span class="n-tag">Y el tema que viene</span>
        Queda una cosa sin resolver, y es la de siempre: todos estos mecanismos necesitan que
        <b>alguien empuje por un extremo</b>. Hasta ahora ese alguien has sido t&uacute;, o el agua, o el
        viento. En el <b>tema 6</b> aparece una forma de energ&iacute;a que llega por un cable, se
        enciende con un interruptor y no se cansa: la <b>electricidad</b>.
      </div>
  """))


# ============================================================================
# La unidad
# ============================================================================
CHIPS = [u'CE1 &middot; 1.2', u'CE3 &middot; 3.1']
MINUTADO = [(u"10'", u'Reto'), (u"20'", u'Teor&iacute;a'), (u"25'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')]
# La 5 es de taller y la 6 de repaso: el reparto de los 60 minutos no es el mismo.
MIN_TALLER = [(u"10'", u'Reto'), (u"15'", u'Trazado'), (u"30'", u'Taller'), (u"5'", u'Cierre')]
MIN_REPASO = [(u"5'", u'La idea'), (u"20'", u'Repaso'), (u"25'", u'Test'), (u"10'", u'Cierre')]

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
 dict(corto=u'Transformar',
      titulo=u'El motor gira y el pist&oacute;n sube y baja: transformar el movimiento',
      entradilla=u'Hasta aqu&iacute; entraba un giro y sal&iacute;a un giro. Desde aqu&iacute; cambia la '
                 u'naturaleza del movimiento, y eso pide cuatro mecanismos nuevos.',
      minutado=MINUTADO, chips=CHIPS, cuerpo=S4),
 dict(corto=u'Montar un mecanismo',
      titulo=u'Dos ruedas de cart&oacute;n que engranen de verdad',
      entradilla=u'Recortadas a ojo no engranan, y no es por recortar mal. Hay una medida que se decide '
                 u'antes que ninguna otra, y a partir de ella el di&aacute;metro ya no se elige.',
      minutado=MIN_TALLER, chips=CHIPS, cuerpo=S5),
 dict(corto=u'Repaso y test',
      titulo=u'Ning&uacute;n mecanismo regala nada',
      entradilla=u'Doce mecanismos y una sola idea debajo. Se encadenan en una m&aacute;quina entera, se '
                 u'pone por escrito y se comprueba con doce preguntas que se corrigen solas.',
      minutado=MIN_REPASO, chips=CHIPS, cuerpo=S6),
]

CFG = dict(
 ruta='2eso/TyD/tema5/',
 migas=u'<a href="../../../">Materiales</a> &middot; <a href="../../">2.&ordm; ESO</a> '
       u'&middot; <a href="../">TyD</a> &middot; Tema 5',
 h1=u'Mecanismos',
 titulo=u'Tema 5 &middot; Mecanismos',
 tema=u'Tema 5', curso=u'2.&ordm; de ESO', materia=u'Tecnolog&iacute;a y Digitalizaci&oacute;n',
 desc=u'Tema 5 de Tecnolog&iacute;a y Digitalizaci&oacute;n de 2.&ordm; de ESO: palanca, poleas y '
      u'polipasto, engranajes y relaci&oacute;n de transmisi&oacute;n, transformaci&oacute;n del '
      u'movimiento, taller de engranajes de cart&oacute;n y test, con escenas interactivas.',
 sesiones=S)


# Nota: esta unidad parcheaba aqui el aviso de licencia porque el molde comun
# decia "dos son de dominio publico por su antiguedad" y en la U5 ya no cuadraba.
# Ese arreglo subio al molde (tema0_base.py), que ahora dice "algunas son de
# dominio publico" sin contar, asi que el parche sobra y se ha quitado.

if __name__ == '__main__':
    html = pagina(CFG)
    if USA_AVATAR[0]:
        html = html.replace(u'</style>', avatar_flat.CSS + u'</style>', 1)
    # El CSS del test tampoco va en el molde comun: lo usa solo la sesion 6.
    html = html.replace(u'</style>', CSS_TEST + u'</style>', 1)
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
