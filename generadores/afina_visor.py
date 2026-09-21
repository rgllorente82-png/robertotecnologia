# -*- coding: utf-8 -*-
u"""Pone el visor de imagenes y la ayuda de las palabras dificiles.

Por que existe. Las dos piezas estaban solo en el HTML publicado: ningun
generador las producia, asi que cualquier build las borraba de la pagina y
nadie se enteraba hasta abrirla. Son iguales en las 27 paginas de los dos
cursos, asi que su sitio es la tuberia y no cada unidad.

EL VISOR (.rtz-*). Un diagrama de 1000 px se ve en un movil de 390 como una
mancha. Al pulsarlo se abre a pantalla completa, con «Ver entero» y «Cerrar»,
y en pantalla pequenia aparece debajo la pista de que se puede ampliar.

LA AYUDA (.rtt). Marca en el texto las palabras que el alumno no tiene por que
saber todavia y las explica al pasar por encima o al pulsarlas.

Se puede volver a pasar: cada pieza lleva su marca y no se duplica.
"""
import io, os, re, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MARCA_VISOR = u'/* visor de imagenes: lo pone afina_visor.py */'
MARCA_AYUDA = u'/* ayuda de palabras: lo pone afina_visor.py */'

VISOR_CSS = MARCA_VISOR + r"""
.rtz-pista{display:none}
@media (max-width:760px){
  figure.foto img{cursor:zoom-in}
  .rtz-pista{display:block;margin-top:6px;font-size:12.5px;letter-spacing:.02em;
    color:var(--muted,#667);text-transform:uppercase}
  /* el sello de licencia va fijo abajo a la derecha: se le reserva sitio para que no
     tape la última línea del contenido */
  body{padding-bottom:64px}
}
.rtz-capa{position:fixed;inset:0;z-index:100000;background:rgba(17,20,24,.94);
  display:none;flex-direction:column}
.rtz-capa.abierta{display:flex}
.rtz-barra{flex:none;display:flex;align-items:center;justify-content:space-between;
  gap:12px;padding:10px 12px;color:#fff;font:500 13.5px/1.3 system-ui,sans-serif}
.rtz-tit{opacity:.85;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.rtz-ajustar{flex:none;background:transparent;color:#fff;border:1px solid rgba(255,255,255,.55);border-radius:2px;padding:8px 12px;font:600 13.5px/1 system-ui,sans-serif;cursor:pointer}
.rtz-cerrar{flex:none;background:#fff;color:#111;border:0;border-radius:2px;
  padding:8px 14px;font:600 13.5px/1 system-ui,sans-serif;cursor:pointer}
.rtz-lienzo{flex:1;overflow:auto;-webkit-overflow-scrolling:touch;padding:10px;
  display:flex;align-items:flex-start;justify-content:flex-start}
.rtz-lienzo img{flex:none;max-width:none;height:auto;background:#fff;border-radius:2px;display:block}
@media print{.rtz-capa{display:none !important}.rtz-pista{display:none !important}}"""

AYUDA_CSS = MARCA_AYUDA + r"""
.rtt{position:absolute;top:10px;right:12px;display:flex;align-items:center;gap:6px;z-index:40}
.rtt span{font:600 10.5px/1 var(--f-m,system-ui);letter-spacing:.06em;text-transform:uppercase;
  opacity:.65;margin-right:2px}
.rtt button{width:30px;height:30px;padding:0;border:1.5px solid var(--line,#ccc);background:var(--surface,#fff);
  color:var(--ink,#222);border-radius:2px;cursor:pointer;font-family:var(--f-m,system-ui);line-height:1}
.rtt button:hover{border-color:var(--goo-azul,#1a73e8)}
.rtt button[aria-pressed="true"]{border-color:var(--goo-azul,#1a73e8);color:var(--goo-azul,#1a73e8);font-weight:700}
.rtt .b1{font-size:11px}.rtt .b2{font-size:13.5px}.rtt .b3{font-size:16px}
@media print{.rtt{display:none}}
@media (max-width:620px){.rtt{position:static;justify-content:flex-end;margin:0 0 10px}}"""

