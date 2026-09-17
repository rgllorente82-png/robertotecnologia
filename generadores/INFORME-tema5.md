# Informe · Unidad 5 de 2.º de ESO · Mecanismos

Rama `tema5`, worktree aislado. Sin push, como pedía el encargo &mdash; y, esta vez,
tampoco con commit: ver el aviso de abajo.

---

## ⚠️ Lo primero, porque condiciona todo lo demás

**En esta sesión no se ha podido ejecutar ni una sola línea de código.** El entorno
deniega la ejecución de `python3` y de `node` (y de `curl`), y el acceso al disco está
limitado al worktree. Lo comprobé antes de empezar y volví a comprobarlo con un
subagente: la respuesta es siempre `This command requires approval`, y la sesión no es
interactiva, así que nadie puede aprobarlo.

Consecuencias, una por una:

| Se pedía | Estado | Por qué |
|---|---|---|
| `2eso/TyD/tema5/index.html` | ✅ hecho | escrito a mano **reproduciendo la salida del molde**, ver abajo |
| `generadores/u5_build.py` | ✅ hecho | es el fuente de verdad, pero **nunca se ha ejecutado** |
| Abrir la página y probar las escenas | ❌ **no hecho** | no hay navegador ni forma de ejecutar JavaScript |
| Lectura en PDF | ⚠️ a medias | el generador está escrito y completo; **el PDF no está creado** (necesita reportlab) |
| Voz + avatar | ⚠️ a medias | guion escrito; **el mp3 no está creado** (necesita edge-tts y red) |
| Fotos de Commons | ⚠️ a medias | licencias verificadas por API; **no se han podido descargar ni ver** |
| Vídeo de YouTube | ⚠️ a medias | título y canal verificados por oEmbed; **nadie los ha visto** |
| `git add` y `git commit` | ❌ **no hecho** | git de escritura también está denegado; mensaje listo en `COMMIT-MSG.txt` |

Todo lo que falta está **preparado para completarse con un comando**, y el generador
está escrito para que la página **nunca salga rota** por ello (ver «Piezas condicionadas»).

### Lo primero que hay que hacer al recoger esto

Comprobar que el generador reproduce exactamente el HTML que dejo escrito:

```bash
cd ~/rt          # o donde esté el worktree de la rama tema5
cp 2eso/TyD/tema5/index.html /tmp/u5-escrito-a-mano.html
~/venv/bin/python generadores/u5_build.py
diff /tmp/u5-escrito-a-mano.html 2eso/TyD/tema5/index.html
```

Ese `diff` **tiene que salir vacío**. Si sale algo, manda el generador y lo que hay que
tirar es mi HTML. Escribí el HTML a mano porque no podía ejecutar el molde, pero no lo
inventé: reproduje la salida de `unidad_base.pagina()` y comprobé mecánicamente que
coincide (ver «Cómo verifiqué el HTML sin poder ejecutarlo»).

Y **el trabajo está sin commitear**, porque `git add` y `git commit` también están
denegados en esta sesión. El mensaje ya está escrito, explicando el porqué de las
decisiones como pide el brief:

```bash
git add -A
git rm --cached COMMIT-MSG.txt        # el mensaje no tiene que entrar en el repo
git commit -F COMMIT-MSG.txt
rm COMMIT-MSG.txt
```

Sin push, claro: se recoge desde el portátil.

---

## Qué hay dentro

### Sesiones 1, 2 y 3 (las 4, 5 y 6 quedan como pendientes)

| # | Título | Escena interactiva | Práctica evaluada sobre 10 |
|---|---|---|---|
| 1 | La barra que multiplica: por qué un tubo afloja lo que tú no | Palanca con apoyo móvil, los tres géneros y el botón «mover la carga» | Regla, lápiz y monedas: **predecir antes de medir** |
| 2 | Ochenta kilos hasta el andamio: poleas y polipasto | Polea fija y polipastos de 2, 3 y 4 tramos, con la cuerda que hay que tirar | El polipasto de las dos escobas |
| 3 | El motor gira como quiere: engranajes y relación de transmisión | Tren de engranajes animado, cadena y tornillo sin fin | Desarrollo de una bici + diseñar un reductor de dos etapas |

Cada una con sus 60 minutos repartidos 10/20/25/5, bloques `copiar` («PARA LA LIBRETA»)
separados de los `entender`, y tres preguntas con respuesta desplegable en el cierre.

### El hilo, que es lo que importa

