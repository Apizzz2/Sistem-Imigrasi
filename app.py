import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Konfigurasi halaman
st.set_page_config(
    page_title="Sistem Analisis Kepuasan Pelayanan Kantor Imigrasi Kelas II TPI Langsa",
    page_icon="🛂",
    layout="wide"
)

# CSS untuk styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f4788;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f4788;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 1.1rem;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🛂 Sistem Analisis Kepuasan Pelayanan Imigrasi</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Kantor Imigrasi - Sistem Terintegrasi</div>', unsafe_allow_html=True)

# Inisialisasi session state
if 'data_responden' not in st.session_state:
    st.session_state.data_responden = pd.DataFrame()

# Sidebar untuk input data
with st.sidebar:
    st.header("📊 Input Data Responden")
    
    with st.form("form_responden"):
        st.subheader("Data Responden Baru")
        
        nama = st.text_input("Nama Responden")
        jenis_kelamin = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
        usia = st.number_input("Usia", min_value=17, max_value=100, value=30)
        jenis_layanan = st.selectbox("Jenis Layanan", 
            ["Paspor Baru", "Perpanjangan Paspor", "Visa", "Izin Tinggal", "Lainnya"])
        
        st.markdown("---")
        st.markdown("**Penilaian (1-5):**")
        st.caption("1=Sangat Tidak Puas, 5=Sangat Puas")
        
        # Aspek penilaian
        tangibles = st.slider("1. Fasilitas Fisik & Kebersihan", 1, 5, 3)
        reliability = st.slider("2. Keandalan & Ketepatan Layanan", 1, 5, 3)
        responsiveness = st.slider("3. Kecepatan Respon Petugas", 1, 5, 3)
        assurance = st.slider("4. Kompetensi & Kesopanan Petugas", 1, 5, 3)
        empathy = st.slider("5. Perhatian Petugas", 1, 5, 3)
        
        waktu_tunggu = st.slider("6. Waktu Tunggu Layanan", 1, 5, 3)
        kemudahan_prosedur = st.slider("7. Kemudahan Prosedur", 1, 5, 3)
        kejelasan_informasi = st.slider("8. Kejelasan Informasi", 1, 5, 3)
        
        kepuasan_keseluruhan = st.slider("Kepuasan Keseluruhan", 1, 5, 3)
        
        saran = st.text_area("Saran & Masukan (Opsional)")
        
        submitted = st.form_submit_button("✅ Simpan Data", use_container_width=True)
        
        if submitted:
            if nama:
                data_baru = {
                    'Tanggal': datetime.now().strftime("%Y-%m-%d %H:%M"),
                    'Nama': nama,
                    'Jenis Kelamin': jenis_kelamin,
                    'Usia': usia,
                    'Jenis Layanan': jenis_layanan,
                    'Fasilitas Fisik': tangibles,
                    'Keandalan': reliability,
                    'Responsivitas': responsiveness,
                    'Jaminan': assurance,
                    'Empati': empathy,
                    'Waktu Tunggu': waktu_tunggu,
                    'Kemudahan Prosedur': kemudahan_prosedur,
                    'Kejelasan Informasi': kejelasan_informasi,
                    'Kepuasan Keseluruhan': kepuasan_keseluruhan,
                    'Saran': saran
                }
                
                if st.session_state.data_responden.empty:
                    st.session_state.data_responden = pd.DataFrame([data_baru])
                else:
                    st.session_state.data_responden = pd.concat([
                        st.session_state.data_responden, 
                        pd.DataFrame([data_baru])
                    ], ignore_index=True)
                
                st.success("✅ Data berhasil disimpan!")
                st.rerun()
            else:
                st.error("Nama responden harus diisi!")
    
    st.markdown("---")
    
    # Upload CSV
    st.subheader("📁 Import Data CSV")
    uploaded_file = st.file_uploader("Upload file CSV", type=['csv'])
    if uploaded_file:
        try:
            df_upload = pd.read_csv(uploaded_file)
            st.session_state.data_responden = df_upload
            st.success(f"✅ {len(df_upload)} data berhasil diimport!")
        except Exception as e:
            st.error(f"Error: {e}")
    
    # Download template dan data
    if not st.session_state.data_responden.empty:
        csv = st.session_state.data_responden.to_csv(index=False)
        st.download_button(
            "💾 Download Data CSV",
            csv,
            "data_kepuasan_imigrasi.csv",
            "text/csv",
            use_container_width=True
        )
    
    if st.button("🗑️ Reset Semua Data", use_container_width=True):
        st.session_state.data_responden = pd.DataFrame()
        st.rerun()

