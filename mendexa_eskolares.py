import streamlit as st
import urllib.parse

# Configuración de la página
st.set_page_config(page_title="Mendexa Abentura Park Planner", layout="wide")

# --- 1. LOGO ETA ESTILOA ---
try:
    st.image("logo_mendexa.png", width=250)
except:
    st.markdown("🌲 **MENDEXA ABENTURA PARK**")

# --- 2. IZENBURUAK ---
st.title("Mendexa Abentura Park: Eskolentzako Kalkulagailua 🌲")
st.subheader("Kalkulatu zure aurrekontua momentuan / Calcula tu presupuesto al instante")

# --- 3. IKASTETXEAREN DATUAK ---
st.markdown("### 🏫 Ikastetxearen Datuak / Datos de la Escuela")
col_esc1, col_esc2, col_esc3 = st.columns(3)

with col_esc1:
    nombre_escuela = st.text_input("Ikastetxearen izena / Nombre del colegio")
with col_esc2:
    telefono_escuela = st.text_input("Telefonoa / Teléfono")
with col_esc3:
    email_escuela = st.text_input("Posta elektronikoa / Email")

st.divider()

# --- 4. ERRESERBA XEHETASUNAK (MULTI-AUKERA) ---
col_input, col_result = st.columns([1.2, 1])

with col_input:
    st.markdown("### 📝 Ikasleak adinaren arabera / Alumnos por edad")
    st.write("Idatzi ikasle kopurua dagokion programan (0 utzi ez badute egingo):")
    
    # Programen zerrenda
    programak = [
        "🟣 🟠 🟡  1 CIRCUITO: Solo YOKO (4 a 8/9 urte)",
        "🟣 🟠 🟢 🟢  2 CIRCUITOS (9 urte edo gehiago)",
        "🟣 🟠 🟢 🔵  2 CIRCUITOS (12 urte edo gehiago)",
        "🟣 🟠 🟢 🔵 🔵  3 CIRCUITOS (12-14 urte bitartean)",
        "🟣 🟠 🟢 🔵 🔴  3 CIRCUITOS (15 urte edo gehiago)"
    ]

    alumnos_por_programa = {}
    total_alumnos = 0

    # Iteratu programa bakoitzetik zenbaki-kutxa bat sortzeko
    for p in programak:
        c1, c2 = st.columns([4, 1])
        with c1:
            st.write(p)
        with c2:
            num = st.number_input("Ikasleak", min_value=0, value=0, key=p, label_visibility="collapsed")
            alumnos_por_programa[p] = num
            total_alumnos += num

    st.markdown("---")
    num_profesores = st.number_input("Irakasle kopurua guztira / Total profesores:", min_value=1, value=3)

with col_result:
    st.markdown("### 💰 Aurrekontua / Presupuesto")
    
    # Gutxieneko ikasle kopuruaren kontrola
    if total_alumnos < 10 and total_alumnos > 0:
        st.warning("⚠️ Talde batentzako gutxieneko prezio aplikagarria 10 pertsonari dagokiona da.")
    
    if total_alumnos == 0:
        st.info("👈 Mesedez, gehitu ikasleak ezkerreko panelean.")
        st.stop()

    # Deskontu-tartea zehaztu IKASLE TOTALEN arabera
    if total_alumnos > 29: tier = 3
    elif 20 <= total_alumnos <= 29: tier = 2
    else: tier = 1

    presupuesto_total = 0
    desglose_html = ""
    desglose_email = ""

    # Kalkulatu programa bakoitzaren azpitotala
    for p, num in alumnos_por_programa.items():
        if num > 0:
            if "YOKO" in p:
                precio = 13.70 if tier == 3 else 14.70 if tier == 2 else 15.70
            elif "2 CIRCUITOS" in p:
                precio = 19.00 if tier == 3 else 20.00 if tier == 2 else 21.00
            else: # 3 CIRCUITOS
                precio = 21.00 if tier == 3 else 22.00 if tier == 2 else 23.00

            subtotal = num * precio
            presupuesto_total += subtotal
            desglose_html += f"<li style='margin-bottom: 8px;'><strong>{num} ikasle</strong> - {p} <br><small style='color: #2E7D32;'>({precio:.2f} €/ikasle) = <strong>{subtotal:.2f} €</strong></small></li>"
            desglose_email += f"- {num} alumnos: {p} ({precio:.2f} EUR/ud) = {subtotal:.2f} EUR\n"

    # Doakotasuna Mendexan: 1 doan 10 ikasleko
    profes_gratis = total_alumnos // 10
    
    st.metric("Guztira / Total", f"{presupuesto_total:.2f} €")
    st.write(f"👥 **Ikasleak guztira:** {total_alumnos}")
    st.write(f"🎁 **Doako irakasleak:** {profes_gratis} plaza (1 plaza 10 ikasleko)")
    
    if tier == 3:
        st.success("🎉 Zorionak! Eskola honek tarifa merkeena lortu du (>29 ikasle).")

# --- 5. RESGUARDO VISUALA ETA BIDALKETA ---
st.divider()
if st.button("Aurrekontua Sortu / Generar Resguardo", type="primary"):
    if nombre_escuela == "":
        st.error("Mesedez, bete ikastetxearen izena.")
    else:
        st.balloons()
        ticket_html = f"""
        <div style="border: 5px solid #4CAF50; border-radius: 15px; padding: 25px; background-color: #fcfcfc; font-family: sans-serif;">
            <h2 style="color: #4CAF50; margin: 0; text-align: center;">🌲 MENDEXA ABENTURA PARK</h2>
            <hr style="border: 1px solid #4CAF50; margin: 15px 0;">
            <p><strong>Eskola:</strong> {nombre_escuela}</p>
            <p><strong>Parte-hartzaileak:</strong> {total_alumnos} ikasle + {num_profesores} irakasle</p>
            
            <div style="background: #f0f0f0; padding: 15px; border-radius: 8px; margin-top: 15px;">
                <h4 style="margin-top: 0; color: #333; margin-bottom: 10px;">Aukeratutako Programak / Desglose:</h4>
                <ul style="color: #555; list-style-type: none; padding-left: 0; margin-bottom: 0;">
                    {desglose_html}
                </ul>
            </div>
            
            <h3 style="text-align: right; color: #333; font-size: 24px; margin-top: 20px;">GUZTIRA: {presupuesto_total:.2f} €</h3>
        </div>
        """
        st.markdown(ticket_html, unsafe_allow_html=True)

        asunto = f"Reserva Mendexa: {nombre_escuela}"
        cuerpo = f"Colegio: {nombre_escuela}\nTelefono: {telefono_escuela}\nEmail: {email_escuela}\n\n--- DESGLOSE DE ALUMNOS ---\n{desglose_email}\nTotal Profesores: {num_profesores}\n\nTOTAL PRESUPUESTO: {presupuesto_total:.2f} EUR"
        mailto_link = f"mailto:info@mendexapark.com,ikerlarrap@gmail.com?subject={urllib.parse.quote(asunto)}&body={urllib.parse.quote(cuerpo)}"
        st.markdown(f'<br><a href="{mailto_link}" target="_blank"><button style="background-color:#4CAF50; color:white; border:none; padding:10px 20px; border-radius:5px; cursor:pointer;">📩 Bidali eskaera (info@mendexapark.com)</button></a>', unsafe_allow_html=True)

st.divider()
st.caption("Mendexa Abentura Park | info@mendexapark.com | 688 85 62 83")