CAPA = r"""
<div class="rtz-capa" role="dialog" aria-modal="true" aria-label="Diagrama ampliado">
  <div class="rtz-barra">
    <span class="rtz-tit"></span>
    <span style="flex:none;display:flex;gap:8px"><button type="button" class="rtz-ajustar">Ver entero</button><button type="button" class="rtz-cerrar">Cerrar</button></span>
  </div>
  <div class="rtz-lienzo"><img alt=""></div>
</div>
"""

VISOR_JS = r"""
(function(){
  var capa=document.querySelector('.rtz-capa'); if(!capa) return;
  var lienzo=capa.querySelector('.rtz-lienzo'), img=lienzo.querySelector('img');
  var tit=capa.querySelector('.rtz-tit'), btn=capa.querySelector('.rtz-cerrar');
  var btnAj=capa.querySelector('.rtz-ajustar'), entero=false;
  var previo=null;

  // ancho al que la imagen se lee. Un SVG es vectorial: se puede estirar hasta
  // que su texto sea legible (nunca menos de 900 px). Una foto NO: pasada de su
  // tamaño real solo se ve pixelada, así que ahí el techo es su propio ancho.
  function esVector(o){ return /\.svg(\?|$)/i.test(o.getAttribute('src')||''); }
  function anchoUtil(o){
    var w=parseInt(o.getAttribute('width'),10)||o.naturalWidth||1000;
    return esVector(o) ? Math.max(w, 900) : w;
  }
  function abrir(o){
    previo=o;
    img.src=o.currentSrc||o.src;
    img.alt=o.alt||'';
    entero=false; if(btnAj) btnAj.textContent='Ver entero';
    img.style.width=anchoUtil(o)+'px';
    tit.textContent=o.alt||'Diagrama';
    capa.classList.add('abierta');
    document.documentElement.style.overflow='hidden';
    lienzo.scrollLeft=0; lienzo.scrollTop=0;
    btn.focus();
  }
  function cerrar(){
    capa.classList.remove('abierta');
    document.documentElement.style.overflow='';
    img.removeAttribute('src');
    if(previo && previo.focus) previo.focus();
  }
  if(btnAj) btnAj.addEventListener('click', function(){
    entero=!entero;
    if(entero){ img.style.width='100%'; btnAj.textContent='Tamaño real'; }
    else { img.style.width=anchoUtil(previo)+'px'; btnAj.textContent='Ver entero'; }
    lienzo.scrollLeft=0; lienzo.scrollTop=0;
  });
  btn.addEventListener('click', cerrar);
  capa.addEventListener('click', function(e){ if(e.target===capa||e.target===lienzo) cerrar(); });
  document.addEventListener('keydown', function(e){
    if(e.key==='Escape' && capa.classList.contains('abierta')) cerrar();
  });

  // delegación: la galería crea sus diagramas con JS, así que no basta con
  // recorrer los que hay al cargar.
  document.addEventListener('click', function(e){
    var o=e.target;
    if(o && o.tagName==='IMG' && /\.(svg|png|jpe?g|webp)(\?|$)/i.test(o.getAttribute('src')||'')
       && !capa.contains(o) && (o.closest('figure.foto') || esVector(o))) abrir(o);
  });
  function marcar(){
    var figs=document.querySelectorAll('figure.foto img, img[src$=".svg"]');
    Array.prototype.forEach.call(figs, function(o){
      if(capa.contains(o) || o.dataset.rtz) return;
      o.dataset.rtz='1';
      o.setAttribute('role','button');
      o.setAttribute('tabindex','0');
      o.addEventListener('keydown', function(ev){
        if(ev.key==='Enter'||ev.key===' '){ ev.preventDefault(); abrir(o); }
      });
      var fig=o.closest('figure.foto');
      if(fig && !fig.querySelector('.rtz-pista')){
        var d=document.createElement('div');
        d.className='rtz-pista';
        d.textContent='Toca el diagrama para ampliarlo';
        var cap=fig.querySelector('figcaption');
        if(cap) cap.parentNode.insertBefore(d, cap); else fig.appendChild(d);
      }
    });
  }
  marcar();
  if(window.MutationObserver){
    new MutationObserver(marcar).observe(document.body,{childList:true,subtree:true});
  }
})();"""

