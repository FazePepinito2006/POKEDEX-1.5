# Pokedex Stats Generator - Solemne 3

## Descripción del Proyecto
Esta aplicación es una herramienta web interactiva desarrollada en Python utilizando **Streamlit**. Permite a los usuarios consultar estadísticas detalladas de Pokémones individuales y realizar análisis comparativos avanzados entre grupos de Pokémones filtrados por tipo y generación (rango de ID).

La aplicación consume datos en tiempo real de la **PokeAPI** (API REST pública).

## Características Principales
1.  **Buscador Individual:** Consulta de datos biográficos, físicos y estadísticos de cualquier Pokémon.
2.  **Visualización de Datos:**
    * Gráfico de barras para estadísticas base.
    * Gráfico de barras agrupadas (Altair) para comparación precisa de stats.
    * Gráfico de dispersión interactivo (Scatter Plot) para análisis de Peso vs Altura.
    * Gráfico de líneas para ranking de Poder Total.
3.  **Filtros Avanzados:** Selección por Tipo y Rango de IDs (Generación).
4.  **Uso Responsable:** Sistema de limitación de solicitudes (máximo 20 elementos) para no saturar la API pública.

## Requisitos del Sistema
* Python 3.8 o superior.
* Conexión a Internet (para consumir la API).

## Librerías Utilizadas
El proyecto utiliza las siguientes librerías externas:
* `streamlit`: Para la interfaz web.
* `pandas`: Para la manipulación y estructuración de datos.
* `requests`: Para la conexión HTTP con la PokeAPI.
* `altair`: Para la generación de gráficos interactivos avanzados.

## Instrucciones de Instalación

1. **Descargar el proyecto:**
   Asegúrese de tener todos los archivos en una misma carpeta (`nombre_de_tu_archivo.py`, `requirements.txt`, `README.md`).

2. **Instalar dependencias:**
   Abra una terminal (consola de comandos) en la carpeta del proyecto y ejecute:
   ```bash
   pip install -r requirements.txt
