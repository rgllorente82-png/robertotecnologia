# Cómo se comprueba que las páginas están bien

Todo esto se pasa sin tocar nada a mano. Si algo sale en rojo, la página tiene
un problema de verdad o el comprobador se ha quedado viejo — y las dos cosas hay
que arreglarlas, porque un comprobador que miente deja de leerse.

```
pip install -r generadores/REQUISITOS.txt
python -m playwright install chromium
```

## Los que sólo miran

No tocan nada y devuelven 1 si hay algo mal, así que valen para un gancho de git
o para una acción automática.

| Qué mira | Cómo se lanza |
|---|---|
| Caracteres rotos, NUL, UTF-8 inválido y rótulos a medias en las 27 páginas, entidades HTML que se han quedado sin su & por una sustitución mal hecha —«cajetcajétíniacute;n»— y que los apartados de «Cómo se evalúa» de cada ficha sumen 10 puntos | `python generadores/comprueba_paginas.py` |
| Que las cuentas escritas en la prosa cuadren, incluidas las escritas con palabras —«0,2 V por 250 mA son 50 mW»— (173 ahora mismo) | `python generadores/comprueba_cuentas.py` |
| Que los enlaces internos lleven a alguna parte: ficheros, anclas y rutas absolutas resueltas contra la base de publicación, que se lee de la dirección canónica | `python generadores/comprueba_enlaces.py [--fuera]` |
| Que los tests no se pisen entre ellos, que la respuesta buena no caiga siempre en el mismo sitio, y qué unidades no tienen ninguno. Cuenta los dos moldes que hay en el sitio: `.ta` y el `.test` del tema 5 de 2.º | `python generadores/comprueba_tests.py` |
| Que los vídeos de YouTube se puedan ver, y **sin cuenta**: separa el que no se deja empotrar, el que pide edad, el que es **sólo para miembros del canal** y el borrado. Necesita red: si no llega a youtube.com para y lo dice, en vez de sacar 92 «no se sabe». Con `--lista` saca sólo los enlaces por unidad, y eso sí va sin red | `python generadores/comprueba_videos.py [--json]` |
| **Las 27 páginas, sesión por sesión**: errores de JavaScript, escenas que dejan el lienzo vacío, desplazamiento a lo ancho en un móvil de 390 px, que cada test dé «N de N» contestando bien y se borre del todo, que el botón de la sesión abierta lo diga y que el pie de cada escena se anuncie solo | `python generadores/comprueba_sitio.py [filtro]` |
| Las escenas de cada unidad, contra un modelo reescrito en Python **desde la definición**, nunca copiado del JavaScript de la página | `python generadores/c1_verifica.py` … `c9`, y `u1`…`u10`, y `t0` para los dos temas 0 |
| Que las lecturas de aula en PDF se abran, traigan la cabecera de nombre y grupo, sus párrafos vayan sin saltos y ninguna cita a un párrafo por su número apunte fuera del texto (las 21, de los dos cursos) | `python generadores/comprueba_lecturas.py` |
| Que los códigos de criterios y saberes de los chips **existan** en el currículo, y que ningún criterio se quede sin unidad que lo declare | `python generadores/comprueba_curriculo.py` |
| Que cada mando de las escenas —deslizador, casilla, desplegable, botón— **diga lo que es**: no basta con que haya un texto al lado, tiene que estar atado | `python generadores/comprueba_mandos.py [filtro]` |
| Que el texto se pueda agrandar al 200 % sin que nada se corte ni se desborde (WCAG 1.4.4, nivel AA) | `python generadores/comprueba_zoom.py [filtro]` |
| Que el lector de respuestas de YouTube separe bien los cinco casos, con muestras escritas a mano (no prueba que las marcas sean las de hoy: eso sólo lo dice pasarlo con red) | `python generadores/comprueba_videos_prueba.py` |
| Que al **imprimir** una unidad salgan sus seis sesiones y no sólo la abierta. No mira el CSS: manda imprimir cada página a PDF y cuenta las cabeceras que salen | `python generadores/comprueba_impresion.py [filtro]` |
| El contraste de los rótulos de las escenas, en tema claro y en oscuro, mirando la figura del propio SVG que hay debajo del texto y no sólo el fondo del DOM. Un rótulo con halo no cuenta: el halo es la solución | `python generadores/comprueba_contraste.py [filtro]` |

Los dos primeros se complementan: `comprueba_sitio.py` no entra en ninguna
unidad pero no se salta ninguna, así que es lo que pilla lo que se rompe en
todas partes a la vez —tocar el CSS común, un script compartido—; los
`*_verifica.py` entran hondo en una sola.

`u1_verifica.py` es el ejemplo de lo que se espera de un verificador: para el
diagrama de Gantt de la sesión 4 no compara con una copia de sus números, sino
que vuelve a montar el plan a partir de las duraciones de las ocho tareas, de
quién hace cada una y de qué tarea no puede empezar hasta que acabe cuál. De ahí
salen los comienzos, el minuto de terminar y qué tareas tienen holgura —esto
último retrasándolas un minuto y mirando si mueven el final, que es la única
forma de que salga bien cuando trabaja una sola persona y todo es crítico—.

## Los que ponen al día

