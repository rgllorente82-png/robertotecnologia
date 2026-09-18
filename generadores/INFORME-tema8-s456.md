# Informe · Tema 8 de 2.º de ESO · Sesiones 4, 5 y 6

Las tres que faltaban, escritas. La unidad queda **completa: seis sesiones**.
Generado con los moldes de la casa, verificado en Chromium y sin `push`.

> **Sobre el nombre de este fichero.** El encargo pedía `INFORME.md`. Lo he
> puesto donde están los otros cinco y con el nombre que usan
> (`INFORME-tema6-s456.md`, `INFORME-tema7-s456.md`…), porque es exactamente
> este mismo trabajo hecho en las unidades anteriores. Si prefieres uno en la
> raíz, es mover el fichero.

---

## Qué hay entregado

| Fichero | Qué es |
|---|---|
| `generadores/u8_escenas2.py` | **Nuevo.** Las cuatro escenas de las sesiones 4-6 (1.093 líneas) |
| `generadores/u8_build.py` | **Modificado.** Las tres sesiones y las diez preguntas del test (871 → 1.838 líneas) |
| `generadores/u8_verifica.py` | **Modificado.** De 61 a **124 comprobaciones** |
| `2eso/TyD/tema8/index.html` | Regenerado: 150 KB → **278 KB**, seis sesiones |
| `img/u8-llave-2fa.jpg`, `u8-datacenter.jpg`, `u8-cintas.jpg`, `u8-aepd.jpg` | Las cuatro fotos nuevas |
| `2eso/TyD/index.html` | **Modificado**: la tarjeta del tema 8 pasa de «3 de 6» a «6 de 6» |

Comprobado: `~/venv/bin/python generadores/u8_verifica.py` → **TODO CORRECTO**,
124 comprobaciones, **tres ejecuciones seguidas** sin fallos ni intermitencias.

> ⚠️ **El commit se ha quedado sin hacer, y le pasa lo mismo que la vez
> anterior.** Está **todo añadido al índice** (`git add -A`, 11 ficheros, 4.609
> líneas), pero este entorno **sigue sin identidad de git** y las tres maneras
> de dársela —`git config`, `git -c` y las variables `GIT_AUTHOR_*`— siguen
> pidiendo una aprobación que en una sesión sin nadie delante no llega. El
> mensaje, ya redactado, está en **`_mensaje.txt`** (sin añadir al índice a
> propósito). Para cerrarlo:
>
> ```
> cd ~/rt/worktrees/tema8b
> git commit -F _mensaje.txt     # con tu identidad de siempre
> rm _mensaje.txt
> ```
>
> No he hecho `push`, ni he tocado `main`. Si esto va a pasar en cada encargo,
> lo que lo arregla de una vez es un `git config --global user.name/user.email`
> en la máquina.

---

## Las tres sesiones

Mismo método que las tres primeras: el problema primero, el fracaso de la
solución ingenua después, y el concepto **solo cuando ya hace falta**.

**S4 · La contraseña: por qué la larga gana a la rara.** Arranca con las dos
contraseñas del encargo (`Ab3$x!Qz` frente a `tres cabras en el tejado`) y hace
que el alumno **tire él mismo** la receta de toda la vida con una potencia que
cabe en la calculadora si se hace por pasos: 94² = 8.836, ese al cuadrado, y ese
al cuadrado. Sale 94⁸ = 6.095.689.385.410.816 (16 cifras) contra un 2 seguido de
34 cifras. La frase gana por **más de 10¹⁸ veces**.

La cuenta que remata es la que pedías: partiendo de ocho minúsculas, llenarla de
símbolos multiplica el montón por **29.190**; añadirle cuatro letras lo
multiplica por **456.976**. Quince veces más, y encima te la acuerdas.

De ahí sale, sin sermón, todo lo demás: si no se adivinan, **¿cómo se pierden?**
→ se escapan de las webs → **¿qué guarda entonces una web?** → la huella y la sal
→ **¿y si la repites?** → la decide la peor web de todas → **no caben en la
cabeza** → gestor → **y si aun así se pierde** → segundo factor.

**S5 · La nube: el ordenador de otro.** Empieza con un experimento de diez
segundos que se hace en clase: móvil en **modo avión** y a abrir fotos viejas.
No se abren. A partir de ahí, «está en la nube» se ve como lo que es —el nombre
de la pregunta, no la respuesta— y la sesión la contesta: un edificio, con
dirección, dueño y factura de la luz. El trato va en una tabla de dos columnas,
sin pintarlo como una trampa, porque no lo es.

