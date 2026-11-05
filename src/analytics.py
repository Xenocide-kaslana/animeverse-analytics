import json
from pathlib import Path

import numpy as np
import pandas as pd

from src.config import MIN_RATING_MEMBERS, PLATFORM_COLUMNS


def safe_mean(series: pd.Series) -> float | None:
    numeric = pd.to_numeric(series, errors="coerce").dropna()
    if numeric.empty:
        return None
    value = numeric.mean()
    return None if pd.isna(value) else float(value)


def _numeric_column(df: pd.DataFrame, column: str) -> pd.Series:
    if column not in df.columns:
        raise KeyError(f"Kolom dataset tidak ditemukan: {column}")
    return pd.to_numeric(df[column], errors="coerce")


def rank_anime(
    df: pd.DataFrame,
    column: str,
    n: int = 10,
    *,
    min_members: int = 0,
    ascending: bool = False,
) -> pd.DataFrame:
    allowed_columns = {
        "mal_score", "mal_members", "mal_favorites", "mal_popularity", "mal_rank"
    }
    if column not in allowed_columns:
        raise KeyError(f"Kolom peringkat tidak didukung: {column}")
    if df.empty:
        return df.head(0)

    ranking = df.copy()
    ranking[column] = _numeric_column(ranking, column)
    ranking["mal_members"] = _numeric_column(ranking, "mal_members")
    ranking["mal_score"] = _numeric_column(ranking, "mal_score")
    ranking = ranking.loc[ranking[column].notna()]
    if column != "mal_members":
        ranking = ranking.loc[ranking["mal_members"].fillna(0).ge(min_members)]
    return ranking.sort_values(
        [column, "mal_score", "mal_id"],
        ascending=[ascending, False, True],
        na_position="last",
    ).head(max(n, 0)).reset_index(drop=True)


def load_clean_data(path: Path | str) -> pd.DataFrame:
    df = pd.read_parquet(path)
    df.attrs["source"] = str(path)
    return df


def executive_kpis(df: pd.DataFrame) -> dict:
    valid_studios = df["studio_main"].dropna().astype(str).str.strip()
    valid_studios = valid_studios[~valid_studios.str.lower().isin(["", "unknown"])]
    recorded_streaming = df["streaming_platforms"].notna()
    genres = set()
    for value in df["genre_list"].dropna():
        genres.update(str(item) for item in value)
    return {
        "total_anime": int(len(df)),
        "average_mal_score": safe_mean(df["mal_score"]),
        "total_valid_studios": int(valid_studios.nunique()),
        "average_mal_members": safe_mean(df["mal_members"]),
        "total_unique_genres": len(genres),
        "anime_by_status": df["status"].value_counts(dropna=True).to_dict(),
        "streaming_recorded_percent": float(recorded_streaming.mean() * 100) if len(recorded_streaming) else 0.0,
        "anime_by_type": df["type"].value_counts(dropna=True).to_dict(),
    }


def count_by_year(df: pd.DataFrame) -> pd.DataFrame:
    return df["year"].dropna().value_counts().sort_index().rename_axis("year").reset_index(name="anime_count")


def count_by_decade(df: pd.DataFrame) -> pd.DataFrame:
    return df["release_decade"].dropna().value_counts().sort_index().rename_axis("decade").reset_index(name="anime_count")


def count_by_season(df: pd.DataFrame) -> pd.DataFrame:
    return df["season"].value_counts(dropna=True).rename_axis("season").reset_index(name="anime_count")


def count_by_type(df: pd.DataFrame) -> pd.DataFrame:
    return df["type"].value_counts(dropna=True).rename_axis("type").reset_index(name="anime_count")


def count_by_source(df: pd.DataFrame) -> pd.DataFrame:
    return df["source"].value_counts(dropna=True).rename_axis("source").reset_index(name="anime_count")


def episode_distribution(df: pd.DataFrame, valid_only: bool = True) -> pd.DataFrame:
    values = df["episodes"]
    if valid_only:
        values = values[(values.notna()) & (values > 0)]
    return values.value_counts().sort_index().rename_axis("episodes").reset_index(name="anime_count")


def mal_score_distribution(df: pd.DataFrame) -> pd.DataFrame:
    return df["mal_score"].dropna().value_counts().sort_index().rename_axis("mal_score").reset_index(name="anime_count")


def score_tier_distribution(df: pd.DataFrame) -> pd.DataFrame:
    return df["score_tier"].value_counts(dropna=True).rename_axis("score_tier").reset_index(name="anime_count")


def popularity_tier_distribution(df: pd.DataFrame) -> pd.DataFrame:
    return df["popularity_tier"].value_counts(dropna=True).rename_axis("popularity_tier").reset_index(name="anime_count")


def top_anime_by_mal_score(
    df: pd.DataFrame, n: int = 20, min_members: int = MIN_RATING_MEMBERS
) -> pd.DataFrame:
    return (
        rank_anime(df, "mal_score", n, min_members=min_members)
        .sort_values(["mal_score", "mal_members", "mal_id"], ascending=[False, False, True])
        .head(n)[["mal_id", "title_english", "mal_score", "mal_members", "mal_favorites", "studio_main"]]
        .reset_index(drop=True)
    )


