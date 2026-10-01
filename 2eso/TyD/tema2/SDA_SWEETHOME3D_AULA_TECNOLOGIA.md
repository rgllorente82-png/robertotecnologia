# Situación de Aprendizaje: «El Aula de Tecnología Modelo»
## Expresión Gráfica y Diseño Asistido por Ordenador (CAD 3D) con Sweet Home 3D

* **Materia:** Tecnología y Digitalización (TyD) — 2.º de ESO
* **Unidad curricular:** Tema 2 · Expresión gráfica de un proyecto
* **Marco normativo:** LOMLOE · Orden de 30 de mayo de 2023 (Andalucía, BOJA núm. 104 de 2 de junio de 2023)
* **Entorno operativo:** EducaAndOS (Linux educativo de la Junta de Andalucía)
* **Herramientas:** Sweet Home 3D, cinta métrica/flexómetro, Google Classroom

---

## 1. Concreción Curricular (Andalucía)

### Competencias Específicas y Criterios de Evaluación
* **Competencia Específica 2 (CE2):** Abordar problemas tecnológicos con autonomía y creatividad, aplicando estrategias de trabajo colaborativo.
  * **Criterio 2.1:** Organizar y planificar el trabajo en equipo de forma equitativa, distribuyendo tareas y responsabilidades para la toma de datos y resolución de un reto técnico.
* **Competencia Específica 4 (CE4):** Describir, representar y comunicar el diseño de un objeto o espacio técnico mediante herramientas de expresión gráfica tradicionales y digitales.
  * **Criterio 4.1:** Representar y acotar la planta de un espacio técnico combinando croquis a mano alzada y herramientas digitales CAD 2D/3D (Sweet Home 3D), aplicando escalas y normas básicas de acotación.

### Saberes Básicos
* **B.1:** Boceto, croquis y plano acotado. Elementos de acotación (líneas de cota, líneas auxiliares, cifras de cota). Escala y proporcionalidad.
* **B.2:** Sistemas de representación: vista en planta (2D) y perspectiva axonométrica/cónica (3D).
* **B.3:** Herramientas digitales CAD: modelado paramétrico de muros, puertas, ventanas, texturizado y renderizado 3D de proyectos técnicos.

### Competencias Clave
* **STEM:** Razonamiento espacial, medición directa y proporcionalidad matemática.
* **CD (Competencia Digital):** Instalación de paquetes de software en EducaAndOS, gestión de librerías libres y uso de software CAD.
* **CPSAA (Personal, Social y de Aprender a Aprender):** Coordinación cooperativa en la toma de medidas físicas del aula.

---

## 2. La Narrativa del Reto

> **El encargo de la Consejería de Desarrollo Educativo:**  
> *«La Junta de Andalucía va a construir nuevos Institutos de Educación Secundaria y quiere recopilar los mejores diseños de aulas de Tecnología de la comunidad para replicar su distribución en los nuevos centros.  
> Como departamento de futuros ingenieros y diseñadores de 2.º de ESO, vuestra misión es medir con precisión milimétrica nuestra aula actual, digitalizar su plano técnico en Sweet Home 3D y proponer una mejora innovadora que demuestre a los inspectores de la Junta por qué nuestra clase debe ser el modelo oficial de Andalucía.»*

---

## 3. Secuencia Didáctica (5 Sesiones)

