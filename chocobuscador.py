# Importar librerías necesarias para Streamlit
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium # Importar st_folium

# Aplicar estilo de blog con CSS
st.markdown("""
<style>
    /* Fondo base chocolate claro */
    .stApp {
        background-color: #fff8e1;
        font-family: 'Trebuchet MS', 'Comic Sans MS', cursive;
    }

    /* Franja superior con imagen decorativa */
    .top-banner {
        background-image: url('https://raw.githubusercontent.com/mmmmeeenna/chocofinal/refs/heads/main/images/FONDO.png');
        background-size: cover;
        background-position: center;
        height: 180px;
        border-bottom: 6px solid #6d4c41;
    }

    /* Estilo del sidebar */
    [data-testid="stSidebar"] {
        background-color: #fff3e0;
        background-image: linear-gradient(to bottom, #fff3e0, #fbe9e7);
        border-right: 3px dashed #4e342e;
        padding: 15px;
    }

    /* Cuadro de contenido tipo glassmorphism */
    .glass-box {
        background-color: rgba(255, 255, 255, 0.92);
        padding: 60px 40px 50px 40px;
        border-radius: 25px;
        margin: 60px auto;
        max-width: 750px;
        box-shadow: 0px 8px 24px rgba(0,0,0,0.2);
        text-align: center;
    }

    /* Títulos principales */
    h1 {
        color: #4e342e;
        font-size: 42px;
        text-shadow: 2px 2px 4px #fff;
        margin-bottom: 20px;
    }

    /* Preguntas del cuestionario */
    .pregunta {
        font-size: 26px;
        font-weight: bold;
        color: #5d4037;
        margin: 30px 0 40px 0;
        text-shadow: 1px 1px 2px rgba(255,255,255,0.5);
    }

    /* Estilo de botones */
    .stButton>button {
        background-color: #6d4c41;
        color: white;
        font-size: 22px;
        font-weight: bold;
        border-radius: 14px;
        padding: 15px 40px;
        margin: 20px 10px;
        border: none;
        box-shadow: 2px 4px 8px rgba(0, 0, 0, 0.25);
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #8d6e63;
        transform: scale(1.05);
    }
</style>
""", unsafe_allow_html=True)

# Cargar y preparar los datos
@st.cache_data
def load_data():
    """Loads and transforms the chocolate and store dataframes."""
    # Load the dataframes
    # Asegúrate de que estos archivos ('chocodata_revisada.xlsx' y 'chocotiendas.xlsx')
    # estén en el mismo directorio que tu script de Streamlit o proporciona la ruta completa.
    try:
        chocoframe = pd.read_excel('chocodata_revisada.xlsx')
        chocotiendas = pd.read_excel('chocotiendas.xlsx')
    except FileNotFoundError:
        st.error("Asegúrate de que 'chocodata_revisada.xlsx' y 'chocotiendas.xlsx' estén en el mismo directorio que el script.")
        st.stop() # Detiene la ejecución de la aplicación si los archivos no se encuentran


    # Transform chocoframe data types
    conv_booleanos = chocoframe.columns[1:16]
    chocoframe[conv_booleanos] = chocoframe[conv_booleanos].astype(bool)

    conv_float = chocoframe.columns[16:31]
    chocoframe[conv_float] = chocoframe[conv_float].apply(pd.to_numeric, errors='coerce').astype(float)

    conv_string = chocoframe.columns[31:34]
    chocoframe[conv_string] = chocoframe[conv_string].astype(str)

    # Clean column names by stripping whitespace
    chocoframe.columns = chocoframe.columns.str.strip()
    chocotiendas.columns = chocotiendas.columns.str.strip()


    return chocoframe, chocotiendas

if selected_page == "Página 1: Buscador":
    chocoframe, chocotiendas = load_data()

# Imagen decorativa en el sidebar
st.sidebar.image(
    "https://raw.githubusercontent.com/mmmmeeenna/chocofinal/refs/heads/main/images/chocolates%20tres%20tipos.png",
    use_container_width=True
)

