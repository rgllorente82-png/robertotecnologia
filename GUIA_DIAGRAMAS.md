# Guía de Diagramas Educativos - robertotecnología

## Sobre esta colección

Esta web contiene **51 diagramas SVG** diseñados para complementar la enseñanza de Tecnología en 2º y 4º de ESO. Cada diagrama fue creado con criterios pedagógicos específicos y puede usarse de varias formas en clase.

---

## 2º ESO - Tecnología y Diseño

### Tema 1: El proceso tecnológico
- **sketch-to-plan-progression.svg** - Evolución desde boceto a plano técnico
  - *Usa para:* Explicar niveles de precisión en dibujo técnico
  - *Ejercicio:* Clasifica tus propios dibujos en la escala

### Tema 2: Materiales
- **materials_wood_metal_plastic.svg** - Propiedades de materiales comunes
- **material-lifecycle.svg** - Ciclo de vida: extracción, uso, reciclaje

### Tema 3: Máquinas simples
- **lever-classes.svg** - Tres clases de palancas con ventaja mecánica
- **simple-machines.svg** - Seis máquinas simples ilustradas
- **mechanical-advantage-levers.svg** - Cálculo de ventaja mecánica
- **triangulation-structures.svg** - Por qué los triángulos son rígidos
- **structures-types.svg** - Viga, arco, tienda comparadas

### Tema 4: Fuerzas
- **forces-newtons-laws.svg** - Las tres leyes de Newton
- **electrical-power-energy.svg** - Diferencia potencia/energía

### Tema 5: Movimiento
- **lever-classes.svg** - Amplifica fuerzas
- **project-phases-timeline.svg** - Timeline de fases de proyecto
- **manufacturing-methods.svg** - Métodos de fabricación (subtractivo vs aditivo)

### Tema 6: Circuitos eléctricos
- **electric-circuit-basics.svg** - Componentes básicos del circuito
- **ohms-law-triangle.svg** - V = I × R mnemotécnico
- **series-parallel-circuits.svg** - Comparación serie vs paralelo
- **series-parallel-circuits.svg** - Comportamiento en ambas configuraciones

### Tema 7: Redes
- **network-layers-osi.svg** - Capas del modelo OSI
- **http-vs-https-security.svg** - Diferencia HTTP vs HTTPS
- **digital-collaboration.svg** - Herramientas de colaboración en línea

### Tema 8: Internet y seguridad
- **http-vs-https-security.svg** - Candado y encriptación HTTPS
- **Más sobre privacidad y datos:** Consulta Tema 9

### Tema 9: Herramientas digitales
- **file-formats.svg** - Formatos: TXT, DOCX, PDF, JPG, MP4, HTML
- **image-pixels-color.svg** - Píxeles y modelo RGB
- **image-resolution-filesize.svg** - Resolución vs tamaño de archivo

---

## 4º ESO - Tecnología

### Tema 1: Pensamiento de diseño
- **design-thinking-process.svg** - Las 5 fases de design thinking
- **problem-vs-solution.svg** - Problemas mal vs bien definidos
- **digital-collaboration.svg** - Trabajo en equipo distribuido

### Tema 2-7: Tecnología aplicada
- **conditional-if-else.svg** - Lógica IF/ELSE en programación
- **state-machine-concept.svg** - Máquinas de estado (qué es un estado)
- **iot-architecture.svg** - Arquitectura IoT (sensor, red, cloud)
- **robot-vs-automation.svg** - Robot ≠ Automatización
- **motor-types-comparison.svg** - Tipos de motores (DC, servo, paso)
- **transistor-basics.svg** - El transistor como interruptor electrónico
- **transistor-switch-concept.svg** - Cómo amplifica una señal

### Tema 8: Sostenibilidad
- **product-lifecycle-sustainability.svg** - Ciclo de vida y sostenibilidad
- **embodied-energy-comparison.svg** - Energía incorporada en materiales
- **appropriate-technology.svg** - Criterios de tecnología apropiada

### Tema 9: Evaluación y impacto
- **evaluation-criteria-matrix.svg** - Rúbrica de evaluación
- **solution-impact-matrix.svg** - Matriz efectividad vs complejidad

---

## Cómo usar estos diagramas en clase

### 1. **Introducción a un concepto** (10 min)
   - Proyecta el diagrama sin explicación
   - Pregunta: "¿Qué ves? ¿Qué no entiendes?"
   - Luego explica

### 2. **Referencia visual durante teoría** (5-10 min)
   - Usa el diagrama al explicar
   - Señala cada parte conforme la nombras
   - Crea conexión visual-auditiva

### 3. **Ejercicio de interpretación**
   - Pide a alumnos: "Explica este diagrama a alguien que no lo entienda"
   - O: "¿Qué está mal en este diagrama?"
   - Fuerza pensamiento crítico

### 4. **Comparación y contraste**
   - Muestra dos diagramas relacionados
   - "¿Qué cambia entre estos dos?"
   - Ejemplo: serie vs paralelo, JPEG vs PNG

### 5. **Ejercicio de creación**
   - "Dibuja tu propio diagrama de este concepto"
   - Luego compara con el oficial

---

## Mejores prácticas de accesibilidad

Cada diagrama incluye:
- ✅ **Descripción alt completa** en el código HTML
- ✅ **Soporte tema claro/oscuro** automático
- ✅ **Contraste verificado** (WCAG AA)
- ✅ **Loading lazy** para performance

### Cómo adaptar para alumnos con discapacidad visual:
1. Lee la descripción alt en voz alta
2. Usa el diagrama como **punto de referencia**, no como información única
3. Proporciona tabla de datos equivalente (disponible en muchos)

---

## Integración con herramientas

### Copiar el HTML de un diagrama:
```html
<figure class="foto">
  <img src="../../../img/[nombre].svg" width="1000" height="700" loading="lazy" 
       alt="[Descripción completa del diagrama]">
  <figcaption>[Explicación breve]. 
    <span class="credito">Elaboración propia · CC BY-SA 4.0</span>
  </figcaption>
</figure>
```

### Reusar en Google Slides, PowerPoint:
- Descarga el SVG
- Importa como imagen
- El SVG se renderiza como cualquier imagen PNG

### Usar en documentos PDF:
- Los SVG se convierten a rasterizado al exportar PDF
- Mantienen calidad (son vectoriales)

---

## Licencia

**CC BY-SA 4.0** - Puedes:
- ✅ Usar libremente
- ✅ Modificar
- ✅ Compartir
- ✅ Usar comercialmente

Siempre que:
- 📝 Atribuyas a "Roberto Tecnología"
- 🔗 Compartas bajo la misma licencia

---

## Contribuir mejoras

Si encuentras un error o tienes sugerencia de diagrama:
1. Abre un issue en el repositorio
2. Describe qué falta o qué está mal
3. Sugiere un tema de diagrama nuevo si lo necesitas

---

**Última actualización:** Septiembre 2026  
**Diagramas totales:** 51  
**Cobertura:** 2º ESO (9 temas), 4º ESO (9 temas)
