# Catálogo de proyectos implementables

El cuello de botella para montar un tema no es explicar las fases: es **encontrar
algo que se pueda construir de verdad** con el material, el tiempo y las manos que
hay en un aula.

Este documento recoge candidatos ya filtrados por esa realidad.

## Decidido para 4.º

> **DECIDIDO (18 sep 2026).** El curso se vertebra con el **riego automático**,
> y los grupos eligen **entre tres**:
>
> | | Proyecto | Sensor | Actuador | Lo que mide de impacto |
> |---|---|---|---|---|
> | **A** | **Riego automático** (el principal) | humedad de suelo | bomba 3-6 V o servo | agua gastada frente a regar a mano |
> | **B** | Aviso de aula mal ventilada | temperatura y humedad (DHT11) | señal luminosa de tres colores | ventilación frente a calefacción |
> | **C** | Lámpara de estudio que se ajusta sola | LDR | LED de potencia o tira | consumo real, con la etiqueta energética |
>
> **Por qué estos tres y no otros.** Cubren tres sensores distintos, tres
> actuadores distintos y tres dimensiones de impacto distintas, así que en la
> puesta en común la clase ve tres casos y no tres veces el mismo. Y los tres
> se montan por menos de 5 € por grupo salvo la bomba del A.
>
> **Se cae el de la barrera** (mecánica exigente, y con tres opciones ya hay
> bastante que gestionar) y **el del contenedor**: su gracia era la radio entre
> dos placas, y en 4.º usamos Arduino, donde la radio pide módulo aparte. En
> micro:bit sería gratis, así que **ese encaja mejor en 2.º**.
>
> Consecuencia para la escritura: las unidades 4 a 8 ya están escritas para
> servir con cualquiera de los cinco, así que siguen valiendo. Las unidades
> **1, 2 y 9** —las que cuelgan del proyecto— se escriben con estos tres.

## La restricción de 4.º

Las seis competencias de 4.º tiran a la vez del mismo proyecto. Para que una
propuesta sirva tiene que permitir las seis cosas:

| CE | Exige que el proyecto… |
|----|------------------------|
| 1 | nazca de un problema **observable en su entorno** |
| 2 | se **fabrique** con material y técnica reales |
| 3 | se **presente y defienda** ante otros |
| 4 | se **automatice**: electrónica y programación |
| 5 | use **herramientas digitales** de diseño o simulación |
| 6 | permita medir su **impacto** ambiental o social |

Eso descarta de entrada dos familias enteras:

- **Solo construcción** (estructura de cartón, puente de palillos, maqueta): no
  hay nada que automatizar. Vale para 2.º, no para 4.º.
- **Solo programación** (una app, un juego en MakeCode): no hay nada que
  fabricar ni impacto material que medir.

El proyecto de 4.º tiene que ser un **objeto físico con sensor y actuador**.

---

## Candidatos

Ocho sesiones por unidad. Coste por grupo de tres, con micro:bit reutilizable del
centro. Todos se simulan antes en Tinkercad, así que el montaje físico llega ya
depurado.

### 1 · Riego automático para una planta del aula

**El problema**: las plantas del centro se secan en vacaciones y en puentes.

- **Sensor**: humedad de suelo (dos clavos galvanizados sirven, o sonda capacitiva ~2 €)
- **Actuador**: bomba sumergible 3-6 V (~3 €) o servo que inclina un depósito
- **Estructura**: soporte del depósito y guía del tubo
- **Impacto**: cuánta agua gasta frente a regar a mano; qué pasa si falla
- **Dificultad**: media · **Riesgo**: agua cerca de electrónica, hay que preverlo

Es el que mejor cumple las seis. Y el problema es real y verificable en el centro.

### 2 · Aviso de aula mal ventilada

**El problema**: después de la clase anterior el aula está cargada y nadie abre.

- **Sensor**: temperatura y humedad (DHT11, ~2 €), o CO₂ si hay presupuesto (~20 €)
- **Actuador**: señal luminosa de tres colores, o aviso en la pantalla del micro:bit
- **Estructura**: carcasa de pared, visible desde toda el aula
- **Impacto**: ventilación frente a calefacción, un debate que se sostiene solo
- **Dificultad**: baja · **Riesgo**: bajo

El más barato y el más seguro. Buen candidato si es la primera vez que montas esto.

### 3 · Contenedor que avisa cuando está lleno

**El problema**: las papeleras de reciclaje del pasillo se desbordan.

- **Sensor**: ultrasonidos HC-SR04 (~2 €)
- **Actuador**: luz, o mensaje por radio al micro:bit del conserje
- **Estructura**: soporte en la tapa que no estorbe al tirar
- **Impacto**: reciclaje, rutas de recogida, residuo electrónico del propio aparato
- **Dificultad**: baja-media · **Riesgo**: bajo

Tiene una ventaja didáctica: la comunicación por radio entre dos micro:bit se
entiende mejor aquí que en cualquier ejemplo abstracto.

### 4 · Barrera o puerta con acceso controlado

**El problema**: la entrada al taller o al aparcamiento de bicis.

- **Sensor**: pulsador, tarjeta, o ultrasonidos para detectar presencia
- **Actuador**: servo SG90 (~2 €)
- **Estructura**: barrera, contrapeso, eje
- **Impacto**: accesibilidad — ¿funciona para alguien en silla de ruedas?
- **Dificultad**: media · **Riesgo**: el mecanismo exige precisión

El que más mecánica lleva. Bueno si quieres cargar el tema hacia mecanismos.

### 5 · Lámpara de estudio que se ajusta sola

**El problema**: se estudia con mala luz, o se deja la luz encendida.

- **Sensor**: LDR (~0,20 €)
- **Actuador**: LED de potencia o tira LED
- **Estructura**: el cuerpo de la lámpara, que es donde entra el diseño
- **Impacto**: consumo real, medible con la etiqueta energética
- **Dificultad**: baja · **Riesgo**: mínimo

El más barato de todos y el que más margen deja al diseño del objeto.

---

## Lo que hay que decidir antes de escribir el tema

1. ~~¿Micro:bit o Arduino?~~ **Decidido (17 sep 2026): micro:bit en 2.º,
   Arduino en 4.º.** En 2.º MakeCode arranca en cinco minutos, se programa por
   bloques y casi no hay que cablear. En 4.º el salto a código y a montar el
   circuito real encaja con el nivel, y Tinkercad simula Arduino mucho mejor que
   micro:bit, así que se puede depurar antes de tocar una placa.
   Los cinco proyectos del catálogo valen para las dos placas; solo cambia el
   sensor concreto y el entorno de programación.
2. **¿Proyecto único o a elegir?** Uno solo simplifica la gestión del aula; a
   elegir motiva más y encaja mejor con «detectar un problema de tu entorno», que
   es literalmente el criterio 1.1.
3. **¿Hay presupuesto de material?** Con la opción 5 y la 2 se puede montar el
   curso con menos de 5 € por grupo. La 1 y la 4 suben algo.

## Para 2.º

Allí la restricción es mucho menor: el criterio 3.1 pide fabricar con
estructuras, mecanismos, electricidad **y/o** electrónica. Ese *y/o* lo cambia
todo — un proyecto puramente constructivo es válido. Por eso el encargo de la
estructura de cartón sí sirve en 2.º y no en 4.º.
