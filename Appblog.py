import streamlit as st
import streamlit.components.v1 as components
import json
import os
from streamlit_quill import st_quill

# Archivo donde se guardarán los textos reales
ARCHIVO_JSON = 'datos_blog.json'

# --- AQUÍ GUARDAMOS TU DISEÑO CORPORATIVO (No molesta al jefe) ---
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

# Datos iniciales (Ahora el texto está limpio, sin CSS, para que Quill no falle)
datos_iniciales = {
    "Ekaina - 1. Astea": {
        "titulo": "Abentura bikoitza: Mendexa Park + Piraguak Lekeition",
        "estado": "Publicado 🟢",
        "texto": "<h1>Ongi etorri Mendexa Parkera!</h1><p>Hau proba bat da. Orain zure nagusiak ondo ikusiko du testua hemen.</p>"
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

# --- SISTEMA DE PESTAÑAS ---
tab_visual, tab_html, tab_preview = st.tabs(["👁️ Editor texto", "💻 Editor html", "🚀 Visual web"])

with tab_visual:
    st.info("💡 **Nagusiarentzat:** Hemen idatzi dezakezu Word batean bezala.")
    
    # Ahora Quill lee texto HTML limpio y no colapsa
    texto_visual = st_quill(value=post_actual["texto"], html=True, key=f"quill_{semana_elegida}")
    
    if st.button("💾 Gorde (Guardar texto)", type="primary", key="btn_visual"):
        datos[semana_elegida]["titulo"] = nuevo_titulo_editado
        datos[semana_elegida]["estado"] = nuevo_estado
        datos[semana_elegida]["texto"] = texto_visual 
        guardar_datos(datos)
        st.success("¡Texto guardado correctamente!")
        st.rerun()

with tab_html:
    st.info("💡 **Zuretzat:** Hemen HTML kode garbia ikusi dezakezu WordPressera eramateko.")
    texto_html_final = st.text_area("HTML Kodea", value=post_actual["texto"], height=450, label_visibility="collapsed")
    
    if st.button("💾 Gorde (Guardar código HTML)", type="primary", key="btn_html"):
        datos[semana_elegida]["titulo"] = nuevo_titulo_editado
        datos[semana_elegida]["estado"] = nuevo_estado
        datos[semana_elegida]["texto"] = texto_html_final 
        guardar_datos(datos)
        st.success("¡Código HTML guardado correctamente!")
        st.rerun()

with tab_preview:
    st.info("💡 Horrela geratuko da azkenean webgunean estiloekin.")
    
    # Magia pura: Inyectamos los estilos y envolvemos el texto limpio justo antes de mostrarlo
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
