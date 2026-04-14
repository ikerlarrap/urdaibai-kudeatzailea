import streamlit as st
import urllib.parse

# Configuración de la página
st.set_page_config(page_title="Mendexa Abentura Park Planner", layout="wide")

# --- 1. LOGO Y ESTILO ---
try:
    st.image("logo_mendexa.png", width=250)
except:
    st.markdown("🌲 **MENDEXA ABENTURA PARK**")

# --- 2. TÍTULOS ---
st.title("Mendexa Abentura Park: Eskolentzako Kalkulagailua 🌲")
st.subheader("Kalkulatu zure aurrekontua momentuan / Calcula tu presupuesto al instante")

# --- 3. DATOS DE LA ESCUELA ---
st.markdown("### 🏫 Ikastetxearen Datuak / Datos de la Escuela")
col_esc1, col_esc2, col_esc3 = st.columns(3)

with col_esc1:
    nombre_escuela = st.text_input("Ikastetxearen izena / Nombre del colegio")
with col_esc2:
    telefono_escuela = st.text_input("Telefonoa / Teléfono")
with col_esc3:
    email_escuela = st.text_input("Posta elektronikoa / Email")

st.divider()

# --- 4. DETALLES DE LA RESERVA ---
col_input, col_result = st.columns([1, 1.5])

with col_input:
    st.markdown("### 📝 Erreserba Xehetasunak")
    
    num_alumnos = st.number_input("Ikasle kopurua (min. 10):", min_value=10, value=25)
    num_profesores = st.number_input("Irakasle kopurua:", min_value=1, value=3)
    
    # Selector de programa con el orden corregido: Naranja tras Demo, y Amarillo al final en Yoko
    paquete = st.selectbox("Aukeratu programa zehatza / Selecciona el programa:", [
        "🟣 🟠 🟡  1 CIRCUITO: Solo YOKO (4 a 8/9 urte)",
        "🟣 🟠 🟢 🟢  2 CIRCUITOS (9 urte edo gehiago)",
        "🟣 🟠 🟢 🔵  2 CIRCUITOS (12 urte edo gehiago)",
        "🟣 🟠 🟢 🔵 🔵  3 CIRCUITOS (12-14 urte bitartean)",
        "🟣 🟠 🟢 🔵 🔴  3 CIRCUITOS (15 urte edo gehiago)"
    ])

    # Lógica de precios y descripción del flujo de circuitos
    if "YOKO" in paquete:
        color_tema = "#FFC107" # Amarillo
        zirkuituak_info = "Demo + Laranja + 3 itzuli Yoko zirkuituan"
        requisitos = "Adina: 4-8 (9) urte | Iraupena: 1,5 - 2 ordu"
        if num_alumnos > 29: precio = 13.70
        elif 20 <= num_alumnos <= 29: precio = 14.70
        else: precio = 15.70
            
    elif "2 CIRCUITOS" in paquete:
        iraupena = "2 - 2,5 ordu"
        if "9 urte" in paquete:
            color_tema = "#4CAF50" # Verde
            zirkuituak_info = "Demo + Laranja + 2 Zirkuitu Berde"
            requisitos = f"Adina: >9 urte | Iraupena: {iraupena}"
        else:
            color_tema = "#2196F3" # Azul
            zirkuituak_info = "Demo + Laranja + Zirkuitu Berdea + Zirkuitu Urdina"
            requisitos = f"Adina: >12 urte | Iraupena: {iraupena}"
        
        if num_alumnos > 29: precio = 19.00
        elif 20 <= num_alumnos <= 29: precio = 20.00
        else: precio = 21.00
            
    else: # 3 CIRCUITOS
        iraupena = "2,5 - 3 ordu"
        if "12-14" in paquete:
            color_tema = "#2196F3" # Azul
            zirkuituak_info = "Demo + Laranja + Zirkuitu Berdea + 2 Zirkuitu Urdin"
            requisitos = f"Adina: 12-14 urte | Iraupena: {iraupena}"
        else:
            color_tema = "#F44336" # Rojo
            zirkuituak_info = "Demo + Laranja + Zirkuitu Berdea + Urdina + Gorria"
            requisitos = f"Adina: >15 urte | Iraupena: {iraupena}"

        if num_alumnos > 29: precio = 21.00
        elif 20 <= num_alumnos <= 29: precio = 22.00
        else: precio = 23.00

    st.info(f"🧗 **Ekintza:** {zirkuituak_info}\n\nℹ️ **Baldintzak:**\n{requisitos}")

with col_result:
    st.markdown("### 💰 Aurrekontua / Presupuesto")
    
    # Gratuidades: Profesores gratis (1 cada 10 alumnos)
    profes_gratis = num_alumnos // 10
    total_euros = num_alumnos * precio
    
    c1, c2 = st.columns(2)
    c1.metric("Guztira / Total", f"{total_euros:.2f} €")
    c2.metric("Ikasleko / Por alumno", f"{precio:.2f} €")
    
    st.write(f"🎁 **Doako irakasleak:** {profes_gratis} plaza (1 plaza 10 ikasleko)")
    st.warning("📅 **Baldintzak:** Aste barruan aplikatzeko tarifak. Gutxienez 10 ikasle. BEZ %10 barne.")

# --- 5. RESGUARDO VISUAL Y ENVÍO ---
st.divider()
if st.button("Aurrekontua Sortu / Generar Resguardo", type="primary"):
    if nombre_escuela == "":
        st.error("Mesedez, bete ikastetxearen izena.")
    else:
        st.balloons()
        ticket_html = f"""
        <div style="border: 5px solid {color_tema}; border-radius: 15px; padding: 25px; background-color: #fcfcfc; font-family: sans-serif;">
            <h2 style="color: {color_tema}; margin: 0; text-align: center;">🌲 MENDEXA ABENTURA PARK</h2>
            <hr style="border: 1px solid {color_tema}; margin: 15px 0;">
            <h4 style="margin-top: 0; color: #444;">Programa: {paquete}</h4>
            <p><strong>Eskola:</strong> {nombre_escuela}</p>
            <p><strong>Parte-hartzaileak:</strong> {num_alumnos} ikasle + {num_profesores} irakasle</p>
            <p style="font-size: 0.9em; color: #666; background: #f0f0f0; padding: 10px; border-radius: 8px;">
                <em>Zirkuituak: {zirkuituak_info}<br>Eskakizunak: {requisitos}</em>
            </p>
            <h3 style="text-align: right; color: #333; font-size: 24px;">GUZTIRA: {total_euros:.2f} €</h3>
        </div>
        """
        st.markdown(ticket_html, unsafe_allow_html=True)

        asunto = f"Reserva Mendexa: {nombre_escuela}"
        cuerpo = f"Colegio: {nombre_escuela}\nTelefono: {telefono_escuela}\nEmail: {email_escuela}\nPrograma: {paquete}\nAlumnos: {num_alumnos}\nTotal: {total_euros:.2f} EUR"
        mailto_link = f"mailto:info@mendexapark.com,ikerlarrap@gmail.com?subject={urllib.parse.quote(asunto)}&body={urllib.parse.quote(cuerpo)}"
        st.markdown(f'<br><a href="{mailto_link}" target="_blank"><button style="background-color:#4CAF50; color:white; border:none; padding:10px 20px; border-radius:5px; cursor:pointer;">📩 Bidali eskaera (info@mendexapark.com)</button></a>', unsafe_allow_html=True)

st.divider()
st.caption("Mendexa Abentura Park | info@mendexapark.com | 688 85 62 83")