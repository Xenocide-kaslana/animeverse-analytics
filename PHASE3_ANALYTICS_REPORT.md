# Tahap 3 - Analytics Engine

## Status
Semua modul analytics berhasil dibuat dan diuji dengan dataset Parquet hasil Tahap 2.

## KPI Executive Overview

- Total anime: **20,000**
- Rata-rata MAL score: **6.42**
- Total studio valid unik: **1,243**
- Rata-rata MAL members: **59,556.85**
- Total genre unik: **78**
- Persentase anime dengan platform streaming tercatat: **36.84%**

## Ranking Genre

| genre | anime_count |
|---|---|
| Comedy | 5,949 |
| Action | 4,150 |
| Fantasy | 4,047 |
| Music | 3,479 |
| Adventure | 3,247 |
| Sci-Fi | 2,839 |
| Drama | 2,505 |
| Shounen | 2,166 |
| School | 2,085 |
| Romance | 2,068 |

### Genre dengan Rata-rata MAL Score

| genre | anime_count | average_mal_score |
|---|---|---|
| Iyashikei | 174 | 7.44 |
| Award Winning | 233 | 7.32 |
| Love Polygon | 107 | 7.28 |
| Love Status Quo | 44 | 7.27 |
| Urban Fantasy | 203 | 7.22 |
| Childcare | 69 | 7.21 |
| Otaku Culture | 102 | 7.18 |
| Adult Cast | 729 | 7.18 |
| Gag Humor | 263 | 7.14 |
| Showbiz | 50 | 7.14 |
| CGDCT | 255 | 7.13 |
| Shounen | 2,166 | 7.08 |
| Organized Crime | 105 | 7.07 |
| Suspense | 426 | 7.03 |
| Detective | 237 | 7.02 |
| Reincarnation | 151 | 7.02 |
| Time Travel | 152 | 7.01 |
| Survival | 75 | 7.01 |
| Mystery | 939 | 6.99 |
| Performing Arts | 145 | 6.96 |
| Medical | 46 | 6.95 |
| Gore | 262 | 6.91 |
| High Stakes Game | 58 | 6.90 |
| Isekai | 452 | 6.89 |
| Seinen | 1,134 | 6.89 |
| Drama | 2,505 | 6.88 |
| School | 2,085 | 6.87 |
| Romance | 2,068 | 6.86 |
| Team Sports | 270 | 6.86 |
| Visual Arts | 90 | 6.86 |
| Martial Arts | 629 | 6.85 |
| Military | 668 | 6.85 |
| Workplace | 207 | 6.85 |
| Mahou Shoujo | 311 | 6.84 |
| Vampire | 175 | 6.84 |
| Psychological | 443 | 6.83 |
| Shoujo | 508 | 6.82 |
| Historical | 1,307 | 6.80 |
| Mythology | 505 | 6.78 |
| Josei | 155 | 6.78 |
| Action | 4,150 | 6.77 |
| Magical Sex Shift | 32 | 6.77 |
| Supernatural | 1,389 | 6.76 |
| Harem | 484 | 6.75 |
| Adventure | 3,247 | 6.75 |
| Delinquents | 69 | 6.74 |
| Super Power | 600 | 6.72 |
| Sports | 669 | 6.71 |
| Combat Sports | 96 | 6.69 |
| Samurai | 227 | 6.69 |
| Girls Love | 121 | 6.67 |
| Crossdressing | 62 | 6.64 |
| Fantasy | 4,047 | 6.63 |
| Gourmet | 170 | 6.61 |
| Idols (Female) | 347 | 6.60 |
| Space | 554 | 6.60 |
| Sci-Fi | 2,839 | 6.58 |
| Reverse Harem | 80 | 6.58 |
| Anthropomorphic | 370 | 6.58 |
| Racing | 173 | 6.57 |
| Video Game | 153 | 6.56 |
| Mecha | 1,099 | 6.55 |
| Boys Love | 192 | 6.55 |
| Comedy | 5,949 | 6.49 |
| Pets | 112 | 6.47 |
| Slice of Life | 913 | 6.47 |
| Idols (Male) | 153 | 6.44 |
| Ecchi | 806 | 6.43 |
| Strategy Game | 316 | 6.30 |
| Parody | 693 | 6.29 |
| Educational | 81 | 6.25 |
| Horror | 515 | 6.22 |
| Hentai | 1,626 | 6.17 |
| Music | 3,479 | 6.05 |
| Erotica | 82 | 6.03 |
| Kids | 1,746 | 5.94 |
| Avant Garde | 649 | 5.29 |

