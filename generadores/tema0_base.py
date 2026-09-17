# -*- coding: utf-8 -*-
"""Molde comun del tema 0. Genera la pagina completa a partir de un dict de contenido."""

AUTOR = u"Roberto P. Garc&iacute;a Llorente"
AUTOR_TXT = u"Roberto P. García Llorente"
CARGO = u"Profesor de Tecnología en Educación Secundaria"
SITIO = u"https://rgllorente82-png.github.io/robertotecnologia"
LIC = u"https://creativecommons.org/licenses/by-sa/4.0/deed.es"
REPO = u"https://github.com/rgllorente82-png/robertotecnologia"

ESTILO = u"""
:root{
  --paper:#f8f9fa;--surface:#fff;--surface-2:#f1f3f4;--ink:#202124;--ink-soft:#5f6368;
  --line:#dadce0;--line-soft:#e8eaed;--accent:#1a73e8;--accent-soft:#e8f0fe;
  --goo-azul:#4285f4;--goo-rojo:#ea4335;--goo-amarillo:#fbbc04;--goo-verde:#34a853;
  --grid:rgba(66,133,244,.09);
  --f-b:"Roboto",-apple-system,"Segoe UI",Arial,sans-serif;
  --f-m:"Roboto Mono",ui-monospace,Consolas,monospace;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --paper:#202124;--surface:#292a2d;--surface-2:#35363a;--ink:#e8eaed;--ink-soft:#9aa0a6;
  --line:#5f6368;--line-soft:#3c4043;--accent:#8ab4f8;--accent-soft:#1f3347;
  --goo-azul:#8ab4f8;--goo-rojo:#f28b82;--goo-amarillo:#fdd663;--goo-verde:#81c995;
  --grid:rgba(138,180,248,.09)}}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.65 var(--f-b);letter-spacing:.01em}
.wrap{max-width:900px;margin:0 auto;padding:0 20px}
header.top{background:var(--surface);border-bottom:2px solid var(--ink);
  background-image:linear-gradient(var(--grid) 1px,transparent 1px),linear-gradient(90deg,var(--grid) 1px,transparent 1px);
  background-size:24px 24px;position:sticky;top:0;z-index:50}
header.top .wrap{padding-block:16px 0}
.eyebrow{font-family:var(--f-m);font-size:11.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent)}
.eyebrow a{color:inherit;text-decoration:none;border-bottom:1px solid transparent}
.eyebrow a:hover{border-bottom-color:currentColor}
h1{font-weight:700;font-size:clamp(22px,4.4vw,30px);margin:6px 0 12px;letter-spacing:-.015em}
nav.sesiones{display:flex;gap:8px;overflow-x:auto;padding-bottom:12px}
nav.sesiones button{flex:none;background:var(--surface);color:var(--ink-soft);border:1.5px solid var(--line);
  border-radius:2px;padding:7px 14px;font:400 13px var(--f-m);cursor:pointer;white-space:nowrap}
nav.sesiones button[aria-selected="true"]{background:var(--goo-azul);border-color:var(--goo-azul);color:#fff}
nav.sesiones button[disabled]{opacity:.45;cursor:default}
main{padding-block:26px 70px}
.ses-head{background:var(--surface);border:1.5px solid var(--line);border-radius:2px;padding:20px;margin-bottom:26px}
.ses-head h2{font-size:22px;margin:6px 0 8px;letter-spacing:-.01em}
.ses-head p{margin:0 0 14px;color:var(--ink-soft)}
.minutado{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:12px}
.min{font-family:var(--f-m);font-size:11.5px;border:1px solid var(--line);border-radius:2px;padding:4px 9px;color:var(--ink-soft)}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{font-family:var(--f-m);font-size:11px;border:1px solid var(--goo-azul);color:var(--goo-azul);border-radius:2px;padding:3px 8px}
.chip.sab{border-color:var(--line);color:var(--ink-soft)}
.bloque{margin-bottom:34px}
.rotulo{display:flex;align-items:center;gap:10px;font-family:var(--f-m);font-size:12px;letter-spacing:.1em;
  text-transform:uppercase;color:var(--ink-soft);margin-bottom:12px}
.rotulo .num{background:var(--goo-azul);color:#fff;border-radius:2px;min-width:26px;height:24px;
  display:inline-grid;place-items:center;font-weight:500}
.rotulo::after{content:"";flex:1;height:2px;background:var(--goo-azul);opacity:.3}
.bloque:nth-of-type(4n+2) .rotulo .num,.bloque:nth-of-type(4n+2) .rotulo::after{background:var(--goo-rojo)}
.bloque:nth-of-type(4n+3) .rotulo .num,.bloque:nth-of-type(4n+3) .rotulo::after{background:var(--goo-verde)}
.bloque:nth-of-type(4n+4) .rotulo .num{background:var(--goo-amarillo);color:#202124}
.bloque:nth-of-type(4n+4) .rotulo::after{background:var(--goo-amarillo)}
h3{font-size:18px;margin:22px 0 6px;letter-spacing:-.01em}
h4{font-size:15.5px;margin:16px 0 4px}
.bloque ul,.bloque ol{padding-left:22px}
.bloque li{margin-bottom:5px}
.nota,.aviso,.def{background:var(--surface);border:1.5px solid var(--line);border-radius:2px;padding:14px 16px;margin:16px 0}
.nota{border-left:5px solid var(--goo-azul)}
.aviso{border-left:5px solid var(--goo-amarillo)}
.def{border-left:5px solid var(--goo-verde)}
.n-tag{display:block;font-family:var(--f-m);font-size:11px;letter-spacing:.1em;text-transform:uppercase;
  color:var(--ink-soft);margin-bottom:5px}
.nota .n-tag{color:var(--goo-azul)}
.escena{background:var(--surface);border:1.5px solid var(--line);border-radius:2px;margin:18px 0}
.escena-barra{display:flex;flex-wrap:wrap;gap:10px;align-items:center;justify-content:space-between;
  padding:12px 16px;border-bottom:1px solid var(--line)}
.escena-titulo{font-family:var(--f-m);font-size:11.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-soft)}
.seg{display:flex;gap:6px;flex-wrap:wrap}
.seg button{background:var(--surface);border:1.5px solid var(--line);border-radius:2px;padding:6px 12px;
  font:400 12px var(--f-m);color:var(--ink-soft);cursor:pointer}
.seg button[aria-pressed="true"]{background:var(--goo-azul);border-color:var(--goo-azul);color:#fff}
.lienzo{padding:10px;background:var(--surface);
  background-image:linear-gradient(var(--grid) 1px,transparent 1px),linear-gradient(90deg,var(--grid) 1px,transparent 1px);
  background-size:20px 20px}
.lienzo svg{width:100%;height:auto;display:block}
.pie{padding:12px 16px;border-top:1px solid var(--line);font-size:14.5px;color:var(--ink-soft)}
.ficha{background:var(--surface);border:1.5px solid var(--line);border-radius:2px;margin:16px 0;overflow:hidden}
.ficha-cab{display:flex;flex-wrap:wrap;gap:10px;justify-content:space-between;align-items:center;
  background:var(--ink);color:var(--surface);padding:12px 16px;font-family:var(--f-m);font-size:11.5px;
  letter-spacing:.08em;text-transform:uppercase}
.ficha-cab .chip{border-color:var(--surface);color:var(--surface)}
.ficha-cuerpo{padding:16px}
.resp{border:1px solid var(--line);border-radius:2px;margin:8px 0}
.resp summary{cursor:pointer;padding:9px 13px;font-family:var(--f-m);font-size:11.5px;letter-spacing:.08em;
  text-transform:uppercase;color:var(--ink-soft)}
.resp summary::-webkit-details-marker{display:none}
.resp-cuerpo{padding:0 13px 13px}
.resp-cuerpo p:last-child{margin-bottom:0}

.narra{display:flex;gap:14px;align-items:flex-start}
.avatar-caja{flex:none;width:104px}
.avatar-caja svg.avatar{width:104px;height:72px;display:block}
.avatar.habla{animation:habla .34s ease-in-out infinite alternate}
@keyframes habla{from{transform:translateY(0)}to{transform:translateY(-2.5px)}}
.globo{flex:1;background:var(--surface-2);border:1.5px solid var(--line);border-radius:2px;padding:11px 13px;position:relative}
.globo::before{content:"";position:absolute;left:-9px;top:20px;width:0;height:0;
  border-top:8px solid transparent;border-bottom:8px solid transparent;border-right:9px solid var(--line)}
.avatar-dice{margin-top:8px;font-family:var(--f-m);font-size:12px;color:var(--goo-azul);font-style:italic}
.voz-no{margin:10px 0 0;font-size:13px;color:var(--ink-soft)}
@media (max-width:520px){.narra{flex-direction:column;align-items:center}.globo::before{display:none}}

.reto-piensa{background:var(--surface);border:1.5px solid var(--goo-amarillo);border-left-width:5px;
  border-radius:2px;padding:14px 16px;margin:16px 0}
.reto-piensa .n-tag{color:#9a7326}
.reto-piensa p{margin:0}
.resp.revela summary{color:var(--goo-azul);font-weight:500}
.resp.revela[open] summary{color:var(--ink-soft)}
.resp.revela table{margin:0}
.secuencia li.oculto{color:transparent;background:var(--surface-2);border-radius:2px;user-select:none}
.secuencia li.oculto *{visibility:hidden}
.secuencia li{transition:color .25s ease,background .25s ease;padding:2px 4px}
#btn-secuencia{background:var(--surface);border:1.5px solid var(--goo-azul);color:var(--goo-azul);
  border-radius:2px;padding:7px 14px;font:500 12px var(--f-m);cursor:pointer}
#btn-secuencia:disabled{border-color:var(--line);color:var(--ink-soft);cursor:default}

/* series del grafico de coste: validadas con el script de dataviz
   claro  #ea4335/#1a73e8  -> min CVD 27.0, vision normal 36.8
   oscuro #ef5350/#4285f4  -> min CVD 24.6, vision normal 33.2 */
:root{--c-analog:#ea4335;--c-digital:#1a73e8}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--c-analog:#ef5350;--c-digital:#4285f4}}
.ejeq{fill:var(--ink-soft);font-family:var(--f-m);font-size:11px}
.etq{fill:var(--ink);font-family:var(--f-m);font-size:11px;font-weight:500}


.foto{margin:16px 0;border:1.5px solid var(--line);border-radius:2px;background:var(--surface);overflow:hidden}
.foto img{width:100%;height:auto;display:block}
.foto figcaption{padding:11px 14px;font-size:14px;line-height:1.5;color:var(--ink);border-top:1px solid var(--line)}
.credito{display:block;margin-top:7px;font-family:var(--f-m);font-size:10.5px;color:var(--ink-soft);letter-spacing:.02em}
.credito a{color:var(--ink-soft)}
.galeria-ri{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(255px,1fr));margin:16px 0}
.galeria-ri .foto{margin:0}
.galeria-ri figcaption{font-size:13.5px}

.video{margin:16px 0}
.video-play{width:100%;display:flex;align-items:center;gap:16px;padding:22px 20px;cursor:pointer;
  background:var(--surface);border:1.5px solid var(--line);border-radius:2px;text-align:left;
  transition:border-color .18s ease}
.video-play:hover{border-color:var(--goo-rojo)}
.video-tri{flex:none;width:52px;height:38px;border-radius:6px;background:var(--goo-rojo);position:relative}
.video-tri::after{content:"";position:absolute;left:20px;top:11px;border-left:14px solid #fff;
  border-top:8px solid transparent;border-bottom:8px solid transparent}
.video-txt b{display:block;font:500 16px var(--f-b);color:var(--ink);margin-bottom:3px}
.video-txt span{font:400 12px var(--f-m);color:var(--ink-soft)}
.video-nota{margin:9px 0 0;font-size:12.5px;color:var(--ink-soft);line-height:1.5}
.video iframe{width:100%;aspect-ratio:16/9;height:auto;border:1.5px solid var(--line);border-radius:2px;display:block}

/* lo que se copia en la libreta, frente a lo que es solo para entender */
.copiar{background:var(--surface);border:2px solid var(--goo-azul);border-radius:2px;
  padding:16px 18px;margin:18px 0;position:relative}
.copiar::before{content:"PARA LA LIBRETA";position:absolute;top:-11px;left:14px;
  background:var(--goo-azul);color:#fff;font-family:var(--f-m);font-size:10.5px;letter-spacing:.1em;
  padding:3px 9px;border-radius:2px}
.copiar > :first-child{margin-top:6px}
.copiar > :last-child{margin-bottom:0}
.copiar h4{font-size:15px;margin:10px 0 4px}
.entender{border-left:4px solid var(--line);padding:2px 0 2px 16px;margin:18px 0;color:var(--ink-soft)}
.entender .e-tag{display:block;font-family:var(--f-m);font-size:10.5px;letter-spacing:.1em;
  text-transform:uppercase;color:var(--ink-soft);margin-bottom:6px}
.entender b{color:var(--ink)}
@media print{
  .entender,.escena,.video,.narra,nav.sesiones{display:none}
  .copiar{border-width:1.5px;break-inside:avoid}
}

/* ---- avatar narrador, plano y sincronizado con la voz ---- */
.narrador{display:flex;gap:16px;align-items:flex-start;background:var(--surface);
  border:1.5px solid var(--line);border-radius:2px;padding:16px;margin:18px 0}
.narrador-fig{flex:none;width:110px}
.narrador-fig svg{width:110px;height:120px;display:block}
.narrador-txt{flex:1;min-width:0}
.narrador-txt h4{margin:0 0 3px;font-size:15.5px}
.narrador-quien{font-family:var(--f-m);font-size:11px;color:var(--ink-soft);display:block;margin-bottom:9px}
.narrador-barra{height:4px;background:var(--surface-2);border-radius:2px;overflow:hidden;margin:11px 0 8px}
.narrador-barra i{display:block;height:100%;width:0;background:var(--goo-azul);transition:width .1s linear}
.narrador-nota{font-size:12.5px;color:var(--ink-soft);margin:8px 0 0;line-height:1.5}
@media (max-width:520px){.narrador{flex-direction:column;align-items:center}
  .narrador-txt{text-align:center}}

/* ---- test de autoevaluacion ---- */
.test{border:2px solid var(--goo-azul);border-radius:2px;padding:18px 18px 14px;margin:20px 0;
  background:var(--surface);position:relative}
.test::before{content:"AUTOEVALUACI\00D3N";position:absolute;top:-11px;left:14px;background:var(--goo-azul);
  color:#fff;font-family:var(--f-m);font-size:10.5px;letter-spacing:.11em;padding:3px 8px;border-radius:2px}
.test h4{margin:8px 0 14px;font-size:16px}
.test-p{border-top:1px solid var(--line-soft);padding:14px 0 4px}
.test-p:first-of-type{border-top:0}
.test-p > p{margin:0 0 9px;font-weight:500}
.test-op{display:block;padding:7px 10px;margin:0 0 5px;border:1.5px solid var(--line);border-radius:2px;
  cursor:pointer;font-size:15px;line-height:1.45;transition:border-color .12s}
.test-op:hover{border-color:var(--goo-azul)}
.test-op input{margin-right:9px}
.test-op.bien{border-color:var(--goo-verde);background:rgba(52,168,83,.07)}
.test-op.mal{border-color:var(--goo-rojo);background:rgba(234,67,53,.07)}
.test-por{display:none;margin:8px 0 2px;padding:10px 12px;border-left:4px solid var(--goo-azul);
  background:var(--surface-2);font-size:14.5px;line-height:1.55}
.test.corregido .test-por{display:block}
.test-pie{display:flex;align-items:center;gap:14px;margin-top:16px;flex-wrap:wrap}
.test-pie button{font-family:var(--f-m);font-size:13px;border:1.5px solid var(--goo-azul);
  background:var(--goo-azul);color:#fff;border-radius:2px;padding:9px 16px;cursor:pointer}
.test-pie button.otra{background:var(--surface);color:var(--goo-azul)}
.test-nota{font-family:var(--f-m);font-size:15px;color:var(--ink)}
.test-aviso{font-size:12.5px;color:var(--ink-soft);margin:10px 0 0}
@media print{.test{break-inside:avoid}.test-por{display:block}}

/* ---- banco de programacion ---- */
.prog{display:flex;gap:16px;flex-wrap:wrap;align-items:flex-start}
.prog-izq{flex:1 1 380px;min-width:300px}
.prog-der{flex:0 1 230px;min-width:200px}
.prog-lista{border:1.5px solid var(--line);border-radius:2px;background:var(--surface);
  min-height:150px;max-height:260px;overflow:auto;padding:6px;margin:0 0 10px}
.prog-lista ol{margin:0;padding:0 0 0 26px}
.prog-lista li{font-family:var(--f-m);font-size:13px;padding:2px 0;line-height:1.5}
.prog-lista li.activa{background:var(--accent-soft);border-radius:2px}
.prog-lista .vacio{font-family:var(--f-m);font-size:12.5px;color:var(--ink-soft);padding:8px 4px;margin:0}
.prog-bot{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 10px}
.prog-bot button{font-family:var(--f-m);font-size:12.5px;border:1.5px solid var(--line);
  background:var(--surface);color:var(--ink);border-radius:2px;padding:7px 10px;cursor:pointer}
.prog-bot button:hover{border-color:var(--goo-azul);color:var(--goo-azul)}
.prog-bot button.ir{background:var(--goo-azul);border-color:var(--goo-azul);color:#fff}
.prog-bot button.ir:hover{color:#fff}
.prog-est{font-family:var(--f-m);font-size:13px;margin:0;line-height:1.6}
.prog-est b{font-size:13.5px}
.rotulo-svg{fill:var(--ink-soft);font-family:var(--f-m);font-size:11px;letter-spacing:.06em}
.hito{fill:var(--surface);stroke:var(--goo-azul);stroke-width:2;cursor:pointer}
.hito.on{fill:var(--goo-azul)}
.eje-t{fill:none;stroke:var(--line);stroke-width:2}
.cc-sello{position:fixed;right:14px;bottom:calc(14px + env(safe-area-inset-bottom,0px));z-index:9999;
  display:flex;align-items:center;gap:8px;padding:8px 13px;border-radius:2px;background:rgba(18,32,46,.95);
  color:#fff;text-decoration:none;font:500 12px var(--f-b);letter-spacing:.02em}
.cc-sello svg{width:17px;height:17px;flex:none;fill:currentColor}
.cc-sello .cc-autor{opacity:.75;font-weight:400}
@media (max-width:620px){.cc-sello .cc-autor{display:none}}
.cc-aviso{background:var(--surface);border:1.5px solid var(--line);border-radius:2px;padding:18px;margin-top:40px;font-size:14.5px}
.cc-aviso h2{font-size:17px;margin:0 0 8px}
.cc-aviso h3{font-size:14px;margin:14px 0 4px}
.cc-cita code{font-family:var(--f-m);font-size:12.5px;background:var(--surface-2);padding:8px 10px;display:block;border-radius:2px}
footer{border-top:1px solid var(--line);color:var(--ink-soft);font-size:13.5px;margin-top:30px}
footer .wrap{padding-block:18px 26px}
@media (max-width:560px){body{font-size:15.5px}.lienzo{padding:4px}}
"""

