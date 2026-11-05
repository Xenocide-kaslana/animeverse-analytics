# Tahap 2 - Cleaning dan Preprocessing

## Status

Pipeline Tahap 2 berhasil dijalankan. Seluruh 20.000 baris anime dipertahankan dan tidak ada penghapusan baris karena missing value.

## Ringkasan Sebelum dan Sesudah

| Metrik | Sebelum | Sesudah |
|---|---:|---:|
| Baris | 20.000 | 20.000 |
| Kolom | 50 | 56 |
| Duplicate `mal_id` | 0 | 0 |
| `mal_id` unik | Ya | Ya |
| Rating MAL tidak valid | 0 | 0 |
| Rating AniList tidak valid | 0 | 0 |
| Episode negatif | 0 | 0 |
| `season` tidak ternormalisasi | Ada campuran huruf besar/kecil | Semua nilai tersedia dalam lowercase |
| Ukuran Parquet | Tidak ada | 7.831.826 bytes |

Enam kolom baru ditambahkan:

- `release_decade`
- `genre_list`
- `genre_count`
- `studio_list`
- `studio_count`
- `score_difference`

Kolom lama tetap dipertahankan. Genre dan daftar studio juga tetap tersedia dalam format teks asli pada kolom `genres` dan `studios_all`.

## Perlakuan Missing Value

Tidak ada nilai missing yang diganti dengan angka atau label yang merepresentasikan fakta buatan. Missing value pada skor, rating, ranking, popularitas, tahun, studio, dan atribut anime tetap mempertahankan nilai missing.

Penanganan khusus:

- `season` ditrims dan dinormalisasikan ke lowercase. Nilai kosong tetap missing.
- Nilai teks kosong atau whitespace dikonversi menjadi missing.
- `streaming_platforms` yang kosong tetap missing dan tidak diartikan sebagai anime yang tidak tersedia.
- `studio_main` bernilai `Unknown` atau kosong tidak dipakai sebagai studio valid dalam fitur ranking.
- `genres` dipisah berdasarkan delimiter `|`; nilai Unknown dibuang dari daftar genre turunan, sedangkan kolom `genres` asli tidak diubah selain normalisasi whitespace.
- `episodes = 0` dipertahankan sebagai nilai sumber. Nilai tersebut tidak ditafsirkan sebagai episode positif atau dibuat menjadi missing.
- Tahun yang tersedia digunakan untuk menghitung `release_decade`; anime tanpa tahun mempertahankan decade sebagai missing.
- `score_difference` dihitung sebagai `mal_score - anilist_score`. Perbandingan ini tidak mencampur dua skala label: kedua nilai bersumber dari skala 10 pada kolom terkait.

## Tipe Data dan Validasi

Konversi dilakukan untuk:

- ID dan penghitung menggunakan tipe integer nullable.
- Tahun, skor, ranking, durasi, dan popularity menggunakan tipe numerik.
- Kolom platform boolean dikonversi ke boolean.
- `genre_list` disimpan sebagai list/array pada kolom Parquet.
- `genre_count` dan `studio_count` disimpan sebagai integer.

Validasi pembacaan ulang Parquet berhasil:

- 20.000 baris.
- 56 kolom.
- `mal_id` tetap unik.
- Tidak ada skor MAL/AniList di luar rentang 0-10.
- Tidak ada episode negatif.
- Semua nilai season terisi yang tersedia adalah `fall`, `spring`, `summer`, atau `winter`.
- 939 baris memiliki `release_decade` missing karena tahun sumbernya missing.

## Daftar Nilai Missing Setelah Cleaning

Missing dipertahankan pada kolom sumber yang tidak tersedia, termasuk:

- `anilist_id`: 2.418
- `title_japanese`: 73
- `title_synonyms`: 8.485
- `source`: 1.165
- `age_rating`: 67
- `season`/`year`: 939
- `duration_min`: 365
- `mal_rank`: 4.873
- `anilist_score`: 3.484
- `streaming_platforms`: 12.632

## Arti Format Unknown dan Tidak Tercatat

Nilai `Unknown` pada studio atau jenis data tidak dipromosikan menjadi studio, genre, atau kategori yang sah. Kolom platform boolean dipertahankan sebagai indikator keberadaan platform. Nilai false pada kolom platform dan teks `streaming_platforms` yang kosong tetap diperlakukan berbeda pada analisis dashboard.

## Reproduksibilitas

Pipeline dapat dijalankan kembali melalui:

```bash
python scripts/clean_dataset.py
```

File keluaran selalu ditulis ulang ke `data/processed/anime_clean.parquet`.

## Berkas Tahap 2

- `src/preprocessing.py`
- `scripts/clean_dataset.py`
- `data/processed/anime_clean.parquet`
- `data/processed/phase2_validation.json`
