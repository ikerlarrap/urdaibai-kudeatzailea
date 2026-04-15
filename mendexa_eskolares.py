import streamlit as st
import urllib.parse

# Orrialdearen konfigurazioa
st.set_page_config(page_title="Mendexa Abentura Park Planner", layout="wide")

# --- 1. LOGOA ETA ESTILOA ---
try:
    st.image("logo_mendexa.png", width=250)
except:
    st.markdown("🌲 **MENDEXA ABENTURA PARK**")

# --- 2. IZENBURUAK (EUSKERAZ) ---
st.title("Mendexa Abentura Park: Eskolentzako Kalkulagailua 🌊")
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
col_input, col_result = st.columns([1.3, 1])

with col_input:
    st.markdown("### 📝 Ikasleak adinaren arabera / Alumnos por edad")
    st.write("Idatzi ikasle kopurua dagokion programan (0 utzi ez badute egingo):")
    
    # Programen definizio zehatza
    info_programak = {
        "🟣 🟠 🟡  1 ZIRKUITUA: YOKO SOILIK": {
            "desc": "Demo + Laranja + 3 itzuli Yoko zirkuituan",
            "req": "Adina: 4-8 (9) urte | Altuera: 1'10m - 1'40m",
            "base_price": 13.70
        },
        "🟣 🟠 🟢 🟢  2 ZIRKUITU (9 urte +)": {
            "desc": "Demo + Laranja + 2 Zirkuitu Berde",
            "req": "Adina: >9 urte | Altuera: >1'40m",
            "base_price": 19.00
        },
        "🟣 🟠 🟢 🔵  2 ZIRKUITU (12 urte +)": {
            "desc": "Demo + Laranja + Zirkuitu Berdea + Urdina",
            "req": "Adina: >12 urte | Altuera: >1'50m",
            "base_price": 19.00
        },
        "🟣 🟠 🟢 🔵 🔵  3 ZIRKUITU (12-14 urte)": {
            "desc": "Demo + Laranja + Zirkuitu Berdea + 2 Urdin",
            "req": "Adina: 12-14 urte | Altuera: >1'50m",
            "base_price": 21.00
        },
        "🟣 🟠 🟢 🔵 🔴  3 ZIRKUITU (15 urte +)": {
            "desc": "Demo + Laranja + Berdea + Urdina + Gorria",
            "req": "Adina: >15 urte | Altuera: >1'50m",
            "base_price": 21.00
        }
    }

    alumnos_por_programa = {}
    total_alumnos = 0

    # Taula moduko bat sortu programak aukeratzeko
    for titulo, info in info_programak.items():
        expander = st.expander(f"{titulo}", expanded=True)
        with expander:
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"**Ekintza:** {info['desc']}")
                st.caption(f"Baldintzak: {info['req']}")
            with c2:
                num = st.number_input("Ikasleak", min_value=0, value=0, key=titulo)
                alumnos_por_programa[titulo] = num
                total_alumnos += num

    st.markdown("---")
    num_profesores = st.number_input("Irakasle kopurua guztira / Total profesores:", min_value=1, value=2)

with col_result:
    st.markdown("### 💰 Aurrekontua / Presupuesto")
    
    if total_alumnos == 0:
        st.info("👈 Gehitu ikasleak ezkerreko panelean aurrekontua ikusteko.")
        st.stop()

    # Prezio tartea (tier) talde osoaren arabera kalkulatu
    if total_alumnos > 29: tier = 3 # Más de 29
    elif 20 <= total_alumnos <= 29: tier = 2 # 20 a 29
    else: tier = 1 # 10 a 19

    presupuesto_total = 0
    desglose_html = ""
    desglose_email = ""

    for titulo, num in alumnos_por_programa.items():
        if num > 0:
            # Prezioen doikuntza tartearen arabera
            if "YOKO" in titulo:
                precio = 13.70 if tier == 3 else 14.70 if tier == 2 else 15.70
            elif "2 ZIRKUITU" in titulo:
                precio = 19.00 if tier == 3 else 20.00 if tier == 2 else 21.00
            else: # 3 ZIRKUITU
                precio = 21.00 if tier == 3 else 22.00 if tier == 2 else 23.00

            subtotal = num * precio
            presupuesto_total += subtotal
            desglose_html += f"""
                <li style='margin-bottom: 10px;'>
                    <strong>{num} ikasle:</strong> {titulo}<br>
                    <small style='color: #666;'>{info_programak[titulo]['desc']}</small><br>
                    <span style='color: #2E7D32;'>{precio:.2f}€ x {num} = {subtotal:.2f}€</span>
                </li>
            """
            desglose_email += f"- {num} ikasle: {titulo} ({precio:.2f}€/u) = {subtotal:.2f}€\n"

    # Doakotasunak: 1 irakasle 10 ikasleko
    profes_gratis = total_alumnos // 10
    
    st.metric("Guztira / Total", f"{presupuesto_total:.2f} €")
    st.write(f"👥 **Ikasleak guztira:** {total_alumnos}")
    st.write(f"🎁 **Doako irakasleak:** {profes_gratis} plaza")
    
    if tier == 3:
        st.success("✅ Talde handia (>29): Tarifa merkeena aplikatu da.")

# --- 5. TICKET ETA BIDALKETA ---
st.divider()
if st.button("Aurrekontua Sortu / Generar Resguardo", type="primary"):
    if nombre_escuela == "":
        st.error("Mesedez, bete ikastetxearen izena.")
    else:
        st.balloons()
        ticket_html = f"""
        <div style="border: 5px solid #2E7D32; border-radius: 15px; padding: 25px; background-color: #fcfcfc; font-family: sans-serif;">
            <h2 style="color: #2E7D32; text-align: center; margin: 0;">🌲 MENDEXA ABENTURA PARK</h2>
            <hr style="border: 1px solid #2E7D32; margin: 15px 0;">
            <p><strong>Eskola:</strong> {nombre_escuela}</p>
            <p><strong>Taldea:</strong> {total_alumnos} ikasle + {num_profesores} irakasle</p>
            
            <div style="background: #f0f0f0; padding: 15px; border-radius: 8px; margin-top: 15px;">
                <h4 style="margin-top: 0; color: #333;">Aukeratutako Programak:</h4>
                <ul style="padding-left: 20px;">
                    {desglose_html}
                </ul>
            </div>
            
            <h3 style="text-align: right; color: #333; font-size: 24px;">GUZTIRA: {presupuesto_total:.2f} €</h3>
        </div>
        """
        st.markdown(ticket_html, unsafe_allow_html=True)

        # Posta bidalketa
        asunto = f"Eskola Erreserba: {nombre_escuela}"
        cuerpo = f"Ikastetxea: {nombre_escuela}\nTelefonoa: {telefono_escuela}\n\n--- ZEHAZTAPENAK ---\n{desglose_email}\nIkasleak guztira: {total_alumnos}\nDoako irakasleak: {profes_gratis}\n\nGUZTIRA: {presupuesto_total:.2f} EUR"
        mailto_link = f"mailto:info@mendexapark.com,ikerlarrap@gmail.com?subject={urllib.parse.quote(asunto)}&body={urllib.parse.quote(cuerpo)}"
        st.markdown(f'<br><a href="{mailto_link}" target="_blank"><button style="background-color:#4CAF50; color:white; border:none; padding:10px 20px; border-radius:5px; cursor:pointer;">📩 Bidali eskaera (info@mendexapark.com)</button></a>', unsafe_allow_html=True)

st.divider()
st.caption("Mendexa Abentura Park | info@mendexapark.com | 688 85 62 83")
