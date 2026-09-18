# Informe · segunda mitad de la unidad 2 de 4.º (Tecnología)

**Diseño y fabricación: del material al producto** · sesiones 5 a 8 · 18-sep-2026

La unidad queda con **8 sesiones escritas y 0 pendientes**. `c2_verifica.py` pasa
**420 comprobaciones, 0 fallos**, y `comprueba_paginas.py` no encuentra caracteres
rotos en ninguna de las 23 páginas del sitio.

---

## 1 · Qué hay escrito

Las cuatro sesiones siguen **una sola pieza del proyecto principal**, el
**soporte del depósito del riego automático** (variante A de `PROYECTOS.md`), y
cada sesión trabaja con las medidas que calculó la anterior:

| | Título | Lo que enseña | Escena |
|---|---|---|---|
| **S5** | El servo mide 23 y no 20 | Malla / sólido por operaciones / paramétrico. Qué es parámetro y qué se deduce. Lo que le pasa a un agujero al exportarlo a STL. | `MODELO` |
| **S6** | Se acabó el tablero con dos piezas por cortar | Despiece, plan de corte con sangría, orden de operaciones y plantillas. | `CORTE` |
| **S7** | La cota que no dibujó nadie | Cadena de cotas del montaje, cota de cierre, peor caso frente a raíz de cuadrados, orden de montaje y qué pieza se lima. | `CIERRE` |
| **S8** | «Nos ha quedado muy bien» no es una respuesta | Expediente de fabricación, control dimensional, desajuste frente a dispersión, defensa de tres minutos. | `CONTROL` |

**El hilo numérico es literal**, y eso es lo que hace que la segunda mitad no sea
cuatro temas sueltos:

- La S5 modela el soporte y calcula, del servo de 23 mm para abajo, el hueco
  (23,60), el agujero (Ø8,30), el canto (24,90), el lado del flanco (49,80) y la
  base (31,60).
- La S6 corta **esas** piezas, con el despiece del proyecto entero.
- La S7 monta el carrete en **ese** hueco de 23,60 y calcula el juego que queda.
- La S8 mide **esas seis cotas** y comprueba si el conjunto de la S7 sigue
  cerrando con el hueco que de verdad ha salido.

También se enlaza hacia atrás con la primera mitad en cada sesión: la S5 usa la
holgura de la S2 y la regla del canto de la S3; la S6 usa la sangría del láser y
las velocidades de la S4; la S7 es la acumulación de error de la S1 pero
atravesando piezas distintas; la S8 contrasta lo que pediste con la dispersión
que la S4 te prometió para cada técnica.

## 2 · Las cuatro escenas, y qué calculan

Ninguna dibuja un número escrito a mano. `c2_verifica.py` vuelve a hacer **el
mismo modelo en Python** y compara resultado por resultado.

- **`MODELO` (S5).** Dos modelos sobre los mismos parámetros: el «vivo», donde
  siete medidas son fórmulas, y el «tonto», congelado en las medidas del primer
  día. Calcula cuántas medidas se recalculan, la **interferencia** contra las
  piezas ya cortadas y, aparte, el agujero exportado a STL como polígono
  **inscrito** de N lados: Ø útil = D · cos(180°/N), la holgura que queda de
  verdad, y el **número mínimo de facetas** para que el eje pase,
  ⌈π / arccos(ds/D)⌉.
- **`CORTE` (S6).** Empaqueta el despiece con un algoritmo de **estantes**
  (la más alta primero, primer hueco que sirva), descontando la sangría entre
  pieza y pieza. Saca tableros, aprovechamiento, superficie tirada, longitud de
  corte, tiempo y euros, y compara **cortar los N grupos juntos frente a un
  tablero por grupo**. Con 10 grupos en el retal de 300 × 200: 7 tableros juntos
  frente a 10 por separado.
