# Cómo se comprueba que las páginas están bien

Todo esto se pasa sin tocar nada a mano. Si algo sale en rojo, la página tiene
un problema de verdad o el comprobador se ha quedado viejo — y las dos cosas hay
que arreglarlas, porque un comprobador que miente deja de leerse.

```
pip install -r generadores/REQUISITOS.txt
python -m playwright install chromium
```

## De una pasada, todo

| Qué mira | Cómo se lanza |
|---|---|
| Caracteres rotos, NUL, UTF-8 inválido y rótulos a medias en las 27 páginas | `python generadores/comprueba_paginas.py` |
| Que los tests de una unidad no se pisen entre ellos | `python generadores/comprueba_tests.py` |
| Que las cuentas escritas en la prosa cuadren | `python generadores/comprueba_cuentas.py` |
| Que los vídeos de YouTube se puedan ver, y sin cuenta | `python generadores/comprueba_videos.py` |
| Las escenas de cada unidad, contra su modelo | `python generadores/c1_verifica.py` … `c9`, `u2`, `u4`…`u10` |

## Lo que mantiene las páginas al día

| Qué hace | Cómo se lanza |
|---|---|
| Índices de curso y portada, contando las sesiones publicadas | `python generadores/ordena_indice.py` |
| Fotos a su tamaño, y las medidas escritas en cada `<img>` | `python generadores/afina_fotos.py` |
| Open Graph, tarjetas de compartir, sitemap y robots | `python generadores/pon_metadatos.py` |
| Títulos sin saltos de nivel y puntos suspensivos | `python generadores/afina_texto.py` |
| El molde y el plano de la tensegridad | `python generadores/u4_molde.py`, `u4_molde_grande.py`, `u4_plano_grande.py` |

Los que empiezan por `comprueba_` no tocan nada: sólo miran y devuelven 1 si hay
algo mal, así que valen para un gancho de git o para una acción automática.

## Añadidos en la revisión de contenido

| Script | Qué comprueba | Cómo se corre |
|---|---|---|
| `u1_verifica.py` | La unidad 1 de 2.º: que esté completa, que el diagrama de Gantt cuadre —rehaciendo el plan desde las duraciones, las personas y las precedencias, no comparando con una copia de sus números—, que las medidas del croquis salgan de los requisitos, y las tres escenas y el test en el navegador. | `python u1_verifica.py` |
| `comprueba_enlaces.py` | Todos los enlaces internos del sitio: ficheros que existan, anclas que existan, y rutas absolutas resueltas contra la base de publicación, que se lee de la dirección canónica. De los externos solo cuenta cuántos hay y a qué sitios van, porque comprobarlos exige red. | `python comprueba_enlaces.py [--fuera]` |
| `pon_enlace_siguiente.py` | No comprueba: **pone**. La línea de «Ir al tema N» al final del cierre de cada unidad, con el título leído del `<h1>` de la página de destino. Idempotente. | `python pon_enlace_siguiente.py` |

`comprueba_tests.py` cuenta ahora los dos moldes de test que hay en el sitio
—`.ta` y el `.test` del tema 5 de 2.º— y nombra las unidades que no tienen
ninguno, en vez de saltárselas en silencio.
