import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from scipy.interpolate import griddata

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="GeoViz Pro", layout="wide", page_icon="🌍")

# CSS Custom untuk sedikit mempercantik tampilan
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# --- JUDUL UTAMA ---
st.title("🌍 3D Reservoir Visualization")
st.markdown("**Interactive Structural Map & Fluid Contact Modeler**")

# --- 1. INISIALISASI SESSION STATE ---
if 'data_points' not in st.session_state:
    st.session_state['data_points'] = []

# --- 2. SIDEBAR KEREN ---
with st.sidebar:
    st.header("🛠️ Panel Input")
    
    # --- BAGIAN A: INPUT DATA ---
    st.markdown("### 📍 Input Koordinat")
    
    with st.form(key='input_form', clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            x_val = st.number_input("X (Timur-Barat)", value=0.0, step=10.0)
        with c2:
            y_val = st.number_input("Y (Utara-Selatan)", value=0.0, step=10.0)
        
        z_val = st.number_input("Z (Kedalaman/Depth)", value=1000.0, step=10.0, help="Makin besar angka, makin dalam")
        
        # Tombol Submit dengan tipe Primary (Warna mencolok)
        submit_button = st.form_submit_button(label='➕ Tambah Titik', type="primary")

    if submit_button:
        st.session_state['data_points'].append({'X': x_val, 'Y': y_val, 'Z': z_val})
        st.toast(f"Titik ({x_val}, {y_val}, {z_val}) berhasil disimpan!", icon='✅')

    # --- BAGIAN B: STATUS DATA ---
    df = pd.DataFrame(st.session_state['data_points'])
    
    if not df.empty:
        st.divider()
        st.markdown("### 📊 Status Data")
        
        # Tampilkan Metrics Sederhana
        m1, m2 = st.columns(2)
        m1.metric("Total Titik", len(df))
        m2.metric("Kedalaman Max", f"{df['Z'].max()} m")
        
        # --- BAGIAN C: KONTAK FLUIDA (Hanya muncul jika ada data) ---
        st.divider()
        st.markdown("### 💧 Kontak Fluida")
        
        min_z, max_z = df['Z'].min(), df['Z'].max()
        
        # Input GOC & WOC dengan warna visual
        st.markdown("**:red[Gas-Oil Contact (GOC)]**")
        goc_input = st.number_input("", value=float(min_z + (max_z-min_z)*0.3), key="goc", label_visibility="collapsed")
        
        st.markdown("**:blue[Water-Oil Contact (WOC)]**")
        woc_input = st.number_input("", value=float(min_z + (max_z-min_z)*0.7), key="woc", label_visibility="collapsed")
        
        if goc_input > woc_input:
            st.warning("⚠️ Awas: GOC > WOC!")

    # --- BAGIAN D: UTILITAS (Disembunyikan di Expander) ---
    st.markdown("---")
    with st.expander("⚙️ Pengaturan Data", expanded=False):
        if st.button("🔄 Reset Semua Data"):
            st.session_state['data_points'] = []
            st.rerun()
        
        if st.button("📂 Load Data Demo"):
            st.session_state['data_points'] = [
                {'X': 100, 'Y': 100, 'Z': 1300}, {'X': 300, 'Y': 100, 'Z': 1300},
                {'X': 100, 'Y': 300, 'Z': 1300}, {'X': 300, 'Y': 300, 'Z': 1300},
                {'X': 200, 'Y': 200, 'Z': 1000}, # Puncak
                {'X': 200, 'Y': 100, 'Z': 1150}, {'X': 200, 'Y': 300, 'Z': 1150},
                {'X': 100, 'Y': 200, 'Z': 1150}, {'X': 300, 'Y': 200, 'Z': 1150},
                {'X': 150, 'Y': 150, 'Z': 1100}, {'X': 250, 'Y': 250, 'Z': 1100},
                {'X': 150, 'Y': 250, 'Z': 1100}, {'X': 250, 'Y': 150, 'Z': 1100}
            ]
            st.rerun()

# --- 3. LOGIC VISUALISASI UTAMA ---
if df.empty:
    st.info("👈 Silakan masukkan data koordinat melalui panel di sebelah kiri.")
    st.image("https://streamlit.io/images/brand/streamlit-mark-color.png", width=100) # Placeholder aja
else:
    # --- PROSES GRIDDATA (Interpolasi) ---
    # Minimal 4 titik untuk kontur yang baik
    if len(df) >= 4:
        grid_x = np.linspace(df['X'].min(), df['X'].max(), 100)
        grid_y = np.linspace(df['Y'].min(), df['Y'].max(), 100)
        grid_x, grid_y = np.meshgrid(grid_x, grid_y)

        try:
            grid_z = griddata((df['X'], df['Y']), df['Z'], (grid_x, grid_y), method='cubic')
        except:
            grid_z = griddata((df['X'], df['Y']), df['Z'], (grid_x, grid_y), method='linear')

        # --- TABS VISUALISASI ---
        tab1, tab2, tab3 = st.tabs(["🗺️ Peta Kontur 2D", "🧊 Model 3D", "📋 Data Mentah"])

        # === TAB 1: 2D ===
        with tab1:
            fig_2d = go.Figure()

            # Layer Kontur
            fig_2d.add_trace(go.Contour(
                z=grid_z, x=np.linspace(df['X'].min(), df['X'].max(), 100),
                y=np.linspace(df['Y'].min(), df['Y'].max(), 100),
                colorscale='Greys', opacity=0.4,
                contours=dict(start=min_z, end=max_z, size=(max_z - min_z)/10, showlabels=True),
                name='Structure'
            ))

            # Layer Titik Fluida
            conditions = [
                (df['Z'] < goc_input),
                (df['Z'] >= goc_input) & (df['Z'] <= woc_input),
                (df['Z'] > woc_input)
            ]
            choices = ['Gas Cap', 'Oil Zone', 'Aquifer']
            colors_map = {'Gas Cap': 'red', 'Oil Zone': 'green', 'Aquifer': 'blue'}
            df['Fluid'] = np.select(conditions, choices, default='Unknown')

            for fluid in choices:
                subset = df[df['Fluid'] == fluid]
                if not subset.empty:
                    fig_2d.add_trace(go.Scatter(
                        x=subset['X'], y=subset['Y'],
                        mode='markers+text', text=subset['Z'].astype(int), textposition="top center",
                        marker=dict(size=12, color=colors_map[fluid], line=dict(width=1, color='black')),
                        name=fluid
                    ))

            fig_2d.update_layout(height=650, margin=dict(l=20, r=20, t=40, b=20),
                                xaxis_title="X Coordinate", yaxis_title="Y Coordinate")
            st.plotly_chart(fig_2d, use_container_width=True)

        # === TAB 2: 3D ===
        with tab2:
            fig_3d = go.Figure()
            
            # Surface Tanah
            fig_3d.add_trace(go.Surface(z=grid_z, x=grid_x, y=grid_y, colorscale='Greys', opacity=0.8, name='Structure'))
            
            # Plane GOC/WOC
            def create_plane(z_lvl, color, name):
                return go.Surface(
                    z=z_lvl * np.ones_like(grid_z), x=grid_x, y=grid_y,
                    colorscale=[[0, color], [1, color]], opacity=0.4, showscale=False, name=name
                )

            fig_3d.add_trace(create_plane(goc_input, 'red', 'GOC'))
            fig_3d.add_trace(create_plane(woc_input, 'blue', 'WOC'))

            # Titik Sumur 3D
            fig_3d.add_trace(go.Scatter3d(
                x=df['X'], y=df['Y'], z=df['Z'], mode='markers',
                marker=dict(size=4, color='black'), name='Wells'
            ))

            fig_3d.update_layout(
                scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Depth', zaxis=dict(autorange="reversed")),
                height=650, margin=dict(l=0, r=0, b=0, t=0)
            )
            st.plotly_chart(fig_3d, use_container_width=True)

        with tab3:
            st.dataframe(df, use_container_width=True)

    else:
        st.warning("⚠️ Data belum cukup untuk membuat kontur. Masukkan minimal 4 titik yang menyebar.")
        st.dataframe(df, use_container_width=True)