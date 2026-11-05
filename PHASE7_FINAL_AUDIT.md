# PHASE7 FINAL AUDIT

## Status

Audit akhir Stage 7 selesai pada aplikasi lokal. Dataset tetap berjumlah 20.000 baris dan tidak ada penggantian data dummy atau perubahan struktur hasil preprocessing.

## Penyebab dan koreksi

### Pemetaan ranking

Label tampilan seperti `Popularitas`, `Peringkat MAL`, dan `Skor MAL` dipisahkan dari nama kolom dataset melalui pemetaan pada halaman Rating & Popularitas. Peringkat kini diproses oleh `rank_anime()` dengan kolom nyata:

- `Skor MAL`: `mal_score`
- `Jumlah Anggota MAL`: `mal_members`
- `Favorit MAL`: `mal_favorites`
- `Popularitas`: `mal_popularity`
- `Peringkat MAL`: `mal_rank`

### Nilai kosong

Kolom ranking dan skor dikonversi dengan `pd.to_numeric(..., errors="coerce")`. Nilai `pd.NA`, `NaN`, dan nilai nonnumerik tidak dikirim ke operasi perhitungan atau `float()` tanpa validasi.

### Visualisasi skor

Histogram menerima nama kolom dataframe yang valid dan membuat dataframe plot berupa nilai numerik bertipe float. Perbandingan MAL/AniList menggunakan kolom `skor_mal_anilist`, bukan kolom `score` yang tidak ada pada dataset.

### Filter tahun

Filter tahun aktif sekarang mengecualikan baris tanpa tahun. Sebelumnya baris dengan tahun kosong dipertahankan karena dievaluasi bersama rentang tahun, meskipun tidak termasuk rentang yang dipilih.

## File diperbaiki dan backup

- `src/analytics.py`
  - backup: `src/analytics.py.bak`
  - ditambahkan `rank_anime()` untuk kelima ukuran ranking.
  - fungsi ranking berbasis members dan favorites dibuat aman terhadap tipe nullable dan nilai numerik tidak valid.
- `src/charts.py`
  - backup: `src/charts.py.bak`
  - histogram mengonversi nilai dengan aman dan tidak mengirim `pd.NA` ke Plotly.
- `pages/3_Rating_Popularity.py`
  - backup: `pages/3_Rating_Popularity.py.bak`
  - ranking UI menggunakan pemetaan kolom dan fungsi ranking terpusat.
  - histogram perbandingan MAL/AniList tidak lagi mencari kolom `score`.
- `src/data_filters.py`
  - backup lanjutan: `src/data_filters.py.phase7-final.bak`
  - tahun kosong tidak dipertahankan ketika filter rentang tahun aktif.

## Pengujian filter

| Pengujian | Hasil |
|---|---:|
| Drama | 2.505 |
| Masterpiece | 15 |
| MADHOUSE | 356 |
| MADHOUSE + Masterpiece | 2 |
| TV + Winter + Drama | 187 |
| Rentang tahun aktif | Baris tahun kosong: 0 |

## Pengujian ranking

Kelima ranking menghasilkan 10 baris pada data penuh:

- Skor MAL
- Jumlah Anggota MAL
- Favorit MAL
- Popularitas
- Peringkat MAL

## Pengujian visualisasi

- Histogram perbandingan memiliki satu trace Plotly.
- Scatter MAL vs members memiliki satu trace Plotly.
- Korelasi Pearson pada data penuh: `0,3781595477791461`.
- Dataset uji tetap berukuran 20.000 baris dan 56 kolom.

## Pengujian halaman

Kelima halaman dibuka melalui browser Streamlit dan tidak memunculkan `KeyError`, `ValueError`, `TypeError`, atau traceback:

1. Ringkasan Utama
2. Tren Anime
3. Rating & Popularitas
4. Studio & Genre
5. Analisis Platform Streaming

## Health check dan kompilasi

- `python -m compileall -q app.py src pages`: berhasil.
- Streamlit endpoint `/_stcore/health`: HTTP 200.
- Import kelima modul halaman: berhasil.
