# Informe · U7 de 2.º de ESO, sesiones 4, 5 y 6

Rama `tema7b`. La unidad **El ordenador y sus componentes** queda completa: las seis
sesiones escritas, seis escenas interactivas, once fotografías, seis vídeos y el test
de autoevaluación al final.

```
generadores/u7_build.py          -> 2eso/TyD/tema7/index.html   (201 KB)
generadores/u7_verifica.py       -> TODO CORRECTO
```

---

## 1. Qué hay ahora

| Sesión | Título | Escena nueva | Foto | Vídeo |
|---|---|---|---|---|
| S4 | Entrada y salida: traducir el mundo a números | conversor A/D | puertos, LDR | UPV |
| S5 | El sistema operativo: quién reparte la máquina | planificador por turnos | Hamilton, DSKY | Educar Portal |
| S6 | Diagnosticar: acotar en vez de adivinar | acotar la avería + **test** | interior de una torre | Edutin |

Reparto del tiempo: S4 y S5 siguen el molde de S1–S3 (10 + 20 + 25 + 5). S6 lleva cinco
bloques para que quepa el test: **10 reto + 15 teoría + 20 práctica + 12 test + 3 cierre = 60**.

Ficheros tocados y nuevos:

- `generadores/u7_build.py` — S4, S5, S6 y las preguntas del test. Las tres entradas
  `pendiente=True` ya no existen.
- `generadores/u7_escenas2.py` — **nuevo**. Las tres escenas, como pedía el encargo.
- `generadores/u7_verifica.py` — ampliado a las seis escenas y al test.
- `generadores/tema0_base.py` — una frase del aviso de licencia (ver §5, **hay que mirarlo**).
- `img/u7-puertos.jpg`, `u7-ldr.jpg`, `u7-hamilton.jpg`, `u7-dsky.jpg`, `u7-pc-dentro.jpg`.
- Utilidades: `oembed.py`, `commons_lote.py`, `u7_capturas.py`, `u7_texto.py` (ver §7).

---

## 2. El hilo, sesión a sesión

Ninguna sesión empieza por una definición. Cada una arranca con un encargo que el alumno
intenta y no puede, y el concepto aparece como salida a ese fracaso.

- **S4** recoge el final de S3 («dentro solo hay ceros y unos») y encarga medir la
  temperatura del aula. Las tres ideas que salen se caen porque *el mundo no va a saltos*.
  De ahí: señal analógica y digital, sensor, **muestreo**, **cuantificación**, error de
  cuantificación, actuador, periféricos y puertos. El puerto se define como un **acuerdo**,
  que es la palabra que ya se usó en S3 para el byte. Deja abierto: «hay una CPU y
  doscientos programas, ¿quién reparte?».
- **S5** encarga escribir las reglas del reparto con 200 procesos y 4 sillas. Las tres reglas
  que escribe todo el mundo fallan por lo mismo: **piden que se porten bien**. De ahí:
  proceso, planificador, multitarea con desalojo, memoria separada, ficheros, carpetas,
  permisos y controladores. Deja abierto: «y cuando una pieza falle, ¿cómo se sabe cuál?».
- **S6** no enseña ninguna pieza nueva: enseña el método. «No va» no es un síntoma, es la
  falta de información. De ahí: síntoma frente a causa, la cadena de arranque, **acotar**
  partiendo por la mitad y las cuatro reglas. Cierra con el test y con el enganche al tema
  de Internet.

Callbacks explícitos que cosen la unidad: el «acuerdo» de S3 vuelve en el puerto (S4) y en la
extensión de fichero (S5); el «doblar con cada bit» de S3 vuelve como el `log₂` del acotado
(S6); la pregunta hardware/software de S1 vuelve como la prueba que más acota (S6); los
0,35 GB por pestaña de la actividad 7.2 se comparan con una medida real en la 7.5.

---

## 3. Las tres escenas calculan, y se ha comprobado que calculan bien