El centro es lo que pedías: **sincronizar no es copia de seguridad**, y no se
afirma, se *demuestra* con la escena. Cierra con la regla 3-2-1 explicada por
qué desastre mata cada número.

**S6 · Tus derechos.** El reto es escribir el mensaje para que borren tus datos.
Sale la misma súplica en toda la clase, y se hunde con tres preguntas: si dicen
que no, ¿qué?; ¿cuándo tienen que contestar?; ¿a quién se lo cuentas? Nada, nunca
y a nadie. De ahí el concepto: **un favor no trae artículo, plazo ni árbitro; un
derecho sí**. Los cuatro derechos, el plazo, la edad, y qué se hace si te pasa
algo. Lleva **cinco bloques** en vez de cuatro (reto, teoría, práctica, test,
cierre) para que quepa el test de la unidad sin comerse la práctica.

**Sobre el tono.** En las tres sesiones no aparece ni una vez «internet es
peligroso», y el cierre lo dice en voz alta: *«quien tiene miedo no decide:
obedece»*. **Tampoco se explica cómo se ataca a nadie**: no hay ni una
herramienta, ni un método, ni un paso. Lo que hay es aritmética de cuántas
combinaciones existen —que es lo que hace cualquier medidor de contraseñas— y,
en la escena de la nube, desastres que le pasan a uno mismo (borrar, romper,
mojar, perder la cuenta). El apartado «y si te pasa algo» está escrito entero
desde **quien lo recibe**.

---

## Las cuatro escenas nuevas: qué calcula cada una

Ninguna lleva dentro una tabla de resultados escrita a mano.

1. **Cuánto aguanta** (S4). Combinaciones = alfabeto^longitud, y el tiempo es la
   mitad del espacio entre los intentos por segundo. **Todo se hace en
   logaritmos decimales**, porque 2¹²⁸ no cabe en un número de JavaScript y una
   escena que dijera `Infinity` no enseñaría nada. Las cuatro cajas del medio son
   la misma contraseña con un carácter más cada vez: el verificador comprueba que
   el tiempo se multiplica **exactamente por el alfabeto**. Las cinco barras
   salen de la misma función que lo que escribe el alumno.
2. **Lo que la web guarda de ti** (S4). Lleva un **SHA-256 escrito entero**, no
   una imitación. Las constantes no están copiadas: las saqué de su definición
   (los 32 bits decimales de las raíces cuadradas de los 8 primeros primos y de
   las cúbicas de los 64 primeros) y las comprobé contra los valores oficiales.
   El verificador compara la salida de la escena con `hashlib` en nueve textos,
   **incluidos los de 55, 56, 63, 64 y 65 bytes**, que es donde el relleno cambia
   de bloque y donde fallaría una implementación mal hecha. Si alguien calcula el
   hash de la misma palabra en otra herramienta, sale lo mismo.
3. **Dónde vive tu archivo** (S5). No es una lista de casos: cada sitio tiene
   estado y versión, y cada desastre es **una regla que se aplica a los sitios
   que cumplen una condición** (lo que está en casa, lo que está en la nube, lo
   que va sincronizado). De ahí sale sola la lección de la sesión, y el
   verificador la comprueba: **se puede cumplir la regla 3-2-1 al pie de la letra
   —3 copias, 3 soportes, 1 fuera— y perderlo todo igual con un borrado**, si las
   tres van sincronizadas. Los días sirven para lo que casi nunca se cuenta: una
   copia siempre va con retraso, y se pierde lo hecho desde la última.
4. **El calendario de tus derechos** (S6). Suma meses **con el arrastre de fin de
   mes**, que es donde falla todo el mundo: 31 de enero + 1 mes = 28 de febrero
   (29 en bisiesto), no el 3 de marzo. Comprobado en el verificador con 2026 y
   con 2024. La línea de tiempo se reparte **en proporción a los días reales**,
   no a tercios, y por eso las marcas se mueven al cambiar la fecha. La edad se
   calcula en años, meses y días.

**Geometría.** Cada escena dice en su cabecera de qué tamaño es el lienzo y cómo
se reparte, y los anchos de texto están medidos contra el gasto real de Roboto
Mono con el `letter-spacing` de `.rotulo-svg` (0,66 × el tamaño de letra). Corregí
**cinco desbordes** que vi mirando las capturas, uno de ellos —el rótulo de la
escena de la nube— solo visible en móvil, y lo cazó el verificador.

