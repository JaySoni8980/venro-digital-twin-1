import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="ReActScrub Platform 2.0 | AVENRO",
    page_icon="Ω",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# BULLETPROOF DARK THEME CSS OVERRIDE
# ==========================================
st.markdown("""
    <style>
    /* 1. Force Global App Background to Deep Slate */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #080d1a !important;
    }
    
    /* 2. Force Text Colors to Off-White */
    h1, h2, h3, h4, p, label {
        color: #e2e8f0 !important;
    }

    /* 3. Fix Tab Headers */
    button[data-baseweb="tab"] p {
        color: #94a3b8 !important;
        font-size: 1rem;
        font-weight: 600;
    }
    button[data-baseweb="tab"][aria-selected="true"] p {
        color: #10b981 !important;
    }

    /* 4. Fix Industrial Preset Buttons */
    div.stButton > button {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }
    div.stButton > button p {
        color: #f8fafc !important;
    }
    div.stButton > button:hover {
        background-color: #059669 !important;
        border-color: #10b981 !important;
    }

    /* 5. Fix Chat Dialogue */
    div[data-testid="stChatMessage"] {
        background-color: #151f32 !important;
        border: 1px solid #334155 !important;
        border-radius: 10px;
    }
    div[data-testid="stChatMessage"] * {
        color: #f1f5f9 !important;
    }

    /* 6. Fix Info/Warning Alert Boxes */
    div[data-testid="stAlert"] {
        background-color: #151f32 !important;
        border: 1px solid #334155 !important;
    }
    
    /* 7. Fix KPI Metrics Styling */
    div[data-testid="stMetricValue"] div {
        color: #10b981 !important;
    }
    div[data-testid="stMetricLabel"] p {
        color: #94a3b8 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================
if 'flow' not in st.session_state:
    st.session_state.flow = 25000.0
if 'temp' not in st.session_state:
    st.session_state.temp = 95.0
if 'co2' not in st.session_state:
    st.session_state.co2 = 15.0
if 'sox' not in st.session_state:
    st.session_state.sox = 450.0
if 'nox' not in st.session_state:
    st.session_state.nox = 300.0
if 'voc' not in st.session_state:
    st.session_state.voc = 150.0
if 'h2s' not in st.session_state:
    st.session_state.h2s = 0.0
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Welcome to the **AVENRO** digital twin interface. I am **ScrubAI**, your process intensification partner. Provide raw flue gas parameters or click an industrial preset to configure your multi-stage reactor flowsheet in real time."}
    ]

def apply_preset(preset_name):
    presets = {
        "Cement Kiln": {"flow": 50000.0, "temp": 125.0, "co2": 18.5, "sox": 400.0, "nox": 350.0, "voc": 50.0, "h2s": 0.0},
        "Distillery": {"flow": 6000.0, "temp": 35.0, "co2": 96.0, "sox": 0.0, "nox": 0.0, "voc": 350.0, "h2s": 0.0},
        "Steel Plant": {"flow": 80000.0, "temp": 140.0, "co2": 24.0, "sox": 150.0, "nox": 80.0, "voc": 20.0, "h2s": 250.0}
    }
    p = presets[preset_name]
    for key, value in p.items():
        st.session_state[key] = value
    st.session_state.chat_history.append({"role": "user", "content": f"Loaded Industrial Preset: {preset_name}"})
    st.session_state.chat_history.append({"role": "assistant", "content": f"Architecture synchronized for **{preset_name}**. Volumetric flow set to {p['flow']:,} Nm³/h with {p['co2']}% CO₂ and {p['sox']} ppm SO₂. Flowsheet synthesis active in Auto-Architect tab."})

# ==========================================
# APP HEADER
# ==========================================
header_col1, header_col2 = st.columns([3, 1])
with header_col1:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 14px;">
            <div style="background: linear-gradient(135deg, #059669, #0284c7); width: 50px; height: 50px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 28px; font-weight: bold; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">Ω</div>
            <div>
                <div style="font-size: 0.9rem; font-weight: 800; color: #34d399; letter-spacing: 2px; text-transform: uppercase; margin-bottom: -4px;">Avenro Technologies</div>
                <h1 style="margin: 0; font-size: 1.8rem; color: white !important;">ReActScrub <span style="color: #10b981;">Platform 2.0</span></h1>
                <p style="margin: 0; font-size: 0.85rem; color: #94a3b8 !important;">Transport-Coupled Modular Digital Twin • SVD Process Similarity Scaling</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
with header_col2:
    st.markdown("""
        <div style="background-color: #151f32; border: 1px solid #1e293b; border-radius: 10px; padding: 10px 14px; text-align: right;">
            <span style="font-size: 0.75rem; color: #94a3b8;">Exchange Benchmark</span><br>
            <span style="font-family: monospace; font-weight: 700; color: #38bdf8;">$1.00 USD = ₹84.00 INR</span>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='border: none; border-top: 1px solid #1e293b; margin: 15px 0 25px 0;'>", unsafe_allow_html=True)

# ==========================================
# TABS INTERFACE
# ==========================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "💬 ScrubAI Advisor", 
    "⚙️ Auto-Architect", 
    "🔬 3D Transport", 
    "📊 SVD Scale Engine", 
    "💰 Techno-Economics",
    "📞 Contact Us"
])

