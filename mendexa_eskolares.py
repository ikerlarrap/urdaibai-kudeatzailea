import streamlit as st
import urllib.parse

# Orrialdearen konfigurazioa / Configuración de la página
st.set_page_config(page_title="Mendexa Abentura Park Planner", layout="wide")

# --- 1. LOGOA ETA ESTILOA ---
try:
    st.image("logo_mendexa.png", width=250)
except:
    st.markdown("🌲 **MENDEXA ABENTURA PARK**")

# --- 2. IZENBURUAK ---
st.title("Mendexa Abentura Park: Eskolentzako Kalkulagailua 🌲🌲🧗")
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

# --- 4. ERRESERBA XEHETASUNAK ---
col_input, col_result = st.columns([1.3, 1])

with col_input:
    st.markdown("### 📝 Aukeratu zure jarduera-paketea / Elige tu paquete de actividades")
    
    # Programen definizio zehatza
    info_programak = {
        "🟣 🟠 🟡  1 ZIRKUITUA: YOKO SOILIK": {
            "desc": "Demo + Laranja + 3 itzuli Yoko zirkuituan",
            "req": "Adina: 4-8 (9) urte | Altuera: 1'10m - 1'40m",
            "id": "yoko"
        },
        "🟣 🟠 🟢 🟢  2 ZIRKUITU (9 urte +)": {
            "desc": "Demo + Laranja + 2 Zirkuitu Berde",
            "req": "Adina: >9 urte | Altuera: >1'40m",
            "id": "2c_9"
        },
        "🟣 🟠 🟢 🔵  2 ZIRKUITU (12 urte +)": {
            "desc": "Demo + Laranja + Zirkuitu Berdea + Urdina",
            "req": "Adina: >12 urte | Altuera: >1'50m",
            "id": "2c_12"
        },
        "🟣 🟠 🟢 🔵 🔵  3 ZIRKUITU (12-14 urte)": {
            "desc": "Demo + Laranja + Zirkuitu Berdea + 2 Urdin",
            "req": "Adina: 12-14 urte | Altuera: >1'50m",
            "id": "3c_12"
        },
        "🟣 🟠 🟢 🔵 🔴  3 ZIRKUITU (15 urte +)": {
            "desc": "Demo + Laranja + Berdea + Urdina + Gorria",
            "req": "Adina: >15 urte | Altuera: >1'50m",
            "id": "3c_15"
        }
    }

    alumnos_por_programa = {}
    total_alumnos = 0

    for titulo, info in info_programak.items():
        with st.expander(f"{titulo}", expanded=True):
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"**Ibilbidea:** {info['desc']}")
                st.caption(f"Mugak: {info['req']}")
            with c2:
                num = st.number_input("Ikasleak", min_value=0, value=0, key=info['id'])
                alumnos_por_programa[titulo] = num
                total_alumnos += num

    st.markdown("---")
    num_profesores = st.number_input("Irakasle kopurua guztira:", min_value=1, value=2)

    # SECCIÓN INFORMATIVA REQUERIDA
    with st.expander("ℹ️ Zer dago barne? / ¿Qué incluye?"):
        st.markdown("""
        * **Zer barne dago?**: Monitoreak, aseguruak, beharrezko material guztia eta instalazioen erabilera (komunak barne).
        * **Jantziak**: Arropa erosoa eta kirol oinetako itxiak (debekatuta sandaliak). Ile luzea jasoa eta poltsikoak hutsik.
        * **Eguraldia**: Jarduera euriarekin egin daiteke. Haize indartsua edo ekaitza badago, parkeko arduradunek erabakiko dute.
        * **Ordutegia**: Txandak mailakatuak dira (9:00etatik aurrera). Zuen beharretara egokitzen gara.
        """)