SELLO = u"""<a class="cc-sello" href="%s" target="_blank" rel="license noopener"
   title="Material bajo licencia Creative Commons Reconocimiento-CompartirIgual 4.0">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.6 0 12 0zm0 2.2c5.4 0 9.8 4.4 9.8 9.8s-4.4 9.8-9.8 9.8S2.2 17.4 2.2 12 6.6 2.2 12 2.2zM9.1 7.4c-2.3 0-3.9 1.7-3.9 4.6 0 3 1.5 4.6 4 4.6 1.6 0 2.8-.7 3.5-2.1l-1.7-.9c-.4.9-.9 1.3-1.7 1.3-1.1 0-1.7-.8-1.7-2.9s.6-2.9 1.6-2.9c.8 0 1.3.4 1.6 1.3l1.8-.8c-.7-1.5-1.9-2.2-3.5-2.2zm7.7 0c-2.3 0-3.9 1.7-3.9 4.6 0 3 1.5 4.6 4 4.6 1.6 0 2.8-.7 3.5-2.1l-1.7-.9c-.4.9-.9 1.3-1.7 1.3-1.1 0-1.7-.8-1.7-2.9s.6-2.9 1.6-2.9c.8 0 1.3.4 1.6 1.3l1.8-.8c-.7-1.5-1.9-2.2-3.5-2.2z"/></svg>
  <span><b>CC BY-SA 4.0</b> <span class="cc-autor">&middot; %s</span></span>
</a>
<script>
(function(){var m=document.querySelector('.cc-sello');if(!m)return;var c=m.cloneNode(true);
new MutationObserver(function(){if(!document.querySelector('.cc-sello'))document.body.appendChild(c.cloneNode(true));})
.observe(document.body,{childList:true,subtree:true});})();
</script>""" % (LIC, AUTOR)


