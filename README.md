OptiLocate - AI Penentu Lokasi Optimal Membuka UMKM

Tentang Proyek
OptiLocate adalah sebuah purwarupa (prototype) sistem cerdas yang dirancang untuk membantu para pelaku UMKM dan pengusaha dalam menentukan lokasi paling strategis untuk membuka cabang bisnis baru (seperti Minimarket dan Apotek) di wilayah DKI Jakarta. 

Aplikasi ini menggunakan algoritma **Min-Max Scaler** secara *real-time* untuk memberikan "Skor Kelayakan" pada setiap kelurahan berdasarkan pendekatan berbasis data (Data-Driven).

Arsitektur & Teknologi
Proyek ini mengintegrasikan beberapa teknologi untuk memastikan keandalan dan akurasi data:
1. Data Sources: 100% menggunakan data riil dari **Open Data Pemerintah Provinsi DKI Jakarta** (Data Kependudukan, Fasilitas Transportasi/Halte, dan Data Ekosistem Bisnis/UMKM).
2. Data Preprocessing: Dibersihkan dan digabungkan menggunakan Python (Pandas) di Google Colab. (*Lihat file `Data_Preprocessing_OptiLocate.ipynb` untuk source code pengolahan data*).
3. Cloud Storage: Dataset yang telah dibersihkan di-hosting di **Microsoft Azure Blob Storage** untuk memastikan *fail-safe mechanism* dan kecepatan akses data tingkat *enterprise*.
4. Front-End / Deployment: Antarmuka web interaktif dibangun menggunakan **Streamlit** dan di-deploy melalui Streamlit Community Cloud.

Kriteria Penilaian AI (Scoring Weights)
Sistem OptiLocate memberikan skor 0-100 pada setiap kelurahan dengan mempertimbangkan 3 variabel utama:
* Populasi (Bobot 50%):Mencari kepadatan penduduk tertinggi untuk menjamin besarnya target pasar.
* Aksesibilitas (Bobot 30%): Memperhitungkan jumlah halte/titik transportasi umum terdekat untuk mobilitas konsumen.
* Tingkat Persaingan (Bobot 20%): Menghitung jumlah kompetitor sejenis di area tersebut. Semakin sedikit kompetitor, semakin tinggi skornya.

Cara Mengakses Aplikasi
Aplikasi ini sudah di-deploy dan dapat diakses secara publik melalui tautan berikut:
[Buka Aplikasi OptiLocate](https://datathonoptilocate.streamlit.app/)
