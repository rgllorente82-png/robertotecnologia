# Materiales de Tecnología

Material de aula para **Tecnología y Digitalización de 2.º de ESO** y
**Tecnología de 4.º de ESO**, publicado como un sitio estático:

**https://rgllorente82-png.github.io/robertotecnologia/**

Lo escribe Roberto P. García Llorente, profesor de Tecnología en Educación
Secundaria, y está abierto para que lo use, lo adapte y lo corrija quien quiera.

## Qué hay

| | Unidades | Sesiones | Estado |
|---|---|---|---|
| **2.º de ESO** · Tecnología y Digitalización | 10 temas, más un tema 0 de presentación | 6 de una hora cada uno | publicado entero |
| **4.º de ESO** · Tecnología | 9 temas, más un tema 0 | 8 de una hora cada uno | publicado entero |

Además: **19 lecturas de aula en PDF**, una por unidad, de treinta párrafos
numerados y diez preguntas; y los **moldes recortables** de la tensegridad de
cartón del tema de estructuras.

## Cómo está hecho

Una unidad es **una sola página HTML que se basta a sí misma**: el CSS, el
JavaScript y los dibujos van dentro. No hay framework, ni paso de compilación,
ni nada que instalar para leerla. Se abre con doble clic desde una memoria USB y
funciona igual que en la web, con o sin conexión —salvo los vídeos, que son de
YouTube y están enlazados, no copiados—.

Cada sesión dura **una hora de clase** y se reparte en bloques con sus minutos
escritos: reto inicial, teoría, práctica y cierre. Las actividades traen su
rúbrica. Y casi todas las sesiones llevan una **escena interactiva**: un dibujo
que se mueve al tocarlo —una polea que sube, un diagrama de Gantt que se
reparte, un circuito que se mide— dibujado en SVG desde el propio navegador.

El sitio se ve en claro y en oscuro, se lee en un móvil sin desplazarse a lo
ancho, y respeta el ajuste de accesibilidad de «reducir el movimiento». El pie
de cada escena es una región viva, así que un lector de pantalla anuncia la
explicación al pulsar un botón: para quien no ve el dibujo, ese pie **es** la
escena.

## Cómo se comprueba que está bien

En [`generadores/`](generadores/) hay más de doscientos scripts. La mayoría son
generadores de un solo uso, los que levantaron la primera versión de cada página
y que después se ha editado a mano; los que se siguen usando están listados abajo.

Los que importan son los **verificadores**, y tienen una regla: un verificador
**no compara con una copia de los números de la página**, sino que vuelve a
calcularlos desde la definición del problema, en Python, y los contrasta con lo
que la página dibuja de verdad en un navegador. Si no coinciden, uno de los dos
está mal —y unas cuantas veces ha sido el verificador—.

Las **diecinueve unidades y los dos temas 0** —las veintiuna páginas de
tema— tienen su verificador. Se
comprueban además las cuentas escritas en la prosa, los enlaces internos, los
caracteres, los tests, las lecturas en PDF, el contraste de los rótulos, que el
texto se pueda agrandar al 200 % sin que nada se corte, y que los códigos de
criterios y saberes de cada unidad existan de verdad en el currículo.

→ [`generadores/COMO-SE-COMPRUEBA.md`](generadores/COMO-SE-COMPRUEBA.md)

## Qué documenta el resto

- [`CURRICULO.md`](CURRICULO.md) — competencias, criterios y saberes de cada
  curso, y qué unidad cubre cada cosa.
- [`PROYECTOS.md`](PROYECTOS.md) — los proyectos que se pueden construir de
  verdad en un aula, ya filtrados por material, tiempo y manos disponibles.

## Licencia

Los **textos, los dibujos y el código** son obra propia y se publican bajo
[**CC BY-SA 4.0**](https://creativecommons.org/licenses/by-sa/4.0/deed.es):
cópialo, adáptalo y redistribúyelo, incluso con fines comerciales, citando la
autoría, indicando si lo has modificado y publicando tus versiones derivadas con
esta misma licencia.

**No cubre las fotografías**, que proceden de Wikimedia Commons y conservan su
propia licencia, indicada bajo cada una; ni los vídeos, que son de sus autores y
están enlazados; ni las tipografías, de Google Fonts.

## Lo que falta

Tres cosas, y las tres necesitan una red que llegue a donde este repositorio no
llega:

- **Comprobar uno a uno los 92 vídeos de YouTube.** Están empotrados sin cookies
  de seguimiento y todos traen debajo su enlace directo, pero que un vídeo
  concreto se deje ver sin cuenta depende de cómo lo tenga configurado su autor
  —empotrado desactivado, restricción de edad, sólo para miembros del canal—, y
  eso sólo lo contesta YouTube. Lo clasifica `comprueba_videos.py`.
- **Fotografías para el tema 3 de 2.º**, el de materiales, que es la única unidad
  sin ninguna. Las trae `bajar_fotos.py` de Wikimedia Commons, con su autor y su
  licencia.
- **Un vídeo para los temas 1, 2 y 3 de 2.º**, las tres únicas unidades sin
  ninguno. La página ya trae el cargador —el vídeo no se descarga hasta que se
  pulsa—, así que es cuestión de elegirlo; pero elegirlo a ciegas sería poner un
  enlace que quizá pida cuenta para verse, que es justo lo que no puede pasar.

Lo demás está: las veintiuna páginas de tema tienen sus escenas, su test que se
corrige solo, sus fichas de actividad y su lectura de aula en PDF.

## Erratas

Si encuentras un error —una cuenta que no sale, una definición torcida, un
enlace roto—, abre una incidencia en
[el repositorio](https://github.com/rgllorente82-png/robertotecnologia/issues).
Se agradece especialmente si traes el número que no cuadra.
