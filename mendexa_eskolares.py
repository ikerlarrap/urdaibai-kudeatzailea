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
st.markdown("### 🏫 Ikastetxearen Datuak / Datos de la Escuela")
c1, c2, c3 = st.columns(3)
with c1: nombre_escuela = st.text_input("Ikastetxearen izena / Nombre del colegio")
with c2: telefono_escuela = st.text_input("Telefonoa / Teléfono")
with c3: email_escuela = st.text_input("Posta elektronikoa / Email")

# Avisos de validación
if telefono_escuela and not es_telefono_valido(telefono_escuela):
    st.caption("⚠️ Telefonoa: gutxienez 9 zenbaki / Mínimo 9 números")
if email_escuela and not es_email_valido(email_escuela):
    st.caption("⚠️ Email okerra / Email no válido")

st.divider()

# --- 3. SELECCIÓN DE ACTIVIDADES ---
col_in, col_res = st.columns([1.4, 1])

with col_in:
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

# --- 4. RESULTADOS ---
with col_res:
    st.markdown("### 💰 Aurrekontu Laburpena / Resumen")
    if total_alumnos > 0:
        tier = 3 if total_alumnos > 29 else 2 if total_alumnos >= 20 else 1
        
        # Semáforo visual
        colores = ["#4CAF50" if tier == i else "#e0e0e0" for i in range(1, 4)]
        st.markdown(f'<div style="display: flex; justify-content: space-between; margin-bottom: 15px;"><div style="background:{colores[0]}; color:white; padding:5px; border-radius:5px; width:32%; text-align:center; font-size:0.75em; font-weight:bold;">10-19 ik</div><div style="background:{colores[1]}; color:white; padding:5px; border-radius:5px; width:32%; text-align:center; font-size:0.75em; font-weight:bold;">20-29 ik</div><div style="background:{colores[2]}; color:white; padding:5px; border-radius:5px; width:32%; text-align:center; font-size:0.75em; font-weight:bold;">+29 ik</div></div>', unsafe_allow_html=True)

        total_euros = 0
        listado_visual = ""
        texto_descarga = "MENDEXA ABENTURA PARK - AURREKONTUA\n"
        texto_descarga += f"Ikastetxea: {nombre_escuela}\n" + "-"*30 + "\n"

        for tit, n in alumnos_por_prog.items():
            if n > 0:
                cat = info_programak[tit]['cat']
                p = (13.7 if tier==3 else 14.7 if tier==2 else 15.7) if cat=="yoko" else (19 if tier==3 else 20 if tier==2 else 21) if cat=="2c" else (21 if tier==3 else 22 if tier==2 else 23)
                subtotal = n * p
                total_euros += subtotal
                listado_visual += f"<li>{n} ikasle - {tit}: <b>{subtotal:.2f} €</b></li>"
                texto_descarga += f"- {n} ikasle - {tit}: {subtotal:.2f}€\n"

        precio_medio = total_euros / total_alumnos
        st.metric("Guztira / Total", f"{total_euros:.2f} €")
        st.metric("Ikasleko / Por alumno", f"{precio_medio:.2f} €")
        st.write(f"👥 Ikasleak: {total_alumnos} | 🎁 Doako plaza: {total_alumnos // 10}")
        
        datos_completos = nombre_escuela != "" and es_email_valido(email_escuela) and es_telefono_valido(telefono_escuela)
        
        st.divider()
        if st.button("Aurrekontua Sortu / Generar", type="primary", disabled=not datos_completos):
            st.balloons()
            st.markdown(f"""
            <div style="border: 3px solid #2E7D32; border-radius: 10px; padding: 15px; background: #f9f9f9; color: black;">
                <h4 style="margin-top:0; color:#2E7D32;">Resguardo / Erreserba</h4>
                <ul>{listado_visual}</ul>
                <h3 style="text-align:right;">Guztira: {total_euros:.2f} €</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Descarga TXT
            texto_descarga += f"\nTOTALA: {total_euros:.2f}€\nBatez besteko prezioa: {precio_medio:.2f}€/ikasle"
            st.download_button("📩 Deskargatu aurrekontua (TXT)", data=texto_descarga, file_name=f"Aurrekontua_{nombre_escuela}.txt")
            
            # Mailto
            asunto = urllib.parse.quote(f"Reserva: {nombre_escuela}")
            cuerpo = urllib.parse.quote(f"Ikastetxea: {nombre_escuela}\nTotal: {total_euros:.2f}€")
            st.markdown(f'<br><center><a href="mailto:ikerlarrap@gmail.com?subject={asunto}&body={cuerpo}" target="_blank"><button style="background:#4CAF50; color:white; border:none; padding:12px; border-radius:8px; cursor:pointer; font-weight:bold;">📧 Bidali eskaera orain</button></a></center>', unsafe_allow_html=True)
    else:
        st.info("👈 Gehitu ikasleak aurrekontua sortzeko.")

st.divider()
st.caption("Mendexa Abentura Park | 688 85 62 83")