- **`CIERRE` (S7).** Cota de cierre, peor caso (suma de las cuatro tolerancias),
  raíz de la suma de cuadrados, y **200 montajes sorteados** con un generador
  reproducible, contando cuántos no entran y cuántos bailan. Las barras de abajo
  son la contribución de cada eslabón. Con los valores de partida: 190 de 200
  bien, 6 que no entran y 4 que bailan.
- **`CONTROL` (S8).** Fabrica las seis cotas con la dispersión de la técnica
  elegida más un desajuste sistemático, las mide, y saca desviación, porcentaje
  de tolerancia consumido y veredicto. De ahí **redacta sola** las dos frases de
  la defensa, y recalcula la cota de cierre de la S7 con el hueco medido.

El verificador nuevo comprueba, entre otras cosas, que los dos tests (`c2` y
`c2b`) no comparten ni un `name=` de radio y que **no hay ningún `id` repetido en
toda la página**.

## 3 · Decisiones que he tomado y conviene conocer

1. **El Gantt no se repite.** La unidad 1 ya tiene camino crítico, holgura y su
   propia escena. La S6 lo nombra, remite explícitamente a la unidad 1 y se queda
   con lo que es suyo: el **orden de las operaciones de fabricación** (taladrar
   antes de recortar, lo irreversible al final) y el **cuello de botella de la
   máquina compartida**. Eso deja la S6 sin escena de planificación, que es lo
   que me pedía el cuerpo; la escena es el **plan de corte**, que no lo toca
   nadie más.
2. **La S8 defiende la pieza, no el proyecto.** Lo dice en un recuadro dentro de
   la propia sesión: contar el proyecto entero es de la unidad 1 y entregarlo, de
   la 9. El expediente que se monta aquí es de **fabricación**: plano final,
   despiece y plan de corte ejecutados, hoja de ruta, control dimensional e
   incidencias.
3. **El material se nombra y se sigue.** «Contrachapado de 4 mm», «PLA», y a
   otra cosa. Ni energía ni CO₂ ni ciclo de vida: eso es de la unidad 3, y el
   cierre de la S8 lo dice apuntando allí.
4. **Corregí una incoherencia interna que me encontré al escribir la S5.** La
   cadena del modelo deducía la distancia al canto como 2 diámetros, y la regla
   de la S3 pide **2 en plástico o metal y 3 en madera o tablero**. El soporte es
   de contrachapado, así que manda el 3. Cambié el modelo (canto = 3 · Ø, flanco
   = 2 · canto) y con él las cotas de la S8 y el despiece de la S6, para que
   `flanco 50 × 50` y `base 70 × 35` sean las piezas que salen del modelo y no
   unas medidas plausibles pegadas al lado.
5. **El despiece lleva piezas de pie a propósito.** El frente de la caja es
   45 × 100 y la pletina del sensor 30 × 90. Sin eso, el botón «girar las
   piezas» no cambiaba absolutamente nada (el algoritmo de estantes es muy
   tolerante en un tablero ancho) y la escena tendría un mando que miente. Para
   que el efecto se vea hay una cuarta opción de tablero, **la tabla estrecha de
   700 × 80**: ahí esas dos piezas miden más de alto que la tabla y, si no se
   pueden girar, **no caben de ninguna manera**. El verificador comprueba las dos
   cosas: que en la tabla estrecha se caen dos piezas, y que en los tres tableros
   anchos prohibir el giro no mejora nada.
6. **La escena de la S5 usa Tinkercad como referencia pero enseña lo que
   Tinkercad no tiene.** Tinkercad no admite fórmulas, así que la sesión dice
   expresamente que allí la tabla de parámetros se lleva **en la libreta** y se
   aplica a mano, y que FreeCAD y Onshape sí las tienen. La práctica se hace en
   Tinkercad, que es lo que hay en el aula.

## 4 · Fotos y vídeos

