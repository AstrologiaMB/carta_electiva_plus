# Programa de Análisis Astrológico

Este programa analiza la compatibilidad entre una carta natal (A) y diferentes momentos en el tiempo (B(n)) para encontrar momentos óptimos según criterios astrológicos específicos.

## Acerca del Proyecto

Este proyecto es una versión mejorada inspirada en el proyecto original de carta electiva. Las mejoras principales incluyen:
- Corrección en el orden de evaluación de cartas en final_table.py
- Mejora en el cálculo de porcentajes y precisión
- Optimización de intervalos de tiempo para mejor rendimiento
- Documentación expandida y clarificada

### Estructura del Repositorio
- `main`: Rama principal con código estable
- `development`: Rama para nuevas características
- `feature/*`: Ramas para características específicas

### Para Desarrolladores
1. **Clonar el Repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd carta_electiva
   git checkout -b development
   ```

2. **Desarrollo de Características**
   ```bash
   # Crear rama para nueva característica
   git checkout -b feature/nombre-caracteristica
   
   # Desarrollar y commitear cambios
   git add .
   git commit -m "Descripción clara del cambio"
   
   # Merge a development cuando esté listo
   git checkout development
   git merge feature/nombre-caracteristica
   ```

3. **Contribuir**
   - Crear rama feature/* desde development
   - Seguir guía de estilo del proyecto
   - Documentar cambios en README si es necesario
   - Crear pull request a development

## Requisitos del Sistema

### Python y Dependencias
- Python 3.11 o superior
- Dependencias principales:
  - immanuel==1.3.2 (cálculos astrológicos)
  - pandas==2.2.2 (manejo de datos)
  - numpy==1.26.4 (cálculos numéricos)
  - pyswisseph==2.10.3.2 (efemérides)
  - python-dateutil==2.9.0 (manejo de fechas)
  - pytz==2024.1 (zonas horarias)
  - timezonefinder==5.2.0 (ubicaciones)

### Configuración del Entorno

#### Entorno Virtual
Este proyecto utiliza el entorno virtual del proyecto original ubicado en:
```
/Users/apple/electiva/carta_electiva/venv_3.11
```

Para activar el entorno:
```bash
# En macOS/Linux:
source ../carta_electiva/venv_3.11/bin/activate

# En Windows:
..\carta_electiva\venv_3.11\Scripts\activate
```

Nota: El entorno virtual ya contiene todas las dependencias necesarias instaladas y configuradas correctamente. No es necesario instalar dependencias adicionales.

#### Variables de Entorno
El proyecto utiliza un archivo .env para configurar el PYTHONPATH:
```
PYTHONPATH=/Users/apple/electiva/carta_electiva_plus
```

Para ejecutar scripts manualmente, asegúrate de incluir el PYTHONPATH:
```bash
PYTHONPATH=/Users/apple/electiva/carta_electiva_plus python your_script.py
```

#### Verificación de la Instalación
El proyecto incluye un script de prueba que verifica la instalación y funcionalidad básica:
```bash
# Activar entorno y ejecutar prueba
source ../carta_electiva/venv_3.11/bin/activate
PYTHONPATH=/Users/apple/electiva/carta_electiva_plus python testing/test_import.py
```

El script verifica:
- Importación correcta de módulos
- Creación de instancias
- Generación de DataFrames
- Cálculo de resultados

Una instalación correcta mostrará:
```
Probando importación de módulos...
✓ final_table importado correctamente
✓ moon_aptitude importado correctamente
✓ Creación de instancia moonAptitude exitosa
✓ Generación de DataFrame exitosa
```

## Configuración del Entorno de Desarrollo

1. **Clonar el Repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd carta_electiva
   ```

2. **Configurar VSCode**
   - Instalar extensiones recomendadas:
     - Python
     - Jupyter
     - Python Test Explorer
   - Seleccionar el intérprete de Python del entorno virtual

3. **Verificar la Instalación**
   ```python
   # En Python o Jupyter
   from astro_package import final_table as ft
   print(ft.__version__)  # Debería mostrar la versión actual
   ```

4. **Estructura de Directorios**
   - Asegurarse de que existe la estructura básica:
     ```bash
     mkdir -p carta_electiva/testing
     mkdir -p carta_electiva/output_files
     ```


## Estructura del Proyecto

