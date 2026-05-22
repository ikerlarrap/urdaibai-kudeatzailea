import streamlit as st
import streamlit.components.v1 as components
import json
import os

# Archivo donde se guardarán los textos reales
ARCHIVO_JSON = 'datos_blog.json'

# Datos iniciales que se cargarán la primera vez
datos_iniciales = {
    "Ekaina - 1. Astea": {
        "titulo": "Abentura bikoitza: Mendexa Park + Piraguak Lekeition",
        "estado": "Publicado ✅",
        "texto": "\n<h1 style='color: #3eab36; font-family: sans-serif;'>Ongi etorri Mendexa Parkera!</h1>\n<p style='font-family: sans-serif;'>Hau proba bat da. (Esto es una prueba para ver el visualizador).</p>"
    },
    "Ekaina - 2. Astea": {
        "titulo": "Lehenengo aldia tirolinetan? 5 aholku ezinbesteko",
        "estado": "Revisión 📝",
        "texto": "Zure lehenengo aldia da abentura parke batean? Ez kezkatu!..."
    },
    "Ekaina - 3. Astea": {
        "titulo": "Familientzako plan ezin hobea: Nola prestatu zure bisita",
        "estado": "Borrador ✏️",
        "texto": "Idazteke... (Sartu hemen testua)"
    }
}

# Funciones para leer y guardar los datos
def cargar_datos():
    if not os.path.exists(ARCHIVO_JSON):
        with open(ARCHIVO_JSON, 'w', encoding='utf-8') as f:
            json.dump(datos_iniciales, f, ensure_ascii=False, indent=4)
    with open(ARCHIVO_JSON, 'r', encoding='utf-8') as f:
        return json.load(f)

def guardar_datos(datos):
    with open(ARCHIVO_JSON, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

# --- CONFIGURACIÓN VISUAL DE LA APP ---
st.set_page_config(page_title="Mendexa Blog Gestorea", page_icon="🌲", layout="wide")

st.title("📅 Mendexa Blog Gestorea")
st.markdown("Revisa, edita y previsualiza las publicaciones del verano como en WordPress.")

datos = cargar_datos()

# --- BARRA LATERAL: AÑADIR NUEVAS SEMANAS ---
with st.sidebar.expander("➕ Gehitu aste berria (Añadir semana)"):
    nueva_semana = st.text_input("Astea (adibidez: Uztaila - 1. Astea)")
    nuevo_titulo = st.text_input("Izenburua (Título del post)")
    
    if st.button("Gehitu (Añadir)"):
        if nueva_semana and nuevo_titulo:
            if nueva_semana not in datos:
                datos[nueva_semana] = {
                    "titulo": nuevo_titulo,
                    "estado": "Borrador ✏️",
                    "texto": ""
                }
                guardar_datos(datos)
                st.success("Ondo gehitu da! (Añadido con éxito)")
                st.rerun() 
            else:
                st.warning("Aste hori badago jada! (Esa semana ya existe)")
        else:
            st.error("Bete eremu guztiak, mesedez. (Rellena todos los campos)")

# --- BARRA LATERAL: SELECCIÓN CON INDICADOR VISUAL ---
st.sidebar.header("Egutegia (Calendario)")

def formato_opcion(clave):
    estado = datos[clave]["estado"]
    icono = estado.split(" ")[-1] if " " in estado else "📌"
    return f"{icono} {clave}"

semana_elegida = st.sidebar.selectbox(
    "Aukeratu astea (Elegir semana):", 
    list(datos.keys()),
    format_func=formato_opcion
)

post_actual = datos[semana_elegida]

# --- ÁREA DE EDICIÓN ---
st.header(post_actual["titulo"])

# Fila con el título y el estado para ahorrar espacio
col1, col2 = st.columns([3, 1])
with col1:
    nuevo_titulo_editado = st.text_input("Izenburua aldatu (Editar título):", post_actual["titulo"])
with col2:
    opciones_estado = ["Borrador ✏️", "Revisión 📝", "Publicado ✅"]
    try:
        indice_estado = opciones_estado.index(post_actual["estado"])
    except ValueError:
        indice_estado = 0
    nuevo_estado = st.selectbox("Egoera (Estado):", opciones_estado, index=indice_estado)

st.write("---")

# --- PESTAÑAS TIPO WORDPRESS (CÓDIGO VS VISUAL) ---
tab1, tab2 = st.tabs(["💻 HTML Kodea (Editor)", "👁️ Ikuspegia (Previsualización Visual)"])

with tab1:
    st.info("Pegatu hemen WordPress-erako edo Mailchimp-erako HTML kodea.")
    # Caja de texto grande
    nuevo_texto = st.text_area("Testua (Cuerpo del artículo):", post_actual["texto"], height=500, label_visibility="collapsed")

with tab2:
    st.info("Horrela ikusiko da webgunean (Así se verá en la web):")
    # Renderizador de HTML interactivo
    if nuevo_texto.strip():
        components.html(nuevo_texto, height=600, scrolling=True)
    else:
        st.warning("Ez dago ezer ikusteko. (No hay código para mostrar todavía).")

st.write("---")

# Botón para guardar cambios
if st.button("Gorde (Guardar cambios)", type="primary"):
    datos[semana_elegida]["titulo"] = nuevo_titulo_editado
    datos[semana_elegida]["estado"] = nuevo_estado
    datos[semana_elegida]["texto"] = nuevo_texto
    guardar_datos(datos)
    st.success("¡Texto guardado correctamente! El archivo se ha actualizado.")
    st.rerun()
