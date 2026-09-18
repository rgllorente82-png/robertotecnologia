# Informe · Tema 9 de 4.º, segunda mitad (sesiones 5 a 8)

**Rama `c9b`.** Unidad: *Tecnología y sociedad: proyectos de servicio*.
Estado al terminar: **8 sesiones escritas, 0 pendientes**.

---

## 1 · Qué hay escrito

Las cuatro sesiones nuevas, con los títulos del encargo y no con los que había
anunciados:

| | Título corto | Título de la sesión | Escena |
|---|---|---|---|
| **S5** | Para quién, exactamente | «Sería útil» no es un requisito; quince días de agosto sí | `REQUISITOS` |
| **S6** | Lo que cuesta mantenerlo | Lo que se rompe primero es lo que nadie sabía que había que hacer | `MANTENIMIENTO` |
| **S7** | Que otro lo pueda continuar | Dentro de tres años alguien abre la caja: ¿qué encuentra? | `CONTINUAR` |
| **S8** | Entregarlo de verdad | «Funciona» no es una entrega; entre 80 y 120 mililitros, sí | `ACEPTACIÓN` |

Cada una con su reto inicial, teoría, escena interactiva propia, ficha de
práctica evaluada sobre 10 y cierre con cuatro preguntas. La S8 lleva además el
test de la unidad entera.

**Ficheros nuevos**

- `generadores/c9_escenas3.py` — escenas de la S5 y la S6.
- `generadores/c9_escenas4.py` — escenas de la S7 y la S8.
- `generadores/c9_fotos2.py` — las cuatro fotos nuevas: consulta de licencia y descarga.

**Ficheros tocados**

- `generadores/c9_build.py` — las cuatro sesiones, los títulos de la barra, el
  `desc` de la página y el docstring. Y **una línea de la primera mitad**, que
  explico en el punto 3.
- `generadores/c9_verifica.py` — de 99 comprobaciones a 226.
- `generadores/c9_mirada.py` — captura las ocho sesiones, no cuatro.
- `4eso/Tecnologia/tema9/index.html` — regenerado.

No he tocado `4eso/Tecnologia/index.html`.

---

## 2 · El hilo, y por qué ese

La primera mitad enseña a **mirar** el proyecto desde fuera (quién decide qué se
fabrica, si encaja en el sitio, cómo se defiende, cuánto cuesta). Las cuatro
nuevas van de lo único que no da ninguna otra unidad: **que el aparato salga del
aula y le sirva a alguien cuando vosotros ya no estéis**.

- **S5** recoge la quinta pregunta del sitio que la S2 dejó abierta —*¿quién
  decidió que este era el problema?*— y la convierte en método: se entrevista, se
  anota entre comillas y se traduce a números.
- **S6** arranca con la sonda de dos clavos comida por electrólisis a las tres
  semanas, y de ahí sale la vida útil en manos de otro.
- **S7** empieza cuando la etiqueta de la S6 ya no basta: hace falta manual,
  esquema y, sobre todo, **permiso**.
- **S8** cierra con lo único que no se puede ensayar: dárselo a alguien, con una
  prueba acordada de antemano.

Como el proyecto del curso ya está decidido (`PROYECTOS.md`, bloque DECIDIDO),
las cuatro aterrizan en el **riego automático** como principal y usan el aviso de
aula (B) y la lámpara (C) como las otras dos variantes. Los tres aparecen en las
escenas de la S6 y la S8; en la S5 aparecen el riego (dos destinatarios
distintos) y el aviso de aula.

---

## 3 · Lo único que he cambiado de la primera mitad

**Una línea**, y creo que no cambiarla habría dejado la página contradiciéndose:

> `S4_CIERRE`, el recuadro «Siguiente sesión». Decía que las cuatro que quedaban
> eran *«el ciclo de vida completo del aparato, diseñarlo para quien no puede
> usarlo como vosotros, mirar dónde acaba cuando se tira, y la defensa de verdad»*
> — o sea, exactamente los cuatro títulos que el encargo manda retirar por
> pisarse con las unidades 3 y 8. Lo he sustituido por el anuncio de las cuatro
> nuevas.