---

## Fuentes: qué está comprobado y cómo

**Los datos legales, uno a uno y en la fuente.** No de memoria:

- **14 años** para consentir en España: Ley Orgánica 3/2018, **art. 7**,
  consultado en el BOE. (El RGPD pone 16 por defecto y deja bajar hasta 13.)
- **Un mes de plazo, prorrogable otros dos** avisando: RGPD art. 12, consultado
  en la AEPD, que lo dice con esas palabras.
- **Ejercerlos es gratis**: lo dice la propia AEPD.
- **017**, línea de INCIBE, **gratuita y confidencial, de 8:00 a 23:00 todos los
  días**: consultado en incibe.es.
- **Canal prioritario** de la AEPD para retirada urgente de contenido sexual o
  violento: consultado en aepd.es.

**Imágenes.** Las cuatro salen de Wikimedia Commons, con la licencia consultada
por la API **y abiertas una a una antes de usarlas**: llave de seguridad (Tony
Webster, CC BY 2.0), centro de datos (BalticServers.com, CC BY-SA 3.0), archivo
de cintas (Linda Bartlett, dominio público) y la puerta de la AEPD (Zarateman,
CC0). Descarté dos por mirarlas: una biblioteca de cintas moderna que no se
entiende qué es, y otra de un stand de feria con un señor de espaldas.

**Vídeos.** Los tres tienen **título y canal verificados hoy con la API oEmbed**:
UOC (doble factor), Xataka (regla 3-2-1) y la **propia AEPD** (tus derechos).
**Nadie los ha visto enteros**: hay que verlos antes de ponerlos en clase.

**Las cuentas.** Comprobadas con Python antes de escribirlas: 94² = 8.836;
94⁴ = 78.074.896; 94⁸ = 6.095.689.385.410.816; 27²⁴ = un 2 con 34 cifras;
94⁸/26⁸ = 29.190; 26¹²/26⁸ = 456.976; 60 GB a 50 Mbit/s = 9.600 s = 2 h 40 min;
a 5 Mbit/s = 96.000 s ≈ 27 h.

---

## Lo que tiene que mirar un humano antes de publicar

1. ⚠️ **La lectura del tema se ha quedado corta, y es lo más importante de esta
   lista.** `lectura-tema8.pdf` tiene 32 párrafos y los escribió la sesión
   anterior: cubre **el viaje del vídeo, el candado y los datos**, o sea S1-S3.
   **No dice ni una palabra de contraseñas, de la nube ni de derechos.** Ahora
   que la unidad está completa, la lectura cubre la mitad. No la he tocado
   porque el encargo era escribir las sesiones y la lectura es material ya
   publicado, pero **habría que añadirle unos diez párrafos** (o hacer una
   segunda). Es una decisión tuya, no mía.
2. **El alfabeto de 94 y no de 95.** La escena cuenta el alfabeto que la
   contraseña **usa de verdad**; `Ab3$x!Qz` no lleva espacio, así que le salen 94
   (26 + 26 + 10 + 32) y no los 95 caracteres imprimibles de toda la vida. Puse
   94 en el texto **para que el alumno que compruebe la cuenta vea lo mismo en
   los dos sitios**; el borrador decía 95 y no cuadraba con la pantalla. Si
   prefieres la convención de 95, hay que cambiar el texto y la tabla `FAMILIAS`
   a la vez, y rehacer las dos multiplicaciones.
3. **Los tres ritmos de la escena son órdenes de magnitud NUESTROS**, no medidas:
   100/s, 100.000/s y 100.000 millones/s. Va dicho en el pie de la escena y en el
   informe. Lo que **no** depende del ritmo —y es lo que se enseña— es quién gana,
   y la práctica hace que el alumno lo compruebe cambiando los tres.
4. **La cuenta de combinaciones solo vale si la contraseña es al azar**, y eso es
   lo más fácil de enseñar mal. Está avisado **tres veces**: en un bloque de
   libreta con borde rojo, en el pie de la escena, y con el ejemplo
   *Pelusa2012*, que sale con barra larga **y marcada en rojo** a propósito, para
   que se vea que un número grande no significa que sea buena.