def aviso_licencia(titulo, canon):
    return u"""<section class="cc-aviso" id="licencia"
  xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/">
  <h2>Licencia y uso</h2>
  <p><span property="dct:title">%s</span> &middot; &copy; 2026
     <a property="cc:attributionName" rel="cc:attributionURL" href="%s">%s</a>, %s.</p>
  <p>Publicado bajo <a rel="license" href="%s"><b>Creative Commons Reconocimiento-CompartirIgual 4.0
     Internacional</b></a>. Puedes copiarlo, adaptarlo y redistribuirlo, incluso con fines comerciales,
     siempre que cites la autor&iacute;a, indiques si lo has modificado y publiques tus versiones
     derivadas con esta misma licencia.</p>
  <h3>C&oacute;mo citar</h3>
  <p class="cc-cita"><code>%s (2026). <i>%s</i>. %s. Bajo licencia CC BY-SA 4.0.</code></p>
  <h3>Qu&eacute; cubre</h3>
  <p>Los <b>textos, los dibujos y el c&oacute;digo</b> de esta p&aacute;gina, que son obra propia.</p>
  <p><b>No cubre las fotograf&iacute;as</b>, que proceden de Wikimedia Commons y conservan su propia
     licencia, indicada bajo cada una. Algunas son de <b>dominio p&uacute;blico</b>; las dem&aacute;s
     est&aacute;n bajo licencias Creative Commons compatibles con esta, y se reproducen citando
     autor&iacute;a y licencia como exigen. Tampoco cubre las tipograf&iacute;as, de Google Fonts con su
     propia licencia.</p>
  <h3>Otros usos</h3>
  <p>Para usos que excedan la licencia, abre una incidencia en
     <a href="%s/issues">el repositorio del proyecto</a>.</p>
</section>""" % (titulo, SITIO, AUTOR, CARGO, LIC, AUTOR, titulo, canon, REPO)