No he tocado nada más de las sesiones 1 a 4.

---

## 4 · Cosas de la primera mitad que creo que están mal (no las he tocado)

1. **El curso se despide en la sesión 4.** La S4 lleva un bloque titulado *«Lo
   que queda del curso»* con las seis competencias «en cristiano», un *«Por dónde
   se sigue, si esto te ha gustado»* (Bachillerato, FP, Tinkercad, repair cafés)
   y un *«Lo que no cabía»*. Con ocho sesiones, esa despedida cae **a mitad de
   unidad**. Tiene todo el sentido que viva en la S8, pero el encargo dice que no
   reescriba la primera mitad, así que la he dejado donde está y he escrito para
   la S8 un cierre **distinto y que no la repite** («Lo que queda cuando os
   vais»: las cuatro sesiones en una frase cada una). Si se mueve, habría que
   quitar de la S8 poco o nada: las dos cosas conviven, pero suena a repetición.
2. **El bloque «Lo que no cabía» de la S4 dice cosas que sí caben.** Afirma que
   se quedan fuera del curso *«la accesibilidad (diseñar para quien no ve, no oye
   o no puede apretar un botón), el residuo electrónico y dónde acaba, y el
   derecho a reparar»*. Según `CURRICULO.md`, la **unidad 8 es Sostenibilidad y
   accesibilidad** y la **unidad 3 es Materiales y ciclo de vida**. O el
   párrafo está mal, o hay que matizarlo («no cabe hacerlo en serio»).
3. **El título del vídeo de la S1 no es el real.** La página escribe *«No te
   olvides de las enfermedades olvidadas (corto documental)»*; por oEmbed el
   título es **«Note-olvides de las enfermedades olvidadas (Corto Documental)»**
   —con el juego de palabras «Note-olvides»—. El canal sí coincide (ISGlobal). Es
   una errata inocente, pero si se corrigiese sería más fiel.

Los tres vídeos de la primera mitad **siguen vivos** y su canal coincide con el
que dice la página: lo he comprobado por oEmbed (punto 7).

---

## 5 · Las cuatro escenas: qué calculan y de dónde salen los números

Ninguna enseña un número escrito a mano. Todas declaran sus constantes con su
origen, y lo que es criterio nuestro lo dice dentro de la propia escena.

### S5 · `REQUISITOS` — «De lo que dijo a lo que se mide»

Tres destinatarios con sus **frases literales** de entrevista (el huerto del
instituto, la vecina que se va quince días, el aula de infantil), cada una
etiquetada como *requisito*, *restricción* o *se comprueba*. Los mandos de la
derecha son **vuestro aparato**, y no cambian al cambiar de persona.

La cadena de cuentas, entera y a propósito:

```
superficie (m²) × lámina de riego (mm/día) → litros/día
litros guardados ÷ litros/día              → días de depósito
Wh = V × A × h                             → Wh/día (placa + bomba)
Wh guardados ÷ Wh/día                      → días de pila
altura del rótulo (mm) × 200               → metros a los que se lee
```

**Lo que enseña, y sale de la cuenta**: con la vecina se llega (6 pilas, 8 L, la
placa durmiendo → cumple 3 de 3). Con el huerto **no se llega ni con los mandos
al máximo**: 43 días × 6 L/día son **258 litros**, que no caben en ningún
depósito que se pueda poner. El mismo aparato, y no es peor: el requisito lo pone
la persona. En infantil pasa lo mismo por el otro lado: 90 días a 1,45 Wh/día son
130 Wh, o sea **36 pilas**.

⚠️ La regla **1:200** (un rótulo se lee a doscientas veces su altura) es una
**regla de dedo de señalización, criterio nuestro**, y está rotulada como tal
dentro de la escena. Sirve para ver que los dígitos de 8 mm de la pantallita no
llegan al fondo del aula; no para certificar nada. **Que la valide un humano.**

### S6 · `MANTENIMIENTO` — «Cinco años en manos de otro»

Simula los **1.825 días** siguientes a la entrega, día a día. Cada consumible
tiene su reloj; cuando uno se agota el aparato **se para** y no vuelve hasta que
alguien va, y eso tarda lo que tarde esa persona más lo que tarde el recambio.
Hay una fecha de abandono en el **día 270**.

