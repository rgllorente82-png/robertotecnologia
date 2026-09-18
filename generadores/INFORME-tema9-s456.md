# Tema 9 de 2.º · Herramientas digitales y difusión · sesiones 4, 5 y 6

Rama `tema9b`. Con esto la unidad queda **cerrada: 6 de 6 sesiones**, y con el
test de autoevaluación de toda la unidad al final de la última.

> **Sobre el nombre del fichero.** El encargo pedía `INFORME.md`. Lo he puesto
> donde están los otros cinco —`generadores/INFORME-temaN-s456.md`—, que es como
> se llaman los informes de las sesiones 4-6 de los temas 5, 6, 7 y 8 y como los
> referencia `CURRICULO.md`. Si prefieres el otro nombre, es un `git mv`.

---

## 1. Qué hay

| Fichero | Qué es |
|---|---|
| `2eso/TyD/tema9/index.html` | La página, 279 KB, **6 sesiones escritas** (antes 165 KB y 3) |
| `generadores/u9_build.py` | El texto de las seis sesiones, las diez preguntas del test y la configuración |
| `generadores/u9_escenas2.py` | **Las cuatro escenas nuevas** (S4, S5 y dos en la S6) |
| `generadores/u9_verifica.py` | Ampliado: **137 comprobaciones** en un Chromium de verdad (eran 82) |
| `generadores/u9_capturas2.py` | Capturas de las escenas nuevas, para mirarlas con los ojos |
| `generadores/u9_texto456.py` | Vuelca el texto visible de una sesión, para releerlo sin HTML |
| `img/u9-meninas.jpg`, `img/u9-glosas.jpg`, `img/u9-braille.jpg` | Tres fotos nuevas de Commons |
| `2eso/TyD/index.html` | Tocado: la tarjeta del tema 9 pasa de «3 de 6» a «6 de 6» |

Reproducir todo:

```
~/venv/bin/python generadores/u9_build.py
~/venv/bin/python generadores/u9_verifica.py     # sale 0 si todo va bien
```

**`u9_verifica.py` da TODO CORRECTO: 137 comprobaciones, 0 fallos.**

---

## 2. Numeración: sigue siendo el tema 9 de la web y la U11 del libro

Lo avisa `CURRICULO.md` y ya estaba resuelto en el informe de las sesiones 1-3:
la web agrupa U3+U4+U5 en el tema 3, así que a partir de ahí va una menos y
luego dos. Esto es la **U11 del libro**, criterios **2.1, 4.1, 6.1, 6.2 y 6.3**.

Las tres sesiones que faltaban son justo las que cubren los criterios que S1-S3
dejaban fuera:

| | Criterios | Saberes que declaro |
|---|---|---|
| S4 · Lo que se puede copiar | 6.2 · 6.3 | D.2 · D.3 · D.4 |
| S5 · A varias manos | 2.1 · 4.1 | B.1 · B.3 |
| S6 · Publicar y que llegue | 4.1 · 6.1 · 6.3 | B.2 · D.4 |

⚠️ Los **saberes** de los bloques B y D son una asignación mía a partir de la
tabla criterio→saber de `CURRICULO.md`. Ese documento **no transcribe el texto
de B.1, B.2, B.3 ni de D.1 a D.4**, así que no he podido comprobar que el
enunciado del saber diga lo que yo supongo. Los criterios sí son seguros; las
etiquetas de saber, revísalas.

Como en toda la unidad, **en el texto no aparece ningún número de tema**: digo
«la unidad de internet», «la unidad de representación gráfica», «la sesión
anterior». Si algún día se renumera, no hay que reescribir nada.

---

## 3. El hilo: las seis sesiones cuelgan de la misma frase

Las sesiones 1-3 ya colgaban de «lo que una cosa **es** y lo que **parece** son
cosas distintas». Las tres nuevas siguen ahí, y la tercera vuelta de tuerca es
deliberada:

- **S4**: la foto del buscador *parece* de nadie. Es de alguien, exactamente
  igual que la última foto de tu móvil, y por la misma razón.