## Ranking Studio

### Studio berdasarkan jumlah anime

| studio | anime_count |
|---|---|
| Toei Animation | 819 |
| Sunrise | 579 |
| J.C.STAFF | 395 |
| Production I.G | 376 |
| MADHOUSE | 356 |
| TMS Entertainment | 318 |
| Studio Pierrot | 297 |
| OLM | 285 |
| Studio DEEN | 277 |
| A-1 Pictures | 258 |

### Studio berdasarkan rata-rata MAL score (minimal 5 anime)

| studio | anime_count | average_mal_score |
|---|---|---|
| Studio Bind | 10 | 8.00 |
| Shenman Entertainment | 11 | 7.90 |
| Sharefun Studio | 7 | 7.82 |
| Red Dog Culture House | 6 | 7.78 |
| bones film | 7 | 7.77 |
| CMC Media | 6 | 7.71 |
| Shuka | 24 | 7.68 |
| Motion Magic | 19 | 7.67 |
| Studio Kafka | 5 | 7.66 |
| Original Force | 13 | 7.65 |

## Popularitas dan Rating

- Korelasi Pearson MAL score dan MAL members: **0.3782** pada 20,000 anime.
- Korelasi menjelaskan hubungan linear dan bukan hubungan sebab-akibat.

### Top Anime Berdasarkan MAL Score

| title_english | mal_score | mal_members | mal_favorites |
|---|---|---|---|
| Frieren: Beyond Journey's End | 9.25 | 1,507,544 | 92,998 |
| Fullmetal Alchemist: Brotherhood | 9.11 | 3,729,776 | 245,350 |
| Re:ZERO -Starting Life in Another World- Season 4 | 9.11 | 320,372 | 8,067 |
| Steel Ball Run: JoJo's Bizarre Adventure | 9.08 | 230,990 | 7,940 |
| Bleach: Thousand-Year Blood War - The Calamity | 9.08 | 155,276 | 2,073 |
| Steins;Gate | 9.07 | 2,847,605 | 204,723 |
| Attack on Titan Season 3 Part 2 | 9.05 | 2,634,317 | 63,953 |
| Gintama Season 4 | 9.05 | 698,568 | 17,639 |
| Chainsaw Man – The Movie: Reze Arc | 9.05 | 542,148 | 15,383 |
| Gintama: The Very Final | 9.05 | 187,969 | 4,727 |

### Top Anime Berdasarkan MAL Members

| title_english | mal_members | mal_score |
|---|---|---|
| Attack on Titan | 4,419,401 | 8.58 |
| Death Note | 4,357,262 | 8.62 |
| Fullmetal Alchemist: Brotherhood | 3,729,776 | 9.11 |
| One-Punch Man | 3,554,821 | 8.47 |
| Demon Slayer: Kimetsu no Yaiba | 3,501,634 | 8.39 |
| My Hero Academia | 3,345,854 | 7.82 |
| Sword Art Online | 3,331,157 | 7.23 |
| Hunter x Hunter | 3,235,560 | 9.03 |
| Naruto | 3,154,253 | 8.02 |
| Jujutsu Kaisen | 3,102,243 | 8.49 |

### Top Anime Berdasarkan Favorites