Resultados (los cita el texto y los comprueba `c9_verifica.py`):

| Montaje | Visitas | Horas | Coste 5 años | Disponibilidad |
|---|---|---|---|---|
| Tal y como está (pilas, dos clavos, 2 L, vosotros) | 72 | 22,2 h | 333 € | **7,1 %**, y muere el día 273 |
| Con el conserje, sin tocar el diseño | 228 | 80,8 h | 1.168 € | 12,7 % |
| Enchufe + sonda capacitiva + 200 L + conserje | 5 | 1,7 h | 22,50 € | **98,1 %** |
| C · lámpara con enchufe | 0 | 0 h | 0 € | 100 % |

La moraleja sale de los propios mandos: los tres que mueven el resultado son de
**diseño** (energía, depósito, sonda), no de mantenimiento.

⚠️ **Suposiciones nuestras, declaradas en el pie de la escena**: el día 270 de
abandono («marzo del curso siguiente»), las vidas de las sondas (20 / 180 / 1.100
días), la hora de trabajo a 12 €/h y que el aparato **detecta el depósito vacío y
no arranca la bomba** (era un requisito de la S5; si no lo hiciera, habría que
sumar una bomba quemada por cada vez que se queda seco). Lo que **no** es
suposición es la electrólisis: los dos clavos con corriente permanente se comen
en semanas, y eso se ve en el taller.

### S7 · `CONTINUAR` — dos modos

**Modo A, los minutos.** Marcas lo que dejas en la caja y la escena suma lo que
le cuesta al grupo de dentro de tres años reconstruir lo que falta: **610 minutos
(10 h 10 min)** si no dejas nada, contra las **8 sesiones = 400 minutos** que
tiene para la unidad entera. No le cabe: lo tira y empieza de cero. Dejarlo todo
escrito cuesta **105 minutos**, o sea **5,8 minutos suyos por cada minuto
vuestro**. Hay una casilla —*dónde está guardado*— que **anula a todas las
demás**: un paquete perfecto en un sitio que desaparece vale cero.

**Modo B, los permisos.** Cinco licencias declaradas como seis banderas (deja
copiar / modificar / publicar / usarlo para ganar dinero, obliga a citar, obliga
a la misma licencia) y cinco cosas que querría hacer el siguiente. **La tabla no
está escrita a mano**: cada casilla se calcula evaluando la acción contra las
banderas. Y se dibuja la cadena de tres generaciones para ver dónde se corta.

Aquí encaja la licencia de la propia web: el texto manda mirar el sello
**CC BY-SA 4.0** del pie y explica qué permite exactamente, incluida la
contrapartida honrada (el SA le quita al siguiente la libertad de cerrar su
versión).

⚠️ Los minutos de cada fila son **estimación nuestra a ojo de taller**, sin
fuente, y la escena lo dice. Lo que no es estimación es la forma de la cuenta.
⚠️ La tabla de licencias es un **resumen para entenderlo, no asesoramiento
legal**, y así está rotulada. Añado dentro un «solo para entenderlo» avisando de
que CC es para obras y que el programa (MIT, GPL) y el hardware (CERN OHL) suelen
llevar otras.

### S8 · `ACEPTACIÓN` — «La prueba que acordáis antes»

Una prueba de aceptación es una **banda**, unas **repeticiones** y **cuántas
tienen que salir**. La escena dibuja dos campanas —la del aparato que está bien y
la de uno que está mal— y calcula con la normal y la binomial **las dos
probabilidades a la vez**: la de aprobar siendo bueno y la de aprobar siendo
malo. Una prueba que no puede suspender a nadie no comprueba nada.

El número que hace la sesión: con la banda 80–120 mL y un aparato que echa 100 de
media, **una medida cae dentro el 73 %** de las veces; exigir **tres de tres** es
0,73³ = **39 %**, o sea que un aparato bueno suspende seis de cada diez entregas.
Con **dos de tres** sube al **82 %** y el malo (55 mL) se queda en el **2 %**. Eso
no se acierta a ojo.