# Main content
if st.session_state.data_responden.empty:
    st.info("👈 Silakan mulai dengan menginput data responden di sidebar atau upload file CSV")
else:
    df = st.session_state.data_responden
    
    # Hitung metrik
    total_responden = len(df)
    rata_rata_kepuasan = df['Kepuasan Keseluruhan'].mean()
    
    # Kategori kepuasan
    def kategori_kepuasan(nilai):
        if nilai >= 4.5:
            return "Sangat Puas"
        elif nilai >= 3.5:
            return "Puas"
        elif nilai >= 2.5:
            return "Cukup Puas"
        elif nilai >= 1.5:
            return "Tidak Puas"
        else:
            return "Sangat Tidak Puas"
    
    # Metrik ringkasan
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Responden", total_responden)
    
    with col2:
        st.metric("Rata-rata Kepuasan", f"{rata_rata_kepuasan:.2f}/5.0")
    
    with col3:
        puas = len(df[df['Kepuasan Keseluruhan'] >= 4])
        persentase_puas = (puas/total_responden*100)
        st.metric("Tingkat Kepuasan", f"{persentase_puas:.1f}%")
    
    with col4:
        st.metric("Status", kategori_kepuasan(rata_rata_kepuasan))
    
    st.markdown("---")
    
    # Tab untuk 3 laporan
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Analisis Tingkat Kepuasan",
        "📈 Pengaruh Kualitas Layanan",
        "📋 Evaluasi Pelayanan Administrasi",
        "📑 Data Mentah"
    ])
    
    with tab1:
        st.header("Analisis Tingkat Kepuasan Masyarakat terhadap Kualitas Pelayanan")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribusi kepuasan keseluruhan
            fig_dist = px.histogram(
                df, 
                x='Kepuasan Keseluruhan',
                nbins=5,
                title='Distribusi Tingkat Kepuasan Keseluruhan',
                labels={'Kepuasan Keseluruhan': 'Skor Kepuasan', 'count': 'Jumlah Responden'},
                color_discrete_sequence=['#1f4788']
            )
            fig_dist.update_layout(showlegend=False)
            st.plotly_chart(fig_dist, use_container_width=True)
            
            # Kepuasan per jenis layanan
            kepuasan_layanan = df.groupby('Jenis Layanan')['Kepuasan Keseluruhan'].mean().sort_values()
            fig_layanan = px.bar(
                kepuasan_layanan,
                orientation='h',
                title='Rata-rata Kepuasan per Jenis Layanan',
                labels={'value': 'Rata-rata Kepuasan', 'index': 'Jenis Layanan'},
                color=kepuasan_layanan.values,
                color_continuous_scale='RdYlGn'
            )
            st.plotly_chart(fig_layanan, use_container_width=True)
        
        with col2:
            # Pie chart kategori kepuasan
            df['Kategori'] = df['Kepuasan Keseluruhan'].apply(
                lambda x: 'Sangat Puas' if x >= 4.5 else 
                         'Puas' if x >= 3.5 else 
                         'Cukup Puas' if x >= 2.5 else 
                         'Tidak Puas'
            )
            kategori_counts = df['Kategori'].value_counts()
            
            fig_pie = px.pie(
                values=kategori_counts.values,
                names=kategori_counts.index,
                title='Proporsi Kategori Kepuasan',
                color_discrete_sequence=px.colors.sequential.Blues_r
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            
            # Demografi
            fig_demo = px.bar(
                df['Jenis Kelamin'].value_counts(),
                title='Demografi Responden',
                labels={'value': 'Jumlah', 'index': 'Jenis Kelamin'},
                color_discrete_sequence=['#1f4788', '#4a90e2']
            )
            st.plotly_chart(fig_demo, use_container_width=True)
        
        st.markdown("---")
        
        # Analisis deskriptif
        st.subheader("📊 Statistik Deskriptif")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Rata-rata per Aspek:**")
            aspek_cols = ['Fasilitas Fisik', 'Keandalan', 'Responsivitas', 
                         'Jaminan', 'Empati', 'Waktu Tunggu', 
                         'Kemudahan Prosedur', 'Kejelasan Informasi']
            for col in aspek_cols:
                rata = df[col].mean()
                st.write(f"• {col}: **{rata:.2f}**")
        
        with col2:
            st.markdown("**Standar Deviasi:**")
            for col in aspek_cols:
                std = df[col].std()
                st.write(f"• {col}: **{std:.2f}**")
        
        with col3:
            st.markdown("**Min - Max:**")
            for col in aspek_cols:
                min_val = df[col].min()
                max_val = df[col].max()
                st.write(f"• {col}: **{min_val} - {max_val}**")
    
    with tab2:
        st.header("Pengaruh Kualitas Pelayanan terhadap Kepuasan Masyarakat")
        
        # Radar chart untuk dimensi ServQual
        aspek_servqual = ['Fasilitas Fisik', 'Keandalan', 'Responsivitas', 'Jaminan', 'Empati']
        rata_servqual = [df[col].mean() for col in aspek_servqual]
        
        fig_radar = go.Figure()
        
        fig_radar.add_trace(go.Scatterpolar(
            r=rata_servqual,
            theta=aspek_servqual,
            fill='toself',
            name='Rata-rata Skor',
            line_color='#1f4788'
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 5])
            ),
            showlegend=True,
            title='Analisis Dimensi Kualitas Pelayanan (ServQual)'
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Korelasi
            st.subheader("📊 Analisis Korelasi")
            
            aspek_all = ['Fasilitas Fisik', 'Keandalan', 'Responsivitas', 
                        'Jaminan', 'Empati', 'Waktu Tunggu', 
                        'Kemudahan Prosedur', 'Kejelasan Informasi']
            
            korelasi_data = []
            for aspek in aspek_all:
                korrel = df[aspek].corr(df['Kepuasan Keseluruhan'])
                korelasi_data.append({'Aspek': aspek, 'Korelasi': korrel})
            
            df_korelasi = pd.DataFrame(korelasi_data).sort_values('Korelasi', ascending=False)
            
            fig_korelasi = px.bar(
                df_korelasi,
                x='Korelasi',
                y='Aspek',
                orientation='h',
                title='Korelasi Aspek Layanan dengan Kepuasan Keseluruhan',
                color='Korelasi',
                color_continuous_scale='RdYlGn',
                range_color=[0, 1]
            )
            st.plotly_chart(fig_korelasi, use_container_width=True)
        
        with col2:
            # Scatter plot pengaruh
            st.subheader("📈 Visualisasi Pengaruh")
            
            aspek_pilihan = st.selectbox(
                "Pilih Aspek untuk Analisis Scatter:",
                aspek_all
            )
            
            fig_scatter = px.scatter(
                df,
                x=aspek_pilihan,
                y='Kepuasan Keseluruhan',
                title=f'Pengaruh {aspek_pilihan} terhadap Kepuasan',
                trendline='ols',
                labels={aspek_pilihan: f'Skor {aspek_pilihan}', 
                       'Kepuasan Keseluruhan': 'Skor Kepuasan Keseluruhan'},
                color_discrete_sequence=['#1f4788']
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
            
            # Tabel korelasi
            st.markdown("**Tabel Korelasi:**")
            st.dataframe(
                df_korelasi.style.background_gradient(cmap='RdYlGn', subset=['Korelasi']),
                use_container_width=True
            )
        
        # Gap Analysis
        st.markdown("---")
        st.subheader("📉 Gap Analysis (Harapan vs Realita)")
        
        st.info("💡 Asumsi: Harapan masyarakat adalah skor sempurna (5.0)")
        
        gap_data = []
        for aspek in aspek_all:
            realisasi = df[aspek].mean()
            harapan = 5.0
            gap = realisasi - harapan
            gap_data.append({
                'Aspek': aspek,
                'Harapan': harapan,
                'Realisasi': realisasi,
                'Gap': gap,
                'Gap %': (gap/harapan)*100
            })
        
        df_gap = pd.DataFrame(gap_data)
        
        fig_gap = go.Figure()
        
        fig_gap.add_trace(go.Bar(
            name='Harapan',
            x=df_gap['Aspek'],
            y=df_gap['Harapan'],
            marker_color='lightblue'
        ))
        
        fig_gap.add_trace(go.Bar(
            name='Realisasi',
            x=df_gap['Aspek'],
            y=df_gap['Realisasi'],
            marker_color='#1f4788'
        ))
        
        fig_gap.update_layout(
            title='Perbandingan Harapan vs Realisasi',
            barmode='group',
            xaxis_tickangle=-45
        )
        
        st.plotly_chart(fig_gap, use_container_width=True)
        
        st.dataframe(
            df_gap.style.format({
                'Harapan': '{:.2f}',
                'Realisasi': '{:.2f}',
                'Gap': '{:.2f}',
                'Gap %': '{:.1f}%'
            }).background_gradient(cmap='RdYlGn_r', subset=['Gap']),
            use_container_width=True
        )
    
    with tab3:
        st.header("Evaluasi Kepuasan Masyarakat terhadap Pelayanan Administrasi Keimigrasian")
        
        # Fokus pada aspek administratif
        aspek_admin = ['Waktu Tunggu', 'Kemudahan Prosedur', 'Kejelasan Informasi', 'Keandalan']
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Box plot
            fig_box = go.Figure()
            
            for aspek in aspek_admin:
                fig_box.add_trace(go.Box(
                    y=df[aspek],
                    name=aspek,
                    boxmean='sd'
                ))
            
            fig_box.update_layout(
                title='Distribusi Penilaian Aspek Administrasi',
                yaxis_title='Skor',
                showlegend=True
            )
            
            st.plotly_chart(fig_box, use_container_width=True)
            
            # Tren per layanan
            st.subheader("📊 Kepuasan per Jenis Layanan")
            
            df_layanan = df.groupby('Jenis Layanan')[aspek_admin + ['Kepuasan Keseluruhan']].mean()
            
            st.dataframe(
                df_layanan.style.format('{:.2f}').background_gradient(cmap='RdYlGn', axis=0),
                use_container_width=True
            )
        
        with col2:
            # Heatmap
            correlation_matrix = df[aspek_admin + ['Kepuasan Keseluruhan']].corr()
            
            fig_heatmap = px.imshow(
                correlation_matrix,
                title='Matriks Korelasi Aspek Administrasi',
                color_continuous_scale='RdYlGn',
                aspect='auto',
                labels=dict(color="Korelasi")
            )
            
            st.plotly_chart(fig_heatmap, use_container_width=True)
            
            # Line chart tren
            st.subheader("📈 Tren Penilaian Administrasi")
            
            df['Tanggal_Parse'] = pd.to_datetime(df['Tanggal'])
            df_sorted = df.sort_values('Tanggal_Parse')
            
            fig_tren = go.Figure()
            
            for aspek in aspek_admin:
                fig_tren.add_trace(go.Scatter(
                    x=df_sorted['Tanggal_Parse'],
                    y=df_sorted[aspek],
                    mode='lines+markers',
                    name=aspek
                ))
            
            fig_tren.update_layout(
                title='Tren Penilaian dari Waktu ke Waktu',
                xaxis_title='Tanggal',
                yaxis_title='Skor'
            )
            
            st.plotly_chart(fig_tren, use_container_width=True)
        
        # Rekomendasi
        st.markdown("---")
        st.subheader("💡 Rekomendasi Perbaikan")
        
        # Identifikasi aspek terlemah
        rata_aspek_admin = {aspek: df[aspek].mean() for aspek in aspek_admin}
        aspek_terlemah = min(rata_aspek_admin, key=rata_aspek_admin.get)
        aspek_terkuat = max(rata_aspek_admin, key=rata_aspek_admin.get)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.error(f"**⚠️ Aspek yang Perlu Ditingkatkan:**")
            st.write(f"• **{aspek_terlemah}**: {rata_aspek_admin[aspek_terlemah]:.2f}/5.0")
            
            if aspek_terlemah == 'Waktu Tunggu':
                st.write("  - Tambah loket layanan")
                st.write("  - Implementasi sistem antrian online")
                st.write("  - Optimalkan proses verifikasi dokumen")
            elif aspek_terlemah == 'Kemudahan Prosedur':
                st.write("  - Sederhanakan alur prosedur")
                st.write("  - Buat panduan visual yang jelas")
                st.write("  - Tingkatkan digitalisasi layanan")
            elif aspek_terlemah == 'Kejelasan Informasi':
                st.write("  - Perbaiki signage dan papan informasi")
                st.write("  - Latih petugas informasi")
                st.write("  - Lengkapi website dengan FAQ")
        
        with col2:
            st.success(f"**✅ Aspek yang Sudah Baik:**")
            st.write(f"• **{aspek_terkuat}**: {rata_aspek_admin[aspek_terkuat]:.2f}/5.0")
            st.write("  - Pertahankan standar layanan")
            st.write("  - Jadikan best practice untuk aspek lain")
            st.write("  - Dokumentasi prosedur yang berhasil")
        
        # Saran responden
        if 'Saran' in df.columns and df['Saran'].notna().any():
            st.markdown("---")
            st.subheader("💬 Saran dari Responden")
            
            saran_list = df[df['Saran'].notna() & (df['Saran'] != '')]['Saran'].tolist()
            
            if saran_list:
                for i, saran in enumerate(saran_list[-10:], 1):  # Tampilkan 10 saran terakhir
                    st.write(f"{i}. {saran}")
            else:
                st.info("Belum ada saran dari responden")
    
    with tab4:
        st.header("📑 Data Mentah Responden")
        
        # Filter
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filter_layanan = st.multiselect(
                "Filter Jenis Layanan",
                options=df['Jenis Layanan'].unique(),
                default=df['Jenis Layanan'].unique()
            )
        
        with col2:
            filter_gender = st.multiselect(
                "Filter Jenis Kelamin",
                options=df['Jenis Kelamin'].unique(),
                default=df['Jenis Kelamin'].unique()
            )
        
        with col3:
            min_kepuasan = st.slider(
                "Minimal Kepuasan",
                1, 5, 1
            )
        
        # Terapkan filter
        df_filtered = df[
            (df['Jenis Layanan'].isin(filter_layanan)) &
            (df['Jenis Kelamin'].isin(filter_gender)) &
            (df['Kepuasan Keseluruhan'] >= min_kepuasan)
        ]
        
        st.write(f"Menampilkan {len(df_filtered)} dari {len(df)} data")
        
        # Tampilkan data
        st.dataframe(
            df_filtered.style.background_gradient(
                cmap='RdYlGn',
                subset=['Kepuasan Keseluruhan']
            ),
            use_container_width=True,
            height=400
        )
        
        # Statistik ringkas
        st.markdown("---")
        st.subheader("📊 Statistik Data yang Ditampilkan")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Jumlah Data", len(df_filtered))
        
        with col2:
            st.metric("Rata-rata Kepuasan", f"{df_filtered['Kepuasan Keseluruhan'].mean():.2f}")
        
        with col3:
            st.metric("Kepuasan Tertinggi", f"{df_filtered['Kepuasan Keseluruhan'].max():.2f}")
        
        with col4:
            st.metric("Kepuasan Terendah", f"{df_filtered['Kepuasan Keseluruhan'].min():.2f}")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p><strong>Sistem Analisis Kepuasan Pelayanan Imigrasi</strong></p>
        <p>Sistem Terintegrasi Kepuasan Masyarakat</p>
    </div>
""", unsafe_allow_html=True)