5. **El vídeo de la S4 es de doble factor, no de contraseñas, y es deliberado.**
   Encontré uno titulado «Contraseñas robustas OSI-INCIBE» y lo descarté por dos
   motivos: el canal **no es el de la OSI** (es una resubida de un tercero), y
   por lo que se lee de esa campaña enseña **reglas mnemotécnicas** para hacer
   contraseñas raras, que es justo lo contrario de lo que demuestra la sesión. No
   lo he visto entero, así que no afirmo qué dice: lo que digo es que **no me
   arriesgo a poner un vídeo que puede contradecir la sesión**. Si conoces uno
   bueno sobre longitud, entra donde está este.
6. **El canal prioritario de la AEPD tiene condiciones de edad** que no he metido
   en el texto para no complicarlo: su web habla de menores de **14 a 17** años
   para denunciar contenido propio o de terceros, y tiene una vía aparte para los
   más pequeños. Si en clase hay alumnado de 12-13 años —que lo habrá— conviene
   que sepas el detalle aunque no esté en la página.
7. **Los horarios del 017 y los precios pueden cambiar.** El 017 lo verifiqué hoy
   (8:00-23:00, todos los días). El precio de la nube de la práctica 8.5 («del
   orden de 10 € al mes por 2 TB») va dicho como orden de magnitud y al alumno se
   le pide que **busque él** el precio del disco, así que no envejece mal.
8. 🔎 **Un desliz que viene de la sesión 3, y que NO he tocado.** En el bloque de
   «solo para entenderlo» de la S3 dice que el RGPD «se aplica desde el 25 de mayo
   de 2018 en los **veintisiete** países». En esa fecha la Unión tenía **28**
   miembros: el Reino Unido no se fue hasta 2020. Es una palabra. No la he
   cambiado porque la S3 es material publicado y mi encargo eran las otras tres,
   pero es un cambio de dos minutos si quieres. (En mi texto de la S6 evité el
   número por esto mismo.)
9. **La foto de la AEPD es flojita de calidad** —parece hecha con un móvil de
   hace años—, pero es la única libre de la sede y la placa se lee. Está ahí por
   lo que cuenta, no por lo bonita: que un derecho tiene portal y timbre. Si te
   chirría, la sesión no depende de ella.
10. **La foto de las cintas es de los años setenta.** El pie lo dice y explica
    que hoy se sigue usando cinta pero en cartuchos. Aun así, un alumno puede
    quedarse con que las copias de seguridad son cosa antigua: merece la pena
    decirlo en voz alta en clase.
11. **Los saberes D.1 a D.4 siguen sin transcribir** en `CURRICULO.md`, como
    avisaba el informe anterior. He puesto los códigos en los chips por la tabla
    criterio→saberes, y **no me he inventado ningún enunciado**. Si al
    transcribirlos no son lo que parecen, hay que revisar los chips de las tres
    sesiones nuevas.
12. **`CURRICULO.md` sigue marcando la U10 como «pendiente»** en la tabla
    inversa, y ya no lo está: es el tema 8 de la web y está completo. No lo he
    tocado (el informe anterior lo dejó dicho igual), pero ahora sí toca.
13. **La práctica 8.4 pide contar las cuentas propias.** Está diseñada para que
    no se exponga nada —solo dos números, sin nombres, sin contraseñas, y un
    aviso arriba de no escribir ninguna de verdad ni siquiera en la escena—, pero
    el tono lo pones tú el día que se haga.

---

## Lo que dejo comprobado automáticamente

`u8_verifica.py` pasó de 61 a **124 comprobaciones**. Las nuevas que más valen no
miran píxeles:

- el **SHA-256** de la escena contra `hashlib`, en nueve textos y en los tamaños
  donde cambia el relleno;
- la escena de la nube **reproduce la lección**: cumple el 3-2-1 y lo pierde todo
  con un borrado; y con el disco fuera de la sincronización, se salva;
- **añadir un carácter multiplica el tiempo por el alfabeto**, medido;
- el **31 de enero + 1 mes**, en año normal y en bisiesto;
- el **test se corrige y da 10 de 10** marcando la correcta de cada pregunta
  (si un índice `ok` estuviera mal, saltaría aquí);
- las **seis sesiones caben a lo ancho de un móvil** de 390 px.

Además comprobé a mano que en la página **no hay identificadores repetidos** (60
`id`, ninguno duplicado, que con nueve escenas en una sola página era el fallo
fácil) y que **no he inventado ninguna clase que empiece por `test-`**: la única
que existe es el `id="test-u8"` que pone el molde.