with col_result:
    st.markdown("### 💰 Aurrekontu Laburpena / Resumen")
    
    if total_alumnos == 0:
        st.info("👈 Gehitu ikasleak ezkerrean aurrekontua ikusteko.")
    else:
        # Tramos de precio según el total de alumnos
        if total_alumnos > 29: tier = 3
        elif 20 <= total_alumnos <= 29: tier = 2
        else: tier = 1

        presupuesto_total = 0
        listado_resumen_html = ""
        desglose_email = ""

        for titulo, num in alumnos_por_programa.items():
            if num > 0:
                if "YOKO" in titulo:
                    precio = 13.70 if tier == 3 else 14.70 if tier == 2 else 15.70
                elif "2 ZIRKUITU" in titulo:
                    precio = 19.00 if tier == 3 else 20.00 if tier == 2 else 21.00
                else: # 3 ZIRKUITU
                    precio = 21.00 if tier == 3 else 22.00 if tier == 2 else 23.00

                subtotal = num * precio
                presupuesto_total += subtotal
                
                listado_resumen_html += f"""
<div style='margin-bottom: 12px; border-left: 4px solid #2E7D32; padding-left: 10px;'>
<span style='font-size: 1.1em;'><strong>{num} ikasle</strong> - {titulo}</span><br>
<small style='color: #555;'>{info_programak[titulo]['desc']}</small><br>
<span style='color: #2E7D32; font-weight: bold;'>{precio:.2f}€ x {num} = {subtotal:.2f}€</span>
</div>"""
                desglose_email += f"- {num} ikasle: {titulo} ({precio:.2f}€/u) = {subtotal:.2f}€\n"

        profes_gratis = total_alumnos // 10
        
        st.metric("Guztira / Total", f"{presupuesto_total:.2f} €")
        st.write(f"👥 **Ikasleak guztira:** {total_alumnos}")
        st.write(f"🎁 **Doako irakasleak:** {profes_gratis} plaza")
        
        if tier == 3:
            st.success("✅ Talde handiko tarifa aplikatu da (>29 ikasle).")

        # --- 5. TICKET ETA BIDALKETA ---
        st.divider()
        st.markdown("### 📥 Eskaera Berretsi / Confirmar Solicitud")

        if st.button("Aurrekontua Sortu / Generar Resguardo", type="primary"):
            if nombre_escuela == "" or email_escuela == "":
                st.error("⚠️ Mesedez, bete ikastetxearen datuak. / Rellena los datos del colegio arriba.")
            else:
                st.balloons()
                
                # 1. El Ticket Visual
                ticket_html = f"""
<div style="border: 5px solid #2E7D32; border-radius: 15px; padding: 25px; background-color: #fcfcfc; font-family: sans-serif; box-shadow: 10px 10px 20px rgba(0,0,0,0.05);">
<h2 style="color: #2E7D32; text-align: center; margin-top: 0;">🌲 MENDEXA ABENTURA PARK 🌲</h2>
<h4 style="text-align: center; color: #666; margin-bottom: 20px;">ESKOLA ERRESERBA / RESGUARDO</h4>
<hr style="border: 1px solid #2E7D32; margin-bottom: 20px;">
<p style="font-size: 1.1em;"><strong>Ikastetxea:</strong> {nombre_escuela}</p>
<p style="font-size: 1.1em;"><strong>Taldea:</strong> {total_alumnos} ikasle (+ {num_profesores} irakasle)</p>
<div style="background: #f0f0f0; padding: 20px; border-radius: 10px; margin: 20px 0;">
<h4 style="margin-top: 0; color: #2E7D32; border-bottom: 1px solid #ccc; padding-bottom: 5px;">Aukeratutakoa / Detalle:</h4>
{listado_resumen_html}
</div>
<div style="text-align: right; border-top: 2px solid #2E7D32; padding-top: 15px;">
<span style="font-size: 1.2em; color: #444;">AURREKONTUA GUZTIRA:</span><br>
<span style="font-size: 2.2em; color: #2E7D32; font-weight: bold;">{presupuesto_total:.2f} €</span>
<p style="font-size: 0.8em; color: #888; margin-top: 5px;">BEZ %10 barne / IVA 10% incluido</p>
</div>
</div>"""
                st.markdown(ticket_html, unsafe_allow_html=True)
                st.info("💡 Aholkua: Egin pantaila-argazkia edo gorde PDF gisa. / Guarda este ticket.")

                # 2. El Botón de abrir el correo (Método simple de Urdaibai)
                asunto = f"Eskola Erreserba Test: {nombre_escuela}"
                cuerpo = f"Ikastetxea: {nombre_escuela}\nTelefonoa: {telefono_escuela}\nEmail: {email_escuela}\n\n--- HAUTATUTAKO PROGRAMAK ---\n{desglose_email}\nIkasleak guztira: {total_alumnos}\nIrakasle doakoak: {profes_gratis}\n\nPREZIOA GUZTIRA: {presupuesto_total:.2f} EUR"
                
                # MAILTO para pruebas
                mailto_link = f"mailto:ikerlarrap@gmail.com?subject={urllib.parse.quote(asunto)}&body={urllib.parse.quote(cuerpo)}"
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(f'<div style="text-align: center;"><a href="{mailto_link}" target="_blank" style="text-decoration:none;"><button style="background-color:#4CAF50; color:white; border:none; padding:15px 30px; border-radius:8px; cursor:pointer; font-size:18px; font-weight:bold; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">📩 Ireki posta eta bidali eskaera / Abrir correo y enviar</button></a></div>', unsafe_allow_html=True)

st.divider()
st.caption("Mendexa Abentura Park | info@mendexapark.com | 688 85 62 83")
