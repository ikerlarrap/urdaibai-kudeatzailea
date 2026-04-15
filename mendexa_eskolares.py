import streamlit as st
import urllib.parse
import re

# Configuración de la página
st.set_page_config(page_title="Mendexa Abentura Park Planner", layout="wide")

# --- FUNCIONES DE VALIDACIÓN ---
def es_email_valido(email):
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(patron, email) is not None

def es_telefono_valido(tel):
    return len(tel) >= 9 and tel.isdigit()

# --- 1. LOGO Y ESTILO ---
try:
    st.image("logo_mendexa.png", width=250)
except:
    st.markdown("🌲 **MENDEXA ABENTURA PARK**")

# --- 2. TÍTULOS ---
st.title("Mendexa Abentura Park: Eskolentzako Kalkulagailua 🌲🌲🧗")
st.subheader("Kalkulatu zure aurrekontua momentuan / Calcula tu presupuesto al instante")

# --- 3. DATOS DE LA ESCUELA ---
st.markdown("### 🏫 Ikastetxearen Datuak / Datos de la Escuela")
col_esc1, col_esc2, col_esc3 = st.columns(3)

with col_esc1:
    nombre_escuela = st.text_input("Ikastetxearen izena / Nombre del colegio")
with col_esc2:
    telefono_escuela = st.text_input("Telefonoa / Teléfono")
    if telefono_escuela and not es_telefono_valido(telefono_escuela):
        st.caption("⚠️ Sartu gutxienez 9 zenbaki / Mínimo 9 números")
with col_esc3:
    email_escuela = st.text_input("Posta elektronikoa / Email")
    if email_escuela and not es_email_valido(email_escuela):
        st.caption("⚠️ Email okerra / Email no válido")

st.divider()

# --- 4. SELECCIÓN DE ACTIVIDADES (DISEÑO COMPACTO) ---
col_input, col_result = st.columns([1.4, 1])

with col_input:
    st.markdown("### 📝 Aukeratu zure jarduera-paketea / Elige tu paquete de actividades")
    
    info_programak = {
        "🟣 🟠 🟡 1 ZIRKUITUA: YOKO SOILIK": {
            "desc": "Demo + Laranja + 3 itzuli Yoko zirkuituan. Adina: 4-8 (9) urte.",
            "id": "yoko", "cat": "yoko"
        },
        "🟣 🟠 🟢 🟢 2 ZIRKUITU (9 urte +)": {
            "desc": "Demo + Laranja + 2 Zirkuitu Berde. Adina: >9 urte.",
            "id": "2c_9", "cat": "2c"
        },
        "🟣 🟠 🟢 🔵 2 ZIRKUITU (12 urte +)": {
            "desc": "Demo + Laranja + Zirkuitu Berdea + Urdina. Adina: >12 urte.",
            "id": "2c_12", "cat": "2c"
        },
        "🟣 🟠 🟢 🔵 🔵 3 ZIRKUITU (12-14 urte)": {
            "desc": "Demo + Laranja + Zirkuitu Berdea + 2 Urdin. Adina: 12-14 urte.",
            "id": "3c_12", "cat": "3c"
        },
        "🟣 🟠 🟢 🔵 🔴 3 ZIRKUITU (15 urte +)": {
            "desc": "Demo + Laranja + Berdea + Urdina + Gorria. Adina: >15 urte.",
            "id": "3c_15", "cat": "3c"
        }
    }

    alumnos_por_programa = {}
    total_alumnos = 0

    # Diseño en filas compactas (sustituye a los expanders)
    for titulo, info in info_programak.items():
        c1, c2, c3 = st.columns([0.1, 4, 1.5])
        with c2:
            st.markdown(f"**{titulo}**", help=info['desc'])
        with c3:
            num = st.number_input("Kopurua", min_value=0, step=1, key=info['id'], label_visibility="collapsed")
            alumnos_por_programa[titulo] = num
            total_alumnos += num

    st.markdown("---")
    num_profesores = st.number_input("Irakasle kopurua guztira:", min_value=0, value=2)

    with st.expander("ℹ️ Zer dago barne? / ¿Qué incluye?"):
        st.markdown("* Monitoreak, aseguruak eta materiala barne. Arropa erosoa eta oinetako itxiak beharrezkoak dira.")

