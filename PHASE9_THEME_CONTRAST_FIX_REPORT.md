# PHASE9 - Theme Contrast Fix Report

## Status pengujian

Pemeriksaan dan perbaikan visual Phase 9 telah dijalankan pada server Streamlit lokal dan browser Playwright.

## Pengujian desktop lanjutan

Pengujian pada ukuran `1366 x 768` menemukan bahwa sidebar sempat tersimpan dalam keadaan collapse.
Perbaikan desktop memastikan sidebar:

- terbuka otomatis dengan lebar `280px`,
- diposisikan tetap di sisi kiri,
- menggeser konten utama ke kanan,
- tidak menutup header atau KPI.
- kontrol collapse bawaan disembunyikan pada desktop agar tidak tampil sebagai ikon panah ganda,
- seluruh tab navigasi top dibiarkan satu baris pada desktop dan dapat digeser bila lebar viewport tidak cukup.

Pada desktop, area aplikasi:

- menggunakan lebar konten `1086px` pada viewport `1366px`,
- tidak memiliki horizontal overflow,
- menampilkan identitas, navigasi horizontal, KPI, dan grafik dalam satu layar web.

Indikator radio hitam bawaan Streamlit telah disembunyikan dan diganti dengan active state lavender.

## Root cause

- Plotly memakai konfigurasi transparan dan font bawaan Streamlit yang pucat untuk tick label.
- Konfigurasi axis pada `src/charts.py` belum menetapkan tick font, title font, legend, dan hover label secara konsisten.
- Marker tema hanya mengandalkan perubahan kelas melalui JavaScript, sehingga sinkronisasi CSS dark/light tidak selalu diterapkan.
- Warna beberapa komponen Streamlit masih mengikuti default.
- Radio navigasi sidebar masih menampilkan indikator bulat bawaan Streamlit.

## Perubahan

### Tema terpusat

- `src/theme.py` diperbarui dengan warna teks, teks sekunder, border, grid, dan Plotly card berdasarkan tema aktif.
- Dark mode menggunakan:
  - background `#171426`
  - sidebar `#120F20`
  - card `#242039`
- Light mode menggunakan:
  - background `#FAF8FF`
  - sidebar `#F0EAFB`
  - card `#FFFFFF`

### Plotly

- Semua grafik dikelola oleh `themed_layout()` di `src/charts.py`.
- Konfigurasi mencakup:
  - paper dan plot background
  - font utama
  - title font
  - tick font sumbu X dan Y
  - title axis
  - grid dan line axis
  - legend
  - hover label
  - colorway pastel
- Grafik kosong juga menerapkan tema agar tidak kembali ke template bawaan.

### Sinkronisasi tema

- `app.py` menambahkan marker tema berdasarkan state Streamlit yang aktif.
- `assets/style.css` menerapkan tema melalui marker, tidak lagi bergantung pada JavaScript untuk seluruh styling.
- Tema berpengaruh pada background, sidebar, header, KPI, chart card, tabel, input, filter, dan dropdown.

### Sidebar

- Indicator radio bulat bawaan disembunyikan pada sidebar.
- Navigasi aktif memakai lavender `#C5ADED`.
- Warna label aktif memakai teks navy gelap agar kontras.

### Koreksi kerangka web desktop

- Frame aplikasi desktop diposisikan pada `280px` dari kiri sesuai sidebar.
- Navigasi horizontal dipaksa satu baris dengan scroll kecil jika diperlukan pada viewport sempit.
- Subtitle identitas ditetapkan pada warna sekunder sesuai tema aktif.
- Dark mode terbukti mengubah latar aplikasi menjadi `rgb(23, 20, 38)`, sidebar menjadi
  `rgb(18, 15, 32)`, dan teks identitas menjadi kontras pada dark mode.

## Hasil pengujian Light Mode

Pengujian visual aktif pada server Streamlit baru:

- Plotly pertama memiliki:
  - `paper_bgcolor = #FFFFFF`
  - `plot_bgcolor = #FFFFFF`
  - tick font `#655D78`
- Label sumbu ter-render dengan kontras `rgb(101, 93, 120)`.
- App background: `rgb(250, 248, 255)`.
- Sidebar background: `rgb(240, 234, 251)`.
- Tidak ada horizontal overflow pada desktop dan mobile.
- KPI: 4 kartu tampil pada Ringkasan Utama.

## Hasil pengujian Dark Mode

- Plotly pertama memiliki:
  - `paper_bgcolor = #242039`
  - `plot_bgcolor = #242039`
  - tick font `#C3BAD8`
- Label sumbu ter-render dengan kontras `rgb(195, 186, 216)`.
- App background: `rgb(23, 20, 38)`.
- Sidebar background: `rgb(18, 15, 32)`.
- Tema berbeda nyata dari light mode pada halaman, sidebar, dan grafik.

## Pengujian kelima halaman

Pada dark mode:

- Ringkasan Utama: 4 grafik, tanpa traceback.
- Tren Anime: 6 grafik, tanpa traceback.
- Rating & Popularitas: 4 grafik, tanpa traceback.
- Studio & Genre: 6 grafik, tanpa traceback.
- Analisis Platform Streaming: 4 grafik, tanpa traceback.

Seluruh halaman memiliki pemeriksaan overflow `false` pada desktop.

## Pengujian responsif

- Mobile 390 px:
  - Light mode: tanpa overflow, lebar `390/390`.
  - Dark mode: tanpa overflow, lebar `385/385`.
- Sidebar dapat dibuka dan ditutup pada mobile.
- Tema dapat diganti setelah sidebar dibuka kembali.

## Kompilasi dan server

- `python -m compileall -q app.py src pages`: berhasil.
- Streamlit health check: HTTP 200.
- Server telah direstart agar proses Python memuat kode tema terbaru.
- Uji browser:
  - identitas tetap terlihat,
  - `RAFFI KURNIAWAN` tampil,
  - `NIM 241041001` tampil,
  - tidak ada `Traceback`, `KeyError`, `ValueError`, atau `TypeError`.

## File diperbarui

- `src/theme.py`
- `src/charts.py`
- `app.py`
- `assets/style.css`

## Koreksi kontras lanjutan

Pengujian screenshot menunjukkan bahwa beberapa widget bawaan Streamlit masih menggunakan warna
default setelah perubahan tema. Override hierarki komponen ditambahkan untuk memastikan:

- Light Mode: label, nilai KPI, subtitle, deskripsi, dan placeholder menggunakan warna gelap
  yang terbaca pada latar putih.
- Dark Mode: label KPI dan subtitle sekunder menggunakan `#C3BAD8`, sedangkan judul dan nilai
  utama menggunakan `#F8F5FF`.
- Multiselect menggunakan latar putih pada Light Mode dan `#242039` pada Dark Mode.
- Field multiselect, teks placeholder, dropdown, tabel, dan elemen sekunder tidak lagi kembali
  ke background hitam Streamlit bawaan pada Light Mode.

Pemeriksaan browser terbaru pada kedua tema menghasilkan:

- Dark Mode: label KPI `rgb(195, 186, 216)`, nilai KPI `rgb(248, 245, 255)`.
- Light Mode: label KPI `rgb(101, 93, 120)`, nilai KPI `rgb(33, 22, 77)`.
- Tidak ada horizontal overflow pada viewport desktop.

## Backup

- `src/theme.py.phase9-theme.bak`
- `src/charts.py.phase9-theme.bak`
- `app.py.phase9-theme.bak`
- `assets/style.css.phase9-theme.bak`
