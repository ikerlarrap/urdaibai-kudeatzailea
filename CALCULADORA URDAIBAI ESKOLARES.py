import streamlit as st
import urllib.parse

# Configuración de la página
st.set_page_config(page_title="UR Urdaibai Planner", layout="wide")

try:
    st.image("logo.png", width=250)
except:
    pass

# Título principal en Euskera
st.title("UR Urdaibai: Eskola-Egitarauen Kudeatzailea 🌊")
st.subheader("Konbinazioa: Kanoa Zeharkaldia + Big SUP")

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
    edad_participantes = st.number_input("Parte-hartzaileen adina / Edad:", min_value=1, value=12)
    
    actividad = st.selectbox("Aukeratu ekintza / Actividad:", [
        "Kanoa Zeharkaldia (1,5 ordu)",
        "BigSUP (1,5 ordu)",
        "Konbinazioa: Kanoa Zeharkaldia + Big SUP (1,5 ordu)",
        "Konbinazioa: Kanoa Zeharkaldia + Big SUP (2 ordu)"
    ])

    # Lógica de precios
    precio_unidad = 0
    edad_minima = 12
    
    if actividad == "Kanoa Zeharkaldia (1,5 ordu)":
        if num_alumnos > 29: precio_unidad = 22.30
        elif 20 <= num_alumnos <= 29: precio_unidad = 24.30
        else: precio_unidad = 26.30
        edad_minima = 12
    elif actividad == "BigSUP (1,5 ordu)":
        if num_alumnos > 29: precio_unidad = 24.50
        elif 20 <= num_alumnos <= 29: precio_unidad = 26.50
        else: precio_unidad = 28.50
        edad_minima = 10
    elif "Konbinazioa" in actividad and "1,5 ordu" in actividad:
        if num_alumnos > 29: precio_unidad = 27.00
        elif 20 <= num_alumnos <= 29: precio_unidad = 29.00
        else: precio_unidad = 31.00
        edad_minima = 12
    elif "Konbinazioa" in actividad and "2 ordu" in actividad:
        if num_alumnos > 29: precio_unidad = 35.00
        elif 20 <= num_alumnos <= 29: precio_unidad = 37.00
        else: precio_unidad = 39.00
        edad_minima = 12

with col_result:
    st.markdown("### 💰 Aurrekontua / Presupuesto")
    
    if edad_participantes < edad_minima:
        st.error(f"⚠️ Kontuz: Gutxieneko adina {edad_minima} urtekoa da.")
    
    profes_gratis = num_alumnos // 20
    total_euros = num_alumnos * precio_unidad
    
    c1, c2 = st.columns(2)
    c1.metric("Guztira / Total", f"{total_euros:.2f} €")
    c2.metric("Ikasleko / Por alumno", f"{precio_unidad:.2f} €")
    
    st.write(f"✅ **Doako irakasleak:** {profes_gratis} plaza")
    st.warning("⚠️ Gogoratu: Ezinbestekoa da igeri egiten jakitea.")

# --- SECCIÓN 3: RESGUARDO VISUAL Y ENVÍO EN 2 PASOS ---
st.divider()
st.markdown("### 📥 Eskaera Berretsi / Confirmar Solicitud")

if st.button("Aurrekontua Sortu / Generar Resguardo", type="primary"):
    if nombre_escuela == "" or email_escuela == "":
        st.error("⚠️ Mesedez, bete ikastetxearen datuak. / Rellena los datos del colegio arriba.")
    else:
        st.balloons()
        
        # 1. El Ticket Visual
        ticket_html = f"""
        <div style="border: 3px solid #1E88E5; border-radius: 15px; padding: 25px; background-color: #F3E5F5; font-family: Arial, sans-serif; box-shadow: 5px 5px 15px rgba(0,0,0,0.1);">
            <h2 style="color: #1E88E5; text-align: center; margin-top: 0;">🎟️ UR URDAIBAI</h2>
            <h4 style="color: #555; text-align: center; margin-bottom: 20px;">Erreserba Froga / Resguardo de Solicitud</h4>
            <hr style="border: 1px solid #1E88E5;">
            <table style="width: 100%; margin-top: 15px; font-size: 16px;">
                <tr><td style="padding: 8px 0;"><strong>🏫 Ikastetxea:</strong></td><td>{nombre_escuela}</td></tr>
                <tr><td style="padding: 8px 0;"><strong>📧 Emaila:</strong></td><td>{email_escuela}</td></tr>
                <tr><td style="padding: 8px 0;"><strong>🏄 Ekintza:</strong></td><td>{actividad}</td></tr>
                <tr><td style="padding: 8px 0;"><strong>👥 Ikasleak:</strong></td><td>{num_alumnos} (Adina: {edad_participantes} urte)</td></tr>
                <tr><td style="padding: 8px 0;"><strong>🧑‍🏫 Irakasleak:</strong></td><td>{num_profesores} (Doan: {profes_gratis})</td></tr>
            </table>
            <hr style="border: 1px dashed #1E88E5; margin: 20px 0;">
            <h3 style="text-align: right; color: #D81B60; margin: 0;">Guztira: {total_euros:.2f} €</h3>
        </div>
        """
        st.markdown(ticket_html, unsafe_allow_html=True)
        st.info("💡 Aholkua: Egin pantaila-argazkia edo gorde PDF gisa. / Guarda este ticket.")

        # 2. El Botón de abrir el correo (Mailto - Método de 2 pasos)
        asunto = f"Reserva Escolar: {nombre_escuela} - {actividad}"
        cuerpo = f"Colegio: {nombre_escuela}\nTeléfono: {telefono_escuela}\nEmail: {email_escuela}\nActividad: {actividad}\nAlumnos: {num_alumnos}\nEdad: {edad_participantes}\nTotal Presupuesto: {total_euros:.2f} EUR"
        
        mailto_link = f"mailto:ikerlarrap@gmail.com?subject={urllib.parse.quote(asunto)}&body={urllib.parse.quote(cuerpo)}"
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f'<a href="{mailto_link}" target="_blank" style="text-decoration:none;"><button style="background-color:#4CAF50; color:white; border:none; padding:10px 20px; border-radius:5px; cursor:pointer; font-size:16px;">📩 Ireki nire posta mezua bidaltzeko / Abrir mi correo para enviar</button></a>', unsafe_allow_html=True)

st.divider()
st.caption("UR Urdaibai - Natur Jarduerak eta Abentura | info@urdaibai.com | 94 627 66 61")
