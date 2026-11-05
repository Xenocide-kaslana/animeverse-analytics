# Tahap 5 - Implementasi Lima Halaman Dashboard

## Status

Tahap 5 berhasil diimplementasikan dan diuji pada server Streamlit lokal.

## Halaman yang diuji

| Halaman | Chart/visualisasi terdeteksi | Status |
|---|---:|---|
| Executive Overview | 4 | Berhasil |
| Anime Trends | 6 | Berhasil |
| Rating & Popularity | 3 | Berhasil |
| Studio & Genre | 8 | Berhasil |
| Streaming Analysis | 4 | Berhasil |

Seluruh halaman berhasil dibuka tanpa `Dashboard error` setelah proses Streamlit lama direfresh dengan source terbaru.

## Implementasi halaman

- Executive Overview: KPI portofolio, distribusi type, tren rilis, distribusi score tier, dan top genre beserta insight aktual.
- Anime Trends: tren tahunan, decade, season, type, source material, dan distribusi episode.
- Rating & Popularity: ranking MAL score dengan minimum members, ranking members, ranking favorites, distribusi score, scatter score-members, perbandingan MAL/AniList, dan popularity tier.
- Studio & Genre: ranking studio, average score studio minimum 5 anime, genre frequency, average score genre, heatmap studio-genre, dan distribusi genre berdasarkan type.
- Streaming Analysis: count dan average score per platform, distribusi jumlah platform, platform vs genre, serta tabel anime multi-platform.

## Filter dan navigasi

- Navigasi lima halaman tersedia pada sidebar.
- Filter global tersedia untuk release year, anime type, season, genre, dan studio.
- Tombol Reset Filters tersedia dan memiliki state widget yang terpisah dari navigasi dan theme.
- Filter data dijalankan pada satu DataFrame hasil Parquet dan tidak mengubah dataset sumber.
- Filter genre dan studio dieksekusi pada kolom eksplisit sehingga agregasi genre tidak menggandakan baris KPI.

## Tema

- Light dan Dark tersedia dan preference disimpan pada session Streamlit.
- Background dark aktif menggunakan `#17152B`.
- Pengujian computed background pada Dark mode menghasilkan `rgb(23, 21, 43)`.

## Responsivitas

Pengujian viewport `390 x 844` menghasilkan:

- Lebar body: 390 px.
- Lebar viewport: 390 px.
- Lebar aplikasi: 390 px.
- Tidak ada horizontal overflow terdeteksi.

## Perbaikan yang diperlukan selama pengujian

1. Kolom `num_platforms` yang tidak tersedia dihapus dari tabel multi-platform. Dataset hanya menghasilkan kolom `platform_count`.
2. `Styler.background_gradient` pada Studio & Genre memerlukan matplotlib yang tidak diperlukan. Bagian genre-type diganti dengan Plotly heatmap tanpa dependency tambahan.
3. Streamlit server lama direstart agar module Python dan perubahan halaman terbaru benar-benar dimuat.
4. Navigasi multipage bawaan Streamlit disembunyikan agar tidak bertabrakan dengan navigasi kustom aplikasi.

## Validasi runtime

- Kompilasi seluruh `app.py`, `src`, dan `pages`: berhasil.
- Semua lima halaman: berhasil dibuka.
- Tidak ditemukan `Dashboard error` pada kelima halaman saat pengujian akhir.
- Aplikasi dapat dijalankan dengan `streamlit run app.py`.
- URL pengujian lokal: `http://127.0.0.1:8501`.

## File yang diubah pada Tahap 5

- `app.py`
- `src/charts.py`
- `src/ui_components.py`
- `assets/style.css`
- `pages/1_Executive_Overview.py`
- `pages/2_Anime_Trends.py`
- `pages/3_Rating_Popularity.py`
- `pages/4_Studio_Genre.py`
- `pages/5_Streaming_Analysis.py`
- `PHASE5_DASHBOARD_REPORT.md`

