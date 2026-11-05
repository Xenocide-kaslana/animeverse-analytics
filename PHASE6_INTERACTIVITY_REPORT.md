# Tahap 6 - Advanced Interactivity

## Status

Tahap 6 berhasil diimplementasikan pada aplikasi Streamlit yang sudah berjalan. Tidak ada perubahan pada dataset, preprocessing, atau analytics engine.

## Fitur yang ditambahkan

- Filter global Score Tier dan Popularity Tier.
- Reset Filters menggunakan callback session state, sehingga widget tidak diubah setelah instantiation pada run yang sama.
- Export CSV filtered aktif dari `anime_clean.parquet`.
- CSV menggunakan encoding UTF-8-SIG.
- Pencarian anime berdasarkan `title_english`, `title_romaji`, dan `title_japanese`.
- Empty state untuk pencarian yang tidak menghasilkan data.
- Detail anime melalui select box.
- Detail menggunakan nama kolom aktual dataset, termasuk `duration_min`.
- Nilai yang tidak tersedia ditampilkan sebagai "Tidak tersedia".
- Ranking rating memiliki minimum MAL members.
- Pilihan ranking tambahan untuk MAL Score, MAL Members, MAL Favorites, Popularity, dan MAL Rank.
- Komponen tabel interaktif reusable dengan search, sort, pagination, jumlah hasil, dan CSV export.

## File yang diubah

- `app.py`
- `src/ui_components.py`
- `pages/3_Rating_Popularity.py`
- `PHASE6_INTERACTIVITY_REPORT.md`

## Validasi runtime

- Semua modul Python berhasil dikompilasi dengan `python -m compileall`.
- Aplikasi berhasil dijalankan ulang dengan:
  `streamlit run app.py`
- Server lokal: `http://127.0.0.1:8501`.
- Executive Overview berhasil dimuat dengan 4 Plotly chart.
- Anime Trends berhasil dimuat tanpa error dashboard.
- Rating & Popularity berhasil dimuat tanpa error dashboard.
- Studio & Genre berhasil dimuat tanpa error dashboard.
- Streaming Analysis berhasil dimuat tanpa error dashboard.

## Pengujian interaktivitas

- Search input tersedia dengan placeholder English, Romaji, dan Japanese title.
- Pencarian `Naruto` menghasilkan select anime dan detail.
- Select box detail anime berhasil ditemukan pada hasil pencarian.
- Tombol Download Filtered CSV berhasil dirender.
- CSS dan layout responsive tetap aktif.
- Viewport mobile `390 x 844` menghasilkan:
  - Lebar body: 390 px.
  - Lebar viewport: 390 px.
  - Tidak ada horizontal overflow.
- Filter Score Tier dan Popularity Tier berhasil dirender pada sidebar.
- Tombol Reset Filters berhasil dirender dengan callback.

## Data yang ditampilkan

- Poster hanya ditampilkan jika `image_url` memiliki URL http/https valid; informasi lain tetap memakai nilai asli.
- Missing values tidak diganti dengan nilai buatan pada field detail.
- Search tidak mengubah atau menduplikasi dataset; hanya memilih subset untuk detail.
- Export memakai subset DataFrame yang mengikuti filter global aktif.