No hay ni una tabla de resultados escrita a mano. El verificador **rehace cada cuenta en
Python** y la compara contra lo que la página imprime; si algún día una cuenta cambia, salta.

**S4 · el conversor.** Dibuja una onda fija —1 kHz con un armónico de 3 kHz— la muestrea
8/16/32 veces en una milésima de segundo y redondea cada medida a 2/4/8 bits. Calcula en el
momento el escalón, el **error medio y el peor de las muestras que hay en pantalla**, el
caudal en bytes/s y los MB por minuto. El verificador comprueba las nueve combinaciones
contra la misma cuenta hecha aparte, y además que el peor error nunca pase de medio escalón.

Los 3 kHz están elegidos a propósito: el ajuste más flojo son 8.000 medidas por segundo, más
del doble de 3 kHz, así que **ninguna combinación cae por debajo de Nyquist** y la escena
nunca enseña *aliasing*, que a esta edad solo confundiría. Lo que se ve empeorar es la
cuantificación, que es de lo que va la sesión.

**S5 · el planificador.** Simula de verdad el reparto por turnos de una CPU entre cinco
programas que piden 377 ms en total, cobrando cada cambio de programa. Saca el diagrama de
quién tiene la CPU, cuándo acaba cada uno y qué porcentaje del tiempo se ha dedicado a
calcular. El verificador reimplementa el mismo reparto en Python y coteja las dos cifras en
los cuatro ajustes. Sale lo que tenía que salir y no estaba escrito en ningún sitio: turno de
0,1 ms → la tecla responde en 15 ms pero solo el **66,7 %** de la máquina calcula; turno de
100 ms → el **99,9 %** calcula pero la tecla tarda **257 ms**, que ya se nota. No hay valor
bueno, y ese es el contenido de la sesión.

**S6 · acotar la avería.** Hay una pieza rota de siete, elegida al azar. La respuesta de cada
prueba **no está en una tabla**: se deduce de dónde está el corte (la señal llega hasta el
punto *j* si la pieza rota viene después). Con cada respuesta se filtra el conjunto de
sospechosos y el contador sale de ese conjunto. El verificador juega **doce averías seguidas
resolviéndolas por bisección** y comprueba que nunca hacen falta más de tres pruebas —que es
`techo(log₂ 7)`— y que la escena cuenta bien las que se han gastado.

---

## 4. Decisiones que he tomado y conviene conocer

1. **La cadena de S6 es un modelo de aula, no la secuencia real de arranque.** Siete eslabones
   en fila. En un equipo de verdad el POST comprueba la RAM antes que el disco, hay UEFI en
   vez de BIOS y la tarjeta gráfica es una rama aparte. Lo he simplificado a propósito porque
   lo que se enseña es *partir por la mitad*, no la secuencia de arranque.
2. **La pantalla está fuera de la cadena, a propósito**, y lo dice un aviso en la teoría: si
   no hay imagen todos los síntomas se ven iguales, y por eso es lo primero que se descarta.
   Me pareció más honrado sacarla y explicarlo que meterla y romper la bisección.
3. **Coste de cambiar de programa: 0,05 ms.** Es un **orden de magnitud**, no una medida. Un
   cambio de hilo puro son unos microsegundos; contando el efecto sobre la caché, decenas.
   He cogido 50 µs porque con esa cifra los cuatro botones enseñan el compromiso de verdad.
   La escena avisa de que el modelo está simplificado (un solo núcleo, nadie espera al disco,
   todos los programas valen lo mismo).
4. **Convenio del conversor: `2ⁿ − 1` escalones.** Reparto los 5 V entre los dos extremos, así
   que con 8 bits salen 255 escalones de 0,0196 V. Un conversor comercial suele describirse
   con 2ⁿ pasos de FS/2ⁿ y el código más alto valiendo FS − 1 LSB. **Las dos cosas se usan**;
   he cogido esta porque es la que sostiene la idea de «cuatro dedos, tres huecos», que es
   donde se equivocan los alumnos, y porque es la que pide la actividad 7.4. Si a Roberto le
   cuadra más el otro convenio, se cambia en una línea (`escalon = VMAX / (niveles - 1)`), pero
   habría que retocar también el paso 3 de la actividad.
