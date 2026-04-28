import streamlit as st
import urllib.parse
import re

# --- CONFIGURACION DE PAGINA ---
st.set_page_config(page_title="Mendexa Abentura Park - Eskolak", layout="wide", initial_sidebar_state="expanded")

# --- CSS PARA TEXTO MÁS GRANDE Y ESPACIADO DEL MENÚ ---
st.markdown("""
<style>
    /* Aumentar el tamaño del texto general */
    body, p, li, div, span, label {
        font-size: 1.15rem !important;
    }
    .stRadio label {
        font-size: 1.2rem !important;
        font-weight: bold !important;
    }
    /* Estilo para forzar saltos de línea en los labels del radio button */
    .stRadio div[role="radiogroup"] > label > div:first-child {
        white-space: pre-wrap;
        line-height: 1.4;
    }
</style>
""", unsafe_allow_html=True)

# --- FUNCIONES DE VALIDACION ---
def es_email_valido(email):
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(patron, email.strip()) is not None

def es_telefono_valido(tel):
    tel_limpio = tel.replace(" ", "").replace("-", "").replace("+", "")
    return len(tel_limpio) >= 9 and tel_limpio.isdigit()

# --- MENU LATERAL (SIDEBAR) ---
with st.sidebar:
    st.image("https://mendexapark.com/wp-content/uploads/2017/09/logo-mendexa.park_.png", width=220)
    st.write("")
    menu = st.radio(
        "📍 Nabigazioa / Navegación",
        [
            "🌲 1. Parkea \n\n El Parque", 
            "🧗 2. Zirkuituak \n\n Circuitos", 
            "🛡️ 3. Segurtasuna \n\n Seguridad", 
            "💶 4. Aurrekontua \n\n Calculadora"
        ]
    )
    st.divider()
    st.caption("📍 Leagi Auzoa, 48289 Mendexa")
    st.caption("📞 688 85 62 83")
    st.caption("✉️ info@mendexapark.com")

# --- CABECERA PRINCIPAL ---
st.markdown("<h2 style='text-align:center; color:#2E7D32; margin-top:-20px;'>Ikastetxeentzat Dossier Interaktiboa / Dossier Escolar Interactivo</h2>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align:center; color:#555;'>Aisialdia eta Abentura ezagutza eta ikaskuntzarekin bat datoz <br> <i>El ocio y la aventura no están reñidos con el conocimiento y el aprendizaje</i></h5>", unsafe_allow_html=True)
st.divider()

# ==========================================
# 1. EL PARQUE (INSTALACIONES + MAPA)
# ==========================================
if menu == "🌲 1. Parkea \n\n El Parque":
    col_img1, col_img2, col_img3 = st.columns([1, 3, 1])
    with col_img2:
        st.image("https://mendexapark.com/wp-content/uploads/2018/02/grupos-escolares-mendexa-park-parque-tirolinas-aventura-01.jpg", use_container_width=True)
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown("### 📍 Non gaude / Dónde estamos")
        st.write("**Euskal Kostaldean zuhaitz abentura parkea / Parque de aventura en la Costa Vasca.**")
        st.write("Mendexan (Bizkaia) kokatua, Lekeitiotik 4 kilometrora eta erraz iristeko modukoa ikastetxeentzat. / Situado en Mendexa (Bizkaia), a 4 Km. de Lekeitio. Fácilmente accesible para todos los centros escolares.")
        st.info("🚌 **Autobusa / Autobús:** Aparkalekua daukagu, autobusentzat prestatutako gunearekin. / Aparcamiento propio con una zona habilitada para autobuses.")
        
    with col_p2:
        st.markdown("### 🏡 Instalazioak / Instalaciones")
        st.write("✓ **Harrera / Recepción:** Bezeroarentzako arreta bulegoa / Oficina de atención al cliente.")
        st.write("✓ **Gordelekua / Consigna:** Motxilak eta elementu pertsonalak gordetzeko lekua / Espacio para guardar mochilas y elementos personales.")
        st.write("✓ **Komunak / Baños:** Gizonezkoen eta emakumezkoen komunak / Baños masculinos y femeninos.")
        st.write("✓ **Piknik Gunea / Merendero:** Mahaiekin prestatutako gunea norbere bazkariarekin erabiltzeko / Zona preparada con mesas tipo merendero que se puede utilizar con comida propia.")
        
    st.divider()
    st.markdown("### 🗺️ Parkeko Mapa / Mapa del Parque")
    col_map1, col_map2, col_map3 = st.columns([1, 4, 1])
    with col_map2:
        st.image("https://mendexapark.com/wp-content/uploads/2022/02/mendexa-plano-finla-Calidad-AltaCASTELLANO.jpg", use_container_width=True)