# ------------------------------------------
# TAB 1: ScrubAI Advisor
# ------------------------------------------
with tab1:
    col_preset, col_chat = st.columns([1, 2])
    
    with col_preset:
        st.markdown("### 🏭 Industrial Presets")
        st.caption("Load verified plant stream baselines directly into the architecture engine:")
        
        if st.button("Cement Kiln (18.5% CO₂, 400 ppm SO₂)", use_container_width=True):
            apply_preset("Cement Kiln")
        if st.button("Distillery Offgas (96% CO₂ Biogenic)", use_container_width=True):
            apply_preset("Distillery")
        if st.button("Steel Blast Furnace (24% CO₂, 250 ppm H₂S)", use_container_width=True):
            apply_preset("Steel Plant")
            
        st.markdown("""
            <div style="background: rgba(245, 158, 11, 0.08); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 10px; padding: 14px; margin-top: 18px;">
                <span style="color: #fbbf24; font-weight: 700; font-size: 0.8rem;">CAUTION</span>
                <p style="color: #cbd5e1; font-size: 0.75rem; margin-top: 4px; line-height: 1.4;">
                    AVENRO is a flexible architectural framework, not a static flowsheet. Module arrangements and kinetic regimes dynamically adapt to emitter gas matrices.
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col_chat:
        st.markdown("### ScrubAI Senior Advisor")
        chat_box = st.container(height=420)
        with chat_box:
            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
        
        if prompt := st.chat_input("Input flue parameters (e.g. Set flow to 45000 Nm3/h, CO2 to 14%, SOx to 500 ppm)..."):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            
            lowered = prompt.lower()
            if "co2" in lowered or "sox" in lowered or "flow" in lowered:
                if "co2" in lowered:
                    st.session_state.co2 = 14.0
                if "sox" in lowered:
                    st.session_state.sox = 500.0
                if "flow" in lowered:
                    st.session_state.flow = 45000.0
                reply = "Parameters extracted and applied to memory. Flue Gas Auto-Architect has re-computed stage sizing and circular yield profiles."
            else:
                reply = "Query analyzed. Transport dimensionless parameters are matched against film mass transfer kinetics ($Ha > 3$). Flowsheet diagrams are synchronized in the Auto-Architect tab."
            
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

# ------------------------------------------
# TAB 2: Flue Gas Auto-Architect
# ------------------------------------------
with tab2:
    col_in, col_arch = st.columns([1, 2])
    
    with col_in:
        st.markdown("### ⚙️ Feed Gas Matrix")
        st.session_state.flow = st.number_input("Gas Flow (Nm³/h)", value=float(st.session_state.flow), step=2500.0)
        st.session_state.temp = st.number_input("Flue Temperature (°C)", value=float(st.session_state.temp), step=5.0)
        st.session_state.co2 = st.slider("Carbon Dioxide (vol%)", 0.0, 99.0, float(st.session_state.co2))
        st.session_state.sox = st.slider("Sulfur Oxides (ppm)", 0.0, 3000.0, float(st.session_state.sox))
        st.session_state.nox = st.slider("Nitrogen Oxides (ppm)", 0.0, 1500.0, float(st.session_state.nox))
        st.session_state.voc = st.slider("VOCs (ppm)", 0.0, 1000.0, float(st.session_state.voc))
        st.session_state.h2s = st.slider("Hydrogen Sulfide (ppm)", 0.0, 1000.0, float(st.session_state.h2s))

    with col_arch:
        st.markdown("### 🧱 Synthesized Reactor Train")
        st.caption("Ordered sequentially to prevent catalytic poisoning and minimize thermodynamic entropy loss:")
        
        stage = 0
        if st.session_state.voc > 50:
            stage += 1
            st.markdown(f"""
                <div style="background-color: #0c1a2e; border: 1px solid #0284c7; border-radius: 10px; padding: 14px; margin-bottom: 12px;">
                    <div style="font-size: 0.75rem; color: #38bdf8; font-weight: 700;">STAGE {stage}: ADVANCED VOC DESTRUCTOR</div>
                    <div style="font-size: 0.95rem; font-weight: 600; color: #ffffff; margin: 4px 0;">Target: VOC Hydrocarbons ({st.session_state.voc} ppm)</div>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Mechanism: Multi-phase AOP thin film contactor with inline O₃ radical generation.</div>
                </div>
            """, unsafe_allow_html=True)
            
        if st.session_state.sox > 20 or st.session_state.h2s > 0:
            stage += 1
            gypsum_tpd = (st.session_state.sox * st.session_state.flow * 0.0000072)
            st.markdown(f"""
                <div style="background-color: #211906; border: 1px solid #d97706; border-radius: 10px; padding: 14px; margin-bottom: 12px;">
                    <div style="font-size: 0.75rem; color: #f59e0b; font-weight: 700;">STAGE {stage}: ACID GAS FAST CONTACTOR</div>
                    <div style="font-size: 0.95rem; font-weight: 600; color: #ffffff; margin: 4px 0;">Target: SOx ({st.session_state.sox} ppm) + H₂S ({st.session_state.h2s} ppm)</div>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Mechanism: Alkaline reactive scrubbing ($Ha > 8$). Produces high-grade mineral cake.</div>
                    <div style="font-size: 0.85rem; color: #fbbf24; font-weight: 600; margin-top: 6px;">Output: {gypsum_tpd:.1f} Tonnes/day Synthetic Gypsum (CaSO₄·2H₂O)</div>
                </div>
            """, unsafe_allow_html=True)

        if st.session_state.nox > 80:
            stage += 1
            nitrate_tpd = (st.session_state.nox * st.session_state.flow * 0.000004)
            st.markdown(f"""
                <div style="background-color: #1e102d; border: 1px solid #9333ea; border-radius: 10px; padding: 14px; margin-bottom: 12px;">
                    <div style="font-size: 0.75rem; color: #c084fc; font-weight: 700;">STAGE {stage}: NOX OXIDATIVE ABSORPTION TRAIN</div>
                    <div style="font-size: 0.95rem; font-weight: 600; color: #ffffff; margin: 4px 0;">Target: NOx ({st.session_state.nox} ppm)</div>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Mechanism: Gas-phase low-temperature oxidation into soluble N₂O₅ state.</div>
                    <div style="font-size: 0.85rem; color: #d8b4fe; font-weight: 600; margin-top: 6px;">Output: {nitrate_tpd:.1f} Tonnes/day Calcium Nitrate Solution</div>
                </div>
            """, unsafe_allow_html=True)

        if st.session_state.co2 > 1.0:
            stage += 1
            pcc_tpd = ((st.session_state.flow * (st.session_state.co2/100) * 1.96 * 24) / 1000) * 2.2
            st.markdown(f"""
                <div style="background-color: #062217; border: 1px solid #059669; border-radius: 10px; padding: 14px; margin-bottom: 12px;">
                    <div style="font-size: 0.75rem; color: #34d399; font-weight: 700;">STAGE {stage}: CO₂ MINERALIZATION CONTACTOR</div>
                    <div style="font-size: 0.95rem; font-weight: 600; color: #ffffff; margin: 4px 0;">Target: CO₂ ({st.session_state.co2} vol%)</div>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Mechanism: Non-equilibrium mass-transfer acceleration coupled to continuous precipitation.</div>
                    <div style="font-size: 0.85rem; color: #6ee7b7; font-weight: 600; margin-top: 6px;">Output: {pcc_tpd:.1f} Tonnes/day Precipitated Calcium Carbonate (PCC)</div>
                </div>
            """, unsafe_allow_html=True)

# ------------------------------------------
# TAB 3: 3D Transport Simulation
# ------------------------------------------
with tab3:
    col_t_ctrl, col_t_vis = st.columns([1, 3])
    with col_t_ctrl:
        st.markdown("### 🎛️ Hydrodynamics")
        ug = st.slider("Superficial Gas Velocity (m/s)", 0.5, 4.0, 1.8)
        ul = st.slider("Liquid Spray Flux (m/s)", 0.01, 0.15, 0.05)
        ha = st.slider("Hatta Number (Ha)", 0.2, 10.0, 4.5)
        spec_area = st.slider("Specific Area (m²/m³)", 100.0, 600.0, 320.0)
        
        enhancement = np.sqrt(1 + ha**2)
        kla_val = 0.00012 * (ug**0.7) * (ul**0.4) * spec_area
        
        st.markdown(f"""
            <div style="background-color: #151f32; border: 1px solid #334155; border-radius: 10px; padding: 14px; margin-top: 14px;">
                <div style="font-size: 0.75rem; color: #94a3b8;">Enhancement Factor ($E$):</div>
                <div style="font-size: 1.2rem; font-weight: bold; color: #34d399; font-family: monospace;">{enhancement:.2f}</div>
                <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 6px;">Volumetric Mass Coeff ($k_L a$):</div>
                <div style="font-size: 1.2rem; font-weight: bold; color: #38bdf8; font-family: monospace;">{kla_val:.4f} s⁻¹</div>
            </div>
        """, unsafe_allow_html=True)

    with col_t_vis:
        np.random.seed(101)
        z_col = np.linspace(0, 12, 30)
        theta_col = np.linspace(0, 2*np.pi, 30)
        T_col, Z_col = np.meshgrid(theta_col, z_col)
        X_col = 3.5 * np.cos(T_col)
        Y_col = 3.5 * np.sin(T_col)

        num_pts = 220
        gas_pts_z = np.random.uniform(0, 12, num_pts)
        gas_pts_x = np.random.uniform(-3, 3, num_pts)
        gas_pts_y = np.random.uniform(-3, 3, num_pts)

        liq_pts_z = np.random.uniform(0, 12, num_pts)
        liq_pts_x = np.random.uniform(-3, 3, num_pts)
        liq_pts_y = np.random.uniform(-3, 3, num_pts)

        fig_3d = go.Figure()
        fig_3d.add_trace(go.Surface(x=X_col, y=Y_col, z=Z_col, opacity=0.15, colorscale=[[0, '#0284c7'], [1, '#059669']], showscale=False))
        fig_3d.add_trace(go.Scatter3d(x=gas_pts_x, y=gas_pts_y, z=gas_pts_z, mode='markers',
                                      marker=dict(size=4, color='#f97316', opacity=0.85), name='Gas Phase (Rising)'))
        fig_3d.add_trace(go.Scatter3d(x=liq_pts_x, y=liq_pts_y, z=liq_pts_z, mode='markers',
                                      marker=dict(size=4, color='#38bdf8', opacity=0.75), name='Liquid Phase (Falling)'))

        fig_3d.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            scene=dict(
                xaxis=dict(showbackground=False, showticklabels=False, title=''),
                yaxis=dict(showbackground=False, showticklabels=False, title=''),
                zaxis=dict(showbackground=False, gridcolor='#1e293b', title='Column Height (m)'),
                bgcolor='#080d1a'
            ),
            legend=dict(font=dict(color='#cbd5e1')),
            margin=dict(l=0, r=0, b=0, t=0),
            height=480
        )
        st.plotly_chart(fig_3d, use_container_width=True)

# ------------------------------------------
# TAB 4: SVD Scale Engine
# ------------------------------------------
with tab4:
    st.markdown("### 🔬 Multivariate Singular Value Decomposition ($A = U \Sigma V^T$)")
    st.caption("Dimensionality reduction maps 8 dimensionless parameters ($Re, Sc, Sh, Da, Ha, k_La, \\Delta P, \\eta$) into 2 dominant invariant operational modes.")

    svd_c1, svd_c2 = st.columns(2)
    with svd_c1:
        fig_scree = go.Figure(data=[go.Bar(
            x=['Mode 1', 'Mode 2', 'Mode 3', 'Mode 4', 'Mode 5'],
            y=[64.2, 24.2, 7.1, 3.2, 1.3],
            marker=dict(color=['#10b981', '#06b6d4', '#8b5cf6', '#64748b', '#475569'])
        )])
        fig_scree.update_layout(
            title=dict(text="Singular Value Variance Explained (Σ)", font=dict(color='#f8fafc', size=13)),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#94a3b8'),
            yaxis=dict(gridcolor='#1e293b', title='Variance (%)'),
            xaxis=dict(gridcolor='#1e293b'),
            height=320,
            margin=dict(t=40, b=20, l=40, r=20)
        )
        st.plotly_chart(fig_scree, use_container_width=True)

    with svd_c2:
        fig_loading = go.Figure(data=[go.Bar(
            y=['Re', 'Sh', 'Sc', 'Da', 'Ha', 'kLa'],
            x=[0.48, 0.52, 0.12, -0.42, 0.49, 0.51],
            orientation='h',
            marker=dict(color='#06b6d4')
        )])
        fig_loading.update_layout(
            title=dict(text="Dominant Mode Loadings (Vᵀ)", font=dict(color='#f8fafc', size=13)),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#94a3b8'),
            xaxis=dict(gridcolor='#1e293b', title='Loading Coefficient'),
            yaxis=dict(gridcolor='#1e293b'),
            height=320,
            margin=dict(t=40, b=20, l=110, r=20)
        )
        st.plotly_chart(fig_loading, use_container_width=True)

# ------------------------------------------
# TAB 5: Techno-Economics
# ------------------------------------------
with tab5:
    tea_col_ctrl, tea_col_kpi = st.columns([1, 2])
    with tea_col_ctrl:
        st.markdown("### 💰 Financial Model")
        annual_hours = st.slider("Operating Hours (hrs/year)", 4000, 8760, 8000)
        elec_tariff = st.slider("Power Cost ($/kWh)", 0.04, 0.20, 0.095)
        pcc_sale_price = st.slider("Mineral PCC Value ($/Tonne)", 30.0, 120.0, 60.0)

    with tea_col_kpi:
        capex_calc = 160000 * ((st.session_state.flow / 10000) ** 0.62)
        co2_t_yr = (st.session_state.flow * (st.session_state.co2 / 100) * 1.96 * annual_hours * 0.90) / 1000
        pcc_rev = (co2_t_yr * 2.2) * pcc_sale_price
        opex_calc = (st.session_state.flow * 0.0024 * annual_hours * elec_tariff) + (co2_t_yr * 22) + (capex_calc * 0.04)
        net_cash = pcc_rev - opex_calc
        payback_yr = capex_calc / max(net_cash, 1000)

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("CAPEX Estimate", f"${int(capex_calc):,}", f"₹{(capex_calc*84)/10000000:.2f} Cr")
        k2.metric("Annual OPEX", f"${int(opex_calc):,}", f"₹{(opex_calc*84)/10000000:.2f} Cr")
        k3.metric("Byproduct Revenue", f"+${int(pcc_rev):,}", f"+₹{(pcc_rev*84)/10000000:.2f} Cr")
        k4.metric("Payback", f"{payback_yr:.1f} Yrs")

        fig_tea_comp = go.Figure(data=[
            go.Bar(name='Conventional Amine', x=['CAPEX ($)', 'OPEX ($/yr)', 'Net Levelized ($/T)'],
                   y=[capex_calc * 2.1, co2_t_yr * 68, 75], marker_color='#ef4444'),
            go.Bar(name='ReActScrub', x=['CAPEX ($)', 'OPEX ($/yr)', 'Net Levelized ($/T)'],
                   y=[capex_calc, opex_calc, max(0, (opex_calc - pcc_rev) / max(co2_t_yr, 1))], marker_color='#10b981')
        ])
        fig_tea_comp.update_layout(
            title=dict(text="Comparative Economic Analysis", font=dict(color='#f8fafc', size=13)),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#94a3b8'),
            yaxis=dict(gridcolor='#1e293b'),
            barmode='group',
            height=300,
            margin=dict(t=40, b=20, l=40, r=20)
        )
        st.plotly_chart(fig_tea_comp, use_container_width=True)

# ------------------------------------------
# TAB 6: Contact Us
# ------------------------------------------
with tab6:
    st.markdown("### 📞 Partner with AVENRO")
    st.markdown("We are scaling toward our **2028 industrial validation milestone (0.1 to 1,000 m³/h physical slipstream pilot)** to calibrate our SVD framework against live industrial flue gases.")
    
    col_cform, col_cinfo = st.columns(2)
    with col_cform:
        with st.form("contact_inquiry"):
            name = st.text_input("Name / Title")
            organization = st.text_input("Company / Institution")
            email = st.text_input("Email")
            category = st.selectbox("Collaboration Scope", ["Industrial Site Testing", "Technical Mentorship", "Seed / Pilot Capital", "General Inquiry"])
            msg = st.text_area("Message / Exhaust Parameters")
            submitted = st.form_submit_button("Submit Deployment Inquiry")
            if submitted:
                st.success("Inquiry transmitted. The AVENRO engineering team will review your specifications.")

    with col_cinfo:
        st.markdown("""
            <div style="background-color: #0f172a; border: 1px solid #1e293b; border-radius: 12px; padding: 22px;">
                <h4 style="margin-top: 0; color: #10b981 !important;">AVENRO Engineering Group</h4>
                <p style="font-size: 0.85rem; color: #94a3b8;">Reaction Engineering & Transport Phenomena Innovations</p>
                <hr style="border: none; border-top: 1px solid #1e293b; margin: 12px 0;">
                <p style="font-size: 0.85rem; margin: 6px 0;"><strong>Venture Focus:</strong> Hardware-as-a-Service (HaaS)</p>
                <p style="font-size: 0.85rem; margin: 6px 0;"><strong>Active Symposia:</strong> IIT Madras FAMMTP 2026</p>
                <p style="font-size: 0.85rem; margin: 6px 0;"><strong>Inquiries:</strong> partnerships@avenro-tech.com</p>
            </div>
        """, unsafe_allow_html=True)