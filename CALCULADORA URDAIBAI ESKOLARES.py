import streamlit as st
import urllib.parse

# Configuración de la página
st.set_page_config(page_title="UR Urdaibai Planner", layout="wide")

# Título principal en Euskera
st.title("UR Urdaibai: Eskola-Egitarauen Kudeatzailea 🌊")
st.subheader("Ikastetxeentzako aurrekontu eta kudeaketa tresna")

# --- SECCIÓN 1: DATOS DE LA ESCUELA ---
st.markdown("### 🏫 Ikastetxearen Datuak / Datos de la Escuela")
col_esc1, col_esc2, col_esc3 = st.columns(3)

with col_esc1:
    nombre_escuela = st.text_input("Ikastetxearen izena / Nombre del colegio")
with col_esc2:
    telefono_escuela = st.text_input("Telefonoa / Teléfono")
with col_esc3:
    email_escuela = st.text_input("Posta elektronikoa / Email")

st.divider()

# --- SECCIÓN 2: CÁLCULOS DE ACTIVIDAD ---
col_input, col_result = st.columns([1, 1.5])

with col_input:
    st.markdown("### 📝 Erreserba Xehetasunak")
    
    num_alumnos = st.number_input("Ikasle kopurua (min. 10):", min_value=10, value=25)
    num_profesores = st.number_input("Irakasle kopurua:", min_value=1, value=2)
    edad_participantes = st.number_input("Parte-hartzaileen adina / Edad participantes:", min_value=1, value=12)
    
    actividad = st.selectbox("Aukeratu ekintza / Actividad:", [
        "Kanoa Zeharkaldia (1,5 ordu)",
        "BigSUP (1,5 ordu)",
        "Konbinazioa: Kanoa Zeharkaldia + Big SUP (1,5 ordu)",
        "Konbinazioa: Kanoa Zeharkaldia + Big SUP (2 ordu)"
    ])

    precio_unidad = 0
    edad_minima = 12
    
    if actividad == "Kanoa Zeharkaldia (1,5 ordu)":
        if num_alumnos > 29:
            precio_unidad = 22.30
        elif 20 <= num_alumnos <= 29:
            precio_unidad = 24.30
        else:
            precio_unidad = 26.30
        edad_minima = 12
        
    elif actividad == "BigSUP (1,5 ordu)":
        if num_alumnos > 29:
            precio_unidad = 24.50
        elif 20 <= num_alumnos <= 29:
            precio_unidad = 26.50
        else:
            precio_unidad = 28.50
        edad_minima = 10
        
    elif actividad == "Konbinazioa: Kanoa Zeharkaldia + Big SUP (1,5 ordu)":
        if num_alumnos > 29:
            precio_unidad = 27.00
        elif 20 <= num_alumnos <= 29:
            precio_unidad = 29.00
        else:
            precio_unidad = 31.00
        edad_minima = 12

    elif actividad == "Konbinazioa: Kanoa Zeharkaldia + Big SUP (2 ordu)":
        if num_alumnos > 29:
            precio_unidad = 35.00
        elif 20 <= num_alumnos <= 29:
            precio_unidad = 37.00
        else:
            precio_unidad = 39.00
        edad_minima = 12

with col_result:
    st.markdown("### 💰 Aurrekontua / Presupuesto")
    
    if edad_participantes < edad_minima:
        st.error(f"⚠️ Kontuz: Ekintza honetarako gutxieneko adina {edad_minima} urtekoa da. / Edad mínima: {edad_minima} años.")
    
    profes_gratis = num_alumnos // 20
    total_euros = num_alumnos * precio_unidad
    
    m_col1, m_col2 = st.columns(2)
    m_col1.metric("Guztira / Total", f"{total_euros:.2f} €")
    m_col2.metric("Ikasleko / Por alumno", f"{precio_unidad:.2f} €")
    
    st.write(f"✅ **Doako irakasleak:** {profes_gratis} plaza (1 plaza 20 ikasleko)")
    st.info("📅 **Denboraldia:** Martxoak 1 - Ekainak 20 / Irailak 1 - Azaroak 14")

# --- SECCIÓN 3: ENVÍO DE EMAIL ---
st.divider()
st.markdown("### 📤 Eskaera Bidali / Enviar Solicitud")

asunto = f"Reserva Escolar: {nombre_escuela} - {actividad}"
cuerpo = f"""Detalles de la reserva:
- Colegio: {nombre_escuela}
- Telefono: {telefono_escuela}
- Email: {email_escuela}
- Actividad: {actividad}
- Alumnos: {num_alumnos}
- Edad: {edad_participantes} anos
- Profesores: {num_profesores} (Gratis: {profes_gratis})
- Presupuesto estimado: {total_euros:.2f} EUROS
"""

mailto_link = f"mailto:ikerlarrap@gmail.com?subject={urllib.parse.quote(asunto)}&body={urllib.parse.quote(cuerpo)}"

if st.button("Emaila Bidali / Enviar Email ahora", type="primary"):
    if nombre_escuela == "" or email_escuela == "":
        st.error("⚠️ Mesedez, bete ikastetxearen datuak. / Rellena los datos del colegio.")
    else:
        st.success("✅ Emaila prest dago bidaltzeko!")
        st.markdown(f'<a href="{mailto_link}" target="_blank" style="text-decoration:none;"><button style="background-color:#ff4b4b; color:white; border:none; padding:10px 20px; border-radius:5px; cursor:pointer;">Confirmar Envío en mi Correo</button></a>', unsafe_allow_html=True)
        st.balloons()

# --- PIE DE PÁGINA ---
st.divider()
st.caption("UR Urdaibai - Natur Jarduerak eta Abentura | info@urdaibai.com | 94 627 66 61")