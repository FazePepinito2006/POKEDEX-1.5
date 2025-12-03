#CARGA DE LIBRERIAS PRINCIPALES
#Sin esto el codigo no tiene por donde funcionar
import streamlit as st
import pandas as pd
import requests

#CONFIGURACION DE LA PAGINA
#Titulo de la app
st.title("Pokedex Stats Generator")

def obtener_datos_pokemon(nombre):
    #Convertimos el nombre a minusculas porque la API lo exige así
    nombre = nombre.lower()
    url = f"https://pokeapi.co/api/v2/pokemon/{nombre}"
    try:
        response = requests.get(url)
        response.raise_for_status() #Lanza un error para codigos de estado HTTP incorrectos
        datos_pokemon = response.json()
        return datos_pokemon
    except requests.exceptions.HTTPError as http_err: #Toda esta seccion es para evitar errores
        st.error(f"error HTTP al obtener datos de {nombre}: {http_err}")
        return None
    except requests.exceptions.ConnectionError as conn_err:
        st.error(f"error de conexión al obtener datos de {nombre}: {conn_err}")
        return None
    except requests.exceptions.Timeout as timeout_err:
        st.error(f"tiempo de espera agotado al obtener datos de {nombre}: {timeout_err}")
        return None
    except requests.exceptions.RequestException as req_err:
        st.error(f"error inesperado al obtener datos de {nombre}: {req_err}")
        return None
#CUADRO DE BUSQUEDA
pokemon_name = st.text_input("Ingresa el nombre del Pokemon:", "pikachu")
if pokemon_name:
    pokemon_data = obtener_datos_pokemon(pokemon_name)
    if pokemon_data:
        st.subheader(f"Datos de {pokemon_data['name'].capitalize()}:")

        # Muestra la imagen del Pokémon en lugar del texto
    if 'sprites' in pokemon_data and 'front_default' in pokemon_data['sprites']:
        st.image(pokemon_data['sprites']['front_default'], caption=f"Sprite de {pokemon_name}")
    
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="ID", value=pokemon_data['id'])
        with col2:
            st.metric(label="Altura (m)", value=pokemon_data['height']/10)

        st.metric(label="Peso (Kg)", value=pokemon_data['weight']/10)

        st.write("Habilidades:") #Titulos
        abilities_list = [ability['ability']['name'] for ability in pokemon_data['abilities']]
        abilities_df = pd.DataFrame(abilities_list, columns=['habilidad'])
        st.dataframe(abilities_df, hide_index=True)

        st.write("Tipos:")
        types_list = [type_entry['type']['name'] for type_entry in pokemon_data['types']]
        types_df = pd.DataFrame(types_list, columns=['tipo'])
        st.dataframe(types_df, hide_index=True)

        st.write("## Estadísticas Base:")
        stats_data = []
        for stat_entry in pokemon_data['stats']:
            stat_name = stat_entry['stat']['name'].replace('-', ' ').title()
            base_stat = stat_entry['base_stat']
            stats_data.append({'estadistica': stat_name, 'valor base': base_stat})

        stats_df = pd.DataFrame(stats_data)
        stats_df = stats_df.set_index('estadistica')
        st.bar_chart(stats_df)

    else:
        st.write("No se pudieron obtener los datos del Pokemon.")

#COMPARACIÓN AVANZADA
st.markdown("---") #Linea divisoria
st.header("Comparador de Pokémones por Tipo y Rango")

#Obtener lista de tipos para el selectbox
url_tipos = "https://pokeapi.co/api/v2/type"
try:
    resp_tipos = requests.get(url_tipos).json()
    lista_tipos = [t['name'] for t in resp_tipos['results']]
    #Primer recuadro: Selectbox
    tipo_seleccionado = st.selectbox("Selecciona un Tipo de Pokémon para analizar:", lista_tipos)
except:
    st.error("No se pudieron cargar los tipos.")
    tipo_seleccionado = None

if tipo_seleccionado:
    #Obtener pokemones de ese tipo
    url_por_tipo = f"https://pokeapi.co/api/v2/type/{tipo_seleccionado}"
    data_tipo = requests.get(url_por_tipo).json()
    
    #Extraemos nombre y URL para sacar el ID
    pokemones_del_tipo = []
    for p in data_tipo['pokemon']:
        nombre_p = p['pokemon']['name']
        url_p = p['pokemon']['url']
        try:
            id_p = int(url_p.split('/')[-2]) #Truco para sacar ID desde la URL
            pokemones_del_tipo.append({'name': nombre_p, 'id': id_p})
        except:
            continue
    
    df_tipo = pd.DataFrame(pokemones_del_tipo)
    
    if not df_tipo.empty:
        #Segundo recuadro: Slider de rango
        st.write("Selecciona el rango de IDs (Antigüedad) a comparar:") #Ya que la API no proporciona datos de fecha, usamos los ID para trabajar con rangos y asi implementar el uso de un deslizador
        rango_ids = st.slider("Rango de ID:", 1, 1025, (1, 151))
        
        #Filtramos el dataframe por el rango del slider
        df_filtrado = df_tipo[(df_tipo['id'] >= rango_ids[0]) & (df_tipo['id'] <= rango_ids[1])]
        
        st.write(f"Encontrados **{len(df_filtrado)}** pokémones de tipo {tipo_seleccionado} en este rango.")

        #Sistema de seguridad para no saturar la API
        if len(df_filtrado) > 20:
            st.warning("Hay muchos Pokémon en este rango!! Se analizarán los primeros 20!!")
            df_filtrado = df_filtrado.head(20)

        #Boton para comenzar el analisis
        if st.button("Generar Gráfico Comparativo"):
            lista_stats_comparacion = []
            
            #Barra de progreso
            barra_progreso = st.progress(0)
            total = len(df_filtrado)
            
            for i, row in enumerate(df_filtrado.iterrows()):
                poke_info = row[1]
                datos = obtener_datos_pokemon(poke_info['name'])
                if datos:
                    hp = datos['stats'][0]['base_stat']
                    ataque = datos['stats'][1]['base_stat']
                    defensa = datos['stats'][2]['base_stat']
                    velocidad = datos['stats'][5]['base_stat']
                    
                    lista_stats_comparacion.append({
                        'Nombre': datos['name'],
                        'HP': hp,
                        'Ataque': ataque,
                        'Defensa': defensa,
                        'Velocidad': velocidad
                    })
                barra_progreso.progress((i + 1) / total)
            
            #Creacion dataframe final
            df_comparativo = pd.DataFrame(lista_stats_comparacion)
            
            if not df_comparativo.empty:
                df_comparativo = df_comparativo.set_index('Nombre')
                
                #Grafico de area
                st.subheader(f"Comparativa de Stats: Tipo {tipo_seleccionado}")
                st.area_chart(df_comparativo[['Ataque', 'Defensa', 'Velocidad']])
                
                #Interpretacion de los resultados
                st.info(f"**Analisis:** Se observa la distribución de stats para el tipo {tipo_seleccionado}. "
                        f"Los picos indican pokemones que destacan en sus atributos dentro del rango seleccionado.")
            else:
                st.warning("No se encontraron datos válidos para graficar.")
