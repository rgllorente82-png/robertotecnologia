/* Recuadro flotante «Del mismo autor» (AptisBot), en todas las páginas.
   Con pantalla ancha flota en el margen izquierdo; en portátil y móvil, abajo, por encima del
   sello de la licencia y en versión corta. Se cierra con la × y vuelve a salir cada vez que se
   abre una página (no se guarda que se cerró). No se imprime. */
(function () {
  var css = '' +
    '.apb-lat{box-sizing:border-box;position:fixed;z-index:9000;background:var(--surface,#fff);color:var(--ink,#202124);border-radius:14px;' +
    'box-shadow:var(--shadow-2,0 1px 3px rgba(60,64,67,.3),0 4px 8px 3px rgba(60,64,67,.15));padding:16px 16px 18px;' +
    'font:14px/1.45 "Roboto",-apple-system,"Segoe UI",Arial,sans-serif;left:14px;top:130px;width:170px}' +
    '.apb-lat .apb-r{font:11px/1.3 "Roboto Mono",ui-monospace,monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-soft,#5f6368);margin:0 18px 8px 0}' +
    '.apb-lat b{display:block;font-weight:500;font-size:15px;line-height:1.3;margin-bottom:6px}' +
    '.apb-lat p{margin:0 0 12px;color:var(--ink-soft,#5f6368)}' +
    '.apb-lat a{display:inline-block;background:var(--accent,#1a73e8);color:var(--surface,#fff);text-decoration:none;font-weight:500;padding:8px 14px;border-radius:999px}' +
    '.apb-lat button{position:absolute;top:4px;right:6px;border:0;background:none;color:var(--ink-soft,#5f6368);font-size:20px;line-height:1;cursor:pointer;padding:6px}' +
    '@media (max-width:1299px){.apb-lat{top:auto;left:10px;right:10px;width:auto;max-width:420px;bottom:calc(58px + env(safe-area-inset-bottom,0px));padding:12px 14px 14px}' +
    '.apb-lat p{display:none}.apb-lat b{margin:0 22px 10px 0}.apb-lat .apb-r{margin-bottom:4px}}' +
    '@media print{.apb-lat{display:none}}';
  function arranca() {
    var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
    var caja = document.createElement('aside');
    caja.className = 'apb-lat';
    caja.setAttribute('aria-label', 'Otro proyecto del mismo autor');
    caja.innerHTML = '<button type="button" aria-label="Cerrar">×</button>' +
      '<div class="apb-r">Del mismo autor · para docentes</div>' +
      '<b>¿Eres docente y necesitas el B2 o el C1 de inglés?</b>' +
      '<p>AptisBot prepara el examen Aptis desde el móvil: práctica diaria y corrección con IA de writing y speaking.</p>' +
      '<a href="https://aptisbot.es/simulador?utm_source=robertotecnologia&utm_medium=web&utm_campaign=flotante" target="_blank" rel="noopener">Prueba nuestro simulacro</a>';
    caja.querySelector('button').addEventListener('click', function () { caja.remove(); });
    document.body.appendChild(caja);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', arranca); else arranca();
})();