### Sesión 1 · Preparación del entorno digital y librerías 3D en EducaAndOS
* **Objetivo:** Instalar Sweet Home 3D y cargar el banco oficial de mobiliario bajo licencias abiertas (Arte Libre, CC-BY, Dominio Público).
* **Desarrollo:**
  1. **Instalación:** Abrir el gestor / repositorio de software de EducaAndOS e instalar **Sweet Home 3D**.
  2. **Descarga de bibliotecas:** Acceder al repositorio oficial (`https://www.sweethome3d.com/es/importar-modelos-3d/`) y descargar los 8 paquetes de modelos en formato `.zip`:
     * `3DModels-Contributions-1.9.3.zip` (29 MB – 511 modelos – Licencia de Arte Libre)
     * `3DModels-LucaPresidente-1.9.3.zip` (3.7 MB – 64 modelos – Licencia de Arte Libre)
     * `3DModels-Trees-1.9.3.zip` (6.7 MB – 10 modelos – Licencia de Arte Libre)
     * `3DModels-Scopia-1.9.3.zip` (69.5 MB – 500 modelos – Licencia CC-BY)
     * `3DModels-KatorLegaz-1.9.3.zip` (8.9 MB – 90 modelos – Licencia CC-BY)
     * `3DModels-BlendSwap-CC-0-1.9.3.zip` (23.8 MB – 175 modelos – Dominio Público)
     * `3DModels-BlendSwap-CC-BY-1.9.3.zip` (23.9 MB – 135 modelos – Licencia CC-BY)
     * `3DModels-Reallusion-1.9.3.zip` (10.7 MB – 25 modelos – Licencia Libre)
  3. **Descompresión obligatoria:** ⚠️ *Paso imprescindible:* Antes de poder importarlos en el programa, hay que **descomprimir cada archivo `.zip`** (clic derecho > *Extraer aquí* en EducaAndOS). Al extraerlos se obtienen los ficheros con extensión `.sh3f` (formato nativo de librerías de Sweet Home 3D). El software no puede leer los modelos directamente desde los archivos comprimidos `.zip`.
  4. **Importación:** En Sweet Home 3D: menú *Mobiliario > Importar biblioteca de mobiliario...* y seleccionar los archivos descomprimidos `.sh3f` (o hacer doble clic sobre cada `.sh3f` para que se instalen automáticamente en el catálogo).
  5. **Familiarización:** Breve prueba de las 4 ventanas de trabajo (Catálogo de muebles a la izquierda, Lista de elementos, Vista en Planta 2D arriba y Vista Virtual 3D abajo).

---

### Sesión 2 · Trabajo de campo colaborativo: toma de medidas y croquis en pizarra
* **Objetivo:** Medir el aula real en equipos cooperativos y consensuar el croquis técnico acotado.
* **Organización en grupos de medición (con flexómetro / cinta métrica):**
  * **Grupo A (Estructura general):** Largo y ancho del aula, grosor de los muros maestros/tabiques y altura del suelo al techo.
  * **Grupo B (Accesos e iluminación):** Anchura y altura de la puerta, batiente de apertura, ancho de ventanas y altura del antepecho (distancia suelo-ventana).
  * **Grupo C (Zona de taller y bancos):** Dimensiones de los bancos de trabajo de madera, tornillos de banco, panel de herramientas y extintores/seguridad.
  * **Grupo D (Zona de informática y almacenaje):** Mesas de ordenadores, armario de materiales, mesa del docente y pizarra interactiva.
* **Consenso colectivo:** Cada grupo vierte sus medidas en la pizarra del aula. Se dibuja entre todos el **croquis acotado en planta** con cotas expresadas en centímetros. Cada alumno copia el croquis definitivo en su cuaderno.

---

### Sesión 3 · Levantamiento arquitectónico y acotación normalizada en Sweet Home 3D
* **Objetivo:** Trazar la planta estructural exacta con sus cotas técnicas en el software CAD.
* **Desarrollo:**
  1. Configuración de preferencias: unidad de medida en centímetros, grosor y altura de paredes por defecto.
  2. **Trazado de paredes (`Crear paredes`):** Dibujar el perímetro exacto siguiendo las cotas del croquis de la Sesión 2.
  3. **Inserción de vanos:** Añadir puertas y ventanas desde el catálogo. Modificar con doble clic sus cotas reales (anchura, altura y elevación del antepecho).
  4. **Acotación normalizada (`Crear cotas`):**
     * Acotación exterior: longitud y anchura total del aula.
     * Acotación interior: distancias entre pilares, huecos de puertas y ventanas.
     * Regla técnica: las cifras de cota deben situarse sobre la línea de cota y sin cruzarse con las paredes.

---