La unidad entera cuelga de **una sola idea**: un mecanismo no crea nada, **cambia una
cosa por otra**. Aparece tres veces con tres caras:

1. la palanca cambia **fuerza por recorrido**;
2. el polipasto hace lo mismo con una cuerda, que puede ser tan larga como haga falta
   (la sesión 2 nace del **límite de recorrido** de la sesión 1);
3. los engranajes cambian **velocidad por fuerza** (la sesión 3 nace de que la palanca y
   la polea van a tirones y en línea recta, y casi todo lo que se mueve hoy gira).

Ninguna sesión empieza por la definición. La 1 empieza por el tubo en la llave de la
rueda —que todo el mundo sabe que funciona y nadie sabe cuánto—, la 2 por qué es más
fácil tirar hacia abajo que hacia arriba, y la 3 por qué patinan dos ruedas lisas justo
cuando más falta hace que no patinen.

**Se cierra el título del tema.** «El músculo mueve poco y mal» se contesta en la
sesión 1 con tu propio brazo: es una palanca de tercer género que **pierde fuerza a
propósito** para ganar velocidad, y el resto del tema son formas de deshacer ese cambio.

Engancha con la unidad anterior (estructuras: lo que se construía tenía que **quedarse
quieto**) y deja abierta la siguiente (la sesión 4, transformar el movimiento).

---

## Decisiones que he tomado, y por qué

### 1. Piezas condicionadas: la página nunca sale rota

`u5_build.py` trae tres ayudantes que **solo pintan si el material existe**:

- `foto(clave)` → solo si el fichero está en `img/`;
- `video(clave)` → solo si alguien ha puesto `visto=True` (es decir, si **alguien lo ha
  visto entero**);
- `narrador()` → solo si están `audio/u5-mecanismos.mp3` y `_env_u5-mecanismos.json`.

Lo que falta se imprime al terminar, **con el comando para conseguirlo**. Hoy los tres
están apagados, así que la página no tiene ni foto rota, ni vídeo sin revisar, ni audio
fantasma. En cuanto se consiga el material y se vuelva a generar, aparecen solos.

Además, si hay narrador, el generador inyecta el CSS del avatar en la hoja de estilos
(`avatar_flat.CSS`), porque el `tema0_base.py` de este worktree **ya no lo trae dentro**
—el de la U3 publicada sí lo tenía—. Lo he hecho por fuera para no tocar un fichero
compartido con las demás unidades.

### 2. Las fotos: licencia verificada, pero **no las he visto**

El encargo avisaba de que ya se coló una imagen que no era lo que decía su título. No
puedo abrir imágenes, así que **he preferido no publicarlas**. Lo que sí está hecho:
licencia, autor y descripción comprobadas una a una contra la API de Commons el
17-sep-2026, y el pie de foto escrito. Están en el diccionario `FOTOS`.

```bash
curl -L -o img/u5-shaduf.jpeg "https://upload.wikimedia.org/wikipedia/commons/6/63/Shaduf2.jpeg"
curl -L -o img/u5-grua-haterii.jpg "https://upload.wikimedia.org/wikipedia/commons/2/2b/Tomb_of_the_Haterii_crane_relief_%28Gusman_Art_decoratif_I_pl_27%29.jpg"
curl -L -o img/u5-anticitera.jpg "https://upload.wikimedia.org/wikipedia/commons/5/5a/Antikythera_Mechanism_-_National_Archaeological_Museum%2C_Athens_by_Joy_of_Museum.jpg"
```

| Clave | Fichero | Licencia | Autor | Qué dice Commons que es |
|---|---|---|---|---|
| `shaduf` | `File:Shaduf2.jpeg` | Dominio público | G. Pearson | Un hombre sacando agua del río con un shaduf (palanca con contrapeso) |
| `haterii` | `File:Tomb of the Haterii crane relief (Gusman...)` | Dominio público | desconocido | El relieve de la grúa de la tumba de los Haterii, Via Labicana, Roma |
| `anticitera` | `File:Antikythera Mechanism - ... Joy of Museum` | CC BY-SA 4.0 | Joyofmuseums | El mecanismo en el Museo Arqueológico Nacional de Atenas |

**Hay que mirarlas antes de dejarlas puestas.** Si alguna no es lo que dice, se quita del
diccionario y ya está: el generador la salta sola.

### 3. Los vídeos: verificados de nombre, no de contenido

Comprobados con la API oEmbed de YouTube (existen y son de quien dicen ser), pero **no
los he visto**, así que van con `visto=False` y no se publican:

