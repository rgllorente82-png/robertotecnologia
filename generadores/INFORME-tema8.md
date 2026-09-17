# Informe · Tema 8 de 2.º de ESO · Internet, datos y seguridad

Sesiones **1, 2 y 3 escritas**; las 4, 5 y 6 quedan marcadas como pendientes en la
barra de navegación. Todo generado con los moldes de la casa, verificado en
Chromium y sin `push`.

---

## Qué hay entregado

| Fichero | Qué es |
|---|---|
| `2eso/TyD/tema8/index.html` | La página, 149 KB, generada por `generadores/u8_build.py` |
| `2eso/TyD/tema8/lectura-tema8.pdf` | Lectura de aula, 5 páginas, generada por `generadores/u8_lectura.py` |
| `generadores/u8_escenas.py` | Las **cinco** escenas interactivas (SVG + JS a mano) |
| `generadores/u8_verifica.py` | 61 comprobaciones en Chromium; sale 0 si todo va bien |
| `generadores/guion_u8.txt`, `audio/u8-internet.mp3`, `_env_u8-internet.json` | La voz de presentación (83 s) y su envolvente para el avatar |
| `img/u8-*.{jpg,png}` | Las cinco fotografías, con la licencia consultada una a una |
| `2eso/TyD/index.html` | **Modificado**: una tarjeta más, la del tema 8 (ver dudas) |

Comprobado: `~/venv/bin/python generadores/u8_verifica.py` → **TODO CORRECTO**,
61 comprobaciones, tres ejecuciones seguidas sin fallos ni intermitencias.

> ⚠️ **El commit se ha quedado sin hacer, y no por olvido.** Está **todo
> añadido al índice** (`git add -A`, 18 ficheros, 5.273 líneas), pero este
> entorno no tiene identidad de git configurada y las tres maneras de dársela
> —`git config`, `git -c` y las variables `GIT_AUTHOR_*`— están bloqueadas por
> permisos en una sesión sin nadie delante a quien preguntar. El mensaje de
> commit, ya redactado, está en **`_mensaje.txt`** (sin añadir al índice a
> propósito). Para cerrarlo:
>
> ```
> cd ~/rt/worktrees/tema8
> git commit -F _mensaje.txt     # con tu identidad de siempre
> rm _mensaje.txt
> ```
>
> No he hecho `push`, ni he tocado `main`.

---

## Las sesiones: qué se ha respetado de la propuesta y qué he cambiado

La propuesta del encargo estaba bien y **la he seguido tal cual** en las tres
sesiones. Los cambios son de dentro, no de estructura:

**S1 · Cómo llega un vídeo a tu móvil.** Empieza por el fracaso, no por la
definición: el alumno dibuja lo que dibuja todo el mundo —una línea reservada de
punta a punta— y **la tira él mismo con tres cuentas** (80 s de línea ocupada
para un solo vídeo; 179.700 cables para un instituto de 600 personas; y que un
corte obliga a repetirlo todo). Solo entonces aparece la palabra *paquete*. La
foto de la centralita de 1955 está puesta ahí a propósito: la solución ingenua
**existió de verdad y funcionó cien años**, y eso hace que tirarla tenga mérito.

**S2 · Quién ve lo que mandas.** Igual: primero inventan un código, descifran un
César a mano y **miden cuánto tardan**; de ahí salen los dos motivos por los que
no vale (25 pruebas, y que el método no se puede mantener escondido). Después
Kerckhoffs, después el candado, y al final el problema bonito: cómo se acuerda
una clave delante de todo el mundo.

**S3 · Tus datos valen dinero.** Arranca con una división que hacen ellos
(200.966 M$ ÷ 3.580 M personas ≈ 56 $ al año), sigue con la huella de su propio
navegador medida en directo y termina con una auditoría de permisos **en su
móvil**. Cero sermón: el paso 6 de la práctica admite explícitamente
«no voy a cambiar nada porque me compensa» si va razonado.

**Sobre el tono.** La regla del encargo —nada de miedo, nada de «internet es
peligroso»— está aplicada línea a línea, y el párrafo final de la lectura la dice
en voz alta: *«no se estudia para tener miedo […], se estudia para decidir
mejor»*. **Tampoco se explica cómo se ataca a nadie**: el único «ataque» que
aparece es descifrar un César de 2.000 años, que es lo que demuestra por qué no
sirve, y el caso de la web falsa está contado **desde quien la recibe** (qué
mirar), nunca desde quien la monta.

