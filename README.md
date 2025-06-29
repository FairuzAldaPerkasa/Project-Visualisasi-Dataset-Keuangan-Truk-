# 🚛 Dashboard Analisis Truk Air Isi Ulang

Dashboard interaktif berbasis Streamlit untuk analisis bisnis operasional truk air isi ulang. Dashboard ini menyediakan insight mendalam tentang kinerja keuangan, operasional, dan efisiensi bisnis pengiriman air.

## 📋 Deskripsi Project

Project ini merupakan sistem analisis data untuk bisnis truk air isi ulang yang memungkinkan pengguna untuk:
- Menganalisis performa keuangan (pemasukan, pengeluaran, laba)
- Memantau operasional pengiriman air
- Menganalisis efisiensi armada dan sopir
- Mengevaluasi pola operasional harian dan bulanan
- Melakukan analisis demografi pengiriman

## 🎯 Fitur Utama

### 1. 💰 Analisis Transaksi Keuangan
- Rekapitulasi total pemasukan, pengeluaran, dan laba bersih
- Analisis trend keuangan bulanan
- Visualisasi perbandingan pemasukan vs pengeluaran

### 2. 🚛 Rekap Pengiriman Air
- Total volume air yang dikirim
- Jumlah pengiriman dan rata-rata volume
- Trend pengiriman bulanan

### 3. 📍 Demografi Pengiriman
- Top 5 lokasi pengiriman berdasarkan volume dan pemasukan
- Analisis trend bulanan per lokasi
- Peta sebaran lokasi (jika data koordinat tersedia)

### 4. 🚚 Penggunaan Armada
- Analisis performa armada berdasarkan volume dan frekuensi
- Korelasi antara penggunaan armada dan biaya operasional
- Trend bulanan per armada

### 5. 👨‍🚀 Kinerja Sopir
- Evaluasi produktivitas sopir berdasarkan volume dan frekuensi tugas
- Analisis korelasi antara kinerja dan pemasukan
- Trend kinerja bulanan per sopir

### 6. ⚡ Efisiensi Operasional
- Kalkulasi efisiensi (Rp/Liter) per bulan, armada, dan sopir
- Analisis profit margin dan ROI
- Identifikasi armada dan sopir paling/kurang efisien

### 7. 📊 Analisis Pola Operasional
- Pola operasional per hari dalam minggu
- Analisis kuartalan untuk perencanaan strategis

### 8. 📈 Analisis Performa Bisnis
- Key Performance Indicators (KPI) bisnis
- Produktivitas dan profitabilitas sopir
- Trend profitabilitas bulanan

## 🛠️ Teknologi yang Digunakan

- **Python 3.8+**
- **Streamlit** - Framework web app
- **Pandas** - Manipulasi dan analisis data
- **Plotly** - Visualisasi data interaktif
- **NumPy** - Komputasi numerik

## 📦 Instalasi

### Prerequisites
```bash
python >= 3.8
pip
```

### Langkah Instalasi

1. **Clone repository**
```bash
git clone https://github.com/username/dashboard-truk-air.git
cd dashboard-truk-air
```

2. **Buat virtual environment (opsional tapi direkomendasikan)**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate     # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Siapkan data**
   - Pastikan file CSV ada di folder `Dataset/Cleaned/`
   - File yang diperlukan: `Sheet2_Cleaned.csv` dan `Sheet3_Cleaned.csv`

## 🚀 Cara Menjalankan

1. **Jalankan aplikasi Streamlit**
```bash
streamlit run dashboard.py
```

2. **Buka browser**
   - Aplikasi akan terbuka otomatis di `http://localhost:8501`
   - Jika tidak, buka manual di browser

3. **Upload data (jika file tidak ditemukan)**
   - Gunakan file uploader di sidebar
   - Upload file `Sheet2_Cleaned.csv` dan `Sheet3_Cleaned.csv`

## 📁 Struktur Project

```
dashboard-truk-air/
│
├── Dashboard/
│   └── dashboard.py          # File utama aplikasi
│
├── Dataset/
│   └── Cleaned/
│       ├── Sheet2_Cleaned.csv    # Data transaksi
│       └── Sheet3_Cleaned.csv    # Data lokasi
│
├── requirements.txt          # Dependencies Python
├── README.md                # Dokumentasi project
└── .gitignore               # File yang diabaikan Git
```

## 📊 Format Data

