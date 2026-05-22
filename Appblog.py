import streamlit as st
import streamlit.components.v1 as components
import json
import os
from streamlit_quill import st_quill

# Archivo donde se guardarán los textos reales
ARCHIVO_JSON = 'datos_blog.json'

# Datos iniciales
datos_iniciales = {
    "Ekaina - 1. Astea": {
        "titulo": "Abentura bikoitza: Mendexa Park + Piraguak Lekeition",
        "estado": "Publicado ✅",
        "texto": "<h1 style='color: #3eab36; font-family: sans-serif;'>Ongi etorri Mendexa Parkera!</h1><p>Hau proba bat da.</p>"
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
                st.success("Ondo gehitu da! (Añadido con éxito)")
                st.rerun() 
            else:
                st.warning("Aste hori badago jada! (Esa semana ya existe)")
        else:
            st.error("Bete eremu guztiak, mesedez.")

# --- BARRA LATERAL: SISTEMA DE SEMÁFOROS ---
st.sidebar.header("Egutegia (Calendario)")

def formato_opcion(clave):
    estado = datos[clave]["estado"]
    # Semáforo visual
    if "Borrador" in estado:
        semaforo = "🔴"
    elif "Revisión" in estado:
        semaforo = "🟡"
    elif "Publicado" in estado:
        semaforo = "🟢"
    else:
        semaforo = "⚪"
    return f"{semaforo} {clave}"

semana_elegida = st.sidebar.selectbox(
    "Aukeratu astea:", 
    list(datos.keys()),
    format_func=formato_opcion
)

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

# --- SISTEMA DE PESTAÑAS (JEFE VS DESARROLLADOR) ---
# La primera pestaña es la que se abre por defecto al entrar
tab_jefe, tab_iker, tab_preview = st.tabs(["👁️ Editorea (Nagusia)", "💻 HTML (Zu)", "🚀 Emaitza (Web)"])

with tab_jefe:
    st.info("💡 **Nagusiarentzat:** Hemen idatzi dezakezu Word batean bezala. (Escribe aquí directamente, pon negritas, listas...)")
    # Editor visual (WYSIWYG). Retorna HTML generado automáticamente.
    texto_visual = st_quill(value=post_actual["texto"], html=True, key=f"quill_{semana_elegida}")

with tab_iker:
    st.info("💡 **Zuretzat:** Hemen HTML kodea ikusi eta estilo pertsonalizatuak sar ditzakezu (Botoiak, CSS, etab).")
    # Si el jefe edita, esto se actualiza. Aquí tú puedes meter mano al código.
    texto_html_final = st.text_area("HTML Kodea", value=texto_visual if texto_visual else post_actual["texto"], height=450, label_visibility="collapsed")

with tab_preview:
    st.info("💡 **Ikuspegia:** Horrela geratuko da azkenean webgunean estiloekin.")
    if texto_html_final and texto_html_final.strip():
        components.html(texto_html_final, height=500, scrolling=True)
    else:
        st.warning("Ez dago ezer ikusteko.")

# --- BOTÓN DE GUARDAR ---
if st.button("💾 Gorde (Guardar cambios)", type="primary"):
    datos[semana_elegida]["titulo"] = nuevo_titulo_editado
    datos[semana_elegida]["estado"] = nuevo_estado
    # Guardamos lo que haya en la pestaña HTML, que es la versión final con tus mejoras
    datos[semana_elegida]["texto"] = texto_html_final 
    guardar_datos(datos)
    st.success("¡Texto guardado correctamente!")
    st.rerun()
