# Pokedex Stats Generator SOLEMNE 3

## Descripcion del proyecto
Esta aplicacion es una herramienta web interactiva desarrollada en Python utilizando Streamlit, la cual permite a los usuarios consultar estadisticas detalladas de Pokemones individuales y realizar ciertos analisis comparativos avanzados entre grupos de Pokemones filtrados por tipo y generacion (rango de ID).

La aplicacion consume datos en tiempo real de la **PokeAPI** (API REST publica).

## Caracteristicas principales
1.  **Buscador individual:** Consulta de datos biogrficos, fisicos y estadisticos de cualquier Pokemon.
2.  **Visualizacion de datos:**
    * Grafico de barras para estadisticas base.
    * Grafico de barras agrupadas (Altair) para comparacion precisa de stats.
    * Grafico de dispersion interactivo (Scatter Plot) para analisis de Peso vs Altura.
    * Grafico de lineas para ranking de Poder Total.
3.  **Filtros avanzados:** Seleccion por tipo y rango de IDs ( O generacion).
4.  **Uso responsable:** Sistema de limitacion de solicitudes (maximo 20 elementos) para no saturar la API y por temas de tiempos de carga.

## Requisitos de sistema
* Conexion a internet (para consumir la API).

## Librerias utilizadas
El proyecto utiliza las siguientes librerias externas:
* **Streamlit:** Para la interfaz web.
* **Pandas:** Para la manipulacion y estructuracion de datos.
* **Requests:** Para la conexion HTTP con la PokeAPI.
* **Altair:** Para la generacion de graficos interactivos avanzados.

## Instrucciones de instalacion
**Antes de intentar correr cualquier codigo hay que instalar las librerias externas**
Debe abrir la consola (CMD), copiar y pegar los siguientes comandos:
* py -m pip install streamlit
* py -m pip install pandas
* py -m pip install requests
* py -m pip install altair