| Clave | ID | Título | Canal |
|---|---|---|---|
| `palanca` | `8fDOm-XJBOQ` | Ley de la palanca (mecanismos) | TECH LAPSE |
| `poleas` | `AlAxnplUNH0` | Polea fija, polea móvil y polipasto | tecnoblas2 |
| `engranajes` | `0pO6cHi3HzE` | Engranajes (Transmisión circular) | TECH LAPSE |

Verlos, y poner `visto=True` solo a los que aporten algo de verdad. Los dos de TECH LAPSE
son del mismo profesor y usan el convenio `i = z1/z2` igual que la unidad; el de
tecnoblas2 no lo he podido contrastar.

### 4. La geometría está calculada, no puesta a ojo

- **Palanca**: 200 px = 1 m, barra de 2,30 m, carga de 500 N. La ley `F·bF = R·bR` se
  resuelve en cada posición del apoyo y los brazos se miden sobre la barra en reposo. Al
  girar, la barra rota **alrededor del apoyo** (no alrededor del centro), y los tres
  géneros cambian qué elemento es el móvil y **hacia dónde apunta la flecha de la
  fuerza** (arriba en 2.º y 3.º, abajo en 1.º, como manda el equilibrio de momentos).
- **Polipasto**: cada tramo de cuerda es **vertical de verdad**. Sale por la tangente de
  una polea y entra por la de la siguiente, que está desplazada exactamente 2r; por eso
  las poleas de arriba están en 360/420 y las de abajo en 330/390. Los cuatro montajes
  tienen la topología real (n=3 lleva el cabo atado **al bloque móvil**, que es lo que
  hace impar el número de tramos). Al tirar, la carga sube `h` y la mano baja `n·h`.
- **Engranajes**: módulo constante (4 px de diámetro por diente), así que `r = m·z/2` y
  los diámetros salen proporcionales a los dientes, que es el punto del tema. El desfase
  de la rueda conducida se calcula para que **un diente de la motriz caiga siempre en un
  hueco** de la otra, y gira a `-ang·z1/z2`, o sea al revés y con la relación exacta.
  ⚠️ El **perfil** del diente es un trapecio radial, no una evolvente: es un esquema
  correcto en radio, número y sentido, pero no es un plano de taller. Lo digo porque el
  brief pide esquemas técnicamente correctos y esto es una simplificación consciente.

### 5. La práctica de las escobas lleva una trampa, a propósito

El polipasto de dos palos de escoba es espectacular y cuesta cero euros, pero **gana más
de lo que dice la fórmula**: parte de la ventaja es el rozamiento de la cuerda al
enrollarse (efecto cabrestante), no el número de tramos. En un polipasto de verdad el
rozamiento va **en contra**. Está dicho dentro de la ficha, y detectarlo es justo lo que
más puntúa. Si prefieres una práctica «limpia», habría que comprar una báscula de maleta
y un par de poleas, y entonces cambia el material.

---

## Cómo verifiqué el HTML sin poder ejecutarlo

No es «lo escribí a mano y ya veremos». Esto es lo que se comprobó, con `diff` y `grep`,
que sí están permitidos:

1. **Cabecera** (205 líneas: metadatos, JSON-LD y el CSS entero) → `diff` contra la
   cabecera de `tema3/index.html`. Sale **idéntica** salvo las cinco cosas que tienen que
   cambiar (título, descripción, canonical, `name` y `creditText` del JSON-LD) y el
   bloque CSS del avatar, que falta **porque todavía no hay narrador** y que el generador
   inyecta solo cuando lo haya.
2. **Pie, `NAV_JS` y sello CC** → `diff` contra `tema1/index.html`: idénticos salvo el
   texto del footer.
3. **Aviso de licencia** → `diff` contra `tema1`: idéntico salvo título y URL.
4. **Contenido** → `grep -Fxv -f u5_build.py` sobre el cuerpo de la página: **todas** las
   líneas de contenido del HTML aparecen literalmente en el generador. Lo único que sale
   como «no encontrado» son las líneas que **fabrica el molde** (nav, `ses-head`, rótulos
   de bloque, cabecera de ficha, `<li>` de las preguntas) y las líneas en blanco.
5. Y al revés: `grep -Fxv -f` del generador contra la página. Lo único que no está en el
   HTML es andamiaje de Python, comentarios y las plantillas condicionadas (foto, vídeo,
   narrador), que hoy no pintan nada. **Ninguna línea de contenido se quedó fuera.**
