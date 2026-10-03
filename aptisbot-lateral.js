/* Recuadro «Del mismo autor» (AptisBot) en el lateral de las páginas.
   Con pantalla ancha va fijo en el margen izquierdo; si no cabe, al final del contenido.
   Se puede cerrar con la × y no vuelve a salir en esa sesión. No se imprime.
   La portada lleva su propio recuadro en el HTML y no carga este fichero. */
(function () {
  try { if (sessionStorage.getItem('aptisbot-lateral') === 'cerrado') return; } catch (e) {}
  var css = '' +
    '.apb-lat{box-sizing:border-box;background:var(--surface,#fff);color:var(--ink,#202124);border-radius:14px;' +
    'box-shadow:var(--shadow,0 1px 3px rgba(60,64,67,.3));padding:16px 16px 18px;font:14px/1.45 "Roboto",-apple-system,"Segoe UI",Arial,sans-serif;position:relative}' +
    '.apb-lat .apb-r{font:11px/1.3 "Roboto Mono",ui-monospace,monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-soft,#5f6368);margin:0 18px 8px 0}' +
    '.apb-lat b{display:block;font-weight:500;font-size:15px;line-height:1.3;margin-bottom:6px}' +
    '.apb-lat p{margin:0 0 12px;color:var(--ink-soft,#5f6368)}' +
    '.apb-lat a{display:inline-block;background:var(--accent,#1a73e8);color:var(--surface,#fff);text-decoration:none;font-weight:500;padding:8px 14px;border-radius:999px}' +
    '.apb-lat button{position:absolute;top:6px;right:8px;border:0;background:none;color:var(--ink-soft,#5f6368);font-size:18px;line-height:1;cursor:pointer;padding:4px}' +
    '.apb-fijo{position:fixed;left:14px;top:130px;width:170px;z-index:50}' +
    '.apb-pie{max-width:62ch;margin:36px auto 0}' +
    '@media print{.apb-lat{display:none}}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
  var caja = document.createElement('aside');
  caja.className = 'apb-lat';
  caja.setAttribute('aria-label', 'Otro proyecto del mismo autor');
  caja.innerHTML = '<button type="button" aria-label="Cerrar">×</button>' +
    '<div class="apb-r">Del mismo autor · para docentes</div>' +
    '<b>¿Eres docente y necesitas el B2 o el C1 de inglés?</b>' +
    '<p>AptisBot prepara el examen Aptis desde el móvil: práctica diaria y corrección con IA de writing y speaking.</p>' +
    '<a href="https://aptisbot.es/simulador?utm_source=robertotecnologia&utm_medium=web&utm_campaign=lateral" target="_blank" rel="noopener">Prueba nuestro simulacro</a>';
  caja.querySelector('button').addEventListener('click', function () {
    caja.remove();
    try { sessionStorage.setItem('aptisbot-lateral', 'cerrado'); } catch (e) {}
  });
  var ancho = window.matchMedia('(min-width: 1300px)');
  function coloca() {
    var destino = document.querySelector('main') || document.body;
    if (ancho.matches) { caja.classList.add('apb-fijo'); caja.classList.remove('apb-pie'); document.body.appendChild(caja); }
    else { caja.classList.add('apb-pie'); caja.classList.remove('apb-fijo'); destino.appendChild(caja); }
  }
  function arranca() { coloca(); if (ancho.addEventListener) ancho.addEventListener('change', coloca); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', arranca); else arranca();
})();
