# AnimeVerse Analytics

**Anime Industry & Popularity Intelligence Dashboard**

AnimeVerse Analytics adalah aplikasi dashboard berbasis Streamlit untuk mengeksplorasi dan menganalisis data industri anime, pola popularitas, rating, studio produksi, genre, serta informasi ketersediaan platform streaming. Dataset yang digunakan merupakan data nyata berjumlah 20.000 judul anime dan seluruh visualisasi dihasilkan dari data hasil preprocessing, bukan data sintetis.

## Identitas Mahasiswa

- Nama: **RAFFI KURNIAWAN**
- NIM: **241041001**
- Mata Kuliah: **Visualisasi Data**
- Semester: **Ganjil 2026/2027**

## Link Dashboard

- Dashboard Streamlit: [Belum tersedia; tambahkan URL deployment aktif di sini]

Link deployment belum tersedia dan tidak dibuat dalam dokumentasi ini.

## Dataset

Dataset bersumber dari Kaggle:

- [Anime Dataset: 20K Titles and Dual Scores](https://www.kaggle.com/datasets/rudrakumargupta/anime-dataset-20k-titles-and-dual-scores)

Dataset sumber disimpan pada:

```text
data/raw/anime_dataset_20k.csv
```

Dataset hasil pembersihan yang digunakan oleh aplikasi disimpan pada:

```text
data/processed/anime_clean.parquet
```

Karakteristik ringkas dataset:

- 20.000 baris data anime.
- Informasi identitas dan metadata anime.
- Skor MAL pada kolom `mal_score`.
- Skor AniList pada kolom `anilist_score`.
- Jumlah anggota MAL pada `mal_members`.
- Informasi favorit, popularitas, peringkat, tahun rilis, studio, genre, dan platform streaming.
- Nilai kosong dipertahankan dan ditangani sesuai ketersediaan data; nilai kosong tidak diganti dengan nilai yang tidak tersedia di dataset.

## Latar Belakang dan Tujuan

Industri anime menghasilkan data dalam jumlah besar, mencakup skor penonton, popularitas, jumlah anggota komunitas, studio produksi, genre, format tayang, dan platform distribusi. Informasi tersebut dapat digunakan untuk memahami tren produksi, karakteristik genre, pola rating, serta cakupan platform streaming.

Tujuan pengembangan AnimeVerse Analytics adalah menyediakan dashboard yang:

1. Menampilkan ringkasan performa industri anime secara menyeluruh.
2. Membandingkan skor MAL dan AniList sebagai sumber data yang terpisah.
3. Mengidentifikasi tren rilis anime berdasarkan tahun dan dekade.
4. Menganalisis genre dan studio produksi.
5. Membandingkan keberadaan anime pada berbagai platform streaming tanpa menafsirkan data kosong sebagai status tidak tersedia.
6. Memberikan filter, pencarian, detail anime, peringkat, tabel interaktif, dan ekspor CSV.
7. Menyajikan hasil analisis dalam bahasa Indonesia dengan format angka yang konsisten.

## Insight Utama Berdasarkan Analisis Aktual

Berikut ringkasan hasil aktual dashboard pada tampilan awal dengan rentang tahun 1917–2026:

1. **Jenis anime paling banyak adalah TV**, dengan 5.410 judul dari 19.061 anime yang memiliki tahun rilis.
2. **Tahun produksi terbanyak adalah 2021**, dengan 866 judul anime.
3. **Genre paling sering muncul adalah Comedy**, pada 5.778 judul anime.
4. **Studio dengan produksi terbanyak adalah Toei Animation**, dengan 801 judul anime.
5. **Genre dengan rata-rata skor MAL tertinggi pada sampel minimal 30 judul adalah Award Winning**, dengan rata-rata 7,50 dari 210 judul.

Analisis korelasi menunjukkan hubungan linear positif antara `mal_score` dan `mal_members` sebesar 0,382 pada 19.061 anime yang memiliki tahun rilis dan nilai kedua metrik. Nilai korelasi tersebut tidak membuktikan hubungan sebab-akibat.

## Fitur Dashboard

- Ringkasan utama berupa KPI dan visualisasi industri.
- Tren rilis anime berdasarkan tahun, dekade, musim, jenis, materi sumber, dan jumlah episode.
- Analisis skor MAL, AniList, popularitas, favorit, serta peringkat anime.
- Eksplorasi studio dan genre dengan batas minimum sampel.
- Analisis ketersediaan platform streaming berdasarkan status `True`, `False`, dan `Unknown`.
- Filter utama untuk tahun rilis, jenis anime, genre, studio, musim tayang, kategori skor, dan kategori popularitas.
- Pencarian judul anime dalam bahasa Inggris, Romaji, dan Jepang.
- Detail anime beserta poster dan informasi yang tersedia.
- Paginasi tabel dan ekspor hasil yang difilter ke CSV UTF-8-SIG.
- Tema terang dan gelap serta antarmuka berbahasa Indonesia.

## Teknologi

- Python 3.12
- Streamlit
- Pandas
- NumPy
- Plotly
- PyArrow

## Struktur Folder

```text
animeverse-analytics/
├── app.py
├── README.md
├── requirements.txt
├── assets/
│   ├── logo.svg
│   └── style.css
├── data/
│   ├── raw/
│   └── processed/
├── pages/
│   ├── 1_Executive_Overview.py
│   ├── 2_Anime_Trends.py
│   ├── 3_Rating_Popularity.py
│   ├── 4_Studio_Genre.py
│   └── 5_Streaming_Analysis.py
├── scripts/
│   ├── inspect_dataset.py
│   ├── clean_dataset.py
│   └── generate_analytics_report.py
└── src/
    ├── analytics.py
    ├── charts.py
    ├── config.py
    ├── genre_analysis.py
    ├── localization.py
    ├── preprocessing.py
    ├── studio_analysis.py
    ├── streaming_analysis.py
    ├── theme.py
    └── ui_components.py
```

## Persyaratan Sistem

- Python 3.12 direkomendasikan.
- Pip untuk pengelolaan dependency.
- Browser modern untuk menjalankan dashboard.

## Instalasi

1. Masuk ke folder project.

```bash
cd animeverse-analytics
```

2. Buat dan aktifkan virtual environment.

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

3. Pasang dependency.

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Menjalankan Aplikasi Secara Lokal

Pastikan file `data/processed/anime_clean.parquet` tersedia, lalu jalankan:

```bash
streamlit run app.py
```

Aplikasi dapat dibuka melalui alamat lokal yang ditampilkan Streamlit, umumnya:

```text
http://localhost:8501
```

## Menyiapkan Dataset Hasil Olahan

Jika file Parquet hasil cleaning belum tersedia, jalankan:

```bash
python scripts/clean_dataset.py
```

Perintah tersebut membaca dataset sumber pada `data/raw/anime_dataset_20k.csv` dan menyimpan hasil olahannya pada `data/processed/anime_clean.parquet`.

## Validasi Data Utama

Hasil validasi dataset:

- Jumlah baris: 20.000.
- `mal_id` unik: 20.000.
- Rata-rata skor MAL: 6,42.
- Rata-rata anggota MAL: 59.556,85.
- Studio valid unik: 1.243.
- Genre unik: 78.
- Anime tanpa tahun rilis: 939.

## Nilai yang Ditampilkan pada Tampilan Awal Dashboard

Filter tahun aktif secara bawaan untuk rentang 1917–2026. Oleh karena itu, baris yang tidak memiliki tahun rilis tidak termasuk dalam tampilan awal:

- Jumlah anime pada tampilan awal: 19.061.
- Rata-rata skor MAL pada tampilan awal: 6,47.
- Rata-rata anggota MAL pada tampilan awal: 62.432.
- Studio valid pada tampilan awal: 1.223.