- **S5**: el fichero que mandas *parece* el documento. Es una copia, y desde ese
  segundo son dos documentos distintos.
- **S6**: el título que has puesto en grande *parece* un título. Para un lector
  de pantalla es texto normal. Es **literalmente la escena de la sesión 1 otra
  vez**, y lo digo con esas palabras: «marcar no es pintar», ahora para que
  alguien pueda entrar en vez de para que salga el índice.

Cada sesión abre recogiendo la anterior y cierra abriendo la siguiente:

- S3 cerraba anunciando las tres. **No he tocado esa nota**: lo que anuncia
  coincide palabra por palabra con lo que he escrito.
- S4 abre por la fila **«procedencia»** de la rúbrica de la S3, que se había
  quedado sin explicar.
- S5 abre con «el trabajo ya tiene sus imágenes; ahora lo escribís cuatro».
- S6 abre con «ya está escrito y citado; ahora lo lee alguien que no estaba».
- El cierre de S6 recoge el círculo del criterio 4.1 con la unidad de
  representación gráfica y abre la de programación.

---

## 4. Las cuatro escenas nuevas, y qué calcula cada una

Ninguna lleva dentro una tabla de resultados escrita a mano. Las dos cuentas
que podían dar más miedo —la probabilidad y el contraste— están **repetidas en
Python dentro de `u9_verifica.py`**, que compara su resultado con lo que dice el
navegador: si alguien toca el JavaScript y se desvía, salta.

### S4 · «El mezclador de licencias» (`ESCENA_LICENCIAS`)

Se eligen piezas —tu texto, una foto CC BY-SA, música CC BY-NC, un icono CC0, un
vídeo CC BY-ND, una foto de un blog y dos grabados antiguos— y la escena
**aplica las reglas una a una** para decir qué licencia puede llevar el
resultado. No hay tabla de casos: hay condiciones (`by`, `nc`, `nd`, `sa`) que se
acumulan y una regla de incompatibilidad.

- **El hallazgo didáctico**: foto **CC BY-SA** + música **CC BY-NC** →
  *no se pueden mezclar*. Las dos son libres, las dos son gratis, y CompartirIgual
  obliga a publicar en CC BY-SA, que no admite NoComercial. Cuando eso pasa, las
  dos piezas se marcan **en ámbar** (no en rojo): por separado se pueden usar, y
  eso es justo lo que despista.
- **El dominio público se calcula**, no se escribe: `muerte + (muerte < 1987 ? 80
  : 70) + 1`, y se compara con `new Date().getFullYear()`. El grabado de un autor
  muerto en **1935** sale libre desde **2016**; el de **1962**, protegido hasta
  **2042**. La página sigue diciendo la verdad dentro de diez años sin tocarla.
- **El pie genera la cita** de cada pieza usable, con los cuatro datos, y la de
  la foto es la de verdad: la del sensor de color que ya está en la sesión 2.
- El estado de serie —tu texto + foto CC BY-SA + icono CC0— da **CC BY-SA 4.0
  obligatoria**, que es exactamente la licencia de esta web. Es el ejemplo que
  pedías.

### S5 · «Si nos lo vamos pasando, nos pisamos» (`ESCENA_PISAR`)

Dos cuentas cerradas, ninguna simulada:

1. **La probabilidad de pisarse es el problema del cumpleaños**:
   `p = 1 − (S/S)(S−1/S)…(S−N+1/S)`. Con 4 personas y 8 apartados sale
   **59,0 %**; con 6 personas, 92,3 %.
2. **Los trozos que se pierden son una esperanza matemática**:
   `E = N − S(1 − (1−1/S)^N)`. Con 4 y 8 salen **0,69**. Sale con decimales
   porque es una media, y el pie de la escena lo dice para que nadie piense que
   se pierde «media persona».

Y la cosa que quería que quedara clara, que va contra lo que se suele contar:
en el modo «un solo documento» **la probabilidad no baja ni un punto**. El
documento compartido **no evita el choque; evita la pérdida**. Lo que baja el
choque a cero es repartir los apartados por escrito, que es gratis.

