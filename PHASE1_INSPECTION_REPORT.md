# Tahap 1 - Laporan Inspeksi Dataset

## Status

Tahap inspeksi selesai berhasil dan sebelum preprocessing, tidak ada nilai baris yang diubah atau dihapus.

## Ringkasan Dataset

- Sumber asli: `data/raw/anime_dataset_20k.csv`
- Ukuran: **20.000 baris x 50 kolom**
- Rentang tahun: **1917-2026**
- Kolom identitas, produksi, skor, popularitas, genre, dan platform tersedia sesuai rancangan.
- Duplicate `mal_id`: **0**
- Nilai rating MAL dan AniList berada dalam rentang 0-10; tidak ditemukan skor di luar rentang.
- Tidak ditemukan episode negatif.
- Terdapat **147** baris dengan `episodes = 0`; nilai tersebut memerlukan review sebagai nilai khusus/unknown, bukan dipakai sebagai episode valid.

## Temuan Kualitas Data

Kolom dengan missing values signifikan:

| Kolom | Jumlah | Persentase |
|---|---:|---:|
| `streaming_platforms` | 12.632 | 63.16% |
| `title_synonyms` | 8.484 | 42.42% |
| `top_tags` | 7.133 | 35.66% |
| `studios_all` | 5.312 | 26.56% |
| `mal_rank` | 4.873 | 24.37% |
| `anilist_score` | 3.484 | 17.42% |
| `anilist_score_100` | 3.484 | 17.42% |
| `year`, `decade`, dan `season_year` | 939 | 4.70% |

Kolom `genres` tidak memiliki missing values. Sumber data memiliki 939 baris tanpa tahun/season sekaligus.
Kolom `streaming_platforms` kosong akan diperlakukan sebagai tidak tercatat, bukan sebagai bukti anime tidak tersedia pada platform streaming.

## Distribusi Format

- TV: 5.449
- OVA: 3.590
- MOVIE: 3.005
- ONA: 2.647
- MUSIC: 2.557
- SPECIAL: 1.520
- TV_SPECIAL: 621
- CM: 382
- PV: 228
- UNKNOWN: 1

## Normalisasi Tahap Berikutnya

- Nilai `season` mengandung campuran lowercase dan uppercase; preprocessing akan mengubah seluruhnya menjadi lowercase.
- `studio_main` memiliki **4.044** baris blank/Unknown dan akan dipisahkan dari peringkat studio.
- Nilai genre akan dipisahkan dengan delimiter `|`.
- Episode bernilai nol tidak akan otomatis diubah menjadi data episode yang salah.
- Nilai platform boolean akan menjadi sumber penandaan tersedia/true; nilai false tetap membedakan tidak tersedia versus kolom teks yang tidak tercatat.

## Batasan

Laporan JSON mesin tersedia di `data/inspection_report.json`. Tahap 2 belum dijalankan.
