import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AI Rekomendasi Lokasi UMKM", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Tambahkan kode ini untuk verifikasi kepemilikan lomba
st.markdown(
    '<meta name="dicoding:email" content="syamil.haniyyah3@gmail.com">',
    unsafe_allow_html=True
)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

URL_AZURE = "https://dataumkmsyamil.blob.core.windows.net/dataset-lomba/data_versi_8_PURE_REAL.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(URL_AZURE)
    return df

try:
    df = load_data()

    st.sidebar.markdown("<h1 style='text-align: center;'>OptiLocate</h1>", unsafe_allow_html=True)
    
    st.sidebar.image("logo_datathon-removebg-preview.png", use_container_width=True)
    
    st.sidebar.header("🔍 Analisis Lokasi")
    
    kelurahan_list = sorted(df['kelurahan'].unique())
    selected_kelurahan = st.sidebar.selectbox("Pilih Kelurahan Target:", kelurahan_list)

    st.sidebar.markdown("---")
    st.sidebar.header("🏪 Kategori Bisnis")
    
    kategori = st.sidebar.selectbox("Pilih Kategori Bisnis:", ["Minimarket", "Apotek"])

    st.sidebar.markdown("---")
    st.sidebar.info("""
    **Tentang Data:**
    Data populasi, fasilitas umum (halte), dan lokasi UMKM yang digunakan pada aplikasi ini bersumber resmi dari **Open Data Pemerintah Provinsi DKI Jakarta**. 
    """)

    st.sidebar.caption("© 2026 | Dikembangkan oleh Tim Kompas")
    
    def min_max_scaling(column):
        if column.max() == column.min():
            return column * 0
        return (column - column.min()) / (column.max() - column.min())

    pop_norm = min_max_scaling(df['jumlah_penduduk'])
    halte_norm = min_max_scaling(df['Jumlah_Halte_Terdekat'])

    komp_norm = 1 - min_max_scaling(df[kategori]) 

    skor_raw = (pop_norm * 0.5) + (halte_norm * 0.3) + (komp_norm * 0.2)

    df['Skor_Dinamis'] = min_max_scaling(skor_raw) * 100

    df['Skor_Dinamis'] = df['Skor_Dinamis'].round(2)

    detail_lokasi = df[df['kelurahan'] == selected_kelurahan].iloc[0]

    st.title("AI Penentu Lokasi Optimal Membuka UMKM")
    st.markdown(f"Menganalisis potensi untuk membuka **{kategori}** di **{selected_kelurahan}**")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Skor Kelayakan", f"{detail_lokasi['Skor_Dinamis']:.2f}/100")
    with col2:
        st.metric("Populasi Penduduk", f"{int(detail_lokasi['jumlah_penduduk']):,}")
    with col3:
        st.metric("Akses Halte Terdekat", f"{int(detail_lokasi['Jumlah_Halte_Terdekat'])} halte")
    with col4:
        st.metric(f"Jumlah {kategori} Saat Ini", f"{int(detail_lokasi[kategori])} kompetitor")
        
    st.subheader("📍 Titik Koordinat Kelurahan")
    map_data = pd.DataFrame({
        'lat': [detail_lokasi['Latitude']],
        'lon': [detail_lokasi['Longitude']]
    })
    st.map(map_data, zoom=14)

    st.subheader(f"Top 10 Kelurahan Terbaik untuk {kategori}")
    
    top_10 = df.sort_values(by='Skor_Dinamis', ascending=False).head(10).copy()
    top_10.index = range(1, 11)
    
    kolom_tampil = ['kelurahan', 'Skor_Dinamis', 'jumlah_penduduk', 'Jumlah_Halte_Terdekat', kategori]
    st.dataframe(top_10[kolom_tampil], use_container_width=True)

except Exception as e:
    st.error(f"Gagal memuat data. Pastikan URL Azure sudah benar. Error: {e}")