5. **«El error medio» es la media de los errores absolutos de las muestras que se ven**, no el
   error cuadrático medio teórico. Es lo que dice el texto y es lo que mide.
6. **No he tocado S1, S2 ni S3** más allá de lo que obliga el §5.

---

## 5. ⚠️ Lo único que toca fuera de la U7, y hay que decidirlo

`generadores/tema0_base.py`, función `aviso_licencia()`, decía:

> «Dos son de dominio público por su antigüedad; las otras están bajo licencias Creative
> Commons compatibles con esta»

Con la foto de Margaret Hamilton, la U7 pasa a tener **tres** de dominio público, así que la
frase quedaba falsa en la página que estoy publicando. La he cambiado por una sin número
(«Algunas son de dominio público; las demás…»), que es verdad en todas las unidades.

**Consecuencia a tener en cuenta:** esa función la comparten todos los generadores, pero el
HTML ya publicado de los otros temas **conserva el texto viejo** hasta que se regenere. No he
regenerado ninguno porque no era mi encargo. La frase vieja no es falsa en esos temas, solo
es más rígida; si se quiere dejar todo igual, basta con volver a lanzar sus `*_build.py`.

---

## 6. Qué debería mirar un humano antes de publicar

**Prioridad alta**

1. **Los tres vídeos: nadie los ha visto enteros.** Título y canal están comprobados uno a uno
   con la API oEmbed de YouTube (`generadores/oembed.py`), que es lo único que la API
   garantiza. Lo que dicen por dentro, no.
   - S4 · `9GxcNyGQsuk` · *Muestreo / Cuantificacion / Codificacion | 6/84 | UPV* ·
     Universitat Politècnica de València. **Es de un canal universitario y el registro está
     por encima del de 2.º de ESO.** Lo he puesto igual porque es la fuente más solvente que
     encontré para este contenido exacto, y el pie del vídeo lo avisa. Si a Roberto le parece
     demasiado, hay alternativas más llanas de canales de aficionados al audio
     (`rundDEGXPFE`, *Hoy Grabo*), con menos garantía de autoría.
   - S5 · `vnJCudAed08` · *Microaprendizaje: ¿Qué es un sistema operativo?* · Educar Portal.
   - S6 · `pMG7x0XnCU8` · *Cómo diagnosticar problemas en mi pc* · Edutin Academy.
2. **La actividad 7.5 se ejecuta sobre el equipo del aula y yo no lo he visto.** Doy los
   atajos de Windows, GNU/Linux y ChromeOS, pero hay que comprobar contra la imagen real de
   eduAndos: que el monitor del sistema esté accesible, que los alumnos tengan carpeta
   personal, que puedan ver los permisos de un fichero de `/usr/bin` y que el intento de
   borrarlo dé el «no» que espera el ejercicio (si el aula va con cuenta de administrador, el
   paso 6 **se lo carga todo** y hay que quitarlo). El enunciado ya prohíbe cerrar procesos,
   borrar nada y usar contraseña de administrador.
3. **La foto de los puertos (S4) es de un miniordenador industrial**, no de una torre de aula:
   se ven USB, jacks de audio y un puerto serie, pero **no hay HDMI ni RJ45**, que son los que
   el alumno reconoce. El pie no engaña —enumera lo que de verdad se ve—, pero si hay manera de
   hacer una foto de la trasera de un equipo del aula, mejora mucho.

**Prioridad media**