with col_result:
    st.markdown("### 💰 Aurrekontu Laburpena / Resumen")
    
    if total_alumnos == 0:
        st.info("👈 Gehitu ikasleak ezkerrean.")
    else:
        # Lógica de tramos (Tiers)
        if total_alumnos > 29: tier = 3
        elif 20 <= total_alumnos <= 29: tier = 2
        else: tier = 1

        # --- SEMÁFORO DE TARIFAS ---
        bg_t1 = "#4CAF50" if tier == 1 else "#e0e0e0"
        bg_t2 = "#4CAF50" if tier == 2 else "#e0e0e0"
        bg_t3 = "#4CAF50" if tier == 3 else "#e0e0e0"
        
        color_t1 = "white" if tier == 1 else "#666"
        color_t2 = "white" if tier == 2 else "#666"
        color_t3 = "white" if tier == 3 else "#666"

        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; margin-bottom: 15px; font-family: sans-serif;">
            <div style="background-color: {bg_t1}; color: {color_t1}; padding: 8px 5px; border-radius: 5px; font-size: 0.85em; text-align: center; width: 32%; font-weight: bold;">
                10-19 ikasle<br><small style="font-weight: normal;">Tarifa Normala</small>
            </div>
            <div style="background-color: {bg_t2}; color: {color_t2}; padding: 8px 5px; border-radius: 5px; font-size: 0.85em; text-align: center; width: 32%; font-weight: bold;">
                20-29 ikasle<br><small style="font-weight: normal;">-1€ Deskontua</small>
            </div>
            <div style="background-color: {bg_t3}; color: {color_t3}; padding: 8px 5px; border-radius: 5px; font-size: 0.85em; text-align: center; width: 32%; font-weight: bold;">
                +29 ikasle<br><small style="font-weight: normal;">-2€ Deskontua</small>
            </div>
        </div>
        """, unsafe_allow_html=True)

        presupuesto_total = 0
        listado_resumen_html = ""
        texto_descarga = f"MENDEXA ABENTURA PARK - AURREKONTUA\nEskola: {nombre_escuela}\n"
        texto_descarga += "-"*40 + "\n"

        for titulo, num in alumnos_por_programa.items():
            if num > 0:
                cat = info_programak[titulo]['cat']
                if cat == "yoko":
                    precio = 13.70 if tier == 3 else 14.70 if tier == 2 else 15.70
                elif cat == "2c":
                    precio = 19.00 if tier == 3 else 20.00 if tier == 2 else 21.00
                else:
                    precio = 21.00 if tier == 3 else 22.00 if tier == 2 else 23.00

                subtotal = num * precio
                presupuesto_total += subtotal
                
                listado_resumen_html += f"""
<div style='margin-bottom: 8px; border-left: 4px solid #2E7D32; padding-left: 10px;'>
<strong>{num} ikasle</strong> - {titulo}<br>
<span style='color: #2E7D32;'>{precio:.2f}€ x {num} = {subtotal:.2f}€</span>
</div>"""
                texto_descarga += f"{num} ikasle - {titulo}: {subtotal:.2f}€\n"

        profes_gratis = total_alumnos // 10
        st.metric("Guztira / Total", f"{presupuesto_total:.2f} €")
        st.write(f"👥 Ikasleak: {total_alumnos} | 🎁 Doako plaza: {profes_gratis}")
        
        # Bloqueo de botón si los datos no son válidos o están vacíos
        datos_listos = nombre_escuela != "" and es_email_valido(email_escuela) and es_telefono_valido(telefono_escuela)

        st.divider()
        if st.button("Aurrekontua Sortu / Generar", type="primary", disabled=not datos_listos):
            st.balloons()
            
            ticket_html = f"""
<div style="border: 5px solid #2E7D32; border-radius: 15px; padding: 25px; background-color: #fcfcfc; font-family: sans-serif;">
<h2 style="color: #2E7D32; text-align: center; margin-top: 0;">🌲 MENDEXA ABENTURA PARK 🌲</h2>
<p><strong>Ikastetxea:</strong> {nombre_escuela}<br><strong>Taldea:</strong> {total_alumnos} ikasle</p>
<div style="background: #f0f0f0; padding: 15px; border-radius: 10px; margin: 15px 0;">
{listado_resumen_html}
</div>
<h3 style="text-align: right; color: #2E7D32;">GUZTIRA: {presupuesto_total:.2f} €</h3>
</div>"""
            st.markdown(ticket_html, unsafe_allow_html=True)
            
            # EXPORTACIÓN: Botón de descarga
            texto_descarga += f"\nTOTALA: {presupuesto_total:.2f}€\nBEZ barne."
            st.download_button("📩 Deskargatu aurrekontua (TXT)", data=texto_descarga, file_name=f"presupuesto_mendexa_{nombre_escuela.replace(' ', '_')}.txt")

            # EMAIL: Mailto
            asunto = f"Eskola Erreserba: {nombre_escuela}"
            cuerpo = f"Ikastetxea: {nombre_escuela}\nTelefonoa: {telefono_escuela}\nTotal: {presupuesto_total:.2f}€\n\nIkusi erantsitako dokumentua xehetasunetarako."
            mailto_link = f"mailto:ikerlarrap@gmail.com?subject={urllib.parse.quote(asunto)}&body={urllib.parse.quote(cuerpo)}"
            st.markdown(f'<div style="text-align: center; margin-top: 15px;"><a href="{mailto_link}" target="_blank"><button style="background-color:#4CAF50; color:white; border:none; padding:12px 20px; border-radius:8px; cursor:pointer;">📧 Bidali eskaera orain</button></a></div>', unsafe_allow_html=True)

st.divider()
st.caption("Mendexa Abentura Park | 688 85 62 83")