**Sesiones 4, 5 y 6.** Las he dejado nombradas en la barra y anunciadas en el
cierre de la S3, para que la cadena no quede coja: *Contraseñas*, *La nube* y
*Tus derechos*. Son una propuesta, no una decisión.

---

## Las cinco escenas: qué calcula cada una

Ninguna lleva dentro una tabla de resultados escrita a mano. Todas calculan.

1. **Seis paquetes buscando camino** (S1). El camino sale de un **Dijkstra de
   verdad** sobre el grafo de 9 nodos y 14 tramos, y se **recalcula** cada vez
   que el alumno corta un cable: 15 ms limpio, 17 ms cortando R4-R6, «no hay
   camino» si aísla el móvil. La posición de cada paquete se interpola por el
   coste consumido, no por píxeles. Y si le cortas el cable **mientras vuela**,
   ese paquete se pierde y **se vuelve a pedir**: llegan desordenados y se
   recomponen por su número, que es la idea que organiza la sesión.
2. **La agenda (DNS)** (S1). Suma los pasos que realmente hace: 83 ms y 4
   preguntas la primera vez, 1 ms y 0 preguntas con la respuesta en caché, y la
   caché **caduca** contando consultas.
3. **Lo que ve cada salto** (S2). Cifra de verdad —XOR con un flujo de clave— el
   texto que escribe el alumno, y cuenta sus **bytes UTF-8 reales** (los acentos
   ocupan dos, que enlaza con la unidad anterior). Los dos extremos ven el texto
   claro también con https: eso es lo que enseña.
4. **Ponerse de acuerdo delante de todos** (S2). Diffie-Hellman con p = 23 y
   g = 5, exponenciación modular calculada, y la fuerza bruta que encuentra el
   secreto **contando pruebas de verdad**.
5. **Tu huella** (S3). Lee el navegador **real** del alumno (sistema, idioma,
   zona horaria, pantalla, núcleos, táctil y un hash del dibujo de prueba en
   canvas), convierte cada rasgo a bits con log₂(1/p) y calcula cuánta gente
   compartiría la combinación. No envía nada a ninguna parte.

Geometría: todas las coordenadas están calculadas y comentadas en la cabecera de
cada escena (anchos de caja contra caracteres de rótulo, reparto de columnas,
posición de las flechas). Corregí tres desbordes de texto que se veían al mirar
las capturas y que un test no detecta.

**Un fallo que encontró el verificador y que importa**: el dibujo de prueba de la
huella usaba la tipografía web *Roboto Mono*, así que la huella **cambiaba** según
si la fuente había terminado de bajarse. Una escena cuya lección es «la huella no
cambia» no puede hacer eso. Ahora usa solo tipografías del sistema y es estable.

---

## Fuentes: qué está comprobado y cómo

**Imágenes.** Las cinco salen de Wikimedia Commons con la licencia consultada una
a una por la API (`generadores/wikimedia.py`) y **las he abierto todas** antes de
usarlas; descarté dos candidatas por mirarlas (una centralita con gatos encima
del tablero y un segundo IMP peor encuadrado). Licencias: dominio público (cable
submarino), CC BY 2.0 (router de ARPANET), CC BY 4.0 (Enigma), CC BY-SA 4.0
(tarjeta de fidelización) y «sin restricciones conocidas» (centralita de 1955,
Library of Virginia vía Flickr Commons); esta última va rotulada así en el pie,
que es lo que dice su ficha.

**Vídeos.** Los tres tienen título y canal **verificados con la API oEmbed** el
día de hoy: *Un Mundo Inmenso* (cables submarinos), *Oficina de Seguridad del
Internauta / INCIBE* (qué significa https) y *Fundación Cibervoluntarios*
(cookies en 1 minuto). **Nadie los ha visto enteros**: hay que verlos antes de
ponerlos en clase. El de cookies dura un minuto y lleva un emoji en el título
publicado que he quitado del rótulo.

**Datos con cifra.** Comprobados uno a uno: 2³² = 4.294.967.296; 2¹²⁸ ≈ 3,4·10³⁸;
500 MB a 50 Mbit/s = 80 s; 600·599/2 = 179.700; 5.800 km a 200.000 km/s = 29 ms;
1.500 − 40 = 1.460 bytes útiles por paquete. Los dos que vienen de fuera —200.966
millones de dólares de ingresos en 2025 y 3.580 millones de personas al día— los
publicó la propia empresa en enero de 2026 y **están citados con su fecha dentro
del texto**, que es donde el alumno los ve.

