import streamlit as st
import urllib.parse
import re

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Mendexa Abentura Park Planner", layout="wide")

# --- FUNCIONES DE VALIDACIÓN ---
def es_email_valido(email):
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(patron, email) is not None

def es_telefono_valido(tel):
    return len(tel) >= 9 and tel.isdigit()

# --- 1. LOGO ---
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

# --- 4. SELECCIÓN DE ACTIVIDADES ---
col_input, col_result = st.columns([1.4, 1])

with col_input:
    st.markdown("### 📝 Aukeratu zure jarduera-paketea / Elige tu paquete")
    
    with st.expander("💶 Prezioen Taula / Tabla de Precios"):
        st.markdown("""
        | Programa | 10-19 ikasle | 20-29 ikasle | +29 ikasle |
        | :--- | :---: | :---: | :---: |
        | **YOKO SOILIK** | **15,70 €** | **14,70 €** | **13,70 €** |
        | **2 ZIRKUITU** | **21,00 €** | **20,00 €** | **19,00 €** |
        | **3 ZIRKUITU** | **23,00 €** | **22,00 €** | **21,00 €** |
        """)
    
    info_programak = {
        "🟣 🟠 🟡 1 ZIRKUITUA: YOKO SOILIK": {"id": "yoko", "cat": "yoko", "desc": "4-8 urte"},
        "🟣 🟠 🟢 🟢 2 ZIRKUITU (9 urte +)": {"id": "2c_9", "cat": "2c", "desc": ">9 urte"},
        "🟣 🟠 🟢 🔵 2 ZIRKUITU (12 urte +)": {"id": "2c_12", "cat": "2c", "desc": ">12 urte"},
        "🟣 🟠 🟢 🔵 🔵 3 ZIRKUITU (12-14 urte)": {"id": "3c_12", "cat": "3c", "desc": "12-14 urte"},
        "🟣 🟠 🟢 🔵 🔴 3 ZIRKUITU (15 urte +)": {"id": "3c_15", "cat": "3c", "desc": ">15 urte"}
    }

    alumnos_por_programa = {}
    total_alumnos = 0

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

with col_result:
    st.markdown("### 💰 Aurrekontu Laburpena / Resumen")
    
    if total_alumnos == 0:
        st.info("👈 Gehitu ikasleak ezkerrean.")
    else:
        tier = 3 if total_alumnos > 29 else 2 if total_alumnos >= 20 else 1

        # --- SEMÁFORO DE TARIFAS ---
        colors = ["#4CAF50" if tier == i else "#e0e0e0" for i in range(1, 4)]
        texts = ["white" if tier == i else "#666" for i in range(1, 4)]
        
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
            <div style="background:{colors[0]}; color:{texts[0]}; padding:8px; border-radius:5px; width:32%; text-align:center; font-size:0.8em; font-weight:bold;">10-19 ik</div>
            <div style="background:{colors[1]}; color:{texts[1]}; padding:8px; border-radius:5px; width:32%; text-align:center; font-size:0.8em; font-weight:bold;">20-29 ik</div>
            <div style="background:{colors[2]}; color:{texts[2]}; padding:8px; border-radius:5px; width:32%; text-align:center; font-size:0.8em; font-weight:bold;">+29 ik</div>
        </div>
        """, unsafe_allow_html=True)

        presupuesto_total = 0
        listado_html = ""
        texto_descarga = f"MENDEXA ABENTURA PARK - AURREKONTUA\nEskola: {nombre_escuela}\n"

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
                listado_html += f"<li>{num} ikasle - {titulo}: {subtotal:.2f}€</li>"
                texto_descarga += f"- {num} ikasle - {titulo}: {subtotal:.2f}€\n"

        precio_medio = presupuesto_total / total_alumnos
        st.metric("Guztira / Total", f"{presupuesto_total:.2f} €")
        st.metric("Ikasleko / Por alumno", f"{precio_medio:.2f} €")
        
        st.write(f"👥 Ikasleak: {total_alumnos} | 🎁 Doako plaza: {total_alumnos // 10}")
        
        # VALIDACIÓN PARA EL BOTÓN
        datos_listos = nombre_escuela != "" and es_email_valido(email_escuela) and es_telefono_valido(telefono_escuela)

        st.divider()
        if st.button("Aurrekontua Sortu / Generar", type="primary", disabled=not datos_listos):
            st.balloons()
            
            st.markdown(f"""
            <div style="border: 4px solid #2E7D32; border-radius: 10px; padding: 20px; background: #f9f9f9;">
                <h3 style="color: #2E7D32; text-align: center;">🌲 MENDEXA ABENTURA PARK</h3>
                <p><b>Ikastetxea:</b> {nombre_escuela}</p>
                <ul>{listado_html}</ul>
                <h4 style="text-align: right;">GUZTIRA: {presupuesto_total:.2f} €</h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Botón de descarga TXT (Sin librerías externas para evitar errores)
            texto_descarga += f"\nTOTALA: {presupuesto_total:.2f}€\nIkasleko: {precio_medio:.2f}€"
            st.download_button("📩 Deskargatu aurrekontua (TXT)", data=texto_descarga, file_name=f"Aurrekontua_{nombre_escuela}.txt")

            # Botón Email
            asunto = urllib.parse.quote(f"Reserva: {nombre_escuela}")
            cuerpo = urllib.parse.quote(f"Ikastetxea: {nombre_escuela}\nTotal: {presupuesto_total:.2f}€")
            mailto_link = f"mailto:ikerlarrap@gmail.com?subject={asunto}&body={cuerpo}"
            st.markdown(f'<center><a href="{mailto_link}" target="_blank"><button style="background:#4CAF50; color:white; border:none; padding:12px; border-radius:8px; cursor:pointer; font-weight:bold;">📧 Bidali eskaera orain</button></a></center>', unsafe_allow_html=True)

st.divider()
st.caption("Mendexa Abentura Park | 688 85 62 83")
