# Tahap 7 - Final Testing, Quality Assurance, dan Optimization

## Status pengujian

Tahap 7 selesai dengan pengujian actual pada aplikasi Streamlit lokal. Bug yang terverifikasi pada posisi tombol CSV telah diperbaiki. Pengujian data dan halaman dilakukan terhadap Parquet bersih, bukan dataset dummy.

## Data validation

Pengujian dataset `data/processed/anime_clean.parquet` menghasilkan:

- Jumlah baris: 20,000.
- `mal_id` unik: 20,000.
- Average MAL score: 6.415.
- Average MAL members: 59,556.85075.
- Valid studio unik: 1,243.
- Genre unik: 78.
- Anime dengan streaming tercatat: 36.84%.

Hasil KPI dashboard dan analytics engine konsisten pada data tanpa filter.

## Pengujian halaman

| Halaman | Status | Chart terdeteksi |
|---|---|---:|
| Executive Overview | Berhasil | 4 |
| Anime Trends | Berhasil | 4 |
| Rating & Popularity | Berhasil | 4 |
| Studio & Genre | Berhasil | 4 |
| Streaming Analysis | Berhasil | 4 |

Pengujian browser tidak menemukan `Dashboard error` atau traceback pada kelima halaman.

## Functional testing

- Navigasi kelima halaman: berhasil.
- Search input anime: berhasil.
- Search yang tidak ditemukan: berhasil menampilkan empty state "Anime not found".
- Select anime dan detail: berhasil dirender.
- Download Filtered CSV: berhasil dirender setelah page header pada setiap halaman.
- Global filters: tersedia untuk tahun, type, season, genre, studio, score tier, dan popularity tier.
- Reset Filters: menggunakan callback dan tidak mengubah widget lain.
- Ranking MAL: memilih minimum members.
- Ranking metrics: MAL Score, MAL Members, MAL Favorites, Popularity, dan MAL Rank tersedia.
- Filter Studio dan Genre tidak mengubah atau menduplikasi dataset sumber.
- Widget key menggunakan namespace unik.

## Data accuracy

- Genre diekstraksi dan dievaluasi terpisah dari KPI utama.
- Studio Unknown tidak masuk daftar valid studio dan ranking studio.
- Studio average rating menggunakan minimum 5 anime pada analytics.
- MAL dan AniList tetap dipisahkan sebagai kolom dan visualisasi.
- Platform boolean tetap dibedakan sebagai True, False, dan Unknown/missing.
- Nilai year, rating, studio, dan popularity yang kosong tidak diganti pada dashboard.

## Responsive testing

Viewport yang diuji:

| Viewport | Hasil overflow |
|---|---|
| 390 x 844 | Tidak ada |
| 768 x 900 | Tidak ada |
| 1366 x 900 | Tidak ada |
| 1920 x 900 | Tidak ada |

Pengujian aktual menghasilkan:

- Pada seluruh viewport aktual, nilai viewport, body, dan aplikasi sama dengan lebar viewport.

## UI/UX

- Light mode tetap aktif.
- Dark mode mengubah computed background menjadi `rgb(23, 21, 43)`.
- Export CSV dipindahkan ke sidebar setelah area filter karena widget Streamlit dapat terangkat di atas header kustom Markdown.
- Navy violet, sidebar, KPI, chart container, dan filter tetap konsisten.

## Performance

- Dataset hanya dibaca dari Parquet melalui loader dengan `st.cache_data`.
- Tidak ada pembacaan CSV dari halaman dashboard.
- Chart menggunakan data teragregasi.
- Ranking dibatasi 10 baris.
- Search dievaluasi pada subset hasil filter.
- Search text tidak memuat seluruh tabel sekaligus ke browser.

## Error handling

Pengujian dan implementasi menyediakan penanganan untuk:

- Dataset Parquet tidak ditemukan melalui `FileNotFoundError`.
- Search tidak ditemukan melalui empty state.
- Poster tidak valid melalui pesan poster tidak tersedia.
- Field detail kosong melalui label "Tidak tersedia".
- Filter tanpa hasil dapat dirender melalui empty state atau fungsi chart yang mendukung data kosong.

## Bug ditemukan dan diperbaiki

1. Tombol export filter global dirender sebelum judul halaman.
   - Diperbaiki: export dipindahkan ke area aksi sidebar setelah filter dan reset.
2. Import UI yang tidak digunakan pada `app.py`.
   - Diperbaiki: import `csv_download` lama pada entry point dihapus.

## Cleanup

- Semua modul Python berhasil dikompilasi.
- Tidak ditemukan proses duplikasi dashboard pada pengujian browser.
- Widget key utama menggunakan prefix unik.
- Dataset dan analytics engine tidak diubah pada Tahap 7.
- Requirements berisi dependency runtime yang diperlukan.

## Kesiapan deployment

Dashboard siap untuk pengujian deployment lanjutan, tetapi belum di-deploy sesuai instruksi.

Responsivitas 390px, 768px, 1366px, dan 1920px telah diuji tanpa horizontal overflow. Unduhan file aktual perlu verifikasi manual sekali lagi sebelum rilis deployment.

## Lokalisasi Bahasa Indonesia - Tahap 6.5

Status: diterapkan dan diuji pada build lokal.

Implementasi:

- Kamus dan helper format tampilan dipusatkan pada `src/localization.py`.
- Navigasi, tema, filter utama, pencarian, detail anime, komponen tabel, status kosong, dan pesan sistem telah diterjemahkan ke Bahasa Indonesia.
- Kelima judul halaman pada navigasi kini menggunakan nama Indonesia: Ringkasan Utama, Tren Anime, Rating & Popularitas, Studio & Genre, dan Analisis Platform Streaming.
- Judul, subtitel, kontrol, tab, KPI, dan insight pada kelima halaman telah dilokalkan.
- Label Plotly untuk sumbu data dipetakan ke bahasa Indonesia melalui `src/charts.py`.
- Nama kolom dataset, nama anime, nama studio, dan nama platform tetap dipertahankan sesuai sumber.

Pengujian aktual:

- Kompilasi seluruh modul aplikasi berhasil tanpa syntax error.
- Health endpoint Streamlit mengembalikan HTTP 200.
- Browser menampilkan navigasi `Navigasi Utama`, pilihan halaman berbahasa Indonesia, serta tema Terang/Gelap.
- Ringkasan Utama, Tren Anime, Rating & Popularitas, Studio & Genre, dan Analisis Platform Streaming dibuka tanpa `Dashboard error`.
- Tren Anime dan Analisis Platform Streaming berhasil menampilkan judul halaman serta section berbahasa Indonesia pada browser.
- Audit source tidak menemukan label UI lama pada halaman utama, kecuali nama teknis dataset/format yang perlu dipertahankan.

Batas pengujian:

- Pemeriksaan visual label pada seluruh tooltip Plotly dan interaksi browser lanjutan tetap memerlukan verifikasi manual pada sesi browser.
- Dataset, analytics engine, dan struktur Parquet tidak diubah selama lokalisasi.
