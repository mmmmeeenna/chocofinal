# Importar librerías necesarias para Streamlit
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium # Importar st_folium

# Especificaciones de formato para que sea vea tipo blog con los colores deseados
st.markdown("""
<style>
    /* Fondo base chocolate claro y forzar esquema claro */
    .stApp {
        background-color: #AD9682;
        font-family: 'Trebuchet MS', 'Comic Sans MS', cursive;
        color: #4e342e !important; /* Color de texto por defecto */
        color-scheme: light !important; /* Forzar modo claro en navegadores que usan dark mode */
    }

    /* Franja superior con imagen decorativa */
    .top-banner {
        background-image: url('https://raw.githubusercontent.com/mmmmeeenna/chocofinal/refs/heads/main/images/fondo%20con%20fondo.png');
        background-size: cover;
        background-position: center;
        height: 180px;
        border-bottom: 6px solid #6d4c41;
    }

    /* Estilo del sidebar */
    [data-testid="stSidebar"] {
        background-color: #6E5846;
        border-right: 3px dashed #AD9682;
        color: white;  /* Para que el texto resalte */
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
        color: #5d4037 !important;  /* Forzamos el color */
        background-color: transparent !important; /* por si algún fondo oscuro se cuela */
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


@st.cache_data
def load_data():
    """Loads and transforms the chocolate and store dataframes."""
    #Se cargan las bases de datos en Excel 
    try:
        chocoframe = pd.read_excel('chocodata_revisada.xlsx')
        chocotiendas = pd.read_excel('chocotiendas.xlsx')
    except FileNotFoundError:
        st.error("Asegúrate de que 'chocodata_revisada.xlsx' y 'chocotiendas.xlsx' estén en el mismo directorio que el script.")
        st.stop() #Detiene la ejecución de la aplicación si los archivos no se encuentran


    #Acá se transforman los datos según lo que se necesita 
    conv_booleanos = chocoframe.columns[1:16] # Estas son las características, por eso las convierto a booleanos para luego poder analizarlas 
    chocoframe[conv_booleanos] = chocoframe[conv_booleanos].astype(bool)

    conv_float = chocoframe.columns[16:31] #Estos valores son los precios los convierto a float para compararlos, tal vez en un futuro añada esta opción
    chocoframe[conv_float] = chocoframe[conv_float].apply(pd.to_numeric, errors='coerce').astype(float)

    conv_string = chocoframe.columns[31:34]
    chocoframe[conv_string] = chocoframe[conv_string].astype(str)

    # Clean column names by stripping whitespace (esto lo añadió la IA al traducirlo)
    chocoframe.columns = chocoframe.columns.str.strip()
    chocotiendas.columns = chocotiendas.columns.str.strip()


    return chocoframe, chocotiendas
    
#Añado una imagen para que se vea más atractivo
st.sidebar.image(
    "https://raw.githubusercontent.com/mmmmeeenna/chocofinal/refs/heads/main/images/chocolates%20tres%20tipos.png",
    use_container_width=True
)

#Sidebar para poder navegar
st.sidebar.title("Navegación")
pages = ("Página 1: Buscador", "Página 2: Ámate con chocolate", "Página 3: Detrás del Chocolate") #Son tres páginas, la primera es el cuestionario y las demás recomendaciones
selected_page = st.sidebar.radio("Ir a:", pages) 

if selected_page == "Página 1: Buscador":
    chocoframe, chocotiendas = load_data()

#Esta es para ir al cuestionario 
if selected_page == "Página 1: Buscador":
    st.write("¡Encuentra tu chocolate ideal en el campus PUCP!")

    #Decoración
    st.markdown('<div class="top-banner"></div>', unsafe_allow_html=True)

    #Título principal después del banner
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

    #Primera pregunta 
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
        "¿Deseas comer chocolate?", #Esta es la pregunta que inicia o termina todo el programa 
        ('Sí', 'No'),
        index=0
    )
    #Estas son las variables en donde se almacenarán los datos, empiezan vacías
    q2_answer = None
    q_ad_answer = None
    q2_1_answer = None
    q2_2_answer = None
    acentos_tipo_answer = None
    keke_acentos_subtipo_answer = None
    galleta_acentos_subtipo_answer = None

    #Advertencia real solo si dijeron que sí en la primera pregunta
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

    #Pregunta 2 (solo si la Q1 es 'Sí')
        q2_answer = st.radio(
            "¿Deseas comer sólo chocolate (en barra o lentejitas), un derivado hecho en su mayoría de chocolate o un derivado con acentos de chocolate?",
            ('Solo de chocolate', 'Hecho en su mayoría de chocolate', 'Con acentos de chocolate')
        )#Aquí preguntamos específicamente que cantidad de chocolate se desea consumir 

        #Aquí, si se ha respondido "Solo de chocolate" se responde con la pregunta sobre el contenido de esa barra o lentejita de chocolate
    if q2_answer == 'Solo de chocolate':
        q_ad_answer = st.radio(
            "¿Prefieres chocolates con maní o almendras?",
            ('Con maní', 'Sin maní', 'Con Almendras', 'Sin Almendras')
        )

    # Luego de eso, se le preguntará qué tipo de chocolate prefiere
        q2_1_answer = st.radio(
            "¿Deseas comer chocolate con leche, blanco o puro (mayor porcentaje de cacao)?",
            ('Con leche', 'Blanco', 'Puro')
        )

    elif q2_answer == 'Hecho en su mayoría de chocolate': #Si se ha respondido que se quiere 'Hecho en su mayoría de chocolate' mostrará los formatos en los que se presentan los productos hechos en su mayoría de chocolate
        q2_2_answer = st.radio(
            "¿Cuál te llama más la atención: Galleta, Keke u otro postre?",
            ('Galleta', 'Keke', 'Otro postre')
        ) 

    elif q2_answer == 'Con acentos de chocolate': #Esta es la otra alternativa a la pregunta 2
        acentos_tipo_answer = st.radio(
            "¿Prefieres un keke o una galleta con acentos de chocolate?",
            ('Keke', 'Galleta') #Se puede responder solo con estos formatos de alimento porque no hay un "postre" asignado pra 
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

                # Inicia tarjeta de producto
                st.markdown(f"""
                <div style='background-color: rgba(255, 255, 255, 0.95); 
                            padding: 25px; 
                            margin: 30px 0; 
                            border-radius: 20px; 
                            box-shadow: 0 4px 15px rgba(0,0,0,0.15);'>
                    <h3 style='color: #4e342e; font-family: "Trebuchet MS", "Comic Sans MS", cursive; text-align: center;'>
                        🍫 {nombre_producto}
                    </h3>
                """, unsafe_allow_html=True)

                # Imagen del producto
                if pd.notna(imagen_producto) and isinstance(imagen_producto, str):
                    st.image(imagen_producto, width=320)
                else:
                    st.markdown("<p style='text-align: center; color: #8d6e63;'>Imagen no disponible</p>", unsafe_allow_html=True)

                # Precios disponibles
                precio_columnas = current_filtered_frame.columns[16:31]
                precios_disponibles = [
                    f"<li><strong>{col.strip()}</strong>: S/ {row[col]:.2f}</li>"
                    for col in precio_columnas if pd.notna(row[col])
                ]

                if precios_disponibles:
                    precios_html = "<ul style='color:#5d4037; font-size: 17px;'>" + "".join(precios_disponibles) + "</ul>"
                    st.markdown(f"""
                    <div style='margin-top: 15px;'>
                        <p style='font-size: 18px; font-weight: bold; color: #6d4c41;'>Precios disponibles:</p>
                        {precios_html}
                    </div>
                    </div> <!-- cierre tarjeta -->
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style='margin-top: 15px; color:#8d6e63; font-size:16px;'>No se encontraron precios disponibles para este producto.</div>
                    </div> <!-- cierre tarjeta -->
                    """, unsafe_allow_html=True)

                # Línea divisoria
                st.markdown("<hr style='border: none; height: 1px; background-color: #ccc;'>", unsafe_allow_html=True)




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

    # Título bonito con fondo blanco transparente (todo en una línea visualmente)
    st.markdown("""
    <div style='text-align: center; margin-top: 20px;'>
        <h1 style='background-color: rgba(255, 255, 255, 0.9); 
                   display: inline-block; 
                   padding: 15px 35px; 
                   border-radius: 15px; 
                   box-shadow: 2px 4px 10px rgba(0,0,0,0.1);
                   color: #4e342e; 
                   font-family: "Trebuchet MS", "Comic Sans MS", cursive;
                   font-size: 34px;
                   white-space: nowrap;
                   overflow: hidden;
                   text-overflow: ellipsis;'>
            ¿Por qué comer chocolate es bueno?
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
