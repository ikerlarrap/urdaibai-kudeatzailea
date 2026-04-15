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

st.title("Mendexa Abentura Park: Eskolentzako Kalkulagailua 🌲🌲🧗")
st.subheader("Kalkulatu zure aurrekontua momentuan / Calcula tu presupuesto al instante")

# --- 2. DATOS ESCUELA ---
st.markdown("### 🏫 Ikastetxearen Datuak")
c1, c2, c3 = st.columns(3)
with c1: nombre_escuela = st.text_input("Ikastetxearen izena")
with c2: telefono_escuela = st.text_input("Telefonoa")
with c3: email_escuela = st.text_input("Posta elektronikoa")

st.divider()

col_in, col_res = st.columns([1.4, 1])

with col_in:
    st.markdown("### 📝 Aukeratu zure jarduera-paketea / Elige tu paquete")
    with st.expander("💶 Prezioen Taula"):
        st.markdown("| Programa | 10-19 ik | 20-29 ik | +29 ik |\n| :--- | :---: | :---: | :---: |\n| YOKO | 15,70€ | 14,70€ | 13,70€ |\n| 2 ZIRK | 21,00€ | 20,00€ | 19,00€ |\n| 3 ZIRK | 23,00€ | 22,00€ | 21,00€ |")

    info_programak = {
        "🟣 🟠 🟡 1 ZIRKUITUA: YOKO SOILIK": {"id": "yoko", "cat": "yoko", "h": "4-8 urte"},
        "🟣 🟠 🟢 🟢 2 ZIRKUITU (9 urte +)": {"id": "2c_9", "cat": "2c", "h": ">9 urte"},
        "🟣 🟠 🟢 🔵 2 ZIRKUITU (12 urte +)": {"id": "2c_12", "cat": "2c", "h": ">12 urte"},
        "🟣 🟠 🟢 🔵 🔵 3 ZIRKUITU (12-14 urte)": {"id": "3c_12", "cat": "3c", "h": "12-14 urte"},
        "🟣 🟠 🟢 🔵 🔴 3 ZIRKUITU (15 urte +)": {"id": "3c_15", "cat": "3c", "h": ">15 urte"}
    }

    alumnos_por_prog = {}
    total_alumnos = 0
    for tit, info in info_programak.items():
        ca, cb, cc = st.columns([0.1, 4, 1.5])
        with cb: st.markdown(f"**{tit}**", help=info['h'])
        with cc:
            n = st.number_input("Kop", min_value=0, step=1, key=info['id'], label_visibility="collapsed")
            alumnos_por_prog[tit] = n
            total_alumnos += n

with col_result:
    st.markdown("### 💰 Aurrekontua")
    if total_alumnos > 0:
        tier = 3 if total_alumnos > 29 else 2 if total_alumnos >= 20 else 1
        
        # Semaforo visual
        s1 = "#4CAF50" if tier == 1 else "#e0e0e0"
        s2 = "#4CAF50" if tier == 2 else "#e0e0e0"
        s3 = "#4CAF50" if tier == 3 else "#e0e0e0"
        st.markdown(f'<div style="display: flex; justify-content: space-between; margin-bottom: 15px;"><div style="background:{s1}; color:white; padding:5px; border-radius:5px; width:32%; text-align:center; font-size:0.7em; font-weight:bold;">10-19 ik</div><div style="background:{s2}; color:white; padding:5px; border-radius:5px; width:32%; text-align:center; font-size:0.7em;">20-29 ik</div><div style="background:{s3}; color:white; padding:5px; border-radius:5px; width:32%; text-align:center; font-size:0.7em;">+29 ik</div></div>', unsafe_allow_html=True)

        total_euro = 0
        listado_html = ""
        for tit, n in alumnos_por_prog.items():
            if n > 0:
                cat = info_programak[tit]['cat']
                p = (13.7 if tier==3 else 14.7 if tier==2 else 15.7) if cat=="yoko" else (19 if tier==3 else 20 if tier==2 else 21) if cat=="2c" else (21 if tier==3 else 22 if tier==2 else 23)
                total_euro += n * p
                listado_html += f"<li>{n} ikasle - {tit}: <b>{n*p:.2f} €</b></li>"

        precio_al = total_euro / total_alumnos
        st.metric("Guztira / Total", f"{total_euro:.2f} €")
        st.metric("Ikasleko / Por alumno", f"{precio_al:.2f} €")
        
        st.write(f"👥 Ikasleak: {total_alumnos} | 🎁 Doako plaza: {total_alumnos // 10}")
        
        datos_ok = nombre_escuela != "" and es_email_valido(email_escuela) and es_telefono_valido(telefono_escuela)
        
        st.divider()
        if st.button("Aurrekontua Sortu / Generar", type="primary", disabled=not datos_ok):
            st.balloons()
            
            # TICKET VISUAL EN APP
            resguardo_html = f"""
            <div style="border: 4px solid #2E7D32; border-radius: 10px; padding: 20px; background: #f9f9f9; color: black;">
                <h2 style="text-align: center; color: #2E7D32;">🌲 MENDEXA ABENTURA PARK</h2>
                <p><b>Ikastetxea:</b> {nombre_escuela}</p>
                <ul>{listado_html}</ul>
                <h3 style="text-align: right; border-top: 1px solid #ccc; padding-top: 10px;">GUZTIRA: {total_euro:.2f} €</h3>
            </div>
            """
            st.markdown(resguardo_html, unsafe_allow_html=True)
            
            # BOTÓN DE DESCARGA (HTML PROFESIONAL)
            html_descarga = f"<html><body style='font-family: Arial; padding: 40px;'><h1 style='color: #2E7D32;'>MENDEXA ABENTURA PARK</h1><h2>Aurrekontua / Presupuesto</h2><hr><p><b>Ikastetxea:</b> {nombre_escuela}</p><p><b>Telefonoa:</b> {telefono_escuela}</p><ul>{listado_html}</ul><h2 style='text-align: right;'>TOTALA: {total_euro:.2f} EUR</h2><p style='font-size: 0.8em; color: gray;'>BEZ barne. Mendexa, 2026.</p></body></html>"
            
            st.download_button("📥 Deskargatu Aurrekontua (Fitxategia)", data=html_descarga, file_name=f"Presupuesto_{nombre_escuela}.html", mime="text/html")
            
            # BOTÓN EMAIL
            asunto = urllib.parse.quote(f"Reserva: {nombre_escuela}")
            cuerpo = urllib.parse.quote(f"Ikastetxea: {nombre_escuela}\nTotal: {total_euro:.2f}€")
            st.markdown(f'<br><center><a href="mailto:ikerlarrap@gmail.com?subject={asunto}&body={cuerpo}" target="_blank"><button style="background:#4CAF50; color:white; border:none; padding:15px; border-radius:8px; cursor:pointer; font-weight:bold;">📧 Bidali eskaera orain</button></a></center>', unsafe_allow_html=True)
    else:
        st.info("👈 Gehitu ikasleak aurrekontua ikusteko.")

st.divider()
st.caption("Mendexa Abentura Park | 688 85 62 83")
