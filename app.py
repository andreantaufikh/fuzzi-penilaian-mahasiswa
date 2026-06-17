import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import io

# Set Page Config
st.set_page_config(
    page_title="Fuzzy Student Grading - Case 1",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Design
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Header card styling */
    .header-card {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 16px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        margin-bottom: 2rem;
    }
    
    /* Section card styling */
    .content-card {
        background-color: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        margin-bottom: 1.5rem;
        border: 1px solid #e5e7eb;
    }
    
    /* Metric styling */
    .metric-container {
        display: flex;
        justify-content: space-around;
        gap: 1rem;
        margin-top: 1rem;
    }
    
    .metric-card {
        flex: 1;
        background-color: #f3f4f6;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        border-top: 5px solid #3b82f6;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    
    .metric-title {
        font-size: 0.875rem;
        color: #4b5563;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: #1f2937;
    }
    
    /* Formula card */
    .formula-card {
        background-color: #f9fafb;
        border-left: 4px solid #10b981;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        font-family: monospace;
    }
</style>
""", unsafe_allow_html=True)

# Fuzzy Membership Functions
def fuzzify_rendah(x):
    if x <= 40:
        return 1.0
    elif 40 < x < 60:
        return (60.0 - x) / 20.0
    else:
        return 0.0

def fuzzify_sedang(x):
    if x <= 40 or x >= 80:
        return 0.0
    elif 40 < x < 60:
        return (x - 40.0) / 20.0
    elif 60 <= x < 80:
        return (80.0 - x) / 20.0
    else:
        return 0.0

def fuzzify_tinggi(x):
    if x <= 60:
        return 0.0
    elif 60 < x < 80:
        return (x - 60.0) / 20.0
    else:
        return 1.0

# Textual Explanation Generators for Step-by-Step UI
def get_explanation_rendah(x):
    if x <= 40:
        return rf"\mu_{{\text{{Rendah}}}}({x}) = 1 \quad \text{{karena }} x \le 40"
    elif 40 < x < 60:
        return rf"\mu_{{\text{{Rendah}}}}({x}) = \frac{{60 - {x}}}{{60 - 40}} = \frac{{{60 - x}}}{{20}} = {fuzzify_rendah(x):.4f}"
    else:
        return rf"\mu_{{\text{{Rendah}}}}({x}) = 0 \quad \text{{karena }} x \ge 60"

def get_explanation_sedang(x):
    if x <= 40:
        return rf"\mu_{{\text{{Sedang}}}}({x}) = 0 \quad \text{{karena }} x \le 40"
    elif 40 < x < 60:
        return rf"\mu_{{\text{{Sedang}}}}({x}) = \frac{{{x} - 40}}{{60 - 40}} = \frac{{{x - 40}}}{{20}} = {fuzzify_sedang(x):.4f}"
    elif 60 <= x < 80:
        return rf"\mu_{{\text{{Sedang}}}}({x}) = \frac{{80 - {x}}}{{80 - 60}} = \frac{{{80 - x}}}{{20}} = {fuzzify_sedang(x):.4f}"
    else:
        return rf"\mu_{{\text{{Sedang}}}}({x}) = 0 \quad \text{{karena }} x \ge 80"

def get_explanation_tinggi(x):
    if x <= 60:
        return rf"\mu_{{\text{{Tinggi}}}}({x}) = 0 \quad \text{{karena }} x \le 60"
    elif 60 < x < 80:
        return rf"\mu_{{\text{{Tinggi}}}}({x}) = \frac{{{x} - 60}}{{80 - 60}} = \frac{{{x - 60}}}{{20}} = {fuzzify_tinggi(x):.4f}"
    else:
        return rf"\mu_{{\text{{Tinggi}}}}({x}) = 1 \quad \text{{karena }} x \ge 80"

# Dominant class determination
def dapatkan_status(r, s, t):
    max_val = max(r, s, t)
    if max_val == 0:
        return "Tidak Terdefinisi"
    
    kategori = []
    if r == max_val:
        kategori.append("Rendah")
    if s == max_val:
        kategori.append("Sedang")
    if t == max_val:
        kategori.append("Tinggi")
        
    return " & ".join(kategori)

# Plotly Membership Graph
def create_membership_plot(highlight_x=None):
    x_vals = np.linspace(0, 100, 500)
    y_rendah = [fuzzify_rendah(x) for x in x_vals]
    y_sedang = [fuzzify_sedang(x) for x in x_vals]
    y_tinggi = [fuzzify_tinggi(x) for x in x_vals]
    
    fig = go.Figure()
    
    # Add traces
    fig.add_trace(go.Scatter(x=x_vals, y=y_rendah, name='Rendah', line=dict(color='#EF4444', width=3)))
    fig.add_trace(go.Scatter(x=x_vals, y=y_sedang, name='Sedang', line=dict(color='#F59E0B', width=3)))
    fig.add_trace(go.Scatter(x=x_vals, y=y_tinggi, name='Tinggi', line=dict(color='#10B981', width=3)))
    
    if highlight_x is not None:
        r = fuzzify_rendah(highlight_x)
        s = fuzzify_sedang(highlight_x)
        t = fuzzify_tinggi(highlight_x)
        
        # Vertical line indicating the score
        fig.add_shape(
            type="line", x0=highlight_x, y0=0, x1=highlight_x, y1=1,
            line=dict(color="#1E3A8A", width=2, dash="dash")
        )
        
        # Markers for intersections
        if r > 0:
            fig.add_trace(go.Scatter(x=[highlight_x], y=[r], mode='markers', marker=dict(color='#EF4444', size=10), showlegend=False))
        if s > 0:
            fig.add_trace(go.Scatter(x=[highlight_x], y=[s], mode='markers', marker=dict(color='#F59E0B', size=10), showlegend=False))
        if t > 0:
            fig.add_trace(go.Scatter(x=[highlight_x], y=[t], mode='markers', marker=dict(color='#10B981', size=10), showlegend=False))
            
    fig.update_layout(
        title='Grafik Fungsi Keanggotaan Logika Fuzzy (Nilai Ujian)',
        xaxis_title='Nilai Ujian (Domain: 0 - 100)',
        yaxis_title='Derajat Keanggotaan μ(x)',
        yaxis=dict(range=[-0.05, 1.05]),
        hovermode="x unified",
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=40, r=40, t=50, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#F3F4F6')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#F3F4F6')
    
    return fig

# Title Banner
st.markdown("""
<div class="header-card">
    <h1 style='margin:0; font-size:2.5rem; font-weight:800; letter-spacing:-0.5px;'>🎓 Implementasi Logika Fuzzy - Kasus 1</h1>
    <p style='margin:8px 0 0 0; font-size:1.1rem; opacity:0.9;'>Sistem Penilaian Derajat Keanggotaan Mahasiswa Berdasarkan Nilai Ujian</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.markdown("<h2 style='text-align: center; color: #1E3A8A;'>Menu Navigasi</h2>", unsafe_allow_html=True)
page = st.sidebar.radio(
    "Pilih Halaman:",
    ["📖 Teori & Konsep", "👤 Perhitungan Individu", "👥 Data Kelompok (Tabel & Bulk)"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
**Detail Kasus 1:**
- **Input:** Nilai Ujian
- **Output:** Rendah, Sedang, Tinggi
- **Domain:** 0 s.d 100

**Dosen Pengampu:**
- Pak Indrawan
""")

# PAGE 1: THEORY & CONCEPTS
if page == "📖 Teori & Konsep":
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.subheader("Representasi Fungsi Keanggotaan")
    st.write("Fungsi keanggotaan fuzzy digunakan untuk mendefinisikan derajat keanggotaan suatu nilai ujian ke dalam tiga kategori: **Rendah**, **Sedang**, dan **Tinggi**.")
    
    # Render Plotly Graph
    fig = create_membership_plot()
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Formulas section
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.subheader("Rumus Matematis Fungsi Keanggotaan")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<h4 style='color: #EF4444;'>1. Kategori Rendah</h4>", unsafe_allow_html=True)
        st.latex(r"""
        \mu_{\text{Rendah}}(x) = \begin{cases} 
        1, & x \le 40 \\
        \frac{60 - x}{60 - 40}, & 40 < x < 60 \\
        0, & x \ge 60
        \end{cases}
        """)
        
    with col2:
        st.markdown("<h4 style='color: #F59E0B;'>2. Kategori Sedang</h4>", unsafe_allow_html=True)
        st.latex(r"""
        \mu_{\text{Sedang}}(x) = \begin{cases}
        0, & x \le 40 \text{ atau } x \ge 80 \\
        \frac{x - 40}{60 - 40}, & 40 < x < 60 \\
        \frac{80 - x}{80 - 60}, & 60 \le x < 80
        \end{cases}
        """)
        
    with col3:
        st.markdown("<h4 style='color: #10B981;'>3. Kategori Tinggi</h4>", unsafe_allow_html=True)
        st.latex(r"""
        \mu_{\text{Tinggi}}(x) = \begin{cases}
        0, & x \le 60 \\
        \frac{x - 60}{80 - 60}, & 60 < x < 80 \\
        1, & x \ge 80
        \end{cases}
        """)
        
    st.markdown("</div>", unsafe_allow_html=True)

# PAGE 2: INDIVIDUAL CALCULATION
elif page == "👤 Perhitungan Individu":
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.subheader("Uji Perhitungan Individu")
    st.write("Masukkan nama dan nilai ujian mahasiswa di bawah ini untuk melihat hasil perhitungan derajat keanggotaan fuzzy secara detail.")
    
    col_input1, col_input2 = st.columns(2)
    with col_input1:
        nama_mhs = st.text_input("Nama Mahasiswa:", "Ahmad Fauzi")
    with col_input2:
        nilai_mhs = st.slider("Nilai Ujian:", min_value=0, max_value=100, value=55)
        
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Calculate
    r = fuzzify_rendah(nilai_mhs)
    s = fuzzify_sedang(nilai_mhs)
    t = fuzzify_tinggi(nilai_mhs)
    status = dapatkan_status(r, s, t)
    
    # Display results
    col_res1, col_res2 = st.columns([3, 2])
    
    with col_res1:
        st.markdown("<div class='content-card'>", unsafe_allow_html=True)
        st.subheader(f"Hasil Analisis: {nama_mhs}")
        
        # Metrics Row
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-card" style="border-top-color: #EF4444;">
                <div class="metric-title">Rendah μ(x)</div>
                <div class="metric-value">{r:.4f}</div>
            </div>
            <div class="metric-card" style="border-top-color: #F59E0B;">
                <div class="metric-title">Sedang μ(x)</div>
                <div class="metric-value">{s:.4f}</div>
            </div>
            <div class="metric-card" style="border-top-color: #10B981;">
                <div class="metric-title">Tinggi μ(x)</div>
                <div class="metric-value">{t:.4f}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="margin-top: 1.5rem; padding: 1rem; background-color: #eff6ff; border-radius: 8px; border-left: 5px solid #2563eb;">
            <strong>Interpretasi Hasil:</strong> Kategori Dominan untuk <strong>{nama_mhs}</strong> dengan Nilai <strong>{nilai_mhs}</strong> adalah <strong>{status}</strong>.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Step-by-Step explanation
        st.markdown("<div class='content-card'>", unsafe_allow_html=True)
        st.subheader("Langkah Perhitungan (Traceability)")
        
        st.write("Berikut adalah proses substitusi nilai ke dalam rumus fungsi keanggotaan:")
        
        st.markdown("**1. Kategori Rendah:**")
        st.latex(get_explanation_rendah(nilai_mhs))
        
        st.markdown("**2. Kategori Sedang:**")
        st.latex(get_explanation_sedang(nilai_mhs))
        
        st.markdown("**3. Kategori Tinggi:**")
        st.latex(get_explanation_tinggi(nilai_mhs))
        
        st.markdown("</div>", unsafe_allow_html=True)

    with col_res2:
        st.markdown("<div class='content-card'>", unsafe_allow_html=True)
        st.subheader("Visualisasi Posisi Nilai")
        # Graph with highlighted line
        fig = create_membership_plot(highlight_x=nilai_mhs)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# PAGE 3: GROUP DATA & BULK TABLE
elif page == "👥 Data Kelompok (Tabel & Bulk)":
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.subheader("Pengelolaan Data Mahasiswa")
    st.write("Di halaman ini, Anda dapat mengelola banyak data mahasiswa sekaligus. Anda bisa mengedit tabel di bawah ini, mengunduh hasilnya, atau mengunggah data baru menggunakan file CSV.")
    
    # Template Data
    default_data = pd.DataFrame({
        "Nama Mahasiswa": ["Andi Wijaya", "Budi Santoso", "Citra Lestari", "Dewi Sartika", "Eko Prasetyo", "Fahri Hamzah", "Gita Gutawa", "Hendra Wijaya"],
        "Nilai Ujian": [35, 45, 58, 60, 72, 85, 95, 50]
    })
    
    # Initialize session state for data
    if "student_data" not in st.session_state:
        st.session_state.student_data = default_data.copy()
        
    # Option to upload CSV
    uploaded_file = st.file_uploader("Unggah File CSV (Kolom: Nama Mahasiswa, Nilai Ujian)", type=["csv"])
    if uploaded_file is not None:
        try:
            uploaded_df = pd.read_csv(uploaded_file)
            # Validation
            if "Nama Mahasiswa" in uploaded_df.columns and "Nilai Ujian" in uploaded_df.columns:
                st.session_state.student_data = uploaded_df[["Nama Mahasiswa", "Nilai Ujian"]].dropna()
                st.success("File CSV berhasil dimuat!")
            else:
                st.error("Kolom CSV harus mengandung 'Nama Mahasiswa' dan 'Nilai Ujian'")
        except Exception as e:
            st.error(f"Gagal memuat file CSV: {str(e)}")
            
    # Add new record form
    with st.expander("➕ Tambah Data Mahasiswa Manual"):
        with st.form("tambah_mhs_form", clear_on_submit=True):
            col_add1, col_add2 = st.columns(2)
            with col_add1:
                new_nama = st.text_input("Nama Mahasiswa Baru:")
            with col_add2:
                new_nilai = st.number_input("Nilai Ujian:", min_value=0, max_value=100, value=70)
            
            submit_btn = st.form_submit_button("Tambah Mahasiswa")
            if submit_btn:
                if new_nama.strip() == "":
                    st.warning("Nama mahasiswa tidak boleh kosong!")
                else:
                    new_row = pd.DataFrame({"Nama Mahasiswa": [new_nama], "Nilai Ujian": [new_nilai]})
                    st.session_state.student_data = pd.concat([st.session_state.student_data, new_row], ignore_index=True)
                    st.success(f"Mahasiswa {new_nama} berhasil ditambahkan!")
                    st.rerun()

    # Reset to default button
    if st.button("🔄 Reset ke Data Default"):
        st.session_state.student_data = default_data.copy()
        st.success("Data berhasil direset!")
        st.rerun()
        
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Table & Calculations
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.subheader("Tabel Data dan Perhitungan Derajat Keanggotaan Fuzzy")
    st.write("Silakan klik dua kali pada sel tabel untuk mengedit nilai secara langsung.")
    
    # Edit data in interactive table
    edited_df = st.data_editor(
        st.session_state.student_data,
        num_rows="dynamic",
        key="editor",
        use_container_width=True
    )
    
    # Save the edits back to session state
    if not edited_df.equals(st.session_state.student_data):
        st.session_state.student_data = edited_df
        st.rerun()
        
    # Process calculations
    if not st.session_state.student_data.empty:
        df_results = st.session_state.student_data.copy()
        
        # Apply fuzzification
        df_results["μ Rendah"] = df_results["Nilai Ujian"].apply(fuzzify_rendah)
        df_results["μ Sedang"] = df_results["Nilai Ujian"].apply(fuzzify_sedang)
        df_results["μ Tinggi"] = df_results["Nilai Ujian"].apply(fuzzify_tinggi)
        
        # Add status column
        df_results["Kategori Dominan"] = df_results.apply(
            lambda r: dapatkan_status(r["μ Rendah"], r["μ Sedang"], r["μ Tinggi"]), axis=1
        )
        
        # Show output table
        st.dataframe(
            df_results.style.format({
                "μ Rendah": "{:.4f}",
                "μ Sedang": "{:.4f}",
                "μ Tinggi": "{:.4f}"
            }),
            use_container_width=True
        )
        
        # Download options
        csv_buffer = io.StringIO()
        df_results.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()
        
        st.download_button(
            label="📥 Unduh Hasil Penilaian (CSV)",
            data=csv_data,
            file_name="hasil_penilaian_fuzzy.csv",
            mime="text/csv"
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Summary & Charts
        st.markdown("<div class='content-card'>", unsafe_allow_html=True)
        st.subheader("Statistik & Distribusi Hasil Penilaian")
        
        # Calculate summary counts based on dominant category
        flat_categories = []
        for cat in df_results["Kategori Dominan"]:
            parts = cat.split(" & ")
            flat_categories.extend(parts)
            
        cat_counts = pd.Series(flat_categories).value_counts()
        
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            # Distribution Bar Chart
            fig_bar = go.Figure(data=[
                go.Bar(
                    x=cat_counts.index, 
                    y=cat_counts.values,
                    marker_color=['#F59E0B', '#EF4444', '#10B981'],
                    text=cat_counts.values,
                    textposition='auto'
                )
            ])
            fig_bar.update_layout(
                title="Jumlah Mahasiswa Per Kategori Dominan",
                xaxis_title="Kategori",
                yaxis_title="Jumlah Mahasiswa",
                plot_bgcolor="white",
                paper_bgcolor="white"
            )
            fig_bar.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#F3F4F6')
            st.plotly_chart(fig_bar, use_container_width=True)
            
        with col_chart2:
            # Scatter Plot: Nilai vs Membership
            fig_scatter = go.Figure()
            
            # Map colors
            fig_scatter.add_trace(go.Scatter(
                x=df_results["Nilai Ujian"],
                y=df_results["μ Rendah"],
                mode='markers',
                name='μ Rendah',
                marker=dict(color='#EF4444', size=10, symbol='circle'),
                text=df_results["Nama Mahasiswa"]
            ))
            fig_scatter.add_trace(go.Scatter(
                x=df_results["Nilai Ujian"],
                y=df_results["μ Sedang"],
                mode='markers',
                name='μ Sedang',
                marker=dict(color='#F59E0B', size=10, symbol='square'),
                text=df_results["Nama Mahasiswa"]
            ))
            fig_scatter.add_trace(go.Scatter(
                x=df_results["Nilai Ujian"],
                y=df_results["μ Tinggi"],
                mode='markers',
                name='μ Tinggi',
                marker=dict(color='#10B981', size=10, symbol='diamond'),
                text=df_results["Nama Mahasiswa"]
            ))
            
            fig_scatter.update_layout(
                title="Sebaran Derajat Keanggotaan Berdasarkan Nilai Ujian",
                xaxis_title="Nilai Ujian",
                yaxis_title="Derajat Keanggotaan",
                plot_bgcolor="white",
                paper_bgcolor="white",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            fig_scatter.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#F3F4F6')
            fig_scatter.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#F3F4F6')
            st.plotly_chart(fig_scatter, use_container_width=True)
            
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("Tidak ada data mahasiswa untuk diproses. Silakan tambah data secara manual atau reset ke data default.")
        st.markdown("</div>", unsafe_allow_html=True)