4. **Datos con cifra o fecha.** Todos están contrastados y estos son los que sostienen el
   texto, por si se quiere revisar alguno:
   - Teléfono: 8.000 medidas por segundo y corte hacia 3.400 Hz; la decisión es de **1962**,
     con el sistema T1 de Chicago, el primer telefónico digital. CD: 44.100 medidas/s.
   - Apolo 11, **20 de julio de 1969**: alarmas **1202** y **1201** (desbordamiento del
     ejecutivo); el radar de encuentro se llevaba **alrededor del 13 %** del tiempo de
     cálculo; el reparto por prioridades tiró las tareas menos importantes y el alunizaje
     siguió. Programa del equipo de Margaret Hamilton, en el MIT.
   - La polilla del Mark II: **9 de septiembre de 1947**, panel F, relé 70. El texto avisa
     expresamente de que **la palabra «bug» ya existía** desde Edison, casi setenta años
     antes, para no repetir la leyenda de siempre.
   - S6: con 7 piezas, 6 pruebas de una en una frente a 3 por bisección; con 1.000, mil
     frente a diez (`techo(log₂ 1000) = 10`).
5. **Registro.** He cambiado un «el culo de un ordenador» por «la trasera» en el pie de la foto
   de los puertos. El resto mantiene el tono directo de S1–S3 («la máquina tonta», «el bicho
   era un bicho», «volverá el jueves»). Si en algún sitio se pasa, es fácil de bajar.
6. **En pantalla de móvil** las seis escenas encogen el texto del SVG, porque el lienzo escala
   entero. Se comporta **igual que las tres de S1–S3**, así que no es una regresión, pero si
   alguna vez se aborda, hay que abordarlas todas juntas.

**Comprobado y sin pendientes**

- Las once fotos: licencia consultada por la API de Commons y **abiertas y miradas una a una**
  antes de ponerlas (los títulos de Commons engañan). Autor y licencia están al pie de cada
  una, y ninguna se repite.
- Las seis escenas responden a todos sus controles, no hay un solo error de JavaScript ni de
  consola, y las once imágenes cargan con su tamaño real.
- El test: 10 preguntas, tres opciones cada una, **todas explican su porqué** también al
  acertar; contestándolas bien da 10 de 10 y «borrar y repetir» deja el bloque limpio.
- Numeración curricular: la web llama **tema 7** a lo que en el libro es la **U9** (el aviso de
  `CURRICULO.md` ya lo advierte). Le toca el criterio **6.1** y los saberes **D.1–D.4**, que es
  exactamente lo que ya llevaban S1–S3; las tres sesiones nuevas llevan los mismos chips.

---

## 7. Utilidades que quedan en `generadores/`

Las he escrito para este encargo y las dejo porque el siguiente las va a necesitar:

| Fichero | Para qué |
|---|---|
| `oembed.py` | Comprueba título y canal de un vídeo de YouTube. **Dice quién lo firma, no si es bueno.** |
| `commons_lote.py` | Busca y baja varias cosas de Commons espaciando las llamadas: encadenadas, Commons contesta **429** y la búsqueda se queda a medias sin avisar. |
| `u7_capturas.py` | Deja en `/tmp/u7-*.png` las escenas en varios estados, para mirarlas. Admite el ancho: `u7_capturas.py 420` para probar en móvil. |
| `u7_texto.py` | Escupe una sesión como texto plano, tal y como la lee el alumno. Es con lo que he cazado las erratas. |

---

## 8. Lo que sigue sin resolver

- **Falta la sesión de lectura en el minutado.** El reparto de `CURRICULO.md` da **6 sesiones
  + lectura** por unidad. La lectura existe (`lectura-tema7.pdf`, 30 párrafos y 10 preguntas)
  y se enlaza desde el cierre de S1, pero **no tiene sesión propia en la navegación**. No lo he
  tocado porque afecta a todas las unidades por igual, no solo a esta.
- **La actividad 7.4 y la escena de S4 comparten convenio de escalones** (§4.4). Si se cambia
  uno hay que cambiar el otro.
- No he tocado `PROYECTOS.md` ni `CURRICULO.md`: la tabla de estado de `CURRICULO.md` sigue
  marcando **U9 · pendiente**, y ahora ya no lo está. Es una línea, pero es una decisión de
  Roberto sobre cuándo se da por publicada una unidad.
