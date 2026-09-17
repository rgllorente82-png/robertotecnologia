# -*- coding: utf-8 -*-
"""Las escenas interactivas de la U9. SVG + JavaScript a mano, sin librerias.

Se separan del texto porque son lo unico del tema que hay que leer como codigo.
Todas CALCULAN: ninguna lleva dentro una tabla de resultados escrita a mano.

  ESCENA_MAQUETA  S1 · el mismo documento en dos ordenadores. Parte el texto en
                  lineas de verdad, con las anchuras AFM de tres tipografias, y
                  lo pagina. El numero de lineas, el de hojas y el sitio donde
                  cae la foto salen de esa cuenta.
  ESCENA_ESTILOS  S1 · indice automatico y cambio de aspecto. Los numeros de
                  pagina salen de paginar el documento; el numero de retoques a
                  mano, de contar los bloques que llevan formato propio.
  ESCENA_MAPA     S2 · el mismo dibujo como mapa de bits y como vectorial. El
                  mapa de bits se RASTERIZA aqui, midiendo la cobertura de la
                  figura casilla a casilla con 4x4 muestras, y se amplia.
  ESCENA_PESO     S2 · cuanto pesa una foto y cuanto de ella llega a verse, con
                  los pixeles que sobran y el ancho que mediria impresa.
  ESCENA_AULA     S3 · si la letra de la diapositiva se lee desde el fondo.
                  Geometria: cuerpo -> altura de mayuscula -> ampliacion del
                  proyector -> comparacion con lo que pide esa distancia.
  ESCENA_CARRERA  S3 · leer contra escuchar. Cuenta las palabras que hay
                  escritas en ese momento y compara los dos tiempos.

Geometria: todas las coordenadas estan calculadas, no puestas a ojo. Cada escena
dice arriba de que tamano es su lienzo y como se reparte.

Las cadenas de JS llevan \\uXXXX y no entidades HTML: una entidad HTML dentro de
una cadena de JavaScript se dibuja como seis caracteres y descuadra el ancho.
Para no escribirlas a mano esta _js(), que convierte un texto de Python. El pie
de cada escena, en cambio, se pone con innerHTML, y ahi las entidades van bien.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import u9_metricas


def _js(s):
    """Un texto de Python, listo para ir dentro de una cadena de JavaScript."""
    out = []
    for ch in s:
        if ch == u'\\':
            out.append(u'\\\\')
        elif ch == u"'":
            out.append(u"\\'")
        elif ord(ch) < 128:
            out.append(ch)
        else:
            out.append(u'\\u%04x' % ord(ch))
    return u''.join(out)


def _lit(s):
    return u"'" + _js(s) + u"'"


# ===========================================================================
# S1 · El mismo documento en dos ordenadores
#
# Lienzo 640 x 440.
#   k = 0,95 px de lienzo por milimetro de papel.
#     A4    210,0 x 297,0 mm ->  199,5 x 282,2 px
#     Carta 215,9 x 279,4 mm ->  205,1 x 265,4 px
#   Rotulos de columna  y 20 y 38 · hojas desde y = 52 (borde superior)
#   Columna A (donde se escribio) x 40 · columna B (el otro ordenador) x 360
#     A ocupa 40..239,5 y B como mucho 360..565,1: caben las dos.
#   Tira de la primera linea, de cerca: y 375..431.
#
# El motor: anchura de cada palabra sumando las anchuras AFM de sus letras,
# corte gloton (la linea se cierra cuando la palabra siguiente ya no cabe, que
# es lo que hace cualquier procesador), interlinea 1,35 y paginado por altura
# util. Las imagenes no se parten: si no caben, se van a la hoja siguiente.
# ===========================================================================
_TXT1 = u9_metricas.TEXTO
_TXT2 = (u'Un fichero de texto plano no guarda nada de todo eso: solo las letras, '
         u'una detrás de otra. Un documento de procesador guarda además las '
         u'marcas que dicen qué papel hace cada trozo, y deja para el final la '
         u'decisión de con qué letra se dibuja. Esa decisión la toma el '
         u'programa al abrirlo, con lo que tenga instalado ese ordenador concreto.')
_TXT3 = (u'De ahí sale la regla que ordena la sesión entera: lo que dice el '
         u'documento y cómo se ve son dos cosas distintas, y conviene tenerlas '
         u'separadas. Cuando se mezclan, cada ordenador dibuja una cosa.')
_PIE1 = u'Una caja de tipos: cada letra, una pieza suelta.'
_PIE2 = u'La misma frase, compuesta con otros tipos.'

_DOC_JS = (
    u"        var DOC = [\n"
    u"          {t:'h',   pt:18, txt:" + _lit(u9_metricas.TITULO) + u"},\n"
    u"          {t:'p',   pt:0,  txt:" + _lit(_TXT1) + u"},\n"
    u"          {t:'img', mm:78},\n"
    u"          {t:'pie', pt:-2, txt:" + _lit(_PIE1) + u"},\n"
    u"          {t:'p',   pt:0,  txt:" + _lit(_TXT2) + u"},\n"
    u"          {t:'img', mm:52},\n"
    u"          {t:'pie', pt:-2, txt:" + _lit(_PIE2) + u"},\n"
    u"          {t:'p',   pt:0,  txt:" + _lit(_TXT3) + u"}\n"
    u"        ];\n")


ESCENA_MAQUETA = u'''
      <div class="escena" id="esc-maqueta">
        <div class="escena-barra">
          <span class="escena-titulo">El mismo documento en dos ordenadores</span>
          <div class="seg" id="seg-maq-f">
            <button type="button" data-f="helv">Helvetica</button>
            <button type="button" data-f="times" aria-pressed="true">Times</button>
            <button type="button" data-f="cour">Courier</button>
          </div>
        </div>
        <div class="escena-barra">
          <span class="escena-titulo">Y adem&aacute;s, en ese ordenador</span>
          <div class="seg" id="seg-maq-o">
            <button type="button" data-p="a4">A4</button>
            <button type="button" data-p="carta" aria-pressed="true">Carta</button>
            <button type="button" data-c="11">11 pt</button>
            <button type="button" data-c="14" aria-pressed="true">14 pt</button>
            <button type="button" data-pdf="1">&#128196; Mandarlo en PDF</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 440" id="svg-maqueta" role="img"
               aria-label="El mismo documento maquetado en dos ordenadores distintos, con las l&iacute;neas y las hojas que salen en cada uno"></svg>
        </div>
        <div class="pie" id="pie-maqueta"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-maqueta');
        if(!svg) return;
        var pie = document.getElementById('pie-maqueta');

        ''' + u9_metricas.js_tablas() + u'''

        var PT_MM = 25.4 / 72;        /* lo que mide un punto, en mil\\u00edmetros */
        var K = 0.95;                 /* px del lienzo por mil\\u00edmetro de papel */
        var MARGEN = 25;              /* mm por los cuatro lados */

        var PAPEL = {
          a4   : {w:210,   h:297,   n:'A4'},
          carta: {w:215.9, h:279.4, n:'Carta'}
        };
        var FUENTE = {
          helv : {n:'Helvetica', w:W_helv,
                  fam:"'Nimbus Sans','Liberation Sans',Helvetica,Arial,sans-serif"},
          times: {n:'Times',     w:W_times,
                  fam:"'Nimbus Roman','Liberation Serif','Times New Roman',Times,serif"},
          cour : {n:'Courier',   w:null,
                  fam:"'Nimbus Mono PS','Liberation Mono','Courier New',Courier,monospace"}
        };

''' + _DOC_JS + u'''
        /* ---- lo que ocupa un texto, en puntos, letra a letra ---- */
        function ancho(txt, f, pt){
          var t = FUENTE[f].w, s = 0;
          for(var i = 0; i < txt.length; i++){
            var c = txt.charAt(i);
            s += t ? (t[c] !== undefined ? t[c] : 500) : 600;
          }
          return s * pt / 1000;
        }

        /* ---- corte de lineas: la linea se cierra cuando la palabra
               siguiente ya no cabe. Es lo que hace un procesador ---- */
        function corta(txt, f, pt, max){
          var pal = txt.split(' '), lin = [], act = '';
          for(var i = 0; i < pal.length; i++){
            var cand = act ? act + ' ' + pal[i] : pal[i];
            if(act && ancho(cand, f, pt) > max){ lin.push(act); act = pal[i]; }
            else act = cand;
          }
          if(act) lin.push(act);
          return lin;
        }

        /* ---- paginado ---- */
        function maqueta(cfg){
          var p = PAPEL[cfg.papel];
          var maxW = (p.w - 2*MARGEN) / PT_MM;     /* anchura util, en puntos */
          var maxH = (p.h - 2*MARGEN) / PT_MM;     /* altura util, en puntos  */
          var pags = [[]], y = 0, lineas = 0, fotos = [];

          function salta(){ pags.push([]); y = 0; }
          function pon(it){ pags[pags.length - 1].push(it); }

          for(var b = 0; b < DOC.length; b++){
            var bl = DOC[b];
            if(bl.t === 'img'){
              var h = bl.mm / PT_MM;
              if(y + h > maxH + 0.01 && y > 0) salta();
              pon({t:'img', y:y, alto:h});
              fotos.push(pags.length);
              y += h + 6;
              continue;
            }
            var pt = bl.pt > 0 ? bl.pt : cfg.pt + bl.pt;
            var inter = pt * 1.35;
            var lin = corta(bl.txt, cfg.f, pt, maxW);
            for(var i = 0; i < lin.length; i++){
              if(y + inter > maxH + 0.01) salta();
              pon({t:'lin', y:y, pt:pt, an:ancho(lin[i], cfg.f, pt), titulo:(bl.t === 'h')});
              y += inter; lineas++;
            }
            y += pt * 0.7;
          }
          return {pags:pags, lineas:lineas, hoja:p, fotos:fotos,
                  primera: corta(DOC[1].txt, cfg.f, cfg.pt, maxW)[0]};
        }

        /* ---- dibujo de la primera hoja ---- */
        function hoja(x, y, m){
          var p = m.hoja, s = '';
          s += '<rect x="'+x+'" y="'+y+'" width="'+(p.w*K).toFixed(1)+'" height="'
             + (p.h*K).toFixed(1)+'" fill="var(--surface)" stroke="var(--line)" '
             + 'stroke-width="1.5"></rect>';
          var ix = x + MARGEN*K, iy = y + MARGEN*K, iw = (p.w - 2*MARGEN)*K;
          s += '<rect x="'+ix.toFixed(1)+'" y="'+iy.toFixed(1)+'" width="'+iw.toFixed(1)
             + '" height="'+((p.h - 2*MARGEN)*K).toFixed(1)
             + '" fill="none" stroke="var(--line-soft)" stroke-width="1" '
             + 'stroke-dasharray="3 3"></rect>';
          var it = m.pags[0];
          for(var i = 0; i < it.length; i++){
            var o = it[i], oy = iy + o.y*PT_MM*K;
            if(o.t === 'img'){
              var oh = o.alto*PT_MM*K;
              s += '<rect x="'+ix.toFixed(1)+'" y="'+oy.toFixed(1)+'" width="'+iw.toFixed(1)
                 + '" height="'+oh.toFixed(1)+'" fill="var(--surface-2)" '
                 + 'stroke="var(--line)" stroke-width="1"></rect>';
              var cx = ix + iw/2, cy = oy + oh/2;
              s += '<path d="M'+(cx-17).toFixed(1)+' '+(cy+10).toFixed(1)
                 + ' l12 -14 l7 8 l5 -6 l10 12 Z" fill="var(--line)"></path>';
              s += '<circle cx="'+(cx+13).toFixed(1)+'" cy="'+(cy-9).toFixed(1)
                 + '" r="4" fill="var(--line)"></circle>';
            } else {
              var bh = Math.max(1.4, o.pt*PT_MM*K*0.56);
              s += '<rect x="'+ix.toFixed(1)+'" y="'+oy.toFixed(1)+'" width="'
                 + (o.an*PT_MM*K).toFixed(1)+'" height="'+bh.toFixed(1)+'" fill="'
                 + (o.titulo ? 'var(--goo-azul)' : 'var(--ink-soft)')+'" opacity="'
                 + (o.titulo ? '.95' : '.5')+'"></rect>';
            }
          }
          s += '<text x="'+(x + p.w*K/2).toFixed(1)+'" y="'+(y + p.h*K + 15).toFixed(1)
             + '" text-anchor="middle" class="rotulo-svg" style="font-size:10.5px">'
             + 'HOJA 1 DE ' + m.pags.length + '  \\u00b7  ' + m.lineas + ' L\\u00cdNEAS</text>';
          return s;
        }

        var A = {f:'helv', papel:'a4', pt:11};      /* donde se escribi\\u00f3 */
        var sel = {f:'times', papel:'carta', pt:14};
        var pdf = false;

        function escapa(s){
          return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
        }

        function pinta(){
          var B = pdf ? A : sel;
          var mA = maqueta(A), mB = maqueta(B);
          var s = '';

          s += '<text x="140" y="20" text-anchor="middle" class="rotulo-svg" '
             + 'style="font-size:11.5px;fill:var(--goo-azul);font-weight:500">'
             + 'DONDE LO ESCRIBISTE</text>';
          s += '<text x="140" y="38" text-anchor="middle" class="rotulo-svg" '
             + 'style="font-size:10px">Helvetica 11 pt  \\u00b7  A4</text>';
          s += '<text x="462" y="20" text-anchor="middle" class="rotulo-svg" '
             + 'style="font-size:11.5px;font-weight:500;fill:'
             + (pdf ? 'var(--goo-verde)' : 'var(--goo-rojo)')+'">'
             + (pdf ? 'EL ORDENADOR DEL AULA, CON EL PDF' : 'EL ORDENADOR DEL AULA')+'</text>';
          s += '<text x="462" y="38" text-anchor="middle" class="rotulo-svg" '
             + 'style="font-size:10px">' + FUENTE[B.f].n + ' ' + B.pt + ' pt  \\u00b7  '
             + PAPEL[B.papel].n + '</text>';

          s += hoja(40, 52, mA);
          s += hoja(360, 52, mB);

          if(pdf){
            s += '<rect x="424" y="60" width="76" height="24" fill="var(--goo-verde)" '
               + 'opacity=".92"></rect>';
            s += '<text x="462" y="77" text-anchor="middle" '
               + 'style="font-family:var(--f-m);font-size:12px;fill:#fff;font-weight:500">'
               + 'PDF</text>';
          }

          s += '<text x="20" y="366" class="rotulo-svg" style="font-size:10px">'
             + 'LA PRIMERA L\\u00cdNEA DEL PRIMER P\\u00c1RRAFO, DE CERCA: MIRA D\\u00d3NDE CORTA'
             + '</text>';
          var filas = [[A, mA, 'var(--goo-azul)', 392],
                       [B, mB, pdf ? 'var(--goo-verde)' : 'var(--goo-rojo)', 424]];
          for(var q = 0; q < filas.length; q++){
            var cfg = filas[q][0], m = filas[q][1], col = filas[q][2], fy = filas[q][3];
            s += '<rect x="20" y="'+(fy-17)+'" width="600" height="24" fill="var(--surface-2)">'
               + '</rect>';
            s += '<rect x="20" y="'+(fy-17)+'" width="3" height="24" fill="'+col+'"></rect>';
            s += '<text x="30" y="'+fy+'" style="font-family:'+FUENTE[cfg.f].fam
               + ';font-size:13px;fill:var(--ink)">' + escapa(m.primera) + '</text>';
          }

          svg.innerHTML = s;

          var na = mA.pags.length, nb = mB.pags.length;
          var t = 'A la izquierda, <b>'+mA.lineas+' l&iacute;neas</b> en <b>'+na
                + (na === 1 ? ' hoja' : ' hojas')+'</b>. A la derecha, <b>'+mB.lineas
                + ' l&iacute;neas</b> en <b>'+nb+(nb === 1 ? ' hoja' : ' hojas')+'</b>. ';
          if(pdf){
            t += 'En PDF <b>no queda nada por decidir</b>: el fichero lleva dentro la letra y '
               + 'la posici&oacute;n exacta de cada cosa, as&iacute; que los botones de arriba ya '
               + 'no lo mueven. Por eso se manda en PDF lo que tiene que verse igual en todas '
               + 'partes &mdash;y por eso luego cuesta tanto editarlo.';
          } else if(mA.lineas === mB.lineas && na === nb){
            t += 'Aqu&iacute; coinciden por poco. Ponle <b>Courier</b> y vuelve a mirar.';
          } else {
            t += 'Es el <b>mismo texto</b>, letra por letra: no se ha estropeado nada ni se ha '
               + 'perdido nada. Lo que ha cambiado es <b>con qu&eacute; se dibuja</b>, y el '
               + 'documento se ha repartido solo otra vez. ';
            t += (mA.fotos[1] !== mB.fotos[1])
              ? 'Y ah&iacute; est&aacute; la queja de siempre: la <b>segunda foto</b> estaba en la '
                + 'hoja ' + mA.fotos[1] + ' y ahora se ha ido a la <b>hoja ' + mB.fotos[1]
                + '</b>. Nadie la ha movido.'
              : 'Las dos fotos siguen cayendo en la misma hoja que antes; cambia algo m&aacute;s '
                + 'y mira qu&eacute; pasa con la segunda.';
          }
          t += '<br><span style="font-size:12.5px">Las anchuras de cada letra son las de verdad, '
             + 'las que publica Adobe para esas tres tipograf&iacute;as. El corte de l&iacute;nea '
             + 'se hace aqu&iacute;, palabra a palabra, igual que en un procesador de textos.'
             + '</span>';
          pie.innerHTML = t;
        }

        function marca(caja, attr, valor){
          caja.querySelectorAll('button['+attr+']').forEach(function(b){
            b.setAttribute('aria-pressed',
              b.getAttribute(attr) === String(valor) ? 'true' : 'false');
          });
        }

        var cajaF = document.getElementById('seg-maq-f');
        var cajaO = document.getElementById('seg-maq-o');
        cajaF.addEventListener('click', function(e){
          var b = e.target.closest('button[data-f]'); if(!b) return;
          sel.f = b.dataset.f; pdf = false;
          marca(cajaF, 'data-f', sel.f); marca(cajaO, 'data-pdf', 'x'); pinta();
        });
        cajaO.addEventListener('click', function(e){
          var b = e.target.closest('button'); if(!b) return;
          if(b.dataset.p){ sel.papel = b.dataset.p; pdf = false; marca(cajaO, 'data-p', sel.papel); }
          else if(b.dataset.c){ sel.pt = +b.dataset.c; pdf = false; marca(cajaO, 'data-c', sel.pt); }
          else if(b.dataset.pdf){ pdf = !pdf; }
          else return;
          marca(cajaO, 'data-pdf', pdf ? '1' : 'x');
          pinta();
        });

        pinta();
      })();
      </script>
'''


# ===========================================================================
# S1 · El indice que se hace solo
#
# Lienzo 640 x 430.
#   Rotulos de columna y 22 · filas del documento desde y = 44
#     un titulo ocupa 20 px y un parrafo 13; con los 18 bloques del caso peor
#     (despues de meter uno) son 297 px y acaban en y = 341.
#   Columna izquierda (el documento)  x  16..322
#   Columna derecha  (el indice)      x 338..624, caja y 34..342
#   Los dos contadores, abajo: y 356..416
#
# Los numeros de pagina NO estan escritos: se paginan los bloques contando
# lineas equivalentes (un titulo grande ocupa tres, uno pequeno dos) con
# LINEAS_HOJA lineas por hoja. Los retoques a mano tambien se cuentan: uno por
# cada bloque del documento, porque a mano hay que ir bloque por bloque.
# ===========================================================================
ESCENA_ESTILOS = u'''
      <div class="escena" id="esc-estilos">
        <div class="escena-barra">
          <span class="escena-titulo">Lo mismo, de dos maneras</span>
          <div class="seg" id="seg-est-m">
            <button type="button" data-m="mano" aria-pressed="true">Formato a mano</button>
            <button type="button" data-m="estilos">Con estilos</button>
          </div>
        </div>
        <div class="escena-barra">
          <span class="escena-titulo">Y ahora te piden esto</span>
          <div class="seg" id="seg-est-a">
            <button type="button" data-a="indice">&#9776; Generar el &iacute;ndice</button>
            <button type="button" data-a="aspecto">&#9998; Cambiar el aspecto</button>
            <button type="button" data-a="mete">&#10133; Meter un apartado al principio</button>
            <button type="button" data-a="reset">&#8635; Reiniciar</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 430" id="svg-estilos" role="img"
               aria-label="Un documento con sus apartados y el &iacute;ndice que se genera a partir de ellos"></svg>
        </div>
        <div class="pie" id="pie-estilos"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-estilos');
        if(!svg) return;
        var pie = document.getElementById('pie-estilos');

        var LINEAS_HOJA = 34;      /* lineas que caben en una hoja */
        var PESO = {h1:3, h2:2};   /* lo que ocupa un titulo, en lineas */

        function documento(){
          return [
            {n:'h1', t:'\\u00bfQu\\u00e9 es un formato?'},
            {n:'p',  l:7},
            {n:'h2', t:'Texto plano y texto con marcas'},
            {n:'p',  l:9},
            {n:'h2', t:'Por qu\\u00e9 el PDF se ve igual'},
            {n:'p',  l:8},
            {n:'h1', t:'Las im\\u00e1genes'},
            {n:'p',  l:6},
            {n:'h2', t:'Mapa de bits'},
            {n:'p',  l:11},
            {n:'h2', t:'Vectorial'},
            {n:'p',  l:7},
            {n:'h1', t:'Presentar'},
            {n:'p',  l:9},
            {n:'h2', t:'Una idea por diapositiva'},
            {n:'p',  l:8}
          ];
        }

        var doc = documento();
        var modo = 'mano', indice = null, aviso = '', metido = false;

        /* ---- paginado: en que hoja cae cada apartado ---- */
        function pagina(){
          var acc = 0, r = [];
          for(var i = 0; i < doc.length; i++){
            var b = doc[i];
            var alto = (b.n === 'p') ? b.l : PESO[b.n];
            /* un titulo no se queda solo al final de la hoja */
            if(b.n !== 'p' && (acc % LINEAS_HOJA) + alto + 2 > LINEAS_HOJA){
              acc += LINEAS_HOJA - (acc % LINEAS_HOJA);
            }
            if(b.n !== 'p') r.push({n:b.n, t:b.t, pag: Math.floor(acc / LINEAS_HOJA) + 1});
            acc += alto;
          }
          return r;
        }

        /* ---- retoques para cambiar el aspecto de todo el documento ---- */
        function retoques(){
          if(modo === 'estilos') return 2;    /* el estilo T\\u00edtulo y el estilo Normal */
          return doc.length;                  /* a mano, bloque por bloque */
        }
        function titulos(){
          return doc.filter(function(b){ return b.n !== 'p'; }).length;
        }

        function texto(x, y, t, op){
          op = op || {};
          return '<text x="'+x+'" y="'+y+'" class="rotulo-svg" style="font-size:'
               + (op.s || 11)+'px'+(op.c ? ';fill:'+op.c : '')
               + (op.p ? ';font-weight:500' : '')
               + (op.a ? ';text-anchor:'+op.a : '')+'">'+t+'</text>';
        }

        function pinta(){
          var s = '', estilos = (modo === 'estilos');
          var col = estilos ? 'var(--goo-verde)' : 'var(--goo-rojo)';

          s += texto(16, 22, 'EL DOCUMENTO  \\u00b7  ' + (estilos
                ? 'MARCADO CON ESTILOS' : 'PINTADO A MANO'), {s:10.5, p:1, c:col});
          s += texto(338, 22, 'EL \\u00cdNDICE QUE SALE', {s:10.5, p:1});

          /* Filas: un titulo ocupa 20 px y un parrafo 13. Con los 18 bloques
             que hay despues de meter uno nuevo salen 9*20 + 9*13 = 297 px, y
             desde y = 44 llegan justo a 341, el borde de la caja del indice. */
          var y = 44;
          for(var i = 0; i < doc.length; i++){
            var b = doc[i];
            if(b.n === 'p'){
              for(var k = 0; k < 2; k++){
                s += '<rect x="34" y="'+(y + 3 + k*5)+'" width="'+(232 - k*54)
                   + '" height="3" fill="var(--ink-soft)" opacity=".30"></rect>';
              }
              s += texto(322, y + 10, b.l + ' l\\u00edn.', {s:9, a:'end'});
              y += 13;
              continue;
            }
            var grande = (b.n === 'h1');
            s += '<rect x="16" y="'+(y + 2)+'" width="6" height="15" fill="'+col+'"></rect>';
            s += texto(30, y + 14, b.t, {s: grande ? 11.5 : 10.5, p:1});
            s += texto(322, y + 14, estilos
                 ? (grande ? 'T\\u00edtulo 1' : 'T\\u00edtulo 2')
                 : 'Normal', {s:9.5, a:'end', c: estilos ? col : 'var(--ink-soft)'});
            y += 20;
          }

          s += '<rect x="338" y="34" width="286" height="308" fill="var(--surface)" '
             + 'stroke="var(--line)" stroke-width="1.5"></rect>';
          if(!indice){
            s += texto(481, 182, 'Pulsa \\u00abGenerar el \\u00edndice\\u00bb',
                       {s:11, a:'middle'});
          } else if(indice.length === 0){
            s += texto(481, 160, 'El programa no encuentra', {s:11.5, a:'middle',
                 c:'var(--goo-rojo)', p:1});
            s += texto(481, 178, 'ning\\u00fan t\\u00edtulo.', {s:11.5, a:'middle',
                 c:'var(--goo-rojo)', p:1});
            s += texto(481, 204, 'Para \\u00e9l todo eso es texto normal', {s:10, a:'middle'});
            s += texto(481, 220, 'que resulta que est\\u00e1 en negrita.', {s:10, a:'middle'});
          } else {
            var iy = 58;
            if(indice[0].mano){
              s += texto(352, 50, 'ESCRITO A MANO POR TI, CON LOS N\\u00daMEROS DE ANTES',
                         {s:9, c:'var(--goo-rojo)'});
              iy = 74;
            }
            for(var j = 0; j < indice.length; j++){
              var e = indice[j];
              var mal = (e.viejo !== undefined && e.viejo !== e.pag);
              var ex = (e.n === 'h1') ? 352 : 368;
              s += texto(ex, iy, e.t, {s: e.n === 'h1' ? 11.5 : 10.5, p: e.n === 'h1' ? 1 : 0});
              s += '<path d="M'+ex+' '+(iy+3)+' H594" stroke="var(--line-soft)" '
                 + 'stroke-width="1" stroke-dasharray="1.5 2.5"></path>';
              s += texto(610, iy, String(e.viejo !== undefined ? e.viejo : e.pag),
                         {s:11.5, a:'end', p:1, c: mal ? 'var(--goo-rojo)' : 'var(--ink)'});
              iy += 19;
            }
          }

          s += '<rect x="16" y="356" width="608" height="60" fill="var(--surface-2)"></rect>';
          s += texto(30, 377, 'CAMBIAR EL ASPECTO DE TODO EL DOCUMENTO CUESTA', {s:9.5});
          s += texto(30, 402, retoques() + (retoques() === 1 ? ' retoque' : ' retoques'),
                     {s:17, p:1, c:col});
          s += texto(340, 377, 'APARTADOS QUE EL PROGRAMA RECONOCE COMO T\\u00cdTULOS', {s:9.5});
          s += texto(340, 402, (estilos ? titulos() : 0) + ' de ' + titulos(),
                     {s:17, p:1, c:col});

          svg.innerHTML = s;
          pie.innerHTML = aviso || ('Los n&uacute;meros de p&aacute;gina no est&aacute;n escritos '
            + 'en ning&uacute;n sitio: se cuentan aqu&iacute; mismo, sumando las l&iacute;neas de '
            + 'cada apartado a raz&oacute;n de <b>' + LINEAS_HOJA + ' l&iacute;neas por hoja</b>. '
            + 'Prueba a generar el &iacute;ndice en los dos modos.');
        }

        function accion(a){
          if(a === 'indice'){
            indice = (modo === 'estilos') ? pagina() : [];
            aviso = (modo === 'estilos')
              ? 'El programa <b>s&iacute; sabe</b> cu&aacute;les son los t&iacute;tulos, porque se '
                + 'lo dijiste al marcarlos con un estilo. Con esa marca hace la lista y le pone al '
                + 'lado la hoja en la que cae cada uno.'
              : 'Nada, y no es un fallo del programa. <b>Nunca le has dicho</b> cu&aacute;les de '
                + 'esas l&iacute;neas son t&iacute;tulos: poner algo en negrita y m&aacute;s grande '
                + 'lo cambia de <b>aspecto</b>, no de <b>papel</b>.';
          } else if(a === 'aspecto'){
            aviso = (modo === 'estilos')
              ? '<b>Dos retoques</b>: cambias el estilo <i>T&iacute;tulo</i> y el estilo '
                + '<i>Normal</i>, y se mueve el documento entero, tenga las p&aacute;ginas que '
                + 'tenga.'
              : '<b>' + retoques() + ' retoques</b>, uno por bloque. Y en un trabajo de verdad, de '
                + 'treinta p&aacute;ginas, son cientos. Ah&iacute; es donde se queda siempre '
                + 'alg&uacute;n t&iacute;tulo distinto de los dem&aacute;s.';
          } else if(a === 'mete'){
            if(metido){
              aviso = 'Ya lo has metido. Pulsa <b>Reiniciar</b> si quieres empezar otra vez.';
            } else {
              var antes = pagina();          /* los numeros de antes de tocar nada */
              doc.unshift({n:'h1', t:'Introducci\\u00f3n'}, {n:'p', l:12});
              metido = true;
              var nuevo = pagina();
              if(modo === 'estilos'){
                indice = nuevo;
                aviso = 'Pulsas <b>actualizar</b> y ya est&aacute;: el &iacute;ndice se rehace '
                      + 'solo, entra el apartado nuevo y todos los n&uacute;meros salen bien.';
              } else {
                /* A mano el indice lo habrias escrito tu, con los numeros de
                   antes. Ahora se comparan con los que tocan de verdad. */
                indice = antes.map(function(e, i){
                  return {n:e.n, t:e.t, pag:nuevo[i + 1].pag, viejo:e.pag, mano:1};
                });
                var fallan = indice.filter(function(e){ return e.viejo !== e.pag; }).length;
                aviso = 'Este es el &iacute;ndice que habr&iacute;as escrito t&uacute;, con los '
                      + 'n&uacute;meros de antes. Al meter un apartado al principio, <b>' + fallan
                      + ' n&uacute;meros</b> han dejado de valer (van en rojo) y falta la entrada '
                      + 'nueva. Hay que arreglarlo <b>a mano, uno a uno</b>, y cada vez que el '
                      + 'documento crezca.';
              }
            }
          } else {
            doc = documento(); indice = null; aviso = ''; metido = false;
          }
          pinta();
        }

        var cajaM = document.getElementById('seg-est-m');
        cajaM.addEventListener('click', function(e){
          var b = e.target.closest('button[data-m]'); if(!b) return;
          modo = b.dataset.m;
          doc = documento(); indice = null; aviso = ''; metido = false;
          cajaM.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          pinta();
        });
        document.getElementById('seg-est-a').addEventListener('click', function(e){
          var b = e.target.closest('button[data-a]'); if(!b) return;
          accion(b.dataset.a);
        });

        pinta();
      })();
      </script>
'''


# ===========================================================================
# S2 · El mismo dibujo, en casillas y en instrucciones
#
# Lienzo 640 x 352.
#   Rotulos y 24 y 40 · dos ventanas cuadradas de 240 px desde y = 52
#     izquierda x  26..266  ·  derecha x 374..614
#   Pie de cada ventana y 312 y 330.
#
# La figura es un anillo mas un triangulo, definida en coordenadas de 0 a 1.
# El anillo va de r = 0,32 a r = 0,44 desde el centro, y el triangulo entero
# cabe dentro del circulo interior (su vertice mas lejano esta a 0,242 del
# centro): por eso la regla par-impar del <path> deja el hueco entre los dos
# y no se come el triangulo.
# El mapa de bits se calcula aqui: cada casilla mide su cobertura con 4x4
# muestras, asi que los bordes salen grises de verdad. Al ampliar se ve la
# misma casilla mas grande, que es exactamente lo que hace un visor.
# El peso del vectorial es la longitud REAL de la cadena del <path>.
# ===========================================================================
ESCENA_MAPA = u'''
      <div class="escena" id="esc-mapa">
        <div class="escena-barra">
          <span class="escena-titulo">Casillas o instrucciones</span>
          <div class="seg" id="seg-mapa-n">
            <button type="button" data-n="10">10 &times; 10</button>
            <button type="button" data-n="20" aria-pressed="true">20 &times; 20</button>
            <button type="button" data-n="40">40 &times; 40</button>
          </div>
        </div>
        <div class="escena-barra">
          <span class="escena-titulo">Acercarse</span>
          <div class="seg" id="seg-mapa-z">
            <button type="button" data-z="1" aria-pressed="true">&times;1</button>
            <button type="button" data-z="4">&times;4</button>
            <button type="button" data-z="10">&times;10</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 352" id="svg-mapa" role="img"
               aria-label="El mismo s&iacute;mbolo guardado como rejilla de casillas y como instrucciones de dibujo, ampliados a la vez"></svg>
        </div>
        <div class="pie" id="pie-mapa"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-mapa');
        if(!svg) return;
        var pie = document.getElementById('pie-mapa');

        var VENT = 240;                 /* lado de cada ventana, en px */
        var X1 = 26, X2 = 374, Y0 = 52;
        var N = 20, Z = 1;

        /* ---- la figura, en coordenadas de 0 a 1 ---- */
        var CX = 0.5, CY = 0.5, R_OUT = 0.44, R_IN = 0.32;
        var TRI = [[0.40, 0.28], [0.40, 0.72], [0.74, 0.50]];

        function sig(x, y, p, q){
          return (x - q[0])*(p[1] - q[1]) - (p[0] - q[0])*(y - q[1]);
        }
        function enTriangulo(x, y){
          var d1 = sig(x, y, TRI[0], TRI[1]);
          var d2 = sig(x, y, TRI[1], TRI[2]);
          var d3 = sig(x, y, TRI[2], TRI[0]);
          var neg = (d1 < 0) || (d2 < 0) || (d3 < 0);
          var pos = (d1 > 0) || (d2 > 0) || (d3 > 0);
          return !(neg && pos);
        }
        function dentro(x, y){
          var dx = x - CX, dy = y - CY, d = Math.sqrt(dx*dx + dy*dy);
          if(d <= R_OUT && d >= R_IN) return true;
          return enTriangulo(x, y);
        }

        /* ---- rasterizar: cobertura de cada casilla con 4x4 muestras ---- */
        function rasteriza(n){
          var m = [], sub = 4;
          for(var j = 0; j < n; j++){
            var fila = [];
            for(var i = 0; i < n; i++){
              var c = 0;
              for(var sj = 0; sj < sub; sj++){
                for(var si = 0; si < sub; si++){
                  if(dentro((i + (si + 0.5)/sub) / n, (j + (sj + 0.5)/sub) / n)) c++;
                }
              }
              fila.push(c / (sub*sub));
            }
            m.push(fila);
          }
          return m;
        }

        /* ---- el vectorial: la cadena que se guardaria de verdad ---- */
        function cadena(){
          function f(v){ return (v*100).toFixed(1); }
          return 'M' + f(CX - R_OUT) + ' ' + f(CY)
               + 'a' + f(R_OUT) + ' ' + f(R_OUT) + ' 0 1 0 ' + f(2*R_OUT) + ' 0'
               + 'a' + f(R_OUT) + ' ' + f(R_OUT) + ' 0 1 0 ' + f(-2*R_OUT) + ' 0'
               + 'M' + f(CX - R_IN) + ' ' + f(CY)
               + 'a' + f(R_IN) + ' ' + f(R_IN) + ' 0 1 0 ' + f(2*R_IN) + ' 0'
               + 'a' + f(R_IN) + ' ' + f(R_IN) + ' 0 1 0 ' + f(-2*R_IN) + ' 0'
               + 'M' + f(TRI[0][0]) + ' ' + f(TRI[0][1])
               + 'L' + f(TRI[1][0]) + ' ' + f(TRI[1][1])
               + 'L' + f(TRI[2][0]) + ' ' + f(TRI[2][1]) + 'Z';
        }

        function bytes(n){
          if(n < 1024) return n + ' B';
          if(n < 1048576) return (n/1024).toFixed(1).replace('.', ',') + ' KiB';
          return (n/1048576).toFixed(2).replace('.', ',') + ' MiB';
        }

        function pinta(){
          var m = rasteriza(N), s = '';
          var lado = VENT * Z;                 /* lo que ocupa la figura al ampliar */
          var off = (lado - VENT) / 2;         /* lo que se sale por cada lado      */
          var paso = lado / N;

          s += '<clipPath id="cl-bit"><rect x="'+X1+'" y="'+Y0+'" width="'+VENT
             + '" height="'+VENT+'"/></clipPath>';
          s += '<clipPath id="cl-vec"><rect x="'+X2+'" y="'+Y0+'" width="'+VENT
             + '" height="'+VENT+'"/></clipPath>';

          s += '<text x="'+(X1 + VENT/2)+'" y="24" text-anchor="middle" class="rotulo-svg" '
             + 'style="font-size:11.5px;fill:var(--goo-rojo);font-weight:500">'
             + 'MAPA DE BITS  \\u00b7  ' + N + ' \\u00d7 ' + N + ' CASILLAS</text>';
          s += '<text x="'+(X2 + VENT/2)+'" y="24" text-anchor="middle" class="rotulo-svg" '
             + 'style="font-size:11.5px;fill:var(--goo-verde);font-weight:500">'
             + 'VECTORIAL  \\u00b7  TRES INSTRUCCIONES</text>';
          s += '<text x="'+(X1 + VENT/2)+'" y="40" text-anchor="middle" class="rotulo-svg" '
             + 'style="font-size:10px">guarda el color de cada casilla</text>';
          s += '<text x="'+(X2 + VENT/2)+'" y="40" text-anchor="middle" class="rotulo-svg" '
             + 'style="font-size:10px">guarda c\\u00f3mo se dibuja</text>';

          s += '<g clip-path="url(#cl-bit)">';
          var i0 = Math.max(0, Math.floor(off / paso));
          var i1 = Math.min(N, Math.ceil((off + VENT) / paso));
          for(var j = i0; j < i1; j++){
            for(var i = i0; i < i1; i++){
              var a = m[j][i];
              if(a <= 0.001) continue;
              s += '<rect x="'+(X1 - off + i*paso).toFixed(2)+'" y="'
                 + (Y0 - off + j*paso).toFixed(2)+'" width="'+(paso + 0.4).toFixed(2)
                 + '" height="'+(paso + 0.4).toFixed(2)+'" fill="var(--ink)" opacity="'
                 + a.toFixed(3)+'"></rect>';
            }
          }
          if(paso > 9){       /* con las casillas gordas se ve la rejilla */
            for(var g = i0; g <= i1; g++){
              s += '<path d="M'+(X1 - off + g*paso).toFixed(2)+' '+Y0+' v'+VENT
                 + '" stroke="var(--goo-rojo)" stroke-width=".5" opacity=".38"></path>';
              s += '<path d="M'+X1+' '+(Y0 - off + g*paso).toFixed(2)+' h'+VENT
                 + '" stroke="var(--goo-rojo)" stroke-width=".5" opacity=".38"></path>';
            }
          }
          s += '</g>';
          s += '<rect x="'+X1+'" y="'+Y0+'" width="'+VENT+'" height="'+VENT
             + '" fill="none" stroke="var(--line)" stroke-width="1.5"></rect>';

          s += '<g clip-path="url(#cl-vec)"><g transform="translate('+(X2 - off).toFixed(2)
             + ' '+(Y0 - off).toFixed(2)+') scale('+(lado/100).toFixed(4)+')">';
          s += '<path d="'+cadena()+'" fill="var(--ink)" fill-rule="evenodd"></path>';
          s += '</g></g>';
          s += '<rect x="'+X2+'" y="'+Y0+'" width="'+VENT+'" height="'+VENT
             + '" fill="none" stroke="var(--line)" stroke-width="1.5"></rect>';

          var pesoBit = N*N*3, pesoVec = cadena().length;
          s += '<text x="'+(X1 + VENT/2)+'" y="312" text-anchor="middle" class="rotulo-svg" '
             + 'style="font-size:12px;fill:var(--ink)">' + (N*N)
             + ' casillas \\u00d7 3 bytes = ' + bytes(pesoBit) + '</text>';
          s += '<text x="'+(X2 + VENT/2)+'" y="312" text-anchor="middle" class="rotulo-svg" '
             + 'style="font-size:12px;fill:var(--ink)">' + pesoVec + ' letras, o sea '
             + bytes(pesoVec) + '</text>';
          s += '<text x="'+(X1 + VENT/2)+'" y="330" text-anchor="middle" class="rotulo-svg" '
             + 'style="font-size:10px">al ampliar, la casilla se hace grande</text>';
          s += '<text x="'+(X2 + VENT/2)+'" y="330" text-anchor="middle" class="rotulo-svg" '
             + 'style="font-size:10px">al ampliar, se vuelve a dibujar</text>';

          svg.innerHTML = s;

          pie.innerHTML = 'A la izquierda hay <b>' + (N*N) + ' casillas</b> y en cada una cabe un '
            + 'color: eso es <b>todo</b> lo que se guarda, y por eso al acercarse no aparece '
            + 'detalle nuevo. No lo hay. A la derecha se guardan tres instrucciones '
            + '&mdash;<span style="font-family:var(--f-m);font-size:11.5px">'
            + cadena().slice(0, 42) + '&hellip;</span>&mdash;, <b>' + pesoVec + ' bytes</b>, y el '
            + 'dibujo se rehace entero cada vez que cambia de tama&ntilde;o.'
            + '<br><span style="font-size:12.5px">La cuenta que hay que ver: para que el mapa de '
            + 'bits se viera igual de fino <b>al doble de tama&ntilde;o</b> har&iacute;an falta '
            + (2*N) + ' &times; ' + (2*N) + ' = <b>' + (4*N*N) + ' casillas</b>, o sea '
            + bytes(4*N*N*3) + '. Al doble de ancho, <b>cuatro veces</b> el peso. El vectorial '
            + 'sigue pesando ' + pesoVec + ' bytes.</span>';
        }

        function conecta(id, attr, fn){
          var caja = document.getElementById(id);
          caja.addEventListener('click', function(e){
            var b = e.target.closest('button['+attr+']'); if(!b) return;
            fn(+b.getAttribute(attr));
            caja.querySelectorAll('button').forEach(function(x){
              x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
            });
            pinta();
          });
        }
        conecta('seg-mapa-n', 'data-n', function(v){ N = v; });
        conecta('seg-mapa-z', 'data-z', function(v){ Z = v; });
        pinta();
      })();
      </script>
'''


# ===========================================================================
# S2 · Lo que pesa y lo que se ve
#
# Lienzo 640 x 330.
#   Izquierda: los dos rectangulos de pixeles, encajados por la esquina de
#              arriba a la izquierda, dentro de un hueco de 262 x 210 px
#              (x 22..284, y 58..268). Rotulos y 34, 48; pie y 296 y 310.
#   Derecha:   cifras y dos barras de peso, x 320..620.
#
# Todo son cuentas exactas: pixeles, bytes en bruto a 3 por pixel, la escala
# que cabe en el destino y el ancho impreso a 300 ppp. La compresion NO se
# estima aqui, porque depende de la foto; eso se mide aparte y se dice.
# ===========================================================================
ESCENA_PESO = u'''
      <div class="escena" id="esc-peso">
        <div class="escena-barra">
          <span class="escena-titulo">La foto que metes</span>
          <div class="seg" id="seg-peso-f">
            <button type="button" data-f="0" aria-pressed="true">M&oacute;vil 12 Mp</button>
            <button type="button" data-f="1">M&oacute;vil 48 Mp</button>
            <button type="button" data-f="2">C&aacute;mara 24 Mp</button>
            <button type="button" data-f="3">Captura de pantalla</button>
          </div>
        </div>
        <div class="escena-barra">
          <span class="escena-titulo">D&oacute;nde va a verse</span>
          <div class="seg" id="seg-peso-d">
            <button type="button" data-d="0" aria-pressed="true">Diapositiva proyectada</button>
            <button type="button" data-d="1">Impresa en A4</button>
            <button type="button" data-d="2">Miniatura en una web</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 330" id="svg-peso" role="img"
               aria-label="Los p&iacute;xeles de una foto comparados con los que caben en su destino, y lo que pesa cada cosa"></svg>
        </div>
        <div class="pie" id="pie-peso"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-peso');
        if(!svg) return;
        var pie = document.getElementById('pie-peso');

        var FOTOS = [
          {n:'M\\u00f3vil 12 Mp',       w:4032, h:3024},
          {n:'M\\u00f3vil 48 Mp',       w:8064, h:6048},
          {n:'C\\u00e1mara 24 Mp',      w:6000, h:4000},
          {n:'Captura de pantalla', w:1920, h:1080}
        ];
        var DESTINOS = [
          {n:'una diapositiva proyectada', w:1920, h:1080},
          {n:'una p\\u00e1gina A4 impresa',    w:2480, h:3508},
          {n:'una miniatura en una web',   w:400,  h:300}
        ];
        var f = 0, d = 0;

        function bytes(n){
          if(n < 1024) return n + ' B';
          if(n < 1048576) return (n/1024).toFixed(1).replace('.', ',') + ' KiB';
          if(n < 1073741824) return (n/1048576).toFixed(1).replace('.', ',') + ' MiB';
          return (n/1073741824).toFixed(2).replace('.', ',') + ' GiB';
        }
        function mil(n){
          return String(Math.round(n)).replace(/\\B(?=(\\d{3})+(?!\\d))/g, '.');
        }
        function num(v, n){ return v.toFixed(n === undefined ? 1 : n).replace('.', ','); }
        function texto(x, y, t, op){
          op = op || {};
          return '<text x="'+x+'" y="'+y+'" class="rotulo-svg" style="font-size:'+(op.s || 11)
               + 'px'+(op.c ? ';fill:'+op.c : '')+(op.p ? ';font-weight:500' : '')
               + (op.a ? ';text-anchor:'+op.a : '')+'">'+t+'</text>';
        }

        function pinta(){
          var F = FOTOS[f], D = DESTINOS[d];
          var esc = Math.min(D.w / F.w, D.h / F.h);   /* lo que cabe sin deformar */
          var cabe = Math.min(1, esc);
          var uw = Math.round(F.w * cabe), uh = Math.round(F.h * cabe);
          var pxF = F.w * F.h, pxU = uw * uh;
          var sobran = (1 - pxU / pxF) * 100;
          var peso = pxF * 3, pesoU = pxU * 3;

          var k = Math.min(262 / F.w, 210 / F.h);     /* px de lienzo por p\\u00edxel */
          var s = '';
          s += texto(22, 34, 'LOS P\\u00cdXELES QUE LLEVA LA FOTO', {s:10, p:1});
          s += texto(22, 48, F.w + ' \\u00d7 ' + F.h + ' = ' + mil(pxF) + ' p\\u00edxeles',
                     {s:10.5});
          s += '<rect x="22" y="58" width="'+(F.w*k).toFixed(1)+'" height="'+(F.h*k).toFixed(1)
             + '" fill="var(--goo-rojo)" opacity=".16" stroke="var(--goo-rojo)" '
             + 'stroke-width="1.5"></rect>';
          s += '<rect x="22" y="58" width="'+(uw*k).toFixed(1)+'" height="'+(uh*k).toFixed(1)
             + '" fill="var(--goo-verde)" opacity=".34" stroke="var(--goo-verde)" '
             + 'stroke-width="1.5"></rect>';
          s += texto(22, 296, 'En verde, lo que de verdad llega a verse.', {s:10});
          s += texto(22, 310, 'En rojo, lo que viaja dentro del fichero.', {s:10});

          var X = 320, y = 34;
          s += texto(X, y, 'PARA ' + D.n.toUpperCase() + ' CABEN', {s:10, p:1}); y += 18;
          s += texto(X, y, uw + ' \\u00d7 ' + uh + ' = ' + mil(pxU) + ' p\\u00edxeles',
                     {s:13, c:'var(--goo-verde)', p:1}); y += 26;
          s += texto(X, y, 'O SEA QUE SOBRAN', {s:10, p:1}); y += 18;
          s += texto(X, y, esc > 1 ? 'nada: la foto se queda corta'
                : (sobran < 0.05 ? 'ninguno: encaja justo'
                   : num(sobran) + ' % de los p\\u00edxeles'),
                {s:13, p:1, c: sobran > 50 ? 'var(--goo-rojo)' : 'var(--ink)'});
          y += 30;

          s += texto(X, y, 'PESO EN BRUTO, A 3 BYTES POR P\\u00cdXEL', {s:10, p:1}); y += 12;
          s += '<rect x="'+X+'" y="'+y+'" width="300" height="20" fill="var(--goo-rojo)" '
             + 'opacity=".55"></rect>';
          s += texto(X + 8, y + 14, bytes(peso) + '  \\u00b7  la foto entera', {s:11});
          y += 26;
          s += '<rect x="'+X+'" y="'+y+'" width="'+Math.max(2, 300*pesoU/peso).toFixed(1)
             + '" height="20" fill="var(--goo-verde)" opacity=".55"></rect>';
          s += texto(X + 8, y + 14, bytes(pesoU) + '  \\u00b7  lo que se ve', {s:11});
          y += 36;
          s += texto(X, y, 'IMPRESA A 300 PUNTOS POR PULGADA MEDIR\\u00cdA', {s:10, p:1}); y += 18;
          s += texto(X, y, num(F.w / 300 * 2.54) + ' cm de ancho', {s:12.5, p:1});

          svg.innerHTML = s;

          var t = 'Una foto no tiene tama&ntilde;o: tiene <b>p&iacute;xeles</b>. ';
          if(esc > 1){
            t += 'Aqu&iacute; la foto <b>se queda corta</b> para ese destino. No sobran '
               + 'p&iacute;xeles: faltan, y al estirarla se ver&aacute; blanda.';
          } else if(sobran < 0.05){
            t += 'Aqu&iacute; encaja justo: ni sobra ni falta un p&iacute;xel.';
          } else {
            t += 'De los <b>' + mil(pxF) + '</b> p&iacute;xeles que llevas, ah&iacute; solo se '
               + 'pueden ense&ntilde;ar <b>' + mil(pxU) + '</b>. Los otros <b>' + mil(pxF - pxU)
               + '</b> viajan en el fichero, ocupan sitio, tardan en abrirse&hellip; y '
               + '<b>no los ve nadie</b>.';
          }
          t += '<br><span style="font-size:12.5px">El peso en bruto es exacto: un p&iacute;xel de '
             + 'color son 3 bytes &mdash;uno de rojo, uno de verde y uno de azul&mdash;, as&iacute; '
             + 'que basta multiplicar. Lo que el fichero pesa <i>de verdad</i> es menos, porque va '
             + 'comprimido, y cu&aacute;nto menos depende de la foto: eso se mide, no se '
             + 'calcula.</span>';
          pie.innerHTML = t;
        }

        function conecta(id, attr, fn){
          var caja = document.getElementById(id);
          caja.addEventListener('click', function(e){
            var b = e.target.closest('button['+attr+']'); if(!b) return;
            fn(+b.getAttribute(attr));
            caja.querySelectorAll('button').forEach(function(x){
              x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
            });
            pinta();
          });
        }
        conecta('seg-peso-f', 'data-f', function(v){ f = v; });
        conecta('seg-peso-d', 'data-d', function(v){ d = v; });
        pinta();
      })();
      </script>
'''


# ===========================================================================
# S3 · Si se lee desde el fondo
#
# Lienzo 640 x 372.
#   Izquierda: planta del aula a escala, 7,0 m de ancho por 9,5 m de fondo.
#     PPM = 252 / 9,5 = 26,53 px por metro -> 185,7 x 252,0 px, en x 40..225,7
#     y 46..298. Filas cada metro, del 2 al 9; cinco sitios cada 1,2 m.
#   Derecha:   la letra dibujada A LA ESCALA DE LA PARED, x 330..620.
#     BK = 0,48 px de lienzo por milimetro de pared. Linea de base en y = 210.
#     Dos barras apoyadas en ella -lo que mide y lo que hace falta- y la
#     palabra al lado, desde x = 384. El caso mas grande (32 pt en pantalla de
#     4 m) da 96,0 mm -> barra de 46 px y una palabra de unos 208 px de ancho:
#     384 + 208 = 592, dentro de los 620.
#   Veredicto: y 284..328. Ninguna linea de texto pasa de x = 620: medido en
#   u9_verifica.py con el navegador a 390 px, que es donde se nota.
#
# La cadena de cuentas, toda con unidades:
#   cuerpo (pt) -> altura de mayuscula (mm) = pt x 0,3528 mm/pt x 0,72
#   ampliacion = ancho proyectado / 0,3386667 m  (la diapositiva 16:9 estandar,
#                que son 13 pulgadas y un tercio de ancho)
#   altura en la pared (mm) = altura en la diapositiva x ampliacion
#   criterio: se lee si esa altura >= distancia / 200
# El 0,72 es la altura de mayuscula de Helvetica (718 milesimas de em).
# El /200 es regla practica NUESTRA, y va rotulada como tal dentro de la escena:
# equivale a que la letra llegue al ojo con unos 17 minutos de arco.
# ===========================================================================
ESCENA_AULA = u'''
      <div class="escena" id="esc-aula">
        <div class="escena-barra">
          <span class="escena-titulo">El cuerpo de letra</span>
          <div class="seg" id="seg-aula-c">
            <button type="button" data-c="12">12 pt</button>
            <button type="button" data-c="18" aria-pressed="true">18 pt</button>
            <button type="button" data-c="24">24 pt</button>
            <button type="button" data-c="32">32 pt</button>
          </div>
        </div>
        <div class="escena-barra">
          <span class="escena-titulo">La pantalla y la fila</span>
          <div class="seg" id="seg-aula-o">
            <button type="button" data-p="1.5">Pantalla 1,5 m</button>
            <button type="button" data-p="2.5" aria-pressed="true">2,5 m</button>
            <button type="button" data-p="4">4 m</button>
            <button type="button" data-d="2">1.&ordf; fila</button>
            <button type="button" data-d="5">En medio</button>
            <button type="button" data-d="9" aria-pressed="true">&Uacute;ltima fila</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 372" id="svg-aula" role="img"
               aria-label="La planta del aula con la fila elegida y la letra dibujada al tama&ntilde;o que tiene sobre la pantalla"></svg>
        </div>
        <div class="pie" id="pie-aula"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-aula');
        if(!svg) return;
        var pie = document.getElementById('pie-aula');

        var PT_MM = 25.4 / 72;     /* un punto, en mil\\u00edmetros */
        var CAP = 0.72;            /* altura de may\\u00fascula de Helvetica */
        /* Ancho de una diapositiva 16:9: 13 pulgadas y un tercio, o sea 33,867 cm.
           Se escribe como la division y no como 0,3387 a proposito: con el valor
           redondeado, el caso de 24 pt a 9 m -que sale EXACTO- se quedaba dos
           millonesimas por debajo y la escena ped\\u00eda 25 pt. */
        var DIAPO_M = 40 / 3 * 0.0254;
        var UMBRAL = 200;          /* se lee si la letra mide al menos d/200 */
        var FONDO = 9.5;           /* fondo del aula, en metros */
        var ANCHO = 7.0;           /* ancho del aula, en metros */
        var PPM = 252 / FONDO;     /* px de lienzo por metro */
        var BK = 0.48;             /* px de lienzo por mil\\u00edmetro de pared */
        var PALABRA = 'DATOS';

        var cuerpo = 18, pantalla = 2.5, dist = 9;

        function cuentas(){
          var hDiapo = cuerpo * PT_MM * CAP;          /* mm sobre la diapositiva */
          var ampl = pantalla / DIAPO_M;              /* cu\\u00e1nto la agranda */
          var hPared = hDiapo * ampl;                 /* mm sobre la pantalla */
          var minimo = dist * 1000 / UMBRAL;          /* mm que hacen falta */
          var ptMin = minimo / (PT_MM * CAP * ampl);  /* el cuerpo que har\\u00eda falta */
          return {hDiapo:hDiapo, ampl:ampl, hPared:hPared, minimo:minimo,
                  ptMin:ptMin, vale:(hPared >= minimo - 0.0001)};
        }

        function texto(x, y, t, op){
          op = op || {};
          return '<text x="'+x+'" y="'+y+'" class="rotulo-svg" style="font-size:'+(op.s || 11)
               + 'px'+(op.c ? ';fill:'+op.c : '')+(op.p ? ';font-weight:500' : '')
               + (op.a ? ';text-anchor:'+op.a : '')+'">'+t+'</text>';
        }
        function num(v, n){ return v.toFixed(n === undefined ? 1 : n).replace('.', ','); }

        function pinta(){
          var c = cuentas(), s = '';
          var AX = 40, AY = 56, AW = ANCHO*PPM, AH = FONDO*PPM, EJE = AX + AW/2;

          /* ---------- la planta del aula, a escala ---------- */
          s += texto(20, 24, 'EL AULA VISTA DESDE ARRIBA, A ESCALA', {s:10, p:1});
          s += '<rect x="'+AX+'" y="'+AY+'" width="'+AW.toFixed(1)+'" height="'+AH.toFixed(1)
             + '" fill="var(--surface-2)" stroke="var(--line)" stroke-width="1"></rect>';
          var pw = pantalla * PPM;
          s += '<rect x="'+(EJE - pw/2).toFixed(1)+'" y="'+(AY - 7)+'" width="'+pw.toFixed(1)
             + '" height="7" fill="var(--goo-azul)"></rect>';
          s += texto(EJE, AY - 12, 'PANTALLA  ' + num(pantalla) + ' m',
                     {s:9.5, a:'middle', c:'var(--goo-azul)', p:1});
          for(var m = 2; m <= 9; m++){
            var fy = AY + m*PPM, aqui = (m === dist);
            for(var k = -2; k <= 2; k++){
              s += '<rect x="'+(EJE + k*1.2*PPM - 8).toFixed(1)+'" y="'+(fy - 5).toFixed(1)
                 + '" width="16" height="10" fill="'
                 + (aqui ? 'var(--goo-rojo)' : 'var(--line)')+'"></rect>';
            }
          }
          var dy = AY + dist*PPM;
          s += '<path d="M'+EJE.toFixed(1)+' '+AY+' V'+dy.toFixed(1)+'" '
             + 'stroke="var(--goo-rojo)" stroke-width="1.5" stroke-dasharray="4 3"></path>';
          s += texto(EJE + 7, (AY + dy)/2, num(dist) + ' m',
                     {s:11.5, c:'var(--goo-rojo)', p:1});
          s += texto(20, AY + AH + 18, 'Aula de ' + num(ANCHO) + ' \\u00d7 ' + num(FONDO)
                     + ' m, ocho filas.', {s:10});

          /* ---------- la letra, al tamano que tiene en la pared ----------
             Dos barras a la MISMA escala de pared, apoyadas en la misma linea
             de base: la maciza es lo que mide la mayuscula y la de rayas, lo
             que haria falta. Comparar las dos es exacto; comparar la palabra
             con una caja no lo era, porque el hueco que ocupa un texto no es
             la altura de sus mayusculas. */
          var DX = 330, BASE = 210;
          s += texto(DX, 24, 'LA LETRA SOBRE LA PANTALLA, A SU TAMA\\u00d1O', {s:10, p:1});
          s += '<path d="M'+DX+' '+BASE+' H620" stroke="var(--line)" stroke-width="1"></path>';
          s += '<rect x="'+DX+'" y="'+(BASE - c.hPared*BK).toFixed(1)+'" width="18" height="'
             + (c.hPared*BK).toFixed(1)+'" fill="'
             + (c.vale ? 'var(--goo-verde)' : 'var(--goo-rojo)')+'"></rect>';
          s += '<rect x="'+(DX + 24)+'" y="'+(BASE - c.minimo*BK).toFixed(1)+'" width="18" '
             + 'height="'+(c.minimo*BK).toFixed(1)+'" fill="none" stroke="var(--ink-soft)" '
             + 'stroke-width="1.5" stroke-dasharray="3 2"></rect>';
          /* la raya de lo que hace falta, cruzando la palabra */
          s += '<path d="M'+DX+' '+(BASE - c.minimo*BK).toFixed(1)+' H620" '
             + 'stroke="var(--ink-soft)" stroke-width="1" stroke-dasharray="3 2" '
             + 'opacity=".7"></path>';
          /* la palabra: el cuerpo en px es la altura de mayuscula dividida por CAP */
          var fpx = c.hPared / CAP * BK;
          s += '<text x="'+(DX + 54)+'" y="'+BASE+'" style="font-family:'
             + "'Nimbus Sans','Liberation Sans',Helvetica,Arial,sans-serif"
             + ';font-size:'+fpx.toFixed(2)+'px;font-weight:500;fill:'
             + (c.vale ? 'var(--goo-verde)' : 'var(--goo-rojo)')+'">'+PALABRA+'</text>';
          s += texto(DX, 232, 'Maciza: lo que mide, ' + num(c.hPared) + ' mm', {s:10.5,
                     c: c.vale ? 'var(--goo-verde)' : 'var(--goo-rojo)'});
          s += texto(DX, 248, 'De rayas: lo que hace falta, ' + num(c.minimo) + ' mm',
                     {s:10.5});
          s += texto(DX, 264, 'Las dos, a la escala de la pantalla.', {s:10.5});

          /* ---------- veredicto ----------
             El -1e-9 no es un apano feo: cuando el cuerpo sale EXACTO -24 pt a
             9 m con pantalla de 2,5 m da 45,000000 mm clavados- la aritmetica
             de coma flotante deja una basurilla en el decimo decimal, y sin el
             margen el redondeo hacia arriba pediria 25 pt en vez de 24. */
          s += '<rect x="330" y="284" width="290" height="44" fill="'
             + (c.vale ? 'var(--accent-soft)' : 'var(--surface-2)')+'" stroke="'
             + (c.vale ? 'var(--goo-verde)' : 'var(--goo-rojo)')+'" stroke-width="1.5"></rect>';
          s += texto(344, 311, c.vale
                ? 'S\\u00cd se lee desde esa fila'
                : 'NO se lee: har\\u00edan falta ' + Math.ceil(c.ptMin - 1e-9) + ' pt',
                {s:14, p:1, c: c.vale ? 'var(--goo-verde)' : 'var(--goo-rojo)'});

          svg.innerHTML = s;

          pie.innerHTML = 'La cadena entera, con sus unidades. <b>' + cuerpo + ' pt</b> &times; '
            + '0,3528 mm/pt &times; 0,72 (lo que sube una may&uacute;scula) = <b>' + num(c.hDiapo)
            + ' mm</b> de alto en la diapositiva. El proyector la estira hasta <b>'
            + num(pantalla) + ' m</b> de ancho, o sea <b>&times;' + num(c.ampl) + '</b>, y en la '
            + 'pared la may&uacute;scula mide <b>' + num(c.hPared) + ' mm</b>. Desde <b>'
            + num(dist) + ' m</b> hace falta al menos <b>' + num(c.minimo) + ' mm</b>.'
            + '<br><span style="font-size:12.5px">Ojo: lo de &laquo;la distancia dividida entre '
            + '200&raquo; es una <b>regla pr&aacute;ctica nuestra</b>, no una norma; equivale a '
            + 'que la letra te llegue con un &aacute;ngulo de unos 17 minutos de arco. Lo que no '
            + 'es opinable es la cuenta de arriba, ni que un cuerpo peque&ntilde;o se hace '
            + 'peque&ntilde;o tambi&eacute;n en la pared.</span>';
        }

        var cajaC = document.getElementById('seg-aula-c');
        var cajaO = document.getElementById('seg-aula-o');
        function marca(caja, attr, valor){
          caja.querySelectorAll('button['+attr+']').forEach(function(b){
            b.setAttribute('aria-pressed',
              b.getAttribute(attr) === String(valor) ? 'true' : 'false');
          });
        }
        cajaC.addEventListener('click', function(e){
          var b = e.target.closest('button[data-c]'); if(!b) return;
          cuerpo = +b.dataset.c; marca(cajaC, 'data-c', b.dataset.c); pinta();
        });
        cajaO.addEventListener('click', function(e){
          var b = e.target.closest('button'); if(!b) return;
          if(b.dataset.p){ pantalla = +b.dataset.p; marca(cajaO, 'data-p', b.dataset.p); }
          else if(b.dataset.d){ dist = +b.dataset.d; marca(cajaO, 'data-d', b.dataset.d); }
          else return;
          pinta();
        });
        pinta();
      })();
      </script>
'''


# ===========================================================================
# S3 · Leer contra escuchar
#
# Lienzo 640 x 216.
#   Eje de tiempo x 132..612 (480 px para el mayor de los dos tiempos), con la
#   marca cada 2, 5, 15 o 30 s segun lo que dure.
#   Barra de lectura y 54..78 · barra de tu explicacion y 98..122
#   Zona en la que ya han terminado de leer: y 50..128, en amarillo.
#   Lectura de resultados y 160..206.
#
# Las palabras se cuentan del texto que haya escrito en ese momento. Los dos
# tiempos salen de dividir, y la velocidad de lectura es un boton -a la vista-
# porque es el unico dato discutible de la cuenta.
# ===========================================================================
_DIAPO_CARGADA = (
    u'Las herramientas digitales permiten crear, editar y difundir contenidos de forma '
    u'eficaz. Los formatos de fichero determinan la compatibilidad entre aplicaciones. '
    u'Las imágenes pueden ser de mapa de bits o vectoriales según cómo '
    u'guarden la información. Una presentación debe estructurarse en '
    u'introducción, desarrollo y conclusión, cuidando la legibilidad y la '
    u'coherencia visual del conjunto.')
_DIAPO_LIMPIA = u'Al doble de ancho, cuatro veces el peso'

_TEXTOS_JS = (
    u"        var TEXTOS = {\n"
    u"          cargada: " + _lit(_DIAPO_CARGADA) + u",\n"
    u"          limpia : " + _lit(_DIAPO_LIMPIA) + u"\n"
    u"        };\n")

ESCENA_CARRERA = u'''
      <div class="escena" id="esc-carrera">
        <div class="escena-barra">
          <span class="escena-titulo">Lo que pone en la diapositiva</span>
          <div class="seg" id="seg-car-t">
            <button type="button" data-t="cargada" aria-pressed="true">La de siempre</button>
            <button type="button" data-t="limpia">Una idea sola</button>
          </div>
        </div>
        <div class="escena-barra">
          <textarea id="car-texto" rows="3" spellcheck="false"
            aria-label="El texto de la diapositiva"
            style="flex:1;min-width:220px;font:400 12.5px var(--f-b);padding:8px 10px;
                   border:1.5px solid var(--line);border-radius:2px;background:var(--surface);
                   color:var(--ink);resize:vertical"></textarea>
        </div>
        <div class="escena-barra">
          <span class="escena-titulo">Y adem&aacute;s</span>
          <div class="seg" id="seg-car-o">
            <button type="button" data-v="150">Leen a 150</button>
            <button type="button" data-v="200" aria-pressed="true">Leen a 200</button>
            <button type="button" data-v="250">Leen a 250</button>
            <button type="button" data-s="30">Hablas 30 s</button>
            <button type="button" data-s="45" aria-pressed="true">Hablas 45 s</button>
            <button type="button" data-s="60">Hablas 60 s</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 216" id="svg-carrera" role="img"
               aria-label="Dos barras de tiempo: lo que tarda la clase en leer la diapositiva y lo que tardas t&uacute; en explicarla"></svg>
        </div>
        <div class="pie" id="pie-carrera"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-carrera');
        if(!svg) return;
        var pie = document.getElementById('pie-carrera');
        var caja = document.getElementById('car-texto');

''' + _TEXTOS_JS + u'''
        var vel = 200, hablas = 45;

        function palabras(){
          var t = caja.value.trim();
          return t ? t.split(/\\s+/).length : 0;
        }
        function texto(x, y, t, op){
          op = op || {};
          return '<text x="'+x+'" y="'+y+'" class="rotulo-svg" style="font-size:'+(op.s || 11)
               + 'px'+(op.c ? ';fill:'+op.c : '')+(op.p ? ';font-weight:500' : '')
               + (op.a ? ';text-anchor:'+op.a : '')+'">'+t+'</text>';
        }
        function seg(v){ return v.toFixed(1).replace('.', ',') + ' s'; }

        function pinta(){
          var n = palabras();
          var tLeer = n / vel * 60;
          var max = Math.max(tLeer, hablas, 1);
          var X0 = 132, ANCHO = 480, k = ANCHO / max;
          var s = '';

          s += texto(20, 30, 'LA CLASE LEE ' + n + (n === 1 ? ' PALABRA' : ' PALABRAS')
               + ' A ' + vel + ' POR MINUTO', {s:10, p:1});

          var paso = max > 90 ? 30 : (max > 40 ? 15 : (max > 18 ? 5 : 2));
          for(var t = 0; t <= max + 0.001; t += paso){
            var x = X0 + t*k;
            s += '<path d="M'+x.toFixed(1)+' 46 V132" stroke="var(--line-soft)" '
               + 'stroke-width="1"></path>';
            s += texto(x, 146, t + ' s', {s:9.5, a:'middle'});
          }

          var sobra = hablas - tLeer;
          if(sobra > 0.2){
            s += '<rect x="'+(X0 + tLeer*k).toFixed(1)+'" y="50" width="'+(sobra*k).toFixed(1)
               + '" height="78" fill="var(--goo-amarillo)" opacity=".22"></rect>';
            s += texto(X0 + tLeer*k + (sobra*k)/2, 43, 'YA LO HAN LE\\u00cdDO TODO',
                       {s:9.5, a:'middle', c:'#9a7326', p:1});
          }

          /* La cifra va detras de la barra, salvo que ya no quepa: entonces se
             mete dentro, alineada a la derecha. Si no, la barra mas larga se
             lleva su numero fuera del lienzo. */
          function cifra(w, y, t){
            return (X0 + w + 60 < 632)
              ? texto(X0 + w + 8, y, t, {s:11})
              : texto(X0 + w - 8, y, t, {s:11, a:'end'});
          }

          s += texto(124, 71, 'LA CLASE LEE', {s:10, a:'end', p:1});
          var wLeer = Math.max(1, tLeer*k);
          s += '<rect x="'+X0+'" y="54" width="'+wLeer.toFixed(1)
             + '" height="24" fill="var(--goo-rojo)" opacity=".55"></rect>';
          s += cifra(wLeer, 71, seg(tLeer));

          s += texto(124, 115, 'T\\u00da HABLAS', {s:10, a:'end', p:1});
          s += '<rect x="'+X0+'" y="98" width="'+(hablas*k).toFixed(1)
             + '" height="24" fill="var(--goo-azul)" opacity=".55"></rect>';
          s += cifra(hablas*k, 115, seg(hablas));

          s += '<rect x="20" y="160" width="600" height="46" fill="var(--surface-2)"></rect>';
          var frase, rojo = true;
          if(n === 0){
            frase = 'Escribe algo en la caja de arriba.'; rojo = false;
          } else if(sobra > 0.2){
            frase = 'Terminan de leer ' + seg(sobra) + ' antes de que t\\u00fa acabes.';
          } else if(sobra < -0.2){
            frase = 'No les da tiempo: les faltan ' + seg(-sobra) + ' para acabar de leerla.';
          } else {
            frase = 'Van a la par, y aun as\\u00ed est\\u00e1n haciendo dos cosas a la vez.';
            rojo = false;
          }
          s += texto(36, 190, frase, {s:14, p:1, c: rojo ? 'var(--goo-rojo)' : 'var(--ink)'});

          svg.innerHTML = s;

          var t2;
          if(n === 0){
            t2 = 'Con la diapositiva en blanco no hay carrera: toda la atenci&oacute;n es tuya.';
          } else if(sobra > 0.2){
            t2 = '<b>' + n + ' palabras</b> a ' + vel + ' palabras por minuto son <b>' + seg(tLeer)
               + '</b> de lectura, y t&uacute; hablas <b>' + hablas + ' s</b>. Durante <b>'
               + seg(sobra) + '</b> la clase ya se sabe el final y te est&aacute; esperando: has '
               + 'contado el remate antes de contarlo.';
          } else {
            t2 = '<b>' + n + ' palabras</b> son <b>' + seg(tLeer) + '</b> de lectura y t&uacute; '
               + 'hablas <b>' + hablas + ' s</b>. No les da tiempo a leerlo mientras te escuchan, '
               + 'as&iacute; que har&aacute;n una de las dos cosas. Normalmente, leer: el ojo '
               + 'gana.';
          }
          t2 += '<br><span style="font-size:12.5px">Las palabras se cuentan de lo que hay escrito '
              + 'ah&iacute; arriba, ahora mismo: b&oacute;rralo y mira lo que pasa. La velocidad '
              + 'de lectura la eliges t&uacute;, y por eso est&aacute; en un bot&oacute;n a la '
              + 'vista: es el &uacute;nico dato discutible de toda la cuenta.</span>';
          pie.innerHTML = t2;
        }

        var cajaT = document.getElementById('seg-car-t');
        cajaT.addEventListener('click', function(e){
          var b = e.target.closest('button[data-t]'); if(!b) return;
          caja.value = TEXTOS[b.dataset.t];
          cajaT.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          pinta();
        });
        var cajaO = document.getElementById('seg-car-o');
        cajaO.addEventListener('click', function(e){
          var b = e.target.closest('button'); if(!b) return;
          var attr = b.dataset.v ? 'data-v' : (b.dataset.s ? 'data-s' : null);
          if(!attr) return;
          if(attr === 'data-v') vel = +b.dataset.v; else hablas = +b.dataset.s;
          cajaO.querySelectorAll('button['+attr+']').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          pinta();
        });
        caja.addEventListener('input', pinta);

        caja.value = TEXTOS.cargada;
        pinta();
      })();
      </script>
'''
