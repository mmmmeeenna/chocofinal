
import streamlit as st
import pandas as pd

# ===================== CSS Y FONDO =====================
st.markdown("""
    <style>
        .stApp {
            background-image: url('https://raw.githubusercontent.com/mmmmeeenna/chocofinal/refs/heads/main/images/FONDO.png');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            font-family: 'Comic Sans MS', cursive;
        }

        [data-testid="stSidebar"] {
            background-color: #d7b49e;
            border-right: 3px solid #6d4c41;
        }

        .glass-box {
            background-color: rgba(255, 255, 255, 0.88);
            padding: 60px 40px 50px 40px;
            border-radius: 25px;
            margin: 60px auto;
            max-width: 750px;
            box-shadow: 0px 8px 24px rgba(0,0,0,0.2);
            text-align: center;
        }

        h1 {
            color: #3e2723;
            font-size: 42px;
            text-shadow: 2px 2px 4px #fff;
            margin-bottom: 20px;
        }

        .pregunta {
            font-size: 26px;
            font-weight: bold;
            color: #5d4037;
            margin: 30px 0 40px 0;
            text-shadow: 1px 1px 2px rgba(255,255,255,0.5);
        }

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

        .cookie-monster {
            display: flex;
            justify-content: center;
            margin-top: 10px;
            margin-bottom: 30px;
        }
        .cookie-monster img {
            width: 180px;
        }

        .si-no-button {
            background-color: #6d4c41;
            color: white;
            font-size: 22px;
            font-weight: bold;
            border-radius: 14px;
            padding: 15px 40px;
            margin: 10px 20px;
            border: none;
            box-shadow: 2px 4px 8px rgba(0, 0, 0, 0.25);
            transition: all 0.3s ease;
            cursor: pointer;
        }

        .si-no-button:hover {
            background-color: #8d6e63;
            transform: scale(1.05);
        }

        .gallery {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 25px;
            padding-top: 30px;
        }

        .gallery img {
            border-radius: 12px;
            transition: transform 0.3s ease;
            width: 120px;
        }

        .gallery img:hover {
            transform: scale(1.15);
        }

        .gallery-caption {
            text-align: center;
            font-size: 14px;
            color: #4e342e;
        }
    </style>
""", unsafe_allow_html=True)

# ===================== DATOS =====================
chocoframe = pd.read_excel("chocodataa.xlsx")
conv_booleanos = chocoframe.columns[1:19]
chocoframe[conv_booleanos] = chocoframe[conv_booleanos].astype(bool)

conv_float = chocoframe.columns[19:34]
chocoframe[conv_float] = chocoframe[conv_float].apply(pd.to_numeric, errors='coerce').astype(float)

conv_string = chocoframe.columns[34:37]
chocoframe[conv_string] = chocoframe[conv_string].astype(str)

# ===================== SIDEBAR CON CHOCOLATES =====================
with st.sidebar:
    st.image(
        "https://raw.githubusercontent.com/mmmmeeenna/chocofinal/refs/heads/main/images/chocolates%20tres%20tipos.png",
        caption="Tipos de chocolate",
        use_container_width=True
    )
    pagina_seleccionada = st.selectbox('🍫 Menú', ['Inicio'])

# ===================== LÓGICA =====================
if "step" not in st.session_state:
    st.session_state.step = "start"
if "current_filtered_frame" not in st.session_state:
    st.session_state.current_filtered_frame = chocoframe.copy()

def reset_chat():
    st.session_state.step = "start"
    st.session_state.current_filtered_frame = chocoframe.copy()

# ===================== INICIO =====================
if st.session_state.step == "start":
    st.markdown("""
    <div class='glass-box'>
        <div class="cookie-monster">
            <img src="https://raw.githubusercontent.com/mmmmeeenna/chocofinal/refs/heads/main/images/mounstrito.png">
        </div>
        <h1>Vamos a comer un chocolate</h1>
        <p class='pregunta'>¿Te provoca algo dulce?</p>
    """, unsafe_allow_html=True)

    # CENTRAMOS BOTONES USANDO COLUMNAS
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        col_si, col_no = st.columns(2)
        with col_si:
            if st.button("Sí"):
                st.session_state.step = "tipo_chocolate"
        with col_no:
            if st.button("No"):
                st.info("¡Está bien! Te esperamos cuando tengas hambre 😋")

    st.markdown("</div>", unsafe_allow_html=True)
