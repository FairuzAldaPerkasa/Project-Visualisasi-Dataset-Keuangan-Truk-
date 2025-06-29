import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import os
import warnings
warnings.filterwarnings('ignore')

# Konfigurasi halaman
st.set_page_config(
    page_title="Dashboard Analisis Truk Air Isi Ulang",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS yang kompatibel dengan dark mode
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .metric-container {
        background-color: rgba(240, 242, 246, 0.1);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin-bottom: 1rem;
    }
    .insight-box {
        background-color: rgba(225, 245, 254, 0.2);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #0277bd;
        margin: 1rem 0;
    }
    .big-metric {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .highlight {
        background-color: rgba(255, 250, 205, 0.3);
        padding: 0.2rem;
        border-radius: 0.3rem;
    }
    /* Penyesuaian untuk dark mode */
    @media (prefers-color-scheme: dark) {
        .metric-container {
            background-color: rgba(31, 119, 180, 0.2);
        }
        .insight-box {
            background-color: rgba(2, 119, 189, 0.2);
        }
        .big-metric {
            color: #4dabf7;
        }
    }
</style>
""", unsafe_allow_html=True)

# Fungsi untuk load data CSV dari file lokal
@st.cache_data
def load_csv_from_files():
    """Load CSV files from local directory"""
    possible_locations = [
        ('https://raw.githubusercontent.com/FairuzAldaPerkasa/Project-Visualisasi-Dataset-Keuangan-Truk-/refs/heads/main/Dataset/Cleaned/Sheet2_Cleaned.csv', 'https://raw.githubusercontent.com/FairuzAldaPerkasa/Project-Visualisasi-Dataset-Keuangan-Truk-/refs/heads/main/Dataset/Cleaned/Sheet3_Cleaned.csv')
    ]
    
    for sheet2_path, sheet3_path in possible_locations:
        if os.path.exists(sheet2_path) and os.path.exists(sheet3_path):
            try:
                sheet2 = pd.read_csv(sheet2_path)
                sheet3 = pd.read_csv(sheet3_path)
                
                # Konversi kolom tanggal
                for df in [sheet2, sheet3]:
                    if 'Tanggal' in df.columns:
                        df['Tanggal'] = pd.to_datetime(df['Tanggal'], errors='coerce')
                
                return sheet2, sheet3
            except Exception as e:
                st.error(f"Error loading CSV files: {str(e)}")
                return None, None
    
    return None, None

# Fungsi untuk load data dari uploaded files
def load_csv_from_upload(uploaded_sheet2, uploaded_sheet3):
    """Load CSV files from uploaded files"""
    try:
        sheet2 = pd.read_csv(uploaded_sheet2)
        sheet3 = pd.read_csv(uploaded_sheet3)
        
        # Konversi kolom tanggal
        for df in [sheet2, sheet3]:
            if 'Tanggal' in df.columns:
                df['Tanggal'] = pd.to_datetime(df['Tanggal'], errors='coerce')
        
        return sheet2, sheet3
    except Exception as e:
        st.error(f"Error loading uploaded files: {str(e)}")
        return None, None

# Fungsi utama untuk load data
def load_csv_data():
    """Main function to load CSV data"""
    # Coba load dari file lokal dulu
    sheet2, sheet3 = load_csv_from_files()
    
    if sheet2 is not None and sheet3 is not None:
        return sheet2, sheet3
    
    # Jika tidak ada file lokal, tampilkan file uploader
    st.error("File dataset tidak ditemukan. Silakan upload file CSV:")
    
    col1, col2 = st.columns(2)
    with col1:
        uploaded_sheet2 = st.file_uploader("Upload Sheet2_Cleaned.csv:", type=['csv'], key="sheet2")
    with col2:
        uploaded_sheet3 = st.file_uploader("Upload Sheet3_Cleaned.csv:", type=['csv'], key="sheet3")
    
    if uploaded_sheet2 is not None and uploaded_sheet3 is not None:
        return load_csv_from_upload(uploaded_sheet2, uploaded_sheet3)
    
    return None, None

# 1. ANALISIS TRANSAKSI KEUANGAN
def analisis_transaksi_keuangan(df):
    st.subheader("💰 Analisis Transaksi Keuangan")
    
    # Pastikan kolom yang diperlukan ada
    required_cols = ['Tanggal', 'Pemasukan', 'Pengeluaran']
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        st.warning(f"Kolom yang diperlukan tidak ditemukan: {missing_cols}")
        return
    
    # Konversi tanggal dan tambahkan kolom bulan
    df['Tanggal'] = pd.to_datetime(df['Tanggal'])
    df['Bulan'] = df['Tanggal'].dt.to_period('M').astype(str)
    
    # Rekapitulasi keuangan
    total_pemasukan = df['Pemasukan'].sum()
    total_pengeluaran = df['Pengeluaran'].sum()
    laba_bersih = total_pemasukan - total_pengeluaran
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-container">
            <h4>💰 Total Pemasukan</h4>
            <p class="big-metric">Rp {total_pemasukan:,.0f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-container">
            <h4>💸 Total Pengeluaran</h4>
            <p class="big-metric">Rp {total_pengeluaran:,.0f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-container">
            <h4>📈 Laba Bersih</h4>
            <p class="big-metric">Rp {laba_bersih:,.0f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Analisis bulanan
    st.markdown("### 📅 Rekapitulasi Bulanan")
    
    monthly_finance = df.groupby('Bulan').agg({
        'Pemasukan': 'sum',
        'Pengeluaran': 'sum'
    }).reset_index()
    monthly_finance['Laba'] = monthly_finance['Pemasukan'] - monthly_finance['Pengeluaran']
    
    fig = make_subplots(specs=[[{"secondary_y": False}]])
    
    fig.add_trace(
        go.Bar(
            x=monthly_finance['Bulan'],
            y=monthly_finance['Pemasukan'],
            name='Pemasukan',
            marker_color='#1f77b4'
        ),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Bar(
            x=monthly_finance['Bulan'],
            y=monthly_finance['Pengeluaran'],
            name='Pengeluaran',
            marker_color='#ff7f0e'
        ),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(
            x=monthly_finance['Bulan'],
            y=monthly_finance['Laba'],
            name='Laba',
            mode='lines+markers',
            line=dict(color='#2ca02c', width=3)
        ),
        secondary_y=False
    )
    
    fig.update_layout(
        title='Pemasukan vs Pengeluaran per Bulan',
        xaxis_title='Bulan',
        yaxis_title='Jumlah (Rp)',
        barmode='group'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabel detail bulanan
    st.markdown("### 📋 Detail Bulanan")
    monthly_finance_display = monthly_finance.copy()
    monthly_finance_display['Pemasukan'] = monthly_finance_display['Pemasukan'].apply(lambda x: f"Rp {x:,.0f}")
    monthly_finance_display['Pengeluaran'] = monthly_finance_display['Pengeluaran'].apply(lambda x: f"Rp {x:,.0f}")
    monthly_finance_display['Laba'] = monthly_finance_display['Laba'].apply(lambda x: f"Rp {x:,.0f}")
    st.dataframe(monthly_finance_display, use_container_width=True)

# 2. REKAP PENGIRIMAN AIR
def rekap_pengiriman_air(df):
    st.subheader("🚛 Rekap Pengiriman Air")
    
    # Pastikan kolom yang diperlukan ada
    required_cols = ['Tanggal', 'Volume (L)']
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        st.warning(f"Kolom yang diperlukan tidak ditemukan: {missing_cols}")
        return
    
    # Konversi tanggal dan tambahkan kolom bulan
    df['Tanggal'] = pd.to_datetime(df['Tanggal'])
    df['Bulan'] = df['Tanggal'].dt.to_period('M').astype(str)
    
    # Total volume
    total_volume = df['Volume (L)'].sum()
    total_pengiriman = len(df)
    rata_volume = total_volume / total_pengiriman if total_pengiriman > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-container">
            <h4>🚰 Total Volume Air</h4>
            <p class="big-metric">{total_volume:,.0f} L</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-container">
            <h4>🚚 Total Pengiriman</h4>
            <p class="big-metric">{total_pengiriman:,}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-container">
            <h4>📊 Rata-rata Volume</h4>
            <p class="big-metric">{rata_volume:,.0f} L</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Analisis bulanan
    st.markdown("### 📅 Volume Pengiriman per Bulan")
    
    monthly_volume = df.groupby('Bulan').agg({
        'Volume (L)': ['sum', 'count', 'mean']
    }).reset_index()
    monthly_volume.columns = ['Bulan', 'Total Volume', 'Jumlah Pengiriman', 'Rata-rata Volume']
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Bar(
            x=monthly_volume['Bulan'],
            y=monthly_volume['Total Volume'],
            name='Total Volume',
            marker_color='#1f77b4'
        ),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(
            x=monthly_volume['Bulan'],
            y=monthly_volume['Jumlah Pengiriman'],
            name='Jumlah Pengiriman',
            mode='lines+markers',
            line=dict(color='#ff7f0e', width=3)
        ),
        secondary_y=True
    )
    
    fig.update_layout(
        title='Volume dan Jumlah Pengiriman per Bulan',
        xaxis_title='Bulan',
        yaxis_title='Volume (L)',
        yaxis2_title='Jumlah Pengiriman'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabel detail bulanan
    st.markdown("### 📋 Detail Bulanan")
    monthly_volume_display = monthly_volume.copy()
    monthly_volume_display['Total Volume'] = monthly_volume_display['Total Volume'].apply(lambda x: f"{x:,.0f} L")
    monthly_volume_display['Rata-rata Volume'] = monthly_volume_display['Rata-rata Volume'].apply(lambda x: f"{x:,.0f} L")
    st.dataframe(monthly_volume_display, use_container_width=True)

# 3. DEMOGRAFI PENGIRIMAN AIR
def demografi_pengiriman_air(df, df_locations):
    st.subheader("📍 Demografi Pengiriman Air")
    
    # Pastikan kolom yang diperlukan ada
    required_cols = ['Tanggal', 'Order', 'Volume (L)', 'Pemasukan']
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        st.warning(f"Kolom yang diperlukan tidak ditemukan: {missing_cols}")
        return
    
    # Konversi tanggal dan tambahkan kolom bulan
    df['Tanggal'] = pd.to_datetime(df['Tanggal'])
    df['Bulan'] = df['Tanggal'].dt.to_period('M').astype(str)
    
    # Gabungkan dengan data lokasi jika ada
    if df_locations is not None and 'Nama Lokasi' in df_locations.columns:
        df = pd.merge(df, df_locations, left_on='Order', right_on='Nama Lokasi', how='left')
    else:
        # Jika tidak ada data lokasi, tambahkan koordinat manual untuk Warung Makan Sari Rasa
        df.loc[df['Order'].str.contains('Sari Rasa', case=False, na=False), 'Latitude'] = -7.9932
        df.loc[df['Order'].str.contains('Sari Rasa', case=False, na=False), 'Longitude'] = 110.3417
    
    # Analisis per lokasi
    st.markdown("### 🏆 Top 5 Lokasi Pengiriman")
    
    location_analysis = df.groupby('Order').agg({
        'Volume (L)': 'sum',
        'Pemasukan': 'sum',
        'Tanggal': 'count'
    }).reset_index()
    location_analysis.columns = ['Lokasi', 'Total Volume', 'Total Pemasukan', 'Jumlah Pengiriman']
    location_analysis = location_analysis.sort_values('Total Volume', ascending=False).head(5)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            location_analysis,
            x='Lokasi',
            y='Total Volume',
            title='Total Volume per Lokasi (Top 5)',
            labels={'Total Volume': 'Volume (L)'},
            color='Total Volume',
            color_continuous_scale='Blues'
        )
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(
            location_analysis,
            x='Lokasi',
            y='Total Pemasukan',
            title='Total Pemasukan per Lokasi (Top 5)',
            labels={'Total Pemasukan': 'Pemasukan (Rp)'},
            color='Total Pemasukan',
            color_continuous_scale='Greens'
        )
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    # Analisis bulanan per lokasi
    st.markdown("### 📅 Trend Bulanan per Lokasi")
    
    top_locations = location_analysis['Lokasi'].head(5).tolist()
    monthly_location = df[df['Order'].isin(top_locations)].groupby(['Bulan', 'Order']).agg({
        'Volume (L)': 'sum',
        'Pemasukan': 'sum'
    }).reset_index()
    
    fig = px.line(
        monthly_location,
        x='Bulan',
        y='Volume (L)',
        color='Order',
        title='Volume Pengiriman per Bulan (Top 5 Lokasi)',
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Peta lokasi jika ada koordinat
    if 'Latitude' in df.columns and 'Longitude' in df.columns:
        st.markdown("### 🗺️ Peta Sebaran Lokasi Pengiriman")
        
        # Agregasi data untuk peta
        map_data = df.groupby(['Order', 'Latitude', 'Longitude']).agg({
            'Volume (L)': 'sum',
            'Pemasukan': 'sum'
        }).reset_index()
        
        # Filter data yang memiliki koordinat valid
        map_data_valid = map_data[
            (map_data['Latitude'].notna()) & 
            (map_data['Longitude'].notna()) &
            (map_data['Latitude'] != 0) &
            (map_data['Longitude'] != 0)
        ]
        
        # Tampilkan peta jika ada data valid
        if len(map_data_valid) > 0:
            # Pastikan ada variasi dalam ukuran dan warna
            if map_data_valid['Volume (L)'].max() == map_data_valid['Volume (L)'].min():
                map_data_valid['size_normalized'] = 50  # Ukuran tetap jika semua sama
            else:
                map_data_valid['size_normalized'] = ((map_data_valid['Volume (L)'] - map_data_valid['Volume (L)'].min()) / 
                                                   (map_data_valid['Volume (L)'].max() - map_data_valid['Volume (L)'].min()) * 50 + 10)
            
            fig = px.scatter_mapbox(
                map_data_valid,
                lat="Latitude",
                lon="Longitude",
                size="size_normalized",
                color="Pemasukan",
                hover_name="Order",
                hover_data={
                    "Volume (L)": ":,.0f",
                    "Pemasukan": ":,.0f",
                    "Latitude": ":.4f",
                    "Longitude": ":.4f",
                    "size_normalized": False
                },
                color_continuous_scale='Viridis',
                size_max=30,
                zoom=11,
                height=600,
                title="Sebaran Lokasi Pengiriman (Ukuran: Volume, Warna: Pemasukan)"
            )
            
            fig.update_layout(
                mapbox_style="open-street-map",
                margin={"r":0,"t":30,"l":0,"b":0}
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Informasi tambahan
            st.markdown("### 📋 Informasi Lokasi Pengiriman")
            display_data = map_data_valid.copy()
            display_data['Volume (L)'] = display_data['Volume (L)'].apply(lambda x: f"{x:,.0f} L")
            display_data['Pemasukan'] = display_data['Pemasukan'].apply(lambda x: f"Rp {x:,.0f}")
            st.dataframe(display_data[['Order', 'Volume (L)', 'Pemasukan', 'Latitude', 'Longitude']], use_container_width=True)
            
        else:
            st.warning("⚠️ Tidak ada data koordinat yang valid untuk ditampilkan di peta")
            
            # Suggestion untuk menambahkan koordinat
            st.markdown("""
            ### 💡 Saran untuk Menambahkan Koordinat
            
            Untuk menampilkan peta, tambahkan koordinat lokasi ke dalam file data.
            
            **Contoh koordinat yang tersedia:**
            - Warung Makan Sari Rasa: -7.9932, 110.3417
            """)
    else:
        st.info("ℹ️ Kolom Latitude dan Longitude tidak ditemukan dalam data.")
        
        # Tambahkan koordinat secara manual jika diperlukan
        if st.button("🗺️ Tambahkan Koordinat Manual untuk Peta"):
            df['Latitude'] = None
            df['Longitude'] = None
            
            # Tambahkan koordinat untuk Warung Makan Sari Rasa
            df.loc[df['Order'].str.contains('Sari Rasa', case=False, na=False), 'Latitude'] = -7.9932
            df.loc[df['Order'].str.contains('Sari Rasa', case=False, na=False), 'Longitude'] = 110.3417
            
            st.success("✅ Koordinat berhasil ditambahkan! Refresh halaman untuk melihat peta.")
            st.experimental_rerun()

# 4. DEMOGRAFI PENGGUNAAN ARMADA
def demografi_penggunaan_armada(df):
    st.subheader("🚚 Demografi Penggunaan Armada")
    
    # Pastikan kolom yang diperlukan ada
    required_cols = ['Plat Nomor', 'Volume (L)']
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        st.warning(f"Kolom yang diperlukan tidak ditemukan: {missing_cols}")
        return
    
    # Tambahkan kolom bulan jika ada tanggal
    if 'Tanggal' in df.columns:
        df['Tanggal'] = pd.to_datetime(df['Tanggal'])
        df['Bulan'] = df['Tanggal'].dt.to_period('M').astype(str)
    
    # Statistik armada
    total_armada = df['Plat Nomor'].nunique()
    total_penggunaan = len(df)
    rata_penggunaan = total_penggunaan / total_armada if total_armada > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-container">
            <h4>🚛 Total Armada</h4>
            <p class="big-metric">{total_armada}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-container">
            <h4>🔄 Total Penggunaan</h4>
            <p class="big-metric">{total_penggunaan:,}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-container">
            <h4>📊 Rata-rata Penggunaan</h4>
            <p class="big-metric">{rata_penggunaan:.1f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Analisis armada
    st.markdown("### 📊 Analisis Penggunaan Armada")
    
    armada_analysis = df.groupby('Plat Nomor').agg({
        'Volume (L)': ['sum', 'mean', 'count'],
        'Pengeluaran': 'sum'
    }).reset_index()
    armada_analysis.columns = ['Plat Nomor', 'Total Volume', 'Rata-rata Volume', 'Frekuensi', 'Total Pengeluaran']
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            armada_analysis.sort_values('Total Volume', ascending=False).head(5),
            x='Plat Nomor',
            y='Total Volume',
            title='Total Volume per Armada (Top 5)',
            labels={'Total Volume': 'Volume (L)'}
        )
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.scatter(
            armada_analysis,
            x='Frekuensi',
            y='Total Volume',
            size='Total Pengeluaran',
            color='Rata-rata Volume',
            title='Korelasi Frekuensi vs Volume vs Biaya',
            hover_name='Plat Nomor',
            labels={
                'Frekuensi': 'Frekuensi Penggunaan',
                'Total Volume': 'Total Volume (L)',
                'Total Pengeluaran': 'Total Pengeluaran (Rp)',
                'Rata-rata Volume': 'Rata-rata Volume (L)'
            }
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Analisis bulanan jika ada data bulan
    if 'Bulan' in df.columns:
        st.markdown("### 📅 Trend Bulanan per Armada")
        
        top_armada = armada_analysis.sort_values('Total Volume', ascending=False).head(3)['Plat Nomor'].tolist()
        monthly_armada = df[df['Plat Nomor'].isin(top_armada)].groupby(['Bulan', 'Plat Nomor']).agg({
            'Volume (L)': 'sum'
        }).reset_index()
        
        fig = px.line(
            monthly_armada,
            x='Bulan',
            y='Volume (L)',
            color='Plat Nomor',
            title='Volume Pengiriman per Bulan (Top 3 Armada)',
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)

# 5. ANALISIS KINERJA SOPIR
def analisis_kinerja_sopir(df):
    st.subheader("👨‍🚀 Analisis Kinerja Sopir")
    
    # Pastikan kolom yang diperlukan ada
    required_cols = ['Sopir', 'Volume (L)']
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        st.warning(f"Kolom yang diperlukan tidak ditemukan: {missing_cols}")
        return
    
    # Tambahkan kolom bulan jika ada tanggal
    if 'Tanggal' in df.columns:
        df['Tanggal'] = pd.to_datetime(df['Tanggal'])
        df['Bulan'] = df['Tanggal'].dt.to_period('M').astype(str)
    
    # Statistik sopir
    total_sopir = df['Sopir'].nunique()
    total_tugas = len(df)
    rata_tugas = total_tugas / total_sopir if total_sopir > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-container">
            <h4>👨‍🚀 Total Sopir</h4>
            <p class="big-metric">{total_sopir}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-container">
            <h4>📋 Total Tugas</h4>
            <p class="big-metric">{total_tugas:,}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-container">
            <h4>📊 Rata-rata Tugas</h4>
            <p class="big-metric">{rata_tugas:.1f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Analisis kinerja sopir
    st.markdown("### 📊 Analisis Kinerja Sopir")
    
    sopir_analysis = df.groupby('Sopir').agg({
        'Volume (L)': ['sum', 'mean', 'count'],
        'Pemasukan': 'sum'
    }).reset_index()
    sopir_analysis.columns = ['Sopir', 'Total Volume', 'Rata-rata Volume', 'Frekuensi', 'Total Pemasukan']
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            sopir_analysis.sort_values('Total Volume', ascending=False).head(5),
            x='Sopir',
            y='Total Volume',
            title='Total Volume per Sopir (Top 5)',
            labels={'Total Volume': 'Volume (L)'}
        )
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.scatter(
            sopir_analysis,
            x='Frekuensi',
            y='Total Volume',
            size='Total Pemasukan',
            color='Rata-rata Volume',
            title='Korelasi Frekuensi vs Volume vs Pemasukan',
            hover_name='Sopir',
            labels={
                'Frekuensi': 'Frekuensi Tugas',
                'Total Volume': 'Total Volume (L)',
                'Total Pemasukan': 'Total Pemasukan (Rp)',
                'Rata-rata Volume': 'Rata-rata Volume (L)'
            }
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Analisis bulanan jika ada data bulan
    if 'Bulan' in df.columns:
        st.markdown("### 📅 Trend Bulanan per Sopir")
        
        top_sopir = sopir_analysis.sort_values('Total Volume', ascending=False).head(3)['Sopir'].tolist()
        monthly_sopir = df[df['Sopir'].isin(top_sopir)].groupby(['Bulan', 'Sopir']).agg({
            'Volume (L)': 'sum'
        }).reset_index()
        
        fig = px.line(
            monthly_sopir,
            x='Bulan',
            y='Volume (L)',
            color='Sopir',
            title='Volume Pengiriman per Bulan (Top 3 Sopir)',
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)

# 6. ANALISIS EFISIENSI OPERASIONAL
def analisis_efisiensi_operasional(df):
    st.subheader("⚡ Analisis Efisiensi Operasional")
    
    # Pastikan kolom yang diperlukan ada
    required_cols = ['Tanggal', 'Plat Nomor', 'Sopir', 'Volume (L)', 'Pemasukan', 'Pengeluaran']
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        st.warning(f"Kolom yang diperlukan tidak ditemukan: {missing_cols}")
        return
    
    # Konversi tanggal dan tambahkan kolom bulan
    df['Tanggal'] = pd.to_datetime(df['Tanggal'])
    df['Bulan'] = df['Tanggal'].dt.to_period('M').astype(str)
    
    # Hitung efisiensi (Pemasukan - Pengeluaran) per liter
    df['Efisiensi'] = (df['Pemasukan'] - df['Pengeluaran']) / df['Volume (L)']
    
    # Metrik utama efisiensi
    efisiensi_total = df['Efisiensi'].mean()
    volume_total = df['Volume (L)'].sum()
    profit_margin = ((df['Pemasukan'].sum() - df['Pengeluaran'].sum()) / df['Pemasukan'].sum()) * 100
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-container">
            <h4>⚡ Efisiensi Rata-rata</h4>
            <p class="big-metric">Rp {efisiensi_total:.2f}/L</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-container">
            <h4>🚰 Total Volume</h4>
            <p class="big-metric">{volume_total:,.0f} L</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-container">
            <h4>📈 Profit Margin</h4>
            <p class="big-metric">{profit_margin:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 1. Efisiensi per Bulan
    st.markdown("### 📅 Efisiensi Operasional per Bulan")
    
    monthly_efficiency = df.groupby('Bulan').agg({
        'Efisiensi': 'mean',
        'Pemasukan': 'sum',
        'Pengeluaran': 'sum',
        'Volume (L)': 'sum'
    }).reset_index()
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Bar(
            x=monthly_efficiency['Bulan'],
            y=monthly_efficiency['Efisiensi'],
            name='Efisiensi (Rp/L)',
            marker_color='#2ca02c'
        ),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(
            x=monthly_efficiency['Bulan'],
            y=monthly_efficiency['Pemasukan'],
            name='Pemasukan (Rp)',
            line=dict(color='#1f77b4', width=3),
            mode='lines+markers'
        ),
        secondary_y=True
    )
    
    fig.add_trace(
        go.Scatter(
            x=monthly_efficiency['Bulan'],
            y=monthly_efficiency['Pengeluaran'],
            name='Pengeluaran (Rp)',
            line=dict(color='#ff7f0e', width=3),
            mode='lines+markers'
        ),
        secondary_y=True
    )
    
    fig.update_layout(
        title='Efisiensi Operasional per Bulan',
        xaxis_title='Bulan',
        yaxis_title='Efisiensi (Rp/Liter)',
        yaxis2_title='Pemasukan/Pengeluaran (Rp)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 2. Efisiensi per Armada
    st.markdown("### 🚚 Efisiensi per Armada")
    
    armada_efficiency = df.groupby('Plat Nomor').agg({
        'Efisiensi': 'mean',
        'Volume (L)': 'sum',
        'Pemasukan': 'sum',
        'Pengeluaran': 'sum'
    }).reset_index()
    armada_efficiency = armada_efficiency.sort_values('Efisiensi', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            armada_efficiency.head(5),
            x='Plat Nomor',
            y='Efisiensi',
            title='Top 5 Armada Paling Efisien',
            labels={'Efisiensi': 'Efisiensi (Rp/L)'},
            color='Efisiensi',
            color_continuous_scale='Greens'
        )
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.scatter(
            armada_efficiency,
            x='Volume (L)',
            y='Efisiensi',
            size='Pemasukan',
            color='Pengeluaran',
            title='Korelasi Volume vs Efisiensi',
            hover_name='Plat Nomor',
            labels={
                'Volume (L)': 'Total Volume (L)',
                'Efisiensi': 'Efisiensi (Rp/L)',
                'Pemasukan': 'Total Pemasukan (Rp)',
                'Pengeluaran': 'Total Pengeluaran (Rp)'
            }
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # 3. Efisiensi per Sopir
    st.markdown("### 👨‍🚀 Efisiensi per Sopir")
    
    sopir_efficiency = df.groupby('Sopir').agg({
        'Efisiensi': 'mean',
        'Volume (L)': 'sum',
        'Pemasukan': 'sum',
        'Pengeluaran': 'sum'
    }).reset_index()
    sopir_efficiency = sopir_efficiency.sort_values('Efisiensi', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            sopir_efficiency.head(5),
            x='Sopir',
            y='Efisiensi',
            title='Top 5 Sopir Paling Efisien',
            labels={'Efisiensi': 'Efisiensi (Rp/L)'},
            color='Efisiensi',
            color_continuous_scale='Greens'
        )
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.scatter(
            sopir_efficiency,
            x='Volume (L)',
            y='Efisiensi',
            size='Pemasukan',
            color='Pengeluaran',
            title='Korelasi Volume vs Efisiensi',
            hover_name='Sopir',
            labels={
                'Volume (L)': 'Total Volume (L)',
                'Efisiensi': 'Efisiensi (Rp/L)',
                'Pemasukan': 'Total Pemasukan (Rp)',
                'Pengeluaran': 'Total Pengeluaran (Rp)'
            }
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Insight tambahan
    st.markdown("### 💡 Key Insights")
    
    most_efficient_month = monthly_efficiency.loc[monthly_efficiency['Efisiensi'].idxmax()]
    least_efficient_month = monthly_efficiency.loc[monthly_efficiency['Efisiensi'].idxmin()]
    
    most_efficient_armada = armada_efficiency.iloc[0]
    least_efficient_armada = armada_efficiency.iloc[-1]
    
    most_efficient_driver = sopir_efficiency.iloc[0]
    least_efficient_driver = sopir_efficiency.iloc[-1]
    
    insights = [
        f"📈 Bulan paling efisien: **{most_efficient_month['Bulan']}** (Rp {most_efficient_month['Efisiensi']:.2f}/L)",
        f"📉 Bulan paling tidak efisien: **{least_efficient_month['Bulan']}** (Rp {least_efficient_month['Efisiensi']:.2f}/L)",
        f"🏆 Armada paling efisien: **{most_efficient_armada['Plat Nomor']}** (Rp {most_efficient_armada['Efisiensi']:.2f}/L)",
        f"🚛 Armada paling tidak efisien: **{least_efficient_armada['Plat Nomor']}** (Rp {least_efficient_armada['Efisiensi']:.2f}/L)",
        f"👨‍🚀 Sopir paling efisien: **{most_efficient_driver['Sopir']}** (Rp {most_efficient_driver['Efisiensi']:.2f}/L)",
        f"🧑‍💼 Sopir paling tidak efisien: **{least_efficient_driver['Sopir']}** (Rp {least_efficient_driver['Efisiensi']:.2f}/L)"
    ]
    
    for insight in insights:
        st.markdown(f"""
        <div class="insight-box">
            {insight}
        </div>
        """, unsafe_allow_html=True)

# 7. ANALISIS POLA OPERASIONAL - VISUALISASI BARU 1
def analisis_pola_operasional(df):
    st.subheader("📊 Analisis Pola Operasional")
    
    # Pastikan kolom yang diperlukan ada
    required_cols = ['Tanggal', 'Volume (L)', 'Pemasukan', 'Pengeluaran']
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        st.warning(f"Kolom yang diperlukan tidak ditemukan: {missing_cols}")
        return
    
    # Konversi tanggal dan tambahkan kolom
    df['Tanggal'] = pd.to_datetime(df['Tanggal'])
    df['Hari_Minggu'] = df['Tanggal'].dt.day_name()
    df['Quarter'] = df['Tanggal'].dt.quarter
    
    # 1. Analisis Hari dalam Minggu
    st.markdown("### 📅 Pola Operasional per Hari dalam Minggu")
    
    daily_pattern = df.groupby('Hari_Minggu').agg({
        'Volume (L)': ['sum', 'count', 'mean'],
        'Pemasukan': 'sum',
        'Pengeluaran': 'sum'
    }).reset_index()
    
    daily_pattern.columns = ['Hari', 'Total_Volume', 'Jumlah_Order', 'Rata_Volume', 'Total_Pemasukan', 'Total_Pengeluaran']
    
    # Urutkan hari
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    daily_pattern['Hari'] = pd.Categorical(daily_pattern['Hari'], categories=day_order, ordered=True)
    daily_pattern = daily_pattern.sort_values('Hari')
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            daily_pattern,
            x='Hari',
            y='Total_Volume',
            title='Total Volume per Hari dalam Minggu',
            labels={'Total_Volume': 'Total Volume (L)', 'Hari': 'Hari'},
            color='Total_Volume',
            color_continuous_scale='Blues'
        )
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(
            daily_pattern,
            x='Hari',
            y='Jumlah_Order',
            title='Jumlah Order per Hari dalam Minggu',
            labels={'Jumlah_Order': 'Jumlah Order', 'Hari': 'Hari'},
            color='Jumlah_Order',
            color_continuous_scale='Oranges'
        )
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    # 2. Analisis Kuartalan
    st.markdown("### 📊 Pola Operasional per Kuartal")
    
    quarterly_pattern = df.groupby('Quarter').agg({
        'Volume (L)': ['sum', 'count', 'mean'],
        'Pemasukan': 'sum',
        'Pengeluaran': 'sum'
    }).reset_index()
    
    quarterly_pattern.columns = ['Kuartal', 'Total_Volume', 'Jumlah_Order', 'Rata_Volume', 'Total_Pemasukan', 'Total_Pengeluaran']
    quarterly_pattern['Profit'] = quarterly_pattern['Total_Pemasukan'] - quarterly_pattern['Total_Pengeluaran']
    quarterly_pattern['Kuartal'] = quarterly_pattern['Kuartal'].apply(lambda x: f'Q{x}')
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Volume per Kuartal', 'Jumlah Order per Kuartal', 
                       'Profit per Kuartal', 'Rata-rata Volume per Kuartal'),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )
    
    fig.add_trace(
        go.Bar(x=quarterly_pattern['Kuartal'], y=quarterly_pattern['Total_Volume'], 
               name='Volume', marker_color='lightblue'),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Bar(x=quarterly_pattern['Kuartal'], y=quarterly_pattern['Jumlah_Order'], 
               name='Order', marker_color='lightcoral'),
        row=1, col=2
    )
    
    fig.add_trace(
        go.Bar(x=quarterly_pattern['Kuartal'], y=quarterly_pattern['Profit'], 
               name='Profit', marker_color='lightgreen'),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Bar(x=quarterly_pattern['Kuartal'], y=quarterly_pattern['Rata_Volume'], 
               name='Rata Volume', marker_color='lightyellow'),
        row=2, col=2
    )
    
    fig.update_layout(height=600, showlegend=False, title_text="Analisis Kuartalan")
    st.plotly_chart(fig, use_container_width=True)

# 8. ANALISIS PERFORMA BISNIS - VISUALISASI BARU 2
def analisis_performa_bisnis(df):
    st.subheader("📈 Analisis Performa Bisnis")
    
    # Pastikan kolom yang diperlukan ada
    required_cols = ['Tanggal', 'Volume (L)', 'Pemasukan', 'Pengeluaran', 'Sopir', 'Plat Nomor']
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        st.warning(f"Kolom yang diperlukan tidak ditemukan: {missing_cols}")
        return
    
    # Konversi tanggal dan tambahkan kolom
    df['Tanggal'] = pd.to_datetime(df['Tanggal'])
    df['Bulan'] = df['Tanggal'].dt.to_period('M').astype(str)
    df['Revenue_per_Liter'] = df['Pemasukan'] / df['Volume (L)']
    df['Cost_per_Liter'] = df['Pengeluaran'] / df['Volume (L)']
    df['Profit_per_Liter'] = df['Revenue_per_Liter'] - df['Cost_per_Liter']
    
    # 1. KPI Dashboard
    st.markdown("### 🎯 Key Performance Indicators (KPI)")
    
    total_revenue = df['Pemasukan'].sum()
    total_cost = df['Pengeluaran'].sum()
    total_profit = total_revenue - total_cost
    avg_revenue_per_liter = df['Revenue_per_Liter'].mean()
    growth_rate = ((df.groupby('Bulan')['Pemasukan'].sum().iloc[-1] - 
                   df.groupby('Bulan')['Pemasukan'].sum().iloc[0]) / 
                   df.groupby('Bulan')['Pemasukan'].sum().iloc[0] * 100) if len(df.groupby('Bulan')) > 1 else 0
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="metric-container">
            <h4>💰 Total Revenue</h4>
            <p class="big-metric">Rp {total_revenue/1000000:.1f}M</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-container">
            <h4>💸 Total Cost</h4>
            <p class="big-metric">Rp {total_cost/1000000:.1f}M</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-container">
            <h4>📊 Net Profit</h4>
            <p class="big-metric">Rp {total_profit/1000000:.1f}M</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-container">
            <h4>💧 Revenue/Liter</h4>
            <p class="big-metric">Rp {avg_revenue_per_liter:.0f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="metric-container">
            <h4>📈 Growth Rate</h4>
            <p class="big-metric">{growth_rate:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 2. Analisis Produktivitas Sopir
    st.markdown("### 👨‍🚀 Produktivitas dan Profitabilitas Sopir")
    
    sopir_productivity = df.groupby('Sopir').agg({
        'Pemasukan': 'sum',
        'Pengeluaran': 'sum',
        'Volume (L)': 'sum',
        'Tanggal': 'count'
    }).reset_index()
    
    sopir_productivity.columns = ['Sopir', 'Total_Revenue', 'Total_Cost', 'Total_Volume', 'Total_Trips']
    sopir_productivity['Revenue_per_Trip'] = sopir_productivity['Total_Revenue'] / sopir_productivity['Total_Trips']
    sopir_productivity['Volume_per_Trip'] = sopir_productivity['Total_Volume'] / sopir_productivity['Total_Trips']
    sopir_productivity['Profit_per_Trip'] = (sopir_productivity['Total_Revenue'] - sopir_productivity['Total_Cost']) / sopir_productivity['Total_Trips']
    
    sopir_productivity = sopir_productivity.sort_values('Revenue_per_Trip', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            sopir_productivity.head(5),
            x='Sopir',
            y='Revenue_per_Trip',
            title='Top 5 Sopir - Revenue per Trip',
            labels={'Revenue_per_Trip': 'Revenue per Trip (Rp)', 'Sopir': 'Sopir'},
            color='Revenue_per_Trip',
            color_continuous_scale='Blues'
        )
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.scatter(
            sopir_productivity,
            x='Total_Trips',
            y='Revenue_per_Trip',
            size='Total_Volume',
            color='Profit_per_Trip',
            title='Produktivitas vs Profitabilitas Sopir',
            hover_name='Sopir',
            labels={
                'Total_Trips': 'Total Trips',
                'Revenue_per_Trip': 'Revenue per Trip (Rp)',
                'Total_Volume': 'Total Volume (L)',
                'Profit_per_Trip': 'Profit per Trip (Rp)'
            }
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # 3. Trend Profitabilitas Bulanan
    st.markdown("### 📊 Trend Profitabilitas Bulanan")
    
    monthly_profit = df.groupby('Bulan').agg({
        'Pemasukan': 'sum',
        'Pengeluaran': 'sum',
        'Volume (L)': 'sum'
    }).reset_index()
    
    monthly_profit['Profit'] = monthly_profit['Pemasukan'] - monthly_profit['Pengeluaran']
    monthly_profit['Profit_Margin'] = (monthly_profit['Profit'] / monthly_profit['Pemasukan']) * 100
    monthly_profit['Revenue_per_Liter'] = monthly_profit['Pemasukan'] / monthly_profit['Volume (L)']
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Bar(
            x=monthly_profit['Bulan'],
            y=monthly_profit['Profit'],
            name='Monthly Profit',
            marker_color='lightgreen'
        ),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(
            x=monthly_profit['Bulan'],
            y=monthly_profit['Profit_Margin'],
            name='Profit Margin (%)',
            mode='lines+markers',
            line=dict(color='red', width=3)
        ),
        secondary_y=True
    )
    
    fig.update_layout(
        title='Trend Profit dan Profit Margin Bulanan',
        xaxis_title='Bulan'
    )
    
    fig.update_yaxes(title_text="Profit (Rp)", secondary_y=False)
    fig.update_yaxes(title_text="Profit Margin (%)", secondary_y=True)
    
    st.plotly_chart(fig, use_container_width=True)

# Main dashboard function - DIPERBARUI
def main():
    st.markdown('<h1 class="main-header">🚛 Dashboard Analisis Truk Air Isi Ulang</h1>', unsafe_allow_html=True)
    
    # Load data CSV
    sheet2, sheet3 = load_csv_data()
    
    if sheet2 is None or sheet3 is None:
        st.stop()
    
    # Sidebar untuk navigasi
    st.sidebar.title("🎛️ Navigasi Dashboard")
    
    analysis_options = [
        "💰 1. Transaksi Keuangan", 
        "🚛 2. Rekap Pengiriman Air",
        "📍 3. Demografi Pengiriman",
        "🚚 4. Penggunaan Armada",
        "👨‍🚀 5. Kinerja Sopir",
        "⚡ 6. Efisiensi Operasional",
        "📊 7. Pola Operasional",
        "📈 8. Performa Bisnis"
    ]
    
    selected_analysis = st.sidebar.selectbox("Pilih Jenis Analisis:", analysis_options)
    
    # Pilihan dataset
    dataset_choice = st.sidebar.selectbox("Pilih Dataset:", ["Sheet 2", "Sheet 3", "Gabungan"])
    
    if dataset_choice == "Sheet 2":
        df = sheet2.copy()
        st.sidebar.success("📄 Dataset: Sheet 2")
    elif dataset_choice == "Sheet 3":
        df = sheet3.copy()
        st.sidebar.success("📄 Dataset: Sheet 3")
    else:
        df = pd.concat([sheet2, sheet3], ignore_index=True)
        st.sidebar.success("📄 Dataset: Gabungan")
    
    # Tampilkan info dataset
    st.sidebar.markdown("### 📋 Info Dataset")
    st.sidebar.write(f"📊 Jumlah Baris: {len(df):,}")
    st.sidebar.write(f"📈 Jumlah Kolom: {len(df.columns)}")
    st.sidebar.write(f"🔍 Missing Values: {df.isnull().sum().sum()}")
    
    # Jalankan analisis sesuai pilihan
    if selected_analysis == "💰 1. Transaksi Keuangan":
        analisis_transaksi_keuangan(df)
    elif selected_analysis == "🚛 2. Rekap Pengiriman Air":
        rekap_pengiriman_air(df)
    elif selected_analysis == "📍 3. Demografi Pengiriman":
        demografi_pengiriman_air(df, sheet3)
    elif selected_analysis == "🚚 4. Penggunaan Armada":
        demografi_penggunaan_armada(df)
    elif selected_analysis == "👨‍🚀 5. Kinerja Sopir":
        analisis_kinerja_sopir(df)
    elif selected_analysis == "⚡ 6. Efisiensi Operasional":
        analisis_efisiensi_operasional(df)
    elif selected_analysis == "📊 7. Pola Operasional":
        analisis_pola_operasional(df)
    elif selected_analysis == "📈 8. Performa Bisnis":
        analisis_performa_bisnis(df)

if __name__ == "__main__":
    main()
