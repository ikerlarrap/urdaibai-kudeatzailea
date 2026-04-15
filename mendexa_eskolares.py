import streamlit as st
import urllib.parse
import re
from fpdf import FPDF

# Configuración de la página
st.set_page_config(page_title="Mendexa Abentura Park Planner", layout="wide")

# --- FUNCIONES DE APOYO ---
def es_email_valido(email):
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(patron, email) is not None

def es_telefono_valido(tel):
    return len(tel) >= 9 and tel.isdigit()

def generar_pdf_pro(escuela, tel, email, total, alumnos, precio_medio, desglose, profes):
    pdf = FPDF()
    pdf.add_page()
    verde_mendexa = (46, 125, 50)
    pdf.set_font('Arial', 'B', 20)
    pdf.set_text_color(*verde_mendexa)
    pdf.cell(0, 10, 'MENDEXA ABENTURA PARK', ln=True, align='C')
    pdf.set_font('Arial', '', 12)
    pdf.set_text_color(100)
    pdf.cell(0, 10, 'Eskola Erreserba / Presupuesto Escolar', ln=True, align='C')
    pdf.ln(10)
    pdf.set_fill_color(240, 240, 240)
    pdf.set_text_color(0)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f" Ikastetxea: {escuela}", ln=True, fill=True)
    pdf.set_font('Arial', '', 11)
    pdf.cell(0, 8, f" Telefonoa: {tel}", ln=True)
    pdf.cell(0, 8, f" Email: {email}", ln=True)
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(*verde_mendexa)
    pdf.cell(0, 10, 'Hautatutako jarduerak:', ln=True)
    pdf.ln(2)
    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(50)
    for linea in desglose:
        pdf.multi_cell(0, 8, f"- {linea}")
    pdf.ln(5)
    pdf.set_fill_color(46, 125, 50)
    pdf.set_text_color(255)
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(95, 12, f" GUZTIRA / TOTAL:", fill=True)
    pdf.cell(95, 12, f" {total:.2f} EUR ", fill=True, align='R', ln=True)
    pdf.set_text_color(0)
    pdf.set_font('Arial', '', 11)
    pdf.cell(0, 10, f" Ikasleak: {alumnos} | Batez besteko prezioa: {precio_medio:.2f} EUR/ik", ln=True)
    return pdf.output(dest='S').encode('latin-1')

# --- UI ---
try:
    st.image("logo_mendexa.png", width=250)
except:
    st.markdown("🌲 **MENDEXA ABENTURA PARK**")

st.title("Mendexa Abentura Park: Eskolentzako Kalkulagailua 🌲🌲🧗")

# DATOS ESCUELA
st.markdown("### 🏫 Ikastetxearen Datuak")
c_e1, c_e2, c_e3 = st.columns(3)
with c_e1: nombre_escuela = st.text_input("Ikastetxearen izena")
with c_e2: telefono_escuela = st.text_input("Telefonoa")
with c_e3: email_escuela = st.text_input("Posta elektronikoa")

st.divider()

col_input, col_result = st.columns([1.4, 1])

with col_input:
    st.markdown("### 📝 Aukeratu zure jarduera-paketea")
    
    with st.expander("💶 Prezioen Taula / Tabla de Precios"):
        st.markdown("| Programa | 10-19 ik | 20-29 ik | +29 ik |\n| :--- | :---: | :---: | :---: |\n| YOKO | 15,70€ | 14,70€ | 13,70€ |\n| 2 ZIRK | 21,00€ | 20,00€ | 19,00€ |\n| 3 ZIRK | 23,00€ | 22,00€ | 21,00€ |")

    info_programak = {
        "🟣 🟠 🟡 1 ZIRKUITUA: YOKO SOILIK": {"desc": "Yoko 3 itzuli. 4-8 urte.", "id": "yoko", "cat": "yoko"},
        "🟣 🟠 🟢 🟢 2 ZIRKUITU (9 urte +)": {"desc": "2 Berde. >9 urte.", "id": "2c_9", "cat": "2c"},
        "🟣 🟠 🟢 🔵 2 ZIRKUITU (12 urte +)": {"desc": "Berdea + Urdina. >12 urte.", "id": "2c_12", "cat": "2c"},
        "🟣 🟠 🟢 🔵 🔵 3 ZIRKUITU (12-14 urte)": {"desc": "Berdea + 2 Urdin. 12-14 urte.", "id": "3c_12", "cat": "3c"},
        "🟣 🟠 🟢 🔵 🔴 3 ZIRKUITU (15 urte +)": {"desc": "Berdea + Urdina + Gorria. >15 urte.", "id": "3c_15", "cat": "3c"}
    }

    alumnos_por_programa = {}
    total_alumnos = 0
    for titulo, info in info_programak.items():
        c1, c2, c3 = st.columns([0.1, 4, 1.5])
        with c2: st.markdown(f"**{titulo}**", help=info['desc'])
        with c3:
            num = st.number_input("Kop", min_value=0, step=1, key=info['id'], label_visibility="collapsed")
            alumnos_por_programa[titulo] = num
            total_alumnos += num

