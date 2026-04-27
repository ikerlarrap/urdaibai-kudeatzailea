import streamlit as st
import urllib.parse
import re

# --- CONFIGURACION DE PAGINA ---
st.set_page_config(page_title="Mendexa Abentura Park Planner", layout="wide")

# --- FUNCIONES DE VALIDACION ---
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

# --- 2. TITULOS ---
st.title("Mendexa Abentura Park: Ikastetxeentzat Aurrekontu Kalkulagailua 🌲🌲🧗")
st.subheader("Kalkulatu zure aurrekontua momentuan / Calcula tu presupuesto al instante")

# --- 3. DATOS DE LA ESCUELA ---
st.markdown("### 🏫 Ikastetxearen Datuak / Datos de la Escuela")

# Datu derrigorrezkoak
col_esc1, col_esc2, col_esc3 = st.columns(3)
with col_esc1:
    nombre_escuela = st.text_input("Ikastetxearen izena / Nombre del centro escolar*")
with col_esc2:
    telefono_escuela = st.text_input("Telefonoa / Teléfono*")
    if telefono_escuela and not es_telefono_valido(telefono_escuela):
        st.caption("⚠️ Sartu gutxienez 9 zenbaki / Mínimo 9 números")
with col_esc3:
    email_escuela = st.text_input("Posta elektronikoa / Email*")
    if email_escuela and not es_email_valido(email_escuela):
        st.caption("⚠️ Email okerra / Email no válido")

# Datu aukerakoak (Opcionales)
col_opt1, col_opt2, col_opt3 = st.columns(3)
with col_opt1:
    cif_escuela = st.text_input("CIF (Aukerakoa / Opcional)")
with col_opt2:
    direccion_escuela = st.text_input("Helbidea / Dirección (Aukerakoa / Opcional)")
with col_opt3:
    provincia_escuela = st.text_input("Probintzia / Provincia (Aukerakoa / Opcional)")

st.divider()

