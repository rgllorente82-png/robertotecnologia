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
| `u1_build.py` | ⛔ **NO**. Solo sabe 2 de las 6 sesiones. |
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

## Lo pendiente

Portar esas 6.500 líneas a los generadores, o decidir que el HTML pasa a ser la
fuente y retirar los generadores. Mientras no se haga, **manda el HTML**.