### Sesión 4 · Equipamiento del aula actual y texturizado de materiales
* **Objetivo:** Replicar el mobiliario existente y aplicar acabados superficiales realistas.
* **Desarrollo:**
  1. **Distribución del taller:** Colocar desde la biblioteca importada los bancos de carpintero, taburetes, paneles de pared, mesas de ordenadores y estanterías de proyectos.
  2. **Escala paramétrica:** Doble clic en cada mueble para ajustar sus tres dimensiones exactas (ancho, fondo, alto) a las medidas reales tomadas en la Sesión 2.
  3. **Materiales y texturas:**
     * `Crear habitaciones`: Generar el suelo y asignarle textura (gres, cemento pulido o parqué).
     * Paredes: Seleccionar colores o texturas técnicas (zócalo blanco/verde institucional).

---

### Sesión 5 · Propuesta de mejora para la Junta de Andalucía y entrega en Classroom
* **Objetivo:** Incorporar la zona de innovación tecnológica, generar la documentación técnica y entregar en Google Classroom.
* **Desarrollo:**
  1. **La Propuesta de Innovación:** Cada alumno/pareja añade a su diseño **un elemento o espacio que actualmente no existe en el aula** y que haría que la Junta elija su proyecto (p. ej.: zona de impresión 3D y corte láser, pista de pruebas de robótica, rincón de energías renovables o rincón de seguridad con taquillas individuales para EPIs).
  2. **Generación de entregables:**
     * **Plano técnico 2D:** Exportar la planta acotada a PDF (*Plano > Exportar en formato PDF...*).
     * **Perspectiva 3D:** Crear una fotografía renderizada de la propuesta de mejora (*Vista 3D > Crear foto...* en calidad media/alta).
     * **Archivo fuente:** Guardar el archivo `.sh3d` como respaldo editable.
  3. **Entrega en Classroom:** Tarea *«SdA: Diseño de nuestra Aula de Tecnología en Sweet Home 3D»*, adjuntando los 3 archivos y un párrafo justificando su propuesta de mejora.

---

## 4. Rúbrica de Evaluación (Séneca / Classroom)

| Criterio / Indicador | Insuficiente (1-4) | Suficiente / Bien (5-6) | Notable (7-8) | Sobresaliente (9-10) | Ponderación |
|---|---|---|---|---|---|
| **Toma de medidas y croquis (CE2 · 2.1)** | No toma medidas o el croquis no incluye cotas representativas. | Toma medidas básicas pero hay desproporciones evidentes en el croquis. | Medidas precisas, croquis claro y trabajo coordinado en el grupo de medición. | Croquis exhaustivo con simbología normalizada y excelente liderazgo de equipo. | **20 %** |
| **Planta y acotación CAD (CE4 · 4.1)** | Paredes desalineadas o sin cotas. Medidas no coincidentes con la realidad. | Planta cerrada con dimensiones aproximadas; cotas incompletas o superpuestas. | Planta fiel al aula con paredes bien dimensionadas y cotas normalizadas legibles. | Precisión milimétrica en planta, vanos perfectamente colocados y acotación técnica impecable. | **30 %** |
| **Mobiliario y texturizado (CE4 · 4.1)** | Mobiliario escaso o sin escalar a las dimensiones reales del aula. | Mobiliario básico colocado pero con fallos de orientación o escalas por defecto. | Mobiliario completo correctamente escalado y texturizado realista de suelos/muros. | Distribución espacial óptima respetando zonas de paso, evacuación y escalas exactas. | **25 %** |
| **Propuesta de innovación (CE2 · 2.1)** | No incluye ninguna propuesta de mejora o no tiene sentido técnico. | Propuesta genérica sin justificar su utilidad en el aula de Tecnología. | Propuesta técnica interesante (impresión 3D, robótica, etc.) bien integrada. | Propuesta sobresaliente, original, funcional y convincentemente justificada para la Junta. | **15 %** |
| **Entrega y formatos digitales (B.3)** | Entrega incompleta o fuera de formato. | Entrega solo uno de los archivos requeridos (solo foto o solo plano). | Entrega los 3 archivos (.sh3d, PDF del plano y render 3D) en Classroom en tiempo. | Documentación técnica profesional impecable y justificación clara en Classroom. | **10 %** |
