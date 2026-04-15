import streamlit as st
import urllib.parse
import re
from fpdf import FPDF
import io

# Orrialdearen konfigurazioa / Configuración de la página
st.set_page_config(page_title="Mendexa Abentura Park Planner", layout="wide")

# --- FUNCIONES DE APOYO ---
def es_email_valido(email):
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(patron, email) is not None

def es_telefono_valido(tel):
    return len(tel) >= 9 and tel.isdigit()

def generar_pdf_pro(escuela, tel, email, total, alumnos, precio_medio, lineas, profes):
    pdf = FPDF()
    pdf.add_page()
    
    # Colores corporativos (Verde Mendexa)
    v_r, v_g, v_b = (46, 125, 50)
    
    # Cabecera
    pdf.set_font('Arial', 'B', 22)
    pdf.set_text_color(v_r, v_g, v_b)
    pdf.cell(0, 15, 'MENDEXA ABENTURA PARK', ln=True, align='C')
    
    pdf.set_font('Arial', 'I', 12)
    pdf.set_text_color(100)
    pdf.cell(0, 10, 'Eskola Erreserba / Presupuesto Escolar', ln=True, align='C')
    pdf.ln(10)
    
    # Bloque de datos del cliente
    pdf.set_fill_color(245, 245, 245)
    pdf.set_text_color(0)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f" Ikastetxea / Centro: {escuela}", ln=True, fill=True)
    pdf.set_font('Arial', '', 11)
    pdf.cell(0, 8, f" Telefonoa / Tel: {tel}", ln=True)
    pdf.cell(0, 8, f" Email: {email}", ln=True)
    pdf.ln(10)
    
    # Detalle de actividades
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(v_r, v_g, v_b)
    pdf.cell(0, 10, 'Hautatutako jarduerak / Detalle de actividades:', ln=True)
    pdf.set_draw_color(v_r, v_g, v_b)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)
    
    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(50)
    for linea in lineas:
        pdf.cell(0, 8, f"- {linea}", ln=True)
    
    pdf.ln(10)
    
    # Cuadro de Totales
    pdf.set_fill_color(v_r, v_g, v_b)
    pdf.set_text_color(255)
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(100, 12, " GUZTIRA / TOTAL (BEZ barne)", fill=True)
    pdf.cell(90, 12, f"{total:.2f} EUR  ", fill=True, align='R', ln=True)
    
    pdf.ln(5)
    pdf.set_text_color(100)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 8, f"Ikasleak guztira: {alumnos}  |  Batez besteko prezioa: {precio_medio:.2f} EUR/ikasle", ln=True)
    pdf.cell(0, 8, f"Doako irakasleak: {profes} plaza", ln=True)
    
    # Pie de página
    pdf.set_y(-40)
    pdf.set_font('Arial', 'I', 8)
    pdf.set_text_color(150)
    pdf.multi_cell(0, 5, "Aurrekontu hau informatiboa da eta prezioak taldearen tamainaren arabera kalkulatu dira. \nEgin klik 'Bidali' botoian aplikazioan erreserba berresteko.", align='C')
    
    return pdf.output(dest='S').encode('latin-1')

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
    st.markdown("### 📝 Aukeratu zure jarduera-paketea / Elige tu paquete de actividades")
    
    with st.expander("💶 Prezioen Taula / Tabla de Precios"):
        st.markdown("""
        | Programa | 10-19 ikasle | 20-29 ikasle | +29 ikasle |
        | :--- | :---: | :---: | :---: |
        | **YOKO SOILIK** | **15,70 €** | **14,70 €** | **13,70 €** |
        | **2 ZIRKUITU** | **21,00 €** | **20,00 €** | **19,00 €** |
        | **3 ZIRKUITU** | **23,00 €** | **22,00 €** | **21,00 €** |
        """)
    
    info_programak = {
        "🟣 🟠 🟡 1 ZIRKUITUA: YOKO SOILIK": {"desc": "Demo + Laranja + 3 itzuli Yoko. 4-8 urte.", "id": "yoko", "cat": "yoko"},
        "🟣 🟠 🟢 🟢 2 ZIRKUITU (9 urte +)": {"desc": "Demo + Laranja + 2 Zirkuitu Berde. >9 urte.", "id": "2c_9", "cat": "2c"},
        "🟣 🟠 🟢 🔵 2 ZIRKUITU (12 urte +)": {"desc": "Demo + Laranja + Berdea + Urdina. >12 urte.", "id": "2c_12", "cat": "2c"},
        "🟣 🟠 🟢 🔵 🔵 3 ZIRKUITU (12-14 urte)": {"desc": "Demo + Laranja + Berdea + 2 Urdin. 12-14 urte.", "id": "3c_12", "cat": "3c"},
        "🟣 🟠 🟢 🔵 🔴 3 ZIRKUITU (15 urte +)": {"desc": "Demo + Laranja + Berdea + Urdina + Gorria. >15 urte.", "id": "3c_15", "cat": "3c"}
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

        # --- SEMÁFORO ---
        b1, b2, b3 = ("#4CAF50", "white") if tier == 1 else ("#e0e0e0", "#666"), ("#4CAF50", "white") if tier == 2 else ("#e0e0e0", "#666"), ("#4CAF50", "white") if tier == 3 else ("#e0e0e0", "#666")
        st.markdown(f'<div style="display: flex; justify-content: space-between; margin-bottom: 15px;"><div style="background:{b1[0]}; color:{b1[1]}; padding:8px; border-radius:5px; width:32%; text-align:center; font-size:0.8em; font-weight:bold;">10-19 ikasle</div><div style="background:{b2[0]}; color:{b2[1]}; padding:8px; border-radius:5px; width:32%; text-align:center; font-size:0.8em; font-weight:bold;">20-29 ikasle</div><div style="background:{b3[0]}; color:{b3[1]}; padding:8px; border-radius:5px; width:32%; text-align:center; font-size:0.8em; font-weight:bold;">+29 ikasle</div></div>', unsafe_allow_html=True)

        presupuesto_total = 0
        listado_html = ""
        lineas_pdf = []

        for titulo, num in alumnos_por_programa.items():
            if num > 0:
                cat = info_programak[titulo]['cat']
                precio = (13.70 if tier == 3 else 14.70 if tier == 2 else 15.70) if cat == "yoko" else (19.00 if tier == 3 else 20.00 if tier == 2 else 21.00) if cat == "2c" else (21.00 if tier == 3 else 22.00 if tier == 2 else 23.00)
                subtotal = num * precio
                presupuesto_total += subtotal
                listado_html += f"<div style='border-left:4px solid #2E7D32; padding-left:10px; margin-bottom:8px;'><strong>{num} ikasle</strong> - {titulo}<br>{precio:.2f}€ x {num} = {subtotal:.2f}€</div>"
                lineas_pdf.append(f"{num} ikasle - {titulo} ({precio:.2f} EUR/u): {subtotal:.2f} EUR")

        profes_gratis = total_alumnos // 10
        precio_medio = presupuesto_total / total_alumnos
        
        c_t1, c_t2 = st.columns(2)
        c_t1.metric("Guztira", f"{presupuesto_total:.2f} €")
        c_t2.metric("Ikasleko", f"{precio_medio:.2f} €")
        
        datos_listos = nombre_escuela != "" and es_email_valido(email_escuela) and es_telefono_valido(telefono_escuela)

        st.divider()
        if st.button("Aurrekontua Sortu / Generar", type="primary", disabled=not datos_listos):
            st.balloons()
            st.markdown(f'<div style="border:5px solid #2E7D32; border-radius:15px; padding:20px; background:#fcfcfc;"><h3 style="color:#2E7D32; text-align:center;">🌲 MENDEXA ABENTURA PARK 🌲</h3><p><strong>Eskola:</strong> {nombre_escuela}</p>{listado_html}<h3 style="text-align:right; color:#2E7D32;">GUZTIRA: {presupuesto_total:.2f} €</h3></div>', unsafe_allow_html=True)
            
            # --- PDF GENERATOR ---
            pdf_bytes = generar_pdf_pro(nombre_escuela, telefono_escuela, email_escuela, presupuesto_total, total_alumnos, precio_medio, lineas_pdf, profes_gratis)
            st.download_button("📥 Deskargatu PDF Profesionala", data=pdf_bytes, file_name=f"Aurrekontua_Mendexa_{nombre_escuela}.pdf", mime="application/pdf")
            
            # --- MAILTO ---
            asunto = f"Eskola Erreserba: {nombre_escuela}"
            cuerpo = f"Ikastetxea: {nombre_escuela}\nTotal: {presupuesto_total:.2f}€"
            mailto_link = f"mailto:ikerlarrap@gmail.com?subject={urllib.parse.quote(asunto)}&body={urllib.parse.quote(cuerpo)}"
            st.markdown(f'<div style="text-align: center; margin-top: 15px;"><a href="{mailto_link}" target="_blank"><button style="background-color:#4CAF50; color:white; border:none; padding:12px 20px; border-radius:8px; cursor:pointer;">📧 Bidali eskaera orain</button></a></div>', unsafe_allow_html=True)

st.divider()
st.caption("Mendexa Abentura Park | 688 85 62 83")