`erf` va por la aproximación 7.1.26 de Abramowitz y Stegun; el verificador lo
contrasta contra `math.erf` de Python y las diferencias no pasan de 0,6 puntos
porcentuales.

⚠️ La campana es **un modelo**, y la escena lo dice. Las σ de partida y las medias
de «el aparato que está mal» son elección nuestra.

---

## 6 · Los dos tests

El de la S4 sigue siendo `test('c9', …)`. El nuevo es **`test('c9b', …)`**, diez
preguntas sobre la **unidad entera**: cuatro de las sesiones 1 a 4 y seis de las
5 a 8. No he inventado ninguna clase que empiece por `test-`; las del módulo
empiezan por `ta`, y las de las escenas nuevas por `q5-`, `q6-`, `q7-` y `q8-`.

El verificador comprueba explícitamente que los dos tests **no comparten ni un
solo `name` de radio** (20 distintos) y que contestar uno no marca nada en el
otro.

---

## 7 · Fotos y vídeos

### Las cuatro fotos nuevas

Licencia consultada por la **API de Commons** (`generadores/c9_fotos2.py ficha`) y
**cada una abierta y mirada** antes de escribirle el pie. Ninguna es decorativa:
en las cuatro, el pie manda mirar algo concreto que se ve en la imagen.

| Sesión | Fichero | Qué se ve, y por qué está ahí | Autoría · licencia |
|---|---|---|---|
| S5 | `c9-entrevista.jpg` | Dos personas ante un portátil: una teclea y la otra **sostiene una hoja de notas a mano** y apunta mientras mira. El pie manda mirar el papel: de una entrevista se sale con el papel lleno. | Samuel Mann · **CC BY 2.0** |
| S6 | `c9-bomba-averiada.jpg` | Dos hombres reparando una bomba de mano de pozo: **tapa abierta, dos llaves fijas y un tornillo en el suelo**, y agua saliendo. Engancha con la PlayPump de la S2: la bomba de mano ganaba porque esto se puede hacer. | Tsumoses · **CC BY-SA 4.0** |
| S7 | `c9-esquema-1917.jpg` | El esquema del receptor **SCR-54** (1917): antena, tierra, inductancias con sus tomas numeradas, condensadores variables, detector, clavija. Cien años después todavía se puede montar con él. | Signal Corps, U.S. Army · **dominio público** |
| S8 | `c9-inspeccion.jpg` | Control de calidad en una fábrica de chips, años setenta: alguien mira por un microscopio para **poder decir que no**, y no es quien lo ha fabricado. | Intel Free Press · **CC BY 2.0** |

Dos notas honradas sobre estas fotos:

- La de la S5 es una prueba de usuario de **una página web**, no de un aparato.
  El pie lo dice con todas las letras y explica por qué da igual: lo que se
  enseña es la técnica, y el detalle que importa (el papel de notas) se ve.
- La de la S8 es una **inspección de fábrica**, no una entrega a un
  destinatario. El pie no finge lo contrario: lo usa para sacar las dos ideas
  que sí son de la sesión (el criterio escrito de antemano y que comprueba
  alguien distinto del que lo hizo). **Si aparece una foto mejor de una entrega
  o de una recepción, esta es la primera que cambiaría**: estuve buscando en
  Commons y no encontré ninguna decente («handover», «acceptance»,
  «commissioning» y «borehole handing over» no dan nada aprovechable).
- La foto de la S6 es **vertical (9:16)**. A todo el ancho de la columna se
  comía dos pantallas de móvil, así que su `<figure>` lleva un `max-width` de
  440 px y va centrada. **La imagen no está recortada**: se enseña entera.
  Para eso le he añadido un parámetro opcional `estilo` a la función `foto()`
  local de `c9_build.py`.

### El vídeo nuevo

Hay uno solo, en la S7:

- **«Qué son y cómo funcionan las licencias Creative Commons»**, canal
  **Ártica - Centro Cultural Online** (`8Ec4Pgs8ClA`). Título y canal
  comprobados por **oEmbed**.

