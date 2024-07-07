import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit.components.v1 as components
import folium
from folium.plugins import FastMarkerCluster
import geopandas as gpd
from branca.colormap import LinearColormap
import streamlit_folium
import plotly.express as px
from wordcloud import WordCloud
import json

st.set_page_config(
    page_title="DataIDEA Consulting",
    page_icon=":sparkles:",
    layout="wide",
    initial_sidebar_state="expanded"
)

def home_page():
    st.title('Exploración de los Airbnb en Málaga')
    st.write('*Informe realizado por DATAIDEA Consulting para el Ayuntamiento de Málaga.*')
    st.image(r'Malaga_foto.jpg')
    photo1=r'logo.PNG'
    photo2=r'ayto-vertical-2lineas-positivo.png'
    photo3=r'Logotipo_de_la_Junta_de_Andalucía_2020.svg.png'
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image(photo1)
    with col2:
        st.image(photo2)
    with col3:
        st.image(photo3)
    st.empty()
    st.empty()
    st.write('*DATAIDEA Consulting*')
    st.write("""Somos un grupo de consultores de datos, especializados en análisis de datos y visualización. 
                    Nuestro objetivo es ayudar a las empresas a tomar decisiones basadas en datos, a través de análisis de datos y visualizaciones interactivas.""")
    st.write("**Si tienes una IDEA, nosotros tenemos los DATOS**")
      
p1= st.Page(home_page, title='Inicio')

def intro():
    st.title('Introducción')
    st.write("""El objetivo de este informe es **analizar los datos de los alojamientos de Airbnb en Málaga**. 
             Para ello, se han realizado diferentes análisis y visualizaciones de datos ,estudiando distintas variables, como la ubicación, el precio o las valoraciones. 
             A continuación, se presentan los resultados obtenidos en este análisis.""")
    st.image(r'intro.PNG')
p2=st.Page(intro, title='Introducción')


def Muestra():
    st.title('Muestra de los datos')
    st.write('Tenemos los datos de **7783 alojamientos de Airbnb** en Málaga, de los que se han estudiado distintas variables, como la **ubicación**, el **precio** o las **valoraciones**.')
    st.write('A continuación, se muestra una tabla con los 5 primeros registros de la base de datos:')
    listings = pd.read_csv('data/listings.csv')
    detailed_listings = pd.read_csv(r'data/detailed_listings.csv')
    target_columns = ["id", "property_type", "accommodates", "first_review", "review_scores_value", "review_scores_cleanliness", "review_scores_location", "review_scores_accuracy", "review_scores_communication", "review_scores_checkin", "review_scores_rating", "maximum_nights", "listing_url", "host_is_superhost", "host_about", "host_response_time", "host_response_rate"]
    short_detailed_listings = detailed_listings[target_columns]
    listings = pd.merge(listings, short_detailed_listings, on='id', how='left')
    st.listings(listings.head(5), wight=1000)
    st.write('Como ya se puede ver en la tabla, hay **columnas** completamente llenas de **datos nulos**, que se **eliminan** para facilitar el análisis.')
p3=st.Page(Muestra, title='Muestra de los datos')


