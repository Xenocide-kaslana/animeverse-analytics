# Laporan Perbaikan Bug Tahap 7

## Status pengujian

Perbaikan dilakukan pada jalur filter global, pemetaan peringkat Rating & Popularitas, nilai kosong, visualisasi skor, dan state data kosong. Pengujian dilakukan terhadap dataset Parquet aktual, tanpa data dummy dan tanpa mengubah jumlah 20.000 baris.

## Ringkasan penyebab error

### `KeyError: 'Popularitas'`

Pilihan ranking ditampilkan sebagai label `"Popularitas"`, tetapi pemetaan masih menggunakan kunci lama `"Popularity"`. Jadi pilihan UI tidak dapat ditemukan pada dictionary kolom.

Perbaikan:

- Pemetaan ranking diselaraskan dengan label yang ditampilkan.
- Label UI dipisahkan dari kolom dataset:
  - `Popularitas` -> `mal_popularity`
  - `Peringkat MAL` -> `mal_rank`
  - `Skor MAL` -> `mal_score`
  - `Jumlah Anggota MAL` -> `mal_members`
  - `Favorit MAL` -> `mal_favorites`

### `KeyError: 'score'`

Visualisasi perbandingan MAL dan AniList membuat kolom bernama `"Skor"` dengan Unicode lokal, tetapi kode histogram mencoba mencari kolom `"score"`.

Perbaikan:

- Kolom hasil komposisi diganti dengan nama sumber yang konsisten dan valid pada histogram, yaitu `skor_mal_anilist`.
- Nama kolom dataset asli `mal_score` dan `anilist_score` tidak diubah.

### Ambiguitas truth value array

Pemfilteran genre menangani `genre_list`, yang bertipe array NumPy pada Parquet. Operasi normalisasi atau pemeriksaan `set(values or [])` dapat memproses array sebagai nilai boolean tunggal.

Perbaikan:

- Diperkuat pemeriksaan container list/tuple/set/NumPy array/Pandas Series.
- Logika genre dipindahkan ke fungsi filter murni pada `src/data_filters.py`.
- Array genre selalu dikonversi ke list, nilai kosong dipastikan tidak ambigu, lalu dibandingkan menggunakan intersection set.

### `TypeError: float() argument must be a string or a real number, not 'NAType'`

Konversi angka dapat menerima `pd.NA` pada data kosong, terutama pada KPI dan kolom numerik gabungan saat kombinasi Studio MADHOUSE dengan Kategori Skor Masterpiece menghasilkan subset terbatas atau saat subset kosong.

Perbaikan:

- Konversi numerik menggunakan `pd.to_numeric(..., errors="coerce")`.
- Nilai `pd.NA`, `NaN`, dan `None` dipisahkan sebelum `float()`.
- Rata-rata kosong mengembalikan `None` dan ditampilkan sebagai `"Tidak tersedia"` pada KPI.
- Korelasi dan insight juga memeriksa nilai numerik yang hilang.

## File yang diperbaiki

- `app.py`
  - Filter global menggunakan fungsi filter terpusat.
  - Kombinasi filter yang tidak menghasilkan data menampilkan empty state.
- `src/data_filters.py`
  - Fungsi baru untuk filter murni dan aman terhadap array genre.
- `pages/3_Rating_Popularity.py`
  - Pemetaan ranking diperbaiki.
  - Visual perbandingan skor menggunakan nama kolom yang benar.
- `src/analytics.py`
  - Mean, korelasi, insight, dan KPI menggunakan konversi numerik aman.
- `src/charts.py`
  - Histogram dan scatter mengabaikan kolom kosong dan mengonversi nilai secara aman.
- `pages/1_Executive_Overview.py`
  - KPI menampilkan `"Tidak tersedia"` jika subset tidak memiliki rata-rata.

## Pengujian filter aktual

| Kombinasi | Jumlah hasil aktual |
|---|---:|
| Genre Drama | 2.505 |
| Kategori Skor Masterpiece | 15 |
| Studio MADHOUSE | 356 |
| Studio MADHOUSE + Kategori Skor Masterpiece | 2 |
| Genre Drama + Studio MADHOUSE | 126 |
| Jenis Anime TV + Musim winter + Genre Drama | 187 |

Dataset awal berhasil dipertahankan:

- Jumlah baris: 20.000.
- `genre_list` aktual bertipe array NumPy pada Parquet.
- Filter Drama menghasilkan baris dengan genre Drama pada setiap hasil yang diuji.
- Filter TV dan winter menghasilkan hanya tipe TV serta musim `winter`.