⚠️ **Nadie lo ha visto entero.** Lo que está comprobado es que el vídeo existe,
que sigue disponible y que su título y su canal son los que dice la página. Que
el contenido sea bueno y adecuado para 4.º **hay que verlo**, y es lo primero
que haría un humano antes de publicar.

De paso comprobé por oEmbed **los tres vídeos de la primera mitad**: los tres
siguen vivos y su canal coincide con el de la página (ISGlobal, Insider Español,
UPV). El único detalle es la errata del título de la S1 que cuento en el punto
4.3.

La unidad queda con **ocho fotos y cuatro vídeos**.

---

## 8 · Fronteras con otras unidades

Las he hecho explícitas **dentro del texto**, para que el alumno también las vea:

- **S5 y la unidad 1** (*detectar un problema del entorno*, criterios 1.1-1.3).
  Es el roce más probable. La distinción: la U1 **detecta** el problema y planifica;
  la S5 no detecta nada, **verifica con una persona concreta** un proyecto que ya
  está construido, y el resultado es una lista de requisitos con números.
  **Que lo mire un humano**: si la U1 ya monta una entrevista de detección, hay
  que repartir quién enseña la técnica de entrevista.
- **S6 y las unidades 3 y 8** (ciclo de vida, residuo, sostenibilidad). El reto de
  la S6 dice con todas las letras que **no** va de lo que contamina ni de dónde
  acaba cuando se tira, sino de cuánto tiempo sigue vivo en manos de otro.
- **S8 y la sesión 3 de esta misma unidad** (presentar y defender), y con la U2.
  Hay un «solo para entenderlo» dedicado: la defensa es ante un tribunal que pone
  nota y se va; la entrega es ante una persona que se lleva el aparato. La
  defensa **termina** a los seis minutos, la entrega **empieza** ahí.
- **S7** no la veo pisada por nadie: en 4.º no hay unidad de herramientas
  digitales y difusión (esa es la U11 de 2.º).

---

## 9 · Lo que debería mirar un humano

1. **La despedida del curso está en la S4** y ahora cae a mitad de unidad (punto
   4.1). Decisión editorial, no la he tomado yo.
2. **El párrafo «Lo que no cabía» de la S4** contradice al currículo (punto 4.2).
3. **La regla 1:200** de legibilidad de rótulos (S5) es criterio nuestro.
4. **El día 270** como fecha de abandono (S6) y **la hora a 12 €** son
   suposiciones fuertes. Las dos están declaradas en el pie de la escena, pero
   mueven mucho el resultado.
5. **Los minutos de reconstrucción** de la S7 no tienen fuente.
6. **Las cuatro fichas de destinatario** de la actividad 5 hay que escribirlas:
   cuatro líneas por persona, una de ellas incómoda. El texto dice que las frases
   de la escena sirven de modelo, pero el papel para el aula no está hecho.
7. **Los chips de saberes** (`A.2`, `D.1`–`D.4`) los he puesto por coherencia con
   las cuatro primeras sesiones. `CURRICULO.md` **no tiene transcritos** los
   enunciados de los saberes de 4.º, así que no están contrastados contra la
   Orden de 30 de mayo de 2023.
8. **Los minutados**. S5, S6 y S7 van 10/25/20/5; la S8 va 10/25/15/10 porque
   lleva el test, igual que la S4. La S7 es la que más texto tiene: puede que los
   25 minutos de teoría se queden cortos con los dos modos de la escena.

---

## 10 · Cómo se comprueba

```
~/venv/bin/python generadores/c9_build.py      # regenera la página
~/venv/bin/python generadores/c9_verifica.py   # abre Chromium y lo pulsa todo
~/venv/bin/python generadores/c9_mirada.py     # capturas de las ocho sesiones
~/venv/bin/python generadores/c9_fotos2.py ficha   # licencias de las fotos nuevas
```

`c9_verifica.py` rehace en Python, **a partir de la definición y no copiando el
JavaScript**, las cuatro cuentas nuevas: la cadena de requisitos, la simulación
de los 1.825 días, los minutos de reconstrucción y la tabla de permisos, y la
normal con la binomial. Después pulsa los mandos de las cuatro escenas y compara
lo que se lee en pantalla con lo calculado aquí.
