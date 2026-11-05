from pathlib import Path
import sys

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.analytics import (
    data_validation, executive_kpis, generate_insights, load_clean_data,
    mal_score_members_correlation, top_anime_by_favorites,
    top_anime_by_mal_score, top_anime_by_members,
)
from src.config import PLATFORM_COLUMNS, PROCESSED_DATA_PATH
from src.genre_analysis import top_genres, genre_average_score
from src.streaming_analysis import anime_count_per_platform, platform_average_score, platform_count_distribution
from src.studio_analysis import top_studios_by_count, top_studios_by_average_score


def markdown_table(df: pd.DataFrame, columns: list[str], integer_columns: list[str] = []) -> str:
    lines = ["| " + " | ".join(columns) + " |", "|" + "|".join(["---"] * len(columns)) + "|"]
    for _, row in df.iterrows():
        cells = []
        for column in columns:
            value = row[column]
            if pd.isna(value):
                text = "N/A"
            elif column in integer_columns and isinstance(value, (int, float)):
                text = f"{int(value):,}"
            elif isinstance(value, float):
                text = f"{value:.2f}"
            else:
                text = str(value)
            cells.append(text.replace("|", "\\|"))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def main() -> None:
    df = load_clean_data(PROCESSED_DATA_PATH)
    kpis = executive_kpis(df)
    validation = data_validation(df)
    top_genre = top_genres(df)
    genre_rating = genre_average_score(df)
    studios_count = top_studios_by_count(df, 10)
    studios_rating = top_studios_by_average_score(df, 10)
    platform_count = anime_count_per_platform(df)
    platform_rating = platform_average_score(df)
    platform_distribution = platform_count_distribution(df)
    insights = generate_insights(df)
    correlation = mal_score_members_correlation(df)

    sections = [
        "# Tahap 3 - Analytics Engine",
        "",
        "## Status",
        "Semua modul analytics berhasil dibuat dan diuji dengan dataset Parquet hasil Tahap 2.",
        "",
        "## KPI Executive Overview",
        "",
        f"- Total anime: **{kpis['total_anime']:,}**",
        f"- Rata-rata MAL score: **{kpis['average_mal_score']:.2f}**",
        f"- Total studio valid unik: **{kpis['total_valid_studios']:,}**",
        f"- Rata-rata MAL members: **{kpis['average_mal_members']:,.2f}**",
        f"- Total genre unik: **{kpis['total_unique_genres']:,}**",
        f"- Persentase anime dengan platform streaming tercatat: **{kpis['streaming_recorded_percent']:.2f}%**",
        "",
        "## Ranking Genre",
        "",
        markdown_table(top_genre, ["genre", "anime_count"], ["anime_count"]),
        "",
        "### Genre dengan Rata-rata MAL Score",
        "",
        markdown_table(genre_rating, ["genre", "anime_count", "average_mal_score"], ["anime_count"]),
        "",
        "## Ranking Studio",
        "",
        "### Studio berdasarkan jumlah anime",
        "",
        markdown_table(studios_count, ["studio", "anime_count"], ["anime_count"]),
        "",
        "### Studio berdasarkan rata-rata MAL score (minimal 5 anime)",
        "",
        markdown_table(studios_rating, ["studio", "anime_count", "average_mal_score"], ["anime_count"]),
        "",
        "## Popularitas dan Rating",
        "",
        f"- Korelasi Pearson MAL score dan MAL members: **{correlation['pearson_correlation']:.4f}** pada {correlation['n']:,} anime.",
        "- Korelasi menjelaskan hubungan linear dan bukan hubungan sebab-akibat.",
        "",
        "### Top Anime Berdasarkan MAL Score",
        "",
        markdown_table(
            top_anime_by_mal_score(df, 10),
            ["title_english", "mal_score", "mal_members", "mal_favorites"],
            ["mal_members", "mal_favorites"],
        ),
        "",
        "### Top Anime Berdasarkan MAL Members",
        "",
        markdown_table(
            top_anime_by_members(df, 10),
            ["title_english", "mal_members", "mal_score"],
            ["mal_members"],
        ),
        "",
        "### Top Anime Berdasarkan Favorites",
        "",
        markdown_table(
            top_anime_by_favorites(df, 10),
            ["title_english", "mal_favorites", "mal_members", "mal_score"],
            ["mal_favorites", "mal_members"],
        ),
        "",
        "## Analisis Platform",
        "",
        markdown_table(platform_count, ["platform", "true_count", "false_count", "unknown_count"], ["true_count", "false_count", "unknown_count"]),
        "",
        markdown_table(platform_rating, ["platform", "average_mal_score", "sample_count"], ["sample_count"]),
        "",
        "### Distribusi Jumlah Platform",
        "",
        markdown_table(platform_distribution, ["platform_count", "anime_count"], ["platform_count", "anime_count"]),
        "",
        "Nilai `unknown_count` berasal dari `streaming_platforms` yang tidak tercatat. Nilai tersebut tidak ditafsirkan sebagai `False`.",
        "",
        "## Validasi Dataset",
        "",
        f"- Jumlah baris: **{validation['row_count']:,}**",
        f"- `mal_id` unik: **{validation['unique_mal_id_count']:,}**",
        f"- Anime tanpa MAL score: **{validation['anime_without_mal_score']:,}**",
        f"- Anime tanpa studio valid: **{validation['anime_without_valid_studio']:,}**",
        f"- Anime tanpa year: **{validation['anime_without_year']:,}**",
        f"- Genre hasil ekstraksi: **{validation['extracted_genre_count']:,}**",
        f"- Studio hasil ekstraksi: **{validation['extracted_studio_count']:,}**",
        "",
        "## Insight Aktual",
        "",
        *[f"- {insight}" for insight in insights],
        "",
        "## Fungsi yang Disediakan",
        "",
        "- `src/analytics.py`: KPI, tren, distribusi, ranking, korelasi, validasi, dan insight.",
        "- `src/genre_analysis.py`: ekstraksi dan agregasi genre serta korelasi genre.",
        "- `src/studio_analysis.py`: peringkat dan agregasi studio.",
        "- `src/streaming_analysis.py`: analisis platform, skor, dan genre.",
        "- `src/config.py`: path, platform, dan batas minimum analitik.",
    ]
    report = ROOT / "PHASE3_ANALYTICS_REPORT.md"
    report.write_text("\n".join(sections) + "\n", encoding="utf-8")
    print(f"Saved: {report}")


if __name__ == "__main__":
    main()