def top_anime_by_members(df: pd.DataFrame, n: int = 20) -> pd.DataFrame:
    ranking = df.copy()
    ranking["mal_members"] = _numeric_column(ranking, "mal_members")
    ranking["mal_score"] = _numeric_column(ranking, "mal_score")
    return ranking.dropna(subset=["mal_members"]).sort_values(
        ["mal_members", "mal_score", "mal_id"], ascending=[False, False, True]
    ).head(n)[["mal_id", "title_english", "mal_members", "mal_score", "mal_favorites", "studio_main"]].reset_index(drop=True)


def top_anime_by_favorites(df: pd.DataFrame, n: int = 20) -> pd.DataFrame:
    ranking = df.copy()
    ranking["mal_favorites"] = _numeric_column(ranking, "mal_favorites")
    ranking["mal_members"] = _numeric_column(ranking, "mal_members")
    ranking["mal_score"] = _numeric_column(ranking, "mal_score")
    return ranking.dropna(subset=["mal_favorites"]).sort_values(
        ["mal_favorites", "mal_members", "mal_id"], ascending=[False, False, True]
    ).head(n)[["mal_id", "title_english", "mal_favorites", "mal_members", "mal_score", "studio_main"]].reset_index(drop=True)


def mal_score_members_correlation(df: pd.DataFrame) -> dict:
    sample = df[["mal_score", "mal_members"]].dropna()
    numeric_correlation = None if len(sample) < 2 else sample["mal_score"].corr(sample["mal_members"])
    correlation = None if pd.isna(numeric_correlation) else float(numeric_correlation)
    return {"n": int(len(sample)), "pearson_correlation": correlation}


def mal_vs_anilist_comparison(df: pd.DataFrame) -> pd.DataFrame:
    sample = df.dropna(subset=["mal_score", "anilist_score"]).copy()
    sample["difference_mal_minus_anilist"] = sample["mal_score"] - sample["anilist_score"]
    return sample[["mal_id", "title_english", "mal_score", "anilist_score", "difference_mal_minus_anilist"]]


def data_validation(df: pd.DataFrame) -> dict:
    valid_studio = df["studio_main"].dropna().astype(str).str.strip()
    valid_studio = valid_studio[~valid_studio.str.lower().isin(["", "unknown"])]
    return {
        "row_count": len(df),
        "unique_mal_id_count": int(df["mal_id"].nunique()),
        "missing_values": {column: int(count) for column, count in df.isna().sum().items() if count},
        "anime_without_mal_score": int(df["mal_score"].isna().sum()),
        "anime_without_valid_studio": int(len(df) - valid_studio.reindex(df.index).notna().sum()),
        "anime_without_year": int(df["year"].isna().sum()),
        "extracted_genre_count": int(df["genre_list"].explode().dropna().nunique()),
        "extracted_studio_count": int(valid_studio.nunique()),
    }


def generate_insights(df: pd.DataFrame) -> list[str]:
    insights = []
    types = count_by_type(df)
    years = count_by_year(df)
    genres = __import__("src.genre_analysis", fromlist=["top_genres"]).top_genres(df, 1)
    studios = __import__("src.studio_analysis", fromlist=["top_studios_by_count"]).top_studios_by_count(df, 1)
    genre_scores = __import__("src.genre_analysis", fromlist=["genre_average_score"]).genre_average_score(df)

    if not types.empty:
        insights.append(f"Tipe anime terbanyak adalah {types.iloc[0]['type']} dengan {int(types.iloc[0]['anime_count']):,}".replace(",", ".") + " anime.")
    if not years.empty:
        busiest_year = years.loc[years["anime_count"].idxmax()]
        insights.append(f"Tahun dengan produksi terbanyak adalah {int(busiest_year['year'])} dengan {int(busiest_year['anime_count']):,}".replace(",", ".") + " anime.")
    if not genres.empty:
        insights.append(f"Genre paling sering muncul adalah {genres.iloc[0]['genre']} pada {int(genres.iloc[0]['anime_count']):,}".replace(",", ".") + " anime.")
    if not studios.empty:
        insights.append(f"Studio dengan produksi terbanyak adalah {studios.iloc[0]['studio']} dengan {int(studios.iloc[0]['anime_count']):,}".replace(",", ".") + " anime.")
    if not genre_scores.empty:
        row = genre_scores.iloc[0]
        average_score = pd.to_numeric(pd.Series([row["average_mal_score"]]), errors="coerce").iloc[0]
        if pd.isna(average_score):
            return insights
        insights.append(
            f"Genre dengan rata-rata MAL score tertinggi pada sampel minimal {30} anime adalah {row['genre']} "
            f"({float(average_score):.2f}".replace(".", ",") + f" dari {int(row['anime_count']):,}".replace(",", ".") + " anime)."
        )
    correlation = mal_score_members_correlation(df)["pearson_correlation"]
    if correlation is not None and len(df) > 1:
        strength = "positif" if correlation > 0 else "negatif"
        insights.append(
            f"Hubungan MAL score dengan mal_members memiliki korelasi Pearson {strength} sebesar {correlation:.3f}".replace(".", ",")
            + f" pada {int(mal_score_members_correlation(df)['n']):,}".replace(",", ".") + " anime; ini bukan bukti sebab-akibat."
        )
    return insights
