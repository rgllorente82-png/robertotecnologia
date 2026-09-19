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
| Caracteres rotos, NUL, UTF-8 inválido y rótulos a medias en las 27 páginas | `python generadores/comprueba_paginas.py` |
| Que las cuentas escritas en la prosa cuadren (171 ahora mismo) | `python generadores/comprueba_cuentas.py` |
| Que los enlaces internos lleven a alguna parte: ficheros, anclas y rutas absolutas resueltas contra la base de publicación, que se lee de la dirección canónica | `python generadores/comprueba_enlaces.py [--fuera]` |
| Que los tests no se pisen entre ellos, y qué unidades no tienen ninguno. Cuenta los dos moldes que hay en el sitio: `.ta` y el `.test` del tema 5 de 2.º | `python generadores/comprueba_tests.py` |
| Que los vídeos de YouTube se puedan ver, y **sin cuenta**. Necesita red: si no llega a youtube.com para y lo dice, en vez de sacar 92 «no se sabe» | `python generadores/comprueba_videos.py [--json]` |
| Las lecturas en PDF | `python generadores/comprueba_lecturas.py` |
| Las escenas de cada unidad, contra un modelo reescrito en Python **desde la definición**, nunca copiado del JavaScript de la página | `python generadores/c1_verifica.py` … `c9`, y `u1`, `u2`, `u4`…`u10` |
| Que las lecturas de aula en PDF se abran, traigan la cabecera de nombre y grupo, y sus párrafos vayan sin saltos (las 19, de los dos cursos) | `python generadores/comprueba_lecturas.py` |
| El contraste de los rótulos de las escenas, en tema claro y en oscuro. Ojo al leerlo: un rótulo blanco sobre una barra de color sale como «contraste 1» y no pasa nada —los que importan son los grises | `python generadores/comprueba_contraste.py` |

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
for v in c1 c2 c3 c4 c5 c6 c7 c8 c9 u1 u2 u4 u5 u6 u7 u8 u9 u10; do
  python generadores/${v}_verifica.py | tail -1
done
python generadores/comprueba_cuentas.py
python generadores/comprueba_tests.py
python generadores/comprueba_paginas.py
python generadores/comprueba_enlaces.py
python generadores/comprueba_lecturas.py
python generadores/comprueba_videos.py     # sólo desde una red que llegue
```

## Aviso sobre `generadores/`

Ocho scripts —los `*_build.py` y los `patch_*`— llevan dentro una ruta absoluta
a una carpeta temporal de la máquina donde se escribió el sitio, que ya no
existe. Son **generadores de un solo uso**: levantaron la primera versión de una
página que después se ha editado a mano muchas veces. No se arreglan a
propósito, porque volverlos ejecutables invita a regenerar una página y perder
todo lo escrito encima.