## Pengujian edge case

- Data kosong menghasilkan KPI dengan nilai `None` dan tidak mengubah nilai source.
- Visualisasi histogram tidak menghasilkan error untuk DataFrame kosong atau kolom numerik kosong.
- Scatter mengonversi koordinat dengan `errors="coerce"` dan menghapus pasangan yang tidak lengkap.
- Filter Genre yang menerima `genre_list` sebagai list, tuple, set, NumPy array, Series, atau nilai scalar aman diproses.
- Kombinasi filter dapat menghasilkan empty state tanpa menghentikan aplikasi secara membalut error.

## Pengujian regresi

### Kompilasi Python

Hasil:

- `python -m compileall -q app.py src pages` berhasil.

### Health Streamlit

Hasil:

- Health endpoint `/ _stcore/health` mengembalikan HTTP 200.

### Halaman

| Halaman | Status pengujian |
|---|---|
| Ringkasan Utama | Dibuka melalui browser lokal; KPI, navigasi, dan judul Indonesia berhasil ditampilkan. |
| Tren Anime | Dibuka melalui sesi browser lokal dan modul Indonesia berhasil ditampilkan. |
| Rating & Popularitas | Dibuka melalui browser lokal tanpa `Dashboard error`; judul dan analisis skor/popularitas tampil. |
| Studio & Genre | Halaman berhasil dikompilasi dan siap diuji pada navigasi aktif. |
| Analisis Platform Streaming | Halaman berhasil dikompilasi dan siap diuji pada navigasi aktif. |

## Error yang masih tersisa

Tidak ada error reproduksi yang tersisa pada jalur filter yang diuji secara programatik pada saat laporan ini dibuat. Ringkasan utama dan halaman Rating & Popularitas berhasil diuji pada browser tanpa traceback. Pengujian interaktif otomatis untuk setiap opsi Streamlit belum dapat dijalankan sepenuhnya dalam sesi browser ini.

## Pemeriksaan lanjutan `data_filters.py`

Pemeriksaan pada fase lanjutan dilakukan langsung terhadap isi file yang benar-benar tersimpan:

- `src/data_filters.py` tidak terpotong dan seluruh fungsi filter tersedia.
- Normalisasi pilihan mendukung nilai tunggal, list, tuple, set, NumPy array, Pandas Series, dan Pandas Index.
- Genre diproses secara eksplisit untuk list/array/Series dan tidak dievaluasi sebagai boolean.
- Konversi tahun hanya terjadi pada nilai numerik yang valid; tahun kosong tidak dipaksa menjadi angka.
- Kategori skor dan kategori popularitas difilter dengan nama kolom dataset asli.

Workspace tidak diinisialisasi sebagai repository Git pada pemeriksaan ini. Oleh karena itu, Git status dan Git diff untuk `src/data_filters.py` tidak tersedia; pemeriksaan dilakukan terhadap file tersimpan, import Python, dan hasil eksekusi fungsi.

### Hasil uji lanjutan

| Kombinasi | Jumlah hasil aktual |
|---|---:|
| Genre Drama | 2.505 |
| Kategori Skor Masterpiece | 15 |
| Studio MADHOUSE | 356 |
| Studio MADHOUSE + Kategori Skor Masterpiece | 2 |
| Jenis Anime TV + Musim winter + Genre Drama | 187 |
| Kombinasi tidak mungkin | 0 |

### Hasil pemeriksaan kelima halaman melalui Streamlit

| Halaman | Hasil |
|---|---|
| Ringkasan Utama | Berhasil dibuka; tidak ditemukan traceback atau exception pada halaman. |
| Tren Anime | Berhasil dibuka; judul "Tren Anime" dan seluruh visualisasi tampil. |
| Rating & Popularitas | Berhasil dibuka; pemilihan halaman tidak menimbulkan `KeyError`, `ValueError`, atau `TypeError`. |
| Studio & Genre | Berhasil dibuka; halaman tidak menimbulkan traceback saat navigasi. |
| Analisis Platform Streaming | Berhasil dibuka; halaman tidak menimbulkan traceback saat navigasi. |

Pengujian akhirnya mencatat:

- `python -m compileall -q app.py src pages`: berhasil.
- Streamlit health endpoint: HTTP 200.
- Tidak ditemukan `KeyError`, `ValueError`, atau `TypeError` pada snapshot browser kelima halaman.
- `data_filters.py` tersimpan lengkap dan dapat digunakan oleh aplikasi saat ini.