Cinco fotos nuevas, todas de Wikimedia Commons, **abiertas y miradas una a una**,
con la licencia comprobada por la API (`c2b_fotos.py` deja el rastro):

| Fichero | Qué es | Autor · licencia |
|---|---|---|
| `c2-cad-arbol.png` | FreeCAD con el **árbol de operaciones** a la izquierda (Sketch, Pad, Pocket, Mirrored…) y el soporte terminado | Donatello29 · CC BY-SA 4.0 |
| `c2-stl-malla.png` | La misma idea exportada: una pieza convertida en **triángulos**, con el borde del hueco poligonal | Kaboldy · CC BY-SA 3.0 |
| `c2-galibo.jpg` | Un **gálibo** de latón del Muséum de Nantes | Koreller · CC BY-SA 4.0 |
| `c2-galgas.jpg` | Juego de **galgas de espesores** Moore & Wright, con los grosores legibles | R. Henrik Nilsson · CC BY 4.0 |
| `c2-cmm.jpg` | Una **máquina de medición por coordenadas** del NIST, con el mapa de desviaciones de −0,02 a +0,02 en pantalla | NIST · dominio público |

⚠️ **`c2-cad-arbol.png` es una obra derivada.** El fichero de Commons es un GIF
animado de 82 fotogramas; lo que interesa para la clase es el último, donde el
árbol ya está montado y se puede leer. Un GIF de interfaz dando vueltas en bucle
dentro de una página de teoría no deja mirar nada. He extraído ese fotograma y lo
he guardado como PNG, con su autor, su licencia CC BY-SA 4.0 y una frase en el
pie que lo dice. `c2b_fotos.py` lo reproduce. **Si esto no se considera
aceptable, dímelo y pongo el GIF entero o busco otra.**

Cuatro vídeos, **título y canal comprobados uno a uno con la API oEmbed de
YouTube** el 18-sep-2026:

- S5 · *Tutorial completo de Diseño y Modelado 3D con Tinkercad - 2022* · josemariafmTIC
- S6 · *Aplicación para optimizar cortes de placas de aglomerados y triplay. CutList Optimizer* · Viejo Roble
- S7 · *Cadenas de Cotas* · AGD Agencia de Gestión Dimensional
- S8 · *Presentación oral de un proyecto* · ULLaudiovisual - Universidad de La Laguna

⚠️ **Nadie del proyecto los ha visto enteros.** La API dice quién los firma y
cómo se llaman; no dice si son buenos. Hay que verlos antes de ponerlos en clase,
y la propia página lo avisa debajo de cada uno. El de la S8 está hecho para la
universidad y se nota en el registro: la nota del vídeo pide quedarse con la
estructura, no con el vocabulario. Si alguno no convence, se cambia el `vid` en
el diccionario `VIDEOS` de `c2_build.py` y listo.

## 5 · Lo que he visto mal y NO he tocado

**En la primera mitad (no la he reescrito, como pedía el encargo):**

1. **El tornillo M3 de la S3 está calculado sobre el diámetro nominal.** El texto
   toma A = π · 3² / 4 = 7,07 mm² y de ahí 1 700 N. El área de la sección
   resistente de un M3 real es **5,03 mm²**, y la del núcleo, unos 4,77: la cifra
   de verdad está sobre los **1 200 N**, un 40 % por debajo. Como la sesión está
   rotulada como estimación de taller y la moraleja es «el tornillo nunca es el
   problema», el error va **a favor del argumento** y no lo estropea. Pero si un
   alumno lo busca, no cuadra, y algún profesor lo va a preguntar. Lo dejo
   apuntado; arreglarlo mueve el 1 700 N de la S3, el cierre de la S3, la escena
   `UNIONES` y dos preguntas de tests.