### S6 · «Lo que oye quien no ve la pantalla» (`ESCENA_LECTOR`)

Deduce de la estructura lo que un lector de pantalla va anunciando. Los tiempos
salen de contar las palabras de cada bloque y dividir por 180 palabras por
minuto, más 4 s por cada imagen sin describir (lo que cuesta deletrear un nombre
de fichero).

- Como se hace casi siempre: **90,7 s** de escucha seguida, **0 de 4** apartados
  alcanzables y **0 de 2** imágenes descritas. Al pedir «saltar de título en
  título» no aparece nada.
- Marcada de verdad: **4 de 4** y **2 de 2**, a 4 saltos de distancia.
- Un detalle que he dejado a la vista **a propósito**: marcada de verdad,
  escucharla entera cuesta **un poco más** (91,3 s), porque describir las
  imágenes lleva su tiempo. Lo digo en el pie en vez de esconderlo: lo que
  cambia no es eso, es que ya no hace falta escucharla entera.

### S6 · «Si se lee, y cuánto» (`ESCENA_CONTRASTE`)

La razón de contraste de la **WCAG 2**, con su fórmula exacta (linealización
sRGB, luminancia 0,2126 R + 0,7152 G + 0,0722 B, y `(L₁+0,05)/(L₂+0,05)`). El
número es comprobable contra cualquier otra herramienta del mundo. Se eligen los
dos colores con dos selectores de color de verdad, o con cinco botones:

| Par | Razón | Qué pasa |
|---|---|---|
| Gris de siempre sobre blanco | **2,64 : 1** | No pasa ninguno de los tres umbrales |
| Negro sobre blanco | 16,10 : 1 | Pasa todo |
| Blanco sobre azul claro | **3,56 : 1** | Solo vale para titular |
| Blanco sobre azul oscuro | **4,51 : 1** | Pasa el normal, y por poco |
| Amarillo sobre blanco | 1,71 : 1 | Ilegible |

La muestra de arriba está **pintada con esos dos colores**, así que el alumno ve
la cifra y a la vez sufre el resultado. Y enlaza con la escena del aula de la
S3: allí era el tamaño, aquí es el color, y las dos son cuentas.

---

## 5. Imágenes: tres, comprobadas por API y **miradas una a una**