6. Este cruce **encontró un fallo real** y lo arreglé: el botón de pausa de los
   engranajes ponía el símbolo con un escape `\uXXXX` en el generador y con el carácter
   literal en el HTML. Ahora los dos usan `innerHTML` con entidades y son idénticos.
7. Estructura: 12 `<section class="bloque">` y 13 cierres (12 + el aviso de licencia), 3
   escenas con sus 3 `<script>` cerrados, todos los `getElementById` apuntan a un `id`
   que existe y no hay `id` repetidos, no quedan marcadores `@@`.
8. Sintaxis del JavaScript: llaves, paréntesis y corchetes **cuadran** en cada uno de los
   tres bloques por separado, y las comillas simples y dobles son pares. Es lo máximo que
   se puede comprobar sin intérprete.

**Esto no sustituye a abrir la página.** Lo digo claro: nadie ha visto esta unidad
renderizada. Ver la lista de comprobación de más abajo.

---

## Lo que no me cuadra (y no me he inventado)

### 1. El número de la unidad

El encargo dice **U5 = Mecanismos**. `CURRICULO.md` dice otra cosa:

| | `CURRICULO.md` | Encargo |
|---|---|---|
| U5 | Materiales de uso técnico (II) · criterios 1.2 · 2.2 | **Mecanismos** |
| U7 | **Mecanismos** · criterio 3.1 | — |

He hecho lo que pedía el encargo (contenido de mecanismos en `2eso/TyD/tema5/`) porque
es la instrucción explícita, pero **una de las dos cosas hay que corregir**: o la unidad
es la 7 y esto debería vivir en `tema7/`, o el mapa de `CURRICULO.md` está desfasado y
hay que actualizarlo. La cadena del propio `CURRICULO.md` («U6 Estructuras → U7
Mecanismos → U8 Electricidad») encaja perfectamente con esta unidad: la escribí abriendo
con las estructuras y cerrando hacia la energía. **No lo decido yo.**

### 2. Los chips curriculares

He puesto **`CE1 · 1.2`** (entender cómo funcionan las cosas antes de construir) y
**`CE3 · 3.1`** (construir con estructuras, mecanismos, electricidad y/o electrónica).
Los dos son códigos reales de `CURRICULO.md` y los dos describen lo que hacen estas
sesiones.

**No he puesto ningún chip de saberes.** El criterio 3.1 remite a `A.4 · A.5 · A.6`, y en
`CURRICULO.md` pone literalmente que *A.1 a A.5 están pendientes de transcribir de la
diapositiva 11*. Como no sé qué dicen, no los cito: la U3 podía poner `A.3` y `A.7`
porque sí están transcritos. **En cuanto estén, se añaden a `CHIPS` y se regenera.**

### 3. Los títulos de las sesiones 4, 5 y 6

Son propuesta mía, para que la navegación tenga sentido: *Transformar el movimiento*
(biela-manivela y piñón-cremallera, que son los saberes del encargo que no caben en tres
sesiones), *Montar un mecanismo* y *Repaso y test* (copiando el formato de la U3, que
cierra con test). Cámbialos sin problema: están en la lista `S` del generador.

---

## La lectura

`generadores/u5_lectura.py` → **30 párrafos numerados** (más 5 titulillos sin numerar) y
**10 preguntas**, las dos últimas de opinión razonada, como espera `lectura.py`.

Partí del borrador, pero **no lo copié**. Lo que cambié:

- ⚠️ **Dos cifras estaban mal.** El borrador decía «en las rampas egipcias hacían falta
  del orden de 50 hombres por tonelada» y «unas 30 veces más rendimiento». La estimación
  que se cita habitualmente (O'Connor, recogida en la ficha de *crane* de Wikipedia a
  partir de Vitruvio *De architectura* X.2) es **50 hombres por bloque de 2,5 t**, o sea
  unos 20 hombres por tonelada, **50 kg por persona**; y la comparación correcta es
  contra la **grúa de rueda de andar** (6.000 kg con la mitad de la cuadrilla, unos
  3.000 kg por persona), lo que da **60 veces**, no 30. Corregido en la lectura y en la
  sesión 2, y marcado como **estimación** en los dos sitios.
- El borrador daba «300 N sostenidos con un brazo» para un alumno de 2.º. Lo he bajado a
  **del orden de 250 N** y lo he puesto como orden de magnitud, no como dato. Es el
  número que usa también la escena de la palanca (el umbral verde/rojo). **Si tienes un
  dato mejor, cámbialo en los dos sitios** (`TU` en la escena, y el texto del reto).