AYUDA_JS = r"""
(function(){
  var SEL='main p, main li, main dd, main dt, main td, main th, main figcaption, main summary,'
        + ' main .nota, main .entender, main .resp-cuerpo';
  var FACTORES=[1, 1.15, 1.32];
  function aplicar(i){
    var f=FACTORES[i]||1;
    var els=document.querySelectorAll(SEL);
    for(var k=0;k<els.length;k++){
      var e=els[k];
      if(!e.dataset.fsBase){
        var fs=parseFloat(window.getComputedStyle(e).fontSize);
        if(!fs) continue;
        e.dataset.fsBase=fs;
      }
      e.style.fontSize=(parseFloat(e.dataset.fsBase)*f).toFixed(2)+'px';
    }
    var bs=document.querySelectorAll('.rtt button');
    for(var j=0;j<bs.length;j++) bs[j].setAttribute('aria-pressed', j===i?'true':'false');
    try{ localStorage.setItem('rt-texto', i); }catch(e){}
  }
  function montar(){
    var cab=document.querySelector('header .wrap') || document.querySelector('header') || document.body;
    if(document.querySelector('.rtt')) return;
    var cont=document.createElement('div');
    cont.className='rtt';
    cont.innerHTML='<span>Texto</span>'
      + '<button type="button" class="b1" aria-label="Tamaño de texto normal">A</button>'
      + '<button type="button" class="b2" aria-label="Tamaño de texto grande">A</button>'
      + '<button type="button" class="b3" aria-label="Tamaño de texto muy grande">A</button>';
    if(getComputedStyle(cab).position==='static') cab.style.position='relative';
    cab.appendChild(cont);
    var bs=cont.querySelectorAll('button');
    for(var i=0;i<bs.length;i++)(function(i){
      bs[i].addEventListener('click', function(){ aplicar(i); });
    })(i);
    var g=0;
    try{ g=parseInt(localStorage.getItem('rt-texto'),10)||0; }catch(e){}
    aplicar(g);
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', montar);
  else montar();
})();"""


def paginas():
    for base, _, ficheros in os.walk(RAIZ):
        if '.git' in base or 'generadores' in base:
            continue
        if 'index.html' in ficheros:
            yield os.path.join(base, 'index.html')


def main():
    visor = ayuda = 0
    for f in paginas():
        s = io.open(f, encoding='utf-8').read()
        original = s
        if u'</style>' not in s or u'</body>' not in s:
            continue
        # Solo donde hay algo que ampliar o que explicar. Un indice sin fotos no
        # necesita el visor, y cargarselo encima seria peso para nada.
        tiene_fotos = u'<figure class="foto"' in s
        tiene_ayuda = u'class="rtt-p"' in s or u'data-rtt' in s

        # Ojo: las paginas publicadas antes del 21-sep llevan el visor SIN esta
        # marca. Si solo se mirase la marca, se duplicaria en todas ellas.
        if tiene_fotos and MARCA_VISOR not in s and u'.rtz-capa{' not in s:
            i = s.rindex(u'</style>')
            s = s[:i] + VISOR_CSS + s[i:]
            j = s.rindex(u'</body>')
            s = s[:j] + CAPA + u'<script>' + VISOR_JS + u'</script>\n' + s[j:]
            visor += 1

        if (tiene_fotos or tiene_ayuda) and MARCA_AYUDA not in s and u'.rtt{position' not in s:
            i = s.rindex(u'</style>')
            s = s[:i] + AYUDA_CSS + s[i:]
            j = s.rindex(u'</body>')
            s = s[:j] + u'<script>' + AYUDA_JS + u'</script>\n' + s[j:]
            ayuda += 1

        if s != original:
            io.open(f, 'w', encoding='utf-8', newline='').write(s)

    print(u'%d paginas con visor, %d con la ayuda de palabras' % (visor, ayuda))
    return 0


if __name__ == '__main__':
    sys.exit(main())