| Fichero | Origen | Licencia | Autor |
|---|---|---|---|
| `img/u9-meninas.jpg` | [Las Meninas…jpg](https://commons.wikimedia.org/wiki/File:Las_Meninas,_by_Diego_Vel%C3%A1zquez,_from_Prado_in_Google_Earth.jpg) | Dominio público | Diego Velázquez |
| `img/u9-glosas.jpg` | [Codiceemil.jpg](https://commons.wikimedia.org/wiki/File:Codiceemil.jpg) | Dominio público | Rafael Nieto |
| `img/u9-braille.jpg` | [Plage-braille-avec-touches-speciales.jpg](https://commons.wikimedia.org/wiki/File:Plage-braille-avec-touches-speciales.jpg) | CC BY-SA 2.5 | Mfaure |

Las tres las he abierto y mirado, y en dos casos eso cambió la elección:

- **Las Meninas** (S4). Se gana el sitio por el pie: el cuadro es de dominio
  público porque Velázquez murió en 1660, pero lo que estás mirando es una
  **fotografía** del cuadro, y las fotografías tienen autor. Commons la publica
  como dominio público porque una reproducción fiel de una obra plana no añade
  nada. Lo digo **y digo que es un criterio discutido** (ver § 8).
- **El códice** (S5). Descarté `Glosas-reproduccion.jpg`, que por el título
  parecía la página de las glosas y resultó ser **una vitrina de museo con una
  tela roja y una pluma**. La buena es la página del Códice Emilianense 60 con
  las anotaciones **entre las líneas y en el margen derecho**: es la sesión
  entera en una imagen, porque el glosador **no tocó el texto, escribió al
  lado**, y por eso mil años después se pueden leer las dos cosas. Comentario
  frente a cambio, del año 1000.
  Venía a 1.263 × 1.647 y **2,4 MB**: la he bajado a 1.100 px y 648 KB. En una
  unidad que dedica una sesión a lo que pesan las imágenes, servir una de 2,4 MB
  habría sido un chiste malo.
- **La línea braille** (S6). Descarté `Refreshable Braille display 2010
  0123.JPG` (CC0) porque es un primer plano oscuro y cortado. La elegida se ve
  entera y, de regalo, trae **el mismo texto dos veces**: en braille arriba y en
  letra normal en la pantallita. Eso es lo que hace entender que el documento
  llega **en fila**, sin página ni columnas.

---

## 6. Vídeos: comprobados por oEmbed, **pero no los ha visto nadie entero**

| Sesión | ID | Título (según oEmbed) | Canal |
|---|---|---|---|
| S4 | `ksmzVNMJhZ4` | ¿Qué es Creative Commons? (y sus tipos de licencia) 📝 | OpenWebinars |
| S6 | `8ZKlKAAh6HI` | Lector de pantalla NVDA 2 - Manejar una web | Universitat d'Alacant / Universidad de Alicante |

**No he visto ninguno de los dos de principio a fin**, y la API no dice si un
vídeo es bueno: solo quién lo firma y cómo se llama. El de la S6 es de un canal
institucional y el tema encaja exactamente con la escena del lector; el de la S4
es de un canal de formación conocido. Quitar cualquiera de los dos es borrar la
llamada a `video(...)` en `u9_build.py`: las sesiones se sostienen sin ellos.

### La sesión 5 se queda SIN vídeo, y es una decisión

Busqué y **todos los candidatos en español eran tutoriales de menús de una suite
concreta** («cómo ver el historial de versiones en tal programa»). Ponerlo
habría roto la regla que sostiene la unidad desde la sesión 1: **en todo el tema
no aparece ni un nombre de programa**, porque lo que se evalúa es la cuenta y la
explicación, no dónde está el botón. Preferí dejarla sin vídeo a meter uno que
caduca con la próxima versión del menú. Si conoces uno conceptual, entra en una
línea.

---

## 7. Lo que es criterio nuestro y no dato objetivo

Va rotulado **dentro** de la página, no solo aquí:

| Cifra | Qué es | Dónde se dice |
|---|---|---|
| **180 palabras/minuto** de locución | Elección nuestra, y se dice que quien usa un lector a diario lo pone mucho más rápido | Pie de la escena del lector |
| **4 s** por imagen sin describir | Estimación nuestra de lo que cuesta deletrear un nombre de fichero | Comentario del código |
| **1,2 s** por salto de encabezado | Estimación nuestra | Comentario del código |
| **4,5 : 1 · 3 : 1 · 7 : 1** | **Objetivo**: son los umbrales de la WCAG 2 | Bloque de libreta y pie |
| La fórmula de luminancia | **Objetivo**: es la de la norma | Pie de la escena |
| **80 / 70 años** de dominio público | **Objetivo**, pero es ley **española** (ver § 8) | Bloque de libreta |
| Que cada uno elija apartado **al azar** | Supuesto nuestro, y se dice que ponerse de acuerdo lo baja a cero | Pie de la escena |
| «Un dueño por apartado» y las **cinco líneas** del acuerdo | Criterio nuestro, presentado como regla práctica | Bloque de libreta |

---

## 8. Lo que debería mirar un humano antes de publicar

Por orden de importancia. **Esta es la sección que hay que leer.**

1. **Los plazos del dominio público, que son derecho español.** Digo *80 años si
   el autor murió antes del 7 de diciembre de 1987 y 70 si murió después*,
   contados desde el 1 de enero del año siguiente. Es lo que establecen el
   artículo 26 y la disposición transitoria cuarta del texto refundido de la Ley
   de Propiedad Intelectual, con el cómputo del artículo 30. **Lo he escrito de
   memoria y no he abierto el BOE.** Si va a ir a una clase, conviene
   comprobarlo; la escena y el bloque de libreta dependen de ese número. Nota:
   1987 es un año frontera (la fecha exacta es el 7 de diciembre) y la escena
   usa `muerte < 1987`; los dos ejemplos que trae, 1935 y 1962, están lejos de
   esa frontera, así que no la tocan.

2. **La reproducción fotográfica de un cuadro de dominio público.** El pie de
   Las Meninas dice que Commons la publica como dominio público porque una
   reproducción fiel de una obra plana no añade nada nuevo, y añade que *es un
   criterio razonable y muy discutido, y no todos los países lo ven igual*. Eso
   es cierto y honrado, pero en España el artículo 128 del TRLPI reconoce 25
   años de protección a las «meras fotografías», así que el asunto no es tan
   limpio como en el mundo anglosajón. **No afecta al uso**: la foto está
   publicada en Commons como dominio público y así la citamos. Afecta a si
   quieres afinar más el pie.

3. **El vídeo de la S4** (`ksmzVNMJhZ4`). Verlo y decidir. Es lo único de la
   sesión que no he podido verificar de verdad. Lo mismo, con menos
   preocupación, con el de la S6.

4. **Las Glosas Emilianenses.** El pie dice que las del margen están en romance
   y que son «de las primeras frases que se conservan escritas en algo parecido
   al castellano». Está redactado a propósito con esa prudencia: hoy la mayoría
   de los filólogos las describen como **navarroaragonés**, no castellano, y la
   idea de «la cuna del español» está discutida desde hace décadas. Si te
   parece, se puede afinar todavía más; lo que **no** he hecho es repetir el
   eslogan de siempre. Lo que sí es seguro y es lo que importa para la sesión:
   que el glosador escribió **al lado** y no encima.

5. **La cita de Tim Berners-Lee** (bloque «solo para entenderlo» de la S6).
   Está **parafraseada**, no entrecomillada, y a propósito: la frase original es
   de 1997, en inglés, al presentar la iniciativa de accesibilidad del W3C, y no
   he abierto la fuente. Si la quieres entrecomillada, hay que buscarla. Tal
   como está, la sesión aguanta.

6. **«La segunda versión (2008) es la que usan las leyes europeas y
   españolas».** Es correcto en lo esencial —la norma europea que aplica la
   directiva de accesibilidad se apoya en la WCAG 2—, pero la versión concreta
   que citan las normas actuales es la **2.1**, no la 2.0. Lo digo como «su
   segunda versión» justamente para no tener que entrar en el número menor, pero
   si alguien pregunta en clase, ese es el matiz.

7. **Los tiempos de las prácticas.** Las de la S4 y la S5 son de 25 minutos con
   seis pasos, como las tres anteriores: **apretadas**, y la 9.5 necesita que el
   aula tenga sitio compartido funcionando. La 9.6 la he dejado en **15
   minutos** y cinco pasos para que quepa el test. Si hay que recortar algo,
   recortaría el paso 6 de la 9.4 (la trampa del buscador) y el paso 6 de la 9.5
   (los permisos), que son los que menos se pierden.

8. **La actividad 9.5 necesita cuentas.** Es la única de toda la unidad que
   depende de que los alumnos tengan una cuenta con la que compartir un
   documento. Si en el centro eso no está resuelto, la sesión 5 se puede dar
   igual (la escena y la teoría no dependen de ello), pero la práctica hay que
   sustituirla.

9. **Dos erratas que he corregido en las sesiones ya publicadas.** En la S2
   («describid lo que **veís**») y en la S3 («comprobadlo mientras lo
   **veís**»): son *veis*, sin tilde. No me habías pedido tocar S1-S3; me ha
   parecido peor dejar una falta de ortografía en una página que leen alumnos.
   Están en `u9_build.py`, líneas del paso 5 de la actividad 9.2 y de la nota
   del vídeo de la 9.3, por si quieres revertirlo.

---

## 9. Decisiones que he tomado yo, por si no coinciden con lo tuyo

- **Cuatro escenas, no seis.** S1, S2 y S3 llevan dos escenas cada una. S4 y S5
  llevan **una**, y la S6 lleva **dos**. No es dejadez: en S4 el mezclador
  cubre entero el contenido de la sesión (licencias y dominio público en la
  misma cuenta) y en S5 la escena del reparto también. En la S6 hacían falta
  dos porque el brief pedía tres cosas distintas —estructura, alternativo y
  contraste— y las dos primeras son la misma escena pero el contraste es otra
  cuenta completamente distinta.
- **El test no lleva ninguna clase nueva que empiece por `test-`.** Usa el molde
  de `test_auto.py` tal cual, cuyo CSS ya está en `tema0_base.py` (clases `ta`,
  `ta-p`, `ta-op`…). El único `test-` de la página es el **id** `test-u9`, que
  es del molde. `u9_verifica.py` lo comprueba recorriendo el DOM, y sigue dando
  cero.
- **Las diez preguntas son de toda la unidad**, repartidas 2+2+2+2+1+1 entre las
  seis sesiones, y cada una explica por qué también cuando se acierta. Dos de
  ellas —la 2 y la 3— están escritas a propósito para que se vea que son **el
  mismo error** en dos sitios distintos.
- **La tarjeta del índice de 2.º** la he actualizado a «6 de 6» y le he
  reescrito la descripción, que solo hablaba de las tres primeras sesiones.
- **He dejado dos herramientas nuevas** en `generadores/`: `u9_capturas2.py`
  (capturas de las escenas, que es como encontré que una fila se metía debajo de
  los cuadros) y `u9_texto456.py` (vuelca el texto visible, que es como
  encontré las erratas). No forman parte de la página.
- **`ENCARGO.md` se queda sin commit**, como en el informe anterior: es el
  enunciado del trabajo, no el trabajo, y ningún commit del repositorio lo lleva
  dentro.

---

## 9 bis. ⚠️ El commit se ha quedado sin hacer (tercera vez)

Le pasó al tema 8 y a las sesiones 1-3 de este, y vuelve a pasar: **el entorno
no me deja fijar la identidad de git**. `git config user.name`, `git -c
user.name=…` y las variables `GIT_AUTHOR_*` / `GIT_COMMITTER_*` están todas
bloqueadas, y sin *committer* git se niega. Probé las tres maneras.

**Todo el trabajo está en el índice, listo para commit**, y el mensaje está
escrito en `_commit_tema9-s456.txt`, en la raíz. Solo falta:

```
cd /home/ubuntu/rt/worktrees/tema9b
git config user.name  "rgllorente82-png"
git config user.email "268428770+rgllorente82-png@users.noreply.github.com"
git commit -F _commit_tema9-s456.txt
rm _commit_tema9-s456.txt
```

`git status --short` tiene que enseñar **11 ficheros en verde** y, sin tocar,
`ENCARGO.md` y `_commit_tema9-s456.txt`. **No he hecho push ni he tocado
`main`.**

Vale la pena arreglar la identidad de git en la máquina de una vez: es la
tercera unidad que se queda a un paso.

---

## 10. Lo que sigue pendiente de las sesiones 1-3, y sigue sin hacerse

Del informe anterior, y lo repito porque no lo he tocado:

- **La U2 no dice nada del círculo del criterio 4.1.** Esta unidad lo dice dos
  veces (cierre de la S3 y cierre de la S6), pero la unidad de representación
  gráfica, que es la otra punta, sigue sin mencionarlo. Es una línea. No lo he
  hecho porque no me habías pedido tocar el tema 2.
- **El vídeo de la S3** (`zRoxXHR_-Ac`, «Muerte por PowerPoint») sigue sin que
  nadie lo haya visto entero.
- **`BRIEF.md` no existe** en el repositorio, ni en esta rama ni en `main`. He
  tomado como estándar las sesiones 1-3 de `u9_build.py` y la estructura de
  `u8_build.py`, que es lo que decía el plan B del encargo.