def Análisis():
    st.title('Análisis exploratorio de los datos')
    listings = pd.read_csv(r'listings.csv')
    detailed_listings = pd.read_csv(r'detailed_listings.csv')
    target_columns = ["id", "property_type", "accommodates", "first_review", "review_scores_value", "review_scores_cleanliness", "review_scores_location", "review_scores_accuracy", "review_scores_communication", "review_scores_checkin", "review_scores_rating", "maximum_nights", "listing_url", "host_is_superhost", "host_about", "host_response_time", "host_response_rate"]
    short_detailed_listings = detailed_listings[target_columns]
    listings = pd.merge(listings, short_detailed_listings, on='id', how='left')
    
    tabs = st.tabs(["Localización", "Tipos", "Personas", "Precios", "Puntuaciones"])
    
    with tabs[0]:
        st.header("Localización de los alojamientos")
        lnp = listings['neighbourhood'].value_counts().sort_values(ascending=True)
        import matplotlib.pyplot as plt
        colors = ["#ADD8E6", "#4682B4", "#1E3A8A", "#000080", "#FFD700", "#FFA500", "#DAA520", "#B8860B"]
        plt.rcParams['axes.prop_cycle'] = plt.cycler(color=colors)
        plt.rcParams['figure.facecolor'] = '#FFFFFF'
        plt.rcParams['axes.facecolor'] = '#FFFFFF'
        plt.rcParams['text.color'] = '#000000'
        plt.rcParams['axes.labelcolor'] = '#000000'
        plt.rcParams['xtick.color'] = '#000000'
        plt.rcParams['ytick.color'] = '#000000'
        plt.rcParams['font.family'] = 'sans-serif'
        fig, ax = plt.subplots(figsize=(10, 8))
        lnp.plot.barh(width=1, ax=ax)
        st.pyplot(fig)
        
        lats2023 = listings['latitude'].tolist()
        lons2023 = listings['longitude'].tolist()
        locations = list(zip(lats2023, lons2023))
        map1 = folium.Map(location=[36.72077, -4.42104], zoom_start=11.5)
        folium.plugins.FastMarkerCluster(data=locations).add_to(map1)
        map_html = map1._repr_html_()
        components.html(map_html, height=1100, width=1450)
    
    with tabs[1]:
        st.header("Tipos de alojamientos")
        freq = listings['room_type'].value_counts().sort_values(ascending=True)
        freq_df = freq.reset_index()
        freq_df.columns = ['room_type', 'count']
        color_palette = ["#ADD8E6", "#4682B4", "#1E3A8A", "#000080", "#FFD700", "#FFA500", "#DAA520", "#B8860B"]
        fig = px.bar(freq_df, y='room_type', x='count', orientation='h', color_discrete_sequence=color_palette, height=600, width=1200, title='Tipos de alojamientos ofertados')
        New_names = {
        'Hotel room': 'Habitación de hotel',
        'Shared room': 'Habitación compartida',
        'Private room': 'Habitación privada',
        'Entire home/apt': 'Casa/apartamento entero'
        }
        freq_df['room_type'] = freq_df['room_type'].map(New_names)
        fig = px.bar(freq_df, y='room_type', x='count', orientation='h', color_discrete_sequence=color_palette, height=600, width=1200, title='Tipos de alojamientos ofertados')
        fig.update_xaxes(title_text='')
        fig.update_yaxes(title_text='')
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig)
        
        min_listings = st.slider("Minimum number of listings for a property type", 50, 500, 100, 50)
        selected_room_types = st.multiselect("Select room types to include", options=listings['room_type'].unique(), default=listings['room_type'].unique())
        filtered_listings = listings[listings['room_type'].isin(selected_room_types)]
        prop = filtered_listings.groupby(['property_type', 'room_type']).room_type.count()
        prop = prop.unstack()
        prop['total'] = prop.iloc[:, 0:3].sum(axis=1)
        prop = prop.sort_values(by=['total'])
        prop = prop[prop['total'] >= min_listings]
        prop = prop.drop(columns=['total'])
        new_column_names = {
        'Hotel room': 'Habitación de hotel',
        'Shared room': 'Habitación compartida',
        'Private room': 'Habitación privada',
        'Entire home/apt': 'Casa/apartamento entero',
        'Entire rental unit': 'Alojamiento entero',
        'Private room in rental unit': 'Habitación privada en alojamiento',
        'Entire condo': 'Condominio entero',
        'Entire home': 'Casa entera',
        'Entire loft': 'Loft entero',
        'Entire serviced apartment': 'Apartamento entero con servicios incluidos',
        'Private room in home': 'Habitación privada en casa',
        'Entire vacation home': 'Casa de vacaciones entera'
        }
        prop = prop.rename(columns=new_column_names)
        fig, ax = plt.subplots(figsize=(15, 8))
        import matplotlib.pyplot as plt
        colors = ["#ADD8E6", "#4682B4", "#1E3A8A", "#000080", "#FFD700", "#FFA500", "#DAA520", "#B8860B"]
        plt.rcParams['axes.prop_cycle'] = plt.cycler(color=colors)
        plt.rcParams['figure.facecolor'] = '#FFFFFF'
        plt.rcParams['axes.facecolor'] = '#FFFFFF'
        plt.rcParams['text.color'] = '#000000'
        plt.rcParams['axes.labelcolor'] = '#000000'
        plt.rcParams['xtick.color'] = '#000000'
        plt.rcParams['ytick.color'] = '#000000'
        plt.rcParams['font.family'] = 'sans-serif'
        prop.plot(kind='barh', stacked=True,
                linewidth=1, grid=True, ax=ax, width=1)
        plt.title('Tipos de propiedades en Málaga con al menos {} listados'.format(min_listings), fontsize=18)
        plt.xlabel('Número de listados', fontsize=14)
        plt.ylabel("")
        plt.legend(loc=4, prop={"size": 13}, title="Tipo de habitación")
        plt.rc('ytick', labelsize=13)
        st.pyplot(fig)
    
    with tabs[2]:
        
        st.header("Personas")
        lnp = listings['accommodates'].value_counts().sort_index()
        fig, ax = plt.subplots(figsize=(10, 8))
        colors = ["#ADD8E6", "#4682B4", "#1E3A8A", "#000080", "#FFD700", "#FFA500", "#DAA520", "#B8860B"]
        plt.rcParams['axes.prop_cycle'] = plt.cycler(color=colors)
        plt.rcParams['figure.facecolor'] = '#FFFFFF'
        plt.rcParams['axes.facecolor'] = '#FFFFFF'
        plt.rcParams['text.color'] = '#000000'
        plt.rcParams['axes.labelcolor'] = '#000000'
        plt.rcParams['xtick.color'] = '#000000'
        plt.rcParams['ytick.color'] = '#000000'
        plt.rcParams['font.family'] = 'sans-serif'
        lnp.plot.bar(width=1, ax=ax)
        plt.title("Alojamientos (número de personas)", fontsize=20)
        plt.ylabel('Número de alojamientos', fontsize=12)
        plt.xlabel('Personas', fontsize=12)
        st.pyplot(fig)
    
    with tabs[3]:
        st.header("Precios")
        def draw_price_chart(accommodates=4):
            filtered_data = listings[listings['accommodates'] == accommodates]
            average_price = filtered_data.groupby('neighbourhood')['price'].mean().sort_values()
            colors = plt.cm.magma(np.linspace(0, 1, len(average_price)))
            plt.figure(figsize=(10, 8))
            colors = ["#ADD8E6", "#4682B4", "#1E3A8A", "#000080", "#FFD700", "#FFA500", "#DAA520", "#B8860B"]
            plt.rcParams['axes.prop_cycle'] = plt.cycler(color=colors)
            plt.rcParams['figure.facecolor'] = '#FFFFFF'
            plt.rcParams['axes.facecolor'] = '#FFFFFF'
            plt.rcParams['text.color'] = '#000000'
            plt.rcParams['axes.labelcolor'] = '#000000'
            plt.rcParams['xtick.color'] = '#000000'
            plt.rcParams['ytick.color'] = '#000000'
            plt.rcParams['font.family'] = 'sans-serif'
            average_price.plot.barh(color=colors)
            plt.title(f"Precio medio diario para un alojamiento de {accommodates} personas", fontsize=15)
            plt.xlabel('Precio medio diario (en €)', fontsize=12)
            st.pyplot(plt)
        accommodates = st.slider('Accommodates:', min_value=1, max_value=10, value=4, step=1)
        draw_price_chart(accommodates) 
        
        
        lam2=pd.read_csv(r'lam_reset.csv')
        lam= gpd.read_file(r"neighbourhoods.geojson")
        lam2=pd.DataFrame(lam2)
        lam2 = pd.merge(lam2, lam, on='neighbourhood', how='left')
        gdf = gpd.GeoDataFrame(lam2, geometry='geometry')
        gdf.rename(columns={'price': 'average_price'}, inplace=True)
        gdf.average_price = gdf.average_price.round(decimals=2)
        map_dict = gdf.set_index('neighbourhood')['average_price'].to_dict()
        color_scale = LinearColormap(['yellow', 'red'], vmin=min(map_dict.values()), vmax=max(map_dict.values()))
        def get_color(feature):
            value = map_dict.get(feature['properties']['neighbourhood'])
            return color_scale(value)
        map3 = folium.Map(location=[36.72016, -4.42034], zoom_start=11)
        folium.GeoJson(
            data=gdf,
            name='Málaga',
            tooltip=folium.features.GeoJsonTooltip(fields=['neighbourhood', 'average_price'],
                                                    labels=True,
                                                    sticky=False),
            style_function=lambda feature: {
                'fillColor': get_color(feature),
                'color': 'black',
                'weight': 1,
                'dashArray': '5, 5',
                'fillOpacity': 0.5
            },
            highlight_function=lambda feature: {'weight': 3, 'fillColor': get_color(feature), 'fillOpacity': 0.8}
        ).add_to(map3)
        map_data = streamlit_folium.folium_static(map3, width=1450, height=1100)
    
    with tabs[4]:
        st.header("Puntuaciones")
        fig = plt.figure(figsize=(20, 10))
        plt.rc('xtick', labelsize=16)
        plt.rc('ytick', labelsize=20)
        ax1 = fig.add_subplot(121)
        mal = listings[listings['number_of_reviews'] >= 10]
        mal = mal.groupby('neighbourhood')['review_scores_location'].mean().sort_values(ascending=True)
        colors = ["#ADD8E6", "#4682B4", "#1E3A8A", "#000080", "#FFD700", "#FFA500", "#DAA520", "#B8860B"]
        plt.rcParams['axes.prop_cycle'] = plt.cycler(color=colors)
        plt.rcParams['figure.facecolor'] = '#FFFFFF'
        plt.rcParams['axes.facecolor'] = '#FFFFFF'
        plt.rcParams['text.color'] = '#000000'
        plt.rcParams['axes.labelcolor'] = '#000000'
        plt.rcParams['xtick.color'] = '#000000'
        plt.rcParams['ytick.color'] = '#000000'
        plt.rcParams['font.family'] = 'sans-serif'
        ax1 = mal.plot.barh(color=colors, width=1)
        plt.title("Media de las puntuaciones por barrio (al menos 10)", fontsize=20)
        plt.xlabel('Puntuación', fontsize=20)
        plt.ylabel("")
        plt.tight_layout()
        st.pyplot(fig)
        
        listings10 = listings[listings['number_of_reviews'] >= 10]
        fig = plt.figure(figsize=(20, 15))
        plt.rc('xtick', labelsize=16)
        plt.rc('ytick', labelsize=16)
        ax1 = fig.add_subplot(321)
        colors = ["#ADD8E6", "#4682B4", "#1E3A8A", "#000080", "#FFD700", "#FFA500", "#DAA520", "#B8860B"]
        plt.rcParams['axes.prop_cycle'] = plt.cycler(color=colors)
        plt.rcParams['figure.facecolor'] = '#FFFFFF'
        plt.rcParams['axes.facecolor'] = '#FFFFFF'
        plt.rcParams['text.color'] = '#000000'
        plt.rcParams['axes.labelcolor'] = '#000000'
        plt.rcParams['xtick.color'] = '#000000'
        plt.rcParams['ytick.color'] = '#000000'
        plt.rcParams['font.family'] = 'sans-serif'
        sns.histplot(data=listings10, x='review_scores_location', bins=10, kde=True, ax=ax1)
        plt.title("Ubicación", fontsize=24)
        plt.ylabel('Número de alojamientos', fontsize=14)
        plt.xlabel('Puntuación media', fontsize=14)
        st.pyplot(fig) 
        
        listings10 = listings[listings['number_of_reviews'] >= 10]
        fig = plt.figure(figsize=(20, 15))
        plt.rc('xtick', labelsize=16)
        plt.rc('ytick', labelsize=16)
        ax1 = fig.add_subplot(321)
        colors = ["#ADD8E6", "#4682B4", "#1E3A8A", "#000080", "#FFD700", "#FFA500", "#DAA520", "#B8860B"]
        plt.rcParams['axes.prop_cycle'] = plt.cycler(color=colors)
        plt.rcParams['figure.facecolor'] = '#FFFFFF'
        plt.rcParams['axes.facecolor'] = '#FFFFFF'
        plt.rcParams['text.color'] = '#000000'
        plt.rcParams['axes.labelcolor'] = '#000000'
        plt.rcParams['xtick.color'] = '#000000'
        plt.rcParams['ytick.color'] = '#000000'
        plt.rcParams['font.family'] = 'sans-serif'
        sns.histplot(data=listings10, x='review_scores_cleanliness', bins=10, kde=True, ax=ax1)
        plt.title("Limpieza", fontsize=24)
        plt.ylabel('Número de alojamientos', fontsize=14)
        plt.xlabel('Puntuación media', fontsize=14)
        st.pyplot(fig) 
        
        listings10 = listings[listings['number_of_reviews'] >= 10]
        fig = plt.figure(figsize=(20, 15))
        plt.rc('xtick', labelsize=16)
        plt.rc('ytick', labelsize=16)
        ax1 = fig.add_subplot(321)
        colors = ["#ADD8E6", "#4682B4", "#1E3A8A", "#000080", "#FFD700", "#FFA500", "#DAA520", "#B8860B"]
        plt.rcParams['axes.prop_cycle'] = plt.cycler(color=colors)
        plt.rcParams['figure.facecolor'] = '#FFFFFF'
        plt.rcParams['axes.facecolor'] = '#FFFFFF'
        plt.rcParams['text.color'] = '#000000'
        plt.rcParams['axes.labelcolor'] = '#000000'
        plt.rcParams['xtick.color'] = '#000000'
        plt.rcParams['ytick.color'] = '#000000'
        plt.rcParams['font.family'] = 'sans-serif'
        sns.histplot(data=listings10, x='review_scores_accuracy', bins=10, kde=True, ax=ax1)
        plt.title("Veracidad", fontsize=24)
        plt.ylabel('Número de alojamientos', fontsize=14)
        plt.xlabel('Puntuación media', fontsize=14)
        st.pyplot(fig) 
        
        listings10 = listings[listings['number_of_reviews'] >= 10]
        fig = plt.figure(figsize=(20, 15))
        plt.rc('xtick', labelsize=16)
        plt.rc('ytick', labelsize=16)
        ax1 = fig.add_subplot(321)
        colors = ["#ADD8E6", "#4682B4", "#1E3A8A", "#000080", "#FFD700", "#FFA500", "#DAA520", "#B8860B"]
        plt.rcParams['axes.prop_cycle'] = plt.cycler(color=colors)
        plt.rcParams['figure.facecolor'] = '#FFFFFF'
        plt.rcParams['axes.facecolor'] = '#FFFFFF'
        plt.rcParams['text.color'] = '#000000'
        plt.rcParams['axes.labelcolor'] = '#000000'
        plt.rcParams['xtick.color'] = '#000000'
        plt.rcParams['ytick.color'] = '#000000'
        plt.rcParams['font.family'] = 'sans-serif'
        sns.histplot(data=listings10, x='review_scores_communication', bins=10, kde=True, ax=ax1)
        plt.title("Comunicación", fontsize=24)
        plt.ylabel('Número de alojamientos', fontsize=14)
        plt.xlabel('Puntuación media', fontsize=14)
        st.pyplot(fig) 
        
        st.image(r'mapa palabras.png')

