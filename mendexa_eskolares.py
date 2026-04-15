import streamlit as st
import urllib.parse
import re

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Mendexa Abentura Park Planner", layout="wide")

# --- FUNCIONES DE VALIDACIÓN ---
def es_email_valido(email):
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email) is not None

def es_telefono_valido(tel):
    return len(tel) >= 9 and tel.isdigit()

# --- 1. LOGO ---
try:
    st.image("logo_mendexa.png", width=250)
except:
    st.markdown("🌲 **MENDEXA ABENTURA PARK**")

# --- 2. TÍTULOS ---
st.title("Mendexa Abentura Park: Kalkulagailua 🌲")
st.subheader("Eskolentzako Aurrekontua / Presupuesto Escolar")

# --- 3. DATOS DE LA ESCUELA ---
st.markdown("### 🏫 Ikastetxearen Datuak")
c1, c2, c3 = st.columns(3)
with c1:
    nombre_escuela = st.text_input("Ikastetxearen izena / Nombre del colegio")
with c2:
    telefono_escuela = st.text_input("Telefonoa / Teléfono")
with c3:
    email_escuela = st.text_input("Posta elektronikoa / Email")

st.divider()

# --- 4. SELECCIÓN DE ACTIVIDADES ---
col_in, col_res = st.columns([1.3, 1])

with col_in:
    st.markdown("### 📝 Aukeratu zure jarduera-paketea")
    
    info_programak = {
        "🟣 🟠 🟡 1 ZIRKUITUA: YOKO": {"id": "yoko", "cat": "yoko", "p": [15.7, 14.7, 13.7]},
        "🟣 🟠 🟢 🟢 2 ZIRKUITU (9+)": {"id": "2c_9", "cat": "2c", "p": [21.0, 20.0, 19.0]},
        "🟣 🟠 🟢 🔵 2 ZIRKUITU (12+)": {"id": "2c_12", "cat": "2c", "p": [21.0, 20.0, 19.0]},
        "🟣 🟠 🟢 🔵 🔵 3 ZIRKUITU (12-14)": {"id": "3c_12", "cat": "3c", "p": [23.0, 22.0, 21.0]},
        "🟣 🟠 🟢 🔵 🔴 3 ZIRKUITU (15+)": {"id": "3c_15", "cat": "3c", "p": [23.0, 22.0, 21.0]}
    }

    alumnos_prog = {}
    total_alumnos = 0

    for tit, info in info_programak.items():
        row_c1, row_c2 = st.columns([3, 1])
        with row_c1:
            st.write(tit)
        with row_c2:
            n = st.number_input("Kop", min_value=0, step=1, key=info['id'], label_visibility="collapsed")
            alumnos_prog[tit] = n
            total_alumnos += n

with col_res:
    st.markdown("### 💰 Resumen")
    if total_alumnos > 0:
        # Lógica de tramos
        tier_idx = 2 if total_alumnos > 29 else 1 if total_alumnos >= 20 else 0
        tramos = ["10-19 ikasle", "20-29 ikasle", "+29 ikasle"]
        st.info(f"Tarifa aplikatua: **{tramos[tier_idx]}**")

        total_final = 0
        desglose_texto = ""
        for tit, n in alumnos_prog.items():
            if n > 0:
                p = info_programak[tit]['p'][tier_idx]
                sub = n * p
                total_final += sub
                desglose_texto += f"- {n} ikasle: {tit} ({p:.2f}€/u) = {sub:.2f}€\n"

        precio_medio = total_final / total_alumnos
        
        st.metric("GUZTIRA / TOTAL", f"{total_final:.2f} €")
        st.metric("Ikasleko / Por alumno", f"{precio_medio:.2f} €")
        
        # Validación de datos para activar botón
        datos_completos = nombre_escuela != "" and es_email_valido(email_escuela) and es_telefono_valido(telefono_escuela)
        
        if not datos_completos:
            st.warning("⚠️ Bete ikastetxearen datu guztiak aurrekontua sortzeko.")

        st.divider()
        if st.button("AURREKONTUA SORTU / GENERAR", type="primary", disabled=not datos_completos):
            st.balloons()
            
            # TICKET USANDO COMPONENTES NATIVOS (SIN HTML QUE SE ROMPA)
            st.success(f"Aurrekontua prest: {nombre_escuela}")
            
            ticket_texto = f"""
🌲 MENDEXA ABENTURA PARK 🌲
----------------------------
Ikastetxea: {nombre_escuela}
Telefonoa: {telefono_escuela}
Ikasleak: {total_alumnos}
----------------------------
DETALLE:
{desglose_texto}
----------------------------
GUZTIRA: {total_final:.2f} EUR
Ikasleko: {precio_medio:.2f} EUR
----------------------------
            """
            st.code(ticket_texto)
            
            # Descarga TXT
            st.download_button("📩 Deskargatu Aurrekontua (TXT)", data=ticket_texto, file_name=f"Aurrekontua_{nombre_escuela}.txt")
            
            # Botón de email (Link directo)
            asunto = urllib.parse.quote(f"Reserva: {nombre_escuela}")
            cuerpo = urllib.parse.quote(f"Ikastetxea: {nombre_escuela}\nTotal: {total_final:.2f}€")
            st.markdown(f"[📧 **BIDALI ESKAERA POSTA BIDEZ / ENVIAR POR EMAIL**](mailto:ikerlarrap@gmail.com?subject={asunto}&body={cuerpo})")
    else:
        st.info("👈 Gehitu ikasleak aurrekontua kalkulatzeko.")

st.divider()
st.caption("Mendexa Abentura Park | 688 85 62 83")