# ==========================================
# 2. LOS CIRCUITOS (ALINEADOS + GALERÍA FINAL)
# ==========================================
elif menu == "🧗 2. Zirkuituak \n\n Circuitos":
    st.markdown("### 🧗 Zirkuituak / Circuitos")
    st.write("78 erronkatik gora eta 23 tirolinadun zirkuituri aurre egingo diezu. / Con más de 78 retos y 23 tirolinas en los árboles, en circuitos de diferente dificultad.")
    st.write("")
    
    # Fila 1 de circuitos
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div style='background-color:#FCE4EC; padding:20px; border-radius:10px; border-left: 5px solid #E91E63; min-height: 280px;'>
        <h4 style='color:#C2185B; margin-top:0;'>🌸 DEMO</h4>
        <b>Adina/Edad:</b> Guztiak / Todos<br>
        <b>Altuera/Altura min.:</b> > 1,30m<br>
        <b>Erronkak/Retos:</b> 5 | <b>Tirolinak:</b> 2<br><br>
        Ezagutza zirkuitua. Partehartzaile guztiak igaro behar dira.<br>
        <i>Circuito inicial por el que todos deben pasar antes de comenzar.</i>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div style='background-color:#FFF59D; padding:20px; border-radius:10px; border-left: 5px solid #FBC02D; min-height: 280px;'>
        <h4 style='color:#F57F17; margin-top:0;'>🟡 YOKO</h4>
        <b>Adina/Edad:</b> 4-8 urte/años<br>
        <b>Altuera/Altura min.:</b> > 1,10m<br>
        <b>Erronkak/Retos:</b> 15 | <b>Tirolinak:</b> 3<br><br>
        Gazte abenturazaleen zirkuitua. 3 itzuli YOKO zirkuituan.<br>
        <i>Circuito para jóvenes aventureros. 3 vueltas en Yoko.</i>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div style='background-color:#FFE0B2; padding:20px; border-radius:10px; border-left: 5px solid #FF9800; min-height: 280px;'>
        <h4 style='color:#E65100; margin-top:0;'>🟠 LARANJA / NARANJA</h4>
        <b>Adina/Edad:</b> > 4 urte/años<br>
        <b>Altuera/Altura min.:</b> > 1,20m<br>
        <b>Erronkak/Retos:</b> 5 | <b>Tirolinak:</b> 2<br><br>
        Yoko ondorengo pausoa, familia osoarentzat.<br>
        <i>Un paso más para los jóvenes aventureros.</i>
        </div>
        """, unsafe_allow_html=True)

    st.write("") # Espaciador

    # Fila 2 de circuitos
    c4, c5, c6 = st.columns(3)
    with c4:
        st.markdown("""
        <div style='background-color:#C8E6C9; padding:20px; border-radius:10px; border-left: 5px solid #4CAF50; min-height: 280px;'>
        <h4 style='color:#2E7D32; margin-top:0;'>🟢 BERDEA / VERDE</h4>
        <b>Adina/Edad:</b> > 9 urte/años<br>
        <b>Altuera/Altura min.:</b> > 1,40m<br>
        <b>Erronkak/Retos:</b> 15 | <b>Tirolinak:</b> 5<br><br>
        Aurkikuntza zirkuitua. 2 itzuli zirkuitu BERDEETAN.<br>
        <i>Circuito de descubrimiento. 2 vueltas en circuitos VERDES.</i>
        </div>
        """, unsafe_allow_html=True)
    with c5:
        st.markdown("""
        <div style='background-color:#BBDEFB; padding:20px; border-radius:10px; border-left: 5px solid #2196F3; min-height: 280px;'>
        <h4 style='color:#1565C0; margin-top:0;'>🔵 URDINA / AZUL</h4>
        <b>Adina/Edad:</b> > 12 urte/años<br>
        <b>Altuera/Altura min.:</b> > 1,50m<br>
        <b>Erronkak/Retos:</b> 17 | <b>Tirolinak:</b> 6<br><br>
        Sentsazioen zirkuitua. Zirkuitu BERDEA + URDINA.<br>
        <i>Circuito de sensaciones. VERDE + AZUL.</i>
        </div>
        """, unsafe_allow_html=True)
    with c6:
        st.markdown("""
        <div style='background-color:#FFCDD2; padding:20px; border-radius:10px; border-left: 5px solid #F44336; min-height: 280px;'>
        <h4 style='color:#C62828; margin-top:0;'>🔴 GORRIA / ROJO</h4>
        <b>Adina/Edad:</b> > 15 urte/años<br>
        <b>Altuera/Altura min.:</b> > 1,50m<br>
        <b>Erronkak/Retos:</b> 21 | <b>Tirolinak:</b> 5<br><br>
        Abenturazaleen zirkuitua. BERDEA + URDINA + GORRIA.<br>
        <i>Circuito para aventureros. VERDE + AZUL + ROJO.</i>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    
    # TIRA DE IMÁGENES AL FINAL (Dos filas de 3 imágenes, sin repetir)
    st.markdown("#### 📸 Irudiak / Imágenes")
    
    # Fila 1 de imágenes
    img1, img2, img3 = st.columns(3)
    with img1:
        st.image("https://mendexapark.com/wp-content/uploads/2018/05/mendexa-abentura-park-tirolinas-circuito-demo-01.jpg", use_container_width=True)
    with img2:
        st.image("https://mendexapark.com/wp-content/uploads/2018/05/mendexa-abentura-park-tirolinas-circuito-yoko-01.jpg", use_container_width=True)
    with img3:
        st.image("https://mendexapark.com/wp-content/uploads/2018/05/mendexa-abentura-park-tirolinas-circuito-verde-01.jpg", use_container_width=True)
        
    st.write("") # Espaciador
    
    # Fila 2 de imágenes
    img4, img5, img6 = st.columns(3)
    with img4:
        st.image("https://mendexapark.com/wp-content/uploads/2018/05/mendexa-abentura-park-tirolinas-circuito-azul-01.jpg", use_container_width=True)
    with img5:
        st.image("https://mendexapark.com/wp-content/uploads/2018/05/mendexa-abentura-park-tirolinas-circuito-rojo-01.jpg", use_container_width=True)
    with img6:
        # Añadida una nueva imagen para completar la cuadrícula sin repetir
        st.image("https://mendexapark.com/wp-content/uploads/2018/02/grupos-escolares-mendexa-park-parque-tirolinas-aventura-04.jpg", use_container_width=True)