with col_result:
    st.markdown("### 💰 Aurrekontu Laburpena")
    if total_alumnos > 0:
        tier = 3 if total_alumnos > 29 else 2 if total_alumnos >= 20 else 1
        
        # Semaforo visual
        b1 = "#4CAF50" if tier == 1 else "#e0e0e0"
        b2 = "#4CAF50" if tier == 2 else "#e0e0e0"
        b3 = "#4CAF50" if tier == 3 else "#e0e0e0"
        st.markdown(f'<div style="display: flex; justify-content: space-between; margin-bottom: 15px;"><div style="background:{b1}; color:white; padding:5px; border-radius:5px; width:32%; text-align:center; font-size:0.7em;">10-19 ik</div><div style="background:{b2}; color:white; padding:5px; border-radius:5px; width:32%; text-align:center; font-size:0.7em;">20-29 ik</div><div style="background:{b3}; color:white; padding:5px; border-radius:5px; width:32%; text-align:center; font-size:0.7em;">+29 ik</div></div>', unsafe_allow_html=True)

        presupuesto_total = 0
        lineas_desglose = []
        for titulo, num in alumnos_por_programa.items():
            if num > 0:
                cat = info_programak[titulo]['cat']
                precio = (13.70 if tier == 3 else 14.70 if tier == 2 else 15.70) if cat == "yoko" else (19.00 if tier == 3 else 20.00 if tier == 2 else 21.00) if cat == "2c" else (21.00 if tier == 3 else 22.00 if tier == 2 else 23.00)
                subtotal = num * precio
                presupuesto_total += subtotal
                lineas_desglose.append(f"{num} ikasle - {titulo}: {subtotal:.2f} EUR")

        precio_medio = presupuesto_total / total_alumnos
        st.metric("Guztira / Total", f"{presupuesto_total:.2f} €")
        st.metric("Ikasleko / Por alumno", f"{precio_medio:.2f} €")
        
        datos_ok = nombre_escuela != "" and es_email_valido(email_escuela) and es_telefono_valido(telefono_escuela)
        
        if st.button("Aurrekontua Sortu / Generar", type="primary", disabled=not datos_ok):
            st.balloons()
            pdf_data = generar_pdf_pro(nombre_escuela, telefono_escuela, email_escuela, presupuesto_total, total_alumnos, precio_medio, lineas_desglose, total_alumnos // 10)
            st.download_button("📥 Deskargatu PDF Profesionala", data=pdf_data, file_name=f"Aurrekontua_{nombre_escuela}.pdf", mime="application/pdf")
            
            asunto = urllib.parse.quote(f"Reserva: {nombre_escuela}")
            cuerpo = urllib.parse.quote(f"Ikastetxea: {nombre_escuela}\nTotal: {presupuesto_total:.2f}€")
            st.markdown(f'<center><a href="mailto:ikerlarrap@gmail.com?subject={asunto}&body={cuerpo}" target="_blank"><button style="background:#4CAF50; color:white; border:none; padding:10px; border-radius:5px; cursor:pointer;">📧 Bidali eskaera orain</button></a></center>', unsafe_allow_html=True)
    else:
        st.info("👈 Gehitu ikasleak")

st.divider()
st.caption("Mendexa Abentura Park | 688 85 62 83")
