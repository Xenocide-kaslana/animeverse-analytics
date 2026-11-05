# PHASE8 - Visual Redesign Report

## Status

Redesign visual AnimeVerse Analytics telah diterapkan langsung pada file proyek dan diuji pada aplikasi Streamlit lokal.

## File diperbarui

- `app.py`
- `src/theme.py`
- `src/charts.py`
- `src/ui_components.py`
- `assets/style.css`
- `PHASE8_VISUAL_REDESIGN_REPORT.md`

Backup dibuat sebelum perubahan:

- `app.py.redesign.bak`
- `src/theme.py.redesign.bak`
- `src/charts.py.redesign.bak`
- `src/ui_components.py.redesign.bak`
- `assets/style.css.redesign.bak`

## Desain yang diterapkan

- Header dashboard berisi `ANIMEVERSE ANALYTICS` dan subtitle `Anime Industry Intelligence Dashboard`.
- Identitas mahasiswa ditampilkan:
  - RAFFI KURNIAWAN
  - NIM 241041001
  - Visualisasi Data — Ganjil 2026/2027
- Sidebar diperbarui dengan identitas mahasiswa dan navigasi compact.
- Navigasi horizontal Spotify-inspired ditambahkan dengan pemilihan:
  - Ringkasan
  - Tren Anime
  - Rating & Popularitas
  - Studio & Genre
  - Streaming
- KPI diberi aksen pastel yang konsisten.
- Card, sidebar, tabel, insight, chart container, dan empty state mengikuti tema.
- Plotly menggunakan lima warna pastel utama sebagai colorway.
- Layout mobile menghindari horizontal overflow pada viewport yang diuji.

## Palette warna

- Lavender: `#C5ADED`
- Pink: `#F8ABEB`
- Soft Pink: `#FFC8DD`
- Baby Blue: `#BCE0FF`
- Sky Blue: `#A2D2FF`
- Light background: `#FAF8FF`
- Light sidebar: `#F0EAFB`
- Light text: `#21164D`
- Dark background: `#171426`
- Dark sidebar: `#120F20`
- Dark card: `#242039`
- Dark text: `#F8F5FF`

## Fitur yang dipertahankan

- Filter global.
- Reset filter.
- Search anime.
- Detail anime.
- Ranking.
- Sorting tabel.
- Pagination.
- Export CSV.
- Light mode dan dark mode.
- Kelima halaman dashboard.
- Engine analytics dan dataset Parquet 20.000 baris.

## Pengujian aktual

### Kompilasi dan server

- Compile seluruh `app.py`, `src`, dan `pages`: berhasil.
- Rekompilasi setelah perbaikan format KPI: berhasil.
- Streamlit health endpoint: HTTP 200.

### Navigasi halaman

Kelima tab berhasil dibuka melalui browser tanpa `Traceback`, `KeyError`, `ValueError`, atau `TypeError`:

1. Ringkasan
2. Tren Anime
3. Rating & Popularitas
4. Studio & Genre
5. Streaming

Pada sesi Playwright baru, konten setiap halaman teridentifikasi melalui judul halaman masing-masing.
Ringkasan Utama menampilkan empat kartu KPI, tanpa titik hitam atau nilai kosong.

Nilai KPI aktual Ringkasan Utama pada data yang difilter:

- Jumlah Anime: `19.061`
- Rata-rata Skor MAL: `6,47`
- Jumlah Studio Valid: `1.223`
- Rata-rata Anggota MAL: `62.432`

Format ribuan pada kartu Jumlah Anime dan Jumlah Studio Valid telah diperbaiki dari
format berbahasa Inggris menjadi format Indonesia dengan pemisah titik.

### Tema

- Light mode berhasil dipilih dan aplikasi tetap dapat dirender.
- Dark mode berhasil dipilih dan halaman tetap dapat dirender.
- Dark mode menghasilkan warna latar aplikasi `rgb(23, 20, 38)`.
- Light mode menghasilkan warna latar aplikasi `rgb(250, 248, 255)`.
- Identitas mahasiswa tetap tampil pada kedua tema.

### Responsive

Tidak ada horizontal overflow pada viewport:

- 390 px: tidak ada overflow.
- 768 px: tidak ada overflow.
- 1366 px: tidak ada overflow.
- 1920 px: tidak ada overflow.

Browser action yang semula gagal diselidiki sebagai kegagalan target klik:
aksi mencoba mengklik elemen sidebar di luar viewport, bukan exception pada aplikasi.
Pengujian diulang pada sesi browser baru dan navigasi horizontal berhasil.

### Filter

Hasil filter tetap valid:

- Drama: 2.505
- Masterpiece: 15
- MADHOUSE: 356
- MADHOUSE + Masterpiece: 2
- TV + Winter + Drama: 187

Dataset tetap berjumlah 20.000 baris.

### Pengujian browser

- Browser action awal gagal karena target tampilan sidebar berada di luar viewport.
- Sesi Playwright baru berhasil memuat seluruh halaman.
- Navigasi horizontal kelima halaman berhasil.
- Tidak ditemukan traceback atau exception kelas Python pada teks halaman.
- Identitas `RAFFI KURNIAWAN` dan `NIM 241041001` tampil.
- Tema gelap dan terang berhasil diterapkan.
- KPI Ringkasan Utama memuat empat nilai numerik dan tidak menampilkan titik kosong.

## Masalah yang masih tersisa

- Belum ada browser automation penuh untuk setiap dropdown filter individual dan alur export file dalam sesi ini.
- Pengujian visual screenshot desktop/mobile tidak disimpan sebagai aset laporan.
