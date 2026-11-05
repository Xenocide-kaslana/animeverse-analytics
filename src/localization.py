from __future__ import annotations

LABELS = {
    "Executive Overview": "Ringkasan Utama",
    "Anime Trends": "Tren Anime",
    "Rating & Popularity": "Rating & Popularitas",
    "Studio & Genre": "Studio & Genre",
    "Streaming Analysis": "Analisis Platform Streaming",
    "Appearance": "Tampilan",
    "Light": "Terang",
    "Dark": "Gelap",
    "Global Filters": "Filter Utama",
    "Release Year": "Tahun Rilis",
    "Anime Type": "Jenis Anime",
    "Season": "Musim Tayang",
    "Genre": "Genre",
    "Studio": "Studio",
    "Reset Filters": "Atur Ulang Filter",
    "Download CSV": "Unduh CSV",
    "Download Filtered CSV": "Unduh CSV Filtered",
    "Search": "Cari",
    "Search Anime": "Cari Anime",
    "Search table": "Cari tabel",
    "Sort By": "Urutkan Berdasarkan",
    "Ascending": "Urutan Naik",
    "Previous": "Sebelumnya",
    "Next": "Berikutnya",
    "Page": "Halaman",
    "No Data Available": "Data Tidak Tersedia",
    "No Results Found": "Tidak Ada Hasil yang Ditemukan",
    "Anime Details": "Detail Anime",
    "English Title": "Judul Inggris",
    "Romaji Title": "Judul Romaji",
    "Japanese Title": "Judul Jepang",
    "Synopsis": "Sinopsis",
    "Episode Count": "Jumlah Episode",
    "Duration": "Durasi",
    "Members": "Jumlah Anggota",
    "Favorites": "Favorit",
    "Ranking": "Peringkat",
    "Streaming Platforms": "Platform Streaming",
    "No Image Available": "Gambar Tidak Tersedia",
    "Select anime": "Pilih anime",
    "Total Anime": "Jumlah Anime",
    "Average MAL Score": "Rata-rata Skor MAL",
    "Valid Studios": "Jumlah Studio Valid",
    "Average MAL Members": "Rata-rata Anggota MAL",
    "Filtered records": "Data Setelah Difilter",
    "Available scores": "Data Skor Tersedia",
    "Industry Overview": "Ringkasan Industri",
    "Dynamic Key Insights": "Insight Utama",
    "Release Activity": "Aktivitas Rilis",
    "Format and Production": "Format dan Produksi",
    "Rankings": "Peringkat",
    "Score and Popularity Analysis": "Analisis Skor dan Popularitas",
    "Studio Rankings": "Peringkat Studio",
    "Genre Analysis": "Analisis Genre",
    "Platform Coverage": "Cakupan Platform",
    "Platform Reach": "Jangkauan Platform",
    "Multi-platform Anime": "Anime Multi-platform",
}

AXIS_LABELS = {
    "year": "Tahun",
    "decade": "Dekade",
    "anime_count": "Jumlah Anime",
    "type": "Jenis Anime",
    "season": "Musim Tayang",
    "source": "Jenis Sumber",
    "episodes": "Jumlah Episode",
    "mal_score": "Skor MAL",
    "score": "Skor",
    "anilist_score": "Skor AniList",
    "score_tier": "Kategori Skor",
    "popularity_tier": "Kategori Popularitas",
    "genre": "Genre",
    "studio": "Studio",
    "average_mal_score": "Rata-rata Skor MAL",
    "mal_members": "Jumlah Anggota MAL",
    "platform": "Platform Streaming",
    "platform_count": "Jumlah Platform",
}


def format_number(value, decimals: int = 0) -> str:
    text = f"{float(value):,.{decimals}f}"
    if "," in text:
        text = text.replace(",", "TEMP_THOUSAND")
        text = text.replace(".", "TEMP_DECIMAL")
        text = text.replace("TEMP_THOUSAND", ".")
        text = text.replace("TEMP_DECIMAL", ",")
    return text.rstrip("0").rstrip(",") if decimals and text.endswith(("0", ",")) else text


def t(text: str) -> str:
    return LABELS.get(text, text)