| Qué hace | Cómo se lanza |
|---|---|
| Índices de curso y portada, contando las sesiones publicadas de cada página | `python generadores/ordena_indice.py` |
| Fotos a su tamaño, y las medidas escritas en cada `<img>` | `python generadores/afina_fotos.py` |
| Open Graph, tarjetas de compartir, sitemap y robots | `python generadores/pon_metadatos.py` |
| Títulos sin saltos de nivel y puntos suspensivos | `python generadores/afina_texto.py` |
| El enlace «Ir al tema N» al final del cierre de cada unidad, con el título leído del `<h1>` de destino | `python generadores/pon_enlace_siguiente.py` |
| Que una tabla ancha se desplace dentro de su caja y no arrastre la página en un móvil | `python generadores/afina_movil.py` |
| Que se respete el ajuste de accesibilidad «reducir el movimiento» (WCAG 2.3.3 y 2.2.2) | `python generadores/afina_movimiento.py` |
| Las tintas de **texto** del ámbar y del verde, que como colores de rellenar no se leen sobre fondo claro: oscuras en el tema claro y claras en el oscuro | `python generadores/afina_tintas.py` |
| La tinta que va **encima** de una barra de color, que es oscura en los dos temas porque los rellenos están elegidos para resaltar | `python generadores/afina_sobre_color.py` |
| Que el pie de cada escena sea una región viva, para que un lector de pantalla anuncie la explicación al pulsar un botón | `python generadores/afina_lectores.py` |
| Que el navegador de sesiones **diga** cuál está abierta y no sólo la pinte: `aria-selected` no es válido en un `<button>` y el navegador lo descarta | `python generadores/afina_navegador.py` |
| Que el test corregido diga con **palabras** cuál era la buena, y no sólo con el color, y que la nota se anuncie al corregir | `python generadores/afina_test.py` |
| Que al imprimir salgan todas las sesiones, cada una en hoja nueva, y que no se impriman los botones que en papel no se pueden pulsar | `python generadores/afina_impresion.py` |
| El enlace de «Saltar al contenido», que evita pasar por las migas y los ocho botones del navegador en cada página (WCAG 2.4.1, nivel A) | `python generadores/afina_salto.py` |
| Repartir por igual el sitio donde cae la respuesta buena en cada test, moviendo las opciones sin tocar su texto | `python generadores/baraja_tests.py` |
| Atar cada `<label>` suelto con el mando que va justo detrás, cuando ese mando tiene `id` | `python generadores/afina_mandos.py` |
| El `scope` de cada celda de encabezado, para que al caer en una casilla se lea «Barato, Bomba sumergible, 2» y no «2» | `python generadores/afina_tablas.py` |
| La plantilla a tamaño real del soporte de móvil, en un A4, con el grueso del cartón como parámetro | `python generadores/u1_plantilla.py [grueso]` |
| El molde y el plano de la tensegridad | `python generadores/u4_molde.py`, `u4_molde_grande.py`, `u4_plano_grande.py` |
| Bajar de Wikimedia Commons una foto con su crédito y su licencia. Necesita red | `python generadores/bajar_fotos.py` |

Todos los de esta tabla se pueden volver a pasar sin duplicar nada.

## Lo que no se puede comprobar desde cualquier sitio

Dos cosas necesitan salida a internet, y donde no la hay **no se dan por
buenas**: los dos scripts paran y lo dicen.

- **Los vídeos.** Que un vídeo se pueda ver sin cuenta depende de cómo lo tenga
  configurado su autor (empotrado desactivado, restricción de edad, sólo para
  miembros del canal), y eso sólo lo contesta YouTube. `comprueba_videos.py`
  clasifica los 92 en `OK`, `NO SE PUEDE EMPOTRAR`, `PIDE INICIAR SESIÓN`,
  `PRIVADO O BORRADO` y `NO SE SABE`.
- **Las fotos de Commons.** `bajar_fotos.py` se trae el fichero y, con él, el
  autor y la licencia que hay que citar debajo.

## Un repaso completo

```
for v in c1 c2 c3 c4 c5 c6 c7 c8 c9 t0 u1 u2 u3 u4 u5 u6 u7 u8 u9 u10; do
  python generadores/${v}_verifica.py | tail -1
done
python generadores/comprueba_sitio.py
python generadores/comprueba_cuentas.py
python generadores/comprueba_tests.py
python generadores/comprueba_paginas.py
python generadores/comprueba_enlaces.py
python generadores/comprueba_lecturas.py
python generadores/comprueba_curriculo.py
python generadores/comprueba_mandos.py
python generadores/comprueba_contraste.py
python generadores/comprueba_zoom.py
python generadores/comprueba_videos.py     # sólo desde una red que llegue
```

## Aviso sobre `generadores/`

Ocho scripts —los `*_build.py` y los `patch_*`— llevan dentro una ruta absoluta
a una carpeta temporal de la máquina donde se escribió el sitio, que ya no
existe. Son **generadores de un solo uso**: levantaron la primera versión de una
página que después se ha editado a mano muchas veces. No se arreglan a
propósito, porque volverlos ejecutables invita a regenerar una página y perder
todo lo escrito encima.

## Tres reglas de color, que salieron de medir

Los cuatro colores del sitio están elegidos para **rellenar**, y usarlos para
otra cosa sale mal de maneras que no se ven leyendo el código:

1. **Como texto sobre fondo claro**, el ámbar da 1,71 : 1 y el verde 3,06. Para
   eso están `--amar-texto` y `--verde-texto`, que cambian con el tema. Los de
   rellenar no se tocan: las barras y los bordes siguen igual.
2. **Como fondo de un texto**, la tinta que va encima es `--tinta-sobre`, oscura
   **en los dos temas**, porque los rellenos son saturados en el claro y pastel
   en el oscuro, y la tinta oscura gana en ambos. El texto blanco encima de una
   barra se lee en el tema claro y desaparece en el oscuro.
3. **Cuando un rótulo cruza dos fondos** —empieza dentro de una barra de ancho
   variable y acaba fuera—, ningún color acierta: lleva **halo**, o sea
   `paint-order:stroke` con un trazo del color del papel. `comprueba_contraste.py`
   no cuenta los rótulos con halo, porque el halo es la solución.
