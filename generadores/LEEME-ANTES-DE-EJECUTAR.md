# ⛔ Los generadores están desincronizados del HTML

**Lanza los builds SOLO así:**

```bash
/home/ubuntu/rt/venv/bin/python generadores/build_seguro.py u5_build.py
/home/ubuntu/rt/venv/bin/python generadores/build_seguro.py --todos
```

`build_seguro.py` guarda las páginas, lanza el build que le digas, pasa la
tubería entera y compara. **Si alguna página ha perdido texto o figuras, lo
deshace** y te dice cuál y cuánto. Un build ya no puede destruir nada aunque te
equivoques de generador.

## Por qué hace falta

Parte del contenido vive **solo en los HTML** y ningún generador sabe
producirlo. El 21-sep-2026 cuatro builds de 2.º se llevaron **5.236 palabras y
17 figuras**, y las páginas siguieron compilando: 0 errores de consola y todos
los comprobadores en verde. No se ve hasta abrir la página.

Medido el 21-sep con la tubería completa puesta, esto es lo que cada build
destruiría hoy si se lanzara a pelo:

| | Palabras | Figuras |
|---|---:|---:|
| **4.º (los nueve `cN_build.py`)** | −368 | 0 |
| **2.º, temas 1, 7, 8, 9, 10** | ≈0 | 0 |
| ⛔ **2.º tema 4** (`u4_build.py`) | **−3.355** | 2 |
| ⛔ **2.º tema 3** (`u3_build.py`) | **−1.493** | 0 |
| ⛔ **2.º tema 6** (`u6_build.py`) | **−1.127** | 0 |
| ⛔ **2.º tema 5** (`u5_build.py`) | **−732** | 0 |
| El tema 2 de 2.º | no tiene generador: **el HTML es la fuente** |

Los cuatro de 2.º son los que se restauraron del 20-sep: su contenido nunca
llegó a los generadores. Con `build_seguro.py` se puede convivir con ello; para
arreglarlo de verdad hay que portar ese contenido a `u3`, `u4`, `u5` y
`u6_build.py`.

## La tubería, que sí existe

Un build **no basta**. El HTML publicado sale del build **y después** de estos
scripts, todos idempotentes, en este orden (es lo que hace `build_seguro.py`):

```
ordena_indice · afina_fotos · pon_metadatos · afina_texto · pon_enlace_siguiente
afina_movil · afina_movimiento · afina_movimiento_js · afina_tintas
afina_sobre_color · afina_lectores · afina_navegador · afina_test
afina_impresion · afina_salto · afina_mandos · afina_tablas · afina_visor
pon_diagramas
```

`pon_diagramas.py` repone las **146 piezas** que viven solo en el HTML:
diagramas, fotos, vídeos y las notas largas de los vídeos de YouTube, que el
generador produce más cortas. Sin él se pierden en cada build.

`baraja_tests.py` **no va en la cadena**: reparte al azar dónde cae la
respuesta buena, así que cada pasada da un resultado distinto, a propósito.

## El entorno

`/home/ubuntu/rt/venv/bin/python`, con `pip install -r REQUISITOS.txt` y
`python -m playwright install chromium`. El Python del sistema es *externally
managed* y no vale.

⚠️ `comprueba_videos.py` ya no sirve desde este servidor: marca los 186 vídeos
del sitio como «pide iniciar sesión». Es YouTube exigiendo sesión, no los
vídeos.

## Lo que queda

Portar a los generadores el contenido de los temas 3, 4, 5 y 6 de 2.º. Mientras
no se haga, **manda el HTML** y `build_seguro.py` es la red.
