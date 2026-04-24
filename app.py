import streamlit as st
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(page_title="AI Rekomendasi Lokasi UMKM", layout="wide")

# 1. LOAD DATA DARI AZURE (Ganti URL di bawah dengan URL Azure barumu)
URL_AZURE = "https://dataumkmsyamil.blob.core.windows.net/dataset-lomba/data_versi_6.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(URL_AZURE)
    return df

try:
    df = load_data()

    # --- SIDEBAR: ANALISIS LOKASI ---
    st.sidebar.header("🔍 Analisis Lokasi")
    
    # Perbaikan 3: Urutan Abjad pada Dropdown
    kelurahan_list = sorted(df['kelurahan'].unique())
    selected_kelurahan = st.sidebar.selectbox("Pilih Kelurahan Target:", kelurahan_list)

    # Fitur Baru: Pilih Kategori UMKM
    st.sidebar.markdown("---")
    st.sidebar.header("🏪 Kategori Bisnis")
    kategori = st.sidebar.radio("Pilih Jenis UMKM:", ["Cafe", "Minimarket", "Apotek", "Laundry"])

    # Ambil data spesifik kelurahan yang dipilih
    detail_lokasi = df[df['kelurahan'] == selected_kelurahan].iloc[0]

    # --- MAIN CONTENT ---
    st.title("🏆 AI Penentu Lokasi Emas UMKM")
    st.markdown(f"Menganalisis potensi untuk membuka **{kategori}** di **{selected_kelurahan}**")

    # Kolom Statistik Utama
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Skor Kelayakan", f"{detail_lokasi['Skor_Kelayakan']:.2f}/100")
    with col2:
        st.metric("Populasi Penduduk", f"{int(detail_lokasi['jumlah_penduduk']):,}")
    with col3:
        st.metric(f"Jumlah {kategori} Saat Ini", f"{int(detail_lokasi[kategori])} kompetitor")

    # --- PETA (Sekarang Akurat dengan Lat/Long Asli) ---
    st.subheader("📍 Titik Koordinat Kelurahan")
    map_data = pd.DataFrame({
        'lat': [detail_lokasi['Latitude']],
        'lon': [detail_lokasi['Longitude']]
    })
    st.map(map_data, zoom=14)

    # --- TABEL RANKING (Perbaikan 2: Index 1-10) ---
    st.subheader(f"🥇 Top 10 Kelurahan Terbaik untuk {kategori}")
    
    # Sortir ulang berdasarkan Skor Kelayakan (Top 10)
    top_10 = df.sort_values(by='Skor_Kelayakan', ascending=False).head(10).copy()
    
    # Reset index agar mulai dari 1
    top_10.index = range(1, 11)
    
    # Tampilkan kolom yang relevan saja termasuk kategori yang dipilih
    kolom_tampil = ['kelurahan', 'Skor_Kelayakan', 'jumlah_penduduk', 'Jumlah_Halte_Terdekat', kategori]
    st.dataframe(top_10[kolom_tampil], use_container_width=True)

except Exception as e:
    st.error(f"Gagal memuat data. Pastikan URL Azure sudah benar. Error: {e}")