```
carta_electiva_plus/
├── .env                         # Configuración de PYTHONPATH
├── .gitignore                   # Exclusiones de Git
├── LICENSE                      # Licencia MIT
├── README.md                    # Este archivo
├── requirements.txt             # Dependencias del proyecto
├── setup.py                     # Configuración de instalación
├── astro_package/              # Paquete principal
│   ├── __init__.py            # Inicialización del paquete (v2.0.0)
│   ├── moon_aptitude.py       # Análisis de Luna
│   ├── rulership_asc.py       # Análisis Regente ASC
│   ├── rulership_10.py        # Análisis Regente Casa 10
│   ├── optimal_minutes.py     # Combinaciones Positivas
│   ├── negative_minutes.py    # Combinaciones Negativas
│   ├── enraizar_a_bn.py      # Enraizamiento entre cartas
│   ├── final_table.py        # Generación tabla final
│   ├── settings_astro.py     # Configuraciones astrológicas
│   └── utils/                # Utilidades compartidas
│       ├── __init__.py
│       └── decorators.py
└── testing/                  # Scripts de prueba
    ├── test_import.py       # Verificación de instalación
    └── tabla_final_expanded.ipynb # Análisis detallado
```

### Archivos Principales

- **.env**: Configura el PYTHONPATH para el proyecto
- **setup.py**: Configuración de instalación del paquete
- **requirements.txt**: Lista de dependencias con versiones específicas
- **test_import.py**: Script para verificar la instalación

### Módulos del Paquete

El paquete `astro_package` (v2.0.0) contiene los módulos principales para el análisis astrológico. Cada módulo está diseñado para una función específica y puede ser usado independientemente o en conjunto a través del módulo integrador `final_table.py`.

## Flujo de Datos

1. **Entrada de Datos**
   ```python
   # Carta Natal (A)
   dob_a = "21/08/1990 07:10"
   lat_a = "32s29"
   lon_a = "58w14"

   # Rango para Carta B(n)
   start = "28/07/2024 6:00"
   end = "28/07/2024 7:00"
   lat_bn = "32s29"
   lon_bn = "58w14"
   ```

2. **Procesamiento**
   ```
   FinalTableGenerator
   ├── Inicialización
   │   └── Crea instancias de cada módulo
   │
   ├── Para cada momento en el rango:
   │   ├── moonAptitude
   │   │   └── Evalúa Luna del momento
   │   │
   │   ├── rulershipConditions
   │   │   └── Evalúa Regente ASC del momento
   │   │
   │   ├── rulershipTen
   │   │   └── Evalúa Regente Casa 10 del momento
   │   │
   │   ├── optimalMinutes
   │   │   └── Evalúa aspectos positivos del momento
   │   │
   │   ├── negativeMinutes
   │   │   └── Evalúa aspectos negativos entre A y B(n)
   │   │
   │   └── enraizarCarta
   │       └── Evalúa conexión entre A y B(n)
   │
   └── Generación de Tabla
       └── Combina resultados de todos los módulos
   ```

3. **Salida de Datos**
   ```
   Tabla Final
   ├── Fecha y Hora
   ├── Puntaje Total
   ├── Color (Rojo/Amarillo/Verde)
   ├── Sumatoria Rojos/Azules
   ├── % Puntos por Módulo
   │   ├── Enraizar
   │   ├── Luna
   │   ├── Regente ASC
   │   ├── Regente 10
   │   ├── Combinaciones Positivas
   │   └── Combinaciones Negativas
   └── Estados de Aptitud
   ```

## Módulos Principales

1. **moonAptitude (Luna)**
   - Evalúa 15 condiciones que pueden hacer un momento no apto
   - Evalúa 18 condiciones que suman puntos (17-34)
   - Máximo: 8 puntos (100%)

2. **rulershipASC (Regente del Ascendente)**
   - Evalúa dignidades y aspectos del regente del ASC
   - Incluye condiciones salvadoras
   - Máximo: 7 puntos (100%)

3. **rulership10 (Regente de Casa 10)**
   - Evalúa dignidades y aspectos del regente de la casa 10
   - Incluye condiciones salvadoras
   - Máximo: 7 puntos (100%)

4. **optimalMinutes (Combinaciones Positivas)**
   - Evalúa aspectos favorables entre planetas
   - Máximo: 7 puntos (100%)

5. **negativeMinutes (Combinaciones Negativas)**
   - Evalúa aspectos desfavorables entre cartas A y B(n)
   - Máximo: -2 puntos (-100%)

6. **enraizarCarta (Enraizamiento)**
   - Evalúa la conexión entre cartas A y B(n)
   - Cuenta condiciones rojas (negativas) y azules (positivas)
   - Máximo: 14 puntos (100%)

## Interacción entre Módulos

1. **Módulos Independientes**
   - moonAptitude, rulershipConditions, rulershipTen, optimalMinutes
   - Solo evalúan la carta B(n)
   - Retornan DataFrame con puntos y condiciones