def cabeza(titulo, desc, canon):
    return u"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>%s</title>
<meta name="description" content="%s">
<meta name="license" content="CC BY-SA 4.0">
<link rel="license" href="%s">
<link rel="canonical" href="%s">
<meta name="author" content="%s">
<meta name="dcterms.rights" content="Creative Commons Reconocimiento-CompartirIgual 4.0 Internacional">
<meta name="dcterms.rightsHolder" content="%s">
<meta name="copyright" content="&copy; 2026 %s">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&family=Roboto+Mono:wght@400;500&display=swap">
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"LearningResource","name":"%s","url":"%s","inLanguage":"es",
 "license":"https://creativecommons.org/licenses/by-sa/4.0/",
 "creditText":"%s (2026) &middot; %s &middot; CC BY-SA 4.0","copyrightYear":"2026",
 "author":{"@type":"Person","name":"%s","affiliation":{"@type":"Organization","name":"%s"}},
 "copyrightHolder":{"@type":"Person","name":"%s"},"isAccessibleForFree":true,
 "educationalLevel":"Educaci&oacute;n Secundaria Obligatoria","learningResourceType":"Unidad did&aacute;ctica interactiva"}
</script>
<style>%s</style>
</head>
<body>""" % (titulo, desc, LIC, canon, AUTOR_TXT, AUTOR_TXT, AUTOR_TXT,
             titulo, canon, AUTOR_TXT, titulo, AUTOR_TXT, CARGO, AUTOR_TXT, ESTILO)