p4=st.Page(Análisis, title='Análisis exploratorio de los datos')
            
def Ayuntamiento():
    st.title('Problemáticas derivadas de los Airbnb')
    imagen_path_crecimiento_urbano = r'CRECIMIENTO_URBANO_MALAGA_FUENTE-DIARIOSUR.ES.jpg'
    st.image(imagen_path_crecimiento_urbano)
    st.caption('Fuente: Diario Sur, 2021')
    st.write("""En este mapa se puede observar el **crecimiento urbano de Málaga** en los últimos años. No obstante, gran parte de este crecimiento se ha transformado en la **masificación de vivienda turística**. 
                Bajo el lema "Málaga para vivir, no para sobrevivir", más de 25.000 manifestantes según la organización y 5.500 según datos de la Policía Nacional, se lanzaron a la calle para denunciar la complicada situación del mercado de la vivienda que afronta la capital malagueña, que sigue ocupando los primeros puestos en los rankings nacionales en cuanto a la **escalada de precios**, así como los procesos de turistificación que empezaron en el primer distrito de la capital y que se extienden ya hasta los barrios, con la **proliferación de viviendas turísticas** o la **desaparición del comercio tradicional** con la reconversión de locales comerciales (*El día, 2024*).""")
    st.image(r'MANI_VIVIENDA_3_FUENTE_EL_ESPAÑOL 1.png')
    st.caption('Fuente: El Español, 2024')
    st.empty()            
    st.write("""Por otro lado, la proliferación de viviendas turísticas ha sido un factor determinante en la problemática existente de la **contaminación acústica**, para la que se ha creado una Asociación vecinal que lucha contra la misma (*La opinión de Málaga, 2024*).""")
    st.image(r'ASOC_VECINAL_RUIDO_FUENTE_LA_OPINION_DE_MALAGA 1.png')
    st.caption('Fuente: La opinión de Málaga, 2024')
    st.write("""Podemos observar como las quejas de la población a la policía por el ruido han ido en aumento año tras año, pasando de 11442 quejas en el año 2011 a 16497 en el año 2020, lo que supone un incremento de las quejas en un 30,6%.
            Les mostramos un gráfico en el cual se ve el aumento de las quejas de los vecinos en los últimos años:""")
    st.image(r'DENUNCIAS VECINOS RUIDOS-2-FUENTE-TECHNI-ACUSTICA 1.jpg')
    st.caption('Fuente: Techni-acústica Elche, 2022')
    st.write("""Ambos problemas se conocen en el ámbito de la economía como **externalidades negativas**, es decir, efectos negativos que no son tenidos en cuenta por el mercado y que afectan a terceros, en este caso, a los vecinos de los barrios de Málaga.""")
    st.write("""En cuanto a **soluciones**, el Gobierno ha adoptado una serie de medidas entre las que está una nueva ordenanza que debe **limitar la posibilidad de abrir nuevas viviendas turísticas** en relación con la saturación del barrio en el que se encuentren, **las viviendas deberán contar con una entrada independiente** (*Málaga hoy, 2024*).
             A esta última limitación, se suma que el consistorio está estudiando si puede acotar que **los locales comerciales convertidos en vivienda deban estar "algo más de un año" en alquiler de larga estancia** antes de ofertarse como turístico.
            Otra posible solución que proponemos es el **fomento de los hoteles**, quizá mediante un **impuesto pigouviano a los Airbnb**, por parte de las autoridades gubernamentales. Como vemos, los hoteles nunca llegan a estar ni al 80% de ocupación, con lo que se podrían adaptar a la demanda y movilizarla hacia el turismo hotelero, bajando así la presión en el mercado de la vivienda y cualquier otro negocio, a la par que se reduciría la contaminación acústica.""")
    st.write("""Nos aventuramos a proponer esta idea ya que, como podemos ver en la siguiente gráfica, la ocupación hotelera no llega ni al 80%:""")
    iframe_code = """
    <iframe id='ep-chart-a74334c8-876c-421d-92ae-a53c2ca35fe0-4282' src='https://embed.epdata.es/representacion/a74334c8-876c-421d-92ae-a53c2ca35fe0-4282/450' style='width: 100%; min-height: 450px; overflow: hidden;' frameborder='0' scrolling='no' height='450'></iframe>
    """
    st.markdown(iframe_code, unsafe_allow_html=True)
    st.caption('Fuente: EPData, INE, 2024')
    
