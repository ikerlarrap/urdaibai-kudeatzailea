import streamlit as st
import streamlit.components.v1 as components
import json
import os
from streamlit_quill import st_quill

# Archivo donde se guardarán los textos reales
ARCHIVO_JSON = 'datos_blog.json'

# --- DISEÑO CORPORATIVO (Se aplica solo en la previsualización) ---
ESTILOS_MENDEXA = """
<style>
    .mendexa-blog-wrapper {
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        color: #333333; line-height: 1.8; max-width: 900px;
        margin: 0px auto; background-color: #ffffff;
        padding: 30px; border-radius: 12px;
    }
    .mendexa-blog-wrapper h1 { color: #3eab36; font-size: 2.2em; text-align: center; margin-bottom: 20px; }
    .mendexa-blog-wrapper h2 { color: #2c5e3b; font-size: 1.6em; border-bottom: 2px solid #e2ece5; padding-bottom: 10px; margin-top: 30px; }
    .mendexa-blog-wrapper p { font-size: 1.1em; margin-bottom: 15px; }
    .mendexa-blog-wrapper ul { margin-bottom: 20px; padding-left: 20px; }
    .mendexa-blog-wrapper li { font-size: 1.1em; margin-bottom: 10px; }
</style>
"""

# Datos iniciales (Solo texto con estructura básica)
datos_iniciales = {
    "Ekaina - 1. Astea": {
        "titulo": "Abentura bikoitza: Mendexa Park + Piraguak Lekeition",
        "estado": "Publicado 🟢",
        "texto": "<h1>Ongi etorri Mendexa Parkera!</h1><p>Idatzi hemen zure testua (Escribe aquí tu texto).</p>"
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
st.markdown("Revisa, edita y previsualiza las publicaciones del verano.")

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
                    "estado": "Borrador 🔴",
                    "texto": ""
                }
                guardar_datos(datos)
                # Al añadir una nueva, le decimos a la memoria que salte a esa nueva semana
                st.session_state.semana_actual = nueva_semana
                st.success("Ondo gehitu da! (Añadido con éxito)")
                st.rerun() 
            else:
                st.warning("Aste hori badago jada! (Esa semana ya existe)")
        else:
            st.error("Bete eremu guztiak, mesedez.")

# --- BARRA LATERAL: SISTEMA DE SEMÁFOROS Y MEMORIA ---
st.sidebar.header("Egutegia (Calendario)")

def formato_opcion(clave):
    estado = datos[clave]["estado"]
    if "Borrador" in estado:
        semaforo = "🔴"
    elif "Revisión" in estado:
        semaforo = "🟡"
    elif "Publicado" in estado:
        semaforo = "🟢"
    else:
        semaforo = "⚪"
    return f"{semaforo} {clave}"

lista_semanas = list(datos.keys())

# MEMORIA: Si es la primera vez que entra, guarda la primera semana en la memoria
if 'semana_actual' not in st.session_state:
    st.session_state.semana_actual = lista_semanas[0]

# MEMORIA: Por si se borra alguna semana, asegurar que no dé error
if st.session_state.semana_actual not in lista_semanas:
    st.session_state.semana_actual = lista_semanas[0]

# Le decimos al selector que empiece en el índice que está guardado en memoria
indice_memoria = lista_semanas.index(st.session_state.semana_actual)

semana_elegida = st.sidebar.selectbox(
    "Aukeratu astea:", 
    lista_semanas,
    index=indice_memoria,
    format_func=formato_opcion
)

# Actualizamos la memoria con lo que elija el usuario manualmente
st.session_state.semana_actual = semana_elegida

post_actual = datos[semana_elegida]

# --- ÁREA DE CABECERA Y ESTADO ---
st.header(post_actual["titulo"])

col1, col2 = st.columns([3, 1])
with col1:
    nuevo_titulo_editado = st.text_input("Izenburua aldatu (Editar título):", post_actual["titulo"])
with col2:
    opciones_estado = ["Borrador 🔴", "Revisión 🟡", "Publicado 🟢"]
    try:
        indice_estado = opciones_estado.index(post_actual["estado"])
    except ValueError:
        indice_estado = 0
    nuevo_estado = st.selectbox("Egoera (Estado):", opciones_estado, index=indice_estado)

st.write("---")

# --- SISTEMA DE PESTAÑAS ---
tab_visual, tab_preview = st.tabs(["📝 Editorea (Testua)", "🚀 Emaitza (Web)"])

with tab_visual:
    st.info("💡 **Nagusiarentzat:** Hemen idatzi eta editatu dezakezu testua Word batean bezala (Mendexako estiloak automatikoki gehituko dira emaitzan).")
    
    # Editor Quill
    texto_editado = st_quill(value=post_actual["texto"], html=True, key=f"quill_editor_{semana_elegida}")
    
    if st.button("💾 Gorde (Guardar)", type="primary"):
        datos[semana_elegida]["titulo"] = nuevo_titulo_editado
        datos[semana_elegida]["estado"] = nuevo_estado
        datos[semana_elegida]["texto"] = texto_editado
        guardar_datos(datos)
        st.success("¡Guardado correctamente!")
        st.rerun()

with tab_preview:
    st.info("💡 Horrela geratuko da azkenean webgunean estiloekin.")
    
    # Inyectamos los estilos
    if post_actual["texto"] and post_actual["texto"].strip():
        html_para_mostrar = f"""
        {ESTILOS_MENDEXA}
        <div class="mendexa-blog-wrapper">
            {post_actual["texto"]}
        </div>
        """
        components.html(html_para_mostrar, height=600, scrolling=True)
    else:
        st.warning("Ez dago ezer ikusteko.")