# ==========================================
# 3. SEGURIDAD
# ==========================================
elif menu == "🛡️ 3. Segurtasuna \n\n Seguridad":
    col_s_img1, col_s_img2, col_s_img3 = st.columns([1, 2, 1])
    with col_s_img2:
        st.image("https://mendexapark.com/wp-content/uploads/2018/02/seguridad-mendexa-park-parque-tirolinas-aventura-01.jpg", use_container_width=True)
    
    st.markdown("### 🛡️ Lerro etengabedun segurtasun sistema berria / Nuevo sistema de línea continua")
    st.write("Mendexa Abentura Parkek **lerro etengabea** jarri du. Behin erabiltzailea bizi-lerroari konektatzen denean, ezin izango da deskonektatu zirkuituaren amaiera arte. Autonomia handiagoaz parkeaz disfrutatzen uzten digun sistema erraza eta guztiz **SEGURUA**.")
    st.write("Mendexa Abentura Park ha instalado la **Línea Continua**. Una vez que el usuario se conecta a la línea de vida no se puede desconectar hasta el final del circuito. Un sistema muy sencillo y totalmente **SEGURO**.")
    
    st.divider()
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown("#### 🎒 Zer ekarri / Vestimenta")
        st.write("✓ **Kirol-arropa erosoa** / Ropa deportiva cómoda.")
        st.write("✓ **Kirol-oinetako itxiak** (sandaliak debekatuta) / Calzado deportivo cerrado (sandalias prohibidas).")
        st.write("✓ **Ile luzea jasota** eraman behar da / El pelo largo debe ir recogido.")
        st.write("✓ **Poltsikoak hutsik** jardueran zehar / Bolsillos vacíos durante la actividad.")
    with col_s2:
        st.markdown("#### 🌦️ Eguraldia / Meteorología")
        st.write("✓ **Euriarekin jarduera egin daiteke.** / La actividad se puede realizar con lluvia.")
        st.write("✓ **Segurtasunagatik** (ekaitza/haizea) parkeak jarduera bertan behera utzi dezake. / Por seguridad (tormenta/viento) el parque puede cancelar la actividad.")
        st.write("✓ **15 minutu lehenago heltzea gomendatzen da.** / Se recomienda llegar 15 minutos antes.")