# Sidebar con navegación
st.sidebar.title("Navegación")
pages = ("Página 1: Buscador", "Página 2: Ámate con chocolate", "Página 3: Detrás del Chocolate")
selected_page = st.sidebar.radio("Ir a:", pages) 

# Contenido de las páginas
if selected_page == "Página 1: Buscador":
    st.write("¡Encuentra tu chocolate ideal en el campus PUCP!")

    # Franja decorativa superior
    st.markdown('<div class="top-banner"></div>', unsafe_allow_html=True)

    # Título principal después del banner
    st.markdown("""
    <div style='text-align: center; margin-top: 20px; margin-bottom: 10px;'>
        <h1 style='background-color: rgba(255, 255, 255, 0.9); 
                   display: inline-block; 
                   padding: 10px 25px; 
                   border-radius: 15px; 
                   box-shadow: 2px 4px 10px rgba(0,0,0,0.1);
                   color: #4e342e; 
                   font-family: "Trebuchet MS", "Comic Sans MS", cursive;
                   font-size: 38px;'>
            🍫 Buscador de Chocolates
        </h1>
    </div>
    """, unsafe_allow_html=True)

    # Question 1
    with st.container():
        st.markdown("""
        <div style="text-align: center; margin-bottom: -10px;">
            <img src="https://raw.githubusercontent.com/mmmmeeenna/chocofinal/refs/heads/main/images/mounstrito.png"
                 alt="Monstruito come galletas"
                 style="width: 120px; height: auto; margin-bottom: -10px;" />
        </div>

        <div style="padding: 25px; border-radius: 20px; background-color: #fff3e0; border: 2px dashed #bf360c; text-align: center;">
            <h2 style="color: #bf360c;">⚠️ ADVERTENCIA ⚠️</h2>
            <p style="font-size: 20px;">INGRESA A ESTA PÁGINA <strong>SI Y SOLO SI</strong> QUIERES COMER CHOCOLATE 🍫</p>
        </div>
        """, unsafe_allow_html=True)    

    q1_answer = st.radio(
        "¿Deseas comer chocolate?",
        ('Sí', 'No'),
        index=0
    )
    # Initialize variables for answers in different paths
    q2_answer = None
    q_ad_answer = None
    q2_1_answer = None
    q2_2_answer = None
    acentos_tipo_answer = None
    keke_acentos_subtipo_answer = None
    galleta_acentos_subtipo_answer = None

    # Advertencia real solo si dijeron que sí
    if q1_answer == 'Sí':
        st.markdown("""
        <div style="margin-top: 25px; padding: 20px; background-color: #ffebee; border: 2px solid #b71c1c; border-radius: 15px;">
            <h4 style="color: #b71c1c;">🚨 Advertencia importante</h4>
            <p style="color: #5d4037; font-size: 17px;">
                Todos los productos contienen lactosa.<br>
                <strong>No son aptos para personas veganas ni diabéticas.</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Question 2 (only if Q1 is 'Sí')
        q2_answer = st.radio(
            "¿Deseas comer sólo chocolate (en barra o lentejitas), un derivado hecho en su mayoría de chocolate o un derivado con acentos de chocolate?",
            ('Solo de chocolate', 'Hecho en su mayoría de chocolate', 'Con acentos de chocolate')
        )

        # Question path based on Q2 answer
    if q2_answer == 'Solo de chocolate':
        q_ad_answer = st.radio(
            "¿Prefieres chocolates con maní o almendras?",
            ('Con maní', 'Sin maní', 'Con Almendras', 'Sin Almendras')
        )

    # Subsequent question for "Solo de chocolate" path
        q2_1_answer = st.radio(
            "¿Deseas comer chocolate con leche, blanco o puro (mayor porcentaje de cacao)?",
            ('Con leche', 'Blanco', 'Puro')
        )

    elif q2_answer == 'Hecho en su mayoría de chocolate':
        q2_2_answer = st.radio(
            "¿Cuál te llama más la atención: Galleta, Keke u otro postre?",
            ('Galleta', 'Keke', 'Otro postre')
        )

    elif q2_answer == 'Con acentos de chocolate':
        acentos_tipo_answer = st.radio(
            "¿Prefieres un keke o una galleta con acentos de chocolate?",
            ('Keke', 'Galleta')
        )

    # Subsequent questions based on acentos_tipo_answer
        if acentos_tipo_answer == 'Keke':
            keke_acentos_subtipo_answer = st.radio(
                "¿Prefieres tu keke con chispas o bañado en chocolate?",
                ('Con chispas', 'Bañado')
            )
        elif acentos_tipo_answer == 'Galleta':
            galleta_acentos_subtipo_answer = st.radio(
                "¿Prefieres tu galleta con chispas, bañada o rellena de chocolate?",
                ('Con chispas', 'Bañada', 'Rellena')
            )

    # Implementar la lógica de filtrado basada en las selecciones de streamlit
    # Inicializar el DataFrame filtrado con el original antes de aplicar filtros
    current_filtered_frame = chocoframe.copy()


    if q1_answer == 'Sí':
        # Filtering based on the second question
        if q2_answer == 'Solo de chocolate':
            col_solo_chocolate = 'barra de chocolate'
            if col_solo_chocolate in current_filtered_frame.columns:
                current_filtered_frame = current_filtered_frame.loc[current_filtered_frame[col_solo_chocolate] == True].copy()
            else:
                st.warning(f"Advertencia: Columna '{col_solo_chocolate}' no encontrada para filtrar.")

            # Filtering based on the maní/almendras question (Q_AD)
            if not current_filtered_frame.empty and q_ad_answer is not None: # Add check for q_ad_answer
                if q_ad_answer == "Con maní":
                    col_mani = 'maní'
                    if col_mani in current_filtered_frame.columns:
                        current_filtered_frame = current_filtered_frame.loc[current_filtered_frame[col_mani] == True].copy()
                    else:
                        st.warning(f"Advertencia: Columna '{col_mani}' no encontrada para filtrar.")
                elif q_ad_answer == "Sin maní":
                    col_mani = 'maní'
                    if col_mani in current_filtered_frame.columns:
                        current_filtered_frame = current_filtered_frame.loc[current_filtered_frame[col_mani] == False].copy()
                    else:
                        st.warning(f"Advertencia: Columna '{col_mani}' no encontrada para filtrar.")
                elif q_ad_answer == "Con Almendras":
                    col_almendras = 'almendras'
                    if col_almendras in current_filtered_frame.columns:
                        current_filtered_frame = current_filtered_frame.loc[current_filtered_frame[col_almendras] == True].copy()
                    else:
                        st.warning(f"Advertencia: Columna '{col_almendras}' no encontrada para filtrar.")
                elif q_ad_answer == "Sin Almendras":
                    col_almendras = 'almendras'
                    if col_almendras in current_filtered_frame.columns:
                        current_filtered_frame = current_filtered_frame.loc[current_filtered_frame[col_almendras] == False].copy()
                    else:
                        st.warning(f"Advertencia: Columna '{col_almendras}' no encontrada para filtrar.")

            # Filtering based on the chocolate type question (Q2_1)
            if not current_filtered_frame.empty and q2_1_answer is not None: # Add check for q2_1_answer
                 if q2_1_answer == "Con leche":
                    col_leche = 'chocolate con leche'
                    if col_leche in current_filtered_frame.columns:
                        current_filtered_frame = current_filtered_frame.loc[current_filtered_frame[col_leche] == True].copy()
                    else:
                        st.warning(f"Advertencia: Columna '{col_leche}' no encontrada para filtrar.")
                 elif q2_1_answer == "Blanco":
                    col_blanco = 'chocolate blanco'
                    if col_blanco in current_filtered_frame.columns:
                        current_filtered_frame = current_filtered_frame.loc[current_filtered_frame[col_blanco] == True].copy()
                    else:
                        st.warning(f"Advertencia: Columna '{col_blanco}' no encontrada para filtrar.")
                 elif q2_1_answer == "Puro":
                    col_puro = 'chocolate puro'
                    if col_puro in current_filtered_frame.columns:
                        current_filtered_frame = current_filtered_frame.loc[current_filtered_frame[col_puro] == True].copy()
                    else:
                        st.warning(f"Advertencia: Columna '{col_puro}' no encontrada para filtrar.")


        elif q2_answer == 'Hecho en su mayoría de chocolate':
            col_hecho_mayoria = 'producto hecho de chocolate'
            if col_hecho_mayoria in current_filtered_frame.columns:
                current_filtered_frame = current_filtered_frame.loc[current_filtered_frame[col_hecho_mayoria] == True].copy()
            else:
                st.warning(f"Advertencia: Columna '{col_hecho_mayoria}' no encontrada para filtrar.")

            # Filtering based on the Galleta/Keke/Postre question (Q2_2)
            if not current_filtered_frame.empty and q2_2_answer is not None: # Add check for q2_2_answer
                if q2_2_answer == "Galleta":
                    col_galleta = 'galleta'
                    if col_galleta in current_filtered_frame.columns:
                        current_filtered_frame = current_filtered_frame.loc[current_filtered_frame[col_galleta] == True].copy()
                    else:
                        st.warning(f"Advertencia: Columna '{col_galleta}' no encontrada para filtrar.")

                elif q2_2_answer == "Keke":
                    col_keke = 'keke'
                    if col_keke in current_filtered_frame.columns:
                        current_filtered_frame = current_filtered_frame.loc[current_filtered_frame[col_keke] == True].copy()
                    else:
                        st.warning(f"Advertencia: Columna '{col_keke}' no encontrada para filtrar.")

                elif q2_2_answer == "Otro postre":
                    col_otro_postre = 'postre'
                    if col_otro_postre in current_filtered_frame.columns:
                        current_filtered_frame = current_filtered_frame.loc[current_filtered_frame[col_otro_postre] == True].copy()
                    else:
                        st.warning(f"Advertencia: Columna '{col_otro_postre}' no encontrada para filtrar.")


        elif q2_answer == 'Con acentos de chocolate':
            col_acentos = 'producto con chocolate'
            if col_acentos in current_filtered_frame.columns:
                current_filtered_frame = current_filtered_frame.loc[current_filtered_frame[col_acentos] == True].copy()
            else:
                st.warning(f"Advertencia: Columna '{col_acentos}' no encontrada para filtrar.")

            # Filtering based on the Keke or Galleta question (acentos_tipo)
            if not current_filtered_frame.empty and acentos_tipo_answer is not None: # Add check for acentos_tipo_answer
                if acentos_tipo_answer == "Keke":
                    col_keke_acentos = 'keke'
                    if col_keke_acentos in current_filtered_frame.columns:
                        current_filtered_frame = current_filtered_frame.loc[current_filtered_frame[col_keke_acentos] == True].copy()
                        if not current_filtered_frame.empty and keke_acentos_subtipo_answer is not None: # Add check for keke_acentos_subtipo_answer
                             # Filtering based on the keke subtipo question (keke_acentos_subtipo)
                             if keke_acentos_subtipo_answer == "Con chispas":
                                 col_keke_chispas = 'con chispas'
                                 if col_keke_chispas in current_filtered_frame.columns:
                                     current_filtered_frame = current_filtered_frame.loc[current_filtered_frame[col_keke_chispas] == True].copy()
                                 else:
                                     st.warning(f"Advertencia: Columna '{col_keke_chispas}' no encontrada para filtrar.")
                             elif keke_acentos_subtipo_answer == "Bañado":
                                  col_keke_banado = 'bañada'
                                  if col_keke_banado in current_filtered_frame.columns:
                                     current_filtered_frame = current_filtered_frame.loc[current_filtered_frame[col_keke_banado] == True].copy()
                                  else:
                                     st.warning(f"Advertencia: Columna '{col_keke_banado}' no encontrada para filtrar.")

                else:
                    st.warning(f"Advertencia: Columna '{col_keke_acentos}' no encontrada para filtrar.")


            elif acentos_tipo_answer == "Galleta":
                col_galleta_acentos = 'galleta'
                if col_galleta_acentos in current_filtered_frame.columns:
                    current_filtered_frame = current_filtered_frame.loc[current_filtered_frame[col_galleta_acentos] == True].copy()
                    if not current_filtered_frame.empty and galleta_acentos_subtipo_answer is not None: # Add check for galleta_acentos_subtipo_answer
                         # Filtering based on the galleta subtipo question (galleta_acentos_subtipo)
                         if galleta_acentos_subtipo_answer == "Con chispas":
                             col_galleta_chispas = 'con chispas'
                             if col_galleta_chispas in current_filtered_frame.columns:
                                 current_filtered_frame = current_filtered_frame.loc[current_filtered_frame[col_galleta_chispas] == True].copy()
                             else:
                                 st.warning(f"Advertencia: Columna '{col_galleta_chispas}' no encontrada para filtrar.")
                         elif galleta_acentos_subtipo_answer == "Bañada":
                             col_galleta_banada = 'bañada'
                             if col_galleta_banada in current_filtered_frame.columns:
                                 current_filtered_frame = current_filtered_frame.loc[current_filtered_frame[col_galleta_banada] == True].copy()
                             else:
                                 st.warning(f"Advertencia: Columna '{col_galleta_banada}' no encontrada para filtrar.")
                         elif galleta_acentos_subtipo_answer == "Rellena":
                             col_rellena = 'rellena'
                             if col_rellena in current_filtered_frame.columns:
                                 current_filtered_frame = current_filtered_frame.loc[current_filtered_frame[col_rellena] == True].copy()
                             else:
                                 st.warning(f"Advertencia: Columna '{col_rellena}' no encontrada para filtrar.")
                    else:
                         st.warning(f"Advertencia: Columna '{col_galleta_acentos}' no encontrada para filtrar.")

    else:
        st.info("Ok, quizás en otro momento. ¡Adiós!") # Display the "Goodbye" message


    # Mostrar los resultados (productos y mapa) usando elementos de Streamlit
    if q1_answer == 'Sí': # Only display results if the user wants chocolate
        if not current_filtered_frame.empty:
            # Add a count of available options
            st.subheader(f"Se encontraron {len(current_filtered_frame)} opciones de chocolate que coinciden con tus preferencias:")

            # Display product information first
            st.subheader("Detalles de los productos:")
            for index, row in current_filtered_frame.iterrows():
                nombre_producto = row["producto"]
                imagen_producto = row["Foto"]

                st.write(f"**Producto:** {nombre_producto}")

                if pd.notna(imagen_producto) and isinstance(imagen_producto, str):
                     st.image(imagen_producto, width=300)
                else:
                     st.write("  Imagen no disponible")

                precio_columnas = current_filtered_frame.columns[16:31]
                precios_encontrados = False
                st.write("**Precios disponibles:**")
                for col in precio_columnas:
                    precio = row[col]
                    if pd.notna(precio):
                        st.write(f"- {col.strip()}: {precio}")
                        precios_encontrados = True

                if not precios_encontrados:
                    st.write("  No se encontraron precios disponibles para este producto en las ubicaciones listadas.")
                st.markdown("---") # Separator between products


            # Create and display the map after product details
            st.subheader("Mapa de ubicaciones con productos disponibles:")

            map_center = [-12.069, -77.08]
            m = folium.Map(location=map_center, zoom_start=14)

            location_columns = current_filtered_frame.columns[16:31]

            for col in location_columns:
                location_name = col.strip()
                location_info = chocotiendas[chocotiendas['Establecimiento'] == location_name]

                if not location_info.empty:
                    lat = location_info['lat'].iloc[0]
                    lon = location_info['lon'].iloc[0]
                    horario = location_info['horario'].iloc[0]

                    popup_content = f"<b>{location_name}</b><br>Horario: {horario}<br><br><b>Productos Disponibles:</b><br>"

                    products_at_location = False
                    for index, product_row in current_filtered_frame.iterrows():
                        product_name = product_row["producto"]
                        price = product_row[col]

                        if pd.notna(price):
                            popup_content += f"- {product_name}: {price}<br>"
                            products_at_location = True

                    if products_at_location:
                        folium.Marker(
                            location=[lat, lon],
                            popup=folium.Popup(popup_content, max_width=300),
                            icon=folium.Icon(color='green', icon='cutlery')
                        ).add_to(m)
                    # No need for an else here, as we only add markers for locations with products

                else:
                    st.warning(f"Advertencia: Ubicación '{location_name}' no encontrada en el DataFrame chocotiendas.")

            # Display the map using st_folium
            st_folium(m, width=700, height=450) # Kept the adjusted height

        else:
            st.info("Lo siento, no se encontraron productos que coincidan con todas tus preferencias.")

elif selected_page == "Página 2: Ámate con chocolate":
    # Franja decorativa superior
    st.markdown('<div class="top-banner"></div>', unsafe_allow_html=True)

    # Título bonito con fondo blanco transparente
    st.markdown("""
    <div style='text-align: center; margin-top: 20px;'>
        <h1 style='background-color: rgba(255, 255, 255, 0.9); 
                   display: inline-block; 
                   padding: 15px 35px; 
                   border-radius: 15px; 
                   box-shadow: 2px 4px 10px rgba(0,0,0,0.1);
                   color: #4e342e; 
                   font-family: "Trebuchet MS", "Comic Sans MS", cursive;
                   font-size: 38px;'>
            ☕️ ¿Por qué comer chocolate es bueno?
        </h1>
    </div>
    """, unsafe_allow_html=True)

    # Imagen del monstruo come galletas comiendo
    st.image("https://raw.githubusercontent.com/mmmmeeenna/chocofinal/refs/heads/main/images/mounstro%20comiendo.png", width=250)

    # Texto explicativo con citas
    st.markdown("""
    <div style='background-color: rgba(255,255,255,0.92); padding: 30px; border-radius: 20px;'>
    <p style='font-size: 20px; color: #5d4037;'>
    El chocolate no solo es delicioso, sino que también tiene <strong>efectos positivos en nuestro cerebro</strong>. 
    De acuerdo con <em>National Geographic</em> (2023), el chocolate:
    </p>
    <ul style='font-size: 18px; color: #4e342e;'>
        <li><strong>Activa la serotonina</strong>, mejorando nuestro estado de ánimo y provocando sensaciones de bienestar.</li>
        <li><strong>Genera deseo</strong>, ya que activa regiones del cerebro relacionadas con el placer y la motivación.</li>
        <li><strong>Produce placer</strong> gracias a compuestos como la <em>teobromina</em> y la <em>feniletilamina</em>.</li>
        <li><strong>Mejora el flujo sanguíneo</strong> gracias a los flavanoles presentes en el cacao oscuro.</li>
    </ul>
    <p style='font-size: 18px; color: #6d4c41;'>
    Cuanto más oscuro el chocolate, más beneficios contiene ✨. 
    </p>
    <p style='font-size: 16px; color: #8d6e63;'>
    Fuente: National Geographic (2023). 
    <a href='https://www.nationalgeographicla.com/ciencia/2023/09/que-efecto-produce-el-chocolate-en-el-cerebro' target='_blank'>
    Qué efecto produce el chocolate en el cerebro
    </a>
    </p>
    </div>
    """, unsafe_allow_html=True)

    # Carrusel de imágenes con chocolate
    col1, col2, col3 = st.columns(3)

    with col1:
        st.image("https://raw.githubusercontent.com/mmmmeeenna/chocofinal/refs/heads/main/images/torta.png", caption="Torta de chocolate", use_container_width=True)
    with col2:
        st.image("https://raw.githubusercontent.com/mmmmeeenna/chocofinal/refs/heads/main/images/brownie.png", caption="Brownie", use_container_width=True)
    with col3:
        st.image("https://raw.githubusercontent.com/mmmmeeenna/chocofinal/refs/heads/main/images/chocolatito.png", caption="Chocolate en barra", use_container_width=True)


elif selected_page == "Página 3: Detrás del Chocolate":
    # Franja decorativa superior
    st.markdown('<div class="top-banner"></div>', unsafe_allow_html=True)

    # Título bonito con fondo blanco transparente
    st.markdown("""
    <div style='text-align: center; margin-top: 20px;'>
        <h1 style='background-color: rgba(255, 255, 255, 0.9); 
                   display: inline-block; 
                   padding: 15px 35px; 
                   border-radius: 15px; 
                   box-shadow: 2px 4px 10px rgba(0,0,0,0.1);
                   color: #4e342e; 
                   font-family: "Trebuchet MS", "Comic Sans MS", cursive;
                   font-size: 38px;'>
            🎬 Videos: El chocolate en tu vida
        </h1>
    </div>
    """, unsafe_allow_html=True)

    # Imagen del monstruo cocinero centrada
    st.markdown("""
    <div style="text-align: center; margin-top: 20px; margin-bottom: 20px;">
        <img src="https://raw.githubusercontent.com/mmmmeeenna/chocofinal/refs/heads/main/images/mounstro%20cocinando%20cortado.png" 
             alt="Monstruo Cocinero" 
             style="width: 220px; height: auto;" />
    </div>
    """, unsafe_allow_html=True)

    # Primer video: Beneficios del chocolate
    st.markdown("## 🍫 Beneficios del chocolate para la salud")
    st.video("https://www.youtube.com/watch?v=Lcw29cUuYSc")
    st.markdown("""
    <div style='background-color: rgba(255,255,255,0.92); padding: 20px; border-radius: 15px;'>
        <p style='font-size: 18px; color: #5d4037;'>
            En este video, el doctor <strong>Francisco Villarreal</strong> nos explica cómo el chocolate puede beneficiar nuestra salud. 
            Desde su laboratorio en la Universidad de San Diego, investiga las propiedades del cacao y su impacto positivo en el cuerpo humano.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Segundo video: Cómo se hace el chocolate
    st.markdown("## 🏭 ¿Cómo se hace el chocolate?")
    st.video("https://www.youtube.com/watch?v=J9G94d9QK08")
    st.markdown("""
    <div style='background-color: rgba(255,255,255,0.92); padding: 20px; border-radius: 15px;'>
        <p style='font-size: 18px; color: #5d4037;'>
            ¿Alguna vez te has preguntado cómo se elabora el chocolate que comes? Este video nos lleva detrás de cámaras para mostrar todo el proceso, 
            desde la <strong>selección y mezcla de granos</strong> hasta el <strong>tueste, descascarillado y trituración</strong>.
        </p>
        <ul style='font-size: 16px; color: #4e342e;'>
            <li><strong>Selección de granos:</strong> por calidad, aroma y origen.</li>
            <li><strong>Tueste:</strong> desarrollo de sabor y aroma mediante calor controlado.</li>
            <li><strong>Descascarillado y trituración:</strong> se obtiene el licor de cacao.</li>
        </ul>
        <p style='font-size: 16px; color: #6d4c41;'>¡Una mirada completa al arte de hacer chocolate! 🍫</p>
    </div>
    """, unsafe_allow_html=True)