2. **Módulos Relacionales**
   - negativeMinutes, enraizarCarta
   - Evalúan relación entre cartas A y B(n)
   - Retornan DataFrame con puntos y aspectos

3. **Módulo Integrador**
   - final_table.py (FinalTableGenerator)
   - Coordina todos los módulos
   - Unifica resultados en tabla final

## Puntos Críticos

1. **Orden de Cartas**
   ```python
   # Correcto
   FinalTableGenerator(
       carta_natal_A,    # Fija
       carta_momento_Bn  # Variable
   )
   ```

2. **Intervalos de Tiempo**
   ```python
   # Recomendado
   interval_hours = 0.167  # 10 minutos
   ```

3. **Cálculo de Porcentajes**
   ```python
   # Por módulo
   porcentaje = puntos_obtenidos / puntos_maximos * 100
   ```

## Consideraciones Importantes

1. Los planetas necesitan tiempo significativo para mostrar cambios:
   - Intervalos menores a 10 minutos no muestran variación
   - Recomendado: intervalos de 10-15 minutos
   - Rangos de al menos 1 hora para ver progresión

2. El orden de las cartas es crucial:
   - Carta A: Natal (fija)
   - Carta B(n): Momento a evaluar (variable)

## Sugerencias de Mejora

1. **Optimización de Cálculos**
   - Cachear cálculos planetarios entre momentos cercanos
   - Implementar cálculo paralelo para rangos grandes

2. **Mejoras en la Interfaz**
   - Agregar visualización gráfica de aspectos
   - Mostrar gráficos de progresión de porcentajes
   - Implementar filtros interactivos

3. **Funcionalidad**
   - Agregar búsqueda automática de momentos óptimos
   - Implementar análisis predictivo
   - Agregar exportación a diferentes formatos

4. **Código**
   - Unificar el manejo de puntos máximos
   - Implementar sistema de logging
   - Agregar más tests unitarios
   - Mejorar documentación inline

5. **Rendimiento**
   - Optimizar cálculos astronómicos
   - Implementar cálculo asíncrono
   - Agregar soporte para GPU en cálculos masivos

## Uso Típico

1. **Configuración Inicial**
   ```python
   import sys
   import os
   from datetime import datetime
   from astro_package import final_table as ft

   # Configurar fechas y ubicaciones
   start_date = "28/07/2024 6:00"
   end_date = "28/07/2024 7:00"
   latitud = "32s29"
   longitud = "58w14"
   dob_bn = "21/08/1990 07:10"
   ```

2. **Generación de Tabla**
   ```python
   # Usar intervalo de 10 minutos
   df = ft.generar_tabla(
       start_date, end_date,
       latitud, longitud,
       dob_bn, latitud, longitud,
       interval_hours=0.167
   )
   ```

3. **Análisis de Resultados**
   - Revisar momentos con mayor puntaje
   - Verificar condiciones de aptitud
   - Analizar distribución de puntos por módulo

## Solución de Problemas Comunes

1. **El paquete no se importa correctamente**
   - Problema: Error "No module named 'astro_package'"
   - Solución: Asegurarse de que PYTHONPATH incluye el directorio del proyecto
   ```bash
   PYTHONPATH=/Users/apple/electiva/carta_electiva_plus python script.py
   ```

2. **Los porcentajes no coinciden con los puntos**
   - Problema: Los porcentajes mostrados no reflejan los puntos calculados
   - Solución: Verificar el orden de las cartas en FinalTableGenerator
   ```python
   # Orden correcto
   generator = FinalTableGenerator(
       carta_natal_A,     # Carta fija
       carta_momento_Bn   # Momento a evaluar
   )
   ```

3. **No se ven cambios entre momentos consecutivos**
   - Problema: Los resultados son idénticos para momentos muy cercanos
   - Solución: Usar intervalos de al menos 10 minutos
   ```python
   # Intervalo recomendado
   interval_hours = 0.167  # 10 minutos
   ```

4. **Errores en la evaluación de aspectos**
   - Problema: Los aspectos planetarios no se detectan correctamente
   - Solución: Verificar el formato de fechas y coordenadas
   ```python
   # Formato correcto
   fecha = "28/07/2024 6:26"
   latitud = "32s29"     # Sur es 's'
   longitud = "58w14"    # Oeste es 'w'
   ```

## Créditos

Este proyecto es una versión mejorada basada en el trabajo original de carta_electiva. Las mejoras incluyen:
- Corrección en el orden de evaluación de cartas
- Optimización de intervalos de tiempo
- Documentación expandida
- Scripts de verificación
