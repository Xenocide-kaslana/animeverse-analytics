from __future__ import annotations

from pathlib import Path
import re

import numpy as np
import pandas as pd


TEXT_COLUMNS = [
    "title_english", "title_romaji", "title_japanese", "title_synonyms",
    "type", "source", "status", "age_rating", "season", "studio_main",
    "studios_all", "genres", "top_tags", "streaming_platforms",
    "season_year",
]

PLATFORM_COLUMNS = [
    "is_crunchyroll", "is_netflix", "is_hidive", "is_funimation",
    "is_amazon_prime", "is_disney_plus", "is_hulu", "is_vrv",
    "is_bilibili", "is_youtube",
]


def _clean_text(value: object) -> object:
    if pd.isna(value):
        return pd.NA
    text = re.sub(r"\s+", " ", str(value).strip())
    return text if text else pd.NA


def _split_pipe(value: object) -> list[str]:
    if pd.isna(value):
        return []
    items = []
    for item in str(value).split("|"):
        cleaned = _clean_text(item)
        if pd.notna(cleaned) and cleaned.lower() != "unknown" and cleaned not in items:
            items.append(str(cleaned))
    return items


def normalize_categorical(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for column in TEXT_COLUMNS:
        if column in df:
            df[column] = df[column].map(_clean_text)

    if "season" in df:
        df["season"] = df["season"].map(
            lambda value: str(value).lower() if pd.notna(value) else pd.NA
        )

    for column in ["type", "source", "status", "age_rating", "studio_main", "score_tier", "popularity_tier"]:
        if column in df:
            df[column] = df[column].str.strip()

    return df


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = normalize_categorical(df)

    integer_columns = [
        "mal_id", "episodes", "mal_scored_by", "mal_members",
        "mal_favorites", "num_platforms",
    ]
    float_columns = [
        "anilist_id", "year", "decade", "duration_min", "mal_score",
        "mal_rank", "mal_popularity", "anilist_score", "anilist_score_100",
        "anilist_favorites", "anilist_popularity", "score_gap_mal_anilist",
    ]

    for column in integer_columns:
        if column in df:
            df[column] = pd.to_numeric(df[column], errors="coerce").astype("Int64")
    for column in float_columns:
        if column in df:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    for column in PLATFORM_COLUMNS:
        if column in df:
            df[column] = df[column].fillna(False).astype(bool)

    boolean_columns = ["is_adult", "is_long_running", "is_movie"]
    for column in boolean_columns:
        if column in df:
            df[column] = df[column].fillna(False).astype(bool)

    df["release_decade"] = pd.Series(
        pd.NA, index=df.index, dtype="Int64"
    )
    valid_year = df["year"].notna()
    df.loc[valid_year, "release_decade"] = (
        np.floor(df.loc[valid_year, "year"] / 10.0) * 10
    ).astype("int64")
    df["release_decade"] = pd.array(df["release_decade"], dtype="Int64")

    df["genre_list"] = df["genres"].map(_split_pipe)
    df["genre_count"] = df["genre_list"].map(len).astype("int32")
    df["studio_list"] = df["studios_all"].map(_split_pipe)
    df["studio_count"] = df["studio_list"].map(len).astype("int32")
    df["score_difference"] = df["mal_score"] - df["anilist_score"]

    # Preserve zero episode because it may be a valid source representation.
    # Missing ratings and rankings remain missing; no fabricated values are inserted.
    return df


def validate_dataset(raw: pd.DataFrame, clean: pd.DataFrame) -> dict:
    invalid_mal = clean["mal_score"].notna() & ~clean["mal_score"].between(0, 10)
    invalid_anilist = clean["anilist_score"].notna() & ~clean["anilist_score"].between(0, 10)
    invalid_episodes = clean["episodes"].notna() & (clean["episodes"] < 0)

    return {
        "raw_rows": int(len(raw)),
        "clean_rows": int(len(clean)),
        "raw_columns": int(raw.shape[1]),
        "clean_columns": int(clean.shape[1]),
        "mal_id_duplicates": int(clean["mal_id"].duplicated().sum()),
        "row_count_preserved": len(raw) == len(clean),
        "mal_id_unique": clean["mal_id"].is_unique,
        "invalid_mal_scores": int(invalid_mal.sum()),
        "invalid_anilist_scores": int(invalid_anilist.sum()),
        "invalid_negative_episodes": int(invalid_episodes.sum()),
        "season_values": sorted(str(value) for value in clean["season"].dropna().unique()),
        "release_decade_nulls": int(clean["release_decade"].isna().sum()),
        "genre_list_nulls": int(clean["genre_list"].isna().sum()),
        "missing_values": {
            column: int(count)
            for column, count in clean.isna().sum().items() if count > 0
        },
    }


def save_parquet(df: pd.DataFrame, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    # Lists are stored as Arrow list columns for lossless round-trip with PyArrow.
    df.to_parquet(destination, engine="pyarrow", index=False)