2. **El recuadro «Lo que queda» del final de la S4 promete otra cosa de la que
   hay.** Dice que la S6 va de «quién hace qué, en qué orden y **con qué
   material**» y que la S8 es «el expediente **del proyecto** y la exposición».
   Con las fronteras que me diste, la S6 no reparte tareas (eso es la unidad 1) ni
   entra en materiales (unidad 3), y la S8 hace el expediente **de fabricación**,
   no el del proyecto. Son dos frases y están en la primera mitad, así que no las
   he tocado: se arreglan en dos minutos cuando recojas.

**En el andamiaje (esto sí lo he tocado, porque es código de comprobación y no
contenido):**

3. **`c2_verifica.py` llevaba fallando desde el commit `7ad4109`.** Ese commit
   cambió `unidad_base.lectura()` para que el molde no repita el enlace del PDF
   cuando ya está en el cuerpo, y quitó el recuadro duplicado del HTML de este
   tema. Pero la comprobación del verificador seguía exigiendo que ese recuadro
   existiera, así que daba FALLO antes de que yo tocara nada. La he cambiado para
   que compruebe lo que ahora tiene que pasar: que la lectura se ofrece
   **exactamente una vez** en toda la página.
4. **Las dos escenas nuevas con sorteo reseedaban con `s * 1103515245`.** En
   JavaScript eso se sale del entero exacto (2⁵³) para semillas de 32 bits, así
   que «otra tanda» dejaba de ser reproducible. Cambiado al multiplicador del
   propio sorteo, 1664525, que cabe de sobra.

## 6 · Dudas y cosas que debería mirar un humano

1. **El vídeo de la S8.** Es el que menos me convence de los cuatro: es
   institucional y serio, pero está pensado para universidad. Si hay algo mejor
   de nivel ESO sobre defender un trabajo técnico, se cambia.
2. **La foto del gálibo.** Es preciosa y legible, pero está en una vitrina de
   **cristalografía**, junto a un goniómetro de Carangeot. El pie lo dice tal
   cual y explica el concepto (convertir una medición en una comparación), que es
   correcto. Aun así, no es un gálibo de taller, y si prefieres uno de carpintería
   se busca.
3. **Los 200 montajes de la S7 suponen distribución uniforme.** En un taller real
   las piezas se parecen más a una campana, y entonces los extremos son todavía
   más raros. La escena lo declara en su pie y el texto lo repite; me parece la
   suposición honesta cuando no sabes nada más, pero es una decisión discutible.
4. **Qué pasa si un grupo eligió la variante B o la C.** La teoría de las cuatro
   sesiones va con el soporte del riego, que es el proyecto principal; **todas las
   prácticas** están escritas para que cada grupo meta su pieza (la tapa del aviso
   de ventilación o el brazo de la lámpara). Creo que está bien repartido, pero es
   justo lo que hay que mirar con la clase delante.
5. **`generadores/c2b_banco.py` y `c2b_busca.py` son herramientas de trabajo**, no
   contenido: el primero monta una escena suelta en `/tmp/banco.html` para no
   tener que reconstruir la unidad entera al tocar una línea de JavaScript, y el
   segundo busca en Commons. Los dejo porque ahorran tiempo la próxima vez, pero
   se pueden borrar sin que nada deje de funcionar.
6. **No he tocado `4eso/Tecnologia/index.html`**, como pedía el encargo.

## 7 · Cómo se reproduce todo

```
/home/ubuntu/venv/bin/python generadores/c2_build.py        # genera la página
/home/ubuntu/venv/bin/python generadores/c2_verifica.py     # 420 comprobaciones
/home/ubuntu/venv/bin/python generadores/c2_capturas.py     # PNG de las 8 escenas
/home/ubuntu/venv/bin/python generadores/c2b_fotos.py baja  # rebaja las fotos
/home/ubuntu/venv/bin/python generadores/comprueba_paginas.py
```

Las capturas salen en `/tmp/c2-capturas/`: cada escena con los valores de partida
y con los mandos en un extremo, que es donde se rompen las maquetas. Las he
mirado todas.
