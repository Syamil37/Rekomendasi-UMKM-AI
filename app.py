import streamlit as st
import pandas as pd

# 1. Mengatur Tampilan Halaman Web
st.set_page_config(page_title="Rekomendasi UMKM", page_icon="🏙️", layout="wide")
st.title("🏙️ Spatial Recommender: Lokasi Emas UMKM")
st.write("Dashboard AI untuk menemukan lokasi terbaik membuka usaha berdasarkan data demografi dan spasial kota.")

# 2. Membaca Data Final dari Fase 2
@st.cache_data
def load_data():
    # Pastikan file CSV ini ada di folder yang sama dengan file app.py
    data = pd.read_csv('https://dataumkmsyamil.blob.core.windows.net/dataset-lomba/data_final_umkm.csv')
    return data

df = load_data()

# 3. Membuat Sidebar untuk Interaksi Pengguna
st.sidebar.header("🔍 Analisis Lokasi")
kelurahan_list = sorted(df['kelurahan'].tolist())
selected_kel = st.sidebar.selectbox("Pilih Kelurahan Target:", kelurahan_list)

# Mengambil data khusus untuk kelurahan yang dipilih
data_kel = df[df['kelurahan'] == selected_kel].iloc[0]

# 4. Menampilkan Kartu Metrik (Angka-angka Penting)
st.subheader(f"📊 Hasil Analisis AI: Kelurahan {selected_kel}")
col1, col2, col3, col4 = st.columns(4)

# Logika Warna Skor
if data_kel['Skor_Kelayakan'] >= 80:
    skor_teks = f"🔥 {data_kel['Skor_Kelayakan']} (Sangat Direkomendasikan)"
elif data_kel['Skor_Kelayakan'] >= 50:
    skor_teks = f"⚠️ {data_kel['Skor_Kelayakan']} (Cukup Potensial)"
else:
    skor_teks = f"❌ {data_kel['Skor_Kelayakan']} (Kurang Disarankan)"

col1.metric("Skor Kelayakan (0-100)", data_kel['Skor_Kelayakan'])
col2.metric("Penduduk (Target Pasar)", f"{int(data_kel['jumlah_penduduk']):,}")
col3.metric("Halte Terdekat (< 2KM)", int(data_kel['Jumlah_Halte_Terdekat']))
col4.metric("Saingan Terdekat (< 1KM)", int(data_kel['Jumlah_Kompetitor']))

st.info(skor_teks)

# 5. Menampilkan Peta Interaktif
st.subheader("🗺️ Peta Titik Kelurahan")
# Streamlit butuh nama kolom spesifik 'lat' dan 'lon' untuk peta
df_map = df.rename(columns={'Lat_Kelurahan': 'lat', 'Lon_Kelurahan': 'lon'})
# Menampilkan hanya titik kelurahan yang dipilih agar fokus
st.map(df_map[df_map['kelurahan'] == selected_kel], zoom=12)

# 6. Menampilkan Leaderboard (Top 10)
st.subheader("🏆 Top 10 Lokasi Emas di Kota Ini")
top_10 = df[['kelurahan', 'Skor_Kelayakan', 'jumlah_penduduk', 'Jumlah_Halte_Terdekat', 'Jumlah_Kompetitor']].head(10).copy()
top_10.index = range(1, 11) # Memaksa index dimulai dari angka 1 sampai 10
st.dataframe(top_10, use_container_width=True)

st.caption("Dibuat untuk Microsoft AI Impact Challenge 2026")
