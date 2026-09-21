# ⛔ Los generadores están desincronizados del HTML

**Antes de ejecutar ningún `uN_build.py` o `tema0_build.py`, lee esto.**

El 20-sep-2026 entró una tanda grande de trabajo (tema 1 completo, el orden
T0 → T2 → T1 → T3, diagramas, lecturas) escrita **directamente en los
`2eso/TyD/temaN/index.html`, sin tocar los generadores**. Son unas **6.500
líneas** que los generadores no saben producir.

Consecuencia: **ejecutar un build hoy borra ese trabajo sin avisar.** El tema 1
volvería a quedarse en dos sesiones de seis.

## Qué se puede ejecutar

| Generador | ¿Seguro? |
|---|---|
| `tema0_build.py` | ⚠️ Rehace el tema 0 de 2.º y de 4.º. Contiene el juego y el vídeo del bulo, pero **no** los cambios del 20-sep. |
| `u1_build.py` | ⚠️ Ya sabe **las 6 sesiones** (21-sep). Le faltan ~277 líneas de infraestructura común. |
| `u3` … `u10_build.py` | ⛔ **NO** sin comparar antes: cada uno perdería entre 350 y 900 líneas. |
| El tema 2 | No tiene generador: **el HTML es la fuente**. |

## Cómo comprobarlo antes de ejecutar

```bash
cp 2eso/TyD/temaN/index.html /tmp/antes.html
cd generadores && python3 uN_build.py && cd ..
diff /tmp/antes.html 2eso/TyD/temaN/index.html   # 0 líneas = seguro
```

## Dos cosas más

- **`u9_build.py` necesita `reportlab`** y el Python del sistema es
  *externally managed*: usar `/home/ubuntu/rt/venv/bin/python`.
- Hasta el 21-sep-2026, `tema0_build`, `u1_build`, `u3_build` y `u4_build`
  escribían en `C:/Users/javie/AppData/Local/Temp/rt-clone`. **No fallaban**:
  creaban un árbol basura y dejaban el repo intacto en silencio. Ya está
  corregido, pero explica por qué parecían idempotentes.

## La tubería, que sí existe

Un build **no basta**: el HTML publicado sale de `uN_build.py` **y después** de
los scripts de «los que ponen al día» de `COMO-SE-COMPRUEBA.md`, todos
idempotentes. En este orden:

```
ordena_indice · afina_fotos · pon_metadatos · afina_texto · pon_enlace_siguiente
afina_movil · afina_movimiento · afina_movimiento_js · afina_tintas
afina_sobre_color · afina_lectores · afina_navegador · afina_test
afina_impresion · afina_salto · afina_mandos · afina_tablas
```

Necesitan el venv y su navegador:
`/home/ubuntu/rt/venv/bin/python`, con `python -m playwright install chromium`.

Pasar la cadena recupera un tercio de la divergencia (en 4.º, de 613 líneas a
416). El resto es contenido que no está en ningún generador.

## Lo pendiente

Lo que queda fuera de los generadores son **~277 líneas por página de
infraestructura común**, no de contenido: el visor de imágenes (`.rtz-*`), el
enlace «Saltar al contenido» (`.saltar`, que `afina_salto.py` no pone porque el
molde no genera `<main>`) y el CSS de las tablas dentro de `.copiar`. Su sitio
es el molde —`unidad_base.py` / `tema0_base.py`—, no cada tema: arreglarlo ahí
cierra de una vez los 19 temas de los dos cursos.

Mientras no se haga, **manda el HTML**.
