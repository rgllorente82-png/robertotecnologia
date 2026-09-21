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
| `u1_build.py` | ✅ Sabe **las 6 sesiones**, con el soporte de móvil (21-sep). Divergencia: 142 líneas. |
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
afina_impresion · afina_salto · afina_mandos · afina_tablas · afina_visor
pon_diagramas          <-- OBLIGATORIO despues de cualquier build
```

⛔ **`pon_diagramas.py` no es opcional.** Repone las 16 figuras —quince diagramas,
la foto del puente de folios— que solo viven en el HTML. El 21-sep-2026 se
comprobó a las malas: lanzar `u3`, `u4`, `u5` y `u6_build.py` para meter unas
fotos borró **5.236 palabras** de contenido del 20-sep, y las páginas siguieron
compilando y pasando los comprobadores como si nada. Se recuperaron del
`git show rescate-20sep:<pagina>`.

Necesitan el venv y su navegador:
`/home/ubuntu/rt/venv/bin/python`, con `python -m playwright install chromium`.

Pasar la cadena recupera un tercio de la divergencia (en 4.º, de 613 líneas a
416). El resto es contenido que no está en ningún generador.

## Lo pendiente

Queda **orden**, no contenido: `afina_tintas` y `afina_sobre_color` escriben las
variables de color en distinto orden del publicado, y el bloque de `.saltar` cae
antes o después del de «reducir el movimiento» según quién pase primero. Son
diferencias que no cambian lo que se ve, pero ensucian el `diff` y esconden las
que sí importan. Fijar ese orden deja los temas a cero.

`baraja_tests.py` **no va en la cadena**: reparte al azar dónde cae la respuesta
buena, así que cada pasada da un resultado distinto a propósito.

Mientras tanto, para el contenido **manda el HTML**.