# --- 4. SELECCION DE ACTIVIDADES ---
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
    
    # Oharra: Demo eta Laranja zirkuituak
    st.info("ℹ️ **GARRANTZITSUA / IMPORTANTE:**\nZirkuitu guztiek **Demo** eta **Laranja** zirkuituak barne hartzen dituzte hasieran, beti egiten dira lehenengo. / Todos los programas incluyen los circuitos **Demo** y **Naranja** al inicio, siempre se realizan primero.")

    # Descripciones mejoradas sin los círculos morado y naranja
    info_programak = {
        "🟡 1 ZIRKUITUA: YOKO SOILIK (Adina / Edad: 4-8 urte)": {
            "id": "yoko", "cat": "yoko", 
            "desc": "3 itzuli YOKO zirkuituan (Guztira 5 zirkuitu).\n\n📏 Altuera / Altura min.: > 1,10m"
        },
        "🟢 🟢 2 ZIRKUITU (Adina / Edad: >9 urte)": {
            "id": "2c_9", "cat": "2c", 
            "desc": "2 itzuli zirkuitu BERDEETAN (Guztira 4 zirkuitu).\n\n📏 Altuera / Altura min.: > 1,40m"
        },
        "🟢 🔵 2 ZIRKUITU (Adina / Edad: >12 urte)": {
            "id": "2c_12", "cat": "2c", 
            "desc": "Zirkuitu BERDEA + URDINA (Guztira 4 zirkuitu).\n\n📏 Altuera / Altura min.: > 1,50m"
        },
        "🟢 🔵 🔵 3 ZIRKUITU (Adina / Edad: 12-14 urte)": {
            "id": "3c_12", "cat": "3c", 
            "desc": "Zirkuitu BERDEA + 2 itzuli URDINEAN (Guztira 5 zirkuitu).\n\n📏 Altuera / Altura min.: > 1,50m"
        },
        "🟢 🔵 🔴 3 ZIRKUITU (Adina / Edad: >15 urte)": {
            "id": "3c_15", "cat": "3c", 
            "desc": "Zirkuitu BERDEA + URDINA + GORRIA (Guztira 5 zirkuitu).\n\n📏 Altuera / Altura min.: > 1,50m"
        }
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

    # --- INFORMACIÓN DEL DOSSIER ACTUALIZADA ---
    st.markdown("### ℹ️ Informazio Garrantzitsua / Información Importante")
    with st.expander("Irakurri baldintzak / Leer condiciones del dossier", expanded=False):
        col_inf1, col_inf2 = st.columns(2)
        with col_inf1:
            st.markdown("""
            **🎒 Zer ekarri:**
            * Kirol-arropa erosoa.
            * Kirol-oinetako itxiak (sandaliak debekatuta).
            * Ile luzea jasota eraman behar da.
            * Poltsikoak hutsik jardueran zehar.
            
            <br>
            
            **📏 Altuerak / Alturas mínimas:**
            * Yoko zirkuitua: > 1,10 m
            * Zirkuitu Berdea: > 1,40 m
            * Zirkuitu Urdina/Gorria: > 1,50 m
            """, unsafe_allow_html=True)
        with col_inf2:
            st.markdown("""
            **🌦️ Eguraldia eta Ordutegia:**
            * Euriarekin jarduera egin daiteke.
            * Segurtasunagatik (ekaitza/haizea) parkeak jarduera bertan behera utzi dezake.
            * 15 minutu lehenago heltzea gomendatzen da.
            """)

    with st.expander("ℹ️ Zer dago barne? / ¿Qué incluye?"):
        st.markdown("* Monitoreak, aseguruak eta materiala barne. Arropa erosoa eta oinetako itxiak beharrezkoak dira.")

# --- 5. RESULTADOS ---
with col_result:
    st.markdown("### 💰 Aurrekontu Laburpena / Resumen")
    
    if total_alumnos == 0:
        st.info("👈 Gehitu ikasleak ezkerrean.")
    else:
        tier = 3 if total_alumnos > 29 else 2 if total_alumnos >= 20 else 1

        # --- SEMAFORO ---
        b1 = "#4CAF50" if tier == 1 else "#e0e0e0"
        b2 = "#4CAF50" if tier == 2 else "#e0e0e0"
        b3 = "#4CAF50" if tier == 3 else "#e0e0e0"
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; margin-bottom: 15px; font-family: sans-serif;">
            <div style="background-color: {b1}; color: white; padding: 8px 5px; border-radius: 5px; font-size: 0.85em; text-align: center; width: 32%; font-weight: bold;">
                10-19 ikasle<br><small style="font-weight: normal;">Tarifa Normala</small>
            </div>
            <div style="background-color: {b2}; color: white; padding: 8px 5px; border-radius: 5px; font-size: 0.85em; text-align: center; width: 32%; font-weight: bold;">
                20-29 ikasle<br><small style="font-weight: normal;">-1€ Deskontua</small>
            </div>
            <div style="background-color: {b3}; color: white; padding: 8px 5px; border-radius: 5px; font-size: 0.85em; text-align: center; width: 32%; font-weight: bold;">
                +29 ikasle<br><small style="font-weight: normal;">-2€ Deskontua</small>
            </div>
        </div>
        """, unsafe_allow_html=True)

        presupuesto_total = 0
        listado_resumen_html = ""
        
        # Bloque de información extra para descargar TXT
        info_txt_opcional = ""
        if cif_escuela: info_txt_opcional += f"CIF: {cif_escuela}\n"
        if direccion_escuela: info_txt_opcional += f"Helbidea/Dirección: {direccion_escuela}\n"
        if provincia_escuela: info_txt_opcional += f"Probintzia/Provincia: {provincia_escuela}\n"

        texto_descarga = f"MENDEXA ABENTURA PARK - AURREKONTUA\nEskola: {nombre_escuela}\n{info_txt_opcional}"
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
                
                listado_resumen_html += f"<div style='margin-bottom: 8px; border-left: 4px solid #2E7D32; padding-left: 10px;'><strong>{num} ikasle</strong> - {titulo.split(' (')[0]}<br><span style='color: #2E7D32;'>{precio:.2f}€ x {num} = {subtotal:.2f}€</span></div>"
                texto_descarga += f"- {num} ikasle - {titulo.split(' (')[0]}: {subtotal:.2f}€\n"

        precio_medio = presupuesto_total / total_alumnos
        st.metric("Guztira / Total", f"{presupuesto_total:.2f} €")
        st.metric("Ikasleko / Por alumno", f"{precio_medio:.2f} €")
        st.write(f"👥 Ikasleak: {total_alumnos} | 🎁 Doako plaza: {total_alumnos // 10}")
        st.caption("Prezio guztiek %10eko BEZa barne hartzen dute / Todos los precios incluyen el 10% de IVA.")
        
        # Bloqueo de botón sigue dependiendo solo de los datos obligatorios
        datos_listos = nombre_escuela != "" and es_email_valido(email_escuela) and es_telefono_valido(telefono_escuela)

        st.divider()
        if st.button("Aurrekontua Sortu / Generar", type="primary", disabled=not datos_listos):
            # Globos eliminados
            
            # Formatear la información extra para la visualización del Ticket HTML
            info_html_opcional = ""
            if cif_escuela: info_html_opcional += f"<strong>CIF:</strong> {cif_escuela}<br>"
            if direccion_escuela: info_html_opcional += f"<strong>Helbidea/Dirección:</strong> {direccion_escuela}<br>"
            if provincia_escuela: info_html_opcional += f"<strong>Probintzia/Provincia:</strong> {provincia_escuela}<br>"

            st.markdown(f"""
            <div style="border: 5px solid #2E7D32; border-radius: 15px; padding: 25px; background-color: #fcfcfc; color: black; font-family: sans-serif;">
                <h2 style="color: #2E7D32; text-align: center; margin-top: 0;">🌲 MENDEXA ABENTURA PARK 🌲</h2>
                <p><strong>Ikastetxea:</strong> {nombre_escuela}<br>{info_html_opcional}<strong>Taldea:</strong> {total_alumnos} ikasle</p>
                <div style="background: #f0f0f0; padding: 15px; border-radius: 10px; margin: 15px 0;">{listado_resumen_html}</div>
                <div style="text-align: right; border-top: 2px solid #2E7D32; padding-top: 15px;">
                    <span style="font-size: 1.1em; color: #666;">Ikasleko (batez beste): {precio_medio:.2f} €</span><br>
                    <span style="font-size: 1.4em; color: #444; font-weight: bold;">GUZTIRA: {presupuesto_total:.2f} €</span><br>
                    <small style="color: #888;">BEZ barne (%10) / IVA incluido (%10)</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            texto_descarga += f"\nTOTALA: {presupuesto_total:.2f}€ (BEZ barne)\nIkasleko: {precio_medio:.2f}€"
            st.download_button("📩 Deskargatu aurrekontua (TXT)", data=texto_descarga, file_name=f"Aurrekontua_{nombre_escuela.replace(' ', '_')}.txt")

            asunto = urllib.parse.quote(f"Reserva: {nombre_escuela}")
            cuerpo = urllib.parse.quote(f"Ikastetxea: {nombre_escuela}\nTotal: {presupuesto_total:.2f}€")
            mailto_link = f"mailto:ikerlarrap@gmail.com?subject={asunto}&body={cuerpo}"
            st.markdown(f'<center><a href="{mailto_link}" target="_blank"><button style="background-color:#4CAF50; color:white; border:none; padding:12px; border-radius:8px; cursor:pointer; font-weight:bold;">📧 Bidali eskaera orain</button></a></center>', unsafe_allow_html=True)

st.divider()
st.caption("Mendexa Abentura Park | 688 85 62 83")