### Sheet2_Cleaned.csv
Kolom yang diperlukan:
- `Tanggal`: Tanggal transaksi (YYYY-MM-DD)
- `Plat Nomor`: Nomor plat kendaraan
- `Sopir`: Nama sopir
- `Volume (L)`: Volume air dalam liter
- `Pemasukan`: Jumlah pemasukan (Rp)
- `Pengeluaran`: Jumlah pengeluaran (Rp)
- `Order`: Nama lokasi/order

### Sheet3_Cleaned.csv
Kolom yang diperlukan:
- `Nama Lokasi`: Nama lokasi pengiriman
- `Latitude`: Koordinat lintang (opsional)
- `Longitude`: Koordinat bujur (opsional)

## 🎨 Fitur Dashboard

### Navigation
- **Sidebar Navigation**: Pilih jenis analisis yang diinginkan
- **Dataset Selection**: Pilih Sheet 2, Sheet 3, atau gabungan
- **Info Dataset**: Tampilan informasi dataset (jumlah baris, kolom, missing values)

### Visualisasi
- **Bar Charts**: Untuk perbandingan kategori
- **Line Charts**: Untuk trend temporal
- **Scatter Plots**: Untuk analisis korelasi
- **Heatmaps**: Untuk pola aktivitas
- **Maps**: Untuk visualisasi geografis (jika data tersedia)

### Interaktivity
- **Responsive Design**: Optimized untuk desktop dan mobile
- **Dark/Light Mode**: Mendukung tema gelap dan terang
- **Interactive Charts**: Hover, zoom, dan pan pada grafik
- **Real-time Updates**: Update otomatis saat data berubah

## 📈 Insight yang Dihasilkan

Dashboard menghasilkan berbagai insight bisnis seperti:

1. **Keuangan**
   - Bulan dengan profit tertinggi/terendah
   - Trend pertumbuhan revenue
   - Analisis cost structure

2. **Operasional**
   - Hari dengan aktivitas tertinggi
   - Lokasi pengiriman paling menguntungkan
   - Efisiensi operasional per periode

3. **SDM**
   - Sopir dengan performa terbaik
   - Produktivitas per sopir
   - Distribusi beban kerja

4. **Aset**
   - Armada dengan utilisasi tertinggi
   - ROI per kendaraan
   - Maintenance cost analysis

## 🔧 Kustomisasi

### Menambah Analisis Baru
1. Buat fungsi analisis baru di `dashboard.py`
2. Tambahkan opsi menu di `analysis_options`
3. Tambahkan kondisi di fungsi `main()`

### Mengubah Visualisasi
- Edit fungsi plotting yang ada
- Sesuaikan color scheme di CSS
- Modifikasi layout menggunakan Streamlit columns

### Menambah Data Source
- Modifikasi fungsi `load_csv_data()`
- Tambahkan validasi kolom baru
- Update dokumentasi format data

## 🤝 Kontribusi

1. Fork repository
2. Buat branch fitur (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buka Pull Request


## 👥 Tim Pengembang

- **Fairuz Alda Perkasa** - *Developer* - [GitHub](https://github.com/FairuzAldaPerkasa)
- **Mata Kuliah**: Visualisasi Data
- **Semester**: 6
- **Program Studi**: Informatika

## 📞 Support

Jika mengalami masalah atau memiliki pertanyaan:

1. **Issues**: Buat issue di GitHub repository
2. **Documentation**: Lihat dokumentasi di README ini

## 🚧 Roadmap

### Version 2.0 (Future)
- [ ] Machine Learning prediction untuk demand forecasting
- [ ] Real-time data integration
- [ ] Mobile app version
- [ ] Advanced reporting features
- [ ] User authentication system
- [ ] Database integration
- [ ] Export to PDF/Excel functionality

## 📚 Dependencies

```txt
streamlit>=1.28.0
pandas>=1.5.0
numpy>=1.21.0
plotly>=5.15.0
datetime
os
warnings
```

## 🔄 Update Log

### v1.0.0 (Current)
- ✅ Basic dashboard functionality
- ✅ 8 jenis analisis utama
- ✅ Interactive visualizations
- ✅ Responsive design
- ✅ Data upload functionality

---

**📊 Dashboard Analisis Truk Air Isi Ulang** - Membantu optimalisasi bisnis pengiriman air melalui analisis data yang komprehensif.