- Añadí lo que faltaba del temario: los tres géneros, el brazo como palanca de tercer
  género, la regla de oro, cadena y correa, el rendimiento y Anticitera.

**El PDF no está generado.** Para hacerlo:

```bash
~/venv/bin/python generadores/u5_lectura.py     # deja 2eso/TyD/tema5/lectura-tema5.pdf
```

---

## La voz

Guion escrito en `generadores/u5_guion.txt` (unas 250 palabras, ~1 min 40 s). Explica el
trato de la unidad y presenta las tres sesiones. Para generarla:

```bash
~/venv/bin/python generadores/voz.py generadores/u5_guion.txt u5-mecanismos
~/venv/bin/python generadores/u5_build.py      # ahora sí monta el avatar
```

El avatar entra al final del reto de la sesión 1, que es donde acaba de quedar planteado
el problema del músculo.

---

## Checklist para el humano, antes de publicar

**Imprescindible:**

1. `~/venv/bin/python generadores/u5_build.py` y `git diff` vacío.
2. **Abrir la página en un navegador** y probar las tres escenas:
   - *Palanca*: pulsar sobre la barra mueve el elemento del medio; con el apoyo cerca de la carga
     la flecha se pone verde y `F` baja; los tres géneros cambian el elemento móvil y el
     sentido de la flecha; «Mover la carga» inclina la barra sin que nada se salga del
     lienzo (es lo que más miedo me da, porque las flechas se recortan por cálculo).
   - *Poleas*: los cuatro montajes; que la cuerda se vea **entera** y por la garganta de
     las poleas; «Tirar» sube la carga y baja la mano **n veces más**.
   - *Engranajes*: que giren encajados y al revés; que la cadena vaya en el mismo
     sentido; el tornillo sin fin; el botón de pausa (texto ⏸/▶).
   - Y la consola del navegador **sin errores**.
3. Mirar las tres fotos antes de descargarlas (o descargarlas y mirarlas).
4. Ver los tres vídeos antes de poner `visto=True`.
5. Generar el PDF de la lectura y el audio.

**Conviene:**

6. Decidir el número de unidad (punto 1 de «lo que no me cuadra»).
7. Enlazar la unidad desde `2eso/TyD/index.html`, que **no he tocado** porque está fuera
   de mi unidad. La tarjeta iría junto a la del tema 3, con este formato:

```html
    <a class="tema" href="tema5/">
      <svg class="ico" viewBox="0 0 48 48" aria-hidden="true">…icono de engranaje…</svg>
      <span class="n">Tema 5</span>
      <h3>Mecanismos</h3>
      <p>El músculo mueve poco y mal: palanca, poleas y engranajes, y el trato que hacen
         todos.</p><div class="prog"><div class="prog-barra"><i style="width:50%"></i></div><span class="prog-txt">3 de 6 sesiones publicadas</span></div>
    </a>
```

8. Revisar dos datos que doy por buenos y no he podido contrastar en fuente primaria: el
   **par de apriete de 110 N·m** de una tuerca de rueda (está dentro del rango habitual
   de 100-120) y la relación **5 cm / 35 cm** de la palanca del bíceps (es el orden de
   magnitud que se usa siempre en didáctica, pero varía por persona). Los dos van con
   «unos» o «del orden de».

---

## Nota sobre `u3_build.py`

El generador de la U3 escribe en `BASE = "C:/Users/javie/AppData/Local/Temp/rt-clone"`,
una ruta de otra máquina. El mío calcula la raíz del repo desde `__file__`, así que
funciona desde cualquier sitio. No he tocado el de la U3 —no es mi unidad—, pero si
alguien intenta regenerar la U3 en el servidor, eso va a fallar.

## Ficheros tocados

Nuevos, y nada más:

```
2eso/TyD/tema5/index.html      la unidad, 3 sesiones + 3 pendientes
generadores/u5_build.py        el generador
generadores/u5_lectura.py      la lectura (30 párrafos + 10 preguntas)
generadores/u5_guion.txt       el guion de la voz
INFORME.md                     esto
COMMIT-MSG.txt                 el mensaje del commit que no he podido hacer
```

`BRIEF.md`, `ENCARGO.md`, `LECTURA-BORRADOR.txt` y el resto de `generadores/` ya estaban
sin seguir por git en el worktree y entran en el commit con `git add -A`, como pedía el
encargo. **No se ha modificado ningún fichero de otra unidad.**