p5=st.Page(Ayuntamiento, title='Problemáticas derivadas de los Airbnb')

def Perspectivas_clave():
    st.title('Perspectivas clave')
    power_bi_url = "https://app.powerbi.com/view?r=eyJrIjoiOTYyOWY1NzUtYmE1My00OTIxLWIxZmYtMDc5ZmQyNzdhNjgyIiwidCI6IjhhZWJkZGI2LTM0MTgtNDNhMS1hMjU1LWI5NjQxODZlY2M2NCIsImMiOjl9"
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center;">
            <iframe title="Informe de Power BI" width="1100" height="800" src="{power_bi_url}" frameborder="0" allowFullScreen="true"></iframe>
        </div>
        """,
        unsafe_allow_html=True
    )
    
p6=st.Page(Perspectivas_clave, title='Perspectivas clave')

def Conclusiones():
    st.title('Conclusiones')
    texto_conclusiones = """
    **CONCLUSIONES DEL ESTUDIO DEL ANÁLISIS Y VISUALIZACIÓN DE LOS DATOS:**

    - Los **hoteles nunca** llegan a tener una **ocupación superior al 80%**.
    - El tipo de **alojamiento más demandado** es el **apartamento**.
    - Dado el punto anterior, el **nº. de huéspedes más habitual** es el de **4** huéspedes, aunque le **siguen** los **2 huéspedes**.
    - Las **zonas más tensionadas** por estos alojamientos son la **zona Centro y la Este**, aunque la **más cara** sería la zona de la **Carretera de Cádiz**, coincidiendo con esta zona con la que más alojamientos ofrece **para 4 personas**.

    - Los **Airbnb en Málaga** han supuesto un **crecimiento excepcional** de la oferta turística, lo que agrava dos problemas:
        - La **contaminación acústica**, sobre todo en la zona centro, que debido al alto índice de turismo que la ciudad tiene durante todo el año, este se magnifica cuantiosamente con los alojamientos turísticos.
        - **Problemas de acceso a la vivienda**, los alojamientos turísticos contribuyen claramente al tensionamiento de los alquileres sobre todo en las zonas en las que más Airbnb hay, dificultando a los ciudadanos malagueños el acceso a la vivienda a un precio digno.
        - Al mismo tiempo se reducen los **locales comerciales**, pues estos son convertidos en pisos turísticos.
    
    - Para **mitigar** estos problemas, se han propuesto soluciones como **limitar la posibilidad de abrir nuevas viviendas turísticas** o **fomentar los hoteles**.
    - En definitiva, es necesario tomar medidas para garantizar la sostenibilidad del turismo en Málaga y para mejorar la calidad de vida de los vecinos.
    - **SÍ AL TURISMO, PERO A UN TURISMO SOSTENIBLE**.
    """
    st.markdown(texto_conclusiones)
    
p7=st.Page(Conclusiones, title='Conclusiones')


pg=st.navigation([p1, p2, p3, p4, p5, p6, p7
                  ])
pg.run()