# ==========================================
# 4. LA CALCULADORA
# ==========================================
elif menu == "💶 4. Aurrekontua \n\n Calculadora":
    st.markdown("### 🏫 Ikastetxearen Datuak / Datos de la Escuela")

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

    col_opt1, col_opt2, col_opt3 = st.columns(3)
    with col_opt1:
        cif_escuela = st.text_input("CIF (Aukerakoa / Opcional)")
    with col_opt2:
        direccion_escuela = st.text_input("Helbidea / Dirección (Aukerakoa / Opcional)")
    with col_opt3:
        provincia_escuela = st.text_input("Probintzia / Provincia (Aukerakoa / Opcional)")

    st.divider()

    col_input, col_result = st.columns([1.4, 1])

    with col_input:
        st.markdown("### 📝 Aukeratu zure jarduera-paketea / Elige tu paquete de actividades")
        
        with st.expander("💶 Prezioen Taula / Tabla de Precios"):
            st.markdown("""
            | Programa | 10-19 ikasle / alumnos | 20-29 ikasle / alumnos | +29 ikasle / alumnos |
            | :--- | :---: | :---: | :---: |
            | **YOKO SOILIK** | **15,70 €** | **14,70 €** | **13,70 €** |
            | **2 ZIRKUITU** | **21,00 €** | **20,00 €** | **19,00 €** |
            | **3 ZIRKUITU** | **23,00 €** | **22,00 €** | **21,00 €** |
            """)
        
        st.info("ℹ️ **GARRANTZITSUA / IMPORTANTE:**\nZirkuitu guztiek **Demo** eta **Laranja** zirkuituak barne hartzen dituzte hasieran, beti egiten dira lehenengo. / Todos los programas incluyen los circuitos **Demo** y **Naranja** al inicio.")

        info_programak = {
            "1 ZIRKUITUA / CIRCUITO: YOKO SOILIK (Adina / Edad: 4-8 urte/años)": {
                "id": "yoko", "cat": "yoko", 
                "desc": "3 itzuli YOKO zirkuituan. / 3 vueltas en circuito YOKO.\n\n📏 Altuera / Altura min.: > 1,10m\n⏱️ Iraupena / Duración: 1h30 - 2h00"
            },
            "2 ZIRKUITU / CIRCUITOS (Adina / Edad: >9 urte/años)": {
                "id": "2c_9", "cat": "2c", 
                "desc": "2 itzuli zirkuitu BERDEETAN. / 2 vueltas en circuitos VERDES.\n\n📏 Altuera / Altura min.: > 1,40m\n⏱️ Iraupena / Duración: 2h00 - 2h30"
            },
            "2 ZIRKUITU / CIRCUITOS (Adina / Edad: >12 urte/años)": {
                "id": "2c_12", "cat": "2c", 
                "desc": "Zirkuitu BERDEA + URDINA. / Circuito VERDE + AZUL.\n\n📏 Altuera / Altura min.: > 1,50m\n⏱️ Iraupena / Duración: 2h00 - 2h30"
            },
            "3 ZIRKUITU / CIRCUITOS (Adina / Edad: 12-14 urte/años)": {
                "id": "3c_12", "cat": "3c", 
                "desc": "Zirkuitu BERDEA + 2 itzuli URDINEAN. / Circuito VERDE + 2 vueltas en AZUL.\n\n📏 Altuera / Altura min.: > 1,50m\n⏱️ Iraupena / Duración: 2h30 - 3h00"
            },
            "3 ZIRKUITU / CIRCUITOS (Adina / Edad: >15 urte/años)": {
                "id": "3c_15", "cat": "3c", 
                "desc": "Zirkuitu BERDEA + URDINA + GORRIA. / Circuito VERDE + AZUL + ROJO.\n\n📏 Altuera / Altura min.: > 1,50m\n⏱️ Iraupena / Duración: 2h30 - 3h00"
            }
        }

        alumnos_por_programa = {}
        total_alumnos = 0

        for titulo, info in info_programak.items():
            c1, c2, c3 = st.columns([0.1, 4, 1.5])
            with c2:
                st.markdown(f"**{titulo}**", help=info['desc'])
            with c3:
                num = st.number_input("Kopurua / Cantidad", min_value=0, step=1, key=info['id'], label_visibility="collapsed")
                alumnos_por_programa[titulo] = num
                total_alumnos += num

        st.markdown("---")
        num_profesores = st.number_input("Irakasle kopurua guztira: / Profesores en total:", min_value=0, value=2)

    with col_result:
        st.markdown("### 💰 Aurrekontu Laburpena / Resumen")
        
        if total_alumnos == 0:
            st.info("👈 Gehitu ikasleak ezkerrean. / Añade alumnos a la izquierda.")
        else:
            tier = 3 if total_alumnos > 29 else 2 if total_alumnos >= 20 else 1

            b1 = "#4CAF50" if tier == 1 else "#e0e0e0"
            b2 = "#4CAF50" if tier == 2 else "#e0e0e0"
            b3 = "#4CAF50" if tier == 3 else "#e0e0e0"
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; margin-bottom: 15px; font-family: sans-serif;">
                <div style="background-color: {b1}; color: white; padding: 8px 5px; border-radius: 5px; font-size: 0.85em; text-align: center; width: 32%; font-weight: bold;">
                    10-19 ikasle<br><small style="font-weight: normal;">Normala</small>
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
            
            info_txt_opcional = ""
            if cif_escuela: info_txt_opcional += f"CIF: {cif_escuela}\n"
            if direccion_escuela: info_txt_opcional += f"Helbidea / Dirección: {direccion_escuela}\n"
            if provincia_escuela: info_txt_opcional += f"Probintzia / Provincia: {provincia_escuela}\n"

            texto_descarga = f"MENDEXA ABENTURA PARK - AURREKONTUA / PRESUPUESTO\nIkastetxea / Centro escolar: {nombre_escuela}\n{info_txt_opcional}"
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
                    
                    listado_resumen_html += f"<div style='margin-bottom: 8px; border-left: 4px solid #2E7D32; padding-left: 10px;'><strong>{num} ikasle/alumnos</strong> - {titulo.split(' (')[0]}<br><span style='color: #2E7D32;'>{precio:.2f}€ x {num} = {subtotal:.2f}€</span></div>"
                    texto_descarga += f"- {num} ikasle / alumnos - {titulo.split(' (')[0]}: {subtotal:.2f}€\n"

            precio_medio = presupuesto_total / total_alumnos
            st.metric("Guztira / Total", f"{presupuesto_total:.2f} €")
            st.metric("Ikasleko / Por alumno", f"{precio_medio:.2f} €")
            st.write(f"👥 Ikasleak / Alumnos: {total_alumnos} | 🎁 Doako plaza / Plazas gratis: {total_alumnos // 10}")
            st.caption("Prezio guztiek %10eko BEZa barne hartzen dute / Todos los precios incluyen el 10% de IVA.")
            
            datos_listos = nombre_escuela != "" and es_email_valido(email_escuela) and es_telefono_valido(telefono_escuela)

            st.divider()
            
            if 'ticket_generado' not in st.session_state:
                st.session_state['ticket_generado'] = False

            if st.button("Aurrekontua Sortu / Generar", type="primary"):
                if not datos_listos:
                    st.error("⚠️ Ezin da aurrekontua sortu: Mesedez, bete itzazu goian eskatutako datu guztiak (*Izena, Telefonoa eta Emaila*). \n\n⚠️ No se puede generar: Por favor, rellena los datos obligatorios arriba (*Nombre, Teléfono y Email*).")
                else:
                    st.session_state['ticket_generado'] = True

            if st.session_state.get('ticket_generado') and datos_listos:
                
                info_html_opcional = ""
                if cif_escuela: info_html_opcional += f"<strong>CIF:</strong> {cif_escuela}<br>"
                if direccion_escuela: info_html_opcional += f"<strong>Helbidea / Dirección:</strong> {direccion_escuela}<br>"
                if provincia_escuela: info_html_opcional += f"<strong>Probintzia / Provincia:</strong> {provincia_escuela}<br>"

                st.markdown(f"""
                <div style="border: 5px solid #2E7D32; border-radius: 15px; padding: 25px; background-color: #fcfcfc; color: black; font-family: sans-serif;">
                    <h2 style="color: #2E7D32; text-align: center; margin-top: 0;">🌲 MENDEXA ABENTURA PARK 🌲</h2>
                    <p><strong>Ikastetxea / Centro Escolar:</strong> {nombre_escuela}<br>{info_html_opcional}<strong>Taldea / Grupo:</strong> {total_alumnos} ikasle/alumnos</p>
                    <div style="background: #f0f0f0; padding: 15px; border-radius: 10px; margin: 15px 0;">{listado_resumen_html}</div>
                    <div style="text-align: right; border-top: 2px solid #2E7D32; padding-top: 15px;">
                        <span style="font-size: 1.1em; color: #666;">Ikasleko (batez beste) / Por alumno (media): {precio_medio:.2f} €</span><br>
                        <span style="font-size: 1.4em; color: #444; font-weight: bold;">GUZTIRA / TOTAL: {presupuesto_total:.2f} €</span><br>
                        <small style="color: #888;">BEZ barne (%10) / IVA incluido (%10)</small>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                texto_descarga += f"\nTOTALA / TOTAL: {presupuesto_total:.2f}€ (BEZ barne / IVA incluido)\nIkasleko / Por alumno: {precio_medio:.2f}€"
                st.download_button("📩 Deskargatu aurrekontua (TXT) / Descargar presupuesto (TXT)", data=texto_descarga, file_name=f"Aurrekontua_{nombre_escuela.replace(' ', '_')}.txt")

                asunto = urllib.parse.quote(f"Eskola Erreserba / Reserva Escolar: {nombre_escuela}")
                cuerpo = urllib.parse.quote(f"Ikastetxea / Centro Escolar: {nombre_escuela}\nGUZTIRA / TOTAL: {presupuesto_total:.2f}€")
                mailto_link = f"mailto:ikerlarrap@gmail.com?subject={asunto}&body={cuerpo}"
                st.markdown(f'<center><a href="{mailto_link}" target="_blank"><button style="background-color:#4CAF50; color:white; border:none; padding:12px; border-radius:8px; cursor:pointer; font-weight:bold;">📧 Bidali eskaera orain / Enviar reserva ahora</button></a></center>', unsafe_allow_html=True)
