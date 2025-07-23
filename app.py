import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Irakani Builder - Dashboard de Costos",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS para tema oscuro y estilo KPI
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    .metric-container {
        background: linear-gradient(135deg, #1e2329 0%, #2d3748 100%);
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #4a5568;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    .metric-title {
        font-size: 14px;
        color: #a0aec0;
        margin-bottom: 5px;
    }
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: #00d4aa;
    }
    .total-metric {
        background: linear-gradient(135deg, #2d5a27 0%, #38a169 100%);
        color: white;
    }
    .stMarkdown h3 {
        color: #00d4aa;
        margin-top: 20px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Precios de los modelos
ANTHROPIC_PRICES = {
    "Claude Opus 4": {"input": 0.015, "output": 0.075},
    "Claude Sonnet 4": {"input": 0.003, "output": 0.015},
    "Claude 3.5 Sonnet": {"input": 0.003, "output": 0.015},
    "Claude 3.5 Haiku": {"input": 0.0008, "output": 0.004}
}

TITAN_PRICES = {
    "< 512x512 Standard": 0.008,
    "< 512x512 Premium": 0.01,
    "> 512x512 Standard": 0.01,
    "> 512x512 Premium": 0.012
}

def main():
    st.title("🚀 Irakani Builder - Dashboard de Costo-Beneficio")
    
    # Sidebar para datos de entrada
    with st.sidebar:
        st.header("⚙️ Datos de Entrada")
        
        st.subheader("📝 Modelos de Texto")
        
        # Claude Sonnet 4
        st.write("**Claude Sonnet 4**")
        col1_1, col1_2 = st.columns([3, 1])
        with col1_1:
            sonnet4_input_1 = st.number_input("Tokens entrada", min_value=0, value=0, key="sonnet4_input_1")
        with col1_2:
            sonnet4_input_2 = st.number_input("+", min_value=0, value=0, key="sonnet4_input_2")
        sonnet4_input = sonnet4_input_1 + sonnet4_input_2
        
        col1_3, col1_4 = st.columns([3, 1])
        with col1_3:
            sonnet4_output_1 = st.number_input("Tokens salida", min_value=0, value=0, key="sonnet4_output_1")
        with col1_4:
            sonnet4_output_2 = st.number_input("+", min_value=0, value=0, key="sonnet4_output_2")
        sonnet4_output = sonnet4_output_1 + sonnet4_output_2
        
        # Claude 3.5 Haiku
        st.write("**Claude 3.5 Haiku**")
        col2_1, col2_2 = st.columns([3, 1])
        with col2_1:
            haiku_input_1 = st.number_input("Tokens entrada", min_value=0, value=0, key="haiku_input_1")
        with col2_2:
            haiku_input_2 = st.number_input("+", min_value=0, value=0, key="haiku_input_2")
        haiku_input = haiku_input_1 + haiku_input_2
        
        col2_3, col2_4 = st.columns([3, 1])
        with col2_3:
            haiku_output_1 = st.number_input("Tokens salida", min_value=0, value=0, key="haiku_output_1")
        with col2_4:
            haiku_output_2 = st.number_input("+", min_value=0, value=0, key="haiku_output_2")
        haiku_output = haiku_output_1 + haiku_output_2
        
        st.subheader("🖼️ Imágenes")
        col3_1, col3_2 = st.columns([3, 1])
        with col3_1:
            titan_small_std_1 = st.number_input("Titan = 512x512", min_value=0, value=0, key="titan_small_std_1")
        with col3_2:
            titan_small_std_2 = st.number_input("+", min_value=0, value=0, key="titan_small_std_2")
        titan_small_std = titan_small_std_1 + titan_small_std_2
        
        st.markdown("---")
        st.subheader("💱 Configuración")
        usd_to_mxn = st.slider("Tipo de cambio USD a MXN", min_value=15.0, max_value=25.0, value=20.0, step=0.1)
    
    
    # Métricas de ahorro de tiempo
    st.markdown("---")
    st.header("⏱️ Métricas de Eficiencia")
    
    # Porcentajes de ahorro para cada funcionalidad (conservadores)
    efficiency_percentages = {
        "app_generation": 50.0,  # De 1-2 días a medio día
        "form_building": 40.0,   # Formularios: de 4 horas a 2.4 horas
        "icon_creation": 60.0,   # Iconos: de 30 min a 12 min
        "code_modification": 30.0 # Código: de 5 horas a 3.5 horas
    }
    
    # Proporciones de tiempo entre Builder e IA (más equilibradas)
    builder_ia_ratio = {
        "app_generation": {"builder": 0.40, "ia": 0.60},  # 40% Builder, 60% IA
        "form_building": {"builder": 0.50, "ia": 0.50},   # 50% Builder, 50% IA
        "icon_creation": {"builder": 0.20, "ia": 0.80},   # 20% Builder, 80% IA
        "code_modification": {"builder": 0.35, "ia": 0.65} # 35% Builder, 65% IA
    }
    
    # Valores tradicionales iniciales más realistas (pueden ser ajustados por el usuario)
    with st.sidebar:
        st.markdown("---")
        st.subheader("🔄 Ajustar Tiempos Tradicionales")
        traditional_times = {
            "app_generation": st.slider("Generación de Apps (min)", 480, 1440, 720, step=60),  # 8-24 horas, default 12h
            "form_building": st.slider("Construcción de Formularios (min)", 120, 480, 240, step=30),  # 2-8 horas, default 4h
            "icon_creation": st.slider("Creación de Iconos (min)", 15, 60, 30, step=5),  # 15-60 min, default 30min
            "code_modification": st.slider("Modificación de Código (min)", 120, 480, 300, step=30)  # 2-8 horas, default 5h
        }
    
    # Calcular tiempos de Irakani+IA basados en los porcentajes de eficiencia
    time_savings = {}
    for key, traditional in traditional_times.items():
        # Calcular tiempo total de Irakani+IA
        total_irakani_ia = traditional * (1 - efficiency_percentages[key]/100)
        
        # Dividir entre Builder e IA según las proporciones
        irakani_time = total_irakani_ia * builder_ia_ratio[key]["builder"]
        ia_time = total_irakani_ia * builder_ia_ratio[key]["ia"]
        
        # Redondear a enteros
        time_savings[key] = {
            "traditional": traditional,
            "irakani": round(irakani_time),
            "ai_support": round(ia_time)
        }
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_traditional = sum([v["traditional"] for v in time_savings.values()])
        total_irakani = sum([v["irakani"] + v["ai_support"] for v in time_savings.values()])
        time_saved = total_traditional - total_irakani
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-title">⏰ Tiempo Ahorrado Total</div>
            <div class="metric-value">{time_saved} min</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        efficiency = ((total_traditional - total_irakani) / total_traditional) * 100
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-title">📈 Eficiencia Ganada</div>
            <div class="metric-value">{efficiency:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-title">🔧 Tiempo Tradicional</div>
            <div class="metric-value">{total_traditional} min</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-container total-metric">
            <div class="metric-title">🚀 Tiempo con Irakani + IA</div>
            <div class="metric-value">{total_irakani} min</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Desglose por funcionalidad
    st.subheader("📊 Desglose por Funcionalidad")
    
    func_names = {
        "app_generation": "🚀 Generación de Apps",
        "form_building": "🔧 Construcción de Formularios", 
        "icon_creation": "🎨 Creación de Iconos",
        "code_modification": "✏️ Modificación de Código"
    }
    
    # Datos para la comparación
    irakani_only = {
        "app_generation": 15,  # minutos
        "form_building": 8,
        "icon_creation": 3,
        "code_modification": 20
    }
    
    for key, data in time_savings.items():
        st.markdown(f"### {func_names[key]}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-title">🕰️ Método Tradicional</div>
                <div class="metric-value">{data['traditional']} min</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_new = data['irakani'] + data['ai_support']
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-title">🚀 Irakani + IA</div>
                <div class="metric-value">{total_new} min</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; margin-top: 5px;">
                <div style="background-color: #2d3748; padding: 5px 10px; border-radius: 5px; color: #00d4aa; font-size: 12px;">
                    🛠️ Builder: {data['irakani']} min
                </div>
                <div style="background-color: #2d3748; padding: 5px 10px; border-radius: 5px; color: #00d4aa; font-size: 12px;">
                    🤖 IA: {data['ai_support']} min
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            savings_pct = ((data['traditional'] - total_new) / data['traditional']) * 100
            time_saved = data['traditional'] - total_new
            st.markdown(f"""
            <div class="metric-container total-metric">
                <div class="metric-title">💰 Ahorro Total</div>
                <div class="metric-value">{savings_pct:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
            st.caption(f"Ahorro: {time_saved} minutos")
        
        st.markdown("---")
    
    # Explicación de métricas
    st.markdown("---")
    st.header("📊 Explicación de Métricas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1e2329 0%, #2d3748 100%); padding: 20px; border-radius: 10px; border: 1px solid #4a5568; margin-bottom: 20px;">
            <h3 style="color: #00d4aa; margin-top: 0;">🚀 Generación de Apps</h3>
            <div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
                <div>
                    <p style="color: #a0aec0; margin: 0;">Método Tradicional</p>
                    <p style="color: #fafafa; font-size: 24px; font-weight: bold; margin: 0;">12 horas</p>
                    <p style="color: #a0aec0; font-size: 12px; margin: 0;">1-2 días de desarrollo</p>
                </div>
                <div>
                    <p style="color: #a0aec0; margin: 0;">Irakani + IA</p>
                    <p style="color: #00d4aa; font-size: 24px; font-weight: bold; margin: 0;">6 horas</p>
                    <p style="color: #a0aec0; font-size: 12px; margin: 0;">🛠️ Builder: 2.4h + 🤖 IA: 3.6h</p>
                </div>
                <div>
                    <p style="color: #a0aec0; margin: 0;">Ahorro Total</p>
                    <p style="color: #38a169; font-size: 24px; font-weight: bold; margin: 0;">50%</p>
                    <p style="color: #a0aec0; font-size: 12px; margin: 0;">6 horas ahorradas</p>
                </div>
            </div>
            <p style="color: #fafafa;"><strong>Interpretación:</strong> La generación de aplicaciones con Irakani Builder optimiza el proceso de desarrollo. Lo que tradicionalmente requiere 1-2 días de trabajo (12 horas) se puede completar en 6 horas. El proceso combina 2.4 horas de configuración en el Builder con 3.6 horas de desarrollo asistido por IA, logrando un ahorro del 50% del tiempo.</p>
        </div>
        
        <div style="background: linear-gradient(135deg, #1e2329 0%, #2d3748 100%); padding: 20px; border-radius: 10px; border: 1px solid #4a5568; margin-bottom: 20px;">
            <h3 style="color: #00d4aa; margin-top: 0;">🎨 Creación de Iconos</h3>
            <div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
                <div>
                    <p style="color: #a0aec0; margin: 0;">Método Tradicional</p>
                    <p style="color: #fafafa; font-size: 24px; font-weight: bold; margin: 0;">30 min</p>
                    <p style="color: #a0aec0; font-size: 12px; margin: 0;">Diseño manual/búsqueda</p>
                </div>
                <div>
                    <p style="color: #a0aec0; margin: 0;">Irakani + IA</p>
                    <p style="color: #00d4aa; font-size: 24px; font-weight: bold; margin: 0;">12 min</p>
                    <p style="color: #a0aec0; font-size: 12px; margin: 0;">🛠️ Builder: 2 min + 🤖 IA: 10 min</p>
                </div>
                <div>
                    <p style="color: #a0aec0; margin: 0;">Ahorro Total</p>
                    <p style="color: #38a169; font-size: 24px; font-weight: bold; margin: 0;">60%</p>
                    <p style="color: #a0aec0; font-size: 12px; margin: 0;">18 minutos ahorrados</p>
                </div>
            </div>
            <p style="color: #fafafa;"><strong>Interpretación:</strong> La creación de iconos con Irakani Builder acelera el proceso de diseño. Lo que tradicionalmente requiere 30 minutos entre diseño manual o búsqueda de iconos apropiados, se reduce a 12 minutos. El proceso combina 2 minutos de configuración en el Builder con 10 minutos de generación y ajustes con IA, logrando un ahorro del 60% del tiempo.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1e2329 0%, #2d3748 100%); padding: 20px; border-radius: 10px; border: 1px solid #4a5568; margin-bottom: 20px;">
            <h3 style="color: #00d4aa; margin-top: 0;">🔧 Construcción de Formularios</h3>
            <div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
                <div>
                    <p style="color: #a0aec0; margin: 0;">Método Tradicional</p>
                    <p style="color: #fafafa; font-size: 24px; font-weight: bold; margin: 0;">4 horas</p>
                    <p style="color: #a0aec0; font-size: 12px; margin: 0;">Codificación manual</p>
                </div>
                <div>
                    <p style="color: #a0aec0; margin: 0;">Irakani + IA</p>
                    <p style="color: #00d4aa; font-size: 24px; font-weight: bold; margin: 0;">2.4 horas</p>
                    <p style="color: #a0aec0; font-size: 12px; margin: 0;">🛠️ Builder: 72 min + 🤖 IA: 72 min</p>
                </div>
                <div>
                    <p style="color: #a0aec0; margin: 0;">Ahorro Total</p>
                    <p style="color: #38a169; font-size: 24px; font-weight: bold; margin: 0;">40%</p>
                    <p style="color: #a0aec0; font-size: 12px; margin: 0;">1.6 horas ahorradas</p>
                </div>
            </div>
            <p style="color: #fafafa;"><strong>Interpretación:</strong> La construcción de formularios con Irakani Builder mejora el proceso de desarrollo. Lo que tradicionalmente requiere 4 horas de codificación manual se reduce a 2.4 horas. El proceso equilibra 72 minutos de configuración visual en el Builder con 72 minutos de personalización asistida por IA, logrando un ahorro del 40% del tiempo.</p>
        </div>
        
        <div style="background: linear-gradient(135deg, #1e2329 0%, #2d3748 100%); padding: 20px; border-radius: 10px; border: 1px solid #4a5568; margin-bottom: 20px;">
            <h3 style="color: #00d4aa; margin-top: 0;">✏️ Modificación de Código</h3>
            <div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
                <div>
                    <p style="color: #a0aec0; margin: 0;">Método Tradicional</p>
                    <p style="color: #fafafa; font-size: 24px; font-weight: bold; margin: 0;">5 horas</p>
                    <p style="color: #a0aec0; font-size: 12px; margin: 0;">Edición manual</p>
                </div>
                <div>
                    <p style="color: #a0aec0; margin: 0;">Irakani + IA</p>
                    <p style="color: #00d4aa; font-size: 24px; font-weight: bold; margin: 0;">3.5 horas</p>
                    <p style="color: #a0aec0; font-size: 12px; margin: 0;">🛠️ Builder: 74 min + 🤖 IA: 136 min</p>
                </div>
                <div>
                    <p style="color: #a0aec0; margin: 0;">Ahorro Total</p>
                    <p style="color: #38a169; font-size: 24px; font-weight: bold; margin: 0;">30%</p>
                    <p style="color: #a0aec0; font-size: 12px; margin: 0;">1.5 horas ahorradas</p>
                </div>
            </div>
            <p style="color: #fafafa;"><strong>Interpretación:</strong> La modificación de código personalizado con Irakani Builder mejora el proceso de desarrollo. Lo que tradicionalmente requiere 5 horas de edición manual se reduce a 3.5 horas. El proceso combina 74 minutos de configuración en el Builder con 136 minutos de desarrollo asistido por IA, logrando un ahorro del 30% del tiempo manteniendo la calidad del código.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Estudio destacado sobre IA y productividad
    st.markdown("---")
    st.header("📘 Estudio Destacado")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1e2329 0%, #2d3748 100%); padding: 20px; border-radius: 10px; border: 1px solid #4a5568;">
            <h3 style="color: #00d4aa; margin-top: 0;">The Impact of AI on Developer Productivity</h3>
            <p style="color: #a0aec0; font-size: 14px;">Evidence from GitHub Copilot</p>
            <p style="color: #fafafa;">Autores: Peng, S., Kalliamvakou, E., Cihon, P., & Demirer, M. (2023)</p>
            <p style="color: #a0aec0;">Publicado en arXiv el 13 de febrero de 2023</p>
            <a href="https://arxiv.org/abs/2302.06590" style="color: #00d4aa; text-decoration: none;">Ver estudio completo →</a>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("🔍 Métricas clave")
        st.markdown("""
        - En un experimento controlado con tiempo cronometrado:
          - El grupo que usó GitHub Copilot completó la tarea un **55.8% más rápido** que el grupo sin IA
          - Tarea: implementación de un servidor HTTP en JavaScript
          - Tiempo promedio con Copilot: **1h 11min**; sin Copilot: **2h 41min**
        
        **Interpretación:**
        - Un aumento del ~56% en eficiencia significa que una tarea que normalmente tomaría ~2h40m puede reducirse a 1h10m
        - Equivale a duplicar la productividad en ese tipo de tarea
        - Aunque es un estudio controlado, representa bien un entorno de programación típico
        """)
    

    
    # Videos de demostración
    st.markdown("---")
    st.header("🎥 Demostraciones de Irakani Builder")
    
    video_tabs = st.tabs(["App Generator", "Builder", "Icon Tools", "Modificaciones"])
    
    with video_tabs[0]:
        st.subheader("🚀 Generación de Aplicaciones")
        col1, col2 = st.columns(2)
        with col1:
            st.video("media/AppGenerator.mp4")
            st.caption("Generación automática de aplicaciones")
        with col2:
            st.video("media/IrakaniApp.mp4")
            st.caption("Aplicación Irakani en acción")
    
    with video_tabs[1]:
        st.subheader("🔧 Constructor de Formularios")
        col1, col2 = st.columns(2)
        with col1:
            st.video("media/BuilderAgregarMasElementosAFormulario.mp4")
            st.caption("Agregar elementos a formularios")
        with col2:
            st.video("media/IrakaniAgregarMasElementos.mp4")
            st.caption("Añadir más elementos")
    
    with video_tabs[2]:
        st.subheader("🎨 Herramientas de Iconos")
        col1, col2 = st.columns(2)
        with col1:
            st.video("media/IconGenerator.mp4")
            st.caption("Generador de iconos")
        with col2:
            st.video("media/IconSearch.mp4")
            st.caption("Búsqueda de iconos")
    
    with video_tabs[3]:
        st.subheader("✏️ Modificaciones y Código")
        col1, col2 = st.columns(2)
        with col1:
            st.video("media/BuilderModificacionElemento.mp4")
            st.caption("Modificación de elementos")
        with col2:
            st.video("media/IrakaniModificacionElemento.mp4")
            st.caption("Modificaciones en Irakani")
        
        col1, col2 = st.columns(2)
        with col1:
            #st.video("media/Generacion de codigo personalizado.mp4")
            st.caption("Generación de código personalizado")
        with col2:
            st.video("media/BuilderCodigoPersonalizado.mp4")
            st.caption("Builder - Código personalizado")

    # Área principal
    st.header("💰 KPIs de Costos")
    
    # Costos de texto (conversión automática a miles para el cálculo)
    sonnet4_cost = ((sonnet4_input / 1000) * ANTHROPIC_PRICES["Claude Sonnet 4"]["input"]) + ((sonnet4_output / 1000) * ANTHROPIC_PRICES["Claude Sonnet 4"]["output"])
    haiku_cost = ((haiku_input / 1000) * ANTHROPIC_PRICES["Claude 3.5 Haiku"]["input"]) + ((haiku_output / 1000) * ANTHROPIC_PRICES["Claude 3.5 Haiku"]["output"])
    
    # Costos de imágenes
    titan_cost = titan_small_std * TITAN_PRICES["< 512x512 Standard"]
    
    total_cost = sonnet4_cost + haiku_cost + titan_cost
    
    # Convertir costos a MXN
    sonnet4_cost_mxn = sonnet4_cost * usd_to_mxn
    haiku_cost_mxn = haiku_cost * usd_to_mxn
    titan_cost_mxn = titan_cost * usd_to_mxn
    total_cost_mxn = total_cost * usd_to_mxn
    
    # KPIs estilo dashboard
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-title">🤖 Claude Sonnet 4</div>
            <div class="metric-value">${sonnet4_cost_mxn:.2f} MXN</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-title">🖼️ Amazon Titan</div>
            <div class="metric-value">${titan_cost_mxn:.2f} MXN</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-title">⚡ Claude 3.5 Haiku</div>
            <div class="metric-value">${haiku_cost_mxn:.2f} MXN</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-container total-metric">
            <div class="metric-title">💎 TOTAL POR INFERENCIA</div>
            <div class="metric-value">${total_cost_mxn:.2f} MXN</div>
        </div>
        """, unsafe_allow_html=True)
    
    
    # Desglose detallado de costos
    if total_cost > 0:
        st.markdown("---")
        st.header("💰 Desglose Detallado de Costos")
        
        with st.expander("Ver detalles de cálculo de costos", expanded=False):
            if sonnet4_cost > 0:
                st.write(f"**Claude Sonnet 4:** ${sonnet4_cost:.4f}")
                st.write(f"  - Entrada: {sonnet4_input:,} tokens × $0.003/1k = ${(sonnet4_input / 1000) * 0.003:.4f}")
                st.write(f"  - Salida: {sonnet4_output:,} tokens × $0.015/1k = ${(sonnet4_output / 1000) * 0.015:.4f}")
            
            if haiku_cost > 0:
                st.write(f"**Claude 3.5 Haiku:** ${haiku_cost:.4f}")
                st.write(f"  - Entrada: {haiku_input:,} tokens × $0.0008/1k = ${(haiku_input / 1000) * 0.0008:.4f}")
                st.write(f"  - Salida: {haiku_output:,} tokens × $0.004/1k = ${(haiku_output / 1000) * 0.004:.4f}")
            
            if titan_cost > 0:
                st.write(f"**Amazon Titan:** ${titan_cost:.4f}")
                st.write(f"  - Imágenes 512x512 (Std): {titan_small_std} × $0.008 = ${titan_small_std * 0.008:.4f}")
    
    # Análisis costo-beneficio
    st.markdown("---")
    st.header("⚖️ Análisis Costo-Beneficio")
    
    # Cálculo de tarifa por hora en pesos mexicanos
    monthly_salary_mxn = 8000  # Pesos mexicanos
    working_hours_per_month = 160  # 8 horas × 20 días laborales
    hourly_rate_mxn = monthly_salary_mxn / working_hours_per_month  # $50 MXN por hora
    
    traditional_hours = total_traditional / 60
    irakani_hours = total_irakani / 60
    
    traditional_labor_cost_mxn = traditional_hours * hourly_rate_mxn
    irakani_labor_cost_mxn = irakani_hours * hourly_rate_mxn
    total_savings_mxn = traditional_labor_cost_mxn - (irakani_labor_cost_mxn + total_cost_mxn)
    roi = (total_savings_mxn / (irakani_labor_cost_mxn + total_cost_mxn)) * 100 if (irakani_labor_cost_mxn + total_cost_mxn) > 0 else 0
    
    # Caso de estudio: Ojo Zarco (más realista)
    ojo_zarco_traditional_cost = 6 * hourly_rate_mxn   # 6 horas-persona (2 devs × 3 horas)
    ojo_zarco_irakani_cost = 3 * hourly_rate_mxn + 50  # 3 horas-persona (1 dev × 3 horas) + 50 MXN IA
    ojo_zarco_savings = ojo_zarco_traditional_cost - ojo_zarco_irakani_cost
    ojo_zarco_savings_pct = (ojo_zarco_savings / ojo_zarco_traditional_cost) * 100
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1e2329 0%, #2d3748 100%); padding: 20px; border-radius: 10px; border: 1px solid #4a5568; margin-bottom: 20px;">
        <h3 style="color: #00d4aa; margin-top: 0;">💻 Caso de Estudio: Ojo Zarco</h3>
        <div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
            <div>
                <p style="color: #a0aec0; margin: 0;">Método Tradicional</p>
                <p style="color: #fafafa; font-size: 24px; font-weight: bold; margin: 0;">${ojo_zarco_traditional_cost:.2f} MXN</p>
                <p style="color: #a0aec0; font-size: 12px; margin: 0;">6 horas-persona × ${hourly_rate_mxn:.0f}/hr</p>
            </div>
            <div>
                <p style="color: #a0aec0; margin: 0;">Con Irakani Builder</p>
                <p style="color: #00d4aa; font-size: 24px; font-weight: bold; margin: 0;">${ojo_zarco_irakani_cost:.2f} MXN</p>
                <p style="color: #a0aec0; font-size: 12px; margin: 0;">Trabajo: $150 + IA: $50</p>
            </div>
            <div>
                <p style="color: #a0aec0; margin: 0;">Ahorro Total</p>
                <p style="color: #38a169; font-size: 24px; font-weight: bold; margin: 0;">${ojo_zarco_savings:.2f} MXN</p>
                <p style="color: #a0aec0; font-size: 12px; margin: 0;">{ojo_zarco_savings_pct:.0f}% de ahorro</p>
            </div>
        </div>
        <p style="color: #fafafa;"><strong>Caso real:</strong> En la demo de Ojo Zarco, se requirieron 2 desarrolladores invirtiendo 3 horas cada uno (total: 6 horas-persona = ${ojo_zarco_traditional_cost:.2f} MXN) para crear 2 aplicaciones de captura de información. Con Irakani Builder, la misma tarea habría requerido solo 1 desarrollador trabajando durante 3 horas más $50 MXN en costos de IA (${ojo_zarco_irakani_cost:.2f} MXN total), representando un ahorro de ${ojo_zarco_savings:.2f} MXN ({ojo_zarco_savings_pct:.0f}% menos costo) y una reducción del 50% en personal necesario.</p>
    </div>
    
    ### Explicación del análisis costo-beneficio

    <div style="background: linear-gradient(135deg, #1e2329 0%, #2d3748 100%); padding: 20px; border-radius: 10px; border: 1px solid #4a5568; margin-bottom: 20px;">
        <h3 style="color: #00d4aa; margin-top: 0;">Análisis Financiero</h3>
        <div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
            <div>
                <p style="color: #a0aec0; margin: 0;">Método Tradicional</p>
                <p style="color: #fafafa; font-size: 24px; font-weight: bold; margin: 0;">${traditional_labor_cost_mxn:.2f} MXN</p>
                <p style="color: #a0aec0; font-size: 12px; margin: 0;">{traditional_hours:.1f} horas × ${hourly_rate_mxn:.0f}/hr</p>
            </div>
            <div>
                <p style="color: #a0aec0; margin: 0;">Irakani + IA</p>
                <p style="color: #00d4aa; font-size: 24px; font-weight: bold; margin: 0;">${irakani_labor_cost_mxn + total_cost_mxn:.2f} MXN</p>
                <p style="color: #a0aec0; font-size: 12px; margin: 0;">Trabajo: ${irakani_labor_cost_mxn:.2f} + IA: ${total_cost_mxn:.2f}</p>
            </div>
            <div>
                <p style="color: #a0aec0; margin: 0;">Ahorro Total</p>
                <p style="color: #38a169; font-size: 24px; font-weight: bold; margin: 0;">${total_savings_mxn:.2f} MXN</p>
                <p style="color: #a0aec0; font-size: 12px; margin: 0;">ROI: {roi:.1f}%</p>
            </div>
        </div>
        <p style="color: #fafafa;"><strong>Interpretación:</strong> El análisis costo-beneficio muestra que Irakani Builder reduce drásticamente los costos de desarrollo. Para una aplicación que tradicionalmente costaría ${traditional_labor_cost_mxn:.2f} MXN ({traditional_hours:.1f} horas a ${hourly_rate_mxn:.0f} MXN/hr), con Irakani + IA el costo se reduce a solo ${irakani_labor_cost_mxn + total_cost_mxn:.2f} MXN ({irakani_hours:.1f} horas de trabajo más el costo de la IA). Esto representa un ahorro de ${total_savings_mxn:.2f} MXN, equivalente a un ROI del {roi:.1f}%. En términos de tiempo, se ahorran {(traditional_hours - irakani_hours):.1f} horas, lo que significa un {((traditional_hours - irakani_hours) / traditional_hours * 100):.1f}% de mejora en eficiencia.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-title">🕰️ Método Tradicional</div>
            <div class="metric-value">${traditional_labor_cost_mxn:.2f} MXN</div>
        </div>
        """, unsafe_allow_html=True)
        st.caption(f"{traditional_hours:.1f} horas × ${hourly_rate_mxn:.0f} MXN/hr")
    
    with col2:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-title">🚀 Irakani + IA</div>
            <div class="metric-value">${irakani_labor_cost_mxn + total_cost_mxn:.2f} MXN</div>
        </div>
        """, unsafe_allow_html=True)
        st.caption(f"Trabajo: ${irakani_labor_cost_mxn:.2f} + IA: ${total_cost_mxn:.2f}")
    
    with col3:
        st.markdown(f"""
        <div class="metric-container total-metric">
            <div class="metric-title">💰 Ahorro Total</div>
            <div class="metric-value">${total_savings_mxn:.2f} MXN</div>
        </div>
        """, unsafe_allow_html=True)
        st.caption(f"ROI: {roi:.1f}%")
    
    with col4:
        st.markdown(f"""
        <div class="metric-container total-metric">
            <div class="metric-title">⏱️ Tiempo Ahorrado</div>
            <div class="metric-value">{(traditional_hours - irakani_hours):.1f}h</div>
        </div>
        """, unsafe_allow_html=True)
        st.caption(f"{((traditional_hours - irakani_hours) / traditional_hours * 100):.1f}% más eficiente")

if __name__ == "__main__":
    main()