# ===================== PASO 2: Tipo de chocolate =====================
elif st.session_state.step == "tipo_chocolate":
    st.markdown("""
    <div class="cookie-monster">
        <img src="https://raw.githubusercontent.com/mmmmeeenna/chocofinal/refs/heads/main/images/mounstro%20cocinando.png" width="140">
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
    st.markdown("<h1>¿Qué tipo de chocolate quieres?</h1>", unsafe_allow_html=True)
    tipo = st.radio("", [
        "Solo chocolate",
        "Hecho en su mayoría de chocolate",
        "Con acentos de chocolate"
    ])
    if st.button("Siguiente ➡️"):
        if tipo == "Solo chocolate":
            st.session_state.step = "mani_almendras"
        elif tipo == "Hecho en su mayoría de chocolate":
            st.session_state.step = "hecho_mayoria"
        else:
            st.session_state.step = "acentos"
    st.markdown("</div>", unsafe_allow_html=True)

# ===================== PASO 3: Maní / Almendras =====================
elif st.session_state.step == "mani_almendras":
    st.session_state.current_filtered_frame = st.session_state.current_filtered_frame.loc[chocoframe['barra de chocolate'] == True]
    st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
    st.markdown("<h1>¿Con maní o almendras?</h1>", unsafe_allow_html=True)
    eleccion = st.radio("", [
        "Con maní", "Sin maní", "Con Almendras", "Sin Almendras"
    ])
    if eleccion == "Con maní":
        st.session_state.current_filtered_frame = st.session_state.current_filtered_frame.loc[chocoframe['mani'] == True]
    elif eleccion == "Sin maní":
        st.session_state.current_filtered_frame = st.session_state.current_filtered_frame.loc[chocoframe['mani'] == False]
    elif eleccion == "Con Almendras":
        st.session_state.current_filtered_frame = st.session_state.current_filtered_frame.loc[chocoframe['almendras'] == True]
    elif eleccion == "Sin Almendras":
        st.session_state.current_filtered_frame = st.session_state.current_filtered_frame.loc[chocoframe['almendras'] == False]
    if st.button("Siguiente ➡️"):
        st.session_state.step = "tipo_final"
    st.markdown("</div>", unsafe_allow_html=True)

# ===================== PASO 4: Tipo final =====================
elif st.session_state.step == "tipo_final":
    st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
    st.markdown("<h1>¿Qué tipo de chocolate prefieres?</h1>", unsafe_allow_html=True)
    tipo_choco = st.radio("", ["Con leche", "Blanco", "Puro"])
    col_map = {
        "Con leche": "chocolate con leche",
        "Blanco": "chocolate blanco",
        "Puro": "chocolate puro"
    }
    col = col_map[tipo_choco]
    st.session_state.current_filtered_frame = st.session_state.current_filtered_frame.loc[chocoframe[col] == True]

    if not st.session_state.current_filtered_frame.empty:
        st.success("✨ ¡Estos chocolates son ideales para ti!")
        st.dataframe(st.session_state.current_filtered_frame)
    else:
        st.warning("No encontramos chocolates con esas preferencias 😢")
    st.button("🔁 Reiniciar", on_click=reset_chat)
    st.markdown("</div>", unsafe_allow_html=True)

    # ========== GALERÍA FINAL ==========
    st.markdown("<div class='gallery'>", unsafe_allow_html=True)

    def galeria(url, caption):
        st.markdown(f"""
        <div>
            <img src="{url}" alt="{caption}">
            <div class="gallery-caption">{caption}</div>
        </div>
        """, unsafe_allow_html=True)

    galeria("https://raw.githubusercontent.com/mmmmeeenna/chocofinal/refs/heads/main/images/chocolatito.png", "Chocolate 🍫")
    galeria("https://raw.githubusercontent.com/mmmmeeenna/chocofinal/refs/heads/main/images/brownie.png", "Brownie 🟤")
    galeria("https://raw.githubusercontent.com/mmmmeeenna/chocofinal/refs/heads/main/images/torta.png", "Quequito 🎂")
    galeria("https://raw.githubusercontent.com/mmmmeeenna/chocofinal/refs/heads/main/images/galletita.png", "Galletita 🍪")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="cookie-monster">
        <img src="https://raw.githubusercontent.com/mmmmeeenna/chocofinal/refs/heads/main/images/mounstro%20comiendo.png">
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<p style='text-align: center;'>¡Gracias por usar nuestro recomendador! 💘</p>", unsafe_allow_html=True)