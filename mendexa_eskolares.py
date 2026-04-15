import streamlit as st
import urllib.parse
import re

# Configuración de la página
st.set_page_config(page_title="Mendexa Abentura Park Planner", layout="wide")

# --- FUNCIONES DE VALIDACIÓN ---
def es_email_valido(email):
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(patron, email) is not None

def es_telefono_valido(tel):
    return len(tel) >= 9 and tel.isdigit()

# --- 1. LOGO Y ESTILO ---
try:
    st.image("logo_mendexa.png", width=250)
except:
    st.markdown("🌲 **MENDEXA ABENTURA PARK**")

# --- 2. TÍTULOS ---
st.title("Mendexa Abentura Park: Eskolentzako Kalkulagailua 🌲🌲🧗")
st.subheader("Kalkulatu zure aurrekontua momentuan / Calcula tu presupuesto al instante")

# --- 3. DATOS DE LA ESCUELA ---
st.markdown("### 🏫 Ikastetxearen Datuak / Datos de la Escuela")
col_esc1, col_esc2, col_esc3 = st.columns(3)

with col_esc1:
    nombre_escuela = st.text_input("Ikastetxearen izena / Nombre del colegio")
with col_esc2:
    telefono_escuela = st.text_input("Telefonoa / Teléfono")
    if telefono_escuela and not es_telefono_valido(telefono_escuela):
        st.caption("⚠️ Sartu gutxienez 9 zenbaki / Mínimo 9 números")
with col_esc3:
    email_escuela = st.text_input("Posta elektronikoa / Email")
    if email_escuela and not es_email_valido(email_escuela):
        st.caption("⚠️ Email okerra / Email no válido")

st.divider()

# --- 4. SELECCIÓN DE ACTIVIDADES (DISEÑO COMPACTO) ---
col_input, col_result = st.columns([1.4, 1])

with col_input:
    st.markdown("### 📝 Aukeratu zure jarduera-paketea / Elige tu paquete de actividades")
    
    info_programak = {
        "🟣 🟠 🟡 1 ZIRKUITUA: YOKO SOILIK": {
            "desc": "Demo + Laranja + 3 itzuli Yoko zirkuituan. Adina: 4-8 (9) urte.",
            "id": "yoko", "cat": "yoko"
        },
        "🟣 🟠 🟢 🟢 2 ZIRKUITU (9 urte +)": {
            "desc": "Demo + Laranja + 2 Zirkuitu Berde. Adina: >9 urte.",
            "id": "2c_9", "cat": "2c"
        },
        "🟣 🟠 🟢 🔵 2 ZIRKUITU (12 urte +)": {
            "desc": "Demo + Laranja + Zirkuitu Berdea + Urdina. Adina: >12 urte.",
            "id": "2c_12", "cat": "2c"
        },
        "🟣 🟠 🟢 🔵 🔵 3 ZIRKUITU (12-14 urte)": {
            "desc": "Demo + Laranja + Zirkuitu Berdea + 2 Urdin. Adina: 12-14 urte.",
            "id": "3c_12", "cat": "3c"
        },
        "🟣 🟠 🟢 🔵 🔴 3 ZIRKUITU (15 urte +)": {
            "desc": "Demo + Laranja + Berdea + Urdina + Gorria. Adina: >15 urte.",
            "id": "3c_15", "cat": "3c"
        }
    }

    alumnos_por_programa = {}
    total_alumnos = 0

    # Diseño en filas compactas
    for titulo, info in info_programak.items():
        c1, c2, c3 = st.columns([0.1, 4, 1.5])
        with c2:
            st.markdown(f"**{titulo}**", help=info['desc'])
        with c3:
            num = st.number_input("Kopurua", min_value=0, step=1, key=info['id'], label_visibility="collapsed")
            alumnos_por_programa[titulo] = num
            total_alumnos += num

    st.markdown("---")
    num_profesores = st.number_input("Irakasle kopurua guztira:", min_value=0, value=2)

    with st.exp
