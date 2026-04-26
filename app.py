import streamlit as st
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(page_title="AI Rekomendasi Lokasi UMKM", layout="wide")

# Menyembunyikan menu default dan footer Streamlit
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 1. LOAD DATA DARI AZURE 
URL_AZURE = "https://dataumkmsyamil.blob.core.windows.net/dataset-lomba/data_versi_6.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(URL_AZURE)
    return df

try:
    df = load_data()

    # --- SIDEBAR: ANALISIS LOKASI ---
    st.sidebar.image("logo_umkm.png", use_container_width=True)
    
    st.sidebar.header("🔍 Analisis Lokasi")
    
    # Urutan Abjad pada Dropdown
    kelurahan_list = sorted(df['kelurahan'].unique())
    selected_kelurahan = st.sidebar.selectbox("Pilih Kelurahan Target:", kelurahan_list)

    # Fitur Baru: Pilih Kategori UMKM
    st.sidebar.markdown("---")
    st.sidebar.header("🏪 Kategori Bisnis")
    kategori = st.sidebar.radio("Pilih Jenis UMKM:", ["Cafe", "Minimarket", "Apotek", "Laundry"])

# --- LOGIKA AI DINAMIS (Real-Time Scoring: MIN-MAX SCALER) ---
    
    # 1. Fungsi Helper Min-Max (Mengubah angka jadi rentang 0.0 sampai 1.0)
    def min_max_scaling(column):
        if column.max() == column.min():
            return column * 0
        return (column - column.min()) / (column.max() - column.min())

    # 2. Normalisasi setiap variabel secara adil
    pop_norm = min_max_scaling(df['jumlah_penduduk'])
    halte_norm = min_max_scaling(df['Jumlah_Halte_Terdekat'])

    # 3. Khusus kompetitor, dibalik (1 - nilai) karena saingan sedikit itu bagus
    komp_norm = 1 - min_max_scaling(df[kategori]) 

    # 4. Hitung Skor Gabungan (Bobot: Populasi 50%, Akses 30%, Kelangkaan Saingan 20%)
    skor_raw = (pop_norm * 0.5) + (halte_norm * 0.3) + (komp_norm * 0.2)

    # 5. Transformasi akhir ke skala 0-100 agar ada yang mendapat nilai 100 sempurna
    df['Skor_Dinamis'] = min_max_scaling(skor_raw) * 100

    # 6. Pembulatan angka agar tabel terlihat rapi
    df['Skor_Dinamis'] = df['Skor_Dinamis'].round(2)

    # ---> AMBIL DATA KELURAHAN SETELAH SKOR DIHITUNG <---
    # ---> AMBIL DATA KELURAHAN SETELAH SKOR DIHITUNG <---
    
    detail_lokasi = df[df['kelurahan'] == selected_kelurahan].iloc[0]

    # --- MAIN CONTENT ---
    st.title("🏆 AI Penentu Lokasi Emas UMKM")
    st.markdown(f"Menganalisis potensi untuk membuka **{kategori}** di **{selected_kelurahan}**")

    # Kolom Statistik Utama
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Skor Kelayakan", f"{detail_lokasi['Skor_Dinamis']:.2f}/100")
    with col2:
        st.metric("Populasi Penduduk", f"{int(detail_lokasi['jumlah_penduduk']):,}")
    with col3:
        st.metric(f"Jumlah {kategori} Saat Ini", f"{int(detail_lokasi[kategori])} kompetitor")

    # --- PETA ---
    st.subheader("📍 Titik Koordinat Kelurahan")
    map_data = pd.DataFrame({
        'lat': [detail_lokasi['Latitude']],
        'lon': [detail_lokasi['Longitude']]
    })
    st.map(map_data, zoom=14)

    # --- TABEL RANKING DINAMIS ---
    st.subheader(f"🥇 Top 10 Kelurahan Terbaik untuk {kategori}")
    
    # Sortir ulang berdasarkan Skor Dinamis yang baru dihitung!
    top_10 = df.sort_values(by='Skor_Dinamis', ascending=False).head(10).copy()
    top_10.index = range(1, 11)
    
    # Tampilkan tabelnya
    kolom_tampil = ['kelurahan', 'Skor_Dinamis', 'jumlah_penduduk', 'Jumlah_Halte_Terdekat', kategori]
    st.dataframe(top_10[kolom_tampil], use_container_width=True)

except Exception as e:
    st.error(f"Gagal memuat data. Pastikan URL Azure sudah benar. Error: {e}")