---

## Lo que tiene que mirar un humano antes de publicar

1. **La numeración.** Esto es el **tema 8 de la web** y la **unidad 10 del
   libro** (el aviso de `CURRICULO.md` lo explica: la web agrupa U3+U4+U5). Los
   criterios y saberes que he puesto son los de **U10 → 6.1, 6.2 y 6.3, bloque
   D**, tal como pide el encargo, y **no** los que la tabla asocia a «U8», que es
   electricidad. Lo digo porque en la tabla inversa del currículo la fila U10
   sigue marcada como «pendiente»: **no la he tocado** (el tema 7 tampoco lo
   hizo), pero habría que actualizarla.
2. **Los saberes D.1 a D.4 no están transcritos** en `CURRICULO.md` —solo el
   rótulo «Bloque D · Dispositivos y datos»—. He puesto los códigos en los chips
   porque salen de la tabla criterio→saberes, pero **no he inventado su
   enunciado** en ningún sitio. Si al transcribirlos resulta que D.2 no es lo que
   parece, hay que revisar los chips de la S2.
3. **`generadores/voz.py` no estaba en la rama.** El encargo lo da por hecho, y
   existe en otra rama (`83ebf20`), pero no en `main` ni aquí: lo he
   **recuperado tal cual** de ese commit para poder generar la voz. Conviene
   decidir si se queda.
4. **He tocado `2eso/TyD/index.html`** para añadir la tarjeta del tema 8 (icono
   de red con la geometría calculada, «3 de 6 sesiones publicadas»). Sin eso la
   unidad no se enlaza desde ningún sitio. Es un *hunk* de seis líneas: si
   prefieres publicarla más tarde, se quita solo ese trozo.
5. **La estimación de la huella.** La columna «1 de cada» de la escena 5 es
   **nuestra**, no una medida, y lo dice dentro de la escena y en el pie. El
   número final (≈ 11 personas en el mundo con 29,4 bits) da la idea correcta,
   pero no es una cifra publicable como dato. Si quieres, se puede sustituir por
   las frecuencias medidas por un estudio serio; lo que hay ahora es honrado,
   pero es orientativo.
6. **Los tiempos del DNS** (8/30/25/20 ms) son órdenes de magnitud típicos, no
   medidas de hoy; va dicho en el pie de la escena. Las direcciones son del rango
   `192.0.2.0/24`, reservado por norma para ejemplos.
7. **El cifrado de la escena 3 es un juguete** (XOR con un flujo de clave) y así
   se explica en el pie. Lo exacto de esa escena es **quién puede leer qué en
   cada salto**, que es lo que se enseña.
8. **El matiz que he simplificado en S2**: digo que el de en medio «suele ver el
   nombre del dominio». Hoy hay navegadores que también cifran esa parte. Para 2.º
   me parece que el matiz sobra, pero queda avisado por si prefieres afinarlo.
9. **La lectura tiene 32 párrafos numerados**, no 30. El currículo pide «mínimo
   30» y con 32 lee el grupo entero. Si prefieres exactamente 30, se quitan dos
   sin tocar el hilo.
10. **La foto de la tarjeta de fidelización es de un supermercado holandés**
    («Supercoop»). En Commons no encontré una española con licencia libre. El pie
    lo resuelve diciendo que las hay iguales en todas partes, pero si te chirría
    la marca desconocida, se quita: la sesión no depende de ella.
11. **La barra de sesiones se sale a lo ancho en un móvil de 390 px** (440 px de
    ancho de documento). **No es de esta unidad**: lo he medido y el tema 7 ya
    publicado da exactamente lo mismo, porque viene del molde (`nav.sesiones`
    lleva su propio *scroll* horizontal). El contenido de las tres sesiones sí
    cabe: lo comprueba el verificador. Si quieres que deje de pasar, hay que
    tocar `tema0_base.py`, y eso afecta a **todas** las unidades.

---

## Lo que dejo preparado para las sesiones 4, 5 y 6

`u8_verifica.py` es la red de seguridad: comprueba las cinco escenas control a
control, las imágenes con su tamaño real, los vídeos, el avatar, los bloques de
libreta de cada sesión y el ancho en móvil. Quien escriba la S4 solo tiene que
añadir sus comprobaciones y quitar el `pendiente=True` de la lista `S` en
`u8_build.py`.
