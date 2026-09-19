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