| title_english | mal_favorites | mal_members | mal_score |
|---|---|---|---|
| One Piece | 255,706 | 2,722,391 | 8.73 |
| Fullmetal Alchemist: Brotherhood | 245,350 | 3,729,776 | 9.11 |
| Hunter x Hunter | 232,009 | 3,235,560 | 9.03 |
| Steins;Gate | 204,723 | 2,847,605 | 9.07 |
| Attack on Titan | 191,806 | 4,419,401 | 8.58 |
| Death Note | 187,637 | 4,357,262 | 8.62 |
| Naruto Shippuden | 121,670 | 2,783,770 | 8.29 |
| Neon Genesis Evangelion | 119,800 | 2,060,381 | 8.37 |
| Code Geass: Lelouch of the Rebellion | 118,905 | 2,505,647 | 8.71 |
| A Silent Voice | 97,307 | 2,656,625 | 8.93 |

## Analisis Platform

| platform | true_count | false_count | unknown_count |
|---|---|---|---|
| Crunchyroll | 3,546 | 3,822 | 12,632 |
| Netflix | 934 | 6,434 | 12,632 |
| HiDive | 422 | 6,946 | 12,632 |
| Funimation | 0 | 7,368 | 12,632 |
| Amazon Prime | 432 | 6,936 | 12,632 |
| Disney+ | 69 | 7,299 | 12,632 |
| Hulu | 808 | 6,560 | 12,632 |
| VRV | 0 | 7,368 | 12,632 |
| Bilibili | 395 | 6,973 | 12,632 |
| YouTube | 2,637 | 4,731 | 12,632 |

| platform | average_mal_score | sample_count |
|---|---|---|
| Netflix | 7.56 | 934 |
| Hulu | 7.34 | 808 |
| Disney+ | 7.32 | 69 |
| Amazon Prime | 7.27 | 432 |
| HiDive | 7.13 | 422 |
| Crunchyroll | 7.09 | 3,546 |
| Bilibili | 7.01 | 395 |
| YouTube | 6.72 | 2,637 |
| Funimation | N/A | 0 |
| VRV | N/A | 0 |

### Distribusi Jumlah Platform

| platform_count | anime_count |
|---|---|
| Unknown/missing | 12,632 |
| 1 | 4,339 |
| 2 | 1,476 |
| 0 | 975 |
| 3 | 405 |
| 4 | 132 |
| 5 | 37 |
| 6 | 4 |

Nilai `unknown_count` berasal dari `streaming_platforms` yang tidak tercatat. Nilai tersebut tidak ditafsirkan sebagai `False`.

## Validasi Dataset

- Jumlah baris: **20,000**
- `mal_id` unik: **20,000**
- Anime tanpa MAL score: **0**
- Anime tanpa studio valid: **4,044**
- Anime tanpa year: **939**
- Genre hasil ekstraksi: **78**
- Studio hasil ekstraksi: **1,243**

## Insight Aktual

- Tipe anime terbanyak adalah TV dengan 5,449 anime.
- Tahun dengan produksi terbanyak adalah 2021 dengan 866 anime.
- Genre paling sering muncul adalah Comedy pada 5,949 anime.
- Studio dengan produksi terbanyak adalah Toei Animation dengan 819 anime.
- Genre dengan rata-rata MAL score tertinggi pada sampel minimal 30 anime adalah Iyashikei (7.44 dari 174 anime).
- Hubungan MAL score dengan mal_members memiliki korelasi Pearson positif sebesar 0.378 pada 20,000 anime; ini bukan bukti sebab-akibat.

## Fungsi yang Disediakan

- `src/analytics.py`: KPI, tren, distribusi, ranking, korelasi, validasi, dan insight.
- `src/genre_analysis.py`: ekstraksi dan agregasi genre serta korelasi genre.
- `src/studio_analysis.py`: peringkat dan agregasi studio.
- `src/streaming_analysis.py`: analisis platform, skor, dan genre.
- `src/config.py`: path, platform, dan batas minimum analitik.
